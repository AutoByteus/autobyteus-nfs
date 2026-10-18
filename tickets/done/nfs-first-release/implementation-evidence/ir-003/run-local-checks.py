"""Implementation-only independent copy checks; never dispatch/sign/publish."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parents[5]
E=Path(__file__).resolve().parent
S=Path((E/'scratch-path.txt').read_text().strip())
source=Path(os.environ.get('NFS_CHECK_SOURCE',str(S/'source')))
source.mkdir()
names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
for name in names:
    if name.startswith('tickets/'):continue
    path=ROOT/name
    if not path.is_file():continue
    dst=source/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dst)
inventory={p.relative_to(source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('*') if p.is_file()}
(E/'source-inputs.json').write_text(json.dumps(inventory,indent=2,sort_keys=True)+'\n')
for name in ['home','tmp','cache','modcache','out']:(S/name).mkdir(exist_ok=True)
env=os.environ|{'HOME':str(S/'home'),'TMPDIR':str(S/'tmp'),'PATH':str(S/'go/bin')+':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin',
                'GOCACHE':str(S/'cache'),'GOMODCACHE':str(S/'modcache'),'GOTOOLCHAIN':'local','PYTHONDONTWRITEBYTECODE':'1'}
# Do not forward account tokens to test subprocesses.
for name in list(env):
    if any(x in name.upper() for x in ('TOKEN','PASSWORD','SECRET','CERTIFICATE')):env.pop(name)
results=[]
def run(name,args,extra=None,expected=0,cwd=source):
    started=time.time()
    with (E/(name+'.log')).open('w') as log:
        process=subprocess.run(args,cwd=cwd,env=env|(extra or {}),stdout=log,stderr=subprocess.STDOUT)
    result={'name':name,'command':args,'exitCode':process.returncode,'expected':expected,'seconds':round(time.time()-started,2),
            'passed':process.returncode==expected}
    results.append(result);(E/'checks-result.json').write_text(json.dumps(results,indent=2)+'\n');print(result,flush=True)
    return result['passed']
run('python',['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
run('actionlint',['/opt/homebrew/bin/actionlint','.github/workflows/ci.yml','.github/workflows/release-nfs.yml'])
run('bash-syntax',['/bin/bash','-n','packaging/sign-macos.sh','scripts/public/nfs/install.sh'])
run('shellcheck',['/opt/homebrew/bin/shellcheck','packaging/sign-macos.sh','scripts/public/nfs/install.sh'])
run('source-hash',['/usr/bin/python3','packaging/release.py','--source-hash'])
run('publish-refusal',['/usr/bin/python3','packaging/release.py','--check-publish'],expected=1)
run('go-race',['go','test','-race','./...'])
run('go-vet',['go','vet','./...'])
run('go-native-build',['go','build','-o',str(S/'out/autobyteus-nfs'),'./cmd/autobyteus-nfs'])
run('native-version',[str(S/'out/autobyteus-nfs'),'version'])
for os_name in ('darwin','linux'):
    for arch in ('arm64','amd64'):
        run('compile-'+os_name+'-'+arch,['go','build','-trimpath','-o',str(S/'out'/('nfs-'+os_name+'-'+arch)),'./cmd/autobyteus-nfs'],
            {'CGO_ENABLED':'0','GOOS':os_name,'GOARCH':arch})
raise SystemExit(0 if all(x['passed'] for x in results) else 1)
