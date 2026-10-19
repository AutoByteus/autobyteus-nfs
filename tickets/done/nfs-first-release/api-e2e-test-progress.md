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

## API-REV-006 — IR007/CRR011 keychain lookup repair

| Time | Case | Event | Result | Note |
|---|---|---|---|---|
| 2026-10-19T07:00:25.303572+00:00 | R01 | Started | Not Tested | Read Checks Run/prior failures first; exact product applicability and native mechanism limits. |
| 2026-10-19T07:02:31.425874+00:00 | R01 | Completed | Pass | IMP07 exact127input applicability confirmed; R01-06-reuse.json; reuse not product/keychain rerun. |
| 2026-10-19T07:02:31.425996+00:00 | R02 | Started | Not Tested | Reuse IMP07 static/hash/no-candidate controls; execute actual old API005 admission refusal. |
| 2026-10-19T07:02:31.689610+00:00 | R02 | Completed | Pass | Actual API005 source/engine mismatch refusal; no stale evidence promotion; static/hash controls reused. |
| 2026-10-19T07:02:50.228170+00:00 | R03 | Started | Not Tested | DR012 exact7bd486e staged; NEW publish=false all4native candidate, not actual signing/root-cause closure. |
| 2026-10-19T07:02:59.567102+00:00 | R03 | Checkpoint | Not Tested | Dispatched exact source7bd486e2e27743441a870f7cd8db1f6c4ee0b493, run39213489075/attempt1; acceptance is not Pass. |
| 2026-10-19T07:03:03.873731+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:03:35.327135+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 queued/None; R03-06-observations.jsonl |
| 2026-10-19T07:04:06.630915+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:05:41.005243+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:06:12.442834+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:08:18.434065+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 queued/None; R03-06-observations.jsonl |
| 2026-10-19T07:08:49.892855+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:09:52.804010+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:10:24.330704+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:10:55.733728+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:12:30.421569+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 in_progress/None; R03-06-observations.jsonl |
| 2026-10-19T07:13:02.064756+00:00 | R03 | Checkpoint | Not Tested | Run39213489075/1 completed/success; R03-06-observations.jsonl |
| 2026-10-19T07:13:19.265828+00:00 | R03 | Completed | Pass | Run39213489075/attempt1 all4native/engine2/fullOCI/aggregation success; R03-06-summary.json. Signing not entered. |
| 2026-10-19T07:13:25.879855+00:00 | R04 | Started | Not Tested | Fetch and verify unique actual current candidate via existing facade, not old-source metadata. |
| 2026-10-19T07:14:11.281190+00:00 | R04 | Completed | Pass | Actual complete candidate/reference verified; corrupt copied envelope refused before destination; retained for Delivery; R04-06-verification.json. |
| 2026-10-19T07:14:15.886473+00:00 | R05 | Started | Not Tested | New downloaded native Darwinarm64 version/candidate admission; owned HOME, no setup. |
| 2026-10-19T07:14:16.490900+00:00 | R05 | Completed | Pass | Exact v0.1.0 stdout; candidate admission refused, no HOME writes; scratch removed. R05-06-smoke.json. |
| 2026-10-19T07:14:16.532672+00:00 | C01 | Started | Not Tested | Final candidate/ownedcleanup/input/Delivery/history/oldcandidate preservation. |
| 2026-10-19T07:14:17.361475+00:00 | C01 | Completed | Pass | Candidate reverified;127inputs/Delivery10files preserved; oldAPI002–005 intact; owned native scratch absent. |

## API-REV-007 — SR005 bound executor recovery

| Time | Case | Event | Result | Note |
|---|---|---|---|---|
| 2026-10-19T08:43:24.199128+00:00 | R01 | Started | Not Tested | Checks Run/prior failure/DR013 signed success read first; exact130inputs reuse audit. |
| 2026-10-19T08:44:12.272438+00:00 | R01 | Completed | Pass | IMP09 exact applicability confirmed; no duplicate suite for independence. |
| 2026-10-19T08:44:12.272532+00:00 | R02 | Started | Not Tested | Current facade strict candidate and real tag-derived absent-authority refusal; no effects. |
| 2026-10-19T08:44:55.463279+00:00 | R02 | Checkpoint | Not Tested | Initial orchestrator expected later hash guard; actual workflow guard correctly refuses first. Preserve raw result; resume without repeating completed R01/CLI. |
| 2026-10-19T08:44:59.168446+00:00 | R02 | Completed | Pass | Current strict candidate/absent real authority refuse, GET-only; no authorization created. |
| 2026-10-19T08:44:59.168545+00:00 | R03 | Started | Not Tested | Carry API006 original product build/candidate by exact record/member identity; not new executor build. |
| 2026-10-19T08:45:01.488559+00:00 | R03 | Completed | Pass | Original API006 record/members/hash matchP; unchanged exact product evidence carries. |
| 2026-10-19T08:45:11.685039+00:00 | R04 | Started | Not Tested | Actual inspect-bound, new owned APFS path; exact envelopes/full P validators/jobs, no admission/effects. |
| 2026-10-19T08:45:58.846411+00:00 | R04 | Completed | Pass | Actual original envelopes/downloads/full P validators/job/signing proof; admission not performed. |
| 2026-10-19T08:46:16.439901+00:00 | R05 | Started | Not Tested | Carry DR013 actual Accepted/signatures by matching newly inspected original archives/binaries, no new signing. |
| 2026-10-19T08:46:16.570691+00:00 | R05 | Completed | Pass | Both original signed-byte proof exact; carried DR013 scope, not new Apple/public install. |
| 2026-10-19T08:46:16.570759+00:00 | R06 | Started | Not Tested | Fresh actual bounded inventory/direct-ID/tag/main/artifact/job GETs; current discovery known417014769. |
| 2026-10-19T08:46:24.212725+00:00 | R06 | Completed | Pass | Actual current list/directID fixes observed draft lookup; live retained job proof/expiry, no effects; run remains failed. |
| 2026-10-19T08:47:48.500483+00:00 | R07 | Started | Not Tested | Independent clone/current code/actual signed bytes; synthetic authority and all external writes locally emulated only. |
| 2026-10-19T08:48:27.870601+00:00 | R07 | Completed | Pass | Actual-byte complete current orchestration/admission with emulated effects; known-missing/excluded drift safeguards; no real authority/effects, clone removed. |
| 2026-10-19T08:50:20.394515+00:00 | C01 | Started | Not Tested | Fresh no-effect remote correlation, exact owned/retained bytes, source/history/other-owner preservation and cleanup. |
| 2026-10-19T08:50:23.819873+00:00 | C01 | Completed | Pass | Own inspection/clone removed; original signed payload/API002–006/source130/other-owner67files unchanged; actual remote main/tag/draft/assets unchanged; no real authority. |
