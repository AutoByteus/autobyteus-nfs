# API/E2E execution coverage — nfs-first-release

## Latest authoritative result
**API-REV-001 / round 1: Fail — 62.86% confidence.** R03-F001 blocks AC001 and real candidate completion. Both Mac jobs of actual candidate run **39111348848 / attempt 1** abort at `.github/workflows/release-nfs.yml:205`: `args[@]: unbound variable`. The exact empty-array workflow snippet reproduces on local `/bin/bash`3.2.57 before command entry; the nonempty fresh-mode control succeeds. No production/test fix by API.

This is a release-workflow shell failure, **not an NFS filesystem failure**, missing signing secret, user-test failure or new requirement. Preliminary **Local Fix → Implementation after Code Review failure-origin confirmation**. No successful-test/Delivery completion handoff is eligible. Missing physical resources remain separately disclosed, not the origin of this failure.

## Round, authority and execution basis
- Task `nfs-first-release` / `autobyteus-nfs-3` / `project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5`; Large / High / Reviewed. No prior API round for this task.
- Approved `requirements-doc.md` R2/SR002; `investigation-notes.md`, `solution-revision-record.md`, `design-spec.md` SR003 Ready; `design-review-report.md` / `architecture-review-revision-record.md` ARCH001 Pass; `implementation-handoff.md` / `implementation-revision-record.md` IR001; `code-review-report.md` / `code-review-revision-record.md` CRR001 Pass100 remain separate authorities.
- Trigger: CRR001 requests current executable release acceptance. `delivery-revision-record.md` DR001 is a bounded reviewed-branch staging prerequisite, **not Delivery Completed** or source recovery. Delivery's own uncommitted records were not staged or edited by API.
- Reviewed product886b55e1cf88f3f696334bd5e7b8c374946a594d; intake reviewc1f1330b8310bfadf772cebb09d085821be8da92; docs-only staged workflow/source **518f4b51e251edaa6b5664f71c7171bde57bafc9**; main remains7e375984be2bea7a4d536e43cc59d6bc2b116870. All119 product inputs identical.
- Canonical plan `api-e2e-coverage-investigation.md` written before execution; `api-e2e-test-case-ledger.md` initialized before cases and updated at checkpoints. Revision baseline `api-e2e-revision-record.md` records this completed result.
- Root AGENTS/DESIGN/TESTING/RELEASE/README and packaging/RELEASE, source/fixture owners inspected. No closer testing instructions. Personal execution only; no delegation. Prior extraction/old shared-filesystem/editor Tasks not reopened.
- Plan followed. Added bounded native local and actual preflight CLI probes before execution, then exact shell reproduction after observed failure. No complete candidate reader was run against fragments. No browser/application acceptance surface is relevant.

## Acceptance-criteria proof
Evidence folder: `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release/tickets/in-progress/nfs-first-release/evidence/api-e2e/api-rev-001` (E below). Paths are relative to E unless stated. None of AC001–008 is claimed fully complete from these partial results.

| AC | Critical | Cases / proof | Result and remaining boundary |
|---|---|---|---|
| AC001 | Yes | R03 `dispatch-receipt.json`, `hosted-final.json`, both Mac raw logs117628928559/117628928627, `post-run-remote.json`; R01/R02 supplement | **Not Proven / Fail**: no prior release needed, exact source dispatched; engine/OCI/Linux jobs succeed, both Mac jobs fail; no complete candidate artifact. Tags/releases/main unchanged. |
| AC002 | Yes | R01/R02 `python-release_records.log`, `publish-refusal.log`; R04, Q01–Q06, U01 | **Not Proven**: actual empty lock refuses; synthetic fixtures not qualification. Candidate absent, authorized physical host pairs unassigned; genuine executed-user-check not performed. |
| AC003 | Yes | R01 `python-release_signing.log`; D01 | **Not Proven**: real shell with fake signing/notary commands only. Candidate mode did not invoke signing. Six provisioned secrets are not validated signing/Accepted-notary evidence. |
| AC004 | Yes | R01 `python-release_publication.log`, `python-release_workflow.log`, R02 `prepare-results.json`; D01 | **Not Proven**: local retry/conflict/normal-version controls pass; actual publisher skipped, no tag/release was created. |
| AC005 | Yes | R01 `python-installer_fixture.log`; D02 | **Not Proven**: inert local installer/integrity controls only; no public versioned assets exist to download/install. |
| AC006 | Yes | R03 `hosted-job-117628015203.log`, `hosted-job-117628015271.log`, `hosted-job-117628452768.log`, `hosted-job-117628492072.log`; R01/R04 | **Not Proven**: actual two-arch engine and retained full OCI built/validated in hosted jobs; complete candidate identity/native archive set and publication equality absent. Never hand-assemble a qualified candidate from fragments. |
| AC007 | Yes | R03 `hosted-final.json`, `failure-summary.json`; D01/D02 | **Not Proven**: truthful failed attempt, not a completed first release. |
| AC008 | Yes | C01 `cleanup-local.json`, `mac-array-reproduction.json`, `final-checks.json`; downstream Delivery | **Not Proven overall**: API inputs/owners preserved and own scratch cleaned; current-main finalization/docs/public receipt remain Delivery-owned. |

