from pathlib import Path
import json,subprocess,hashlib,difflib,collections
E=Path(__file__).resolve().parent;N=E.parents[4]
S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs');base='3712cd9bf0db998501d162db7f8655f169e3def6'
def git(r,*args):return subprocess.check_output(['git','-C',str(r),*args])
def normalize(s):return s.replace('github.com/AutoByteus/autobyteus-workspace/autobyteus-nfs','github.com/AutoByteus/autobyteus-nfs')
d=json.loads((E/'source-audit.json').read_text())
if not (E/'attempt-1/source-audit.json').exists():(E/'attempt-1/source-audit.json').write_bytes((E/'source-audit.json').read_bytes())
for row in d['goComparison']:
 p=N/row['path']; before=git(S,'show',base+':autobyteus-nfs/'+row['path']).decode()
 row['kind']='removed' if not p.exists() else 'normalized-equal' if normalize(before)==p.read_text() else 'changed'
oldpaths=set(git(S,'ls-tree','-r','--name-only',base).decode().splitlines())
for row in d['sourceSizes']:
 if row['repo']!='N':continue
 p=row['path'];old=p if p.startswith('scripts/') else 'autobyteus-nfs/'+p
 b=git(S,'show',base+':'+old).decode() if old in oldpaths else ''
 a=(N/p).read_text(); plus=minus=0
 for line in difflib.unified_diff(normalize(b).splitlines(),a.splitlines(),n=0):
  if line.startswith('+') and not line.startswith('+++') and line[1:].strip():plus+=1
  if line.startswith('-') and not line.startswith('---') and line[1:].strip():minus+=1
 row.update(addedNonblank=plus,removedNonblank=minus,deltaOver220=plus+minus>220)
d['normalization']='Only old Go module import prefix; no behavior/text normalization.'
scans=[]
for repo,pat,paths in [(S,'configuredSharedWorkspace|checkSharedWorkspaceForRun|admitSharedRunWorkspace|scopedProjectGitEnvironment|autobyteus-nfs|nfs-attachment|shared-workspace-binding|mount-observation|safe\\.directory|NFS_STORAGE_ID',['autobyteus-server-ts/src','scripts/public/docker','autobyteus-web']), (N,'PublicStore|launcher-attachment|attachNodes|reconnectNodes|detachNodes|autobyteus-workspace',['internal','cmd','go.mod','packaging','scripts/public',':(exclude)**/*_test.go'])]:
 argv=['git','-C',str(repo),'grep','-n','-i','-E',pat,'--',*paths]
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 scans.append({'argv':argv,'exit':p.returncode,'output':p.stdout})
d['activeCouplingScans']=scans
sizeKeys={(x['repo'],x['path']) for x in d['sourceSizes']}
d['unchangedBackendPlatformServiceProduction']=[x['path'] for x in d['goComparison'] if x['kind']=='normalized-equal' and x['path'].startswith(('internal/backend/','internal/platform/','internal/service/')) and not x['path'].endswith('_test.go')]
assert all(x['equal'] for x in d['licensesAndEngine'])
assert not any(x['over500Grown'] or x['deltaOver220'] for x in d['sourceSizes'])
assert all(x['exit']==1 and not x['output'] for x in scans)
(E/'source-audit.json').write_text(json.dumps(d,indent=2)+'\n')
print('go',collections.Counter(x['kind'] for x in d['goComparison']),'preserved production',len(d['unchangedBackendPlatformServiceProduction']),'sizes',len(d['sourceSizes']))
print('max source size',max(d['sourceSizes'],key=lambda x:x['afterNonblank']))
