"""Run the same material-floor candidate on the native 12/24 grids for diagnosis."""
import argparse
from collections import namedtuple
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import tarfile


PREVIOUS_PIN = "c0e077ad5961d7be8dd801ea2f527b76089b362a"
PREVIOUS_MANIFEST = "e179d76257d39c16df2c2acd786bd9bcdf6ced382dbab62467e356dc80558253"
RETURN_HASH = "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65"
NEW_PATH = "docs/reviews/suyoung_floor_fine_20261123/"
OLD_PATH = "docs/reviews/suyoung_floor_full_20261123/"
BUDGET = {12: 3600, 24: 14400}
DT = {12: 0.001497578010986372, 24: 0.000748789005493186}
POINTS = {12: 21609, 24: 87857}
# Canonical C-order little-endian arrays, taken from the fixed native initializer only.
SEEDS = {
    12: ("499e377a027ae742a609a8612d2eb324e00fcc7923ba8499aa041adbe5749b72",
         "d2a45cd7a3dfd8bdce398c2f2675dfa8c66ca16f278cab46f8dc16a1c01e3f5a",
         "1a9e9a6bfc902a4a0e6552ac9c83974b7715eabca9588111f8372c783457869d"),
    24: ("09b0d2c662fa9efac2c59329c007c5c548fff49a8e0cf18712cca5c1daad20c1",
         "b1123a2bae8daf7e7bd45e7042443e86d3eefc21f7f2b605c248e88b8eaef2bc",
         "85b4c8db8d8daf34ea4f8f91f49f5d7edcbf1457bcbc9c08ea00872b9e15b242"),
}
Context = namedtuple("Context", "identity full previous compare driver solver kernel floor")


def require(condition, what):
    if not condition:
        raise ValueError(what)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("bound_" + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def context(root):
    # Authenticate the old execution manifest before loading any of its modules.
    old_root = root / "old_full"
    manifest = (old_root / "SOURCE_SHA256SUMS").read_bytes()
    require(sha(manifest) == PREVIOUS_MANIFEST, "previous package identity")
    old_names = set()
    for row in manifest.decode("ascii").splitlines():
        checksum, name = row.split("  ")
        require(sha((old_root / name).read_bytes()) == checksum, "previous package file " + name)
        old_names.add("old_full/" + name)
    allowed = old_names | {"old_full/SOURCE_SHA256SUMS", "RELEASE", NEW_PATH + "fine_floor.py", NEW_PATH + "run_fine.sh"}
    pack = (root / "SOURCE_SHA256SUMS").read_bytes()
    found = set()
    for row in pack.decode("ascii").splitlines():
        checksum, name = row.split("  ")
        require(name in allowed and name not in found and sha((root / name).read_bytes()) == checksum,
                "new package file or checksum " + name)
        found.add(name)
    release = (root / "RELEASE").read_text("ascii").strip()
    require(found == allowed and re.fullmatch("[0-9a-f]{40}", release)
            and (root / NEW_PATH / "fine_floor.py").resolve() == Path(__file__).resolve(), "new release")
    full = load(old_root / OLD_PATH / "full_floor.py")
    previous = full.sources(old_root)
    _, _, old_identity, driver, solver, kernel, floor, _ = previous
    require(old_identity["release"] == PREVIOUS_PIN, "prior release pin")
    compare = load(old_root / OLD_PATH / "full_compare.py")
    identity = dict(release=release, package_manifest_sha256=sha(pack), previous_pin=PREVIOUS_PIN,
                    base_physics_pin=old_identity["physics_pin"], floor_sha256=old_identity["floor_sha256"],
                    previous_return_sha256=RETURN_HASH)
    return Context(identity, full, previous, compare, driver, solver, kernel, floor)


def previous_pair(ctx, path):
    """Reconstruct both coarse receipts and their common-support comparison from the fixed archive."""
    full, previous = ctx.full, ctx.previous
    previous_operator, matched = previous[:2]
    traces, receipts = {}, {}
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == RETURN_HASH, "wrong previous return")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            def read(name):
                member = tar.getmember("run/" + name)
                require(member.isfile(), name)
                return tar.extractfile(member).read()
            summary = json.loads(read("summary.json"))
            require(read("RELEASE").decode("ascii").strip() == PREVIOUS_PIN
                    and sha(read("SOURCE_SHA256SUMS")) == PREVIOUS_MANIFEST
                    and read("screen.txt").splitlines()[-1] == b"COMMAND_RC=0"
                    and summary["release"] == PREVIOUS_PIN and summary["both_native_terminated"] is True,
                    "missing completed previous pair")
            for cells in (8, 16):
                name = f"F{cells}/"
                trace = read(name + "trace.csv")
                prefix = b"".join(trace.splitlines(keepends=True)[:previous_operator.END[cells] + 2])
                require(sha(prefix) == full.PREFIX_TRACE[cells], "previous short trace")
                result = read(name + "result.json")
                rec = json.loads(read(name + "full_receipt.json"))
                expected = full.receipt(previous, {cells: prefix}, cells, trace, json.loads(result), rec["floor_audit"])
                require(rec == dict(expected, result_sha256=sha(result)) == summary["arms"][f"F{cells}"],
                        "previous full receipt")
                traces[cells], receipts[cells] = trace, rec
    stats = ctx.compare.compare_pair(traces[8], traces[16], width=matched.WIDTH, speed=matched.SPEED,
                                     dt8=2 * matched.DT, dt16=matched.DT,
                                     terminal8=receipts[8]["terminal_reason"], terminal16=receipts[16]["terminal_reason"])
    require(stats == summary["comparison"], "previous common-support readback")
    return dict(fixed_reference_ratio=stats["common"]["fixed_reference_ratio"],
                fixed_reference_comparison=stats["common"]["fixed_reference_comparison"],
                comparison_samples=stats["common"]["samples"])


