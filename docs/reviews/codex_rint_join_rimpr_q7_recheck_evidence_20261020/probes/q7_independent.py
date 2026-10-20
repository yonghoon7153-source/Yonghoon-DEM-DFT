"""Independent Q7/N9b review; immutable source snapshots, tiny FV diagnostics."""
from pathlib import Path
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import sys
import warnings

for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / "rint_g2_impl_reverify_20261015/source/scripts"
NEW = ROOT / "source/scripts"
sys.path[:0] = [str(NEW), str(ROOT.parent / "lhs_coverage_review_20260930/deps"),
               str(ROOT.parent / "gen2_network_reverify3_20261007/deps")]
import numpy as np
import scipy
from scipy.sparse.linalg import spsolve


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


S = load("q7_new_s3", NEW / "step3_sigma.py")
O = load("q7_old_s3", BASE / "step3_sigma.py")
sys.modules["step3_sigma"] = S
R = load("q7_rrm", NEW / "rint_rrm_reference.py")
SIG = S.electronic_sigma_table(.010, .005, 100., 10., 250.)
TABLE = {"AM_S|AM_S": .001, "AM_S|AM_P": .002, "AM_P|AM_P": .0015}
original_solvers = {S: S._solve_cg, O: O._solve_cg}
FIELDS = {}


def quiet(fn, *args, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kw)


def digest(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, np.ndarray):
        return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(eq(a[k], b[k]) for k in a)
    if isinstance(a, (tuple, list)):
        return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    return a == b


def rep(ans):
    out = {k: ans.get(k) for k in
           ("sigma_eff", "resid", "n_dof", "n_through_dof", "cg_info", "unconverged")}
    out["sigma_hex"] = ans["sigma_eff"].hex()
    p = ans.get("phi")
    if p is not None:
        out["phi"] = {"shape": list(p.shape), "dtype": str(p.dtype), "sha256": digest(p),
                      "min": float(np.min(p)), "max": float(np.max(p))}
    return out


def observe(fn):
    try:
        ans = fn()
        return {"accepted": True, "result": rep(ans) if isinstance(ans, dict) and "sigma_eff" in ans else bool(ans)}
    except Exception as ex:
        return {"accepted": False, "type": type(ex).__name__, "message": str(ex)}


def clone(p):
    return {k: v if k == "ledger" else copy.deepcopy(v) for k, v in p.items()}


def seal(p):
    p["fp_rows"] = S._iface_rows_fp(p["axes"])
    return p


def bed(axis=2):
    order = {0: [2, 0, 1], 1: [0, 2, 1], 2: [0, 1, 2]}[axis]
    c = np.array([[1.03, .97, 1.], [1.03, .97, 2.833]])[:, order]
    hi = np.array([2., 2., 3.833])[order]
    sid, pid = quiet(S.rasterize, c, np.ones(2), np.array([2, 2]), None, None,
                     (0., 0., 0.), hi, .1, bridge_um=.7)
    led = quiet(S.am_iface_ledger, c, np.ones(2), np.array([2, 2]), sid, sid,
                (0., 0., 0.), .1, delta_bound_um=0., bridge_um=.7)
    plans = {"cnc": S.am_iface_plan(led, TABLE), "rrm": R.rrm_plan(led, TABLE, resolve_k=4.)}
    return sid, pid, led, plans, dict(return_field=True, z_bot_um=0., z_top_um=float(hi[2]))


@contextlib.contextmanager
def recording_solver(module, direct=True):
    calls = []
    def solver(a, b):
        calls.append({"shape": list(a.shape), "nnz": a.nnz, "data": digest(a.data),
                      "indices": digest(a.indices), "indptr": digest(a.indptr), "rhs": digest(b)})
        return (spsolve(a.tocsc(), b), 0) if direct else original_solvers[module](a, b)
    saved = module._solve_cg
    module._solve_cg = solver
    try:
        yield calls
    finally:
        module._solve_cg = saved


def checked_solve(module, sid, plan, kw, direct=True):
    with recording_solver(module, direct) as calls:
        ans = quiet(module.solve_sigma_z, sid, SIG, .1, iface=plan, **kw)
    return ans, calls


