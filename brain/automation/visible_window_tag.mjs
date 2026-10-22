/**
 * Golden Rule AW-1: persistent, fail-closed identity tag for automation-OWNED pages.
 * This adapter creates its OWN disposable page. It never captures an existing
 * personal window or claims a pre-existing browser tab.
 *
 * Adapter requires browserContext.newPage() and Playwright-compatible page API.
 * No network access, credentials, MCP permissions, or native TradingView writes.
 */
export const AW1_TAG_ID = 'aw1-automation-owner-tag';
export const AW1_MODES = Object.freeze(['READ-ONLY', 'EDIT-QA', 'STAGING']);
export const AW1_STATES = Object.freeze(['READY', 'RUNNING', 'PAUSED', 'BLOCKED', 'FINISHED']);
const MUTATING_ACTIONS = new Set([
  'click', 'fill', 'type', 'press', 'paste', 'upload', 'drag',
  'native-click', 'native-key', 'script-edit', 'publish', 'trade'
]);
const DENIED_ACTIONS = new Set([
  'publish', 'trade', 'broker-order', 'production-alert',
  'protected-chart-edit', 'shell', 'cross-project'
]);

export class AutomationWindowBlocked extends Error {
  constructor(reason) { super('BLOCKED:UNLABELED_WINDOW:' + reason); this.name = 'AutomationWindowBlocked'; }
}
function compact(value, field) {
  if (typeof value !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,39}$/.test(value))
    throw new AutomationWindowBlocked('INVALID_' + field);
  return value;
}
function normalOrigin(s) {
  try {
    const u = new URL(s);
    if (u.protocol !== 'https:' || u.username || u.password || u.hash || u.search) return null;
    return u.origin;
  } catch { return null; }
}
export function validateLease(lease) {
  if (!lease || typeof lease !== 'object' || Array.isArray(lease))
    throw new AutomationWindowBlocked('MISSING_LEASE');
  const project = compact(lease.project, 'PROJECT');
  const worker = compact(lease.worker, 'WORKER');
  const taskId = compact(lease.taskId, 'TASK');
  if (!AW1_MODES.includes(lease.mode)) throw new AutomationWindowBlocked('INVALID_MODE');
  if (!AW1_STATES.includes(lease.state) || lease.state === 'FINISHED')
    throw new AutomationWindowBlocked('INVALID_STATE');
  if (!Number.isSafeInteger(lease.expiresAt) || lease.expiresAt <= Date.now())
    throw new AutomationWindowBlocked('STALE_LEASE');
  if (!Array.isArray(lease.allowedOrigins) || lease.allowedOrigins.length === 0 ||
      !lease.allowedOrigins.every((x) => typeof x === 'string' && normalOrigin(x) === x))
    throw new AutomationWindowBlocked('INVALID_ORIGIN_ALLOWLIST');
  return Object.freeze({
    project, worker, taskId, mode: lease.mode, state: lease.state,
    expiresAt: lease.expiresAt, allowedOrigins: Object.freeze([...lease.allowedOrigins])
  });
}
export function tagText(data) {
  return 'AUTOMATION | ' + data.project + ' | ' + data.worker + ' | ' +
    data.taskId + ' | ' + data.mode + ' | ' + data.state;
}

/** Runs ONLY in the verified owned page (and as addInitScript after reload). */
export function renderAutomationWindowTag(data) {
  const TAG_ID = 'aw1-automation-owner-tag';
  const label = 'AUTOMATION | ' + data.project + ' | ' + data.worker + ' | ' +
    data.taskId + ' | ' + data.mode + ' | ' + data.state;
  const put = () => {
    if (!document.documentElement) return;
    let host = document.getElementById(TAG_ID);
    if (!host) {
      host = document.createElement('div');
      host.id = TAG_ID;
      host.setAttribute('data-aw1-automation-only', 'true');
      host.attachShadow({ mode: 'open' });
      document.documentElement.appendChild(host);
    }
    const root = host.shadowRoot;
    if (!root) return;
    if (!root.getElementById('aw1-label')) {
      const style = document.createElement('style');
      style.textContent = ':host{all:initial!important;position:fixed!important;top:8px!important;left:8px!important;right:8px!important;z-index:2147483647!important;pointer-events:none!important;visibility:visible!important;display:block!important;} #aw1-label{box-sizing:border-box;display:inline-block;max-width:100%;padding:7px 10px;border:2px solid white;border-radius:6px;background:#101828;color:#fff;font:700 12px/1.4 system-ui,sans-serif;word-break:break-word;box-shadow:0 2px 9px #0006;} @media(max-width:390px){#aw1-label{font-size:11px;padding:5px 8px}}';
      const span = document.createElement('span');
      span.id = 'aw1-label';
      span.setAttribute('role', 'status');
      span.setAttribute('aria-label', 'Automated window identity');
      root.append(style, span);
    }
    root.getElementById('aw1-label').textContent = label;
    host.dataset.aw1Task = data.taskId;
    host.dataset.aw1Mode = data.mode;
    host.dataset.aw1State = data.state;
  };
  put();
  if (!document.documentElement) document.addEventListener('DOMContentLoaded', put, { once: true });
  // Same-document SPA changes cannot silently hide ownership.
  if (!window.__aw1TagObserverStarted && document.documentElement) {
    window.__aw1TagObserverStarted = true;
    const observer = new MutationObserver(() => {
      if (!document.getElementById(TAG_ID)) put();
    });
    observer.observe(document.documentElement, { childList: true });
  }
  return { text: label, installed: Boolean(document.getElementById(TAG_ID)) };
}
export function inspectAutomationWindowTag(expected) {
  const host = document.getElementById('aw1-automation-owner-tag');
  const child = host?.shadowRoot?.getElementById('aw1-label');
  if (!host || !child || child.textContent !== expected || host.dataset.aw1Task !==
      expected.split(' | ')[3]) return { visible: false, text: child?.textContent || null };
  const rect = child.getBoundingClientRect();
  const style = getComputedStyle(host);
  const styleChild = getComputedStyle(child);
  return {
    visible: rect.width > 0 && rect.height > 0 &&
      style.display !== 'none' && style.visibility !== 'hidden' &&
      styleChild.display !== 'none' && styleChild.visibility !== 'hidden',
    text: child.textContent
  };
}

