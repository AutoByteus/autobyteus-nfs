# Case R02; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment local macOS26.5.2 arm64; Python3.9.6/Bash3.2.57
# Step: resume-local.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import subprocess,tempfile,json,hashlib,shutil,datetime
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2];audit=json.loads((E/'input-audit.json').read_text())
root=Path(tempfile.mkdtemp(prefix='nfs-first-api003-control-',dir=Path.home()));src=root/'source';src.mkdir()
for name,h in audit['source'].items():
 assert hashlib.sha256((N/name).read_bytes()).hexdigest()==h
 d=src/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(N/name,d)
for n in ['home','tmp']:(root/n).mkdir()
env={'PATH':'/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),'PYTHONDONTWRITEBYTECODE':'1','LANG':'en_US.UTF-8'}
rows=[]
commands=[('recipe-hash-corrected',['/usr/bin/python3','-c',"import sys;sys.path.insert(0,'packaging/engine');import source;print(source.recipe_hash())"],0,'299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274'),('readiness-refusal',['/usr/bin/python3','packaging/release.py','--check-publish'],1,'Current engine and structured release readiness required'),('shell-syntax',['/bin/bash','-n','scripts/public/nfs/install.sh','packaging/sign-macos.sh'],0,''),('shellcheck',['/opt/homebrew/bin/shellcheck','scripts/public/nfs/install.sh','packaging/sign-macos.sh'],0,'')]
try:
 for name,args,expect,needle in commands:
  p=subprocess.run(args,cwd=src,env=env,capture_output=True,text=True,timeout=120)
  (E/(name+'.log')).write_text('$ '+' '.join(args)+'\ncwd '+str(src)+'\n'+p.stdout+p.stderr)
  r=dict(name=name,command=args,exit=p.returncode,expected=expect,pass_=p.returncode==expect and needle in p.stdout+p.stderr);rows.append(r)
  (E/'local-control-results.json').write_text(json.dumps(rows,indent=2)+'\n')
  with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R02 | '+('Pass' if r['pass_'] else 'Fail')+' '+name+' | '+name+'.log |\n')
  assert r['pass_'],r
finally:
 mismatches=[p for p,h in audit['source'].items() if hashlib.sha256((src/p).read_bytes()).hexdigest()!=h or hashlib.sha256((N/p).read_bytes()).hexdigest()!=h]
 shutil.rmtree(root)
 (E/'cleanup-local-controls.json').write_text(json.dumps(dict(root=str(root),absent=not root.exists(),mismatches=mismatches),indent=2)+'\n')
 assert not mismatches
print('4 corrected/remaining checks pass; initial wrong-command attempt preserved')
