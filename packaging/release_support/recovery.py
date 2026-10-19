"""Admission of reviewed executor repairs; no authority creation or remote effects."""
from . import identity as i
from .source_context import ancestor, frozen, tree

REPAIR_PATHS = frozenset({
    'packaging/release.py', i.WORKFLOW,
    *('packaging/release_support/' + name + '.py' for name in
      ('identity', 'source_context', 'recovery', 'candidate', 'readiness', 'payload', 'publication')),
})
GUIDES = frozenset({'RELEASE.md', 'packaging/RELEASE.md', 'TESTING.md', 'README.md'})
TESTS = frozenset('scripts/tests/' + name + '.py' for name in (
    'nfs_release_fixture', 'test_nfs_release_records', 'test_nfs_release_publication',
    'test_nfs_release_workflow', 'test_nfs_source_identity', 'test_nfs_release_recovery', 'test_nfs_packaging'))
TICKET = 'tickets/done/nfs-first-release/'


def scope(repository, older, newer, version, repair):
    before, after = tree(repository, older), tree(repository, newer)
    changed = sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
    for name in changed:
        allowed = (name in GUIDES or name in TESTS or name.startswith(TICKET) or
                   name.startswith('packaging/recovery/' + version + '/'))
        i.require(allowed or (repair and name in REPAIR_PATHS), 'Unreviewed recovery change: ' + name)
    return changed


def admit(executor, source, tag):
    binding = tag['binding']
    version = i.version(binding['version'])
    name = 'packaging/recovery/' + version + '/authorization.json'
    entries = tree(executor.repository, executor.commit, (name,))
    i.require(name in entries, 'Reviewed recovery authorization required')
    executor.assert_files(entries)
    path = i.local_file(executor.root, name, i.JSON_LIMIT)
    record = i.read_json(path)
    i.fields(record, 'schema kind repository version payloadSourceCommit tagObject binding payloadJobId expectedReleaseId executor evidence')
    i.require(type(record['schema']) is int and record['schema'] == 1 and
              record['kind'] == 'same-payload-executor-repair' and record['repository'] == i.REPOSITORY and
              record['version'] == version and record['payloadSourceCommit'] == source.commit == binding['sourceCommit'] and
              record['tagObject'] == tag['object'] and record['binding'] == binding,
              'Recovery authorization does not match immutable payload')
    i.positive(record['payloadJobId'])
    if record['expectedReleaseId'] is not None:
        i.positive(record['expectedReleaseId'])
    reviewed = i.fields(record['executor'], 'reviewedCommit sourceHash')
    h = i.hex_value(reviewed['reviewedCommit'], 40)
    i.hex_value(reviewed['sourceHash'])
    ancestor(executor.repository, source.commit, h)
    ancestor(executor.repository, h, executor.commit)
    scope(executor.repository, source.commit, h, version, True)
    scope(executor.repository, h, executor.commit, version, False)
    with frozen(executor, h) as reviewed_source:
        i.require(executor.source_hash() == reviewed_source.source_hash() == reviewed['sourceHash'],
                  'Executor differs from reviewed production hash')
    evidence = i.fields(record['evidence'], 'architectureReview sourceReview validation retainedSigning deliveryAuthorization')
    for reference in evidence.values():
        i.fields(reference, 'path sha256')
        i.require(reference['path'].startswith('packaging/recovery/' + version + '/'), 'Unstable recovery evidence')
        proof = i.local_file(executor.root, reference['path'], 64 * 1024**2)
        i.require(i.sha(proof) == i.hex_value(reference['sha256']), 'Recovery evidence missing/changed')
        entries = tree(executor.repository, executor.commit, (reference['path'],))
        i.require(reference['path'] in entries, 'Recovery evidence is not committed')
        executor.assert_files(entries)
    return record, {'path': name, 'sha256': i.sha(path)}
