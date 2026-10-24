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
const which=process.argv[2]||'native', id=which==='native'?'API-03':which==='docker'?'API-04':'API-05';
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
 try{
 browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,chromiumSandbox:true,env:{...process.env,HOME:S+'/home',TMPDIR:S+'/tmp'}});result.environment.browser=browser.version();result.environment.browserProcesses=cp.execFileSync('/bin/ps',['-axo','pid,ppid,args'],{encoding:'utf8'}).split('\n').filter(l=>l.includes(S)&&l.includes('Google Chrome'));assert.ok(result.environment.browserProcesses.length);assert.ok(result.environment.browserProcesses.every(l=>!l.includes('--no-sandbox')));
 await start(which==='client'?'client':'server');
 if(which==='client'){
   await shown('setup');await page.locator('#connection-input').fill('{bad');let bad=await setup();assert.equal(bad.state,'incomplete');record('malformed-connection-no-effects',{operation:bad});
   const conn=JSON.parse(fs.readFileSync(S+'/connection.json'));await page.locator('#connection-input').fill(JSON.stringify(conn));let occupied=remote('sudo mkdir -p /Volumes/api-occupied; printf "occupied-original\\n" | sudo tee /Volumes/api-occupied/sentinel');assert.equal(occupied.exit,0);await page.locator('#mount-root').fill('/Volumes/api-occupied');let blocked=await setup();assert.equal(blocked.state,'incomplete');assert.equal(blocked.error.effectsMayHaveStarted,false);let kept=remote('cat /Volumes/api-occupied/sentinel');assert.ok(kept.stdout.includes('occupied-original'));record('occupied-target-refused-and-preserved',{operation:blocked,observation:kept});await page.locator('#mount-root').fill('/Volumes/api-client-override');let plan=await setup();assert.equal(plan.state,'succeeded');assert.equal(plan.data.configuration.connection.mountRoot,'/Volumes/api-client-override');
   await shown('review');await screenshot('client-review');const deadline=Date.parse(plan.data.expiresAt);record('client-exact-paste-override-review',{review:plan.data});
   let busy=remote('sudo -- /usr/libexec/autobyteus-nfs/autobyteus-nfs status');result.cliBusyObservation=busy;assert.notEqual(busy.exit,0);assert.ok(busy.stderr.includes('another administrative operation is checking/incomplete'));record('independent-CLI-busy-during-review',{observation:busy});
   await page.reload();await shown('review');assert.equal(await page.locator('#consent').isChecked(),false);record('reload-preserves-review-not-consent');
   console.log('waiting for actual five-minute lease expiry');await sleep(Math.max(0,deadline-Date.now()+1600));await checktext('review-deadline','Expired');assert.equal(await page.locator('#commit').isEnabled(),false);let free=remote('sudo -- /usr/libexec/autobyteus-nfs/autobyteus-nfs status');assert.ok(!free.stderr.includes('another administrative operation is checking/incomplete'));record('actual-review-expiry-no-cli-lock',{observation:free,elapsedMs:Date.now()-Date.parse(plan.startedAt)});
   await click('cancel');await page.locator('#review').waitFor({state:'hidden'});record('expired-review-cleared');
 }else{
   let prep=remote('mkdir -p /home/admin/api-dashboard/data; printf "api-original-sentinel\\n" > /home/admin/api-dashboard/data/original.txt');assert.equal(prep.exit,0);
   await shown('setup');
   await page.locator('#browse').click();await shown('chooser');await until(async()=>assert.ok(await page.locator('#choose-directory').isEnabled()));await page.locator('#directory-path').fill('/home/admin/api-dashboard');await page.locator('#directory-form button[type=submit]').click();await until(async()=>assert.ok((await page.locator('#directory-list').innerText()).includes('data')));assert.ok(!(await page.locator('#directory-list').innerText()).includes('driver.py'));await page.locator('#directory-list button').filter({hasText:/^data$/}).click();await until(async()=>assert.ok(await page.locator('#choose-directory').isEnabled()));await page.locator('#choose-directory').click();assert.equal(await page.locator('#source').inputValue(),'/home/admin/api-dashboard/data');record('ordinary-user-directory-only-chooser');
   await page.locator('#source').fill('/home/admin/api-dashboard/data');await page.locator('#endpoint').fill(ip);await page.locator('#allowlist').fill(ip+'/32');await page.locator('#mount-root').fill('/Volumes/api-'+which);await page.locator('#backend').selectOption(which==='native'?'ganesha-native':'ganesha-docker');
   if(which==='native'){await page.locator('#source').fill('/');let rejected=await setup();assert.equal(rejected.state,'incomplete');assert.equal(rejected.error.effectsMayHaveStarted,false);await checktext('notice','Operation incomplete');await shown('error');assert.equal(await page.evaluate(()=>document.activeElement.id),'error');record('real-invalid-source-error-before-effects',{operation:rejected});await screenshot('source-error');await page.locator('#source').fill('/home/admin/api-dashboard/data')}
   let plan=await setup();assert.equal(plan.state,'succeeded',JSON.stringify(plan));await shown('review');assert.equal(await page.locator('#commit').isEnabled(),false);
   await screenshot('review');record('exact-native-plan-before-consent',{review:plan.data});
   await click('cancel');await page.locator('#review').waitFor({state:'hidden'});let absent=remote('test ! -f /var/lib/autobyteus-nfs/attachment.json; findmnt -rn /Volumes/api-'+which);assert.equal(absent.stdout,'');record('cancel-no-mount');
   plan=await setup();await shown('review');await page.reload();await shown('review');assert.equal(await page.locator('#consent').isChecked(),false);
   let op;
   if(which==='docker'){
    let down=remote('sudo systemctl stop docker.service docker.socket');assert.equal(down.exit,0);record('owned-daemon-unavailable-after-review',{observation:down});
    op=await approve();assert.equal(op.state,'incomplete');assert.equal(op.data.configuration.state,'pending');record('actual-failed-apply-retains-pending',{operation:op});await checktext('notice','Operation incomplete');await screenshot('pending-error');
    let up=remote('sudo systemctl start docker.service');assert.equal(up.exit,0);await click('inspect');await checktext('configuration-title','incomplete');await page.locator('#setup').waitFor({state:'hidden'});
    let resume=await click('reconnect');assert.equal(resume.state,'succeeded');assert.equal(resume.data.kind,'resume');assert.equal(resume.data.configuration.connection.storageId,plan.data.configuration.connection.storageId);record('saved-pending-fresh-review-same-identity',{review:resume.data});op=await approve();
   }else op=await approve();record('apply-returned',{operation:op});assert.equal(op.state,'succeeded',JSON.stringify(op));await checktext('notice','Ready at');
   let conn=op.data.configuration.connection;fs.writeFileSync(S+'/connection.json',JSON.stringify(conn));
   let rw=remote(`python3 - <<'PY'\nfrom pathlib import Path\nimport os,json,hashlib\np=Path('${conn.mountRoot}'); assert (p/'original.txt').read_text()=='api-original-sentinel\\n'\nwith (p/'browser-write.txt').open('w') as f:f.write('native-browser-'+ '${which}'+'\\n');f.flush();os.fsync(f.fileno())\nassert Path('/home/admin/api-dashboard/data/browser-write.txt').read_text()=='native-browser-${which}\\n'\nprint(json.dumps({'uid':os.getuid(),'mount':str(p),'sourceAndMountedExact':True,'sha256':hashlib.sha256((p/'browser-write.txt').read_bytes()).hexdigest()}))\nPY`);assert.equal(rw.exit,0,JSON.stringify(rw));record('browser-to-actual-nonroot-mounted-bytes',{observation:rw});
   await page.locator('#copy').click();assert.equal(await page.evaluate(()=>window.apiCopied),await page.locator('#connection-output').inputValue());await page.evaluate(()=>window.apiDeny=true);await page.locator('#copy').click();await checktext('copy-result','manually');record('connection-copy-and-denial',{boundary:'clipboard doubled; exact rendered JSON'});
   await click('inspect');await checktext('notice','Configured');assert.equal(await page.locator('#observed').isVisible(),false);record('inspect-not-fake-ready');let ready=await click('check');assert.equal(ready.state,'succeeded');record('explicit-readiness',{operation:ready});
   let re=await click('reconnect');assert.equal(re.state,'succeeded');let done=await approve();assert.equal(done.state,'succeeded');record('reviewed-reconnect',{operation:done});
   await page.setViewportSize({width:390,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await screenshot('ready-390');record('actual-native-narrow-surface',{errors});
   await stop();let remains=remote('cat /Volumes/api-'+which+'/browser-write.txt');assert.equal(remains.exit,0);record('stop-keeps-storage',{observation:remains});
   lines=[];terminal=[];await start('client');await shown('wrong-role');await checktext('wrong-role','autobyteus-nfs server');assert.equal(await page.locator('#setup').isVisible(),false);assert.equal(await page.locator('#detach').isVisible(),false);record('actual-wrong-role-ui-blocks-mutation');await stop();
   lines=[];terminal=[];await start('server');await checktext('notice','Configured');await page.locator('#setup').waitFor({state:'hidden'});record('restart-direct-saved-state-no-migration');
   let d=await click('detach');assert.equal(d.state,'succeeded');await screenshot('detach-review');let detached=await approve(true);assert.equal(detached.state,'succeeded',JSON.stringify(detached));await shown('setup');await page.locator('#observed').waitFor({state:'hidden'});
   let kept=remote('cat /home/admin/api-dashboard/data/original.txt /home/admin/api-dashboard/data/browser-write.txt; sha256sum /home/admin/api-dashboard/data/.autobyteus-nfs/storage.json; findmnt -rn /Volumes/api-'+which);assert.ok(kept.stdout.includes('api-original-sentinel')&&kept.stdout.includes('native-browser-'+which));record('drained-detach-preserves-source-marker',{observation:kept,operation:detached});
 }
 assert.deepEqual(errors,[]);await stop();result.result='Pass';
 }catch(e){result.result='Fail';result.error=e.stack;try{await screenshot('failure');result.lastState=await state()}catch{};console.error(e.stack)}
 finally{
  // Never kill storage/helper. Request orderly dashboard stop only; retained VM handled separately.
  if(context){try{if(await page.locator('#chooser').isVisible())await page.locator('#close-chooser').click();await page.locator('#stop').click({timeout:2000});await until(()=>assert.ok(terminal.length),20000)}catch(e){result.cleanupWait=e.message}await context.close()}
  if(tunnel)tunnel.kill('SIGTERM');if(browser)await browser.close();
  result.terminal=terminal;fs.writeFileSync(E+'/'+id+'-runtime.json',JSON.stringify(result,null,2)+'\n');process.exitCode=result.result==='Pass'?0:1;
 }
})();
