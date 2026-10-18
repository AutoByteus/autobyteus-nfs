# Implementation Handoff — nfs-first-release

## Upstream Artifact Package

Task **autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5**,
Project project_6416db5b-926a-4865-8705-d8ebb2425780. Worktree
`/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release`, branch
`codex/nfs-first-release`, target `origin/main`. Canonical ticket
`tickets/in-progress/nfs-first-release/`. Personal execution, no delegation.

- Requirements **R3/SR004 Approved**, requirements-doc.md and approval-record-sr004.md.
  User explicitly requests official signed normal v0.1.0 first, then tests/fixes.
- Design **SR004 Ready**: design-spec.md / solution-design-handoff.md. Investigation
  investigation-notes.md E19–22 and solution-revision-record.md SR004.
- Independent architecture review **ARCH-REV-002 Pass**: design-review-report.md /
  architecture-review-revision-record.md; intake e08e078a3303c1ef073c45c9e0b5a044e5dd898c,
  SD basis bc1f1bbb13bb35180625b71ad12117452e79780c.
- Supplement postpublication-testing-plan.md; Delivery's DR003 exact user direction
  remains untracked and untouched. All16 Delivery-owned files are excluded from
  implementation commits. Six signing entries already provisioned; no new request.
- Trigger **approved Behavior Change**, not another CRR002 Local Fix. Historical
  IR002/CRR003 Pass covered R2 only. API002 Blocked73.57 and its complete old-source
  candidate are historical, not acceptance for this delta. Related DR003 is
  sequencing/context only; no Delivery outcome overwritten.
- Remote target last reported7e375984be2bea7a4d536e43cc59d6bc2b116870; not fetched,
  merged or pushed by this round. Delivery must refresh current main later.

## Current Implementation Summary

**IR-003 Implementation Complete / ready for independent Code Review.**
Source **3d2710b30ec1a8106faeb2f7c4f2e70183a25cd3**. Cycle Rework; cumulative
implementation-revision-record.md preserves IR001/IR002 byte prefix. Related
SR004/ARCH002; current-delta CRR/API result **N/A — not executed yet**; prior
CRR003/API002/DR003 retained as attributed context. Triggering finding ID N/A.

One release-first readiness owner now replaces qualification across metadata,
preflight, payload and publication/resume. Native distribution schema2 separates
releaseTargets from explicit deferred fieldValidation. Current native/build,
release-control/source review and genuine release-first authority are required;
physical/shared-filesystem/user tests are deferred, not falsely passed or demanded
as publication/closure prerequisites. Actual readiness evidence remains Delivery's
responsibility. Default lock is engine=null, releaseReadiness=null.

Retained pipeline: manual build-only candidate → audited readiness → fresh final
metadata and both Mac signing/Accepted notarization → retained complete payload →
exact annotation-bound tag/draft/missing byte-equal assets → exact OCI promotion +
anonymous access → normal release/public download checks. No unsigned fallback,
clobber, stale candidate, bypass flag, new framework or live-host behavior change.

Current source hash with null engine/readiness:
`d75c50c83a5848d45209e85511f271f36d5d99362fd87f41b8e24263203591ac`.
Real measured engine changes the real candidate hash. Engine manifest writer/docs
changed, so recipe identity also changes normally; pins/patch unchanged. Old API002
candidate remains untouched and stale, not reused/relabelled for this source.

## Routing Classification

- **Large / High — Confirmed** against SR004 Task Size And Architectural Risk.
  Cross-language distribution schema/authorization/signing/immutable-publication
  contract remains material despite bounded delta. No downgrade from local Pass.
- Selected route **Code Review**, fresh rule saved ir-003/routing.json at handoff.
- Direct-route lightweight review N/A; implementation self-check completed, not a
  substitute for independent source review. New Design Impact/Requirement Gap None.

## Reviewed Behavior Implementation Trace

| Behavior / coverage | Actual path / outcome |
| --- | --- |
| BEH001 / SCN001 / AC001 | Existing candidate.py verifies complete engine/OCI/native identities; schema2 empty releaseTargets in candidate metadata. Workflow keeps nonempty Bash3.2 argv fix, four native runners, build-only default and cancellation guards. NEW hosted candidate required. |
| BEH002 / SCN002/005 / AC002/003/006 | readiness.py exact shape, stable hashed refs, current candidate/source/engine/OCI/run/review, R3 authority, passed native/releaseControls, exact deferred statuses and nonempty plan/notes. release.py/publication.py/payload.py all consume it; lock/engine-reset clean-cut. Signing implementation unchanged. |
| BEH003 / SCN003/006 / AC004/006 | Payload provenance schema2 binds releaseReadiness and fieldValidation; deterministic mandatory disclosure appended to reviewed prose and rechecked on verify/resume. Existing annotation/same-byte non-clobber/digest-preserving/public-effect ordering retained. |
| BEH004 / SCN004/005 / AC005/007 | setup.Release named FieldValidation + schema2; VerifyRelease strict local unknown/duplicate/trailing/schema/status/target/equality admission; dispatcher stderr notice only after success; version stdout unchanged. Installer verify still before writes; language now versioned release. |
| BEH005 / SCN002/004/007 / AC005/008 | config.Decode additive host-state policy and all backend/platform/config/docker/service safety owners unchanged. Release metadata decoding is local only. Go tests prove preservation at fixture boundaries, no live NFS/state action. |
| BEH006 / SCN007/008 / AC007/008 | Root DESIGN/README/RELEASE/TESTING plus package/engine guides align release-first/deferred claims; public notes/provenance cannot hide them. Existing approved plan custody Delivery→terminalSD→requestingPM remains, no premature handoff/task invention. |

