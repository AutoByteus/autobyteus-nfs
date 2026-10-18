# Implementation Revision Record — nfs-first-release

Current code and implementation-handoff.md are authoritative; this record locates
implementation rounds, not independent acceptance. Prior extraction/filesystem
records do not belong to this new Task.

## Revision Index

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-001 | Architecture Reviewer / design-review-report.md / ARCH-REV-001 | N/A | Initial Baseline | R2/SR002, SR003, ARCH-REV-001; CRR/API/DR N/A | Implementation Complete; local checks passed; source review required |

## Revision Entries

### IR-001 — Identity-bound candidate and normal-release publication

- Trigger: original ARCH-REV-001 Pass resumed after poweroff; not a duplicate round.
- Task: autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
- Prior authoritative result: **N/A** (initial implementation baseline).
- Current result: **Implementation Complete**, Large/High confirmed; independent
  source review next. No actual hosted/qualified/signed/published result claimed.
- Related solution: R2/SR002 Approved, SR003 Ready. Architecture: ARCH-REV-001.
  Code/API/Delivery revisions and triggering findings: **N/A** for this Task.
- Input review commit2051fd9559f4f4fa7beae68723429f8199b50004; source commit
  **886b55e1cf88f3f696334bd5e7b8c374946a594d** on codex/nfs-first-release.
- Baseline reason: implement BEH001–006 / REQ001–010 / AC001–008's release-control
  paths without pretending that implementation-local tests satisfy actual release
  acceptance. Default qualification remains empty.
- Delta: manual candidate/fresh/resume workflow; exact source/run/attempt/artifact,
  two-arch engine and complete OCI identities; structured mode/physical/user evidence
  validator; isolated signing with Accepted gate; retained final payload; annotated
  exact tag/draft/non-clobber/digest-preserving/public-download reconciliation;
  bounded installer manifest/checksum integrity; normal-version independent docs.
- Main areas: .github/workflows/release-nfs.yml; packaging/release.py,
  release_support/{identity,candidate,qualification,payload,publication}.py,
  sign-macos.sh; scripts/public/nfs/install.sh; scripts/tests/test_nfs_*.py;
  root/packaging release/testing/README documentation. Go runtime, engine recipes,
  pins, licensing and ordinary CI are byte-preserved.
- Local validation: final independent Mac/Linux arm64 native race7packages,
  vet/build/version; Python38 (Mac37executed+1skip; Linux35+3); four compile targets;
  workflow/Bash/shellcheck; expected empty-lock refusal; real nonroot skopeo on
  synthetic OCI; six detected mutations; scope/hash/import/size audit.
  implementation-evidence/ir-001/checks-and-limits.md owns detailed attribution.
- Local corrections: protected-source and host-bridged-lock harness placement;
  skopeo rootless archive-reader issue corrected using verified unchanged bytes in
  an owned layout. No runtime guard or design-policy change. All attempts retained.
- Next route: configured Large/High independent Code Review, selected by fresh
  rules in implementation-evidence/ir-001/routing.json before handoff.
- Remaining risks: actual hosted four-target candidate, physical/current-user
  qualification, provisioned credential validation/Accepted notarization, current
  main finalization, registry visibility/recovery, public downloads/install/signature
  and actual first normal v0.1.0 release remain API/Delivery responsibilities.
  No push/tag/release/deployment/TaskDone/user verification or terminal claim.

## Revision Index Addition

| Revision ID | Triggering Role / Report / Round | Finding IDs | Classification | Related Revision IDs | Result |
| --- | --- | --- | --- | --- | --- |
| IR-002 | Code Reviewer / code-review-report.md / CRR002 | CR-001 = API R03-F001 | Local Fix | R2/SR002, SR003, ARCH001, CRR001–002, API001, DR001 staging context | Correction complete; local checks pass; targeted source re-review required |

### IR-002 — Nonempty native metadata argv under supported Mac Bash

- Trigger: CRR002 failure-origin review ca048be893516d79bc1ea895b929af17580e25dd,
  confirming actual candidate39111348848/attempt1 fails both Mac jobs before
  metadata/native tests. CR-001 = API R03-F001; earlier local/source review gap.
- Classification: **Local Fix**, existing **Large/High** unchanged. No requirement
  or design change; R2/SR002 Approved / SR003 Ready / ARCH001 retained.
- Prior authoritative implementation: IR001 source886b55e; historical CRR001
  sourcePass100. Current review is CRR002 Fail and API001 Fail62.86%; those verdicts
  remain owned by those specialists, not silently replaced by these local results.
- Current implementation result: **Local Fix Complete / ready for targeted source
  re-review**, source8436d0cf6048cd3b4cadbf28815e3d9f82ba6b34. Related DR001 only
  staged reviewed branch518f4b51 for candidate execution, not finalization or release.
- Approved basis: SCN001/BEH001/REQ001–002/AC001 and dependent AC007; fresh qualified
  invocation preserves BEH002/003. No runtime/storage/signing policy deviation.
- Delta: `.github/workflows/release-nfs.yml` native metadata array now begins with
  all mandatory arguments, then appends exact fresh flags; quoted expansion is
  always nonempty under Bash3.2 nounset. No masking or shell/target replacement.
- Durable test: `scripts/tests/test_nfs_release_workflow.py` executes actual strict
  prefix/JSON pipeline under /bin/bash with inert release-command boundary; exact
  argv candidate/fresh, metadata-error propagation, missing input and pipefail.
  TESTING.md records this new scope and limitations.
- Validation: original workflow fails new regression (7tests,5assertion failures),
  corrected7pass; independent full41tests/40executed+1child skip; actionlint,
  prefix syntax/shellcheck, empty-lock refusal and three guard mutations pass their
  expected outcomes. Local shell3.2.57 arm64; TARGET strings are not amd64 execution.
- Preservation: other116/119 source inputs, all eight Delivery untracked files and
  earlier history unchanged. Owned scratch removed; no new live/remote resources.
- Next: fresh Large/High Local Fix source-review rule (ir-002/routing.json), then
  API-owned NEW current hosted candidate/full aggregation. Workflow source hash
  changed; do not qualify or relabel failed fragments. Current empty-lock hash
  26af7e5bcab00ae22d4bdebe1820c6d38b0dc51a44f1b834036334ea79528298.
- Remaining: physical/genuine-user/signing/current-main/publication/download gates;
  six secrets already provisioned, not reprovisioned or proven. No target merge,
  push, publication, TaskDone/user verification/Terminal claim. Detailed commands,
  raw results and limits: implementation-evidence/ir-002/checks-and-limits.md.
