# Requirements — First NFS release

## Document Status
- **Approved — R2 / SR-002**, normal releases only. User explicitly selected removal of beta; Solution Designer approves the aligned requirements within the assigned direction, user informed in conversation2026-10-18. Architecture may proceed; implementation still needs completed design/applicable review.
- Package: `nfs-first-release`; Task `autobyteus-nfs-3` / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`; Project `project_6416db5b-926a-4865-8705-d8ebb2425780`.
- Requested by `/project_task_manager`, run `project_task_manager_a5f6d9d306e54970bafdad895bdf731d`; owner Solution Designer; date2026-10-18.
- User direction via PM: “we should ... enable the release ... improve it to enable release ... if you look at the SuperRapro project, RCI also do the release ... make the NFS project also do release.” Actual publication is authorized when readiness is established; this does not establish qualification or user-test evidence.
- Release basis: **v0.1.0** as the first normal release; thereafter strict `vMAJOR.MINOR.PATCH`, no beta/prerelease channel. Preserve the current four target tuples: native macOS26+ and Ubuntu24.04, ARM64/x64, with Docker-Linux storage engine. No target is silently dropped or marked qualified. No Product/UI supplement.
- Approval reference: user2026-10-18, “I will directly drop the beta release approach. I will just use the normal release.” SD notification: “NFS will use normal versioned releases, starting with v0.1.0, with no beta channel” and retained macOS/Ubuntu scope. This approves intent, not a user test or completed qualification. Behavior-defining supplement: none.
- Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`; branch `codex/nfs-first-release`; fresh base `origin/main`7e375984be2bea7a4d536e43cc59d6bc2b116870; finalization `origin/main`.

## Problem And Desired Outcome
The public NFS repository has no tags/releases or release-workflow runs. Its ordinary CI checks native code without downloadable executable assets. Its manual release workflow assumes an existing tag/release and has no currently qualified targets. Users cannot complete the intended public download/install journey.

Deliver a repeatable standalone CI-driven release journey, from a reviewed version/candidate through qualification and authorized publication to verified public downloads/install instructions. Actual first release, not YAML alone, is required for Task completion. Concrete external blockers keep the Task open. Prior extraction no-release instructions must be reconciled with this explicit follow-up, not treated as a permanent prohibition.

## Current, Desired And Preserved Behavior
| ID | Kind / scenarios | Current (evidence) | Desired | Preserve |
| --- | --- | --- | --- | --- |
| BEH001 | Operational SCN001 | Developer CI runs native checks; release build-only needs existing tag (E03) | Maintainer prepares a versioned candidate without hand-making a public release; receives usable, traceable non-public candidate artifacts | Ordinary push/PR never authorizes publication; candidate is not qualified merely by build |
| BEH002 | Contract SCN002/005 | Empty qualification; source/engine/physical/user/signing gates (E04) | Current candidate has explicit target/mode evidence and truthful readiness before publication | Required evidence, engine identity, exact source, Mac signing/notarization; no invented Pass |
| BEH003 | Operational SCN003/006 | Existing-release upload only; image can publish before Mac signing completes; clobber upload (E03) | Authorized version completes tag/release/assets/notes workflow, with clear staged/failed/partial/success outcomes | No moved published tags, no substituted qualified engine, no accidental competing-asset overwrite |
| BEH004 | User SCN004/005 | Placeholder installer refuses; qualified target absent; four-member archive/checksum/manifest guards (E05) | User downloads supported platform assets and follows exact versioned install/run guidance | Integrity checks, bounded archive/matching embedded metadata, no compiler/PPA requirement, unsupported-target refusal |
| BEH005 | Contract SCN002/004/007 | Host-only source/mount setup, data preservation, private state, coarse private-host trust (E06) | Behavior unchanged in release artifacts | App independence; consent; incompatible predecessor-state refusal; no live-user setup/upgrade by this task |
| BEH006 | Operational SCN007 | Extraction-era no-release/paired-finalization prose (E07) | NFS-only policy/docs describe current independent release process and observed support limits | Attribution/license/source provenance, safe main finalization and owned cleanup |

## Stakeholders
Maintainer selects approved version and advances evidence-backed release; end user obtains a usable supported CLI; API/E2E owns executable qualification; Delivery owns final evidence judgement, actual authorized publication, download confirmation and cleanup. User remains authority for material release/channel/platform changes. No application/server dependency.

