"""Short 2D development comparison at one quarter of the original lid speed."""
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
DEPTH_MANIFEST = "897480bee4ea3cc329daf6f527596b66f57dea2d16652a76a8f76881cb69407a"
DEPTH_APP = "docs/reviews/suyoung_half_speed_readback_20261123/depth_prefix.py"
STEPS = {12:2276, 24:4552}
MARKS = {12:(1860,2276), 24:(3720,4552)}
BUDGET = {12:1800, 24:3600}
GAP_TOLERANCE = 2e-12


def require(test, reason):
    if not test:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(file, value):
    with file.open("x", encoding="ascii", newline="\n") as stream:
        json.dump(value, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


def read_archive(path, expected, names):
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream,"sha256").hexdigest() == expected, "unexpected previous return")
        stream.seek(0)
        with tarfile.open(fileobj=stream,mode="r:gz") as archive:
            result = {}
            for name in names:
                item=archive.getmember("run/"+name)
                require(item.isfile(), name)
                result[name]=archive.extractfile(item).read()
            return result


def schedule(original_speed, old_half_speed):
    require(math.isfinite(original_speed) and original_speed>0 and original_speed*.5==old_half_speed, "reference speed")
    return original_speed*.25


def setup(root, depth_tar, half_tar, material_tar, balance_tar):
    history=root/"history"
    manifest=(history/"SOURCE_SHA256SUMS").read_bytes()
    require(sha(manifest)==DEPTH_MANIFEST and (history/"RELEASE").read_text().strip()==DEPTH_PIN,"depth source manifest")
    for line in manifest.decode("ascii").splitlines():
        digest,name=line.split("  ")
        require(sha((history/name).read_bytes())==digest,"frozen source "+name)
    module=importlib.util.spec_from_file_location("frozen_depth_prefix",history/DEPTH_APP)
    depth=importlib.util.module_from_spec(module)
    module.loader.exec_module(depth)
    half,native,fine,ctx,model,clipped,old_id=depth.setup(history,half_tar,material_tar,balance_tar)
    common=["summary.json","screen.txt","RELEASE","SOURCE_SHA256SUMS"]
    data=read_archive(depth_tar,DEPTH_SHA,common+[f"F{n}/{f}" for n in STEPS
        for f in ("layer_receipt.json","trace.csv","wall_steps.csv","layer_steps.csv")])
    receipt=json.loads(data["summary.json"])
    require(receipt["status"]=="DEPTH_PREFIX_COMPLETE" and all(receipt[k]==v for k,v in old_id.items())
            and data["RELEASE"]==(DEPTH_PIN+"\n").encode() and data["SOURCE_SHA256SUMS"]==manifest
            and data["screen.txt"].splitlines()[-1]==b"COMMAND_RC=0","depth completion")
    for n in STEPS:
        key=f"F{n}/"
        arm=json.loads(data[key+"layer_receipt.json"])
        require(arm==receipt["arms"][str(n)] and arm["trace_sha256"]==sha(data[key+"trace.csv"]) and
                arm["wall_sha256"]==sha(data[key+"wall_steps.csv"]) and arm["layer_sha256"]==sha(data[key+"layer_steps.csv"]) and
                (data[key+"trace.csv"],data[key+"wall_steps.csv"])==clipped[n][:2],"depth arm lineage")
    sources={}
    for tag,path,digest in (("original",material_tar,half.PREVIOUS_RETURN),("half",half_tar,depth.HALF_TAR)):
        record=read_archive(path,digest,["summary.json",*[f"F{n}/trace.csv" for n in STEPS]])
        saved=json.loads(record["summary.json"])
        traces={n:record[f"F{n}/trace.csv"] for n in STEPS}
        require(all(sha(raw)==saved["arms"][str(n)]["trace_sha256"] for n,raw in traces.items()),"historical traces")
        sources[tag]=traces
        if tag=="half":
            sources["reference"]=saved["pressure_union"]
    speed=ctx.solver.WALL_SPEED
    quarter=schedule(speed,old_id["half_speed"])
    pin=(root/"RELEASE").read_text().strip()
    require(re.fullmatch("[0-9a-f]{40}",pin),"release")
    identity=dict(release=pin,source_sha256=sha((root/"SOURCE_SHA256SUMS").read_bytes()),original_wall_speed=speed,
                  previous_half_wall_speed=old_id["half_speed"],quarter_wall_speed=quarter,depth_sha256=DEPTH_SHA,
                  half_sha256=depth.HALF_TAR,material_sha256=half.PREVIOUS_RETURN,balance_sha256=native.PRIOR_RESULT)
    return depth,half,native,fine,ctx,model,sources,identity


