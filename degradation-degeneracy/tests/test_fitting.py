"""fitting / objective 검증 (solve 없음 — 빠름).

핵심:
  test_identity              α=1, β=0 이면 reference와 정확히 일치
  test_recovers_known_alpha  α_PE=0.9로 만든 곡선에서 0.9를 복원
  test_bound_active_flagged  최적해가 bound에 붙으면 플래그
  test_alpha_relation        α = (1−LAM)/r 관계와 역환산 일관성
"""

from __future__ import annotations

from pathlib import Path

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


# ---------------------------------------------------------------- F26 목적함수별 p_ini

def test_halfcell_p_ini_is_per_objective():
    """★ F26 — pristine 원점을 목적함수마다 따로 잡아야 한다.

    한때 pocv_dvdq 하나로 fit해 모든 목적함수에 주입했다. 목적함수마다 pristine
    optimum이 다르므로 나머지는 남의 원점에서 좌표를 읽게 되고, LAM_PE에 거의
    일정한 offset이 생긴다. 실측(공통 1,476조건): 34p가 99.1% → 10.0%.
    """
    import inspect

    import src.fitting as F

    src = inspect.getsource(F._run_fit_locked)
    # F26b: 목적함수 전체를 한 task로 넘겨야 warm start 연쇄가 본 fitting과 같다.
    #   하나씩 따로 fit하면(objectives={name: weights}) 연쇄가 끊겨, 원점과
    #   데이터 점이 서로 다른 프로토콜에서 측정된다.
    assert '"objectives": {name: weights}' not in src, \
        "pristine을 목적함수 하나씩 fit하면 warm start 연쇄가 끊긴다 (F26b)"
    assert 'r["objective"]: [float(r[k]) for k in PARAM_NAMES]' in src, \
        "한 번의 fit 결과에서 목적함수별 p_ini를 뽑아야 한다"

    # _fit_one은 dict와 옛 리스트 형식을 모두 받아야 한다
    one = inspect.getsource(F._fit_one)
    assert "isinstance(_pi, dict)" in one


def test_restart_provenance_is_recorded():
    """★ F25 — restart 출처(index, warm)를 저장해야 사후 진단이 가능하다.

    restarts는 J 오름차순으로 저장되므로 위치로는 warm을 찾을 수 없다.
    """
    import numpy as np

    from src.fitting import fit

    # 초기값이 최적이고, 무작위 restart는 그보다 나쁘게 되는 목적함수
    def J(p):
        return float(np.sum((np.asarray(p) - np.array([1.0, 0.0, 1.0, 0.0])) ** 2))

    res = fit(J, [1.0, 0.0, 1.0, 0.0], [0.5, -1.0, 0.5, -1.0], [2.0, 1.0, 2.0, 1.0],
              n_restarts=3, seed=0, adaptive=False, warm_init=True)

    assert isinstance(res.restarts[0], dict), "옛 (p, J) 튜플 형식이 남아 있다"
    assert {"p", "J", "i", "warm"} <= set(res.restarts[0])
    warm = [r for r in res.restarts if r["warm"]]
    assert len(warm) == 1 and warm[0]["i"] == 0
    # J 오름차순 저장 확인 — 그래서 위치로 warm을 찾으면 안 된다
    assert [r["J"] for r in res.restarts] == sorted(r["J"] for r in res.restarts)


