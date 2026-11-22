"""Package the one-shot F8/F16 author pair from fixed Git blobs. Does not run a model."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile
import textwrap


MODEL = "2cf17b1df57396ef01505a72641e01b19629bed5"
ROOT = "docs/reviews/"
PRIOR_ADAPTER = "e5c3ac7bba373efc4a7a0367c6f6ecee41018f29"
PRIOR_FOLDER = ROOT+"suyoung_u6c_updated_f16_20261122/"
FOLDER = ROOT+"suyoung_u6c_f16_stop_20261122/"
KERNEL = "scripts/suyoung_multicontact_dev.py"
KERNEL_SHA = "8af03f07e8149219a13baa1d1ca79c2fc87940bb991c6055769ac0beeb3a8880"
FROZEN = (
    KERNEL, "scripts/dem_suyoung_sf2d_dev.py", "scripts/suyoung_u6_first_dev.py", "scripts/suyoung_u6b_dev.py",
    ROOT+"suyoung_u6c_node145_20261122/node145_pair.py", ROOT+"suyoung_u6c_step145_20261122/capture_stop.py",
    ROOT+"suyoung_u6c_wall_return_20261122/dt_control.py", ROOT+"suyoung_u6c_force_rule_20261122/force_rule.py",
    ROOT+"suyoung_u6c_force_rule_20261122/rule.json", ROOT+"suyoung_u6c_doubling_readback_20261122/doubling.py",
)
HEAD = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 3 || ( $1 != CHECK_ONLY && $1 != GO_SUYOUNG_F8_F16_CONTACT_ONCE ) ]]; then
    echo 'Usage: bash THIS.txt CHECK_ONLY|GO_SUYOUNG_F8_F16_CONTACT_ONCE final_F8_result.tar.gz stopped_F16_result.tar.gz' >&2
    exit 2
fi
f8=$(realpath -e -- "$2")
stop=$(realpath -e -- "$3")
package=$(mktemp -d "${TMPDIR:-/tmp}/suyoung_contact_pair_pkg_XXXXXXXX")
cd -- "$package"
base64 -d > source.tar.gz <<'F16_SOURCE_TAR'
"""
TAIL = """
F16_SOURCE_TAR
printf '%s  source.tar.gz\\n' '@TAR_SHA@' | sha256sum -c --status -
tar -xzf source.tar.gz
sha256sum -c --status SHA256SUMS
printf 'RELEASE=@PIN@\\nSOURCE_TAR_SHA256=@TAR_SHA@\\nPACKAGE_DIR=%s\\n' "$package"
bash "$package/PASTE_INNER.txt" "$1" "$f8" "$stop"
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sums(members):
    return "".join(sha(data)+"  "+name+"\n" for name,data in sorted(members.items())).encode("ascii")


def git(repo,*args):
    return subprocess.run(["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo),*args],
                          check=True,capture_output=True).stdout


def pack(members):
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer,mode="wb",mtime=0,filename="") as compressed:
        with tarfile.open(fileobj=compressed,mode="w",format=tarfile.USTAR_FORMAT) as t:
            for name,data in sorted(members.items()):
                item = tarfile.TarInfo(name)
                item.size = len(data)
                item.mode = 0o600
                t.addfile(item,io.BytesIO(data))
    raw = buffer.getvalue()
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as t:
        if t.getnames()!=sorted(members) or any(not item.isfile() or t.extractfile(item).read()!=members[item.name]
                                                for item in t):
            raise ValueError("Source TAR verification")
    return raw


def store(path, data):
    if not path.exists():
        with path.open("xb") as out:
            out.write(data)
    elif path.read_bytes()!=data:
        raise FileExistsError(path)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--commit",required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    repo=args.repo.resolve(strict=True)
    pin=git(repo,"rev-parse","--verify","--end-of-options",args.commit+"^{commit}").decode().strip()
    git(repo,"merge-base","--is-ancestor",MODEL,pin)
    def blob(name, rev=pin):
        return git(repo,"cat-file","blob",rev+":"+name)
    prior_tools=(PRIOR_FOLDER+"f16_candidate.py", PRIOR_FOLDER+"read_f8_f16.py")
    members={name:blob(name) for name in (*FROZEN,*prior_tools,FOLDER+"run_pair.py")}
    changed=git(repo,"diff","--name-only","--no-renames",MODEL,pin,"--","scripts/").decode().splitlines()
    if changed != [KERNEL]:
        raise ValueError("Expected only the contact kernel to differ under scripts/: "+repr(changed))
    for name in prior_tools:
        if members[name]!=blob(name,PRIOR_ADAPTER):
            raise ValueError("Historical adapter differs: "+name)
    for name in FROZEN:
        if name!=KERNEL and members[name]!=blob(name,MODEL):
            raise ValueError("Frozen source differs: "+name)
    if sha(blob(KERNEL,MODEL))!=KERNEL_SHA or sha(members[KERNEL])==KERNEL_SHA:
        raise ValueError("Historical or candidate kernel identity")
    members["RELEASE"]=(pin+"\n"+MODEL+"\n"+PRIOR_ADAPTER+"\n").encode("ascii")
    members["SOURCE_SHA256SUMS"]=sums(members)
    template=blob(FOLDER+"run_wsl.in")
    if any(template.count(tag)!=1 for tag in (b"@PIN@",b"@SOURCE_SUMS@",b"@KERNEL@")):
        raise ValueError("Unbound block template")
    members["PASTE_INNER.txt"]=template.replace(b"@PIN@",pin.encode()).replace(b"@KERNEL@",sha(members[KERNEL]).encode()).replace(
        b"@SOURCE_SUMS@",sha(members["SOURCE_SHA256SUMS"]).encode())
    members["README_KO.md"]=blob(FOLDER+"README.md")
    members["SHA256SUMS"]=sums(members)
    raw=pack(members)
    block=(HEAD+"\n".join(textwrap.wrap(base64.b64encode(raw).decode("ascii"),76))+
           TAIL.replace("@TAR_SHA@",sha(raw)).replace("@PIN@",pin)).encode("ascii")
    out=args.out.resolve()
    out.mkdir(exist_ok=True,parents=True)
    for file,data in (("PASTE_SUYOUNG_U6C_F8_F16_CONTACT_"+pin[:12]+"_1122.txt",block),
                      ("suyoung_u6c_f8_f16_contact_source_"+pin[:12]+"_20261122.tar.gz",raw)):
        store(out/file,data)
        store(out/(file+".sha256"),sums({file:data}))
        print(file,sha(data))


if __name__=="__main__":
    main()
