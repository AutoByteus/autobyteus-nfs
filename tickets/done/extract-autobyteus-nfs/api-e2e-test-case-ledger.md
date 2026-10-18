# API/E2E Test-Case Ledger

## API-REV-001 Ledger Meta (historical)
- Task: extract-autobyteus-nfs; first round API-REV-001 (no prior API result).
- Scope: approved R2/SR003, Ready SR004, ARCH-REV-002, CRR-002. Large / High / Reviewed.
- Investigation: api-e2e-coverage-investigation.md. Report: api-e2e-execution-coverage-report.md (pending).
- Multiple independent cases and clean builds require durable checkpoints.
- Planned before execution, 2026-10-18. N and S refer to the two assigned worktrees, not old shared-network-workspaces.

## Planned Cases
| ID | Journey | ACs | Surface / expected result |
|---|---|---|---|
| E01 | Current independent source, removal and license audit | AC001/004/006/008 | Archive/hash/import/lock audit; no sibling linkage |
| N01 | Bounded predecessor-state admission and host lifecycle | AC009 | Focused Go config/CLI/setup tests, then race/vet all packages |
| N02 | Standalone packaging and refusal gates | AC001/002/005 | Python fixtures, installer shell, actionlint, current source hash/publication refusal |
| N03 | Current four-target compile and exact retained engine verification | AC001/002/005 | CGO0 darwin/linux arm64/amd64; native version; real arm64 manifest/embed |
| S01 | Clean consumer setup, production build and typecheck | AC003/006 | Frozen filtered install including script-only dependencies; integration:prepare/typecheck |
| S02 | Ordinary registered paths and filesystem-independent private profiles | AC003/010 | Focused registered/native/private preparation/bootstrappers/process tests |
| S03 | Runtime owner regression closure | AC003/006/010 | Broader backends/services/workspaces/terminal/Codex/activation units; real process fixture included |
| S04 | Ordinary file/skill APIs | AC003/010 | Local composed server REST/GraphQL tests, owned filesystem fixtures |
| S05 | Ordinary run and native PTY/WebSocket lifecycle | AC003/010 | Current-build path/memory-layout/terminal integration; local dummy LLM, no paid provider |
| S06 | Generic launcher and factual disabled Guide | AC003/005/006 | Bash fixture launcher; four Guide/localization suites and guards; carry unchanged current Guide render proof |
| E02 | Cleanup and evidence/source integrity | AC008 | Own scratch/process cleanup; source and protected resources unchanged |

