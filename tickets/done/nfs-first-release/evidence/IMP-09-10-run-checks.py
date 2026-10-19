"""IMP-09-10; 2026-10-19; owned independent Git clone, local checks only.
Command: python3 tickets/done/nfs-first-release/evidence/IMP-09-10-run-checks.py
Source: exact commit recorded in IMP-09-10-checks.json. No remote operations.
"""
import datetime
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

N=Path(__file__).resolve().parents[4]
E=Path(__file__).resolve().parent
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip()
root=Path(tempfile.mkdtemp(prefix='nfs-ir009-checks-',dir=Path.home())).resolve()
result={'check':'IMP-09-10','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'commit':commit,'environment':platform.platform(),'python':sys.version,'scratch':str(root),'checks':[]}
(E/'IMP-09-10-checks.json').write_text(json.dumps(result,indent=2)+'\n')
source=root/'source'
try:
    subprocess.run(['git','clone','--quiet','--no-hardlinks','--no-checkout',str(N),str(source)],check=True)
    subprocess.run(['git','checkout','--quiet','--detach',commit],cwd=source,check=True)
    env=os.environ.copy()
    for name in ('home','tmp','cache'):(root/name).mkdir(mode=0o700)
    env.update(HOME=str(root/'home'),TMPDIR=str(root/'tmp'),PYTHONDONTWRITEBYTECODE='1',
               PYTHONPYCACHEPREFIX=str(root/'cache'),GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1')
    commands=[('python',[sys.executable,'-m','unittest','discover','-s','scripts/tests','-p','test_nfs_release_publication.py','-v']),
              ('actionlint',['actionlint','.github/workflows/checks.yml','.github/workflows/release-nfs.yml']),
              ('bash',['/bin/bash','-n','scripts/public/nfs/install.sh','packaging/sign-macos.sh']),
              ('source-hash',[sys.executable,'packaging/release.py','--source-hash']),
              ('whitespace',['git','diff','--check',commit+'^',commit])]
    # Discover actual workflow names, avoiding a guessed CI filename.
    commands[1]=('actionlint',['actionlint',*[str(p.relative_to(source)) for p in sorted((source/'.github/workflows').glob('*.yml'))]])
    for label,command in commands:
        log=E/('IMP-09-10-'+label+'.log')
        with log.open('w') as out:
            out.write(f'Check: IMP-09-10/{label}\nCommand: {command!r}\nCommit: {commit}\nEnvironment: {platform.platform()}, Python {sys.version.split()[0]}\nDate: {result["date"]}\n\n');out.flush()
            p=subprocess.run(command,cwd=source,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=1200)
        result['checks'].append({'command':command,'exit':p.returncode,'log':log.name})
        (E/'IMP-09-10-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    result['cloneTrackedStatus']=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=source,text=True)
    result['result']='pass' if all(x['exit']==0 for x in result['checks']) and not result['cloneTrackedStatus'] else 'fail'
finally:
    shutil.rmtree(root)
    result['cleanup']='owned clone/home/tmp/cache removed'
    (E/'IMP-09-10-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
