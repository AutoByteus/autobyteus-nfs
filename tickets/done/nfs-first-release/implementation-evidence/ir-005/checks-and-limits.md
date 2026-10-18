# IR-005 signing failure diagnostic boundary — local evidence

R3/SR004 Approved/Ready, ARCH002; Large/High confirmed. Trigger DR005 Blocked
at b2c6fdf after already-completed main7683494 source finalization. This round
repairs the demonstrated diagnostic loss, not an established credential failure.
`diagnosis.md` traces exact original run/jobs/log lines and remaining uncertainty.

## Changes and local checks

- Existing signing shell emits fixed stage/exit/cleanup on saved stderr and an
  exclusive sanitized failure sidecar after cleanup. No raw arguments/tool output,
  identity/account values, passwords/P12/keychain data uploaded or logged.
- Staged keychain-list capture cannot restore a failed partial snapshot. Cleanup
  failure refuses success without masking original nonzero stage/exit. Known
  rejected/pending notary receipt remains separate; Accepted plus command exit0
  and successful cleanup are still required. No real signing command arguments
  or target/gate change. Failed/pending jobs cannot package/publish.
- Workflow always-upload allowlist now includes only sanitized notary and failure
  JSON receipts. No broad directory upload of private signing state.
- New executable control fails on baseline missing receipt; current focused17
  tests pass. Independent exact source copy/private HOME+TMP runs full52 Python
  tests:51 executed,1 expected standalone-Go-child skip. No new Go-parent claim.
- System Bash3.2.57 arm64/Python3.9.6; Bash syntax, ShellCheck0.11.0 and
  actionlint1.7.11 pass. Source/recipe hash commands pass. Four bounded mutations
  are detected: hidden safe diagnostic, conditional function disabling errexit,
  failed search-list capture restored, and invalid notary acceptance.
- --check-publish without candidate refuses with "Identified candidate is
  required"; logfile label was over-specific (attempts.md). Source hash comparison
  separately proves current readiness is stale; no new real readiness prepared.

Commands/exits/timings: checks-result.json; full raw Python log python-all.log,
focused-final.log, mutation logs and source-check.json. Baseline harness mistake,
first implementation's hidden trap stderr, overlapping initial edit and ShellCheck
literal warning are disclosed in attempts.md, not counted as final-source passes.
Raw failed-diagnostic whitespace is preserved at15 locations across7 raw/headered
logs, enumerated in final-checks.json. Source/docs and other staged whitespace
must be clean. Primary check-ID/headered evidence and the Checks Run table were
added under ticket evidence/ following the updated skill; original raw logs remain.

## Limits and continuation

All command-boundary tests use fake credentials and tools. Native Go/runtime,
Linux/four-target build, actual Apple import/signature/notary, hosted upload and
public downloads were NOT executed this round. Go/runtime and engine recipe/pins
are unchanged; prior CRR005/006, API00395 and DR005 four-native checks retain their
exact-input scope, not new signing evidence. The original real signing stage/cause
is still unknown; six provisioned secrets must not be blamed/reprovisioned absent
specific evidence from the next authorized hosted run.

No source push/main merge/hosted dispatch, live keychain/state/host-storage change,
credential read/export, release or TaskDone/Terminal. Delivery's finalized source,
readiness records and retained candidates remain in place unchanged. Own scratch
and doubled resources cleaned. Archive tickets/done/nfs-first-release remains the
canonical authority; archive location is not Task completion.

Production signing/workflow changed, so NEW complete applicable current-source
candidate and affected API evidence must precede renewed Delivery acceptance and
actual signed publication. Reviewer receives this bounded correction first. The
existing source finalization must not be undone/replayed. Field/user testing is
explicitly deferred and not a release/closure gate; genuine both-Mac Accepted
notary/signatures, final immutable payload and public receipt gates still stand.
