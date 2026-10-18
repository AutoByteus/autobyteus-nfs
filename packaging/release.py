#!/usr/bin/env python3
"""NFS release facade. Candidate/readiness/payload/publication have distinct owners."""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_support import candidate, identity as i, payload, publication, readiness
from manifest import embed as embed_engine, validate as validate_engine


def metadata(args):
    lock = i.read_json(i.ROOT / 'packaging/release-lock.json')
    measured = i.read_json(args.engine_manifest) if args.engine_manifest else lock['engine']
    if measured is not None:
        validate_engine(measured)
    if args.source_hash:
        print(i.source_hash(measured))
        return
    if args.check_publish:
        readiness.load()  # Useful default refusal before a candidate is supplied.
        i.require(args.candidate is not None, 'Identified candidate is required')
        readiness.validate(args.candidate)
        return
    i.version(args.tag)
    release = False
    if args.release:
        i.require(args.candidate is not None, 'Release metadata requires identified candidate')
        readiness.validate(args.candidate)
        c = candidate.verify(args.candidate)
        i.require(args.tag == c['version'] and args.engine_image == i.IMAGE + '@' + c['oci']['index'] and
                  measured == candidate.engine(args.candidate / 'engine'), 'Release metadata inputs differ')
        release = True
    if args.candidate is not None:
        c = candidate.verify(args.candidate)
        i.require(args.tag == c['version'] and args.engine_image.endswith('@' + c['oci']['index']) and
                  measured == candidate.engine(args.candidate / 'engine'), 'Candidate metadata inputs differ')
    if measured is None:
        i.require(not args.release and not args.engine_image, 'Release metadata needs measured engine')
        result = {'schema': 2, 'fieldValidation': dict(i.DEFERRED_FIELD_VALIDATION), 'version': args.tag, 'sourceHash': i.source_hash(), 'ubuntuPackages': lock['ubuntuPackages'],
                  'engineImage': '', 'releaseTargets': []}
    else:
        result = candidate.runtime_metadata(args.tag, args.engine_image, measured, release)
    if args.target and args.target.startswith('linux-'):
        i.require(measured is not None and args.engine_artifacts is not None, 'Linux release requires matching engine bundle')
        embed_engine(measured, args.engine_artifacts, args.target.split('-')[1], i.ROOT / 'internal/backend/engine-assets')
    if args.output:
        i.write_json(args.output, result)
    else:
        print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operation', choices=['prepare', 'candidate', 'verify-candidate', 'payload', 'bind', 'publish', 'oci', 'candidate-envelope', 'fetch-candidate'])
    parser.add_argument('--source-hash', action='store_true')
    parser.add_argument('--check-publish', action='store_true')
    parser.add_argument('--tag')
    parser.add_argument('--engine-image', default='')
    parser.add_argument('--engine-manifest', type=Path)
    parser.add_argument('--engine-artifacts', type=Path)
    parser.add_argument('--target', choices=i.TARGETS)
    parser.add_argument('--release', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--directory', type=Path)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--native', type=Path)
    parser.add_argument('--binding', type=Path)
    parser.add_argument('--envelope', type=Path)
    parser.add_argument('--artifact-id', type=int)
    parser.add_argument('--run-id', type=int)
    parser.add_argument('--attempt', type=int)
    parser.add_argument('--source-commit')
    parser.add_argument('--workflow-commit')
    args = parser.parse_args()
    result = None
    if args.operation == 'prepare':
        tag = i.version(args.tag)
        source = i.hex_value(args.source_commit, 40)
        i.require(i.commit() == source and os.environ.get('GITHUB_REPOSITORY') == i.REPOSITORY and
                  os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch', 'Dispatch/source identity differs')
        workflow_commit = i.hex_value(os.environ.get('GITHUB_SHA'), 40)
        i.require(i.command('git', 'show', workflow_commit + ':' + i.WORKFLOW) == (i.ROOT / i.WORKFLOW).read_bytes(),
                  'Dispatch workflow differs from checked-out release source')
        mode = 'candidate'
        if os.environ.get('WANT_PUBLISH') == 'true':
            mode = publication.prepare(tag, source, args.run_id, args.directory)
        lock = i.read_json(i.ROOT / 'packaging/release-lock.json')
        result = {'tag': tag, 'source': source, 'mode': mode, 'base': lock['ubuntuBaseImage']}
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            for name, value in result.items():
                i.text(value)
                output.write(name + '=' + value + '\n')
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as summary:
            summary.write(f'## NFS release inputs\n\nVersion: `{tag}`\n\n'
                          f'Source: `{source}`\n\nWorkflow: `{workflow_commit}`\n\nMode: `{mode}`\n')
    elif args.operation == 'candidate':
        result = candidate.assemble(args.directory, args.tag, args.source_commit,
                                    args.workflow_commit, args.run_id, args.attempt)
    elif args.operation == 'candidate-envelope':
        result = candidate.envelope(args.artifact_id, args.run_id, args.attempt, args.workflow_commit, candidate.CANDIDATE)
    elif args.operation == 'fetch-candidate':
        e = i.read_json(args.envelope)
        candidate.download(e, candidate.CANDIDATE, args.directory)
        c = candidate.verify(args.directory)
        i.require((c['runId'], c['runAttempt'], c['workflowCommit']) ==
                  (e['runId'], e['runAttempt'], e['workflowCommit']), 'Downloaded candidate attempt differs')
        result = {'recordSha256': i.sha(args.directory / 'candidate.json'), 'envelope': e}
    elif args.operation == 'verify-candidate':
        result = candidate.verify(args.directory)
    elif args.operation == 'oci':
        result = candidate.oci(args.directory)
    elif args.operation == 'payload':
        result = payload.assemble(args.directory, args.candidate, args.native, args.source_commit, args.run_id, args.attempt)
    elif args.operation == 'bind':
        result = publication.bind(args.directory, args.candidate, args.artifact_id, args.run_id, args.attempt)
    elif args.operation == 'publish':
        result = publication.publish(args.directory, args.candidate, i.read_json(args.binding), args.output)
    else:
        metadata(args)
    if result is not None:
        if args.output:
            i.write_json(args.output, result)
        else:
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        raise SystemExit('Release refused: ' + str(error))
