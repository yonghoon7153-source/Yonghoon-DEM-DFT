"""Build the fixed-height paired dwell block from its commit and the frozen quarter-speed operator block."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile


BASE = '4a56e468c931e024d08f5476df9ccb0237694741'
BLOCK_SHA = '302518e5c287250e782fc5be10fd78657a6ad5cf262c62b44e660cadf9abb4dd'
ARCHIVE_SHA = 'a39fb07fe971a906093d4f658aeec2098aff33157207afd367152206dcaa01f4'
FOLDER = 'docs/reviews/suyoung_speed_ladder_20261123/'
NEW_FILES = ('hold_pair.py', 'run_hold.sh')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(files):
    return ''.join(f'{digest(raw)}  {name}\n' for name, raw in sorted(files.items())).encode('ascii')


def previous_sources(previous_block):
    block = previous_block.read_bytes()
    if digest(block) != BLOCK_SHA:
        raise ValueError('unexpected quarter-speed operator block')
    encoded = block.split(b"<<'QUARTER_SPEED_SOURCES'\n", 1)[1].split(b'\nQUARTER_SPEED_SOURCES\n', 1)[0]
    archive = base64.b64decode(b''.join(encoded.splitlines()), validate=True)
    if digest(archive) != ARCHIVE_SHA:
        raise ValueError('unexpected quarter-speed source archive')
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
[[ $# -eq 6 && ( "$1" == CHECK_ONLY || "$1" == GO_SUYOUNG_FIXED_HEIGHT_ONCE ) ]] || { echo 'Expected CHECK_ONLY or GO_SUYOUNG_FIXED_HEIGHT_ONCE, depth result, half-speed result, material-lid result, wall-balance result, and quarter-speed result.' >&2; exit 2; }
depth=$(realpath -e -- "$2")
prior=$(realpath -e -- "$3")
material=$(realpath -e -- "$4")
baseline=$(realpath -e -- "$5")
quarter=$(realpath -e -- "$6")
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'FIXED_HEIGHT_SOURCES'
"""
    footer = f"""FIXED_HEIGHT_SOURCES
printf '%s  source.tar.gz\\n' '{digest(raw)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash {FOLDER}run_hold.sh "$1" "$depth" "$prior" "$material" "$baseline" "$quarter"
""".encode('ascii')
    block = out / f'PASTE_SUYOUNG_FIXED_HEIGHT_{pin[:12]}_1123.txt'
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
