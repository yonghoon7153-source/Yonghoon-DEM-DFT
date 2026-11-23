"""Observe the first F12/F24 loading steps with the exact returned pressure trajectories."""
import argparse
import csv
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import tarfile

import numpy as np


PREVIOUS_PIN = "e8e2f2535aa12b9fb089d714e1325d862cb1161b"
PREVIOUS_MANIFEST = "65b61a27d274b8fa0ea4a9892820d450faf972b94b382ff5f3de8dd9f2d57f0f"
RETURN = "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673"
OLD = "docs/reviews/suyoung_floor_fine_20261123/"
NEW = "docs/reviews/suyoung_floor_fine_return_20261123/"
STEPS = {12: 569, 24: 1138}
SAMPLES = {12:(465,569),24:(930,1138)}
BUDGET = {12: 600, 24: 1200}
STAGES = ("floor", "lid", "contact", "grid_change", "particle_change")
COLUMNS = ("step","displacement_code","top_gap_before","floor_gap_before","native_floor_impulse",
           *(stage+"_"+part for stage in STAGES for part in ("all","bottom_row")))


def check(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(root):
    old = root / "history"
    manifest = (old/"SOURCE_SHA256SUMS").read_bytes()
    check(digest(manifest) == PREVIOUS_MANIFEST, "previous execution manifest")
    names = {"history/SOURCE_SHA256SUMS", "RELEASE", NEW+"run_balance.sh", NEW+"early_wall_observer.py"}
    for line in manifest.decode("ascii").splitlines():
        checksum, name = line.split("  ",1)
        check(digest((old/name).read_bytes()) == checksum, name)
        names.add("history/"+name)
    outer = (root/"SOURCE_SHA256SUMS").read_bytes()
    seen = set()
    for line in outer.decode("ascii").splitlines():
        checksum, name = line.split("  ",1)
        check(name in names and name not in seen and digest((root/name).read_bytes())==checksum, name)
        seen.add(name)
    release = (root/"RELEASE").read_text("ascii").strip()
    check(names==seen and re.fullmatch("[0-9a-f]{40}",release) and
          (root/NEW/"early_wall_observer.py").resolve()==Path(__file__).resolve(), "outer source identity")
    spec = importlib.util.spec_from_file_location("pinned_fine", old/OLD/"fine_floor.py")
    fine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fine)
    ctx = fine.context(old)
    check(ctx.identity["release"]==PREVIOUS_PIN, "previous pin")
    return fine, ctx, dict(release=release, observer_sha256=digest(Path(__file__).read_bytes()),
                           manifest_sha256=digest(outer), previous_pin=PREVIOUS_PIN,
                           previous_tar_sha256=RETURN, floor_sha256=ctx.identity["floor_sha256"])


def prior_traces(path, fine, ctx):
    traces = {}
    with path.open("rb") as f:
        check(hashlib.file_digest(f,"sha256").hexdigest()==RETURN, "wrong F12/F24 return")
        f.seek(0)
        with tarfile.open(fileobj=f, mode="r:gz") as t:
            def read(name):
                item = t.getmember("run/"+name)
                check(item.isfile(), name)
                return t.extractfile(item).read()
            check(read("RELEASE").decode("ascii").strip()==PREVIOUS_PIN and
                  digest(read("SOURCE_SHA256SUMS"))==PREVIOUS_MANIFEST and
                  read("screen.txt").splitlines()[-1]==b"COMMAND_RC=0","prior status")
            summary = json.loads(read("summary.json"))
            for n,end in STEPS.items():
                arm = f"F{n}/"
                tr = read(arm+"trace.csv")
                r = json.loads(read(arm+"fine_receipt.json"))
                check(fine.receipt(ctx,n,tr,read(arm+"result.json"),r["floor_audit"])==r==summary["arms"][f"F{n}"]
                      and r["native_steps"]>=end and r["reached_target"], "prior arm receipt")
                traces[n]=b"".join(tr.splitlines(keepends=True)[:end+2])
    return traces


