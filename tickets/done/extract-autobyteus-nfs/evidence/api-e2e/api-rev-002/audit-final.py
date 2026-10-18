from common import *
import hashlib,re,shutil
p=T/'api-e2e-revision-record.md';s=p.read_text();row='| API-REV-002 | CRR005 Pass after IR003/IR004/DR001 integrated recovery | R2/SR003, SR004/ARCH002, IR003/004, CRR004/005 | API001 Pass95 at Sa2023 | Pass /95.00% at S60b67 |\n'
if row not in s:
 at=s.index('\n\n## API-REV-001');s=s[:at]+'\n'+row.rstrip('\n')+s[at:];p.write_text(s)
old=subprocess.check_output(['git','-C',str(N),'show','HEAD:'+str(p.relative_to(N))])
entry=old[old.index(b'## API-REV-001'):]
assert entry in p.read_bytes()
audit=json.loads((E/'input-audit.json').read_text());mismatches={}
for label,root in [('N',N),('S',S)]:
 mismatches[label]=[p for p,h in audit[label]['paths'] if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
assert not any(mismatches.values())
assert subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip()==audit['S']['head']
assert not subprocess.check_output(['git','-C',str(S),'status','--porcelain'],text=True).strip()
summary=json.loads((E/'execution-summary.json').read_text());assert len(summary['checks'])==15 and all(c['pass_'] for c in summary['checks'])
assert not Path(summary['cleanup']['scratch']).exists()
allowed={str((T/n).relative_to(N)) for n in ['api-e2e-coverage-investigation.md','api-e2e-execution-coverage-report.md','api-e2e-revision-record.md','api-e2e-test-case-ledger.md']}
changed=subprocess.check_output(['git','-C',str(N),'diff','--name-only','HEAD'],text=True).splitlines()
assert all(p in allowed or p.startswith(str(E.relative_to(N))+'/') for p in changed),changed
for f in E.rglob('__pycache__'):shutil.rmtree(f)
# Focused index, not a retransmission of old cumulative manifests.
critical=['validation-plan.md','carry-validity.json','source-contract-audit.json','execution-summary.json','commands.jsonl','test-counts.json','cleanup.json','test-review-scope.md','consumer-narrow.log','consumer-unit.log','consumer-integration.log','consumer-core.log','consumer-routes.log','consumer-path-pty.log','consumer-guide.log','consumer-launcher.log']
write('package-index.json',dict(revision='API-REV-002',source=audit['S']['head'],canonical=[str(T/n) for n in sorted(Path(v).name for v in allowed)],critical=[dict(path=str(E/n),sha256=hashlib.sha256((E/n).read_bytes()).hexdigest()) for n in critical],carried_evidence='../api-rev-001; original N proof linked in AC table with fresh108-input equality',upstream='CRR005/IR004/IR003, R2/SR003/SR004/ARCH002; no authoritative source/design edit'))
write('final-checks.json',dict(pass_=True,current_commands=15,failed_commands=0,fresh_case_groups=8,carried_case_groups=3,confidence=95.0,critical_API_criteria_proven=True,AC007='Delivery-owned not executed',source_mismatches=mismatches,prior_API001_entry_exact=True,S_clean=True,owned_scratch_absent=True,production_changes=[],durable_test_changes=[],N_tracked_changes=changed,selected_recipient='/software_engineering_team/code_reviewer'))
print('final audit Pass')
