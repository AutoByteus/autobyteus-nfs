# Requirements — Extract AutoByteus NFS

## Document Status
- Package `extract-autobyteus-nfs`; Task `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`; Project `project_6416db5b-926a-4865-8705-d8ebb2425780`.
- Requested by `/project_task_manager`; original repository-separation direction supplemented by the user's direct filesystem-only boundary correction on 2026-10-16.
- **Approved R2 / SR-003**, 2026-10-16. Approver: Solution Designer within the explicit corrected direction; user informed in the conversation message beginning “Exactly. The boundary should be a directory path—not an NFS attachment contract.” The message also states that application-private runtime data stays separate regardless of filesystem type. No Needs user decision remains.
- Approval input: `user-filesystem-boundary-correction.md`, containing the user's own words. R1's requirement to preserve NFS-specific application integration is superseded, not silently retained. R1 and ARCH-REV-001 remain historical at Git commits 381231ee / 5d354b9.
- Authorities read: solution-designer SKILL, full requirements-engineering standard and requirements/investigation/history templates; source root and package policies; new NFS root policies. Evidence: investigation-notes.md.

## Problem And Desired Outcome
Establish one maintained Go NFS project at `/Users/normy/autobyteus_org/autobyteus-nfs`, independently developable/buildable/checkable. Remove the embedded implementation from the superrepo. The filesystem path is the entire application integration boundary: NFS manages sharing and mounts; AutoByteus uses normal filesystem APIs and must not identify NFS, determine whether a path is mounted, read NFS attachment descriptors or invoke the NFS CLI.
This replaces the earlier extraction-only assumption of unchanged application coupling. It is not a new filesystem implementation, live deployment or requalification of prior Tasks.

## Stakeholders, Actors, And Outcomes
NFS contributors need an independent service; application maintainers need ordinary path-based workspace behavior; operators own making storage available and mapping directories into containers; delivery maintainers need traceable two-repo commits and preserved unrelated work.

## Supported Scenarios And Journeys
| Scenario / use case | Actor, trigger, sequence and expected outcome | Alternate/error | Validity / evidence |
| --- | --- | --- | --- |
| SCN-001 / UC-001 | Contributor clones NFS repo, installs declared tools, develops/builds/checks without a superrepo checkout | Missing prerequisite produces truthful failure/skip, not hidden sibling dependency | Supported Normal Scenario; original user request and E02–07 |
| SCN-002 / UC-002 | Maintainer prepares a nonpublishing candidate/installer check from service-owned inputs | Unqualified, malformed or stale inputs refuse; build-only cannot publish | Supported Normal and Supported Explicit Edge Scenario; E04–07 |
| SCN-003 / UC-003 | Operator supplies a directory to AutoByteus, optionally exposes it using the existing generic Docker workspace mapping; user selects workspace and performs normal file/run/terminal operations | Normal path/permission/I/O errors apply. A registered workspace that cannot resolve is not silently replaced with another workspace. No NFS metadata is needed | Supported Normal and Supported Explicit Edge Scenario; direct user correction E12, app/launcher traces E14–16 |
| SCN-004 / UC-004 | Delivery finalizes independent maintained source and source-side decoupling, records two-repo identities and owned cleanup | Concurrent owner/ref changes are integrated safely or reported, never overwritten | Supported Normal / explicit preservation edge; original Task |
| SCN-006 / UC-005 | Operator uses standalone create/connect/status/reconnect/drained detach for a host export/mount | Wrong source/mount identity, invalid permission/configuration, busy detach or incompatible existing node-managed installation refuses before resource mutation; source bytes remain | Supported Normal / explicit safety edge; existing host flow E18–19 |
| SCN-007 / UC-006 | A supported runtime prepares configured skills for a run on any directory, then completes/fails/cancels | Application-generated exposure files stay in application-private execution storage; project-owned skills survive; failure remains scoped to the run | Supported Normal / explicit cleanup edge; existing private profile owners E15 |

SCN-005 (retained ID): live deployment/upgrade, full cross-OS/physical qualification, old editor acceptance, paid/provider-authenticated campaigns or publication are outside scope. Arbitrary filesystem failure repair and mount-loss isolation are not implied by ordinary filesystem APIs.

