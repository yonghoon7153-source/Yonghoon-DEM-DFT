"""Setting ②, original constant-speed dense F arm and registered target readback."""
import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys
import tarfile
import tempfile
from types import SimpleNamespace


CELLS = (8, 12, 16, 24)
BUDGET = {8: 1800, 12: 3600, 16: 5400, 24: 14400}
HISTORY = "e8e2f2535aa12b9fb089d714e1325d862cb1161b"
HISTORY_MANIFEST = "65b61a27d274b8fa0ea4a9892820d450faf972b94b382ff5f3de8dd9f2d57f0f"
FINE_PATH = "docs/reviews/suyoung_floor_fine_20261123/fine_floor.py"
REGISTERED_READER = "docs/reviews/suyoung_u6_repeat_20261120/repeat_readback.py"
PROTOCOL = "U6a-setting2-gap-only-original-bottom-loading"
LOCKS = dict(u6_qualified=False, stage3_go=False, three_dimensional_go=False)


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("bound_" + path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def write_json(path, data):
    """Publish complete evidence exclusively, also when the process is interrupted."""
    raw = (json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("ascii")
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            stream.close()
            temporary.unlink()
            raise
    try:
        if os.name == "nt":
            # Windows rename already refuses to replace an existing target.
            os.rename(temporary, path)
        else:
            os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def setup(root, full_tar, fine_tar):
    base = root / "history"
    require((base/"RELEASE").read_text().strip() == HISTORY and
            sha((base/"SOURCE_SHA256SUMS").read_bytes()) == HISTORY_MANIFEST, "fixed source history")
    here = Path(__file__).resolve().parent
    manifest = (root/"SOURCE_SHA256SUMS").read_bytes()
    refs = {}
    for line in manifest.decode("ascii").splitlines():
        digest, name = line.split("  ")
        path = (root/name).resolve()
        require(path.is_relative_to(root.resolve()) and path not in refs and
                sha(path.read_bytes()) == digest, "source manifest or member")
        refs[path] = digest
    paths = [here/"setting2_run.py", here/"gap_kernel.py", here/"read_gate.py", root/REGISTERED_READER,
             base/FINE_PATH, base/"SOURCE_SHA256SUMS", root/"RELEASE"]
    require(all(path.resolve() in refs for path in paths), "unbound entry source")
    fine = load(base/FINE_PATH)
    ctx = fine.context(base)
    readback = load(here/"read_gate.py")
    first = readback.evaluate(full_tar, fine_tar, root/REGISTERED_READER)
    require(first["status"] == "FAIL" and first["physics_pin"] == ctx.identity["base_physics_pin"]
            and first["floor_sha256"] == ctx.identity["floor_sha256"], "setting 1 eligibility")
    rule = readback.registered_reader(root/REGISTERED_READER)
    release = (root/"RELEASE").read_text().strip()
    require(re.fullmatch("[0-9a-f]{40}", release), "release identity")
    identity = dict(release=release, source_manifest_sha256=sha(manifest), previous_fine_release=HISTORY,
                    prior_full_tar_sha256=first["full_return_sha256"], prior_fine_tar_sha256=first["fine_return_sha256"],
                    base_physics_pin=first["physics_pin"], floor_sha256=first["floor_sha256"],
                    registered_reader_sha256=readback.RULE, gap_sha256=refs[(here/"gap_kernel.py").resolve()],
                    setting=2, label="DEVELOPMENT_ONLY", gap_correction=True, distance_filter=False, **LOCKS)
    return SimpleNamespace(fine=fine, ctx=ctx, rule=rule, gap=load(here/"gap_kernel.py"), identity=identity)


def seed_and_clock(e, cells):
    ctx = e.ctx
    if cells in e.fine.POINTS:
        arrays = e.fine.initial(ctx,cells)
        dt = e.fine.DT[cells]
        hashes = e.fine.SEEDS[cells]
    else:
        operator, matched = ctx.previous[:2]
        arrays = matched.seed_arrays(ctx.solver,cells)
        dt = operator.dt_for(matched,cells)
        hashes = matched.GEOMETRY[cells]
    require(ctx.driver.field_ids("F",arrays[1]) is arrays[1] and ctx.driver.step_size(ctx.solver,cells) == dt,
            "original field identity or native time step")
    return arrays, dt, list(hashes)


@contextmanager
def mark_native_result(driver):
    """Use the unchanged native loop; attach the actual setting before it writes its one result."""
    old = driver.write_json
    def write(path, result):
        require(path.name == "result.json" and result["setting"] == 1 and result["protocol"] == driver.PROTOCOL,
                "unexpected native result")
        result.update(setting=2, protocol=PROTOCOL)
        write_json(path,result)
    driver.write_json = write
    try:
        yield
    finally:
        driver.write_json = old


def target_receipt(e,cells,arm_dir,observation,dt,seed_hash,points):
    raw = (arm_dir/"trace.csv").read_bytes()
    result_raw = (arm_dir/"result.json").read_bytes()
    result = json.loads(result_raw)
    expected = dict(arm="F", cells=cells, setting=2, protocol=PROTOCOL, label="DEVELOPMENT_ONLY", origin="new",
                    budget_s=BUDGET[cells], source_sha256=e.ctx.driver.SOURCE, points_count=points,
                    status="TARGET_BRACKETED", trace_sha256=sha(raw))
    require(all(result.get(k) == v for k,v in expected.items()) and
            math.isfinite(result["elapsed_s"]) and 0 <= result["elapsed_s"] <= BUDGET[cells]+30,
            "target or native result identity")
    require(observation["identity"] == e.identity and observation["cells"] == cells and
            observation["geometry_sha256"] == seed_hash and observation["steps"] == result["steps"] and
            observation["interbody_calls"] == result["steps"], "source or contact count")
    gap_info = dict(setting=2, cell_size_gap_correction=True, distance_based_contact_detection=False,
                    gap_law="positive_projected_support_gap_over_dt", boundary_vertices_per_body=e.gap.VERTICES,
                    normal="pinned_field_mass_gradient_b_minus_a_with_center_fallback",
                    base_kernel_sha256=e.gap.BASE_KERNEL, pair_material_sha256=e.gap.PAIR_MATERIAL,
                    calls=result["steps"])
    require(observation["gap"] == gap_info, "per-step setting 2 contact identity")
    floor = observation["floor"]
    _, pressures = e.ctx.compare.read_native(raw, e.ctx.solver.WIDTH, e.ctx.solver.WALL_SPEED, dt, result["status"])
    require(len(pressures) == result["steps"]+1 and floor["steps"] == result["steps"]
            and floor["floor_passes"] == 2*result["steps"] and floor["disk_boundary_vertices"] == 256,
            "native target clock or floor calls")
    require(0. <= floor["max_penetration"] <= 2e-12 and math.isclose(floor["accumulated_impulse"],
            math.fsum(pressures)*dt*e.ctx.solver.WIDTH/10., rel_tol=1e-10, abs_tol=1e-13), "floor impulse or geometry")
    phi = e.rule.bracket_value(raw, e.ctx.solver.TARGET, result["steps"])
    return dict(**e.identity, cells=cells, status="TARGET_BRACKETED", phi_m=phi,
                bracket_steps=[result["steps"]-1,result["steps"]], bracket_pressure_MPa=pressures[-2:],
                elapsed_seconds=result["elapsed_s"], budget_seconds=BUDGET[cells], points=points, dt=dt,
                wall_speed=e.ctx.solver.WALL_SPEED, geometry_sha256=seed_hash, trace_sha256=sha(raw),
                result_sha256=sha(result_raw), observation_sha256=sha((arm_dir/"observation.json").read_bytes()))


def run_arm(e, cells, dest):
    require(not dest.exists() and not dest.is_symlink(), "existing arm directory")
    ctx = e.ctx
    arrays, dt, hashes = seed_and_clock(e,cells)
    floor = ctx.floor.make_advance(ctx.solver,cells)
    gap = e.gap.GapProjector(ctx.kernel)
    seeds = contacts = steps = 0
    def seed(n):
        nonlocal seeds
        require(n == cells and not seeds, "unexpected seed request")
        seeds += 1
        return arrays
    def project(*args):
        nonlocal contacts
        require(contacts == steps and floor.boundary is not None and args[-1] == 0.5, "interbody call order")
        value = gap.project(floor.boundary,dt,*args)
        contacts += 1
        return value
    def advance(*args):
        nonlocal steps
        height = ctx.solver.WIDTH - dt*(steps+1)*ctx.solver.WALL_SPEED
        require(args[-3:] == (10*cells,dt,ctx.solver.LO+height) and args[4] is arrays[1] and args[5] is arrays[2],
                "original forcing, field IDs or clock changed")
        value = floor(*args)
        steps += 1
        require(contacts == steps, "contact omitted")
        return value
    try:
        with e.fine.bind_driver(ctx,seed,project), mark_native_result(ctx.driver):
            result = ctx.driver.run_arm("F",cells,BUDGET[cells],dest,advance=advance)
        require(seeds == 1 and contacts == steps == result["steps"], "arm execution counts")
        require(result["status"] == "TARGET_BRACKETED", result["status"])
        observation = dict(identity=e.identity, cells=cells, geometry_sha256=hashes, steps=steps,
                           interbody_calls=contacts, gap=gap.metadata(), floor=floor.audit)
        write_json(dest/"observation.json",observation)
        receipt = target_receipt(e,cells,dest,observation,dt,hashes,len(arrays[1]))
        write_json(dest/"target_receipt.json",receipt)
    except (ArithmeticError, KeyError, IndexError, RuntimeError, TypeError, ValueError, OSError) as exc:
        if dest.is_dir() and not (dest/"incomplete.json").exists():
            write_json(dest/"incomplete.json",dict(**e.identity,cells=cells,status="INCOMPLETE",steps=steps,
                       interbody_calls=contacts,reason=str(exc)))
        raise


def decision(rule,phi):
    require(set(phi) == set(CELLS) and all(math.isfinite(v) and v>0 for v in phi.values()),
            "four complete registered endpoints required")
    d = abs(phi[12]-phi[16])
    return d, "PASS" if rule.grid_status(d) == "WITHIN_DEVELOPMENT_BAND" else "FAIL"


def summarize(e,run):
    arms = {}
    for cells in CELLS:
        dest = run/f"F{cells}"
        require(not (dest/"incomplete.json").exists(), "incomplete arm")
        observation = json.loads((dest/"observation.json").read_bytes())
        arrays,dt,hashes = seed_and_clock(e,cells)
        receipt = target_receipt(e,cells,dest,observation,dt,hashes,len(arrays[1]))
        require(receipt == json.loads((dest/"target_receipt.json").read_bytes()), "arm receipt drift")
        arms[cells] = receipt
    delta, status = decision(e.rule, {n:a["phi_m"] for n,a in arms.items()})
    return dict(**e.identity, gate="U6(a)", assessment=status, threshold=e.rule.BAND, absolute_delta=delta,
                selected_setting=2 if status=="PASS" else None,
                next_gate="SETTING2_U6B" if status=="PASS" else "SETTING3_U6A",
                timeouts_this_return=0, arms=arms)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("check","arm","summary"))
    for name in ("root","full","fine"):
        p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--run",type=Path)
    p.add_argument("--cells",type=int,choices=CELLS)
    args = p.parse_args()
    e = setup(args.root,args.full,args.fine)
    if args.mode == "check":
        for cells in CELLS:
            seed_and_clock(e,cells)
        e.gap.GapProjector(e.ctx.kernel)
        print("SETTING2_GATE_SOURCES_AND_SETTING1_RETURN_OK")
        return
    require(args.run and args.run.is_dir() and all((args.run/k).read_bytes()==(args.root/k).read_bytes()
            for k in ("RELEASE","SOURCE_SHA256SUMS")), "run source manifest")
    if args.mode == "arm":
        require(args.cells in CELLS,"one grid required")
        run_arm(e,args.cells,args.run/f"F{args.cells}")
    else:
        write_json(args.run/"summary.json",summarize(e,args.run))
        print("SETTING2_U6A_READBACK_COMPLETE")


if __name__ == "__main__":
    try:
        main()
    except (ArithmeticError,KeyError,IndexError,RuntimeError,TypeError,ValueError,OSError,tarfile.TarError) as error:
        print("INCOMPLETE", type(error).__name__, str(error), file=sys.stderr)
        raise SystemExit(4)
