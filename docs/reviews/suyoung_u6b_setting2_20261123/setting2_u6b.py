"""Read the selected F curves and run only the matched single-field U6(b) controls."""
import argparse
import csv
from contextlib import contextmanager
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import sys
import tarfile
from types import SimpleNamespace

import numpy as np


A_DIR = "docs/reviews/suyoung_u6a_gates_20261123"
B_DIR = "docs/reviews/suyoung_u6b_setting2_20261123"
A_PIN = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"
A_PACK = "7d698c085e250be40fd7d2bfdad7ae84233ddaa847bed4939d69d0ac343834b3"
A_TAR = "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af"
A_SCREEN = "711488b61bf077172335d60de019ca06f7004de4a118f8c15d70268c84b6758c"
CELLS = (8, 12, 16, 24)
PROTOCOL = "U6b-setting2-matched-single-field-native-loading"
LOCKS = dict(u6_qualified=False, stage3_go=False, three_dimensional_go=False)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("u6b_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verify_manifest(root):
    names = set()
    content = (root / "SOURCE_SHA256SUMS").read_bytes()
    for line in content.decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        path = (root / name).resolve()
        require(path.is_relative_to(root.resolve()) and name not in names and sha(path.read_bytes()) == value,
                "source manifest, duplicate or member hash")
        names.add(name)
    return names, sha(content)


def context(root):
    root = root.resolve()
    names, manifest = verify_manifest(root)
    runtime = root / "history"
    nested, nested_manifest = verify_manifest(runtime)
    require(nested_manifest == A_PACK and (runtime/"RELEASE").read_text().strip() == A_PIN, "setting 2 source lineage")
    require("RELEASE" in names and B_DIR+"/setting2_u6b.py" in names and
            "history/SOURCE_SHA256SUMS" in names and all("history/"+n in names for n in nested) and
            (root/B_DIR/"setting2_u6b.py") == Path(__file__).resolve(), "executed release binding")
    gate = load(runtime/A_DIR/"setting2_run.py")
    fine = load(runtime/"history"/gate.FINE_PATH)
    ctx = fine.context(runtime/"history")
    rule_module = load(runtime/A_DIR/"read_gate.py")
    rule = rule_module.registered_reader(runtime/gate.REGISTERED_READER)
    pin = (root/"RELEASE").read_text().strip()
    require(re.fullmatch("[a-f0-9]{40}", pin), "release")
    identity = dict(release=pin, source_manifest_sha256=manifest, gate_return_sha256=A_TAR, gate_pin=A_PIN,
                    base_physics_pin=ctx.identity["base_physics_pin"], floor_sha256=ctx.identity["floor_sha256"],
                    parser_sha256=sha(Path(ctx.driver.__file__).read_bytes()), setting=2, gate="U6(b)",
                    label="DEVELOPMENT_ONLY", **LOCKS)
    return SimpleNamespace(ctx=ctx, gate=gate, fine=fine, rule=rule, identity=identity)


def confirm_selection(summary, phi):
    delta = abs(phi[12] - phi[16])
    require(summary.get("gate") == "U6(a)" and summary.get("setting") == summary.get("selected_setting") == 2
            and summary.get("assessment") == "PASS" and summary.get("gap_correction") is True and
            summary.get("distance_filter") is False and summary.get("threshold") == .005 and
            delta == summary.get("absolute_delta") and delta <= .005, "setting 2 selection")


def read_f(e, path):
    raw = path.read_bytes()
    require(sha(raw) == A_TAR, "wrong selected F archive")
    screen = (path.parent/"screen.txt").read_bytes()
    require(sha(screen) == A_SCREEN, "original F screen")
    sums = (path.parent/"SHA256SUMS").read_text("ascii").splitlines()
    require(len(sums) == 2 and set(sums) == {f"{A_TAR}  {path.name}", f"{A_SCREEN}  screen.txt"}, "external F manifest")
    records, phi = {}, {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as arc:
        def read(name):
            item = arc.getmember("run/"+name)
            require(item.isfile(), "F return member")
            return arc.extractfile(item).read()
        require(read("screen.txt") == screen and screen.splitlines()[-1] == b"COMMAND_RC=0" and
                read("RELEASE").decode().strip() == A_PIN and sha(read("SOURCE_SHA256SUMS")) == A_PACK, "F return provenance")
        summary = json.loads(read("summary.json"))
        for n in CELLS:
            pre = f"F{n}/"
            trace, result_raw, obs = (read(pre+k) for k in ("trace.csv","result.json","observation.json"))
            result, rec = json.loads(result_raw), json.loads(read(pre+"target_receipt.json"))
            require(rec == summary["arms"][str(n)] and rec["release"] == A_PIN and rec["source_manifest_sha256"] == A_PACK
                    and result["arm"] == "F" and result["cells"] == rec["cells"] == n and result["setting"] == 2
                    and rec["trace_sha256"] == result["trace_sha256"] == sha(trace)
                    and rec["result_sha256"] == sha(result_raw) and rec["observation_sha256"] == sha(obs)
                    and result["status"] == rec["status"] == "TARGET_BRACKETED"
                    and rec["floor_sha256"] == e.identity["floor_sha256"], "bound F trace, observation, or receipt")
            _, dt, geometry = e.gate.seed_and_clock(e, n)
            require(geometry == rec["geometry_sha256"] and dt == rec["dt"], "matched F clock and geometry")
            phi[n] = e.rule.bracket_value(trace, e.ctx.solver.TARGET, result["steps"])
            require(phi[n] == rec["phi_m"], "F endpoint recalculation")
            records[n] = curve_record(e, trace, result, dt, origin="setting2-U6a-return")
    confirm_selection(summary, phi)
    return records


def merge_surface_fields(boundary, physical_ids):
    require(np.array_equal(boundary.groups, physical_ids[boundary.owners]), "physical surface owner IDs")
    # The seed attachment remains per disk. The floor constraints sharing grid velocities
    # must be solved together, including vertices originally owned by different disks.
    boundary.groups = np.zeros_like(boundary.groups)


def single_field_contact(ids, nodes, mass, gradient, velocity, centers, friction):
    require(np.all(ids == 0) and len(centers) == 1 and friction == .5 and
            np.all(nodes[1:] > nodes[:-1]), "single field must have one velocity for each occupied grid node")
    # There is no second field at any occupied S node.


def verify_coupled_floor(floor):
    """Two synthetic surfaces on one node must stop one mass exactly once."""
    ids = np.arange(2)
    boundary = floor.MaterialBoundary(ids, np.array([[0., 0.], [1., 0.]]), ids)
    merge_surface_fields(boundary, ids)
    step = floor.SurfaceStep(boundary, np.zeros((2,1), dtype=int), np.ones((2,1)), 0., 1.)
    mass = np.array([2.])
    velocity = np.array([[.25, -1.]])
    impulse = step.project(mass, velocity)
    require(abs(impulse-2.) <= 1e-12 and np.allclose(velocity, [[.25,0.]], rtol=0, atol=1e-12),
            "coupled single-field floor reference")


def surface_and_seed(e, cells):
    arrays, dt, hashes = e.gate.seed_and_clock(e, cells)
    x, physical_ids, volume = arrays
    boundary = e.ctx.floor.disk_boundary(e.ctx.solver, x, physical_ids, cells)
    require(len(boundary.owners) == 49*256 and len(np.unique(physical_ids)) == 49, "native 49 physical disk outlines")
    merge_surface_fields(boundary, physical_ids)
    return arrays, dt, hashes, boundary


@contextmanager
def mark_result(e):
    driver = e.ctx.driver
    old = driver.write_json
    def write(path, result):
        require(path.name == "result.json" and result["arm"] == "S" and result["setting"] == 1
                and result["protocol"] == driver.PROTOCOL, "unrecognized native result")
        result.update(protocol=PROTOCOL, setting=2, field_count=1, cohort_reference="selected-F-setting-2")
        e.gate.write_json(path, result)
    driver.write_json = write
    try:
        yield
    finally:
        driver.write_json = old


def run_s(e, n, dest):
    arrays, dt, geometry, boundary = surface_and_seed(e,n)
    floor = e.ctx.floor.make_advance(e.ctx.solver, n, boundary=boundary)
    seeds = 0
    calls = 0
    def seed(cells):
        nonlocal seeds
        require(seeds == 0 and cells == n, "S arm native seed")
        seeds += 1
        return arrays
    def project(*args):
        nonlocal calls
        single_field_contact(*args)
        calls += 1
    def step(x,v,affine,elastic,ids,volume,grid,step_dt,lid):
        k = floor.audit["steps"]+1
        height = e.ctx.solver.WIDTH - dt*k*e.ctx.solver.WALL_SPEED
        require(volume is arrays[2] and np.all(ids == 0) and (grid,step_dt,lid) == (10*n,dt,e.ctx.solver.LO+height),
                "mixed S fields, geometry or schedule changed")
        return floor(x,v,affine,elastic,ids,volume,grid,step_dt,lid)
    with e.fine.bind_driver(e.ctx,seed,project), mark_result(e):
        result = e.ctx.driver.run_arm("S",n,e.gate.BUDGET[n],dest,advance=step)
    require(seeds == 1 and result["steps"] == calls == floor.audit["steps"], "S update count")
    observation = dict(identity=e.identity, cells=n, geometry_sha256=geometry, field_count=1, physical_disks=49,
                       material_vertices=49*256, interbody_impulses=0, checked_single_field_calls=calls,
                       dt=dt, floor=floor.audit)
    e.gate.write_json(dest/"observation.json", observation)
    if result["status"] not in ("TARGET_BRACKETED","GEOMETRY_LIMIT"):
        raise ValueError("S arm incomplete: " + result["status"])
    record = read_s(e,n,dest)
    e.gate.write_json(dest/"receipt.json",record)


def curve_record(e, trace, result, dt, *, origin):
    s = e.ctx.solver
    _, ps = e.ctx.compare.read_native(trace, s.WIDTH, s.WALL_SPEED, dt, result["status"])
    require(len(ps) == result["steps"]+1, "complete native curve length")
    rows = csv.DictReader(io.StringIO(trace.decode("ascii"), newline=""))
    targets = e.ctx.driver.pressures_at_targets((float(row["phi_m"]), p) for row,p in zip(rows,ps,strict=True))
    return dict(arm=result["arm"], cells=result["cells"], origin=origin, terminal=result["status"],
                trace_sha256=sha(trace), steps=result["steps"], points=targets, elapsed_seconds=result["elapsed_s"])


def read_s(e, n, dest):
    result_raw = (dest/"result.json").read_bytes()
    obs_raw = (dest/"observation.json").read_bytes()
    trace = (dest/"trace.csv").read_bytes()
    r, obs = json.loads(result_raw), json.loads(obs_raw)
    arrays, dt, geometry = e.gate.seed_and_clock(e,n)
    required = dict(arm="S",cells=n,field_count=1,setting=2,protocol=PROTOCOL,source_sha256=e.ctx.driver.SOURCE,
                    points_count=len(arrays[1]), origin="new", label="DEVELOPMENT_ONLY", budget_s=e.gate.BUDGET[n],
                    cohort_reference="selected-F-setting-2", trace_sha256=sha(trace))
    require(all(r.get(k) == v for k,v in required.items()) and math.isfinite(r["elapsed_s"]) and
            0<=r["elapsed_s"]<=e.gate.BUDGET[n]+30, "S result binding")
    nsteps = r["steps"]
    audit = obs["floor"]
    require(obs["identity"] == e.identity and obs["cells"] == n and obs["geometry_sha256"] == geometry and
            (obs["field_count"],obs["physical_disks"],obs["material_vertices"],obs["interbody_impulses"]) == (1,49,49*256,0)
            and obs["dt"] == dt and obs["checked_single_field_calls"] == audit["steps"] == nsteps and
            audit["floor_passes"] == 2*nsteps and audit["disk_boundary_vertices"] == 256 and
            0 <= audit["max_penetration"] <= 2e-12, "S floor or seed binding")
    curve = curve_record(e,trace,r,dt,origin="matched-single-field-new")
    _, ps = e.ctx.compare.read_native(trace, e.ctx.solver.WIDTH, e.ctx.solver.WALL_SPEED,dt,r["status"])
    require(math.isclose(audit["accumulated_impulse"],math.fsum(ps)*dt*e.ctx.solver.WIDTH/10.,
                         rel_tol=1e-10,abs_tol=1e-13), "S floor impulse")
    return dict(**curve,result_sha256=sha(result_raw),observation_sha256=sha(obs_raw))


def summarize(e,f_curves, run):
    records = {("F",n): obs for n,obs in f_curves.items()}
    for n in CELLS:
        folder = run/f"S{n}"
        record = read_s(e,n,folder)
        require(json.loads((folder/"receipt.json").read_bytes()) == record, "S receipt readback")
        records[("S",n)] = record
    values = {k:v["points"] for k,v in records.items()}
    report = e.ctx.driver.compare(values)
    report.update(**e.identity, protocol=PROTOCOL, original_grids=list(CELLS),
                  inputs={f"{a}{n}":v for (a,n),v in records.items()},
                  fresh_s_arms=4, reused_f_arms=4, automatic_retries=0,
                  timeouts_this_complete_return=0)
    e.gate.write_json(run/"summary.json", report)
    print("SETTING2_U6B_READBACK_COMPLETE")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("check","arm","summary"))
    for name in ("root","gate"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--run",type=Path)
    p.add_argument("--cells",type=int,choices=CELLS)
    args = p.parse_args()
    e = context(args.root)
    f_curves = read_f(e,args.gate)
    if args.mode == "check":
        verify_coupled_floor(e.ctx.floor)
        for n in CELLS:
            surface_and_seed(e,n)
        print("SETTING2_F_GATE_FOUR_CURVES_AND_MATCHED_S_SEEDS_OK")
        return
    require(args.run and args.run.is_dir() and all((args.root/k).read_bytes() == (args.run/k).read_bytes()
            for k in ("RELEASE","SOURCE_SHA256SUMS")), "run/source provenance")
    if args.mode == "summary":
        summarize(e,f_curves,args.run)
    else:
        require(args.cells in CELLS,"one S resolution")
        run_s(e,args.cells,args.run/f"S{args.cells}")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, ArithmeticError, KeyError, OSError, RuntimeError, tarfile.TarError) as error:
        print("SETTING2_U6B_INCOMPLETE",error,file=sys.stderr)
        raise SystemExit(4)
