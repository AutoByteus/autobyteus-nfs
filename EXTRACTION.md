# Source extraction provenance

Date: 2026-10-16. Task: project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8,
`extract-autobyteus-nfs`. Approved R1/SR001, design SR002, ARCH-REV-001.

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
| scripts/tests/test_nfs_packaging_and_launcher.py | Service cases in scripts/tests/test_nfs_packaging.py; launcher cases remain app-owned as test_nfs_launcher.py |
| .github/workflows/release-nfs.yml | Same path; NFS-owned manual-only version/candidate workflow, paths rebased, gates retained |
| CLA.md | Verbatim |
| LICENSING.md, NOTICE, CONTRIBUTING.md | Repository/component references adapted; copyright/contact/contribution terms and section7 additional permission retained |

Runtime files differ only by Go import namespace. The Go-to-Python bootstrap test
uses the new root. Packaging source identity is now local NFS plus declared
integration contract, not a digest of arbitrary application code. New policies,
CI and integration-contract documentation establish independent maintenance.
No installed path, serialized schema, runtime algorithm or engine recipe/pin is
changed. Exact engine source/patch/COPYRIGHT obligations remain in packaging/engine
and THIRD_PARTY_NOTICES. No license change or Apache predecessor claim.

Generated/ignored outputs, old binaries/debs/engine candidates, PM task-plans,
application source and historical ticket trees were not imported. A retained
arm64 engine may be copied read-only into owned scratch and freshly verified for
packaging checks, never promoted to current runtime/publication qualification.
The qualification lock remains empty; no tag, release, image push or deployment
is authorized. Historical filesystem/editor Tasks remain closed.

The app owns its installed-CLI/descriptor consumers and an exact local fixture
with real producer commit/path/SHA provenance. Paired equality is checked at
integration, without requiring a sibling checkout for ordinary app tests.
Delivery records both actual finalized commits; this file intentionally contains
no fabricated or self-referential destination commit. Finalization order and
partial-completion policy are in RELEASE.md.
