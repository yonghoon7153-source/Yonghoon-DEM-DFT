"""Package the one-shot F8/F16 short signed momentum observation from fixed Git blobs. Does not run a model."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile
import textwrap


MODEL = "99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f"
ROOT = "docs/reviews/"
PRIOR_FOLDER = ROOT+"suyoung_u6c_updated_f16_20261122/"
PAIR = ROOT+"suyoung_u6c_f16_stop_20261122/run_pair.py"
FOLDER = ROOT+"suyoung_wall_momentum_20261122/"
PREFIX_PIN = "e1db2841252d7f5babfbc4e55ad401540040ca24"
PREFIX_OBSERVER = ROOT+"suyoung_first_grid_return_20261122/observe_prefix.py"
PREFIX_OBSERVER_SHA = "b257e8b8cbaf9c3e04e722cc3061b2119fb310b4ec07a7ace60e8c2b90a04f3e"
KERNEL = "scripts/suyoung_multicontact_dev.py"
KERNEL_SHA = "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"
FROZEN = (
    KERNEL, "scripts/dem_suyoung_sf2d_dev.py", "scripts/suyoung_u6_first_dev.py", "scripts/suyoung_u6b_dev.py",
    ROOT+"suyoung_u6c_node145_20261122/node145_pair.py", ROOT+"suyoung_u6c_step145_20261122/capture_stop.py",
    ROOT+"suyoung_u6c_wall_return_20261122/dt_control.py", ROOT+"suyoung_u6c_force_rule_20261122/force_rule.py",
    ROOT+"suyoung_u6c_force_rule_20261122/rule.json", ROOT+"suyoung_u6c_doubling_readback_20261122/doubling.py",
)
HEAD = """#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 2 || ( $1 != CHECK_ONLY && $1 != GO_SUYOUNG_WALL_MOMENTUM_ONCE ) ]]; then
    echo 'Usage: bash THIS.txt CHECK_ONLY|GO_SUYOUNG_WALL_MOMENTUM_ONCE suyoung_wall_prefix_result.tar.gz' >&2
    exit 2
fi
prior=$(realpath -e -- "$2")
package=$(mktemp -d "${TMPDIR:-/tmp}/suyoung_wall_momentum_pkg_XXXXXXXX")
cd -- "$package"
base64 -d > source.tar.gz <<'MOMENTUM_SOURCE_TAR'
"""
TAIL = """
MOMENTUM_SOURCE_TAR
printf '%s  source.tar.gz\\n' '@TAR_SHA@' | sha256sum -c --status -
tar -xzf source.tar.gz
sha256sum -c --status SHA256SUMS
printf 'RELEASE=@PIN@\\nSOURCE_TAR_SHA256=@TAR_SHA@\\nPACKAGE_DIR=%s\\n' "$package"
bash "$package/PASTE_INNER.txt" "$1" "$prior"
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
    git(repo,"merge-base","--is-ancestor",PREFIX_PIN,pin)
    def blob(name, rev=pin):
        return git(repo,"cat-file","blob",rev+":"+name)
    prior_tools=(PRIOR_FOLDER+"f16_candidate.py", PRIOR_FOLDER+"read_f8_f16.py", PAIR)
    dependencies=(*FROZEN,*prior_tools)
    members={name:blob(name) for name in (*dependencies,PREFIX_OBSERVER,FOLDER+"observe_momentum.py",FOLDER+"momentum_plan.md")}
    if git(repo,"rev-parse",MODEL+":scripts")!=git(repo,"rev-parse",pin+":scripts"):
        raise ValueError("Full scripts tree differs from completed pair")
    for name in dependencies:
        if members[name]!=blob(name,MODEL):
            raise ValueError("Frozen dependency differs from completed pair: "+name)
    if members[PREFIX_OBSERVER]!=blob(PREFIX_OBSERVER,PREFIX_PIN) or sha(members[PREFIX_OBSERVER])!=PREFIX_OBSERVER_SHA:
        raise ValueError("Prior lower-wall observer identity")
    if sha(members[KERNEL])!=KERNEL_SHA:
        raise ValueError("Contact kernel identity")
    members["RELEASE"]=(pin+"\n"+MODEL+"\n"+PREFIX_PIN+"\n").encode("ascii")
    members["SOURCE_SHA256SUMS"]=sums(members)
    template=blob(FOLDER+"run_wsl.in")
    if any(template.count(tag)!=1 for tag in (b"@PIN@",b"@SOURCE_SUMS@",b"@KERNEL@")):
        raise ValueError("Unbound block template")
    members["PASTE_INNER.txt"]=template.replace(b"@PIN@",pin.encode()).replace(b"@KERNEL@",sha(members[KERNEL]).encode()).replace(
        b"@SOURCE_SUMS@",sha(members["SOURCE_SHA256SUMS"]).encode())
    members["SHA256SUMS"]=sums(members)
    raw=pack(members)
    block=(HEAD+"\n".join(textwrap.wrap(base64.b64encode(raw).decode("ascii"),76))+
           TAIL.replace("@TAR_SHA@",sha(raw)).replace("@PIN@",pin)).encode("ascii")
    out=args.out.resolve()
    out.mkdir(exist_ok=True,parents=True)
    for file,data in (("PASTE_SUYOUNG_U6C_WALL_MOMENTUM_"+pin[:12]+"_1122.txt",block),
                      ("suyoung_u6c_wall_momentum_source_"+pin[:12]+"_20261122.tar.gz",raw)):
        store(out/file,data)
        store(out/(file+".sha256"),sums({file:data}))
        print(file,sha(data))


if __name__=="__main__":
    main()
