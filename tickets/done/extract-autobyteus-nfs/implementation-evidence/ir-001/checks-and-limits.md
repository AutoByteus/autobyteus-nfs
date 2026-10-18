# IR-001 implementation checks

Current service source N83726b27400b405a7a6a79bd962d8e2419daa561.
Current app source Sd3f7f67015587b4c8aa26824786be807793485d1 (production delta in 2448e166, nested fixture correction in d3f7f670).
Approved R2/SR003, design SR004, ARCH-REV-002. These are implementation-scoped results, not API/E2E or release signoff.

| Check | Actual local result / evidence |
| --- | --- |
| Independent N archive, no S checkout | Committed N source archived excluding tickets; hashes in standalone-final-archive.json. Native Darwin arm64 Go1.27.2 full race suite: seven packages exit0, CLI cmd has no tests; vet exit0. Native diskutil/source capture concerns use owned directories. No mounts |
| N Python | 20 collected, 19 executed successfully, one explicit child-binary skip; Go platform TestBootstrapDirectoryModes invokes that permission fixture. Five service-owned suites, no Node/app checkout |
| N actionlint / shell | exit0. Workflow boolean/control fixtures exercise candidate reuse, failures/cancellation/current source/signing requirements. Not hosted Actions |
| N packaging / source hash | Source-hash and invalidation/missing-input controls pass. Hash 348046594b470f7b294aa2162f78ec349eb57c4edf74aa2db32112a9dc9da90e. Publication check expected exit1; unqualified lock unchanged. No candidate publication |
| N targets / retained engine | CGO0 Darwin/Linux × arm64/amd64 compile. Only native Darwin arm64 version executed. Exact retained arm64 engine source/debs/COPYRIGHT/manifest freshly hashed, manifest validated/files checked, copied into owned archive and embedded Linux arm64 CLI compiled; no engine execution/rebuild or new qualification. standalone-binaries.json / retained-engine-verification.json |
| S prerequisites / production typecheck | Documented server test:integration:prepare exit0 (core/SDKs/server/devkit/importable application, sanitized built-in bootstrap). tsc -p tsconfig.build.json --noEmit exit0. consumer-final-checks.json |
| S focused unit areas | 102 files / 1158 tests successful; four AGY live files / six tests intentionally opt-in skipped. Includes actual private-profile files, native child process fixtures, bootstrap source/collision/no-binding/exact release, registered resolution. consumer-final-unit.log |
| S activation / terminal owner units | Separate final selector: two files / 40 tests successful. Mock PTY owner tests, not native shell proof. consumer-final-activation-terminal.json/log |
| S local route/profile composition | Existing file REST and GitHub/private-skill GraphQL fixture suites: three files / 39 checks, command exit0. Actual local socket/file operations plus external provider doubles. No downstream API verdict. consumer-final-local-routes.log |
| S local native path/PTY integration | Existing manager composition, real memory-layout with dummy LLM, and native PTY WebSocket lifecycle: three files /17 checks exit0 with canonical owned HOME/TMPDIR. Requested ordinary cwd, server home, missing-cwd refusal, close/churn and run lifecycle. consumer-final-path-integration-physical-home.json/log; earlier alias failure retained |
| S frontend | Nuxt prepare and affected four Guide/command component/utility suites:24 tests successful; localization boundary guard exit0. Current Guide rendered EN/zh at1440/390, disabled buttons/no release link, no horizontal overflow/runtime errors. guide-render/result.json and four screenshots; browser/Nuxt/route cleanup recorded |
| S generic launcher | Python suite36 collected,34 executed successfully; pwsh unavailable and occupied port8001 collision fixture skipped. Bash syntax exit0. No Docker daemon/container mutation. consumer-launcher-localization.log |
| Source/ownership | 28 backend/platform/service production files normalized-equal after Go import relocation. All83 original Go files classified:45 normalized-equal,23 deliberately R2-changed,15 removed. source-audit.json records full map, no forbidden runtime coupling; no source size guard violation.58 changed TS files parse clean |
| License / state preservation | Service LICENSE/CLA/notices/release-lock exact, engine recipe pins unchanged; section7 permission equal ignoring wrapping. Reviewed R2 documents unchanged. PM board and old retained engine input hashes unchanged |

## Limits / deferred to selected workflow

Independent source review and API/E2E coverage classification still required. Finalization AC007 is Delivery-owned and not done. No live NFS create/connect/reboot/physical test, installed migration, real provider authentication, old VM/editor campaign, Windows/Powershell execution, hosted workflow/signing, release/tag/image push or deployment. Source identity is service-local; engine artifacts and app revision are separately named. Historical filesystem results are provenance only.

No fake replacement detector or compatibility bridge. App intentionally no longer protects against a path whose mount disappears; ordinary OS path/I/O semantics apply. Operators own storage readiness and container binds. Old NFS active/pending node obligations refuse under lock rather than migrating or discarding them. This task never touched a live such installation.

Removal of obsolete tests follows R2: N app-node behavior and S NFS admission/Git-injection/project materializer wrappers/paired fixture disappear. The old Codex bootstrap integration file asserted removed project-materializer discovery, so it is removed, not counted as current native-provider proof. Replacements exercise private profile/current bootstrap/process ownership; genuinely external-provider opt-in checks remain unclaimed.

Failed attempts are detailed in attempts.md; raw logs, including ANSI and diagnostic whitespace, are intentionally preserved. Earlier mechanical R1 extraction and first preparation failure are not current success. Source hashes and clean isolated input copies distinguish current source from prior artifacts.
