from common import *
summary=json.loads((E/'execution-summary.json').read_text());assert summary['result']=='Pass' and summary['cleanup']['pass_']
(T/'api-e2e-coverage-investigation.md').write_text('''# API/E2E Coverage Investigation

## Current round, authority and archived location
API-REV-003, extract-autobyteus-nfs / project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8. **Large / High / Reviewed**. Personal execution, no delegation.
Canonical ticket: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs/tickets/done/extract-autobyteus-nfs. Archive does not mean terminal completion. N recovery branch codex/extract-autobyteus-nfs; intake d32309db1d938a7d975c0f1a06b15f9c74624b0b, test candidate09cac96225fe4f36fb0dcbe6ddec01248992874f, runtime83726b27400b405a7a6a79bd962d8e2419daa561 unchanged.
Trigger CRR007 source Pass100 after IR005 / DR002 native Linux fixture Local Fix. Read current implementation/review/Delivery handoffs, history and finalization receipts, existing API investigation/report/ledger/history, and full approved requirements/investigation/design/solution/supplement/ARCH002 basis. Eight authorities byte-exact to API002 (authority-audit.json). Approved R2/SR003, Ready SR004/ARCH002 unchanged; no behavioral revision.
DR002 already pushed N main/ticket22e934b first and S9b72c8d1→personal55bff1f5 (--no-ff/tree-equal), populated D0/kept PM, retired S worktree and corrected stale R1 RELEASE prose. Do not repeat those operations or resurrect the docs item. DR002 remains Blocked on fresh hosted verification/terminal receipts; user wants NO RELEASE.

## Investigation, changed boundary and test validity
Only internal/setup/hosted_config_test.go differs from blocker56c0c59; other107 N inputs identical. Compared with API002 N input: only this fixture and Delivery's RELEASE prose differ. Production, workflows, private-config trust policy, source hash, engine pins/license/CLA remain unchanged. S has no impact; its worktree remains absent, API002 S evidence carries exactly within prior limits.
Reviewed actual Service.Status/Detach -> CheckConfiguration -> VerifyGanesha/VerifyGaneshaForDetach -> platform Mounts/Observe/Matches/Unmount -> later job/package/engine paths. Linux Mounts reads /proc/self/mountinfo directly, bypassing the Darwin Runner trap. The old fixture's absent default target allowed later trust refusal or deliberately incomplete Docker-client panic; IR005 native baseline proof and CRR007 independently establish fixture origin, not a supported production defect.
Current fixture is **Still Valid**: Linux verifies an existing unrelated proc mount read-only and reaches exact source mismatch/unrelated-unmount refusal before effects; Darwin retains exactly one command error. Invalid/missing Status must specifically fail configuration verification/ENOENT. Current/missing partial-detach retry and Apple/connect controls preserve config/receipt bytes AND absent files. No Linux skip, real mount/proc write, root bypass, nil-client production fallback or new injection seam. All original supported groups retained. API durable changes: None; no uncovered supported case needs a new test. Fresh temporary mutation copies test assertion sensitivity, not product changes.
Legacy/Compatibility and Persisted transition checks remain as in preserved implementation: absent/null/empty host-only Nodes directly usable, meaningful/malformed active/pending predecessor obligations refused under existing lock before effects, no automatic migration or dual runtime. Ordinary S paths/private exact owners untouched. No old filesystem/editor/provider scenario reopened.

## Instructions and pre-execution impact plan
Read N AGENTS.md, TESTING.md, DESIGN.md, README.md, go.mod and .github/workflows/ci.yml, changed test plus forward production path. No closer AGENTS/TESTING. Project commands: go test -race, vet, build/version, Python fixtures/Bash, sourcehash/refusal, isolated root archive; no installed create/connect/detach or live resources. Prior API S TESTING and current exact prior proof remain relevant but require no rerun for this independent N fixture-only delta.
Plan and ledger written BEFORE execution: evidence/api-e2e/api-rev-003/validation-plan.md. E01 source identity/cleanup fresh; N01 rerun Linux and Darwin; N02 packaging/refusal fresh on both; N03 native builds fresh, old four-target/arm64 artifact proof carries; N04 new isolated three-mutant control. S01–06 Still Valid at API002 S60b67; no new S run/recreation. API001/002 exact results are not retroactive native Linux/hosted approval.
Setup: independent108-input archive, official SHA-verified Go1.27.2 native Darwin/Linux arm64, private HOME/TMPDIR/cache, clean test env. Linux pinned Ubuntu24.04 disposable developer container, UID1001, GCC13.3/Python3.12.3, read-only own-input mount, no host Docker socket, ports or privileged mode. Root package preparation only inside own container. Darwin UID501/clang17/Python3.9.6, current source outside protected temp hierarchy. OS copies run as personal independent processes; no shared package build outputs. No provider credentials, user app, NFS engine, mounts or remote target operations.

## Completed evidence and confidence decision
All current candidate checks pass; Linux/Darwin each7 Go packages race/vet, native builds/version, packaging/hash/refusal. Linux47 top-level214 including subtests; Darwin59/252. Linux Python17/20 executed with3 explicit skips; Darwin19/20 with1 child skip. Linux bootstrap parent intentionally container-skipped; Darwin parent exercises child. Three native Linux mutants fail intended assertions, not compilation. Focused30 Linux pass records,31 Darwin; additional no-live-source-detach test is Darwin-only and not claimed on Linux.
Native Linux broader validation was **Required and Completed** to close the runner/mock gap. After repository/native execution: all seven applicable categories95%, mean95%, none below90%; all critical API-owned ACs have direct or unchanged exact carried proof. **Further broader validation Not Required** for this bounded fixture correction: actual proc path and Darwin runner path, before-effect refusals/record preservation and mutation negatives are executed. New live storage/provider/desktop campaign would not improve the changed boundary. Hosted amd64/cancelled macOS matrix completion remains an explicitly separate Delivery gate, not inferred from local arm64.

## Attempt and cleanup correction
One API-owned cleanup attempt stopped before deletion because the guard rejected any UID1001 process, including an exited Go zombie. Diagnosis confirmed State Z/PPid1/FDSize0 in own sleep-infinity container (no init reaper), not a running product process. Preserved cleanup-attempt-1 script/log/inventory. Corrected only evidence guard to reject live checker processes and separately verify/report adopted zombies before removing the exact owned container, clearing its namespace; no suite/assertion/source change or rerun needed. Final cleanup completed, no owned host process/cwd,108 canonical/copied inputs and535 upstream artifacts/PM/ignored cache preserved, D0 populated main unchanged, S still retired.
No current candidate test failure or remaining in-scope finding. Historical IR005 wrong-root attempt/baseline failures and hosted failure/cancellation remain separately attributed. Canonical report maps all ACs and exact counts. Next proportional successful-test gate; Delivery fix-forward/hosted terminal verification after that, no release.
''')
report='''# API/E2E Execution Coverage Report

## Latest authoritative result
**API-REV-003 — Pass /95.00% (2026-10-18), affected local native N fixture validation with unchanged evidence carried.** Large / High / Reviewed. No remaining in-scope candidate failure. Nine fresh platform/case groups completed, six S groups carried; initial E02 cleanup-guard attempt retained and resolved. No API production/durable-test edit.
Native Linux fixture closure is NOT hosted CI success, release qualification or Task completion. **DR002 remains Delivery-owned Blocked** until fresh checked-candidate CI/terminal receipts. No release, target push or user verification by API.

## Canonical archived location and authority
N=/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs; ticket=N/tickets/done/extract-autobyteus-nfs. Continue in this archive, not in-progress. N branch codex/extract-autobyteus-nfs; input d32309db1d938a7d975c0f1a06b15f9c74624b0b; reviewed test candidate09cac96225fe4f36fb0dcbe6ddec01248992874f; runtime83726b27400b405a7a6a79bd962d8e2419daa561 unchanged.
R2/SR003 Approved, SR004 Ready/ARCH002 Pass; eight governing authorities byte-exact to API002. IR005 / CRR007 source Pass100 is this trigger; prior API002 Pass95 and CRR006 successful no-delta gate retain exact-input limits, not a native Linux claim. Full upstream package, prior API/history and DR002 were read. Investigation/ledger/impact plan precede execution.
**DR002 completed source operations:** N main/ticket22e934b9f2b95daf3c72a840788ee155cbd4ff6d first; S ticket9b72c8d1c8d6f7e294af2c23fb497211c67f930c→personal55bff1f5eea1f140bab6e372e3faadeb7ea33465 (--no-ff/tree-equal). D0 populated/PM preserved; S worktree retired. RELEASE R1 prose already corrected. These are carried Delivery receipt facts, not fresh remote observations or actions by API. Do not replay pushes, recreate S or reopen the docs item.

## Impact and execution identity
Only N/internal/setup/hosted_config_test.go differs from blocker56c0c59;107 other inputs equal. Compared to API002, the other change is RELEASE.md prose only. No runtime/workflow/engine/pin/license/private-config safety change. Current production source hash on BOTH OSes:
`348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e`.
E3=evidence/api-e2e/api-rev-003, E2=api-rev-002, E1=api-rev-001 under the same evidence parent. E3/validation-plan.md, input-audit.json, authority-audit.json, fixture.diff and carry-validity.json record the pre-run plan, actual delta and attribution. Old raw logs' in-progress paths are historical locations, not current canonical paths.
Exact commands/cwd/exit expectations/timing: E3/commands.jsonl / execution-summary.json.35 logged commands matched expected exits;2 publication refusals and3 mutant failures intentionally exit1. The initial cleanup guard failure is separately retained, not hidden by command success counts.

| Case | Current result | Direct evidence under E3 unless stated |
|---|---|---|
| E01 | Fresh Pass | input-audit.json, archive-integrity.json, authority-audit.json:108 exact independent inputs,107 unchanged from blocker, one fixture delta; clean native toolchains/container identity |
| N01-linux | Fresh Pass | linux-focused.log, linux-race.log, linux-vet.log: actual read-only proc observation, exact invalid-config/status/unmount-before-effects assertions;7 packages race/vet |
| N01-darwin | Fresh Pass | darwin-focused.log, darwin-race.log, darwin-vet.log: one injected command boundary, extra Darwin no-live-source detach;7 packages race/vet |
| N02-linux / N02-darwin | Fresh Pass with explicit skips | native Python/Bash/sourcehash/expected refusal logs; Linux container installer cases unexecuted, Darwin parent permission fixture executes |
| N03-linux / N03-darwin | Fresh native build/version Pass | native build/version logs: development-unqualified, no lifecycle invocation. E1 four-target and actual arm64 manifest/embed proof carries; not rerun or new qualification |
| N04 | Fresh expected-negative Pass | mutation-results.json +3 mutation logs: skipped Status verification, skipped Detach verification and overstrict missing-partial-config refusal all fail specific assertions |
| S01–06 | Carried API002 Pass, NOT rerun | E2 current S60b67 builds/path/profile/process/composed API/native PTY/Guide/launcher evidence. DR002 docs-only finalization/tree receipt; no current S impact/recreation |
| E02 | Fresh Pass after cleanup-only correction | cleanup-attempt-1, cleanup-process-diagnosis.log, cleanup-exited-children.json, cleanup.json: exact owned namespace and scratch removed, protected inputs intact |

## Acceptance-Criteria Proof
Evidence folder: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs/tickets/done/extract-autobyteus-nfs/evidence/api-e2e/api-rev-003
AC-007 is Delivery-owned and not overridden. Earlier AC identifiers without hyphens refer to the same criteria.

| AC | Direct evidence / disposition |
|---|---|
| AC-001 | E3/archive-integrity.json, linux/darwin-race/build/version logs: standalone independent N archive/toolchain, no S checkout |
| AC-002 | E3 native Python/sourcehash/build/version logs plus unchanged E1/binaries.json/engine-check.json: layout/invalidation/manifest/embed/compilation controls. No new engine/runtime/publication qualification |
| AC-003 | Carried E2/consumer-narrow.log, consumer-unit.log, consumer-routes.log, consumer-path-pty.log, consumer-launcher.log: ordinary paths/errors/run/file/PTY/generic mapping unchanged; E3/carry-validity.json and DR002 finalization receipt |
| AC-004 | E3 exact input/delta and authority audit + E2/source-contract-audit.json: license/CLA/notices/section7/engine pins unchanged; no rewrite |
| AC-005 | E3/linux-publish-refusal.log, darwin-publish-refusal.log, sourcehash/Python logs; unchanged empty qualification and E2/consumer-guide.log disabled Guide. No publication |
| AC-006 | E3 independent builds/input equality; carried E2/source-contract-audit.json and consumer build/typecheck/unit/launcher logs: no app/service binding, classifier, Git trust or paired pin restored |
| AC-007 | **Delivery-owned terminal gate open.** DR002/finalization.json proves already completed paired source pushes/tree receipt; fresh fix-forward target/hosted CI/terminal receipt pending, not a new API result |
| AC-008 | E3/commands.jsonl, execution-summary.json, test-counts.json, cleanup.json and canonical ledger/history: exact attribution, preserved failed cleanup attempt/skips, safe cleanup |
| AC-009 | E3/linux-focused.log/darwin-focused.log, both race logs, mutation-results.json: actual config verification and before-effect mount refusals, retry/receipt preservation, broader host/state safety. No installed live mount/lifecycle claim |
| AC-010 | Carried E2 current private profile/process/path/API/memory evidence; no S impact. Exact pre-await ownership, no-binding/no-fallback and close-before-release remain unchanged |

## Counts and platform limits
- **Linux arm64:**7 Go packages Pass;47 top-level tests /214 including subtests Pass. Focused hosted config30 pass records (included again in broader race, not unique-added). Go skips TestBootstrapDirectoryModes on container hosts and direct TestInstallerDirectoryModeChild. Python20 collected:17 executed,3 skipped (two installer cases deliberately refuse container hosts; one parent-invoked child fixture). No Linux container-installer permission proof.
- **Darwin arm64:**7 Go packages Pass;59 top-level tests /252 including subtests Pass. Focused31 pass records includes the Darwin-only no-live-source-detach test. Direct Go child skip is intentional; TestBootstrapDirectoryModes parent executes the child. Python20 collected:19 executed,1 child-only skip. Both platforms vet/build/version/Bash/hash/refusal passed.
- **Mutations:**3 native Linux assertion failures expected and observed; none is a compilation failure or candidate failure. Independent copied source only. No canonical production/test mutation.
- Linux focus selector named the extra Darwin-only test but it does not compile on Linux. Generic runner checkpoint wording is clarified in ledger; only actual30 Linux records are claimed.
- S counts remain E2's1666 unit Pass/6 gated live skips,39 API,17 run-memory/native PTY,21 integration,15 core,24 Guide and34 launcher/2skips, with overlap28/narrow34 not unique-added. They are carried, not new execution.
- Native Linux is Ubuntu24.04.5 arm64 UID1001/GCC13.3/Python3.12.3 on LinuxKit kernel; Darwin25.5 arm64 UID501/clang17/Python3.9.6. Go1.27.2 SHA-verified native archives. No amd64 emulation or hosted execution. Source-hash equality is not platform qualification.
- Hosted39097778705/39097779223 stay failed/cancelled. Local arm64 does NOT complete GitHub Ubuntu amd64 or the cancelled macOS matrix jobs. Delivery owns a current hosted run after the reviewed fix-forward. User wants NO RELEASE.

## Failure origin, current attempt and resolution
IR005/CRR007 established the original fixture-only cause: Linux Mounts bypasses Runner and reads proc. Old absent mount let correct production root-store refusal or deliberately unusable Docker sentinel escape the intended boundary. Current test verifies existing proc mount read-only, exact Status mismatch/Unmount refusal and zero Linux commands; Darwin keeps one injected error. Missing/invalid Status specifically checks configuration failure, not any later error. All current candidate tests green; no production defect or runtime fallback prescribed.
One **API-owned cleanup environment Local Fix**: initial inventory guard rejected all checker entries, including exited `[go] <defunct>` PID2898. Diagnosis `/proc/2898/status` showed State Z, PPid1, no open FD table in own sleep-infinity container without init reaper. It was not a running product process. Original guard/script/log/inventory retained at cleanup-attempt-1. Corrected guard still refuses live checker processes and verifies any retained entries are adopted zombies before exact owned-container removal. That removal clears the namespace; final inspect absent and host process/cwd checks pass. No source/test/assertion edits or weakened production safety; no suite rerun necessary for this evidence-only guard. E02 initial Fail attempt followed by final Pass is retained.
IR005 wrong-root preparation and baseline/mutant failures stay historical Implementation evidence, not rerun or relabeled. API001/002 earlier bounded results and setup corrections remain intact. No remaining in-scope finding, no new follow-up or approval loop.

## Confidence and broader-validation decision
| Mandatory category | Post-native repository | Final | Basis / residual limit |
|---|---|---|---|
| Requirement and AC proof |95%|95%| Current AC009/008 fixture/isolation proof plus exact unchanged carry; AC007 explicit downstream terminal gate |
| Changed-boundary execution directness |95%|95%| Actual Linux proc and Darwin command boundary, store/files/config/refusal; privileged storage effects intentionally not invoked |
| Cross-boundary realism / mock gap |95%|95%| Native OS mount observation closes runner-only gap; real files and mutation negatives. S native-child/socket/PTY proof carries; no live export/provider qualification |
| Environment/configuration/identity/fixtures |95%|95%|108 exact inputs, verified native tools, nonroot clean OS copies, private data; local arm64 not hosted amd64 or cancelled matrix proof |
| Failure/edge/lifecycle/recovery |95%|95%| Specific invalid/missing config refusal, repeated partial detach, Apple/connect preservation,3 mutants, full race. Cleanup guard corrected with recorded zombie diagnosis; no live outage/upgrade claim |
| User-surface/browser/desktop-shell |95%|95%| No current UI change; exact carried API002 component/render evidence and disabled Guide. No new browser/desktop journey |
| Durable regression quality/relevance |95%|95%| Reviewed portable fixture preserves assertions, real OS paths and mutation sensitivity; no stale runner assumption or new skip |

Overall post-execution/final **95.00%**, equal mean; no category below90%, all critical API-owned criteria directly supported within scope.
**Broader native Linux validation: Required and Completed. Further broader validation: Not Required for this fixture correction.** Fresh Linux and Darwin execution, actual source-mismatch/unmount refusal before effects and assertion mutants close the material local boundary uncertainty. Another S/VM/NFS/provider/editor campaign would not improve it. Fresh hosted CI remains Delivery's explicit separate terminal gate, not silently waived or assigned Pass. No user-only missing dependency.

## Durable coverage, safety and cleanup
Current reviewed durable change: **N/internal/setup/hosted_config_test.go**, IR00509cac962, already source-reviewed CRR007. API added/updated/removed production or durable tests: **None**. Temporary scripts only archive/run/audit and mutate disposable copies. Proportional successful-test review still required on Large/High; not a new full source review.
Owned developer container and all source/toolchains/homes/caches/mutation copies removed. No live checker or owned host process/cwd remains; adopted zombie cleared with namespace removal.108 current source inputs,535 upstream ticket artifacts, one existing ignored cache and PM board preserved byte-exact. D0 populated main22e934b/branch unchanged; S worktree still retired. Only immutable pinned Ubuntu shared pull cache retained, no built image/live resource.
No host mount/proc mutation, live NFS/container/app/provider use, secrets, socket sharing, host privilege changes, target fetch/merge/push/reset/tag/release/deployment/TaskDone/Terminal/user verification. Completed paired pushes untouched. Delivery's stale RELEASE task is already resolved, not pending.

## Reconciliation / next stage
Ledger current9 fresh platform groups Pass (E01,N01-L/D,N02-L/D,N03-L/D,N04,E02);6 S groups carried. Logical cases reuse N01–03 with platform evidence; prior four-target/actual engine and workflow-lint proof carries only where unchanged. Initial E02 cleanup attempt remains visible/resolved. No interrupted, blocked or unstarted required local case.
Fresh handoff rules determine exact successful-test reviewer recipient. After that gate, Delivery resumes fix-forward/fresh hosted CI/terminal receipts. No duplicate notification, S recreation or initial paired-push replay.
'''
(T/'api-e2e-execution-coverage-report.md').write_text(report)
p=T/'api-e2e-test-case-ledger.md';p.write_text(p.read_text()+'''\n## API-REV-003 final reconciliation
Nine fresh platform/case groups Pass: E01,N01-linux/darwin,N02-linux/darwin,N03-linux/darwin,N04,E02. S01–06 carry API002 with exact limits, no rerun. Existing N03 cross-compilation/engine and N02 actionlint proof carry where unchanged; new native proof separately attributed. Initial E02 cleanup-guard failure resolved after diagnosed exited zombie and exact owned-container removal, raw attempt retained. No remaining failure/blocked/unstarted current local case. API003 Pass95%. DR002/hosted failed-cancelled runs/terminal gates remain Delivery-owned; source pushes and docs sync already completed; no release.\n''')
p=T/'api-e2e-revision-record.md';old=p.read_bytes();write('prior-api-history.json',dict(bytes=len(old),sha256=hashlib.sha256(old).hexdigest()))
s=old.decode();row='| API-REV-003 | CRR007 after DR002/IR005 native Linux fixture recovery | R2/SR003, SR004/ARCH002, IR005, CRR007 | API002 Pass95 local/exact-input | Pass /95.00% affected native N + unchanged carry |\n'
at=s.index('\n\n## API-REV-001');s=s[:at]+'\n'+row.rstrip('\n')+s[at:]
s+='''\n## API-REV-003 — Native hosted-config fixture recovery
2026-10-18. Trigger CRR007 source Pass100 after DR002/IR005. Canonical ticket already tickets/done/extract-autobyteus-nfs; do not recreate in-progress. Prior API002 Pass95 remains its exact local input result, not native Linux/hosted qualification. Current **Pass95%**, fixture09cac962/runtime83726b, R2/SR003/SR004/ARCH002 and Large/High unchanged.
Plan/ledger before execution: current affected N rerun, no S impact/recreation. E01 exact108 input audit/107 unchanged from blocker; eight authorities unchanged. Native Linux arm64 UID1001 proc observation and Darwin arm64 focused/race7packages/vet; both Python/Bash/hash/refusal/native build/version; three isolated Linux mutant failures at intended assertions. Linux47 top-level214 incl subtests/2 Go skips and Python17/20+3skips; Darwin59/252/1 Go child skip, parent exercises child, Python19/20+1skip. Focused results repeat within broad; Darwin-only extra case not Linux coverage. No API production/durable-test edit.
Initial E02 cleanup guard stopped on an exited Go zombie (Z/PPid1) in own non-reaping container. Preserved original attempt, diagnosed, corrected only evidence guard to reject live processes and separately verify zombies, removed exact container/namespace and scratch. Final no-owned-host-process/cwd;108 inputs,535 upstream artifacts, ignored cache and PM unchanged, D0 populated main retained, S retired. No candidate test failure; all35 command exit expectations met, including negative controls. No original hosted failure relabeled.
Nine fresh groups complete, six S groups carried; prior packaging/compiler/artifact limits explicit. Seven confidence categories95%, mean95. Broader native Linux Required and Completed; no further local campaign needed. Native arm64 does not complete hosted amd64/cancelled macOS matrix. DR002 remains Blocked pending Delivery fix-forward/current hosted CI/terminal receipts. Completed N-first/S-second pushes stand; RELEASE prose already synced. No target action/release/TaskDone/Terminal/user verification. Proportional successful-test gate next, not immediate Delivery. API001/002 entries preserved byte-exact.\n'''
p.write_text(s)
(E/'checks-and-limits.md').write_text('''# API-REV-003 — native fixture validation
Current candidate09cac962, runtime83726b unchanged. N108 inputs,107 unchanged from blocker56c0c59. Eight authorities unchanged. S no impact/retired; API002 carries. Canonical report AC table is authoritative scope mapping.

Fresh personally executed Linux arm64 Ubuntu24.04 UID1001 and Darwin arm64 UID501: focused hosted tests + full race7packages/vet/native build/version/Python/Bash/sourcehash/expected publication refusal. Linux47 top-level214 incl subtests Pass,2 Go skips; Python17/20+3skips. Darwin59/252 Pass, direct child skip but bootstrap parent executes; Python19/20+1skip. Focused30 vs31 includes Darwin-only extra test, not additive coverage. Actual Linux proc path; no privileged storage effects. No hosted amd64/matrix/provider/publication qualification.
Three fresh Linux disposable mutants exit1 at intended assertions, not compile errors. All35 command exits match expected values. One separate cleanup guard attempt stopped on exited Go zombie; original script/log retained, Z/PPid1 diagnosis, live-process guard preserved, exact namespace removed. No product/test change. cleanup.json proves own resources absent,535 upstream/108 source/PM/cache preserved; D0 populated main and retired S unchanged.

API003 Pass95, no durable API delta; proportional successful-test gate requested for IR005 hosted_config_test.go correction already source-reviewed CRR007. Delivery DR002 remains Blocked; old hosted39097778705/39097779223 failed/cancelled, completed paired pushes not replayed, RELEASE docs already fixed. No release authorized.\n''')
(E/'attempts.md').write_text('''# API-REV-003 attempts
- No failed current candidate Go/Python/build/vet/refusal command. Refusal exit1 and3 mutant exit1 outcomes are expected controls, separately asserted.
- E02 initial cleanup guard failed before removal on UID1001 exited Go zombie. Original script/log/inventory retained under cleanup-attempt-1. /proc status confirms State Z/PPid1/FDSize0, adopted by sleep-infinity PID1 without init reaper. Corrected evidence guard only: all live checker processes still refused, any retained entries must be adopted zombies; exact owned-container removal clears them. Final cleanup confirmed absent namespace/scratch and no host process/cwd. No candidate test or source change/rerun required.
- Generic focused checkpoint wording included a Darwin-only no-live-source-detach selector; ledger/report explicitly distinguish actual30 Linux hosted records from31 Darwin. No claimed Linux execution of build-tag-excluded test.
- IR005 wrong-root setup/baseline/mutant evidence and failed/cancelled hosted runs are historical, not rerun or relabeled.\n''')
(E/'test-review-scope.md').write_text('''# Proportional successful-test gate
Large/High/Reviewed. Source gate CRR007 accepted IR005 fixture09cac962.
Only durable changed product-tree path: internal/setup/hosted_config_test.go
(70 additions/22 deletions vs blocker56c0c59). API durable/production delta NONE.
Current native Linux and Darwin runs plus3 assertion-sensitive mutants validate
that reviewed fixture. No runtime fallback/trust relaxation/OS skip, no new API
framework. Temporary orchestration/cleanup guard correction is evidence-only;
original failed guard attempt is retained. Request bounded successful-test gate,
not another architecture/source campaign or S/worktree resurrection. After it,
Delivery fix-forward/current hosted CI/terminal receipts; completed source pushes
and synced RELEASE prose must not be replayed. NO RELEASE.\n''')
print('API003 canonical artifacts finalized')
