# API/E2E Execution Coverage Report

## Latest authoritative result
**API-REV-001 — Pass / 95.00% (2026-10-18).** Extract-autobyteus-nfs, not the completed shared-network-workspaces task. All11 planned API case groups have final Pass. The initial S03 fixture-closure failure is preserved and resolved by environment-only correction, not relabeled.
Large / High / Reviewed. **Proportional successful-test review required** before Delivery. No production or durable-test edits by API. No target merge/push/tag/release/deploy/TaskDone/user verification.

## Execution round and authority
First completed round; prior API/DR result N/A. Trigger CRR002 source Pass100 over IR002/IR001. Approved R2/SR003, Ready SR004, ARCH-REV-002 remain governing.
Authority paths at this ticket root: requirements-doc.md, investigation-notes.md, solution-revision-record.md, design-spec.md, user-filesystem-boundary-correction.md, solution-design-handoff.md; design-review-report.md and architecture-review-revision-record.md; implementation-handoff.md and implementation-revision-record.md; code-review-report.md and code-review-revision-record.md.
Coverage investigation and ledger were written before execution. Their canonical paths are api-e2e-coverage-investigation.md / api-e2e-test-case-ledger.md; history is api-e2e-revision-record.md.
N input HEAD62f7b3933b4ec040b50f2ac12c333b2a9f23b459 (review receipt; unchanged service source83726b27400b405a7a6a79bd962d8e2419daa561). S a2023feff3d498fb6c51cebf1c93360da3679a45. Both branches codex/extract-autobyteus-nfs.
N=/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs
S=/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs

## Scope / changed-boundary evidence
SCN001/002/003/006/007: independent service/build/distribution, host-only admission/lifecycle, ordinary application paths, private runtime profiles. SCN004/AC007 remains Delivery-owned. SCN005 live provider/platform/old filesystem/editor campaigns are excluded, not Passed.
Exact commands/cwd/exits/timing are in evidence/api-e2e/api-rev-001/commands.jsonl; environment/tool versions in environment.json/toolchain.json. Production source is archived exactly; no stale installed app or old dist was used. Only root ticket history was initially excluded;11 tracked fixtures actually consumed by two broad unit suites were restored verbatim after ENOENT proof.

| Case | Final | Observation / boundary | Evidence under evidence/api-e2e/api-rev-001/ |
|---|---|---|---|
| E01 | Pass | 47 source/license/pin/removal contracts; exact108 N/7215 S source archive inputs | source-contract-audit.json; archive-integrity.json |
| N01 | Pass | 7 Go packages;59 top-level tests/252 including subtests Pass, race/vet; focused locked refusal | nfs-focused.log; nfs-race.log; nfs-vet.log |
| N02 | Pass | 19 Python tests executed;1 Go-child skip; workflow/shell/hash and expected publication refusal | nfs-python.log; nfs-actionlint.log; nfs-shell.log; nfs-source-hash.log; nfs-publish-refusal.log |
| N03 | Pass | 4 targets compile, native version, actual retained arm64 manifest/bytes verified and embedded compile | binaries.json; engine-check.json; nfs-version.log; nfs-build-embedded.log |
| S01 | Pass | Frozen install and fresh documented production/prerequisite builds/typecheck | consumer-install.log; consumer-build.log; consumer-typecheck.log |
| S02 | Pass | 7 files/34 tests; ordinary registered errors and private preparation/files/process controls | consumer-narrow.log |
| S03 | Pass | Same full broad suite green after exact replay-fixture closure; initial failure preserved | consumer-unit-confirm.log; consumer-fixture-confirm.log; fixture-restoration.json; consumer-unit.log |
| S04 | Pass | Local composed ordinary file/skill API contracts | consumer-routes.log |
| S05 | Pass | Local run/memory layout and actual native PTY/WebSocket lifecycle | consumer-path-pty.log |
| S06 | Pass | Generic Bash launcher and disabled Guide/localization checks; carried current render evidence | consumer-launcher.log; consumer-guide-confirm.log; consumer-localization.log; consumer-web-boundary.log |
| E02 | Pass | Both owned archives removed, no owned processes, source/protected data unchanged | cleanup.json; cleanup-preflight.json |

