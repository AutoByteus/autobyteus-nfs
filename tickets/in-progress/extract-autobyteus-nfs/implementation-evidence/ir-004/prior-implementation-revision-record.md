# Implementation Revision Record

Current code and implementation-handoff.md are authoritative. History begins with the first completed implementation handoff for this extraction Task; no result before IR001 is inferred.

## Revision index
| Revision | Trigger | Findings | Classification | Related revisions | Result |
| --- | --- | --- | --- | --- | --- |
| IR-001 | Architecture Reviewer replacement design-review-report.md | N/A | Initial Baseline | R2/SR003, SR004, ARCH-REV-002; CRR/API-REV/DR N/A | Ready for independent source review; implementation local checks complete |
| IR-002 | Code Reviewer code-review-report.md / CRR-001 | CR-001 | Implementation-owned Local Fix | R2/SR003, SR004, ARCH-REV-002; CRR-001; API-REV/DR N/A | Five-binding cleanup complete; ready for targeted source re-review |
| IR-003 | Delivery Engineer DR-001 / handoff-summary.md | Latest-base Codex test conflict | Implementation-owned Local Fix | R2/SR003, SR004, ARCH-REV-002; CRR002/003; API-REV-001; DR-001 | Integrated candidate checked; ready for targeted source review |

## IR-001 — Independent host NFS and filesystem-only application boundary
- Triggering role/report/round: architecture_reviewer, canonical design-review-report.md, ARCH-REV-002 Pass.
- Triggering findings: N/A. Prior authoritative implementation result: **N/A**.
- Current result: initial implementation complete against replacement R2/SR004; no API/E2E, Delivery, user-verification or release verdict.
- Related solution revisions: SR003/SR004 current; SR001/SR002 historical.
- Architecture review: ARCH-REV-002 current; ARCH-REV-001 historical only.
- Code review / API/E2E / Delivery revisions: N/A for this Task.
- Why recorded: preserves the first complete two-repo implementation baseline after the user's material filesystem-boundary correction. Held N353dd2c/0c9fd27/S390e0c76 and failed preparation are preserved, not reset or mislabeled as a prior Pass.
- Behaviors/requirements: BEH001–006, REQ001–010; implementation supports AC001–006,008–010 locally; Delivery-owned AC007 remains pending.
- Actual delta: root module/service tools/docs/workflow extraction; N host-only CLI/setup/state/Docker engine and locked incompatible active/pending state refusal before binary/resource effects. S ordinary workspace/PTY/run paths, removed descriptor/mount/Git-trust/launcher coupling, uniform exact private configured-skill profiles for supported runtimes, no-binding no-acquisition behavior, dead wrappers/paired fixtures removed. Scope is R2 semantic refactor, not byte-identical relocation.
- Code identities: N83726b27400b405a7a6a79bd962d8e2419daa561; Sd3f7f67015587b4c8aa26824786be807793485d1 (production2448e166). E/change-inventory.json enumerates both.
- Focused validation: independent N Go race/vet, five Python suites, native version/four-target compile, exact retained arm64 input verification/embed compile, packaging/hash/refusal/workflow controls; S build/production typecheck,1158 units+40 activation/PTY units,39 local route/profile and17 native path/run/PTY checks,24 frontend checks,34 executed launcher cases, rendered disabled Guide EN/zh1440/390, source/license/permission audit. Skips and failures retained in E/checks-and-limits.md and E/attempts.md.
- Classification recheck: Large/High confirmed. No demonstrated new design gap. No direct low-risk self-review route.
- Next route: independent Code Review selected by fresh rules; routing receipt stored in E/routing.json before dispatch.
- Remaining limitations: no live NFS/installed migration/physical/platform/provider/hosted-signing qualification, no release, no target finalization. Six AGY-live opt-ins and environmental child/pwsh/port fixture skips explicit. Historical completed Tasks not reopened.

