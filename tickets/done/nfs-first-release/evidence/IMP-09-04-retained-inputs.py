"""IMP-09-04; 2026-10-19; read-only retained bytes plus saved DR013 endpoints.
Command: PYTHONDONTWRITEBYTECODE=1 python3 tickets/done/nfs-first-release/evidence/IMP-09-04-retained-inputs.py
No remote API/credential, old code execution, signing, admission or publication.
"""
import datetime
import json
import platform
import sys
from pathlib import Path
from unittest.mock import patch

N=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent
sys.path.insert(0,str(N/'packaging'))
from release_support import candidate, identity as i, payload, publication, recovery, source_context as sc

P='238bdc183e8affac99ffdee9be9cb333b0eb126f'
C=Path('/Users/normy/nfs-first-candidate-api006-a8aune30/candidate')
D=Path('/Users/normy/nfs-first-final-dr013-gmvotux9/payload')
T=N/'tickets/done/nfs-first-release';saved=T/'delivery-evidence/dr-013'
executor=sc.current()
binding=i.read_json(saved/'actual-publication-receipt.json')['payload']
before={'candidate':i.inventory(C),'payload':i.inventory(D)}
result={'check':'IMP-09-04','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'commit':executor.commit,'environment':platform.platform(),'payloadSource':P,
        'limits':'Existing retained files and saved DR013 endpoint/job observations; NOT fresh remote/expiry/API/signing/publication verification.'}
with sc.frozen(executor,P) as source:
    snapshot=source.root
    c=candidate.verify(C,source)
    receipt=payload.verify(D,C,source)
    assert i.sha(D/'publication.json')==binding['payloadSha256']
    assert source.source_hash()=='3e1af43a4191c17ddf8a5d6043a1e374c5cd0101f2ac18dd6ee9fee79c131086'
    result.update(candidateRecordSha256=i.sha(C/'candidate.json'),publicationSha256=i.sha(D/'publication.json'),
                  originalSourceHash=source.source_hash(),executorSourceHash=executor.source_hash(),
                  candidateSource=c['sourceCommit'],payloadReceiptSource=receipt['sourceCommit'],
                  signing=i.read_json(D/'assets/release-provenance.json')['signing'])
    tag={'object':'f4a04fd0c80a6625708ba002b4cef5507a03f514','binding':binding}
    try:recovery.admit(executor,source,tag)
    except ValueError as error:
        assert str(error)=='Reviewed recovery authorization required'
        result['realAuthorityAbsenceRefusal']=str(error)
    else:raise AssertionError('Real authorization must not exist')
    jobs=i.read_json(saved/'publication-final-jobs.json')
    expected=f'repos/{i.REPOSITORY}/actions/runs/39215470944/attempts/1/jobs?per_page=100&page=1'
    def saved_jobs(endpoint):
        assert endpoint==expected
        return {'total_count':len(jobs),'jobs':jobs}
    with patch.object(candidate,'api',side_effect=saved_jobs):result['savedPayloadJobId']=publication.payload_jobs(binding,117940491787)
    draft=i.read_json(saved/'draft-by-id.json')
    def saved_release(endpoint,**kwargs):
        if endpoint==publication.RELEASES+'?per_page=100&page=1':return [draft]
        if endpoint==publication.RELEASES+'/417014769':return draft
        raise AssertionError('Unexpected saved-data endpoint: '+endpoint)
    with patch.object(publication,'api',side_effect=saved_release):
        result['savedSelectedDraftId']=publication.discover(D,binding,417014769)['id']
assert not snapshot.exists()
result['allowedActualRepairDelta']=recovery.scope(N,P,executor.commit,'v0.1.0',True)
try:candidate.verify(C)
except ValueError as error:result['currentCandidateRefusal']=str(error)
else:raise AssertionError('Old candidate admitted as new executor')
assert before=={'candidate':i.inventory(C),'payload':i.inventory(D)}
result.update(result='pass',retainedInputsUnchanged=True,snapshotCleanup=True)
(E/'IMP-09-04-retained-inputs.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
