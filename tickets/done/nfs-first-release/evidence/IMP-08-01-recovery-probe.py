"""IMP-08-01: offline DR013 reproduction and existing recovery admission controls.
Command: PYTHONDONTWRITEBYTECODE=1 python3 tickets/done/nfs-first-release/evidence/IMP-08-01-recovery-probe.py
Input: a7eb8a819c604358a5b01bd66b1fe1ffda313b19, Darwin arm64/Python3.9.6, 2026-10-19.
No real remote, signing, retained payload/candidate or production-file mutation.
"""
import json
from pathlib import Path
import shutil
import sys
import tempfile
from unittest.mock import patch

R = Path(__file__).resolve().parents[4]
T = R/'tickets/done/nfs-first-release'
sys.path.insert(0, str(R/'scripts/tests'))
from nfs_release_fixture import Fixture
from release_support import identity as i, publication, payload

result = {'check':'IMP-08-01','command':__doc__.splitlines()[1][9:],
          'commit':'a7eb8a819c604358a5b01bd66b1fe1ffda313b19','environment':'Darwin arm64/Python3.9.6, offline command doubles and own fixture copy',
          'date':'2026-10-19','remoteCalls':False,'productionModified':False,'retainedInputsModified':False}
assessment = json.loads((T/'delivery-evidence/dr-013/failure-assessment.json').read_text())
observed = json.loads((T/'delivery-evidence/dr-013/draft-reconciliation-observation.json').read_text())
draft = observed['endpoints'][0]['body'][0]
original_binding = assessment['payload']
assert draft['id'] == 417014769 and draft['draft'] is True
scratch = Path(tempfile.mkdtemp(prefix='nfs-imp08-',dir='/Users/normy/autobyteus_org'))
try:
    (scratch/'assets').mkdir()
    notes = draft['body'].split('\n\n<!-- nfs-publication\n')[0]
    (scratch/'assets/release-notes.md').write_text(notes)
    assert publication.body_for(scratch,original_binding) == draft['body']
    calls = []
    def read_api(endpoint, method='GET', body=None, missing=False):
        assert method == 'GET', 'No mutation allowed in replay'
        calls.append(endpoint)
        if '/releases/tags/' in endpoint:return None
        if endpoint.endswith('/releases?per_page=100'):return [draft]
        if endpoint.endswith('/releases/417014769'):return draft
        raise AssertionError('Unexpected API endpoint')
    with patch.object(publication,'api',side_effect=read_api), patch.object(i,'command',return_value=b'') as command:
        found = publication.release('v0.1.0')
        assert found is None
        try:
            publication.reconcile_release(found,scratch,original_binding)
        except TypeError as error:
            result['draftLookup']={'releaseReturnedNone':True,'exception':str(error),
                'listOrIdRequested':any('/releases/tags/' not in x for x in calls),
                'mockCreateAttempts':sum(c.args[:3] == ('gh','release','create') for c in command.call_args_list),
                'realEffects':False}
        else:raise AssertionError('Original lookup unexpectedly reconciled draft')
    # Source-hash impact uses only a disposable copy, no actual repair/bypass.
    repo = scratch/'source'; repo.mkdir()
    for name in i.SOURCES + ('packaging/release-lock.json',):
        src,dst=R/name,repo/name;dst.parent.mkdir(parents=True,exist_ok=True)
        if src.is_dir():shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.deb'))
        else:shutil.copyfile(src,dst)
    before=i.source_hash(root=repo)
    owner=repo/'packaging/release_support/publication.py'
    with owner.open('a') as f:f.write('\n# Disposable source-hash sensitivity marker, not a production patch.\n')
    after=i.source_hash(root=repo)
    assert before != after
    result['publisherHash']={'before':before,'afterDisposableMarker':after,'changed':True}
    ref={'object':{'type':'tag','sha':'f4a04fd0c80a6625708ba002b4cef5507a03f514'}}
    tag=observed['endpoints'][2]['body']
    with patch.object(publication,'api',side_effect=[ref,tag]):
        try:publication.tag_binding('v0.1.0','b'*40)
        except ValueError as error:result['newExecutorTagRefusal']=str(error)
        else:raise AssertionError('Changed executor must not silently rebind old tag')
    fixture_root=scratch/'fixture';fixture_root.mkdir()
    f=Fixture(fixture_root)
    try:
        f.final_payload()
        with patch.object(i,'commit',return_value='b'*40):
            try:payload.verify(f.p,f.c)
            except ValueError as error:result['newExecutorPayloadRefusal']=str(error)
            else:raise AssertionError('Changed executor must not silently verify old payload source')
    finally:f.close()
    with patch.object(publication,'api',return_value={'object':{'type':'commit','sha':'b'*40}}):
        try:publication.fresh_main(original_binding['sourceCommit'])
        except ValueError as error:result['advancedMainRefusal']=str(error)
        else:raise AssertionError('Changed main must refuse old binding under current contract')
    assert result['newExecutorTagRefusal']=='Published tag points to different source'
    assert result['newExecutorPayloadRefusal']=='Publication inputs differ'
    assert result['advancedMainRefusal']=='Remote main advanced; reintegrate before publication'
    result['allExpectedObservationsConfirmed']=True
finally:
    shutil.rmtree(scratch)
    result['ownedScratchRemoved']=not scratch.exists()
    (T/'evidence/IMP-08-01-recovery-probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
