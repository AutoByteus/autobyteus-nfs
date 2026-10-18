from pathlib import Path
import subprocess,tempfile,shutil,json,hashlib,time
E=Path(__file__).resolve().parent
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
P=Path(tempfile.mkdtemp(prefix='nfs-extract-ir002-'))
(E/'scratch-path.txt').write_text(str(P)+'\n')
R=P/'repo';R.mkdir()
inputs=[]
for rel in subprocess.check_output(['git','-C',str(S),'ls-files','-z']).decode().split('\0'):
 if not rel or rel.startswith('tickets/'):continue
 f=S/rel
 if not f.is_file():continue
 d=R/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,d)
 inputs.append(dict(path=rel,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
for d in ['home','tmp']:(P/d).mkdir()
env={'PATH':'/Users/normy/.nvm/versions/node/v22.21.1/bin:/opt/homebrew/bin:/usr/bin:/bin','HOME':str(P/'home'),'TMPDIR':str(P/'tmp'),'CI':'true','COREPACK_ENABLE_DOWNLOAD_PROMPT':'0'}
(E/'check-environment.json').write_text(json.dumps(dict(scratch=str(P),env=env,inputs_count=len(inputs),source_head=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip(),source_patch='source.diff'),indent=2)+'\n')
checks=[
 ('install',['pnpm','install','--frozen-lockfile','--filter','autobyteus-server-ts...']),
 ('prisma',['pnpm','-C','autobyteus-server-ts','exec','prisma','generate','--schema','./prisma/schema.prisma']),
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
mismatches=[v['path'] for v in inputs if hashlib.sha256((S/v['path']).read_bytes()).hexdigest()!=v['sha256'] or hashlib.sha256((R/v['path']).read_bytes()).hexdigest()!=v['sha256']]
(E/'input-integrity.json').write_text(json.dumps(dict(files=len(inputs),mismatches=mismatches),indent=2)+'\n')
assert not mismatches
raise SystemExit(any(c['exit'] for c in out))
