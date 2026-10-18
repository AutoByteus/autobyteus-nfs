# CRR005 — CR-002 resolution

Independent source diff contains exactly the two requested local alias removals.
Normalized AST comparison removes those aliases from the prior tree and compares
every remaining node to current source, excluding line positions. Other118/120
non-ticket inputs are byte-identical. Sixteen extant IR003-changed Python files
have no unused local import under a Name-load scan. This is not a compiler or
proof that public/dynamic exports are unused; the caller trace supplies that check.

- `packaging/engine/manifest.py:8` still imports VERSION/NAMES/identity/source_identity
  from source. `source.py:11` owns LOCK, which its identity/preparation code uses;
  `build.py:14,39,44,59` imports/uses that owner. Module initialization still occurs.
  No manifest.LOCK or from-manifest LOCK consumer exists in packaging/scripts/internal.
  Workflow invokes manifest's explicit merge/verify/lock CLI, not this alias.
- `scripts/tests/nfs_release_fixture.py:13` retains candidate/i/payload. Fixture
  methods only use these owners. Tests import Fixture/TAG/SHA/make_oci from this
  fixture and import readiness directly from release_support. payload.py:7,28,56,75,122
  retains readiness import/validation/notes calls. No fixture.readiness re-export
  consumer or configured/dynamic public entry point depends on the removed name.
- Existing reset/readiness/payload/signing/publication/installer assertions are
  unchanged and executed by the current full Python suite. No test disabled,
  assertion weakened, module deleted or behavior redesigned.

Independent governing basis is Core7/touched-file cleanup, already established by
CRR004/CG012. Resolution restores that contract; it does not fix or claim a new
runtime NFS/signing defect. Production hash and recipe include manifest, so the
required new hosted candidate must bind current bytes even for this import cleanup.
