"""Close only implementation-owned local scratch after evidence preservation."""
import hashlib,json,shutil,subprocess,tarfile
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4]
S=Path((E/'scratch-path.txt').read_text().strip())
N=Path((E/'native-source-root.txt').read_text().strip())
def write(name,value):(E/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
inputs=json.loads((E/'final-source-inputs.json').read_text())
with tarfile.open(S/'linux/source.tar') as tar:
 linux_inputs={x.name:hashlib.sha256(tar.extractfile(x).read()).hexdigest() for x in tar if x.isreg()}
assert linux_inputs==inputs
native=json.loads((E/'checks-result.json').read_text());linux=json.loads((E/'linux-checks-result.json').read_text());mut=json.loads((E/'mutations.json').read_text())
assert all(x['passed'] for x in native) and linux['passed'] and all(x['detected'] for x in mut)
for p in E.glob('mutation-*.log'):
 s=p.read_text();assert 'FAIL:' in s and 'ERROR:' not in s and 'FAILED (failures=1)' in s,p
assert (E/'input-oci.json').read_bytes()==(E/'copied-oci.json').read_bytes()
containers=[]
for p in E.rglob('linux-resource.json'):
 name=json.loads(p.read_text())['container']
 assert name.startswith('nfs-release-ir001-')
 remaining=subprocess.check_output(['/usr/local/bin/docker','ps','-aq','--filter','name=^/'+name+'$'],text=True).strip()
 assert not remaining,name
 containers.append(name)
removed=[]
for p in (S,N):
 assert p.name.startswith(('nfs-release-ir001-','nfs-release-ir001-check-')) and p.is_dir() and not p.is_symlink(),p
 shutil.rmtree(p);assert not p.exists();removed.append(str(p))
read_temp=Path('/tmp/nfs-release-design-read.txt')
if read_temp.exists():read_temp.unlink();removed.append(str(read_temp))
write('cleanup.json',{'result':'Complete','removedOwnedScratch':removed,'containersConfirmedAbsent':containers,'noPersistentDaemonOrMountedResourceCreated':True,'preserved':'Canonical NFS/app checkouts, PM data, historical worktrees/assets, shared Docker base cache untouched. No signing credential/hosted/publication resource created.'})
write('final-checks.json',{'result':'Implementation local checks passed; independent source review required','sourceCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'inputReviewCommit':'2051fd9559f4f4fa7beae68723429f8199b50004','sourceHashUnqualified':(E/'source-hash.log').read_text().strip(),'sourceInputCount':len(inputs),'exactIndependentNativeAndLinuxInputs':True,'nativeCheckGroups':len(native),'nativePython':{'collected':38,'executed':37,'skipped':1},'linuxPython':{'collected':38,'executed':35,'skipped':3},'goRacePackagesPerNativeOS':7,'goVetBuildVersion':'pass macOS26.5.2 arm64 and Ubuntu24.04 arm64 guest','crossCompile':'darwin/linux arm64/amd64, compilation only','realSkopeoTransport':'1.13.3 all-child preserve-digests success on synthetic OCI; identical index/children','mutationsDetected':len(mut),'hostedSigningPhysicalUserPublicationQualification':'NOT performed; default lock remains unqualified','cleanup':'Complete'})
print('final exact-source evidence and owned cleanup complete')
