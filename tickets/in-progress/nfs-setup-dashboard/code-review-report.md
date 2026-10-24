# Code Review Report — nfs-setup-dashboard

## Latest Authoritative Result

**Fail — CRR-002 / focused API/E2E failure-origin review.** Confirmed
**CR-001 = API-F001**, Medium, **implementation-owned Local Fix**: the new
chooser's asynchronous directory-list completion overwrites an active path edit.
No NFS runtime defect or filesystem-data loss is established.

Task **autobyteus-nfs-2 / project_task_f1264eb8-5a99-4a19-949f-09d141c955a1**.
**Large / High / Reviewed** unchanged. R1/SR001 Approved, SR003/ARCH-REV-002 Pass.
No new approval, architecture campaign or unrelated follow-up is needed.

## Review Round Meta And Scope

- Date: 2026-10-24; round2; scope **N/A — failure-origin only**, not a new full implementation audit or successful-test review.
- Worktree: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, branch `codex/nfs-setup-dashboard`; target `origin/main` untouched.
- Trigger: API/E2E Engineer's **API-REV-001 Fail81.43%**, case **API-07 / API-F001 / REQ-009 / AC-007**.
- Intake `042821aa5e26dec38a6a310fabdf34eb7574612c`; API evidence `c2095979e823dc886be4ebdd3a479d275329db87`.
- Validated product `5f8cabf8ee31318a38aa9c0ed94e9c6960b9c409`; source/tests `2445aabf61126b1bb64b05b5f925b140c67917b8`, identical non-ticket tree at this review. Recorded sourceHash `324bf4dbb24b8001324033a0abc131bc50a26e5d98284dcbb95d1be790e8cf13` is unchanged, not claimed as a new runtime check.
- Prior **CRR-001 Pass100/100** at `d9beb0f796894c37a371217768b9e33afcde315a` and receipt `deeea2f5826304d2d6fd20f5d91b7ce577d94b41` remains historical. This report supersedes its clean verdict for the confirmed defect; prior full structural review is not rerun.
- Read current API investigation, execution report (Cases/Acceptance-Criteria Proof), API revision record, R1 scope/REQ009/AC007/SCN002, design Local chooser, implementation Checks Run and prior reviewer report/history. Applicable TESTING.md and updated reviewer skill/finding-the-cause/ticket-scope/Example7/handoff read; no testing-guideline conflict.
- Revisions: SR001–003, ARCH-REV-002, IR-001, CRR-001, API-REV-001; delivery **N/A**. No production/durable-test changes by API or reviewer.
- Focused source: forms.js, chooser HTML, ordinary directory-list producer and existing browser coverage's waiting sequence. No storage/backend, privilege, release or app/editor re-review.

## Approved Behavior And Scenario Basis

**Supported Normal Scenario — SCN-002 / BEH-002**, grounded independently in
R1 UC-002 folder selection, REQ009 labelled keyboard/path-entry contract, DEC004
directory-only chooser plus explicit path entry, and design Local chooser.
A user selecting a server folder opens Browse folders and types an absolute
directory into its enabled field. The field is not documented or implemented as
unavailable until the first listing returns; current status even says manual
path entry remains available.

Expected: ordinary typing is retained while background listing updates its
results. Explicit List folders, child/parent navigation and selection retain
their existing meanings. This is one coherent user's normal workflow, not
imagined multi-tab concurrency, contradictory actions or arbitrary timing.

| Behavior | Current disposition | Evidence |
|---|---|---|
| BEH002 / SCN002 folder selection, REQ009/AC007 keyboard path entry | **Contradicted in this bounded part** | actual enabled-field typing and late completion overwrite; forms.js:28,38 |
| Other previously confirmed behaviors | Not reopened | no product delta or evidence tying this failure to another owner/backend; API scoped passed cases retain their attribution |

### Candidate Finding And Mechanism Gate

| Candidate | Independent trigger / contract | Forward path / lifecycle / consequence | Evidence | Disposition / scope |
|---|---|---|---|---|
| CG-008 — asynchronous listing replaces path draft | SCN002 normal user opens chooser and types; REQ009/AC007 and DEC004 | Browse → list(source/home) → POST running render → enabled input receives keys → scheduled GET complete → render assigns old listing path → remaining keys append to replacement | API07 real response timing/native-key control, forms.js:25–43, index.html:64, directories.go | **Promote / This ticket**, CR-001 |

Scenario/reachability gate **Pass**; material-premise gate **Pass**. Cause is
established, not held for more evidence. No new behavior ID or upstream
requirements change is invented.

## Failure Evidence And Reproduction

Primary evidence: `evidence/API-07-finding.md`, `API-07-runtime.json`,
`API-07-chooser.cjs`, `API-07-typing.png` and report API07 row. Reviewer inspected
the screenshot and response trace, not only the summary.

Recorded exact executable command:

```sh
/Users/normy/.hermes/node/bin/node /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard/tickets/in-progress/nfs-setup-dashboard/evidence/API-07-chooser.cjs
```

