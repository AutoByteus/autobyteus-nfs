"""Complete final signed payload. Separate from remote publication/reconciliation."""
import hashlib
import shutil
import re
import tarfile

from . import candidate, identity as i, readiness
from .source_context import current


def binary_hash(archive):
    digest = hashlib.sha256()
    with tarfile.open(archive, 'r:gz') as tar:
        with tar.extractfile('autobyteus-nfs') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
    return digest.hexdigest()


def signing_proof(proof, archive):
    i.fields(proof, 'status submissionId teamId binarySha256')
    i.require(proof['status'] == 'Accepted', 'Mac notarization was not Accepted')
    i.require(re.fullmatch(r'[a-fA-F0-9-]{36}', proof['submissionId']) and
              re.fullmatch(r'[A-Z0-9]{10}', proof['teamId']), 'Missing notarization identity')
    i.require(proof['binarySha256'] == binary_hash(archive), 'Signed binary identity differs')


def assemble(directory, candidate_dir, native_dir, source_commit, run_id, attempt):
    q = readiness.validate(candidate_dir)
    c = candidate.verify(candidate_dir)
    i.require(i.commit() == source_commit, 'Final source commit differs')
    i.require(not directory.exists(), 'Payload destination must be new')
    assets = directory / 'assets'
    assets.mkdir(parents=True)
    measured = candidate.engine(candidate_dir / 'engine')
    metadata = candidate.runtime_metadata(c['version'], i.IMAGE + '@' + c['oci']['index'], measured, True)
    signatures = {}
    for target in i.TARGETS:
        name = i.archive_name(c['version'], target)
        archive = i.local_file(native_dir, name)
        candidate.native_archive(archive, metadata)
        if target.startswith('darwin'):
            proof = i.read_json(native_dir / (target + '-notary.json'))
            signing_proof(proof, archive)
            signatures[target] = proof
        shutil.copyfile(archive, assets / name)
    installer = (i.ROOT / 'scripts/public/nfs/install.sh').read_text().replace('__RELEASE_TAG__', c['version'])
    (assets / 'autobyteus-nfs-install.sh').write_text(installer)
    i.write_json(assets / 'autobyteus-nfs-manifest.json', metadata)
    shutil.copyfile(candidate_dir / 'engine/engine-manifest.json', assets / 'autobyteus-nfs-engine-manifest.json')
    for arch, bundle in measured['architectures'].items():
        for item in (bundle['correspondingSource'], bundle['buildInventory']):
            shutil.copyfile(candidate_dir / 'engine' / arch / item['file'], assets / item['file'])
        shutil.copyfile(candidate_dir / 'engine' / arch / 'COPYRIGHT', assets / ('engine-COPYRIGHT-' + arch))
    for name in ('LICENSE', 'THIRD_PARTY_NOTICES'):
        shutil.copyfile(i.ROOT / name, assets / name)
    (assets / 'release-notes.md').write_text(readiness.release_notes(q))
    provenance = {'schema': 2, 'repository': i.REPOSITORY, 'version': c['version'],
                  'sourceCommit': source_commit, 'candidate': q['candidate'],
                  'candidateCommit': c['sourceCommit'], 'sourceHash': c['sourceHash'], 'oci': c['oci'],
                  'releaseReadiness': i.read_json(i.ROOT / 'packaging/release-lock.json')['releaseReadiness'],
                  'fieldValidation': q['fieldValidation'],
                  'signing': signatures, 'members': i.inventory(assets)}
    i.write_json(assets / 'release-provenance.json', provenance)
    checksums = ''.join(value['sha256'] + '  ' + name + '\n' for name, value in i.inventory(assets).items())
    (assets / 'SHA256SUMS-nfs').write_text(checksums)
    receipt = {'schema': 1, 'repository': i.REPOSITORY, 'workflow': i.WORKFLOW,
               'sourceCommit': source_commit, 'version': c['version'],
               'runId': i.positive(run_id), 'runAttempt': i.positive(attempt),
               'candidateRecordSha256': q['candidate']['recordSha256'], 'members': i.inventory(directory)}
    i.write_json(directory / 'publication.json', receipt)
    return verify(directory, candidate_dir)


