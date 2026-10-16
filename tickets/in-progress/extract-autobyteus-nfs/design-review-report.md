# Design Review Report — Extract AutoByteus NFS

## Review Round Meta

- Date / reviewer: 2026-10-16 / architecture reviewer; personal review, no delegation.
- Upstream Requirements Doc: [requirements-doc.md](requirements-doc.md), **R1 Approved / SR-001**.
- Upstream Investigation Notes: [investigation-notes.md](investigation-notes.md), E01–E11 / A01–A05.
- Upstream Solution Revision Record: [solution-revision-record.md](solution-revision-record.md).
- Reviewed Design Spec: [design-spec.md](design-spec.md), **SR-002** at destination input commit `381231ee90d1dc3e494e06768e18d082c6cd46d2`.
- Supplemental Task Artifacts Reviewed: [solution-design-handoff.md](solution-design-handoff.md); historical DR-002 handoff summary indexed in investigation. Historical raw campaigns were not re-audited or adopted as new acceptance results.
- Relevant Solution Revision IDs: **SR-001, SR-002**.
- Architecture Review Revision Record: [architecture-review-revision-record.md](architecture-review-revision-record.md).
- Current Architecture Review Revision ID / round: **ARCH-REV-001 / 1**.
- Trigger: new repository-separation Task `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`, Architecture Design Complete / Large / High.
- Prior Review Round Reviewed: **N/A**; neither review artifact existed. No result inherited from the completed filesystem/editor Tasks.
- Latest Authoritative Round: this report, ARCH-REV-001.
- Workspace aliases: **N** = `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`; **S** = `/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs`; **D0** = `/Users/normy/autobyteus_org/autobyteus-nfs`. Both task branches are `codex/extract-autobyteus-nfs`.
- Current-State Evidence Basis: independent local reads at S commit **`3712cd9bf0db998501d162db7f8655f169e3def6`**. N and S were clean before reviewer edits. D0 remains unborn main with untracked `task-plans/`; its shared Git database contains N's task commit. No remote freshness claim is made by this review; Delivery must refresh both remotes.

Evidence used below (source paths relative to S):

| Key | Independent inspection | Architectural relevance |
| --- | --- | --- |
| V1 | All five current package documents; source root AGENTS/DESIGN/TESTING/RELEASE, server/web AGENTS; architecture-reviewer skill, shared principles and full report/revision templates | Approval, scope, separation of authorities, applicable finalization/testing policies |
| V2 | `autobyteus-nfs/go.mod`, `cmd/autobyteus-nfs/main.go`; `internal/platform/directory_modes_test.go`; three service Python suites and mixed `scripts/tests/test_nfs_packaging_and_launcher.py` | Actual module/root dependencies and ownership split, including Go-to-Python fixture |
| V3 | Full `autobyteus-nfs/packaging/release.py`, `release-lock.json`, Dockerfile and full `.github/workflows/release-nfs.yml`; engine `source.py` / `build.py`; workflow gate tests | Source identity, candidate reuse, packaging paths, refusal/signing gates and parent-independent recipe |
| V4 | `internal/cli/launcher.go:12–45`; `internal/config/{state.go,store.go,connection.go,config_test.go}`; `testdata/attachment.json`; installed app import in `internal/docker/exec.go` | Producer, persisted identities/paths and intentional deployed app integration |
| V5 | `scripts/public/docker/autobyteus-docker.d/bash/nfs-attachment.sh:3–35`; `autobyteus-server-ts/src/workspaces/shared-workspace-binding.ts:14–78`; full binding unit test | Seven-line consumer checks, actual descriptor parser/admission, sibling fixture dependency |
| V6 | `scripts/public/nfs/install.sh:5–45`; NFS LICENSE/THIRD_PARTY_NOTICES; root LICENSING/NOTICE/CONTRIBUTING/CLA; tracked active-reference search excluding historical tickets and `.codex` | Installer repository ownership, inherited terms, license equality, removal coverage |
| V7 | Read-only Git HEAD/status/ref observations for N/S/D0; historical DR-002 summary explicitly indexed by investigation | Safe initial-history and two-repository sequencing; bounded old evidence, not new qualification |

