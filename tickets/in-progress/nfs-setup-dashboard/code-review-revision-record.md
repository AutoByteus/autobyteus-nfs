# Code Review Revision Record — nfs-setup-dashboard

## Revision Index

| Revision | Canonical report | Entry / trigger | Prior result | Current result | Findings |
|---|---|---|---|---|---|
| CRR-001 | code-review-report.md | Implementation Review / IR-001 initial completed Large/High package | N/A | Pass100/100 | None |

## CRR-001 — Embedded dashboard and complete shared admin owner

- Date: 2026-10-24. Round1, **Full Review**. Initial baseline, no prior source/API verdict inferred.
- Canonical report: `code-review-report.md`. Trigger: Implementation Engineer's `implementation-handoff.md`, IR-001.
- Related authorities: R1/SR-001 Approved; SR-002–003 solution history, current SR-003; ARCH-REV-002 Pass (ARCH-REV-001/ARCH-F001 resolved); IR-001. API-REV / DR: **N/A**.
- Source base52c17fb5480d23b89752a8ae201419e356b4c3fc; production5f8cabf8ee31318a38aa9c0ed94e9c6960b9c409; final source/tests2445aabf61126b1bb64b05b5f925b140c67917b8; intakee5662dd1333192c66cf29bf27e6f82ccb14c2efd. All165 non-ticket inputs audited; no post-check non-ticket delta.
- Reviewed full39-path change and affected existing authority callers: nonroot HTTP, exact local authorization/private helper, strict typed IPC, retained plan/global lock, metadata versus readiness, safe stop/drain, preserved CLI and complete DS6 serial service lifecycle. Inspected durable tests, reused valid implementation checks and retained rendered images; no product test rerun or native/resource action by reviewer.
- Current result **Pass100/100**, Large/High confirmed. All24 structural checks pass. Max236nonempty source; operations240added pressure is cohesive, no split required. No source findings, unsupported machinery or new follow-up.
- Behavior basis BEH001–007/SCN001–010 confirmed against R1/SR003. No new/reclassified material premise. Candidate records CG001–007 in report explain accepted mechanisms and rejected non-findings.

### Prior Finding Resolution

None — initial source review. Upstream ARCH-F001 is verified implemented through admin.Supervise/reconcileOnce and removal of old callback owner; it is not a prior code-review finding.

- New/remaining finding IDs: None. Classification N/A; prior score N/A.
- Recommended recipient: API/E2E Engineer via fresh source-review Pass rule; no duplicate implementation/Designer/Delivery outcome dispatch under the team's single-recipient instruction.
- Limits: phase2/earlier Linux native evidence remains attributed; current Mac/Linux-client and test-only Linux cleanup follow-on separate. Browser root/clipboard doubles and native HTTP/TTY proof are not one live browser-to-mount test. No AMD64 runtime, physical/field/user/release claim. API owns acceptance; Delivery owns fresh source integration/AC008. No product/source change, push, merge, release, TaskDone or user verification.

## CRR-002 — Chooser input overwrite, focused failure origin

| Revision | Canonical report | Entry / trigger | Prior result | Current result | Findings |
|---|---|---|---|---|---|
| CRR-002 | code-review-report.md | API/E2E Failure-Origin Review / API-REV-001 API07 | CRR001 sourcePass100 historical | Fail; implementation Local Fix | CR-001 = API-F001 |

