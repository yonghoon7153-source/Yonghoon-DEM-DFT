"""Selected-setting Q13. Prior curves are replayed; only the two 36-cell arms are new."""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import tarfile
from types import ModuleType

S_PATH = "docs/reviews/suyoung_u6b_setting2_20261123/setting2_u6b.py"
HIST_MANIFEST = "7647ce296cffe72d4776ce33b8201fd97ca2266bb549e6c479a100802e25eb4b"
FLOOR = "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b"
DT = 0.0004991926703287907
POINTS = 198597
SEEDS = ("9f8933b9cb8016a4e173d74109bf48f4d87507f07e7c3e78520ca22b47ad035e",
         "b65eb9e75f7ec625d4ec6888dc5fd344b34b3393c5bbd2424ecf3d9c6efe4a3d",
         "5c7b447c3b83887d1a044237cc37bfdd00ff20dfb676010b7827869526f9a4b4")
BUDGET = {"S": 28800, "F": 21600}
THREADS = ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","BLIS_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS")

def need(condition, reason):
    if not condition:
        raise ValueError(reason)

def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write("\n")

def context(root, arm):
    original = root/"baseline"
    s = load(original/S_PATH)
    need(sha((original/"SOURCE_SHA256SUMS").read_bytes()) == HIST_MANIFEST, "S baseline manifest")
    e = s.context(original)
    raw = Path(e.ctx.floor.__file__).read_bytes()
    guard = b"cells not in (8, 12, 16, 24) or not"
    need(sha(raw) == FLOOR and raw.count(guard) == 1, "material floor identity")
    floor = ModuleType("original_floor_with_36_allowed")
    floor.__file__ = e.ctx.floor.__file__
    expanded = raw.replace(guard,b"cells not in (8, 12, 16, 24, 36) or not")
    exec(compile(expanded,floor.__file__,"exec"),floor.__dict__)
    e.ctx = e.ctx._replace(floor=floor)
    e.ctx.driver.GRIDS = (*e.ctx.driver.GRIDS,36)
    e.fine.POINTS[36], e.fine.DT[36], e.fine.SEEDS[36] = POINTS, DT, SEEDS
    e.gate.BUDGET[36] = BUDGET[arm]
    e.gap = s.load(original/"history"/s.A_DIR/"gap_kernel.py")
    e.identity.update(release=(root/"RELEASE").read_text().strip(),
                      source_manifest_sha256=sha((root/"SOURCE_SHA256SUMS").read_bytes()),
                      gate="U6(b)-Q13",s_baseline_sha256=HIST_MANIFEST,
                      original_material_floor_sha256=FLOOR,extended_floor_sha256=sha(expanded))
    return s,e

def history(root, sdir, fdir):
    h = load(root/"history_reader.py")
    prior = h.readback(sdir,fdir)
    need(prior["setting"] == 2 and prior["grid_order"] == [8,12,16,24] and
         prior["return_sha256"] == h.S_RETURN[1] and prior["reused_f_return_sha256"] == h.F_RETURN[1],
         "wrong original returns")
    # Use the native values after independent target interpolation has verified them.
    with tarfile.open(sdir/h.S_RETURN[0],"r:gz") as archive:
        old = json.load(archive.extractfile("run/summary.json"))
    rows = {}
    hashes = {}
    for arm in ("S","F"):
        for n in (12,16,24):
            key = arm+str(n)
            row = old["inputs"][key]
            need(row["trace_sha256"] == prior["trace_sha256"][key], "reused trace binding")
            rows[arm,n] = row["points"]
            hashes[key] = row["trace_sha256"]
    return rows,hashes,{"S":h.S_RETURN[1],"F":h.F_RETURN[1]}

def decision(targets):
    def resolved(point):
        data = targets[point]
        intervals = [data["arms"][a]["ln_pressure_interval"] for a in ("S","F")]
        intervals.append(data["ln_S_over_F_interval_report_only"])
        return data["common"] is True and all(isinstance(v,list) and len(v)==2 and
                    all(isinstance(x,(float,int)) and math.isfinite(x) for x in v) and v[0]<=v[1]
                    for v in intervals)
    if not all(resolved(p) for p in ("0.84","0.90")):
        return "CLOSE_2D_UNDISTINGUISHED"
    if targets["0.95"]["common"] and not resolved("0.95"):
        return "HOLD_OTHER_COMMON_POINT"
    return "PREPARE_STAGE3_REVIEW"

