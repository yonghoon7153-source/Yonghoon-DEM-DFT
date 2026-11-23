"""Measure depth-resolved material momentum at the original plate speed on the frozen trajectory."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import tarfile
from types import SimpleNamespace


DEPTH_PIN = "9638542795ed98edf8b1c9ac52d88c3a0e2f8f3b"
DEPTH_SHA = "cd9b0e6b9ce31719716b3ae4b9f97734a7a4ba3614c7de7bd3d93d44f3be83e6"
MANIFEST = "897480bee4ea3cc329daf6f527596b66f57dea2d16652a76a8f76881cb69407a"
FROZEN = "docs/reviews/suyoung_half_speed_readback_20261123/depth_prefix.py"
STEPS = {12:555, 24:1110}
BUDGET = {12:600, 24:1200}
EVENTS = ((439,878),(481,962),(524,1048),(555,1110))


def require(condition,message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_archive(filename, digest, names):
    with filename.open("rb") as stream:
        require(hashlib.file_digest(stream,"sha256").hexdigest() == digest,"historical archive identity")
        stream.seek(0)
        with tarfile.open(fileobj=stream,mode="r:gz") as tar:
            result = {}
            for name in names:
                member = tar.getmember("run/"+name)
                require(member.isfile(), name)
                result[name]=tar.extractfile(member).read()
            return result


def setup(root, depth_tar, half_tar, material_tar, balance_tar):
    history=root/"history"
    manifest=(history/"SOURCE_SHA256SUMS").read_bytes()
    require(sha(manifest)==MANIFEST and (history/"RELEASE").read_text().strip()==DEPTH_PIN, "depth release")
    for line in manifest.decode("ascii").splitlines():
        digest,name=line.split("  ")
        require(sha((history/name).read_bytes())==digest, "frozen source "+name)
    spec=importlib.util.spec_from_file_location("original_layer_reference",history/FROZEN)
    depth=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(depth)
    half,native,fine,ctx,model,half_prefix,old_id=depth.setup(history,half_tar,material_tar,balance_tar)
    names=["summary.json","RELEASE","SOURCE_SHA256SUMS","screen.txt"]+[f"F{n}/{f}" for n in STEPS
            for f in ("trace.csv","wall_steps.csv","layer_steps.csv","layer_receipt.json")]
    data=read_archive(depth_tar, DEPTH_SHA,names)
    summary=json.loads(data["summary.json"])
    require(summary["status"]=="DEPTH_PREFIX_COMPLETE" and all(summary[k]==v for k,v in old_id.items())
            and data["SOURCE_SHA256SUMS"]==manifest and data["RELEASE"]==(DEPTH_PIN+"\n").encode()
            and data["screen.txt"].splitlines()[-1]==b"COMMAND_RC=0","half-speed depth evidence")
    original=read_archive(material_tar,half.PREVIOUS_RETURN,["summary.json"]+[f"F{n}/{f}" for n in STEPS
                          for f in ("trace.csv","wall_steps.csv")])
    old=json.loads(original["summary.json"])
    refs, half_layers, specs={},{},{}
    for n,end in STEPS.items():
        key=f"F{n}/"
        arm=json.loads(data[key+"layer_receipt.json"])
        require(arm==summary["arms"][str(n)] and sha(data[key+"layer_steps.csv"])==arm["layer_sha256"] and
                (data[key+"trace.csv"],data[key+"wall_steps.csv"])==half_prefix[n][:2],"fixed comparison arm")
        half_layers[n]=[{k:float(v) for k,v in r.items()} for r in native.rows(data[key+"layer_steps.csv"])]
        specs[n]=arm["layer_spec"]
        tr,w=original[key+"trace.csv"],original[key+"wall_steps.csv"]
        require(old["arms"][str(n)]["trace_sha256"]==sha(tr) and old["arms"][str(n)]["wall_csv_sha256"]==sha(w),
                "original material-lid pressure or plate impulses")
        refs[n]=depth.prefix(tr,end+1),depth.prefix(w,end)
    pin=(root/"RELEASE").read_text().strip()
    require(re.fullmatch("[0-9a-f]{40}",pin), "release pin")
    speed=ctx.solver.WALL_SPEED
    require(speed>0 and speed==2*old_id["half_speed"],"original plate speed")
    ident=dict(release=pin,source_sha256=sha((root/"SOURCE_SHA256SUMS").read_bytes()),label="DEVELOPMENT_ONLY",
               half_depth_sha256=DEPTH_SHA,half_return_sha256=depth.HALF_TAR,original_return_sha256=half.PREVIOUS_RETURN,
               balance_return_sha256=native.PRIOR_RESULT,wall_speed=speed,material_lid_release=half.PREVIOUS_RELEASE,
               u6_qualified=False,stage3_go=False,three_dimensional_go=False)
    return SimpleNamespace(depth=depth,half=half,native=native,fine=fine,ctx=ctx,model=model,refs=refs,
                           half_layers=half_layers,specs=specs,identity=ident)


class Observe:
    def __init__(self,depth,base,solver,expected,seed_spec,emit):
        self.depth,self.base,self.emit=depth,base,emit
        self.expected,self.seed_spec=expected,seed_spec
        self.groups=depth.LayerObservation(None,solver.LO,solver.WIDTH,None,None)

    def __getattr__(self,name):
        return getattr(self.base,name)

    def __call__(self,x,v,affine,elastic,ids,mass,grid,dt,lid):
        groups=self.groups
        if groups.labels is None:
            groups.group(x,mass)
            require(groups.spec==self.seed_spec,"initial layer membership, counts or masses")
        p0=float(mass @ v[:,1])
        g0=groups.sampled(v)
        result=self.base(x,v,affine,elastic,ids,mass,grid,dt,lid)
        p1=float(mass @ result[1][:,1])
        g1=groups.sampled(result[1])
        wall=self.base.last_step
        n=wall["step"]
        hist=self.expected[n-1]
        floor,lid=wall["floor_impulse"],wall["lid_signed_impulse"]
        require(hist["step"]==str(n) and float(hist["floor_impulse"])==floor and float(hist["lid_signed_impulse"])==lid,
                "original half-open step wall impulses diverged")
        row=dict(step=n,floor_J=floor,lid_signed_J=lid,whole_before=p0,whole_after=p1,whole_delta=p1-p0,
                 wall_signed_J=math.fsum((floor,lid)))
        for name,a,b in zip(self.depth.LAYERS,g0,g1,strict=True):
            row.update({name+"_before":a,name+"_after":b,name+"_delta":b-a})
        self.depth.check_row(row)
        self.emit(row)
        return result


def verify(e,dest,n):
    trace,walls=e.refs[n]
    require((dest/"trace.csv").read_bytes()==trace and (dest/"wall_steps.csv").read_bytes()==walls,"original native prefix bytes")
    layers=(dest/"layer_steps.csv").read_bytes()
    parsed=e.native.rows(layers)
    wr=e.native.rows(walls)
    require(len(parsed)==len(wr)==STEPS[n],"incomplete original observational rows")
    previous={k:0. for k in (*e.depth.LAYERS,"whole")}
    result=[]
    for i,(raw,ref) in enumerate(zip(parsed,wr,strict=True),1):
        require(tuple(raw)==e.depth.COLUMNS and raw["step"]==str(i),"layer schema and step")
        row={k:float(v) for k,v in raw.items()}
        e.depth.check_row(row)
        require(row["floor_J"]==float(ref["floor_impulse"]) and row["lid_signed_J"]==float(ref["lid_signed_impulse"]),
                "historical plate impulses")
        for name,p in previous.items():
            require(p==row[name+"_before"],"discontinuous material momentum")
            previous[name]=row[name+"_after"]
        result.append(row)
    receipt=dict(e.identity,cell_count=n,layer_spec=e.specs[n],steps=STEPS[n],budget_seconds=BUDGET[n],
                 trace_sha256=sha(trace),wall_sha256=sha(walls),layer_sha256=sha(layers),
                 max_abs_direct_wall_residual_J=max(abs(r["whole_delta"]-r["wall_signed_J"]) for r in result))
    return result,receipt


def arm(e,n,dest):
    file=writer=None
    def emit(row):
        nonlocal file,writer
        if writer is None:
            file=(dest/"layer_steps.csv").open("x",encoding="ascii",newline="")
            writer=csv.DictWriter(file,e.depth.COLUMNS,lineterminator="\n")
            writer.writeheader()
        writer.writerow(row)
    def make(*args,**kwargs):
        base=e.model.make_advance(*args,**kwargs)
        return Observe(e.depth,base,e.ctx.solver,e.native.rows(e.refs[n][1]),e.specs[n],emit)
    core_identity={k:v for k,v in e.identity.items() if k not in ("label","u6_qualified","stage3_go")}
    require(e.ctx.solver.WALL_SPEED==e.identity["wall_speed"],"changed solver speed")
    try:
        with e.half.override(e.native,STEPS=STEPS,BUDGET=BUDGET):
            e.native.run_arm(e.fine,e.ctx,SimpleNamespace(make_advance=make),
                             {k:tr for k,(tr,wall) in e.refs.items()},core_identity,n,dest)
    finally:
        if file is not None:
            file.close()
    _,receipt=verify(e,dest,n)
    e.depth.write_json(dest/"layer_receipt.json",receipt)


def compare(e,original):
    with e.half.override(e.depth,SAMPLES=EVENTS):
        old=e.depth.summarize(original,e.fine.DT,e.ctx.solver.WIDTH)
        half=e.depth.summarize(e.half_layers,e.fine.DT,e.ctx.solver.WIDTH)
    comparisons=[]
    for (a,b),orig,slow in zip(EVENTS,old,half,strict=True):
        t=a*e.fine.DT[12]
        require(t==b*e.fine.DT[24],"matched native clock")
        comparisons.append(dict(F12_step=a,F24_step=b,time_code=t,
             original_travel_D=t*e.identity["wall_speed"]/.1,half_travel_D=t*.5*e.identity["wall_speed"]/.1,
             original=orig,half=slow))
    return comparisons


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("check","arm","summary"))
    for name in ("root","depth","prior","material","baseline"):
        p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--run",type=Path)
    p.add_argument("--cells",type=int,choices=tuple(STEPS))
    a=p.parse_args()
    e=setup(a.root,a.depth,a.prior,a.material,a.baseline)
    for n in STEPS:
        x,_,m=e.fine.initial(e.ctx,n)
        g=e.depth.LayerObservation(None,e.ctx.solver.LO,e.ctx.solver.WIDTH,None,None)
        g.group(x,m)
        require(g.spec==e.specs[n],"original and half layer labels or masses")
    if a.mode=="check":
        print("ORIGINAL_LAYER_SEEDS_CLOCKS_AND_FOUR_RETURNS_OK")
        return
    require(a.run and a.run.is_dir() and all((a.run/k).read_bytes()==(a.root/k).read_bytes()
        for k in ("RELEASE","SOURCE_SHA256SUMS")),"new output identity")
    if a.mode=="arm":
        require(a.cells in STEPS and not (a.run/f"F{a.cells}").exists(),"arm already exists")
        arm(e,a.cells,a.run/f"F{a.cells}")
        return
    series={}
    arms={}
    for n in STEPS:
        dest=a.run/f"F{n}"
        series[n],arms[n]=verify(e,dest,n)
        require(arms[n]==json.loads((dest/"layer_receipt.json").read_bytes()),"observational receipt")
    e.depth.write_json(a.run/"summary.json",dict(e.identity,status="ORIGINAL_LAYER_COMPLETE",arms=arms,
                       at_same_code_time=compare(e,series)))
    print("ORIGINAL_LAYER_NATIVE_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (OSError,KeyError,ValueError,TypeError,RuntimeError,ArithmeticError,IndexError,tarfile.TarError) as exc:
        print("INCOMPLETE",type(exc).__name__,str(exc),file=sys.stderr)
        raise SystemExit(4)
