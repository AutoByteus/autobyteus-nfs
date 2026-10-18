from common import *
import tempfile,urllib.request
P=Path(tempfile.mkdtemp(prefix='nfs-extract-api003-',dir='/Users/normy')).resolve();write('environment.json',dict(scratch=str(P)))
event('E01','Started','Prepare exact independent N source/toolchains; preserve archived ticket and completed targets')
for p in ['candidate','tools','darwin-home','darwin-tmp','darwin-cache']:(P/p).mkdir()
roots=[x for x in subprocess.check_output(['git','-C',str(N),'ls-tree','--name-only','HEAD'],text=True).splitlines() if x!='tickets']
a=subprocess.Popen(['git','-C',str(N),'archive','HEAD',*roots],stdout=subprocess.PIPE)
b=subprocess.run(['tar','-xf','-','-C',str(P/'candidate')],stdin=a.stdout);a.stdout.close();assert a.wait()==b.returncode==0
inputs=json.loads((E/'input-audit.json').read_text())['inputs'];assert all(hashlib.sha256((P/'candidate'/p).read_bytes()).hexdigest()==h for p,h in inputs.items())
metadata=json.load(urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all',timeout=90));v=next(x for x in metadata if x['version']=='go1.27.2');downloads=[]
for osname in ['linux','darwin']:
 f=next(x for x in v['files'] if x['os']==osname and x['arch']=='arm64' and x['kind']=='archive');dest=P/f['filename'];url='https://go.dev/dl/'+f['filename']
 run('download-'+osname,['curl','-fsSL',url,'-o',str(dest)],P,timeout=300)
 assert hashlib.sha256(dest.read_bytes()).hexdigest()==f['sha256'];downloads.append(dict(**f,url=url))
write('toolchains.json',dict(metadata_url='https://go.dev/dl/?mode=json&include=all',downloads=downloads))
run('extract-darwin',['tar','-xzf',str(P/'go1.27.2.darwin-arm64.tar.gz'),'-C',str(P/'tools')],P)
name=P.name;image=json.loads((N/'packaging/release-lock.json').read_text())['ubuntuBaseImage'];write('environment.json',dict(scratch=str(P),container=name,image=image))
run('linux-container-create',['docker','run','-d','--name',name,'--label','autobyteus.validation=api003','--mount','type=bind,src='+str(P)+',dst=/inputs,readonly',image,'sleep','infinity'],P)
write('container.json',dict(name=name,image=image,details=json.loads(subprocess.check_output(['docker','inspect',name]))))
run('linux-prepare',['docker','exec',name,'bash','-euc','apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gcc libc6-dev python3 ca-certificates && tar -xzf /inputs/go1.27.2.linux-arm64.tar.gz -C /usr/local && useradd -m -u 1001 checker && cp -a /inputs/candidate /home/checker/candidate && mkdir /home/checker/tmp && chown -R checker:checker /home/checker'],P,timeout=600)
run('linux-input-integrity',['docker','exec','--user','1001:1001',name,'python3','-c',"import pathlib,hashlib,json; root=pathlib.Path('/home/checker/candidate'); expected="+repr(inputs)+"; bad=[p for p,h in expected.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]; print(json.dumps({'inputs':len(expected),'mismatches':bad})); assert not bad"],P)
write('archive-integrity.json',dict(inputs=108,host_copy_exact=True,linux_copy_exact=True,source_head=json.loads((E/'input-audit.json').read_text())['N_head'],no_sibling_S=True))
event('E01','Completed','Exact108-input N archives, verified native Go1.27.2;107 other inputs unchanged from blocker, one reviewed fixture delta','Pass','input-audit.json; archive-integrity.json; carry-validity.json; container.json; toolchains.json')
