# Investigation — NFS terminal approval feedback

Package `nfs-cli-approval-feedback` / `autobyteus-nfs-7`; Solution Designer, 2026-10-24. Requirements R1/SR-001 Approved; architecture evidence E06 supports SR-002. Evidence, intent and technical design remain separate.

## Workspace and authorities
N = `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-cli-approval-feedback`; branch `codex/nfs-cli-approval-feedback`. Bootstrap refreshed origin and created this task worktree from `origin/main` **456e5808e828d224804f9d4ce65c4cf740816eca**. Finalization target `origin/main`, fresh integration under RELEASE.md. Canonical checkout `/Users/normy/autobyteus_org/autobyteus-nfs` remains local main7e375984 with untracked task-plans; not authored/reset/cleaned. Older detached task archives untouched. No bootstrap blocker.

Authorities read in full this conversation: current solution-designer SKILL.md; references/requirements-engineering.md, finding-the-cause.md, ticket-scope.md, handoff.md; requirements/investigation/solution-revision-record templates. Architecture gate after R1 approval: references/architecture-design.md, design-principles.md, design-spec-template.md; project root DESIGN.md reread. Root AGENTS.md, DESIGN.md, TESTING.md and RELEASE.md read; no closer tracked package AGENTS/DESIGN found. General design-examples not needed for this local presentation shape. No authority conflict found.

## Sources and findings
All source line references are against base456e5808. No source was changed by Solution Designer. Additional post-approval read-only `git diff --name-only 448cef839b4919a1e3ae0489e8d86ae36f5cee33 HEAD -- internal cmd go.mod go.sum` returned empty: these current production paths equal the published-source paths, without claiming fresh installed-binary execution.

| Evidence | Method | Source / observation | Meaning and limits |
|---|---|---|---|
| E01 | Read | PM current assignment, user observes installed publicv0.2.0 server at Password with no subsequent text; Ctrl+C has existing safe-stop text | Screenshot described, not attached/inspected. No diagnosis of wrong password, stall or broken share. No private token/password collected |
| E02 | Read | cli/run.go:58–72 dispatches host-checked roles; cli/dashboard.go:68–104 ordinary-user/TTY, digest and fixed `/usr/bin/sudo -- <same executable> internal-install internal-dashboard-helper <role>`, child stderr unchanged; dashboard/browser.go:45–58 already serves private HTTP/prints deliberate one-time fallback before any authorization | PID and elapsed time cannot establish approval. No change to sudo retry/env/argv is needed to add feedback |
| E03 | Read | cli/install.go:34–55 root/host checks, serialized install, sanitized exec; cli/dashboard.go:18–65 installed path/pipe/initiator checks then admin.New; admin/session.go:45–70 root/trust/digest admission; admin/pipe.go:16–20 emits hello afterward | Validated matching hello is the first existing parent-observable evidence of admitted administrative helper, not the precise password-acceptance instant. Root installation/admission can fail before hello |
| E04 | Read | dashboard/privilege.go:29–64 launches, prints only PID line, waits for bounded validated hello; read:90–95 gives ambiguous disconnect/approval error; session.go:147–182 performs authorization then initial inspect, updates cached operation only; admin/state.go:57–120 metadata-only inspection | Successful inspect can return empty/configured/pending; no mount/probe/readiness. reply.Error can leave helper alive while operation incomplete. There is no terminal success or failure output after launch |
| E05 | Reproduced | Independent archive of456e5808, official verified Go1.27.2 darwin/arm64; current Session.submit/perform/authorize and real child pipes with controlled helper. `evidence/approval-feedback-probe.log` and result | 12 subcases (2roles × empty/configured/pending/inspect-error/denied-exit/mismatched digest) all reach expected existing states; all fail feedback assertions. Six success cases: authorized=true, operation succeeded, terminal only PID. Six failure controls: incomplete, terminal only PID. This establishes local missing feedback, not actual sudo/OS/password/storage behavior |
| E06 | Read; post-approval architecture | Search `authorize\(` shows one production call session.go:156, one durable test call privilege_test.go:42; `s.log` set browser.go:46, consumed session.go:156. submit:120–145 owns stop/serial/dedup; perform:167–181 drains on transport error then completes state; Stop/Drain:184–200. browser.go:69–97 has opener goroutine and shutdown output | Existing Session owns attempt and final state; output must share serialization, stop readiness/reminders without cancelling work. No root/protocol change needed. All messages are ordinary-user presentation |
| E07 | Read | dashboard/web/app.js:5–18,56–70 already names awaiting authorization, exposes operation errors and distinguishes configured/pending/readiness. docs/dashboard.md Open and authorize/End management; dashboard/privilege_test.go and http_test.go:105–169 | Browser UI can stay unchanged; current tests verify correlation/dedup but not terminal text. Existing same-request retry and explicit post-expiry authorization are supported; not new concurrent workflows |

## Supported scenario basis and behavior inventory
R1 owns product-level scenarios SCN-001–007 and BEH-001–003. Independent witnesses: user workflow/explicit request, public documented role launches/Authorize/Stop, existing idle-expiry/dedup/security contract. Protocol doubles reproduce these established boundaries; they do not create new product scope. Manual corruption/hidden-state edits, unrelated multi-session coordination and field setup are excluded. No additional unclear material scenario was used to drive design.

