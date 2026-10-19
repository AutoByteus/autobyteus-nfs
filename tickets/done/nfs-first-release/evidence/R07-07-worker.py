# R07; isolated current executor + actual retained bytes, fresh-observation-shaped external doubles;22205cc; localMacarm64/Python3.9.6;2026-10-19. NOT AUTHORITY.
from pathlib import Path
import sys,os,json,hashlib,shutil,subprocess,copy,datetime
from contextlib import ExitStack
from unittest.mock import patch
from urllib.parse import urlsplit,parse_qs
repo=Path(sys.argv[1]);inspection=Path(sys.argv[2]);observed=Path(sys.argv[3]);output=Path(sys.argv[4]);sys.path.insert(0,str(repo/'packaging'))
from release_support import identity as i,publication as p,candidate,payload,source_context as sc
C=inspection/'candidate';D=inspection/'payload';obs=i.read_json(observed);binding=obs['before']['tag']['binding'];tag=obs['before']['tag'];H=i.commit();before={'candidate':i.inventory(C),'payload':i.inventory(D)};hashH=i.source_hash()
def git(*args):return subprocess.check_output(['git',*args],cwd=repo,text=True).strip()
def commit():
 subprocess.run(['git','add','--','packaging/recovery'],cwd=repo,check=True,capture_output=True)
 subprocess.run(['git','-c','user.name=API Fixture','-c','user.email=fixture@example.invalid','commit','-m','SYNTHETIC API007 authority only, never publication'],cwd=repo,check=True,capture_output=True)
 return git('rev-parse','HEAD')
# This record exists ONLY in disposable clone; human evidence deliberately says SYNTHETIC.
authpath=repo/'packaging/recovery/v0.1.0/authorization.json';authpath.parent.mkdir(parents=True)
proof={}
for name in ['architectureReview','sourceReview','validation','retainedSigning','deliveryAuthorization']:
 path=authpath.parent/(name+'.txt');path.write_text('SYNTHETIC API007 CONTROL; NOT REAL RELEASE AUTHORITY: '+name+'\n');proof[name]={'path':str(path.relative_to(repo)),'sha256':i.sha(path)}
auth={'schema':1,'kind':'same-payload-executor-repair','repository':i.REPOSITORY,'version':'v0.1.0','payloadSourceCommit':binding['sourceCommit'],'tagObject':tag['object'],'binding':binding,'payloadJobId':117940491787,'expectedReleaseId':417014769,'executor':{'reviewedCommit':H,'sourceHash':hashH},'evidence':proof}
i.write_json(authpath,auth);E=commit();assert i.source_hash()==hashH
calls=[];effects=[];assets={};release=copy.deepcopy(obs['draft']);state={'missing':False,'image':None};original_run=subprocess.run

def api(endpoint,method='GET',body=None,missing=False):
 calls.append({'endpoint':endpoint,'method':method})
 if endpoint.endswith('/git/ref/heads/main'):return {'object':{'sha':i.commit(),'type':'commit'}}
 if endpoint.endswith('/git/ref/tags/v0.1.0'):return {'object':{'sha':tag['object'],'type':'tag'}}
 if '/git/tags/' in endpoint:return {'sha':tag['object'],'tag':'v0.1.0','object':{'type':'commit','sha':binding['sourceCommit']},'message':p.TAG_PREFIX+json.dumps(binding)}
 if endpoint==p.RELEASES+'?per_page=100&page=1':return [] if state['missing'] else [copy.deepcopy(release)]
 if endpoint==p.RELEASES+'/417014769/assets?per_page=100&page=1':return [copy.deepcopy(x) for x in assets.values()]
 if endpoint==p.RELEASES+'/417014769':
  if method=='PATCH':
   assert body=={'draft':False,'prerelease':False,'make_latest':'true'};release['draft']=False;effects.append('PATCH417014769')
  else:assert method=='GET'
  return copy.deepcopy(release)
 if endpoint==p.RELEASES+'/tags/v0.1.0':return copy.deepcopy(release) if not release['draft'] else None
 raise AssertionError('Unexpected external call '+method+' '+endpoint)

def jobs(endpoint):
 assert endpoint==f'repos/{i.REPOSITORY}/actions/runs/39215470944/attempts/1/jobs?per_page=100&page=1'
 return copy.deepcopy(obs['jobs'])

def download(envelope,name,destination,successful=True):
 origin=C if name==candidate.CANDIDATE else D
 expected=i.read_json(repo/'packaging/releases/v0.1.0/readiness.json')['candidate']['envelope'] if name==candidate.CANDIDATE else binding['envelope']
 assert envelope==expected and successful==(name==candidate.CANDIDATE)
 shutil.copytree(origin,destination)

def run(args,**kwargs):
 if args[:2]==['gh','api']:
  ident=int(args[4].rsplit('/',1)[1]);asset=next(a for a in assets.values() if a['id']==ident)
  with (D/'assets'/asset['name']).open('rb') as f:shutil.copyfileobj(f,kwargs['stdout'])
  return subprocess.CompletedProcess(args,0)
 assert args[0]=='git',f'Unexpected subprocess {args}'
 return original_run(args,**kwargs)

