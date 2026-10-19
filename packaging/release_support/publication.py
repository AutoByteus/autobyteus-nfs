"""Reconcile immutable payloads using a separately admitted current executor."""
from contextlib import contextmanager
from dataclasses import dataclass
import http.client
import json
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote

from . import candidate, identity as i, payload, readiness, recovery
from .source_context import current, frozen, tree, SELECTED, SourceContext

TAG_PREFIX = 'AutoByteus NFS retained payload\n'
RELEASES = f'repos/{i.REPOSITORY}/releases'

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


def tag_identity(tag):
    i.version(tag)
    prefix = f'repos/{i.REPOSITORY}/git/'
    ref = api(prefix + 'ref/tags/' + tag, missing=True)
    if ref is None:
        return None
    i.require(ref['object']['type'] == 'tag', 'Existing tag is not the owned annotated tag')
    oid = i.hex_value(ref['object']['sha'], 40)
    obj = api(prefix + 'tags/' + oid)
    i.require(obj['sha'] == oid and obj['tag'] == tag and obj['object']['type'] == 'commit', 'Tag object differs')
    source = i.hex_value(obj['object']['sha'], 40)
    i.require(obj['message'].startswith(TAG_PREFIX), 'Tag has no retained-payload identity')
    binding = i.fields(i.decode(obj['message'][len(TAG_PREFIX):].strip()),
                       'repository version sourceCommit payloadSha256 envelope')
    i.require(binding['repository'] == i.REPOSITORY and binding['version'] == tag and
              binding['sourceCommit'] == source, 'Tag annotation identity differs')
    i.hex_value(binding['payloadSha256'])
    return {'object': oid, 'binding': binding}


@dataclass(frozen=True)
class PublicationContext:
    executor: SourceContext
    source: SourceContext
    tag: dict
    mode: str
    authorization: dict = None
    authorization_ref: dict = None

    def identities(self):
        return {'mode': self.mode, 'executor': {'commit': self.executor.commit,
                'sourceHash': self.executor.source_hash(), 'workflow': i.WORKFLOW, 'workflowCommit': self.executor.commit,
                'runId': os.environ.get('GITHUB_RUN_ID'), 'runAttempt': os.environ.get('GITHUB_RUN_ATTEMPT')},
                'payloadSourceCommit': self.source.commit, 'tag': self.tag,
                'reviewedCommit': self.authorization['executor']['reviewedCommit'] if self.authorization else None,
                'authorization': self.authorization_ref}


@contextmanager
def context_for(tag, dispatch=True, inspect=False):
    executor = current()
    executor.assert_files(tree(executor.repository, executor.commit, SELECTED))
    if dispatch:
        i.require(os.environ.get('GITHUB_REPOSITORY') == i.REPOSITORY and
                  os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch' and
                  os.environ.get('GITHUB_REF') == 'refs/heads/main' and
                  os.environ.get('GITHUB_SHA') == executor.commit, 'Publish must use exact dispatch main')
        for key in ('GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT'):
            i.positive(int(os.environ.get(key, '0')))
        i.require(executor.blob(executor.commit, i.WORKFLOW) == (executor.root / i.WORKFLOW).read_bytes(),
                  'Dispatched executor workflow differs')
    tag_record = tag_identity(tag)
    i.require(not inspect or tag_record is not None, 'inspect-bound requires an owned annotated tag')
    p = tag_record['binding']['sourceCommit'] if tag_record else executor.commit
    with frozen(executor, p) as source:
        mode = 'fresh' if tag_record is None else 'resume' if p == executor.commit else 'recover'
        auth, ref = (recovery.admit(executor, source, tag_record)
                     if mode == 'recover' and not inspect else (None, None))
        yield PublicationContext(executor, source, tag_record, mode, auth, ref)


