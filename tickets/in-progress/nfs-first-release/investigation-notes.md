# Investigation — First NFS release

## Meta / Bootstrap
- Package nfs-first-release; Task autobyteus-nfs-3 / project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5.
- Git isolated worktree /Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-first-release; branch codex/nfs-first-release.
- Fresh git fetch origin succeeded2026-10-18; resolved origin/main7e375984be2bea7a4d536e43cc59d6bc2b116870; finalization origin/main under repository policy.
- Canonical checkout has untracked task-plans; untouched. Prior extract checkout detached/retained; no reuse or archive changes.
- Authorities read in full: solution-designer SKILL; requirements-engineering; requirements/investigation/revision templates; N AGENTS/DESIGN/TESTING/RELEASE.
- Requirements investigation underway; architecture not started. Current SR N/A.

## Initial Request
PM forwarded explicit2026-10-18 user direction to enable releases analogous in usability to superrepo CI and publish first usable NFS release. Former extraction no-release choice is historical, not a permanent ban. User approval to publish is not runtime qualification or a user test. No dashboard or live storage upgrade authorized.

## Source log
E01: read incoming PM copy of extraction DR003 terminal receipt at /Users/normy/.autobyteus/server-data/projects/project_6416db5b-926a-4865-8705-d8ebb2425780/tasks/project_task_97c6ab09-83cb-46df-bf28-d07b39259dd5/context/ctx_f9bcfb27c948__extract-autobyteus-nfs-dr003-terminal-receipt.md. Native CI7packages on Ubuntu/macOS passed but explicitly no mounted/platform/signing/publication qualification. Prior scope/closedTask preserved.
E02: canonical git status/remote/worktree inventory, fetch and isolated worktree creation above. No source changes or live resources.

## Unknowns
Current release gates/assets/targets; source of supported qualification; signing secret names/availability without retrieving values; superrepo conventions; actual version/channel choice; independent release outcome versus blockers.

## Supplement inventory
None yet. Prior finalized receipt is reference-only evidence, not a new requirements supplement or qualification.

## Completed requirements evidence (2026-10-18)
E03 — `.github/workflows/ci.yml`, full `.github/workflows/release-nfs.yml`: ordinary push/PR runs native race/vet/build/version/Python/Bash, no artifacts. Release manual-only has release_tag/publish=false/candidate_run_id; prepare checks out tag; both native engine architectures build in pinned Ubuntu; exact package candidate is reused on publish; image is rebuilt/pushed before binary/signing matrix; public upload requires existing release and uses --clobber. Native Mac runners15 do not establish actual CheckHost floor26. No workflow creates tag/release. Full workflow read, not executed.

E04 — full `packaging/RELEASE.md`, `packaging/release-lock.json`, `packaging/release.py`, `packaging/engine/manifest.py`, engine README: lock qualifiedTargets=[], qualifiedSourceHash='', physicalEvidence=[], userVerified=false, engine=null. Publish code demands supported targets, exact production-source hash, userVerified, at least3 existing in-repo physical evidence paths and both measured engine architectures; docs additionally require semantic independent physical Mac/Linux/Docker sufficiency. Path count is not proof of semantic Pass. Hash includes production source, installer, engine recipe, workflow, license and filesystem usage, excluding tests/deb/cache; engine identities are hash inputs. `manifest lock` clears qualification. No current full candidate/run exists in NFS Actions. Historical single-VM command tests are not current or independent physical qualification.

E05 — full `scripts/public/nfs/install.sh`, `internal/cli/verify-release.go`, cmd main: placeholder installer fails before network. Versioned GitHub URLs, archive SHA, exact four regular members, binary equality against downloaded manifest and runtime target required; then user CLI staged and invoked. No-argument invocation enters setup; downstream download smoke must pass `version` with owned HOME and must not invoke live-user create/connect/reconnect/detach. Installer blocks container host; container-only smoke is not valid host installer success. Source checksum manifest currently covers tar.gz only, not every loose release asset.

E06 — README current target table and `internal/cli/install.go` CheckHost: native macOS26+ / APFS / Apple NFSv3; Ubuntu24.04 ext4 / corrected Ganesha NFSv4.1; Docker engine only on Linux host. ARM64/x64 packaging targets. Native Mac/Linux clients and externally configured ordinary-directory consumers; no Mac Docker Desktop hosting or application nodes. Existing CheckHost rejects /.dockerenv; installed source/consent/state guards preserved. No live runtime probing was done.

E07 — full N root AGENTS/DESIGN/TESTING/RELEASE and packaging policy; superrepo RELEASE.md (full, missing truncated excerpt reread), `.github/workflows/release-desktop.yml` first210lines and `scripts/desktop-release.sh` first170lines, plus release_versions reference search. Superrepo reference supports independent build-only, selected beta/stable, version/tag consistency, tag-driven CI with release creation, no published-tag movement, partial-release reporting and fresh-base finalization. Desktop package version, mobile version limits, assets/providers are not NFS requirements. Superrepo shared HEAD5096011674c7db6ec0e92e522ea37f32f8f4ea40 is reference-only, not modified or claimed current release source. N fresh base7e375984 above remains actual task source. N root policy's extraction-specific paired/bootstrap/no-release text must be reconciled only in authorized NFS scope.

