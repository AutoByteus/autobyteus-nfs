# Design Review Report — nfs-first-release

## Review Round Meta

- Task: `autobyteus-nfs-3` / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`.
- Date / reviewer: 2026-10-18 / architecture reviewer, personal execution.
- Workspace: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`; branch `codex/nfs-first-release`.
- Upstream Requirements Doc: `requirements-doc.md`, R2 / SR-002 Approved.
- Upstream Investigation Notes: `investigation-notes.md`, E01–18 and administrative resume inventory.
- Upstream Solution Revision Record: `solution-revision-record.md`, SR-001–003.
- Reviewed Design Spec: `design-spec.md`, SR-003; handoff `solution-design-handoff.md`.
- Supplemental Task Artifacts Reviewed: intake repository preflight; signing metadata, export-progress and final upload receipts; design-artifact audit; poweroff-resume receipt. Earlier credential states are historical, not outstanding requests.
- Relevant Solution Revision IDs: SR-002 approved basis; SR-003 completed design. Poweroff resume does not change either.
- Architecture Review Revision Record: `architecture-review-revision-record.md`.
- Current Architecture Review Revision ID: **ARCH-REV-001**.
- Current Review Round: **1**, resumed original review, not a second review round.
- Trigger: original Architecture Design Complete handoff, followed by explicit user-requested continuation after poweroff.
- Prior Review Round Reviewed: **N/A** for this task. Conversation checkpoint records no completed result/forwarding; no canonical report/history or corresponding Git history existed at resume. No prior Pass inferred. Closed extraction reviews are not release authority.
- Latest Authoritative Round: this report / ARCH-REV-001.
- Reviewed HEAD: `1a095f75396916a98d0b60c5517d14272890861a`; design checkpoint `cbf7b35edc3fae86d90800003a1720528666d67e`; source base `7e375984be2bea7a4d536e43cc59d6bc2b116870`. Requirements/design unchanged between checkpoints; source delta from base is task documentation only.
- Current-State Evidence Basis: read root AGENTS/DESIGN/TESTING/RELEASE, packaging/RELEASE, complete release workflow/release.py/engine manifest validator/Dockerfile/installer/VerifyRelease, developer CI and release fixtures; focused runtime Release, host admission and Docker EnsureEngine paths. Shared design principles, Example 9 and handoff guidance applied. Nine intake source-file hashes independently matched. No source audit of unrelated runtime, tests/builds, credential access, CI dispatch, live resources or publication performed.

