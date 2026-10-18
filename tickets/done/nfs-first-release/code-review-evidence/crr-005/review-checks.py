"""CRR005: independently check only the requested two-import correction."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

E = Path(__file__).resolve().parent
R = E.parents[4]
A = json.loads((E / 'input-audit.json').read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=R).decode()


def write(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')


changes = {
    'packaging/engine/manifest.py': ('source', 'LOCK'),
    'scripts/tests/nfs_release_fixture.py': ('release_support', 'readiness'),
}
prior = A['prior_source']
delta = git('diff', prior, A['source_commit'], '--', ':!tickets')
(E / 'source.diff').write_text(delta)
changed = git('diff', '--name-only', prior, A['source_commit'], '--', ':!tickets').splitlines()
assert set(changed) == set(changes), changed
ast_results = []
for path, (module, binding) in changes.items():
    old_text = git('show', prior + ':' + path)
    old = ast.parse(old_text)
    new_text = (R / path).read_text()
    new = ast.parse(new_text)
    removed = []
    for node in ast.walk(old):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            removed.extend(a.name for a in node.names if a.name == binding)
            node.names = [a for a in node.names if a.name != binding]
    assert removed == [binding]
    assert ast.dump(old) == ast.dump(new), path
    ast_results.append({'path': path, 'removed_binding': binding,
                        'other_ast_identical': True,
                        'prior_nonempty': sum(bool(x.strip()) for x in old_text.splitlines()),
                        'current_nonempty': sum(bool(x.strip()) for x in new_text.splitlines())})
same = []
for path in A['source_inputs']:
    if path not in changes:
        data = subprocess.check_output(['git', 'show', prior + ':' + path], cwd=R)
        assert data == (R / path).read_bytes(), path
        same.append(path)
assert len(same) == 118
py_paths = [p for p in git('diff', '--name-only', '8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34', prior,
                           '--', ':!tickets').splitlines() if p.endswith('.py') and (R / p).exists()]
imports = []
for path in py_paths:
    tree = ast.parse((R / path).read_text())
    loaded = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    unused = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if getattr(node, 'module', None) == '__future__':
                    continue
                local = alias.asname or (alias.name.split('.')[0] if isinstance(node, ast.Import) else alias.name)
                if local not in loaded:
                    unused.append({'line': node.lineno, 'binding': local})
    imports.append({'path': path, 'unused_local_bindings': unused})
assert len(py_paths) == 16
assert not any(row['unused_local_bindings'] for row in imports)
write('source-audit.json', {'changed_paths': changed, 'other_source_inputs_unchanged': len(same),
                          'ast_delta': ast_results, 'import_scan': imports,
                          'scan_limit': 'AST local Name-load audit, not a compiler or public-export proof; direct caller trace separately reviewed.'})
prior_audit = json.loads((E.parent / 'crr-004/input-audit.json').read_text())
authorities = ['requirements-doc.md', 'design-spec.md', 'approval-record-sr004.md',
               'postpublication-testing-plan.md', 'design-review-report.md',
               'architecture-review-revision-record.md', 'investigation-notes.md', 'solution-revision-record.md']
authority_records = {}
for name in authorities:
    path = 'tickets/in-progress/nfs-first-release/' + name
    assert sha(R / path) == prior_audit['protected_ticket_inputs'][path], name
    authority_records[path] = sha(R / path)
write('carry-validity.json', {'unchanged_authorities': authority_records,
                           'unchanged_source_paths': same,
                           'prior_review': 'CRR004 Full Re-Audit; independent Go/actionlint/shell evidence carries, not newly executed.',
                           'new_engine_candidate_required': True})

scratch = Path(tempfile.mkdtemp(prefix='nfs-release-crr005-', dir='/Users/normy'))
(E / 'scratch-path.txt').write_text(str(scratch) + '\n')
repo = scratch / 'source'
rows = []
env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': str(scratch / 'home'),
       'TMPDIR': str(scratch / 'tmp'), 'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C'}
try:
    for name in ('home', 'tmp'):
        (scratch / name).mkdir()
    for path, digest in A['source_inputs'].items():
        dest = repo / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(R / path, dest)
        assert sha(dest) == digest

    def run(name, args, expected=0, required=None):
        start = time.monotonic()
        result = subprocess.run(args, cwd=repo, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=240)
        (E / (name + '.log')).write_bytes(result.stdout)
        row = {'name': name, 'argv': args, 'cwd': str(repo), 'exit_code': result.returncode,
               'expected_exit': expected, 'seconds': round(time.monotonic() - start, 3)}
        rows.append(row)
        write('checks-result.json', {'commands': rows, 'environment': env})
        assert result.returncode == expected, row
        if required is not None:
            assert required.encode() in result.stdout, row
        return result.stdout.decode()

    run('python-version', ['/usr/bin/python3', '--version'], required='Python 3.9.6')
    run('shell-version', ['/bin/bash', '--version'], required='3.2.57')
    run('python-all', ['/usr/bin/python3', '-m', 'unittest', 'discover', '-s', 'scripts/tests',
                       '-p', 'test_nfs_*.py', '-v'], required='Ran 45 tests')
    output = (E / 'python-all.log').read_text()
    assert 'OK (skipped=1)' in output
    run('source-hash', ['/usr/bin/python3', 'packaging/release.py', '--source-hash'],
        required='c7fd64e87b62509165d8655cc576fba9261867a306f13a93ad420776304e4a60')
    run('recipe-hash', ['/usr/bin/python3', '-c',
        "import sys;sys.path.insert(0,'packaging/engine');import source;print(source.recipe_hash())"],
        required='299db7012dcc543f8606632695d286548d1513c13ace8b108eb712984fd39274')
    run('readiness-refusal', ['/usr/bin/python3', 'packaging/release.py', '--check-publish'], 1,
        'Current engine and structured release readiness required')
    assert all(sha(repo / p) == v and sha(R / p) == v for p, v in A['source_inputs'].items())
    write('source-integrity.json', {'copied_source_inputs': 120, 'copy_and_original_unchanged': True})
    print(json.dumps({'commands': len(rows), 'all_expected': True, 'python_collected': 45,
                      'python_executed': 44, 'python_skipped': 1, 'ast_delta': ast_results}, indent=2))
finally:
    processes = subprocess.check_output(['ps', '-axo', 'pid=,stat=,command=']).decode()
    matches = [line for line in processes.splitlines() if str(scratch) in line]
    assert not matches, matches
    shutil.rmtree(scratch)
    write('cleanup.json', {'scratch': str(scratch), 'removed': not scratch.exists(),
                          'matching_processes_before_removal': matches,
                          'owned_external_resources': [], 'other_owners_touched': False})
