import hashlib,json,pathlib,subprocess,time,zipfile
N=pathlib.Path('/Users/normy/autobyteus_org/autobyteus-nfs-worktrees/nfs-dashboard-release');E=N/'tickets/done/nfs-dashboard-release/delivery-evidence/dr-001';S=pathlib.Path('/Users/normy/nfs-dashboard-release-ytwviz3y')
for _ in range(150):
 if (E/'publication-resume-summary.json').exists():break
 time.sleep(5)
else:raise RuntimeError('Resume result unavailable')
d=json.loads((E/'publication-resume-summary.json').read_text());assert d['conclusion']=='success','Do not run public checks after failed resume'
arts=[x for x in d['artifacts'] if x['name']=='nfs-publication-receipt'];assert len(arts)==1;a=arts[0]
p=subprocess.run(['gh','api',f'repos/AutoByteus/autobyteus-nfs/actions/artifacts/{a["id"]}/zip'],capture_output=True);assert p.returncode==0
assert 'sha256:'+hashlib.sha256(p.stdout).hexdigest()==a['digest'];z=S/'publication-final-receipt.zip';z.write_bytes(p.stdout)
with zipfile.ZipFile(z) as archive:
 assert archive.namelist()==['publication-receipt.json'];info=archive.infolist()[0];assert info.file_size<65536
 receipt=json.loads(archive.read(info))
(E/'publication-receipt-final.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['result']=='published' and receipt['releaseId']==422823635 and receipt['payloadSourceCommit']=='448cef839b4919a1e3ae0489e8d86ae36f5cee33'
print('Actual publication receipt:',receipt['result'],receipt['releaseUrl'],flush=True)
p=subprocess.run(['python3','-B',str(E/'verify-public.py')],cwd=N);assert p.returncode==0,'Public verification failure: preserve evidence, diagnose'
p=subprocess.run(['python3','-B',str(E/'public-dashboard-smoke.py')],cwd=N);assert p.returncode==0,'Distributed dashboard smoke needs diagnosis'
print('Public download/install/launch checks finished; screenshots await human agent inspection',flush=True)
