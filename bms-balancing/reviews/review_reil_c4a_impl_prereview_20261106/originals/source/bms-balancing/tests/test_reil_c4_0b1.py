"""REIL C4-0b1 — 배열 · 규칙 봉인 (profile Sobol 2 · 동시 Sobol 16 · label → seed 표 · 규칙 기록) + H 핵심
(목적 J_V · J_D · ρ · J_V^s · Phase A · 결합 ρ · 증인 분류 · 정확 잔차 · 문턱 · 공통 갱신) — 상태 문서 §46 (사용자 B 안).

합성 입력과 보존된 util 사본만 쓴다. REIL xlsx · pkl · 노트북은 열지 않는다. 실행 횟수는 §46 (RED 1 · GREEN 1 · 건조 1).
근거 절: 부속 A §1–§4 · 부속 B §1–§3 · v2 §5 (H4 정규화).
"""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_h as h

BMS = Path(__file__).resolve().parents[1]
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
UTIL_COPY = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "util_LFP.py.txt"
PHASE_A_ARRAYS = BMS / "reil_c4_arrays_20261013"
NEW_SEAL = BMS / "reil_c6_rebuild_20261013"
NEW_SEAL_MANIFEST = "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc"
ANNEX_A = BMS / "docs" / "REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md"
ANNEX_B = BMS / "docs" / "REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md"
F = Fraction


def _p0():
    return json.loads(P0_RESULT.read_text(encoding="utf-8"))


def _max_q():
    return F(_p0()["max_q"]["fraction"])


@pytest.fixture(scope="module")
def util():
    from scripts import reil_c5_pilot as c5
    mod, uf = c5.load_util(UTIL_COPY, c5.UTIL_COPY_SHA)
    return SimpleNamespace(mod=mod, file=uf)


# ======================================================================== (1) label · seed (부속 A §3-6 · 확인 요청 §1 토큰)
def test_01_label_format_and_seed_are_the_registered_strings():
    lab = h.label(3, "A0", "J_V", "profile", k="LII", grid_index=7)
    assert lab == "reil-v2a|3|A0|J_V|profile|LII|7|-"
    assert h.seed_of(lab) == int(hashlib.sha256(lab.encode("utf-8")).hexdigest()[:8], 16)
    sim = h.label(10, "A1", "J_Vs", "simultaneous", tau="0.05")
    assert sim == "reil-v2a|10|A1|J_Vs|simultaneous|-|-|0.05"
    assert h.label(0, "A0", "rho", "profile", k="m_P", grid_index=0) == "reil-v2a|0|A0|rho|profile|m_P|0|-"


@pytest.mark.parametrize("kw", [
    dict(row=11, region="A0", objective="J_V", stage="profile", k="m_P", grid_index=0),
    dict(row=True, region="A0", objective="J_V", stage="profile", k="m_P", grid_index=0),
    dict(row=0, region="A3", objective="J_V", stage="profile", k="m_P", grid_index=0),
    dict(row=0, region="A0", objective="JV", stage="profile", k="m_P", grid_index=0),
    dict(row=0, region="A0", objective="J_V", stage="profile", k="d_P", grid_index=0),
    dict(row=0, region="A0", objective="J_V", stage="profile", k="m_P", grid_index=-1),
    dict(row=0, region="A0", objective="J_V", stage="profile", k="m_P", grid_index=0, tau="0.02"),
    dict(row=0, region="A0", objective="J_V", stage="simultaneous", tau="0.03"),
    dict(row=0, region="A0", objective="J_V", stage="simultaneous", k="m_P", tau="0.02"),
    dict(row=0, region="A0", objective="J_V", stage="nominal"),
])
def test_01_label_rejects_tokens_outside_the_table(kw):
    row = kw.pop("row")
    with pytest.raises(ValueError):
        h.label(row, kw.pop("region"), kw.pop("objective"), kw.pop("stage"), **kw)


# ======================================================================== (2) 단위 77 (C4 v2 §1 · 부속 A §3-8)
def test_02_the_unit_table_has_77_units_in_a_fixed_order():
    us = h.units()
    assert len(us) == 77 and len({u["unit"] for u in us}) == 77
    by = {}
    for u in us:
        by.setdefault((u["objective"], u["region"]), []).append(u["row"])
    assert set(by) == {("J_V", "A0"), ("J_V", "A1"), ("J_V", "A2"), ("J_D", "A0"), ("rho", "A0"), ("J_Vs", "A0"), ("J_Vs", "A1")}
    assert all(sorted(v) == list(range(11)) for v in by.values())
    assert sum(u["hypothesis"] == "H1/H2" for u in us) == 33 and sum(u["hypothesis"] == "H3" for u in us) == 22
    assert sum(u["hypothesis"] == "H4" for u in us) == 22
    assert h.units() == us and us[0]["unit"] == "J_V|A0|0"


