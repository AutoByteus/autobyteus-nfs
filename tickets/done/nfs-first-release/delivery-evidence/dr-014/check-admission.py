from pathlib import Path
import sys,json,datetime
root=Path.cwd();sys.path.insert(0,str(root/'packaging'));from release_support import publication,readiness,payload,identity as i
E=Path(__file__).resolve().parent;C=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate');D=Path('/Users/normy/nfs-first-final-dr013-gmvotux9/payload')
with publication.context_for('v0.1.0',dispatch=False) as ctx:
 assert ctx.mode=='recover' and ctx.authorization['expectedReleaseId']==417014769 and ctx.authorization['executor']['reviewedCommit']=='6cb497f4a0bb83d52ddfc41b5aaad95a8e482440'
 readiness.validate(C,ctx.source);payload.verify(D,C,ctx.source);assert publication.payload_jobs(ctx.tag['binding'],117940491787)==117940491787
 draft=publication.discover(D,ctx.tag['binding'],417014769);r={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'identities':ctx.identities(),'realCommittedAuthorityValidated':True,'originalFullReadinessPayloadValidated':True,'actualSelectedRelease':draft['id'],'draft':draft['draft'],'effects':'None; dispatch=False read-only admission/data validation, not fake hosted execution'}
 (E/('admission-'+ctx.executor.commit+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
