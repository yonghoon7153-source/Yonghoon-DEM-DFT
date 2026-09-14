"""규진팀 MATLAB electrode balancing (Si/Gr 블렌드) 의 **충실한 Python 포팅**.

이 파일의 목적은 하나다: 그들의 α·β(=[a_PE,b_PE,a_NE,b_NE,γ_Si]) 가
**데이터로부터 실제로 정해지는가**를 여기서 재기 위한 것. 그러므로

  ⚠ **모델을 고치지 않는다.** 눈에 보이는 결함(경계·창 자르기·외삽·비결정성)도
    그대로 옮긴다. 고쳐서 옮기면 "그들의 답"이 아니라 "우리 답"을 재게 된다.
    고칠 자리는 `verify.py` 가 **측정한 뒤** 별도로 제안한다.

원본 대응 (2026-09-10 받은 zip):

  electrode_ocv.m          → load_halfcell()
  differential.m           → differential()
  build_blend_functions.m  → build_blend()
  electrode_balancing_blend.m → Objective / fit()
  main_blend_final.m       → pipeline.py

MATLAB 과 다를 수 있는 자리는 전부 `# ≠MATLAB` 으로 표시했다. 그 자리는
포팅 충실도 검사(`verify.py --port-check`)가 숫자로 확인한다.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator
from scipy.signal import savgol_filter, find_peaks

# ── MATLAB 호환 유틸 ────────────────────────────────────────────────────


def matlab_quantile(x: np.ndarray, p: float) -> float:
    """MATLAB `quantile` — plotting position (i-0.5)/n 의 선형 보간.

    numpy 기본(linear, (i-1)/(n-1))과 다르다. 창 자르기 경계가 몇 점씩
    달라지면 RMSE 가 미세하게 달라지므로 정의를 맞춘다.
    """
    x = np.sort(np.asarray(x, dtype=float))
    n = x.size
    if n == 0:
        return np.nan
    if n == 1:
        return float(x[0])
    pos = (np.arange(1, n + 1) - 0.5) / n
    return float(np.interp(p, pos, x, left=x[0], right=x[-1]))


def average_duplicates(x: np.ndarray, y: np.ndarray):
    """averageDuplicates.m — 같은 x 를 하나로 접고 y 는 평균."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xu, inv = np.unique(x, return_inverse=True)
    ysum = np.bincount(inv, weights=y)
    ycnt = np.bincount(inv)
    return xu, ysum / ycnt


def _unique_first(x: np.ndarray, y: np.ndarray):
    """MATLAB `[u, i] = unique(x)` 는 **정렬된** 값과 그 인덱스를 준다."""
    xu, idx = np.unique(np.asarray(x, dtype=float), return_index=True)
    return xu, np.asarray(y, dtype=float)[idx]


def _pchip(xq_src: np.ndarray, y_src: np.ndarray, xq: np.ndarray) -> np.ndarray:
    """MATLAB interp1(...,'pchip') — 범위 밖은 pchip 외삽."""
    return PchipInterpolator(xq_src, y_src, extrapolate=True)(xq)


