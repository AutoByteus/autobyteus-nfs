# Case R05; source 585d416c2746cf2963058d591b0753d0db8088f5; executed 2026-10-18 UTC; environment local macOS26.5.2 arm64; Python3.9.6/Bash3.2.57
# Step: smoke-candidate-native.py; exact command/steps in body or companion result JSON. Reader annotation 2026-10-18T10:40:08.210765+00:00; original captured body follows unchanged.
from pathlib import Path
import json,subprocess,tempfile,hashlib,tarfile,shutil,datetime,os
E=Path(__file__).resolve().parent;T=E.parents[2]
resource=json.loads((E/'retained-candidate-resource.json').read_text());candidate=Path(resource['root'])/'candidate';record=json.loads((E/'actual-candidate.json').read_text());archive=candidate/'native/autobyteus-nfs-0.1.0-darwin-arm64.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['members']['native/'+archive.name]['sha256']
root=Path(tempfile.mkdtemp(prefix='nfs-first-api003-version-',dir=Path.home()));os.chmod(root,0o700);binary=root/'autobyteus-nfs';result={}
try:
 with tarfile.open(archive,'r:gz') as t:
  m=t.getmember('autobyteus-nfs');assert m.isreg() and 0<m.size<=100*1024**2
  binary.write_bytes(t.extractfile(m).read());binary.chmod(0o700)
  manifest=json.load(t.extractfile('release.json'));assert manifest['version']=='v0.1.0' and manifest['releaseTargets']==[] and manifest['schema']==2 and manifest['fieldValidation']=={'filesystem':'deferred','user':'deferred'}
 (root/'home').mkdir();(root/'tmp').mkdir()
 p=subprocess.run([str(binary),'version'],env={'PATH':'/usr/bin:/bin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp')},cwd=root,capture_output=True,text=True,timeout=30)
 (E/'candidate-native-version.log').write_text('# Case R05; commit585d416c2746cf2963058d591b0753d0db8088f5; local Macarm64/current CLI or real Actions-read API; date '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n$ '+str(binary)+' version\n'+p.stdout+p.stderr)
 result=dict(archive=str(archive),archiveSha256=hashlib.sha256(archive.read_bytes()).hexdigest(),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),binarySize=binary.stat().st_size,metadata=manifest,os=subprocess.check_output(['sw_vers'],text=True),machine=subprocess.check_output(['uname','-m'],text=True).strip(),file=subprocess.check_output(['file',str(binary)],text=True).strip(),exit=p.returncode,stdout=p.stdout,stderr=p.stderr,pass_=p.returncode==0 and p.stdout=='v0.1.0\n' and p.stderr=='',scope='Actual downloaded unsigned candidate CLI version in owned HOME only, no installation/setup/physical NFS/signature qualification')
 assert result['pass_'],result
 manifest_path=root/'release.json';manifest_path.write_text(json.dumps(manifest))
 checks=[]
 for name,value,needle in [('candidate',manifest,'does not admit the current computer/CPU'),('false-claim',{**manifest,'fieldValidation':{'filesystem':'deferred','user':'passed'}},'unsupported release schema or field-validation claim'),('legacy-claim',{**manifest,'qualifiedTargets':[]},'unknown field')]:
  manifest_path.write_text(json.dumps(value))
  q=subprocess.run([str(binary),'verify-release',str(manifest_path)],env={'PATH':'/usr/bin:/bin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp')},cwd=root,capture_output=True,text=True,timeout=30)
  row=dict(name=name,exit=q.returncode,stdout=q.stdout,stderr=q.stderr,pass_=q.returncode!=0 and q.stdout=='' and needle in q.stderr)
  checks.append(row);assert row['pass_'],row
 result['admissionRefusals']=checks
 result['noInstallEffects']=not (root/'home/.local').exists()
 assert result['noInstallEffects']
 result['scope']='Actual downloaded unsigned schema2 candidate: version exact stdout and expected candidate/false/legacy admission refusals. Positive release notice is native Go fixture evidence, not a signed/public install claim.'
finally:
 shutil.rmtree(root);result['scratchAbsent']=not root.exists();result['scratch']=str(root)
 (E/'candidate-native-version.json').write_text(json.dumps(result,indent=2)+'\n')
with (T/'api-e2e-test-progress.md').open('a') as f:f.write('| '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' | R05 | Completed | '+('Pass' if result['pass_'] else 'Fail')+' | actual retained Darwinarm64 CLI version on local Mac; owned scratch removed, no physical NFS qualification; evidence candidate-native-version.json |\n')
print(json.dumps({k:result[k] for k in ['exit','stdout','binarySha256','machine','scratchAbsent']},indent=2))