## Execution Events
| Time UTC | Case | Event | Observation | Result | Evidence |
|---|---|---|---|---|---|
| 2026-10-18T03:26:16.070830+00:00 | E01 | Started | Create independent exact source archives; no runtime source mutation | N/A |  |
| 2026-10-18T03:26:29.329720+00:00 | E01 | Checkpoint | Exact independent archives verified, pinned official toolchain verified; source-contract audit still pending | N/A | archive-integrity.json; toolchain.json |
| 2026-10-18T03:26:54.696229+00:00 | E01 | Completed | 47 source/license/pin/removal contracts checked; independent archives exact | Pass | source-contract-audit.json; archive-integrity.json |
| 2026-10-18T03:27:20.550239+00:00 | N01 | Started | Focused admission/current host controls, then complete race/vet | N/A |  |
| 2026-10-18T03:27:21.673467+00:00 | S01 | Started | Frozen install with script-only integration build closure; isolated private HOME/TMPDIR | N/A |  |
| 2026-10-18T03:27:53.176080+00:00 | N01 | Completed | Focused current reader/lock/pre-effect refusal and all Go race/vet passed | Pass | nfs-focused.log; nfs-race.log; nfs-vet.log |
| 2026-10-18T03:27:53.176583+00:00 | N02 | Started | Root packaging/installer/workflow/refusal fixtures | N/A |  |
| 2026-10-18T03:27:56.340866+00:00 | N02 | Completed | Packaging/shell/workflow checks passed; unqualified publication refused as expected. Python child skip is not counted Pass | Pass | nfs-python.log; nfs-actionlint.log; nfs-shell.log; nfs-source-hash.log; nfs-publish-refusal.log |
| 2026-10-18T03:27:56.340995+00:00 | N03 | Started | Compile all four targets; current native version and exact arm64 artifact | N/A |  |
| 2026-10-18T03:28:17.741238+00:00 | N03 | Completed | Four target builds/native version + actual verified arm64 bundle embedded compile passed; no target runtime qualification | Pass | binaries.json; engine-check.json; nfs-build-embedded.log |
| 2026-10-18T03:28:47.244843+00:00 | S01 | Completed | Fresh production/prerequisite builds and production typecheck exit0 | Pass | consumer-install.log; consumer-build.log; consumer-typecheck.log |
| 2026-10-18T03:28:47.244960+00:00 | S02 | Started | Current ordinary path and private profile narrow tests | N/A |  |
| 2026-10-18T03:28:56.095713+00:00 | S02 | Completed | Real files/aliases/collisions and registered error/native Codex/Grok process controls passed | Pass | consumer-narrow.log |
| 2026-10-18T03:28:56.095824+00:00 | S03 | Started | Broader affected ownership/runtime/path/terminal regression | N/A |  |
| 2026-10-18T03:30:07.651032+00:00 | S03 | Completed | consumer-unit exit 1 | Fail | commands.jsonl; latest log |
| 2026-10-18T03:30:36.837045+00:00 | S03 | Checkpoint | All 12 failures are missing 11 tracked replay fixtures excluded by archive setup; restore exact current bytes without test edits | N/A | consumer-unit.log; fixture-restoration.json |
| 2026-10-18T03:30:44.307401+00:00 | S03 | Started | Rerun exact restored replay fixtures first, then full affected suite | N/A |  |
| 2026-10-18T03:30:48.022563+00:00 | S03 | Started | Broader affected ownership/runtime/path/terminal regression | N/A |  |
| 2026-10-18T03:32:05.340143+00:00 | S03 | Completed | Affected regression suite passed; live-gated skips retained separately | Pass | consumer-unit-confirm.log; consumer-fixture-confirm.log; fixture-restoration.json |
| 2026-10-18T03:32:05.341172+00:00 | S04 | Started | Local socket/inject file and skill API contracts | N/A |  |
| 2026-10-18T03:32:22.872220+00:00 | S04 | Completed | Ordinary file/skill local transport and filesystem cases passed | Pass | consumer-routes.log |
| 2026-10-18T03:32:22.873021+00:00 | S05 | Started | Current-build run/memory layout/native PTY and WebSocket lifecycle | N/A |  |
| 2026-10-18T03:32:35.198923+00:00 | S05 | Completed | Local run registration/memory and actual native PTY/WebSocket lifecycle passed | Pass | consumer-path-pty.log |
| 2026-10-18T03:32:35.200473+00:00 | S06 | Started | Generic launcher and disabled Guide/localization tests | N/A |  |
| 2026-10-18T03:33:14.038762+00:00 | S06 | Completed | consumer-guide exit 1 | Fail | commands.jsonl; latest log |
| 2026-10-18T03:33:36.335287+00:00 | S06 | Started | Correct API omission of documented Nuxt prepare before exact suite rerun | N/A |  |
| 2026-10-18T03:33:50.939293+00:00 | S06 | Completed | Generic launcher green; after documented Nuxt preparation all4 Guide suites and both guards passed; no product/test edit | Pass | consumer-guide-confirm.log; consumer-nuxt-prepare.log; consumer-launcher.log; consumer-localization.log; consumer-web-boundary.log |
| 2026-10-18T03:33:59.583202+00:00 | E02 | Started | Check source/protected data and own runtime process quiescence, then remove only two API archives | N/A |  |
| 2026-10-18T03:34:26.859833+00:00 | E02 | Completed | Both API scratch roots removed; 108 N/7215 S source inputs and nine protected PM/engine files unchanged; no owned process remains | Pass | cleanup.json; cleanup-preflight.json |

