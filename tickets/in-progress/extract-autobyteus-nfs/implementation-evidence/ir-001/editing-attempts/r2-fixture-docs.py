from pathlib import Path
import re
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
p=S/'autobyteus-server-ts/tests/e2e/agent-definitions/agent-package-private-skills.e2e.test.ts';s=p.read_text();s='\n'.join(l for l in s.split('\n') if 'codex-workspace-skill-materializer' not in l and 'shared/workspace-skill-materializer' not in l and 'import type { CodexAppServerClientManager }' not in l)
s='import type { RuntimeSkillProfile, RuntimeSkillExposure } from "../../../src/agent-execution/backends/shared/runtime-skill-profile.js";\n'+s
s=s.replace('  runId: string;\n  agentDefinitionId:', '  runId: string;\n  memoryDir: string;\n  agentDefinitionId:').replace('runtimeKind: RuntimeKind.CODEX_APP_SERVER,\n      workspaceId:', 'runtimeKind: RuntimeKind.CODEX_APP_SERVER,\n      memoryDir: input.memoryDir,\n      workspaceId:')
a=s.index('  // Codex discovers no skills');b=s.index('  const agentToolMcpRunSessions',a);s=s[:a]+s[b:]
s=s.replace('/** The enclosing factory owns acquired resources; this probe accepts every acquisition and keeps none. */','/** The probe registers each exact profile before acquisition and releases it at teardown. */\nconst profiles: RuntimeSkillProfile[] = [];').replace('  ownSkill: () => undefined,\n  ownCodexClient: () => undefined,','  ownSkillProfile: (profile: RuntimeSkillProfile) => { profiles.push(profile); },')
s=s.replace('MaterializedWorkspaceSkill | undefined','RuntimeSkillExposure | undefined').replace('materialized.name','materialized.skill.name').replace('materialized.sourceRootPath','materialized.sourceRoot').replace('materialized.materializedRootPath','materialized.linkRoot')
s=s.replace('    vi.restoreAllMocks();\n    for (const filePath', '    vi.restoreAllMocks();\n    for (const profile of profiles.splice(0)) await profile.release();\n    for (const filePath')
s=s.replace('    cleanupPaths.add(workspaceRoot);\n\n    const singleAgentId = `codex', '    cleanupPaths.add(workspaceRoot);\n    const memoryDir = await fs.mkdtemp(path.join(os.tmpdir(), "codex-private-execution-"));\n    cleanupPaths.add(memoryDir);\n\n    const singleAgentId = `codex',1)
s=s.replace('runId: `codex-single-run-${unique}`,','runId: `codex-single-run-${unique}`, memoryDir,').replace('runId: `codex-multi-run-${unique}`,','runId: `codex-multi-run-${unique}`, memoryDir,')
s=s.replace('runtimeContext.materializedConfiguredSkills','runtimeContext.privateSkillProfile!.exposures').replace('.map((skill) => [skill.name, skill])','.map((exposure) => [exposure.skill.name, exposure])').replace('.exposures.map((skill) => skill.name)','.exposures.map((exposure) => exposure.skill.name)')
s=s.replace('    await expect(fs.readdir(path.join(workspaceRoot, ".codex", "skills"))).resolves.toEqual(\n      expect.arrayContaining([singleSkillName, toneSkillName, outlineSkillName]),\n    );','    await expect(fs.readdir(workspaceRoot)).resolves.toEqual([]);')
p.write_text(s)
# Fake provider supports private metadata by inspecting the exact launch argument in test-owned storage.
p=S/'autobyteus-server-ts/tests/fixtures/grok-acp/fake-acp-agent.mjs';s=p.read_text().replace('import readline from "node:readline";','import readline from "node:readline";\nimport path from "node:path";')
s=s.replace('  received.push(JSON.parse(line));','''  const message = JSON.parse(line);
  const pluginIndex = process.argv.indexOf("--plugin-dir");
  if (message.method === "_x.ai/skills/list" && pluginIndex !== -1) {
    const skillsRoot = path.join(process.argv[pluginIndex + 1], "skills");
    const skills = fs.readdirSync(skillsRoot).map(name => ({ name, enabled:true,
      path:path.join(skillsRoot,name,"SKILL.md"), plugin_name:"autobyteus-configured" }));
    send({jsonrpc:"2.0",id:message.id,result:{result:{skills}}});
    return;
  }
  received.push(message);''');p.write_text(s)
p=S/'autobyteus-server-ts/docs/modules/shared_network_workspaces.md';p.write_text('''# Filesystem workspaces and external storage

AutoByteus uses ordinary directory paths and filesystem APIs. It does not detect
mounts, identify NFS or storage UUIDs, read host attachment descriptors, invoke a
storage CLI, or perform storage admission before activation or terminal creation.
Workspace registration remains metadata-only. Selecting a registered workspace
preserves its resolution errors rather than silently substituting a temporary
folder. The existing no-selection and unknown-ID fallback policy is unchanged.

Storage is an operator concern. [AutoByteus NFS](https://github.com/AutoByteus/autobyteus-nfs)
is one independent host service; see its
[filesystem usage guide](https://github.com/AutoByteus/autobyteus-nfs/blob/main/docs/filesystem-usage.md).
The Docker launcher can use any operator-supplied directory through
`AUTOBYTEUS_DOCKER_SHARED_WORKSPACE_DIR`: `<root>/shared` maps to the shared folder
and `<root>/nodes/<name>` to that node's workspace. The launcher retains private
settings, sign-ins and memory volumes but neither installs nor controls NFS.

## Configured skills and process ownership

Claude, Codex and Grok use exact execution-private skill profiles on every
filesystem. A profile is registered with its owner before awaited acquisition,
in valid application-private execution storage outside the project, including
symlink aliases. No configured bindings means no profile acquisition. Missing
storage or unsupported native discovery refuses preparation; it does not fall
back to project links. Configured collisions fail; ALL_INSTALLED prefers the
user-owned project entry. Other adapters' genuine materializers remain.

Native discovery checks the logical name and actual source manifest. A proven
native process/client close precedes exact profile release. Cleanup removes only
that profile's wrappers/links, never source bytes or a peer profile. Managed
catalog lookup selects the current matching source; it does not retain an old
generation. Source Update/Remove remains independent, so linked bytes can
disappear. AGY retains its separate private capsule and missing-source policy.

AutoByteus does not inject `safe.directory` into Git environments. Explicit
operator Git configuration and provider authentication remain independent.
Normal explorer, PTY, tools and REST contracts are unchanged. Filesystem outages
can stall ordinary operations; bounded outage isolation is not implemented.

## Evidence and distribution boundary

There is no paired NFS fixture or application/service protocol pin. Tests use
ordinary owned directories and independent repository inputs. Future combined
storage evidence must identify service/engine and application revisions, not
claim that a service source hash attests arbitrary app code. The disabled Guide
is informational: no qualified release or command is implied by extraction,
component checks, historical filesystem evidence or an architecture review.
''')
