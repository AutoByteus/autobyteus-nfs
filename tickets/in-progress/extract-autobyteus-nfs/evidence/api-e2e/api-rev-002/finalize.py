from common import *
import hashlib
summary=json.loads((E/'execution-summary.json').read_text());assert summary['all_current_commands_pass'] and summary['cleanup']['pass_']
counts=summary['counts'];a=json.loads((E/'input-audit.json').read_text());E1=E.parent/'api-rev-001'
count_lines='\n'.join('- **'+name+'**: '+'; '.join(rows) for name,rows in counts.items() if rows)
head='''# API/E2E Coverage Investigation

## Current authority and scope
API-REV-002, extract-autobyteus-nfs / project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8; Large / High / Reviewed. Personal execution, no delegation.
Trigger CRR005 source Pass100 after integrated IR003 and IR004 one-import cleanup. Full original R2 package remains active: requirements-doc, investigation-notes, solution-revision-record, design-spec, user-filesystem-boundary-correction, solution-design-handoff, design-review-report, architecture-review-revision-record. Eight authority documents byte-unchanged since API001. Approved R2/SR003, Ready SR004/ARCH002. Read current implementation handoff/history, code-review report/history, DR001 and existing API investigation/report/history/ledger.
N=/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs. S=/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs. Both codex/extract-autobyteus-nfs. N service83726b27400b405a7a6a79bd962d8e2419daa561. Current S60b67dabecaf5569a8e26128dbdb26117c988811 integrates personal2f211340 through merge156ea2d plus narrow test cleanup. Exact input HEADs/hashes: evidence/api-e2e/api-rev-002/input-audit.json.
API001 Pass95 and CRR003 apply to preintegration Sa2023, not current integrated S. DR001 remains Delivery's last verdict; this stage does not override it. Known S RELEASE.md obsolete R1 tail is Delivery docs-sync work.

## Impact plan written before execution
Current S TESTING.md shared-foundation rule required rerunning ALL S01–06 after core/contracts/harness/fixture changes. Complete diff since Sa2023 and original plan: evidence/api-e2e/api-rev-002/integrated-changed-paths.txt and validation-plan.md. E01/current source audit and E02/own cleanup rerun. N01–03 Still Valid only after all108 independent N inputs and authority equality; no new N campaign. Prior API001 scope/limits retained. No historical skip promoted to Pass.
Read applicable N AGENTS/TESTING/DESIGN/README and S AGENTS/TESTING/DESIGN, server/web AGENTS/README, manifests/scripts/vitest config and real suite/fixture paths. No closer TESTING override. Clean frozen whole-workspace install, documented integration:prepare/current production typecheck, Nuxt prepare; serialized in one owned exact-source archive. Eleven tracked replay fixtures included upfront, unlike API001's corrected omission. No inherited app/provider environment; private canonical HOME/TMPDIR/store, Node22.21.1/pnpm10.28.2. Assigned worktree old builds never consumed.

## Scenarios and changed boundaries
| Scenario / AC | Changed boundary | Planned and completed evidence | Limit |
|---|---|---|---|
| SCN001/002; AC001/002/004/005/006 | Independent N module/tools/distribution | Exact108-input carry verification,47 current source/license/pin/removal checks; API001 Go/Python/workflow/compiler/manifest evidence | No sibling source dependency; compile is not target runtime/publication |
| SCN006; AC009 | Host-only trusted active/pending admission and lifecycle | Unchanged actual store/lock/files/refusal controls carried N01 | Privileged engine/mount effects doubled; no live upgrade |
| SCN003; AC003/006 | Ordinary workspace/run/PTY and generic launcher | S02/03 path errors, S04 composed file/skill APIs, S05 real native PTY/WebSocket/current run-memory, S06 Bash launcher fixture | No mounted-filesystem contract; Docker executable doubled |
| SCN007; AC010 | Filesystem-independent private configured profiles | S02/03 actual files/aliases/collisions/ownership and native Codex/Grok scripted children; S04 private skill publication/import | Claude client/model/remote source fixtures, not authenticated inference |
| Integrated inputPreface/publication/memory | Shared runtime integration preserves exact ownership | Expanded S03 all agent-execution +memory/notice units, Brief/skill-notice integration, core preface/collector/pipeline; S05 current native memory lifecycle | Scoped integration, not all imported product features |
| Guide; AC005 | Factual null-release/disabled UI | Current4 component suites/bothguards; exact Guide/catalog equality to carried IR001 EN/zh wide/narrow render proof | Presentation-only carry, no new browser/desktop journey |
| SCN004; AC007 | Ordered finalization | Not executed, Delivery-owned | Fresh refs/ordered N then S and PM preservation remain downstream |
| SCN005 | Live mount/platform/provider/old editor campaigns | Out of scope, Not Tested | No qualification inferred |

## Durable coverage validity and changes
All current R2 tests are Still Valid: N installation_state/install_state/standalone_state and host safety/packaging suites; S registered-workspace/native resolution, prepare-private-runtime-skills/runtime-skill-profile/private-skill-bootstrappers, Codex/Grok process tests, backend activation/cancellation/close owners, composed routes/run/PTY, generic launcher/Guide.
IR003/004 cleanup retains assertions and current prompt/team-kind/approval contracts; only unused fixture inputs/imports removed. Fresh overlap28 and narrow34 precede expanded broad units, where they repeat. No test is stale or unclear under approved R2. No uncovered supported critical API behavior was found requiring an added durable test or temporary product probe. API durable/production changes: None. Evidence-only orchestration/audits are not shipped test framework changes.

## Legacy and persisted transition
Implementation Legacy/Compatibility/Persisted sections read and consistent. Host-only absent/null/empty Nodes directly usable, current writers omit Nodes; meaningful/malformed active/pending obligations refuse under admin lock before effects. No history scan, migration, dual-version runtime or source deletion. S ordinary path/error semantics, no mount/UUID/classifier/Git-trust/paired pin restoration. Profiles exact-owned pre-await and close-before-release; no-binding no acquisition/project fallback. Project skills, credentials/history/registry untouched.

## Completed repository and broader decision
All current planned checks passed on S60b67; carried independent N evidence remains exact. See canonical report and evidence/api-e2e/api-rev-002/execution-summary.json. No failed execution attempt this round. API001 failures remain historical and resolved, not erased.
Seven applicable confidence categories95% each; mean95%, no category below90%, all critical API-owned ACs directly supported. **Broader validation: Not Required beyond executed repository-native process/API/PTY surfaces.** Real files/registered errors, child transports, current composed local server, native shell/PTY/WebSocket, memory/publish/lifecycle integration already exercise the changed R2 boundary. Unchanged privileged N backend and current pre-effect refusal are bounded fixture claims, not live qualification. No authored browser/shell behavior changed in integration; component inputs remain exact and fresh component controls pass. New VM/mount/paid-provider/desktop campaign would expand scope, not close a material extraction gap.
E02 cleaned the only API002 archive after source/fixture/protected data and process/cwd verification. No user-only dependency or new finding. Proportional successful-test gate is next, not immediate Delivery.
'''
(T/'api-e2e-coverage-investigation.md').write_text(head)
report='''# API/E2E Execution Coverage Report

## Latest authoritative result
**API-REV-002 — Pass /95.00% (2026-10-18), current integrated extraction scope.** Large / High / Reviewed. E01/S01–06/E02 freshly Pass; N01–03 Still Valid / carried Pass after exact108-input verification. All11 case groups reconciled; no unresolved in-scope failure, blocked or unstarted case. No API production/durable-test changes. Proportional successful-test review required before Delivery resumes.
This is extract-autobyteus-nfs, not a reopened shared-filesystem/editor Task. No storage/platform/provider/publication/end-user verification implied. AC007 and Delivery DR001 remain downstream.

## Round identities and governing inputs
Trigger CRR005 Pass100 over IR004/IR003 integrated recovery after DR001. R2/SR003, ReadySR004/ARCH002 unchanged. Full requirements/investigation/design/solution history/supplement and implementation/review/history accepted; eight authority docs verified unchanged from API001. Current investigation and ledger were updated BEFORE execution; history preserved in api-e2e-revision-record.md.
N=/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs; input HEAD062b5da0c9ba78bf5573feafaf0356fee2cf88f9; service83726b27400b405a7a6a79bd962d8e2419daa561 unchanged.
S=/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs; tested **60b67dabecaf5569a8e26128dbdb26117c988811**, branch codex/extract-autobyteus-nfs. Merge156ea2d integrates personal2f211340; only three test files authored after merge, current exact source archived.
Prior API001 Pass95 / CRR003 applies to Sa2023feff, not current integrated S. DR001 is Delivery-owned Blocked—Local Fix; this report supplies new API evidence without declaring delivery complete. Known obsolete R1 prose in S RELEASE.md remains a required Delivery docs-sync item.

## Impact, execution and case results
Current TESTING.md core/contracts/harness/fixture impact rule: ALL S01–06 rerun, not only the removed unused Skill import. E01/E02 fresh. N01–03 unchanged and carried with original limits. Full before-plan/diff and carry proof: [validation-plan](evidence/api-e2e/api-rev-002/validation-plan.md), [carry-validity](evidence/api-e2e/api-rev-002/carry-validity.json), integrated-changed-paths.txt.
Evidence **E2** = evidence/api-e2e/api-rev-002; **E1** = evidence/api-e2e/api-rev-001. Exact commands/cwd/exits/durations in E2/commands.jsonl; environment/tool versions and source hashes in E2/environment.json, toolchain.json and input-audit.json.

| Case | Result / attribution | Evidence and boundary |
|---|---|---|
| E01 | Fresh Pass | E2/source-contract-audit.json:47 current source/license/pin/Guide/removal checks; E2/archive-integrity.json:7307 exact S inputs +11 replay fixtures;108 N exact to E1 |
| N01 | Carried Pass, NOT rerun | E1/nfs-focused.log, nfs-race.log, nfs-vet.log;7 packages,59 top-level/252 incl subtests; real trusted store/lock/refusal before doubled effects |
| N02 | Carried Pass, NOT rerun | E1/nfs-python.log:19 executed/1 child skip; actionlint/shell/sourcehash/refusal logs. Go parent exercises permission child |
| N03 | Carried Pass, NOT rerun | E1/binaries.json, engine-check.json, native-version/build logs;4-target compile, native version and actual arm64 embed, not runtime qualification |
| S01 | Fresh Pass | E2/consumer-install/build/typecheck/nuxt-prepare logs; whole frozen install and documented current prerequisites/builds |
| S02 | Fresh Pass | E2/consumer-overlap.log and consumer-narrow.log; current Claude/Codex overlap plus7 path/profile/native-child controls |
| S03 | Fresh Pass | E2/consumer-unit.log, consumer-integration.log, consumer-core.log; expanded activation/runtime/path/memory/notice ownership, integrated Brief/notice and core input-preface |
| S04 | Fresh Pass | E2/consumer-routes.log; current composed HTTP/GraphQL/inject file/skill contracts, ordinary owned files/bytes/MIME/containment/removal |
| S05 | Fresh Pass | E2/consumer-path-pty.log; current run/memory lifecycle and native PTY/WebSocket actual cwd/home/error/close/churn |
| S06 | Fresh Pass | E2/consumer-launcher/guide/localization/web-boundary logs; generic Bash/Docker-command fixture + disabled Guide/components/guards |
| E02 | Fresh Pass | E2/cleanup.json and cleanup-preflight.json; only own archive removed, no owned process/cwd, source/protected inputs exact |

## Acceptance-Criteria Proof
Critical proof uses current S and verified unchanged N only. AC identifiers without hyphens in older ledger rows mean the same approved ACs.
Evidence folder absolute: /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs/tickets/in-progress/extract-autobyteus-nfs/evidence/api-e2e/api-rev-002

| AC | Cases | Direct evidence / conclusion |
|---|---|---|
| AC-001 | E01/N01–03 | E2/carry-validity.json + E1/archive-integrity.json/nfs-race.log/nfs-python.log/binaries.json: independent unchanged N archive/toolchain has no S dependency |
| AC-002 | N02/03 | E1/nfs-python.log/nfs-source-hash.log/binaries.json/engine-check.json, exact N equality E2: root layout/hash/invalidation/manifest/embed/four compilations |
| AC-003 | S02–06 | E2/consumer-narrow.log/consumer-unit.log/consumer-routes.log/consumer-path-pty.log/consumer-launcher.log: ordinary selected path/error/file/run/native PTY/generic mapping |
| AC-004 | E01 | E2/source-contract-audit.json: exact license/CLA/notices/section7 content and pinned engine recipes, unchanged N inputs |
| AC-005 | E01/N02/S06 | E2/source-contract-audit.json/consumer-guide.log + E1/nfs-publish-refusal.log/nfs-python.log: empty qualification, refused publish, disabled Guide |
| AC-006 | E01/S01–03/S06 | E2/source-contract-audit.json/consumer-build.log/consumer-typecheck.log/consumer-unit.log/consumer-launcher.log: removed coupling absent; current integrated owners/builds execute |
| AC-007 | None; Delivery-owned | **Not Tested / not achieved here**. Fresh target refs, ordered N→S finalization/push/cleanup and D0 PM preservation remain downstream |
| AC-008 | All/E02 | E2/commands.jsonl/execution-summary.json/cleanup.json + canonical ledger/history: exact identity, traceable current/carried proof, honest skips and cleanup |
| AC-009 | N01 | E1/nfs-focused.log/nfs-race.log + E2/carry-validity.json: current host-only direct reader, incompatible active/pending refusal under lock before effects, lifecycle controls unchanged |
| AC-010 | S02–05 | E2/consumer-narrow.log/consumer-unit.log/consumer-integration.log/consumer-routes.log/consumer-path-pty.log: exact private owner, pre-await/no-binding/no-fallback, alias/collision/source preservation, close/retry/release and integrated activation/memory |

## Fresh counts (separate runs, not additive unique coverage)
'''+count_lines+'''

Overlap28 and narrow34 are repeated within broad units, not extra unique tests. IR0031666/21/15/24/34 and final76 are Implementation-attributed historical/local checks, not added to API execution totals. Raw API002 logs/commands are the current evidence.
Six gated live AGY tests/four files remain skipped, not Passed. Launcher2 skips are disclosed in its raw log (PowerShell unavailable and occupied default collision port); controlled busy-port fixture still executes without touching the occupying service. No authenticated provider or real Docker qualification. N standalone child skip and Go-parent execution remain distinct carried facts.
Fresh install warnings about devkit bins before documented build and ignored unrelated @google/genai build script are retained. No dependency/security policy loosened or source upgraded. Current preparation produced the required outputs. Toolchain: Node22.21.1, pnpm10.28.2, test Python3.14.2, Darwin arm64; orchestrator system Python3.9.6. No new Go/toolchain/engine download or N execution.

## Attempts / findings / persisted-data disposition
No failed execution/preparation attempt this round. Prior API001 replay-fixture and Nuxt-preparation failures remain in its logs/history and were resolved there; this round included exact11 replay fixtures and Nuxt prepare upfront. Current CR001/CR002 are source-review-resolved; no new defect or test validity ambiguity found. No assertion weakening or production change.
The E01 copied audit event's phrase 'independent archives exact' refers to fresh S archive plus exact carried N input identity; **no second fresh N archive/run occurred in API002**.
Approved Directly Usable—No Migration remains: host-only absent/null/empty Nodes usable, current writes omit Nodes; incompatible active/pending obligations refuse before effects, unknown harmless fields/history inert. No compatibility version branch, mount classifier/Git trust/pin, migration or scan/sweep introduced. Profiles remain exact-owned; project skills/history/credentials not rewritten. Legacy/Compatibility/Persisted sections agree with observed source and tests.

## Confidence and broader-validation decision
| Mandatory category | Post-repository | Final | Evidence / residual limit |
|---|---|---|---|
| Requirement and AC proof |95%|95%| All critical API-owned ACs directly evidenced; AC007 explicit downstream boundary, no release/platform inference |
| Changed-boundary execution directness |95%|95%| Current real files/paths/profile owners/builds/native children and exact carried store/locks; privileged N effects doubled |
| Cross-boundary realism / mock gap |95%|95%| Actual local HTTP/GraphQL/PTY/WebSocket + native scripted children + fresh integrated runtime/core; Claude/model/remote-fetch doubles are not paid-provider proof |
| Environment/configuration/identity/fixtures |95%|95%| Fresh7307+11 exact-source archive, private HOME/TMPDIR/store, frozen deps/current builds; one Darwin arm64 host only |
| Failure/edge/lifecycle/recovery |95%|95%| Exact cleanup/cancel/retry, alias/collision/source safety, registered errors, native close/churn, integrated notice/memory; no live outage/upgrade/reboot claim |
| User-surface/browser/desktop-shell |95%|95%| Fresh Guide/component/guards; byte-exact Guide/catalog vs IR001 EN/zh wide/narrow render evidence; no new authored UI/shell behavior or browser rerun |
| Durable regression quality/relevance |95%|95%| Current approved path/ownership tests, expanded affected regression and real socket/process layers; explicit tracked ticket replay dependencies |

Overall post-repository/final **95.00%**, equal mean; no category below90%, no missing/failing critical API-owned criterion.
**Broader validation: Not Required beyond executed repository-native process/API/PTY surfaces.** They already cross the actual changed filesystem/registered-path/process/socket/memory/publication boundaries. Unchanged host backend equality and pre-effect admission proof do not require a new mounted campaign. Integrated Guide presentation inputs unchanged, fresh component checks pass. A new paid-provider/VM/mount/browser/desktop campaign would expand qualification rather than close a material R2 uncertainty.
No only-user-checkable dependency is needed for this verdict. Live installed upgrades/mounted/cross-OS/physical/provider/signing/hosted-publication remain Not Tested, not a questionnaire or implied Pass.

## Changes, cleanup and next stage
API durable tests added/updated/removed: **None**; production edits: **None**. Current three post-merge fixture cleanups were already source-reviewed CRR004/005; E2/test-review-scope.md identifies them for proportional successful-test gate. Temporary scripts only orchestrate current-source archives, documented checks, evidence and cleanup; no shipped framework addition.
Single API002 archive/home/tmp/store/dependencies/builds removed after no owned process or cwd.108 N and7307 S source inputs,11 current replay fixtures,9 protected PM/retained-engine files unchanged. D0 remains unborn main. No user app/node/VM/mount/firewall/credential mutation, target ref fetch/merge/push/tag/release/deploy/TaskDone/user verification. Assigned worktree old dist untouched.
Fresh routing required: successful-test gate first, then normal Delivery continuation. Delivery must refresh targets, sync obsolete S RELEASE.md R1 tail and own AC007 ordered finalization; DR001 not overridden here. No duplicate informational dispatch or reopened old filesystem/editor Task.
'''
(T/'api-e2e-execution-coverage-report.md').write_text(report)
p=T/'api-e2e-test-case-ledger.md';s=p.read_text().replace('## Ledger Meta','## API-REV-001 Ledger Meta (historical)',1).replace('## Final Reconciliation','## API-REV-001 Final Reconciliation (historical)',1)
s+='''\n## API-REV-002 final reconciliation
Fresh E01/S01–06/E02 Pass at S60b67dabecaf5569a8e26128dbdb26117c988811; N01–03 carried API001 Pass only after exact108 independent N input equality. Seven fresh case checks plus E02 and three carried groups =11 groups. No failed, blocked, interrupted or unstarted current case. All15 current commands exit0. Narrow/overlap repeat inside broad; do not add as unique. See execution-summary.json and test-counts.json for exact fresh counts/skips. API002 Pass95% covers current executable extraction scope only. No new N campaign; copied E01 audit phrase is clarified in the report. AC007/DR001 and stale RELEASE docs remain Delivery-owned.\n'''
p.write_text(s)
p=T/'api-e2e-revision-record.md';prior=p.read_bytes();write('prior-history.json',dict(bytes=len(prior),sha256=hashlib.sha256(prior).hexdigest()))
entry='''\n## API-REV-002 — Current integrated consumer validation
2026-10-18. Trigger CRR005 source Pass100 after IR003/IR004 integrated recovery from DR001. Prior API result **API001 Pass95% at Sa2023**, not current integrated proof. Current **Pass95%**, S60b67dabecaf5569a8e26128dbdb26117c988811; unchanged N83726b. Approved R2/SR003, ReadySR004/ARCH002, Large/High/Reviewed unchanged.
Before execution recorded all-case impact plan and complete old→new path diff. Current shared-foundation rule invalidates allS01–06; all personally rerun with fresh frozen install/current builds/typecheck/private environment. E01/E02 fresh; N01–03 exact108-input carry with original privileged-double/compile/skip limits. Expanded current agent-execution/memory/notice regression, core input-preface/pipeline and Brief/notice integration; actual composed APIs and native run-memory/PTY/WebSocket rerun. Current logs/counts at evidence/api-e2e/api-rev-002; overlap not unique-added.
No failed current attempt or in-scope finding. Historical API001 setup failures remain preserved/resolved; exact replay fixtures and Nuxt preparation included upfront. CR001/CR002 source closures retained, no source verdict invented. No API durable-test/production changes, only evidence orchestration. Current Guide presentation unchanged; no new browser/mounted/paid-provider/old editor campaign or platform/publication claim.
All11 case groups reconciled (8 fresh/3 carried); seven confidence categories95, average95; broader validation Not Required beyond actual repository-native process/API/PTY surfaces. Own single scratch removed after exact source/fixture/protected data and no-owned-process/cwd checks; D0 unborn PM preserved. No target/release/TaskDone/user verification action.
Proportional successful-test gate required; DR001/AC007/fresh targets/ordered finalization and stale S RELEASE R1 docs tail remain Delivery-owned. Prior API001 entry bytes retained unchanged before this append.\n'''
with p.open('a') as f:f.write(entry)
(E/'checks-and-limits.md').write_text('''# API-REV-002 current integrated validation

Current S60b67; unchanged N83726b. All15 current command exits0,8 fresh case groups and3 exact-input carried N groups. Seven-category95% confidence. Canonical report has the AC proof and actual mock boundaries. API-owned source/durable-test delta: none. Test review scope is test-review-scope.md; no renewed source/architecture review requested.

'''+count_lines+'''\n
N01–03 carried, not rerun. Overlap28/narrow34 repeat within broad1666; no unique count sum. Six AGY live skips and2 launcher skips remain unexecuted; model/remote-source/Docker effects scripted, no paid-provider/live-node claim. Actual local HTTP/GraphQL, native Codex/Grok protocol children, native PTY/WebSocket and DummyLLM memory lifecycle execute. Independent N privileged effects are fixture controls, underlying backend inputs unchanged. Source/readers/locks/state are actual files.

No failed current attempt. API001 failures preserved separately; fixtures and Nuxt preparation upfront. E01 copied phrase 'archives exact' does not imply a fresh N archive: carry-validity proves N unchanged and archive-integrity proves only fresh S. Install warning about devkit bins resolved by prescribed build; ignored @google/genai script policy unchanged.

Single own archive deleted, no own process/cwd, assigned7307S/108N +11fixtures +9protected inputs unchanged. No credentials/live app/VM/mount/target action. Current authority, ledger, raw commands and cleanup evidence persisted. Fresh successful-test gate, then Delivery; stale S RELEASE.md R1 tail/fresh targets/AC007 remain downstream.\n''')
(E/'attempts.md').write_text('''# Attempts — API-REV-002
No failed test/preparation command in this round. Source audit and all15 planned commands passed. Prior API001 replay/Nuxt setup failures were resolved there and remain in immutable evidence/history; current preparation includes both upfront. No test/production change or assertion relaxation. Native asynchronous negative-control logs are expected assertions, not failed commands. Copied E01 event wording is clarified in current report: only S was freshly archived, N exact108-input evidence carried. No hidden retry or provider/platform qualification.\n''')
print('canonical API002 artifacts finalized')
