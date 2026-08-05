"""fitting / objective 검증 (solve 없음 — 빠름).

핵심:
  test_identity              α=1, β=0 이면 reference와 정확히 일치
  test_recovers_known_alpha  α_PE=0.9로 만든 곡선에서 0.9를 복원
  test_bound_active_flagged  최적해가 bound에 붙으면 플래그
  test_alpha_relation        α = (1−LAM)/r 관계와 역환산 일관성
"""

from __future__ import annotations

import numpy as np
import pytest

from src.config import load_config
from src.fitting import (_bound_active, fit, make_ref_interp, modes_to_params,
                         reconstruct, to_degradation_modes)
from src.objective import compute_features, default_scales, make_objective
from tests.conftest import ROOT

X = np.linspace(0, 1, 300)


@pytest.fixture(scope="module")
def obj_cfg():
    return load_config(ROOT / "configs" / "objectives.yaml")


@pytest.fixture(scope="module")
def refs():
    """합성 half-cell 곡선 — 실제 곡선과 유사한 단조 형태 + 미세 구조(피크용)."""
    pe = 4.25 - 0.55 * X - 0.25 * X ** 3 + 0.02 * np.sin(9 * np.pi * X)
    ne = 0.06 + 0.9 * X ** 6 + 0.03 * np.sin(7 * np.pi * X)
    return make_ref_interp(X, pe), make_ref_interp(X, ne), pe, ne


def _objective_for(target_v, refs, obj_cfg, weights):
    from src.fitting import window_shortfall

    f_pe, f_ne, pe, ne = refs
    target = compute_features(X, target_v, obj_cfg, with_peaks=True)
    ref_feat = compute_features(X, pe - ne, obj_cfg, v_grid=target.v_grid)

    def model_fn(p):
        _, _, full = reconstruct(p, f_pe, f_ne, X)
        return X, full

    obs = np.isfinite(target_v)
    lo, hi = float(X[obs].min()), float(X[obs].max())
    return make_objective(target, model_fn, weights, default_scales(ref_feat),
                          obj_cfg, lambda p: window_shortfall(p, lo, hi))


def test_identity(refs):
    """α=1, β=0 → reference와 완전히 일치해야 한다 (NaN 없이)."""
    f_pe, f_ne, pe, ne = refs
    r_pe, r_ne, full = reconstruct([1.0, 0.0, 1.0, 0.0], f_pe, f_ne, X)
    assert np.isfinite(full).all()
    np.testing.assert_allclose(r_pe, pe, atol=1e-12)
    np.testing.assert_allclose(r_ne, ne, atol=1e-12)
    np.testing.assert_allclose(full, pe - ne, atol=1e-12)


def test_identity_is_objective_minimum(refs, obj_cfg):
    """reference를 타깃으로 주면 p=[1,0,1,0]에서 J가 0이어야 한다."""
    f_pe, f_ne, pe, ne = refs
    J = _objective_for(pe - ne, refs, obj_cfg,
                       {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 1.0})
    assert J([1.0, 0.0, 1.0, 0.0]) == pytest.approx(0.0, abs=1e-9)
    assert J([0.95, -0.02, 1.05, 0.01]) > 1e-3      # 다른 해는 확실히 나쁨


@pytest.mark.parametrize("a_pe_true", [1.00, 1.10, 1.25])
@pytest.mark.parametrize("weights", [
    {"w_pocv": 1.0},
    {"w_pocv": 1.0, "w_dvdq": 1.0},
    {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 1.0},   # 34p — landscape가 가장 거침
], ids=["pocv", "pocv_dvdq", "pocv_dvdq_dqdv"])
def test_recovers_known_alpha(refs, obj_cfg, a_pe_true, weights):
    """알려진 α_PE로 만든 곡선에서 그 값을 복원한다 (목적함수 3종 모두)."""
    f_pe, f_ne, _, _ = refs
    p_true = [a_pe_true, 0.0, 1.05, 0.0]
    _, _, target = reconstruct(p_true, f_pe, f_ne, X)

    J = _objective_for(target, refs, obj_cfg, weights)
    res = fit(J, init=[1.0, 0.0, 1.0, 0.0], lb=[0.7, -0.4, 0.7, -0.4],
              ub=[1.8, 0.4, 1.8, 0.4], n_restarts=4, seed=1)

    # optimizer가 정답만큼은 좋은 해를 찾아야 한다. (J(정답)=0 이므로 사실상 J≈0)
    # 이 검사가 없으면 optimizer의 게으름이 '목적함수가 나쁘다'로 둔갑하고,
    # Phase 6의 목적함수 비교가 통째로 무의미해진다.
    assert res.J <= J(p_true) + 1e-4, f"정답 J={J(p_true):.3e} < 찾은 J={res.J:.3e}"
    # degeneracy 판정 허용오차(2%p)보다 훨씬 정확해야 한다
    assert res.p[0] == pytest.approx(a_pe_true, abs=0.005)
    assert res.p[2] == pytest.approx(1.05, abs=0.005)