def checked_trace(half,native,fine,ctx,identity,n,previous,trace):
    with half.override(half, STEPS=STEPS):
        return half.validate_trace(native,previous,trace,n,ctx.solver.WIDTH,identity["quarter_wall_speed"],fine.DT[n])


def onsets(walls, trace, width):
    result={}
    for name,field in (("first_floor_impulse","floor_impulse"),("first_lid_impulse","lid_downward_impulse"),
                       ("first_floor_gap_within_tolerance","floor_gap_after")):
        result[name]=None
        for step, record in enumerate(walls,1):
            v=float(record[field])
            if (v<=GAP_TOLERANCE if field=="floor_gap_after" else v>0.):
                row=trace[step]
                result[name]=dict(step=step,time_code=float(row["time_code"]),
                                  displacement_D=(width-float(row["height"]))/.1,value=v)
                break
    return result


def read_arm(depth,half,native,fine,ctx,identity,cells,dest,previous):
    trace=(dest/"trace.csv").read_bytes()
    raw_wall=(dest/"wall_steps.csv").read_bytes()
    raw_motion=(dest/"particle_momentum.csv").read_bytes()
    raw_layers=(dest/"layer_steps.csv").read_bytes()
    rows=checked_trace(half,native,fine,ctx,identity,cells,previous[cells],trace)
    arm=json.loads((dest/"candidate_receipt.json").read_bytes())
    with half.override(native,STEPS=STEPS):
        wanted=native.receipt(fine,ctx,identity,cells,trace,raw_wall,arm["floor"],arm["lid"])
    require(half.same(arm,wanted),"native quarter receipt")
    walls, observed=native.rows(raw_wall), native.rows(raw_motion)
    layers=native.rows(raw_layers)
    require(len(observed)==len(layers)==len(walls)==STEPS[cells],"momentum observation count")
    before=0.
    motion=[]
    previous_layer={k:0. for k in depth.LAYERS}
    residuals=[]
    for i,(w,m,lr) in enumerate(zip(walls,observed,layers,strict=True),1):
        require(tuple(m)==half.MOMENTUM and m["step"]==str(i) and float(m["particle_Py_before"])==before,"momentum continuity")
        after=float(m["particle_Py_after"])
        row=half.momentum_row(i,before,after,dict(w,step=int(w["step"])))
        require(all(float(m[k])==row[k] for k in half.MOMENTUM[1:]),"direct versus signed impulse")
        require(tuple(lr)==depth.COLUMNS and lr["step"]==str(i),"layer observation sequence")
        layer={k:float(v) for k,v in lr.items()}
        depth.check_row(layer)
        require(layer["whole_before"]==before and layer["whole_after"]==after and layer["whole_delta"]==row["particle_delta_Py"]
                and layer["floor_J"]==float(w["floor_impulse"]) and layer["lid_signed_J"]==float(w["lid_signed_impulse"])
                and all(layer[k+"_before"]==previous_layer[k] for k in depth.LAYERS),"layer and wall histories")
        previous_layer={k:layer[k+"_after"] for k in depth.LAYERS}
        residuals.append(abs(math.fsum(layer[k+"_delta"] for k in depth.LAYERS)-row["particle_delta_Py"]))
        motion.append(row)
        before=after
    seed,_,mass=fine.initial(ctx,cells)
    groups=depth.LayerObservation(None,ctx.solver.LO,ctx.solver.WIDTH,None,None)
    groups.group(seed,mass)
    require(groups.spec==json.loads((dest/"layer_spec.json").read_bytes()),"native initial layer labels")
    receipt=dict(arm,particle_momentum_sha256=sha(raw_motion),particle_momentum_rows=len(motion),native_dt=fine.DT[cells],
                 max_absolute_particle_wall_residual_J=max(abs(m["residual_J"]) for m in motion),
                 layer_sha256=sha(raw_layers),layer_spec=groups.spec,max_layer_sum_residual_J=max(residuals),
                 onsets=onsets(walls,rows,ctx.solver.WIDTH), budget_seconds=BUDGET[cells], status="QUARTER_SPEED_PREFIX_COMPLETE",
                 three_dimensional_go=False)
    return rows,walls,motion,receipt