def payload_jobs(binding, expected_id=None):
    e = binding['envelope']
    prefix = f'repos/{i.REPOSITORY}/actions/runs/{e["runId"]}/attempts/{e["runAttempt"]}/jobs'
    jobs, seen = [], set()
    for page in range(1, 101):
        result = candidate.api(prefix + f'?per_page=100&page={page}')
        batch = result['jobs']
        i.require(type(batch) is list and len(batch) <= 100, 'Invalid jobs page')
        for job in batch:
            jid = i.positive(job['id'])
            i.require(jid not in seen and job['run_id'] == e['runId'] and job['run_attempt'] == e['runAttempt'] and
                      job['head_sha'] == binding['sourceCommit'], 'Payload job attempt/identity differs')
            seen.add(jid)
            jobs.append(job)
        if len(batch) < 100:
            i.require(result['total_count'] == len(jobs), 'Incomplete job inventory')
            break
    else:
        raise ValueError('Jobs exceed bounded pagination')
    def successful(name):
        matches = [x for x in jobs if x['name'] == name]
        i.require(len(matches) == 1 and matches[0]['status'] == 'completed' and matches[0]['conclusion'] == 'success',
                  'Missing/ambiguous/unsuccessful job: ' + name)
        return matches[0]
    job = successful('payload')
    i.require(expected_id is None or job['id'] == expected_id, 'Payload job ID differs')
    for runner, os_name, arch in (('macos-15', 'darwin', 'arm64'), ('macos-15-intel', 'darwin', 'amd64'),
                                  ('ubuntu-24.04', 'linux', 'amd64'), ('ubuntu-24.04-arm', 'linux', 'arm64')):
        native = successful(f'binaries ({runner}, {os_name}, {arch})')
        if os_name == 'darwin':
            steps = [x for x in native['steps'] if x['name'] == 'Developer ID and Accepted notarization before public effects']
            i.require(len(steps) == 1 and steps[0]['status'] == 'completed' and steps[0]['conclusion'] == 'success',
                      'Original Mac signing step did not succeed')
    return job['id']


def retained(ctx, directory, binding=None):
    binding = binding or ctx.tag['binding']
    _, q = readiness.load(ctx.source)
    c = candidate.fetch(q['candidate'], directory / 'candidate', ctx.source)
    i.require(c['version'] == binding['version'], 'Candidate version differs')
    candidate.download(binding['envelope'], candidate.PAYLOAD, directory / 'payload', successful=False)
    i.require(i.sha(directory / 'payload/publication.json') == binding['payloadSha256'], 'Retained payload differs')
    receipt = payload.verify(directory / 'payload', directory / 'candidate', ctx.source)
    e = binding['envelope']
    i.require((receipt['runId'], receipt['runAttempt'], receipt['sourceCommit']) ==
              (e['runId'], e['runAttempt'], e['workflowCommit']), 'Retained payload attempt differs')
    return payload_jobs(binding, ctx.authorization['payloadJobId'] if ctx.authorization else None)


def inspect_bound(tag, directory):
    i.require(not directory.exists(), 'Inspection destination must be new')
    with context_for(tag, dispatch=False, inspect=True) as ctx:
        job = retained(ctx, directory)
        report = ctx.identities() | {'verifiedPayloadJobId': job, 'executorPublicationAdmission': 'not performed'}
        i.write_json(directory / 'inspection.json', report)
        return report


def prepare(tag, source_commit, candidate_run, directory):
    i.require(not directory.exists() and source_commit == current().commit, 'Preflight source/destination differs')
    with context_for(tag) as ctx:
        _, q = readiness.load(ctx.source)
        i.require(q['candidate']['envelope']['runId'] == i.positive(candidate_run), 'Selected candidate run differs')
        if ctx.tag:
            retained(ctx, directory)
            i.write_json(directory / 'binding.json', ctx.tag['binding'])
        else:
            c = candidate.fetch(q['candidate'], directory / 'candidate', ctx.source)
            i.require(c['version'] == tag, 'Candidate version differs')
            readiness.validate(directory / 'candidate', ctx.source)
        published = api(RELEASES + '/tags/' + tag, missing=True)
        image = package_version(tag)
        i.require(ctx.tag is not None or (published is None and image is None), 'Remote stage without owned tag')
        if published is not None:
            owned_release(published, directory / 'payload', ctx.tag['binding'])
        i.require(image is None or image['name'] == q['oci']['index'], 'Existing image version conflicts')
        report = ctx.identities() | {'draftInventory': 'non-authoritative; deferred to publisher'}
        i.write_json(directory / 'preflight.json', report)
        return report


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


