"""REIL C4-0b2 — Phase B (프로파일 · 동시 · 명목) · 적응적 시작점 봉인 · H4 대조 · 표지 · 연결부 · 읽기 전용 건조 (상태 문서 §55).

대조 목록은 범위 확인 요청 `docs/REIL_C4_0B2_CONFIRMATION_REQUEST_20261014.md` §4 의 39 그대로다 (시험 이름의 앞머리 = 목록 ID).
합성 입력 · 보존 util 사본 · P0 기록 · 봉인 배열 (읽기만) 만 쓴다. REIL xlsx · pkl · 노트북은 열지 않고 Sobol 을 새로 만들지 않는다.
새 대조는 `reil_c4_hb` 의 함수와 기존 `reil_c4_h.run_phase_a` 만 부른다 — RED (새 모듈 골격) 에서 b0_1 은 통과 (회귀 대조),
나머지는 골격 NotImplementedError 로 실패가 예상이다.
연결부 시험 (c_4–c_8 · r_1) 은 등록 격자의 부분집합 (원래 격자 index 와 t 를 그대로 둔 index 0 하나) 을 주입해 실행 수를 줄인다 —
격자 엔진은 p_* 가 실제 격자로 본다. 부분집합은 등록 · 실행 · 대조에 똑같이 쓰인다.
"""
import hashlib
import importlib.machinery
import importlib.util
import json
import math
import itertools
import shutil
import warnings
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_e3a as e3a
from scripts import reil_c4_h as h
from scripts import reil_c4_hb as hb
from scripts import reil_c4_monitor as mon

BMS = Path(__file__).resolve().parents[1]
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
UTIL_COPY = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "util_LFP.py.txt"
PHASE_A_ARRAYS = BMS / "reil_c4_arrays_20261013"
H_ARRAYS = BMS / "reil_c4_arrays_0b1_20261013"
H_MANIFEST = "d122117f4b9dc70988b8636be7f2de91fa8e285dfff7c5340dcebac2e1f24b33"
NEW_SEAL = BMS / "reil_c6_rebuild_20261013"
NEW_SEAL_MANIFEST = "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc"
F = Fraction
MAX_Q = F(json.loads(P0_RESULT.read_text(encoding="utf-8"))["max_q"]["fraction"])
X0 = [0.9, 0.8, 0.3, 0.1]
UNKNOWN = "Unknown solver options: not_a_cobyqa_option"
LIM = {"measure": 60.0, "grace": 3.0, "rss": 10 ** 12, "rss_gap": 5.0, "disk_new": 10 ** 12, "disk_free": 0, "disk_gap": 15.0}
SUB = lambda unit, k: [0]                                              # noqa: E731 — 등록 격자의 부분집합 (index 0) 주입
FAKE_IDENT = lambda **kw: {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}   # noqa: E731

FAKE_UTIL = '''
import numpy as np

MODE = {"kind": "ok", "calls": 0}
TARGET = np.array([0.9, 0.8, 0.3, 0.1])


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    q = np.linspace(-0.5, 5.0, 50)
    return q, q, q, q, q, q, q, q


def objective_fun(x, Model, halfcell):
    MODE["calls"] += 1
    if MODE["kind"] == "value_error":
        raise ValueError("fake util error")
    if MODE["kind"] == "nan":
        return np.array([0.0, float("nan"), 0.0, float("nan")])
    d = np.asarray(x, dtype=float) - TARGET
    return np.array([0.0, float(d @ d) + 1e-6, 0.0, float(np.abs(d).sum()) + 1e-6])
'''


def MODEL():
    return {"Q_exp_interp": np.linspace(0.0, 3.0, 100), "V_exp_interp": np.linspace(2.0, 3.6, 100), "dVdQ_exp_interp": np.full(100, 0.2)}


@pytest.fixture
def fake(tmp_path):
    """가짜 util 을 파일로 써서 경로로 로드한다 — 그 frame 이 util 로 분류되게 (보완 라운드 시험과 같은 방식)."""
    p = tmp_path / "fake_util_LFP_b2.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4b2_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    ctx = {"util": mod, "util_file": str(p.resolve()), "models": {r: MODEL() for r in range(11)}, "halfcell": [None] * 4,
           "options": dict(h.DRY_OPTIONS), "gates": {r: {"accepted": False} for r in range(11)}, "denominators": {},
           "max_q": MAX_Q, "sigma_v": {r: 0.01 for r in range(11)}}
    return SimpleNamespace(mod=mod, ctx=ctx, tmp=tmp_path)


_UTIL = {}
_SEALS = itertools.count()


def _util():
    """보존 util 사본 — H4 대조 시험 안에서 골격 함수를 먼저 부른 뒤에만 로드한다 (RED 의 util 호출 0)."""
    if "u" not in _UTIL:
        from scripts import reil_c5_pilot as c5
        mod, uf = c5.load_util(UTIL_COPY, c5.UTIL_COPY_SHA)
        _UTIL["u"] = SimpleNamespace(mod=mod, file=uf)
    return _UTIL["u"]


@pytest.fixture(scope="module")
def arrays():
    return h.load_phase_a_arrays(PHASE_A_ARRAYS)


def _fake_minimize(monkeypatch, *, warn=False, n_calls=2, status=0, success=True, message="fake status", after=None):
    """알려진 반환을 주는 가짜 minimize — warn 이면 scipy 와 같은 모르는 옵션 경고를 먼저 낸다 · 목적을 n_calls 번 부른 뒤 x0 를 돌려준다."""
    import scipy.optimize as so

    def fake_min(fun, x0, **kw):
        if warn:
            warnings.warn(UNKNOWN, so.OptimizeWarning)
        for _ in range(n_calls):
            fun(np.asarray(x0, dtype=float))
        if after is not None:
            after()
        return SimpleNamespace(x=np.asarray(x0, dtype=float), fun=0.5, status=status, success=success, message=message,
                               nfev=n_calls, nit=1)
    monkeypatch.setattr(so, "minimize", fake_min)


def _unit(name):
    return next(u for u in h.units() if u["unit"] == name)


def _btask(fake, stage, *, k="m_P", t=0.9, x0=None, key=None):
    """Phase B 지역 실행 작업 하나 — 시작 배열을 먼저 봉인하고 그 봉인을 작업에 결속한다."""
    unit = {"profile": "J_V|A0|3", "simultaneous": "J_V|A0|1", "nominal": "J_V|A0|1"}[stage]
    x0 = list(x0 if x0 is not None else {"profile": (0.7, 0.3, 0.05), "simultaneous": (1.0, 1.0, 0.4, 0.1), "nominal": (0.1,)}[stage])
    seal = hb.seal_starts(fake.tmp / "seals", key or f"b0|{stage}|{k}", {"starts": [{"slot": "s1"}], "array": [x0]})
    o, region, row = unit.split("|")
    return {"task_id": 0, "run_id": 0, "unit": unit, "objective": o, "region": region, "row": int(row), "seed": None, "stage": stage,
            "k": k if stage == "profile" else "-", "grid_index": 0 if stage == "profile" else "-", "t": t if stage == "profile" else None,
            "tau": "0.05" if stage == "simultaneous" else ("0" if stage == "nominal" else None), "slot": "s1", "x0": x0, "worker": 0,
            "seal": {"path": seal["path"], "sha256": seal["sha256"], "row": 0}}


def _full(task):
    z = task["x0"]
    if task["stage"] == "profile":
        return [task["t"]] + list(z)                                    # k = m_P
    if task["stage"] == "simultaneous":
        return list(z)
    return [1.0, 1.0, z[0] + float(MAX_Q * (F(1) - F("0.9"))), z[0]]   # 명목 (#1 · m_P · m_N = 1 · Δ* = max_q (m_P* − LII*))


def _fab_pa_runner(valid=lambda unit: True, value=lambda unit, run_id: 0.1 + 0.001 * run_id):
    """Phase A 작업을 돌리지 않고 완료 행을 만드는 실행기 — 연결부 대조용 (최적화 · 목적 호출 0)."""
    def runner(tasks, ctx, task_fn):
        assert task_fn is h.run_phase_a
        states = []
        for t in tasks:
            x, ok, v = list(t["x0"]), valid(t["unit"]), value(t["unit"], t["run_id"])
            states.append({"task_id": t["task_id"], "run_id": t["run_id"], "unit": t["unit"], "objective": t["objective"],
                           "region": t["region"], "row": t["row"], "seed": t["seed"], "x0": x, "x": x,
                           "value": v if ok else float("nan"), "witness": "valid" if ok else "invalid:NONFINITE",
                           "termination": "converged", "components": {"J_V": v, "J_D": v} if t["objective"] == "rho" else None,
                           "residuals": {"box": "0", "box_by_coord": ["0"] * 4, "g": None if t["region"] == "A2" else "0"},
                           "feasibility_class": "exact_feasible", "n_out_PE": 0, "n_out_NE": 0, "state": "COMPLETED"})
        return {"states": states, "global_stop": None}
    return runner