## Scope Guardrail
### In-scope use cases
| ID | Use case | Scenarios |
| --- | --- | --- |
| UC001 | Prepare and identify release candidate | SCN001 |
| UC002 | Qualify candidate and reject incomplete publication requests | SCN002/005 |
| UC003 | Publish and recover the independently versioned release | SCN003/006 |
| UC004 | Download, verify and install supported CLI | SCN004/005 |
| UC005 | Reconcile policies, report evidence and finalize safely | SCN007 |

Out of scope: dashboard nfs-2, superrepo release/source changes, application integration/Guide activation, live-user mounts/data/nodes or upgrades, new NFS capabilities/backends/OS families, auth/encryption/public service, outage isolation, automatic remote notifications, editor/updater work, license changes or unrelated cleanup. No live storage migration. No silent platform drop or qualification weakening to obtain a green release.

Non-goals: auto-publication on arbitrary main/PR changes; desktop/mobile-version coupling; performance benchmarks or general filesystem equivalence; proving checksums resist a compromised publisher. No public beta/prerelease channel; internal build-only candidate artifacts remain necessary and are not releases.

Preserved boundary: BEH002/004/005. Existing source/wire protocol/backport/package selection/privileged consent/source identity and private-state behavior remain unchanged unless an actual in-scope defect requires solution recovery. Current physical and explicit-user verification gates remain until an explicit approved policy revision; the new publication request is not such evidence.

Review authority: blocking findings must trace to approved REQ/AC/preserved behavior. New behavior, platform, threat model or weakened qualification is a Requirement Gap for Solution Designer/user; adjacent problems remain non-authoritative follow-ups. No review comment silently amends scope.

## Requirements
| ID | Requirement | Behavior | Priority / rationale / source |
| --- | --- | --- | --- |
| REQ001 | Provide documented candidate and authorized-publication journeys without requiring the maintainer to manually pre-create a GitHub release; independent NFS version and exact source identity are consistent throughout | BEH001/003 | Required; user outcome/E03/E08 |
| REQ002 | Ordinary development CI and build-only candidates cannot publish releases/images or set qualification; candidates expose useful version/platform/provenance information and downloadable CI artifacts clearly labeled non-release | BEH001 | Required; user separation and existing policy |
| REQ003 | Preserve current source/engine, independent physical Mac/Linux/Docker and explicit-user verification gates; require evidence applicable to every advertised target/mode. Candidate/source/engine changes invalidate affected qualification. Report missing prerequisites concretely | BEH002 | Required; user prohibits fabricated evidence/E04 |
| REQ004 | Mac release assets must pass Developer ID signing/notarization; unavailable credentials are a named external blocker, never unsigned fallback or unapproved omission | BEH002/003 | Required; packaging policy/E09 |
| REQ005 | Publish only the approved version/channel/platform set with complete executable archives, installer, manifest, checksums, required engine image/corresponding modified source/inventory/notices and understandable release notes. Only strict normal vMAJOR.MINOR.PATCH releases are supported; reject beta/prerelease inputs; publish the first qualified v0.1.0 as a normal GitHub release | BEH003/004 | Required; explicit user normal-release choice / DEC001 |
| REQ006 | Promotion preserves tested candidate provenance and exact engine package identities; qualified input loss/expiration, hash mismatch, failed/cancelled checks or signing must fail closed. Partial effects and safe retry boundaries must be explicit, not clobbered or relabeled | BEH002/003 | Required; existing candidate contract and release safety |
| REQ007 | Public versioned download/install must verify archive and embedded/retrieved manifest consistency before installation; unsupported OS/CPU, wrong checksum or unsafe archive fails without host setup. Document actual OS floor/limits and exact version/run commands | BEH004/005 | Required; current installer guarantees/E05/E06 |
| REQ008 | Prove the resulting workflow through a real authorized release run and download/install checks on test-owned resources; preserve actual raw results/skips/failures and distinguish native fixture/build checks from filesystem qualification | BEH002/004 | Required; Task definition of done |
| REQ009 | Reconcile root/packaging/README/testing/release documentation with current direction and single-repository ownership, retaining license/attribution/source provenance and an honest release/support table | BEH006 | Required; contradictory extraction policy |
| REQ010 | Finalize on current integrated main under repo rules; preserve PM/unrelated work and archives, remove only task-owned resources, return URL/version/platform/assets/commands/evidence or precise still-open blocker | BEH005/006 | Required; Task constraints/done |

