"""Bind the two new case names to the unchanged B2 observer's geometry and frame plan."""
import hashlib
import json
from pathlib import Path
import runpy
import tarfile

HERE = Path(__file__).resolve().parent
MANIFEST = "ef4b774f6ced93492e7eeffddb3830bd768f10ee45d574effd131ef424659b97"


def verified_observer(frozen):
    raw=(frozen/"SHA256SUMS").read_bytes()
    if hashlib.sha256(raw).hexdigest()!=MANIFEST:
        raise ValueError("unknown observer packet")
    for row in raw.decode("ascii").splitlines():
        digest,member=row.split("  ",1)
        if hashlib.sha256((frozen/member).read_bytes()).hexdigest()!=digest:
            raise ValueError("changed observer member")
    return runpy.run_path(str(frozen/"scripts/mixer_precal_observe.py"))


def binding(observer, frozen, arm, deck, meta):
    ref=observer["preparation"].prepare_case("PRECAL_R1_B2_U")
    other=observer["preparation"].prepare_case("PRECAL_R1_B2_C")
    generator=frozen/"scripts/make_mixer_deck.py"
    recipe=runpy.run_path(str(HERE/"recipe.py"))
    expected=recipe["generate"](generator,ref["deck"],other["deck"],json.dumps(ref["meta"]).encode())
    if arm not in expected or deck!=expected[arm][0] or json.loads(meta)!=json.loads(expected[arm][1]):
        raise ValueError("unbound ladder deck or metadata")
    refcase="PRECAL_R1_B2_U"
    geom=observer["validate_case"](refcase,ref["deck"],ref["meta"])
    observer["_check_binding"](geom,refcase)
    name="MIXER_B2_"+arm
    return dict(geom,case_id=name,role=arm,frame_pm=dict(geom["frame_pm"],arm=name))


def check_package(frozen, package):
    observer=verified_observer(frozen)
    with tarfile.open(package) as tar:
        for arm in ("L020","L050"):
            def get(n):
                return tar.extractfile("assets/"+arm+"/"+n).read()
            deck=get("in.mixer")
            geo=binding(observer,frozen,arm,deck,get("deck_meta.json"))
            items=[(i*32976,Path("mix_%d.liggghts"%(i*32976))) for i in range(1,235)]
            plan=observer["_frozen_plan"](deck,geo,items)
            if plan["t0_step"]!=34*32976 or plan["bin_steps"]!=[i*32976 for i in range(134,234)]:
                raise ValueError("wrong observation frames")
            print(geo["case_id"],geo["seed"],len(plan["bin_steps"]),"FROZEN_FRAME_PLAN_OK")


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("frozen",type=Path)
    p.add_argument("package",type=Path)
    a=p.parse_args()
    check_package(a.frozen.resolve(),a.package)
