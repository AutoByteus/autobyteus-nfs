Check: IMP-05-08
Command/steps: Four disposable mutations of signing boundary, exact commands in implementation-evidence/ir-005/checks-result.json
Commit tested: 75f4dbe5527a7159f536bafcf9448bc2d6a01604 (identical uncommitted source tree at b2c6fdf; committed after checks)
Environment: Darwin arm64; Bash3.2.57; Python3.9.6; independent private HOME/TMP where stated
Recorded UTC: 2026-10-18T11:10:49.946492+00:00

All four returned expected exit1; full logs in IMP-05-08-mutations.log.
- Hidden safe stderr: assertion cannot find Signing failed stage line.
- Function called as conditional: original import failure no longer preserved.
- Failed keychain-list capture restored: assertion finds forbidden restore call.
- Invalid/pending notary accepted: three status subtests reject unexpected success.
These are detected negative controls, not actual signing failures.
