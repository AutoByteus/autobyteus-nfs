// Actual published binary/Run, sandbox denies sudo/open execution; no root or protocol double.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const { chromium } = require(process.env.NFS_SMOKE_PLAYWRIGHT);
(async () => {
  const input = JSON.parse(fs.readFileSync(process.env.NFS_SMOKE_PRIVATE_INPUT, 'utf8'));
  fs.unlinkSync(process.env.NFS_SMOKE_PRIVATE_INPUT);
  const browser = await chromium.launch({headless:true, chromiumSandbox:true});
  const processRows = execFileSync('ps',['-axo','pid=,command='],{encoding:'utf8'}).split('\n').filter(line=>line.includes(process.env.PLAYWRIGHT_BROWSERS_PATH) && line.includes('--remote-debugging-pipe'));
  assert.ok(processRows.length>0,'Owned browser process must be observed');
  assert.ok(processRows.every(line=>!line.includes('--no-sandbox')),'Sandbox must remain enabled');
  const context = await browser.newContext({viewport:{width:1280,height:900}});
  const page = await context.newPage();
  const errors=[], requests=[];
  page.on('pageerror', e=>errors.push(String(e).replace(/#[A-Za-z0-9_-]+/g,'#[redacted]')));
  page.on('request', r=>{const u=new URL(r.url()); requests.push({method:r.method(),path:u.pathname});});
  const result={role:input.role,version:'v0.2.1',browser:browser.version(),observedSandbox:true,browserProcesses:processRows,widths:[],limits:'Actual published executable/embedded HTTP/UI. OS opener and sudo exec denied by enclosing sandbox. Explicit authorize request exercises only failed local helper startup; no sudo process, approval or storage work. This is public distribution launch, not setup/storage/field qualification.'};
  try {
    await page.goto(input.url,{waitUntil:'domcontentloaded'});
    await page.locator('#title').filter({hasText:input.role==='server'?'Set up shared storage':'Connect this computer'}).waitFor();
    await page.locator('#authorization').waitFor({state:'visible'});
    assert.equal(new URL(page.url()).hash,'');
    assert.ok((await page.locator('#notice').innerText()).startsWith('Not authorized.'));
    assert.equal(await page.locator('#authorize').isEnabled(),true);
    assert.equal(await page.locator('#setup').isVisible(),false);
    assert.equal(await page.locator('#configuration').isVisible(),false);
    const state=await page.evaluate(async()=>{
      const token=sessionStorage.getItem('autobyteus-nfs-dashboard');
      return await (await fetch('/api/state',{headers:{Authorization:'Bearer '+token}})).json();
    });
    assert.equal(state.role,input.role);assert.equal(state.authorized,false);assert.equal(Object.hasOwn(state,'operation'),false);assert.equal(state.home,input.home);
    result.state={role:state.role,authorized:state.authorized,operation:null,operationPropertyAbsent:true,ownedHome:true};
    // The PTY parent MUST install a sandbox denying /usr/bin/sudo before this request.
    await page.locator('#authorize').click();
    let failed;
    for (let attempt=0;attempt<80;attempt++) {
      failed=await page.evaluate(async()=>await (await fetch('/api/state',{headers:{Authorization:'Bearer '+sessionStorage.getItem('autobyteus-nfs-dashboard')}})).json());
      if (failed.operation?.state==='incomplete') break;
      await page.waitForTimeout(100);
    }
    assert.equal(failed.authorized,false);
    assert.equal(failed.operation?.kind,'authorize');assert.equal(failed.operation?.state,'incomplete');
    result.controlledFailure={authorized:false,kind:failed.operation.kind,state:failed.operation.state,helperBoundary:'Sandbox denied local process-exec; not OS consent denial'};
    for (const width of [1280,390]) {
      await page.setViewportSize({width,height:900});
      const metrics=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:innerWidth}));
      assert.ok(metrics.scroll<=metrics.viewport);
      const file=path.join(process.env.NFS_SMOKE_EVIDENCE,`public-${input.role}-${width}.png`);
      await page.screenshot({path:file,fullPage:true});result.widths.push({width,metrics,screenshot:path.basename(file)});
    }
    assert.equal(requests.filter(r=>r.path==='/api/operations' && r.method==='POST').length,1);
    await page.getByRole('button',{name:'Stop dashboard',exact:true}).click();
    await page.locator('#notice').filter({hasText:'Dashboard stopped.'}).waitFor();
    assert.equal(await page.evaluate(()=>sessionStorage.getItem('autobyteus-nfs-dashboard')),null);
    assert.equal(errors.length,0);
    result.result='Pass';result.sandboxDeniedAdminExecution=true;result.stopAndTokenRemoval=true;result.requests=requests;result.errors=errors;
  } finally {await context.close();await browser.close();}
  fs.writeFileSync(path.join(process.env.NFS_SMOKE_EVIDENCE,`public-${input.role}-browser.json`),JSON.stringify(result,null,2)+'\n');
})().catch(e=>{console.error(String(e).replace(/#[A-Za-z0-9_-]+/g,'#[redacted]'));process.exitCode=1;});
