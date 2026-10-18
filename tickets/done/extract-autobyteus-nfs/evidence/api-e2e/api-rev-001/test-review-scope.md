# Proportional successful-test review scope

No API-authored production or durable test edits. This round executes the cumulative current R2 tests, not only IR002 import cleanup. CRR002 source Pass remains separate. This index selects the task delta; it is not a cumulative forwarding manifest.

N=/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs
S=/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs

## Current R2 durable coverage delta

### N relative to fc5d2ff3f404de3a683994766dfd47c258efb374

~~~text
M	internal/cli/cli_test.go
A	internal/cli/install_state_test.go
M	internal/config/config_test.go
A	internal/config/installation_state_test.go
M	internal/docker/docker_test.go
D	internal/docker/start_recovery_test.go
M	internal/platform/directory_modes_test.go
D	internal/setup/detach_nodes_test.go
M	internal/setup/hosted_config_test.go
D	internal/setup/reconnect_nodes_test.go
M	internal/setup/setup_test.go
M	internal/setup/source_binding_darwin_test.go
A	internal/setup/standalone_state_test.go
M	scripts/tests/test_nfs_installer_fixture.py
M	scripts/tests/test_nfs_source_identity.py
~~~

### S relative to 3712cd9bf0db998501d162db7f8655f169e3def6

~~~text
M	autobyteus-server-ts/tests/e2e/agent-definitions/agent-package-private-skills.e2e.test.ts
M	autobyteus-server-ts/tests/e2e/helpers/claude-live-agent-harness.ts
M	autobyteus-server-ts/tests/e2e/memory/codex-live-memory-persistence.e2e.test.ts
M	autobyteus-server-ts/tests/e2e/runtime/claude-agent-websocket-interrupt-resume.e2e.test.ts
M	autobyteus-server-ts/tests/e2e/runtime/codex-interrupted-compaction.e2e.test.ts
M	autobyteus-server-ts/tests/e2e/skills/github-skill-runtime-harness.ts
M	autobyteus-server-ts/tests/e2e/skills/github-skill-sources-graphql.e2e.test.ts
M	autobyteus-server-ts/tests/fixtures/codex-owned-terminal-cli.mjs
M	autobyteus-server-ts/tests/fixtures/grok-acp/fake-acp-agent.mjs
M	autobyteus-server-ts/tests/integration/agent-execution/claude-agent-run-backend-factory.integration.test.ts
M	autobyteus-server-ts/tests/integration/agent-execution/claude-session-manager.integration.test.ts
M	autobyteus-server-ts/tests/integration/agent-execution/codex-agent-run-backend-factory.integration.test.ts
D	autobyteus-server-ts/tests/integration/agent-execution/codex-thread-bootstrapper.integration.test.ts
M	autobyteus-server-ts/tests/integration/application-backend/brief-package-team-prompt.integration.test.ts
M	autobyteus-server-ts/tests/integration/runtime-execution/codex-app-server/thread/codex-long-turn-cadence.probe.test.ts
M	autobyteus-server-ts/tests/integration/runtime-execution/codex-app-server/thread/codex-raw-vs-backend-cadence.probe.test.ts
M	autobyteus-server-ts/tests/integration/runtime-execution/codex-app-server/thread/codex-thread-manager.integration.test.ts
M	autobyteus-server-ts/tests/integration/runtime-execution/codex-app-server/thread/codex-thread.integration.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/agent-provider-factory-builder.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/acp/acp-agent-run-backend-factory.test.ts
A	autobyteus-server-ts/tests/unit/agent-execution/backends/autobyteus/native-workspace-resolution.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts
D	autobyteus-server-ts/tests/unit/agent-execution/backends/claude/claude-workspace-skill-materializer.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/claude/session/claude-input-terminal-release.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/claude/session/claude-session-cleanup.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/claude/session/claude-session-manager.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/codex/backend/codex-thread-bootstrapper.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/codex/codex-input-terminal-release.test.ts
A	autobyteus-server-ts/tests/unit/agent-execution/backends/codex/codex-private-profile-process.test.ts
D	autobyteus-server-ts/tests/unit/agent-execution/backends/codex/codex-workspace-skill-materializer.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/codex/thread/codex-thread-manager.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/grok/grok-build-runtime-registration.test.ts
A	autobyteus-server-ts/tests/unit/agent-execution/backends/grok/grok-private-profile-process.test.ts
M	autobyteus-server-ts/tests/unit/agent-execution/backends/shared/prepare-private-runtime-skills.test.ts
A	autobyteus-server-ts/tests/unit/agent-execution/backends/shared/private-skill-bootstrappers.test.ts
A	autobyteus-server-ts/tests/unit/agent-execution/backends/shared/registered-workspace-resolvers.test.ts
D	autobyteus-server-ts/tests/unit/agent-execution/backends/shared/shared-workspace-resolvers.test.ts
D	autobyteus-server-ts/tests/unit/runtime-management/shared/scoped-project-git-environment.test.ts
D	autobyteus-server-ts/tests/unit/workspaces/shared-workspace-binding.test.ts
D	scripts/tests/test_nfs_engine_packaging.py
D	scripts/tests/test_nfs_installer_fixture.py
D	scripts/tests/test_nfs_packaging_and_launcher.py
D	scripts/tests/test_nfs_release_workflow.py
M	scripts/tests/test_public_docker_launcher_shared_workspace.py
A	scripts/tests/test_public_docker_launcher_stop.py
~~~

## Review emphasis
- N installation_state/install_state/standalone_state: actual lock/trusted bounded readers; no resource/binary side effect on refusal; exact host-only writer and additive-field direct-use policy.
- S private preparation/bootstrappers/runtime profile: no bindings/no acquisition; actual temp FS/aliases/project collision/current managed source; pre-await ownership and deterministic cancellation.
- Codex/Grok process fixtures use actual owned child processes but fake protocol/model; Claude close-error retry is a deterministic client double. No inference/native-provider qualification claim.
- Registered/native resolvers preserve selected identity and errors, no mount discriminator. Ordinary REST/GraphQL and actual native PTY/WebSocket proof is local, not NFS.
- Removed binding/Git/project materializer/paired fixtures assert obsolete R1 coupling; replacements prove R2. Generic launcher stop/mapping controls survive.
- Guide production component is unchanged; EN/zh text changed. IR001 renders carried only after byte equality; fresh 4-file/24-test component checks passed.
- Raw execution artifacts and AC proof table in canonical API report. No old shared-network-workspaces af9f23 test-review scope for this new task.
