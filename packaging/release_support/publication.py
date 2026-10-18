"""Observe, bind, and advance a normal release without overwriting prior effects."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

from . import candidate, identity as i, payload, qualification

TAG_PREFIX = 'AutoByteus NFS retained payload\n'


def api(endpoint, method='GET', body=None, missing=False):
    i.require(endpoint.startswith(('repos/' + i.REPOSITORY + '/',
                                  'orgs/AutoByteus/packages/container/autobyteus-nfs')), 'Foreign publication API')
    args = ['gh', 'api', '--hostname', 'github.com', '--method', method, endpoint]
    if body is not None:
        args += ['--input', '-']
    try:
        raw = i.command(*args, input=json.dumps(body).encode() if body is not None else None)
        return i.decode(raw) if raw else None
    except subprocess.CalledProcessError as error:
        if missing and method == 'GET' and b'(HTTP 404)' in error.stderr:
            return None
        raise


def tag_binding(tag, source_commit):
    i.version(tag)
    prefix = 'repos/' + i.REPOSITORY + '/git/'
    ref = api(prefix + 'ref/tags/' + tag, missing=True)
    if ref is None:
        return None
    i.require(ref['object']['type'] == 'tag', 'Existing tag is not the owned annotated tag')
    obj = api(prefix + 'tags/' + i.hex_value(ref['object']['sha'], 40))
    i.require(obj['tag'] == tag and obj['object']['type'] == 'commit' and obj['object']['sha'] == source_commit,
              'Published tag points to different source')
    i.require(obj['message'].startswith(TAG_PREFIX), 'Tag has no retained-payload identity')
    binding = i.decode(obj['message'][len(TAG_PREFIX):].strip())
    i.fields(binding, 'repository version sourceCommit payloadSha256 envelope')
    i.require(binding['repository'] == i.REPOSITORY and binding['version'] == tag and
              binding['sourceCommit'] == source_commit, 'Tag annotation identity differs')
    i.hex_value(binding['payloadSha256'])
    return binding


def release(tag):
    return api(f'repos/{i.REPOSITORY}/releases/tags/{i.version(tag)}', missing=True)


def prepare(tag, source_commit, candidate_run, directory):
    """Read-only preflight resolves existing public state BEFORE rebuilding/signing."""
    i.version(tag)
    i.require(os.environ.get('GITHUB_REPOSITORY') == i.REPOSITORY and
              os.environ.get('GITHUB_REF') == 'refs/heads/main' and
              os.environ.get('GITHUB_SHA') == source_commit == i.commit(), 'Publish must use exact dispatch main')
    lock, q = qualification.load()
    i.require(q['candidate']['envelope']['runId'] == i.positive(candidate_run), 'Selected candidate run differs')
    c = candidate.fetch(q['candidate'], directory / 'candidate')
    i.require(c['version'] == tag, 'Candidate version differs')
    qualification.validate(directory / 'candidate')
    binding = tag_binding(tag, source_commit)
    existing = release(tag)
    image = package_version(tag)
    i.require(binding is not None or (existing is None and image is None), 'Remote stage without owned tag cannot be adopted')
    i.require(image is None or image['name'] == c['oci']['index'], 'Existing image version conflicts')
    if binding is not None:
        candidate.download(binding['envelope'], candidate.PAYLOAD, directory / 'payload', successful=False)
        i.require(i.sha(directory / 'payload/publication.json') == binding['payloadSha256'], 'Retained payload differs')
        receipt = payload.verify(directory / 'payload', directory / 'candidate')
        e = binding['envelope']
        i.require((receipt['runId'], receipt['runAttempt'], receipt['sourceCommit']) ==
                  (e['runId'], e['runAttempt'], e['workflowCommit']), 'Retained payload attempt differs')
        # An artifact from a failed run is valid only after the payload job actually
        # succeeded. Publication may subsequently have failed after tag creation.
        jobs = candidate.api(f'repos/{i.REPOSITORY}/actions/runs/{e["runId"]}/attempts/{e["runAttempt"]}/jobs?per_page=100')
        i.require(jobs['total_count'] <= 100 and any(job['name'] == 'payload' and job['conclusion'] == 'success'
                                                   for job in jobs['jobs']), 'Payload retention job was not successful')
        i.write_json(directory / 'binding.json', binding)
    diff = i.command('git', 'diff', '--name-status', c['sourceCommit'], source_commit).decode()
    i.write_json(directory / 'preflight.json', {'mode': 'resume' if binding else 'fresh',
                 'sourceCommit': source_commit, 'candidateCommit': c['sourceCommit'],
                 'productionHash': lock['qualifiedSourceHash'], 'interveningDiff': diff})
    return 'resume' if binding else 'fresh'


def bind(directory, candidate_dir, artifact_id, run_id, attempt):
    receipt = payload.verify(directory, candidate_dir)
    i.require((receipt['runId'], receipt['runAttempt']) == (run_id, attempt), 'Final payload run differs')
    e = candidate.envelope(artifact_id, run_id, attempt, receipt['sourceCommit'], candidate.PAYLOAD, successful=False)
    return {'repository': i.REPOSITORY, 'version': receipt['version'], 'sourceCommit': receipt['sourceCommit'],
            'payloadSha256': i.sha(directory / 'publication.json'), 'envelope': e}


def fresh_main(source_commit):
    remote = api(f'repos/{i.REPOSITORY}/git/ref/heads/main')
    i.require(remote['object']['type'] == 'commit' and remote['object']['sha'] == source_commit,
              'Remote main advanced; reintegrate before publication')


def body_for(directory, binding):
    notes = (directory / 'assets/release-notes.md').read_text()
    return notes + '\n\n<!-- nfs-publication\n' + json.dumps(binding, sort_keys=True) + '\n-->\n'


def reconcile_release(existing, directory, binding):
    if existing is None:
        i.command('gh', 'release', 'create', binding['version'], '--repo', i.REPOSITORY,
                  '--verify-tag', '--draft', '--prerelease=false', '--title', 'AutoByteus NFS ' + binding['version'],
                  '--notes', body_for(directory, binding))
        existing = release(binding['version'])
    i.require(existing['tag_name'] == binding['version'] and existing['prerelease'] is False and
              existing['body'] == body_for(directory, binding), 'Unrelated release/draft cannot be adopted')
    return existing


def verify_assets(existing, directory, add_missing):
    expected = i.inventory(directory / 'assets')
    remote = existing['assets']
    i.require(len(remote) == len({x['name'] for x in remote}) and
              {x['name'] for x in remote} <= set(expected), 'Duplicate/unexpected remote asset')
    with tempfile.TemporaryDirectory(prefix='nfs-assets-') as scratch:
        for asset in remote:
            name = asset['name']
            i.require(asset['size'] == expected[name]['size'], 'Existing asset size conflict: ' + name)
            output = Path(scratch) / name
            with output.open('xb') as stream:
                subprocess.run(['gh', 'api', '--hostname', 'github.com',
                                f'repos/{i.REPOSITORY}/releases/assets/{i.positive(asset["id"])}',
                                '-H', 'Accept: application/octet-stream'], stdout=stream, check=True, timeout=1800)
            i.require(i.file_record(output) == expected[name], 'Existing asset bytes conflict: ' + name)
    missing = set(expected) - {x['name'] for x in remote}
    i.require(not missing or add_missing, 'Published release is incomplete; cannot modify it')
    for name in sorted(missing):
        i.command('gh', 'release', 'upload', existing['tag_name'], directory / 'assets' / name, '--repo', i.REPOSITORY)
    if missing:
        verify_assets(release(existing['tag_name']), directory, False)


def package_version(tag):
    """GitHub package version inventory distinguishes absent tag from transport errors."""
    prefix = 'orgs/AutoByteus/packages/container/autobyteus-nfs'
    package = api(prefix, missing=True)
    if package is None:
        return None
    i.require(package['repository']['full_name'] == i.REPOSITORY, 'Container package belongs to different repository')
    matches = []
    for page in range(1, 101):
        versions = api(prefix + f'/versions?per_page=100&page={page}')
        matches.extend(x for x in versions if tag in x['metadata']['container']['tags'])
        if len(versions) < 100:
            i.require(len(matches) <= 1, 'Ambiguous container version')
            return matches[0] if matches else None
    raise ValueError('Container inventory exceeds bounded pagination')


def promote(candidate_dir, tag, allow_write):
    c = candidate.verify(candidate_dir)
    expected = c['oci']
    existing = package_version(tag)
    i.require(existing is None or existing['name'] == expected['index'], 'Container version tag conflict')
    i.require(existing is not None or allow_write, 'Published release lacks image version')
    if existing is None:
        with tempfile.TemporaryDirectory(prefix='nfs-promotion-oci-') as scratch:
            layout = Path(scratch) / 'layout'
            i.require(candidate.materialize_oci(candidate_dir / 'engine.oci.tar', layout) == expected,
                      'Retained OCI layout differs')
            i.command('skopeo', 'copy', '--all', '--preserve-digests',
                      'oci:' + str(layout), 'docker://' + i.IMAGE + ':' + tag)
        existing = package_version(tag)
        i.require(existing is not None and existing['name'] == expected['index'], 'Promoted image identity differs')
    # Re-download all manifests/layers anonymously, not just an authenticated HEAD.
    # The exact package may need Delivery's scoped visibility operation; no global
    # permission changes or authenticated fallback are performed here.
    with tempfile.TemporaryDirectory(prefix='nfs-public-oci-') as scratch:
        root = Path(scratch)
        auth = root / 'empty-auth.json'
        i.write_json(auth, {'auths': {}})
        archive = root / 'anonymous.oci.tar'
        i.command('skopeo', 'copy', '--all', '--preserve-digests', '--src-authfile', auth,
                  'docker://' + i.IMAGE + '@' + expected['index'], 'oci-archive:' + str(archive))
        i.require(candidate.oci(archive) == expected, 'Anonymous OCI identity differs')
    return {'versionId': existing['id'], 'digest': expected['index'], 'anonymousPlatforms': sorted(expected['children'])}


def publish(directory, candidate_dir, binding, journal=None):
    stages = []
    def stage(name):
        stages.append(name)
        if journal is not None:
            i.write_json(journal, {'result': 'incomplete', 'stages': stages, 'payload': binding,
                                  'note': 'An attempted remote effect may have completed; reconcile, never roll back.'})
    stage('validating-before-effects')
    receipt = payload.verify(directory, candidate_dir)
    i.require(binding['sourceCommit'] == receipt['sourceCommit'] and binding['version'] == receipt['version'] and
              binding['payloadSha256'] == i.sha(directory / 'publication.json'), 'Payload binding differs')
    q = qualification.validate(candidate_dir)
    ce = q['candidate']['envelope']
    i.require(candidate.envelope(ce['artifactId'], ce['runId'], ce['runAttempt'], ce['workflowCommit'],
                                candidate.CANDIDATE) == ce, 'Candidate expired/changed before publication')
    e = binding['envelope']
    i.require(candidate.envelope(e['artifactId'], e['runId'], e['runAttempt'], e['workflowCommit'],
                                candidate.PAYLOAD, successful=False) == e, 'Payload retention differs')
    # Re-download the retained artifact and check its exact bytes before any write.
    with tempfile.TemporaryDirectory(prefix='nfs-retained-') as scratch:
        retained = Path(scratch) / 'payload'
        candidate.download(e, candidate.PAYLOAD, retained, successful=False)
        i.require(i.sha(retained / 'publication.json') == binding['payloadSha256'], 'Retained receipt differs')
        payload.verify(retained, candidate_dir)
    observed = tag_binding(binding['version'], binding['sourceCommit'])
    i.require(observed is None or observed == binding, 'Existing tag binds a different payload')
    existing = release(binding['version'])
    if existing is not None:
        i.require(observed == binding, 'Release cannot precede owned tag')
        # Observe asset conflicts before any additional writes on a retry.
        i.require(existing['body'] == body_for(directory, binding) and existing['prerelease'] is False,
                  'Existing release identity conflict')
    image = package_version(binding['version'])
    c = candidate.verify(candidate_dir)
    i.require(image is None or image['name'] == c['oci']['index'], 'Existing image tag conflict')
    fresh_main(binding['sourceCommit'])  # immediately before first externally visible write
    if observed is None:
        stage('tag-write-attempted')
        obj = api(f'repos/{i.REPOSITORY}/git/tags', 'POST', {
            'tag': binding['version'], 'message': TAG_PREFIX + json.dumps(binding, sort_keys=True),
            'object': binding['sourceCommit'], 'type': 'commit'})
        api(f'repos/{i.REPOSITORY}/git/refs', 'POST', {'ref': 'refs/tags/' + binding['version'], 'sha': obj['sha']})
    i.require(tag_binding(binding['version'], binding['sourceCommit']) == binding, 'Remote tag verification failed')
    stage('tag-confirmed; draft-reconciliation-attempted')
    existing = reconcile_release(existing, directory, binding)
    stage('draft-confirmed; asset-reconciliation-attempted')
    verify_assets(existing, directory, existing['draft'])
    stage('assets-confirmed; image-promotion-and-anonymous-read-attempted')
    image_receipt = promote(candidate_dir, binding['version'], existing['draft'])
    if existing['draft']:
        stage('image-public-confirmed; release-publication-attempted')
        api(f'repos/{i.REPOSITORY}/releases/{i.positive(existing["id"])}', 'PATCH',
            {'draft': False, 'prerelease': False, 'make_latest': 'true'})
    final = release(binding['version'])
    i.require(final['draft'] is False and final['prerelease'] is False, 'Release remains unpublished')
    verify_assets(final, directory, False)
    stage('release-published; public-download-verification-attempted')
    # Public versioned HTTPS bytes must match the retained payload, not merely
    # authenticated draft downloads. Actual native execution remains downstream.
    with tempfile.TemporaryDirectory(prefix='nfs-public-assets-') as scratch:
        for name, expected in i.inventory(directory / 'assets').items():
            output = Path(scratch) / name
            url = f'https://github.com/{i.REPOSITORY}/releases/download/{binding["version"]}/{name}'
            i.command('curl', '--fail', '--silent', '--show-error', '--location', '--proto', '=https',
                      '--tlsv1.2', '--max-time', '600', '--max-filesize', str(expected['size']), url, '-o', output)
            i.require(i.file_record(output) == expected, 'Public download differs: ' + name)
        home = Path(scratch) / 'home'
        home.mkdir(mode=0o700)
        smoke = subprocess.run(['/bin/bash', str(Path(scratch) / 'autobyteus-nfs-install.sh'), 'version'],
                               env=os.environ | {'HOME': str(home), 'TMPDIR': scratch},
                               capture_output=True, text=True, check=True, timeout=600)
        i.require(smoke.stdout.strip() == binding['version'], 'Public installer/version smoke differs')
    return {'releaseUrl': final['html_url'], 'tag': binding['version'], 'sourceCommit': binding['sourceCommit'],
            'payload': binding, 'image': image_receipt,
            'installerSmoke': 'owned HOME, explicit version only, publication runner (Ubuntu amd64)',
            'remaining': 'Delivery must verify remaining native installer/signature downloads on supported owned hosts'}