## Acceptance Criteria
| ID | REQ | Scenarios | Observable success / important failure | Verification intent |
| --- | --- | --- | --- | --- |
| AC001 | 001/002 | 001 | Candidate journey starts from an exact reviewed ref/version with no existing release; CI artifacts identify source/platform/engine; no public release/image/tag side effect in build-only | Actual hosted candidate run and remote inventory; unit controls supplement |
| AC002 | 003/006 | 002/005 | Selected targets have current-source actual candidate qualification and verification records; empty/stale/mismatched/missing physical/user evidence refuses publication | Semantic evidence audit plus executable negative controls; CI build alone insufficient |
| AC003 | 004 | 002/005 | Every selected Mac asset is signed and accepted by notarization; missing inputs/failed signing are explicit blockers before final public promotion | Actual signing/notary logs and downloaded artifact verification, no secrets in evidence |
| AC004 | 001/005/006 | 003/006 | Authorized run produces correct immutable normal version tag/source, non-prerelease status and complete release assets/notes; prerelease inputs are refused; repeat cannot silently replace another version/source/asset; failure leaves truthful recoverable disposition | Actual hosted run, tag/release/image identities and failure/retry controls |
| AC005 | 005/007 | 004/005 | Real public downloads match checksums/manifests; installed CLI reports version; exact commands documented. Unsupported/corrupt/mismatched archive rejected without setup; scope-specific platform prerequisites explicit | Owned HOME/temp/no-setup version smoke plus approved isolated actual-host qualification |
| AC006 | 003/006 | 002/006 | Published engine packages equal qualified candidate bytes, correct architecture/source/inventory/notices retained; missing/expired candidate cannot be silently rebuilt under an old Pass | Hash comparison and adversarial fixture; actual run identities |
| AC007 | 008 | 001–006 | Real first release completed; all required checks report truthful pass/fail/skip and evidence boundary. No workflow-only closure; external prerequisite keeps Task open | API/Delivery reports and public receipt |
| AC008 | 009/010 | 007 | NFS docs consistent; no desktop version/node coupling; licenses preserved; current main merge/push exact; cleanup and preserved-owner inventory complete | Source/doc review and finalization/cleanup receipt |

## Relevant Scenarios And Journeys
| ID | Actor / goal and trigger | Product-level sequence and outcome | Supported alternate / failure | Validity / evidence |
| --- | --- | --- | --- | --- |
| SCN001 | Maintainer, explicit candidate preparation | Choose intended NFS version/source; CI builds/checks; retrieve identified candidate and results without publication | Build/toolchain/package failure leaves failed evidence, not release | Supported Normal Scenario; user/E03/E07 |
| SCN002 | Qualification owner, candidate available | Verify candidate identities; exercise supported storage/client modes on designated test-owned hosts; record source/target/engine outcomes and explicit verification; determine release readiness | Unavailable physical host/credential/evidence remains blocker; no old same-kernel evidence promotion | Supported Normal Scenario; existing qualification policy/E04/E06 |
| SCN003 | Maintainer, authorized qualified version | Request publication; gates succeed; version tag/release/assets/notes available; verify public receipt | Any unmet gate fails; tag/release need not preexist manually | Supported Normal Scenario; explicit new user direction |
| SCN004 | User, supported host and public release | Follow versioned instructions, download/verify/install, run version/help or choose setup with normal consent | Host/runtime/permissions errors explained; installation smoke does not exercise setup on user's host | Supported Normal Scenario; README/installer/E05 |
| SCN005 | Safety contract, missing/changed input or unsupported host | Refuse wrong checksum/manifest/archive/target, stale evidence, missing signing or candidate before unsafe continuation | No best-effort unqualified publication or beta fallback | Supported Explicit Edge Scenario; existing checks and Task safety constraints |
| SCN006 | Maintainer, interrupted/failed or repeated release attempt | Inspect source/assets and stage status; retry only safe same-input failed work, otherwise choose new version; disclose partial publication | Never move published tag or clobber unrelated/different asset; keep original failed evidence | Supported Explicit Edge Scenario; superrepo recovery reference and current irreversible publication path |
| SCN007 | Delivery, successful release or external blocker | Sync docs/evidence, safely finalize current main, preserve unrelated work and clean owned resources; return definitive release receipt or exact blocker | Do not close Task as done for only workflow enablement | Supported Normal Scenario; Task done/constraints |

