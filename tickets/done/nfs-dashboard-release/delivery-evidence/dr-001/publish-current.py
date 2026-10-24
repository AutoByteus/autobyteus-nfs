import base64,datetime,hashlib,json,pathlib,subprocess,time
N=pathlib.Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-dashboard-release');E=N/'tickets/done/nfs-dashboard-release/delivery-evidence/dr-001'
repo='AutoByteus/autobyteus-nfs';P='448cef839b4919a1e3ae0489e8d86ae36f5cee33'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def gh(*a):return subprocess.check_output(['gh',*a],cwd=N,text=True)
def api(path):return json.loads(gh('api',path))
# No dispatch unless exact-current ordinary source checks completed successfully.
for i in range(90):
 if (E/'source-ci-summary.json').exists():break
 time.sleep(10)
else:raise RuntimeError('Source CI summary unavailable; no dispatch')
ci=json.loads((E/'source-ci-summary.json').read_text());print('SOURCE CI',json.dumps(ci),flush=True)
for run in [40107371147,40107380865]:
 d=api(f'repos/{repo}/actions/runs/{run}');assert d['conclusion']=='success' and d['status']=='completed'
assert gh('rev-parse','HEAD') if False else True
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=N,text=True).strip()==P
assert not subprocess.check_output(['git','diff','--name-only'],cwd=N,text=True).strip()
main=api(f'repos/{repo}/git/ref/heads/main');assert main['object']['sha']==P
rels=[]
for page in range(1,101):
 rows=api(f'repos/{repo}/releases?per_page=100&page={page}');rels+=rows
 if len(rows)<100:break
else:raise RuntimeError('Release inventory pagination bound')
assert not any(r['tag_name']=='v0.2.0' for r in rels)
tags=subprocess.check_output(['git','ls-remote','origin','refs/tags/v0.2.0','refs/tags/v0.2.0^{}'],cwd=N,text=True);assert not tags.strip()
runs=api(f'repos/{repo}/actions/workflows/release-nfs.yml/runs?per_page=100')['workflow_runs'];assert all(r['status']=='completed' for r in runs),'Another release workflow is active'
w=api(f'repos/{repo}/contents/.github/workflows/release-nfs.yml?ref={P}');wb=base64.b64decode(w['content']);assert wb==(N/'.github/workflows/release-nfs.yml').read_bytes()
assert hashlib.sha256(wb).hexdigest()=='c86062e3c07e931b4df290b5bb1372efbe2f95ae204190964bf171f5249695f9'
record={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main':P,'candidateRun':40105960980,'version':'v0.2.0','workflowSHA256':hashlib.sha256(wb).hexdigest(),'existingReleases':[{'id':r['id'],'tag':r['tag_name'],'draft':r['draft'],'prerelease':r['prerelease'],'assetCount':len(r['assets'])} for r in rels],'v020TagAbsent':True,'activeReleaseRuns':[],'priorRunIds':[r['id'] for r in runs]}
save('publication-preflight.json',record)
cmd=['gh','workflow','run','release-nfs.yml','--repo',repo,'--ref','main','-f','release_tag=v0.2.0','-f','source_sha='+P,'-f','candidate_run_id=40105960980','-f','publish=true']
p=subprocess.run(cmd,cwd=N,capture_output=True,text=True);save('publication-dispatch.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'main':P});assert p.returncode==0
prior=set(record['priorRunIds'])
for i in range(30):
 current=api(f'repos/{repo}/actions/workflows/release-nfs.yml/runs?per_page=100')['workflow_runs']
 found=[r for r in current if r['id'] not in prior and r['head_sha']==P and r['event']=='workflow_dispatch']
 if found:break
 time.sleep(3)
assert len(found)==1,'Dispatch identity must be unique, do not re-dispatch'
run=found[0];rid=run['id'];save('publication-run.json',run);print('PUBLICATION RUN',rid,run['html_url'],flush=True)
history=[]
for i in range(240):
 run=api(f'repos/{repo}/actions/runs/{rid}');jobs=api(f'repos/{repo}/actions/runs/{rid}/attempts/1/jobs?per_page=100')
 save('publication-run.json',run);save('publication-jobs.json',jobs)
 row={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':rid,'status':run['status'],'conclusion':run['conclusion'],'jobs':[{'id':j['id'],'name':j['name'],'status':j['status'],'conclusion':j['conclusion'],'active':[s['name'] for s in j['steps'] if s['status']=='in_progress']} for j in jobs['jobs']]};history.append(row);save('publication-monitor.json',history)
 print(json.dumps(row),flush=True)
 if run['status']=='completed':break
 time.sleep(20)
else:raise RuntimeError('Monitoring time bound reached; do not cancel or replay')
log=subprocess.run(['gh','run','view',str(rid),'--repo',repo,'--attempt','1','--log'],cwd=N,capture_output=True);(E/'publication.log').write_bytes(log.stdout);(E/'publication-log-fetch.txt').write_bytes(log.stderr)
art=api(f'repos/{repo}/actions/runs/{rid}/artifacts?per_page=100');save('publication-artifacts.json',art)
summary={'run':rid,'attempt':run['run_attempt'],'source':run['head_sha'],'conclusion':run['conclusion'],'url':run['html_url'],'jobs':row['jobs'],'logFetchExit':log.returncode,'logSHA256':hashlib.sha256(log.stdout).hexdigest(),'artifacts':[{'id':a['id'],'name':a['name'],'digest':a['digest'],'size':a['size_in_bytes'],'expires_at':a['expires_at']} for a in art['artifacts']]};save('publication-summary.json',summary);print(json.dumps(summary),flush=True)
assert run['conclusion']=='success','Publication failure/partial effects require precise diagnosis; no automatic retry'
