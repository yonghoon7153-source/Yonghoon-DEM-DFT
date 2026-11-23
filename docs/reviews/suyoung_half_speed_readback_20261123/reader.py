"""Read pressures, wall impulses and measured particle momentum from two frozen returns."""
import argparse
from bisect import bisect_left
from dataclasses import dataclass
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


REF_MPA = 0.6636991102836952
DIAMETER = 0.1
PRIOR = "cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e"
CURRENT = "ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863"
ORIGINAL_PIN = "35099db02148c1a5dc2581f880e0adbf28c0368d"
HALF_PIN = "ba0e2bb980a4f098aee6ee526d069ed2d2446151"
BASELINE = "1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e"
SPEED = 0.01996548746349992
DT = {12: 0.001497578010986372, 24: 0.000748789005493186}


def check(ok, what):
    if not ok:
        raise ValueError(what)


def equal(a, b, what):
    check(math.isclose(a, b, abs_tol=1e-13, rel_tol=1e-12), what)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_files(path, expected):
    raw = path.read_bytes()
    check(digest(raw) == expected, "return archive hash")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        files = {}
        for member in tar:
            if member.isdir():
                continue
            check(member.isfile() and member.name.startswith("run/") and member.name not in files, "return member")
            files[member.name] = tar.extractfile(member).read()
        return files


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"))))


@dataclass
class Arm:
    heights: list
    pressure: list
    time: list
    floor: list
    lid: list
    py: list
    dt: float
    width: float
    residual_J: float


def arm_data(files, summary, cells, half):
    name = f"run/F{cells}/"
    get = lambda key: files[name + key]
    trace, wall = get("trace.csv"), get("wall_steps.csv")
    rec = json.loads(get("candidate_receipt.json"))
    record = summary["arms"][str(cells)]
    if half:
        check(record == json.loads(get("half_speed_receipt.json")) and all(record[k] == v for k, v in rec.items()), "half receipt")
        motion = get("particle_momentum.csv")
        check(record["particle_momentum_sha256"] == digest(motion), "momentum digest")
        motion = rows(motion)
    else:
        check(record == rec, "original receipt")
        motion = None
    check(rec["release"] == summary["release"] and rec["source_sha256"] == summary["source_sha256"] and
          rec["trace_sha256"] == digest(trace) and rec["wall_csv_sha256"] == digest(wall), "arm binding")
    tr, wr = rows(trace), rows(wall)
    steps = (569 if cells == 12 else 1138) * (2 if half else 1)
    check(len(tr) == steps+1 and len(wr) == rec["steps"] == steps and
          (motion is None or len(motion) == record["particle_momentum_rows"] == steps), "arm counts")
    heights = [float(r["height"]) for r in tr]
    time = [float(r["time_code"]) for r in tr]
    pressure = [10*float(r["bottom_pressure_E"]) for r in tr]
    width = heights[0]
    dt = DT[cells]
    floor, lid, py = [0.], [0.], [0.]
    max_residual = 0.
    for i, r in enumerate(tr):
        check(r["step"] == str(i) and time[i] == i*dt and heights[i] == width-i*dt*SPEED/(2 if half else 1)
              and math.isfinite(pressure[i]) and pressure[i] >= 0, "drive coordinates")
        if i == 0:
            continue
        w = wr[i-1]
        f, l = float(w["floor_impulse"]), float(w["lid_signed_impulse"])
        check(w["step"] == str(i) and f >= 0 and l <= 0 and float(w["lid_downward_impulse"]) == -l, "wall impulse")
        equal(pressure[i], 10*f/(width*dt), "floor pressure")
        floor.append(f)
        lid.append(l)
        if motion is not None:
            m = motion[i-1]
            check(m["step"] == str(i) and float(m["particle_Py_before"]) == py[-1], "momentum continuity")
            next_py = float(m["particle_Py_after"])
            delta, net = next_py-py[-1], math.fsum((f, l))
            residual = delta-net
            check(float(m["particle_delta_Py"]) == delta and float(m["wall_signed_J"]) == net and
                  float(m["residual_J"]) == residual and abs(residual) <= 2e-12*max(1.,f,-l,abs(next_py),abs(py[-1])),
                  "particle and signed walls")
            max_residual = max(max_residual, abs(residual))
            py.append(next_py)
    if half:
        check(max_residual == record["max_absolute_particle_wall_residual_J"], "momentum residual peak")
    return Arm(heights, pressure, time, floor, lid, py if half else [], dt, width, max_residual)


