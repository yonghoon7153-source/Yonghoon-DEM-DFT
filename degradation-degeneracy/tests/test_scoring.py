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


def _r(p, J, i, source="random"):
    """restart 한 개. source는 warm / base_init / random 중 하나 (F31)."""
    return {"p": p, "J": J, "i": i, "source": source, "warm": source == "warm"}


def test_skip_first_removes_warm_start_artifact():
    """★ F21b — warm start 지점이 flat_valley 관측을 가리는 것을 보정한다.

    warm 지점만 최적이고 무작위들이 제각각이면 그대로는 항상 multimodal로 찍힌다.
    무작위끼리만 보면 그중 둘이 같은 J·다른 해라는 사실이 드러난다.

    ★ F25 — 저장 순서는 **J 오름차순**이라 위치로 warm을 찾으면 안 된다.
      아래 목록도 J순으로 두되 warm 플래그는 그것과 무관하게 붙인다.
    """
    import pandas as pd

    from src.scoring import multistart_diagnostics

    restarts = [                                  # J 오름차순 = 저장 순서
        _r([1.00, 0.00, 1.00, 0.00], 0.0, i=0, source="warm"),   # warm (유일한 최적)
        _r([1.20, -0.30, 1.05, -0.05], 0.5, i=2),            # 이 둘은 J가 같고
        _r([1.05, -0.05, 1.20, -0.30], 0.5, i=1),            # 해가 멀다 = flat valley
        _r([1.40, 0.20, 1.40, 0.20], 0.9, i=3),
        _r([0.80, -0.50, 0.80, -0.50], 1.3, i=4),
    ]
    df = pd.DataFrame([_warm_row("pocv_dvdq_dqdv", restarts)])

    with_warm = multistart_diagnostics(df)
    assert with_warm["multistart_kind"].iloc[0] == "multimodal"
    assert with_warm["n_near_J"].iloc[0] == 1

    random_only = multistart_diagnostics(df, skip_first=True)
    assert random_only["multistart_kind"].iloc[0] == "flat_valley", \
        "warm 지점을 빼면 같은 J·다른 해가 보여야 한다"
    assert random_only["n_near_J"].iloc[0] == 2
    assert bool(random_only["random_only"].iloc[0])
    assert int(random_only["n_nonrandom_dropped"].iloc[0]) == 1


def test_warm_is_found_by_flag_not_position():
    """★ F25 — warm이 J순 정렬 때문에 목록 중간에 있어도 그것만 빠져야 한다.

    위치로 골랐던 옛 구현은 여기서 best restart를 버려, 남은 것들이 우연히
    flat_valley로 보이거나 J_best가 엉뚱하게 커진다.
    """
    import pandas as pd

    from src.scoring import multistart_diagnostics

    restarts = [
        _r([1.00, 0.00, 1.00, 0.00], 0.0, i=3),              # best (무작위)
        _r([1.30, -0.30, 1.30, -0.30], 0.5, i=0, source="warm"),  # warm — 중간에 있다
        _r([1.31, -0.31, 1.31, -0.31], 0.5, i=1),
    ]
    df = pd.DataFrame([_warm_row("pocv_dvdq_dqdv", restarts)])

    out = multistart_diagnostics(df, skip_first=True)
    assert out["n_restarts_total"].iloc[0] == 2
    assert out["J_best"].iloc[0] == 0.0, \
        "warm이 아니라 best restart를 버렸다 (F25가 고친 바로 그 버그)"


def test_legacy_restarts_are_not_silently_corrected(caplog):
    """★ F25 — 출처 없는 옛 형식은 보정을 **생략**하고 경고해야 한다.

    위치로 추정하면 조용히 틀린 값이 나온다. 못 하는 건 못 한다고 해야 한다.
    """
    import logging

    import pandas as pd

    from src.scoring import multistart_diagnostics

    legacy = [([1.0, 0, 1.0, 0], 0.0), ([1.2, 0, 1.2, 0], 0.5), ([1.4, 0, 1.4, 0], 0.9)]
    df = pd.DataFrame([_warm_row("x", legacy)])

    with caplog.at_level(logging.WARNING):
        out = multistart_diagnostics(df, skip_first=True)
    assert out["n_restarts_total"].iloc[0] == 3, "옛 형식에서는 아무것도 버리면 안 된다"
    assert not bool(out["random_only"].iloc[0])
    assert "F25" in caplog.text


