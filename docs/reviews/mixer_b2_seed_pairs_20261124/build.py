"""Prepare reproducible field and WSL bundles from hash-pinned B2 and ladder distributions."""
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

HERE=Path(__file__).resolve().parent
LADDER="708b3a688d5a75d8cb65bd987342e7d35c06bc817d853d5386a6e5dae4f7a9bc"
B2="caa6000642f68814ee7fed4aade680997cecff11615b2744d563e20ec477cdc6"
OBS="bb2f322987fa6eb2e49159e6cc1447f5264036fc9cd84b3f4d59a60ffbc63710"
OLD_RESULT="12f0b9d0899b792b0e11466924087b229b82ecb41fcf16712ae452f20a9ac0f2"
F8="packet/B/docs/reviews/mixer_first8_launch_preparation_20261106/planned_assets/"
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(data):return (json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode()
def write_tar(files,path):
    with path.open("xb") as f,gzip.GzipFile(fileobj=f,filename="",mode="wb",mtime=0) as gz,tarfile.open(fileobj=gz,mode="w") as t:
        for n,b in sorted(files.items()):
            m=tarfile.TarInfo(n);m.size=len(b);m.mode=0o600
            t.addfile(m,io.BytesIO(b))

def build(args):
    out=args.out
    out.mkdir(parents=True,exist_ok=True)
    if sha(args.old.read_bytes())!=B2 or sha(args.ladder.read_bytes())!=LADDER or sha(args.prior.read_bytes())!=OLD_RESULT:
        raise ValueError("reference package identity")
    if not re.fullmatch(r"[0-9a-f]{40}",args.pin):raise ValueError("pin")
    recipe=runpy.run_path(str(HERE/"seed_decks.py"))
    files={n:(HERE/n).read_bytes() for n in ("repeat.py","seed_decks.py","worker.sh","readback.py","registration.md")}
    files["prior_pair.json"]=args.prior.read_bytes()
    info={}
    with tarfile.open(args.ladder) as lt,tarfile.open(args.old) as bt,tempfile.TemporaryDirectory() as tmp:
        def get(t,n):return t.extractfile(n).read()
        files["ladder_base.py"]=get(lt,"ladder.py")
        names=("make_mixer_deck","make_mixer_resume","mixer_deck_diff","mixer_deck_readback","mixer_precal_observe","mixer_precal_prepare","measure_bed_aspect","measure_mixing_index","mixer_contact_reader")
        for n in names:
            files["observer/"+n+".py"]=get(bt,"packet/B/scripts/"+n+".py")
        if sha(files["observer/mixer_precal_observe.py"])!=OBS:raise ValueError("observer identity")
        g=Path(tmp)/"make_mixer_deck.py"
        g.write_bytes(files["observer/make_mixer_deck.py"])
        gen=runpy.run_path(str(g))
        for family,seed in recipe["SEEDS"].items():
            w={"ladder.py":(HERE/"wave_entry.py").read_bytes()}
            for m in lt.getnames():
                if m.startswith(("lib/","control/")):w[m]=get(lt,m)
            ratios={}
            for role,ratio in (("U",0.1),("C",1.0)):
                arm=family+role
                ratios[arm]=ratio
                pre=F8+"PRECAL_R1_B2_"+role+"/"
                raw,meta,pair=recipe["generate"](gen,get(bt,pre+"in.mixer"),json.loads(get(bt,pre+"deck_meta.json")),arm)
                dest="assets/"+arm+"/"
                w[dest+"in.mixer"]=raw
                w[dest+"deck_meta.json"]=dump(meta)
                for n in ("Drum.stl","Front.stl","Back.stl"):w[dest+n]=get(bt,pre+n)
                info[arm]=dict(seed=seed,role=role,secondary_seed=pair[1],ratio=ratio,deck=sha(raw),metadata=sha(dump(meta)))
            w["release.json"]=dump(dict(pin=args.pin,arms=ratios,seed=seed,files={n:sha(b) for n,b in w.items()}))
            files.update({family+"/"+n:b for n,b in w.items()})
    files["campaign.json"]=dump(dict(pin=args.pin,seeds=recipe["SEEDS"],predecessors=["373356","373357"],arms=info,
                                files={n:sha(b) for n,b in files.items()}))
    pack=out/("mixer_seed_pairs_"+args.pin[:12]+".tar.gz")
    write_tar(files,pack)
    lines=args.header.read_text(encoding="utf-8-sig").splitlines()
    hdr=lines[:2]
    if not re.fullmatch(r"IBB='[\w.@-]+'",hdr[0]) or not re.fullmatch(r"IBBP=\d+",hdr[1]):raise ValueError("operator header")
    op=(HERE/"operator.template").read_text(encoding="utf8").replace("@PACK@",pack.name).replace("@PIN@",args.pin).replace("@SHA@",sha(pack.read_bytes()))
    (out/"PASTE_MIXER_B2_SEEDS.txt").write_bytes(("\n".join(hdr)+"\n"+op).encode())
    print(pack.name,sha(pack.read_bytes()),info)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for key in ("old","ladder","prior","header","pin","out"):
        p.add_argument(key,type=str if key=="pin" else Path)
    build(p.parse_args())
