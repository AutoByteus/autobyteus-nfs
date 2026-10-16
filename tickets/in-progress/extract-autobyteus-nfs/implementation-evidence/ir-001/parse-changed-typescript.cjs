const fs=require('fs'),cp=require('child_process'),path=require('path');
const E=__dirname,S='/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs';
const P=fs.readFileSync(path.join(E,'consumer-scratch-path.txt'),'utf8').trim();
const ts=require(path.join(P,'repo/autobyteus-server-ts/node_modules/typescript'));
const paths=cp.execFileSync('git',['-C',S,'diff','--name-only','3712cd9bf0db998501d162db7f8655f169e3def6','HEAD'],{encoding:'utf8'}).trim().split('\n');
let errors=[],checked=[];
for(const p of paths.filter(p=>p.endsWith('.ts')&&fs.existsSync(path.join(S,p)))){
 const s=ts.createSourceFile(p,fs.readFileSync(path.join(S,p),'utf8'),ts.ScriptTarget.Latest,true);
 checked.push(p);for(const d of s.parseDiagnostics)errors.push({path:p,message:ts.flattenDiagnosticMessageText(d.messageText,'\n'),start:d.start});
}
const result={scope:'Changed TypeScript parse diagnostics, not full test semantic typecheck',checked,errors};
fs.writeFileSync(path.join(E,'changed-typescript-parse.json'),JSON.stringify(result,null,2)+'\n');
console.log(checked.length,'files;',errors.length,'parse errors');process.exitCode=errors.length?1:0;
