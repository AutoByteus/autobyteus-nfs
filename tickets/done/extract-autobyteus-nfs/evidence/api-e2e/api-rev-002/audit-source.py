from common import *
import hashlib
audit=json.loads((E/'input-audit.json').read_text())
B='3712cd9bf0db998501d162db7f8655f169e3def6'
def old(path):return subprocess.check_output(['git','-C',str(S),'show',B+':'+path])
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def check(name,ok,details=None):
 checks.append(dict(name=name,pass_=bool(ok),details=details))
 assert ok,name
for a,b in [('autobyteus-nfs/LICENSE','LICENSE'),('CLA.md','CLA.md'),('autobyteus-nfs/THIRD_PARTY_NOTICES','THIRD_PARTY_NOTICES'),('autobyteus-nfs/packaging/release-lock.json','packaging/release-lock.json')]:
 check('exact '+b,old(a)==(N/b).read_bytes(),sha((N/b).read_bytes()))
pins=[]
for p in subprocess.check_output(['git','-C',str(S),'ls-tree','-r','--name-only',B,'autobyteus-nfs/packaging/engine'],text=True).splitlines():
 if p.endswith('README.md'):continue
 q=p[len('autobyteus-nfs/'):]
 check('engine '+q,old(p)==(N/q).read_bytes())
for p,h in audit['N']['paths']:
 if p.startswith(('internal/backend/','internal/platform/','internal/service/')) and p.endswith('.go') and not p.endswith('_test.go'):
  check('preserved host '+p,old('autobyteus-nfs/'+p).replace(b'github.com/AutoByteus/autobyteus-workspace/autobyteus-nfs',b'github.com/AutoByteus/autobyteus-nfs')==(N/p).read_bytes())
removed=['autobyteus-nfs','.github/workflows/release-nfs.yml','scripts/public/nfs','autobyteus-server-ts/src/workspaces/shared-workspace-binding.ts','autobyteus-server-ts/src/workspaces/shared-workspace-mount-observation.ts','autobyteus-server-ts/src/agent-execution/services/shared-run-workspace-admission.ts','scripts/public/docker/autobyteus-docker.d/bash/nfs-attachment.sh']
check('retired S paths absent',all(not (S/p).exists() for p in removed),removed)
for label,prefixes,tokens in [('S',('autobyteus-server-ts/src/','scripts/public/docker/'),['scopedProjectGitEnvironment','shared-workspace-binding','launcher-attachment','/etc/autobyteus-nfs','safe.directory']),('N',('internal/','cmd/'),['/app/autobyteus','launcher-attachment','NodeAttachment','PublicDirectory','/etc/autobyteus-nfs'])]:
 root=N if label=='N' else S
 hits=[dict(path=p,token=t) for p,h in audit[label]['paths'] if p.startswith(prefixes) and not p.endswith('_test.go') for t in tokens if t.encode() in (root/p).read_bytes()]
 check('removed coupling '+label,not hits,hits)
check('independent Go', 'replace ' not in (N/'go.mod').read_text())
check('independent source hash',all(s not in (N/'packaging/release.py').read_text() for s in ['autobyteus-server-ts','autobyteus-web']))
lock=json.loads((N/'packaging/release-lock.json').read_text())
check('qualification empty',lock['qualifiedTargets']==[] and lock['qualifiedSourceHash']=='' and lock['physicalEvidence']==[] and lock['userVerified']==False and lock['engine'] is None)
# Current Guide equals exact implementation render source, not an installed app.
paths=['autobyteus-web/components/settings/NfsGuideCard.vue','autobyteus-web/localization/messages/en/settings.ts','autobyteus-web/localization/messages/zh-CN/settings.ts','autobyteus-web/utils/nfsLauncherCommands.ts']
for p in paths:
 prior=subprocess.check_output(['git','-C',str(S),'show','d3f7f67015587b4c8aa26824786be807793485d1:'+p])
 check('Guide render input '+p,prior==(S/p).read_bytes(),sha(prior))
write('source-contract-audit.json',dict(baseline=B,checks=checks,pass_=True,guide_render_carried=str(T/'implementation-evidence/ir-001/guide-render/result.json')))
# Protect only explicitly task-relevant artifacts; do not inspect credentials.
D0=Path('/Users/normy/autobyteus_org/autobyteus-nfs')
retained=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/shared-network-workspaces/autobyteus-nfs/out/ir005-local-candidate/engine-candidate')
protected=[]
for r in [D0/'task-plans',retained]:
 if r.exists():
  protected.extend(dict(path=str(f),sha256=sha(f.read_bytes())) for f in r.rglob('*') if f.is_file())
write('protected-inputs.json',dict(files=protected,D0_head=subprocess.run(['git','-C',str(D0),'rev-parse','--verify','HEAD'],capture_output=True,text=True).returncode,D0_branch=subprocess.check_output(['git','-C',str(D0),'symbolic-ref','HEAD'],text=True).strip()))
event('E01','Completed',str(len(checks))+' source/license/pin/removal contracts checked; independent archives exact','Pass','source-contract-audit.json; archive-integrity.json')
