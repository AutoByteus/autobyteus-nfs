# Requirements — Extract AutoByteus NFS

## Document Status
- Status: **Approved**; exact baseline **R1 / SR-001**, 2026-10-16.
- Package: `extract-autobyteus-nfs`; Task `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`; Project `project_6416db5b-926a-4865-8705-d8ebb2425780`.
- Requested by `/project_task_manager`, carrying the user's explicit repository-separation direction of 2026-10-16.
- Owner/approver: Solution Designer **within the direction (user informed)**. Approval reference: conversation message beginning “The NFS source, installer, packaging and service tests will move to the standalone repository.” No Needs user decision remains.
- Behavior-defining supplements: None. Prior filesystem artifacts are provenance, not renewed acceptance obligations.
- Authorities read: solution-designer SKILL; references/requirements-engineering.md; requirements and investigation templates; 2026-10-16.

## Problem And Desired Outcome
The independent Go service is maintained inside the AutoByteus superrepo and its developer/distribution tooling reaches into application files. Establish one maintained home at `/Users/normy/autobyteus_org/autobyteus-nfs`, preserving necessary source/tests/setup/build/docs, attribution and supported integration. A contributor can build and check the service without the superrepo; the superrepo no longer owns a second service implementation. Both repositories finish with validated, traceable commits and safe cleanup.

## Stakeholders, Actors, And Outcomes
NFS contributors need independent development; AutoByteus maintainers need an intact external-service contract; delivery maintainers need unambiguous ownership and provenance; users need unchanged installed behavior and no live mutations from this task.

## Relevant Scenarios And Journeys
| Scenario / use case | Actor, goal and supported trigger | Sequence and expected outcome | Alternate / error | Validity and independent evidence |
| --- | --- | --- | --- | --- |
| SCN-001 / UC-001 | Contributor clones canonical NFS repo to develop/build/check it | Install documented developer prerequisites, run checks/build, receive usable development binary and honest check results without AutoByteus checkout | Missing toolchain/engine prerequisite gives actionable failure, not an implicit superrepo dependency | Supported Normal Scenario; user's explicit standalone outcome; existing README developer flow |
| SCN-002 / UC-002 | Maintainer runs candidate packaging or installer/distribution checks | Prepare local candidate/metadata from owned inputs; preserve integrity, attribution and publication refusal until separately qualified/authorized | Unqualified/stale/malformed inputs refuse; build-only cannot publish | Supported Normal plus Supported Explicit Edge for refusal under existing packaging/security contract |
| SCN-003 / UC-003 | AutoByteus launcher/runtime uses an installed service | Existing launcher attachment command and descriptor/mount identity continue to govern mounting/admission; app checks no longer import sibling service source | Wrong identity/daemon/unsafe attachment continues to refuse; unavailable Guide remains unavailable | Supported Normal plus existing explicit refusal contract; launcher and TS binding readers |
| SCN-004 / UC-004 | Delivery maintainer finalizes the requested repository move | Establish standalone history with extraction provenance, remove superseded source ownership, commit/push both targets, record identities and cleanup | Concurrent remote or local owner changes are integrated safely or reported; never overwritten | Supported Normal plus explicit preservation contract in Task/RELEASE.md |

SCN-005: a live deployment/upgrade, full physical/cross-OS requalification or new app/editor journey is **outside approved scope**, not implied by mechanically being able to execute it.

## Relevant Current And Desired Behavior
| Behavior | Kind / scenarios | Evidence-backed current | Desired delta | Preserved |
| --- | --- | --- | --- | --- |
| BEH-001 | Operational / SCN-001 | Go module nested at autobyteus-nfs; installer fixture and build hash reach superrepo | Independent contributor workflow at canonical destination | Runtime semantics; developer prerequisite honesty |
| BEH-002 | Contract / SCN-002 | Same-superrepo release workflow/version check; unqualified lock, disabled public installer | Independent owned build/distribution inputs and docs, no new release | Integrity/signing/source obligations, physical qualification and explicit release authorization; no promotion of old evidence |
| BEH-003 | System / SCN-003 | Launcher consumes installed CLI; TS consumes /etc descriptor; one test reads sibling Go fixture | Retain consumer ownership and contract with independently runnable checks | CLI/descriptor/schema/paths, mount and source identity, permissions, lifecycle and safety policies; Guide null release |
| BEH-004 | Operational / SCN-004 | Current source integrated at 3712cd9bf0db998501d162db7f8655f169e3def6; destination unborn main plus PM metadata | One maintained source home, auditable two-repo finalization | Existing source history, prior archives, PM boards, unrelated changes and ignored assets |

Evidence authority: investigation-notes.md, source log E01–E10.