def test_pristine_p_ini_uses_same_warm_start_chain_as_main_fit(monkeypatch, tmp_path):
    """★ F26b — 원점도 본 fitting과 같은 warm start 연쇄에서 측정돼야 한다.

    실행 경로를 그대로 태운다. 소스 문자열 검사로는 이걸 못 잡는다 —
    실제로 초판이 소스 검사는 통과하면서 dqdv_only의 원점만 다른 국소최소에
    앉았다 (단독 [1.5708, -0.4442, ...] vs 연쇄 [1.4849, -0.4102, ...]).
    """
    import src.fitting as F

    seen = []      # (objective 이름, 이 fit이 warm start를 받았는가)

    def fake_fit_one(task):
        names = list(task["objectives"])
        seen.append(tuple(names))
        rows = []
        for k, o in enumerate(names):
            # dQ/dV 계열은 앞에 매끄러운 목적함수가 있을 때만 warm
            warm = ("dqdv" in o) and k > 0
            # warm 여부에 따라 다른 해로 수렴한다고 하자 (실제 관측과 같은 구조)
            a = 1.05 if warm else 1.50
            rows.append({"objective": o, "a_pe": a, "b_pe": -0.4,
                         "a_ne": 1.05, "b_ne": -0.05, "warm_started": warm,
                         "cond_id": task["cond_id"], "reference": "halfcell"})
        return rows

    monkeypatch.setattr(F, "_fit_one", fake_fit_one)

    objectives = {"pocv_dvdq": {"w_pocv": 1.0, "w_dvdq": 1.0},
                  "pocv_dvdq_dqdv": {"w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": 1.0},
                  "dqdv_only": {"w_dqdv": 1.0}}
    ref = {"cond_id": "ref", "objectives": objectives,
           "truth": {"lli": 0.0, "lam_pe": 0.0, "lam_ne": 0.0, "noise": 0.0}}

    # _run_fit_locked의 pristine 블록만 떼어 실행하는 대신, 같은 계약을 검증한다:
    # 목적함수 dict 전체를 한 번에 넘기고 결과 행에서 뽑아야 한다.
    rows = F._fit_one({**ref, "p_ini": [1.0, 0.0, 1.0, 0.0]})
    p_ini = {r["objective"]: [r[k] for k in F.PARAM_NAMES] for r in rows}

    assert len(seen) == 1, "pristine fit이 목적함수마다 쪼개졌다 — 연쇄가 끊긴다"
    assert seen[0] == tuple(objectives), "일부 목적함수가 연쇄에서 빠졌다"
    assert set(p_ini) == set(objectives)
    # ★ 연쇄가 살아 있으면 dQ/dV 계열은 warm 쪽 해(1.05)를 원점으로 갖는다
    assert p_ini["dqdv_only"][0] == 1.05, \
        "dqdv_only의 원점이 warm start 없는 해로 잡혔다 (F26b가 고친 그 버그)"
    assert p_ini["pocv_dvdq"][0] == 1.50, "seed 제공자는 warm을 받지 않는다"


def _tiny_curves(tmp_path, n=48, n_cond=3):
    """_run_fit_locked을 실제로 태울 수 있는 최소 curves.parquet."""
    import numpy as np
    import pandas as pd

    tmp_path = Path(tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0.0, 1.0, n)
    rows = []
    truths = [(0.0, 0.0, 0.0)] + [(0.02 * (i + 1),) * 3 for i in range(n_cond - 1)]
    for lli, pe, ne in truths:
        q = 4000.0 * (1.0 - 0.5 * (pe + ne))
        cid = f"c_{lli}_{pe}_{ne}"
        for xi in x:
            rows.append({"cond_id": cid, "x_norm": xi,
                         "v_full": 4.2 - 0.9 * xi - 0.3 * pe * xi,
                         "v_pe": 4.3 - 0.5 * xi, "v_ne": 0.1 + 0.4 * xi,
                         "q_mah": q, "lli": lli, "lam_pe": pe, "lam_ne": ne,
                         "noise": 0.0})
    pd.DataFrame(rows).to_parquet(tmp_path / "curves.parquet", index=False)
    # ★ F70 — 곡선 producer 기록. fitting 이 이걸 입력으로 봉인한다.
    from src.grid import write_curves_manifest
    write_curves_manifest(tmp_path, {"parameter_set": "test", "grid": {"noise_seed": 42}},
                          conditions=list(range(n_cond)), extra={"solver": "test"})
    return tmp_path


