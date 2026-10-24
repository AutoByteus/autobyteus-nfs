# API/E2E Test Review Report — CRR-004

## Review Meta

- Date: 2026-10-24. First successful-test gate, cumulative reviewer round4.
- Task: **nfs-setup-dashboard / autobyteus-nfs-2 / project_task_f1264eb8-5a99-4a19-949f-09d141c955a1**.
- Trigger: **API-REV-002 Pass95.00%** following CRR003/IR002. Large/High/Reviewed unchanged. This is not failure-origin or another implementation review.
- Input: f71c4c3d26763a16a8b30fa09a1ce78e3c09ee0d; source/tests7b0577a4f2637ddf12a74a0156e4243a41a3719c; reviewc223dcb/receipt34afb80caa80afa293cabc1d2786618a3c9516bc. Tracked clean at intake. Git confirms zero non-ticket delta since CRR003 receipt.
- Worktree: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, `codex/nfs-setup-dashboard`, target origin/main.
- Approved context carried: R1/SR001 `requirements-doc.md`, `investigation-notes.md`, `solution-revision-record.md`; SR003 `design-spec.md`; ARCH-REV-002 and `architecture-review-revision-record.md`. No supplementary behavior or new decision.
- Implementation context: `implementation-handoff.md` Checks Run and IR002 in `implementation-revision-record.md`. Original source review: `code-review-report.md` CRR003 Pass100; unchanged by this gate.
- Current reviewer history: `code-review-revision-record.md`, **CRR-004**. No prior unresolved test-review finding. CR-001 source-resolved in CRR003; API-F001 execution-resolved by API002, not by this reviewer.
- Read current `api-e2e-coverage-investigation.md`, `api-e2e-execution-coverage-report.md` (Cases/AC Proof), `api-e2e-revision-record.md`, selected current runtime/cleanup/attempt evidence. Delivery revision: N/A.
- Project testing guideline: root `TESTING.md`, notably source-built dashboard section; no closer guideline or discrepancy found. Applicable AGENTS/DESIGN unchanged.
- Supported product scenario basis **Yes**: SCN002/BEH002/REQ009/AC007/DEC004, normal folder selection using the enabled path field while its initial listing returns. Established before fixtures by approved behavior and original API07 actual user-surface failure.

## Changed Durable Test Scope

**No durable test file changed during API001 or API002: Yes.** Current-stage test-code result is **Not Applicable**. Temporary browser probes, raw logs and screenshots are executable evidence, not new durable suites. No fabricated API-authored delta or fresh full source score.

The requested cumulative IR002 coverage was already independently read in CRR003. Its exact bytes and review remain valid:

| Durable path | Earlier change | Related scenario / responsibility | Current disposition |
|---|---|---|---|
| internal/dashboard/__tests__/chooser.cjs | Added by IR002 | SCN002/REQ009/AC007: real embedded chooser, actual POST/GET response delivery held across keyboard prefix/suffix; settled input, explicit navigation, exact selection and correctable error | CRR003 review carried; unchanged, no new finding |
| internal/dashboard/__tests__/browser.cjs | Updated by IR002 | Existing rootless preview runner, both engines/widths and original normal role controls; invokes coherent chooser cases and closes modal before Stop | CRR003 review carried; unchanged, no new finding |

Other cumulative durable coverage remains within CRR001's unchanged review. No removals or assertion weakening. No implementation-source size limits applied to tests or temporary evidence.

## Proportional Test-Code Checks

N/A denotes the absent new durable delta; notes record why cumulative prior review and successful evidence can advance without repetition.

| Check | Result | Evidence / notes |
|---|---|---|
| Clear scenario grouping and names | N/A | Carried CRR003: chooser-post/poll separate initial response boundaries; normal roles remain distinct |
| Assertions prove requirements | N/A | Exact draft/focus/suffix and listed-path selection, not incidental call counts standing in for UI behavior |
| Meaningful fixture/helper reuse | N/A | Same existing tagged Go preview; one chooser scenario reused across methods/engines/widths |
| Isolation and determinism | N/A | Owned source/HOME/browser; durable controlled delivery, natural-timing API proof separate |
| Coherent navigable tests | N/A | One chooser journey plus existing runner; no new mixed suite |
| No stale/disabled/compatibility-only tests | N/A | No new durable delta; old failure and normal controls retained |
| Coverage agrees with investigation and execution | Pass | API002 plan/report plus IMP17 red, IMP18 16green; current natural timing below; counts overlap, not additive unique coverage |
| Independent supported-scenario basis | Pass | Approved folder/path-entry contract and prior actual API07 failure, not a scenario invented from test internals |
| Real trigger and actor steps | Pass | Browse → focus/normal keyboard → actual listing completion → explicit navigation/selection. Root double only exposes UI; no fabricated directory bytes |

## Executable Evidence / Closure Assessment

Read `evidence/API-07-02-browser.cjs` as an evidence harness, not production source. It observes real directory responses; it contains no route/response/clock interception. `API-07-02-result.json` records and asserts completion within the keyboard interval:

| Width | Initial GET completes after typing begins | Typing span | Result |
|---|---:|---:|---|
|1280|510ms|6042ms|Exact intended text retained;10 checkpoints Pass|
|390|512ms|6049ms|Exact intended text retained;10 checkpoints Pass|

Same settled80ms/key control, focus, explicit List/parent/child/exact source selection/reopen, failed-list correction, no browser errors/overflow and Stop/token-clear pass. Actual ordinary-user Go HTTP/directory reader, isolated sandboxed Chrome156 on Macarm64. Root protocol doubled to inspect only; no storage or clipboard action. This closes the changed chooser boundary, not a new native storage campaign.

Inspected retained `API-07-02-390-typing.png`: focused long-path input scrolls to its tail; Use this folder is disabled for the unlisted draft, labelled modal/actions remain visible. Exact full text is proved by JSON/assertions, not inferred from clipped input display. No reviewer browser/product execution.

Preparation's unsupported Python tar-filter call and initial post-process-exit token check are disclosed in `API-07-02-attempts.md`. Corrected harness waits for the existing stopped UI acknowledgement before the same token-absence assertion. No production workaround/assertion removal; prior failed attempts retained. `API-06-02-cleanup.json` reports166 matched inputs, both preview exits0, no owned process and removed scratch.

`API-01-02-reuse.json` correctly separates current IMP18/19 and unchanged API03–05 native/Docker/pending/client/expiry proof. Only later TESTING instructions differ from checked7b0577a4. Native proof keeps its original source/binary/platform and composite-client limits. No fresh native/AMD64/physical/field/user/release qualification inferred. Current API report proves API-owned AC001–008 portions; AC008 integration/finalization stays Delivery-owned.

## Findings / Follow-ups

- New test-code findings: **None**. No classification or corrective dispatch.
- Prior API-F001 / CR-001: source closure remains CRR003; API002 provides executable closure. API001 Fail81.43 and original red evidence remain unchanged history.
- Follow-ups added: **None**.

## Latest Authoritative Result

**Not Applicable — no new durable API/E2E test delta; successful-test gate complete and package ready for Delivery.** Cumulative IR002 test review is carried from CRR003 without findings. No unresolved finding IDs. No new source score or reassignment of API's95% confidence.

Normal successful-validation continuation goes to Delivery under the fresh selected rule in `evidence/CRR-04-routing.json`. Delivery must perform documentation synchronization, fresh target/integration verification and permitted source finalization; source/API Pass is not Delivery completion. This is the source-only NFS task, with **no release/tag/publication authorization**. No app/superrepo edits, push/target merge/TaskDone or user-verification claim by reviewer.
