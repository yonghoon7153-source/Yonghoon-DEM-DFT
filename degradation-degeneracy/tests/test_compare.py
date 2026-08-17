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
                            # ★ 12차 발견 3 — 끝점 대조는 네 parameter 를 전부
                            #   본다 (a_pe·b_pe·a_ne·b_ne). 실제 fits 에는 항상
                            #   있으므로 fixture 도 갖춘다.
                            "a_pe": 1.0, "b_pe": 0.0,
                            "a_ne": 1.0, "b_ne": 0.0,
                            # ★ 11차 발견 5 — 끝점 일치 확인이 J 를 비교한다.
                            #   목적함수별 결정적 값이라 sweep 끝점과 본 실행이
                            #   같은 값을 갖는다 (정의가 같으므로 그래야 맞다).
                            "J": 0.1 + 0.01 * oi,
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
    # ★ F87 — 빈 placeholder 를 쓰지 않는다. "존재하지만 내용 없음"은 이제
    #   stale 로 잡히며, 그게 옳다 (저장본이 현재 fits 에 대응하지 않는다).
    #   필요한 테스트는 run_scoring 을 직접 부른다.

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "격차 붕괴" in text
    # ★ 15차 발견 2 — count 우선 렌더로 문구가 바뀌었다
    i_gap = text.index("두 전극을 같다고 답한 것은")
    i_22p = text.index("근방의 recovery failure")   # ★ 15차 발견 7 로 문구 변경
    assert i_gap < i_22p, "격차 붕괴 결론이 22p 근방 성적보다 앞에 와야 한다"
    # 붕괴율 100% → 사건률 비가 1 미만이어야 하고, "실제로 비슷" 결론이 나오면 안 된다
    import re
    m = re.search(r"사건률 비 = ([\d.]+)", text)
    assert m, "사건률 비가 결론에 없다"
    assert float(m.group(1)) < 1.0, f"붕괴율 100%인데 사건률 비가 {m.group(1)}"
    # ★ F28 — 사건률 비를 결론으로 승격시키면 안 된다. 세 제약이 항상 붙어야 한다.
    assert "실제로 비슷하게 열화했다" not in text, \
        "사건률 비를 '실제로 비슷하다'는 결론으로 승격시켰다"
    for must in ("임계 의존", "posterior가 아님", "부분집단 조건화"):
        assert must in text, f"사건률 비 제약 '{must}'이 빠졌다"


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
    # ★ F87 — 빈 placeholder 를 쓰지 않는다. "존재하지만 내용 없음"은 이제
    #   stale 로 잡히며, 그게 옳다 (저장본이 현재 fits 에 대응하지 않는다).
    #   필요한 테스트는 run_scoring 을 직접 부른다.

    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    # 붕괴가 0이면 사건률 비가 inf가 되는데, 그 경우에도 문서가 깨지지 않아야 한다
    import re
    assert re.search(r"사건률 비 = (\S+)", text), "사건률 비가 결론에 없다"
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
    # ★ F87 — 빈 placeholder 를 쓰지 않는다. "존재하지만 내용 없음"은 이제
    #   stale 로 잡히며, 그게 옳다 (저장본이 현재 fits 에 대응하지 않는다).
    #   필요한 테스트는 run_scoring 을 직접 부른다.

    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    # ★ 18차 발견 2 — 제목의 종수는 이제 표에서 나온다 (하드코딩 4 였다)
    import re as _re
    _m = _re.search(r"^## 목적함수 \d+종 비교$", text, _re.M)
    assert _m, "목적함수 비교 절 제목을 못 찾았다"
    head = text[:_m.start()]                              # 결론 구간만
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
    # ★ F87 — 빈 placeholder 를 쓰지 않는다. "존재하지만 내용 없음"은 이제
    #   stale 로 잡히며, 그게 옳다 (저장본이 현재 fits 에 대응하지 않는다).
    #   필요한 테스트는 run_scoring 을 직접 부른다.

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
    # ★ F87 — 빈 placeholder 를 쓰지 않는다. "존재하지만 내용 없음"은 이제
    #   stale 로 잡히며, 그게 옳다 (저장본이 현재 fits 에 대응하지 않는다).
    #   필요한 테스트는 run_scoring 을 직접 부른다.
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


def _complete_artifact(tmp_path, repo_root=None, objectives=("pocv_dvdq",)):
    """provenance 검사를 **실제로** 통과하는 artifact.

    ★ F43/F50/F56/F57 — 이 fixture 는 세 번 깨졌다. 매번 validator 를 강화하자
      "통과한다고 부르던 것"이 실제로는 통과하면 안 되는 것이었음이 드러났다.
      지금은 진짜 입력 파일 · 진짜 해시 · 시작 봉인 map · 디스크의 start/attempt
      파일까지 갖춘다.
    """
    import hashlib
    import json

    import yaml

    from src.io import (canonical_input_key, env_fingerprint, file_digest,
                        seal_inputs, source_digest)
    _k = lambda p: canonical_input_key(p, repo_root)   # noqa: E731

    d = Path(tmp_path) / "res"
    d.mkdir(parents=True, exist_ok=True)

    cfg = d / "base.yaml"              # 이름이 필수 입력 판정에 쓰인다 (F50)
    cfg.write_text("dummy: 1\n", encoding="utf-8")
    # ★ F70/F74 — 곡선 producer 기록 (upstream truth 봉인).
    #   ★ 11차 발견 3 — fit artifact 의 validator 가 봉인된 producer 를 **다시
    #   검증**하므로, fixture 도 서명·행별 sig·시작 기록·replay_recipe 를 갖춘
    #   진짜 producer 여야 한다 (예전엔 solver 만 적힌 껍데기였다).
    from tests.test_fitting import sign_producer
    sign_producer(d, _fits(objectives=("pocv_dvdq",)))
    curves = d / "curves.parquet"
    prod = d / "curves_manifest.yaml"
    prod_start = d / "curves_manifest_start.yaml"

    sealed = seal_inputs([curves, cfg, prod, prod_start], repo_root=repo_root)
    # ★ F68 — 조건 집합 서명은 **실제 fits 의 조건**에서 나와야 한다.
    #   하드코딩하면 그 자체가 위조 통로가 된다.
    from src.io import _sha256_lines
    _df0 = _fits(objectives=tuple(objectives))
    _conds = sorted(set(_df0["cond_id"].astype(str)))
    src = source_digest()
    env = env_fingerprint()
    attempt_id = "20260807T000000_1_000"

    # ★ 11차 발견 5 — 끝점 동치 검사가 **가중치 정의**를 비교하므로 fixture 도
    #   configs/objectives.yaml 의 실제 정의를 쓴다 (이름만 같으면 안 된다).
    _W = {"pocv": {"w_pocv": 1.0},
          "pocv_dvdq": {"w_pocv": 1.0, "w_dvdq": 1.0},
          "pocv_dvdq_dqdv": {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 1.0},
          "dqdv_only": {"w_dqdv": 1.0}}
    spec = {"sig_version": 5,
            "objectives": {o: _W.get(o, {"w_pocv": 1.0}) for o in objectives},
            # ★ F67 — 계산을 고정하는 축들. 설정만으론 부족하다.
            "objective_order": list(objectives),
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
            "curves_sha": sealed[_k(curves)],
            "base_config_sha": sealed[_k(cfg)],
            "producer_sha": sealed[_k(prod)],
            "producer": {"config_hash": "test", "solver": "test",
                         "curves_sha256": file_digest(curves, full=True)},
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
    # ★ F72 — 계산은 봉인한 바이트(스냅샷)만 읽는다. fixture 도 실제로 떠 둔다.
    from src.io import snapshot_inputs
    snapshot_inputs(sealed, d, repo_root=repo_root)
    # ★ F87 — 빈 placeholder 를 쓰지 않는다. "존재하지만 내용 없음"은 이제
    #   stale 로 잡히며, 그게 옳다 (저장본이 현재 fits 에 대응하지 않는다).
    #   필요한 테스트는 run_scoring 을 직접 부른다.
    (d / "manifest.yaml").write_text(yaml.safe_dump({
        "config_hash": "deadbeef1234", "git_dirty": False, "reproducible": True,
        "run_signature": sig, "run_spec": spec,
        "start_provenance": start, "attempt_id": attempt_id,
        "git_commit_changed_during_run": False,
        "source_digest_changed_during_run": False,
        "inputs_changed_during_run": False,
        "input_sha256": sealed, "input_sha256_source": "sealed_at_start",
        "input_sha256_at_end": dict(sealed), "inputs_changed_during_run": False,
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


# ──────────────────────────── F71: archive fail-closed (7차 게이트 리뷰 발견 8)

def _nested_sweep(run_dir):
    """run_dir 안에 자기 manifest 를 가진 하위 실행(wsweep) 을 만든다."""
    import shutil

    sub = Path(run_dir) / "wsweep"
    sub.mkdir(exist_ok=True)
    for n in ("manifest.yaml", "manifest_start.yaml", "fits.parquet",
              "curves.parquet", "base.yaml", "curves_manifest.yaml"):
        if (Path(run_dir) / n).is_file():
            shutil.copy2(Path(run_dir) / n, sub / n)
    shutil.copytree(Path(run_dir) / "attempts", sub / "attempts", dirs_exist_ok=True)
    return sub


def test_bundle_includes_nested_sweep_provenance(tmp_path):
    """★ F71/8-2 — 하위 sweep 의 manifest·start·attempts 가 묶음에 들어가야 한다.

    반례: 초판은 `wsweep/` 에서 fits 와 요약만 복사했다. 복원된 sweep 은 14개
    검사가 실패했는데 배너는 sweep provenance 를 합산하지 않아 조용히 지나갔다.
    """
    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    _nested_sweep(d)

    out = tmp_path / "art"
    res = bundle(d, out)
    assert res["nested"] == ["wsweep"], res
    for n in ("manifest.yaml", "manifest_start.yaml", "fits.parquet"):
        assert (out / "wsweep" / n).is_file(), n
    assert (out / "wsweep" / "attempts").is_dir()
    assert check(out)["ok"], check(out)["missing"]


def test_bundle_staging_removes_stale_files(tmp_path):
    """★ F71/8-4 — source 에서 사라진 파일이 옛 묶음에 남아 통과시키면 안 된다."""
    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)
    assert (out / "fits.parquet").is_file()

    (d / "fits.parquet").unlink()
    res = bundle(d, out)
    assert any("fits.parquet" in m for m in res["missing"]), res
    assert not (out / "fits.parquet").exists(), "옛 묶음의 잔재가 남았다"
    assert not check(out)["ok"]


def test_check_detects_payload_tampering(tmp_path):
    """★ F71 — 묶음 안에서 파일이 바뀌면 payload 재해시로 잡는다."""
    import pandas as pd

    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)
    assert check(out)["ok"]

    f = pd.read_parquet(out / "fits.parquet")
    f["lam_pe_hat"] = f["lam_pe_hat"] + 0.5
    f.to_parquet(out / "fits.parquet", index=False)
    res = check(out)
    assert not res["ok"] and any("payload" in m for m in res["missing"]), res


def test_restore_refuses_conflicting_existing_files(tmp_path):
    """★ F71/8-3 — 기존 파일을 바이트 비교 없이 건너뛰면 안 된다.

    반례: archive 의 fits 와 dest 의 fits 가 다른데(`lam_pe_hat += 0.321`)
    restore 가 skip 처리했고, 그 뒤 validate 는 **원본**을 검증해 통과했다.
    즉 "묶음을 검증했다"는 말이 거짓이었다.
    """
    import pandas as pd

    from tools.archive_bundle import bundle, restore

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)

    f = pd.read_parquet(d / "fits.parquet")
    f["lam_pe_hat"] = f["lam_pe_hat"] + 0.321
    f.to_parquet(d / "fits.parquet", index=False)

    res = restore(out, run_dir=d, repo_root=tmp_path)
    assert res["ok"] is False
    assert any("fits.parquet" in c for c in res["conflict"]), res

    res2 = restore(out, run_dir=d, force=True, repo_root=tmp_path)
    assert res2["ok"] and any("fits.parquet" in w for w in res2["written"])


def test_restore_blocks_path_traversal(tmp_path):
    """★ F71/8-6 — restore_map 의 `..`·절대경로로 저장소 밖에 쓸 수 없다.

    반례: `inputs/payload.txt: ../escaped.txt` 를 넣은 묶음이 repository root
    **밖에** 파일을 썼다. 외부에서 받은 묶음에 restore 를 돌릴 수 있으므로
    임의 쓰기는 그 자체로 결함이다.
    """
    import pytest
    import yaml

    from tools.archive_bundle import _safe_target, bundle

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)

    meta = yaml.safe_load((out / "restore_map.yaml").read_text(encoding="utf-8"))
    meta["inputs"] = {"inputs/payload.txt": "../escaped.txt"}
    (out / "inputs").mkdir(exist_ok=True)
    (out / "inputs" / "payload.txt").write_text("x", encoding="utf-8")
    (out / "restore_map.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")

    for bad in ("../escaped.txt", "/etc/passwd", "a/../../b"):
        with pytest.raises(ValueError):
            _safe_target(bad, tmp_path)
    assert not (tmp_path.parent / "escaped.txt").exists()


def test_bundle_includes_tracked_inputs_for_portability(tmp_path):
    """★ F71/8-5 — git tracked 입력도 exact bytes 로 동봉한다.

    저장소에 EOL 정책이 없으면 Windows clone 의 `configs/base.yaml` 은 LF blob 과
    다른 바이트가 된다. validator 는 raw bytes 를 재해시하므로 Linux artifact 를
    Windows clone 에서 검증하면 실패한다.
    """
    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)
    # 이 fixture 의 입력은 run_dir 안에 있으므로 이름 그대로 동봉된다
    assert (out / "base.yaml").is_file()
    assert (out / "curves.parquet").is_file()
    assert (out / "curves_manifest.yaml").is_file()
    assert check(out)["ok"], check(out)["missing"]

    # 저장소 EOL 정책도 있어야 한다 (clone 시점의 바이트를 고정한다)
    ga = Path(__file__).resolve().parent.parent / ".gitattributes"
    assert ga.is_file() and "eol=lf" in ga.read_text(encoding="utf-8")


def test_bundle_restores_and_validates_in_isolated_root(tmp_path):
    """★ F71/8-1 — **다른 clone** 에서 복원해도 검증을 통과해야 한다.

    반례: half-cell 캐시 경로가 절대경로로 봉인돼, relocated clone 에서
    `입력_digest_재해시` 가 "파일 없음"으로 실패했다 (`bundle check = False`,
    `relocated clone validate = False`). F65 로 봉인 키를 저장소 상대경로로
    정규화했고, 여기서 그 왕복을 실제로 돌린다.

    이 테스트가 `scripts/archive_results.sh` 가 매 보관마다 자동으로 하는 것과
    같은 절차다 — 원본 `results/` 가 남은 서버에서 검증하면 묶음이 아니라
    원본을 검증하게 되므로, 반드시 빈 root 에서 해야 한다.
    """
    import shutil

    from src.io import validate_provenance
    from tools.archive_bundle import bundle, check, restore

    # 가짜 저장소 root 를 만들고 그 안에서 봉인한다 (경로가 전부 상대가 된다)
    home = tmp_path / "repo_a"
    (home / "results").mkdir(parents=True)
    d, _ = _complete_artifact(home / "results", repo_root=home)
    assert validate_provenance(d, repo_root=home)["checks"]["입력_digest_재해시"] == "통과"

    out = tmp_path / "artifacts" / "run"
    assert not bundle(d, out, repo_root=home)["missing"]
    assert check(out)["ok"], check(out)["missing"]

    # 완전히 다른 root 로 복원 — 원본은 지워서 "원본을 검증"할 여지를 없앤다
    away = tmp_path / "repo_b"
    away.mkdir()
    res = restore(out, repo_root=away)
    shutil.rmtree(home)

    v = validate_provenance(res["run_dir"], repo_root=away)
    for k in ("입력_digest_재해시", "출력봉인_재계산", "start_파일_존재",
              "attempt_파일_존재", "producer_곡선일치", "조건집합_서명일치"):
        assert v["checks"][k] == "통과", f"{k}: {v['checks'][k]}"