Review consisted of document/code/reference inspection and read-only Git checks, not executable validation. No build, runtime test, VM/container, installed CLI, live mount, release/tag, network publication or cleanup action was performed. Source and historical artifacts were not modified.

## Routing Classification Review

- Task size: **Large**. Independent development, distribution, consumer test ownership, removal and two-repository finalization are distinct coordinated workstreams, not simply a large file move.
- Architectural risk: **High**. Build attestation and privileged-service distribution ownership change while public interfaces must remain intact.
- Classification rationale reviewed: design §§Task Size And Architectural Risk / Change Scope, corroborated by V2–V6.
- Independent Architecture Review required: **Yes**.
- Classification correction required: **None**.

## Upstream Behavior And Production-Path Basis Confirmation

- Overall Basis Status: **Confirmed**.
- Approved intent: R1/SR-001 authorizes one independent maintained NFS home, intact installed integration, preserved licensing/qualification and safe finalization; approval is recorded as Solution Designer within explicit user direction, user informed.
- Scope guardrail: UC-001–004 in scope. Live deployment/upgrade, new runtime policy/schema, new platform qualification, old UI/VM/editor campaigns and unrelated cleanup are excluded. Review does not reopen those business decisions.
- Relevant existing behavior: module/build/fixture dependencies actually cross repository boundaries; production consumers already use installed interfaces (V2–V6).
- Every prospective blocking Design Impact finding traceable to approved authority: **Yes — no blockers raised**.
- Remaining material ambiguity: **None for this design decision**. Pending execution is not missing approved intent.

| Behavior ID | Kind | Design Alignment With Approved Intent | Approved Trigger / Contract And Current-State Evidence | Target Outcome / Path / Spine Coherence | Status | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| BEH-001 | Operational | Pass | Pass — SCN-001 contributor clone/build action; Go module, mixed repository roots and fixture invocation in V2 | Pass — DS-001 root module and moved local tests; independent archive check makes independence observable | Confirmed | Execute AC-001/002 downstream |
| BEH-002 | Contract | Pass | Pass — SCN-002 maintainer candidate command / separately authorized future publication; actual release tool, job graph and installer in V3/V6 | Pass — DS-002/003 local owned source hash, explicit consumer evidence, empty qualification, manual-only publish input and preserved gates | Confirmed | Execute packaging/refusal checks; no publication now |
| BEH-003 | System | Pass | Pass — SCN-003 selected-node setup/recreation/new-run admission; CLI → seven-line shell checks and descriptor → mount/marker parser in V4/V5 | Pass — DS-004 unchanged installed production boundary; DS-005 pinned test data replaces sibling source access | Confirmed | Prove normalized-source preservation and producer/consumer equality |
| BEH-004 | Operational | Pass | Pass — SCN-004 requested repository move and preservation contract; distinct source target, unborn destination and PM data in V7 | Pass — DS-006 validates paired candidates, establishes N main, pins S, integrates personal, reports partial success without force | Confirmed | Refresh/integrate/record both targets at Delivery |

## Supplemental Artifact Coherence Verdict

No new behavior-defining supplements. Investigation is the canonical inventory; old proof is historical context only.

| Artifact | Purpose And Scope Clear? | Linked To Core? | Internally Complete? | Consistent? | Status / Approval Applicability Clear? | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| Current solution-design-handoff.md | Pass | Pass | Pass | Pass | Pass | None; identifies both worktrees and next review stage |
| Historical DR-002 summary / archive references | Pass | Pass | Pass for provenance use | Pass | Pass | Keep read-only; do not import old acceptance gates or treat historical test results as extraction proof |
| E11 retained engine candidate reference | Pass | Pass | Pass as input location, not validity proof | Pass | Pass | Copy only into owned scratch and freshly verify when used; no historical source-hash promotion |

