from pathlib import Path
import subprocess,json,datetime,base64,hashlib
root=Path.cwd();t=root/'tickets/done/nfs-first-release';e=Path(__file__).resolve().parent;P='238bdc183e8affac99ffdee9be9cb333b0eb126f';commands=[]
def write(n,v):(e/n).write_text(json.dumps(v,indent=2)+'\n')
def run(args):
 p=subprocess.run(args,capture_output=True,text=True);commands.append({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});write('finalization-commands.json',commands);assert p.returncode==0,(args,p.stderr[-1000:]);return p.stdout.strip()
assert json.loads((e/'admission-d6587007cbc7e99f76075287ff7154faff239044.json').read_text())['passed']
assert run(['git','branch','--show-current'])=='codex/nfs-first-release';assert not run(['git','diff','--cached','--name-only'])
run(['git','fetch','--no-tags','origin','refs/heads/main:refs/remotes/origin/main']);assert run(['git','rev-parse','origin/main'])==P
for n in ['handoff-summary.md','release-deployment-report.md','delivery-revision-record.md']:
 p=t/n;p.write_text(p.read_text()+'\nDR014 actual committed-authority admission passed atd6587007cbc7e99f76075287ff7154faff239044: P/H/E scope/hash/evidence/current full original C/P and live successful signing jobs/known draft validated. No new executable drift; no full suite/native/signing repeat. Hosted recovery still pending.\n')
changed=run(['git','diff','--name-only']).splitlines();assert all(x.startswith(str(t.relative_to(root))+'/') for x in changed)
new=run(['git','ls-files','--others','--exclude-standard']).splitlines();assert all(x.startswith(str(e.relative_to(root))+'/') for x in new)
run(['git','diff','--check','--',*changed]);run(['git','add','--',*changed,*[x for x in new if not x.endswith('/finalization-commands.json')]])
run(['git','commit','-m','docs(release): verify genuine same-payload executor admission'])
ticket=run(['git','rev-parse','HEAD']);run(['git','-c','push.followTags=false','push','--no-follow-tags','origin',ticket+':refs/heads/codex/nfs-first-release'])
run(['git','fetch','--no-tags','origin','refs/heads/main:refs/remotes/origin/main']);assert run(['git','rev-parse','origin/main'])==P
run(['git','switch','-c','codex/nfs-first-release-finalize-dr014','origin/main']);run(['git','merge','--no-ff','codex/nfs-first-release','-m','Merge reviewed same-payload publication executor recovery'])
E=run(['git','rev-parse','HEAD']);assert run(['git','rev-parse','HEAD^{tree}'])==run(['git','rev-parse',ticket+'^{tree}'])
run(['python3','-B',str(e/'check-admission.py')]);assert run(['git','ls-remote','origin','refs/heads/main']).split()[0]==P
run(['git','-c','push.followTags=false','push','--no-follow-tags','origin',E+':refs/heads/main'])
heads={l.split()[1]:l.split()[0] for l in run(['git','ls-remote','origin','refs/heads/main','refs/heads/codex/nfs-first-release','refs/tags/v0.1.0']).splitlines()};assert heads['refs/heads/main']==E and heads['refs/heads/codex/nfs-first-release']==ticket and heads['refs/tags/v0.1.0']=='f4a04fd0c80a6625708ba002b4cef5507a03f514'
w=json.loads(run(['gh','api','repos/AutoByteus/autobyteus-nfs/contents/.github/workflows/release-nfs.yml?ref='+E]));b=base64.b64decode(w['content']);assert b==(root/'.github/workflows/release-nfs.yml').read_bytes()
run(['git','switch','codex/nfs-first-release']);run(['git','merge','--ff-only',E])
write('source-finalization.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ticketCommit':ticket,'freshTargetBefore':P,'executorCommit':E,'payloadSource':P,'reviewedCommit':'6cb497f4a0bb83d52ddfc41b5aaad95a8e482440','policy':'fresh finalize --no-ff, exact tree equality and actual committed admission check','remoteHeads':heads,'workflowSha256':hashlib.sha256(b).hexdigest(),'remoteWorkflowBytesEqual':True,'sourceFinalization':'Completed','release':'Not yet dispatched','canonicalCheckoutUntouched':True})
print(json.dumps({'ticket':ticket,'E':E,'P':P,'sourceFinalization':'Completed'},indent=2))
