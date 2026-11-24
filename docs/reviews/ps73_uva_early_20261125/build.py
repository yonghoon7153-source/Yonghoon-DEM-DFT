"""Build a single WSL block from committed sources. The login header stays outside Git."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile

SOURCE = "docs/reviews/ps73_uva_early_20261125/"
def build(repo, revision, header_file, out):
    repo = repo.resolve()
    git = ["git", "-c", "safe.directory="+repo.as_posix(), "-C", str(repo)]
    pin = subprocess.check_output(git+["rev-parse", revision+"^{commit}"]).decode().strip()
    def blob(name):
        return subprocess.check_output(git+["show", pin+":"+SOURCE+name])
    files = {n:blob(n) for n in ("worker.sh","early.py")}
    files["RELEASE"] = (pin+"\n").encode()
    checks = "".join(hashlib.sha256(v).hexdigest()+"  "+n+"\n" for n,v in sorted(files.items())).encode()
    files["SOURCE_SHA256SUMS"] = checks
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf,mode="wb",mtime=0) as gz, tarfile.open(fileobj=gz,mode="w") as tar:
        for name,data in sorted(files.items()):
            m = tarfile.TarInfo(name); m.size = len(data)
            m.mode = 0o700 if name=="worker.sh" else 0o600
            tar.addfile(m,io.BytesIO(data))
    pack = buf.getvalue()
    body = blob("operator.template.sh").replace(b"@SHA@",hashlib.sha256(pack).hexdigest().encode())
    body = body.replace(b"@MAN@",hashlib.sha256(checks).hexdigest().encode()).replace(b"@PAYLOAD@",base64.encodebytes(pack).strip())
    hdr = header_file.read_bytes().splitlines()[:2]
    if len(hdr)!=2 or not hdr[0].startswith(b"IBB=") or not hdr[1].startswith(b"IBBP="):
        raise ValueError("expected original private operator header")
    out.mkdir(exist_ok=True,parents=True)
    block = out / "PASTE_PS73_UVA_EARLY.txt"
    data = b"\n".join(hdr)+b"\n"+body
    with block.open("xb") as f: f.write(data)
    print(pin, hashlib.sha256(data).hexdigest(), block)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("repo",type=Path); p.add_argument("revision")
    p.add_argument("header_file",type=Path); p.add_argument("out",type=Path)
    a=p.parse_args(); build(**vars(a))
