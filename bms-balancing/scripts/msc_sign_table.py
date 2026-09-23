"""MSC 부호표 — P1 · P5 · P7 · P8 에서 '정상 열화(저항 증가)' 와 'MSC(누설)' 가 반대로 움직이는가.

`docs/MSC_SEMINAR_2026-09-23_APPLICATION.md` §3 의 구분 원리 중 모델로 미리 볼 수 있는 셋을 PyBaMM 으로 잰다.

  P1  전류 반전 짝 휴지 — [충전 → 휴지] 와 [방전 → 휴지] 의 후기 드리프트를 더한다.
      가설: 분극 이완은 부호가 반대라 합 ≈ 0, 누설은 둘 다 전압을 내려 합 < 0.
  P7  CV 유지 전류를 지수 + 상수로 적합 — 가설: 저항 증가는 τ 를, MSC 는 점근값 I_∞ 를 올린다.
  P2  (부록) 평형 누설 휴지의 ΔV 와 ΔQ 를 SOC 별로 — ΔV 의 SOC 모양이 dV/dQ 에서 오는지.
  P8  부분 고리(±ΔSOC) 폐합 오차를 고리 주기 두 개로 — 가설: MSC 는 주기에 비례해 하향 이동.
  P5  C-rate 계단(올렸다 내림) — ΔV–I 기울기(R)와 전압 기반 전하 결손의 시간 비례분을 분리한다.
  두 장부  같은 추가 보관 구간의 전하 손실을 전압 복귀(pOCV 환산) 와 쿨롱 계수(Q_in − Q_out, 컷오프–컷오프) 로 잰다.
      가설: MSC 는 두 장부가 같고, SEI(음극만의 리튬 손실) 는 전압 장부 ≪ 쿨롱 장부.

셀: PyBaMM `Chen2020` (LG M50, ≈5 Ah), 모델 SPMe. 공개 파라미터만 쓴다(규진팀 원자료 없음).
  base   : 그대로
  R_up   : 정상 열화의 '저항' 판 — 접촉 저항 0.03 Ω 추가 + 두 전극 교환전류 ×0.5
  MSC    : base + 외부 병렬 옴 누설 R_s (셀 전류 = 외부 전류 + V/R_s, 휴지 중에도 흐른다)
  D_down : 정상 열화의 '확산' 판 — 두 전극 입자 확산계수 ×0.3 (휴지 이완을 느리게 하는 쪽)
  SEI · SEI+MSC : 부반응 대조군 — reaction-limited SEI, 교환전류 ×400 (누설과 같은 크기의 시간 비례 Li 손실을 만들려는 인위 설정)
  R_up+MSC · D_down+MSC: 열화 + 누설

누설은 `pybamm.step.CustomStepImplicit`(대수 제약 I_cell − (I_ext + V/R_s) = 0)로 넣는다. CV 단계는 전압 제어이고,
외부에서 재는 전류는 I_ext = I_cell − V/R_s 로 사후 계산한다. 부호: PyBaMM 은 방전 전류가 양수다.

⚠ 모델 명제다. OCV 히스테리시스 없음(P8 의 '열역학 고리' 는 없다 — 동역학 이완만), 부반응은 SEI 대조군 하나뿐, 누설은 옴.
RUN_SCOPE 밖(bms-balancing).

실행:  python3 -m scripts.msc_sign_table --out out/msc_sign/result.json
"""
from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
import pybamm  # noqa: E402

pybamm.set_logging_level("ERROR")