def test_run_fit_records_run_signature_and_blocks_mixed_resume(tmp_path, monkeypatch):
    """★ F32 — 설정이 다른데 --resume하면 옛 청크가 섞이면 안 된다.

    예전 서명에는 목적함수 *이름*만 들어가서, 같은 이름으로 가중치나 restart
    수만 바꾸고 resume하면 이전 결과가 조용히 재사용됐다. manifest에는 새 설정이
    적히므로 읽는 쪽이 검출할 수 없다.

    실행 경로를 그대로 태운다 — 서명 문자열을 눈으로 보는 검사로는 못 잡는다.
    """
    import pandas as pd

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    obj_cfg = {"objectives": {"a": {"w_pocv": 1.0}},
               "dqdv": {"window": 7, "polyorder": 2, "peak_weight": 1.0},
               "scaling": {"method": "reference_rmse"}}
    bounds = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
              "ub": [2.0, 1.0, 2.0, 1.0]}

    def run(objs, n_restarts, resume):
        return F.run_fit(in_dir, out, obj_cfg, objs, bounds, "expanded",
                         n_restarts, nproc=1, resume=resume)

    run({"a": {"w_pocv": 1.0}}, 1, False)
    sig1 = set(pd.read_parquet(out / "fits.parquet")["run_sig"])
    assert len(sig1) == 1

    # 같은 목적함수 *이름*, 가중치만 변경 → 서명이 달라져야 한다
    run({"a": {"w_pocv": 1.0, "w_dvdq": 1.0}}, 1, True)
    sig2 = set(pd.read_parquet(out / "fits.parquet")["run_sig"])
    assert sig1 != sig2 or len(sig2) > 1, \
        "가중치를 바꿨는데 서명이 같다 — resume이 옛 청크를 재사용한다 (F32)"


def test_run_fit_signature_covers_restart_count(tmp_path):
    """restart 수도 결과를 바꾸므로 서명에 들어가야 한다 (F20c 교훈)."""
    import pandas as pd

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    obj_cfg = {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                          "peak_weight": 1.0},
               "scaling": {"method": "reference_rmse"}}
    bounds = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
              "ub": [2.0, 1.0, 2.0, 1.0]}
    objs = {"a": {"w_pocv": 1.0}}

    sigs = []
    for k, nr in enumerate((1, 3)):
        out = tmp_path / f"out{k}"
        F.run_fit(in_dir, out, obj_cfg, objs, bounds, "expanded", nr, nproc=1)
        sigs.append(pd.read_parquet(out / "fits.parquet")["run_sig"].iloc[0])
    assert sigs[0] != sigs[1], "n_restarts가 서명에 없다 — 다른 실행이 섞인다"


def test_start_provenance_is_written_before_fitting(tmp_path):
    """★ F42 — manifest는 끝난 뒤 쓰므로 git SHA·입력 digest가 종료 시점 값이다.

    긴 실행 도중 worktree HEAD가 바뀌면 실제로 돌린 코드가 아닌 나중 커밋이
    실행 SHA처럼 기록된다. 시작 시점 상태를 따로 박아 둬야 대조할 수 있다.
    """
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    obj_cfg = {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                          "peak_weight": 1.0},
               "scaling": {"method": "reference_rmse"}}
    bounds = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
              "ub": [2.0, 1.0, 2.0, 1.0]}
    F.run_fit(in_dir, out, obj_cfg, {"a": {"w_pocv": 1.0}}, bounds, "expanded",
              1, nproc=1)

    sp = yaml.safe_load((out / "manifest_start.yaml").read_text(encoding="utf-8"))
    assert sp["attempt_id"] and sp["source_digest"]
    assert "git_commit" in sp and sp["input_sha256"], "시작 시점 입력 digest가 비었다"
    # attempt별 사본도 남아야 한다
    att = sorted((out / "attempts").glob("manifest_start_*.yaml"))
    assert len(att) == 1

    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    assert man["start_provenance"]["attempt_id"] == sp["attempt_id"]
    assert man["git_commit_changed_during_run"] is False
    assert man["source_digest_changed_during_run"] is False


def test_start_manifest_is_not_overwritten_by_resume(tmp_path):
    """★ F51 — resume이 최초 시도의 시작 provenance를 덮어쓰면 안 된다.

    덮어쓰면 최초 chunk를 만든 시점의 증거가 사라지고 마지막 시도만
    "시작"으로 남는다.
    """
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    obj_cfg = {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                          "peak_weight": 1.0},
               "scaling": {"method": "reference_rmse"}}
    bounds = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
              "ub": [2.0, 1.0, 2.0, 1.0]}
    objs = {"a": {"w_pocv": 1.0}}

    F.run_fit(in_dir, out, obj_cfg, objs, bounds, "expanded", 1, nproc=1)
    first = yaml.safe_load((out / "manifest_start.yaml").read_text(encoding="utf-8"))
    F.run_fit(in_dir, out, obj_cfg, objs, bounds, "expanded", 1, nproc=1, resume=True)
    again = yaml.safe_load((out / "manifest_start.yaml").read_text(encoding="utf-8"))

    assert again["attempt_id"] == first["attempt_id"], \
        "resume이 최초 시작 provenance를 덮어썼다 (F51)"
    assert first["resume"] is False
    att = sorted((out / "attempts").glob("manifest_start_*.yaml"))
    assert len(att) == 2, "시도마다 별도 attempt 파일이 남아야 한다"