Independent primary-contract checks (2026-10-18): explicit tag verification/draft operations are supported by [GitHub CLI](https://cli.github.com/manual/gh_release_create); artifact identity/digest/expiry and attempt metadata are available through [artifact](https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28) and [workflow-run](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28) APIs. Complete multi-arch copy with digest-preservation refusal is supported by [skopeo](https://github.com/podman-container-tools/skopeo/blob/main/docs/skopeo-copy.1.md). Public image access is distinct from repository visibility in [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry). Apple's [notarization guidance](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow) was checked using its official Markdown representation after the HTML returned a JS shell: standalone binary tickets cannot be stapled. These support the design, not an execution success claim.

## Routing Classification Review

- Task size: **Large**. Architectural risk: **High**. Independent review: **Yes**.
- Rationale confirmed: release-control decomposition, cross-run candidate identity, qualification records, secret-bearing signing and irreversible Git/Release/registry transitions. This is structural distribution work, not merely many documents or unchanged runtime code.
- No classification correction required. No source push or release action belongs to this review stage.

## Upstream Behavior And Production-Path Basis Confirmation

**Overall: Confirmed.** R2 authorizes an actual first normal `v0.1.0` release, never beta, with all four existing target tuples and current physical/user/signing gates. Publication authorization does not constitute qualification. UC001–005, out-of-scope boundaries and review authority are explicit. Proposed changes stay in release tooling/workflow/docs; app independence, engine/runtime behavior, installed data and live-user storage are preserved. Every prospective blocking Design Impact must cite R2; no such finding remains. No material intent ambiguity.

| Behavior ID | Kind | Intent alignment | Approved trigger / current-state evidence | Target path coherence | Status | Required action |
| --- | --- | --- | --- | --- | --- | --- |
| BEH001 | Operational | Pass | Pass — maintainer candidate dispatch; current workflow lines 24–167 requires tag checkout and builds engine/artifacts | Pass — DS1 resolves exact source, builds measured candidate without write privileges or qualification | Confirmed | Implement D1–2; prove hosted no-effects outcome |
| BEH002 | Contract | Pass | Pass — REQ003/004/006 qualification contract; release.py lines 62–76 currently checks empty lock, source, user and evidence paths | Pass — DS2 binds semantic target/mode receipts to exact engine/OCI/candidate; real signing distinct | Confirmed | Execute actual gates downstream; no inferred Pass |
| BEH003 | Operational | Pass | Pass — authorized publish/retry, SCN003/006; current image push precedes binary signing and upload uses clobber | Pass — DS3/5 final payload precedes public effects, exact annotated tag and draft reconcile retained bytes | Confirmed | Implement staged publisher and failure/resume controls |
| BEH004 | User | Pass | Pass — versioned installer → archive → VerifyRelease → user install; no-argument final invocation enters setup | Pass — DS4 retains admission, adds complete checksums/bounds and explicit owned-HOME version smoke | Confirmed | Validate actual downloads, not just fixture success |
| BEH005 | Contract | Pass | Pass — CheckHost, setup.Release/Plan and EnsureEngine preserve supported host and consent paths | Pass — DS2/4 use test-owned hosts; metadata-only qualification registry alias retains image digest, no runtime override | Confirmed | Preserve Go/runtime and host-state boundaries |
| BEH006 | Operational | Pass | Pass — Delivery finalizes source and documents release under REQ009/010; current policies still describe extraction | Pass — DS3 receipt and named policy replacement retain provenance and fresh-main nonforce finalization | Confirmed | Replace obsolete prose during implementation/delivery |

## Supplemental Artifact Coherence Verdict

| Artifact | Purpose/scope | Core links | Complete for purpose | Consistent | Status/approval clear | Required action |
| --- | --- | --- | --- | --- | --- | --- |
| repository-release-preflight.json | Pass | Pass | Pass | Pass | Pass | Historical empty remote/credential inventory, not current signing state |
| signing metadata/export-progress/final upload receipts | Pass | Pass | Pass | Pass | Pass | Six entries provisioned; actual import/notary remains unvalidated. No repeat credential request absent a real validation failure |
| design-artifact-audit.json | Pass | Pass | Pass | Pass | Pass | Administrative consistency only, not tests |
| poweroff-resume.json and handoff resume section | Pass | Pass | Pass | Pass | Pass | Continue this original round; no new approval or duplicated dispatch |

No behavior-defining supplement or UI ambiguity. Earlier placeholder records remain chronological evidence, explicitly superseded by E18; do not treat their former prerequisites as current blockers.

## Task Design Health Assessment Verdict

| Assessment area | Result | Evidence | Required action |
| --- | --- | --- | --- |
| Current posture stated | Pass | Larger release requirement, not filesystem redesign | None |
| Root cause evidence-backed | Pass | Workflow engine job pushes before signing; path-count gate and clobber remain in current source | None |
| Refactor decision explicit | Pass | Bounded packaging/workflow refactor now | Implement designated owners |
| Concrete design follows decision | Pass | D1–6, removal/file maps separate identity, candidate, qualification and publication | None |

## Spine Inventory Verdict

All five inventories expose meaningful entry, ownership and end state; the CLI facade is not mistaken for the governing owner. No application callback/event spine is introduced.

| Spine | Scope | Readable | Narrative | Facade/owner | Subject naming | Ownership | Off-spine separation | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1 | Primary candidate dispatch → checkout/build → verify/aggregate → retained artifact | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS2 | Primary candidate → owned-host execution → receipts/user check → reviewed lock/readiness | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS3 | Primary authorized dispatch → qualification/final signing → payload → tag/draft/OCI → downloads/receipt | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS4 | Primary versioned user download → integrity/admission → installed CLI/version | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| DS5 | Local under DS3: observe partial remote state → resolve retained identity → fill missing exact outputs/refuse | Pass | Pass | Pass | Pass | Pass | Pass | Pass |

## Boundary Encapsulation Verdict

| Boundary / owner | Public entry clear | Internals internal | Bypass controlled | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| release.py / release_support | Pass | Pass | Pass | Pass | Workflow schedules; facade dispatches to authoritative candidate/qualification/publication owners |
| Engine manifest validator | Pass | Pass | Pass | Pass | Existing measured-pair validation/embedding reused, not a second package decoder |
| Mac signing | Pass | Pass | Pass | Pass | Narrow script receives secrets only in intended Mac publication jobs; no publishing authority |
| Runtime installer / VerifyRelease | Pass | Pass | Pass | Pass | Existing exact metadata/target admission; runtime does not consult release-control evidence |

## Dependency Direction / Forbidden Shortcut Verdict

| Owner / boundary | Allowed direction clear | Forbidden shortcuts explicit | Coherent | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Workflow → release facade → subject modules | Pass | Pass | Pass | Pass | No duplicated shell gate policy or early image push |
| Publication → verified candidate/qualification → bounded remote effects | Pass | Pass | Pass | Pass | No run-ID-only trust, clobber, force tag or rebuilt qualified image |
| Installer → runtime admission | Pass | Pass | Pass | Pass | No source-build prerequisite, unsigned fallback or restored app coupling |

## Interface Boundary Verdict

| Interface | Subject clear | Singular responsibility | Explicit identity | Generic risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| Candidate assemble/verify | Pass | Pass | Pass — repo/workflow/run/attempt/source/version/artifact/engine/OCI | Low | Pass |
| Source-hash / metadata | Pass | Pass | Pass — production inputs plus exact engine; runtime Release separate | Low | Pass |
| Check-publish | Pass | Pass | Pass — candidate + current lock + referenced qualification | Low | Pass |
| Publication plan/resume | Pass | Pass | Pass — source/version + final payload and remote observations | Low | Pass |
| Installer / VerifyRelease | Pass | Pass | Pass — versioned manifest equals embedded metadata/current target | Low | Pass |

## Existing Capability / Subsystem Reuse Verdict

| Concern | Existing checked | Reuse/extension sound | New piece justified | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Engine identity/source/inventory | Pass | Pass | N/A | Pass | manifest.py validate/verify/embed and existing recipe remain owners |
| Release admission and metadata | Pass | Pass | Pass | Pass | Refactor current release.py, retain command spellings and runtime Release shape |
| Native signing | Pass | Pass | Pass | Pass | Extract current inline responsibility, tighten credential isolation/Accepted status |
| Installer/host lifecycle | Pass | Pass | N/A | Pass | Preserve installer/Go boundary, no new runtime service |

## Subsystem / Capability-Area Allocation Verdict

| Capability | Allocation clear | Reuse/extend/create sound | Correct spine owner | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Actions scheduling | Pass | Pass | Pass | Pass | Runner matrix, permissions and explicit job-result gates |
| Release control | Pass | Pass | Pass | Pass | Cohesive packaging subject owners; identity parsing shared narrowly |
| Engine and signing | Pass | Pass | Pass | Pass | Independent existing engine provenance and bounded Mac secret operation |
| API/Delivery | Pass | Pass | Pass | Pass | Real execution/evidence judgement remains human-owned, not manufactured by JSON validation |

## Reusable Owned Structures Verdict

| Repeated logic | Extraction evaluated | Shared file sound | Owner clear | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Version/hash/path identity | Pass | Pass | Pass | Pass | release_support/identity.py; cover newly extracted executable files in source digest |
| Engine pair validation | Pass | Pass | Pass | Pass | Reuse engine/manifest.py rather than copy checks |
| Qualification/publication records | Pass | Pass | Pass | Pass | Compose verified identity, not independently trusted copies or generic context bag |

## Shared Structure / Data Model Tightness Verdict

| Structure | One meaning per field | Redundancy controlled | Overlap controlled | Composition sound | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| CandidateIdentity + Actions envelope | Pass | Pass | Pass | Pass | Pass | Artifact ID/wrapper digest assigned after upload; no self-hash cycle |
| Qualification | Pass | Pass | Pass | Pass | Pass | Target/mode rows and hashed receipts reference exact candidate; lock assertions checked consistently |
| PublicationIdentity | Pass | Pass | Pass | Pass | Pass | Final signed payload differs from candidate; original run/attempt retained for resume |
| Runtime Release | Pass | Pass | Pass | Pass | Pass | Version/source/engine/image/targets retained; no CI/evidence fields leak into runtime |

## File Responsibility Mapping Verdict

| File | Singular responsibility | Matches owner | Re-tightened after extraction | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| release-nfs.yml / ci.yml | Pass | Pass | Pass | Pass | Schedule and carry artifacts; ordinary CI cannot publish |
| release.py / release_support/__init__.py | Pass | Pass | Pass | Pass | Command facade/package boundary, no import effects |
| identity.py / candidate.py | Pass | Pass | Pass | Pass | Distinct value parsing and compound artifact verification |
| qualification.py / publication.py | Pass | Pass | Pass | Pass | Evidence applicability versus external stage reconciliation |
| sign-macos.sh | Pass | Pass | Pass | Pass | Ephemeral credential/keychain/sign/notary lifetime |
| install.sh / release-lock.json / tests / docs | Pass | Pass | Pass | Pass | Bounded user install, reviewed record, durable controls and truthful guidance |

## Subsystem / Folder / File Placement Verdict

| Path | Placement clear | Owning boundary | Mixed/over-split risk | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| .github/workflows | Pass | Pass | Low | Pass | Transport/scheduling, not release policy |
| packaging/release_support | Pass | Pass | Low | Pass | Four cohesive subjects; no per-field framework or extra service layer |
| packaging/engine; packaging/sign-macos.sh | Pass | Pass | Low | Pass | Distinct build identity and platform-specific secret operation |
| scripts/public; scripts/tests; ticket evidence | Pass | Pass | Low | Pass | User entry, durable checks, and task execution records remain distinct |
| internal / cmd | Pass | Pass | Low | Pass | Runtime unchanged; generated release metadata only |

## Removal / Decommission Completeness Verdict

| Item | Removal named | Replacement clear | Scope explicit | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| Tag/precreated-release prerequisite | Pass | Pass | Pass | Pass | Existing workflow checkout/view replaced by explicit source and controlled creation |
| Rebuild/early image push and clobber upload | Pass | Pass | Pass | Pass | Exact candidate promotion and missing-only reconciliation |
| Beta/parser/subset and path-count-only sufficiency | Pass | Pass | Pass | Pass | R2 normal-only exact target set, semantic evidence validator |
| Old no-create fixtures and extraction policy | Pass | Pass | Pass | Pass | Replace with current candidate-no-effects/publish-gate tests and independent-release docs |

These are reachable old behaviors explicitly superseded by R2, not falsely described as dead code. Their callers/tests are mapped. No additional dead piece discovered in the inspected changed surfaces requiring another removal prescription; implementation must remove obsolete imports/branches when replacing this path.

## Legacy / Backward-Compatibility Verdict

| Area | Dual path / wrapper retained | Clean cut explicit | Verdict | Notes |
| --- | --- | --- | --- | --- |
| Release behavior | No | Pass | Pass | No old publisher, beta fallback or path-count qualification fallback |
| Tool command spelling | No | Pass | Pass | Existing facade commands continue through one implementation, not parallel legacy logic |
| Host state | No new path | Pass | Pass | Existing host-only reader/refusal behavior unchanged; no migration adapter |

## Persisted-Data Transition Verdict (When Applicable)

| Stored subject | Decision | Evidence sufficient | Proportionate | Migration safety | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Installed host state | Not Affected | Pass | Pass | N/A | Pass | Runtime readers/writers/schema not changed; no deployment |
| Empty qualification lock | Discard or Rebuild qualification fields | Pass | Pass | N/A | Pass | Current lock has no engine/evidence/qualified target; populate only from actual new proof |
| Candidate outputs | Rebuild only as new candidate | Pass | Pass | N/A | Pass | Artifact expiry cannot preserve an old qualification claim |
| Tags/releases/assets/OCI | Directly Usable — No Migration | Pass | Pass | N/A | Pass | Empty initial inventory; observe/reconcile new objects without overwriting history |
| Repository secrets | Directly Usable — No Migration | Pass | Pass | N/A | Pass | Provisioning complete per E18/resume; ordinary intended validation only |

No data migration machinery is justified. Historical evidence/failed attempts remain intact; disposable owned output is not interchangeable with a retained qualified artifact.

## Change / Refactor Safety Verdict

| Area | Sequence realistic | Temporary seam explicit | Cleanup explicit | Verdict |
| --- | --- | --- | --- | --- |
| Identity/candidate/qualification first | Pass | Pass | Pass | Pass |
| Final payload/signing before public effects | Pass | Pass | Pass | Pass |
| Candidate qualification-registry alias → canonical digest | Pass | Pass | Pass | Pass |
| Single-repo main integration → authorized release → receipt | Pass | Pass | Pass | Pass |

D3 discloses registry alias/qualified-target/signature differences and requires final native/metadata/download checks; it does not falsely claim binary equality. Same production hash, exact engine/OCI, ancestry and reviewed intervening diff allow only the specified qualification/docs/test changes. Any changed production input invalidates affected evidence. Staged source finalization can enable hosted workflow testing; it is not Task completion. Retry resolves prior retained payload before any rebuild and rejects conflict/expiry.

## Example Adequacy Verdict

| Topic | Needed | Clear example | Avoided shape | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| OCI preservation | Yes | Pass | Pass | Pass | Digest A stays A; same packages rebuilt into B are not A |
| User verification | Yes | Pass | Pass | Pass | Actual scoped user check, not permission to release |
| Retry | Yes | Pass | Pass | Pass | Exact existing asset reused; different bytes conflict, never clobber |

## Material Premise Validation (Only When Needed)

No additional speculative scenario is required. Two consequential mechanism premises were independently checked below; both are already supported by R2, not new recovery/security policy. Example 9 was applied.

### MP001 — Publication can leave a version tag before a release is complete

- Authority: REQ006 / AC004, SCN006, BEH003; **Supported Explicit Edge Scenario**.
- Initiating basis: **Operational** — maintainer resumes an interrupted/failed authorized release, explicitly supported by UC003, independently of the proposed receipt mechanism.
- Forward approved path: authorized publish dispatch → verified qualification and successful final signed payload → nonforce tag creation → separate draft/assets/registry/publication operations. An interruption after acknowledged tag creation leaves the tag but not a complete public release. GitHub tag and Release operations are separate; the CLI contract does not provide a transaction across them.
- Preconditions/consequence: same version/source already has a public ref; rebuilding/re-signing changes payload bytes and loses unambiguous recovery identity. Neither a failed run nor tag existence establishes completed publication.
- Reachability: **Reachable** under the explicit interrupted-release contract, not inferred merely from an exception branch.
- Response: D5 binds pre-write artifact identity in the annotation, observes remote state and reuses exact retained bytes or refuses. No tag deletion/rollback framework. Proportionate; no finding.

### MP002 — First Docker hosting setup needs the candidate image reachable by registry digest

- Authority: REQ003/006/008, AC002/006/007, SCN002, BEH002/005; **Supported Normal Scenario**.
- Initiating basis: **Operational** — qualification owner exercises the approved first-use Docker-Linux storage mode on a designated clean owned host.
- Forward current path: ordinary CLI create with Docker backend and consent → setup plan records Release.EngineImage → backend engine setup → `internal/docker/engine.go:EnsureEngine` observes no owned engine and `create=true` → POST `/images/create?fromImage=<digest>` → create/start exact engine.
- Preconditions/consequence: new owned installation has no engine container. A locally loaded archive alone does not eliminate the actual pull call. An unavailable canonical registry would prevent the first-use qualification path before service creation.
- Reachability: **Reachable** from a clean supported installation, independently of the proposed test registry.
- Response: D3 serves the exact OCI digest from a test-owned registry and discloses the metadata-only alias; no runtime override, live-host trust change or claim of public-installer success. Final canonical anonymous pulls remain mandatory. Proportionate; no finding.

## Unresolved Approved-Behavior Or Current-State Gaps

None blocking architecture. Physical-host inventory, actual candidate, user verification, signing/notary validity and publication execution remain explicit downstream prerequisites, not ambiguity about intended behavior and not waived by this result.

## Review Decision

**Pass — ARCH-REV-001 / SR-003 on R2/SR-002.** Ready for implementation of the reviewed release architecture. Not a source-review, qualification, signing, publication, Delivery Completed or TaskDone result.

## Findings

None. No new behavior, platform reduction, credential questionnaire or adjacent-task work requested.

## Classification

Pass; failure classification **N/A**. Task size **Large**, architectural risk **High**, unchanged.

## Recommended Recipient

Fresh `get_handoff_rules` selected the primary implementation-ready Pass rule: **`/software_engineering_team/implementation_engineer`**. Apply the controlling single-most-specific-recipient convention: one primary dispatch, no duplicate informational/PM/API or closed extraction dispatch. The tool delivery receipt records forwarding; this document does not assert delivery before that succeeds. This review owns only its report/history, not upstream design edits or release execution.

## Residual Risks

- All six signing entries are provisioned, not validated. Actual P12/password pairing, selected identity/team and Accepted notarization must succeed in the intended job. Do not request repeated export/entry solely because old placeholder receipts exist.
- Four-target and mode-specific independent physical/current-source proof plus genuine user verification remain required. Hosted native tests, VMs, historical extraction or schema-valid JSON are not substitutes. Exact owned host/registry availability must be established by execution owners; no live-user storage or paid infrastructure authority inferred.
- Candidate retention, run-attempt reconciliation and full OCI preservation must be exercised with the chosen tools. Semantic unit/negative controls support but cannot replace hosted evidence.
- Final signed/qualified binaries differ from build-only candidates. Record that relationship and execute the specified final native/manifest/signature/download checks; same source hash alone is not final acceptance.
- Tag, draft, image and release are non-atomic. GHCR package visibility can require scoped administration; failures retain truthful partial-state receipts and safe refusal, not rollback/clobber.
- Actual first normal release/public downloads are still required for completion. Docs-only source enablement, this Pass, and earlier source CI cannot close the Task. API/Delivery retain final judgement and routing.

## Latest Authoritative Result

- Review Decision: **Pass**.
- Material-Premise Gate: **Pass**.
- Current round: **ARCH-REV-001**, resumed original SR-003 review; prior decision **N/A**.
- Notes: no blocking findings; only review documents authored. Requirements/design/source/credentials remain unchanged. Implementation and all executable release gates remain pending.
- Artifact checks: all 28 template sections present in order; report/history IDs and whitespace checked; no tracked production/unrelated delta from review input. These are document checks only.