def test_too_few_restarts_after_dropping_nonrandom():
    """무작위가 아닌 것을 빼고 나서 비교할 게 1개뿐이면 제외."""
    import pandas as pd

    from src.scoring import multistart_diagnostics

    df = pd.DataFrame([_warm_row("x", [_r([1.0, 0, 1.0, 0], 0.0, 0, source="warm"),
                                       _r([1.1, 0, 1.1, 0], 0.4, 1)])])
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


# ---------------------------------------------------------------- F27 행별 복원가능성

def test_recoverability_is_row_wise_not_frame_wise():
    """★ F27 — halfcell 행이 섞여도 grid 행의 판정이 바뀌면 안 된다.

    예전에는 `(reference != "grid").any()`로 프레임 전체를 봐서, halfcell이
    한 줄만 섞여도 grid 행까지 전부 복원가능이 됐다. 비교표의 분모가 소리 없이
    늘어나는 실패라 눈으로는 못 잡는다.
    """
    import pandas as pd

    from src.scoring import classify_recoverability

    # lam=0.3, r=1.0 → alpha_true = 0.7 < 1 → grid 기준에서 복원 불가
    rows = [{"reference": "grid", "lam_pe": 0.3, "lam_ne": 0.0, "r": 1.0},
            {"reference": "halfcell", "lam_pe": 0.3, "lam_ne": 0.0, "r": 1.0}]

    only_grid = classify_recoverability(pd.DataFrame(rows[:1]))
    mixed = classify_recoverability(pd.DataFrame(rows))

    assert not bool(only_grid["recoverable"].iloc[0])
    assert not bool(mixed["recoverable"].iloc[0]), \
        "halfcell 행이 섞였다고 grid 행이 복원가능으로 바뀌었다"
    assert bool(mixed["recoverable"].iloc[1])
    # halfcell의 True는 측정이 아니라 가정이라는 사실이 열로 남아야 한다
    assert bool(mixed["recoverable_measured"].iloc[0])
    assert not bool(mixed["recoverable_measured"].iloc[1])


# ---------------------------------------------------------------- F30 provenance

def test_manifest_records_reproducibility_and_flags_dirty(tmp_path, monkeypatch):
    """★ F30 — `git_dirty: true`만 적힌 manifest는 provenance가 아니다.

    커밋된 grid_fine_v2·halfcell_v1이 `config_hash: ''` + dirty였다. parquet은
    재집계할 수 있어도 그 숫자를 만든 코드가 남아 있지 않다.
    """
    import src.io as IO

    monkeypatch.setattr(IO, "git_info",
                        lambda *a, **k: {"git_commit": "abc", "git_dirty": True})
    m = IO.base_manifest("", out_dir=tmp_path)
    assert m["reproducible"] is False
    assert "_주의" in m and "clean commit" in m["_주의"]

    monkeypatch.setattr(IO, "git_info",
                        lambda *a, **k: {"git_commit": "abc", "git_dirty": False})
    m2 = IO.base_manifest("deadbeef", out_dir=tmp_path)
    assert m2["reproducible"] is True
    assert "_주의" not in m2