## API-REV-001 Final Reconciliation (historical)
All11 case groups have final Pass; initial S03/S06 Fail attempts are retained, exact fixture/build setup corrected and same broad command rerun. No running/interrupted/unstarted API case. Reconciled into api-e2e-execution-coverage-report.md (API-REV-001 Pass95%). AC007 is downstream Delivery-owned, not claimed as executed.

## API-REV-002 pre-execution impact plan

# API-REV-002 current integrated validation plan

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


## API-REV-002 Execution Events
| Time UTC | Case | Event | Observation | Result | Evidence |
|---|---|---|---|---|---|
| 2026-10-18T04:12:53.298737+00:00 | E01 | Started | Verify current source identity and carry independent unchanged N only | N/A |  |
| 2026-10-18T04:12:57.939827+00:00 | E01 | Checkpoint | Exact7307-source archive plus11 current replay inputs prepared; no stale build dependency | N/A | archive-integrity.json; fixture-inputs.json; carry-validity.json |
| 2026-10-18T04:13:00.178703+00:00 | E01 | Completed | 47 source/license/pin/removal contracts checked; independent archives exact | Pass | source-contract-audit.json; archive-integrity.json |
| 2026-10-18T04:13:00.288205+00:00 | S01 | Started | Frozen install with script-only integration build closure; isolated private HOME/TMPDIR | N/A |  |
| 2026-10-18T04:14:23.667269+00:00 | S01 | Completed | Fresh production/prerequisite builds and production typecheck exit0 | Pass | consumer-install.log; consumer-build.log; consumer-typecheck.log |
| 2026-10-18T04:14:23.667951+00:00 | S02 | Started | Current ordinary path and private profile narrow tests | N/A |  |
| 2026-10-18T04:14:40.959620+00:00 | S02 | Completed | Real files/aliases/collisions and registered error/native Codex/Grok process controls passed | Pass | consumer-narrow.log |
| 2026-10-18T04:14:40.960240+00:00 | S03 | Started | Broader affected ownership/runtime/path/terminal regression | N/A |  |
| 2026-10-18T04:17:49.592732+00:00 | S03 | Completed | Affected regression suite passed; live-gated skips retained separately | Pass | consumer-unit.log |
| 2026-10-18T04:17:49.593579+00:00 | S04 | Started | Local socket/inject file and skill API contracts | N/A |  |
| 2026-10-18T04:18:04.466023+00:00 | S04 | Completed | Ordinary file/skill local transport and filesystem cases passed | Pass | consumer-routes.log |
| 2026-10-18T04:18:04.466136+00:00 | S05 | Started | Current-build run/memory layout/native PTY and WebSocket lifecycle | N/A |  |
| 2026-10-18T04:18:13.074853+00:00 | S05 | Completed | Local run registration/memory and actual native PTY/WebSocket lifecycle passed | Pass | consumer-path-pty.log |
| 2026-10-18T04:18:13.075360+00:00 | S06 | Started | Generic launcher and disabled Guide/localization tests | N/A |  |
| 2026-10-18T04:18:58.698870+00:00 | S06 | Completed | Generic launcher and Guide/guards passed; explicit skips in log; carried Guide render inputs verified | Pass | consumer-launcher.log; consumer-guide.log; consumer-localization.log; consumer-web-boundary.log; source-contract-audit.json |
| 2026-10-18T04:19:27.822953+00:00 | E02 | Started | Verify exact assigned inputs/protected data and process quiescence before removing own archive | N/A |  |
| 2026-10-18T04:19:50.421866+00:00 | E02 | Completed | Owned S archive removed; no owned process/cwd;108 N/7307 S +11 replay inputs and protected PM/engine unchanged | Pass | cleanup.json; cleanup-preflight.json |

