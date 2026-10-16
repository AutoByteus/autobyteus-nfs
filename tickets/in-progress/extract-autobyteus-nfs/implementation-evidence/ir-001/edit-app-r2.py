from pathlib import Path
import re
R=Path('autobyteus-server-ts/src')
def edit(rel,fn):
 p=R/rel;p.write_text(fn(p.read_text()))
def remove_imports(s,needles):
 return re.sub(r'^import\b[\s\S]*?;\n',lambda m:'' if any(n in m[0] for n in needles) else m[0],s,flags=re.M)
# infrastructure-specific imports/callers
for p in R.rglob('*.ts'):
 s=p.read_text()
 if any(k in s for k in ['scoped-project-git-environment.js','shared-workspace-binding.js','native-shared-workspace.js','shared-run-workspace-admission.js']):
  s=remove_imports(s,['scoped-project-git-environment.js','shared-workspace-binding.js','native-shared-workspace.js','shared-run-workspace-admission.js']);p.write_text(s)
edit('agent-execution/services/agent-run-manager.ts',lambda s:re.sub(r'preparation: \{\n\s*prepare: async \(\) => \{ await admitSharedRunWorkspace[\s\S]*?\n\s*\},','preparation,',s,count=1))
edit('services/terminal-streaming/pty-session-manager.ts',lambda s:s.replace('      const shared = await checkSharedWorkspaceForRun(cwd);\n','').replace('session.start(cwd, shared ? scopedProjectGitEnvironment(process.env, cwd) : undefined)','session.start(cwd)'))
for provider in ['claude','codex']:
 edit(f'agent-execution/backends/{provider}/{provider}-workspace-resolver.ts',lambda s:s.replace('registeredRoot && await configuredSharedWorkspace(registeredRoot)','registeredRoot'))
edit('agent-execution/backends/autobyteus/autobyteus-agent-run-backend-factory.ts',lambda s:s.replace('    if (workspaceId && !workspaceInstance) workspaceInstance = await resolveNativeSharedWorkspace(this.workspaceManager, workspaceId);','    if (workspaceId && !workspaceInstance && await this.workspaceManager.getRegisteredWorkspaceRootPath(workspaceId)) {\n      workspaceInstance = await this.workspaceManager.getOrCreateWorkspace(workspaceId);\n    }').replace('      ...await nativeSharedTerminalData(workspaceRootPath),\n',''))
edit('agent-execution/backends/antigravity/backend/agy-agent-run-backend-factory.ts',lambda s:re.sub(r'    const env = await configuredSharedWorkspace[^;]+;\n','',s).replace('conversationId: expectedId, env','conversationId: expectedId'))
edit('agent-execution/backends/acp/backend/acp-agent-run-backend-factory.ts',lambda s:s.replace('const { materializedSkills } = privateSkillProfile ?', 'const { materializedSkills } = this.deps.privateSkills ?').replace('env: prepared.privateSkillProfile ? scopedProjectGitEnvironment(env, prepared.workingDirectory) : env,','env,'))
edit('agent-execution/backends/claude/session/claude-session-query-options.ts',lambda s:s.replace('      env: scopedProjectGitEnvironment(process.env, sessionConfig.workingDirectory),\n','').replace('runContext.runtimeContext.materializedConfiguredSkills.length > 0 || ',''))
edit('runtime-management/codex/client/codex-app-server-client-manager.ts',lambda s:s.replace('((cwd, profile) => new CodexAppServerClient({','((cwd) => new CodexAppServerClient({').replace('      env: profile ? scopedProjectGitEnvironment(process.env, cwd) : undefined,\n',''))
def helper(s):
 s=s.replace('/** Runtime preparation follows the common activation\'s binding admission. */','/** Configured exposure is application-private on every workspace. */')
 a=s.index('  const binding =');b=s.index('  if (!input.guard.ownSkillProfile)',a)
 return s[:a]+'''  input.guard.assertAccepting();
  if (!input.bindings.length) return null;
  if (!input.memoryDir || !path.isAbsolute(input.memoryDir)) {
    throw new Error("Runtime skills require absolute application-private execution storage.");
  }
'''+s[b:]
edit('agent-execution/backends/shared/prepare-private-runtime-skills.ts',helper)
# Validation lives inside owned profile preparation, before any filesystem acquisition.
edit('agent-execution/backends/shared/runtime-skill-profile.ts',lambda s:s.replace('    await fs.mkdir(this.input.privateParent,', '''    const executionRoot = await fs.realpath(path.dirname(this.input.privateParent));
    const projectRoot = await fs.realpath(this.workingDirectory);
    if (!(await fs.stat(executionRoot)).isDirectory()) throw new Error("Private execution storage must be a directory.");
    let privateRoot: string;
    try { privateRoot = await fs.realpath(this.input.privateParent); }
    catch (error) {
      if (!missing(error)) throw error;
      privateRoot = path.join(executionRoot, path.basename(this.input.privateParent));
    }
    const relative = path.relative(projectRoot, privateRoot);
    if (relative === "" || (!path.isAbsolute(relative) && relative !== ".." && !relative.startsWith(`..${path.sep}`))) {
      throw new Error("Runtime skill storage must be outside the project, including aliases.");
    }
    this.assertAccepting();
    await fs.mkdir(this.input.privateParent,''',1))
