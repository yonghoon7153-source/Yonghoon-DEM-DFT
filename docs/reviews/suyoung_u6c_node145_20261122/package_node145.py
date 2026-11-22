"""Build the U6(c) two-arm F8 friction control author TXT from committed blobs. No solver entry points."""
import argparse
import base64
import hashlib
import io
from pathlib import Path
import subprocess
import textwrap
import zipfile


PRIOR_PIN = "6bdfac91520c868b5036071e6d60464972727f49"
HIST_PAIR = 'docs/reviews/suyoung_u6c_friction_candidate_20261122/friction_pair.py'
PAIR_PIN = '001e5e5e5f3bedde8106b608910e95f5dd1f78cb'
CAPTURE = 'docs/reviews/suyoung_u6c_step145_20261122/capture_stop.py'
CAPTURE_PIN = 'f24cce28be28aece96d18cf77173d8fe05a2bfb0'
FOLDER = "docs/reviews/suyoung_u6c_node145_20261122/"
BASE_SOURCES = ("scripts/suyoung_u6b_dev.py", "scripts/suyoung_u6_first_dev.py",
                "scripts/dem_suyoung_sf2d_dev.py")
DT_LIBRARY = "docs/reviews/suyoung_u6c_wall_return_20261122/dt_control.py"
DT_PIN = "c36516a26d4a66f3db71c70de31b75802cb4bdb7"
ORDER_LIBRARY = "docs/reviews/suyoung_u6c_seed_return_20261122/order_control.py"
ORDER_PIN = "c3c9ae92655ad39508ea6dd52efac8b71e5001b8"
TOOLS = ("scripts/suyoung_multicontact_dev.py", FOLDER+"node145_pair.py", HIST_PAIR, CAPTURE, ORDER_LIBRARY, DT_LIBRARY)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sums(by_name):
    return "".join(sha(data) + "  " + name + "\n" for name, data in sorted(by_name.items())).encode("ascii")


def git(repo, *args):
    return subprocess.run(["git","-c","safe.directory=" + repo.as_posix(),"-C",str(repo),*args],
                          check=True,stdout=subprocess.PIPE).stdout


def write_checked(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(path)
    else:
        with path.open("xb") as out:
            out.write(data)


HEAD = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 4 || ( $1 != CHECK_ONLY && $1 != GO_SUYOUNG_F8_NODE145_PAIR_ONCE ) ]]; then
    echo 'Usage: bash THIS.txt CHECK_ONLY|GO_SUYOUNG_F8_NODE145_PAIR_ONCE wall_result.tar.gz order_result.tar.gz capture145_result.tar.gz' >&2
    exit 2
fi

wall=$(realpath -e -- "$2")
order=$(realpath -e -- "$3")
capture=$(realpath -e -- "$4")
package=$(mktemp -d "${TMPDIR:-/tmp}/suyoung_node145_pkg_XXXXXXXX")
cd -- "$package"
base64 -d > source.zip <<'ORDER_PACKAGE'
"""
TAIL = """
ORDER_PACKAGE
printf '%s  source.zip\\n' '@ZIP_SHA@' | sha256sum --check --status -
unzip -q source.zip
sha256sum --check --status SHA256SUMS
printf 'RELEASE=@PIN@\\nPACKAGE_DIR=%s\\n' "$package"
bash "$package/PASTE_INNER.txt" "$1" "$wall" "$order" "$capture"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    pin = git(repo, "rev-parse", "--verify", "--end-of-options", args.commit+"^{commit}").decode().strip()
    def blob(path, commit=pin):
        return git(repo, "cat-file", "blob", commit+":"+path)
    contents = {name:blob(name) for name in (*BASE_SOURCES, *TOOLS)}
    for name in BASE_SOURCES:
        if contents[name] != blob(name, PRIOR_PIN):
            raise ValueError("Historical source differs: "+name)

    if contents[DT_LIBRARY] != blob(DT_LIBRARY, DT_PIN):
        raise ValueError("Historical half-step readback library differs")
    if contents[ORDER_LIBRARY] != blob(ORDER_LIBRARY, ORDER_PIN):
        raise ValueError("Historical order adapter differs")
    for name, expected in ((HIST_PAIR, PAIR_PIN), (CAPTURE, CAPTURE_PIN)):
        if contents[name] != blob(name, expected):
            raise ValueError("Frozen dependency differs: "+name)
    kernel = "scripts/suyoung_multicontact_dev.py"
    if contents[kernel] == blob(kernel, PAIR_PIN):
        raise ValueError("Candidate kernel equals historical failed source")
    contents["RELEASE"] = (pin+"\n"+PRIOR_PIN+"\n"+DT_PIN+"\n"+ORDER_PIN+"\n"+PAIR_PIN+"\n"+CAPTURE_PIN+"\n").encode("ascii")
    contents["SOURCE_SHA256SUMS"] = sums(contents)
    template = blob(FOLDER + "run_wsl.in")
    if template.count(b"@PIN@") != 1 or template.count(b"@SOURCE_SUMS@") != 1:
        raise ValueError("Unbound workflow template")
    contents["PASTE_INNER.txt"] = template.replace(b"@PIN@", pin.encode()).replace(
        b"@SOURCE_SUMS@", sha(contents["SOURCE_SHA256SUMS"]).encode())
    contents["README_KO.md"] = blob(FOLDER+"README.md")
    contents["SHA256SUMS"] = sums(contents)
    packed = io.BytesIO()
    with zipfile.ZipFile(packed, "w") as archive:
        for name, data in sorted(contents.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    raw = packed.getvalue()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if sorted(archive.namelist()) != sorted(contents) or archive.testzip() is not None:
            raise ValueError("ZIP verification failed")
        for name, data in contents.items():
            if archive.read(name) != data:
                raise ValueError("Mismatch: "+name)
    script = (HEAD + "\n".join(textwrap.wrap(base64.b64encode(raw).decode("ascii"), 76))
              + TAIL.replace("@ZIP_SHA@", sha(raw)).replace("@PIN@", pin)).encode("ascii")
    txt = "PASTE_SUYOUNG_U6C_F8_NODE145_PAIR_"+pin[:12]+"_1122.txt"
    zipname = "suyoung_u6c_f8_node145_pair_wsl_"+pin[:12]+"_20261122.zip"
    out = args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    write_checked(out/txt, script)
    write_checked(out/zipname, raw)
    for name, data in ((txt,script),(zipname,raw)):
        write_checked(out/(name+".sha256"), sums({name:data}))
        print(name, sha(data))


if __name__ == "__main__":
    main()
