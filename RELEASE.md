# Finalization and release

## Repository finalization (no release by default)

Target is `origin/main`; task branches use `codex/<ticket>`. Work in the task
worktree, not the user canonical checkout or another owner's dirty checkout.
Before each target push, fetch origin and compare the current remote main with
the base actually integrated. Never force push/reset, overwrite competing work,
or assume a previously empty remote is still empty.

For this repository's initial reviewed history, establish main from the validated
task branch only after confirming remote main is absent. Do not invent an empty
base or merge unrelated history. If main has appeared, reconcile actual ownership
and commits first; report a concrete blocker rather than overwriting it.
Subsequent reviewed changes merge with `--no-ff` into a fresh finalize branch from
origin/main. Record ticket/target commits and remote confirmation.

The extraction spans two repositories. Validate paired candidates first; establish
this repository's main, then finalize the application's filesystem-only decoupling
under that repository's `origin/personal` / `--no-ff` policy. If the second step
fails, report partial finalization and preserve the first; never force rollback.
Only after remote finalization may the canonical still-unborn main be populated
with normal non-force checkout/tracking, after checking new owner content.
Preserve `task-plans/` and all unrelated files byte-for-byte. Do not author there.
Archive evidence and clean only owned scratch/worktrees after durable receipts;
canonical checkouts and retained historical candidates are not disposable.

## Publication and rollout

**No release** is the default. Finalizing source does not authorize a tag,
GitHub release, image push, signing operation, installer publication or deployment.
There is no automatic tag/main publication workflow. A future explicitly
approved NFS release owns its version/tag independently from AutoByteus desktop.
The maintainer must separately authorize/create the tag and existing GitHub
release before a publish dispatch; the workflow does not create either.

[packaging/RELEASE.md](packaging/RELEASE.md) defines the exact candidate reuse,
service/engine/host evidence, physical/user qualification, signing and
existing-release gates. `workflow_dispatch` defaults `publish=false`. Do not
enable the app's unavailable Guide from build-only artifacts. No live rollout
is implied by extraction. Preserve installed paths/data; any later supported
upgrade transition needs its own evidence and plan. Never move a published tag
or relabel failed/unqualified evidence as a release result.
