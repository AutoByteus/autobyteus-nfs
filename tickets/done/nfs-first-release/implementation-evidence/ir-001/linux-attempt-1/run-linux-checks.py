"""Owned nonprivileged Linux packaging/native-check container; no host storage."""
import hashlib,json,os,shutil,subprocess,tarfile,time,urllib.request,uuid
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4];S=Path((E/'scratch-path.txt').read_text().strip())
linux=S/'linux';linux.mkdir();source=Path((E/'native-source-root.txt').read_text().strip())/'source'
with tarfile.open(linux/'source.tar','w') as tar:
 for p in sorted(source.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:tar.add(p,arcname=p.relative_to(source),recursive=False)
releases=json.load(urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all'))
f=next(x for r in releases if r['version']=='go1.27.2' for x in r['files'] if x['os']=='linux' and x['arch']=='arm64' and x['kind']=='archive')
archive=linux/'go.tar.gz';urllib.request.urlretrieve('https://go.dev/dl/'+f['filename'],archive)
assert hashlib.sha256(archive.read_bytes()).hexdigest()==f['sha256']
name='nfs-release-ir001-'+uuid.uuid4().hex[:10]
base=json.loads((ROOT/'packaging/release-lock.json').read_text())['ubuntuBaseImage']
(E/'linux-resource.json').write_text(json.dumps({'container':name,'base':base,'toolchain':f,'mount':str(linux),'purpose':'local fixture/native checks only; no Docker socket or privileged mode'},indent=2)+'\n')
script='''set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gcc libc6-dev python3 ca-certificates skopeo
useradd -m -u 1001 checker
mkdir -p /work/src /work/home /work/tmp /work/cache /work/modcache /work/out
tar -xf /work/source.tar -C /work/src
tar -xzf /work/go.tar.gz -C /work
chown -R checker:checker /work
su checker -s /bin/bash -c '
set -eu
export HOME=/work/home TMPDIR=/work/tmp GOCACHE=/work/cache GOMODCACHE=/work/modcache GOTOOLCHAIN=local PYTHONDONTWRITEBYTECODE=1 PATH=/work/go/bin:/usr/bin:/bin
cd /work/src
uname -a; id; go version; python3 --version; skopeo --version
python3 -m unittest discover -s scripts/tests -p "test_nfs_*.py" -v
go test -race ./...
go vet ./...
go build -o /work/out/autobyteus-nfs ./cmd/autobyteus-nfs
/work/out/autobyteus-nfs version
python3 -c "import sys;from pathlib import Path;sys.path.insert(0,\\"scripts/tests\\");from nfs_release_fixture import make_oci;make_oci(Path(\\"/work/input.oci.tar\\"))"
skopeo copy --all --preserve-digests oci-archive:/work/input.oci.tar oci-archive:/work/copied.oci.tar
python3 packaging/release.py --operation oci --directory /work/input.oci.tar > /work/input-oci.json
python3 packaging/release.py --operation oci --directory /work/copied.oci.tar > /work/copied-oci.json
cmp /work/input-oci.json /work/copied-oci.json
'
'''
(linux/'run.sh').write_text(script)
started=time.time()
try:
 with (E/'linux-checks.log').open('w') as log:
  r=subprocess.run(['/usr/local/bin/docker','run','--name',name,'--rm','--label','autobyteus.task=nfs-first-release-ir001',
                    '-v',str(linux)+':/work',base,'bash','/work/run.sh'],stdout=log,stderr=subprocess.STDOUT)
 result={'exitCode':r.returncode,'passed':r.returncode==0,'seconds':round(time.time()-started,2),'container':name,
         'scope':'Ubuntu24.04 Linux arm64 native Go/Python and synthetic OCI transport; NOT mounted/physical/hosted qualification'}
 for file in ('input-oci.json','copied-oci.json'):
  if (linux/file).exists():shutil.copy2(linux/file,E/file)
finally:
 remaining=subprocess.check_output(['/usr/local/bin/docker','ps','-aq','--filter','name=^/'+name+'$'],text=True).strip()
 if remaining:subprocess.run(['/usr/local/bin/docker','rm','-f',name],check=True)
(E/'linux-checks-result.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
raise SystemExit(result['exitCode'])
