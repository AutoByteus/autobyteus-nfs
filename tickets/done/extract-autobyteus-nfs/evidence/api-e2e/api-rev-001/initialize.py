from pathlib import Path
import json,subprocess,hashlib
N=Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs')
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
T=N/'tickets/in-progress/extract-autobyteus-nfs'
E=T/'evidence/api-e2e/api-rev-001';E.mkdir(parents=True,exist_ok=False)
cases=[
('E01','Current independent source, removal and license audit','AC001/004/006/008','Archive/hash/import/lock audit; no sibling linkage'),
('N01','Bounded predecessor-state admission and host lifecycle','AC009','Focused Go config/CLI/setup tests, then race/vet all packages'),
('N02','Standalone packaging and refusal gates','AC001/002/005','Python fixtures, installer shell, actionlint, current source hash/publication refusal'),
('N03','Current four-target compile and exact retained engine verification','AC001/002/005','CGO0 darwin/linux arm64/amd64; native version; real arm64 manifest/embed'),
('S01','Clean consumer setup, production build and typecheck','AC003/006','Frozen filtered install including script-only dependencies; integration:prepare/typecheck'),
('S02','Ordinary registered paths and filesystem-independent private profiles','AC003/010','Focused registered/native/private preparation/bootstrappers/process tests'),
('S03','Runtime owner regression closure','AC003/006/010','Broader backends/services/workspaces/terminal/Codex/activation units; real process fixture included'),
('S04','Ordinary file/skill APIs','AC003/010','Local composed server REST/GraphQL tests, owned filesystem fixtures'),
('S05','Ordinary run and native PTY/WebSocket lifecycle','AC003/010','Current-build path/memory-layout/terminal integration; local dummy LLM, no paid provider'),
('S06','Generic launcher and factual disabled Guide','AC003/005/006','Bash fixture launcher; four Guide/localization suites and guards; carry unchanged current Guide render proof'),
('E02','Cleanup and evidence/source integrity','AC008','Own scratch/process cleanup; source and protected resources unchanged'),
]
(T/'api-e2e-test-case-ledger.md').write_text('''# API/E2E Test-Case Ledger

## Ledger Meta
- Task: extract-autobyteus-nfs; first round API-REV-001 (no prior API result).
- Scope: approved R2/SR003, Ready SR004, ARCH-REV-002, CRR-002. Large / High / Reviewed.
- Investigation: api-e2e-coverage-investigation.md. Report: api-e2e-execution-coverage-report.md (pending).
- Multiple independent cases and clean builds require durable checkpoints.
- Planned before execution, 2026-10-18. N and S refer to the two assigned worktrees, not old shared-network-workspaces.

## Planned Cases
| ID | Journey | ACs | Surface / expected result |
|---|---|---|---|
'''+''.join('| '+' | '.join(c)+' |\n' for c in cases)+'''
## Execution Events
| Time UTC | Case | Event | Observation | Result | Evidence |
|---|---|---|---|---|---|

## Reconciliation
No completed execution yet. AC007 ordered finalization is Delivery-owned and is not claimed as executed.
''')
(T/'api-e2e-coverage-investigation.md').write_text('''# API/E2E Coverage Investigation

## Authority and classification
First API-REV-001, extract-autobyteus-nfs / project_task_fdb2c737-fb08-48cf-8aca-e04df2d02ae8. This is NOT the completed shared-network-workspaces task.
Current basis: requirements-doc.md (Approved replacement R2/SR003), investigation-notes.md, solution-revision-record.md, design-spec.md (Ready SR004), user-filesystem-boundary-correction.md, solution-design-handoff.md; design-review-report.md / architecture-review-revision-record.md (ARCH-REV-002 Pass); implementation-handoff.md / implementation-revision-record.md (IR002 over cumulative IR001); code-review-report.md / code-review-revision-record.md (CRR002 Pass100). Delivery revision and prior API result: N/A.
Large / High / Reviewed; successful output requires proportional test-code review, not immediate Delivery. Personal execution, no delegation.

## Current behavior and supported scenarios
SCN001 independent N contribution; SCN002 nonpublishing packaging; SCN003 ordinary workspace/run/PTY and generic mappings; SCN006 host-only lifecycle and bounded refusal; SCN007 private configured skills. SCN004/AC007 finalization belongs to Delivery. SCN005 live deployment/platform/provider/old editor campaigns are excluded.
N owns host storage only. S consumes ordinary directory paths regardless of backing filesystem. No app NFS attachment/UUID/mount classifier, automatic Git trust or replacement bridge. Native and generic ACP existing behavior remains. Claude/Codex/Grok configured skills use private execution-owned profiles on every filesystem, exact acquisition before await and close-before-release. No bindings means no acquisition and no project fallback.
The latest five unused imports are not the full test scope; cumulative extraction and decoupling are assessed.

## Changed boundaries
| Boundary | Change / evidence choice | Limit |
|---|---|---|
| Independent module/build/distribution | N root archive, real toolchain, source hash/manifest/four-target builds and refusal fixtures | Cross compilation is not target runtime or publication qualification |
| Host orchestration/persisted admission | Go actual readers/locks/files, doubled privileged engine/mount commands | No live mounts, root administration or predecessor live upgrade |
| Ordinary registered workspace/runtime/PTY | Source removal audit plus current runtime tests, local socket APIs and native PTYs | No storage/mount-loss contract or old VM acceptance campaign |
| Runtime profile preparation/native process close | Real temp files/symlinks, production bootstrappers/owners, Codex/Grok owned native process fixtures and Claude client mocks | No authenticated provider inference claim |
| Launcher | Real Bash + doubled Docker command, generic paths/private volumes | No live Docker/platform qualification |
| Guide | Factual copy, null release/disabled state; component/localization tests + unchanged IR001 current-component EN/zh render evidence | No new Electron/native-shell surface; installed app untouched |
| Worker/distributed/authenticated providers | No newly supported distributed/provider behavior | Out of scope, not Passed |

## Project execution discovery
Read N AGENTS.md, TESTING.md, DESIGN.md, README.md, root module/packaging/source-lock instructions; S AGENTS.md, TESTING.md, DESIGN.md, server/web AGENTS.md, package scripts, server vitest.config.ts and relevant test fixtures. No closer TESTING overrides found for changed owners.
N TESTING requires an independent archive, private HOME/TMPDIR, Go1.27.2 CI toolchain, race/vet/Python/actionlint/shell; direct installed privileged CLI is prohibited. S documented test:integration:prepare builds current prerequisites; frozen install must include application-backend-sdk/devkit/Brief Studio script dependencies, not only import graph.
Environment: own home/tmp/cache, explicit environment with no inherited app/provider credentials. Canonical real HOME/TMPDIR paths avoid /var vs /private alias errors. N source under owned home scratch, not /private (source security tests reject that location). No service secret needed; tests select ephemeral local ports. Dependencies downloaded only to own scratch. No live app/VM/node stop or user data mutation.
N/S assigned roots and exact commits/source hashes are captured in evidence/api-e2e/api-rev-001/input-audit.json. D0 unborn main/PM files and retained engine candidate are read-only/protected. No remote/target finalization.

## Persisted data and legacy removal
Directly Usable — No Migration for host-only active/pending records with absent/null/empty Nodes. Current writes omit Nodes. Meaningful/malformed predecessor obligations refuse under admin lock before binary/resource effects. Only active/pending records inspected, irrelevant additive fields and history remain inert. Exact state/source/binary preservation and lock ordering are required.
Application registration/history/private memory are not migrated. Known registered resolution errors propagate; only absent/unknown selection retains ordinary fallback. Retired public descriptors are inert, not deletion targets.
Implementation Legacy/Compatibility and Persisted Data sections agree with R2; no ambiguity requiring reroute found.

## Existing durable coverage validity
| Path/group | Decision | Why / action |
|---|---|---|
| N internal/config/installation_state_test.go; internal/cli/install_state_test.go; internal/setup/standalone_state_test.go | Still Valid | Actual trusted readers, absent/empty/null/additive/malformed/duplicate/node obligations, exact current writers, lock/refusal-before-effect; execute |
| N setup/source-binding/backend/platform/service and Docker engine tests | Still Valid | Host source/pending/permissions/drained detach/engine lifecycle remains required; execute race/vet |
| N scripts/tests/test_nfs_*.py and CLI release/permission tests | Still Valid | Extracted root tooling/gates; child fixture skip is covered by Go invocation, not silently Pass |
| S registered-workspace-resolvers/native-workspace-resolution/workspaces/terminal | Still Valid | Ordinary path/error and no known-ID fallback assertions; execute |
| S prepare-private-runtime-skills/runtime-skill-profile/private-skill-bootstrappers | Still Valid | Real files, pre-await ownership, no bindings/no fallback, aliases/collision/source preservation |
| S codex-private-profile-process/grok-private-profile-process; Claude/Codex factories/session cleanup/cancel tests | Still Valid | Native owned process boundary plus deterministic failure/close controls; no paid provider needed |
| S workspace-content-rest/GitHub sources/private packages/local run/PTY websocket | Still Valid | Real local transport/build/filesystem/PTY compose current owners; execute after prerequisite build |
| S generic launcher and Guide/localization suites | Still Valid | Generic volumes/stop remain; NFS bridge gone; release remains null |
| Deleted binding/automatic Git/project-materializer/paired attachment fixtures | Replace / already removed by IR001 | R2 explicitly removes old assertion; ordinary path and private profile tests replace it; no further removal here |
| Live authenticated AGY/Claude/Codex/Grok/platform/old editor/VM tests | Out Of Scope | Not accepted behavior changes for this extraction; record skips honestly |

No new durable coverage gap established after source/test inspection. Plan: retain and execute existing current tests. If execution exposes a genuine uncovered current requirement, update this investigation before adding narrow regression coverage. No production edits.

## Execution plan and ledger
api-e2e-test-case-ledger.md owns E01, N01–N03, S01–S06, E02. Narrow affected checks precede broader affected suites; preserve all attempts. Commands, cwd, explicit environment, timing, exits and log paths are persisted by the evidence runner. Each terminal attempt updates the ledger before the next case.
Temporary probes: archive/source/license/removal audit; exact retained arm64 manifest/embed; cleanup/hash audit. These packaging/integrity experiments are ticket evidence, not duplicate test architecture.

## Confidence and broader-validation decision (initial)
Not yet scored: no API execution in this task. Required first: repository tests and real local process/API/PTY suites. After those, score all seven categories and choose additional validation only for a material remaining boundary gap.
Browser not selected initially: only factual Guide copy/null-release presentation changes, already rendered on exact current Guide source by IR001. Verify unchanged inputs and fresh component/localization assertions before relying on that carried presentation evidence. No shell-specific change, no desktop launch needed.
No manufactured physical/provider/platform qualification. AC007 remains downstream verification, not API-owned or waived.
Proceed: Yes. Durable additions/updates/removals planned by API: None. Reroute before execution: No.
''')
def snap(root):
 entries=[]
 for p in subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split('\0'):
  if not p or p.startswith('tickets/'):continue
  f=root/p
  if f.is_file():entries.append([p,hashlib.sha256(f.read_bytes()).hexdigest()])
 return {'root':str(root),'head':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),'paths':entries}
audit={'N':snap(N),'S':snap(S),'authority':'Approved R2/SR003, Ready SR004, ARCH002, CRR002','service_source':'83726b27400b405a7a6a79bd962d8e2419daa561','initial_status_N':subprocess.check_output(['git','-C',str(N),'status','--porcelain'],text=True),'initial_status_S':subprocess.check_output(['git','-C',str(S),'status','--porcelain'],text=True)}
(E/'input-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(E/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
print(E)
