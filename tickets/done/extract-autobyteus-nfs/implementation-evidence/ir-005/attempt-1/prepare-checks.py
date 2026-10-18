from pathlib import Path
import subprocess,json,hashlib,shutil
E=Path(__file__).resolve().parent;N=E.parents[3]; P=Path((E/'scratch-path.txt').read_text().strip())
B=P/'baseline';B.mkdir()
for rel in subprocess.check_output(['git','-C',str(N),'ls-files','-z']).decode().split('\0'):
 if not rel or rel.startswith('tickets/'):continue
 p=N/rel
 if p.is_file():
  dest=B/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
metadata=json.loads(subprocess.check_output(['curl','-fsSL','https://go.dev/dl/?mode=json&include=all']))
version=next(x for x in metadata if x['version']=='go1.27.2')
downloads=[]
for osname in ['darwin','linux']:
 f=next(x for x in version['files'] if x['os']==osname and x['arch']=='arm64' and x['kind']=='archive')
 archive=P/f['filename']; subprocess.run(['curl','-fsSL','https://go.dev/dl/'+f['filename'],'-o',str(archive)],check=True)
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==f['sha256']
 downloads.append(f)
 if osname=='darwin':
  dest=P/'tools';dest.mkdir();subprocess.run(['tar','-xzf',str(archive),'-C',str(dest)],check=True)
(E/'toolchain-downloads.json').write_text(json.dumps(dict(metadata_url='https://go.dev/dl/?mode=json&include=all',files=downloads),indent=2)+'\n')
image=json.loads((N/'packaging/release-lock.json').read_text())['ubuntuBaseImage']
name='nfs-extract-ir005-'+P.name.rsplit('-',1)[1]
with (E/'linux-prepare.log').open('w') as log:
 for cmd in [
  ['docker','pull',image],
  ['docker','run','-d','--name',name,'--network','bridge','--mount','type=bind,src='+str(P)+',dst=/inputs,readonly',image,'sleep','infinity'],
  ['docker','exec',name,'bash','-euc','apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gcc libc6-dev python3 ca-certificates && tar -xzf /inputs/go1.27.2.linux-arm64.tar.gz -C /usr/local && useradd -m -u 1001 checker && cp -a /inputs/baseline /home/checker/baseline && mkdir /home/checker/tmp && chown -R checker:checker /home/checker'],
 ]:
  log.write('$ '+' '.join(cmd)+'\n');log.flush()
  subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
(E/'linux-container.json').write_text(json.dumps(dict(name=name,image=image,details=json.loads(subprocess.check_output(['docker','inspect',name])),purpose='Nonroot native Linux developer fixtures only, no Docker socket/privileged caps/live storage resources'),indent=2)+'\n')
print('prepared',name,flush=True)