## Acceptance-Criteria Proof
Evidence folder: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs/tickets/in-progress/extract-autobyteus-nfs/evidence/api-e2e/api-rev-001
Table filenames resolve under that folder unless marked ticket-root. The API Pass covers executable extraction scope; AC007 remains explicitly unproven by this stage.

| AC | Critical to API gate | Cases | Evidence | Disposition |
|---|---|---|---|---|
| AC001 | Yes | E01/N01/N02/N03 | archive-integrity.json; nfs-race.log; nfs-python.log; binaries.json | Proven: independent N root/toolchain with no S source access required |
| AC002 | Yes | N02/N03 | nfs-python.log; nfs-source-hash.log; binaries.json; engine-check.json | Proven: layout/hash/invalidation/manifest/embed/compiler boundary; runtime qualification not claimed |
| AC003 | Yes | S02/S03/S04/S05/S06 | consumer-narrow.log; consumer-unit-confirm.log; consumer-routes.log; consumer-path-pty.log; consumer-launcher.log | Proven: ordinary selected path/error, file API, run/PTY and generic launcher mapping |
| AC004 | Yes | E01 | source-contract-audit.json | Proven: exact licenses/CLA/third-party/section7 via license equality, engine recipes/pins |
| AC005 | Yes | E01/N02/S06 | source-contract-audit.json; nfs-python.log; nfs-publish-refusal.log; consumer-guide-confirm.log | Proven: qualification remains empty; unqualified publication refused, Guide disabled |
| AC006 | Yes | E01/S01/S03/S06 | source-contract-audit.json; consumer-build.log; consumer-typecheck.log; consumer-unit-confirm.log; consumer-launcher.log | Proven: removed bridge/owners/imports, independent builds, current owners execute |
| AC007 | No — Delivery-owned | None | implementation-handoff.md and design-spec.md (ticket-root authorities) | Not Proven / Not Tested here: fresh target verification and ordered N then S finalization remain Delivery work |
| AC008 | Yes | E01/E02/all | commands.jsonl; execution-summary.json; attempts.md; cleanup.json | Proven: traceable executions, retained failures/skips/cleanup and bounded verdict |
| AC009 | Yes | N01 | nfs-focused.log; nfs-race.log; source-contract-audit.json | Proven: actual trusted active/pending admission/lock before effects, current host-only shape and retained lifecycle controls |
| AC010 | Yes | S02/S03/S04/S05 | consumer-narrow.log; consumer-unit-confirm.log; consumer-routes.log; consumer-path-pty.log | Proven: private exact pre-await owner, aliases/collision/no-binding/no fallback and source-preserving close/retry/release |

