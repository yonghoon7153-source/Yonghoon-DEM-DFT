"""Fixed-displacement development branch from the reproduced quarter-speed peak."""
import argparse
from contextlib import ExitStack
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import time
from types import ModuleType, SimpleNamespace

import numpy as np


QUARTER = "5bee9a0cc9f92ba88fd7039444c7efb71bb8946c84912159d6a23838f8399d04"
QUARTER_PIN = "4a56e468c931e024d08f5476df9ccb0237694741"
QUARTER_MANIFEST = "8d8f1cd80492f264857a459ce8775da93cd7adb2330d224dc83699e2c88391de"
QUARTER_APP = "docs/reviews/suyoung_depth_readback_20261123/quarter_speed.py"
LID_SOURCE = "34ba6abab29c1c05661002aa7d6f946f60b78770c0aacd7ad6f5d3fc652212e5"
STATIONARY_SOURCE = "c0b806e68633eacd2704e3c2c94ae6f1d0cc1fc8cb870b425651750a75dbd856"
RAMP = {12:1638, 24:3276}
HOLD = {12:1200, 24:2400}
BUDGET = {12:1800, 24:4500}
TRACE = ("step","time_code","height","bottom_pressure_E","phi_m")
ENERGY = ("step","phase","plate_speed","particle_ke","vertical_ke","max_particle_speed")
OBS = ("trace.csv","wall_steps.csv","layer_steps.csv","particle_momentum.csv")
LAYERS = ("lower","middle","upper")
SCOPE = dict(label="DEVELOPMENT_ONLY",u6_qualified=False,stage3_go=False,three_dimensional_go=False)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def stationary_source(source):
    # Only the stationary clock is specialized. Position/impulse/projection checks
    # and the actual constitutive/contact operation retain the pinned implementation.
    old = b"or dt <= 0. or speed <= 0.:"
    new = b"or dt <= 0. or speed != 0. or lid != self.previous_lid:"
    require(digest(source) == LID_SOURCE and source.count(old) == 1, "moving lid source or guard")
    held = source.replace(old,new,1)
    require(digest(held) == STATIONARY_SOURCE, "stationary guard derivation")
    return held


def stationary_call(model):
    path = Path(model.__file__)
    source = stationary_source(path.read_bytes())
    module = ModuleType("pinned_stationary_material_lid")
    module.__file__ = str(path)
    exec(compile(source,str(path),"exec"),module.__dict__)
    return module.MaterialLidAdvance.__call__


def prefix(raw, rows):
    lines = raw.splitlines(keepends=True)
    require(0 < rows < len(lines), "missing native rows")
    return b"".join(lines[:rows+1])


