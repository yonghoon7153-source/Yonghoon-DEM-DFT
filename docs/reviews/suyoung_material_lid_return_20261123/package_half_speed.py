"""Build the half-speed operator block from committed sources and the pinned material-lid block."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile


BASE = '35099db02148c1a5dc2581f880e0adbf28c0368d'
BLOCK_SHA = '60405324f8134c1a60e451df5b91cdf4ca18f7728a2e5a3b470ca24a6de43e85'
ARCHIVE_SHA = 'cfb8483f0b5984f1f5fe4e76b2d2375809f9d6b6979652c8a564c2f654bfc8ed'
FOLDER = 'docs/reviews/suyoung_material_lid_return_20261123/'
NEW_FILES = ('half_speed.py', 'run_half_speed.sh')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(files):
    return ''.join(f'{digest(raw)}  {name}\n' for name, raw in sorted(files.items())).encode('ascii')


def previous_sources(previous_block):
    block = previous_block.read_bytes()
    if digest(block) != BLOCK_SHA:
        raise ValueError('unexpected material-lid operator block')
    encoded = block.split(b"<<'MATERIAL_LID_SOURCES'\n", 1)[1].split(b'\nMATERIAL_LID_SOURCES\n', 1)[0]
    archive = base64.b64decode(b''.join(encoded.splitlines()), validate=True)
    if digest(archive) != ARCHIVE_SHA:
        raise ValueError('unexpected material-lid source archive')
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as reader:
        files = {member.name: reader.extractfile(member).read() for member in reader if member.isfile()}
    previous_manifest = files.pop('SOURCE_SHA256SUMS')
    if manifest(files) != previous_manifest or files['RELEASE'] != (BASE + '\n').encode('ascii'):
        raise ValueError('previous source manifest or release mismatch')
    files['SOURCE_SHA256SUMS'] = previous_manifest
    return {'history/' + name: raw for name, raw in files.items()}


def sources(repo, previous_block, ref):
    files = previous_sources(previous_block)
    git = ['git', '-c', 'safe.directory=' + repo.as_posix(), '-C', str(repo)]
    pin = subprocess.check_output(git + ['rev-parse', '--verify', ref + '^{commit}']).decode('ascii').strip()
    subprocess.run(git + ['merge-base', '--is-ancestor', BASE, pin], check=True)
    for name in NEW_FILES:
        path = FOLDER + name
        files[path] = subprocess.check_output(git + ['show', pin + ':' + path])
    files['RELEASE'] = (pin + '\n').encode('ascii')
    files['SOURCE_SHA256SUMS'] = manifest(files)
    buf = io.BytesIO()
    with gzip.GzipFile(filename='', fileobj=buf, mode='wb', mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w|') as archive:
            for name, raw in sorted(files.items()):
                member = tarfile.TarInfo(name)
                member.size = len(raw)
                archive.addfile(member, io.BytesIO(raw))
    return pin, buf.getvalue()


def build(repo, previous_block, out, ref='HEAD'):
    pin, raw = sources(repo.resolve(), previous_block, ref)
    header = b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# -eq 3 && ( "$1" == CHECK_ONLY || "$1" == GO_SUYOUNG_HALF_SPEED_ONCE ) ]] || { echo 'Expected CHECK_ONLY or GO_SUYOUNG_HALF_SPEED_ONCE, material-lid result.tar.gz, and wall-balance result.tar.gz.' >&2; exit 2; }
prior=$(realpath -e -- "$2")
baseline=$(realpath -e -- "$3")
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'HALF_SPEED_SOURCES'
"""
    footer = f"""HALF_SPEED_SOURCES
printf '%s  source.tar.gz\\n' '{digest(raw)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash {FOLDER}run_half_speed.sh "$1" "$prior" "$baseline"
""".encode('ascii')
    block = out / f'PASTE_SUYOUNG_HALF_SPEED_{pin[:12]}_1123.txt'
    data = header + base64.encodebytes(raw) + footer
    sidecar = block.with_suffix('.txt.sha256')
    outputs = {block: data, sidecar: f'{digest(data)}  {block.name}\n'.encode('ascii')}
    out.mkdir(parents=True, exist_ok=True)
    for path, contents in outputs.items():
        if path.exists() and path.read_bytes() != contents:
            raise FileExistsError(f'different file already exists: {path}')
    for path, contents in outputs.items():
        if not path.exists():
            with path.open('xb') as stream:
                stream.write(contents)
    return block, digest(data), digest(raw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('repo', 'previous_block', 'out'):
        parser.add_argument(arg, type=Path)
    parser.add_argument('--ref', default='HEAD')
    args = parser.parse_args()
    block, block_hash, archive_hash = build(args.repo, args.previous_block, args.out, args.ref)
    print(block.name, block_hash, archive_hash)
