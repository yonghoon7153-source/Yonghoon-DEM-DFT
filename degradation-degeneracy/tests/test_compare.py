"""Phase 6 — 목적함수 비교·가중치 sweep·보고서 생성 테스트."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.scoring import (add_error_columns, apply_bias_correction,
                         classify_recoverability, clean_bias)
from src.weight_sweep import (build_weight_objectives, obj_name, pick_optimum,
                              stratified_subset, sweep_summary)
from tools.compare_objectives import (comparison_table, to_markdown, verdict_22p)


def _fits(objectives=("pocv", "pocv_dvdq"), n_lli=3, seed=0, err_scale=0.05):
    """정답과 복원값이 있는 최소 fits 테이블. objective마다 오차 크기를 다르게."""
    rng = np.random.default_rng(seed)
    rows = []
    vals = np.round(np.linspace(0.0, 0.20, n_lli), 4)
    for oi, o in enumerate(objectives):
        # 뒤 objective일수록 정확 — "개선 효과"가 표에 나타나야 한다
        s = err_scale / (oi + 1)
        for lli in vals:
            for pe in vals:
                for ne in vals:
                    for noise in (0.0, 0.005):
                        e = rng.normal(0, s, 3)
                        rows.append({
                            "cond_id": f"c_{lli}_{pe}_{ne}_{noise}",
                            "objective": o, "noise": noise,
                            "lli": lli, "lam_pe": pe, "lam_ne": ne,
                            "lli_hat": lli + e[0], "lam_pe_hat": pe + e[1],
                            "lam_ne_hat": ne + e[2],
                            "r": 1.0 - 0.5 * (pe + ne) - 0.1 * lli,
                            "a_pe": 1.0, "a_ne": 1.0,
                            "reference": "grid",
                        })
    return pd.DataFrame(rows)


def _scored(df, tol=0.02):
    d = classify_recoverability(add_error_columns(df, tol))
    return apply_bias_correction(d, clean_bias(d), tol)


# ---------------------------------------------------------------- 비교표

def test_comparison_table_orders_and_covers_all_objectives():
    tbl = comparison_table(_scored(_fits()))
    assert list(tbl["objective"]) == ["pocv", "pocv_dvdq"]     # 34p 누적 순서
    assert (tbl["n"] > 0).all()
    assert tbl["degenerate_frac"].between(0, 1).all()


def test_comparison_table_uses_only_recoverable_rows():
    """★ F1 — 복원불가군이 표에 섞이면 안 된다."""
    df = _scored(_fits())
    assert not df["recoverable"].all(), "테스트 데이터에 복원불가군이 있어야 유효"
    tbl = comparison_table(df)
    n_rec = int(df[df["objective"] == "pocv"]["recoverable"].sum())
    assert int(tbl.loc[tbl["objective"] == "pocv", "n"].iloc[0]) == n_rec


def test_better_objective_shows_lower_degeneracy():
    """오차가 작은 목적함수가 표에서 실제로 더 낮게 나와야 한다."""
    tbl = comparison_table(_scored(_fits())).set_index("objective")
    assert tbl.loc["pocv_dvdq", "degenerate_frac"] < tbl.loc["pocv", "degenerate_frac"]
    assert tbl.loc["pocv_dvdq", "mean_abs_err"] < tbl.loc["pocv", "mean_abs_err"]


def test_by_noise_table_splits_noise_levels():
    """F10 — 노이즈별 분리 보고."""
    tbl = comparison_table(_scored(_fits()), by_noise=True)
    assert "noise" in tbl.columns
    assert set(tbl["noise"].unique()) == {0.0, 0.005}
    assert len(tbl) == 4                      # 2 objective × 2 noise


def _n_cells(line: str) -> int:
    """열 구분자만 센다. 헤더의 `\\|err\\|`(이스케이프된 파이프)는 열이 아니다."""
    return line.replace(r"\|", "").count("|")


@pytest.mark.parametrize("by_noise", [False, True])
def test_markdown_table_is_wellformed(by_noise):
    md = to_markdown(comparison_table(_scored(_fits()), by_noise=by_noise))
    lines = md.splitlines()
    ncol = _n_cells(lines[0])
    assert ncol == (8 if by_noise else 7)          # 열 수 + 1
    assert all(_n_cells(line) == ncol for line in lines), "열 수가 행마다 달라짐"
    assert set(lines[1].replace("|", "").replace("-", "")) <= {" ", ""}
    assert "%" in md


# ---------------------------------------------------------------- 22p 판정

def test_verdict_22p_finds_neighbourhood():
    df = _scored(_fits())
    v = verdict_22p(df, "pocv", noise=0.0)
    assert "error" not in v
    assert v["n_near"] >= 1
    assert 0.0 <= v["degenerate_frac"] <= 1.0
    assert v["nearest_distance"] < 0.15


def test_verdict_22p_falls_back_to_nearest_point():
    """격자에 22p 조건이 정확히 없어도 최근접 1점으로 답을 낸다."""
    df = _scored(_fits(n_lli=2))          # 0.0과 0.2뿐 — 0.13/0.17이 없음
    v = verdict_22p(df, "pocv", noise=0.0, radius=1e-6)
    assert v["n_near"] == 1
    assert v["nearest_distance"] > 0


# ---------------------------------------------------------------- 층화 표본

def test_stratified_subset_preserves_axis_corners():
    """★ 무작위 추출이면 코너가 빠질 수 있다 — 격자 구조를 보존하는지 확인."""
    curves = _fits(objectives=("pocv",), n_lli=5)[
        ["cond_id", "lli", "lam_pe", "lam_ne"]].drop_duplicates("cond_id")
    ids = stratified_subset(curves, stride=2)
    sub = curves[curves["cond_id"].isin(ids)]
    for a in ("lli", "lam_pe", "lam_ne"):
        assert sub[a].max() == curves[a].max(), f"{a} 최대 코너가 빠졌다"
        assert sub[a].min() == curves[a].min(), f"{a} 최소 코너가 빠졌다"
    assert 0 < len(ids) < curves["cond_id"].nunique()


def test_stratified_subset_stride_one_keeps_everything():
    curves = _fits(objectives=("pocv",), n_lli=3)[
        ["cond_id", "lli", "lam_pe", "lam_ne"]].drop_duplicates("cond_id")
    assert len(stratified_subset(curves, stride=1)) == curves["cond_id"].nunique()


# ---------------------------------------------------------------- 가중치 sweep

def test_build_weight_objectives_varies_only_dqdv():
    objs = build_weight_objectives([0.0, 1.0, 2.0])
    assert set(objs) == {obj_name(w) for w in (0.0, 1.0, 2.0)}
    assert {o["w_pocv"] for o in objs.values()} == {1.0}
    assert {o["w_dvdq"] for o in objs.values()} == {1.0}
    assert sorted(o["w_dqdv"] for o in objs.values()) == [0.0, 1.0, 2.0]


def test_sweep_summary_parses_w_from_objective_name():
    df = _scored(_fits(objectives=(obj_name(0.0), obj_name(1.0))))
    s = sweep_summary(df)
    assert set(s["w_dqdv"].unique()) == {0.0, 1.0}
    assert "noise" in s.columns and s["n"].gt(0).all()


def test_pick_optimum_selects_minimum_and_flags_disagreement():
    s = pd.DataFrame({
        "objective": [obj_name(w) for w in (0.0, 1.0, 2.0)] * 2,
        "w_dqdv": [0.0, 1.0, 2.0] * 2,
        "noise": [0.0] * 3 + [0.005] * 3,
        "n": [10] * 6,
        # noise 0은 w=2가 최적, noise 0.005는 w=0이 최적 → 불일치
        "degenerate_frac_corrected": [0.5, 0.3, 0.1, 0.1, 0.3, 0.5],
        "degenerate_frac": [0.5, 0.3, 0.1, 0.1, 0.3, 0.5],
    })
    opt = pick_optimum(s)
    assert opt["per_noise"][0.0]["w_dqdv"] == 2.0
    assert opt["per_noise"][0.005]["w_dqdv"] == 0.0
    assert opt["noise_levels_agree"] is False      # ★ F10: 이걸 놓치면 튜닝이 된다
    assert "특정" in opt["_주의"]


def test_pick_optimum_agreement_when_noise_levels_match():
    s = pd.DataFrame({
        "objective": [obj_name(w) for w in (0.0, 1.0)] * 2,
        "w_dqdv": [0.0, 1.0] * 2,
        "noise": [0.0, 0.0, 0.005, 0.005],
        "n": [10] * 4,
        "degenerate_frac_corrected": [0.5, 0.2, 0.6, 0.3],
        "degenerate_frac": [0.5, 0.2, 0.6, 0.3],
    })
    opt = pick_optimum(s)
    assert opt["noise_levels_agree"] is True
    assert opt["w_star_mean_over_noise"] == 1.0


# ---------------------------------------------------------------- 보고서

def test_make_results_builds_document(tmp_path):
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    _scored(_fits()).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(
        yaml.safe_dump({"n_rows_recoverable": 100,
                        "coverage_gap": {"max_lam_pe_at_low_lli": 0.1,
                                         "max_lam_pe_overall": 0.2}}),
        encoding="utf-8")

    run_compare(d, d)
    out = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path)
    text = out.read_text(encoding="utf-8")

    assert "핵심 결론" in text
    assert "이 결론이 말하지 않는 것" in text     # 한계가 결론 바로 밑에
    assert "22p" in text
    assert "degeneracy" in text
    # 결론에 실제 숫자가 채워졌는지 (자리표시자 '?'만 남으면 실패)
    assert text.count("%") > 10


def test_run_compare_writes_expected_artifacts(tmp_path):
    from tools.compare_objectives import run_compare

    d = tmp_path / "res"
    d.mkdir()
    _scored(_fits()).to_parquet(d / "degeneracy_map.parquet", index=False)
    res = run_compare(d, d)

    assert (d / "objective_comparison.csv").exists()
    assert (d / "objective_comparison_by_noise.csv").exists()
    assert (d / "objective_comparison.yaml").exists()
    assert res["figures"], "패널 그림이 하나도 안 나왔다"
    for p in res["figures"].values():
        assert Path(p).stat().st_size > 1000


def test_run_compare_requires_scoring_first(tmp_path):
    from tools.compare_objectives import run_compare

    with pytest.raises(SystemExit, match="score"):
        run_compare(tmp_path)


# ---------------------------------------------------------------- 격차 붕괴

def _gap_fits(collapse: bool, n=9, seed=1):
    """참 격차가 넓은 조건들. collapse=True면 복원값이 둘을 같다고 답한다."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        pe, ne = 0.20, 0.02              # 참 격차 18%p — 뚜렷이 다름
        mid = 0.5 * (pe + ne)
        pe_hat, ne_hat = (mid, mid) if collapse else (pe, ne)
        rows.append({
            "cond_id": f"g{i}", "objective": "pocv_dvdq", "noise": 0.0,
            "lli": 0.0, "lam_pe": pe, "lam_ne": ne,
            "lli_hat": 0.0,
            "lam_pe_hat": pe_hat + rng.normal(0, 1e-4),
            "lam_ne_hat": ne_hat + rng.normal(0, 1e-4),
            # r <= 1-max(LAM) 이어야 alpha_true=(1-LAM)/r >= 1 → 복원가능군
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
    return pd.DataFrame(rows)


def test_gap_collapse_detected_when_fit_merges_electrodes():
    """★ 참값이 다른데 같다고 답하면 붕괴율 100%."""
    from tools.compare_objectives import gap_analysis

    g = gap_analysis(_scored(_gap_fits(collapse=True)), "pocv_dvdq")
    assert g["n_wide_gap_true"] == 9
    assert g["gap_collapse_frac"] == 1.0
    assert g["shrinkage"] < 0.05


def test_gap_collapse_zero_when_fit_separates_electrodes():
    from tools.compare_objectives import gap_analysis

    g = gap_analysis(_scored(_gap_fits(collapse=False)), "pocv_dvdq")
    assert g["gap_collapse_frac"] == 0.0
    assert g["shrinkage"] == pytest.approx(1.0, abs=0.01)


def test_gap_analysis_reports_false_split():
    """참값이 같은데 다르다고 답하는 반대 방향 오류도 잡는다."""
    from tools.compare_objectives import gap_analysis

    df = pd.DataFrame([{
        "cond_id": f"s{i}", "objective": "pocv_dvdq", "noise": 0.0,
        "lli": 0.0, "lam_pe": 0.10, "lam_ne": 0.10,
        "lli_hat": 0.0, "lam_pe_hat": 0.16, "lam_ne_hat": 0.04,   # 격차 12%p 생성
        "r": 0.85, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
    } for i in range(5)])
    g = gap_analysis(_scored(df), "pocv_dvdq")
    assert g["n_zero_gap_true"] == 5
    assert g["false_split_frac"] == 1.0


def test_gap_plot_written(tmp_path):
    from tools.compare_objectives import plot_gap

    p = plot_gap(_scored(_gap_fits(collapse=True)),
                 tmp_path / "gap.png", "pocv_dvdq")
    assert Path(p).stat().st_size > 1000


def test_results_doc_leads_with_gap_collapse(tmp_path):
    """★ 보고서가 '22p 근방 성적'이 아니라 '격차 붕괴율'을 먼저 말해야 한다."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    # 넓은 격차 + 22p 근방을 함께 담은 데이터
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "격차 붕괴" in text
    i_gap = text.index("두 전극을 같다고 답하는 비율")
    i_22p = text.index("근방 자체의 degeneracy")
    assert i_gap < i_22p, "격차 붕괴 결론이 22p 근방 성적보다 앞에 와야 한다"
    # 붕괴율이 100%인 데이터 → "관측이 증거가 안 된다" 쪽 결론
    assert "나와도 두 전극이 실제로" in text
    assert "뭉개지는 않는다" not in text


def test_results_doc_conclusion_follows_the_number(tmp_path):
    """★ 결론 문장이 서사가 아니라 숫자를 따라가는지.

    붕괴율이 낮으면 "증거가 못 된다"고 단정해선 안 된다 — 데이터가 반대다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=False), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "뭉개지는 않는다" in text
    assert "나와도 두 전극이 실제로" not in text
    # 실패가 반대 방향(거짓 분리)이라는 사실이 결론에 실려야 한다
    assert "없는 격차를 만들어낸다" in text