def setup(args):
    hist = args.root/"history"
    manifest = (hist/"SOURCE_SHA256SUMS").read_bytes()
    require(digest(manifest) == QUARTER_MANIFEST and (hist/"RELEASE").read_text().strip() == QUARTER_PIN, "quarter source")
    for line in manifest.decode().splitlines():
        h, name = line.split("  ")
        require(digest((hist/name).read_bytes()) == h, "frozen source: "+name)
    spec = importlib.util.spec_from_file_location("attested_quarter",hist/QUARTER_APP)
    q = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(q)
    depth,half,native,fine,ctx,model,_,ref = q.setup(hist,args.depth,args.prior,args.material,args.baseline)
    names = ["RELEASE","SOURCE_SHA256SUMS","screen.txt","summary.json"]
    names += [f"F{n}/{f}" for n in RAMP for f in (*OBS,"quarter_speed_receipt.json")]
    data = q.read_archive(args.quarter,QUARTER,names)
    s = json.loads(data["summary.json"])
    require(s["status"] == "QUARTER_SPEED_PREFIX_COMPLETE" and all(s[k] == v for k,v in ref.items())
            and data["RELEASE"] == (QUARTER_PIN+"\n").encode() and data["SOURCE_SHA256SUMS"] == manifest
            and data["screen.txt"].splitlines()[-1] == b"COMMAND_RC=0", "quarter return identity")
    peak = s["pressure_union"]["quarter_on_common_1139"]["peak"]
    previous = {}
    receipts = {}
    speed = ref["quarter_wall_speed"]
    for n in RAMP:
        receipts[n] = rec = json.loads(data[f"F{n}/quarter_speed_receipt.json"])
        require(rec == s["arms"][str(n)] and peak[f"step_F{n}_quarter"] == RAMP[n], "quarter peak")
        keys = ("trace_sha256","wall_csv_sha256","layer_sha256","particle_momentum_sha256")
        previous[n] = {name:data[f"F{n}/{name}"] for name in OBS}
        require(all(digest(previous[n][name]) == rec[k] for name,k in zip(OBS,keys,strict=True)), "quarter observations")
        with half.override(ctx.solver,WALL_SPEED=speed):
            fine.initial(ctx,n)
        require(fine.DT[n] > 0 and HOLD[n]*fine.DT[n] == HOLD[12]*fine.DT[12], "matched hold duration")
    pin = (args.root/"RELEASE").read_text().strip()
    require(re.fullmatch("[a-f0-9]{40}",pin) is not None, "release")
    return SimpleNamespace(q=q, depth=depth, half=half, native=native, fine=fine, ctx=ctx, model=model,
        stationary=stationary_call(model), old=previous, old_receipts=receipts, speed=speed,
        identity=dict(release=pin,source_sha256=digest((args.root/"SOURCE_SHA256SUMS").read_bytes()),
                      quarter_return_sha256=QUARTER,quarter_release=QUARTER_PIN,
                      moving_lid_source=LID_SOURCE,stationary_clock_variant=STATIONARY_SOURCE, **SCOPE))


class PhaseLid:
    """Retain the material markers and contact state on the original object in both phases."""
    def __init__(self, base, fixed_call):
        self.base,self.fixed_call = base,fixed_call
        self.fixed = None

    def __getattr__(self,name):
        return getattr(self.base,name)

    def hold(self, lid):
        require(self.fixed is None and self.base.previous_lid == lid and not self.base.failed, "invalid handover")
        self.fixed = lid

    def __call__(self,*args):
        if self.fixed is None:
            return self.base(*args)
        require(args[-1] == self.fixed and self.base.previous_lid == self.fixed and self.base.solver.WALL_SPEED == 0.,
                "held lid drifted")
        return self.fixed_call(self.base,*args)


def energy(v, mass):
    squared = np.einsum("ij,ij->i",v,v)
    total = .5*float(mass @ squared)
    vertical = .5*float(mass @ (v[:,1]*v[:,1]))
    vmax = math.sqrt(float(np.max(squared)))
    require(all(math.isfinite(f) and f>=0. for f in (total,vertical,vmax)) and vertical<=total+1e-13, "particle energy")
    return total,vertical,vmax


def write_rows(path, columns, stack, trace=False):
    stream = stack.enter_context(path.open("x",newline="",encoding="ascii"))
    writer = csv.writer(stream,lineterminator="\r\n" if trace else "\n")
    writer.writerow(columns)
    return stream,writer


def state_hashes(x,v,C,F,markers,ids,mass):
    return {name:digest(a.tobytes(order="C")) for name,a in
            (("x",x),("v",v),("affine",C),("elastic",F),("boundary",markers),("ids",ids),("mass",mass))}


def observed_prefix(dest,ref,n):
    result = {}
    for name in OBS:
        rows = RAMP[n] + int(name=="trace.csv")
        want = prefix(ref[name],rows)
        seen = prefix((dest/name).read_bytes(),rows)
        require(want==seen, "quarter trajectory differs before fork: "+name)
        result[name] = digest(seen)
    return result


