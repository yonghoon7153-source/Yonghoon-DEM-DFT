"""Use exactly the returned trajectories' clocks and seeds to vary only the moving lid."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tarfile
import time

PRIOR_PIN = "0c4eb97d447f9afa984303425e1c5ab221ae9cec"
PRIOR_RESULT = "1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e"
PRIOR_MANIFEST = "65b6b8253e0098abd6a4dd232d735b53357a634bbc94a38af26105cb1b63b65b"
BEFORE = "docs/reviews/suyoung_floor_fine_return_20261123/early_wall_observer.py"
STEPS = {12: 569, 24: 1138}
BUDGET = {12: 600, 24: 1200}
REF_MPA = 0.6636991102836952
SAMPLE_STEPS = {12: (465, 569), 24: (930, 1138)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup(pkg, prior):
    previous = pkg / "history"
    require(sha((previous / "SOURCE_SHA256SUMS").read_bytes()) == PRIOR_MANIFEST, "previous manifest")
    observer = load_module("previous_observer", previous / BEFORE)
    fine, ctx, identity = observer.load(previous)
    require(identity["release"] == PRIOR_PIN, "previous release")
    with prior.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == PRIOR_RESULT, "expected balance return")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            def read(name):
                entry = archive.getmember("run/" + name)
                require(entry.isfile(), name)
                return archive.extractfile(entry).read()
            require(read("RELEASE").decode().strip() == PRIOR_PIN
                    and sha(read("SOURCE_SHA256SUMS")) == PRIOR_MANIFEST
                    and read("screen.txt").splitlines()[-1] == b"COMMAND_RC=0", "previous completion")
            summary = json.loads(read("summary.json"))
            traces = {}
            for cells, end in STEPS.items():
                key = f"F{cells}/"
                raw = read(key + "trace.csv")
                receipt = json.loads(read(key + "balance_receipt.json"))
                require(receipt == summary["arms"][str(cells)] and receipt["steps"] == end
                        and sha(raw) == receipt["trace_sha256"]
                        and sha(read(key + "wall_impulses.csv")) == receipt["observer_table_sha256"], "previous arm")
                traces[cells] = raw
    model = load_module("candidate_lid", Path(__file__).with_name("material_lid.py"))
    release = (pkg / "RELEASE").read_text("ascii").strip()
    return fine, ctx, model, traces, dict(release=release, source_sha256=sha((pkg / "SOURCE_SHA256SUMS").read_bytes()),
                                         baseline_sha256=PRIOR_RESULT, lid_sha256=sha(Path(model.__file__).read_bytes()))


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"), newline="")))


def paired_trace(before, after, cells):
    """Check every independent variable byte-for-byte, including the initial state."""
    reference, observed = rows(before), rows(after)
    require(len(observed) == len(reference) == STEPS[cells] + 1, "missing native samples")
    require(reference[0] == observed[0], "changed initial trace")
    columns = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
    for i, (a, b) in enumerate(zip(reference, observed, strict=True)):
        require(tuple(a) == tuple(b) == columns and b["step"] == str(i), "trace columns or order")
        require(all(a[k] == b[k] for k in columns if k != "bottom_pressure_E"), "changed clock, lid or fraction")
        p = float(b["bottom_pressure_E"])
        require(math.isfinite(p) and p >= 0, "invalid lower pressure")
    return observed


def compare(traces, width):
    # Take the union of native knots. Both schedules start at zero and end at the
    # same height; the F12 observations coincide with every second F24 observation.
    slow, fast = traces[12], traces[24]
    require(len(fast) == 2 * len(slow) - 1, "native 2:1 clocks")
    result = []
    for i, row in enumerate(fast):
        j = i // 2
        end = float(row["height"])
        p24 = 10 * float(row["bottom_pressure_E"])
        a = slow[j]
        if i % 2:
            b = slow[j + 1]
            ha, hb = float(a["height"]), float(b["height"])
            require(ha > end > hb, "outside interpolation bracket")
            w = (ha - end) / (ha - hb)
            pa, pb = float(a["bottom_pressure_E"]), float(b["bottom_pressure_E"])
            p12 = 10 * (pa + w * (pb - pa))
        else:
            require(a["height"] == row["height"], "unmatched native displacement")
            p12 = 10 * float(a["bottom_pressure_E"])
        result.append(dict(step_F24=i, displacement_diameters=(width - end) / .1,
                           F12_MPa=p12, F24_MPa=p24, signed_gap_MPa=p12-p24))
    peak = max(result, key=lambda item: abs(item["signed_gap_MPa"]))
    return dict(samples=len(result), peak=peak, fixed_reference_percent=100*abs(peak["signed_gap_MPa"])/REF_MPA,
                first_above=next((r for r in result if abs(r["signed_gap_MPa"]) > .05*REF_MPA), None),
                anchors=[result[i] for i in SAMPLE_STEPS[24]])


class EndPrefix(Exception):
    """Leave the native driver after it has recorded the requested last step."""


def run_arm(fine, ctx, model, prior, identity, cells, dest):
    initial = fine.initial(ctx, cells)
    advance = model.make_advance(ctx.solver, cells, floor_module=ctx.floor)
    steps = seeds = projections = 0
    wall_rows = []
    def seed(n):
        nonlocal seeds
        require(n == cells and seeds == 0, "duplicate or inconsistent seed")
        seeds += 1
        return initial

    def project(*args):
        nonlocal projections
        require(steps == projections and args[-1] == .5, "interbody contact order")
        result = ctx.kernel.project_contacts(*args)
        projections += 1
        return result

    def step(*args):
        nonlocal steps
        if steps == STEPS[cells]:
            raise EndPrefix()
        dt = fine.DT[cells]
        h = ctx.solver.WIDTH - dt*(steps + 1)*ctx.solver.WALL_SPEED
        require(args[-3:] == (10*cells, dt, ctx.solver.LO+h) and args[4] is initial[1] and args[5] is initial[2],
                "changed grid, geometry, IDs or schedule")
        result = advance(*args)
        steps += 1
        require(projections == steps, "missing interbody update")
        wall_rows.append(dict(advance.last_step))
        return result
    def save_walls(filename):
        with (dest/filename).open("x", newline="", encoding="ascii") as stream:
            table = csv.DictWriter(stream, WALL_COLUMNS, lineterminator="\n")
            table.writeheader()
            table.writerows(wall_rows)

    try:
        with fine.bind_driver(ctx, seed, project):
            result = ctx.driver.run_arm("F", cells, BUDGET[cells], dest, advance=step)
        if steps != STEPS[cells] or result["status"] != "TARGET_BRACKETED":
            raise ValueError("early native stop: " + result["status"])
    except EndPrefix:
        pass
    except Exception:
        if dest.is_dir():
            save_walls("partial_wall_steps.csv")
        raise
    require(steps == projections == STEPS[cells] and seeds == 1, "incomplete schedule")
    save_walls("wall_steps.csv")
    data = (dest/"trace.csv").read_bytes()
    paired_trace(prior[cells], data, cells)
    report = receipt(fine, ctx, identity, cells, data, (dest/"wall_steps.csv").read_bytes(), advance.audit, advance.lid_audit)
    fine.write_json(dest/"candidate_receipt.json", report)


WALL_COLUMNS = ("step", "floor_impulse", "lid_downward_impulse", "lid_signed_impulse", "top_gap_before",
                "top_gap_after", "floor_gap_after", "lid_grid_impulse_error")


def validate_lid(lid, n):
    require(all(math.isfinite(v) and v >= 0 for v in lid.values()), "invalid lid counters")
    require(all(type(lid[k]) is int for k in ("steps","lid_passes","positive_passes")) and
            lid["steps"] == n and lid["lid_passes"] == 2*n and 0 <= lid["positive_passes"] <= 2*n,
            "upper wall schedule")
    require(lid["max_penetration"] <= 2e-12 and lid["max_clock_error"] <= 2e-12, "upper wall position")


def receipt(fine, ctx, identity, cells, data, wall_data, floor, lid):
    p = [10*float(r["bottom_pressure_E"]) for r in rows(data)]
    n = STEPS[cells]
    require(all(math.isfinite(v) and v >= 0 for v in floor.values())
            and all(type(floor[k]) is int for k in ("steps","floor_passes","positive_passes"))
            and floor["steps"] == n and floor["floor_passes"] == 2*n
            and max(floor["max_penetration"], floor["max_grid_impulse_error"], floor["max_g2p_momentum_error"])<=2e-12,
            "lower wall constraints")
    require(math.isclose(floor["accumulated_impulse"], math.fsum(p)*fine.DT[cells]*ctx.solver.WIDTH/10,
                         rel_tol=1e-10, abs_tol=1e-13), "floor impulse vs native CSV")
    validate_lid(lid, n)
    measurements=rows(wall_data)
    require(len(measurements)==n and all(tuple(r)==WALL_COLUMNS for r in measurements), "incomplete wall observations")
    impulses=[]
    lower_penetration=upper_penetration=upper_error=0.
    for i,row in enumerate(measurements,1):
        values={k:float(v) for k,v in row.items()}
        require(row["step"]==str(i) and all(math.isfinite(v) for v in values.values()), "invalid wall measurement")
        down=values["lid_downward_impulse"]
        require(down>=0 and down == -values["lid_signed_impulse"] and
                min(values["top_gap_after"], values["floor_gap_after"])>=-2e-12, "wall signs or penetration")
        require(math.isclose(values["floor_impulse"]*10/(fine.DT[cells]*ctx.solver.WIDTH),p[i],
                             abs_tol=1e-13,rel_tol=1e-12), "step pressure vs lower impulse")
        require(0<=values["lid_grid_impulse_error"]<=2e-12*max(1.,down), "upper wall impulse balance")
        lower_penetration=max(lower_penetration,-values["floor_gap_after"])
        upper_penetration=max(upper_penetration,-values["top_gap_after"])
        upper_error=max(upper_error,values["lid_grid_impulse_error"])
        impulses.append(down)
    require(floor["max_penetration"]==lower_penetration and lid["max_penetration"]==upper_penetration and
            lid["max_grid_impulse_error"]==upper_error, "recorded wall maxima")
    for audit, values in ((floor,p[1:]),(lid,impulses)):
        count=sum(v>0. for v in values)
        require(count<=audit["positive_passes"]<=2*count, "positive wall pass count")
    require(math.isclose(math.fsum(impulses), lid["accumulated_downward_impulse"], abs_tol=1e-13, rel_tol=1e-10),
            "total upper impulse")
    return dict(**identity, cells=cells, label="DEVELOPMENT_ONLY", steps=n, trace_sha256=sha(data), wall_csv_sha256=sha(wall_data),
                first_lid_down_step=next((i for i,j in enumerate(impulses,1) if j>0),None),
                first_positive_step=next((i for i,v in enumerate(p) if v>0),None),
                floor=floor, lid=lid, u6_qualified=False, stage3_go=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check","arm","summary"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--cells", type=int, choices=tuple(STEPS))
    a=parser.parse_args()
    fine,ctx,model,prior,identity=setup(a.root, a.prior)
    if a.mode=="check":
        for n in STEPS:
            fine.initial(ctx,n)
        compare({n:rows(raw) for n,raw in prior.items()}, ctx.solver.WIDTH)
        print("NATIVE_SEEDS_BASELINE_RECEIPTS_AND_PREFIXES_OK")
        return
    require(a.run is not None and a.run.is_dir(), "run folder required")
    require(all((a.run/name).read_bytes()==(a.root/name).read_bytes() for name in ("SOURCE_SHA256SUMS","RELEASE")),
            "run release changed")
    if a.mode=="arm":
        require(a.cells in STEPS,"arm resolution")
        dest=a.run/f"F{a.cells}"
        require(not dest.exists(),"existing output")
        start=time.monotonic()
        try:
            run_arm(fine,ctx,model,prior,identity,a.cells,dest)
        except Exception as exc:
            if dest.is_dir():
                trace=dest/"trace.csv"
                count=max(0,len(trace.read_bytes().splitlines())-2) if trace.is_file() else 0
                fine.write_json(dest/"incomplete.json",dict(**identity,cells=a.cells,completed_trace_steps=count,
                                elapsed_seconds=time.monotonic()-start,reason=f"{type(exc).__name__}: {exc}",
                                status="INCOMPLETE",u6_qualified=False,stage3_go=False))
            raise
        return
    new, arms={}, {}
    for n in STEPS:
        dest=a.run/f"F{n}"
        trace=(dest/"trace.csv").read_bytes()
        new[n]=paired_trace(prior[n],trace,n)
        rec=json.loads((dest/"candidate_receipt.json").read_bytes())
        require(rec == receipt(fine,ctx,identity,n,trace,(dest/"wall_steps.csv").read_bytes(),rec["floor"],rec["lid"]),
                "candidate receipt mismatch")
        arms[n]=rec
    before=compare({n:rows(raw) for n,raw in prior.items()},ctx.solver.WIDTH)
    after=compare(new,ctx.solver.WIDTH)
    fine.write_json(a.run/"summary.json", dict(**identity,label="DEVELOPMENT_ONLY",arms=arms,
                    status="MATCHED_PREFIX_COMPLETE",old_grid_lid=before,new_material_lid=after,
                    reference_MPa=REF_MPA,u6_qualified=False,stage3_go=False,three_dimensional_go=False))
    print("MATERIAL_LID_NATIVE_PREFIX_READBACK_OK")


if __name__=="__main__":
    try:
        main()
    except (ArithmeticError,KeyError,OSError,RuntimeError,TypeError,ValueError,tarfile.TarError) as exc:
        print("INCOMPLETE",type(exc).__name__,str(exc),file=sys.stderr)
        raise SystemExit(4)
