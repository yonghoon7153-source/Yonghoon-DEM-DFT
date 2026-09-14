"""사이클별 α·β 적합 — 규진팀 `main_blend_final.m` 의 사이클 루프를 우리 하네스로 (BML_R1_RESPONSE §9 결정 실험).

무엇이 같은가: 모델(`Objective` — E_cell = E_PE((x−b_PE)/a_PE) − E_NE_blend((x−b_NE)/a_NE, γ)) · 경계 `LB5/UB5`
(= main_blend_final.m:46-47 의 lb5/ub5) · 목적함수 항과 가중(w_pocv 1 · w_dvdq 1 · w_dqdv 0 = "방법3") · 원자료 형식
(`extractMyData` 규약: '<cycle>_capacity' / '<cycle>_voltage' 열) · 수출 공식(`model.degradation_modes`, main_blend_final.m:137-151).
무엇이 다른가: MultiStart 는 우리 `verify.multistart`(L-BFGS-B, **seed 있음**) — MATLAB 의 rng(0) 오염이 만든 "사이클마다 같은
시작점" 은 여기서 `--seed` 로 **의도적으로** 재현하거나 바꿀 수 있다. 두 seed 의 산출이 갈리면 그 적합은 시작점이 정한 것이다.
기준행(cycle 0)은 그 워크북 안에서 정한다 — 항등식의 분모.
"""
from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd

from . import data as D
from .model import LB5, UB5, Blend, HalfCell, Objective, _extract, degradation_modes, fit_gamma_si
from .schema import inputs_digest
from .verify import active_bounds, multistart, near_optimal_extrema

#: main_blend_final.m:45 — 원본은 γ 를 Track B 로 대체하고 나머지 넷을 시작점으로 쓴다. 여기서는 seed 시작점들에 이 점 하나를 더한다.
INITIAL5 = (1.08, -0.04, 1.05, -0.03, 0.25)
_CYCLE_COL = re.compile(r"^(\d+)_capacity$")


def read_workbook(src) -> pd.DataFrame:
    """xlsx (또는 csv) → DataFrame. `src` 는 경로나 bytes 스트림 (한 번 읽은 bytes 로 파싱·해시, Codex R6-03)."""
    name = str(getattr(src, "name", src))
    if name.lower().endswith(".csv"):
        return pd.read_csv(src)
    return pd.read_excel(src)


def discover_cycles(df: pd.DataFrame) -> list:
    """'<n>_capacity' 와 짝 '<n>_voltage' 가 둘 다 있는 n — 오름차순 정수."""
    out = []
    for c in df.columns:
        m = _CYCLE_COL.match(str(c))
        if m and f"{m.group(1)}_voltage" in df.columns:
            out.append(int(m.group(1)))
    return sorted(set(out))


def load_cycle(df: pd.DataFrame, cycle: int):
    """그 사이클의 (capacity, voltage) — `extractMyData` 와 같은 규칙(각 열 따로 dropna). 없으면 KeyError."""
    if f"{cycle}_capacity" not in df.columns or f"{cycle}_voltage" not in df.columns:
        raise KeyError(f"cycle {cycle}: '{cycle}_capacity'/'{cycle}_voltage' 열이 없다 (있는 사이클: {discover_cycles(df)})")
    return _extract(df, str(cycle))



#: 폭을 못 쟀을 때 채우는 값 — **빈 칸이지 0 이 아니다.** 0 으로 채우면 읽는 쪽이 "폭이 0 = 완벽히 식별됐다"
#: 로 읽는다 (본체 게이트 61차 P1-3 과 같은 축: 측정 실패가 성공 영수증이 되면 안 된다).
_WIDTH_EMPTY = {"width_tol": "", "width_is_lower_bound": "",
                "LAM_PE_lo": "", "LAM_PE_hi": "", "LAM_NE_lo": "", "LAM_NE_hi": "", "LLI_lo": "", "LLI_hi": ""}


def _width_fields(widths, obj, ref_p, ref_c, c_cell, best, best_val, tol, starts, seed, lb5, say):
    """근최적 집합 위의 LAM/LLI 폭을 **이 적합이 쓴 상자에서** 잰다 (W-11 · W-12).

    단위: `near_optimal_extrema` 는 % 로 돌려주는데 행의 `LAM_*`/`LLI` 는 **분수**다 — 100 으로 나눈다.
    안 나누면 폭이 100 배가 되고, 점추정은 여전히 그 안에 들어가므로 범위 검사만으로는 안 걸린다.

    실패하면 **값을 지어내지 않고** `failed` 로 적는다. 적합 자체는 살아 있으므로 산출을 버리지도 않는다.
    """
    if not widths:
        return {"width_status": "not_requested", **_WIDTH_EMPTY}
    try:
        ext = near_optimal_extrema(obj, ref_p, ref_c, c_cell, best, best_val,
                                   tol=float(tol), seeds=[], n_starts=int(starts), seed=int(seed),
                                   lb=lb5, ub=UB5)
        out = {"width_status": "measured", "width_tol": float(tol),
               "width_is_lower_bound": all(bool(ext[k].get("is_lower_bound")) for k in ("LAM_PE", "LAM_NE", "LLI"))}
        for mode in ("LAM_PE", "LAM_NE", "LLI"):
            out[f"{mode}_lo"] = float(ext[mode]["min"]) / 100.0
            out[f"{mode}_hi"] = float(ext[mode]["max"]) / 100.0
        return out
    except Exception as e:                                   # noqa: BLE001
        say(f"  ! 폭 계산 실패 ({type(e).__name__}: {e}) — 이 행은 width_status=failed 로 적는다")
        return {"width_status": "failed", **_WIDTH_EMPTY}


