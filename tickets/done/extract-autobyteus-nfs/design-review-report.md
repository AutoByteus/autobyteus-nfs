# Design Review Report — Extract AutoByteus NFS

## Review Round Meta

- Date / reviewer: 2026-10-16 / architecture reviewer; personal execution, no delegation.
- Upstream Requirements Doc: [requirements-doc.md](requirements-doc.md), **R2 Approved / SR-003**, user informed within explicit corrected direction.
- Upstream Investigation Notes: [investigation-notes.md](investigation-notes.md), current E12–E20; E01–E11 explicitly historical where superseded.
- Upstream Solution Revision Record: [solution-revision-record.md](solution-revision-record.md), **SR-003 / SR-004**.
- Reviewed Design Spec: [design-spec.md](design-spec.md), **SR-004 Ready**, destination input commit **983812e8b4fe3363909e44cc905285fc800ca19a**.
- Supplemental Task Artifacts Reviewed: [user correction](user-filesystem-boundary-correction.md), [held implementation checkpoint](implementation-evidence/ir-001/hold-checkpoint.json), [handoff](solution-design-handoff.md), prior canonical review and history.
- Architecture Review Revision Record: [architecture-review-revision-record.md](architecture-review-revision-record.md).
- Current Architecture Review Revision ID / round: **ARCH-REV-002 / 2**.
- Trigger: replacement review following the user's explicit filesystem-only application boundary; Task `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`.
- Prior Review Round Reviewed: **ARCH-REV-001**, Pass only for superseded R1/SR-002, retained in history and Git `5d354b91616c431a358f6024993ef1d52e682dc3`. No unresolved prior finding; prior coupling-preservation verdicts do not authorize current work.
- Latest Authoritative Round: **this report, ARCH-REV-002**.
- Workspaces: **N** `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`; **S** `/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs`; both branches `codex/extract-autobyteus-nfs`. N contains held extraction commits `353dd2c` / `0c9fd27` followed by SD recovery docs. S is clean at **390e0c76dda56c206ed8cabd65fc3564caaf1804**, extraction provenance **3712cd9bf0db998501d162db7f8655f169e3def6**.
- Current-State Evidence Basis: focused independent source reads below plus prior unaffected extraction review. N's preexisting untracked `implementation-evidence/` belongs to Implementation Engineer and is untouched. No production code, upstream design, scratch or live resource was changed by this review.

| Evidence | Independently inspected source / context | What it establishes |
| --- | --- | --- |
| V1 | R2, SR-003/004, current handoff/investigation/correction/checkpoint; N AGENTS/DESIGN/TESTING/RELEASE; S root design and package rules, server migration guideline; reviewer skill/principles/templates and reachability Example 9 | New approved basis; old policy clauses identified for correction, not precedence over R2; bounded state admission versus migration |
| V2 | S `agent-execution/services/{agent-run-manager,shared-run-workspace-admission}.ts`; `services/terminal-streaming/pty-session-manager.ts`; prior inspected binding/mount observer; current import search | Real activation and terminal gates, not merely unused fixture coupling |
| V3 | S `workspaces/{workspace-manager,filesystem-workspace}.ts`; Claude/Codex workspace resolvers; native shared helper and factory call sites | Registered workspace ownership and metadata-only workspace path; mount classification is removable without new path owner |
| V4 | S shared `prepare-private-runtime-skills.ts`, full `runtime-skill-profile.ts`; Claude bootstrap/cleanup and SDK plugin call sites; Codex bootstrap/factory/thread/client owner; ACP factory/release and Grok private adapter; provisioning `prepareFreshRun` | Existing private exposure, exact pre-await ownership, capability checks and close-before-release; production supplies execution memoryDir |
| V5 | S scoped Git-environment helper and all located callers; Docker entry/core/config/runtime/commands | Child safe.directory injection is actual behavior; generic bind roots/private volumes already exist independently of NFS attachment module |
| V6 | N `internal/cli/{run,install}.go`, `setup/{service,plan,apply,pending,lifecycle}.go`, config state/store and platform lock, service supervisor | Selected-node intent is persisted before node effects; installer currently replaces binary before administrative dispatch; correct new guard boundaries are concrete |
| V7 | N `internal/docker/{client,engine,snapshot}.go` and engine-used helper references | Docker engine identity/capability/config checks share types with app-node recreation; deletion must retain engine-used pieces |
| V8 | Prior ARCH-REV-001 distribution/license/file inspection and current extracted policies; current held checkpoint and Git state | Reuse unaffected extraction decisions only; no build/test readiness carried forward; R1 integration docs must be rewritten |

