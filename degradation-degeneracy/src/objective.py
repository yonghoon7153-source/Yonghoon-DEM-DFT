"""objective.py — 34p 목적함수 J(p).

    J(p) = w_pocv · RMSE_pocv(p)/scale_pocv
         + w_dvdq · RMSE_dvdq(p)/scale_dvdq
         + w_dqdv · RMSE^w_dqdv(p)/scale_dqdv

RMSE^w_dqdv 의 위첨자 w는 **피크 가중 RMSE**를 뜻한다 (33p "peak weight factor").
타깃 dQ/dV에서 피크를 검출해 그 주변 ±halfwidth 구간에 peak_weight 배 가중한다.

scale: 세 항의 크기를 맞추기 위한 정규화 상수.
  reference 조건 신호의 RMS 변동폭을 쓴다 (조건마다 바뀌지 않아야 J를 격자 전체에서
  비교할 수 있으므로 reference 기준으로 한 번만 계산해 공유한다).
"""

from __future__ import annotations

import os

from dataclasses import dataclass

import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage import correlate1d
from scipy.signal import find_peaks, savgol_filter

# 창 밖(NaN)이 많은 해에 주는 벌점. 스케일 정규화 후 값이라 O(1) 대비 충분히 크다.
INVALID_PENALTY = 50.0
_MIN_VALID_FRAC = 0.5


# ── savgol 연산자 캐시 (F22) ───────────────────────────────────────────────
#
# 프로파일 실측: 한 조건 fitting 51초 중 **34초(66%)가 savgol_filter**였고,
# 그 안의 16초는 가장자리 다항식 적합의 lstsq였다 (조건당 lstsq 12만 회).
# scipy는 호출할 때마다 계수와 가장자리 적합을 다시 푼다.
#
# savgol은 고정 길이 신호에 대해 **선형 연산자**이므로 한 번 구해 재사용하면 된다.
# 단위행렬에 필터를 적용하면 그 연산자가 정확히 나온다 — 근사가 아니다
# (실측 최대오차 1.3e-13, 신호 스케일 21.8 → 기계 정밀도).
#
# ★ 다만 조밀 n×n 행렬로 들고 있으면 안 된다.
#   0이 아닌 원소가 7%뿐인데(내부 행은 창 크기 21개, 나머지 279개는 0)
#   32워커가 동시에 698 KB씩 읽으면 **메모리 대역폭이 병목**이 된다.
#   V100 실측: 단일 스레드 2.6배 가속이 32워커에서는 1.65배로 줄었다.
#
#   그래서 띠 구조를 그대로 쓴다 — 내부는 컨볼루션, 가장자리 2h행만 작은 블록.
#   이 세 조각은 **n에 의존하지 않는다** (가장자리는 늘 앞뒤 w개 점에 다항식을
#   맞춘다). 실측 격자의 길이 조합이 204종이어도 캐시는 (창,차수)별 하나뿐이다.
#
#     저장량   조밀 698 KB  →  띠 3.4 KB          (203배)
#     속도     scipy 387 us →  조밀 18.1 us  →  띠 13.2 us   (단일 스레드)
_SMOOTH_KERNEL: dict[tuple[int, int], tuple] = {}
# 0으로 두면 캐시를 끄고 scipy를 그대로 쓴다 (동등성 검증용)
_SMOOTH_CACHE_ENABLED = os.environ.get("DD_SMOOTH_CACHE", "1") != "0"


def _smooth_kernel(w: int, polyorder: int):
    """(내부 컨볼루션 계수, 상단 가장자리 블록, 하단 가장자리 블록, 반폭)."""
    key = (w, polyorder)
    k = _SMOOTH_KERNEL.get(key)
    if k is None:
        h = w // 2
        # 길이 w 신호에 대한 savgol 연산자. 단위행렬의 행 e_j를 필터링하면
        # 결과의 i번째 성분이 M[i, j] → 전치해야 M이 된다.
        Mw = np.ascontiguousarray(savgol_filter(np.eye(w), w, polyorder, axis=-1).T)
        k = (np.ascontiguousarray(Mw[h]),        # 중앙 행 = 내부 컨볼루션 계수
             np.ascontiguousarray(Mw[:h]),       # 앞 h행 (앞 w개 점에 작용)
             np.ascontiguousarray(Mw[-h:]),      # 뒤 h행 (뒤 w개 점에 작용)
             h)
        _SMOOTH_KERNEL[key] = k
    return k