def run_arm(e,n,dest):
    start = time.monotonic()
    dest.mkdir(exist_ok=False)
    s = e.ctx.solver
    dt = e.fine.DT[n]
    with e.half.override(s,WALL_SPEED=e.speed):
        x,ids,mass = e.fine.initial(e.ctx,n)
    v = np.zeros_like(x)
    C = np.zeros((len(x),2,2))
    F = np.broadcast_to(np.eye(2),C.shape).copy()
    total = float(mass.sum())
    boundary = PhaseLid(e.model.make_advance(s,n,floor_module=e.ctx.floor),e.stationary)
    completed = contacts = 0
    fork, fork_height = {}, s.WIDTH-dt*RAMP[n]*e.speed
    def contact(*args):
        nonlocal contacts
        require(contacts==completed and args[-1]==.5, "projection schedule")
        result = e.ctx.kernel.project_contacts(*args)
        contacts += 1
        return result
    # The native driver uses this hook on each substep. The explicit two-phase
    # clock below reproduces the original one through the fork. It never reseeds.
    with ExitStack() as st:
        columns = {"trace.csv":TRACE,"wall_steps.csv":e.native.WALL_COLUMNS,"layer_steps.csv":e.depth.COLUMNS,
                   "particle_momentum.csv":e.half.MOMENTUM,"energy.csv":ENERGY}
        outputs = {k:write_rows(dest/k,cols,st,trace=(k=="trace.csv")) for k,cols in columns.items()}
        def record(name,row):
            outputs[name][1].writerow(row[k] for k in columns[name])
        observed = e.q.LayerAdvance(e.depth,e.half,boundary,s,record)
        st.enter_context(e.half.override(s,project_contacts=contact))
        outputs["trace.csv"][1].writerow((0,0,s.WIDTH,0,total/s.WIDTH**2))
        outputs["energy.csv"][1].writerow((0,"initial",e.speed,0,0,0))
        for phase,steps,wall_speed in (("compression",RAMP[n],e.speed),("hold",HOLD[n],0.)):
            with e.half.override(s,WALL_SPEED=wall_speed):
                if phase=="hold":
                    boundary.hold(s.LO+fork_height)
                    require(fork["state_sha256"] == state_hashes(x,v,C,F,boundary.positions,ids,mass), "fork state continuity")
                for _ in range(steps):
                    step=completed+1
                    require(time.monotonic()-start<BUDGET[n], "arm time limit")
                    height=s.WIDTH-dt*step*e.speed if phase=="compression" else fork_height
                    x,v,C,F,p = observed(x,v,C,F,ids,mass,10*n,dt,s.LO+height)
                    require(contacts==step and math.isfinite(p) and p>=0., "step count or reaction")
                    require(phase!="compression" or p<s.TARGET, "unexpected native compression stop")
                    outputs["trace.csv"][1].writerow((step,step*dt,height,p,total/(s.WIDTH*height)))
                    outputs["energy.csv"][1].writerow((step,phase,wall_speed,*energy(v,mass)))
                    record("wall_steps.csv",boundary.last_step)
                    completed=step
                if phase=="compression":
                    for stream,_ in outputs.values():
                        stream.flush()
                    fork = dict(prefix_sha256=observed_prefix(dest,e.old[n],n), step=completed, height=height,
                                state_sha256=state_hashes(x,v,C,F,boundary.positions,ids,mass))
        require(time.monotonic()-start<=BUDGET[n] and contacts==RAMP[n]+HOLD[n], "incomplete arm")
    e.q.write_json(dest/"layer_spec.json",observed.groups.spec)
    with e.half.override(e.native,STEPS={k:RAMP[k]+HOLD[k] for k in RAMP}):
        audit=e.native.receipt(e.fine,e.ctx,{},n,(dest/"trace.csv").read_bytes(),(dest/"wall_steps.csv").read_bytes(),
                               boundary.audit,boundary.lid_audit)
    record = dict(e.identity,status="HOLD_ARM_COMPLETE",grid=n,budget_seconds=BUDGET[n],fork=fork,
                  floor=audit["floor"],lid=audit["lid"],hashes={k:digest((dest/k).read_bytes()) for k in (*OBS,"energy.csv","layer_spec.json")})
    e.q.write_json(dest/"hold_receipt.json",record)


def mean(values):
    return math.fsum(values)/len(values)


