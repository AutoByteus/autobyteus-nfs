from pathlib import Path
import subprocess,json,tempfile,hashlib,tarfile,os,shutil,datetime
E=Path(__file__).resolve().parent;original=Path('/Users/normy/nfs-first-final-dr013-gmvotux9/payload');r=json.loads(subprocess.check_output(['gh','api','repos/AutoByteus/autobyteus-nfs/releases/tags/v0.1.0'],text=True));assert r['id']==417014769 and r['draft'] is False and r['prerelease'] is False
root=Path(tempfile.mkdtemp(prefix='nfs-dr014-public-',dir='/Users/normy'));download=root/'downloads';download.mkdir();home=root/'home';home.mkdir();tmp=root/'tmp';tmp.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();commands=[];inventory={}
(E/'public-smoke-ownership.json').write_text(json.dumps({'root':str(root),'HOME':str(home),'TMPDIR':str(tmp),'purpose':'Anonymous immutable release downloads and owned-HOME version only; no storage setup'},indent=2)+'\n')
def run(name,args,env=None):
 p=subprocess.run(args,capture_output=True,text=True,env=env,timeout=600);(E/(name+'.log')).write_text(p.stdout+p.stderr);commands.append({'name':name,'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
try:
 expected={p.name:p for p in (original/'assets').iterdir()};assert len(expected)==18 and {a['name'] for a in r['assets']}==set(expected)
 for name,src in sorted(expected.items()):
  out=download/name;url='https://github.com/AutoByteus/autobyteus-nfs/releases/download/v0.1.0/'+name;p=run('public-download-'+name.replace('.','-'),['curl','--fail','--silent','--show-error','--location','--proto','=https','--tlsv1.2','--max-time','600','--max-filesize',str(src.stat().st_size),url,'-o',str(out)]);assert p.returncode==0 and out.stat().st_size==src.stat().st_size and sha(out)==sha(src);inventory[name]={'size':out.stat().st_size,'sha256':sha(out),'anonymousUrl':url,'equalsOriginalRetained':True}
 provenance=json.loads((download/'release-provenance.json').read_text());signatures={}
 for target in ['darwin-arm64','darwin-amd64']:
  d=root/target;d.mkdir();archive=download/f'autobyteus-nfs-0.1.0-{target}.tar.gz'
  with tarfile.open(archive,'r:gz') as tar:
   assert sorted(tar.getnames())==['LICENSE','THIRD_PARTY_NOTICES','autobyteus-nfs','release.json']
   for m in tar.getmembers():assert m.isfile()
   binary=d/'autobyteus-nfs';binary.write_bytes(tar.extractfile('autobyteus-nfs').read());binary.chmod(0o700)
  assert sha(binary)==provenance['signing'][target]['binarySha256']
  v=run('public-'+target+'-codesign-verify',['codesign','--verify','--strict','--verbose=2',str(binary)]);info=run('public-'+target+'-codesign-details',['codesign','-d','--verbose=4',str(binary)]);assert v.returncode==info.returncode==0 and 'Authority=Developer ID Application:' in info.stderr and 'TeamIdentifier=7Y86YBQ7B4' in info.stderr and 'Timestamp=' in info.stderr and 'runtime' in info.stderr
  gate=run('public-'+target+'-gatekeeper',['spctl','--assess','--type','execute','--verbose=4',str(binary)])
  signatures[target]={'binarySha256':sha(binary),'codesignStrict':v.returncode,'DeveloperIdTeamTimestampRuntime':True,'notary':provenance['signing'][target],'gatekeeperExit':gate.returncode,'gatekeeperOutput':gate.stdout+gate.stderr,'localEnvironment':'macOS native arm64; Intel signature assessment only, no Intel execution'}
 env=dict(os.environ,HOME=str(home),TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1');install=run('public-owned-home-install-version',['/bin/bash',str(download/'autobyteus-nfs-install.sh'),'version'],env);assert install.returncode==0 and install.stdout.strip()=='v0.1.0' and 'deferred' in install.stderr.lower()
 binary=home/'.local/bin/autobyteus-nfs';version=run('public-installed-version',[str(binary),'version'],env);assert version.returncode==0 and version.stdout=='v0.1.0\n';assert sha(binary)==provenance['signing']['darwin-arm64']['binarySha256']
 assert not (home/'.config').exists();result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'releaseId':r['id'],'releaseUrl':r['html_url'],'downloadedAssets':inventory,'signatures':signatures,'installer':{'exit':install.returncode,'stdout':install.stdout,'stderr':install.stderr,'explicitVersionOnly':True,'installedBinarySha256':sha(binary),'noHostConfiguration':True},'originalPayloadSource':provenance['sourceCommit'],'executor':'3424f8dddef795d4a42e83ed8746268a4aab4d7d','fieldValidation':provenance['fieldValidation'],'scope':'Actual anonymous release bytes, current native Macarm installer/version and both Mac static signatures/Gatekeeper; no field/user or native Intel execution'}
 (E/'public-download-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'assets':len(inventory),'installer':'Pass','gatekeeper':{k:v['gatekeeperExit'] for k,v in signatures.items()}},indent=2))
finally:
 (E/'public-download-commands.json').write_text(json.dumps(commands,indent=2)+'\n');shutil.rmtree(root);(E/'public-smoke-cleanup.json').write_text(json.dumps({'root':str(root),'absent':not root.exists(),'scope':'Only owned public download/extraction/HOME/TMP; original retained payload/candidates untouched'},indent=2)+'\n')