## Task Design Health Assessment Verdict

| Assessment Area | Result | Evidence | Required Action |
| --- | --- | --- | --- |
| Current task posture present | Pass | Design identifies Refactor, not runtime defect repair | None |
| Root cause explicit and evidence-backed | Pass | Boundary/ownership and file placement: app-inclusive source hash, desktop version assertion, mixed tests and TS sibling fixture (V2/V3/V5) | None |
| Refactor decision explicit | Pass | Refactor now for repository coupling; retain healthy service internals | None |
| Decision reflected concretely | Pass | Named file moves/split, local hash inputs, fixture provenance, removal and ordered finalization | None |

## Spine Inventory Verdict

| Spine ID | Scope | Readable? | Narrative Clear? | Facade Vs Governing Owner Clear? | Domain Subject Naming Clear? | Ownership Clear? | Off-Spine Concerns Separate? | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS-001 | Contributor independent build/check | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS-002 | Manual candidate identity/build/archive | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS-003 | Future gated publication/verified installation, not executed now | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS-004 | Preserved setup/attachment/app admission | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS-005 | Producer fixture → pinned consumer → integration verdict | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS-006 | Paired integration/finalization/receipt | Pass | Pass | Pass | Pass | Pass | Pass | Pass |

The release workflow orchestrates six bounded jobs; release.py governs identity/refusal, not application versioning. Installer transfer does not own setup consent. Existing supervisor/recovery loops and CLI errors are retained, not turned into new asynchronous spines.

## Boundary Encapsulation Verdict

| Boundary / Owner | Public Entry Clear? | Owned Mechanisms Internal? | Bypass Controlled? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| NFS CLI/setup/config/backend/docker | Pass | Pass | Pass | Pass | Installed CLI and public descriptor remain the app boundary; private stores are not consumer APIs |
| Packaging/workflow/installer | Pass | Pass | Pass | Pass | Manual workflow delegates source/engine qualification; installer verifies archive/embedded metadata before existing CLI consent |
| App launcher and TS admission | Pass | Pass | Pass | Pass | Seven lines, daemon/volume identity and observed mount/marker checks preserved (V4/V5) |
| Fixture provenance | Pass | Pass | Pass | Pass | Consumer owns local data/pin, not Go implementation; integration verifies real producer commit |

## Dependency Direction / Forbidden Shortcut Verdict

| Boundary | Allowed Dependencies Clear? | Forbidden Shortcuts Explicit? | Direction Coherent? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| N developer/distribution | Pass | Pass | Pass | Pass | Local declared inputs/toolchains; no app checkout, pnpm, package.json or sibling Go replace |
| S ordinary tests | Pass | Pass | Pass | Pass | Local pinned snapshot; no mutable-main fetch or required neighboring checkout |
| Optional deployed app integration | Pass | Pass | Pass | Pass | Installed `/app/.../shared-workspace-binding.js`, supervisor and selected-node checks intentionally remain; independence is not removal of the integration contract |
| Source ownership removal | Pass | Pass | Pass | Pass | No second implementation, embedded symlink, forwarding installer or submodule |

## Interface Boundary Verdict

| Interface | Subject Clear? | Singular Responsibility? | Identity Shape Explicit? | Generic Boundary Risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| launcher-attachment --nodes / seven-line output | Pass | Pass | Pass — selected node, storage UUID, daemon ID, volume and options retain their distinct roles | Low | Pass |
| Public five-field descriptor / TS parser | Pass | Pass | Pass — endpoint/export/protocol/mountRoot/storageId unchanged | Low | Pass |
| source_hash / release qualification | Pass | Pass | Pass — local source + declared contract + exact engine; consumer revision separately identified | Low | Pass |
| Consumer provenance repository/commit/path/sha256 | Pass | Pass | Pass — real committed producer, not mutable branch or placeholder | Low | Pass |

