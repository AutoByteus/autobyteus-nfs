from pathlib import Path
import hashlib,json,subprocess
E=Path(__file__).parent;T=E.parent.parent;N=T.parent.parent.parent;S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
A=T/'evidence/api-e2e/api-rev-001'; sha=lambda b:hashlib.sha256(b).hexdigest()
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args])
def aggregate(h):return sha(''.join(p+'\0'+h[p]+'\n' for p in sorted(h)).encode())
prior=json.loads((T/'code-review-evidence/crr-002/input-audit.json').read_text())
result={'review':'CRR-003','entry':'Successful API/E2E test-code review','result':'Not Applicable','reason':'API authored no production or durable-test change; current cumulative implementation tests remain those covered by CRR001/002.'}
result['current_heads']={k:git(p,'rev-parse','HEAD').decode().strip() for k,p in [('N',N),('S',S)]}
result['input_identity']={}
for key,p in [('N',N),('S',S)]:
 names=[f for f in git(p,'ls-files','-z').decode().split('\0')[:-1] if not f.startswith('tickets/')]
 h=aggregate({f:sha((p/f).read_bytes()) for f in names})
 assert h==prior['repositories'][key]['current_aggregate_sha256']
 result['input_identity'][key]={'count':len(names),'sha256':h,'unchanged_since_source_review':True}
assert git(S,'status','--porcelain')==b''
delta=git(N,'diff','--name-only','62f7b3933b4ec040b50f2ac12c333b2a9f23b459','HEAD').decode().splitlines()
assert all(f.startswith(str(T.relative_to(N))+'/') for f in delta)
result['API_delta']={'N_ticket_artifacts_changed':len(delta),'outside_ticket_changes':[],'S_changed_paths':[],'new_durable_test_paths':[]}
for name,h in prior['authority_files_unchanged'].items():assert sha((T/name).read_bytes())==h
report=(T/'code-review-report.md').read_bytes(); result['source_report_sha256']=sha(report)
assert report==git(N,'show','62f7b3933b4ec040b50f2ac12c333b2a9f23b459:'+str((T/'code-review-report.md').relative_to(N)))
summary=json.loads((A/'execution-summary.json').read_text());final=json.loads((A/'final-checks.json').read_text());clean=json.loads((A/'cleanup.json').read_text());archive=json.loads((A/'archive-integrity.json').read_text())
assert final['final_result']=='Pass' and not final['source_mismatches'] and not final['production_and_durable_test_changes']
assert len(final['all_final_cases_pass'])==11 and not archive['mismatches']
assert not clean['source_mismatches'] and not clean['protected_changes'] and not clean['owned_process_matches']
assert all(x['removed'] and not Path(x['path']).exists() for x in clean['removed'])
result['API_owned_verdict']={'revision':'API-REV-001','result':final['final_result'],'confidence':final['confidence'],'cases':final['all_final_cases_pass']}
result['execution_summary_inspected']={k:v['summary'] for k,v in summary['vitest'].items()}
result['go_counts']=summary['go'];result['python_counts']=summary['python']
result['raw_success_log_tail_checks']={}
for name,needles in {'consumer-unit-confirm':['1198 passed','6 skipped'],'consumer-routes':['39 passed'],'consumer-path-pty':['17 passed'],'consumer-guide-confirm':['24 passed'],'consumer-fixture-confirm':['86 passed']}.items():
 text=(A/(name+'.log')).read_text()
 assert all(x in text for x in needles),(name,needles)
 result['raw_success_log_tail_checks'][name]=needles
result['no_workflow_rerun']=True;result['new_resources']=False;result['cleanup_receipt_verified_paths_absent']=True
protected=[p for p in git(N,'ls-files','-z').decode().split('\0')[:-1] if p.startswith(str(T.relative_to(N))+'/') and p!=str((T/'code-review-revision-record.md').relative_to(N))]
result['protected_ticket_inputs']={'count':len(protected),'sha256':aggregate({p:sha((N/p).read_bytes()) for p in protected})}
result['history_before_sha256']=sha((T/'code-review-revision-record.md').read_bytes())
(E/'package-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['execution_summary_inspected','go_counts','python_counts']},indent=2))
