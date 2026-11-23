"""Read-only Lagrangian layer observer for the frozen half-speed development prefix."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import tarfile
from types import SimpleNamespace

import numpy as np


HALF_PIN = "ba0e2bb980a4f098aee6ee526d069ed2d2446151"
HALF_MANIFEST = "119e5b68641a10bdc2fa68754215e646dbb376593b731653acb8d246e36ba985"
HALF_TAR = "ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863"
HALF_APP = "docs/reviews/suyoung_material_lid_return_20261123/half_speed.py"
STEPS = {12:555, 24:1110}
BUDGET = {12:600, 24:1200}
SAMPLES = ((481,962),(555,1110))
LAYERS = ("lower","middle","upper")
COLUMNS = ("step","floor_J","lid_signed_J","whole_before","whole_after","whole_delta","wall_signed_J")
COLUMNS += tuple(f"{layer}_{field}" for layer in LAYERS for field in ("before","after","delta"))


def check(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def equal(a,b):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b) <= 2e-12*max(1.,abs(a),abs(b))


def write_json(file, value):
    with file.open("x",encoding="ascii",newline="\n") as out:
        json.dump(value,out,sort_keys=True,indent=2,allow_nan=False)
        out.write("\n")


def prefix(raw, rows):
    lines = raw.splitlines(keepends=True)
    check(len(lines) >= rows+1, "missing native rows")
    return b"".join(lines[:rows+1])


def setup(root, prior, material, baseline):
    history = root/"history"
    manifest = (history/"SOURCE_SHA256SUMS").read_bytes()
    check(sha(manifest) == HALF_MANIFEST and (history/"RELEASE").read_text().strip() == HALF_PIN, "frozen speed source")
    for line in manifest.decode("ascii").splitlines():
        digest,path = line.split("  ")
        check(sha((history/path).read_bytes()) == digest, "half-speed source "+path)
    spec = importlib.util.spec_from_file_location("bound_half_speed", history/HALF_APP)
    half = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(half)
    native,fine,ctx,model,material_traces,_,hs_identity = half.setup(history,material,baseline)
    save = {}
    with prior.open("rb") as stream:
        check(hashlib.file_digest(stream,"sha256").hexdigest() == HALF_TAR, "wrong half-speed return")
        stream.seek(0)
        with tarfile.open(fileobj=stream,mode="r:gz") as tar:
            def get(name):
                m=tar.getmember("run/"+name)
                check(m.isfile(),name)
                return tar.extractfile(m).read()
            summary=json.loads(get("summary.json"))
            screen=get("screen.txt").splitlines()
            check(summary["status"]=="HALF_SPEED_PREFIX_COMPLETE" and summary["release"]==HALF_PIN and
                  get("SOURCE_SHA256SUMS")==manifest and get("RELEASE")== (HALF_PIN+"\n").encode() and
                  screen[-1]==b"COMMAND_RC=0" and b"HALF_SPEED_PREFIX_READBACK_COMPLETE" in screen,"previous completion")
            for n,end in STEPS.items():
                base=f"F{n}/"
                tr,wall,motion=(get(base+s) for s in ("trace.csv","wall_steps.csv","particle_momentum.csv"))
                rec=json.loads(get(base+"half_speed_receipt.json"))
                check(summary["arms"][str(n)]==rec and rec["release"]==HALF_PIN and
                      rec["trace_sha256"]==sha(tr) and rec["wall_csv_sha256"]==sha(wall) and
                      rec["particle_momentum_sha256"]==sha(motion),"previous arm binding")
                half.validate_trace(native,material_traces[n],tr,n,ctx.solver.WIDTH,hs_identity["half_wall_speed"],fine.DT[n])
                save[n]=(prefix(tr,end+1),prefix(wall,end),native.rows(prefix(motion,end)))
    pin=(root/"RELEASE").read_text().strip()
    check(re.fullmatch("[0-9a-f]{40}",pin),"current release")
    identity=dict(release=pin,source_sha256=sha((root/"SOURCE_SHA256SUMS").read_bytes()),model_release=HALF_PIN,
                  half_return_sha256=HALF_TAR,material_return_sha256=half.PREVIOUS_RETURN,
                  balance_return_sha256=native.PRIOR_RESULT,half_speed=hs_identity["half_wall_speed"],
                  label="DEVELOPMENT_ONLY",u6_qualified=False,stage3_go=False,three_dimensional_go=False)
    return half,native,fine,ctx,model,save,identity


class LayerObservation:
    """The native driver preserves material-point row order; freeze labels on its first call."""
    def __init__(self, base, floor, width, expected, emit):
        self.base,self.floor,self.width,self.expected,self.emit=base,floor,width,expected,emit
        self.labels=None
        self.spec=None

    def __getattr__(self,name):
        return getattr(self.base,name)

    def group(self,x,mass):
        normalized=(x[:,1]-self.floor)/self.width
        check((np.isfinite(normalized) & (normalized>=0) & (normalized<=1)).all() and
              (np.isfinite(mass) & (mass>0)).all(),"invalid seed coordinates or mass")
        self.labels=np.searchsorted([1/3,2/3],normalized,side="right").astype(np.uint8)
        self.indices=tuple(np.flatnonzero(self.labels==i) for i in range(3))
        self.masses=tuple(mass[ix] for ix in self.indices)
        check(all(len(ix)>0 for ix in self.indices),"empty material layer")
        self.spec=dict(label_sha256=sha(self.labels.tobytes()), counts=[len(ix) for ix in self.indices],
                       masses=[float(m.sum()) for m in self.masses],
                       seed_y_bounds=[self.floor+i*self.width/3 for i in range(4)])

    def sampled(self,v):
        return [float(m @ v[ix,1]) for m,ix in zip(self.masses,self.indices,strict=True)]

    def __call__(self,x,v,affine,elastic,ids,mass,grid,dt,lid):
        if self.labels is None:
            self.group(x,mass)
        before=self.sampled(v)
        initial=float(mass @ v[:,1])
        result=self.base(x,v,affine,elastic,ids,mass,grid,dt,lid)
        after=self.sampled(result[1])
        final=float(mass @ result[1][:,1])
        wall=self.base.last_step
        i=wall["step"]
        ref=self.expected[i-1]
        floor,top=wall["floor_impulse"],wall["lid_signed_impulse"]
        total=math.fsum((floor,top))
        check(ref["step"]==str(i) and initial==float(ref["particle_Py_before"]) and
              final==float(ref["particle_Py_after"]) and total==float(ref["wall_signed_J"]),"historical particle / wall trajectory")
        row=dict(step=i,floor_J=floor,lid_signed_J=top,whole_before=initial,whole_after=final,whole_delta=final-initial,wall_signed_J=total)
        for label,b,a in zip(LAYERS,before,after,strict=True):
            row.update({label+"_before":b,label+"_after":a,label+"_delta":a-b})
        check_row(row)
        self.emit(row)
        return result


def check_row(r):
    check(r["floor_J"]>=0 and r["lid_signed_J"]<=0, "plate impulse signs")
    check(r["wall_signed_J"]==math.fsum((r["floor_J"],r["lid_signed_J"])) and
          r["whole_delta"]==r["whole_after"]-r["whole_before"] and equal(r["wall_signed_J"],r["whole_delta"]),"wall momentum")
    for k in LAYERS:
        check(r[k+"_delta"]==r[k+"_after"]-r[k+"_before"],"layer momentum difference")
    for k in ("before","after","delta"):
        check(equal(math.fsum(r[layer+"_"+k] for layer in LAYERS),r["whole_"+k]),"summed layer "+k)


def verify_arm(native, dest,n, expected):
    trace,wall,ref=expected
    check((dest/"trace.csv").read_bytes()==trace and (dest/"wall_steps.csv").read_bytes()==wall,"native pressure/geometry/wall prefix differs")
    rows=native.rows((dest/"layer_steps.csv").read_bytes())
    history=native.rows(wall)
    check(len(rows)==len(ref)==len(history)==STEPS[n],"incomplete layer prefix")
    result=[]
    for i,(raw,prev,w) in enumerate(zip(rows,ref,history,strict=True),1):
        check(tuple(raw)==COLUMNS and raw["step"]==str(i),"layer rows or columns")
        r={k:float(v) for k,v in raw.items()}
        check_row(r)
        check(r["whole_before"]==float(prev["particle_Py_before"]) and r["whole_after"]==float(prev["particle_Py_after"]) and
              r["floor_J"]==float(w["floor_impulse"]) and r["lid_signed_J"]==float(w["lid_signed_impulse"]), "native momentum / impulses")
        check(all(r[k+"_before"] == (result[-1][k+"_after"] if result else 0.) for k in LAYERS),"layer continuity")
        result.append(r)
    return result


def run_arm(half,native,fine,ctx,model,expected,identity,n,dest):
    observer = output = writer = None
    def emit(row):
        nonlocal output,writer
        if output is None:
            output=(dest/"layer_steps.csv").open("x",newline="",encoding="ascii")
            writer=csv.DictWriter(output,COLUMNS,lineterminator="\n")
            writer.writeheader()
        writer.writerow(row)
    def make(*args,**kwargs):
        nonlocal observer
        observer=LayerObservation(model.make_advance(*args,**kwargs),ctx.solver.LO,ctx.solver.WIDTH,expected[n][2],emit)
        return observer
    prior={j:items[0] for j,items in expected.items()}
    native_identity={k:v for k,v in identity.items() if k not in ("label","u6_qualified","stage3_go")}
    try:
        with half.override(native,STEPS=STEPS,BUDGET=BUDGET),half.override(ctx.solver,WALL_SPEED=identity["half_speed"]):
            native.run_arm(fine,ctx,SimpleNamespace(make_advance=make),prior,native_identity,n,dest)
    finally:
        if output is not None:
            output.close()
    verify_arm(native,dest,n,expected[n])
    check(observer is not None and observer.spec is not None,"missing original material layer membership")
    receipt=dict(identity,cell_count=n,layer_spec=observer.spec,steps=STEPS[n],budget_seconds=BUDGET[n],
                 trace_sha256=sha((dest/"trace.csv").read_bytes()),wall_sha256=sha((dest/"wall_steps.csv").read_bytes()),
                 layer_sha256=sha((dest/"layer_steps.csv").read_bytes()))
    write_json(dest/"layer_receipt.json",receipt)


def window(rows,a,b,dt,width):
    lo,hi=rows[a-1],rows[b-1]
    factor=10/((b-a+1)*dt*width)
    fields=("lower","middle","upper","whole")
    out={k+"_delta_MPa":(hi[k+"_after"]-lo[k+"_before"])*factor for k in fields}
    out.update({k+"_before_Py":lo[k+"_before"] for k in fields})
    out.update({k+"_after_Py":hi[k+"_after"] for k in fields})
    for k in ("floor_J","lid_signed_J"):
        out[k.replace("_J","_MPa")]=math.fsum(r[k] for r in rows[a-1:b])*factor
    return out


def summarize(rows,dt,width):
    data=[]
    for a,b in SAMPLES:
        c=window(rows[12],a,a,dt[12],width)
        f=window(rows[24],b,b,dt[24],width)
        f2=window(rows[24],b-1,b,dt[24],width)
        delta=lambda window: {k:c[k]-window[k] for k in c if k.endswith("_MPa")}
        data.append(dict(steps_F12_F24=[a,b],F12=c,F24=f,F24_equal_duration=f2,F12_minus_F24=delta(f),
                         F12_minus_F24_equal_duration=delta(f2)))
    return data


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode",choices=["check","arm","summary"])
    for name in ("root","prior","material","baseline"):
        cli.add_argument("--"+name,type=Path,required=True)
    cli.add_argument("--cells",type=int,choices=tuple(STEPS))
    cli.add_argument("--run",type=Path)
    args=cli.parse_args()
    half,native,fine,ctx,model,expected,identity=setup(args.root,args.prior,args.material,args.baseline)
    def spec(n):
        x,_,m=fine.initial(ctx,n)
        obs=LayerObservation(None,ctx.solver.LO,ctx.solver.WIDTH,None,None)
        obs.group(x,m)
        return obs.spec
    if args.mode=="check":
        for n in STEPS: spec(n)
        print("DEPTH_PREFIX_SOURCES_SEEDS_AND_RETURNS_OK")
        return
    check(args.run is not None and args.run.is_dir() and all((args.run/k).read_bytes()==(args.root/k).read_bytes()
          for k in ("RELEASE","SOURCE_SHA256SUMS")), "run identity")
    if args.mode=="arm":
        n=args.cells
        check(n in STEPS and not (args.run/f"F{n}").exists(),"existing arm")
        run_arm(half,native,fine,ctx,model,expected,identity,n,args.run/f"F{n}")
        return
    receipts, observed={},{}
    for n in STEPS:
        dest=args.run/f"F{n}"
        observed[n]=verify_arm(native,dest,n,expected[n])
        receipt=json.loads((dest/"layer_receipt.json").read_bytes())
        want=dict(identity,cell_count=n,steps=STEPS[n],layer_spec=spec(n),budget_seconds=BUDGET[n],
                  trace_sha256=sha(expected[n][0]),wall_sha256=sha(expected[n][1]),layer_sha256=sha((dest/"layer_steps.csv").read_bytes()))
        check(half.same(receipt,want),"layer receipt")
        receipts[n]=receipt
    write_json(args.run/"summary.json",dict(identity,status="DEPTH_PREFIX_COMPLETE",arms=receipts,
               observations=summarize(observed,fine.DT,ctx.solver.WIDTH),
               interpretation="Initial material-point thirds; per-layer momentum change includes internal transfers, not interface tractions."))
    print("DEPTH_PREFIX_NATIVE_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (OSError,ValueError,TypeError,KeyError,IndexError,ArithmeticError,RuntimeError,tarfile.TarError) as exc:
        raise SystemExit(f"INCOMPLETE {type(exc).__name__}: {exc}")
