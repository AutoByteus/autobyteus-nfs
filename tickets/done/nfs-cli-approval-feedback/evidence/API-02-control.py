# API02 | 2026-10-24 | input4cf2eaa/e15e5e8 | Macarm64 isolated current/mutant Stop control; no root/OS/browser/storage.
from pathlib import Path
import os,subprocess,hashlib,shutil,json,tempfile,datetime,urllib.request
n=Path.cwd();e=n/'tickets/in-progress/nfs-cli-approval-feedback/evidence';r=Path(tempfile.mkdtemp(prefix='nfs-feedback-api-',dir='/Users/normy'));os.chmod(r,0o700)
rec={'case':'API-02','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'environment':'Macarm64 private source/HOME/TMP/cache; ordinary subprocess double','scratch':str(r),'attempts':[],'invalidPriorControl':'IMP07 Stop mutant failed compilation; not an assertion kill'}
file=e/'API-02-control.json'
def save():file.write_text(json.dumps(rec,indent=2)+'\n')
save()
for d in ['source','home','tmp','cache','tools']:(r/d).mkdir()
inputs=[]
for rel in subprocess.check_output(['git','ls-files'],text=True).splitlines():
 p=n/rel
 if rel.startswith('tickets/') or not p.is_file():continue
 q=r/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);inputs.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
rec['inputs']=inputs;save()
archive=r/'tools/go.tar.gz';url='https://go.dev/dl/go1.27.2.darwin-arm64.tar.gz';urllib.request.urlretrieve(url,archive)
sha=hashlib.sha256(archive.read_bytes()).hexdigest();assert sha=='76812b213b1b2302c978d28fa52fa92d541704b9e7d9d5db8002c50e4018c4c5'
rec['Go']={'url':url,'sha256':sha};save();subprocess.run(['/usr/bin/tar','-xzf',str(archive),'-C',str(r/'tools')],check=True)
env={**os.environ,'HOME':str(r/'home'),'TMPDIR':str(r/'tmp'),'GOCACHE':str(r/'cache'),'GOTOOLCHAIN':'local'}
cmd=[str(r/'tools/go/bin/go'),'test','./internal/dashboard','-run','^TestStopSuppressesFeedbackButDrainsAdmittedWork$','-count=1','-timeout=60s','-v']
source=r/'source/internal/dashboard/session.go';original=source.read_bytes();old=b's.closing = true; s.terminal.stop(); s.mu.Unlock()';assert original.count(old)==1
try:
 for name in ['current','mutant']:
  if name=='mutant':source.write_bytes(original.replace(old,b's.closing = true; s.mu.Unlock()'))
  out=e/f'API-02-{name}.log'
  with out.open('w') as f:
   f.write(f'# API02 {name} | {rec["date"]} | {rec["input"]} | Macarm64 Go1.27.2 | command {cmd}\n');f.flush();p=subprocess.run(cmd,cwd=r/'source',env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180);f.write(f'\n# exit={p.returncode}\n')
  log=out.read_text();row={'name':name,'command':cmd,'cwd':str(r/'source'),'exit':p.returncode,'log':out.name};rec['attempts'].append(row);save()
  if name=='current':assert p.returncode==0 and '--- PASS: TestStopSuppressesFeedbackButDrainsAdmittedWork' in log
  else:assert p.returncode!=0 and 'late phase after Stop' in log and '[build failed]' not in log
 rec['result']='Pass';rec['proof']='current passes; syntactically valid mutation fails late phase after Stop'
finally:
 source.write_bytes(original);rec['mutantRestored']=source.read_bytes()==original;save()
print(json.dumps({k:v for k,v in rec.items() if k!='inputs'},indent=2))
