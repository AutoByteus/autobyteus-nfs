"""Candidate contents and exact Actions run/attempt/artifact reconciliation."""
import datetime
import selectors
import time
import hashlib
import shutil
import stat
import subprocess
import sys
import tarfile
import zipfile

from . import identity as i

sys.path.insert(0, str(i.ROOT / 'packaging/engine'))
from manifest import validate as validate_engine, verify_files

CANDIDATE = 'nfs-release-candidate'
PAYLOAD = 'nfs-release-payload'


def engine(directory, both=True):
    result = validate_engine(i.read_json(directory / 'engine-manifest.json'), require_both=both)
    for arch, bundle in result['architectures'].items():
        verify_files(bundle, directory / arch)
        i.regular(directory / arch / 'COPYRIGHT', 4 * 1024**2)
    return result


def oci(path):
    """Validate the complete retained OCI graph, not only an index digest string."""
    i.regular(path)
    with tarfile.open(path, 'r:') as archive:
        members = {}
        total = 0
        for entry in archive:
            name = entry.name.removeprefix('./')
            if entry.isdir():
                if name in ('', '.'):
                    continue
                i.safe_name(name.rstrip('/'))
                continue
            i.safe_name(name)
            i.require(entry.isreg() and name not in members and 0 < entry.size <= i.ARTIFACT_LIMIT,
                      'Unsafe/duplicate OCI member')
            total += entry.size
            i.require(total <= i.ARTIFACT_LIMIT and len(members) < 4096, 'OCI exceeds bounds')
            members[name] = entry
        i.require('oci-layout' in members and 'index.json' in members, 'Incomplete OCI layout')

        def raw(name):
            i.require(name in members and members[name].size <= i.JSON_LIMIT, 'Missing/oversized OCI metadata')
            return archive.extractfile(members[name]).read()

        i.require(i.decode(raw('oci-layout')) == {'imageLayoutVersion': '1.0.0'}, 'Unsupported OCI layout')
        outer = i.decode(raw('index.json'))
        i.require(outer['schemaVersion'] == 2 and len(outer['manifests']) == 1, 'Ambiguous OCI root')
        visited = {'oci-layout', 'index.json'}

        def blob(descriptor, metadata=False):
            digest = descriptor['digest']
            i.require(isinstance(digest, str) and digest.startswith('sha256:'), 'OCI digest type')
            name = 'blobs/sha256/' + i.hex_value(digest[7:])
            size = i.positive(descriptor['size'], i.ARTIFACT_LIMIT)
            i.require(name in members and members[name].size == size, 'Missing OCI child/size mismatch')
            stream = archive.extractfile(members[name])
            measured = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                measured.update(chunk)
            i.require(measured.hexdigest() == digest[7:], 'OCI child digest mismatch')
            visited.add(name)
            return i.decode(raw(name)) if metadata else None

        root = outer['manifests'][0]
        i.require(root['mediaType'] == 'application/vnd.oci.image.index.v1+json', 'Expected multiarch OCI index')
        index = blob(root, True)
        i.require(index['schemaVersion'] == 2 and len(index['manifests']) == 2, 'Exactly two OCI platforms required')
        children = {}
        for descriptor in index['manifests']:
            platform = descriptor['platform']
            target = platform['os'] + '-' + platform['architecture']
            i.require(target in ('linux-amd64', 'linux-arm64') and target not in children,
                      'Unexpected/duplicate OCI platform')
            i.require(descriptor['mediaType'] == 'application/vnd.oci.image.manifest.v1+json', 'OCI manifest type')
            manifest = blob(descriptor, True)
            i.require(manifest['schemaVersion'] == 2 and 0 < len(manifest['layers']) <= 128, 'OCI image shape')
            config = blob(manifest['config'], True)
            i.require(config['os'] == platform['os'] and config['architecture'] == platform['architecture'],
                      'OCI config/platform mismatch')
            for layer in manifest['layers']:
                blob(layer)
            children[target] = descriptor['digest']
        i.require(set(members) == visited, 'Unexpected unreferenced OCI content')
        return {'index': root['digest'], 'children': children}


