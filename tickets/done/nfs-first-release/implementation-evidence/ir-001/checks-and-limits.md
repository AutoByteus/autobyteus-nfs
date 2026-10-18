# IR-001 — implementation checks and limits

## Exact input and scope

Source commit `886b55e1cf88f3f696334bd5e7b8c374946a594d`, from reviewed
`2051fd9559f4f4fa7beae68723429f8199b50004`, branch `codex/nfs-first-release`.
R2/SR002 Approved, SR003 Ready, ARCH-REV-001 Pass; Large/High unchanged.
No target merge/push, hosted dispatch, signing credential access, registry push,
release/tag, live service setup, storage/mount/node mutation, or delegation.

`source-inputs.json` / `final-source-inputs.json` match the complete final independent
source copy and the archive extracted into the Linux guest. `source-audit.json`
records exact preserved runtime/engine/license inputs and changed paths. Default
source hash `8c1bcc13194f919c41cf4de9ad825a48acb4281bd558374ac77cbb1426820bac`
uses **engine=null**; it is not a real candidate hash or qualification.

## Current local results

| Check | Result / precise boundary | Evidence |
| --- | --- | --- |
| Independent macOS26.5.2 arm64 Go1.27.2 race/vet/build/version | All7 tested packages pass; version development-unqualified | checks-result.json, go-race.log, go-vet.log, go-native-build.log, native-version.log |
| Independent native Python3.9.6 suites | 38 collected,37 executed,1 Go-child-only skip; child exercised by native Go bootstrap fixture | python.log |
| Ubuntu24.04 arm64 guest, Go1.27.2/Python3.12.3 | All7 race packages, vet/build/version pass; Python38 collected35 executed3 explicit skips (two installer/container cases, one Go-child entry); no host installer qualification | linux-checks.log, linux-checks-result.json |
| Four-target CGO-disabled builds | darwin/linux × arm64/amd64 compile; only local arm64 binaries executed | compile-*.log, compile-identities.json |
| Workflow/shell | actionlint1.7.11, bash syntax, shellcheck pass | actionlint.log, bash-syntax.log, shellcheck.log |
| Default publish refusal | Exit1, no qualified release targets; expected | publish-refusal.log |
| Record/adversarial fixtures | Strict versions/JSON/path/size; exact engine/OCI/native/member hashes; source/workflow invalidation; run/attempt/expiry envelope; evidence mode/user checks; final payload/signature/checksums | python.log, scripts/tests/test_nfs_release_records.py |
| Publication fixtures | Actual record parsers with doubled GH/registry: exact tag/main, draft normal/verify-tag, no-clobber assets, failed-stage retry and original-payload reuse/expiry refusal, all-child anonymous transport flags | test_nfs_release_publication.py, python.log |
| Signing fixtures | Actual shell, fake commands/credentials: six missing/placeholder inputs, import/sign/verify/notary failure, Accepted-only and owned cleanup | test_nfs_release_signing.py, python.log |
| Real OCI transport | Nonroot skopeo1.13.3 copies synthetic two-platform verified layout with --all --preserve-digests; parsed index and both child digests identical after copy | linux-checks.log, input-oci.json, copied-oci.json |
| Six deliberate scratch mutations | Each detected by exactly one assertion failure; no test errors: user consent, OCI blob hash, executed workflow, preserve-digests, fresh main, Accepted notary | mutations.json, mutation-*.log |
| Scope/dead imports/size | Runtime/engine recipe and pins/licenses/ordinary CI unchanged; no unused touched Python import binding; implementation files ≤358 nonempty lines | source-audit.json, audit-source.py |

Fixtures use inert/synthetic native/engine/OCI bytes and mocked external effects;
none is proof of a real engine build, physical/independent-client test, Apple
acceptance or GitHub publication. Native race checks read only owned test paths;
there was no old filesystem/editor/provider campaign. Linux is a Docker Desktop
arm64 guest with native guest filesystem, not a physical host; amd64 is compile
only. No historical retained engine was consumed or modified.

## Local corrections and preservation

`attempts.md` and raw attempt directories retain all failures. First native source
copy was under protected /private; the guard refused it. First Linux copy used
host-bridged flock and failed its safety fixture. Moving owned test sources to
proper APFS/guest filesystems fixed the harness, not runtime guards.

The second Linux run reached real nonroot skopeo: its OCI-archive reader attempted
chown of root-owned tar entries. Production now verifies the full archive then
copies identical file bytes into an owned OCI layout before skopeo transport.
No root workaround, image rebuild/recompression or weakening of digest preservation.
Third Linux attempt proved that correction. Current final run repeats it after the
small final source-summary addition and unused test-import cleanup.

Intermediate `python-final.log` and `final-check-delta.json` retain their original
snapshot meaning; **current** results are python.log/checks-result.json,
linux-checks-result.json, mutations.json and final-checks.json. No old result was
silently promoted to the final input. Raw duplicate-ZIP warning is intentional.

## Self-review and remaining work

The size-pressure signal (>220 changed lines) was assessed: candidate retains one
cohesive artifact/run-verification owner, publication one external effect owner;
final payload assembly/verification was split into payload.py. Identity,
qualification, facade and signing stay separate. No generic workflow framework,
legacy publisher/fallback or runtime/schema change was added. AST import audit is
narrow, supplemented by manual path/owner inspection, not a whole-repo linter.

API must independently review/exercise the new tests, hosted candidate identity,
actual four-target checks, exact measured engine and complete OCI, applicable
physical Mac/Linux/Docker and genuine user evidence. All six secrets are provisioned
but import/password/team/Accepted-notary are not validated. Delivery owns evidence
sufficiency, current main integration, scoped GHCR visibility, final signed payload,
same-payload partial recovery and real public downloads/signatures/install smoke.
Qualification remains empty. This handoff is **not** AC001–008 acceptance, TaskDone,
user verification, source finalization, deployment or release.

Cleanup: see cleanup.json; exact owned containers and both scratch roots removed.
Shared base image cache, canonical checkouts, PM files, old assets and upstream
artifacts preserved. No owned process/resource needs downstream cleanup.

Raw-log hygiene exception: four Linux apt/dpkg command logs retain terminal CR
line endings byte-for-byte. whitespace-audit.json enumerates exact paths/counts
and hashes; all other staged artifacts pass git diff --check. No source formatting
exception. The temporary whitespace diagnostic output was removed after audit.