def params(kind: str):
    pv = pybamm.ParameterValues("Chen2020")
    opts = {}
    if kind in ("D_down", "D_down+MSC"):
        for key in ("Negative particle diffusivity [m2.s-1]", "Positive particle diffusivity [m2.s-1]"):
            f = pv[key]
            pv[key] = (lambda f: (lambda *a: 0.3 * f(*a)))(f) if callable(f) else 0.3 * f
    if kind in ("SEI", "SEI+MSC"):
        # 부반응 대조군: reaction-limited SEI, 교환전류 ×400 → 휴지 중 LLI ≈ 36 mAh/h (100 Ω 누설 ≈ 37 mA 와 같은 크기).
        # 실셀 속도가 아니라 '누설과 같은 크기의 시간 비례 손실' 을 만들려고 인위적으로 키운 것이다.
        opts["SEI"] = "reaction limited"
        pv["SEI reaction exchange current density [A.m-2]"] = 400 * pv["SEI reaction exchange current density [A.m-2]"]
    if kind in ("R_up", "R_up+MSC"):
        opts["contact resistance"] = "true"
        pv.update({"Contact resistance [Ohm]": 0.03}, check_already_exists=False)
        for key in ("Negative electrode exchange-current density [A.m-2]",
                    "Positive electrode exchange-current density [A.m-2]"):
            f = pv[key]
            pv[key] = (lambda f: (lambda *a: 0.5 * f(*a)))(f)
    return pv, opts


class LeakStep(pybamm.step.CustomStepImplicit):
    """외부 전류 I_ext + 병렬 누설 R_s. 대수 제약 I_cell − (I_ext + V/R_s) = 0.

    PyBaMM 26.8 의 `CustomStepImplicit` 은 `hash_args=None` 이라 함수가 달라도 모든 사용자 정의 단계가 `==` 로
    같고, 실험은 첫 단계의 모델을 나머지에 재사용한다(누설 휴지 뒤 충전이 휴지로 돌았다 —
    `tests/test_msc_sign_table.py`). 그래서 (I_ext, R_s, 종료 조건) 을 식별자로 박는다.
    `Experiment` 는 단계를 `copy()` 로 복제하는데 부모의 `copy` 는 `CustomStepImplicit` 을 새로 만들어 식별자를
    잃으므로 `copy` 도 덮는다.
    """

    def __init__(self, I_ext_A, R_s, termination=None, **kw):
        f = lambda v: v["Current [A]"] - (I_ext_A + v["Voltage [V]"] / R_s)  # noqa: E731
        super().__init__(f, control="algebraic", termination=termination, **kw)
        self._leak_args = (I_ext_A, R_s, termination, kw)
        term = getattr(termination, "value", termination)
        op = getattr(termination, "operator", None)
        self.hash_args = f"I_ext={I_ext_A!r}, R_s={R_s!r}, term={term!r}{op or ''}"
        # `Experiment` 는 `repr(step)`(= repr_args, 부모에서 None) 로도 단계를 합친다 → 길이·주기까지 넣는다
        self.repr_args = f"{self.hash_args}, duration={self.duration!r}, period={self.period!r}"

    def copy(self):
        I_ext_A, R_s, termination, kw = self._leak_args
        return LeakStep(I_ext_A, R_s, termination=termination, **kw)


def cc(I_ext_A, dur_s, R_s, period=10, termination=None):
    """정전류 (외부 전류 I_ext, 방전 +). 누설이 있으면 셀 전류 = I_ext + V/R_s."""
    if R_s is None:
        if I_ext_A == 0:
            return pybamm.step.rest(duration=dur_s, period=period)
        return pybamm.step.current(I_ext_A, duration=dur_s, period=period, termination=termination)
    return LeakStep(I_ext_A, R_s, termination=termination, duration=dur_s, period=period)


def simulate(kind, steps, initial_soc):
    pv, opts = params(kind)
    model = pybamm.lithium_ion.SPMe(opts)
    sim = pybamm.Simulation(model, parameter_values=pv, experiment=pybamm.Experiment(steps))
    sol = sim.solve(initial_soc=initial_soc)
    return sol


def cycle_arrays(sol, idx):
    s = sol.cycles[idx]
    return (np.asarray(s["Time [s]"].entries), np.asarray(s["Voltage [V]"].entries),
            np.asarray(s["Current [A]"].entries))


def late_drift(t, v, window_s):
    m = t >= t[-1] - window_s
    return float(v[m][-1] - v[m][0])