def inventory(endpoint):
    result, seen = [], set()
    for page in range(1, 101):
        batch = api(endpoint + f'?per_page=100&page={page}')
        i.require(type(batch) is list and len(batch) <= 100, 'Invalid inventory page')
        for item in batch:
            ident = i.positive(item['id'])
            i.require(ident not in seen, 'Repeated inventory ID/page')
            seen.add(ident)
            result.append(item)
        if len(batch) < 100:
            return result
    raise ValueError('Inventory exceeds bounded pagination')


def body_for(directory, binding):
    return ((directory / 'assets/release-notes.md').read_text() + '\n\n<!-- nfs-publication\n' +
            json.dumps(binding, sort_keys=True) + '\n-->\n')


def owned_release(record, directory, binding):
    i.require(type(record) is dict, 'Missing selected release response')
    ident = i.positive(record['id'])
    i.require(record['url'] == 'https://api.github.com/' + RELEASES + '/' + str(ident) and
              record['tag_name'] == binding['version'] and type(record['draft']) is bool and
              record['prerelease'] is False and record['body'] == body_for(directory, binding),
              'Unrelated release/draft cannot be adopted')
    return record


def discover(directory, binding, expected_id=None):
    matches = [x for x in inventory(RELEASES) if x['tag_name'] == binding['version']]
    i.require(len(matches) <= 1, 'Ambiguous matching releases')
    if not matches:
        i.require(expected_id is None, 'Known release is missing; cannot recreate')
        return None
    ident = i.positive(matches[0]['id'])
    i.require(expected_id is None or ident == expected_id, 'Selected release ID differs')
    owned_release(matches[0], directory, binding)
    direct = owned_release(api(RELEASES + '/' + str(ident)), directory, binding)
    i.require(direct['id'] == ident and direct['draft'] == matches[0]['draft'], 'Direct release identity/state differs')
    return direct


def reconcile_release(directory, binding, expected_id, guard):
    existing = discover(directory, binding, expected_id)
    if existing is not None:
        return existing
    guard()
    i.require(discover(directory, binding) is None, 'Release appeared before create; reconcile on new attempt')
    created = api(RELEASES, 'POST', {'tag_name': binding['version'], 'draft': True, 'prerelease': False,
                  'name': 'AutoByteus NFS ' + binding['version'], 'body': body_for(directory, binding)})
    i.require(type(created) is dict, 'Ambiguous draft creation response')
    ident = i.positive(created['id'])  # Ambiguous response stops, never another POST.
    owned_release(created, directory, binding)
    i.require(created['draft'] is True, 'Create did not return draft')
    confirmed = discover(directory, binding, ident)
    i.require(confirmed['draft'] is True, 'New draft changed state before confirmation')
    return confirmed


