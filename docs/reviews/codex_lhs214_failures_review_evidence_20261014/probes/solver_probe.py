"""Read-only review probes against the submitted pin; never edits source/ledgers.

Uses actual solve_network, _net_sigma_status and certificate_problem. Any fault
injection is temporary in-memory replacement of scipy call sites, restored after
each 3-node solve. No real-bed solve, subprocess, production data modification.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import math
import os
from pathlib import Path
import sys

for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["NETWORK_DEBUG"] = "1"
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
sys.path[:0] = [str(ROOT / "source/scripts"),
               str(WORK / "lhs_coverage_review_20260930/deps"),
               str(WORK / "gen2_network_reverify3_20261007/deps")]
import numpy as np
import scipy
import network_conductivity as nc


def network(plate_z=1.0):
    return {
        "nodes": {0, 1, 2}, "bottom": {0}, "top": {2},
        "scale": 1.0, "plate_z": plate_z, "box_x": 1.0, "box_y": 1.0,
        "edges": [{"id1": a, "id2": b, "R_total": 0.25,
                   "R_bulk": 0.1, "R_constriction": 0.15}
                  for a, b in ((0, 1), (1, 2))],
    }


def finite_numerics(info):
    """Separate inspection only; no modification of actual solver certificate.

    Call the actual certificate checker on a copy with only public eligibility
    status normalized, explicitly revealing its status gate vs numeric result.
    This is NOT a recommended production way to validate a model-limit record.
    """
    normalized = copy.deepcopy(info)
    normalized["status"] = "computed"
    return nc.certificate_problem(normalized)


def solve(name, net=None, mode="full", fault=None):
    net = network() if net is None else net
    old = {key: getattr(nc, key) for key in ("spsolve", "cg", "gmres")}
    if fault == "exception":
        def broken(*args, **kwargs):
            raise RuntimeError("review injected first-rung exception")
        nc.spsolve = broken
    elif fault in ("bad_certificate", "nonfinite_vector"):
        value = 0.0 if fault == "bad_certificate" else float("nan")
        nc.spsolve = lambda A, b: np.full(len(b), value)
        nc.cg = lambda A, b, **kwargs: (np.full(len(b), value), 0)
        nc.gmres = lambda A, b, **kwargs: (np.full(len(b), value), 0)
    elif fault == "not_converged":
        nc.spsolve = lambda A, b: np.full(len(b), float("nan"))
        nc.cg = lambda A, b, **kwargs: (np.zeros(len(b)), 1)
        nc.gmres = lambda A, b, **kwargs: (np.zeros(len(b)), 1)
    log = io.StringIO()
    result = None
    error = None
    try:
        with contextlib.redirect_stdout(log):
            result = nc.solve_network(net, mode=mode)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    finally:
        for key, value in old.items():
            setattr(nc, key, value)
    info = net.get("solve_info", {}).get(mode)
    q_reconstructed = (info["I_bottom"] * info["g_to_q"]
                       if info and info.get("I_bottom") is not None
                       and info.get("g_to_q") is not None else None)
    return {
        "name": name, "mode": mode, "fault": fault,
        "network": net, "return": result, "exception": error,
        "raw_q_from_adopted_current_and_geometry": q_reconstructed,
        "status_mapping": nc._net_sigma_status(result[1], not nc.active_fractions(net)["perc_nodes"], info) if result else None,
        "actual_certificate_problem": nc.certificate_problem(info),
        "numeric_checker_on_status_normalized_copy": finite_numerics(info) if info else None,
        "stdout": log.getvalue(),
    }


probes = [solve("normal_q0p5", network(0.25)),
          solve("full_q2_rejected_after_numeric_pass"),
          solve("full_q1p5_boundary", network(0.75)),
          solve("full_just_below_1p5", network(0.75 - 1e-8)),
          solve("full_just_above_1p5", network(0.75 + 1e-8)),
          solve("contact_free_q5_retained", mode="bulk_only"),
          solve("constriction_only_q3p333_retained", mode="constriction_only")]
thermal = network()
thermal["is_thermal"] = True
probes.append(solve("thermal_q2_retained", thermal))
overlap = network()
overlap["top"] = {0}
probes.append(solve("boundary_overlap_stays_noncomputed", overlap))
no_path = network()
no_path["top"] = {3}
no_path["nodes"].add(3)
probes.append(solve("no_through_path", no_path))
zero = network()
zero["edges"][0]["R_constriction"] = 0.0
probes.append(solve("constriction_zero_resistance", zero, "constriction_only"))
for fault in ("exception", "bad_certificate", "nonfinite_vector", "not_converged"):
    probes.append(solve(f"high_q_graph_with_{fault}", fault=fault))
zero_g = network()
for edge in zero_g["edges"]:
    edge["R_total"] = float("inf")
probes.append(solve("zero_conductance_hits_parallel_bound", zero_g))
probes.append(solve("infinite_geometry_must_not_be_model_limit", network(float("inf"))))
probes.append(solve("nan_geometry_must_not_be_model_limit", network(float("nan"))))

EV = ROOT / "submitted/lhs214_run_evidence_1014_1520"
failures = []
for p in sorted(EV.glob("*/failed/*/network_attempt.json")):
    attempt = json.loads(p.read_text(encoding="utf-8"))
    worker = json.loads((p.parent / "worker.json").read_text(encoding="utf-8"))
    w = worker["attempts"][-1]
    failures.append({
        "case": p.parent.name, "file": str(p.relative_to(ROOT)),
        "wrapper_rc": w["rc"], "signal": w["signal"], "attempt": w["attempt"],
        "peak_rss_mb": w["peak_rss_mb"],
        "stage_plan": w["stage_plan"]["stages"],
        "failure_kind": attempt["failure_kind"], "reason": attempt["reason"],
        "active_status": attempt["active_status"],
        "previous_generation_kept": attempt["previous_generation_kept"],
        "input_digests": attempt["input_digests"],
        "source_files": sorted(x.name for x in p.parent.iterdir()),
        "cause_evidence": "publication_failure_collapsed_solve_failed; per-case certificate absent",
    })

diagnostic = []
for mode in ("physics", "hertzian"):
    path = EV / "diag_lhsx054" / f"network_conductivity_{mode}.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    for prefix, channel in (("", "ionic"), ("electronic_", "electronic"), ("thermal_", "thermal")):
        cert = record[prefix + "solve_certificate_full"]
        diagnostic.append({
            "file": str(path.relative_to(ROOT)), "mode": mode, "channel": channel,
            "published_sigma": record[prefix + "sigma_full"],
            "certificate": cert,
            "q_reconstructed": cert["I_bottom"] * cert["g_to_q"] / cert["delta_V"],
            "actual_certificate_problem": nc.certificate_problem(cert),
            "numeric_checker_on_status_normalized_copy": finite_numerics(cert),
        })

by_name = {p["name"]: p for p in probes}
checks = {
    "full_q2_withheld": by_name["full_q2_rejected_after_numeric_pass"]["return"] == (None, None),
    "full_q2_numeric_pass": by_name["full_q2_rejected_after_numeric_pass"]["numeric_checker_on_status_normalized_copy"] is None,
    "full_q2_collapsed_to_solve_failed": by_name["full_q2_rejected_after_numeric_pass"]["status_mapping"] == ("not_computed", "solve_failed"),
    "q1p5_retained": by_name["full_q1p5_boundary"]["return"] == (2.0, 1.5),
    "q_above_1p5_withheld": by_name["full_just_above_1p5"]["return"] == (None, None),
    "q_below_1p5_retained": by_name["full_just_below_1p5"]["return"][1] < 1.5,
    "cf_q5_retained": by_name["contact_free_q5_retained"]["status_mapping"] == ("model_over_conduction", "q_gt_1p5"),
    "thermal_q2_retained": by_name["thermal_q2_retained"]["return"] == (2.0, 2.0),
    "overlap_preserved": by_name["boundary_overlap_stays_noncomputed"]["status_mapping"] == ("not_computed", "boundary_overlap"),
    "no_through_is_valid_zero": by_name["no_through_path"]["status_mapping"] == ("valid_zero", "no_through_path"),
    "exception_still_failed": by_name["high_q_graph_with_exception"]["status_mapping"] == ("not_computed", "solve_failed"),
    "certificate_failure_takes_precedence": by_name["high_q_graph_with_bad_certificate"]["status_mapping"] == ("not_computed", "current_conservation_failed"),
    "nonfinite_raw_q_has_same_guard_reason": by_name["infinite_geometry_must_not_be_model_limit"]["network"]["solve_info"]["full"]["status"] == "over_conduction_guard",
    "nan_raw_q_is_nonfinite": by_name["nan_geometry_must_not_be_model_limit"]["status_mapping"] == ("not_computed", "non_finite"),
    "fourteen_failures_inspected": len(failures) == 14,
    "all_fourteen_network_process_rc_zero": all(next(s for s in f["stage_plan"] if s["step"] == "Network Solver (both modes)")["rc"] == 0 for f in failures),
}
assert all(checks.values()), checks
result = {
    "scope": "read-only pinned actual-function 3-node synthetic probes and submitted JSON inspection",
    "pin": "1087a9b2f4a93aa6a3b0debc698a14fffa13488d",
    "source_sha256": hashlib.sha256((ROOT / "source/scripts/network_conductivity.py").read_bytes()).hexdigest(),
    "versions": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__},
    "assertions": checks,
    "probe_count": len(probes), "probes": probes,
    "production_failure_count": len(failures), "production_failures": failures,
    "standalone_lhsx054_diagnostic": diagnostic,
    "evidence_limit": "Only lhsx054 has a standalone channel certificate; absent raw inputs/digests in that diagnostic prevent independently binding it to the failed production attempt. Other thirteen lower-level causes are unproven.",
}


def strict_json(value):
    if isinstance(value, dict):
        return {key: strict_json(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [strict_json(val) for val in value]
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, (float, np.floating)) and not math.isfinite(value):
        return {"nonfinite": str(value)}
    if isinstance(value, np.integer):
        return int(value)
    return value


output = ROOT / "evidence/solver_probe_results.json"
output.write_text(json.dumps(strict_json(result), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
for p in probes:
    info = p["network"].get("solve_info", {}).get(p["mode"], {})
    print(p["name"], "return", p["return"], "status", info.get("status"),
          "reason", info.get("reason"), "mapping", p["status_mapping"],
          "numeric_issue", p["numeric_checker_on_status_normalized_copy"])
print("failures", len(failures), "diag", len(diagnostic), "output", output)
