from pathlib import Path
import subprocess,json,hashlib,urllib.request,tarfile,tempfile
E=Path(__file__).resolve().parent;N=E.parents[4];S=Path('/Users/normy/autobyteus_org/autobyteus-worktrees/extract-autobyteus-nfs');scratch=Path((E/'scratch-path.txt').read_text().strip())
# Fresh official pinned toolchain metadata and archive; historical record is not validation.
entries=json.load(urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all',timeout=60))
file=next(f for v in entries if v['version']=='go1.27.2' for f in v['files'] if f['filename']=='go1.27.2.darwin-arm64.tar.gz')
url='https://go.dev/dl/'+file['filename'];p=scratch/'tools'/file['filename']
with urllib.request.urlopen(url,timeout=90) as response,p.open('wb') as out:
    while block:=response.read(1024*1024):out.write(block)
assert hashlib.sha256(p.read_bytes()).hexdigest()==file['sha256']
with tarfile.open(p) as t:t.extractall(scratch/'tools',filter='data')
(E/'toolchain.json').write_text(json.dumps({'url':url,'officialFile':file,'go':str(scratch/'tools/go/bin/go'),'actionlint':subprocess.check_output(['actionlint','--version'],text=True)},indent=2)+'\n')
consumer=Path(tempfile.mkdtemp(prefix='nfs-consumer-ir001-'));(E/'consumer-scratch-path.txt').write_text(str(consumer)+'\n')
for root,dest in [(N,scratch/'standalone'),(S,consumer/'repo')]:
    dest.mkdir();roots=[x for x in subprocess.check_output(['git','-C',str(root),'ls-tree','--name-only','HEAD'],text=True).splitlines() if x!='tickets']
    a=subprocess.Popen(['git','-C',str(root),'archive','HEAD',*roots],stdout=subprocess.PIPE);b=subprocess.run(['tar','-xf','-','-C',str(dest)],stdin=a.stdout);a.stdout.close();assert b.returncode==a.wait()==0
for x in ['home','tmp']:(consumer/x).mkdir()
(E/'check-inputs.json').write_text(json.dumps({'N':subprocess.check_output(['git','-C',str(N),'rev-parse','HEAD'],text=True).strip(),'S':subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip(),'standaloneArchive':str(scratch/'standalone'),'consumerArchive':str(consumer/'repo'),'archives':'all tracked source excluding historical tickets; separate temporary roots, no sibling source or Go replace'},indent=2)+'\n')
print('Prepared independent archives and verified toolchain',flush=True)
