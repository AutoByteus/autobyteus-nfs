# Design — Standalone NFS setup dashboard

## Solution and approval basis
Package `nfs-setup-dashboard`, Task `autobyteus-nfs-2` / `project_task_f1264eb8-5a99-4a19-949f-09d141c955a1`.
**SR-002 — Architecture Design Complete / Ready for independent review**, not yet reviewed or implementation-approved. Requirements **R1/SR-001 Approved** by Solution Designer within explicit user direction; conversation notification and exact basis in requirements-doc.md. No behavior supplement or separate Product deliverable.
Workspace `/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-setup-dashboard`, branch `codex/nfs-setup-dashboard`; fetched base/target `origin/main` **52c17fb5480d23b89752a8ae201419e356b4c3fc**. No release authorization.
Canonical evidence: `tickets/in-progress/nfs-setup-dashboard/investigation-notes.md`.
Authorities read 2026-10-24: architecture-design, latest design-principles/design-examples (examples2/4/8; cases1/2/3/7), finding-the-cause, ticket-scope, handoff, latest design template; current project AGENTS/DESIGN/TESTING/RELEASE. No principle conflict. Project's prohibition on application HTTP protocols remains: this is private local **NFS management**, never an application readiness API. Clarify that wording in own NFS docs.

## Intended change and current-state read
Add two role commands and a bundled local browser interface over the existing storage operations. Today CLI `run.go` owns root installation, lock, pending selection, Docker handle and operation sequencing, while `setup.Service` owns storage plan/apply/recovery invariants (E02–10). Duplicate that orchestration in a web handler and two policy owners would diverge. Extract the coherent root administrative lifecycle into `internal/admin`; terminal and a private pipe adapter use it. Keep actual NFS/config/backend implementations and their protections in place.

The HTTP listener and directory chooser run as the ordinary user. A child instance of the **same root-installed program**, started only after explicit OS administrator approval, accepts a bounded private-pipe protocol. No root HTTP listener, shell commands from HTTP, public API, new daemon or password form. Existing installed storage supervisor remains independent.

## Change Scope
In scope UC001–005: role dispatch; nonroot HTTP session/browser launch/directory choice; typed private IPC; shared root operation/plan lifecycle; embedded assets and UI; narrow current CLI/supervisor caller migration; security/lifecycle/host/browser tests and NFS documentation/developer checks. Source identity automatically covers assets under `internal`.
Derived consumers: CLI text/JSON, new UI view, helper wire DTOs, installed service caller, tests, source-hash/build and docs all get explicit decisions below. No persisted field or Connection schema change.
Deliberately untouched: application/superrepo/skills/Guide/PM boards; backend engine policy, source/identity/mount/cache/permissions implementation unless a directly demonstrated integration correction is necessary; release lock/readiness/published metadata/signing/installer/release workflow; old ticket archives/candidates. No multiple-share, remote-control or discoverability contract.
Follow-ups: None identified. Stale app-Guide/qualification wording in touched README/filesystem usage is corrected to truthful standalone scope; not a reason to alter the app.

## Task size and architectural risk — completed-design classification
- **task_size: Large**: new frontend/transport plus privileged IPC and common admin lifecycle across CLI/service, embedded build coverage and two-OS isolated host validation. Approximately 15–20 new production files and several existing caller/docs/tests, not a two-command alias.
- **architectural_risk: High**: materially new browser authorization and privilege boundary, administrative process/plan/lock concurrency and safety-critical lifecycle. No schema migration, but mistakes can alter host exports/mounts.
- Escalate to Solution Designer for changed privilege model/public surface/platform/schema/required authority, changed backend safety, or source-built artifact admission that needs release-policy changes. Missing test resources are precise external blockers, not authorization to bypass.

## Architecture investigation evidence
E02–12 in investigation notes contain exact file/line references. After R1 approval, production caller search confirmed only CLI run.go and interactive-setup.go coordinate `setup.Service`, including the service callback. Inspected private serializers, fixed job/probe owners, installer exec/env and actual recursive source hash. Installed sudo manual supports descriptors0/1/2 and terminal authentication; real nonroot pipe/flock premise probe recorded. These support the structure but do **not** prove the proposed sudo/UI implementation. Primary Go CSRF source shows why token and exact Host/origin checks are additionally required. Browser API contract explains directory-only local chooser. Remaining implementation gates: native sudo/PTY/EOF/signals, browser bootstrap, embedded assets and actual isolated operations.