def _interp_lin_extrap(xs: np.ndarray, ys: np.ndarray, xq):
    """MATLAB interp1(...,'linear','extrap').

    ⚠ 2026-09-10: MATLAB `interp1` 은 x 가 **단조 증가든 단조 감소든** 받는다.
      `np.interp` 는 증가를 **가정만 하고 검사하지 않는다** — 감소하는 x 를
      주면 조용히 틀린 값을 낸다 (범위 안 점까지 전부).

      드러난 경위: 원통형 셀(#168)을 붙였더니 `E_PE(0.5)` 가 **29.96 V** 로
      나왔다. 그 셀 양극 반쪽전지가 파우치와 반대 방향으로 측정돼서, 방향
      정규화(`pe_c = 1 - pe_c/pe_c[-1]`)를 지나면 x 가 내림차순이 된다.
      파우치 자료는 오름차순이라 이 자리가 여태 안 드러났다.

      파우치 결과는 영향이 없다 — 그 경로는 오름차순이고, 아래 뒤집기는
      내림차순일 때만 걸린다. (그리고 파우치 값들은 MATLAB 과 1e-13 에서
      맞춰 놓은 것이라, 만약 내림차순이었다면 그 대조가 진작 깨졌다.)
    """
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    xq = np.atleast_1d(np.asarray(xq, dtype=float))
    if xs.size >= 2 and xs[0] > xs[-1]:
        xs, ys = xs[::-1], ys[::-1]
    # ⚠ 2026-09-11 (R2 후속, L0-7): MATLAB `interp1` 은 x 가 단조가 아니면(중복 포함)
    #   에러다. `np.interp` 는 조용히 값을 낸다. 원통형 워크북은 우리가 썼으므로 중복
    #   용량점이 들어올 수 있고, 그러면 조용한 쓰레기가 "넓은 띠" 로 보인다. 죽인다.
    if xs.size >= 2 and np.any(np.diff(xs) <= 0):
        bad = int(np.argmax(np.diff(xs) <= 0))
        raise ValueError(
            f"interp1: x 가 단조 증가/감소가 아니다 (index {bad}: {xs[bad]!r} → {xs[bad+1]!r}). "
            "MATLAB interp1 은 여기서 에러다 — 중복·비단조 용량점을 적재 단계에서 걸러라.")
    out = np.interp(xq, xs, ys)
    # 범위 밖은 양 끝 기울기로 선형 외삽 (np.interp 는 끝값을 유지한다)
    if xs.size >= 2:
        lo = xq < xs[0]
        if lo.any():
            m = (ys[1] - ys[0]) / (xs[1] - xs[0])
            out[lo] = ys[0] + m * (xq[lo] - xs[0])
        hi = xq > xs[-1]
        if hi.any():
            m = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
            out[hi] = ys[-1] + m * (xq[hi] - xs[-1])
    return out


def sgolay(y: np.ndarray, poly_order: int, window: int) -> np.ndarray:
    """MATLAB sgolayfilt(y, order, framelen).

    ≠MATLAB: MATLAB 은 가장자리를 다항 근사로 따로 처리한다. scipy 의
    mode='interp' 가 같은 방침이다 (끝 구간에 다항식을 맞춰 값을 낸다).
    완전히 같은 수는 아닐 수 있어 포팅 충실도 검사로 확인한다.
    """
    y = np.asarray(y, dtype=float)
    if window % 2 == 0:
        window += 1
    if window > y.size:
        window = y.size if y.size % 2 == 1 else y.size - 1
    if window <= poly_order:
        return y.copy()
    return savgol_filter(y, window_length=window, polyorder=poly_order,
                         mode="interp")


# ── differential.m ──────────────────────────────────────────────────────

class Differential:
    """differential.m 의 결과 묶음."""

    __slots__ = ("capacity_uniform", "voltage_uniform", "dqdv",
                 "capacity_uniform2", "voltage_uniform2", "dvdq")

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def differential(capacity, voltage, window: int = 9, poly_order: int = 1,
                 n_points: int = 500) -> Differential:
    capacity = np.asarray(capacity, dtype=float)
    voltage = np.asarray(voltage, dtype=float)
    ok = np.isfinite(capacity) & np.isfinite(voltage)
    capacity, voltage = capacity[ok], voltage[ok]

    # dQ/dV — voltage 균일 격자
    vu, cu = _unique_first(voltage, capacity)
    v_uniform = np.linspace(vu.min(), vu.max(), n_points)
    c_uniform = _pchip(vu, cu, v_uniform)
    c_smooth = sgolay(c_uniform, poly_order, window)
    dqdv = np.gradient(c_smooth) / np.gradient(v_uniform)

    # dV/dQ — capacity 균일 격자
    cu2, vu2 = _unique_first(capacity, voltage)
    c_uniform2 = np.linspace(cu2.min(), cu2.max(), n_points)
    v_uniform2 = _pchip(cu2, vu2, c_uniform2)
    v_smooth2 = sgolay(v_uniform2, poly_order, window)
    dvdq = np.gradient(v_smooth2) / np.gradient(c_uniform2)

    return Differential(capacity_uniform=c_smooth, voltage_uniform=v_uniform,
                        dqdv=dqdv, capacity_uniform2=c_uniform2,
                        voltage_uniform2=v_uniform2, dvdq=dvdq)