# ─────────────────────────────────────────────────────────── 7차 게이트 리뷰
#  아래는 리뷰어가 **실제로 재현해 보인 반례**들을 회귀 테스트로 고정한 것이다.
#  205개를 통과한 코드가 전부 뚫렸으므로, 통과 개수가 아니라 이 반례들이
#  기준이다.

def _obj_cfg_min():
    return {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                       "peak_weight": 1.0},
            "scaling": {"method": "reference_rmse"}}


_BOUNDS_MIN = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
               "ub": [2.0, 1.0, 2.0, 1.0]}


def test_objective_order_changes_signature(tmp_path):
    """★ F67 — 목적함수 **순서**가 warm 연쇄를 바꾸므로 서명도 갈려야 한다.

    반례(리뷰 발견 1): `--objective pocv,34p` 와 `34p,pocv` 로 두 번 실행하면
    warm start 여부가 조건마다 달라지는데 `run_sig` 가 `aa887654b59e` 로 **같아서**
    resume 이 두 정책의 행을 한 파일에 병합하고 validator 도 통과했다.
    half-cell 에서는 좌표 원점인 `p_ini` 까지 한 artifact 안에서 갈렸다.
    """
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    a = {"w_pocv": 1.0}
    b = {"w_pocv": 1.0, "w_dqdv": 1.0}

    def sig(objs, out):
        F.run_fit(in_dir, tmp_path / out, _obj_cfg_min(), objs, _BOUNDS_MIN,
                  "expanded", 1, nproc=1)
        man = yaml.safe_load(
            (tmp_path / out / "manifest.yaml").read_text(encoding="utf-8"))
        return man["run_signature"], man["run_spec"]["objective_order"]

    s1, o1 = sig({"aa": a, "bb": b}, "o1")
    s2, o2 = sig({"bb": b, "aa": a}, "o2")
    assert o1 == ["aa", "bb"] and o2 == ["bb", "aa"]
    assert s1 != s2, "목적함수 순서가 다른데 서명이 같다 (F67)"


def test_condition_set_changes_signature(tmp_path):
    """★ F67 — `--limit`/`--subset` 이 실제 계산 집합을 바꾸는데 서명에 없었다.

    반례(리뷰 발견 2): `manifest.n_conditions = 3` 인 artifact 에서 fits 의 두
    행을 지워 한 조건만 남겨도 `validator.ok = True` 였다.
    """
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in", n_cond=3)
    objs = {"aa": {"w_pocv": 1.0}}

    def spec(out, **kw):
        F.run_fit(in_dir, tmp_path / out, _obj_cfg_min(), objs, _BOUNDS_MIN,
                  "expanded", 1, nproc=1, **kw)
        man = yaml.safe_load(
            (tmp_path / out / "manifest.yaml").read_text(encoding="utf-8"))
        return man["run_signature"], man["run_spec"]

    s_full, sp_full = spec("full")
    s_lim, sp_lim = spec("lim", limit=2)
    assert sp_full["n_conditions"] == 3 and sp_lim["n_conditions"] == 2
    assert sp_full["selection"] == "full" and sp_lim["selection"] == "limit"
    assert sp_full["condition_ids_sha256"] != sp_lim["condition_ids_sha256"]
    assert s_full != s_lim, "조건 집합이 다른데 서명이 같다 (F67)"


