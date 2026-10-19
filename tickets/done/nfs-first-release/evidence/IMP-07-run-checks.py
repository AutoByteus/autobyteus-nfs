"""IMP-07: independent local keychain lookup checks, no real signing or remote effects.
Command: python3 tickets/done/nfs-first-release/evidence/IMP-07-run-checks.py
Commit: recorded from git at execution; environment Darwin arm64/Python3.9.6/Bash3.2.
Date: 2026-10-19. No source change is made by this runner.
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

E = Path(__file__).resolve().parent
R = E.parents[3]
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
S = Path(tempfile.mkdtemp(prefix='nfs-release-ir007-', dir='/Users/normy/autobyteus_org'))
source = S/'source'; source.mkdir()
paths = subprocess.check_output(['git', 'ls-files'], cwd=R, text=True).splitlines()
paths = [p for p in paths if not p.startswith(('tickets/', 'task-plans/'))]
for p in paths:
    target = source/p; target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(R/p, target)
for p in ('home', 'tmp'):(S/p).mkdir()
env = {'PATH':'/usr/bin:/bin:/usr/sbin:/sbin', 'HOME':str(S/'home'),
       'TMPDIR':str(S/'tmp'), 'PYTHONDONTWRITEBYTECODE':'1'}
results = []

def run(check, args, expected=0):
    start = time.time()
    log = E/(check+'.log')
    with log.open('w') as f:
        f.write(f'Check: {check}\nCommand: {args!r}\nCommit: {commit}\nEnvironment: Darwin arm64, private HOME/TMP, Python3.9.6/Bash3.2; command doubles only\nDate: 2026-10-19\n\n'); f.flush()
        result = subprocess.run(args, cwd=source, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=900)
        f.write(f'\nObserved exit: {result.returncode}; expected exit: {expected}\n')
    results.append({'check':check, 'command':args, 'commit':commit, 'exit':result.returncode,
                    'expected':expected, 'passed':result.returncode == expected,
                    'seconds':round(time.time()-start, 2), 'log':log.name})
    print(results[-1], flush=True)
    (E/'IMP-07-results.json').write_text(json.dumps({'check':'IMP-07', 'command':'IMP-07-run-checks.py',
        'commit':commit, 'environment':'Darwin arm64 independent copy, private HOME/TMP', 'date':'2026-10-19',
        'checks':results}, indent=2)+'\n')

try:
    if not os.environ.get('SKIP_FOCUSED'):run('IMP-07-04-focused', ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing','scripts.tests.test_nfs_release_workflow','-v'])
    if os.environ.get('FOCUSED_ONLY'):
        assert all(x['passed'] for x in results)
    else:
        run('IMP-07-05-python', ['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
        run('IMP-07-06-syntax', ['/bin/bash','-n','packaging/sign-macos.sh'])
        run('IMP-07-07-shellcheck', ['/opt/homebrew/bin/shellcheck','packaging/sign-macos.sh'])
        run('IMP-07-08-actionlint', ['/opt/homebrew/bin/actionlint','.github/workflows/release-nfs.yml'])
        run('IMP-07-09-source-hash', ['/usr/bin/python3','packaging/release.py','--source-hash'])
        run('IMP-07-10-recipe-hash', ['/usr/bin/python3','-c','import sys;sys.path.insert(0,"packaging/engine");import source;print(source.recipe_hash())'])
        run('IMP-07-11-no-candidate-refusal', ['/usr/bin/python3','packaging/release.py','--check-publish'], 1)
        sign = source/'packaging/sign-macos.sh'; original = sign.read_text()
        controls = [
            ('omit-owned-membership', "sys.argv[2], *prior]", "*prior]", 'test_temporary_keychain_preserves_existing_search_entries_and_order'),
            ('replace-original-list', "sys.argv[2], *prior]", "sys.argv[2]]", 'test_temporary_keychain_preserves_existing_search_entries_and_order'),
            ('swallow-configuration-failure', 'PYLIST\n', 'PYLIST\n', None),
            ('skip-restore', 'if [[ -f "$scratch/search.json" ]]; then', 'if false; then', 'test_temporary_keychain_preserves_existing_search_entries_and_order'),
        ]
        for name, old, new, test in controls:
            if test is None:
                old = 'python3 - "$scratch/search.json" "$keychain" <<\'PYLIST\''
                new = old+' || true'
                test = 'test_search_list_configuration_failure_stops_before_signing'
            assert original.count(old) == 1, old
            sign.write_text(original.replace(old, new, 1))
            run('IMP-07-12-mutant-'+name, ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing.SigningTest.'+test,'-v'], 1)
            sign.write_text(original)
        # Original signer with new fixture fails lookup because it omits membership.
        sign.write_bytes(subprocess.check_output(['git','show','79e35392bfe4f795464fecd8c034670b622c1684:packaging/sign-macos.sh'],cwd=R))
        run('IMP-07-13-original-control', ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing.SigningTest.test_temporary_keychain_preserves_existing_search_entries_and_order','-v'], 1)
        run('IMP-07-14-original-hash', ['/usr/bin/python3','packaging/release.py','--source-hash'])
        sign.write_text(original)
        assert all((source/p).read_bytes() == (R/p).read_bytes() for p in paths)
        digest = hashlib.sha256()
        for p in sorted(paths):digest.update(p.encode()+b'\0'+(source/p).read_bytes())
        (E/'IMP-07-15-copy.json').write_text(json.dumps({'check':'IMP-07-15', 'command':'compare independent copy bytes to worktree; SHA256 ordered path/NUL/bytes',
            'commit':commit, 'environment':'Darwin arm64', 'date':'2026-10-19', 'fileCount':len(paths),
            'allCopiedInputsStillMatch':True, 'aggregateSha256':digest.hexdigest()}, indent=2)+'\n')
        assert all(x['passed'] for x in results)
finally:
    shutil.rmtree(S)
    (E/'IMP-07-16-cleanup.json').write_text(json.dumps({'check':'IMP-07-16', 'command':'remove owned independent source/HOME/TMP',
        'commit':commit, 'environment':'Darwin arm64', 'date':'2026-10-19', 'scratch':str(S), 'absent':not S.exists(),
        'realKeychainOrAppleAccess':False, 'retainedCandidatesTouched':False, 'remoteActions':False}, indent=2)+'\n')
