from pathlib import Path
import subprocess,os,json,hashlib,shutil,sys,time
E=Path(__file__).resolve().parent;N=E.parents[4];P=Path((E/'scratch-path.txt').read_text().strip());R=Path((E/'standalone-final-root.txt').read_text().strip())/'standalone'
R.mkdir()
roots=[x for x in subprocess.check_output(['git','-C',str(N),'ls-tree','--name-only','HEAD'],text=True).splitlines() if x!='tickets']
a=subprocess.Popen(['git','-C',str(N),'archive','HEAD',*roots],stdout=subprocess.PIPE)
b=subprocess.run(['tar','-xf','-','-C',str(R)],stdin=a.stdout);a.stdout.close();assert b.returncode==a.wait()==0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
archive={str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file()}
(E/'standalone-final-archive.json').write_text(json.dumps({'commit':subprocess.check_output(['git','-C',str(N),'rev-parse','HEAD'],text=True).strip(),'files':archive,'path':str(R)},indent=2)+'\n')
env={'PATH':str(P/'tools/go/bin')+':/opt/homebrew/bin:/usr/bin:/bin','HOME':str(P/'home'),'TMPDIR':str(P/'tmp'),'GOTOOLCHAIN':'local'}
results=[]
def run(name,cmd,expected=0,extra=None):
 start=time.time()
 with (E/('final-'+name+'.log')).open('w') as log:
  x=subprocess.run(cmd,cwd=R,env={**env,**(extra or {})},stdout=log,stderr=subprocess.STDOUT)
 results.append({'name':name,'command':cmd,'exit':x.returncode,'expected':expected,'pass':x.returncode==expected,'seconds':round(time.time()-start,3)})
 (E/'standalone-final-checks.json').write_text(json.dumps(results,indent=2)+'\n');print(name,x.returncode,flush=True)
run('standalone-go-race',['go','test','-race','-count=1','./...'])
run('standalone-go-vet',['go','vet','./...'])
run('standalone-python',['python3','-m','unittest','discover','-s','scripts/tests','-p','test_*.py','-v'])
run('standalone-actionlint',['actionlint','.github/workflows/release-nfs.yml'])
run('standalone-shell',['bash','-n','scripts/public/nfs/install.sh'])
run('standalone-source-hash',['python3','packaging/release.py','--source-hash'])
run('standalone-publish-refusal',['python3','packaging/release.py','--check-publish'],1)
for goos in ['darwin','linux']:
 for arch in ['arm64','amd64']:
  run('standalone-build-'+goos+'-'+arch,['go','build','-trimpath','-o',str(P/('nfs-'+goos+'-'+arch)),'./cmd/autobyteus-nfs'],extra={'GOOS':goos,'GOARCH':arch,'CGO_ENABLED':'0'})
run('standalone-version',[str(P/'nfs-darwin-arm64'),'version'])
# Fresh read/verify, then copy only into owned scratch. Neither old manifests nor engine bytes are changed.
prior=json.loads((E/'input-audit.json').read_text())['retainedEngine']
for row in prior: assert sha(Path(row['path']))==row['sha256']
source=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/shared-network-workspaces/autobyteus-nfs/out/ir005-local-candidate/engine-candidate')
engine=R.parent/'retained-engine';shutil.copytree(source,engine)
sys.path.insert(0,str(R/'packaging/engine'));import manifest
m=manifest.validate(json.loads((engine/'engine-manifest.json').read_text()))
for arch,bundle in m['architectures'].items(): manifest.verify_files(bundle,engine/arch)
manifest.embed(m,engine,'arm64',R/'internal/backend/engine-assets')
(E/'retained-engine-verification.json').write_text(json.dumps({'source':str(source),'copy':str(engine),'freshSHA256':prior,'manifestValidated':True,'embeddedArchitecture':'arm64','qualification':False},indent=2)+'\n')
run('standalone-build-linux-arm64-embedded',['go','build','-trimpath','-o',str(P/'nfs-linux-arm64-embedded'),'./cmd/autobyteus-nfs'],extra={'GOOS':'linux','GOARCH':'arm64','CGO_ENABLED':'0'})
# Save binary hashes; four-target compilation is not native execution qualification.
(E/'standalone-binaries.json').write_text(json.dumps([{ 'name':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(P.glob('nfs-*')) if p.is_file()],indent=2)+'\n')
assert all(row['pass'] for row in results),results
