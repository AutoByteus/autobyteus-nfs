# Requirements — First NFS release

## Document Status / Approval
- **Approved — R3 / SR-004**, 2026-10-18. Supersedes R2/SR002 only for publication/testing sequence and the related distribution-admission claim. User explicitly approved publishing the official signed release first, then testing and fixing forward. Solution Designer approves the aligned details within that direction; no outstanding Needs user decision.
- Package `nfs-first-release`; Task `autobyteus-nfs-3` / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`; Project `project_6416db5b-926a-4865-8705-d8ebb2425780`.
- Requested by `/project_task_manager`, run `project_task_manager_a5f6d9d306e54970bafdad895bdf731d`; owner Solution Designer.
- Original request: enable independent end-to-end NFS release automation and actually publish the first downloadable release. User retained normal-only release direction: “I will directly drop the beta release approach. I will just use the normal release.”
- **Controlling new approval:** “please publish first, then we could test. and if we found problem, then we fix”; “create one official signed release first. please”. Exact durable source: `delivery-evidence/dr-003/user-publish-first-direction.json`, received from Delivery after it explained the unavailable independent/physical hosts. This is sequencing/publication authorization, **not** an executed-user-test receipt.
- First **v0.1.0**, normal/non-prerelease, four build/distribution targets `darwin-amd64`, `darwin-arm64`, `linux-amd64`, `linux-arm64`. Intended host floors remain macOS26+/APFS and Ubuntu24.04/ext4, with native Mac/Linux and Docker-on-Linux storage modes. Build availability does not assert field-qualified support.
- Approval details and scoped deferred-test supplement: `approval-record-sr004.md`, `postpublication-testing-plan.md`. SD notification in this conversation: publish-first gates will replace physical/user prerequisites; signing/integrity/host protections remain, deferred tests are not passed.
- Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch `codex/nfs-first-release`; intake HEAD `a5f57097578f9503eff0beb120dbc9e33e194eef`, integration target `origin/main`, last Delivery-refreshed base `7e375984be2bea7a4d536e43cc59d6bc2b116870`. Fresh fetch/integration remains Delivery-owned. Canonical checkout/PM boards/old archives are not authoring workspaces.

## Problem And Desired Outcome
The implemented release path can build candidates but currently prevents publication and installer admission without independent physical and executed-user qualification. The first complete candidate succeeded, yet API002 remained Blocked73.57 because assigned physical/independent test hosts were absent. GitHub has no public release at this recovery intake.

Publish a real official signed normal v0.1.0 through the reviewed workflow after current-source build/release-control/signing/integrity checks. Mark shared-filesystem/physical/user testing **Deferred — not executed for this release**, retain specific follow-up custody, test after publication and fix forward. Do not call build success filesystem qualification. Actual downloadable usable assets/install instructions, finalization and owned cleanup remain required; a YAML-only or build-only result is not done. External signing, integrity, repository or distribution-access blockers remain real blockers.

## Current, Desired And Preserved Behavior
| ID | Scenarios | Current evidence | Desired | Preserve |
| --- | --- | --- | --- | --- |
| BEH001 | SCN001 | Manual build-only candidate succeeds; E19/API002 | Current reviewed-source candidate with traceable four-target artifacts | Push/PR never publishes; no inferred field Pass |
| BEH002 | SCN002/005 | physical/user qualification blocks publication; E20 | Separate release readiness from deferred field/user testing; require evidence for the checks actually claimed | Exact source/engine/OCI, review/native/release-control proof and actual signing/notary; no fabricated userVerified or topology |
| BEH003 | SCN003/006 | Reviewed immutable tag/draft/assets/image publisher exists | Publish authorized normal v0.1.0 before field tests; preserve recoverable same-input partial stages | No force/moved tags, clobber, substituted artifact or unsigned fallback |
| BEH004 | SCN004/005 | Installer requires manifest QualifiedTargets, currently empty | Verified published-target binary is installable despite explicitly deferred field tests; show the limitation without a new approval questionnaire | Checksum, bounded archive, embedded/downloaded equality, wrong-target refusal, no Go/Homebrew requirement |
| BEH005 | SCN002/004/007 | Host-only setup/consent/source/state guards | Unchanged; publish/download/version checks do not touch live storage | Host OS/source/identity, admin/storage consent, private state, incompatibility refusal and safe detach |
| BEH006 | SCN007/008 | Docs retain prepublication physical/user gate | Consistent release-first policy and explicit postpublication test/fix custody | Independent NFS versioning, licensing, history, safe finalization/cleanup |

## Scope Guardrail
| ID | In-scope use case | Scenarios |
| --- | --- | --- |
| UC001 | Prepare identified nonpublic candidate | SCN001 |
| UC002 | Establish release readiness, disclose deferred field qualification | SCN002/005 |
| UC003 | Publish and safely recover the independent version | SCN003/006 |
| UC004 | Download, verify and install released CLI | SCN004/005 |
| UC005 | Reconcile policy, report release evidence, retain follow-up and finalize | SCN007/008 |

Allowed delta: release-readiness/evidence policy, packaging metadata, installer admission, workflow wording/necessary plumbing, affected tests and documentation. No current runtime filesystem capability change. No manual gate bypass: implement the changed authority coherently before publication.

Out of scope: dashboard nfs-2, Homebrew distribution, superrepo/app/Guide/editor/updater work, new backend/OS family, paid infrastructure, auth/public-service/outage/remote-notification features, live-user mounts/exports/firewalls/data/node upgrades, credential reprovisioning without demonstrated failure, licensing changes and generic cleanup. Closed tasks/archives stay closed.

Non-goals: public beta/prerelease, automatic main/PR publication, asserting production readiness or independent-client/physical/platform support from hosted builds. Internal candidates remain build-only. Physical/shared-filesystem and genuine user-check completion is **not a prepublication or this release-task closure prerequisite** under the explicit change; concrete handoff custody is required, not silent abandonment. Postpublication testing is separate scoped follow-up work, not authority to run against live user data.

Review authority: changes to signing/integrity/host protection or additional scope need Solution Designer recovery. Do not re-ask the settled publish-first/no-beta choice or restore missing-host questions as a release dependency.

## Requirements
| ID | Requirement | Behavior / priority |
| --- | --- | --- |
| REQ001 | Independent NFS version/exact-source candidate and authorized release journeys must work without hand-creating tag/release | BEH001/003; Required |
| REQ002 | Ordinary CI/build-only candidates cannot publish or imply field qualification; candidate identity/results stay explicit | BEH001; Required |
| REQ003 | For v0.1.0, permit release before independent/physical shared-filesystem and genuine user tests. Require truthful deferred status and scoped postpublication custody; retain current-source native/build/release-control evidence and source/engine/OCI applicability. Never fabricate physical/user proof or relabel API002/historical outcomes | BEH002/006; Required, direct new approval |
| REQ004 | Every Mac release binary must be Developer ID signed and notarization Accepted; real failures block, no unsigned fallback or omitted Mac target | BEH002/003; Required, unchanged |
| REQ005 | Publish normal non-prerelease v0.1.0 for all four build targets, with executable archives, installer, manifests, checksums, notes, exact engine image/corresponding modified source/inventories/notices. Reject beta/build-suffix versions | BEH003/004; Required, unchanged target/channel |
| REQ006 | Promotion must preserve current candidate provenance and exact engine/OCI bytes. Missing/expired/mismatched inputs or failed/cancelled required checks/signing fail closed; partial effects and same-payload retries remain explicit | BEH002/003; Required |
| REQ007 | Public installer must admit an intact release-authorized target while stating field/user validation is deferred; reject unsupported target, wrong checksum, unsafe archive or mismatched metadata before installation/setup. Preserve OS/setup safety and document exact commands/floors/limits | BEH004/005; Required |
| REQ008 | Exercise a real authorized publication and public download/install/version/signature checks on owned resources. Distinguish these from deferred NFS operations; preserve real failures/skips and native platform limitations | BEH002/004; Required |
| REQ009 | Align root/package/README/testing/release docs and public validation statements with R3; distinguish build targets from field-qualified support; retain licensing and test/fix-forward custody | BEH006; Required |
| REQ010 | Finalize reviewed current main, preserve other owners/archives, clean own temporary resources; return real URL/version/platform/assets/commands/evidence and deferred work or an exact remaining release blocker | BEH005/006; Required |

## Acceptance Criteria
| ID | REQ / scenarios | Observable success / failure | Verification intent |
| --- | --- | --- | --- |
| AC001 | 001/002; SCN001 | New current-source four-target candidate, exact run/attempt/engine/OCI/member identity; no publication in candidate mode | Actual hosted run and remote inventory; no old-candidate relabel |
| AC002 | 003/006; SCN002/005 | Audited release readiness permits explicitly deferred physical/user status; missing authorization/reference/candidate/build/source-review or stale identity refuses. No executed-user/physical Pass is required or invented | Updated schema/admission negative controls + semantic evidence review |
| AC003 | 004; SCN002/005 | Both Mac targets actually signed, Accepted notarization and exact downloaded signature evidence; missing/rejected inputs block before promotion | Actual Apple receipts/signature checks, no secret values |
| AC004 | 001/005/006; SCN003/006 | Real immutable exact-SHA normal tag/release/assets/image; honest release-first notes; conflict/failed prerequisite/unsafe retry refused, no overwrite | Actual workflow/publication + focused recovery controls |
| AC005 | 005/007; SCN004/005 | Public checksums/archive/manifest match, released target installs and version runs with deferred notice; candidate/old-qualified-only/wrong-target/malformed/corrupt metadata refuses without setup | Native/installer tests; actual owned-HOME public download/version proof, not NFS setup |
| AC006 | 003/006; SCN002/006 | Published engine packages and complete OCI equal the new candidate; metadata/signing delta attributable; stale/lost candidate cannot be rebuilt under old evidence | Actual hashes/identities and negative controls |
| AC007 | 008/003; SCN001–008 | First signed public release actually completed; current prepublication checks evidenced, field/user tests explicitly deferred with named owner/plan; old API002 remains historical Blocked | API/Delivery receipts, public downloads and follow-up custody, no filesystem campaign prerequisite |
| AC008 | 009/010; SCN007/008 | Docs and metadata make consistent bounded claims, licenses intact, main finalized/pushed, owned cleanup and preservation complete; follow-up handed off | Doc/source review and final receipt |

## Relevant Scenarios And Journeys
| ID | Actor / trigger / coherent sequence | Alternate / outcome | Validity / evidence |
| --- | --- | --- | --- |
| SCN001 | Maintainer requests versioned current-source candidate; CI builds/checks and retains identified artifacts | Failed build is failed candidate, never release | Supported Normal Scenario; original task/API002 |
| SCN002 | Release owner receives candidate; audits native/release checks and identity, records user-approved deferral, source review and test/fix plan; establishes release readiness | Missing physical hosts do not block; missing actual build/identity/review or signing still does | Supported Normal Scenario; direct user approval/E19–21 |
| SCN003 | Maintainer requests official signed release before field tests; preflight/signing succeed, immutable tag/assets/image published and downloads verified | Unmet retained gate keeps precise unfinished stage; no unsigned/beta workaround | Supported Normal Scenario; direct user words |
| SCN004 | User downloads versioned released CLI, sees deferred-field notice, verifies/installs and runs version; may choose normal setup with consent | Unsupported host/archive errors refuse; no automatic test on user's storage | Supported Normal Scenario; existing installer and user publish-first intent |
| SCN005 | Changed/missing inputs, unsupported target or false validation claim reaches admission | Fail closed on integrity/authority/claim mismatch; deferred testing alone is not an error | Supported Explicit Edge Scenario; retained safety contracts/R3 |
| SCN006 | Maintainer resumes interrupted publication | Reuse bound same payload, fill missing exact outputs or refuse conflict/expiry; different output requires new version approval | Supported Explicit Edge Scenario; existing publisher |
| SCN007 | Delivery completes release/finalization or encounters actual blocker | Evidence-backed receipt/owned cleanup, no build-only closure or false field Pass | Supported Normal Scenario; task done |
| SCN008 | After publication, delegated test owner receives scoped plan and exact release identities; gets test-owned hosts/user participation, runs field tests and reports/fixes through normal ownership | Unassigned resources remain explicit follow-up, not release blocker; any fix uses new reviewed version rather than overwrite | Supported Normal Scenario; latest user instruction, supplement |

## UI / Quality / Data / Supplements
Product UI/UX: **N/A — not applicable**; no dashboard. QR001: immutable integrity, explicit authorization/claims and signed Mac assets. QR002: safe repeat/partial-state handling. QR003: no app coupling, licensing and owner preservation. No new security or performance claim.

Release-control records and generated manifests are affected, not installed host/source state. Preserve candidate/history/failed evidence, immutable external identities and unrelated resources. Old build-only candidates can remain historical; no in-place reinterpretation as current source. The architecture must investigate actual readers/writers before deciding metadata transition. No live storage migration.

Behavior-defining supplement: `postpublication-testing-plan.md`, approved within this user-approved scope. Exact approval receipt and `approval-record-sr004.md` establish authority; investigation is factual evidence, not intended behavior. GitHub/Apple retention/access/signing constraints remain unchanged.

## Decisions / Uncertainty
- DEC001 unchanged: normal-only first v0.1.0/four targets, not beta or unsupported new platforms.
- DEC002 unchanged: automate controlled tag/release creation, ordinary CI remains nonpublishing.
- DEC003 **superseded for physical/user sequencing by DEC005**: publication approval remains distinct from testing evidence; signing/source/integrity gates retained.
- DEC004 unchanged: standalone NFS, no superrepo version/release change.
- DEC005 User decided publish first, test/fix later. SD chooses explicit release readiness versus field-validation terminology and installability to make this usable without a false qualification claim. No new waiver prompt, no platform omission, no auto-mount or silent field Pass. **Decided**, exact source above.
- ASM001 Six signing secrets provisioned; actual import/notary not yet proven. No fresh private input needed absent demonstrated error. Field hosts/user testing deferred; native/release/signature/public-access failures remain execution prerequisites. No paid hosts authorized.

## Readiness / Architecture Input
R3 ready and approved: supported scenarios/BEH/REQ/AC traceability, scope/limits/data preservation and user decision explicit. No material unanswered product question. Approval does not bypass implementation/review or invent a test result. Design SR004 must replace the qualification/install-admission dependency coherently, preserve immutable publication controls and invalidate changed production candidates. Prior SR003/ARCH001/IR002/CRR003 remain historical for the basis they covered, not a Pass for this change.
