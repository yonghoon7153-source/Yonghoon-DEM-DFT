"""Exercise the delivered files offline. No cluster calls or physics engine."""
import argparse
from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import runpy
import tarfile
import tempfile
from unittest.mock import patch

def module(name,p):
    sp=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    return m

def run(package):
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp).resolve()
        with tarfile.open(package) as t:
            for member in t:
                p=root/member.name
                assert member.isfile() and root in p.resolve().parents
                p.parent.mkdir(exist_ok=True,parents=True)
                p.write_bytes(t.extractfile(member).read())
        r=module("repeat_fixture",root/"repeat.py")
        b=module("readback_fixture",root/"readback.py")
        man=r.source_check()
        obs=runpy.run_path(str(root/"observer/mixer_precal_observe.py"))
        assert not obs["_BOOT_ERROR"],obs["_BOOT_ERROR"]
        golden={}
        for arm,facts in man["arms"].items():
            a=r.wave(arm[:2])
            assert a.verify(a.library()["base"])["pin"]==man["pin"]
            deck=a.ROOT/"assets"/arm/"in.mixer"
            meta=b.read(deck.with_name("deck_meta.json"))
            bind=b.qualifier(obs,arm,man)
            geom=bind(a.case(arm),deck.read_bytes(),meta)
            obs["_check_binding"](geom,a.case(arm))
            listing=[(i*32976,"mix_%d.liggghts"%(i*32976)) for i in range(1,235)]
            assert obs["_frozen_plan"](deck.read_bytes(),geom,listing)["bin_steps"]==b.STEPS
            for bad in (dict(meta,seed=32452843),dict(meta,seed=man["seeds"]["S3" if arm[:2]=="S2" else "S2"])):
                try:bind(a.case(arm),deck.read_bytes(),bad)
                except ValueError:pass
                else:raise AssertionError("seed swap accepted")
            golden[arm]=geom["seed"]
        print("FOUR_FROZEN_DECK_BINDINGS_AND_100_PHASES_OK",golden)

        jobs=[];wait=[];watch=[]
        original_wave=r.wave
        def wave(name):
            a=original_wave(name)
            def setup(arm,*args):
                (a.context(arm)/a.case(arm)).mkdir(parents=True)
            a.setup=setup
            a.environment=lambda:()
            def send(arm,base):
                jid=str(100+len(jobs))
                jobs.append((arm,jid))
                return jid
            a.submit=send
            a.monitor_detached=lambda arm,jid:watch.append((arm,jid))
            return a
        with patch.object(r,"wave",side_effect=wave),patch.object(r.socket,"gethostname",return_value="ibb-master"), \
             patch.object(r,"wait_done",side_effect=lambda j:wait.append(tuple(j))),patch.object(r,"queue",return_value="1|RUNNING|6"):
            r.launch()
            assert [n for n,j in jobs]==["S2U","S2C","S3U","S3C"]
            assert wait==[("373356","373357"),("100","101")] and jobs==watch
            try:r.launch()
            except FileExistsError:pass
            else:raise AssertionError("repeated GO")
        print("STAGED_PAIRS_AND_ONE_GO_OK")

        def row(step,val):
            keys=b.METRICS
            return dict(step=step,n={"SE":100},resolution={"lo":dict.fromkeys(keys,val),"hi":dict.fromkeys(keys,val)},
                        **{g:{k:val} for k,g in keys.items()})
        def arm(v):return dict(steps=b.STEPS,observer={},frames=[row(s,v) for s in b.STEPS])
        pos=b.paired(arm(.1),arm(.2));neg=b.paired(arm(.2),arm(.1));zero=b.paired(arm(.1),arm(.1))
        k="se_frac_in_clusters"
        assert [d[k]["exact_fraction_delta"] for d in (pos,neg,zero)]==["1/10","-1/10","0"]
        rows=[dict(status="OK",seed=s,metrics=m) for s,m in zip([32452843,49979687,67867967],[pos,neg,zero])]
        ag=b.aggregate(rows)
        assert ag["df"]==2 and ag["metrics"][k]["seed_mean_pp"]==0 and not ag["both_practical_directions"]
        rows[-1]["status"]="MISSING"
        assert b.aggregate(rows)["status"]=="NEED_THREE_VALID_SEEDS"
        with redirect_stdout(io.StringIO()):b.main(root,root/"blank_return.json")
        assert b.read(root/"blank_return.json")["comparison"]["status"]=="NEED_THREE_VALID_SEEDS"
        print("SIGNED_PER_SEED_AND_THREE_PAIR_INTERVAL_OK")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("package",type=Path)
    run(ap.parse_args().package)
