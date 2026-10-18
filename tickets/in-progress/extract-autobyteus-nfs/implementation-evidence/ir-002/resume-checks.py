from pathlib import Path
import json,subprocess,time,hashlib
E=Path(__file__).resolve().parent
cfg=json.loads((E/'check-environment.json').read_text());P=Path(cfg['scratch']);R=P/'repo';env=cfg['env']
checks=[
 ('install',['pnpm','install','--frozen-lockfile','--filter','autobyteus-server-ts...','--filter','@autobyteus/application-backend-sdk...']),
 ('typecheck',['pnpm','-C','autobyteus-server-ts','typecheck']),
]
out=[]
for name,cmd in checks:
 t=time.time()
 with (E/f'{name}.log').open('w') as log:
  log.write('$ '+' '.join(cmd)+'\n');log.flush()
  r=subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 out.append(dict(name=name,command=cmd,exit=r.returncode,seconds=round(time.time()-t,3)))
 (E/'checks-result.json').write_text(json.dumps(out,indent=2)+'\n')
 print(name,r.returncode,flush=True)
 if r.returncode:break
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
paths=[p for p in subprocess.check_output(['git','-C',str(S),'ls-files','-z']).decode().split('\0') if p and not p.startswith('tickets/') and (S/p).is_file()]
mismatches=[p for p in paths if (S/p).read_bytes()!=(R/p).read_bytes()]
(E/'input-integrity.json').write_text(json.dumps(dict(files=len(paths),mismatches=mismatches),indent=2)+'\n')
assert not mismatches
raise SystemExit(any(c['exit'] for c in out))
