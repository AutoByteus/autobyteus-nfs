"""IMP-07-01: actual empty, owned keychain lookup; no credentials or trust changes.
Command: python3 tickets/done/nfs-first-release/evidence/IMP-07-01-keychain-probe.py
Input: 79e35392bfe4f795464fecd8c034670b622c1684; Darwin arm64; 2026-10-19.
"""
import hashlib
import json
import os
from pathlib import Path
import secrets
import shlex
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[4]
result = {'check': 'IMP-07-01', 'input': '79e35392bfe4f795464fecd8c034670b622c1684',
          'date': '2026-10-19', 'environment': 'Darwin arm64', 'scope': 'Empty disposable keychain and own binary copy only; no user signing key, P12, trust change, timestamp request or notary'}
scratch = Path(tempfile.mkdtemp(prefix='nfs-imp07-empty-', dir=Path.home()))
os.chmod(scratch, 0o700)
keychain = scratch / 'signing.keychain-db'
prior = subprocess.check_output(['/usr/bin/security', 'list-keychains', '-d', 'user'])
prior_list = shlex.split(prior.decode())
password = secrets.token_hex(32)
try:
    r = subprocess.run(['/usr/bin/security', 'create-keychain', '-p', password, str(keychain)], capture_output=True)
    result['createExit'] = r.returncode
    result['exactPathExists'] = keychain.exists()
    result['doubledSuffixExists'] = Path(str(keychain)+'-db').exists()
    assert r.returncode == 0
    current = shlex.split(subprocess.check_output(['/usr/bin/security', 'list-keychains', '-d', 'user']).decode())
    result['createdKeychainInSearchList'] = str(keychain) in current
    result['priorEntriesRetained'] = all(p in current for p in prior_list)
    binary = scratch/'probe'
    shutil.copyfile('/usr/bin/true', binary)
    before = hashlib.sha256(binary.read_bytes()).hexdigest()
    missing = 'NFS-IMP07-missing-' + secrets.token_hex(8)
    r = subprocess.run(['/usr/bin/codesign', '--force', '--timestamp', '--options', 'runtime', '--keychain', str(keychain), '--sign', missing, str(binary)], capture_output=True)
    result['missingIdentityExit'] = r.returncode
    # No private input. Still emit only equality with the documented literal shape.
    result['identityPrefixedNoIdentityFound'] = r.stderr.decode().strip() == missing+': no identity found'
    result['binaryUnchanged'] = before == hashlib.sha256(binary.read_bytes()).hexdigest()
finally:
    restore = subprocess.run(['/usr/bin/security', 'list-keychains', '-d', 'user', '-s', *prior_list], capture_output=True)
    delete = subprocess.run(['/usr/bin/security', 'delete-keychain', str(keychain)], capture_output=True)
    result['restoreExit'] = restore.returncode
    result['deleteExit'] = delete.returncode
    result['searchListExactlyRestored'] = subprocess.check_output(['/usr/bin/security', 'list-keychains', '-d', 'user']) == prior
    shutil.rmtree(scratch)
    result['ownedScratchRemoved'] = not scratch.exists()
    (root/'tickets/done/nfs-first-release/evidence/IMP-07-01-keychain-probe.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
