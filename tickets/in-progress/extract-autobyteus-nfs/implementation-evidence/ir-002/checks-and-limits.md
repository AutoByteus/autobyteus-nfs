# IR-002 checks and limits

Task extract-autobyteus-nfs / project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8.
Approved R2/SR003, Ready SR004, ARCH-REV-002; Large/High retained.
Only CRR001/CR001: five local bindings removed in three S production files.
No N source/runtime/test changes. S commit a2023feff3d498fb6c51cebf1c93360da3679a45.

## Fresh checks
- `node audit-unused-imports.cjs`: TypeScript5.9.3 read-only unused-local
  diagnostics6133/6192/6196 over25 extraction-touched TS production files; zero.
  This uses the reviewer audit copied into E2, not overwriting reviewer evidence.
  It is no-resolution analysis, not the semantic typecheck.
- `node audit-delta.cjs`: exact three-file scope, unchanged generated JavaScript
  before/after using production compiler options, ClaudeSessionEvent public
  re-export retained, all files shrink (60→59,165→162,49→48 nonempty lines).
- Owned current-source copy with clean HOME/TMPDIR: frozen install of server and
  script-only backend SDK prerequisite closures, Prisma client generation,
  then `pnpm -C autobyteus-server-ts typecheck` including documented
  pretypecheck/shared builds; final exit0.
- Input-integrity receipt checks source/copy equality for all copied tracked
  non-ticket files after the check. `git diff --check` passes.
- Node22.21.1, pnpm10.28.2, TS5.9.3, Darwinarm64. Initial audit invocation used
  host Node22.23.1; final audit rerun used22.21.1. Toolchain receipt retained.

## Scope and failures
No new tests authored or executed: this cleanup changes no emitted JavaScript.
Production semantic typecheck plus unused diagnostics directly checks the finding;
IR001 behavioral tests and CRR001 standalone checks carry with their existing
limits, not as newly run or new API approval. Frontend feedback N/A for this delta.
Two setup failures (audit rootDir, missing script-only SDK install closure) are
retained in attempts.md and attempt subfolders; no product policy weakened.
No real app, NFS, mounted filesystem, container, VM, external provider or user
configuration changed. No old editor/filesystem qualification reopened.
Cleanup removes only scratch recorded by run-checks.py; no active owned process
remained. No merge/push/release or user-verification claim. Source re-review,
proportionate API validation and Delivery-owned AC007 remain downstream.

Raw Prisma logs (current and retained attempt-2) and the final typecheck log each
end with a tool-emitted extra blank line. The three staged diff-check EOF
diagnostics are retained as raw-log exceptions, not source whitespace failures;
all non-log staged artifacts pass the separate whitespace check.
