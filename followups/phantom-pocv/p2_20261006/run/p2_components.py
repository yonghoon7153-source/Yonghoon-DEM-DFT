"""P2 성분 분석 (사본 밖 · 진단 전용 · 인용 금지).

사본 디렉터리에서 `python <이 파일> --out <json>` 으로 돈다 (cwd = 사본 — src/tools import).
다리 경로는 results/_smoke/p2/ 아래 고정 이름.

판정 규칙 (데이터 보기 전 고정 · 2026-10-06):
  · 원점 건강: L1 의 p_ini a_ne ∈ [1.05, 1.08] — 두 목적함수 모두 (아니면 전체 중단).
  · 왜곡 다리 원점 오염: 그 다리 a_ne ∉ [1.05, 1.08] → 권고 5 대로 세트 중단.
  · 조건 집합: L1–L6 의 cond_id 집합이 같아야 한다 (목적함수별).
  · + 부호 재현: objective pocv_dvdq_dqdv (§7.10 의 목적함수) · gap_stats 원 창에서
    Δ = gap_bias(L2) − gap_bias(L1) > 0 그리고 Δ(L3) > 0. 아니면 tilt 해석 전에 멈춘다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.getcwd())

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import yaml  # noqa: E402

from tools.analyze_22p_gap import _pooled  # noqa: E402
from tools.diagnose_pini_transition import gap_stats  # noqa: E402

ROOT = "results/_smoke/p2"
LEGS = {
    "L1": ("fit_L1_ocp", 0.0, 0.0),
    "L2": ("fit_L2_u5", 5.0, 0.0),
    "L3": ("fit_L3_u10", 10.0, 0.0),
    "L4": ("fit_L4_t5", 5.0, 10.0),
    "L5": ("fit_L5_t10", 10.0, 20.0),
    "L6": ("fit_L6_tilt10", 0.0, 10.0),
}
L0 = "fit_L0_grid"
OBJECTIVES = ("pocv_dvdq", "pocv_dvdq_dqdv")
Y_T, Y_B = 0.2699987322515213, 0.9260882648404596
Y_MIN, Y_MAX = 1e-4, 1 - 1e-4          # halfcell 표 y 구간 (np.linspace(1e-4, 1-1e-4))
A_NE_OK = (1.05, 1.08)
B = 10000
SEED = 20261006


def window(f, tol_eps: float):
    return f[(f["lli"] - 0.17).abs().le(0.02 + tol_eps)
             & (((f["lam_pe"] + f["lam_ne"]) / 2) - 0.13).abs().le(0.02 + tol_eps)]


def gap_stats_tol(f, tol):
    """gap_stats 와 같은 식 · 창 경계만 `<= 0.02 + 1e-9` (부동소수 허용 창)."""
    g = f[f["noise"] == 0].copy()
    g["true_gap"] = (g["lam_pe"] - g["lam_ne"]).abs()
    g["rec_gap"] = (g["lam_pe_hat"] - g["lam_ne_hat"]).abs()
    near = window(g, 1e-9)
    zero = near[near["true_gap"] <= 1e-9]
    signed = ((near["lam_pe_hat"] - near["lam_pe"]) - (near["lam_ne_hat"] - near["lam_ne"]))
    return {"n_near": int(len(near)), "n_gap0": int(len(zero)),
            "false_split": int((zero["rec_gap"] >= tol).sum()),
            "gap_bias_pp": round(100 * float(signed.mean()), 2) if len(near) else None}


def errs(f):
    return pd.DataFrame({
        "cond_id": f["cond_id"].values,
        "e_pe": (f["lam_pe_hat"] - f["lam_pe"]).values,
        "e_ne": (f["lam_ne_hat"] - f["lam_ne"]).values,
        "e_lli": (f["lli_hat"] - f["lli"]).values,
    }).assign(gap=lambda d: d["e_pe"] - d["e_ne"]).set_index("cond_id")


def boot_ci(x, rng):
    x = np.asarray(x, float)
    if len(x) == 0:
        return None
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = x[idx].mean(axis=1)
    return [round(100 * float(np.percentile(m, 2.5)), 3), round(100 * float(np.percentile(m, 97.5)), 3)]


def delta_mv(y, offset, tilt):
    yc = 0.5 * (Y_T + Y_B)
    return offset + tilt * np.clip((yc - y) / (Y_B - Y_T), -0.5, 0.5)


def delta_eff(a_pe, b_pe, offset, tilt):
    """조건의 동작 창 x∈[0,1] (셀 정규 용량) 위 용량-균일 평균 오프셋 (mV).
    y(x) = y_min + (y_max − y_min)·(x − b_pe)/a_pe — fitting 의 halfcell 정규화 역변환."""
    x = np.linspace(0.0, 1.0, 2001)
    y = Y_MIN + (Y_MAX - Y_MIN) * (x[None, :] - b_pe[:, None]) / a_pe[:, None]
    return delta_mv(y, offset, tilt).mean(axis=1)


def summarize(v):
    v = np.asarray(v, float)
    return {"mean": round(float(v.mean()), 4), "min": round(float(v.min()), 4),
            "max": round(float(v.max()), 4)} if len(v) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--legs", nargs="*", default=list(LEGS), help="분석할 다리 (중단 시 일부)")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)
    out = {"rules": __doc__, "y_T": Y_T, "y_B": Y_B, "bootstrap": {"B": B, "seed": SEED}, "objectives": {}}
    stops = []
    for obj in OBJECTIVES:
        ref = _pooled([__import__("pathlib").Path(ROOT) / L0], obj, 0.02, "--restrict-to")
        ref = ref[ref["noise"] == 0]
        pop = set(ref.loc[ref["recoverable"], "cond_id"])
        o = {"n_pop_L0_recoverable": len(pop), "legs": {}}
        frames, sets = {}, {}
        for name in args.legs:
            d, off, tilt = LEGS[name]
            p = f"{ROOT}/{d}"
            man = yaml.safe_load(open(f"{p}/manifest.yaml", encoding="utf-8")) or {}
            spec = man.get("run_spec") or {}
            p_ini = (spec.get("p_ini") or {}).get(obj)
            f = pd.read_parquet(f"{p}/fits.parquet")
            f = f[(f["objective"] == obj) & (f["noise"] == 0)]
            sets[name] = set(f["cond_id"])
            fp = f[f["cond_id"].isin(pop)]
            frames[name] = fp
            a_ne = float(p_ini[2]) if p_ini else None
            origin_ok = a_ne is not None and A_NE_OK[0] <= a_ne <= A_NE_OK[1]
            e = errs(fp)
            ew, ewt = errs(window(fp, 0.0)), errs(window(fp, 1e-9))
            leg = {
                "dir": p, "offset_mv": off, "tilt_mv": tilt,
                "recipe": spec.get("halfcell_recipe"), "source_digest": spec.get("source_digest"),
                "p_ini": [round(float(x), 4) for x in p_ini] if p_ini else None,
                "origin_a_ne": a_ne, "origin_ok": origin_ok,
                "n_noise0": int(len(f)), "n_pop": int(len(fp)),
                "gap_stats_strict": gap_stats(f[f["cond_id"].isin(pop)], 0.02),
                "gap_stats_tol": gap_stats_tol(f[f["cond_id"].isin(pop)], 0.02),
                "mean_err_pp_pop": {k: round(100 * float(e[k].mean()), 3) for k in e.columns},
                "mean_err_pp_window_strict": {k: round(100 * float(ew[k].mean()), 3) for k in ew.columns},
                "mean_err_pp_window_tol": {k: round(100 * float(ewt[k].mean()), 3) for k in ewt.columns},
                "n_window_strict": int(len(ew)), "n_window_tol": int(len(ewt)),
                "n_restarts_dist": {str(k): int(v) for k, v in fp["n_restarts"].value_counts().sort_index().items()},
                "n_restarts_mean": round(float(fp["n_restarts"].mean()), 3),
                "converged_frac": round(float(fp["converged"].mean()), 4),
            }
            o["legs"][name] = leg
            if name == "L1" and not origin_ok:
                stops.append(f"{obj}: L1 원점 a_ne={a_ne} ∉ {A_NE_OK} — 전체 중단")
            elif not origin_ok:
                stops.append(f"{obj}: {name} 원점 a_ne={a_ne} ∉ {A_NE_OK} — 오염 (권고 5: 세트 중단)")
        base = sets.get("L1")
        o["cond_sets_equal"] = all(s == base for s in sets.values())
        if not o["cond_sets_equal"]:
            stops.append(f"{obj}: 다리 간 cond_id 집합 불일치")
        # paired Δ vs L1 + δ_eff (L1 의 창 = 무왜곡 기준 fit 이 본 창)
        if "L1" in frames:
            e1 = errs(frames["L1"])
            f1 = frames["L1"].set_index("cond_id")
            for name in args.legs:
                if name == "L1":
                    continue
                d, off, tilt = LEGS[name]
                en = errs(frames[name])
                common = e1.index.intersection(en.index)
                dd = en.loc[common] - e1.loc[common]
                fn = frames[name].set_index("cond_id")
                wmask = {k: window(f1.loc[common].reset_index(), eps)["cond_id"] for k, eps in (("strict", 0.0), ("tol", 1e-9))}
                pd_ = {"n": int(len(common))}
                for scope, ids in (("pop", common), ("window_strict", pd.Index(wmask["strict"])),
                                   ("window_tol", pd.Index(wmask["tol"]))):
                    sub = dd.loc[ids]
                    pd_[scope] = {k: {"mean_pp": round(100 * float(sub[k].mean()), 3), "ci95_pp": boot_ci(sub[k], rng)}
                                  for k in ("e_pe", "e_ne", "e_lli", "gap")}
                    pd_[scope]["n"] = int(len(sub))
                leg = o["legs"][name]
                leg["paired_delta_vs_L1"] = pd_
                ids_w = pd.Index(wmask["strict"])
                leg["delta_eff_mv"] = {
                    "L1_window_pop": summarize(delta_eff(f1.loc[common, "a_pe"].values, f1.loc[common, "b_pe"].values, off, tilt)),
                    "L1_window_strict": summarize(delta_eff(f1.loc[ids_w, "a_pe"].values, f1.loc[ids_w, "b_pe"].values, off, tilt)),
                    "own_window_strict": summarize(delta_eff(fn.loc[ids_w, "a_pe"].values, fn.loc[ids_w, "b_pe"].values, off, tilt)),
                }
                gs, g1 = leg["gap_stats_strict"]["gap_bias_pp"], o["legs"]["L1"]["gap_stats_strict"]["gap_bias_pp"]
                gt, g1t = leg["gap_stats_tol"]["gap_bias_pp"], o["legs"]["L1"]["gap_stats_tol"]["gap_bias_pp"]
                leg["gap_bias_delta_pp"] = {"strict": None if gs is None else round(gs - g1, 2),
                                            "tol": None if gt is None else round(gt - g1t, 2)}
            if obj == "pocv_dvdq_dqdv":
                for name in ("L2", "L3"):
                    if name in o["legs"]:
                        dlt = o["legs"][name]["gap_bias_delta_pp"]["strict"]
                        if dlt is None or not dlt > 0:
                            stops.append(f"{obj}: {name} Δ 격차 bias (원 창) = {dlt} — + 부호 재현 실패 · tilt 해석 전 중단")
        out["objectives"][obj] = o
    out["stops"] = stops
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"stops": stops}, ensure_ascii=False))
    for obj, o in out["objectives"].items():
        print(f"== {obj} · pop {o['n_pop_L0_recoverable']} · cond 집합 같음 {o['cond_sets_equal']}")
        for n, L in o["legs"].items():
            print(f"  {n} a_ne={L['origin_a_ne']} ok={L['origin_ok']} n={L['n_pop']} "
                  f"bias strict/tol={L['gap_stats_strict']['gap_bias_pp']}/{L['gap_stats_tol']['gap_bias_pp']} "
                  f"Δ={L.get('gap_bias_delta_pp')} err_win={L['mean_err_pp_window_strict']} "
                  f"δeff={(L.get('delta_eff_mv') or {}).get('L1_window_strict')} restarts={L['n_restarts_mean']}")
    return 1 if stops else 0


if __name__ == "__main__":
    raise SystemExit(main())
