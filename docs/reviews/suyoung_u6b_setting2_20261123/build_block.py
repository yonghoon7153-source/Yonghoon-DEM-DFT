"""Build a single-file WSL operator at an immutable commit, reusing the exact U6(a) sources."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path, PurePosixPath
import subprocess
import tarfile


HERE = "docs/reviews/suyoung_u6b_setting2_20261123/"
GATE_PIN = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"
BLOCK_HASH = "1b5a76a30c55e9fd45ec6b7a1ed6a708891b8abc11aa488abef788c363f19ed7"
SOURCE_HASH = "db385a40dcb12c8a17046af810bcf948b0e2436c4561d98bcba9378ed2a6545e"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(files):
    return "".join(f"{sha(raw)}  {name}\n" for name, raw in sorted(files.items())).encode("ascii")


def gate_sources(block):
    if sha(block) != BLOCK_HASH:
        raise ValueError("U6(a) operator hash")
    payload = block.split(b"<<'SETTING2_SOURCES'\n", 1)[1].split(b"\nSETTING2_SOURCES\n", 1)[0]
    raw = base64.b64decode(b"".join(payload.splitlines()), validate=True)
    if sha(raw) != SOURCE_HASH:
        raise ValueError("U6(a) embedded source hash")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        files = {}
        for item in tar:
            p = PurePosixPath(item.name)
            if (not item.isfile() or item.name in files or p.is_absolute()
                    or str(p) != item.name or ".." in p.parts):
                raise ValueError("invalid source entry")
            files[item.name] = tar.extractfile(item).read()
    old_manifest = files.pop("SOURCE_SHA256SUMS")
    if files["RELEASE"].decode().strip() != GATE_PIN or old_manifest != manifest(files):
        raise ValueError("U6(a) source identity")
    files["SOURCE_SHA256SUMS"] = old_manifest
    return {"history/" + k: v for k, v in files.items()}


def build(repo, pin, previous, out):
    git = ["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo)]
    full_pin = subprocess.check_output([*git, "rev-parse", "--verify", pin + "^{commit}"]).decode().strip()
    subprocess.run([*git, "merge-base", "--is-ancestor", GATE_PIN, full_pin], check=True)
    files = gate_sources(previous.read_bytes())
    for name in ("run_u6b.sh", "setting2_u6b.py"):
        files[HERE + name] = subprocess.check_output([*git, "show", full_pin + ":" + HERE + name])
    files["RELEASE"] = (full_pin + "\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = manifest(files)
    data = io.BytesIO()
    with gzip.GzipFile(fileobj=data, mode="wb", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w|") as archive:
            for name, content in sorted(files.items()):
                item = tarfile.TarInfo(name)
                item.size = len(content)
                archive.addfile(item, io.BytesIO(content))
    archive = data.getvalue()
    header = b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# == 2 ]] || { echo 'Expected mode and setting-2 U6(a) return TAR' >&2; exit 2; }
case "$1" in CHECK_ONLY|GO_SUYOUNG_U6B_SETTING2_ONCE) ;; *) exit 2 ;; esac
gate=$(realpath -e -- "$2")
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'U6B_SOURCES'
"""
    footer = f"""U6B_SOURCES
printf '%s  source.tar.gz\\n' '{sha(archive)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{full_pin}' ]]
exec bash {HERE}run_u6b.sh "$1" "$gate"
""".encode("ascii")
    block = header + base64.encodebytes(archive) + footer
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"PASTE_SUYOUNG_U6B_SETTING2_{full_pin[:12]}_1123.txt"
    for target, raw in ((path, block), (path.with_suffix(".txt.sha256"), manifest({path.name: block}))):
        if target.exists():
            if target.read_bytes() != raw:
                raise FileExistsError(target)
        else:
            with target.open("xb") as stream:
                stream.write(raw)
    print(path.name, sha(block), sha(archive))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("pin")
    p.add_argument("previous_block", type=Path)
    p.add_argument("output_directory", type=Path)
    args = p.parse_args()
    build(args.repo.resolve(), args.pin, args.previous_block, args.output_directory)
