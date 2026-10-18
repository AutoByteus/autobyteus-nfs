# CRR-001 independent checks and limits

Inputs: N9208f8d4f81c78c537b4105773bae85dd74a0076 (service source83726b27400b405a7a6a79bd962d8e2419daa561), Sd3f7f67015587b4c8aa26824786be807793485d1. R2/SR003, SR004, ARCH-REV-002, IR-001. This is initial source review, not API/E2E validation.

## Personal execution

- Independent tracked N snapshot, no S checkout/dependency; 108 non-ticket inputs. Own physical archive under `/Users/normy/autobyteus_org`, private HOME/TMPDIR/Go caches, verified Go1.27.2 Darwin arm64 download. Exact commands in run-standalone-checks.py/checks-result.json.
- Go race `-count=1 ./...`: seven packages Pass; command package has no tests. `go vet ./...` Pass. Python20 collected,19 executed Pass,1 explicit child-only skip; Go platform suite exercises child fixture. Actionlint and Bash syntax Pass.
- Service source hash348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e confirmed; `--check-publish` expected exit1, empty qualification refused. No publish attempted. Python fixtures cover source mutation/missing inputs and workflow/installer gates.
- Read-only TypeScript5 compiler unused-local check over changed server production files: five unused import bindings in three touched files. `audit-unused-imports.cjs` uses noEmit/noResolve; it is NOT a full typecheck. Direct source reference inspection confirms each diagnosis; exported ClaudeSessionEvent remains independently re-exported and must be kept.
- All132 implementation package-index entries independently hash-match. All83 predecessor Go files classified45 normalized-equal/23 deliberate R2 changes/15 removals, including28 unchanged backend/platform/service production files. Normalization ONLY replaces the actual Go import prefix. Source sizes and no-active-coupling scans recorded in source-audit.json.
- LICENSE, CLA, THIRD_PARTY_NOTICES, release-lock and five engine recipe/pin files match original S3712cd9b bytes. Provenance and adapted permission references inspected; no legal interpretation or new qualification.
- Inspected implementation rendered EN390 and zh1440 screenshots plus four-state result: readable copy, bounded layout, unavailable release state; no personal browser session or desktop acceptance claim.

## Attributed upstream execution, not reviewer reruns

IR001 final S production build/typecheck,1158 focused units plus40 activation/PTY units,39 local route/profile checks,17 local real-run/native-PTY checks,24 Guide/utility checks and34 launcher checks. Six AGY live opt-ins, absent pwsh and occupied8001 skips retained. Local provider children are scripted, not authenticated inference. Four N target compiles and verified retained arm64 embedded build are implementation evidence, not newly executed/qualified here.

## Attempts and cleanup

attempts.md explains the reviewer's initial archive-location failure, conservative import-normalization mistake, source-scan false positive and discovery misses. Failed logs remain intact. Only own harness paths/scans changed; no production/test policy weakened. Final independent checks green within their stated scope.

Both owned N scratch roots were removed in their respective cleanup receipts, all synchronous subprocesses awaited. No S build/output, live app, VM, container, mount/export, provider/account, user data, PM board, historical engine or old dist tree changed. No production/test edit by reviewer. No target merge/push/tag/release/deploy/TaskDone/user verification.

API/E2E must still provide its selected validation after source review passes. AC007 remains Delivery-owned. Do not reopen completed filesystem/editor Tasks or the old VM/provider campaign; R2 filesystem-only boundary and host-only refusal policy govern.
