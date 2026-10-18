# API/E2E case ledger — nfs-first-release

API-REV-001 reconciled result: Fail62.86%. Initial plan preceded execution; events below preserve checkpoints. D01/D02 downstream-owned, not silently waived. 50planned cases:3Pass/1Fail/43Blocked/3NotTested; supplements are not extra unique cases.

| Case | Expected | State | Evidence |
|---|---|---|---|
| R01 | Current release/control/installer fixtures pass | Pass — local only | local-results.json, python-all.log |
| R02 | Static/hash/refusal plus native Go and real CLI preflight | Pass — local only | local-results.json, native-results.json, prepare-results.json |
| R03 | Exact hosted candidate: two engine arches/whole OCI/four native targets | Fail | hosted-final.json, hosted-log-index.json |
| R04 | Fetch/verify complete actual candidate | Blocked — no candidate artifact after R03 failure | hosted-final.json |
| Q01-01 | Q01 mode/operation01 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q01-02 | Q01 mode/operation02 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q01-03 | Q01 mode/operation03 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q01-04 | Q01 mode/operation04 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q01-05 | Q01 mode/operation05 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q01-06 | Q01 mode/operation06 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q01-07 | Q01 mode/operation07 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-01 | Q02 mode/operation01 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-02 | Q02 mode/operation02 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-03 | Q02 mode/operation03 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-04 | Q02 mode/operation04 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-05 | Q02 mode/operation05 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-06 | Q02 mode/operation06 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q02-07 | Q02 mode/operation07 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-01 | Q03 mode/operation01 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-02 | Q03 mode/operation02 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-03 | Q03 mode/operation03 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-04 | Q03 mode/operation04 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-05 | Q03 mode/operation05 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-06 | Q03 mode/operation06 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q03-07 | Q03 mode/operation07 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-01 | Q04 mode/operation01 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-02 | Q04 mode/operation02 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-03 | Q04 mode/operation03 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-04 | Q04 mode/operation04 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-05 | Q04 mode/operation05 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-06 | Q04 mode/operation06 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q04-07 | Q04 mode/operation07 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-01 | Q05 mode/operation01 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-02 | Q05 mode/operation02 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-03 | Q05 mode/operation03 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-04 | Q05 mode/operation04 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-05 | Q05 mode/operation05 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-06 | Q05 mode/operation06 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q05-07 | Q05 mode/operation07 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-01 | Q06 mode/operation01 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-02 | Q06 mode/operation02 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-03 | Q06 mode/operation03 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-04 | Q06 mode/operation04 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-05 | Q06 mode/operation05 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-06 | Q06 mode/operation06 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| Q06-07 | Q06 mode/operation07 per investigation | Blocked — no complete candidate/assigned disposable pair | hosted-final.json; inventory.json |
| U01 | Genuine user execution against identified candidate | Not Tested | No usable candidate; no user-test receipt |
| D01 | Delivery final signing/publication/recovery | Not Tested | Downstream gates; publisher skipped |
| D02 | Final public downloads/receipts | Not Tested | No release; post-run-remote.json |
| C01 | Owned cleanup/source preservation | Pass | cleanup-local.json; mac-array-reproduction.json; final-checks.json |