## Scope Guardrail
In-scope use cases UC-001–004 only: coherent service extraction, necessary source-side removal/integration/reference/build/test/docs changes, repository policy establishment and finalization.
Out of scope: new filesystem/backend capabilities, outage isolation, Mac Docker Desktop hosting feasibility, auth/encryption/public service, automatic remote notifications, rejected UNFS alternatives, updater/editor work, unrelated cleanup. Prior Task0793009f and completed editor a4f90984 stay closed. Do not rewrite unrelated history or finalized archives, change licensing, mutate live mounts/storage/Docker nodes, deploy or upgrade.
Non-goals: a new public release/version/tag; new runtime-platform qualification; throughput/scalability benchmarks; importing all historical tickets into the new repository.
Preserved boundary: BEH-002–004 / REQ-003–007. Repository relocation is not installed-data relocation.
Review authority: blocking findings must cite these requirements/ACs/preserved behavior. New behavior/security/policy/migration promises require a Requirement Gap and approval before becoming authoritative. Adjacent proposals are nonblocking follow-ups, not implicit scope.

## Requirements And Traceability
All are Must; rows also provide requirement → use case → behavior → scenario → AC traceability.
| ID | Requirement and rationale | UC / BEH / SCN | AC |
| --- | --- | --- | --- |
| REQ-001 | Maintain NFS source, tests, setup/build tooling and docs solely in canonical independent repository; avoid a second maintained implementation, subrepo checkout requirement or hidden sibling dependency | 001 / 001 / 001 | 001 |
| REQ-002 | Standalone documented build/check and candidate preparation work with declared Go/Python/platform tooling; engine packaging uses its own exact source/artifact inputs, not app source | 001,002 / 001,002 / 001,002 | 002 |
| REQ-003 | Preserve delivered service behavior and public consumer contracts, including source/mount/storage identity, permissions/private state, launcher decisions, reconnect/refusal and safe detach; retain required AutoByteus integration and its tests | 003 / 003 / 003 | 003 |
| REQ-004 | Preserve license texts, applicable additional permissions, attribution, third-party notices/source recipe/pins and traceable source commit/path provenance | 002,004 / 002,004 / 002,004 | 004 |
| REQ-005 | Keep unqualified/default metadata, publication refusal, integrity/signing/candidate-reuse gates and Guide unavailable state; extraction neither authorizes nor claims new platform/publication qualification | 002,003 / 002,003 / 002,003 | 005 |
| REQ-006 | Update active references/consumer test inputs and remove superseded embedded implementation/distribution ownership without editing historical evidence; source app remains buildable/checkable without local NFS checkout | 003,004 / 003,004 / 003,004 | 006 |
| REQ-007 | Finalize both repositories with exact target/commit identities under applicable rules; preserve unrelated dirty work/PM metadata/history/assets; clean only task-owned temporary resources; do not mutate live resources | 004 / 004 / 004 | 007 |
| REQ-008 | Provide fresh extraction/integration evidence, explicit skipped/blocked/not-required limits, historical provenance clearly separated, and actual remaining decisions; no false aggregate “fully qualified” claims | 001–004 / 001–004 / 001–004 | 008 |

## Acceptance Criteria
| ID | Preconditions / trigger | Observable expected outcome | Alternate / verification intent |
| --- | --- | --- | --- |
| AC-001 | Clean isolated checkout of standalone candidate, no source superrepo access | Documented service build/unit checks and Python fixtures resolve only local owned files and declared external tooling | Inspect file/import inventory and execute from independent scratch; missing tool cannot be counted Pass |
| AC-002 | Same candidate, nonpublishing packaging checks | Source hashing, metadata, manifest/embed/integrity fixtures, archive/installer checks and four-target compilation use new paths; changed qualified inputs invalidate qualification | Fresh test/build evidence plus executable path/negative controls; distinguish empty development assets from release-ready Linux artifact |
| AC-003 | Current extracted service and source consumer candidate | Relevant Go contract/safety/lifecycle tests and app binding/launcher tests pass with unchanged public fields/output/path semantics; explicit cross-repo fixture equality is evidenced at pinned service revision | Compare normalized runtime source; preserve actual parser tests and negative controls, do not replace them with string-only checks |
| AC-004 | Extraction candidate inventory | License unchanged, additional permission and owner attribution retained, exact engine pins/patch/source obligations retained; source repository+commit+path/remap provenance available | Inspect tracked candidate/packaging contents; no legal terms rewritten |
| AC-005 | Default unqualified state; local build-only/refusal controls | Publication remains refused; stale/current-source qualification correctly invalidates; Guide has no enabled download/copy command; no release/tag/image push/deployment performed | Run refusal and workflow gate fixtures; read workflow syntax/paths; signing/live CI not executed is explicit limitation |
| AC-006 | Both candidates integrated | Embedded Go project, NFS-owned workflow/installer/tests removed from source; active docs/test references point to maintained home or owned consumer fixture; no stale build ownership | Tracked-reference audit excluding historical tickets; focused source tests/typecheck as affected; no sibling checkout required |
| AC-007 | Delivery, refreshed refs and preserved canonical checkout state | Destination main and source personal finalized per policy; exact committed/pushed identities recorded, no force overwrite, owned scratch cleaned, unowned assets untouched | Git/cleanup receipts; concurrent changes require re-integration or precise blocker; unsafe/unneeded removal recorded Not required |
| AC-008 | Handoff/delivery | Evidence matrix maps ACs to actual checks and limits; no old failed/blocker receipt relabelled; no hidden required gate left | Delivery verifies evidence, reports remaining decisions if any; no new user questionnaire or old editor/VM acceptance gate |