# ── P1 ────────────────────────────────────────────────────────────────
def p1(kind, R_s, I=1.0, pulse_s=600, rest_s=3600, window_s=1200):
    steps = [cc(0.0, 3600, R_s),                  # 0 전처리 휴지
             cc(-I, pulse_s, R_s), cc(0.0, rest_s, R_s),    # 1,2 충전 → 휴지
             cc(+I, pulse_s, R_s), cc(0.0, rest_s, R_s)]    # 3,4 방전 → 휴지
    sol = simulate(kind, steps, 0.5)
    t2, v2, _ = cycle_arrays(sol, 2)
    t4, v4, _ = cycle_arrays(sol, 4)
    t0, v0, _ = cycle_arrays(sol, 0)
    d_c, d_d = late_drift(t2, v2, window_s), late_drift(t4, v4, window_s)
    return dict(drift_after_charge_mV=1e3 * d_c, drift_after_discharge_mV=1e3 * d_d,
                sum_mV=1e3 * (d_c + d_d), pre_rest_drift_mV=1e3 * late_drift(t0, v0, window_s))


# ── P7 ────────────────────────────────────────────────────────────────
def p7(kind, R_s, V_hold=4.1, cv_s=3600):
    # 사용자 정의 단계는 충·방전 방향을 모르므로 "4.1 V" 문자열 종료가 무시된다 → 연산자 명시
    term = f"{V_hold} V" if R_s is None else pybamm.step.VoltageTermination(V_hold, operator=">")
    steps = [cc(-2.5, 7200, R_s, termination=term), pybamm.step.voltage(V_hold, duration=cv_s, period=10)]
    sol = simulate(kind, steps, 0.3)
    t, v, i_cell = cycle_arrays(sol, 1)
    t = t - t[0]
    i_ext = i_cell - (0.0 if R_s is None else v / R_s)      # 외부 계측 전류 (충전 = 음수)
    y = -i_ext                                               # 충전 전류 크기
    from scipy.optimize import curve_fit
    m = t >= 60
    f = lambda tt, a, tau, c: a * np.exp(-tt / tau) + c      # noqa: E731
    p0 = (max(y[m][0] - y[m][-1], 1e-4), 600.0, max(y[m][-1], 1e-5))
    try:
        (a, tau, c), _ = curve_fit(f, t[m], y[m], p0=p0, maxfev=20000)
    except Exception as e:                                   # noqa: BLE001
        a = tau = c = float("nan")
        print("[P7] fit failed", kind, e)
    t_half = float(t[m][np.argmin(np.abs(y[m] - (y[m][0] + y[m][-1]) / 2))])
    return dict(tau_s=float(tau), I_inf_mA=1e3 * float(c), amp_mA=1e3 * float(a),
                I_end_mA=1e3 * float(y[-1]), t_half_s=t_half)


# ── P2 ────────────────────────────────────────────────────────────────
def p2(R_s, socs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), rest_s=7200):
    """평형(초기 SOC) 에서 누설 휴지만. ΔV 는 SOC 따라 크게 변하고 ΔQ(= ∫V/R_s dt) 는 거의 일정한가."""
    rows = []
    for soc in socs:
        sol = simulate("MSC", [cc(0.0, rest_s, R_s, period=60)], soc)
        t, v, i_cell = cycle_arrays(sol, 0)
        dq_mAh = float(np.trapezoid(i_cell, t)) / 3.6
        dv_mV = 1e3 * float(v[-1] - v[0])
        rows.append(dict(soc=soc, V0=float(v[0]), dV_mV=dv_mV, dQ_mAh=dq_mAh, dVdQ_mV_per_mAh=dv_mV / dq_mAh))
    return rows


# ── P5 ────────────────────────────────────────────────────────────────
def dvdq_calibration(dq_Ah=0.1, I=0.5, soc=0.5):
    """base 셀 SOC(기본 0.5) 에서 저율 충전 ΔQ 뒤 1 h 휴지 → 셀 OCV 기울기 dV/dQ [V/Ah] (충전 방향 +)."""
    sol = simulate("base", [cc(0.0, 1800, None), cc(-I, dq_Ah / I * 3600, None), cc(0.0, 3600, None)], soc)
    v_before = cycle_arrays(sol, 0)[1][-1]
    v_after = cycle_arrays(sol, 2)[1][-1]
    return float((v_after - v_before) / dq_Ah)


