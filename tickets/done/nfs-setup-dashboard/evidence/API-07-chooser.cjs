// API-03/04/05; 2026-10-24; current source; host browser/SSH loopback test transport.
// No root/IPC/HTTP double. Only clipboard is doubled to preserve host clipboard.
const fs=require('node:fs'), path=require('node:path'), cp=require('node:child_process'), assert=require('node:assert/strict');
const S='/Users/normy/nfs-dashboard-api-w47yo5sg', E=path.resolve('tickets/in-progress/nfs-setup-dashboard/evidence');
const {chromium}=require(S+'/browser-tools/node_modules/playwright');
const ip=fs.readFileSync(S+'/ip','utf8').trim();
const sshargs=['-i',S+'/key','-o','IdentitiesOnly=yes','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+S+'/known_hosts','-o','ConnectTimeout=10'];
function remote(command){let r=cp.spawnSync('/usr/bin/ssh',[...sshargs,'admin@'+ip,command],{encoding:'utf8',timeout:30000});return {command,exit:r.status,stdout:r.stdout,stderr:r.stderr};}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(fn,ms=20000){let end=Date.now()+ms,last;do{try{return await fn()}catch(e){last=e;await sleep(100)}}while(Date.now()<end);throw last}
const which='probe', id='API-07';
const result={case:id,date:new Date().toISOString(),command:process.argv.join(' '),commit:cp.execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),environment:{host:'Mac Chrome isolated profile',guest:ip,transport:'SSH forwards exact guest loopback port, no LAN listener; public role actual TTY/sudo/pipes; clipboard double only'},steps:[]};
function record(name,data={}){result.steps.push({name,result:'Pass',...data});fs.writeFileSync(E+'/'+id+'-runtime.json',JSON.stringify(result,null,2)+'\n');console.log(name)}
let browser,context,page,tunnel,driver,lines=[],terminal=[], errors=[];
async function start(role){
 driver=cp.spawn('/usr/bin/ssh',[...sshargs,'admin@'+ip,'python3 /home/admin/api-dashboard/driver.py '+role]);let buffer='';
 driver.stdout.on('data',b=>{buffer+=b;let i;while((i=buffer.indexOf('\n'))>=0){const l=buffer.slice(0,i);buffer=buffer.slice(i+1);try{let v=JSON.parse(l);lines.push(v);if(v.terminal)terminal.push(v)}catch{}}});let err='';driver.stderr.on('data',b=>err+=b);
 let session=await until(()=>{assert.ok(lines[0]?.url,'no session '+err);return lines[0]});let u=new URL(session.url);
 tunnel=cp.spawn('/usr/bin/ssh',[...sshargs,'-o','ExitOnForwardFailure=yes','-N','-L',`127.0.0.1:${u.port}:127.0.0.1:${u.port}`,'admin@'+ip]);tunnel.stderr.on('data',b=>err+=b);
 await until(async()=>{let r=await fetch(u.origin);assert.equal(r.status,200)});assert.equal((await fetch(u.origin+'/api/state')).status,403);record('actual-loopback-unauthorized-refusal');
 context=await browser.newContext({viewport:{width:1280,height:1000}});page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{window.apiCopied='';Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{if(window.apiDeny)throw Error('fixture clipboard denied');window.apiCopied=t}}})});
 await page.goto(session.url);await page.locator('#authorization').waitFor();assert.equal(new URL(page.url()).hash,'');
 record('manual-private-bootstrap-consumed-no-auto-privilege',{role,uid:remote('id').stdout,listener:remote('ss -ltnp | grep :'+u.port).stdout});
 await page.reload();await page.locator('#authorize').focus();await page.keyboard.press('Enter');await page.locator('#configuration').waitFor();await waitop();
 record('native-sudo-pipes-authorized',{state:await state()});
}
async function state(){return page.evaluate(async()=>{let t=sessionStorage.getItem('autobyteus-nfs-dashboard');return(await fetch('/api/state',{headers:{Authorization:'Bearer '+t}})).json()})}
async function waitop(){return until(async()=>{let s=await state();assert.notEqual(s.operation?.state,'running');return s.operation},600000)}
async function click(id){const before=(await state()).operation?.requestId||0;await page.locator('#'+id).click();if(id==='stop')return;await until(async()=>assert.ok((await state()).operation?.requestId>before));return waitop()}
async function shown(id){await page.locator('#'+id).waitFor({state:'visible'})}
async function checktext(id,text){await until(async()=>assert.ok((await page.locator('#'+id).innerText()).includes(text),id+' missing '+text))}
async function setup(){const before=(await state()).operation?.requestId||0;await page.locator('#setup-form button[type=submit]').click();await until(async()=>assert.ok((await state()).operation?.requestId>before));return waitop()}
async function screenshot(name){await page.screenshot({path:E+'/'+id+'-'+name+'.png',fullPage:true});fs.writeFileSync(E+'/'+id+'-'+name+'.txt',`Case ${id}; ${new Date().toISOString()}; current ${result.commit}; actual DOM\n`+await page.locator('body').innerText())}
async function approve(drained=false){await shown('review');assert.equal(await page.locator('#commit').isEnabled(),false);await page.locator('#consent').check();if(drained){assert.equal(await page.locator('#commit').isEnabled(),false);await page.locator('#drained').check()}let op=await click('commit');return op}
async function stop(){await click('stop').catch(()=>{});await until(()=>assert.ok(terminal.length,'public process still draining'),25000);assert.equal(terminal.at(-1).exit,0);record('dashboard-stop-terminal-drained',{terminal:terminal.at(-1)});await context.close();context=null;tunnel.kill('SIGTERM');await until(()=>assert.ok(tunnel.exitCode!==null||tunnel.signalCode!==null));tunnel=null}
(async()=>{
 try {
  browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,chromiumSandbox:true,env:{...process.env,HOME:S+'/home',TMPDIR:S+'/tmp'}});result.environment.browser=browser.version();
  await start('server');await shown('setup');
  const responses=[];page.on('response',async r=>{if(new URL(r.url()).pathname==='/api/directories'){try{responses.push({at:Date.now(),method:r.request().method(),request:r.request().postData(),status:r.status(),body:await r.json()})}catch{}}});
  await page.locator('#browse').click();await shown('chooser');
  const expected='/home/admin/api-dashboard', began=Date.now();
  await page.locator('#directory-path').focus();await page.keyboard.press('Meta+A');await page.keyboard.type(expected,{delay:80});await sleep(1000);
  const actual=await page.locator('#directory-path').inputValue();result.typing={expected,actual,began,finished:Date.now(),nativeKeyboardDelayMs:80,responses};
  await screenshot('typing');record('actual-native-key-chooser-observation',{expected,actual});
  await page.locator('#directory-path').focus();await page.keyboard.press('Meta+A');await page.keyboard.type(expected,{delay:80});await sleep(700);
  const control=await page.locator('#directory-path').inputValue();result.settledControl={expected,actual:control};assert.equal(control,expected);
  await page.locator('#close-chooser').click();await stop();
  result.result=actual===expected?'Pass':'Fail';result.finding=actual===expected?'No native-key input loss reproduced':'Initial directory listing completion replaced an in-progress user path edit; settled control retains identical native-key input';
 }catch(e){result.result='HarnessError';result.error=e.stack;console.error(e.stack)}
 finally{if(context){try{if(await page.locator('#chooser').isVisible())await page.locator('#close-chooser').click();await page.locator('#stop').click({timeout:2000});await until(()=>assert.ok(terminal.length),20000)}catch{}await context.close()}if(tunnel)tunnel.kill('SIGTERM');if(browser)await browser.close();result.terminal=terminal;fs.writeFileSync(E+'/'+id+'-runtime.json',JSON.stringify(result,null,2)+'\n');console.log(result.result,result.finding);process.exitCode=result.result==='Pass'?0:1}
})();
