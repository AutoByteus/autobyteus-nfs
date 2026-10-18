# CR-002 bounded cleanup

AST audit across every extant IR003-changed Python source/test found exactly two
unused local bindings at intake; after removing them it finds none. This audit is
local binding/reference analysis, not a configured compiler/linter diagnostic.

- manifest.py imports source VERSION/NAMES/identity/source_identity; each remains
  live. Importing LOCK there had no local load or manifest.LOCK public/dynamic
  consumer. source.py LOCK and build.py LOCK are unchanged and live; source module
  loading remains required by the surviving imports. No engine recipe logic removed.
- nfs_release_fixture.py uses candidate/i/payload; readiness has no local load or
  fixture re-export consumer. Test consumers directly import readiness and payload
  still imports it, so readiness validation/module loading/assertions remain.

Direct `rg` searches under packaging/scripts/internal for manifest.LOCK,
from-manifest LOCK, nfs_release_fixture.readiness and from-fixture readiness have
no matches. The reviewer's corroborating public/dynamic entry inspection is
recorded in crr-004/unused-reference-trace.md, not invented as a new runtime test.
Only the two import lines changed; the other118 source inputs and all runtime/
assertion logic remain identical. No broad unused-code cleanup or design change.