out = {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
       "source_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [NEW / "step3_sigma.py", BASE / "step3_sigma.py", NEW / "rint_rrm_reference.py"]},
       "solver_note": "Unmodified assembly with common direct spsolve for exact comparison; native CG also run separately.",
       "bad_values": [], "positive_rotations": [], "n9b": {}, "schema_boundary": []}

# One actual non-cut row of each axis and family: 24 cases. RRM tombstones: 12 more.
for axis in range(3):
    sid, pid, led, plans, kw = bed(axis)
    for family, p in plans.items():
        assert not p["rejections"]
        a = p["axes"][axis]
        row = int(np.flatnonzero(~a["cut"])[0])
        out["positive_rotations"].append(
            {"axis": axis, "family": family, "shape": list(sid.shape),
             "film": p["n_film_rows"], "cut": p["n_cut_rows"],
             "gate": S.iface_require_quantitative(p, sid, SIG, vox=.1) is p})
        targets = [("film", row)]
        if a["cut"].any():
            targets.append(("cut", int(np.flatnonzero(a["cut"])[0])))
        for role, row_index in targets:
            for tag, val in [("nan", np.nan), ("positive_inf", np.inf),
                             ("negative_inf", -np.inf), ("negative", -.001)]:
                q = clone(p)
                q["axes"][axis]["rface"][row_index] = val
                seal(q)
                gate = observe(lambda: S.iface_require_quantitative(q, sid, SIG, vox=.1) is q)
                with recording_solver(S) as calls:
                    solve = observe(lambda: quiet(S.solve_sigma_z, sid, SIG, .1, iface=q, **kw))
                rec = {"axis": axis, "family": family, "row_role": role, "value": tag,
                       "fingerprint_matches": q["fp_rows"] == S._iface_rows_fp(q["axes"]),
                       "gate": gate, "solve": solve, "cg_calls": len(calls)}
                out["bad_values"].append(rec)
                assert not gate["accepted"] and gate["type"] == "ValueError" and "r_face" in gate["message"]
                assert not solve["accepted"] and solve["type"] == "ValueError" and len(calls) == 0

# Independent explicit controls on the fixture underlying the previous review numbers.
sid, pid, led, plans, kw = bed()
controls = {}
answers = {}
for family, p in plans.items():
    p0 = S.am_iface_plan(led, {"AM_S|AM_S": 0.}) if family == "cnc" else R.rrm_plan(led, {"AM_S|AM_S": 0.}, resolve_k=4.)
    p2 = clone(p)
    for a in p2["axes"]:
        a["rface"][~a["cut"]] *= 2.
    seal(p2)
    for tag, q in [("normal", p), ("registered_zero", p0), ("doubled_all", p2)]:
        name = family + "_" + tag
        ans, calls = checked_solve(S, sid, q, kw)
        old_ans, old_calls = checked_solve(O, sid, q, kw)
        controls[name] = {"gate": S.iface_require_quantitative(q, sid, SIG, vox=.1) is q,
                          "film": q["n_film_rows"], "cut": q["n_cut_rows"],
                          "zero_film_rows": sum(int(((a["rface"] == 0) & ~a["cut"]).sum()) for a in q["axes"]),
                          "zero_cut_rows": sum(int(((a["rface"] == 0) & a["cut"]).sum()) for a in q["axes"]),
                          "new": rep(ans), "baseline": rep(old_ans), "entire_result_identical": eq(ans, old_ans),
                          "matrix_rhs_identical": calls == old_calls}
        if family == "rrm":
            controls[name]["rrm_check_codes"] = [{"code": v["code"], "n": v["n"]} for v in R.rrm_check(q, led)]
            assert bool(controls[name]["rrm_check_codes"]) == (tag == "doubled_all")
        assert eq(ans, old_ans) and calls == old_calls
        answers[name] = ans
        FIELDS[name] = ans["phi"]
    assert answers[family + "_doubled_all"]["sigma_eff"] < answers[family + "_normal"]["sigma_eff"] < answers[family + "_registered_zero"]["sigma_eff"]
