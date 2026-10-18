# Finalization and release

## Source finalization

Target `origin/main`; use `codex/<ticket>` in the task worktree, not the canonical
checkout or another owner's worktree. Fetch immediately before finalization and
compare the remote main with the base actually integrated. Merge reviewed changes
with `--no-ff` on a fresh finalize branch, run affected integrated checks and record
ticket/target commits and remote confirmation. Never force push/reset or overwrite
competing work. NFS is independent: no paired application merge or desktop version.
Preserve PM `task-plans/`, archives and retained historical assets byte-for-byte.
Archive evidence and clean only owned scratch/worktrees after durable receipts.

## Publication authorization

Source finalization alone does **not** authorize publication or deployment. The
`nfs-first-release` task explicitly authorizes the first **normal v0.1.0** release
once its existing readiness gates are met. Normal `vMAJOR.MINOR.PATCH` only; no
beta/prerelease or build suffix. The manual workflow defaults to build-only and
ordinary push/PR checks never publish. Do not pre-create a version tag or release.

[packaging/RELEASE.md](packaging/RELEASE.md) owns candidate identity, release readiness,
signing, retained final payload and publication/recovery procedure. API/E2E owns
executable evidence; Delivery judges sufficiency, records audited readiness, finalizes
current main, executes the authorized release and verifies public receipts. A
build, source-review Pass, configured secret or permission to release is **not**
independent physical testing, actual user verification or Accepted notarization.
The user explicitly requests signed v0.1.0 **before** field/user testing; those
tests are deferred, not passed and not publication/closure prerequisites. Retain
current native/release-control/source-review checks, real signing/notary, exact
payload integrity and public download checks. Delivery transfers the scoped
postpublication test/fix-forward plan via terminal Solution Designer to the
requesting PM, without a prepublication host questionnaire.

Staged source finalization may be needed to exercise the hosted workflow. It does
not complete the Task: actual normal release, exact public downloads and truthful
distribution/signature receipts and explicit deferred field/user-test custody are required. Any concrete external prerequisite
keeps the release open. Do not silently drop a target or weaken a gate.

## Partial effects and cleanup

Publication is non-atomic. Preserve tag/draft/image/assets and failed-run evidence.
Retry resolves the annotation-bound original payload before building/signing;
never clobber an asset, move/delete a published tag, rebuild a bound engine or
re-sign under an existing payload identity. Missing/expired/conflicting inputs
block automatic recovery; a different output needs a newly authorized version.
A scoped package-visibility permission failure leaves the release draft, not Pass.

No live-user setup, storage migration, node upgrade, application Guide activation
or deployment is implied. Do not delete user configuration/source data or claim
rollback of a publication. Clean only this task's ephemeral resources/credentials;
retain artifacts through readiness and recovery. Return actual URL/version,
source/tag/run/attempt/artifact/image identities, supported targets and exact
commands, or the precise unfinished stage and preserved partial effects.
