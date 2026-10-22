/**
 * AW-1 disposable native-Chromium visual QA.
 * Only creates local file:// fixtures and isolated headless profiles.
 * Never attaches to owner tabs, CDP sessions, TradingView or remote websites.
 * Invocation: node tests/aw1_native_visual_qa.mjs
 */
import { mkdirSync, writeFileSync, readFileSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import { renderAutomationWindowTag, inspectAutomationWindowTag } from '../brain/automation/visible_window_tag.mjs';

const root = path.join(tmpdir(), 'aw1-native-visual-disposable-20261022');
mkdirSync(root, { recursive: true, mode: 0o700 });
const browser = process.env.AW1_CHROME_BINARY || '/opt/google/chrome/google-chrome';
const widths = [390, 1440];
const tag = {
  project: 'PINE-QA', worker: 'DELL', taskId: 'AW1-TEST-ONLY',
  mode: 'READ-ONLY', state: 'RUNNING'
};
const scriptCheck = "function check(){render(tag);const expected='AUTOMATION | '+tag.project+' | '+tag.worker+' | '+tag.taskId+' | '+tag.mode+' | '+tag.state;const status=inspect(expected);document.documentElement.setAttribute('data-aw1-visible',String(status.visible));document.documentElement.setAttribute('data-aw1-exact-tag',String(status.text===expected));}";
const html = [
  '<!doctype html><html><head><meta charset="utf-8"><title>AW-1 isolated test</title></head>',
  '<body style="margin:0;background:#ecf2fa;color:#17202a;font:19px/1.6 system-ui;padding:75px 20px">',
  '<main><h1>Disposable AW-1 tag test</h1><p>This browser profile belongs to a test only.</p></main>',
  '<script>',
  'const tag=', JSON.stringify(tag), ';',
  'const render=', renderAutomationWindowTag.toString(), ';',
  'const inspect=', inspectAutomationWindowTag.toString(), ';',
  scriptCheck,
  'document.readyState==="loading"?document.addEventListener("DOMContentLoaded",check,{once:true}):check();',
  '</script></body></html>'
].join('');
const file = path.join(root, 'aw1-disposable.html');
writeFileSync(file, html, { mode: 0o600 });
const uri = pathToFileURL(file).href;
const rows = [];
for (const width of widths) {
  const common = [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-extensions',
    '--disable-background-networking', '--no-first-run', '--disable-dev-shm-usage',
    '--window-size=' + width + ',850', '--virtual-time-budget=1500'
  ];
  const base = path.join(root, 'browser-' + width);
  const dom = spawnSync(browser, [...common, '--user-data-dir=' + base + '-dom',
    '--dump-dom', uri], { encoding: 'utf8', timeout: 15000, maxBuffer: 1000000 });
  const screenshot = path.join(root, 'aw1-tag-' + width + '.png');
  const snap = spawnSync(browser, [...common, '--user-data-dir=' + base + '-snap',
    '--screenshot=' + screenshot, uri], { encoding: 'utf8', timeout: 15000, maxBuffer: 1000000 });
  const text = String(dom.stdout || '');
  const visible = text.includes('data-aw1-visible="true"');
  const correct = text.includes('data-aw1-exact-tag="true"');
  let bytes = 0, screenshotWidth = 0, screenshotHeight = 0;
  try {
    bytes = statSync(screenshot).size;
    const header = readFileSync(screenshot).subarray(0, 24);
    if (header.toString('hex', 0, 8) === '89504e470d0a1a0a') {
      screenshotWidth = header.readUInt32BE(16);
      screenshotHeight = header.readUInt32BE(20);
    }
  } catch {}
  const row = {
    width, visible, correct, screenshotWidth, screenshotHeight, screenshotBytes: bytes,
    domExit: dom.status, screenshotExit: snap.status,
    screenshotPath: screenshot, accepted: visible && correct && bytes > 2000 &&
      screenshotWidth >= width && screenshotHeight >= 400
  };
  rows.push(row);
}
console.log(JSON.stringify({ test: 'AW1_NATIVE_DISPOSABLE_VISUAL', rows, passed: rows.every(x => x.accepted) }, null, 2));
if (rows.some(x => !x.accepted)) process.exitCode = 1;