def test_dirty_scope_ignores_unrelated_subproject(tmp_path):
    """★ F73 — 저장소를 공유하는 **다른 프로젝트** 수정이 이 실행을 오염시키면 안 된다.

    실측: V100 에서 `se_curve/xfer_kit_ps_7_3_*.json` 2개(MPM/DEM 쪽 산출물)가
    수정돼 있어서 `git_dirty=True` 가 됐다. 그대로 본 실행을 돌리면 열 시간짜리
    산출물이 전부 `clean_worktree` 실패로 인용 불가가 된다.

    판정을 **느슨하게** 하는 변경이므로 두 가지를 함께 보장한다.
      · 범위 안(src/tools/configs/scripts/run.sh/requirements) 수정은 여전히 dirty
      · 범위 밖 수정도 `git_dirty_out_of_scope` 에 **반드시 기록**된다 (숨기지 않는다)
    """
    import subprocess

    from src.io import git_info

    repo = tmp_path / "mono"
    (repo / "proj" / "src").mkdir(parents=True)
    (repo / "other").mkdir()
    for f, body in ((repo / "proj" / "src" / "a.py", "x = 1\n"),
                    (repo / "other" / "b.json", '{"v": 1}\n')):
        f.write_text(body, encoding="utf-8")

    def git(*a, cwd=repo):
        return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)

    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    git("add", "-A")
    git("commit", "-qm", "init")

    proj = repo / "proj"
    assert git_info(proj)["git_dirty"] is False

    # ① 다른 프로젝트만 수정 → 이 실행은 clean 이어야 한다
    (repo / "other" / "b.json").write_text('{"v": 2}\n', encoding="utf-8")
    g = git_info(proj)
    assert g["git_dirty"] is False, g
    assert g["git_dirty_repo_wide"] is True
    assert any("other/b.json" in x for x in g["git_dirty_out_of_scope"]), g

    # ② 이 프로젝트의 코드 수정 → 반드시 dirty
    (proj / "src" / "a.py").write_text("x = 2\n", encoding="utf-8")
    g = git_info(proj)
    assert g["git_dirty"] is True
    assert any("src/a.py" in x for x in g["git_dirty_files_in_scope"]), g


def test_dirty_scope_bypasses_are_closed(tmp_path):
    """★ F75/8차 발견 4 — F73 의 세 우회를 닫는다.

    반례 (전부 리뷰 실측):
      4-a  `git mv proj/src/a.py other/a.py` → rename 탐지가 새 경로만 줘서
           실행 source 를 **삭제한** tracked 변경이 clean 승인
      4-b  untracked `src/한글.py` → quoting("src/\355...") 때문에
           `startswith("src/")` 실패 → clean
      4-c  `.gitignore` 의 `*.parquet` 규칙에 걸린 `configs/lookup.parquet` →
           untracked 목록에 아예 안 나와 clean. source_digest 는 내용을 해시해도
           **clean clone 에는 그 파일이 없어** 재현이 불가능하다
    """
    import subprocess

    from src.io import git_info

    repo = tmp_path / "mono"
    (repo / "proj" / "src").mkdir(parents=True)
    (repo / "proj" / "configs").mkdir()
    (repo / "other").mkdir()
    (repo / "proj" / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
    (repo / ".gitignore").write_text("*.parquet\n*.local\n", encoding="utf-8")

    def git(*a):
        return subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True)

    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    git("add", "-A")
    git("commit", "-qm", "init")

    proj = repo / "proj"
    assert git_info(proj)["git_dirty"] is False

    # 4-a — 실행 범위 밖으로 rename
    git("mv", "proj/src/a.py", "other/a.py")
    g = git_info(proj)
    assert g["git_dirty"] is True, f"rename-out 이 clean 으로 승인됐다: {g}"
    git("mv", "other/a.py", "proj/src/a.py")     # 원복
    assert git_info(proj)["git_dirty"] is False

    # 4-b — 비ASCII untracked (critical 경로)
    (proj / "src" / "한글.py").write_text("x = 1\n", encoding="utf-8")
    g = git_info(proj)
    assert g["git_dirty"] is True, f"한글 경로 untracked 가 clean 이다: {g}"
    assert any("한글" in x for x in g["git_untracked_critical"]), g
    (proj / "src" / "한글.py").unlink()

    # 4-c — ignored 인데 실행 경로에 있는 입력
    (proj / "configs" / "lookup.parquet").write_bytes(b"data")
    (proj / "src" / "settings.local").write_text("k=v\n", encoding="utf-8")
    g = git_info(proj)
    assert g["git_dirty"] is True, f"ignored 실행 입력이 clean 이다: {g}"
    assert any("lookup.parquet" in x for x in g["git_untracked_critical"]), g