def initial(ctx, cells):
    arrays = ctx.solver.seed(cells)
    count = POINTS[cells]
    for arr, shape, dtype, expected in zip(arrays, ((count, 2), (count,), (count,)),
                                            ("<f8", "<i8", "<f8"), SEEDS[cells], strict=True):
        require(arr.shape == shape and arr.dtype.kind == dtype[1] and arr.dtype.itemsize == 8
                and sha(arr.astype(dtype, copy=False).tobytes(order="C")) == expected,
                f"native F{cells} seed array")
    require(ctx.driver.step_size(ctx.solver, cells) == DT[cells] and
            ctx.driver.field_ids("F", arrays[1]) is arrays[1], "native F field clock or IDs")
    return arrays


def receipt(ctx, cells, trace, result_raw, audit):
    result = json.loads(result_raw)
    required = dict(arm="F", cells=cells, setting=1, label="DEVELOPMENT_ONLY", origin="new",
                    protocol=ctx.driver.PROTOCOL, points_count=POINTS[cells], budget_s=BUDGET[cells],
                    trace_sha256=sha(trace), source_sha256=ctx.driver.SOURCE)
    require(all(result.get(k) == v for k, v in required.items()) and
            math.isfinite(result["elapsed_s"]) and 0 <= result["elapsed_s"] <= BUDGET[cells] + 30, "native receipt")
    # The historical parser enforces the original schedule including the first target crossing
    # or, for geometry termination, the final permitted step with no earlier pressure crossing.
    _, pressure = ctx.compare.read_native(trace, ctx.solver.WIDTH, ctx.solver.WALL_SPEED, DT[cells], result["status"])
    steps = len(pressure) - 1
    require(result["steps"] == steps == audit["steps"] and audit["floor_passes"] == 2 * steps
            and audit["disk_boundary_vertices"] == 256, "floor schedule")
    positives = sum(p > 0. for p in pressure)
    require(type(audit["positive_passes"]) is int and positives <= audit["positive_passes"] <= 2 * positives,
            "positive contact count")
    for field in ("accumulated_impulse", "max_grid_impulse_error", "max_g2p_momentum_error", "max_penetration"):
        require(math.isfinite(audit[field]) and audit[field] >= 0, field)
    require(audit["max_penetration"] <= 2e-12 and math.isclose(audit["accumulated_impulse"],
            math.fsum(pressure) * DT[cells] * ctx.solver.WIDTH / 10., rel_tol=1e-10, abs_tol=1e-13),
            "floor impulse and penetration")
    return dict(**ctx.identity, cells=cells, label="DEVELOPMENT_ONLY", native_terminal=result["status"],
                reached_target=result["status"] == "TARGET_BRACKETED", native_steps=steps,
                grid=10*cells, points=POINTS[cells], dt=DT[cells], geometry_sha256=list(SEEDS[cells]),
                first_positive_step=next((i for i, p in enumerate(pressure) if p > 0.), None),
                positive_native_samples=positives, result_sha256=sha(result_raw), trace_sha256=sha(trace),
                floor_audit=audit, u6_qualified=False, stage3_go=False)


@contextmanager
def bind_driver(ctx, seed, project):
    solver, driver = ctx.solver, ctx.driver
    saved = solver.seed, solver.project_contacts, driver.fixed_solver
    solver.seed, solver.project_contacts, driver.fixed_solver = seed, project, lambda: solver
    try:
        yield
    finally:
        solver.seed, solver.project_contacts, driver.fixed_solver = saved


def write_json(path, value):
    with path.open("x", encoding="ascii", newline="\n") as out:
        json.dump(value, out, sort_keys=True, indent=2, allow_nan=False)
        out.write("\n")


