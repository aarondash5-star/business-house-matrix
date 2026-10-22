import test from 'node:test';
import assert from 'node:assert/strict';
import {
  AW1_TAG_ID, AutomationWindowBlocked, validateLease, tagText,
  createVisibleWindowGuard, renderAutomationWindowTag, inspectAutomationWindowTag
} from '../brain/automation/visible_window_tag.mjs';

const lease = (change = {}) => ({
  project: 'PINE-QA', worker: 'DELL', taskId: 'A1-0007',
  mode: 'READ-ONLY', state: 'RUNNING',
  expiresAt: Date.now() + 120000, allowedOrigins: ['https://example.org'],
  ...change
});
class FakePage {
  constructor() { this.closed = false; this.visible = false; this.tag = null; this.init = false; this.url = ''; }
  async addInitScript(spec) { this.init = spec.content.includes('renderAutomationWindowTag') || spec.content.includes('aw1-automation-owner-tag'); }
  async goto(url) { this.url = url; this.visible = this.init && !!this.tag; }
  async evaluate(fn, args) {
    if (fn === renderAutomationWindowTag) {
      this.tag = args; this.visible = true;
      return { installed: true, text: tagText(args) };
    }
    if (fn === inspectAutomationWindowTag)
      return { visible: this.visible, text: this.tag ? tagText(this.tag) : null };
    throw new Error('UNEXPECTED_EVALUATE');
  }
  isClosed() { return this.closed; }
  async close() { this.closed = true; }
}
class Context {
  constructor() { this.pages = []; }
  async newPage() { const p = new FakePage(); this.pages.push(p); return p; }
}
async function fixture(spec = lease()) {
  const context = new Context();
  const guard = createVisibleWindowGuard(context);
  const page = await guard.open(spec, 'https://example.org/allowed');
  return { context, guard, page, spec };
}
function denied(promise, message) {
  return assert.rejects(promise, e => e instanceof AutomationWindowBlocked && e.message.includes(message));
}

