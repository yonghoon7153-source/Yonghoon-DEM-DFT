"""Generate one portable author block with an immutable native floor source package."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import re
import subprocess
import tarfile


PREFIX_RELEASE = "b16bef3f7791b86d31f0197d86b58d9d93d84750"
PREFIX_MANIFEST = "30c1282abdc3029d9c28d126e384f838d17e7a11710802fe69a09a50d63d57e1"
OLD_CASE = "docs/reviews/suyoung_floor_contact_20261123/"
FULL_CASE = "docs/reviews/suyoung_floor_full_20261123/"
OLD_PATHS = (
    "docs/reviews/suyoung_wall_layers_20261123/matched_controls.py",
    "scripts/dem_suyoung_sf2d_dev.py",
    "scripts/suyoung_multicontact_dev.py",
    "scripts/suyoung_u6_first_dev.py",
    "scripts/suyoung_u6b_dev.py",
    *(OLD_CASE + name for name in ("material_floor.py", "floor_operator.py", "run_floor.sh",
                                   "render_weekly.py", "weekly_type.npz")),
)
NEW_PATHS = tuple(FULL_CASE + name for name in ("full_compare.py", "full_floor.py", "run_full.sh"))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(files):
    return "".join(f"{digest(raw)}  {name}\n" for name, raw in sorted(files.items())).encode("ascii")


def make_block(repo, ref):
    git = ["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo)]
    release = subprocess.check_output(git + ["rev-parse", "--verify", ref+"^{commit}"]).decode().strip()
    if not re.fullmatch("[0-9a-f]{40}", release):
        raise ValueError("invalid release identity")
    subprocess.run(git + ["merge-base", "--is-ancestor", PREFIX_RELEASE, release], check=True)

    def read(pin, path):
        return subprocess.check_output(git + ["show", pin+":"+path])

    prior = {path: read(PREFIX_RELEASE, path) for path in OLD_PATHS}
    prior["RELEASE"] = (PREFIX_RELEASE+"\n").encode("ascii")
    prior["SOURCE_SHA256SUMS"] = manifest(prior)
    if digest(prior["SOURCE_SHA256SUMS"]) != PREFIX_MANIFEST:
        raise ValueError("prior execution package does not match the reported prefix manifest")
    files = {"prefix/"+path: value for path, value in prior.items()}
    files.update({path: read(release, path) for path in NEW_PATHS})
    files["RELEASE"] = (release+"\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = manifest(files)
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode="wb", mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode="w") as tar:
            for path, raw in sorted(files.items()):
                member = tarfile.TarInfo(path)
                member.size = len(raw)
                member.mode = 0o600
                tar.addfile(member, io.BytesIO(raw))
    body = stream.getvalue()
    header = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 2 ]]; then
    echo 'Usage: CHECK_ONLY|GO_SUYOUNG_FLOOR_FULL_PAIR_ONCE <completed floor-prefix result.tar.gz>' >&2
    exit 2
fi
case "$1" in CHECK_ONLY|GO_SUYOUNG_FLOOR_FULL_PAIR_ONCE) ;; *) exit 2 ;; esac
prior=$(realpath -e -- "$2")
[[ -f "$prior" ]]
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'FULL_FLOOR_SOURCES'
"""
    footer = """FULL_FLOOR_SOURCES
printf '%s  source.tar.gz\n' __TAR__ | sha256sum --check --strict -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == __RELEASE__ ]]
exec bash docs/reviews/suyoung_floor_full_20261123/run_full.sh "$1" "$prior"
"""
    # RFC 2045 lines keep the self-contained text portable via both Git and file transfer.
    block = header.encode("ascii") + base64.encodebytes(body) + footer.replace("__TAR__", digest(body)).replace("__RELEASE__", release).encode("ascii")
    return release, body, block


def save(path, content):
    if path.exists():
        if path.read_bytes() != content:
            raise FileExistsError(path)
        return
    with path.open("xb") as stream:
        stream.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    release, archive, block = make_block(args.repo.resolve(), args.ref)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"PASTE_SUYOUNG_FLOOR_FULL_PAIR_{release[:12]}_1123.txt"
    save(path, block)
    save(path.with_name(path.name+".sha256"), f"{digest(block)}  {path.name}\n".encode("ascii"))
    print(path)
    print("BLOCK_SHA256="+digest(block))
    print("SOURCE_TAR_SHA256="+digest(archive))