def _fab_b_row(task, value):
    """Phase B 작업의 완료 행을 만든다 (격자 엔진 대조용 · 최적화 0) — x 는 시작과 다른 고정점 (중복 대체가 끼지 않게)."""
    return {"task_id": task["task_id"], "unit": task["unit"], "stage": task["stage"], "k": task["k"], "grid_index": task["grid_index"],
            "slot": task["slot"], "x0_free": task["x0"], "x_free": task["x0"], "x": [0.9, 0.81, 0.31, 0.11], "value": value,
            "witness": "valid", "termination": "converged", "feasibility_class": "exact_feasible",
            "residuals": {"box": "0", "box_by_coord": ["0"] * 4, "g": "0", "eq": "0"}, "n_out_PE": 0, "n_out_NE": 0}


def _store_ready(fake, arrays, monkeypatch, cell=0, region="A1"):
    """(셀 · 영역) 의 Phase A (만든 완료 행) → Phase B 등록 탐색 전부 (가짜 minimize · 부분 격자) — 공통 갱신 전 상태."""
    _fake_minimize(monkeypatch, n_calls=1)
    store = hb.new_store()
    names = [u["unit"] for u in h.units() if u["row"] == cell and u["region"] == region]
    hb.stage_a(names, fake.ctx, _fab_pa_runner(), store, arrays)
    hb.run_searches(cell, region, fake.ctx, hb.direct_runner, store, arrays=arrays, arrays_dir=H_ARRAYS,
                    seal_dir=fake.tmp / f"seals_{cell}_{region}_{next(_SEALS)}", grids=SUB)
    return store


W = [{"run_id": 7, "x": [0.9, 0.8, 0.3, 0.1]}, {"run_id": 3, "x": [0.85, 0.75, 0.25, 0.1]}, {"run_id": 9, "x": [0.8, 0.7, 0.2, 0.05]}]
SOB2 = np.array([[0.6, 0.1, 0.2], [0.7, 0.2, 0.3]])
SOB16 = np.array([[0.96 + 0.005 * i, 0.97, 0.3, 0.2] for i in range(16)])


# ======================================================================== b0 — 지역 실행기 일반화 (reil_c4_h.py)
OPTS = {k: repr(v) for k, v in sorted(h.DRY_OPTIONS.items())}
BASE = {"task_id": 0, "run_id": 0, "unit": "J_V|A0|3", "objective": "J_V", "region": "A0", "row": 3, "seed": 0, "x0": X0, "worker": 0,
        "options_received": OPTS}
RET = {"x": X0, "fun": 0.5, "status": 0, "message": "fake status", "nfev": 2, "nit": 1, "termination": "converged", "error": None}
TIMES = ("t_start", "t_end", "wall", "cpu")


def _a_task():
    return {"task_id": 0, "run_id": 0, "unit": "J_V|A0|3", "objective": "J_V", "region": "A0", "row": 3, "seed": 0, "start_index": 0,
            "x0": list(X0), "worker": 0}


def test_b0_1_phase_a_rows_are_unchanged_by_the_generalization(fake, monkeypatch):
    """[RED 통과 — 회귀 대조 · 기준 행은 가짜 정의에서 손으로 적었다] 정상 · util 오류 · 경고 + 반환의 Phase A 행 / partial 전체 (시각 필드 제외)."""
    _fake_minimize(monkeypatch, n_calls=2)
    row = h.run_phase_a(_a_task(), fake.ctx)
    want = {**BASE, "n_eval": 2, "n_nonfinite": 0, "warnings": [], **RET, "value": float(np.sqrt(1e-6)), "components": None,
            "reeval_error": None, "witness": "valid", "feasibility_class": "exact_feasible",
            "residuals": {"box": "0", "box_by_coord": ["0", "0", "0", "0"], "g": "0"}, "active": {"bounds": [], "g": False},
            "n_out_PE": 0, "n_out_NE": 0, "state": "COMPLETED"}
    assert {k: v for k, v in row.items() if k not in TIMES} == want
    fake.mod.MODE["kind"] = "value_error"
    row = h.run_phase_a(_a_task(), fake.ctx)
    err = row.pop("error")
    assert {k: v for k, v in err.items() if k != "traceback"} == {"kind": "local", "origin": "util", "stage": "optimize",
                                                                  "type": "ValueError", "message": "fake util error"}
    nulls = dict.fromkeys(("x", "fun", "status", "message", "nfev", "nit", "value", "components", "reeval_error", "residuals",
                           "feasibility_class", "active", "n_out_PE", "n_out_NE"))
    assert {k: v for k, v in row.items() if k not in TIMES} == {**BASE, "n_eval": 1, "n_nonfinite": 0, "warnings": [], **nulls,
                                                                 "termination": "solver_error", "witness": "invalid:SOLVER_ERROR",
                                                                 "state": "COMPLETED"}
    fake.mod.MODE["kind"] = "ok"
    _fake_minimize(monkeypatch, warn=True, n_calls=2)
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_a_task(), fake.ctx)
    msg = f"OptimizeWarning: {UNKNOWN}"
    stop = {"kind": "structural", "origin": "optimizer", "stage": "optimize", "type": "OptimizeWarning",
            "message": "알 수 없는 옵션 경고 — fail-closed (부속 A §3-1)", "traceback": [msg]}
    part = {k: v for k, v in ei.value.partial.items() if k != "t_start"}
    assert part == {**BASE, "n_eval": 2, "n_nonfinite": 0, "warnings": [msg], **RET, "stop_error": stop}


@pytest.mark.parametrize("stage", ["profile", "simultaneous", "nominal"])
def test_b0_2_the_option_warning_stop_keeps_the_return_fields_in_every_phase_b_problem(fake, monkeypatch, stage):
    """[RED 골격 실패] 모르는 옵션 경고 + 정상 반환 → OptimizeWarning 구조 중지 · partial 에 반환점 (자유 · 완전) · status · termination · 계수 · 경고."""
    task = _btask(fake, stage)
    _fake_minimize(monkeypatch, warn=True, n_calls=2)
    with pytest.raises(mon.Structural) as ei:
        hb.run_phase_b(task, fake.ctx)
    part = ei.value.partial or {}
    assert ei.value.info["type"] == "OptimizeWarning" and (part.get("stop_error") or {}).get("type") == "OptimizeWarning"
    assert part["x_free"] == task["x0"] and part["x"] == _full(task)
    assert (part["status"], part["termination"], part["n_eval"]) == (0, "converged", 2)
    assert any(UNKNOWN in w for w in part["warnings"]) and "witness" not in part and "value" not in part


def test_b0_3_an_unclassified_termination_stops_everything_in_phase_b(fake, monkeypatch):
    """[RED 골격 실패] 미분류 termination → 전체 중지 · 원 status / message · 재평가 0."""
    task = _btask(fake, "profile")
    _fake_minimize(monkeypatch, n_calls=1, status=99, success=False, message="odd status")
    with pytest.raises(mon.Structural) as ei:
        hb.run_phase_b(task, fake.ctx)
    part = ei.value.partial or {}
    assert ei.value.info["type"] == "UnclassifiedTermination"
    assert (part["status"], part["message"], part["termination"]) == (99, "odd status", "unclassified")
    assert fake.mod.MODE["calls"] == 1 and "value" not in part