# ── electrode_ocv.m ─────────────────────────────────────────────────────

def _extract(df: pd.DataFrame, prefix: str):
    """extractMyData.m — capacity/voltage 를 **각각** dropna 한다.

    ⚠ 원본 그대로다. 두 열의 NaN 위치가 다르면 쌍이 어긋난 채로 진행된다
    (지금 데이터에서는 어긋나지 않는 것을 실측 확인했다 — `verify.py` 가
    매번 다시 센다).
    """
    c = df[f"{prefix}_capacity"].to_numpy(dtype=float)
    v = df[f"{prefix}_voltage"].to_numpy(dtype=float)
    c = c[np.isfinite(c)]
    v = v[np.isfinite(v)]
    return c, v


class HalfCell:
    """electrode_ocv.m 의 반환값."""

    def __init__(self, path, window=9, poly_order=1):
        df = pd.read_excel(path)
        pe_c, pe_v = _extract(df, "PE")
        ne_c, ne_v = _extract(df, "NE")
        self.raw_len_mismatch = {"PE": len(pe_c) != len(pe_v),
                                 "NE": len(ne_c) != len(ne_v)}
        n = min(len(pe_c), len(pe_v))
        pe_c, pe_v = pe_c[:n], pe_v[:n]
        n = min(len(ne_c), len(ne_v))
        ne_c, ne_v = ne_c[:n], ne_v[:n]

        pe_c, pe_v = average_duplicates(pe_c, pe_v)
        ne_c, ne_v = average_duplicates(ne_c, ne_v)

        # 방향 판정 — **양 끝점 두 개**로만 정한다 (원본 그대로)
        self.pe_direction = "lithiation" if pe_v[-1] < pe_v[0] else "delithiation"
        if pe_v[-1] < pe_v[0]:
            pe_c = 1.0 - pe_c / pe_c[-1]
        else:
            pe_c = pe_c / pe_c[-1]

        self.ne_direction = "delithiation" if ne_v[-1] > ne_v[0] else "lithiation"
        if ne_v[-1] > ne_v[0]:
            ne_c = 1.0 - ne_c / ne_c[-1]
        else:
            ne_c = ne_c / ne_c[-1]

        self.pe_capacity, self.pe_voltage = pe_c, pe_v
        self.ne_capacity, self.ne_voltage = ne_c, ne_v

        self._d_pe = differential(pe_c, pe_v, window, poly_order)
        self._d_ne = differential(ne_c, ne_v, window, poly_order)

    def E_PE(self, x):
        return _interp_lin_extrap(self.pe_capacity, self.pe_voltage, x)

    def E_NE(self, x):
        return _interp_lin_extrap(self.ne_capacity, self.ne_voltage, x)

    def dv_PE(self, x):
        return _interp_lin_extrap(self._d_pe.capacity_uniform2, self._d_pe.dvdq, x)

    def dv_NE(self, x):
        return _interp_lin_extrap(self._d_ne.capacity_uniform2, self._d_ne.dvdq, x)


# ── build_blend_functions.m ─────────────────────────────────────────────

class GammaFit(SimpleNamespace if False else object):
    """`fit_gamma_si` 의 반환값 — 원본 `result` 구조체와 같은 이름."""

    __slots__ = ("gamma_Si_fit", "rmse", "gamma_scan", "rmse_scan")

    def __init__(self, gamma_Si_fit, rmse, gamma_scan, rmse_scan):
        self.gamma_Si_fit, self.rmse = float(gamma_Si_fit), float(rmse)
        self.gamma_scan, self.rmse_scan = gamma_scan, rmse_scan

    def __repr__(self):
        return f"GammaFit(gamma_Si_fit={self.gamma_Si_fit:.6f}, rmse={self.rmse:.6g})"