class LayerAdvance:
    """Sample fixed initial layers on either side of the unchanged native update."""
    def __init__(self, depth, half, base, solver, record):
        self.depth,self.record=depth,record
        self.groups=depth.LayerObservation(None,solver.LO,solver.WIDTH,None,None)
        self.motion=None
        self.base=half.ObservedAdvance(base,self.on_motion)

    def __getattr__(self,name):
        return getattr(self.base,name)

    def on_motion(self,row):
        self.motion=row
        self.record("particle_momentum.csv",row)

    def __call__(self,x,v,affine,elastic,ids,mass,grid,dt,lid):
        if self.groups.labels is None:
            self.groups.group(x,mass)
        before=self.groups.sampled(v)
        self.motion=None
        result=self.base(x,v,affine,elastic,ids,mass,grid,dt,lid)
        after=self.groups.sampled(result[1])
        w=self.base.last_step
        m=self.motion
        require(m is not None and m["step"]==w["step"],"whole observation order")
        row=dict(step=w["step"],floor_J=w["floor_impulse"],lid_signed_J=w["lid_signed_impulse"],
                 whole_before=m["particle_Py_before"],whole_after=m["particle_Py_after"],
                 whole_delta=m["particle_delta_Py"],wall_signed_J=m["wall_signed_J"])
        for k,a,b in zip(self.depth.LAYERS,before,after,strict=True):
            row[k+"_before"],row[k+"_after"],row[k+"_delta"]=a,b,b-a
        self.depth.check_row(row)
        self.record("layer_steps.csv",row)
        return result


def run_arm(depth,half,native,fine,ctx,model,previous,identity,n,dest):
    streams,writers={},{}
    fields={"particle_momentum.csv":half.MOMENTUM,"layer_steps.csv":depth.COLUMNS}
    def record(name,row):
        if name not in writers:
            streams[name]=(dest/name).open("x",newline="",encoding="ascii",buffering=1)
            writers[name]=csv.DictWriter(streams[name],fields[name],lineterminator="\n")
            writers[name].writeheader()
        writers[name].writerow(row)
    observer=None
    def observe(*args,**kwargs):
        nonlocal observer
        require(observer is None,"multiple advance factories")
        observer=LayerAdvance(depth,half,model.make_advance(*args,**kwargs),ctx.solver,record)
        return observer
    def validate(ref,trace,cells):
        return checked_trace(half,native,fine,ctx,identity,cells,ref,trace)
    try:
        with half.override(ctx.solver,WALL_SPEED=identity["quarter_wall_speed"]), \
             half.override(native,STEPS=STEPS,BUDGET=BUDGET,paired_trace=validate):
            native.run_arm(fine,ctx,SimpleNamespace(make_advance=observe),previous,identity,n,dest)
    finally:
        for stream in streams.values():
            stream.close()
    require(observer is not None and observer.groups.spec,"missing layer labels")
    write_json(dest/"layer_spec.json",observer.groups.spec)
    write_json(dest/"quarter_speed_receipt.json",read_arm(depth,half,native,fine,ctx,identity,n,dest,previous)[-1])


