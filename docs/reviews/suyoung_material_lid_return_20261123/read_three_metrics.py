"""Read a completed material-lid prefix return and its pinned baseline without running a solver."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tarfile
from types import ModuleType, SimpleNamespace


REVIEW = "docs/reviews/suyoung_wall_balance_return_20261123"
DEFAULT_NATIVE = Path(__file__).resolve().parents[3] / REVIEW / "lid_prefix.py"
DEFAULT_BASELINE = Path(os.environ.get("SUYOUNG_BALANCE_RETURN","suyoung_wall_balance_result.tar.gz"))
NATIVE_SHA = "a44904535761c79381c03a8f24fa9b27f4a80b1fd73a7f25f0dc45af2ab8fd99"
IDENTITY = {
    "release": "35099db02148c1a5dc2581f880e0adbf28c0368d",
    "source_sha256": "29723077bab89d14d024f95e13986b4791eefc95c3ae31496107270b8f8f6727",
    "baseline_sha256": "1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e",
    "lid_sha256": "34ba6abab29c1c05661002aa7d6f946f60b78770c0aacd7ad6f5d3fc652212e5",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_native(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == NATIVE_SHA, "lid_prefix.py SHA-256")
    module = ModuleType("verified_lid_prefix")
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def read_run(path, expected_sha, wall_name, receipt_name):
    require(re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha), "expected archive SHA-256")
    wanted = {"run/" + name for name in ("RELEASE", "SOURCE_SHA256SUMS", "screen.txt", "summary.json")}
    wanted.update(f"run/F{n}/{name}" for n in (12, 24) for name in ("trace.csv", wall_name, receipt_name))
    files = {}
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == expected_sha.lower(), "archive SHA-256")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            for entry in archive:
                require(not entry.name.endswith(("/incomplete.json", "/partial_wall_steps.csv")), "partial return")
                if entry.name in wanted:
                    require(entry.isfile() and entry.name not in files, "duplicate or non-file " + entry.name)
                    files[entry.name] = archive.extractfile(entry).read()
    require(files.keys() == wanted, "missing required archive member")
    screen = files["run/screen.txt"].splitlines()
    require(screen and screen[-1] == b"COMMAND_RC=0" and b"F12_RC=0" in screen and b"F24_RC=0" in screen,
            "incomplete terminal or arm status")
    return files


def same_json(a, b):
    # Canonical serialization also distinguishes a false flag from the integer zero.
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)


def interval(walls, start, end, dt, width):
    """The wall series is ordered from step one. All impulses act on the material."""
    subset = walls[start-1:end]
    floor = math.fsum(pair[0] for pair in subset)
    lid = math.fsum(pair[1] for pair in subset)
    net = math.fsum((floor, lid))
    factor = 10 / (width * dt * len(subset))
    return {
        "steps": [start, end], "duration_code": dt * len(subset),
        "floor_J": floor, "lid_signed_J": lid, "inferred_whole_delta_Py_J": net,
        "floor_over_abs_lid": floor / abs(lid) if lid else None,
        "floor_equivalent_MPa": floor * factor, "lid_signed_equivalent_MPa": lid * factor,
        "inferred_whole_delta_Py_equivalent_MPa": net * factor,
    }


def landmarks(native, traces, walls, dt, width, pairs=None):
    records = []
    if pairs is None:
        pairs=zip(native.SAMPLE_STEPS[12], native.SAMPLE_STEPS[24], strict=True)
    for coarse, fine in pairs:
        left, right = traces[12][coarse], traces[24][fine]
        require(left["time_code"] == right["time_code"] and left["height"] == right["height"]
                and traces[12][coarse-1]["time_code"] == traces[24][fine-2]["time_code"], "unaligned windows")
        snapshots = {}
        for n, end in ((12, coarse), (24, fine)):
            snap = interval(walls[n], end, end, dt[n], width)
            snap["native_bottom_pressure_MPa"] = 10 * float(traces[n][end]["bottom_pressure_E"])
            snap["since_initial_inferred_whole_delta_Py_J"] = interval(walls[n], 1, end, dt[n], width)["inferred_whole_delta_Py_J"]
            snapshots[f"F{n}"] = snap
        a, b = snapshots["F12"], snapshots["F24"]
        common = interval(walls[24], fine-1, fine, dt[24], width)
        terms = ("floor_equivalent_MPa", "lid_signed_equivalent_MPa", "inferred_whole_delta_Py_equivalent_MPa")
        records.append({
            "displacement_D": (width - float(left["height"])) / .1, "time_code": float(left["time_code"]),
            "native_steps": snapshots, "F12_minus_F24_native": {k: a[k] - b[k] for k in terms},
            "identical_window": {"F12": a, "F24": common, "F12_minus_F24": {k: a[k] - common[k] for k in terms}},
        })
    return records


def evaluate(candidate, expected_sha, baseline=DEFAULT_BASELINE, native_path=DEFAULT_NATIVE):
    native = load_native(native_path)
    previous = read_run(baseline, IDENTITY["baseline_sha256"], "wall_impulses.csv", "balance_receipt.json")
    run = read_run(candidate, expected_sha, "wall_steps.csv", "candidate_receipt.json")
    for data, pin, manifest in ((previous, native.PRIOR_PIN, native.PRIOR_MANIFEST),
                                (run, IDENTITY["release"], IDENTITY["source_sha256"])):
        require(data["run/RELEASE"] == (pin + "\n").encode() and native.sha(data["run/SOURCE_SHA256SUMS"]) == manifest,
                "run release or source manifest")
    require(b"MATERIAL_LID_PREFIX_READBACK_COMPLETE" in run["run/screen.txt"].splitlines(), "missing readback")
    before_summary = json.loads(previous["run/summary.json"])
    old, new, old_walls, new_walls, dt, receipts = {}, {}, {}, {}, {}, {}
    for n in native.STEPS:
        key = f"run/F{n}/"
        trace, wall = previous[key+"trace.csv"], previous[key+"wall_impulses.csv"]
        rec = json.loads(previous[key+"balance_receipt.json"])
        require(same_json(rec, before_summary["arms"][str(n)]) and rec["steps"] == native.STEPS[n]
                and rec["trace_sha256"] == native.sha(trace) and rec["observer_table_sha256"] == native.sha(wall),
                "baseline arm binding")
        old[n] = native.rows(trace)
        dt[n] = rec["dt"]
        old_walls[n] = [(float(r["floor_all"]), float(r["lid_all"])) for r in native.rows(wall)]
        new[n] = native.paired_trace(trace, run[key+"trace.csv"], n)
    width = float(old[12][0]["height"])
    require(dt[12] == 2 * dt[24] and width == float(old[24][0]["height"]), "baseline native constants")
    for n in native.STEPS:
        key = f"run/F{n}/"
        wall = run[key+"wall_steps.csv"]
        actual = json.loads(run[key+"candidate_receipt.json"])
        expected = native.receipt(SimpleNamespace(DT=dt), SimpleNamespace(solver=SimpleNamespace(WIDTH=width)),
                                  IDENTITY, n, run[key+"trace.csv"], wall, actual["floor"], actual["lid"])
        require(same_json(actual, expected), "candidate arm receipt")
        receipts[str(n)] = expected
        new_walls[n] = [(float(r["floor_impulse"]), float(r["lid_signed_impulse"])) for r in native.rows(wall)]
    old_union, new_union = native.compare(old, width), native.compare(new, width)
    require(old_union["samples"] == new_union["samples"] == 1139, "native displacement union")
    expected_summary = dict(**IDENTITY, label="DEVELOPMENT_ONLY", arms=receipts, status="MATCHED_PREFIX_COMPLETE",
                            old_grid_lid=old_union, new_material_lid=new_union, reference_MPa=native.REF_MPA,
                            u6_qualified=False, stage3_go=False, three_dimensional_go=False)
    require(same_json(json.loads(run["run/summary.json"]), expected_summary), "candidate summary")
    report = dict(**IDENTITY, candidate_sha256=expected_sha.lower(), fixed_reference_MPa=native.REF_MPA,
                  status="MATCHED_PREFIX_COMPLETE", label="DEVELOPMENT_ONLY",
                  u6_qualified=False, stage3_go=False, three_dimensional_go=False,
                  convention="Upward is positive. Whole-system delta Py is inferred from signed walls. "
                             "A null floor/abs(lid) ratio has a zero denominator. MPa equivalents use 10 J/(width dt).")
    for name, union, traces, walls in (("old_grid_lid", old_union, old, old_walls),
                                       ("new_material_lid", new_union, new, new_walls)):
        report[name] = {"pressure_union": dict(union, max_abs_gap_MPa=abs(union["peak"]["signed_gap_MPa"])),
                        "fixed_landmarks": landmarks(native, traces, walls, dt, width)}
        peak_step=new_union["peak"]["step_F24"]
        if peak_step>0 and peak_step % 2 == 0:
            report[name]["at_candidate_peak_native"]=landmarks(native,traces,walls,dt,width,[(peak_step//2,peak_step)])[0]
    return report


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("candidate", type=Path)
    cli.add_argument("--sha256", required=True, help="expected candidate TAR SHA-256 from the return receipt")
    cli.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    cli.add_argument("--native", type=Path, default=DEFAULT_NATIVE, help="release-bound lid_prefix.py")
    args = cli.parse_args()
    try:
        print(json.dumps(evaluate(args.candidate, args.sha256, args.baseline, args.native), indent=2, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, IndexError, tarfile.TarError) as exc:
        cli.exit(2, f"Readback failed: {exc}\n")
