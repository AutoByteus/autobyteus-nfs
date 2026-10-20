from pathlib import Path
import subprocess,json,hashlib,datetime,urllib.request
E=Path(__file__).resolve().parent;R='repos/AutoByteus/autobyteus-nfs';P='238bdc183e8affac99ffdee9be9cb333b0eb126f';tag='f4a04fd0c80a6625708ba002b4cef5507a03f514';payload=Path('/Users/normy/nfs-first-final-dr013-gmvotux9/payload')
def api(p):return json.loads(subprocess.check_output(['gh','api',p],text=True))
a=api(R+'/releases/tags/v0.1.0');b=api(R+'/releases/417014769');latest=api(R+'/releases/latest');ref=api(R+'/git/ref/tags/v0.1.0');obj=api(R+'/git/tags/'+tag);assets=api(R+'/releases/417014769/assets?per_page=100')
assert a['id']==b['id']==latest['id']==417014769 and not a['draft'] and not a['prerelease'];assert ref['object']['sha']==tag and obj['object']['sha']==P
expected={p.name:p for p in (payload/'assets').iterdir()};assert {a['name'] for a in assets}==set(expected) and len(assets)==18
for x in assets:
 p=expected[x['name']];assert x['state']=='uploaded' and x['size']==p.stat().st_size and x['digest']=='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
req=urllib.request.Request('https://api.github.com/'+R+'/releases/tags/v0.1.0',headers={'User-Agent':'nfs-delivery-public-check'})
with urllib.request.urlopen(req,timeout=30) as resp:
 anon=json.load(resp);assert resp.status==200 and anon['id']==417014769 and anon['draft'] is False
v={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release':{'id':a['id'],'url':a['html_url'],'draft':a['draft'],'prerelease':a['prerelease'],'publishedAt':a['published_at'],'latestId':latest['id'],'anonymousReadable':True,'notesSha256':hashlib.sha256(a['body'].encode()).hexdigest()},'tagObject':tag,'payloadSource':P,'assetCount':len(assets),'allAssetApiDigestsAndSizesEqualOriginal':True,'main':api(R+'/git/ref/heads/main')['object']['sha'],'releaseRun':api(R+'/actions/runs/39233821032')['conclusion']}
assert v['releaseRun']=='success'
(E/'final-public-state.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v,indent=2))
