"""Native F8/F16 development runs with the pinned material-floor integrator and prefix."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
import re
import sys
import tarfile
from pathlib import Path


PREFIX_PIN = "b16bef3f7791b86d31f0197d86b58d9d93d84750"
PREFIX_MANIFEST = "30c1282abdc3029d9c28d126e384f838d17e7a11710802fe69a09a50d63d57e1"
PREFIX_TAR = "57d0a6fe178b2faf0545013ef43b9ff6d175c1fdb18e93522ec8dcb8eb1b7e34"
PREFIX_OPERATOR = "32674a6875421d7c7c9dbcc04602240c87eafb9995326f85ed737c7f9165be20"
OLD = "docs/reviews/suyoung_floor_contact_20261123/"
NEW = "docs/reviews/suyoung_floor_full_20261123/"
FLOOR = "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b"
PREFIX_TRACE = {8:"487cd8c96f8406df14d6f83c70c37ab46bc69d4fd42a179f4284a8ab178a703d",
                16:"1ba3d21deedeec47fe6b6966539ec98ae6514cf3c02442eca8ae965cd23622d7"}
COLS = ("step","time_code","height","bottom_pressure_E","phi_m")
BUDGET = {8:1800,16:5400}  # per-arm wall seconds
POINTS = {8:9653,16:39053}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def module(path):
    spec=importlib.util.spec_from_file_location("full_run_"+path.stem,path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sources(root):
    prefix=root/"prefix"
    old_manifest=(prefix/"SOURCE_SHA256SUMS").read_bytes()
    require(sha(old_manifest)==PREFIX_MANIFEST,"PREFIX_SOURCE_MANIFEST")
    expected={"prefix/"+ln.split("  ",1)[1] for ln in old_manifest.decode("ascii").splitlines()}
    expected.update({"prefix/SOURCE_SHA256SUMS","RELEASE",*(NEW+k for k in
                     ("full_floor.py","full_compare.py","run_full.sh"))})
    raw=(root/"SOURCE_SHA256SUMS").read_bytes()
    seen={}
    for ln in raw.decode("ascii").splitlines():
        digest,name=ln.split("  ",1)
        require(name in expected and name not in seen and re.fullmatch("[0-9a-f]{64}",digest),"PACKAGE_MEMBER")
        require(sha((root/name).read_bytes())==digest,"PACKAGE_HASH "+name)
        seen[name]=digest
    require(set(seen)==expected and sha(Path(__file__).read_bytes())==seen[NEW+"full_floor.py"],"PACKAGE_BINDING")
    release=(root/"RELEASE").read_text("ascii").strip()
    require(re.fullmatch("[0-9a-f]{40}",release),"RELEASE_PIN")
    old_op=prefix/(OLD+"floor_operator.py")
    require(sha(old_op.read_bytes())==PREFIX_OPERATOR,"PREFIX_OPERATOR")
    op=module(old_op)
    m, base, driver, solver, kernel, cand=op.sources(prefix)
    require(base["release"]==PREFIX_PIN and base["candidate_sha256"]==FLOOR,"FROZEN_FLOOR")
    metadata=dict(release=release,source_manifest_sha256=sha(raw),floor_sha256=FLOOR,
                  floor_release=PREFIX_PIN,physics_pin=m.PHY,prior_return_sha256=PREFIX_TAR)
    return op,m,metadata,driver,solver,kernel,cand,base


def prior_inputs(parts,path):
    op,m,_,_,_,_,_,base=parts
    result={}
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream,"sha256").hexdigest()==PREFIX_TAR,"PRIOR_TAR_HASH")
        stream.seek(0)
        with tarfile.open(fileobj=stream,mode="r:gz") as tar:
            def read(name):
                info=tar.getmember("run/"+name)
                require(info.isfile(),"PRIOR_REGULAR_MEMBER")
                return tar.extractfile(info).read()
            require(read("RELEASE").decode("ascii").strip()==PREFIX_PIN
                    and sha(read("SOURCE_SHA256SUMS"))==PREFIX_MANIFEST and
                    read("screen.txt").splitlines()[-1]==b"COMMAND_RC=0","PRIOR_RETURN_STATUS")
            summary=json.loads(read("summary.json"))
            for cells in POINTS:
                key=f"candidate/F{cells}"
                receipt=read(key+"/receipt.json")
                raw=read(key+"/trace.csv")
                rec=json.loads(receipt)
                require(sha(raw)==PREFIX_TRACE[cells]==summary["trace_sha256"][key+"/trace.csv"] and
                        sha(receipt)==summary["receipt_sha256"][key] and
                        op.candidate_receipt(m,base,cells,raw,rec["interbody_calls"],rec["floor_audit"])==rec,
                        "PRIOR_NATIVE_RECEIPT")
                result[cells]=raw
    return result


def validate_complete(m,raw,prefix,result,audit,*,cells,expected_sources):
    dt=m.DT*(2 if cells==8 else 1)
    require(raw.startswith(prefix) and prefix.endswith(b"\n"),"PRIOR_PREFIX_BYTES")
    reader=csv.DictReader(io.StringIO(raw.decode("ascii"),newline=""))
    require(tuple(reader.fieldnames or ())==COLS,"TRACE_COLUMNS")
    expected_result={"protocol":"U6b-setting1-bottom-loading-v1","label":"DEVELOPMENT_ONLY",
                     "arm":"F","cells":cells,"setting":1,"origin":"new","points_count":POINTS[cells],
                     "source_sha256":expected_sources,"budget_s":BUDGET[cells],"trace_sha256":sha(raw)}
    require(all(result.get(k)==v for k,v in expected_result.items()),"TERMINAL_RECEIPT")
    terminal=result["status"]
    require(terminal in ("TARGET_BRACKETED","GEOMETRY_LIMIT"),"NOT_A_COMPLETED_NATIVE_ARM")
    require(math.isfinite(result["elapsed_s"]) and 0<=result["elapsed_s"]<=BUDGET[cells]+30,
            "ELAPSED_TIME")
    pressures=[]
    for i,row in enumerate(reader):
        require(tuple(row)==COLS and row["step"]==str(i),"NATIVE_STEP")
        t,h,p,phi=map(float,(row[k] for k in COLS[1:]))
        require(t==dt*i and h==m.WIDTH-t*m.SPEED and h>=.75*m.WIDTH and
                math.isclose(phi,.78*m.WIDTH/h,rel_tol=1e-12) and math.isfinite(p) and p>=0,
                "NATIVE_ROW")
        pressures.append(p)
    n=len(pressures)-1
    require(n>=1 and result["steps"]==n and pressures[0]==0. and
            all(p<.12 for p in pressures[:-1]),"NOT_FIRST_NATIVE_PRESSURE_CAP")
    if terminal=="TARGET_BRACKETED":
        require(pressures[-1]>=.12,"TERMINAL_DID_NOT_REACH_CAP")
    else:
        require(pressures[-1]<.12 and m.WIDTH-(n+1)*dt*m.SPEED < .75*m.WIDTH,
                "NOT_NATIVE_GEOMETRY_ENDPOINT")
    require(audit["steps"]==n and audit["floor_passes"]==2*n and audit["disk_boundary_vertices"]==256,
            "FLOOR_STEP_COUNTS")
    positive=[i for i,p in enumerate(pressures) if p>0.]
    require(type(audit["positive_passes"]) is int and len(positive)<=audit["positive_passes"]<=2*len(positive),
            "POSITIVE_FLOOR_PASSES")
    for name in ("accumulated_impulse","max_grid_impulse_error","max_g2p_momentum_error","max_penetration"):
        require(math.isfinite(audit[name]) and audit[name]>=0.,"INVALID_AUDIT "+name)
    require(audit["max_penetration"]<=2e-12 and math.isclose(audit["accumulated_impulse"],
            math.fsum(pressures)*dt*m.WIDTH,rel_tol=1e-10,abs_tol=1e-13),"FLOOR_IMPULSE_BALANCE")
    onset=positive[0] if positive else None
    return dict(terminal_step=n,terminal_reason=terminal,reached_target=terminal=="TARGET_BRACKETED",
                terminal_pressure_MPa=10*pressures[-1],first_nonzero_step=onset,
                first_nonzero_displacement_code=None if onset is None else m.WIDTH-(m.WIDTH-onset*dt*m.SPEED),
                first_nonzero_pressure_MPa=None if onset is None else 10*pressures[onset],
                positive_native_steps=len(positive))


def receipt(parts,old,cells,raw,result,audit):
    op,m,meta,driver=parts[:4]
    s=validate_complete(m,raw,old[cells],result,audit,cells=cells,expected_sources=driver.SOURCE)
    return dict(**meta,**s,status="FULL_NATIVE_TERMINUS_OBSERVED",label="DEVELOPMENT_ONLY",cells=cells,
                grid=10*cells,dt=op.dt_for(m,cells),width=m.WIDTH,wall_speed=m.SPEED,
                native_target_MPa=1.2,seconds_limit=BUDGET[cells],
                geometry_hashes=list(m.GEOMETRY[cells]),interbody_calls=s["terminal_step"],
                trace_sha256=sha(raw),prior_trace_sha256=sha(old[cells]),floor_audit=audit,
                u6_qualified=False,stage3_go=False)


def run_arm(parts,old,cells,dest):
    op,m,meta,driver,solver,kernel,cand,_=parts
    initial=m.seed_arrays(solver,cells)
    require(driver.field_ids("F",initial[1]) is initial[1],"F_FIELD_IDS")
    dt=op.dt_for(m,cells)
    expected=[float(r["bottom_pressure_E"]) for r in csv.DictReader(io.StringIO(old[cells].decode("ascii")))]
    corrected=cand.make_advance(solver,cells)
    seed_calls=steps=contacts=0
    def seed(n):
        nonlocal seed_calls
        require(n==cells and seed_calls==0,"SEED_REQUEST")
        seed_calls+=1
        return initial
    def contact(*args):
        nonlocal contacts
        require(contacts==steps and args[-1]==.5,"INTERBODY_SCHEDULE")
        value=kernel.project_contacts(*args)
        contacts+=1
        return value
    def advance(*args):
        nonlocal steps
        require(args[-3:]==(cells*10,dt,solver.LO+(m.WIDTH-(steps+1)*dt*m.SPEED)) and
                args[4] is initial[1] and args[5] is initial[2],"ADVANCE_CLOCK_OR_FIELDS")
        value=corrected(*args)
        steps+=1
        require(contacts==steps,"INTERBODY_COUNT")
        if steps<len(expected):
            require(value[-1]==expected[steps],"PRIOR_PRESSURE_STEP_"+str(steps))
        return value
    require(not dest.exists() and not dest.is_symlink(),"EXISTING_ARM")
    saved=solver.seed,solver.project_contacts,driver.fixed_solver
    solver.seed,solver.project_contacts,driver.fixed_solver=seed,contact,lambda:solver
    try:
        result=driver.run_arm("F",cells,BUDGET[cells],dest,advance=advance)
        require(seed_calls==1 and steps==contacts==result["steps"],"NATIVE_DRIVER_COUNTS")
        require(result["status"] in ("TARGET_BRACKETED","GEOMETRY_LIMIT"),"NATIVE_STOP_"+result["status"])
        raw=(dest/"trace.csv").read_bytes()
        rec=receipt(parts,old,cells,raw,result,corrected.audit)
        rec["result_sha256"]=sha((dest/"result.json").read_bytes())
        op.write_json(dest/"full_receipt.json",rec)
        return 0
    except (ValueError,TypeError,KeyError,OSError,ArithmeticError,RuntimeError) as exc:
        if dest.is_dir():
            op.write_json(dest/"incomplete.json",dict(**meta,status="INCOMPLETE",cells=cells,steps=steps,
                interbody_calls=contacts,floor_audit=corrected.audit,reason=type(exc).__name__+": "+str(exc),
                u6_qualified=False,stage3_go=False))
        print("INCOMPLETE",cells,str(exc),file=sys.stderr)
        return 4
    finally:
        solver.seed,solver.project_contacts,driver.fixed_solver=saved


def read_arm(parts,old,cells,dest):
    require(not (dest/"incomplete.json").exists(),"INCOMPLETE_ARM")
    raw=(dest/"trace.csv").read_bytes()
    result=(dest/"result.json").read_bytes()
    rec=json.loads((dest/"full_receipt.json").read_bytes())
    calculated=receipt(parts,old,cells,raw,json.loads(result),rec["floor_audit"])
    require(dict(calculated,result_sha256=sha(result))==rec,"FULL_RECEIPT_BINDING")
    return raw,rec


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("check","arm","summary"))
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--prior",type=Path,required=True)
    p.add_argument("--run",type=Path)
    p.add_argument("--cells",type=int,choices=(8,16))
    a=p.parse_args()
    parts=sources(a.root)
    op,m,meta,_,solver=parts[:5]
    old=prior_inputs(parts,a.prior)
    if a.mode=="check":
        for cells in POINTS:
            m.seed_arrays(solver,cells)
        print("FULL_SOURCE_CLOCK_SEEDS_AND_PREFIXES_OK")
        return 0
    require(a.run is not None and a.run.is_dir(),"NEW_RUN_DIRECTORY")
    for name in ("RELEASE","SOURCE_SHA256SUMS"):
        require((a.root/name).read_bytes()==(a.run/name).read_bytes(),"RUN_RELEASE_BINDING")
    if a.mode=="arm":
        require(a.cells in POINTS,"CELLS_REQUIRED")
        return run_arm(parts,old,a.cells,a.run/f"F{a.cells}")
    c=module(a.root/NEW/"full_compare.py")
    raw8,f8=read_arm(parts,old,8,a.run/"F8")
    raw16,f16=read_arm(parts,old,16,a.run/"F16")
    stats=c.compare_pair(raw8,raw16,width=m.WIDTH,speed=m.SPEED,dt8=op.dt_for(m,8),dt16=op.dt_for(m,16),
                         terminal8=f8["terminal_reason"],terminal16=f16["terminal_reason"])
    summary=dict(**meta,status="DEVELOPMENT_FULL_PAIR_READBACK",label="DEVELOPMENT_ONLY",
                 arms={"F8":f8,"F16":f16},both_native_terminated=True,
                 both_reached_target=f8["reached_target"] and f16["reached_target"],
                 comparison=stats,registered_peak_MPa=m.FINE_PEAK,
                 finer_F12_F24="UNMEASURED",u6_qualified=False,stage3_go=False)
    op.write_json(a.run/"summary.json",summary)
    print("FULL_PAIR_READBACK_OK")
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except (ArithmeticError,RuntimeError,TypeError,KeyError,IndexError,OSError,ValueError,tarfile.TarError) as e:
        print("INCOMPLETE",str(e),file=sys.stderr)
        raise SystemExit(4)