## Existing Capability / Subsystem Reuse Verdict

| Need | Existing Capability Checked? | Reuse Decision Sound? | New Support Justified? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Runtime service and app integration | Pass | Pass | N/A | Pass | Move existing owners; no new coordinator/parser/schema library |
| Release identity/engine verification | Pass | Pass | N/A | Pass | Rebase established release.py and manifest logic; preserve byte-sensitive recipe |
| Independent checks | Pass | Pass | Pass | Pass | Split mixed tests and add local CI/policies, not a new generic test framework |
| Cross-repo contract evidence | Pass | Pass | Pass | Pass | Tiny pinned fixture and producer equality reuse real Go/TS parsers |

## Subsystem / Capability-Area Allocation Verdict

| Area | Allocation Clear? | Reuse / Extend / New Sound? | Supports Spine Owner? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| cmd/cli/setup/config/platform/backend/docker/service | Pass | Pass | Pass | Pass | Existing runtime allocation retained |
| packaging + service installer/tests + release workflow | Pass | Pass | Pass | Pass | One NFS-owned distribution chain |
| S launcher/admission tests/docs | Pass | Pass | Pass | Pass | Consumer-side responsibility remains in S |
| Delivery | Pass | Pass | Pass | Pass | Explicit two-repo sequencing; no atomicity claim |

## Reusable Owned Structures Verdict

| Repeated Structure | Extraction Need Evaluated? | Shared File Choice Sound? | Shared Ownership Clear? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Engine source/manifest recipe | Pass | Pass | Pass | Pass | Move one existing implementation, avoid copying it into app |
| Descriptor fixture | Pass | Pass | Pass | Pass | Producer fixture plus explicitly pinned consumer data; not two independently maintained schemas |
| Mixed packaging/launcher test file | Pass | Pass | Pass | Pass | Split by service vs app responsibility, no cross-repo helper import |

## Shared Structure / Data Model Tightness Verdict

| Structure | One Meaning Per Field? | Redundancy Controlled? | Overlapping Representations Controlled? | Core Vs Variant Sound? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Connection / NodeAttachment / TS binding | Pass | Pass | Pass | Pass | Pass | Preserved specialized consumers; no universal DTO or extra persisted fields |
| Qualification lock and evidence | Pass | Pass | Pass | Pass | Pass | Source hash no longer claims app bytes; separate explicit consumer commit/image evidence, all qualification fields remain empty |
| Consumer provenance | Pass | Pass | Pass | Pass | Pass | Digest proves snapshot bytes, pinned commit/path supplies producer provenance; neither substitutes for parser/equality checks |

## File Responsibility Mapping Verdict

| File / group | Responsibility Clear? | Correct Owner? | Re-Tightened After Split? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| N go.mod / cmd / internal | Pass | Pass | N/A | Pass | Only module/import relocation; preserve runtime semantics |
| N packaging/release.py / Dockerfile / workflow | Pass | Pass | Pass | Pass | Local roots/source inputs and independent version owner; detailed mapping covers archive/signing/COPYRIGHT paths |
| N test_nfs_packaging.py / S test_nfs_launcher.py | Pass | Pass | Pass | Pass | Service refusal vs installed consumer controls separated |
| N directory_modes_test.go | Pass | Pass | N/A | Pass | `../..` reaches new root; preserve actual Go/Python fixture and honest prerequisites/skips |
| S binding test / fixture provenance | Pass | Pass | Pass | Pass | Offline local snapshot + actual parser, explicit paired producer check |
| N policies/licensing/EXTRACTION/integration-contract; S active docs | Pass | Pass | Pass | Pass | Clear authority rather than duplicated release ownership or imported unrelated policies |

## Subsystem / Folder / File Placement Verdict