def window(wall, layers, energies, dt, width):
    require(len(wall)==len(layers)>0 and (energies is None or len(energies)==len(wall)),"window length")
    scale=10/(dt*width)
    floor=[float(r["floor_impulse"])*scale for r in wall]
    lid=[float(r["lid_downward_impulse"])*scale for r in wall]
    stats=dict(samples=len(wall),floor_mean_MPa=mean(floor),lid_mean_MPa=mean(lid),
               floor_range_MPa=[min(floor),max(floor)],lid_range_MPa=[min(lid),max(lid)],
               floor_minus_lid_mean_MPa=mean(floor)-mean(lid),
               floor_positive_steps=sum(f>0. for f in floor),lid_positive_steps=sum(p>0. for p in lid),
               floor_gap_range=[min(float(r["floor_gap_after"]) for r in wall),max(float(r["floor_gap_after"]) for r in wall)],
               upper_gap_range=[min(float(r["top_gap_after"]) for r in wall),max(float(r["top_gap_after"]) for r in wall)])
    for name in (*LAYERS,"whole"):
        stats[name+"_delta_Py_MPa"]=scale*mean([float(r[name+"_delta"]) for r in layers])
    require(abs(stats["whole_delta_Py_MPa"]-stats["floor_minus_lid_mean_MPa"])<5e-10,"mean material momentum balance")
    if energies is not None:
        for k in ("particle_ke","vertical_ke","max_particle_speed"):
            vals=[float(r[k]) for r in energies]
            require(all(math.isfinite(x) and x>=0. for x in vals),"invalid material kinetic energy")
            stats[k]=dict(mean=mean(vals),min=min(vals),max=max(vals),last=vals[-1])
    return stats


def read_arm(e,n,dest):
    rec=json.loads((dest/"hold_receipt.json").read_bytes())
    require(rec["status"]=="HOLD_ARM_COMPLETE" and rec["grid"]==n and all(rec[k]==v for k,v in e.identity.items()),"arm receipt")
    require(set(rec["hashes"])==set((*OBS,"energy.csv","layer_spec.json")) and
            all(rec["hashes"][name]==digest((dest/name).read_bytes()) for name in rec["hashes"]), "arm members")
    require(rec["fork"]["prefix_sha256"]==observed_prefix(dest,e.old[n],n) and
            json.loads((dest/"layer_spec.json").read_bytes())==e.old_receipts[n]["layer_spec"],"fork inputs")
    ts,wr,ls,ms,ke=[e.native.rows((dest/name).read_bytes()) for name in (*OBS,"energy.csv")]
    count=RAMP[n]+HOLD[n]
    require(len(ts)==len(ke)==len(wr)+1==len(ls)+1==len(ms)+1==count+1,"observation count")
    dt=e.fine.DT[n]
    width=e.ctx.solver.WIDTH
    fixed=width-dt*RAMP[n]*e.speed
    require(rec["fork"]["height"]==fixed and rec["fork"]["step"]==RAMP[n] and set(rec["fork"]["state_sha256"])==
            {"x","v","affine","elastic","boundary","ids","mass"} and
            all(re.fullmatch("[a-f0-9]{64}",v) for v in rec["fork"]["state_sha256"].values()),"fork state receipt")
    with e.half.override(e.native,STEPS={k:RAMP[k]+HOLD[k] for k in RAMP}):
        e.native.receipt(e.fine,e.ctx,{},n,(dest/"trace.csv").read_bytes(),(dest/"wall_steps.csv").read_bytes(),rec["floor"],rec["lid"])
    prior_py=0.
    prior_layers={k:0. for k in LAYERS}
    for i in range(1,count+1):
        moving=i<=RAMP[n]
        r,energy_row,m,w,layer=ts[i],ke[i],ms[i-1],wr[i-1],ls[i-1]
        expected_height=width-dt*i*e.speed if moving else fixed
        require(float(r["height"])==expected_height and float(r["time_code"])==i*dt and
                energy_row["phase"]==("compression" if moving else "hold") and float(energy_row["plate_speed"])==(e.speed if moving else 0.)
                and all(int(x["step"])==i for x in (r,energy_row,m,w,layer)), "motion clock drift")
        require(all(math.isfinite(float(energy_row[k])) and float(energy_row[k])>=0. for k in ENERGY[3:])
                and float(energy_row["vertical_ke"])<=float(energy_row["particle_ke"])+1e-13,"invalid translational energy")
        motion=e.half.momentum_row(i,prior_py,float(m["particle_Py_after"]),dict(w,step=i))
        require(all(float(m[k])==motion[k] for k in e.half.MOMENTUM),"particle vs signed wall impulse")
        vals={k:float(v) for k,v in layer.items()}
        e.depth.check_row(vals)
        require(vals["whole_before"]==prior_py and vals["whole_after"]==motion["particle_Py_after"] and
                vals["floor_J"]==float(w["floor_impulse"]) and vals["lid_signed_J"]==float(w["lid_signed_impulse"])
                and all(vals[k+"_before"]==prior_layers[k] for k in LAYERS),"direct layer continuity")
        prior_py=motion["particle_Py_after"]
        prior_layers={k:vals[k+"_after"] for k in LAYERS}
    mult=n//12
    windows={}
    # Both late windows span 300 F12 steps at identical model times. Continued
    # loading was recorded for just 638 coarse steps beyond the common fork.
    for name,start,end in (("first_300",0,300),("overlap_last_300",300,600),("late_1",600,900),("late_2",900,1200)):
        lo=RAMP[n]+start*mult
        hi=RAMP[n]+end*mult
        result=window(wr[lo:hi],ls[lo:hi],ke[lo+1:hi+1],dt,width)
        result.update(first_step=lo+1,last_step=hi,time_since_stop=[start*mult*dt,end*mult*dt])
        windows[name]=result
    old_w=e.native.rows(e.old[n]["wall_steps.csv"])
    old_l=e.native.rows(e.old[n]["layer_steps.csv"])
    for name,start,end in (("first_300",0,300),("overlap_last_300",300,600)):
        lo=RAMP[n]+start*mult
        hi=RAMP[n]+end*mult
        windows[name]["continued_compression_equal_time_different_height"]=window(old_w[lo:hi],old_l[lo:hi],None,dt,width)
    return dict(receipt=rec,windows=windows,fork_energy=ke[RAMP[n]],
                final_energy=ke[-1],locked_height=fixed,hold_time=HOLD[n]*dt)