def fit_gamma_si(ne_capacity, ne_voltage, si_capacity_lit, si_voltage_lit, gr_capacity_lit, gr_voltage_lit,
                 *, gamma_range=(0.02, 0.5), use_dv: bool = True, window: int = 9, poly_order: int = 1):
    """`fit_gamma_si.m` 포팅 — 측정된 pristine 블렌드와 **독립** 문헌 Si/Gr 로 γ 를 1 차원 최적화한다.

    `Q_blend(U; γ) = γ·Q_Si(U) + (1−γ)·Q_Gr(U)` 를 세 곡선의 **공통 전압 구간**에서 만들고, 그 모델이 실측
    블렌드와 가장 잘 맞는 γ 를 찾는다 (Schmitt 2022 §3.2 의 DV 매칭). `generate_si_ocp` 류의 역산과 다른 점은
    문헌 곡선이 γ 와 **무관하게 고정**이라 γ 자체가 추정 대상이 된다는 것이다.

    원본 그대로: 전압으로 unique → 세 곡선의 겹치는 구간 → 1000 점 pchip → **각각** 0~1 재정규화 →
    (use_dv 면) `differential` 의 `dvdq` 를 실측 격자에 linear/extrap 으로 얹어 RMSE → 60 점 스캔 + `fminbnd`.
    모델 쪽 `differential` 이 실패하면 그 γ 의 값은 1e6 이다 (원본의 `catch`).

    ⚠ `Blend` 와 합치지 않는다: `Blend` 는 Si·Gr **둘**의 구간에서 2000 점을 쓰고, 여기는 **측정 곡선까지 셋**의
      구간에서 1000 점을 쓴다. 두 규약을 한 클래스에 욱여넣으면 어느 쪽도 원본과 같지 않게 된다.
    """
    lb, ub = float(gamma_range[0]), float(gamma_range[1])
    ne_v, ne_c = _unique_first(np.asarray(ne_voltage, float), np.asarray(ne_capacity, float))
    si_v, si_c = _unique_first(np.asarray(si_voltage_lit, float), np.asarray(si_capacity_lit, float))
    gr_v, gr_c = _unique_first(np.asarray(gr_voltage_lit, float), np.asarray(gr_capacity_lit, float))
    v_min = max(ne_v.min(), si_v.min(), gr_v.min())
    v_max = min(ne_v.max(), si_v.max(), gr_v.max())
    if v_min >= v_max:
        raise ValueError("블렌드/Si/Gr 문헌 데이터의 전압 구간이 겹치지 않는다")
    v_common = np.linspace(v_min, v_max, 1000)

    def norm01(a):
        lo, hi = a.min(), a.max()
        return (a - lo) / (hi - lo)

    q_meas = norm01(_pchip(ne_v, ne_c, v_common))
    q_si = norm01(_pchip(si_v, si_c, v_common))
    q_gr = norm01(_pchip(gr_v, gr_c, v_common))

    dv_meas_x = dv_meas_y = None
    if use_dv:
        d = differential(q_meas, v_common, window, poly_order)
        dv_meas_x, dv_meas_y = d.capacity_uniform2, d.dvdq

    def objective(gamma: float) -> float:
        q = norm01(gamma * q_si + (1.0 - gamma) * q_gr)
        if not use_dv:
            return float(np.sqrt(np.mean((q_meas - q) ** 2)))
        try:
            dm = differential(q, v_common, window, poly_order)
            fit = _interp_lin_extrap(dm.capacity_uniform2, dm.dvdq, dv_meas_x)
        except Exception:                                  # noqa: BLE001 — 원본의 catch
            return 1e6
        return float(np.sqrt(np.mean((dv_meas_y - fit) ** 2)))

    gamma_scan = np.linspace(lb, ub, 60)
    rmse_scan = np.array([objective(g) for g in gamma_scan], dtype=float)
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(objective, bounds=(lb, ub), method="bounded", options={"xatol": 1e-6})
    g_fit, v_fit = float(r.x), float(r.fun)
    # ⚠ `fminbnd` 는 국소 최소다 — 스캔이 더 좋은 점을 찾았으면 그것을 쓴다 (원본은 진단용으로만 두지만,
    #   그때 보고값과 스캔이 어긋나면 "무엇이 최적인가" 를 두 벌로 말하게 된다).
    j = int(np.argmin(rmse_scan))
    if rmse_scan[j] < v_fit:
        g_fit, v_fit = float(gamma_scan[j]), float(rmse_scan[j])
    return GammaFit(g_fit, v_fit, gamma_scan, rmse_scan)


