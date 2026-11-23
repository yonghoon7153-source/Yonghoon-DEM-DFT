"""Run and read a single half-speed counterfactual on the frozen 2D material-plate model."""
import argparse
from contextlib import contextmanager
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import tarfile
import time
from types import SimpleNamespace


PREVIOUS_RELEASE = "35099db02148c1a5dc2581f880e0adbf28c0368d"
PREVIOUS_RETURN = "cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e"
PREVIOUS_MANIFEST = "29723077bab89d14d024f95e13986b4791eefc95c3ae31496107270b8f8f6727"
PREVIOUS_READER = "docs/reviews/suyoung_wall_balance_return_20261123/lid_prefix.py"
STEPS = {12: 1138, 24: 2276}
MARKS = {12: (930, 1138), 24: (1860, 2276)}
BUDGET = {12: 900, 24: 1800}
MOMENTUM = ("step", "particle_Py_before", "particle_Py_after", "particle_delta_Py", "wall_signed_J", "residual_J")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)


@contextmanager
def override(obj, **values):
    saved = {name: getattr(obj, name) for name in values}
    try:
        for name, value in values.items():
            setattr(obj, name, value)
        yield
    finally:
        for name, value in saved.items():
            setattr(obj, name, value)


def setup(root, prior, baseline):
    history = root / "history"
    manifest = (history/"SOURCE_SHA256SUMS").read_bytes()
    require(sha(manifest) == PREVIOUS_MANIFEST, "frozen material-lid source manifest")
    for line in manifest.decode("ascii").splitlines():
        digest, name = line.split("  ")
        require(sha((history/name).read_bytes()) == digest, "previous source " + name)
    require((history/"RELEASE").read_text("ascii").strip() == PREVIOUS_RELEASE, "previous release")
    spec = importlib.util.spec_from_file_location("frozen_lid_prefix", history/PREVIOUS_READER)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    fine, ctx, model, grid_traces, identity = native.setup(history, baseline)
    with prior.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == PREVIOUS_RETURN, "previous material-lid return SHA-256")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            def read(name):
                entry = archive.getmember("run/"+name)
                require(entry.isfile(), name)
                return archive.extractfile(entry).read()
            require(read("RELEASE") == (PREVIOUS_RELEASE+"\n").encode() and read("SOURCE_SHA256SUMS") == manifest
                    and read("screen.txt").splitlines()[-1] == b"COMMAND_RC=0", "previous completion")
            traces, walls, arms = {}, {}, {}
            for n in STEPS:
                key = f"F{n}/"
                raw, wall = read(key+"trace.csv"), read(key+"wall_steps.csv")
                rec = json.loads(read(key+"candidate_receipt.json"))
                expected = native.receipt(fine, ctx, identity, n, raw, wall, rec["floor"], rec["lid"])
                require(same(rec, expected), "previous arm receipt")
                native.paired_trace(grid_traces[n], raw, n)
                traces[n], walls[n], arms[str(n)] = raw, native.rows(wall), rec
            old = native.compare({n: native.rows(b) for n, b in grid_traces.items()}, ctx.solver.WIDTH)
            material = native.compare({n: native.rows(b) for n, b in traces.items()}, ctx.solver.WIDTH)
            expected = dict(**identity, label="DEVELOPMENT_ONLY", arms=arms, status="MATCHED_PREFIX_COMPLETE",
                            old_grid_lid=old, new_material_lid=material, reference_MPa=native.REF_MPA,
                            u6_qualified=False, stage3_go=False, three_dimensional_go=False)
            require(same(json.loads(read("summary.json")), expected), "previous material-lid summary")
    release = (root/"RELEASE").read_text("ascii").strip()
    require(re.fullmatch("[0-9a-f]{40}", release), "current release")
    identity = dict(release=release, source_sha256=sha((root/"SOURCE_SHA256SUMS").read_bytes()),
                    original_speed_material_lid_sha256=PREVIOUS_RETURN, baseline_sha256=native.PRIOR_RESULT,
                    lid_sha256=identity["lid_sha256"], half_speed_driver_sha256=sha(Path(__file__).read_bytes()),
                    original_wall_speed=ctx.solver.WALL_SPEED, half_wall_speed=.5*ctx.solver.WALL_SPEED)
    return native, fine, ctx, model, traces, walls, identity