def _smooth(y: np.ndarray, window: int, polyorder: int) -> np.ndarray:
    n = len(y)
    w = min(window, n if n % 2 else n - 1)
    if w <= polyorder + 1:
        return y
    if w % 2 == 0:
        w -= 1
    # 신호가 창보다 길지 않으면 내부 구간이 없다 → scipy에 맡긴다 (드물고 싸다)
    if not _SMOOTH_CACHE_ENABLED or n <= w:
        return savgol_filter(y, w, polyorder)

    coef, e_top, e_bot, h = _smooth_kernel(w, polyorder)
    out = correlate1d(y, coef, mode="constant")
    out[:h] = e_top @ y[:w]
    out[-h:] = e_bot @ y[-w:]
    return out


def dqdv_on_grid(x: np.ndarray, v: np.ndarray, v_grid: np.ndarray,
                 window: int = 21, polyorder: int = 3) -> np.ndarray:
    """dQ/dV를 공통 전압 격자 위로 올린다.

    ★ 순서가 중요하다: **먼저 Q(V)를 균일 전압 격자로 보간한 뒤 미분**한다.
      미분을 먼저 하면 전압 평탄 구간(dV≈0)에서 값이 발산하고, 그 스파이크가
      파라미터에 따라 요동쳐 목적함수에 국소최소를 만든다 (실측: 34p 목적함수에서
      정답 J=0인데 최적화가 J=0.49에 갇힘).
    타깃과 모델의 전압 범위가 달라 못 덮는 구간은 NaN.
    """
    finite = np.isfinite(x) & np.isfinite(v)
    if finite.sum() < 5:
        return np.full_like(v_grid, np.nan)
    xs, vs = x[finite], v[finite]

    order = np.argsort(vs)
    vs, xs = vs[order], xs[order]
    keep = np.concatenate([[True], np.diff(vs) > 1e-9])   # 단조 증가 강제
    vs, xs = vs[keep], xs[keep]
    if len(vs) < 5:
        return np.full_like(v_grid, np.nan)

    q = interp1d(vs, xs, bounds_error=False, fill_value=np.nan)(v_grid)
    inside = np.isfinite(q)
    if inside.sum() < 5:
        return np.full_like(v_grid, np.nan)

    out = np.full_like(v_grid, np.nan)
    out[inside] = np.gradient(_smooth(q[inside], window, polyorder),
                              v_grid[inside])
    return out


@dataclass
class CurveFeatures:
    """한 곡선의 pOCV / dV/dQ / dQ/dV 표현. 타깃은 1회만 계산해 재사용한다."""

    x: np.ndarray
    v: np.ndarray
    dvdq: np.ndarray
    v_grid: np.ndarray
    dqdv: np.ndarray
    peak_weight: np.ndarray      # dQ/dV 격자 위의 가중치 (피크 주변 > 1)


def compute_features(x: np.ndarray, v: np.ndarray, cfg: dict,
                     v_grid: np.ndarray | None = None,
                     with_peaks: bool = False,
                     need_dvdq: bool = True, need_dqdv: bool = True) -> CurveFeatures:
    """곡선 → 특징. with_peaks=True면 dQ/dV 피크 가중치도 계산 (타깃 전용).

    need_* 로 실제 쓰이는 항만 계산한다 — 목적함수 평가마다 호출되므로
    안 쓰는 변환을 빼는 것만으로 pocv/dvdq 계열이 크게 빨라진다.
    """
    d = cfg.get("dqdv", {})
    window = int(d.get("window", 21))
    polyorder = int(d.get("polyorder", 3))

    dvdq = np.full_like(v, np.nan)
    if need_dvdq:
        finite = np.isfinite(v)
        if finite.sum() >= 5:
            dvdq[finite] = np.gradient(_smooth(v[finite], window, polyorder), x[finite])

    if v_grid is None:
        lo, hi = np.nanmin(v), np.nanmax(v)
        v_grid = np.linspace(lo, hi, len(x))
    dqdv = (dqdv_on_grid(x, v, v_grid, window, polyorder) if need_dqdv
            else np.full_like(v_grid, np.nan))

    w = np.ones_like(v_grid)
    if with_peaks:
        prom = float(d.get("peak_prominence", 0.05))
        half = int(d.get("peak_halfwidth", 10))
        factor = float(d.get("peak_weight", 3.0))
        y = np.nan_to_num(dqdv, nan=0.0)
        peaks, _ = find_peaks(np.abs(y), prominence=prom)
        for pk in peaks:
            w[max(0, pk - half): pk + half + 1] = factor
    return CurveFeatures(x=x, v=v, dvdq=dvdq, v_grid=v_grid, dqdv=dqdv, peak_weight=w)


