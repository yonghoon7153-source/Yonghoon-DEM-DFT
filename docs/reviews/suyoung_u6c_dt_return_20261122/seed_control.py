"""F8 grid with F16 material-point sampling at the previously verified F16 step size."""
import argparse
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tarfile
from hashlib import sha256


PREVIOUS_TOOL = Path(__file__).resolve().parent.parent / "suyoung_u6c_wall_return_20261122" / "dt_control.py"
if sha256(PREVIOUS_TOOL.read_bytes()).hexdigest() != "1811424d5e02767f70f210cfe292c9a4d49091ecf63c5ced7bcb6229095a3e17":
    raise ValueError("PREVIOUS_TOOL_IDENTITY")
_spec = importlib.util.spec_from_file_location("private_seed_dt_reference", PREVIOUS_TOOL)
dt = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = dt
_spec.loader.exec_module(dt)

HALF_SHA = "e574396d010514b3cd77f57d2e06d0c25227c88a7b6e985577f2981aa8c154e4"
PROTOCOL = "U6c-F8-grid-F16-seed-and-dt-v1"
NPOINTS = 39053
# Scalar reconstruction of the fixed F16 seed, row-major, little-endian 64-bit.
SEED = {
    "positions": "ce12e262721141b2c4fc36cc72733686055a9e22ce62a8cc733a1e2ad591858a",
    "ids": "da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
    "volume": "06f4c3ce49ffece1d401bdcae453605728c4ba0e7731b4c2c6027e337cdc88b4",
}
GAPS = ("F8_half_minus_F16", "F8_half_minus_F8_dense", "F8_dense_minus_F16")


def verify_seed(arrays):
    dn = {}
    for name, arr, shape, dtype in zip(SEED, arrays, ((NPOINTS, 2), (NPOINTS,), (NPOINTS,)), ("<f8","<i8","<f8"), strict=True):
        dt.require(arr.shape == shape, "SEED_SHAPE")
        dt.require(arr.dtype.kind == dtype[1] and arr.dtype.itemsize == 8, "SEED_TYPE")
        dn[name] = dt.sha(arr.astype(dtype, copy=False).tobytes(order="C"))
    dt.require(dn == SEED, "SEED_HASH")
    return dn


def integrate(driver, budget, out):
    # run_arm fetches its solver through this factory. Its own cells=8 computes
    # grid=80 and advances the usual field IDs; only the seed source is changed.
    factory = driver.fixed_solver
    solver = factory()
    original_seed = solver.seed
    checked = []

    def seed(cells):
        dt.require(cells == 8 and not checked, "UNEXPECTED_SEED_CALL")
        arrays = original_seed(16)
        checked.append(verify_seed(arrays))
        return arrays

    solver.seed = seed
    driver.fixed_solver = lambda: solver
    try:
        native = dt.integrate(driver, budget, out)
        dt.require(len(checked) == 1, "MISSING_SEED_CALL")
        return native, checked[0]
    finally:
        driver.fixed_solver = factory
        solver.seed = original_seed