def fit_cycles(root, half_cell, full_cell, si_source: str, *, cell: str, cycles=None,
               n_starts: int = 20, seed: int = 0, scale_seed: int = 0, w_dqdv: float = 0.0, run_id: str = "",
               literature=None, gamma_prefit: bool = False, gamma_lb: float | None = None,
               widths: bool = False, width_tol: float = 0.01, width_starts: int = 4,
               log=None) -> dict:
    """사이클마다 적합 → {"rows": [CYCLES_ROW dict …], "consumed": 공통 receipt, "settings": 기록된 optimizer 설정}.

    입력 셋(기준 반쪽전지 · 풀셀 워크북 · 문헌 Si/Gr)은 한 번 읽은 bytes 로 파싱하고 그 bytes 를 해시한다.
    행마다 receipt 는 같은 셋 + 그 행의 cycle 이다 (`REQUIRED_ROLES` 그대로).

    ⚠ `seed` 는 **MultiStart 시작점**만, `scale_seed` 는 **목적함수 scale 표본**(50 개, R5-07)만 움직인다. 둘을 한 인자에
      묶으면 seed 를 바꿨을 때의 값 차이가 시작점 탓인지 scale 탓인지 가를 수 없다 (사용자 기계 HD_knee 첫 실행이 그랬다).
      "시작점이 정한 적합인가" 는 `scale_seed` 고정 · `seed` 변경으로 묻는다; scale 의존은 `verify scale-noise` 의 축이다.
    """
    say = log or (lambda *a, **k: None)
    hb = D.read_input(half_cell)
    half = HalfCell(hb.stream(), window=11, poly_order=3)
    lit_id: dict = {}
    # ⚠ `literature` 는 정본 8 소스 **밖**의 검증 데이터를 받는 길이다 (pyDMA 예제처럼 Si·Gr 이 한 파일).
    #   로스터 이름 하나에 남의 파일을 밀어 넣으면 receipt 가 거짓말을 하므로 라벨도 `external` 로 짝을 맞춘다.
    if literature is not None:
        if si_source != D.EXTERNAL_SI_SOURCE:
            raise ValueError(f"외부 문헌 파일을 주면 si_source 는 '{D.EXTERNAL_SI_SOURCE}' 여야 한다 (받은 값 {si_source!r}) — "
                             f"로스터 이름은 그 소스의 데이터를 뜻한다")
        si_c, si_v, gr_c, gr_v = D.load_literature_file(literature, identity=lit_id)
    else:
        if si_source == D.EXTERNAL_SI_SOURCE:
            raise ValueError(f"si_source 가 '{D.EXTERNAL_SI_SOURCE}' 인데 --literature 가 없다 — 무엇을 읽었는지 말할 수 없다")
        si_c, si_v, gr_c, gr_v = D.load_literature(root, si_source, identity=lit_id)
    blend = Blend(si_c, si_v, gr_c, gr_v, window=11, poly_order=3)
    fb = D.read_input(full_cell)
    df = read_workbook(fb.stream())
    have = discover_cycles(df)
    want = sorted(set(int(c) for c in cycles)) if cycles else have
    missing = [c for c in want if c not in have]
    if missing:
        raise ValueError(f"요청한 cycle 이 워크북에 없다: {missing} (있는 사이클: {have})")
    if 0 not in want:
        raise ValueError(f"cycle 0 (기준행) 이 없다 — 항등식의 분모가 없다 (있는 사이클: {have})")
    consumed = {"half_cell": hb.identity(), "full_cell": fb.identity(), "literature": lit_id}
    # ⚠ γ 사전 적합 (pyDMA Track C 대조): 반쪽전지만으로 γ 를 먼저 적합해 초기값으로 쓴다 (`fit_gamma_si.m`).
    #   하한도 함께 올릴 수 있다 (Track C 는 0.02). **둘 다 기록되는 실행 조건**이다 — 조용히 바뀌면 두 실행의
    #   차이를 설정 탓인지 데이터 탓인지 가를 수 없다.
    lb5 = np.asarray(LB5, dtype=float).copy()
    initial5 = np.asarray(INITIAL5, dtype=float).copy()
    gamma_init = None
    if gamma_lb is not None:
        lb5[4] = float(gamma_lb)
    if gamma_prefit:
        gf = fit_gamma_si(half.ne_capacity, half.ne_voltage, si_c, si_v, gr_c, gr_v,
                          gamma_range=(float(lb5[4]), float(UB5[4])))
        gamma_init = float(gf.gamma_Si_fit)
        initial5[4] = gamma_init
        say(f"  γ 사전 적합 (반쪽전지만): {gamma_init:.4f} · RMSE {gf.rmse:.6g}")
    settings = {"lb": [float(x) for x in lb5], "ub": [float(x) for x in UB5],
                "initial": [float(x) for x in initial5],
                "gamma_prefit": bool(gamma_prefit), "gamma_init": gamma_init,
                "gamma_lb": (float(gamma_lb) if gamma_lb is not None else None),
                # ⚠ 폭은 **기록되는 실행 조건**이다 — 허용(tol)을 안 밝힌 폭은 인용할 수 없다 (§12-3 과 같은 이유).
                "widths": bool(widths), "width_tol": (float(width_tol) if widths else None),
                "width_starts": (int(width_starts) if widths else None),
                "width_method": ("near_optimal_extrema" if widths else None),
                "free": ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"], "n_multistart": int(n_starts),
                "seed": int(seed), "scale_seed": int(scale_seed), "w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": float(w_dqdv),
                "optimizer": "L-BFGS-B (scipy)"}
    fits = {}
    for k in want:
        c, v = load_cycle(df, k)
        obj = Objective(half, blend, c, v, window=11, poly_order=3, w_pocv=1.0, w_dvdq=1.0, w_dqdv=w_dqdv,
                        use_peak_weight=True, scale_seed=scale_seed)
        best, val, _ = multistart(obj, n_starts=n_starts, seed=seed, x0=initial5, lb=lb5, ub=UB5)
        if best is None:
            raise RuntimeError(f"cycle {k}: 채택된 적합이 없다 ({multistart.last_stats})")
        fits[k] = (obj, np.asarray(best, dtype=float), float(val), dict(multistart.last_stats))
        say(f"  cycle {k}: a_PE {best[0]:.6f} b_PE {best[1]:.6f} a_NE {best[2]:.6f} b_NE {best[3]:.6f} "
            f"γ {best[4]:.4f} · obj {val:.6g} · 채택 {multistart.last_stats['accepted']}/{multistart.last_stats['tried']}")
    o0, p0, _, _ = fits[0]
    rows = []
    for k in want:
        o, p, val, st = fits[k]
        m = degradation_modes(p0, o0.c_cell, p, o.c_cell)
        rec = {"half_cell": consumed["half_cell"], "full_cell": dict(consumed["full_cell"], cycle=k),
               "literature": consumed["literature"]}
        rows.append({
            "cell": cell, "cycle": k, "C_cell": o.c_cell, "x_cell": o.c_cell / o0.c_cell,
            "a_PE": p[0], "b_PE": p[1], "a_NE": p[2], "b_NE": p[3], "gamma_Si": p[4],
            "c_lit": o.c_cell * (p[0] + p[1] - p[3]),
            "LAM_PE": m["LAM_PE"], "LAM_NE": m["LAM_NE"], "LLI": m["LLI"],
            **_width_fields(widths, o, p0, o0.c_cell, o.c_cell, p, val, width_tol, width_starts, seed, lb5, say),
            "obj": val, "rmse_pocv": o.rmse_pocv(p), "rmse_dvdq": o.rmse_dvdq(p), "rmse_dqdv": o.rmse_dqdv(p),
            "n_starts": int(n_starts), "n_accepted": int(st.get("accepted", 0)),
            # ⚠ scale 은 행이 스스로 말한다 (R5-07) — 두 seed 실행의 scale 열이 같아야 그 차이가 시작점의 것이다
            "scale_seed": int(scale_seed), "scale_pocv": o.scales.get("pocv"), "scale_dvdq": o.scales.get("dvdq"),
            "scale_dqdv": o.scales.get("dqdv"),
            # ⚠ W-06: 경계 판정은 **이 실행이 쓴 상자**로 한다. 상자를 안 넘기던 판은 `--gamma-lb 0.05` 로
            #   올린 하한에 γ 가 정확히 붙어도 `b_PE=ub` 만 적고 γ 는 자유로운 것처럼 내보냈다 (실측).
            #   "경계에 붙은 값" 을 세는 것이 규진팀 97 행에서 32 행을 잡아낸 그 검사다 (§2).
            "bounds": ",".join(active_bounds(p, lb=lb5, ub=UB5)) or "-", "run_id": run_id,
            "inputs_sha": inputs_digest(rec), "consumed_inputs": json.dumps(rec, ensure_ascii=False, sort_keys=True),
        })
    return {"rows": rows, "consumed": consumed, "settings": settings, "cycles": want}
