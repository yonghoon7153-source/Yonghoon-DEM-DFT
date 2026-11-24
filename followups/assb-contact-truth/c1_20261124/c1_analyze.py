"""C1 후처리 — z 지도 · MC 특징 규칙 · 판정 · f* · 일반 문장 · 서명 표 · C1b 재현 · 첫 충전 상한 (설계서 §4-2 · §5-4–§5-6 · §8-5).
진단 전용 · 인용 금지 · 정본 아님.

사용: python -I c1_analyze.py <failcheck|c1a|c1b|ad> --out <grid out dir> --spk <spike dir> --csv <저장소 요약 csv 폴더>
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(os.environ["C1_COPY"]).resolve()))
sys.path.insert(0, str(HERE))

import c1_observe as ob  # noqa: E402
import c1_truth as tr  # noqa: E402

F_K = [2.0 ** (-k / 4) for k in range(9)]
LOGF = np.log(np.array(F_K))
REP_K = (2, 4, 8)
SOCS = (0.8, 0.5, 0.2)
PULSES = [(s, amp, sgn) for s in SOCS for amp in ("lin", "taf") for sgn in ("+", "-")]
DTS = (1e-4, 1e-3, 1e-2, 1e-1, 1.0)
SIGS = (1e-4, 1e-3)
DR0S = ("none", "free")
M = 20
Z_SEP, Z_LOW, K_SIG, FRAC = 5.0, 2.0, 3.0, 0.9      # §5-5 (D5 그대로)
PLANNED = 165
K_ALL = tuple(range(9))                              # C1a f 격자 지표 (0 = 신품)
SHAPES = tr.SHAPES
WAS = (10.0, 0.1)
FA_LV = (1.0, 0.8, 0.6, 0.4)
FK_LV = (1.0, 0.7, 0.5, 0.35, 0.25)


def jdump(obj, path):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)
    Path(path).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=conv))


def wcsv(path, rows):
    if not rows:
        Path(path).write_text("")
        return
    keys = list(rows[0].keys())
    for r in rows[1:]:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})


def reg(spk):
    return json.loads((Path(spk) / "s6_registered.json").read_text())


# --------------------------------------------------------------------------------------------
# 규칙 6 — 해법 실패 비율 (계획 165 대비)
# --------------------------------------------------------------------------------------------
def failcheck(a):
    out = Path(a.out)
    n_fail, n_done = 0, 0
    for p in list(out.glob("c1a/*_summary.json")) + list(out.glob("c1b/c1b_Wa*.json")):
        d = json.loads(p.read_text())
        n_fail += d.get("n_fail", 0)
        n_done += len(d.get("runs", d.get("rows", [])))
    p = out / "dc" / "dc_runs.json"
    if p.exists():
        d = json.loads(p.read_text())
        n_fail += d.get("n_fail", 0)
    p = out / "conv" / "conv.json"
    frac = n_fail / PLANNED
    print(f"failcheck: solver failures {n_fail} / planned {PLANNED} = {frac:.3%} (limit 5 %) · rows {n_done}")
    return 3 if frac > 0.05 else 0


# --------------------------------------------------------------------------------------------
# C1a
# --------------------------------------------------------------------------------------------
def obs_index(dt_obs, n_pulse):
    tp = tr.grid_after_step(10.0)
    trs = tr.grid_after_step(60.0)
    ip = ob.observe_indices(tp, dt_obs)
    ip = ip[tp[ip] > 0]
    ir = ob.observe_indices(trs, dt_obs)
    ir = ir[trs[ir] > 0]
    return tp, ip, ir, np.concatenate([ip, n_pulse + ir])


def load_cell(out, shape, Wa, arms=("A", "K")):
    V = {}
    f0 = np.load(out / "c1a" / f"{shape}_Wa{Wa:g}_fresh_k0.npz")
    n_pulse = int(f0["n_pulse"])
    for arm in arms:
        V[(arm, 0)] = f0["V"]
        folder = "c1a" if arm in ("A", "K") else "ad_c1a"
        for k in K_ALL[1:]:
            V[(arm, k)] = np.load(out / folder / f"{shape}_Wa{Wa:g}_{arm}_k{k}.npz")["V"]
    return V, n_pulse


def mc_task(task):
    """한 (칸 · k · Δt · σ_V) 의 M = 20 실현 × 팔 둘 F1 τ̂ (§5-5 규칙 2 · §8-5)."""
    (key, t_win, vA, vK, V0, I, dt_obs, sig) = task
    taus = {}
    for arm, v in (("A", vA), ("K", vK)):
        tl = []
        for m in range(M):
            seed = tr.seed_for(f"{key}|{arm}|m{m}")
            vn = ob.noisy(np.concatenate([[V0], v]), sig, seed)
            r = ob.fit_f1(t_win, vn[1:], I=I, V0=float(vn[0]), dt=dt_obs)
            tl.append(r["tau"])
        taus[arm] = np.array(tl, float)
    ta, tk = taus["A"], taus["K"]
    n_nan = int(np.isnan(ta).sum() + np.isnan(tk).sum())
    if n_nan:
        return key, {"n_nan": n_nan, "med_A": np.nan, "med_K": np.nan, "sd_A": np.nan, "sd_K": np.nan, "pass": False}
    mA, mK = float(np.median(ta)), float(np.median(tk))
    sA, sK = float(np.std(ta, ddof=1)), float(np.std(tk, ddof=1))
    return key, {"n_nan": 0, "med_A": mA, "med_K": mK, "sd_A": sA, "sd_K": sK,
                 "pass": bool(abs(mA - mK) >= K_SIG * max(sA, sK))}


def verdict(z, fpass):
    if z < Z_LOW:
        return "못 가른다"
    if z >= Z_SEP and fpass:
        return "가른다"
    return "경계"


def analyze_c1a(a, arms=("A", "K"), tag="c1a", do_mc=True):
    t0 = time.time()
    R = reg(a.spk)
    out = Path(a.out)
    csvd = Path(a.csv)
    csvd.mkdir(parents=True, exist_ok=True)
    S5 = json.loads((Path(a.spk) / "s5p.json").read_text())
    regflag = {(sh, s): (s in [str(x) for x in S5["shapes"][sh]["soc_points_flag_reg_gt_1e-3"]])
               for sh in tr.SHAPES for s in map(str, SOCS)}
    zrows, mc_tasks, sig_rows, meta = [], [], [], {}
    zstore = {}
    armA, armK = arms
    logf = np.log(np.array([F_K[k] for k in K_ALL]))
    for shape in SHAPES:
        for Wa in WAS:
            V, n_pulse = load_cell(out, shape, Wa, arms=arms)
            for j, (s, amp, sgn) in enumerate(PULSES):
                x = R["soc_x"][str(s)]
                I = R["pulse_I_A"][amp + sgn]
                w = R["W_fit_s"][f"{shape}|SOC{s}"]
                cell = f"{shape}|Wa{Wa:g}|SOC{s}|{amp}{sgn}"
                for dt_obs in DTS:
                    tp, ip, ir, idx = obs_index(dt_obs, n_pulse)
                    i_t = np.concatenate([np.full(ip.size, I), np.zeros(ir.size)])
                    famA = np.array([V[(armA, k)][j][idx] for k in K_ALL])
                    famK = np.array([V[(armK, k)][j][idx] for k in K_ALL])
                    for dr in DR0S:
                        for ii, k in enumerate(K_ALL):
                            z1 = ob.z_cell(famA, famK, logf, idx=ii, i_t=i_t, sigma=1.0, dR0=dr)
                            for sig in SIGS:
                                zstore[(cell, k, dt_obs, sig, dr)] = z1 / sig
                                zrows.append({"cell": cell, "k": k, "dt_s": dt_obs, "sigma_V": sig, "dR0": dr, "z": z1 / sig})
                    # MC 과제 (대표 f 셋)
                    iw = ip[(tp[ip] >= dt_obs - 1e-12) & (tp[ip] <= w + 1e-12)]
                    for k in REP_K:
                        for sig in SIGS:
                            key = f"{tag}|{cell}|k{k}|dt{dt_obs:g}|sv{sig:g}"
                            mc_tasks.append((key, tp[iw], V[(armA, k)][j][iw], V[(armK, k)][j][iw], tr.ocp(x), I, dt_obs, sig))
                # 서명 표 (잡음 0 · truth Δt)
                tp, ip, ir, idx = obs_index(1e-4, n_pulse)
                iw = ip[(tp[ip] >= 1e-4 - 1e-12) & (tp[ip] <= w + 1e-12)]
                feats = {}
                for arm in arms:
                    for k in (0,) + REP_K:
                        feats[(arm, k)] = ob.fit_f1(tp[iw], V[(arm, k)][j][iw], I=I, V0=tr.ocp(x), dt=1e-4)
                for k in (0,) + REP_K:
                    row = {"cell": cell, "shape": shape, "Wa": Wa, "soc": s, "x": x, "amp": amp, "dir": sgn, "k": k, "f": F_K[k],
                           "W_fit_s": w, "reg_flag": regflag[(shape, str(s))]}
                    for nm in ("R0", "Rp", "tau", "C", "k", "Rp_over_k"):
                        for arm in arms:
                            v0 = feats[(arm, 0)][nm]
                            vk = feats[(arm, k)][nm]
                            row[f"{arm}_{nm}"] = vk
                            row[f"{arm}_{nm}_ratio"] = vk / v0 if (v0 and np.isfinite(v0)) else np.nan
                        row[f"AoverK_{nm}"] = (feats[(armA, k)][nm] / feats[(armK, k)][nm]) if feats[(armK, k)][nm] else np.nan
                    sig_rows.append(row)
    wcsv(csvd / f"{tag}_zmap.csv", zrows)
    wcsv(csvd / f"{tag}_signature.csv", sig_rows)
    meta["t_z_s"] = time.time() - t0
    print(f"{tag}: z rows {len(zrows)} · signature rows {len(sig_rows)} · MC tasks {len(mc_tasks)} · {meta['t_z_s']:.0f}s", flush=True)
    if not do_mc:
        jdump(meta, csvd / f"{tag}_meta.json")
        return 0
    t1 = time.time()
    with Pool(4) as pool:
        mc = dict(pool.map(mc_task, mc_tasks, chunksize=8))
    meta["t_mc_s"] = time.time() - t1
    mc_rows, vrows, fstar_rows, gen_rows = [], [], [], []
    for key, v in mc.items():
        mc_rows.append({"key": key, **v})
    for shape in SHAPES:
        for Wa in WAS:
            for j, (s, amp, sgn) in enumerate(PULSES):
                cell = f"{shape}|Wa{Wa:g}|SOC{s}|{amp}{sgn}"
                for dt_obs in DTS:
                    for sig in SIGS:
                        for dr in DR0S:
                            best = None
                            for k in REP_K:
                                z = zstore[(cell, k, dt_obs, sig, dr)]
                                fm = mc[f"{tag}|{cell}|k{k}|dt{dt_obs:g}|sv{sig:g}"]
                                vd = verdict(z, fm["pass"])
                                vrows.append({"cell": cell, "shape": shape, "Wa": Wa, "soc": s, "amp": amp, "dir": sgn,
                                              "k": k, "f": F_K[k], "dt_s": dt_obs, "sigma_V": sig, "dR0": dr, "z": z,
                                              "feature_pass": fm["pass"], "n_nan": fm["n_nan"], "verdict": vd,
                                              "reg_flag": regflag[(shape, str(s))]})
                                if vd == "가른다" and (best is None or F_K[k] > best):
                                    best = F_K[k]
                            fstar_rows.append({"cell": cell, "shape": shape, "Wa": Wa, "soc": s, "amp": amp, "dir": sgn,
                                               "dt_s": dt_obs, "sigma_V": sig, "dR0": dr,
                                               "f_star": best if best is not None else ""})
    for dt_obs in DTS:
        for sig in SIGS:
            for dr in DR0S:
                vs = [r for r in vrows if r["k"] == 4 and r["dt_s"] == dt_obs and r["sigma_V"] == sig and r["dR0"] == dr]
                n_sep = sum(r["verdict"] == "가른다" for r in vs)
                n_bd = sum(r["verdict"] == "경계" for r in vs)
                frac = n_sep / len(vs)
                gen_rows.append({"dt_s": dt_obs, "sigma_V": sig, "dR0": dr, "n_cells": len(vs), "n_separate": n_sep,
                                 "n_boundary": n_bd, "n_cannot": len(vs) - n_sep - n_bd, "frac_separate": frac,
                                 "sentence_allowed": bool(frac >= FRAC),
                                 "reg_condition": any(r["reg_flag"] for r in vs)})
    wcsv(csvd / f"{tag}_mc.csv", mc_rows)
    wcsv(csvd / f"{tag}_verdicts.csv", vrows)
    wcsv(csvd / f"{tag}_fstar.csv", fstar_rows)
    wcsv(csvd / f"{tag}_general.csv", gen_rows)
    meta["n_mc_fits"] = len(mc_tasks) * 2 * M
    jdump(meta, csvd / f"{tag}_meta.json")
    print(f"{tag}: MC {len(mc_tasks)} tasks ({meta['n_mc_fits']} fits) {meta['t_mc_s']:.0f}s")
    for g in gen_rows:
        print(f"  Δt {g['dt_s']:g} σ {g['sigma_V']:g} ΔR0 {g['dR0']}: 가른다 {g['n_separate']}/48 · 경계 {g['n_boundary']} · "
              f"못 {g['n_cannot']} → 일반 문장 {'허용' if g['sentence_allowed'] else '불가'}")
    return 0


# --------------------------------------------------------------------------------------------
# 예상 대조 (§5-4 표 — Wa ≫ 1 · 선형 극한) · DC 특징
# --------------------------------------------------------------------------------------------
PRED = {"A": {"R0": lambda f: 1, "Rp": lambda f: 1 / f, "tau": lambda f: 1, "C": lambda f: f, "k": lambda f: 1,
              "Rp_over_k": lambda f: 1 / f},
        "K": {"R0": lambda f: 1, "Rp": lambda f: 1 / f, "tau": lambda f: 1 / f, "C": lambda f: 1, "k": lambda f: 1,
              "Rp_over_k": lambda f: 1 / f}}


def expectation(a, tag="c1a"):
    csvd = Path(a.csv)
    rows = list(csv.DictReader(open(csvd / f"{tag}_signature.csv")))
    outr = []
    for arm in ("A", "K"):
        for nm in PRED[arm]:
            for Wa in ("10", "0.1"):
                for amp in ("lin", "taf"):
                    sel = [r for r in rows if r["Wa"] in (Wa, Wa + ".0") and r["amp"] == amp and r["k"] != "0"]
                    devs = []
                    for r in sel:
                        f = float(r["f"])
                        obs = float(r[f"{arm}_{nm}_ratio"]) if r[f"{arm}_{nm}_ratio"] not in ("", "nan") else np.nan
                        devs.append(obs / PRED[arm][nm](f) - 1)
                    devs = np.array(devs, float)
                    outr.append({"arm": arm, "feature": nm, "Wa": Wa, "amp": amp, "n": int(devs.size),
                                 "max_abs_rel_dev_from_prediction": float(np.nanmax(np.abs(devs))) if devs.size else np.nan,
                                 "median_rel_dev": float(np.nanmedian(devs)) if devs.size else np.nan})
    wcsv(csvd / f"{tag}_expectation.csv", outr)
    return outr


def dc_features(a):
    out = Path(a.out)
    csvd = Path(a.csv)
    d = json.loads((out / "dc" / "dc_runs.json").read_text())
    z = json.loads((out / "dc" / "dc_z.json").read_text())
    rows = []
    fresh = {(r["Wa"], r["rate"]): r for r in d["runs"] if r["arm"] == "fresh"}
    for r in d["runs"]:
        fr = fresh[(r["Wa"], r["rate"])]
        rows.append({"run": r["run"], "Wa": r["Wa"], "arm": r["arm"], "k": r["k"], "rate": r["rate"], "status": r["status"],
                     "Q_Ah": r["Q_Ah"], "Q_ratio": (r["Q_Ah"] / fr["Q_Ah"]) if fr["Q_Ah"] else np.nan,
                     "mean_overpotential_V": r.get("mean_overpotential_V"), "dqdv_peak_V": r.get("dqdv_peak_V"),
                     "li_rel": r.get("li_rel")})
    wcsv(csvd / "dc_features.csv", rows)
    wcsv(csvd / "dc_z_qf_decision.csv", z["z_rows_qf_decision"])
    wcsv(csvd / "dc_z_time_diagnostic.csv", z["z_rows_time_diagnostic"])
    return rows


# --------------------------------------------------------------------------------------------
# C1b (§5-6)
# --------------------------------------------------------------------------------------------
def analyze_c1b(a, tag="c1b", mode="off"):
    out = Path(a.out)
    csvd = Path(a.csv)
    rows = []
    for Wa in WAS:
        p = out / tag / f"c1b_Wa{Wa:g}.json"
        rows += [r for r in json.loads(p.read_text())["rows"]]
    res_rows, summary = [], {}
    for Wa in WAS:
        rr = [r for r in rows if r["Wa"] == Wa and r["status"] == "ok"]
        ref = [r for r in rr if r["f_A"] == 1.0 and r["f_k"] == 1.0 and r["f_sigma"] == 1.0 and r["theta"] == 1.0][0]
        refd = {"Rp": ref["Rp"], "gitt_ratio": ref["gitt_ratio"], "Qdis": ref["Q_dis_Ah"], "Qch": ref["Q_ch_Ah"]}
        S = []
        for r in rr:
            o = ob.c1b_observables(refd, {"Rp": r["Rp"], "gitt_ratio": r["gitt_ratio"], "Qdis": r["Q_dis_Ah"], "Qch": r["Q_ch_Ah"]})
            inb = {kk: bool(ob.BANDS[kk][0] <= o[kk] <= ob.BANDS[kk][1]) for kk in ob.BANDS}
            rep = all(inb.values())
            dq = ref["Q_dis_Ah"] - r["Q_dis_Ah"]
            o5 = ob.first_charge_bound(Qch_ref=ref["Q_ch_Ah"], Qch_var=r["Q_ch_Ah"], Qdis_ref=ref["Q_dis_Ah"],
                                       Qdis_var=r["Q_dis_Ah"]) if dq != 0 else np.nan
            share = np.nan
            if r["theta"] < 1.0:
                twin = [q for q in rr if q["theta"] == 1.0 and q["f_A"] == r["f_A"] and q["f_k"] == r["f_k"]
                        and q["f_sigma"] == r["f_sigma"]]
                if twin and dq != 0:
                    share = ob.true_theta_share(Qdis_theta1=twin[0]["Q_dis_Ah"], Qdis_theta=r["Q_dis_Ah"], Qdis_ref=ref["Q_dis_Ah"])
            row = {"run": r["run"], "Wa": Wa, "f_A": r["f_A"], "f_k": r["f_k"], "p": r["p"], "f_sigma": r["f_sigma"],
                   "theta": r["theta"], **o, **{f"in_{kk}": v for kk, v in inb.items()}, "reproduces": rep,
                   "O5_bound": o5, "true_theta_share": share,
                   "bound_holds": (bool(o5 >= share) if (np.isfinite(o5) and np.isfinite(share)) else ""),
                   "looseness": (o5 - share) if (np.isfinite(o5) and np.isfinite(share)) else np.nan,
                   "Q_ch_Ah": r["Q_ch_Ah"], "Q_dis_Ah": r["Q_dis_Ah"], "gitt_ratio": r["gitt_ratio"], "Rp": r["Rp"]}
            res_rows.append(row)
            if rep:
                S.append(row)
        blocked = [kk for kk in ob.BANDS if not any(rw[f"in_{kk}"] for rw in res_rows if rw["Wa"] == Wa)]
        th1 = [rw for rw in res_rows if rw["Wa"] == Wa and rw["theta"] == 1.0 and np.isfinite(rw["O5_bound"])]
        th096 = [rw for rw in res_rows if rw["Wa"] == Wa and rw["theta"] < 1.0 and rw["bound_holds"] != ""]
        if mode == "off":
            reading = ("1D 균질 truth (AD 끔) 로 65호 80 wt% 모양 재현 불가" if not S else
                       "곱 p 로만 재현 — f_A · f_k 짝은 구성상 비식별")
        else:
            if not S:
                reading = "재현 불가"
            else:
                fa_lv, fk_lv = list(FA_LV), list(FK_LV)
                ij = [(fa_lv.index(s_["f_A"]), fk_lv.index(s_["f_k"])) for s_ in S]
                far = any(abs(p_[0] - q_[0]) > 1 or abs(p_[1] - q_[1]) > 1 for p_ in ij for q_ in ij)
                reading = "짝 비식별 (이 표적 넷으로)" if far else "격자 해상도 안에서 유일"
        summary[str(Wa)] = {"n_runs_ok": len(rr), "S_size": len(S), "S_runs": [s_["run"] for s_ in S],
                            "blocked_targets": blocked, "reading": reading,
                            "O_ranges": {kk: [float(np.nanmin([rw[kk] for rw in res_rows if rw["Wa"] == Wa])),
                                              float(np.nanmax([rw[kk] for rw in res_rows if rw["Wa"] == Wa]))] for kk in ob.BANDS},
                            "bound_theta1_range": [float(np.nanmin([rw["O5_bound"] for rw in th1])) if th1 else np.nan,
                                                   float(np.nanmax([rw["O5_bound"] for rw in th1])) if th1 else np.nan],
                            "bound_violations_theta096": [rw["run"] for rw in th096 if rw["bound_holds"] is False],
                            "looseness_theta096_range": [float(np.nanmin([rw["looseness"] for rw in th096])) if th096 else np.nan,
                                                         float(np.nanmax([rw["looseness"] for rw in th096])) if th096 else np.nan],
                            "true_share_theta096_range": [float(np.nanmin([rw["true_theta_share"] for rw in th096])) if th096 else np.nan,
                                                          float(np.nanmax([rw["true_theta_share"] for rw in th096])) if th096 else np.nan]}
    wcsv(csvd / f"{tag}_table.csv", res_rows)
    jdump(summary, csvd / f"{tag}_summary.json")
    for Wa, s_ in summary.items():
        print(f"{tag} Wa{Wa}: ok {s_['n_runs_ok']} · |S| {s_['S_size']} · blocked {s_['blocked_targets']} · {s_['reading']} · "
              f"O ranges {s_['O_ranges']} · bound θ=1 {s_['bound_theta1_range']} · violations {s_['bound_violations_theta096']} · "
              f"looseness {s_['looseness_theta096_range']}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["failcheck", "c1a", "c1b", "ad"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--spk", required=True)
    ap.add_argument("--csv", default=None)
    a = ap.parse_args(argv)
    rc = _dispatch(a)
    import c1_memguard as mg
    rc_mem = mg.rusage_exit_hook()                       # §8-11 ③ 교차 확인
    return rc_mem if (rc_mem is not None and rc == 0) else rc


def _dispatch(a):
    if a.step == "failcheck":
        return failcheck(a)
    if a.step == "c1a":
        rc = analyze_c1a(a)
        expectation(a)
        dc_features(a)
        return rc
    if a.step == "c1b":
        return analyze_c1b(a)
    if a.step == "ad":
        rc = analyze_c1a(a, arms=("AD", "K"), tag="ad_c1a", do_mc=False)
        analyze_c1b(a, tag="ad_c1b", mode="on")
        import c1_grid as cg
        rq, rt, pr = cg.dc_z(Path(a.out), reg(a.spk)["I_1C_A"], arm_a="AD", tag_a="ad_dc")
        wcsv(Path(a.csv) / "ad_dc_z_qf.csv", rq)
        wcsv(Path(a.csv) / "ad_dc_z_time.csv", rt)
        jdump({"problems": pr, "z_max_qf": max((r["z"] for r in rq), default=None)}, Path(a.csv) / "ad_dc_z_meta.json")
        return rc
    return 2


if __name__ == "__main__":
    sys.exit(main())
