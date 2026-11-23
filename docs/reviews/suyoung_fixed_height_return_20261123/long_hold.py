"""Fourfold stationary observation after the exact prior ramp and short hold."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from types import ModuleType, SimpleNamespace


SHORT_PIN = "cf81ed8a70fd4c6b7b65874f45920c31c0871ee9"
SHORT_SOURCE = "00cdc32cad0cf8b8981e3175bfe4d3e4d50e31e51c20f49e012d68c953db2a79"
SHORT_MANIFEST = "d0f0783801d4b826cf9dd8b7fd5b86d4e7c8bdfa77371f080c6cdce8be1061c4"
SHORT_RETURN = "218f4b4b784a63ededdefefba92a8160e41c86bc56f0e2c121febc7cd4ff4cf2"
DRIVER = "docs/reviews/suyoung_speed_ladder_20261123/hold_pair.py"
RAMP = {12: 1638, 24: 3276}
OLD_HOLD = {12: 1200, 24: 2400}
HOLD = {12: 4800, 24: 9600}
BUDGET = {12: 2400, 24: 7200}
CSV = ("trace.csv", "wall_steps.csv", "layer_steps.csv", "particle_momentum.csv", "energy.csv")
WINDOW_NAMES = ("first_300", "overlap_last_300", "late_1", "late_2")
COMPLETED = b"                    completed=step\n"
CHECKPOINT = b"""                    if completed == RAMP[n] + PREVIOUS_HOLD[n]:
                        for stream,_ in outputs.values():
                            stream.flush()
                        confirm_before_extension(dest,e,n,fork,observed.groups.spec,
                                                state_hashes(x,v,C,F,boundary.positions,ids,mass))
