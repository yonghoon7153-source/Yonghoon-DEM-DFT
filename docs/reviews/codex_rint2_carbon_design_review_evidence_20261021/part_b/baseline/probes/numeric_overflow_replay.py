"""Minimal local replay of existing RIMPR-04 finite-input arithmetic limitation."""
from pathlib import Path
import contextlib
import io
import json
import math
import os
import sys
import types
import warnings

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "--baseline" in sys.argv
SRC = ROOT.parent / "rint_g2_impl_reverify_20261015/source" if BASELINE else ROOT / "source"
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
sys.dont_write_bytecode = True
sys.path[:0] = [str(SRC / "scripts"), str(ROOT.parent / "lhs_coverage_review_20260930/deps"),
               str(ROOT.parent / "gen2_network_reverify3_20261007/deps")]
if os.name == "nt":
    resource = types.ModuleType("resource")
    resource.RUSAGE_SELF = 0
    resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=float("nan"))
    sys.modules["resource"] = resource
import numpy as np
import rint_iface_join as J
import step3_sigma as S


def paths(tag):
    return [ROOT / "tmp/numeric_current" / f"{tag}_{n}" for n in ("sc.csv", "atom.dump", "contact.dump")]


normal = J.am_iface_join(*paths("normal"), type_map={1: "AM_P", 2: "SE"})
with contextlib.redirect_stdout(io.StringIO()):
    sid, _ = S.rasterize(*(normal["particles"][k] for k in ("c_um", "r_um", "t")),
                        None, None, (0, 0, 0), (6, 4, 4), .25, bridge_um=.24)
ledger = S.am_iface_ledger(*(normal["particles"][k] for k in ("c_um", "r_um", "t")),
                          sid, sid, (0, 0, 0), .25,
                          delta_bound_um=normal["g_geo"]["delta_bound_um"], bridge_um=.24)
out = {"source": str(SRC), "cases": {}}
for tag in ("normal", "huge_nonam_inside_box", "huge_nonam_1e150_control"):
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        join = J.am_iface_join(*paths(tag), type_map={1: "AM_P", 2: "SE"})
    plan = S.am_iface_plan(ledger, {"AM_P|AM_P": .001}, join=join,
                          gap_law="cut", unreg_law="cut", ambiguous_arm="cut")
    rec = {"join_status": join["status"], "join_codes": [r["code"] for r in join["rejections"]],
           "entrance_status": join["entrance"]["status"],
           "max_delta_pos_ratio": join["g_frame"]["max_delta_pos_ratio"],
           "n_delta_pos_mismatch": join["g_frame"]["n_delta_pos_mismatch"],
           "delta_bound_um": join["g_geo"]["delta_bound_um"],
           "same_am_particles": normal["fp_particles"] == join["fp_particles"],
           "plan_codes": [r["code"] for r in plan["rejections"]],
           "warnings": [str(w.message) for w in ws]}
    try:
        S.iface_require_quantitative(plan, sid=sid, vox=.25)
        rec["quantitative_guard"] = "ACCEPT"
    except Exception as exc:
        rec["quantitative_guard"] = type(exc).__name__ + ": " + str(exc)
    if tag != "normal":
        atoms = J.read_atom_dump_frame(paths(tag)[1])
        contacts = J.read_contact_dump_frame(paths(tag)[2])
        row = 1
        dv = contacts["pos1"][row] - contacts["pos2"][row]
        hs = contacts["h_pos1"][row] + contacts["h_pos2"][row]
        with np.errstate(over="ignore"):
            distance_used = float(np.sqrt(np.sum(dv*dv)))
            tol_norm_used = float(np.sqrt(np.sum(hs*hs)))
        robust_distance = math.hypot(*dv)
        robust_tol = math.hypot(*hs) + float(atoms["hr"][2] + atoms["hr"][3] + contacts["h_delta"][row])
        robust_tol += 8 * np.finfo(float).eps * (.002 + robust_distance + .0005)
        rec["arithmetic"] = {
            "radius1": float(atoms["r"][2]), "radius2": float(atoms["r"][3]),
            "delta_dump": float(contacts["delta"][row]), "dx": float(dv[0]),
            "distance_used": distance_used, "tol_norm_used": tol_norm_used,
            "distance_hypot": robust_distance, "tolerance_hypot": robust_tol,
            "absolute_delta_mismatch_hypot": abs(.0005-(.002-robust_distance)),
            "hypot_mismatch_gt_tolerance": bool(abs(.0005-(.002-robust_distance)) > robust_tol),
            "all_atoms_inside_box": bool(((atoms["x"] >= atoms["box_lo"]) & (atoms["x"] <= atoms["box_hi"])).all())}
    out["cases"][tag] = rec
dest = ROOT / "evidence" / ("numeric_overflow_replay_baseline.json" if BASELINE else "numeric_overflow_replay_current.json")
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(out, ensure_ascii=False, indent=2))
