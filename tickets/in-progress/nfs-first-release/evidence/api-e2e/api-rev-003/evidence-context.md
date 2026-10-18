# Evidence context — API003

Step: read completed API003 prepublication evidence. Source/workflow `585d416c2746cf2963058d591b0753d0db8088f5`, product850dfeb, execution2026-10-18UTC. Environments L/H/A and cases R01–R05/C01 are defined in the canonical execution report. This reader guide was written 2026-10-18T10:40:08.210765+00:00; it is not another test run.

## Read in this order
1. Report Cases and Acceptance-Criteria Proof distinguish current proof from downstream actual release gates. `prepublication-result.json` is a concise actual-check summary, **not a populated readiness lock or final release receipt**.
2. R01/R02: `release-control-excerpt.log` → full local logs / local-results.json + local-control-results.json. Original unsupported recipe command exit2 remains; `attempts.md` explains correction. No failed output erased. Focused7/12 overlap full45; one expected standalone Go-child skip.
3. R03: hosted-final.json + hosted-execution-summary.json and four hosted-excerpt-*.log. The ten full hosted-job-*.log captures are alongside them; hosted-log-index.json binds exact job URL/raw-body hashes. Actual run39118784695/1, native4 plus engine2/wholeOCI/aggregation complete; publisher/payload intentionally skipped.
4. R04: candidate-reference.json + actual-candidate.json establish real wrapper/record identity. candidate-validation-results.json contains exact facade argv/exit expectations, candidate-control-excerpt.log the refused cases, actual-envelope-refusal.json the real API pre-download rejection. candidate-metadata-diff.json proves alias-only change, not registry access.
5. R05: candidate-native-version.json includes actual binary/archive hashes, OS, exact stdout/stderr, three strict refusal results and absent owned HOME. candidate-native-version.log is version output. The Python probe gives exact admission steps.
6. C01: final-checks.json and final-candidate-verify.log show completed final integrity/cleanup; candidate-local-retention.json says what intentionally remains for Delivery. Old API002 candidate is preserved but stale for changed R3 production.

## Formats / provenance
Logs have context headers, exact commands, and original output. `evidence-annotations.json` records only the body digests/offsets of files annotated after capture; original bodies are unchanged. It is not an incoming-package inventory. Hosted headers were added by the collector with raw hashes in hosted-log-index.json. Existing run-specific Python scripts remain evidence, not durable product tests.

JSON candidate/envelope/reference records and API response captures deliberately retain valid exact machine-readable schemas; prepending prose or adding fields would corrupt the actual evidence or strict reader contract. Their context is the Cases table, this guide and companion command log. Recheck exact source/run/attempt/field values, not only booleans. Synthetic fixture readiness/Apple inputs are never used as actual authority.

## Known limits
No real Apple signing/notarization, public registry copy, public released install or main finalization here. No physical/shared-filesystem/user qualification. All four native hosted suites ran; native Go logs are nonverbose, so individual test counts/skips are not fabricated. Source-review/mutation evidence from earlier owners is attributed, not counted as this run. Final binary metadata/signature differences still require Delivery's actual final checks.
