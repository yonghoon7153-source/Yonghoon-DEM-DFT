"""Freeze the counterfactual moving-lid and the complete previous observation package."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile

BASE = "0c4eb97d447f9afa984303425e1c5ab221ae9cec"
BLOCK_SHA = "d00e4d7040b15592740922a04be242269be237d2dc1be6c5615fcdb384f4006d"
ARCHIVE_SHA = "9ed251a0b07cc392782728d28732f0acd4014945e9c2a63d56c3c06136543410"
FOLDER = "docs/reviews/suyoung_wall_balance_return_20261123/"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sources(repo, block, ref):
    config = ["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo)]
    pin=subprocess.check_output(config+["rev-parse","--verify",ref+"^{commit}"]).decode().strip()
    subprocess.run(config+["merge-base","--is-ancestor",BASE,pin],check=True)
    text=block.read_bytes()
    if digest(text)!=BLOCK_SHA:
        raise ValueError("wrong previous source block")
    marker=b"WALL_BALANCE_SOURCES"
    section=text.split(b"<<'"+marker+b"'\n",1)[1].split(b"\n"+marker+b"\n",1)[0]
    archive=base64.b64decode(b"".join(section.splitlines()),validate=True)
    if digest(archive)!=ARCHIVE_SHA:
        raise ValueError("wrong previous embedded sources")
    with tarfile.open(fileobj=io.BytesIO(archive),mode="r:gz") as t:
        files={"history/"+m.name:t.extractfile(m).read() for m in t if m.isfile()}
    for name in ("material_lid.py","lid_prefix.py","run_lid.sh"):
        files[FOLDER+name]=subprocess.check_output(config+["show",pin+":"+FOLDER+name])
    files["RELEASE"]=(pin+"\n").encode()
    files["SOURCE_SHA256SUMS"]="".join(f"{digest(v)}  {k}\n" for k,v in sorted(files.items())).encode()
    buf=io.BytesIO()
    with tarfile.open(fileobj=buf,mode="w") as out:
        for k,v in sorted(files.items()):
            entry=tarfile.TarInfo(k)
            entry.size=len(v)
            out.addfile(entry,io.BytesIO(v))
    return pin,gzip.compress(buf.getvalue(),mtime=0)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for k in ("repo","previous_block","out"):
        parser.add_argument(k,type=Path)
    parser.add_argument("--ref",default="HEAD")
    a=parser.parse_args()
    pin,src=sources(a.repo.resolve(),a.previous_block,a.ref)
    header=b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# -eq 2 && ( "$1" == CHECK_ONLY || "$1" == GO_SUYOUNG_MATERIAL_LID_ONCE ) ]] || { echo 'Expected CHECK_ONLY or GO_SUYOUNG_MATERIAL_LID_ONCE and wall-balance result.tar.gz' >&2; exit 2; }
prior=$(realpath -e -- "$2")
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'MATERIAL_LID_SOURCES'
"""
    footer=f"""MATERIAL_LID_SOURCES
printf '%s  source.tar.gz\\n' '{digest(src)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash {FOLDER}run_lid.sh "$1" "$prior"
""".encode("ascii")
    data=header+base64.encodebytes(src)+footer
    a.out.mkdir(parents=True,exist_ok=True)
    block=a.out/f"PASTE_SUYOUNG_MATERIAL_LID_{pin[:12]}_1123.txt"
    for path,raw in ((block,data),(block.with_suffix(".txt.sha256"),f"{digest(data)}  {block.name}\n".encode())):
        if path.exists() and path.read_bytes()==raw:
            continue
        with path.open("xb") as out:
            out.write(raw)
    print(block.name, digest(data), digest(src))


if __name__=="__main__":
    main()
