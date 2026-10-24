// Run only against the build-tagged owned Go preview. No sudo, NFS or installer.
const { createRequire } = require('node:module');
const { spawn } = require('node:child_process');
const { mkdtemp, readFile, rm, access, mkdir } = require('node:fs/promises');
const { join } = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');
const playwright = createRequire(process.env.NFS_PLAYWRIGHT_MODULE)(process.env.NFS_PLAYWRIGHT_MODULE);
const root = process.env.NFS_PREVIEW_SCRATCH, binary = process.env.NFS_PREVIEW_BINARY, output = process.env.NFS_PREVIEW_EVIDENCE;
if (!root || !binary || !output) throw new Error('Explicit owned scratch, preview binary and evidence directory required');
const results = [], versions = {};
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
async function eventually(fn, timeout = 10000) { const until = Date.now() + timeout; let last; do { try { return await fn(); } catch (e) { last = e; await sleep(50); } } while (Date.now() < until); throw last; }
async function shown(page, id) { await page.locator('#' + id).waitFor({ state: 'visible', timeout: 10000 }); }
async function hidden(page, id) { await page.locator('#' + id).waitFor({ state: 'hidden', timeout: 10000 }); }
async function includes(page, id, expected) { await eventually(async () => assert.ok((await page.locator('#' + id).textContent()).includes(expected), `${id}: missing ${expected}`)); }
async function controls(page, role) {
 if (role === 'server') {
   await page.locator('#source').fill('/Shared/projects'); await page.locator('#endpoint').fill('192.168.1.20'); await page.locator('#allowlist').fill('192.168.1.21');
 } else await page.locator('#connection-input').fill('{"storageId":"c87ff813-c2ce-4bd5-9208-7f6e3b7d7cf7","endpoint":"192.168.1.20","export":"/Shared","protocol":"3","mountRoot":"/Volumes/autobyteus-shared"}');
}
async function run(browser, engine, role, width, scenario) {
 const dir = await mkdtemp(join(root, 'view-'));
 const file = join(dir, 'session.json');
 const child = spawn(binary, ['-test.run=^TestBrowserFixture$', '-test.timeout=180s'], { env: { ...process.env, NFS_PREVIEW_OUTPUT: file, NFS_PREVIEW_ROLE: role, NFS_PREVIEW_SCENARIO: scenario }, stdio: ['ignore', 'pipe', 'pipe'] });
 let diagnostic = ''; child.stderr.on('data', b => diagnostic += b); child.stdout.on('data', b => diagnostic += b);
 const exited = new Promise(resolve => child.on('exit', (code, signal) => resolve({ code, signal })));
 const context = await browser.newContext({ viewport: { width, height: 1000 } });
 const page = await context.newPage(), errors = [];
 page.on('pageerror', error => errors.push(error.message));
 // Browser clipboard boundary double; never alter the operator's OS clipboard.
 await page.addInitScript(() => { window.copied = ''; Object.defineProperty(navigator, 'clipboard', { value: { writeText: async text => { if (window.denyCopy) throw new Error('fixture denial'); window.copied = text; } } }); });
 let session;
 try {
   session = await eventually(async () => JSON.parse(await readFile(file, 'utf8')));
   await page.goto(pathToFileURL(session.bootstrap).href);
   await shown(page, 'authorization');
   assert.equal(new URL(page.url()).hash, '');
   await eventually(async () => { try { await access(session.bootstrap); assert.fail('bootstrap not removed'); } catch (e) { if (e.code !== 'ENOENT') throw e; } });
   // Actual page uses its tab-scoped token on reload; no automatic privilege.
   await page.reload(); await shown(page, 'authorization');
   await page.locator('#authorize').focus(); await page.keyboard.press('Enter');
   await shown(page, 'configuration');
   if (scenario === 'wrong-role') {
     await shown(page, 'wrong-role'); await hidden(page, 'setup'); await hidden(page, 'detach'); await hidden(page, 'reconnect'); await hidden(page, 'check');
   } else if (scenario === 'pending') {
     await includes(page, 'configuration-title', 'incomplete'); await hidden(page, 'setup');
     await page.locator('#reconnect').click(); await shown(page, 'review'); await includes(page, 'review-title', 'saved');
     await page.locator('#cancel').click(); await hidden(page, 'review');
   } else {
     await shown(page, 'setup');
     if (role === 'server' && scenario === 'normal') {
       await page.locator('#browse').click(); await shown(page, 'chooser');
       await eventually(async () => assert.equal(await page.locator('#choose-directory').isEnabled(), true));
       const names = await page.locator('#directory-list').innerText(); assert.ok(names.includes('visible-folder')); assert.ok(!names.includes('private-file'));
       await page.locator('#directory-list button').filter({ hasText: 'visible-folder' }).click();
       await eventually(async () => assert.equal(await page.locator('#choose-directory').isEnabled(), true));
       await page.locator('#choose-directory').click(); assert.ok((await page.locator('#source').inputValue()).endsWith('/visible-folder')); await hidden(page, 'chooser');
     }
     await controls(page, role); await page.locator('#setup-form button[type=submit]').click();
     if (scenario === 'error') {
       await shown(page, 'error'); await includes(page, 'notice', 'Operation incomplete'); assert.equal(await page.locator('#error img').count(), 0); await includes(page, 'error', '<img');
       assert.equal(await page.evaluate(() => document.activeElement.id), 'error');
     } else {
       await shown(page, 'review'); assert.equal(await page.locator('#commit').isEnabled(), false);
       await includes(page, 'review-connection', 'c87ff813-c2ce-4bd5-9208-7f6e3b7d7cf7');
       await includes(page, 'review-connection', '"protocol"');
       if (scenario === 'expired') {
         await includes(page, 'review-deadline', 'Expired'); assert.equal(await page.locator('#consent').isEnabled(), false);
       } else {
         await page.reload(); await shown(page, 'review'); assert.equal(await page.locator('#commit').isEnabled(), false);
         await page.locator('#consent').check(); await page.locator('#commit').click();
         if (scenario === 'slow' || scenario === 'stop-running') {
           await includes(page, 'notice', 'Applying');
           // Polling must stay responsive without starting another operation.
           const state = await page.evaluate(async () => { const token=sessionStorage.getItem('autobyteus-nfs-dashboard'); return (await fetch('/api/state',{headers:{Authorization:'Bearer '+token}})).json(); });
           assert.equal(state.operation.state, 'running');
         }
         if (scenario === 'stop-running') {
           await page.locator('#stop').click(); await includes(page, 'notice', 'Storage is NOT disconnected');
           const immediate = await Promise.race([exited, sleep(100).then(() => 'still-draining')]);
           assert.equal(immediate, 'still-draining');
           const ended = await Promise.race([exited, sleep(6000).then(() => ({timeout:true}))]); assert.equal(ended.code,0,diagnostic);
           assert.equal(await page.evaluate(() => sessionStorage.getItem('autobyteus-nfs-dashboard')), null);
           results.push({engine,role,width,scenario,result:'Pass',scope:'stopping drains the doubled 3-second root operation'});
           return;
         }
         await shown(page, 'connection-panel'); await hidden(page, 'review'); await includes(page, 'notice', 'Ready at');
         await page.locator('#copy').click(); await includes(page, 'copy-result', 'copied');
         assert.equal(await page.evaluate(() => window.copied), await page.locator('#connection-output').inputValue());
         await page.evaluate(() => { window.denyCopy = true; }); await page.locator('#copy').click(); await includes(page, 'copy-result', 'manually');
         assert.equal(await page.evaluate(() => document.activeElement.id), 'connection-output');
         await page.locator('#check').click(); await includes(page, 'checked-at', 'Ready at');
         await page.locator('#detach').click(); await shown(page, 'review'); await shown(page, 'drain-label');
         await page.locator('#consent').check(); assert.equal(await page.locator('#commit').isEnabled(), false);
         await page.locator('#drained').check(); await page.locator('#commit').click();
         await shown(page, 'setup'); await hidden(page, 'observed'); await includes(page, 'notice', 'Not configured');
       }
     }
   }
   assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'horizontal overflow');
   assert.deepEqual(errors, []);
   await page.screenshot({ path: join(output, `${engine}-${role}-${width}-${scenario}.png`), fullPage: true });
   const calls = (await readFile(file+'.calls','utf8')).trim().split('\n').map(line => JSON.parse(line));
   assert.equal(calls.filter(c => c.kind === 'inspect').length, 1, 'reload repeated authorization/inspection');
   assert.ok(calls.filter(c => c.kind === 'commit').length <= 2, 'replayed commit');
   await page.locator('#stop').click(); await includes(page, 'notice', 'Storage is NOT disconnected');
   assert.equal(await page.evaluate(() => sessionStorage.getItem('autobyteus-nfs-dashboard')), null);
   const ended = await Promise.race([exited, sleep(5000).then(() => ({ timeout: true }))]); assert.equal(ended.code, 0, diagnostic);
   results.push({ engine, role, width, scenario, result: 'Pass', calls: calls.map(c => c.kind) });
 } catch (e) {
   await page.screenshot({ path: join(output, `${engine}-${role}-${width}-${scenario}-failure.png`), fullPage: true }).catch(() => {});
   results.push({ engine, role, width, scenario, result: 'Fail', error: e.message, diagnostic }); throw e;
 } finally {
   // Only our rootless test fixture, not the product or any storage child.
   await page.locator('#stop').click({timeout:500}).catch(() => {});
   if (child.exitCode === null) { child.kill('SIGTERM'); await exited; }
   await context.close(); await rm(dir, { recursive: true, force: true });
 }
}
(async () => {
 await mkdir(output, { recursive: true });
 try {
   for (const engine of ['chromium', 'webkit']) {
     const browser = await playwright[engine].launch(); versions[engine] = browser.version();
     try {
       const selected = (process.env.NFS_PREVIEW_SCENARIOS || 'normal,pending,wrong-role,error,expired,slow,stop-running').split(',');
       if (selected.includes('normal')) for (const role of ['server', 'client']) for (const width of [1280, 390]) await run(browser, engine, role, width, 'normal');
       for (const scenario of ['pending', 'wrong-role', 'error', 'expired', 'slow', 'stop-running'].filter(s => selected.includes(s))) await run(browser, engine, 'client', 390, scenario);
     } finally { await browser.close(); }
   }
 } finally {
   await require('node:fs/promises').writeFile(join(output,'result.json'), JSON.stringify({ versions, results, boundary:'real embedded browser/HTTP, subprocess root-protocol double; no native NFS proof', cleanup:'owned contexts/preview processes/directory fixtures closed and removed' },null,2)+'\n');
 }
})().catch(e => { console.error(e.stack); process.exitCode=1; });
