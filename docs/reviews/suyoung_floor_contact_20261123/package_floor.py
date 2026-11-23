"""Build a self-contained WSL block from committed Git blobs; it runs only on the author's GO."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile
import textwrap

def emit(repo, ref, dest):
    repo = repo.resolve()
    git = ["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo)]
    pin = subprocess.check_output(git + ["rev-parse", "--verify", ref + "^{commit}"]).decode().strip()
    case = "docs/reviews/suyoung_floor_contact_20261123/"
    matched = "docs/reviews/suyoung_wall_layers_20261123/matched_controls.py"
    program_names = ("material_floor.py", "floor_operator.py", "run_floor.sh", "render_weekly.py", "weekly_type.npz")
    native = ("dem_suyoung_sf2d_dev.py", "suyoung_multicontact_dev.py", "suyoung_u6_first_dev.py", "suyoung_u6b_dev.py")

    def blob(refspec, path):
        return subprocess.check_output(git + ["show", refspec + ":" + path])

    items = {case + name: blob(pin, case + name) for name in program_names}
    items[matched] = blob(pin, matched)
    if items[matched] != blob("ebba5037e29de3ca760de7fe3d1a85d43ff3f1e6", matched):
        raise ValueError("matched baseline changed")
    for name in native:
        path = "scripts/" + name
        items[path] = blob(pin, path)
        if items[path] != blob("99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f", path):
            raise ValueError("original physics changed: " + name)
    items["RELEASE"] = (pin + "\n").encode("ascii")
    digest = lambda data: hashlib.sha256(data).hexdigest()
    items["SOURCE_SHA256SUMS"] = "".join(digest(raw) + "  " + name + "\n"
                                          for name, raw in sorted(items.items())).encode("ascii")
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gzipfile, tarfile.open(fileobj=gzipfile, mode="w") as tar:
        for name, raw in sorted(items.items()):
            entry = tarfile.TarInfo(name)
            entry.size = len(raw)
            tar.addfile(entry, io.BytesIO(raw))
    payload = buf.getvalue()
    body = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -lt 1 || $# -gt 2 ]]; then echo 'Usage: CHECK_ONLY|GO_SUYOUNG_FLOOR_PREFIX_ONCE [cross-return.tar.gz]' >&2; exit 2; fi
case "$1" in CHECK_ONLY|GO_SUYOUNG_FLOOR_PREFIX_ONCE) ;; *) exit 2 ;; esac
mode=$1
args=("$mode")
if [[ $# == 2 ]]; then args+=("$(realpath -e -- "$2")"); fi
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'FLOOR_SOURCE_BYTES'
""" + "\n".join(textwrap.wrap(base64.b64encode(payload).decode("ascii"), 76)) + """
FLOOR_SOURCE_BYTES
echo 'PAYLOAD_SHA  source.tar.gz' | sha256sum --check --strict -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == 'RELEASE_SHA' ]]
exec bash docs/reviews/suyoung_floor_contact_20261123/run_floor.sh "${args[@]}"
"""
    body = body.replace("PAYLOAD_SHA", digest(payload)).replace("RELEASE_SHA", pin).encode("ascii")
    name = "PASTE_SUYOUNG_FLOOR_PREFIX_" + pin[:12] + "_1123.txt"
    dest.mkdir(parents=True, exist_ok=True)
    for path, raw in ((dest / name, body), (dest / (name + ".sha256"), (digest(body) + "  " + name + "\n").encode("ascii"))):
        if path.exists():
            if path.read_bytes() != raw:
                raise FileExistsError(path)
        else:
            with path.open("xb") as stream:
                stream.write(raw)
    return dest / name, digest(body), digest(payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    path, digest, payload = emit(args.repo, args.ref, args.out)
    print(path)
    print("BLOCK_SHA256=" + digest)
    print("PAYLOAD_SHA256=" + payload)
