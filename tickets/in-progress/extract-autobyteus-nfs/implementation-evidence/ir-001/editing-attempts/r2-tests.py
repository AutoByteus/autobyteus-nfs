from pathlib import Path
N=Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/extract-autobyteus-nfs')
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs/autobyteus-server-ts')
p=N/'README.md';s=p.read_text().split('### Selected Docker clients after an ordinary host restart')[0];s=s.replace('mount/export/recreate real nodes','mount/export storage or alter real containers');p.write_text(s)
p=N/'packaging/RELEASE.md';p.write_text(p.read_text().replace('declared integration contract','declared filesystem usage boundary'))
# Remove superseded workspace-materialization tests by balanced it blocks using lines; new cross-bootstrapper tests replace them.
p=S/'tests/unit/agent-execution/backends/claude/backend/claude-session-bootstrapper.test.ts';s=p.read_text();s=s[:s.index('  it("maps resolved')]+'});\n';s=s.replace('  const workspaceSkillMaterializer = { materializeConfiguredWorkspaceSkills: vi.fn(async (input: { requests?: unknown[] }) => ({ materializedSkills: [], effectiveRequests: input.requests ?? [] })) };\n','').replace('return { bootstrapper, workspaceSkillMaterializer };','return { bootstrapper };').replace(', ownSkill: () => undefined, ownCodexClient: () => undefined','');p.write_text(s)
p=S/'tests/unit/agent-execution/backends/codex/backend/codex-thread-bootstrapper.test.ts';s=p.read_text()
# Capture whole old tests by top-level it start/end (each is directly inside describe).
starts=[];lines=s.splitlines(True);i=0;out=[]
markers=['reconciles an already','reconciles already','Codex already','catalog\'s copy','maps every binding','prefers user-owned','falls back to workspace materialization']
# exact start for discoverable case is discovered below; match its block content instead.
while i<len(lines):
 if lines[i].startswith('  it('):
  j=i+1
  while j<len(lines) and not lines[j].startswith('  });'): j+=1
  block=''.join(lines[i:j+1])
  if ('workspaceSkillMaterializer' in block and 'materializeConfiguredWorkspaceSkills' in block):
   i=j+1;continue
 out.append(lines[i]);i+=1
s=''.join(out)
a=s.index('const createMaterializerMock =');b=s.index('const createBootstrapper =',a);s=s[:a]+s[b:]
s=s.replace('  materializeImplementation?: WorkspaceSkillMaterializer["materializeConfiguredWorkspaceSkills"];\n','')
a=s.index('  const workspaceSkillMaterializer =');b=s.index('  const workspaceResolver =',a);s=s[:a]+s[b:]
a=s.index('  const client = {');b=s.index('  const agentToolMcpRunSessions =',a);s=s[:a]+s[b:]
s=s.replace('    workspaceSkillMaterializer,\n    client,\n    clientManager,\n','')
s=s.replace('      materializeImplementation: async () => {\n        throw new Error("workspace materialization failed after issue");\n      },\n','')
s=s.replace('"workspace materialization failed after issue"','"absolute application-private execution storage"')
s=s.replace(', ownSkill: () => undefined, ownCodexClient: () => undefined','')
s='\n'.join(l for l in s.split('\n') if 'import { testCodexLeaseManager }' not in l and 'import type { WorkspaceSkillMaterializer }' not in l and 'import type { CodexAppServerClientManager }' not in l)
p.write_text(s)
p=S/'tests/unit/agent-execution/backends/claude/session/claude-session-cleanup.test.ts';s=p.read_text().replace('listener/skill/MCP','listener/MCP').replace("    const owned = [{ ownerRunId: 'A', holderToken: 'same-owned-holder' }];\n",'').replace('materializedConfiguredSkills: owned, ','').replace('    const skills = { cleanupMaterializedWorkspaceSkills: vi.fn(async () => undefined) };\n','').replace('new ClaudeSessionCleanup(skills as never)','new ClaudeSessionCleanup()');s='\n'.join(l for l in s.split('\n') if 'expect(skills.' not in l);p.write_text(s)
p=S/'tests/unit/agent-execution/backends/claude/session/claude-input-terminal-release.test.ts';s=p.read_text().replace('  const skills = { cleanupMaterializedWorkspaceSkills: vi.fn(async () => undefined) };\n','')
s=s.replace('    const context = new AgentRunContext({ runId,','    const privateSkillProfile = { release: vi.fn(async () => undefined), exposures: [], root: "/test-private" };\n    const context = new AgentRunContext({ runId,')
s=s.replace('runtimeToolExposure: buildRuntimeAgentToolExposure([]) }),','runtimeToolExposure: buildRuntimeAgentToolExposure([]), privateSkillProfile: privateSkillProfile as never }),')
s=s.replace('return { run, backend, session };','return { run, backend, session, privateSkillProfile };').replace('manager, sdk, skills, mcp','manager, sdk, mcp')
s=s.replace('h.skills.cleanupMaterializedWorkspaceSkills','h.privateSkillProfile.release')
# First failed/held physical checks must retain private profile; successful retry releases once.
pos=s.index("it('retries only failed physical");a=s[:pos];b=s[pos:];b=b.replace('expect(h.privateSkillProfile.release).toHaveBeenCalledOnce();','expect(h.privateSkillProfile.release).not.toHaveBeenCalled();',1);s=a+b
pos=s.index("it('flushes pending approval");a=s[:pos];b=s[pos:];b=b.replace('expect(h.privateSkillProfile.release).toHaveBeenCalledOnce();','expect(h.privateSkillProfile.release).not.toHaveBeenCalled();',1);s=a+b
p.write_text(s)
p=S/'tests/unit/agent-execution/backends/codex/codex-input-terminal-release.test.ts';s=p.read_text();s='\n'.join(l for l in s.split('\n') if 'import type { CodexThreadCleanup }' not in l and 'const cleanup = { cleanupPreparedWorkspaceSkills' not in l);s=s.replace('manager, cleanup, close','manager, close')
s=s.replace('await vi.waitFor(() => expect(h.cleanup.cleanupPreparedWorkspaceSkills).toHaveBeenCalled());','await vi.waitFor(() => expect(h.manager.getThread(run.runId)).toBeNull());')
s=s.replace('// Existing independent skill cleanup can run even when turn proof fails;\n      // only exact thread/lease disposal is gated on the complete receipt.\n      expect(h.cleanup.cleanupPreparedWorkspaceSkills).toHaveBeenCalledTimes(1);','// Exact thread/lease disposal is gated on terminal proof.\n      expect(h.manager.getThread(run.runId)).toBe(h.thread);')
s=s.replace('expect(h.cleanup.cleanupPreparedWorkspaceSkills).toHaveBeenCalledTimes(2);','expect(h.manager.getThread(run.runId)).toBeNull();');p.write_text(s)
