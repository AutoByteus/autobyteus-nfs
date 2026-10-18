"""Validate release-first distribution readiness, never fabricate evidence or field tests."""
from . import candidate
from . import identity as i

DISCLOSURE = ('Field validation: shared-filesystem/physical and user testing is deferred. '
              'Distribution and signature checks are not field qualification. '
              'Postpublication testing and any fixes will be tracked separately; fixes use a new release.')


def evidence(reference, root=None):
    root = root or i.ROOT
    i.fields(reference, 'path sha256')
    relative = i.safe_name(reference['path'])
    i.require(relative.parts[:2] != ('tickets', 'in-progress'), 'Release evidence must survive ticket archival')
    path = i.local_file(root, reference['path'], 64 * 1024**2)
    i.require(i.sha(path) == i.hex_value(reference['sha256']), 'Evidence missing/changed')
    return path


def load(root=None):
    root = root or i.ROOT
    lock = i.read_json(root / 'packaging/release-lock.json')
    i.fields(lock, 'ubuntuBaseImage ubuntuPackages engine releaseReadiness note')
    i.require(lock['releaseReadiness'] is not None and lock['engine'] is not None,
              'Current engine and structured release readiness required')
    return lock, i.read_json(evidence(lock['releaseReadiness'], root))


def validate(directory, root=None):
    root = root or i.ROOT
    lock, record = load(root)
    c = candidate.verify(directory)
    i.fields(record, 'schema kind version targets candidate sourceHash engineManifestSha256 oci '
                     'authorization checks fieldValidation postpublicationPlan review releaseNotes')
    i.require(type(record['schema']) is int and record['schema'] == 1 and record['kind'] == 'release-first',
              'Release readiness schema/kind differs')
    i.require(record['version'] == c['version'] and record['targets'] == list(i.TARGETS),
              'Release readiness version/targets differ')
    i.fields(record['candidate'], 'recordSha256 envelope')
    i.require(record['candidate']['recordSha256'] == i.sha(directory / 'candidate.json'), 'Readiness candidate differs')
    e = i.fields(record['candidate']['envelope'], 'artifactId runId runAttempt workflowCommit digest expiresAt')
    for key in ('artifactId', 'runId', 'runAttempt'):
        i.positive(e[key])
    i.hex_value(e['workflowCommit'], 40)
    i.require(isinstance(e['digest'], str) and e['digest'].startswith('sha256:'), 'Artifact digest missing')
    i.hex_value(e['digest'][7:])
    candidate.timestamp(e['expiresAt'])
    i.require((e['runId'], e['runAttempt'], e['workflowCommit']) ==
              (c['runId'], c['runAttempt'], c['workflowCommit']), 'Readiness attempt differs')
    i.require(record['sourceHash'] == c['sourceHash'] and
              record['engineManifestSha256'] == c['engineManifestSha256'] and record['oci'] == c['oci'],
              'Stale readiness source/engine/OCI')
    i.require(lock['engine'] == candidate.engine(directory / 'engine'), 'Release engine bytes differ')
    authorization = i.fields(record['authorization'], 'kind requirementsRevision version evidence')
    i.require(authorization['kind'] == 'publish-before-field-testing' and
              authorization['requirementsRevision'] == 'R3/SR004' and authorization['version'] == c['version'],
              'Release-first authorization differs')
    evidence(authorization['evidence'], root)
    checks = i.fields(record['checks'], 'native releaseControls')
    for check in checks.values():
        i.fields(check, 'status evidence')
        i.require(check['status'] == 'passed', 'Required prepublication check did not pass')
        evidence(check['evidence'], root)
    i.require(record['fieldValidation'] == i.DEFERRED_FIELD_VALIDATION, 'Field validation must be explicitly deferred')
    evidence(record['postpublicationPlan'], root)
    review = i.fields(record['review'], 'candidateCommit sourceHash evidence')
    i.require(review['candidateCommit'] == c['sourceCommit'] and review['sourceHash'] == c['sourceHash'],
              'Candidate-to-final source review differs')
    evidence(review['evidence'], root)
    evidence(record['releaseNotes'], root)
    i.command('git', 'merge-base', '--is-ancestor', c['sourceCommit'], 'HEAD', cwd=root)
    return record


def release_notes(record):
    """Preserve reviewed prose and append the mandatory, deterministic disclosure."""
    return evidence(record['releaseNotes']).read_text() + '\n\n' + DISCLOSURE + '\n'
