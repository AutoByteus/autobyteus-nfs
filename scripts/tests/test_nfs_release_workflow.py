"""Nonpublishing NFS workflow regression (stdlib only; no secrets/network/jobs).
Run: python3 -m unittest scripts/tests/test_nfs_release_workflow.py -v.
Reads the workflow's actual single-line job needs/if fields and evaluates only
its boolean-expression subset. Models GitHub's transitive default-success rule;
not a hosted Actions runner or release qualification. Native metadata tests also
execute the actual workflow prefix under /bin/bash (Mac system Bash3.2 included),
doubling only the release.py OCI/metadata boundary, never signing or building.
Contracts: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idneeds
https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions
"""
import ast
import json
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[2] / '.github/workflows/release-nfs.yml'
ORDER = ['prepare', 'engine-packages', 'engine-inputs', 'engine', 'binaries', 'candidate', 'payload', 'publish']


def job_gates(text):
    # Deliberately narrow fixture reader, not a general YAML parser. New shapes
    # fail explicitly; workflow grammar is separately checked with actionlint.
    blocks = re.findall(r'^  ([a-z-]+):\n(.*?)(?=^  [a-z-]+:|\Z)',
                        text.split('\njobs:\n', 1)[1], re.M | re.S)
    assert [name for name, _ in blocks] == ORDER
    jobs = {}
    for name, body in blocks:
        needs = re.findall(r'^    needs: (.+)$', body, re.M)
        condition = re.findall(r'^    if: (.+)$', body, re.M)
        assert len(needs) <= 1 and len(condition) <= 1
        deps = needs[0].strip('[]').split(', ') if needs else []
        assert all(dep in jobs for dep in deps), (name, deps)
        expr = condition[0] if condition else 'success()'
        if expr.startswith('${{ '):
            assert expr.endswith(' }}')
            expr = expr[4:-3]
        jobs[name] = {'needs': deps, 'if': expr}
    return jobs


