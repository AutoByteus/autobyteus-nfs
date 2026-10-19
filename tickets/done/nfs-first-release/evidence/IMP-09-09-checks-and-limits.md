# IMP-09-09 — Implementation check excerpts and limits

Date: 2026-10-19. Environment: macOS26.5.2 arm64, Python3.9.6,
Bash3.2.57, actionlint1.7.11. Commands: IMP-09-05/06/07/10/11 harnesses beside
this file; exact argv and source commit in each result/log. Production4c665e0;
final source/tests22205cc (test-only delta). No remote/publication execution.

## Final observations

- IMP-09-06 full Python: `Ran 72 tests in 330.543s`; `OK (skipped=1)`.
  The skip is `invoked by Go platform bootstrap regression`; the Go parent was not
  rerun this round. Thus71 executed tests, not72 executed. Full log `IMP-09-06-python.log`.
- IMP-09-10 affected publication at22205cc: `Ran 15 tests in 53.114s`; `OK`.
  Added four controls retain explicit tag/annotation refusal, same-size corrupt
  existing assets, private-image failure→same-byte retry, and public-download byte
  checking before an owned-HOME version command. Other suites unchanged from06.
  No claim of one full76-test current-commit run.
- Both harness results: all five commands exit0; owned clones/home/tmp/cache removed.
  Actionlint checks both actual workflows; Bash syntax separate from executable
  supported-shell controls in Python. Source hash is
  `e3e814176d8315f0426df379035a995b6c0e6d5f89f82483f121b074c79eea21`.
- IMP-09-05 six mutants each exit1 and `detected: true`. Omitted admission,
  omitted full-tree scope, recreation of missing known draft and omitted main
  freshness yield `AssertionError: ValueError not raised`. Restored published-only
  discovery yields `TypeError: 'NoneType' object is not subscriptable`. Substituting
  E for P yields `ValueError: Candidate source/engine differs`. Logs preserve full
  traces. These are expected negative controls, not failing final product tests.
- IMP-09-07 actually reads retained candidate/payload; uses current full validators
  against a Git-proven frozen P snapshot. Candidate recordSHA67eb4dd2…,
  publicationSHA3b0cbedd…, P source3e1af43a… match; both Accepted receipt binary hashes
  match actual retained archives. `retainedInputsUnchanged: true`, `snapshotCleanup: true`.
  `Reviewed recovery authorization required` refuses absent real authority;
  current default candidate verification refuses original candidate as expected.
- Same07 uses **saved** DR013 jobs/draft through endpoint doubles, not gh/network:
  successful payload117940491787, four native jobs/two signing steps, exact owned
  draft417014769/body. No fresh remote visibility/retention/Apple result is inferred.
- IMP-09-11: fixed repair scope, no original lock/releases/runtime/engine/signer/
  installer/license drift, unchanged source_hash/SOURCES AST; empty unused import
  list, max388 nonempty production lines. Other-owner authorities unchanged.
  Prior IR001–008 prefix preserved. No actual recovery authorization created.

## Attempts preserved

01: first10 publication tests had2 errors from owned Mac `/var` alias in the new
snapshot assertion. Fixed by resolving the owned temporary directory; symlink
source rejection remains, covered by positive/negative tests. 02:54 focused
initial tests pass. 03: user-interrupted full check onccf3d5b, no final verdict.
No associated process remained at continuation; its exact owned scratch was
removed and partial log kept. 04: earlier actual-byte check atccf3d5b, superseded
by07. 08: source audit at4c665, superseded for added tests by11. No hidden retries,
failed-baseline promotion or stale-result relabelling.

## Limits / custody

Endpoint adapters use authenticated-production semantics but synthetic network,
registry and command boundaries. Synthetic Git history/authorization is test-only.
Actual retained bytes and saved job/Accepted evidence are not a current API result,
fresh source-review Pass or permission to publish. Full real read-only inspect-bound
and affected API validation remain downstream; then Delivery judges evidence and
creates genuine stable authorization, fresh-integrates E and performs hosted
same-byte recovery/public download/OCI/install/signature verification.

No new Go/Linux/native-engine/signing/credential/field campaign solely for executor
repair. Runtime/installer/signer and original assets are unchanged. Both Mac actual
DeveloperID/Accepted proof remains DR013; deleted historical signing causes are not
recovered. No tag/draft mutation, main push/merge, release, TaskDone or Terminal.
All prior candidates, private local diagnostic, PM data and other-owner work remain.
Field/user Deferred custody: Delivery → terminal Solution Designer → requesting PM.


Raw-log whitespace exception: IMP-09-03-python.log:47 (interrupted unittest
progress line) and IMP-09-05-recreate-known-draft.log:7 (raw unittest subtest
progress line) retain their original trailing space. They are evidence, not
source/style defects. Header-only silent-command logs explicitly annotate no
output/exit0. All other staged source/docs/evidence whitespace is clean.