No product tests/builds, provider requests, VM/container/mount actions, release/tag, deployment, remote push or cleanup were executed. Failed bootstrap is the implementer's reported preparation failure, not a reviewer test result. Discovery misses for guessed source filenames were corrected by source search; they establish no defect.

## Routing Classification Review

- **Large / High**, confirmed. The delta now changes runtime admission, configured-skill preparation, Git policy and privileged host/node ownership as well as extraction/distribution/finalization. This is not a mechanical relocation or content-volume classification.
- Independent review required: **Yes**. No classification correction.

## Upstream Behavior And Production-Path Basis Confirmation

- Overall Basis Status: **Confirmed**. R2 explicitly replaces prior protocol preservation; it is not an unapproved reviewer relaxation of R1.
- Approved change: AutoByteus consumes directory paths/ordinary filesystem results; NFS owns host sharing only. Removed app wrong-mount/UUID admission and automatic node management are no longer guarantees.
- Preserved boundaries: NFS host source/mount/permission/engine/pending safety, app identity/private state/project skills, licensing, closed publication and safe two-repo completion.
- Scope guardrail: UC-001–006 only. No live upgrade/migration, new provider/backend, mounted-path classification elsewhere, outage isolation, editor repair, old acceptance campaign or general framework.
- Prospective blocking Design Impact traceability: **Yes — none raised**. No remaining material ambiguity for architecture readiness.
- Design uses compact BEH001–006 / DS1–6 labels; these refer to requirements BEH-001–006 and the same stable subjects.

| Behavior ID | Kind | Design Alignment | Approved Trigger / Contract And Current Evidence | Target Path / Spine Coherence | Status | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| BEH-001 | Operational | Pass | Pass — contributor independently clones/builds; extracted Go/local tooling and prior V2/V3 review | Pass — DS1 remains standalone | Confirmed | Fresh independent archive checks downstream |
| BEH-002 | Contract | Pass | Pass — maintainer candidate command; closed qualification/installer/workflow baseline | Pass — DS2 service-only inputs, no consumer pin, same closed release gates | Confirmed | Recheck changed hash paths and refusal controls |
| BEH-003 | System | Pass | Pass — user selects registered workspace, activates/restores run or opens terminal; V2/V3/V5 traces | Pass — DS3 uses WorkspaceManager and normal cwd/file APIs; generic launcher binds remain | Confirmed | Remove callers and prove ordinary paths/registered error handling |
| BEH-004 | Operational | Pass | Pass — explicit two-repo request and preservation; held checkpoint and current Git state | Pass — DS6 preserves partial commits, integrates N main then S personal, no longer pins a protocol fixture | Confirmed | Fresh refs and exact receipts at Delivery |
| BEH-005 | System | Pass | Pass — operator host create/connect/reconnect/drained detach and predecessor-state preservation contract; V6/V7 | Pass — DS4 keeps host checks; bounded refusal protects active/pending node obligations before replacement/effects | Confirmed | Execute host-only, engine and incompatible-state controls |
| BEH-006 | System | Pass | Pass — configured skills during ordinary new/restore preparation and cancellation/termination; V4 | Pass — DS5 existing private profiles independent of filesystem, exact ownership/release and no project fallback | Confirmed | Actual profile/caller/process-fixture coverage, not just mocks of removed selector |

Prior unresolved findings checked after establishing this basis: **None**. The earlier Pass's preservation conclusions are superseded by changed requirements, not evidence of an implementation defect.

## Supplemental Artifact Coherence Verdict

