from pathlib import Path
import subprocess,json,tempfile,hashlib,tarfile,shutil,datetime
E=Path(__file__).resolve().parent; prior=json.loads((E/'public-download-verification.json').read_text());root=Path(tempfile.mkdtemp(prefix='nfs-dr015-notary-',dir='/Users/normy'));rows=[]
try:
 for target in ['darwin-arm64','darwin-amd64']:
  name=f'autobyteus-nfs-0.1.0-{target}.tar.gz';a=root/name
  subprocess.run(['curl','--fail','--silent','--show-error','--location','--proto','=https','--max-time','300',prior['downloadedAssets'][name]['anonymousUrl'],'-o',str(a)],check=True)
  assert hashlib.sha256(a.read_bytes()).hexdigest()==prior['downloadedAssets'][name]['sha256']
  d=root/target;d.mkdir();p=d/'autobyteus-nfs'
  with tarfile.open(a,'r:gz') as t:
   assert sorted(t.getnames())==['LICENSE','THIRD_PARTY_NOTICES','autobyteus-nfs','release.json'];assert all(m.isfile() for m in t.getmembers());p.write_bytes(t.extractfile('autobyteus-nfs').read());p.chmod(0o700)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==prior['signatures'][target]['binarySha256']
  args=['codesign','--verify','--strict','--verbose=4','--check-notarization','-R=notarized',str(p)]
  r=subprocess.run(args,capture_output=True,text=True,timeout=180)
  (E/f'public-{target}-notarized-requirement.log').write_text(r.stdout+r.stderr)
  rows.append({'target':target,'binarySha256':hashlib.sha256(p.read_bytes()).hexdigest(),'argv':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
finally:
 shutil.rmtree(root)
 result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':rows,'cleanup':{'root':str(root),'absent':not root.exists()},'source':'https://developer.apple.com/videos/play/wwdc2019/703/','interpretation':'spctl execute app assessment returns3 valid-but-not-an-app for CLI. Preserve that observation, use Apple-documented notarized requirement for other signed code. No security disable, re-sign or credential access. --check-notarization permits online ticket lookup; no claim that cache was empty.'}
 (E/'public-notarization-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
assert len(rows)==2 and all(r['exit']==0 and 'explicit requirement satisfied' in r['stderr'] for r in rows)
