# Case R04/R05/C01; actual candidate facade/downloaded CLI; source1c00b7a; local Macarm64/Actions API;2026-10-19UTC.
from pathlib import Path
import subprocess,json,datetime,tempfile,os,hashlib,tarfile,shutil,sys
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2];sha=json.loads((E/'R03-05-dispatch.json').read_text())['run']['head_sha']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(cid,name,obj):(E/f'{cid}-05-{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
def event(cid,kind,result,note):
 with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | {cid} | {kind} | {result} | {note} |\n')
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/AutoByteus/autobyteus-nfs/'+path],cwd=N,text=True))
def command(cid,name,args,expected=0,needle=None,env=None):
 p=subprocess.run(args,cwd=N,text=True,capture_output=True,timeout=1800,env=env or {**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 (E/f'{cid}-05-{name}.log').write_text(f'# Case {cid}; command {args!r}; cwd {N}; source{sha}; local macOS26.5.2 arm64/Python3.9.6; {now()}\n'+p.stdout+p.stderr+f'\nExit: {p.returncode}\n')
 result={'case':cid,'step':name,'utc':now(),'sourceCommit':sha,'environment':'local Macarm64/Actions API where invoked','command':list(map(str,args)),'exit':p.returncode,'expected':expected,'stdout':p.stdout,'stderr':p.stderr,'pass':p.returncode==expected and (needle is None or needle in p.stdout+p.stderr)}
 save(cid,name+'-result',result);assert result['pass'],result
 return p
mode=sys.argv[1]
if mode=='fetch':
 f=json.loads((E/'R03-05-final.json').read_text());r=f['run'];assert r['conclusion']=='success' and r['head_sha']==sha
 event('R04','Started','Not Tested','Fetch and verify unique actual current candidate via existing facade, not old-source metadata.')
 artifacts=api(f'actions/runs/{r["id"]}/artifacts?per_page=100');matches=[a for a in artifacts['artifacts'] if a['name']=='nfs-release-candidate'];assert len(matches)==1
 root=Path(tempfile.mkdtemp(prefix='nfs-first-candidate-api005-',dir=Path.home()));os.chmod(root,0o700)
 save('R04','retention',{'case':'R04','step':'Owned candidate retained for Delivery','utc':now(),'sourceCommit':sha,'root':str(root),'candidate':str(root/'candidate'),'run':r['id'],'attempt':r['run_attempt'],'artifact':matches[0]['id'],'environment':'private local APFS parent0700','owner':'API005; preserve through release'})
 cli=['/usr/bin/python3',str(N/'packaging/release.py')]
 command('R04','envelope',cli+['--operation','candidate-envelope','--artifact-id',str(matches[0]['id']),'--run-id',str(r['id']),'--attempt',str(r['run_attempt']),'--workflow-commit',sha,'--output',str(E/'R04-05-envelope.json')])
 command('R04','fetch',cli+['--operation','fetch-candidate','--envelope',str(E/'R04-05-envelope.json'),'--directory',str(root/'candidate'),'--output',str(E/'R04-05-reference.json')])
 command('R04','verify',cli+['--operation','verify-candidate','--directory',str(root/'candidate'),'--output',str(E/'R04-05-candidate.json')])
 c=json.loads((E/'R04-05-candidate.json').read_text());assert c['sourceCommit']==sha and c['workflowCommit']==sha
 wrong=json.loads((E/'R04-05-envelope.json').read_text());wrong['digest']='sha256:'+'0'*64;save('R04','wrong-envelope',wrong)
 command('R04','wrapper-refusal',cli+['--operation','fetch-candidate','--envelope',str(E/'R04-05-wrong-envelope.json'),'--directory',str(root/'refused-destination')],1,'Retained artifact envelope differs');assert not (root/'refused-destination').exists()
 save('R04','verification',{'case':'R04','step':'Actual complete artifact and wrapper-refusal assertions','utc':now(),'sourceCommit':sha,'sourceHash':c['sourceHash'],'engineManifestSha256':c['engineManifestSha256'],'oci':c['oci'],'files':len(list(p for p in (root/'candidate').rglob('*') if p.is_file())),'bytes':sum(p.stat().st_size for p in (root/'candidate').rglob('*') if p.is_file()),'corruptWrapperDestinationAbsent':True,'zipAbsent':not (root/'candidate.zip').exists(),'pass':True})
 event('R04','Completed','Pass','Actual complete candidate/reference verified; corrupt copied envelope refused before destination; retained for Delivery; R04-05-verification.json.')
 report=T/'api-e2e-execution-coverage-report.md';report.write_text(report.read_text().replace('|Read-only Actions/local|Not Tested|Pending current artifact|',f'|Read-only Actions/local|Pass|Actual artifact{matches[0]["id"]}; R04-05-reference.json/candidate.json/verification.json; wrong-wrapper refusal before destination. No old-record promotion.|'))
 print(str(root/'candidate'),c['sourceHash'],flush=True)
elif mode=='smoke':
 retained=json.loads((E/'R04-05-retention.json').read_text());candidate=Path(retained['candidate']);archive=next((candidate/'native').glob('*darwin-arm64.tar.gz'));root=Path(tempfile.mkdtemp(prefix='nfs-first-api005-smoke-',dir=Path.home()));event('R05','Started','Not Tested','New downloaded native Darwinarm64 version/candidate admission; owned HOME, no setup.')
 try:
  with tarfile.open(archive,'r:gz') as tar:
   for name in ['autobyteus-nfs','release.json']:
    member=tar.getmember(name);assert member.isfile() and member.size<100*1024*1024;(root/name).write_bytes(tar.extractfile(member).read())
  binary=root/'autobyteus-nfs';binary.chmod(0o700);home=root/'home';home.mkdir();tmp=root/'tmp';tmp.mkdir();env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(home),'TMPDIR':str(tmp)}
  p=command('R05','version',[str(binary),'version'],env=env);assert p.stdout=='v0.1.0\n' and p.stderr==''
  command('R05','candidate-refusal',[str(binary),'verify-release',str(root/'release.json')],1,'this release does not admit the current computer/CPU',env)
  assert not list(home.iterdir())
  out={'case':'R05','step':'Actual new downloaded native smoke','utc':now(),'sourceCommit':sha,'environment':subprocess.check_output(['sw_vers'],text=True),'archiveSha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'versionStdout':p.stdout,'candidateAdmissionRefused':True,'noHomeWrites':True,'scratch':str(root),'pass':True}
 finally:shutil.rmtree(root)
 report=T/'api-e2e-execution-coverage-report.md';report.write_text(report.read_text().replace('|Private HOME/local Macarm64|Not Tested|Pending new binary|','|Private HOME/local Macarm64|Pass|R05-05-smoke.json; actual version exact, candidate refusal expected, noHOMEwrites, scratch removed.|'))
 out['scratchAbsent']=not root.exists();save('R05','smoke',out);event('R05','Completed','Pass','Exact v0.1.0 stdout; candidate admission refused, no HOME writes; scratch removed. R05-05-smoke.json.');print('SMOKE PASS',flush=True)
elif mode=='final-verify':
 retained=json.loads((E/'R04-05-retention.json').read_text());command('C01','candidate-final-verify',['/usr/bin/python3',str(N/'packaging/release.py'),'--operation','verify-candidate','--directory',retained['candidate']])
else:raise SystemExit('mode required')