def materialize_oci(archive_path, destination):
    """Copy verified bytes to an owned layout; never adopt archive uid/gid/modes.

    Noble skopeo's oci-archive reader tries chown on root-owned tar entries. The
    oci directory transport avoids that privilege requirement without changing
    the index or any blob, unlike rebuilding/repacking the image.
    """
    identity = oci(archive_path)
    i.require(not destination.exists(), 'OCI layout destination must be new')
    destination.mkdir(parents=True)
    with tarfile.open(archive_path, 'r:') as archive:
        for member in archive:
            if not member.isreg():
                continue  # oci() already refused everything except files/directories
            path = destination / member.name.removeprefix('./')
            path.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as source, path.open('xb') as output:
                shutil.copyfileobj(source, output)
    return identity


def runtime_metadata(tag, image, measured, release=False):
    i.version(tag)
    i.image_reference(image)
    if release:
        i.require(image.startswith(i.IMAGE + '@sha256:'), 'Canonical engine image required for publication')
    lock = i.read_json(i.ROOT / 'packaging/release-lock.json')
    return {'schema': 2, 'fieldValidation': dict(i.DEFERRED_FIELD_VALIDATION), 'version': tag, 'sourceHash': i.source_hash(measured),
            'ubuntuPackages': lock['ubuntuPackages'], 'engineImage': image,
            'releaseTargets': list(i.TARGETS) if release else [], 'engine': measured}


def native_archive(path, expected):
    i.regular(path, 104 * 1024**2)
    with tarfile.open(path, 'r:gz') as archive:
        members = archive.getmembers()
        i.require(len(members) == 4 and {x.name for x in members} == {
            'LICENSE', 'THIRD_PARTY_NOTICES', 'autobyteus-nfs', 'release.json'}, 'Native archive member set')
        for member in members:
            limit = 100 * 1024**2 if member.name == 'autobyteus-nfs' else i.JSON_LIMIT
            i.require(member.isreg() and 0 < member.size <= limit, 'Unsafe/oversized native member')
        metadata = i.decode(archive.extractfile('release.json').read())
        i.require(metadata == expected, 'Native metadata differs from release inputs')
        i.require(archive.extractfile('LICENSE').read() == (i.ROOT / 'LICENSE').read_bytes(), 'License differs')
        notices = archive.extractfile('THIRD_PARTY_NOTICES').read()
        i.require(notices.startswith((i.ROOT / 'THIRD_PARTY_NOTICES').read_bytes()), 'Notices missing')


def assemble(directory, tag, source_commit, workflow_commit, run_id, attempt):
    measured = engine(directory / 'engine')
    image = oci(directory / 'engine.oci.tar')
    expected = runtime_metadata(tag, i.IMAGE + '@' + image['index'], measured)
    for target in i.TARGETS:
        native_archive(directory / 'native' / i.archive_name(tag, target), expected)
    record = {'schema': 1, 'repository': i.REPOSITORY, 'workflow': i.WORKFLOW,
              'runId': i.positive(run_id), 'runAttempt': i.positive(attempt),
              'sourceCommit': i.hex_value(source_commit, 40), 'workflowCommit': i.hex_value(workflow_commit, 40),
              'version': i.version(tag), 'sourceHash': expected['sourceHash'],
              'engineManifestSha256': i.sha(directory / 'engine/engine-manifest.json'), 'oci': image,
              'buildInputs': {'go': i.GO_VERSION, 'ubuntuBaseImage': measured['source']['buildBase']},
              'members': i.inventory(directory)}
    i.write_json(directory / 'candidate.json', record)
    return verify(directory)


