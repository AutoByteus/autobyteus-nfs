from pathlib import Path
import subprocess, os, tempfile, json, hashlib, shutil, time, urllib.request
E=Path(__file__).resolve().parent
N=E.parents[4]
root=Path(tempfile.mkdtemp(prefix='nfs-extract-crr001-',dir='/Users/normy/autobyteus_org')).resolve()
(E/'scratch-path.txt').write_text(str(root)+'\n')
results=[]
def run(name,argv,cwd,env,expected=0):
    start=time.monotonic()
    with (E/(name+'.log')).open('w') as out:
        r=subprocess.run(argv,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=600)
    row={'name':name,'argv':argv,'exit':r.returncode,'expected':expected,'seconds':round(time.monotonic()-start,3)}
    results.append(row); (E/'checks-result.json').write_text(json.dumps(results,indent=2)+'\n'); print(row,flush=True)
    if r.returncode!=expected: raise RuntimeError(name)
try:
    source=root/'source';source.mkdir()
    files=subprocess.check_output(['git','-C',str(N),'ls-files','-z']).decode().split('\0')
    hashes={}
    for p in files:
        if not p or p.startswith('tickets/'):continue
        data=subprocess.check_output(['git','-C',str(N),'show','HEAD:'+p])
        target=source/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        target.chmod((N/p).stat().st_mode & 0o777)
        hashes[p]=hashlib.sha256(data).hexdigest()
    (E/'standalone-inputs.json').write_text(json.dumps(hashes,indent=2)+'\n')
    tool=root/'tools';tool.mkdir();a=tool/'go.tar.gz'
    url='https://go.dev/dl/go1.27.2.darwin-arm64.tar.gz'
    with urllib.request.urlopen(url,timeout=90) as r,a.open('wb') as w:shutil.copyfileobj(r,w)
    digest=hashlib.sha256(a.read_bytes()).hexdigest()
    assert digest=='76812b213b1b2302c978d28fa52fa92d541704b9e7d9d5db8002c50e4018c4c5'
    subprocess.run(['tar','-xzf',str(a),'-C',str(tool)],check=True)
    home=root/'home';home.mkdir();tmp=root/'tmp';tmp.mkdir()
    env={'PATH':str(tool/'go/bin')+':/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(home),'TMPDIR':str(tmp),'GOCACHE':str(root/'gocache'),'GOMODCACHE':str(root/'gomodcache'),'GOTOOLCHAIN':'local','PYTHONDONTWRITEBYTECODE':'1'}
    (E/'toolchain.json').write_text(json.dumps({'url':url,'sha256':digest,'version':subprocess.check_output([str(tool/'go/bin/go'),'version'],env=env,text=True)},indent=2)+'\n')
    for name,argv,expected in [('go-race',['go','test','-race','-count=1','./...'],0),('go-vet',['go','vet','./...'],0),('python',['python3','-m','unittest','discover','-s','scripts/tests','-p','test_*.py','-v'],0),('source-hash',['python3','packaging/release.py','--source-hash'],0),('publish-refusal',['python3','packaging/release.py','--check-publish'],1),('actionlint',['actionlint','.github/workflows/release-nfs.yml'],0),('shell',['bash','-n','scripts/public/nfs/install.sh'],0)]:run(name,argv,source,env,expected)
    assert all(hashlib.sha256((source/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
finally:
    shutil.rmtree(root)
    (E/'cleanup.json').write_text(json.dumps({'ownedScratch':str(root),'removed':not root.exists(),'resources':'No VM/container/mount/export/provider/browser actions; subprocesses waited normally.'},indent=2)+'\n')
