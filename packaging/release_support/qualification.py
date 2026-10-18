"""Validate current evidence applicability; never create qualification or receipts."""
from . import candidate
from . import identity as i

CASES = ('create-connect', 'reciprocal-bytes', 'directory-visibility', 'permissions-locks-git',
         'safe-detach-refusal', 'restart-reconnect', 'private-state')
MODES = {(target, mode) for target in i.TARGETS
         for mode in (('mac-native',) if target.startswith('darwin') else ('linux-native', 'linux-docker'))}


def evidence(reference, root=None):
    root = root or i.ROOT
    i.fields(reference, 'path sha256')
    path = i.local_file(root, reference['path'], 64 * 1024**2)
    i.require(i.sha(path) == i.hex_value(reference['sha256']), 'Evidence missing/changed')
    return path


def load(root=None):
    root = root or i.ROOT
    lock = i.read_json(root / 'packaging/release-lock.json')
    i.require(lock['qualifiedTargets'] == list(i.TARGETS), 'No qualified release targets: exactly all four required')
    i.require(lock['userVerified'] is True and lock['engine'] is not None, 'Current engine/user evidence required')
    i.require(lock.get('qualification') is not None, 'Structured qualification required')
    return lock, i.read_json(evidence(lock['qualification'], root))


def validate(directory, root=None):
    root = root or i.ROOT
    lock, record = load(root)
    c = candidate.verify(directory)
    i.fields(record, 'schema candidate sourceHash engineManifestSha256 oci rows userVerification review releaseNotes')
    i.require(record['schema'] == 1, 'Qualification schema differs')
    i.require(record['candidate']['recordSha256'] == i.sha(directory / 'candidate.json'), 'Qualification candidate differs')
    i.fields(record['candidate'], 'recordSha256 envelope')
    e = i.fields(record['candidate']['envelope'], 'artifactId runId runAttempt workflowCommit digest expiresAt')
    i.positive(e['artifactId'])
    i.require(e['digest'].startswith('sha256:'), 'Artifact digest missing')
    i.hex_value(e['digest'][7:])
    candidate.timestamp(e['expiresAt'])
    i.require((e['runId'], e['runAttempt'], e['workflowCommit']) ==
              (c['runId'], c['runAttempt'], c['workflowCommit']), 'Qualification attempt differs')
    i.require(lock['qualifiedSourceHash'] == record['sourceHash'] == c['sourceHash'] and
              record['engineManifestSha256'] == c['engineManifestSha256'] and record['oci'] == c['oci'],
              'Stale qualification source/engine/OCI')
    i.require(lock['engine'] == candidate.engine(directory / 'engine'), 'Qualified engine bytes differ')
    i.require(type(record['rows']) is list and len(record['rows']) == len(MODES), 'Incomplete mode coverage')
    seen, physical_modes, physical_paths = set(), set(), []
    for row in record['rows']:
        i.fields(row, 'target mode osVersion filesystem backend topology cases evidence binarySha256 manifestSha256 engineImage')
        key = (row['target'], row['mode'])
        i.require(key in MODES and key not in seen, 'Duplicate/inapplicable qualification row')
        seen.add(key)
        mode = row['mode']
        if mode == 'mac-native':
            i.require(row['osVersion'].split('.')[0].isdigit() and int(row['osVersion'].split('.')[0]) >= 26 and
                      row['filesystem'] == 'APFS' and row['backend'] == 'apple-nfs3', 'Unsupported Mac evidence')
        else:
            i.require(row['osVersion'] == '24.04' and row['filesystem'] == 'ext4' and
                      row['backend'] == ('ganesha-native' if mode == 'linux-native' else 'ganesha-docker'),
                      'Unsupported Linux evidence')
        topology = i.fields(row['topology'], 'kind serverHost clientHost serverKernel clientKernel')
        i.require(topology['kind'] in ('physical', 'virtual'), 'Topology must be explicit')
        for name in ('serverHost', 'clientHost', 'serverKernel', 'clientKernel'):
            i.text(topology[name])
        i.require(topology['serverHost'] != topology['clientHost'] and
                  topology['serverKernel'] != topology['clientKernel'], 'Independent host/kernel evidence required')
        i.require(row['cases'] == dict.fromkeys(CASES, 'pass'), 'Missing/failed qualification cases')
        evidence(row['evidence'], root)
        for name in ('binarySha256', 'manifestSha256'):
            i.hex_value(row[name])
        i.require(isinstance(row['engineImage'], str) and row['engineImage'].endswith('@' + c['oci']['index']) and
                  len(row['engineImage'].split('@')) == 2, 'Qualification registry must retain exact OCI digest')
        if topology['kind'] == 'physical':
            physical_modes.add(mode)
            physical_paths.append(row['evidence']['path'])
    i.require(seen == MODES and physical_modes == {'mac-native', 'linux-native', 'linux-docker'},
              'Independent physical Mac/Linux/Docker evidence incomplete')
    i.require(len(physical_paths) == len(set(physical_paths)) and
              sorted(lock['physicalEvidence']) == sorted(physical_paths), 'Physical evidence references differ')
    user = i.fields(record['userVerification'], 'kind candidateRecordSha256 statement checks evidence')
    i.require(user['kind'] == 'executed-user-check' and user['candidateRecordSha256'] == record['candidate']['recordSha256'],
              'Publication consent is not user verification')
    i.text(user['statement'])
    i.require(user['checks'] == dict.fromkeys(i.TARGETS, 'pass'), 'User check must cover exact candidate targets')
    evidence(user['evidence'], root)
    review = i.fields(record['review'], 'candidateCommit sourceHash evidence')
    i.require(review['candidateCommit'] == c['sourceCommit'] and review['sourceHash'] == c['sourceHash'],
              'Candidate-to-final source review differs')
    evidence(review['evidence'], root)
    evidence(record['releaseNotes'], root)
    i.command('git', 'merge-base', '--is-ancestor', c['sourceCommit'], 'HEAD', cwd=root)
    return record
