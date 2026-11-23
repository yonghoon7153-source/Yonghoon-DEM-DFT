"""Read model Mach numbers, floor arrival and initial-layer velocity arrivals without running MPM."""
import argparse
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_depth import CURRENT, HALF, LAYERS, archive, check_prefix, close, hash_bytes, require, table


ORIGINAL = "cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e"
MATERIAL_HASH = "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5"
DRIVER_HASH = "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762"
DIAMETER = .1


def first_sustained(values, threshold, intervals):
    """First sample with the threshold sustained through the endpoint n intervals later."""
    require(intervals >= 0 and threshold > 0 and all(math.isfinite(x) for x in values), "arrival inputs")
    return next((i for i in range(len(values)-intervals)
                 if all(x >= threshold for x in values[i:i+1+intervals])), None)


def layer_arrivals(trace, layer_rows, masses, speed, cells):
    require(len(trace) == len(layer_rows)+1 and cells in (12,24), "layer/trace length or grid")
    require(len(masses) == 3 and min(masses) > 0 and speed > 0, "initial layer masses or speed")
    intervals = 2*(cells//12)
    results = {}
    for k,mass in zip(LAYERS,masses,strict=True):
        v = [0.] + [-float(r[k+"_after"])/(mass*speed) for r in layer_rows]
        marks = {}
        for threshold in (.05,.10,.20):
            i = first_sustained(v,threshold,intervals)
            marks[f"{threshold:.2f}"] = None if i is None else location(trace,i)
        results[k] = marks
    return results


def location(trace,i):
    return dict(step=i, time_code=float(trace[i]["time_code"]),
                displacement_D=(float(trace[0]["height"])-float(trace[i]["height"]))/DIAMETER)


def reference_speeds(source_manifest, v, sample_dt):
    expected = {"suyoung_u6_first_dev.py":MATERIAL_HASH, "suyoung_u6b_dev.py":DRIVER_HASH}
    for name, digest in expected.items():
        require(any(line.startswith(digest+"  ") and line.endswith("/"+name)
                    for line in source_manifest.decode().splitlines()), "material/driver source binding")
    # E=1, nu=.45, rho=1 in the actual U6 solver. The CFL uses lambda+2*mu.
    E,nu,rho = 1.,.45,1.
    mu = E/(2*(1+nu))
    lam = E*nu/((1+nu)*(1-2*nu))
    cp,cs = math.sqrt((lam+2*mu)/rho), math.sqrt(mu/rho)
    close(v,.034*cs,"prescribed original speed")
    for n,dt in sample_dt.items():
        close(dt,.35/((n/DIAMETER)*cp),"wave speed vs frozen CFL clock")
    return dict(E=E, nu=nu, rho=rho, mu=mu, lam=lam, c_P=cp, c_S=cs,
                speeds={s:dict(v=v*f, Mach_P=v*f/cp, Mach_S=v*f/cs) for s,f in
                        (("original",1.),("half",.5),("quarter_planned",.25))})


def evaluate(depth_path, half_path, original_path):
    dep,half,old = (archive(p,d) for p,d in ((depth_path,CURRENT),(half_path,HALF),(original_path,ORIGINAL)))
    hs = json.loads(half["run/summary.json"])
    speed = hs["original_wall_speed"]
    require(hs["half_wall_speed"] == speed/2 and hs["original_speed_material_lid_sha256"] == ORIGINAL, "velocity lineage")
    contacts, layer, dt, waves, specs = {}, {}, {}, {}, {}
    for n in (12,24):
        key = f"run/F{n}/"
        events = {}
        for run, speed_factor, files in (("original",1,old),("half",.5,half)):
            tr,wr = (table(files[key+s]) for s in ("trace.csv","wall_steps.csv"))
            i = next(i for i,r in enumerate(wr,1) if float(r["floor_impulse"]) > 0.)
            gap_zero = next(i for i,r in enumerate(wr,1) if float(r["floor_gap_after"]) <= 0.)
            require(i == gap_zero, "first floor force vs first closed gap")
            events[run] = loc = location(tr,i)
            close(loc["time_code"]*speed*speed_factor/DIAMETER,loc["displacement_D"],"arrival displacement")
        o,h = events["original"],events["half"]
        expected = o["displacement_D"]/2
        events.update(half_D_if_same_arrival_time=expected, half_D_excess=h["displacement_D"]-expected,
                      displacement_ratio=h["displacement_D"]/o["displacement_D"],
                      half_over_original_time=h["time_code"]/o["time_code"])
        contacts[str(n)] = events
        rec = json.loads(dep[key+"layer_receipt.json"])
        specs[str(n)] = rec["layer_spec"]
        require(rec["layer_sha256"]==hash_bytes(dep[key+"layer_steps.csv"]), "layer receipt")
        check_prefix(dep[key+"trace.csv"],half[key+"trace.csv"],rec["steps"]+1)
        trace = table(dep[key+"trace.csv"])
        dt[n] = float(trace[1]["time_code"])
        layer[str(n)] = layer_arrivals(trace,table(dep[key+"layer_steps.csv"]),rec["layer_spec"]["masses"],speed/2,n)
    for run in ("original","half"):
        waves[run] = contacts["24"][run]["time_code"]/contacts["12"][run]["time_code"]
    delay = {k:layer["24"][k]["0.10"]["time_code"]/layer["12"][k]["0.10"]["time_code"]-1 for k in LAYERS}
    return dict(material=reference_speeds(half["run/SOURCE_SHA256SUMS"],speed,dt),floor_contact=contacts,
                floor_time_ratio_F24_over_F12=waves,half_layer_arrivals=layer,half_layer_relative_grid_delay=delay,
                initial_layer_specs=specs,original_layer_arrivals=None,quarter_result=None,qualification="HOLD")


def speed_comparison(before, after, fraction):
    """Factor the travel ratio into the prescribed speed ratio and measured arrival-time ratio."""
    ratios = {}
    for n in ("12","24"):
        ratios[n] = {}
        for layer in LAYERS:
            a,b = before[n][layer]["0.10"],after[n][layer]["0.10"]
            rec = None
            if a is not None and b is not None:
                t = b["time_code"]/a["time_code"]
                u = b["displacement_D"]/a["displacement_D"]
                close(u,fraction*t,"layer travel vs speed and time")
                rec = dict(speed_ratio=fraction, time_ratio=t, travel_ratio=u,
                           travel_D_at_constant_arrival_time=fraction*a["displacement_D"],
                           travel_D_beyond_constant_time=b["displacement_D"]-fraction*a["displacement_D"])
            ratios[n][layer] = rec
    return ratios


def add_observation(result, options, kind, original_path):
    path,digest,release = options
    files = archive(Path(path),digest)
    s = json.loads(files["run/summary.json"])
    quarter = kind=="quarter"
    status = "QUARTER_SPEED_PREFIX_COMPLETE" if quarter else "ORIGINAL_LAYER_COMPLETE"
    require(s["release"]==release==files["run/RELEASE"].decode().strip()
            and s["status"]==status and s["label"]=="DEVELOPMENT_ONLY"
            and all(s[k] is False for k in ("u6_qualified","stage3_go","three_dimensional_go"))
            and s["source_sha256"]==hash_bytes(files["run/SOURCE_SHA256SUMS"])
            and files["run/screen.txt"].splitlines()[-1]==b"COMMAND_RC=0","new observation identity")
    lineage = ("depth_sha256","half_sha256","material_sha256") if quarter else (
        "half_depth_sha256","half_return_sha256","original_return_sha256")
    require(tuple(s[k] for k in lineage) == (CURRENT,HALF,ORIGINAL),"new history hashes")
    v=result["material"]["speeds"]["quarter_planned" if quarter else "original"]["v"]
    source = None if quarter else archive(original_path, ORIGINAL)
    measured = {}
    for n in (12,24):
        key=f"run/F{n}/"
        receipt=json.loads(files[key+("quarter_speed_receipt.json" if quarter else "layer_receipt.json")])
        require(receipt==s["arms"][str(n)] and receipt["release"]==release
                and receipt["layer_spec"]==result["initial_layer_specs"][str(n)], "new arm receipt or seed identity")
        trace, layers=files[key+"trace.csv"],files[key+"layer_steps.csv"]
        require(hash_bytes(trace)==receipt["trace_sha256"] and hash_bytes(layers)==receipt["layer_sha256"],"new layer hashes")
        tr=table(trace)
        if source is not None:
            check_prefix(trace,source[key+"trace.csv"],len(tr))
            check_prefix(files[key+"wall_steps.csv"],source[key+"wall_steps.csv"],len(tr)-1)
        for i,r in enumerate(tr):
            require(r["step"]==str(i),"new clock")
            close(location(tr,i)["displacement_D"],float(r["time_code"])*v/DIAMETER,"new travel vs speed")
        measured[str(n)]=layer_arrivals(tr,table(layers),receipt["layer_spec"]["masses"],v,n)
    if quarter:
        result["quarter_layer_arrivals"]=measured
        result["half_to_quarter_layer_scaling"]=speed_comparison(result["half_layer_arrivals"],measured,.5)
        result["quarter_result"]=s["pressure_union"]["quarter_on_common_1139"]
    else:
        result["original_layer_arrivals"]=measured
        result["original_to_half_layer_scaling"]=speed_comparison(measured,result["half_layer_arrivals"],.5)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("depth","half","original","out"):
        cli.add_argument(name, type=Path)
    for name in ("original","quarter"):
        cli.add_argument("--"+name+"-layers", nargs=3, metavar=("TAR","SHA256","RELEASE"))
    args = cli.parse_args()
    result=evaluate(args.depth,args.half,args.original)
    for kind,options in (("original",args.original_layers),("quarter",args.quarter_layers)):
        if options is not None:
            add_observation(result,options,kind,args.original)
    args.out.write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())
