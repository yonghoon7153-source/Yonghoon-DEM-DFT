"""MSC 복합 프로토콜 사전 부호표 (2026-10-05) — 설계안 10종 검토(`docs/MSC_PROTOCOL_DESIGNS_REVIEW_2026-10-05.md`)의 모델 확인.

`scripts/msc_sign_table.py` 의 셀 · 누설 단계 · 열화 판(base · R_up · D_down · SEI · MSC)을 그대로 쓴다.
셀: PyBaMM `Chen2020` (LG M50 ≈ 5 Ah) · SPMe · 공개 파라미터. 누설은 외부 병렬 옴 저항 R_s (셀 전류 = 외부 전류 + V/R_s).
설정값은 전부 이 스크립트가 고른 일반값이다 — 검토한 설계안의 설정값을 옮긴 것이 아니다.

  E1  정전위 대칭 짝 — 휴지 끝 전압 V0 를 잡고 V0+δ · V0−δ 정전위 계단을 번갈아 반복한다. 짝마다 Q_ch − Q_dis (외부 계측).
      본다: 누설이 짝마다 ∫V/R_s 로 더해지는가 · 열화(R_up · D_down)는 ≈ 0 인가 · 시작 과도 · 접근 방향(아래 · 위)의 이완 편향과
      두 방향 평균 · 누설 이력 편향(휴지 중 누설이 만든 분극이 풀리는 시간) · 음극 SEI 가 보이는가 · 1/R_s 비례.
  E2  부분 고리 폐합 — 1C 로 SOC 0.5 에 접근 → 휴지(5 min · 60 min) → 대칭 고리 두 주기(C/2 · C/4) 와 두 전류 고리(C/2 짧게 ↔ C/10 길게).
      본다: 고리 끝 전압 드리프트가 누설을 시간 비례로 잡는가 · 짧은 휴지의 이완이 누설처럼 보이는가 · 두 주기 차분 · 두 전류의 R.
  E3  율 계열 (C/2 · 1C · 2C 전 범위 CC) — Peukert 지수와 (Q_ch − Q_dis) 의 경과 시간 회귀. E3cv 는 양 끝에 CV(C/50) 를 붙여
      시작 · 끝 상태를 맞춘 판.
  E4  (a) 1C 펄스 저항의 R_s 의존과 같은 바이어스 전류만 흘린 base 셀 비교 (병렬 경로 ↔ 작동점) · (b) CV 유지 중 dI/dt 와 전류 차.

⚠ 모델 명제다 (SPMe 한 모델 · 공개 파라미터 한 벌 · OCV 히스테리시스 없음 · 이중층 없음 · 부반응은 음극 SEI 대조군 하나 · 양극 쪽
부반응 없음 · 누설은 옴). RUN_SCOPE 밖(bms-balancing).

실행 (bms-balancing 에서):  python3 -m scripts.msc_protocol_prescreen --out out/msc_prescreen/result.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pybamm

from scripts import msc_sign_table as mst

CAP = 5.0  # Ah (Chen2020 공칭)


def ext(sol, idx, R_s):
    """외부 계측 전류 (방전 +). 누설이 있으면 셀 전류에서 V/R_s 를 뺀다 (CV 단계에서도 같다)."""
    t, v, i_cell = mst.cycle_arrays(sol, idx)
    return t, v, i_cell - (0.0 if R_s is None else v / R_s)


def mAh(t, y):
    return float(np.trapezoid(y, t)) / 3.6


def slope_per_h(t_s, y):
    if len(t_s) < 2:
        return float("nan")
    return float(np.polyfit(np.asarray(t_s) / 3600.0, np.asarray(y), 1)[0])


def sei_loss_mAh(sol, t_a, t_b):
    t = sol["Time [s]"].entries
    lli = sol["Loss of lithium to negative SEI [mol]"].entries
    m = (t >= t_a) & (t <= t_b)
    return float(lli[m][-1] - lli[m][0]) * 96485 / 3.6


# ── E1 정전위 대칭 짝 ─────────────────────────────────────────────────
def e1(kind, R_s, direction, delta=0.010, step_s=60, n_pairs=20, I_app=1.0, dsoc=0.05, rest_s=3600, soc=0.5,
       half_first=False):
    """[휴지 1 h] → [C/5 로 ±5 % 접근] → [휴지 rest_s] → 정전위 짝 n_pairs.

    half_first=False: (+δ, −δ) × n — 짝 = (+δ, −δ).
    half_first=True : [+δ 반] → (−δ, +δ) × n → [−δ 반] — 짝 = (−δ, +δ). 시작 과도를 줄이려는 판.
    """
    soc0 = soc - dsoc if direction == "from_below" else soc + dsoc
    I = -I_app if direction == "from_below" else +I_app
    pre = [mst.cc(0.0, 3600, R_s, period=60),
           mst.cc(I, dsoc * CAP / I_app * 3600, R_s, period=10),
           mst.cc(0.0, rest_s, R_s, period=30)]
    V0 = float(mst.cycle_arrays(mst.simulate(kind, pre, soc0), 2)[1][-1])
    steps = list(pre)
    if half_first:
        steps.append(pybamm.step.voltage(V0 + delta, duration=step_s / 2, period=1))
        for _ in range(n_pairs):
            steps += [pybamm.step.voltage(V0 - delta, duration=step_s, period=1),
                      pybamm.step.voltage(V0 + delta, duration=step_s, period=1)]
        steps.append(pybamm.step.voltage(V0 - delta, duration=step_s / 2, period=1))
    else:
        for _ in range(n_pairs):
            steps += [pybamm.step.voltage(V0 + delta, duration=step_s, period=1),
                      pybamm.step.voltage(V0 - delta, duration=step_s, period=1)]
    sol = mst.simulate(kind, steps, soc0)
    V0_rerun = float(mst.cycle_arrays(sol, 2)[1][-1])
    rows, prev_last_i = [], None
    for k in range(n_pairs):
        if half_first:
            td, vd, idis = ext(sol, 4 + 2 * k, R_s)
            tc, vc, ic = ext(sol, 5 + 2 * k, R_s)
            r_up = 2 * delta / abs(ic[0] - idis[-1])                                       # −δ → +δ 전환
            r_dn = 2 * delta / abs(idis[0] - prev_last_i) if prev_last_i is not None else None
            prev_last_i = ic[-1]
        else:
            tc, vc, ic = ext(sol, 3 + 2 * k, R_s)
            td, vd, idis = ext(sol, 4 + 2 * k, R_s)
            r_up = 2 * delta / abs(ic[0] - prev_last_i) if prev_last_i is not None else None
            r_dn = 2 * delta / abs(idis[0] - ic[-1])                                       # +δ → −δ 전환
            prev_last_i = idis[-1]
        q_ch, q_dis = -mAh(tc, ic), mAh(td, idis)
        leak = 0.0 if R_s is None else mAh(tc, vc / R_s) + mAh(td, vd / R_s)
        rows.append(dict(pair=k + 1, Q_ch_mAh=q_ch, Q_dis_mAh=q_dis, HI_Q_mAh=q_ch - q_dis, truth_leak_mAh=leak,
                         R_step_up_mOhm=None if r_up is None else 1e3 * r_up,
                         R_step_dn_mOhm=None if r_dn is None else 1e3 * r_dn))
    hi = np.array([r["HI_Q_mAh"] for r in rows])
    rs = [r[k] for r in rows for k in ("R_step_up_mOhm", "R_step_dn_mOhm") if r[k] is not None]
    out = dict(kind=kind, R_s=R_s, direction=direction, half_first=half_first, delta_V=delta, step_s=step_s,
               V0=V0, V0_rerun_diff_uV=1e6 * (V0_rerun - V0),
               HI_Q_first_mAh=float(hi[0]), HI_Q_mean_1_5=float(hi[:5].mean()),
               HI_Q_mean_16_20=float(hi[15:20].mean()) if n_pairs >= 20 else None,
               HI_Q_mean_last5=float(hi[-5:].mean()),
               truth_leak_per_pair_mAh=float(np.mean([r["truth_leak_mAh"] for r in rows])),
               R_step_mOhm_median=float(np.median(rs)), rows=rows)
    if kind in ("SEI", "SEI+MSC"):
        t_a = float(mst.cycle_arrays(sol, 3)[0][0])
        t_b = float(sol["Time [s]"].entries[-1])
        out["truth_sei_per_pair_mAh"] = sei_loss_mAh(sol, t_a, t_b) / ((t_b - t_a) / (2 * step_s))
    return out


# ── E2 부분 고리 폐합 ─────────────────────────────────────────────────
def e2(kind, R_s, approach_rest_s, pattern, n_loops=20, soc=0.5, dsoc_app=0.05):
    soc0 = soc - dsoc_app
    steps = [mst.cc(0.0, 3600, R_s, period=60),
             mst.cc(-CAP, dsoc_app * 3600, R_s, period=5),          # 1C 로 5 % 충전해 SOC 0.5 에 접근
             mst.cc(0.0, approach_rest_s, R_s, period=10)]
    if pattern in ("sym_C2", "sym_C4"):
        I = 2.5 if pattern == "sym_C2" else 1.25
        d = 0.05 * CAP / I * 3600
        loop = [(-I, d), (0.0, 60), (+I, d), (0.0, 60)]
    elif pattern == "two_current":
        q = 45.0                                                  # A·s (= 0.25 % SOC) — C/2 18 s ↔ C/10 90 s
        loop = [(-2.5, q / 2.5), (0.0, 30), (+0.5, q / 0.5), (0.0, 30),
                (-0.5, q / 0.5), (0.0, 30), (+2.5, q / 2.5), (0.0, 30)]
    else:
        raise ValueError(pattern)
    for _ in range(n_loops):
        for I, d in loop:
            steps.append(mst.cc(I, d, R_s, period=1 if I else 5))
    sol = mst.simulate(kind, steps, soc0)
    n = len(loop)
    t_end, v_end, v_mid, r_hi, r_lo = [], [], [], [], []
    for k in range(n_loops):
        b = 3 + k * n
        tl, vl, _ = mst.cycle_arrays(sol, b + n - 1)
        t_end.append(float(tl[-1]))
        v_end.append(float(vl[-1]))
        if pattern.startswith("sym"):
            v_mid.append(0.5 * (float(mst.cycle_arrays(sol, b)[1][-1]) + float(mst.cycle_arrays(sol, b + 2)[1][-1])))
        else:
            for j, store in ((0, r_hi), (4, r_lo)):               # 충전 펄스 시작 1 s 뒤 전압 − 직전 휴지 끝 전압
                prev_v = float(mst.cycle_arrays(sol, b + j - 1)[1][-1])
                tp, vp, _ = mst.cycle_arrays(sol, b + j)
                store.append(1e3 * (float(np.interp(tp[0] + 1.0, tp, vp)) - prev_v) / abs(loop[j][0]))
    rel_t = [t - t_end[0] for t in t_end]
    out = dict(kind=kind, R_s=R_s, approach_rest_s=approach_rest_s, pattern=pattern,
               loop_period_s=float(sum(d for _, d in loop)), V_end_first=v_end[0], V_end_last=v_end[-1],
               V_end_slope_mV_per_h_all=1e3 * slope_per_h(rel_t, v_end),
               V_end_slope_mV_per_h_last10=1e3 * slope_per_h(rel_t[-10:], v_end[-10:]),
               V_end_closure_per_loop_mV=1e3 * (v_end[-1] - v_end[0]) / (n_loops - 1))
    if v_mid:
        out["V_mid_slope_mV_per_h_all"] = 1e3 * slope_per_h(rel_t, v_mid)
    if r_hi:
        out.update(R_hi_mOhm=float(np.median(r_hi)), R_lo_mOhm=float(np.median(r_lo)))
    t_all, v_all = sol["Time [s]"].entries, sol["Voltage [V]"].entries
    m = t_all >= t_end[0]
    if R_s is not None:
        out["truth_leak_mA"] = 1e3 * float(np.mean(v_all[m])) / R_s
    if kind in ("SEI", "SEI+MSC"):
        out["truth_sei_mA"] = sei_loss_mAh(sol, t_end[0], float(t_all[-1])) * 3600 / float(t_all[-1] - t_end[0])
    return out


# ── E3 율 계열 ────────────────────────────────────────────────────────
def e3(kind, R_s, rates=(0.5, 1.0, 2.0)):
    """전 범위 CC 만 (CV 없음) — 율마다 [충전 → 4.2 V] → 휴지 15 min → [방전 → 2.5 V] → 휴지 30 min."""
    hi = "4.2 V" if R_s is None else pybamm.step.VoltageTermination(4.2, operator=">")
    lo = "2.5 V" if R_s is None else pybamm.step.VoltageTermination(2.5, operator="<")
    steps = [mst.cc(+0.5, 10 * 3600, R_s, period=60, termination=lo), mst.cc(0.0, 1800, R_s, period=60)]
    for c in rates:
        I = c * CAP
        steps += [mst.cc(-I, 3 * 3600 / c, R_s, period=5, termination=hi), mst.cc(0.0, 900, R_s, period=30),
                  mst.cc(+I, 3 * 3600 / c, R_s, period=5, termination=lo), mst.cc(0.0, 1800, R_s, period=60)]
    sol = mst.simulate(kind, steps, 0.2)
    rows = []
    for j, c in enumerate(rates):
        b = 2 + 4 * j
        tc, vc, ic = ext(sol, b, R_s)
        td, vd, idis = ext(sol, b + 2, R_s)
        q_ch, q_dis = -mAh(tc, ic), mAh(td, idis)
        leak = 0.0
        if R_s is not None:
            tt, vv = sol["Time [s]"].entries, sol["Voltage [V]"].entries
            m = (tt >= tc[0]) & (tt <= td[-1])
            leak = float(np.trapezoid(vv[m] / R_s, tt[m])) / 3.6
        rows.append(dict(C_rate=c, Q_ch_mAh=q_ch, Q_dis_mAh=q_dis, dQ_mAh=q_ch - q_dis,
                         elapsed_h=(float(td[-1]) - float(tc[0])) / 3600, truth_leak_mAh=leak))
    I = np.array([r["C_rate"] * CAP for r in rows])
    qd = np.array([r["Q_dis_mAh"] for r in rows])
    el = np.array([r["elapsed_h"] for r in rows])
    s_, c0 = np.polyfit(el, np.array([r["dQ_mAh"] for r in rows]), 1)
    return dict(kind=kind, R_s=R_s, rows=rows, peukert_k=1.0 - float(np.polyfit(np.log(I), np.log(qd), 1)[0]),
                Qdis_2C_over_C2=float(qd[-1] / qd[0]), dQ_vs_time_slope_mA=float(s_), dQ_vs_time_intercept_mAh=float(c0),
                truth_leak_mean_mA=float(sum(r["truth_leak_mAh"] for r in rows) / el.sum()) if R_s else 0.0)


def e3cv(kind, R_s, rates=(0.5, 1.0, 2.0), i_cut="C/50"):
    """E3 와 같되 각 CC 끝에 CV(전기화학 전류 C/50 까지)를 붙여 시작 · 끝 상태를 맞춘다. Peukert 는 CC 방전 몫만으로."""
    hi = "4.2 V" if R_s is None else pybamm.step.VoltageTermination(4.2, operator=">")
    lo = "2.5 V" if R_s is None else pybamm.step.VoltageTermination(2.5, operator="<")
    steps = [mst.cc(+0.5, 10 * 3600, R_s, period=60, termination=lo),
             pybamm.step.voltage(2.5, duration=10 * 3600, period=30, termination=i_cut), mst.cc(0.0, 1800, R_s, period=60)]
    for c in rates:
        I = c * CAP
        steps += [mst.cc(-I, 3 * 3600 / c, R_s, period=5, termination=hi),
                  pybamm.step.voltage(4.2, duration=10 * 3600, period=10, termination=i_cut), mst.cc(0.0, 900, R_s, period=30),
                  mst.cc(+I, 3 * 3600 / c, R_s, period=5, termination=lo),
                  pybamm.step.voltage(2.5, duration=10 * 3600, period=10, termination=i_cut), mst.cc(0.0, 1800, R_s, period=60)]
    sol = mst.simulate(kind, steps, 0.2)
    rows = []
    for j, c in enumerate(rates):
        b = 3 + 6 * j
        segs = [ext(sol, b + m, R_s) for m in range(6)]
        q_ch = -mAh(segs[0][0], segs[0][2]) - mAh(segs[1][0], segs[1][2])
        q_dis = mAh(segs[3][0], segs[3][2]) + mAh(segs[4][0], segs[4][2])
        t_a, t_b = float(segs[0][0][0]), float(segs[5][0][-1])
        leak = sei = 0.0
        tt, vv = sol["Time [s]"].entries, sol["Voltage [V]"].entries
        m = (tt >= t_a) & (tt <= t_b)
        if R_s is not None:
            leak = float(np.trapezoid(vv[m] / R_s, tt[m])) / 3.6
        if kind in ("SEI", "SEI+MSC"):
            sei = sei_loss_mAh(sol, t_a, t_b)
        rows.append(dict(C_rate=c, Q_ch_mAh=q_ch, Q_dis_mAh=q_dis, Q_dis_CC_mAh=mAh(segs[3][0], segs[3][2]),
                         dQ_mAh=q_ch - q_dis, elapsed_h=(t_b - t_a) / 3600, truth_leak_mAh=leak, truth_sei_mAh=sei))
    I = np.array([r["C_rate"] * CAP for r in rows])
    qd = np.array([r["Q_dis_CC_mAh"] for r in rows])
    el = np.array([r["elapsed_h"] for r in rows])
    s_, c0 = np.polyfit(el, np.array([r["dQ_mAh"] for r in rows]), 1)
    tot = float(sum(r["truth_leak_mAh"] + r["truth_sei_mAh"] for r in rows))
    return dict(kind=kind, R_s=R_s, rows=rows, peukert_k_CC=1.0 - float(np.polyfit(np.log(I), np.log(qd), 1)[0]),
                QdisCC_2C_over_C2=float(qd[-1] / qd[0]), dQ_vs_time_slope_mA=float(s_), dQ_vs_time_intercept_mAh=float(c0),
                truth_loss_mean_mA=tot / float(el.sum()))


# ── E4 펄스 R 과 CV ──────────────────────────────────────────────────
def e4_dcir(R_s, soc=0.5, I=5.0, t_R=1.0):
    """60 s 휴지(누설 있으면 그동안 셀이 V/R_s 로 방전) → 1C 방전 펄스 10 s. R = (펄스 직전 − 펄스 t_R 뒤) / I."""
    sol = mst.simulate("base" if R_s is None else "MSC", [mst.cc(0.0, 60, R_s, period=1), mst.cc(+I, 10, R_s, period=0.1)], soc)
    v_before = float(mst.cycle_arrays(sol, 0)[1][-1])
    t1, v1, _ = mst.cycle_arrays(sol, 1)
    return dict(R_s=R_s, R_app_mOhm=1e3 * (v_before - float(np.interp(t1[0] + t_R, t1, v1))) / I)


def e4_dcir_bias(I_bias, soc=0.5, I=5.0, t_R=1.0):
    """누설 없이 base 셀에 바이어스 전류 I_bias 만 흘린 상태에서 같은 펄스 — 작동점(BV 비선형) 몫을 따로 본다."""
    steps = [pybamm.step.current(I_bias, duration=60, period=1) if I_bias else pybamm.step.rest(duration=60, period=1),
             pybamm.step.current(I_bias + I, duration=10, period=0.1)]
    sol = mst.simulate("base", steps, soc)
    v_before = float(mst.cycle_arrays(sol, 0)[1][-1])
    t1, v1, _ = mst.cycle_arrays(sol, 1)
    return dict(I_bias_A=I_bias, R_app_mOhm=1e3 * (v_before - float(np.interp(t1[0] + t_R, t1, v1))) / I)


def e4_cv(kind, R_s, V_hold=4.1, cv_s=600):
    """휴지 30 min → C/2 충전 → 4.1 V → CV 10 min. CV 중 외부 전류(충전 +) 의 평균 dI/dt 와 곡선."""
    term = f"{V_hold} V" if R_s is None else pybamm.step.VoltageTermination(V_hold, operator=">")
    steps = [mst.cc(0.0, 1800, R_s, period=60), mst.cc(-2.5, 4 * 3600, R_s, period=10, termination=term),
             pybamm.step.voltage(V_hold, duration=cv_s, period=1)]
    sol = mst.simulate(kind, steps, 0.3)
    t, v, i_ext = ext(sol, 2, R_s)
    t = t - t[0]
    y = -i_ext
    m = t >= 5
    return dict(kind=kind, R_s=R_s, t=t[m].tolist(), I_mA=(1e3 * y[m]).tolist(),
                mean_dIdt_uA_per_s=1e6 * float(np.mean(np.gradient(y[m], t[m]))), I_end_mA=1e3 * float(y[-1]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out/msc_prescreen/result.json")
    args = ap.parse_args(argv)
    t_start = time.time()
    base_tool = Path(mst.__file__).read_bytes()
    res = dict(script="bms-balancing/scripts/msc_protocol_prescreen.py", model="PyBaMM SPMe", params="Chen2020 (public)",
               pybamm_version=pybamm.__version__, base_tool="bms-balancing/scripts/msc_sign_table.py",
               base_tool_sha256=hashlib.sha256(base_tool).hexdigest(),
               R_up="contact resistance 0.03 Ohm + exchange-current x0.5 (both electrodes)",
               D_down="particle diffusivity x0.3 (both electrodes)",
               SEI="reaction-limited SEI, exchange current x400 (artificial: Li loss rate of the order of the 100 Ohm leak)")
    res["E1"] = []
    for kind, R_s in (("base", None), ("R_up", None), ("D_down", None), ("SEI", None), ("MSC", 100.0), ("MSC", 300.0),
                      ("MSC", 1000.0), ("R_up+MSC", 100.0), ("D_down+MSC", 100.0)):
        for direction in ("from_below", "from_above"):
            for half in (False, True):
                r = e1(kind, R_s, direction, half_first=half, n_pairs=60)
                res["E1"].append(r)
                print("E1", kind, R_s, direction, half, {k: (round(v, 4) if isinstance(v, float) else v)
                                                        for k, v in r.items() if k != "rows"}, flush=True)
    res["E2"] = []
    for kind, R_s in (("base", None), ("R_up", None), ("D_down", None), ("SEI", None), ("MSC", 100.0), ("D_down+MSC", 100.0)):
        for rest in (300, 3600):
            for pattern in ("sym_C2", "sym_C4", "two_current"):
                r = e2(kind, R_s, rest, pattern)
                res["E2"].append(r)
                print("E2", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    res["E3"] = []
    for kind, R_s in (("base", None), ("R_up", None), ("D_down", None), ("SEI", None), ("MSC", 100.0)):
        r = e3(kind, R_s)
        res["E3"].append(r)
        print("E3", kind, R_s, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "rows"}, flush=True)
    res["E3cv"] = []
    for kind, R_s in (("base", None), ("R_up", None), ("D_down", None), ("SEI", None), ("MSC", 100.0),
                      ("R_up+MSC", 100.0), ("D_down+MSC", 100.0)):
        r = e3cv(kind, R_s)
        res["E3cv"].append(r)
        print("E3cv", kind, R_s, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "rows"},
              flush=True)
    res["E4_dcir"] = [e4_dcir(R) for R in (None, 100.0, 30.0, 3.0, 0.3)]
    res["E4_dcir_bias"] = [e4_dcir_bias(b) for b in (0.0, 0.0374, 0.123, 1.23, 12.3)]
    print("E4 dcir", res["E4_dcir"], res["E4_dcir_bias"], flush=True)
    res["E4_cv"] = [e4_cv(k, R) for k, R in (("base", None), ("R_up", None), ("D_down", None), ("MSC", 100.0))]
    for r in res["E4_cv"]:
        print("E4 cv", r["kind"], r["R_s"], round(r["mean_dIdt_uA_per_s"], 3), round(r["I_end_mA"], 2), flush=True)
    res["dvdq_V_per_Ah_soc05"] = mst.dvdq_calibration(soc=0.5)
    res["wall_s"] = time.time() - t_start
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", p, "wall_s", round(res["wall_s"], 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
