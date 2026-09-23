"""MSC 부호표 — P1 · P7 · P8 에서 '정상 열화(저항 증가)' 와 'MSC(누설)' 가 반대로 움직이는가.

`docs/MSC_SEMINAR_2026-09-23_APPLICATION.md` §3 의 구분 원리 중 모델로 미리 볼 수 있는 셋을 PyBaMM 으로 잰다.

  P1  전류 반전 짝 휴지 — [충전 → 휴지] 와 [방전 → 휴지] 의 후기 드리프트를 더한다.
      가설: 분극 이완은 부호가 반대라 합 ≈ 0, 누설은 둘 다 전압을 내려 합 < 0.
  P7  CV 유지 전류를 지수 + 상수로 적합 — 가설: 저항 증가는 τ 를, MSC 는 점근값 I_∞ 를 올린다.
  P2  (부록) 평형 누설 휴지의 ΔV 와 ΔQ 를 SOC 별로 — ΔV 의 SOC 모양이 dV/dQ 에서 오는지.
  P8  부분 고리(±ΔSOC) 폐합 오차를 고리 주기 두 개로 — 가설: MSC 는 주기에 비례해 하향 이동.

셀: PyBaMM `Chen2020` (LG M50, ≈5 Ah), 모델 SPMe. 공개 파라미터만 쓴다(규진팀 원자료 없음).
  base   : 그대로
  R_up   : 정상 열화의 '저항' 판 — 접촉 저항 0.03 Ω 추가 + 두 전극 교환전류 ×0.5
  MSC    : base + 외부 병렬 옴 누설 R_s (셀 전류 = 외부 전류 + V/R_s, 휴지 중에도 흐른다)
  D_down : 정상 열화의 '확산' 판 — 두 전극 입자 확산계수 ×0.3 (휴지 이완을 느리게 하는 쪽)
  R_up+MSC · D_down+MSC: 열화 + 누설

누설은 `pybamm.step.CustomStepImplicit`(대수 제약 I_cell − (I_ext + V/R_s) = 0)로 넣는다. CV 단계는 전압 제어이고,
외부에서 재는 전류는 I_ext = I_cell − V/R_s 로 사후 계산한다. 부호: PyBaMM 은 방전 전류가 양수다.

⚠ 모델 명제다. OCV 히스테리시스 없음(P8 의 '열역학 고리' 는 없다 — 동역학 이완만), 부반응 없음, 누설은 옴.
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
    cells = [("base", None), ("R_up", None), ("D_down", None), ("MSC", R), ("R_up+MSC", R), ("D_down+MSC", R)]
    res = {}
    for kind, R_s in cells:
        # params() 는 R_up·D_down 계열만 바꾼다 — "MSC" 는 base 파라미터 + 누설
        # P7_6h: 1 h 창의 '점근값' 이 참 점근값인지(확산 꼬리는 0 으로, 누설은 V/R_s 로) 보려는 긴 유지
        res[kind] = dict(P1=p1(kind, R_s), P7=p7(kind, R_s), P7_6h=p7(kind, R_s, cv_s=6 * 3600),
                         P8=p8(kind, R_s))
        print(kind, json.dumps(res[kind], ensure_ascii=False))
    res["P2_MSC_rest_vs_soc"] = p2(R)
    out = dict(script="bms-balancing/scripts/msc_sign_table.py", model="PyBaMM SPMe", params="Chen2020 (public)",
               pybamm_version=pybamm.__version__, R_s_ohm=R,
               R_up="contact resistance 0.03 Ohm + exchange-current x0.5 (both electrodes)",
               D_down="particle diffusivity x0.3 (both electrodes)", results=res)
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