def mass_delta(mass, before, after):
    """Upward impulse on each mass-weighted field node."""
    return mass * (after - before)


def totals(values, low):
    return float(values.sum()), float(values[low].sum())


class Recorder:
    def begin(self):
        self.events=[]
        self.mass=self.gv=self.initial=self.final=self.ids=self.gaps=None
        self.floor_j = 0.
        self.changes = {}

    def floor(self, original, surface, mass, gv):
        check(len(self.events) in (0,3),"floor order")
        if not self.events:
            self.mass, self.gv = mass, gv
            self.initial = gv[:,1].copy()
            self.surface = surface
        check(mass is self.mass and gv is self.gv and surface is self.surface,"floor field identity")
        before=gv[:,1].copy()
        j=original(surface,mass,gv)
        self.record("floor",before)
        self.floor_j+=j
        return j

    def lid(self, original, solver, xy, gv, lid):
        check(len(self.events) in (1,4) and gv is self.gv,"upper wall order")
        if self.gaps is None:
            y=self.surface.boundary.positions[:,1]
            self.gaps=(float(lid-y.max()),float(y.min()-solver.LO))
        before=gv[:,1].copy()
        result=original(solver,xy,gv,lid)
        self.record("lid",before)
        if len(self.events)==5:
            self.final=gv[:,1].copy()
        return result

    def contact(self, original, fields, nodes, mass, grad, gv, centers, friction):
        check(self.events==["floor","lid"] and mass is self.mass and gv is self.gv
              and friction==.5 and fields.shape==mass.shape,"interbody schedule")
        self.ids=fields.copy()
        before=gv[:,1].copy()
        result=original(fields,nodes,mass,grad,gv,centers,friction)
        self.record("contact",before)
        return result

    def record(self, stage, before):
        self.events.append(stage)
        delta=mass_delta(self.mass,before,self.gv[:,1])
        if stage not in self.changes:
            self.changes[stage]=delta
        else:
            self.changes[stage]+=delta

    def finish(self, step, displacement, ids, volume, incoming_y, outgoing_y):
        check(self.events==["floor","lid","contact","floor","lid"],"missing projection")
        # Seed construction uses id=7*i+j with j increasing vertically. Membership follows the disk.
        low=self.ids%7==0
        self.changes["grid_change"]=mass_delta(self.mass,self.initial,self.final)
        row=dict(step=step,displacement_code=displacement,top_gap_before=self.gaps[0],
                 floor_gap_before=self.gaps[1], native_floor_impulse=self.floor_j)
        for stage in STAGES:
            if stage=="particle_change":
                pair=totals(mass_delta(volume,incoming_y,outgoing_y),ids%7==0)
            else:
                pair=totals(self.changes[stage],low)
            row[stage+"_all"],row[stage+"_bottom_row"]=pair
        return row


@contextmanager
def monitor(floor, recorder):
    surface, upper = floor.SurfaceStep.project, floor._other_walls
    floor.SurfaceStep.project=lambda obj,m,v:recorder.floor(surface,obj,m,v)
    floor._other_walls=lambda solver,xy,v,lid:recorder.lid(upper,solver,xy,v,lid)
    try:
        yield
    finally:
        floor.SurfaceStep.project, floor._other_walls=surface, upper


