"""Fresh anonymous public byte verification and owned-HOME Mac install; no storage."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,tarfile,urllib.request
E=Path(__file__).resolve().parent;N=E.parents[4]
S=Path(json.loads((E/'resources.json').read_text())['root']);V='v0.2.1';REPO='AutoByteus/autobyteus-nfs'
P=json.loads((E/'publication-dispatch.json').read_text())['sourceCommit']
proof=json.loads((E/'retained-final.json').read_text());assert proof['payloadSourceCommit']==P
retained=S/'final-inspection/payload';bound=json.loads((retained/'publication.json').read_text());assert bound['sourceCommit']==P
root=S/'public';root.mkdir(mode=0o700);download=root/'downloads';download.mkdir();home=root/'home';home.mkdir(mode=0o700);tmp=root/'tmp';tmp.mkdir(mode=0o700)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):(E/name).write_text(json.dumps(value,indent=2)+'\n')
commands=[]
def run(name,args,env=None):
 p=subprocess.run(args,cwd=N,capture_output=True,text=True,env=env,timeout=900)
 (E/(name+'.log')).write_text(p.stdout+p.stderr+'\nexit='+str(p.returncode)+'\n')
 commands.append({'name':name,'argv':args,'exit':p.returncode});save('public-commands.json',commands);return p
def public(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NFS-release-verification'}),timeout=60) as r:
  assert r.status==200;return json.load(r)
r=public(f'https://api.github.com/repos/{REPO}/releases/tags/{V}');latest=public(f'https://api.github.com/repos/{REPO}/releases/latest');save('public-release.json',r)
assert r['id']==latest['id'] and not r['draft'] and not r['prerelease'] and r['tag_name']==V
expected={f.name:f for f in (retained/'assets').iterdir()};assert len(expected)==18 and set(expected)=={x['name'] for x in r['assets']}
inventory={}
for name,src in sorted(expected.items()):
 out=download/name;url=f'https://github.com/{REPO}/releases/download/{V}/{name}'
 result=run('download-'+name.replace('.','-'),['curl','--fail','--location','--proto','=https','--tlsv1.2','--silent','--show-error',url,'-o',str(out)])
 assert result.returncode==0 and out.stat().st_size==src.stat().st_size and sha(out)==sha(src),name
 inventory[name]={'size':out.stat().st_size,'sha256':sha(out),'anonymousUrl':url,'equalsRetained':True};save('public-assets.json',inventory)
checks={s.split('  ',1)[1]:s.split('  ',1)[0] for s in (download/'SHA256SUMS-nfs').read_text().splitlines()}
assert len(checks)==17 and set(checks)==set(expected)-{'SHA256SUMS-nfs'} and all(checks[k]==inventory[k]['sha256'] for k in checks)
prov=json.loads((download/'release-provenance.json').read_text());meta=json.loads((download/'autobyteus-nfs-manifest.json').read_text());assert prov['sourceCommit']==P and prov['fieldValidation']=={'filesystem':'deferred','user':'deferred'}
sigs={};archives={}
for target in ['darwin-arm64','darwin-amd64','linux-arm64','linux-amd64']:
 with tarfile.open(download/f'autobyteus-nfs-{V[1:]}-{target}.tar.gz','r:gz') as tar:
  assert sorted(tar.getnames())==['LICENSE','THIRD_PARTY_NOTICES','autobyteus-nfs','release.json'] and all(m.isfile() for m in tar.getmembers())
  assert json.load(tar.extractfile('release.json'))==meta
  member=tar.getmember('autobyteus-nfs');assert member.size<=100*1024**2;data=tar.extractfile(member).read()
  archives[target]={'binarySHA256':hashlib.sha256(data).hexdigest(),'binarySize':len(data),'fourRegularMembers':True,'metadataEqual':True}
  if not target.startswith('darwin'):continue
  dest=root/target;dest.mkdir(mode=0o700);binary=dest/'autobyteus-nfs';binary.write_bytes(data);binary.chmod(0o700)
 notary=prov['signing'][target];assert notary['status']=='Accepted' and sha(binary)==notary['binarySha256']
 verify=run(target+'-strict-signature',['codesign','--verify','--strict','--verbose=4',str(binary)])
 details=run(target+'-signature-details',['codesign','-d','--verbose=4',str(binary)])
 online=run(target+'-online-notary',['codesign','--verify','--strict','--verbose=4','--check-notarization','-R=notarized',str(binary)])
 assert verify.returncode==details.returncode==online.returncode==0
 assert 'Authority=Developer ID Application:' in details.stderr and 'TeamIdentifier='+notary['teamId'] in details.stderr and 'Timestamp=' in details.stderr and 'runtime' in details.stderr and 'explicit requirement satisfied' in online.stderr
 sigs[target]={'notary':notary,'strictSignatureExit':0,'DeveloperIdTeamTimestampRuntime':True,'onlineNotarizedRequirementExit':0,'limits':'Actual current Mac ARM64 static/online standalone-code checks; not Intel execution/Finder/offline/field qualification'};save('public-signatures.json',sigs)
env={k:v for k,v in os.environ.items() if k not in ['GH_TOKEN','GITHUB_TOKEN']};env.update(HOME=str(home),TMPDIR=str(tmp),XDG_CONFIG_HOME=str(home/'.config'),XDG_CACHE_HOME=str(home/'.cache'))
p=run('public-mac-install-version',['/bin/bash',str(download/'autobyteus-nfs-install.sh'),'version'],env)
assert p.returncode==0 and p.stdout==V+'\n' and 'deferred' in p.stderr.lower()
installed=home/f'.local/lib/autobyteus-nfs/{V}/autobyteus-nfs';assert installed.is_file() and sha(installed)==prov['signing']['darwin-arm64']['binarySha256'] and (home/'.local/bin/autobyteus-nfs').resolve()==installed
q=run('public-mac-installed-version',[str(installed),'version'],env);assert q.returncode==0 and q.stdout==V+'\n'
assert not (home/'.config').exists() and not list(tmp.iterdir())
save('public-install.json',{'result':'Pass','version':V,'installedBinary':str(installed),'home':str(home),'binarySHA256':sha(installed),'installerExit':0,'installedVersionExit':0,'noStorageConfiguration':True,'installerScratchRemoved':True,'limits':'Owned HOME public install/version; not user upgrade/storage'})
save('public-verification.json',{'result':'Pass','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'version':V,'releaseId':r['id'],'url':r['html_url'],'normalLatest':True,'source':P,'tag':proof['tag'],'payloadJobId':proof['verifiedPayloadJobId'],'assets':inventory,'archives':archives,'signatures':sigs,'sourceHash':prov['sourceHash'],'oci':prov['oci'],'readiness':prov['releaseReadiness'],'fieldValidation':prov['fieldValidation'],'limits':'Actual public distribution; hosted Ubuntu installer/wholeOCI proof in publisher receipt/log, feedback smoke separate. No field qualification.'})
print('Public18assets,4archive metadata,2Mac signatures/online notary, owned Mac install/version: Pass')
