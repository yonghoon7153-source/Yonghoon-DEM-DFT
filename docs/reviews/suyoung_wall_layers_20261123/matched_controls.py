"""Two short, ordered 2D controls localizing grid, seed and time-step effects at the wall."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import tarfile

import numpy as np


PHY = "99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f"
PRIOR = "4bb6fe0cdff8964c6bf02cfbf3f9dd9f7bdec5199cfddce0e3d8160b0dd4f391"
SOURCES = {
    "suyoung_u6b_dev.py": "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
    "suyoung_multicontact_dev.py": "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645",
}
GEOMETRY = {
    8: ("474424dea2a36388e28e02b9a5d47f9dad183bb1672dbf4e33ea84bdf7a6efc9",
        "a91d7701d1e24908a53f6807d6bc9042402e70fba67bc82393889895a06868e4",
        "78fe7907be63b6b084b71ec3262bf2d3f936b2b4eca65c255fc99cdd666a69f0"),
    16: ("ce12e262721141b2c4fc36cc72733686055a9e22ce62a8cc733a1e2ad591858a",
         "da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
         "06f4c3ce49ffece1d401bdcae453605728c4ba0e7731b4c2c6027e337cdc88b4"),
}
NATIVE_TRACE = {8: "0e5e021706abbc88a728a305807edfce02aa877bcd92d824d5aa2988515aebce",
                16: "60b31c9055734a24cd9aaa0ed1b5809fad338fb6d5848ab0a49f4d52f9945eca"}
DT, WIDTH, SPEED = .0011231835082397789, .7024180763115129, .01996548746349992
FINE_PEAK, BUDGET, STEPS = .6636991102836952, 600, 540
COLUMNS = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
COMPONENTS = ("dt_MPa", "seed_MPa", "grid_MPa", "native_gap_MPa")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    with path.open("x", encoding="ascii", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=True, allow_nan=False, sort_keys=True, indent=2)
        handle.write("\n")


def load(path):
    spec = importlib.util.spec_from_file_location("matched_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def engine(repo):
    scripts = repo / "scripts"
    for name, expected in SOURCES.items():
        need(sha((scripts / name).read_bytes()) == expected, "SOURCE_BINDING")
    driver = load(scripts / "suyoung_u6b_dev.py")
    solver = driver.fixed_solver()
    kernel = load(scripts / "suyoung_multicontact_dev.py")
    need((solver.WIDTH, solver.WALL_SPEED, solver.DIAMETER, solver.TARGET) ==
         (WIDTH, SPEED, .1, .12), "ARM_CONSTANTS")
    need(driver.step_size(solver, 16) == DT and driver.step_size(solver, 8) == 2*DT, "ARM_CLOCK")
    return driver, solver, kernel


def seed_arrays(solver, cells):
    x, ids, volume = solver.seed(cells)
    points = {8: 9653, 16: 39053}[cells]
    for value, shape, dtype, expected in zip((x, ids, volume), ((points, 2), (points,), (points,)),
                                             ("<f8", "<i8", "<f8"), GEOMETRY[cells]):
        need(value.shape == shape and value.dtype.kind == dtype[1] and value.dtype.itemsize == 8
             and sha(value.astype(dtype, copy=False).tobytes(order="C")) == expected, "SEED_BINDING")
    return x, ids, volume


def parse_trace(raw, dt, last):
    reader = csv.DictReader(io.StringIO(raw.decode("ascii")))
    need(tuple(reader.fieldnames or ()) == COLUMNS, "TRACE_HEADER")
    result = []
    for step, row in enumerate(reader):
        need(len(row) == len(COLUMNS) and row["step"] == str(step), "TRACE_STEP")
        time, height, pressure, phi = (float(row[k]) for k in COLUMNS[1:])
        need(time == step*dt and height == WIDTH-time*SPEED and math.isfinite(phi)
             and math.isclose(phi, .78*WIDTH/height, rel_tol=1e-12), "NATIVE_SCHEDULE")
        need(0. <= pressure < .12 and (step != 0 or pressure == 0.), "PRESSURE_OR_EARLY_TARGET")
        result.append(10.*pressure)
    need(len(result) == last+1, "PARTIAL_TRACE")
    return result


def native(path):
    with path.open("rb") as stream:
        need(hashlib.file_digest(stream, "sha256").hexdigest() == PRIOR, "CROSS_RETURN")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            result = {}
            for cells, dt, last in ((8, 2*DT, 270), (16, DT, 540)):
                e = archive.getmember(f"run/F{cells}/trace.csv")
                need(e.isfile(), "NATIVE_TRACE_MEMBER")
                raw = archive.extractfile(e).read()
                need(sha(raw) == NATIVE_TRACE[cells], "NATIVE_TRACE_HASH")
                result[cells] = parse_trace(raw, dt, last)
            return result


def receipt(cells, raw):
    return dict(protocol="grid80-matched-prefix-v1", label="DEVELOPMENT_ONLY", physics_pin=PHY,
                source_sha256=SOURCES, observer_sha256=sha(Path(__file__).read_bytes()),
                archive_sha256=PRIOR, native_trace_sha256={str(k):v for k,v in NATIVE_TRACE.items()},
                cells=8, grid=80, seed_cells=cells, seed_hashes=list(GEOMETRY[cells]),
                dt=DT, mapping="ORIGINAL", friction=.5, step_count=STEPS, kernel_calls=STEPS,
                seconds_limit=BUDGET, trace_sha256=sha(raw), status="PREFIX_COMPLETE",
                u6_qualified=False, stage3_go=False)


class EndPrefix(Exception):
    """Stop on entry to step 541 before advancing the state."""


def run_arm(repo, cells, out):
    if out.exists() or out.is_symlink():
        raise FileExistsError(out)
    driver, solver, kernel = engine(repo)
    initial = seed_arrays(solver, cells)
    need(driver.field_ids("F", initial[1]) is initial[1], "FIELD_IDENTITY")
    calls, steps, seeds = 0, 0, 0
    failure = {}
    original_step = solver.advance

    def fixed_seed(grid_cells):
        nonlocal seeds
        need(grid_cells == 8 and seeds == 0, "UNEXPECTED_SEED_REQUEST")
        seeds += 1
        return initial

    def project(*args):
        nonlocal calls
        need(calls == steps and args[-1] == .5, "CONTACT_SCHEDULE")
        value = kernel.project_contacts(*args)
        calls += 1
        return value

    def advance(*args):
        nonlocal steps
        if steps == STEPS:
            raise EndPrefix()
        need(args[-3:] == (80, DT, solver.LO + (WIDTH - DT*(steps+1)*SPEED))
             and args[4] is initial[1] and args[5] is initial[2], "NATIVE_ADVANCE_CONTRACT")
        try:
            value = original_step(*args)
        except (ArithmeticError, ValueError, RuntimeError) as exc:
            # The pinned advance computes new arrays; it never mutates these incoming arrays.
            path = out / "failed_incoming.npz"
            failure.update(attempted_step=steps+1, exception=type(exc).__name__)
            try:
                names = ("x","v","affine","elastic","ids","volume","grid","dt","lid")
                with path.open("xb") as stream:
                    np.savez_compressed(stream, attempted_step=steps+1, **dict(zip(names,args)))
                failure["incoming_sha256"] = sha(path.read_bytes())
            except (ValueError, OSError) as capture_error:
                failure["capture_error"] = type(capture_error).__name__
            raise
        steps += 1
        need(calls == steps, "CONTACT_CALL_COUNT")
        return value

    original_seed, original_project = solver.seed, solver.project_contacts
    original_factory, original_dt = driver.fixed_solver, driver.step_size
    solver.seed, solver.project_contacts = fixed_seed, project
    driver.fixed_solver, driver.step_size = lambda: solver, lambda s, n: DT
    try:
        result = driver.run_arm("F", 8, BUDGET, out, advance=advance)
        reason = result["status"]
    except EndPrefix:
        need((steps, calls, seeds) == (STEPS, STEPS, 1), "PREFIX_CALL_COUNTS")
        raw = (out/"trace.csv").read_bytes()
        parse_trace(raw, DT, STEPS)
        write(out/"receipt.json", receipt(cells, raw))
        return 0
    except (ArithmeticError, ValueError, RuntimeError) as exc:
        reason = type(exc).__name__ + ": " + str(exc)
    finally:
        solver.seed, solver.project_contacts = original_seed, original_project
        driver.fixed_solver, driver.step_size = original_factory, original_dt
    if out.is_dir():
        write(out/"incomplete.json", dict(status="INCOMPLETE", reason=reason, steps=steps, seed_cells=cells,
                                          kernel_calls=calls, failed_advance=failure,
                                          stage3_go=False, u6_qualified=False))
    return 4


def control_read(folder, cells):
    need(not (folder/"incomplete.json").exists() and not (folder/"result.json").exists(), "UNFINISHED_ARM")
    raw = (folder/"trace.csv").read_bytes()
    need(json.loads((folder/"receipt.json").read_bytes()) == receipt(cells, raw), "CONTROL_RECEIPT")
    return parse_trace(raw, DT, STEPS)


def bridge(coarse, a, b, fine):
    need((len(coarse),len(a),len(b),len(fine)) == (271,541,541,541), "MISSING_SHARED_STEPS")
    samples = []
    for i, p in enumerate(coarse):
        j = 2*i
        vals = (p-a[j], a[j]-b[j], b[j]-fine[j], p-fine[j])
        need(math.isclose(math.fsum(vals[:3]), vals[3], abs_tol=1e-12, rel_tol=1e-12), "TELESCOPE")
        samples.append(dict(coarse_step=i, fine_step=j, u=WIDTH-(WIDTH-j*DT*SPEED),
                            **dict(zip(COMPONENTS, vals))))
    peaks = {}
    for k in COMPONENTS:
        row = max(samples, key=lambda r:abs(r[k]))
        peaks[k] = dict(coarse_step=row["coarse_step"], fine_step=row["fine_step"], signed_MPa=row[k],
                        abs_MPa=abs(row[k]), fraction_of_registered_peak=abs(row[k])/FINE_PEAK)
    return dict(label="DEVELOPMENT_ONLY", status="ORDERED_MATCHED_PREFIX", ordered_changes=["dt","seed","grid"],
                registered_fine_peak_MPa=FINE_PEAK, registered_limit=0.05, shared_samples=len(samples),
                qualification_computed=False, stage3_go=False, u6_qualified=False,
                native_u6c_status="F8_F16_EXCEEDS_F12_F24_UNMEASURED",
                primary=[samples[269],samples[270]], peaks=peaks, samples=samples)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for name in ("check", "arm", "read"):
        sub = commands.add_parser(name)
        sub.add_argument("--repo", required=True, type=Path)
        sub.add_argument("--prior", required=True, type=Path)
        if name == "arm":
            sub.add_argument("--seed-cells", choices=(8,16), type=int, required=True)
        if name != "check":
            sub.add_argument("--out", required=True, type=Path)
        if name == "read":
            sub.add_argument("--run", required=True, type=Path)
    args=parser.parse_args()
    try:
        prior = native(args.prior)
        if args.action == "arm":
            return run_arm(args.repo, args.seed_cells, args.out)
        _, solver, _ = engine(args.repo)
        if args.action == "check":
            for n in (8,16):
                seed_arrays(solver,n)
            print("MATCHED_CONTROLS_SOURCES_SEEDS_PRIOR_OK")
            return 0
        data = bridge(prior[8],control_read(args.run/"seed8",8),control_read(args.run/"seed16",16),prior[16])
        write(args.out,data)
        print(data["status"])
        return 0
    except (ArithmeticError, KeyError, OSError, tarfile.TarError, TypeError, ValueError) as exc:
        print("INCOMPLETE",type(exc).__name__,str(exc))
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