class Connection:
 def __init__(self,host,timeout):assert host=='uploads.github.com' and timeout==600
 def request(self,method,url,body,headers):
  assert method=='POST';parsed=urlsplit(url);assert parsed.path==f'/repos/{i.REPOSITORY}/releases/417014769/assets'
  name=parse_qs(parsed.query,strict_parsing=True)['name'][0];assert name not in assets
  size=0;h=hashlib.sha256()
  for block in iter(lambda:body.read(1024*1024),b''):size+=len(block);h.update(block)
  expected=before['payload']['assets/'+name];assert {'sha256':h.hexdigest(),'size':size}==expected
  assert int(headers['Content-Length'])==size and headers['Content-Type']=='application/octet-stream'
  self.response={'id':9000+len(assets),'name':name,'size':size,'state':'uploaded'};assets[name]=self.response;effects.append('STREAM '+name)
 def getresponse(self):
  data=json.dumps(self.response).encode()
  class Response:
   status=201
   def read(self,limit):assert len(data)<limit;return data
  return Response()
 def close(self):pass

def promote(cdir,version,allow_write,context,guard):
 assert candidate.verify(cdir,context)['sourceHash']=='3e1af43a4191c17ddf8a5d6043a1e374c5cd0101f2ac18dd6ee9fee79c131086';guard()
 if state['image'] is None:assert allow_write;state['image']={'id':1,'name':i.read_json(C/'candidate.json')['oci']['index']};effects.append('EMULATED OCI')
 return {'emulated':True,'digest':state['image']['name']}

def public_downloads(directory,version):
 assert version=='v0.1.0' and i.inventory(directory)==before['payload'];effects.append('EMULATED PUBLIC READ')

with ExitStack() as stack:
 stack.enter_context(patch.object(p,'api',side_effect=api));stack.enter_context(patch.object(candidate,'api',side_effect=jobs));stack.enter_context(patch.object(candidate,'download',side_effect=download));stack.enter_context(patch.object(p,'package_version',side_effect=lambda tag:state['image']));stack.enter_context(patch.object(p.http.client,'HTTPSConnection',Connection));stack.enter_context(patch.object(subprocess,'run',side_effect=run));stack.enter_context(patch.object(p,'promote',side_effect=promote));stack.enter_context(patch.object(p,'public_downloads',side_effect=public_downloads));stack.enter_context(patch.dict(os.environ,{'GITHUB_REPOSITORY':i.REPOSITORY,'GITHUB_EVENT_NAME':'workflow_dispatch','GITHUB_REF':'refs/heads/main','GITHUB_SHA':E,'GITHUB_RUN_ID':'7007','GITHUB_RUN_ATTEMPT':'1','GH_TOKEN':'SYNTHETIC-NOT-CREDENTIAL'}))
 state['missing']=True
 try:p.publish(D,C,binding,output.parent/'missing-receipt.json')
 except ValueError as err:assert str(err)=='Known release is missing; cannot recreate';missingRefusal=str(err)
 else:raise AssertionError('Expected known missing draft refusal')
 assert effects==[];state['missing']=False
 preflight=p.prepare('v0.1.0',E,39213489075,output.parent/'preflight');assert preflight['mode']=='recover' and preflight['payloadSourceCommit']==binding['sourceCommit']
 result=p.publish(D,C,binding,output.parent/'publish-receipt.json');assert result['result']=='published' and result['releaseId']==417014769 and result['executor']['commit']==E and result['reviewedCommit']==H and result['payloadSourceCommit']==binding['sourceCommit']
 assert len(assets)==len(before['payload'])-1 # publication.json is not a public asset
 assert not any(c['method']=='POST' for c in calls), 'No tag/draft create; raw asset streams separate'
 firstEffects=list(effects);count=len(effects);second=p.publish(D,C,binding);assert second['result']=='published' and effects[count:]==['EMULATED PUBLIC READ']
 # Hash-excluded generated drift still fails full-tree admission before effects.
 generated=repo/'cmd/autobyteus-nfs/release.json';generated.write_text('SYNTHETIC excluded-input drift\n');original_run(['git','add','--',str(generated)],cwd=repo,check=True,capture_output=True);original_run(['git','-c','user.name=API Fixture','-c','user.email=fixture@example.invalid','commit','-m','SYNTHETIC excluded drift negative'],cwd=repo,check=True,capture_output=True)
 drift=i.commit();os.environ['GITHUB_SHA']=drift;assert i.source_hash()==hashH;count=len(effects)
 try:p.publish(D,C,binding)
 except ValueError as err:assert 'Unreviewed recovery change' in str(err);driftRefusal=str(err)
 else:raise AssertionError('Expected full-tree drift refusal')
 assert len(effects)==count
assert before=={'candidate':i.inventory(C),'payload':i.inventory(D)}
i.write_json(output,{'case':'R07','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'R07-07-worker.py in isolated clone','environment':'Private HOME/TMP, actual retained bytes; all external effects EMULATED','reviewedH':H,'syntheticE':E,'syntheticDriftCommit':drift,'executorHash':hashH,'realPayloadSource':binding['sourceCommit'],'binding':binding,'syntheticAuthorityOnly':True,'realAuthorizationCreated':False,'missingKnownRefusal':missingRefusal,'excludedDriftRefusal':driftRefusal,'preflight':preflight,'result':result,'publicAssetCount':len(assets),'firstEffects':firstEffects,'completedRetryNoWrites':True,'endpointCalls':calls,'retainedInputsUnchanged':True,'pass':True,'limits':'Not actual hosted dispatch, permission, write/publication, registry/public HTTP or installer execution; synthetic records never leave removed clone'})
print('R07 COMPLETE REAL-BYTE EMULATED PATH PASS')