def test_b0_4_phase_b_local_errors_are_rows_and_our_errors_are_structural(fake, monkeypatch):
    """[RED 골격 실패] 최적화 중 util 예외 → SOLVER_ERROR (반환 필드 없음) · 재평가 util 예외 → REEVAL_ERROR · NaN → NONFINITE · 우리 코드 → 구조."""
    fake.mod.MODE["kind"] = "value_error"
    _fake_minimize(monkeypatch, n_calls=1)
    row = hb.run_phase_b(_btask(fake, "profile", key="b0_4_solver"), fake.ctx)
    assert (row["termination"], row["witness"], row["x"], row.get("x_free")) == ("solver_error", "invalid:SOLVER_ERROR", None, None)
    assert row["error"]["origin"] == "util" and row["error"]["stage"] == "optimize"
    fake.mod.MODE["kind"] = "ok"
    _fake_minimize(monkeypatch, n_calls=1, after=lambda: fake.mod.MODE.update(kind="value_error"))
    row = hb.run_phase_b(_btask(fake, "profile", key="b0_4_reeval"), fake.ctx)
    assert row["witness"] == "invalid:REEVAL_ERROR" and row["termination"] == "converged" and row["reeval_error"]["origin"] == "util"
    fake.mod.MODE["kind"] = "nan"
    _fake_minimize(monkeypatch, n_calls=1)
    row = hb.run_phase_b(_btask(fake, "profile", key="b0_4_nan"), fake.ctx)
    assert row["witness"] == "invalid:NONFINITE" and row["n_nonfinite"] == 1
    fake.mod.MODE["kind"] = "ok"
    monkeypatch.setattr(hb, "residuals_b", lambda *a, **kw: 1 / 0)
    with pytest.raises(mon.Structural) as ei:
        hb.run_phase_b(_btask(fake, "profile", key="b0_4_ours"), fake.ctx)
    assert ei.value.info["type"] == "ZeroDivisionError" and ei.value.info["origin"] == "ours"


def test_b0_5_phase_b_rows_record_the_free_and_full_point_and_the_extra_residuals(fake, monkeypatch):
    """[RED 골격 실패] 자유 변수 반환 → 완전 x · 증인은 완전 x 그대로 · 등식 잔차는 기록 (등급 아님) · τ 상자 밖은 수용 실패 (등급은 영역 A)."""
    task = _btask(fake, "profile", k="LII", t=0.95, x0=(1.0, 0.9, 0.3), key="b0_5_lii")
    _fake_minimize(monkeypatch, n_calls=1)
    row = hb.run_phase_b(task, fake.ctx)
    dn = 0.3 - float(MAX_Q) * (1.0 - 0.95)
    assert row["x_free"] == [1.0, 0.9, 0.3] and row["x"] == [1.0, 0.9, 0.3, dn]
    assert row["witness"] == "valid" and row["feasibility_class"] == "exact_feasible"
    assert F(row["residuals"]["eq"]) <= F("1e-10") and row["start_seal_sha256"] == task["seal"]["sha256"]
    sim = _btask(fake, "simultaneous", x0=(1.0, 1.0, 0.3, 0.2), key="b0_5_sim")   # LII = 1 − 0.1/max_q ≈ 0.968 > 0.95 (τ 상자 밖)
    row = hb.run_phase_b(sim, fake.ctx)
    assert row["witness"] == "invalid:INFEASIBLE_RETURN" and row["feasibility_class"] == "exact_feasible"
    assert F(row["residuals"]["tau"]) > F("1e-10") and len(row["residuals"]["tau_by_coord"]) == 3


# ======================================================================== p — 프로파일 (부속 A §3-3 · B §2-1 · §2-2)
def test_p_1_profile_order_is_the_center_then_outward_by_distance_and_t():
    """[RED 골격 실패] 중심 = 최근접 (동률 작은 t) · (거리, t) 오름차순 · 등록 점마다 한 번 (숨은 추가 sweep 0)."""
    ts = [F(0), F(1, 10), F(2, 10), F(3, 10), F(5, 10)]
    assert hb.profile_order(ts, F(24, 100)) == [2, 1, 3, 0, 4]
    assert hb.profile_order(ts, F(25, 100)) == [2, 1, 3, 0, 4]
    assert hb.profile_order(ts, F(-1)) == [0, 1, 2, 3, 4] and hb.profile_order(ts, F(9, 10))[0] == 4
    assert (hb.inner_neighbor(3, 2), hb.inner_neighbor(0, 2), hb.inner_neighbor(2, 2)) == (2, 1, None)
    g = h.profile_grid("m_P", "A0", 3, MAX_Q)
    order = hb.profile_order([F(t) for t in g["t"]], F("0.64"))
    assert sorted(order) == list(range(len(g["t"])))


@pytest.mark.parametrize("k,t,x0", [("m_P", 0.9, (0.7, 0.3, 0.05)), ("m_N", 0.8, (0.7, 0.3, 0.05)), ("LII", 0.8365, (0.9, 0.7, 0.35))])
def test_p_2_elimination_rebuilds_the_full_point_and_moves_g_and_the_d_n_box(fake, k, t, x0):
    """[RED 골격 실패] 소거 셋: 완전 x 복원 · LII 에서 G → m_P ≥ t + 1e-4/max_q · d_N 상자 → 선형 제약 · 실제 COBYQA 1 회."""
    task = _btask(fake, "profile", k=k, t=t, x0=x0, key=f"p_2_{k}")
    prob = hb.profile_problem(task, fake.ctx)
    q = float(MAX_Q)
    want = {"m_P": [t, 0.75, 0.25, 0.04], "m_N": [0.75, t, 0.25, 0.04], "LII": [0.75, 0.25, 0.04, 0.04 - q * (0.75 - t)]}[k]
    assert [float(v) for v in prob["full"](np.array([0.75, 0.25, 0.04]))] == want and len(prob["lo"]) == 3
    rows = [(list(a[0]), lb, ub) for a, lb, ub in prob["cons"]]
    if k == "LII":
        assert ([-q, 0.0, 1.0], 0.0 - q * t, 1.0 - q * t) in rows and ([1.0, 0.0, 0.0], t + float(F("1e-4") / MAX_Q), math.inf) in rows
    else:
        assert rows == [([0.0, 1.0, -1.0], 1e-4, math.inf)]
    row = hb.run_phase_b(task, fake.ctx)
    assert row["termination"] in ("converged", "budget") and row["x"] == [float(v) for v in prob["full"](np.array(row["x_free"]))]
    assert row["witness"] == "valid" and F(row["residuals"]["eq"]) <= F("1e-10")


def test_p_3_profile_starts_follow_the_registered_chain_duplicates_and_shortages():
    """[RED 골격 실패] s1 · s2 사슬 (안쪽 이웃 → 안쪽으로 걷기 → Phase A 둘째 → 시작 부족 (s2)) · 중복 → 다음 대체 → 시작 부족 (중복)."""
    kw = dict(k="m_P", region="A0", t=0.9, max_q=MAX_Q, sobol2=SOB2)
    a = hb.profile_starts(ranked=W, inner=[{"grid_index": 5, "witness": {"run_id": 2, "x": [0.95, 0.6, 0.3, 0.2]}}], is_center=False, **kw)
    assert [s["slot"] for s in a["starts"]] == ["s1", "s2", "s3", "s4"] and a["shortages"] == []
    assert a["starts"][0]["x_free"] == [0.8, 0.3, 0.1] and a["starts"][1]["x_free"] == [0.6, 0.3, 0.2]
    assert a["starts"][0]["source"] == {"kind": "phase_a", "run_id": 7} and a["starts"][1]["source"] == {"kind": "grid", "grid_index": 5, "run_id": 2}
    assert [s["x_free"] for s in a["starts"][2:]] == SOB2.tolist() and a["array"] == [s["x_free"] for s in a["starts"]]
    b = hb.profile_starts(ranked=W, inner=[{"grid_index": 5, "witness": None},
                                           {"grid_index": 6, "witness": {"run_id": 4, "x": [0.9, 0.55, 0.35, 0.15]}}], is_center=False, **kw)
    assert b["starts"][1]["source"] == {"kind": "grid", "grid_index": 6, "run_id": 4}
    c = hb.profile_starts(ranked=W, inner=[], is_center=True, **kw)
    assert c["starts"][1]["source"] == {"kind": "phase_a", "run_id": 3} and c["starts"][1]["x_free"] == [0.75, 0.25, 0.1]
    d = hb.profile_starts(ranked=W[:1], inner=[], is_center=True, **kw)
    assert [s["slot"] for s in d["starts"]] == ["s1", "s3", "s4"] and d["shortages"] == ["시작 부족 (s2)"]
    dup = [{"grid_index": 5, "witness": {"run_id": 2, "x": [0.95, 0.8, 0.3, 0.1]}}]     # 자유 좌표가 s1 과 같다
    e = hb.profile_starts(ranked=W, inner=dup, is_center=False, **kw)
    assert e["starts"][1]["source"] == {"kind": "phase_a", "run_id": 3}
    assert e["starts"][1]["replaced"] == [{"kind": "grid", "grid_index": 5, "run_id": 2}]
    f = hb.profile_starts(ranked=W[:1], inner=dup, is_center=False, **kw)
    assert [s["slot"] for s in f["starts"]] == ["s1", "s3", "s4"] and f["shortages"] == ["시작 부족 (중복)"]