# ======================================================================== (3) 프로파일 격자 (부속 A §2-5 · §3-3)
def test_03_t_range_is_the_closed_form_in_exact_rationals():
    q = _max_q()
    assert h.t_range("m_P", "A0", q) == (F("0.6"), F("1.1"))
    assert h.t_range("m_N", "A1", q) == (F("0.3"), F("1.5"))
    assert h.t_range("LII", "A0", q) == (F("0.6") - F("0.5") / q, F("1.1") - F("1e-4") / q)
    assert h.t_range("LII", "A1", q) == (F("0.3") - F("2") / q, F("1.5") - F("1e-4") / q)
    assert h.t_range("LII", "A2", q) == (F("0.3") - F("2") / q, F("1.5") + F("2") / q)


def test_03_grid_is_41_exact_points_plus_nominal_offsets_with_duplicates_and_outside_dropped():
    q = _max_q()
    g = h.profile_grid("m_P", "A0", 0, q)                  # 명목 1.0 · 0.95 · 1.05 는 41 등분점과 같은 float → 중복
    base = [float(F("0.6") + F("0.5") * F(i, 40)) for i in range(41)]
    assert g["t"] == sorted(set(base) | {0.98, 1.02})
    assert {s["reason"] for s in g["skipped"]} == {"미평가 (중복)"} and len(g["skipped"]) == 3
    g3 = h.profile_grid("m_P", "A0", 3, q)                 # 명목 0.64 — 0.59 는 상자 밖
    assert len(g3["t"]) == 45 and 0.64 in g3["t"] and 0.59 not in g3["t"]
    assert [s["reason"] for s in g3["skipped"]] == ["미평가 (영역 밖)"]
    assert all(a < b for a, b in zip(g3["t"], g3["t"][1:]))
    gl = h.profile_grid("LII", "A0", 5, q)                 # 명목 LII 0.64
    lo, hi = h.t_range("LII", "A0", q)
    assert gl["t"][0] == float(lo) and gl["t"][-1] == float(hi) and 0.64 in gl["t"] and len(gl["t"]) <= 46
    assert len(gl["t_fraction"]) == len(gl["t"])


def test_03_free_variable_boxes_follow_the_elimination():
    assert h.free_box("m_P", "A0") == (("m_N", "d_P", "d_N"), ("0.5", "0.005", "0"), ("1.1", "0.5", "1"))
    assert h.free_box("m_N", "A2") == (("m_P", "d_P", "d_N"), ("0.3", "-0.5", "-0.5"), ("1.5", "1.5", "1.5"))
    assert h.free_box("LII", "A1") == (("m_P", "m_N", "d_P"), ("0.3", "0.3", "-0.5"), ("1.5", "1.5", "1.5"))


def test_03_region_boxes_agree_with_the_c6_seal_boxes():
    from scripts import reil_c6_profile as prof
    lo0, hi0 = h.region_bounds("A0")
    assert (list(lo0), list(hi0)) == prof.BOXES["A0_their_box"]
    for r in ("A1", "A2"):
        lo, hi = h.region_bounds(r)
        assert (list(lo), list(hi)) == prof.BOXES["A1_A2_wide_box"]


# ======================================================================== (4) 동시 상자 · PRIOR_INCOMPATIBLE 제외 (부속 A §3-4)
def test_04_simultaneous_box_and_the_p0_exclusion():
    q = _max_q()
    lo, hi = h.sim_box(0, "A0", "0.02", q)
    assert lo == (F("0.98"), F("0.98"), F("0.005"), F("0")) and hi == (F("1.02"), F("1.02"), F("0.5"), F("1"))
    lo5, hi5 = h.sim_box(9, "A1", "0.05", q)
    assert lo5[:2] == (F("0.59"), F("0.51")) and hi5[:2] == (F("0.69"), F("0.61"))
    assert h.sim_box(3, "A0", "0.02", q) is None and h.sim_box(2, "A0", "0.02", q) is None
    assert h.sim_box(2, "A1", "0.02", q) is not None


def test_04_the_p0_record_and_the_recomputed_status_must_agree():
    res = _p0()
    res["prior_table"] = [dict(e, status="PRIOR_COMPATIBLE") if (e["row"], e["tau"], e["region"]) == (3, "0.02", "A0") else e
                          for e in res["prior_table"]]
    with pytest.raises(h.HStop):
        h.array_plan(res)


# ======================================================================== (5) 배열 계획 · 봉인 (부속 B §2-1 · C4 v2 §4-3)
def test_05_the_array_plan_from_p0_has_134_simultaneous_labels_and_unique_seeds():
    plan = h.array_plan(_p0())
    prof_e = [e for e in plan["entries"] if e["stage"] == "profile"]
    sim_e = [e for e in plan["entries"] if e["stage"] == "simultaneous"]
    assert len(sim_e) == 134 and len(plan["skipped_simultaneous"]) == 20
    assert 77 * 3 * 41 <= len(prof_e) <= 77 * 3 * 46
    labels = [e["label"] for e in plan["entries"]]
    assert len(set(labels)) == len(labels)
    assert all(e["seed"] == h.seed_of(e["label"]) for e in plan["entries"])
    assert all(e["n"] == 2 and len(e["box_lo"]) == 3 for e in prof_e)
    assert all(e["n"] == 16 and e["use"] == 12 and len(e["box_lo"]) == 4 for e in sim_e)


