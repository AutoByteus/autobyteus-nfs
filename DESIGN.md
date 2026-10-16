# AutoByteus NFS design principles

Implement supported behavior through existing owners; keep the smallest coherent
change and explicit trust/ownership boundaries. `cmd` dispatches to `internal/cli`
and setup; config owns bounded persisted data; platform/backend/docker own their
existing system integrations. Do not add frameworks or fallback paths for
speculative scenarios. Preserve refusal/security guarantees, not accidental
repository coupling. Remove obsolete paths and dependencies when replacing them.

Repository location and Go import names are not installed-state addresses.
Preserve CLI/descriptor fields, source/mount identity, permissions, admin/drain
consent, private state and owned detach/recovery semantics. No implicit migration,
live export/mount/node mutation, recursive permission change or local fallback.

Service source/build/tests must not need an AutoByteus app checkout or vendor app
implementation. Optional deployed app-node probes remain intentional contracts,
not build dependencies. See [integration contract](docs/integration-contract.md).
Changes to that contract need explicit consumer evidence, not mutable network
lookups in ordinary tests. Keep engine recipe/pin/provenance and publication
qualification distinct from a successful local build.

Validate at the affected boundary with owned scratch and truthful limitations.
Cross-compilation, synthetic fixtures and historical results do not qualify
runtime platforms. Follow TESTING/RELEASE; no silent expansion of approved scope.