def test_validator_rejects_duplicate_swap_with_resealed_record(tmp_path):
    """★ F76/8차 발견 5 — 한 조합을 다른 조합의 중복으로 바꾸고 봉인 기록까지
    재계산해 넣어도 잡아야 한다.

    반례: 2조건×2목적함수에서 ('c0','b') 를 ('c1','b') 중복으로 교체 + reseal →
    KEYS 에 ('c1','b') 가 두 번, ('c0','b') 없음인데 VALID_AFTER_DUP_RESEAL=True.
    조건 집합·행 수·objectives 집합이 전부 보존되기 때문이다.
    """
    import pandas as pd
    import yaml

    from src.io import fits_seal, validate_provenance

    d, _ = _complete_artifact(tmp_path, objectives=("aa", "bb"))
    assert validate_provenance(d)["ok"], validate_provenance(d)["fail"]

    f = pd.read_parquet(d / "fits.parquet")
    conds = sorted(set(f["cond_id"]))
    c0, c1 = conds[0], conds[1]
    # ('c0','bb') 행의 cond_id 를 c1 로 바꾼다 → ('c1','bb') 중복, ('c0','bb')
    # 누락. c0 는 ('c0','aa') 로 여전히 존재하므로 **조건 집합은 보존**된다 —
    # 리뷰 반례 그대로다.
    i = f[(f["cond_id"] == c0) & (f["objective"] == "bb")].index[0]
    f.loc[i, "cond_id"] = c1
    f.to_parquet(d / "fits.parquet", index=False)

    m = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    m["fits_seal"] = fits_seal(d / "fits.parquet")       # 기록을 파일에 맞춘다
    (d / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    v = validate_provenance(d)
    assert not v["ok"], "중복 교체 + reseal 이 통과했다"


def test_report_renders_recomputed_not_saved_yaml(tmp_path):
    """★ F77/8차 발견 6 — 저장 YAML 을 바꿔도 보고서 숫자는 안 바뀌어야 한다.

    반례 (전부 리뷰 실측, 배너 없음):
      · objective table `0.944… → 0.123456` 이 그대로 렌더
      · `degeneracy_summary.n_rows_recoverable → 987654` 렌더
      · sweep `optimum w → 123.456` 렌더
    `_flat_pairs` 가 list 를 건너뛰었고 summary·sweep 은 재검산 자체가 없었다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    run_compare(d, d)
    from src.scoring import run_scoring
    run_scoring(d)

    base = build(d, tmp_path / "R0.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "인용 금지" not in base[:600], base[:600]

    # ① list 안의 표 숫자 변조
    y = yaml.safe_load((d / "objective_comparison.yaml").read_text(encoding="utf-8"))
    orig = y["table"][0]["degenerate_frac"]
    y["table"][0]["degenerate_frac"] = 0.123456
    (d / "objective_comparison.yaml").write_text(
        yaml.safe_dump(y, allow_unicode=True), encoding="utf-8")

    # ② summary 변조
    s = yaml.safe_load((d / "degeneracy_summary.yaml").read_text(encoding="utf-8"))
    s["n_rows_recoverable"] = 987654
    (d / "degeneracy_summary.yaml").write_text(
        yaml.safe_dump(s, allow_unicode=True), encoding="utf-8")

    out = build(d, tmp_path / "R1.md", repo_root=tmp_path).read_text(encoding="utf-8")
    # 변조 값이 렌더되지 않고
    assert "12.3456" not in out and "0.123456" not in out
    assert "987654" not in out
    # 배너가 뜬다
    assert "인용 금지" in out[:600]
    assert "파생_stale_objective_comparison.yaml" in out
    assert "파생_stale_degeneracy_summary.yaml" in out
    # 진짜 값은 여전히 실린다
    assert f"{100 * orig:.0f}%" in out


def test_compare_cases_rejects_different_optimizer_pipeline(tmp_path):
    """★ F78/8차 발견 7 — optimizer 정책이 다른 두 실행은 "기준 곡선 효과"가
    아니다. 예전 공통성 검사는 curves·objectives·v_col·조건집합만 봤다."""
    import yaml

    from tools.compare_cases import compare

    a, _ = _complete_artifact(tmp_path / "a")
    b, _ = _complete_artifact(tmp_path / "b")
    m = yaml.safe_load((b / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["reference"] = "halfcell"
    m["run_spec"]["optimizer"] = dict(m["run_spec"]["optimizer"], adaptive=False)
    (b / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    res = compare(a / "fits.parquet", b / "fits.parquet")
    assert res["provenance_ok"] is False
    assert res["공통_run_spec"]["optimizer"]["일치"] is False
    assert "optimizer 정책" in res["_주의_공통성"]


def test_compare_cases_scopes_causal_claim_to_pipeline(tmp_path):
    """★ F78 — bounds preset 이 다르면(설계상 그렇다) 인과 문구가 pipeline
    수준으로 제한돼야 한다."""
    import yaml

    from tools.compare_cases import compare

    a, _ = _complete_artifact(tmp_path / "a")
    b, _ = _complete_artifact(tmp_path / "b")
    m = yaml.safe_load((b / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["reference"] = "halfcell"
    m["run_spec"]["bounds_preset"] = "halfcell"
    (b / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    res = compare(a / "fits.parquet", b / "fits.parquet")
    assert "bounds_preset" in res["reference별_허용차이"]
    assert "pipeline" in res["_인과범위"]
    assert "기준 곡선 단독" in res["_인과범위"]


def test_archive_wrapper_style_provenance_json_survives_payload(tmp_path):
    """★ F80/9-a — provenance.json 이 payload 를 깨지 않아야 한다.

    반례: wrapper 가 bundle **뒤** 묶음 안에 provenance.json 을 추가해, 방금 만든
    payload digest 목록과 즉시 어긋났다 — 정상 묶음을 스스로 무효화했다.
    이제 wrapper 는 bundle 전에 원본 실행 디렉터리에 쓰고 KEEP_FILES 가 담는다.
    """
    import json

    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    (d / "provenance.json").write_text(json.dumps({"ok": True}), encoding="utf-8")
    out = tmp_path / "art"
    bundle(d, out)
    assert (out / "provenance.json").is_file()
    assert check(out)["ok"], check(out)["missing"]


def test_restore_refuses_tampered_bundle(tmp_path):
    """★ F80/9-d — 변조된 묶음(check 실패)은 direct restore 도 거부해야 한다."""
    import yaml

    from tools.archive_bundle import bundle, restore

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)

    y = yaml.safe_load(
        (out / "curves_manifest.yaml").read_text(encoding="utf-8")) or {}
    y["tampered"] = 123
    (out / "curves_manifest.yaml").write_text(yaml.safe_dump(y), encoding="utf-8")

    res = restore(out, run_dir=tmp_path / "dest", repo_root=tmp_path)
    assert res["ok"] is False
    assert any("check 실패" in c for c in res["conflict"]), res


def test_safe_target_rejects_prefix_sibling(tmp_path):
    """★ F80/9-f — `/a` 가 `/ab/...` 에 매칭되는 접두사 버그."""
    import pytest

    from tools.archive_bundle import _safe_target

    root = tmp_path / "a"
    root.mkdir()
    (tmp_path / "ab").mkdir()
    # 형제 디렉터리 /ab 로 나가는 상대경로 — 문자열 startswith 로는 통과했다
    with pytest.raises(ValueError):
        _safe_target("../ab/x.txt", root)


def test_payload_keys_are_posix(tmp_path):
    """★ F80/9-c — payload 키는 OS 무관하게 POSIX 구분자여야 한다."""
    import yaml

    from tools.archive_bundle import bundle

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)
    keys = list((yaml.safe_load(
        (out / "payload_sha256.yaml").read_text(encoding="utf-8")) or {}))
    assert any("attempts/" in k for k in keys)
    assert not any("\\" in k for k in keys)


def test_grid_producer_bundle_uses_producer_schema(tmp_path):
    """★ F80/9-e — grid producer 는 fits 없이도 완비 묶음이어야 한다.

    반례: REQUIRED_RUN_FILES 가 모든 artifact 에 fits.parquet 과
    manifest_start.yaml 을 요구해 **정상 grid artifact 도 반드시 실패**했다
    (기본 보관 대상에 grid_curves_v3 가 있는데도).
    """
    import pandas as pd
    import yaml

    from tools.archive_bundle import artifact_kind, bundle, check

    # _tiny_curves 형식의 producer 디렉터리 (fit 없음)
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from tests.test_fitting import _tiny_curves
    d = _tiny_curves(tmp_path / "curves")
    (d / "manifest.yaml").write_text(yaml.safe_dump(
        {"run_type": "grid", "config_hash": "test"}), encoding="utf-8")
    assert artifact_kind(d) == "grid_producer"

    out = tmp_path / "art"
    res = bundle(d, out)
    assert not res["missing"], res["missing"]
    assert check(out)["ok"], check(out)["missing"]
    assert (out / "curves.parquet").is_file()
    assert (out / "curves_manifest_start.yaml").is_file()


def test_empty_saved_yaml_is_stale(tmp_path):
    """★ F87/9차 발견 8 — 저장본이 빈 mapping 이면 stale 로 잡아야 한다.

    `_flat_pairs` 는 저장본 key 를 중심으로 순회하므로 빈 문서는 비교할 쌍이
    0개가 되어 "일치"로 판정됐다. 표 숫자는 재계산본을 렌더하니 직접 오염은
    없지만, 저장본이 현재 fits 에 대응한다는 보장이 사라진다.
    """
    import yaml

    from src.scoring import run_scoring
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    run_compare(d, d)
    run_scoring(d)
    assert "인용 금지" not in build(
        d, tmp_path / "R0.md", repo_root=tmp_path).read_text(encoding="utf-8")[:600]

    # 저장본만 빈 mapping 으로 바꾼다 — 예전에는 falsy 라 조건 자체를 건너뛰어
    # "일치"로 판정됐다
    (d / "degeneracy_summary.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    out = build(d, tmp_path / "R1.md", repo_root=tmp_path).read_text(encoding="utf-8")
    assert "파생_stale_degeneracy_summary.yaml" in out
    assert "인용 금지" in out[:600]


# ──────────────────────────────── 10차 게이트 리뷰 (Codex 9차-재실행-전 + 자체)

def test_report_survives_multistart_meta_keys(tmp_path):
    """★ 10차 발견 3 — n_restarts≥3 이면 `multistart_random_only` 블록에
    `random_only_적용`(bool)·`평균_제외_restart수`(float)·`pairwise`(dict) 같은
    메타 키가 생기는데, `_` 접두사만 거르던 렌더가 bool 에 `.get()` 을 불러
    보고서 생성이 통째로 죽었다 (리뷰 실측: AttributeError). 목적함수 행의
    스키마를 가진 dict 만 표에 올라야 한다."""
    import json

    import yaml

    from src.io import fits_seal
    from src.scoring import run_scoring
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path, objectives=("pocv", "pocv_dvdq"))
    # 무작위 restart 2개 이상 → random-only 공정 비교가 성립 → 메타 키가 생긴다
    f = pd.read_parquet(d / "fits.parquet")
    f["restarts_json"] = json.dumps(
        [{"p": [1.0, 0.0, 1.0, 0.0], "J": 0.0, "i": 0, "source": "base_init"},
         {"p": [1.1, 0.1, 1.1, 0.1], "J": 0.5, "i": 1, "source": "random"},
         {"p": [1.6, 0.2, 1.2, 0.2], "J": 0.7, "i": 2, "source": "random"}])
    f.to_parquet(d / "fits.parquet", index=False)
    man = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    man["fits_seal"] = fits_seal(d / "fits.parquet")
    (d / "manifest.yaml").write_text(
        yaml.safe_dump(man, allow_unicode=True, sort_keys=False), encoding="utf-8")

    # 전제조건 — 재채점 요약에 비-dict 메타 키가 실제로 있어야 이 테스트가 유효
    s = run_scoring(d, out_dir=tmp_path / "sc")
    blk = s.get("multistart_random_only") or {}
    assert any(not str(k).startswith("_") and not isinstance(v, dict)
               for k, v in blk.items()), "메타 키 미생성 — 크래시 경로가 재현되지 않았다"

    run_compare(d, d)
    text = build(d, tmp_path / "R.md",
                 repo_root=tmp_path).read_text(encoding="utf-8")   # 죽으면 안 된다
    assert "multi-start 진단" in text
    assert "| random_only_적용 |" not in text, "메타 키가 표 행으로 렌더됐다"
    assert "| pairwise |" not in text


def test_report_renders_recomputed_case_numbers(tmp_path):
    """★ 10차 발견 5 — case 표의 `n_conditions_*` 를 999999 로 바꿔도 예전
    재검산은 세 지표만 대조해 통과했고, 보고서가 999999 를 그대로 실었다.
    이제 표는 재계산본에서 렌더되고 숫자 전체 대조로 stale 이 뜬다."""
    import yaml

    from tools.compare_cases import compare
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    h, _ = _complete_artifact(tmp_path / "h")
    m = yaml.safe_load((h / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["reference"] = "halfcell"
    (h / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    run_compare(d, d)

    cc = compare(d / "fits.parquet", h / "fits.parquet")
    cc["n_conditions_compared"] = 999999          # 세 지표 밖이던 숫자
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(cc, allow_unicode=True), encoding="utf-8")
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "999999" not in text, "변조된 숫자가 보고서에 렌더됐다"
    assert "파생_case_comparison.yaml" in text
    assert "인용 금지" in text[:600]


def _wsweep_run(d, objectives=("wdqdv_0.00", "wdqdv_1.00"),
                optimizer=None, n_restarts=None, ws_extra=None):
    """본 실행 artifact `d` 안에 provenance 를 갖춘 wsweep 하위 실행을 만든다.

    manifest run_spec 을 sweep 목적함수로 바꾸고 서명·행 서명·fits_seal 을
    다시 계산한다 — validator 가 실제로 통과하는 sweep 이어야 F88 대조 검사
    자체를 테스트할 수 있다.
    """
    import hashlib
    import json

    import yaml

    from src.io import fits_seal, snapshot_inputs
    from src.scoring import (add_error_columns, apply_bias_correction,
                             classify_recoverability, clean_bias)
    from src.weight_sweep import pick_optimum, sweep_summary

    sub = _nested_sweep(d)
    man = yaml.safe_load((sub / "manifest.yaml").read_text(encoding="utf-8"))
    spec = man["run_spec"]
    spec["objectives"] = {o: {"w_pocv": 1.0, "w_dvdq": 1.0,
                              "w_dqdv": float(o.split("_")[1])}
                          for o in objectives}
    spec["objective_order"] = list(objectives)
    if optimizer:
        spec["optimizer"] = {**spec["optimizer"], **optimizer}
    if n_restarts is not None:
        spec["n_restarts"] = n_restarts
        spec["optimizer"]["n_restarts"] = n_restarts
    sig = hashlib.sha1(json.dumps(spec, sort_keys=True, default=str)
                       .encode()).hexdigest()[:12]

    f = _fits(objectives=tuple(objectives))
    f["run_sig"] = sig
    idxs = (list(range(int(spec["optimizer"]["n_restarts"])))
            if spec["optimizer"].get("adaptive") is False else [0, 1])
    f["restarts_json"] = json.dumps(
        [{"p": [1.0 + 0.1 * i, 0.0, 1.0, 0.0], "J": 0.1 * i, "i": i,
          "source": "base_init" if i == 0 else "random"} for i in idxs])
    f.to_parquet(sub / "fits.parquet", index=False)

    man["run_signature"] = sig
    man["run_spec"] = spec
    man["fits_seal"] = fits_seal(sub / "fits.parquet")
    (sub / "manifest.yaml").write_text(
        yaml.safe_dump(man, allow_unicode=True, sort_keys=False), encoding="utf-8")
    snapshot_inputs(man["input_sha256"], sub)

    tol = 0.02
    sw = classify_recoverability(add_error_columns(
        pd.read_parquet(sub / "fits.parquet"), tol))
    sw = apply_bias_correction(sw, clean_bias(sw), tol)
    opt = pick_optimum(sweep_summary(sw, tol))
    # ★ 14차 3차 — 실제 `run_weight_sweep` 이 쓰는 키를 그대로 갖춘다.
    #   `stride` 가 빠져 있어서 재현 명령의 `--w-stride` 오류를 fixture 가
    #   가렸다 (기본 sweep metadata 에는 항상 있다).
    ws = {"w_grid": [float(o.split("_")[1]) for o in objectives],
          "stride": 2,
          "tol": tol,
          "method": spec["optimizer"]["method"],
          "adaptive": spec["optimizer"]["adaptive"],
          "n_restarts": spec["n_restarts"],
          "n_conditions": spec["n_conditions"],
          "warm_start": spec["warm_start"],
          "optimum": opt}
    if ws_extra:
        ws.update(ws_extra)
    (sub / "weight_sweep.yaml").write_text(
        yaml.safe_dump(ws, allow_unicode=True), encoding="utf-8")
    return sub


def test_sweep_settings_verified_against_main_spec(tmp_path):
    """★ 10차 발견 4 — "본 실행과 같은 설정" 문장은 자기신고가 아니라
    두 run_spec 의 대조로 판정한다."""
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    # ① 같은 설정 — 대조로 확인된 초록 문장.
    #    ★ 11차 발견 5 — 끝점 두 개(w=0 ≡ pocv_dvdq, w=1 ≡ pocv_dvdq_dqdv)가
    #    본 실행에 다 있어야 "같은 답을 낸다"를 실제로 확인할 수 있다.
    d, _ = _complete_artifact(tmp_path / "same",
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    _wsweep_run(d)
    run_compare(d, d)
    text = build(d, tmp_path / "R_same.md",
                 repo_root=tmp_path).read_text(encoding="utf-8")
    assert "같은 설정으로 돌렸습니다" in text
    assert "설정이 다릅니다" not in text
    assert "wsweep metadata 불일치" not in text

    # ② sweep 이 실제로 다른 설정 (adaptive off·restart 3) — 자기신고는
    #    spec 과 일치시켜 두므로(F88 은 통과) 본 실행과의 대조만 남는다
    d2, _ = _complete_artifact(tmp_path / "diff",
                               objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    _wsweep_run(d2, optimizer={"adaptive": False}, n_restarts=3)
    run_compare(d2, d2)
    text2 = build(d2, tmp_path / "R_diff.md",
                  repo_root=tmp_path).read_text(encoding="utf-8")
    assert "설정이 다릅니다" in text2
    assert "같은 설정으로 돌렸습니다" not in text2


def test_sweep_wgrid_selfreport_checked_against_spec(tmp_path):
    """★ 10차 발견 4 — weight_sweep.yaml 의 w_grid 자기신고를 서명된 spec 의
    목적함수 이름(wdqdv_X.XX)에서 재구성해 대조한다."""
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    # 실제로는 {0, 1} 만 돌았는데 기록은 더 촘촘한 sweep 을 주장한다
    _wsweep_run(d, ws_extra={"w_grid": [0.0, 0.5, 1.0]})
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "wsweep metadata 불일치" in text
    assert "인용 금지" in text[:600]


def test_bundle_refuses_seal_mismatched_bytes(tmp_path):
    """★ 10차 자체 리뷰 — 봉인 기록과 다른 bytes 는 **묶지 않는다.**

    예전에는 실행 후 변조된 fits 도 현재 bytes 그대로 담아 payload 를
    만들었으므로 check() 가 "온전"을 인증했고, 재보관(staging 교체)이 마지막
    정상 묶음을 파괴했다.
    """
    import pytest

    from tools.archive_bundle import bundle, check

    d, _ = _complete_artifact(tmp_path)
    out = tmp_path / "art"
    bundle(d, out)
    assert check(out)["ok"]

    f = pd.read_parquet(d / "fits.parquet")
    f["lam_pe_hat"] = f["lam_pe_hat"] + 0.5      # fits_seal 은 그대로 둔 변조
    f.to_parquet(d / "fits.parquet", index=False)
    with pytest.raises(RuntimeError, match="봉인 불일치"):
        bundle(d, out)
    assert check(out)["ok"], "실패한 재보관이 기존 정상 묶음을 파괴했다"


def test_nested_external_inputs_restored(tmp_path):
    """★ 10차 자체 리뷰 — nested 실행의 외부 봉인 입력은 최상위 `inputs/` 에
    묶여야 restore 가 실제로 복원한다. 예전에는 `<bundle>/wsweep/inputs/` 에
    떨어져 restore 가 절대 읽지 않는 죽은 사본이 됐다."""
    import yaml

    from src.io import canonical_input_key, file_digest
    from tools.archive_bundle import bundle, restore

    root = tmp_path
    d, _ = _complete_artifact(root / "a", repo_root=root)
    sub = _nested_sweep(d)
    # sweep 에만 있는 외부 봉인 입력 (run_dir 밖)
    ext = root / "a" / "ext_only_for_sweep.yaml"
    ext.write_text("k: 1\n", encoding="utf-8")
    m = yaml.safe_load((sub / "manifest.yaml").read_text(encoding="utf-8"))
    m["input_sha256"][canonical_input_key(ext, root)] = file_digest(ext)
    (sub / "manifest.yaml").write_text(
        yaml.safe_dump(m, allow_unicode=True, sort_keys=False), encoding="utf-8")

    out = tmp_path / "art"
    bundle(d, out, repo_root=root)
    assert (out / "inputs" / "ext_only_for_sweep.yaml").is_file(), \
        "외부 입력이 최상위 inputs/ 에 없다"
    assert not (out / "wsweep" / "inputs").exists(), \
        "restore 가 읽지 않는 위치(wsweep/inputs)에 사본이 남았다"

    iso = tmp_path / "iso"
    res = restore(out, repo_root=iso)
    assert res["ok"], res["conflict"]
    restored = iso / canonical_input_key(ext, root)
    assert restored.is_file() and restored.read_text(encoding="utf-8") == "k: 1\n", \
        "복원본에 외부 입력이 없다 — 죽은 사본이었다"


# ──────────────────────────────── 11차 게이트 리뷰

def test_sweep_flags_different_curves_and_endpoints(tmp_path):
    """★ 11차 발견 5 — optimizer 축만 보면 sweep 이 **다른 곡선**으로 돌아도
    "본 실행과 같은 설정" 초록 문장이 실린다 (리뷰 실측: main/sweep curves_sha
    가 다른데 배너 없음). 실험 identity 와 끝점 정의·결과까지 봐야 한다."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path, objectives=("pocv_dvdq",))
    sub = _wsweep_run(d)
    m = yaml.safe_load((sub / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["curves_sha"] = "다른곡선"          # 다른 데이터로 돈 sweep
    (sub / "manifest.yaml").write_text(
        yaml.safe_dump(m, allow_unicode=True, sort_keys=False), encoding="utf-8")
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "설정이 다릅니다" in text and "curves_sha 불일치" in text
    assert "같은 설정으로 돌렸습니다" not in text


def test_sweep_endpoint_definition_equality_checked(tmp_path):
    """★ 11차 발견 5 — 끝점은 **이름이 아니라 가중치 정의**가 같아야 한다.
    `wdqdv_0.00` 의 w_dqdv 를 몰래 바꾸면 w=0 ≡ pocv_dvdq 전제가 깨진다."""
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path, objectives=("pocv_dvdq",))
    sub = _wsweep_run(d)
    m = yaml.safe_load((sub / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["objectives"]["wdqdv_0.00"]["w_dqdv"] = 0.3   # 이름만 w=0
    (sub / "manifest.yaml").write_text(
        yaml.safe_dump(m, allow_unicode=True, sort_keys=False), encoding="utf-8")
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "끝점 정의" in text
    assert "같은 설정으로 돌렸습니다" not in text


def test_check_sweep_consistency_cli_exits_nonzero(tmp_path, monkeypatch):
    """★ 11차 발견 5 — 불일치인데 exit 0 이면 파이프라인에 넣어도 아무것도
    막지 못한다 (보고서는 이 도구가 확인한다고 써 왔다)."""
    import sys

    import pytest

    import tools.check_sweep_consistency as C

    monkeypatch.setattr(C, "run_check", lambda *a, **k: {
        "sweep_dir": "s", "main_dir": "m", "일치": False,
        "pairs": [{"sweep_objective": "wdqdv_0.00", "main_objective": "pocv_dvdq",
                   "n_sweep": 0, "n_main": 3, "n_common": 0, "일치": False,
                   "_오류": "한쪽에 해당 목적함수 행이 없다",
                   "판정": "불일치 — 비교할 행이 없다"}]})
    monkeypatch.setattr(sys, "argv", ["chk", "--sweep", "s", "--main", "m"])
    with pytest.raises(SystemExit) as e:
        C.main()
    assert e.value.code == 1


def test_canonical_input_key_is_posix(tmp_path):
    """★ 11차 발견 8 — 봉인 키는 어느 OS 에서 만들든 POSIX 여야 한다.
    Windows 의 `a\\res\\curves.parquet` 는 archive 의 POSIX restore_map 과
    어긋나 완비된 묶음도 복원 불가였다."""
    from src.io import canonical_input_key

    p = tmp_path / "res" / "sub" / "curves.parquet"
    p.parent.mkdir(parents=True)
    p.write_text("x", encoding="utf-8")
    key = canonical_input_key(p, tmp_path)
    assert key == "res/sub/curves.parquet"
    assert "\\" not in key


def test_sweep_endpoint_requires_exact_agreement(tmp_path):
    """★ 12차 발견 3 — 끝점 판정은 다수결·5%p 허용이 아니라 **조건별 수치
    동일성**이어야 한다.

    반례(리뷰 실측): 49%의 조건에서 J 를 2% 키워도, 모든 lam_pe_hat 을 +10%p
    옮겨도, 공통 조건이 0건이어도 "일치" 였다.
    """
    from tools.check_sweep_consistency import run_check

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    sub = _wsweep_run(d)
    base = run_check(sub, d)
    assert base["일치"], base["pairs"]

    # ① 절반 조건의 J 를 2% 키운다 → 예전 임계(>50%)로는 통과했다
    f = pd.read_parquet(sub / "fits.parquet")
    half = f["cond_id"].isin(sorted(set(f["cond_id"]))[: len(set(f["cond_id"])) // 2])
    f.loc[half, "J"] = f.loc[half, "J"] * 1.02
    f.to_parquet(sub / "fits.parquet", index=False)
    r1 = run_check(sub, d)
    assert not r1["일치"]
    assert any("J" in str(p.get("조건별_차이", {})) for p in r1["pairs"])

    # ② 해(parameter)만 어긋난 경우 — J 는 같아도 잡아야 한다
    f = pd.read_parquet(sub / "fits.parquet")
    f["J"] = pd.read_parquet(d / "fits.parquet")["J"].to_numpy()[: len(f)]
    f["lam_pe_hat"] = f["lam_pe_hat"] + 0.10
    f.to_parquet(sub / "fits.parquet", index=False)
    r2 = run_check(sub, d)
    assert not r2["일치"], "해가 10%p 어긋났는데 일치로 판정했다"

    # ③ 공통 조건 0건은 명시적 실패
    f = pd.read_parquet(sub / "fits.parquet")
    f["cond_id"] = "없는조건_" + f["cond_id"].astype(str)
    f.to_parquet(sub / "fits.parquet", index=False)
    r3 = run_check(sub, d)
    assert not r3["일치"]
    assert all(p["n_common"] == 0 for p in r3["pairs"])


def test_sweep_endpoint_coverage_checked(tmp_path):
    """★ 12차 발견 3 — sweep 조건이 서명된 수보다 적거나 본 실행에 없는 조건을
    포함하면 "일부만 맞았다"를 일치로 볼 수 없다."""
    from tools.check_sweep_consistency import run_check

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    sub = _wsweep_run(d)

    f = pd.read_parquet(sub / "fits.parquet")
    drop = sorted(set(f["cond_id"]))[:2]
    f[~f["cond_id"].isin(drop)].to_parquet(sub / "fits.parquet", index=False)
    r = run_check(sub, d)
    assert not r["일치"]
    assert any("서명된" in p["판정"] for p in r["pairs"]), \
        [p["판정"] for p in r["pairs"]]


def test_sweep_checker_is_fail_closed(tmp_path):
    """★ 13차 발견 2 — 끝점 "정확 일치" 가 NaN·Inf·중복·다른 조건집합을
    승인했다 (결론이 바뀜).

    리뷰 실측:
      · sweep J = NaN → 비교 n=0, n_violate=0 → "일치"
      · sweep J = Inf → dev=Inf, tol=Inf, Inf > Inf 가 거짓 → "일치"
      · 두 끝점이 main 의 **서로 다른** 5조건씩 → 각각 n_common=5 → "일치"
      · 같은 조건 행 중복(17행/16조건) → set 기반 개수 검사 통과
      · sweep manifest 부재 → expected_conditions=None → 일치 판정 가능
    """
    import numpy as np

    from tools.check_sweep_consistency import run_check

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    sub = _wsweep_run(d)
    assert run_check(sub, d)["일치"], "기준 상태가 일치여야 이 테스트가 유효하다"

    def _mutate(fn):
        f = pd.read_parquet(sub / "fits.parquet")
        f = fn(f)
        f.to_parquet(sub / "fits.parquet", index=False)
        r = run_check(sub, d)
        return r

    orig = pd.read_parquet(sub / "fits.parquet").copy()

    def _restore():
        orig.to_parquet(sub / "fits.parquet", index=False)

    # ① NaN — 비교에서 조용히 빠지면 안 된다
    r = _mutate(lambda f: f.assign(J=np.nan))
    assert not r["일치"], "NaN J 를 일치로 판정했다"
    _restore()

    # ② Inf
    r = _mutate(lambda f: f.assign(J=np.inf))
    assert not r["일치"], "Inf J 를 일치로 판정했다"
    _restore()

    # ③ 행 중복 — (cond_id, objective) 는 정확히 한 행이어야 한다
    def _dup(f):
        return pd.concat([f, f.iloc[[0]]], ignore_index=True)
    r = _mutate(_dup)
    assert not r["일치"], "중복 행을 일치로 판정했다"
    _restore()

    # ④ 두 끝점이 서로 다른 조건집합 (각각은 main 의 부분집합)
    def _split(f):
        conds = sorted(set(f["cond_id"]))
        half = len(conds) // 2
        a = f[(f["objective"] == "wdqdv_0.00") & (f["cond_id"].isin(conds[:half]))]
        b = f[(f["objective"] == "wdqdv_1.00") & (f["cond_id"].isin(conds[half:]))]
        return pd.concat([a, b], ignore_index=True)
    r = _mutate(_split)
    assert not r["일치"], "두 끝점의 조건집합이 다른데 일치로 판정했다"
    assert any("끝점" in p["판정"] or "조건" in p["판정"] for p in r["pairs"])
    _restore()

    # ⑤ sweep manifest 부재 → 서명된 조건집합을 확인할 수 없다 (fail-closed)
    mp = sub / "manifest.yaml"
    bak = mp.read_text(encoding="utf-8")
    mp.unlink()
    r = run_check(sub, d)
    assert not r["일치"], "manifest 없이 일치로 판정했다"
    mp.write_text(bak, encoding="utf-8")
    assert run_check(sub, d)["일치"], "복구 후 기준 상태로 돌아와야 한다"


# ──────────────────────────────── 14차 게이트 리뷰

def test_sweep_checker_requires_signed_condition_digest(tmp_path):
    """★ 14차 발견 3 — 서명된 condition_ids_sha256 없이는 "일치"가 안 된다.

    반례(리뷰어): 두 끝점을 **같은** 절반 조건으로 줄이고 run_spec.n_conditions
    를 그 수로 고친 뒤 condition_ids_sha256 만 지우면 — 개수 검사·끝점 동일성
    검사·조건별 수치 검사 전부 통과 → "일치". 축소된 모집단의 sweep 최적 w 가
    본 실행 대표로 인용된다. digest 누락/빈값은 즉시 fail 이어야 하고, 양
    끝점의 digest 가 서명 digest 와 같음이 최상위 verdict 에 들어가야 한다.
    """
    import yaml

    from tools.check_sweep_consistency import run_check

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    sub = _wsweep_run(d)
    base = run_check(sub, d)
    assert base["일치"], base["pairs"]
    assert base.get("끝점_서명digest_일치") is True, \
        "정상 경로에서 digest 대조가 명시적으로 참이어야 한다"

    # 두 끝점을 같은 절반 조건으로 축소하고 개수를 맞춘다
    f = pd.read_parquet(sub / "fits.parquet")
    conds = sorted(set(f["cond_id"]))
    keep = conds[: len(conds) // 2]
    f[f["cond_id"].isin(keep)].to_parquet(sub / "fits.parquet", index=False)
    mp = sub / "manifest.yaml"
    m = yaml.safe_load(mp.read_text(encoding="utf-8"))
    m["run_spec"]["n_conditions"] = len(keep)
    del m["run_spec"]["condition_ids_sha256"]
    mp.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                  encoding="utf-8")
    r = run_check(sub, d)
    assert not r["일치"], "digest 없이 축소 모집단이 일치로 통과했다 (14차 발견 3)"

    # 빈 문자열 digest 도 fail-closed
    m["run_spec"]["condition_ids_sha256"] = ""
    mp.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                  encoding="utf-8")
    r2 = run_check(sub, d)
    assert not r2["일치"], "빈 digest 를 일치로 판정했다"


def test_build_weight_objectives_rejects_name_collisions_and_bad_values():
    """★ 14차 발견 4 — `build_weight_objectives([0, 0.001])` 이 이름
    `wdqdv_0.00` 하나로 붕괴하며 **w=0 seed 를 소리 없이 삭제**한다.

    이름은 `%.2f` 라 0.001·0.004 가 전부 0.00 으로 접힌다 — dict 라 뒤 값이
    이기고, `0.0 in w_grid` 라 숨은 seed 도 안 끼워져 w=0 끝점 자체가 없어진다.
    끝점 검증(check_sweep_consistency)은 남은 `wdqdv_0.00` 을 w=0 정의로
    대조하므로 붕괴가 검출되지 않는다. 요구: 값↔이름 1:1, 충돌·중복·비유한·
    음수는 즉시 fail.
    """
    import numpy as np
    import pytest

    from src.weight_sweep import build_weight_objectives

    # 정상 격자는 그대로 — 이름과 값이 1:1
    objs = build_weight_objectives([0.0, 0.25, 1.0])
    assert list(objs) == ["wdqdv_0.00", "wdqdv_0.25", "wdqdv_1.00"]

    # 이름 충돌 (0.001 → "wdqdv_0.00") — 조용한 삭제 금지
    with pytest.raises(ValueError, match="충돌|1:1"):
        build_weight_objectives([0.0, 0.001])

    # 같은 값 중복도 조용히 합쳐지면 안 된다
    with pytest.raises(ValueError, match="중복|충돌|1:1"):
        build_weight_objectives([0.0, 0.0, 1.0])

    # 비유한·음수 fail-closed
    with pytest.raises(ValueError, match="유한|음수|아니"):
        build_weight_objectives([0.0, float("nan")])
    with pytest.raises(ValueError, match="유한|음수|아니"):
        build_weight_objectives([0.0, np.inf])
    with pytest.raises(ValueError, match="유한|음수|아니"):
        build_weight_objectives([-0.25, 0.0])


def test_reproduce_commands_follow_manifest_paths_and_vcol(tmp_path):
    """★ 14차 발견 6 — 재현 명령이 실제 실행의 경로·target 을 따라야 한다.

    현재 명령은 grid `--out {in_dir}` / fit `--in {in_dir}` 라, 곡선 producer
    와 fit 산출물이 다른 디렉터리인 실제 v4 배치(grid_curves_v4 →
    grid_fit_v4)에서 그대로 실행하면 **fit 산출물 위에 곡선을 만들고 자기
    자신을 입력으로 fit 하는 다른 pipeline** 이 된다. 또 `run_spec.v_col ==
    "v_full"`(clean fit) 인데 `--clean` 이 없으면 noisy fit 이 재현된다.
    목적함수 간 비교(결론 2)의 인용 정본 문서도 명시해야 한다.
    """
    import yaml

    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path)
    mp = d / "manifest.yaml"
    m = yaml.safe_load(mp.read_text(encoding="utf-8"))
    m["input"] = "results/grid_curves_v4"        # 실제 fit 이 기록하는 키
    mp.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                  encoding="utf-8")

    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(
        encoding="utf-8")

    assert "--out results/grid_curves_v4" in text, \
        "grid 재현 명령이 producer 경로(manifest.input)를 --out 으로 써야 한다"
    assert f"--in results/grid_curves_v4 --out {d}" in text, \
        "fit 재현 명령이 producer 를 --in, 현재 산출물을 --out 으로 써야 한다"
    assert "--clean" in text, \
        "run_spec.v_col == v_full 이면 --clean 이 재현 명령에 있어야 한다"
    assert "RESULTS_PAIRED_FIXED5.md" in text, \
        "목적함수 간 비교(결론 2)의 인용 정본 문서를 명시해야 한다"


def test_archive_records_computation_commit_and_promotion_is_fail_closed(tmp_path):
    """★ 14차 발견 7·8 — archive 의 source_commit 출처와 승격 fail-closed.

    발견 8: artifact_index 의 `source_commit` 이 manifest **최상위**
    `git_commit`(기록 시점)에서 나온다 — 계산을 고정하는 것은 서명된
    `run_spec.git_commit`(시작 시점)이다. fixture manifest 는 최상위 키가
    없어 현재 코드는 None 을 기록한다. "다음 commit" 문구도 실제 워크플로
    (`git add artifacts && git commit` 한 번)와 어긋난다.

    발견 7: 승격의 첫 이동(`mv out → .previous_`)이 실패해도 검사 없이
    진행돼 `mv cand out` 이 **기존 묶음 안으로 candidate 를 중첩**시키고
    성공(exit 0)으로 끝난다. 실패 시 후보를 제거하고 n_bad 로 계상해야 한다.
    """
    import os
    import shutil
    import stat
    import subprocess

    import pytest
    import yaml

    # ★ 14차 2차 발견 6 — Windows native pytest 에는 bare `bash` 가 없어
    #   FileNotFoundError 로 죽었다. shell wrapper 회귀는 POSIX shell 이 있는
    #   환경에서만 의미가 있다 — 없으면 **명시적으로 skip** 한다 (조용한 통과가
    #   아니라 "이 환경에서 검증되지 않았다"를 남긴다).
    if shutil.which("bash") is None:
        pytest.skip("bash 없음 — archive shell 회귀는 POSIX shell 환경에서만 "
                    "실행된다 (Windows 는 Git Bash wrapper 실측으로 대체)")

    repo = Path(__file__).resolve().parent.parent
    d, _ = _complete_artifact(tmp_path)          # tmp_path/res
    dest = tmp_path / "arch"

    def _run(env_extra=None):
        env = {**os.environ, "ARCHIVE_DEST": str(dest), **(env_extra or {})}
        return subprocess.run(
            ["bash", str(repo / "scripts" / "archive_results.sh"), str(d)],
            cwd=repo, env=env, capture_output=True, text=True)

    # ① 정상 승격 — source_commit 은 서명된 run_spec.git_commit 이어야 한다
    r1 = _run()
    assert r1.returncode == 0, r1.stdout + r1.stderr
    idx = yaml.safe_load((dest / "artifact_index.yaml").read_text(
        encoding="utf-8"))
    ent = idx["runs"]["res"]
    assert ent["source_commit"] == "0" * 40, \
        f"source_commit 은 계산 시작 커밋(run_spec.git_commit)이어야 한다: {ent}"
    assert "다음 commit" not in str(idx.get("_주의", "")), \
        "index 문구가 실제 워크플로(한 commit)와 어긋난다 (14차 발견 8)"

    # ② 첫 이동 실패 주입 — fail-closed 여야 한다
    fake = tmp_path / "bin"
    fake.mkdir()
    mv = fake / "mv"
    mv.write_text("#!/bin/bash\n"
                  "for a in \"$@\"; do case \"$a\" in *.previous_*)\n"
                  "  echo 'mv: simulated failure' >&2; exit 1;; esac; done\n"
                  "exec /bin/mv \"$@\"\n", encoding="utf-8")
    mv.chmod(mv.stat().st_mode | stat.S_IEXEC)
    r2 = _run({"PATH": f"{fake}:{os.environ['PATH']}"})
    assert r2.returncode != 0, \
        "첫 이동(mv out → .previous_)이 실패했는데 성공으로 끝났다 (14차 발견 7)"
    assert not (dest / "res" / ".candidate_res").exists(), \
        "candidate 가 기존 묶음 안으로 중첩됐다"
    assert (dest / "res" / "manifest.yaml").is_file(), \
        "실패 시 기존 묶음이 그대로 남아 있어야 한다"


def test_build_weight_objectives_requires_name_round_trip():
    """★ 14차 2차 발견 3 — 단일 값도 자기 이름과 exact round-trip 해야 한다.

    충돌 검사는 "서로 다른 두 값이 같은 이름"만 본다. `[0.001]` 은 충돌이 없어
    통과하지만 이름은 `wdqdv_0.00` 이고, 하류 집계(`sweep_summary:163`
    `float(o.split("_")[-1])`)는 그 이름을 다시 float 으로 읽는다 — 요청 weight
    0.001 과 보고 weight 0.00 이 갈린다. `-0.0` 은 `wdqdv_-0.00` 이 되어 진짜
    `wdqdv_0.00` seed 제공자가 없어진다. 빈 격자도 시작 전에 거부한다.
    """
    import pytest

    from src.weight_sweep import build_weight_objectives, obj_name

    # 표현 불가능한 단일 값 — 충돌은 없지만 이름이 값을 잃는다
    for bad in ([0.001], [1.001], [0.0, 0.125]):
        with pytest.raises(ValueError, match="round-trip|표현|소수"):
            build_weight_objectives(bad)

    # signed zero 는 +0.0 으로 정규화 — seed 제공자 이름 계약 유지
    objs = build_weight_objectives([-0.0, 1.0])
    assert list(objs) == ["wdqdv_0.00", "wdqdv_1.00"], list(objs)
    assert objs["wdqdv_0.00"]["w_dqdv"] == 0.0
    assert not str(objs["wdqdv_0.00"]["w_dqdv"]).startswith("-")

    # 빈 격자 거부
    with pytest.raises(ValueError, match="비어|empty|하나"):
        build_weight_objectives([])

    # 기본 격자는 전부 정확히 표현된다 (계약이 실제로 성립하는지)
    from src.weight_sweep import DEFAULT_W_GRID
    for w in DEFAULT_W_GRID:
        assert float(obj_name(w).split("_")[-1]) == w, w


def test_reproduce_block_covers_every_rendered_section(tmp_path):
    """★ 14차 2차 발견 4 — "재현" 블록만 실행하면 이 문서가 렌더한 절이 전부
    다시 나와야 한다.

    현재 블록에는 `--mode wsweep`, half-cell 준비(`--force --verify`),
    half-cell 기준 fit·score, `report --compare <halfcell>` 이 없다. 그래서
    sweep 절과 Case 1↔Case 2 비교 절을 렌더하면서도 명령대로 재실행하면
    최적-weight 절과 기준 곡선 비교 절이 생기지 않는다.
    """
    import yaml

    from tools.compare_cases import compare
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    h, _ = _complete_artifact(tmp_path / "h",
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    sub = _wsweep_run(d)
    mp = d / "manifest.yaml"
    m = yaml.safe_load(mp.read_text(encoding="utf-8"))
    m["input"] = "results/grid_curves_v4"
    mp.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                  encoding="utf-8")

    res = compare(d / "fits.parquet", h / "fits.parquet")
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(res, allow_unicode=True), encoding="utf-8")
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(
        encoding="utf-8")

    # 렌더된 절 (전제 확인 — 이게 없으면 이 테스트가 무의미하다)
    assert "가중치" in text and "기준 곡선 비교" in text

    repro = text.split("## 재현")[1]
    assert "--mode wsweep" in repro, "sweep 절을 렌더하면서 재현 명령에 wsweep 이 없다"
    assert "src.halfcell" in repro and "--verify" in repro, \
        "Case 1 절을 렌더하면서 half-cell 준비 명령이 없다"
    assert "--reference halfcell" in repro, "half-cell 기준 fit 명령이 없다"
    assert f"--compare {h}" in repro, \
        "기준 곡선 비교 절을 만드는 report --compare 가 없다"


def test_reproduce_block_wrapper_parser_smoke_and_canonical_paths(tmp_path):
    """★ 14차 3차 발견 1·2 — 재현 명령이 **실제 wrapper 를 통과**하고 정본
    경로를 가리켜야 한다. (★ 14차 4차 발견 5 — 범위는 **parser smoke** 다:
    wrapper 옵션 존재·정본 경로 문자열·옵션명만 증명하고, 인자 전달·하류
    argparse·실제 계산은 strict smoke 가 담당한다.)

    두 오류가 문자열 존재 검사(`"--mode wsweep" in text`)를 빠져나갔다.
      · sweep 출력이 `<main-fit>/wsweep` 이 아니라 `<main-fit>` 자체 —
        `run_weight_sweep` 은 명시된 `--out` 을 그대로 쓰고 생략 시에만
        `<in>/wsweep` 을 기본값으로 한다. 보고서·strict smoke 가 소비하는
        정본 위치는 `<main-fit>/wsweep` 이다.
      · wrapper 옵션명은 `--w-stride` 인데 `--stride` 를 출력 — 실측
        `./run.sh --mode wsweep --stride 2` → `알 수 없는 인자: --stride`, exit 1.
    """
    import os
    import shutil
    import subprocess

    import pytest
    import yaml

    from tools.compare_cases import compare
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    if shutil.which("bash") is None:
        pytest.skip("bash 없음 — wrapper parser 검증은 POSIX shell 에서만")

    repo = Path(__file__).resolve().parent.parent
    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    h, _ = _complete_artifact(tmp_path / "h",
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    _wsweep_run(d)
    res = compare(d / "fits.parquet", h / "fits.parquet")
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(res, allow_unicode=True), encoding="utf-8")
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(
        encoding="utf-8")
    repro = text.split("## 재현")[1].split("```")[1]

    # ① sweep 출력은 정본 위치 <main-fit>/wsweep
    #    (주 fit 의 `--out {in_dir}` 은 정상이므로 wsweep 줄로 한정해 본다)
    _sw_line = next(ln for ln in repro.splitlines() if "--mode wsweep" in ln)
    assert f"--out {d / 'wsweep'}" in _sw_line, _sw_line
    assert f"--out {d} " not in _sw_line, "sweep 을 main fit 디렉터리에 쓰려 한다"
    assert f"--in {d} " in _sw_line or f"--in {d}\n" in _sw_line + "\n", \
        "sweep 입력은 곡선 디렉터리여야 한다 (smoke 정본과 동일)"

    # ② 옵션명은 wrapper 가 실제로 받는 것이어야 한다
    assert "--w-stride" in _sw_line, _sw_line
    assert " --stride " not in repro, "존재하지 않는 --stride 를 출력한다"

    # ③ 모든 ./run.sh 줄이 실제 wrapper 의 인자 파싱을 통과해야 한다.
    #    (계산은 시키지 않는다 — 없는 입력으로 파싱 뒤 단계에서 죽는 것은 정상)
    for line in repro.splitlines():
        line = line.strip()
        if not line.startswith("./run.sh"):
            continue
        argv = line.replace("$(nproc)", "1").split()[1:]
        # `--help` 를 붙여 파싱 직후 종료시킨다 (계산은 시키지 않는다)
        r = subprocess.run(["bash", str(repo / "run.sh"), *argv, "--help"],
                           cwd=repo, capture_output=True, text=True,
                           env={**os.environ})
        # ★ 14차 4차 발견 5 — 문구뿐 아니라 **종료 코드**까지 본다.
        #   다만 이것은 wrapper **parser smoke** 다: token 이 wrapper 옵션으로
        #   존재하는지만 증명하며, mode 별 인자 전달·하류 argparse·실제 출력
        #   디렉터리·숫자 생성은 증명하지 않는다 (그건 strict smoke 담당).
        assert "알 수 없는 인자" not in r.stderr, (line, r.stderr[:200])
        assert r.returncode == 0, (line, r.returncode, r.stderr[:200])


def test_halfcell_reproduce_command_carries_nondefault_flags(tmp_path):
    """★ 14차 3차 발견 4 — half-cell 재현 명령도 그 artifact 의 **서명된**
    nondefault 설정을 복원해야 한다.

    현재 블록은 `--reference halfcell` 만 붙이고 objective_order·n_restarts·
    clean/noisy target·adaptive·warm_start 를 읽지 않는다. 기본값으로 돈
    half-cell 이면 숫자가 같지만, "렌더된 절과 같은 signed 조건을 재현한다"는
    설명은 그때만 참이다.
    """
    import yaml

    from tools.compare_cases import compare
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    h, _ = _complete_artifact(tmp_path / "h",
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    # half-cell 쪽만 nondefault protocol 로 서명한다
    hm = h / "manifest.yaml"
    m = yaml.safe_load(hm.read_text(encoding="utf-8"))
    m["run_spec"] = {**m["run_spec"], "n_restarts": 7, "warm_start": False,
                     "v_col": "v_full",
                     "optimizer": {**(m["run_spec"].get("optimizer") or {}),
                                   "adaptive": False}}
    hm.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                  encoding="utf-8")

    res = compare(d / "fits.parquet", h / "fits.parquet")
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(res, allow_unicode=True), encoding="utf-8")
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(
        encoding="utf-8")
    repro = text.split("## 재현")[1].split("```")[1]
    hc_line = next(ln for ln in repro.splitlines()
                   if "--reference halfcell" in ln)

    assert "--n-restarts 7" in hc_line, hc_line
    assert "--no-adaptive" in hc_line, hc_line
    assert "--no-warm-start" in hc_line, hc_line
    assert "--clean" in hc_line, hc_line


def test_halfcell_prep_command_uses_signed_method(tmp_path):
    """★ 14차 4차 발견 4 — half-cell 준비 명령의 `--method` 도 서명값이어야 한다.

    `run_spec.halfcell_recipe.method` 가 `sim` 인 artifact 를 렌더하면서
    준비 명령은 `--method ocp` 기본값을 출력했다 — 그 문서의 Case 1 절을
    명령대로 재현하면 다른 기준 곡선으로 계산된다.
    """
    import yaml

    from tools.compare_cases import compare
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    h, _ = _complete_artifact(tmp_path / "h",
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    hm = h / "manifest.yaml"
    m = yaml.safe_load(hm.read_text(encoding="utf-8"))
    m["run_spec"] = {**m["run_spec"], "halfcell_recipe": {"method": "sim"}}
    hm.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                  encoding="utf-8")

    res = compare(d / "fits.parquet", h / "fits.parquet")
    (d / "case_comparison.yaml").write_text(
        yaml.safe_dump(res, allow_unicode=True), encoding="utf-8")
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(
        encoding="utf-8")
    prep = next(ln for ln in text.split("## 재현")[1].splitlines()
                if "src.halfcell" in ln)
    assert "--method sim" in prep, prep


def _gap_cmp_res():
    """결론 2 렌더를 태우는 최소 cmp_res — v4 실측값을 그대로 넣는다."""
    return {
        "table": [
            {"objective": "pocv_dvdq", "n": 1476, "degenerate_frac": 0.619241,
             "degenerate_frac_corrected": 0.144309, "mean_abs_err": 0.024227,
             "pe_ne_antisym_frac": 0.68},
            {"objective": "pocv_dvdq_dqdv", "n": 1476, "degenerate_frac": 0.871951,
             "degenerate_frac_corrected": 0.945122, "mean_abs_err": 0.065287,
             "pe_ne_antisym_frac": 0.36},
        ],
        "gap_analysis": {"pocv_dvdq": {
            "population": "recoverable", "tol": 0.02, "gap_thresh": 0.06,
            "n_wide_gap_true": 245, "n_small_gap_true": 98,
            "gap_collapse_frac": 1 / 245, "false_split_frac": 0.6326530612244898,
            "mean_true_gap_wide": 0.099, "mean_recovered_gap_wide": 0.104,
            "shrinkage": 1.06, "likelihood_ratio_equal": 90.0,
            # ★ 18차 발견 1 — 이 key 가 없으면 임계 의존 문단 자체가 렌더되지
            #   않아, "관측 가능한 범위" 문장 검사가 **분기를 안 태우고** 통과했다.
            "collapse_requires_gap_err": 0.04, "gap_err_median": 0.026,
            "gap_err_p99": 0.057, "collapse_margin_median": -0.082,
            "collapse_margin_max": -0.011, "n_wide_gap_toward_collapse": 121,
            "lr_sensitivity_min": 2.47, "lr_sensitivity_max": 113.7,
            "lr_sensitivity_median": 16.83, "lr_is_local_spike": True,
        }},
        "gap_analysis_all_conditions": {"pocv_dvdq": {
            "population": "all", "n_wide_gap_true": 604,
            "gap_collapse_frac": 0.10596026490066225,
            "likelihood_ratio_equal": 3.6903044871794877,
        }},
        "unrecoverable_frac": 0.519,
    }


def test_conclusion_renders_counts_not_rounded_percent():
    """★ 15차 발견 2 — 붕괴를 정수 percent 로 반올림해 `0%` 로 쓰면 안 된다.

    실제 값은 `1/245 = 0.408%` 인데 `_pct(x, 0)` 가 `0%` 로 반올림했다. 0건이면
    사건률 비가 90.0 이 아니라 무한대여야 하므로, 보고서가 스스로 모순된 숫자를
    실은 셈이다. count/denominator 를 먼저 쓴다.
    """
    from tools.make_results import _conclusion

    txt = "\n".join(_conclusion(_gap_cmp_res(), {"n_rows_recoverable": 1476}))
    assert "1/245 (0.41%)" in txt, txt[:800]
    assert "36/98" in txt, "작은 격차군도 count 로 써야 한다"
    import re
    assert not re.search(r"(?<![\d./])0%", txt), "정수 반올림 0% 가 남아 있다"


def test_conclusion_1_uses_counts_and_decimal():
    """★ 15차 발견 1 — 결론 1 도 정수 반올림하면 안 된다.

    paired 정본은 `61.9% → 87.2%` 인데 `_pct(x, 0)` 이 `62% → 87%` 로 반올림해
    원장이 비대칭 pipeline 값(62→63)과 헷갈리는 통로가 됐다. count 와 소수를
    함께 낸다.
    """
    from tools.make_results import _conclusion

    txt = "\n".join(_conclusion(_gap_cmp_res(), {"n_rows_recoverable": 2952}))
    assert "914/1476" in txt and "1287/1476" in txt, txt[:500]
    assert "61.9" in txt and "87.2" in txt, "소수 한 자리가 없다"


def test_conclusion_unrecoverable_is_domain_not_physics():
    """★ 15차 발견 9 — "원리적으로 복원 불가" 는 실제 셀·다른 reference 까지
    확장되는 물리 명제로 읽힌다. 현재 fitter 의 feasible domain 판정으로 쓴다."""
    from tools.make_results import _conclusion

    txt = "\n".join(_conclusion(_gap_cmp_res(), {"n_rows_recoverable": 2952}))
    assert "원리적으로 복원 불가" not in txt, "물리 명제로 읽히는 표현이 남아 있다"
    # ★ 18차 발견 3 — `feasible domain` 토큰을 요구하던 assertion 을 바꾼다.
    #   실제 판정은 α-window eligibility criterion 이다.
    assert "eligibility" in txt, txt[-600:]


def test_conclusion_numbering_is_sequential():
    """★ 15차 — 결론 번호가 3 다음 5 로 건너뛴다 (`len(lines)+1` 이 부속 줄까지
    센다). 읽는 사람은 빠진 항목이 있다고 오해한다."""
    import re

    from tools.make_results import _conclusion

    nums = [int(m.group(1)) for line in _conclusion(_gap_cmp_res(), {})
            if (m := re.match(r"^(\d+)\. ", line))]
    assert nums == list(range(1, len(nums) + 1)), f"번호가 건너뛴다: {nums}"


def test_conclusion_pairs_conditional_ratio_with_all_population():
    """★ 15차 발견 3 — 사건률 비 90 은 recoverable 조건부다. 전체 격자 값(3.69)과
    함께 쓰지 않으면 단독 인용된다. '우도비' 라는 무조건적 이름도 쓰지 않는다."""
    from tools.make_results import _conclusion

    txt = "\n".join(_conclusion(_gap_cmp_res(), {"n_rows_recoverable": 1476}))
    assert "조건부 사건률 비" in txt, txt[:800]
    assert "population=recoverable" in txt
    assert "64/604" in txt and "3.69" in txt, "전체 격자 값이 병기되지 않았다"
    assert "우도비" not in txt, "무조건적 '우도비' 표현이 남아 있다"


def test_report_labels_error_column_as_max_mode(tmp_path):
    """★ 15차 발견 6 — `평균 |err|` 는 일반 MAE 가 아니라 **행별 max-mode 절대
    오차의 평균**이다 (`src/scoring.py`). 라벨이 계산과 달라 오인된다."""
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path, objectives=("pocv_dvdq",))
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "max-mode" in text, "오차 열 라벨이 max-mode 임을 밝히지 않는다"