## API-REV-002 final reconciliation
Fresh E01/S01–06/E02 Pass at S60b67dabecaf5569a8e26128dbdb26117c988811; N01–03 carried API001 Pass only after exact108 independent N input equality. Seven fresh case checks plus E02 and three carried groups =11 groups. No failed, blocked, interrupted or unstarted current case. All15 current commands exit0. Narrow/overlap repeat inside broad; do not add as unique. See execution-summary.json and test-counts.json for exact fresh counts/skips. API002 Pass95% covers current executable extraction scope only. No new N campaign; copied E01 audit phrase is clarified in the report. AC007/DR001 and stale RELEASE docs remain Delivery-owned.

## API-REV-003 pre-execution impact plan

# API-REV-003 — archived fixture recovery plan (before execution)

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

## API-REV-003 Execution Events
| UTC | Case | Event | Observation | Result | Evidence |
|---|---|---|---|---|---|
| 2026-10-18T04:58:35.751254+00:00 | E01 | Started | Prepare exact independent N source/toolchains; preserve archived ticket and completed targets | N/A |  |
| 2026-10-18T04:59:29.984161+00:00 | E01 | Completed | Exact108-input N archives, verified native Go1.27.2;107 other inputs unchanged from blocker, one reviewed fixture delta | Pass | input-audit.json; archive-integrity.json; carry-validity.json; container.json; toolchains.json |
| 2026-10-18T04:59:39.233852+00:00 | N01-linux | Started | Current fixture through actual linux mount-observation path, nonroot focused first then race/vet | N/A |  |
| 2026-10-18T04:59:39.234408+00:00 | N01-darwin | Started | Current fixture through actual darwin mount-observation path, nonroot focused first then race/vet | N/A |  |
| 2026-10-18T05:00:05.691166+00:00 | N01-darwin | Checkpoint | Focused hosted-config/no-live-source detach passed; native path exercised, broader package closure running | N/A | darwin-focused.log |
| 2026-10-18T05:00:08.923468+00:00 | N01-linux | Checkpoint | Focused hosted-config/no-live-source detach passed; native path exercised, broader package closure running | N/A | linux-focused.log |
| 2026-10-18T05:00:31.368334+00:00 | N01-linux | Completed | Current focused plus all-package race/vet passed; skips retained separately | Pass | linux-focused.log; linux-race.log; linux-vet.log |
| 2026-10-18T05:00:31.369133+00:00 | N02-linux | Started | Packaging/installer fixture controls, Bash/sourcehash and expected empty-qualification refusal | N/A |  |
| 2026-10-18T05:00:33.220857+00:00 | N01-darwin | Completed | Current focused plus all-package race/vet passed; skips retained separately | Pass | darwin-focused.log; darwin-race.log; darwin-vet.log |
| 2026-10-18T05:00:33.220985+00:00 | N02-darwin | Started | Packaging/installer fixture controls, Bash/sourcehash and expected empty-qualification refusal | N/A |  |
| 2026-10-18T05:00:33.434142+00:00 | N02-linux | Completed | Packaging/Bash/hash/refusal passed within explicit native/container skip limits | Pass | linux-python.log; linux-source-hash.log; linux-publish-refusal.log |
| 2026-10-18T05:00:33.434295+00:00 | N03-linux | Started | Current native build/version, not live installed service or target qualification | N/A |  |
| 2026-10-18T05:00:34.602406+00:00 | N03-linux | Completed | Current native binary built/version executable passed; no service lifecycle invoked | Pass | linux-build.log; linux-version.log |
| 2026-10-18T05:00:38.322418+00:00 | N02-darwin | Completed | Packaging/Bash/hash/refusal passed within explicit native/container skip limits | Pass | darwin-python.log; darwin-source-hash.log; darwin-publish-refusal.log |
| 2026-10-18T05:00:38.322881+00:00 | N03-darwin | Started | Current native build/version, not live installed service or target qualification | N/A |  |
| 2026-10-18T05:00:39.952935+00:00 | N03-darwin | Completed | Current native binary built/version executable passed; no service lifecycle invoked | Pass | darwin-build.log; darwin-version.log |
| 2026-10-18T05:00:48.287204+00:00 | N04 | Started | Independent native Linux assertion-sensitivity controls in three disposable mutated copies | N/A |  |
| 2026-10-18T05:00:50.684432+00:00 | N04 | Checkpoint | ignore-status-preflight failed the intended assertion (expected exit1, not compilation failure) | N/A | mutation-ignore-status-preflight.log |
| 2026-10-18T05:00:52.528259+00:00 | N04 | Checkpoint | ignore-detach-preflight failed the intended assertion (expected exit1, not compilation failure) | N/A | mutation-ignore-detach-preflight.log |
| 2026-10-18T05:00:54.286831+00:00 | N04 | Checkpoint | reject-partial-detach failed the intended assertion (expected exit1, not compilation failure) | N/A | mutation-reject-partial-detach.log |
| 2026-10-18T05:00:54.287160+00:00 | N04 | Completed | All3 actual Linux mutant controls caught missing/overstrict preflight; canonical production/tests unchanged | Pass | mutation-results.json; mutation-*.log |
| 2026-10-18T05:01:32.546427+00:00 | E02 | Started | Confirm source/protected-state exactness and native quiescence, then remove only API003-owned resources | N/A |  |
| 2026-10-18T05:01:59.622649+00:00 | E02 | Attempt stopped | Initial cleanup guard rejected exited Go zombie owned by UID1001; container not yet removed; no test failed | Fail | cleanup-attempt-1/cleanup-console.log; cleanup-process-diagnosis.log |
| 2026-10-18T05:01:59.677771+00:00 | E02 | Started | Confirm source/protected-state exactness and native quiescence, then remove only API003-owned resources | N/A |  |
| 2026-10-18T05:02:05.847113+00:00 | E02 | Completed | Own container/archive/toolchains/caches removed;108 inputs +535 upstream artifacts +PM/ignored cache preserved; D0 populated main unchanged, S retired | Pass | cleanup.json; cleanup-preflight.json; linux-final-inputs.log; linux-final-processes.log |
| 2026-10-18T05:02:05.847417+00:00 | N01-linux | Clarification | Focused Linux selector executed30 hosted-config pass records; extra no-live-source-detach case is Darwin-only (31 there), not Linux coverage | N/A | test-counts.json; linux-focused.log; darwin-focused.log |