def p5(kind, R_s, dvdq_V_per_Ah, levels=(0.25, 0.5, 1.0, 2.5, 5.0, 5.0, 2.5, 1.0, 0.5, 0.25),
       dq_Ah=0.2, rest_s=1800, t_R=10.0, soc=0.5):
    """C-rate 계단(올렸다 내림). 단계마다 [충전 ΔQ → 방전 ΔQ → 휴지] (외부 전하는 0 으로 맞춤).

    관측량 두 개 (실험에서 잴 수 있는 것만 쓴다):
      ΔV–I 기울기  : 충전 시작 t_R 초 뒤 전압 − 직전 휴지 끝 전압, 을 I 에 대해 직선 적합 → R_fit [Ω]
      전하 결손    : 휴지 끝 전압의 단계 간 변화 ÷ dV/dQ → 결손 [mAh], 을 단계 경과 시간에 대해 직선 적합
                     → 기울기 [mA] = 시간 비례분, 절편 [mAh] = 시간 무관분
    truth(관측 불가, 대조용): MSC 는 ∫V/R_s dt, SEI 는 음극 SEI 로 잃은 Li.
    """
    steps = [cc(0.0, rest_s, R_s, period=30)]
    for I in levels:
        d = dq_Ah / I * 3600
        steps += [cc(-I, d, R_s, period=2), cc(+I, d, R_s, period=2), cc(0.0, rest_s, R_s, period=30)]
    sol = simulate(kind, steps, soc)
    rows = []
    for k, I in enumerate(levels):
        t_prev, v_prev, _ = cycle_arrays(sol, 3 * k)
        t_c, v_c, _ = cycle_arrays(sol, 3 * k + 1)
        t_end, v_end, _ = cycle_arrays(sol, 3 * k + 3)
        dv_R = float(np.interp(t_c[0] + t_R, t_c, v_c) - v_prev[-1])
        closure = float(v_end[-1] - v_prev[-1])
        rows.append(dict(I_A=I, dV_at_tR_mV=1e3 * dv_R, R_mOhm=1e3 * dv_R / I,
                         elapsed_h=float(t_end[-1] - t_prev[-1]) / 3600, closure_mV=1e3 * closure,
                         deficit_mAh=-1e3 * closure / dvdq_V_per_Ah))
    I_arr = np.array([r["I_A"] for r in rows])
    dv_arr = np.array([r["dV_at_tR_mV"] for r in rows])
    el = np.array([r["elapsed_h"] for r in rows])
    de = np.array([r["deficit_mAh"] for r in rows])
    R_slope, _ = np.polyfit(I_arr, dv_arr, 1)
    d_slope, d_icpt = np.polyfit(el, de, 1)
    total_h = float(sol["Time [s]"].entries[-1] - sol["Time [s]"].entries[0]) / 3600
    truth = None
    if R_s is not None:
        t_all, v_all = sol["Time [s]"].entries, sol["Voltage [V]"].entries
        truth = float(np.trapezoid(v_all / R_s, t_all)) / 3.6 / total_h            # mA
    elif kind == "SEI":
        lli = sol["Loss of lithium to negative SEI [mol]"].entries
        truth = float(lli[-1] - lli[0]) * 96485 / 3.6 / total_h                     # mA
    return dict(R_fit_mOhm=float(R_slope), deficit_slope_mA=float(d_slope), deficit_intercept_mAh=float(d_icpt),
                truth_loss_mA=truth, dvdq_V_per_Ah=dvdq_V_per_Ah, soc=soc, rows=rows)


