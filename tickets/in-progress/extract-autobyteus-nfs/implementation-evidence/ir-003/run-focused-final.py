from pathlib import Path
import subprocess,json,time,hashlib
E=Path(__file__).resolve().parent;cfg=json.loads((E/'check-environment.json').read_text());R=Path(cfg['scratch'])/'repo'
cmd=['pnpm','-C','autobyteus-server-ts','exec','vitest','run','tests/unit/agent-execution/backends/codex/backend/codex-thread-bootstrapper.test.ts','tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts','tests/unit/agent-execution/backends/codex/thread/codex-thread-manager.test.ts','tests/unit/agent-execution/agent-run-manager.test.ts','tests/unit/agent-execution/agent-run-input-preface.test.ts','tests/integration/application-backend/brief-package-team-prompt.integration.test.ts','--maxWorkers=2','--no-watch']
t=time.time()
with (E/'focused-final.log').open('w') as log:
 log.write('$ '+' '.join(cmd)+'\n');log.flush()
 r=subprocess.run(cmd,cwd=R,env=cfg['env'],stdout=log,stderr=subprocess.STDOUT)
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
out=dict(command=cmd,exit=r.returncode,seconds=round(time.time()-t,3),commit=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip())
(E/'focused-final-result.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
inputs=json.loads((E/'source-inputs.json').read_text())
changed=[v['path'] for v in inputs if hashlib.sha256((S/v['path']).read_bytes()).hexdigest()!=v['sha256']]
assert changed==['autobyteus-server-ts/tests/unit/agent-execution/backends/codex/backend/codex-thread-bootstrapper.test.ts'],changed
assert all((S/v['path']).read_bytes()==(R/v['path']).read_bytes() for v in inputs)
(E/'final-input-integrity.json').write_text(json.dumps(dict(files=len(inputs),source_changes_since_broad=changed,final_copy_matches=True),indent=2)+'\n')
raise SystemExit(r.returncode)