Scope Guardrail respected **Yes**, UC001–005 only. No old filesystem/editor/provider
campaign, dashboard/app/Guide change, paid infrastructure or credential re-export.

## Key Files / Ownership

- packaging/release_support/readiness.py replaces qualification.py (deleted);
  identity.py only adds named deferred status constant. No dual record/flag path.
- release.py uses --release; candidate.py generates schema2; payload.py owns
  disclosure/provenance integrity; publication.py uses readiness sourceHash.
- packaging/release-lock.json exact new shape; engine/manifest.py validates current
  shape and clears readiness without old fields on measured-engine write.
- internal/setup/service.go typed metadata; cli/verify-release.go release-only
  strict decoder, cli/run.go notice; noninstallable tracked development stub.
- Durable tests: release_admission_test.go; existing CLI/engine equality tests;
  release records/publication/workflow, engine reset, installer/source/hash suites.
  Python fixtures are synthetic and cannot serve as real readiness evidence.

## Design Health / Legacy / Transition Check

Behavior Change; reviewed boundary/claim coupling and bounded refactor confirmed.
No challenge to SR004 or new fallback needed. One readiness authority, tight named
Go validation values; no overlapping qualified/userVerified fields, --qualified
alias, topology/user-pass code or old module retained. Dead touched qualification
constants/loops removed; no unrelated dead-code work found. Shared guidance applied.
All changed implementation files below500 effective lines and changed-line deltas
below220 (source-audit.json); tests excluded from that hard size limit.

Transition **Discard or Rebuild**: release control and generated distribution
metadata/candidates only. Empty lock replaced, current schema rebuilt; legacy
claims refuse. No published-client compatibility obligation or installed-state
migration. Host records **Not Affected**; external identities/history **Directly
Usable — No Migration**, preserved. No deviation from approved transition.

## Local Checks / Environment / Limits

Details and raw-command paths in implementation-evidence/ir-003/checks-and-limits.md.
- Independent source copy, private HOME/TMPDIR/caches. Native macOS26.5.2 arm64
  Go1.27.2 seven-package race/vet/build/version pass, focused admission rerun pass.
- Owned Ubuntu24.04 arm64 container guest filesystem: final seven-package
  race/vet/build/version pass, Python45 collected42 executed3 container/child skips.
  No host socket/privileged mode, live mounts or independent-host qualification.
- Mac final Python45 collected44 executed1 Go-child skip (parent covers child).
  `/usr/bin/python3`3.9.6 suite; Go-child PATH Python3.14.2. Actual Bash3.2.57 shell
  regression passes; actionlint/Bash syntax/shellcheck pass; empty readiness refuses.
- Four-target compilation passes, **not** four-native execution. Eight bounded
  invariant mutations detected. Current payload disclosure test rehashes tampered
  notes/provenance to reach semantic guards rather than only inventory checks.
- Three final test-only enhancements then final45 Mac/Linux suites; last fetch
  docstring wording correction then current45 Mac suite/hash rerun. No executable
  code changed after native checks; precise attribution in final-comment-delta.json.
- No failed product/test attempt this round; intentionally failing mutants retained.
  Earlier failed evidence remains untouched. Raw apt progress whitespace excepted.
- Cleanup recorded ir-003/cleanup.json. Source/license/pins and16 Delivery files
  preservation audit; historical candidate path never altered. No binaries/assets
  committed. No new API score, physical/user claim or release acceptance inferred.

Frontend rendered-result **Not Applicable**: CLI/packaging, no rendered interface.
CLI interaction (stderr notice/exact version) exercised without live setup.

## Downstream Work / Remaining Risks

1. Independent source review of IR003 against SR004; current code/handoff authoritative,
   history is an index only. Preserve prior source/API outcomes as exact-input history.
2. API updates current ledger for R3 and executes changed release/admission cases plus
   a **NEW complete current-source four-native hosted candidate**. Prior run39113335636/1,
   artifact12131531399 and `/Users/normy/nfs-first-candidate-api002-n940gd8s/candidate`
   remain historical. No old candidate edit or failed-fragment aggregation.
3. Delivery prepares genuine archive-stable readiness/approval/check/review/plan/notes
   under packaging/releases/v0.1.0 after that evidence; parser doesn't establish truth.
   Refresh/integrate main under repository policy; preserve exact source/engine/OCI.
4. Both Mac Developer ID signatures + Accepted notarization, retained final payload,
   authorized normal v0.1.0 publication, anonymous public bytes/OCI and owned-HOME
   version/signature checks remain mandatory. Six secrets provisioned, not validated
   by this implementation; no repeat provisioning absent real validation failure.
5. Field/physical/shared-filesystem/user testing **Deferred, not passed**, not a release
   or closure hold. Delivery binds actual identities and transfers approved plan via
   terminal SD to requesting PM. No new questionnaire, Task or dispatch by implementation.

No source push/main merge, signing, publication/tag/release/deployment, user
verification, TaskDone or Terminal claimed. Actual release still required by task.
