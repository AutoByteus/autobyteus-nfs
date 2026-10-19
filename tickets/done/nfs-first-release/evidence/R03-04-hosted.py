# Case R03; dispatch/observe exact new build-only candidate; current IR00575f4dbe; macOS gh CLI plus native4 hosted;2026-10-19UTC.
from pathlib import Path
import subprocess,json,datetime,time,hashlib,base64,sys,re
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2];repo='AutoByteus/autobyteus-nfs'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):(E/('R03-04-'+name+'.json')).write_text(json.dumps(obj,indent=2)+'\n')
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/'+path],cwd=N,text=True))
def event(event,result,note):
 with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | R03 | {event} | {result} | {note} |\n')
mode=sys.argv[1]
if mode=='dispatch':
 sha=sys.argv[2];assert not (E/'R03-04-dispatch.json').exists(),'Never duplicate existing dispatch'
 ref=api('git/ref/heads/codex/nfs-first-release');assert ref['object']['sha']==sha
 wf=api('contents/.github/workflows/release-nfs.yml?ref='+sha);body=base64.b64decode(wf['content']);assert body==(N/'.github/workflows/release-nfs.yml').read_bytes()
 runs=api('actions/workflows/release-nfs.yml/runs?event=workflow_dispatch&per_page=50');old={r['id'] for r in runs['workflow_runs']}
 save('remote-before',{'case':'R03','step':'Exact remote workflow and inventory before dispatch','utc':now(),'sourceCommit':sha,'workflowBlob':wf['sha'],'workflowSha256':hashlib.sha256(body).hexdigest(),'tags':api('tags?per_page=100'),'releases':api('releases?per_page=100'),'main':api('git/ref/heads/main'),'priorRunIds':sorted(old)})
 cmd=['gh','workflow','run','release-nfs.yml','--repo',repo,'--ref','codex/nfs-first-release','-f','release_tag=v0.1.0','-f','source_sha='+sha,'-f','publish=false']
 p=subprocess.run(cmd,cwd=N,text=True,capture_output=True,timeout=60)
 (E/'R03-04-dispatch.log').write_text(f'# Case R03; source {sha}; local gh CLI; {now()}; cwd {N}\n$ '+ ' '.join(cmd)+'\n'+p.stdout+p.stderr+f'\nExit: {p.returncode}\n');assert p.returncode==0
 for n in range(30):
  matches=[r for r in api('actions/workflows/release-nfs.yml/runs?event=workflow_dispatch&per_page=50')['workflow_runs'] if r['id'] not in old and r['head_sha']==sha and r['head_branch']=='codex/nfs-first-release']
  if matches:break
  time.sleep(3)
 assert len(matches)==1,matches
 save('dispatch',{'case':'R03','step':'Actual new dispatch receipt','utc':now(),'command':cmd,'run':matches[0],'selection':'Exactly one new matching head/branch event relative to prior IDs; no latest guessing'})
 event('Checkpoint','Not Tested',f"Dispatched exact source{sha}, run{matches[0]['id']}/attempt{matches[0]['run_attempt']}; acceptance is not Pass.");print(matches[0]['id'],flush=True)
elif mode=='monitor':
 receipt=json.loads((E/'R03-04-dispatch.json').read_text());rid=receipt['run']['id'];attempt=receipt['run']['run_attempt'];sha=receipt['run']['head_sha'];previous=None
 for n in range(100):
  r=api(f'actions/runs/{rid}');j=api(f'actions/runs/{rid}/attempts/{attempt}/jobs?per_page=100');a=api(f'actions/runs/{rid}/artifacts?per_page=100');assert r['run_attempt']==attempt and r['head_sha']==sha
  states=[(x['id'],x['name'],x['status'],x['conclusion']) for x in j['jobs']];key=[r['status'],r['conclusion'],states,[(x['id'],x['name']) for x in a['artifacts']]]
  if key!=previous:
   obs={'case':'R03','utc':now(),'run':rid,'attempt':attempt,'source':sha,'status':r['status'],'conclusion':r['conclusion'],'jobs':states,'artifacts':[(x['id'],x['name']) for x in a['artifacts']]}
   with (E/'R03-04-observations.jsonl').open('a') as f:f.write(json.dumps(obs)+'\n')
   print(json.dumps(obs),flush=True);event('Checkpoint','Not Tested',f"Run{rid}/{attempt} {r['status']}/{r['conclusion']}; R03-04-observations.jsonl");previous=key
  if r['status']=='completed':
   save('final',{'case':'R03','step':'Actual completed Actions observation','utc':now(),'run':r,'jobs':j,'artifacts':a});break
  time.sleep(30)
 else:raise SystemExit('Monitor limit; run unresolved, NOT cancelled')
elif mode=='collect':
 f=json.loads((E/'R03-04-final.json').read_text());rid=f['run']['id'];sha=f['run']['head_sha'];before=json.loads((E/'R03-04-remote-before.json').read_text());after={'case':'R03','step':'Post-run public-state observation','utc':now(),'source':sha,'tags':api('tags?per_page=100'),'releases':api('releases?per_page=100'),'main':api('git/ref/heads/main'),'originalFailedRun':api('actions/runs/39121007787/attempts/1')}
 for k in ['tags','releases','main']:after[k+'Unchanged']=after[k]==before[k]
 save('remote-after',after);summary=[]
 for j in f['jobs']['jobs']:
  if j['conclusion']=='skipped':continue
  cmd=['gh','api',f'repos/{repo}/actions/jobs/{j["id"]}/logs'];p=subprocess.run(cmd,capture_output=True);assert p.returncode==0,p.stderr
  header=f'# Case R03; command {cmd!r}; source{sha}; environment {j["name"]}; {now()}\n# Original captured bytes follow unchanged.\n';name=f'R03-04-job-{j["id"]}.log';(E/name).write_bytes(header.encode()+p.stdout)
  lines=p.stdout.decode('utf-8-sig',errors='replace').splitlines();selected=[l for l in lines if any(s in l for s in ['##[error]','FAIL','unbound variable','Ran 52 tests','OK (skipped=','skipped ','ok  \t','test "$(out/autobyteus-nfs version)"','Artifact upload has successfully completed'])]
  excerpt=f'R03-04-excerpt-{j["id"]}.log';(E/excerpt).write_text(header+'\n'.join(selected)+'\n')
  summary.append({'job':j['id'],'name':j['name'],'conclusion':j['conclusion'],'log':name,'excerpt':excerpt,'nativePackagePassLines':[l for l in lines if re.search(r'Z ok\s+github.com/',l)],'pythonSummary':[l for l in lines if 'Ran 52 tests' in l or 'OK (skipped=' in l],'errors':[l for l in lines if '##[error]' in l],'rawBodySha256':hashlib.sha256(p.stdout).hexdigest()})
 save('summary',{'case':'R03','step':'Completed job log collection','utc':now(),'source':sha,'run':rid,'attempt':f['run']['run_attempt'],'jobs':summary,'limits':'Actual hosted candidate/native checks, no signing/diagnostic artifact upload or public release proof'})
 assert all(after[k+'Unchanged'] for k in ['tags','releases','main'])
 assert after['originalFailedRun']['conclusion']=='failure'
 print('COLLECTED',f['run']['conclusion'],[(x['name'],len(x['nativePackagePassLines'])) for x in summary],flush=True)
else:raise SystemExit('mode required')