class Blend:
    """문헌 순수 Si / 순수 Gr 을 γ 로 섞은 합성 음극.

    Q_blend(V) = γ·Si(V) + (1-γ)·Gr(V), 그 뒤 0~1 재정규화.
    """

    def __init__(self, si_capacity, si_voltage, gr_capacity, gr_voltage,
                 window=9, poly_order=1, n_points=2000):
        si_v, si_c = _unique_first(si_voltage, si_capacity)
        gr_v, gr_c = _unique_first(gr_voltage, gr_capacity)
        v_min = max(si_v.min(), gr_v.min())
        v_max = min(si_v.max(), gr_v.max())
        if v_min >= v_max:
            raise ValueError("문헌 Si/Gr OCP 의 전압 구간이 겹치지 않는다")
        self.V_common = np.linspace(v_min, v_max, n_points)
        si = _pchip(si_v, si_c, self.V_common)
        gr = _pchip(gr_v, gr_c, self.V_common)
        self.Si = (si - si.min()) / (si.max() - si.min())
        self.Gr = (gr - gr.min()) / (gr.max() - gr.min())
        self.window, self.poly_order = window, poly_order
        self._dv_cache: dict[float, tuple] = {}

    def _q_norm(self, gamma: float):
        q = gamma * self.Si + (1.0 - gamma) * self.Gr
        q = (q - q.min()) / (q.max() - q.min())
        idx = np.argsort(q, kind="stable")
        return q[idx], self.V_common[idx]

    def E(self, x, gamma: float):
        q_sorted, v_sorted = self._q_norm(gamma)
        return _interp_lin_extrap(q_sorted, v_sorted, x)

    def dv(self, x, gamma: float):
        key = round(float(gamma), 9)
        if key not in self._dv_cache:
            q_sorted, v_sorted = self._q_norm(gamma)
            d = differential(q_sorted, v_sorted, self.window, self.poly_order)
            self._dv_cache[key] = (d.capacity_uniform2, d.dvdq)
            if len(self._dv_cache) > 4096:          # 메모리 상한
                self._dv_cache.clear()
                self._dv_cache[key] = (d.capacity_uniform2, d.dvdq)
        cap, dvdq = self._dv_cache[key]
        return _interp_lin_extrap(cap, dvdq, x)


# ── electrode_balancing_blend.m — 목적함수 ──────────────────────────────

#: scale 의 "원본 설명식과 같다" 는 이 상대 허용오차 안의 **근사**다 (Codex R5-06). eps/하위절반평균 이 이보다 크면
#: +eps 가드가 결과를 바꾼다. 비교기의 MODEL_REL(1e-9)과 같은 크기.
SCALE_EQUIV_REL = 1e-9

LB5 = np.array([1.0, -0.5, 1.0, -0.5, 0.00])
UB5 = np.array([1.4, 0.0, 1.4, 0.1, 0.50])


