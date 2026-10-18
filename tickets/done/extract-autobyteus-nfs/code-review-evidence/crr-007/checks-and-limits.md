# CRR007 checks and limits

Scope: archived ticket, DR002/IR005 test-only fixture correction. Read full diff,
fixture, actual Status/Detach/preflight/native mount/unmount/later-effect paths,
requirements SCN001/006, N DESIGN/TESTING/ci.yml and completed Delivery receipts.
Personal git/byte audit: only hosted_config_test.go differs from56c0c59;107 other
non-ticket inputs unchanged; eight authority docs unchanged. Sourcehash unchanged,
expected unqualified refusal. review-audit.json stores commands/identities.

Assertions judged against independent repository-check/isolation/host-refusal
contracts, not a synthetic new product scenario. Linux /proc is read-only and
verified nonmatching; no live command executes. Exact error assertions prevent
ignored preflight passing on a later mismatch. Retry/Apple/connect controls
preserve receipt/config bytes and missing files. No source seam or Linux skip.
Prior review missed OS-specific runner assumption; corrected fixture accepted,
no product bug inferred from expected root Store refusal or dummy client panic.

IR005 native baseline/focused/race/vet/build/mutations inspected, not rerun.
No Go on reviewer PATH; no toolchain/runtime resource created. API owns affected
validation; Delivery owns hosted Ubuntu amd64/macOS completion. Prior failed/
cancelled hosted runs remain historical failures, not cleared by arm64 evidence.
A discovery read guessed mount_table.go and returned ENOENT; actual source is
mount-observation.go and was read. No source/test failure or assertion change.

CRR007 Pass, source score100 retained. No API/test-review confidence assigned.
No new Task, S rebuild/worktree recreation, completed push replay, target action,
release or terminal completion. IR005 scratch absent; container cleanup attributed.