def verify(directory):
    record = i.read_json(directory / 'candidate.json')
    i.fields(record, 'schema repository workflow runId runAttempt sourceCommit workflowCommit version sourceHash engineManifestSha256 oci buildInputs members')
    i.require(record['schema'] == 1 and record['repository'] == i.REPOSITORY and record['workflow'] == i.WORKFLOW,
              'Foreign candidate identity')
    for key in ('runId', 'runAttempt'):
        i.positive(record[key])
    for key in ('sourceCommit', 'workflowCommit'):
        i.hex_value(record[key], 40)
    i.version(record['version'])
    workflow_bytes = i.command('git', 'show', record['workflowCommit'] + ':' + i.WORKFLOW)
    i.require(workflow_bytes == (i.ROOT / i.WORKFLOW).read_bytes(), 'Executed workflow differs from hashed source')
    i.verify_inventory(directory, record['members'], ('candidate.json',))
    measured = engine(directory / 'engine')
    lock = i.read_json(i.ROOT / 'packaging/release-lock.json')
    i.require(measured['source']['buildBase'] == lock['ubuntuBaseImage'], 'Engine base differs from release lock')
    expected_names = {'engine/engine-manifest.json', 'engine.oci.tar'}
    expected_names.update('native/' + i.archive_name(record['version'], target) for target in i.TARGETS)
    for arch, bundle in measured['architectures'].items():
        expected_names.update('engine/' + arch + '/' + x['file'] for x in
                              bundle['packages'] + [bundle['correspondingSource'], bundle['buildInventory']])
        expected_names.update({'engine/' + arch + '/COPYRIGHT', 'engine/' + arch + '/SHA256SUMS'})
    i.require(set(record['members']) == expected_names, 'Candidate contains unexpected/missing files')
    i.require(i.sha(directory / 'engine/engine-manifest.json') == record['engineManifestSha256'] and
              i.source_hash(measured) == record['sourceHash'], 'Candidate source/engine differs')
    i.require(record['buildInputs'] == {'go': i.GO_VERSION, 'ubuntuBaseImage': measured['source']['buildBase']},
              'Build inputs differ')
    image = oci(directory / 'engine.oci.tar')
    i.require(record['oci'] == image, 'Candidate OCI identity differs')
    expected = runtime_metadata(record['version'], i.IMAGE + '@' + image['index'], measured)
    for target in i.TARGETS:
        native_archive(directory / 'native' / i.archive_name(record['version'], target), expected)
    return record


def api(endpoint):
    """Read-only GitHub API. No mutation method is exposed by this owner."""
    i.require(endpoint.startswith('repos/' + i.REPOSITORY + '/'), 'Foreign API path')
    return i.decode(i.command('gh', 'api', '--hostname', 'github.com', endpoint))


def timestamp(value):
    return datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))


def envelope(artifact_id, run_id, attempt, source_commit, name, successful=True):
    """Attempt-specific run + immutable artifact API data; no newest-artifact guess."""
    for value in (artifact_id, run_id, attempt):
        i.positive(value)
    prefix = 'repos/' + i.REPOSITORY + '/actions/'
    run = api(f'{prefix}runs/{run_id}/attempts/{attempt}')
    i.require(run['id'] == run_id and run['run_attempt'] == attempt and
              run['repository']['full_name'] == i.REPOSITORY and
              run['head_repository']['full_name'] == i.REPOSITORY and
              run['path'] == i.WORKFLOW and run['event'] == 'workflow_dispatch' and
              run['head_sha'] == source_commit, 'Actions run identity differs')
    if successful:
        i.require(run['status'] == 'completed' and run['conclusion'] == 'success', 'Candidate run not successful')
    artifact = api(f'{prefix}artifacts/{artifact_id}')
    now = datetime.datetime.now(datetime.timezone.utc)
    i.require(artifact['id'] == artifact_id and artifact['name'] == name and
              artifact['workflow_run']['id'] == run_id and artifact['workflow_run']['head_sha'] == source_commit,
              'Actions artifact/run mismatch')
    i.require(artifact['expired'] is False and timestamp(artifact['expires_at']) > now and
              timestamp(artifact['created_at']) >= timestamp(run['run_started_at']), 'Expired/stale-attempt artifact')
    digest = artifact['digest']
    i.require(isinstance(digest, str) and digest.startswith('sha256:'), 'Missing Actions artifact digest')
    i.hex_value(digest[7:])
    i.positive(artifact['size_in_bytes'], i.ARTIFACT_LIMIT)
    return {'artifactId': artifact_id, 'runId': run_id, 'runAttempt': attempt,
            'workflowCommit': source_commit, 'digest': digest, 'expiresAt': artifact['expires_at']}


