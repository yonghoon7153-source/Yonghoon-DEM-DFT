"""C1 격자 구동 — 설계서 `followups/assb-contact-truth/DESIGN_v1.md` §5-2 · §5-3 · §5-8 · §5-9 · §8-5 (구현 해석). 진단 전용.

사용: python -I c1_grid.py <conv|c1a|dc|c1b|ad_c1a|ad_dc|ad_c1b> --out <dir> [--shape G05|G2 --Wa 10|0.1]
종료 코드: 0 정상 · 3 = §5-8 중단 조건 발동 (기록 뒤) · 4 = 벽시계 상한 (규칙 7).
환경변수 C1_COPY (사본) · C1_T0 (2 차 시계 원점 ISO).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(os.environ["C1_COPY"]).resolve()))
sys.path.insert(0, str(HERE))

import c1_observe as ob  # noqa: E402
import c1_truth as tr  # noqa: E402

F_K = [2.0 ** (-k / 4) for k in range(9)]          # C1a f = 2^(−k/4)
P_K = [2.0 ** (-k / 4) for k in range(10)]         # C1b p
SOCS = (0.8, 0.5, 0.2)
PULSES = [(s, amp, sgn) for s in SOCS for amp in ("lin", "taf") for sgn in ("+", "-")]
REP_K = (2, 4, 8)                                   # 대표 f 0.707 · 0.5 · 0.25
K_RUN = tuple(range(1, 9))                          # C1a 열화 k (f < 1)
WAS = (10.0, 0.1)                                   # 명목 Wa (격자 라벨 — 설계서 그대로)
FA_LV = (1.0, 0.8, 0.6, 0.4)                        # C1b AD 켬 f_A (§5-3)
FK_LV = (1.0, 0.7, 0.5, 0.35, 0.25)                 # C1b AD 켬 f_k
LI_LIMIT = 1e-6                                     # §5-8 규칙 4
FAIL_FRAC = 0.05                                    # §5-8 규칙 6
DC_Z_LIMIT = 2.0                                    # §5-8 규칙 3(a)
CONV_TAU, CONV_Z = 0.01, 0.05                       # §5-8 규칙 5
VAR_FINE = {"x_s": 80, "x_p": 80, "r_p": 80}         # 3 차 판정 짝의 정밀판 (표준 40 의 × 2 · §8-7 ①)
TOL_FINE = 1e-10                                    # 표준 1e-9 ÷ 10
CONV_DIAG = (("v80_t1e-9", {"var_pts": {"x_s": 80, "x_p": 80, "r_p": 80}, "rtol": 1e-9, "atol": 1e-9}),
             ("v40_t1e-10", {"var_pts": {"x_s": 40, "x_p": 40, "r_p": 40}, "rtol": 1e-10, "atol": 1e-10}))   # 귀속 진단 (판정에 안 씀)
DC_DT_OUT = {"C/20": 1.0, "C/3": 0.1, "1C": 0.05}  # §8-7 ② B2 출력 간격


def jdump(obj, path):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)
    Path(path).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=conv))


def deadline() -> float:
    t0 = dt.datetime.strptime(os.environ["C1_T0"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return t0.timestamp() + 4 * 3600


def budget_left() -> float:
    return deadline() - time.time()


def reg(spk: Path) -> dict:
    return json.loads((spk / "s6_registered.json").read_text())


# --------------------------------------------------------------------------------------------
# B3 펄스 묶음 (C1a · 수렴 · AD)
# --------------------------------------------------------------------------------------------
LI_KEEP = ("Voltage [V]", "R-averaged positive particle concentration [mol.m-3]",
           "Positive electrode surface potential difference [V]")


def run_bundle(model, solver, sim, d, R):
    """12 펄스 (SOC 3 × 진폭 2 × 방향 2) — 펄스마다 균일 평형에서. 반환: V (12, n_t) · Li 상대 오차 (12)."""
    Vs, li = [], []
    for s, amp, sgn in PULSES:
        I = R["pulse_I_A"][amp + sgn]
        res = tr.run_pulse(model, solver, sim, d, x_start=R["soc_x"][str(s)], I_A=I, keep=LI_KEEP)
        li.append(tr.li_balance(res, d, I, 10.0)["rel_with_dl"])
        Vs.append(res["Voltage [V]"])
        n_pulse = res["n_pulse"]
    return np.array(Vs), np.array(li), n_pulse


def arm_list(arms=("A", "K")):
    runs = [("fresh", 0)]
    for arm in arms:
        for k in K_RUN:
            runs.append((arm, k))
    return runs


def c1a(args, arms=("A", "K"), tag="c1a"):
    R = reg(Path(args.spk))
    out = Path(args.out) / tag
    out.mkdir(parents=True, exist_ok=True)
    model, solver, sim = tr.build_model(args.shape)
    base = tr.base_inputs(shape=args.shape, Wa=args.Wa, x_mid=R["x_mid"])
    runs = arm_list(arms) if tag == "c1a" else [(a, k) for a in arms for k in K_RUN]
    summary = []
    n_fail = 0
    for arm, k in runs:
        if budget_left() < 60:
            jdump({"stop": "rule7_wallclock", "done": summary}, out / f"{args.shape}_Wa{args.Wa:g}_summary.json")
            return 4
        f = F_K[k]
        d = base if arm == "fresh" else tr.knob_inputs(arm, f, base=base)
        name = f"{args.shape}_Wa{args.Wa:g}_{arm}_k{k}"
        t0 = time.time()
        try:
            V, li, n_pulse = run_bundle(model, solver, sim, d, R)
        except Exception as e:  # 해법 실패 — 조용히 빼지 않는다
            n_fail += 1
            summary.append({"run": name, "status": "solver_fail", "error": repr(e)[:300]})
            continue
        np.savez_compressed(out / f"{name}.npz", V=V, li=li, n_pulse=n_pulse)
        summary.append({"run": name, "arm": arm, "k": k, "f": f, "status": "ok", "elapsed_s": time.time() - t0,
                        "li_max": float(li.max()), "V_min": float(V.min()), "V_max": float(V.max())})
    li_bad = [s for s in summary if s.get("status") == "ok" and s["li_max"] > LI_LIMIT]
    res = {"shape": args.shape, "Wa": args.Wa, "runs": summary, "n_fail": n_fail, "n_runs": len(runs),
           "li_violations": [s["run"] for s in li_bad]}
    jdump(res, out / f"{args.shape}_Wa{args.Wa:g}_summary.json")
    print(f"{tag} {args.shape} Wa{args.Wa:g}: runs {len(runs)} · fail {n_fail} · Li max "
          f"{max((s.get('li_max', 0) for s in summary), default=0):.2e}")
    if li_bad:
        print(f"STOP rule 4 (Li > {LI_LIMIT}): {res['li_violations']}")
        return 3
    return 0


# --------------------------------------------------------------------------------------------
# 격자 수렴 (§5-2 · §5-8 규칙 5) — Wa 0.1 · G½ · 신품 · A(0.25) · K(0.25)
# --------------------------------------------------------------------------------------------
def onset_samples(n_pulse, dt_obs, w_fit):
    tp = tr.grid_after_step(10.0)
    idx = ob.observe_indices(tp, dt_obs)
    idx = idx[(tp[idx] >= dt_obs - 1e-12) & (tp[idx] <= w_fit + 1e-12)]
    return tp, idx


def f1_noise_free(V, n_pulse, x, I, dt_obs, w_fit):
    tp, idx = onset_samples(n_pulse, dt_obs, w_fit)
    return ob.fit_f1(tp[idx], V[:n_pulse][idx], I=I, V0=tr.ocp(x), dt=dt_obs)


def _conv_compare(Va, Vb, R, shape, n_pulse, runs):
    rows, worst_tau, worst_z = [], 0.0, 0.0
    for j, (s, amp, sgn) in enumerate(PULSES):
        x = R["soc_x"][str(s)]
        I = R["pulse_I_A"][amp + sgn]
        w = R["W_fit_s"][f"{shape}|SOC{s}"]
        for name in runs:
            a = f1_noise_free(Va[name][j], n_pulse, x, I, 1e-4, w)["tau"]
            b = f1_noise_free(Vb[name][j], n_pulse, x, I, 1e-4, w)["tau"]
            ch = abs(a / b - 1) if (np.isfinite(a) and np.isfinite(b)) else (0.0 if (np.isnan(a) and np.isnan(b)) else np.inf)
            worst_tau = max(worst_tau, ch)
            rows.append({"pulse": f"SOC{s} {amp}{sgn}", "run": name, "tau_std": a, "tau_other": b, "rel_change": ch})
        zs = np.linalg.norm(Va["A_k8"][j] - Va["K_k8"][j]) / 1e-3
        zf = np.linalg.norm(Vb["A_k8"][j] - Vb["K_k8"][j]) / 1e-3
        chz = abs(zs / zf - 1)
        worst_z = max(worst_z, chz)
        rows.append({"pulse": f"SOC{s} {amp}{sgn}", "run": "z_A_vs_K_k8_direct", "z_std": zs, "z_other": zf, "rel_change": chz})
    return rows, worst_tau, worst_z


def conv(args):
    R = reg(Path(args.spk))
    out = Path(args.out) / "conv"
    out.mkdir(parents=True, exist_ok=True)
    shape, Wa = "G05", 0.1
    base = tr.base_inputs(shape=shape, Wa=Wa, x_mid=R["x_mid"])
    runs = {"fresh": base, "A_k8": tr.knob_inputs("A", 0.25, base=base), "K_k8": tr.knob_inputs("K", 0.25, base=base)}
    V, li, el = {}, {}, {}
    variants = [("std", {}), ("fine", {"var_pts": VAR_FINE, "rtol": TOL_FINE, "atol": TOL_FINE})] + list(CONV_DIAG)
    n_pulse = None
    for lab, kw in variants:
        t0 = time.time()
        model, solver, sim = tr.build_model(shape, **kw)
        V[lab] = {}
        for name, d in runs.items():
            Vb, l_, n_pulse = run_bundle(model, solver, sim, d, R)
            V[lab][name] = Vb
            li[f"{lab}|{name}"] = float(l_.max())
        el[lab] = time.time() - t0
        print(f"conv variant {lab}: {el[lab]:.1f}s", flush=True)
    rows, worst_tau, worst_z = _conv_compare(V["std"], V["fine"], R, shape, n_pulse, runs)
    diag = {}
    for lab, _ in CONV_DIAG:
        r2, wt, wz = _conv_compare(V["std"], V[lab], R, shape, n_pulse, runs)
        diag[lab] = {"worst_tau_rel_change": wt, "worst_z_rel_change": wz, "rows": r2}
    stop = worst_tau > CONV_TAU or worst_z > CONV_Z
    res = {"decision_pair": "std (40 · 1e-9) vs fine (80 · 1e-10)", "rows": rows, "worst_tau_rel_change": worst_tau,
           "worst_z_rel_change": worst_z, "li": li, "elapsed_s": el, "limits": {"tau": CONV_TAU, "z": CONV_Z},
           "stop_rule5": bool(stop), "diagnostics_not_for_decision": diag}
    jdump(res, out / "conv.json")
    print(f"conv (판정 짝 표준 ↔ 80·1e-10): worst τ̂ change {worst_tau:.3e} (limit {CONV_TAU}) · worst z change {worst_z:.3e} (limit {CONV_Z})")
    for lab, dd in diag.items():
        print(f"conv 진단 {lab} (판정 아님): τ̂ {dd['worst_tau_rel_change']:.3e} · z {dd['worst_z_rel_change']:.3e}")
    print(f"conv Li max {max(li.values()):.2e}")
    if any(v > LI_LIMIT for v in li.values()):
        print("STOP rule 4")
        return 3
    if stop:
        print("STOP rule 5 (격자 수렴)")
        return 3
    return 0


# --------------------------------------------------------------------------------------------
# DC 영 채널 (B2) — §4-2 · §5-8 규칙 3(a)
# --------------------------------------------------------------------------------------------
RATES = (("C/20", 1 / 20), ("C/3", 1 / 3), ("1C", 1.0))
CC_KEEP = ("Voltage [V]", "R-averaged positive particle concentration [mol.m-3]",
           "Positive electrode surface potential difference [V]")


def run_b2(model, solver, sim, d, R, rate, rname):
    I = rate * R["I_1C_A"]
    try:
        r = tr.run_cc(model, solver, sim, d, x_start=R["x_top"], I_A=I, t_max=1.6 * 3600 / rate, dt_out=DC_DT_OUT[rname],
                      V_lo=tr.V_LOW, V_hi=10.0, keep=tr.QF_KEEP)
    except Exception as e:
        msg = repr(e)
        if "non-positive at initial conditions" in msg or "initial conditions" in msg:
            return {"status": "immediate_cutoff", "t": np.array([]), "V": np.array([]), "QF": np.array([]), "Q_Ah": 0.0,
                    "error": msg[:200]}
        return {"status": "solver_fail", "t": np.array([]), "V": np.array([]), "QF": np.array([]), "Q_Ah": np.nan, "error": msg[:300]}
    t, V = r["t"], r["Voltage [V]"]
    q = tr.qf_and_li(r, d, I)
    xbar = R["x_top"] + I * t / (tr.q_per_x() * d["eps_am"] / tr.EPS_CAM0)
    eta = np.array([tr.ocp(min(xx, 1 - 1e-9)) for xx in xbar[:: max(1, int(10.0 / DC_DT_OUT[rname]))]]) - V[:: max(1, int(10.0 / DC_DT_OUT[rname]))]
    return {"status": "ok", "t": t, "V": V, "QF": q["qf"], "Q_Ah": I * float(t[-1]) / 3600, "termination": str(r["termination"]),
            "li_rel": q["rel"], "Qdl_end_C": q["Qdl_end_C"], "mean_overpotential_V": float(np.mean(eta)), "n_out": int(t.size)}


def dqdv_peak(t, V, I):
    from src.curves import to_dqdv
    if len(t) < 20:
        return np.nan
    q = I * t / 3600
    sl = slice(3, len(q) - 3)                      # 끝단 절단 3 점 (P3 n_trim 관례)
    qn = np.linspace(q[sl][0], q[sl][-1], 300)     # 보간 300 점
    vn = np.interp(qn, q[sl], V[sl])
    vs, dqdv = to_dqdv((qn - qn[0]) / (qn[-1] - qn[0]), vn)
    return float(vs[np.argmax(np.abs(dqdv))])


def dc_runs(args, arms=("A", "K"), tag="dc", include_fresh=True):
    R = reg(Path(args.spk))
    out = Path(args.out) / tag
    out.mkdir(parents=True, exist_ok=True)
    model, solver, sim = tr.build_model("G05")
    summ = []
    n_fail = 0
    for Wa in WAS:
        base = tr.base_inputs(shape="G05", Wa=Wa, x_mid=R["x_mid"])
        runs = ([("fresh", 0)] if include_fresh else []) + [(a, k) for a in arms for k in (4, 8)]
        for arm, k in runs:
            d = base if arm == "fresh" else tr.knob_inputs(arm, F_K[k], base=base)
            name = f"G05_Wa{Wa:g}_{arm}_k{k}"
            store = {}
            for rname, rate in RATES:
                r = run_b2(model, solver, sim, d, R, rate, rname)
                if r["status"] == "solver_fail":
                    n_fail += 1
                store[f"t_{rname}"] = r["t"]
                store[f"V_{rname}"] = r["V"]
                store[f"QF_{rname}"] = r["QF"]
                summ.append({"run": name, "Wa": Wa, "arm": arm, "k": k, "rate": rname,
                             **{kk: vv for kk, vv in r.items() if kk not in ("t", "V", "QF")},
                             "dqdv_peak_V": dqdv_peak(r["t"], r["V"], rate * R["I_1C_A"]) if rname == "C/20" else None})
            np.savez_compressed(out / f"{name}.npz", **{k_.replace("/", "_"): v for k_, v in store.items()})
    jdump({"runs": summ, "n_fail": n_fail}, out / "dc_runs.json")
    return summ, n_fail


def dc_groups(out: Path, arm_a="A", tag_a="dc"):
    """(Wa, 율) 묶음의 곡선 다섯 — 신품 · arm_a {0.5, 0.25} · K {0.5, 0.25} (§8-7 ②)."""
    groups = {}
    for Wa in WAS:
        load = {}
        for key, folder in ((("fresh", 0), "dc"), ((arm_a, 4), tag_a), ((arm_a, 8), tag_a), (("K", 4), "dc"), (("K", 8), "dc")):
            load[key] = np.load(out / folder / f"G05_Wa{Wa:g}_{key[0]}_k{key[1]}.npz")
        for rname, rate in RATES:
            k_ = rname.replace("/", "_")
            g = {}
            for key, z in load.items():
                kk = ("A", key[1]) if key[0] == arm_a else key
                g[kk] = (z[f"t_{k_}"], z[f"V_{k_}"], z[f"QF_{k_}"])
            groups[(Wa, rname, rate)] = g
    return groups


def dc_z(out: Path, I_1C: float, arm_a="A", tag_a="dc"):
    """보정 z_DC (Q_F 축 — 판정) · 시간 축 z_DC (2 차 정의 — 진단). σ_V 1 mV · 상대 팔 격자 {1, 0.5, 0.25}."""
    rows_q, rows_t, problems = [], [], []
    for (Wa, rname, rate), g in dc_groups(out, arm_a, tag_a).items():
        if any(len(v[0]) < 3 for v in g.values()):
            problems.append({"Wa": Wa, "rate": rname, "status": "curve_missing (immediate cutoff)"})
            continue
        I = rate * I_1C                               # 전류 [A] — ΔQ = I·10 s (§8-7 ②)
        tag = {"Wa": Wa, "rate": rname}
        try:
            for r in ob.dc_z_qf({k: (v[2], v[1]) for k, v in g.items()}, I=I, dt_equiv=10.0, sigma=1e-3):
                rows_q.append({**tag, **r})
        except ValueError as e:
            problems.append({**tag, "status": f"QF_not_monotonic: {e}"})
        for r in ob.dc_z_time({k: (v[0], v[1]) for k, v in g.items()}, I=I, dt_grid=10.0, sigma=1e-3):
            rows_t.append({**tag, **r})
    return rows_q, rows_t, problems


def dc(args):
    summ, n_fail = dc_runs(args)
    rows_q, rows_t, problems = dc_z(Path(args.out), reg(Path(args.spk))["I_1C_A"])
    zmax = max((r["z"] for r in rows_q), default=np.nan)
    zmax_t = max((r["z"] for r in rows_t), default=np.nan)
    nonmono = [p for p in problems if str(p.get("status", "")).startswith("QF_not_monotonic")]
    stop = bool(np.isfinite(zmax) and zmax >= DC_Z_LIMIT)
    li_bad = [s for s in summ if s.get("status") == "ok" and s["li_rel"] > LI_LIMIT]
    res = {"z_rows_qf_decision": rows_q, "z_rows_time_diagnostic": rows_t, "problems": problems, "z_max_qf": zmax,
           "z_max_time_diag": zmax_t, "limit": DC_Z_LIMIT, "stop_rule3a": stop, "n_fail": n_fail,
           "li_violations": [(s["run"], s["rate"]) for s in li_bad]}
    jdump(res, Path(args.out) / "dc" / "dc_z.json")
    for r in rows_q:
        if r["dR0"] == "none":
            print(f"DC(Q_F) Wa{r['Wa']:g} {r['rate']} f{r['f']:.3f}: z {r['z']:.3f} (direct {r['z_direct_same_f']:.3f}) "
                  f"max|ΔV| {r['max_abs_dV_same_f_V']:.2e} V · n {r['n_samples']}")
    for r in rows_t:
        if r["dR0"] == "none":
            print(f"DC(time · 진단) Wa{r['Wa']:g} {r['rate']} f{r['f']:.3f}: z {r['z']:.3f}")
    for p_ in problems:
        print(f"DC problem: {p_}")
    print(f"DC z_max (Q_F · 판정) {zmax:.3f} (limit {DC_Z_LIMIT}) · z_max (time · 진단) {zmax_t:.3f} · fail {n_fail} · "
          f"Li violations {res['li_violations']}")
    if li_bad:
        print("STOP rule 4")
        return 3
    if nonmono:
        print("STOP — Q_F 가 단조 증가가 아니어서 보정 z 를 계산할 수 없다 (§8-7 ② · 기록)")
        return 3
    if stop:
        print("STOP rule 3(a) — DC 영 채널 (Q_F 축) A ↔ K 의 z ≥ 2 (대수 예측 오류 · 구현 결함을 가르지 않는다)")
        return 3
    return 0


# --------------------------------------------------------------------------------------------
# C1b (§5-3) — B0 · B4 · B3 의 x_mid C/10 방전 펄스
# --------------------------------------------------------------------------------------------
def _continue(sol):
    """사건으로 끝난 해에서 다음 구간을 잇는다 — PyBaMM step() 은 사건 종료 해를 그대로 돌려주므로 (실험 기계는 '[experiment]' 표지로
    통과) 마지막 상태의 종료 표지만 'final time' 으로 바꿔 넘긴다 (배관 점검 결함 수정 · 물리 변경 없음 · 일관 초기화는 PyBaMM 이 다시 한다)."""
    st = sol.last_state
    st.termination = "final time"
    return st


def run_b0(model, solver, sim, d, R):
    """조립 x0 균일 → C/10 충전 4.3 V → 휴지 10 min → C/10 방전 3.0 V (출력 10 s)."""
    I = R["I_C10_A"]
    dd = dict(d)
    dd.update({"I": -I, "c0": R["x0_assembled"] * tr.C_MAX, "V_lo": 0.0, "V_hi": tr.V_HIGH})
    inp = tr.to_pybamm_inputs(sim, dd)
    t_i = np.round(np.arange(0, 12 * 3600, 10.0), 6)
    s1 = solver.solve(model, t_eval=[0.0, 12 * 3600.0], t_interp=t_i, inputs=inp)
    t_ch = float(s1.t[-1])
    dd2 = dict(dd)
    dd2.update({"I": 0.0, "V_lo": 0.0, "V_hi": 10.0})
    s2 = solver.step(_continue(s1), model, dt=600.0, t_interp=np.round(np.arange(0, 601, 10.0), 6),
                     inputs=tr.to_pybamm_inputs(sim, dd2))
    dd3 = dict(dd)
    dd3.update({"I": I, "V_lo": tr.V_LOW, "V_hi": 10.0})
    s3 = solver.step(_continue(s2), model, dt=12 * 3600.0, t_interp=np.round(np.arange(0, 12 * 3600, 10.0), 6),
                     inputs=tr.to_pybamm_inputs(sim, dd3))
    t_rest = float(s2.t[-1]) - t_ch
    t_dis = float(s3.t[-1]) - float(s3.t[0])
    c0 = np.asarray(s1["R-averaged positive particle concentration [mol.m-3]"].entries)[:, 0]
    c1 = np.asarray(s3["R-averaged positive particle concentration [mol.m-3]"].entries)[:, -1]
    p0 = np.asarray(s1["Positive electrode surface potential difference [V]"].entries)[:, 0]
    p1 = np.asarray(s3["Positive electrode surface potential difference [V]"].entries)[:, -1]
    n_x = c0.size
    dx = tr.L_PE / n_x
    dN = tr.AREA * d["eps_am"] * dx * (c1 - c0).sum()
    a = 3.0 * d["eps_am"] / tr.R_P
    Qdl = tr.AREA * a * d["c_dl"] * dx * (p1 - p0).sum()
    q_in = -I * t_ch + I * t_dis
    li_rel = abs(tr.F * dN - Qdl - q_in) / (I * (t_ch + t_dis))
    t = np.concatenate([np.asarray(s1.t), np.asarray(s2.t)[1:], np.asarray(s3.t)[1:]])
    V = np.concatenate([np.asarray(s1["Voltage [V]"].entries), np.asarray(s2["Voltage [V]"].entries)[1:],
                        np.asarray(s3["Voltage [V]"].entries)[1:]])
    return {"Q_ch_Ah": I * t_ch / 3600, "Q_dis_Ah": I * t_dis / 3600, "term_ch": str(s1.termination),
            "term_rest": str(s2.termination), "t_rest_s": t_rest, "term_dis": str(s3.termination), "li_rel": float(li_rel),
            "t": t, "V": V}


def run_b4(model, solver, sim, d, R):
    """x_mid 균일 → C/10 방전 10 min → 휴지 1 h (출력 1 s) · GITT 비 (§4-2 O2) · V_pre = U(x_mid)."""
    I = R["I_C10_A"]
    dd = dict(d)
    dd.update({"I": I, "c0": R["x_mid"] * tr.C_MAX, "V_lo": 0.0, "V_hi": 10.0})
    tp = np.round(np.arange(0, 601, 1.0), 6)
    s1 = solver.solve(model, t_eval=[0.0, 600.0], t_interp=tp, inputs=tr.to_pybamm_inputs(sim, dd))
    dd2 = dict(dd)
    dd2["I"] = 0.0
    s2 = solver.step(s1, model, dt=3600.0, t_interp=np.round(np.arange(0, 3601, 1.0), 6),
                     inputs=tr.to_pybamm_inputs(sim, dd2))
    V = np.asarray(s2["Voltage [V]"].entries)
    vp = V[: tp.size]
    vr = V[tp.size + 1:]                           # 휴지 상대 1..3600 s (t_rel = 0 제외)
    tr_ = np.arange(1, 3601, 1.0)
    g = ob.gitt_ratio(t_pulse=tp, v_pulse=vp, t_rest=tr_, v_rest=vr, v_pre=tr.ocp(R["x_mid"]))
    return {**g, "V_end_rest": float(vr[-1]), "OCV_x_mid": tr.ocp(R["x_mid"])}


def c1b_one(model, solver, sim, d, R, w_fit):
    b0 = run_b0(model, solver, sim, d, R)
    b4 = run_b4(model, solver, sim, d, R)
    I = R["I_C10_A"]
    res = tr.run_pulse(model, solver, sim, d, x_start=R["x_mid"], I_A=I, keep=LI_KEEP)
    li_p = tr.li_balance(res, d, I, 10.0)["rel_with_dl"]
    tp, idx = onset_samples(res["n_pulse"], 1e-3, w_fit)
    f1 = ob.fit_f1(tp[idx], res["Voltage [V]"][: res["n_pulse"]][idx], I=I, V0=tr.ocp(R["x_mid"]), dt=1e-3)
    return b0, b4, f1, li_p


def c1b(args, mode="off"):
    R = reg(Path(args.spk))
    tag = "c1b" if mode == "off" else "ad_c1b"
    out = Path(args.out) / tag
    out.mkdir(parents=True, exist_ok=True)
    model, solver, sim = tr.build_model("G05")
    w_fit = R["W_fit_s"]["G05|SOC0.5"]
    rows, n_fail = [], 0
    if mode == "off":
        grid = [(Wa, p_k, fs, th) for Wa in (args.Wa,) for p_k in range(len(P_K)) for fs in (1.0, 0.1) for th in (1.0, 0.96)]
    else:
        grid = [(Wa, (fa, fk), 1.0, th) for Wa in (args.Wa,) for fa in FA_LV for fk in FK_LV for th in (1.0, 0.96)]
    for Wa, pk, fs, th in grid:
        if budget_left() < 120:
            jdump({"stop": "rule7_wallclock", "rows": rows}, out / f"c1b_Wa{Wa:g}.json")
            return 4
        base = tr.base_inputs(shape="G05", Wa=Wa, x_mid=R["x_mid"])
        if mode == "off":
            p = P_K[pk]
            d = tr.knob_inputs("K", p, base=base, theta=th, f_sigma=fs)   # 곱 p 를 k₀ 로 (f_A = 1 · §8-5)
            lab = {"p_k": pk, "p": p, "f_A": 1.0, "f_k": p}
        else:
            fa, fk = pk
            d = tr.knob_inputs("AD", fa, base=base, theta=th, f_sigma=fs) if fa < 1.0 else dict(
                tr.knob_inputs("K", 1.0, base=base, theta=th, f_sigma=fs))
            d["k0"] = d["k0"] * fk
            lab = {"f_A": fa, "f_k": fk, "p": fa * fk}
        name = f"Wa{Wa:g}_" + "_".join(f"{k}{v:g}" for k, v in lab.items() if k != "p") + f"_fs{fs:g}_th{th:g}"
        try:
            b0, b4, f1, li_p = c1b_one(model, solver, sim, d, R, w_fit)
        except Exception as e:
            n_fail += 1
            rows.append({"run": name, "status": "solver_fail", "error": repr(e)[:300], **lab, "f_sigma": fs, "theta": th, "Wa": Wa})
            continue
        led = tr.ledger(theta=th, xbar_iso=R["x0_assembled"])
        np.savez_compressed(out / f"{name}_b0.npz", t=b0["t"], V=b0["V"])
        rows.append({"run": name, "status": "ok", "Wa": Wa, **lab, "f_sigma": fs, "theta": th,
                     "Q_ch_Ah": b0["Q_ch_Ah"], "Q_dis_Ah": b0["Q_dis_Ah"], "term_ch": b0["term_ch"], "term_dis": b0["term_dis"],
                     "term_rest": b0["term_rest"], "t_rest_s": b0["t_rest_s"],
                     "li_b0": b0["li_rel"], "li_pulse": li_p,
                     "gitt_dE_t": b4["dE_t"], "gitt_dE_s": b4["dE_s"], "gitt_ratio": b4["ratio"], "gitt_dE_s_10min": b4["dE_s_10min"],
                     "Rp": f1["Rp"], "R0": f1["R0"], "tau": f1["tau"], "k_sqrt": f1["k"],
                     "N_iso_mol": led["N_iso"], "V_iso_m3": led["V_iso"]})
        print(f"{tag} {name}: Qch {b0['Q_ch_Ah']:.4f} Qdis {b0['Q_dis_Ah']:.4f} GITT {b4['ratio']:.4f} Rp {f1['Rp']:.4e} "
              f"li {max(b0['li_rel'], li_p):.1e}", flush=True)
    li_bad = [r["run"] for r in rows if r.get("status") == "ok" and max(r["li_b0"], r["li_pulse"]) > LI_LIMIT]
    jdump({"rows": rows, "n_fail": n_fail, "n_runs": len(grid), "li_violations": li_bad}, out / f"c1b_Wa{args.Wa:g}.json")
    if li_bad:
        print(f"STOP rule 4: {li_bad}")
        return 3
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["conv", "c1a", "dc", "c1b", "ad_c1a", "ad_dc", "ad_c1b"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--spk", required=True)
    ap.add_argument("--shape", default="G05")
    ap.add_argument("--Wa", type=float, default=10.0)
    a = ap.parse_args(argv)
    if budget_left() < 0:
        print("STOP rule 7 (벽시계)")
        return 4
    if a.step == "conv":
        return conv(a)
    if a.step == "c1a":
        return c1a(a)
    if a.step == "dc":
        return dc(a)
    if a.step == "c1b":
        return c1b(a, "off")
    if a.step == "ad_c1a":
        return c1a(a, arms=("AD",), tag="ad_c1a")
    if a.step == "ad_dc":
        summ, n_fail = dc_runs(a, arms=("AD",), tag="ad_dc", include_fresh=False)
        jdump({"n_fail": n_fail}, Path(a.out) / "ad_dc" / "ad_dc_status.json")
        return 0
    if a.step == "ad_c1b":
        return c1b(a, "on")
    return 2


if __name__ == "__main__":
    sys.exit(main())
