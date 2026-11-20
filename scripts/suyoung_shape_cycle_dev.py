"""Four-disk CPU development cycle with the existing S/F solver and passive shape output."""
import argparse
import csv
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dem_suyoung_sf2d_dev as model

GRID, DT, SPEED, FRICTION = 32, .0005, .15, .20
COUNTS = (1200, 600, 1600, 600)
CLEAR_STEPS = 120
SOLVER_PIN = "00f0a1758349079a10d9c3fe9d1424620117dd27"
KERNEL_SHA256 = "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4"
COLORS = ("#246298", "#cf6727", "#41865e", "#885aa2")


@dataclass(frozen=True)
class PlateStep:
    step: int
    phase: str
    top: float
    velocity: float


def schedule(counts=COUNTS):
    """Same top law as the four-disk loading run; all positions are actual step ends."""
    load, relax, lift, post = counts
    if any(type(k) is not int or k < 1 for k in counts):
        raise ValueError("positive integer durations required")
    compressed = model.TOP0 - SPEED*DT*load
    raised = compressed + SPEED*DT*lift
    if compressed <= model.FLOOR+.25 or raised > 1.:
        raise ValueError("piston travel outside the development domain")
    start = 0
    for phase, n, velocity in (("LOAD",load,-SPEED),("RELAX",relax,0.),
                               ("LIFT",lift,SPEED),("POST_LIFT",post,0.)):
        for j in range(1,n+1):
            if phase == "LOAD":
                top = model.TOP0 - SPEED*DT*j
            elif phase == "LIFT":
                top = compressed + SPEED*DT*j
            else:
                top = compressed if phase == "RELAX" else raised
            yield PlateStep(start+j,phase,top,velocity)
        start += n


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_kernel():
    if sha(Path(model.__file__).read_bytes()) != KERNEL_SHA256:
        raise ValueError("corrected, pinned four-disk kernel bytes required")


def frame_schedule(counts):
    load,relax,lift,post=counts
    return {0:("INITIAL","Initial"), load:("LOAD","Load end"),
            load+relax:("RELAX","Fixed hold end"),
            load+relax+(lift+1)//2:("LIFT","Mid lift"), load+relax+lift:("LIFT","Lift end"),
            load+relax+lift+post:("POST_LIFT","Post-lift end")}


def write_json(path, value):
    with path.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(value,stream,indent=2,allow_nan=False)
        stream.write("\n")


def wall_gaps(x,total,top,grid):
    """Signed top clearance for point centers and the highest carried affine corner."""
    half = .25/grid
    extent_y = half*np.sum(np.abs(total[:,1,:]),axis=1)
    return float(top-np.max(x[:,1])), float(top-np.max(x[:,1]+extent_y))


def release_evidence(rows,required):
    loaded = any(r["phase"]=="LOAD" and r["plate_pressure"]>0 for r in rows)
    following = [r for r in rows if r["phase"]!="LOAD"]
    first_zero = next((r["step"] for r in following if r["plate_pressure"]==0.),None)
    first_gap = next((r["step"] for r in following if r["cell_gap"]>0.),None)
    last_contact = next((r["step"] for r in reversed(rows) if r["plate_pressure"]>0.),None)
    tail = 0
    for r in reversed(following):
        if r["phase"]!="POST_LIFT" or r["plate_pressure"]!=0. or r["cell_gap"]<=0.:
            break
        tail += 1
    return dict(compression_had_positive_reaction=loaded, first_zero_pressure_step=first_zero,
                first_positive_cell_gap_step=first_gap,last_positive_pressure_step=last_contact,
                clear_tail_steps=tail,required_tail_steps=required,
                separated_in_final_window=loaded and tail>=required)


def state_sha(state,total):
    h=hashlib.sha256()
    for a in (state["ids"],state["x"],state["v"],state["C"],state["F"],total):
        h.update(a.tobytes(order="C"))
    return h.hexdigest()


def save_frame(root,state,initial,total,step,phase,top,pressure):
    n=len(initial)
    path=root/f"frame_{step:06d}.npz"
    with path.open("xb") as f:
        np.savez_compressed(f, X=initial, x=state["x"], v=state["v"], C=state["C"],
                            F_elastic=state["F"], F_total=total,
                            particle_id=state["ids"],point_id=np.arange(n,dtype="<i8"),
                            reference_area=np.full(n,(.5/GRID)**2),mass=np.full(n,model.RHO*(.5/GRID)**2),
                            step=np.int64(step),time_code=np.float64(step*DT),top_code=np.float64(top))
    center_gap,cell_gap=wall_gaps(state["x"],total,top,GRID)
    return dict(step=step,time_code=DT*step,phase=phase,top_code=top,file=path.name,
                plate_pressure=pressure,center_gap=center_gap,cell_gap=cell_gap,
                sha256=sha(path.read_bytes()))


