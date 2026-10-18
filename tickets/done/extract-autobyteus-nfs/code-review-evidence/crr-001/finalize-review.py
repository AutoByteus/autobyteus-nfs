from pathlib import Path
import json,subprocess,hashlib,difflib,datetime,re
E=Path(__file__).resolve().parent;N=E.parents[4];T=E.parents[1]
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
def git(r,*a):return subprocess.check_output(['git','-C',str(r),*a]).decode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((E/'source-audit.json').read_text())
p='.github/workflows/release-nfs.yml';before=git(S,'show','3712cd9b:'+p);after=(N/p).read_text()
plus=minus=0
for line in difflib.unified_diff(before.splitlines(),after.splitlines(),n=0):
    if line.startswith('+') and not line.startswith('+++') and line[1:].strip():plus+=1
    if line.startswith('-') and not line.startswith('---') and line[1:].strip():minus+=1
row={'repo':'N','path':p,'beforeNonblank':sum(bool(x.strip()) for x in before.splitlines()),'afterNonblank':sum(bool(x.strip()) for x in after.splitlines()),'addedNonblank':plus,'removedNonblank':minus}
row.update(over500Grown=row['afterNonblank']>500 and row['afterNonblank']>row['beforeNonblank'],deltaOver220=plus+minus>220)
d['sourceSizes']=[x for x in d['sourceSizes'] if (x['repo'],x['path'])!=('N',p)]+[row]
assert not any(x['over500Grown'] or x['deltaOver220'] for x in d['sourceSizes'])
(E/'source-audit.json').write_text(json.dumps(d,indent=2)+'\n')
lines=['# Source size and responsibility audit','', 'Base: S3712cd9bf0db998501d162db7f8655f169e3def6, with predecessor embedded paths mapped into N. Counts are nonblank lines; delta is nonblank additions plus removals after only Go module-prefix normalization. Tests, fixture data, evidence, docs and EN/zh translation payloads are not source-size targets. Unchanged relocated owners are included for transparency. No file requires a size-driven split. CR-001 is the separate unused-import finding.','', '| Repo / source file | Before | After | Added + removed | >500 check | >220 delta | SoC / placement | Action |','| --- | --- | --- | --- | --- | --- | --- | --- |']
for x in sorted(d['sourceSizes'],key=lambda x:(x['repo'],x['path'])):
    lines.append(f"| {x['repo']}/{x['path']} | {x['beforeNonblank']} | {x['afterNonblank']} | {x['addedNonblank']} + {x['removedNonblank']} | Pass | Pass | Pass — existing concrete owner | None for size |")
(E/'source-size-audit.md').write_text('\n'.join(lines)+'\n')
baseline=json.loads((E/'input-identities.json').read_text());changes=[]
for repo,key in [(N,'Nfiles'),(S,'Sfiles')]:
    for p,h in baseline[key].items():
        if not (repo/p).is_file() or sha(repo/p)!=h:changes.append(str(repo/p))
assert not changes,changes
up=json.loads((T/'implementation-evidence/ir-001/package-index.json').read_text())
assert all(sha(N/x['path'])==x['sha256'] for x in up['files'])
cleanups=[]
for p in [E/'cleanup.json',E/'attempt-1/cleanup.json']:
    c=json.loads(p.read_text());assert c['removed'] and not Path(c['ownedScratch']).exists();cleanups.append(c)
checks=json.loads((E/'checks-result.json').read_text());assert all(x['exit']==x['expected'] for x in checks)
assert len(json.loads((E/'unused-imports.json').read_text())['diagnostics'])==5
report=(T/'code-review-report.md').read_text()
broken=[]
for link in re.findall(r'\]\(([^)]+)\)',report):
    if '://' not in link and not (T/link.split('#')[0]).exists():broken.append(link)
assert not broken,broken
assert '| 10 | Cleanup Completeness | **8.8**' in report
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'NHead':git(N,'rev-parse','HEAD').strip(),'SHead':git(S,'rev-parse','HEAD').strip(),'unchangedNonTicketInputs':{k:len(baseline[k]) for k in ['Nfiles','Sfiles']},'upstream132HashChecks':len(up['files']),'sourceSizeRows':len(d['sourceSizes']),'brokenReportLinks':broken,'ownedScratchAbsent':True,'NTrackedDiff':git(N,'diff','--name-only'),'STrackedDiff':git(S,'diff','--name-only'),'reviewDecision':'Fail','classification':'Local Fix','finding':'CR-001','score':98.8}
(E/'final-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