def facts(row, p_mpa, dt, width):
    check(all(math.isfinite(v) for v in row.values()),"nonfinite observer")
    # Momentum impulses use the native solver units throughout. Floor/lid signs apply to the material.
    tol=2.e-12*max(1.,*(abs(row[s+"_"+suf]) for s in STAGES for suf in ("all","bottom_row")))
    check(row["floor_all"] >= -tol and row["lid_all"] <= tol and row["native_floor_impulse"] >= 0.,
          "wall direction")
    check(abs(row["floor_all"]-row["native_floor_impulse"])<=tol and
          math.isclose(row["native_floor_impulse"]/(dt*width)*10., p_mpa, rel_tol=1.e-14,abs_tol=1.e-14),
          "returned floor pressure")
    check(abs(row["contact_all"])<=tol,"interbody sum")
    for suf in ("_all","_bottom_row"):
        demand=sum(row[s+suf] for s in ("floor","lid","contact"))
        check(abs(demand-row["grid_change"+suf])<=tol and
              abs(row["grid_change"+suf]-row["particle_change"+suf])<=tol, "step momentum closure")


class EndPrefix(Exception):
    pass


def check_arm(fine,ctx,identity,previous,cells,folder):
    prefix=(folder/"trace.csv").read_bytes()
    check(prefix==previous[cells],"observed replay changed native raw prefix")
    end=STEPS[cells]
    native=list(csv.DictReader(prefix.decode("ascii").splitlines()))
    raw=(folder/"wall_impulses.csv").read_bytes()
    reader=csv.DictReader(raw.decode("ascii").splitlines())
    check(tuple(reader.fieldnames or ())==COLUMNS and len(native)==end+1,"observer fields")
    rows=[]
    dt=fine.DT[cells]
    for i,r in enumerate(reader, 1):
        check(i<=end and r["step"]==str(i),"observer step")
        row={name:(i if name=="step" else float(v)) for name,v in r.items()}
        check(row["displacement_code"] == ctx.solver.WIDTH-float(native[i]["height"]), "plate position")
        facts(row,10*float(native[i]["bottom_pressure_E"]),dt,ctx.solver.WIDTH)
        rows.append(row)
    check(len(rows)==end,"truncated observer")
    sums={name:math.fsum(r[name] for r in rows) for name in COLUMNS[4:]}
    first_lid=next((r for r in rows if r["lid_all"] < 0.), None)
    first_floor=next((r for r in rows if r["native_floor_impulse"] > 0.), None)
    gap_lid=[r for r in rows if r["top_gap_before"]>1.e-12 and r["lid_all"] < 0.]
    return dict(**identity,cells=cells,steps=end,seconds_limit=BUDGET[cells],dt=dt,width=ctx.solver.WIDTH,
                trace_sha256=digest(prefix),observer_table_sha256=digest(raw),
                impulse_sign="positive upward on the material",bottom_row="initial IDs 0,7,14,21,28,35,42",
                first_lid_down_impulse=first_lid,first_floor_up_impulse=first_floor,
                steps_with_lid_impulse_and_positive_material_gap=len(gap_lid),
                cumulative_lid_impulse_with_positive_material_gap=math.fsum(r["lid_all"] for r in gap_lid),
                snapshots=[rows[i-1] for i in SAMPLES[cells]],signed_impulse_sums=sums,
                u6_qualified=False,stage3_go=False)


