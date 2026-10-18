from pathlib import Path
import subprocess,json,datetime,tempfile,hashlib,tarfile,os
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
run=39111348848;attempt=1;sha='518f4b51e251edaa6b5664f71c7171bde57bafc9';repo='AutoByteus/autobyteus-nfs'
def api(s):return json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/'+s],text=True))
def write(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
def event(s,e):
 with (T/'api-e2e-test-case-ledger.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R04 | '+s+' | '+e+' |\n')
r=api(f'actions/runs/{run}/attempts/{attempt}')
assert r['status']=='completed' and r['conclusion']=='success' and r['head_sha']==sha
artifacts=api(f'actions/runs/{run}/artifacts?per_page=100');matches=[a for a in artifacts['artifacts'] if a['name']=='nfs-release-candidate'];assert len(matches)==1
write('candidate-selection.json',dict(run=r,artifacts=artifacts,selectedArtifact=matches[0]['id'],selection='Exact successful run/attempt and unique named candidate, not latest-run guessing'))
root=Path(tempfile.mkdtemp(prefix='nfs-first-candidate-api001-',dir=Path.home()));os.chmod(root,0o700)
write('retained-candidate-resource.json',dict(owner='api_e2e_engineer/nfs-first-release/API-REV-001',root=str(root),run=run,attempt=attempt,artifact=matches[0]['id'],purpose='Actual candidate retained for qualification/recovery; not repository generated source'))
rows=[]
def cmd(name,args,expected=0,contains=None):
 argv=['/usr/bin/python3',str(N/'packaging/release.py')]+list(map(str,args));p=subprocess.run(argv,cwd=N,capture_output=True,text=True,timeout=2400,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(E/(name+'.log')).write_text('$ '+' '.join(argv)+'\n'+p.stdout+p.stderr)
 row=dict(name=name,command=argv,exit=p.returncode,expected=expected,pass_=p.returncode==expected and (contains is None or contains in p.stdout+p.stderr));rows.append(row);write('candidate-validation-results.json',rows);event(('Pass' if row['pass_'] else 'Fail')+' '+name,name+'.log');assert row['pass_'],row
 return p
cmd('candidate-envelope',['--operation','candidate-envelope','--artifact-id',matches[0]['id'],'--run-id',run,'--attempt',attempt,'--workflow-commit',sha,'--output',E/'candidate-envelope.json'])
cmd('candidate-fetch',['--operation','fetch-candidate','--envelope',E/'candidate-envelope.json','--directory',root/'candidate','--output',E/'candidate-reference.json'])
cmd('candidate-verify',['--operation','verify-candidate','--directory',root/'candidate','--output',E/'actual-candidate.json'])
c=json.loads((E/'actual-candidate.json').read_text());assert c['sourceCommit']==sha and c['workflowCommit']==sha
write('actual-engine-manifest.json',json.loads((root/'candidate/engine/engine-manifest.json').read_text()))
# Metadata-only admission probe. This reserved hostname is NOT a registry or first-pull proof.
base=['--tag','v0.1.0','--engine-image','registry.invalid/owned-api001/nfs@'+c['oci']['index'],'--engine-manifest',root/'candidate/engine/engine-manifest.json','--candidate',root/'candidate']
cmd('candidate-metadata-alias',base+['--output',E/'candidate-metadata-alias.json'])
with tarfile.open(next((root/'candidate/native').glob('*darwin-arm64.tar.gz')),'r:gz') as t:original=json.load(t.extractfile('release.json'))
alias=json.loads((E/'candidate-metadata-alias.json').read_text());assert alias['qualifiedTargets']==[];assert {k:v for k,v in alias.items() if k!='engineImage'}=={k:v for k,v in original.items() if k!='engineImage'}
write('candidate-metadata-diff.json',dict(changedKeys=[k for k in original if original[k]!=alias[k]],original=original,alias=alias,limit='Metadata only. registry.invalid was neither resolved nor contacted, no first-use pull or qualified binary exists.'))
bad=base.copy();bad[3]='registry.invalid/owned-api001/nfs@sha256:'+'0'*64
cmd('candidate-metadata-wrong-digest',bad,1,'Candidate metadata inputs differ')
bad=base.copy();bad[1]='v0.1.1'
cmd('candidate-metadata-wrong-version',bad,1,'Candidate metadata inputs differ')
cmd('candidate-unqualified-refusal',['--check-publish','--candidate',root/'candidate'],1,'No qualified release targets: exactly all four required')
write('candidate-local-retention.json',dict(root=str(root),candidate=str(root/'candidate'),reference=json.loads((E/'candidate-reference.json').read_text()),members=len(c['members'])+1,bytes=sum(p.stat().st_size for p in (root/'candidate').rglob('*') if p.is_file()),zipRemoved=not (root/'candidate.zip').exists(),aliasIsNotQualification=True))
event('Pass actual artifact/engine/full OCI/four archives verified; alias-only admission and refusals; no host/first-pull qualification','candidate-validation-results.json; candidate-local-retention.json')
print(json.dumps(dict(candidate=str(root/'candidate'),sourceHash=c['sourceHash'],oci=c['oci'])))
