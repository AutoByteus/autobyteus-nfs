# AutoByteus NFS design principles

Implement supported behavior through existing owners; keep the smallest coherent
change and explicit trust/ownership boundaries. `cmd` dispatches to `internal/cli`; terminal, helper and installed supervision
share the root `internal/admin` operation owner; config owns bounded persisted data; platform/backend/docker own their
existing system integrations. Do not add frameworks or fallback paths for
speculative scenarios. Preserve refusal/security guarantees, not accidental
repository coupling. Remove obsolete paths and dependencies when replacing them.

Repository location and Go import names are not installed-state addresses.
Preserve host source/mount identity, permissions, admin/drain consent, private
state and safe detach/pending recovery. The current product is host-only: no
application node/descriptor/HTTP/installed-module protocol or launcher coupling.
Consumers use ordinary filesystem paths, not service metadata.

Persisted state: current writers emit exact host records and readers tolerate
irrelevant additive fields. Active/pending predecessor node obligations are not
irrelevant: a bounded read-only config admission refuses nonempty/malformed lists
under the administrative lock before binary replacement or resource effects.
No history scan, migration, deletion or legacy execution path. Absent/node-free
state remains usable; operators recover incompatible state with its matching tool.
Service source/build/tests need no AutoByteus checkout or paired fixture. Keep
engine recipe/pin/provenance and publication readiness separate from field qualification.

Validate at the affected boundary with owned scratch and truthful limitations.
Cross-compilation, synthetic fixtures and historical results do not qualify
runtime platforms. Follow TESTING/RELEASE; no silent expansion of approved scope.

The embedded dashboard is private local **NFS management**, not an application
readiness API. Its HTTP listener, directory chooser and opener are ordinary-user
operations; only the same-binary private-pipe helper administers storage after
terminal sudo approval. Keep the exact root plan and global lock together through
review/commit/cancel. `admin.Session` owns complete serial service reconciliation
and completion-relative retry as well as explicit operations; do not restore a
callback driver or acquire a second lock around the shared setup reconnect.
