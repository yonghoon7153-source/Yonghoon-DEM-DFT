"""Observe incoming particle states at four existing endpoints, then project them on fixed wall masks."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tarfile

import numpy as np

PROBE_PATH = "docs/reviews/suyoung_wall_stress_probe_20261122/probe.py"
PROBE_SHA = "60b9617157b5cc70d03f621a608449547649a60824a82811a2650d6126568ed4"
PROBE_PIN = "77f38e5c4fab089d1b6c378234b63f565a9f4923"
PROBE_RETURN = "fcf9fd337d57c77cb9b4f751a6b938ce60a1d9010e438026ac10ffa762104cfd"
STATUS = "DEVELOPMENT_FROZEN_CROSS_OBSERVED"
STEPS = {8: (269, 270), 16: (538, 540)}
COLS = ("yy", "yx", "unit_yy", "unit_yx")
STATE = ("x", "volume", "ids", "yy", "yx")
PREFIX_FILES = ("trace.csv", "wall_observations.json", "prefix_receipt.json")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sources(repo):
    path = repo / PROBE_PATH
    require(sha(path.read_bytes()) == PROBE_SHA, "PROBE_SOURCE")
    spec = importlib.util.spec_from_file_location("fixed_unit_stress", path)
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    return p, *p.sources(repo)


def histories(prior, probe, p, m, prefix, pair, lo):
    hist, walls = m.history(prior, prefix, pair)
    old = {}
    with probe.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == PROBE_RETURN, "PROBE_ARCHIVE")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            def raw(name):
                entry = tar.getmember("run/" + name)
                require(entry.isfile(), "PROBE_MEMBER")
                return tar.extractfile(entry).read()
            origin = dict(line.split("=", 1) for line in raw("origin.txt").decode("ascii").splitlines())
            require((origin["release"],origin["physics_pin"],origin["kernel_sha256"],origin["prior_sha256"],
                     origin["momentum_sha256"]) == (PROBE_PIN,prefix.PIN,prefix.KERNEL,m.PRIOR,p.RETURN_SHA),
                    "PROBE_ORIGIN")
            prior_summary = {}
            for n in STEPS:
                files = {k:raw(f"F{n}/{k}") for k in (*p.FILES,"probe.json")}
                pr = json.loads(raw(f"F{n}/probe_receipt.json"))
                require(pr == dict(status=p.STATUS, cells=n, steps=list(STEPS[n]),
                            observer_sha256=PROBE_SHA, old_momentum_return_sha256=p.RETURN_SHA,
                            basis_record_sha256=sha(files["probe.json"]),
                            regenerated={k:sha(files[k]) for k in p.FILES}), "ARCHIVED_PROBE_RECEIPT")
                require(files["trace.csv"] == hist[n] and json.loads(files["wall_observations.json"]) == walls[n],
                        "PRIOR_PREFIX")
                masks = p.original_masks(files)
                rows = json.loads(files["probe.json"])
                require([r["step"] for r in rows] == list(STEPS[n]), "PROBE_SAMPLE_STEPS")
                obs = {r["step"]:r["projection"] for r in rows}
                prior_summary[n] = {}
                for step in STEPS[n]:
                    mask = masks[step]
                    m.compare_sample(prefix, walls[n][step-1], mask, n, lo)
                    prior_summary[n][step] = p.reduce_record(obs[step], mask, prefix.DT[n], prefix.WIDTH)
                old[n] = dict(files={k:files[k] for k in PREFIX_FILES}, projection=obs)
            prior_json = json.loads(json.dumps(p.summarize(prefix, walls, prior_summary), allow_nan=False))
            require(prior_json == json.loads(raw("summary.json")), "ARCHIVED_PROBE_SUMMARY")
    return hist, walls, old


def validate(state):
    require(set(state) == set(STATE), "SNAPSHOT_COLUMNS")
    ids = state["ids"]
    require(ids.ndim == 1 and ids.size and ids.dtype.kind == "i" and ids.dtype.itemsize == 8
            and ((0 <= ids) & (ids < 49)).all(), "PARTICLE_IDS")
    require(state["x"].shape == (len(ids),2), "POINT_LAYOUT")
    for name in ("volume","yy","yx"):
        require(state[name].shape == ids.shape, "POINT_LAYOUT")
    for name in ("x","volume","yy","yx"):
        values = state[name]
        require(values.dtype.kind == "f" and values.dtype.itemsize == 8 and np.isfinite(values).all(),
                "POINT_VALUES")
    require((state["volume"] > 0).all(), "PARTICLE_VOLUME")


def snapshot(solver, x, elastic, ids, volume):
    tau = solver.model.stress(elastic)
    state = dict(x=x.copy(),volume=volume.copy(),ids=ids.copy(),yy=tau[:,1,1].copy(),yx=tau[:,1,0].copy())
    validate(state)
    return state


def bind_seed(state, geometry):
    validate(state)
    for name, original, kind in (("ids","physical_ids","<i8"),("volume","volume","<f8")):
        require(sha(state[name].astype(kind,copy=False).tobytes(order="C")) == geometry[original], "SEED_IDENTITY")


def save_state(path, state):
    validate(state)
    with path.open("xb") as stream:
        np.savez_compressed(stream, **state)


def supported(x, grid):
    base = np.floor(x * grid - .5)
    return bool((base >= 0).all() and (base+2 <= grid).all())


def project_state(model, state, grid, width, keys):
    validate(state)
    require(type(grid) is int and grid > 0 and math.isfinite(width) and width > 0, "GRID_AND_WIDTH")
    require(type(keys) is list and keys == sorted(set(keys)) and all(type(k) is int and
            0 <= k < 49*(grid+1)**2 for k in keys), "MASK_KEYS")
    require(supported(state["x"],grid), "TARGET_STENCIL_OUTSIDE")
    nodes, weights, _, offset = model.stencil(state["x"], grid)
    all_keys, inverse = np.unique((state["ids"][:,None]*(grid+1)**2+nodes).ravel(),return_inverse=True)
    slots = inverse.ravel()
    weight = (40.*grid**2/width)*state["volume"][:,None]*weights
    uy, ux = weight*offset[:,:,1], weight*offset[:,:,0]
    part = dict(yy=uy*state["yy"][:,None],yx=ux*state["yx"][:,None],unit_yy=uy,unit_yx=ux)
    take = np.searchsorted(all_keys, np.asarray(keys,dtype=np.int64))
    safe = np.minimum(take,len(all_keys)-1)
    # Native stencils can list zero-weight endpoints. Positive weight determines geometric support.
    positive = np.bincount(slots,weights=(weights>0.).ravel(),minlength=len(all_keys)) > 0
    found = (take < len(all_keys)) & (all_keys[safe] == keys) & positive[safe]
    result = dict(keys=keys,requested_keys=len(keys),positive_support_keys=int(found.sum()),
                  unsupported_keys=len(keys)-int(found.sum()))
    for name, vals in part.items():
        accumulated=np.bincount(slots,weights=vals.ravel(),minlength=len(all_keys))
        require(np.isfinite(accumulated).all(), "NONFINITE_PROJECTION")
        result[name]=np.where(found,accumulated[safe],0.).tolist()
    return result


def target_projection(model,state,grid,width,keys,native):
    validate(state)
    if not supported(state["x"],grid):
        require(not native, "NATIVE_STENCIL_OUTSIDE")
        return dict(status="UNAVAILABLE_TARGET_STENCIL_OUTSIDE",values=None)
    return dict(status="OK",values=project_state(model,state,grid,width,keys))


def totals(row):
    result = {k:math.fsum(row[k]) for k in COLS}
    return dict(result, stress_MPa=math.fsum([result["yy"],result["yx"]]),
                compression_minus_one_MPa=-result["unit_yy"])


def match_native(actual, target):
    require(actual["keys"] == target["keys"], "NATIVE_MASK")
    for k in COLS:
        left,right=actual[k],target[k]
        require(len(left)==len(right) and all(math.isclose(a,b,abs_tol=1e-12,rel_tol=1e-12)
                                              for a,b in zip(left,right)), "NATIVE_KEY_COLUMN")
        require(math.isclose(math.fsum(left),math.fsum(right),abs_tol=1e-12,rel_tol=1e-12),"NATIVE_SUM")


def contrasts(c):
    cc,cf,fc,ff = (c[k] for k in ((8,8),(8,16),(16,8),(16,16)))
    return dict(native_F8_minus_F16=cc-ff,state_F8_minus_F16_on_F8_target=cc-fc,
                state_F8_minus_F16_on_F16_target=cf-ff,target_F8_minus_F16_at_F8_state=cc-cf,
                target_F8_minus_F16_at_F16_state=fc-ff,interaction=(cc-fc)-(cf-ff))


def endpoints(walls,prefix,i,j):
    require((i,j) in zip(STEPS[8],STEPS[16]) and walls[8][i-1]["u"] == walls[16][j-1]["u"]
            and prefix.DT[8]*i == prefix.DT[16]*j,"NATIVE_COMMON_END")
    return dict(common_end_u=walls[8][i-1]["u"],common_end_time=i*prefix.DT[8],
                incoming_u={n:walls[n][s-2]["u"] for n,s in ((8,i),(16,j))},
                incoming_time={n:(s-1)*prefix.DT[n] for n,s in ((8,i),(16,j))})

def receipt(n,folder):
    names=list(PREFIX_FILES)+[f"state_{i}.npz" for i in STEPS[n]]
    return dict(status=STATUS,cells=n,steps=list(STEPS[n]),prior_probe_sha256=PROBE_RETURN,
                observer_sha256=sha(Path(__file__).read_bytes()),files={k:sha((folder/k).read_bytes()) for k in names})


def match_prefix(old,folder):
    for name in PREFIX_FILES:
        require((folder/name).read_bytes() == old["files"][name], "NATIVE_FILE_MISMATCH")


def arm(prefix,pair,mods,hist,old,n,folder):
    original=prefix.Observer
    geometry=pair.expected_geometry(n)
    class SnapshotObserver(original):
        def advance(self,*args):
            step=len(self.rows)+1
            if step not in STEPS[n]:
                return super().advance(*args)
            x,_,_,elastic,ids,volume,grid,dt,_=args
            require(grid==10*n and dt==prefix.DT[n],"NATIVE_SCHEDULE")
            frozen=snapshot(self.solver,x,elastic,ids,volume)
            bind_seed(frozen,geometry)
            output=super().advance(*args)
            ref=old["projection"][step]
            actual=project_state(self.solver.model,frozen,grid,prefix.WIDTH,ref["keys"])
            match_native(actual,ref)
            save_state(folder/f"state_{step}.npz",frozen)
            return output
    prefix.Observer=SnapshotObserver
    try:
        prefix.arm(pair,mods,hist,n,folder)
    finally:
        prefix.Observer=original
    match_prefix(old,folder)
    prefix.write(folder/"cross_receipt.json",receipt(n,folder))


def read_arm(n,folder,old,geometry):
    match_prefix(old,folder)
    require(json.loads((folder/"cross_receipt.json").read_bytes())==receipt(n,folder),"CROSS_RETURN_IDENTITY")
    states={}
    for step in STEPS[n]:
        with np.load(folder/f"state_{step}.npz",allow_pickle=False) as archive:
            require(len(archive.files)==len(STATE) and set(archive.files)==set(STATE),"STATE_ARCHIVE")
            states[step]={k:archive[k] for k in STATE}
        bind_seed(states[step],geometry)
    return states


def summary(model,prefix,walls,old,states):
    pairs=[]
    for i,j in zip(STEPS[8],STEPS[16]):
        times=endpoints(walls,prefix,i,j)
        corners={}
        for n,s in ((8,i),(16,j)):
            for t,k in ((8,i),(16,j)):
                target=old[t]["projection"][k]
                supplied=target_projection(model,states[n][s],10*t,prefix.WIDTH,target["keys"],n==t)
                entry=dict(source_cells=n,source_step=s,target_cells=t,target_step=k,
                           requested_keys=len(target["keys"]),status=supplied["status"])
                projected=supplied["values"]
                if projected is not None:
                    if n==t:
                        require(projected["unsupported_keys"]==0,"NATIVE_SUPPORT")
                        match_native(projected,target)
                    entry.update(positive_support_keys=projected["positive_support_keys"],
                                 unsupported_keys=projected["unsupported_keys"],values=totals(projected))
                corners[n,t]=entry
        complete=all(q["status"]=="OK" for q in corners.values())
        delta={col:contrasts({k:v["values"][col] for k,v in corners.items()})
               for col in (*COLS,"stress_MPa","compression_minus_one_MPa")} if complete else None
        pairs.append(dict(steps=[i,j],timing=times,corners=list(corners.values()),contrasts=delta,
                          all_corners_available=complete))
    return dict(status=STATUS,label="DEVELOPMENT_ONLY",paired=pairs,native_diagonal_checked=True,
                all_crossed_corners_available=all(p["all_corners_available"] for p in pairs),
                stress_unit="one tensile-positive solver stress; positive upward wall-pressure response in MPa",
                selection="original target mask; equal output displacement; source snapshots are incoming",
                scope="fixed source state, target grid and saved target mask; algebraic projections only",
                u6_qualified=False,stage3_go=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    for name in ("check","arm","read"):
        cmd=sub.add_parser(name)
        for key in ("repo","probe","prior"):
            cmd.add_argument("--"+key,type=Path,required=True)
        if name in ("arm","read"):
            cmd.add_argument("--out",type=Path,required=True)
        if name=="arm":
            cmd.add_argument("--cells",type=int,choices=STEPS,required=True)
        if name=="read":
            cmd.add_argument("--run",type=Path,required=True)
    args=parser.parse_args()
    try:
        p,m,prefix,pair,mods=sources(args.repo)
        solver=mods["driver"].fixed_solver()
        hist,walls,old=histories(args.prior,args.probe,p,m,prefix,pair,solver.LO)
        if args.command=="check":
            for n in STEPS:
                pair.setup_geometry(mods["driver"],solver,n)
            print("CROSS_SOURCES_SEEDS_AND_HISTORIES_BOUND")
        elif args.command=="arm":
            arm(prefix,pair,mods,hist,old[args.cells],args.cells,args.out)
            print(STATUS)
        else:
            states={n:read_arm(n,args.run/f"F{n}",old[n],pair.expected_geometry(n)) for n in STEPS}
            prefix.write(args.out,summary(solver.model,prefix,walls,old,states))
            print(STATUS)
    except (OSError,ArithmeticError,ValueError,TypeError,RuntimeError,KeyError,IndexError,tarfile.TarError) as exc:
        print("HOLD", str(exc) if str(exc).isupper() else type(exc).__name__)
        return 4
    return 0


if __name__=="__main__":
    raise SystemExit(main())
