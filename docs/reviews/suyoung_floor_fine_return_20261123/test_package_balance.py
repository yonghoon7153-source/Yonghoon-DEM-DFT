"""Exercise block assembly without launching a field run or mutating a worktree."""
import argparse
import base64
import importlib.util
import io
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("package_balance", Path(__file__).with_name("package_balance.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def check(previous):
    historical=m.previous_sources(previous)
    pin="f"*40
    content={m.CASE+"early_wall_observer.py":b"raise SystemExit(23)\n",
             m.CASE+"run_balance.sh":Path(__file__).with_name("run_balance.sh").read_bytes()}
    def git(argv):
        if "rev-parse" in argv:
            return (pin+"\n").encode()
        return content[argv[-1].split(":",1)[1]]
    with TemporaryDirectory() as tmp, patch.object(m.subprocess,"check_output",side_effect=git), patch.object(m.subprocess,"run") as ancestor:
        out=Path(tmp)/"out"
        m.build(Path(tmp),"HEAD",previous,out)
        ancestor.assert_called_once()
        block=next(out.glob("*.txt")).read_bytes()
        encoded=block.split(b"base64 -d > source.tar.gz <<'WALL_BALANCE_SOURCES'\n",1)[1].split(b"\nWALL_BALANCE_SOURCES",1)[0]
        raw=base64.b64decode(b"".join(encoded.splitlines()),validate=True)
        assert m.digest(raw).encode() in block
        with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as t:
            files={i.name:t.extractfile(i).read() for i in t}
        assert m.manifest({k:v for k,v in files.items() if k!="SOURCE_SHA256SUMS"}) == files["SOURCE_SHA256SUMS"]
        assert {k:v for k,v in files.items() if k.startswith("history/")} == historical
        assert all(files[n]==v for n,v in content.items())
        assert files["RELEASE"]==(pin+"\n").encode()
        _, rerun=m.payload(Path(tmp),"HEAD",previous)
        assert raw==rerun
    print("PACKAGE_INTERIOR_SET_AND_PIN_OK")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("previous",type=Path)
    check(p.parse_args().previous)