def upload(existing, path):
    ident = i.positive(existing['id'])
    endpoint = f'/repos/{i.REPOSITORY}/releases/{ident}/assets'
    i.require(existing['upload_url'] == 'https://uploads.github.com' + endpoint + '{?name,label}',
              'Unsafe release upload URL')
    i.safe_name(path.name)
    i.regular(path)
    token = os.environ.get('GH_TOKEN')
    i.require(bool(token), 'Publisher token required')
    connection = http.client.HTTPSConnection('uploads.github.com', timeout=600)
    try:
        with path.open('rb') as stream:
            connection.request('POST', endpoint + '?name=' + quote(path.name, safe=''), body=stream,
                headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/octet-stream',
                         'Content-Length': str(path.stat().st_size), 'User-Agent': 'autobyteus-nfs-publisher'})
            response = connection.getresponse()
            # No redirects or automatic POST retries; never log credential-bearing headers/body.
            i.require(response.status == 201, 'Asset upload failed or ambiguous; reconcile on new attempt')
            result = i.decode(response.read(i.JSON_LIMIT + 1))
            i.require(result['name'] == path.name and result['state'] == 'uploaded' and
                      result['size'] == path.stat().st_size, 'Upload response differs')
            i.positive(result['id'])
    finally:
        connection.close()


def verify_assets(existing, directory, add_missing, guard):
    expected = i.inventory(directory / 'assets')
    remote = inventory(RELEASES + '/' + str(i.positive(existing['id'])) + '/assets')
    names = [x['name'] for x in remote]
    i.require(len(names) == len(set(names)) and set(names) <= set(expected), 'Duplicate/unexpected remote asset')
    with tempfile.TemporaryDirectory(prefix='nfs-assets-') as scratch:
        for asset in remote:
            name = asset['name']
            i.require(asset['state'] == 'uploaded' and asset['size'] == expected[name]['size'], 'Asset state/size conflict')
            output = Path(scratch) / name
            with output.open('xb') as stream:
                subprocess.run(['gh', 'api', '--hostname', 'github.com',
                                f'{RELEASES}/assets/{i.positive(asset["id"])}', '-H', 'Accept: application/octet-stream'],
                               stdout=stream, check=True, timeout=600)
            i.require(i.file_record(output) == expected[name], 'Existing asset bytes conflict: ' + name)
    missing = set(expected) - set(names)
    i.require(not missing or add_missing, 'Published release is incomplete; cannot modify it')
    for name in sorted(missing):
        guard()
        upload(existing, directory / 'assets' / name)
    if missing:
        guard()
        verify_assets(existing, directory, False, guard)


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


def promote(candidate_dir, tag, allow_write, context, guard):
    c = candidate.verify(candidate_dir, context)
    expected = c['oci']
    existing = package_version(tag)
    i.require(existing is None or existing['name'] == expected['index'], 'Container version tag conflict')
    i.require(existing is not None or allow_write, 'Published release lacks image version')
    if existing is None:
        with tempfile.TemporaryDirectory(prefix='nfs-promotion-oci-') as scratch:
            layout = Path(scratch) / 'layout'
            i.require(candidate.materialize_oci(candidate_dir / 'engine.oci.tar', layout) == expected,
                      'Retained OCI layout differs')
            guard()
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


def public_downloads(directory, tag):
    with tempfile.TemporaryDirectory(prefix='nfs-public-assets-') as scratch:
        for name, expected in i.inventory(directory / 'assets').items():
            output = Path(scratch) / name
            url = f'https://github.com/{i.REPOSITORY}/releases/download/{tag}/{name}'
            i.command('curl', '--fail', '--silent', '--show-error', '--location', '--proto', '=https',
                      '--tlsv1.2', '--max-time', '600', '--max-filesize', str(expected['size']), url, '-o', output)
            i.require(i.file_record(output) == expected, 'Public download differs: ' + name)
        home = Path(scratch) / 'home'
        home.mkdir(mode=0o700)
        smoke = subprocess.run(['/bin/bash', str(Path(scratch) / 'autobyteus-nfs-install.sh'), 'version'],
                               env=os.environ | {'HOME': str(home), 'TMPDIR': scratch},
                               capture_output=True, text=True, check=True, timeout=600)
        i.require(smoke.stdout.strip() == tag, 'Public installer/version smoke differs')


