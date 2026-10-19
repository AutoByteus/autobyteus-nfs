# Solution Design Handoff — SR005 immutable signed-publication recovery

## Result and requested action
**Architecture Design Complete / R3 Approved unchanged / SR005 Ready / Large / High.**
Review the narrow corrected-executor/source and draft-discovery design before dependent implementation. This is IR008 Design Impact recovery, not new product approval, signing repair, field campaign, Delivery Completed or Terminal. No new version is authorized. Prior ARCH002 Pass covers SR004 only; new review artifact N/A — not yet produced.

Task nfs-first-release / autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5. Original PM request: enable independent NFS automation and actually deliver first signed downloadable normal release. User chose no beta and explicitly instructed official signed v0.1.0 first, tests/fixes afterward. R3/SR004 and approval-record-sr004.md remain authority; existing postpublication-testing-plan.md retains field/user Deferred and named custody. No re-questioning settled release intent.

## Workspace and ownership
- NFS task worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch `codex/nfs-first-release`.
- Canonical ticket `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/done/nfs-first-release`; do not recreate/move the old in-progress path or reopen extraction.
- Intake032c4e50b265f045277241f30b4982449af495c3 (IR008 docs). Last finalized/Delivery-observed main238bdc183e8affac99ffdee9be9cb333b0eb126f. Non-ticket source unchanged from that main. SD made no new remote freshness claim, source/test edit, build/signing/publication or finalization action. Finalization target remains origin/main under RELEASE.md.
- **NFS only. No workspace/shared skill, agent-package, superrepo/app/GitHub-config edits or work on the separately fixed workspace bug.** Do not reprovision secrets, mutate live mounts/exports/data/nodes, or touch PM/unowned files.
- Own five docs are the authority: requirements-doc.md, investigation-notes.md E23–26, design-spec.md, solution-revision-record.md SR005 and this handoff. Other owners' reports/history are retained and linked, not rewritten. Updated handoff-references.md read in full; selected attachments only.

## Established problem, carried success and completed design
Delivery DR013 created annotated v0.1.0 and empty owned draft; publisher then failed because published-by-tag lookup returns None for a draft. IR008 reproduced that actual endpoint mismatch offline and correctly held implementation: the publisher is production-hashed, and the old architecture requires executing source/main, candidate source and immutable payload/tag source to coincide. Blindly fixing code/new candidate cannot satisfy the original tag without breaking immutability.

SR005 fixes the full boundary:
1. **E**, reviewed current main executor, and **P**, immutable original payload source, are explicit. Current verifier code reads a bounded Git-proven P snapshot as data only; full original source/candidate/readiness/engine/OCI/payload/signing proof remains checked. Fresh mode stays strict and all corrected code remains hashed.
2. Delivery later records a finite audited authorization binding original tag/payload/job/draft to **H**, reviewed corrected code; actual E must retain H's exact executable identity, permitted scope and fresh main. Original runtime/installer/engine/signing/lock/readiness remain byte-identical. No manual bypass, old-code execution, record edit, rebind, re-sign or rebuild.
3. Publisher uses bounded unique draft inventory plus direct-ID reconciliation and ID-directed asset upload/readback. Known draft417014769 missing/hidden/ambiguous is a blocker, not permission to recreate it. Read-only prepare never treats absent published results as proof no draft exists.
4. New workflow recover mode skips candidate/native/signing/payload/bind and revalidates all inputs before effects. Read-only inspect-bound permits API to validate actual retained bytes before final executor authorization; it grants no write permission. External execution receipt names both identities; original public assets/body/provenance/checksums stay unchanged.

**Both Mac signing/notarization already succeeded** in39215470944/1 at238: DeveloperID/team/runtime/securetimestamp/strictverify and Accepted; ARM52450985-4e16-482e-b22a-d7b15b8791b7, Intel563db88f-7ded-48ba-9d90-bcdbf8705961. DR013 downloaded-binary evidence carries; no repeat successful signing campaign. Old failed/unknown histories remain original. API006/CRR012 exact source scope remains, not acceptance of new SR005 code.

## Immutable inputs to preserve
- P238bdc183e8affac99ffdee9be9cb333b0eb126f; annotated tag objectf4a04fd0c80a6625708ba002b4cef5507a03f514; owned draft417014769, exact body, last observed zero assets.
- Original successful payload job117940491787; artifact12169472209 / run39215470944 / attempt1; wrapper sha256:b552faeaf6de1337ef8cf3056878b9bf0f1822faed5645033a8d5145fd1d0336, expires2027-01-17T07:21:36Z; publication.json SHA3b0cbedd15782871e0c88c51b6847abcf276e7db00aab6f10c4dd387b4133dc8.
- Original source hash3e1af43a4191c17ddf8a5d6043a1e374c5cd0101f2ac18dd6ee9fee79c131086; candidate run39213489075/1, artifact12168544425. Full original candidate/engine/OCI refs in unchanged packaging/releases/v0.1.0/readiness.json and investigation E24.
- Retained payload `/Users/normy/nfs-first-final-dr013-gmvotux9/payload`; retained candidate `/Users/normy/nfs-first-candidate-api006-a8aune30/candidate`. Do not delete/alter. No new remote freshness claim by SD.

## Review focus and next outputs
Evaluate D2–D5 and DS5 against unchanged SCN006/REQ006/AC004: full context propagation, authoritative fixed repair scope and H/E admission, old-job/retention/ready/signing evidence, fresh-mode nonregression, draft visibility/uniqueness/direct-ID/post-create failures, no-clobber effects and precise receipt. Assess source-context/recovery owner split for proportionate complexity; do not repeat settled business/signing work.

After passing review, use your configured route for implementation. Implementation/source review/API own current code/tests; Delivery owns genuine stable authorization/integration, actual same-payload hosted run/public OCI/download/install/signature checks and cleanup. No product tests or executable acceptance by SD. Historical candidate/failed runs must not be relabelled. Field/user follow-up remains separate, no new PM Task or dispatch.

The requested finished user outcome is still actual release URL/version/four available platforms and exact install/run guidance. It is **not yet delivered**. Remaining execution risks are remote drift/expiry/access and new executor validation, not a missing user product decision. Preserve partial state on failure and report precise blocker.

## Selected supporting references
All relative paths below are within the absolute canonical ticket above:
- approval-record-sr004.md; postpublication-testing-plan.md — unchanged approval/deferral basis.
- design-review-report.md — ARCH002 prior basis only.
- evidence/IMP-08-02-design-impact.md — current implementation diagnosis, links offline probes.
- delivery-evidence/dr-013/failure-assessment.json and draft-reconciliation-observation.json — actual partial state/signing carry.
Other source is in the worktree; implementation-handoff.md/history and API execution report Cases/progress/coverage links lead to any further evidence. No need to forward historical source files or entire evidence folders.

## Routing
Fresh get_handoff_rules selects exactly **/software_engineering_team/architecture_reviewer**: Architecture Design Complete with Large or High and approved aligned package. Low-risk direct implementation and Delivery receipt-gap rules do not match. Exact returned rules/selection are in evidence/design-recovery/sr005/routing.json. Send only this review route, then stop; no duplicate Implementation/API/Delivery/PM notification. The authoring commit is supplied in the dispatch message to avoid a self-referential commit record.
