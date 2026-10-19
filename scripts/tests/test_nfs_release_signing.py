"""Real signing shell with command doubles; no Apple calls or real credentials."""
import base64
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FAKE = r'''#!/usr/bin/env python3
import json,os,shlex,signal,stat,sys
from pathlib import Path
name=Path(sys.argv[0]).name;args=sys.argv[1:]
operation=name+':'+args[0]
prior=json.loads(os.environ['ORIGINAL_SEARCH'])
state=Path(os.environ['SEARCH_STATE'])
if operation=='security:list-keychains' and '-s' in args:
 selected=args[args.index('-s')+1:]
 operation+=':restore' if selected==prior else ':configure'
 if operation.endswith(':configure'):
  assert selected[1:]==prior, 'prior keychains/order must survive configuration'
  assert Path(selected[0]).is_file() and selected[0].startswith(os.environ['RUNNER_TEMP']+'/')
with open(os.environ['CALLS'],'a') as f:f.write(operation+'\n')
if operation=='codesign:--force' and os.environ.get('SIGN_OUTPUT'):
 # Verify private capture on the changed path. No real keychain or Apple process.
 assert stat.S_IMODE(os.fstat(2).st_mode)==0o600
 output=os.environ['SIGN_OUTPUT'].replace('{binary}',args[-1]).replace('{identity}',os.environ['IDENTITY'])
 if os.environ.get('INVALID_SIGN_BYTES'):sys.stderr.buffer.write(b'\xff')
 print(output*int(os.environ.get('SIGN_REPEAT','1')),file=sys.stderr)
if operation==os.environ.get('SIGNAL_AT'):os.kill(os.getppid(),signal.SIGTERM)
if operation in os.environ.get('FAIL','').split(','):
 for stream in (sys.stdout,sys.stderr):
  print('PRIVATE-COMMAND-OUTPUT fake-export-password ZmFrZSBwMTI= fake-app-password fake-keychain-password',file=stream)
 sys.exit(5)
if name=='security':
 if args[0]=='list-keychains':
  if '-s' in args:state.write_text(json.dumps(selected))
  else:print(' '.join(shlex.quote(p) for p in json.loads(state.read_text())))
 if args[0]=='create-keychain':Path(args[-1]).touch()
 if args[0]=='delete-keychain':Path(args[-1]).unlink()
 if args[0]=='find-identity' and not os.environ.get('NO_IDENTITY'):print('1) ABC "'+os.environ['IDENTITY']+'"')
if operation=='codesign:--force':
 # Reproduce the real empty/new-keychain lookup contract, not a text-only check.
 assert args[args.index('--keychain')+1] in json.loads(state.read_text()), 'owned keychain absent from search list'
 assert '--timestamp' in args and args[args.index('--options')+1]=='runtime'
if name=='codesign' and args[0]=='-d':
 print('TeamIdentifier='+os.environ['APPLE_TEAM_ID'],file=sys.stderr)
 print('Authority='+os.environ['IDENTITY'],file=sys.stderr)
 if not os.environ.get('NO_RUNTIME'):print('CodeDirectory flags=0x10000(runtime)',file=sys.stderr)
 print('Timestamp=Oct 18, 2026',file=sys.stderr)
if name=='xcrun':
 if os.environ.get('BAD_NOTARY_JSON'):print('PRIVATE-COMMAND-OUTPUT not JSON')
 else:print(json.dumps({'status':os.environ.get('NOTARY','Accepted'),'id':'12345678-1234-1234-1234-123456789abc'}))
 sys.exit(int(os.environ.get('NOTARY_EXIT','0')))
if name=='ditto':Path(args[-1]).write_bytes(b'carrier')
if name=='openssl':print('fake-keychain-password')
'''