| Path / Item | Placement Clear? | Owning Boundary Matches? | Mixed-Layer / Over-Split Risk | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| N root Go module / internal folders | Pass | Pass | Low | Pass | Existing compact concern layout retained |
| N scripts/tests and scripts/public/nfs | Pass | Pass | Low | Pass | Local service tooling; stable relative layout minimizes fixture churn |
| S tests/fixtures/shared-network-workspaces | Pass | Pass | Low | Pass | Consumer-owned test data, not production service source |
| N RELEASE vs packaging/RELEASE | Pass | Pass | Low | Pass | Root finalization authority links detailed distribution contract, no conflicting owners |

## Removal / Decommission Completeness Verdict

| Item | Obsolete Piece Named? | Replacement Clear? | Scope Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| S tracked autobyteus-nfs tree | Pass | Pass | Pass | Pass | N becomes maintained source; ignored outputs are not blindly copied/deleted |
| S service workflow/installer/Python suites | Pass | Pass | Pass | Pass | Move service ownership, retain launcher cases under new test name |
| S sibling fixture and same-repo distribution claims | Pass | Pass | Pass | Pass | Pinned fixture and external owner links |
| Old workflow tag trigger / desktop version assertion / app source hash inputs | Pass | Pass | Pass | Pass | Manual explicit input, NFS version ownership and separate consumer evidence replace repository coupling, not safety checks |

V6's active tracked references match the named owner/removal set. No newly dead runtime branch was identified in the inspected relocation boundary; this is not a whole-code dead-code audit. Historical ticket paths and actual installed-path references are intentionally retained, not obsolete code. Implementation must verify the final active-reference inventory rather than mechanically delete every `autobyteus-nfs` string.

## Legacy / Backward-Compatibility Verdict

| Area | Wrapper / Dual-Path / Legacy Retention? | Clean Cut Explicit? | Verdict | Notes |
| --- | --- | --- | --- | --- |
| Repository extraction | No | Pass | Pass | No symlink, forwarding installer, submodule, replace or dual source home |
| Installed CLI/state/descriptor/app paths | No new compatibility path | Pass | Pass | These are current public contracts, not legacy shims |
| Historical provenance | No runtime legacy | Pass | Pass | Immutable references do not keep an obsolete runtime implementation active |

## Persisted-Data Transition Verdict (When Applicable)

| Stored Subject | Approved Decision | Reader / Semantic / Invariant Evidence Sufficient? | Choice Proportionate? | Migration Safety If Required | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Private hosted/attachment state, public descriptor, source marker and node references | Not Affected | Pass — config state/store/paths and both installed readers in V4/V5; design changes no fields or deployed paths | Pass | N/A | Pass | Go import identity and release build root are not persisted addresses; no migration/reset/live enumeration warranted |
| PM task-plans / old evidence / unrelated owner data | Preserve unchanged | Pass — scope, D0 observation and V7 | Pass | N/A | Pass | Non-force checkout only after recheck; no broad clean/prune |

## Change / Refactor Safety Verdict

| Area | Sequence Realistic? | Temporary Seams Explicit? | Cleanup / Removal Explicit? | Verdict |
| --- | --- | --- | --- | --- |
| Tracked extraction and mechanical namespace/path edits | Pass | Pass — compare normalized runtime source, not blanket semantic rewriting | Pass | Pass |
| Standalone and paired consumer verification | Pass | Pass — temporary producer checkout only for explicit equality, not ordinary test dependency | Pass | Pass |
| N main then S pinned integration/personal | Pass | Pass — partial finalization is reported, no false transaction/force rollback | Pass | Pass |
| Canonical D0 population and task cleanup | Pass | Pass — recheck unborn state/owner conflicts; preserve PM data | Pass | Pass |

No claim that local ref observations guarantee future remote state. Design requires refresh and safe reconciliation at each actual finalization boundary.

## Example Adequacy Verdict