def run_command(directory, budget, out):
    for name, digest in dt.SOURCE.items():
        dt.require(dt.sha((directory/name).read_bytes()) == digest, "SOURCE_IDENTITY")
    spec = importlib.util.spec_from_file_location("seed_control_driver", directory/"suyoung_u6b_dev.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    native, seed_hashes = integrate(driver, budget, out)
    trace_sha = dt.sha((out/"trace.csv").read_bytes())
    dt.require(native["trace_sha256"] == trace_sha and native["points_count"] == NPOINTS, "NATIVE_IDENTITY")
    dt.write_json(out/"seed_control.json", {
        "protocol":PROTOCOL, "label":"DEVELOPMENT_ONLY", "u6_qualified":False,
        "native_result_sha256":dt.sha((out/"result.json").read_bytes()), "trace_sha256":trace_sha,
        "reader_sha256":dt.sha(Path(__file__).read_bytes()), "source_sha256":dt.SOURCE,
        "grid_cells_per_diameter":8, "seed_cells_per_diameter":16, "dt_cells_per_diameter":16,
        "arm":"F", "status":native["status"], "initial_seed_sha256":seed_hashes,
    })
    print(native["status"])
    return 0 if native["status"] == "TARGET_BRACKETED" else 4


def references(wall_path, half_path):
    native_curves, refs, peak = dt.load_prior(wall_path)
    raw = half_path.read_bytes()
    dt.require(dt.sha(raw) == HALF_SHA, "HALF_ARCHIVE_IDENTITY")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        def read(name):
            item = archive.getmember("run/" + name)
            dt.require(item.isfile(), "HALF_MEMBER_TYPE")
            return archive.extractfile(item).read()

        native_bytes = read("F8_HALF/result.json")
        native = json.loads(native_bytes)
        receipt = json.loads(read("F8_HALF/dt_control.json"))
        trace = read("F8_HALF/trace.csv")
        summary = json.loads(read("dt_summary.json"))
    dt.check_native(native, receipt, trace, refs[8]["points_count"])
    dt.require(receipt["native_result_sha256"] == dt.sha(native_bytes), "HALF_RECEIPT_BINDING")
    half = dt.parse_curve(trace, native["steps"], refs[16]["dt"], refs[8]["width"], dt.SPEED)
    anchor = peak["at_first_worst_total_gap"]["u"]
    dt.require(summary["prior_sha256"] == dt.PRIOR_SHA and summary["status"] == "DEVELOPMENT_DT_SENSITIVITY"
               and summary["native_trace_sha256"] == dt.sha(trace)
               and summary["comparison"]["prior_peak_gap_u"] == anchor, "ANCHOR_BINDING")
    return half, native_curves[16], refs[16], anchor


def dense_curve(folder, ref):
    native_bytes = (folder/"result.json").read_bytes()
    native = json.loads(native_bytes)
    dt.require(native["status"] == "TARGET_BRACKETED", "INCOMPLETE_ARM")
    dt.require((native["arm"],native["cells"],native["origin"],native["points_count"],native["setting"],
                native["protocol"],native["label"]) == ("F",8,"new",NPOINTS,1,dt.NATIVE,"DEVELOPMENT_ONLY")
               and ref["points_count"] == NPOINTS, "NATIVE_CONFIGURATION")
    dt.require(native["source_sha256"] == {k:v for k,v in dt.SOURCE.items() if k != "suyoung_u6b_dev.py"}, "NATIVE_SOURCE")
    receipt = json.loads((folder/"seed_control.json").read_bytes())
    trace = (folder/"trace.csv").read_bytes()
    expected = {"protocol":PROTOCOL, "label":"DEVELOPMENT_ONLY", "arm":"F", "status":"TARGET_BRACKETED",
                "grid_cells_per_diameter":8,"seed_cells_per_diameter":16,"dt_cells_per_diameter":16,
                "source_sha256":dt.SOURCE, "initial_seed_sha256":SEED, "reader_sha256":dt.sha(Path(__file__).read_bytes()),
                "trace_sha256":dt.sha(trace), "native_result_sha256":dt.sha(native_bytes)}
    dt.require(receipt["u6_qualified"] is False and all(receipt[k] == v for k,v in expected.items()), "CONTROL_BINDING")
    dt.require(native["trace_sha256"] == expected["trace_sha256"], "NATIVE_TRACE")
    return dt.parse_curve(trace, native["steps"], ref["dt"], ref["width"], dt.SPEED), receipt["trace_sha256"]


def compare(half, fine, dense, anchor):
    common = min(curve.u[-1] for curve in (half, fine, dense))
    knots = sorted({u for curve in (half, fine, dense) for u in curve.u if u <= common})

    def observation(u):
        h, f, d = (curve.at(u) for curve in (half, fine, dense))
        gaps = (h-f, h-d, d-f)
        dt.require(abs(gaps[0]-gaps[1]-gaps[2]) <= 8*math.ulp(max(abs(h), abs(f), abs(d))), "GAP_CLOSURE")
        return {"u":u, "F8_half_MPa":h, "F16_MPa":f, "F8_dense_MPa":d, "gaps_MPa":dict(zip(GAPS,gaps))}

    worst = max(knots, key=lambda u:abs(half.at(u)-fine.at(u)))
    reached = knots[0] <= anchor <= common
    return {"fixed_u":anchor, "anchor_status":"REACHED" if reached else "NOT_REACHED",
            "at_original_anchor":observation(anchor) if reached else None,
            "largest_residual_on_common_support":observation(worst), "common_knots":len(knots),
            "common_start_u":knots[0], "common_end_u":common}


def read_command(wall, half_file, folder, out):
    result = {"status":"INCOMPLETE", "protocol":PROTOCOL, "label":"DEVELOPMENT_ONLY",
              "u6_qualified":False, "stage3_go":False}
    try:
        half, fine, ref, anchor = references(wall, half_file)
        dense, trace_sha = dense_curve(folder, ref)
        result.update(status="DEVELOPMENT_SEED_GRID_CONTRAST", comparison=compare(half, fine, dense, anchor),
                      seed_trace_sha256=trace_sha, prior_wall_sha256=dt.PRIOR_SHA, prior_half_sha256=HALF_SHA)
    except (ValueError, KeyError, OSError, TypeError, ArithmeticError, tarfile.TarError, dt.csv.Error) as exc:
        result["issue"] = str(exc) if isinstance(exc, ValueError) and str(exc).isupper() else type(exc).__name__
    dt.write_json(out, result)
    print(result["status"])
    return 0 if "comparison" in result else 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    run = modes.add_parser("run")
    run.add_argument("--source-dir", type=Path, required=True)
    run.add_argument("--budget", type=float, required=True)
    run.add_argument("--out", type=Path, required=True)
    read = modes.add_parser("read")
    for arg in ("wall", "half", "arm", "out"):
        read.add_argument("--" + arg, required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "run":
        return run_command(args.source_dir, args.budget, args.out)
    return read_command(args.wall, args.half, args.arm, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
