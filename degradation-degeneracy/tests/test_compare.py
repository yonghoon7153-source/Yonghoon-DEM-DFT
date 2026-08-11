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
    from src.weight_sweep import SEED_NAME

    objs = build_weight_objectives([0.0, 1.0, 2.0])
    reported = {k: v for k, v in objs.items() if k != SEED_NAME}
    assert set(reported) == {obj_name(w) for w in (0.0, 1.0, 2.0)}
    assert {o["w_pocv"] for o in reported.values()} == {1.0}
    assert {o["w_dvdq"] for o in reported.values()} == {1.0}
    assert sorted(o["w_dqdv"] for o in reported.values()) == [0.0, 1.0, 2.0]


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
    # F28: 이 군의 조건은 "참 격차 < tol"이지 "정확히 0"이 아니다 — 이름이 조건을
    # 잘못 말하고 있어서 바꿨고, 정확히 0인 수는 따로 센다.
    assert g["n_small_gap_true"] == 5
    assert g["n_exact_zero_gap_true"] == 5
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
    # 붕괴율 100% → 우도비가 1 미만이어야 하고, "실제로 비슷" 결론이 나오면 안 된다
    import re
    m = re.search(r"우도비 = ([\d.]+)", text)
    assert m, "우도비가 결론에 없다"
    assert float(m.group(1)) < 1.0, f"붕괴율 100%인데 우도비가 {m.group(1)}"
    # ★ F28 — 우도비를 결론으로 승격시키면 안 된다. 세 제약이 항상 붙어야 한다.
    assert "실제로 비슷하게 열화했다" not in text, \
        "우도비를 '실제로 비슷하다'는 결론으로 승격시켰다"
    for must in ("임계 의존", "posterior가 아님", "부분집단 조건화"):
        assert must in text, f"우도비 제약 '{must}'이 빠졌다"


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

    # 붕괴가 0이면 우도비가 inf가 되는데, 그 경우에도 문서가 깨지지 않아야 한다
    import re
    assert re.search(r"우도비 = (\S+)", text), "우도비가 결론에 없다"
    # ★ 임계 의존성 경고 — 붕괴가 관측 불가능한 설정이면 반드시 붙어야 한다
    assert ("임계 설정에서 붕괴가 관측되기 어렵다" in text
            or "collapse_measurable" not in text), "임계 의존성 경고가 빠졌다"
    # ★ F28 — 붕괴율이 낮게 나와도 '실제로 비슷하다'로 승격하면 안 된다
    assert "실제로 비슷하게 열화했다" not in text
    assert "방어할 수 있는 문장은 하나뿐" in text


# ---------------------------------------------------------------- F20 계단식 초기값

def test_warm_start_passes_smooth_solution_to_dqdv_objectives(monkeypatch):
    """★ F20 — dQ/dV 목적함수가 앞선 매끄러운 해를 초기값으로 받는가.

    실측 근거: 무열화 조건에서 J(정답)=0 인데도 최적화가 J=0.402에 멈추고
    LAM_PE=-6.5%p를 답했다. 최소의 유인역이 좁아서다.
    """
    import src.fitting as F

    seen = []          # (objective 이름 순서대로) fit()에 들어간 init

    def fake_fit(objective, init, lb, ub, **kw):
        seen.append(list(map(float, init)))
        # 매끄러운 목적함수는 (1,0,1,0)을 찾았다고 하자
        p = np.array([1.0, 0.0, 1.0, 0.0])
        return F.FitResult(p=p, J=0.0, converged=True, n_eval=1,
                           bound_active=(False,) * 4, n_restarts=1,
                           n_restarts_agree=1, restarts=[(p.tolist(), 0.0)])

    monkeypatch.setattr(F, "fit", fake_fit)

    n = 64
    x = np.linspace(0, 1, n)
    task = {
        "cond_id": "t0", "x": x, "v_target": 4.0 - 1.0 * x, "q_mah": 100.0, "r": 1.0,
        "truth": {"lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0, "noise": 0.0},
        "ref_x": x, "ref_pe": 4.2 - 0.5 * x, "ref_ne": 0.2 + 0.5 * x,
        "ref_full": 4.0 - 1.0 * x,
        "obj_cfg": {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                               "peak_weight": 3.0,
                                               "peak_prominence": 0.05,
                                               "peak_halfwidth": 3}},
        "objectives": {"pocv_dvdq": {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 0.0},
                       "pocv_dvdq_dqdv": {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 1.0}},
        "init": [1.03, -0.10, 1.08, -0.01],
        "lb": [0.7, -0.6, 0.7, -0.6], "ub": [1.8, 0.4, 1.8, 0.4],
        "bounds_preset": "expanded", "n_restarts": 1,
        "inventory": {"w_pe": 0.29, "w_ne": 0.71, "kappa": 0.71},
        "reference": "grid", "halfcell": None, "p_ini": None, "seed": 0,
    }

    rows = F._fit_one({**task, "warm_start": True})
    assert seen[0] == task["init"], "첫 목적함수는 기본 초기값이어야 한다"
    assert seen[1] == [1.0, 0.0, 1.0, 0.0], "dQ/dV 목적함수가 앞 해를 못 받았다"
    assert {r["objective"]: r["warm_started"] for r in rows} == {
        "pocv_dvdq": False, "pocv_dvdq_dqdv": True}

    seen.clear()
    rows = F._fit_one({**task, "warm_start": False})
    assert seen[0] == seen[1] == task["init"], "--no-warm-start인데 물려받았다"
    assert all(not r["warm_started"] for r in rows)