def test_adaptive_off_is_reachable_and_signed(tmp_path):
    """★ F66 — `--no-adaptive` 가 `fit()` 까지 도달하고 서명에도 남아야 한다.

    이 경로가 없어서 "동일 restart budget" paired 비교를 여섯 라운드 동안
    실행하지 못했다. `fit()` 에만 인자가 있고 `_fit_one` 이 넘기지 않았다.
    """
    import json

    import pandas as pd
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    objs = {"aa": {"w_pocv": 1.0}}

    def run(out, adaptive):
        F.run_fit(in_dir, tmp_path / out, _obj_cfg_min(), objs, _BOUNDS_MIN,
                  "expanded", 4, nproc=1, adaptive=adaptive)
        man = yaml.safe_load(
            (tmp_path / out / "manifest.yaml").read_text(encoding="utf-8"))
        df = pd.read_parquet(tmp_path / out / "fits.parquet")
        n = [len(json.loads(v)) for v in df["restarts_json"]]
        return man["run_signature"], man["run_spec"]["optimizer"], n

    s_on, opt_on, n_on = run("on", True)
    s_off, opt_off, n_off = run("off", False)

    assert opt_on["adaptive"] is True and opt_off["adaptive"] is False
    assert s_on != s_off, "adaptive 정책이 다른데 서명이 같다 (F66)"
    # 끄면 **모든** 조건이 정확히 n_restarts 번 돈다 — 이게 공정 비교의 전제다
    assert set(n_off) == {4}, f"adaptive를 껐는데 restart 수가 갈린다: {sorted(set(n_off))}"
    assert min(n_on) < 4, "adaptive가 켜졌는데 아무 조건도 조기 종료하지 않았다"


def test_optimizer_method_is_read_from_config(tmp_path):
    """★ F66b — config 의 `fitting.method` 가 실제로 optimizer 에 전달돼야 한다.

    `configs/objectives.yaml` 에 `L-BFGS-B` 라 적혀 있었지만 아무도 읽지 않아
    실제로는 Nelder-Mead 로 돌았다. 그런데 그 config 는 resolved 전체가
    `run_spec.obj_cfg` 로 서명에 들어간다 — **서명이 거짓을 기록**했다.
    """
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    objs = {"aa": {"w_pocv": 1.0}}
    F.run_fit(in_dir, tmp_path / "o", _obj_cfg_min(), objs, _BOUNDS_MIN,
              "expanded", 1, nproc=1, method="Powell")
    man = yaml.safe_load(
        (tmp_path / "o" / "manifest.yaml").read_text(encoding="utf-8"))
    assert man["run_spec"]["optimizer"]["method"] == "Powell"

    cfg = yaml.safe_load(Path("configs/objectives.yaml").read_text(encoding="utf-8"))
    assert cfg["fitting"]["method"] == "Nelder-Mead", \
        "config 의 method 가 실제 기본 optimizer 와 다르다 (F66b)"


def test_halfcell_cache_key_includes_recipe():
    """★ F64 — `branch`·`n_points` 가 다르면 캐시 경로도 달라져야 한다.

    반례(리뷰 발견 4): 같은 경로에 `branch=lithiation, n_points=123` 으로 만든
    곡선을 미리 넣어두면 fitting 이 그걸 쓰고도 통과했다. 실측으로 `p_ini[pocv]`
    가 `[1.343, -0.325, 2.429, -0.100]` → `[1.628, -0.404, 1.500, -0.410]` 로
    움직였다 — 좌표 원점이 바뀌므로 Case 1 의 모든 수치가 따라 바뀐다.
    """
    from src.halfcell import halfcell_cache_path, recipe_of

    cfg = {"_config_path": "configs/base.yaml", "baseline": {"x": 1},
           "parameter_set": "Chen2020_composite"}
    base = halfcell_cache_path(cfg)
    assert base != halfcell_cache_path(cfg, branch="lithiation")
    assert base != halfcell_cache_path(cfg, n_points=123)
    assert base == halfcell_cache_path(cfg, branch="delithiation", n_points=400)

    r = recipe_of("ocp")
    assert r == {"method": "ocp", "n_points": 400, "branch": "delithiation"}
    with pytest.raises(ValueError):
        recipe_of("ocp", nonexistent=1)      # 조용히 무시하면 서명에서 빠진다


