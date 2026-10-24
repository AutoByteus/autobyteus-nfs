# Docs sync — nfs-cli-approval-feedback

DR-001,2026-10-24; Small/Low/Direct. Trigger API001 Pass95.00%.
Bootstrap and freshly integrated remote base both456e5808e828d224804f9d4ce65c4cf740816eca;
merge Already current before Delivery-owned edits. Evidence: delivery-evidence/dr-001/preflight.json
and verification.md. No source or test changes by Delivery.

## Long-lived docs reviewed
| Path | Result | Reason |
| --- | --- | --- |
| docs/dashboard.md | No additional change | Implementation already documents source-only feedback, trustworthy handshake vs password observation, metadata-only readiness, one10s reminder, uncertain failures and Stop/drain. Explicitly says publicv0.2.0 does not contain this improvement. |
| TESTING.md | No additional change | Current terminal-feedback section explains real child/HTTP/PTY boundaries, scheduler vs real10s, ordinary protocol double and excluded OS/storage campaigns. |
| RELEASE.md | No change | Source-only main finalization and separate version authorization remain applicable. No release requested by this Task. |

## Durable knowledge and removal
The two implemented doc additions are sufficient and match integrated source and
approved design: terminal projection is not an authority, a successful metadata
read is not storage readiness, Stop suppresses stale guidance without cancelling
admitted work. Session owns feedback; obsolete PID-only/raw transport logging was
removed as recorded in implementation-handoff.md. No compatible old-message path,
persistent readiness flag or migration needs documenting.

**Docs impact for Delivery: No additional change.** Do not rewrite already accurate
long-lived docs for activity credit. New delivery documents record evidence-method
correction and actual finalization separately; upstream reports are preserved.
No unresolved wording/scope issue, follow-up or guide deviation. Release notes
Not required for this source-only task. Continue source finalization only.