## Execution events
| UTC | Case | Result/checkpoint | Evidence |
|---|---|---|---|
| 2026-10-18T08:20:17.707690+00:00 | R01 | Pass checkpoint | python-version.log |
| 2026-10-18T08:20:19.890070+00:00 | R01 | Pass checkpoint | python-release_records.log |
| 2026-10-18T08:20:22.423323+00:00 | R01 | Pass checkpoint | python-release_publication.log |
| 2026-10-18T08:20:29.742880+00:00 | R01 | Pass checkpoint | python-release_signing.log |
| 2026-10-18T08:20:29.970246+00:00 | R01 | Pass checkpoint | python-release_workflow.log |
| 2026-10-18T08:20:34.110070+00:00 | R01 | Pass checkpoint | python-installer_fixture.log |
| 2026-10-18T08:20:49.893750+00:00 | R01 | Pass checkpoint | python-all.log |
| 2026-10-18T08:20:50.079163+00:00 | R02 | Pass checkpoint | actionlint.log |
| 2026-10-18T08:20:50.090873+00:00 | R02 | Pass checkpoint | installer-syntax.log |
| 2026-10-18T08:20:50.102016+00:00 | R02 | Pass checkpoint | signing-syntax.log |
| 2026-10-18T08:20:50.235435+00:00 | R02 | Pass checkpoint | shellcheck.log |
| 2026-10-18T08:20:50.524533+00:00 | R02 | Pass checkpoint | source-hash.log |
| 2026-10-18T08:20:50.805840+00:00 | R02 | Pass checkpoint | publish-refusal.log |
| 2026-10-18T08:20:50.806062+00:00 | R01 | Pass LOCAL fixtures only; 38collected/37executed/1Go-child skip; narrow counts overlap broad | python-all.log |
| 2026-10-18T08:20:50.806119+00:00 | R02 | Pass LOCAL static/hash/default refusal; no measured-engine identity or host/CI qualification | local-results.json |
| 2026-10-18T08:21:19.348681+00:00 | R02-native | Pass checkpoint | go-download.log |
| 2026-10-18T08:21:22.230528+00:00 | R02-native | Pass checkpoint | go-extract.log |
| 2026-10-18T08:21:23.126768+00:00 | R02-native | Pass checkpoint | go-version.log |
| 2026-10-18T08:21:43.471668+00:00 | R02-preflight | Pass valid | prepare-valid.log |
| 2026-10-18T08:21:43.719109+00:00 | R02-preflight | Pass old-workflow | prepare-old-workflow.log |
| 2026-10-18T08:21:43.960611+00:00 | R02-preflight | Pass wrong-event | prepare-wrong-event.log |
| 2026-10-18T08:21:44.178307+00:00 | R02-preflight | Pass beta | prepare-beta.log |
| 2026-10-18T08:21:44.434115+00:00 | R02-preflight | Pass non-main-publish | prepare-non-main-publish.log |
| 2026-10-18T08:21:51.242287+00:00 | R02-native | Pass checkpoint | go-race.log |
| 2026-10-18T08:21:56.958008+00:00 | R02-native | Pass checkpoint | go-vet.log |
| 2026-10-18T08:21:57.356230+00:00 | R02-native | Pass checkpoint | go-build.log |
| 2026-10-18T08:21:58.285166+00:00 | R02-native | Pass checkpoint | native-version.log |
| 2026-10-18T08:22:21.974847+00:00 | R03 | Pending prerequisite: reviewed ref absent remotely; Delivery-owned staged availability requested, no dispatch attempted against old workflow | inventory.json; remote-refs.log |
| 2026-10-18T08:22:21.974847+00:00 | Q01–Q06 | Pending host inventory: only live user Mac and existing unowned Docker application nodes found, no assigned physical test pair; no storage setup performed | inventory.json |
| 2026-10-18T08:22:51.087882+00:00 | R02-native | Pass native Darwin race7packages/vet/build/version; direct Go-child skip covered by parent; NOT physical NFS/hosted proof | native-results.json, test-counts.json |
| 2026-10-18T08:22:51.087882+00:00 | C01-local | Pass local owned scratch/toolchain/cache cleanup;119inputs preserved; reviewer routing receipt appended externally, not restored | cleanup-local.json |
| 2026-10-18T08:25:01.519498+00:00 | R03 | Running hosted build-only run 39111348848 attempt 1; dispatch accepted NOT Pass | dispatch-receipt.json |
| 2026-10-18T08:26:50.548134+00:00 | R03 | Hosted checkpoint in_progress/None; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-001.json |
| 2026-10-18T08:27:21.908811+00:00 | R03 | Hosted checkpoint in_progress/None; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-002.json |
| 2026-10-18T08:27:53.462192+00:00 | R03 | Hosted checkpoint in_progress/None; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-003.json |
| 2026-10-18T08:29:59.426872+00:00 | R03 | Hosted checkpoint queued/None; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-007.json |
| 2026-10-18T08:30:31.154036+00:00 | R03 | Hosted checkpoint in_progress/None; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-008.json |
| 2026-10-18T08:31:02.986467+00:00 | R03 | Hosted checkpoint in_progress/None; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-009.json |
| 2026-10-18T08:31:34.553157+00:00 | R03 | Hosted checkpoint completed/failure; completed job conclusions retained; no run Pass inferred | hosted-checkpoint-010.json |
| 2026-10-18T08:32:14.088624+00:00 | R03 | Fail exact run39111348848/attempt1: both Mac native checks fail; both Linux native jobs/engine pair/OCI pass; candidate/payload/publish skipped. No forced cancellation or reduced matrix. Investigating original logs. | hosted-final.json |
| 2026-10-18T08:32:50.270992+00:00 | R03-F001 | Reproduced candidate empty-array exit1 before command entry on system Bash; fresh-mode nonempty control exit0. No fix. | mac-array-reproduction.json |