## Actual production path (both roles)
1. Ordinary CLI role → CheckHost/TTY → dashboard.New (nonroot loopback listener) → Run (private bootstrap/opener/fallback, signal lifetime).
2. Browser explicit Authorize → authenticated same-origin operations endpoint → Session.submit serial/request-ID admission → perform.
3. Fixed launcher → actual OS sudo (terminal owns retries/password/cached consent) → root binary install/admission → installed helper root/role/pipe/initiator checks → admin.New trusted digest → ServePipe hello.
4. Parent authorize validates protocol version/ID/role/digest → perform calls inspect through same serial pipe → admin locked InspectConfiguration metadata only → correlated reply → operation result/browser polling. Current terminal only logs child PID before step3 completes.
5. Ctrl+C/Stop closes admission → HTTP shutdown → workers and helper drain → bootstrap/capabilities cleared; storage is not disconnected. Existing helper Close closes input and waits, not kill. Service reconciliation/lock/reconnect remain unrelated preserved admin paths.

## Diagnostic execution and reproducibility
Owned root `/Users/normy/nfs-feedback-probe-2tp40to6` was0700, with independent Git archive, HOME/TMPDIR/cache/toolchain. Official metadata at https://go.dev/dl/?mode=json&include=all was fetched; downloaded go1.27.2.darwin-arm64.tar.gz size/hash matched its record (see probe-toolchain.json). A **test-only probe file** was added to the independent source copy, never production source or canonical checkout. No diagnostic production edits, sudo, root helper, OS browser, exported storage, network service configuration or credentials were used. New() bound ordinary localhost listeners which were closed by deferred cleanup; no private URL was printed. Child fixtures exercise actual session/pipe logic and do not simulate real OS qualification.

Reproduce using an independent owned source archive outside /private or /tmp, with private HOME/TMPDIR/GOCACHE and local Go1.27.2: copy `evidence/approval-feedback-probe.go.txt` to `internal/dashboard/approval_feedback_probe_test.go` in that disposable copy, then `go test ./internal/dashboard -run '^TestApprovalFeedbackProbe$' -v -count=1 -timeout=45s`. Base result exit1 is intentional missing-feedback red, with all control states correct. For implementation, preserve the diagnostic baseline; adapt the private output capture if its owner changes and strengthen per-phase assertions in durable tests rather than treating this minimal diagnostic as a complete acceptance suite. No production fix was tested here.

Toolchain preparation completed without error. Probe pass/fail result and raw output retained unchanged. Parent execution collected; process scan of owned resolved path empty; owned source/toolchain/cache/HOME removed. `probe-cleanup.json` records exact evidence hashes and root absence. No active probe process/resource or owned scratch remains.

## Design-health evidence and constraints
Local presentation omission, not a proven privilege/storage defect. Relevant source sizes: session200, privilege133, browser101 lines at base; no size/ownership refactor prerequisite. Admin has a single existing root owner; dashboard has a single existing attempt owner. Feedback can consume its actual completion events and remain off the execution path. Root configuration/state schemas/readers/writers unchanged; **Not Affected**, no stored-data migration. New private output state must not become a readiness authority or browser DTO.

No dead code identified in relevant traced production paths. Replaced PID-only presentation call/signature may become removable in implementation; existing pipe/wait methods remain live. No new follow-up/prerequisite found. Existing field qualification Task autobyteus-nfs-4 is outside scope and unchanged.

## Unknowns and validation boundaries
- Actual user's sudo result/wait time and current root/storage state unknown and deliberately uninspected. Source+probe establishes why the terminal can be silent even on success.
- No actual password-entry/cached OS approval/negative OS policy validation performed by Solution Designer. No root/real mount acceptance claim.
- Full affected/current tests and realistic PTY flows belong to Implementation/API; they must report doubles, failed attempts, skips and exact source. Separate physical-field validation remains deferred, not a prerequisite or Pass.
- Timer/output ordering and Stop races need focused race tests; no new administrative or application concurrency contract is intended.

## Supplement inventory
All paths below relative to this ticket; owned by Solution Designer, supporting evidence only, not behavior-defining approval supplements.
| Path | Purpose / scope | Status / related IDs |
|---|---|---|
| evidence/approval-feedback-probe.go.txt | Reproducible ordinary-user session/pipe feedback diagnostic; never product source | Baseline red; AC-001/003/004 |
| evidence/approval-feedback-probe.log | Unedited current baseline execution | Observed red; E05 |
| evidence/approval-feedback-probe-result.json | Command/source/exit/scope summary | E05, no OS acceptance |
| evidence/probe-toolchain.json | Official toolchain origin/hash/size | Preparation evidence |
| evidence/probe-root.txt | Exact owned disposable root identity | Removed, not retained runtime |
| evidence/probe-cleanup.json | Removal/no-process/evidence hash receipt | Complete |
Product/UI artifacts: N/A. No full forwarding manifest; other authorities remain canonical repository files.
