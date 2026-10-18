import hashlib,json,os,shutil,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[4];S=Path((E/'scratch-path.txt').read_text().strip());src=S/'source'
old=json.loads((E/'final-source-inputs.json').read_text());changed=[]
for n,h in old.items():
 if hashlib.sha256((R/n).read_bytes()).hexdigest()!=h:
  changed.append(n);shutil.copy2(R/n,src/n)
assert changed==['packaging/release_support/candidate.py'],changed
(E/'final-comment-delta.json').write_text(json.dumps({'changed':changed,'detail':'Only fetch docstring Qualification -> Readiness; executable behavior identical. Prior native Go/Linux checks carry; final Python whole suite rerun.'},indent=2)+'\n')
(E/'final-source-inputs.json').write_text(json.dumps({n:hashlib.sha256((src/n).read_bytes()).hexdigest() for n in old},indent=2)+'\n')
env={'PATH':str(S/'go/bin')+':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(S/'home'),'TMPDIR':str(S/'tmp'),
     'GOCACHE':str(S/'cache'),'GOMODCACHE':str(S/'modcache'),'GOTOOLCHAIN':'local','PYTHONDONTWRITEBYTECODE':'1'}
results=[]
for name,args in [('python-current',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v']),
                  ('source-hash-current',['/usr/bin/python3','packaging/release.py','--source-hash'])]:
 with (E/(name+'.log')).open('w') as log:r=subprocess.run(args,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append({'name':name,'command':args,'exitCode':r.returncode})
(E/'current-checks.json').write_text(json.dumps(results,indent=2)+'\n');assert all(x['exitCode']==0 for x in results)