def pressure_curve(arms, knots):
    left, right = arms[12], arms[24]
    coarse = [-v for v in left.heights]
    fine = [-v for v in right.heights]
    curve = []
    for h in knots:
        ix = bisect_left(coarse, -h)
        iy = bisect_left(fine, -h)
        check(ix < len(coarse) and iy < len(fine) and fine[iy] == -h, "pressure knot outside observed range")
        if coarse[ix] == -h:
            p12, sample = left.pressure[ix], ix
        else:
            check(ix > 0, "pressure interpolation below range")
            weight = (-h-coarse[ix-1])/(coarse[ix]-coarse[ix-1])
            p12 = left.pressure[ix-1]+weight*(left.pressure[ix]-left.pressure[ix-1])
            sample = None
        p24 = right.pressure[iy]
        curve.append(dict(displacement_D=(left.width-h)/DIAMETER, F12_step=sample, F24_step=iy,
                          F12_MPa=p12, F24_MPa=p24, gap_MPa=p12-p24))
    return curve


def window(arm, end, count):
    lo = end-count+1
    factor = 10/(arm.width*arm.dt*count)
    floor = math.fsum(arm.floor[lo:end+1])
    lid = math.fsum(arm.lid[lo:end+1])
    return dict(steps=[lo, end], floor_MPa=floor*factor, lid_down_MPa=-lid*factor,
                ratio=floor/-lid if lid else None, wall_net_MPa=math.fsum((floor, lid))*factor,
                particle_delta_MPa=(arm.py[end]-arm.py[lo-1])*factor if arm.py else None)


def force_comparison(arms, sample):
    x, y = sample["F12_step"], sample["F24_step"]
    if x is None or x == 0:
        return None
    check(arms[12].time[x] == arms[24].time[y], "different step ends")
    a, b, b2 = window(arms[12], x, 1), window(arms[24], y, 1), window(arms[24], y, 2)
    def diff(right):
        return {k: a[k]-right[k] if a[k] is not None else None for k in
                ("floor_MPa", "lid_down_MPa", "wall_net_MPa", "particle_delta_MPa")}
    return dict(F12=a, F24=b, F24_equal_duration=b2, gap=diff(b), equal_duration_gap=diff(b2))


def summary_features(data, curve, expected):
    peak = max(curve, key=lambda r: abs(r["gap_MPa"]))
    first = next((r for r in curve if abs(r["gap_MPa"]) > .05*REF_MPA), None)
    check(len(curve) == expected["samples"], "comparison knot count")
    def compare_point(p, q):
        check((p is None) == (q is None), "first crossing presence")
        if p is not None:
            for lhs,rhs in (("displacement_D","displacement_diameters"), ("F12_MPa","F12_MPa"),
                            ("F24_MPa","F24_MPa"), ("gap_MPa","signed_gap_MPa")):
                equal(p[lhs], q[rhs], "different pressure summary")
    compare_point(peak, expected["peak"])
    compare_point(first, expected["first_above"])
    equal(abs(peak["gap_MPa"])*100/REF_MPA, expected["fixed_reference_percent"], "peak percentage")
    return dict(samples=len(curve), peak=peak, first_above_5pct=first,
                peak_pct=100*abs(peak["gap_MPa"])/REF_MPA, peak_walls=force_comparison(data, peak))