def run_arm(arm,out,counts=COUNTS,initialize=model.initial_state,advance=model.step,
            clock=time.monotonic,wall_seconds=570.):
    check_kernel()
    if arm not in ("S","F"):
        raise ValueError("S or F arm required")
    out.mkdir(exist_ok=False,parents=True)
    start=clock()
    load,relax,lift,post=counts
    stops=frame_schedule(counts)
    state=initialize(GRID)
    original_ids=state["ids"].copy()
    initial=state["x"].copy()
    total=np.tile(np.eye(2),(len(initial),1,1))
    frames=[save_frame(out,state,initial,total,0,"INITIAL",model.TOP0,None)]
    transitions=[]
    rows=[]
    phase_end={load,load+relax,load+relax+lift}
    prior=None
    with (out/"trace.csv").open("x",encoding="ascii",newline="") as stream:
        writer=None
        for e in schedule(counts):
            if clock()-start >= wall_seconds:
                raise TimeoutError("arm wall-clock limit")
            if prior is not None:
                boundary=state_sha(state,total)
                if boundary != prior["before_sha256"]:
                    raise ValueError("material state changed across phase boundary")
                transitions.append({**prior,"into":e.phase,"after_sha256":boundary})
                prior=None
            data=advance(state,arm,GRID,DT,e.top,e.velocity,FRICTION)
            if not np.array_equal(original_ids,state["ids"]):
                raise ValueError("particle identity changed")
            total=(np.eye(2)[None,:,:]+DT*state["C"]) @ total
            if not np.isfinite(total).all() or np.any(np.linalg.det(total)<=0):
                raise ValueError("invalid carried affine map")
            center_gap,cell_gap=wall_gaps(state["x"],total,e.top,GRID)
            pressure=float(data["plate_pressure"])
            if not np.isfinite([pressure,center_gap,cell_gap]).all() or pressure<0.:
                raise ValueError("invalid reaction or clearance")
            row=dict(step=e.step,time_code=e.step*DT,phase=e.phase,top=e.top,wall_velocity=e.velocity,
                     plate_pressure=pressure,center_gap=center_gap,cell_gap=cell_gap,
                     kinetic_energy=data["kinetic_energy"],mass=data["mass"],
                     contact_residual=data["residual_closing"],contact_projections=data["pair_node_projections"])
            if writer is None:
                writer=csv.DictWriter(stream,fieldnames=list(row))
                writer.writeheader()
            writer.writerow(row)
            rows.append(row)
            if e.step in stops:
                frames.append(save_frame(out,state,initial,total,e.step,e.phase,e.top,pressure))
            if e.step in phase_end:
                prior=dict(from_phase=e.phase,step=e.step,before_sha256=state_sha(state,total))
    release=release_evidence(rows,CLEAR_STEPS)
    if clock()-start >= wall_seconds:
        raise TimeoutError("arm budget including snapshots")
    result=dict(label="DEVELOPMENT_ONLY",arm=arm,solver_pin=SOLVER_PIN,setting_tested=1,
                selected_setting=None,u6_qualified=False,physical_qualification=False,
                grid=GRID,dt=DT,wall_speed=SPEED,friction=FRICTION,counts=list(counts),
                steps=len(rows),initial_points=len(initial),disk_ids=np.unique(original_ids).tolist(),
                release=release,transitions=transitions,frames=frames,seconds=clock()-start,
                kernel_sha256=sha(Path(model.__file__).read_bytes()),driver_sha256=sha(Path(__file__).read_bytes()),
                trace_sha256=sha((out/"trace.csv").read_bytes()))
    write_json(out/"arm.json",result)
    return result


def svg_series(root,record):
    offsets=.25/GRID*np.array([[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]])
    groups=[[] for _ in COLORS]
    with np.load(root/record["file"],allow_pickle=False) as z:
        if int(z["step"])!=record["step"] or float(z["top_code"])!=record["top_code"]:
            raise ValueError("stored frame does not match its actual step and plate height")
        quad=z["x"][:,None,:]+np.einsum("nij,kj->nki",z["F_total"],offsets)
        for pid,vertices in zip(z["particle_id"],quad):
            coords=" ".join(f"{p[0]:.6f},{p[1]:.6f}" for p in vertices)
            groups[int(pid)].append("M"+coords+"Z")
    # Same-ID affine cells use positive winding and a common colour.
    paths=[]
    for color,commands in zip(COLORS,groups):
        paths.append(f'<path fill="{color}" d="{" ".join(commands)}"/>')
    top=record["top_code"]
    paths.append(f'<path fill="none" stroke="#344651" stroke-width=".006" d="M.1,{top} H.9 M.1,{model.FLOOR} H.9"/>')
    return "".join(paths)


