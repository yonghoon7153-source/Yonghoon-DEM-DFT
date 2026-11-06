#!/usr/bin/env python3
"""P3 운전 스크립트 — 논문 후속 (Phantom pOCV) · **진단 전용 · smoke · 인용 금지 · 정본 아님**.

승인: `followups/phantom-pocv/P3_APPROVAL_REQUEST.md` §4 · §7 · 실행 전 고정값 §8.
저장소 밖 사본 (`--copy`) 의 `src` 를 불러 쓴다 — 저장소 코드 · RUN_SCOPE 변경 0.
사본 패치는 `src/modes.py` 한 곳 (`build_overrides` 의 `lam_gr` · `lam_si`).

명령 (순서대로 · 단계마다 §5 중단 조건을 본다):
  curves   truth 곡선 61 (원점 1 · 격자 48 · 경로 12)        → out/curves.json
  f4       기존 4 매개 적합 (`_fit_one` 그대로)              → out/f4_rows.json   (원점 a_ne 검사)
  f5       γ_Si 자유 5 매개 (원점 · 격자)                    → out/f5_rows.json   (대조 γ̂ 검사)
  w        경로: 독립 restart 20 ↔ 앞 단계 해에서 warm 1   → out/w_rows.json
  s        Si 가지 mean · lithiation 기준 (격자 잡음 0)       → out/s_rows.json
  analyze  R1–R6 · 해석 규칙 §4-4                            → out/analysis.json · out/analysis.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

OBJECTIVES = ("pocv", "pocv_dvdq")
NOISES = (0.0, 0.001)
NOISE_SEED = 101
GAMMA_LB, GAMMA_UB = 0.0, 0.40
N_PROC = 4
SI_KEYS = {"delithiation": "Secondary: Negative electrode delithiation OCP [V]",
           "lithiation": "Secondary: Negative electrode lithiation OCP [V]",
           "mean": "Secondary: Negative electrode OCP [V]"}
STOP = 3                                   # §5 중단 조건 발동 종료 코드

# ---------------------------------------------------------------- 정의 (§2 고정)

def gamma0(cfg: dict) -> float:
    """기준 Si 몫 (용량) — halfcell.py 의 q_gr · q_si 와 같은 식."""
    b = cfg["baseline"]
    q_gr = float(b["ne_primary_max_conc"]) * float(b["ne_primary_vf"])
    q_si = float(b["ne_secondary_max_conc"]) * float(b["ne_secondary_vf"])
    return q_si / (q_gr + q_si)


def truth_of(c: dict, g0: float) -> dict:
    lgr, lsi = float(c["lam_gr"]), float(c["lam_si"])
    return {"lli": float(c["lli"]), "lam_pe": float(c["lam_pe"]),
            "lam_ne": (1 - g0) * lgr + g0 * lsi, "lam_gr": lgr, "lam_si": lsi,
            "gamma": g0 * (1 - lsi) / ((1 - g0) * (1 - lgr) + g0 * (1 - lsi)),
            "noise": float(c["noise"])}


def make_cond(set_: str, lli, lpe, lgr, lsi, nz, step=None) -> dict:
    key = f"{lli:.6f}|{lpe:.6f}|{lgr:.6f}|{lsi:.6f}|de|de|{nz:.6f}"
    seed = NOISE_SEED + int(hashlib.sha1(key.encode()).hexdigest()[:6], 16)
    c = {"lli": float(lli), "lam_pe": float(lpe), "lam_gr": float(lgr), "lam_si": float(lsi),
         "lam_pe_type": "de", "lam_ne_type": "de", "noise": float(nz), "seed": int(seed)}
    cid = hashlib.sha1(json.dumps(c, sort_keys=True).encode()).hexdigest()[:12]
    return {**c, "set": set_, "step": step, "cond_id": cid}


def all_conditions() -> list[dict]:
    out = [make_cond("origin", 0.0, 0.0, 0.0, 0.0, 0.0)]
    for lli in (0.05, 0.15):
        for lpe in (0.05, 0.15):
            for lgr in (0.05, 0.15):
                for lsi in (lgr, 0.30, 0.60):
                    for nz in NOISES:
                        out.append(make_cond("grid", lli, lpe, lgr, lsi, nz))
    for k in range(1, 7):
        for nz in NOISES:
            out.append(make_cond("path", round(0.02 * k, 6), round(0.01 * k, 6),
                                 round(0.01 * k, 6), round(0.1 * k, 6), nz, k))
    return out


# ---------------------------------------------------------------- 5 매개 음극 기준

def ne_blend_tables(cfg: dict, branch: str = "delithiation", n_points: int = 400) -> dict:
    """compute_halfcell_from_ocp 의 음극 부분 (src/halfcell.py 127–142) 과 같은 식.
    다른 점은 Gr · Si 무게를 고정하지 않고 밖으로 꺼낸다는 것뿐이다."""
    import pybamm

    from src.halfcell import _eval_ocp
    p = pybamm.ParameterValues(cfg["parameter_set"])
    x = np.linspace(1e-4, 1 - 1e-4, n_points)
    u_gr = _eval_ocp(p["Primary: Negative electrode OCP [V]"], x)
    u_si = _eval_ocp(p[SI_KEYS[branch]], x)
    u_grid = np.linspace(min(u_gr.min(), u_si.min()), max(u_gr.max(), u_si.max()), n_points * 2)
    x_gr = np.interp(u_grid, u_gr[::-1], x[::-1], left=1.0, right=0.0)
    x_si = np.interp(u_grid, u_si[::-1], x[::-1], left=1.0, right=0.0)
    return {"u_grid": u_grid, "x_gr": x_gr, "x_si": x_si, "branch": branch}


def ne_ref_interp(tab: dict, gamma: float):
    """z_γ = (1−γ) x_Gr + γ x_Si → build_reference_interps("halfcell") 음극 갈래 (fitting.py 656–661) 와 같은 식."""
    from src.fitting import make_ref_interp
    from src.halfcell import _dedupe_sorted
    z = (1.0 - gamma) * tab["x_gr"] + gamma * tab["x_si"]
    z_s, u_n = _dedupe_sorted(z, tab["u_grid"])
    s_ne = 1.0 - z_s
    s_ne = (s_ne - s_ne.min()) / (s_ne.max() - s_ne.min())
    order = np.argsort(s_ne)
    return make_ref_interp(s_ne[order], u_n[order])


def make_j5(target, ref_pe, tab, x, weights, scales, obj_cfg, x_lo, x_hi):
    from src.fitting import reconstruct, window_shortfall
    from src.objective import make_objective

    def model_fn(p):
        return x, reconstruct(p[:4], ref_pe, ne_ref_interp(tab, float(p[4])), x)[2]

    def shortfall(p):
        return window_shortfall(p[:4], x_lo, x_hi)

    return make_objective(target, model_fn, weights, scales, obj_cfg, shortfall)


def modes5(p, p_ini, r: float) -> dict:
    """§2 정의: LAM_X = 1 − Q_X / Q_X0 · Q_Si = γ̂ Q_NE · Q_Gr = (1 − γ̂) Q_NE · 원점은 같은 목적함수 · 같은 가지의 자기 적합 (F26)."""
    from src.fitting import to_modes_halfcell
    m = to_modes_halfcell(list(p[:4]), list(p_ini[:4]), r)
    a, g, a0, g0 = float(p[2]), float(p[4]), float(p_ini[2]), float(p_ini[4])
    m["lam_si"] = 1.0 - (g * a * r) / (g0 * a0)
    m["lam_gr"] = 1.0 - ((1.0 - g) * a * r) / ((1.0 - g0) * a0)
    m["gamma"] = g
    return m


# ---------------------------------------------------------------- 공통

G: dict = {}                                # fork 로 워커에 물려줄 문맥


def _jdump(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)),
                          encoding="utf-8")


def _cfgs(copy: Path):
    from src.config import load_config
    return load_config(copy / "configs" / "base.yaml"), load_config(copy / "configs" / "objectives.yaml")


def _seed(text: str) -> int:
    return int(hashlib.sha1(text.encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- curves

def _solve(c: dict) -> dict:
    from src.curves import add_noise, extract_curves
    from src.modes import Baseline, InfeasibleConditionError, build_overrides
    from src.runner import run_one
    cfg, d = G["cfg"], G["d"]
    b = Baseline.from_config(cfg)
    t = truth_of(c, G["g0"])
    try:
        ov = build_overrides(c["lli"], c["lam_pe"], t["lam_ne"], "de", "de", b, d, cfg.get("guards", {}),
                             lam_gr=c["lam_gr"], lam_si=c["lam_si"])
    except InfeasibleConditionError as e:
        return {**c, "error": f"infeasible: {e}"}
    res = run_one(cfg, ov, cfg.get("grid_protocol_override", "charge_first"))
    if not res.ok:
        return {**c, "error": str(res.error)}
    cur = extract_curves(res.solution, int(cfg["postprocess"]["n_trim"]), int(cfg["postprocess"]["n_interp"]))
    vn = add_noise(cur["v_full"], c["noise"], c["seed"])
    return {**c, "error": None, "elapsed_s": res.elapsed_s, "q_mah": cur["q_mah"],
            "x_norm": cur["x_norm"].tolist(), "v_pe": cur["v_pe"].tolist(), "v_ne": cur["v_ne"].tolist(),
            "v_full": cur["v_full"].tolist(), "v_full_noisy": vn.tolist()}


def cmd_curves(copy: Path, out: Path) -> int:
    from src.baseline import get_discharged_state
    cfg, _ = _cfgs(copy)
    G.update(cfg=cfg, d=get_discharged_state(cfg), g0=gamma0(cfg))
    conds = all_conditions()
    print(f"conditions {len(conds)} · gamma0 {G['g0']:.6f} · discharged {G['d']}", flush=True)
    with Pool(N_PROC) as pool:
        res = pool.map(_solve, conds)
    bad = [r for r in res if r.get("error")]
    _jdump(res, out / "curves.json")
    for r in bad:
        print(f"FAILED {r['set']} {r['cond_id']}: {r['error']}", flush=True)
    print(f"ok {len(res) - len(bad)} / {len(res)}", flush=True)
    return STOP if bad else 0


# ---------------------------------------------------------------- 공통 적합 문맥

def _ctx(copy: Path, out: Path) -> None:
    from src.halfcell import compute_halfcell_from_ocp
    cfg, obj_cfg = _cfgs(copy)
    curves = json.loads((out / "curves.json").read_text(encoding="utf-8"))
    origin = next(c for c in curves if c["set"] == "origin")
    G.update(cfg=cfg, obj_cfg=obj_cfg, curves=curves, origin=origin, g0=gamma0(cfg),
             hc=compute_halfcell_from_ocp(cfg, n_points=400, branch="delithiation").as_dict(),
             bounds=obj_cfg["fitting"]["bounds_presets"]["halfcell"],
             objectives={n: obj_cfg["objectives"][n] for n in OBJECTIVES}, tabs={})


def _f4_task(c: dict) -> dict:
    o, bd = G["origin"], G["bounds"]
    return {"cond_id": c["cond_id"], "x": np.asarray(c["x_norm"]), "v_target": np.asarray(c["v_full_noisy"]),
            "q_mah": c["q_mah"], "r": c["q_mah"] / o["q_mah"], "truth": {**truth_of(c, G["g0"]), "set": c["set"]},
            "ref_x": np.asarray(o["x_norm"]), "ref_pe": np.asarray(o["v_pe"]), "ref_ne": np.asarray(o["v_ne"]),
            "ref_full": np.asarray(o["v_full"]), "obj_cfg": G["obj_cfg"], "objectives": G["objectives"],
            "init": bd["init"], "lb": bd["lb"], "ub": bd["ub"], "bounds_preset": "halfcell", "n_restarts": 5,
            "inventory": {"w_pe": None, "w_ne": None, "kappa": None}, "reference": "halfcell",
            "halfcell": G["hc"], "p_ini": G.get("p_ini4"), "warm_start": True, "adaptive": True,
            "method": "Nelder-Mead", "seed": _seed(c["cond_id"])}


def _f4_one(c: dict) -> list:
    from src.fitting import _fit_one
    return _fit_one(_f4_task(c))


def cmd_f4(copy: Path, out: Path) -> int:
    from src.fitting import PARAM_NAMES, _fit_one
    _ctx(copy, out)
    ini_rows = _fit_one({**_f4_task(G["origin"]), "p_ini": [1.0, 0.0, 1.0, 0.0]})
    G["p_ini4"] = {r["objective"]: [float(r[k]) for k in PARAM_NAMES] for r in ini_rows}
    print("p_ini4", json.dumps(G["p_ini4"]), flush=True)
    todo = [c for c in G["curves"] if c["set"] in ("origin", "grid")]
    with Pool(N_PROC) as pool:
        rows = [r for rs in pool.map(_f4_one, todo) for r in rs]
    _jdump({"p_ini4": G["p_ini4"], "rows": rows}, out / "f4_rows.json")
    bad = {n: p[2] for n, p in G["p_ini4"].items() if not 1.05 <= p[2] <= 1.08}
    print(f"rows {len(rows)} · origin a_ne {json.dumps({n: round(p[2], 4) for n, p in G['p_ini4'].items()})}", flush=True)
    if bad:
        print(f"STOP §5: origin a_ne outside [1.05, 1.08]: {bad}", flush=True)
        return STOP
    return 0


# ---------------------------------------------------------------- 5 매개 적합

def _tab(branch: str) -> dict:
    if branch not in G["tabs"]:
        G["tabs"][branch] = ne_blend_tables(G["cfg"], branch=branch, n_points=400)
    return G["tabs"][branch]


def _f5_job(job: dict) -> list:
    """job = {cond, branch, n_restarts, init (목적함수별 또는 None), warm, tag}."""
    from src.fitting import build_reference_interps, fit
    from src.objective import compute_features, default_scales
    c, branch = job["cond"], job["branch"]
    o, bd, obj_cfg = G["origin"], G["bounds"], G["obj_cfg"]
    x = np.asarray(c["x_norm"])
    target = compute_features(x, np.asarray(c["v_full_noisy"]), obj_cfg, with_peaks=True)
    scales = default_scales(compute_features(np.asarray(o["x_norm"]), np.asarray(o["v_full"]), obj_cfg))
    ref_pe = build_reference_interps("halfcell", None, G["hc"])[0]
    obs = np.isfinite(target.v)
    lo, hi = float(x[obs].min()), float(x[obs].max())
    lb, ub = list(bd["lb"]) + [GAMMA_LB], list(bd["ub"]) + [GAMMA_UB]
    rows = []
    for name in OBJECTIVES:
        J = make_j5(target, ref_pe, _tab(branch), x, G["objectives"][name], scales, obj_cfg, lo, hi)
        init = (job["init"] or {}).get(name) or (list(bd["init"]) + [G["g0"]])
        t0 = time.perf_counter()
        res = fit(J, init, lb, ub, n_restarts=job["n_restarts"], seed=_seed(f"{c['cond_id']}|{branch}"),
                  method="Nelder-Mead", adaptive=False, warm_init=bool(job["warm"]))
        rows.append({"cond_id": c["cond_id"], "set": c["set"], "step": c["step"], "objective": name,
                     "branch": branch, "tag": job["tag"], "r": c["q_mah"] / o["q_mah"],
                     **truth_of(c, G["g0"]), "p": [float(v) for v in res.p], "J": float(res.J),
                     "n_eval": int(res.n_eval), "n_restarts": int(res.n_restarts),
                     "bound_active": list(res.bound_active), "init": [float(v) for v in init],
                     "restarts_json": json.dumps(res.restarts), "elapsed_s": time.perf_counter() - t0})
    return rows


def _origin_p_ini5(branch: str, tag: str) -> tuple[dict, list]:
    rows = _f5_job({"cond": G["origin"], "branch": branch, "n_restarts": 20, "init": None, "warm": False, "tag": tag})
    return {r["objective"]: r["p"] for r in rows}, rows


def cmd_f5(copy: Path, out: Path) -> int:
    _ctx(copy, out)
    _tab("delithiation")
    p_ini5, orows = _origin_p_ini5("delithiation", "F5_origin")
    print("p_ini5", json.dumps(p_ini5), flush=True)
    jobs = [{"cond": c, "branch": "delithiation", "n_restarts": 20 if c["noise"] == 0 else 5,
             "init": None, "warm": False, "tag": "F5"} for c in G["curves"] if c["set"] == "grid"]
    with Pool(N_PROC) as pool:
        rows = orows + [r for rs in pool.map(_f5_job, jobs) for r in rs]
    _jdump({"p_ini5": p_ini5, "rows": rows}, out / "f5_rows.json")
    g0 = G["g0"]
    ctrl = [r for r in rows if r["set"] == "grid" and r["noise"] == 0 and r["lam_si"] == r["lam_gr"]]
    off = [r for r in ctrl if abs(r["p"][4] - g0) > 0.01]
    print(f"rows {len(rows)} · control fits {len(ctrl)} · gamma off (>0.01) {len(off)}", flush=True)
    if len(off) > 0.10 * len(ctrl):
        print("STOP §5: control gamma outside gamma0 ± 0.01 in > 10 %: "
              + json.dumps([(r["cond_id"], r["objective"], round(r["p"][4], 4)) for r in off]), flush=True)
        return STOP
    return 0


def _w_chain(key: tuple) -> list:
    name, nz = key
    path = sorted([c for c in G["curves"] if c["set"] == "path" and c["noise"] == nz], key=lambda c: c["step"])
    prev = G["p_ini5"][name]
    rows = []
    for c in path:
        r = [x for x in _f5_job({"cond": c, "branch": "delithiation", "n_restarts": 1,
                                 "init": {n: prev for n in OBJECTIVES}, "warm": True, "tag": "W_warm"})
             if x["objective"] == name][0]
        rows.append(r)
        prev = r["p"]
    return rows


def cmd_w(copy: Path, out: Path) -> int:
    _ctx(copy, out)
    _tab("delithiation")
    G["p_ini5"] = json.loads((out / "f5_rows.json").read_text(encoding="utf-8"))["p_ini5"]
    cold = [{"cond": c, "branch": "delithiation", "n_restarts": 20, "init": None, "warm": False, "tag": "W_cold"}
            for c in G["curves"] if c["set"] == "path"]
    with Pool(N_PROC) as pool:
        rows = [r for rs in pool.map(_f5_job, cold) for r in rs]
        rows += [r for rs in pool.map(_w_chain, [(n, nz) for n in OBJECTIVES for nz in NOISES]) for r in rs]
    _jdump({"rows": rows}, out / "w_rows.json")
    print(f"rows {len(rows)}", flush=True)
    return 0


def cmd_s(copy: Path, out: Path) -> int:
    _ctx(copy, out)
    res = {"p_ini5": {}, "rows": []}
    for branch in ("mean", "lithiation"):
        _tab(branch)
        p_ini, orows = _origin_p_ini5(branch, f"S_origin_{branch}")
        res["p_ini5"][branch] = p_ini
        jobs = [{"cond": c, "branch": branch, "n_restarts": 5, "init": None, "warm": False, "tag": f"S_{branch}"}
                for c in G["curves"] if c["set"] == "grid" and c["noise"] == 0]
        with Pool(N_PROC) as pool:
            res["rows"] += orows + [r for rs in pool.map(_f5_job, jobs) for r in rs]
        print(f"branch {branch} · p_ini5 {json.dumps(p_ini)}", flush=True)
    _jdump(res, out / "s_rows.json")
    print(f"rows {len(res['rows'])}", flush=True)
    return 0


# ---------------------------------------------------------------- analyze

def _corr(a, b) -> float | None:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def cmd_analyze(copy: Path, out: Path) -> int:
    import pandas as pd

    from src.fitting import to_modes_halfcell
    from src.scoring import multistart_diagnostics
    cfg, _ = _cfgs(copy)
    g0 = gamma0(cfg)
    f4 = json.loads((out / "f4_rows.json").read_text(encoding="utf-8"))
    f5 = json.loads((out / "f5_rows.json").read_text(encoding="utf-8"))
    A: dict = {"gamma0": g0, "notes": "진단 전용 · smoke · 인용 금지 · 정본 아님"}
    pp = lambda v: round(100.0 * float(v), 3)          # noqa: E731  — %p

    # R1 — F4 편향
    r1 = []
    for r in f4["rows"]:
        if r.get("set") != "grid":
            continue
        e = {k: r[f"{k}_hat"] - r[k] for k in ("lam_pe", "lam_ne", "lli")}
        r1.append({"objective": r["objective"], "noise": r["noise"], "dlam": round(r["lam_si"] - r["lam_gr"], 6),
                   **{f"err_{k}_pp": pp(v) for k, v in e.items()},
                   "fail_2pp": bool(max(abs(v) for v in e.values()) > 0.02)})
    d1 = pd.DataFrame(r1)
    A["R1_f4_mean_err_by_dlam"] = (d1.groupby(["objective", "noise", "dlam"])
                                   [["err_lam_pe_pp", "err_lam_ne_pp", "err_lli_pp"]].mean().round(3)
                                   .reset_index().to_dict("records"))
    A["R1_f4_fail_2pp"] = d1.groupby(["objective", "noise"])["fail_2pp"].agg(["sum", "count"]).reset_index().to_dict("records")

    # R2 — F5 복원
    p5 = f5["p_ini5"]
    r2 = []
    for r in f5["rows"]:
        if r["set"] != "grid":
            continue
        m = modes5(r["p"], p5[r["objective"]], r["r"])
        e = {"lam_pe": m["lam_pe"] - r["lam_pe"], "lli": m["lli"] - r["lli"],
             "lam_gr": m["lam_gr"] - r["lam_gr"], "lam_si": m["lam_si"] - r["lam_si"]}
        r2.append({"cond_id": r["cond_id"], "objective": r["objective"], "noise": r["noise"],
                   "dlam": round(r["lam_si"] - r["lam_gr"], 6), "gamma_true": r["gamma"], "gamma_hat": m["gamma"],
                   "err_gamma": m["gamma"] - r["gamma"], **{f"err_{k}_pp": pp(v) for k, v in e.items()},
                   "err_lam_ne_tot_pp": pp(m["lam_ne"] - r["lam_ne"]),
                   "neg_component": bool(m["lam_gr"] < 0 or m["lam_si"] < 0),
                   "fail_2pp": bool(max(abs(v) for v in e.values()) > 0.02), "J": r["J"]})
    d2 = pd.DataFrame(r2)
    A["R2_f5_mean_abs_err_by_dlam"] = (d2.assign(**{c: d2[c].abs() for c in d2.columns if c.startswith("err_")})
                                       .groupby(["objective", "noise", "dlam"])
                                       [["err_lam_pe_pp", "err_lli_pp", "err_lam_gr_pp", "err_lam_si_pp", "err_gamma"]]
                                       .mean().round(4).reset_index().to_dict("records"))
    A["R2_f5_fail_2pp"] = d2.groupby(["objective", "noise"])["fail_2pp"].agg(["sum", "count"]).reset_index().to_dict("records")
    A["R2_f5_negative_component"] = d2.groupby(["objective", "noise"])["neg_component"].agg(["sum", "count"]).reset_index().to_dict("records")

    # R3 — 다중 시작 진단 (잡음 0 · restart 20)
    rows0 = [r for r in f5["rows"] if r["set"] == "grid" and r["noise"] == 0]
    ms = multistart_diagnostics(pd.DataFrame([{**r, "lam_ne": r["lam_ne"]} for r in rows0]))
    A["R3_multistart_kind"] = ms.groupby(["objective", "multistart_kind"]).size().reset_index(name="n").to_dict("records")
    r3 = []
    for r in rows0:
        rs = json.loads(r["restarts_json"])
        js = np.array([d["J"] for d in rs]); ps = np.array([d["p"] for d in rs])
        near = np.abs(js - js.min()) <= 1e-3 * max(1.0, abs(js.min()))
        gam, ane = ps[near, 4], ps[near, 2]
        lli_n = [to_modes_halfcell(list(p[:4]), list(p5[r["objective"]][:4]), r["r"])["lli"] for p in ps[near]]
        r3.append({"cond_id": r["cond_id"], "objective": r["objective"], "dlam": round(r["lam_si"] - r["lam_gr"], 6),
                   "n_near": int(near.sum()), "gamma_spread_near": float(gam.max() - gam.min()),
                   "corr_gamma_ane": _corr(gam, ane), "corr_gamma_lli": _corr(gam, lli_n)})
    A["R3_near_optimal"] = r3

    # R4 — 목적값 개선 vs 잡음
    j4 = {(r["cond_id"], r["objective"]): r["J"] for r in f4["rows"]}
    key = lambda r: (r["lli"], r["lam_pe"], r["lam_gr"], r["lam_si"], r["objective"])   # noqa: E731
    by_truth: dict = {}
    for r in f5["rows"]:
        if r["set"] == "grid":
            by_truth.setdefault(key(r), {})[r["noise"]] = r
    r4 = []
    for k, d in by_truth.items():
        if 0.0 in d and 0.001 in d:
            r0, r1n = d[0.0], d[0.001]
            r4.append({"objective": k[4], "dlam": round(k[3] - k[2], 6),
                       "dJ_model_noise0": j4[(r0["cond_id"], k[4])] - r0["J"],
                       "dJ_noise_f5": r1n["J"] - r0["J"],
                       "abs_err_gamma_noise0": abs(modes5(r0["p"], p5[k[4]], r0["r"])["gamma"] - r0["gamma"])})
    A["R4_rows"] = r4
    d4 = pd.DataFrame(r4)
    A["R4_corr_dJmodel_absdlam"] = {o: _corr(g["dJ_model_noise0"], g["dlam"].abs())
                                     for o, g in d4.groupby("objective")}
    A["R4_corr_dJmodel_errgamma"] = {o: _corr(g["dJ_model_noise0"], g["abs_err_gamma_noise0"])
                                      for o, g in d4.groupby("objective")}

    # §4-4 해석 규칙 (잡음 0)
    rule = {}
    for o in OBJECTIVES:
        sub = d2[(d2["objective"] == o) & (d2["noise"] == 0)]
        k = ms[ms["objective"] == o]
        rule[o] = {"frac_all4_within_2pp": float((~sub["fail_2pp"]).mean()),
                   "frac_unique_min": float((k["multistart_kind"] == "unique_min").mean()),
                   "claim_allowed": bool((~sub["fail_2pp"]).mean() >= 0.9
                                         and (k["multistart_kind"] == "unique_min").mean() >= 0.9)}
    A["rule_4_4"] = rule

    # R5 — warm ↔ cold
    if (out / "w_rows.json").exists():
        w = json.loads((out / "w_rows.json").read_text(encoding="utf-8"))["rows"]
        cold = {(r["cond_id"], r["objective"]): r for r in w if r["tag"] == "W_cold"}
        r5 = []
        for r in w:
            if r["tag"] != "W_warm":
                continue
            cr = cold[(r["cond_id"], r["objective"])]
            mw, mc = modes5(r["p"], p5[r["objective"]], r["r"]), modes5(cr["p"], p5[r["objective"]], cr["r"])
            r5.append({"objective": r["objective"], "noise": r["noise"], "step": r["step"],
                       "max_abs_dp": float(np.max(np.abs(np.subtract(r["p"], cr["p"])))),
                       "J_warm_minus_cold": r["J"] - cr["J"], "gamma_true": r["gamma"],
                       "gamma_warm": mw["gamma"], "gamma_cold": mc["gamma"],
                       "err_lam_si_pp_warm": pp(mw["lam_si"] - r["lam_si"]),
                       "err_lam_si_pp_cold": pp(mc["lam_si"] - cr["lam_si"]),
                       "err_lam_gr_pp_warm": pp(mw["lam_gr"] - r["lam_gr"]),
                       "err_lam_gr_pp_cold": pp(mc["lam_gr"] - cr["lam_gr"])})
        A["R5_warm_vs_cold"] = r5

    # R6 — Si 가지 순위
    if (out / "s_rows.json").exists():
        s = json.loads((out / "s_rows.json").read_text(encoding="utf-8"))
        allp = {"delithiation": p5, **s["p_ini5"]}
        pool_rows = [r for r in rows0] + [r for r in s["rows"] if r["set"] == "grid"]
        by: dict = {}
        for r in pool_rows:
            m = modes5(r["p"], allp[r["branch"]][r["objective"]], r["r"])
            err = max(abs(m[k] - r[k]) for k in ("lam_pe", "lli", "lam_gr", "lam_si"))
            by.setdefault((r["cond_id"], r["objective"]), {})[r["branch"]] = (r["J"], err)
        agree, n, r6 = 0, 0, []
        for (cid, o), d in by.items():
            if len(d) == 3:
                n += 1
                bj = min(d, key=lambda b: d[b][0]); be = min(d, key=lambda b: d[b][1])
                agree += int(bj == be)
                r6.append({"cond_id": cid, "objective": o, "best_by_J": bj, "best_by_err": be,
                           **{f"J_{b}": d[b][0] for b in d}, **{f"maxerr_pp_{b}": pp(d[b][1]) for b in d}})
        A["R6_rank_agreement"] = {"n": n, "argminJ_equals_argminErr": agree}
        A["R6_rows"] = r6

    _jdump(A, out / "analysis.json")
    print(json.dumps({k: A[k] for k in ("rule_4_4", "R1_f4_fail_2pp", "R2_f5_fail_2pp", "R3_multistart_kind")},
                     ensure_ascii=False, default=str), flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["curves", "f4", "f5", "w", "s", "analyze"])
    ap.add_argument("--copy", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    copy, out = Path(a.copy).resolve(), Path(a.out).resolve()
    sys.path.insert(0, str(copy))
    os.chdir(copy)
    out.mkdir(parents=True, exist_ok=True)
    return {"curves": cmd_curves, "f4": cmd_f4, "f5": cmd_f5, "w": cmd_w, "s": cmd_s,
            "analyze": cmd_analyze}[a.cmd](copy, out)


if __name__ == "__main__":
    sys.exit(main())