- Date: 2026-10-24. Round2; scope N/A — focused failure-origin, no full structural/source score rerun and no successful-test review.
- Relevant revisions: R1/SR001 Approved, SR003/ARCH-REV-002 Pass, IR-001, CRR-001, API-REV-001 Fail81.43%; DR N/A. Large/High unchanged.
- Input042821aa5e26dec38a6a310fabdf34eb7574612c; source/tests2445aabf and production5f8cabf unchanged. All non-ticket differences since reviewed source empty. No product or durable-test edit by API/reviewer.
- Confirmed Medium CR-001: normal SCN002 folder selection/REQ009/AC007 path typing is overwritten by forms.js:28 on async initial completion at38. Real API07 expected /home/admin/api-dashboard but observed /home/adminadmin/api-dashboard; same settled keyboard sequence passed. Source introduced by this ticket, not an unrelated editor/filesystem issue.
- Candidate CG008 promoted / This ticket. Existing approved behavior is contradicted only at this bounded chooser surface; no new requirement or material ambiguity. No follow-up added.
- Origin established by Read of current source plus API's reproduced/measured browser, actual HTTP/directory listing and settled control. Screenshot inspected. Reviewer performed no product rerun/instrumentation/resource action.
- Earlier review gap acknowledged: unconditional setter overwriting active input should have been caught; prior browser coverage waited for completion, leaving this normal typing path untested. Correct affected runtime-fidelity rationale, not reclassify storage successes or recompute a whole score.

### Prior Finding Resolution

None — CRR001 had no code findings. CR-001 is new and Open, confirmed against API07/source. Prior full-review report remains in commit d9beb0f796894c37a371217768b9e33afcde315a; prior entry above unchanged.

- Next: implementation's bounded chooser correction plus durable red/green regression, then source re-review and affected API validation. No broad storage campaign absent changed impact, no Designer/approval loop.
- Risks/limits: no directory/storage plan submitted by failure probe; no file data loss or backend/security failure proven. API's scoped storage/lifecycle/client proof and its limits remain unchanged. No release/finalization/TaskDone/user-verification claim.

## CRR-003 — Chooser edit-ownership Local Fix re-review

| Revision | Canonical report | Entry / trigger | Prior result | Current result | Findings |
|---|---|---|---|---|---|
| CRR-003 | code-review-report.md | Implementation Review / IR002 | CRR002 Fail | Pass100/100 | CR-001 source-resolved; API closure pending |

- Date: 2026-10-24. Round3, **Targeted Delta Review**. R1/SR001 Approved, SR003/ARCH-REV-002 Pass, IR002, API-REV-001 Fail81.43; DR N/A. **Large/High unchanged**.
- Intake629f7f008f6ada3f539ca854a1add82ca08f7dbd; source/tests7b0577a4f2637ddf12a74a0156e4243a41a3719c. Four non-ticket paths since CRR002; only production forms.js changes. Since checked source only TESTING instructions changed, not executables/tests.
- Source trace confirms explicit navigation owns path seeding; background render owns listing/results, never active draft. Single eligibility rule prevents unlisted/failed/pending draft from selecting old folder. SCN002/BEH002/REQ009/AC007/DEC004 supported normal workflow unchanged.
- Current all24 structural rows Pass; full10-category score100 with unaffected CRR001 evidence carried. forms.js47→55nonempty,11add/3del; no size pressure, shared interface/schema, privilege/storage/admin/service/CLI delta or extra mechanism.
- Read reused IMP17 original-code red; IMP18 same-regression16/16 green across two engines/two widths (8chooser+8normal); IMP19 race/vet+2embedding/hash checks; IMP20 cleanup. Inspected retained narrow WebKit screenshot. Root/clipboard doubles and held real HTTP response delivery labelled, not a new native run. No reviewer product rerun/resources.

### Prior Finding Resolution

| Finding | Prior | Current | Proof / remaining boundary |
|---|---|---|---|
| CR-001 = API-F001 | Medium implementation Local Fix / Open | Resolved in source review | Old async setter removed; explicit List/Browse/parent/child and matching selection preserved; red/green exercises actual input. API001 remains Fail until affected API validation. |

- New/remaining source findings and follow-ups: None. Earlier review gap remains recorded in CRR002 above, not erased.
- Next: fresh primary source-Pass route to API/E2E only; affected chooser/control validation, preserving unchanged scoped native/storage proofs. No Designer/Delivery/implementation duplicate outcome notification under team's single-recipient rule.
- Source-only NFS; no release, target merge/push/tag, TaskDone/user verification. Reviewer changes documents/evidence only; prior history byte prefix preserved by CRR03 audit.
