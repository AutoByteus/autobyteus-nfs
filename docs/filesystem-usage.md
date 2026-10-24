# Filesystem usage boundary

AutoByteus NFS owns host create/connect/status/reconnect/drained detach. It exports
one selected source in place, or mounts the explicit Connection supplied by a
storage computer. Source identity, private state, marker, mount source/protocol,
nonroot permissions, allowlist and busy-detach safety remain internal obligations.
Docker is only an optional Linux Ganesha storage-engine backend.

The boundary to every consumer is an ordinary filesystem directory. There is no
application attachment protocol, server JS probe, application HTTP readiness API, launcher
query, selected-node discovery or automatic container recreation. No application
checkout, consumer fixture pin or test-time network lookup is needed.

Operators provision storage and map directories outside applications. An app uses
its selected path and normal filesystem results/errors; it neither classifies
local/mounted/NFS storage nor detects an absent mount that leaves a directory.
Hard NFS can stall I/O; there is no local substitute, force-unmount or outage
isolation guarantee. Do not depend on remote watcher events or same-file merging.

For Docker consumers, use the consumer's documented generic bind mapping. In the
AutoByteus launcher, AUTOBYTEUS_DOCKER_SHARED_WORKSPACE_DIR is a **host root**:
shared/ and nodes/<name>/ children are mapped; it is not an arbitrary NFS mount
root automatically bound wholesale. Private application volumes remain separate.
Changing old specially attached deployments requires explicit operator drain and
reconfiguration outside this source task. No live deployment/migration is run.

The local source hash attests this service's declared files and engine inputs,
not application bytes or readiness. Release readiness is separate from deferred
field/filesystem/user validation. Historical
filesystem evidence, fixture checks and cross-compilation are not new runtime or
physical/publication qualification. See ../packaging/RELEASE.md.

Source-built `server`/`client` dashboards are local NFS-management entry forms,
not consumer admission APIs. They preserve the same host-state/source/permission
and detach boundaries. Their authenticated loopback listener is ordinary-user;
terminal approval starts the root-installed same-binary private helper. See
[dashboard usage](dashboard.md). Published v0.1.0 does not contain this UI.
