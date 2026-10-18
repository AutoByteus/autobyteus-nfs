import hashlib,json,os,shutil,subprocess,time
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4];S=Path((E/'scratch-path.txt').read_text().strip());src=S/'source'
prior=json.loads((E/'source-inputs.json').read_text())
changes=[]
for name in prior:
 if (ROOT/name).is_file() and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=prior[name]:
  changes.append(name);shutil.copy2(ROOT/name,src/name)
assert set(changes)=={'scripts/tests/test_nfs_release_records.py','scripts/tests/test_nfs_engine_packaging.py','scripts/tests/test_nfs_packaging.py'},changes
(E/'final-test-delta.json').write_text(json.dumps({'changedAfterInitialChecks':changes,'productionChanged':False},indent=2)+'\n')
(E/'final-source-inputs.json').write_text(json.dumps({n:hashlib.sha256((src/n).read_bytes()).hexdigest() for n in prior},indent=2)+'\n')
env={'PATH':str(S/'go/bin')+':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(S/'home'),'TMPDIR':str(S/'tmp'),
     'GOCACHE':str(S/'cache'),'GOMODCACHE':str(S/'modcache'),'GOTOOLCHAIN':'local','PYTHONDONTWRITEBYTECODE':'1'}
results=[]
for name,args in [('python-final',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v']),
                  ('go-admission',['go','test','-race','./internal/cli','-run','TestRelease|TestEngineIdentity','-v']),
                  ('tool-versions',['/bin/bash','-c','sw_vers; uname -m; go version; python3 --version; /bin/bash --version; actionlint --version; shellcheck --version'])]:
 start=time.time()
 with (E/(name+'.log')).open('w') as log:r=subprocess.run(args,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append({'name':name,'command':args,'exitCode':r.returncode,'seconds':round(time.time()-start,2)})
(E/'focused-final.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['exitCode']==0 for x in results)