def download(envelope_record, name, destination, successful=True):
    e = i.fields(envelope_record, 'artifactId runId runAttempt workflowCommit digest expiresAt')
    actual = envelope(e['artifactId'], e['runId'], e['runAttempt'], e['workflowCommit'], name, successful)
    i.require(actual == e, 'Retained artifact envelope differs')
    i.require(not destination.exists(), 'Artifact destination must be new')
    destination.mkdir(parents=True)
    wrapper = destination.parent / (destination.name + '.zip')
    i.require(not wrapper.exists(), 'Artifact scratch collision')
    # gh follows authenticated API redirects without forwarding credentials cross-host.
    # Stream with a hard bound rather than retaining multi-GB OCI wrappers in memory.
    args = ['gh', 'api', '--hostname', 'github.com',
            f'repos/{i.REPOSITORY}/actions/artifacts/{e["artifactId"]}/zip']
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        size = 0
        deadline = time.monotonic() + 1800
        with wrapper.open('xb') as stream, selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                i.require(remaining > 0 and selector.select(remaining), 'Actions artifact download timed out')
                chunk = process.stdout.read1(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                i.require(size <= i.ARTIFACT_LIMIT, 'Actions download exceeds bound')
                stream.write(chunk)
        i.require(process.wait(timeout=60) == 0, 'Actions artifact download failed')
        i.require(i.sha(wrapper) == e['digest'][7:], 'Actions wrapper digest mismatch')
        extract_wrapper(wrapper, destination)
    finally:
        if process.poll() is None:
            process.kill()
        process.wait()
        process.stdout.close()
        wrapper.unlink(missing_ok=True)


def extract_wrapper(wrapper, destination):
    with zipfile.ZipFile(wrapper) as archive:
        seen, total = set(), 0
        for entry in archive.infolist():
            name = entry.filename
            i.safe_name(name)
            mode = entry.external_attr >> 16
            i.require(not entry.is_dir() and not stat.S_ISLNK(mode) and
                      stat.S_IFMT(mode) in (0, stat.S_IFREG) and name not in seen,
                      'Unsafe/duplicate Actions member')
            seen.add(name)
            total += i.positive(entry.file_size, i.ARTIFACT_LIMIT)
            i.require(len(seen) <= 4096 and total <= i.ARTIFACT_LIMIT, 'Actions artifact exceeds bounds')
        for entry in archive.infolist():
            path = destination / entry.filename
            path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(entry) as source, path.open('xb') as output:
                shutil.copyfileobj(source, output)


def fetch(record, destination):
    """Readiness supplies a content hash AND external envelope; both must match."""
    i.fields(record, 'recordSha256 envelope')
    download(record['envelope'], CANDIDATE, destination)
    i.require(i.sha(destination / 'candidate.json') == record['recordSha256'], 'Release candidate record differs')
    candidate = verify(destination)
    e = record['envelope']
    i.require((candidate['runId'], candidate['runAttempt'], candidate['workflowCommit']) ==
              (e['runId'], e['runAttempt'], e['workflowCommit']), 'Candidate content/attempt differs')
    return candidate
