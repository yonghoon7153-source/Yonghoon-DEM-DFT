"""One F8 half-time-step sensitivity run and read-only comparison against F8/F16."""
import argparse
from bisect import bisect_left
import csv
from dataclasses import dataclass
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import tarfile


CONTROL = "U6c-F8-half-native-dt-v1"
NATIVE = "U6b-setting1-bottom-loading-v1"
PRIOR_SHA = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
SOURCE = {
    "suyoung_u6b_dev.py":"50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "suyoung_u6_first_dev.py":"5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py":"6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
TRACE = {8:"03f3bc2c106aa466f1ccc2b774e0b768f2a902792006609680faa53038434cdf",
         16:"5475cc87df297533002afb621cbdac06c0319ca40eb65ddf40322ae6c018b0de"}
COLUMNS = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
GAPS = ("original_F8_minus_F16", "F8_minus_F8_half_dt", "F8_half_dt_minus_F16")
SPEED = .034 * math.sqrt(1. / (2. * (1. + .45)))


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, report):
    with path.open("x", encoding="ascii", newline="\n") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def integrate(driver, budget, out):
    original = driver.step_size

    def half_dt(solver, cells):
        require(cells == 8, "UNEXPECTED_RESOLUTION")
        dt = original(solver, 8) * .5
        require(dt == original(solver, 16), "REFERENCE_TIME_STEP_MISMATCH")
        return dt

    driver.step_size = half_dt
    try:
        return driver.run_arm("F", 8, budget, out)
    finally:
        driver.step_size = original


