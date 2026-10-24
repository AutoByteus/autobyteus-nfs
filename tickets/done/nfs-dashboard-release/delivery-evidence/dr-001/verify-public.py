"""Actual final public bytes/signatures/install; private HOME, no host setup."""
import datetime,hashlib,json,os,pathlib,subprocess,sys,tarfile,urllib.request
E=pathlib.Path(__file__).resolve().parent;N=E.parents[4]
S=pathlib.Path(json.loads((E/'resources.json').read_text())['root']);P='448cef839b4919a1e3ae0489e8d86ae36f5cee33';repo='AutoByteus/autobyteus-nfs'
summary=json.loads((E/'publication-resume-summary.json').read_text());assert summary['conclusion']=='success' and summary['source']==P
root=S/'public';assert root.is_dir();download=root/'downloads';assert download.is_dir();home=root/'home';tmp=root/'tmp';assert home.is_dir() and tmp.is_dir() and not list(home.iterdir()) and not list(tmp.iterdir())
commands=json.loads((E/'public-attempt-1/public-verification-commands.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(E/name).write_text(json.dumps(x,indent=2)+'\n')
def run(name,args,env=None,timeout=900):
 p=subprocess.run(args,cwd=N,capture_output=True,text=True,env=env,timeout=timeout)
 (E/(name+'.log')).write_text(p.stdout+p.stderr+'\nexit='+str(p.returncode)+'\n')
 commands.append({'name':name,'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save('public-verification-commands.json',commands);return p
# Existing inspect-bound independently resolves tag/source/envelopes and all byte/job proofs; no authority/effect.
sys.path.insert(0,str(N/'packaging'));from release_support import publication,payload
proof=json.loads((E/'retained-final.json').read_text());assert publication.tag_identity('v0.2.0')==proof['tag']
payload.verify(S/'final-inspection/payload',S/'final-inspection/candidate')
retained=S/'final-inspection/payload';proof=json.loads((E/'retained-final.json').read_text());assert proof['payloadSourceCommit']==P
record=json.loads((retained/'publication.json').read_text());assert record['sourceCommit']==P and record['runId']==40107739742 and proof['tag']['binding']['envelope']['runId']==record['runId']
# Public APIs and versioned URLs below have NO Authorization header or gh credentials.
def public_json(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AutoByteus-NFS-release-verification'}),timeout=60) as response:
  assert response.status==200;return json.load(response)
r=public_json(f'https://api.github.com/repos/{repo}/releases/tags/v0.2.0');latest=public_json(f'https://api.github.com/repos/{repo}/releases/latest')
assert r['id']==latest['id'] and not r['draft'] and not r['prerelease'] and r['tag_name']=='v0.2.0';save('public-release.json',r)
expected={f.name:f for f in (retained/'assets').iterdir()};assert len(expected)==18 and set(expected)=={a['name'] for a in r['assets']}
inventory={}
for name,src in sorted(expected.items()):
 out=download/name;url=f'https://github.com/{repo}/releases/download/v0.2.0/{name}'
 # Reuse exact first-attempt anonymous downloads; verify again, do not claim a second network download.
 assert out.is_file() and out.stat().st_size==src.stat().st_size and sha(out)==sha(src)
 inventory[name]={'size':out.stat().st_size,'sha256':sha(out),'anonymousUrl':url,'equalsRetained':True}
 save('public-assets.json',inventory)
checks={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (download/'SHA256SUMS-nfs').read_text().splitlines()};assert len(checks)==17 and set(checks)==set(expected)-{'SHA256SUMS-nfs'}
assert all(checks[name]==inventory[name]['sha256'] for name in checks)
provenance=json.loads((download/'release-provenance.json').read_text());metadata=json.loads((download/'autobyteus-nfs-manifest.json').read_text());assert provenance['sourceCommit']==P and provenance['fieldValidation']=={'filesystem':'deferred','user':'deferred'}
signatures={};archives={}
for target in ('darwin-arm64','darwin-amd64','linux-arm64','linux-amd64'):
 archive=download/f'autobyteus-nfs-0.2.0-{target}.tar.gz'
 with tarfile.open(archive,'r:gz') as tar:
  assert sorted(tar.getnames())==['LICENSE','THIRD_PARTY_NOTICES','autobyteus-nfs','release.json'];assert all(m.isfile() for m in tar.getmembers())
  assert json.load(tar.extractfile('release.json'))==metadata
  raw=tar.extractfile('autobyteus-nfs').read();assert len(raw)<=100*1024*1024
  archives[target]={'binarySHA256':hashlib.sha256(raw).hexdigest(),'binarySize':len(raw),'fourRegularMembers':True,'metadataEqualsPublic':True}
  if not target.startswith('darwin'):continue
  dest=root/target;dest.mkdir(exist_ok=True);binary=dest/'autobyteus-nfs'
  if binary.exists():assert binary.read_bytes()==raw
  else:binary.write_bytes(raw);binary.chmod(0o700)
 notary=provenance['signing'][target];assert notary['status']=='Accepted' and sha(binary)==notary['binarySha256']
 verify=run('public-'+target+'-strict-signature',['codesign','--verify','--strict','--verbose=4',str(binary)])
 details=run('public-'+target+'-signature-details',['codesign','-d','--verbose=4',str(binary)])
 assert verify.returncode==details.returncode==0 and 'Authority=Developer ID Application:' in details.stderr and 'TeamIdentifier='+notary['teamId'] in details.stderr and 'Timestamp=' in details.stderr and 'runtime' in details.stderr
 gate=run('public-'+target+'-gatekeeper',['spctl','--assess','--type','execute','--verbose=4',str(binary)])
 signatures[target]={'notary':notary,'strictSignatureExit':verify.returncode,'DeveloperIdTeamTimestampRuntime':True,'gatekeeperExit':gate.returncode,'gatekeeperOutput':gate.stdout+gate.stderr,'limits':'Static signature and online assessment on macOS26.5.2 ARM64; not native Intel execution'}
 save('public-signatures.json',signatures)
 assert gate.returncode==0 or (gate.returncode==3 and 'the code is valid but does not seem to be an app' in gate.stderr),'Unexpected policy assessment needs diagnosis'
 online=run('public-'+target+'-online-notary',['codesign','--verify','--strict','--verbose=4','--check-notarization','-R=notarized',str(binary)])
 assert online.returncode==0 and 'explicit requirement satisfied' in online.stderr,'Actual online notarization requirement failed'
 signatures[target]['onlineNotarizedRequirementExit']=online.returncode
 signatures[target]['appAssessmentInterpretation']='Not an app: observed exit3 is not a Gatekeeper Pass; appropriate standalone-code online notarized requirement is mandatory and passed.' if gate.returncode==3 else 'Accepted app assessment'
 save('public-signatures.json',signatures)
env=dict(os.environ,HOME=str(home),TMPDIR=str(tmp),XDG_CONFIG_HOME=str(home/'.config'),XDG_CACHE_HOME=str(home/'.cache'),PYTHONDONTWRITEBYTECODE='1')
install=run('public-mac-install-version',['/bin/bash',str(download/'autobyteus-nfs-install.sh'),'version'],env);assert install.returncode==0 and install.stdout=='v0.2.0\n' and 'deferred' in install.stderr.lower()
installed=home/'.local/lib/autobyteus-nfs/v0.2.0/autobyteus-nfs';assert installed.is_file() and sha(installed)==provenance['signing']['darwin-arm64']['binarySha256']
assert (home/'.local/bin/autobyteus-nfs').resolve()==installed
version=run('public-mac-installed-version',[str(installed),'version'],env);assert version.returncode==0 and version.stdout=='v0.2.0\n'
assert not (home/'.config').exists();assert not list(tmp.iterdir())
save('public-install.json',{'result':'Pass','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'version':'v0.2.0','installedBinary':str(installed),'home':str(home),'binarySHA256':sha(installed),'installerExit':install.returncode,'stdout':install.stdout,'stderr':install.stderr,'installedVersionExit':version.returncode,'noStorageConfiguration':True,'installerScratchRemoved':True,'limits':'Private HOME native Mac ARM64 public install/version only; no user installation or storage setup'})
save('public-verification.json',{'result':'Pass','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'releaseId':r['id'],'releaseUrl':r['html_url'],'normalLatest':True,'source':P,'tag':proof['tag'],'payloadJobId':proof['verifiedPayloadJobId'],'assetCount':len(inventory),'assets':inventory,'archives':archives,'signatures':signatures,'sourceHash':provenance['sourceHash'],'oci':provenance['oci'],'readiness':provenance['releaseReadiness'],'fieldValidation':provenance['fieldValidation'],'limits':'Exact public distribution, not field testing. Hosted Ubuntu install/anonymous fullOCI proof in publication receipt/log; public dashboard launch separate.'})
print(json.dumps({'result':'Pass','assets':len(inventory),'release':r['html_url'],'bothMacOnlineNotarized':{k:v['onlineNotarizedRequirementExit'] for k,v in signatures.items()},'appAssessmentObservedNotApp':{k:v['gatekeeperExit'] for k,v in signatures.items()},'privateMacInstall':'Pass'}))