## Execution and ledger reconciliation
50 planned top-level/qualification cases: **3 Pass (R01/R02/C01), 1 Fail (R03), 43 Blocked (R04 +42 Q cases), 3 Not Tested (U01/D01/D02)**. R02-native/R02-preflight and R03-F001 are supplements/checkpoints, not extra unique cases. No case remains running. Narrow suite reruns overlap broader counts and are not summed as unique coverage.

| Cases | Surface / exact scope | Observed result | Evidence |
|---|---|---|---|
| R01 | Fresh119-file independent APFS copy, private HOME/TMP/cache; `/usr/bin/python3 -m unittest discover -s scripts/tests -p 'test_nfs_*.py' -v` after relevant narrow suites | Pass:38collected/37executed/1Go-child-only skip. Signing commands, GitHub/registry and user evidence doubled; installer binary inert. | `local-results.json`, `python-all.log`, narrow logs |
| R02 | actionlint1.7.11, ShellCheck0.11.0, separate Bash syntax, production source hash, expected empty-lock publication refusal | Pass local controls; unqualified source hash8c1bcc… is **not measured-engine candidate identity** | `local-results.json`, `source-hash.log`, `publish-refusal.log` |
| R02-native | Fresh official Go1.27.2 native macOS26.5.2arm64; `go test -race -json -count=1 ./...`, `go vet ./...`, build/version | Pass7packages,59top-level/252including subtests; standalone child skip covered by parent. Built development-unqualified, not release. | `native-results.json`, `test-counts.json`, `go-race.log`, `native-binary.json` |
| R02-preflight | Actual release.py CLI/Git with emulated Actions environment | Valid candidate preflight succeeds; stale workflow/wrong event/beta/non-main publication4expected refusals. Not actual hosted run. | `prepare-results.json`, `prepare-*.log` |
| R03 | `gh workflow run release-nfs.yml --repo AutoByteus/autobyteus-nfs --ref codex/nfs-first-release -f release_tag=v0.1.0 -f source_sha=518f4b51e251edaa6b5664f71c7171bde57bafc9 -f publish=false` | **Fail** run39111348848 attempt1; full matrix allowed to finish, not cancelled by API. | `dispatch.log`, `dispatch-receipt.json`, `hosted-final.json` |
| R03 hosted passes | prepare, engine-package amd64/arm64, merged engine, OCI, native Linux amd64/arm64 | 7jobs successful. Each Linux native job: race7packages/vet/Python38collected37executed1skip/build/version/package. Actual pinned engines and whole OCI; no physical setup. | `hosted-log-index.json`, `hosted-execution-summary.json`,9raw job logs |
| R03 hosted failures | macos-15 arm64 job117628928559; macos-15-intel amd64 job117628928627 | Both exit1 in native-check shell at empty array; no Mac metadata/Go/native archive checks reached. Hosted OS15 is not required OS26 physical qualification regardless. | two Mac raw logs and focused excerpts |
| R03-F001 | `python3 .../probe-mac-array.py`, exact source lines203–205, `/bin/bash`3.2.57, inert python function to observe command entry | Candidate exit1/not called; fresh control exit0/called. Local shell version measured; hosted logs identify `/bin/bash` but do not separately print its version. No source patch. | `mac-array-reproduction.json`, `mac-array-system-{candidate,fresh}.log` |
| R04 | Documented actual candidate-envelope/fetch/verify and alias-only probe | Blocked: final candidate job skipped, artifact absent. `fetch-actual-candidate.py` is **unexecuted scaffolding**, not evidence. | `hosted-final.json`, `post-run-remote.json` |
| Q01–Q06 / seven operations each | Four target tuples/six native-or-Docker modes; public NFS CLI/standard shell/Python/Git, independent host/kernel boundaries and required physical coverage | Blocked: no current complete candidate and no assigned disposable physical host pairs. No live host/app containers repurposed, no fabricated first-use registry pull. | `inventory.json`, `remote-refs.log`, DR001 assigned-host statement |
| U01 | Genuine executed-user-check | Not Tested. Only user can supply their own actual execution statement; requested resource inventory is not verification or a release approval questionnaire. | No user-test receipt exists |
| D01/D02 | Delivery qualification acceptance/current-main/final signed payload/publication/recovery/public-download | Not Tested; downstream gates, neither Pass nor waived | `post-run-remote.json` and Delivery DR001 |
| C01 | Cleanup and preservation | Pass within API ownership; remote failed-run partial build artifacts intentionally retained with identities/expiry | `cleanup-local.json`, `mac-array-reproduction.json`, `final-checks.json`, `post-run-remote.json` |

