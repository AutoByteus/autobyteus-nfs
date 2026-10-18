from pathlib import Path
import subprocess,json,hashlib,re,datetime
E=Path(__file__).resolve().parent; N=E.parents[4]; S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
B='3712cd9bf0db998501d162db7f8655f169e3def6'; R='fc5d2ff3f404de3a683994766dfd47c258efb374'
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def old(p):return git(S,'show',B+':'+p)
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(root):return [p for p in git(root,'ls-files','-z').decode().split('\0') if p and not p.startswith('tickets/')]
def eff(b):return sum(bool(x.strip()) for x in b.decode().splitlines())
npaths=rows(N); spaths=rows(S)
comparison=[]
oldgo=[p for p in git(S,'ls-tree','-r','--name-only',B,'autobyteus-nfs').decode().splitlines() if p.endswith('.go')]
for p in oldgo:
 q=p.removeprefix('autobyteus-nfs/');data=old(p).replace(b'github.com/AutoByteus/autobyteus-workspace/autobyteus-nfs',b'github.com/AutoByteus/autobyteus-nfs')
 comparison.append(dict(source=p,destination=q,kind='removed' if not (N/q).exists() else 'normalized-equal' if data==(N/q).read_bytes() else 'R2-changed'))
license_rows=[]
for a,b in [('autobyteus-nfs/LICENSE','LICENSE'),('CLA.md','CLA.md'),('autobyteus-nfs/THIRD_PARTY_NOTICES','THIRD_PARTY_NOTICES'),('autobyteus-nfs/packaging/release-lock.json','packaging/release-lock.json')]:
 data=old(a);eq=data==(N/b).read_bytes();assert eq,(a,b);license_rows.append(dict(source=a,destination=b,sha256=sha(data),equal=True))
pins=[]
for p in git(S,'ls-tree','-r','--name-only',B,'autobyteus-nfs/packaging/engine').decode().splitlines():
 if p.endswith('README.md'):continue
 q=p.removeprefix('autobyteus-nfs/')
 assert old(p)==(N/q).read_bytes(),q
 pins.append(dict(path=q,sha256=sha(old(p))))
# Every backend/platform/service production Go file remains mechanically equal after import rebasing.
preserved=[r for r in comparison if r['destination'].startswith(('internal/backend/','internal/platform/','internal/service/')) and not r['destination'].endswith('_test.go')]
assert all(r['kind']=='normalized-equal' for r in preserved),preserved
removedS=['autobyteus-nfs','.github/workflows/release-nfs.yml','scripts/public/nfs','autobyteus-server-ts/src/workspaces/shared-workspace-binding.ts','autobyteus-server-ts/src/workspaces/shared-workspace-mount-observation.ts','autobyteus-server-ts/src/agent-execution/services/shared-run-workspace-admission.ts','scripts/public/docker/autobyteus-docker.d/bash/nfs-attachment.sh','autobyteus-server-ts/tests/fixtures/shared-network-workspaces/attachment.json','autobyteus-server-ts/tests/fixtures/shared-network-workspaces/provenance.json']
assert all(not (S/p).exists() for p in removedS)
forbidden=['scopedProjectGitEnvironment','shared-workspace-binding','launcher-attachment','/etc/autobyteus-nfs','/app/autobyteus-server','safe.directory']
sprod=[p for p in spaths if p.startswith(('autobyteus-server-ts/src/','scripts/public/docker/'))]
hits=[dict(path=p,token=t) for p in sprod for t in forbidden if t.encode() in (S/p).read_bytes()]
assert not hits,hits
nforbidden=['/app/autobyteus','launcher-attachment','NodeAttachment','PublicDirectory','/etc/autobyteus-nfs']
nhits=[dict(path=p,token=t) for p in npaths if p.endswith('.go') and not p.endswith('_test.go') for t in nforbidden if t.encode() in (N/p).read_bytes()]
assert not nhits,nhits
# No sibling Go module or app-source hash dependency.
assert 'replace ' not in (N/'go.mod').read_text()
assert 'autobyteus-server-ts' not in (N/'packaging/release.py').read_text()
assert 'autobyteus-web' not in (N/'packaging/release.py').read_text()
sizes=[]
for label,root,base in [('S',S,B),('N',N,R)]:
 for row in git(root,'diff','--numstat',base,'HEAD').decode().splitlines():
  a,d,p=row.split('\t',2)
  if '{' in p or ' => ' in p or not (root/p).is_file():continue
  if not p.endswith(('.go','.ts','.vue','.sh','.py')) or '/tests/' in p or '/__tests__/' in p or p.endswith('_test.go') or p.startswith('tickets/'):continue
  try:prev=git(root,'show',base+':'+p)
  except subprocess.CalledProcessError:prev=b''
  now=(root/p).read_bytes(); b=eff(prev);n=eff(now)
  sizes.append(dict(repo=label,path=p,before=b,after=n,changed=int(a)+int(d),largeExisting=n>500 and n<=b,violation=n>500 and n>b))
assert not [v for v in sizes if v['violation']]
# Reviewed basis is unchanged by implementation.
basis=[]
for p in ['requirements-doc.md','design-spec.md','design-review-report.md','architecture-review-revision-record.md','investigation-notes.md','solution-revision-record.md','solution-design-handoff.md']:
 q='tickets/in-progress/extract-autobyteus-nfs/'+p
 assert git(N,'show',R+':'+q)==(N/q).read_bytes(),q
 basis.append(dict(path=q,sha256=sha((N/q).read_bytes())))
prior=json.loads((E/'input-audit.json').read_text())
for r in prior['retainedEngine']:assert sha(Path(r['path']).read_bytes())==r['sha256']
pm=[]
for r in prior['pm']:
 v=dict(r);v['currentSHA256']=sha(Path(r['path']).read_bytes());v['unchanged']=v['sha256']==v['currentSHA256'];pm.append(v)
out=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),N=git(N,'rev-parse','HEAD').decode().strip(),S=git(S,'rev-parse','HEAD').decode().strip(),baseline=B,review=R,normalizedGoComparison=comparison,preservedRuntimeProduction=preserved,licenses=license_rows,engineRecipePins=pins,removedAppOwners=removedS,forbiddenAppHits=hits,forbiddenNfsHits=nhits,sourceSizes=sizes,reviewedBasis=basis,retainedEngineUnchanged=True,pm=pm)
(E/'source-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(comparisonCounts={k:sum(v['kind']==k for v in comparison) for k in ['removed','normalized-equal','R2-changed']},preservedProduction=len(preserved),sizeSignals=[v for v in sizes if v['largeExisting'] or v['changed']>220],pm=pm),indent=2))
