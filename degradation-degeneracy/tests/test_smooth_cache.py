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