def summarize(e, run):
    arms={n:read_arm(e,n,run/f"F{n}") for n in RAMP}
    require(arms[12]["locked_height"]==arms[24]["locked_height"] and arms[12]["hold_time"]==arms[24]["hold_time"],
            "unequal hold history")
    gaps={}
    for name in ("first_300","overlap_last_300","late_1","late_2"):
        a,b=arms[12]["windows"][name],arms[24]["windows"][name]
        require(a["time_since_stop"]==b["time_since_stop"],"window times differ")
        cols=("floor_mean_MPa","lid_mean_MPa","whole_delta_Py_MPa",*(k+"_delta_Py_MPa" for k in LAYERS))
        gaps[name]={k:a[k]-b[k] for k in cols}
    summary=dict(e.identity,status="HOLD_PAIR_COMPLETE",arms=arms,F12_minus_F24_equal_time=gaps,
                 reference_MPa=e.native.REF_MPA, qualification_basis="fixed_height_transient_development_only")
    e.q.write_json(run/"summary.json",summary)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("check","arm","summary"))
    for name in ("root","quarter","depth","prior","material","baseline"):
        p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--cells",type=int,choices=(12,24))
    p.add_argument("--run",type=Path)
    a=p.parse_args()
    e=setup(a)
    if a.mode=="check":
        print("HOLD_PAIR_FORK_AND_FIVE_RETURNS_OK")
        return
    require(a.run is not None and a.run.is_dir() and all((a.root/k).read_bytes()==(a.run/k).read_bytes() for k in ("RELEASE","SOURCE_SHA256SUMS")),
            "run source binding")
    if a.mode=="arm":
        require(a.cells in RAMP,"missing cells")
        run_arm(e,a.cells,a.run/f"F{a.cells}")
    else:
        summarize(e,a.run)
        print("HOLD_PAIR_NATIVE_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (ArithmeticError,IndexError,KeyError,OSError,RuntimeError,TypeError,ValueError) as error:
        print("INCOMPLETE",type(error).__name__,str(error),file=sys.stderr)
        raise SystemExit(4)
