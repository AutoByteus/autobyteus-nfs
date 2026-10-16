# Source extraction provenance

Date: 2026-10-16. Task: project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8,
`extract-autobyteus-nfs`. Initial relocation: R1/SR001, SR002, ARCH-REV-001 (historical).
Current runtime boundary: Approved R2/SR003, SR004, ARCH-REV-002.

Original repository: https://github.com/AutoByteus/autobyteus-workspace
Exact source commit: **3712cd9bf0db998501d162db7f8655f169e3def6**.
Original authorship and complete history remain at that repository; this is a
bounded tracked-source snapshot, not an authorship reset or unrelated-history
rewrite. Copyright/license/CLA and third-party attribution are retained.

| Original source path | Standalone path / disposition |
| --- | --- |
| autobyteus-nfs/{cmd,internal,go.mod,testdata,packaging,README.md,LICENSE,THIRD_PARTY_NOTICES,.gitignore} | Root same names; Go module/import prefix github.com/AutoByteus/autobyteus-nfs |
| scripts/public/nfs/install.sh | Same path; future download repository changed to AutoByteus/autobyteus-nfs; unqualified placeholder unchanged |
| scripts/tests/test_nfs_engine_packaging.py, test_nfs_installer_fixture.py, test_nfs_release_workflow.py | Same names; root-local packaging paths |
| scripts/tests/test_nfs_packaging_and_launcher.py | Service cases in scripts/tests/test_nfs_packaging.py; generic launcher cases remain app-owned; retired NFS adapter cases removed |
| .github/workflows/release-nfs.yml | Same path; NFS-owned manual-only version/candidate workflow, paths rebased, gates retained |
| CLA.md | Verbatim |
| LICENSING.md, NOTICE, CONTRIBUTING.md | Repository/component references adapted; copyright/contact/contribution terms and section7 additional permission retained |

Initial extraction commits 353dd2c17a59dead97c900a327f78a2bb21f46ce and
0c9fd27a77d65504b8eef41ece8972badb31778c mechanically relocated Go imports and
build paths. The final R2 implementation is **not** a byte-identical runtime move:
app-node CLI/control/probes/public descriptors are removed, host-only lifecycle
retained, and incompatible active/pending node obligations refuse without migration.
The service Connection fixture is named testdata/connection.json, not an app API.
Packaging source identity covers local NFS inputs and filesystem-usage.md only.

In the source app, NFS admission/terminal/Git/launcher coupling and paired fixtures
are removed. Registered workspace errors remain; private configured-skill profiles
are used independent of filesystem for Claude/Codex/Grok. No automatic Git trust
or generated workspace-link fallback replaces the removed selectors.
Engine source/patch/COPYRIGHT obligations and license/CLA remain unchanged.

Generated/ignored outputs, old binaries/debs/engine candidates, PM task-plans,
application source and historical ticket trees were not imported. A retained
arm64 engine may be copied read-only into owned scratch and freshly verified for
packaging checks, never promoted to current runtime/publication qualification.
The qualification lock remains empty; no tag, release, image push or deployment
is authorized. Historical filesystem/editor Tasks remain closed.

Both repositories are independently maintained. Delivery records both exact
finalized revisions, not a consumer protocol pin. Finalization order and truthful
partial-completion policy are in RELEASE.md. Historical tickets are not rewritten.
