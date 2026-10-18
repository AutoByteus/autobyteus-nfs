from common import *
import tempfile,hashlib
E1=E.parent/'api-rev-001'
event('E01','Started','Verify current source identity and carry independent unchanged N only')
P=Path(tempfile.mkdtemp(prefix='nfs-extract-api002-S-',dir='/Users/normy')).resolve()
for d in ['repo','home','tmp','pnpm-store']:(P/d).mkdir()
R=P/'repo';env=envfor(P);write('environment.json',dict(S=str(P),envS=env))
roots=[p for p in subprocess.check_output(['git','-C',str(S),'ls-tree','--name-only','HEAD'],text=True).splitlines() if p!='tickets']
a=subprocess.Popen(['git','-C',str(S),'archive','HEAD',*roots],stdout=subprocess.PIPE)
b=subprocess.run(['tar','-xf','-','-C',str(R)],stdin=a.stdout);a.stdout.close();assert b.returncode==a.wait()==0
fixtures=[]
for f in json.loads((E1/'fixture-restoration.json').read_text())['files']:
 p=f['path'];data=subprocess.check_output(['git','-C',str(S),'show','HEAD:'+p]);dest=R/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 assert data==(S/p).read_bytes()
 fixtures.append(dict(path=p,sha256=hashlib.sha256(data).hexdigest()))
write('fixture-inputs.json',dict(files=fixtures,source='current S HEAD; restored before all checks'))
audit=json.loads((E/'input-audit.json').read_text())
mismatches=[p for p,h in audit['S']['paths'] if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not mismatches
write('archive-integrity.json',dict(S=len(audit['S']['paths']),fixtures=len(fixtures),mismatches=mismatches,source_head=audit['S']['head']))
write('toolchain.json',dict(node=subprocess.check_output(['node','--version'],env=env,text=True).strip(),pnpm=subprocess.check_output(['pnpm','--version'],env=env,text=True).strip(),python=subprocess.check_output(['python3','--version'],env=env,text=True).strip(),platform=subprocess.check_output(['uname','-a'],text=True).strip()))
event('E01','Checkpoint','Exact7307-source archive plus11 current replay inputs prepared; no stale build dependency','N/A','archive-integrity.json; fixture-inputs.json; carry-validity.json')
