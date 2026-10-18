# IR-004 CR-002 validation plan

Approved R2/SR003, SR004/ARCH002; Large/High unchanged.
Input N5c2c95895422a9f51857546e3bd38fa98a51e591 (service83726b unchanged),
S5559abbf017566f0030d95b023614f7418d3f212. Reviewer CRR004 Fail99.8;
sole mandatory cleanup is the unused local Skill import in the Claude bootstrap test.

## Delta and impact before checks
Remove exactly that one import. No production, fixtures, assertions, dependencies,
build configuration or persisted data changes. The Skill domain class and actual
configured-skill types stay. Frontend feedback loop Not Applicable.

| Prior check / last validated input | Disposition | Reason |
| --- | --- | --- |
| CRR004 unused audit / S5559abbf | Rerun | Sole6133 finding must disappear across same25 production+4 tests |
| IR003 final Claude bootstrap controls / S5559abbf | Rerun | Own test file loses unused import |
| IR003 remaining local suites / S8c5c76 then Codex-only5559abbf focused76 | Still valid within recorded scope | No exercised production/shared input/other test change |
| Independent N / service83726b, CRR002/API001 | Still valid with original limits | All service inputs unchanged |
| API001 S groups / Sa2023fef | Existing integrated rerun requirement remains | Shared foundations changed in IR003; this import cleanup does not close API-owned S04/S05 |

Run the same read-only TS5.9.3 no-unused audit, then the affected Claude test via
documented vitest run --no-watch in a fresh current-source copy with private
HOME/TMPDIR, frozen server + script-prerequisite closure install and server prebuild.
Production typecheck evidence from IR003 carries: this round changes tests only.
Compare entire file with the predecessor minus the one import to preserve all
assertions/fixtures, and verify copied inputs and cleanup. No1666-test repeat,
full API/E2E, provider/storage/VM/editor campaign or new approval.