def test_input_digest_resolves_against_repo_root_not_cwd(tmp_path, monkeypatch):
    """★ 15차-3 발견 — 봉인 입력을 **CWD 기준으로 먼저** 찾으면 격리 검증이 빈다.

    `src/io.py` 의 재해시는 `cand = Path(path_s)` 로 CWD 상대 경로를 먼저 보고,
    없을 때만 `repo_root` 로 갔다. 그런데 `scripts/archive_results.sh` 의 격리
    복원 검증은 **cwd = 원본 저장소**에서 돈다. 따라서 저장소 상대 봉인 입력
    (`configs/base.yaml`·`.cache/halfcell/*`·`results/*/curves.parquet`)은 복원본이
    아니라 **원본 저장소 파일**로 대조됐다 — 묶음에서 그 파일이 빠지거나 깨져도
    통과한다. F71/8-3 이 막으려던 실패 모드 그대로다.

    실측(v4): 격리 root 의 half-cell meta 를 위조해도 `ok=True` 였다.
    봉인 키는 F65 로 **저장소 root 상대**임이 보장되므로 root 로만 풀어야 한다.
    """
    import yaml

    from src.io import validate_provenance

    d, _ = _complete_artifact(tmp_path, repo_root=tmp_path)
    assert validate_provenance(d, repo_root=tmp_path)["ok"]

    man = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    key = next(k for k in man["input_sha256"] if k.endswith("base.yaml"))
    good = (tmp_path / key).read_bytes()

    # CWD 에는 **정상** 사본, root 아래에는 **위조본** — 격리 검증이라면 잡아야 한다
    decoy = tmp_path / "cwd_decoy"
    (decoy / Path(key)).parent.mkdir(parents=True, exist_ok=True)
    (decoy / key).write_bytes(good)
    (tmp_path / key).write_bytes(good + b"\n# forged\n")
    monkeypatch.chdir(decoy)

    v = validate_provenance(d, repo_root=tmp_path)
    assert "입력_digest_재해시" in v["fail"], (
        "CWD 의 정상 사본이 root 의 위조본을 가렸다 — 격리 검증이 비어 있다")