def publish(directory, candidate_dir, binding, journal=None):
    stages, receipt = [], {'result': 'incomplete'}
    def stage(name):
        stages.append(name)
        if journal is not None:
            i.write_json(journal, receipt | {'stages': stages,
                'note': 'An attempted remote effect may have completed; reconcile, never roll back.'})
    stage('validating-before-effects')
    with context_for(i.version(binding['version'])) as ctx, tempfile.TemporaryDirectory(prefix='nfs-retained-') as scratch:
        receipt.update(ctx.identities())
        i.require(ctx.tag is None or ctx.tag['binding'] == binding, 'Existing tag binds a different payload')
        i.require(binding['sourceCommit'] == ctx.source.commit, 'Payload source differs')
        retained(ctx, Path(scratch), binding)
        # Preflight is transport, not authority. Compare against freshly downloaded proof.
        payload.verify(directory, candidate_dir, ctx.source)
        i.require(i.inventory(directory) == i.inventory(Path(scratch) / 'payload') and
                  i.inventory(candidate_dir) == i.inventory(Path(scratch) / 'candidate'), 'Transport differs from retained inputs')
        expected_id = ctx.authorization['expectedReleaseId'] if ctx.authorization else None
        existing = discover(directory, binding, expected_id)
        i.require(ctx.tag is not None or existing is None, 'Release cannot precede owned tag')
        image = package_version(binding['version'])
        c = candidate.verify(candidate_dir, ctx.source)
        i.require(image is None or image['name'] == c['oci']['index'], 'Existing image tag conflict')
        observed = ctx.tag
        def guard():
            fresh_main(ctx.executor.commit)
            i.require(tag_identity(binding['version']) == observed, 'Annotated tag changed during publication')
            if existing is not None:
                latest = discover(directory, binding, existing['id'])
                i.require(latest['draft'] == existing['draft'], 'Release state changed during publication')
        guard()
        if observed is None:
            stage('tag-write-attempted')
            obj = api(f'repos/{i.REPOSITORY}/git/tags', 'POST', {
                'tag': binding['version'], 'message': TAG_PREFIX + json.dumps(binding, sort_keys=True),
                'object': ctx.source.commit, 'type': 'commit'})
            oid = i.hex_value(obj['sha'], 40)
            api(f'repos/{i.REPOSITORY}/git/refs', 'POST', {'ref': 'refs/tags/' + binding['version'], 'sha': oid})
            observed = {'object': oid, 'binding': binding}
        guard()
        receipt['tag'] = observed
        stage('tag-confirmed; draft-reconciliation-attempted')
        existing = reconcile_release(directory, binding, expected_id, guard)
        receipt['releaseId'] = existing['id']
        guard()
        stage('draft-confirmed; asset-reconciliation-attempted')
        verify_assets(existing, directory, existing['draft'], guard)
        guard()
        stage('assets-confirmed; image-promotion-and-anonymous-read-attempted')
        image_receipt = promote(candidate_dir, binding['version'], existing['draft'], ctx.source, guard)
        guard()
        if existing['draft']:
            stage('image-public-confirmed; release-publication-attempted')
            api(RELEASES + '/' + str(existing['id']), 'PATCH',
                {'draft': False, 'prerelease': False, 'make_latest': 'true'})
        final = discover(directory, binding, existing['id'])
        published = api(RELEASES + '/tags/' + binding['version'])
        i.require(final['draft'] is False and owned_release(published, directory, binding)['id'] == final['id'] and
                  published['draft'] is False, 'Release remains unpublished or by-tag identity differs')
        existing = final
        guard()
        verify_assets(final, directory, False, guard)
        stage('release-published; public-download-verification-attempted')
        public_downloads(directory, binding['version'])
        return receipt | {'result': 'published', 'stages': stages, 'releaseUrl': final['html_url'],
                'payload': binding, 'image': image_receipt,
                'installerSmoke': 'owned HOME, explicit version only, Ubuntu amd64 publisher',
                'remaining': 'Delivery must verify other native installer/signature downloads on owned hosts'}
