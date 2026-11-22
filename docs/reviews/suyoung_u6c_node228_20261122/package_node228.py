"""Build the author's F8 development archive from a fixed Git commit."""
import argparse
import base64
import importlib.util
import io
from pathlib import Path
import textwrap
import zipfile


OLD = "d0c33bc19c2dd1291f3cf3ae0788fd193065e72b"
FOLDER = "docs/reviews/suyoung_u6c_node228_20261122/"
PREVIOUS = "docs/reviews/suyoung_u6c_node145_20261122/"
HELPER = PREVIOUS+"package_node145.py"


def shared_builder():
    # The sibling packaging utilities operate only on committed blobs.
    p = Path(__file__).resolve().parent.parent/"suyoung_u6c_node145_20261122"/"package_node145.py"
    spec = importlib.util.spec_from_file_location("pinned_package_util", p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HEAD = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 5 || ( $1 != CHECK_ONLY && $1 != GO_SUYOUNG_F8_NODE228_PAIR_ONCE ) ]]; then
    echo 'Usage: bash THIS.txt CHECK_ONLY|GO_SUYOUNG_F8_NODE228_PAIR_ONCE wall.tar.gz order.tar.gz capture145.tar.gz stop228.tar.gz' >&2
    exit 2
fi
mode=$1
shift
inputs=()
for archive in "$@"; do inputs+=("$(realpath -e -- "$archive")"); done
package=$(mktemp -d "${TMPDIR:-/tmp}/suyoung_node228_pkg_XXXXXXXX")
cd -- "$package"
base64 -d > source.zip <<'SOURCE_ZIP'
"""
TAIL = """
SOURCE_ZIP
printf '%s  source.zip\\n' '@ZIP_SHA@' | sha256sum -c --status -
unzip -q source.zip
sha256sum -c --status SHA256SUMS
printf 'RELEASE=@PIN@\\nPACKAGE_DIR=%s\\n' "$package"
bash "$package/PASTE_INNER.txt" "$mode" "${inputs[@]}"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    helper = shared_builder()
    repo = args.repo.resolve(strict=True)
    pin = helper.git(repo, "rev-parse", "--verify", "--end-of-options", args.commit+"^{commit}").decode().strip()

    def blob(name, rev=pin):
        return helper.git(repo, "cat-file", "blob", rev+":"+name)

    if Path(helper.__file__).read_bytes().replace(b"\r\n", b"\n") != blob(HELPER, OLD):
        raise ValueError("Packaging helper identity")
    contents = {name:blob(name) for name in (*helper.BASE_SOURCES, *helper.TOOLS, FOLDER+"bind_stop228.py")}
    kernel = "scripts/suyoung_multicontact_dev.py"
    for name in (*helper.BASE_SOURCES, *helper.TOOLS):
        if name != kernel and contents[name] != blob(name, OLD):
            raise ValueError("Frozen source differs: "+name)
    if any(contents[kernel] == blob(kernel, rev) for rev in (OLD,helper.PAIR_PIN)):
        raise ValueError("Candidate matches a previous failed kernel")
    contents["RELEASE"] = (pin+"\n"+OLD+"\n").encode("ascii")
    contents["SOURCE_SHA256SUMS"] = helper.sums(contents)
    template = blob(FOLDER+"run_wsl.in")
    if template.count(b"@PIN@") != 1 or template.count(b"@SOURCE_SUMS@") != 1:
        raise ValueError("Block binding points")
    contents["PASTE_INNER.txt"] = template.replace(b"@PIN@",pin.encode()).replace(
        b"@SOURCE_SUMS@",helper.sha(contents["SOURCE_SHA256SUMS"]).encode())
    contents["README_KO.md"] = blob(FOLDER+"README.md")
    contents["SHA256SUMS"] = helper.sums(contents)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer,"w") as archive:
        for name,data in sorted(contents.items()):
            info = zipfile.ZipInfo(name,(2026,11,22,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info,data)
    raw = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if archive.testzip() or {name:archive.read(name) for name in archive.namelist()} != contents:
            raise ValueError("Source ZIP verification")
    script = (HEAD + "\n".join(textwrap.wrap(base64.b64encode(raw).decode("ascii"),76))
              + TAIL.replace("@ZIP_SHA@",helper.sha(raw)).replace("@PIN@",pin)).encode("ascii")
    out = args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    for name,data in (("PASTE_SUYOUNG_U6C_F8_NODE228_PAIR_"+pin[:12]+"_1122.txt",script),
                      ("suyoung_u6c_f8_node228_pair_wsl_"+pin[:12]+"_20261122.zip",raw)):
        helper.write_checked(out/name,data)
        helper.write_checked(out/(name+".sha256"),helper.sums({name:data}))
        print(name,helper.sha(data))


if __name__ == "__main__":
    main()
