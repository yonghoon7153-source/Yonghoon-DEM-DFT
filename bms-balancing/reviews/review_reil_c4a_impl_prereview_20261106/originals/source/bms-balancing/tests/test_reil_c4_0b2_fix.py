"""REIL C4-0b2 한정 보완 (C4B2-N1 · N2 · N3) — 중단 집계 · 저장 float 격자 중심 · 발견 폭의 근거 / 등급 / 부가 라벨 (결과 검토 회신 2026-10-14 · 상태 문서 §57).

승인 전 고정본: `docs/REIL_C4_0B2_FIX_CONTROLS_DRAFT_20261014.py.txt`. 승인 뒤 `tests/test_reil_c4_0b2_fix.py` 로 바이트 그대로 복사해 쓴다
(sha256 은 승인 요청문 `docs/REIL_C4_0B2_FIX_APPROVAL_REQUEST_20261014.md`). 고칠 곳 `docs/REIL_C4_0B2_FIX_PATCH_DRAFT_20261014.diff` 도 같이 고정.

합성 입력만 쓴다 — tmp 에 쓰는 가짜 util · 가짜 minimize · 만든 완료 행 (최적화 0) · 합성 저장 기록 · 봉인 배열 (읽기만) · P0 기록. 보존 util 사본 ·
REIL 자료는 쓰지 않고 Sobol 을 새로 만들지 않는다. 각 시험 docstring 의 [RED …] 는 지금 코드 (패치 전) 에서의 예상이다 — 다섯 모두 행동 반례
(AssertionError) 이고, 실패하는 단언 앞의 단언은 RED 에서도 지난다.
"""
import importlib.machinery
import importlib.util
import json
import warnings
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_h as h
from scripts import reil_c4_hb as hb

BMS = Path(__file__).resolve().parents[1]
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
PHASE_A_ARRAYS = BMS / "reil_c4_arrays_20261013"
H_ARRAYS = BMS / "reil_c4_arrays_0b1_20261013"
F = Fraction
MAX_Q = F(json.loads(P0_RESULT.read_text(encoding="utf-8"))["max_q"]["fraction"])
UNKNOWN = "Unknown solver options: not_a_cobyqa_option"

FAKE_UTIL = '''
import numpy as np

MODE = {"kind": "ok", "calls": 0}
TARGET = np.array([0.9, 0.8, 0.3, 0.1])


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    q = np.linspace(-0.5, 5.0, 50)
    return q, q, q, q, q, q, q, q


def objective_fun(x, Model, halfcell):
    MODE["calls"] += 1
    d = np.asarray(x, dtype=float) - TARGET
    return np.array([0.0, float(d @ d) + 1e-6, 0.0, float(np.abs(d).sum()) + 1e-6])
'''


def MODEL():
    return {"Q_exp_interp": np.linspace(0.0, 3.0, 100), "V_exp_interp": np.linspace(2.0, 3.6, 100), "dVdQ_exp_interp": np.full(100, 0.2)}


@pytest.fixture
def fake(tmp_path):
    """가짜 util 을 파일로 써서 경로로 로드한다 — 그 frame 이 util 로 분류되게 (C4-0b2 시험과 같은 방식)."""
    p = tmp_path / "fake_util_LFP_b2f.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4b2f_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    ctx = {"util": mod, "util_file": str(p.resolve()), "models": {r: MODEL() for r in range(11)}, "halfcell": [None] * 4,
           "options": dict(h.DRY_OPTIONS), "gates": {r: {"accepted": False} for r in range(11)}, "denominators": {},
           "max_q": MAX_Q, "sigma_v": {r: 0.01 for r in range(11)}}
    return SimpleNamespace(mod=mod, ctx=ctx, tmp=tmp_path)


@pytest.fixture(scope="module")
def arrays():
    return h.load_phase_a_arrays(PHASE_A_ARRAYS)


def _fake_minimize(monkeypatch, *, warn=False, n_calls=1):
    """가짜 minimize — warn 이면 scipy 와 같은 모르는 옵션 경고를 먼저 낸다 · 목적을 n_calls 번 부른 뒤 x0 를 돌려준다."""
    import scipy.optimize as so

    def fake_min(fun, x0, **kw):
        if warn:
            warnings.warn(UNKNOWN, so.OptimizeWarning)
        for _ in range(n_calls):
            fun(np.asarray(x0, dtype=float))
        return SimpleNamespace(x=np.asarray(x0, dtype=float), fun=0.5, status=0, success=True, message="fake status", nfev=n_calls, nit=1)
    monkeypatch.setattr(so, "minimize", fake_min)