def boolean(node):
    if isinstance(node, ast.Constant):
        assert isinstance(node.value, (str, bool))
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not boolean(node.operand)
    if isinstance(node, ast.BoolOp):
        values = [boolean(n) for n in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        if isinstance(node.op, ast.Or):
            return any(values)
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        left, right = boolean(node.left), boolean(node.comparators[0])
        if isinstance(node.ops[0], ast.Eq):
            return left == right
        if isinstance(node.ops[0], ast.NotEq):
            return left != right
    raise AssertionError(f'Unsupported gate expression: {ast.dump(node)}')


def eligible(jobs, name, results, mode, cancelled=False):
    deps = set(jobs[name]['needs'])
    pending = list(deps)
    while pending:
        for dep in jobs[pending.pop()]['needs']:
            if dep not in deps:
                deps.add(dep)
                pending.append(dep)
    success = not cancelled and all(results[d] == 'success' for d in deps)
    expr = jobs[name]['if']
    if not re.search(r'\b(always|success|failure|cancelled)\(\)', expr):
        if not success:  # Ordinary booleans still inherit implicit success().
            return False
    expr = expr.replace('needs.prepare.outputs.mode', repr(mode))
    def result(match):
        assert match[1] in jobs[name]['needs'], match[1]
        return repr(results[match[1]])
    expr = re.sub(r'needs\.([a-z-]+)\.result', result, expr)
    for fn, value in [('always', True), ('cancelled', cancelled), ('success', success),
                      ('failure', any(results[d] == 'failure' for d in deps))]:
        expr = expr.replace(fn + '()', str(value))
    expr = re.sub(r'!(?!=)', ' not ', expr).replace('&&', ' and ').replace('||', ' or ')
    return boolean(ast.parse(expr.strip(), mode='eval').body)


def schedule(jobs, mode, failures=None):
    results = {}
    for name in ORDER:
        results[name] = ((failures or {}).get(name, 'success')
                         if eligible(jobs, name, results, mode) else 'skipped')
    return results


class ReleaseWorkflowGatesTest(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text()
        self.jobs = job_gates(self.text)

    def test_manual_only_and_permissions(self):
        trigger=self.text.split('on:\n',1)[1].split('permissions:',1)[0]
        self.assertIn('workflow_dispatch:',trigger)
        self.assertIn('default: false',trigger)
        self.assertNotIn('  push:',trigger)
        self.assertNotIn('pull_request',self.text)
        self.assertNotIn('--clobber',self.text)
        self.assertNotIn('push: true',self.text)
        self.assertIn('cancel-in-progress: false',self.text)
        self.assertEqual(self.text.count('fail-fast: false'),2)
        for action in re.findall(r'uses: (.+)',self.text):
            self.assertRegex(action,r'^[a-z-]+/[a-z-]+@[a-f0-9]{40}$')
        self.assertEqual(self.text.count('contents: write'),1)
        self.assertEqual(self.text.count('packages: write'),1)
        self.assertNotIn('contents: write',self.text.split('  publish:')[0])
        self.assertIn("if: matrix.os == 'darwin' && needs.prepare.outputs.mode == 'fresh'",self.text)
        self.assertIn('retention-days: 90',self.text)
        self.assertIn('path: retained/',self.text)

    def test_all_modes(self):
        self.assertEqual(schedule(self.jobs,'candidate'),dict(zip(ORDER,
            ['success','success','success','success','success','success','skipped','skipped'])))
        self.assertEqual(schedule(self.jobs,'fresh'),dict(zip(ORDER,
            ['success','skipped','skipped','skipped','success','skipped','success','success'])))
        self.assertEqual(schedule(self.jobs,'resume'),dict(zip(ORDER,
            ['success','skipped','skipped','skipped','skipped','skipped','skipped','success'])))
        # Resume must not rebuild/re-sign; prepare resolves exact retained payload.
        self.assertIn('--operation prepare',self.text)
        self.assertIn('--operation bind',self.text)
        self.assertIn('--operation publish',self.text)

    def test_failure_cancellation_and_unexpected_skip_never_publish(self):
        for mode in ('candidate','fresh','resume'):
            baseline=schedule(self.jobs,mode)
            terminal='candidate' if mode=='candidate' else 'publish'
            for name in ORDER:
                if baseline[name]!='success' or name==terminal:continue
                for state in ('failure','cancelled','skipped'):
                    with self.subTest(mode=mode,job=name,state=state):
                        results=schedule(self.jobs,mode,{name:state})
                        self.assertEqual(results[terminal],'skipped')
            for name in ORDER:
                self.assertFalse(eligible(self.jobs,name,baseline,mode,cancelled=True))

    def test_legitimate_skips_do_not_accept_failures(self):
        for mode in ('fresh','resume'):
            results=schedule(self.jobs,mode)
            for name in ('binaries','publish'):
                for dep in self.jobs[name]['needs']:
                    for state in ('failure','cancelled'):
                        self.assertFalse(eligible(self.jobs,name,dict(results,**{dep:state}),mode))


class NativeMetadataShellTest(unittest.TestCase):
    def setUp(self):
        # Narrow literal-block reader, not a second YAML parser. Include the real
        # strict-mode and OCI pipeline lines; stop before any native build/tests.
        block = WORKFLOW.read_text().split(
            '      - name: Native checks and exact engine metadata (not physical qualification)\n', 1)[1]
        block = block.split('        run: |\n', 1)[1].split('          go test -race ./...\n', 1)[0]
        self.prefix = textwrap.dedent(block)
        self.assertIn('python3 packaging/release.py', self.prefix)

    def run_prefix(self, mode, target='darwin-arm64', metadata_exit=0, oci_exit=0):
        with tempfile.TemporaryDirectory(prefix='nfs-native-shell-') as scratch:
            root = Path(scratch)
            recorder = root / 'release-boundary.py'
            recorder.write_text('''import json, os, sys
from pathlib import Path
args = sys.argv[1:]
if args == ['packaging/release.py', '--operation', 'oci', '--directory', 'work/candidate/engine.oci.tar']:
    print(json.dumps({'index': 'sha256:' + 'a' * 64}))
    sys.exit(int(os.environ['OCI_EXIT']))
Path(os.environ['ARGV_RECORD']).write_text(json.dumps(args))
sys.exit(int(os.environ['METADATA_EXIT']))
''')
            # Use the real stdlib interpreter for the workflow's JSON pipeline;
            # intercept only the packaging facade to avoid engine/metadata writes.
            script = '''python3() {
  if [[ "$1" == packaging/release.py ]]; then
    "$TEST_PYTHON" "$RECORDER" "$@"
  else
    "$TEST_PYTHON" "$@"
  fi
}
''' + self.prefix + "printf 'CONTINUED\\n'\n"
            env = {'PATH': '/usr/bin:/bin', 'HOME': scratch, 'TMPDIR': scratch,
                   'PYTHONDONTWRITEBYTECODE': '1', 'TEST_PYTHON': sys.executable,
                   'RECORDER': str(recorder), 'ARGV_RECORD': str(root / 'argv.json'),
                   'MODE': mode, 'TAG': 'v0.1.0', 'METADATA_EXIT': str(metadata_exit),
                   'OCI_EXIT': str(oci_exit)}
            if target is not None:
                env['TARGET'] = target
            result = subprocess.run(['/bin/bash', '-e', '-c', script], cwd=root,
                                    env=env, capture_output=True, text=True, timeout=30)
            args = json.loads((root / 'argv.json').read_text()) if (root / 'argv.json').exists() else None
            return result, args

    def test_candidate_and_fresh_metadata_argv(self):
        # TARGET values exercise argument construction, not four native CPUs.
        for target in ('darwin-arm64', 'darwin-amd64', 'linux-arm64', 'linux-amd64'):
            for mode in ('candidate', 'fresh'):
                with self.subTest(target=target, mode=mode):
                    result, args = self.run_prefix(mode, target)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    expected = ['packaging/release.py', '--tag', 'v0.1.0', '--engine-image',
                                'ghcr.io/autobyteus/autobyteus-nfs@sha256:' + 'a' * 64,
                                '--engine-manifest', 'work/candidate/engine/engine-manifest.json',
                                '--engine-artifacts', 'work/candidate/engine', '--target', target,
                                '--output', 'cmd/autobyteus-nfs/release.json']
                    if mode == 'fresh':
                        expected += ['--qualified', '--candidate', 'work/candidate']
                    self.assertEqual(args, expected)
                    self.assertEqual(result.stdout, 'CONTINUED\n')

    def test_metadata_failure_stops_step(self):
        for mode in ('candidate', 'fresh'):
            with self.subTest(mode=mode):
                result, args = self.run_prefix(mode, metadata_exit=17)
                self.assertIsNotNone(args)
                self.assertEqual(result.returncode, 17, result.stderr)
                self.assertNotIn('CONTINUED', result.stdout)

    def test_nounset_and_oci_pipefail_stop_before_metadata(self):
        for options in ({'target': None}, {'oci_exit': 23}):
            with self.subTest(options=options):
                result, args = self.run_prefix('candidate', **options)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(args)
                self.assertNotIn('CONTINUED', result.stdout)

if __name__ == '__main__':unittest.main()
