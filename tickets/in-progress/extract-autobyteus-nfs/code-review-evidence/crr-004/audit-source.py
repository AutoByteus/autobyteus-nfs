from pathlib import Path
import hashlib,json,subprocess
E=Path(__file__).parent;T=E.parent.parent;N=T.parent.parent.parent;S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs');sha=lambda b:hashlib.sha256(b).hexdigest()
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args])
def paths(repo,rev):return git(repo,'ls-tree','-r','--name-only','-z',rev).decode().split('\0')[:-1]
def agg(h):return sha(''.join(p+'\0'+h[p]+'\n' for p in sorted(h)).encode())
old='a2023feff3d498fb6c51cebf1c93360da3679a45';base='2f211340ee36b81cef74a74b2e042b5102c269d3';initial='3712cd9bf0db998501d162db7f8655f169e3def6';merge='156ea2dacc0fb4989a6b5d8a7206fa143fde0c54';head=git(S,'rev-parse','HEAD').decode().strip()
assert head=='5559abbf017566f0030d95b023614f7418d3f212' and not git(S,'status','--porcelain')
assert git(S,'show','-s','--format=%P',merge).decode().split()==[old,base]
oldfiles=set(git(S,'diff','--name-only',initial,old).decode().splitlines());newbase=set(git(S,'diff','--name-only',initial,base).decode().splitlines());overlap=sorted(oldfiles&newbase);assert len(overlap)==5
prior=json.loads((T/'code-review-evidence/crr-002/input-audit.json').read_text())
result={'review':'CRR-004','N_head':git(N,'rev-parse','HEAD').decode().strip(),'S_head':head,'integrated_base':base,'merge':merge,'overlap':overlap,'input_identity':{}}
for key,repo in [('N',N),('S',S)]:
 names=[p for p in paths(repo,'HEAD') if not p.startswith('tickets/')];h={p:sha((repo/p).read_bytes()) for p in names}
 result['input_identity'][key]={'paths':len(names),'sha256':agg(h)}
 if key=='N':assert agg(h)==prior['repositories']['N']['current_aggregate_sha256']
result['N_source_unchanged']=True
prod=json.loads((E/'unused-locals.json').read_text())['production'];changed=[p for p in prod if (S/p).read_bytes()!=git(S,'show',old+':'+p)];assert changed==['autobyteus-server-ts/src/agent-execution/services/agent-run-manager.ts']
result['R2_production_files']=len(prod);result['changed_R2_production']=changed
manager=changed[0];current=(S/manager).read_text();upstream=git(S,'show',base+':'+manager).decode()
upstream=upstream.replace('import { admitSharedRunWorkspace } from "./shared-run-workspace-admission.js";\n','').replace('''preparation: {
          prepare: async () => { await admitSharedRunWorkspace(config.workspaceId); return preparation.prepare(); },
          cancel: () => preparation.cancel(),
          release: () => preparation.release(),
        },''','preparation,')
assert upstream==current
result['manager_equals_upstream_except_approved_admission_removal']=True
result['manager_nonempty']={'previous':sum(bool(x.strip()) for x in git(S,'show',old+':'+manager).decode().splitlines()),'current':sum(bool(x.strip()) for x in current.splitlines())}
result['post_merge_changed_paths']=git(S,'diff','--name-only',merge,'HEAD').decode().splitlines();assert len(result['post_merge_changed_paths'])==2
(E/'manager.diff').write_bytes(git(S,'diff',old,'HEAD','--',manager))
removed=json.loads((T/'implementation-evidence/ir-003/integration-audit.json').read_text())['removed_owners'];assert all(not (S/p).exists() for p in removed);result['retired_owner_paths_absent']=removed
for name,h in prior['authority_files_unchanged'].items():assert sha((T/name).read_bytes())==h
result['unchanged_authority_files']=8
finding=json.loads((E/'unused-locals.json').read_text())['diagnostics'];assert len(finding)==1
p=finding[0]['path'];before=git(S,'show',old+':'+p).decode();assert 'import { Skill }' in before and before.count('new Skill(')==0
result['finding_provenance']='Skill import already unused at a2023fef; original R2 deleted old materializer cases, and IR003 touches this file again. Prior production-only unused audit did not cover test imports.'
result['finding']=finding[0]
protected=[p for p in paths(N,'HEAD') if p.startswith(str(T.relative_to(N))+'/') and Path(p).name not in ['code-review-report.md','code-review-revision-record.md']]
result['protected_ticket_inputs']={'count':len(protected),'sha256':agg({p:sha((N/p).read_bytes()) for p in protected})}
result['prior_history_sha256']=sha((T/'code-review-revision-record.md').read_bytes())
result['IR003_scratch_absent']=not Path(json.loads((T/'implementation-evidence/ir-003/cleanup.json').read_text())['scratch']).exists();assert result['IR003_scratch_absent']
(E/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