def verify(directory, candidate_dir, context=None):
    context = context or current()
    q = readiness.validate(candidate_dir, context)
    c = candidate.verify(candidate_dir, context)
    receipt = i.read_json(directory / 'publication.json')
    i.fields(receipt, 'schema repository workflow sourceCommit version runId runAttempt candidateRecordSha256 members')
    i.require(receipt['schema'] == 1 and receipt['repository'] == i.REPOSITORY and receipt['workflow'] == i.WORKFLOW,
              'Foreign publication payload')
    i.require(receipt['sourceCommit'] == context.commit and receipt['version'] == c['version'] and
              receipt['candidateRecordSha256'] == q['candidate']['recordSha256'], 'Publication inputs differ')
    i.positive(receipt['runId'])
    i.positive(receipt['runAttempt'])
    i.verify_inventory(directory, receipt['members'], ('publication.json',))
    assets = directory / 'assets'
    i.require(all(name.startswith('assets/') and name.count('/') == 1 for name in receipt['members']),
              'Unexpected payload path')
    provenance = i.read_json(assets / 'release-provenance.json')
    i.fields(provenance, 'schema repository version sourceCommit candidate candidateCommit sourceHash oci releaseReadiness fieldValidation signing members')
    i.require(provenance['schema'] == 2 and provenance['repository'] == i.REPOSITORY and
              provenance['version'] == c['version'] and provenance['sourceCommit'] == receipt['sourceCommit'] and
              provenance['candidate'] == q['candidate'] and provenance['candidateCommit'] == c['sourceCommit'] and
              provenance['sourceHash'] == c['sourceHash'] and provenance['oci'] == c['oci'] and
              provenance['releaseReadiness'] == i.read_json(context.root / 'packaging/release-lock.json')['releaseReadiness'] and
              provenance['fieldValidation'] == q['fieldValidation'],
              'Provenance differs')
    i.verify_inventory(assets, provenance['members'], ('release-provenance.json', 'SHA256SUMS-nfs'))
    checksums = ''.join(value['sha256'] + '  ' + name + '\n'
                        for name, value in i.inventory(assets, ('SHA256SUMS-nfs',)).items())
    i.require((assets / 'SHA256SUMS-nfs').read_text() == checksums, 'Incomplete payload checksums')
    measured = candidate.engine(candidate_dir / 'engine')
    metadata = candidate.runtime_metadata(c['version'], i.IMAGE + '@' + c['oci']['index'], measured, True, context)
    i.require(i.read_json(assets / 'autobyteus-nfs-manifest.json') == metadata and
              i.read_json(assets / 'autobyteus-nfs-engine-manifest.json') == measured, 'Final manifests differ')
    i.require(set(provenance['signing']) == {'darwin-amd64', 'darwin-arm64'}, 'Missing Mac signing proofs')
    expected_names = {'autobyteus-nfs-install.sh', 'autobyteus-nfs-manifest.json',
                      'autobyteus-nfs-engine-manifest.json', 'LICENSE', 'THIRD_PARTY_NOTICES', 'release-notes.md'}
    expected_names.update(i.archive_name(c['version'], target) for target in i.TARGETS)
    for arch, bundle in measured['architectures'].items():
        for item in (bundle['correspondingSource'], bundle['buildInventory']):
            expected_names.add(item['file'])
            i.require(i.file_record(assets / item['file']) == {k: item[k] for k in ('size', 'sha256')},
                      'Corresponding source/inventory differs')
        name = 'engine-COPYRIGHT-' + arch
        expected_names.add(name)
        i.require((assets / name).read_bytes() == (candidate_dir / 'engine' / arch / 'COPYRIGHT').read_bytes(),
                  'Engine notices differ')
    i.require(set(provenance['members']) == expected_names, 'Incomplete release payload')
    for name in ('LICENSE', 'THIRD_PARTY_NOTICES'):
        i.require((assets / name).read_bytes() == (context.root / name).read_bytes(), 'Release license/notices differ')
    i.require((assets / 'release-notes.md').read_text() == readiness.release_notes(q, context),
              'Unreviewed release notes')
    i.require((assets / 'autobyteus-nfs-install.sh').read_text() ==
              (context.root / 'scripts/public/nfs/install.sh').read_text().replace('__RELEASE_TAG__', c['version']),
              'Versioned installer differs')
    for target in i.TARGETS:
        archive = assets / i.archive_name(c['version'], target)
        candidate.native_archive(archive, metadata, context)
        if target.startswith('darwin'):
            signing_proof(provenance['signing'][target], archive)
    return receipt
