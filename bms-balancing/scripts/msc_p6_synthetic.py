"""MSC P6 합성 검사 — α·β 하네스가 마이크로 쇼츠(MSC)와 LLI 를 가르는가.

`docs/MSC_SEMINAR_2026-09-23_APPLICATION.md` §3 P6 의 가설:
  순수 MSC 는 내부 자기방전이라 두 전극이 **같이** 방전된다 → 전극 정렬(오프셋 b)이 그대로다.
  LLI 는 정렬을 민다.

이 스크립트는 그 가설을 하네스 적합기(`verify.multistart` + `model.Objective`, 수정 없이)로 잰다.
합성 truth 는 PyBaMM 공개 파라미터(Chen2020_composite) 의 OCP 로 만든다 — 규진팀 원자료는 쓰지 않는다.

두 경우를 가른다:
  (A) **RPT 사이의** MSC — RPT 가 컷오프에서 컷오프까지 가면 직전 상태는 지워진다 → 곡선 불변(자명).
  (B) **RPT 도중의** MSC — 측정 중 새는 전하가 **계수 용량 축을 늘이거나 줄인다**:
        방전 RPT: 실제 dq/dt = −(I + V/R_s), 계수 dQ = I dt  → 계수 용량 < 참
        충전 RPT: 실제 dq/dt =  (I − V/R_s), 계수 dQ = I dt  → 계수 용량 > 참
      하네스의 모드 식(`degradation_modes`)은 `a·c`, `(a+b_PE−b_NE)·c` 로 정규화되므로, 축이 균일하게
      늘거나 줄면 a·b 는 그대로이고 c 만 바뀐다 → **LAM_PE = LAM_NE = LLI 가 같은 크기로** 움직이는
      공통 모드 가짜 열화가 예상된다. 이것을 숫자로 확인한다.

OCV 만 쓴다(분극 0) — 누설 효과만 떼어 보기 위해서다. 실제 pOCV 의 분극은 별도 교란이다.
RUN_SCOPE 밖(bms-balancing). 원자료 없이 돈다.

실행:  python3 -m scripts.msc_p6_synthetic --out out/msc_p6/result.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")

from bms_balancing.model import Blend, Objective, degradation_modes, differential, _interp_lin_extrap  # noqa: E402
from bms_balancing.verify import multistart  # noqa: E402

V_LO, V_HI = 3.0, 4.2           # 셀 컷오프 [V]
GAMMA_TRUE = 0.10               # 음극 Si 분율 (truth)
Q_P, Q_N = 3.40, 3.40           # 전극 용량 [Ah]
QP0, QN0 = -0.65, -1.00         # 전극 오프셋 [Ah] (q 원점 기준)
# ⇒ truth p ≈ [1.204, −0.053, 1.204, −0.177, 0.10], 창 c ≈ 2.83 Ah — 하네스 상자(LB5/UB5) 안,
#   전극 사용 구간 x_P ∈ [0.044, 0.875] · x_N ∈ [0.147, 0.978] (OCP 자료 범위 안, 외삽 없음)


# ── truth OCP (PyBaMM Chen2020_composite, 공개) ──────────────────────────
def _pybamm_ocp():
    import pybamm
    pv = pybamm.ParameterValues("Chen2020_composite")

    def ev(key, sto):
        f = pv[key]
        return np.array([float(np.asarray(f(pybamm.Scalar(float(s))).evaluate()).ravel()[0]) for s in sto])

    y = np.linspace(0.0, 1.0, 801)
    # 양극: 하네스 규약 x_P = 탈리튬 분율 → 전압 증가. 리튬화 y = 0.995 − 0.85 x
    pe_v = ev("Positive electrode OCP [V]", 0.995 - 0.85 * y)
    # 음극 문헌 곡선: 리튬화 용량(0→1)과 전압(감소) — Blend 가 받는 형식
    sto = np.linspace(0.02, 0.95, 801)
    gr_v = ev("Primary: Negative electrode OCP [V]", sto)
    si_v = ev("Secondary: Negative electrode OCP [V]", sto)
    cap = (sto - sto[0]) / (sto[-1] - sto[0])
    return y, pe_v, cap, gr_v, cap, si_v


class SynthHalf:
    """`model.HalfCell` 과 같은 인터페이스(E_PE, dv_PE)를 합성 배열로."""

    def __init__(self, pe_capacity, pe_voltage, window=9, poly_order=1):
        self.pe_capacity, self.pe_voltage = np.asarray(pe_capacity), np.asarray(pe_voltage)
        self._d_pe = differential(self.pe_capacity, self.pe_voltage, window, poly_order)

    def E_PE(self, x):
        return _interp_lin_extrap(self.pe_capacity, self.pe_voltage, x)

    def dv_PE(self, x):
        return _interp_lin_extrap(self._d_pe.capacity_uniform2, self._d_pe.dvdq, x)


# ── 물리 셀 → 곡선 ─────────────────────────────────────────────────────
def cell_voltage(q, half, blend, Qp, Qn, qp0, qn0, gamma):
    xp = (q - qp0) / Qp
    xn = (q - qn0) / Qn
    return half.E_PE(xp) - blend.E(np.atleast_1d(xn), gamma)


def window(half, blend, Qp, Qn, qp0, qn0, gamma, n=20001):
    q = np.linspace(-0.5, 4.5, n)
    v = cell_voltage(q, half, blend, Qp, Qn, qp0, qn0, gamma)
    ok = np.where((v >= V_LO) & (v <= V_HI))[0]
    if len(ok) == 0:
        raise ValueError("컷오프 창이 비었다")
    return q[ok[0]], q[ok[-1]]


def truth_p(Qp, Qn, qp0, qn0, qmin, qmax, gamma):
    c = qmax - qmin
    return np.array([Qp / c, (qp0 - qmin) / c, Qn / c, (qn0 - qmin) / c, gamma]), c


def measured_curve(half, blend, Qp, Qn, qp0, qn0, gamma, *, direction, I, R_s, n=3001):
    """누설이 있는 RPT 에서 계수된 (용량, 전압). R_s=inf 면 누설 0."""
    qmin, qmax = window(half, blend, Qp, Qn, qp0, qn0, gamma)
    q = np.linspace(qmin, qmax, n)
    v = cell_voltage(q, half, blend, Qp, Qn, qp0, qn0, gamma)
    leak = np.zeros_like(v) if not np.isfinite(R_s) else v / R_s
    if direction == "discharge":
        # q 가 qmax → qmin 으로 간다. 계수 dQ = I dt, 실제 |dq| = (I+leak) dt
        dQ_dq = I / (I + leak)
        qq, vv, g = q[::-1], v[::-1], dQ_dq[::-1]
    else:
        if np.isfinite(R_s) and np.any(I - leak <= 0):
            raise ValueError("충전 전류가 누설보다 작다")
        dQ_dq = I / (I - leak)
        qq, vv, g = q, v, dQ_dq
    dq = np.abs(np.diff(qq))
    Qc = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * dq)])
    return Qc, vv, (qmin, qmax)


def fit(half, blend, cap, volt, *, n_starts, seed, objective_version):
    obj = Objective(half, blend, cap, volt, objective_version=objective_version)
    best, val, _ = multistart(obj, n_starts=n_starts, seed=seed)
    return obj, best, val


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out/msc_p6/result.json")
    ap.add_argument("--starts", type=int, default=24)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--objective-version", default="chain_rule_v2")
    args = ap.parse_args(argv)

    y, pe_v, gr_c, gr_v, si_c, si_v = _pybamm_ocp()
    half = SynthHalf(y, pe_v)
    blend = Blend(si_c, si_v, gr_c, gr_v)
    inputs_sha = hashlib.sha256(np.concatenate([pe_v, gr_v, si_v]).tobytes()).hexdigest()

    C_nom = 2.83                 # 공칭 [Ah] ≈ 창 용량
    rows = []

    def run(name, *, Qp=Q_P, Qn=Q_N, qp0=QP0, qn0=QN0, direction="discharge", c_rate=0.05, R_s=np.inf):
        I = c_rate * C_nom
        cap, volt, (qmin, qmax) = measured_curve(half, blend, Qp, Qn, qp0, qn0, GAMMA_TRUE,
                                                 direction=direction, I=I, R_s=R_s)
        p_t, c_t = truth_p(Qp, Qn, qp0, qn0, qmin, qmax, GAMMA_TRUE)
        obj, p_fit, val = fit(half, blend, cap, volt, n_starts=args.starts, seed=args.seed,
                              objective_version=args.objective_version)
        return dict(name=name, direction=direction, c_rate=c_rate, R_s=None if not np.isfinite(R_s) else R_s,
                    c_true=float(c_t), c_meas=float(obj.c_cell), p_true=p_t.tolist(), p_fit=p_fit.tolist(),
                    obj=float(val), rmse_pocv_mV=1e3 * obj.rmse_pocv(p_fit),
                    leak_over_I_at_3V7=(0.0 if not np.isfinite(R_s) else 3.7 / R_s / I))

    ref = run("pristine_noleak")
    rows.append(ref)
    p_ref, c_ref = np.array(ref["p_fit"]), ref["c_meas"]
    p_ref_t, c_ref_t = np.array(ref["p_true"]), ref["c_true"]

    scen = [
        ("MSC_300ohm_discharge_C20", dict(R_s=300.0, direction="discharge", c_rate=0.05)),
        ("MSC_300ohm_discharge_C10", dict(R_s=300.0, direction="discharge", c_rate=0.10)),
        ("MSC_300ohm_charge_C20",    dict(R_s=300.0, direction="charge", c_rate=0.05)),
        ("MSC_1000ohm_discharge_C20", dict(R_s=1000.0, direction="discharge", c_rate=0.05)),
        ("LLI_3pct_noleak",          dict(qn0=QN0 + 0.03 * C_nom)),
        ("LAMPE_3pct_noleak",        dict(Qp=Q_P * 0.97)),
        ("LLI_3pct_plus_MSC_300ohm_discharge_C20", dict(qn0=QN0 + 0.03 * C_nom, R_s=300.0,
                                                        direction="discharge", c_rate=0.05)),
    ]
    for name, kw in scen:
        r = run(name, **kw)
        r["modes_fit"] = degradation_modes(p_ref, c_ref, np.array(r["p_fit"]), r["c_meas"])
        r["modes_true"] = degradation_modes(p_ref_t, c_ref_t, np.array(r["p_true"]), r["c_true"])
        r["dp_fit_minus_ref"] = (np.array(r["p_fit"]) - p_ref).tolist()
        rows.append(r)

    out = dict(
        script="bms-balancing/scripts/msc_p6_synthetic.py",
        truth_source="PyBaMM Chen2020_composite OCPs (public); no BML raw data",
        inputs_sha256=inputs_sha, objective_version=args.objective_version,
        starts=args.starts, seed=args.seed, cutoffs=[V_LO, V_HI], gamma_true=GAMMA_TRUE,
        electrodes=dict(Q_P=Q_P, Q_N=Q_N, qp0=QP0, qn0=QN0, C_nom=C_nom),
        rows=rows,
    )
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False))

    print(f"{'scenario':42s} {'leak/I':>7s} {'c_meas/c_ref':>12s} {'LAM_PE':>8s} {'LAM_NE':>8s} {'LLI':>8s} "
          f"{'Δb_PE':>8s} {'Δb_NE':>8s} {'rmse mV':>8s}")
    for r in rows[1:]:
        m, d = r["modes_fit"], r["dp_fit_minus_ref"]
        print(f"{r['name']:42s} {r['leak_over_I_at_3V7']:7.3f} {r['c_meas']/c_ref:12.4f} "
              f"{m['LAM_PE']:8.4f} {m['LAM_NE']:8.4f} {m['LLI']:8.4f} {d[1]:8.4f} {d[3]:8.4f} {r['rmse_pocv_mV']:8.3f}")
        mt = r["modes_true"]
        print(f"{'   └ truth':42s} {'':7s} {r['c_true']/c_ref_t:12.4f} "
              f"{mt['LAM_PE']:8.4f} {mt['LAM_NE']:8.4f} {mt['LLI']:8.4f}")
    print(f"[ref] rmse_pocv {ref['rmse_pocv_mV']:.3f} mV · p_fit {np.round(p_ref, 4).tolist()} · "
          f"p_true {np.round(p_ref_t, 4).tolist()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
