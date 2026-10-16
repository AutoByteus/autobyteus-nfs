# Installed AutoByteus integration contract

This document declares the service-owned boundary, not a copy of application
implementation. Repository relocation does not change installed paths or JSON.
The fixture [testdata/attachment.json](../testdata/attachment.json) is the exact
producer contract example, parsed by Go tests. The AutoByteus consumer keeps an
identical local fixture with `{repository, commit, path, sha256}` provenance and
uses its actual TS parser offline. Updates require reviewed paired equality and
producer/consumer checks; ordinary tests do not fetch mutable main.

## Descriptor and identity

`/etc/autobyteus-nfs/attachment.json` exposes five nonsecret fields:
`storageId`, `endpoint`, `export`, `protocol`, `mountRoot`. The default mount root
is `/Volumes/autobyteus-shared`; protocol is `3` or `4.1`. This descriptor is not
proof of a mount. Consumers check actual mounted endpoint/export/protocol and
`.autobyteus-nfs/storage.json` storageId, refusing a local substitute or wrong
identity. Private root-owned state stays under `/var/lib/autobyteus-nfs` or
`/Library/Application Support/AutoByteusNFS`, never in the public descriptor.

## Launcher boundary

The installed user CLI is `~/.local/bin/autobyteus-nfs`.
`launcher-attachment --nodes <node>` emits exactly seven ordered lines after
trusted configuration checks:
1. storageId
2. mountRoot
3. Docker volume name
4. public descriptor directory
5. Docker daemon ID
6. export device
7. mount options

Per-node opt-in references remain `/etc/autobyteus-nfs/nodes/<node>.json`. The
application launcher checks daemon and actual owned volume and binds the descriptor
directory read-only; no source checkout is consulted. CLI flags, state schema,
private executable paths, drain/administration consent, ownership, source/marker
binding and restart/refusal/detach behavior are unchanged by repository moves.

## Optional managed application nodes

Selected-node integration deliberately checks the deployed supervisor/UID and
`/app/autobyteus-server-ts/dist/workspaces/shared-workspace-binding.js` inside the
actual node, and uses existing readiness/API probes. Those deployed strings are
not build-time sibling dependencies and must not be removed to claim independence.
Unsupported nodes refuse before destructive changes. The app owns its source,
launcher, parser and disabled/unpublished NFS Guide; this repo owns the service.

## Qualification boundary

The local source hash attests NFS-owned source plus this declared contract, not
arbitrary AutoByteus bytes. Future managed-node/physical publication evidence
must name tested service sourceHash/commit, engine identities and exact AutoByteus
consumer commit/image identities. The app's release/Guide decision separately
validates its pinned consumer. Historical one-VM/shared-kernel filesystem proof,
synthetic fixtures or compilation do not qualify other combinations/platforms.
The default qualification lock remains empty. No runtime metadata schema or
network fetch is added for this documentation/test provenance.