## Current, Desired And Preserved Behavior
| Behavior | Current evidence | Desired delta | Preserved outcome |
| --- | --- | --- | --- |
| BEH-001 operational | N now contains an unvalidated extraction; original embedded build roots crossed repos | Self-contained source/tools/tests/docs, no second maintained copy | Go service/platform prerequisites remain explicit |
| BEH-002 contract | Unqualified lock and controlled release workflow | Service-owned distribution identity, independent version/tag ownership | Licensing, source integrity, signing/publication refusal; no new release |
| BEH-003 system | App admission, terminals, skills and launcher read NFS state / mount identity; NFS probes/manages app nodes | Remove two-way product coupling. App consumes ordinary paths and normal OS outcomes | General filesystem API behavior, app-private state, selected registered workspace identity, normal launcher private volumes |
| BEH-004 operational | Two isolated branches, old-basis implementation held | Complete coherent extraction/decoupling and safe finalization | Histories, unrelated dirty work, PM boards, old finalized archives/assets |
| BEH-005 system | NFS setup coordinates host sharing AND optional app-node recreation | NFS owns export/mount/backend lifecycle only; no application-node discovery/control/API probes/public app descriptor | Source UUID/binding, trust/permission checks, hard-NFS semantics, host reconnect and safe drained detach |
| BEH-006 system | Private runtime skill profiles selected only when NFS descriptor covers workspace | Use application-private configured-skill exposure uniformly for already-capable runtimes; selection is not filesystem-based | Project-owned skills, configured bindings/collision policy, exact execution cleanup, credentials/history locations |

## Scope Guardrail
In scope: UC-001–006, standalone service extraction, necessary removal of app-specific coupling in both products, generic path/runtime behavior replacing those branches, corresponding tests/docs/policies and two-repo finalization.
Deliberately removed: app mount/UUID admission and auto Git-trust adjustment, NFS selected-node setup/recreation/recovery and published app attachment protocol. These are no longer preservation requirements.
Out of scope: new filesystems/backends, outage isolation, Mac Docker Desktop hosting feasibility, auth/encryption/public-service scope, automatic remote notifications, rejected UNFS alternatives, unrelated cleanup, updater/editor work, provider redesign or generic storage abstraction framework. Prior filesystem Task0793009f and editor a4f90984 remain DONE.
No live mount/storage/node/credential/config mutation, automatic installed-data migration, deployment/upgrade, history rewrite, licensing change, public release/version/tag. Preserve sources/markers/user bytes and other owners' work. Reviewer proposals beyond this guardrail are follow-ups, not new acceptance gates.

## Requirements And Traceability
All Must. Stable earlier IDs retained; new 009–010 make corrected obligations explicit.
| ID | Requirement | UC / BEH / SCN | AC |
| --- | --- | --- | --- |
| REQ-001 | One maintained NFS source/tests/setup/build/docs home, no hidden superrepo checkout or second source copy | 001 / 001 / 001 | 001 |
| REQ-002 | Declared standalone build/check/candidate preparation uses service-owned exact inputs | 001,002 / 001,002 / 001,002 | 002 |
| REQ-003 | AutoByteus application/runtime/launcher must neither classify filesystem/mount state nor require NFS CLI, descriptor or storage UUID. Consume ordinary paths and handle normal filesystem results/errors | 003 / 003 / 003 | 003 |
| REQ-004 | Preserve license/permission/attribution/third-party source obligations and exact extraction provenance | 002,004 / 002,004 / 002,004 | 004 |
| REQ-005 | Keep unqualified metadata, publication refusal, integrity/signing/candidate-reuse gates. No claim of newly qualified platforms or enabled NFS download | 002 / 002 / 002 | 005 |
| REQ-006 | Remove superseded embedded service and active two-way integration owners, protocols and sibling/contract test dependency; both projects independently build/check | 001,003,004 / 001,003,004 / 001,003,004 | 006 |
| REQ-007 | Finalize exact targets/commits under policies; preserve PM/unrelated work, original archives/assets; cleanup only owned scratch; no live action | 004 / 004 / 004 | 007 |
| REQ-008 | Fresh evidence and truthful limits, separate old proof/failed checks from current results; report actual remaining gates | all / all / all | 008 |
| REQ-009 | NFS keeps its host source/export/mount/security/lifecycle responsibilities, not AutoByteus-node control. Do not reinterpret an active old node-management obligation as harmless deleted fields or mutate that installation | 005 / 005 / 006 | 009 |
| REQ-010 | Application private runtime state remains app-owned, independent of filesystem classification; retain configured-skill/collision/cleanup semantics and normal Git trust policy, never global/wildcard trust | 003,006 / 003,006 / 003,007 | 010 |