def _unit(name):
    return next(u for u in h.units() if u["unit"] == name)


def _fab_pa_runner():
    """Phase A 작업을 돌리지 않고 완료 행을 만드는 실행기 (최적화 · 목적 호출 0) — C4-0b2 시험의 것과 같은 꼴."""
    def runner(tasks, ctx, task_fn):
        assert task_fn is h.run_phase_a
        states = []
        for t in tasks:
            x, v = list(t["x0"]), 0.1 + 0.001 * t["run_id"]
            states.append({"task_id": t["task_id"], "run_id": t["run_id"], "unit": t["unit"], "objective": t["objective"],
                           "region": t["region"], "row": t["row"], "seed": t["seed"], "x0": x, "x": x, "value": v, "witness": "valid",
                           "termination": "converged", "components": {"J_V": v, "J_D": v} if t["objective"] == "rho" else None,
                           "residuals": {"box": "0", "box_by_coord": ["0"] * 4, "g": None if t["region"] == "A2" else "0"},
                           "feasibility_class": "exact_feasible", "n_out_PE": 0, "n_out_NE": 0, "state": "COMPLETED"})
        return {"states": states, "global_stop": None}
    return runner


def _fab_b_row(task, value):
    """Phase B 작업의 완료 행 (최적화 0) — x 는 시작과 다른 고정점."""
    return {"task_id": task["task_id"], "unit": task["unit"], "stage": task["stage"], "k": task["k"], "grid_index": task["grid_index"],
            "slot": task["slot"], "x0_free": task["x0"], "x_free": task["x0"], "x": [0.9, 0.81, 0.31, 0.11], "value": value,
            "witness": "valid", "termination": "converged", "feasibility_class": "exact_feasible",
            "residuals": {"box": "0", "box_by_coord": ["0"] * 4, "g": "0", "eq": "0"}, "n_out_PE": 0, "n_out_NE": 0}


# ======================================================================== N1 — 중단 집계 (회신 §2)
def test_n1_a_a_wave_one_structural_stop_classifies_every_planned_unit_and_never_promotes_unfit(fake, arrays, monkeypatch):
    """[RED 실패 — ρ 미분류: `store["not_run"]` 에 rho|A0|2 없음] 검토자 반례 그대로 — 실제 stage_a + direct_runner · 첫 지역 실행의 등록 구조 중지
    (모르는 옵션 경고) → 1 STARTED_INTERRUPTED + 255 NOT_STARTED · ρ 실행 0 · NOT_RUN:RHO_PRECONDITION (사유에 중지 원문) · 계획 3 단위 · 384 실행이
    겹치지 않는 칸으로 다 들어간다 · UNFIT 0 (중단 · 미착수는 UNFIT 근거가 아니다)."""
    _fake_minimize(monkeypatch, warn=True, n_calls=1)
    store = hb.new_store()
    seen = []

    def runner(tasks, ctx, task_fn):
        seen.append((task_fn, len(tasks)))
        return hb.direct_runner(tasks, ctx, task_fn)
    with pytest.raises(hb.HStop) as ei:
        hb.stage_a(["J_V|A0|2", "J_D|A0|2", "rho|A0|2"], fake.ctx, runner, store, arrays)
    assert seen == [(h.run_phase_a, 256)]                                                # 1 파 한 번 · ρ 파 0
    stops = [e["reason"] for e in store["events"] if e["kind"] == "global_stop"]
    assert len(stops) == 1 and "OptimizeWarning" in stops[0] and stops[0] in str(ei.value)
    st = Counter(r["state"] for u in ("J_V|A0|2", "J_D|A0|2") for r in store["phase_a"][u])
    assert st == {"STARTED_INTERRUPTED": 1, "NOT_STARTED": 255}
    nr = store["not_run"].get("rho|A0|2") or {}
    assert nr.get("category") == "NOT_RUN:RHO_PRECONDITION" and stops[0] in nr["reason"] and "선행 미완" in nr["reason"]
    assert "rho|A0|2" not in store["phase_a"]
    a = hb.plan_counts(store)["phase_a"]
    assert (a["planned_units"], a["run_units"], a["not_run"], a["unaccounted_units"]) == (3, 2, {"NOT_RUN:RHO_PRECONDITION": 1}, [])
    assert a["unit_classes"] == {"완료": 0, "착수 뒤 중단": 1, "미착수": 1, "미완 (기타)": 0} and a["unfit_units"] == 0
    assert a["run_states"] == {"NOT_STARTED": 255, "STARTED_INTERRUPTED": 1} and a["executed_runs"] == 0
    assert (a["planned_runs"], a["row_count_mismatch"], a["not_run_runs"], a["unaccounted_runs"]) == (384, 0, 128, 0)
    assert a["planned_runs"] == sum(a["run_states"].values()) + a["row_count_mismatch"] + a["not_run_runs"] + a["unaccounted_runs"]
    assert a["global_stops"] == stops