## Behavior and production-path map
| Behavior | REQ / AC | Existing evidence | Target change/preservation | Spine |
|---|---|---|---|---|
| BEH001 | 001,009 / 001,007 | E02–03 | server/client branch before ordinary elevation; launch nonroot local UI; legacy terminal entry forms still supported, not compatibility fallback | DS1 |
| BEH002 | 002,006 / 002,006 | E04–05 | Server draft → OS authorization → root exact plan → review/commit → existing Apply and observed result; same in-place source/self-mount | DS2 |
| BEH003 | 003,006 / 003,006 | E04–05 | Client Connection parse/local target → root plan/review/commit; no guessed identity or generic shell | DS2 |
| BEH004 | 004–005,007 / 004–005,007 | E06–10 | Separate metadata from readiness; explicit active/pending reconnect; reviewed drained detach; no automatic repair | DS3 |
| BEH005 | 006–008 / 006,008 | E03,09 | Exact HTTP authorization → bounded typed IPC → root admin authority → setup; browser cannot submit Plan/User/Store/command | DS1–4 |
| BEH006 | 007 / 007 | E09–10 | UI session stop vs plan cancel vs running operation vs installed storage job are distinct; lock retained across children | DS4 |
| BEH007 | 008,010 / 008 | E01,11–12 | Existing store schema/runtime/releases unchanged; embedded new UI in next source build; published v0.1.0 not claimed to contain it | DS5 |

## Task design health assessment
Feature; **Boundary Or Ownership Issue would arise if added naively**: root lifecycle is coupled to terminal prompting in run.go:75–178 and interactive-setup.go:11–56. Existing setup backend is not diagnosed defective. Triggers: new entry form otherwise duplicates lock/config/Docker/reconnect/job/error sequencing, and root-only CLI dispatch would accidentally elevate HTTP. Required bounded refactor **Yes**: one root `admin.Session` operation owner replacing that CLI sequencing; thin terminal/pipe adapters only. Source/config/backend policy stays with current owners. No general command bus, plugin framework, storage rewrite or >500-line “dashboard server” god-file. No existing dead path proven outside scope; do not remove unrelated code. New authority is intentionally narrow; root and browser lifetimes are the residual high-risk boundary requiring review.

## Terminology and state decision
- **Server**: storage role (`HostedFilesystem` plus its own local attachment), not the HTTP listener.
- **Client**: mount-only storage role. **Connection** retains current JSON meaning, not auth token.
- **Dashboard session**: unprivileged process + browser authorization + one child-helper lifecycle.
- **Admin session**: root owner of current private IPC connection; idle is not an administrative lock.
- **Plan lease**: process-local exact operation + opaque random ID + held lock + expiry, never a browser-authoritative or persisted Plan.
- **Operation**: one admitted host check/change, distinct from HTTP request or stored installation ID.
- **Readiness**: observed result of `setup.Status`, not “configured” or helper authorized.
One meaning/name across UI, HTTP, IPC and code; do not call all of these `sessionId`/`status`. No project glossary currently specified; define these in dashboard design documentation, not a new global framework.

### Persisted data / transition
**Directly Usable — No Migration.** Existing root-private `attachment.json`, hosted-filesystem, pending-setup, docker-endpoint, resource and recovery receipts keep their current bounded schemas/meaning/readers/writers (E07,E09,E12). Source marker/identity unchanged. Normal new UI calls create these records through setup only. Existing fixtures, current structs/readers and serializers show no shape change required; no live data was inspected. Dashboard token, operation response, draft and lease remain ephemeral; no new READY flag, auth file under service store or history scan. Losing unsubmitted UI/session state is acceptable; pending applied intent is not. Existing node-obligation admission continues to refuse before installation/effects. Migration conventions therefore need no transformation/startup-gate extension.

## Spines, narratives and ownership
| Spine | Scope / actual order | Governing owner and narrative |
|---|---|---|
| DS1 | CLI role launch → dashboard.Session → loopback HTTP/static page → browser authentication → form | dashboard.Session owns listener, per-launch authorization, opener and shutdown. It does not install/root-plan until explicit authorize. Browser is presentation/input, not storage authority. |
| DS2 | Browser draft → dashboard.Session → adminwire pipe → admin.Session.BeginServer/BeginClient → setup.Plan → review DTO → browser confirm → admin.Session.Commit → setup.Apply → setup.Status → operation result | admin.Session owns root operation order and the exact retained plan. It directly calls setup and the existing platform mechanisms; no callback lets a downstream component call back into upstream coordination. |
| DS3 | Browser inspect/recheck/reconnect/disconnect → dashboard.Session → admin.Session → private config / setup.PendingPlan or Reconnect or Detach → outcome | admin.Session differentiates cheap installed metadata from potentially blocking readiness. Role/pending/current selectors are explicit. Same owner serves CLI callers; service reconciliation remains noninteractive and never pending-resumes. |
| DS4 | auth/IPC/plan input → session loop → state transition → one worker/result → browser polling | Each session owns its bounded loop. Cancel-before-commit releases lease. Running filesystem calls are not aborted on an HTTP disconnect. Stop rejects new work, drains what is active and releases only safe resources. |
| DS5 | Go build → embedded web resources → same binary/root helper identity → normal packaging hash and checks | Existing Go/build/release owners; no new asset service, runtime compiler, installer publication or release channel. |

