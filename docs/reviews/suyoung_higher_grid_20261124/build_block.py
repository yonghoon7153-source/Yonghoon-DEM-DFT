"""Package the original setting-2 operator and its registered force reader for WSL."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile

PHYSICS = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"
BLOCK = "1b5a76a30c55e9fd45ec6b7a1ed6a708891b8abc11aa488abef788c363f19ed7"
MANIFEST = "7d698c085e250be40fd7d2bfdad7ae84233ddaa847bed4939d69d0ac343834b3"
HERE = "docs/reviews/suyoung_higher_grid_20261124/"
RULES = {
    "suyoung_u6c_force_rule_20261122/force_rule.py": "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db",
    "suyoung_u6c_force_rule_20261122/rule.json": "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4",
    "suyoung_u6c_doubling_readback_20261122/doubling.py": "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def manifest(files):
    return "".join(f"{sha(data)}  {name}\n" for name, data in sorted(files.items())).encode("ascii")


def original(path):
    block = path.read_bytes()
    if sha(block) != BLOCK:
        raise ValueError("wrong original operator")
    encoded = block.split(b"<<'SETTING2_SOURCES'\n", 1)[1].split(b"\nSETTING2_SOURCES\n", 1)[0]
    raw = base64.b64decode(b"".join(encoded.splitlines()), validate=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        files = {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}
    checks = files.pop("SOURCE_SHA256SUMS")
    if sha(checks) != MANIFEST or checks != manifest(files) or files["RELEASE"].decode().strip() != PHYSICS:
        raise ValueError("incorrect original source package")
    files["SOURCE_SHA256SUMS"] = checks
    return {"baseline/" + name: data for name, data in files.items()}


def build(repo, release, previous, output):
    git = ["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo)]
    pin = subprocess.check_output([*git, "rev-parse", "--verify", release+"^{commit}"]).decode().strip()
    files = original(previous)
    for path, digest in RULES.items():
        raw = subprocess.check_output([*git, "show", PHYSICS+":docs/reviews/"+path])
        if sha(raw) != digest:
            raise ValueError("incorrect registered reader " + path)
        files["rule/"+path] = raw
    for name in ("higher.py", "registration.md", "run.sh"):
        files[name] = subprocess.check_output([*git, "show", pin+":"+HERE+name])
    files["RELEASE"] = (pin+"\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = manifest(files)
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, filename="", mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w|") as tar:
            for name, data in sorted(files.items()):
                entry = tarfile.TarInfo(name)
                entry.size = len(data)
                tar.addfile(entry, io.BytesIO(data))
    raw = stream.getvalue()
    start = b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# == 2 ]] || { echo 'Expected mode and original setting-2 result TAR' >&2; exit 2; }
case "$1" in CHECK_ONLY|GO_SUYOUNG_F32_F48_ONCE) ;; *) exit 2 ;; esac
prior=$(realpath -e -- "$2")
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'HIGHER_SOURCE'
"""
    end = f"""HIGHER_SOURCE
printf '%s  source.tar.gz\\n' '{sha(raw)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash run.sh "$1" "$prior"
""".encode("ascii")
    operator = start + base64.encodebytes(raw) + end
    name = f"PASTE_SUYOUNG_F32_F48_{pin[:12]}_1124.txt"
    output.mkdir(parents=True, exist_ok=True)
    for dest, data in ((output/name, operator), (output/(name+".sha256"), manifest({name: operator}))):
        if dest.exists() and dest.read_bytes() == data:
            continue
        with dest.open("xb") as handle:
            handle.write(data)
    print(name, "operator_sha256="+sha(operator), "tar_sha256="+sha(raw))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("release")
    parser.add_argument("previous_block", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.repo.resolve(), args.release, args.previous_block, args.output)