def test_n1_b_a_rho_wave_stop_classifies_the_remaining_rho_units_without_running_them(fake, arrays):
    """[RED 실패 — 뒤 ρ 미분류: `store["not_run"]` 에 rho|A0|3 없음] 같은 결함의 ρ 파 변형 — 두 셀의 1 파는 완료 (만든 행 · 최적화 0) · 첫 ρ 파가
    전역 중지 → 뒤 셀의 ρ 는 실행 없이 NOT_RUN:RHO_PRECONDITION (사유에 중지 원문) · 중지된 ρ 의 행 · 완료 대조 기록 · 계획 6 단위 · 768 실행 분류."""
    stop = "단계 경계 — 합성 중지 (n1_b)"
    fab = _fab_pa_runner()
    calls = []

    def runner(tasks, ctx, task_fn):
        units = sorted({t["unit"] for t in tasks})
        calls.append(units)
        if units[0].startswith("rho|"):
            return {"states": [{"task_id": t["task_id"], "worker": 0, "state": "STARTED_INTERRUPTED" if i == 0 else "NOT_STARTED",
                                "interrupt_reason": stop} for i, t in enumerate(tasks)], "global_stop": stop}
        return fab(tasks, ctx, task_fn)
    store = hb.new_store()
    names = ["J_V|A0|2", "J_D|A0|2", "rho|A0|2", "J_V|A0|3", "J_D|A0|3", "rho|A0|3"]
    with pytest.raises(hb.HStop) as ei:
        hb.stage_a(names, fake.ctx, runner, store, arrays)
    assert calls == [["J_D|A0|2", "J_D|A0|3", "J_V|A0|2", "J_V|A0|3"], ["rho|A0|2"]] and stop in str(ei.value)
    nr = store["not_run"].get("rho|A0|3") or {}
    assert nr.get("category") == "NOT_RUN:RHO_PRECONDITION" and stop in nr["reason"] and "rho|A0|3" not in store["phase_a"]
    ev = [(e["kind"], e["key"]) for e in store["events"]]
    assert ("global_stop", "rho|A0|2") in ev and ("phase_a_incomplete", "rho|A0|2") in ev
    a = hb.plan_counts(store)["phase_a"]
    assert (a["planned_units"], a["run_units"], a["not_run"], a["unaccounted_units"]) == (6, 5, {"NOT_RUN:RHO_PRECONDITION": 1}, [])
    assert a["unit_classes"] == {"완료": 4, "착수 뒤 중단": 1, "미착수": 0, "미완 (기타)": 0} and a["unfit_units"] == 0
    assert a["run_states"] == {"COMPLETED": 512, "NOT_STARTED": 127, "STARTED_INTERRUPTED": 1}
    assert (a["planned_runs"], a["row_count_mismatch"], a["not_run_runs"], a["unaccounted_runs"]) == (768, 0, 128, 0)
    assert a["global_stops"] == [stop]