# Claude one private path, no generated workspace-link acquisition/cleanup.
def claude(s):
 s=remove_imports(s,['claude-workspace-skill-materializer.js','workspace-skill-materializer.js'])
 s='\n'.join(x for x in s.split('\n') if 'workspaceSkillMaterializer' not in x)
 a=s.index('  releaseSkills(');b=s.index('  async bootstrapForCreate',a);s=s[:a]+s[b:]
 a=s.index('    const preparedSkills =');b=s.index('    const carpenterSystemPrompt',a)
 s=s[:a]+'''    guard.assertAccepting();
    const configuredSkills = privateSkillProfile?.exposures.map(entry => entry.skill) ?? [];
'''+s[b:];return s.replace('        materializedConfiguredSkills,\n','')
edit('agent-execution/backends/claude/backend/claude-session-bootstrapper.ts',claude)
def codex(s):
 s=remove_imports(s,['node:fs','node:path','codex-workspace-skill-materializer.js','workspace-skill-materializer.js','configured-agent-skill-binding.js','codex-app-server-client-manager.js'])
 s=s.replace('  type WorkspaceCollisionPolicy,\n','')
 a=s.index('type DiscoverableSkillLookupClient');b=s.index('export const resolveApprovalPolicy',a);s=s[:a]+s[b:]
 s='\n'.join(x for x in s.split('\n') if not any(n in x for n in ['workspaceSkillMaterializer','clientManager']))
 a=s.index('    const materializedConfiguredSkills =');b=s.index('    return new AgentRunContext',a);s=s[:a]+s[b:]
 s=s.replace('        materializedConfiguredSkills,\n','');s=s[:s.index('  private async prepareWorkspaceSkills')]+'}\n';return s
edit('agent-execution/backends/codex/backend/codex-thread-bootstrapper.ts',codex)
for provider in ['claude','codex']:
 rel=f'agent-execution/backends/{provider}/backend/{provider}-agent-run-context.ts'
 def context(s):
  s=remove_imports(s,['workspace-skill-materializer.js','codex-thread-cleanup.js']);s='\n'.join(x for x in s.split('\n') if 'materializedConfiguredSkills' not in x)
  if '  toCleanupTarget()' in s:
   a=s.index('  toCleanupTarget()');b=s.index('\n  }',a)+4;s=s[:a]+s[b:]
  return s
 edit(rel,context)
 rel=f'agent-execution/backends/{provider}/backend/{provider}-agent-run-backend-factory.ts'
 def factory(s):
  s=remove_imports(s,['workspace-skill-materializer.js','codex-app-server-client-manager.js','codex-thread-cleanup.js'])
  s='\n'.join(x for x in s.split('\n') if not any(n in x for n in ['const skills:','const clients:','readonly threadCleanup:','threadCleanup: CodexThreadCleanup','this.threadCleanup =','this.sessionBootstrapper.releaseSkills','this.threadCleanup.cleanupPreparedWorkspaceSkills']))
  a=s.index('        const guard =');b=s.index(';\n',a)+1
  # first ; may inside push(profile); use end of full declaration based next statement
  b=s.index('        let platformAgentRunId',a) if provider=='claude' else s.index('        runContext =',a)
  s=s[:a]+'        const guard = { assertAccepting, ownSkillProfile: (profile: RuntimeSkillProfile) => { profiles.push(profile); } };\n'+s[b:]
  if '        for (const lease' in s:
   a=s.index('        for (const lease');b=s.index('        if (!errors.length)',a);s=s[:a]+s[b:]
  return s
 edit(rel,factory)
edit('agent-execution/backends/provider-preparation-guard.ts',lambda s:remove_imports('\n'.join(x for x in s.split('\n') if not any(n in x for n in ['  ownSkill(', '  ownCodexClient?'])),['workspace-skill-materializer.js','codex-app-server-client-manager.js']))
def session_manager(s):
 s=remove_imports(s,['claude-workspace-skill-materializer.js','workspace-skill-materializer.js']);s=s.replace('    workspaceSkillMaterializer: WorkspaceSkillMaterializer =\n      getClaudeWorkspaceSkillMaterializer(),\n','').replace('new ClaudeSessionCleanup(workspaceSkillMaterializer)','new ClaudeSessionCleanup()');return s
edit('agent-execution/backends/claude/session/claude-session-manager.ts',session_manager)
def cleanup(s):
 s=remove_imports(s,['claude-workspace-skill-materializer.js','workspace-skill-materializer.js']);a=s.index('  constructor(');b=s.index('  /**',a);s=s[:a]+s[b:];s='\n'.join(x for x in s.split('\n') if '["skills",' not in x);s=s.replace('// Unlike ordinary workspace links, private profile exposure remains needed by','// Private profile exposure remains needed by');return s
edit('agent-execution/backends/claude/session/claude-session-cleanup.ts',cleanup)
def threadmanager(s):
 s=remove_imports(s,['codex-thread-cleanup.js']);s='\n'.join(x for x in s.split('\n') if not any(n in x for n in ['readonly threadCleanup:', 'threadCleanup: CodexThreadCleanup', 'this.threadCleanup =']))
 s=s.replace('      try { await this.threadCleanup.cleanupPreparedWorkspaceSkills(context.runtimeContext.materializedConfiguredSkills); }\n      catch (error) { errors.push(error); }\n','');return s
edit('agent-execution/backends/codex/thread/codex-thread-manager.ts',threadmanager)
for rel in ['agent-execution/services/shared-run-workspace-admission.ts','workspaces/shared-workspace-binding.ts','workspaces/shared-workspace-mount-observation.ts','agent-execution/backends/autobyteus/native-shared-workspace.ts','runtime-management/shared/scoped-project-git-environment.ts','agent-execution/backends/claude/claude-workspace-skill-materializer.ts','agent-execution/backends/codex/codex-workspace-skill-materializer.ts','agent-execution/backends/codex/backend/codex-thread-cleanup.ts']:(R/rel).unlink()