| Topic | Example Needed? | Present And Clear? | Avoided Shape Explained? | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Standalone roots/hash and fixture paths | Yes | Pass | Pass | Pass | Concrete ROOT/SOURCES list, Go fixture root and provenance fields are actionable |
| Workflow and version ownership | Yes | Pass | Pass | Pass | Manual-only inputs, default false and preserved six-job gates; no auto tag/release |
| Runtime migration/recovery | No | N/A | Pass | Pass | No runtime change; inventing a new migration/recovery example would widen scope |
| Two-repo initial finalization | Yes | Pass | Pass | Pass | Ordered N/S/D0 steps and partial-failure handling named |

## Material Premise Validation (Only When Needed)

**None.** No finding or new mechanism depends on a material scenario outside the established BEH-001–004 basis. Candidate refusal and concurrent-owner preservation already have independent SCN-002/004 governing contracts and forward paths. No hypothetical runtime failure is used to demand new validation, migration or recovery machinery.

## Unresolved Approved-Behavior Or Current-State Gaps

**None for architecture readiness.** Independent builds, executable packaging controls, consumer equality and final remote receipts are required downstream evidence, not results claimed by this review.

## Review Decision

**Pass — ARCH-REV-001, R1/SR-001 and SR-002.** Approved behavior is confirmed; ownership, spines, dependency removal, qualification boundary and no-data-transition decision are coherent and actionable. Ready for implementation of the approved extraction. This is not source-review acceptance, test Pass, platform qualification, Delivery Completed or authorization to publish/deploy.

## Findings

**None.** No Design Impact or Requirement Gap requiring upstream revision was established. No unrelated follow-up is created.

## Classification

**Pass; failure classification N/A.** Preserve **Large / High / independently reviewed**.

## Recommended Recipient

Fresh handoff rules select **`/software_engineering_team/implementation_engineer`**: architecture review passes and the cumulative package is ready for implementation. Fail/Blocked does not apply; the informational-after-primary condition is not the current work handoff. Send the single primary recipient this paired-repository extraction result and both authoritative review artifacts plus current requirements/design/investigation/history/workspace context. No duplicate dispatch, bulk historical manifest or old campaign restart.

## Residual Risks

1. **Mechanical drift:** ROOT/import/workflow/archive paths can break despite sound design. Fresh independent archive checks, normalized runtime comparison and moved negative controls remain required, not yet executed.
2. **Qualification meaning:** N's source hash attests owned inputs plus declared integration contract, not arbitrary app revisions. Future publication must retain explicit service/engine/consumer commit or image evidence, current-source/physical/user/candidate/signing gates. Existing evidence-path checks alone are not semantic validation of those receipts; extraction starts unqualified and does not claim otherwise. No new receipt schema is imposed here.
3. **Consumer drift:** pinned fixture equality and actual parser/launcher tests protect this paired candidate; they do not promise all future service/app combinations. Pin changes need explicit review/checks as designed.
4. **Artifact/platform limits:** retained arm64 engine bytes must be freshly verified in owned scratch. Synthetic fixtures, cross-compilation and old bounded runtime proof are not native amd64/Mac/physical/hosted-Actions/signing qualification. Availability is downstream execution evidence, not inferred from this report.
5. **Two-repo completion is non-atomic:** refreshed refs and actual producer identity are required. A successful N push followed by a blocked S integration is partial completion, not permission to force rollback or erase another owner's work. Preserve D0 task-plans and old retained assets.
6. **Licensing/provenance transcription:** exact LICENSE/CLA/additional permission and recipe attribution must survive implementation. This review confirms the preservation design against repository texts, not new legal advice or relicensing authority.

## Latest Authoritative Result

- Review Decision: **Pass**.
- Material-Premise Gate: **Pass**.
- Current review: **ARCH-REV-001**, first baseline; prior decision **N/A**.
- Applicable solution: **R1 / SR-001 approved; SR-002 design**.
- Notes: design review only; no execution/finalization/publication claim. Required implementation, independent source review, executable validation and Delivery remain with their owners under fresh routes.