# ======================================================================== N2 — 저장 float 격자 중심 (회신 §3)
def test_n2_a_the_profile_center_and_order_follow_the_stored_float_grid(fake):
    """[RED 실패 — 중심 index 2 · 순서 [2, 1, 3, 0]] 검토자 반례 (CENTER_COUNTEREXAMPLE.json): A0 · #1 · m_P · x̂⁽⁰⁾ 의 m_P = float(0.61875) 는 저장
    float(0.6125) 와 0.625 의 정확한 가운데 → 동률 규칙 (작은 t) 으로 index 1 이 중심 · 순서 [1, 2, 0, 3] · s2 근거 = 안쪽 이웃 (중심은 Phase A 둘째).
    부분 격자 [0, 1, 2, 3] (원래 index · t 그대로) · 만든 행 (최적화 0)."""
    g = h.profile_grid("m_P", "A0", 1, MAX_Q)
    a, b, m = F(g["t"][1]), F(g["t"][2]), F(0.61875)
    assert (a, b) == (F(0.6125), F(5, 8)) and m - a == b - m == F(56294995342131, 9007199254740992)    # 반례의 정확 산술 그대로
    assert m - F(g["t_fraction"][1]) > b - m                                                             # 반올림 전 분수로는 index 2 가 더 가깝다
    store = hb.new_store()
    seen = []

    def runner(tasks, ctx, task_fn):
        seen.append(tasks[0]["grid_index"])
        return {"states": [dict(_fab_b_row(t, 0.1), state="COMPLETED") for t in tasks], "global_stop": None}
    ranked = [{"run_id": 5, "x": [0.61875, 0.75, 0.25, 0.125], "value": 0.01}, {"run_id": 9, "x": [0.9, 0.8, 0.3, 0.1], "value": 0.02}]
    rec = hb.run_profile_k(_unit("J_V|A0|1"), "m_P", fake.ctx, runner, store, arrays_dir=H_ARRAYS, seal_dir=fake.tmp / "seals_n2a",
                           ranked=ranked, grids=lambda unit, k: [0, 1, 2, 3])
    assert rec["center"] == 1 and rec["order"] == [1, 2, 0, 3] and seen == [1, 2, 0, 3]
    seal = {p["grid_index"]: json.loads(Path(p["seal"]["path"]).read_text(encoding="utf-8")) for p in rec["points"]}
    assert [gi for gi in range(4) if seal[gi]["is_center"]] == [1]
    assert seal[1]["starts"][1]["source"] == {"kind": "phase_a", "run_id": 9}
    assert [seal[gi]["starts"][1]["source"].get("grid_index") for gi in (2, 0, 3)] == [1, 1, 2]


# ======================================================================== N3 — 발견 폭의 근거 · 등급 · 부가 라벨 (회신 §4)
def _x_for(k, t):
    """h_k(x) ≈ t 인 점 (m_P · m_N 은 정확 · LII 는 d_P − d_N = 0.1 로 m_P 를 맞춤 — 오차 ~1e-16)."""
    if k == "m_P":
        return [float(t), 0.75, 0.3, 0.1]
    if k == "m_N":
        return [0.9, float(t), 0.3, 0.1]
    return [float(F(t) + F(1, 10) / MAX_Q), 0.9, 0.15, 0.05]


def _rec(unit, k, gi, t, value, *, box="0", termination="converged", n_out=0):
    row = {"task_id": 1000 + gi, "run_id": 0, "unit": unit, "stage": "profile", "k": k, "grid_index": gi, "t": float(t), "slot": "s1",
           "x": _x_for(k, t), "value": value, "witness": "valid", "termination": termination,
           "feasibility_class": "exact_feasible" if box == "0" else "numerically_accepted",
           "residuals": {"box": box, "box_by_coord": [box] * 4, "g": "0", "eq": "0"}, "n_out_PE": n_out, "n_out_NE": n_out}
    return {"status": "DONE", "rows": [row], "below_J0": False}


def _store_for(unit, spec):
    """합성 저장 기록 — spec[k] = [(grid_index, 값, 추가 인자)] (Phase B 프로파일 기록만 · 실행 0)."""
    row = _unit(unit)["row"]
    store = hb.new_store()
    for k, pts in spec.items():
        g = h.profile_grid(k, "A0", row, MAX_Q)
        for gi, value, kw in pts:
            store["phase_b"][hb._key(unit, "profile", k, gi)] = _rec(unit, k, gi, g["t"][gi], value, **kw)
    return store, (lambda u, k: [p[0] for p in spec[k]])


