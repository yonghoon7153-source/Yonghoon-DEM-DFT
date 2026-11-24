"""Build the operator release from committed Git blobs. The connection header stays in the local output."""
import argparse
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile
import zipfile

PREFIX="docs/reviews/ps73_parallel_20261124/"
OLD="docs/reviews/ps73_development_sequence_20261121/"
def sha(b):
    return hashlib.sha256(b).hexdigest()

def build(repo, revision, out, header):
    def git(*args):
        return subprocess.check_output(["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo),*args])
    pin=git("rev-parse",revision+"^{commit}").decode().strip()
    def blob(name):
        return git("show",pin+":"+name)
    files={n:blob(PREFIX+n) for n in ("parallel.py","site_ops.py","engine.py","batch.sh")}
    files["ps73_node.py"]=blob(OLD+"node/ps73_node.py")
    files["ps73_sequence.py"]=blob(OLD+"sequence/ps73_sequence.py")
    files["RELEASE"]=(pin+"\n").encode()
    sums="".join(sha(b)+"  "+n+"\n" for n,b in sorted(files.items())).encode()
    files["SOURCE_SHA256SUMS"]=sums
    buf=io.BytesIO()
    with gzip.GzipFile(fileobj=buf,mode="wb",mtime=0) as gz:
        with tarfile.open(fileobj=gz,mode="w") as tar:
            for name,data in sorted(files.items()):
                m=tarfile.TarInfo(name)
                m.size=len(data)
                m.mode=0o700 if name=="batch.sh" else 0o600
                tar.addfile(m,io.BytesIO(data))
    out.mkdir(exist_ok=True,parents=True)
    pack=out/("ps73_parallel_"+pin[:12]+".tar.gz")
    pack.write_bytes(buf.getvalue())
    first=header.read_text(encoding="utf8").splitlines()[:2]
    if not (len(first)==2 and first[0].startswith("IBB=") and first[1].startswith("IBBP=")):
        raise ValueError("local operator header required")
    block=out/"PASTE_PS73_PARALLEL.txt"
    source=blob(PREFIX+"operator.template.sh").decode().replace("@TARBALL@",pack.name).replace("@TAR_SHA@",sha(pack.read_bytes())).replace("@MANIFEST_SHA@",sha(sums))
    block.write_bytes(("\n".join(first)+"\n"+source).encode())
    manifest="".join(sha(path.read_bytes())+"  "+path.name+"\n" for path in (block,pack)).encode()
    (out/"SHA256SUMS").write_bytes(manifest)
    archive=out/("AUTHOR_PS73_PARALLEL_"+pin[:12]+".zip")
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for path in (block,pack,out/"SHA256SUMS"):
            z.write(path,path.name)
    print(pin,sha(archive.read_bytes()),archive.name)

if __name__=="__main__":
    cli=argparse.ArgumentParser()
    for n in ("repo","revision","out","header"):
        cli.add_argument(n,type=str if n=="revision" else Path)
    a=cli.parse_args()
    build(a.repo.resolve(),a.revision,a.out,a.header)
