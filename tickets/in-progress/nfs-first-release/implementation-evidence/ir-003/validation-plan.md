# IR003 implementation check scope

R3/SR004 / ARCH002 replaces release qualification with explicit release-first
readiness; Large/High retained. No actual authorization/readiness is written.

- Independent source snapshot, private HOME/TMPDIR/caches. Native macOS arm64
  Go1.27.2 race/vet/build/version and Python stdlib fixtures; actionlint, Bash3.2
  invocation regression, syntax/shellcheck, null-readiness refusal and source hash.
- Native Ubuntu24.04 arm64 checks in an owned nonprivileged Docker container with
  source extracted on guest filesystem; no host socket/live mounts/NFS. Container
  installer skips remain explicit, not host-install qualification.
- Four CGO-disabled compilation targets, distinct from native execution.
- Focused mutations of readiness/source applicability, semantic deferral,
  engine-reset, CLI legacy/unknown/status admission and installer invocation.
  Executable parser fixtures preserve engine/OCI/signing/immutable retry controls.
- Actual current hosted candidate and signed public payload/download proof remain
  API/Delivery-owned; old API002 candidate/history untouched. Field/physical/user
  tests are deferred by R3, not pass or publication/closure prerequisites.
- Protected Delivery files are hash-audited before/after. No app/UI, credentials,
  remote write, live storage or historical evidence edit is in these local checks.
