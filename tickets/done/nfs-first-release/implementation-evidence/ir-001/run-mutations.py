"""Disposable source mutations: assert focused tests detect each removed invariant."""
import json,os,shutil,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4];S=Path((E/'scratch-path.txt').read_text().strip());source=S/'mutation-source-final'
source.mkdir()
for name in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines():
    if name.startswith('tickets/'):continue
    p=ROOT/name
    if p.is_file():out=source/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1','HOME':str(S/'home'),'TMPDIR':str(S/'tmp')}
cases=[
 ('user-consent','packaging/release_support/qualification.py',"user['kind'] == 'executed-user-check'","True",'test_nfs_release_records.py'),
 ('oci-blob-hash','packaging/release_support/candidate.py',"measured.hexdigest() == digest[7:]","True",'test_nfs_release_records.py'),
 ('workflow-identity','packaging/release_support/candidate.py',"workflow_bytes == (i.ROOT / i.WORKFLOW).read_bytes()","True",'test_nfs_release_records.py'),
 ('image-preserve','packaging/release_support/publication.py',"'--all', '--preserve-digests'","'--all'",'test_nfs_release_publication.py'),
 ('fresh-main','packaging/release_support/publication.py',"    fresh_main(binding['sourceCommit'])","    pass # removed fresh_main(binding['sourceCommit'])",'test_nfs_release_publication.py'),
 ('notary-accepted','packaging/sign-macos.sh',"assert r['status'] == 'Accepted', 'Notarization not Accepted'","# removed Accepted gate",'test_nfs_release_signing.py'),
]
results=[]
for name,file,before,after,test in cases:
 p=source/file;original=p.read_text();assert before in original;p.write_text(original.replace(before,after))
 try:
  with (E/('mutation-'+name+'.log')).open('w') as log:
   r=subprocess.run(['/usr/bin/python3','-m','unittest','discover','-s','scripts/tests','-p',test,'-v'],cwd=source,env=env,stdout=log,stderr=subprocess.STDOUT)
  result={'name':name,'test':test,'exitCode':r.returncode,'detected':r.returncode!=0};results.append(result);print(result,flush=True)
 finally:p.write_text(original)
(E/'mutations.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(0 if all(x['detected'] for x in results) else 1)
