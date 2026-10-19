# IR-005 local attempts and limits

1. Initial import-failure double referenced CERTIFICATE after the script deliberately
   unset it, so the fake command exited1 before its intended5. Raw
   baseline-harness-attempt1.log retained. Corrected only the test double to emit
   fixed fake sentinel values; no real credentials used or observed.
2. Corrected baseline diagnostic control on unchanged production exits5 but fails
   the new missing-failure-receipt assertion; baseline-diagnostic-control.log.
3. First implementation signing-focused-attempt1.log fails32 assertions: EXIT trap
   inherited the private function stderr redirection, hiding the safe stderr line.
   Fixed via dedicated saved stderr for constant diagnostics only. This attempt
   overlapped the search-list staging correction and is not final source proof.
4. Initial ShellCheck warned SC2100 for an unquoted internal keychain-password
   label; quoted the literal (no runtime change). Current shellcheck.log supersedes.
5. Cleanup inspection found the existing search-list pipeline could save [] after
   a failing security command and then restore it. Capture now moves from a pending
   file only after the strict pipeline succeeds; focused control prohibits restore
   on failed capture. No live keychain/list was touched: all external commands doubled.

Final current-source independent suite and lint results are recorded separately.
No local or hosted real signing run, secret read/export, remote write or public
release was attempted. DR005 original command stage/root cause remains unknown;
new safe diagnostics are prerequisite evidence for the affected hosted continuation.

6. The final runner's logfile label `stale-readiness-refusal` is over-specific:
   the actual `--check-publish` invocation had no candidate argument and refused
   "Identified candidate is required". This is missing-input refusal, not an
   executed stale-candidate validation. Current-vs-recorded source hash comparison
   establishes stale readiness; existing full-suite source invalidation tests pass.
   Raw file/command/result retained without relabeling its diagnostic.

7. Evidence runner-only unused hashlib/os imports were removed after execution.
   Its command lists, executable body and tested source are unchanged; this is
   not a post-validation production change or another claimed execution.