class SigningTest(unittest.TestCase):
    def run_case(self, stage=None, code=1, cleanup='complete', notary_receipt=False, existing_failure=False, diagnostic=None, **changes):
        with tempfile.TemporaryDirectory(prefix='nfs-sign-fixture-') as temp:
            root = Path(temp); bin_dir = root/'bin'; bin_dir.mkdir()
            scratch = root/'scratch'; scratch.mkdir()
            for name in ('security', 'codesign', 'xcrun', 'ditto', 'openssl'):
                path = bin_dir/name; path.write_text(FAKE); path.chmod(0o755)
            if changes.get('PARSER_FAILURE'):
                # Only the diagnostics parser fails, not signing or earlier Python checks.
                wrapper = bin_dir/'python3'
                wrapper.write_text('#!/bin/bash\nif [[ "${2:-}" == */sign.txt ]]; then\n'
                                   ' echo PRIVATE-COMMAND-OUTPUT >&2; exit 42\nfi\n'
                                   'exec /usr/bin/python3 "$@"\n')
                wrapper.chmod(0o755)
            binary = root/'binary'; binary.write_bytes(b'fake unsigned CLI')
            calls = root/'calls'; receipt = root/'receipt.json'
            original_search = ['/owned/original.keychain-db', "/owned/a space and 'quote;$.keychain-db"]
            search_state = root/'search-state.json'; search_state.write_text(json.dumps(original_search))
            failure = root/'receipt-failure.json'
            if existing_failure:failure.write_text('owned prior receipt')
            env = os.environ | {'PATH':str(bin_dir)+':'+os.environ['PATH'],
                'RUNNER_TEMP':str(scratch), 'CERTIFICATE':base64.b64encode(b'fake p12').decode(),
                'PASSWORD':'fake-export-password', 'IDENTITY':'Developer ID Application: Fixture (ABCDEFG123)',
                'APPLE_TEAM_ID':'ABCDEFG123', 'APPLE_ID':'fixture@example.invalid',
                'APPLE_APP_SPECIFIC_PASSWORD':'fake-app-password', 'CALLS':str(calls),
                'ORIGINAL_SEARCH':json.dumps(original_search), 'SEARCH_STATE':str(search_state),
                'FAIL':'', 'NOTARY':'Accepted', 'NOTARY_EXIT':'0', 'SIGNAL_AT':'',
                'NO_IDENTITY':'', 'NO_RUNTIME':'', 'BAD_NOTARY_JSON':'',
                'SIGN_OUTPUT':'', 'SIGN_REPEAT':'1', 'INVALID_SIGN_BYTES':''} | changes
            result = subprocess.run(['/bin/bash', str(ROOT/'packaging/sign-macos.sh'),
                                     str(binary), str(receipt)], env=env, text=True,
                                    capture_output=True, timeout=30)
            self.assertEqual(result.returncode, code if stage else 0, result.stdout+result.stderr)
            self.assertEqual(list(scratch.iterdir()), [], 'signing scratch/keychain leaked')
            if cleanup == 'complete':
                self.assertEqual(json.loads(search_state.read_text()), original_search, 'prior search list changed')
            self.assertEqual(receipt.exists(), not stage or notary_receipt)
            self.assertEqual(failure.exists(), stage is not None, result.stdout+result.stderr)
            if stage and diagnostic:
                self.assertIn('diagnostic='+diagnostic, result.stderr)
            if existing_failure:
                self.assertEqual(failure.read_text(), 'owned prior receipt')
                self.assertIn('Signing failure receipt unavailable (not overwritten)', result.stderr)
            elif stage:
                record = json.loads(failure.read_text())
                self.assertEqual(record, {'schema':1, 'status':'Failed', 'stage':stage,
                                             'exitCode':code, 'cleanup':cleanup,
                                             'diagnostic':diagnostic or ('unclassified' if stage == 'sign' and code != 143 else 'not-collected')})
                self.assertIn('Signing failed: stage='+stage+' exit='+str(code)+' cleanup='+cleanup,
                              result.stderr)
            else:
                self.assertEqual(json.loads(receipt.read_text())['status'], 'Accepted')
            public = result.stdout+result.stderr+(''.join(p.read_text() for p in (failure,receipt) if p.exists()))
            for secret in ('fake-export-password', 'fake-app-password', 'fake-keychain-password',
                           base64.b64encode(b'fake p12').decode(), 'PRIVATE-COMMAND-OUTPUT',
                           'fixture@example.invalid', 'Developer ID Application: Fixture'):
                self.assertNotIn(secret, public)
            self.assertNotIn(str(scratch), public)
            trace = calls.read_text().splitlines() if calls.exists() else []
            if 'security:create-keychain' in trace and env['FAIL'] != 'security:create-keychain':
                self.assertIn('security:delete-keychain', trace)
            if env['FAIL'] == 'security:list-keychains':
                self.assertNotIn('security:list-keychains:restore', trace)
            elif 'security:list-keychains' in trace:
                self.assertIn('security:list-keychains:restore', trace)
            if stage and stage not in ('notary-submit', 'notary-receipt', 'notary-accepted', 'cleanup'):
                self.assertNotIn('xcrun:notarytool', trace)
            return trace

    def test_accepted_and_sanitized_receipt(self):
        self.run_case()

    def test_temporary_keychain_preserves_existing_search_entries_and_order(self):
        trace = self.run_case()
        self.assertLess(trace.index('security:list-keychains:configure'), trace.index('security:find-identity'))
        self.assertLess(trace.index('security:list-keychains:configure'), trace.index('codesign:--force'))
        self.assertGreater(trace.index('security:list-keychains:restore'), trace.index('codesign:--force'))

    def test_search_list_configuration_failure_stops_before_signing(self):
        trace = self.run_case('configure-search-list', 5, FAIL='security:list-keychains:configure')
        self.assertNotIn('codesign:--force', trace)
        self.assertNotIn('security:find-identity', trace)

    def test_import_failure_receipt_and_secret_safety(self):
        self.run_case('import-certificate', 5, FAIL='security:import')

    def test_command_failures_report_exact_stage_and_exit(self):
        stages = {'security:list-keychains':'read-search-list', 'openssl:rand':'keychain-password',
                  'security:create-keychain':'create-keychain', 'security:unlock-keychain':'unlock-keychain',
                  'security:set-key-partition-list':'partition-key', 'security:find-identity':'find-identity',
                  'codesign:--force':'sign', 'codesign:--verify':'verify-signature',
                  'codesign:-d':'inspect-signature', 'ditto:-c':'notary-archive',
                  'xcrun:notarytool':'notary-submit'}
        for command, stage in stages.items():
            with self.subTest(command=command):self.run_case(stage, 5, FAIL=command)

    def test_codesign_diagnostics_are_allowlisted_not_private_output(self):
        cases = {
            '{identity}: no identity found': 'identity-not-found',
            'prefix {identity}: no identity found suffix': 'unclassified',
            '{binary}: errSecInternalComponent': 'internal-component',
            '{binary}: User interaction is not allowed.': 'interaction-not-allowed',
            '{binary}: The user name or passphrase you entered is not correct.': 'authentication-failed',
            '{binary}: The specified item could not be found in the keychain.': 'keychain-item-not-found',
            '{binary}: An expired certificate was detected.': 'certificate-expired',
            '{binary}: The certificate was revoked.': 'certificate-revoked',
            '{binary}: The timestamp service is not available.': 'timestamp-unavailable',
            'Warning: unable to build chain to self-signed root for signer "{identity}"\n{binary}: errSecInternalComponent': 'chain-build-warning',
            'Warning: unable to build chain to self-signed root for signer "(null)"': 'chain-build-warning',
            'PRIVATE-COMMAND-OUTPUT fake-app-password': 'unclassified',
            'prefix {binary}: errSecInternalComponent suffix': 'unclassified',
            '{binary}: errSecInternalComponent\n{binary}: User interaction is not allowed.': 'unclassified',
        }
        for output, expected in cases.items():
            with self.subTest(diagnostic=expected, output=output):
                self.run_case('sign', 5, diagnostic=expected, FAIL='codesign:--force', SIGN_OUTPUT=output)

    def test_codesign_capture_bound_and_decode_failure_preserve_exit(self):
        self.run_case('sign', 5, diagnostic='output-too-large', FAIL='codesign:--force',
                      SIGN_OUTPUT='x'*1024, SIGN_REPEAT='65')
        self.run_case('sign', 5, diagnostic='unavailable', FAIL='codesign:--force',
                      SIGN_OUTPUT='PRIVATE-COMMAND-OUTPUT', INVALID_SIGN_BYTES='1')

    def test_codesign_parser_failure_does_not_hide_signing_exit(self):
        self.run_case('sign', 5, diagnostic='unavailable', FAIL='codesign:--force', PARSER_FAILURE='1')

    def test_codesign_success_does_not_turn_warning_into_failure(self):
        self.run_case(SIGN_OUTPUT='{binary}: errSecInternalComponent')

    def test_validation_failures_are_not_credential_dumps(self):
        self.run_case('decode-certificate', CERTIFICATE='not base64!')
        self.run_case('validate-identity', IDENTITY='Not a Developer ID')
        self.run_case('validate-identity-available', NO_IDENTITY='1')
        self.run_case('validate-signature', NO_RUNTIME='1')
        self.run_case('notary-receipt', BAD_NOTARY_JSON='1')
        self.run_case('notary-receipt', NOTARY='Unknown')
        self.run_case('create-scratch', RUNNER_TEMP='')

    def test_rejected_or_pending_notary_retains_known_receipt_but_fails(self):
        for status in ('Invalid', 'Rejected', 'In Progress'):
            with self.subTest(status=status):
                self.run_case('notary-accepted', notary_receipt=True, NOTARY=status)
        self.run_case('notary-submit', 7, notary_receipt=True, NOTARY_EXIT='7')

    def test_all_six_missing_placeholder_values_fail_before_keychain(self):
        for name in ('CERTIFICATE', 'PASSWORD', 'IDENTITY', 'APPLE_ID',
                     'APPLE_APP_SPECIFIC_PASSWORD', 'APPLE_TEAM_ID'):
            for value in ('', 'REPLACE_ME_BEFORE_RELEASE'):
                with self.subTest(name=name, value=value):
                    self.assertEqual(self.run_case('validate-inputs', **{name:value}), [])

    def test_failure_receipt_never_clobbers_existing_evidence(self):
        self.run_case('import-certificate', 5, existing_failure=True, FAIL='security:import')

    def test_signal_reports_current_stage_and_cleans_up(self):
        self.run_case('sign', 143, SIGNAL_AT='codesign:--force')

    def test_cleanup_failure_cannot_succeed_or_hide_primary_failure(self):
        for command in ('security:list-keychains:restore', 'security:delete-keychain'):
            with self.subTest(command=command):
                self.run_case('cleanup', cleanup='failed', notary_receipt=True, FAIL=command)
                self.run_case('import-certificate', 5, cleanup='failed', FAIL='security:import,'+command)


if __name__ == '__main__':unittest.main()
