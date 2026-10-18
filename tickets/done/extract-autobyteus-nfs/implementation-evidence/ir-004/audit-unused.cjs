// Derived from CRR004 read-only audit; same29 files, own output only.
const fs=require('fs'),path=require('path'),cp=require('child_process'),assert=require('assert');
const ts=require('/Users/normy/autobyteus_org/autobyteus-workspace-superrepo/autobyteus-server-ts/node_modules/typescript/lib/typescript.js');
const S='/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs';
const prior=JSON.parse(fs.readFileSync(path.join(__dirname,'../../code-review-evidence/crr-002/unused-imports.json'),'utf8')).files;
const tests=['tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts','tests/unit/agent-execution/backends/codex/backend/codex-thread-bootstrapper.test.ts','tests/unit/agent-execution/backends/codex/thread/codex-thread-manager.test.ts','tests/integration/application-backend/brief-package-team-prompt.integration.test.ts'].map(p=>'autobyteus-server-ts/'+p);
const names=[...prior,...tests];
const options={noEmit:true,noResolve:true,noUnusedLocals:true,target:ts.ScriptTarget.ESNext,module:ts.ModuleKind.ESNext,skipLibCheck:true};
const program=ts.createProgram(names.map(p=>path.join(S,p)),options);
const diagnostics=program.getSemanticDiagnostics().filter(d=>[6133,6192,6196].includes(d.code)).map(d=>({path:path.relative(S,d.file.fileName),line:d.file.getLineAndCharacterOfPosition(d.start).line+1,code:d.code,message:ts.flattenDiagnosticMessageText(d.messageText,'\n')}));
const result={typescript:ts.version,scope:'Read-only compiler unused-local analysis of the25 R2 production files plus4 overlapping test files. Not a full semantic typecheck.',production:prior,tests,diagnostics};
fs.writeFileSync(path.join(__dirname,process.argv[2]||'unused-locals.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({typescript:ts.version,production_files:prior.length,tests:tests.length,diagnostics},null,2));
if(diagnostics.length)process.exitCode=1;
