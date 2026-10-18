const fs=require('fs');const cp=require('child_process');const path=require('path');
const ts=require('/Users/normy/autobyteus_org/autobyteus-workspace-superrepo/autobyteus-server-ts/node_modules/typescript/lib/typescript.js');
const S='/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs';
const names=cp.execFileSync('git',['-C',S,'diff','--name-only','3712cd9b','HEAD'],{encoding:'utf8'}).trim().split('\n').filter(x=>x.includes('/src/')&&x.endsWith('.ts')&&fs.existsSync(path.join(S,x)));
const options={noEmit:true,noResolve:true,noUnusedLocals:true,target:ts.ScriptTarget.ESNext,module:ts.ModuleKind.ESNext,skipLibCheck:true};
const program=ts.createProgram(names.map(x=>path.join(S,x)),options);
const diagnostics=program.getSemanticDiagnostics().filter(d=>[6133,6192,6196].includes(d.code)).map(d=>({path:path.relative(S,d.file.fileName),line:d.file.getLineAndCharacterOfPosition(d.start).line+1,code:d.code,message:ts.flattenDiagnosticMessageText(d.messageText,'\n')}));
fs.writeFileSync(path.join(__dirname,'unused-imports.json'),JSON.stringify({typescript:ts.version,scope:'No-emit/no-resolution compiler unused-local analysis only; not a full production typecheck.',files:names,diagnostics},null,2)+'\n');
console.log(JSON.stringify(diagnostics,null,2));

if (diagnostics.length) process.exitCode = 1;
