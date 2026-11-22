"""Build an author-only, single F8 ORIGINAL step-145 diagnostic from Git blobs."""
import argparse
import base64
import hashlib
import io
from pathlib import Path
import subprocess
import zipfile


OLD = "001e5e5e5f3bedde8106b608910e95f5dd1f78cb"
FOLDER = "docs/reviews/suyoung_u6c_step145_20261122/"
INPUTS = (
    "scripts/dem_suyoung_sf2d_dev.py", "scripts/suyoung_u6_first_dev.py",
    "scripts/suyoung_u6b_dev.py", "scripts/suyoung_multicontact_dev.py",
    "docs/reviews/suyoung_u6c_friction_candidate_20261122/friction_pair.py",
    "docs/reviews/suyoung_u6c_seed_return_20261122/order_control.py",
    "docs/reviews/suyoung_u6c_wall_return_20261122/dt_control.py",
)
HEAD = r'''#!/usr/bin/env bash
set -eu -o pipefail
umask 077
if [[ $# -ne 2 || ( $1 != CHECK_ONLY && $1 != GO_SUYOUNG_CAPTURE_145_ONCE ) ]]; then
    echo 'Usage: bash THIS.txt CHECK_ONLY|GO_SUYOUNG_CAPTURE_145_ONCE prior_friction_result.tar.gz' >&2
    exit 2
fi
prior=$(realpath -e -- "$2")
pkg=$(mktemp -d "${TMPDIR:-/tmp}/suyoung_capture145_pkg_XXXXXXXX")
cd -- "$pkg"
base64 -d > source.zip <<'CAPTURE_SOURCE'
'''
TAIL = r'''CAPTURE_SOURCE
printf '%s  source.zip\n' '@ZIP@' | sha256sum --check --status -
unzip -q source.zip
sha256sum --check --status SHA256SUMS
printf 'PACKAGE_DIR=%s\n' "$pkg"
exec bash "$pkg/PASTE_INNER.txt" "$1" "$prior"
'''


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sums(files):
    return "".join(f"{sha(data)}  {name}\n" for name, data in sorted(files.items())).encode("ascii")


def write_once(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(path)
    else:
        with path.open("xb") as f:
            f.write(data)


def build(repo, revision, output):
    def git(*args):
        return subprocess.check_output(["git", "-c", "safe.directory=" + repo.as_posix(),
                                        "-C", str(repo), *args])

    pin = git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    files = {}
    for path in INPUTS:
        data = git("cat-file", "blob", f"{pin}:{path}")
        if data != git("cat-file", "blob", f"{OLD}:{path}"):
            raise ValueError("Original replay source differs: " + path)
        files[path] = data
    path = FOLDER + "capture_stop.py"
    files[path] = git("cat-file", "blob", f"{pin}:{path}")
    files["RELEASE"] = (pin + "\n" + OLD + "\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = sums(files)
    template = git("cat-file", "blob", pin + ":" + FOLDER + "capture_wsl.in")
    for token, value in ((b"@PIN@", pin), (b"@SUMS@", sha(files["SOURCE_SHA256SUMS"]))):
        if template.count(token) != 1:
            raise ValueError("Missing or repeated token: " + token.decode())
        template = template.replace(token, value.encode("ascii"))
    files["PASTE_INNER.txt"] = template
    files["SHA256SUMS"] = sums(files)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(path, (2026, 11, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    raw = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip() or len(z.namelist()) != len(files) or any(z.read(k) != v for k, v in files.items()):
            raise ValueError("Source package byte mismatch")
    txt = HEAD.encode("ascii") + base64.encodebytes(raw) + TAIL.replace("@ZIP@", sha(raw)).encode("ascii")
    output.mkdir(parents=True, exist_ok=True)
    for name, data in ((f"PASTE_SUYOUNG_CAPTURE_145_{pin[:12]}_1122.txt", txt),
                       (f"suyoung_capture_145_wsl_{pin[:12]}_20261122.zip", raw)):
        write_once(output/name, data)
        write_once(output/(name + ".sha256"), sums({name:data}))
        print(name, sha(data))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    build(args.repo.resolve(strict=True), args.commit, args.out.resolve())
