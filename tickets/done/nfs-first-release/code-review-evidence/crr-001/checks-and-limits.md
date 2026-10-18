# CRR-001 evidence map and limitations

## Inputs and scope

- `input-audit.json`: exact input/base/source commits,119 non-ticket file SHA256s,775 protected preexisting ticket SHA256s,26 changed non-ticket paths,11 implementation source-size rows and empty AST unused-import candidates.
- `checks-result.json`: exact independent-copy argv, timings and expected exits. Clean private HOME/TMPDIR; source in owned local APFS development path, not a protected runtime-source location. No prerequisite install or network mutation.
- `python.log`: Python38 tests collected,37 executed,1 standalone Go-child skip, all executed passed. Real local parsers/files/archives and fake external/signing boundaries; not hosted/native-user qualification.
- `actionlint.log`, `shellcheck.log`, `bash-syntax.log`: successful static checks. `tools-and-signing-syntax.json` additionally records the separately parsed signing script (bash treats later arguments as script arguments), macOS26.5.2 arm64, actionlint1.7.11, ShellCheck0.11.0. `python-version.log` records Python3.14.2.
- `source-hash.log`:8c1bcc13194f919c41cf4de9ad825a48acb4281bd558374ac77cbb1426820bac is the empty-lock/unqualified identity, NOT a measured-engine candidate.
- `publish-refusal.log`: expected exit1, exactly all four qualified targets required. No public effect.
- `cleanup.json`: owned scratch removed;119 source/775 existing ticket hashes unchanged at cleanup. `scratch-path.txt` is a historical identity, not a surviving resource.
- `primary-contracts.md`: primary GitHub/skopeo contracts consulted read-only.
- `final-checks.json`: final source/protected-artifact/record/whitespace checks before handoff. `routing.json`: fresh routing authority and selected exact recipient. Receipt stored after delivery.

## Attribution and limits

IR001 `final-checks.json`, `checks-and-limits.md`, `mutations.json`, `attempts.md` and linked logs retain implementation-native Go/race/vet/build, four-target compilation, synthetic OCI real skopeo and corrected harness evidence. Reviewer did not repeat these unchanged-Go checks or count them as new API/hosted/physical executions. Independent current Python/static checks above passed with no failed reviewer execution.

Six secrets are provisioned, not signing-qualified. Actual candidate/native hosted jobs, target/mode/independent physical/user evidence, real Mac import/sign/notary, exact public OCI/assets/downloads and Delivery current-main/finalization gates remain. No scope waiver, live resource use, source/test edit, CI dispatch, target merge/push, tag/release, registry write, TaskDone or user-verification claim.