## Counts and exact limits
- consumer-narrow: Test Files  7 passed (7); Tests  34 passed (34); Duration  7.82s (transform 2.36s, setup 64ms, import 5.78s, tests 706ms, environment 0ms).
- consumer-unit: Test Files  2 failed | 102 passed | 4 skipped (108); Tests  12 failed | 1186 passed | 6 skipped (1204); Duration  71.00s (transform 3.90s, setup 815ms, import 30.21s, tests 30.67s, environment 7ms).
- consumer-fixture-confirm: Test Files  2 passed (2); Tests  86 passed (86); Duration  3.02s (transform 1.52s, setup 35ms, import 2.34s, tests 31ms, environment 0ms).
- consumer-unit-confirm: Test Files  104 passed | 4 skipped (108); Tests  1198 passed | 6 skipped (1204); Duration  76.72s (transform 5.12s, setup 972ms, import 34.52s, tests 30.93s, environment 8ms).
- consumer-routes: Test Files  3 passed (3); Tests  39 passed (39); Duration  16.88s (transform 6.24s, setup 43ms, import 12.22s, tests 3.88s, environment 0ms).
- consumer-path-pty: Test Files  3 passed (3); Tests  17 passed (17); Duration  11.60s (transform 5.18s, setup 78ms, import 9.17s, tests 1.28s, environment 0ms).
- consumer-guide: Test Files  4 failed (4); Tests  no tests; Duration  964ms (transform 32ms, setup 0ms, collect 0ms, tests 0ms, environment 821ms, prepare 513ms).
- consumer-guide-confirm: Test Files  4 passed (4); Tests  24 passed (24); Duration  9.21s (transform 3.70s, setup 16.32s, collect 171ms, tests 103ms, environment 643ms, prepare 447ms).
- Counts are separate runs, not additive unique coverage: S02's34 and the restored-fixture86 are repeated inside S03's final broad suite.
- Go cmd package has no tests; standalone TestInstallerDirectoryModeChild is opt-in skipped, and the Python child fixture is skipped in standalone discovery. Parent TestBootstrapDirectoryModes invokes the permission child regression and passed. Do not promote either skip to a separate Pass.
- Six AGY live tests/four files are gated and not executed; no authenticated provider proof claimed. Launcher ran34 tests;2 skipped: pwsh unavailable and port8001 unavailable for collision fixture. Existing controlled-busy-port coverage passed without changing the occupying service. Skips are not masked.
- Frozen install warned about a not-yet-built devkit bin and a disallowed unrelated @google/genai build script. Documented integration preparation built the devkit and invokes its CLI directly; all selected builds/checks passed. No approval policy or dependency scripts were loosened.

## Attempts and preliminary classification
S03 initial12 failures were all ENOENT for11 replay files under root tickets/done excluded by API archive setup. fixture-restoration.json identifies exact current-commit paths/hashes; tests and assertions unchanged. The2 affected suites passed86 tests, followed by full same broad command. **API-owned environment Local Fix resolved**; no product defect or reviewer-origin routing required. Initial consumer-unit.log and commands remain.
S06 initially collected zero tests in4 suites because API omitted documented Nuxt preparation (.nuxt/tsconfig.json absent). consumer-guide.log preserves that setup failure. Ran documented nuxt prepare and the identical4 suites passed; no source/config/assertion change. API-owned environment Local Fix resolved.

An initial summary formatter mixed None with bool during Go counting; original script retained under summary-attempt-1, corrected without altering raw logs. Evidence tooling error, not product failure. Other discovery/tooling notes in attempts.md.

## Confidence scorecard
| Category | Post-repository | Final | Supporting proof | Residual limit |
|---|---|---|---|---|
| Requirement and acceptance-criteria proof | 95% | 95% | Direct evidence for AC001–006/008–010; AC007 explicitly belongs to Delivery | No publication/platform inference; scope-limited proof |
| Changed-boundary execution directness | 95% | 95% | Real root builds/tooling/locks/readers/files/private profile owners; no sibling linkage | Privileged mount/engine side effects remain doubled; underlying production backend/platform/service mechanically unchanged |
| Cross-boundary integration realism and mock gap | 95% | 95% | Local HTTP/GraphQL + actual native PTY/WebSocket + Codex/Grok owned child protocols | Fake model/native-protocol fixtures and Claude client doubles, not authenticated provider proof |
| Environment, configuration, identity and fixture fidelity | 95% | 95% | Exact current source archives, canonical private HOME/TMPDIR, frozen dependencies/current builds,11 exact restored tracked fixtures | Single Darwin arm64 host; no target platform execution claim |
| Failure, edge-case, lifecycle and recovery | 95% | 95% | Malformed/predecessor refusal before effects, source/busy-detach controls, cancellation, alias/collision, exact close/retry/release | No live installation migration/outage/reboot qualification |
| User-surface, browser and desktop-shell | 95% | 95% | Fresh Guide/component/localization checks; exact-byte current Guide matches IR001 rendered EN/zh wide/narrow evidence | Carried rendered component proof attributed to IR001; no API browser or Electron rerun, no shell-specific change |
| Durable regression coverage quality and relevance | 95% | 95% | Current R2 ownership/path/admission tests replace obsolete coupling tests; narrow then broader regression green | Replay fixtures currently live in tracked ticket data; isolated runs must include these explicit dependencies |

