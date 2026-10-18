import hashlib,json,pathlib,subprocess,tempfile,urllib.request
E=pathlib.Path(__file__).resolve().parent
S=pathlib.Path(tempfile.mkdtemp(prefix='nfs-release-ir003-',dir='/Users/normy/autobyteus_org'))
(E/'scratch-path.txt').write_text(str(S)+'\n')
releases=json.load(urllib.request.urlopen('https://go.dev/dl/?mode=json&include=all'))
r=next(x for x in releases if x['version']=='go1.27.2')
receipt=[]
for os in ('darwin','linux'):
 f=next(x for x in r['files'] if x['os']==os and x['arch']=='arm64' and x['kind']=='archive')
 p=S/f['filename'];urllib.request.urlretrieve('https://go.dev/dl/'+f['filename'],p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
 receipt.append(f)
 if os=='darwin':subprocess.run(['tar','-xzf',str(p),'-C',str(S)],check=True)
(E/'toolchain.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(S)
