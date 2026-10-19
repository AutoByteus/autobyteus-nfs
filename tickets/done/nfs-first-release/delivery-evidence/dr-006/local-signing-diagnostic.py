"""User-authorized local Developer ID diagnostic; no export/publication/keychain edits."""
from pathlib import Path
import subprocess, json, os, tempfile, datetime, hashlib, urllib.request, tarfile, io
ROOT=Path.cwd(); E=ROOT/'tickets/done/nfs-first-release/delivery-evidence/dr-006'
S=Path(tempfile.mkdtemp(prefix='nfs-local-signing-',dir='/Users/normy')); os.chmod(S,0o700)
(E/'scratch-path.txt').write_text(str(S)+'\n')
def write(name, obj): (E/name).write_text(json.dumps(obj,indent=2)+'\n')
def run(name,args,env=None,cwd=None,timeout=300):
 r=subprocess.run(args,cwd=cwd or ROOT,env=env,capture_output=True,timeout=timeout)
 p=E/(name+'.log');p.write_bytes(r.stdout+r.stderr)
 rec={'name':name,'argv':args,'exit':r.returncode,'log':p.name,'logSha256':hashlib.sha256(p.read_bytes()).hexdigest()};checks.append(rec);write('checks.json',checks)
 print(name,'exit',r.returncode,flush=True)
 return r
checks=[]
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(); src=S/'source';src.mkdir();
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',head],text=True).splitlines(); paths=[p for p in paths if not p.startswith('tickets/')]
for p in paths:
 dst=src/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(subprocess.check_output(['git','show',head+':'+p]))
home=S/'home';home.mkdir(mode=0o700);tmp=S/'tmp';tmp.mkdir(mode=0o700)
# Public official toolchain inventory; no credential inputs.
releases=json.load(urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all'))
r=next(x for x in releases if x['version']=='go1.27.2');f=next(x for x in r['files'] if x['os']=='darwin' and x['arch']=='arm64' and x['kind']=='archive')
write('toolchain.json',f); archive=S/f['filename'];urllib.request.urlretrieve('https://go.dev/dl/'+f['filename'],archive)
assert hashlib.sha256(archive.read_bytes()).hexdigest()==f['sha256']
subprocess.run(['tar','-xzf',str(archive),'-C',str(S)],check=True)
go=str(S/'go/bin/go'); env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL') if k in os.environ};env.update(HOME=str(home),TMPDIR=str(tmp),GOCACHE=str(S/'go-cache'),GOPATH=str(S/'go-path'),GOTOOLCHAIN='local',CGO_ENABLED='0')
assert run('go-version',[go,'version'],env).returncode==0
binary=S/'autobyteus-nfs';assert run('build',[go,'build','-trimpath','-o',str(binary),'./cmd/autobyteus-nfs'],env,src).returncode==0
unsigned=hashlib.sha256(binary.read_bytes()).hexdigest(); assert run('unsigned-version',[str(binary),'version'],env).returncode==0
# Use only the exact existing Developer ID identity; no key export, unlock or list changes.
keychain='/Users/normy/Library/Keychains/login.keychain-db'; identity='37C9698B12C2CE90D9B9E9F882B67C65C9F5B4FA'
run('keychain-list-before',['security','list-keychains','-d','user'])
write('input.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceCommit':head,'sourceInputCount':len(paths),'buildMetadata':'development: diagnostic only, not release payload','unsignedBinarySha256':unsigned,'identitySha1':identity,'existingKeychain':keychain,'noKeyExportOrPasswordRead':True,'knownLimit':'Existing-identity signing does not test hosted P12/password import or Apple notarization. User directly authorized local signing diagnostic.'})
print('START codesign using existing Developer ID; macOS may request user authorization',flush=True)
try:
 sign=run('codesign',['codesign','--force','--timestamp','--options','runtime','--keychain',keychain,'--sign',identity,str(binary)],timeout=180)
 if sign.returncode==0:
  assert run('verify',['codesign','--verify','--strict','--verbose=2',str(binary)]).returncode==0
  details=run('details',['codesign','-d','--verbose=4',str(binary)])
  s=(details.stdout+details.stderr).decode();assert 'TeamIdentifier=7Y86YBQ7B4' in s and 'Authority=Developer ID Application:' in s and 'Timestamp=' in s and 'runtime' in s
  assert run('signed-version',[str(binary),'version'],env).returncode==0
 result={'localSigning':'Passed' if sign.returncode==0 else 'Failed','signExit':sign.returncode,'signedBinarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'notarization':'Not executed; no locally assigned credential/profile','hostedCause':'Not established by existing-keychain path','publication':'None','scratch':str(S)}
except subprocess.TimeoutExpired:
 result={'localSigning':'Timed out / possible interactive key access','notarization':'Not executed','publication':'None','scratch':str(S)}
run('keychain-list-after',['security','list-keychains','-d','user'])
result['keychainSearchListUnchanged']=(E/'keychain-list-before.log').read_bytes()==(E/'keychain-list-after.log').read_bytes();write('local-result.json',result);print(json.dumps(result),flush=True)