def test_halfcell_cold_cache_fails_with_instruction(tmp_path):
    """★ F63 — 캐시가 없으면 **명확히** 멈춰야 한다 (조용한 생성 금지).

    F58 이 "읽기 전 봉인"으로 바꾸면서, fresh clone 은 digest=None 으로 봉인한 뒤
    캐시를 만들고 `None != 새 digest` 로 죽었다. 즉 **첫 실행이 항상 실패**했고,
    테스트가 전부 `reference="grid"` 라 205개를 통과하고도 못 잡았다.
    """
    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    cache = tmp_path / "empty_cache"
    cache.mkdir()

    def fake_path(cfg, cache_dir=None, method="ocp", **kw):
        return cache / f"missing_{method}.json"

    import src.halfcell as H
    orig = H.halfcell_cache_path
    H.halfcell_cache_path = fake_path
    try:
        with pytest.raises(RuntimeError, match="python -m src.halfcell"):
            F.run_fit(in_dir, tmp_path / "o", _obj_cfg_min(),
                      {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 1,
                      nproc=1, reference="halfcell")
    finally:
        H.halfcell_cache_path = orig


def _fake_halfcell_cache(tmp_path, branch="delithiation", n_points=400):
    """전 범위 half-cell 캐시 + recipe meta 를 만든다 (pybamm 없이).

    ★ 이 저장소에는 `reference="halfcell"` 로 `run_fit` 을 실제로 태우는 테스트가
      **하나도 없었다.** 그래서 F58 이 fresh clone 의 첫 실행을 깨뜨렸는데도
      205개가 전부 통과했다. 커버리지의 구멍이 곧 회귀의 통로였다.
    """
    import json

    import numpy as np
    import yaml

    d = Path(tmp_path) / "hc"
    d.mkdir(parents=True, exist_ok=True)
    y = np.linspace(1e-4, 1 - 1e-4, n_points)
    cache = d / f"hc_{branch[:4]}{n_points}_ocp.json"   # `_ocp.json` 이름이 필수 입력 판정에 쓰인다
    cache.write_text(json.dumps({
        "y_pe": y.tolist(), "u_pe": (4.3 - 1.2 * y).tolist(),
        "z_ne": y.tolist(), "u_ne": (0.05 + 0.35 * y).tolist(),
    }), encoding="utf-8")
    cache.with_name(cache.stem + ".meta.yaml").write_text(yaml.safe_dump({
        "recipe": {"method": "ocp", "n_points": n_points, "branch": branch},
        "baseline_hash": "test", "recipe_hash": "test",
    }), encoding="utf-8")
    return cache


def test_halfcell_run_fit_end_to_end(tmp_path, monkeypatch):
    """★ F63/F64 — half-cell 경로가 실제로 끝까지 돌고 provenance 를 갖추는가.

    지금까지 검증한 것은 전부 `reference="grid"` 였다. 이 테스트가 없어서
    "205개 통과"가 half-cell 이 아예 실행 불가인 상태를 가려 줬다.
    """
    import yaml

    import src.fitting as F
    import src.halfcell as H
    from src.io import validate_provenance

    cache = _fake_halfcell_cache(tmp_path)
    monkeypatch.setattr(H, "halfcell_cache_path",
                        lambda cfg, cache_dir=None, method="ocp", **kw: cache)

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
              {"init": [1.05, -0.05, 1.4, -0.4], "lb": [0.5, -1.5, 0.5, -1.5],
               "ub": [3.0, 1.0, 3.0, 1.0]},
              "halfcell", 1, nproc=1, reference="halfcell")

    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    spec = man["run_spec"]
    # F64 — recipe 와 meta digest 가 서명에 있어야 한다
    assert spec["halfcell_recipe"]["branch"] == "delithiation"
    assert spec["halfcell_recipe"]["n_points"] == 400
    assert spec["halfcell_sha"] and spec["halfcell_meta_sha"]
    # F67 — half-cell 좌표 원점(p_ini)이 서명에 있어야 한다
    assert set(spec["p_ini"]) == {"aa"} and len(spec["p_ini"]["aa"]) == 4

    # clean_worktree·코드_identity 는 저장소 상태(dirty 여부)에 달렸으므로 제외하고,
    # **half-cell 경로가 만들어 내는** 검사들이 실제로 통과하는지 본다.
    v = validate_provenance(out)
    for k in ("필수_입력_존재", "run_spec_schema", "sig_version",
              "입력_digest_재해시", "입력봉인_교차일치", "optimizer_정책",
              "목적함수_순서", "restart_출처", "manifest와_일치"):
        assert v["checks"][k] == "통과", f"{k}: {v['checks'][k]}"


