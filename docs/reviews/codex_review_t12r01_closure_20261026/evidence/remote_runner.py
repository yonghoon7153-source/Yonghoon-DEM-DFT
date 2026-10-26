#!/usr/bin/env python3
"""Synthetic P1 boundary probes, pinned independently of the checkout's ULPR.

Run with python3 -I. Uses only local Git objects and temporary synthetic files.
This is preparation evidence, not a P2 producer, registration, or T12 qualification.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PIN = "4c29705fa1c4ba94737a858b206fa4f4c5bb2bde"
PREFIX = "docs/data/ps45_unload_20261009/"
FILES = {"ul_reader.py", "ul_gates.py", "ul_lib.py", "ul_observers.py", "ul_s3.py", "unload_params.json"}
EVIDENCE = "docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024"
PARAM_KEYS = ("schema", "units", "Ps_sign", "plate_fn_compressive_sign", "P_meas_report_MPa",
              "protocol", "windows", "steady", "records", "s3", "g_aux", "ke_rot_base",
              "surface", "selection", "arms", "tuples")
BED_KEYS = ("s0", "h0", "atoms", "orig_np", "s0_candidates")


def snapshot(repo, manifest, dest):
    if manifest["consumer_pin"] != PIN or manifest["source_prefix"] != PREFIX:
        raise ValueError("Consumer pin/prefix differs from this fixture specification")
    if set(manifest["files_sha256"]) != FILES:
        raise ValueError("Source manifest must cover the complete six-file import/params closure")
    verified = {}
    # The environment guard must override the caller. The explicit option also
    # fails closed on Git versions that do not support disabling lazy fetch.
    git_env = dict(os.environ, GIT_NO_LAZY_FETCH="1")
    for name, expected in sorted(manifest["files_sha256"].items()):
        result = subprocess.run(["git", "--no-lazy-fetch", "-C", str(repo), "show", f"{PIN}:{PREFIX}{name}"],
                                capture_output=True, check=False, env=git_env)
        if result.returncode:
            raise ValueError(f"Pinned Git object could not be read offline: {PIN}:{PREFIX}{name}; "
                             "Git with --no-lazy-fetch support is required. If objects are missing, "
                             "fetch origin codex/unloading-ulpri explicitly, then retry. "
                             "This read forces lazy fetch off.")
        digest = hashlib.sha256(result.stdout).hexdigest()
        if digest != expected:
            raise ValueError(f"Pinned source SHA256 mismatch: {name}")
        (dest / name).write_bytes(result.stdout)
        verified[name] = digest
    return verified


def write_dump(path, cols, rows, step, local=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    count, data = ("ENTRIES", "ENTRIES") if local else ("ATOMS", "ATOMS")
    path.write_text(f"ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF {count}\n{len(rows)}\n"
                    "ITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n0 0.2\n"
                    f"ITEM: {data} {' '.join(cols)}\n" +
                    "".join(" ".join(str(row[c]) for c in cols) + "\n" for row in rows), encoding="utf-8")


def run_probes(root, reader, gates, lib, s3, contract):
    P = lib.load_params()
    bed = "ps_7_3_r45"
    step = P["beds"][bed]["s0"]
    results = []
    boundaries = {"mass_outside_g2", "spin_outside_g2", "atom_mass_inventory_not_checked",
                  "gravity_UB", "gravity_G_UB", "dt_half_unchanged_w_halves_window"}

    def probe(name, function, expected, observe):
        try:
            actual = observe()
            passed = actual == expected
            entry = {"case": name, "function": function, "expected": expected,
                     "observed": actual, "pass": passed}
        except Exception as exc:
            entry = {"case": name, "function": function, "expected": expected,
                     "exception": f"{type(exc).__name__}: {exc}", "pass": False}
        positive = expected is True or expected == "PASS" or (isinstance(expected, dict) and bool(expected.get("authorized")))
        entry["kind"] = ("coverage_boundary" if name in boundaries else
                         "positive" if positive or name.startswith("window_") else "negative")
        results.append(entry)

    probe("extracted_p1_contract", "ul_lib.load_params + exact excerpt comparison", True,
          lambda: contract["ulpr_pin"] == PIN and
          contract["params"] == {k: P[k] for k in PARAM_KEYS} and
          contract["bed_parameters"] == {b: {k: P["beds"][b].get(k) for k in BED_KEYS} for b in reader.BEDS} and
          contract["physical_ready"] is False and contract["p2_registration"] is None and contract["T12"] == "NOT_RUN" and
          contract["source_params_sha256"] == hashlib.sha256(Path(lib.PARAMS).read_bytes()).hexdigest())

    atom = dict(zip(reader.ATOM_COLS, [1, 1, .01, .01, .1, .001, 1e-6,
                                     0, 0, 0, 0, 0, 0, 0, 0, 1e-10]))
    source = root / "original.liggghts"
    write_dump(source, reader.ATOM_COLS, [atom], step)
    for name, updates, expected in [
        ("equal_atom", {}, "PASS"), ("mass_outside_g2", {"mass": 2e-6}, "PASS"),
        ("spin_outside_g2", {"omegaz": 7}, "PASS"), ("phase_type_change", {"type": 2}, "FAIL")]:
        path = root / f"{name}.liggghts"
        write_dump(path, reader.ATOM_COLS, [{**atom, **updates}], step)
        probe(name, "ul_gates.g2_compare", expected,
              lambda p=path: gates.g2_compare(str(p), str(source), expected_step=step)["status"])

    for name, rows, frame_step, expected in [
        ("atom_full_positive", [atom], step, True),
        ("atom_wrong_step", [atom], step + 1, False),
        ("atom_fractional_id", [{**atom, "id": 1.5}], step, False),
        ("atom_duplicate_id", [atom, atom], step, False),
        ("atom_nonfinite_id", [{**atom, "id": "nan"}], step, False),
        ("atom_outside_s0_id", [{**atom, "id": 2}], step, False),
        ("atom_mass_inventory_not_checked", [{**atom, "mass": 2e-6}], step, True)]:
        path = root / f"{name}.liggghts"
        write_dump(path, reader.ATOM_COLS, rows, frame_step)
        probe(name, "ul_reader._atom_frame", expected,
              lambda p=path: reader._atom_frame(str(p), step, {1})[0] is not None)

    for name, first_kind, ext, expected in [
        ("s0_positive", "valid", False, True),
        ("s0_filename_is_not_step", "wrong_step", False, False),
        ("s0_corrupt_first_no_fallback", "corrupt", True, False),
        ("s0_absent_first_allows_ext", "absent", True, True)]:
        place = root / name
        first = place / bed / "in" / f"atom_{step}.liggghts"
        if first_kind != "absent":
            write_dump(first, reader.ATOM_COLS, [atom], step + (first_kind == "wrong_step"))
            if first_kind == "corrupt":
                first.write_text("ITEM: TIMESTEP\nbroken\n", encoding="utf-8")
        if ext:
            write_dump(place / bed / "EXT/post" / f"atom_{step}.liggghts", reader.ATOM_COLS, [atom], step)
        probe(name, "ul_reader._s0_frame", expected,
              lambda d=place: reader._s0_frame(str(d), bed, P)[0] == {1})

    history = {**atom, **{f"f_history_zwall_bot[{i}]": v for i, v in enumerate((.002, 0, 0, 0), 1)}}
    for name, value, expected in [("wall_history_equal", .002, True), ("wall_delta_max_changed", .003, False)]:
        probe(name, "ul_reader._hist_equal", expected,
              lambda v=value: reader._hist_equal([history], [{**history, "f_history_zwall_bot[1]": v}]))

    # c_cpl[23] is current overlap, NOT deltaMax history. Change an observed force.
    contact = {c: 0.0 for c in reader.CPL_COLS}
    contact.update({"c_cpl[7]": 1, "c_cpl[8]": 2, "c_cpl[10]": .01,
                    "c_cpl[16]": .003, "c_cpl[22]": .0001, "c_cpl[23]": .002})
    original_contact = root / "contact_original.liggghts"
    write_dump(original_contact, reader.CPL_COLS, [contact], step, local=True)
    for name, changed, columns, frame_step, expected in [
        ("contact_equal", {}, reader.CPL_COLS, step, "PASS"),
        ("contact_force_changed", {"c_cpl[10]": .02}, reader.CPL_COLS, step, "FAIL"),
        ("contact_missing_column", {}, reader.CPL_COLS[:-1], step, "NOT_COMPUTED"),
        ("contact_wrong_step", {}, reader.CPL_COLS, step + 1, "FAIL")]:
        path = root / f"{name}.liggghts"
        write_dump(path, columns, [{**contact, **changed}], frame_step, local=True)
        probe(name, "ul_gates.g2c_compare", expected,
              lambda p=path: gates.g2c_compare(str(p), str(original_contact), expected_step=step)["status"])
    probe("restore_missing_observation", "ul_gates.restoration_verdict", "UNCONFIRMED",
          lambda: gates.restoration_verdict(True, True, True, None, True, True))
    probe("restore_observed_mismatch", "ul_gates.restoration_verdict", "VALUE_MISMATCH",
          lambda: gates.restoration_verdict(True, True, True, False, True, True))

    def resume_fixture(name, **changes):
        d = root / name
        (d / "restart").mkdir(parents=True)
        events = [dict(event="CROSS", k="3", step="120", plate_z=".1", lift="0", detail="old_attempt"),
                  dict(event=changes.get("event_marker", "RESUME"), k=changes.get("event_k", "2.000e0"),
                       step=changes.get("event_step", "1e2"), plate_z=".1", lift="0", detail="restart")]
        if changes.get("duplicate_event"):
            events.append(events[-1].copy())
        if "extra_event_marker" in changes:
            events.append({**events[-1], "event": changes["extra_event_marker"], "k": "2.49"})
        for key, rows in (("events", events), ("windows", []), ("steps", [])):
            cols = P["records"][key + "_cols"]
            if key in ("windows", "steps"):
                for k, s in ((2, 100), (3, 120)):
                    row = {c: "0" for c in cols}
                    row.update(arm="UB", bed=bed, k=str(k), step=str(s))
                    if key == "windows":
                        row["w"] = "1"
                    else:
                        row.update(kind="A", n_windows="1")
                    rows.append(row)
            with (d / f"ul_{key}.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, cols)
                w.writeheader()
                w.writerows(rows)
                if key == "events" and changes.get("broken_csv"):
                    f.write("RESUME,2,100\n")
        state = f"variable ul_k equal {changes.get('state_k', '2')}\nvariable ul_rstep equal 100\n"
        if changes.get("duplicate_state"):
            state += "variable ul_k equal 2\n"
        (d / "restart/state_unload_100.in").write_text(state, encoding="utf-8")
        (d / "run_manifest.txt").write_text(changes.get("manifest", "resume_from=100\n"), encoding="utf-8")
        inputs = sorted(p for p in d.rglob("*") if p.is_file())
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
        run = reader.read_run(str(d), P)
        return {"authorized": [list(v) for v in run["resume_auth"]],
                "remaining_steps": [v["step"] for v in run["steps"]],
                "remaining_windows": [v["step"] for v in run["windows"]],
                "n_superseded_rows": run["n_superseded_rows"],
                "old_event_retained": any(v["event"] == "CROSS" for v in run["events"]),
                "raw_inputs_unchanged": before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                "has_problems": bool(run["problems"])}

    good = {"authorized": [[2, 100]], "remaining_steps": [100], "remaining_windows": [100],
            "n_superseded_rows": 2,
            "old_event_retained": False, "raw_inputs_unchanged": True, "has_problems": False}
    bad = {"authorized": [], "remaining_steps": [100, 120], "remaining_windows": [100, 120],
           "n_superseded_rows": 0,
           "old_event_retained": True, "raw_inputs_unchanged": True, "has_problems": True}
    for name, changes, expected in [
        ("resume_exact_scientific", {}, good),
        ("resume_exact_ascii_space", {"event_k": " 2.0 "}, good),
        ("resume_normal_crlf_manifest", {"manifest": "resume_from=100\r\n"}, good),
        ("resume_normal_cr_manifest", {"manifest": "resume_from=100\r"}, good),
        ("resume_fractional_k_precision", {"event_k": "2.0000000000000000001"}, bad),
        ("resume_fractional_step_precision", {"event_step": "100.000000000000000001"}, bad),
        ("resume_fractional_state_precision", {"state_k": "2.0000000000000000001"}, bad),
        ("resume_duplicate_event", {"duplicate_event": True}, bad),
        ("resume_duplicate_state", {"duplicate_state": True}, bad),
        ("resume_nonascii_space", {"event_k": "\u00a02"}, bad),
        ("resume_nonascii_manifest", {"manifest": "\u00a0resume_from=100\n"}, bad),
        ("resume_malformed_csv", {"broken_csv": True}, bad),
        ("resume_literal_fractional_coexisting", {"extra_event_marker": "RESUME"}, bad),
        ("resume_marker_leading_ascii_space", {"extra_event_marker": " RESUME"}, bad),
        ("resume_marker_trailing_ascii_space", {"extra_event_marker": "RESUME "}, bad),
        ("resume_marker_leading_nbsp", {"extra_event_marker": "\u00a0RESUME"}, bad),
        ("resume_marker_trailing_nbsp", {"extra_event_marker": "RESUME\u00a0"}, bad),
        ("resume_manifest_embedded_nel", {"manifest": "resume_from=100\nnote=old\u0085resume_from=100.49\n"}, bad),
        ("resume_manifest_embedded_ls", {"manifest": "resume_from=100\nnote=old\u2028resume_from=100.49\n"}, bad),
        ("resume_manifest_embedded_ps", {"manifest": "resume_from=100\nnote=old\u2029resume_from=100.49\n"}, bad),
        ("resume_single_leading_ls_raw_csv", {"event_marker": "\u2028RESUME"}, bad)]:
        probe(name, "ul_reader.read_run", expected, lambda n=name, c=changes: resume_fixture(n, **c))

    for job, expected in [("UB", "PASS"), ("G_UB", "FAIL")]:
        probe(f"gravity_{job}", "ul_reader._arm_g -> ul_s3.s3_residual", expected,
              lambda j=job: s3.s3_residual([atom], [], {1}, .2, atom_step=step, contact_step=step,
                                          g=reader._arm_g(j, P))["status"])
    for job, expected in [("UB", 5000), ("UT", 10000)]:
        probe(f"window_{job}", "ul_reader._arm_wsteps", expected,
              lambda j=job: reader._arm_wsteps(str(root / "no_deck"), j, P))
    override = root / "half_window"
    override.mkdir()
    (override / "deck.liggghts").write_text("variable ul_W equal 5000\n", encoding="utf-8")
    probe("dt_half_unchanged_w_halves_window", "ul_reader._arm_wsteps (actual deck override)", .0025,
          lambda: reader._arm_wsteps(str(override), "UT", P) * P["protocol"]["dt0"] * P["arms"]["UT"]["dt_factor"])
    probe("known_p1_rj_gate", "ul_reader.gate", True, lambda: reader.gate(str(root), bed, "RJ", P)[0])
    probe("unknown_p2_rj_gate", "ul_reader.gate", False, lambda: reader.gate(str(root), "P2_unregistered", "RJ", P)[0])
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", type=Path, help="Write a new receipt; refuses to replace an existing file")
    args = parser.parse_args()
    if not sys.flags.isolated:
        parser.error("Run with python3 -I")
    manifest_path = Path(__file__).resolve().parents[1] / EVIDENCE / "source-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        contract = json.loads((manifest_path.parent / "p1-consumer-contract.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix="dem-t12-synthetic-") as tmp:
            base = Path(tmp)
            src, fixtures = base / "source", base / "fixtures"
            src.mkdir()
            fixtures.mkdir()
            hashes = snapshot(args.repo, manifest, src)
            sys.path.insert(0, str(src))
            modules = [importlib.import_module(n) for n in ("ul_reader", "ul_gates", "ul_lib", "ul_s3")]
            for name in ("ul_reader", "ul_gates", "ul_lib", "ul_observers", "ul_s3"):
                if Path(sys.modules[name].__file__).resolve().parent != src.resolve():
                    raise ValueError(f"Module escaped pinned snapshot: {name}")
            cases = run_probes(fixtures, *modules, contract)
    except (ValueError, OSError, KeyError) as exc:
        print(f"T12 preparation source failure: {exc}", file=sys.stderr)
        return 2
    report = {"schema": "dem_gen2_t12_synthetic_consumer_receipt_v1", "consumer_pin": PIN,
              "source_sha256": hashes, "fixture_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python": sys.version.split()[0], "synthetic": True,
              "status": "PASS" if all(c["pass"] for c in cases) else "FAIL",
              "case_count": len(cases), "passed": sum(c["pass"] for c in cases),
              "physical_ready": False, "P2_registration": None, "physical_T12": "NOT_RUN",
              "research_runs_started": 0, "cases": cases}
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        with args.json.open("x", encoding="utf-8") as f:
            f.write(output)
    print(output, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