# ── 두 장부 비교 ─────────────────────────────────────────────────────
def pseudo_ocv_table(I=0.1):
    """base 셀 C/50 방전·충전 곡선의 평균 → (V, Q_from_bottom[Ah]) 표. 전압 장부의 환산에 쓴다 (실험의 pOCV 역할)."""
    dis = simulate("base", [pybamm.step.current(I, duration=60 * 3600, period=60, termination="2.5 V")], 1.0)
    chg = simulate("base", [pybamm.step.current(-I, duration=60 * 3600, period=60, termination="4.2 V")], 0.0)
    td, vd = dis["Time [s]"].entries, dis["Voltage [V]"].entries
    tc, vc = chg["Time [s]"].entries, chg["Voltage [V]"].entries
    qd = I * (td[-1] - td) / 3600                        # 바닥에서 잰 전하 (방전 곡선)
    qc = I * (tc - tc[0]) / 3600
    q = np.linspace(max(qd.min(), qc.min()), min(qd.max(), qc.max()), 2000)
    v = 0.5 * (np.interp(q, qd[::-1], vd[::-1]) + np.interp(q, qc, vc))
    return v, q


def two_ledgers(kind, R_s, ocv, soc=0.5, T1_h=1.0, T2_h=5.0, I=1.0, cap_Ah=5.0):
    """같은 '추가 보관 구간'(T2 − T1) 의 전하 손실을 두 장부로 잰다.

    한 번의 실행: [방전 → 2.5 V] → 휴지 1 h → [충전 Q_in = soc·cap] → 휴지 1 h(이완) → 보관 T → [방전 → 2.5 V]
      전압 장부  : 보관 시작 전압(이완 뒤) 과 끝 전압을 pOCV 표로 전하로 바꾼 차이
      쿨롱 장부  : Q_in − Q_out (외부 계측 전하. 넣었는데 컷오프까지 못 꺼낸 전하)
    T1 · T2 두 실행의 차분이 추가 보관 구간만 남긴다 (충·방전 중 누설·분극·SEI 몫은 상쇄).
    """
    v_tab, q_tab = ocv
    q_of_v = lambda v: float(np.interp(v, v_tab, q_tab))  # noqa: E731
    lo = "2.5 V" if R_s is None else pybamm.step.VoltageTermination(2.5, operator="<")
    runs = {}
    for T in (T1_h, T2_h):
        q_in = soc * cap_Ah
        steps = [cc(+I, 10 * 3600, R_s, termination=lo), cc(0.0, 3600, R_s, period=60),
                 cc(-I, q_in / I * 3600, R_s, period=30), cc(0.0, 3600, R_s, period=60),
                 cc(0.0, T * 3600, R_s, period=60), cc(+I, 10 * 3600, R_s, termination=lo)]
        sol = simulate(kind, steps, 0.5)
        _, v_relax, _ = cycle_arrays(sol, 3)
        _, v_store, _ = cycle_arrays(sol, 4)
        t_out, _, _ = cycle_arrays(sol, 5)
        q_out = I * float(t_out[-1] - t_out[0]) / 3600
        leak = sei = 0.0                                  # 대조용 실제 손실 (관측 불가) — 누설 몫과 SEI 몫을 따로
        if R_s is not None:
            leak = float(np.trapezoid(sol["Voltage [V]"].entries / R_s, sol["Time [s]"].entries)) / 3600
        if kind in ("SEI", "SEI+MSC"):
            lli = sol["Loss of lithium to negative SEI [mol]"].entries
            sei = float(lli[-1] - lli[0]) * 96485 / 3600
        runs[T] = dict(q_in_Ah=q_in, q_out_Ah=q_out, coulomb_deficit_Ah=q_in - q_out,
                       V_store_start=float(v_relax[-1]), V_store_end=float(v_store[-1]),
                       voltage_deficit_Ah=q_of_v(v_relax[-1]) - q_of_v(v_store[-1]),
                       truth_leak_Ah=leak, truth_sei_Ah=sei)
    a, b = runs[T1_h], runs[T2_h]
    d_v = 1e3 * (b["voltage_deficit_Ah"] - a["voltage_deficit_Ah"])
    d_c = 1e3 * (b["coulomb_deficit_Ah"] - a["coulomb_deficit_Ah"])
    t_leak = 1e3 * (b["truth_leak_Ah"] - a["truth_leak_Ah"])
    t_sei = 1e3 * (b["truth_sei_Ah"] - a["truth_sei_Ah"])
    return dict(soc=soc, extra_storage_h=T2_h - T1_h, voltage_ledger_mAh=d_v, coulomb_ledger_mAh=d_c,
                # 쿨롱 장부가 1 mAh 미만이면 비율은 뜻이 없다 (분모 ≈ 0)
                ratio_voltage_over_coulomb=(d_v / d_c) if abs(d_c) > 1.0 else None,
                truth_leak_mAh=t_leak, truth_sei_mAh=t_sei, runs={str(k): v for k, v in runs.items()})


