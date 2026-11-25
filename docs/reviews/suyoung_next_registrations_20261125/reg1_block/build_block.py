"""Build the WSL operator (one PASTE TXT + its .sha256) for the Suyoung 2D registration 1 (contact mini).

Q13 form: every packaged file is read from one pinned commit (`git show PIN:path`), the pinned
ones are refused unless their sha256 matches the pins (reg1_queue.PINS and the driver's SOURCES),
and the package (tar.gz, sorted members, fixed metadata) travels base64-encoded inside one bash
TXT that checks its own embedded sha256 and RELEASE before running `run.sh`.

    python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/reg1_block/build_block.py REPO PIN OUT

OUT should be outside the repository (the TXT is not committed); it receives
PASTE_SUYOUNG_CONTACT_MINI_<pin12>_1125.txt and PASTE_..._1125.txt.sha256.
"""
import argparse
import ast
import base64
import gzip
import hashlib
import io
from pathlib import Path
import re
import subprocess
import tarfile


BLOCK_DIR = "docs/reviews/suyoung_next_registrations_20261125/reg1_block/"
BLOCK_FILES = ("run.sh", "reg1_queue.py", "reg1_reader.py")
MARK = "CONTACT_MINI_SOURCES"
MODES = ("CHECK_ONLY", "GO_SUYOUNG_CONTACT_MINI_ONCE", "READBACK")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def manifest(files):
    return "".join(f"{sha(data)}  {name}\n" for name, data in sorted(files.items())).encode("ascii")


def literal_assignment(source, name):
    """The literal value assigned to a module-level `name` (no code is executed)."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError("no literal assignment " + name)


def collect(read, pin):
    """Package files from `read(path) -> bytes` of one pinned tree; RELEASE and SOURCE_SHA256SUMS added."""
    queue = read(BLOCK_DIR + "reg1_queue.py")
    pins = literal_assignment(queue, "PINS")
    driver_path = literal_assignment(queue, "DRIVER")
    sources = literal_assignment(read(driver_path), "SOURCES")
    if set(pins) & set(sources):
        raise ValueError("overlapping pins")
    files = {}
    for relative, digest in sorted({**pins, **sources}.items()):
        data = read(relative)
        if sha(data) != digest:
            raise ValueError("pinned file changed: " + relative)
        files[relative] = data
    for name in BLOCK_FILES:
        files[name] = read(BLOCK_DIR + name)
    if not re.fullmatch(r"[0-9a-f]{40}", pin):
        raise ValueError("pin must be a full commit id")
    files["RELEASE"] = (pin + "\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = manifest(files)
    return files


def package(files):
    """Deterministic tar.gz: sorted members, mode 0644, owner 0, time 0."""
    stream = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=stream, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w|", format=tarfile.USTAR_FORMAT) as archive:
            for name, data in sorted(files.items()):
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(data), 0o644, 0
                archive.addfile(info, io.BytesIO(data))
    return stream.getvalue()


def operator(package_bytes, pin):
    head = f"""#!/usr/bin/env bash
# Suyoung 2D registration 1 (contact mini) - DEVELOPMENT_ONLY operator, release {pin}.
# bash THIS CHECK_ONLY | bash THIS GO_SUYOUNG_CONTACT_MINI_ONCE | bash THIS READBACK RETURN_DIRECTORY
set -euo pipefail
umask 077
case "${{1:-}}" in
    CHECK_ONLY|GO_SUYOUNG_CONTACT_MINI_ONCE) [[ $# == 1 ]] || {{ echo 'Expected exactly one mode'; exit 2; }} ;;
    READBACK) [[ $# == 2 ]] || {{ echo 'READBACK expects the return directory'; exit 2; }} ;;
    *) echo 'Expected CHECK_ONLY, GO_SUYOUNG_CONTACT_MINI_ONCE or READBACK'; exit 2 ;;
esac
args=("$1")
if [[ $1 == READBACK ]]; then
    received=$(realpath -e -- "$2")
    args+=("$received")
fi
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'{MARK}'
""".encode("ascii")
    tail = f"""{MARK}
printf '%s  source.tar.gz\\n' '{sha(package_bytes)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash run.sh "${{args[@]}}"
""".encode("ascii")
    return head + base64.encodebytes(package_bytes) + tail


def decode_operator(txt):
    """(package bytes, embedded sha256, release) of an operator TXT."""
    body = txt.split(f"<<'{MARK}'\n".encode(), 1)[1].split(f"\n{MARK}\n".encode(), 1)[0]
    package_bytes = base64.b64decode(b"".join(body.splitlines()), validate=True)
    embedded = re.search(rb"printf '%s  source.tar.gz\\n' '([0-9a-f]{64})'", txt).group(1).decode()
    pin = re.search(rb"\[\[ \$\(cat RELEASE\) == '([0-9a-f]{40})' \]\]", txt).group(1).decode()
    return package_bytes, embedded, pin


def txt_name(pin):
    return f"PASTE_SUYOUNG_CONTACT_MINI_{pin[:12]}_1125.txt"


def build(repo, release, out):
    repo, out = Path(repo).resolve(), Path(out)
    git = ["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo)]
    pin = subprocess.check_output([*git, "rev-parse", "--verify", release + "^{commit}"]).decode().strip()

    def read(path):
        return subprocess.check_output([*git, "show", f"{pin}:{path}"])
    files = collect(read, pin)
    package_bytes = package(files)
    txt = operator(package_bytes, pin)
    name = txt_name(pin)
    out.mkdir(parents=True, exist_ok=True)
    for dest, data in ((out / name, txt), (out / (name + ".sha256"), manifest({name: txt}))):
        if dest.exists() and dest.read_bytes() != data:
            raise FileExistsError(dest)
        if not dest.exists():
            with dest.open("xb") as handle:
                handle.write(data)
    return dict(pin=pin, name=name, txt_sha256=sha(txt), txt_bytes=len(txt), package_sha256=sha(package_bytes),
                package_bytes=len(package_bytes), files=len(files), manifest_sha256=sha(files["SOURCE_SHA256SUMS"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("repo", type=Path)
    parser.add_argument("release")
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    built = build(args.repo, args.release, args.out)
    print(" ".join(f"{k}={v}" for k, v in built.items()))


if __name__ == "__main__":
    main()