def test_p_4_sobol_starts_come_from_the_sealed_block_and_a_changed_block_is_refused(tmp_path):
    """[RED 골격 실패] s3 · s4 = 봉인 Sobol 2 (label · INDEX 행 범위 · raw sha 대조) — 봉인과 다른 블록은 거부."""
    lab = h.label(3, "A0", "J_V", "profile", k="m_P", grid_index=0)
    blk, ent = hb.sealed_block(H_ARRAYS, lab)
    assert blk.shape == (2, 3) and hashlib.sha256(np.ascontiguousarray(blk, dtype="<f8").tobytes()).hexdigest() == ent["raw_sha256"]
    assert ent["label"] == lab and ent["grid_index"] == 0
    d = tmp_path / "copy"
    (d / "profile").mkdir(parents=True)
    shutil.copy(H_ARRAYS / "INDEX.json", d / "INDEX.json")
    a = np.load(H_ARRAYS / ent["file"], allow_pickle=False).copy()
    a[ent["rows"][0], 0] += 1e-9
    np.save(d / ent["file"], a, allow_pickle=False)
    with pytest.raises(hb.HStop):
        hb.sealed_block(d, lab)


def test_p_5_rounding_clips_are_for_starts_only_and_recorded():
    """[RED 골격 실패] bounds 를 반올림만큼 넘은 증인 좌표는 시작점 구성에서만 자르고 기록한다 — 증인 기록은 그대로."""
    w = [{"run_id": 1, "x": [0.9, 0.8, 0.5 + 1e-13, 0.1]}, {"run_id": 2, "x": [0.8, 0.7, 0.2, 0.05]}]
    orig = [list(v["x"]) for v in w]
    s = hb.profile_starts(ranked=w, inner=[], is_center=True, k="m_P", region="A0", t=0.9, max_q=MAX_Q, sobol2=SOB2)
    assert s["starts"][0]["x_free"] == [0.8, 0.5, 0.1] and s["starts"][0]["clip"] == [{"coord": "d_P", "from": 0.5 + 1e-13, "to": 0.5}]
    assert [v["x"] for v in w] == orig and s["starts"][1]["clip"] == []


def test_p_6_a_grid_point_is_the_valid_minimum_and_unevaluated_points_never_run(fake):
    """[RED 골격 실패] 격자점 값 = 유효 최소 · 넷 다 무효 → 실패 · 미평가 (영역 밖 · 중복) 실행 0 · J < Ĵ⁽⁰⁾ 표시 (실행은 만든 행 — 최적화 0)."""
    rows = [{"witness": "valid", "value": 0.3, "slot": "s1"}, {"witness": "invalid:NONFINITE", "value": float("nan"), "slot": "s2"},
            {"witness": "valid", "value": 0.2, "slot": "s3"}, {"witness": "invalid:SOLVER_ERROR", "value": None, "slot": "s4"}]
    v = hb.grid_point_value(rows)
    assert (v["value"], v["witness_slot"], v["n_valid"], v["search"]) == (0.2, "s3", 2, "OK")
    assert hb.grid_point_value([dict(r, witness="invalid:NONFINITE") for r in rows])["search"] == "실패"
    store = hb.new_store()
    seen = []

    def runner(tasks, ctx, task_fn):
        seen.extend(tasks)
        return {"states": [dict(_fab_b_row(t, 0.5 if t["grid_index"] % 2 else 0.0005), state="COMPLETED") for t in tasks],
                "global_stop": None}
    g = h.profile_grid("m_P", "A0", 3, MAX_Q)
    assert g["skipped"]
    rec = hb.run_profile_k(_unit("J_V|A0|3"), "m_P", fake.ctx, runner, store, arrays_dir=H_ARRAYS, seal_dir=fake.tmp / "seals_p6",
                           ranked=W, J0=0.001)
    assert len(rec["points"]) == len(g["t"]) and len(seen) == 4 * len(g["t"])
    assert {t["grid_index"] for t in seen} == set(range(len(g["t"]))) and rec["skipped"] == g["skipped"]
    assert all(p["search"] == "OK" for p in rec["points"])
    assert [p["below_J0"] for p in rec["points"]] == [p["value"] < 0.001 for p in rec["points"]]


def test_p_7_adaptive_starts_are_sealed_before_the_run_and_cannot_be_rewritten(fake, monkeypatch):
    """[RED 골격 실패] 실행 직전 봉인 (근거 run · 증인 · 변환) · 실행 행에 시작 배열 sha · 같은 격자점 재봉인 · 봉인 위조 거부."""
    store = hb.new_store()
    seals = fake.tmp / "seals_p7"

    def runner(tasks, ctx, task_fn):
        for t in tasks:
            got = hb.verify_seal(t["seal"])                              # 실행 직전 — 봉인이 이미 있다
            assert got["array"][t["seal"]["row"]] == t["x0"]
        return {"states": [dict(_fab_b_row(t, 0.1), state="COMPLETED") for t in tasks], "global_stop": None}
    unit = _unit("J_V|A0|3")
    pt = hb.profile_point(unit, "m_P", 0, fake.ctx, runner, store, arrays_dir=H_ARRAYS, seal_dir=seals, ranked=W, inner=[], is_center=True)
    rec = json.loads(Path(pt["seal"]["path"]).read_text(encoding="utf-8"))
    assert rec["starts"][0]["source"] == {"kind": "phase_a", "run_id": 7} and rec["start_array_sha256"] == pt["seal"]["start_array_sha256"]
    assert rec["starts"][2]["source"]["label"] == h.label(3, "A0", "J_V", "profile", k="m_P", grid_index=0)
    with pytest.raises(hb.HStop):
        hb.profile_point(unit, "m_P", 0, fake.ctx, runner, store, arrays_dir=H_ARRAYS, seal_dir=seals, ranked=W, inner=[], is_center=True)
    task = dict(pt["tasks"][0])
    _fake_minimize(monkeypatch, n_calls=1)
    row = hb.run_phase_b(task, fake.ctx)
    assert row["start_seal_sha256"] == pt["seal"]["sha256"] and row["start_array_sha256"] == pt["seal"]["start_array_sha256"]
    Path(pt["seal"]["path"]).write_bytes(Path(pt["seal"]["path"]).read_bytes() + b" ")
    with pytest.raises(mon.Structural):
        hb.run_phase_b(dict(task, task_id=1), fake.ctx)


# ======================================================================== s — 동시 양립 (부속 A §3-4 · B §2-3 · §1-3)
def test_s_1_simultaneous_starts_are_the_top_four_clipped_plus_the_first_twelve_sobol():
    """[RED 골격 실패] 시작 16 = 상위 min(4, n_valid) (P · N 으로 자름 · d 그대로) + 봉인 Sobol 앞 12 · 뒤 4 는 쓰지 않는다."""
    w = [{"run_id": i, "x": [0.9 - 0.01 * i, 0.8, 0.3, 0.1 + 0.01 * i]} for i in range(6)]
    s = hb.sim_starts(row=1, region="A0", tau="0.05", max_q=MAX_Q, ranked=w, sobol16=SOB16)
    xs = [st["x"] for st in s["starts"]]
    assert len(xs) == 16 and s["shortages"] == [] and xs[4:] == SOB16[:12].tolist()
    assert xs[:4] == [[0.95, 0.95, 0.3, 0.1 + 0.01 * i] for i in range(4)]
    assert all(r not in xs for r in SOB16[12:].tolist())
    assert [st["source"] for st in s["starts"][:4]] == [{"kind": "phase_a", "run_id": i} for i in range(4)]


def test_s_2_simultaneous_shortage_and_duplicates_after_clipping_are_recorded():
    """[RED 골격 실패] n_valid < 4 → 시작 부족 (Phase A 증인) · 자른 뒤 같은 좌표 → 다음 순위 → 시작 부족 (중복) · 복제 · 추가 추출 0."""
    w = [{"run_id": 0, "x": [0.9, 0.8, 0.3, 0.1]}, {"run_id": 1, "x": [0.92, 0.85, 0.3, 0.1]}]
    s = hb.sim_starts(row=1, region="A0", tau="0.05", max_q=MAX_Q, ranked=w, sobol16=SOB16)
    assert len(s["starts"]) == 13 and s["shortages"] == ["시작 부족 (Phase A 증인) 2", "시작 부족 (중복)"]
    w3 = w + [{"run_id": 2, "x": [0.8, 0.7, 0.25, 0.1]}]
    s3 = hb.sim_starts(row=1, region="A0", tau="0.05", max_q=MAX_Q, ranked=w3, sobol16=SOB16)
    assert [st["source"]["run_id"] for st in s3["starts"][:2]] == [0, 2]
    assert s3["shortages"] == ["시작 부족 (Phase A 증인) 1", "시작 부족 (중복)"] and len(s3["starts"]) == 14


