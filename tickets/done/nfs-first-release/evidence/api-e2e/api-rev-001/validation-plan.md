# API/E2E coverage investigation — nfs-first-release

## API-REV-001 plan before execution
R2/SR002 Approved; SR003 Ready; ARCH001 Pass; IR001 source886b55e; CRR001 Pass100 at c1f1330. Large/High. This NEW first normal v0.1.0 task authorizes release only after readiness; old extraction no-release and command-only topology do NOT replace its approved current gates. No old Task reopened. Complete requirements/investigation/design/history/handoffs/architecture and source reports plus IR evidence map/intake E18 read. Six signing secrets provisioned, not validated; no reprovisioning request.

Read root AGENTS/DESIGN/TESTING/RELEASE/README, go.mod, packaging/RELEASE and actual workflow, candidate/qualification/facade/test paths. No closer guidelines. Local checks require independent APFS source outside /private/tmp, private HOME/TMPDIR; Linux archives extracted inside guest filesystem. Fixtures do not imply privileged runtime authorization. Current source runtime/engine pins/ordinary CI unchanged; all119 source inputs and existing tracked ticket artifacts preserved by input-audit.json.

Boundaries: Actions scheduling/retention, source/engine/full OCI identity, structured qualification, Mac keychain/sign/notary, final payload/publication/recovery, bounded installer. No app/browser/UI work. UI category N/A; CLI/download covered under actual user boundary. Legacy removal and state decisions inspected: single current release path, no old publisher/beta/path-count fallback; host state Not Affected, qualification rebuilt ONLY from actual candidate, external immutable identity directly read/reconciled.

## Coverage validity and gap decisions
- Still Valid: all test_nfs_release_{records,publication,signing,workflow}, source_identity, engine_packaging, packaging and installer fixtures; reviewed current assertions follow SCN001–006. Execute actual parsers/files/signing shell/inert installer with disclosed external doubles. Synthetic evidence NEVER copied into real lock.
- Still Valid/carried attribution: IR001 native Go race/vet/four compiles and six mutation controls, CRR001 independent Python/static evidence; unchanged Go runtime and ordinary CI justify reuse for local scope only. Required current hosted native four-target execution is separate and not carried.
- Add Durable Coverage only if investigation/execution discovers a specific missing supported release boundary; none established now. Do not rewrite source from a test assumption. No stale coverage removal.
- Temporary executable actual checks required: hosted exact candidate/run/envelope/no-public-effects, retained measured two-arch engine/whole OCI, qualification-only same-digest registry and native host journeys; exact current OS/topology inventory first. Publication/signing/final public payload is Delivery-owned after qualification acceptance. Real missing prerequisite remains explicit; do not manufacture receipts.

## Cases / expected evidence
| Case | SCN / AC | Surface / expectation |
|---|---|---|
| R01 | 005 /001–006 | Fresh independent current local fixtures: release records, publication/retry, signing/cleanup, workflow truth table, installer; expected refusals, all valid controls pass |
| R02 | 001/005 /001/006 | Source identity/static workflow/shell/empty-lock refusal; preserve exact inputs; native Go local proof attributed IR001, not new qualification |
| R03 | 001 /001/006 | Read-only remote inventory then actual publish=false dispatch on available reviewed ref; 2engine architectures+complete OCI+4native targets succeed, no tag/release/image writes; retain exact run/attempt/artifact envelope |
| R04 | 002/005 /002/006 | Fetch/verify actual retained candidate, no latest guessing; inspect source/engine/OCI/native hashes and retention; alias metadata bounded without qualified targets |
| Q01 | 002 /002/006 | darwin-arm64 mac-native, macOS26+ APFS, independent hosts/kernels |
| Q02 | 002 /002/006 | darwin-amd64 mac-native, macOS26+ APFS, independent hosts/kernels |
| Q03 | 002 /002/006 | linux-arm64 linux-native, Ubuntu24.04 ext4, independent hosts/kernels |
| Q04 | 002 /002/006 | linux-amd64 linux-native, Ubuntu24.04 ext4, independent hosts/kernels |
| Q05 | 002 /002/006 | linux-arm64 linux-docker, same exact OCI from test-owned reachable registry on Ubuntu24.04 ext4 |
| Q06 | 002 /002/006 | linux-amd64 linux-docker, same exact OCI from test-owned reachable registry on Ubuntu24.04 ext4 |
| U01 | 002 /002 | Genuine executed-user-check of exact candidate/all4targets; publication/secret consent not verification; only request after executable candidate scope exists |
| D01 | 003/006 /003/004/006/007 | Downstream Delivery: accepted qualification/current-main, real signing+Accepted notary, retained final payload, normal publication and same-payload recovery; not API-owned remote writes |
| D02 | 004/007 /005/007/008 | Downstream Delivery/public checks: final fourtarget download/install/version/signature identities; docs/finalization/current refs/receipt |
| C01 | 007 /008 | Owned cleanup, exact source/upstream preservation; retained real candidate ownership/path/expiry explicit if created |

Each Q row has seven independently recorded operations Qxx-01..07: (01) public create/connect and plan/consent/UUID; (02) bidirectional exact text/binary bytes through distinct client/server paths with measured <=5s visibility after close; (03) create/edit/rename/move/mkdir/list/delete and concurrent distinct paths without cache flush/manual remount; (04) nonroot permissions/executable preservation, supported fcntl exclusion/release and Git init/add/commit/status plus lock conflicts (no automatic trust); (05) wrong source/identity/busy/unowned detach refusal then safe detach preserving source/private state; (06) stop/restart and reconnect with source UUID/client state retained, recorded host reboot only on authorized disposable node; (07) private/runtime files not exported, chosen-path/existing bytes preserved. Planned commands use Python/standard shell/Git/NFS CLI, no product app/editor/provider. All required rows and at least physical mac-native/linux-native/linux-docker categories must be real; VMs cannot fill physical rows, containers not independent kernels.

## Environment and safety plan
Inventory local OS/CPU, available disposable VM managers and existing process/container names read-only; do not open SSH config, credentials, broad private files or touch running resources. Discover project-documented assigned remote hosts, not assumed physical resources. Inspect GitHub refs/workflow/run/artifact/tag/release metadata with gh read API. If reviewed workflow/source is unavailable remotely, request necessary staged ref/finalization from Delivery owner, never self-merge/push; no false API Pass to unblock it. No paid infrastructure or live-user mount/firewall/daemon changes. Actual setup only assigned test-owned hosts and minimal data. Never restore/delete other owners' work.

## Confidence / broader decision before execution
Unscored until local results; no API verdict yet. Broader validation REQUIRED: fixtures cannot prove hosted Actions, real BuildKit OCI, physical target/mode behavior, user verification or notarization/public download. Candidate and host availability unresolved; these are execution dependencies, not a new design/approval loop. Follow up on concrete findings through normal origin rules. No qualification lock mutation or immediate Delivery completion.