def test_full_chain_threads_repo_root_to_validator(tmp_path, monkeypatch):
    """★ 16차 발견 1 — `repo_root` 가 score·compare·report 까지 관통해야 한다.

    `src/io.py` 의 CWD 우선 참조는 15차-3 에서 고쳤지만, `build()`·`run_scoring()`
    ·`compare()` 가 `validate_provenance()` 에 root 를 **넘기지 않아** 기본
    root(=`src/io.py` 가 있는 원본 저장소)로 되돌아갔다. 격리 root 에서 보고서를
    만들어도 원본 저장소 파일이 검증되므로, 초록 provenance 가 격리본을
    증명하지 않는다.

    위조 파일로 재현하려면 기본 root 에 **일치하는** 사본이 있어야 해서 환경에
    의존한다. 그래서 전달 자체를 관찰한다 — validator 가 받은 `repo_root` 를
    기록하고, 모두 우리가 준 root 인지 본다.
    """
    import src.io as io_mod
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path, repo_root=tmp_path)
    run_compare(d, d)

    seen: list = []
    orig = io_mod.validate_provenance

    def spy(run_dir, repo_root=None, fits_path=None):
        seen.append((Path(run_dir).name, repo_root))
        return orig(run_dir, repo_root=repo_root, fits_path=fits_path)

    monkeypatch.setattr(io_mod, "validate_provenance", spy)
    build(d, tmp_path / "R.md", repo_root=tmp_path)

    assert seen, "validator 가 호출되지 않았다 — 테스트가 무의미하다"
    bad = [r for _, r in seen if r is None or Path(r) != Path(tmp_path)]
    assert not bad, (
        f"{len(bad)}/{len(seen)} 호출이 repo_root 를 받지 못했다 (기본 root 로 "
        f"되돌아간다): {bad[:3]}")


