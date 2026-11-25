"""Build one self-contained WSL operator from the pinned S operator and Git blobs."""
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import tarfile

HERE = "docs/reviews/suyoung_q13_setting2_20261125/"
B_BLOCK = "51c4aca0e39164055b677948c0b605601c4594830fd4785e735a845ad2060282"
B_MANIFEST = "7647ce296cffe72d4776ce33b8201fd97ca2266bb549e6c479a100802e25eb4b"
B_PIN = "c858862722bf6e5eb587ccbd54e1eef7dd59aa27"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def manifest(members):
    return "".join(f"{sha(data)}  {key}\n" for key,data in sorted(members.items())).encode("ascii")

def baseline(block):
    if sha(block) != B_BLOCK:
        raise ValueError("S operator identity")
    payload = block.split(b"<<'U6B_SOURCES'\n",1)[1].split(b"\nU6B_SOURCES\n",1)[0]
    with tarfile.open(fileobj=io.BytesIO(base64.b64decode(b"".join(payload.splitlines()),validate=True)), mode="r:gz") as archive:
        members = {}
        for item in archive:
            if not item.isfile() or item.name in members or item.name.startswith("/") or ".." in item.name.split("/"):
                raise ValueError("source member")
            members[item.name] = archive.extractfile(item).read()
    sums = members.pop("SOURCE_SHA256SUMS")
    if sha(sums) != B_MANIFEST or sums != manifest(members) or members["RELEASE"].decode().strip() != B_PIN:
        raise ValueError("source manifest")
    members["SOURCE_SHA256SUMS"] = sums
    return {"baseline/"+name:data for name,data in members.items()}

def build(repo, release, block, out):
    git = ["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo)]
    pin = subprocess.check_output([*git,"rev-parse","--verify",release+"^{commit}"]).decode().strip()
    def source(ref,path):
        return subprocess.check_output([*git,"show",ref+":"+path])
    files = baseline(block.read_bytes())
    for name in ("q13.py","coordinate.py","run.sh","registration.md"):
        files[name] = source(pin,HERE+name)
    for name in ("suyoung_u6b_dev.py","suyoung_u6b36_dev.py"):
        files["rules/"+name] = source(B_PIN,"scripts/"+name)
    files["history_reader.py"] = source(pin,"docs/reviews/suyoung_u6b_return_20261123/verify_return.py")
    files["RELEASE"] = (pin+"\n").encode()
    files["SOURCE_SHA256SUMS"] = manifest(files)
    buf = io.BytesIO()
    with gzip.GzipFile(filename="",fileobj=buf,mode="wb",mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w|") as archive:
            for name,data in sorted(files.items()):
                info = tarfile.TarInfo(name)
                info.size = len(data)
                archive.addfile(info,io.BytesIO(data))
    package = buf.getvalue()
    operator = b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
case "${1:-}" in GO_SUYOUNG_Q13_PAIR_ONCE|CHECK_ONLY|READBACK) ;; *) echo 'Expected GO_SUYOUNG_Q13_PAIR_ONCE, CHECK_ONLY or READBACK'; exit 2;; esac
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'Q13_PAIR_SOURCES'
""" + base64.encodebytes(package) + f"""Q13_PAIR_SOURCES
printf '%s  source.tar.gz\\n' '{sha(package)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash run.sh "$@"
""".encode()
    out.mkdir(parents=True,exist_ok=True)
    name = f"PASTE_SUYOUNG_Q13_PAIR_{pin[:12]}_1125.txt"
    for k,data in ((name,operator),(name+".sha256",manifest({name:operator}))):
        dest = out/k
        if not dest.exists():
            dest.write_bytes(data)
        elif dest.read_bytes()!=data:
            raise FileExistsError(dest)
    print(name, sha(operator), sha(package))

if __name__=="__main__":
    build(Path(sys.argv[1]).resolve(),sys.argv[2],Path(sys.argv[3]),Path(sys.argv[4]))