def test_05_sobol_points_use_the_c6_generator_call():
    lo, hi = h.region_bounds("A0")
    a = h.sobol_points(0, lo, hi, 6)
    sealed = np.load(PHASE_A_ARRAYS / "sobol_A0_their_box_seed0.npy", allow_pickle=False)
    assert a.dtype == np.dtype("<f8") and np.array_equal(a, sealed)
    assert h.sobol_points(123, ("0", "0", "0"), ("1", "2", "3"), 1).shape == (2, 3)


def test_05_seal_writes_index_seed_table_rules_and_manifest_and_check_regenerates(tmp_path):
    out = tmp_path / "h_arrays"
    units = ["J_V|A0|3", "J_Vs|A1|0"]
    rec = h.seal_h_arrays(out, p0_result=P0_RESULT, units=units)
    names = {p.name for p in out.iterdir()}
    assert {"INDEX.json", "LABEL_SEED_TABLE.json", "RULES.json", "MANIFEST.json", "profile"} <= names
    man_b = (out / "MANIFEST.json").read_bytes()
    assert rec["manifest_sha256"] == hashlib.sha256(man_b).hexdigest()
    man = json.loads(man_b)
    assert man["units"] == units and man["complete"] is False
    idx = json.loads((out / "INDEX.json").read_text(encoding="utf-8"))
    sim = [e for e in idx["entries"] if e["stage"] == "simultaneous"]
    assert all(e["unit"] != "J_V|A0|3" for e in sim)                     # #3 A0 는 τ 둘 다 PRIOR_INCOMPATIBLE
    assert len([e for e in sim if e["unit"] == "J_Vs|A1|0"]) == 2
    e0 = idx["entries"][0]
    arr = np.load(out / e0["file"], allow_pickle=False)
    block = np.ascontiguousarray(arr[e0["rows"][0]:e0["rows"][1]], dtype="<f8")
    assert hashlib.sha256(block.tobytes()).hexdigest() == e0["raw_sha256"]
    table = json.loads((out / "LABEL_SEED_TABLE.json").read_text(encoding="utf-8"))
    assert [t[0] for t in table] == [e["label"] for e in idx["entries"]]
    chk = h.check_h_arrays(out, manifest_sha256=rec["manifest_sha256"], p0_result=P0_RESULT)
    assert chk["ok"] and chk["complete"] is False and chk["n_labels"] == len(table)
    with pytest.raises(h.HStop):
        h.seal_h_arrays(out, p0_result=P0_RESULT, units=units)          # 덮어쓰지 않는다


def test_05_check_fails_closed_on_a_changed_array_or_manifest(tmp_path):
    out = tmp_path / "h_arrays"
    rec = h.seal_h_arrays(out, p0_result=P0_RESULT, units=["rho|A0|1"])
    with pytest.raises(h.HStop):
        h.check_h_arrays(out, manifest_sha256="0" * 64, p0_result=P0_RESULT)
    f = sorted((out / "profile").iterdir())[0]
    a = np.load(f, allow_pickle=False)
    a[0, 0] = np.nextafter(a[0, 0], 2.0)
    np.save(f, a, allow_pickle=False)
    with pytest.raises(h.HStop):
        h.check_h_arrays(out, manifest_sha256=rec["manifest_sha256"], p0_result=P0_RESULT)