"""


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def derive_driver(source):
    require(digest(source) == SHORT_SOURCE and source.count(COMPLETED) == 1, "short driver identity or checkpoint")
    return source.replace(COMPLETED, COMPLETED + CHECKPOINT, 1)


def load_driver(path):
    module = ModuleType("long_pin_observation")
    module.__file__ = str(path)
    source = derive_driver(path.read_bytes())
    exec(compile(source, str(path), "exec"), module.__dict__)
    module.PREVIOUS_HOLD = OLD_HOLD
    module.confirm_before_extension = confirm_before_extension
    return module


def setup(args):
    history = args.root / "history"
    manifest = (history / "SOURCE_SHA256SUMS").read_bytes()
    require(digest(manifest) == SHORT_MANIFEST and (history/"RELEASE").read_text().strip() == SHORT_PIN,
            "fixed-height source identity")
    for line in manifest.decode("ascii").splitlines():
        expected, name = line.split("  ")
        require(digest((history/name).read_bytes()) == expected, "fixed-height source member " + name)
    short = load_driver(history/DRIVER)
    require(short.RAMP == RAMP and short.HOLD == OLD_HOLD, "prior schedule")
    e = short.setup(SimpleNamespace(**(vars(args) | {"root": history})))
    names = ["summary.json", "screen.txt", "SOURCE_SHA256SUMS", "RELEASE"]
    names += [f"F{n}/{name}" for n in RAMP for name in (*CSV, "layer_spec.json", "hold_receipt.json")]
    members = e.q.read_archive(args.fixed, SHORT_RETURN, names)
    prior = json.loads(members["summary.json"])
    screen = members["screen.txt"].splitlines()
    require(prior["status"] == "HOLD_PAIR_COMPLETE" and all(prior[k] == v for k,v in e.identity.items())
            and members["SOURCE_SHA256SUMS"] == manifest and members["RELEASE"] == (SHORT_PIN+"\n").encode()
            and screen[-1] == b"COMMAND_RC=0" and all(k in screen for k in (b"F12_RC=0", b"F24_RC=0")),
            "fixed-height return identity")
    e.replay = {}
    for n in RAMP:
        arm = prior["arms"][str(n)]
        receipt = json.loads(members[f"F{n}/hold_receipt.json"])
        require(receipt == arm["receipt"] and all(receipt[k] == v for k,v in e.identity.items())
                and receipt["status"] == "HOLD_ARM_COMPLETE" and receipt["grid"] == n
                and receipt["budget_seconds"] == short.BUDGET[n], "prior arm receipt")
        files = {name: members[f"F{n}/{name}"] for name in (*CSV, "layer_spec.json")}
        require({k:digest(v) for k,v in files.items()} == receipt["hashes"], "prior observations")
        for name in CSV:
            expected_rows = 1 + RAMP[n] + OLD_HOLD[n] + int(name in ("trace.csv", "energy.csv"))
            require(len(files[name].splitlines()) == expected_rows, "prior observation count")
        e.replay[n] = SimpleNamespace(files=files, receipt=receipt, windows=arm["windows"])
    e.short = short
    new_pin = (args.root/"RELEASE").read_text().strip()
    new_manifest = (args.root/"SOURCE_SHA256SUMS").read_bytes()
    require(re.fullmatch("[0-9a-f]{40}", new_pin) is not None, "release")
    e.identity.update(release=new_pin, source_sha256=digest(new_manifest), short_hold_pin=SHORT_PIN,
                      fixed_return_sha256=SHORT_RETURN, old_hold_source_sha256=SHORT_SOURCE,
                      long_driver_sha256=digest(derive_driver((history/DRIVER).read_bytes())))
    require(all(HOLD[n] == 4*OLD_HOLD[n] for n in RAMP), "long schedule")
    return e


def compare_prefix(dest, plan, full_prefix):
    hashes = {}
    for name in CSV:
        expected = plan.files[name]
        with (dest/name).open("rb") as stream:
            observed = stream.read(len(expected))
            require(observed == expected, "short-hold bytes changed: " + name)
            if full_prefix:
                require(not stream.read(1), "unexpected row before extension: " + name)
        hashes[name] = digest(expected)
    return hashes


def confirm_before_extension(dest, e, n, fork, spec, state):
    plan = e.replay[n]
    require(fork == plan.receipt["fork"] and spec == json.loads(plan.files["layer_spec.json"]),
            "fork state, material membership or layer identity changed")
    hashes = compare_prefix(dest, plan, full_prefix=True)
    data = dict(e.identity, status="SHORT_HOLD_PREFIX_REPLAYED", grid=n, step=RAMP[n]+OLD_HOLD[n],
                previous_return_sha256=SHORT_RETURN, fork=fork, prefix_sha256=hashes,
                replay_endpoint_state_sha256=state)
    e.q.write_json(dest/"old_hold_boundary.json", data)


def read_boundary(e,n,dest):
    boundary = json.loads((dest/"old_hold_boundary.json").read_bytes())
    require(all(boundary[k]==v for k,v in e.identity.items()) and boundary["status"]=="SHORT_HOLD_PREFIX_REPLAYED"
            and boundary["grid"]==n and boundary["step"]==RAMP[n]+OLD_HOLD[n]
            and boundary["previous_return_sha256"]==SHORT_RETURN
            and boundary["fork"]==e.replay[n].receipt["fork"]
            and boundary["prefix_sha256"]==compare_prefix(dest,e.replay[n],full_prefix=False)
            and (dest/"layer_spec.json").read_bytes()==e.replay[n].files["layer_spec.json"], "short replay receipt")
    state=boundary["replay_endpoint_state_sha256"]
    require(set(state)==set(boundary["fork"]["state_sha256"]) and
            all(re.fullmatch("[0-9a-f]{64}",v) for v in state.values()), "endpoint state hashes")
    return boundary


def long_receipt(e,n,dest):
    boundary = read_boundary(e,n,dest)
    return dict(e.identity,status="LONG_HOLD_ARM_COMPLETE",grid=n,short_hold_replayed=boundary["step"],
                budget_seconds=BUDGET[n],hold_steps=HOLD[n],ramp_steps=RAMP[n],
                boundary_receipt_sha256=digest((dest/"old_hold_boundary.json").read_bytes()),
                arm_receipt_sha256=digest((dest/"hold_receipt.json").read_bytes()))


def average(values):
    return math.fsum(values)/len(values)


def stats(values):
    return dict(mean=average(values),min=min(values),max=max(values),rms=math.sqrt(average([x*x for x in values])))


def paired_pressure(a,b,scale12,scale24):
    """Integrate the two fine impulses over the same elapsed interval as one coarse impulse."""
    require(len(a)>0 and len(b)==2*len(a), "incomplete equal-time window")
    deltas={}
    for field in ("floor_impulse","lid_downward_impulse"):
        deltas[field]=[scale12*float(coarse[field])-scale24*average([float(b[2*i][field]),float(b[2*i+1][field])])
                       for i,coarse in enumerate(a)]
    low,high=deltas.values()
    return dict(floor_MPa=stats(low),lid_MPa=stats(high),
                mean_of_plates_MPa=stats([.5*(x+y) for x,y in zip(low,high,strict=True)]),
                half_plate_difference_MPa=stats([.5*(x-y) for x,y in zip(low,high,strict=True)]))


def make_windows(e,arms,observations):
    windows=[]
    for i in range(16):
        window=dict(index=i+1, source="previous" if i<4 else "extension",
                    time_since_stop=[300*i*e.fine.DT[12],300*(i+1)*e.fine.DT[12]])
        wall_parts={}
        scales={}
        for n in RAMP:
            walls,layers,energies=observations[n]
            size=300*(n//12)
            first=RAMP[n]+size*i
            end=first+size
            wall_parts[n]=walls[first:end]
            dt=e.fine.DT[n]
            scales[n]=10/(dt*e.ctx.solver.WIDTH)
            record=e.short.window(wall_parts[n],layers[first:end],energies[first+1:end+1],dt,e.ctx.solver.WIDTH)
            if i<4:
                prior=arms[n]["windows"][WINDOW_NAMES[i]]
                require(all(prior[k]==v for k,v in record.items()),"historical window changed")
            window[f"F{n}"]=record
        window["F12_minus_F24"]=paired_pressure(wall_parts[12],wall_parts[24],scales[12],scales[24])
        windows.append(window)
    return windows


def last_four(windows):
    require(len(windows)==16 and [r["index"] for r in windows]==list(range(1,17)), "missing windows")
    keys=("floor_mean_MPa","lid_mean_MPa","floor_minus_lid_mean_MPa","whole_delta_Py_MPa")
    series={f"{arm}_{k}":[w[arm][k] for w in windows[-4:]] for arm in ("F12","F24") for k in keys}
    for arm in ("F12","F24"):
        series[arm+"_particle_ke"]=[w[arm]["particle_ke"]["mean"] for w in windows[-4:]]
    for k in ("floor_MPa","lid_MPa"):
        series["F12_minus_F24_"+k]=[w["F12_minus_F24"][k]["mean"] for w in windows[-4:]]
    return {k:dict(values=v,mean=average(v),minimum=min(v),maximum=max(v),last_minus_first=v[-1]-v[0])
            for k,v in series.items()}


def summarize(e,run):
    arms={}
    obs={}
    for n in RAMP:
        dest=run/f"F{n}"
        require(json.loads((dest/"long_hold_receipt.json").read_bytes())==long_receipt(e,n,dest), "long arm identity")
        arms[n]=e.short.read_arm(e,n,dest)
        require(arms[n]["windows"]==e.replay[n].windows, "previous four windows or continued controls changed")
        obs[n]=[e.native.rows((dest/name).read_bytes()) for name in ("wall_steps.csv","layer_steps.csv","energy.csv")]
    require(arms[12]["locked_height"]==arms[24]["locked_height"] and arms[12]["hold_time"]==arms[24]["hold_time"]
            and e.fine.DT[12]==2*e.fine.DT[24], "different physical intervals")
    windows=make_windows(e,arms,obs)
    e.q.write_json(run/"summary.json",dict(e.identity,status="LONG_HOLD_PAIR_COMPLETE",arms=arms,
                   previous_windows=4,extension_windows=12,windows=windows,last_four_windows=last_four(windows),
                   reference_MPa=e.native.REF_MPA, qualification_basis="fixed_height_transient_development_only"))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("check","arm","summary"))
    for name in ("root","depth","prior","material","baseline","quarter","fixed"):
        p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--cells",type=int,choices=(12,24))
    p.add_argument("--run",type=Path)
    args=p.parse_args()
    e=setup(args)
    if args.mode=="check":
        print("LONG_HOLD_SIX_RETURNS_OK")
        return
    require(args.run is not None and args.run.is_dir() and all((args.root/k).read_bytes()==(args.run/k).read_bytes()
            for k in ("RELEASE","SOURCE_SHA256SUMS")), "run source binding")
    with e.half.override(e.short,HOLD=HOLD,BUDGET=BUDGET):
        if args.mode=="arm":
            require(args.cells in RAMP,"missing grid")
            dest=args.run/f"F{args.cells}"
            e.short.run_arm(e,args.cells,dest)
            e.q.write_json(dest/"long_hold_receipt.json", long_receipt(e,args.cells,dest))
        else:
            summarize(e,args.run)
            print("LONG_HOLD_NATIVE_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (ArithmeticError,IndexError,KeyError,OSError,RuntimeError,TypeError,ValueError) as error:
        print("INCOMPLETE",type(error).__name__,str(error),file=sys.stderr)
        raise SystemExit(4)