def test_alpha_below_one_is_range_limited(refs, obj_cfg):
    """★ α<1은 reference 곡선의 범위 밖이라 원리적으로 복원이 편향된다.

    α<1이면 재구성 창(폭 1/α > 1)이 reference가 담고 있는 구간을 넘어선다.
    reference 곡선은 '기준 셀이 실제로 지나간 구간'만 담고 있으므로 그 바깥은
    정보가 없다 → 창 부족 벌점이 α를 1 쪽으로 밀어 올린다.

    즉 33p의 lb=1.00 을 풀어줘도 **reference 곡선의 범위가 사실상 같은 하한을
    만든다.** 이를 없애려면 full-range half-cell OCV(별도 반쪽셀 측정)가 필요하다.
    22p가 "provided half-cell OCV"를 쓴 이유가 이것이다.
    """
    f_pe, f_ne, _, _ = refs
    p_true = [0.90, 0.0, 1.05, 0.0]
    _, _, target = reconstruct(p_true, f_pe, f_ne, X)
    assert np.isnan(target).any(), "α<1이면 타깃 끝단이 정의되지 않아야 한다"

    J = _objective_for(target, refs, obj_cfg, {"w_pocv": 1.0, "w_dvdq": 1.0})
    res = fit(J, init=[1.0, 0.0, 1.0, 0.0], lb=[0.7, -0.4, 0.7, -0.4],
              ub=[1.8, 0.4, 1.8, 0.4], n_restarts=4, seed=1)
    assert res.p[0] >= p_true[0] - 1e-6      # 아래로는 안 내려감 (위쪽 편향)


def test_bound_active_flagged(refs, obj_cfg):
    """정답이 bound 밖이면 해가 bound에 붙고 플래그가 켜진다.

    ★ 33p 상황의 재현: 참값 α_PE=0.90 인데 lb=1.00 이면 α는 1.00에 붙는다.
      그 결과 LAM 추정이 강제로 '용량손실'과 같아진다.
    """
    f_pe, f_ne, _, _ = refs
    _, _, target = reconstruct([0.90, 0.0, 1.05, 0.0], f_pe, f_ne, X)
    J = _objective_for(target, refs, obj_cfg, {"w_pocv": 1.0, "w_dvdq": 1.0})

    res = fit(J, init=[1.03, -0.1, 1.08, -0.01], lb=[1.00, -0.30, 1.00, -0.15],
              ub=[1.10, 0.00, 1.10, 0.00], n_restarts=3, seed=2)
    assert res.any_bound_active
    assert res.bound_active[0]                      # α_PE가 하한에 붙음
    assert res.p[0] == pytest.approx(1.00, abs=1e-6)


def test_bound_active_helper():
    assert _bound_active([1.0, 0.0, 1.5, 0.2], [1.0, -0.3, 1.0, -0.3],
                         [1.1, 0.0, 1.8, 0.4]) == (True, True, False, False)


def test_alpha_relation_roundtrip():
    """α = (1−LAM)/r 와 역환산(21p)이 서로 정확히 반대여야 한다."""
    for lam_pe, lam_ne, lli, r in [(0.0, 0.0, 0.0, 1.0), (0.05, 0.15, 0.10, 0.86),
                                   (0.20, 0.00, 0.05, 0.78)]:
        p = modes_to_params(lam_pe, lam_ne, lli, r)
        got = to_degradation_modes(p, r, "paper")
        assert got["lam_pe"] == pytest.approx(lam_pe, abs=1e-12)
        assert got["lam_ne"] == pytest.approx(lam_ne, abs=1e-12)
        assert got["lli"] == pytest.approx(lli, abs=1e-12)


