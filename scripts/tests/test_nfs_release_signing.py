"""Exercise the real signing shell against command doubles; never real credentials."""
import base64
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FAKE=r'''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
name=Path(sys.argv[0]).name;args=sys.argv[1:]
with open(os.environ['CALLS'],'a') as f:f.write(name+' '+(args[0] if args else '')+'\n')
if os.environ.get('FAIL')==name+':'+args[0]:sys.exit(5)
if name=='security':
 if args[0]=='list-keychains' and '-s' not in args:print('"/owned/original.keychain-db"')
 if args[0]=='create-keychain':Path(args[-1]).touch()
 if args[0]=='delete-keychain':Path(args[-1]).unlink()
 if args[0]=='find-identity':print('1) ABC "'+os.environ['IDENTITY']+'"')
if name=='codesign' and args[0]=='-d':
 print('TeamIdentifier='+os.environ['APPLE_TEAM_ID'],file=sys.stderr)
 print('Authority='+os.environ['IDENTITY'],file=sys.stderr)
 print('CodeDirectory flags=0x10000(runtime)',file=sys.stderr)
 print('Timestamp=Oct 18, 2026',file=sys.stderr)
if name=='xcrun':print(json.dumps({'status':os.environ.get('NOTARY','Accepted'),'id':'12345678-1234-1234-1234-123456789abc'}))
if name=='ditto':Path(args[-1]).write_bytes(b'carrier')
'''


class SigningTest(unittest.TestCase):
    def run_case(self,fail='',notary='Accepted',missing=None):
        with tempfile.TemporaryDirectory(prefix='nfs-sign-fixture-') as temp:
            root=Path(temp);bin_dir=root/'bin';bin_dir.mkdir();scratch=root/'scratch';scratch.mkdir()
            for name in ('security','codesign','xcrun','ditto'):
                path=bin_dir/name;path.write_text(FAKE);path.chmod(0o755)
            binary=root/'binary';binary.write_bytes(b'fake unsigned CLI')
            calls=root/'calls';receipt=root/'receipt.json'
            env=os.environ|{'PATH':str(bin_dir)+':'+os.environ['PATH'],'RUNNER_TEMP':str(scratch),
                'CERTIFICATE':base64.b64encode(b'fake p12').decode(),'PASSWORD':'fake-export-password',
                'IDENTITY':'Developer ID Application: Fixture (ABCDEFG123)','APPLE_TEAM_ID':'ABCDEFG123',
                'APPLE_ID':'fixture@example.invalid','APPLE_APP_SPECIFIC_PASSWORD':'fake-app-password',
                'CALLS':str(calls),'FAIL':fail,'NOTARY':notary}
            if missing:env[missing]='REPLACE_ME_BEFORE_RELEASE'
            result=subprocess.run(['/bin/bash',str(ROOT/'packaging/sign-macos.sh'),str(binary),str(receipt)],
                                  env=env,text=True,capture_output=True)
            expected=not fail and not missing and notary=='Accepted'
            self.assertEqual(result.returncode==0,expected,result.stdout+result.stderr)
            self.assertEqual(list(scratch.iterdir()),[],'signing scratch/keychain leaked')
            self.assertEqual(receipt.exists(),not fail and not missing)
            for secret in ('fake-export-password','fake-app-password',env['CERTIFICATE']):
                self.assertNotIn(secret,result.stdout+result.stderr)
            if expected:self.assertEqual(json.loads(receipt.read_text())['status'],'Accepted')
            if not missing:
                trace=calls.read_text();self.assertIn('security list-keychains',trace)
                self.assertIn('security delete-keychain',trace)

    def test_accepted_and_sanitized_receipt(self):self.run_case()
    def test_failed_import_sign_verify_submit_and_rejected_notary_clean_up(self):
        for fail in ('security:import','codesign:--force','codesign:--verify','xcrun:notarytool'):
            with self.subTest(fail=fail):self.run_case(fail=fail)
        self.run_case(notary='Invalid')
        self.run_case(notary='In Progress')
    def test_all_six_missing_placeholder_values_fail_before_keychain(self):
        for name in ('CERTIFICATE','PASSWORD','IDENTITY','APPLE_ID','APPLE_APP_SPECIFIC_PASSWORD','APPLE_TEAM_ID'):
            with self.subTest(name=name):self.run_case(missing=name)

if __name__=='__main__':unittest.main()
