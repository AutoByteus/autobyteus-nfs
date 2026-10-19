# Implementation Handoff — nfs-first-release

## Current result

**IR-008 — Design Impact: safe repair of an already-bound publication requires a
completed executor-versus-payload recovery contract. Dependent implementation held.**
The draft-discovery defect is reproduced, not fixed. No production/durable-test
change this round; current source remains authoritative and unchanged.

Task autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
Worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`,
branch `codex/nfs-first-release`; canonical archive `tickets/done/nfs-first-release`.
Intake/source checkpoint **a7eb8a819c604358a5b01bd66b1fe1ffda313b19**;
finalized main **238bdc183e8affac99ffdee9be9cb333b0eb126f**. No push or finalization
replay. Own evidence/docs commit supplied in handoff.

## Authority / trigger / classification

- R3/SR004 Approved/Ready, ARCH-REV-002; requirements-doc.md,
  approval-record-sr004.md, design-spec.md, investigation-notes.md,
  solution-revision-record.md, design-review-report.md and architecture-review-
  revision-record.md remain authority. postpublication-testing-plan.md keeps
  field/user testing Deferred, not release/closure prerequisites.
- Trigger Delivery **DR013 Blocked / publisher Local Fix** in
  release-deployment-report.md / delivery-revision-record.md;
  delivery-evidence/dr-013/failure-assessment.json and
  draft-reconciliation-observation.json establish the actual partial state.
- Prior implementation **IR007** has now passed actual BOTH-Mac hosted signing and
  Accepted notarization, as evidenced by Delivery DR013. API006/CRR012 carry their
  exact-input scopes. No signing/credentials repair is requested or performed.
  Old DR005/009/011 remain historical failures; deleted raw causes not recovered.
- **Large / High / Reviewed confirmed.** New issue is a technical publication
  trust/identity boundary gap, not changed user intent or a new version/field
  approval request. Current IR008 CRR/API: N/A (investigation/design return).
- Most-specific route: **Solution Designer — Design Impact**, not completed Local
  Fix/source review. No duplicate Delivery/API/reviewer/PM dispatch. No delegation.

## Demonstrated gap / requested next work

`publication.release()` uses the published-by-tag endpoint. After creating an
owned draft, `reconcile_release()` gets None and dereferences it. Offline replay
of DR013's exact recorded draft with by-tag404 and list/ID availability reproduces
that TypeError and proves no list/ID lookup occurs. Current unit coverage mocks
release() itself, concealing the endpoint-semantic mismatch. Bounded exact-tag
inventory/direct-ID reconciliation with conflict/ambiguity refusal is needed.

But that repair changes production-hashed publisher bytes. Current checks bind
executing checkout, candidate source hash, payload source commit, annotated tag
target and current main together. Corrected code cannot consume the old candidate
under that contract; new source cannot match the immutable tag/payload. Checking
out old source merely restores the bug. Removing hash inputs, patching an old
checkout in place, changing records, manual uploads or rebuilding/re-signing the
same version would bypass existing guarantees.

**Return a narrow reviewed recovery design** defining the authority/identity and
scope of a corrected executor separately from the immutable bound payload source,
and how both are validated/freshness-checked before effects. Preserve the exact
old candidate/engine/OCI, original successful payload artifact/attempt, signatures,
notes/provenance and checksums; keep fresh-mode strict equality and all conflict,
retention, job-success, current-main authorization and no-clobber checks. Specify
bounded draft visibility/discovery/uniqueness/post-create behavior in the existing
publication owner. No arbitrary bypass, new release authorization or user prompt.
Details and complete constraint trace: **evidence/IMP-08-02-design-impact.md**.

## Behavior and health trace

| Basis / path | Current result |
| --- | --- |
| BEH001/002, AC001/002/006: candidate/readiness/source identity | Guards preserved. Offline source-hash sensitivity shows any publisher edit invalidates the original current-source comparison. No new candidate built or old one relabelled. |
| BEH003, AC003/004/006: signing → retained payload → publication | BOTH-Mac success is attributed to DR013, not rerun. Publisher draft discovery fails; DS5 retry assumes unchanged executing main. New-executor tag/payload/main refusals reproduced. |
| BEH004/005, AC005/007/008: installer/host contracts | Unchanged; no runtime, host, storage, app or credential mutation. |
| BEH006: truthful release-first/deferral and recovery instructions | Preserved. Same-byte recovery remains intended; technical authority needed to repair its executor safely. No TaskDone/Terminal/publication claim. |

Scope Guardrail retained. Original reuse-of-immutable-retry assessment is
insufficient for a code defect AFTER a tag/draft exists, hence Design Impact
rather than an undocumented exception. No implementation refactor/bypass chosen.
Frontend **N/A**. Installed persisted data/migration **Not Affected**; immutable
publication records are preserved. No compatibility code, dead production code
or source-size growth introduced (no production delta). Probe imports cleaned.

## Checks Run / evidence

| Check | Commit / environment | Command or observation / code exercised | Result / what to look for |
| --- | --- | --- | --- |
| IMP-08-01 | a7eb8a8 / Darwin arm64, Python3.9.6, offline doubles/owned fixture | `PYTHONDONTWRITEBYTECODE=1 python3 tickets/done/nfs-first-release/evidence/IMP-08-01-recovery-probe.py` | JSON: exact TypeError; `listOrIdRequested: false`; mocked create1, realEffectsfalse. This confirms the defect, NOT product Pass. |
| IMP-08-01 controls | same | Same probe: disposable hash marker; real tag_binding/payload.verify/fresh_main with controlled identity inputs | `newExecutorTagRefusal: Published tag points to different source`; `newExecutorPayloadRefusal: Publication inputs differ`; `advancedMainRefusal: Remote main advanced; reintegrate before publication`. `allExpectedObservationsConfirmed: true`. |
| IMP-08-02 | same source / read-only | Source and design/guide/workflow trace; official GitHub releases documentation; incoming DR013 saved endpoint observations | design-impact.md separates actual remote evidence (Delivery) from offline reproduction and lists each current invariant. |
| IMP-08-03 | a7eb8a8 → own evidence/docs / local inspection | Own scope/history/import/ancestry audit | audit.json: production unchanged, prior IR prefix and finalized238 ancestry preserved; fixture scratch absent. |

Probe is ticket evidence, not a durable release executor/test replacement. It was
rerun unchanged semantically after removing unused probe imports/dead assignment;
no unexpected failure or production patch. All command effects are doubled;
source-hash mutation occurs only in a removed disposable copy. No actual gh API,
signing/keychain/Apple, candidate/engine/native/API rerun or remote write. Full
release suite is not rerun because no release code/tests changed. No retained
payload/candidate bytes copied or altered; own fixture scratch removed.

## Immutable partial state / custody

Source hash unchanged **3e1af43a4191c17ddf8a5d6043a1e374c5cd0101f2ac18dd6ee9fee79c131086**.
Original run39215470944/1 main238: tag objectf4a04fd0c80a6625708ba002b4cef5507a03f514,
owned draft417014769 empty, payload job117940491787 succeeded. Annotation binds
artifact12169472209, wrapperSHA b552faeaf6de1337ef8cf3056878b9bf0f1822faed5645033a8d5145fd1d0336,
publication.json SHA3b0cbedd15782871e0c88c51b6847abcf276e7db00aab6f10c4dd387b4133dc8,
expiry2027-01-17T07:21:36Z. These are Delivery's last actual observations, not a new
remote freshness claim. No moving/deleting tag/draft, new signatures/repack, assets
upload, main reset, manual publish or next-version authorization.

Preserve `/Users/normy/nfs-first-final-dr013-gmvotux9/payload`, candidate
`/Users/normy/nfs-first-candidate-api006-a8aune30/candidate`, all older candidates
and local diagnostic. Main238/72/f830/768 history and PM/other owners untouched.
Delivery retains actual same-payload publication, public OCI/download/install/
notice/signature verification ownership after valid recovery. Field/user Deferred;
plan custody Delivery → terminal Solution Designer → requesting PM after completion.
