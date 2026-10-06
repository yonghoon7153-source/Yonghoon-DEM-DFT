"""REIL C5 비용 파일럿 — 합성 입력만 (REIL 자료 · 정식 Sobol · 측정 0). RED 를 먼저 본 뒤 구현한다.

규칙 원문: `docs/REIL_C5_PILOT_APPROVAL_REQUEST_v2_20261006.md` §2 · §3 · §4 · §5 (덮을 것 10 항목) · 부록 `…_v2_ADDENDUM_20261006.md`
A1 (계산 없는 환경 식별) · A2 (상태 4 + 전체 RECORD_INCOMPLETE). 읽는 저장소 텍스트 입력 (부록 A3): `evidence/reil_p0_20261006/P0_RESULT.json` ·
봉인 `reil_c6_rebuild_20261006/COBYQA_OPTIONS.json` · util 사본 `reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt`.
가짜 util 은 `tmp_path` 의 파일로 만들어 같은 방식 (경로 로드) 으로 읽는다 — traceback 의 util frame 판정을 실물과 같게.
"""
import json
import math
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c5_pilot as pl

BMS = Path(__file__).resolve().parents[1]

FAKE_UTIL = '''
import os
import time
import numpy as np

MODE = {"kind": "ok"}
CALLS = {"n": 0}


def objective_fun(x, Model, halfcell):
    CALLS["n"] += 1
    Model["touched"] = CALLS["n"]                 # 그들 코드처럼 Model 에 키를 써 넣는다
    k = MODE["kind"]
    if k == "raise_value" and CALLS["n"] >= MODE.get("at", 1):
        np.max(np.array([]))                     # 그들 205 행의 빈 배열 np.max 형태 (ValueError)
    if k == "raise_memory":
        raise MemoryError("fake")
    if k == "raise_os":
        raise OSError("fake")
    if k == "raise_recursion":
        raise RecursionError("fake")
    if k == "exit":
        os._exit(7)
    if k == "sleep":
        time.sleep(MODE.get("s", 0.2))
    if k == "bad_return":
        return ["a", "b"]
    if k == "reeval_raise" and MODE.get("armed"):
        np.max(np.array([]))
    if k == "nan" and CALLS["n"] % 2 == 0:
        return np.array([0.0, float("nan"), 0.0, 0.0])
    m_P, m_N, d_P, d_N = x
    f2 = (m_P - 0.9) ** 2 + (m_N - 0.8) ** 2 + (d_P - 0.2) ** 2 + (d_N - 0.1) ** 2
    return np.array([0.0, f2, 0.0, 0.0])


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    if MODE["kind"] == "label_raise":
        raise ValueError("label")
    q = np.linspace(0.0, 1.0, interp_len)
    return (q * m_P - d_P, q * m_N - d_N, None, None, None, None, None, None)
'''

SMALL = dict(pl.OPTIONS, maxfev=40, maxiter=80)
X_GOOD = [0.9, 0.8, 0.2, 0.1]