def test_n3_a_width_claims_carry_their_own_support_grades_and_side_labels_in_the_reading(fake):
    """[RED 실패 — 폭 결과에 grades · support · extra 없음] 최종 `_read_unit` 판독 — 경계 행 #0 (J_V A0) · 각 좌표의 격자 양 끝 (명목 ± 0.05 밖):
    m_P = 명목 양립 NOT_FOUND (extra 빈칸) + WIDE · 근거 증인 하나가 budget 종료 · 외삽 (n_out 2) · 목적 경계 (T − 1e-12) → 폭에 그 셋 /
    m_N = 수치 수용 증인에만 기대는 WIDE (수치 경계 의존) → 선형 제약 경계 · 등급 수 1 · 1 / LII = 경계 행 → 제약 절단."""
    T, unit = 0.05, "J_V|A0|0"
    last = {k: len(h.profile_grid(k, "A0", 0, MAX_Q)["t"]) - 1 for k in h.COORDS}
    spec = {"m_P": [(0, 0.01, {}), (last["m_P"], T - 1e-12, {"termination": "budget", "n_out": 2})],
            "m_N": [(0, 0.01, {}), (last["m_N"], 0.01, {"box": "1/100000000000000000"})],
            "LII": [(0, 0.01, {}), (last["LII"], 0.01, {})]}
    store, grids = _store_for(unit, spec)
    for k in h.COORDS:
        g = h.profile_grid(k, "A0", 0, MAX_Q)
        nom = F(hb.p0.NOMINAL[0][h.COORDS.index(k)])
        assert all(abs(F(g["t_fraction"][gi]) - nom) > F("0.05") for gi in (0, last[k]))           # 둘 다 명목 ± 0.05 밖
    r = hb._read_unit(store, _unit(unit), T, lambda p: p["value"], ctx=fake.ctx, grids=grids)
    assert all(r["compat_individual"]["m_P"][tau]["value"] == "NOT_FOUND" and r["compat_individual"]["m_P"][tau]["extra"] == []
               for tau in ("0", "0.02", "0.05"))
    for tau in ("0.02", "0.05"):
        wp, wn, wl = (r["width"][k][tau] for k in ("m_P", "m_N", "LII"))
        assert wp["value"] == "WIDE" and wp["unresolved"] is False
        assert wp.get("grades") == {"exact_feasible": 2, "numerically_accepted": 0}
        assert [s["grid_index"] for s in wp["support"]] == [0, last["m_P"]] and [s["grade"] for s in wp["support"]] == ["exact_feasible"] * 2
        assert [F(s["h_k"]) for s in wp["support"]] == [F(h.profile_grid("m_P", "A0", 0, MAX_Q)["t"][gi]) for gi in (0, last["m_P"])]
        assert wp["extra"] == ["budget 종료 증인", "경계 근접", "외삽 의존"]
        assert wn["value"] == "WIDE (수치 경계 의존)" and wn["unresolved"] is True
        assert wn["grades"] == {"exact_feasible": 1, "numerically_accepted": 1} and wn["extra"] == ["선형 제약 경계"]
        assert [s["grade"] for s in wn["support"]] == ["exact_feasible", "numerically_accepted"]
        assert wl["value"] == "WIDE" and wl["extra"] == ["제약 절단"] and wl["grades"] == {"exact_feasible": 2, "numerically_accepted": 0}


def test_n3_b_narrow_and_empty_widths_keep_the_basis_labels_and_the_boundary_row_cut(fake):
    """[RED 실패 — 폭 결과에 support · extra 없음] `_read_unit` · 붙은 격자점 [0, 1] (폭 ≤ 2τ): NARROW_FOUND 의 근거 = 고려한 증인 전부 (budget 하나 →
    budget 종료 증인) · 충족 증인 0 → observed None · support [] · 경계 행 #4 의 LII 폭에는 그래도 제약 절단 · 경계 행이 아닌 #1 의 LII 에는 없음."""
    T = 0.05
    spec = {"m_P": [(0, 0.01, {}), (1, 0.01, {"termination": "budget"})],
            "m_N": [(0, 0.5, {}), (1, 0.5, {})],
            "LII": [(0, 0.5, {}), (1, 0.5, {})]}
    out = {}
    for unit in ("J_V|A0|4", "J_V|A0|1"):
        store, grids = _store_for(unit, spec)
        out[unit] = hb._read_unit(store, _unit(unit), T, lambda p: p["value"], ctx=fake.ctx, grids=grids)["width"]
    w4 = out["J_V|A0|4"]
    for tau in ("0.02", "0.05"):
        assert w4["m_P"][tau]["value"] == "NARROW_FOUND" and w4["m_P"][tau]["unresolved"] is True
        assert [s["grid_index"] for s in w4["m_P"][tau].get("support", [])] == [0, 1]
        assert w4["m_P"][tau]["extra"] == ["budget 종료 증인"] and w4["m_P"][tau]["grades"] == {"exact_feasible": 2, "numerically_accepted": 0}
        assert w4["m_N"][tau]["observed"] is None and w4["m_N"][tau]["support"] == [] and w4["m_N"][tau]["extra"] == []
        assert w4["LII"][tau]["value"] == "NARROW_FOUND" and w4["LII"][tau]["support"] == [] and w4["LII"][tau]["extra"] == ["제약 절단"]
        assert out["J_V|A0|1"]["LII"][tau]["extra"] == []
