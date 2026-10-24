"""One fresh manual same-byte resume after exact draft/payload re-observation."""
import base64,datetime,hashlib,json,pathlib,subprocess,sys,time
N=pathlib.Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-dashboard-release');E=N/'tickets/done/nfs-dashboard-release/delivery-evidence/dr-001';S=pathlib.Path('/Users/normy/nfs-dashboard-release-ytwviz3y')
repo='AutoByteus/autobyteus-nfs';P='448cef839b4919a1e3ae0489e8d86ae36f5cee33'
sys.path.insert(0,str(N/'packaging'));from release_support import publication,payload

def save(n,x):(E/('publication-resume-'+n)).write_text(json.dumps(x,indent=2)+'\n')
def api(path):return json.loads(subprocess.check_output(['gh','api',path],cwd=N,text=True))
for _ in range(120):
 if (E/'retained-final.json').exists():break
 time.sleep(5)
else:raise RuntimeError('Retained inspection unavailable; no dispatch')
proof=json.loads((E/'retained-final.json').read_text());assert proof['payloadSourceCommit']==P
binding=proof['tag']['binding'];tag=publication.tag_identity('v0.2.0');assert tag==proof['tag'] and tag['object']=='51e84a18e9283c9f6dda9be5d396dcb4b1b6f75f'
validated=payload.verify(S/'final-inspection/payload',S/'final-inspection/candidate');assert validated['runId']==40107739742
existing=publication.discover(S/'final-inspection/payload',binding,422823635);assert existing['draft'] is True
assets=publication.inventory(f'repos/{repo}/releases/422823635/assets');assert assets==[]
main=api(f'repos/{repo}/git/ref/heads/main');assert main['object']['sha']==P
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip()==P and not subprocess.check_output(['git','diff','--name-only'],cwd=N,text=True).strip()
w=api(f'repos/{repo}/contents/.github/workflows/release-nfs.yml?ref={P}');wb=base64.b64decode(w['content']);assert wb==(N/'.github/workflows/release-nfs.yml').read_bytes()
runs=api(f'repos/{repo}/actions/workflows/release-nfs.yml/runs?per_page=100')['workflow_runs'];assert all(r['status']=='completed' for r in runs)
save('preflight.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main':P,'tag':tag,'releaseId':existing['id'],'draft':True,'assets':0,'workflowSHA256':hashlib.sha256(wb).hexdigest(),'retainedPayloadVerified':True,'payloadJobId':proof['verifiedPayloadJobId'],'originalFailedRun':40107739742,'priorRunIds':[r['id'] for r in runs],'assessment':'Initial publisher observed no matching release in list immediately after successful draft POST. Actual current list/direct-ID/body and annotation correlate unique draft422823635. Cause of original visibility mismatch unproven. Guide authorizes one new same-byte manual resume, not failed-job rerun or recreate/rebuild/re-sign.','tokenLimit':'Local read-only observer differs from workflow token; hosted prepare/publisher must independently re-observe.'})
cmd=['gh','workflow','run','release-nfs.yml','--repo',repo,'--ref','main','-f','release_tag=v0.2.0','-f','source_sha='+P,'-f','candidate_run_id=40105960980','-f','publish=true']
p=subprocess.run(cmd,cwd=N,capture_output=True,text=True);save('dispatch.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
prior={r['id'] for r in runs}
for _ in range(30):
 found=[r for r in api(f'repos/{repo}/actions/workflows/release-nfs.yml/runs?per_page=100')['workflow_runs'] if r['id'] not in prior and r['head_sha']==P and r['event']=='workflow_dispatch']
 if found:break
 time.sleep(3)
assert len(found)==1
rid=found[0]['id'];print('RESUME',rid,flush=True);history=[]
for _ in range(120):
 r=api(f'repos/{repo}/actions/runs/{rid}');j=api(f'repos/{repo}/actions/runs/{rid}/attempts/1/jobs?per_page=100');save('run.json',r);save('jobs.json',j)
 row={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':rid,'status':r['status'],'conclusion':r['conclusion'],'jobs':[{'id':x['id'],'name':x['name'],'status':x['status'],'conclusion':x['conclusion'],'active':[s['name'] for s in x['steps'] if s['status']=='in_progress']} for x in j['jobs']]};history.append(row);save('monitor.json',history);print(json.dumps(row),flush=True)
 if r['status']=='completed':break
 time.sleep(20)
else:raise RuntimeError('Resume monitor bound; no automatic cancellation/replay')
p=subprocess.run(['gh','run','view',str(rid),'--repo',repo,'--attempt','1','--log'],cwd=N,capture_output=True);(E/'publication-resume.log').write_bytes(p.stdout);(E/'publication-resume-log-fetch.txt').write_bytes(p.stderr)
a=api(f'repos/{repo}/actions/runs/{rid}/artifacts?per_page=100');save('artifacts.json',a)
summary={'run':rid,'attempt':r['run_attempt'],'source':r['head_sha'],'conclusion':r['conclusion'],'url':r['html_url'],'jobs':row['jobs'],'logFetchExit':p.returncode,'logSHA256':hashlib.sha256(p.stdout).hexdigest(),'artifacts':[{'id':x['id'],'name':x['name'],'digest':x['digest'],'size':x['size_in_bytes'],'expires_at':x['expires_at']} for x in a['artifacts']]};save('summary.json',summary);print(json.dumps(summary),flush=True)
assert r['conclusion']=='success','No automatic additional attempt; diagnose and route if needed'