def test_wsweep_validator_is_in_the_threaded_call_set(tmp_path, monkeypatch):
    """★ 17차 발견 2 — nested wsweep 검증에서 `repo_root` 가 다시 끊긴다.

    16차 대응은 main·scoring·case 세 경로만 관통시켰고
    `make_results.py:563` 의 `_vp(in_dir / "wsweep")` 은 빠졌다. 그런데 기존
    spy 테스트 fixture 에는 `wsweep/` 가 아예 없어 그 분기를 **실행조차 하지
    않았다** — "관측된 호출은 모두 옳다" 는 검사만으로는 빠진 호출을 못 잡는다.

    그래서 **기대 호출 집합**을 고정한다: 빠진 호출도 실패여야 한다.
    """
    import src.io as io_mod
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path,
                              objectives=("pocv_dvdq", "pocv_dvdq_dqdv"))
    _wsweep_run(d)
    run_compare(d, d)

    seen: list = []
    orig = io_mod.validate_provenance

    def spy(run_dir, repo_root=None, fits_path=None):
        seen.append((Path(run_dir).name, repo_root))
        return orig(run_dir, repo_root=repo_root, fits_path=fits_path)

    monkeypatch.setattr(io_mod, "validate_provenance", spy)
    build(d, tmp_path / "R.md", repo_root=tmp_path)

    assert "wsweep" in {n for n, _ in seen}, (
        f"wsweep provenance 검증이 아예 호출되지 않았다: {sorted({n for n, _ in seen})}")
    bad = [(n, r) for n, r in seen if r is None or Path(r) != Path(tmp_path)]
    assert not bad, f"repo_root 가 끊긴 호출: {bad}"




def test_conclusion_22p_does_not_claim_all_equal_truth():
    """★ 16차 발견 4 — 최근접 8점이 "모두 참값이 같다" 는 거짓이다.

    0.02 step 에서 (0.13, 0.13, 0.17) 의 8 corner 는 PE=NE 4개 + |ΔLAM|=2%p
    4개이고 평균 참 격차가 1%p 다. 같은 줄에서 평균 격차 1.0%p 를 쓰면서
    "모두 같은 격자점" 이라고 하던 자기모순을 고정한다.
    """
    from tools.make_results import _conclusion

    cmp_res = _gap_cmp_res()
    # ★ 17차 사전 — 구성 문장이 데이터에서 나오게 바뀌면서, 구성 key 가 없는
    #   fixture 는 이제 "구성을 알 수 없다" 로 렌더된다(지어내지 않는 것이 옳다).
    #   v4 실측 구성을 넣어 원래 검사하려던 문장을 계속 태운다.
    cmp_res["verdict_22p"] = {"pocv_dvdq": {
        "n_near": 8, "degenerate_frac": 0.125, "mean_abs_err": 0.0168,
        "pe_ne_antisym_frac": 0.5, "true_pe_ne_gap": 0.010,
        "recovered_pe_ne_gap": 0.019,
        "n_near_exact_equal": 4, "max_true_pe_ne_gap": 0.02}}
    txt = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))

    assert "애초에 LAM_PE = LAM_NE인 격자점" not in txt, "거짓 전제가 남아 있다"
    assert "모두 같은 격자점이 아니다" in txt, txt[-700:]
    assert "wide-gap" in txt, "wide-gap 부재를 밝히지 않았다"


# ── 17차 사전 자체발견 — 16차 발견 4 의 잔여 + 하드코딩된 구성 ──────────────

def test_gap_section_intro_does_not_claim_all_22p_points_are_equal(tmp_path):
    """★ 16차 발견 4 잔여 — 결론과 22p 절만 고치고 격차 절 도입부를 놓쳤다.

    `make_results.build` 의 "전극 격차를 구분하는가" 절 도입부가 여전히
    "22p 근방 격자점은 **참값이 애초에 LAM_PE = LAM_NE** 다" 라고 단정한다.
    같은 문서 안에서 "이 8점은 모두 참값이 같은 격자점이 아니다" 와 정면으로
    모순된다. 문서 전체를 한 번에 보는 검사로 고정한다.
    """
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    run_compare(d, d)
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "참값이 애초에" not in text, \
        "격차 절 도입부가 22p 근방이 모두 PE=NE 라는 거짓 전제를 다시 말한다"


def _p22_frame():
    """근방에 PE=NE 1점 + 격차 4%p 1점만 두는 격자 (반경 안에 들어오게 배치)."""
    rows = []
    for i, (pe, ne) in enumerate([(0.13, 0.13), (0.13, 0.09)]):
        rows.append({
            "cond_id": f"n{i}", "objective": "pocv_dvdq", "noise": 0.0,
            "lli": 0.17, "lam_pe": pe, "lam_ne": ne,
            "lli_hat": 0.17, "lam_pe_hat": pe, "lam_ne_hat": ne,
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
    return pd.DataFrame(rows)


def test_p22_truth_composition_comes_from_data():
    """★ 근방 표본의 참값 구성은 **데이터에서** 나와야 한다.

    보고서가 "절반은 PE=NE, 절반은 2%p", "wide-gap 은 하나도 없다" 를 문자열
    상수로 박아두면 다른 격자·반경에서 그대로 거짓이 된다.
    """
    from tools.compare_objectives import p22_truth_composition

    c = p22_truth_composition(_scored(_p22_frame()), "pocv_dvdq", radius=0.05)

    assert c["n_near_exact_equal"] == 1, c
    assert c["max_true_pe_ne_gap"] == pytest.approx(0.04), c


def test_p22_composition_stays_out_of_sealed_comparison_schema():
    """★ 17차 사전 — 렌더 전용 파생값을 봉인 YAML schema 에 넣으면 안 된다.

    구성을 `verdict_22p` 반환에 넣었더니, 봉인된 `objective_comparison.yaml`
    (v4, 그 key 가 없던 시절) 과 재계산본의 **key 집합**이 달라져 F87 이
    정당하게 stale 을 올렸다 — v4 보고서 재생성에서 인용 금지 배너가 실제로
    떴다. 8시간 재실행 없이는 되돌릴 수 없는 종류의 실수다.

    fixture 로는 못 잡는 결함이다(같은 코드가 저장본을 쓰면 항상 일치한다).
    그래서 **schema 자체**를 검사한다.
    """
    from tools.compare_objectives import verdict_22p

    v = verdict_22p(_scored(_p22_frame()), "pocv_dvdq", radius=0.05)

    for k in ("n_near_exact_equal", "max_true_pe_ne_gap"):
        assert k not in v, (
            f"`{k}` 가 verdict_22p 반환에 들어갔다 — 봉인된 "
            f"objective_comparison.yaml 과 key 집합이 달라져 stale 이 뜬다")


def test_report_renders_p22_composition_without_going_stale(tmp_path):
    """★ 위 제약을 지키면서도 보고서에는 구성이 나와야 한다.

    저장본(`objective_comparison.yaml`)이 구성 key 를 갖고 있지 않아도
    보고서는 fits 정본에서 뽑아 렌더하고, stale·인용 금지 배너는 뜨지 않는다.
    """
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    # 구성은 **fits 정본에서** 뽑히므로 fits.parquet 이 있어야 경로가 태워진다
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)          # 저장본을 봉인 — 구성 key 는 여기 없다
    text = build(d, tmp_path / "RESULTS.md", repo_root=tmp_path).read_text(encoding="utf-8")

    # (이 fixture 는 manifest·run_spec 이 없어 인용 금지 배너 자체는 항상 뜬다.
    #  검사 대상은 **파생 stale 이 추가로 뜨는가** 다.)
    assert "파생_stale_objective_comparison.yaml" not in text, \
        "렌더 전용 구성 주입이 봉인 대조를 깨뜨렸다"
    assert "PE=NE 가 " in text, "구성이 보고서에 렌더되지 않았다"


def test_conclusion_22p_composition_is_not_hardcoded():
    """★ 구성 문장이 fixture 값을 따라가야 한다 — '절반' 같은 상수는 금지."""
    from tools.make_results import _conclusion

    def render(n_near, n_eq, max_gap):
        cmp_res = _gap_cmp_res()
        cmp_res["verdict_22p"] = {"pocv_dvdq": {
            "n_near": n_near, "degenerate_frac": 0.125, "mean_abs_err": 0.0168,
            "pe_ne_antisym_frac": 0.5, "true_pe_ne_gap": 0.010,
            "recovered_pe_ne_gap": 0.019,
            "n_near_exact_equal": n_eq, "max_true_pe_ne_gap": max_gap}}
        return "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))

    a = render(8, 4, 0.02)
    b = render(6, 1, 0.09)

    assert "절반" not in a, "구성을 '절반' 이라는 상수로 쓰고 있다"
    assert "4/8" in a, a[-800:]
    assert "1/6" in b, b[-800:]
    # 최대 참 격차가 임계(6%p) 를 넘으면 "wide-gap 하나도 없다" 라고 하면 안 된다
    assert "하나도 없" in a, a[-800:]
    assert "하나도 없" not in b, "wide-gap 이 있는데도 없다고 단정한다"


def test_conclusion_4_denominators_come_from_data():
    """★ 결론 4 의 '98·245조건, 22p 는 8조건' 이 상수로 박혀 있으면 안 된다."""
    from tools.make_results import _conclusion

    cmp_res = _gap_cmp_res()
    cmp_res["gap_analysis"]["pocv_dvdq"]["n_small_gap_true"] = 40
    cmp_res["gap_analysis"]["pocv_dvdq"]["n_wide_gap_true"] = 77
    cmp_res["verdict_22p"] = {"pocv_dvdq": {
        "n_near": 3, "degenerate_frac": 0.0, "mean_abs_err": 0.01,
        "pe_ne_antisym_frac": 0.0, "true_pe_ne_gap": 0.0,
        "recovered_pe_ne_gap": 0.0,
        "n_near_exact_equal": 3, "max_true_pe_ne_gap": 0.0}}
    txt = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))

    assert "98·245조건" not in txt, "gap 분모가 상수로 박혀 있다"
    assert "40·77조건" in txt, txt[-600:]
    assert "22p 는 3조건" in txt, txt[-600:]


# ── 17차 발견 1 — 2%p 경계가 binary float 때문에 작은-gap 군에 섞인다 ────────