Run from the NFS worktree with private `HOME=$S/home TMPDIR=$S/tmp`;
historical `S=/Users/normy/nfs-dashboard-api-w47yo5sg` was removed. Native rerun
requires fresh owned resources from the linked API03 builders/resources/PTY
driver and updated harness scratch/IP/key paths. Transfer `API-03-pty.py` as
`driver.py`, not `pty.py` (which shadows stdlib). Do not run against operator
state or blindly reuse removed resource paths.

API's actual boundary: current public server, ordinary UID1000/GID109, real
loopback HTTP/private sudo helper and guest directory I/O; sandboxed
Chrome156.0.8078.47 reached the exact loopback port through test-only SSH.
Clipboard was doubled for host safety; directory responses, clock and keyboard
sequence were not replaced. No chooser storage plan was submitted.

| Observation | Recorded value |
|---|---|
| POST /api/directories |202/running, path /home/admin, time1792848888226 |
| Typing began |1792848888229; focus, Meta+A, /home/admin/api-dashboard,80ms/key |
| GET completion |200/complete, same path /home/admin, time1792848888728;502ms after POST |
| Expected final text |`/home/admin/api-dashboard` |
| Actual text |`/home/adminadmin/api-dashboard` |
| Same keyboard sequence after listing settled |exact expected text retained |
| Overall API07 |Fail; observation substep's Pass means capture completed, not functional acceptance |

The API reproduction proves the real user boundary and control. Review
attribution is **Read**: current source plus API's **Reproduced/Measured**
evidence. No additional reproduction, instrumentation, browser/VM creation or
product check was necessary; no reviewer execution is claimed.

## Confirmed Origin / CR-001

**Medium / Local Fix / implementation / open.**

1. `forms.js:41` opens the chooser and lists source/home.
2. `render` at25–28 assigns `directory-path.value = value.path || home` on
   every response, not only deliberate navigation/initialization.
3. Line38 schedules another render after the running response. Input remains
   enabled (`index.html:64`); no edit ownership is checked before assignment.
4. Real completion occurs inside the recorded typing interval. It resets the
   partial edit to `/home/admin`; subsequent keys produce the corrupted path.
   Settled control rules out inherent Meta+A/keyboard failure. Backend returns
   the correct requested directory.

forms.js is new in this ticket (absent at base52c17fb5, introduced by502205f),
and unchanged since CRR001/API execution. This is neither a change after review
nor an old surrounding-code bug. UC002/REQ009/AC007 fail in changed functionality,
so it is **this ticket**, not a prerequisite or follow-up. Working main-form
fallback does not make this enabled input correct.

Consequence: loss/corruption of active chooser path edit and unreliable keyboard
folder navigation. No file-content loss, storage mutation, wrong export,
privilege bypass or backend failure demonstrated; do not inflate the finding.

### Earlier review gap

**This should have been caught in CRR001.** The unconditional input assignment
on the asynchronous render path was visible, and normal manual path entry was
already in scope. Existing `browser.cjs:53–58` waits until Use this folder is
enabled before navigating/selecting; it did not exercise editing while the first
listing completes. That passing coverage was too narrow for the blanket chooser
behavioral-fidelity conclusion. Current evidence corrects the affected Runtime
Correctness/Behavioral Fidelity rationale and adds CR-001. No new composite
source score/full structural audit is assigned for this failure-origin-only
round; CRR001's100 is historical, not a current clean verdict.

## Bounded Required Correction And Validation

- Preserve active path edits across background listing completion. Keep explicit
  list submission, child/parent navigation, displayed listing and selected
  directory coherent. Fix the chooser owner, not storage/backend/shared admin
  architecture; no generic cross-session machinery requested.
- Start from supplied failing case and add a durable regression entering the
  normal chooser, typing before initial completion and asserting exact retained
  text. A controlled rootless browser fixture may hold a response for deterministic
  timing if labelled; exercise actual UI, do not claim fresh native storage proof.
  Do not hide failure by waiting for completion before typing, testing only
  settled input, or removing required manual-path behavior.
- Check settled typing and affected explicit navigation/selection alongside the
  regression. Reuse unchanged checks; no whole Go/native/Docker campaign solely
  for a bounded frontend correction without material affected inputs.
- Return Local Fix for targeted source review, then affected API/E2E validation.
  API owns resolution of API-F001 and its execution verdict.

## Evidence Preservation / Cleanup / Handoff

`evidence/CRR-02-origin-review.json` records source equality and response interval.
No diagnostic edits, tests, resources or scratch created by reviewer; only
reviewer documents/evidence change. API06 cleanup remains API-owned proof.
Prior storage/pending/expiry/CLI/service successes remain scoped evidence, not a
new blanket API Pass. No unrelated defect or follow-up added.

Recommended owner: **/software_engineering_team/implementation_engineer**,
selected by the fresh most-specific API/E2E failure-origin implementation-defect
rule in `evidence/CRR-02-routing.json`. No Delivery advancement, Designer/PM notification
or new approval loop. Source-only NFS task: no target merge/push/tag/release,
field/physical/user-verification/TaskDone claim.