| Artifact | Purpose / Scope Clear? | Linked To Core? | Internally Complete? | Consistent? | Status / Approval Applicability Clear? | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| User correction | Pass | Pass | Pass | Pass | Pass | Its initial hold language is explicitly historical; R2/SR-004 now govern |
| Held checkpoint | Pass | Pass | Pass for coordination | Pass | Pass | Existing owner retains failed preparation/scratch; no reset, new copy or success claim |
| Prior review/history | Pass | Pass | Pass | Pass as historical | Pass | ARCH-REV-002 replaces current result; retain ARCH-REV-001 history |
| Historical delivery/engine references | Pass | Pass | Pass for provenance | Pass | Pass | Not new qualification, not a renewed test campaign |

## Task Design Health Assessment Verdict

| Assessment Area | Result | Evidence | Required Action |
| --- | --- | --- | --- |
| Current posture present | Pass | Behavior Change + ownership refactor, not merely move | None |
| Root cause explicit/evidenced | Pass | App admits by NFS metadata; service controls app nodes; skill privacy/Git selected by descriptor | None |
| Refactor decision explicit | Pass | Remove coupling now, retain host owners and existing private profile support | None |
| Concrete response supports decision | Pass | Caller/removal map, engine retention, state admission ordering and focused validation | None |

## Spine Inventory Verdict

| Spine | Scope | Readable? | Narrative Clear? | Facade / Owner Clear? | Naming Clear? | Ownership Clear? | Off-Spine Separation? | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1 | Standalone development | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS2 | Candidate/distribution gates | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS3 | Workspace selection through ordinary operation/cwd | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS4 | Host setup and bounded supervisor reconciliation | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS5 | Runtime preparation through process/client close and profile release | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS6 | Two-repo finalization/receipt | Pass | Pass | Pass | Pass | Pass | Pass | Pass |

DS5 is not just a filesystem helper: the preparation factory owns acquisition before awaits, native client/process uses the profile, and cleanup proves close before release. DS4 preserves the existing serial administrative lock/reconciliation owner rather than adding a second coordinator. Existing error/event surfaces suffice.

## Boundary Encapsulation Verdict

| Boundary / Owner | Public Entry Clear? | Mechanisms Internal? | Bypass Controlled? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| App WorkspaceManager / filesystem APIs | Pass | Pass | Pass | Pass | Registered IDs resolve through existing manager; no private NFS state or mount observer |
| Runtime preparation/profile/native process | Pass | Pass | Pass | Pass | Exact preparation owner receives profile before staging; no source/credential ownership transfer |
| NFS CLI/setup/config | Pass | Pass | Pass | Pass | Host resources only; trusted private admission before installation/administrative effects |
| NFS Docker engine adapter | Pass | Pass | Pass | Pass | Retain engine inspect/start/stop/remove/validation; remove app discovery/recreation/HTTP/JS probes |
| Generic launcher | Pass | Pass | Pass | Pass | Directory mapping and private volumes, no hidden replacement attachment bridge |

## Dependency Direction / Forbidden Shortcut Verdict

| Boundary | Allowed Dependencies Clear? | Forbidden Shortcuts Explicit? | Direction Coherent? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| S ordinary file/run/terminal | Pass | Pass | Pass | Pass | No descriptor/CLI/UUID/mount-table dependency; no renamed generic mount checker |
| N service | Pass | Pass | Pass | Pass | No app API/module/node dependency; NFS's own source marker/connection remain internal |
| Runtime skills | Pass | Pass | Pass | Pass | Existing app-private execution path and source service; no filesystem classifier or project-exposure fallback |
| Build/test/docs | Pass | Pass | Pass | Pass | Independent roots, no sibling replace/submodule/paired fixture; factual cross-repository docs are not a runtime dependency |

## Interface Boundary Verdict

| Interface | Subject Clear? | Singular Responsibility? | Identity Explicit? | Generic Boundary Risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| Workspace ID → registered path | Pass | Pass | Pass | Low | Pass |
| RuntimeSkillProfile / preparation guard | Pass | Pass | Pass — execution-owned profile and source skills distinct | Low | Pass |
| Host Connection / Attachment / HostedFilesystem | Pass | Pass | Pass — source and installation identity retained, Nodes removed | Low | Pass |
| CheckStandaloneState(Store) | Pass | Pass | Pass — bounded active/pending obligation admission, not node interpretation | Low | Pass |
| Docker engine Snapshot/Object | Pass | Pass | Pass — only retained engine uses shape | Low | Pass |

