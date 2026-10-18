from pathlib import Path
import json,subprocess,datetime,shutil
E=Path(__file__).resolve().parent;N=E.parents[5];T=E.parents[2]
def run(name,args):
 p=subprocess.run(args,cwd=N,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
 (E/(name+'.log')).write_text('$ '+' '.join(args)+'\n'+p.stdout+p.stderr)
 r=dict(args=args,exit=p.returncode,stdout=p.stdout,stderr=p.stderr)
 try:r['json']=json.loads(p.stdout)
 except ValueError:pass
 return r
out={}
for name,cmd in [('local-os',['sw_vers']),('local-arch',['uname','-m']),('local-kernel',['uname','-r']),('local-disks',['df','-T',str(N)]),('local-tools',['bash','-c','for t in gh python3 go actionlint shellcheck docker tart limactl virsh; do command -v "$t" || true; done']),('remote-refs',['git','ls-remote','origin','refs/heads/main','refs/heads/codex/nfs-first-release','refs/tags/v0.1.0']),('docker-context',['docker','context','show']),('docker-containers',['docker','ps','--format','{{.Names}}\t{{.Image}}\t{{.Status}}'])]:
 try:out[name]=run(name,cmd)
 except (FileNotFoundError,subprocess.TimeoutExpired) as err:out[name]={'error':str(err)}
for name,endpoint in [('remote-repo','repos/AutoByteus/autobyteus-nfs'),('remote-workflows','repos/AutoByteus/autobyteus-nfs/actions/workflows'),('remote-runs','repos/AutoByteus/autobyteus-nfs/actions/workflows/release-nfs.yml/runs?per_page=20'),('remote-releases','repos/AutoByteus/autobyteus-nfs/releases?per_page=30'),('remote-artifacts','repos/AutoByteus/autobyteus-nfs/actions/artifacts?per_page=30')]:out[name]=run(name,['gh','api',endpoint])
for tool in ['tart','limactl']:
 if shutil.which(tool):out[tool+'-inventory']=run(tool+'-inventory',[tool,'list','--json'] if tool=='limactl' else [tool,'list','--format','json'])
(E/'inventory.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),observations=out,limits='Read-only known local surfaces/repo metadata. No arbitrary remote network probes/SSH/credential read or live resource changes. Local user host is not assigned disposable physical host.'),indent=2)+'\n')
for n,r in out.items():
 if n.startswith('remote') and 'json' in r:
  j=r['json'];print(n,'exit',r['exit'],'count',len(j) if isinstance(j,list) else j.get('total_count',j.get('default_branch','metadata')))
 else:print(n,r.get('exit'),r.get('stdout','')[:1000],r.get('error',''))
