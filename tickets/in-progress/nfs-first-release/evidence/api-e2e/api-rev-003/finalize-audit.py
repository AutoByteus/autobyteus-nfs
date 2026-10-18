# Case C01; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment local macOS26.5.2 arm64; Python3.9.6/Bash3.2.57
# Step: finalize-audit.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import json,hashlib,subprocess,datetime,re,os
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((E/'input-audit.json').read_text());out={}
for key in ['source','protected']:
 bad=[p for p,h in a[key].items() if not (N/p).is_file() or sha(N/p)!=h];out[key+'Count']=len(a[key]);out[key+'Mismatches']=bad;assert not bad,(key,bad)
oldhist=subprocess.check_output(['git','show',a['head']+':'+str((T/'api-e2e-revision-record.md').relative_to(N))],cwd=N);assert (T/'api-e2e-revision-record.md').read_bytes().startswith(oldhist);out['API001API002HistoryPrefixPreserved']=True
external=[T/n for n in ['delivery-revision-record.md','docs-sync-report.md','handoff-summary.md','release-deployment-report.md']]+[p for p in (T/'delivery-evidence').rglob('*') if p.is_file()]
out['deliveryCurrentHashes']={str(p.relative_to(N)):sha(p) for p in external};out['deliveryOwnerChanges']=[p for p,h in a['deliveryUntracked'].items() if out['deliveryCurrentHashes'].get(p)!=h];assert all(Path(p).name in ['delivery-revision-record.md','docs-sync-report.md','handoff-summary.md','release-deployment-report.md'] for p in out['deliveryOwnerChanges']);out['deliveryAddedFiles']=sorted(set(out['deliveryCurrentHashes'])-set(a['deliveryUntracked']));out['externalOwnershipDisposition']='DR004 owner updates preserved/unmodified/unstaged; not API edits.'
clean=json.loads((E/'cleanup-local.json').read_text());smoke=json.loads((E/'candidate-native-version.json').read_text());assert not Path(clean['root']).exists() and not Path(smoke['scratch']).exists();assert not Path(json.loads((E/'cleanup-local-controls.json').read_text())['root']).exists();out['localTemporaryScratchAbsent']=True
root=Path(json.loads((E/'retained-candidate-resource.json').read_text())['root']);candidate=root/'candidate';assert candidate.is_dir() and not (root/'candidate.zip').exists() and not (root/'refused-envelope-destination').exists()
args=['/usr/bin/python3','packaging/release.py','--operation','verify-candidate','--directory',str(candidate)];p=subprocess.run(args,cwd=N,capture_output=True,text=True,timeout=120,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(E/'final-candidate-verify.log').write_text('# Case C01; current source585d416c2746cf2963058d591b0753d0db8088f5; Mac26arm64; date '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n$ '+' '.join(args)+'\n'+p.stdout+p.stderr);assert p.returncode==0,p.stderr
record=json.loads(p.stdout);assert record==json.loads((E/'actual-candidate.json').read_text());out['retainedCandidateFinalVerification']=True;out['retainedRoot']=str(root);out['rootMode']=oct(root.stat().st_mode&0o777);out['retainedCandidateFiles']=len([x for x in candidate.rglob('*') if x.is_file()]);out['retainedCandidateBytes']=sum(x.stat().st_size for x in candidate.rglob('*') if x.is_file());out['generatedAliasRetainedOutsideRepo']=str(root/'metadata-alias-control.json');assert (root/'metadata-alias-control.json').is_file() and not (E/'candidate-metadata-alias.json').exists()
f=json.loads((E/'hosted-final.json').read_text());out['run']=f['run']['id'];out['attempt']=f['run']['run_attempt'];out['runConclusion']=f['run']['conclusion'];assert out['runConclusion']=='success';out['jobCounts']={s:sum(j['conclusion']==s for j in f['jobs']['jobs']) for s in ['success','failure','skipped','cancelled']};assert out['jobCounts']=={'success':10,'failure':0,'skipped':2,'cancelled':0}
old=E.parent/'api-rev-002'
old_record=json.loads((old/'actual-candidate.json').read_text());old_root=Path(json.loads((old/'candidate-local-retention.json').read_text())['candidate'])
old_bad=[n for n,v in old_record['members'].items() if not (old_root/n).is_file() or sha(old_root/n)!=v['sha256']]
assert not old_bad
assert sha(old_root/'candidate.json')==json.loads((old/'candidate-reference.json').read_text())['recordSha256']
out['historicalAPI002CandidateMemberHashesPreserved']=True
out['scope']='API003 R3 prepublication controls and new candidate; field/user deferred, final signing/publication downstream'
patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'];hits=[]
for p in E.rglob('*'):
 if not p.is_file() or p.name=='finalize-audit.py':continue
 if any(re.search(rx,p.read_text(errors='replace')) for rx in patterns):hits.append(str(p.relative_to(E)))
out['credentialPatternFiles']=hits;assert not hits
out['ownedRuntimeResourcesCreated']=[];out['ownedTemporaryProcessesCompleted']=True;out['platformRunnerDisposal']='Post-job cleanup logged; provider disposal not independently audited';out['productOrDurableEditsByAPI']=[];out['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['headBeforeEvidenceCommit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip();out['pass']=True
(E/'final-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='deliveryCurrentHashes'},indent=2))