def test_s_3_the_simultaneous_problem_has_the_box_g_and_both_lii_faces(fake):
    """[RED 골격 실패] 상자 = sim_box · 선형 제약 = G · LII ∈ I 두 면 · τ 상자 잔차 · 실제 COBYQA 1 회."""
    task = _btask(fake, "simultaneous", key="s_3")
    prob = hb.sim_problem(task, fake.ctx)
    sb = h.sim_box(1, "A0", "0.05", MAX_Q)
    q = float(MAX_Q)
    assert prob["lo"] == [float(v) for v in sb[0]] and prob["hi"] == [float(v) for v in sb[1]]
    rows = [(list(a[0]), lb, ub) for a, lb, ub in prob["cons"]]
    assert ([1.0, 0.0, -1.0 / q, 1.0 / q], float(F("0.85")), float(F("0.95"))) in rows and ([0.0, 0.0, 1.0, -1.0], 1e-4, math.inf) in rows
    row = hb.run_phase_b(task, fake.ctx)
    assert row["termination"] in ("converged", "budget") and row["witness"] == "valid" and F(row["residuals"]["tau"]) <= F("1e-10")


def test_s_4_prior_incompatible_runs_nothing_and_other_points_never_become_simultaneous_witnesses(fake):
    """[RED 골격 실패] PRIOR_INCOMPATIBLE → 실행 0 · 다른 탐색의 반환점이 그 τ 상자에 있어도 동시 증인 0 (B §1-3 P0 불변)."""
    store = hb.new_store()

    def runner(tasks, ctx, task_fn):
        raise AssertionError("PRIOR_INCOMPATIBLE 인데 실행했다")
    rec = hb.run_simultaneous(_unit("J_V|A0|3"), "0.05", fake.ctx, runner, store, arrays_dir=H_ARRAYS, seal_dir=fake.tmp / "s4", ranked=W)
    assert rec["status"] == "NOT_RUN" and rec["category"] == "NOT_RUN:PRIOR_INCOMPATIBLE"
    pt = {"witness": "valid", "value": 0.0, "x": [0.64, 1.0, 0.3, 0.3], "residuals": {"box": "0", "box_by_coord": ["0"] * 4, "g": "0"},
          "termination": "converged", "n_out_PE": 0, "n_out_NE": 0}
    lab = hb.compat_simultaneous([pt], "0.05", 1.0, row=3, region="A0", max_q=MAX_Q)
    assert lab["value"] == "PRIOR_INCOMPATIBLE" and lab["grades"] == {"exact_feasible": 0, "numerically_accepted": 0}


# ======================================================================== n — 명목점 정확 대조 (부속 A §3-5)
def test_n_1_the_nominal_interval_and_201_points_are_exact_and_each_point_is_evaluated(fake):
    """[RED 골격 실패] Δ* (정확) · d_N 구간 · 201 점 (양 끝 포함) · 격자점마다 독립 평가 · 잔차."""
    iv = hb.nominal_interval(1, "A0", MAX_Q)
    delta = MAX_Q * (F(1) - F("0.9"))
    assert iv["delta"] == delta and iv["lo"] == max(F(0), F("0.005") - delta) and iv["hi"] == min(F(1), F("0.5") - delta)
    g = hb.nominal_grid(iv)
    assert len(g) == 201 and g[0] == iv["lo"] and g[-1] == iv["hi"] and g[1] - g[0] == (iv["hi"] - iv["lo"]) / 200
    task = {"task_id": 0, "run_id": 0, "unit": "J_V|A0|1", "objective": "J_V", "region": "A0", "row": 1, "seed": None,
            "stage": "nominal_grid", "worker": 0}
    pts = hb.run_nominal_grid(task, fake.ctx)["grid"]
    assert len(pts) == 201 and fake.mod.MODE["calls"] == 201 and all(p["witness"] == "valid" for p in pts)
    assert pts[0]["x"] == [1.0, 1.0, float(g[0]) + float(delta), float(g[0])]
    assert all(F(p["residuals"]["tau"]) <= F("1e-10") for p in pts)


def test_n_2_the_lowest_grid_point_is_refined_once_and_the_smaller_valid_value_wins(fake):
    """[RED 골격 실패] 최저 격자점 (같으면 작은 d_N) 에서 1 변수 COBYQA 1 회 (실제) · 둘 중 유효 최소 · PRIOR_INCOMPATIBLE 이면 0."""
    store = hb.new_store()
    calls = []

    def runner(tasks, ctx, task_fn):
        calls.append([t["stage"] for t in tasks])
        return hb.direct_runner(tasks, ctx, task_fn)
    rec = hb.run_nominal_stage(_unit("J_V|A0|1"), fake.ctx, runner, store, seal_dir=fake.tmp / "n2")
    assert calls == [["nominal_grid"], ["nominal"]]
    best = min((p["value"], F(p["d_N"])) for p in rec["grid"] if p["witness"] == "valid")
    assert (rec["start"]["value"], F(rec["start"]["d_N"])) == best and rec["refine"]["x0_free"] == [float(best[1])]
    cands = [(best[0], "grid")] + ([(rec["refine"]["value"], "refine")] if rec["refine"]["witness"] == "valid" else [])
    win = min(cands, key=lambda c: (c[0], c[1] != "grid"))
    assert (rec["best"]["source"], rec["best"]["value"]) == (win[1], win[0])

    def no_runner(tasks, ctx, task_fn):
        raise AssertionError("τ = 0 PRIOR_INCOMPATIBLE 인데 실행했다")
    nr = hb.run_nominal_stage(_unit("J_V|A0|0"), fake.ctx, no_runner, store, seal_dir=fake.tmp / "n2b")
    assert nr["status"] == "NOT_RUN" and nr["category"] == "NOT_RUN:PRIOR_INCOMPATIBLE"


# ======================================================================== h — H4 대조 (부속 A §4-4 · §4-5 · B §4)
def _h4_inputs(util_mod):
    """양성 대조를 지날 수 있는 합성 입력 — 반쪽전지 q 범위 3.3 · 4.0 · 실험 Q 2.5 (R1 의 세 점 모두 n_out 0 이 되는 격자)."""
    q_pe = np.linspace(0.0, 3.3, 400)
    v_pe = 3.2 + 0.2 * q_pe / 3.3 + 0.2 * (1.0 + np.tanh(10.0 * (q_pe - 3.15)))
    q_ne = np.linspace(0.0, 4.0, 400)
    v_ne = 0.05 + 1.5 * np.exp(-3.0 * q_ne)
    q = np.linspace(0.0, 2.5, 300)
    model = util_mod.extract_battery_data([np.vstack([q, 2.0 + 1.6 * (q / 2.5) ** 2])], 0)
    return model, [q_pe, v_pe, q_ne, v_ne]


def test_h_1_the_positive_control_takes_the_first_valid_candidate_and_checks_symmetry():
    """[RED 골격 실패] R1 → R2 → R3 · x · 0.9x · 1.1x 모두 유효 (n_out 0 · 교차 · span > 0) 인 첫 후보 · |ΔJ_V^s| ≤ 1e-9."""
    assert [c["name"] for c in hb.h4_candidates()] == ["R1", "R2", "R3"]
    util = _util()
    model, halfcell = _h4_inputs(util.mod)
    gate = h.endpoint_gate(float(model["V_exp_interp"][0]), float(model["V_exp_interp"][-1]))
    r = hb.h4_positive(util.mod, model, halfcell, gate)
    assert gate["accepted"] and r["status"] == "PASS" and r["candidate"] == "R1"
    assert all(abs(r["values"][c] - r["values"]["1"]) <= 1e-9 for c in ("0.9", "1.1"))
    assert all(p["n_out_PE"] == 0 and p["n_out_NE"] == 0 for p in r["points"].values())


def test_h_2_a_symmetry_failure_rejects_the_h4_implementation_for_every_cell():
    """[RED 골격 실패] 대칭을 깨는 가짜 J_V^s → 실패 → H4 구현 기각 (모든 셀 H4 중지 · 기록) — 가설 판정 아님."""
    assert [c["name"] for c in hb.h4_candidates()] == ["R1", "R2", "R3"]
    util = _util()
    model, halfcell = _h4_inputs(util.mod)
    gate = h.endpoint_gate(float(model["V_exp_interp"][0]), float(model["V_exp_interp"][-1]))
    r = hb.h4_positive(util.mod, model, halfcell, gate, jvs=lambda u, x, m, hc, g: {"value": float(x[0]), "reason": None, "span": 1.0})
    assert r["status"] == "FAIL" and r["stop_all_cells"] is True and "가설" in r["meaning"]
    store = hb.new_store()
    hb.record_h4(store, 3, r)
    assert hb.h4_block(store, 3) == "NOT_RUN:H4_IMPLEMENTATION_REJECTED" and hb.h4_block(store, 8) == "NOT_RUN:H4_IMPLEMENTATION_REJECTED"


