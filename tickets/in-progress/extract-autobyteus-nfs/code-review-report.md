# Code Review Report — Extract AutoByteus NFS

## Review Round Meta

- Date / reviewer: 2026-10-18 (source/checks performed 2026-10-16; unchanged input identities reverified on continuation) / code reviewer, personal execution; no delegation.
- Entry point / round / scope: **Implementation Review / 1 / Full Review**. Initial result **CRR-001**; prior review N/A, not an inferred Pass.
- Task: `extract-autobyteus-nfs` / `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`.
- Requirements / investigation / solution history: [requirements-doc.md](requirements-doc.md), **replacement R2 Approved / SR-003**; [investigation-notes.md](investigation-notes.md), E12–20; [solution-revision-record.md](solution-revision-record.md).
- Design / supplemental authority: [design-spec.md](design-spec.md), **SR-004 Ready**; [user-filesystem-boundary-correction.md](user-filesystem-boundary-correction.md); [solution-design-handoff.md](solution-design-handoff.md).
- Architecture: [design-review-report.md](design-review-report.md) **ARCH-REV-002 Pass**, [architecture-review-revision-record.md](architecture-review-revision-record.md). ARCH001/R1 are historical only.
- Trigger: Implementation Engineer's [implementation-handoff.md](implementation-handoff.md), [implementation-revision-record.md](implementation-revision-record.md), **IR-001 initial baseline**. Entire relevant artifact chain considered, not only its summary.
- Code review history: [code-review-revision-record.md](code-review-revision-record.md), CRR-001 initial baseline.
- N worktree: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`; reviewed HEAD **9208f8d4f81c78c537b4105773bae85dd74a0076**, service source **83726b27400b405a7a6a79bd962d8e2419daa561**.
- S worktree: `/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs`; reviewed HEAD **d3f7f67015587b4c8aa26824786be807793485d1**, production delta2448e166. Both `codex/extract-autobyteus-nfs`; extraction provenance S3712cd9bf0db998501d162db7f8655f169e3def6.
- API/E2E and Delivery revisions/reports/failing scenarios: **N/A for this new Task**. This is not a failure-origin review or old filesystem/editor continuation.
- Evidence shorthand: **E** = [code-review-evidence/crr-001](code-review-evidence/crr-001); **IR** = [implementation-evidence/ir-001](implementation-evidence/ir-001). Exact commands, failures, limits and cleanup: [E/checks-and-limits.md](code-review-evidence/crr-001/checks-and-limits.md).

## Routing Classification Review

**Large / High**, independently confirmed: extraction plus bidirectional runtime-boundary removal, privileged installation admission, persisted obligations, private runtime profile ownership and two-repository delivery. Independent source review required. No classification or architecture revision requested.

## Review Scope

Reviewed all six approved behavior spines; standalone development/package/installer/workflow, host CLI/config/setup/supervisor and retained engine lifecycle; S workspace/run/PTY resolution, Claude/Codex/Grok configured-skill preparation/release, AGY/native Git-policy removal, composition dependencies, generic launcher and Guide copy. Read actual production owners and representative tests; normalized comparison establishes unchanged host safety implementation, not a semantic shortcut for changed R2 code.

Policies: shared design principles and Example9; N AGENTS/DESIGN/TESTING and S root DESIGN/TESTING/package AGENTS; approved migration analysis. No conflict requiring changed requirements. No review of live installed state, no provider authentication, no old acceptance campaign, no editor modification. Delivery finalization/AC007 is deliberately not claimed complete.

## Upstream Behavior And Production-Path Basis Confirmation

**Confirmed** against replacement R2. Filesystem paths are the whole application integration boundary; app mount/UUID classification and service application-node control are intentionally removed, not missing safeguards to reinstate. No newly discovered behavior or material ambiguity.

| Behavior | Status | Current implementation path / lifecycle evidence |
| --- | --- | --- |
| BEH-001 / DS1 | Confirmed | Contributor clone -> root go.mod/cmd/internal -> service-owned tests/packaging -> independent build/check. Reviewer clean N snapshot uses no S dependency; service-only paths and original removal audited. |
| BEH-002 / DS2 | Confirmed | Maintainer candidate invocation -> local release.py/source hash/engine manifest -> manual workflow gates -> qualified metadata/installer refusal. Empty lock remains; source changes invalidate it; current hash independently reproduced. |
| BEH-003 / DS3 | Confirmed | Workspace selection/activation -> existing WorkspaceManager/resolvers -> provider workingDirectory or PTY session.start(cwd) -> ordinary OS file/process result. Registered errors propagate; unknown/no-selection fallback remains. Launcher maps ordinary root/shared and root/nodes/name; private volumes retained. No descriptor/mount observer/automatic Git trust in active callers. |
| BEH-004 / DS6 | Confirmed for current stage | Preserved two development histories -> explicit source/provenance/evidence -> future fresh target verification and ordered N then S finalization. AC007 remains Delivery-owned; no remote completion implied. |
| BEH-005 / DS4 | Confirmed | CLI consent/elevation -> private store/admin lock -> bounded active/pending admission -> host Plan/Apply or Reconnect/Status/Detach -> backend/mount/nonroot probe. Installer guard precedes root binary parent/replacement. Supervisor guard runs inside each serial locked reconcile. Source bind is saved before export/mount effects; detach unmounts without force before owned teardown. Docker retains only storage-engine identity/config/capability/lifecycle. |
| BEH-006 / DS5 | Confirmed | New/restore run -> provider bootstrap -> configured bindings -> ownSkillProfile before async prepare -> resolved private execution directory/profile -> native plugin/extraRoots adapter -> exact process/client close -> exact profile release. No bindings acquire nothing, no project-link fallback. Source resolution/collision handling and generic nonprivate ACP behavior retained. |

No prior finding applies. Existing preparation/cancellation ownership is reused; no new scheduler, migration framework, receipt scan or alternate storage abstraction introduced.

## Supported Product Scenario And Reachability Gate

| Scenario / contract | Kind / initiator, goal and supported entry | Forward path / lifecycle and consequence | Independent authority | Validity / use |
| --- | --- | --- | --- | --- |
| SCN-001 / REQ001,006 | Operational: contributor develops standalone N from checkout/archive | Root module/tools -> local sources/engine inputs -> compile/tests without app checkout | R2 standalone request; DS1; root tools | Supported Normal Scenario / Use |
| SCN-002 / REQ002,004,005 | Contract: maintainer creates nonpublishing candidate | release.py -> source/engine identity -> manual workflow and qualified metadata gates; unqualified publication refused | R2 licensing/preservation/closed-release contract, DS2 | Supported Normal Scenario / Use |
| SCN-003 / REQ003,006 | User: select supplied directory, start/restore run or terminal; operator configures generic container root | Existing workspace/resolver/activation -> cwd/file APIs or launcher binds -> ordinary result/error, no mount classification or fallback on known registration failure | User correction, DEC001/005/007, DS3 | Supported Normal Scenario / Use |
| SCN-004 / REQ007,008 | Operational: Delivery finalizes both repositories without losing existing work | Preserved branch/evidence -> fresh refs -> N then S/no-ff -> exact receipt, no forced partial-success claim | R2 two-target request; DS6 | Supported Normal Scenario / Use, future owner gate |
| SCN-006 / REQ009 | Operator: create/connect/reconnect/status/draineddetach of host storage | Locked trusted config -> source/backend/mount/probe or non-forced unmount -> host-only result preserving source/marker/private evidence | R2 host safety contract; DS4 | Supported Normal Scenario / Use |
| MP-001 / SCN-006 | Operational: install/administer host-only tool while predecessor active node obligations remain | Predecessor create/connect consent -> persisted active Attachment.Nodes -> new installRootBinary/Run -> guard refuses before replacement/backend effects | ARCH002 source-derived predecessor writer path; R2 no abandoned obligations | Supported Explicit Edge Scenario / Use |
| MP-002 / SCN-006 | Operational: retry after predecessor setup saved pending intent but did not complete | Predecessor SaveIntent before resource effects -> pending Plan.Attachment.Nodes -> new install/dispatch/supervisor guard -> refuse, retain bytes | ARCH002 interrupted-setup preservation contract and production ordering | Supported Explicit Edge Scenario / Use |
| SCN-007 / REQ010 | User/system: configured-skill runtime preparation, normal termination or supported cancellation | Existing run memory layout -> own profile pre-await -> source links/native adapters -> close-before-release; project/source/peer profiles preserved | R2 DEC006; DS5; current provisioning/preparation/process owners | Supported Normal Scenario and explicitly supported cancellation edge / Use |
| ENG-DEAD / Core Principle7 | Engineering contract: changed modules must not retain unused imports | Touched production files still contain five import bindings with no consumers -> unnecessary misleading dependencies in source | Mandatory shared no-dead-code rule explicitly includes preexisting imports in touched files | Supported contract / Use |

### Candidate Finding And Mechanism Gate

| ID | Observation / mechanism | Independent basis / trigger | Path, lifecycle and consequence | Evidence | Disposition / scope / proportionate response |
| --- | --- | --- | --- | --- | --- |
| C-001 | Five unused import bindings in three touched runtime files | ENG-DEAD, not an invented runtime failure | Factories and manager were modified in R2, but those local names have no reference. TypeScript reports6133. Cleanup contract unsatisfied; no runtime breakage attributed | E/unused-imports.json + direct full-file reads; base inspection confirms preexisting provenance; current diff confirms all three files touched | **Promote / This ticket / CR-001**. Remove only unused bindings; preserve actual symbols and public re-export. No behavior redesign/new test campaign. |
| C-002 | Active/pending obligation refusal and private-profile path/ownership checks | MP001/002, REQ009/010 | Protect actual predecessor persisted obligations before binary/resource effects; private configured exposure stays outside selected project and retained until child close | Installer/Run/setup guard trace; RuntimeSkillProfile/preparation/native managers; independent N checks, IR local profile tests | Promote as justified existing mechanisms, **not defects**. Keep bounded current owners; no migration/history scan or new machinery. |
| C-003 | Search hit for removed launcher-attachment command in test | No supported active production caller | cli_test.go passes removed option specifically to assert parser refusal; not a current action implementation | Raw audit attempt-2; corrected production-only scan | **Reject — Not Reachable as active implementation**. Negative regression remains valid; no deduction. |

## Structural / Design Checks

| Check | Result | Evidence | Required action |
| --- | --- | --- | --- |
| Task design health assessment present/evidence-backed/preserved | Pass | R2 boundary refactor; DS1–6 match current owners | None |
| Approved supplemental artifacts matched | Pass | User correction and ARCH002, not historical R1 | None |
| Data-flow spine inventory clarity/preservation | Pass | Six complete trigger-to-effect paths above | None |
| Ownership boundary preservation/clarity | Pass | App paths vs N host owner; profiles stay runtime-owned | None |
| Off-spine concerns serve clear owners | Pass | Config admission, profile exposure, packaging identity bounded | None |
| Existing capability/subsystem reuse | Pass | Existing Store, lock, workspace manager, preparation and native clients | None |
| Reusable owned structures | Pass | One profile builder and trusted state admission, no provider-specific copies | None |
| Shared-structure/data-model tightness | Pass | Host Attachment loses Nodes; ACP private/generic union prevents conflicting adapters | None |
| Repeated coordination ownership | Pass | Existing preparation/thread/session owners retain exact release | None |
| Empty indirection | Pass | Removed admission wrapper; surviving owners own actual policy/lifecycle | None |
| Scope-appropriate separation/file responsibility | Pass | Distribution/config/host orchestration/runtime profiles remain separate | None |
| Ownership-driven dependency direction | Pass | No app/service runtime imports; no sibling module/build dependency | None |
| Authoritative Boundary Rule | Pass | WorkspaceManager, session/thread managers and config.Store remain authoritative | None |
| File placement | Pass | Admission under config, native profile under shared runtime concern | None |
| Flat versus over-split layout | Pass | Existing small owners reused, obsolete modules removed | None |
| Interface/API/command boundaries | Pass | Host-only commands; exact profile/lease identities; ordinary cwd | None |
| Naming/responsibility alignment | Pass | Connection fixture is service input, not public app attachment contract | None |
| No unjustified duplication | Pass | Shared private preparation and engine helpers retained once | None |
| Patch-on-patch complexity control | Pass | Clean removal, no old/new strategy branch or compatibility bridge | None |
| Dead code removed in touched files/modules | **Fail** | C-001 / CR-001: five unused import bindings | Bounded import cleanup |
| Relevant test scenarios/assertions clear | Pass | Admission pre-effect refusal, no-binding/source/collision/exact release, ordinary registered paths | None |
| Test fixtures/helper coherence | Pass | Test-owned stores/profiles/processes; independent N tests; intentional provider doubles | None |
| No stale/duplicated/compatibility-only tests | Pass | Old app-node/paired/admission/materializer tests removed; generic launcher and negative option checks preserved | None |
| API/E2E readiness | Pass | Explicit evidence map/local checks and honest limits; no ambiguous product contract | After cleanup/review, proportional current validation only |

## Source File Size And Structure Audit

Full per-file counts and normalized deltas: [E/source-size-audit.md](code-review-evidence/crr-001/source-size-audit.md), machine evidence [E/source-audit.json](code-review-evidence/crr-001/source-audit.json). Original S3712cd9b mapped to N for extraction, not a misleading all-new-file count. Test/fixture/generated evidence and translation payload excluded from implementation thresholds. The workflow is separately included. No >500 growth or >220 normalized delta requiring a split; largest production owner is native backend factory473 nonblank before/after. This does not waive CR-001.

## Legacy / Backward-Compatibility Verdict

| Check | Result | Notes |
| --- | --- | --- |
| No compatibility mechanism | Pass | No paired pin, descriptor fallback or legacy execution path |
| No legacy old-behavior retention | Pass | App node management, mount admission and automatic Git trust removed |
| Dead code removed in touched files/modules | **Fail** | CR-001 only; do not mislabel unused imports as an active old runtime |
| Approved persisted transition followed | Pass | Host-only state directly usable; incompatible active/pending obligations refused; no user data rewritten |
| No version-specific dual read/write | Pass | General trusted envelope inspection, not version branching |
| Transition mechanics proportionate | Pass | Two bounded current records under existing lock; no historical receipt scan/migration |

## Dead / Obsolete / Legacy Items Requiring Removal

All paths below are relative to **S**. Import bindings only; do not remove exported domain classes/types or behavior.

| Item / path | Type | Evidence | Why / required action |
| --- | --- | --- | --- |
| Claude backend/claude-agent-run-backend-factory.ts:6 `AgentRunConfig`, :7 `RuntimeAgentRunContext` | DeadCode / unused imports | TypeScript6133; zero use outside import | ENG-DEAD; remove these two bindings, retain AgentRunContext |
| Codex backend/codex-agent-run-backend-factory.ts:5 `AgentRunConfig`, :6 `RuntimeAgentRunContext` | DeadCode / unused imports | TypeScript6133; zero use outside import | Same bounded cleanup |
| Claude session/claude-session-manager.ts:3–5 local `ClaudeSessionEvent` import | DeadCode / unused import | TypeScript6133; separate direct re-export at:22 supplies public API | Remove local import **only**, keep direct public re-export |

Full prefixes and diagnostic lines are in E/unused-imports.json. These bindings predate extraction, but all three files are actively changed and Core Principle7 explicitly makes their cleanup part of this ticket. No runtime defect or performance penalty is claimed.

## Docs-Impact Verdict

**Yes**, and current extraction/usage/policy/Guide references reflect host-only service and ordinary app paths. Licenses/provenance preserved. Guide remains release=null/disabled; inspected two screenshots from the implementation's four-state render proof. No new UI or editor scope. Delivery still owns final integration docs/receipts; CR-001 needs no product documentation change.

## Additional Material Premise Validation

| Upstream premise | Status | Verification |
| --- | --- | --- |
| MP-001 active predecessor obligations | Confirmed | Existing writer persistence path plus locked installer/dispatch refusal before effects; tests retain state and target bytes |
| MP-002 pending predecessor obligations | Confirmed | SaveIntent precedes resource changes; guard separately checks pending Attachment; supervisor cannot silently resume it |

No additional behavioral premise invented. No requirement for app mount-loss classification, automatic Git trust, provider-authenticated testing or historical cleanup was inferred from technical possibility.

## Review Scorecard

Overall **9.88/10 = 98.8/100**, arithmetic mean for visibility, **not approval**. One mandatory cleanup gap makes the result Fail; all other categories have no evidenced in-scope defect. No deduction for historical limits or unsupported scenarios, no double penalty for the same imports.

| Priority | Category | Score | Reason | Weakness / improvement |
| --- | --- | --- | --- | --- |
| 1 | Data-Flow Spine Inventory and Clarity | 10 | DS1–6 independently traced to meaningful effects | None demonstrated |
| 2 | Ownership Clarity and Boundary Encapsulation | 10 | Filesystem-only app boundary and host-only service respected | None demonstrated |
| 3 | API / Interface / Query / Command Clarity | 10 | Removed obsolete options; exact profile/lease/current-state contracts | None demonstrated |
| 4 | Separation of Concerns and File Placement | 10 | Existing concern owners preserved, no replacement framework | None demonstrated |
| 5 | Shared-Structure / Data-Model Tightness and Reusable Owned Structures | 10 | Host state narrowed; profile builder shared; ACP variant explicit | None demonstrated |
| 6 | Naming Quality and Local Readability | 10 | Subjects and scope explicit; no size pressure | None demonstrated |
| 7 | API/E2E Readiness | 10 | Evidence map/checks/limits support proportional validation once cleanup clears | No separate readiness defect; downstream not yet executed |
| 8 | Runtime Correctness And Behavioral Fidelity | 10 | Supported paths match R2; N independently green; S traces and attributed implementation evidence coherent | No established runtime defect; not live qualification |
| 9 | No Backward-Compatibility / No Legacy Retention | 10 | Clean-cut behavior and bounded refusal, no compatibility execution | None demonstrated |
| 10 | Cleanup Completeness | **8.8** | Most obsolete owners removed, but C-001 violates mandatory touched-file rule | Remove five unused bindings; focused source re-review, no design change |

## Findings

### CR-001 — Remove five unused imports in three touched runtime files

- **Low severity; mandatory cleanup; Local Fix (implementation-owned)**. Candidate C-001 / engineering contract ENG-DEAD.
- Exact items are enumerated above and compiler-confirmed in E/unused-imports.json. All are preexisting bindings in files changed by this refactor; the shared no-dead-code rule explicitly applies here.
- Consequence: unnecessary, misleading source dependencies remain in the current refactored owner. **Not** a proven runtime failure, broken extraction or architectural defect.
- Response: remove only those local import bindings, preserve the ClaudeSessionEvent public re-export and real classes/types. Do not expand into unrelated unused-code cleanup, provider changes or new product requirements. Rerun a focused no-unused check and appropriate production typecheck; source review then proportionate API validation remain the existing route.

## Follow-ups

None. No new Task requested. Completed filesystem/editor Tasks remain closed; no old follow-up is reopened or carried as a blocker here.

## Classification

**Local Fix — implementation-owned**, limited to CR-001. No Design Impact, Requirement Gap or failure-origin attribution. The earlier architecture approval remains valid.

## Recommended Recipient

`/software_engineering_team/implementation_engineer`, subject to fresh routing rules. No API/E2E advance until cleanup/source re-review passes. No duplicate Designer/API/PM dispatch.

## Residual Risks

No live mount/export/installed upgrade/provider-authenticated/physical/platform/publication proof was performed here. IR four-target compilation is not native runtime qualification. Application deliberately treats an existing unmounted directory as an ordinary directory; operator owns storage/bind setup. Private profile source exposure uses existing native adapters, not proof of real inference. AC007 and fresh two-target finalization remain Delivery-owned; no release authorized. First reviewer source-test run failed only because its owned archive was under prohibited `/private` temp storage; corrected archive location passed unchanged source/tests. Raw failure retained, not hidden or attributed to product code.

## Latest Authoritative Result

- **Review Decision: Fail — CR-001 bounded import cleanup only.**
- Entry point: Implementation Review / Full Review / CRR-001.
- Supported Product Scenario Gate: **Pass**; Material-Premise Gate: **Pass**.
- Score: **9.88/10 / 98.8/100**; no score overrides mandatory cleanup.
- Failure origin: N/A, not an API failure-origin review.
- Recommended recipient: implementation engineer, then source re-review and proportionate API validation.
- Reviewer production/test modifications: **None**. Both input source identities preserved; owned scratch cleaned. No target finalization, release, TaskDone or user-verification claim.