def check_shifted_reader(root):
    """Exercise the packaged decision on artificial pressures, without an MPM step."""
    rules=load(root/"rules/suyoung_u6b36_dev.py").legacy
    rows={}
    for arm,scale in (("S",1.3),("F",1.)):
        for n,pressure in zip((12,16,24,36),(.85,.7,.5,math.sqrt(.5**3/.7)),strict=True):
            rows[arm,n]={k:{"state":"VALUE","pressure_MPa":scale*pressure} for k in ("0.84","0.90","0.95")}
    targets=rules.compare(rows)["targets"]
    sample=targets["0.84"]
    need(decision(targets)=="PREPARE_STAGE3_REVIEW" and
         all(sample["arms"][a]["resolution"]["rule"]=="A" for a in ("S","F")),"shifted A comparison")
    si=sample["arms"]["S"]["ln_pressure_interval"]
    fi=sample["arms"]["F"]["ln_pressure_interval"]
    need(sample["ln_S_over_F_interval_report_only"]==[si[0]-fi[1],si[1]-fi[0]],"interval subtraction")
    rows["F",36]["0.90"]=rows["F",24]["0.90"]
    need(decision(rules.compare(rows)["targets"])=="CLOSE_2D_UNDISTINGUISHED","primary stop rule")

def f_receipt(e,folder):
    result_raw=(folder/"result.json").read_bytes()
    obs_raw=(folder/"observation.json").read_bytes()
    result,obs=json.loads(result_raw),json.loads(obs_raw)
    if result["status"]=="TARGET_BRACKETED":
        return e.gate.target_receipt(e,36,folder,obs,DT,list(SEEDS),POINTS)
    # A real geometric endpoint is a valid U6(b) loading trace even when the
    # U6(a) caliper (defined at 1.2 MPa) has no value.
    trace=(folder/"trace.csv").read_bytes()
    expected=dict(arm="F",cells=36,setting=2,protocol=e.gate.PROTOCOL,origin="new",
                  status="GEOMETRY_LIMIT",source_sha256=e.ctx.driver.SOURCE,points_count=POINTS,
                  budget_s=BUDGET["F"],trace_sha256=sha(trace),label="DEVELOPMENT_ONLY")
    need(all(result.get(k)==v for k,v in expected.items()) and
         0<=result["elapsed_s"]<=BUDGET["F"]+30,"F native geometry result")
    _,ps=e.ctx.compare.read_native(trace,e.ctx.solver.WIDTH,e.ctx.solver.WALL_SPEED,DT,result["status"])
    n=len(ps)-1
    audit=obs["floor"]
    gap=e.gap.GapProjector(e.ctx.kernel).metadata()
    gap["calls"]=n
    need(obs["identity"]==e.identity and obs["geometry_sha256"]==list(SEEDS) and obs["cells"]==36
         and obs["gap"]==gap and obs["interbody_calls"]==obs["steps"]==audit["steps"]==result["steps"]==n
         and audit["floor_passes"]==2*n and audit["disk_boundary_vertices"]==256
         and 0<=audit["max_penetration"]<=2e-12 and math.isclose(audit["accumulated_impulse"],
             math.fsum(ps)*DT*e.ctx.solver.WIDTH/10,rel_tol=1e-10,abs_tol=1e-13),"F geometry audit")
    return dict(**e.identity,status="GEOMETRY_LIMIT",cells=36,phi_m=None,trace_sha256=sha(trace),
                result_sha256=sha(result_raw),observation_sha256=sha(obs_raw),dt=DT,geometry_sha256=list(SEEDS))

def run_f(e,folder):
    arrays,dt,hashes=e.gate.seed_and_clock(e,36)
    ctx=e.ctx
    floor=ctx.floor.make_advance(ctx.solver,36)
    gap=e.gap.GapProjector(ctx.kernel)
    steps=contacts=seeds=0
    def seed(n):
        nonlocal seeds
        need(n==36 and seeds==0,"F36 seed")
        seeds+=1
        return arrays
    def contact(*args):
        nonlocal contacts
        need(contacts==steps and floor.boundary is not None and args[-1]==.5,"F contact order")
        value=gap.project(floor.boundary,dt,*args)
        contacts+=1
        return value
    def advance(*args):
        nonlocal steps
        height=ctx.solver.WIDTH-dt*(steps+1)*ctx.solver.WALL_SPEED
        need(args[-3:]==(360,dt,ctx.solver.LO+height) and args[4] is arrays[1] and args[5] is arrays[2],
             "F native geometry and driver clock")
        state=floor(*args)
        steps+=1
        need(contacts==steps,"missing F contact")
        return state
    with e.fine.bind_driver(ctx,seed,contact),e.gate.mark_native_result(ctx.driver):
        result=ctx.driver.run_arm("F",36,BUDGET["F"],folder,advance=advance)
    need(seeds==1 and contacts==steps==result["steps"] and result["status"] in
         ("TARGET_BRACKETED","GEOMETRY_LIMIT"),"incomplete F arm: "+result["status"])
    write(folder/"observation.json",dict(identity=e.identity,cells=36,geometry_sha256=hashes,
          steps=steps,interbody_calls=contacts,gap=gap.metadata(),floor=floor.audit))
    write(folder/"target_receipt.json",f_receipt(e,folder))