def run_arm(ctx, cells, dest):
    require(not dest.exists() and not dest.is_symlink(), "existing arm directory")
    arrays = initial(ctx, cells)
    solver = ctx.solver
    advance_floor = ctx.floor.make_advance(solver, cells)
    steps = projections = seeds = 0
    def seed(n):
        nonlocal seeds
        require(n == cells and seeds == 0, "arm seed")
        seeds += 1
        return arrays
    def project(*args):
        nonlocal projections
        require(steps == projections and args[-1] == .5, "friction schedule")
        result = ctx.kernel.project_contacts(*args)
        projections += 1
        return result
    def advance(*args):
        nonlocal steps
        height = solver.WIDTH - DT[cells]*(steps+1)*solver.WALL_SPEED
        require(args[-3:] == (10*cells, DT[cells], solver.LO + height)
                and args[4] is arrays[1] and args[5] is arrays[2], "schedule or field changed")
        result = advance_floor(*args)
        steps += 1
        require(steps == projections, "interbody call count")
        return result
    try:
        with bind_driver(ctx, seed, project):
            native = ctx.driver.run_arm("F", cells, BUDGET[cells], dest, advance=advance)
        require(seeds == 1 and steps == projections == native["steps"], "native call count")
        result_bytes = (dest / "result.json").read_bytes()
        require(json.loads(result_bytes) == native, "native result changed")
        data = receipt(ctx, cells, (dest / "trace.csv").read_bytes(), result_bytes, advance_floor.audit)
        write_json(dest / "fine_receipt.json", data)
    except (ArithmeticError, KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
        if dest.is_dir():
            write_json(dest / "incomplete.json", dict(**ctx.identity, status="INCOMPLETE", cells=cells,
                       steps=steps, completed_projections=projections, reason=f"{type(exc).__name__}: {exc}",
                       u6_qualified=False, stage3_go=False))
        raise


def compare_fine(compare, traces, receipts, width, speed):
    # The numerical F8/F16 reader takes arbitrary native traces at an exact 2:1 clock ratio.
    # Only its two arm names are replaced; all comparison arithmetic is reused unchanged.
    data = compare.compare_pair(traces[12], traces[24], width=width, speed=speed, dt8=DT[12], dt16=DT[24],
                                terminal8=receipts[12]["native_terminal"], terminal16=receipts[24]["native_terminal"])
    labels = {"F8": "F12", "F16": "F24", "F8_MPa": "F12_MPa", "F16_MPa": "F24_MPa",
              "F8_minus_F16_MPa": "F12_minus_F24_MPa", "F8_native": "F12_native", "F16_native": "F24_native"}
    def relabel(item):
        if isinstance(item, dict):
            return {labels.get(k, k): relabel(v) for k, v in item.items()}
        return item
    result = relabel(data)
    result["pair"] = "F12_F24"
    return result


def summarize(ctx, prior, run):
    traces, receipts = {}, {}
    for cells in POINTS:
        dest = run / f"F{cells}"
        require(not (dest / "incomplete.json").exists(), "incomplete arm")
        trace = (dest / "trace.csv").read_bytes()
        rec = json.loads((dest / "fine_receipt.json").read_bytes())
        require(rec == receipt(ctx, cells, trace, (dest / "result.json").read_bytes(), rec["floor_audit"]),
                "fine receipt changed")
        traces[cells], receipts[cells] = trace, rec
    result = compare_fine(ctx.compare, traces, receipts, ctx.solver.WIDTH, ctx.solver.WALL_SPEED)
    return dict(**ctx.identity, status="FINE_DEVELOPMENT_PAIR_READBACK", label="DEVELOPMENT_ONLY",
                arms={f"F{n}": value for n, value in receipts.items()}, previous_F8_F16=prior, comparison=result,
                both_reached_target=all(r["reached_target"] for r in receipts.values()),
                u6_qualified=False, stage3_go=False, three_dimensional_go=False)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("check", "arm", "summary"))
    p.add_argument("--root", required=True, type=Path)
    p.add_argument("--prior", required=True, type=Path)
    p.add_argument("--run", type=Path)
    p.add_argument("--cells", type=int, choices=(12, 24))
    a = p.parse_args()
    ctx = context(a.root)
    prior = previous_pair(ctx, a.prior)
    if a.mode == "check":
        for cells in POINTS:
            initial(ctx, cells)
        print("FINE_NATIVE_SEEDS_AND_PREVIOUS_FULL_RETURN_OK")
    else:
        require(a.run is not None and a.run.is_dir(), "missing run directory")
        for name in ("RELEASE", "SOURCE_SHA256SUMS"):
            require((a.run / name).read_bytes() == (a.root / name).read_bytes(), name)
        if a.mode == "arm":
            require(a.cells in POINTS, "arm resolution")
            run_arm(ctx, a.cells, a.run / f"F{a.cells}")
        else:
            write_json(a.run / "summary.json", summarize(ctx, prior, a.run))
            print("FINE_PAIR_READBACK_OK")


if __name__ == "__main__":
    try:
        main()
    except (ArithmeticError, KeyError, OSError, RuntimeError, TypeError, ValueError, tarfile.TarError) as exc:
        print("INCOMPLETE", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(4)
