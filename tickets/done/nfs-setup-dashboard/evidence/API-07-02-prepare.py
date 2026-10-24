# API07 round2; 2026-10-24; current34afb80; Macarm64; independent source/Go preview preparation, no tests/storage effects.
from pathlib import Path
import tempfile,subprocess,shutil,hashlib,json,os,datetime,urllib.request,tarfile
n=Path.cwd();e=n/'tickets/in-progress/nfs-setup-dashboard/evidence';r=Path(json.loads((e/'API-07-02-environment.json').read_text())['scratch']) if (e/'API-07-02-environment.json').exists() else Path(tempfile.mkdtemp(prefix='nfs-dashboard-api002-',dir='/Users/normy'))
rec={'case':'API-07','round':'API-REV-002','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scratch':str(r),'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'sourceTests':'7b0577a4f2637ddf12a74a0156e4243a41a3719c','platform':subprocess.check_output(['uname','-sm'],text=True).strip(),'commands':[]}
file=e/'API-07-02-environment.json'
def save():file.write_text(json.dumps(rec,indent=2)+'\n')
save()
for p in ['home','tmp','cache','tools','source']: (r/p).mkdir(exist_ok=True)
inputs=[]
for rel in subprocess.check_output(['git','ls-files'],text=True).splitlines():
 p=n/rel
 if rel.startswith('tickets/') or not p.is_file():continue
 q=r/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);inputs.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
rec['sourceInputs']=inputs
url='https://go.dev/dl/go1.27.2.darwin-arm64.tar.gz';archive=r/'tools/go.tar.gz';urllib.request.urlretrieve(url,archive)
sha=hashlib.sha256(archive.read_bytes()).hexdigest();assert sha=='76812b213b1b2302c978d28fa52fa92d541704b9e7d9d5db8002c50e4018c4c5'
rec['Go']={'url':url,'sha256':sha}
subprocess.run(['/usr/bin/tar','-xzf',str(archive),'-C',str(r/'tools')],check=True)
env={**os.environ,'HOME':str(r/'home'),'TMPDIR':str(r/'tmp'),'GOCACHE':str(r/'cache'),'GOTOOLCHAIN':'local','PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD':'1'}
for cmd,cwd in [([str(r/'tools/go/bin/go'),'test','-c','-tags=dashboardpreview','-o',str(r/'dashboard-preview'),'./internal/dashboard'],r/'source'),(['npm','install','--prefix',str(r/'browser-tools'),'--no-audit','--no-fund','--ignore-scripts','playwright@1.64.1'],r)]:
 print('command',cmd,flush=True);p=subprocess.run(cmd,cwd=cwd,env=env);rec['commands'].append({'argv':cmd,'cwd':str(cwd),'exit':p.returncode});save();assert p.returncode==0
rec['binarySHA256']=hashlib.sha256((r/'dashboard-preview').read_bytes()).hexdigest();rec['result']='Prepared';save();print(str(r),flush=True)
