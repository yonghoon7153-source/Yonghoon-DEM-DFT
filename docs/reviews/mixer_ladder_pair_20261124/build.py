"""Build a deterministic private distribution using the original B2-C source bundle."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
OLD = "caa6000642f68814ee7fed4aade680997cecff11615b2744d563e20ec477cdc6"
F8 = "packet/B/docs/reviews/mixer_first8_launch_preparation_20261106/"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def build(old, pin, out, operator=None):
    if not re.fullmatch("[0-9a-f]{40}", pin) or sha(old.read_bytes()) != OLD:
        raise ValueError("invalid pin or B2-C source bundle")
    out.mkdir(exist_ok=True, parents=True)
    files = {n:(HERE/n).read_bytes() for n in ("worker.sh","ladder.py")}
    with tarfile.open(old) as src, tempfile.TemporaryDirectory() as td:
        def get(n):
            return src.extractfile(n).read()
        u = F8+"planned_assets/PRECAL_R1_B2_U/"
        c = F8+"planned_assets/PRECAL_R1_B2_C/"
        generator = Path(td)/"make_mixer_deck.py"
        generator.write_bytes(get("packet/B/scripts/make_mixer_deck.py"))
        assets = runpy.run_path(str(HERE/"recipe.py"))["generate"](
            generator,get(u+"in.mixer"),get(c+"in.mixer"),get(u+"deck_meta.json"))
        for arm,(deck,meta) in assets.items():
            prefix="assets/"+arm+"/"
            files[prefix+"in.mixer"],files[prefix+"deck_meta.json"] = deck,meta
            for geom in ("Drum.stl","Front.stl","Back.stl"):
                if get(u+geom)!=get(c+geom):
                    raise ValueError("B2 mesh differs")
                files[prefix+geom]=get(u+geom)
        for n in ("mixer_b1_pair_ibb.py","mixer_rotation_n0_ibb.py","mixer_e0_pilot_ibb.py"):
            files["lib/"+n]=get("packet/controller/"+n)
        files["lib/job_start.py.txt"]=get(F8+"job_start.py.txt")
        files["control/runtime_reference.json"]=get("packet/control/runtime_reference.json")
    reg = {"pin":pin,"arms":{"L020":0.20,"L050":0.50},"seed":32452843,
           "NP":20,"max_pair_cpus":40,"account_cap":60,"hours":48,
           "B2_source_sha256":OLD,"files":{n:sha(v) for n,v in files.items()}}
    files["release.json"]=(json.dumps(reg,sort_keys=True,indent=2)+"\n").encode()
    package=out/("mixer_ladder_pair_source_"+pin[:12]+".tar.gz")
    with package.open("xb") as raw, gzip.GzipFile(filename="",fileobj=raw,mode="wb",mtime=0) as gz, tarfile.open(fileobj=gz,mode="w") as tar:
        for n,body in sorted(files.items()):
            header=tarfile.TarInfo(n)
            header.size=len(body)
            header.mode=0o600
            tar.addfile(header,io.BytesIO(body))
    if operator:
        lines=operator.read_text(encoding="utf-8-sig").splitlines()
        host=[s for s in lines if re.fullmatch(r"IBB='[\w.@-]+'",s)]
        port=[s for s in lines if re.fullmatch(r"IBBP=\d+",s)]
        if len(host)!=1 or len(port)!=1:
            raise ValueError("site header must be unique")
        block=(HERE/"operator.template").read_text().replace("IBB='@IBB@'",host[0]).replace("IBBP=@PORT@",port[0])
        block=block.replace("@SOURCE@",package.name).replace("@PIN@",pin).replace("@SHA@",sha(package.read_bytes()))
        with (out/"PASTE_MIXER_LADDER_PAIR.txt").open("x",encoding="utf8",newline="\n") as f:
            f.write(block)
    return package


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("b2_source",type=Path)
    p.add_argument("pin")
    p.add_argument("output",type=Path)
    p.add_argument("--operator",type=Path)
    a=p.parse_args()
    result=build(a.b2_source,a.pin,a.output,a.operator)
    print(result.name,sha(result.read_bytes()))