# ── P8 ────────────────────────────────────────────────────────────────
def p8(kind, R_s, dsoc=0.05, cap_Ah=5.0, loops=3, rest_s=1800):
    out = {}
    for label, I in (("fast_C2", 2.5), ("slow_C10", 0.5)):
        dur = dsoc * cap_Ah / I * 3600
        steps = [cc(0.0, rest_s, R_s)]
        for _ in range(loops):
            steps += [cc(-I, dur, R_s), cc(+I, dur, R_s)]
        steps += [cc(0.0, rest_s, R_s)]
        sol = simulate(kind, steps, 0.5)
        _, v0, _ = cycle_arrays(sol, 0)
        _, v_end, _ = cycle_arrays(sol, len(steps) - 1)
        loop_time_h = loops * 2 * dur / 3600
        out[label] = dict(closure_mV=1e3 * float(v_end[-1] - v0[-1]), loop_time_h=loop_time_h)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out/msc_sign/result.json")
    ap.add_argument("--Rs", type=float, default=100.0)
    args = ap.parse_args(argv)
    R = args.Rs
    cells = [("base", None), ("R_up", None), ("D_down", None), ("SEI", None),
             ("MSC", R), ("R_up+MSC", R), ("D_down+MSC", R)]
    res = {}
    dvdq = {soc: dvdq_calibration(soc=soc) for soc in (0.2, 0.5, 0.8)}
    for kind, R_s in cells:
        # params() 는 R_up·D_down 계열만 바꾼다 — "MSC" 는 base 파라미터 + 누설
        # P7_6h: 1 h 창의 '점근값' 이 참 점근값인지(확산 꼬리는 0 으로, 누설은 V/R_s 로) 보려는 긴 유지
        res[kind] = dict(P1=p1(kind, R_s), P7=p7(kind, R_s), P7_6h=p7(kind, R_s, cv_s=6 * 3600),
                         P8=p8(kind, R_s), P5=p5(kind, R_s, dvdq[0.5]))
        print(kind, json.dumps(res[kind], ensure_ascii=False))
    res["P2_MSC_rest_vs_soc"] = p2(R)
    # P5 의 SOC 의존: 전압 기반 결손이 MSC 와 SEI 를 각각 얼마나 잡는가 (흑연 평탄부 ↔ 기울기 구간)
    ocv = pseudo_ocv_table()
    res["two_ledgers"] = {f"{kind}@{soc}": two_ledgers(kind, R_s, ocv, soc=soc)
                          for soc in (0.5, 0.2)
                          for kind, R_s in (("base", None), ("R_up", None), ("D_down", None),
                                            ("MSC", R), ("SEI", None), ("SEI+MSC", R))}
    res["P5_soc_scan"] = {f"{kind}@{soc}": p5(kind, R_s, dvdq[soc], soc=soc)
                          for soc in (0.2, 0.8) for kind, R_s in (("MSC", R), ("SEI", None))}
    out = dict(script="bms-balancing/scripts/msc_sign_table.py", model="PyBaMM SPMe", params="Chen2020 (public)",
               pybamm_version=pybamm.__version__, R_s_ohm=R,
               R_up="contact resistance 0.03 Ohm + exchange-current x0.5 (both electrodes)",
               D_down="particle diffusivity x0.3 (both electrodes)",
               SEI="reaction-limited SEI, exchange current x400 (artificial: matches the 100 Ohm leak rate)",
               dvdq_V_per_Ah=dvdq, results=res)
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