def _rmse(a: np.ndarray, b: np.ndarray, w: np.ndarray | None = None) -> float:
    """공통 유효 구간에서의 (가중) RMSE. 겹치는 점이 없으면 NaN."""
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 5:
        return float("nan")
    e2 = (a[m] - b[m]) ** 2
    if w is None:
        return float(np.sqrt(e2.mean()))
    ww = w[m]
    return float(np.sqrt((ww * e2).sum() / ww.sum()))


def default_scales(ref: CurveFeatures) -> dict:
    """reference 신호의 RMS 변동폭. 세 항을 무차원 O(1)로 맞춘다."""

    def rms_dev(y):
        m = np.isfinite(y)
        if m.sum() < 5:
            return 1.0
        val = float(np.sqrt(np.mean((y[m] - y[m].mean()) ** 2)))
        return val if val > 1e-12 else 1.0

    return {
        "pocv": rms_dev(ref.v),
        "dvdq": rms_dev(ref.dvdq),
        "dqdv": rms_dev(ref.dqdv),
    }


def make_objective(target: CurveFeatures, model_fn, weights: dict,
                   scales: dict, cfg: dict, shortfall_fn=None):
    """J(p)를 반환. model_fn(p) -> (x, v_model) 이어야 한다.

    벌점: 재구성 창이 관측 구간을 다 덮지 못하면 **부족량에 비례해** 더한다.
    NaN 점 개수로 세면 점이 하나씩 들락날락할 때마다 J가 계단처럼 튀어
    국소최소가 잔뜩 생긴다 (실측: 정답 J=0인데 최적화가 J=3.5에 갇힘).
    shortfall_fn(p)은 관측 구간 대비 창 부족량을 연속량으로 돌려줘야 한다.
    """
    w_pocv = float(weights.get("w_pocv", 0.0))
    w_dvdq = float(weights.get("w_dvdq", 0.0))
    w_dqdv = float(weights.get("w_dqdv", 0.0))

    obs = np.isfinite(target.v)
    n_obs = max(int(obs.sum()), 1)

    def J(p) -> float:
        _, v_model = model_fn(p)
        coverage = float((obs & np.isfinite(v_model)).sum()) / n_obs
        short = float(shortfall_fn(p)) if shortfall_fn is not None else 0.0
        penalty = INVALID_PENALTY * short
        if coverage < _MIN_VALID_FRAC:
            return INVALID_PENALTY * 10.0 + penalty

        total = 0.0
        if w_pocv:
            r = _rmse(v_model, target.v)
            if not np.isfinite(r):
                return INVALID_PENALTY * 10.0 + penalty
            total += w_pocv * r / scales["pocv"]
        if w_dvdq or w_dqdv:
            model = compute_features(target.x, v_model, cfg, v_grid=target.v_grid,
                                     need_dvdq=bool(w_dvdq), need_dqdv=bool(w_dqdv))
            if w_dvdq:
                r = _rmse(model.dvdq, target.dvdq)
                if not np.isfinite(r):
                    return INVALID_PENALTY * 10.0 + penalty
                total += w_dvdq * r / scales["dvdq"]
            if w_dqdv:
                r = _rmse(model.dqdv, target.dqdv, target.peak_weight)
                if not np.isfinite(r):
                    return INVALID_PENALTY * 10.0 + penalty
                total += w_dqdv * r / scales["dqdv"]

        return total + penalty

    return J


def load_objectives(cfg: dict) -> dict:
    """objectives.yaml의 4종 가중치 정의."""
    return dict(cfg["objectives"])
