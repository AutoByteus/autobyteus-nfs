# R05/R06; actual downloaded original bytes + fresh GET-only draft/job observations;6cb497f/22205cc; localMacarm64/Python3.9.6;2026-10-19UTC.
from pathlib import Path
import subprocess,json,sys,datetime,tarfile,hashlib
E=Path(__file__).resolve().parent;T=E.parent;N=T.parents[2];sys.path.insert(0,str(N/'packaging'))
from release_support import identity as i,publication as p,candidate

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(cid,name,v):(E/f'{cid}-07-{name}.json').write_text(json.dumps(v,indent=2)+'\n')
def event(cid,kind,result,note):
 with (T/'api-e2e-test-progress.md').open('a') as f:f.write(f'| {now()} | {cid} | {kind} | {result} | {note} |\n')
def row(cid,note):
 path=T/'api-e2e-execution-coverage-report.md';lines=path.read_text().splitlines()
 for index,l in enumerate(lines):
  if l.startswith('| '+cid+' |'):
   a=l.split('|');a[-3]=' Pass ';a[-2]=' '+note+' ';lines[index]='|'.join(a)
 path.write_text('\n'.join(lines)+'\n')
head=i.commit();root=Path(i.read_json(E/'R04-07-ownership.json')['directory']);D=root/'payload';C=root/'candidate';r=i.read_json(E/'R04-07-inspection.json');binding=r['tag']['binding'];meta={'commit':head,'date':now(),'environment':'localMacarm64 actual downloaded retained original bytes / liveGET','command':'R05-07-observe.py'}
event('R05','Started','Not Tested','Carry DR013 actual Accepted/signatures by matching newly inspected original archives/binaries, no new signing.')
signed=i.read_json(T/'delivery-evidence/dr-013/retained-payload-verification.json')['signatures'];provenance=i.read_json(D/'assets/release-provenance.json');assert i.sha(D/'publication.json')==binding['payloadSha256']
for target,proof in signed.items():
 archive=D/'assets'/f'autobyteus-nfs-0.1.0-{target}.tar.gz';assert i.sha(archive)==proof['archiveSha256']
 with tarfile.open(archive) as tar:actual=hashlib.sha256(tar.extractfile('autobyteus-nfs').read()).hexdigest()
 assert actual==proof['binarySha256']==proof['notary']['binarySha256']
 assert proof['codesignStrictExit']==0 and proof['DeveloperIdTeamTimestampRuntimeVerified'] and proof['notary']['status']=='Accepted'
 assert provenance['signing'][target]==proof['notary']
save('R05','carried-signatures',meta|{'case':'R05','payloadSha256':binding['payloadSha256'],'signatures':signed,'archiveAndBinaryMatchesFreshDownload':True,'attribution':'DR013 actual codesign/Accepted; current API only reads/hashes bytes; not new Apple or public download proof','pass':True})
row('R05','R05-07-carried-signatures.json: both fresh-downloaded original archives/binaries match DR013 strict DeveloperID/runtime/timestamp/Accepted proofs; no signing repeat.')
event('R05','Completed','Pass','Both original signed-byte proof exact; carried DR013 scope, not new Apple/public install.')
event('R06','Started','Not Tested','Fresh actual bounded inventory/direct-ID/tag/main/artifact/job GETs; current discovery known417014769.')
requests=[];orig=p.api

def observe(endpoint,method='GET',body=None,missing=False):
 assert method=='GET' and body is None
 result=orig(endpoint,method,body,missing);requests.append({'endpoint':endpoint,'method':method,'missingAllowed':missing,'result':result});return result
p.api=observe
try:
 before={'tag':p.tag_identity('v0.1.0'),'main':p.api(f'repos/{i.REPOSITORY}/git/ref/heads/main')}
 bytag=p.api(p.RELEASES+'/tags/v0.1.0',missing=True)
 draft=p.discover(D,binding,417014769);assets=p.inventory(p.RELEASES+'/417014769/assets')
 assert draft['id']==417014769 and draft['draft'] and bytag is None and assets==[]
 jobs=p.api(f'repos/{i.REPOSITORY}/actions/runs/39215470944/attempts/1/jobs?per_page=100&page=1')
 original_run=p.api(f'repos/{i.REPOSITORY}/actions/runs/39215470944/attempts/1')
 artifacts=[p.api(f'repos/{i.REPOSITORY}/actions/artifacts/{id}') for id in [12169472209,12168544425]]
 after={'tag':p.tag_identity('v0.1.0'),'main':p.api(f'repos/{i.REPOSITORY}/git/ref/heads/main')};assert before==after and before['tag']==r['tag']
 assert original_run['conclusion']=='failure' and original_run['head_sha']==binding['sourceCommit']
 assert all(not a['expired'] for a in artifacts)
finally:p.api=orig
# Exercise the current job validator with its real endpoint, not saved data.
original_api=candidate.api

def observe_jobs(endpoint):
 value=original_api(endpoint);requests.append({'endpoint':endpoint,'method':'GET','result':value});return value
candidate.api=observe_jobs
try:job=p.payload_jobs(binding,117940491787)
finally:candidate.api=original_api
save('R06','observations',meta|{'case':'R06','date':now(),'requests':requests,'before':before,'after':after,'draft':draft,'assets':assets,'publishedByTag':bytag,'jobs':jobs,'run':original_run,'artifacts':artifacts,'payloadJobValidated':job,'writes':0,'pass':True,'limit':'Positive known-draft visibility now; no future token permission/main freshness/publication claim'})
row('R06','R06-07-observations.json: by-tag absent, unique exact draft417014769/direct-ID/body match/0assets; actual payload117940491787 and4native/bothsign steps success within failed run; unexpired wrappers; GET-only tag/main unchanged.')
event('R06','Completed','Pass','Actual current list/directID fixes observed draft lookup; live retained job proof/expiry, no effects; run remains failed.')
print('R05/R06 PASS')