## Existing Capability / Subsystem Reuse Verdict

| Need | Existing Capability Checked? | Reuse Sound? | New Support Justified? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Ordinary workspace/cwd | Pass | Pass | N/A | Pass | Manager and metadata-only FileSystemWorkspace already provide it |
| Private configured skills | Pass | Pass | N/A | Pass | RuntimeSkillProfile plus existing Claude/Codex/Grok adapters and exact cleanup |
| Generic container workspace | Pass | Pass | N/A | Pass | Existing root/shared and root/nodes/name mappings/private volumes |
| Host lifecycle and state safety | Pass | Pass | Pass | Pass | Existing lock/store/pending owner; small read-only refusal check is justified by REQ-009, not a migration framework |
| Distribution | Pass | Pass | N/A | Pass | Existing extracted packaging and engine manifest logic |

## Subsystem / Capability-Area Allocation Verdict

| Area | Allocation Clear? | Reuse / Extend / New Sound? | Supports Spine Owners? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| N config/setup/backend/platform/service | Pass | Pass | Pass | Pass | Host administration and persisted host semantics remain together |
| N docker | Pass | Pass | Pass | Pass | Reduce mixed module to actual storage-engine responsibilities |
| S workspace/runtime/preparation/terminal | Pass | Pass | Pass | Pass | Remove storage policy, retain operation/cancellation ownership |
| S launcher / N distribution | Pass | Pass | Pass | Pass | Each maintains its own product, not counterpart protocol |

## Reusable Owned Structures Verdict

| Structure / Logic | Extraction Evaluated? | Shared File Choice Sound? | Ownership Clear? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Engine-used Snapshot/Object/label helpers | Pass | Pass | Pass | Pass | Explicit retain/move before app-only file deletion |
| Private profile and preparation guard | Pass | Pass | Pass | Pass | One existing generic preparation helper, not per-runtime filesystem selectors |
| Node/public attachment protocol and fixture | Pass | N/A — remove | Pass | Pass | No new shared DTO or bridge replaces retired protocol |
| Generic skill materializers | Pass | Pass | Pass | Pass | Remove newly unreachable touched helpers; retain only actual remaining callers such as non-private ACP adapters |

## Shared Structure / Data Model Tightness Verdict

| Structure | Clear Fields? | Redundancy Controlled? | Overlap Controlled? | Core / Variant Choice Sound? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Host Attachment/Plan/Status | Pass | Pass | Pass | Pass | Pass | No Nodes/Public/retryConsumed; existing source-binding meanings retained |
| Private profile / runtime context | Pass | Pass | Pass | Pass | Pass | Existing per-execution roots/exposures, no new persisted registry or copied credentials |
| Connection fixture | Pass | Pass | Pass | Pass | Pass | Renamed for NFS client subject, not a cross-language application schema |
| Admission projection | Pass | Pass | Pass | Pass | Pass | Retired obligation presence only; empty/null harmless, incompatible/malformed active state refuses, exact current writes |

## File Responsibility Mapping Verdict

| File / Group | Singular/Clear? | Correct Owner? | Re-Tightened After Split? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| N cli inputs/run/install; deleted launcher.go | Pass | Pass | Pass | Pass | Thin host commands and pre-replacement admission; no app CLI |
| N config installation_state.go and host structs | Pass | Pass | Pass | Pass | Bounded safety read under existing trust/lock; no transformation or legacy execution |
| N setup apply/pending/lifecycle/status | Pass | Pass | Pass | Pass | Preserve host ordering/partial binding; remove node branches/public writes |
| N docker retained files vs app-only removals | Pass | Pass | Pass | Pass | Named engine helpers are retained before deleting mixed machinery |
| S run manager/resolvers/native/PTY | Pass | Pass | Pass | Pass | Ordinary registered path/preparation lifecycle; no replacement storage selector |
| S private skills/bootstrap/native launch/cleanup | Pass | Pass | Pass | Pass | Uniform existing capable-runtime exposure, no-bindings path explicit; remove implicit Git injection |
| S launcher entry/config/runtime, fixtures and tests | Pass | Pass | Pass | Pass | Remove download/source slots as well as callers, retain generic stop/mapping controls |
| N/S policies, documentation, Guide copy, source hash | Pass | Pass | Pass | Pass | Correct superseded R1 promises; no UI redesign or enabled release |