off, _ = checked_solve(S, sid, None, kw)
controls["cnc_zero_equals_off"] = {
    "sigma_hex": off["sigma_eff"].hex() == answers["cnc_registered_zero"]["sigma_eff"].hex(),
    "phi_bytes": eq(off["phi"], answers["cnc_registered_zero"]["phi"])}
assert all(controls["cnc_zero_equals_off"].values())
out["positive_controls"] = controls

# N9b: old NaN uses exactly the registered-zero matrix/rhs, including cut connectivity.
qnan = clone(plans["rrm"])
for a in qnan["axes"]:
    a["rface"][~a["cut"]] = np.nan
seal(qnan)
pzero = R.rrm_plan(led, {"AM_S|AM_S": 0.}, resolve_k=4.)
old_nan, nan_matrix = checked_solve(O, sid, qnan, kw)
old_zero, zero_matrix = checked_solve(O, sid, pzero, kw)
new_zero, new_zero_matrix = checked_solve(S, sid, pzero, kw)
same = {"sigma_hex": old_nan["sigma_eff"].hex() == old_zero["sigma_eff"].hex() == new_zero["sigma_eff"].hex(),
        "phi_bytes": eq(old_nan["phi"], old_zero["phi"]) and eq(old_nan["phi"], new_zero["phi"]),
        "n_dof": old_nan["n_dof"] == old_zero["n_dof"] == new_zero["n_dof"],
        "resid_hex": old_nan["resid"].hex() == old_zero["resid"].hex() == new_zero["resid"].hex(),
        "matrix_rhs": nan_matrix == zero_matrix == new_zero_matrix}
assert all(same.values())
FIELDS["old_rrm_nan"] = old_nan["phi"]
out["n9b"]["nan_zero"] = {"old_nan": rep(old_nan), "old_zero": rep(old_zero), "new_zero": rep(new_zero),
                         "exact_equal": same, "matrix": nan_matrix}
qcut = clone(plans["rrm"])
qcut["axes"] = tuple({k: v[~a["cut"]].copy() for k, v in a.items()} for a in qcut["axes"])
qcut["n_cut_rows"] = 0
qcut["record"]["iface_rrm"]["resolve_k"] = 5.
seal(qcut)
cut_ans, _ = checked_solve(S, sid, qcut, kw)
saved_plan = R.rrm_plan
R.rrm_plan = lambda *args, **kwargs: qcut  # bypass regeneration only, leave independent checker intact.
try:
    independent = R.rrm_check(qcut, led)
finally:
    R.rrm_plan = saved_plan
with recording_solver(S) as calls:
    wrapped = observe(lambda: quiet(R.rrm_solve, sid, SIG, .1, qcut, led, **kw))
out["n9b"]["cut_deleted_k_changed"] = {"generic_gate": S.iface_require_quantitative(qcut, sid, SIG, vox=.1) is qcut,
                                     "generic_solve": rep(cut_ans),
                                     "independent_check_regeneration_disabled": independent,
                                     "wrapper": wrapped, "wrapper_cg_calls": len(calls)}
assert independent and not wrapped["accepted"] and not calls
FIELDS["rrm_cut_deleted"] = cut_ans["phi"]
qpure = clone(qcut)
qpure["record"]["iface_rrm"]["resolve_k"] = 4.
R.rrm_plan = lambda *args, **kwargs: qpure
try:
    pure_independent = R.rrm_check(qpure, led)
finally:
    R.rrm_plan = saved_plan
out["n9b"]["pure_cut_deleted_independent"] = [{"code": v["code"], "n": v["n"]} for v in pure_independent]
assert out["n9b"]["pure_cut_deleted_independent"] == [{"code": "film_off_outside", "n": 85}]

