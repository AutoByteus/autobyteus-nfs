from pathlib import Path
import subprocess,json,datetime,time,hashlib,base64
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2];repo='AutoByteus/autobyteus-nfs';sha='96c8de3a381f74ec8f2b9e93425fb90e17e7e693'
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/'+path],cwd=N,text=True))
def write(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
ref=api('git/ref/heads/codex/nfs-first-release');assert ref['object']['sha']==sha
wf=api('contents/.github/workflows/release-nfs.yml?ref='+sha);b=base64.b64decode(wf['content']);assert b==(N/'.github/workflows/release-nfs.yml').read_bytes()
before=api('actions/workflows/release-nfs.yml/runs?event=workflow_dispatch&per_page=50');old={r['id'] for r in before['workflow_runs']}
write('pre-dispatch.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ref=ref,workflow_blob=wf['sha'],workflow_sha256=hashlib.sha256(b).hexdigest(),runs=before,tags=api('tags?per_page=100'),releases=api('releases?per_page=100'),delivery_prerequisite='API002 reviewed-current branch staging only; no main merge or qualification'))
with (T/'api-e2e-coverage-investigation.md').open('a') as f:f.write('\nAPI002 R03 prerequisite resolved by current Delivery staging: reviewed remote ticket96c8de3 available, exact workflow bytes rechecked; no integration delta from reviewed IR002 source. Now execute ONLY publish=false candidate on this exact ref/source, v0.1.0, no candidate_run_id. Four native runners and two measured engine builds/complete OCI required; no signing/publication. Delivery records stay uncommitted/untouched.\n')
args=['gh','workflow','run','release-nfs.yml','--repo',repo,'--ref','codex/nfs-first-release','-f','release_tag=v0.1.0','-f','source_sha='+sha,'-f','publish=false']
p=subprocess.run(args,cwd=N,capture_output=True,text=True,timeout=60)
(E/'dispatch.log').write_text('$ '+' '.join(args)+'\n'+p.stdout+p.stderr);assert p.returncode==0,p.stderr
for attempt in range(20):
 runs=api('actions/workflows/release-nfs.yml/runs?event=workflow_dispatch&per_page=50')
 matches=[r for r in runs['workflow_runs'] if r['id'] not in old and r['head_sha']==sha and r['head_branch']=='codex/nfs-first-release']
 if matches:break
 time.sleep(3)
assert len(matches)==1,matches
r=matches[0];write('dispatch-receipt.json',dict(command=args,exit=p.returncode,run=r,identity_selection='Exactly one new workflow_dispatch run relative to pre-dispatch IDs, exact branch/head SHA; not latest-run guessing',candidate_mode_only=True))
with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R03 | Running hosted build-only run '+str(r['id'])+' attempt '+str(r['run_attempt'])+'; dispatch accepted NOT Pass | dispatch-receipt.json |\n')
print(r['id'],r['run_attempt'],r['html_url'],r['status'])