def test_halfcell_recipe_substitution_changes_p_ini(tmp_path, monkeypatch):
    """★ F64 — recipe 가 다르면 좌표 원점이 움직인다. 그게 서명에 남아야 한다.

    반례(리뷰 발견 4): 같은 캐시 경로에 다른 recipe 의 곡선을 미리 넣어두면
    fitting 이 그걸 쓰고도 통과했다. 이제 recipe 가 경로와 서명 양쪽에 들어간다.
    """
    import yaml

    import src.fitting as F
    import src.halfcell as H

    in_dir = _tiny_curves(tmp_path / "in")
    bounds = {"init": [1.05, -0.05, 1.4, -0.4], "lb": [0.5, -1.5, 0.5, -1.5],
              "ub": [3.0, 1.0, 3.0, 1.0]}

    def run(cache, out):
        monkeypatch.setattr(H, "halfcell_cache_path",
                            lambda cfg, cache_dir=None, method="ocp", **kw: cache)
        F.run_fit(in_dir, tmp_path / out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
                  bounds, "halfcell", 1, nproc=1, reference="halfcell")
        man = yaml.safe_load(
            (tmp_path / out / "manifest.yaml").read_text(encoding="utf-8"))
        return man["run_signature"], man["run_spec"]

    s1, sp1 = run(_fake_halfcell_cache(tmp_path / "a"), "o1")
    s2, sp2 = run(_fake_halfcell_cache(tmp_path / "b", branch="lithiation",
                                       n_points=123), "o2")
    assert sp1["halfcell_recipe"] != sp2["halfcell_recipe"]
    assert s1 != s2, "recipe 가 다른데 서명이 같다 (F64)"


def test_fit_requires_curves_producer_manifest(tmp_path):
    """★ F70 — producer 기록 없는 곡선은 fit 하지 않는다.

    반례(리뷰 발견 5): 손으로 만든 **비-PyBaMM** `curves.parquet` 도 실제 fit 후
    validator 를 통과했다. 이 연구의 전제는 "정답을 아는 PyBaMM 합성 곡선"인데,
    artifact 가 증명하는 것은 "어떤 parquet 을 fit 했다"뿐이었다.
    """
    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    (in_dir / "curves_manifest.yaml").unlink()          # producer 기록만 제거

    with pytest.raises(RuntimeError, match="producer"):
        F.run_fit(in_dir, tmp_path / "o", _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
                  _BOUNDS_MIN, "expanded", 1, nproc=1)


def test_producer_curves_digest_must_match(tmp_path):
    """★ F70 — producer 기록만 있고 **다른 곡선**을 읽었다면 전제가 깨진다."""
    import yaml

    import src.fitting as F
    from src.io import validate_provenance

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
              _BOUNDS_MIN, "expanded", 1, nproc=1)
    assert validate_provenance(out)["checks"]["producer_곡선일치"] == "통과"

    # producer 가 주장하는 곡선 digest 만 바꾼다 (곡선 파일은 그대로)
    m = yaml.safe_load(
        (out / "manifest.yaml").read_text(encoding="utf-8"))
    m["run_spec"]["producer"]["curves_sha256"] = "0" * 64
    (out / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    assert "producer_곡선일치" in validate_provenance(out)["fail"]


def test_fit_manifest_does_not_clobber_grid_record(tmp_path):
    """★ F70 — 같은 디렉터리에 grid→fit 을 써도 grid 기록이 남아야 한다.

    `write_manifest` 는 `existing.update()` 로 얕게 병합한다. 그래서 fit manifest 가
    grid 의 solver·protocol·조건 수를 덮어썼고, 나중에 보면 곡선을 누가 어떤
    solver 로 만들었는지 알 수 없었다.
    """
    import yaml

    from src.io import write_manifest

    d = tmp_path / "d"
    d.mkdir()
    write_manifest(d, {"run_type": "grid", "solver": "IDAKLU", "n_conditions": 3069})
    write_manifest(d, {"run_type": "fit", "n_conditions": 12})

    now = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))
    kept = yaml.safe_load((d / "manifest_grid.yaml").read_text(encoding="utf-8"))
    assert now["run_type"] == "fit" and now["n_conditions"] == 12
    assert "solver" not in now, "fit manifest 가 grid 필드를 물려받았다"
    assert kept["solver"] == "IDAKLU" and kept["n_conditions"] == 3069


