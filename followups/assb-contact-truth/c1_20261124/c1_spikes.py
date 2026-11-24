"""C1 구현 스파이크 S1–S6 (설계서 §3-2) — 통과 조건은 설계서 표 그대로. 진단 전용 · 인용 금지.

사용: python -I c1_spikes.py <s1|s2|s3|s4|s5|s6|all> --out <dir>
환경변수 C1_COPY (사본 — c1_observe 의 add_noise 재사용 경로).
S7 (pybamm-eis) 은 D4 보류 — 실행하지 않는다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(os.environ["C1_COPY"]).resolve()))
sys.path.insert(0, str(HERE))

import c1_truth as tr  # noqa: E402

R_LIN, R_TAF = 0.2, 5.0          # r_kin (§5-2)
SOCS = (0.8, 0.5, 0.2)
F_K = 0.25                        # τ_max 어림의 K 팔 손실 (§5-2 창 규칙)


def jdump(obj, path):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)
    Path(path).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=conv))


def x_window():
    x_top = tr.x_of_ocp(tr.V_HIGH)
    x_low = tr.x_of_ocp(tr.V_LOW)
    return x_top, x_low


def c10_end(model, solver, sim, b, x_top, I10):
    r = tr.run_cc(model, solver, sim, b, x_start=x_top, I_A=I10, t_max=12.5 * 3600, dt_out=10.0,
                  V_lo=tr.V_LOW, V_hi=10.0, keep=("Voltage [V]", "Electrolyte concentration [mol.m-3]"))
    t_end = float(r["t"][-1])
    q = I10 * t_end
    return x_top + q / tr.q_per_x(), r


# ------------------------------------------------------------------ S6 (등록 수) — 다른 스파이크가 x_mid 를 쓴다
def s6(out: Path) -> dict:
    t0 = time.time()
    xs = np.linspace(1e-6, 1 - 1e-6, 200001)
    U = np.array([tr.ocp(x) for x in xs[::100]])
    mono = bool(np.all(np.diff(U) < 0))
    x_top, x_low = x_window()
    q1c = tr.q_1c_ah()
    I1C = q1c                                     # A (1 h)
    I10 = 0.1 * I1C
    model, solver, sim = tr.build_model("G05")
    x_mid = 0.5 * (x_top + x_low)
    hist = []
    for it in range(12):
        b = tr.base_inputs(shape="G05", Wa=10.0, x_mid=x_mid)
        x_end, r = c10_end(model, solver, sim, b, x_top, I10)
        x_new = 0.5 * (x_top + x_end)
        hist.append({"it": it, "x_mid_in": x_mid, "x_end": x_end, "x_mid_out": x_new, "term": str(r["termination"])})
        if abs(x_new - x_mid) < 1e-7:
            x_mid = x_new
            break
        x_mid = x_new
    b = tr.base_inputs(shape="G05", Wa=10.0, x_mid=x_mid)
    x_end, r = c10_end(model, solver, sim, b, x_top, I10)
    soc_x = {s: x_top + (1 - s) * (x_end - x_top) for s in SOCS}
    j0t = tr.j0_target()
    I_lin = R_LIN * tr.A_SURF0 * j0t * tr.L_PE * tr.AREA
    I_taf = R_TAF * tr.A_SURF0 * j0t * tr.L_PE * tr.AREA
    cap5 = 5.0 * I1C
    pulses = {"lin+": I_lin, "lin-": -I_lin, "taf+": min(I_taf, cap5), "taf-": -min(I_taf, cap5)}
    tau_ct0 = tr.VT * tr.C_DL0 / j0t
    tau_max, w_fit = {}, {}
    for shape in tr.SHAPES:
        bb = tr.base_inputs(shape=shape, Wa=10.0, x_mid=x_mid)
        for s, x in soc_x.items():
            tau = tr.VT * tr.C_DL0 / (F_K * bb["k0"] * float(tr.g_shape(shape, x)))
            key = f"{shape}|SOC{s}"
            tau_max[key] = tau
            w_fit[key] = min(max(0.5, 10 * tau), 10.0)
    kap = {}
    for Wa in (10.0, 0.1):
        bb = tr.base_inputs(shape="G05", Wa=Wa, x_mid=x_mid)
        k_eff = bb["kappa"] * tr.EPS_SE ** tr.BRUGG_E
        R_ion = tr.L_PE / k_eff
        R_el = tr.L_PE / tr.SIGMA_S0
        kap[str(Wa)] = {"kappa_eff_S_m": k_eff, "kappa_bulk_S_m": bb["kappa"], "kappa_eff_mS_cm": k_eff * 10,
                        "R_ion_geo_ohm_m2": R_ion, "R_el_geo_ohm_m2": R_el,
                        "Wa_incl_electronic": tr.RCT_GEO0 / (R_ion + R_el),
                        "R_sep_ohm_m2": float(tr._P["Separator thickness [m]"]) / (bb["kappa"] * float(tr._P["Separator porosity"]) ** 1.5)}
    # 사본 configs/base.yaml 과 대조 (§1-4 — 양극 기하 그대로)
    import yaml
    cfg = yaml.safe_load(Path(os.environ["C1_COPY"], "configs", "base.yaml").read_text())
    geo_ok = (cfg["parameter_set"] == tr.PV_NAME and cfg["baseline"]["pe_vf"] == tr.EPS_CAM0
              and cfg["baseline"]["pe_porosity"] == tr.EPS_SE and cfg["baseline"]["pe_max_conc"] == tr.C_MAX)
    res = {
        "spike": "S6", "ocp_monotone_decreasing": mono, "U_x_top": tr.ocp(x_top), "U_x_low": tr.ocp(x_low),
        "cutoffs_V": [tr.V_LOW, tr.V_HIGH], "cutoff_rule_triggered": False,
        "cutoff_rule_note": "OCP 함수 (Chen2020_composite) 의 정규화 항 1e-4·(1/x+1/(x−1)) 때문에 (0,1) 의 상이 [3.0, 4.3] V 를 덮는다 → 대체 규칙 미발동",
        "x_top": x_top, "x_low_ocv": x_low, "x0_assembled": x_low,
        "x0_note": "조립 상태 '완전 리튬화' = OCV 창의 리튬화 끝 U⁻¹(3.0 V) (x = 1 은 U · j₀ 특이)",
        "Q_1C_Ah": q1c, "I_1C_A": I1C, "I_C10_A": I10,
        "x_mid_fixed_point": hist, "x_mid": x_mid, "x_end_C10": x_end, "C10_termination": str(r["termination"]),
        "soc_x": {str(k): v for k, v in soc_x.items()},
        "j0_target_A_m2": j0t, "k0": {sh: tr.base_inputs(shape=sh, Wa=10.0, x_mid=x_mid)["k0"] for sh in tr.SHAPES},
        "pulse_I_A": pulses, "pulse_C_rate": {k: v / I1C for k, v in pulses.items()},
        "pulse_cap_5C_hit": I_taf > cap5, "r_kin": {"lin": R_LIN, "taf": R_TAF},
        "tau_ct0_s": tau_ct0, "tau_max_s": tau_max, "W_fit_s": w_fit, "Wa": kap,
        "A_surf_m-1": tr.A_SURF0, "aL": tr.A_SURF0 * tr.L_PE, "C_geo_F_m2": tr.A_SURF0 * tr.L_PE * tr.C_DL0,
        "tau_Li_s": tr.VT / tr.J0_LI * tr.CDL_LI, "D_e": tr.D_E, "geometry_matches_copy_base_yaml": geo_ok,
        "elapsed_s": time.time() - t0,
    }
    jdump(res, out / "s6_registered.json")
    print(f"S6 x_top={x_top:.6f} x_low={x_low:.6f} x_mid={x_mid:.6f} x_end={x_end:.6f} "
          f"SOC x={[round(v, 6) for v in soc_x.values()]} Q1C={q1c:.4f}Ah tau_ct0={tau_ct0*1e3:.3f}ms "
          f"geo_ok={geo_ok} mono={mono}")
    print("S6 PASS" if (mono and geo_ok and "Minimum voltage" in str(r["termination"])) else "S6 FAIL")
    return res


def reg(out: Path) -> dict:
    return json.loads((out / "s6_registered.json").read_text())


# ------------------------------------------------------------------ S1
def s1(out: Path) -> dict:
    t0 = time.time()
    R = reg(out)
    model, solver, sim = tr.build_model("G05")
    b = tr.base_inputs(shape="G05", Wa=10.0, x_mid=R["x_mid"])
    r = tr.run_cc(model, solver, sim, b, x_start=R["x_top"], I_A=R["I_C10_A"], t_max=12.5 * 3600, dt_out=10.0,
                  V_lo=tr.V_LOW, V_hi=10.0, keep=("Voltage [V]", "Electrolyte concentration [mol.m-3]"))
    ce = r["Electrolyte concentration [mol.m-3]"]
    tau_li = tr.VT / tr.J0_LI * tr.CDL_LI
    limit = 1e-4 / 100.0                     # 관측 창의 가장 짧은 축 = truth 간격 0.1 ms 의 1/100
    conv = "Minimum voltage" in str(r["termination"])
    res = {"spike": "S1", "termination": str(r["termination"]), "t_end_s": float(r["t"][-1]),
           "Q_dis_Ah": R["I_C10_A"] * float(r["t"][-1]) / 3600, "V_first": float(r["Voltage [V]"][0]),
           "V_last": float(r["Voltage [V]"][-1]), "ce_max_rel_dev": float(np.max(np.abs(ce / tr.CE0 - 1))),
           "tau_Li_s": tau_li, "tau_Li_limit_s": limit,
           "counter_dl_note": "LithiumMetalSurfaceForm: C_dl,Li·dΔφ/dt = i_cc − j_pl (평면 이중층 · 'Negative electrode double-layer capacity')",
           "pass": bool(conv and tau_li <= limit), "elapsed_s": time.time() - t0}
    jdump(res, out / "s1.json")
    print(f"S1 term={res['termination']} t_end={res['t_end_s']:.0f}s Q={res['Q_dis_Ah']:.4f}Ah tau_Li={tau_li:.3e}s "
          f"(≤{limit:.0e}) ce_dev={res['ce_max_rel_dev']:.3e}")
    print("S1 PASS" if res["pass"] else "S1 FAIL")
    return res


# ------------------------------------------------------------------ S2
def s2(out: Path) -> dict:
    t0 = time.time()
    R = reg(out)
    model, solver, sim = tr.build_model("G05")
    b = tr.base_inputs(shape="G05", Wa=10.0, x_mid=R["x_mid"])
    I = 0.1 * R["pulse_I_A"]["lin+"]
    C_hand = tr.A_SURF0 * tr.C_DL0 * tr.L_PE * tr.AREA
    out_rows = {}
    for label, kmul, win in (("faradaic_suppressed_k0x1e-4", 1e-4, (0.010, 0.100)),
                             ("as_is_t0plus", 1.0, (1e-4, 5e-4))):
        bb = dict(b)
        bb["k0"] = b["k0"] * kmul
        res = tr.run_pulse(model, solver, sim, bb, x_start=R["x_mid"], I_A=I, t_on=1.0, t_off=1.0,
                           keep=("Voltage [V]",))
        t = res["t"][: res["n_pulse"]]
        v = res["Voltage [V]"][: res["n_pulse"]]
        m = (t >= win[0] - 1e-12) & (t <= win[1] + 1e-12)
        slope = np.polyfit(t[m], v[m], 1)[0]
        C_eff = -I / slope
        out_rows[label] = {"window_s": win, "slope_V_s": slope, "C_eff_F": C_eff, "C_hand_F": C_hand,
                           "rel": C_eff / C_hand - 1.0}
    rel = out_rows["faradaic_suppressed_k0x1e-4"]["rel"]
    resd = {"spike": "S2", "I_A": I, "rows": out_rows, "pass": bool(abs(rel) <= 0.05),
            "param_name": "Positive electrode double-layer capacity [F.m-2] (실제 접촉 면적당 — 모형식 a·C_dl·dΔφ/dt)",
            "elapsed_s": time.time() - t0}
    jdump(resd, out / "s2.json")
    for k, v in out_rows.items():
        print(f"S2 {k}: C_eff={v['C_eff_F']:.6f}F hand={C_hand:.6f}F rel={v['rel']:+.4%}")
    print("S2 PASS" if resd["pass"] else "S2 FAIL")
    return resd


# ------------------------------------------------------------------ S3 (+ S4 · S5c 재료)
def bundle(model, solver, sim, d, R):
    rows = []
    for s in SOCS:
        x = R["soc_x"][str(s)]
        for amp in ("lin", "taf"):
            for sgn in ("+", "-"):
                I = R["pulse_I_A"][amp + sgn]
                t0 = time.time()
                res = tr.run_pulse(model, solver, sim, d, x_start=x, I_A=I)
                el = time.time() - t0
                ce = res["Electrolyte concentration [mol.m-3]"]
                lb = tr.li_balance(res, d, I, 10.0)
                v = res["Voltage [V]"]
                rows.append({"soc": s, "amp": amp, "sgn": sgn, "I_A": I, "elapsed_s": el, "n_t": int(res["t"].size),
                             "ce_max_rel_dev": float(np.max(np.abs(ce / tr.CE0 - 1))),
                             "ce_spatial_rel": float(np.max((ce.max(axis=0) - ce.min(axis=0)) / tr.CE0)),
                             "li_rel_with_dl": lb["rel_with_dl"], "li_rel_no_dl": lb["rel_no_dl"],
                             "V_min": float(v.min()), "V_max": float(v.max()), "term": [str(x_) for x_ in res["termination"]]})
    return rows


def s3(out: Path) -> dict:
    t0 = time.time()
    R = reg(out)
    rows_all = {}
    timing = {}
    for shape, Wa in (("G05", 10.0), ("G2", 0.1)):
        tb = time.time()
        model, solver, sim = tr.build_model(shape)
        t_build = time.time() - tb
        d = tr.base_inputs(shape=shape, Wa=Wa, x_mid=R["x_mid"])
        ts = time.time()
        rows = bundle(model, solver, sim, d, R)
        timing[f"{shape}|Wa{Wa}"] = {"build_s": t_build, "bundle_s": time.time() - ts}
        rows_all[f"{shape}|Wa{Wa}"] = rows
    per_run = max(v["bundle_s"] for v in timing.values())
    n_core = 68 + 10 + 3 + 80            # 격자 수렴 3 · C1a 68 해 · DC 10 · C1b 80 (C1b · DC 는 펄스 묶음보다 가벼움 — 상한 어림)
    proj = {"per_bundle_s_max": per_run, "core_runs": n_core, "projected_core_s_upper": per_run * n_core}
    ok = all(all(str(t).startswith("final time") or "final time" in str(t) for t in r["term"])
             for rows in rows_all.values() for r in rows)
    res = {"spike": "S3", "timing": timing, "projection": proj, "rows": rows_all, "all_final_time": ok,
           "pass": bool(ok), "elapsed_s": time.time() - t0}
    jdump(res, out / "s3.json")
    for k, v in timing.items():
        print(f"S3 {k}: build {v['build_s']:.2f}s bundle(12 pulses) {v['bundle_s']:.2f}s")
    print(f"S3 projection core ≤ {proj['projected_core_s_upper']/60:.1f} min (upper) · all_final_time={ok}")
    print("S3 PASS" if res["pass"] else "S3 FAIL")
    return res


# ------------------------------------------------------------------ S4
def s4(out: Path) -> dict:
    t0 = time.time()
    R = reg(out)
    S1 = json.loads((out / "s1.json").read_text())
    S3 = json.loads((out / "s3.json").read_text())
    dev_s3 = max(r["ce_max_rel_dev"] for rows in S3["rows"].values() for r in rows)
    sp_s3 = max(r["ce_spatial_rel"] for rows in S3["rows"].values() for r in rows)
    dev = max(S1["ce_max_rel_dev"], dev_s3)
    # 진단 (판정 아님): 기작 — 이중층 항 −a·C_dl·dΔφ/dt / F 를 줄이면 편차가 비례해 주는가 · 예측값
    model, solver, sim = tr.build_model("G05")
    d = tr.base_inputs(shape="G05", Wa=10.0, x_mid=R["x_mid"])
    I = R["pulse_I_A"]["taf+"]
    x = R["x_mid"]
    diag = {}
    for mul in (1.0, 1e-3):
        dd = dict(d)
        dd["c_dl"] = d["c_dl"] * mul
        res = tr.run_pulse(model, solver, sim, dd, x_start=x, I_A=I)
        ce = res["Electrolyte concentration [mol.m-3]"]
        dphi = res["Positive electrode surface potential difference [V]"]
        n_x = dphi.shape[0]
        a = 3 * dd["eps_am"] / tr.R_P
        # 예측: Δ(∫ε c_e dx) = −∫ a C_dl ΔΔφ dx / F → 셀 평균 편차 (양극 부분만 · 분리막 확산 무시 어림)
        pred = -(a * dd["c_dl"] * (dphi[:, -1] - dphi[:, 0])).mean() / tr.F / tr.EPS_SE / tr.CE0
        nce = ce.shape[0]
        ce_pos_mean_end = ce[nce - n_x:, -1].mean()
        diag[f"c_dl_x{mul:g}"] = {"ce_max_rel_dev": float(np.max(np.abs(ce / tr.CE0 - 1))),
                                  "ce_pos_mean_rel_end": float(ce_pos_mean_end / tr.CE0 - 1), "pred_pos_rel_end_est": float(pred)}
    # 진단: c_e 결합 여부 — D_e × 10 · c_e0 × 2 에서 V(t) 차
    v_ref = tr.run_pulse(model, solver, sim, d, x_start=x, I_A=I, keep=("Voltage [V]",))["Voltage [V]"]
    dec = {}
    for lab, kw in (("D_e_x10", {"D_e": tr.D_E * 10}), ("ce0_x2", {"ce0": tr.CE0 * 2})):
        m2, s2_, sim2 = tr.build_model("G05", **kw)
        v2 = tr.run_pulse(m2, s2_, sim2, d, x_start=x, I_A=I, keep=("Voltage [V]",))["Voltage [V]"]
        dec[lab] = float(np.max(np.abs(v2 - v_ref)))
    res = {"spike": "S4", "ce_max_rel_dev_S1_C10": S1["ce_max_rel_dev"], "ce_max_rel_dev_S3_bundles": dev_s3,
           "ce_spatial_rel_S3": sp_s3, "ce_max_rel_dev": dev, "limit": 1e-9, "pass": bool(dev <= 1e-9),
           "diag_mechanism": diag, "diag_decoupling_max_abs_dV_V": dec,
           "mechanism_note": "PyBaMM 26.8 full_diffusion: ∂(εc)/∂t = −∇·(−D∇c + t₊ i_e/F) + Σa j_F/F · FullDifferential: a C_dl ∂Δφ/∂t = ∇·i_e − Σa j_F → t₊=1 이면 ∂(εc)/∂t = ∇·D∇c − a C_dl ∂Δφ/∂t / F",
           "elapsed_s": time.time() - t0}
    jdump(res, out / "s4.json")
    print(f"S4 ce max rel dev: S1(C/10) {S1['ce_max_rel_dev']:.3e} · S3 bundles {dev_s3:.3e} (spatial {sp_s3:.3e}) · limit 1e-9")
    for k, v in diag.items():
        print(f"S4 diag {k}: {v}")
    print(f"S4 diag decoupling max|ΔV|: {dec}")
    print("S4 PASS" if res["pass"] else "S4 FAIL")
    return res


# ------------------------------------------------------------------ S5
def s5(out: Path) -> dict:
    t0 = time.time()
    R = reg(out)
    S3 = json.loads((out / "s3.json").read_text())
    j0s = {}
    for shape in tr.SHAPES:
        model, solver, sim = tr.build_model(shape)
        d = tr.base_inputs(shape=shape, Wa=10.0, x_mid=R["x_mid"])
        res = tr.run_pulse(model, solver, sim, d, x_start=R["x_mid"], I_A=0.0, t_on=1.0, t_off=1.0,
                           keep=("Positive electrode exchange current density [A.m-2]",))
        j0s[shape] = float(np.asarray(res["Positive electrode exchange current density [A.m-2]"])[:, 0].mean())
    j0t = tr.j0_target()
    rel_g = max(abs(v / j0t - 1) for v in j0s.values())
    li_with = max(r["li_rel_with_dl"] for rows in S3["rows"].values() for r in rows)
    li_without = max(r["li_rel_no_dl"] for rows in S3["rows"].values() for r in rows)
    res = {"spike": "S5", "j0_at_x_mid": j0s, "j0_target": j0t, "g_norm_rel": rel_g,
           "physical_area_impl": "없음 (26.8 · spherical: a = 3ε/R 고정 · 'no particles' 는 입자 확산이 없어 DFN 의 면적 노브가 아님) → 미확인 · 대수로만 (조건부 8 실행 안 함)",
           "li_rel_with_dl_max": li_with, "li_rel_literal_no_dl_max": li_without,
           "pass_g": bool(rel_g <= 1e-12), "pass_li": bool(li_with <= 1e-6),
           "pass": bool(rel_g <= 1e-12 and li_with <= 1e-6), "elapsed_s": time.time() - t0}
    jdump(res, out / "s5.json")
    print(f"S5 j0(x_mid) {j0s} target {j0t:.6e} rel {rel_g:.2e} · Li rel (dl 포함) max {li_with:.2e} · 문자 그대로 (dl 없음) {li_without:.2e}")
    print("S5 PASS" if res["pass"] else "S5 FAIL")
    return res


# ------------------------------------------------------------------ 2 차 (§8-4 · 사후 규칙 변경) — S4′ · S5′
S4P_LIMIT = 1e-6        # V = 0.01 × σ_V,min (0.1 mV) — 판정 잡음 바닥의 1 % (호출자 · 사용자 승인 (가))


def s4p(out: Path) -> dict:
    """S4′: t₊ = 1 truth 의 c_e 되먹임 — 진단 변형 (D_e × 10 · c_e0 × 2) 과 기준의 max |ΔV| (공통 출력 시각)
    · 범위 = C1 프로토콜: C/10 방전 (G½ × Wa 10 · 0.1) + 12 펄스 묶음 (G½ · G2 × Wa 10 · 0.1)."""
    t0 = time.time()
    R = reg(out)
    rows = []
    for shape in tr.SHAPES:
        base_m = {}
        for Wa in (10.0, 0.1):
            d = tr.base_inputs(shape=shape, Wa=Wa, x_mid=R["x_mid"])
            m0 = tr.build_model(shape)
            mv = {lab: tr.build_model(shape, **kw) for lab, kw in tr.FEEDBACK_VARIANTS}
            if shape == "G05":
                r0 = tr.run_cc(*m0, d, x_start=R["x_top"], I_A=R["I_C10_A"], t_max=12.5 * 3600, dt_out=10.0,
                               V_lo=tr.V_LOW, V_hi=10.0)
                for lab, mm in mv.items():
                    r1 = tr.run_cc(*mm, d, x_start=R["x_top"], I_A=R["I_C10_A"], t_max=12.5 * 3600, dt_out=10.0,
                                   V_lo=tr.V_LOW, V_hi=10.0)
                    c = tr.common_max_abs_dv(r0["t"], r0["Voltage [V]"], r1["t"], r1["Voltage [V]"])
                    rows.append({"protocol": "C/10", "shape": shape, "Wa": Wa, "variant": lab, **c,
                                 "t_end_base": float(r0["t"][-1]), "t_end_var": float(r1["t"][-1])})
            for s in SOCS:
                x = R["soc_x"][str(s)]
                for amp in ("lin", "taf"):
                    for sgn in ("+", "-"):
                        I = R["pulse_I_A"][amp + sgn]
                        r0 = tr.run_pulse(*m0, d, x_start=x, I_A=I, keep=("Voltage [V]",))
                        for lab, mm in mv.items():
                            r1 = tr.run_pulse(*mm, d, x_start=x, I_A=I, keep=("Voltage [V]",))
                            c = tr.common_max_abs_dv(r0["t"], r0["Voltage [V]"], r1["t"], r1["Voltage [V]"])
                            rows.append({"protocol": f"pulse SOC{s} {amp}{sgn}", "shape": shape, "Wa": Wa,
                                         "variant": lab, **c})
    worst = max(rows, key=lambda r: r["max_abs_dv"])
    by_proto = {}
    for r in rows:
        k = "C/10" if r["protocol"] == "C/10" else "pulse"
        by_proto[k] = max(by_proto.get(k, 0.0), r["max_abs_dv"])
    res = {"spike": "S4p", "limit_V": S4P_LIMIT, "max_abs_dv_V": worst["max_abs_dv"], "worst": worst,
           "max_by_protocol": by_proto, "n_comparisons": len(rows), "rows": rows,
           "pass": bool(worst["max_abs_dv"] <= S4P_LIMIT and all(r["n_common"] > 0 for r in rows)),
           "elapsed_s": time.time() - t0}
    jdump(res, out / "s4p.json")
    print(f"S4′ max|ΔV| = {worst['max_abs_dv']:.3e} V (limit {S4P_LIMIT:.0e}) · by protocol {by_proto} · worst {worst['protocol']} "
          f"{worst['shape']} Wa{worst['Wa']} {worst['variant']} t={worst['t_at_max']} · n={len(rows)}")
    print("S4′ PASS" if res["pass"] else "S4′ FAIL")
    return res


def s5p(out: Path) -> dict:
    """S5′: 모형 j₀ = k₀·g_reg (SOC 점 셋 + 창 [x_top, x_end] 조밀 201 점 · 상대 ≤ 1e-12) · 두 g 의 x_mid j₀ = 목표 (≤ 1e-12)
    · 진단 |g_reg/g − 1| (창 · [x_top, x0]) · Li 보존 (이중층 항 포함) ≤ 1e-6 (S3 출력)."""
    t0 = time.time()
    R = reg(out)
    S3 = json.loads((out / "s3.json").read_text())
    x_top, x_end, x0 = R["x_top"], R["x_end_C10"], R["x0_assembled"]
    soc_pts = np.array([R["soc_x"][str(s)] for s in SOCS])
    dense = np.linspace(x_top, x_end, 201)
    res_shape = {}
    for shape in tr.SHAPES:
        k0 = tr.base_inputs(shape=shape, Wa=10.0, x_mid=R["x_mid"])["k0"]
        js = tr.model_j0_at(shape=shape, xs=soc_pts, x_mid=R["x_mid"])
        jd = tr.model_j0_at(shape=shape, xs=dense, x_mid=R["x_mid"])
        jm = tr.model_j0_at(shape=shape, xs=np.array([R["x_mid"]]), x_mid=R["x_mid"])[0]
        rel_soc = float(np.max(np.abs(js / (k0 * tr.g_reg(shape, soc_pts)) - 1)))
        rel_dense = float(np.max(np.abs(jd / (k0 * tr.g_reg(shape, dense)) - 1)))
        rel_mid = abs(jm / tr.j0_target() - 1)
        reg_soc = np.abs(tr.g_reg(shape, soc_pts) / tr.g_shape(shape, soc_pts) - 1)
        xw = np.linspace(x_top, x_end, 20001)
        xf = np.linspace(x_top, x0, 20001)
        reg_win = np.abs(tr.g_reg(shape, xw) / tr.g_shape(shape, xw) - 1)
        reg_full = np.abs(tr.g_reg(shape, xf) / tr.g_shape(shape, xf) - 1)
        res_shape[shape] = {"k0": k0, "rel_model_vs_k0greg_soc": rel_soc, "rel_model_vs_k0greg_dense": rel_dense,
                            "rel_j0_x_mid_vs_target": rel_mid,
                            "reg_effect_soc": {str(s): float(v) for s, v in zip(SOCS, reg_soc)},
                            "reg_effect_window_max": float(reg_win.max()),
                            "reg_effect_window_x_at_max": float(xw[np.argmax(reg_win)]),
                            "reg_effect_x_top_to_x0_max": float(reg_full.max()),
                            "soc_points_flag_reg_gt_1e-3": [str(s) for s, v in zip(SOCS, reg_soc) if v > 1e-3]}
    li_with = max(r["li_rel_with_dl"] for rows in S3["rows"].values() for r in rows)
    ok_impl = all(v["rel_model_vs_k0greg_soc"] <= 1e-12 and v["rel_model_vs_k0greg_dense"] <= 1e-12
                  and v["rel_j0_x_mid_vs_target"] <= 1e-12 for v in res_shape.values())
    res = {"spike": "S5p", "shapes": res_shape, "li_rel_with_dl_max": li_with,
           "physical_area_impl": "없음 (26.8 · spherical a = 3ε/R) → 미확인 · 대수로만 (조건부 8 실행 안 함)",
           "pass_impl": bool(ok_impl), "pass_li": bool(li_with <= 1e-6), "pass": bool(ok_impl and li_with <= 1e-6),
           "elapsed_s": time.time() - t0}
    jdump(res, out / "s5p.json")
    for sh, v in res_shape.items():
        print(f"S5′ {sh}: model/k0·g_reg soc {v['rel_model_vs_k0greg_soc']:.2e} dense {v['rel_model_vs_k0greg_dense']:.2e} · "
              f"x_mid vs target {v['rel_j0_x_mid_vs_target']:.2e} · |g_reg/g−1| soc {v['reg_effect_soc']} window max "
              f"{v['reg_effect_window_max']:.2e} @x={v['reg_effect_window_x_at_max']:.6f} · x_top→x0 max {v['reg_effect_x_top_to_x0_max']:.3e}")
    print(f"S5′ Li (dl 포함) max {li_with:.2e}")
    print("S5′ PASS" if res["pass"] else "S5′ FAIL")
    return res


# ------------------------------------------------------------------ 5 차 (§8-11 ② (c)) — S8 제한 출력 동치 (40 · 1e-9)
S8_RES = {"var_pts": {"x_s": 40, "x_p": 40, "r_p": 40}, "rtol": 1e-9, "atol": 1e-9}


def s8(out: Path) -> dict:
    """(i) B2 C/3 (0.1 s) · x_top · Wa 10 · G½ 신품: 제한 ↔ 전체 — 통과 조건 · (ii) 펄스 → 휴지 잇기 (제한 출력) ↔ 전체 — 기록."""
    t0 = time.time()
    R = reg(out)
    d = tr.base_inputs(shape="G05", Wa=10.0, x_mid=R["x_mid"])
    full = tr.build_model("G05", **S8_RES)
    rest = tr.build_model("G05", output_variables=list(tr.QF_KEEP), **S8_RES)
    I = R["I_1C_A"] / 3.0
    rf = tr.run_cc(*full, d, x_start=R["x_top"], I_A=I, t_max=1.6 * 3 * 3600, dt_out=0.1, V_lo=tr.V_LOW, V_hi=10.0, keep=tr.QF_KEEP)
    rr = tr.run_cc(*rest, d, x_start=R["x_top"], I_A=I, t_max=1.6 * 3 * 3600, dt_out=0.1, V_lo=tr.V_LOW, V_hi=10.0, keep=tr.QF_KEEP)
    c = tr.common_max_abs_dv(rf["t"], rf["Voltage [V]"], rr["t"], rr["Voltage [V]"])
    qf_f, qf_r = tr.qf_and_li(rf, d, I), tr.qf_and_li(rr, d, I)
    dt_end = abs(float(rf["t"][-1]) - float(rr["t"][-1]))
    dqf = abs(qf_f["qf"][-1] - qf_r["qf"][-1])
    lim_q = 1e-10 * I * float(rf["t"][-1])
    ok_i = bool(c["max_abs_dv"] <= 1e-10 and dqf <= lim_q and dt_end <= 1e-6 and qf_r["rel"] <= 1e-6 and c["n_common"] > 0)
    del rf, rr
    # (ii) 펄스 → 휴지 (제한 출력 · 끝 상태에서 step)
    ii = {}
    try:
        x, Ip = R["soc_x"]["0.2"], R["pulse_I_A"]["taf-"]
        lean = tr.run_pulse_lean(*full, d, x_start=x, I_A=Ip)
        m, so, sim = rest
        dd = dict(d)
        dd.update({"I": Ip, "c0": x * tr.C_MAX, "V_lo": 0.0, "V_hi": 10.0})
        q1 = so.solve(m, t_eval=[0.0, 10.0], t_interp=tr.grid_after_step(10.0), inputs=tr.to_pybamm_inputs(sim, dd))
        v1 = np.asarray(q1["Voltage [V]"].entries)
        dd["I"] = 0.0
        q2 = so.step(q1.last_state, m, dt=60.0, t_interp=tr.grid_after_step(60.0), inputs=tr.to_pybamm_inputs(sim, dd))
        v2 = np.asarray(q2["Voltage [V]"].entries)[1:]
        vr = np.concatenate([v1, v2])
        ii = {"supported": True, "n": int(vr.size), "max_abs_dv": float(np.max(np.abs(vr - lean["V"]))) if vr.size == lean["V"].size else None,
              "same_length": bool(vr.size == lean["V"].size)}
        ii["within_1e-10"] = bool(ii["same_length"] and ii["max_abs_dv"] <= 1e-10)
    except Exception as e:
        ii = {"supported": False, "error": repr(e)[:300]}
    res = {"spike": "S8", "res": "40 · 1e-9", "i_cc": {"max_abs_dv": c["max_abs_dv"], "n_common": c["n_common"], "dt_end_s": dt_end,
           "dQF_end_C": dqf, "lim_QF_C": lim_q, "li_rel_restricted": qf_r["rel"], "li_rel_full": qf_f["rel"], "pass": ok_i},
           "ii_pulse_rest": ii, "pass": ok_i, "elapsed_s": time.time() - t0}
    jdump(res, out / "s8.json")
    print(f"S8 (i) CC C/3 0.1 s 제한 ↔ 전체: max|ΔV| {c['max_abs_dv']:.2e} V (n {c['n_common']}) · |Δt_end| {dt_end:.1e} s · "
          f"|ΔQ_F| {dqf:.2e} C (lim {lim_q:.2e}) · Li(제한) {qf_r['rel']:.1e} · (ii) {ii}")
    print("S8 PASS" if ok_i else "S8 FAIL")
    return res


# ------------------------------------------------------------------ 6 차 (§8-13) — S9 표면 쪽 지수 반경 격자 ↔ 균일 기준판 (5 차 최악 행)
S9_TAF_ROWS = (("SOC0.8 taf+", "fresh"), ("SOC0.8 taf-", "fresh"), ("SOC0.8 taf+", "K_k8"), ("SOC0.8 taf-", "K_k8"),
               ("SOC0.5 taf+", "fresh"), ("SOC0.8 taf+", "A_k8"), ("SOC0.8 taf-", "A_k8"))      # 5 차 |τ̂ 변화| 1–7 위
S9_LIN_ROWS = (("SOC0.8 lin-", "fresh"), ("SOC0.8 lin+", "fresh"))                             # 선형 중 5 차 변화 최대 둘 (대조)
S9_Z_PULSES = ("SOC0.8 taf+", "SOC0.8 taf-")                                                    # A_k8 · K_k8 이 둘 다 든 펄스
S9_CONFIGS = (("nu80_t1e-9", {"var_pts": {"x_s": 80, "x_p": 80, "r_p": 80}, "rtol": 1e-9, "atol": 1e-9}),          # 반경 = 표준 꼴 (tr.STD_R_MESH)
              ("nu160_t1e-10", {"var_pts": {"x_s": 80, "x_p": 80, "r_p": 160}, "rtol": 1e-10, "atol": 1e-10}),
              ("ref_u1280_t1e-10", {"var_pts": {"x_s": 80, "x_p": 80, "r_p": 1280}, "rtol": 1e-10, "atol": 1e-10,
                                    "r_mesh": None, "output_variables": tr.PULSE_KEEP}))               # 균일 기준판 · 제한 출력
S9_LIM = {"tau": 0.01, "z": 0.05, "li": 1e-6}


def _fin(*v) -> bool:
    return all(isinstance(x, (int, float, np.floating)) and bool(np.isfinite(x)) for x in v)


def s9_verdict(tau_rows, z_rows, li_values, lim=S9_LIM) -> dict:
    """§8-13 ④ — τ̂ 행마다 (i) |nu/ref − 1| ≤ 1 % · (ii) |nu/nu2 − 1| ≤ 1 % · z 행마다 (iii) |nu/ref − 1| · |nu/nu2 − 1| ≤ 5 % ·
    (iv) Li 값 모두 ≤ 1e-6. NaN · 무한 · 0 분모 · 빈 표 → 실패."""
    fails, worst = [], {"i": 0.0, "ii": 0.0, "iii_ref": 0.0, "iii_2N": 0.0, "li": 0.0}
    if not tau_rows:
        fails.append({"crit": "empty", "what": "tau_rows"})
    if not z_rows:
        fails.append({"crit": "empty", "what": "z_rows"})
    if not li_values:
        fails.append({"crit": "empty", "what": "li_values"})
    for r in tau_rows:
        if not _fin(r["nu"], r["nu2"], r["ref"]) or r["ref"] == 0 or r["nu2"] == 0:
            fails.append({"crit": "nan", "row": r["row"]})
            continue
        ci, cii = abs(r["nu"] / r["ref"] - 1), abs(r["nu"] / r["nu2"] - 1)
        worst["i"], worst["ii"] = max(worst["i"], ci), max(worst["ii"], cii)
        if ci > lim["tau"]:
            fails.append({"crit": "i", "row": r["row"], "value": ci})
        if cii > lim["tau"]:
            fails.append({"crit": "ii", "row": r["row"], "value": cii})
    for r in z_rows:
        if not _fin(r["nu"], r["nu2"], r["ref"]) or r["ref"] == 0 or r["nu2"] == 0:
            fails.append({"crit": "nan", "pulse": r["pulse"]})
            continue
        a, b = abs(r["nu"] / r["ref"] - 1), abs(r["nu"] / r["nu2"] - 1)
        worst["iii_ref"], worst["iii_2N"] = max(worst["iii_ref"], a), max(worst["iii_2N"], b)
        if a > lim["z"] or b > lim["z"]:
            fails.append({"crit": "iii", "pulse": r["pulse"], "value_ref": a, "value_2N": b})
    for v in li_values:
        if not _fin(v) or v > lim["li"]:
            fails.append({"crit": "iv", "value": v})
        else:
            worst["li"] = max(worst["li"], float(v))
    return {"pass": not fails, "fails": fails, "worst": worst}


def _s9_need():
    need = list(S9_TAF_ROWS) + list(S9_LIN_ROWS)
    for p in S9_Z_PULSES:
        for r in ("A_k8", "K_k8"):
            if (p, r) not in need:
                need.append((p, r))
    return need


def s9(out: Path, reg_path: Path) -> dict:
    """§8-13 ② – ④: 5 차 등록점 · 수렴 묶음 (Wa 0.1 · G½) 의 고른 펄스를 판 셋 (NU80 · NU160 · 균일 1280 기준판) 으로 →
    τ̂ (5 차 수렴과 같은 잡음 없는 F1) · z · Li → 판정. 판 · 펄스마다 npz + JSONL 점진 기록."""
    import gc
    import c1_grid as gr
    t0 = time.time()
    R = json.loads(Path(reg_path).read_text())
    base = tr.base_inputs(shape="G05", Wa=0.1, x_mid=R["x_mid"])
    runs = {"fresh": base, "A_k8": tr.knob_inputs("A", 0.25, base=base), "K_k8": tr.knob_inputs("K", 0.25, base=base)}
    need = _s9_need()
    od = out / "s9"
    od.mkdir(parents=True, exist_ok=True)
    V, li, cfg_info, errors = {}, {}, {}, []
    stop = None
    for lab, kw in S9_CONFIGS:
        kw = dict(kw)
        if "output_variables" in kw:
            kw["output_variables"] = list(kw["output_variables"])
        if gr.budget_left() < 60:
            stop = "rule7_wallclock"
            break
        tb = time.time()
        try:
            model, solver, sim = tr.build_model("G05", **kw)
        except Exception as e:  # 기준판을 만들지 못함 → 실패 (멈춤)
            errors.append({"cfg": lab, "stage": "build", "error": repr(e)[:400]})
            continue
        e_r = np.asarray(sim.mesh["positive particle"].edges)
        info = {"build_s": time.time() - tb, "n_states": int(model.concatenated_initial_conditions.shape[0]),
                "r_surface_cell_m": float(e_r[-1] - e_r[-2]), "r_centre_cell_m": float(e_r[1] - e_r[0]), "n_r": int(e_r.size - 1)}
        V[lab] = {}
        ts = time.time()
        for (p, run) in need:
            if gr.budget_left() < 60:
                stop = "rule7_wallclock"
                break
            soc, ampsgn = p.split()
            s = soc.replace("SOC", "")
            tp = time.time()
            try:
                res = tr.run_pulse_lean(model, solver, sim, runs[run], x_start=R["soc_x"][s], I_A=R["pulse_I_A"][ampsgn])
            except Exception as e:  # 해법 실패
                errors.append({"cfg": lab, "pulse": p, "run": run, "stage": "solve", "error": repr(e)[:400]})
                continue
            term = [str(x) for x in res["termination"]]
            if any(x != "final time" for x in term):
                errors.append({"cfg": lab, "pulse": p, "run": run, "stage": "termination", "termination": term})
            V[lab][(p, run)] = (res["V"], res["n_pulse"])
            li[f"{lab}|{p}|{run}"] = float(res["li_rel_with_dl"])
            np.savez_compressed(od / f"{lab}__{p.replace(' ', '_')}__{run}.npz", V=res["V"], n_pulse=res["n_pulse"],
                                li=res["li_rel_with_dl"])
            gr.append_jsonl(od / "s9.jsonl", {"cfg": lab, "pulse": p, "run": run, "li": float(res["li_rel_with_dl"]),
                                              "termination": term, "solve_s": time.time() - tp,
                                              "utc": time.strftime("%H:%M:%SZ", time.gmtime())})
            del res
        info["solve_s"] = time.time() - ts
        cfg_info[lab] = info
        del model, solver, sim
        gc.collect()
        print(f"S9 {lab}: n_r {info['n_r']} · surface cell {info['r_surface_cell_m'] * 1e9:.3f} nm · states {info['n_states']} · "
              f"build {info['build_s']:.1f} s · solve {info['solve_s']:.1f} s", flush=True)
        if stop:
            break
    labs = [lab for lab, _ in S9_CONFIGS]

    def tau_of(lab, key):
        if lab not in V or key not in V[lab]:
            return float("nan")
        p, _ = key
        s, ampsgn = p.split()[0].replace("SOC", ""), p.split()[1]
        Vv, n_pulse = V[lab][key]
        return float(gr.f1_noise_free(Vv, n_pulse, R["soc_x"][s], R["pulse_I_A"][ampsgn], 1e-4, R["W_fit_s"][f"G05|SOC{s}"])["tau"])

    def z_of(lab, p):
        try:
            va, vk = V[lab][(p, "A_k8")][0], V[lab][(p, "K_k8")][0]
        except KeyError:
            return float("nan")
        return float(np.linalg.norm(va - vk) / 1e-3) if va.shape == vk.shape else float("nan")

    tau_rows = [{"row": f"{p}|{r}", "nu": tau_of(labs[0], (p, r)), "nu2": tau_of(labs[1], (p, r)), "ref": tau_of(labs[2], (p, r))}
                for (p, r) in list(S9_TAF_ROWS) + list(S9_LIN_ROWS)]
    z_rows = [{"pulse": p, "nu": z_of(labs[0], p), "nu2": z_of(labs[1], p), "ref": z_of(labs[2], p)} for p in S9_Z_PULSES]
    n_expected = len(need) * len(labs)
    v = s9_verdict(tau_rows, z_rows, list(li.values()))
    if errors:
        v["fails"].append({"crit": "solver", "errors": errors})
        v["pass"] = False
    if len(li) != n_expected:
        v["fails"].append({"crit": "incomplete", "n_done": len(li), "n_expected": n_expected})
        v["pass"] = False
    if stop:
        v["fails"].append({"crit": stop})
        v["pass"] = False
    res = {"spike": "S9", "configs": dict(S9_CONFIGS), "cfg_info": cfg_info, "tau_rows": tau_rows, "z_rows": z_rows, "li": li,
           "errors": errors, "stop": stop, "verdict": v, "pass": v["pass"], "limits": S9_LIM, "reg": str(reg_path),
           "elapsed_s": time.time() - t0}
    jdump(res, out / "s9.json")
    for r in tau_rows:
        print(f"S9 τ̂ {r['row']}: nu80 {r['nu'] * 1e3:.4f} · nu160 {r['nu2'] * 1e3:.4f} · ref {r['ref'] * 1e3:.4f} ms", flush=True)
    for r in z_rows:
        print(f"S9 z {r['pulse']}: nu80 {r['nu']:.3f} · nu160 {r['nu2']:.3f} · ref {r['ref']:.3f}", flush=True)
    print(f"S9 worst (i) {v['worst']['i']:.3e} · (ii) {v['worst']['ii']:.3e} · (iii) ref {v['worst']['iii_ref']:.3e} · 2N "
          f"{v['worst']['iii_2N']:.3e} · (iv) Li {v['worst']['li']:.2e} · fails {len(v['fails'])}", flush=True)
    print("S9 PASS" if v["pass"] else "S9 FAIL", flush=True)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["s1", "s2", "s3", "s4", "s5", "s6", "s4p", "s5p", "s8", "s9", "all", "all2", "all5"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--reg", default=None, help="s9: 5 차 S6 등록 파일 (s6_registered.json)")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.which == "s9":
        r = s9(out, Path(a.reg))
        jdump({"s9": r["pass"], "stop": r["stop"]}, out / "spike_status_s9.json")
        import c1_memguard as mg
        rc_mem = mg.rusage_exit_hook()
        if rc_mem is not None:
            return rc_mem
        return 0 if r["pass"] else (4 if r["stop"] else 3)
    if a.which == "all":
        order = ["s6", "s1", "s2", "s3", "s4", "s5"]
    elif a.which == "all2":     # 2 차: S4 (1 차 판정 — 정보로만 다시 잼) + S4′ · S5′ (판정)
        order = ["s6", "s1", "s2", "s3", "s4", "s4p", "s5p"]   # 1 차 S5 는 다시 재지 않는다 (k₀ 정규화가 g_reg 로 바뀌어 같은 식이 자명해짐)
    elif a.which == "all5":     # 5 차: all2 + S8 (제한 출력 동치 · §8-11 ② (c))
        order = ["s6", "s1", "s2", "s3", "s4", "s4p", "s5p", "s8"]
    else:
        order = [a.which]
    info_only = {"s4"} if a.which in ("all2", "all5") else set()
    status = {}
    for w in order:
        r = globals()[w](out)
        status[w] = None if (w == "s6" or w in info_only) else r.get("pass", True)
        if w in info_only:
            status[w + "_info_pass"] = r.get("pass")
    jdump(status, out / "spike_status.json")
    fails = [k for k, v in status.items() if v is False and not k.endswith("_info_pass")]
    print("SPIKES FAIL: " + ",".join(fails) if fails else "SPIKES ALL PASS")
    import c1_memguard as mg
    rc_mem = mg.rusage_exit_hook()                       # §8-11 ③ 교차 확인
    if rc_mem is not None:
        return rc_mem
    return 3 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
