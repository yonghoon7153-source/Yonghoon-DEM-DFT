"""savgol 행렬 캐시가 scipy와 **같은 값**을 주는지 (F22).

이건 속도 최적화지 근사가 아니다. 값이 달라지면 지금까지의 모든 결과와
비교가 깨지므로, 기계 정밀도로 고정한다.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.signal import savgol_filter

import src.objective as O


@pytest.fixture(autouse=True)
def _clear_cache():
    O._SMOOTH_KERNEL.clear()
    yield
    O._SMOOTH_KERNEL.clear()


@pytest.mark.parametrize("n", [23, 51, 100, 298, 299, 300])
@pytest.mark.parametrize("window,polyorder", [(21, 3), (11, 2), (31, 4)])
def test_matrix_smoothing_matches_scipy(n, window, polyorder):
    rng = np.random.default_rng(n * 7 + window)
    y = np.cumsum(rng.normal(size=n))

    got = O._smooth(y, window, polyorder)
    # _smooth의 창 보정 규칙을 그대로 재현해 scipy 기준값을 만든다
    w = min(window, n if n % 2 else n - 1)
    if w % 2 == 0:
        w -= 1
    want = y if w <= polyorder + 1 else savgol_filter(y, w, polyorder)

    assert got.shape == want.shape
    scale = max(float(np.ptp(want)), 1.0)
    assert np.max(np.abs(got - want)) < 1e-11 * scale


def test_kernel_is_shared_across_lengths():
    """★ 가장자리 연산자는 n에 의존하지 않는다 — 길이가 달라도 캐시는 하나."""
    rng = np.random.default_rng(0)
    for n in (120, 200, 299, 300):
        O._smooth(np.cumsum(rng.normal(size=n)), 21, 3)
    assert len(O._SMOOTH_KERNEL) == 1, "길이마다 커널을 새로 만들었다"
    O._smooth(np.cumsum(rng.normal(size=200)), 11, 2)
    assert len(O._SMOOTH_KERNEL) == 2, "(창,차수)가 다르면 별도 커널이어야 한다"


def test_kernel_memory_is_small():
    """조밀 n×n(698 KB)이 아니라 띠(수 KB)여야 한다 — 대역폭이 병목이므로."""
    O._smooth(np.cumsum(np.random.default_rng(0).normal(size=299)), 21, 3)
    coef, top, bot, _ = next(iter(O._SMOOTH_KERNEL.values()))
    total = coef.nbytes + top.nbytes + bot.nbytes
    assert total < 20_000, f"커널이 {total}바이트 — 띠 구조가 깨졌다"


def test_linearity_holds():
    """선형 연산자이므로 M(a·y1 + y2) == a·M(y1) + M(y2) 여야 한다."""
    rng = np.random.default_rng(3)
    y1, y2 = rng.normal(size=200), rng.normal(size=200)
    lhs = O._smooth(2.5 * y1 + y2, 21, 3)
    rhs = 2.5 * O._smooth(y1, 21, 3) + O._smooth(y2, 21, 3)
    assert np.allclose(lhs, rhs, atol=1e-12)


def test_can_be_disabled_and_matches_scipy(monkeypatch):
    """캐시를 끄면 scipy 경로로 가고 값은 그대로여야 한다 (동등성 검증용 스위치)."""
    monkeypatch.setattr(O, "_SMOOTH_CACHE_ENABLED", False)
    y = np.cumsum(np.random.default_rng(1).normal(size=150))
    got = O._smooth(y, 21, 3)
    assert not O._SMOOTH_KERNEL, "꺼져 있는데 커널을 만들었다"
    assert np.allclose(got, savgol_filter(y, 21, 3), atol=1e-12)


def test_short_signal_returns_unchanged():
    y = np.arange(4.0)
    assert np.array_equal(O._smooth(y, 21, 3), y)


@pytest.mark.parametrize("n", [60, 299])
def test_features_identical_to_scipy_path(n, monkeypatch):
    """★ 실제 사용 경로(compute_features)에서 두 구현이 같은 값을 내는가."""
    cfg = {"dqdv": {"window": 21, "polyorder": 3}}
    x = np.linspace(0, 1, n)
    v = 4.2 - 1.5 * x + 0.05 * np.sin(18 * x)

    fast = O.compute_features(x, v, cfg, with_peaks=True)
    O._SMOOTH_KERNEL.clear()
    monkeypatch.setattr(O, "_SMOOTH_CACHE_ENABLED", False)   # scipy 경로 강제
    slow = O.compute_features(x, v, cfg, with_peaks=True)

    for name in ("dvdq", "dqdv"):
        a, b = getattr(fast, name), getattr(slow, name)
        m = np.isfinite(a) & np.isfinite(b)
        assert np.array_equal(np.isfinite(a), np.isfinite(b)), f"{name} NaN 위치가 다름"
        assert np.max(np.abs(a[m] - b[m])) < 1e-9 * max(float(np.ptp(b[m])), 1.0)


# ── OCP 모델 오차 민감도 (한계 4) ──────────────────────────────────────────
#
# ★ 이 연구의 결론 전체가 "half-cell OCP 함수가 정확하다" 는 가정 위에 있다.
#   합성 truth 를 만든 바로 그 OCP 로 fit 했기 때문이다. 실측에서는 우리 모델과
#   실제 전극이 어긋나고, 어긋난 만큼 half-cell 기준의 우위가 깎인다. 그래서
#   기준 곡선에만 계통 왜곡을 넣을 수 있어야 한다 — truth 는 그대로 두고.
#
#   왜곡을 `ocp` recipe 에 끼우면 기존 v4 half-cell 묶음의 recipe_hash 가 바뀌어
#   검증이 깨진다. **별도 method `ocpbias`** 로 둬서 기존 identity 를 건드리지
#   않는다.

def _base_cfg():
    from src.config import load_config
    return load_config("configs/base.yaml")


def test_ocpbias_is_a_separate_method_leaving_ocp_untouched():
    """★ 기존 `ocp` recipe 는 한 글자도 안 바뀌어야 한다 (v4 묶음 보호)."""
    from src.halfcell import RECIPE_DEFAULTS

    assert RECIPE_DEFAULTS["ocp"] == {"n_points": 400, "branch": "delithiation"}
    assert "ocpbias" in RECIPE_DEFAULTS
    for k in ("pe_offset_mv", "ne_offset_mv", "pe_stretch", "ne_stretch"):
        assert k in RECIPE_DEFAULTS["ocpbias"], k


def test_ocpbias_with_zero_perturbation_equals_ocp():
    """★ 왜곡 0 이면 `ocp` 와 **배열이 같아야** 한다 (엄밀한 일반화)."""
    import numpy as np
    from src.halfcell import compute_halfcell_from_ocp

    cfg = _base_cfg()
    a = compute_halfcell_from_ocp(cfg, n_points=64)
    b = compute_halfcell_from_ocp(cfg, n_points=64, pe_offset_mv=0.0,
                                  ne_offset_mv=0.0, pe_stretch=1.0,
                                  ne_stretch=1.0)
    for k in ("y_pe", "u_pe", "z_ne", "u_ne"):
        np.testing.assert_allclose(getattr(a, k), getattr(b, k), rtol=0, atol=0)


def test_ocpbias_offset_shifts_voltage_and_stretch_shifts_stoichiometry():
    """★ 두 왜곡이 각각 의도한 축을 움직여야 한다."""
    import numpy as np
    from src.halfcell import compute_halfcell_from_ocp

    cfg = _base_cfg()
    a = compute_halfcell_from_ocp(cfg, n_points=64)
    off = compute_halfcell_from_ocp(cfg, n_points=64, pe_offset_mv=10.0)
    np.testing.assert_allclose(off.u_pe, a.u_pe + 0.010, atol=1e-12)
    np.testing.assert_allclose(off.u_ne, a.u_ne, atol=1e-12)

    st = compute_halfcell_from_ocp(cfg, n_points=64, pe_stretch=0.95)
    assert st.y_pe.max() < a.y_pe.max(), "PE 화학량론이 안 줄었다"
    np.testing.assert_allclose(st.u_pe, a.u_pe, atol=1e-12)


def test_ocpbias_perturbation_changes_the_cache_key():
    """★ 왜곡은 recipe 서명에 들어가야 한다 — 다른 캐시 파일이 되어야 한다."""
    from src.halfcell import halfcell_cache_path, recipe_hash

    cfg = _base_cfg()
    h0 = recipe_hash(cfg, "ocpbias")
    h1 = recipe_hash(cfg, "ocpbias", pe_offset_mv=10.0)
    assert h0 != h1, "왜곡이 recipe 해시에 안 들어갔다"
    assert halfcell_cache_path(cfg, None, "ocpbias") \
        != halfcell_cache_path(cfg, None, "ocpbias", pe_offset_mv=10.0)


def test_ocpbias_rejects_unknown_perturbation_args():
    """★ 모르는 인자는 조용히 무시되면 안 된다 (서명 밖 변수)."""
    import pytest as _pt
    from src.halfcell import recipe_of

    with _pt.raises(ValueError, match="모르는 인자"):
        recipe_of("ocpbias", pe_offset_volt=0.01)


def test_ocpbias_method_name_matches_the_sealed_cache_pattern():
    """★ hessian 의 봉인 staging 정규식이 `[a-z]+` 라 밑줄이 들어가면 안 된다."""
    import re

    assert re.fullmatch(r"[a-z]+", "ocpbias"), "method 이름에 밑줄·숫자 금지"