## UI / Quality / Data
Product UI/UX fields: **N/A — not applicable**. GitHub workflow inputs/results, CLI instructions and release notes are operational text, not a dashboard design request.

QR001 (REQ003–007/AC002–006): explicit source/artifact identity, fail-closed qualification and signed Mac artifacts. QR002 (REQ006/AC004/006): controlled retries preserve published provenance and failed evidence. QR003 (REQ009–010/AC008): independent versioning, preserved licensing and unrelated files.

Persisted/external state affected: Git refs/releases/assets/registry artifacts and release qualification records. Preserve published tags/assets/history, retained candidates and owner state. Regenerate only own disposable build/check output; no live user NFS state change or loss is authorized. No installed-state schema migration proposed.

## External Contracts And Supplements
GitHub Actions artifact retention/read-access, Release tag/asset semantics and Apple signing/notarization are external contracts (investigation E08). Expired artifacts/permission/credential failures are explicit blockers. No new costs or paid infrastructure purchase authorized.

`investigation-notes.md` is evidence, not intent. `evidence/intake/repository-release-preflight.json` is timestamped read-only repository/secret-name metadata; no credential values. No behavior-defining supplement beyond this R2; normal-only policy is DEC001.

## Decisions And Assumptions
| ID | Question / reasoning before recommendation | Owner / status |
| --- | --- | --- |
| DEC001 | User explains NFS releases will be infrequent and explicitly rejects the desktop-style beta approach. Use normal versions only; first v0.1.0 is the proposed independent initial version without implying a mature1.0 API. Retain the existing four-target scope rather than infer an unrequested Linux-only deferral. Required qualification/signing still gates every normal release. | User chose normal-only; SD selected initial version/retained scope within direction, user informed / **Decided**2026-10-18 |
| DEC002 | Current manual tag/release prerequisite obstructs end-to-end flow; automate controlled creation as part of authorized release, while retaining ordinary CI/build-only nonpublication. Exact trigger/structure belongs to architecture. | SD / Decided within direction |
| DEC003 | Prior extraction no-release is superseded by explicit publication authorization for this Task, but no physical/user/signing evidence was supplied by that authorization. Retain evidence gates and report blockers; do not invent a verification record. | SD / Decided within direction |
| DEC004 | Superrepo provides usability/recovery examples, not NFS platform promises, Android version limits or desktop version ownership. Its beta channel is explicitly not adopted. Keep NFS independent; no superrepo edits. | SD / Decided within direction |
| ASM001 | Available test-host inventory and successful signing/notary validation remain unresolved execution prerequisites. E18 confirms all six required repository-secret entries are now populated, including the user-confirmed selected local Developer ID .p12 and user-entered export/app passwords. Temporary private export removed; no secret values persisted in artifacts. This establishes provisioning, not password pairing/signing validity. GitHub read APIs expose no secret values; do not scrape source secrets or assume physical hosts are available/unavailable without an inventory. | API/Delivery prerequisite coordination; provision complete, validation/inventory open |

## Traceability And Architecture Input
REQ001/002 → UC001/003 → BEH001/003 → SCN001/003 → AC001/004.
REQ003/004/006 → UC002/003 → BEH002/003 → SCN002/005/006 → AC002/003/004/006.
REQ005/007/008 → UC003/004 → BEH003/004/005 → SCN003/004/005 → AC004/005/007.
REQ009/010 → UC005 → BEH005/006 → SCN007 → AC008.

Architecture must trace candidate/source/engine/image/binary/manifest/evidence/tag/release identities, permissions and failure boundaries after approval. Verify qualified-artifact preservation across build/promotion, installer trust and exact hosted gate behavior. The completed technical design is design-spec.md / SR-003, Ready for applicable independent review; requirements approval remains R2/SR-002. No persisted host-data migration is requested.

## Readiness
Problem/current/desired/preserved behavior, scope, testable traceability and supported scenarios: Yes. Product/UI: N/A. Material decisions visible: Yes. **Content ready: Yes; approval recorded: Yes (R2/SR002, user normal-only choice plus SD within-direction approval and notification); approved basis ready for architecture: Yes.** Publication execution also needs real candidate/qualification/signing prerequisites; these are not claimed ready and do not justify dropping gates.