def test_results_doc_reports_multistart_and_warns_about_old_metrics(tmp_path):
    """★ F21 — flat_valley/multimodal이 문서에 실리고, 옛 지표에 경고가 붙는가."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    _scored(_fits()).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({
        "multistart": {
            "pocv_dvdq": {"n": 100, "flat_valley_frac": 0.42,
                          "multimodal_frac": 0.10, "unique_min_frac": 0.48},
            "pocv_dvdq_dqdv": {"n": 100, "flat_valley_frac": 0.05,
                               "multimodal_frac": 0.70, "unique_min_frac": 0.25},
            "_해석": "설명",
        }}, allow_unicode=True), encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "multi-start 진단" in text
    assert "flat valley" in text
    assert "42%" in text and "70%" in text
    # 옛 지표를 그대로 인용하지 말라는 경고가 반드시 함께 있어야 한다
    assert "agree_frac" in text and "정의상 0" in text
    # 설명 키(_해석)가 표에 행으로 새어나오면 안 된다
    assert "| _해석 |" not in text


# ---------------------------------------------------------------- 기준 곡선 비교

def _hc_fits(base, shift=0.0):
    """halfcell 쪽 fits — reference 열만 다르고 오차에 일정 오프셋을 준다."""
    d = base.copy()
    d["reference"] = "halfcell"
    for m in ("lli", "lam_pe", "lam_ne"):
        d[f"{m}_hat"] = d[m] + shift
    return d


def test_compare_cases_matches_row_counts():
    """★ 두 기준을 그냥 나란히 놓으면 행 수가 달라 난이도 차이가 섞인다.

    grid 기준은 α_true<1 조건을 복원불가로 빼므로 모집단이 작아진다.
    비교는 반드시 공통·복원가능 조건으로 맞춘 뒤에 해야 한다.
    """
    import tempfile

    from tools.compare_cases import compare

    g = _fits(objectives=("pocv_dvdq",))
    h = _hc_fits(g, shift=0.001)          # halfcell이 훨씬 정확한 상황

    with tempfile.TemporaryDirectory() as td:
        gp, hp = Path(td) / "g.parquet", Path(td) / "h.parquet"
        g.to_parquet(gp, index=False)
        h.to_parquet(hp, index=False)
        res = compare(gp, hp)

    # grid 복원가능군으로 좁혀졌는가
    scored = _scored(g)
    n_rec = scored.loc[scored["recoverable"], "cond_id"].nunique()
    assert res["n_conditions_compared"] == n_rec
    assert res["grid"]["pocv_dvdq"]["n"] == res["halfcell"]["pocv_dvdq"]["n"], \
        "두 기준의 행 수가 다르면 비교가 성립하지 않는다"
    # 실제로 더 정확한 쪽이 표에서도 낫게 나와야 한다
    assert (res["halfcell"]["pocv_dvdq"]["mean_abs_err"]
            < res["grid"]["pocv_dvdq"]["mean_abs_err"])
    # halfcell 복원불가 0%가 측정이 아니라는 경고가 들어 있어야 한다
    assert "측정이 아니라" in res["_주의_복원불가"]


def test_weight_sweep_matches_main_run_optimizer_settings():
    """★ F20d — sweep의 optimizer 설정은 본 실행과 같아야 한다.

    "모두 같은 출발선"이 공정하다고 보고 warm start를 껐다가 틀렸다. sweep의
    양 끝점은 본 실행의 목적함수와 정의가 같으므로(w=0 ≡ pocv_dvdq,
    w=1 ≡ pocv_dvdq_dqdv) 결과가 일치해야 하는데, 끄면 w>0만 어긋난다
    (실측: w=1의 J중앙값 0.406 vs 0.326, 51.7%의 조건에서 sweep이 더 큼).
    """
    import inspect

    from src.weight_sweep import run_weight_sweep

    sig = inspect.signature(run_weight_sweep).parameters
    assert sig["warm_start"].default is True, \
        "sweep을 warm start 없이 돌리면 가중치가 아니라 최적화 난이도를 잰다"
    assert sig["n_restarts"].default == 5, \
        "restart 2는 부족하다 — 같은 목적함수가 본 실행 17% vs sweep 92%였다"
    assert "warm_start=warm_start" in inspect.getsource(run_weight_sweep), \
        "인자를 받고도 run_fit에 넘기지 않으면 설정이 무시된다"


def test_seed_objective_only_when_w_grid_lacks_zero():
    """warm start의 seed 제공자는 w=0이다. 없을 때만 숨은 seed를 끼운다."""
    from src.weight_sweep import SEED_NAME, build_weight_objectives

    with_zero = build_weight_objectives([0.0, 1.0, 2.0])
    assert SEED_NAME not in with_zero, "w=0이 있으면 seed는 군더더기다"
    assert next(iter(with_zero)) == obj_name(0.0), \
        "seed 제공자가 맨 앞이어야 뒤의 w들이 그 해를 물려받는다"

    without_zero = build_weight_objectives([0.5, 1.0])
    assert next(iter(without_zero)) == SEED_NAME, \
        "w=0이 없으면 seed 제공자가 없어 아무도 warm start를 못 받는다"
    assert without_zero[SEED_NAME]["w_dqdv"] == 0.0


def test_sweep_yaml_warns_when_settings_diverge(tmp_path, monkeypatch):
    """설정이 본 실행과 다르면 결과 파일이 스스로 경고를 달아야 한다."""
    import inspect

    from src.weight_sweep import run_weight_sweep

    src = inspect.getsource(run_weight_sweep)
    assert "if not warm_start:" in src, "warm start를 끈 실행에 경고가 없다"
    assert "elif n_restarts < 5:" in src, "restart 부족 실행에 경고가 없다"
    assert '"_경고"' in src


def test_legacy_seed_rows_are_excluded_from_summary():
    from src.weight_sweep import SEED_NAME, obj_name, sweep_summary

    df = _fits(objectives=(SEED_NAME, obj_name(0.0), obj_name(1.0)))
    s = sweep_summary(_scored(df))
    assert SEED_NAME not in set(s["objective"]), "숨은 seed가 결과표에 새어나왔다"
    assert set(s["w_dqdv"].unique()) == {0.0, 1.0}


def test_warm_flag_overrides_default_rule(monkeypatch):
    """_warm 플래그가 있으면 w_dqdv 값과 무관하게 그것을 따른다."""
    import src.fitting as F

    seen = []

    def fake_fit(objective, init, lb, ub, **kw):
        seen.append(list(map(float, init)))
        p = np.array([1.0, 0.0, 1.0, 0.0])
        return F.FitResult(p=p, J=0.0, converged=True, n_eval=1,
                           bound_active=(False,) * 4, restarts=[(p.tolist(), 0.0)])

    monkeypatch.setattr(F, "fit", fake_fit)
    n = 64
    x = np.linspace(0, 1, n)
    task = {
        "cond_id": "t", "x": x, "v_target": 4.0 - x, "q_mah": 100.0, "r": 1.0,
        "truth": {"lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0, "noise": 0.0},
        "ref_x": x, "ref_pe": 4.2 - 0.5 * x, "ref_ne": 0.2 + 0.5 * x,
        "ref_full": 4.0 - x,
        "obj_cfg": {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2}},
        # w_dqdv=0 인데 _warm=True → 초기값을 받아야 한다
        "objectives": {"seed": {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 0.0,
                                "_warm": False},
                       "zero_but_warm": {"w_pocv": 1.0, "w_dvdq": 1.0,
                                         "w_dqdv": 0.0, "_warm": True}},
        "init": [1.03, -0.10, 1.08, -0.01],
        "lb": [0.7, -0.6, 0.7, -0.6], "ub": [1.8, 0.4, 1.8, 0.4],
        "bounds_preset": "expanded", "n_restarts": 1,
        "inventory": {"w_pe": 0.29, "w_ne": 0.71, "kappa": 0.71},
        "reference": "grid", "halfcell": None, "p_ini": None, "seed": 0,
        "warm_start": True,
    }
    rows = F._fit_one(task)
    assert seen[0] == task["init"]
    assert seen[1] == [1.0, 0.0, 1.0, 0.0], "_warm=True인데 초기값을 못 받았다"
    assert {r["objective"]: r["warm_started"] for r in rows} == {
        "seed": False, "zero_but_warm": True}


def test_results_doc_warns_when_multistart_sample_sizes_differ(tmp_path):
    """★ F4 — restart 0을 뺀 뒤 표본 수가 목적함수마다 달라지면 경고해야 한다.

    실측 halfcell: pocv 1667 vs dqdv_only 3008 — 두 배 차이인데 같은 표에
    나란히 놓이면 소수점 차이를 읽게 된다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    _scored(_fits()).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({
        "multistart_random_only": {
            "pocv": {"n": 1667, "flat_valley_frac": 0.03,
                     "multimodal_frac": 0.44, "unique_min_frac": 0.53},
            "pocv_dvdq": {"n": 3008, "flat_valley_frac": 0.02,
                          "multimodal_frac": 0.91, "unique_min_frac": 0.07},
        }}, allow_unicode=True), encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "표본 수가 목적함수마다 다릅니다" in text
    assert "1667" in text and "3008" in text


