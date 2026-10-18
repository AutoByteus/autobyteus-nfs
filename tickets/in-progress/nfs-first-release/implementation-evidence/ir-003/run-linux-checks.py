"""Owned Linux arm64 local checks only; no privileged mode/socket/host storage."""
import json,subprocess,tarfile,time,uuid
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=E.parents[4];S=Path((E/'scratch-path.txt').read_text().strip())
linux=S/'linux';linux.mkdir(exist_ok=True)
with tarfile.open(linux/'source.tar','w') as tar:
 for name in json.loads((E/'final-source-inputs.json').read_text()):
  tar.add(S/'source'/name,arcname=name,recursive=False)
name='nfs-release-ir003-'+uuid.uuid4().hex[:10]
base=json.loads((ROOT/'packaging/release-lock.json').read_text())['ubuntuBaseImage']
(E/'linux-resource.json').write_text(json.dumps({'container':name,'base':base,'mount':str(S),'scope':'Ubuntu24.04 arm64 native unit/packaging only, no field testing'},indent=2)+'\n')
script='''set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gcc libc6-dev python3 ca-certificates
useradd -m -u 1001 checker
mkdir -p /work/src /work/home /work/tmp /work/cache /work/modcache /work/out
tar -xf /input/linux/source.tar -C /work/src
tar -xzf /input/go1.27.2.linux-arm64.tar.gz -C /work
chown -R checker:checker /work
su checker -s /bin/bash -c '\nset -eu
export HOME=/work/home TMPDIR=/work/tmp GOCACHE=/work/cache GOMODCACHE=/work/modcache GOTOOLCHAIN=local PYTHONDONTWRITEBYTECODE=1 PATH=/work/go/bin:/usr/bin:/bin
cd /work/src
uname -a; id; go version; python3 --version
python3 -m unittest discover -s scripts/tests -p "test_nfs_*.py" -v
go test -race ./...
go vet ./...
go build -o /work/out/autobyteus-nfs ./cmd/autobyteus-nfs
/work/out/autobyteus-nfs version
'
'''
(linux/'run.sh').write_text(script)
started=time.time()
try:
 with (E/'linux-checks.log').open('w') as log:
  r=subprocess.run(['/usr/local/bin/docker','run','--name',name,'--label','autobyteus.task=nfs-first-release-ir003',
                    '-v',str(S)+':/input:ro',base,'bash','/input/linux/run.sh'],stdout=log,stderr=subprocess.STDOUT)
 result={'exitCode':r.returncode,'passed':r.returncode==0,'seconds':round(time.time()-started,2),'container':name,
         'scope':'native Linux arm64 Go/Python local checks, NOT mounted/physical/hosted qualification'}
finally:
 remaining=subprocess.check_output(['/usr/local/bin/docker','ps','-aq','--filter','name=^/'+name+'$'],text=True).strip()
 if remaining:subprocess.run(['/usr/local/bin/docker','rm','-f',name],check=True)
(E/'linux-checks-result.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
raise SystemExit(result['exitCode'])
