import fs from 'node:fs/promises';
import {createWriteStream} from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import net from 'node:net';
import assert from 'node:assert/strict';
const E=path.dirname(fileURLToPath(import.meta.url));
const P=(await fs.readFile(path.join(E,'consumer-scratch-path.txt'),'utf8')).trim();
const web=path.join(P,'repo/autobyteus-web');
const {chromium}=await import(pathToFileURL(path.join(web,'node_modules/playwright-core/index.mjs')));
const route=path.join(web,'pages/implementation-nfs-guide.vue');
const out=path.join(E,'guide-render');await fs.mkdir(out);
const result={layer:'implementation rendered component, not live app/storage qualification',events:[],states:[]};
let child,browser,log;
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const server=net.createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));const port=server.address().port;await new Promise(r=>server.close(r));
try{
 await fs.writeFile(route,`<template><main class="min-h-screen bg-slate-100 p-4"><nav class="mb-3 flex gap-4"><button id="en" @click="setPreference('en')">English</button><button id="zh" @click="setPreference('zh-CN')">中文</button></nav><NfsGuideCard :release="nfsPublishedRelease" /></main></template><script setup lang="ts">import NfsGuideCard from '~/components/settings/NfsGuideCard.vue';import {nfsPublishedRelease} from '~/utils/nfsLauncherCommands';import {useLocalization} from '~/composables/useLocalization';definePageMeta({layout:false});const {setPreference}=useLocalization();</script>`,{flag:'wx'});
 log=createWriteStream(path.join(out,'nuxt.log'));
 child=spawn(path.join(web,'node_modules/.bin/nuxi'),['dev','--host','127.0.0.1','--port',String(port)],{cwd:web,detached:true,env:{...process.env,NUXT_TELEMETRY_DISABLED:'1',BACKEND_NODE_BASE_URL:'http://127.0.0.1:9'},stdio:['ignore','pipe','pipe']});child.stdout.pipe(log);child.stderr.pipe(log);result.nuxtPid=child.pid;result.port=port;
 const url=`http://127.0.0.1:${port}/implementation-nfs-guide`;
 let ready=false;for(let i=0;i<240;i++){try{if((await fetch(url)).ok){ready=true;break;}}catch{} if(child.exitCode!==null)throw Error('Nuxt exited');await wait(500);}assert(ready,'Nuxt readiness');
 browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1100},locale:'en-US'});
 page.on('pageerror',error=>result.events.push({kind:'pageerror',message:error.message}));
 await page.route('**/graphql',r=>r.fulfill({contentType:'application/json',body:JSON.stringify({data:{serverSettings:[],agentDefinitions:[],agentTeamDefinitions:[],workspaces:[]}})}));
 await page.routeWebSocket(/\/ws\//,ws=>{ws.send(JSON.stringify({type:'connected'}));});
 await page.goto(url);await page.locator('[data-testid="nfs-guide-card"]').waitFor();await wait(2500);
 for(const locale of ['en','zh']){
  await page.locator('#'+locale).click();await wait(200);
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:1100});const card=page.locator('[data-testid="nfs-guide-card"]');
   assert.equal(await card.locator('button').count(),2);
   for(const button of await card.locator('button').all())assert(await button.isDisabled());
   assert.equal(await card.locator('a').count(),0);assert.equal(await card.locator('pre').count(),0);
   const state=await card.evaluate(el=>({text:el.innerText,width:el.getBoundingClientRect().width,scroll:document.documentElement.scrollWidth,viewport:innerWidth}));
   assert(state.scroll<=state.viewport,'horizontal overflow');
   if(locale==='en'){assert(state.text.includes('does not detect or manage'));assert(!state.text.includes('Select only the local Docker nodes'));}
   else assert(state.text.includes('不检测或管理'));
   await page.screenshot({path:path.join(out,`${locale}-${width}.png`),fullPage:true});result.states.push({locale,width,...state});
  }
 }
 result.result='Pass';
}catch(error){result.result='Fail';result.error=error.stack;process.exitCode=1;}
finally{
 await browser?.close();if(child?.pid){try{process.kill(-child.pid,'SIGTERM');}catch{}await wait(1000);try{process.kill(-child.pid,0);process.kill(-child.pid,'SIGKILL');}catch{}}
 log?.end();await fs.rm(route,{force:true});result.cleanup={browserClosed:true,routeRemoved:true,nuxtStopped:child?.exitCode!==null};
 await fs.writeFile(path.join(out,'result.json'),JSON.stringify(result,null,2)+'\n');
}
