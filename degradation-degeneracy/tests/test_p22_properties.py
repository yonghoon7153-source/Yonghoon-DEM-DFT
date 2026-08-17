"""22p 선택·경계 규약의 **property test** (★ 18차 Q4 3층).

단위 테스트는 "이 값에서 이 답" 을 고정한다. 여기서는 **불변식**을 고정한다 —
radius·noise·격자 간격·empty-radius fallback·임계 부동소수점 표현을 흔들면서,
어떤 조합에서도 깨지면 안 되는 성질만 본다.

리뷰가 요구한 핵심 불변식
────────────────────────
P1  선택 집합 일치   verdict 와 구성이 **같은 표본**에서 나온다
P2  경계 규약 일관   nominal 격자값은 표현 오차와 무관하게 같은 쪽에 들어간다
P3  fallback 정직    radius 안에 점이 없으면 그 사실이 fact 에 실린다
P4  단조성           radius 를 넓히면 표본이 줄어들지 않는다
P5  문장-사실 대응   렌더된 문장이 fact 와 어긋나지 않는다
"""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import pytest

from tests.test_compare import _scored
from tools.compare_objectives import (EXP_22P, GAP_ATOL, gap_analysis, gap_ge,
                                      gap_is_zero, gap_lt,
                                      p22_truth_composition, verdict_22p)

RADII = (0.005, 0.021, 0.05, 0.12)
NOISES = (0.0, 0.001)
STEPS = (0.01, 0.02, 0.05)
#: 0 이 아닌 offset 은 반경 안을 비워 fallback 경로를 태운다
OFFSETS = (0.0, 0.035)