def _boundary_frame():
    """참 격차가 **정확히 nominal 2%p** 인 조건들.

    0.15−0.13 = 0.01999999999999999 처럼 float 표현이 임계 아래로 떨어지는
    쌍과, 0.13−0.11 = 0.020000000000000004 처럼 위로 올라가는 쌍을 함께 둔다.
    수학적으로는 둘 다 `|ΔLAM| = 2%p` 이므로 `< 2%p` 군에 **하나도** 들어가면
    안 된다.
    """
    rows = []
    pairs = [(0.15, 0.13), (0.09, 0.07), (0.19, 0.17),   # float < 0.02
             (0.13, 0.11), (0.17, 0.15), (0.07, 0.05)]   # float > 0.02
    for i, (pe, ne) in enumerate(pairs):
        rows.append({
            "cond_id": f"b{i}", "objective": "pocv_dvdq", "noise": 0.0,
            "lli": 0.0, "lam_pe": pe, "lam_ne": ne,
            "lli_hat": 0.0, "lam_pe_hat": pe, "lam_ne_hat": ne,
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
    # 넓은 격차군이 없으면 gap_analysis 가 붕괴 지표를 안 낸다 — 함께 넣는다
    return pd.concat([pd.DataFrame(rows), _gap_fits(collapse=False, n=4, seed=7)],
                     ignore_index=True)


def test_nominal_2pp_gap_is_not_counted_as_small_gap():
    """★ 17차 발견 1 — nominal 2%p 는 `< 2%p` 가 아니다.

    문서가 수학적으로 `|ΔLAM|_true < 2%p` 라고 쓰므로, 표현 오차로 임계
    아래로 내려간 nominal 2%p 조건이 분모·분자에 들어가면 사건률 비가
    바뀐다. v4 실측: raw 98 vs nominal 66 (32조건이 표현 오차로 편입).
    """
    from tools.compare_objectives import gap_analysis

    g = gap_analysis(_scored(_boundary_frame()), "pocv_dvdq")

    assert g["n_small_gap_true"] == 0, (
        f"nominal 2%p 조건 {g['n_small_gap_true']}개가 `< 2%p` 군에 들어갔다")


def test_nominal_6pp_gap_is_counted_as_wide_gap():
    """★ 반대 방향 — nominal 6%p 는 `≥ 6%p` 다 (표현 오차로 빠지면 안 된다)."""
    from tools.compare_objectives import gap_analysis

    rows = []
    for i, (pe, ne) in enumerate([(0.19, 0.13), (0.17, 0.11), (0.13, 0.07)]):
        rows.append({
            "cond_id": f"w{i}", "objective": "pocv_dvdq", "noise": 0.0,
            "lli": 0.0, "lam_pe": pe, "lam_ne": ne,
            "lli_hat": 0.0, "lam_pe_hat": pe, "lam_ne_hat": ne,
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
    g = gap_analysis(_scored(pd.DataFrame(rows)), "pocv_dvdq")

    assert g["n_wide_gap_true"] == 3, g


def test_gap_sensitivity_uses_the_same_boundary_rule():
    """★ 발견 1 — `gap_analysis` 와 `gap_sensitivity` 가 같은 helper 를 써야 한다.

    민감도 표가 다른 경계 규약을 쓰면, 같은 (gap_thresh, tol) 칸이 본 분석과
    다른 분모를 보고한다.
    """
    from tools.compare_objectives import gap_analysis, gap_sensitivity

    # 경계 조건 + 진짜 작은-격차(PE=NE) 조건을 함께 — 그래야 (0.06,0.02) 칸이 산다
    eq = []
    for i, pe in enumerate([0.13, 0.11]):
        eq.append({
            "cond_id": f"e{i}", "objective": "pocv_dvdq", "noise": 0.0,
            "lli": 0.0, "lam_pe": pe, "lam_ne": pe,
            "lli_hat": 0.0, "lam_pe_hat": pe, "lam_ne_hat": pe,
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
    df = _scored(pd.concat([_boundary_frame(), pd.DataFrame(eq)],
                           ignore_index=True))
    g = gap_analysis(df, "pocv_dvdq", gap_thresh=0.06, tol=0.02)
    cell = [r for r in gap_sensitivity(df, "pocv_dvdq")
            if r["same_def"] == "lt_tol"
            and round(r["gap_thresh"], 6) == 0.06 and round(r["tol"], 6) == 0.02]

    assert cell, "민감도 표에 (0.06, 0.02) 칸이 없다"
    assert cell[0]["n_same"] == g["n_small_gap_true"], (
        f"민감도 n_same={cell[0]['n_same']} vs 본 분석 "
        f"n_small_gap_true={g['n_small_gap_true']}")
    assert cell[0]["n_wide"] == g["n_wide_gap_true"]


# ── 17차 발견 3·4·5·6·10 — 표와 반대이거나 protocol 과 안 맞는 서술 ──────────

def _noise_cmp_res(better_with_noise: bool):
    """노이즈별 표를 담은 최소 cmp_res.

    `better_with_noise=True` 면 34p 가 모든 noise 에서 33p 보다 **나쁘다**
    (paired 정본의 실제 방향). 그때 "dQ/dV 이점이 노이즈에서 희석된다" 는
    문장은 표와 반대다.
    """
    rows = []
    for noise, a, b in ((0.0, 0.60, 0.88), (0.001, 0.62, 0.88), (0.005, 0.64, 0.86)):
        if not better_with_noise:
            a, b = b, a
        for o, f in (("pocv_dvdq", a), ("pocv_dvdq_dqdv", b)):
            rows.append({"objective": o, "noise": noise, "n": 100,
                         "degenerate_frac": f, "degenerate_frac_corrected": f,
                         "mean_abs_err": 0.02, "pe_ne_antisym_frac": 0.5})
    return rows


def test_noise_dilution_claim_is_not_asserted_unconditionally():
    """★ 17차 발견 3 — "dQ/dV 이점은 노이즈에서 희석된다" 는 표와 반대다.

    paired 정본은 noise 0/0.001/0.005 에서 34p−33p 가 `+28/+26/+22%p` 로
    **어느 noise 에서도 이점이 없다**. 표를 보지 않고 문장을 박으면 안 된다.
    """
    from tools.make_results import _noise_note

    txt = _noise_note(_noise_cmp_res(better_with_noise=True))

    assert "희석" not in txt, f"표와 반대인 단정이 남아 있다: {txt}"
    assert "noise" in txt or "노이즈" in txt


def test_multistart_agree_frac_note_branches_on_protocol():
    """★ 17차 발견 4 — fixed-budget 실행에 adaptive 조기 종료 설명이 붙는다.

    paired 는 `adaptive=False`·restart 5 고정인데 같은 문서가 `agree_frac` 이
    "adaptive 조기 종료 때문에" 정의상 0 이라고 적는다.
    """
    from tools.make_results import _agree_frac_note

    assert "adaptive 조기 종료" in _agree_frac_note(adaptive=True)
    fixed = _agree_frac_note(adaptive=False)
    assert "adaptive 조기 종료" not in fixed, fixed
    assert "고정" in fixed, fixed


def test_unrecoverable_is_never_called_principally_impossible():
    """★ 17차 발견 6 — 결론에서는 완화하고 본문에서 "원리적으로" 로 되돌아간다.

    실제 분류는 `alpha_true >= 1-atol` 이라는 eligibility rule 이다
    (`src/scoring.py`). bounds 전체의 표현 가능성도, 다른 reference 의
    불가능성도 검사하지 않는다.
    """
    import re

    from tools.make_results import _unrecoverable_note

    txt = _unrecoverable_note()

    assert not re.search(r"원리적으로\s*\*{0,2}\s*복원", txt), txt
    assert "eligibility" in txt or "α-window" in txt, txt


def test_case_table_error_label_names_the_max_mode_statistic():
    """★ 17차 발견 5 — Case 표의 값은 `abs_err_max.mean()` 이다."""
    from tools.compare_cases import _case_markdown_header

    head = _case_markdown_header()

    assert "max-mode" in head, head


def test_conclusion_2_renders_both_all_population_numerators():
    """★ 17차 발견 10-1 — 전체군 사건률 비의 **반대쪽 분자**가 결론에 없다.

    `64/604` 와 3.69 만 쓰면 핵심 결론만으로 비를 검산할 수 없다.
    """
    from tools.make_results import _conclusion

    cmp_res = _gap_cmp_res()
    cmp_res["gap_analysis_all_conditions"]["pocv_dvdq"].update(
        {"n_small_gap_true": 93, "false_split_frac": 1 - 34 / 93})
    txt = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))

    assert "34/93" in txt, txt[txt.index("2. "):][:900]


def test_conclusion_22p_states_noise_and_radius():
    """★ 17차 발견 10-2 — 22p 결론에 `noise` 와 `radius` 가 없다."""
    from tools.make_results import _conclusion

    cmp_res = _gap_cmp_res()
    cmp_res["verdict_22p"] = {"pocv_dvdq": {
        "n_near": 8, "degenerate_frac": 0.125, "mean_abs_err": 0.0168,
        "pe_ne_antisym_frac": 0.5, "true_pe_ne_gap": 0.010,
        "recovered_pe_ne_gap": 0.019, "noise": 0.0, "radius": 0.021,
        "n_near_exact_equal": 4, "max_true_pe_ne_gap": 0.02}}
    txt = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))

    seg = txt[txt.index("3. **22p"):]
    assert "noise=0" in seg, seg[:700]
    assert "radius=0.021" in seg, seg[:700]


def test_threshold_caveat_does_not_claim_the_rate_is_purely_thresholds():
    """★ 17차 발견 10-3 — "낮은 붕괴율은 측정이 아니라 임계 설정의 결과" 는 과도.

    임계 간격 4%p > 실측 중앙 격차오차 2.6%p 는 붕괴를 어렵게 만든다는 뜻이지,
    관측률 전체가 임계 설정만의 결과라는 증명이 아니다.
    """
    from tools.make_results import _gap_table_legend

    txt = _gap_table_legend()

    assert "측정이 아니라 임계 설정의" not in txt, txt
    assert "일부는" in txt or "상당 부분" in txt, txt


# ── 17차 발견 9 — 22p selection protocol 공유 ────────────────────────────────

def test_verdict_22p_records_its_selection_protocol():
    """★ 17차 발견 9 — `radius` 는 결론을 정의하는 protocol 인데 기록되지 않았다.

    renderer 가 구성 helper 를 부를 때 기본값 0.021 을 다시 쓰므로, verdict 를
    다른 radius 로 계산하면 **서로 다른 표본**의 `n_near` 와 구성 문장이
    한 문단에 섞인다.
    """
    from tools.compare_objectives import verdict_22p

    v = verdict_22p(_scored(_p22_frame()), "pocv_dvdq", radius=0.05)

    assert v["radius"] == pytest.approx(0.05), v


def test_p22_composition_refuses_a_different_sample():
    """★ 발견 9 — 구성과 verdict 의 표본이 다르면 렌더를 실패시킨다."""
    from tools.make_results import _p22_composition

    v = {"n_near": 8, "n_near_exact_equal": 4, "max_true_pe_ne_gap": 0.02,
         "n_near_composition": 6}          # 구성이 다른 표본에서 나왔다
    with pytest.raises(ValueError, match="표본"):
        _p22_composition(v, {"gap_thresh": 0.06})


def test_build_passes_the_recorded_radius_to_the_composition_helper(tmp_path, monkeypatch):
    """★ 발견 9 — renderer 가 기본값이 아니라 **기록된 radius** 를 써야 한다."""
    import tools.compare_objectives as co
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)

    seen: list = []
    orig = co.p22_truth_composition

    def spy(frame, objective="pocv_dvdq", noise=0.0, radius=0.021):
        seen.append(radius)
        return orig(frame, objective, noise, radius)

    monkeypatch.setattr(co, "p22_truth_composition", spy)
    build(d, tmp_path / "R.md", repo_root=tmp_path)

    assert seen, "구성 helper 가 호출되지 않았다"
    from tools.compare_objectives import verdict_22p
    want = verdict_22p(_scored(df), "pocv_dvdq")["radius"]
    assert all(r == pytest.approx(want) for r in seen), (seen, want)


# ── 17차 발견 7 — Hessian 은 녹색 배지·재현 명령 범위 밖이다 ─────────────────

def _hessian_run(d, objectives=("pocv_dvdq",), eps=1e-4):
    """fit 디렉터리에 Hessian 산출물을 놓는다 (렌더 경로만 태운다)."""
    for o in objectives:
        pd.DataFrame({
            "cond_id": [f"c{i}" for i in range(4)],
            "condition_number": [12.8, 229.0, 17381.0, 44.0],
            "flat_direction_score": [0.1, 0.2, 0.3, 0.4],
            "min_eigval_positive": [True, True, False, True],
            "pe_ne_coupled": [True, False, False, True],
            "eps": [eps] * 4,
        }).to_parquet(d / f"hessian_{o}.parquet", index=False)


def _built_with_hessian(tmp_path):
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    _hessian_run(d)
    run_compare(d, d)
    return build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")


def test_reproduce_block_does_not_offer_a_broken_hessian_command(tmp_path):
    """★ 17차 발견 7 — 재현 명령의 `--mode hessian` 은 분리배치에서 실패한다.

    `src/hessian.py:135` 가 `curves.parquet` 을 못 찾고, 곡선을 임시로 놓아도
    `degeneracy_summary.yaml` 을 변이시켜 보고서를 stale 로 만든다 (A·B 미수정).
    문서가 그 명령을 제시하면 독자가 artifact 를 망가뜨린다.
    """
    text = _built_with_hessian(tmp_path)

    assert "--mode hessian" not in text, \
        "A·B 가 닫히기 전에는 Hessian 재현 명령을 제시하면 안 된다"


def test_hessian_is_declared_outside_the_provenance_scope(tmp_path):
    """★ 발견 7 — 녹색 provenance 배지가 Hessian 까지 검증한 것처럼 보인다.

    fit provenance validator 는 Hessian 의 fits·곡선·obj_cfg·v_col·reference·
    표본·eps 연결을 전혀 보지 않는다. 범위를 문서가 명시해야 한다.
    """
    text = _built_with_hessian(tmp_path)

    i = text.index("곡률 진단")
    assert "provenance 검증 범위 밖" in text[i:i + 1200], text[i:i + 900]


def test_hessian_eps_ordering_claim_needs_more_than_one_objective(tmp_path):
    """★ 발견 7 추가 — "같은 eps 에서의 순서는 의미 있다" 는 지지되지 않는다.

    표에 objective 가 하나뿐이면 순서 자체가 없다.
    """
    text = _built_with_hessian(tmp_path)

    i = text.index("곡률 진단")
    seg = text[i:i + 2500]
    assert "같은 eps에서의 순서**뿐입니다" not in seg, seg[:900]


def test_sensitivity_says_when_the_two_same_definitions_coincide():
    """★ 17차 자체 발견 — 경계 규약을 고치면 F34 의 두 정의가 **같은 집합**이 된다.

    격자 step 이 0.02 이므로 canonical 하게 `참 격차 < 2%p` 는 `참 격차 == 0` 과
    같다. v4 에서 tol=1%p·2%p 열의 두 패널이 완전히 동일해진다(n_same 66, LR
    89.09). 두 패널을 나란히 실으면서 그 사실을 적지 않으면, 독자는 서로 독립인
    두 확인으로 읽는다 — F34 가 두 정의를 나눈 이유(임계 효과 분리)가 인용
    지점에서는 성립하지 않는다.
    """
    from tools.make_results import _same_def_overlap_note

    same = [{"same_def": "lt_tol", "tol": 0.02, "gap_thresh": 0.06, "n_same": 66},
            {"same_def": "exact_zero", "tol": 0.02, "gap_thresh": 0.06, "n_same": 66}]
    diff = [{"same_def": "lt_tol", "tol": 0.05, "gap_thresh": 0.06, "n_same": 247},
            {"same_def": "exact_zero", "tol": 0.05, "gap_thresh": 0.06, "n_same": 66}]

    txt = _same_def_overlap_note(same + diff, tol=0.02, gap_thresh=0.06)
    assert "같은 집합" in txt, txt
    assert "66" in txt, txt

    assert _same_def_overlap_note(same + diff, tol=0.05, gap_thresh=0.06) == ""


# ── 18차 발견 1 — collapse_measurable 은 붕괴 관측 가능성을 증명하지 않는다 ──

def test_collapse_measurable_is_gone():
    """★ 18차 발견 1 — 부호와 행별 필요량을 버린 지표다.

    `|recovered − true|` 의 p99 를 모든 행 공통 `gap_thresh − tol` 과 비교했다.
    붕괴에는 (a) `true − recovered > 0` 방향과 (b) 행마다 다른 필요 감소량
    `true − tol` 이 필요한데 둘 다 버린다. 반례: true 0.10 → recovered 0.20 은
    붕괴와 **정반대** 방향인데 절대오차 0.10 으로 measurable 판정을 받는다.
    게다가 같은 결과에서 뽑은 오차분포로 그 결과의 낮은 사건률을 방어하므로
    논리도 순환적이다.
    """
    from tools.compare_objectives import gap_analysis

    df = pd.DataFrame({"objective": ["x"], "noise": [0.0], "recoverable": [True],
                       "pe_ne_gap_true": [0.10], "pe_ne_gap_recovered": [0.20]})
    g = gap_analysis(df, "x")

    assert "collapse_measurable" not in g, g
    assert g["gap_collapse_frac"] == 0.0


def test_collapse_margin_is_signed_and_row_wise():
    """★ 대체 지표 — 부호 있는 행별 여유(margin)를 기술통계로만 낸다.

    margin = (참 격차 − 복원 격차) − (참 격차 − tol)
           = tol − 복원 격차
    즉 복원 격차가 tol 아래로 얼마나 더 내려가야 붕괴인가. 양수면 이미 붕괴.
    """
    from tools.compare_objectives import gap_analysis

    df = pd.DataFrame({
        "objective": ["x"] * 3, "noise": [0.0] * 3, "recoverable": [True] * 3,
        "pe_ne_gap_true": [0.10, 0.10, 0.10],
        "pe_ne_gap_recovered": [0.20, 0.05, 0.01],   # 반대방향 / 근접 / 붕괴
    })
    g = gap_analysis(df, "x")

    # 복원 0.20 → margin −0.18, 0.05 → −0.03, 0.01 → +0.01
    assert g["collapse_margin_median"] == pytest.approx(-0.03), g
    assert g["collapse_margin_max"] == pytest.approx(0.01), g
    assert g["n_wide_gap_toward_collapse"] == 2, g   # 격차가 줄어든 행 수


def test_conclusion_does_not_claim_collapse_was_observable():
    """★ 발견 1 — "붕괴가 원리적으로 관측 가능한 범위" 문장을 삭제한다."""
    from tools.make_results import _conclusion

    txt = "\n".join(_conclusion(_gap_cmp_res(), {"n_rows_recoverable": 1476}))

    assert "관측 가능한 범위" not in txt, txt[txt.index("2. "):][:800]
    assert "상당 부분" not in txt, "핵심 결론과 표 범례가 서로 다른 강도를 쓴다"


# ── 18차 발견 2·3·7·8·9·10 ─────────────────────────────────────────────────

def test_conclusion_unrecoverable_uses_eligibility_criterion_only():
    """★ 18차 발견 3 — `classify_recoverability()` 는 `alpha_true >= 1-atol` 만 본다.

    configured box bounds 도, β 도, 물리 feasible domain 도 검사하지 않는다.
    `α/bounds feasible domain 밖` 은 그 판정보다 넓은 주장이다.
    """
    from tools.make_results import _conclusion

    txt = "\n".join(_conclusion(_gap_cmp_res(), {"n_rows_recoverable": 1476}))

    assert "feasible domain" not in txt, txt[-700:]
    assert "eligibility" in txt, txt[-700:]


def test_multistart_random_only_note_branches_on_warm_start():
    """★ 18차 발견 2 — no-warm 실행에 warm-start 인과 설명이 붙는다.

    paired 정본은 `--no-warm-start` 라 restart 0 은 warm solution 이 아니라
    `base_init` 이다. 그런데 `multistart_random_only` 블록의 존재만 보고
    warm 전용 설명을 냈다.
    """
    from tools.make_results import _random_only_note

    warm = _random_only_note(warm_start=True)
    nowarm = _random_only_note(warm_start=False)

    assert "매끄러운 해를 초기값으로" in warm, warm
    assert "매끄러운 해를 초기값으로" not in nowarm, nowarm
    assert "base_init" in nowarm or "결정론적" in nowarm, nowarm


def test_objective_section_heading_counts_the_rendered_objectives():
    """★ 발견 2 — paired 는 2종인데 제목이 "4종" 이다."""
    from tools.make_results import _objective_section_heading

    assert _objective_section_heading(2) == "## 목적함수 2종 비교"
    assert _objective_section_heading(4) == "## 목적함수 4종 비교"


def test_p_spread_zero_is_not_equated_with_a_single_restart():
    """★ 18차 발견 7 — 여러 restart 가 같은 p 로 수렴해도 spread 는 0 이다."""
    from tools.make_results import _agree_frac_note

    for adaptive in (True, False):
        txt = _agree_frac_note(adaptive)
        assert "하나뿐\"이라는 뜻" not in txt, txt
        assert "같은 파라미터에 수렴" in txt, txt


def test_sensitivity_range_names_which_panel_it_came_from():
    """★ 18차 발견 8 — 범위는 `lt_tol` 패널에서만 계산된다.

    보고서는 exact-zero 패널도 함께 싣고 그 최대값은 다르다. 한 범위를 전체
    민감도 범위처럼 쓰면 안 된다.
    """
    from tools.make_results import _conclusion

    cmp_res = _gap_cmp_res()
    cmp_res["gap_analysis"]["pocv_dvdq"]["lr_sensitivity_max_exact_zero"] = 165.4
    txt = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))

    assert "`<tol` 정의" in txt or "lt_tol" in txt, txt[txt.index("2. "):][:1200]
    assert "165.4" in txt, txt[txt.index("2. "):][:1200]