def read_new(root,arm,run):
    s,e = context(root,arm)
    folder = run/(arm+"36")
    need(not (folder/"incomplete.json").exists(), "incomplete arm")
    if arm == "S":
        rec = s.read_s(e,36,folder)
        need(rec == json.loads((folder/"receipt.json").read_bytes()), "S receipt replay")
        return rec
    e.gate.seed_and_clock(e,36)
    rec = f_receipt(e,folder)
    need(rec == json.loads((folder/"target_receipt.json").read_bytes()), "F receipt replay")
    return s.curve_record(e,(folder/"trace.csv").read_bytes(),json.loads((folder/"result.json").read_bytes()),
                          DT,origin="selected-gap-only-new")

def summary(root,run,sdir,fdir):
    need(all((root/n).read_bytes()==(run/n).read_bytes() for n in ("RELEASE","SOURCE_SHA256SUMS")), "return release")
    rows, hashes, priors = history(root,sdir,fdir)
    coord = load(root/"coordinate.py")
    execution = json.loads((run/"execution.json").read_bytes())
    coord.validate_execution(execution)
    for arm in ("S","F"):
        child = json.loads((run/(arm+"_affinity.json")).read_bytes())
        need(child == {k:execution[arm][k] for k in child} and set(child)=={"arm","cpu","core","affinity","threads"},
             "returned worker affinity")
        rec = read_new(root,arm,run)
        rows[arm,36] = rec["points"]
        hashes[arm+"36"] = rec["trace_sha256"]
    shifted = load(root/"rules/suyoung_u6b36_dev.py")
    targets = shifted.legacy.compare(rows)["targets"]
    for row in targets.values():
        bounds = row["ln_S_over_F_interval_report_only"]
        row["S_over_F_interval"] = None if bounds is None else [None if v is None else math.exp(v) for v in bounds]
    return {"label":"DEVELOPMENT_ONLY","setting":2,"release":(root/"RELEASE").read_text().strip(),
            "after_result_amendment":True,"witness":12,"judgment_grids":[16,24,36],"prior_tar_sha256":priors,
            "trace_sha256":hashes,"targets":targets,"decision":decision(targets),
            "original_item6":"FAILED","item6_percent":[79.25,19.25],"item6_threshold_percent":5,
            "stage3_go":False,"three_dimensional_go":False}

def perform(root,run,arm,cpu):
    need(os.sched_getaffinity(0) == {cpu} and all(os.environ.get(k)=="1" for k in THREADS),
         "single-thread affinity")
    coord = load(root/"coordinate.py")
    write(run/(arm+"_affinity.json"),dict(arm=arm,cpu=cpu,core=list(coord.topology(cpu)),affinity=[cpu],threads=1))
    s,e = context(root,arm)
    if arm=="S":
        s.run_s(e,36,run/"S36")
    else:
        run_f(e,run/"F36")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=("check","arm","summary","replay"))
    parser.add_argument("root",type=Path)
    parser.add_argument("sdir",type=Path)
    parser.add_argument("fdir",type=Path)
    parser.add_argument("--run",type=Path)
    parser.add_argument("--arm",choices=("S","F"))
    parser.add_argument("--cpu",type=int)
    args=parser.parse_args()
    root=args.root.resolve()
    if args.mode=="arm":
        perform(root,args.run,args.arm,args.cpu)
    elif args.mode=="check":
        history(root,args.sdir,args.fdir)
        s,e = context(root,"S")
        s.verify_coupled_floor(e.ctx.floor)
        _,dt,hashes,boundary = s.surface_and_seed(e,36)
        need(hashes==list(SEEDS) and dt==DT and len(set(boundary.groups))==1,"shared S field")
        _,f = context(root,"F")
        arrays,_,_ = f.gate.seed_and_clock(f,36)
        bound = f.ctx.floor.disk_boundary(f.ctx.solver,arrays[0],arrays[1],36)
        need(len(set(bound.groups))==49 and (bound.groups==arrays[1][bound.owners]).all(),"F physical IDs")
        f.gap.GapProjector(f.ctx.kernel)
        check_shifted_reader(root)
        print("Q13_TWO_RETURNS_SIX_TRACES_BOTH_36_SEEDS_OK")
    else:
        data = summary(root,args.run,args.sdir,args.fdir)
        dest = args.run/"summary.json"
        if args.mode=="summary":
            write(dest,data)
        else:
            need(json.loads(dest.read_bytes())==data,"archived summary mismatch")
        for p,item in data["targets"].items():
            print(p,"S/F",item["S_over_F_interval"])
        print(data["decision"])

if __name__=="__main__":
    main()
