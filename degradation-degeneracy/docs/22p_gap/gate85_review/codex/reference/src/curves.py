"""curves.py — solution → pOCV / dV/dQ / dQ/dV 곡선 추출.

원본 로직 보존 (reference/degrade_mode_sim_original.py):
  - 마지막 cycle의 마지막 step(최종 방전)에서 추출
  - cap = |Discharge capacity - 첫 값| × 1000 [mAh]
  - NE: "Battery negative electrode bulk open-circuit potential [V]"
  - PE: "X-averaged positive electrode open-circuit potential [V]"
  - full cell = PE − NE
  - 끝단 n_trim(기본 3)개 절단 후 보간 (cutoff 근처 solver 튐 방지)
  - x_cell_norm = np.linspace(0, 1, n_interp=300)
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

NE_OCP_VAR = "Battery negative electrode bulk open-circuit potential [V]"
PE_OCP_VAR = "X-averaged positive electrode open-circuit potential [V]"
CAP_VAR = "Discharge capacity [A.h]"


def extract_curves(solution, n_trim: int = 3, n_interp: int = 300,
                   q_ref_mah: float | None = None) -> dict:
    """최종 방전 step에서 곡선 추출.

    반환 dict:
      q_mah        : 실측 용량 [mAh] (trim 후 마지막 값)
      q_end_mah    : trim 전 원시 용량 [mAh]
      x_norm       : 정규화 용량 격자 (0..1, n_interp점) — q_ref 기준
      v_pe, v_ne, v_full : x_norm 위로 보간된 전위 [V]
      raw          : trim된 원시 (cap_mah, pe, ne) — 저장 옵션용
    q_ref_mah가 주어지면 그 값으로 정규화(원본 Q_ref 방식), 없으면 자기 용량으로.
    """
    step = solution.cycles[-1].steps[-1]

    cap = step[CAP_VAR].entries * 1000.0
    cap = np.abs(cap - cap[0])
    ne = step[NE_OCP_VAR].entries
    pe = step[PE_OCP_VAR].entries

    if len(cap) <= n_trim + 2:
        raise ValueError(f"곡선 포인트 부족: {len(cap)}점 (n_trim={n_trim})")

    if n_trim > 0:
        cap_t, pe_t, ne_t = cap[:-n_trim], pe[:-n_trim], ne[:-n_trim]
    else:
        cap_t, pe_t, ne_t = cap, pe, ne

    q_end = float(cap_t[-1])
    q_ref = float(q_ref_mah) if q_ref_mah else q_end
    cap_norm = cap_t / q_ref

    # 원본 windowed_curve와 동일한 보간 정책: 범위 밖은 끝값 유지
    f_pe = interp1d(cap_norm, pe_t, bounds_error=False,
                    fill_value=(pe_t[0], pe_t[-1]))
    f_ne = interp1d(cap_norm, ne_t, bounds_error=False,
                    fill_value=(ne_t[0], ne_t[-1]))

    x = np.linspace(0.0, 1.0, n_interp)
    v_pe = f_pe(x)
    v_ne = f_ne(x)

    return {
        "q_mah": q_end,
        "q_end_mah": float(cap[-1]),
        "x_norm": x,
        "v_pe": v_pe,
        "v_ne": v_ne,
        "v_full": v_pe - v_ne,
        "raw": (cap_t, pe_t, ne_t),
    }


def add_noise(v: np.ndarray, sigma: float, seed: int) -> np.ndarray:
    """full cell 전압에 gaussian 노이즈 추가. seed 고정으로 재현성 확보."""
    if sigma <= 0:
        return v.copy()
    rng = np.random.default_rng(seed)
    return v + rng.normal(0.0, sigma, size=v.shape)


def to_dvdq(x_norm: np.ndarray, v: np.ndarray,
            window: int = 21, polyorder: int = 3) -> np.ndarray:
    """dV/dQ (정규화 용량 기준). savgol 스무딩 후 gradient."""
    vs = savgol_filter(v, min(window, len(v) // 2 * 2 - 1), polyorder)
    return np.gradient(vs, x_norm)


def to_dqdv(x_norm: np.ndarray, v: np.ndarray,
            window: int = 21, polyorder: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """dQ/dV. 전압 축 정렬 후 gradient. 반환 (v_sorted, dqdv)."""
    vs = savgol_filter(v, min(window, len(v) // 2 * 2 - 1), polyorder)
    order = np.argsort(vs)
    v_sorted = vs[order]
    q_sorted = x_norm[order]
    with np.errstate(divide="ignore", invalid="ignore"):
        dqdv = np.gradient(q_sorted, v_sorted)
    return v_sorted, np.nan_to_num(dqdv, nan=0.0, posinf=0.0, neginf=0.0)


def windowed_curve(f_ref, x_cell_norm: np.ndarray,
                   alpha: float, beta: float) -> np.ndarray:
    """원본 windowed_curve 그대로 이식 (fitting의 정방향 모델).

    sto = (x − β)/α, 창 밖(sto∉[0,1])은 NaN.
    """
    sto = (x_cell_norm - beta) / alpha
    y = f_ref(np.clip(sto, 0, 1))
    return np.where((sto >= 0) & (sto <= 1), y, np.nan)