def test_p22_wide_judgment_uses_the_shared_boundary_rule():
    """★ 18차 발견 9 — p22 최대 격차 판정만 raw `<` 를 쓴다.

    `0.05999999999999999` 가 임계 0.06 일 때 다른 분석과 다른 문장이 나온다.
    """
    from tools.make_results import _p22_composition

    v = {"n_near": 8, "n_near_exact_equal": 4,
         "max_true_pe_ne_gap": 0.29 - 0.23,        # 0.05999999999999997
         "n_near_composition": 8}
    c = _p22_composition(v, {"gap_thresh": 0.06})

    assert "하나도 없" not in c["wide"], (
        f"nominal 6%p 를 wide-gap 부재로 판정했다: {c['wide']}")


def test_p22_composition_flags_the_empty_radius_fallback():
    """★ 발견 9 — radius 안에 점이 없으면 밖의 최근접 1점으로 대체된다.

    그런데 renderer 는 항상 "radius 안의 조건" 이라고 쓴다.
    """
    from tools.compare_objectives import p22_truth_composition

    far = pd.DataFrame([{
        "cond_id": "f0", "objective": "pocv_dvdq", "noise": 0.0,
        "lli": 0.02, "lam_pe": 0.02, "lam_ne": 0.02,
        "lli_hat": 0.02, "lam_pe_hat": 0.02, "lam_ne_hat": 0.02,
        "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
    }])
    c = p22_truth_composition(_scored(far), "pocv_dvdq", radius=0.001)

    assert c["p22_radius_fallback"] is True, c


def test_hessian_does_not_assert_saddle_points(tmp_path):
    """★ 18차 발견 10 — eps 미수렴 상태에서 saddle 과 수치 artifact 를 못 가른다."""
    text = _built_with_hessian(tmp_path)

    i = text.index("곡률 진단")
    seg = text[i:i + 3000]
    assert "안장점**에서 곡률을 잰 것" not in seg, seg[:1500]
    assert "구분하지 않습니다" in seg, seg[:1500]
    assert "입증되지 않은" in seg, seg[:1500]


def test_reproduction_scope_is_rendered_from_what_was_emitted(tmp_path):
    """★ 18차 발견 4 — "재현 범위" 가 고정 boilerplate 였다.

    paired 는 sweep·half-cell 절도 명령도 없는데 그 설정을 복원한다고 썼고,
    main 은 Hessian 명령을 뺐으면서 뒤 문장에서는 **비기본 eps** 만 빠진 축인
    것처럼 읽혔다. 실제로 출력한 명령이 재현하는 절만 열거해야 한다.
    """
    from tools.make_results import _reproduction_scope_note

    bare = _reproduction_scope_note(has_wsweep=False, has_halfcell=False,
                                    has_hessian=False, warm_start=False)
    assert "sweep" not in bare, bare
    assert "half-cell" not in bare, bare

    full = _reproduction_scope_note(has_wsweep=True, has_halfcell=True,
                                    has_hessian=True, warm_start=True)
    assert "sweep" in full and "half-cell" in full, full
    # Hessian 절이 있으면 **기본 eps 포함 전체**가 명령에서 빠졌다고 말해야 한다
    assert "Hessian 절" in full, full
    assert "비기본" not in full, "기본 Hessian 도 빠졌는데 비기본만 빠진 것처럼 쓴다"


# ── 18차 발견 6 — 파생 산출물의 versioned analysis manifest ─────────────────

def test_comparison_yaml_carries_its_own_analysis_anchor(tmp_path):
    """★ 18차 발견 6 — YAML 을 **직접 읽는** 소비자가 이번 오류의 시작점이다.

    파일 자체에 schema version·spec id·fits anchor 가 없으면, 복원한 사람이
    그 숫자가 어느 fits 에서 어느 규약으로 나왔는지 알 수 없다.
    """
    import yaml

    from tools.compare_objectives import run_compare

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)

    y = yaml.safe_load((d / "objective_comparison.yaml").read_text(encoding="utf-8"))
    a = y.get("_analysis")
    assert a, "objective_comparison.yaml 에 `_analysis` self-description 이 없다"
    assert a["schema_version"] >= 1
    assert len(a["analysis_spec_id"]) == 64
    assert len(a["fits_sha256"]) == 64


def test_analysis_anchor_does_not_trip_the_stale_check(tmp_path):
    """★ `_analysis` 는 `_` 로 시작해 F87 key 집합 대조에서 제외돼야 한다."""
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)
    text = build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(encoding="utf-8")

    assert "파생_stale_objective_comparison.yaml" not in text


def test_analysis_manifest_records_the_full_provenance_chain(tmp_path):
    """★ 발견 6 — raw producer 와 derived generator 를 **분리** 기록한다.

    `manifest.yaml` 에 파생 정보를 덧붙이면 후대 분석 코드를 원래 계산에 거짓
    귀속하게 된다. 별도 `analysis_manifest.yaml` 이어야 한다.
    """
    import yaml

    from tools.compare_objectives import run_compare

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)

    m = yaml.safe_load((d / "analysis_manifest.yaml").read_text(encoding="utf-8"))

    assert m["analysis_schema_version"] >= 1
    assert len(m["analysis_spec_id"]) == 64
    assert len(m["raw_inputs"]["fits_sha256"]) == 64
    g = m["generator"]
    assert len(g["git_commit"]) in (0, 40)
    assert g["source_digest"]
    assert g["git_dirty"] in (True, False)
    p = m["parameters"]
    assert p["tol"] == 0.02 and p["gap_thresh"] == 0.06
    assert p["gap_atol"] == 1e-9
    assert p["p22_center"] == [0.13, 0.13, 0.17]
    assert p["p22_radius"] == 0.021
    assert p["p22_metric"] == "unscaled_euclidean_fractional_coordinates"
    assert p["p22_empty_radius_policy"] == "nearest_fallback"
    assert len(p["selected_condition_ids_sha256"]) == 64
    assert len(m["derived_outputs"]["objective_comparison.yaml"]) == 64
    # raw 계산 manifest 는 건드리지 않는다
    assert "analysis_schema_version" not in (
        yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
        if (d / "manifest.yaml").exists() else {})


def test_derived_semantic_gate_fails_on_stale_yaml(tmp_path):
    """★ 발견 6 — 보관 전에 **봉인 fits 에서 재계산**해 의미 동치를 검사한다.

    `payload_sha256.yaml` 은 stale bytes 도 충실히 해시한다. 바이트 보존은
    파생 파일이 최신 의미를 담는지 증명하지 못한다.
    """
    import yaml

    from tools.compare_objectives import run_compare, verify_derived_freshness

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)

    assert verify_derived_freshness(d)["ok"] is True

    # 저장본의 숫자 하나를 옛 값으로 되돌린다 (= stale 보관본 재현)
    y = yaml.safe_load((d / "objective_comparison.yaml").read_text(encoding="utf-8"))
    y["gap_analysis"]["pocv_dvdq"]["n_small_gap_true"] = 98
    (d / "objective_comparison.yaml").write_text(
        yaml.safe_dump(y, allow_unicode=True, sort_keys=False), encoding="utf-8")

    got = verify_derived_freshness(d)
    assert got["ok"] is False, got
    assert any("n_small_gap_true" in w for w in got["fail"]), got


def test_archive_gate_blocks_a_run_whose_derived_yaml_is_stale(tmp_path):
    """★ 18차 발견 6 — 보관 게이트가 파생 semantic freshness 를 봐야 한다.

    지금까지 게이트는 raw inputs/fits provenance 만 봤다. stale 파생 YAML 은
    바이트 무결성 검사를 그대로 통과하므로 묶음 안으로 들어갔다.
    """
    import subprocess
    import sys

    import yaml

    from tools.compare_objectives import run_compare

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)

    root = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, "-m", "tools.check_derived_fresh", str(d)]
    ok = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr

    y = yaml.safe_load((d / "objective_comparison.yaml").read_text(encoding="utf-8"))
    y["gap_analysis"]["pocv_dvdq"]["n_small_gap_true"] = 98
    (d / "objective_comparison.yaml").write_text(
        yaml.safe_dump(y, allow_unicode=True, sort_keys=False), encoding="utf-8")

    bad = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert bad.returncode != 0, bad.stdout
    assert "n_small_gap_true" in bad.stdout + bad.stderr


# ── 19차 사전 자체 발견 — freshness 게이트 비대칭 + fallback 렌더 미분기 ─────

def _freshness_fixture(tmp_path):
    from tools.compare_objectives import run_compare

    d = tmp_path / "res"
    d.mkdir()
    df = pd.concat([_gap_fits(collapse=True), _fits(objectives=("pocv_dvdq",))],
                   ignore_index=True)
    _scored(df).to_parquet(d / "degeneracy_map.parquet", index=False)
    df.to_parquet(d / "fits.parquet", index=False)
    run_compare(d, d)
    return d


def test_freshness_gate_catches_a_subset_stale_yaml(tmp_path):
    """★ 19차 사전 발견 1 — walk 가 saved→now 한 방향만 돌았다.

    새 코드가 계산하는 key 가 **빠진** 저장본(= 더 오래된 schema)이 공유 key 의
    숫자만 맞으면 통과했다. v4.1 재보관 직후 실측으로 증명한 구멍이다.
    """
    import yaml

    from tools.compare_objectives import verify_derived_freshness

    d = _freshness_fixture(tmp_path)
    p = d / "objective_comparison.yaml"
    y = yaml.safe_load(p.read_text(encoding="utf-8"))
    del y["gap_analysis"]["pocv_dvdq"]["collapse_margin_median"]
    p.write_text(yaml.safe_dump(y, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")

    got = verify_derived_freshness(d)
    assert got["ok"] is False, "부분집합-stale 이 게이트를 통과했다"
    assert any("collapse_margin_median" in w for w in got["fail"]), got


def test_freshness_gate_checks_the_analysis_spec_id(tmp_path):
    """★ 19차 사전 발견 2 — spec 이 다른 파일은 숫자가 맞아도 stale 이다."""
    import yaml

    from tools.compare_objectives import verify_derived_freshness

    d = _freshness_fixture(tmp_path)
    p = d / "objective_comparison.yaml"
    y = yaml.safe_load(p.read_text(encoding="utf-8"))
    y["_analysis"]["analysis_spec_id"] = "0" * 64
    p.write_text(yaml.safe_dump(y, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")

    got = verify_derived_freshness(d)
    assert got["ok"] is False, got
    assert any("analysis_spec_id" in w for w in got["fail"]), got


def test_conclusion_22p_says_fallback_instead_of_inside_radius():
    """★ 19차 사전 발견 3 — 18차 발견 9 의 부분 마감.

    `radius_fallback` 을 **기록**만 하고 renderer 는 무조건 "radius 안의 최근접
    N grid 조건" 이라고 썼다. fallback 이면 그 문장은 거짓이다.
    """
    from tools.make_results import _conclusion

    cmp_res = _gap_cmp_res()
    base = {"n_near": 1, "degenerate_frac": 0.0, "mean_abs_err": 0.01,
            "pe_ne_antisym_frac": 0.0, "true_pe_ne_gap": 0.0,
            "recovered_pe_ne_gap": 0.0, "noise": 0.0, "radius": 0.021,
            "n_near_composition": 1, "n_near_exact_equal": 1,
            "max_true_pe_ne_gap": 0.0}
    cmp_res["verdict_22p"] = {"pocv_dvdq": dict(base, radius_fallback=True)}
    fb = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))
    seg = fb[fb.index("3. **22p"):]

    assert "안의 최근접" not in seg, "fallback 인데 'radius 안' 이라고 쓴다"
    assert "밖" in seg and ("최근접 1" in seg or "대체" in seg), seg[:500]

    cmp_res["verdict_22p"] = {"pocv_dvdq": dict(base, radius_fallback=False)}
    ok = "\n".join(_conclusion(cmp_res, {"n_rows_recoverable": 1476}))
    assert "안의 최근접" in ok[ok.index("3. **22p"):]