def test_h_3_without_a_valid_candidate_the_cell_h4_is_unfit_unverifiable():
    """[RED 골격 실패] 세 후보 모두 어느 점에서 무효 (여기서는 n_out > 0) → 그 셀 H4 UNFIT (구현 검증 불가)."""
    assert [c["name"] for c in hb.h4_candidates()] == ["R1", "R2", "R3"]
    util = _util()
    model, halfcell = h.synthetic_wide_inputs(util.mod)
    gate = h.endpoint_gate(float(model["V_exp_interp"][0]), float(model["V_exp_interp"][-1]))
    r = hb.h4_positive(util.mod, model, halfcell, gate)
    assert r["status"] == "UNFIT_UNVERIFIABLE" and r["candidate"] is None and set(r["tried"]) == {"R1", "R2", "R3"}
    store = hb.new_store()
    hb.record_h4(store, 2, r)
    assert hb.h4_block(store, 2) == "NOT_RUN:H4_CONTROL_UNVERIFIABLE" and hb.h4_block(store, 5) is None


def test_h_4_the_negative_control_needs_distinguishable_absolute_curves():
    """[RED 골격 실패] D_abs > 1e-6 (c 둘 다) 통과 · 절대 곡선을 정규화한 가짜 → 실패 → "구현 · 수치 점검" (가설 기각 아님)."""
    assert [c["name"] for c in hb.h4_candidates()] == ["R1", "R2", "R3"]
    util = _util()
    _, halfcell = _h4_inputs(util.mod)
    x = [1.0, 1.0, 0.10, 0.05]
    r = hb.h4_negative(util.mod, halfcell, x)
    assert r["status"] == "PASS" and all(r["D_abs"][c] > 1e-6 for c in ("0.9", "1.1"))
    flat = lambda u, xx, hc: ((lambda q: 2.0 + 1.6 * np.asarray(q, dtype=float) / 3.0), 3.0)   # noqa: E731 — x 와 무관한 곡선
    bad = hb.h4_negative(util.mod, halfcell, x, vfull=flat)
    assert bad["status"] == "FAIL" and bad["action"] == "구현 · 수치 점검" and "가설" in bad["meaning"]


def test_h_5_control_points_never_enter_the_pools_witnesses_or_readings(fake, arrays, monkeypatch):
    """[RED 골격 실패] 대조 점 (control_pos · control_neg) 은 Ĵ 풀 · 증인 · 판독에 들어가지 않는다 (연결부 수준)."""
    store = _store_ready(fake, arrays, monkeypatch)
    store["phase_b"]["J_V|A1|0|control_pos|R1"] = {"status": "DONE", "unit": "J_V|A1|0", "stage": "control_pos",
                                                   "rows": [{"stage": "control_pos", "witness": "valid", "value": 1e-12, "x": X0,
                                                             "objective": "J_V", "region": "A1", "row": 0}]}
    pool = hb.pool_records(store, 0, "A1")
    assert pool and all(r["stage"] not in h.CONTROL_STAGES for r in pool)
    assert all(p.get("stage") not in h.CONTROL_STAGES for p in hb.unit_points(store, "J_V|A1|0"))
    out = hb.finalize(0, "A1", store, fake.ctx, grids=SUB)
    assert out["update"]["final"]["J_V|A1|0"] > 1e-12


# ======================================================================== r — ray 유보 (범위 확인 §9-2 · 부속 A §4-6)
def test_r_1_an_h4_unit_that_reaches_ray_stops_the_cell_region_without_an_update(fake, arrays, monkeypatch):
    """[RED 골격 실패] 끝점 수용된 합성 H4 단위가 Phase B 뒤 ray 단계에 닿음 → 구조 중지 RayNotImplemented · 그 (셀 · 영역) 갱신 0 · 완료 0."""
    _fake_minimize(monkeypatch, n_calls=1)
    ctx = dict(fake.ctx, gates={**fake.ctx["gates"], 3: {**h.endpoint_gate(2.0, 3.6)}})
    store = hb.new_store()
    hb.stage_a(["J_V|A1|3", "J_Vs|A1|3"], ctx, _fab_pa_runner(valid=lambda u: u == "J_Vs|A1|3"), store, arrays)
    monkeypatch.setattr(hb, "h4_positive", lambda *a, **kw: {"status": "PASS", "candidate": "R1", "stop_all_cells": False})
    monkeypatch.setattr(hb, "h4_negative", lambda *a, **kw: {"status": "PASS"})
    with pytest.raises(hb.RayNotImplemented):
        hb.stage_b(3, "A1", ctx, hb.direct_runner, store, arrays=arrays, arrays_dir=H_ARRAYS, seal_dir=fake.tmp / "r1", grids=SUB)
    assert "3|A1" not in store["updates"] and store["ray"]["reached"] == 1 and store["ray"]["status"] == "미구현"


def test_r_2_with_every_h4_unit_endpoint_gated_ray_is_never_reached_and_never_counted_complete(fake, arrays, monkeypatch):
    """[RED 골격 실패] H4 가 모두 끝점 UNFIT → ray 도달 0 · 기록 "ray: 미구현 (도달 0)" · 완료로 세지 않는다."""
    store = hb.new_store()
    hb.stage_a(["J_V|A1|0", "J_Vs|A1|0"], fake.ctx, _fab_pa_runner(valid=lambda u: False), store, arrays)
    out = hb.stage_b(0, "A1", fake.ctx, hb.direct_runner, store, arrays=arrays, arrays_dir=H_ARRAYS, seal_dir=fake.tmp / "r2", grids=SUB)
    assert out["ray"] == {"status": "미구현", "reached": 0} and "완료" not in json.dumps(out["ray"], ensure_ascii=False)
    assert store["not_run"]["J_Vs|A1|0"]["category"] == "NOT_RUN:ENDPOINT_GATE"


# ======================================================================== l — 표지 · 판독 (부속 A §7 · §3-7 · §1-1 · B §1-3 · §4)
def _pt(x, value, *, box="0", g="0", termination="converged", n_out=0, k=None, t=None):
    return {"witness": "valid", "value": value, "x": list(x), "residuals": {"box": box, "box_by_coord": [box] * 4, "g": g},
            "termination": termination, "n_out_PE": n_out, "n_out_NE": n_out, "k": k, "t": t}


def test_l_1_compatibility_grades_follow_the_exact_set_of_each_claim():
    """[RED 골격 실패] exact_feasible 하나 → COMPATIBLE · 모두 numerically_accepted → COMPATIBLE (수치 경계 의존) + UNRESOLVED · 없음 → NOT_FOUND."""
    q = MAX_Q
    xa = [1.0, 1.0, 0.3, 0.3 - float(q) * 0.1]                          # h = (1, 1, ≈0.9) — #1 의 명목 근처 (A0)
    pts = [dict(_pt(xa, 0.01), grid_t="1"), dict(_pt(xa, 0.01, box="1/100000000000000000"), grid_t="1")]
    a = hb.compat_individual(pts, "m_P", "0.02", 0.05, row=1, max_q=q)
    assert a["value"] == "COMPATIBLE" and a["unresolved"] is False and a["grades"] == {"exact_feasible": 1, "numerically_accepted": 1}
    b = hb.compat_individual(pts[1:], "m_P", "0.02", 0.05, row=1, max_q=q)
    assert b["value"] == "COMPATIBLE (수치 경계 의존)" and b["unresolved"] is True and "선형 제약 경계" in b["extra"]
    c = hb.compat_individual(pts, "m_P", "0.02", 0.001, row=1, max_q=q)
    assert c["value"] == "NOT_FOUND" and c["unresolved"] is True
    s = hb.compat_simultaneous([_pt(xa, 0.01)], "0.05", 0.05, row=1, region="A0", max_q=q)
    assert s["value"] in ("COMPATIBLE", "COMPATIBLE (수치 경계 의존)") and s["grades"]["exact_feasible"] + s["grades"]["numerically_accepted"] == 1