def evaluate(half_return, material_return):
    archives = (read_files(material_return, PRIOR), read_files(half_return, CURRENT))
    summaries, datasets = [], []
    for files, pin in zip(archives,(ORIGINAL_PIN, HALF_PIN),strict=True):
        summary = json.loads(files["run/summary.json"])
        check(summary["release"] == pin == files["run/RELEASE"].decode().strip() and
              summary["source_sha256"] == digest(files["run/SOURCE_SHA256SUMS"]), "run source binding")
        screen = files["run/screen.txt"].splitlines()
        check(screen[-1] == b"COMMAND_RC=0" and b"F12_RC=0" in screen and b"F24_RC=0" in screen, "run completion")
        check(summary["reference_MPa"] == REF_MPA and summary["label"] == "DEVELOPMENT_ONLY" and
              all(summary[k] is False for k in ("u6_qualified","stage3_go","three_dimensional_go")), "development status")
        half = pin == HALF_PIN
        if half:
            check(summary["status"] == "HALF_SPEED_PREFIX_COMPLETE" and summary["baseline_sha256"] == BASELINE
                  and summary["original_speed_material_lid_sha256"] == PRIOR and
                  summary["half_wall_speed"] == .5*summary["original_wall_speed"] == .5*SPEED, "previous return binding")
        datasets.append({n:arm_data(files,summary,n,half) for n in (12,24)})
        summaries.append(summary)
    original, half = datasets
    for n in (12, 24):
        check(original[n].heights == half[n].heights[::2], "speed pair has different matched displacements")
    p, q = summaries
    native0 = pressure_curve(original, original[24].heights)
    common = pressure_curve(half, original[24].heights)
    dense = pressure_curve(half, half[24].heights)
    p0 = summary_features(original,native0,p["new_material_lid"])
    summary_features(original,native0,q["pressure_union"]["original_native_1139"])
    ph = summary_features(half,common,q["pressure_union"]["half_on_original_1139"])
    ph_all = summary_features(half,dense,q["pressure_union"]["half_native_2277"])
    # Within one speed the two grids share a physical clock. Across speeds the
    # same clock is a different plate displacement and is only a timing diagnostic.
    shared_clock = []
    for event, end in (("half_first_common_above", ph["first_above_5pct"]["F24_step"]),
                       ("original_peak", p0["peak"]["F24_step"]),
                       ("half_peak", ph_all["peak"]["F24_step"])):
        original_time, half_time = original[24].time[end], half[24].time[end]
        check(original_time == half_time, "unequal diagnostic clocks")
        at_clock = {"event": event, "F24_step": end, "time_code": original_time}
        for label, pair, at in (("original", original, native0[end]), ("half", half, dense[end])):
            measured = force_comparison(pair, at)
            at_clock[label] = dict(displacement_D=at["displacement_D"], floor_gap_MPa=at["gap_MPa"],
                                   signed_wall_gaps_MPa=measured["gap"] if measured is not None else None)
        shared_clock.append(at_clock)
    fixed = []
    for t in (930,1138):
        record = dict(displacement_D=native0[t]["displacement_D"])
        for j, (key, data, sample) in enumerate((("original",original,native0[t]),("half",half,common[t]))):
            item = force_comparison(data, sample)
            win = q[("original_fixed_windows","half_fixed_windows")[j]][len(fixed)]
            for lhs,rhs in (("F12","F12_native"),("F24","F24_native"),("F24_equal_duration","F24_same_duration_two_steps")):
                equal(item[lhs]["ratio"],win[rhs]["floor_over_abs_lid"], "fixed wall ratio")
            equal(item["gap"]["wall_net_MPa"], win["F12_minus_F24_native"]["inferred_delta_Py_equivalent_MPa"], "fixed wall net")
            if key == "half":
                equal(item["gap"]["particle_delta_MPa"],win["F12_minus_F24_native"]["direct_delta_Py_equivalent_MPa"], "fixed particle delta")
            record[key] = dict(signed_pct=100*sample["gap_MPa"]/REF_MPA, **sample, **item)
        fixed.append(record)
    starts = {}
    for label, arms in (("original", original), ("half", half)):
        starts[label] = {}
        for n, arm in arms.items():
            def start(step):
                return dict(step=step, displacement_D=(arm.width-arm.heights[step])/DIAMETER, time_code=arm.time[step])
            starts[label][f"F{n}"] = dict(first_positive_floor=start(next(i for i,f in enumerate(arm.floor) if f > 0)),
                                          first_downward_lid=start(next(i for i,l in enumerate(arm.lid) if l < 0)))
    return dict(original_tar_sha256=PRIOR, half_speed_tar_sha256=CURRENT, release=HALF_PIN,
                status="DEVELOPMENT_ONLY", U6c="HOLD", stage3="HOLD", three_dimensional="HOLD",
                reference_MPa=REF_MPA, original_common=p0, half_common=ph, half_native=ph_all,
                original_peak_delta_MPa=abs(p0["peak"]["gap_MPa"])-abs(ph["peak"]["gap_MPa"]),
                max_abs_particle_wall_residual_J={"F12":half[12].residual_J,"F24":half[24].residual_J},
                first_observed_impulses=starts, same_clock_diagnostic=shared_clock, fixed=fixed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("half_return", "material_return"):
        parser.add_argument(key, type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = evaluate(args.half_return, args.material_return)
    text = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if args.json:
        args.json.write_bytes(text.encode("ascii"))
    else:
        print(text, end="")