## Subsystem / Folder / File Placement Verdict

| Path / Item | Placement Clear? | Correct Boundary? | Mixed-Layer / Over-Split Risk | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| N internal/config/installation_state.go | Pass | Pass | Low | Pass | Small state admission concern; no migration subsystem |
| N existing runtime folders | Pass | Pass | Low | Pass | Retain host architecture, shrink Docker mixed owner |
| S existing workspace/runtime/launcher folders | Pass | Pass | Low | Pass | No new generic storage module or infrastructure policy in app |
| N filesystem-usage docs / connection fixture | Pass | Pass | Low | Pass | Actual standalone subject, no paired consumer fixture |

## Removal / Decommission Completeness Verdict

| Item | Obsolete Piece Named? | Replacement Clear? | Scope Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| S binding/mount observer/admission/native-shared helper | Pass | Pass | Pass | Pass | Remove production imports/wrappers/test hooks, use ordinary owners |
| S Git injection helper/callers | Pass | Pass | Pass | Pass | Remove automatic scoped trust, preserve operator environment; no wildcard trust |
| S configured-skill workspace fallback in capable runtimes | Pass | Pass | Pass | Pass | Private profile or no acquisition for no bindings; retain other real materializer callers |
| S NFS launcher module/list slot/hash/run/start and fixture/pin | Pass | Pass | Pass | Pass | Generic mapping/stop retained; protocol fully removed |
| N nodes/launcher CLI/public stores/app Docker methods and tests | Pass | Pass | Pass | Pass | Host lifecycle + engine adapter remain; unsupported obligations refused |
| R1 integration docs/policies/hash entries | Pass | Pass | Pass | Pass | Explicit rewrite to R2; historic tickets remain historical |

These paths are reachable today: their retirement is the approved behavior change, not a claim that the current source is already dead. After caller rewiring, newly unreachable touched helpers/tests must be deleted and confirmed by imports/builds. Static inventory is not executable completion evidence.

## Legacy / Backward-Compatibility Verdict

| Area | Wrapper / Dual Path / Legacy Runtime? | Clean Cut Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- |
| Cross-product runtime protocol | No target retention | Pass | Pass | No optional bridge, renamed mount detector or old node execution |
| Incompatible active state admission | No legacy execution | Pass | Pass | Narrow preserved-obligation refusal, not fallback interpretation/rewriting |
| Public descriptors / detached receipts | No current dependency | Pass | Pass | Inert external residue preserved, not scanned/deleted to infer readiness |
| Unaffected host state | No version branch | Pass | Pass | Same meanings, tolerant irrelevant fields, exact current writes |

## Persisted-Data Transition Verdict (When Applicable)

| Stored Subject | Decision | Reader / Invariant Evidence Sufficient? | Proportionate? | Migration Safety If Required | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| App registry/history/credentials/project source skills | Not Affected | Pass — existing path/profile owners, no schema rewrite | Pass | N/A | Pass | No scan or cleanup of historical project links/profiles |
| Current per-execution generated profiles | Existing exact ownership/release | Pass — V4 pre-await receipt and close-before-release | Pass | N/A | Pass | Future configured exposure uses private execution storage, not project fallback |
| Node-free NFS host config/pending source binding | Directly Usable — No Migration | Pass — V6, unchanged connection/source/installation semantics | Pass | N/A | Pass | Keep partial/unbound source rules; omit retired field on normal new writes |
| Active/pending node obligations | Preserve and refuse automatic adoption | Pass — V6 and MP-001/002 below | Pass | N/A — no conversion authorized | Pass | Before root binary replacement and administrative resource changes; old matching operator tool needed for recovery |
| Old public descriptor/completed receipts | Inert/preserved | Pass — detach removes active intent after owned effects | Pass | N/A | Pass | Not task-owned cleanup and not evidence of active obligation by themselves |