def run_command(directory, budget, out):
    for name, digest in SOURCE.items():
        require(sha((directory/name).read_bytes()) == digest, "SOURCE_MISMATCH")
    spec = importlib.util.spec_from_file_location("private_F8_dt_driver", directory/"suyoung_u6b_dev.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    native = integrate(driver, budget, out)
    trace_sha = sha((out/"trace.csv").read_bytes())
    require(native["trace_sha256"] == trace_sha, "TRACE_BINDING")
    receipt = {"protocol":CONTROL, "source_sha256":SOURCE, "native_dt_multiplier":.5,
               "cells":8, "arm":"F", "only_changed_parameter":"time_step", "status":native["status"],
               "tool_sha256":sha(Path(__file__).read_bytes()), "trace_sha256":trace_sha,
               "native_result_sha256":sha((out/"result.json").read_bytes()),
               "label":"DEVELOPMENT_ONLY", "u6_qualified":False}
    write_json(out/"dt_control.json", receipt)
    print(native["status"])
    return 0 if native["status"] == "TARGET_BRACKETED" else 4


@dataclass(frozen=True)
class Curve:
    u: tuple
    p: tuple

    def at(self, u):
        j = bisect_left(self.u, u)
        if j < len(self.u) and self.u[j] == u:
            return self.p[j]
        require(0 < j < len(self.u), "OUTSIDE_COMMON_SUPPORT")
        t = (u-self.u[j-1])/(self.u[j]-self.u[j-1])
        return self.p[j-1] + t*(self.p[j]-self.p[j-1])


def parse_curve(data, steps, dt, width, speed):
    reader = csv.DictReader(io.StringIO(data.decode("ascii"), newline=""))
    require(tuple(reader.fieldnames or ()) == COLUMNS, "TRACE_COLUMNS")
    xs, ps = [], []
    for i, row in enumerate(reader):
        require(None not in row and None not in row.values() and row["step"] == str(i), "STEP_SEQUENCE")
        t, h, p, phi = (float(row[key]) for key in COLUMNS[1:])
        require(t == dt*i and h == width-dt*i*speed and h >= .75*width, "NATIVE_SCHEDULE")
        require(math.isfinite(p) and p >= 0 and (i != 0 or p == 0.), "INVALID_REACTION")
        require(math.isclose(phi, 49*math.pi*.05**2/(width*h), rel_tol=1e-12), "SEED_AREA")
        u = width-h
        require(not xs or u > xs[-1], "DISPLACEMENT_ORDER")
        require(p < .12 if i < steps else p >= .12, "FIRST_PRESSURE_CROSSING")
        xs.append(u)
        ps.append(10.*p)
    require(steps > 0 and len(xs) == steps+1, "STEP_COUNT")
    return Curve(tuple(xs), tuple(ps))


def load_prior(path):
    raw = path.read_bytes()
    require(sha(raw) == PRIOR_SHA, "PRIOR_ARCHIVE_IDENTITY")
    curves, receipts = {}, {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        def data(name):
            item = tar.getmember(name)
            require(item.isfile(), "PRIOR_MEMBER_TYPE")
            return tar.extractfile(item).read()

        for n in (8, 16):
            prefix = f"run/arms/F{n}/"
            native = json.loads(data(prefix+"result.json"))
            obs = json.loads(data(prefix+"observer.json"))
            trace = data(prefix+"trace.csv")
            require(sha(trace) == native["trace_sha256"] == TRACE[n], "PRIOR_TRACE_BINDING")
            curves[n] = parse_curve(trace, native["steps"], obs["dt"], obs["width"], SPEED)
            receipts[n] = {"dt":obs["dt"], "width":obs["width"], "points_count":native["points_count"]}
        peak = json.loads(data("run/wall_summary.json"))["decomposition"]
    require(receipts[8]["dt"]*.5 == receipts[16]["dt"] and
            receipts[8]["width"] == receipts[16]["width"], "PRIOR_NORMALIZATION")
    return curves, receipts, peak


def check_native(native, control, data, expected_points):
    require(native.get("status") == "TARGET_BRACKETED", "INCOMPLETE_NATIVE")
    require((native["protocol"], native["label"], native["setting"], native["arm"], native["cells"],
             native["origin"], native["points_count"]) ==
            (NATIVE, "DEVELOPMENT_ONLY", 1, "F", 8, "new", expected_points), "NATIVE_BINDING")
    require(native["source_sha256"] == {k:v for k,v in SOURCE.items() if k != "suyoung_u6b_dev.py"},
            "NATIVE_SOURCE_BINDING")
    require((control["protocol"], control["label"], control["arm"], control["cells"],
             control["native_dt_multiplier"], control["status"], control["only_changed_parameter"]) ==
            (CONTROL, "DEVELOPMENT_ONLY", "F", 8, .5, native["status"], "time_step") and
            control["u6_qualified"] is False and control["source_sha256"] == SOURCE and
            control["tool_sha256"] == sha(Path(__file__).read_bytes()), "CONTROL_BINDING")
    require(sha(data) == control["trace_sha256"] == native["trace_sha256"], "CONTROL_TRACE_BINDING")


def compare(coarse, fine, half):
    end = min(coarse.u[-1], fine.u[-1])
    old_knots = sorted({u for curve in (coarse,fine) for u in curve.u if u <= end})
    anchor = max(old_knots, key=lambda x: abs(coarse.at(x)-fine.at(x)))
    common = min(end, half.u[-1])
    knots = sorted({u for curve in (coarse,fine,half) for u in curve.u if u <= common})

    def observation(u):
        c, f, h = (curve.at(u) for curve in (coarse,fine,half))
        gaps = (c-f, c-h, h-f)
        require(abs(gaps[0]-gaps[1]-gaps[2]) <= 8*math.ulp(max(abs(c),abs(f),abs(h))), "GAP_CLOSURE")
        return {"u":u, "F8_MPa":c, "F16_MPa":f, "F8_half_dt_MPa":h,
                "signed_gaps_MPa":dict(zip(GAPS, gaps))}

    maxima = dict.fromkeys(GAPS, 0.)
    max_original = -1.
    largest_original = None
    for u in knots:
        sample = observation(u)
        gaps = sample["signed_gaps_MPa"]
        if abs(gaps["original_F8_minus_F16"]) > max_original:
            max_original = abs(gaps["original_F8_minus_F16"])
            largest_original = sample
        for key in GAPS:
            maxima[key] = max(maxima[key], abs(gaps[key]))
    return {"prior_peak_gap_u":anchor, "prior_peak_gap_MPa":abs(coarse.at(anchor)-fine.at(anchor)),
            "prior_peak_coverage":"REACHED" if anchor <= common else "NOT_REACHED",
            "at_prior_peak":observation(anchor) if anchor <= common else None,
            "common_start_u":knots[0], "common_end_u":common, "common_knots":len(knots),
            "at_largest_original_gap_on_common_support":largest_original,
            "common_max_abs_gap_MPa":maxima}


def read_command(prior, arm, out):
    result = {"status":"INCOMPLETE", "protocol":CONTROL, "label":"DEVELOPMENT_ONLY",
              "u6_qualified":False, "stage3_go":False}
    try:
        curves, refs, peak = load_prior(prior)
        native_data = (arm/"result.json").read_bytes()
        native = json.loads(native_data)
        receipt = json.loads((arm/"dt_control.json").read_bytes())
        data = (arm/"trace.csv").read_bytes()
        check_native(native, receipt, data, refs[8]["points_count"])
        require(receipt["native_result_sha256"] == sha(native_data), "CONTROL_RECEIPT_BINDING")
        half = parse_curve(data, native["steps"], refs[16]["dt"], refs[8]["width"], SPEED)
        comparison = compare(curves[8], curves[16], half)
        require(comparison["prior_peak_gap_u"] == peak["at_first_worst_total_gap"]["u"] and
                comparison["prior_peak_gap_MPa"] == peak["maximum_absolute_total_gap_MPa"], "PRIOR_PEAK_REPLAY")
        result.update(status="DEVELOPMENT_DT_SENSITIVITY", comparison=comparison, prior_sha256=PRIOR_SHA,
                      native_trace_sha256=native["trace_sha256"], native_result_sha256=sha(native_data),
                      remaining_contrast="same time step; grid, seeding and their interactions still differ")
    except (ValueError, KeyError, OSError, TypeError, ArithmeticError, csv.Error, tarfile.TarError) as exc:
        result["issue"] = str(exc) if isinstance(exc,ValueError) and str(exc).isupper() else type(exc).__name__
    write_json(out, result)
    print(result["status"])
    return 0 if "comparison" in result else 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    run = modes.add_parser("run")
    run.add_argument("--source-dir", required=True, type=Path)
    run.add_argument("--out", required=True, type=Path)
    run.add_argument("--budget", required=True, type=float)
    read = modes.add_parser("read")
    read.add_argument("--prior", required=True, type=Path)
    read.add_argument("--arm", required=True, type=Path)
    read.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "run":
        return run_command(args.source_dir, args.budget, args.out)
    return read_command(args.prior, args.arm, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