def test_alpha_one_means_lam_equals_capacity_loss():
    """★ α=1.00 ⟺ LAM = 용량손실. 33p 하한이 22p 패턴을 강제하는 이유."""
    for r in (0.95, 0.87, 0.80):
        modes = to_degradation_modes([1.0, 0.0, 1.0, 0.0], r, "paper")
        assert modes["lam_pe"] == pytest.approx(1 - r, abs=1e-12)
        assert modes["lam_ne"] == pytest.approx(1 - r, abs=1e-12)


def test_convention_code_ignores_capacity_ratio():
    """원본 코드 규약은 r을 반영하지 않는다 — 두 규약이 다름을 명시적으로 고정."""
    p = [1.05, -0.05, 1.02, 0.01]
    paper = to_degradation_modes(p, 0.85, "paper")
    code = to_degradation_modes(p, 0.85, "code")
    assert paper["lli"] != pytest.approx(code["lli"], abs=1e-6)
    with pytest.raises(ValueError):
        to_degradation_modes(p, 1.0, "nope")


def test_window_outside_is_penalized(refs, obj_cfg):
    """창을 크게 벗어나는 해는 벌점으로 확실히 나쁜 값이 된다."""
    f_pe, f_ne, pe, ne = refs
    J = _objective_for(pe - ne, refs, obj_cfg, {"w_pocv": 1.0})
    assert J([0.3, 0.9, 0.3, -0.9]) > 10.0


def test_dqdv_peak_weighting_applied(refs, obj_cfg):
    """피크 구간 가중치가 실제로 1보다 큰 값으로 설정된다."""
    f_pe, f_ne, pe, ne = refs
    feats = compute_features(X, pe - ne, obj_cfg, with_peaks=True)
    assert feats.peak_weight.max() == pytest.approx(
        obj_cfg["dqdv"]["peak_weight"], abs=1e-9)
    assert (feats.peak_weight == 1.0).any()


# ---------------------------------------------------------------- LLI 환산식

def test_derived_lli_requires_constants():
    with pytest.raises(ValueError, match="w_pe"):
        to_degradation_modes([1.1, 0, 1.05, 0], 0.9, "derived")


def test_derived_lli_differs_from_21p_by_beta_sign():
    """★ 21p 식은 유도식의 특수해가 아니다 — β 항의 부호가 반대다.

    유도식(w_PE=1, w_NE=0, κ=1) :  1 − r·(α_PE − β_PE + β_NE)
    21p 식                      :  1 − r·(α_PE + β_PE − β_NE)
    합성 데이터에서는 유도식 쪽 부호가 맞다 (|오차| 0.076 vs 0.128).
    원본 코드 주석의 "기존 부호가 반대였음"과도 같은 지점을 가리킨다.
    """
    p, r = [1.12, -0.04, 1.06, 0.02], 0.87
    got = to_degradation_modes(p, r, "derived", w_pe=1.0, w_ne=0.0, kappa=1.0)
    ref = to_degradation_modes(p, r, "paper")
    beta_term = r * (p[1] - p[3])
    assert got["lli"] == pytest.approx(ref["lli"] + 2 * beta_term, abs=1e-12)


def test_reference_inventory_weights_sum_to_one(cfg):
    from src.inventory import reference_inventory

    inv = reference_inventory(cfg, q_ref_ah=5.72)
    assert inv.w_pe + inv.w_ne == pytest.approx(1.0, abs=1e-12)
    assert 0 < inv.w_pe < inv.w_ne              # 이 셀은 재고 대부분이 음극에
    assert inv.kappa == pytest.approx(5.72 / inv.n_total_ah, abs=1e-12)