def shared_knots(quarter, original_f24, width, reference, anchors):
    shared=[]
    for i,old in enumerate(original_f24):
        a,b=quarter[12][2*i],quarter[24][4*i]
        require(a["height"]==b["height"]==old["height"],"shared height")
        p12,p24=10*float(a["bottom_pressure_E"]),10*float(b["bottom_pressure_E"])
        shared.append(dict(step_F24_original=i,step_F12_quarter=2*i,step_F24_quarter=4*i,
                           displacement_diameters=(width-float(old["height"]))/.1,F12_MPa=p12,F24_MPa=p24,signed_gap_MPa=p12-p24))
    peak=max(shared,key=lambda r:abs(r["signed_gap_MPa"]))
    return dict(samples=len(shared),peak=peak,fixed_reference_percent=100*abs(peak["signed_gap_MPa"])/reference,
                first_above=next((r for r in shared if abs(r["signed_gap_MPa"])>.05*reference),None),
                anchors=[shared[i] for i in anchors])


def compare(half,native,hist,quarter,width):
    earlier={tag:{n:native.rows(raw) for n,raw in hist[tag].items()} for tag in ("original","half")}
    verified=half.compare_speeds(native,earlier["original"],earlier["half"],width)
    require(half.same(hist["reference"],verified),"old speed pair readback")
    shared=shared_knots(quarter,earlier["original"][24],width,native.REF_MPA,native.SAMPLE_STEPS[24])
    with half.override(native,SAMPLE_STEPS=MARKS):
        dense=native.compare(quarter,width)
    require(shared["samples"]==1139 and dense["samples"]==4553,"pressure union counts")
    return dict(original_on_common_1139=verified["original_native_1139"],half_on_common_1139=verified["half_on_original_1139"],
                quarter_on_common_1139=shared,quarter_native_4553=dense)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=("check","arm","summary"))
    for opt in ("root","depth","prior","material","baseline"):
        parser.add_argument("--"+opt,type=Path,required=True)
    parser.add_argument("--run",type=Path)
    parser.add_argument("--cells",type=int,choices=tuple(STEPS))
    args=parser.parse_args()
    depth,half,native,fine,ctx,model,history,identity=setup(args.root,args.depth,args.prior,args.material,args.baseline)
    if args.mode=="check":
        with half.override(ctx.solver,WALL_SPEED=identity["quarter_wall_speed"]):
            for n in STEPS:
                fine.initial(ctx,n)
                require(STEPS[n]==2*half.STEPS[n] and MARKS[n]==tuple(2*i for i in half.MARKS[n]) and
                        ctx.driver.step_size(ctx.solver,n)==fine.DT[n],"native seeds or quarter schedule")
        print("QUARTER_SPEED_SOURCES_SEEDS_AND_RETURNS_OK")
        return
    require(args.run is not None and args.run.is_dir() and
            all((args.root/k).read_bytes()==(args.run/k).read_bytes() for k in ("SOURCE_SHA256SUMS","RELEASE")),"run identity")
    if args.mode=="arm":
        require(args.cells in STEPS and not (args.run/f"F{args.cells}").exists(),"existing arm")
        run_arm(depth,half,native,fine,ctx,model,history["half"],identity,args.cells,args.run/f"F{args.cells}")
        return
    quarter,walls,motion,receipts={},{},{},{}
    for n in STEPS:
        dest=args.run/f"F{n}"
        quarter[n],walls[n],motion[n],receipts[n]=read_arm(depth,half,native,fine,ctx,identity,n,dest,history["half"])
        require(half.same(receipts[n],json.loads((dest/"quarter_speed_receipt.json").read_bytes())),"quarter receipt binding")
    pressure=compare(half,native,history,quarter,ctx.solver.WIDTH)
    result=dict(identity,label="DEVELOPMENT_ONLY",status="QUARTER_SPEED_PREFIX_COMPLETE", speed_fraction=.25,
                arms=receipts,reference_MPa=native.REF_MPA,pressure_union=pressure,u6_qualified=False,stage3_go=False,
                three_dimensional_go=False,quarter_fixed_windows=half.fixed_windows(walls,motion,MARKS,ctx.solver.WIDTH,fine.DT))
    write_json(args.run/"summary.json",result)
    print("QUARTER_SPEED_NATIVE_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (OSError,ValueError,RuntimeError,ArithmeticError,TypeError,IndexError,KeyError,tarfile.TarError) as exc:
        print("INCOMPLETE",type(exc).__name__,str(exc),file=sys.stderr)
        raise SystemExit(4)
