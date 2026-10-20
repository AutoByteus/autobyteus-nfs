from pathlib import Path
import subprocess,json,hashlib,io,zipfile,datetime,re
E=Path(__file__).resolve().parent;repo='repos/AutoByteus/autobyteus-nfs';runid=39233821032
sha=lambda b:hashlib.sha256(b).hexdigest()
def api(url):return json.loads(subprocess.check_output(['gh','api',url],text=True))
def write(name,value):(E/name).write_text(json.dumps(value,indent=2)+'\n')
r=api(f'{repo}/actions/runs/{runid}');assert r['status']=='completed'
jobs=api(f'{repo}/actions/runs/{runid}/attempts/1/jobs?per_page=100')['jobs'];art=api(f'{repo}/actions/runs/{runid}/artifacts?per_page=100')['artifacts'];write('publication-final-run.json',r);write('publication-final-jobs.json',jobs);write('publication-final-artifacts.json',art)
summary=[]
for j in jobs:
 row={'id':j['id'],'name':j['name'],'conclusion':j['conclusion'],'steps':j.get('steps',[])}
 if j['conclusion']!='skipped':
  b=subprocess.check_output(['gh','api',f'{repo}/actions/jobs/{j["id"]}/logs']);s=b.decode('utf-8-sig')
  # GitHub masks provisioned values. Refuse persistence if a known secret env line is visibly unmasked.
  for line in s.splitlines():
   m=re.search(r'\b(CERTIFICATE|PASSWORD|IDENTITY|APPLE_ID|APPLE_APP_SPECIFIC_PASSWORD|APPLE_TEAM_ID|GH_TOKEN): (.*)$',line)
   if m:assert m[2].strip()=='***', 'Unexpected unmasked secret-shaped env field; do not print/persist'
  name=f'publication-job-{j["id"]}.log';(E/name).write_bytes(b);row.update(log=name,sha256=sha(b),packageLines=[x for x in s.splitlines() if re.search(r'\bok\s+github.com/AutoByteus/autobyteus-nfs/',x)],testSummary=[x for x in s.splitlines() if re.search(r'Ran \d+ tests|OK \(skipped=|FAILED \(',x)],errors=[x for x in s.splitlines() if '##[error]' in x or 'Signing failed:' in x or 'Release refused:' in x])
 summary.append(row)
write('publication-execution-summary.json',{'run':runid,'attempt':1,'conclusion':r['conclusion'],'source':r['head_sha'],'jobs':summary,'counts':{c:sum(j['conclusion']==c for j in jobs) for c in ['success','failure','cancelled','skipped']}})
proof=[]
for a in art:
 if a['name'] not in ['nfs-signing-darwin-arm64','nfs-signing-darwin-amd64']:continue
 b=subprocess.check_output(['gh','api',f'{repo}/actions/artifacts/{a["id"]}/zip']);assert 'sha256:'+sha(b)==a['digest']
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  members=z.infolist();assert 1<=len(members)<=2
  contents=[]
  for m in members:
   assert re.fullmatch(r'darwin-(arm64|amd64)-notary(?:-failure)?\.json',m.filename) and m.file_size<8192
   raw=z.read(m);v=json.loads(raw);allowed={'status','submissionId','teamId','binarySha256'} if 'submissionId' in v else {'schema','status','stage','exitCode','cleanup','diagnostic'};assert set(v)==allowed
   (E/('signing-'+m.filename)).write_bytes(raw);contents.append({'name':m.filename,'sha256':sha(raw),'receipt':v})
 proof.append({'artifactId':a['id'],'name':a['name'],'wrapperSha256':sha(b),'members':contents})
write('signing-artifact-receipts.json',proof)
print(json.dumps({'run':runid,'conclusion':r['conclusion'],'jobs':[[j['name'],j['conclusion']] for j in jobs],'safeSigningReceipts':proof},indent=2))
