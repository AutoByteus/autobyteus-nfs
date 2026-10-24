# API-03; 2026-10-24; d9beb0f; Mac arm64 host; current development-only Linux build.
from pathlib import Path
import os,sys,shutil,subprocess,json,datetime,hashlib
sys.dont_write_bytecode=True
n=Path.cwd();e=n/'tickets/in-progress/nfs-setup-dashboard/evidence';r=Path('/Users/normy/nfs-dashboard-api-w47yo5sg');s=r/'source';s.mkdir()
for rel in subprocess.check_output(['git','ls-files'],text=True).splitlines():
 p=n/rel
 if not rel.startswith('tickets/') and p.is_file():q=s/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
sys.path[:0]=[str(s/'packaging'),str(s/'packaging/engine')]
from release_support import identity
import manifest
original=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate/engine'); engine=json.loads((original/'engine-manifest.json').read_text());manifest.validate(engine,require_both=True)
for arch,bundle in engine['architectures'].items():manifest.verify_files(bundle,original/arch)
sourcehash=identity.source_hash(engine,root=s)
assert sourcehash=='324bf4dbb24b8001324033a0abc131bc50a26e5d98284dcbb95d1be790e8cf13'
lock=json.loads((s/'packaging/release-lock.json').read_text())
metadata={'schema':2,'version':'development-dashboard','sourceHash':sourcehash,'engine':engine,'ubuntuPackages':lock['ubuntuPackages'],'engineImage':'ghcr.io/autobyteus/autobyteus-nfs@sha256:e39b1b13d09c6c6c604de470023a8c3d6ba834d127f2df5e2dbb79e931a585ec','releaseTargets':[],'fieldValidation':{'filesystem':'deferred','user':'deferred'}}
(s/'cmd/autobyteus-nfs/release.json').write_text(json.dumps(metadata,indent=2)+'\n');manifest.embed(engine,original,'arm64',s/'internal/backend/engine-assets')
out=r/'autobyteus-nfs';cmd=[str(r/'tools/go/bin/go'),'build','-trimpath','-o',str(out),'./cmd/autobyteus-nfs'];env={**os.environ,'HOME':str(r/'home'),'TMPDIR':str(r/'tmp'),'GOCACHE':str(r/'cache'),'GOTOOLCHAIN':'local','CGO_ENABLED':'0','GOOS':'linux','GOARCH':'arm64'}
with (e/'API-03-build.log').open('w') as f:
 f.write('API-03 current d9beb0f Linux-arm64 development build; Mac host 2026-10-24\n');f.flush();p=subprocess.run(cmd,cwd=s,env=env,stdout=f,stderr=subprocess.STDOUT)
record={'case':'API-03','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'command':cmd,'environment':env|{'PATH':'not recorded'},'sourceHash':sourcehash,'engineManifestSHA256':hashlib.sha256((original/'engine-manifest.json').read_bytes()).hexdigest(),'exit':p.returncode,'binarySHA256':hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None,'scope':'development/no release admission; Linux compile only until guest execution'}
record['environment']={k:env[k] for k in ['HOME','TMPDIR','GOCACHE','GOTOOLCHAIN','CGO_ENABLED','GOOS','GOARCH']}
(e/'API-03-build.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));sys.exit(p.returncode)