def test_l_2_wide_needs_two_satisfied_witnesses_more_than_two_tau_apart_in_actual_h_k():
    """[RED 골격 실패] 실제 h_k 차 (정확) > 2τ 且 둘 다 exact_feasible → WIDE · 하나라도 numerically_accepted → WIDE (수치 경계 의존) + UNRESOLVED · 아니면 NARROW_FOUND."""
    pts = [_pt([0.9, 0.8, 0.3, 0.1], 0.01), _pt([0.96, 0.8, 0.3, 0.1], 0.01), _pt([1.0, 0.8, 0.3, 0.1], 0.5)]
    assert hb.width(pts, "m_P", "0.02", 0.05, max_q=MAX_Q)["value"] == "WIDE"
    pn = [pts[0], dict(pts[1], residuals={"box": "1/100000000000000000", "box_by_coord": ["0"] * 4, "g": "0"})]
    wn = hb.width(pn, "m_P", "0.02", 0.05, max_q=MAX_Q)
    assert wn["value"] == "WIDE (수치 경계 의존)" and wn["unresolved"] is True
    nf = hb.width(pts, "m_P", "0.05", 0.05, max_q=MAX_Q)
    assert nf["value"] == "NARROW_FOUND" and nf["unresolved"] is True


def test_l_3_grid_statuses_and_side_labels_attach_together_and_never_replace_each_other():
    """[RED 골격 실패] 격자점 상태 넷 · 부가 라벨 (외삽 의존 · 제약 절단 · 경계 근접 · 선형 제약 경계 · budget 종료 증인) 이 함께 붙는다 · 등급별 증인 수."""
    T = 0.05
    assert hb.point_status({"search": "OK", "value": 0.04}, T) == "충족" and hb.point_status({"search": "OK", "value": 0.06}, T) == "초과"
    assert hb.point_status({"search": "실패", "value": None}, T) == "실패" and hb.point_status({"search": "미평가", "value": None}, T) == "미평가"
    p = _pt([0.9, 0.8, 0.3, 0.1], T - 1e-12, box="1/100000000000000000", termination="budget", n_out=2)
    lab = hb.extra_labels([p], T, row=0, k="LII")
    assert {"외삽 의존", "제약 절단", "경계 근접", "선형 제약 경계", "budget 종료 증인"} <= set(lab)
    assert hb.extra_labels([_pt([0.9, 0.8, 0.3, 0.1], 0.01)], T, row=1, k="m_P") == []


def test_l_4_the_main_reading_is_after_the_update_and_the_pre_update_reading_is_kept(fake, arrays, monkeypatch):
    """[RED 골격 실패] 계산 축 (OK · UNFIT:<이유>) · 주 판독 = 갱신 뒤 · 갱신 전 부표 · 둘 다 저장 (결과를 보고 고르지 않는다)."""
    store = _store_ready(fake, arrays, monkeypatch)
    out = hb.finalize(0, "A1", store, fake.ctx, grids=SUB)
    r = out["reading"]["J_V|A1|0"]
    assert set(r) >= {"pre", "final"} and r["final"]["H2"]["computation"] == "OK" and r["pre"]["H2"]["computation"] == "OK"
    assert r["final"]["H2"]["T"] <= r["pre"]["H2"]["T"]
    assert out["reading"]["J_Vs|A1|0"]["computation"] == "UNFIT:NOT_RUN:ENDPOINT_GATE"
    ctx = dict(fake.ctx, sigma_v={**fake.ctx["sigma_v"], 0: float("nan")})
    store2 = _store_ready(fake, arrays, monkeypatch)
    r2 = hb.finalize(0, "A1", store2, ctx, grids=SUB)["reading"]["J_V|A1|0"]
    assert r2["final"]["H2"]["computation"].startswith("UNFIT:")


# ======================================================================== c — 연결부 (회신 §5-3–5 · 부속 A §3-2 · §1-1 · B §4)
def _pa_rows(unit, arrays, value=lambda i: 0.1 + 0.001 * i):
    return _fab_pa_runner(value=lambda u, i: value(i))(h.phase_a_tasks([_unit(unit)], arrays, 1), {}, h.run_phase_a)["states"]


def test_c_1_rho_never_starts_on_an_incomplete_single_objective_phase_a(fake, arrays):
    """[RED 골격 실패] J_V A0 · J_D A0 중 하나라도 미완 (행 < 128 · 중단 · 봉인과 다른 x0 · run 중복) → ρ 0 · NOT_RUN:RHO_PRECONDITION (선행 미완)."""
    def runner(tasks, ctx, task_fn):
        raise AssertionError("선행 미완인데 ρ 를 돌렸다")
    fv, fd = _pa_rows("J_V|A0|2", arrays), _pa_rows("J_D|A0|2", arrays)
    cases = {"rows_127": fv[:-1], "interrupted": fv[:-1] + [{"task_id": fv[-1]["task_id"], "state": "STARTED_INTERRUPTED"}],
             "x0_changed": fv[:-1] + [dict(fv[-1], x0=[0.7, 0.7, 0.3, 0.05])], "run_duplicate": fv[:-1] + [dict(fv[-1], run_id=0)]}
    for name, rv in cases.items():
        store = hb.new_store()
        store["phase_a"]["J_V|A0|2"], store["phase_a"]["J_D|A0|2"] = rv, fd
        rec = hb.rho_wave(2, fake.ctx, runner, store, arrays)
        assert rec["status"] == "NOT_RUN" and rec["category"] == "NOT_RUN:RHO_PRECONDITION" and "선행 미완" in rec["reason"], name
        assert store["not_run"]["rho|A0|2"]["category"] == "NOT_RUN:RHO_PRECONDITION" and "rho|A0|2" not in store["phase_a"], name


def test_c_2_non_positive_denominators_or_an_empty_mask_make_the_combined_unit_unfit(fake, arrays):
    """[RED 골격 실패] 둘 다 완료지만 Ĵ⁽⁰⁾ 가 유한한 양수가 아님 · J_D 빈 마스크 → ρ 0 · 결합 UNFIT · 사유."""
    def runner(tasks, ctx, task_fn):
        raise AssertionError("분모가 없는데 ρ 를 돌렸다")
    store = hb.new_store()
    store["phase_a"]["J_V|A0|2"] = _pa_rows("J_V|A0|2", arrays, value=lambda i: 0.0)
    store["phase_a"]["J_D|A0|2"] = _pa_rows("J_D|A0|2", arrays)
    rec = hb.rho_wave(2, fake.ctx, runner, store, arrays)
    assert rec["category"] == "NOT_RUN:RHO_PRECONDITION" and "분모" in rec["reason"]
    store = hb.new_store()
    ctx = dict(fake.ctx, models={**fake.ctx["models"], 2: dict(MODEL(), dVdQ_exp_interp=np.full(100, 0.5))})
    hb.stage_a(["J_V|A0|2", "J_D|A0|2", "rho|A0|2"], ctx, _fab_pa_runner(), store, arrays)
    assert store["not_run"]["J_D|A0|2"]["category"] == "NOT_RUN:JD_EMPTY_MASK"
    assert store["not_run"]["rho|A0|2"]["category"] == "NOT_RUN:JD_EMPTY_MASK" and len(store["phase_a"]["J_V|A0|2"]) == 128


def test_c_3_rho_starts_only_after_both_phase_a_completion_records(fake, arrays):
    """[RED 골격 실패] 두 Phase A 의 완료 기록 뒤에만 ρ 작업이 시작한다 (사건 순서)."""
    store = hb.new_store()
    hb.stage_a(["J_V|A0|2", "J_D|A0|2", "rho|A0|2"], fake.ctx, _fab_pa_runner(), store, arrays)
    ev = {(e["kind"], e["key"]): e["seq"] for e in store["events"]}
    assert ev[("rho_start", "rho|A0|2")] > max(ev[("phase_a_complete", "J_V|A0|2")], ev[("phase_a_complete", "J_D|A0|2")])
    assert len(store["phase_a"]["rho|A0|2"]) == 128 and all(r["state"] == "COMPLETED" for r in store["phase_a"]["rho|A0|2"])


def test_c_4_the_common_update_refuses_when_a_registered_search_is_missing(fake, arrays, monkeypatch):
    """[RED 골격 실패] 빠진 격자점 · τ · 단위가 하나라도 있으면 갱신 거부 · 구조 중지 · 빠진 목록 기록 (은폐 불허)."""
    store = _store_ready(fake, arrays, monkeypatch)
    key = next(k for k in store["phase_b"] if "|profile|" in k)
    del store["phase_b"][key]
    with pytest.raises(hb.HStop) as ei:
        hb.finalize(0, "A1", store, fake.ctx, grids=SUB)
    assert key in str(ei.value) and "0|A1" not in store["updates"]
    store2 = _store_ready(fake, arrays, monkeypatch)
    sim = next(k for k in store2["phase_b"] if "|simultaneous|" in k)
    del store2["phase_b"][sim]
    with pytest.raises(hb.HStop) as ei:
        hb.finalize(0, "A1", store2, fake.ctx, grids=SUB)
    assert sim in str(ei.value)