## UI, Interaction, And Experience Requirements
Applicable: No. Product design fields, visual references and Product approval: **N/A — not applicable**. Preserve existing disabled Guide; no UI work requested.

## Quality And Non-Functional Requirements
- QR-001 security/integrity: REQ-003,005 / AC-003,005, unchanged installed paths/private data and refusal contracts; no live modification.
- QR-002 operability: REQ-001,002,006 / AC-001,002,006, independently usable docs and executable checks.
- QR-003 attribution/provenance: REQ-004 / AC-004, unchanged terms/source obligations.
- QR-004 preservation: REQ-007,008 / AC-007,008, two-repo identities and truthful evidence.
No new performance target.

## Data Continuity And Acceptable Loss
Persisted/external runtime data affected: **No intended change**. Preserve all workspace bytes, source IDs, descriptors, mounts, private config, Docker nodes/volumes, app data, PM metadata and old evidence. Only task-owned build scratch can be rebuilt/deleted. Extraction must not invoke installed create/connect/upgrade/detach as a migration. Architecture confirms Not Affected against readers/writers.

## External Contracts And Dependencies
- Existing Go CLI/descriptor v1 and installed filesystem paths remain authoritative public integration; no internal Go imports by the app.
- Existing exact distro/Ganesha source, patch, manifest identities and third-party terms remain required.
- Go toolchain, Python stdlib/Bash for fixtures; Docker/native runners only for applicable packaging checks, isolated from live nodes.
- GitHub destination origin supplied by user; repository initially empty. No credential/secret/branch-protection reconfiguration authorized.

## Supplemental Artifacts
None behavior-defining. Investigation links incoming prior delivery context read-only; design and later validation derive from this R1, not old full-platform acceptance gates.

## Assumptions And Decisions
| ID | Question / evidence and reasoning → decision | Owner / status |
| --- | --- | --- |
| DEC-001 | User explicitly wants independent service and removal of embedded copy; app launcher/TS integration is a consumer, not the service → move service-owned development/distribution, retain application-owned integration | Solution Designer / Decided |
| DEC-002 | Existing checkout has unborn main, no committed policy; source has explicit personal policy → establish destination main finalization policy, retain source personal, no release; check races before writing either remote | Solution Designer / Decided within requested repository establishment |
| DEC-003 | Importing unrelated app or full history would preserve accidental coupling; traceability can point to immutable source commit → bounded tracked-source snapshot with exact provenance, no unrelated-history rewrite/import | Solution Designer / Decided |
| DEC-004 | Build/qualification tooling must be standalone yet old receipt is bounded → rebase identity to service-owned inputs and retain separate explicit consumer evidence for integration; clear/unqualified publication remains, no inferred new qualification | Solution Designer / Decided; technical mechanism in design |
| DEC-005 | Runtime relocation is unnecessary and unauthorized → preserve all installed paths/contracts; test extraction delta without reopening full VM/UI qualification | Solution Designer / Decided |

ASM-001: destination remains empty/unowned except PM metadata until finalization; observed at bootstrap, recheck by implementer/delivery, never assume exclusivity. No outstanding product decision.

## Architecture Phase Input
Map SCN-001–004 and BEH-001–004 through actual build/distribution/consumer/finalization paths. Verify all embedded path assumptions, module imports, release source identity, workflow tag/package dependency, fixture ownership, licensing context and installed state invariance. Determine concrete copy/remove/path conversion and self-contained evidence boundary after approval. Risks: stale sibling references, accidental qualification weakening, two-repo partial finalization, hidden copying of unowned/generated assets.

## Readiness Check
Current behavior evidenced, intended/preserved behavior explicit, scope/testable ACs/scenario validity/decisions/traceability complete: **Yes**. Product/UI: **N/A**. Content ready: **Yes**. Approval and exact basis recorded with user informed: **Yes**. Approved basis ready for architecture: **Yes**. Remaining blocker: **None**.
