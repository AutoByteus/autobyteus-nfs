# R07; run actual-byte emulation in isolated current local clone, cleanup;6cb497f/22205cc; macOSarm64/Python3.9.6;2026-10-19UTC.
from pathlib import Path
import subprocess,tempfile,os,json,datetime,shutil
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip();inspection=json.loads((E/'R04-07-ownership.json').read_text())['directory']
with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | R07 | Started | Not Tested | Independent clone/current code/actual signed bytes; synthetic authority and all external writes locally emulated only. |\n')
root=Path(tempfile.mkdtemp(prefix='nfs-api007-emulated-',dir=Path.home()));repo=root/'repo';result={}
try:
 (root/'home').mkdir();(root/'tmp').mkdir();env={'PATH':os.environ['PATH'],'HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),'PYTHONDONTWRITEBYTECODE':'1'}
 subprocess.run(['git','clone','--quiet','--no-hardlinks','--local',str(N),str(repo)],check=True,capture_output=True,timeout=120,env=env)
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True,env=env).strip()==head
 cmd=['/usr/bin/python3',str(E/'R07-07-worker.py'),str(repo),inspection,str(E/'R06-07-observations.json'),str(root/'result.json')]
 p=subprocess.run(cmd,cwd=repo,env=env,text=True,capture_output=True,timeout=900)
 (E/'R07-07-console.log').write_text(f'# R07; command {cmd!r}; reviewed{head}; localisolatedMacarm64/privateHOME+TMP;{now()}\n'+p.stdout+p.stderr+f'\nExit:{p.returncode}\n')
 if (root/'result.json').exists():result=json.loads((root/'result.json').read_text());(E/'R07-07-result.json').write_text(json.dumps(result,indent=2)+'\n')
 assert p.returncode==0,p.stderr
finally:
 shutil.rmtree(root)
 (E/'R07-07-cleanup.json').write_text(json.dumps({'case':'R07','step':'Remove only own isolated clone/synthetic authorization/emulated results','date':now(),'commit':head,'environment':'localAPFS','root':str(root),'absent':not root.exists(),'realAuthorityAbsent':not (N/'packaging/recovery/v0.1.0/authorization.json').exists()},indent=2)+'\n')
assert result['pass']
p=T/'api-e2e-execution-coverage-report.md';lines=p.read_text().splitlines()
for idx,l in enumerate(lines):
 if l.startswith('| R07 |'):
  a=l.split('|');a[-3]=' Pass ';a[-2]=' R07-07-result.json/console.log/cleanup.json: actual old bytes/current full prepare+publish;18streamed emulated uploads/sameID, completed retry read-only; known missing and hash-excluded drift refuse; clone removed. ';lines[idx]='|'.join(a)
p.write_text('\n'.join(lines)+'\n')
with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | R07 | Completed | Pass | Actual-byte complete current orchestration/admission with emulated effects; known-missing/excluded drift safeguards; no real authority/effects, clone removed. |\n')
print('R07 PASS')
