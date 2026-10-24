# IMP-06: isolated current source + freshly measured unchanged engine.
# Never writes repository release.json/lock/assets; does not admit any release.
from pathlib import Path
import os,sys,shutil,subprocess,json,datetime,hashlib
sys.dont_write_bytecode=True
w=Path.cwd();r=Path('/Users/normy/nfs-dashboard-imp-1ed_m7l0');s=r/sys.argv[1];s.mkdir()
for rel in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],text=True).splitlines():
 p=w/rel
 if not rel.startswith('tickets/') and p.is_file():q=s/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
sys.path.insert(0,str(s/'packaging'));sys.path.insert(0,str(s/'packaging/engine'))
from release_support import identity
import manifest
engine=json.loads((r/'measured-engine/engine-manifest.json').read_text());manifest.validate(engine,require_both=True)
for arch,bundle in engine['architectures'].items():manifest.verify_files(bundle,r/'measured-engine'/arch)
sourcehash=identity.source_hash(engine,root=s)
lock=json.loads((s/'packaging/release-lock.json').read_text())
metadata={'schema':2,'version':'development-dashboard','sourceHash':sourcehash,'engine':engine,'ubuntuPackages':lock['ubuntuPackages'],'engineImage':'ghcr.io/autobyteus/autobyteus-nfs@sha256:e39b1b13d09c6c6c604de470023a8c3d6ba834d127f2df5e2dbb79e931a585ec','releaseTargets':[],'fieldValidation':{'filesystem':'deferred','user':'deferred'}}
(s/'cmd/autobyteus-nfs/release.json').write_text(json.dumps(metadata,indent=2)+'\n')
manifest.embed(engine,r/'measured-engine','arm64',s/'internal/backend/engine-assets')
record={'id':'IMP-06','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':str(s),'baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'sourceHash':sourcehash,'metadata':metadata,'note':'working implementation, development/unpublished, no release admission; retained engine bytes reused not rebuilt','binaries':{}}
for system in ['darwin','linux']:
 out=r/(sys.argv[1]+'-'+system)
 cmd=[str(r/'go/bin/go'),'build','-trimpath','-o',str(out),'./cmd/autobyteus-nfs']
 env={**os.environ,'HOME':str(r/'home'),'TMPDIR':str(r/'tmp'),'GOCACHE':str(r/'cache'),'GOTOOLCHAIN':'local','CGO_ENABLED':'0','GOOS':system,'GOARCH':'arm64'}
 with (w/('tickets/in-progress/nfs-setup-dashboard/evidence/IMP-06-'+sys.argv[1]+'-'+system+'.log')).open('w') as log:result=subprocess.run(cmd,cwd=s,env=env,stdout=log,stderr=subprocess.STDOUT)
 record['binaries'][system]={'command':cmd,'exit':result.returncode,'sha256':hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None}
 if result.returncode:break
(w/('tickets/in-progress/nfs-setup-dashboard/evidence/IMP-06-'+sys.argv[1]+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
