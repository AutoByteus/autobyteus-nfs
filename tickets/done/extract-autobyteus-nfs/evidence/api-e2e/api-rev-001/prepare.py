from common import *
import tempfile,hashlib,urllib.request,tarfile
event('E01','Started','Create independent exact source archives; no runtime source mutation')
cfg={}
for label,root in [('N',N),('S',S)]:
 p=Path(tempfile.mkdtemp(prefix='nfs-extract-api001-'+label+'-',dir='/Users/normy')).resolve()
 for d in ['home','tmp','tools','repo']:(p/d).mkdir()
 roots=[x for x in subprocess.check_output(['git','-C',str(root),'ls-tree','--name-only','HEAD'],text=True).splitlines() if x!='tickets']
 a=subprocess.Popen(['git','-C',str(root),'archive','HEAD',*roots],stdout=subprocess.PIPE)
 b=subprocess.run(['tar','-xf','-','-C',str(p/'repo')],stdin=a.stdout);a.stdout.close();assert b.returncode==a.wait()==0
 cfg[label]=str(p)
 write('environment.json',cfg)
audit=json.loads((E/'input-audit.json').read_text())
for label in ['N','S']:
 r=Path(cfg[label])/'repo'
 mismatches=[p for p,h in audit[label]['paths'] if not (r/p).is_file() or hashlib.sha256((r/p).read_bytes()).hexdigest()!=h]
 assert not mismatches,mismatches
cfg['envN']=envfor(Path(cfg['N']),True);cfg['envS']=envfor(Path(cfg['S']));write('environment.json',cfg)
P=Path(cfg['N']);meta=json.load(urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all',timeout=90))
f=next(f for v in meta if v['version']=='go1.27.2' for f in v['files'] if f['filename']=='go1.27.2.darwin-arm64.tar.gz')
archive=P/'tools'/f['filename'];url='https://go.dev/dl/'+f['filename']
with urllib.request.urlopen(url,timeout=90) as inp,archive.open('wb') as out:
 while True:
  b=inp.read(1024*1024)
  if not b:break
  out.write(b)
assert hashlib.sha256(archive.read_bytes()).hexdigest()==f['sha256']
subprocess.run(['tar','-xzf',str(archive),'-C',str(P/'tools')],check=True)
write('toolchain.json',dict(goFile=f,url=url,go=subprocess.check_output([str(P/'tools/go/bin/go'),'version'],text=True),node=subprocess.check_output(['/Users/normy/.nvm/versions/node/v22.21.1/bin/node','--version'],text=True),python=subprocess.check_output(['/usr/bin/python3','--version'],text=True),actionlint=subprocess.check_output(['/opt/homebrew/bin/actionlint','--version'],text=True),platform=subprocess.check_output(['uname','-a'],text=True)))
write('archive-integrity.json',dict(N=len(audit['N']['paths']),S=len(audit['S']['paths']),mismatches=[],excluded='root tickets only; nested historic artifacts preserved'))
event('E01','Checkpoint','Exact independent archives verified, pinned official toolchain verified; source-contract audit still pending','N/A','archive-integrity.json; toolchain.json')