## Confidence and broader-validation decision
Equal mean over7applicable categories; CLI is the user surface, browser/desktop N/A. Scores are validation confidence, **not Code Review source quality**. Actual execution increases direct knowledge but reveals a missed material regression; more jobs green do not compensate for missing critical evidence.

| Category | Post-local | Final | Evidence / uncertainty |
|---|---:|---:|---|
| Requirements/AC proof |50|50|Critical actual candidate criterion fails; platform/public criteria absent. |
| Changed-boundary directness |75|75|Real complete hosted attempt plus exact local shell reproduction; candidate reader/publication never reachable. |
| Integration realism/mock gap |50|50|Real Actions/builders/OCI and Linux native jobs; no physical NFS/real registry first-use or public release. |
| Environment/configuration/identity fidelity |50|50|Exact SHA/run/attempt/workflow bytes, measured engine builds; required physical Mac26/Linux pairs missing. |
| Failure/edge/lifecycle/recovery |75|75|Actual failed-stage gating and bounded shell control; parser/sign/retry/refusal fixtures pass but public recovery/host lifecycle unexecuted. |
| CLI/download user-surface |50|50|Local CLI/version/inert installer checks; no complete candidate or final public native install. |
| Durable regression relevance |95|90|Existing assertions remain valid; bounded material gap: static workflow truth tables/syntax do not execute empty-array path on Mac shell. |

Post-local63.57%; final **440/7 =62.86%**. Threshold95% unmet; all applicable categories except durable coverage below90. All critical criteria directly proven: **No**. Broader validation **Required** after source correction; physical subsection also **Blocked** on assigned resources. This round's dominant verdict is **Fail**, not a request to lower qualification. Real user execution is separately listed for Delivery, not the reason for this numeric failure.

## Validity, state, scope and coverage changes
- Existing durable coverage remains Still Valid; no assertions removed/reinterpreted to obtain green. Add targeted executable supported-shell coverage in the bounded correction after origin review; none authored by API this round. **Durable paths added/updated/removed: None. Production paths changed: None.** Successful-test review N/A on this failed result; request failure-origin review instead.
- Local source archive sufficient for repository tests; actual host/candidate/publication boundaries deliberately separate. No broad validation on user-running applications.
- Host persisted state Not Affected; no migration/dual-reader/legacy fallback introduced. Qualification is an empty lock awaiting actual rebuilt evidence, not old extraction qualification. General original-payload recovery is supported, not a legacy compatibility shim.
- Fixtures emulate GitHub/registry, notary/keychain and synthetic qualification to exercise parser/refusal/cleanup. Local CLI preflight emulates GitHub environment; real hosted evidence is separately bound to the exact attempt. Shell probe stubs only the invoked command to show it is not reached in candidate mode. No synthetic record enters a real qualification lock.
- Scripts and logs under E are temporary execution/evidence artifacts. `fetch-actual-candidate.py` remains unexecuted because candidate missing; no local candidate resource/alias metadata was created. No source manifest embedding, registry writes or platform setup.

## Cleanup, effects and preservation
Independent source/toolchain/cache/native binary removed after source equality/no-owned-process checks. Shell probe temporary home removed. Hosted jobs completed their post-job cleanup; platform-managed runner disposal is not independently audited. API monitor process finished; no cancellation, owned persistent daemon, mount, export, VM, registry, container or user application process created. Existing app containers untouched.

Seven remote run artifacts are intentionally retained as **partial failed-attempt evidence**, not a qualified candidate: engine package arm64/amd64, merged engine, OCI, BuildKit record, Linux native arm64/amd64. `post-run-remote.json` gives immutable IDs, wrapper digests/sizes, actual expiry **2027-01-16T08:24:58Z**. No remote deletion. No `nfs-release-candidate`, final payload or signing/publication receipt exists. Tags/releases and main unchanged; publisher skipped, OCI build `push:false`, no candidate registry login/write/signing path executed. Qualification lock unchanged.

119product inputs and795protected ticket inputs checked unchanged against recorded input audit. Delivery's concurrent uncommitted documents/evidence remain separately owned and unmodified; explicit API-only staging required. No push/main merge/tag/release/deploy/TaskDone/user-verification/Terminal action by API.

## Failure-origin package and resumption
**R03-F001 / AC001,AC007:** expected current supported Mac candidate shell enters metadata/native check; observed exit1 before entry on both hosted arches. Recommended owner Implementation for bounded workflow invocation + executable supported-shell regression, confirmed by Code Reviewer. Source/engine/OCI/default gates must not be weakened; no unbound-variable suppression, target removal or synthetic qualification claimed here. Exact logs/positive control attached, no new architecture/user-approval cycle inferred.

After reviewed correction, reuse case IDs and explicitly close R03-F001 with new actual candidate execution. Workflow belongs to production source hash: current attempt cannot become a new-source Pass by changing a label. R04 then uses exact successful run/artifact; only afterward can assigned physical resources enable Q01–Q06. Delivery owns actual final acceptance/signing/publication once all prerequisites are met. Fresh routing recorded in E/routing.json; only matching failure-origin recipient receives this result.
