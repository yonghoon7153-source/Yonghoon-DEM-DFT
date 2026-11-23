"""Short native F contact comparison with authenticated original traces."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import sys
import tarfile
import zlib


CASE = "docs/reviews/suyoung_floor_contact_20261123/"
MATCHED = "docs/reviews/suyoung_wall_layers_20261123/matched_controls.py"
MATCHED_PIN = "ebba5037e29de3ca760de7fe3d1a85d43ff3f1e6"
MATCHED_HASH = "dab772e3409e555e5097743f7958869e6db4384e8336e200627abe42a4edcf37"
OLD_MANIFEST = "484ef4815e0c83085fc40ad3c10b42b91c01d4a29e635d8249ab10a0ee302539"
CROSS_RECEIPT = {
    8: "d0d7f3c615fa89d2cd111598ea2f3a605841c2f3eab5e082cf02e2bfef381499",
    16: "3ee58cbd7a6a9f447184f449a042eacd6f2d19ce15f5ddca772b02136f2612ee",
}
END = {8: 270, 16: 540}
MODELS = ("original", "candidate")
TABLE = ("wall_model", "cells", "step", "time_code", "height", "displacement_code", "pressure_MPa")
PROGRAMS = ("material_floor.py", "floor_operator.py", "run_floor.sh", "render_weekly.py", "weekly_type.npz")


def require(test, msg):
    if not test:
        raise ValueError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def write_json(path, obj):
    write(path, (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("ascii"))


def module(path):
    spec = importlib.util.spec_from_file_location("floor_protocol_" + path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = obj
    spec.loader.exec_module(obj)
    return obj


def sources(root):
    matched_file = root / MATCHED
    require(sha(matched_file.read_bytes()) == MATCHED_HASH, "MATCHED_SOURCE")
    matched = module(matched_file)
    names = {"RELEASE", MATCHED, *("scripts/" + name for name in matched.SOURCES),
             *(CASE + name for name in PROGRAMS)}
    manifest = (root / "SOURCE_SHA256SUMS").read_bytes()
    hashes = {}
    for row in manifest.decode("ascii").splitlines():
        digest, name = row.split("  ")
        require(name in names and name not in hashes and re.fullmatch("[0-9a-f]{64}", digest),
                "PACKAGE_MANIFEST_ENTRY")
        require(sha((root / name).read_bytes()) == digest, "PACKAGE_SOURCE_BYTES " + name)
        hashes[name] = digest
    require(set(hashes) == names, "PACKAGE_SOURCE_SET")
    pin = (root / "RELEASE").read_text("ascii").strip()
    require(bool(re.fullmatch("[0-9a-f]{40}", pin)), "PACKAGE_RELEASE")
    driver, solver, kernel = matched.engine(root)
    source = dict(release=pin, release_manifest_sha256=sha(manifest), physics_pin=matched.PHY,
                  native_protocol_pin=MATCHED_PIN, physics_sha256=matched.SOURCES,
                  candidate_sha256=hashes[CASE + "material_floor.py"],
                  operator_sha256=hashes[CASE + "floor_operator.py"], archive_sha256=matched.PRIOR)
    return matched, source, driver, solver, kernel, module(root / CASE / "material_floor.py")


def dt_for(matched, cells):
    return matched.DT * (2 if cells == 8 else 1)


def original(matched, path):
    """Reauthenticate the prior archive and the completed native cross/prefix receipts."""
    entries = {}
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == matched.PRIOR, "CROSS_ARCHIVE_HASH")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            def get(name):
                info = tar.getmember("run/" + name)
                require(info.isfile(), "CROSS_MEMBER")
                return tar.extractfile(info).read()

            require(sha(get("SOURCE_SHA256SUMS")) == OLD_MANIFEST, "CROSS_SOURCE")
            require(get("screen.txt").splitlines()[-1] == b"COMMAND_RC=0", "CROSS_NOT_FINISHED")
            for cells in END:
                data = {name: get(f"F{cells}/" + name) for name in
                        ("trace.csv", "prefix_receipt.json", "cross_receipt.json")}
                raw = data["trace.csv"]
                cross = json.loads(data["cross_receipt.json"])
                prefix = json.loads(data["prefix_receipt.json"])
                dt, steps = dt_for(matched, cells), END[cells]
                x, ids, vol = matched.GEOMETRY[cells]
                require(sha(data["cross_receipt.json"]) == CROSS_RECEIPT[cells]
                        and cross["status"] == "DEVELOPMENT_FROZEN_CROSS_OBSERVED"
                        and cross["cells"] == cells and cross["steps"][-1] == steps
                        and sha(raw) == cross["files"]["trace.csv"] == matched.NATIVE_TRACE[cells]
                        and sha(data["prefix_receipt.json"]) == cross["files"]["prefix_receipt.json"],
                        "ORIGINAL_CROSS_RECEIPT")
                require(prefix["cells"] == cells and prefix["dt"] == dt and prefix["steps"] == steps
                        and prefix["mapping"] == "ORIGINAL" and prefix["previous_pin"] == matched.PHY
                        and prefix["kernel_sha256"] == matched.SOURCES["suyoung_multicontact_dev.py"]
                        and prefix["geometry"] == dict(positions=x, physical_ids=ids, field_ids=ids, volume=vol)
                        and prefix["raw_prefix_sha256"] == sha(raw)
                        and prefix["status"] == "DEVELOPMENT_PREFIX_OBSERVED", "ORIGINAL_PREFIX_RECEIPT")
                matched.parse_trace(raw, dt, steps)
                entries[cells] = data
    return entries


class EndPrefix(Exception):
    """Stop before entering the first advance past the requested native step."""


def validate_audit(audit, raw, matched, cells):
    steps, dt = END[cells], dt_for(matched, cells)
    pressures = matched.parse_trace(raw, dt, steps)
    require(audit["steps"] == steps and audit["floor_passes"] == 2 * steps
            and type(audit["positive_passes"]) is int and 0 <= audit["positive_passes"] <= 2 * steps
            and audit["disk_boundary_vertices"] == 256, "FLOOR_PASS_COUNTS")
    for key in ("accumulated_impulse", "max_grid_impulse_error", "max_g2p_momentum_error", "max_penetration"):
        require(math.isfinite(audit[key]) and audit[key] >= 0, "FLOOR_AUDIT " + key)
    require(audit["max_penetration"] <= 2e-12, "FLOOR_PENETRATION_LIMIT")
    nonzero_steps = sum(p > 0 for p in pressures)
    require(nonzero_steps <= audit["positive_passes"] <= 2*nonzero_steps, "POSITIVE_IMPULSE_SCHEDULE")
    integral = math.fsum(pressures) * dt * matched.WIDTH / 10.
    require(math.isclose(audit["accumulated_impulse"], integral, rel_tol=1e-10, abs_tol=1e-13),
            "TRACE_IMPULSE_MISMATCH")


def candidate_receipt(matched, src, cells, raw, contacts, audit):
    validate_audit(audit, raw, matched, cells)
    require(contacts == END[cells], "INTERBODY_CALLS")
    return dict(**src, status="SHORT_PREFIX_COMPLETE", label="DEVELOPMENT_ONLY", wall_model="candidate",
                cells=cells, grid=10*cells, seed_hashes=list(matched.GEOMETRY[cells]), mapping="ORIGINAL",
                dt=dt_for(matched, cells), width=matched.WIDTH, lid_speed=matched.SPEED,
                steps=END[cells], seconds_limit=matched.BUDGET, friction=.5, interbody_calls=contacts,
                floor_audit=audit, trace_sha256=sha(raw), u6_qualified=False, stage3_go=False)


def arm(parts, cells, folder):
    matched, src, driver, solver, kernel, candidate = parts
    initial = matched.seed_arrays(solver, cells)
    require(driver.field_ids("F", initial[1]) is initial[1], "F_FIELD_IDENTITY")
    dt, steps, contacts, seeds = dt_for(matched, cells), 0, 0, 0
    saved_seed, saved_contact, saved_factory = solver.seed, solver.project_contacts, driver.fixed_solver

    def seed(n):
        nonlocal seeds
        require(n == cells and seeds == 0, "ARM_SEED_REQUEST")
        seeds += 1
        return initial

    def contact(*args):
        nonlocal contacts
        require(contacts == steps and args[-1] == .5, "INTERBODY_SCHEDULE")
        value = kernel.project_contacts(*args)
        contacts += 1
        return value

    def advance(*args):
        nonlocal steps
        if steps == END[cells]:
            raise EndPrefix()
        require(args[-3:] == (10*cells, dt, solver.LO + (matched.WIDTH - dt*(steps+1)*matched.SPEED))
                and args[4] is initial[1] and args[5] is initial[2], "ARM_NATIVE_SCHEDULE")
        value = corrected(*args)
        steps += 1
        require(contacts == steps, "INTERBODY_CALL_COUNT")
        return value

    require(not folder.exists() and not folder.is_symlink(), "EXISTING_ARM")
    solver.seed, solver.project_contacts, driver.fixed_solver = seed, contact, lambda: solver
    try:
        corrected = candidate.make_advance(solver, cells)
        result = driver.run_arm("F", cells, matched.BUDGET, folder, advance=advance)
        reason = result["status"]
    except EndPrefix:
        require((steps, contacts, seeds) == (END[cells], END[cells], 1), "ARM_CALLS")
        raw = (folder / "trace.csv").read_bytes()
        write_json(folder / "receipt.json", candidate_receipt(matched, src, cells, raw, contacts, corrected.audit))
        return 0
    except (ArithmeticError, ValueError, RuntimeError) as exc:
        reason = type(exc).__name__ + ": " + str(exc)
    finally:
        solver.seed, solver.project_contacts, driver.fixed_solver = saved_seed, saved_contact, saved_factory
    if folder.is_dir():
        write_json(folder / "incomplete.json", dict(status="INCOMPLETE", reason=reason, cells=cells, steps=steps,
                                                    interbody_calls=contacts, u6_qualified=False, stage3_go=False))
    return 4


def read_four(matched, src, old, run):
    series = {}
    receipts = {}
    for cells in END:
        files = old[cells]
        opath = run / "original" / f"F{cells}"
        for name, raw in files.items():
            require((opath / name).read_bytes() == raw, "ORIGINAL_RETURN_CHANGED")
        cpath = run / "candidate" / f"F{cells}"
        require(not (cpath / "incomplete.json").exists() and not (cpath / "result.json").exists(),
                "UNFINISHED_CANDIDATE")
        raw = (cpath / "trace.csv").read_bytes()
        receipt_bytes = (cpath / "receipt.json").read_bytes()
        rec = json.loads(receipt_bytes)
        require(rec == candidate_receipt(matched, src, cells, raw, rec["interbody_calls"], rec["floor_audit"]),
                "CANDIDATE_RECEIPT")
        receipts[f"candidate/F{cells}"] = sha(receipt_bytes)
        receipts[f"original/F{cells}"] = {name: sha(content) for name, content in files.items() if name.endswith(".json")}
        for model, data in (("original", files["trace.csv"]), ("candidate", raw)):
            series[model, cells] = matched.parse_trace(data, dt_for(matched, cells), END[cells])
    return series, receipts


def long_csv(matched, series):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(TABLE)
    for model in MODELS:
        for cells in END:
            for step, value in enumerate(series[model, cells]):
                time = step * dt_for(matched, cells)
                height = matched.WIDTH - time * matched.SPEED
                writer.writerow((model, cells, step, time, height, matched.WIDTH-height, value))
    return out.getvalue().encode("ascii")


def gap_summary(matched, coarse, fine):
    """Interpolate the coarse pressure at odd fine steps for the gap diagnostic alone."""
    require((len(coarse), len(fine)) == (271, 541), "NATIVE_TRACES_REQUIRED")
    gaps = []
    def travel(step, dt):
        return matched.WIDTH - (matched.WIDTH - step * dt * matched.SPEED)
    for j, value in enumerate(fine):
        i = j // 2
        p8 = coarse[i]
        if j % 2:
            left, right = travel(i, 2*matched.DT), travel(i+1, 2*matched.DT)
            weight = (travel(j, matched.DT) - left) / (right - left)
            p8 += weight * (coarse[i+1] - coarse[i])
        delta = p8 - value
        gaps.append(dict(fine_step=j, coarse_interpolated=bool(j % 2), f8_MPa=p8, f16_MPa=value,
                         signed_gap_MPa=delta, abs_over_registered_peak=abs(delta)/matched.FINE_PEAK))
    def stats(rows):
        return dict(count=len(rows), peak=max(rows, key=lambda r:abs(r["signed_gap_MPa"])),
                    first_above_5pct=next((r for r in rows if r["abs_over_registered_peak"] > .05), None))
    return dict(native_union=stats(gaps), shared_native=stats(gaps[::2]), edge=gaps[-3:])


def summarize(parts, old, run, *, write_outputs):
    matched, src = parts[:2]
    series, receipts = read_four(matched, src, old, run)
    table = long_csv(matched, series)
    csv_path = run / "pressure_displacement.csv"
    if write_outputs:
        write(csv_path, table)
    require(csv_path.read_bytes() == table, "FOUR_CURVE_CSV")
    gaps = {model: gap_summary(matched, series[model, 8], series[model, 16]) for model in MODELS}
    paths = {f"{model}/F{cells}/trace.csv": sha((run / model / f"F{cells}" / "trace.csv").read_bytes())
             for model in MODELS for cells in END}
    both_zero = all(not any(series["candidate", cells]) for cells in END)
    return dict(**src, status="SHORT_PREFIX_COMPLETE", label="DEVELOPMENT_ONLY", u6_qualified=False,
                stage3_go=False, qualification_computed=False, finer_pair_status="UNMEASURED",
                candidate_zero_throughout=both_zero, candidate_resolution_qualification="UNDETERMINED",
                candidate_response="BOTH_ZERO_THROUGHOUT_PREFIX" if both_zero else "NONZERO_IN_PREFIX",
                shared_points=271, samples_per_model={"F8":271, "F16":541}, native_rows=1624,
                registered_fine_peak_MPa=matched.FINE_PEAK, development_display_threshold=.05,
                trace_sha256=paths, receipt_sha256=receipts, pressure_displacement_sha256=sha(table),
                gap_summary=gaps)


def png_hash(path, csv_hash):
    """Check the renderer embedded the digest of this exact four-curve dataset."""
    raw = path.read_bytes()
    require(raw.startswith(b"\x89PNG\r\n\x1a\n"), "MISSING_WEEKLY_PNG")
    offset, labels, chunks = 8, [], []
    while offset + 12 <= len(raw):
        size = int.from_bytes(raw[offset:offset+4], "big")
        data = raw[offset+4:offset+8+size]
        end = offset+12+size
        require(end <= len(raw) and zlib.crc32(data) == int.from_bytes(raw[end-4:end], "big"),
                "WEEKLY_PNG_CHUNK")
        chunks.append(data[:4])
        if data.startswith(b"tEXtCSV_SHA256\x00"):
            labels.append(data[15:])
        offset = end
    require(offset == len(raw) and chunks[:1] == [b"IHDR"] and b"IDAT" in chunks
            and chunks[-1:] == [b"IEND"] and labels == [csv_hash.encode("ascii")], "WEEKLY_PNG_CSV_BINDING")
    return sha(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "import-original", "arm", "table", "seal", "verify"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--cells", type=int, choices=(8,16))
    args = parser.parse_args()
    parts = sources(args.root)
    matched = parts[0]
    old = original(matched, args.prior)
    if args.command == "check":
        for cells in END:
            matched.seed_arrays(parts[3], cells)
        print("SOURCE_CLOCK_SEEDS_AND_BOTH_ORIGINAL_RECEIPTS_OK")
        return 0
    run = args.run
    require(run is not None and run.is_dir(), "RUN_DIRECTORY")
    for name in ("RELEASE", "SOURCE_SHA256SUMS"):
        require((run / name).read_bytes() == (args.root / name).read_bytes(), "RETURN_SOURCE " + name)
    if args.command == "import-original":
        for cells, files in old.items():
            folder = run / "original" / f"F{cells}"
            folder.mkdir(parents=True, exist_ok=False)
            for name, raw in files.items():
                write(folder / name, raw)
    elif args.command == "arm":
        require(args.cells in END, "ARM_CELLS")
        return arm(parts, args.cells, run / "candidate" / f"F{args.cells}")
    else:
        require(not (run / "incomplete.json").exists(), "INCOMPLETE_RETURN")
        summary = summarize(parts, old, run, write_outputs=args.command == "table")
        if args.command == "table":
            return 0
        summary["weekly_png_sha256"] = png_hash(run / "weekly_pressure_displacement.png",
                                               summary["pressure_displacement_sha256"])
        if args.command == "seal":
            write_json(run / "summary.json", summary)
        else:
            require(json.loads((run / "summary.json").read_bytes()) == summary, "RETURN_SUMMARY")
        print("FOUR_TRACES_AND_WEEKLY_FIGURE_VERIFIED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ArithmeticError, IndexError, KeyError, OSError, TypeError, ValueError, tarfile.TarError) as exc:
        print("INCOMPLETE", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(4)