Overall post-repository and final confidence **95.00%**, equal mean. Every critical API-owned AC has direct proof, no category below90%, no material unclosed R2 boundary risk.
**Broader validation: Not Required beyond executed repository-native process/API/PTY tests.** Real filesystem, lock, native child, local socket and PTY boundaries are already exercised. Changed host admission is tested before privileged effects; unchanged backend/platform/service bytes are mechanically proven. A new mounted/provider/desktop campaign would expand qualification rather than close a material extraction gap.
Guide: carried IR001 implementation-rendered current component EN/zh at1440/390, verified exact current component/catalog bytes and fresh component tests. API personally inspected en-390/zh-1440 and all4 result states. No new browser run or Electron shell claim. No effect on running user application.

## Persisted transition / legacy check
Approved **Directly Usable — No Migration**: absent/null/empty old Nodes are usable and not perpetuated by current writers; meaningful/malformed active or pending obligations refuse under existing admin lock before binary or resource effects. Unknown additive fields/history remain inert; no scan/migration/dual-version runtime. Install existing binary/state preservation, all setup entry refusal, source/pending/permissions/busy-detach controls execute. Application registration/history/project skills/credentials are not transformed.
No invalid compatibility retention observed. Removed binding/classifier/automatic Git trust and paired protocol assertions were superseded by R2; ordinary path/private profile tests are their replacements. No source or test removed by API.

## Durable coverage and proportional review
API durable additions/updates/removals: **None**; current R2 coverage is adequate and unchanged. Temporary ticket scripts only orchestrate safe archives/checks/audits. The cumulative R2 test delta is listed in evidence/api-e2e/api-rev-001/test-review-scope.md (N relativefc5d2ff; S relative3712cd9b; old embedded-service deletion is not a new API change).
Review should remain proportional to executed current coverage and stated fixture/mock limits. No source rereview, old af9f23/editor acceptance loop or new approval request.

## Environment / mocks / safety / cleanup
Fresh owned archives with explicit PATH/HOME/TMPDIR and no inherited application/provider environment. Actual versions/platform in toolchain.json; Go1.27.2 official archive SHA verified, Node22.21.1, pnpm10.28.2, Python system3.9, Darwin arm64.
N tests double root/engine/mount effects; Docker launcher doubles Docker. Claude SDK failure controls are doubles; Codex/Grok protocol executables are actual owned children without paid inference. Local route/run/PTY tests use minimal fixture data and documented current build prerequisites. No VM/Docker/mount/firewall/user-app/provider/remote-ref operation.
Both owned source/tool/cache/node_modules/data/build roots removed after no-owned-process preflight.108 N and7215 S source files unchanged;11 restored fixtures hash-exact;9 protected PM/retained-engine files unchanged. D0 remains unborn main with PM data preserved. cleanup.json and cleanup-preflight.json prove boundaries. No binaries/bundles/database/node_modules committed.
No only-user-checkable behavior is required for this API verdict. Live mounted/install/provider/physical/cross-OS/signing/hosted-publication qualification remains Not Tested, not a user-approval request. AC007 is pending downstream Delivery work.

## Ledger reconciliation and next action
Ledger initialized before execution, each attempt recorded before next case; N and S independent groups ran concurrently in personally owned processes. E01/N01–03/S01–06/E02 all final Pass. No running, interrupted, blocked or unstarted API case. Initial S03 failure retained with final resolution.
Fresh get_handoff_rules must select the exact recipient. Request proportional successful-test review; then normal Delivery. No direct Delivery or duplicate notifications.

## Applied route
Fresh rules selected only /software_engineering_team/code_reviewer: API Pass + Large/High + cumulative proportional test-code review. Failure, direct low-risk Delivery, and upstream-ambiguity rules do not match. routing.json preserves the returned rules. No duplicate notification.

Raw test logs retained verbatim; git whitespace diagnostics are confined to captured log formatting. Non-log artifact check exit0; artifact-whitespace.json records both results.
