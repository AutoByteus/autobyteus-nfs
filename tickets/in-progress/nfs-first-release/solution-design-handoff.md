# Architecture Design Complete — release-first recovery SR004

## Identity / outcome
**nfs-first-release / autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5**; Project6416db5b-926a-4865-8705-d8ebb2425780. Requested by `/project_task_manager`, run project_task_manager_a5f6d9d306e54970bafdad895bdf731d.

**R3/SR004 Approved; SR004 design Ready; Large / High.** Changed basis needs its configured review; previous ARCH001 is not a Pass for it. Result is Architecture Design Complete, not implementation completion, API Pass, Delivery Completed, release or TaskDone.

Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch `codex/nfs-first-release`. Ticket `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release`. Recovery intake a5f57097578f9503eff0beb120dbc9e33e194eef; reviewed prior product8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34/IR002/CRR003. Last Delivery-refreshed base/main7e375984be2bea7a4d536e43cc59d6bc2b116870, finalization origin/main after fresh Delivery checks. SD final doc commit is supplied in the message, no main merge/push.

## Original goal and exact changed approval
User originally authorized enabling and **publishing** the first independently versioned NFS release; normal-only v0.1.0, no beta. After Delivery explained successful candidate and unavailable physical test hosts, user said:

> please publish first, then we could test. and if we found problem, then we fix

> create one official signed release first. please

Exact source `delivery-evidence/dr-003/user-publish-first-direction.json`. R3/approval-record-sr004 records this approval, not a user test. Do not repeat the same release decision or physical-host questionnaire as a prepublication gate. No new product question is open. The approved supplement postpublication-testing-plan.md retains scoped testing/fix custody.

Goal remains real official signed v0.1.0 assets through actual workflow, then field/user testing and fix-forward. Preserve all four Mac/Linux build targets, unchanged intended OS floors, Developer ID/Accepted notarization, source/artifact/engine/OCI integrity, immutable tag/assets, recovery and host-data safety. Release-first does not mean unsigned, beta, silently qualified or no checks. No live storage change, dashboard, app/superrepo coupling, new backend, paid hosts or secret reprovisioning.

## Evidence and narrow completed design
- Current qualification.py and all publisher/payload call sites require physical/user Pass, and VerifyRelease requires QualifiedTargets. These are correct old-R2 behavior, now contradicted by explicit new intent. A publisher-only bypass would leave installer blocked or require a false qualification claim.
- Replace that single control owner with readiness.py: real current candidate/native/release-control/source-review evidence, actual release-first authority and deferred field/user status; no synthetic pass rows/userVerified. Null/mismatched/stale references still refuse.
- Clean-cut generated/runtime schema2: releaseTargets distinguishes install permission from fieldValidation={filesystem:deferred,user:deferred}. --release replaces --qualified; candidate targets empty. Keep exact manifest/engine equality/strict admission at existing VerifyRelease and show a concise stderr notice. No host-state migration or runtime filesystem logic change; no extra confirmation prompt.
- Current effect ordering/signing/OCI retention/same-payload recovery reused. Public notes/provenance declare deferred status. Stable packaging/releases/v0.1.0 readiness/evidence paths prevent archive-induced broken references. Implementation updates root/package/README/TESTING policy simultaneously; SD has not changed/bypassed executable gates.
- Source hash includes changed runtime/control/workflow/installer: **a NEW actual reviewed candidate is required**. Do not relabel API002 candidate as current or exclude changed files from hashing. After that, same-production-hash evidence-only descendants may advance normally.
- API validates affected release/admission/workflow scope and current candidate, not another full field/application campaign. Delivery owns actual credentials/signing/publication/download/finalization. Field/user tests are deferred with custody, not release-task closure prerequisites; terminal SD hands the scoped follow-up once to PM.

Concrete contracts, removal plan, migration decision, production paths, file map and validation intent are in design-spec.md. Existing safety/signing rules are retained, not reinvented. This scope merits Large/High independent delta review; do not restart settled product choices or dispatch directly around review.

## Current execution state / custody
API002 report remains **Blocked73.57**, API001 Fail62.86 historical. Actual build-only run39113335636/attempt1 on96c8de3a381f74ec8f2b9e93425fb90e17e7e693 and artifact12131531399 succeeded; signatures/physical/user/publication not proven. API retained candidate `/Users/normy/nfs-first-candidate-api002-n940gd8s/candidate` stays untouched; it becomes historical after new production changes, not silently deleted. Intake read-only GitHub releases/tags counts0/0.

All six signing secrets already provisioned. Import/password/account/Accepted notarization not yet validated; use intended jobs, do not ask to re-enter credentials absent an actual failure. No credential values read/written in this round.

**Other-owner work:** Delivery's untracked handoff-summary.md, docs-sync-report.md, release-deployment-report.md, delivery-revision-record.md and delivery-evidence/dr001–003 belong to Delivery. Preserve/exclude from unrelated staging. API/source/review history, canonical checkout, PM boards, archives/unowned caches remain intact. SD changed only own solution documents/supplements/admin evidence; no production, product tests/builds/CI/live resources/remote effects. Source/preservation audit is administrative only.

## Canonical documents / selected references
All paths below are within the absolute ticket folder above unless stated otherwise:
- Own authorities: requirements-doc.md, investigation-notes.md, solution-revision-record.md, design-spec.md, this solution-design-handoff.md.
- Approval and deferred scope: approval-record-sr004.md, postpublication-testing-plan.md.
- Exact external direction: delivery-evidence/dr-003/user-publish-first-direction.json (Delivery-owned).
- API evidence/retained candidate and raw links: api-e2e-execution-coverage-report.md (API002).
- Prior review basis: design-review-report.md and architecture-review-revision-record.md (ARCH001, historical SR003 only). New review artifact N/A — not yet applicable.
Implementation-handoff.md/revision-record, code-review-report.md/revision-record and Delivery handoff/history remain available for scoped context; no forwarding of all raw files. Earlier SD authority snapshots are under evidence/release-first/sr004; old finalized tasks are read-only.

## Expected next output
Configured architecture review of **R3/SR004 delta**, then reviewed implementation → independent affected validation → Delivery actual signed release. Review concerns must trace to approved R3/AC or retained safety; release-first is settled direction, not a request for more host allocation. Missing real signing/access/integrity prerequisites remain exact blockers; no fabricated readiness or premature task closure. Reviewer owns configured Pass→implementation handoff; informational Pass must not cause SD duplicate dispatch.

## Routing
Fresh get_handoff_rules selects only **/software_engineering_team/architecture_reviewer**: Architecture Design Complete, Large/High, R3 and supplement approved. Focused SR004 delta review, then reviewer-owned configured implementation handoff. Raw rules/decision in evidence/release-first/sr004/routing.json. No API/Implementation/PM/Delivery duplicate dispatch. Stop after successful send.
