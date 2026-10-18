from common import *
import hashlib,shutil,sys
c=json.loads((E/'environment.json').read_text());P=Path(c['N']);R=P/'repo';env=c['envN']
case='N01'
try:
 event(case,'Started','Focused admission/current host controls, then complete race/vet')
 run('nfs-focused',['go','test','-count=1','-v','./internal/config','./internal/cli','./internal/setup','-run','Standalone|InstallRefuses|BootstrapDirectoryModes'],R,env)
 run('nfs-race',['go','test','-race','-count=1','-json','./...'],R,env)
 run('nfs-vet',['go','vet','./...'],R,env)
 event(case,'Completed','Focused current reader/lock/pre-effect refusal and all Go race/vet passed','Pass','nfs-focused.log; nfs-race.log; nfs-vet.log')
 case='N02';event(case,'Started','Root packaging/installer/workflow/refusal fixtures')
 run('nfs-python',['python3','-m','unittest','discover','-s','scripts/tests','-p','test_nfs_*.py','-v'],R,env)
 run('nfs-actionlint',['actionlint',*map(str,(R/'.github/workflows').glob('*.yml'))],R,env)
 run('nfs-shell',['bash','-n','scripts/public/nfs/install.sh'],R,env)
 run('nfs-source-hash',['python3','packaging/release.py','--source-hash'],R,env)
 run('nfs-publish-refusal',['python3','packaging/release.py','--check-publish'],R,env,expected=1)
 event(case,'Completed','Packaging/shell/workflow checks passed; unqualified publication refused as expected. Python child skip is not counted Pass','Pass','nfs-python.log; nfs-actionlint.log; nfs-shell.log; nfs-source-hash.log; nfs-publish-refusal.log')
 case='N03';event(case,'Started','Compile all four targets; current native version and exact arm64 artifact')
 binaries=[]
 for goos in ['darwin','linux']:
  for arch in ['arm64','amd64']:
   p=P/('autobyteus-nfs-'+goos+'-'+arch)
   run('nfs-build-'+goos+'-'+arch,['go','build','-trimpath','-o',str(p),'./cmd/autobyteus-nfs'],R,dict(env,CGO_ENABLED='0',GOOS=goos,GOARCH=arch))
   binaries.append(dict(target=goos+'/'+arch,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),path=str(p)))
 run('nfs-version',[str(P/'autobyteus-nfs-darwin-arm64'),'version'],R,env)
 source=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/shared-network-workspaces/autobyteus-nfs/out/ir005-local-candidate/engine-candidate')
 bundle=P/'engine-candidate';shutil.copytree(source,bundle)
 sys.path.insert(0,str(R/'packaging/engine'));import manifest
 m=manifest.validate(json.loads((bundle/'engine-manifest.json').read_text()))
 for arch,data in m['architectures'].items():manifest.verify_files(data,bundle/arch)
 manifest.embed(m,bundle,'arm64',R/'internal/backend/engine-assets')
 write('engine-check.json',dict(source=str(source),copy=str(bundle),manifest=m,validation='actual retained artifacts validate/verify_files/embed; unchanged source pins; not fresh engine build or runtime qualification'))
 p=P/'autobyteus-nfs-linux-arm64-embedded'
 run('nfs-build-embedded',['go','build','-trimpath','-o',str(p),'./cmd/autobyteus-nfs'],R,dict(env,CGO_ENABLED='0',GOOS='linux',GOARCH='arm64'))
 write('binaries.json',binaries)
 event(case,'Completed','Four target builds/native version + actual verified arm64 bundle embedded compile passed; no target runtime qualification','Pass','binaries.json; engine-check.json; nfs-build-embedded.log')
except Exception as e:
 event(case,'Completed',str(e),'Fail','commands.jsonl; latest log')
 raise