def test_derived_lli_recovers_truth_on_synthetic(cfg):
    """★ 참값 (LAM, LLI)로 만든 α·β에서 유도식이 LLI를 정확히 되돌린다."""
    from src.inventory import reference_inventory

    inv = reference_inventory(cfg, q_ref_ah=5.72)
    for lam_pe, lam_ne, lli, r in [(0.0, 0.0, 0.0, 1.0), (0.05, 0.15, 0.10, 0.86),
                                   (0.10, 0.05, 0.20, 0.75)]:
        a_pe, a_ne = (1 - lam_pe) / r, (1 - lam_ne) / r
        # 유도식을 만족하도록 β 차이를 역산 → 되돌렸을 때 lli가 나와야 함
        d_beta = ((1 - lli) / r - inv.w_pe * a_pe - inv.w_ne * a_ne) / inv.kappa
        got = to_degradation_modes([a_pe, 0.0, a_ne, d_beta], r, "derived",
                                   inv.w_pe, inv.w_ne, inv.kappa)
        assert got["lam_pe"] == pytest.approx(lam_pe, abs=1e-12)
        assert got["lam_ne"] == pytest.approx(lam_ne, abs=1e-12)
        assert got["lli"] == pytest.approx(lli, abs=1e-12)


# ---------------------------------------------------------------- 리뷰 반영 회귀

def test_halfcell_lli_identity_and_scale_invariance():
    """to_modes_halfcell: p=p_ini·(참조상태)면 LAM=LLI=0, 그리고 테이블 정규화
    상수가 α·β 전체에 곱해져도 결과 불변 (리뷰 F20 공백 보강)."""
    from src.fitting import to_modes_halfcell

    p_ini = [1.4652, -0.3954, 1.0289, -0.0255]     # 실측 ini
    got = to_modes_halfcell(p_ini, p_ini, r=1.0)
    assert got["lam_pe"] == pytest.approx(0.0, abs=1e-12)
    assert got["lam_ne"] == pytest.approx(0.0, abs=1e-12)
    assert got["lli"] == pytest.approx(0.0, abs=1e-12)

    # 열화 상태 하나 (r<1) — 스케일 c를 α·β 모두에 곱해도 LAM·LLI 불변
    p = [1.30, -0.30, 1.10, -0.10]
    r = 0.85
    base = to_modes_halfcell(p, p_ini, r)
    c = 1.7
    scaled = to_modes_halfcell([v * c for v in p], [v * c for v in p_ini], r)
    for k in ("lam_pe", "lam_ne", "lli"):
        assert scaled[k] == pytest.approx(base[k], rel=1e-12), k


def test_minimize_until_stable_returns_consistent_pair():
    """리뷰 F16: 반환된 p에서 J를 다시 평가하면 반환 J와 일치해야 한다."""
    from src.fitting import _minimize_until_stable

    def J(p):
        return float((p[0] - 0.3) ** 2 + (p[1] + 0.2) ** 2)

    x, f, ok, nfev = _minimize_until_stable(J, [0.9, 0.9],
                                            [(-1, 1), (-1, 1)], "Nelder-Mead")
    assert J(x) == pytest.approx(f, abs=1e-12)


def test_alpha_wall_flag_semantics():
    """리뷰 F1: α=1 소프트 벽은 box bound가 아니라 별도 플래그로 잡아야 한다."""
    from src.fitting import _bound_active

    # α=1.0은 expanded bound(0.7~1.8) 내부 → bound_active는 False여야 정상
    assert _bound_active([1.0, 0.0, 1.0, 0.0],
                         [0.7, -0.6, 0.7, -0.6], [1.8, 0.4, 1.8, 0.4]) == \
        (False, False, False, False)
    # 벽 감지는 fits 행의 alpha_wall_* 열이 담당 (fitting._fit_one에서 |α−1|<1e-3)


def test_dqdv_linear_voltage_gives_constant_dqdv(obj_cfg):
    """리뷰 F20: 해석적 검증 — V가 x에 선형이면 dQ/dV는 상수(=1/기울기)."""
    from src.objective import dqdv_on_grid

    x = np.linspace(0, 1, 300)
    v = 4.2 - 1.5 * x                       # dV/dQ = -1.5 → dQ/dV = -1/1.5
    v_grid = np.linspace(2.8, 4.1, 200)
    out = dqdv_on_grid(x, v, v_grid, window=21, polyorder=3)
    inner = out[np.isfinite(out)][10:-10]   # 경계 몇 점 제외
    np.testing.assert_allclose(inner, -1.0 / 1.5, rtol=5e-3)
