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
