"""Read only fixed kit and 368315 evidence. Test the original UB gate on real receipt bytes, no engine."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import zipfile


def need(ok, why):
    if not ok: raise ValueError(why)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(payload,returned):
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)
        kit=root/"fixed_kit"
        kit.mkdir()
        src=payload.read_bytes()
        need(sha(src)=="7eaab059442c2216ced003ed557ebd0ba1a050a6d70a11332018f4ded3e80a5d","A5 payload")
        with zipfile.ZipFile(io.BytesIO(src)) as z:
            fixed=z.read("fixed_kit_9fd6aa9d3bee.zip")
        need(sha(fixed)=="d8074dfd86d227d80bc3188fa8817a7af7b22b333caa3c22292ce62b10650920","kit")
        with zipfile.ZipFile(io.BytesIO(fixed)) as z:
            z.extractall(kit)
        folder=root/"ps_7_3_r45"
        rj=folder/"RJ"
        rj.mkdir(parents=True)
        with zipfile.ZipFile(returned) as z:
            report=z.read("RJ.report.tgz")
        need(sha(report)=="356599363557f30ac878605349d485c8aa4f96821a842926436d2abde1b01b99","returned report")
        with tarfile.open(fileobj=io.BytesIO(report),mode="r:gz") as a:
            for name,pin in (("RJ/run_manifest.txt","d4647c1654acf8d225b2b24f64c5e0d8246328f299c057ff3c033b6e6944b5e1"),
                             ("RJ/restore_verdict.json","b049a3707aede899f4c6badc7176eb63246da8986dea58459dbea4aae45e73e6"),
                             ("ul_base.in","016f0402edba632864ef0a0423a5aaf8360a7eac2054e0b5b4191917648ce272")):
                data=a.extractfile(name).read()
                need(sha(data)==pin,name)
                (folder/name).write_bytes(data)
        cmd=[sys.executable,"-I","-B",str(kit/"ul_reader.py"),"gate",str(root),"ps_7_3_r45","UB"]
        # Only the gate is called. It consumes bytes without rewriting paths or reading physical values.
        res=subprocess.run(cmd,stdout=subprocess.PIPE)
        need(res.returncode==0 and res.stdout.startswith(b"GATE bed=ps_7_3_r45 job=UB ALLOW "),"legacy UB gate")
        # Strict ad hoc copy location must fail the sealed dispatcher's original-job binding.
        cmd[3]=str(kit/"rt_dispatch_a5.py")
        result=subprocess.run(cmd,stdout=subprocess.PIPE)
        need(result.returncode==2 and result.stdout.startswith(b"GATE bed=ps_7_3_r45 job=UB REFUSE "),"A5 original location")
        print("ACTUAL_368315_LEGACY_GATE=ALLOW A5_RELOCATED_GATE=REFUSE A5_ORIGIN=AUTHOR_SITE_RECEIPT")


if __name__=="__main__":
    arg=argparse.ArgumentParser()
    arg.add_argument("payload",type=Path); arg.add_argument("returned",type=Path)
    opt=arg.parse_args()
    main(opt.payload,opt.returned)