def validate_trace(native, prior_bytes, half_bytes, cells, width, speed, dt):
    old, rows = native.rows(prior_bytes), native.rows(half_bytes)
    require(len(rows) == STEPS[cells]+1 == 2*len(old)-1 and rows[0] == old[0], "incomplete or changed seed trace")
    phi0 = float(old[0]["phi_m"])
    columns = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
    for i, row in enumerate(rows):
        t, h, p, phi = (float(row[k]) for k in columns[1:])
        require(tuple(row) == columns and row["step"] == str(i) and t == i*dt and h == width - i*dt*speed
                and math.isfinite(p) and p >= 0 and math.isclose(phi, phi0*width/h, rel_tol=2e-14),
                "half-speed native trace clock, geometry or pressure")
        if i % 2 == 0:
            ref = old[i//2]
            require(row["height"] == ref["height"] and row["phi_m"] == ref["phi_m"]
                    and t == 2*float(ref["time_code"]), "same-displacement pair")
    return rows


def momentum_row(step, before_py, after_py, wall):
    floor, lid = float(wall["floor_impulse"]), float(wall["lid_signed_impulse"])
    delta = after_py - before_py
    net = math.fsum((floor, lid))
    residual = delta - net
    require(wall["step"] == step and all(map(math.isfinite, (before_py, after_py, floor, lid, residual)))
            and floor >= 0 and lid <= 0, "invalid whole-system momentum observation")
    require(abs(residual) <= 2e-12*max(1., abs(before_py), abs(after_py), floor, -lid),
            f"particle / wall momentum residual at step {step}: before={before_py}, after={after_py}, "
            f"floor={floor}, lid={lid}, residual={residual}")
    return dict(step=step, particle_Py_before=before_py, particle_Py_after=after_py,
                particle_delta_Py=delta, wall_signed_J=net, residual_J=residual)


class ObservedAdvance:
    def __init__(self, base, write):
        self.base, self.write = base, write

    def __getattr__(self, name):
        return getattr(self.base, name)

    def __call__(self, x, v, affine, elastic, ids, mass, grid, dt, lid):
        before = float(mass @ v[:, 1])
        result = self.base(x, v, affine, elastic, ids, mass, grid, dt, lid)
        after = float(mass @ result[1][:, 1])
        self.write(momentum_row(self.base.last_step["step"], before, after, self.base.last_step))
        return result


def compare_speeds(native, original, half, width):
    old_union = native.compare(original, width)
    with override(native, SAMPLE_STEPS=MARKS):
        half_union = native.compare(half, width)
    # Every original F24 location is native on *both* half-speed grids.
    # Keeping the odd original F24 knots also keeps the intervening half-speed F12 values.
    common, changes = [], []
    for i, row in enumerate(original[24]):
        a, b = half[12][i], half[24][2*i]
        require(row["height"] == a["height"] == b["height"], "common displacement knot")
        p12, p24 = 10*float(a["bottom_pressure_E"]), 10*float(b["bottom_pressure_E"])
        record = dict(step_F24_original=i, step_F12_half=i, step_F24_half=2*i,
                      displacement_diameters=(width-float(row["height"]))/.1,
                      F12_MPa=p12, F24_MPa=p24, signed_gap_MPa=p12-p24)
        common.append(record)
        l = original[12][i//2]
        p = float(l["bottom_pressure_E"])
        if i % 2:
            r = original[12][i//2+1]
            w = (float(l["height"])-float(row["height"]))/(float(l["height"])-float(r["height"]))
            p += w*(float(r["bottom_pressure_E"])-p)
        old_gap = 10*p - 10*float(row["bottom_pressure_E"])
        changes.append(dict(**record, original_signed_gap_MPa=old_gap, half_minus_original_gap_MPa=record["signed_gap_MPa"]-old_gap))
    peak = max(common, key=lambda r:abs(r["signed_gap_MPa"]))
    change = max(changes, key=lambda r:abs(r["half_minus_original_gap_MPa"]))
    shared = dict(samples=len(common), peak=peak, fixed_reference_percent=100*abs(peak["signed_gap_MPa"])/native.REF_MPA,
                  first_above=next((r for r in common if abs(r["signed_gap_MPa"]) > .05*native.REF_MPA), None),
                  anchors=[common[i] for i in native.SAMPLE_STEPS[24]])
    return dict(original_native_1139=old_union, half_native_2277=half_union, half_on_original_1139=shared,
                same_displacement_gap_change=dict(max_pointwise_absolute_change=change,
                    half_minus_original_peak_amplitude_MPa=abs(peak["signed_gap_MPa"])-abs(old_union["peak"]["signed_gap_MPa"])))


def wall_window(walls, motion, start, end, dt, width):
    selected = walls[start-1:end]
    floor = math.fsum(float(r["floor_impulse"]) for r in selected)
    lid = math.fsum(float(r["lid_signed_impulse"]) for r in selected)
    factor = 10/((end-start+1)*dt*width)
    net = math.fsum((floor, lid))
    direct = None if motion is None else motion[end-1]["particle_Py_after"] - motion[start-1]["particle_Py_before"]
    return dict(steps=[start,end], floor_J=floor, lid_signed_J=lid, floor_over_abs_lid=floor/abs(lid) if lid else None,
                inferred_delta_Py_J=net, direct_delta_Py_J=direct, floor_equivalent_MPa=floor*factor,
                inferred_delta_Py_equivalent_MPa=net*factor,
                direct_delta_Py_equivalent_MPa=None if direct is None else direct*factor)


def read_half_arm(native, fine, ctx, identity, cells, dest, previous):
    trace = (dest/"trace.csv").read_bytes()
    raw_wall = (dest/"wall_steps.csv").read_bytes()
    raw_motion = (dest/"particle_momentum.csv").read_bytes()
    rows = validate_trace(native, previous, trace, cells, ctx.solver.WIDTH, identity["half_wall_speed"], fine.DT[cells])
    arm = json.loads((dest/"candidate_receipt.json").read_bytes())
    with override(native, STEPS=STEPS):
        expected = native.receipt(fine, ctx, identity, cells, trace, raw_wall, arm["floor"], arm["lid"])
    require(same(arm, expected), "half-speed candidate receipt")
    walls, observed = native.rows(raw_wall), native.rows(raw_motion)
    require(len(observed) == len(walls), "whole-system momentum row count")
    before = 0.
    motion = []
    for step, (w, m) in enumerate(zip(walls, observed, strict=True), 1):
        require(tuple(m) == MOMENTUM and m["step"] == str(step) and float(m["particle_Py_before"]) == before,
                "whole-system momentum continuity")
        after = float(m["particle_Py_after"])
        want = momentum_row(step, before, after, dict(w, step=int(w["step"])))
        require(all(float(m[k]) == want[k] for k in MOMENTUM[1:]), "whole-system momentum table mismatch")
        motion.append(want)
        before = after
    rec = dict(**arm, particle_momentum_sha256=sha(raw_motion), particle_momentum_rows=len(motion),
               max_absolute_particle_wall_residual_J=max(abs(m["residual_J"]) for m in motion),
               direct_delta_Py_since_initial_J=motion[-1]["particle_Py_after"], native_dt=fine.DT[cells],
               budget_seconds=BUDGET[cells], status="HALF_SPEED_PREFIX_COMPLETE", three_dimensional_go=False)
    return rows, walls, motion, rec


def run_arm(native, fine, ctx, model, previous, identity, cells, dest):
    file = writer = None
    def write(record):
        nonlocal file, writer
        if writer is None:
            file = (dest/"particle_momentum.csv").open("x", encoding="ascii", newline="", buffering=1)
            writer = csv.DictWriter(file, MOMENTUM, lineterminator="\n")
            writer.writeheader()
        writer.writerow(record)

    def observe(*args, **kwargs):
        return ObservedAdvance(model.make_advance(*args, **kwargs), write)

    def paired(prior, trace, n):
        return validate_trace(native, prior, trace, n, ctx.solver.WIDTH, identity["half_wall_speed"], fine.DT[n])

    start = time.monotonic()
    try:
        try:
            with override(ctx.solver, WALL_SPEED=identity["half_wall_speed"]), \
                 override(native, STEPS=STEPS, BUDGET=BUDGET, SAMPLE_STEPS=MARKS, paired_trace=paired):
                native.run_arm(fine, ctx, SimpleNamespace(make_advance=observe), previous, identity, cells, dest)
        finally:
            if file is not None:
                file.close()
        rec = read_half_arm(native, fine, ctx, identity, cells, dest, previous[cells])[-1]
        fine.write_json(dest/"half_speed_receipt.json", rec)
    except Exception as exc:
        if dest.is_dir():
            trace_file = dest/"trace.csv"
            count = max(0, len(trace_file.read_bytes().splitlines())-2) if trace_file.is_file() else 0
            fine.write_json(dest/"incomplete.json", dict(**identity, cells=cells, completed_trace_steps=count,
                            elapsed_seconds=time.monotonic()-start, reason=f"{type(exc).__name__}: {exc}",
                            status="INCOMPLETE", u6_qualified=False, stage3_go=False, three_dimensional_go=False))
        raise


def fixed_windows(all_walls, all_motion, marks, width, dt):
    results = []
    for a, b in zip(marks[12], marks[24], strict=True):
        def window(n, start, end):
            return wall_window(all_walls[n], all_motion.get(n), start, end, dt[n], width)
        coarse, fine, fine_two = window(12, a, a), window(24, b, b), window(24, b-1, b)
        def delta(x, y):
            keys = ("floor_equivalent_MPa","inferred_delta_Py_equivalent_MPa","direct_delta_Py_equivalent_MPa")
            return {k: None if x[k] is None else x[k]-y[k] for k in keys}
        results.append(dict(F12_native=coarse, F24_native=fine, F12_minus_F24_native=delta(coarse, fine),
                            F24_same_duration_two_steps=fine_two, F12_minus_F24_same_duration=delta(coarse, fine_two)))
    return results


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("check","arm","summary"))
    for name in ("root", "prior", "baseline"):
        cli.add_argument("--"+name, type=Path, required=True)
    cli.add_argument("--run", type=Path)
    cli.add_argument("--cells", type=int, choices=tuple(STEPS))
    args = cli.parse_args()
    native, fine, ctx, model, previous, previous_walls, identity = setup(args.root, args.prior, args.baseline)
    if args.mode == "check":
        with override(ctx.solver, WALL_SPEED=identity["half_wall_speed"]):
            for n in STEPS:
                fine.initial(ctx, n)
                require(STEPS[n] == 2*native.STEPS[n] and ctx.driver.step_size(ctx.solver,n) == fine.DT[n]
                        and MARKS[n] == tuple(2*s for s in native.SAMPLE_STEPS[n]), "half-speed native schedule")
        print("HALF_SPEED_REFERENCE_AND_SEEDS_OK")
        return
    require(args.run is not None and args.run.is_dir(), "missing run")
    require(all((args.root/k).read_bytes() == (args.run/k).read_bytes() for k in ("RELEASE", "SOURCE_SHA256SUMS")),
            "run release or manifest")
    if args.mode == "arm":
        require(args.cells in STEPS, "arm resolution")
        dest = args.run/f"F{args.cells}"
        require(not dest.exists(), "existing arm")
        run_arm(native, fine, ctx, model, previous, identity, args.cells, dest)
        return
    original = {n: native.rows(data) for n,data in previous.items()}
    half, walls, motion, arms = {}, {}, {}, {}
    for n in STEPS:
        dest = args.run/f"F{n}"
        half[n], walls[n], motion[n], arms[n] = read_half_arm(native, fine, ctx, identity, n, dest, previous[n])
        require(same(arms[n], json.loads((dest/"half_speed_receipt.json").read_bytes())), "half-speed receipt mismatch")
    width = ctx.solver.WIDTH
    result = dict(**identity, label="DEVELOPMENT_ONLY", status="HALF_SPEED_PREFIX_COMPLETE", arms=arms,
                  reference_MPa=native.REF_MPA, speed_fraction=.5, pressure_union=compare_speeds(native, original, half, width),
                  original_fixed_windows=fixed_windows(previous_walls, {}, native.SAMPLE_STEPS, width, fine.DT),
                  half_fixed_windows=fixed_windows(walls, motion, MARKS, width, fine.DT),
                  u6_qualified=False, stage3_go=False, three_dimensional_go=False)
    fine.write_json(args.run/"summary.json", result)
    print("HALF_SPEED_NATIVE_PREFIX_READBACK_OK")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, IndexError, RuntimeError, ArithmeticError, tarfile.TarError) as exc:
        print("INCOMPLETE", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(4)
