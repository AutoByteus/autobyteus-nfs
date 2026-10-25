# Actual public v0.2.1 smoke inspection

2026-10-25, Delivery personally viewed server/client1280/390 screenshots. Correct
role titles, approval-only page, safety notice and Stop button; no overlap or
document overflow. These images capture the transient waiting frame following
Authorize; they are NOT screenshots of a settled failure or successful approval.
Direct actual HTTP state had already reported incomplete/unauthorized; terminal
transcripts independently show waiting→Could not start helper→safe Stop. No false
confirmed/ready line. This is not a UI redesign or full failure-rendering claim.

Actual installed public MacARM64 binary/Run/currentHTTP/PTY and sandboxed Chromium
156.0.8078.4, no request/root protocol doubles. Per-process OS sandbox denies both
sudo and opener execution before they run (preflight control verified). One explicit
authorize submission per role; no sudo process/cache/password/root/storage changes.
Actual Stop clears browser token and process exits0 with no bootstrap residue.
Both traces inspected; zero browser errors. Source success/long-wait/Stop proofs
remain separately attributed controlled-child tests, not real OS approval evidence.
No automatic browser-opener, Intel-local/physical/field/user qualification claim.