def _grid(step: float, noise: float = 0.0, half: int = 2,
          offset: float = 0.0) -> pd.DataFrame:
    """`EXP_22P` 중심의 정육면체 격자 — step·offset 을 바꿔가며 만든다.

    ★ `offset` 이 없으면 격자에 중심점이 **항상** 포함돼 empty-radius fallback
    이 한 번도 일어나지 않는다. 실제로 그래서 P1·P3 축이 통째로 안 태워졌고,
    뮤테이션(fallback 을 항상 False 로)이 물지 않아 발각됐다.
    """
    rows, k = [], 0
    rng = range(-half, half + 1)
    for i, j, l in itertools.product(rng, rng, rng):
        pe = round(EXP_22P["lam_pe"] + offset + i * step, 10)
        ne = round(EXP_22P["lam_ne"] + offset + j * step, 10)
        li = round(EXP_22P["lli"] + offset + l * step, 10)
        if min(pe, ne, li) < 0 or max(pe, ne) > 0.45:
            continue
        rows.append({
            "cond_id": f"c{k}", "objective": "pocv_dvdq", "noise": noise,
            "lli": li, "lam_pe": pe, "lam_ne": ne,
            "lli_hat": li, "lam_pe_hat": pe, "lam_ne_hat": ne,
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
        k += 1
    return _scored(pd.DataFrame(rows))


@pytest.mark.parametrize("step", STEPS)
@pytest.mark.parametrize("radius", RADII)
@pytest.mark.parametrize("noise", NOISES)
@pytest.mark.parametrize("offset", OFFSETS)
def test_p1_verdict_and_composition_see_the_same_sample(step, radius, noise, offset):
    """P1 — 같은 protocol 이면 두 함수의 표본 크기가 반드시 같다."""
    df = _grid(step, noise, offset=offset)
    v = verdict_22p(df, "pocv_dvdq", noise=noise, radius=radius)
    c = p22_truth_composition(df, "pocv_dvdq", noise=noise, radius=radius)

    assert v["n_near"] == c["n_near_composition"], (step, radius, noise, offset)
    assert v["radius_fallback"] == c["p22_radius_fallback"]
    assert v["radius"] == pytest.approx(radius)


@pytest.mark.parametrize("step", STEPS)
@pytest.mark.parametrize("radius", RADII)
@pytest.mark.parametrize("offset", OFFSETS)
def test_p3_fallback_is_reported_exactly_when_the_radius_is_empty(step, radius, offset):
    """P3 — fallback 플래그가 "반경 안에 점이 없다" 와 정확히 동치인가."""
    df = _grid(step, offset=offset)
    sub = df[df["objective"] == "pocv_dvdq"]
    d = np.sqrt(sum((sub[k] - v) ** 2 for k, v in EXP_22P.items()))
    empty = bool((d <= radius).sum() == 0)

    v = verdict_22p(df, "pocv_dvdq", radius=radius)
    assert v["radius_fallback"] is empty, (step, radius, offset,
                                          int((d <= radius).sum()))
    if empty:
        assert v["n_near"] == 1, "fallback 이면 최근접 1점이어야 한다"


@pytest.mark.parametrize("step", STEPS)
def test_p4_widening_the_radius_never_shrinks_the_sample(step):
    """P4 — 단조성. 반경을 넓혔는데 표본이 줄면 선택 로직이 깨진 것이다."""
    df = _grid(step)
    counts = [verdict_22p(df, "pocv_dvdq", radius=r)["n_near"] for r in RADII]
    # fallback(반경 비어 최근접 1점) 구간을 지난 뒤부터는 단조 증가여야 한다
    real = [(r, n) for r, n in zip(RADII, counts)
            if not verdict_22p(df, "pocv_dvdq", radius=r)["radius_fallback"]]
    ns = [n for _, n in real]
    assert ns == sorted(ns), (step, real)


@pytest.mark.parametrize("mult", range(1, 25))
def test_p2_nominal_grid_values_land_on_the_intended_side(mult):
    """P2 — nominal 격자값은 표현 오차와 무관하게 같은 쪽에 들어간다.

    `0.01 * k` 를 뺀 값은 이진 부동소수점에서 임계 위·아래 어느 쪽으로도
    떨어진다. 경계 helper 는 **수학적 값** 기준으로 판정해야 한다.
    """
    thresh = round(0.01 * mult, 10)
    # 같은 nominal 값을 여러 경로로 만들어 표현이 갈리게 한다
    variants = [thresh,
                sum(0.01 for _ in range(mult)),
                (0.13 + thresh) - 0.13,
                float(np.float64(thresh))]
    for x in variants:
        assert not gap_lt(x, thresh), f"{x!r} 가 {thresh} '미만' 으로 판정됐다"
        assert gap_ge(x, thresh), f"{x!r} 가 {thresh} '이상' 이 아니라고 판정됐다"


@pytest.mark.parametrize("mult", range(1, 25))
def test_p2_values_strictly_below_stay_below(mult):
    """P2 반대편 — 한 격자칸 아래는 반드시 '미만' 이어야 한다."""
    thresh = round(0.01 * mult, 10)
    below = round(thresh - 0.01, 10)
    if below <= 0:
        assert gap_is_zero(max(below, 0.0))
        return
    assert gap_lt(below, thresh)
    assert not gap_ge(below, thresh)


def test_p2_zero_rule_is_tighter_than_the_threshold_rule():
    """P2 — exact-zero 판정이 atol 보다 넓어지면 안 된다."""
    assert gap_is_zero(0.0)
    assert gap_is_zero(GAP_ATOL / 2)
    assert not gap_is_zero(1e-6), "1e-6 격차를 '정확히 0' 으로 세면 안 된다"


@pytest.mark.parametrize("step", STEPS)
def test_p2_gap_analysis_denominators_are_grid_consistent(step):
    """P2 — 분모가 격자 구조와 모순되지 않는가.

    작은-격차군은 `< tol`, 넓은-격차군은 `>= gap_thresh` 이므로 두 군은 절대
    겹치지 않고, 합이 전체를 넘지 않는다.
    """
    df = _grid(step)
    g = gap_analysis(df, "pocv_dvdq", tol=0.02, gap_thresh=0.06)
    n_total = int((df["objective"] == "pocv_dvdq").sum())

    assert g["n_small_gap_true"] + g["n_wide_gap_true"] <= n_total
    assert g["n_exact_zero_gap_true"] <= g["n_small_gap_true"]


@pytest.mark.parametrize("radius", RADII)
@pytest.mark.parametrize("step", STEPS)
def test_p5_rendered_sentence_agrees_with_the_facts(step, radius):
    """P5 — 문장이 fact 와 어긋나지 않는가 (fallback·구성·wide-gap 부재)."""
    from tools.make_results import P22RenderFacts, _p22_composition

    df = _grid(step)
    v = verdict_22p(df, "pocv_dvdq", radius=radius)
    c = p22_truth_composition(df, "pocv_dvdq", radius=radius)
    f = P22RenderFacts.build(v, c, {"gap_thresh": 0.06})
    txt = _p22_composition(f)

    assert f"/{f.n_near}" in txt["detail"], (txt, f)
    # wide-gap 부재 문장은 최대 참 격차가 임계 미만일 때만
    if gap_ge(f.max_true_pe_ne_gap, f.gap_thresh):
        assert "하나도 없" not in txt["wide"], (step, radius, f)
    else:
        assert "하나도 없" in txt["wide"], (step, radius, f)


def test_p1_default_selection_protocol_is_shared():
    """P1 보강 — 두 함수의 **기본 radius** 가 같아야 한다.

    renderer 가 기록된 radius 를 넘기도록 고쳤지만(17차 발견 9), 기본값이
    갈려 있으면 그 경로를 안 타는 호출자가 조용히 다른 표본을 본다.
    """
    import inspect

    a = inspect.signature(verdict_22p).parameters["radius"].default
    b = inspect.signature(p22_truth_composition).parameters["radius"].default
    assert a == b, f"기본 radius 가 다르다: verdict={a} composition={b}"


@pytest.mark.parametrize("radius", (0.01, 0.02, 0.05))
def test_p3_a_point_exactly_at_the_radius_is_included(radius):
    """P3 보강 — 거리가 **정확히 radius** 인 점은 포함이다 (`<=`).

    격자 property 만으로는 이 경계가 안 태워졌다 (거리 == radius 인 점이
    생기지 않는다). 뮤테이션(`<=` → `<`)이 물지 않아 발각됐다.
    """
    rows = []
    for k, (dx, tag) in enumerate(((radius, "on"), (radius * 2, "out"))):
        rows.append({
            "cond_id": f"b{k}_{tag}", "objective": "pocv_dvdq", "noise": 0.0,
            "lli": EXP_22P["lli"], "lam_pe": EXP_22P["lam_pe"] + dx,
            "lam_ne": EXP_22P["lam_ne"],
            "lli_hat": EXP_22P["lli"], "lam_pe_hat": EXP_22P["lam_pe"] + dx,
            "lam_ne_hat": EXP_22P["lam_ne"],
            "r": 0.75, "a_pe": 1.0, "a_ne": 1.0, "reference": "grid",
        })
    v = verdict_22p(_scored(pd.DataFrame(rows)), "pocv_dvdq", radius=radius)

    assert v["radius_fallback"] is False, "경계 위의 점을 반경 밖으로 뒀다"
    assert v["n_near"] == 1, (radius, v)
