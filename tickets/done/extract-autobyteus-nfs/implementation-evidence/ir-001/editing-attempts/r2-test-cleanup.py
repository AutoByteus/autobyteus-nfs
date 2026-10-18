from pathlib import Path
import re
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs/autobyteus-server-ts')
# Old live suite tests the removed discovery/materialization branch. Private discovery is covered at the actual adapter boundary, with separate gated downstream qualification.
(S/'tests/integration/agent-execution/codex-thread-bootstrapper.integration.test.ts').unlink()
for p in (S/'tests').rglob('*.ts'):
 s=p.read_text()
 if p.name in ['github-skill-runtime-harness.ts','agent-package-private-skills.e2e.test.ts']:continue
 s=re.sub(r'^import[^\n]*(?:CodexThreadCleanup|getClaudeWorkspaceSkillMaterializer)[^\n]*\n','',s,flags=re.M)
 s=re.sub(r'^\s*const workspaceSkillMaterializer = getClaudeWorkspaceSkillMaterializer\(\);\n','\n',s,flags=re.M)
 s=re.sub(r'^    const (?:threadCleanup|cleanup) = \{\s*cleanupPreparedWorkspaceSkills: vi.fn\(async \(\) => undefined\),?\s*\} as unknown as CodexThreadCleanup;\n','',s,flags=re.M)
 if p.name in ['agent-provider-factory-builder.test.ts','claude-agent-run-backend-factory.integration.test.ts','codex-agent-run-backend-factory.integration.test.ts']:
  s=re.sub(r'^\s*(?:workspaceSkillMaterializer|threadCleanup):[^\n]*\n','\n',s,flags=re.M) if p.name!='codex-agent-run-backend-factory.integration.test.ts' else s
  s=s.replace('      workspaceSkillMaterializer,\n','')
  if p.name=='codex-agent-run-backend-factory.integration.test.ts':
   s=s.replace('      workspaceSkillMaterializer: {\n        materializeConfiguredWorkspaceSkills: async () => ({ materializedSkills: [], effectiveRequests: [] }),\n        cleanupMaterializedWorkspaceSkills: async () => undefined,\n      } as never,\n','').replace('      threadCleanup: new CodexThreadCleanup(undefined, input.clientManager),\n','').replace('      workspaceSkillMaterializer: inert,\n','')
 if s!=p.read_text():p.write_text(s)
p=S/'tests/unit/agent-execution/backends/shared/private-skill-bootstrappers.test.ts';s=p.read_text().replace(",managedSource:{sourceId:'source-id'} as never",'');s=s.replace("    const f=fixture(runtime,[{kind:'resolved',skill:initial}]);","    initial.managedSource={sourceId:'source-id',generation:'old'};\n    const f=fixture(runtime,[{kind:'resolved',skill:initial}]);");p.write_text(s)
# Existing API fixture adaptation, not a new API suite.
p=S/'tests/e2e/skills/github-skill-runtime-harness.ts';s=p.read_text();s='\n'.join(l for l in s.split('\n') if 'import { getCodexWorkspaceSkillMaterializer' not in l and 'import { getClaudeWorkspaceSkillMaterializer' not in l)
s=s.replace('// Actual adapter preparation and profile-owned materializers;', '// Actual adapter preparation and execution-private profiles;')
s=s.replace('  const definition =', '  const memoryDir = path.join(root, "runtime-private"); fs.mkdirSync(memoryDir);\n  const definition =',1).replace('autoExecuteTools: false });','autoExecuteTools: false, memoryDir });')
s=s.replace('  let discoverCurrent = false;\n','').replace('    workspace, link: path.join(workspace, "." + adapter, "skills", "api-writer"),\n    setDiscoverCurrent: () => { discoverCurrent = true; },','    workspace,')
s=s.replace('        const backend =', '        const parent = path.join(memoryDir, "runtime-skill-profiles");\n        const before = new Set(fs.existsSync(parent) ? fs.readdirSync(parent) : []);\n        const backend =',1)
s=s.replace('        return { cleanup, root: fs.realpathSync(path.join(workspace, ".grok", "skills", "api-writer")) };','        const acquired = fs.readdirSync(parent).filter(name => !before.has(name));\n        if (acquired.length !== 1) throw new Error("Expected one exact new private profile");\n        const link = path.join(parent, acquired[0]!, "skills", "api-writer");\n        return { cleanup, link, root: fs.realpathSync(link) };')
a=s.index('      // No preparation is cancelled');b=s.index('\n    },\n    async close',a)
s=s[:a]+'''      const guard = { assertAccepting: () => undefined, ownSkillProfile: (profile: {release():Promise<void>}) => cleanups.push(() => profile.release()) };
      const result = await boot!.bootstrapForCreate(new AgentRunContext({ runId: id, config: config(), runtimeContext: null }), guard);
      const profile = result.runtimeContext.privateSkillProfile!;
      return { cleanup: () => profile.release(), link: profile.exposures[0]!.linkRoot, root: profile.exposures[0]!.sourceRoot };'''+s[b:];p.write_text(s)
p=S/'tests/e2e/skills/github-skill-sources-graphql.e2e.test.ts';s=p.read_text().replace('path.join(runtime.link, "SKILL.md")','path.join(first.link, "SKILL.md")',1);s=s.replace('path.join(runtime.link, "SKILL.md")','path.join(second.link, "SKILL.md")').replace('        // Codex\'s native-discovery branch must still reconcile an existing owned old link.\n        if (adapter === "codex" && retain) runtime.setDiscoverCurrent();\n','').replace('expect(fs.lstatSync(runtime.link).isSymbolicLink()).toBe(true);','expect(fs.existsSync(order[0]!.link)).toBe(false);\n        expect(fs.lstatSync(order[1]!.link).isSymbolicLink()).toBe(true);').replace('expect(fs.existsSync(runtime.link)).toBe(false);','expect(fs.existsSync(order[1]!.link)).toBe(false);\n        expect(fs.readdirSync(runtime.workspace)).toEqual([]);');p.write_text(s)