/** Create owned windows only. A manually supplied page has no enrollment path. */
export function createVisibleWindowGuard(browserContext) {
  if (!browserContext || typeof browserContext.newPage !== 'function')
    throw new AutomationWindowBlocked('NO_DISPOSABLE_WINDOW_FACTORY');
  const owned = new WeakMap();
  const writers = new Set();

  async function inspect(page, lease) {
    const record = owned.get(page);
    if (!record || record.lease.taskId !== lease?.taskId ||
        record.lease.worker !== lease?.worker || record.lease.project !== lease?.project ||
        record.lease.mode !== lease?.mode || record.lease.state !== lease?.state ||
        record.lease.expiresAt !== lease?.expiresAt)
      throw new AutomationWindowBlocked('UNOWNED_OR_MISMATCHED_WINDOW');
    if (record.finished || lease.expiresAt <= Date.now() || record.lease.expiresAt <= Date.now())
      throw new AutomationWindowBlocked('STALE_OR_FINISHED_LEASE');
    if (typeof page.isClosed === 'function' && page.isClosed())
      throw new AutomationWindowBlocked('WINDOW_CLOSED');
    const visible = await page.evaluate(inspectAutomationWindowTag, tagText(record.lease));
    if (visible?.visible !== true || visible.text !== tagText(record.lease))
      throw new AutomationWindowBlocked('TAG_NOT_VISIBLE');
    return true;
  }

  async function open(leaseSpec, url) {
    const lease = validateLease(leaseSpec);
    if (!lease.allowedOrigins.includes(normalOrigin(url)))
      throw new AutomationWindowBlocked('DESTINATION_NOT_ALLOWED');
    const page = await browserContext.newPage();
    const record = { lease, finished: false };
    owned.set(page, record);
    try {
      const tag = { ...lease };
      await page.addInitScript({ content: '(' + renderAutomationWindowTag.toString() +
        ')(' + JSON.stringify(tag) + ');' });
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.evaluate(renderAutomationWindowTag, tag);
      await inspect(page, lease);
      return page;
    } catch (error) {
      record.finished = true;
      if (typeof page.close === 'function') await page.close().catch(() => {});
      throw error;
    }
  }

  async function run(page, lease, action, fn) {
    if (typeof fn !== 'function') throw new AutomationWindowBlocked('MISSING_ACTION');
    // Authenticate exact owned page and lease BEFORE evaluating the proposed action.
    await inspect(page, lease);
    if (DENIED_ACTIONS.has(action)) throw new AutomationWindowBlocked('ACTION_FORBIDDEN');
    if (owned.get(page)?.lease.mode === 'READ-ONLY' && MUTATING_ACTIONS.has(action))
      throw new AutomationWindowBlocked('READ_ONLY_ACTION');
    if (writers.has(page)) throw new AutomationWindowBlocked('SINGLE_WRITER_CONFLICT');
    writers.add(page);
    try {
      const result = await fn(page);
      // A command may have executed before postcondition failed; caller MUST NOT blindly retry.
      try { await inspect(page, lease); }
      catch (e) { throw new AutomationWindowBlocked('AMBIGUOUS_ACTION_CHECK_RECEIPT'); }
      return result;
    } finally {
      writers.delete(page);
    }
  }

  async function navigate(page, lease, url) {
    const record = owned.get(page);
    if (!record || !record.lease.allowedOrigins.includes(normalOrigin(url)))
      throw new AutomationWindowBlocked('DESTINATION_NOT_ALLOWED');
    await inspect(page, lease);
    if (writers.has(page)) throw new AutomationWindowBlocked('SINGLE_WRITER_CONFLICT');
    writers.add(page);
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      // addInitScript restores tag before the next action. Do not auto-mutate an unknown tab.
      await inspect(page, lease);
    } finally { writers.delete(page); }
  }

  async function finish(page, lease) {
    await inspect(page, lease);
    const record = owned.get(page);
    record.finished = true;
    await page.evaluate(renderAutomationWindowTag, { ...record.lease, state: 'FINISHED' });
    return { taskId: record.lease.taskId, status: 'FINISHED' };
  }

  return Object.freeze({ open, run, navigate, finish, inspect });
}