@pytest.fixture
def fake(tmp_path):
    p = tmp_path / "fake_util_LFP.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    import importlib.machinery
    import importlib.util
    loader = importlib.machinery.SourceFileLoader(f"fake_util_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    model = {"Q_exp_interp": np.linspace(-0.2, 1.2, 50), "V_exp_interp": np.linspace(2.0, 3.6, 50)}
    halfcell = [np.linspace(0, 1, 10), np.linspace(3.2, 3.5, 10), np.linspace(0, 1, 10), np.linspace(0.6, 0.1, 10)]
    ctx = {"util": mod, "util_file": str(p.resolve()), "model": model, "halfcell": halfcell, "options": SMALL}
    return SimpleNamespace(mod=mod, ctx=ctx, path=p)


def _run(rid=0, x0=(0.85, 0.75, 0.25, 0.05), worker=0):
    return {"run_id": rid, "seed": 0, "row": rid, "x0": list(x0), "worker": worker}


def _runs(n, n_workers):
    return [_run(i, worker=i % n_workers) for i in range(n)]


DISK_OK = staticmethod(lambda d: (0, 100 * 2 ** 30))


def _orch(fake, runs, n_workers=2, **kw):
    lim = dict(pl.LIMITS_DRY, measure=kw.pop("measure", 60.0), grace=kw.pop("grace", 3.0),
               rss_gap=kw.pop("rss_gap", 5.0), disk_gap=kw.pop("disk_gap", 15.0))
    return pl.orchestrate(runs, fake.ctx, n_workers=n_workers, limits=lim, t0=time.monotonic(),
                          rss_fn=kw.pop("rss_fn", lambda pids: 1000), disk_fn=kw.pop("disk_fn", lambda d: (0, 100 * 2 ** 30)),
                          out_dir=None, tick=0.05, disk_every=0.05, **kw)


# ======================================================================== (1) 정확 잔차 · 증인 · 종료
def test_01_exact_residuals_are_rationals_and_the_tolerance_is_inclusive():
    r = pl.exact_residuals([0.75, 0.5, 0.1001, 0.1])
    assert isinstance(r["box"], Fraction) and isinstance(r["g"], Fraction)
    assert r["box"] == 0
    assert pl.witness(solver_error=False, reeval_error=False, jv=0.1, x=[0.75, 0.5, 0.1001, 0.1]) == "valid"
    # 상자 경계는 십진 문자열의 정확 유리수 — float 0.6 은 3/5 보다 2.2e-17 작아 '경계 밖 · 허용치 안' 이다
    assert 0 < pl.exact_residuals([0.6, 0.5, 0.1001, 0.1])["box"] <= pl.TOL
    assert pl.feasibility_class([0.6, 0.5, 0.1001, 0.1]) == "within_tol"
    assert pl.witness(solver_error=False, reeval_error=False, jv=0.1, x=[1.1 + 5e-11, 0.8, 0.2, 0.1]) == "valid"
    assert pl.witness(solver_error=False, reeval_error=False, jv=0.1, x=[1.1 + 2e-10, 0.8, 0.2, 0.1]) == "invalid:INFEASIBLE_RETURN"
    assert pl.witness(solver_error=False, reeval_error=False, jv=0.1, x=[0.9, 0.8, 0.2, 0.2 - 1e-4 + 2e-10]) \
        == "invalid:INFEASIBLE_RETURN"
    assert pl.frac_str(Fraction(1, 3)) == "1/3" and pl.frac_str(Fraction(2)) == "2"
    assert pl.exact_residuals([1.1 + 2e-10, 0.8, 0.2, 0.1])["box"] == Fraction(1.1 + 2e-10) - Fraction("1.1")


def test_01_witness_priority_and_nonfinite():
    assert pl.witness(solver_error=True, reeval_error=True, jv=0.1, x=X_GOOD) == "invalid:SOLVER_ERROR"
    assert pl.witness(solver_error=False, reeval_error=True, jv=0.1, x=X_GOOD) == "invalid:REEVAL_ERROR"
    assert pl.witness(solver_error=False, reeval_error=False, jv=float("nan"), x=X_GOOD) == "invalid:NONFINITE"
    assert pl.witness(solver_error=False, reeval_error=False, jv=0.1, x=[float("nan"), 0.8, 0.2, 0.1]) == "invalid:NONFINITE"
    assert pl.feasibility_class(X_GOOD) == "feasible"
    assert pl.feasibility_class([1.1 + 5e-11, 0.8, 0.2, 0.1]) == "within_tol"
    assert pl.feasibility_class([1.2, 0.8, 0.2, 0.1]) == "infeasible"


def test_01_termination_classes_keep_converged_budget_and_others_apart():
    assert pl.termination_of(SimpleNamespace(success=True, status=0)) == "converged"
    assert pl.termination_of(SimpleNamespace(success=False, status=5)) == "budget"
    assert pl.termination_of(SimpleNamespace(success=False, status=6)) == "budget"
    assert pl.termination_of(SimpleNamespace(success=False, status=-1)) == "unclassified"


# ======================================================================== (2) 오류 분류 · 우선순위 · 카운터
def test_02_util_error_during_optimization_is_a_local_solver_error_counted_with_the_failing_call(fake):
    fake.mod.MODE.update(kind="raise_value", at=3)
    row = pl.run_one(_run(), fake.ctx)
    assert row["state"] == "COMPLETED" and row["termination"] == "solver_error"
    assert row["witness"] == "invalid:SOLVER_ERROR" and row["reeval_attempts"] == 0 and row["x"] is None
    assert row["error"]["origin"] == "util" and row["error"]["stage"] == "optimize" and row["error"]["type"] == "ValueError"
    assert row["n_eval"] == 3, "예외로 끝난 호출도 센다"
    assert row["error"]["traceback"], "traceback 요약"


def test_02_an_error_inside_scipy_outside_the_objective_is_local_with_optimizer_origin(fake):
    row = pl.run_one(_run(x0=(0.9, 0.8, 0.2)), fake.ctx)          # 길이 3 — scipy 안에서 거부
    assert row["termination"] == "solver_error" and row["error"]["origin"] == "optimizer"


@pytest.mark.parametrize("kind,typ", [("raise_memory", "MemoryError"), ("raise_os", "OSError"),
                                      ("raise_recursion", "RecursionError")])
def test_02_structural_errors_from_util_stop_the_pilot(fake, kind, typ):
    fake.mod.MODE.update(kind=kind)
    with pytest.raises(pl.Structural) as ei:
        pl.run_one(_run(), fake.ctx)
    assert ei.value.info["kind"] == "structural" and ei.value.info["type"] == typ


def test_02_an_error_in_our_own_wrapper_is_structural(fake):
    fake.mod.MODE.update(kind="bad_return")
    with pytest.raises(pl.Structural) as ei:
        pl.run_one(_run(), fake.ctx)
    assert ei.value.info["origin"] == "ours"


def test_02_a_reeval_error_keeps_the_returned_point_and_is_its_own_reason(fake):
    fake.mod.MODE.update(kind="reeval_raise")
    seen = []

    def notify(kind, payload):
        seen.append(kind)
        fake.mod.MODE["armed"] = True                              # 반환 뒤에만 실패
    row = pl.run_one(_run(), fake.ctx, notify=notify)
    assert seen == ["returned"]
    assert row["witness"] == "invalid:REEVAL_ERROR" and row["reeval_attempts"] == 1
    assert row["x"] is not None and row["status"] is not None and row["termination"] in ("converged", "budget", "unclassified")
    assert row["reeval_error"]["stage"] == "reeval" and row["reeval_error"]["origin"] == "util"


def test_02_unknown_option_warning_is_fail_closed(fake):
    fake.ctx["options"] = dict(SMALL, zz_unknown=1)
    with pytest.raises(pl.Structural) as ei:
        pl.run_one(_run(), fake.ctx)
    assert "옵션" in ei.value.info["message"]


def test_02_classification_table_without_running_a_solver(fake):
    try:
        raise ValueError("x")
    except ValueError as e:
        info = pl.classify_exception(e, "record", fake.ctx["util_file"])
    assert info["kind"] == "structural", "기록 단계의 예외는 구조 오류"


# ======================================================================== (3) 비유한 전달 · 따로 기록
def test_03_nonfinite_is_passed_through_unchanged_and_counted(fake):
    fake.mod.MODE.update(kind="nan")
    obj = pl.Objective(fake.mod, {}, None)
    a, b = obj(X_GOOD), obj(X_GOOD)
    assert math.isfinite(a) and math.isnan(b), "nan 을 유한 벌점으로 바꾸지 않는다"
    assert obj.n_eval == 2 and obj.n_nonfinite == 1
    row = pl.run_one(_run(), fake.ctx)
    assert row["n_nonfinite"] >= 1
    assert (row["termination"] == "solver_error") or (row["x"] is not None and "jv_reeval" in row)


# ======================================================================== (4) 시간 상한 → 상태 · 보존 · 숨은 재시작 없음
def test_04_all_runs_complete_without_a_global_stop(fake):
    o = _orch(fake, _runs(4, 2))
    assert o["global_stop"] is None, o["global_stop"]
    assert [s["state"] for s in o["states"]] == ["COMPLETED"] * 4
    assert sorted(s["run_id"] for s in o["states"]) == [0, 1, 2, 3]
    assert o["owned_alive_after"] == 0


def test_04_a_stop_before_start_leaves_every_run_not_started(fake):
    o = _orch(fake, _runs(3, 2), measure=0.0)
    assert {s["state"] for s in o["states"]} == {"NOT_STARTED"} and "단계 경계" in o["global_stop"]


def test_04_the_measurement_boundary_interrupts_and_keeps_what_was_secured(fake):
    fake.mod.MODE.update(kind="sleep", s=0.15)
    o = _orch(fake, _runs(6, 2), measure=1.0, grace=2.0)
    st = [s["state"] for s in o["states"]]
    assert "단계 경계" in o["global_stop"]
    assert "STARTED_INTERRUPTED" in st and len(st) == 6 and set(st) <= set(pl.STATES)
    for s in o["states"]:
        if s["state"] == "STARTED_INTERRUPTED":
            assert s["n_eval_observed"].startswith("≥ ") and s["n_eval_observed"].endswith("미확인")
            assert s["elapsed_s"] is not None and s["interrupt_reason"]
    assert len({s["run_id"] for s in o["states"]}) == 6, "한 실행이 두 번 나오지 않는다 (숨은 재시작 없음)"
    assert o["owned_alive_after"] == 0


def test_04_returned_but_not_reevaluated_is_its_own_state_and_keeps_the_point():
    runs = [_run(0), _run(1), _run(2)]
    ev = {"started": {0: {"t": 1.0}, 1: {"t": 1.0}, 2: {"t": 2.0}}, "returned": {1: {"x": X_GOOD, "status": 5}},
          "done": {0: {"run_id": 0, "witness": "valid", "termination": "converged"}}}
    st = pl.assemble_states(runs, ev, {0: 9, 1: 40, 2: 5}, "단계 경계", 10.0)
    assert [s["state"] for s in st] == ["COMPLETED", "RETURNED_REEVAL_INTERRUPTED", "STARTED_INTERRUPTED"]
    assert st[1]["returned"]["x"] == X_GOOD and st[1]["witness"] == "미확정"
    assert st[2]["n_eval_observed"] == "≥ 5 · 미확인" and st[2]["elapsed_s"] == 8.0


def test_04_record_deadline_or_write_failure_is_record_incomplete_and_keeps_written_files(tmp_path):
    parts = {"ROWS.json": [{"a": 1}], "SUMMARY.json": {"b": float("nan")}, "RUN_RECORD.json": {"c": 3}}
    (tmp_path / "ok").mkdir()
    ok = pl.final_record(tmp_path / "ok", parts, t0=0.0)
    assert ok["record_state"] == "COMPLETE" and set(ok["files"]) == set(parts)
    for n, h in ok["files"].items():
        assert pl._sha((tmp_path / "ok" / n).read_bytes()) == h
    assert json.loads((tmp_path / "ok" / "SUMMARY.json").read_text())["b"] == "nan"
    (tmp_path / "bad").mkdir()
    calls = []

    def write(path, data):
        calls.append(path.name)
        if len(calls) == 2:
            raise OSError("disk full (fake)")
        path.write_bytes(data)
    bad = pl.final_record(tmp_path / "bad", parts, t0=0.0, write=write)
    assert bad["record_state"] == "RECORD_INCOMPLETE" and (tmp_path / "bad" / "ROWS.json").is_file()
    assert not (tmp_path / "bad" / "RUN_RECORD.json").exists()
    (tmp_path / "late").mkdir()
    late = pl.final_record(tmp_path / "late", parts, clock=lambda: 100.0, t0=0.0, limit=10.0)
    assert late["record_state"] == "RECORD_INCOMPLETE" and late["files"] == {}


# ======================================================================== (5) 전역 중단 · 소유 작업자만 종료
@pytest.mark.parametrize("case", ["worker_exit", "structural", "rss_over", "monitor_fail", "rss_gap", "disk_new", "disk_free"])
def test_05_global_stops_end_only_owned_workers(fake, case):
    ext = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        kw = {}
        if case == "worker_exit":
            fake.mod.MODE.update(kind="exit")
            want = "비정상 종료"
        elif case == "structural":
            fake.mod.MODE.update(kind="raise_memory")
            want = "MemoryError"
        else:
            fake.mod.MODE.update(kind="sleep", s=0.1)
            if case == "rss_over":
                kw["rss_fn"], want = (lambda pids: 5 * 2 ** 30), "메모리"
            elif case == "monitor_fail":
                def boom(pids):
                    raise RuntimeError("proc unreadable")
                kw["rss_fn"], want = boom, "감시 실패"
            elif case == "rss_gap":
                kw["rss_fn"], kw["rss_gap"], want = (lambda pids: None), 0.3, "누락"
            elif case == "disk_new":
                kw["disk_fn"], want = (lambda d: (2 ** 31, 100 * 2 ** 30)), "디스크"
            else:
                kw["disk_fn"], want = (lambda d: (0, 2 ** 30)), "디스크"
        o = _orch(fake, _runs(4, 2), **kw)
        assert o["global_stop"] and want in o["global_stop"], o["global_stop"]
        assert o["owned_alive_after"] == 0
        assert ext.poll() is None, "소유하지 않은 프로세스를 건드렸다"
        assert len(o["states"]) == 4 and all(s["state"] in pl.STATES for s in o["states"])
    finally:
        ext.kill()
        ext.wait()


# ======================================================================== (6) 식별 변조 거부 — 계산 없는 환경 식별 (부록 A1)
def _sealed(tmp_path):
    sealed = tmp_path / "sealed"
    sealed.mkdir()
    impl = tmp_path / "site"
    (impl / "scipy/_lib/cobyqa").mkdir(parents=True)
    (impl / "scipy/_lib/cobyqa/main.py").write_text("main", encoding="utf-8")
    real = json.loads((pl.SEALED / "COBYQA_OPTIONS.json").read_text(encoding="utf-8"))
    cob = {"options": real["options"],
           "implementation_files_sha256": {"scipy/_lib/cobyqa/main.py": pl._sha(b"main")}}
    (sealed / "COBYQA_OPTIONS.json").write_text(json.dumps(cob), encoding="utf-8")
    (sealed / "REIL_C6.lock.txt").write_text("LOCK\n", encoding="utf-8")
    (sealed / "PROFILE.json").write_text(pl.prof._dump({"p": 1}), encoding="utf-8")
    man = {n: pl._sha((sealed / n).read_bytes()) for n in ("COBYQA_OPTIONS.json", "REIL_C6.lock.txt", "PROFILE.json")}
    (sealed / "MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    return sealed, impl


@pytest.fixture
def no_compute(monkeypatch):
    """식별은 합성 최적화 · Sobol · emit · full check 를 부르지 않는다 — 부르면 시험이 떨어진다."""
    def forbidden(*a, **k):
        raise AssertionError("계산하는 C6 함수를 불렀다")
    for name in ("cobyqa_options", "sobol", "emit", "check"):
        monkeypatch.setattr(pl.prof, name, forbidden)
    monkeypatch.setattr(pl.prof, "lock_text", lambda: "LOCK\n")
    monkeypatch.setattr(pl.prof, "profile", lambda: {"p": 1})


def test_06_identity_passes_without_computation_and_leaves_the_full_check_not_run(tmp_path, no_compute):
    sealed, impl = _sealed(tmp_path)
    r = pl.env_identity(venv=sys.prefix, sealed=sealed, impl_root=impl)
    assert r["ok"], r["problems"]
    assert r["full_c6_check"] == "NOT_RUN"
    assert r["record"]["executable"] and r["record"]["prefix"] == sys.prefix


@pytest.mark.parametrize("tamper", ["interpreter", "lock", "profile", "options", "impl_file", "manifest"])
def test_06_identity_tampering_is_refused(tmp_path, no_compute, monkeypatch, tamper):
    sealed, impl = _sealed(tmp_path)
    venv, opts = sys.prefix, dict(pl.OPTIONS)
    if tamper == "interpreter":
        venv = str(tmp_path / "other_venv")
    elif tamper == "lock":
        monkeypatch.setattr(pl.prof, "lock_text", lambda: "LOCK changed\n")
    elif tamper == "profile":
        monkeypatch.setattr(pl.prof, "profile", lambda: {"p": 2})
    elif tamper == "options":
        opts["maxfev"] = 2001
    elif tamper == "impl_file":
        (impl / "scipy/_lib/cobyqa/main.py").write_text("main changed", encoding="utf-8")
    else:
        (sealed / "PROFILE.json").write_text(pl.prof._dump({"p": 1}) + " ", encoding="utf-8")
    r = pl.env_identity(venv=venv, sealed=sealed, options=opts, impl_root=impl)
    assert not r["ok"] and r["problems"], tamper


def test_06_options_equal_the_sealed_c6_table_and_a_change_is_named():
    table = json.loads((pl.SEALED / "COBYQA_OPTIONS.json").read_text(encoding="utf-8"))["options"]
    assert pl.check_options(table, pl.OPTIONS) == []
    bad = pl.check_options(table, dict(pl.OPTIONS, maxfev=2001))
    assert bad and "maxfev" in bad[0]
    assert pl.check_options(table, {k: v for k, v in pl.OPTIONS.items() if k != "disp"})


def test_06_pilot_arrays_are_compared_byte_for_byte_with_the_seal(tmp_path):
    rng = np.random.default_rng(0)
    arrs = {s: rng.random((64, 4)) for s in (0, 1)}
    sealed = tmp_path / "s"
    sealed.mkdir()
    for s, name in pl.PILOT_ARRAYS.items():
        np.save(sealed / name, np.ascontiguousarray(arrs[s], dtype="<f8"), allow_pickle=False)
    got, probs = pl.pilot_arrays(sealed, make=lambda s: arrs[s])
    assert probs == [] and set(got) == {0, 1}
    _, probs = pl.pilot_arrays(sealed, make=lambda s: arrs[s] + (np.eye(64, 4) * 1e-12 if s == 1 else 0.0))
    assert len(probs) == 1 and "seed 1" in probs[0]


def test_06_run_plan_is_fixed_by_run_number_and_bad_starts_are_refused():
    arrs = {0: np.full((64, 4), 0.5), 1: np.full((64, 4), 0.6)}
    runs = pl.plan_runs(arrs, 4)
    assert [r["run_id"] for r in runs] == list(range(128))
    assert all(r["worker"] == r["run_id"] % 4 for r in runs)
    assert runs[64]["seed"] == 1 and runs[64]["row"] == 0 and runs[63]["row"] == 63
    with pytest.raises(pl.GlobalStop):
        pl.plan_runs({0: np.full((64, 3), 0.5)}, 4)
    with pytest.raises(pl.GlobalStop):
        pl.plan_runs({0: np.full((64, 4), np.nan)}, 4)


# ======================================================================== (7) 종료 HEAD · 작업 트리 · 소스 변경 · 산출 dirty
def test_07_git_state_records_head_and_raw_porcelain_and_own_output_is_split():
    g = pl.git_state()
    assert len(g["head"]) == 40 and g["head_rc"] == 0 and isinstance(g["porcelain"], str)
    lines = "?? bms-balancing/evidence/reil_c5_x/ROWS.json\n M bms-balancing/scripts/reil_c5_pilot.py\n"
    d = pl.split_dirty(lines, ["bms-balancing/evidence/reil_c5_x"])
    assert len(d["own_output"]) == 1 and len(d["other"]) == 1 and "scripts" in d["other"][0]


def test_07_a_source_change_during_the_run_is_detected(tmp_path):
    a = tmp_path / "a.py"
    a.write_text("x = 1\n", encoding="utf-8")
    h0 = pl.source_hashes([a, tmp_path / "missing.py"])
    a.write_text("x = 2\n", encoding="utf-8")
    assert pl.source_changed(h0, pl.source_hashes([a, tmp_path / "missing.py"])) == [str(a)]
    assert pl.source_changed(h0, h0) == []


# ======================================================================== (8) Model 격리 · 원본 해시 불변
def test_08_runs_and_reeval_use_fresh_deep_copies_and_the_original_is_unchanged(fake):
    h_model, h_half = pl.model_digest(fake.ctx["model"]), pl.model_digest(fake.ctx["halfcell"])
    r1 = pl.run_one(_run(0), fake.ctx)
    r2 = pl.run_one(_run(1), fake.ctx)
    assert "touched" not in fake.ctx["model"], "원본 Model 에 그들 코드의 쓰기가 남았다"
    assert pl.model_digest(fake.ctx["model"]) == h_model and pl.model_digest(fake.ctx["halfcell"]) == h_half
    assert r1["witness"] == r2["witness"] == "valid"


# ======================================================================== (9) 비용 요약 — 빠짐없이 나누고 상한 도달을 완료로 올리지 않음
def test_09_summary_partitions_every_run_and_keeps_censored_apart():
    st = [{"state": "COMPLETED", "termination": "converged", "witness": "valid", "wall": 2.0, "cpu": 2.0, "n_eval": 10, "worker": 0},
          {"state": "COMPLETED", "termination": "budget", "witness": "valid", "wall": 4.0, "cpu": 4.0, "n_eval": 20, "worker": 1},
          {"state": "COMPLETED", "termination": "solver_error", "witness": "invalid:SOLVER_ERROR", "wall": 1.0, "cpu": 1.0,
           "n_eval": 3, "worker": 0},
          {"state": "STARTED_INTERRUPTED", "elapsed_s": 50.0, "worker": 1},
          {"state": "RETURNED_REEVAL_INTERRUPTED", "elapsed_s": 30.0, "worker": 0},
          {"state": "NOT_STARTED", "worker": 1}]
    s = pl.summarize(st, wall=10.0)
    assert sum(s["by_state"].values()) == 6 and s["by_state"]["COMPLETED"] == 3
    assert s["completed_without_local_error"] == 2 and s["completed_local_error"] == 1
    assert s["interrupted"] == 2 and s["not_started"] == 1
    assert s["censored_elapsed_s"] == [30.0, 50.0] and s["wall_completed_s"]["max"] == 4.0, "중단은 완료 분포에 섞지 않는다"
    assert s["budget_ratio_of_completed"] == pytest.approx(1 / 3)
    text = json.dumps(pl._jsonable(s))
    assert "jv" not in text and "speedup" not in s and "efficiency" not in s


# ======================================================================== (10) 자료 경로 · fixture Sobol · 셀 규칙 · util 사본
def test_10_data_paths_are_refused_in_this_stage():
    for p in ("x/LFP_Data.xlsx", "r/a.pkl", "n/nb.ipynb"):
        with pytest.raises(pl.GlobalStop):
            pl.guard_paths([p])
    pl.guard_paths([pl.UTIL_COPY])


def test_10_fixture_starts_are_four_points_in_the_box_and_deterministic():
    a, b = pl.fixture_starts(), pl.fixture_starts()
    assert a.shape == (4, 4) and np.array_equal(a, b)
    lo, hi = pl.prof.BOXES["A0_their_box"]
    assert np.all(a >= np.array(lo)) and np.all(a <= np.array(hi))
    assert pl.FIXTURE_SOBOL_RNG == 20261006 and pl.FIXTURE_SOBOL_RNG not in (0, 1)


def test_10_the_cell_rule_picks_row_1_from_the_p0_result_and_refuses_another():
    res = json.loads(pl.P0_RESULT.read_text(encoding="utf-8"))
    assert pl.select_cell(res) == 1 and pl.require_cell(res) == 1
    for r in res["prior_table"]:
        if r["row"] == 1 and r["region"] == "A0" and r["tau"] == "0":
            r["status"] = "PRIOR_INCOMPATIBLE"
    try:
        assert pl.select_cell(res) != 1                          # 다른 행을 고르거나
    except pl.GlobalStop:
        pass                                                     # 고를 행이 없거나 — 어느 쪽도 #1 이 아니다
    with pytest.raises(pl.GlobalStop):
        pl.require_cell(res)


def test_10_the_preserved_util_copy_loads_by_path_after_its_sha_and_static_check():
    mod, path = pl.load_util(pl.UTIL_COPY, pl.UTIL_COPY_SHA)
    assert callable(mod.objective_fun) and callable(mod.dVdQ_hc) and Path(path).name == "util_LFP.py.txt"
    with pytest.raises(pl.GlobalStop):
        pl.load_util(pl.UTIL_COPY, "0" * 64)
