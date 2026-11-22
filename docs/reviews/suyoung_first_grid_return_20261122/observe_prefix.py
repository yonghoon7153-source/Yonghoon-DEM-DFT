"""Observe the two bottom-wall impulses before the recorded F8/F16 first crossing."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tarfile

import numpy as np


PAIR_PATH="docs/reviews/suyoung_u6c_f16_stop_20261122/run_pair.py"
PAIR_SHA="4ba6682e6ea55a40fcf7cf769c72bbb966e5bcd96f28abcdfa39b3704233e70a"
PRIOR="fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea"
PIN="99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f"
KERNEL="acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"
TRACE={8:"56f0f5f836e00cc5c7a94afaaef7885e684f17c7983abf631f06e7e39a1c8132",
       16:"91cbbbd1b249dc9989df8ecf641ca522a3cee2e1131619926c82f7e0746572d9"}
DT={8:.0022463670164795577,16:.0011231835082397789}
WIDTH=.7024180763115129
STEPS={8:270,16:540}
FINE_PEAK=0.6636991102836952  # complete prior F16 within its common interval with F8
ATOL=1e-12  # MPa; checks observer arithmetic only
RTOL=1e-12
STATUS="DEVELOPMENT_PREFIX_OBSERVED"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sources(repo):
    path=repo/PAIR_PATH
    require(sha(path.read_bytes())==PAIR_SHA,"PAIR_RUNNER_BINDING")
    spec=importlib.util.spec_from_file_location("pinned_prefix_pair",path)
    pair=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pair)
    require(pair.KERNEL==KERNEL,"WRONG_KERNEL")
    return pair,pair.load_sources(repo)


def history(prior):
    with prior.open("rb") as source:
        require(hashlib.file_digest(source,"sha256").hexdigest()==PRIOR,"WRONG_RETURN")
        source.seek(0)
        with tarfile.open(fileobj=source,mode="r:gz") as archive:
            def read(member):
                item=archive.getmember("run/"+member)
                require(item.isfile(),"PRIOR_MEMBER")
                return archive.extractfile(item).read()
            origin=dict(line.split("=",1) for line in read("origin.txt").decode("ascii").splitlines())
            require(origin["release"]==PIN,"WRONG_RELEASE")
            previous=json.loads(read("grid_comparison.json"))["pairs"]["F8_F16"]
            require(previous["fine_peak_MPa"]==FINE_PEAK and previous["first_exceedance_u"]==0.012087024470351482,
                    "FIRST_CROSSING_PROVENANCE")
            result={}
            for n,stop in STEPS.items():
                trace=read(f"F{n}/trace.csv")
                rec=json.loads(read(f"F{n}/candidate.json"))
                require(sha(trace)==rec["trace_sha256"]==TRACE[n] and rec["kernel_sha256"]==KERNEL
                        and rec["mapping"]=="ORIGINAL" and rec["status"]=="TARGET_BRACKETED", "PRIOR_TRACE")
                result[n]=b"".join(trace.splitlines(keepends=True)[:stop+2])
    return result


def validate_prefix(raw,n,hist):
    require(raw==hist[n],"RAW_PREFIX_MISMATCH")
    rows=list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
    require(len(rows)==STEPS[n]+1 and [int(r["step"]) for r in rows]==list(range(STEPS[n]+1)),
            "PREFIX_STEP_COUNT")
    return rows


def floor_measure(mass,xy,vel,lo):
    require(np.isfinite(mass).all() and (mass>=0.).all() and np.isfinite(vel[:,1]).all()
            and np.isfinite(xy[:,1]).all(),"WALL_NONFINITE")
    mask=(mass>0.) & (xy[:,1]<=lo) & (vel[:,1]<0.)
    m=mass[mask]
    total=math.fsum(m)
    mean=math.fsum((m/total)*(-vel[mask,1])) if len(m) else None
    return dict(count=len(m),M=total,mean_down=mean)


def close(a,b):
    return math.isclose(a,b,rel_tol=RTOL,abs_tol=ATOL)


def component(part,dt,width):
    count,m,mean,j=(part[k] for k in ("count","M","mean_down","J"))
    require(type(count) is int and count>=0 and math.isfinite(m) and m>=0. and
            math.isfinite(j) and j>=0. and math.isfinite(dt) and dt>0 and math.isfinite(width) and width>0,
            "INVALID_WALL")
    factor=10./width
    if count==0:
        require(m==0. and j==0. and mean is None,"EMPTY_WALL")
        return 0.
    require(m>0. and mean is not None and math.isfinite(mean) and mean>0.,"MISSING_WALL_MEAN")
    p=(m/dt)*mean*factor
    require(close(p,j/dt*factor),"MASS_SPEED_IMPULSE")
    return p


class PrefixComplete(Exception):
    """Raised on entry to the next step, before calling the native advance."""


class Observer:
    def __init__(self,solver,kernel,cells):
        self.solver,self.kernel,self.cells=solver,kernel,cells
        self.original_wall=solver.walls
        self.rows=[]
        self.events=[]
        self.parts=[]
        self.step=0

    def begin(self,step):
        self.step=step
        self.events=[]
        self.parts=[]

    def wall(self,mass,xy,vel,lid,speed):
        require(self.events in ([],["wall","contact"]),"WALL_CALL_ORDER")
        values=floor_measure(mass,xy,vel,self.solver.LO)
        j=self.original_wall(mass,xy,vel,lid,speed)
        values["J"]=j
        self.parts.append(values)
        self.events.append("wall")
        return j

    def project(self,*args):
        require(self.events==["wall"] and args[-1]==.5,"CONTACT_CALL_ORDER")
        result=self.kernel.project_contacts(*args)
        self.events.append("contact")
        return result

    def advance(self,*args):
        if len(self.rows)==STEPS[self.cells]:
            raise PrefixComplete
        step=len(self.rows)+1
        grid,dt,lid=args[-3:]
        height=self.solver.WIDTH-dt*step*self.solver.WALL_SPEED
        require(grid==10*self.cells and dt==DT[self.cells] and lid==self.solver.LO+height,"STEP_SCHEDULE")
        self.begin(step)
        out=self.solver.advance(*args)
        require(self.events==["wall","contact","wall"],"INCOMPLETE_NATIVE_STEP")
        pre,post=self.parts
        native=(pre["J"]+post["J"])/(dt*self.solver.WIDTH)
        require(native==out[-1],"NATIVE_IMPULSE_SUM")
        p=10.*native
        require(close(component(pre,dt,WIDTH)+component(post,dt,WIDTH),p),"NATIVE_PRESSURE_FACTOR")
        self.rows.append(dict(step=step,u=self.solver.WIDTH-height,pre=pre,post=post,p_MPa=p))
        return out


def write(path,value):
    with path.open("x",encoding="ascii",newline="\n") as out:
        json.dump(value,out,allow_nan=False,sort_keys=True,indent=2)
        out.write("\n")


def receipt(n,geometry,folder):
    return dict(status=STATUS,prior_sha256=PRIOR,previous_pin=PIN,kernel_sha256=KERNEL,runner_sha256=PAIR_SHA,
                observer_sha256=sha(Path(__file__).read_bytes()),raw_prefix_sha256=sha((folder/"trace.csv").read_bytes()),
                observations_sha256=sha((folder/"wall_observations.json").read_bytes()),mapping="ORIGINAL",cells=n,
                steps=STEPS[n],geometry=geometry,dt=DT[n],label="DEVELOPMENT_ONLY",u6_qualified=False,stage3_go=False)


def validate_rows(records,n,trace):
    require(type(records) is list and len(records)==STEPS[n],"WALL_ROW_COUNT")
    for i,r in enumerate(records,1):
        require(type(r["step"]) is int and r["step"]==i and r["u"]==WIDTH-float(trace[i]["height"])
                and r["p_MPa"]==10.*float(trace[i]["bottom_pressure_E"]),"NATIVE_ROW_BINDING")
        pre,post=r["pre"],r["post"]
        require(close(component(pre,DT[n],WIDTH)+component(post,DT[n],WIDTH),r["p_MPa"]),
                "NATIVE_SUM")
        require(10.*((pre["J"]+post["J"])/(DT[n]*WIDTH))==r["p_MPa"],"WALL_IMPULSE_BYTES")


def arm(pair,mods,hist,n,folder):
    if folder.exists() or folder.is_symlink():
        raise FileExistsError(folder)
    driver=mods["driver"]
    factory,selector=driver.fixed_solver,driver.field_ids
    solver=factory()
    pair.setup_geometry(driver,solver,n)
    base_seed,base_project=solver.seed,solver.project_contacts
    obs=Observer(solver,mods["kernel"],n)
    observed={}
    def seed(cells):
        require(not observed and cells==n,"SEED_REQUEST")
        x,ids,volume=base_seed(cells)
        observed.update(pair.seed_hashes(x,ids,volume,n))
        return x,ids,volume
    driver.fixed_solver=lambda:solver
    driver.field_ids=lambda mode,ids:pair.select_fields(selector,n,mode,ids,observed)
    solver.seed,solver.walls,solver.project_contacts=seed,obs.wall,obs.project
    try:
        native=driver.run_arm("F",n,pair.BUDGET[n],folder,advance=obs.advance)
        raise ValueError("EARLY_NATIVE_STOP_"+str(native["status"]))
    except PrefixComplete:
        require(observed==pair.expected_geometry(n),"FIELD_IDS")
        trace=validate_prefix((folder/"trace.csv").read_bytes(),n,hist)
        validate_rows(obs.rows,n,trace)
        write(folder/"wall_observations.json",obs.rows)
        write(folder/"prefix_receipt.json",receipt(n,observed,folder))
    finally:
        driver.fixed_solver,driver.field_ids=factory,selector
        solver.seed,solver.walls,solver.project_contacts=base_seed,obs.original_wall,base_project


def checked_records(pair,hist,n,folder):
    trace=validate_prefix((folder/"trace.csv").read_bytes(),n,hist)
    records=json.loads((folder/"wall_observations.json").read_bytes())
    validate_rows(records,n,trace)
    expected=receipt(n,pair.expected_geometry(n),folder)
    actual=json.loads((folder/"prefix_receipt.json").read_bytes())
    require(json.dumps(expected,sort_keys=True)==json.dumps(actual,sort_keys=True),"RETURN_RECEIPT")
    return records


def summarize(coarse,fine):
    c0,c1=coarse[-2:]
    f0,f1=fine[-2:]
    require((c0["step"],c1["step"],f0["step"],f1["step"])==(269,270,539,540) and
            fine[-3]["step"]==538 and c0["u"]==fine[-3]["u"]<f0["u"]<c1["u"]==f1["u"],"MATCHED_LOCATION")
    alpha=(f0["u"]-c0["u"])/(c1["u"]-c0["u"])
    interpolated=c0["p_MPa"]+alpha*(c1["p_MPa"]-c0["p_MPa"])
    first_gap=interpolated-f0["p_MPa"]
    require(20*abs(first_gap)>FINE_PEAK and 20*abs(c0["p_MPa"]-fine[-3]["p_MPa"])<=FINE_PEAK,
            "FIRST_CROSSING_BRACKET")
    delta=c1["p_MPa"]-f1["p_MPa"]
    contributions={k:component(c1[k],DT[8],WIDTH)-component(f1[k],DT[16],WIDTH) for k in ("pre","post")}
    require(close(sum(contributions.values()),delta),"MATCHED_DIFFERENCE")
    meaningful=not close(delta,0.)
    return dict(status=STATUS if meaningful else "HOLD_UNRESOLVED_NUMERICAL_DIFFERENCE",label="DEVELOPMENT_ONLY",
                u6_qualified=False,stage3_go=False,coarse_original=[c0,c1],fine_original=[f0,f1],
                first_exceedance=dict(u=f0["u"],common_fine_peak_MPa=FINE_PEAK,threshold_MPa=FINE_PEAK/20,
                    coarse_total_interpolated_MPa=interpolated,fine_total_observed_MPa=f0["p_MPa"],
                    coarse_minus_fine_MPa=first_gap),
                matched=dict(u=c1["u"],coarse_minus_fine_MPa=delta,components_MPa=contributions,
                    component_pressures_MPa={f"F{n}":{k:component(r[k],DT[n],WIDTH) for k in ("pre","post")}
                                             for n,r in ((8,c1),(16,f1))},
                    mass_over_dt={f"F{n}":{k:r[k]["M"]/DT[n] for k in ("pre","post")}
                                  for n,r in ((8,c1),(16,f1))}))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    for name in ("check","arm","read"):
        cmd=sub.add_parser(name)
        for key in ("repo","prior"):
            cmd.add_argument("--"+key,required=True,type=Path)
        if name in ("arm","read"):
            cmd.add_argument("--out",required=True,type=Path)
        if name=="arm":
            cmd.add_argument("--cells",required=True,type=int,choices=(8,16))
        if name=="read":
            cmd.add_argument("--run",required=True,type=Path)
    args=p.parse_args()
    try:
        pair,mods=sources(args.repo)
        hist=history(args.prior)
        if args.command=="check":
            for n in STEPS:
                pair.setup_geometry(mods["driver"],mods["driver"].fixed_solver(),n)
                validate_prefix(hist[n],n,hist)
            print("PREFIX_SOURCES_SEEDS_AND_PRIOR_BOUND")
        elif args.command=="arm":
            arm(pair,mods,hist,args.cells,args.out)
            print(STATUS)
        else:
            result=summarize(*(checked_records(pair,hist,n,args.run/f"F{n}") for n in STEPS))
            write(args.out,result)
            print(result["status"])
            return 0 if result["status"]==STATUS else 4
    except (OSError,ValueError,RuntimeError,ArithmeticError,KeyError,TypeError,IndexError,tarfile.TarError) as exc:
        reason=str(exc) if str(exc).isupper() else type(exc).__name__
        if args.command=="read" and not args.out.exists():
            write(args.out,dict(status="HOLD_INCOMPLETE",issue=reason,u6_qualified=False,stage3_go=False))
        print("HOLD",reason)
        return 4
    return 0


if __name__=="__main__":
    raise SystemExit(main())
