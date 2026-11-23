"""Build the one-use author block from Git's immutable 8/16 and 12/24 source trees."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile


PREFIX_PIN = "b16bef3f7791b86d31f0197d86b58d9d93d84750"
FULL_PIN = "c0e077ad5961d7be8dd801ea2f527b76089b362a"
PREFIX_MANIFEST = "30c1282abdc3029d9c28d126e384f838d17e7a11710802fe69a09a50d63d57e1"
FULL_MANIFEST = "e179d76257d39c16df2c2acd786bd9bcdf6ced382dbab62467e356dc80558253"
PREFIX_DIR = "docs/reviews/suyoung_floor_contact_20261123/"
FULL_DIR = "docs/reviews/suyoung_floor_full_20261123/"
FINE_DIR = "docs/reviews/suyoung_floor_fine_20261123/"

def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def freeze(files, release, expected=None):
    files["RELEASE"] = (release + "\n").encode("ascii")
    manifest = "".join(sha(blob) + "  " + name + "\n" for name, blob in sorted(files.items())).encode("ascii")
    if expected is not None and sha(manifest) != expected:
        raise ValueError("Historical source manifest differs for " + release)
    files["SOURCE_SHA256SUMS"] = manifest
    return files


def payload(repo, ref):
    git = ["git", "-c", "safe.directory="+repo.as_posix(), "-C", str(repo)]
    release = subprocess.check_output(git+["rev-parse", "--verify", ref+"^{commit}"]).decode().strip()
    subprocess.run(git+["merge-base", "--is-ancestor", FULL_PIN, release], check=True)

    def blobs(pin, paths):
        return {p: subprocess.check_output(git+["show", pin+":"+p]) for p in paths}
    scripts = ["scripts/"+name for name in ("dem_suyoung_sf2d_dev.py", "suyoung_u6_first_dev.py",
                                              "suyoung_multicontact_dev.py", "suyoung_u6b_dev.py")]
    prefix_paths = scripts + ["docs/reviews/suyoung_wall_layers_20261123/matched_controls.py"] + [
        PREFIX_DIR+n for n in ("material_floor.py", "floor_operator.py", "run_floor.sh", "render_weekly.py", "weekly_type.npz")]
    prefix = freeze(blobs(PREFIX_PIN, prefix_paths), PREFIX_PIN, PREFIX_MANIFEST)
    full = {"prefix/"+k: v for k, v in prefix.items()}
    full.update(blobs(FULL_PIN, [FULL_DIR+n for n in ("full_compare.py", "full_floor.py", "run_full.sh")]))
    freeze(full, FULL_PIN, FULL_MANIFEST)
    files = {"old_full/"+k: v for k, v in full.items()}
    files.update(blobs(release, [FINE_DIR+"fine_floor.py", FINE_DIR+"run_fine.sh"]))
    freeze(files, release)
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode="wb", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w") as tar:
            for name, blob in sorted(files.items()):
                member = tarfile.TarInfo(name)
                member.mode = 0o600
                member.size = len(blob)
                tar.addfile(member, io.BytesIO(blob))
    return release, stream.getvalue()


def block(repo, ref):
    release, archive = payload(repo, ref)
    header = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 2 ]]; then
    echo 'Usage: CHECK_ONLY|GO_SUYOUNG_FLOOR_FINE_PAIR_ONCE <completed F8/F16 floor return tar.gz>' >&2
    exit 2
fi
case "$1" in CHECK_ONLY|GO_SUYOUNG_FLOOR_FINE_PAIR_ONCE) ;; *) exit 2 ;; esac
prior=$(realpath -e -- "$2")
[[ -f "$prior" ]]
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'FINE_FLOOR_SOURCES'
"""
    footer = f"""FINE_FLOOR_SOURCES
printf '%s  source.tar.gz\\n' '{sha(archive)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{release}' ]]
exec bash {FINE_DIR}run_fine.sh "$1" "$prior"
"""
    return release, archive, header.encode("ascii") + base64.encodebytes(archive) + footer.encode("ascii")


def save(path, data):
    if path.exists() and path.read_bytes() == data:
        return
    with path.open("xb") as target:
        target.write(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    release, archive, data = block(args.repo.resolve(), args.ref)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"PASTE_SUYOUNG_FLOOR_FINE_PAIR_{release[:12]}_1123.txt"
    save(path, data)
    save(path.with_name(path.name + ".sha256"), (sha(data)+"  "+path.name+"\n").encode("ascii"))
    print(path)
    print("BLOCK_SHA256="+sha(data))
    print("SOURCE_TAR_SHA256="+sha(archive))
