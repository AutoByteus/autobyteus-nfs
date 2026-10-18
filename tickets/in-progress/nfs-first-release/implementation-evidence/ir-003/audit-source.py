"""Focused scope, source-size and owner-preservation audit, no cumulative history index."""
import hashlib,json,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[4];T=E.parents[1]
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).splitlines()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
intake=json.loads((E/'input-audit.json').read_text());snapshot=json.loads((E/'final-source-inputs.json').read_text())
changed=git('diff','--name-only',intake['head'])
new=[p for p in git('ls-files','--others','--exclude-standard') if not p.startswith('tickets/')]
source=[p for p in changed+new if not p.startswith('tickets/')]
assert all((R/p).is_file() and sha(R/p)==digest for p,digest in snapshot.items())
assert set(snapshot)=={p for p in git('ls-files','--cached','--others','--exclude-standard') if not p.startswith('tickets/') and (R/p).is_file()}
assert all((R/p).is_file() and sha(R/p)==digest for p,digest in intake['protectedUntracked'].items())
assert not git('diff','--name-only',intake['head'],'--','internal/config','internal/backend','internal/docker','internal/platform','internal/service','packaging/sign-macos.sh','LICENSE','CLA.md','THIRD_PARTY_NOTICES','packaging/engine/source-lock.json','packaging/engine/get-dir-delegation.patch')
assert not (R/'packaging/release_support/qualification.py').exists()
production=[p for p in source if (p.endswith('.go') and not p.endswith('_test.go')) or
            (p.startswith('packaging/') and p.endswith('.py')) or p=='scripts/public/nfs/install.sh']
sizes={p:sum(bool(l.strip()) and not l.lstrip().startswith(('#','//')) for l in (R/p).read_text().splitlines()) for p in production if (R/p).exists()}
assert all(v<=500 for v in sizes.values()),sizes
counts={}
for row in git('diff','--numstat',intake['head']):
 a,b,p=row.split('\t');counts[p]=int(a)+int(b)
assert all(counts.get(p,0)<=220 for p in production),counts
lock=json.loads((R/'packaging/release-lock.json').read_text())
assert set(lock)=={'ubuntuBaseImage','ubuntuPackages','engine','releaseReadiness','note'} and lock['releaseReadiness'] is None and lock['engine'] is None
original=json.loads(subprocess.check_output(['git','show',intake['head']+':packaging/release-lock.json'],cwd=R))
assert all(lock[k]==original[k] for k in ('ubuntuBaseImage','ubuntuPackages','engine'))
output={'sourceInputs':len(snapshot),'sourceDelta':source,'effectiveProductionLines':sizes,'changedLines':{p:counts.get(p,'new') for p in production},
        'protectedDeliveryFiles':len(intake['protectedUntracked']),'protectedFilesMatch':True,'hostRuntimeSafetyAndLicensesPinsUnchanged':True,
        'defaultReadinessNull':True,'noGeneratedArtifactsInSource':not any(p.endswith('.deb') for p in snapshot)}
(E/'source-audit.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