test('validates complete task identity and least-privilege scope', () => {
  const a = validateLease(lease());
  assert.equal(tagText(a), 'AUTOMATION | PINE-QA | DELL | A1-0007 | READ-ONLY | RUNNING');
  assert.equal(AW1_TAG_ID, 'aw1-automation-owner-tag');
  assert.ok(Object.isFrozen(a));
  assert.throws(() => validateLease(lease({ project: 'A <script>' })), /INVALID_PROJECT/);
  assert.throws(() => validateLease(lease({ taskId: '' })), /INVALID_TASK/);
  assert.throws(() => validateLease(lease({ expiresAt: Date.now() - 1 })), /STALE_LEASE/);
  assert.throws(() => validateLease(lease({ allowedOrigins: [] })), /INVALID_ORIGIN_ALLOWLIST/);
  assert.throws(() => validateLease(lease({ allowedOrigins: ['http://localhost'] })), /INVALID_ORIGIN_ALLOWLIST/);
});
test('creates only a new disposable automation-owned page', async () => {
  const { context, guard, page, spec } = await fixture();
  assert.equal(context.pages.length, 1);
  assert.equal(page.url, 'https://example.org/allowed');
  await assert.doesNotReject(guard.inspect(page, spec));
  assert.equal(page.tag.state, 'RUNNING');
});
test('never claims a manually supplied page', async () => {
  const { guard, spec } = await fixture();
  const manual = new FakePage();
  manual.tag = lease(); manual.visible = true;
  await denied(guard.run(manual, spec, 'screenshot', () => true), 'UNOWNED_OR_MISMATCHED_WINDOW');
});
test('missing overlay fails closed before any GUI action', async () => {
  const { guard, page, spec } = await fixture();
  let calls = 0;
  page.visible = false;
  await denied(guard.run(page, spec, 'screenshot', () => { calls++; }), 'TAG_NOT_VISIBLE');
  assert.equal(calls, 0);
});
test('forged mode or task cannot override read-only lease', async () => {
  const { guard, page, spec } = await fixture();
  await denied(guard.run(page, { ...spec, mode: 'EDIT-QA' }, 'click', () => true), 'UNOWNED_OR_MISMATCHED_WINDOW');
  await denied(guard.run(page, { ...spec, taskId: 'OTHER' }, 'snapshot', () => true), 'UNOWNED_OR_MISMATCHED_WINDOW');
  await denied(guard.run(page, spec, 'fill', () => true), 'READ_ONLY_ACTION');
});
test('production alerts, broker trades, publishing and shell always refused', async () => {
  const { guard, page, spec } = await fixture(lease({ mode: 'EDIT-QA' }));
  for (const action of ['trade', 'publish', 'production-alert', 'broker-order', 'protected-chart-edit', 'shell', 'cross-project']) {
    await denied(guard.run(page, spec, action, () => true), 'ACTION_FORBIDDEN');
  }
});
test('navigation to allowlisted origin restores tag; foreign navigation refused', async () => {
  const { guard, page, spec } = await fixture();
  await guard.navigate(page, spec, 'https://example.org/another');
  assert.equal(page.url, 'https://example.org/another');
  await assert.doesNotReject(guard.inspect(page, spec));
  await denied(guard.navigate(page, spec, 'https://elsewhere.org/private'), 'DESTINATION_NOT_ALLOWED');
  assert.equal(page.url, 'https://example.org/another');
});
test('origin must be approved before creating page', async () => {
  const context = new Context(); const guard = createVisibleWindowGuard(context);
  await denied(guard.open(lease(), 'https://elsewhere.org/'), 'DESTINATION_NOT_ALLOWED');
  assert.equal(context.pages.length, 0);
});
test('offline UI test may open only its exact pinned local fixture', async () => {
  const context = new Context(), guard = createVisibleWindowGuard(context);
  const spec = lease({ allowedOrigins: [], offlineFixtureUrl: 'file:///tmp/aw1-offline-fixture.html' });
  const page = await guard.open(spec, spec.offlineFixtureUrl);
  await assert.doesNotReject(guard.inspect(page, spec));
  await denied(guard.navigate(page, spec, 'file:///etc/passwd'), 'DESTINATION_NOT_ALLOWED');
  await denied(guard.navigate(page, spec, 'file:///tmp/other-fixture.html'), 'DESTINATION_NOT_ALLOWED');
  assert.equal(page.url, spec.offlineFixtureUrl);
});
test('one-writer blocks parallel actions on same page', async () => {
  const { guard, page, spec } = await fixture(lease({ mode: 'EDIT-QA' }));
  let release;
  const blockedAction = new Promise(r => { release = r; });
  const first = guard.run(page, spec, 'click', async () => { await blockedAction; return 'done'; });
  await new Promise(resolve => setImmediate(resolve));
  await denied(guard.run(page, spec, 'click', () => true), 'SINGLE_WRITER_CONFLICT');
  release();
  assert.equal(await first, 'done');
});
test('completion leaves FINISHED tag and disallows further action', async () => {
  const { guard, page, spec } = await fixture();
  const result = await guard.finish(page, spec);
  assert.equal(result.status, 'FINISHED');
  assert.equal(page.tag.state, 'FINISHED');
  await denied(guard.run(page, spec, 'snapshot', () => true), 'STALE_OR_FINISHED_LEASE');
});
test('lost tag after an action is ambiguous and never silently retried', async () => {
  const { guard, page, spec } = await fixture(lease({ mode: 'EDIT-QA' }));
  let acted = 0;
  await denied(guard.run(page, spec, 'click', async () => { acted++; page.visible = false; }), 'AMBIGUOUS_ACTION_CHECK_RECEIPT');
  assert.equal(acted, 1);
});
test('opening a page with failed render closes only its new disposable page', async () => {
  const context = new Context();
  context.newPage = async () => {
    const p = new FakePage();
    p.evaluate = async () => { throw new Error('inject failed'); };
    context.pages.push(p);
    return p;
  };
  const guard = createVisibleWindowGuard(context);
  await assert.rejects(guard.open(lease(), 'https://example.org/'), /inject failed/);
  assert.ok(context.pages[0].closed);
});
