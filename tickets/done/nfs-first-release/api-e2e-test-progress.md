# API/E2E Test Progress

Execution report: api-e2e-execution-coverage-report.md. Planned cases: api-e2e-coverage-investigation.md.
Introduced during API003 after the skill update. Earlier starts/events remain in api-e2e-test-case-ledger.md; rows below are recorded now from saved evidence, not fabricated earlier Started timestamps. Only append rows. Historical ledger is frozen after this transition; current results belong to the report.

| Time | Case ID | Event | Result | Note |
|---|---|---|---|---|
| 2026-10-18T10:28:36.912777+00:00 | R01 | Completed | Pass | Completed before skill update; actual full45/44executed/1skip plus overlapping workflow7/records12 in E3 logs. |
| 2026-10-18T10:28:36.912777+00:00 | R02 | Completed | Pass | Completed before skill update; original unsupported recipe command preserved; corrected API and remaining checks pass, cleanup complete. |
| 2026-10-18T10:28:36.912777+00:00 | R03 | Checkpoint | Not Tested | New exact run39118784695/1 still running; engine jobs passed, native jobs pending. Existing monitor PID/session tracked, do not dispatch another run. |
| 2026-10-18T10:30:50.376078+00:00 | R03 | Completed | Pass | Run39118784695/1 success; all4 native/engine2/OCI/aggregation passed. Logs collected; payload/publish intentionally skipped; remote main/tag/release unchanged. |
| 2026-10-18T10:30:50.376078+00:00 | R04 | Started | Not Tested | Fetch/verify exact new candidate using repository facade; current envelope first. |
| 2026-10-18T10:30:52.932968+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-envelope; evidence candidate-envelope.log |
| 2026-10-18T10:31:23.465095+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-fetch; evidence candidate-fetch.log |
| 2026-10-18T10:31:24.456510+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-verify; evidence candidate-verify.log |
| 2026-10-18T10:31:25.446800+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-metadata-alias; evidence candidate-metadata-alias.log |
| 2026-10-18T10:31:26.313119+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-metadata-wrong-digest; evidence candidate-metadata-wrong-digest.log |
| 2026-10-18T10:31:27.057066+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-metadata-wrong-version; evidence candidate-metadata-wrong-version.log |
| 2026-10-18T10:31:27.252948+00:00 | R04 | Checkpoint | Not Tested | Pass candidate-readiness-refusal; evidence candidate-readiness-refusal.log |
| 2026-10-18T10:31:27.263210+00:00 | R04 | Checkpoint | Not Tested | Pass actual artifact/engine/full OCI/four archives verified; alias-only admission and refusals; no host/first-pull qualification; evidence candidate-validation-results.json; candidate-local-retention.json |
| 2026-10-18T10:31:39.592732+00:00 | R04 | Completed | Pass | actual API envelope mismatch refused before destination/download; correct candidate untouched; evidence actual-envelope-refusal.json |
| 2026-10-18T10:31:57.008202+00:00 | R05 | Started | Not Tested | Actual retained Darwinarm64 binary version and strict admission refusals in owned HOME; no installation/setup. |
| 2026-10-18T10:31:58.521499+00:00 | R05 | Completed | Pass | actual retained Darwinarm64 CLI version on local Mac; owned scratch removed, no physical NFS qualification; evidence candidate-native-version.json |
| 2026-10-18T10:32:22.847039+00:00 | C01 | Started | Not Tested | Final owned cleanup/source/Delivery preservation; reverify new retained candidate, historical old candidate member hashes only. |
| 2026-10-18T10:39:22.679066+00:00 | C01 | Completed | Pass | Recorded after interruption from completed final-checks.json at 2026-10-18T10:32:46.929421+00:00;120source/1186protected inputs unchanged, temporary scratch absent,19file candidate reverified and retained, old candidate preserved. No runtime rerun. |