No new migration runner, versioned execution branch, journal, historical scan or backup-copy choreography. Refusal is capability-scoped to NFS administration; app/version/help/verify-release must not depend on old installation state. The proposed check cannot silently drop malformed active content, infer completion from residue, or replace the root binary before refusal. CLI installer and supervisor each require the existing lock at their respective admission boundary; this ordering needs executable controls, not only parser tests.

## Change / Refactor Safety Verdict

| Area | Sequence Realistic? | Temporary Seams Explicit? | Cleanup / Removal Explicit? | Verdict |
| --- | --- | --- | --- | --- |
| Resume held extraction | Pass | Pass — existing owner/commits/scratch, replacement dispatch only | Pass | Pass |
| N admission then host-only removal | Pass | Pass — retain engine-used types first and source/pending semantics | Pass | Pass |
| S caller/profile/launcher decoupling | Pass | Pass — no final bridge/fallback; exact async ownership retained | Pass | Pass |
| Tests/docs/independent builds | Pass | Pass — failed preparation remains evidence; R1 mechanical diff no longer sufficient | Pass | Pass |
| Two-repo finalization | Pass | Pass — fresh refs, ordered non-atomic completion, no paired fixture pin | Pass | Pass |

No live deployment transition is claimed. Old specially attached containers require explicit operator drain/reconfiguration outside this Task; generic mapping is not a promise of automatic transition or mount propagation.

## Example Adequacy Verdict

| Topic | Example Needed? | Present / Clear? | Avoided Shape Clear? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Ordinary directory semantics | Yes | Pass | Pass | Pass | Existing-but-unmounted directory remains ordinary; absent/malformed NFS metadata irrelevant |
| Private profile no-bindings/invalid parent | Yes | Pass | Pass | Pass | No acquisition for no bindings; invalid private path fails run, no project fallback; symlink aliases included |
| Old active/pending vs residue | Yes | Pass | Pass | Pass | Explicit supported/disallowed dispositions and pre-effect boundaries |
| Generic Docker mapping | Yes | Pass | Pass | Pass | Root/shared and root/nodes/name, not arbitrary mount-root identity |
| New framework/migration | No | N/A | Pass | Pass | Explicitly rejected; concrete existing owners suffice |

## Material Premise Validation (Only When Needed)

The following records confirm the revised guard's preservation basis; they do not add scenarios or a live upgrade campaign. Example 9's independent-origin rule was applied.

### MP-001 — Completed predecessor setup retains active selected-node obligations

- Authority / behavior: R2 REQ-009, AC-009 / BEH-005; retain unsupported active obligations rather than silently adopting them.
- Initiating kind / trigger: **User**; predecessor public create/connect with selected `--nodes`, approved setup consent, coherent goal of sharing that source with selected nodes.
- Evidence / forward path: N cli inputs/run/setup → setup.Plan copies requested node names into Attachment → Apply validates and SaveIntent → writes private attachment before EnsureVolume/Probe/Recreate/publishNode → successful setup removes pending intent but keeps active Attachment.Nodes. Source V6, not a synthetic JSON mutation, produces this state.
- Lifecycle / consequence: the configured installation still contains an obligation to those nodes until supported drained detach removes it. A later installation/administrative invocation of the new host-only tool cannot safely pretend it only owns a host mount. Existing InstallRoot replaces the root binary before normal Run, so checking only late setup code would be insufficient.
- Scenario validity / reachability: **Supported Normal Scenario plus explicit preservation contract / Reachable**. No claim such a live installation was inspected or upgrade executed.
- Review consequence: approve the bounded trusted-state refusal before binary replacement/effects, retaining matching-old-tool recovery externally. Do not keep old execution machinery or add automatic migration.

### MP-002 — Supported incomplete predecessor setup retains pending node intent

