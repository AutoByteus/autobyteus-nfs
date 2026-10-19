from pathlib import Path
import sys,json,tempfile,hashlib,subprocess,tarfile,shutil,datetime
root=Path.cwd();E=Path(__file__).resolve().parent;sys.path.insert(0,str(root/'packaging'))
from release_support import candidate,payload,identity as i,publication
binding=json.loads((E/'actual-publication-receipt.json').read_text())['payload'];cand=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate');parent=Path(tempfile.mkdtemp(prefix='nfs-first-final-dr013-',dir='/Users/normy'));dest=parent/'payload'
(E/'retained-payload-ownership.json').write_text(json.dumps({'parent':str(parent),'directory':str(dest),'mode':oct(parent.stat().st_mode&0o777),'retain':'Exact already tag-bound signed payload; no rebuild/re-sign or cleanup before recovery'},indent=2)+'\n')
candidate.download(binding['envelope'],candidate.PAYLOAD,dest,successful=False);assert i.sha(dest/'publication.json')==binding['payloadSha256'];receipt=payload.verify(dest,cand);assert publication.tag_binding('v0.1.0',i.commit())==binding
provenance=i.read_json(dest/'assets/release-provenance.json');sigs={};scratch=Path(tempfile.mkdtemp(prefix='nfs-dr013-signature-check-',dir='/Users/normy'))
try:
 for target in ['darwin-arm64','darwin-amd64']:
  d=scratch/target;d.mkdir();archive=dest/'assets'/i.archive_name('v0.1.0',target)
  with tarfile.open(archive,'r:gz') as tf:
   m=tf.getmember('autobyteus-nfs');assert m.isfile();binary=d/'autobyteus-nfs';binary.write_bytes(tf.extractfile(m).read());binary.chmod(0o700)
  assert i.sha(binary)==provenance['signing'][target]['binarySha256']
  verify=subprocess.run(['/usr/bin/codesign','--verify','--strict','--verbose=2',str(binary)],capture_output=True,text=True);details=subprocess.run(['/usr/bin/codesign','-d','--verbose=4',str(binary)],capture_output=True,text=True);assert verify.returncode==details.returncode==0
  s=details.stderr;assert 'Authority=Developer ID Application:' in s and 'TeamIdentifier=7Y86YBQ7B4' in s and 'runtime' in s and 'Timestamp=' in s
  (E/f'downloaded-{target}-codesign.log').write_text(verify.stdout+verify.stderr+details.stdout+details.stderr)
  sigs[target]={'archiveSha256':i.sha(archive),'binarySha256':i.sha(binary),'codesignStrictExit':verify.returncode,'DeveloperIdTeamTimestampRuntimeVerified':True,'notary':provenance['signing'][target]}
finally:shutil.rmtree(scratch)
r={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'directory':str(dest),'binding':binding,'publicationSha256':i.sha(dest/'publication.json'),'payloadVerified':True,'signatures':sigs,'scratchRemoved':not scratch.exists(),'scope':'Actual Actions-retained signed payload/download signatures, NOT public release downloads/install or field tests'}
(E/'retained-payload-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