def test_no_warning_when_sample_sizes_match(tmp_path):
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    _scored(_fits()).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({
        "multistart_random_only": {
            "pocv": {"n": 1000, "flat_valley_frac": 0.03,
                     "multimodal_frac": 0.44, "unique_min_frac": 0.53},
            "pocv_dvdq": {"n": 1020, "flat_valley_frac": 0.02,
                          "multimodal_frac": 0.91, "unique_min_frac": 0.07},
        }}, allow_unicode=True), encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "표본 수가 목적함수마다 다릅니다" not in text


def test_threshold_caveat_always_in_conclusion(tmp_path):
    """★ 임계 의존성은 붕괴가 '관측 가능'해도 결론에 실려야 한다.

    표에만 두면 결론만 떼어 인용될 때 빠진다.
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
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    head = text[:text.index("## 목적함수 4종 비교")]      # 결론 구간만
    assert "임계 설정에 의존한다" in head
    assert "격차 오차가 필요한데" in head


# ---------------------------------------------------------------- F28/F29 리뷰 대응

def _gap_frame(n_same=40, n_wide=40, collapse=2, split=10):
    """참 격차가 0인 군과 큰 군을 섞은 합성 프레임."""
    rows = []
    for i in range(n_same):                      # 참 격차 0
        gap_hat = 0.10 if i < split else 0.0     # split개는 거짓 분리
        rows.append({"cond_id": f"z{i}", "objective": "pocv_dvdq", "noise": 0.0,
                     "lli": 0.0, "lam_pe": 0.10, "lam_ne": 0.10, "lli_hat": 0.0,
                     "lam_pe_hat": 0.10 + gap_hat, "lam_ne_hat": 0.10,
                     "r": 0.80, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid"})
    for i in range(n_wide):                      # 참 격차 10%p
        gap_hat = 0.0 if i < collapse else 0.10  # collapse개만 붕괴
        rows.append({"cond_id": f"w{i}", "objective": "pocv_dvdq", "noise": 0.0,
                     "lli": 0.0, "lam_pe": 0.15, "lam_ne": 0.05, "lli_hat": 0.0,
                     "lam_pe_hat": 0.05 + gap_hat, "lam_ne_hat": 0.05,
                     "r": 0.80, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid"})
    return _scored(pd.DataFrame(rows))


def test_gap_sensitivity_surface_is_emitted():
    """★ F28 — 우도비 하나만 내면 안 된다. 임계 격자 전체가 나와야 한다."""
    from tools.compare_objectives import gap_sensitivity

    rows = gap_sensitivity(_gap_frame(), "pocv_dvdq")
    assert len(rows) >= 6
    assert {"gap_thresh", "tol", "likelihood_ratio",
            "p_same_given_same", "p_same_given_wide", "n_same", "n_wide"} <= set(rows[0])
    # gap_thresh <= tol 조합은 정의가 무너지므로 나오면 안 된다
    assert all(r["gap_thresh"] > r["tol"] for r in rows)


def test_gap_analysis_carries_its_own_sensitivity_and_caveat():
    """★ F28 — 우도비를 떼어 인용하지 못하게 경고와 범위를 같은 dict에 넣는다."""
    from tools.compare_objectives import gap_analysis

    g = gap_analysis(_gap_frame(), "pocv_dvdq")
    assert "likelihood_ratio_equal" in g
    for k in ("lr_sensitivity_min", "lr_sensitivity_max", "lr_sensitivity_median",
              "lr_is_local_spike"):
        assert k in g, f"{k}가 없으면 임계 의존성을 모르고 인용하게 된다"
    assert "posterior가 아니라" in g["_주의"]
    assert g["population"] == "recoverable"


def test_comparison_table_can_report_all_conditions():
    """★ F29 — 복원가능군 제외가 결론을 만드는지 보려면 전체군이 필요하다."""
    from tools.compare_objectives import comparison_table

    df = _gap_frame()
    df.loc[df.index[:20], "recoverable"] = False
    rec = comparison_table(df)
    allc = comparison_table(df, recoverable_only=False)
    assert int(allc["n"].sum()) > int(rec["n"].sum())


def test_antisym_and_population_caveats_ride_with_conclusion_1(tmp_path):
    """★ F29 — 33p·34p를 나란히 놓는 순간 두 경고가 결론에 붙어야 한다.

    (a) PE-NE 상쇄는 raw 오차 부호만 세므로 전역 편향 부호차를 상쇄로 잡는다.
        실측에서 편향을 빼면 방향이 뒤집혔다(70.5→52.6 raw vs 33.1→42.9 중심화).
    (b) 복원가능군 조건화가 33p·34p의 우열을 뒤집는다면 그 사실도 함께 나와야 한다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = _fits(objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "상쇄를 줄였다'로 읽지 마세요" in text
    assert "전체 격자 (복원불가군 포함)" in text, "전체군 표가 빠지면 F29를 볼 수 없다"


def test_results_doc_carries_citation_block_without_provenance(tmp_path):
    """★ F35 — provenance 없는 artifact로 만든 문서는 맨 위에 인용 금지 배너.

    회답을 별도 문서에만 두면 저장소를 여는 사람은 철회 전 결론을 먼저 본다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    _scored(_fits(objectives=("pocv_dvdq",))).to_parquet(
        d / "degeneracy_map.parquet", index=False)
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    (d / "manifest.yaml").write_text(
        yaml.safe_dump({"config_hash": "", "git_dirty": True, "reproducible": False}),
        encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "인용 금지" in text[:400], "배너가 문서 맨 위에 없다"
    # 실패 사유가 길어질 수 있으므로 본문 전체에서 확인한다
    assert "config_hash" in text and "clean_worktree" in text
    assert "08_REVIEW_RESPONSE.md" in text
    # F56/F57: 새 검사들도 실패 목록에 나와야 한다
    for k in ("run_spec_schema", "시작_provenance", "start_파일_존재"):
        assert k in text, f"{k} 검사가 배너에 없다"


def _complete_artifact(tmp_path):
    """provenance 검사를 **실제로** 통과하는 artifact.

    ★ F43/F50/F56/F57 — 이 fixture 는 세 번 깨졌다. 매번 validator 를 강화하자
      "통과한다고 부르던 것"이 실제로는 통과하면 안 되는 것이었음이 드러났다.
      지금은 진짜 입력 파일 · 진짜 해시 · 시작 봉인 map · 디스크의 start/attempt
      파일까지 갖춘다.
    """
    import hashlib
    import json

    import yaml

    from src.io import env_fingerprint, file_digest, seal_inputs, source_digest

    d = Path(tmp_path) / "res"
    d.mkdir(parents=True, exist_ok=True)

    curves = d / "curves.parquet"       # 이름이 필수 입력 판정에 쓰인다 (F50)
    _fits(objectives=("pocv_dvdq",)).to_parquet(curves, index=False)
    cfg = d / "base.yaml"              # 〃
    cfg.write_text("dummy: 1\n", encoding="utf-8")

    sealed = seal_inputs([curves, cfg])          # F56: 한 번만 봉인
    # ★ F68 — 조건 집합 서명은 **실제 fits 의 조건**에서 나와야 한다.
    #   하드코딩하면 그 자체가 위조 통로가 된다.
    from src.io import _sha256_lines
    _df0 = _fits(objectives=("pocv_dvdq",))
    _conds = sorted(set(_df0["cond_id"].astype(str)))
    src = source_digest()
    env = env_fingerprint()
    attempt_id = "20260807T000000_1_000"

    spec = {"sig_version": 5, "objectives": {"pocv_dvdq": {"w_pocv": 1.0}},
            # ★ F67 — 계산을 고정하는 축들. 설정만으론 부족하다.
            "objective_order": ["pocv_dvdq"],
            "condition_ids_sha256": _sha256_lines(_conds)[:16],
            "n_conditions": len(_conds), "selection": "full",
            "optimizer": {"method": "Nelder-Mead", "adaptive": True,
                          "n_restarts": 5, "agree_tol": 1e-3,
                          "seed_scheme": "sha1(cond_id)[:8]"},
            "reference": "grid", "bounds_preset": "expanded",
            "bounds": {"init": [1.0, 0.0, 1.0, 0.0]}, "v_col": "v_full",
            "n_restarts": 5, "warm_start": True, "obj_cfg": {"objectives": {}},
            "inventory": {"w_pe": 0.3, "w_ne": 0.7, "kappa": 0.7},
            "env": env, "sealed_inputs": sealed,
            "curves_sha": sealed[str(curves)],
            "base_config_sha": sealed[str(cfg)],
            "git_commit": "0" * 40, "git_dirty": False, "source_digest": src}
    sig = hashlib.sha1(
        json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()[:12]

    start = {"attempt_id": attempt_id, "started_at": "2026-08-07T00:00:00",
             "resume": False, "source_digest": src, "env": env,
             "git_commit": "0" * 40, "git_dirty": False,
             "input_sha256": sealed}
    (d / "manifest_start.yaml").write_text(
        yaml.safe_dump(start, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (d / "attempts").mkdir(exist_ok=True)
    (d / "attempts" / f"manifest_start_{attempt_id}.yaml").write_text(
        yaml.safe_dump(start, allow_unicode=True, sort_keys=False), encoding="utf-8")

    _scored(_fits(objectives=("pocv_dvdq",))).to_parquet(
        d / "degeneracy_map.parquet", index=False)
    # fits.parquet 은 **채점 전** 원본이어야 한다 — 채점 열이 이미 있으면
    # 하류의 apply_bias_correction 이 merge 충돌로 죽는다
    df = _df0.copy()
    df["run_sig"] = sig
    df["restarts_json"] = json.dumps(
        [{"p": [1.0, 0.0, 1.0, 0.0], "J": 0.0, "i": 0, "source": "base_init"},
         {"p": [1.1, 0.0, 1.1, 0.0], "J": 0.5, "i": 1, "source": "random"}])
    df.to_parquet(d / "fits.parquet", index=False)
    # ★ F68 — 출력 봉인. fixture 도 실제 파일에서 계산해야 한다 (가짜 값을 넣으면
    #   validator 가 다시 잡는다 — 지금까지 이 fixture 가 계속 그 역할을 했다).
    from src.io import fits_seal
    _seal = fits_seal(d / "fits.parquet")
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    (d / "manifest.yaml").write_text(yaml.safe_dump({
        "config_hash": "deadbeef1234", "git_dirty": False, "reproducible": True,
        "run_signature": sig, "run_spec": spec,
        "start_provenance": start, "attempt_id": attempt_id,
        "git_commit_changed_during_run": False,
        "source_digest_changed_during_run": False,
        "inputs_changed_during_run": False,
        "input_sha256": sealed, "input_sha256_source": "sealed_at_start",
        "fits_seal": _seal,
    }), encoding="utf-8")
    return d, sig


def test_provenance_validator_rejects_forged_signature(tmp_path):
    """★ F38 — `run_sig` 열이 있기만 하면 통과하던 판정을 실제 검사로 바꾼다."""
    import pandas as pd
    import yaml

    from src.io import validate_provenance

    d, sig = _complete_artifact(tmp_path)
    assert validate_provenance(d)["ok"], validate_provenance(d)["fail"]

    # ① manifest와 다른 서명
    f = pd.read_parquet(d / "fits.parquet")
    f["run_sig"] = "other0000000"
    f.to_parquet(d / "fits.parquet", index=False)
    assert "manifest와_일치" in validate_provenance(d)["fail"]

    # ② 서명이 둘 이상
    f.loc[f.index[:5], "run_sig"] = sig
    f.to_parquet(d / "fits.parquet", index=False)
    assert "단일_서명" in validate_provenance(d)["fail"]

    # ③ 일부 행이 null
    f["run_sig"] = sig
    f.loc[f.index[:3], "run_sig"] = None
    f.to_parquet(d / "fits.parquet", index=False)
    assert "행별_서명" in validate_provenance(d)["fail"]

    # ④ 옛 restarts 형식 (source 없음)
    f["run_sig"] = sig
    f["restarts_json"] = "[[[1.0, 0.0, 1.0, 0.0], 0.0]]"
    f.to_parquet(d / "fits.parquet", index=False)
    assert "restart_출처" in validate_provenance(d)["fail"]

    # ⑤ 입력 digest 누락
    d2, _ = _complete_artifact(tmp_path / "b")
    m = yaml.safe_load((d2 / "manifest.yaml").read_text(encoding="utf-8"))
    m["input_sha256"] = {}
    (d2 / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    assert "입력_digest" in validate_provenance(d2)["fail"]


def test_results_doc_has_no_banner_when_provenance_complete(tmp_path):
    """반대로 provenance가 **실제로** 갖춰지면 배너가 붙으면 안 된다."""
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "인용 금지" not in text
    assert "provenance 검증 통과" in text


def test_validator_requires_mandatory_inputs_and_schema(tmp_path):
    """★ F50 — 존재하는 임의 파일 하나·최소 spec으로는 통과하면 안 된다."""
    import yaml

    from src.io import validate_provenance

    d, sig = _complete_artifact(tmp_path)

    # ① 필수 입력(curves) 누락 — 다른 실제 파일만 남긴다
    m = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    keep = {k: v for k, v in m["input_sha256"].items() if "base.yaml" in k}
    m2 = dict(m, input_sha256=keep)
    (d / "manifest.yaml").write_text(yaml.safe_dump(m2), encoding="utf-8")
    assert "필수_입력_존재" in validate_provenance(d)["fail"]

    # ② run_spec 필수 키 누락 (self-consistent 최소 spec)
    import hashlib
    import json

    d2, _ = _complete_artifact(tmp_path / "b")
    m = yaml.safe_load((d2 / "manifest.yaml").read_text(encoding="utf-8"))
    tiny = {"reference": "grid"}
    m["run_spec"] = tiny
    m["run_signature"] = hashlib.sha1(
        json.dumps(tiny, sort_keys=True, default=str).encode()).hexdigest()[:12]
    import pandas as _pd
    f = _pd.read_parquet(d2 / "fits.parquet")
    f["run_sig"] = m["run_signature"]
    f.to_parquet(d2 / "fits.parquet", index=False)
    (d2 / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    fail = validate_provenance(d2)["fail"]
    assert "run_spec_schema" in fail and "코드_identity" in fail


def test_validator_rejects_null_and_partial_restart_arrays(tmp_path):
    """★ F50 — `.dropna()` 때문에 전부 null이어도 통과했고, `rs[0]`만 봤다."""
    import json

    import pandas as pd

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)

    # ① 전부 null
    f = pd.read_parquet(d / "fits.parquet")
    f["restarts_json"] = None
    f.to_parquet(d / "fits.parquet", index=False)
    assert "restart_출처" in validate_provenance(d)["fail"], \
        "restarts_json이 전부 null인데 통과했다 (F50)"

    # ② 첫 원소만 source 있고 두 번째는 없음
    f["restarts_json"] = json.dumps(
        [{"p": [1.0, 0, 1.0, 0], "J": 0.0, "i": 0, "source": "random"},
         {"p": [1.1, 0, 1.1, 0], "J": 0.5, "i": 1}])
    f.to_parquet(d / "fits.parquet", index=False)
    assert "restart_출처" in validate_provenance(d)["fail"], \
        "배열 뒤쪽 원소에 source가 없는데 통과했다 (F50)"


def test_validator_rejects_code_change_during_run(tmp_path):
    """★ F49/F50 — 실행 도중 코드가 바뀐 artifact는 인용 불가."""
    import yaml

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)
    m = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    m["source_digest_changed_during_run"] = True
    (d / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    assert "실행중_코드불변" in validate_provenance(d)["fail"]

    # F50b: git commit만 바뀌고 source가 그대로면 실패가 아니다 (문서 커밋 등)
    d3, _ = _complete_artifact(tmp_path / "d")
    m = yaml.safe_load((d3 / "manifest.yaml").read_text(encoding="utf-8"))
    m["git_commit_changed_during_run"] = True
    (d3 / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    r = validate_provenance(d3)
    assert r["ok"], f"문서 커밋 때문에 실패했다: {r['fail']}"
    assert "_참고_git이동" in r["checks"]

    # 시작 provenance 자체가 없으면(F51 이전 실행) 그것도 실패
    d2, _ = _complete_artifact(tmp_path / "c")
    m = yaml.safe_load((d2 / "manifest.yaml").read_text(encoding="utf-8"))
    del m["start_provenance"]
    (d2 / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    assert "시작_provenance" in validate_provenance(d2)["fail"]


def test_banner_stays_when_compared_artifact_fails_provenance(tmp_path):
    """★ F52b — 비교에 쓰인 half-cell artifact가 실패하면 배너가 남아야 한다.

    배너가 주 입력만 검사하면, 검증된 grid + 검증 안 된 half-cell로 만든
    비교표가 녹색 배너 아래 실린다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    run_compare(d, d)

    # half-cell 쪽이 실패했다고 봉인된 비교 결과
    (d / "case_comparison.yaml").write_text(yaml.safe_dump({
        "provenance": {
            "grid": {"run_dir": str(d), "ok": True, "fail": []},
            "halfcell": {"run_dir": "results/halfcell_x", "ok": False,
                         "fail": ["행별_서명"]},
        },
        "provenance_ok": False,
    }), encoding="utf-8")

    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "인용 금지" in text[:1500], "비교 입력이 실패했는데 배너가 사라졌다 (F52b)"
    assert "비교입력_halfcell" in text


def test_banner_flags_legacy_case_comparison_without_provenance(tmp_path):
    """F52 이전에 만든 case_comparison.yaml도 인용 불가로 잡아야 한다."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    run_compare(d, d)
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump({"common": {"n": 10}}), encoding="utf-8")

    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "인용 금지" in text[:1500]
    assert "비교입력_provenance_없음" in text


def test_validator_rejects_non_canonical_scored_file(tmp_path):
    """★ F59 — 검증 대상과 채점 대상이 달라선 안 된다.

    compare가 alternate.parquet을 채점하면서 검증은 fits.parquet에 했더니,
    파일 인자 하나로 degeneracy를 94.4% → 0%로 바꾸고도 통과했다.
    """
    import pandas as pd

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)
    assert validate_provenance(d)["ok"]

    alt = d / "alternate.parquet"
    pd.read_parquet(d / "fits.parquet").to_parquet(alt, index=False)
    r = validate_provenance(d, fits_path=alt)
    assert "채점파일_정본" in r["fail"], "정본이 아닌 파일을 채점해도 통과했다 (F59)"


def test_compare_cases_validates_the_file_it_scores(tmp_path):
    """★ F59 — compare_cases가 실제 채점 파일을 검증 대상으로 넘겨야 한다."""
    import pandas as pd

    from tools.compare_cases import compare

    g, _ = _complete_artifact(tmp_path / "g")
    h, _ = _complete_artifact(tmp_path / "h")
    alt = h / "alternate.parquet"
    df = pd.read_parquet(h / "fits.parquet").copy()
    # 복원값을 참값 쪽으로 크게 당긴다 (degeneracy가 확 낮아지는 조작)
    for k in ("lam_pe", "lam_ne", "lli"):
        df[f"{k}_hat"] = df[k] + (df[f"{k}_hat"] - df[k]) * 0.01
    df.to_parquet(alt, index=False)

    res = compare(g / "fits.parquet", alt)
    assert res["provenance"]["halfcell"]["scored_file"] == str(alt)
    assert res["provenance_ok"] is False, \
        "정본이 아닌 파일을 채점했는데 provenance_ok가 참이다 (F59)"


def test_report_revalidates_compared_artifacts_at_generation(tmp_path):
    """★ F60 — 저장된 ok를 믿으면 stale·변조 artifact가 녹색으로 통과한다."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    h, _ = _complete_artifact(tmp_path / "h")
    run_compare(d, d)

    # 만들 당시엔 유효했다고 봉인해 두고
    (d / "case_comparison.yaml").write_text(yaml.safe_dump({
        "grid": {}, "provenance_ok": True,
        "provenance": {
            "grid": {"run_dir": str(d), "scored_file": str(d / "fits.parquet"),
                     "ok": True, "fail": []},
            "halfcell": {"run_dir": str(h), "scored_file": str(h / "fits.parquet"),
                         "ok": True, "fail": []}},
    }), encoding="utf-8")
    # 그 뒤 half-cell manifest를 무효화한다
    m = yaml.safe_load((h / "manifest.yaml").read_text(encoding="utf-8"))
    m["config_hash"] = ""
    (h / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "인용 금지" in text[:400], \
        "봉인된 ok만 믿고 stale artifact를 통과시켰다 (F60)"


def test_report_requires_both_tags_and_top_level_flag(tmp_path):
    """★ F60 — tag 누락이나 provenance_ok=False도 배너를 유지해야 한다."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    run_compare(d, d)
    (d / "case_comparison.yaml").write_text(yaml.safe_dump({
        "grid": {}, "provenance_ok": False,
        "provenance": {"grid": {"run_dir": str(d),
                                "scored_file": str(d / "fits.parquet"),
                                "ok": True, "fail": []}},
    }), encoding="utf-8")

    text = build(d, tmp_path / "R2.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "인용 금지" in text[:400]
    assert "비교입력_tag불완전" in text and "비교입력_provenance_ok_아님" in text


def test_validator_rejects_null_valued_restart_entries(tmp_path):
    """★ F61 — 키만 있고 값이 전부 null인 restart도 거부해야 한다."""
    import json

    import pandas as pd

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)
    f = pd.read_parquet(d / "fits.parquet")
    f["restarts_json"] = json.dumps([{"p": None, "J": None, "i": None,
                                      "source": None}])
    f.to_parquet(d / "fits.parquet", index=False)
    assert "restart_출처" in validate_provenance(d)["fail"]

    # 허용 enum 밖의 source, 음수 index, 길이가 다른 p도 거부
    for bad in ([{"p": [1.0, 0, 1.0, 0], "J": 0.0, "i": 0, "source": "hmm"}],
                [{"p": [1.0, 0, 1.0, 0], "J": 0.0, "i": -1, "source": "random"}],
                [{"p": [1.0, 0, 1.0], "J": 0.0, "i": 0, "source": "random"}]):
        f["restarts_json"] = json.dumps(bad)
        f.to_parquet(d / "fits.parquet", index=False)
        assert "restart_출처" in validate_provenance(d)["fail"], bad


def test_archive_bundle_roundtrip_validates(tmp_path):
    """★ F62 — 보관 묶음을 복원하면 provenance 검증을 통과해야 한다.

    검증기를 세 라운드에 걸쳐 강화하는 동안 archive 스크립트는 그대로였다.
    그 결과 `manifest_start.yaml` · `attempts/` · `curves.parquet` 이 빠진
    묶음만 저장소에 남았고, **clone 한 사람은 결과를 검증할 수 없었다.**
    재생성으로도 못 때운다 — curves를 다시 만들면 바이트가 달라 digest가 깨진다.
    """
    from src.io import validate_provenance
    from tools.archive_bundle import bundle, check, restore

    d, _ = _complete_artifact(tmp_path)
    assert validate_provenance(d)["ok"], validate_provenance(d)["fail"]

    out = tmp_path / "artifacts" / "run"
    res = bundle(d, out)
    assert not res["missing"], res["missing"]
    assert check(out)["ok"], check(out)["missing"]

    # 원본을 지워도 묶음만으로 복원·검증이 되어야 한다
    import shutil
    shutil.rmtree(d)
    r = restore(out, run_dir=d)
    assert Path(r["run_dir"]) == d
    v = validate_provenance(d)
    assert v["ok"], v["fail"]


def test_archive_bundle_check_catches_missing_start_files(tmp_path):
    """★ F62 — 옛 archive 방식(요약+fits만)은 '검증 불가'로 걸려야 한다."""
    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "artifacts" / "run"
    bundle(d, out)

    for victim in ("manifest_start.yaml", "curves.parquet"):
        (out / victim).unlink()
        res = check(out)
        assert not res["ok"] and any(victim in m for m in res["missing"]), res
        bundle(d, out)          # 되돌려 놓고 다음 항목

    import shutil
    shutil.rmtree(out / "attempts")
    res = check(out)
    assert not res["ok"] and any("attempts/" in m for m in res["missing"]), res


# ─────────────────────────────────────────────── F68: 출력 봉인 (7차 게이트 리뷰)
#  리뷰가 **실제로 재현해 보인** 조작들이다. 여섯 라운드 동안 "인용 가능성"을
#  판정하는 장치를 강화하면서, 정작 인용되는 숫자는 한 번도 검사하지 않았다.

def test_validator_rejects_tampered_fit_values(tmp_path):
    """★ F68 — 복원값을 바꾸면 잡아야 한다.

    반례: `lam_pe_hat = 0.999`, `lli_hat = -0.777`, `J = 12345` 로 바꿔도
    `validator.ok = True`, `fail = []` 였다. LAM/LLI 복원값과 degeneracy 분류를
    직접 바꿀 수 있으므로 결론 1~3의 **모든 정량값**을 바꿀 수 있다.
    """
    import pandas as pd

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)
    assert validate_provenance(d)["ok"], validate_provenance(d)["fail"]

    f = pd.read_parquet(d / "fits.parquet")
    f.loc[f.index[0], "lam_pe_hat"] = 0.999
    f.loc[f.index[0], "lli_hat"] = -0.777
    f.to_parquet(d / "fits.parquet", index=False)
    v = validate_provenance(d)
    assert not v["ok"] and "출력봉인_재계산" in v["fail"], v["checks"]


def test_validator_rejects_column_wide_shift(tmp_path):
    """★ F68 — 한 열 전체에 상수를 더하는 조작 (반례: `lam_pe_hat += 0.5`)."""
    import pandas as pd

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)
    f = pd.read_parquet(d / "fits.parquet")
    f["lam_pe_hat"] = f["lam_pe_hat"] + 0.5
    f.to_parquet(d / "fits.parquet", index=False)
    assert "출력봉인_재계산" in validate_provenance(d)["fail"]


def test_validator_rejects_deleted_condition_rows(tmp_path):
    """★ F68 — 행을 지우면 분모가 조용히 달라진다.

    반례: `manifest.n_conditions = 3` 인데 fits 에서 두 조건을 지워 한 조건만
    남겨도 통과했다. 조건 subset/union 이 바뀌어도 같은 서명을 재사용할 수 있어
    결론 2의 분모와 sweep 최적값이 바뀔 수 있었다.
    """
    import pandas as pd

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path)
    f = pd.read_parquet(d / "fits.parquet")
    keep = sorted(set(f["cond_id"]))[:2]
    f[f["cond_id"].isin(keep)].to_parquet(d / "fits.parquet", index=False)
    v = validate_provenance(d)
    for k in ("출력봉인_재계산", "조건집합_서명일치", "출력_완전성"):
        assert k in v["fail"], f"{k}가 통과했다: {v['checks'][k]}"


def test_validator_rejects_forged_seal_record(tmp_path):
    """★ F68 — 봉인 **기록**을 파일에 맞춰 고쳐도 서명과 어긋나면 잡는다.

    조작자가 fits 를 바꾸고 `fits_seal` 도 다시 계산해 넣으면 재계산 검사는
    통과한다. 그러나 `condition_ids_sha256` 은 `run_spec` 안에 있고 그건
    `run_signature` 로 해시돼 있으므로, 조건을 지우면 여기서 걸린다.
    """
    import pandas as pd
    import yaml

    from src.io import fits_seal, validate_provenance

    d, _ = _complete_artifact(tmp_path)
    f = pd.read_parquet(d / "fits.parquet")
    keep = sorted(set(f["cond_id"]))[:2]
    f[f["cond_id"].isin(keep)].to_parquet(d / "fits.parquet", index=False)

    m = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    m["fits_seal"] = fits_seal(d / "fits.parquet")       # 기록을 파일에 맞춘다
    (d / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    v = validate_provenance(d)
    assert "출력봉인_재계산" not in v["fail"]          # 기록은 맞췄으니 통과
    assert "조건집합_서명일치" in v["fail"], "서명된 조건 집합과의 대조가 없다"
    assert "출력_완전성" in v["fail"]


# ────────────────────────────────────── F69: 파생 체인 (7차 게이트 리뷰 발견 7)
#  F59/F60 은 Case 비교의 **한 입구**만 막았고, 실제 scoring → compare → report
#  체인은 열려 있었다. 아래 셋 전부 리뷰가 실제로 재현해 보인 것이다.

def test_scoring_rejects_uncanonical_fits(tmp_path):
    """★ F69 — `--fits` 로 임의 parquet 을 채점할 수 없다.

    반례: canonical `fits.parquet` 은 그대로 두고 `alternate.parquet` 의 hats 를
    truth 로 조작한 뒤 `run_scoring(..., fits_name='alternate.parquet')` 를 돌리면
    **objective degeneracy 가 94% → 0%** 가 되고 인용 금지 배너는 뜨지 않았다.
    """
    import pytest

    from src.scoring import run_scoring

    d, _ = _complete_artifact(tmp_path)
    alt = _fits(objectives=("pocv_dvdq",)).copy()
    for k in ("lli", "lam_pe", "lam_ne"):
        alt[f"{k}_hat"] = alt[k]                     # 오차 0 — degeneracy 0%
    alt.to_parquet(d / "alternate.parquet", index=False)

    with pytest.raises(RuntimeError, match="정본"):
        run_scoring(d, fits_name="alternate.parquet")

    # 진단 목적으로 허용하면 산출물이 스스로 무효를 밝힌다
    s = run_scoring(d, out_dir=tmp_path / "diag", fits_name="alternate.parquet",
                    allow_uncanonical=True)
    assert s["_채점원본"]["인용가능"] is False
    assert not s["_채점원본"]["canonical"]


def test_compare_cases_rejects_grid_grid(tmp_path):
    """★ F69 — grid artifact 두 개를 넣으면 "기준 곡선 비교"가 아니다.

    반례: 두 artifact 의 `run_spec.reference` 가 모두 `grid` 인데
    `compare_cases.provenance_ok = True` 였고 인용 금지 배너도 없었다.
    tag 가 **인자 순서**로만 붙었기 때문이다. 결론 3 전체가 이 전제 위에 있다.
    """
    from tools.compare_cases import compare

    a, _ = _complete_artifact(tmp_path / "a")
    b, _ = _complete_artifact(tmp_path / "b")      # 둘 다 reference: grid
    res = compare(a / "fits.parquet", b / "fits.parquet")

    assert res["provenance_ok"] is False
    assert res["provenance"]["halfcell"]["reference_실제"] == "grid"
    assert "reference_역할불일치" in res["provenance"]["halfcell"]["fail"]


def test_compare_cases_flags_different_experiments(tmp_path):
    """★ F69 — 서로 다른 curves·조건 집합의 두 표는 "기준 곡선 효과"가 아니다."""
    import yaml

    from tools.compare_cases import compare

    a, _ = _complete_artifact(tmp_path / "a")
    b, _ = _complete_artifact(tmp_path / "b")
    m = yaml.safe_load((b / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["reference"] = "halfcell"        # 역할은 맞춰 두고
    m["run_spec"]["curves_sha"] = "다른곡선"        # 입력만 다르게
    (b / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    res = compare(a / "fits.parquet", b / "fits.parquet")
    assert res["provenance_ok"] is False
    assert res["공통_run_spec"]["curves_sha"]["일치"] is False
    assert "인용 금지" in res["_주의_공통성"]


def test_results_banner_catches_tampered_derived_yaml(tmp_path):
    """★ F69 — 파생 YAML 의 **숫자**를 고치면 배너가 떠야 한다.

    반례: `case_comparison.yaml` 의 `degenerate_frac: 0.944444 → 0.123456` 로
    바꾸면 보고서가 **12% 를 그대로 렌더**하고 배너는 뜨지 않았다. F60 은
    fits digest 만 다시 봤고 숫자는 재계산하지 않았기 때문이다.
    """
    import yaml

    from tools.compare_cases import compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    h, _ = _complete_artifact(tmp_path / "h")
    m = yaml.safe_load((h / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["reference"] = "halfcell"
    (h / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    from tools.compare_objectives import run_compare
    run_compare(d, d)

    cc = compare(d / "fits.parquet", h / "fits.parquet")
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(cc, allow_unicode=True), encoding="utf-8")
    before = build(d, tmp_path / "R0.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "파생_case_comparison.yaml" not in before or "인용 금지" not in before[:600]

    # 비율 하나만 고친다
    tag = next(iter(cc["grid"]))
    cc["grid"][tag]["degenerate_frac"] = 0.123456
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(cc, allow_unicode=True), encoding="utf-8")
    after = build(d, tmp_path / "R1.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "파생_case_comparison.yaml" in after, "변조된 파생 숫자를 잡지 못했다"
    assert "인용 금지" in after[:600]
    assert before != after