## IR-002 — Bounded touched-file unused import cleanup
- Triggering role/report/round: code_reviewer, canonical code-review-report.md and code-review-revision-record.md, CRR-001 initial Full Review Fail /98.8%, finding CR-001 only.
- Prior implementation result: IR001 Ready for independent source review; subsequent reviewer result Fail for mandatory cleanup, not a runtime/design defect.
- Current result: cleanup and implementation-scoped checks complete; Ready for targeted source re-review. Reviewer/API verdict is not assigned by implementation.
- Related revisions: approved R2/SR003, Ready SR004, ARCH-REV-002 unchanged; CRR-001; API-REV and DR N/A for this Task.
- Reason: satisfy mandatory no-dead-code rule in already-touched files without broadening into unrelated unused-code work.
- Behavior/requirements: BEH006 / REQ010 / AC010 preserved. No intended behavior, schema, lifecycle, profile or runtime API change.
- Actual delta: remove AgentRunConfig and RuntimeAgentRunContext imports in Claude/Codex backend factories, plus local ClaudeSessionEvent import in Claude session manager. Preserve real AgentRunContext and independent public ClaudeSessionEvent re-export. Three files only; 2insertions/7deletions, no test changes.
- Source identities: N83726b27400b405a7a6a79bd962d8e2419daa561 unchanged; Sa2023feff3d498fb6c51cebf1c93360da3679a45 atop reviewed d3f7f67015587b4c8aa26824786be807793485d1. N starting review receipt a77048efc905f1996d6481963625d3940a2c542a.
- Focused validation: TypeScript5.9.3 no-unused audit25 touched production TS files has no diagnostics; documented production typecheck with shared prerequisite builds exit0 in owned current-source copy; identical JavaScript emission in all3 files; public re-export and shrinking file-size assertions; source whitespace/input-integrity checks. Initial audit rootDir and filtered-install setup failures retained and corrected without product/config edits.
- Classification recheck: Large/High unchanged; no Design Impact/Requirement Gap. Frontend loop N/A for import-only delta.
- Evidence: implementation-evidence/ir-002/checks-and-limits.md, checks-result.json, unused-imports.json, delta-audit.json, attempts.md and cleanup.json. IR001 and reviewer N checks are carried/attributed, not rerun or promoted to new runtime proof.
- Route: fresh configured source-review route; no duplicate Designer/API/PM dispatch.
- Limitations: targeted source re-review then proportionate current API validation remain. AC007 remains Delivery-owned. No live app/VM/storage/node/provider campaign, old filesystem/editor work, target merge/push/tag/release/deployment/TaskDone/user verification. Owned scratch removed.

## IR-003 — Latest-base consumer integration recovery
- Trigger: delivery_engineer, DR-001 Blocked / Local Fix; handoff-summary.md, delivery-revision-record.md and delivery-evidence/dr-001/integration-state.json. Finding: one Codex test import conflict; no new numbered CR finding.
- Prior implementation result: IR002 cleanup Ready, then CRR002 source Pass100, API-REV-001 Pass95, CRR003 successful-test Not Applicable. Delivery blocked before paired finalization; those upstream results are retained for their original inputs.
- Current result: integration Local Fix complete, Ready for targeted source review; no independent current API/Delivery verdict assigned.
- Authority/classification: Approved R2/SR003, Ready SR004, ARCH-REV-002; Large/High/Reviewed unchanged. No Design Impact/Requirement Gap/new approval.
- Behavior/requirements: preserve BEH003/006 (ordinary paths/exact private runtime profiles), BEH001/002/005 unchanged N; BEH004/AC007 delivery sequence still pending.
- Actual delta: merge personal2f211340 (165 base-only commits) into S ticket via156ea2dacc0fb4989a6b5d8a7206fa143fde0c54. Resolve conflict by omitting both unused competing imports while retaining upstream current prompts and R2 bootstrap dependencies. Preserve four auto-merged overlaps. Separate8c5c76 removes obsolete Brief guard no-ops;5559abbf removes ignored Codex request fixture input and21 callers; assertions unchanged by those cleanups.
- Current identities: S5559abbf017566f0030d95b023614f7418d3f212; N service83726b27400b405a7a6a79bd962d8e2419daa561 unchanged from intake27db7441523e7b9c1a2ee3263ae83f857ef30d80. N remote has no heads/main; no remote target altered.
- Impact plan before tests: E3/validation-plan.md and integrated-changed-paths.txt. Core/contracts/fixtures changed, so S cases require rerun; independent N proof remains valid. API-owned S04/S05 reruns explicitly downstream per role boundary, not closed by implementation.
- Fresh local checks: prerequisite build/production typecheck;1666 unit Pass with6 gated skips;21 narrow integration,15 core,24 Guide; launcher34 executed/2 environmental skips; localization/web guards. Final fixture-only rerun76 overlap/control checks Pass (repeated, not additive).7318 source/copy input equality, current source/coupling/size audit. No product/test failure; initial audit-script parse/setup error preserved.
- Scope/cleanup: no authored production change beyond upstream integration, no renewed architecture/old VM/editor/provider qualification. Owned scratch removed and no owned active process; D0 unborn/PM board unchanged. N service/licenses/CLA/engine pins/empty qualification/disabled Guide remain.
- Frontend loop: N/A for backend/test reconciliation; prior render proof historical, fresh component checks not browser/desktop proof.
- Remaining: targeted source review, current affected API validation, Delivery docs sync (including obsolete R1 NFS tail in S RELEASE.md), fresh refs and N then S finalization. AC007 not achieved. No target merge/push/tag/release/deploy/TaskDone/user verification.
- Evidence: implementation-evidence/ir-003 (E3): validation-plan.md, checks-result.json, test-counts.json, focused-final-result.json, integration-audit.json, final-input-integrity.json, attempts.md, cleanup.json. Route via fresh most-specific rules.