def compare(root):
    check_kernel()
    reports=[]
    for arm in ("S","F"):
        folder=root/arm
        result=json.loads((folder/"arm.json").read_bytes())
        if (result["arm"]!=arm or result["trace_sha256"]!=sha((folder/"trace.csv").read_bytes())
                or result["solver_pin"]!=SOLVER_PIN
                or result["kernel_sha256"]!=sha(Path(model.__file__).read_bytes())
                or result["driver_sha256"]!=sha(Path(__file__).read_bytes())):
            raise ValueError("arm or trace identity mismatch")
        rows=[]
        counts=result["counts"]
        frame_times=frame_schedule(counts)
        expected=[(i,phase) for i,(phase,_) in frame_times.items()]
        if (result["steps"]!=sum(counts)
                or [(f["step"],f["phase"]) for f in result["frames"]]!=expected):
            raise ValueError("required actual phase frames are missing or relabelled")
        with (folder/"trace.csv").open(encoding="ascii",newline="") as f:
            for entry,row in zip(schedule(counts),csv.DictReader(f),strict=True):
                observed=(int(row["step"]),row["phase"],float(row["top"]),float(row["wall_velocity"]),float(row["time_code"]))
                if observed!=(entry.step,entry.phase,entry.top,entry.velocity,entry.step*DT):
                    raise ValueError("actual trace differs from plate schedule")
                reaction,center,gap=(float(row[k]) for k in ("plate_pressure","center_gap","cell_gap"))
                if not np.isfinite([reaction,center,gap]).all() or reaction<0. or gap>center:
                    raise ValueError("invalid stored reaction or clearance")
                rows.append(dict(step=entry.step,phase=entry.phase,plate_pressure=reaction,
                                 center_gap=center,cell_gap=gap,top=entry.top))
        if release_evidence(rows,CLEAR_STEPS)!=result["release"]:
            raise ValueError("release evidence differs from recorded trace")
        for f in result["frames"]:
            if Path(f["file"]).name!=f["file"] or sha((folder/f["file"]).read_bytes())!=f["sha256"]:
                raise ValueError("frame hash or name mismatch")
            step=f["step"]
            expected_top=rows[step-1]["top"] if step else model.TOP0
            if f["time_code"]!=step*DT or f["top_code"]!=expected_top:
                raise ValueError("stored frame timing or height differs from schedule")
            if step and any(f[k]!=rows[step-1][k] for k in ("plate_pressure","cell_gap","center_gap")):
                raise ValueError("frame reaction or clearance differs from its trace")
        reports.append(result)
    keys=("grid","dt","wall_speed","friction","counts","kernel_sha256","driver_sha256","initial_points","disk_ids")
    if any(reports[0][k]!=reports[1][k] for k in keys):
        raise ValueError("arm input mismatch")
    def times(r):
        return [(f["step"],f["time_code"],f["phase"],f["top_code"]) for f in r["frames"]]
    if times(reports[0])!=times(reports[1]):
        raise ValueError("unpaired actual step or plate position")
    with (np.load(root/"S"/reports[0]["frames"][0]["file"],allow_pickle=False) as s,
          np.load(root/"F"/reports[1]["frames"][0]["file"],allow_pickle=False) as f):
        if set(s.files)!=set(f.files) or any(not np.array_equal(s[k],f[k]) for k in s.files):
            raise ValueError("seed snapshot contents differ")
    stage_labels=[caption for phase,caption in frame_schedule(reports[0]["counts"]).values()]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1260 570">',
         '<rect width="1260" height="570" fill="white"/>',
         '<g font-family="sans-serif" fill="#203245">',
         '<text x="38" y="38" font-size="25">Four-disk compression and release</text>',
         '<text x="38" y="68" font-size="18">Actual time steps | affine material cells | normalized 2D development</text>']
    for row,record in enumerate(reports):
        arm=record["arm"]
        svg.append(f'<text x="22" y="{242+row*215}" font-size="22">{arm}</text>')
        for col,frame in enumerate(record["frames"]):
            xpos=52+col*198
            if row==0:
                svg.append(f'<text x="{xpos+4}" y="105" font-size="18">{stage_labels[col]}</text>')
                svg.append(f'<text x="{xpos+4}" y="129" font-size="15">step {frame["step"]}</text>')
            svg.append(f'<g transform="translate({xpos} {330+row*215}) scale(192 -192)">')
            svg.append(svg_series(root/arm,frame))
            svg.append('</g>')
    svg.append('</g></svg>')
    with (root/"shape_pair.svg").open("x",encoding="ascii",newline="\n") as f:
        f.write("\n".join(svg)+"\n")
    both=all(r["release"]["separated_in_final_window"] for r in reports)
    write_json(root/"comparison.json",
               dict(label="DEVELOPMENT_ONLY",solver_pin=SOLVER_PIN,setting_tested=1,
                    selected_setting=None,u6_qualified=False,physical_qualification=False,
                    status="DEVELOPMENT_SEPARATION_OBSERVED" if both else "DEVELOPMENT_SEPARATION_UNRESOLVED",
                    release_by_arm={r["arm"]:r["release"] for r in reports},
                    arm_sha256={r["arm"]:sha((root/r["arm"]/"arm.json").read_bytes()) for r in reports},
                    figure_sha256=sha((root/"shape_pair.svg").read_bytes())))
    return 0 if both else 4


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=("S","F","compare"))
    p.add_argument("output",type=Path)
    args=p.parse_args()
    if args.action=="compare":
        return compare(args.output)
    result=run_arm(args.action,args.output)
    print(json.dumps(result["release"],sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
