from pathlib import Path
import json,subprocess,hashlib,shutil
N=Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs');T=N/'tickets/done/extract-autobyteus-nfs';E=T/'evidence/api-e2e/api-rev-003';E.mkdir()
def git(*a):return subprocess.check_output(['git','-C',str(N),*a],text=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
assert not git('status','--porcelain').strip()
paths={p:h(N/p) for p in git('ls-files').splitlines() if not p.startswith('tickets/') and (N/p).is_file()}
changed=git('diff','--name-only','56c0c59','HEAD','--',':!tickets').splitlines();assert changed==['internal/setup/hosted_config_test.go'],changed
(E/'fixture.diff').write_text(git('diff','56c0c59','HEAD','--',changed[0]))
prior=json.loads((T/'evidence/api-e2e/api-rev-002/input-audit.json').read_text())
old_diff=[p for p,v in prior['N']['paths'] if paths.get(p)!=v]
assert old_diff==['RELEASE.md','internal/setup/hosted_config_test.go'],old_diff
own={'api-e2e-coverage-investigation.md','api-e2e-execution-coverage-report.md','api-e2e-test-case-ledger.md','api-e2e-revision-record.md'}
protected={str(p.relative_to(N)):h(p) for p in T.rglob('*') if p.is_file() and p.name not in own and not p.is_relative_to(E)}
cache={str(p.relative_to(N)):h(p) for p in (N/'scripts/tests/__pycache__').glob('*') if p.is_file()}
D0=Path('/Users/normy/autobyteus_org/autobyteus-nfs');pm={str(p):h(p) for p in (D0/'task-plans').rglob('*') if p.is_file()}
d0={k:subprocess.check_output(['git','-C',str(D0),*v],text=True).strip() for k,v in [('head',['rev-parse','HEAD']),('branch',['symbolic-ref','HEAD'])]}
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs');assert not S.exists()
write('input-audit.json',dict(N_head=git('rev-parse','HEAD').strip(),candidate='09cac96225fe4f36fb0dcbe6ddec01248992874f',runtime='83726b27400b405a7a6a79bd962d8e2419daa561',inputs=paths,delta_from_blocker=changed,delta_from_API002=old_diff,protected_ticket=protected,ignored_cache=cache,PM=pm,D0=d0,S_retired=True))
write('carry-validity.json',dict(N_count=len(paths),N_unchanged_since_blocker=len(paths)-1,runtime_workflow_pins_unchanged=True,API002_delta=old_diff,RELEASE='DR002 prose-only sync, not still pending',S='API002 executed S60b67; DR002 docs9b72 tree-equal final personal55bff. No new S impact or recreation.',N01='Rerun native Linux and Darwin; no prior native Linux API Pass inferred',N02='Fresh native Linux/Darwin packaging/hash/refusal checks; existing container installer skips explicit',N03='Fresh native build/version; old four-target/actual arm64 engine compile carries (source unchanged)',previous_hosted='39097778705/39097779223 failed/cancelled, not closed locally',completed_targets=json.loads((T/'delivery-evidence/dr-002/finalization.json').read_text())))
plan='''# API-REV-003 — archived fixture recovery plan (before execution)

Task extract-autobyteus-nfs; canonical tickets/done/extract-autobyteus-nfs. Trigger CRR007 source Pass100 / IR005 / DR002 Blocked. R2/SR003 Approved, SR004 Ready/ARCH002, Large/High/Reviewed. Runtime83726b unchanged; current fixture09cac962; intake d32309d. Prior API002 Pass95 is local/exact-input evidence, not hosted Linux qualification.

Read full current upstream handoff/review/history/DR002 and preserved requirements/investigation/design/solution history/supplement/ARCH002 basis; no authority change. N AGENTS/TESTING/DESIGN/README/go.mod/ci.yml; actual hosted fixture, Status/Detach/VerifyGanesha and mount-observation/Unmount paths. No closer instructions. Legacy/Compatibility/Persisted Data: host-only direct reader and bounded refusal remain, no migration, app binding or nil-client fallback.

Linux Mounts reads /proc/self/mountinfo, not Darwin Runner. Old runner-only trap let valid config reach later unrelated effects. Current fixture verifies existing proc mount read-only then stops at actual source mismatch/unrelated-unmount refusal. Invalid Status config must fail verification/ENOENT, not a later error. Retry and Apple/connect controls preserve bytes and absence. No root/proc-write/live-mount bypass, no Linux skip. Existing tests now Still Valid; no API durable edit needed. No additional supported scenario uncovered. IR005 baseline/mutant execution is attributed to Implementation, not our Pass.

| Case | Last exact proof | Impact / expected result |
|---|---|---|
| E01 | API002 input audit | Fresh current108 inputs;107 unchanged from blocker, only fixture; RELEASE prose from DR002 is only other delta from API002. Protect archived authorities/history, D0/PM and existing ignored cache |
| N01-L | No prior API native Linux run; IR005 evidence inspected | Required fresh native Linux arm64 nonroot Ubuntu24.04 container; focused TestHostedConfig first, then race all7packages/vet; actual proc path, no later effects |
| N01-D | API001 Darwin source83726 / old fixture | Rerun changed hosted-config + no-live-source-detach, all race/vet on native Darwin arm64 |
| N02 | API001 root packaging/refusal | Fresh Python/Bash/sourcehash/refusal on both OSes; container-only skips not Pass. actionlint/workflow unchanged carries |
| N03 | API001 compile/real arm64 artifact | Fresh native build/version on Linux/Darwin; four-target/engine manifest/embed unchanged carries; no new engine or platform qualification |
| N04 | IR005 three mutants | Fresh isolated Linux controls: omit Status preflight, omit Detach preflight, reject missing partial-detach config; expect assertion failures, not compile failures |
| S01–06 | API002 S60b67 | Still Valid; no S impact, DR002 docs-only finalization/tree receipt; no S worktree recreation/rerun |
| E02 | Prior scratch receipts | Fresh own development-container/scratch cleanup, source/protected bytes and no-owned-process/cwd proof |

Prepare independent exact N archive under own home scratch; official SHA-verified Go1.27.2 Darwin/Linux arm64 toolchains; private HOME/TMPDIR/cache. Linux immutable pinned Ubuntu24.04 image, own named development container, no host Docker socket/ports/privileged caps; apt compiler/python only inside it. Tests UID1001 with clean env. Darwin nonroot host, independent source/private env. Both may run concurrently as separate personally owned OS processes; builds serialize per copy. No installed CLI lifecycle invocation, live storage daemon, proc mutation, paid provider or user app. Preserve IR005 wrong-root attempt and baseline/mutant logs historically; no blind baseline rerun needed because independently established cause is exact fixture delta.

Broader native Linux execution REQUIRED to close previous runner/mock gap; selected development container, not VM/storage campaign. Reassess after execution. Native Linux arm64 is not hosted Ubuntu amd64, Mac cancelled jobs remain cancelled; Delivery owns fresh current hosted CI and terminal receipts. No target fetch/push/merge/reset/finalization/release/TaskDone/Terminal/user verification. Completed paired pushes stand; D0 now populated, S retired, stale RELEASE prose already fixed. User wants NO RELEASE.
'''
(E/'validation-plan.md').write_text(plan)
p=T/'api-e2e-coverage-investigation.md';p.write_text('# Current API-REV-003 investigation — in progress\n\n'+plan+'\n## API002 investigation (historical)\n'+p.read_text())
p=T/'api-e2e-test-case-ledger.md';p.write_text(p.read_text()+'\n## API-REV-003 pre-execution impact plan\n\n'+plan+'\n## API-REV-003 Execution Events\n| UTC | Case | Event | Observation | Result | Evidence |\n|---|---|---|---|---|---|\n')
p=T/'api-e2e-execution-coverage-report.md';p.write_text('# API-REV-003 in progress\n\nAffected native N fixture validation planned before execution in evidence/api-e2e/api-rev-003/validation-plan.md. No new API verdict yet. Canonical archived path; DR002 Blocked and completed pushes preserved. S no impact; old report below is historical (stale RELEASE task was resolved by DR002).\n\n'+p.read_text())
shutil.copy2('/tmp/init-nfs-api003.py',E/'initialize.py')
print(E, len(paths), len(protected),len(pm))
