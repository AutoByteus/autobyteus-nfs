"""IMP-07-02: real-tool synthetic identity lookup with/without search membership.
Command: python3 tickets/done/nfs-first-release/evidence/IMP-07-02-identity-probe.py
Input: 79e35392bfe4f795464fecd8c034670b622c1684; Darwin arm64; 2026-10-19.
Only a newly generated disposable self-signed identity; NEVER release proof.
"""
import json
import os
from pathlib import Path
import secrets
import shlex
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[4]
result = {'check': 'IMP-07-02', 'input': '79e35392bfe4f795464fecd8c034670b622c1684',
          'date': '2026-10-19', 'environment': 'Darwin arm64',
          'scope': 'Synthetic self-signed identity generated in owned scratch; no real Developer ID key/P12/trust store/notary; no timestamp request; never a release fallback'}
scratch = Path(tempfile.mkdtemp(prefix='nfs-imp07-identity-', dir=Path.home()))
os.chmod(scratch, 0o700)
keychain = scratch/'signing.keychain-db'
prior = subprocess.check_output(['/usr/bin/security', 'list-keychains', '-d', 'user'])
prior_list = shlex.split(prior.decode())
password = secrets.token_hex(32)
identity = 'NFS-IMP07-Synthetic-'+secrets.token_hex(8)
def run(name, args):
    r = subprocess.run(args, capture_output=True, timeout=30)
    result[name+'Exit'] = r.returncode
    if r.returncode:
        raise RuntimeError(name+' failed; no private output printed')
    return r
try:
    cfg = scratch/'openssl.cnf'
    cfg.write_text('[req]\ndistinguished_name=dn\nx509_extensions=ext\nprompt=no\n[dn]\nCN='+identity+'\n[ext]\nbasicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature\nextendedKeyUsage=codeSigning\n')
    run('generate', ['/usr/bin/openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','1','-config',str(cfg),'-keyout',str(scratch/'key.pem'),'-out',str(scratch/'cert.pem')])
    # This exports ONLY our newly generated synthetic key, never a user identity.
    run('syntheticP12', ['/usr/bin/openssl','pkcs12','-export','-inkey',str(scratch/'key.pem'),'-in',str(scratch/'cert.pem'),'-out',str(scratch/'synthetic.p12'),'-passout','pass:'+password])
    run('create', ['/usr/bin/security','create-keychain','-p',password,str(keychain)])
    run('unlock', ['/usr/bin/security','unlock-keychain','-p',password,str(keychain)])
    run('import', ['/usr/bin/security','import',str(scratch/'synthetic.p12'),'-k',str(keychain),'-P',password,'-T','/usr/bin/codesign'])
    run('partition', ['/usr/bin/security','set-key-partition-list','-S','apple-tool:,apple:,codesign:','-s','-k',password,str(keychain)])
    ids = run('findIdentity', ['/usr/bin/security','find-identity','-v','-p','codesigning',str(keychain)])
    result['exactIdentityInExplicitValidQuery'] = ('"'+identity+'"').encode() in ids.stdout
    for membership in ('original','with-owned-keychain'):
        if membership != 'original':
            run('addOwnedMembership', ['/usr/bin/security','list-keychains','-d','user','-s',str(keychain),*prior_list])
        binary = scratch/('probe-'+membership)
        shutil.copyfile('/usr/bin/true',binary)
        r = subprocess.run(['/usr/bin/codesign','--force','--timestamp=none','--options','runtime','--keychain',str(keychain),'--sign',identity,str(binary)],capture_output=True,timeout=30)
        lines = r.stderr.decode().splitlines()
        result[membership] = {'signExit': r.returncode,
          'identityPrefixedNoIdentityFound': identity+': no identity found' in lines,
          'chainWarning': any(x.startswith('Warning: unable to build chain to self-signed root for signer ') for x in lines),
          'internalComponent': str(binary)+': errSecInternalComponent' in lines,
          'verifyExit': subprocess.run(['/usr/bin/codesign','--verify','--strict',str(binary)],capture_output=True).returncode if r.returncode == 0 else None}
finally:
    restore = subprocess.run(['/usr/bin/security','list-keychains','-d','user','-s',*prior_list],capture_output=True)
    delete = subprocess.run(['/usr/bin/security','delete-keychain',str(keychain)],capture_output=True)
    result['restoreExit'] = restore.returncode
    result['deleteExit'] = delete.returncode
    result['searchListExactlyRestored'] = subprocess.check_output(['/usr/bin/security','list-keychains','-d','user']) == prior
    shutil.rmtree(scratch)
    result['ownedScratchRemoved'] = not scratch.exists()
    (root/'tickets/done/nfs-first-release/evidence/IMP-07-02-identity-probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
