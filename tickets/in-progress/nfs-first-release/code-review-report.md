# Code Review Report — nfs-first-release

## Review Round Meta

- Date:2026-10-18. Task `autobyteus-nfs-3` / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`.
- Entry: **API/E2E Failure-Origin Review**, round **2**, revision **CRR-002**. Review scope: **N/A — focused failure origin**, not full source or successful-test review.
- Trigger: API-REV-001 **Fail62.86%**, case R03, failure **R03-F001**; actual build-only candidate run39111348848/attempt1.
- Requirements: `requirements-doc.md`, **R2/SR-002 Approved**. Investigation/design/history: `investigation-notes.md`, `design-spec.md`, `solution-revision-record.md`, **SR-003 Ready**; relevant SCN001/BEH001/DS1 and D1/D2/D4 unchanged.
- Architecture: `design-review-report.md`, `architecture-review-revision-record.md`, **ARCH-REV-001 Pass**. Implementation: `implementation-handoff.md`, `implementation-revision-record.md`, **IR-001**. No later source fix exists.
- Prior review: **CRR-001 source Pass100.00** at c1f1330b8310bfadf772cebb09d085821be8da92, receipt518f4b51e251edaa6b5664f71c7171bde57bafc9. Prior complete report remains in Git at that commit; this canonical report now governs the failed boundary. History: `code-review-revision-record.md`, CRR001 byte prefix retained.
- API context read: `api-e2e-coverage-investigation.md`, `api-e2e-execution-coverage-report.md`, `api-e2e-test-case-ledger.md`, `api-e2e-revision-record.md` and focused raw evidence under `evidence/api-e2e/api-rev-001` (A below).
- Delivery context: **DR-001** staged the reviewed ticket branch only as an API prerequisite. This is not delivery-stage source recovery or Delivery Completed. Its eight existing untracked files remain owned by Delivery and unchanged/unstaged by review.
- Input HEAD72dc48b1aedbec8260951a4e851a7417a5672201; actual hosted source/workflow518f4b51e251edaa6b5664f71c7171bde57bafc9; product source886b55e1cf88f3f696334bd5e7b8c374946a594d. All119 non-ticket inputs identical since source review. Branch `codex/nfs-first-release`; target `origin/main`.
- Root TESTING.md and existing workflow fixture scope reread. Existing syntax/truth-table tests are valid for their stated boundary; they do not execute this native shell block. No guideline conflict.

## Routing Classification And Scope

**Large / High / Reviewed** unchanged. Confirm only the supported Mac candidate shell failure, source origin and necessary correction/coverage. Do not reopen architecture, Go/NFS runtime, editor/application, physical-host policy, signing provisioning or public recovery design. API authored no production or durable-test change; its diagnostic runner is evidence, not a new product scenario.

## Upstream Behavior And Production-Path Basis

Approved behavior is unchanged and clear. **BEH001 implementation status: Contradicted** for the normal Mac candidate path. REQ001/002 and AC001 require the exact reviewed nonpublishing candidate journey across the advertised matrix; AC007 cannot complete without it. The design selects both Mac runners and requires all native jobs before aggregation. No new behavior or unsupported edge case is invented.

| Scenario | Independent actor / goal / entry | Forward path and lifecycle | Expected consequence | Evidence / validity / use |
| --- | --- | --- | --- | --- |
| SCN001 / BEH001 / DS1 | Maintainer prepares first normalv0.1.0 from the reviewed ref through manual publish=false dispatch | prepare resolves candidate → engine pair/merge/OCI succeed → native Mac job enters `/bin/bash -e` run block → strict mode → args=() and fresh-only append → line205 argument expansion → intended metadata/native tests/archive → complete candidate | Candidate mode must invoke metadata with no qualification options, then run checks and retain its native archive; all required jobs permit candidate aggregation | R2 REQ001/002,AC001; SR003 D1/D2/D4; actual run and both raw Mac logs. **Supported Normal Scenario; Reachable; Use**. |

### Candidate Finding Gate

| Candidate | Observation | Independent trigger / contract | Forward state / consequence | Evidence | Disposition / scope / response |
| --- | --- | --- | --- | --- | --- |
| CG008 | Empty optional-array expansion under the actual supported Mac job shell aborts candidate metadata invocation | SCN001 normal publish=false dispatch, not a synthetic test or manually corrupted state | MODE=candidate leaves args empty; set -u expansion fails before Python invocation; Mac native checks/archives absent, aggregate candidate skipped | workflow203–205; A/hosted-job-117628928559.log:252–259 and117628928627.log:252–259; reviewer reproduction.json | **Promote — This ticket**. CR-001 bounded workflow invocation and executable regression correction. |

No held or rejected material candidate. Existing MP001/MP002 are not implicated or reclassified. Scenario gate **Pass** means the defect has a valid supported basis, not that implementation passed.

## Failure Evidence And Independent Confirmation

Actual API command:

```sh
gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha=518f4b51e251edaa6b5664f71c7171bde57bafc9 -f publish=false
```

[Actual run39111348848](https://github.com/AutoByteus/autobyteus-nfs/actions/runs/39111348848), attempt1: completed failure. Seven jobs succeeded (prepare, two engine builders, merge, OCI and two Linux native jobs); both Mac jobs failed; candidate/payload/publish skipped. Reviewer inspected the preserved API run/job records, not a new hosted run.

- Mac jobs117628928559 (arm64) and117628928627 (amd64) show `shell: /bin/bash -e {0}`, MODE=candidate, their respective darwin TARGET, then `line 5: args[@]: unbound variable` and exit1. The printed native block maps this precisely to source205. Command text printed by Actions is not proof those later commands executed.
- Exact current source203–205 initializes an empty array, only populates it in fresh mode, then expands it under preceding `set -euo pipefail`. The failure happens before the metadata-generating Python invocation and subsequent Go tests. The earlier OCI-inspection command is not the failed call.
- Reviewer independently extracted those three **unchanged** lines and executed `/bin/bash -e` in four isolated observations (two mode values for each TARGET environment value). Inert Python function records command entry/argv only. Candidate exits1 before entry; fresh/nonempty control exits0 and includes the expected qualification options.
- Local measured shell: **GNU Bash3.2.57(1)-release, arm64-apple-darwin25**. TARGET=darwin-amd64 is only a string in the local probe, not amd64 execution. Actual amd64 failure is established by its hosted job. Hosted shell version itself was **not printed**, and is not inferred from local version.
- Evidence: `code-review-evidence/crr-002/input-audit.json`, `hosted-evidence-review.json`, `exact-snippet.sh`, `reproduction.json`, `review-failure.py`, `checks-and-cleanup.json`. API reproduction remains corroboration and was not rerun because its runner appends to API-owned documents.

## Finding — CR-001: Mac candidate shell aborts before native checks

- Priority: **High — blocks the approved candidate journey**, not a data-loss/security/NFS-runtime attribution.
- Path: `.github/workflows/release-nfs.yml:203–205`, specifically line205 optional argument expansion.
- Related failure/case: **R03-F001 / R03**. Related approved basis: **SCN001,BEH001,REQ001/002,AC001**, downstream AC007. Promoted candidate: **CG008**.
- Origin: **implementation-owned release workflow defect introduced in IR001, plus an earlier source-review gap**. Exact workflow/product bytes are unchanged after CRR001; this is not an implementation change after review.
- Why in scope: the newly delivered first-release candidate path cannot complete for either retained Mac target. It is inherent to AC001, not a surrounding pre-existing issue or optional follow-up.
- Required correction: make metadata argument construction/invocation work under the supported runner shell with both candidate (no qualification arguments) and fresh (the exact qualification arguments) while preserving strict failure handling and correct argument boundaries. Add a bounded **executable** regression at that shell boundary, sensitive to the original candidate failure and covering the populated fresh control. Do not merely add text assertions, drop targets, mask the error, weaken qualification, or introduce a runtime filesystem change. The exact implementation is the implementation owner's decision.
- Closure: targeted source re-review, then API-owned actual new current hosted candidate including both Mac native jobs and complete aggregate artifact, plus affected qualification/refusal checks. Workflow is production-hashed; preserve the failed run and partial artifacts, but do not relabel them as a successful new-source candidate or hand-assemble one.

## Origin Alternatives And Earlier Review Gap

| Attribution | Decision / evidence |
| --- | --- |
| Implementation defect | **Confirmed**: approved candidate mode produces the failing empty-array state in unchanged production workflow on both actual Mac jobs. |
| Earlier review gap | **Confirmed, bounded**: CRR001 checked scheduling truth tables, syntax and static analysis but did not execute the native candidate argument block under the Mac system shell. The review should have verified that the intentionally empty optional arguments remain callable under the selected shell and set -u; the small local inert-command probe now demonstrates that this was reasonably detectable without physical hosts/secrets. |
| Runtime-only unknowable failure | Not the right attribution: external hosted execution exposed it, but the same source-level shell invariant is independently locally reproducible. |
| Invalid/stale test or fixture/environment error | Not supported: actual intended runner/dispatch, correct candidate state and unchanged source fail before tests. A production job's unsupported assumption about its selected shell is not an excuse to waive the failure as a test environment problem. |
| NFS/runtime or credential failure | Not established: metadata/native test/signing boundary not reached. Physical resource shortage and six provisioned-but-unvalidated secrets are separate remaining gates, not this cause. |
| Design/requirement gap | Not established: four-target candidate behavior and workflow ownership are already explicit; no approval change or architecture loop required. |

## Affected Prior Review Rationale

CRR001 remains historical; its source-quality100 is **not the current acceptance result**. Its BEH001 confirmation and category7 API/E2E-readiness/category8 behavioral-fidelity rationale are superseded for this shell boundary by CR-001. A complete new scorecard is **N/A for focused failure-origin review**; no arithmetic re-score or repeat of unrelated24 structural checks. Unaffected architecture/source evidence is not declared newly failed or reexecuted. Current canonical verdict is **Fail** until the bounded correction is independently reviewed and tested.

## Classification / Recommended Recipient

**Local Fix — implementation_engineer**, exact recipient selected by fresh failure-origin rule. No source or durable-test fix by reviewer. After correction require source review and API/E2E again; later successful execution receives proportional test-code review normally. No duplicate API/Designer/Delivery dispatch.

## Follow-ups

None. This defect belongs to the current ticket. No PM follow-up or previous filesystem/editor task reopening.

## Cleanup, Preservation And Residual Limits

Own diagnostic temporary directories removed; four subprocess observations completed. No hosted dispatch, source/test modification, credentials, mounts, VM/container, registry/publication, target fetch/merge/push or live-user action. All119 product inputs and selected existing evidence unchanged during the probe; Delivery's eight untracked files remain unstaged and byte-preserved. History append preserves CRR001 bytes; final audit separately confirms all pre-existing tracked inputs except the two intentionally updated canonical review documents.

API's retained records show no complete candidate and seven partial failed-run artifacts with actual expiry2027-01-16T08:24:58Z. They stay untouched, not qualification. Its post-run remote receipt reports tags/releases/main unchanged and no signing/publication/registry-write path reached; reviewer did not independently mutate or refresh remote state.

Physical/independent host inventory, actual user execution, real signing/Accepted notary, final payload/publication/download and Delivery current-main gates remain open and independent of this local correction. Six secrets are provisioned; do not ask again without an actual provisioning/validation failure. Current task conditionally authorizes normalv0.1.0; old extraction no-release direction does not apply. No TaskDone, Terminal or release completion claim.

## Latest Authoritative Result

- **Fail — CRR-002**, API/E2E Failure-Origin Review.
- **CR-001 / R03-F001: implementation-owned Local Fix; bounded earlier review gap acknowledged.**
- Supported-scenario and material-premise gates: **Pass**. Behavior BEH001: **Contradicted at the Mac candidate invocation**.
- Score: **N/A — focused failure-origin round**; API's Fail62.86% remains API-owned.
- Next: Implementation Engineer for bounded workflow/regression correction, then targeted source review and new current API candidate validation.
