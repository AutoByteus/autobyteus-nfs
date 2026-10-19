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

## API-REV-004 — IR005/CRR007 continuation

| Time | Case ID | Event | Result | Note |
|---|---|---|---|---|
| 2026-10-19T05:06:01.402893+00:00 | R01 | Started | Not Tested | Read IMP Checks Run; compare exact tested input before reuse, no duplicate product run. |
| 2026-10-19T05:06:31.493191+00:00 | R01 | Completed | Pass | Reused exact current IMP-05-01/02/08/09; all127 inputs unchanged; no duplicate product check. |
| 2026-10-19T05:06:31.493208+00:00 | R02 | Started | Not Tested | Reuse clear IMP-05-03–07; additionally execute actual old-candidate refusal (missing-input control did not cover it). |
| 2026-10-19T05:07:13.569662+00:00 | R02 | Completed | Pass | IMP-05-03–07 reused; actual old API003 candidate refused by current workflow binding, exit1; no product change. |
| 2026-10-19T05:07:13.569662+00:00 | R03 | Started | Not Tested | Delivery-owned reviewed remote staging requested; not dispatched against old remote bytes. Prepare exact build-only run. |
| 2026-10-19T05:07:35.662260+00:00 | R03 | Checkpoint | Not Tested | Dispatched exact source44e2487b4b30da99797c149c17fa0c8bcaa6a87f, run39202907777/attempt1; acceptance is not Pass. |
| 2026-10-19T05:07:39.098576+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:08:10.325891+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:10:15.872883+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:10:47.379584+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:12:53.758109+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 queued/None; R03-04-observations.jsonl |
| 2026-10-19T05:13:25.200898+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:14:28.298727+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:14:59.840674+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:16:35.256607+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 in_progress/None; R03-04-observations.jsonl |
| 2026-10-19T05:17:07.127932+00:00 | R03 | Checkpoint | Not Tested | Run39202907777/1 completed/success; R03-04-observations.jsonl |
| 2026-10-19T05:18:00.814569+00:00 | R03 | Completed | Pass | Actual run39202907777/1;10success/2intended skips; native4 logs verified, no public effects. R03-04-summary.json. |
| 2026-10-19T05:18:00.941664+00:00 | R04 | Started | Not Tested | Fetch and verify unique actual current candidate via existing facade, not old-source metadata. |
| 2026-10-19T05:18:35.204776+00:00 | R04 | Completed | Pass | Actual complete candidate/reference verified; corrupt copied envelope refused before destination; retained for Delivery; R04-04-verification.json. |
| 2026-10-19T05:19:29.651512+00:00 | R05 | Started | Not Tested | New downloaded native Darwinarm64 version/candidate admission; owned HOME, no setup. |
| 2026-10-19T05:19:30.311820+00:00 | R05 | Completed | Pass | Exact v0.1.0 stdout; candidate admission refused, no HOME writes; scratch removed. R05-04-smoke.json. |
| 2026-10-19T05:19:39.410383+00:00 | C01 | Started | Not Tested | Reverify new retained candidate, preserve old candidate members and Delivery-owned files; no local-notary diagnostic access. |
| 2026-10-19T05:19:40.610153+00:00 | C01 | Completed | Pass | Current candidate reverified;127 source unchanged, Delivery10 files excluded, old candidates preserved, native scratch removed; C01-04-cleanup.json. |

## API-REV-005 — IR006/CRR009 diagnostic source continuation

| Time | Case | Event | Result | Note |
|---|---|---|---|---|
| 2026-10-19T06:14:21.984099+00:00 | R01 | Started | Not Tested | Read IMP Checks Run and DR009 failed receipts first; compare exact current product before reuse. |
| 2026-10-19T06:14:57.206451+00:00 | R01 | Completed | Pass | IMP06 exact127input applicability confirmed; R01-05-reuse.json. Reused, not rerun. |
| 2026-10-19T06:14:57.206650+00:00 | R02 | Started | Not Tested | Reused03–08/11; actual old API004 candidate admission additionally exercised. |
| 2026-10-19T06:15:10.642226+00:00 | R02 | Completed | Pass | Actual old API004 refused Candidate source/engine differs; reused static/current controls. |
| 2026-10-19T06:16:25.663122+00:00 | R03 | Started | Not Tested | DR010 staged exact1c00; new publish=false candidate, not signing/root-fix proof. |
| 2026-10-19T06:16:34.962770+00:00 | R03 | Checkpoint | Not Tested | Dispatched exact source1c00b7afd6327fb4ba69dbc176c69d698a309fee, run39208967217/attempt1; acceptance is not Pass. |
| 2026-10-19T06:17:43.761273+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:19:17.828907+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:19:49.079457+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:21:55.081558+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 queued/None; R03-05-observations.jsonl |
| 2026-10-19T06:22:26.541794+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:23:30.312041+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:24:02.835247+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:25:37.373144+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 in_progress/None; R03-05-observations.jsonl |
| 2026-10-19T06:26:08.831197+00:00 | R03 | Checkpoint | Not Tested | Run39208967217/1 completed/success; R03-05-observations.jsonl |
| 2026-10-19T06:26:26.241545+00:00 | R03 | Completed | Pass | Run39208967217/attempt1 all4native/engine2/fullOCI/aggregation success; R03-05-summary.json. Signing not entered. |
| 2026-10-19T06:26:29.145595+00:00 | R04 | Started | Not Tested | Fetch and verify unique actual current candidate via existing facade, not old-source metadata. |
| 2026-10-19T06:27:18.670906+00:00 | R04 | Completed | Pass | Actual complete candidate/reference verified; corrupt copied envelope refused before destination; retained for Delivery; R04-05-verification.json. |
| 2026-10-19T06:27:23.091108+00:00 | R05 | Started | Not Tested | New downloaded native Darwinarm64 version/candidate admission; owned HOME, no setup. |
| 2026-10-19T06:27:23.714102+00:00 | R05 | Completed | Pass | Exact v0.1.0 stdout; candidate admission refused, no HOME writes; scratch removed. R05-05-smoke.json. |
| 2026-10-19T06:27:23.758606+00:00 | C01 | Started | Not Tested | Final candidate verification/owned cleanup/source and Delivery preservation, no product suite repeat. |
| 2026-10-19T06:27:24.603467+00:00 | C01 | Completed | Pass | Candidate reverified;127 source inputs and Delivery10 files preserved; oldAPI002/003/004 untouched; owned native scratch absent. |
