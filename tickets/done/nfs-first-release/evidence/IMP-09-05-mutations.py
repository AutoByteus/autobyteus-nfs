"""IMP-09-05; 2026-10-19; current HEAD independent clone, controlled mutants only.
Command: python3 tickets/done/nfs-first-release/evidence/IMP-09-05-mutations.py
No remote or real publication effects; endpoint doubles and synthetic Git histories.
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

N=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip()
root=Path(tempfile.mkdtemp(prefix='nfs-ir009-mutants-',dir=Path.home())).resolve()
source=root/'source'
result={'check':'IMP-09-05','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'commit':commit,'environment':platform.platform(),'python':sys.version,'scratch':str(root),'checks':[]}
mutants=[
('omit-admission','publication.py',
 "recovery.admit(executor, source, tag_record)","(None, None)",
 'test_nfs_release_recovery.RecoveryTest.test_missing_authorization_blocks_effects_but_inspection_is_read_only'),
('omit-full-tree-scope','recovery.py',
 "    scope(executor.repository, source.commit, h, version, True)\n    scope(executor.repository, h, executor.commit, version, False)","    # mutant removes both full-tree scope checks",
 'test_nfs_release_recovery.RecoveryTest.test_excluded_generated_drift_is_rejected_by_admission'),
('verify-payload-at-executor','payload.py',"context = context or current()","context = current()",
 'test_nfs_release_recovery.RecoveryTest.test_distinct_git_context_full_chain_and_fresh_refusal'),
('published-only-discovery','publication.py',"def discover(directory, binding, expected_id=None):", "def discover(directory, binding, expected_id=None):\n    return api(RELEASES + '/tags/' + binding['version'], missing=True)",
 'test_nfs_release_publication.PublicationTest.test_published_only_404_does_not_hide_draft'),
('recreate-known-draft','publication.py',"        i.require(expected_id is None, 'Known release is missing; cannot recreate')","        pass # mutant discards known release identity",
 'test_nfs_release_recovery.RecoveryTest.test_missing_known_draft_wrong_job_and_main_dispatch_refuse'),
('omit-main-freshness','publication.py',"            fresh_main(ctx.executor.commit)","            pass # mutant omits main freshness",
 'test_nfs_release_publication.PublicationTest.test_fresh_resume_completed_and_stage_drift')]
try:
    subprocess.run(['git','clone','--quiet','--no-hardlinks','--no-checkout',str(N),str(source)],check=True)
    subprocess.run(['git','checkout','--quiet','--detach',commit],cwd=source,check=True)
    env=os.environ.copy()
    for name in ('home','tmp','cache'):(root/name).mkdir(mode=0o700)
    env.update(HOME=str(root/'home'),TMPDIR=str(root/'tmp'),PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX=str(root/'cache'),
               PYTHONPATH=str(source/'scripts/tests'),GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1')
    for label,file,before,after,test in mutants:
        path=source/'packaging/release_support'/file;original=path.read_text()
        assert original.count(before)==1,(file,before,original.count(before))
        path.write_text(original.replace(before,after))
        command=[sys.executable,'-m','unittest',test,'-v']
        log=E/('IMP-09-05-'+label+'.log')
        try:
            with log.open('w') as out:
                out.write(f'Check: IMP-09-05/{label}\nCommand: {command!r}\nCommit: {commit} plus isolated mutant {file}\nEnvironment: {platform.platform()}, Python {sys.version.split()[0]}\nDate: {result["date"]}\n\n');out.flush()
                p=subprocess.run(command,cwd=source,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=600)
            raw=log.read_text()
            detected=p.returncode!=0 and 'FAILED (' in raw and 'SyntaxError' not in raw and 'ModuleNotFoundError' not in raw
            result['checks'].append({'mutant':label,'test':test,'exit':p.returncode,'detected':detected,'log':log.name})
        finally:path.write_text(original)
        (E/'IMP-09-05-mutations.json').write_text(json.dumps(result,indent=2)+'\n')
    result['result']='pass' if len(result['checks'])==len(mutants) and all(x['detected'] for x in result['checks']) else 'fail'
finally:
    shutil.rmtree(root);result['cleanup']='owned mutant clone/home/tmp/cache removed'
    (E/'IMP-09-05-mutations.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
