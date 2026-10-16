from pathlib import Path
import subprocess,os,json,time,hashlib
E=Path(__file__).resolve().parent
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
P=Path((E/'consumer-scratch-path.txt').read_text().strip()); R=P/'repo'
env=dict(os.environ,PATH='/Users/normy/.nvm/versions/node/v22.21.1/bin:/opt/homebrew/bin:/usr/bin:/bin',HOME=str(P/'home'),TMPDIR=str(P/'tmp'),CI='true')
paths=[p for p in subprocess.check_output(['git','-C',str(S),'ls-files','-z']).decode().split('\0') if p and not p.startswith('tickets/')]
inputs=[dict(path=p,sha256=hashlib.sha256((S/p).read_bytes()).hexdigest()) for p in paths if (S/p).is_file()]
assert all((R/v['path']).is_file() and hashlib.sha256((R/v['path']).read_bytes()).hexdigest()==v['sha256'] for v in inputs)
(E/'consumer-final-inputs.json').write_text(json.dumps(dict(commit=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip(),inputs=inputs),indent=2)+'\n')
checks=[
 ('build',['pnpm','-C','autobyteus-server-ts','test:integration:prepare']),
 ('typecheck',['pnpm','-C','autobyteus-server-ts','exec','tsc','-p','tsconfig.build.json','--noEmit']),
 ('unit',['pnpm','-C','autobyteus-server-ts','exec','vitest','run','tests/unit/agent-execution/backends','tests/unit/agent-execution/services','tests/unit/agent-execution/agent-provider-factory-builder.test.ts','tests/unit/workspaces','tests/unit/services/terminal-streaming','tests/unit/runtime-management/codex','--maxWorkers=2']),
 ('local-routes',['pnpm','-C','autobyteus-server-ts','exec','vitest','run','tests/e2e/file-explorer/workspace-content-rest.e2e.test.ts','tests/e2e/skills/github-skill-sources-graphql.e2e.test.ts','tests/e2e/agent-definitions/agent-package-private-skills.e2e.test.ts','--maxWorkers=1']),
]
out=[]
for name,cmd in checks:
 t=time.time()
 with (E/f'consumer-final-{name}.log').open('w') as f:
  f.write('$ '+' '.join(cmd)+'\n');f.flush();r=subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 out.append(dict(name=name,command=cmd,exit=r.returncode,seconds=round(time.time()-t,3)))
 print(name,r.returncode,flush=True)
 (E/'consumer-final-checks.json').write_text(json.dumps(out,indent=2)+'\n')
 if r.returncode:break
assert all(hashlib.sha256((S/v['path']).read_bytes()).hexdigest()==v['sha256'] and hashlib.sha256((R/v['path']).read_bytes()).hexdigest()==v['sha256'] for v in inputs)
print('input hashes unchanged',flush=True)
raise SystemExit(any(c['exit'] for c in out))
