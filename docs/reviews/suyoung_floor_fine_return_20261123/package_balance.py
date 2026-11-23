"""Build the observation block using the immutable, previously delivered 12/24 package."""
import argparse
import base64
import gzip
import hashlib
import io
import subprocess
import tarfile
from pathlib import Path


PRIOR_PIN = "e8e2f2535aa12b9fb089d714e1325d862cb1161b"
PRIOR_TXT = "96270f3c4f37980436c23c72b86a238370e2dbcfe0eb3702407bc2b078f7ad3a"
PRIOR_ARCHIVE = "a6bdf77ce8d0562a141267519f6d747e278f2fc40e12f4ef4d970f5c8eca2c7f"
PRIOR_MANIFEST = "65b61a27d274b8fa0ea4a9892820d450faf972b94b382ff5f3de8dd9f2d57f0f"
CASE = "docs/reviews/suyoung_floor_fine_return_20261123/"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def manifest(files):
    return "".join(f"{digest(raw)}  {name}\n" for name,raw in sorted(files.items())).encode("ascii")


def previous_sources(previous_block):
    txt = previous_block.read_bytes()
    if digest(txt) != PRIOR_TXT:
        raise ValueError("previous operator block hash")
    start = b"base64 -d > source.tar.gz <<'FINE_FLOOR_SOURCES'\n"
    encoded = txt.split(start, 1)[1].split(b"\nFINE_FLOOR_SOURCES\n", 1)[0]
    data = base64.b64decode(b"".join(encoded.splitlines()), validate=True)
    if digest(data) != PRIOR_ARCHIVE:
        raise ValueError("previous embedded source archive hash")
    with tarfile.open(fileobj=io.BytesIO(data),mode="r:gz") as tar:
        if not all(m.isfile() for m in tar) or len(tar.getnames()) != len(set(tar.getnames())):
            raise ValueError("previous source archive members")
        files = {m.name:tar.extractfile(m).read() for m in tar}
    recorded = files.pop("SOURCE_SHA256SUMS")
    if (digest(recorded) != PRIOR_MANIFEST or manifest(files) != recorded or
            files["RELEASE"] != (PRIOR_PIN+"\n").encode()):
        raise ValueError("previous source manifest")
    files["SOURCE_SHA256SUMS"] = recorded
    return {"history/"+n:v for n,v in files.items()}


def payload(repo, ref, previous_block):
    repo=repo.resolve()
    git=["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo)]
    release=subprocess.check_output(git+["rev-parse","--verify",ref+"^{commit}"]).decode().strip()
    subprocess.run(git+["merge-base","--is-ancestor",PRIOR_PIN,release],check=True)
    files=previous_sources(previous_block)
    for path in (CASE+"early_wall_observer.py",CASE+"run_balance.sh"):
        files[path]=subprocess.check_output(git+["show",release+":"+path])
    files["RELEASE"]=(release+"\n").encode()
    files["SOURCE_SHA256SUMS"]=manifest(files)
    stream=io.BytesIO()
    with gzip.GzipFile(fileobj=stream,mode="wb",mtime=0) as gz:
        with tarfile.open(fileobj=gz,mode="w") as tar:
            for name,raw in sorted(files.items()):
                m=tarfile.TarInfo(name)
                m.mode=0o600
                m.size=len(raw)
                tar.addfile(m,io.BytesIO(raw))
    return release,stream.getvalue()


def build(repo,ref,previous_block,out):
    pin,archive=payload(repo,ref,previous_block)
    top=b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 2 ]]; then
    echo 'Usage: CHECK_ONLY|GO_SUYOUNG_WALL_BALANCE_ONCE <completed F12/F24 result.tar.gz>' >&2
    exit 2
fi
case "$1" in CHECK_ONLY|GO_SUYOUNG_WALL_BALANCE_ONCE) ;; *) exit 2 ;; esac
prior=$(realpath -e -- "$2")
[[ -f "$prior" ]]
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'WALL_BALANCE_SOURCES'
"""
    end=f"""WALL_BALANCE_SOURCES
printf '%s  source.tar.gz\\n' '{digest(archive)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash {CASE}run_balance.sh "$1" "$prior"
""".encode("ascii")
    block=top+base64.encodebytes(archive)+end
    out.mkdir(parents=True,exist_ok=True)
    path=out/f"PASTE_SUYOUNG_WALL_BALANCE_{pin[:12]}_1123.txt"
    for p,raw in ((path,block),(path.with_suffix(".txt.sha256"),(digest(block)+"  "+path.name+"\n").encode())):
        if p.exists() and p.read_bytes()==raw:
            continue
        with p.open("xb") as output:
            output.write(raw)
    print(path, "BLOCK_SHA256="+digest(block), "SOURCE_TAR_SHA256="+digest(archive),sep="\n")


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo",type=Path,required=True)
    cli.add_argument("--ref",required=True)
    cli.add_argument("--out",type=Path,required=True)
    cli.add_argument("--previous-block",type=Path,required=True)
    a=cli.parse_args()
    build(a.repo,a.ref,a.previous_block,a.out)
