# Solution Design Handoff — extract-autobyteus-nfs

## Result And Requested Next Action
**Architecture Design Complete — SR-002; task_size Large; architectural_risk High.** Requirements R1/SR-001 Approved by Solution Designer within explicit user direction, user informed in conversation. No Needs user decision. Independent review **not yet performed**; implementation/validation/delivery **not yet performed**. Request the configured architecture review of the coherent two-repository extraction, then the normal downstream route. This is new Task fdb2c737, not renewed testing/approval of the completed filesystem/editor Tasks.

## Original Direction / Goal / Boundary
Requester `/project_task_manager`, run project_task_manager_a5f6d9d306e54970bafdad895bdf731d. Task `project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8`, Project AutoByteus NFS `project_6416db5b-926a-4865-8705-d8ebb2425780`. User 2026-10-16 explicitly requires independent Go NFS repository at `/Users/normy/autobyteus_org/autobyteus-nfs`, origin `https://github.com/AutoByteus/autobyteus-nfs.git`, one maintained home with source/tests/build/setup/docs and intact AutoByteus integration. Remove superseded embedded source, preserve license/attribution/provenance and supported behavior. Engineering owns exact boundaries.
No new filesystem capabilities, backends, generic cleanup, editor/updater, deferred outage/Mac-hosting/auth/encryption/notifications/UNFS work, live storage/node/config mutation or deployment. No release/version/tag. Prior Task0793009f and editor a4f90984 stay DONE; finalized archives read-only. Preserve all other owners' dirty work/PM metadata/assets.

## Authoritative Package (one canonical ticket)
`/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs/tickets/in-progress/extract-autobyteus-nfs`
- requirements-doc.md — approved R1 intended behavior, SCN/UC/BEH-001–004, REQ/AC-001–008.
- investigation-notes.md — current evidence E01–E11, architecture A01–A05, authorities, bootstrap, historical supplement inventory and limits.
- design-spec.md — SR-002 target owners/paths/removals, qualification boundary, verification and finalization sequencing.
- solution-revision-record.md — SR-001 requirements approval then SR-002 architecture; no invented prior review.
- This handoff — full next-owner context and route.
No new behavior-defining supplements or Product artifacts. New review/implementation/test reports: N/A — not applicable yet. Relevant prior proof remains linked in investigation; no forwarding manifest needed.

## Workspaces, Provenance And Ownership
1. Source task worktree `/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs`, branch `codex/extract-autobyteus-nfs`, clean production tree at freshly fetched origin/personal **3712cd9bf0db998501d162db7f8655f169e3def6**. Source origin `git@github.com-ryan:AutoByteus/autobyteus-workspace.git`. Target origin/personal, --no-ff per source RELEASE; never finalize from canonical superrepo checkout (unrelated work exists).
2. Destination task worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`, branch `codex/extract-autobyteus-nfs`, initially orphan/unborn base. Only this Task's five design documents authored so far. Target origin/main under new standalone policy. See commit identity in handoff message/Git; no self-referential hash in this file.
3. User canonical destination `/Users/normy/autobyteus_org/autobyteus-nfs`: checked twice, main unborn, remote no refs, only .git and PM untracked task-plans/. Do not overwrite new owner changes. Final initial checkout population after validated remote main must be non-force/preserve PM files. Task authoring/finalization occurs in isolated worktrees.
4. Old source merge f69ee786260715e0ec461cc4d7d49a8df7409be8 and receipt88c865d4129efd23bd23f009d80dc7aa3db6e405 are provenance, not the current base. Relevant NFS files have no delta since that receipt, but current base includes completed editor work. Old retained checkout `/Users/normy/autobyteus_org/autobyteus-worktrees/shared-network-workspaces` stays read-only, including ignored candidate/dist assets.

## Design In Brief
- Lift tracked embedded Go module to N root; imports become github.com/AutoByteus/autobyteus-nfs, existing runtime owners/fields/OS paths/semantics unchanged.
- Move service installer/packaging/three Python suites and service half of mixed suite; app launcher controls remain in source suite. Fix Go-to-Python fixture root. Never copy app runtime/launcher to make N tests work.
- New N policies/CI/docs/provenance; preserve exact LICENSE/CLA/source pins and applicable terms. Build identity covers only owned N inputs plus declared integration contract. Qualification lock remains empty; historic bounded proof is not new qualification.
- N release workflow becomes manual-only, no desktop version assertion, no automatic publish on main/tag. Keep exact-engine candidate reuse, signing, current-source/physical/user gates and existing-release requirement. No release action now.
- App consumes installed service as before. Preserve in-service app-node probe strings to installed /app/... binding module. Replace TS sibling fixture with exact pinned local consumer snapshot and repository/commit/path/digest provenance; cross-repo equality evidence at integration, offline ordinary tests.
- Remove embedded maintained tree/workflow/installer/service tests and stale active docs claims. Do not rewrite historical tickets.
- Validate paired candidates, finalize N main then source personal pinned to N producer; handle ref races/partial completion honestly, no force. Cleanup only owned work after durable receipts.

## Evidence / Limits / Risks
Investigation only, no fresh runtime/build/test result claimed. Current source and policies inspected, empty destination rechecked, workspaces isolated; source task tree remains untouched. Historical one-VM/shared-kernel command-only delivery remains bounded. New extraction checks must run on standalone archive/clone, not hide sibling dependencies; Go/Python/packaging/refusal/consumer contract coverage, unchanged-runtime diff, license/provenance and paired Git receipts required. Existing retained arm64 engine input can be copied read-only into owned scratch and freshly verified for packaging checks; missing amd64/signing/physical execution is not Pass. No user/live VM/UI/editor acceptance gate added.
Risks: stale path/version/source-hash assumptions; accidental qualification weakening; optional installed app integration mistaken for build dependency; two-repo race/partial finalization. No unresolved design/scope blocker.

## Expected Receiver Output
Independent technical design assessment against R1 and SR-002; preserve scope/classification, route actionable design findings here or pass under your rules to implementation. Not a request for another requirements questionnaire, old application campaign, source implementation by reviewer or deployment. Downstream package lives in N, with both worktree identities included at every handoff.

## Applied Route
Fresh rules returned after all five documents were persisted. The most-specific and only matching condition is Architecture Design Complete with task_size=Large or architectural_risk=High and approved aligned requirements. Selected exact recipient: `/software_engineering_team/architecture_reviewer`. Direct implementation and delivery-receipt-gap conditions do not match. Send these five owned documents; other source/evidence is located by investigation links, not forwarded en masse. No delegation or duplicate PM/implementation handoff.