## Acceptance Criteria
| ID | Trigger / observable expected outcome | Verification intent / negative boundary |
| --- | --- | --- |
| AC-001 | Clean NFS archive without source repo builds/checks using documented tools | Local import/file audit plus actual independent checks; missing tool is not Pass |
| AC-002 | Nonpublishing packaging/source hash/manifest/embed/installer checks and target compilation work in new layout | Current input mutation invalidates qualification; exact engine pins; distinguish runtime, compile and fixture evidence |
| AC-003 | Ordinary workspace file operations, registered workspace resolution, run preparation and terminal creation do not call mount observation, NFS CLI or attachment parsing | Absent/stale/malformed NFS metadata cannot affect behavior. Actual ordinary-directory path works; missing/denied path remains ordinary failure. Existing directory after an absent mount is still just a directory to the app—no special storage-identity guarantee |
| AC-004 | License/permission/provenance and engine source recipe/pin/notice audit passes | No license rewritten and no historic bounded proof promoted |
| AC-005 | Empty qualification and build-only/refusal controls still refuse publication; Guide remains unavailable | No release/tag/image push/deployment; hosted Actions/signing/physical platform execution not performed must remain explicit |
| AC-006 | S owns no embedded Go project/service workflow/installer, NFS mount-admission/launcher protocol or paired attachment fixture. N has no app node discovery/control/probe dependency | Active reference/import/source-hash audit, focused actual parser/owner tests for retained contracts, app production build/typecheck; old tickets exempt |
| AC-007 | Both repos finalized to origin/main (N) and origin/personal (S), exact push/cleanup receipts | Fresh refs, no force; canonical D0 populated only safely; PM and unowned assets byte-preserved; partial completion reported if necessary |
| AC-008 | Evidence matrix maps every AC, distinguishes pre-change history/held checks/current results and cleanup | No completed old campaign re-labelled; no invented live user check or reopened editor acceptance |
| AC-009 | Host-only create/connect/status/reconnect/detach retain source/marker/mount/nonroot/allowlist/backend safety; no app node/HTTP activity | Unit/integration fixture proofs of preserved host lifecycle; old active node-bearing state refuses before binary replacement or resource/config mutation; node-free records remain directly usable; no user-byte migration/deletion |
| AC-010 | For Claude/Codex/Grok configured skills, ordinary workspaces use existing private profile ownership/collision/cleanup contracts without mount classification; runtimes already using private storage keep it | Exact owner registered before async acquisition; concurrent profiles isolated; close-before-release, failed preparation cleanup, project skill/source preservation; no generated configured-skill exposure written into project as fallback, no automatic safe.directory injected |

## UI / Interaction
No new UI/UX design. Existing NFS Guide may remain informational documentation for an external tool; it must not promise automatic app-node attachment or determine workspace admission. Keep disabled download/copy state. Necessary factual copy/reference correction only; no Product Design handoff or editor changes.

## Quality And Nonfunctional Requirements
Preserve source/permission/ownership safety inside NFS (not reimplemented in app); preserve application runtime credential/history ownership. No assurance all filesystems have identical timing, notification or failure behavior. Existing NFS visibility/cache semantics remain NFS-side obligations; ordinary app I/O can block or fail as supplied filesystem does. No new outage deadline or benchmark.

## Data Continuity And Acceptable Loss
No user data loss, reset or bulk migration allowed. Workspace registry/history/credentials/source bytes/markers remain. Private profiles are per-execution generated state with existing exact cleanup; no sweep of old project skill links or historical profiles. Old public descriptors become unused by current consumers and are not deleted as task cleanup. Already-configured host-only NFS records retain meaning; active old node-management state requires explicit unsupported/refusal disposition and operator recovery with its matching old tool, not silent adoption. No such live recovery is executed by this Task.

## Decisions / Reasoning / Approval
- DEC-001 **Revised:** prior installed protocol preservation contradicted user's direct instruction. Required integration now means ordinary path use; NFS and AutoByteus must not require each other at runtime/build/test time.
- DEC-002 retained: N main / S personal finalization with fresh refs and no force; no release.
- DEC-003 retained: tracked snapshot with immutable provenance, not unrelated history import.
- DEC-004 revised: service-only source identity; no app qualification fixture/pin. Prior publication gates stay closed; changes do not qualify new behavior.
- DEC-005 revised: runtime policy is affected, though no installed-data move/deployment is authorized. Removed app mount-readiness guarantees are explicitly not promised elsewhere in app.
- DEC-006: use existing private runtime profiles for configured skills on every workspace of the already-capable runtimes, rather than exposing generated files to potentially shared projects. App-owned path/permissions, not underlying filesystem classification, define this boundary; operator remains responsible for deployment topology. No new provider framework.
- DEC-007: registered workspace resolution failures propagate equally for all filesystems; retain existing no-workspace/unknown-ID behavior outside that known-path case. Ordinary I/O does not warrant bypassing Git's ownership checks; remove implicit trust injection rather than extend it to all paths.
- DEC-008: remove app-node administration from NFS but keep Docker as an NFS storage-engine backend. Preserve active predecessor obligations through bounded refusal, not a second old execution path or automatic migration.
All decisions owned by Solution Designer within corrected direction and original preservation constraints. R2 approval applies to REQ/AC001–010, UC001–006, revised BEH003 and new BEH005–006. User informed as recorded above. No outstanding product decision.

## Architecture Input / Readiness
Requirements evidence E12–19 and hold checkpoint supersede R1 assumptions. Rebuild design around generic application paths plus standalone host NFS lifecycle; inspect current private profiles, state readers/writers and Docker engine dependencies before removing mixed modules. Large/High impact anticipated but final classification follows completed design. Readiness: scenarios, preserved/changed behavior, testable ACs, state dispositions, approval and scope complete; **ready for architecture**. Implementation remains held until replacement reviewed dispatch.