## API-REV-003 final reconciliation
Nine fresh platform/case groups Pass: E01,N01-linux/darwin,N02-linux/darwin,N03-linux/darwin,N04,E02. S01–06 carry API002 with exact limits, no rerun. Existing N03 cross-compilation/engine and N02 actionlint proof carry where unchanged; new native proof separately attributed. Initial E02 cleanup-guard failure resolved after diagnosed exited zombie and exact owned-container removal, raw attempt retained. No remaining failure/blocked/unstarted current local case. API003 Pass95%. DR002/hosted failed-cancelled runs/terminal gates remain Delivery-owned; source pushes and docs sync already completed; no release.

Final identity audit correction: pre-run prose called review-report commit d32309d the intake; machine input-audit.json correctly captured actual HEAD487e74c9bf926f98a10d7d39d5f62bbc14a9566d. The intervening commit changes only CRR007/routing.json, not any source/test. Current report/investigation corrected; original plan/runner text retained. No test validity impact.

Final finalization audit first stopped on PM board hash change AFTER the successful cleanup check (cleanup05:02:05 UTC; PM mtime05:04:20 UTC). Current board includes a separate dashboard Task. Author not independently verified; API made no write. Kept external board untouched, preserved failed audit, and record final mismatch explicitly rather than restore another owner's work. See final-audit-attempt-1 and external-PM-observation.json. No source/test/evidence input change.