E08 — primary external contracts checked by browser:
- https://cli.github.com/manual/gh_release_create : creates release; nonexistent tag defaults to default-branch tip unless target supplied; verify-tag prevents implicit creation; draft/assets/publish are separate operations; prerelease/latest flags exist. A future design must pin exact intended source rather than allow default-tip drift.
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts : artifacts expire (default90days) and require signed-in read access. Candidate CI artifacts are not a replacement for public release downloads.
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow : retrieved for later trigger investigation; no trigger design selected before requirements approval.
- Apple https://developer.apple.com/documentation/security/customizing-the-notarization-workflow returned a JS-only body; not used as a newly verified procedural claim. Existing repository signing policy remains authority; more primary procedural validation required during architecture.

E09 — `evidence/intake/repository-release-preflight.json`: successful read-only gh API2026-10-18. Repo public/defaultmain; current authenticated metadata permits push/admin (not a signing credential claim). Tags[], releases[], release-nfs runs0. Repo secret names0, organization secrets available to this repo0, environments[]. No secret values read/copied and no settings changed. All six current Mac publication inputs are absent: NFS_MAC_CERTIFICATE_P12_BASE64, NFS_MAC_CERTIFICATE_PASSWORD, NFS_MAC_SIGNING_IDENTITY, APPLE_ID, APPLE_APP_SPECIFIC_PASSWORD, APPLE_TEAM_ID. These may be supplied through normal repository secret administration later; do not scrape superrepo secrets, print values or assume its differently named signing configuration automatically applies.

## Scenario / surface inventory
BEH001 candidate/CI; BEH002 qualification; BEH003 publish/retry; BEH004 install; BEH005 preserved host-only behavior; BEH006 docs/finalization map to requirements SCN001–007. Supported triggers are explicit maintainer preparation/publication, documented first-use install, current qualification contract, and operational failure/retry. No hypothetical malformed internal host-state migration is added.

Structural surfaces: privileged publication credentials, Git tags/GitHub release/assets/GHCR identity, qualification JSON/source hash, candidate artifact lifecycle, signed binary manifests and install scripts. Payload surfaces: engine manifests/package/source archives/inventory/notices, per-target executable archives, checksums/release notes and physical/user receipts. Runtime service engine/source semantics are preserved; qualification is not inferred from compilation. Existing tests in scripts/tests/test_nfs_release_workflow.py explicitly assert no tag/release creation and model limited job booleans; these need coherent approved-scope updates, not just fixture-string replacement presented as hosted proof. test_nfs_packaging.py exercises placeholder/unqualified refusal. No tests executed for this investigation.

## State, dependencies and unknowns
No live host state may be altered; new intended external state is versioned release/tag/assets. Existing installed state safety is not repository path-dependent. A real authorized release needs exact candidate, independently adequate physical/host-mode receipts and user-verification reference, plus selected Mac signing/notary inputs. Test-owned physical host availability is **unknown**, not claimed unavailable or satisfied by local VMs/hosted unit runners. No paid resource acquisition authorized. Current-source candidate and qualification do not yet exist; no agent is dispatched to execution in this requirements hold.

## User decision / approval applicability
DEC001 asks first release channel/version/platform set directly: recommend v0.1.0-beta.1 full macOS/Ubuntu ARM64/x64 versus expressly Linux-only first with Mac deferred. This is material scope/channel, not an implementation questionnaire. Await answer; preserving current physical/signing/user-evidence gates is explicit. Source policy says user verification is required; publication consent cannot populate userVerified=true. No other requirements decision currently requires user preference. Architecture work has not begun.

## Supplemental artifact inventory (current)
| Path | Owner / purpose | Scope / related IDs | Status / approval |
| --- | --- | --- | --- |
| evidence/intake/repository-release-preflight.json | SD, timestamped GitHub metadata and source-file hashes | REQ001/003/004; AC001/002/003 | Read-only evidence, no secret values; not behavior-defining |
| Original DR003 terminal receipt path E01 | SD/Delivery prior completion provenance | Preserved extraction boundary | Finalized read-only; no current release qualification |

## Current status / next work
R1/SR001 Ready for Approval of DEC001. Further target architecture awaits approval and full architecture reading gate. No source/policy/workflow change, tag/release/registry/secret write, CI dispatch, mount/service/container or test execution performed. Only new task documents and metadata evidence authored in isolated worktree. Failed guessed read of a nonexistent filename was not a product failure; actual tests located and read. No Task completion/handoff claim.
