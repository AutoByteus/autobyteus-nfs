"""IMP-06: independent local signing-diagnostic checks, no real signing or remote effects.
Command: python3 tickets/done/nfs-first-release/evidence/IMP-06-run-checks.py
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
S = Path(tempfile.mkdtemp(prefix='nfs-release-ir006-', dir='/Users/normy/autobyteus_org'))
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
        result = subprocess.run(args, cwd=source, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=300)
        f.write(f'\nObserved exit: {result.returncode}; expected exit: {expected}\n')
    results.append({'check':check, 'command':args, 'commit':commit, 'exit':result.returncode,
                    'expected':expected, 'passed':result.returncode == expected,
                    'seconds':round(time.time()-start, 2), 'log':log.name})
    print(results[-1], flush=True)
    (E/'IMP-06-results.json').write_text(json.dumps({'check':'IMP-06', 'command':'IMP-06-run-checks.py',
        'commit':commit, 'environment':'Darwin arm64 independent copy, private HOME/TMP', 'date':'2026-10-19',
        'checks':results}, indent=2)+'\n')

try:
    if not os.environ.get('SKIP_FOCUSED'):run('IMP-06-01-focused', ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing','scripts.tests.test_nfs_release_workflow','-v'])
    if os.environ.get('FOCUSED_ONLY'):
        assert all(x['passed'] for x in results)
    else:
        run('IMP-06-02-python', ['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'])
        run('IMP-06-03-syntax', ['/bin/bash','-n','packaging/sign-macos.sh'])
        run('IMP-06-04-shellcheck', ['/opt/homebrew/bin/shellcheck','packaging/sign-macos.sh'])
        run('IMP-06-05-actionlint', ['/opt/homebrew/bin/actionlint','.github/workflows/release-nfs.yml'])
        run('IMP-06-06-source-hash', ['/usr/bin/python3','packaging/release.py','--source-hash'])
        run('IMP-06-07-recipe-hash', ['/usr/bin/python3','-c','import sys;sys.path.insert(0,"packaging/engine");import source;print(source.recipe_hash())'])
        run('IMP-06-08-no-candidate-refusal', ['/usr/bin/python3','packaging/release.py','--check-publish'], 1)
        sign = source/'packaging/sign-macos.sh'; original = sign.read_text()
        controls = [
            ('classify-all-unknown', 'print(result)', "print('unclassified')", 'test_codesign_diagnostics_are_allowlisted_not_private_output'),
            ('leak-private-output', 'print(result)', "print(data.decode('utf-8'))", 'test_codesign_diagnostics_are_allowlisted_not_private_output'),
            ('hide-signing-exit', 'exit "$sign_exit"', 'exit 42', 'test_codesign_diagnostics_are_allowlisted_not_private_output'),
            ('ignore-read-bound', 'if len(data) > 65536:', 'if False:', 'test_codesign_capture_bound_and_decode_failure_preserve_exit'),
        ]
        for name, old, new, test in controls:
            assert original.count(old) == 1, old
            sign.write_text(original.replace(old, new, 1))
            run('IMP-06-09-mutant-'+name, ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing.SigningTest.'+test,'-v'], 1)
            sign.write_text(original)
        # Old production with new test: original exits5, but supplies no diagnostic.
        sign.write_bytes(subprocess.check_output(['git','show','b279d556e2c0f5e90ca24b61c7e67bc809644947:packaging/sign-macos.sh'],cwd=R))
        run('IMP-06-10-original-control', ['/usr/bin/python3','-m','unittest','scripts.tests.test_nfs_release_signing.SigningTest.test_command_failures_report_exact_stage_and_exit','-v'], 1)
        run('IMP-06-11-original-hash', ['/usr/bin/python3','packaging/release.py','--source-hash'])
        sign.write_text(original)
        assert all((source/p).read_bytes() == (R/p).read_bytes() for p in paths)
        digest = hashlib.sha256()
        for p in sorted(paths):digest.update(p.encode()+b'\0'+(source/p).read_bytes())
        (E/'IMP-06-12-copy.json').write_text(json.dumps({'check':'IMP-06-12', 'command':'compare independent copy bytes to worktree; SHA256 ordered path/NUL/bytes',
            'commit':commit, 'environment':'Darwin arm64', 'date':'2026-10-19', 'fileCount':len(paths),
            'allCopiedInputsStillMatch':True, 'aggregateSha256':digest.hexdigest()}, indent=2)+'\n')
        assert all(x['passed'] for x in results)
finally:
    shutil.rmtree(S)
    (E/'IMP-06-13-cleanup.json').write_text(json.dumps({'check':'IMP-06-13', 'command':'remove owned independent source/HOME/TMP',
        'commit':commit, 'environment':'Darwin arm64', 'date':'2026-10-19', 'scratch':str(S), 'absent':not S.exists(),
        'realKeychainOrAppleAccess':False, 'retainedCandidatesTouched':False, 'remoteActions':False}, indent=2)+'\n')