Return spine: root typed event/reply → IPC reader → dashboard operation snapshot → authenticated browser poll → status/error rendering. Nonroot directory selection is a bounded local concern of dashboard.Session, not a root filesystem API. UI/HTTP requests query cached operation state quickly instead of calling NFS in handlers.

| Main node / facade | Owns | Must not own |
|---|---|---|
| cli.Run and terminal adapter | Parse/route, terminal prompts/text/JSON, OS approval bootstrap | HTTP policy, duplicate root lifecycle/backend implementation |
| dashboard.Session | Local auth, HTTP request serialization, child lifetime, current operation responses and browser events | sudo password, persisted NFS state, actual setup policy |
| admin.Session | Root private-store/lock/Docker resource scope, exact plan, typed operation admission and order | HTTP, browser rendering, arbitrary command dispatch |
| setup.Service | Plan/apply/source/pending/reconnect/detach/readiness invariants | UI session token, presentation, opener |
| platform/config/backend/docker/service | Their existing trusted OS/state/engine/probe/supervisor mechanisms | App node/launcher control |

## Interface boundaries and security contract
### DS1 — nonroot launch and browser
1. Parse exact server/client; reject setup flags (`--yes`, `--source`, etc.) on these launches rather than silently applying hidden inputs. Existing commands unchanged. Call CheckHost. Require ordinary user and launching TTY for administration; never open a browser under sudo/root. No rootless “read-only fallback” that later bypasses controls.
2. Bind **tcp4 127.0.0.1:0**. No `--listen`, LAN wildcard, proxy, remote URL or port-forward feature. Pin actual literal host+port for request validation. Embed assets with `go:embed` below `internal/dashboard/web`; serve an explicit allowlist, not a directory on disk.
3. Generate >=256-bit random launch secret. Avoid putting it in OS opener argv: write a task-process-owned bootstrap HTML (0600 inside newly-created0700 private temporary directory) that navigates to the exact local URL with secret in fragment. Open the **file path**, not a secret URL, with fixed `/usr/bin/open` on Mac or installed `xdg-open` on Linux as ordinary user; no shell interpolation. File association failure/editor opening is an opener failure, not success: terminal also gives the local browser URL for deliberate manual opening. No promise to override OS browser associations. Delete private bootstrap after authentication or shutdown; never log/commit it. User terminal may display the private fallback URL, not a server/access log. Real browser tests must cover bootstrap and fallback; if OS file handling fails, truthful fallback is required.
4. Page consumes fragment, immediately removes it with replaceState, then exchanges it via POST `/api/session` for a separate random session bearer token. One successful exchange per launch; unauthorized retry/guess gets generic refusal. Session token is tab-scoped (`sessionStorage` for reload) and cleared on explicit stop; expires with this process. No cookie, localStorage, persistent credential, remote analytics/CDN/service worker or URL query token. Same-user compromised code/root/browser extensions are not the threat boundary; untrusted web origins/unauthorized LAN/other-user requests are. The private launch file prevents routine process-argument exposure to other users.
5. Every API except the one-time exchange requires constant-time bearer verification. Exact Host validation on **all** routes; explicit exact Origin for POST, reject `null`/foreign origins and cross-site metadata. Authenticated GET validates Origin if present and denies cross-site Fetch metadata. No CORS/trusted-origin exemptions. Add Go CrossOriginProtection defense-in-depth, but do not rely on its safe-method/missing-header allowance as authorization. Ignore forwarding headers as authority. Unknown route/method →404/405 with no effects; OPTIONS does not authorize anything.
6. CSP self-only script/style/connect, no inline/eval, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'none'`, Referrer-Policy no-referrer, X-Content-Type-Options nosniff, Cache-Control no-store for API/session and sensitive state. Render filenames/errors/JSON with textContent, not innerHTML. No token or sudo/stdin logging.
7. Enforce body32KiB, header8KiB, read-header timeout5s and finite ordinary HTTP request timeouts; no long-lived HTTP handler awaits NFS. Strict typed JSON with unknown/duplicate keys/trailing document rejection at new HTTP/IPC boundary. Existing installed/config additive-field policy remains untouched. Connection data still parsed by config.ParseConnection with16KiB bound.

### Local chooser
Directory-only listing as ordinary UID, not root. Explicit selected path, home starting point, parent navigation, real-directory entries only; no recursive scan, contents, download, write, chmod or mkdir. Show canonical path; omit symlink entries and do not silently resolve a chosen noncanonical source into an approved different source. Existing source/path safety revalidates root-side. A new source is a typed single child under an existing parent, only created later by setup.Apply's nonroot child. Mount path is a field with default `/Volumes/autobyteus-shared` and optional parent chooser; warn that an existing writable/nonempty target is not suitable.
Bound listing to200 entries/one outstanding listing, with “too many—enter path” indication; don't accumulate unbounded goroutines. Directory I/O may itself block on a user-selected mounted path: use a separate bounded asynchronous listing slot, keep HTTP/operation status responsive, never claim timeout cancelled an OS call. No root escalation to bypass listing permission; manual field remains available.

### DS2 — OS approval and private IPC
- Browser Authorize action explicitly explains root-binary installation/use, private state and terminal prompt. Only this action starts `/usr/bin/sudo -- <resolved current executable> internal-install internal-dashboard-helper <fixed-role>` with **stdin/stdout as anonymous pipes**, stderr/OS prompt at launching terminal. No -S, askpass, password JSON or shell. Normal sudo cached-credential policy remains OS-owned; consent is still required when no password is requested.
- Reuse installRootBinary admission/lock/trusted path/environment, not a second installer or bypass. Existing install creates private state/root executable: these are disclosed administrative effects, separate from sharing consent. A denied/cancelled sudo returns authorization failure, never triggers automatic retries.
- Internal helper dispatch occurs before public parser; requires euid0, trusted root installed executable, correct invocation arity/role, real initiating nonroot user resolved from sudo identity. No HTTP-supplied UID/GID/home/release/binary/store/socket-address authority. Root helper opens **no listening socket** and speaks only inherited standard pipes. Transport carries no password.
- Handshake binds protocol version, role and executable digest to the launching executable. Compute digest of executing/source binary before install and root-owned target after install; mismatch refuses. Under each operation lock check installed target still matches helper digest before spawning internal probe children. If changed, close helper/re-authorize; do not run one version's parent with another version's probe. No change to release qualification semantics.
- Helper idle timeout15min (only when no lease/operation); UI shows authorization expired and allows a new explicit authorization. No permanent privileged management service. Release root resources on pipe EOF when idle; cancel a review lease on EOF. Never exit/delete state to pretend an active apply/check has rolled back.
- `adminwire` current protocol is internal to this exact same binary; no compatibility version branches. Messages carry protocol version, request ID, **specific operation kind** and its typed payload. Frames32KiB request/64KiB reply; bounded error/summary output (truncation explicitly flagged, no omitted safety summary may be approved). Unknown version/kind/fields, duplicate IDs or malformed frames refuse/close without dispatch. Never send serialized setup.Plan to be trusted back. Error responses separate machine code from literal user-visible detail and `effectsMayHaveStarted`.

### Root methods / plan lease
| Method or message | Accepted input / identity | Owner action |
|---|---|---|
| InspectConfiguration | no browser path/record selector | Acquire existing nonblocking lock; read-only CheckStandaloneState, current typed attachment/hosted/pending summary; release. Classify empty/client/server/pending/refused; no mount traversal/probe. |
| BeginServer | source, endpoint, allowlist, backend, mountRoot, optional existing local Docker socket | Acquire lock; set initiating User; resolve fixed store/binary/release; validate role/config; open validated local Docker handle if chosen; call setup.Plan. Return display-only review and opaque lease ID. |
| BeginClient | bounded Connection JSON + optional local mountRoot | Same root owner; ParseConnection and set local override before Plan; never accept hosted config or identity override outside that contract. |
| BeginReconnect | matching role, no new source/endpoint/config | Lock/read current state; PendingPlan if pending, otherwise saved-attachment reconnect review. No auto pending resume or stale reconstructed plan. |
| BeginDetach | matching role, no arbitrary target | Lock/read current or supported pending scope; review affected mount/export and data-retention/drain notice. No host readiness probe required just to allow safe detach. |
| Commit | exact lease ID + explicit consent, and drained=true for detach | Reject expired/foreign/consumed lease; mark consumed **before** effects. Apply retained Plan, or Reconnect+InstallJob, or Detach. Only setup's existing trusted operations execute. |
| CancelReview | exact lease ID | Only before commit; discard lease, close Docker handle and administrative lock. No storage changes/cleanup. |
| CheckReadiness | no paths | Fresh locked setup.Status and result; explicit user action, not automatic polling. |
| Close | no data | Reject new work; cancel review or drain active operation; terminate idle helper only. |

**At most one root operation/lease per admin session**, and existing global flock excludes other CLI/supervisor/helpers. Keep actual lock/service/Docker/Plan in root memory from Begin through Commit/Cancel. UI review expires after5min; expiry releases only a waiting lease, never a running operation's lock. Display deadline and warning “storage management is reserved during review”; supervisor's existing30s nonblocking retry may wait during review (E09–10). This preserves today's exact-plan-under-lock contract without a second optimistic-plan/hash/rebinding protocol. Do not persist lease IDs or bypass Apply's fresh source/target checks. If preparation itself stalls, it is an operation, not a ready lease.

New setup refuses any pending/existing config through existing Plan. Pending wins over active metadata for UI state. Wrong-role launch may display factual configuration but no new/commit/reconnect/detach action; show the correct short command. No browser role switch that mutates helper authority. Both CLI and UI root owners validate actual configured role, not a browser assertion. Legacy CLI semantics do not gain an opposite-role restriction where no role command was specified.

Initiating-user entry forms must remain explicit: new create/connect and the dashboard helper resolve the real nonroot user through the existing OS/sudo identity rule; browser input cannot choose it. The installed `service` entry has no SUDO_UID and must still work: its active reconnect uses stored attachment identity, never requires an interactive user or resumes pending. Root CLI status/detach similarly need no invented user. For pending resume that needs a source-home validation context, resolve the saved attachment owner through the OS user database and preserve its stored UID/GID; refuse missing/invalid identity rather than substituting root or the browser. Tests cover all these entry forms, not only new nonroot launch.

### DS3/4 — operation outcomes, concurrency and stopping
- dashboard.Session accepts one admin request, allocates operationId, returns202 and polls cached progress/result; root IPC reader updates that snapshot. Host filesystem work is never on HTTP handler goroutine. Repeated HTTP submit with same request ID returns that same operation; a different overlapping submit returns409. Root lease consume prevents duplicate commit even if UI races. Bound retained responses to current/last operation, not an ever-growing log.
- UI labels: Not authorized; Not configured; Configured—unchecked; Preparing/review; Applying/reconnecting/disconnecting/checking; Ready at timestamp; Incomplete/error; Authorization expired/disconnected. A completed Apply followed by failed Status is **configured/incomplete check**, not rollback. Connection details may be shown as configured, not proof readiness. Refreshing browser never automatically replays a mutation.
- Separate config observation from readiness. No periodic `setup.Status` every UI poll, no automatic reconnect when page opens. Operation state polling continues even if hard NFS blocks. Exact stage labels only where root owner actually enters a stage; no invented percentage. Before/after check timestamps distinguish stale result from current work.
- Stop dashboard / Ctrl-C: stop new requests, cancel uncommitted review, close auth/bootstrap/listener as appropriate, tell terminal if a host operation is still in flight. Wait for safe child completion; do not force kill, unmount, release inherited operation lock or declare cleanup complete while children may act. Catch orderly signals in helper; abrupt frontend loss closes IPC but helper drains the in-flight operation. Existing setup pending record and inherited child lock govern interruption; no additional transaction journal.
- Timeout/session expiry does not cancel committed filesystem work. A hung administrative child is reported with owned process details and recovery advice (restore storage); deliberate retention/blocker is honest. Subsequent invocation obeys existing global lock, not a “force retry” button. Idle helper and bootstrap/browser-private state are cleaned on success/exit. Browser tab close does not imply stop; relaunch/read state is supported. Dashboard process has no keepalive installed job.

## Encapsulation, interfaces and dependencies
| Boundary | Encapsulated mechanisms | Allowed callers | Forbidden bypass |
|---|---|---|---|
| dashboard.Session | HTTP auth + operation cache + private helper client + chooser | CLI launch, HTTP thin handlers | direct setup.Service, root Store reads, arbitrary exec |
| admin.Session | root store/lock/Docker scope, exact plan/reconnect/detach order | terminal adapter and typed pipe server | raw plan/user/path/command/Runner from HTTP; a second CLI copy |
| setup.Service | storage invariants and resource lifecycle | admin.Session; existing tested internal setup callers | web handler manipulating pending/source records |
| platform/backend/docker/config/service | OS/provider/state mechanisms | setup/admin under existing rules | browser daemon socket proxy, app-node container management |

Thin HTTP handlers validate/translate and call the governing dashboard session; thin pipe decoder calls root admin session. adminwire owns only transport schemas/constants/strict codecs, not policy. Dependency shape: cmd→cli→dashboard OR admin; dashboard→adminwire; admin→adminwire/setup/config/platform/docker/service; setup retains existing dependencies. No admin→dashboard, setup→HTTP or backend→UI cycles. Existing terminal.Service direct coordination is removed, not retained as a wrapper chain.

Boundary check: server setup/client setup have separate typed input shapes; reconnect/detach select only current installation, no ambiguous arbitrary IDs. LeaseId identifies a process-local exact review; operationId identifies one session operation; storageId remains NFS source identity. Session tokens identify browser authorization, never storage. All interface responsibilities singular; medium risk at wire/state mapping is controlled by named methods and negative tests.

## Off-spine concerns and capability reuse
| Concern | Serves owner | Reuse/extend/create and why |
|---|---|---|
| Host policy/paths/UUID/source safety | admin/setup | Reuse config/platform/setup unchanged; browser validation only advisory |
| Private lock, child execution, installed binary | admin + CLI privilege adapter | Reuse existing installation/lock/Commands/NonrootProbe; extend same-binary handshake only |
| Browser auth/origin/asset serving | dashboard | New because no HTTP surface exists; stdlib net/http/crypto/rand, no framework |
| Presentation/forms/copy | dashboard web assets | New embedded HTML/CSS/ES modules; no separate UI runtime/build server |
| Directory listing/opener | dashboard | Nonroot bounded local OS adapter, not root platform command API |
| Wire format/errors | both transport ends | New adminwire with one current schema; no duplicate JSON model in CLI/root HTTP |
| Logging | each owner | Stage/error facts without tokens/passwords/file contents; no new telemetry |
| Build/provenance | existing packaging | Reuse recursive internal hashing; tests prove web assets affect hash; no release-control redesign |

## File responsibilities and target mapping
Draft responsibilities are refined to the following final projection. No one-file-per-method scaffolding; split additional files only where a concrete concern grows. The layout separates transport/web assets from privileged domain coordination and existing providers.
| Path | Change / owner | Responsibility / prohibited contents |
|---|---|---|
| internal/cli/inputs.go | Modify thin CLI | Recognize server/client, validate launch-only arguments; preserve terminal parser contract |
| internal/cli/run.go | Modify thin dispatch | Role launch before elevation; internal helper dispatch; terminal/service delegate to admin owner; keep existing internal probe/verify handlers |
| internal/cli/interactive-setup.go | Modify terminal adapter | Collect/render/prompt, call common admin plan/commit; no local storage ordering |
| internal/cli/install.go | Extend privilege bootstrap | Reuse install/exec admission, support fixed helper route; no HTTP or alternate installer |
| internal/cli/dashboard.go | New entry adapter | ordinary user/TTY/host launch and fixed sudo helper process bootstrap plumbing |
| internal/admin/session.go | New governing root owner | operation/lease lifecycle, lock/Docker ownership, same-binary checks, close/drain; no HTTP |
| internal/admin/operations.go | New methods on same root owner | distinct begin/commit/status/reconnect/detach and service reconcile calls; single operation sequence owner |
| internal/admin/state.go | New owned projection | fixed private-record summary/role/pending, typed result/errors; no stored schema change |
| internal/admin/pipe.go | New thin root transport | strict framed message dispatch and result emission, no shell or second policy |
| internal/adminwire/protocol.go | New shared transport schema | current request/reply enums/bounds/codec; don't move config's persisted types here |
| internal/dashboard/session.go | New governing nonroot owner | auth lifecycle, helper/operation state, bounded submission/close |
| internal/dashboard/http.go | New thin transport | exact API route map, body/auth/Host/origin guards, cached responses; not NFS I/O |
| internal/dashboard/privilege.go | New private helper client | stdin/stdout framing/handshake/process wait; may use narrow launcher provided by CLI, never callback into root operation coordination |
| internal/dashboard/browser.go | New nonroot adapter | private launch file, fixed opener/manual URL, cleanup; no sudo |
| internal/dashboard/directories.go | New nonroot concern | directory-only bounded listing/path choices; no file content/actions |
| internal/dashboard/assets.go | New embed owner | explicit static allowlist/security headers integration |
| internal/dashboard/web/{index.html,styles.css,app.js,api.js,forms.js} | New web assets | labelled forms/review/status/render/copy and exact transport client; no NFS policy, secrets/logging, CDNs, framework dependency |
| adjacent *_test.go; internal/dashboard/__tests__/ | Add durable tests | current boundary/state/HTTP tests, isolated frontend browser harness (dev dependency only if necessary) |
| scripts/tests/test_nfs_dashboard_packaging.py | Add focused packaging regression | embedded asset inclusion/hash sensitivity and CLI no-runtime-dependency checks |
| README.md; DESIGN.md; TESTING.md; docs/filesystem-usage.md; docs/dashboard.md | Modify/add bounded docs | launch/auth/lifetime/safety/test instructions, standalone boundary; no old release availability overclaim |
| .github/workflows/ci.yml | Only if needed for deterministic UI test | developer checks only; no release/signing/manual publication operation |

Reusable structures: current config.Connection and setup.Request/Plan remain authoritative; `admin` result/review DTOs reference one current operation/role vocabulary; `adminwire` serializes only allowed projections, not arbitrary methods. Don't add redundant `ready=true` to configuration or duplicate path/UUID fields with competing values. UI displays server fields, does not rewrite policy. Stored `Attachment` consumers (setup/status/reconnect/detach/supervisor) unchanged; CLI moves to admin projections; tests protect same text/JSON outcomes where contractual; docs get exact new commands and source-only availability.

Folder check: `dashboard` is bounded nonroot management/control+transport with separate web asset depth; `admin` root domain-control/pipe boundary clearly separated from dashboard; `adminwire` transport only; existing setup/provider folders reused. Compact same-owner methods remain together instead of generic manager/helper/service chains.

## Removal / clean-cut replacement / compatibility rejection
| Remove/rewrite | Evidence/replacement |
|---|---|
| root lock/store/Docker lifecycle and direct setup switch in CLI run.go:75–188 | Move to admin.Session; terminal dispatch becomes prompt/output adapter. Do not retain second implementation. |
| interactive-setup.go constructing Service.Plan/Apply/Status directly | Common begin/commit/status owner; keep input presentation only. |
| old helper openSavedDocker in CLI after migration | Move one equivalent owned scope into admin; preserve surfaced error behavior where intentional, no dead leftover duplicate. |
| stale NFS-doc claims that the unrelated app Guide remains disabled | NFS repo describes own published CLI and source-built UI only; no app patch. |

Existing public `create/connect/...` and `service` are **not legacy fallbacks**: R1 explicitly preserves distinct terminal/headless and installed service entry forms sharing one policy. Reject a web controller that invokes CLI commands with --yes and parses their terminal output (loses exact plan authority and error/privilege separation); reject root HTTP, browser-side Plan persistence, generic exec/file API, fallback on failed source identity, a second stored dashboard config, or old/new wire compatibility branches. No obsolete runtime flow retained.

## Concrete shapes / applied patterns
Good: `BeginClient(Connection, localRoot) -> {leaseId, summary, expiresAt}` then `Commit(leaseId, consent=true)`; root retains Plan/lock. Bad: browser POSTs full `Plan{UserUID, Hosted, Binary...}` or arbitrary CLI string to sudo.
Good: UI GET operation returns “checking since…” while worker calls setup.Status. Bad: synchronous GET /status every second starts a new NFS probe or timeout marks ready.
Good: one `admin.Session` method owns acquire→admit→open Docker→setup→job/result→close. Bad: facade hands callbacks through three “coordinators” and both CLI and HTTP apply the sequence.
Patterns used: thin adapters; typed capability protocol; exact-plan lease over existing lock; bounded worker/state snapshots. No plugin registry/event bus/framework.

## Change/refactor sequence and proof gates
1. Add shared admin owner and tests; migrate terminal and supervisor coordination without changing setup/config/provider rules or CLI outputs. Pin current fixtures and all current entry forms. Remove duplicate sequencing immediately, no permanent dual path.
2. Implement helper protocol/bootstrap and ordinary-user role dispatch. Verify exact binary identity, privilege denial/TTY absence, malformed input, EOF/signals and lock behavior in isolated resources **before** connecting browser mutation controls.
3. Implement authenticated local server/embedded shell/directory chooser and browser bootstrap/fallback. Test genuine HTTP requests from correct/foreign origins and real browser; do not assume localhost or compile success supplies auth.
4. Forms server/client/review/status/reconnect/drain-disconnect; keyboard/copy/error/expiry behavior. Hook only typed commands. Existing state controls based on actual root inspect; no prefilled success fixtures in production.
5. Relevant native isolated execution and regressions; docs/test instructions; verify asset hashing and portable archive build. No change to v0.1.0 or publication gates. Update current source/intent only via normal recovery if a blocker reveals a requirement gap.
6. Hand off reviewed code to API per configured route; Delivery integrates fresh origin/main and verifies evidence/cleanup. No public version/tag/release.

### Validation matrix — obligations, not results
| Layer | Required scoped proof | Boundaries/limits |
|---|---|---|
| Current behavior regressions | Go race/vet/build/version, terminal parse/output/consent, root admission, source identity/pending/safe detach/job tests, Python packaging/Bash | Existing setup unit doubles stay labelled; no pretending native storage proof |
| Admin/IPC | Actual process and pipe transport, identical binary handshake, admin denial/noTTY, malformed/oversized/duplicate/unknown frames, lease expiry/replay/EOF, one global lock and inherited-child busy refusal | Run real sudo/root integration in owned guests only; injected Runner tests are complementary |
| HTTP/security | Real listening endpoint/browser; localhost-only/no LAN binding; Host/Origin/token/Fetch metadata/CSRF/form POST/preflight rejection; CSP/text escaping/private bootstrap/token hygiene | Browser fakes of root can prove transport but not privilege/storage |
| UI | Both roles at1280 and390, keyboard/focus/errors, directory selection/manual path, copy/failure, plan cancel/expiry, pending/wrong-role/error/slow work and reconnect/drain-disconnect | Actual browser program assets; deliberately doubled pending/denial states labelled separately |
| Host integration | Owned isolated macOS26+ guest and Ubuntu24.04 guest; actual UI/control-originated native server setup and client mount on appropriate hosts, real private source/sentinel bytes/identity, status/reconnect/drained detach; sequential existing Linux Docker server option on owned daemon | No live operator root store/NFS/Docker state; guest snapshots/source/network/process inventory and cleanup. Bounded virtual journeys are not physical/field campaign. No public port or host firewall/bridge modifications without separate authorization |
| Packaging | Same binary serves assets without checkout; local archive/build works; mutating representative JS/CSS changes existing source hash; four-target builds as suitable, native results only for actually run CPU/OS | No release workflow dispatch or public asset replacement. Plain development JSON lacks Linux packages; controlled local build must include measured current pinned engine/package metadata in disposable build tree and record new code hash, never call an old signed executable the dashboard build |

For native Linux Docker, use existing immutable engine contract on the isolated daemon; no new image publication. Reuse retained engine **read-only by verified identity**, or rebuild pinned engine in owned scratch, not a credentials/signing campaign. Guest setup may install pinned packages as disclosed test operations; no host installation. Owned test-only runtime metadata must identify the new build as development/unpublished with no released-target admission, while carrying actual measured current engine/package inputs; never label it the signed public v0.1.0 executable or weaken VerifyRelease. This metadata belongs in disposable build inputs/evidence, not a production release-lock edit. No particular VM utility assumed present. If required guest/OS/admin resources cannot be obtained within authorized isolation, report exact incomplete AC and resource blocker; do not use macOS15 CI as Mac26 qualification or substitute unit tests. Existing field-validation Task is neither silently passed nor a prerequisite for this new UI work.

## Risks, tradeoffs and implementation guidance
- Terminal sudo approval is a deliberate security/portability tradeoff instead of collecting passwords or shipping a privileged browser. UX must clearly direct focus there; no claim of entirely browser-only OS authentication.
- A5min review lock temporarily defers supervisor reconciliation; cancel/expiry releases it, applying operations have no fake deadline. Prefer this bounded use of existing contract over snapshot/rebinding complexity.
- Browser bootstrap through an OS HTML handler can fail; manual local URL is first-class and tested. Do not hide failure or leak secret in opener argv/logs to improve convenience.
- Hard NFS/OS calls may outlive browser/helper connection; operational cleanup may be deliberate safe retention with exact evidence, never force-unmount or parallel retries. UI responsiveness is not outage isolation.
- An embedded plain web UI keeps standalone runtime small; a developer-only browser test dependency is acceptable if bounded/documented, not a runtime/build prerequisite for Go binaries. No shelling into app/superrepo tools.
- R1 supports existing backends, not all imaginable browsers/hosts. Verify supported current desktop browsers and fallback; cite exact tested versions, CPU/OS and doubles.
- Production files should remain cohesive/readable; if one exceeds ~500 lines, split concrete concern within its owner, not arbitrary wrappers. No project design-case entry is due for a new feature; if a real design mistake is corrected later, suggest `docs/design-cases.md` because DESIGN currently specifies no location.
- Reproduction to start from: no bug reproduction/new UI exists. Baseline `Parse` rejects requested commands by E02 read evidence. Preserve existing tests then add new runtime witnesses; the narrow nonroot OS premise probe in investigation is not product acceptance.

## Readiness
R1 unchanged and approved, all supported scenarios mapped, no migration/security-policy relaxation or release implied. Design Ready for independent architecture review; **Large / High**. Main uncertainty is executable cross-process/native integration proof downstream, not missing user product choice. No implementation has started and no passing validation claimed.
