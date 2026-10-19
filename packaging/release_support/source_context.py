"""Git-proven source projections. Frozen files are data, never imported/executed."""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
from pathlib import Path
import subprocess
import tempfile

from . import identity as i

MAX_FILES = 20000
MAX_TOTAL = 512 * 1024**2
MAX_FILE = 64 * 1024**2
SELECTED = i.SOURCES + ('packaging/release-lock.json', 'packaging/releases')


def git(repository, *args, limit=MAX_FILE):
    # Bound captured output without first retaining an arbitrary blob in memory.
    with tempfile.TemporaryFile() as output:
        subprocess.run(['git', '--no-replace-objects', *map(str, args)], cwd=repository,
                       stdout=output, stderr=subprocess.PIPE, check=True, timeout=120)
        i.require(output.tell() <= limit, 'Git input exceeds bound')
        output.seek(0)
        return output.read()


def ancestor(repository, older, newer):
    git(repository, 'merge-base', '--is-ancestor', i.hex_value(older, 40), i.hex_value(newer, 40))


def tree(repository, commit, paths=()):
    i.hex_value(commit, 40)
    i.require(git(repository, 'cat-file', '-t', commit).strip() == b'commit', 'Source is not a Git commit')
    raw = git(repository, 'ls-tree', '-rlz', '--full-tree', commit, '--', *paths)
    result, total = {}, 0
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        header, name = entry.split(b'\t', 1)
        mode, kind, oid, size = header.decode('ascii').split()
        name = name.decode('utf-8')
        i.safe_name(name)
        i.require(mode in ('100644', '100755') and kind == 'blob', 'Non-regular Git input refused')
        size = int(size)
        i.require(0 <= size <= MAX_FILE and name not in result, 'Invalid Git member')
        total += size
        result[name] = (mode, i.hex_value(oid, 40), size)
        i.require(len(result) <= MAX_FILES and total <= MAX_TOTAL, 'Git inventory exceeds bounds')
    return result


def blob_identity(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


@dataclass(frozen=True)
class SourceContext:
    root: Path
    commit: str
    repository: Path

    def blob(self, commit, name):
        i.safe_name(name)
        return git(self.repository, 'show', i.hex_value(commit, 40) + ':' + name)

    def ancestor(self, older):
        ancestor(self.repository, older, self.commit)

    def source_hash(self, engine=None):
        return i.source_hash(engine, self.root)

    def assert_files(self, entries):
        for name, (_, oid, size) in entries.items():
            path = self.root / name
            # Empty tracked files are legal source inputs, not evidence records.
            i.require(not any(p.is_symlink() for p in (path, *path.parents)), 'Linked source input refused')
            i.require(path.is_file() and path.stat().st_size == size and
                      blob_identity(path.read_bytes()) == oid, 'Source differs from Git: ' + name)


def current():
    root = i.ROOT.resolve()
    commit = i.hex_value(git(root, 'rev-parse', 'HEAD').decode().strip(), 40)
    return SourceContext(root, commit, root)


@contextmanager
def frozen(executor, commit):
    ancestor(executor.repository, commit, executor.commit)
    entries = tree(executor.repository, commit, SELECTED)
    for required in i.SOURCES + ('packaging/release-lock.json',):
        i.require(any(name == required or name.startswith(required + '/') for name in entries),
                  'Missing Git source input: ' + required)
    with tempfile.TemporaryDirectory(prefix='nfs-source-') as scratch:
        root = Path(scratch).resolve()
        for name, (_, oid, size) in entries.items():
            data = git(executor.repository, 'cat-file', 'blob', oid)
            i.require(len(data) == size and blob_identity(data) == oid, 'Git blob identity differs')
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(0o400)
        context = SourceContext(root, commit, executor.repository)
        context.assert_files(entries)
        yield context
