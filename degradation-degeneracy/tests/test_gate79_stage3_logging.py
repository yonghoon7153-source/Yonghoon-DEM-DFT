"""79차 — 단계 3 계약 §11 의 제한 오프라인 구현 **단계 2** (78차 회신 수정 조건부 적합 · 사용자 승인 2026-09-27).

범위 (그 밖은 하지 않는다):
  (a) restart 행에 `converged` · `termination_status` · restart 별 `n_eval` 을 **추가** 한다 — 기존 optimizer
      초기값·후보 선택·횟수·tolerance·J/p·scoring 정의는 바꾸지 않는다 (수치 불변 골든이 그것을 고정한다).
  (b) `termination_status` 는 solver 의 **native** 종료(마지막 round · best round 를 따로) 와
      `_minimize_until_stable` **바깥 반복** 의 종료 사유를 구별한다. 기존 `converged` 의 뜻(그 restart 의 마지막
      round `res.success`)은 조용히 바꾸지 않는다 — 시험이 그 의미를 못 박는다.
  (c) 예외로 실패한 restart 는 `restarts` 에서 여전히 빠지지만(기존 동작·`n_restarts` 불변) `restart_errors` 에
      index·source·오류를 남기고 fits 행에 `restart_errors_json` 으로 실린다.
  (d) `validate_provenance` 가 깨진 parquet 을 예외로 올리지 않고 `fail` 항목으로 보고한다 (계약 §9.4).
  (e) 역사적 reader: 옛 restart 기록(튜플 · 새 키 없는 dict)의 부재 필드는 **미기록(None)** 이다 — false/0 으로
      소급 채우지 않는다.

이 파일은 패치 전 (a)(b)(c)(d)(e) 가 RED, 수치 불변 골든(g79_02)만 GREEN 이어야 한다 — 골든은 변경 **전** 코드
(16d97ce6)에서 잡은 값이라 처음부터 통과하는 것이 맞다 (fixture 감사: 그것이 이 시험의 목적이다).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from src import fitting as F                                   # noqa: E402
from src.io import validate_curves_provenance, validate_provenance   # noqa: E402


def _obj(p):
    p = np.asarray(p, float)
    return float((p[0] - 1.3) ** 2 + 10 * (p[1] - 0.2) ** 2 + (p[2] - 0.9) ** 4
                 + np.sin(3 * p[0]) * 0.1 + (p[3] + 0.1) ** 2)


_INIT, _LB, _UB = [1.0, 0.0, 1.0, 0.0], [0.5, -1, 0.5, -1], [2, 1, 2, 1]

# 변경 **전** 코드(16d97ce6)에서 잡은 골든 — restart 순서(J 오름차순)·p·J·n_eval·agree·spread 전부.
_GOLDEN = {
    False: {"p": [1.3809040070171776, 0.19999999901730184, 0.9000143461631405, -0.09999999944396251],
            "J": -0.07766206708133525, "converged": True, "n_eval": 2316, "n_restarts": 3, "agree": 3,
            "p_spread": 7.92498585538981e-05, "J_spread": 1.3877787807814457e-17,
            "restarts": [
                {"p": [1.3809040070171776, 0.19999999901730184, 0.9000143461631405, -0.09999999944396251], "J": -0.07766206708133525, "i": 1, "source": "random", "warm": False},
                {"p": [1.3809040067493972, 0.2000000001604931, 0.8999900642053585, -0.09999999946553742], "J": -0.07766206708133525, "i": 2, "source": "random", "warm": False},
                {"p": [1.3809040068277434, 0.2000000000888424, 0.8999350963045866, -0.09999999948012947], "J": -0.07766206708133523, "i": 0, "source": "base_init", "warm": False}]},
    True: {"p": [1.3809040070171776, 0.19999999901730184, 0.9000143461631405, -0.09999999944396251],
           "J": -0.07766206708133525, "converged": True, "n_eval": 1562, "n_restarts": 2, "agree": 2,
           "p_spread": 7.92498585538981e-05, "J_spread": 1.3877787807814457e-17,
           "restarts": [
               {"p": [1.3809040070171776, 0.19999999901730184, 0.9000143461631405, -0.09999999944396251], "J": -0.07766206708133525, "i": 1, "source": "random", "warm": False},
               {"p": [1.3809040068277434, 0.2000000000888424, 0.8999350963045866, -0.09999999948012947], "J": -0.07766206708133523, "i": 0, "source": "base_init", "warm": False}]},
}

_OUTER = {"no_improvement", "nonfinite", "max_rounds"}
_NATIVE_KEYS = {"status", "success", "message", "nfev", "nit"}


# ─────────────────────────────────────────────────────────────────────────────
# (a)(b) restart 행 필드
# ─────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("adaptive", [False, True])
def test_g79_01_each_restart_carries_converged_n_eval_and_a_two_level_termination_status(adaptive):
    r = F.fit(_obj, _INIT, _LB, _UB, n_restarts=3, seed=7, adaptive=adaptive)
    assert r.restarts, "restart 기록이 없다"
    for e in r.restarts:
        assert isinstance(e.get("converged"), bool), e
        assert isinstance(e.get("n_eval"), int) and e["n_eval"] >= 1, e
        ts = e.get("termination_status")
        assert isinstance(ts, dict), e
        assert ts.get("outer") in _OUTER, ts
        assert isinstance(ts.get("n_rounds"), int) and ts["n_rounds"] >= 1, ts
        for k in ("native_last", "native_best"):
            assert isinstance(ts.get(k), dict) and _NATIVE_KEYS <= set(ts[k]), (k, ts)
            assert isinstance(ts[k]["status"], int) and isinstance(ts[k]["success"], bool), ts
    # restart 별 n_eval 의 합 = FitResult.n_eval (리뷰 F17 의 합계와 같은 자리에서 나온다)
    assert sum(e["n_eval"] for e in r.restarts) == r.n_eval
    # best restart(정렬 뒤 첫 원소) 의 converged = FitResult.converged — 뜻을 바꾸지 않았다
    assert r.restarts[0]["converged"] == r.converged
    # JSON 직렬화 가능 (fits 행의 restarts_json)
    json.dumps(r.restarts)


@pytest.mark.parametrize("adaptive", [False, True])
def test_g79_02_numerical_behaviour_is_unchanged_against_the_pre_change_golden(adaptive):
    """★ 수치 불변 — 변경 전 코드(16d97ce6)의 골든과 **정확히** 같다 (부동소수 동일). 처음부터 GREEN 이 정상."""
    g = _GOLDEN[adaptive]
    r = F.fit(_obj, _INIT, _LB, _UB, n_restarts=3, seed=7, adaptive=adaptive)
    assert r.p.tolist() == g["p"] and r.J == g["J"]
    assert (r.converged, r.n_eval, r.n_restarts, r.n_restarts_agree) == (g["converged"], g["n_eval"], g["n_restarts"], g["agree"])
    assert (r.p_spread, r.J_spread) == (g["p_spread"], g["J_spread"])
    got = [{k: e[k] for k in ("p", "J", "i", "source", "warm")} for e in r.restarts]
    assert got == g["restarts"], "restart 순서·p·J·출처가 골든과 다르다 — 수치 동작이 바뀌었다"


def test_g79_03_native_best_and_native_last_are_distinguished_and_converged_keeps_its_old_meaning(monkeypatch):
    """best round ≠ last round 인 상황을 가짜 minimize 로 만든다: round 1 이 best(status 0·success),
    round 2 가 더 나쁨(status 1·실패) → 개선 없음으로 바깥 반복 종료. 기존 `converged` = 마지막 round 의 success (False)."""
    from scipy.optimize import OptimizeResult
    calls = []

    def fake_minimize(objective, x0, method=None, bounds=None, options=None):
        calls.append(np.asarray(x0, float).copy())
        if len(calls) == 1:
            return OptimizeResult(x=np.asarray(x0, float) + 0.01, fun=1.0, success=True, status=0,
                                  message="ok", nfev=10, nit=3)
        return OptimizeResult(x=np.asarray(x0, float) + 0.02, fun=1.5, success=False, status=1,
                              message="max iter", nfev=7, nit=2)

    monkeypatch.setattr(F, "minimize", fake_minimize)
    x, f, ok, nfev, term = F._minimize_until_stable(lambda p: 0.0, [1.0, 0.0, 1.0, 0.0],
                                                    list(zip(_LB, _UB)), "Nelder-Mead")
    assert f == 1.0 and nfev == 17
    assert ok is False, "기존 의미: converged 는 마지막 round 의 success 다 — 바뀌었다"
    assert term["outer"] == "no_improvement" and term["n_rounds"] == 2
    assert term["native_best"]["status"] == 0 and term["native_best"]["success"] is True and term["native_best"]["nfev"] == 10
    assert term["native_last"]["status"] == 1 and term["native_last"]["success"] is False and term["native_last"]["nfev"] == 7


def test_g79_03b_outer_stop_reasons_are_named(monkeypatch):
    from scipy.optimize import OptimizeResult

    def nonfinite(objective, x0, method=None, bounds=None, options=None):
        return OptimizeResult(x=np.asarray(x0, float), fun=float("nan"), success=False, status=2, message="nan", nfev=3, nit=1)
    monkeypatch.setattr(F, "minimize", nonfinite)
    *_, term = F._minimize_until_stable(lambda p: 0.0, _INIT, list(zip(_LB, _UB)), "Nelder-Mead")
    assert term["outer"] == "nonfinite" and term["n_rounds"] == 1 and term["native_best"] is None

    k = {"n": 0}

    def always_improving(objective, x0, method=None, bounds=None, options=None):
        k["n"] += 1
        return OptimizeResult(x=np.asarray(x0, float), fun=10.0 - k["n"], success=True, status=0, message="ok", nfev=1, nit=1)
    monkeypatch.setattr(F, "minimize", always_improving)
    *_, term = F._minimize_until_stable(lambda p: 0.0, _INIT, list(zip(_LB, _UB)), "Nelder-Mead", max_rounds=3)
    assert term["outer"] == "max_rounds" and term["n_rounds"] == 3


# ─────────────────────────────────────────────────────────────────────────────
# (c) 실패한 restart 의 기록
# ─────────────────────────────────────────────────────────────────────────────
def test_g79_04_a_failed_restart_is_recorded_without_changing_the_surviving_set(monkeypatch):
    real = F._minimize_until_stable

    def flaky(objective, x0, bounds, method, **kw):
        if not np.allclose(np.asarray(x0, float), _INIT):      # k ≥ 1 (random) 중 첫 호출만 실패
            if not flaky.done:
                flaky.done = True
                raise RuntimeError("injected restart failure")
        return real(objective, x0, bounds, method, **kw)
    flaky.done = False
    monkeypatch.setattr(F, "_minimize_until_stable", flaky)
    r = F.fit(_obj, _INIT, _LB, _UB, n_restarts=3, seed=7, adaptive=True)
    assert r.n_restarts == len(r.restarts) == 2, "살아남은 집합의 뜻(n_restarts = 성공한 restart 수)이 바뀌었다"
    assert {e["i"] for e in r.restarts} == {0, 2}
    assert r.restart_errors == [{"i": 1, "source": "random", "error": "RuntimeError: injected restart failure"}]
    json.dumps(r.restart_errors)


def test_g79_04b_adaptive_false_still_raises_on_a_failed_restart(monkeypatch):
    """F86 공정 모드의 즉시 실패는 그대로다 — 기록 추가가 그 정책을 완화하지 않는다."""
    def boom(objective, x0, bounds, method, **kw):
        if not np.allclose(np.asarray(x0, float), _INIT):
            raise RuntimeError("injected")
        return F.__dict__["_minimize_until_stable_orig"](objective, x0, bounds, method, **kw)
    F.__dict__["_minimize_until_stable_orig"] = F._minimize_until_stable
    monkeypatch.setattr(F, "_minimize_until_stable", boom)
    with pytest.raises(RuntimeError, match="F86"):
        F.fit(_obj, _INIT, _LB, _UB, n_restarts=3, seed=7, adaptive=False)


def test_g79_04c_run_fit_writes_restart_errors_json_and_the_new_restart_keys(tmp_path):
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False)
    f = pd.read_parquet(out / "fits.parquet")
    assert "restart_errors_json" in f.columns
    assert all(json.loads(v) == [] for v in f["restart_errors_json"])
    for v in f["restarts_json"]:
        for e in json.loads(v):
            assert {"converged", "n_eval", "termination_status"} <= set(e), e
    # 기존 검증기는 새 키를 가진 행을 그대로 받는다 (restart_출처 검사 · 예산 완주 검사)
    v = validate_provenance(out)
    assert v["checks"]["restart_출처"] == "통과" and v["checks"]["restart_예산_완주"] == "통과", v["checks"]


# ─────────────────────────────────────────────────────────────────────────────
# (d) 깨진 parquet 은 예외가 아니라 발견이다
# ─────────────────────────────────────────────────────────────────────────────
def test_g79_05_a_corrupt_fits_parquet_is_reported_as_a_failed_check_not_raised(tmp_path):
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False)
    (out / "fits.parquet").write_bytes(b"PAR1 this is not a parquet file")
    v = validate_provenance(out)                      # 예외를 올리면 여기서 죽는다
    assert v["ok"] is False
    assert any("읽" in v["checks"][k] for k in v["fail"]), v["fail"]
    assert isinstance(v["fail"], list) and isinstance(v["reasons"], list)


def test_g79_05b_a_corrupt_curves_parquet_is_reported_as_a_failed_check_not_raised(tmp_path):
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    (in_dir / "curves.parquet").write_bytes(b"PAR1 broken")
    v = validate_curves_provenance(in_dir)
    assert v["ok"] is False
    assert any("읽" in v["checks"][k] for k in v["fail"]), v["fail"]


# ─────────────────────────────────────────────────────────────────────────────
# (e) 역사적 reader — 부재는 미기록이다
# ─────────────────────────────────────────────────────────────────────────────
def test_g79_06_historical_restart_records_report_absent_fields_as_unrecorded_not_false_or_zero():
    old_tuple = [[1.0, 0.0, 1.0, 0.0], 0.5]
    old_dict = {"p": [1.0, 0.0, 1.0, 0.0], "J": 0.5, "i": 0, "source": "base_init", "warm": False}
    new = {**old_dict, "converged": True, "n_eval": 12,
           "termination_status": {"outer": "no_improvement", "n_rounds": 1,
                                  "native_last": {"status": 0, "success": True, "message": "ok", "nfev": 12, "nit": 3},
                                  "native_best": {"status": 0, "success": True, "message": "ok", "nfev": 12, "nit": 3}}}
    a, b, c = (F.normalize_restart_record(x) for x in (old_tuple, old_dict, new))
    assert a["record_generation"] == "legacy_pair" and b["record_generation"] == "legacy_dict" and c["record_generation"] == "v6_prep_logging"
    for r in (a, b):
        assert r["converged"] is None and r["n_eval"] is None and r["termination_status"] is None
    assert a["source"] is None and a["i"] is None and b["source"] == "base_init"
    assert c["converged"] is True and c["n_eval"] == 12 and c["termination_status"]["outer"] == "no_improvement"
    assert a["p"] == [1.0, 0.0, 1.0, 0.0] and a["J"] == 0.5


def test_g79_07_the_pinned_projection_parser_and_the_validator_accept_the_new_keys():
    """row_projection.py 는 봉인 pin 이라 고치지 않는다 — 새 키를 가진 행을 지금 그대로 받는지 확인한다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("_rp_g79", REPO / "docs" / "22p_gap" / "row_projection.py")
    rp = importlib.util.module_from_spec(spec); spec.loader.exec_module(rp)
    from src.io import _restart_ok
    e = {"p": [1.0, 0.0, 1.0, 0.0], "J": 0.5, "i": 0, "source": "base_init", "warm": False,
         "converged": True, "n_eval": 3, "termination_status": {"outer": "max_rounds", "n_rounds": 4,
                                                                "native_last": {"status": 0, "success": True, "message": "", "nfev": 3, "nit": 1},
                                                                "native_best": {"status": 0, "success": True, "message": "", "nfev": 3, "nit": 1}}}
    assert rp._restart_list(json.dumps([e])) == [e]
    assert _restart_ok(e) is True
