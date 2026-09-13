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
from .model import LB5, UB5, Blend, HalfCell, Objective, _extract, degradation_modes
from .schema import inputs_digest
from .verify import active_bounds, multistart

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


def fit_cycles(root, half_cell, full_cell, si_source: str, *, cell: str, cycles=None,
               n_starts: int = 20, seed: int = 0, w_dqdv: float = 0.0, run_id: str = "",
               log=None) -> dict:
    """사이클마다 적합 → {"rows": [CYCLES_ROW dict …], "consumed": 공통 receipt, "settings": 기록된 optimizer 설정}.

    입력 셋(기준 반쪽전지 · 풀셀 워크북 · 문헌 Si/Gr)은 한 번 읽은 bytes 로 파싱하고 그 bytes 를 해시한다.
    행마다 receipt 는 같은 셋 + 그 행의 cycle 이다 (`REQUIRED_ROLES` 그대로).
    """
    say = log or (lambda *a, **k: None)
    hb = D.read_input(half_cell)
    half = HalfCell(hb.stream(), window=11, poly_order=3)
    lit_id: dict = {}
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
    settings = {"lb": [float(x) for x in LB5], "ub": [float(x) for x in UB5], "initial": list(INITIAL5),
                "free": ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"], "n_multistart": int(n_starts),
                "seed": int(seed), "w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": float(w_dqdv), "optimizer": "L-BFGS-B (scipy)"}
    fits = {}
    for k in want:
        c, v = load_cycle(df, k)
        obj = Objective(half, blend, c, v, window=11, poly_order=3, w_pocv=1.0, w_dvdq=1.0, w_dqdv=w_dqdv,
                        use_peak_weight=True, scale_seed=seed)
        best, val, _ = multistart(obj, n_starts=n_starts, seed=seed, x0=np.asarray(INITIAL5, dtype=float))
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
            "obj": val, "rmse_pocv": o.rmse_pocv(p), "rmse_dvdq": o.rmse_dvdq(p), "rmse_dqdv": o.rmse_dqdv(p),
            "n_starts": int(n_starts), "n_accepted": int(st.get("accepted", 0)),
            "bounds": ",".join(active_bounds(p)) or "-", "run_id": run_id,
            "inputs_sha": inputs_digest(rec), "consumed_inputs": json.dumps(rec, ensure_ascii=False, sort_keys=True),
        })
    return {"rows": rows, "consumed": consumed, "settings": settings, "cycles": want}
