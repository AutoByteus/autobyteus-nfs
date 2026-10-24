// IMP-06 | current IR001 source | 2026-10-24 | owned Chromium/current local assets
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.NFS_PLAYWRIGHT_MODULE);
(async()=>{
 const dir=process.env.NFS_FB_DIR, mode=process.env.NFS_FB_MODE;
 const browser=await chromium.launch({headless:true});
 try{
  const context=await browser.newContext({viewport:{width:1100,height:900}});
  const page=await context.newPage();
  await page.goto(JSON.parse(fs.readFileSync(path.join(dir,'connection.json'),'utf8')).url);
  await page.locator('#authorize').click();console.log('submitted');
  if(mode==='success'){
   await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('Not configured.'));
   await page.screenshot({path:path.join(dir,'ready.png')});
   await page.locator('#stop').click();
  }else if(mode==='denied'||mode==='refused'){
   await page.locator('#error').waitFor({state:'visible'});
   await page.locator('#stop').click();
  }else{
   while(!fs.existsSync(path.join(dir,'browser-go'))) await new Promise(r=>setTimeout(r,20));
   if(mode==='hold-inspect')await page.locator('#stop').click();
  }
  console.log('browser-complete');await context.close();
 }finally{await browser.close()}
})().catch(e=>{console.error(e.message.replace(/http:\/\/127\.0\.0\.1:\d+\/#[^\s]+/g,'[private URL]'));process.exitCode=1});
