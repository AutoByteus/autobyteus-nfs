from pathlib import Path
import subprocess,json,hashlib,re
E=Path(__file__).resolve().parent;N=E.parents[4];S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs')
before='a2023feff3d498fb6c51cebf1c93360da3679a45';base='3712cd9bf0db998501d162db7f8655f169e3def6'
def git(r,*args):return subprocess.check_output(['git','-C',str(r),*args],text=True).strip()
# All N source incl policies is identical to the successfully validated candidate.
assert not git(N,'diff','--name-only','83726b27400b405a7a6a79bd962d8e2419daa561','HEAD','--','.',':!tickets')
production=git(S,'ls-files','autobyteus-server-ts/src','scripts/public/docker').splitlines()
forbidden=['scopedProjectGitEnvironment','shared-workspace-binding','shared-workspace-mount-observation','launcher-attachment','/etc/autobyteus-nfs','safe.directory']
hits=[{'path':p,'token':t} for p in production if (S/p).is_file() for t in forbidden if t in (S/p).read_text(errors='replace')]
assert not hits,hits
removed=['autobyteus-nfs','.github/workflows/release-nfs.yml','scripts/public/nfs','autobyteus-server-ts/src/workspaces/shared-workspace-binding.ts','autobyteus-server-ts/src/workspaces/shared-workspace-mount-observation.ts','autobyteus-server-ts/src/agent-execution/services/shared-run-workspace-admission.ts','scripts/public/docker/autobyteus-docker.d/bash/nfs-attachment.sh','autobyteus-server-ts/tests/fixtures/shared-network-workspaces/attachment.json','autobyteus-server-ts/tests/fixtures/shared-network-workspaces/provenance.json']
assert all(not (S/p).exists() for p in removed)
r2owners=[p for p in git(S,'diff','--name-only',base,before,'--','autobyteus-server-ts/src').splitlines() if (S/p).is_file()]
ownerchanges=[p for p in r2owners if git(S,'diff',before,'HEAD','--',p)]
assert ownerchanges==['autobyteus-server-ts/src/agent-execution/services/agent-run-manager.ts'],ownerchanges
manager=(S/ownerchanges[0]).read_text()
for token in ['inputPreface: this.inputPreface','onPublished: run => this.notifyPublished(run, request.kind)','factory.beginPreparation(','releaseExactRun','releaseRetiredRun']:
 assert token in manager,token
codex=(S/'autobyteus-server-ts/tests/unit/agent-execution/backends/codex/backend/codex-thread-bootstrapper.test.ts').read_text()
assert 'WORK_REQUEST_EXECUTION_LLM_INSTRUCTION' not in codex and 'testCodexLeaseManager' not in codex
assert 'On receiving a request, follow your own instructions and skills.' in codex
assert "Don't send acknowledgements, status chatter or promises to work." in codex
assert 'testCodexLeaseManager' in (S/'autobyteus-server-ts/tests/unit/agent-execution/backends/codex/thread/codex-thread-manager.test.ts').read_text()
sizes=[]
for p in ownerchanges:
 old=git(S,'show',before+':'+p);now=(S/p).read_text()
 count=lambda t:len([l for l in t.splitlines() if l.strip()])
 sizes.append(dict(path=p,before=count(old),after=count(now)))
 assert count(now)<=500 or count(now)<=count(old)
guide=['autobyteus-web/components/settings/NfsGuideCard.vue','autobyteus-web/utils/nfsLauncherCommands.ts']
for p in guide:assert not git(S,'diff',before,'HEAD','--',p)
out=dict(N_service_unchanged=True,S_head=git(S,'rev-parse','HEAD'),base_merged=git(S,'rev-parse','origin/personal'),removed_owners=removed,forbidden_hits=hits,R2_production_owners_count=len(r2owners),R2_production_owners_changed_since_API001=ownerchanges,source_sizes=sizes,unchanged_guide_paths=guide,conflict_resolution='Neither stale import is used; current prompt assertions and R2 dependency/guard shapes retained.',no_new_production_logic_beyond_upstream=True)
(E/'integration-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
