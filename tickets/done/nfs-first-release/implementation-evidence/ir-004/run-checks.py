"""Proportional import-only local checks in an independent source copy."""
import hashlib,json,os,shutil,subprocess,tempfile,time
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[4]
S=Path(tempfile.mkdtemp(prefix='nfs-release-ir004-',dir='/Users/normy/autobyteus_org'))
(E/'scratch-path.txt').write_text(str(S)+'\n')
a=json.loads((E/'input-audit.json').read_text());source=S/'source';source.mkdir()
for name in a['sourceInputs']:
 out=source/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/name,out)
for name in ('home','tmp'):(S/name).mkdir()
env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(S/'home'),'TMPDIR':str(S/'tmp'),'PYTHONDONTWRITEBYTECODE':'1'}
results=[]
def run(name,args,expected=0):
 start=time.time()
 with (E/(name+'.log')).open('w') as log:p=subprocess.run(args,cwd=source,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append({'name':name,'command':args,'exitCode':p.returncode,'expected':expected,'passed':p.returncode==expected,'seconds':round(time.time()-start,2)})
 (E/'checks-result.json').write_text(json.dumps(results,indent=2)+'\n');print(results[-1],flush=True)
run('python-version',['/usr/bin/python3','--version'])
run('python-all',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
run('source-hash',['/usr/bin/python3','packaging/release.py','--source-hash'])
run('recipe-hash',['/usr/bin/python3','-c','import sys;sys.path.insert(0,"packaging/engine");import source;print(source.recipe_hash())'])
run('readiness-refusal',['/usr/bin/python3','packaging/release.py','--check-publish'],1)
inventory={n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in a['sourceInputs']}
assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==v for n,v in inventory.items())
changed={n for n,v in inventory.items() if v!=a['sourceInputs'][n]}
assert changed=={'packaging/engine/manifest.py','scripts/tests/nfs_release_fixture.py'},changed
assert (E/'source-hash.log').read_text()!=(E/'source-hash-before.log').read_text()
assert (E/'recipe-hash.log').read_text()!=(E/'recipe-hash-before.log').read_text()
(E/'source-inputs.json').write_text(json.dumps(inventory,indent=2)+'\n')
(E/'hash-transition.json').write_text(json.dumps({'sourceBefore':(E/'source-hash-before.log').read_text().strip(),'sourceAfter':(E/'source-hash.log').read_text().strip(),'recipeBefore':(E/'recipe-hash-before.log').read_text().strip(),'recipeAfter':(E/'recipe-hash.log').read_text().strip(),'delta':sorted(changed),'other118InputsUnchanged':True,'note':'Actual recipe/source hash changed. No new engine built; NEW complete current-source hosted candidate remains required.'},indent=2)+'\n')
shutil.rmtree(S)
(E/'cleanup.json').write_text(json.dumps({'result':'Complete','ownedScratch':str(S),'absent':not S.exists(),'newProcessesOrResources':'none retained','GoLinuxHostedSigningLiveStorage':'not executed','retainedAPI002Candidate':'untouched'},indent=2)+'\n')
assert all(x['passed'] for x in results)