def test_05_rules_record_seals_the_label_format_and_the_annex_text():
    rules = h.rules_record()
    assert rules["label_format"] == "reil-v2a|<셀 #>|<영역>|<목적>|<단계>|<k>|<격자 index>|<τ>"
    assert rules["tokens"]["목적"] == ["J_V", "J_D", "rho", "J_Vs"]
    for key, path in (("annex_A", ANNEX_A), ("annex_B", ANNEX_B)):
        src = rules["sources"][key]
        assert src["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
        lines = path.read_text(encoding="utf-8").splitlines()
        for ex in src["excerpts"]:
            a, b = ex["lines"]
            assert ex["text"] == "\n".join(lines[a - 1:b])
    cats = {ex["rule"] for src in rules["sources"].values() for ex in src["excerpts"]}
    assert {"순회", "동률", "대체", "중복", "부족", "label", "격자", "동시", "seed"} <= cats
    assert "적응적" in rules["not_sealed_here"]


# ======================================================================== (6) 목적 — 교차 · 끝점 · V_full · J_V^s (부속 A §4 · B §3 · v2 §5)
Q5 = np.array([0.0, 1.0, 2.0, 3.0, 4.0])


def test_06_a_grid_point_crossing_is_one_crossing_identified_by_index():
    c = h.crossings(Q5, np.array([1.8, 1.9, 2.0, 2.1, 2.2]), 2.0)
    assert not c["flat"] and c["n_unique"] == 1
    assert c["items"] == [{"kind": "grid", "index": 2, "Q": 2.0}]


def test_06_a_touch_without_sign_change_counts_once_and_two_touches_are_two():
    assert h.crossings(Q5, np.array([2.2, 2.1, 2.0, 2.1, 2.2]), 2.0)["n_unique"] == 1
    assert h.crossings(Q5, np.array([2.0, 2.1, 2.2, 2.1, 2.0]), 2.0)["n_unique"] == 2


def test_06_a_flat_segment_at_the_cutoff_is_nonfinite():
    c = h.crossings(Q5, np.array([1.9, 2.0, 2.0, 2.1, 2.2]), 2.0)
    assert c["flat"] and c["n_unique"] is None


def test_06_interior_crossings_use_linear_interpolation_on_strict_sign_change():
    c = h.crossings(Q5, np.array([1.9, 2.1, 2.3, 2.4, 2.5]), 2.0)
    assert c["n_unique"] == 1 and c["items"][0]["kind"] == "interior" and c["items"][0]["interval"] == [0, 1]
    assert c["items"][0]["Q"] == 0.0 + (2.0 - 1.9) * (1.0 - 0.0) / (2.1 - 1.9)
    assert h.crossings(Q5, np.array([1.9, 2.1, 1.9, 2.1, 2.2]), 2.0)["n_unique"] == 3


def test_06_endpoint_gate_uses_nu_0_01_and_the_nearest_cutoff():
    ok = h.endpoint_gate(2.005, 3.595)
    assert ok["accepted"] and ok["c_a"] == 2.0 and ok["c_b"] == 3.6
    dis = h.endpoint_gate(3.6, 2.0)
    assert dis["accepted"] and dis["c_a"] == 3.6 and dis["c_b"] == 2.0
    assert not h.endpoint_gate(2.3365, 3.5525)["accepted"]          # P0 #0 의 기록값 — 시작이 cutoff 에서 0.34 V 떨어져 있다
    assert not h.endpoint_gate(2.0, 3.58)["accepted"]


def test_06_v_full_is_the_same_curve_objective_fun_builds(util):
    model, halfcell = h.synthetic_wide_inputs(util.mod)
    x = np.array([1.0, 1.0, 0.10, 0.05])
    fn, qmax = h.v_full(util.mod, x, halfcell)
    m = dict(model)
    util.mod.objective_fun(x, m, halfcell)
    assert np.array_equal(fn(model["Q_exp_interp"]), m["Vf_sim"])
    assert qmax == pytest.approx(1.0 * 3.2 - 0.10, abs=1e-12)


def test_06_j_v_and_j_d_are_square_roots_of_f2_and_f4(util):
    model, halfcell = h.synthetic_wide_inputs(util.mod)
    x = np.array([0.95, 1.0, 0.12, 0.05])
    f = util.mod.objective_fun(x, dict(model), halfcell)
    jv, jd = h.jv_jd(util.mod, x, dict(model), halfcell)
    assert jv == float(np.sqrt(f[1])) and jd == float(np.sqrt(f[3]))
    assert h.rho(jv, jd, 0.5 * jv, 2.0 * jd) == pytest.approx(2.0)
    assert h.jd_gate(model) == {"ok": True, "reason": None}
    empty = dict(model, dVdQ_exp_interp=np.full(100, 0.5))
    assert h.jd_gate(empty) == {"ok": False, "reason": "빈 마스크 (dVdQ_exp_interp < 0.4 인 점 0)"}


def test_06_rho_needs_finite_positive_denominators():
    for bad in (0.0, -1.0, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            h.rho(1.0, 1.0, bad, 1.0)


def test_06_j_vs_is_finite_on_a_crossing_curve_and_invariant_under_scaling(util):
    model, halfcell = h.synthetic_wide_inputs(util.mod)
    gate = h.endpoint_gate(float(model["V_exp_interp"][0]), float(model["V_exp_interp"][-1]))
    assert gate["accepted"]
    x = np.array([1.0, 1.0, 0.10, 0.05])
    r = h.j_vs(util.mod, x, model, halfcell, gate)
    assert math.isfinite(r["value"]) and r["reason"] is None and r["span"] > 0
    assert r["crossings"]["2.0"]["n_unique"] == 1 and r["crossings"]["3.6"]["n_unique"] == 1
    for c in (0.9, 1.1):
        rc = h.j_vs(util.mod, c * x, model, halfcell, gate)
        assert abs(rc["value"] - r["value"]) <= 1e-9
    rev = h.j_vs(util.mod, x, model, halfcell, h.endpoint_gate(3.6, 2.0))
    assert not math.isfinite(rev["value"]) and rev["reason"] == "span"


def test_06_j_vs_refuses_a_rejected_gate(util):
    model, halfcell = h.synthetic_wide_inputs(util.mod)
    with pytest.raises(ValueError):
        h.j_vs(util.mod, np.array([1.0, 1.0, 0.1, 0.05]), model, halfcell, h.endpoint_gate(2.3365, 3.5525))


def test_06_v_full_that_cannot_be_built_is_nonfinite_not_an_exception(util):
    model, halfcell = h.synthetic_wide_inputs(util.mod)
    gate = h.endpoint_gate(2.0, 3.6)
    r = h.j_vs(util.mod, np.array([0.3, 0.3, 1.5, -0.5]), model, halfcell, gate)   # Q_PE_hc_ad 전부 음수 → 슬라이스 < 2
    assert not math.isfinite(r["value"]) and r["reason"].startswith("V_full")


# ======================================================================== (7) 정확 잔차 · 증인 · 종료 (부속 A §2-1–§2-3 · B §1-2)
def test_07_exact_residuals_per_region_and_feasibility_class():
    r = h.exact_residuals([0.8, 0.8, 0.2, 0.1], "A0")
    assert r["box"] == 0 and r["g"] == 0 and h.feasibility_class(r) == "exact_feasible"
    r2 = h.exact_residuals([0.8, 0.8, 0.2, 0.1], "A2")
    assert r2["g"] is None and h.feasibility_class(r2) == "exact_feasible"
    near = h.exact_residuals([1.1 + 5e-11, 0.8, 0.2, 0.1], "A0")
    assert 0 < near["box"] <= F("1e-10") and h.feasibility_class(near) == "numerically_accepted"
    far = h.exact_residuals([0.8, 0.8, 0.2, 0.2], "A0")                  # d_P − d_N = 0 < 1e-4
    assert far["g"] == F("1e-4") and h.feasibility_class(far) == "infeasible"
    assert h.exact_residuals([0.8, 0.8, 0.2, 0.2], "A2")["g"] is None
    assert h.exact_residuals([float("nan"), 0.8, 0.2, 0.1], "A0") is None


def test_07_witness_reasons_are_the_registered_three():
    good = h.exact_residuals([0.8, 0.8, 0.2, 0.1], "A0")
    assert h.witness(solver_error=True, value=None, residuals=None) == "invalid:SOLVER_ERROR"
    assert h.witness(solver_error=False, value=float("nan"), residuals=good) == "invalid:NONFINITE"
    assert h.witness(solver_error=False, value=None, residuals=good) == "invalid:NONFINITE"
    assert h.witness(solver_error=False, value=0.1, residuals=None) == "invalid:NONFINITE"
    bad = h.exact_residuals([0.8, 0.8, 0.2, 0.2], "A0")
    assert h.witness(solver_error=False, value=0.1, residuals=bad) == "invalid:INFEASIBLE_RETURN"
    assert h.witness(solver_error=False, value=0.1, residuals=good) == "valid"


def test_07_termination_is_converged_budget_or_unclassified():
    from scipy._lib.cobyqa.settings import ExitStatus
    assert h.termination(SimpleNamespace(success=True, status=0)) == "converged"
    assert h.termination(SimpleNamespace(success=False, status=ExitStatus.MAX_EVAL_WARNING.value)) == "budget"
    assert h.termination(SimpleNamespace(success=False, status=ExitStatus.MAX_ITER_WARNING.value)) == "budget"
    assert h.termination(SimpleNamespace(success=False, status=ExitStatus.LINALG_ERROR.value)) == "unclassified"   # C4 v2 §5-4 (C4-0B1-N2)


def test_07_active_bounds_and_g_are_recorded():
    a = h.active_set([1.1, 0.8, 0.2, 0.2 - 1e-4], "A0")
    assert a["bounds"] == [["m_P", "hi"]] and a["g"] is True
    assert h.active_set([0.8, 0.8, 0.2, 0.0], "A2") == {"bounds": [], "g": None}


# ======================================================================== (8) Phase A (부속 A §3-2 · §2-3 · §2-4)
def _fake_util(kind="ok"):
    target = np.array([0.9, 0.8, 0.3, 0.1])

    def objective_fun(x, Model, halfcell):
        if kind == "value_error":
            raise ValueError("zero-size array to reduction operation maximum which has no identity")
        d = np.asarray(x, float) - target
        return np.array([0.0, float(d @ d) + 1e-6, 0.0, float(np.abs(d).sum()) + 1e-6])

    def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
        q = np.linspace(-0.5, 5.0, 50)
        return q, q, q, q, q, q, q, q
    return SimpleNamespace(objective_fun=objective_fun, dVdQ_hc=dVdQ_hc)


def _ctx(util_mod, **kw):
    model = {"Q_exp_interp": np.linspace(0.0, 3.0, 100), "V_exp_interp": np.linspace(2.0, 3.6, 100),
             "dVdQ_exp_interp": np.full(100, 0.2)}
    base = {"util": util_mod, "util_file": None, "models": {r: model for r in range(11)}, "halfcell": [None] * 4,
            "options": dict(h.DRY_OPTIONS), "gates": {}, "denominators": {}}
    base.update(kw)
    return base


def test_08_phase_a_tasks_are_128_per_unit_from_the_sealed_region_arrays():
    arrays = h.load_phase_a_arrays(PHASE_A_ARRAYS)
    us = [u for u in h.units() if u["unit"] in ("J_V|A0|0", "J_V|A2|0")]
    tasks = h.phase_a_tasks(us, arrays, n_workers=4)
    assert len(tasks) == 256 and [t["task_id"] for t in tasks] == list(range(256))
    a0 = [t for t in tasks if t["unit"] == "J_V|A0|0"]
    assert [t["run_id"] for t in a0] == list(range(128)) and {t["seed"] for t in a0[:64]} == {0}
    assert np.array_equal(np.array([t["x0"] for t in a0[:64]]), arrays[("A0", 0)])
    assert np.array_equal(np.array([t["x0"] for t in a0[64:]]), arrays[("A0", 1)])
    a2 = [t for t in tasks if t["unit"] == "J_V|A2|0"]
    assert np.array_equal(np.array([t["x0"] for t in a2[:64]]), arrays[("A2", 0)])
    assert all(t["worker"] == t["task_id"] % 4 for t in tasks)
    g_bad = sum(1 for t in a0 if t["x0"][2] - t["x0"][3] < 1e-4)
    assert g_bad > 0                                                    # G 위반 시작점은 그대로 둔다


def test_08_a_run_records_reeval_residuals_class_termination_and_constraints(monkeypatch):
    import scipy.optimize as so
    seen = {}
    real = so.minimize

    def spy(fun, x0, **kw):
        seen["bounds"], seen["constraints"] = kw.get("bounds"), kw.get("constraints")
        return real(fun, x0, **kw)
    monkeypatch.setattr(so, "minimize", spy)
    task = {"task_id": 0, "run_id": 5, "unit": "J_V|A0|2", "objective": "J_V", "region": "A0", "row": 2, "seed": 0,
            "x0": [0.7, 0.7, 0.3, 0.05], "worker": 0}
    row = h.run_phase_a(task, _ctx(_fake_util()))
    assert row["state"] == "COMPLETED" and row["termination"] in ("converged", "budget")
    assert row["witness"] == "valid" and row["feasibility_class"] in ("exact_feasible", "numerically_accepted")
    assert row["value"] == pytest.approx(math.sqrt(float(np.sum((np.array(row["x"]) - [0.9, 0.8, 0.3, 0.1]) ** 2)) + 1e-6))
    assert set(row["residuals"]) >= {"box", "g", "box_by_coord"} and isinstance(row["residuals"]["box"], str)
    assert seen["constraints"] is not None and list(seen["bounds"].lb) == [0.6, 0.5, 0.005, 0.0]
    task2 = dict(task, unit="J_V|A2|2", region="A2")
    row2 = h.run_phase_a(task2, _ctx(_fake_util()))
    assert seen["constraints"] in (None, [], ()) and row2["residuals"]["g"] is None


def test_08_a_util_error_is_solver_error_and_our_error_is_structural(monkeypatch):
    task = {"task_id": 0, "run_id": 0, "unit": "J_D|A0|1", "objective": "J_D", "region": "A0", "row": 1, "seed": 0,
            "x0": [0.7, 0.7, 0.3, 0.05], "worker": 0}
    util_file = Path(__file__).resolve()                                # 가짜 util frame = 이 시험 파일
    row = h.run_phase_a(task, _ctx(_fake_util("value_error"), util_file=str(util_file)))
    assert row["termination"] == "solver_error" and row["witness"] == "invalid:SOLVER_ERROR"
    assert row["error"]["kind"] == "local" and row["error"]["origin"] == "util"
    from scripts import reil_c4_monitor as mon
    monkeypatch.setattr(h, "witness", lambda **kw: 1 / 0)
    with pytest.raises(mon.Structural):
        h.run_phase_a(task, _ctx(_fake_util()))


def test_08_rho_runs_use_the_phase_a_denominators_and_record_both_components():
    task = {"task_id": 0, "run_id": 0, "unit": "rho|A0|4", "objective": "rho", "region": "A0", "row": 4, "seed": 1,
            "x0": [0.7, 0.7, 0.3, 0.05], "worker": 0}
    row = h.run_phase_a(task, _ctx(_fake_util(), denominators={4: (0.5, 0.25)}))
    assert row["witness"] == "valid" and set(row["components"]) == {"J_V", "J_D"}
    assert row["value"] == pytest.approx(max(row["components"]["J_V"] / 0.5, row["components"]["J_D"] / 0.25))
    with pytest.raises(Exception):
        h.run_phase_a(task, _ctx(_fake_util(), denominators={}))


def test_08_summary_is_min_over_valid_witnesses_with_seed_minima_and_reason_counts():
    rows = [
        {"run_id": 0, "seed": 0, "witness": "valid", "value": 0.30, "x": [1, 1, 1, 1], "termination": "converged"},
        {"run_id": 1, "seed": 0, "witness": "invalid:NONFINITE", "value": None, "x": [2, 2, 2, 2], "termination": "budget"},
        {"run_id": 64, "seed": 1, "witness": "valid", "value": 0.20, "x": [3, 3, 3, 3], "termination": "budget"},
        {"run_id": 65, "seed": 1, "witness": "valid", "value": 0.20, "x": [4, 4, 4, 4], "termination": "converged"},
        {"run_id": 66, "seed": 1, "witness": "invalid:INFEASIBLE_RETURN", "value": 0.01, "x": [5, 5, 5, 5],
         "termination": "converged"},
        {"run_id": 2, "seed": 0, "witness": "invalid:SOLVER_ERROR", "value": None, "x": None, "termination": "solver_error"},
    ]
    s = h.phase_a_summary(rows, expected=6)
    assert s["J0"] == 0.20 and s["x_hat"] == [3, 3, 3, 3] and s["argmin_run_id"] == 64
    assert s["per_seed_min"] == {"0": 0.30, "1": 0.20} and s["n_valid"] == 3 and not s["unfit"]
    assert s["invalid_by_reason"] == {"NONFINITE": 1, "INFEASIBLE_RETURN": 1, "SOLVER_ERROR": 1}
    assert s["termination_counts"] == {"converged": 3, "budget": 2, "solver_error": 1}
    assert s["ranked_run_ids"] == [64, 65, 0] and s["complete"]
    none = h.phase_a_summary([dict(r, witness="invalid:NONFINITE") for r in rows], expected=6)
    assert none["unfit"] and none["J0"] is None and none["x_hat"] is None


def test_08_rho_denominators_need_both_a0_units_finite_positive():
    ok = {"J_V|A0|4": {"unfit": False, "J0": 0.5}, "J_D|A0|4": {"unfit": False, "J0": 0.25}}
    assert h.rho_denominators(ok, 4) == (0.5, 0.25)
    assert h.rho_denominators({**ok, "J_D|A0|4": {"unfit": True, "J0": None}}, 4) is None
    assert h.rho_denominators({**ok, "J_V|A0|4": {"unfit": False, "J0": 0.0}}, 4) is None
    assert h.rho_denominators({"J_V|A0|4": ok["J_V|A0|4"]}, 4) is None


# ======================================================================== (9) 문턱 · 판독 · 공통 갱신 (부속 A §1)
def test_09_thresholds_follow_the_correspondence_table():
    s = 0.001
    t = h.thresholds("J_V", "A0", J_hat=0.010, sigma_v=s)
    assert t["H2"] == {"status": "OK", "T": 0.010 + 2 * s}
    assert t["H3"]["status"] == "OK" and t["H3"]["T_by_delta"] == {d: (1 + float(d)) * 0.010 for d in ("0.01", "0.05", "0.1", "0.2")}
    assert "H3" not in h.thresholds("J_V", "A1", J_hat=0.010, sigma_v=s)
    assert h.thresholds("J_V", "A2", J_hat=0.0, sigma_v=s)["H2"] == {"status": "OK", "T": 2 * s}
    assert h.thresholds("J_V", "A0", J_hat=0.0, sigma_v=s)["H3"]["status"] == "UNFIT"
    assert h.thresholds("J_V", "A0", J_hat=0.01, sigma_v=float("nan"))["H2"]["status"] == "UNFIT"
    assert h.thresholds("J_D", "A0", J_hat=0.2, sigma_v=s)["H3"]["T_by_delta"]["0.1"] == pytest.approx(0.22)
    assert h.thresholds("rho", "A0", J_hat=None, sigma_v=s, J_hat_V=0.01, J_hat_D=0.2)["H3"]["T_by_delta"]["0.1"] == pytest.approx(1.1)
    assert h.thresholds("rho", "A0", J_hat=None, sigma_v=s, J_hat_V=0.01, J_hat_D=float("inf"))["H3"]["status"] == "UNFIT"
    assert h.thresholds("J_Vs", "A1", J_hat=0.003, sigma_v=s)["H4"] == {"status": "OK", "T": 0.003 + 2 * s}
    assert h.thresholds("J_Vs", "A1", J_hat=float("nan"), sigma_v=s)["H4"]["status"] == "UNFIT"


def test_09_reading_marks_points_within_1e_9_as_near_boundary():
    assert h.reading(0.5, 0.5) == {"pass": True, "near_boundary": True}
    assert h.reading(0.5 + 5e-10, 0.5) == {"pass": False, "near_boundary": True}
    assert h.reading(0.4, 0.5) == {"pass": True, "near_boundary": False}
    assert h.reading(float("nan"), 0.5) == {"pass": False, "near_boundary": False}


def test_09_common_update_keeps_pools_independent_and_excludes_controls():
    rec = [
        {"row": 1, "region": "A0", "objective": "J_V", "stage": "phase_a", "valid": True, "value": 0.020},
        {"row": 1, "region": "A0", "objective": "J_V", "stage": "profile", "valid": True, "value": 0.015},
        {"row": 1, "region": "A0", "objective": "J_V", "stage": "profile", "valid": False, "value": 0.001},
        {"row": 1, "region": "A0", "objective": "J_D", "stage": "phase_a", "valid": True, "value": 0.30},
        {"row": 1, "region": "A0", "objective": "rho", "stage": "phase_a", "valid": True, "value": 1.0,
         "components": {"J_V": 0.010, "J_D": 0.33}},
        {"row": 1, "region": "A0", "objective": "J_Vs", "stage": "phase_a", "valid": True, "value": 0.004},
        {"row": 1, "region": "A0", "objective": "J_Vs", "stage": "ray", "valid": True, "value": 0.003},
        {"row": 1, "region": "A0", "objective": "J_Vs", "stage": "control_pos", "valid": True, "value": 0.0001},
    ]
    pre = {("J_V", "A0", 1): 0.020, ("J_D", "A0", 1): 0.30, ("J_Vs", "A0", 1): 0.004}
    u = h.common_update(rec, pre=pre)
    assert u["final"][("J_V", "A0", 1)] == 0.015 and u["final"][("J_D", "A0", 1)] == 0.30
    assert u["final"][("J_Vs", "A0", 1)] == 0.003                        # ray 포함 · 대조 제외
    assert all(u["final"][k] <= pre[k] for k in pre)
    assert u["combined_lower"] == [{"row": 1, "region": "A0", "objective": "J_V", "value": 0.010, "pool_min": 0.015}]
    assert u["rho_hat"][1]["search"] == 1.0
    assert u["rho_hat"][1]["final"] == pytest.approx(max(0.010 / 0.015, 0.33 / 0.30))


def test_09_common_update_refuses_a_final_above_the_pre_update_value():
    rec = [{"row": 0, "region": "A1", "objective": "J_V", "stage": "phase_a", "valid": True, "value": 0.03}]
    with pytest.raises(h.HStop):
        h.common_update(rec, pre={("J_V", "A1", 0): 0.02})


# ======================================================================== (10) 건조 — 계획 9,856 · 게이트 · 읽기만 (상태 §46 · §48 승인 경계 A1)
def test_10_dryrun_writes_only_the_plan(tmp_path):
    harr = tmp_path / "h_arrays"
    seal = h.seal_h_arrays(harr, p0_result=P0_RESULT)
    fake_ident = lambda **kw: {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}
    out = tmp_path / "dry"
    rec = h.dryrun(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=PHASE_A_ARRAYS,
                   h_arrays_dir=harr, h_manifest_sha256=seal["manifest_sha256"], util_copy=UTIL_COPY,
                   p0_result=P0_RESULT, env_identity=fake_ident)
    plan = json.loads((out / "PLAN.json").read_text(encoding="utf-8"))
    assert rec["ok"] and plan["phase_a"]["registered_runs"] == 9856
    assert plan["phase_a"]["wave1_runs"] == 66 * 128 and plan["phase_a"]["wave2_rho_runs"] == 11 * 128
    assert set(plan["gates"]["h4_endpoint"]) == {str(r) for r in range(11)}
    assert not (out / "SYNTHETIC_SAMPLE.json").exists()                 # 승인 경계 C4-0B1-A1 — 건조는 계획 · seed · 봉인만 읽는다
    assert plan["execution"] == {"optimizer_calls": 0, "objective_calls": 0, "util_imported": False, "sobol_generated": 0}
    with pytest.raises(h.HStop):
        h.dryrun(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=PHASE_A_ARRAYS,
                 h_arrays_dir=harr, h_manifest_sha256=seal["manifest_sha256"], util_copy=UTIL_COPY,
                 p0_result=P0_RESULT, env_identity=fake_ident)


def test_10_dryrun_refuses_incomplete_arrays_and_data_paths(tmp_path):
    harr = tmp_path / "h_arrays"
    seal = h.seal_h_arrays(harr, p0_result=P0_RESULT, units=["J_V|A0|0"])
    fake_ident = lambda **kw: {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}
    with pytest.raises(h.HStop):
        h.dryrun(tmp_path / "dry", venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=PHASE_A_ARRAYS,
                 h_arrays_dir=harr, h_manifest_sha256=seal["manifest_sha256"], util_copy=UTIL_COPY,
                 p0_result=P0_RESULT, env_identity=fake_ident)
    with pytest.raises(Exception):
        h.dryrun(tmp_path / "dry2", venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST,
                 arrays_dir=PHASE_A_ARRAYS, h_arrays_dir=harr, h_manifest_sha256=seal["manifest_sha256"],
                 util_copy=Path("/x/LFP_Data.xlsx"), p0_result=P0_RESULT, env_identity=fake_ident)


def test_10_the_cli_requires_explicit_paths():
    with pytest.raises(SystemExit):
        h.main(["seal-arrays", "--out", "/tmp/x"])
    with pytest.raises(SystemExit):
        h.main(["dryrun", "--venv", "/v"])
