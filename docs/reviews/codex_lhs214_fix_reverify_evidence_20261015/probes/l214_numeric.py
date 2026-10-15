"""Independent pinned-source numeric review; tiny synthetic networks only.

No source, registration, ledger or Git mutations. Generates review evidence.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
SOURCE = ROOT / "source"
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["TMP"] = os.environ["TEMP"] = str(ROOT / "tmp")
sys.dont_write_bytecode = True
sys.path[:0] = [str(SOURCE / "scripts"), str(SOURCE / "webapp"),
               str(WORK / "lhs_coverage_review_20260930/deps"),
               str(WORK / "gen2_network_reverify3_20261007/deps")]
import numpy as np
import scipy
import network_conductivity as nc
import tau_flux as tf
import pipeline_service as ps


def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def safe(fn, *args, **kwargs):
    try:
        return {"result": quiet(fn, *args, **kwargs), "error": None}
    except Exception as exc:
        return {"result": None, "error": f"{type(exc).__name__}: {exc}"}


def net3(**kw):
    d = {"nodes": {0, 1, 2}, "bottom": {0}, "top": {2},
         "plate_z": 1.0, "scale": 1.0, "box_x": 1.0, "box_y": 1.0,
         "edges": [{"id1": i, "id2": j, "R_total": 0.25,
                    "R_bulk": 0.1, "R_constriction": 0.15}
                   for i, j in ((0, 1), (1, 2))]}
    d.update(kw)
    return d


def solve_probe(label, mode="full", **kw):
    n = net3(**kw)
    out = safe(nc.solve_network, n, mode=mode)
    info = n.get("solve_info", {}).get(mode)
    ret = out["result"]
    out.update(label=label, geometry=info.get("geometry"), solve_info=info,
               model_limit_check=safe(nc.model_limit_certificate_problem, info),
               mapped_status=(safe(nc._net_sigma_status, ret[1], False, info, channel="ionic") if ret else None))
    return out


def certificate_result(cert):
    return {"certificate": cert, "check": safe(nc.model_limit_certificate_problem, cert)}


def record_result(rec, dual=None, ledger=None):
    out = {"full_model_limit": safe(tf.full_model_limit_problem, rec, "ionic", "physics"),
           "ion_record": safe(tf.ion_record_problem, rec),
           "certificate_binding": safe(tf.certificate_binding_problems, "physics", rec),
           "channel_verdict": safe(ps.channel_verdict, rec, "ionic", "physics")}
    if dual is not None:
        d = copy.deepcopy(dual)
        d["physics"] = rec
        out["generation"] = safe(tf.network_generation_contract, d)
        out["tau_columns"] = safe(tf.ion_columns, d, ledger, 100.0)
        folder = ROOT / "tmp/numeric_content"
        folder.mkdir(exist_ok=True)
        for mode, data in d.items():
            (folder / f"network_conductivity_{mode}.json").write_text(json.dumps(data), encoding="utf-8")
        out["content_verdict"] = safe(ps.network_content_verdict, str(folder))
    return out


def main():
    sols = [solve_probe("q2"), solve_probe("q1p5", plate_z=0.75),
            solve_probe("q1p5_nextdown", plate_z=math.nextafter(0.75, 0.0)),
            solve_probe("q1p5_nextup", plate_z=math.nextafter(0.75, math.inf)),
            solve_probe("thermal_q2", is_thermal=True),
            solve_probe("cf_q5", mode="bulk_only"),
            solve_probe("constriction_q10over3", mode="constriction_only")]
    for key in nc.CERT_GEOMETRY_FIELDS:
        for val in (True, "1", 0.0, -1.0, float("nan"), float("inf"), -float("inf")):
            sols.append(solve_probe(f"geometry_{key}_{val!r}", **{key: val}))
    sols.extend([solve_probe("geometry_scale_square_overflow", scale=1e200),
                 solve_probe("geometry_area_underflow", scale=1e-200),
                 solve_probe("q_intermediate_overflow", plate_z=1e308, box_x=1e154, box_y=1e154)])
    c0 = copy.deepcopy(sols[0]["solve_info"])
    mutations = {}
    for name, key, value in (("residual_1", "residual_rel", 1.0),
                             ("residual_nan", "residual_rel", float("nan")),
                             ("cons_1", "conservation_rel", 1.0),
                             ("krylov_nonzero", "krylov_info", 1),
                             ("error_present", "error", "RuntimeError: synthetic contradiction"),
                             ("outcome_fail", "outcome", "certificate_failed"),
                             ("current_mismatch", "I_bottom", 2.1)):
        c = copy.deepcopy(c0)
        c["attempts"][-1][key] = value
        mutations[name] = certificate_result(c)
    for steps in (1, 8, 16, 17, 32):
        c = copy.deepcopy(c0)
        for _ in range(steps):
            c["q_withheld"] = math.nextafter(c["q_withheld"], math.inf)
        mutations[f"q_plus_{steps}_ulp"] = certificate_result(c)
    c = copy.deepcopy(c0)
    c["geometry"].update(plate_z=1e308, box_x=1e154, box_y=1e154)
    mutations["overflow_q_reconstruction_geometry"] = certificate_result(c)
    c = copy.deepcopy(c0)
    c["geometry"]["scale"] = 1e200
    mutations["overflow_geometry_scale_square"] = certificate_result(c)

    # Independently constructed 21-node synthetic chain, not a real specimen.
    atoms = {i: {"type": 1, "x": 0., "y": 0., "z": float(i - 1), "radius": 1.} for i in range(1, 22)}
    contacts = [{"id1": i, "id2": i + 1, "contact_area": 0.5, "delta": 0.2} for i in range(1, 21)]
    dual = {mode: quiet(nc._run_all_networks, atoms, contacts, [1], [], {1: "SE"}, 1., 20., 1., 1., None, contact_mode=mode)
            for mode in ("hertzian", "physics")}
    dual = json.loads(json.dumps(dual))
    ledger = {"thickness_um": 20., "thickness_mass_conserving_um": 20.,
              "phi_se_mass_conserving": 21 * 4 / 3 * math.pi / 20}
    rec0 = dual["physics"]
    records = {"valid_synthetic": {"record": rec0, "results": record_result(rec0, dual, ledger)}}
    r = copy.deepcopy(rec0)
    c = r["solve_certificate_full"]
    c.update(I_bottom=1e308, I_top=-1e308, sum_g=1e308)
    c["attempts"][-1].update(I_bottom=1e308, I_top=-1e308)
    records["overflow_q_reconstruction_currents"] = {"record": r, "results": record_result(r, dual, ledger)}
    for key, val in (("residual_rel", 1.0), ("krylov_info", 1), ("conservation_rel", 1.0)):
        r = copy.deepcopy(rec0)
        r["solve_certificate_full"]["attempts"][-1][key] = val
        records[f"contradictory_attempt_{key}"] = {"record": r, "results": record_result(r, dual, ledger)}

    spec = importlib.util.spec_from_file_location("numeric_base_nc", ROOT / "base/scripts/network_conductivity.py")
    baseline_nc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline_nc)
    omitted = {"electronic_sigma_full_status", "electronic_sigma_full_reason", "thermal_sigma_full_status", "thermal_sigma_full_reason"}
    noimpact = {}
    for mode in ("hertzian", "physics"):
        args = (atoms, contacts, [1], [], {1: "SE"}, 1., 20., 3., 3., None)
        old = quiet(baseline_nc._run_all_networks, *args, contact_mode=mode)
        new = quiet(nc._run_all_networks, *args, contact_mode=mode)
        filtered = {k: v for k, v in new.items() if k not in omitted}
        # Python equality alone conflates 0/-0; canonical float.hex preserves that bit difference.
        def exact(x):
            if isinstance(x, float):
                return {"float_hex": x.hex()}
            if isinstance(x, dict):
                return {k: exact(v) for k, v in x.items()}
            if isinstance(x, (list, tuple)):
                return [exact(v) for v in x]
            return x
        noimpact[mode] = {"all_old_fields_bit_identical": exact(old) == exact(filtered),
                          "added_fields": {k: new[k] for k in omitted if k in new},
                          "old": old, "new": new}

    # Exact source comparison for the existing ladder (only independently scoped comments elsewhere changed).
    def ladder_bytes(path):
        s = path.read_bytes()
        start = s.index(b"    def _cg(A, b, M=None, maxiter=20000):")
        end = s.index(b"    # Convert to ", start)
        return s[start:end]
    new_ladder = ladder_bytes(SOURCE / "scripts/network_conductivity.py")
    old_ladder = ladder_bytes(ROOT / "base/scripts/network_conductivity.py")
    result = {"pin": "9e3ef54ca228111360bfe5f6d9dad4ebe26d54af", "base": "0c557e72aaffdf6cfd033c0667c643de4501c5b1",
              "scope": "3-node actual solver and 21-node synthetic producer; no real specimen or production run",
              "versions": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__},
              "source_sha256": hashlib.sha256((SOURCE / "scripts/network_conductivity.py").read_bytes()).hexdigest(),
              "ladder_bytes_identical": old_ladder == new_ladder,
              "solves": sols, "certificate_mutations": mutations, "records": records,
              "normal_synthetic_base_comparison": noimpact}
    outfile = ROOT / "evidence/numeric_probes.json"
    outfile.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    print(json.dumps({"evidence": str(outfile), "solves": len(sols), "certificate_mutations": len(mutations),
                      "records": len(records), "ladder_bytes_identical": old_ladder == new_ladder,
                      "overflow_record": records["overflow_q_reconstruction_currents"]["results"]["content_verdict"],
                      "attempt_record": records["contradictory_attempt_residual_rel"]["results"]["content_verdict"]}, ensure_ascii=False))


def selftests():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(sys.path[:4])
    result = []
    for script, flags, label in (("scripts/test_lhs214_model_limit.py", ["--selftest"], "model_limit"),
                                  ("scripts/network_conductivity.py", ["--selftest"], "network")):
        cmd = [sys.executable, "-X", "utf8", "-B", script, *flags]
        p = subprocess.run(cmd, cwd=SOURCE, env=env, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = ROOT / f"evidence/numeric_selftest_{label}.log"
        log.write_text(p.stdout, encoding="utf-8")
        result.append({"command": cmd, "cwd": str(SOURCE), "returncode": p.returncode, "log": str(log), "tail": p.stdout.splitlines()[-4:]})
    (ROOT / "evidence/numeric_selftests.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    if any(r["returncode"] for r in result):
        raise SystemExit(1)


if __name__ == "__main__":
    selftests() if "--selftests" in sys.argv else main()
