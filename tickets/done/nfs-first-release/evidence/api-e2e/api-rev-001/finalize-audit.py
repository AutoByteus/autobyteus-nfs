from pathlib import Path
import json,hashlib,subprocess,datetime,re
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((E/'input-audit.json').read_text());out={}
for key in ['source','protected_ticket']:
 bad=[p for p,h in a[key].items() if not (N/p).is_file() or sha(N/p)!=h]
 out[key+'Count']=len(a[key]);out[key+'Mismatches']=bad
 assert not bad,(key,bad)
# Preserve the concurrently authored Delivery documents exactly, without staging them.
own_names=['api-e2e-coverage-investigation.md','api-e2e-execution-coverage-report.md','api-e2e-test-case-ledger.md','api-e2e-revision-record.md']
delivery_names=['docs-sync-report.md','handoff-summary.md','release-deployment-report.md','delivery-revision-record.md']
external=[T/n for n in delivery_names if (T/n).is_file()]+[p for p in (T/'delivery-evidence').rglob('*') if p.is_file()]
out['concurrentDeliveryFiles']={str(p.relative_to(N)):sha(p) for p in external}
scratch=json.loads((E/'scratch.json').read_text());out['initialScratchRecord']=scratch
out['localCleanup']=json.loads((E/'cleanup-local.json').read_text())
assert out['localCleanup']['scratch_removed'] and not Path(out['localCleanup']['scratch']).exists()
probe=json.loads((E/'mac-array-reproduction.json').read_text());assert probe['scratchAbsent'] and not Path(probe['scratch']).exists()
out['arrayScratchAbsent']=True;out['ownedContainersCreated']=0;out['ownedMountedStorageCreated']=0
processes=subprocess.check_output(['ps','-axo','pid=,command='],text=True)
out['runningOwnedMonitors']=[l for l in processes.splitlines() if str(E/'monitor-hosted.py') in l and re.search(r'python\S* .*monitor-hosted.py',l)]
assert not out['runningOwnedMonitors']
f=json.loads((E/'hosted-final.json').read_text());out['runId']=f['run']['id'];out['runAttempt']=f['run']['run_attempt'];out['runConclusion']=f['run']['conclusion'];assert out['runConclusion']=='failure'
out['jobCounts']={s:sum(j['conclusion']==s for j in f['jobs']['jobs']) for s in ['success','failure','skipped','cancelled']}
out['noCompleteCandidate']=not any(x['name']=='nfs-release-candidate' for x in f['artifacts']['artifacts']);assert out['noCompleteCandidate']
out['retainedRemoteArtifacts']=[dict(id=x['id'],name=x['name'],digest=x['digest'],expiresAt=x['expires_at'],size=x['size_in_bytes']) for x in f['artifacts']['artifacts']]
out['retentionLimit']='Partial failed-attempt build artifacts only. Not qualified, no complete candidate, no successful envelope. Kept on Actions, no local download; expiry authoritative.'
ledger=(T/'api-e2e-test-case-ledger.md').read_text();rows=[l for l in ledger.splitlines() if re.match(r'\| (?:R0[1-4]|Q\d{2}-\d{2}|U01|D01|D02|C01) \|',l) and not l.startswith('| 2026')]
out['ledgerPlannedRows']=len(rows);assert len(rows)==50
out['ledgerFinalStates']={s:sum(l.split('|')[3].strip().startswith(s) for l in rows) for s in ['Pass','Fail','Blocked','Not Tested']};assert out['ledgerFinalStates']=={'Pass':3,'Fail':1,'Blocked':43,'Not Tested':3}
# Broad credential pattern check within OWN evidence only, no private configuration search.
patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
hits=[]
for p in E.rglob('*'):
 if not p.is_file() or p.name=='finalize-audit.py':continue
 text=p.read_text(errors='replace')
 if any(re.search(rx,text) for rx in patterns):hits.append(str(p.relative_to(E)))
out['credentialPatternFiles']=hits;assert not hits
out['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip();out['productAndDurableChangesByAPI']=[];out['pass']=True
(E/'final-checks.json').write_text(json.dumps(out,indent=2)+'\n')
index={'canonical':{n:sha(T/n) for n in own_names},'evidence':{str(p.relative_to(E)):sha(p) for p in E.rglob('*') if p.is_file() and p.name!='package-index.json'},'route':'Failure-origin review only; no legacy cumulative references forwarded','result':'Fail62.86%'}
(E/'package-index.json').write_text(json.dumps(index,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['concurrentDeliveryFiles','retainedRemoteArtifacts','localCleanup','initialScratchRecord']},indent=2))
