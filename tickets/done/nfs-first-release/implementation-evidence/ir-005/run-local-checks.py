"""Current independent release-boundary checks; never real signing/publication."""
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

E = Path(__file__).resolve().parent
R = E.parents[4]
S = Path(tempfile.mkdtemp(prefix='nfs-release-ir005-', dir='/Users/normy/autobyteus_org'))
(E/'scratch-path.txt').write_text(str(S)+'\n')
source = S/'source'; source.mkdir()
paths = subprocess.check_output(['git','ls-files'], cwd=R).decode().splitlines()
paths = [p for p in paths if not p.startswith(('tickets/', 'task-plans/'))]
for p in paths:
    target = source/p; target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(R/p, target)
for name in ('home','tmp'):(S/name).mkdir()
env = {'PATH':'/usr/bin:/bin:/usr/sbin:/sbin', 'HOME':str(S/'home'),
       'TMPDIR':str(S/'tmp'), 'PYTHONDONTWRITEBYTECODE':'1'}
results = []

def run(name, args, expected=0):
    start = time.time()
    with (E/(name+'.log')).open('w') as log:
        p = subprocess.run(args, cwd=source, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=300)
    results.append({'name':name, 'command':args, 'exitCode':p.returncode,
                    'expected':expected, 'passed':p.returncode==expected, 'seconds':round(time.time()-start,2)})
    (E/'checks-result.json').write_text(json.dumps(results, indent=2)+'\n')
    print(results[-1], flush=True)

try:
    run('python-version', ['/usr/bin/python3','--version'])
    run('bash-version', ['/bin/bash','--version'])
    run('python-all', ['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
    run('bash-syntax', ['/bin/bash','-n','packaging/sign-macos.sh'])
    run('shellcheck', ['/opt/homebrew/bin/shellcheck','packaging/sign-macos.sh'])
    run('actionlint', ['/opt/homebrew/bin/actionlint','.github/workflows/release-nfs.yml'])
    run('source-hash', ['/usr/bin/python3','packaging/release.py','--source-hash'])
    run('recipe-hash', ['/usr/bin/python3','-c','import sys;sys.path.insert(0,"packaging/engine");import source;print(source.recipe_hash())'])
    run('stale-readiness-refusal', ['/usr/bin/python3','packaging/release.py','--check-publish'], 1)
    # Mutate only this disposable copy, prove the new assertions notice violations.
    sign = source/'packaging/sign-macos.sh'; original = sign.read_text()
    controls = [
        ('mutation-hidden-diagnostic', '"$cleanup_status" >&3', '"$cleanup_status" >/dev/null', 'test_import_failure_receipt_and_secret_safety'),
        ('mutation-ignore-errexit', 'sign_and_notarize >/dev/null 2>&1', 'if sign_and_notarize >/dev/null 2>&1; then :; fi', 'test_import_failure_receipt_and_secret_safety'),
        ('mutation-restore-failed-capture', '> "$scratch/search-pending.json"\n  mv -- "$scratch/search-pending.json" "$scratch/search.json"', '> "$scratch/search.json"', 'test_command_failures_report_exact_stage_and_exit'),
        ('mutation-accept-invalid-notary', "assert json.load(open(sys.argv[1]))['status'] == 'Accepted', 'Notarization not Accepted'", "json.load(open(sys.argv[1]))", 'test_rejected_or_pending_notary_retains_known_receipt_but_fails')]
    for name, old, new, test in controls:
        assert old in original
        sign.write_text(original.replace(old,new,1))
        run(name, ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing.SigningTest.'+test,'-v'], 1)
        sign.write_text(original)
    # Reproduce the actual baseline hash with only the two production edits restored.
    intake = json.loads((E/'intake.json').read_text())['head']
    for p in ('packaging/sign-macos.sh','.github/workflows/release-nfs.yml'):
        (source/p).write_bytes(subprocess.check_output(['git','show',intake+':'+p],cwd=R))
    run('source-hash-before', ['/usr/bin/python3','packaging/release.py','--source-hash'])
    for p in ('packaging/sign-macos.sh','.github/workflows/release-nfs.yml'):shutil.copy2(R/p,source/p)
    assert all((R/p).read_bytes() == (source/p).read_bytes() for p in paths)
    assert (E/'source-hash-before.log').read_text().strip() == 'a425e3f887f3156d920d022801df9069ba5bc2d49bdb0e4dd8097ee76a01fe9e'
    assert (E/'source-hash.log').read_text() != (E/'source-hash-before.log').read_text()
    (E/'source-check.json').write_text(json.dumps({'copiedFiles':len(paths), 'copyMatchesWorktree':True,
        'sourceBefore':(E/'source-hash-before.log').read_text().strip(),
        'sourceAfter':(E/'source-hash.log').read_text().strip(),
        'recipeHash':(E/'recipe-hash.log').read_text().strip(),
        'notes':'Actual current measured-engine lock preserved; old readiness now correctly stale. No new candidate/engine/real signing.'},indent=2)+'\n')
    assert all(x['passed'] for x in results)
finally:
    shutil.rmtree(S)
    (E/'cleanup.json').write_text(json.dumps({'ownedScratch':str(S), 'absent':not S.exists(),
        'testOwnedCommandDoublesOnly':True, 'retainedCandidateOrLiveKeychainTouched':False,
        'remoteActions':False},indent=2)+'\n')