def test_c_5_the_common_update_runs_exactly_once(fake, arrays, monkeypatch):
    """[RED 골격 실패] (셀 · 영역) 마다 갱신 1 회 — 탐색 대조 전 (중간) 호출 · 둘째 호출 거부."""
    store = _store_ready(fake, arrays, monkeypatch)
    with pytest.raises(hb.HStop):
        hb.common_update_once(0, "A1", store)
    out = hb.finalize(0, "A1", store, fake.ctx, grids=SUB)
    assert "0|A1" in store["updates"] and out["update"]["final"]
    with pytest.raises(hb.HStop):
        hb.finalize(0, "A1", store, fake.ctx, grids=SUB)
    with pytest.raises(hb.HStop):
        hb.common_update_once(0, "A1", store)


def test_c_6_the_reading_rereads_the_same_final_stored_points_and_every_rho_pair(fake, arrays, monkeypatch):
    """[RED 골격 실패] 판독 = 같은 최종 저장점 집합 · 새 평가 0 · 결합 단위의 모든 유효 (J_V, J_D) 쌍을 최종 분모로 다시 비교."""
    store = _store_ready(fake, arrays, monkeypatch, cell=0, region="A0")
    calls = fake.mod.MODE["calls"]
    out = hb.finalize(0, "A0", store, fake.ctx, grids=SUB)
    assert fake.mod.MODE["calls"] == calls
    fv, fd = out["update"]["final"]["J_V|A0|0"], out["update"]["final"]["J_D|A0|0"]
    valid = [p for p in hb.unit_points(store, "rho|A0|0") if p["witness"] == "valid"]
    rr = out["reading"]["rho|A0|0"]["final_rho"]
    assert len(rr) == len(valid) >= 128
    assert all(r["rho_final"] == max(p["components"]["J_V"] / fv, p["components"]["J_D"] / fd) for r, p in zip(rr, valid))


def test_c_7_not_run_and_unresolved_are_counted_apart_and_the_plan_adds_up(fake, arrays, monkeypatch):
    """[RED 골격 실패] 끝점 게이트 · J_D 빈 마스크 · ρ 선행 · PRIOR_INCOMPATIBLE · UNFIT · 미해결을 따로 센다 · 계획 = 실행 + 미실행."""
    store = _store_ready(fake, arrays, monkeypatch)
    ctx = dict(fake.ctx, models={**fake.ctx["models"], 5: dict(MODEL(), dVdQ_exp_interp=np.full(100, 0.5))})
    hb.stage_a(["J_V|A0|5", "J_D|A0|5", "rho|A0|5", "J_V|A2|7"], ctx, _fab_pa_runner(valid=lambda u: u != "J_V|A2|7"), store, arrays)
    hb.finalize(0, "A1", store, fake.ctx, grids=SUB)
    pc = hb.plan_counts(store)
    a = pc["phase_a"]
    assert a["not_run"] == {"NOT_RUN:ENDPOINT_GATE": 1, "NOT_RUN:JD_EMPTY_MASK": 2}
    assert a["planned_units"] == a["run_units"] + sum(a["not_run"].values()) and a["unfit_units"] == 1
    assert a["planned_runs"] == 128 * a["planned_units"] and "끝점 게이트만" in a["note"]
    b = pc["phase_b"]["0|A1"]
    assert b["registered"] == b["done"] + sum(b["not_run"].values()) and b["not_run"].get("NOT_RUN:PRIOR_INCOMPATIBLE") == 1
    assert set(pc["unresolved"]) == {"초과", "실패", "NOT_FOUND"} and all(isinstance(v, int) for v in pc["unresolved"].values())


def test_c_8_end_to_end_one_cell_a0_through_supervise_and_phase_b(fake, arrays, monkeypatch):
    """[RED 골격 실패] 단계 A (가짜 minimize · supervise fork 작업자 1 · J_V A0 · J_D A0 → ρ) → 단계 B (부분 격자) → 갱신 1 회 → 판독 · 표지."""
    _fake_minimize(monkeypatch, n_calls=1)
    store = hb.new_store()
    run_sup = hb.supervise_runner(limits=dict(LIM), n_workers=1, rss_fn=lambda p: 1000, disk_fn=lambda r: (0, 10 ** 12),
                                  tick=0.05, disk_every=0.05)
    hb.stage_a(["J_V|A0|0", "J_D|A0|0", "rho|A0|0", "J_Vs|A0|0"], fake.ctx, run_sup, store, arrays)
    assert all(len(store["phase_a"][u]) == 128 for u in ("J_V|A0|0", "J_D|A0|0", "rho|A0|0"))
    assert store["not_run"]["J_Vs|A0|0"]["category"] == "NOT_RUN:ENDPOINT_GATE"
    out = hb.stage_b(0, "A0", fake.ctx, hb.direct_runner, store, arrays=arrays, arrays_dir=H_ARRAYS, seal_dir=fake.tmp / "c8", grids=SUB)
    assert "0|A0" in store["updates"] and {"J_V|A0|0", "J_D|A0|0", "rho|A0|0"} <= set(out["reading"])
    lab = out["reading"]["J_V|A0|0"]["final"]["H2"]
    assert set(lab["compat_individual"]) == set(h.COORDS) and lab["compat_nominal"]["value"] == "PRIOR_INCOMPATIBLE"
    assert out["ray"] == {"status": "미구현", "reached": 0}


# ======================================================================== d — 읽기 전용 건조 (C4 v2 §4-5 · A1 이후 규칙)
def test_d_1_the_phase_b_dry_run_writes_only_plan_b(tmp_path):
    """[RED 골격 실패] PLAN_B.json 하나 · execution 0 · 0b1 배열 바이트 대조 · 게이트 반영 상한과 미정 (C4-A) 을 구분."""
    out = tmp_path / "dry_b"
    rec = hb.dryrun_b(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=PHASE_A_ARRAYS, h_arrays_dir=H_ARRAYS,
                      h_manifest_sha256=H_MANIFEST, util_copy=UTIL_COPY, p0_result=P0_RESULT, env_identity=FAKE_IDENT)
    assert rec["ok"] and sorted(p.name for p in out.iterdir()) == ["PLAN_B.json"]
    plan = json.loads((out / "PLAN_B.json").read_text(encoding="utf-8"))
    assert plan["execution"] == {"optimizer_calls": 0, "objective_calls": 0, "util_imported": False, "sobol_generated": 0}
    assert plan["arrays"]["h"]["mode"] == "bytes" and plan["phase_a"]["planned_after_endpoint_gate"] == 7040
    assert "끝점 게이트만" in plan["phase_a"]["note"] and plan["h4"]["endpoint_gated_units"] == 22 and plan["ray"]["status"] == "미구현"
    pb = plan["phase_b"]
    assert pb["units_after_endpoint_gate"] == 55 and pb["undetermined"]
    assert pb["upper_bound_local_runs"] == pb["profile_runs_ub"] + pb["simultaneous_runs_ub"] + pb["nominal_refine_ub"]


def test_d_2_the_phase_b_dry_run_refuses_bad_arrays_data_paths_and_an_existing_output(tmp_path):
    """[RED 골격 실패] 다른 MANIFEST sha · 이미 있는 출력 · 자료 경로를 거부 (fail-closed) · CLI 는 명시 경로만."""
    kw = dict(venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=PHASE_A_ARRAYS, h_arrays_dir=H_ARRAYS,
              util_copy=UTIL_COPY, p0_result=P0_RESULT, env_identity=FAKE_IDENT)
    with pytest.raises(hb.HStop):
        hb.dryrun_b(tmp_path / "a", h_manifest_sha256="0" * 64, **kw)
    (tmp_path / "b").mkdir()
    with pytest.raises(hb.HStop):
        hb.dryrun_b(tmp_path / "b", h_manifest_sha256=H_MANIFEST, **kw)
    with pytest.raises((hb.HStop, e3a.E3aStop)):
        hb.dryrun_b(tmp_path / "c", h_manifest_sha256=H_MANIFEST, **dict(kw, util_copy=Path("/x/LFP_Data.xlsx")))
    assert not (tmp_path / "a").exists() and not (tmp_path / "c").exists()
    with pytest.raises(SystemExit):
        hb.main(["dryrun-b", "--venv", "/v"])