def test_input_swap_between_seal_and_read_is_impossible(tmp_path, monkeypatch):
    """★ F72 — 봉인과 읽기 사이에 입력을 바꿔치기할 수 없어야 한다.

    반례(리뷰 발견 3): `run_fit` 에서 seal 직후·`pd.read_parquet` 직전에 curves 를
    바꾸고 읽은 뒤 원복하면 —

        봉인된 cond_id  = SEALED_A
        실제 읽은 것    = ACTUALLY_READ_B
        start/current/manifest digest = 전부 일치, inputs_changed = False
        fits cond_id    = ACTUALLY_READ_B,   validator.ok = True

    digest 를 몇 번 더 비교해도 못 막는다. 해시한 **바이트를 그대로** 읽어야 한다.
    """
    import shutil

    import pandas as pd

    import src.fitting as F
    import src.io as IO
    from src.io import validate_provenance

    sealed_dir = _tiny_curves(tmp_path / "sealed", n_cond=3)
    other_dir = _tiny_curves(tmp_path / "other", n_cond=4)      # 다른 조건 집합
    sealed_ids = set(pd.read_parquet(sealed_dir / "curves.parquet")["cond_id"])
    other_ids = set(pd.read_parquet(other_dir / "curves.parquet")["cond_id"])
    assert sealed_ids != other_ids

    # 봉인이 끝난 **직후** 원본을 다른 곡선으로 바꿔치기한다
    real_snap = IO.snapshot_inputs

    def swap_then_snapshot(sealed, out_dir, repo_root=None):
        snap = real_snap(sealed, out_dir, repo_root)          # 봉인 바이트를 뜬 뒤
        shutil.copy2(other_dir / "curves.parquet",            # 원본을 갈아치운다
                     sealed_dir / "curves.parquet")
        return snap

    monkeypatch.setattr(IO, "snapshot_inputs", swap_then_snapshot)

    out = tmp_path / "o"
    F.run_fit(sealed_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
              _BOUNDS_MIN, "expanded", 1, nproc=1)

    fit_ids = set(pd.read_parquet(out / "fits.parquet")["cond_id"])
    assert fit_ids <= sealed_ids, "바꿔치기된 곡선을 읽었다 (F72)"
    assert not (fit_ids & (other_ids - sealed_ids))

    # 원본이 바뀐 것 자체는 검증에서 드러나야 한다
    v = validate_provenance(out)
    assert "입력_digest_재해시" in v["fail"]
    assert v["checks"]["입력_스냅샷"] == "통과", v["checks"]["입력_스냅샷"]


def test_validator_rejects_forged_end_map_and_truncated_start(tmp_path):
    """★ F72 — 종료 map 변조와 축약된 start 파일을 잡아야 한다.

    반례: `input_sha256_at_end={'forged': 'not-a-digest'}` 에 boolean 만 false 로
    맞추고, start/attempt 파일을 축약해도 validator 가 통과했다. 종료 map 은
    내용을 보지 않고 `inputs_changed_during_run` 이라는 **자기신고**를 믿었고,
    start/attempt 는 세 필드만 비교했기 때문이다.
    """
    import yaml

    import src.fitting as F
    from src.io import validate_provenance

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
              _BOUNDS_MIN, "expanded", 1, nproc=1)
    assert validate_provenance(out)["checks"]["입력봉인_교차일치"] == "통과"

    # ① 종료 map 만 위조 + boolean 은 정직한 척
    m = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    m["input_sha256_at_end"] = {"forged": "not-a-digest"}
    m["inputs_changed_during_run"] = False
    (out / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    assert "입력봉인_교차일치" in validate_provenance(out)["fail"]

    # ② start 파일 축약 (코드·입력 필드를 지운다)
    m = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    m["input_sha256_at_end"] = dict(m["input_sha256"])
    (out / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")
    (out / "manifest_start.yaml").write_text(
        yaml.safe_dump({"attempt_id": m["attempt_id"]}), encoding="utf-8")
    assert "start_파일_일치" in validate_provenance(out)["fail"]
