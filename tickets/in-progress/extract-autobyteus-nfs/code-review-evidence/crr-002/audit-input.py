from pathlib import Path
import hashlib, json, subprocess
N=Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs')
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
T=N/'tickets/in-progress/extract-autobyteus-nfs'; E=Path(__file__).parent
sha=lambda b: hashlib.sha256(b).hexdigest()
def git(repo,*args): return subprocess.check_output(['git','-C',str(repo),*args])
def tracked(repo): return git(repo,'ls-files','-z').decode().split('\0')[:-1]
def aggregate(hashes): return sha(''.join(p+'\0'+hashes[p]+'\n' for p in sorted(hashes)).encode())
old=json.loads((T/'code-review-evidence/crr-001/input-identities.json').read_text())
expected=[r['path'] for r in json.loads((E/'delta-audit.json').read_text())['results']]
result={'review':'CRR-002','basis':'CRR-001 / IR-002','scope':'Root tickets/ excluded; nested historical ticket inputs retained in S inventory, not counted as new production code.','repositories':{}}
for key,repo in [('N',N),('S',S)]:
 names=[p for p in tracked(repo) if not p.startswith('tickets/')]
 assert set(names)==set(old[key+'files'])
 hashes={p:sha((repo/p).read_bytes()) for p in names}
 changed=sorted(p for p,h in hashes.items() if h!=old[key+'files'][p])
 assert changed==([] if key=='N' else expected),changed
 result['repositories'][key]={'head':git(repo,'rev-parse','HEAD').decode().strip(),'tracked_inputs':len(names),'added_or_removed':[],'changed_since_CRR001':changed,'current_aggregate_sha256':aggregate(hashes)}
 if key=='S':
  assert git(repo,'status','--porcelain')==b''
  delta=git(repo,'diff',old['S'],'HEAD','--')
  (E/'source.diff').write_bytes(delta)
  result['repositories'][key]['numstat']=git(repo,'diff','--numstat',old['S'],'HEAD').decode()
result['authority_files_unchanged']={}
for name in ['requirements-doc.md','investigation-notes.md','solution-revision-record.md','design-spec.md','user-filesystem-boundary-correction.md','solution-design-handoff.md','design-review-report.md','architecture-review-revision-record.md']:
 p=T/name; before=git(N,'show','a77048efc905f1996d6481963625d3940a2c542a:'+str(p.relative_to(N)))
 assert p.read_bytes()==before
 result['authority_files_unchanged'][name]=sha(before)
protected=[p for p in tracked(N) if p.startswith(str(T.relative_to(N))+'/') and Path(p).name not in ['code-review-report.md','code-review-revision-record.md']]
assert all((N/p).read_bytes()==git(N,'show','HEAD:'+p) for p in protected)
result['protected_tracked_ticket_inputs']={'count':len(protected),'aggregate_sha256':aggregate({p:sha((N/p).read_bytes()) for p in protected})}
history=(T/'code-review-revision-record.md').read_bytes()
result['prior_review_history']={'bytes':len(history),'sha256':sha(history),'CRR001_entry_sha256':sha(history.split(b'### CRR-001',1)[1])}
result['current_unused_diagnostics']=json.loads((E/'unused-imports.json').read_text())['diagnostics']; assert result['current_unused_diagnostics']==[]
result['toolchain']={'node':subprocess.check_output(['node','--version']).decode().strip(),'typescript':json.loads((E/'unused-imports.json').read_text())['typescript']}
(E/'input-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
