# Code Review Report — Extract AutoByteus NFS

## Review Round Meta

- Date/reviewer:2026-10-18, code reviewer; personal execution, no delegation.
- Entry: implementation-return source/test review after **DR002 hosted Linux Local Fix / IR005**. Source round5 / **Targeted Delta Review / CRR-007**. Not successful post-API test review or a new architecture review.
- Task extract-autobyteus-nfs / project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8. **Large / High / Reviewed**, unchanged.
- Canonical ticket is already **tickets/done/extract-autobyteus-nfs** in N. Archive location does not mean terminal completion. Prior source report CRR005 Pass100 retained in N a61e4120aaf3b3bab440861bc9d5504202420767 at its then-in-progress path; prior test report remains CRR006 unchanged.
- Authority: [requirements-doc.md](requirements-doc.md), **R2 Approved/SR003**; [investigation-notes.md](investigation-notes.md); [solution-revision-record.md](solution-revision-record.md); [design-spec.md](design-spec.md), **SR004 Ready**; [solution-design-handoff.md](solution-design-handoff.md); [user-filesystem-boundary-correction.md](user-filesystem-boundary-correction.md); [design-review-report.md](design-review-report.md)/**ARCH-REV-002 Pass**; [architecture-review-revision-record.md](architecture-review-revision-record.md). Eight authorities unchanged.
- Trigger/current implementation: [implementation-handoff.md](implementation-handoff.md), [implementation-revision-record.md](implementation-revision-record.md), IR005; [delivery-revision-record.md](delivery-revision-record.md), DR002 Blocked; [handoff-summary.md](handoff-summary.md), [finalization.json](delivery-evidence/dr-002/finalization.json). [code-review-revision-record.md](code-review-revision-record.md) appends CRR007.
- N worktree `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs`, recovery branch codex/extract-autobyteus-nfs. Reviewed HEAD21ec9f7c05f959e2b4361f2e335a3d71209a8dd2; test candidate09cac96225fe4f36fb0dcbe6ddec01248992874f atop56c0c59efdd3b963b2fc11ba07bda7410b4067b2. Runtime83726b27400b405a7a6a79bd962d8e2419daa561 unchanged.
- Completed pushes are Delivery-owned recorded facts, not repeated actions: N main/ticket22e934b first, S ticket9b72c8d1 then personal55bff1f5 --no-ff/tree-equal. S worktree retired; not recreated. D0 populated by Delivery; untouched here.
- [api-e2e-execution-coverage-report.md](api-e2e-execution-coverage-report.md)/[api-e2e-revision-record.md](api-e2e-revision-record.md): API002 integrated S Pass95 and CRR006 no-delta gate retain exact-input limits. They did not qualify hosted Linux. Hosted runs39097778705/39097779223 remain failed/cancelled; no current CI claim.
- Current reviewer evidence [review-audit.json](code-review-evidence/crr-007/review-audit.json), [checks-and-limits.md](code-review-evidence/crr-007/checks-and-limits.md). IR005 logs/mutations are inspected implementation execution, not reviewer reruns.

## Routing Classification Review / Scope

Large/High retained. **Targeted Delta Review of the new DR002 fixture-recovery boundary**: only internal/setup/hosted_config_test.go changes; no production spine, interface, data shape, dependency, workflow or security policy changes. This is a test-only implementation return, not a fresh full source audit because it follows CR002 chronologically. Proportional test checks apply without implementation-file size limits. All unchanged production structural evidence/scores from CRR005 carry explicitly; fixture/assertion/readiness checks are freshly revalidated below. No source-score deduction for a corrected fixture or unexecuted downstream hosted gate.

Read full changed file and actual Status/Detach -> VerifyGanesha/VerifyGaneshaForDetach -> Mounts/Observe/Matches/Unmount path, later RemoveJob/package-mask/Docker effects, baseline/candidate/mutation logs, current root policies and DR002 completed-operation context. No additional package instructions found. Read-only identity audit confirms107 of108 non-ticket inputs identical to blocker baseline; only the test differs. All production/workflow/config-safety bytes unchanged. Source hash independently remains348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e; publication still refuses with empty qualification.

## Supported Behavior / Production-Path Basis

| Contract/scenario | Independent basis and supported entry | Forward path/lifecycle/consequence | Review treatment |
| --- | --- | --- | --- |
| SCN001 / REQ001,002 / ENG-NATIVE-CHECKS | Contributor or CI runs documented go test -race ./... on supported Linux/macOS; N TESTING and ci.yml | Hosted-config fixture invokes actual Service methods against owned private records and controlled effects; suite must distinguish config preflight from later observation | Supported normal engineering scenario; fixture portability is in ticket, not extra runtime functionality |
| SCN006 / BEH005 / AC009 | Operator asks public status or consented drained detach; wrong config/source and partial-owned teardown preservation are explicit requirements | CLI -> Service.CheckConfiguration -> backend Verify -> platform observe/unmount -> only then job/backend teardown; changed config must refuse, missing partial-detach config must reach existing checks | Supported normal/explicit safety edge, unchanged contract |
| ENG-ISOLATION | Documented unprivileged repository tests must not mutate live mounts/jobs/configuration | Synthetic owned records -> verified unrelated existing proc observation -> real mismatch refusal before teardown; Darwin runner error still controls command boundary | Supported test-isolation contract. /proc is a read-only test stand-in, NOT an endorsed NFS deployment target |
| Other R2 SCN001/002/003/007, DS1–6 | Approved independent service/ordinary application paths/private-profile ownership | Production bytes unchanged; S delivery receipt/tree preserved, API002 S evidence retains limits | Carry CRR005/006 basis; no app/NFS management coupling or frontend tab removal |

### Candidate Finding And Mechanism Gate

| ID | Candidate / independent premise | Trace/evidence | Disposition |
| --- | --- | --- | --- |
| C007 | DR002 old fixture assumed all mounts pass through Runner; ENG-NATIVE-CHECKS | Linux Mounts reads /proc/self/mountinfo directly. Absent default target yields Status mismatch; Detach passes absent mount, reaches correct root-owned mask-store refusal or deliberately unusable Docker client panic. Baseline native UID1001 reproduces exact failures | **Confirmed fixture defect, corrected by IR005**; no remaining finding. Earlier reviews missed this OS-specific runner assumption; Darwin/cross-compile evidence never proved native Linux. Historical results retain limits |
| C008 | Possible production trust/Docker defect inferred from those fixture errors | The bad runner assumption let a deliberately incomplete test service escape its intended observation boundary. Actual root-store refusal is expected policy; fixture nil HTTP client is not evidence of a supported production nil-client lifecycle | **Reject as production defect attribution**; do not bypass trust, add runtime fallback or require a new injection seam |
| C009 | Is /proc fixture hiding ignored preflight or causing live effects? ENG-ISOLATION/SCN006 | Fixture verifies proc filesystem and nonmatch; Status asserts specific config error/ENOENT for invalid/missing inputs; valid config asserts exact mismatch. Detach asserts unrelated-source refusal, zero Linux commands, exact bytes/absence after retries. Three mutants fail relevant assertions | **Promote as justified fixture mechanism, not defect**. No proc write, real unmount, root bypass or Linux skip |

## Focused Fixture Review

- Four existing test groups retain engine/content/pending cases; no assertion disabled or test skipped. Native and Docker hosted cases still cover missing/old/different/malformed/current configuration.
- Linux observes its native mount table; Darwin uses one injected mount-command error. OS-specific call counts are explicit and reset between retries, not weakened to any-error success.
- Invalid/missing Status config cannot pass merely because later mount observation fails. Missing configuration during partial detach remains permitted to reach existing refusal, not mistaken for readiness.
- Retry and Apple/connect controls preserve configuration and private receipt bytes as well as file absence. All fixture writes remain under t.TempDir; reads of /proc are intentional/checked.
- Existing unusable Docker client is a tripwire, not a newly added runtime dependency. Actual source-order inspection confirms before-effect refusal; mutation controls detect removed verification and overstrict missing-config rejection.
- Earlier source-review gap is acknowledged: fixture assumed a Darwin seam without checking Linux Mounts. The current fix closes the code-level gap; it does not retroactively make failed hosted runs pass.

## Structural / Design Checks

Unchanged production checks below carry CRR005 source evidence; test clarity, fixture isolation, stale assumptions and readiness are freshly reviewed. No S checkout recreation or unrelated full audit.

| Check | Result | Evidence | Required action |
| --- | --- | --- | --- |
| Task design health assessment present/evidence-backed/preserved | Pass | R2 boundary refactor; DS1–6 match current owners | None |
| Approved supplemental artifacts matched | Pass | User correction and ARCH002, not historical R1 | None |
| Data-flow spine inventory clarity/preservation | Pass | All six R2 paths re-evaluated; E4 manager/activation/input/publication trace, unchanged N identity | None |
| Ownership boundary preservation/clarity | Pass | App paths vs N host owner; profiles stay runtime-owned | None |
| Off-spine concerns serve clear owners | Pass | Config admission, profile exposure, packaging identity bounded | None |
| Existing capability/subsystem reuse | Pass | Existing Store, lock, workspace manager, preparation and native clients | None |
| Reusable owned structures | Pass | One profile builder and trusted state admission, no provider-specific copies | None |
| Shared-structure/data-model tightness | Pass | Current upstream optional input/observer ports remain separate from private profiles; host/ACP shapes unchanged | None |
| Repeated coordination ownership | Pass | Existing preparation/thread/session owners retain exact release | None |
| Empty indirection | Pass | Removed admission wrapper; surviving owners own actual policy/lifecycle | None |
| Scope-appropriate separation/file responsibility | Pass | Distribution/config/host orchestration/runtime profiles remain separate | None |
| Ownership-driven dependency direction | Pass | No app/service runtime imports; no sibling module/build dependency | None |
| Authoritative Boundary Rule | Pass | WorkspaceManager, session/thread managers and config.Store remain authoritative | None |
| File placement | Pass | Admission under config, native profile under shared runtime concern | None |
| Flat versus over-split layout | Pass | Existing small owners reused, obsolete modules removed | None |
| Interface/API/command boundaries | Pass | Current upstream publication/input interfaces preserved; host-only commands/exact profile/ordinary cwd unchanged | None |
| Naming/responsibility alignment | Pass | Connection fixture is service input, not public app attachment contract | None |
| No unjustified duplication | Pass | Shared private preparation and engine helpers retained once | None |
| Patch-on-patch complexity control | Pass | Clean removal, no old/new strategy branch or compatibility bridge | None |
| Dead code removed in touched files/modules | Pass | CR001/CR002 resolved; prior29-file audit carries; current fixture helpers/imports used | None |
| Relevant test scenarios/assertions clear | Pass | Fresh review: missing/changed Status config cannot pass via unrelated error; current/missing retry and Apple/connect controls retain intent | None |
| Test fixtures/helper coherence | Pass | Fresh review: per-test private state, read-only Linux mount observation, inert command runner, exact record preservation | None |
| No stale/duplicated/compatibility-only tests | Pass | Fresh review: OS-specific fixture expectations, no Linux skip or obsolete runner-only assumption retained | None |
| API/E2E readiness | Pass | IR005 actual native fixture evidence; no safety weakening; source-stage ready | Affected N API validation, then Delivery hosted CI |

## Source File Size And Structure Audit

No production file changed or grew. Existing CRR005 size/ownership audit carries; test files are explicitly outside implementation size/delta thresholds.70 additions/22 deletions in one coherent hosted-config test file add OS-aware boundary checks and a small private-record preservation helper, not production infrastructure.

## Legacy / Persisted Data / Dead Code

Production legacy/compatibility/persisted-state decisions unchanged: host-only direct usable state with bounded active/pending obligation refusal, no migration/history scan/alternate version runtime. No old application coupling restored. Removed test assumptions are replaced rather than retained behind a Linux skip. CR001/CR002 remain resolved; no new unused helper/import observed in the changed file. Root/private config safety unchanged.

## Docs-Impact Verdict

No product documentation change required for this fixture correction. Delivery already corrected stale R1 RELEASE prose during DR002; it is **not still an outstanding item**. Delivery must update current CI/fix-forward receipts and terminal status. Retain existing frontend instructional Guide; no release authorized.

## Additional Material Premise Validation

MP001 active and MP002 pending predecessor obligations unchanged; prior source/persistence evidence carries. No new production premise or recovery machinery. The only new fixture assumption—existing Linux proc mount—is checked read-only and fails explicitly if unavailable, never silently skipped.

## Review Scorecard

**10/10 =100/100 retained**, not a new test confidence or hosted-CI score. Ten source categories carry unchanged production evidence; affected readiness/cleanup/test structure revalidated with the bounded fixture review. No score deductions or open source findings.

| Priority | Category | Score | Reason | Weakness / improvement |
| --- | --- | --- | --- | --- |
| 1 | Data-Flow Spine Inventory and Clarity | 10 | Carried DS1–6 review; production spine unchanged | None demonstrated |
| 2 | Ownership Clarity and Boundary Encapsulation | 10 | Filesystem-only app boundary and host-only service respected | None demonstrated |
| 3 | API / Interface / Query / Command Clarity | 10 | Adopted upstream ports and R2 direct preparation preserved; no restored mount interface | None demonstrated |
| 4 | Separation of Concerns and File Placement | 10 | Existing concern owners preserved, no replacement framework | None demonstrated |
| 5 | Shared-Structure / Data-Model Tightness and Reusable Owned Structures | 10 | Host state narrowed; profile builder shared; ACP variant explicit | None demonstrated |
| 6 | Naming Quality and Local Readability | 10 | Subjects and scope explicit; no size pressure | None demonstrated |
| 7 | API/E2E Readiness | 10 | IR005 fixture issue corrected without production changes; affected N validation next | Hosted completion remains Delivery-owned |
| 8 | Runtime Correctness And Behavioral Fidelity | 10 | R2 production unchanged; prior integrated source review and API002 S controls carry | No established runtime defect; API002 S validation remains valid |
| 9 | No Backward-Compatibility / No Legacy Retention | 10 | Clean-cut behavior and bounded refusal, no compatibility execution | None demonstrated |
| 10 | Cleanup Completeness | **10** | CR001/CR002 resolved; prior unused audit carries; current fixture helpers/imports used | None demonstrated |


## Findings / Prior Resolution

No remaining finding. CR001/CR002 import findings remain resolved. DR002 fixture defect corrected at source/test-review boundary by IR005; affected independent validation and fresh hosted CI remain separate gates. No established production defect or changed requirement, so no Design Impact/Requirement Gap/failure-origin machinery prescribed.

## Follow-ups

None. No new Task or reopened filesystem/editor/provider work.

## Classification / Recommended Recipient

**Pass — bounded fixture correction accepted; failure classification N/A.** Use fresh most-specific fixture/test Local Fix complete route to `/software_engineering_team/api_e2e_engineer` for affected N validation only. Then normal successful-test gate/Delivery fix-forward. Do not repeat unaffected S suites or recreate its worktree. No duplicate dispatch.

## Evidence And Limits

Personal read-only diff/identity/path audit, source-hash and expected publication-refusal checks pass. No Go binary on current reviewer PATH; no download or runtime suite rerun undertaken because current native baseline/candidate/mutation evidence plus direct source analysis establish this review result. Independent API remains next.

IR005-attributed native Linux arm64 Ubuntu24.04 UID1001 container: baseline failure; corrected focused/full race7packages/vet/build/version/Bash pass; Python20collected17executed3skips, existing Go container/child skips. Native Darwin arm64 focused/no-live-source-detach plus race7packages/vet pass. Three native Linux mutants fail intended assertions, not compilation. Initial implementation harness wrong-root attempt retained. Reviewer discovery read of nonexistent mount_table.go returned ENOENT; corrected to actual mount-observation.go, no test/product failure.

Local arm64 success is not hosted Ubuntu amd64 or cancelled macOS matrix completion. No actual live NFS/export/provider/physical qualification, release or user verification. IR005 scratch independently absent; container cleanup is attributed to its receipt. No live resource created here, source/test edits, target fetch/push/reset or completed paired-operation replay. DR002 Blocked persists until Delivery's own current-CI and final gates.

## Latest Authoritative Result

**CRR007 Pass / source score retained100**, targeted implementation-return fixture review. Production and clean separation unchanged; current test correction judged valid without weakened safety or assertions. API affected N validation next. Archived ticket remains canonical. Completed paired source pushes stand; hosted/final Delivery completion still open. No release/TaskDone/Terminal claim.
