"""Create a standalone WSL operator block from a fixed commit and the pinned four-grid solver."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile

BASE = "206dd6dd00547237fba2ef577098a448263b7736"
HISTORY = "e8e2f2535aa12b9fb089d714e1325d862cb1161b"
PRIOR_BLOCK = "96270f3c4f37980436c23c72b86a238370e2dbcfe0eb3702407bc2b078f7ad3a"
PRIOR_SOURCE = "a6bdf77ce8d0562a141267519f6d747e278f2fc40e12f4ef4d970f5c8eca2c7f"
HERE = "docs/reviews/suyoung_u6a_gates_20261123/"
RULE = "docs/reviews/suyoung_u6_repeat_20261120/repeat_readback.py"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sums(files):
    return "".join(f"{digest(data)}  {name}\n" for name, data in sorted(files.items())).encode("ascii")


def history(block):
    if digest(block) != PRIOR_BLOCK:
        raise ValueError("wrong four-grid operator block")
    marker = b"FINE_FLOOR_SOURCES"
    encoded = block.split(b"<<'" + marker + b"'\n", 1)[1].split(b"\n" + marker + b"\n", 1)[0]
    raw = base64.b64decode(b"".join(encoded.splitlines()), validate=True)
    if digest(raw) != PRIOR_SOURCE:
        raise ValueError("wrong four-grid source")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        files = {item.name: archive.extractfile(item).read() for item in archive if item.isfile()}
    manifest = files.pop("SOURCE_SHA256SUMS")
    if files["RELEASE"].decode().strip() != HISTORY:
        raise ValueError("four-grid release")
    listed = {line.split("  ", 1)[1]: line.split("  ", 1)[0] for line in manifest.decode("ascii").splitlines()}
    if listed != {name: digest(data) for name, data in files.items()}:
        raise ValueError("four-grid source contents")
    files["SOURCE_SHA256SUMS"] = manifest
    return {"history/" + name: data for name, data in files.items()}


def write_once(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(path)
        return
    with path.open("xb") as stream:
        stream.write(data)


def build(repo, previous, out):
    git = ["git", "-c", "safe.directory="+repo.as_posix(), "-C", str(repo)]
    pin = subprocess.check_output([*git, "rev-parse", "--verify", "HEAD^{commit}"]).decode().strip()
    subprocess.run([*git, "merge-base", "--is-ancestor", BASE, pin], check=True)
    files = history(previous.read_bytes())
    names = ["gap_kernel.py", "read_gate.py", "setting2_run.py", "run_setting2.sh", "setting2_registration.md"]
    for name in [RULE, *(HERE + n for n in names)]:
        files[name] = subprocess.check_output([*git, "show", pin+":"+name])
    files["RELEASE"] = (pin+"\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = sums(files)
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=buffer, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w|") as archive:
            for name, data in sorted(files.items()):
                entry = tarfile.TarInfo(name)
                entry.size = len(data)
                archive.addfile(entry, io.BytesIO(data))
    tar = buffer.getvalue()
    header = b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# == 3 ]] || { echo 'Expected mode, original F8/F16 return TAR, original F12/F24 return TAR' >&2; exit 2; }
case "$1" in CHECK_ONLY|GO_SUYOUNG_U6A_SETTING2_ONCE) ;; *) exit 2 ;; esac
full=$(realpath -e -- "$2")
fine=$(realpath -e -- "$3")
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'SETTING2_SOURCES'
"""
    footer = f"""SETTING2_SOURCES
printf '%s  source.tar.gz\\n' '{digest(tar)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash {HERE}run_setting2.sh "$1" "$full" "$fine"
""".encode("ascii")
    out.mkdir(parents=True, exist_ok=True)
    name = f"PASTE_SUYOUNG_U6A_SETTING2_{pin[:12]}_1123.txt"
    data = header + base64.encodebytes(tar) + footer
    write_once(out/name, data)
    write_once(out/(name+".sha256"), sums({name: data}))
    print(name, digest(data), digest(tar))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("repo", "previous_block", "output"):
        p.add_argument(arg, type=Path)
    args = p.parse_args()
    build(args.repo.resolve(), args.previous_block, args.output)
