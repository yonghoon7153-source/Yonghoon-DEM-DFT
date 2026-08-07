"""scoring / hessian 검증 — 리뷰 규칙이 코드에 실제로 박혀 있는지 고정한다."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.scoring import (add_error_columns, apply_bias_correction, classify_recoverability,
                         clean_bias, score, summarize)


def _frame(**kw) -> pd.DataFrame:
    n = len(next(iter(kw.values())))
    base = {"objective": ["pocv_dvdq"] * n, "noise": [0.0] * n,
            "r": [0.9] * n, "a_pe": [1.05] * n, "a_ne": [1.05] * n,
            "reference": ["grid"] * n}
    base.update(kw)
    return pd.DataFrame(base)


def test_score_basic_and_antisym():
    s = score({"lli": 0.1, "lam_pe": 0.1, "lam_ne": 0.1},
              {"lli": 0.1, "lam_pe": 0.15, "lam_ne": 0.05})
    assert s["err_lam_pe"] == pytest.approx(0.05)
    assert s["err_lam_ne"] == pytest.approx(-0.05)
    assert s["pe_ne_antisym"] is True        # ★ 상쇄 = degeneracy 지문
    assert s["abs_err_max"] == pytest.approx(0.05)
    assert s["degenerate"] is True           # 0.05 > 0.02


def test_score_not_degenerate_within_tol():
    s = score({"lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0},
              {"lli": 0.01, "lam_pe": 0.005, "lam_ne": 0.005})
    assert s["degenerate"] is False
    assert s["pe_ne_antisym"] is False


def test_recoverability_flags_alpha_below_one():
    """★ F1: 참값 α=(1−LAM)/r < 1 이면 원리적 복원 불가로 분류돼야 한다."""
    df = _frame(lli=[0.0, 0.0], lam_pe=[0.0, 0.20], lam_ne=[0.0, 0.0],
                lli_hat=[0.0, 0.0], lam_pe_hat=[0.0, 0.0], lam_ne_hat=[0.0, 0.0],
                r=[1.0, 0.95])
    out = classify_recoverability(df)
    # 1행: α=1/1.0=1.0 → 복원가능 / 2행: α=0.8/0.95=0.842 <1 → 불가
    assert bool(out["recoverable"].iloc[0]) is True
    assert bool(out["recoverable"].iloc[1]) is False
    assert out["alpha_true_pe"].iloc[1] == pytest.approx(0.8 / 0.95)


def test_halfcell_reference_has_no_alpha_wall():
    """halfcell 기준은 전 범위 테이블이라 α<1 벽이 없다 → 전부 복원가능."""
    df = _frame(lli=[0.0], lam_pe=[0.20], lam_ne=[0.0], lli_hat=[0.0],
                lam_pe_hat=[0.0], lam_ne_hat=[0.0], r=[0.95])
    df["reference"] = "halfcell"
    assert bool(classify_recoverability(df)["recoverable"].iloc[0]) is True


def test_clean_bias_and_correction():
    """★ F5: 노이즈0 조건의 평균 오차를 방법 바이어스로 빼면 잔차가 준다."""
    df = _frame(lli=[0.0] * 4, lam_pe=[0.0] * 4, lam_ne=[0.0] * 4,
                lli_hat=[0.0] * 4, lam_ne_hat=[0.0] * 4,
                lam_pe_hat=[0.03, 0.03, 0.03, 0.03])   # 일정한 +3%p 편향
    df = classify_recoverability(add_error_columns(df))
    bias = clean_bias(df)
    assert bias["bias_err_lam_pe"].iloc[0] == pytest.approx(0.03)

    out = apply_bias_correction(df, bias)
    assert out["degenerate"].all()                     # 원래 판정은 degenerate
    assert not out["degenerate_corrected"].any()       # 보정하면 아님
    assert out["abs_resid_max"].max() == pytest.approx(0.0, abs=1e-12)


def test_summarize_reports_review_caveats():
    df = _frame(lli=[0.0, 0.2], lam_pe=[0.0, 0.02], lam_ne=[0.0, 0.02],
                lli_hat=[0.0, 0.25], lam_pe_hat=[0.0, 0.02], lam_ne_hat=[0.0, 0.02],
                n_restarts=[2, 5], n_restarts_agree=[2, 3], p_spread=[0.0, 0.1])
    df = classify_recoverability(add_error_columns(df))
    s = summarize(df)
    assert "by_objective" in s and "pocv_dvdq" in s["by_objective"]
    assert s["by_objective"]["pocv_dvdq"]["degenerate_frac"] == pytest.approx(0.5)
    # F4: restart 조건화 블록 + 경고문이 반드시 있어야 한다
    assert "restart_conditioned" in s and "_F4_주의" in s
    # F14: 커버리지 공백 명시
    assert "coverage_gap" in s and "_주의" in s["coverage_gap"]


def test_hessian_of_quadratic_is_exact():
    """해석적 검증: J = ½ pᵀ A p 이면 Hessian = A."""
    from src.hessian import eigen_analysis, numerical_hessian

    A = np.diag([4.0, 1.0, 0.01, 2.0])
    H = numerical_hessian(lambda p: 0.5 * float(np.asarray(p) @ A @ np.asarray(p)),
                          np.zeros(4), eps=1e-3)
    np.testing.assert_allclose(H, A, atol=1e-6)

    e = eigen_analysis(H)
    assert e["eigval_0"] == pytest.approx(0.01, rel=1e-6)
    assert e["condition_number"] == pytest.approx(400.0, rel=1e-5)
    assert e["flat_direction_score"] == pytest.approx(0.0025, rel=1e-5)
    assert e["min_eigval_positive"] is True


def test_eigen_analysis_detects_pe_ne_coupling():
    """★ 최소 고윳값 방향이 α_PE·α_NE를 같은 부호로 묶으면 감지돼야 한다.

    22p에서 LAM_PE ≈ LAM_NE가 나온 이유가 물리가 아니라 수학임을 보이는 지표.
    """
    from src.hessian import eigen_analysis

    v = np.array([1.0, 0.0, 1.0, 0.0]) / np.sqrt(2)     # a_pe·a_ne 동시 이동
    others = np.linalg.qr(np.column_stack([v, np.eye(4)[:, 1:]]))[0]
    H = others @ np.diag([0.001, 1.0, 1.0, 1.0]) @ others.T
    e = eigen_analysis(H)
    assert e["pe_ne_coupled"] is True
    assert abs(e["flat_vec_a_pe"]) > 0.3 and abs(e["flat_vec_a_ne"]) > 0.3


# ---------------------------------------------------------------- F21 multi-start

def _restart_row(cond, obj, restarts):
    import json
    return {"cond_id": cond, "objective": obj, "lli": 0.0, "lam_pe": 0.0,
            "lam_ne": 0.0, "noise": 0.0, "restarts_json": json.dumps(restarts)}


def test_multistart_flat_valley_is_same_J_different_p():
    """★ 같은 J에 서로 다른 해 = degeneracy의 직접 증거."""
    from src.scoring import multistart_diagnostics

    df = pd.DataFrame([_restart_row("c0", "pocv_dvdq", [
        ([1.00, 0.00, 1.00, 0.00], 0.010),
        ([1.20, -0.20, 0.80, 0.20], 0.010),      # J 같음, p 멀다
        ([0.90, 0.10, 1.10, -0.10], 0.010),
    ])])
    ms = multistart_diagnostics(df)
    r = ms.iloc[0]
    assert r["multistart_kind"] == "flat_valley"
    assert r["n_near_J"] == 3
    assert r["p_spread_near"] > 0.1


def test_multistart_multimodal_is_different_J():
    """J가 다른 국소최소 여럿 = 최적화 난이도이지 degeneracy가 아니다."""
    from src.scoring import multistart_diagnostics

    df = pd.DataFrame([_restart_row("c0", "pocv_dvdq_dqdv", [
        ([1.00, 0.00, 1.00, 0.00], 0.000),
        ([1.30, -0.30, 0.70, 0.30], 0.400),      # 훨씬 나쁜 J
        ([1.40, -0.40, 0.60, 0.40], 0.500),
    ])])
    ms = multistart_diagnostics(df)
    r = ms.iloc[0]
    assert r["multistart_kind"] == "multimodal"
    assert r["n_near_J"] == 1
    assert r["p_spread_all"] > 0.1


def test_multistart_unique_min():
    from src.scoring import multistart_diagnostics

    df = pd.DataFrame([_restart_row("c0", "pocv", [
        ([1.000, 0.000, 1.000, 0.000], 0.001),
        ([1.001, 0.001, 1.000, 0.000], 0.001),
    ])])
    assert multistart_diagnostics(df).iloc[0]["multistart_kind"] == "unique_min"


def test_multistart_summary_separates_the_two_failure_modes():
    """★ flat_valley와 multimodal을 뭉치면 처방이 반대가 된다."""
    from src.scoring import multistart_diagnostics, multistart_summary

    df = pd.DataFrame([
        _restart_row("c0", "A", [([1.0, 0, 1.0, 0], 0.01),
                                 ([1.3, -0.3, 0.7, 0.3], 0.01)]),   # flat
        _restart_row("c1", "A", [([1.0, 0, 1.0, 0], 0.01),
                                 ([1.3, -0.3, 0.7, 0.3], 0.01)]),   # flat
        _restart_row("c2", "B", [([1.0, 0, 1.0, 0], 0.00),
                                 ([1.3, -0.3, 0.7, 0.3], 0.50)]),   # multimodal
    ])
    s = multistart_summary(multistart_diagnostics(df))
    assert s["A"]["flat_valley_frac"] == 1.0
    assert s["A"]["multimodal_frac"] == 0.0
    assert s["B"]["multimodal_frac"] == 1.0
    assert s["B"]["flat_valley_frac"] == 0.0


def test_multistart_missing_column_is_graceful():
    from src.scoring import multistart_diagnostics

    assert multistart_diagnostics(pd.DataFrame({"cond_id": ["a"]})).empty


# ---------------------------------------------------------------- F21b warm start 보정

def _warm_row(objective, restarts):
    import json
    return {"cond_id": f"c_{objective}", "objective": objective, "recoverable": True,
            "lli": 0.1, "lam_pe": 0.1, "lam_ne": 0.1, "noise": 0.0,
            "restarts_json": json.dumps(restarts)}


def test_skip_first_removes_warm_start_artifact():
    """★ F21b — warm start 지점이 flat_valley 관측을 가리는 것을 보정한다.

    restart 0만 최적이고 1~4가 제각각이면, 그대로는 항상 multimodal로 찍힌다.
    무작위 restart끼리만 보면 그중 둘이 같은 J·다른 해라는 사실이 드러난다.
    """
    import pandas as pd

    from src.scoring import multistart_diagnostics

    restarts = [
        ([1.00, 0.00, 1.00, 0.00], 0.0),      # warm start 지점 (유일한 최적)
        ([1.20, -0.30, 1.05, -0.05], 0.5),    # 무작위 — 이 둘은 J가 같고
        ([1.05, -0.05, 1.20, -0.30], 0.5),    # 해가 멀다 = flat valley
        ([1.40, 0.20, 1.40, 0.20], 0.9),
        ([0.80, -0.50, 0.80, -0.50], 1.3),
    ]
    df = pd.DataFrame([_warm_row("pocv_dvdq_dqdv", restarts)])

    with_warm = multistart_diagnostics(df)
    assert with_warm["multistart_kind"].iloc[0] == "multimodal"
    assert with_warm["n_near_J"].iloc[0] == 1

    random_only = multistart_diagnostics(df, skip_first=True)
    assert random_only["multistart_kind"].iloc[0] == "flat_valley", \
        "restart 0을 빼면 같은 J·다른 해가 보여야 한다"
    assert random_only["n_near_J"].iloc[0] == 2


def test_skip_first_drops_rows_with_too_few_restarts():
    """restart가 2개뿐이면 0번을 빼고 나서 비교할 게 없다 → 제외."""
    import pandas as pd

    from src.scoring import multistart_diagnostics

    df = pd.DataFrame([_warm_row("x", [([1.0, 0, 1.0, 0], 0.0),
                                          ([1.1, 0, 1.1, 0], 0.4)])])
    assert multistart_diagnostics(df, skip_first=True).empty
    assert not multistart_diagnostics(df).empty


# ---------------------------------------------------------------- F24 lock 진입점

def test_run_entrypoints_cover_every_module_that_fits():
    """★ F24 — lock 판정 목록이 실제 진입점과 어긋나면 살아 있는 실행의 lock을
    stale로 오판해 지운다 → 같은 --out에 두 프로세스가 붙는다.

    2026-08-07 실측: src.weight_sweep이 빠져 있어서 sweep 위에 sweep이 겹쳤다.
    새 진입점을 만들면 이 테스트가 먼저 깨지게 둔다.
    """
    import pathlib

    from src.io import _RUN_ENTRYPOINTS

    root = pathlib.Path(__file__).resolve().parent.parent
    # run.sh가 `python -m <module>` 로 띄우는 모듈 = 계산 진입점
    launched = set()
    for line in (root / "run.sh").read_text(encoding="utf-8").splitlines():
        if "python -m src." in line:
            mod = line.split("python -m ")[1].split()[0]
            launched.add(mod)

    # fitting을 수행하는 것만 lock 대상 (baseline/sweep1d 등 단발성은 제외)
    need = {m for m in launched if m in {"src.grid", "src.fitting", "src.weight_sweep"}}
    missing = need - set(_RUN_ENTRYPOINTS)
    assert not missing, (
        f"run.sh가 띄우는데 _RUN_ENTRYPOINTS에 없는 모듈: {missing}. "
        f"이대로면 그 실행의 lock이 stale로 오판돼 동시 실행이 뚫린다.")


def test_pid_alive_recognises_weight_sweep(monkeypatch, tmp_path):
    """weight_sweep 프로세스를 '살아 있음'으로 인정해야 lock이 지켜진다."""
    import src.io as IO

    cmdline = tmp_path / "cmdline"
    cmdline.write_text("python\x00-m\x00src.weight_sweep\x00--in\x00results/x")

    class _P:
        def __init__(self, *a): pass
        def exists(self): return True
        def read_text(self, **kw): return cmdline.read_text()

    monkeypatch.setattr(IO.os, "kill", lambda *a: None)
    monkeypatch.setattr(IO, "Path", lambda *a: _P())
    assert IO._pid_alive(12345) is True