def test_git_info_saves_dirty_diff(tmp_path):
    """dirty면 diff를 파일로 남겨야 재현이 가능하다."""
    import subprocess

    from src.io import git_info

    repo = tmp_path / "r"
    repo.mkdir()
    for cmd in (["git", "init", "-q"], ["git", "config", "user.email", "t@t"],
                ["git", "config", "user.name", "t"]):
        subprocess.run(cmd, cwd=repo, check=True, capture_output=True)
    (repo / "a.txt").write_text("one\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "i"], cwd=repo, check=True, capture_output=True)
    (repo / "a.txt").write_text("two\n")          # dirty로 만든다

    out = tmp_path / "run" / "run_dirty.patch"
    info = git_info(repo, save_diff_to=out)
    assert info["git_dirty"] is True
    assert out.exists() and "two" in out.read_text()
    assert info["git_dirty_diff"] == "run_dirty.patch"


def test_file_digest_changes_with_content(tmp_path):
    from src.io import file_digest

    p = tmp_path / "x.bin"
    p.write_bytes(b"a")
    d1 = file_digest(p)
    p.write_bytes(b"b")
    assert d1 != file_digest(p)
    assert file_digest(tmp_path / "missing") is None


def test_dirty_ignores_unrelated_untracked_files(tmp_path):
    """★ F30 — untracked 파일 때문에 모든 실행이 dirty로 찍히면 안 된다.

    재현을 막는 건 **추적 중인 파일의 수정**이다. 저장소 루트에 다른 프로젝트
    산출물이 널려 있다고 해서 이 실행이 재현 불가능해지는 건 아니다.
    (실측: 사용자 저장소 루트에 untracked 20여 개가 상시 존재)
    """
    import subprocess

    from src.io import git_info

    repo = tmp_path / "r"
    repo.mkdir()
    for cmd in (["git", "init", "-q"], ["git", "config", "user.email", "t@t"],
                ["git", "config", "user.name", "t"]):
        subprocess.run(cmd, cwd=repo, check=True, capture_output=True)
    (repo / "a.txt").write_text("one\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "i"], cwd=repo, check=True, capture_output=True)

    (repo / "unrelated.zip").write_bytes(b"x")      # 다른 프로젝트 산출물
    info = git_info(repo)
    assert info["git_dirty"] is False, "untracked 파일이 dirty로 잡혔다"
    assert info["git_untracked_count"] == 1         # 정보로는 남는다

    (repo / "a.txt").write_text("two\n")            # 추적 파일 수정
    assert git_info(repo)["git_dirty"] is True


def test_random_only_excludes_deterministic_base_init():
    """★ F31 — restart 0은 warm이 아니어도 무작위가 아니다.

    warm만 제거하면 warm을 받은 목적함수는 restart 0이 빠지고, 안 받은
    목적함수는 공통 결정론적 초기값(base_init)이 그대로 남는다. 비교하는
    restart 집합의 성격이 목적함수마다 달라져 "무작위끼리만"이 성립하지 않는다.
    """
    import pandas as pd

    from src.scoring import multistart_diagnostics

    # warm을 안 받은 목적함수: restart 0이 base_init
    cold = [_r([1.00, 0.0, 1.00, 0.0], 0.0, i=0, source="base_init"),
            _r([1.20, -0.2, 1.20, -0.2], 0.5, i=1),
            _r([1.21, -0.21, 1.21, -0.21], 0.5, i=2)]
    df = pd.DataFrame([_warm_row("pocv_dvdq", cold)])

    out = multistart_diagnostics(df, skip_first=True)
    assert out["n_restarts_total"].iloc[0] == 2, "base_init이 남았다 (F31)"
    assert int(out["n_nonrandom_dropped"].iloc[0]) == 1
    assert out["J_best"].iloc[0] == 0.5, "base_init의 J가 최적으로 남아 있다"


def test_random_only_flags_unequal_restart_counts(tmp_path):
    """★ F31 — 목적함수마다 남은 무작위 restart 수가 다르면 비교 불가로 표시."""
    import json

    import pandas as pd
    import yaml

    from src.scoring import run_scoring

    def row(cond, obj, n_rand):
        rs = [_r([1.0, 0.0, 1.0, 0.0], 0.0, i=0, source="warm")]
        rs += [_r([1.0 + 0.1 * k, 0.0, 1.0, 0.0], 0.5, i=k) for k in range(1, n_rand + 1)]
        return {"cond_id": cond, "objective": obj, "noise": 0.0,
                "lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0,
                "lli_hat": 0.0, "lam_pe_hat": 0.0, "lam_ne_hat": 0.0,
                "r": 1.0, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
                "restarts_json": json.dumps(rs)}

    # A는 무작위 4개, B는 2개 — adaptive 조기 종료가 만드는 상황
    df = pd.DataFrame([row(f"c{i}", "A", 4) for i in range(3)]
                      + [row(f"d{i}", "B", 2) for i in range(3)])
    df.to_parquet(tmp_path / "fits.parquet", index=False)

    run_scoring(tmp_path)
    s = yaml.safe_load((tmp_path / "degeneracy_summary.yaml").read_text(encoding="utf-8"))
    blk = s["multistart_random_only"]
    assert blk["random_only_적용"] is True
    assert blk["비교가능"] is False, "restart 수가 2배 차이인데 비교가능으로 나왔다"
    assert "검정력" in blk["_주의"]


def test_random_only_requires_matched_condition_sets(tmp_path):
    """★ F40 — 평균 restart 수가 같아도 조건 집합이 다르면 비교 불가.

    adaptive 조기 종료로 탈락하는 cond_id가 목적함수마다 다르다. 평균만 보면
    **완전히 겹치지 않는 두 모집단**도 "비교가능"으로 통과한다.
    """
    import json

    import pandas as pd
    import yaml

    from src.scoring import run_scoring

    def row(cond, obj, n_rand):
        rs = [_r([1.0, 0.0, 1.0, 0.0], 0.0, i=0, source="warm")]
        rs += [_r([1.0 + 0.1 * k, 0.0, 1.0, 0.0], 0.5, i=k)
               for k in range(1, n_rand + 1)]
        return {"cond_id": cond, "objective": obj, "noise": 0.0,
                "lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0,
                "lli_hat": 0.0, "lam_pe_hat": 0.0, "lam_ne_hat": 0.0,
                "r": 1.0, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
                "restarts_json": json.dumps(rs)}

    # 평균 restart 수는 똑같이 3인데 cond_id가 전혀 겹치지 않는다
    df = pd.DataFrame([row(f"a{i}", "A", 3) for i in range(5)]
                      + [row(f"b{i}", "B", 3) for i in range(5)])
    df.to_parquet(tmp_path / "fits.parquet", index=False)

    run_scoring(tmp_path)
    blk = yaml.safe_load(
        (tmp_path / "degeneracy_summary.yaml").read_text(encoding="utf-8")
    )["multistart_random_only"]

    assert blk["n_common_conditions"] == 0, "겹치는 조건이 없어야 유효한 테스트"
    assert blk["비교가능"] is False, \
        "조건 집합이 전혀 안 겹치는데 비교가능으로 통과했다 (F40)"
    assert "제외율_목적함수별" in blk


def test_paired_subset_declares_its_selection_bias(tmp_path):
    """★ F41 — paired subset은 결과(최적화 난이도)로 선택된 집합이다.

    조기 종료를 겪은 조건이 탈락하므로 "모두에게 어려웠던 조건"만 남는다.
    그 사실이 요약에 남아야 격자 전체로 일반화하는 오독을 막는다.
    """
    import json

    import pandas as pd
    import yaml

    from src.scoring import run_scoring

    def row(cond, obj, n_rand):
        rs = [_r([1.0, 0.0, 1.0, 0.0], 0.0, i=0, source="warm")]
        rs += [_r([1.0 + 0.1 * k, 0.0, 1.0, 0.0], 0.5, i=k)
               for k in range(1, n_rand + 1)]
        return {"cond_id": cond, "objective": obj, "noise": 0.0,
                "lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0,
                "lli_hat": 0.0, "lam_pe_hat": 0.0, "lam_ne_hat": 0.0,
                "r": 1.0, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
                "restarts_json": json.dumps(rs)}

    # A는 전 조건이 끝까지 가고, B는 절반이 조기 종료(무작위 1개 → 탈락)
    rows = []
    for i in range(40):
        rows.append(row(f"c{i}", "A", 4))
        rows.append(row(f"c{i}", "B", 4 if i < 20 else 1))
    pd.DataFrame(rows).to_parquet(tmp_path / "fits.parquet", index=False)

    run_scoring(tmp_path)
    blk = yaml.safe_load(
        (tmp_path / "degeneracy_summary.yaml").read_text(encoding="utf-8")
    )["multistart_random_only"]

    assert blk["n_paired_conditions"] == 20
    assert "_선택편향" in blk and "무작위 표본이 아니다" in blk["_선택편향"]
    # 제외율이 목적함수마다 다르다는 사실 자체가 경고문에 들어가야 한다
    assert blk["제외율_목적함수별"]["A"] != blk["제외율_목적함수별"]["B"]