class Objective:
    """5-파라미터 목적함수. p = [a_PE, b_PE, a_NE, b_NE, γ_Si]."""

    def __init__(self, half: HalfCell, blend: Blend, cell_capacity,
                 cell_voltage, window=11, poly_order=3,
                 w_pocv=1.0, w_dvdq=1.0, w_dqdv=0.0,
                 peak_weight=7.0, sigma_ratio=0.03, use_peak_weight=True,
                 n_model=500, scale_seed=0, n_scale_samples=50):
        self.half, self.blend = half, blend
        self.window, self.poly_order = window, poly_order

        capacity = np.asarray(cell_capacity, dtype=float)
        voltage = np.asarray(cell_voltage, dtype=float)
        capacity, voltage = average_duplicates(capacity, voltage)
        self.c_cell = float(capacity[-1])
        if voltage[0] < voltage[-1]:
            capacity = capacity / self.c_cell
        else:
            capacity = 1.0 - capacity / self.c_cell
        self.capacity, self.voltage = capacity, voltage

        d = differential(capacity, voltage, window, poly_order)
        # dV/dQ 창: capacity 15~85 % 분위수 (원본 그대로 — 양 끝 30 % 를 버린다)
        lo, hi = matlab_quantile(d.capacity_uniform2, 0.15), matlab_quantile(d.capacity_uniform2, 0.85)
        m = (d.capacity_uniform2 >= lo) & (d.capacity_uniform2 <= hi)
        self.cap_dv_fit, self.dv_fit_data = d.capacity_uniform2[m], d.dvdq[m]
        self.dv_window = (lo, hi)

        # dQ/dV 창: voltage 5~95 % 분위수
        vlo, vhi = matlab_quantile(d.voltage_uniform, 0.05), matlab_quantile(d.voltage_uniform, 0.95)
        mv = (d.voltage_uniform >= vlo) & (d.voltage_uniform <= vhi)
        self.vol_dq_fit, self.dq_fit_data = d.voltage_uniform[mv], d.dqdv[mv]
        self.dq_window = (vlo, vhi)
        self.diff_cell = d

        self.x_model = np.linspace(0.0, 1.0, n_model)
        self.w_pocv, self.w_dvdq, self.w_dqdv = w_pocv, w_dvdq, w_dqdv
        self.use_peak_weight = use_peak_weight
        self.w_peak = self._peak_weights(peak_weight, sigma_ratio)

        # ⚠ 원본은 `rand` 50 개로 scale 을 잡는다 — **seed 가 없다.**
        #   포팅에서는 seed 를 받아 결정론적으로 만들되, 그 값이 seed 마다
        #   얼마나 흔들리는지는 verify.py 가 따로 잰다.
        self.scale_seed = scale_seed
        self.n_scale_samples = n_scale_samples
        self.scales = self._auto_scales(scale_seed, n_scale_samples)

    # -- 개별 항 --------------------------------------------------------
    def E_cell(self, p, x):
        return (self.half.E_PE((x - p[1]) / p[0])
                - self.blend.E(np.atleast_1d((x - p[3]) / p[2]), p[4]))

    def dv_cell(self, p, x):
        return (self.half.dv_PE((x - p[1]) / p[0])
                - self.blend.dv(np.atleast_1d((x - p[3]) / p[2]), p[4]))

    def rmse_pocv(self, p) -> float:
        r = self.voltage - self.E_cell(p, self.capacity)
        return float(np.sqrt(np.mean(r ** 2)))

    def rmse_dvdq(self, p) -> float:
        r = self.dv_fit_data - self.dv_cell(p, self.cap_dv_fit)
        return float(np.sqrt(np.mean(r ** 2)))

    def _model_dqdv(self, p):
        v_model = self.E_cell(p, self.x_model)
        v_smooth = sgolay(v_model, self.poly_order, self.window)
        dq_model = np.gradient(self.x_model) / np.gradient(v_smooth)
        # ⚠ 원본: unique(v_smooth) — 모델 전압이 단조가 아니면 점이 조용히
        #   버려지고 남은 것으로 보간한다. 그대로 옮긴다.
        v_u, uid = np.unique(v_smooth, return_index=True)
        return v_u, dq_model[uid]

    def rmse_dqdv(self, p, weighted=False) -> float:
        v_u, dq_u = self._model_dqdv(p)
        m = (self.vol_dq_fit >= v_u.min()) & (self.vol_dq_fit <= v_u.max())
        if m.sum() < 5:
            return 1e6
        dq_i = np.interp(self.vol_dq_fit[m], v_u, dq_u)
        resid = self.dq_fit_data[m] - dq_i
        if weighted:
            w = self.w_peak[m]
            return float(np.sqrt(np.sum(w * resid ** 2) / np.sum(w)))
        return float(np.sqrt(np.mean(resid ** 2)))

    # -- 가중치·scale ---------------------------------------------------
    def _peak_weights(self, peak_weight, sigma_ratio):
        dq = self.dq_fit_data
        vol = self.vol_dq_fit
        w = np.ones_like(dq)
        prom = 0.1 * (dq.max() - dq.min())
        locs, _ = find_peaks(dq, prominence=prom)
        # 몇 개를 찾았는지 남긴다 — dd_eval.m 대조의 `n_peaks` 앵커가 이것이다
        # (같은 규칙을 verify.py 에 다시 쓰지 않으려고 여기 둔다).
        self.peak_locs = locs
        if locs.size == 0:
            return w
        sigma = sigma_ratio * (vol.max() - vol.min())
        for k in locs:
            w = w + (peak_weight - 1.0) * np.exp(-((vol - vol[k]) ** 2) / (2 * sigma ** 2))
        return w

    #: ⚠ Codex R4-05: 원본 `lower_half_mean_local` 은 **NaN 만** 지운다 (`vals(~isnan(vals))`) — Inf 는 남아
    #:   정렬 뒤 하위 절반에 들면 scale 이 Inf 가 된다. 이 포팅은 **NaN 과 ±Inf 를 전부** 지운다. 그러므로 두
    #:   구현은 raw RMSE 표본이 전부 유한한 영역에서만 같다. 평탄부(dV/dQ=0)가 있는 forward 는 유한·연속이어도
    #:   `rmse_dqdv` 에 Inf 를 만들 수 있고, `__call__` 의 1e6 가드는 여기 raw 호출을 감싸지 않는다.
    #:   그래서 표본의 개수(n·유한·Inf·NaN)를 `scale_audit` 에 남긴다 — Inf 표본이 0 이면 그 실행에서 동치.
    NONFINITE_SCALE_POLICY = ("Python: NaN 과 ±Inf 표본을 모두 제거한 뒤 정렬·하위 절반 평균 (+eps). "
                              "원본 설명식: NaN 만 제거 — Inf 표본이 있으면 두 scale 이 다르다 (R4-05). "
                              "그리고 +eps 는 하위 절반 평균이 eps 에 비해 클 때만 무시된다 (R5-06): "
                              "동치 flag = 전부 유한 · 예외 없음 · eps/평균 ≤ SCALE_EQUIV_REL (상대 근사, 정확 동치 아님).")

    def _auto_scales(self, seed, n_samples, lb=None, ub=None):
        """목적함수 항의 scale. 원본은 `samples = lb + rand(n,5).*(ub-lb)`.

        ⚠ 2026-09-10 리뷰 [A1]: `lb`/`ub` 를 받게 열어 둔 이유는, MATLAB
          검증기의 고정-γ 프로파일이 `lb(5)=ub(5)=g` 를 **넘겨서** fit 을
          부르기 때문이다. 원 scale 식이 넘겨받은 경계에서 표본을 만들면
          MATLAB 은 γ 마다 다른 scale 을 쓰고, 전역 경계로 한 번 뽑아 재사용하는
          우리 프로파일과 **다른 목적함수**를 최적화하게 된다.
          기본값(전역)은 그대로 두되 선택할 수 있게 한다 — 어느 쪽이 그들
          절차인지는 그들 소스를 봐야 정해진다.
        """
        lb = LB5 if lb is None else np.asarray(lb, dtype=float)
        ub = UB5 if ub is None else np.asarray(ub, dtype=float)
        rng = np.random.default_rng(seed)
        s = lb + rng.random((n_samples, 5)) * (ub - lb)
        vals = {"pocv": [], "dvdq": [], "dqdv": []}
        n_exc = {k: 0 for k in vals}
        metrics = {"pocv": lambda row: self.rmse_pocv(row),
                   "dvdq": lambda row: self.rmse_dvdq(row),
                   "dqdv": lambda row: self.rmse_dqdv(row, self.use_peak_weight)}
        for row in s:
            # ⚠ Codex R5-10: 항마다 표본당 정확히 한 기록. 전 판은 둘째 항의 예외가 세 배열 모두에 NaN 을
            #   **다시** 넣어 첫째 항이 n=100 이 됐다. 예외는 따로 센다 (원본은 삼킨다 — 값은 NaN 으로).
            for k, fn in metrics.items():
                try:
                    vals[k].append(float(fn(row)))
                except Exception:                      # noqa: BLE001
                    vals[k].append(np.nan); n_exc[k] += 1
        eps = float(np.finfo(float).eps)
        out, audit = {}, {}
        for k, v in vals.items():
            a = np.array(v, dtype=float)
            rec = {"n": int(a.size), "n_finite": int(np.isfinite(a).sum()),
                   "n_inf": int(np.isinf(a).sum()), "n_nan": int(np.isnan(a).sum()), "n_exception": n_exc[k]}
            a = a[np.isfinite(a)]
            if a.size == 0:
                out[k] = eps
                rec.update(raw_lower_half_mean=None, scale=eps, eps_rel=float("inf"), equivalent_within_rel=False)
            else:
                a.sort()
                half = max(1, a.size // 2)
                raw = float(a[:half].mean())
                out[k] = raw + eps
                # ⚠ Codex R5-06: "전부 유한" 은 충분조건이 아니다 — +eps 의 상대 영향 eps/raw 가 커지면
                #   (raw ~ 1e-20 이면 22205 배) 원본 설명식과 갈린다. 동치는 상대 SCALE_EQUIV_REL 안의 근사로만.
                eps_rel = float("inf") if raw <= 0 else eps / raw
                rec.update(raw_lower_half_mean=raw, scale=out[k], eps_rel=eps_rel,
                           equivalent_within_rel=bool(rec["n_inf"] == 0 and rec["n_nan"] == 0
                                                      and n_exc[k] == 0 and eps_rel <= SCALE_EQUIV_REL))
            audit[k] = rec
        self.scale_audit = audit                      # R4-05/R5-06: 표본 개수·raw 평균·eps 영향·동치 flag
        return out

    # -- 합 -------------------------------------------------------------
    def __call__(self, p) -> float:
        p = np.asarray(p, dtype=float)
        try:
            val = (self.w_pocv * self.rmse_pocv(p) / self.scales["pocv"]
                   + self.w_dvdq * self.rmse_dvdq(p) / self.scales["dvdq"])
            if self.w_dqdv:
                val += (self.w_dqdv
                        * self.rmse_dqdv(p, self.use_peak_weight) / self.scales["dqdv"])
        except Exception:                              # noqa: BLE001
            return 1e6
        return float(val) if np.isfinite(val) else 1e6


# ── LAM / LLI (main_blend_final.m) ──────────────────────────────────────

def degradation_modes(p_ref, c_ref, p, c):
    """pristine(ref) 대비 LAM_PE · LAM_NE · LLI.

    원본 그대로:
        LAM_PE = (a_PE_i·c_i − a_PE·c) / (a_PE_i·c_i)
        LAM_NE = (a_NE_i·c_i − a_NE·c) / (a_NE_i·c_i)
        c_lit  = (a_PE + b_PE − b_NE)·c
        LLI    = (c_lit_i − c_lit) / c_lit_i
    """
    a_pe_i, b_pe_i, a_ne_i, b_ne_i = p_ref[0], p_ref[1], p_ref[2], p_ref[3]
    a_pe, b_pe, a_ne, b_ne = p[0], p[1], p[2], p[3]
    lam_pe = (a_pe_i * c_ref - a_pe * c) / (a_pe_i * c_ref)
    lam_ne = (a_ne_i * c_ref - a_ne * c) / (a_ne_i * c_ref)
    c_lit_i = (a_pe_i + b_pe_i - b_ne_i) * c_ref
    c_lit = (a_pe + b_pe - b_ne) * c
    lli = (c_lit_i - c_lit) / c_lit_i
    return {"LAM_PE": float(lam_pe), "LAM_NE": float(lam_ne), "LLI": float(lli)}
