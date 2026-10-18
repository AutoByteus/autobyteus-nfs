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
