"""Build the author block from checked-in bytes, without opening any case directory."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile

B7 = "35f0327377a4213774010a090df4d224e50d29e1"
FOLDER = "docs/reviews/lhs_wsl30_source_freeze_20261124"
GO = "GO_LHS_WSL30_SECTION5_PRESSURE_ONCE"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(repo, output, commit):
    git=["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo)]
    def blob(ref, name):
        return subprocess.check_output([*git,"show",ref+":"+name])
    pin=subprocess.check_output([*git,"rev-parse","--verify",commit+"^{commit}"]).decode().strip()
    files={name:blob(pin,FOLDER+"/"+name) for name in ("read_after_go.py","roster.json")}
    for name in ("lhs_pressure_record.py","parse_liggghts.py","press_units.py"):
        files["b7/"+name]=blob(B7,"scripts/"+name)
    if digest(files["b7/lhs_pressure_record.py"])!="34eb74142884489505590501840ccc6423a014a508989c82f135020146283ad3":
        raise ValueError("wrong B7 reader")
    files["RELEASE"]=(pin+"\n").encode()
    files["SOURCE_SHA256SUMS"]="".join(f"{digest(b)}  {n}\n" for n,b in sorted(files.items())).encode()
    s=io.BytesIO()
    with gzip.GzipFile(fileobj=s,mode="wb",mtime=0,filename="") as gz:
        with tarfile.open(fileobj=gz,mode="w|") as arc:
            for n,b in sorted(files.items()):
                entry=tarfile.TarInfo(n)
                entry.size=len(b)
                arc.addfile(entry,io.BytesIO(b))
    data=s.getvalue()
    prefix=f"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# == 1 && $1 == {GO} ]] || {{ echo 'First-author approval for WSL30 pressure is required.' >&2; exit 2; }}
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'LHS_S5_SOURCE'
""".encode()
    suffix=f"""LHS_S5_SOURCE
printf '%s  source.tar.gz\\n' '{digest(data)}' | sha256sum --strict -c -
tar -xzf source.tar.gz
sha256sum --strict --status -c SOURCE_SHA256SUMS
[[ $(cat RELEASE) == '{pin}' ]]
out=$(mktemp -d "$HOME/lhs_wsl30_s5_return_XXXXXXXX")
printf 'RETURN_DIRECTORY=%s\\n' "$out"
exec "$HOME/Yonghoon-DEM-DFT/venv/bin/python" -I -X utf8 -B read_after_go.py "$1" "$out"
""".encode()
    data=prefix+base64.encodebytes(data)+suffix
    output.mkdir(parents=True,exist_ok=True)
    name="PASTE_LHS_WSL30_SECTION5_"+pin[:12]+"_1124.txt"
    for path,raw in ((output/name,data),(output/(name+".sha256"),f"{digest(data)}  {name}\n".encode())):
        if not path.exists():
            path.write_bytes(raw)
        elif path.read_bytes()!=raw:
            raise FileExistsError(path)
    print(name,digest(data))
    return name


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("repo",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("commit")
    a=p.parse_args()
    build(a.repo.resolve(),a.output,a.commit)
