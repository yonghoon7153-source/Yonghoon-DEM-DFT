"""Read the three directly observed material-layer returns. No MPM import or simulation."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


SPEEDS = ("original", "half", "quarter")
GRIDS = (12, 24)
LAYERS = ("lower", "middle", "upper")
SHA256 = {
    "original": "835993a11053b31bfd1174941ecb043fc1f65a46f423cd6820b86d9890c94142",
    "half": "cd9b0e6b9ce31719716b3ae4b9f97734a7a4ba3614c7de7bd3d93d44f3be83e6",
    "quarter": "5bee9a0cc9f92ba88fd7039444c7efb71bb8946c84912159d6a23838f8399d04",
}
RELEASE = "4a56e468c931e024d08f5476df9ccb0237694741"
HALF_RELEASE = "9638542795ed98edf8b1c9ac52d88c3a0e2f8f3b"
DIAMETER = .1


def require(ok, explanation):
    if not ok:
        raise ValueError(explanation)


def csv_rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("ascii"))))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def close(a, b):
    return math.isclose(a, b, rel_tol=5e-12, abs_tol=1e-13)


def arrival_index(rows, column, threshold_py, sample_count):
    """Return first saved step in first run of consecutive qualifying samples."""
    count = 0
    for row in rows:
        count = count + 1 if -float(row[column]) >= threshold_py else 0
        if count == sample_count:
            return int(row["step"]) - count + 1
    return None


def momentum_window(rows, step, count, dt, width):
    """Up is positive. Bottom pressure difference = material rate plus downward top load."""
    require(0 < count <= step <= len(rows), "momentum window out of bounds")
    window = rows[step-count:step]
    scale = 10/(dt*count*width)
    result = {}
    for key in LAYERS:
        result[key] = scale*math.fsum(float(r[key+"_after"])-float(r[key+"_before"]) for r in window)
    result["whole"] = scale*math.fsum(float(r["whole_after"])-float(r["whole_before"]) for r in window)
    result["lid_down"] = -scale*math.fsum(float(r["lid_signed_J"]) for r in window)
    result["floor"] = scale*math.fsum(float(r["floor_J"]) for r in window)
    require(abs(sum(result[k] for k in LAYERS)-result["whole"]) < 5e-11, "layer sum at maximum")
    require(abs(result["whole"]+result["lid_down"]-result["floor"]) < 5e-11, "two-wall momentum balance at maximum")
    return result


def read_run(case, path, peak):
    raw = path.read_bytes()
    require(digest(raw) == SHA256[case], "return hash for " + case)
    expected_pin = HALF_RELEASE if case == "half" else RELEASE
    results = {}
    windows = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        def member(path):
            return archive.extractfile("run/" + path).read()
        summary = json.loads(member("summary.json"))
        require(member("RELEASE").decode().strip() == summary["release"] == expected_pin, "source pin")
        speed = summary[{"original":"wall_speed","half":"half_speed","quarter":"quarter_wall_speed"}[case]]
        for grid in GRIDS:
            prefix = f"F{grid}/"
            receipt_name = "quarter_speed_receipt.json" if case == "quarter" else "layer_receipt.json"
            rec = json.loads(member(prefix + receipt_name))
            require(rec == summary["arms"][str(grid)], "receipt vs summary")
            buffers = [member(prefix + name) for name in ("trace.csv","layer_steps.csv","wall_steps.csv")]
            require([digest(b) for b in buffers] == [rec["trace_sha256"],rec["layer_sha256"],rec.get("wall_sha256",rec.get("wall_csv_sha256"))], "CSV receipt hashes")
            trace, layers, wall = map(csv_rows, buffers)
            require(len(trace) == len(layers)+1 == len(wall)+1 == int(rec["steps"])+1, "saved steps")
            require(all(int(t["step"]) == i for i,t in enumerate(trace)), "trace step numbering")
            require(all(int(l["step"]) == int(w["step"]) == i for i,(l,w) in enumerate(zip(layers,wall),1)), "observation step numbering")
            height = float(trace[0]["height"])
            def event(step):
                if step is None:
                    return None
                t = float(trace[step]["time_code"])
                d = (height - float(trace[step]["height"]))/DIAMETER
                require(close(d, t*speed/DIAMETER), "prescribed plate speed")
                return {"step":step, "time":t, "travel_D":d}
            first_floor = next(int(w["step"]) for w in wall if float(w["floor_impulse"]) > 0)
            require(first_floor == next(int(w["step"]) for w in wall if float(w["floor_gap_after"]) <= 0), "floor contact vs first closed gap")
            masses = rec["layer_spec"]["masses"]
            for l in layers:
                require(close(sum(float(l[k+"_after"]) for k in LAYERS), float(l["whole_after"])), "sum of labeled material momentum")
            thresholds = {}
            for alpha in (.05,.10,.20):
                thresholds[str(alpha)] = {
                    name:event(arrival_index(layers,name+"_after",alpha*speed*mass,1+2*grid//12))
                    for name,mass in zip(LAYERS,masses,strict=True)
                }
            results[str(grid)] = {"speed":speed,"initial_label_hash":rec["layer_spec"]["label_sha256"],
                                  "first_floor":event(first_floor),"thresholds":thresholds}
            factor = {"original":1,"half":2,"quarter":4}[case]
            pin_step = peak.get("step_F24_original",peak.get("step_F24")) * factor
            require(pin_step % 2 == 0, "maximum must be sampled by both arms")
            index = pin_step*grid//24
            dt = float(trace[1]["time_code"])
            require(close(event(index)["travel_D"],peak["displacement_diameters"]), "common maximum travel")
            # In this square 2D geometry the initial trace height equals plate width.
            windows[grid] = {}
            for convention, nsteps in (("native",1),("equal_duration",grid//12)):
                row = momentum_window(layers,index,nsteps,dt,height)
                csv_pressure = 10*float(trace[index]["bottom_pressure_E"])
                require(close(csv_pressure,peak[f"F{grid}_MPa"]), "maximum trace vs frozen pressure")
                if convention == "native":
                    require(close(csv_pressure,row["floor"]), "force units at each native maximum")
                row["first_step"] = index-nsteps+1
                row["last_step"] = index
                windows[grid][convention] = row
    differences = {}
    for name in ("native", "equal_duration"):
        differences[name] = {k:windows[12][name][k] - windows[24][name][k] for k in (*LAYERS,"whole","lid_down","floor")}
    require(close(differences["native"]["floor"],peak["signed_gap_MPa"]), "pressure maximum")
    return results, {"travel_D": peak["displacement_diameters"], "step_F24_original": peak.get("step_F24_original",peak.get("step_F24")),
                     "F12":windows[12],"F24":windows[24],"F12_minus_F24":differences}


def read_all(paths):
    require(digest(paths[2].read_bytes()) == SHA256["quarter"], "quarter archive identity")
    with tarfile.open(paths[2], mode="r:gz") as z:
        union = json.load(z.extractfile("run/summary.json"))["pressure_union"]
    peaks = {s:union[s+"_on_common_1139"]["peak"] for s in SPEEDS}
    readouts, windows = {}, {}
    for speed,path in zip(SPEEDS,paths,strict=True):
        readouts[speed], windows[speed] = read_run(speed,path,peaks[speed])
    for grid in ("12","24"):
        require(len({readouts[s][grid]["initial_label_hash"] for s in SPEEDS}) == 1,"same initial material layers")
    delays, step_scaling = {}, {}
    for speed, result in readouts.items():
        coarse, fine = result["12"], result["24"]
        delays[speed] = {}
        for alpha in (.05,.10,.20):
            thresholds = {}
            for layer in (*LAYERS, "floor"):
                a,b = (c["first_floor"] if layer == "floor" else c["thresholds"][str(alpha)][layer] for c in (coarse,fine))
                thresholds[layer] = None if a is None or b is None else (b["time"]/a["time"]-1)*100
            delays[speed][str(alpha)] = thresholds
    for fast, slow in zip(SPEEDS[:-1],SPEEDS[1:]):
        rows = {}
        for grid in ("12", "24"):
            a,b = readouts[fast][grid],readouts[slow][grid]
            rows[grid] = {}
            for label in (*LAYERS,"floor"):
                prev,next_ = (c["first_floor"] if label == "floor" else c["thresholds"]["0.1"][label] for c in (a,b))
                if prev is None or next_ is None:
                    rows[grid][label] = None
                    continue
                t_ratio = next_["time"]/prev["time"]
                d_ratio = next_["travel_D"]/prev["travel_D"]
                require(close(d_ratio, .5*t_ratio), "velocity and travel scaling")
                rows[grid][label] = {"time_ratio":t_ratio,"travel_ratio":d_ratio,"travel_excess_D":next_["travel_D"]-.5*prev["travel_D"]}
        step_scaling[fast+"_to_"+slow] = rows
    return {"scope":"DEVELOPMENT_ONLY","input_sha256":SHA256,"events":readouts,
            "F24_delay_percent_relative_to_F12":delays,"successive_speed_pairs_10pct":step_scaling,
            "momentum_at_each_speeds_1139_sample_maximum_MPa":windows}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for name in (*SPEEDS, "output"):
        cli.add_argument(name,type=Path)
    args = cli.parse_args()
    data = read_all([args.original,args.half,args.quarter])
    args.output.write_bytes((json.dumps(data,indent=2,allow_nan=False)+"\n").encode("ascii"))
