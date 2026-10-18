# IR003 — local checks and limits

Basis R3/SR004 Approved / SR004 Ready / ARCH002 Pass. This is implementation
validation, not API/E2E sign-off or publication/field qualification.
Source commit 3d2710b30ec1a8106faeb2f7c4f2e70183a25cd3; default-null-engine/readiness
source hash d75c50c83a5848d45209e85511f271f36d5d99362fd87f41b8e24263203591ac.
The future measured engine participates in the real candidate's hash.

## Executed

- Independent non-ticket source copy under owned APFS development scratch, private
  HOME/TMPDIR/Go caches; no sibling repo, token forwarding or live storage setup.
  source-inputs.json/final-source-inputs.json identify 120 source/docs/test
  inputs; the historical119 count is not reused.
- Native macOS26.5.2 arm64, Go1.27.2: `go test -race ./...` (seven tested packages),
  `go vet ./...`, native build and explicit version; all pass. Focused final
  `go test -race ./internal/cli -run 'TestRelease|TestEngineIdentity' -v` also passes:
  schema/legacy/unknown/duplicate/status/target/source/engine/size/link refusal,
  successful stderr notice, exact version stdout and preserved additive host decode.
- CGO-disabled compile for darwin-arm64/amd64 and linux-arm64/amd64 passes. This
  does NOT execute amd64 targets or claim four-native runtime coverage.
- Python `/usr/bin/python3` 3.9.6: final45 collected,44 executed,1 explicit Go-child
  skip. Native Go's platform parent executes that bootstrap permission child.
  Go-child's PATH resolves Homebrew Python3.14.2. The tool-versions log's unqualified
  python3 is this PATH version, not the direct `/usr/bin/python3` suite interpreter.
- Native Ubuntu24.04 arm64 in two consecutive owned nonprivileged Docker local
  check containers; no socket, privileged mode, daemon mutation or host mount/export.
  Read-only archives extracted onto guest filesystem, nonroot checker uid1001.
  Final Python45 collected,42 executed,3 explicit container/Go-child skips;
  seven-package Go race, vet, build/version pass. Linux native execution is a
  shared-kernel container local check, not a separate physical/independent NFS host.
- actionlint1.7.11 both workflows, Bash syntax and shellcheck0.11.0 installer/signing;
  executable native-prefix regression on actual `/bin/bash`3.2.57; all pass.
  Target environment strings in shell fixtures are not architecture execution.
- Current null-readiness `--check-publish` refuses with exit1 as expected; source
  hash computed with current production. No synthetic record entered real lock.
- Eight mutations all detected by failed test assertions (not import/build errors):
  release-first approval revision, source applicability, false field claim, removed
  notes disclosure, false provenance status, missing engine-reset, accepted legacy
  runtime claim, false runtime schema/status. See mutations.json and raw logs.
- Source audit: current inputs, permitted file scope, unchanged host safety owners,
  license/CLA/notices/pins, source-size/delta guardrails, no generated assets,
  and all16 protected Delivery files. Exact counts/list in source-audit.json.

## Sequence / attribution

Initial42-test worktree check passed. Added explicit engine reset and semantic
payload controls: second44 passed. Independent initial Mac/Linux44 checks passed.
After adding a removed-flag control and strengthening happy-final-metadata/reset
assertions in three test files, final45 suites passed on Mac/Linux; no production
change in that increment (final-test-delta.json). The only subsequent production
edit was `candidate.fetch` docstring Qualification→Readiness. Current45 Python
suite and source hash rerun; native Go/Linux behavior evidence carries unchanged
executable bytes/semantics (final-comment-delta.json). No failed product/test
attempt occurred in IR003; mutation failures are intentional sensitivity checks.
Earlier IR001/IR002/API failures remain in their original history, not erased.

## Not executed / retained requirements

No Actions dispatch, real candidate engine build, signing-secret access, Developer
ID import, Apple notary request, registry/publication effect, target merge/push,
public download or installer against live released bytes. Fixtures use synthetic
engine/native/OCI/check/approval records and fake remote/signing boundaries.
Native tests do not exercise actual mounted NFS or user storage. Readiness parser
checks shape/content applicability, not the truth of evidence; human review remains.

API002 Blocked73.57 and run39113335636/1/artifact12131531399 remain historical.
The retained /Users/normy/nfs-first-candidate-api002-n940gd8s/candidate is untouched.
New production requires NEW complete current-source hosted candidate and affected
API result. All four targets, both Mac Developer ID + Accepted notarization, exact
engine/whole OCI, retained final payload, immutable same-byte retry, fresh main and
public-download verification remain. Field/physical/user testing is DEFERRED by
R3, not a publication/closure prerequisite; Delivery carries postpublication plan
to terminal SD/requesting PM. No credentials should be re-provisioned without an
actual validation failure. No release, user verification, TaskDone or Terminal claim.

## Evidence hygiene

Logs are unmodified command output. Raw Linux apt/dpkg progress includes CR-based
trailing whitespace; explicit diagnostic exception applies only to linux-checks.log
and initial-linux/linux-checks.log. No secrets/credentials or generated binaries
are included. Own scratch removed after identities captured (cleanup.json);
no other owner's scratch, API candidate, canonical repo or Delivery files removed.