- Authority / behavior: REQ-009 / AC-009 and existing saved-setup retry contract, BEH-005.
- Initiating kind / governing contract: **Contract**; predecessor setup explicitly persists intended resources and exposes reconnect to review/resume incomplete setup. Preservation applies to that committed pending intent, not just completed active state.
- Evidence / forward path: operator consents to selected-node create/connect → Apply.SaveIntent writes pending Plan.Attachment.Nodes before package/source/export/mount/node effects → subsequent setup error returns without erasing intent → public reconnect reads pending plan and offers review/recovery. Source Apply/pending/Run implement that contract. No invented manual deletion, external corruption or arbitrary concurrent workflow is needed.
- Lifecycle / consequence: active attachment need not yet exist at the saved-intent boundary; inspecting only active attachment could miss an unresolved selected-node plan. Existing partial source binding separately constrains host recovery and must remain intact.
- Scenario validity / reachability: **Supported Explicit Edge Scenario / Reachable**, established by the governing saved-setup contract and production ordering; not a claim of a fresh reproduction.
- Review consequence: include the bounded pending envelope in the same refusal boundary. No receipt/workspace/history enumeration and no transformation/legacy recovery path.

## Unresolved Approved-Behavior Or Current-State Gaps

**None for the architecture decision.** Native provider operation, bootstrap/toolchain availability and executable candidate behavior remain downstream evidence obligations. Existing native adapter code establishes a reusable architecture, not fresh provider qualification. A demonstrated inability to honor R2 must return upstream, not trigger a silent project-file fallback.

## Review Decision

**Pass — ARCH-REV-002 / R2-SR-003 / SR-004.** The revised basis is confirmed and the design is actionable. This replaces the current ARCH-REV-001 result; it does not carry forward the rejected attachment contract. Resume the existing held implementation under this replacement basis only.

## Findings

**None.** No blocking Design Impact, Requirement Gap or Unclear issue established. No unrelated follow-up or old Task campaign created.

## Classification

**Pass; failure classification N/A. Large / High / independently reviewed.** This is a material behavior/ownership revision, not a docs-only acceptance adjustment or completed implementation.

## Recommended Recipient

Fresh rules select **`/software_engineering_team/implementation_engineer`** for architecture Pass / cumulative package ready for implementation. Send the replacement basis to that existing owner, not a new copy. Carry this report/history, R2 requirements, SR-004 design and current investigation/handoff/correction; checkpoint remains in the canonical ticket. Preserve existing scratch/evidence. Fail/Blocked does not apply; no duplicate dispatch or bulk evidence manifest.

## Residual Risks

1. **Removal completeness:** all actual admission/terminal/Git/profile/launcher call sites and dynamic module slots must disappear coherently. Ordinary registered workspace failure must not become a fallback to a different path. Compilation plus actual ordinary-path/caller fixtures are required.
2. **Private exposure behavior:** new ordinary-directory coverage expands use of existing native adapters. Validate no-bindings, unresolved/collision policy, symlink alias rejection, failed/cancelled preparation, concurrent profile ownership and close-before-release. Unsupported provider capability remains a truthful run failure, not permission to restore project materialization.
3. **Privileged reduction:** retain Docker engine-used helpers and identity/security checks, source/pending ordering and busy-detach refusal. Verify state admission at installation, CLI and supervisor boundaries before effects, including binary replacement; helper-only tests are insufficient.
4. **Intentional lost promises:** app cannot detect an unmounted-but-existing directory, wrong NFS source or mounted-state changes. It may receive ordinary Git ownership/I/O errors. No outage isolation, automatic container transition or global filesystem equivalence is implied.
5. **Policy/proof drift:** N's extracted R1 policy clauses and old review are not current authority. Correct source-hash inputs/docs/Guide claims; all qualification fields remain closed. No source/compile/fixture result can substitute for native/physical/signing/publication evidence.
6. **Execution/finalization pending:** failed Python bootstrap must be repaired in owned setup with its failed evidence retained. Fresh standalone and affected S checks and actual integrated identities remain required. Preserve D0 PM data, untracked implementation evidence, old assets and partial completion; do not reset/force/release/deploy.

## Latest Authoritative Result

- Review Decision: **Pass**.
- Material-Premise Gate: **Pass**, MP-001/MP-002 independently grounded.
- Current review: **ARCH-REV-002**, superseding ARCH-REV-001 only as current result; baseline history preserved.
- Applicable authority: **R2 / SR-003 Approved; SR-004 Ready**.
- Notes: replacement design review, no product tests or implementation acceptance. Source review, executable validation and Delivery remain with their owners. No new approval questionnaire, live-resource authorization, public qualification or completion claim.
