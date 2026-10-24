// API07 round2 | 2026-10-24 | current34afb80/7b0577a4 | Mac Chrome sandbox; actual embedded HTTP/directory reader.
// No response interception or clock shortening. Root-protocol double only; no storage/clipboard/privilege action.
const fs=require('node:fs/promises'), path=require('node:path'), cp=require('node:child_process'), assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const E=path.resolve('tickets/in-progress/nfs-setup-dashboard/evidence');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(fn,ms=15000){let end=Date.now()+ms,last;do{try{return await fn()}catch(e){last=e;await sleep(50)}}while(Date.now()<end);throw last}
(async()=>{
 const preparation=JSON.parse(await fs.readFile(E+'/API-07-02-environment.json','utf8')),S=preparation.scratch;
 const {chromium}=require(S+'/browser-tools/node_modules/playwright');
 const result={case:'API-07',round:'API-REV-002',date:new Date().toISOString(),commit:cp.execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),command:process.argv,environment:{platform:process.platform,arch:process.arch,source:preparation.sourceTests,previewSHA256:preparation.binarySHA256,rootBoundary:'subprocess root-protocol double, inspect only; real ordinary-user directory IO',browser:'new private sandboxed Chrome profile',clipboard:'unused',timing:'actual responses; no route/response/clock double'},runs:[]};
 let browser;
 try{
  browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,chromiumSandbox:true,env:{...process.env,HOME:S+'/home',TMPDIR:S+'/tmp'}});
  result.environment.browserVersion=browser.version();
  const processes=cp.execFileSync('ps',['-axo','pid=,command='],{encoding:'utf8'}).split('\n').filter(x=>x.includes('Google Chrome')&&x.includes(S+'/tmp')&&x.includes('--user-data-dir='));
  assert.ok(processes.length);assert.ok(processes.every(x=>!x.includes('--no-sandbox')));result.environment.sandboxProcessEvidence=processes;
  for(const width of [1280,390]){
   const dir=await fs.mkdtemp(S+'/natural-'),file=dir+'/session.json',responses=[],errors=[];
   const run={width,steps:[],responses};result.runs.push(run);
   const record=(name,data={})=>{run.steps.push({name,result:'Pass',...data});console.log(width,name)};
   const child=cp.spawn(S+'/dashboard-preview',['-test.run=^TestBrowserFixture$','-test.timeout=120s'],{env:{...process.env,NFS_PREVIEW_OUTPUT:file,NFS_PREVIEW_ROLE:'server',NFS_PREVIEW_SCENARIO:'normal'},stdio:['ignore','pipe','pipe']});
   let diagnostic='';child.stdout.on('data',b=>diagnostic+=b);child.stderr.on('data',b=>diagnostic+=b);const exited=new Promise(resolve=>child.once('exit',(code,signal)=>resolve({code,signal})));
   const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
   try{
    const session=await until(async()=>JSON.parse(await fs.readFile(file,'utf8')));
    await page.goto(pathToFileURL(session.bootstrap).href);await page.locator('#authorization').waitFor();assert.equal(new URL(page.url()).hash,'');
    await page.locator('#authorize').focus();await page.keyboard.press('Enter');await page.locator('#setup').waitFor();
    page.on('response',async r=>{if(new URL(r.url()).pathname==='/api/directories'){const at=Date.now();try{responses.push({at,method:r.request().method(),status:r.status(),body:await r.json()})}catch(e){responses.push({at,error:e.message})}}});
    await page.locator('#browse').click();await page.locator('#chooser').waitFor();
    const input=page.locator('#directory-path'),choose=page.locator('#choose-directory');
    const expected=dir+'/visible-folder';await input.focus();await page.keyboard.press('Meta+A');
    const began=Date.now();await page.keyboard.type(expected,{delay:80});const finished=Date.now();
    await until(()=>assert.ok(responses.some(r=>r.method==='GET'&&r.body?.state==='complete')));
    assert.ok(responses.some(r=>r.method==='GET'&&r.body?.state==='complete'&&r.at>=began&&r.at<=finished),'real listing must complete while actual keys are being typed');
    const actual=await input.inputValue();run.typing={expected,actual,began,finished,nativeKeyboardDelayMs:80};assert.equal(actual,expected);
    assert.equal(await page.evaluate(()=>document.activeElement.id),'directory-path');assert.equal(await choose.isEnabled(),false);
    record('original-natural-keyboard-edit-preserved',{expected,actual});
    await page.screenshot({path:E+`/API-07-02-${width}-typing.png`,fullPage:true});
    await fs.writeFile(E+`/API-07-02-${width}-typing.txt`,`API07 round2; ${result.date}; ${result.commit}; Mac Chrome${result.environment.browserVersion}; actual DOM\n`+await page.locator('body').innerText());
    await input.focus();await page.keyboard.press('Meta+A');await page.keyboard.type(expected,{delay:80});assert.equal(await input.inputValue(),expected);record('same-settled-native-key-control');
    await page.keyboard.press('Enter');await until(async()=>assert.equal(await choose.isEnabled(),true));assert.equal(await input.inputValue(),expected);record('explicit-list-exact-draft');
    await page.locator('#directory-parent').click();await until(async()=>{assert.equal(await choose.isEnabled(),true);assert.equal(await input.inputValue(),dir)});
    const names=await page.locator('#directory-list').innerText();assert.ok(names.includes('visible-folder'));assert.ok(!names.includes('private-file'));record('parent-directory-only-navigation');
    await page.locator('#directory-list button').filter({hasText:'visible-folder'}).click();await until(async()=>{assert.equal(await choose.isEnabled(),true);assert.equal(await input.inputValue(),expected)});
    await choose.click();assert.equal(await page.locator('#source').inputValue(),expected);assert.equal(await page.evaluate(()=>document.activeElement.id),'source');record('child-selection-exact-source');
    await page.locator('#browse').click();await until(async()=>{assert.equal(await choose.isEnabled(),true);assert.equal(await input.inputValue(),expected)});record('reopen-selected-source');
    const missing=dir+'/not-created';await input.fill(missing);assert.equal(await choose.isEnabled(),false);await page.keyboard.press('Enter');await until(async()=>assert.ok((await page.locator('#directory-message').innerText()).includes('no such file')));
    assert.equal(await input.inputValue(),missing);assert.equal(await choose.isEnabled(),false);record('failed-list-preserves-correctable-draft');
    await input.fill(dir);assert.equal(await choose.isEnabled(),false);await page.keyboard.press('Enter');await until(async()=>assert.equal(await choose.isEnabled(),true));assert.equal(await input.inputValue(),dir);record('correction-requires-explicit-list');
    assert.deepEqual(errors,[]);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));record('no-browser-errors-or-overflow');
    await page.screenshot({path:E+`/API-07-02-${width}-navigation.png`,fullPage:true});
    await page.locator('#close-chooser').click();await page.locator('#stop').click();const ended=await Promise.race([exited,sleep(10000).then(()=>({timeout:true}))]);assert.equal(ended.code,0,diagnostic);
    assert.equal(await page.evaluate(()=>sessionStorage.getItem('autobyteus-nfs-dashboard')),null);
    const calls=(await fs.readFile(file+'.calls','utf8')).trim().split('\n').map(x=>JSON.parse(x).kind);assert.deepEqual(calls,['inspect']);record('stopped-no-storage-commands',{ended,calls});run.result='Pass';
   }catch(e){run.result='Fail';run.error=e.stack;await page.screenshot({path:E+`/API-07-02-${width}-failure.png`,fullPage:true}).catch(()=>{});throw e}
   finally{
    if(child.exitCode===null){try{if(await page.locator('#chooser').isVisible())await page.locator('#close-chooser').click();await page.locator('#stop').click({timeout:2000});await Promise.race([exited,sleep(3000)])}catch{}if(child.exitCode===null){child.kill('SIGTERM');await exited;run.fixtureTermination='SIGTERM owned rootless fixture after failed cleanup'}}
    run.terminal={exit:child.exitCode,signal:child.signalCode,diagnostic};await context.close();await fs.rm(dir,{recursive:true,force:true});run.directoryRemoved=true;
   }
  }
  result.result='Pass';
 }catch(e){result.result='Fail';result.error=e.stack;console.error(e.stack);process.exitCode=1}
 finally{if(browser)await browser.close();result.cleanup='own browser contexts/preview subprocesses/directory fixtures closed; toolchain/source scratch pending API06';await fs.writeFile(E+'/API-07-02-result.json',JSON.stringify(result,null,2)+'\n');console.log(result.result)}
})().catch(e=>{console.error(e.stack);process.exitCode=1});