def arm(fine,ctx,identity,previous,cells,dest):
    check(not dest.exists() and not dest.is_symlink(),"existing arm")
    init=fine.initial(ctx,cells)
    def take_seed(n):
        nonlocal seeds
        check(n==cells and seeds==0,"seed calls")
        seeds+=1
        return init
    seeds=0
    recorder=Recorder()
    advance_floor=ctx.floor.make_advance(ctx.solver,cells)
    rows=[]
    def contact(*args):
        return recorder.contact(ctx.kernel.project_contacts,*args)
    def advance(*args):
        step=len(rows)+1
        if step>STEPS[cells]:
            raise EndPrefix()
        dt=fine.DT[cells]
        h=ctx.solver.WIDTH-step*dt*ctx.solver.WALL_SPEED
        check(args[-3:]==(cells*10,dt,ctx.solver.LO+h) and args[4] is init[1]
              and args[5] is init[2],"native schedule")
        recorder.begin()
        incoming=args[1][:,1].copy()
        result=advance_floor(*args)
        row=recorder.finish(step,ctx.solver.WIDTH-h,init[1],init[2],incoming,result[1][:,1])
        facts(row,10*result[-1],dt,ctx.solver.WIDTH)
        rows.append(row)
        return result
    try:
        with fine.bind_driver(ctx,take_seed,contact), monitor(ctx.floor,recorder):
            terminal=ctx.driver.run_arm("F",cells,BUDGET[cells],dest,advance=advance)
        raise ValueError("unexpected native terminal "+terminal["status"])
    except EndPrefix:
        check(len(rows)==STEPS[cells] and seeds==1,"prefix schedule")
    with (dest/"wall_impulses.csv").open("x",encoding="ascii",newline="") as f:
        wr=csv.DictWriter(f,COLUMNS,lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    fine.write_json(dest/"balance_receipt.json",check_arm(fine,ctx,identity,previous,cells,dest))


def summarize(fine,ctx,identity,previous,run):
    arms={}
    for n in STEPS:
        dest=run/f"F{n}"
        rec=check_arm(fine,ctx,identity,previous,n,dest)
        check(rec==json.loads((dest/"balance_receipt.json").read_bytes()),"observer receipt")
        arms[n]=rec
    samples=[]
    for i in range(2):
        snapshot={n:arms[n]["snapshots"][i] for n in STEPS}
        check(snapshot[12]["displacement_code"]==snapshot[24]["displacement_code"],"unmatched native snapshot")
        row=dict(displacement_diameters=snapshot[12]["displacement_code"]/.1,steps=[snapshot[n]["step"] for n in STEPS])
        for n,table in snapshot.items():
            scale=10./(fine.DT[n]*ctx.solver.WIDTH)
            row[f"F{n}"]=dict(floor_MPa=table["native_floor_impulse"]*scale,
                        lid_signed_equivalent_MPa=table["lid_all"]*scale,
                        contact_all_signed_equivalent_MPa=table["contact_all"]*scale,
                        contact_bottom_row_signed_equivalent_MPa=table["contact_bottom_row"]*scale,
                        top_gap_diameters=table["top_gap_before"]/.1,
                        bottom_gap_diameters=table["floor_gap_before"]/.1)
        samples.append(row)
    return dict(**identity,status="DEVELOPMENT_MATCHED_PREFIX_BALANCE",arms=arms,samples=samples,
                interpretation="Signed momentum changes under one trajectory; interbody terms redistribute momentum among fields.",
                u6_qualified=False,stage3_go=False,three_dimensional_go=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=("check","arm","summary"))
    for name in ("root","prior"):
        parser.add_argument("--"+name,required=True,type=Path)
    parser.add_argument("--run",type=Path)
    parser.add_argument("--cells",type=int,choices=(12,24))
    a=parser.parse_args()
    fine,ctx,identity=load(a.root)
    prior=prior_traces(a.prior,fine,ctx)
    if a.mode=="check":
        for n in STEPS:
            fine.initial(ctx,n)
        print("BALANCE_SOURCES_AND_REAL_NATIVE_PREFIXES_OK")
        return
    check(a.run is not None and a.run.is_dir(),"run directory")
    for name in ("RELEASE","SOURCE_SHA256SUMS"):
        check((a.root/name).read_bytes()==(a.run/name).read_bytes(),name)
    if a.mode=="arm":
        check(a.cells in STEPS,"missing cells")
        arm(fine,ctx,identity,prior,a.cells,a.run/f"F{a.cells}")
    else:
        fine.write_json(a.run/"summary.json",summarize(fine,ctx,identity,prior,a.run))
        print("EARLY_WALL_BALANCE_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (ArithmeticError,KeyError,IndexError,OSError,RuntimeError,TypeError,ValueError,tarfile.TarError) as e:
        print("INCOMPLETE",type(e).__name__,str(e),file=sys.stderr)
        raise SystemExit(4)