# The normal plan contract uses 1D float64 row arrays. These explore error boundaries,
# not a claim that arbitrary dictionaries are authenticated by the generic value guard.
for tag in ("missing_rface", "rface_none", "rface_empty", "rface_2d", "rface_scalar",
            "float32_nan", "string_inf", "string_positive", "complex_imag_nan", "all_rows_removed"):
    q = clone(plans["rrm"])
    a = q["axes"][2]
    if tag == "missing_rface":
        a.pop("rface")
    elif tag == "rface_none":
        a["rface"] = None
    elif tag == "rface_empty":
        a["rface"] = np.zeros(0, dtype=np.float64)
    elif tag == "rface_2d":
        a["rface"] = a["rface"][:, None]
    elif tag == "rface_scalar":
        a["rface"] = np.array(.001)
    elif tag == "float32_nan":
        a["rface"] = a["rface"].astype(np.float32)
        a["rface"][0] = np.nan
    elif tag == "string_inf":
        a["rface"] = a["rface"].astype("U32")
        a["rface"][0] = "1e309"
    elif tag == "string_positive":
        a["rface"] = a["rface"].astype("U32")
    elif tag == "complex_imag_nan":
        a["rface"] = a["rface"].astype(np.complex128)
        film_index = int(np.flatnonzero(~a["cut"])[0])
        a["rface"][film_index] = complex(float(a["rface"][film_index].real), np.nan)
    elif tag == "all_rows_removed":
        q["axes"] = tuple(S._iface_empty_rows() for _ in range(3))
        q["n_film_rows"] = q["n_cut_rows"] = 0
    seal(q)
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        gate = observe(lambda: S.iface_require_quantitative(q, sid, SIG, vox=.1) is q)
        with recording_solver(S) as calls:
            solve = observe(lambda: quiet(S.solve_sigma_z, sid, SIG, .1, iface=q, **kw))
    out["schema_boundary"].append({"name": tag, "gate": gate, "solve": solve, "cg_calls": len(calls),
                                   "warnings": [str(w.message) for w in warns]})

# Full return-object equality on 16 OFF cases, including r1 and rasterization.
off_cases = []
c = np.array([[1., 1., 1.], [1., 1., 2.9]])
r = np.ones(2)
t = np.array([2, 1])
for h in (.1, .2):
    for order in ([0, 1], [1, 0]):
        for bridge in (.24, None):
            for rint in (None, {(1, 2): .001}):
                values = []
                for m in (O, S):
                    ss, pp = quiet(m.rasterize, c[order], r[order], t[order], None, None,
                                   (0., 0., 0.), (2., 2., 3.9), h, bridge_um=bridge)
                    with recording_solver(m):
                        ans = quiet(m.solve_sigma_z, ss, SIG, h, return_field=True,
                                    z_bot_um=0., z_top_um=3.9, rint=rint, pid=pp)
                    values.append((ss, pp, ans))
                equal = eq(values[0], values[1])
                assert equal
                off_cases.append({"h": h, "order": order, "bridge": bridge, "r1": bool(rint),
                                  "entire_result_and_raster_byte_equal": equal, "new": rep(values[1][2])})
out["off_cases"] = off_cases

# Native CG sanity with no numerical-function replacement beyond a forwarding spy.
out["native_cg"] = {}
for name, q in [("off", None), ("rrm", plans["rrm"]), ("rrm_zero", pzero), ("cnc", plans["cnc"])]:
    ans, calls = checked_solve(S, sid, q, kw, direct=False)
    old_ans, old_calls = checked_solve(O, sid, q, kw, direct=False)
    out["native_cg"][name] = {"new": rep(ans), "baseline": rep(old_ans),
                               "entire_result_identical": eq(ans, old_ans), "matrix_rhs_identical": calls == old_calls}
    assert eq(ans, old_ans) and calls == old_calls and not ans["unconverged"]

out["summary"] = {"negative_value_cases": len(out["bad_values"]),
                  "all_rejected_before_cg": all(not r["solve"]["accepted"] and not r["cg_calls"] for r in out["bad_values"]),
                  "off_byte_identical": len(off_cases), "native_cg_comparisons": len(out["native_cg"])}
(ROOT / "evidence/q7_independent.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
np.savez_compressed(ROOT / "evidence/q7_fields.npz", **FIELDS)
print(json.dumps(out["summary"], indent=2))
print("N9b old NaN / zero:", old_nan["sigma_eff"], same)
print("N9b finite cut deletion:", cut_ans["sigma_eff"])
