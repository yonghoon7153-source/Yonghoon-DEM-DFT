"""Independent launch-gate review; synthetic files only, no launcher/simulator.

Reuses historical fixture builders, but imports all production modules and
extracts the rest gate from the pinned round-6 source mirror.  The historical
probe's main is never called. All writes are to disposable fixtures or this
agent's output directory.
"""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
HIST = ROOT / "fixture_helpers.py"
ns = {"__name__": "fixture_helpers_only", "__file__": str(ROOT / "fixture_helpers.py")}
exec(compile(HIST.read_text(encoding="utf-8"), str(HIST), "exec"), ns)
sc, mi, np = ns["sc"], ns["mi"], ns["np"]
results = {}


def analyze(run, ref):
    with contextlib.redirect_stdout(io.StringIO()):
        z = mi.analyse(str(run), str(ref), .013138, cells=16, x_cells=4, n_min=20, axis="x")
    return {"complete": z["smoke"]["complete"], "tech_smoke": z["smoke"]["tech_smoke"],
            "expected": z["smoke"]["expected"], "present": z["smoke"]["present"]}


def check_gate(key, invoke, expected):
    got = invoke()
    got["expected_rc"] = expected
    got["matches_expected"] = got["rc"] == expected
    results[key] = got


with tempfile.TemporaryDirectory(prefix="hbr6_launch_") as tmp:
    td = Path(tmp)
    d = ns["rundir"](td, "start_guard", ns["SMALL"])
    binary = td / "guard_binary"
    binary.write_bytes(b"not-a-simulator")
    good = ns["bind"](d, binary, backend="slurm")
    runner = d / "run_lh.sbatch"
    env = dict(os.environ, SLURM_NTASKS="20", SLURM_JOB_ID="12345", PYTHONIOENCODING="utf-8")
    invalid = [("empty_dict", {}), ("null", None), ("list", []), ("string", "invalid")]
    for key, value in (("valid", good), *invalid):
        ns["js"](d / "launch_record.json", value)
        p = subprocess.run([sys.executable, str(ROOT / "dem_scripts/mixer_20260921/start_check.py"),
                            str(d), str(binary), str(runner)], env=env, capture_output=True,
                           text=True, encoding="utf-8")
        okp = d / "job_start.json"
        results["start_" + key] = dict(rc=p.returncode, expected_rc=0 if key == "valid" else 3,
            stdout=p.stdout, stderr=p.stderr, job_start_exists=okp.exists(),
            refused_exists=(d / "job_start.refused.12345.json").exists())
        if okp.exists():
            okp.unlink()
    # Broad malformed mandatory-field matrix tests actual pure checker.
    for key, path, value in [
        ("np_bool", ("slurm", "np"), True), ("np_float", ("slurm", "np"), 20.0),
        ("np_zero", ("slurm", "np"), 0), ("no_binary_sha", ("lmp_sha256",), None),
        ("no_deck_sha", ("sha256", "in.mixer"), None),
        ("bad_runner_sha", ("slurm", "runner_sha256"), "z" * 64),
        ("relative_binary", ("lmp_realpath",), "binary"), ("wrong_backend", ("backend",), "local"),
    ]:
        q = copy.deepcopy(good)
        target = q
        for k in path[:-1]:
            target = target[k]
        target[path[-1]] = value
        ns["js"](d / "launch_record.json", q)
        record, why = sc.check(str(d), str(binary), str(runner), env)
        results["shape_" + key] = dict(ok=record["ok"], reasons=why, expected_ok=False)

    with contextlib.redirect_stdout(io.StringIO()):
        run, ref, cert, original, invoke = ns["smoke_fixture"](td / "smoke")
    check_gate("smoke_normal", invoke, 0)
    source = run / "post/mix_400.liggghts"
    duplicate = run / "post/copy_400.liggghts"
    shutil.copyfile(source, duplicate)
    check_gate("smoke_after_duplicate", invoke, 1)
    results["reader_after_duplicate"] = analyze(run, ref)
    duplicate.unlink()
    offgrid = run / "post/mix_410.liggghts"
    offgrid.write_text(source.read_text().replace("ITEM: TIMESTEP\n400\n", "ITEM: TIMESTEP\n410\n"), encoding="utf-8")
    check_gate("smoke_after_offgrid", invoke, 1)
    results["reader_after_offgrid"] = analyze(run, ref)
    offgrid.unlink()
    e0dup = ref / "post/copy_200.liggghts"
    shutil.copyfile(ref / "post/mix_200.liggghts", e0dup)
    check_gate("smoke_after_e0_duplicate", invoke, 1)
    try:
        results["reader_after_e0_duplicate"] = analyze(run, ref)
    except SystemExit as e:
        results["reader_after_e0_duplicate"] = {"refused": str(e)}
    e0dup.unlink()
    later = run / "post/copy_1400.liggghts"
    shutil.copyfile(run / "post/mix_1400.liggghts", later)
    check_gate("smoke_after_bin1_duplicate", invoke, 0)
    results["reader_after_bin1_duplicate"] = analyze(run, ref)
    later.unlink()
    # Normal certificate only sees through bin0; later live-run additions remain accepted.
    early = copy.deepcopy(original)
    early["provenance"]["run"]["frames"] = mi.frame_bundle(
        [(s, p) for s, p in ns["cv"].frames(str(run / "post")) if 200 <= s < 1200])
    ns["js"](cert, [early])
    check_gate("smoke_with_later_bin_additions", invoke, 0)
    # Q5: actual rest gate accepts a strict allowlist with no M, S0, SR, rows/by_rev.
    opaque = {k: copy.deepcopy(original[k]) for k in ("run", "provenance", "plan", "t0_step")}
    opaque["smoke"] = {"complete": original["smoke"]["complete"],
                       "tech_smoke": original["smoke"]["tech_smoke"],
                       "qc_repr": {"pass": original["smoke"]["qc_repr"]["pass"]}}
    ns["js"](cert, [opaque])
    check_gate("opaque_allowlisted_certificate", invoke, 0)
    results["opaque_projection_fields"] = {"top_level": sorted(opaque), "smoke": sorted(opaque["smoke"]),
                                            "qc_repr": sorted(opaque["smoke"]["qc_repr"])}
    # Snapshot/plan fields in a certificate are trusted claims: demonstrate scope.
    # This explicitly edits the certificate and is NOT asserted as an accidental-data bypass.
    tampered = copy.deepcopy(opaque)
    tampered["plan"]["steps_per_rev"] = 1.0
    ns["js"](cert, [tampered])
    shutil.copyfile(source, duplicate)
    check_gate("tampered_certificate_narrows_bin0", invoke, 0)
    duplicate.unlink()

    # Non-integer period control checks semantics beyond the regex-equality test.
    with contextlib.redirect_stdout(io.StringIO()):
        run, ref, cert, original, invoke = ns["smoke_fixture"](td / "fractional")
    deck = run / "in.mixer"
    deck.write_text(deck.read_text().replace("period 1\n", "period 1.00025\n"), encoding="utf-8")
    lr = json.loads((run / "launch_record.json").read_text())
    lr["sha256"]["in.mixer"] = ns["sha"](deck)
    lr["cohort"][run.name]["in.mixer"] = ns["sha"](deck)
    ns["js"](run / "launch_record.json", lr)
    with contextlib.redirect_stdout(io.StringIO()):
        actual = mi.analyse(str(run), str(ref), .013138, cells=16, x_cells=4, n_min=20, axis="x")
    ns["js"](cert, [actual])
    results["fractional_window"] = {"steps_per_rev": actual["plan"]["steps_per_rev"],
                                    "expected": actual["smoke"]["expected"]}
    check_gate("fractional_smoke_normal", invoke, 0)
    for step, expected in ((1200, 1), (1240, 0)):
        duplicate = run / f"post/copy_{step}.liggghts"
        shutil.copyfile(run / f"post/mix_{step}.liggghts", duplicate)
        check_gate(f"fractional_duplicate_{step}", invoke, expected)
        results[f"fractional_reader_{step}"] = analyze(run, ref)
        duplicate.unlink()

results["scope"] = "Only start_check CLI/functions, reader functions, and Python extracted from rest; no shell launch, MPI, SLURM, or DEM invocation. Synthetic data only."
results["pin"] = "18787ab98a13361c37b2343bd07ae276142d0953"
(OUT / "probe_launch_output.json").write_text(json.dumps(ns["clean"](results), ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
print(json.dumps({k: ({x: v[x] for x in ("rc", "expected_rc", "matches_expected") if x in v} if "rc" in v else v)
                  for k, v in results.items() if isinstance(v, dict)}, ensure_ascii=False, indent=2))
assert all(v.get("matches_expected", True) for v in results.values() if isinstance(v, dict))
