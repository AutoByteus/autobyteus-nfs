from pathlib import Path
import subprocess,json,datetime,hashlib,base64,re
root=Path.cwd();t=root/'tickets/done/nfs-first-release';e=t/'delivery-evidence/dr-011';base='f830c50bf1238270343afce151dd05b65b10237a';intake='c8084c94278eab9f0babb025dfd36529ff0dfbe3';candidate='/Users/normy/nfs-first-candidate-api005-61mqnd8a/candidate';commands=[]
def write(name,data):(e/name).write_text(json.dumps(data,indent=2)+'\n')
def run(args):
 p=subprocess.run(args,capture_output=True,text=True);commands.append({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});write('finalization-commands.json',commands);assert p.returncode==0,(args,p.stderr);return p.stdout.strip()
assert json.loads((e/'readiness-data-tests.json').read_text())['passed']
assert run(['git','rev-parse','HEAD'])==intake
assert run(['git','branch','--show-current'])=='codex/nfs-first-release'
assert not run(['git','diff','--cached','--name-only'])
run(['git','fetch','--no-tags','origin','refs/heads/main:refs/remotes/origin/main']);assert run(['git','rev-parse','origin/main'])==base
for name in ['handoff-summary.md','release-deployment-report.md']:
 p=t/name;s=p.read_text();s=s.replace('Independent actual-readiness data validation in progress before finalization; it is not real Apple validation.','Independent actual-readiness data validation passed56collected/55executed/1expected Go-childskip, exit0; scratch removed. This is not real Apple validation.')
 p.write_text(s)
tracked=run(['git','diff','--name-only']).splitlines();allowed=['packaging/release-lock.json',*[f'packaging/releases/v0.1.0/{f}.json' for f in ['native-checks','release-controls','source-review','readiness']],*[f'tickets/done/nfs-first-release/{f}.md' for f in ['handoff-summary','docs-sync-report','delivery-revision-record','release-deployment-report']]];assert set(tracked)==set(allowed)
new=run(['git','ls-files','--others','--exclude-standard']).splitlines();assert all(p.startswith(('tickets/done/nfs-first-release/delivery-evidence/dr-010/','tickets/done/nfs-first-release/delivery-evidence/dr-011/')) for p in new)
paths=set(run(['git','ls-files']).splitlines()+new);fold={}
for p in paths:
 assert p.casefold() not in fold or fold[p.casefold()]==p;fold[p.casefold()]=p
 for part in Path(p).parts:assert not re.search(r'[<>:"\\|?*\x00-\x1f]',part) and not part.endswith((' ','.')) and not re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?',part),p
write('portable-paths.json',{'paths':len(paths),'errors':[]});new=run(['git','ls-files','--others','--exclude-standard']).splitlines()
run(['git','diff','--check','--',*allowed]);run(['git','add','--',*allowed,*[p for p in new if p!=str((e/'finalization-commands.json').relative_to(root))]])
# Command journal is kept unstaged until the operation's final result; do not dirty a tracked file while switching branches.
run(['git','commit','-m','docs(release): accept current API005 candidate readiness for signed v0.1.0'])
ticket=run(['git','rev-parse','HEAD']);run(['git','-c','push.followTags=false','push','--no-follow-tags','origin',ticket+':refs/heads/codex/nfs-first-release'])
run(['git','fetch','--no-tags','origin','refs/heads/main:refs/remotes/origin/main']);assert run(['git','rev-parse','origin/main'])==base
run(['git','switch','-c','codex/nfs-first-release-finalize-dr011','origin/main']);run(['git','merge','--no-ff','codex/nfs-first-release','-m','Merge reviewed NFS codesign diagnostics and current release readiness'])
merge=run(['git','rev-parse','HEAD']);assert run(['git','rev-parse',merge+'^{tree}'])==run(['git','rev-parse',ticket+'^{tree}'])
run(['python3','-B','packaging/release.py','--check-publish','--candidate',candidate]);digest=run(['python3','-B','packaging/release.py','--source-hash']);assert digest=='0a209d1efe327e13feeabe426c90e411728813a7261467c0428271eeee1db8e3'
assert run(['git','ls-remote','origin','refs/heads/main']).split()[0]==base
run(['git','-c','push.followTags=false','push','--no-follow-tags','origin',merge+':refs/heads/main'])
heads={l.split()[1]:l.split()[0] for l in run(['git','ls-remote','origin','refs/heads/main','refs/heads/codex/nfs-first-release']).splitlines()};assert heads=={'refs/heads/main':merge,'refs/heads/codex/nfs-first-release':ticket}
r=json.loads(run(['gh','api','repos/AutoByteus/autobyteus-nfs/contents/.github/workflows/release-nfs.yml?ref='+merge]));remote=base64.b64decode(r['content']);assert remote==(root/'.github/workflows/release-nfs.yml').read_bytes()
run(['git','switch','codex/nfs-first-release']);run(['git','merge','--ff-only',merge])
write('source-finalization.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ticketCommit':ticket,'freshTargetBefore':base,'mergeCommit':merge,'mergePolicy':'fresh finalize branch --no-ff; exact ticket tree equality','remoteHeads':heads,'sourceHash':digest,'postMergeReadinessAndSourceCheck':'Pass','remoteWorkflowBytesEqual':True,'workflowSha256':hashlib.sha256(remote).hexdigest(),'localTicketNowContainsFinalizedMain':True,'canonicalCheckoutUntouched':True,'sourceFinalization':'Completed','actualRelease':'Not yet dispatched'})
print(json.dumps({'ticketCommit':ticket,'main':merge,'sourceFinalization':'Completed','readiness':'Pass'},indent=2))
