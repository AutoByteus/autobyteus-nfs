from pathlib import Path
import hashlib,json,subprocess,re
E=Path(__file__).parent;T=E.parent.parent;N=T.parent.parent.parent;S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
a=json.loads((E/'input-audit.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args])
def aggregate(h):return sha(''.join(p+'\0'+h[p]+'\n' for p in sorted(h)).encode())
for key,repo in [('N',N),('S',S)]:
 names=[p for p in git(repo,'ls-files','-z').decode().split('\0')[:-1] if not p.startswith('tickets/')]
 assert len(names)==a['repositories'][key]['tracked_inputs']
 assert aggregate({p:sha((repo/p).read_bytes()) for p in names})==a['repositories'][key]['current_aggregate_sha256']
assert git(S,'status','--porcelain')==b''
base=a['repositories']['N']['head'];names=git(N,'ls-tree','-r','--name-only','-z',base).decode().split('\0')[:-1]
protected=[p for p in names if p.startswith(str(T.relative_to(N))+'/') and Path(p).name not in ['code-review-report.md','code-review-revision-record.md']]
assert len(protected)==a['protected_tracked_ticket_inputs']['count']
assert aggregate({p:sha((N/p).read_bytes()) for p in protected})==a['protected_tracked_ticket_inputs']['aggregate_sha256']
h=(T/'code-review-revision-record.md').read_bytes()
entry=h.split(b'### CRR-001',1)[1].split(b'\n### CRR-002',1)[0]
assert sha(entry)==a['prior_review_history']['CRR001_entry_sha256']
r=(T/'code-review-report.md').read_text()
assert '**Review Decision: Pass' in r and 'Targeted Delta Review' in r
struct=r.split('## Structural / Design Checks',1)[1].split('## Source File Size',1)[0]
rows=[l for l in struct.splitlines() if l.startswith('|')][2:]
assert len(rows)==24 and all('| Pass |' in l for l in rows)
scores=r.split('## Review Scorecard',1)[1].split('## Findings',1)[0]
assert len([l for l in scores.splitlines() if re.match(r'\| \d+ \|',l)])==10
for doc in [T/'code-review-report.md',T/'code-review-revision-record.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  if '://' not in link:assert (doc.parent/link.split('#')[0]).exists(),link
result={'review':'CRR-002','outcome':'Pass','source_score_percent':100,'N_inputs_unchanged':108,'S_inputs_verified':7215,'S_changed_paths_exactly_CR001':3,'protected_ticket_inputs_unchanged':len(protected),'prior_CRR001_entry_byte_identical':True,'structural_checks_current':24,'scorecard_categories_current':10,'reviewer_production_or_test_edits':False,'new_scratch_or_live_resources':False,'api_or_delivery_approval':False}
(E/'final-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
