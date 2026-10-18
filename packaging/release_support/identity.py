"""Release values and bounded, content-addressed local inputs. No remote effects."""
import hashlib
import json
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY = 'AutoByteus/autobyteus-nfs'
WORKFLOW = '.github/workflows/release-nfs.yml'
IMAGE = 'ghcr.io/autobyteus/autobyteus-nfs'
TARGETS = ('darwin-amd64', 'darwin-arm64', 'linux-amd64', 'linux-arm64')
GO_VERSION = '1.27.2'
JSON_LIMIT = 4 * 1024 * 1024
ARTIFACT_LIMIT = 8 * 1024**3
SOURCES = ('internal', 'cmd/autobyteus-nfs/main.go', 'go.mod',
           'scripts/public/nfs', 'packaging/Dockerfile', 'packaging/engine',
           'packaging/release.py', 'packaging/release_support', 'packaging/sign-macos.sh',
           WORKFLOW, 'testdata/connection.json', 'docs/filesystem-usage.md',
           'LICENSE', 'THIRD_PARTY_NOTICES')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def version(value):
    require(isinstance(value, str) and re.fullmatch(
        r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', value),
        'A strict normal vMAJOR.MINOR.PATCH release is required')
    return value


def image_reference(value):
    require(isinstance(value, str) and re.fullmatch(r'[a-z0-9][a-z0-9./:_-]*@sha256:[a-f0-9]{64}', value),
            'Engine image must be an immutable registry reference')
    return value


def hex_value(value, size=64):
    require(isinstance(value, str) and re.fullmatch('[a-f0-9]{%d}' % size, value),
            'Invalid hexadecimal identity')
    return value


def positive(value, limit=2**63-1):
    require(type(value) is int and 0 < value <= limit, 'Invalid positive integer/size')
    return value


def text(value):
    require(isinstance(value, str) and 0 < len(value) <= 4096 and
            not any(ord(c) < 32 for c in value), 'Invalid text identity')
    return value


def fields(record, names):
    require(type(record) is dict and set(record) == set(names.split()), 'Unexpected record fields')
    return record


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def decode(data):
    require(len(data) <= JSON_LIMIT, 'JSON input exceeds bound')
    return json.loads(data, object_pairs_hook=unique_pairs,
                      parse_constant=lambda _: require(False, 'Invalid JSON constant'))


def read_json(path):
    regular(path, JSON_LIMIT)
    return decode(path.read_bytes())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def safe_name(name):
    require(isinstance(name, str) and len(name) <= 240 and
            re.fullmatch(r'[A-Za-z0-9_./+~-]+', name) and
            not name.startswith('/') and all(x not in ('', '.', '..') for x in name.split('/')),
            'Unsafe artifact/evidence path')
    return PurePosixPath(name)


def regular(path, limit=ARTIFACT_LIMIT):
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and 0 < info.st_size <= limit,
            'Expected bounded regular file: ' + str(path))
    return path


def local_file(root, name, limit=ARTIFACT_LIMIT):
    relative = safe_name(name)
    path = root
    for part in relative.parts:
        path = path / part
        require(not path.is_symlink(), 'Linked input refused')
    require(path.resolve().is_relative_to(root.resolve()), 'Input escapes root')
    return regular(path, limit)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def file_record(path):
    regular(path)
    return {'size': path.stat().st_size, 'sha256': sha(path)}


def inventory(directory, exclude=()):
    result = {}
    for path in sorted(directory.rglob('*')):
        require(not path.is_symlink(), 'Linked artifact member refused')
        if path.is_dir():
            continue
        name = path.relative_to(directory).as_posix()
        safe_name(name)
        if name not in exclude:
            result[name] = file_record(path)
    require(0 < len(result) <= 4096 and sum(x['size'] for x in result.values()) <= ARTIFACT_LIMIT,
            'Artifact count/size bound exceeded')
    return result


def verify_inventory(directory, expected, exclude=()):
    require(type(expected) is dict and 0 < len(expected) <= 4096, 'Invalid member inventory')
    for name, record in expected.items():
        safe_name(name)
        fields(record, 'size sha256')
        positive(record['size'], ARTIFACT_LIMIT)
        hex_value(record['sha256'])
    require(inventory(directory, exclude) == expected, 'Artifact member identity/set differs')


def source_hash(engine=None, root=None):
    root = root or ROOT
    lock = read_json(root / 'packaging/release-lock.json')
    inputs = {key: lock[key] for key in ('ubuntuBaseImage', 'ubuntuPackages', 'engine')}
    if engine is not None:
        inputs['engine'] = engine
    digest = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode())
    files = []
    for name in SOURCES:
        path = root / name
        files.extend(p for p in path.rglob('*') if p.is_file()) if path.is_dir() else files.append(path)
    for path in sorted(files):
        if path.name.endswith('_test.go') or '__tests__' in path.parts or '__pycache__' in path.parts or path.suffix == '.deb':
            continue
        regular(path)
        digest.update(path.relative_to(root).as_posix().encode() + b'\0' + path.read_bytes())
    return digest.hexdigest()


def command(*args, cwd=ROOT, input=None):
    return subprocess.run([str(x) for x in args], cwd=cwd, input=input, check=True,
                          capture_output=True, timeout=1800).stdout


def commit():
    return hex_value(command('git', 'rev-parse', 'HEAD').decode().strip(), 40)


def archive_name(tag, target):
    version(tag)
    require(target in TARGETS, 'Unsupported release target')
    return f'autobyteus-nfs-{tag[1:]}-{target}.tar.gz'
