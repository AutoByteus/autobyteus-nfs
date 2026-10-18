from pathlib import Path
import subprocess,json,hashlib,datetime,shutil
N=Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs');S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs');T=N/'tickets/in-progress/extract-autobyteus-nfs';E=T/'evidence/api-e2e/api-rev-002';E.mkdir()
E1=E.parent/'api-rev-001'
def git(r,*a):return subprocess.check_output(['git','-C',str(r),*a],text=True)
def write(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
audit={}
for label,r in [('N',N),('S',S)]:
 assert not git(r,'status','--porcelain').strip()
 paths=[(p,hashlib.sha256((r/p).read_bytes()).hexdigest()) for p in git(r,'ls-files').splitlines() if not p.startswith('tickets/') and (r/p).is_file()]
 audit[label]=dict(root=str(r),head=git(r,'rev-parse','HEAD').strip(),paths=paths)
write('input-audit.json',audit)
old=json.loads((E1/'input-audit.json').read_text())
assert audit['N']['paths']==[tuple(p) for p in old['N']['paths']]
authorities=['requirements-doc.md','investigation-notes.md','solution-revision-record.md','design-spec.md','user-filesystem-boundary-correction.md','solution-design-handoff.md','design-review-report.md','architecture-review-revision-record.md']
changes=git(N,'diff','--name-only','77a1c29749583a18cf5b1e061ff99015c88202e9','HEAD','--',*[str(p.relative_to(N)) for p in [T/x for x in authorities]])
assert not changes.strip(),changes
write('carry-validity.json',dict(N_inputs=len(audit['N']['paths']),N_all_exact_API001=True,unchanged_authorities=authorities,N_service='83726b27400b405a7a6a79bd962d8e2419daa561',N_cases=['N01','N02','N03'],original_evidence='../api-rev-001',S_previous=old['S']['head'],S_current=audit['S']['head'],S_cases='ALL S01-S06 Rerun: changed core/contracts/harness/fixtures; API001 does not prove integrated S'))
(E/'integrated-changed-paths.txt').write_text(git(S,'diff','--name-only',old['S']['head'],'HEAD'))
(E/'manager-integration.diff').write_text(git(S,'diff',old['S']['head'],'HEAD','--','autobyteus-server-ts/src/agent-execution/services/agent-run-manager.ts'))
for p in ['common.py','audit-source.py']:shutil.copy2(E1/p,E/p)
plan='''# API-REV-002 current integrated validation plan

Planned before execution 2026-10-18. Trigger CRR005 Pass100 after IR003/IR004/DR001.
Last API001 S:a2023feff3d498fb6c51cebf1c93360da3679a45; current S:60b67dabecaf5569a8e26128dbdb26117c988811.
N service83726b unchanged: all108 non-ticket tracked inputs match API001; eight authority documents unchanged.
Current S TESTING.md shared-foundation rule invalidates all six recorded S groups after core/contracts/test harness/fixture integration. Complete diff: integrated-changed-paths.txt.

| Case | Last validated | Decision / expected result |
|---|---|---|
| E01 | API001 N83726/Sa2023 | Rerun current removal/license/Guide equality and source/authority audit; no coupling restored |
| N01 | API001 N83726 | Still Valid: all independent N inputs exact; Go race/vet/locked refusal with original privileged-double limits |
| N02 | API001 N83726 | Still Valid: independent packaging/hash/workflow/refusal,19 Python pass/1 child skip |
| N03 | API001 N83726 | Still Valid: four-target compile/native version/actual arm64 embed; no runtime qualification |
| S01 | API001 Sa2023 | Rerun: clean frozen whole-workspace install, current integration:prepare/typecheck, Nuxt prepare |
| S02 | API001 Sa2023 | Rerun:7 private-profile/path/process suites; first affected Claude/Codex/Brief overlap integration controls |
| S03 | API001 Sa2023 | Rerun and broaden: all agent-execution/workspace/terminal/Codex/memory/skill-notice units; core input-preface/collector/pipeline and Brief/skill-notice integration |
| S04 | API001 Sa2023 | Rerun:3 composed API suites, actual HTTP/GraphQL/inject bytes/MIME/ordinary skill/profile paths |
| S05 | API001 Sa2023 | Rerun:3 run/memory/native PTY/WebSocket suites; current built core/runtime, DummyLLM only |
| S06 | API001 Sa2023 | Rerun: launcher/4 Guide suites/bothguards; Guide visual sources byte-exact so IR001 rendered proof remains attributed only to component presentation |
| E02 | API001 prior scratch | Rerun: own fresh archive/process cleanup; current source/fixtures/protected data unchanged |

Applicable discovery: N AGENTS/TESTING/DESIGN/README; S AGENTS/TESTING/DESIGN, server and web AGENTS/README, package scripts/vitest config; no closer TESTING overrides. Current source/harness read for actual API removal lifecycle, run memory fixture, private owner and native PTY paths.
Durable test decisions: current R2 coverage Still Valid, no edit planned. Post-merge cleanup removes only obsolete unused test inputs/imports, assertions remain. No missing approved case requires a new test/probe. Read Legacy/Compatibility/Persisted transition in handoff: unchanged direct host-only reader + bounded refusal; no migration or compatibility bridge.

Prepare a single own canonical home scratch with exact current tracked S bytes (root tickets excluded EXCEPT11 known replay fixtures restored upfront), private HOME/TMPDIR/store, explicit Node22 PATH, no inherited credentials/provider gates. Never consume assigned-worktree old dist. Serialize all builds/tests. No N scratch/toolchain/engine campaign. No VM/Docker/mount/installed application/provider/remote action. Record cases immediately. No prior Pass is a fresh run; Implementation1666/21/15/24/34 and overlapping76 are inspected, not counted as our executions.

Confidence and broader decision pending execution. Repository native process/API/PTY surfaces are selected to prove actual changed boundary; not an end-user desktop or storage qualification journey. No additional browser/VM/paid-provider campaign expected if these pass and no material gap emerges. No old filesystem/editor Task reopened. AC007/fresh-ref ordered finalization and stale S RELEASE R1 tail remain Delivery-owned.
'''
(E/'validation-plan.md').write_text(plan)
p=T/'api-e2e-coverage-investigation.md';p.write_text('# Current Round — API-REV-002 (in progress)\n\n'+plan.split('\n',1)[1]+'\n## Prior API001 investigation and decisions (historical)\n\n'+p.read_text())
p=T/'api-e2e-test-case-ledger.md';p.write_text(p.read_text()+'\n## API-REV-002 pre-execution impact plan\n\n'+plan.split('Applicable discovery:')[0]+'\n## API-REV-002 Execution Events\n| Time UTC | Case | Event | Observation | Result | Evidence |\n|---|---|---|---|---|---|\n')
p=T/'api-e2e-execution-coverage-report.md';p.write_text('# API-REV-002 execution in progress\n\nCurrent integrated S60b67 validation planned in evidence/api-e2e/api-rev-002/validation-plan.md. All S01–06 Rerun; N01–03 carried only after108-input equality. No current integrated API result assigned yet. Prior authoritative result below applies only to its exact inputs. DR001 remains Delivery-owned.\n\n'+p.read_text())
shutil.copy2('/tmp/init-api002.py',E/'initialize.py')
print(E);print({k:(v['head'],len(v['paths'])) for k,v in audit.items()})
