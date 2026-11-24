"""C1 truth — ASSB 합성 truth 의 forward (설계서 `followups/assb-contact-truth/DESIGN_v1.md` §1–§4 · 경로 P-A).

진단 전용 · smoke · 인용 금지 · 정본 아님. 저장소 밖 버리는 venv (프로필 C 핵심 셋) 에서만 실행한다.

- 모델: `pybamm.lithium_ion.DFN` full · 반쪽전지 (`"working electrode": "positive"` — Li 금속 상대극) ·
  `"surface form": "differential"` · 양극 입자 상 하나 (§1-1).
- 노브 = 매개 바꿈 (§2-3 · P-A): 면적 A = (k₀×f, c_dl×f) · `j₀` K = (k₀×f) · AD 대리 = (k₀×f, c_dl×f, D×f²) ·
  θ = 연결 부피 ε_conn = θ·ε_CAM (+ 모형 밖 장부) · ε_SE (`porosity`) 는 어느 노브도 바꾸지 않는다 (R3).
- 단일 이온 SE: t+ = 1 · κ 상수 (Wa 로 역산) · D_e 상수 · 열역학 인자 1 (§1-3).
- 모든 노브 · 프로토콜 값은 PyBaMM InputParameter 로 넣는다 — 모형 구조 (= g 모양) 하나당 빌드 한 번.
"""
from __future__ import annotations

import hashlib
import time

import numpy as np

# --------------------------------------------------------------------------------------------
# 상수 — 설치본 매개변수 사전 (Chen2020_composite) 에서 읽는다 (§1-4 · S6 에서 사본 configs/base.yaml 과 대조)
# --------------------------------------------------------------------------------------------
F = 96485.33212
R_GAS = 8.314462618
T_K = 298.15
VT = R_GAS * T_K / F                      # RT/F [V]

PV_NAME = "Chen2020_composite"


def _chen():
    import pybamm
    return pybamm.ParameterValues(PV_NAME)


_P = _chen()
EPS_CAM0 = float(_P["Positive electrode active material volume fraction"])   # 0.665
EPS_SE = float(_P["Positive electrode porosity"])                             # 0.335 (= SE 분율로 읽는다)
L_PE = float(_P["Positive electrode thickness [m]"])                          # 7.56e-5
R_P = float(_P["Positive particle radius [m]"])                               # 5.22e-6
C_MAX = float(_P["Maximum concentration in positive electrode [mol.m-3]"])     # 63104
AREA = float(_P["Electrode height [m]"]) * float(_P["Electrode width [m]"])    # 0.1027 m²
BRUGG_E = float(_P["Positive electrode Bruggeman coefficient (electrolyte)"])  # 1.5
SIGMA_S0 = float(_P["Positive electrode conductivity [S.m-1]"])               # 0.18 (전극 Bruggeman 0)
D_S0 = float(_P["Positive particle diffusivity [m2.s-1]"])                    # 4e-15
OCP_FUN = _P["Positive electrode OCP [V]"]
A_SURF0 = 3.0 * EPS_CAM0 / R_P                                                # a [m-1]

# truth 고유 선택 (§1-4 · §8 에 기록)
C_DL0 = 0.1            # F m⁻² = 10 µF cm⁻² (곱 축퇴 페이지 19호 절 규약 — 측정 아님)
RCT_GEO0 = 66e-4       # Ω m² = 66 Ω cm² (109호 R_Ca 자릿수 — 사본 · 입력 후보) · x_mid 에서 맞춘다
CE0 = 1000.0           # mol m⁻³
D_E = 8.794e-11 * (CE0 / 1000) ** 2 - 3.972e-10 * (CE0 / 1000) + 4.862e-10   # Nyman2008 값 @1000 (상수로)
J0_LI = 1.0e4          # A m⁻² — 이상 상대극 (빠른 동역학)
CDL_LI = 0.01          # F m⁻² — 상대극 RC τ_Li = (RT/F)/J0_LI · CDL_LI
V_HIGH, V_LOW = 4.3, 3.0
SHAPES = ("G05", "G2")


def g_shape(shape: str, x):
    """j₀(x) = k₀·g(x) 의 설계 모양 (§2-6 · 정칙화 전). c_e 인자는 상수 (단일 이온 · c_e 균일 가정)."""
    x = np.asarray(x, dtype=float)
    if shape == "G05":
        return np.sqrt(x * (1.0 - x))
    if shape == "G2":
        return (x * (1.0 - x)) ** 2
    raise ValueError(shape)


def _reg_delta() -> float:
    import pybamm
    return float(pybamm.settings.tolerances["reg_power"])


REG_DELTA = _reg_delta()
SHAPE_P = {"G05": 0.5, "G2": 2.0}


def g_reg(shape: str, x):
    """PyBaMM 26.8 이 j₀ FunctionParameter 에 붙이는 RegulariseSqrtAndPower 후처리 뒤의 g (§8-4 S5′ · 사후):
    RegPower(y, p) = y·(y² + δ²)^((p−1)/2) · y = x(1 − x) (사전에 없는 상태 의존 밑수 → 척도 1) · δ = reg_power."""
    if shape not in SHAPE_P:
        raise ValueError(shape)
    p = SHAPE_P[shape]
    x = np.asarray(x, dtype=float)
    y = x * (1.0 - x)
    return y * (y * y + REG_DELTA ** 2) ** ((p - 1.0) / 2.0)


def j0_target() -> float:
    """신품 x_mid 의 실제 접촉 면적당 j₀ — R_ct,기하 = RT/(F·a·j₀·L) = RCT_GEO0."""
    return VT / (A_SURF0 * L_PE * RCT_GEO0)


def base_inputs(*, shape: str, Wa: float, x_mid: float) -> dict:
    """신품 (모든 배수 1) 의 InputParameter 사전. Wa = R_ct,기하 / (L/κ_eff) (§5-2 정의).
    k₀ 정규화는 모형이 실제로 쓰는 g_reg 로 (§8-4 S5′ · 1 차 g 정규화와의 차 ≤ 1e-5 상대)."""
    k0 = j0_target() / float(g_reg(shape, x_mid))
    kappa_eff = Wa * L_PE / RCT_GEO0
    kappa = kappa_eff / EPS_SE ** BRUGG_E
    return {"k0": k0, "c_dl": C_DL0, "D_s": D_S0, "eps_am": EPS_CAM0, "eps_se": EPS_SE,
            "sigma_s": SIGMA_S0, "kappa": kappa}


def knob_inputs(arm: str, f: float, *, base: dict, theta: float = 1.0, f_sigma: float = 1.0,
                lam_pe: float = 0.0, d_lam: float = 0.0) -> dict:
    """노브 → 매개 덮어쓰기 (T1). arm ∈ {A, K, AD, A0}. A0 = R5 끔 (c_dl 보상) — K 와 같은 사전."""
    if arm not in ("A", "K", "AD", "A0"):
        raise ValueError(f"unknown arm {arm!r}")
    if not (0.0 < f <= 1.0):
        raise ValueError(f"f must be in (0, 1]: {f}")
    if not (0.0 < theta <= 1.0) or not (0.0 <= lam_pe < 1.0) or d_lam not in (0.0, 1.0):
        raise ValueError("theta / lam_pe / d_lam out of range")
    d = dict(base)
    d["k0"] = base["k0"] * f
    if arm in ("A", "AD"):
        d["c_dl"] = base["c_dl"] * f
    if arm == "AD":
        d["D_s"] = base["D_s"] * f * f
    d["eps_am"] = theta * (1.0 - lam_pe) * EPS_CAM0           # 연결 · 살아 있는 부피만 모형 안에
    if lam_pe > 0.0 and d_lam == 1.0:
        d["c_dl"] = d["c_dl"] * (1.0 + lam_pe / (1.0 - lam_pe))  # 죽은 재료 표면이 이중층을 유지
    d["sigma_s"] = base["sigma_s"] * f_sigma
    d["eps_se"] = EPS_SE                                       # R3 — 어느 노브도 ε_SE 를 바꾸지 않는다
    return d


def porosity_of(d: dict) -> float:
    return d["eps_se"]


def ledger(*, theta: float, xbar_iso: float) -> dict:
    """모형 밖 고립 입자 장부 (R2): 부피 (1−θ)·ε_CAM·L·A · Li N_iso = 부피 × c_max × x̄(s_iso)."""
    v_iso = (1.0 - theta) * EPS_CAM0 * L_PE * AREA
    return {"V_iso": v_iso, "N_iso": v_iso * C_MAX * xbar_iso}


# --------------------------------------------------------------------------------------------
# OCP 역함수 · C-rate 기준
# --------------------------------------------------------------------------------------------
def ocp(x: float) -> float:
    return float(OCP_FUN(x))


def x_of_ocp(v: float, lo: float = 1e-9, hi: float = 1 - 1e-9) -> float:
    """U(x) = v 의 근 (U 는 (0,1) 에서 감소 — S6 에서 단조성을 확인)."""
    from scipy.optimize import brentq
    return float(brentq(lambda x: ocp(x) - v, lo, hi, xtol=1e-15, rtol=1e-15, maxiter=500))


def q_per_x() -> float:
    """연결 부피 전체 (θ = 1) 의 Δx = 1 당 전하 [C]."""
    return F * C_MAX * EPS_CAM0 * L_PE * AREA


def q_1c_ah() -> float:
    """C-rate 기준: OCV 창 [U⁻¹(4.3), U⁻¹(3.0)] 의 신품 용량 [A h] — 모든 실행에 고정 (절대 전류)."""
    return q_per_x() * (x_of_ocp(V_LOW) - x_of_ocp(V_HIGH)) / 3600.0


# --------------------------------------------------------------------------------------------
# PyBaMM 모형
# --------------------------------------------------------------------------------------------
INPUT_NAMES = ("k0", "c_dl", "D_s", "eps_am", "eps_se", "sigma_s", "kappa", "I", "c0", "V_lo", "V_hi")


STD_VAR_PTS = {"x_s": 80, "x_p": 80, "r_p": 80}   # 4 차 표준 (§8-9 ①) · 3 차 40 · 1 · 2 차 PyBaMM 기본 20
STD_TOL = 1e-9


def build_model(shape: str, *, var_pts=STD_VAR_PTS, rtol: float = STD_TOL, atol: float = STD_TOL, D_e: float = D_E,
                ce0: float = CE0, kappa_ce_exp: float = 0.0, output_variables=None):
    """g 모양 하나의 truth 모형을 만들어 (model, solver, sim) 를 돌려준다.
    kappa_ce_exp ≠ 0 은 시험의 음성 대조 전용 (κ ∝ (c_e/CE0)^n — truth 는 0)."""
    import pybamm
    pv = _chen()
    k0 = pybamm.InputParameter("k0")
    if shape == "G05":
        def gsym(x):
            return (x * (1 - x)) ** 0.5
    elif shape == "G2":
        def gsym(x):
            return (x * (1 - x)) ** 2
    else:
        raise ValueError(shape)

    def j0(c_e, c_s_surf, c_s_max, T):
        return k0 * gsym(c_s_surf / c_s_max)

    pv.update({
        "Exchange-current density for lithium metal electrode [A.m-2]": J0_LI,
        "Lithium metal partial molar volume [m3.mol-1]": 1.3e-05,
    }, check_already_exists=False)
    pv.update({
        "Negative electrode double-layer capacity [F.m-2]": CDL_LI,
        "Cation transference number": 1.0,
        "Thermodynamic factor": 1.0,
        "Electrolyte conductivity [S.m-1]": "[input]",
        "Electrolyte diffusivity [m2.s-1]": D_e,
        "Initial concentration in electrolyte [mol.m-3]": ce0,
        "Positive electrode double-layer capacity [F.m-2]": "[input]",
        "Positive electrode exchange-current density [A.m-2]": j0,
        "Positive electrode charge transfer coefficient": 0.5,
        "Positive particle diffusivity [m2.s-1]": "[input]",
        "Positive electrode active material volume fraction": "[input]",
        "Positive electrode porosity": "[input]",
        "Positive electrode conductivity [S.m-1]": "[input]",
        "Current function [A]": "[input]",
        "Initial concentration in positive electrode [mol.m-3]": "[input]",
        "Lower voltage cut-off [V]": "[input]",
        "Upper voltage cut-off [V]": "[input]",
        "Ambient temperature [K]": T_K,
        "Initial temperature [K]": T_K,
        "Reference temperature [K]": T_K,
    })
    if kappa_ce_exp != 0.0:
        def kappa_fun(c_e, T):
            return pybamm.InputParameter("Electrolyte conductivity [S.m-1]") * (c_e / CE0) ** kappa_ce_exp
        pv.update({"Electrolyte conductivity [S.m-1]": kappa_fun})
    _rename = {"kappa": "Electrolyte conductivity [S.m-1]", "c_dl": "Positive electrode double-layer capacity [F.m-2]",
               "D_s": "Positive particle diffusivity [m2.s-1]", "eps_am": "Positive electrode active material volume fraction",
               "eps_se": "Positive electrode porosity", "sigma_s": "Positive electrode conductivity [S.m-1]",
               "I": "Current function [A]", "c0": "Initial concentration in positive electrode [mol.m-3]",
               "V_lo": "Lower voltage cut-off [V]", "V_hi": "Upper voltage cut-off [V]"}
    model = pybamm.lithium_ion.DFN({"working electrode": "positive", "surface form": "differential"})
    if var_pts is not None:                       # 정밀판: 기본 사전에 덮어쓴다 (반쪽전지도 x_n 키를 요구 — 배관 점검 결함 수정)
        vp = dict(model.default_var_pts)
        vp.update(var_pts)
        var_pts = vp
    # output_variables: §8-11 ② (c) — B2 (DC) 의 촘촘 출력에서 전체 상태를 저장하지 않는다 (해의 끝 상태는 PyBaMM 이 따로 둔다)
    solver = pybamm.IDAKLUSolver(rtol=rtol, atol=atol, output_variables=list(output_variables) if output_variables else None)
    sim = pybamm.Simulation(model, parameter_values=pv, solver=solver, var_pts=var_pts)
    sim.build()
    sim._c1_rename = _rename
    return sim.built_model, sim.solver, sim


def to_pybamm_inputs(sim, d: dict) -> dict:
    out = {}
    for k, v in d.items():
        out[sim._c1_rename.get(k, k)] = float(v)
    return out


def grid_after_step(t_len: float, dense: float = 0.5, dt_dense: float = 1e-4, dt_coarse: float = 1e-2):
    """전류가 바뀐 뒤 0.5 s 까지 0.1 ms · 그 뒤 10 ms (§4-1 B3). 정수 배로 만들어 부동소수 끝 넘침을 막는다."""
    n_d = int(round(dense / dt_dense))
    n_c = int(round((t_len - dense) / dt_coarse))
    t = np.concatenate([np.arange(n_d) * dt_dense, dense + np.arange(n_c + 1) * dt_coarse])
    t = np.round(t, 10)
    t[-1] = t_len
    return t


PULSE_VARS = ("Voltage [V]", "Electrolyte concentration [mol.m-3]",
              "Positive electrode surface potential difference [V]",
              "R-averaged positive particle concentration [mol.m-3]")


def run_pulse(model, solver, sim, d_inputs: dict, *, x_start: float, I_A: float, t_on: float = 10.0,
              t_off: float = 60.0, keep=PULSE_VARS, no_cutoff: bool = True) -> dict:
    """균일 평형 x_start 에서 펄스 (t_on) → 휴지 (t_off). 펄스는 전압 컷오프 없이 (§8 에 고정)."""
    d = dict(d_inputs)
    d.update({"I": I_A, "c0": x_start * C_MAX,
              "V_lo": 0.0 if no_cutoff else V_LOW, "V_hi": 10.0 if no_cutoff else V_HIGH})
    inp = to_pybamm_inputs(sim, d)
    t1 = grid_after_step(t_on)
    s1 = solver.solve(model, t_eval=[0.0, t_on], t_interp=t1, inputs=inp)
    d2 = dict(d)
    d2["I"] = 0.0
    inp2 = to_pybamm_inputs(sim, d2)
    t2 = grid_after_step(t_off)
    s2 = solver.step(s1, model, dt=t_off, t_interp=t2, inputs=inp2)
    out = {"t": np.asarray(s2.t), "n_pulse": len(s1.t), "termination": [s1.termination, s2.termination]}
    for k in keep:
        out[k] = np.asarray(s2[k].entries)
    return out


def run_pulse_lean(model, solver, sim, d_inputs: dict, *, x_start: float, I_A: float, t_on: float = 10.0,
                   t_off: float = 60.0, no_cutoff: bool = True) -> dict:
    """§8-11 ② (a): run_pulse 와 같은 계산 — 펄스 해에서 V · 첫 열만 뽑고 버린 뒤, 마지막 상태에서 휴지를 step 으로 잇는다
    (step 은 어느 쪽이든 마지막 상태를 초기값으로 쓴다). 반환: V (펄스 + 휴지 · run_pulse 와 같은 배치) · Li 상대 오차 (이중층 항 포함)."""
    import gc
    d = dict(d_inputs)
    d.update({"I": I_A, "c0": x_start * C_MAX,
              "V_lo": 0.0 if no_cutoff else V_LOW, "V_hi": 10.0 if no_cutoff else V_HIGH})
    inp = to_pybamm_inputs(sim, d)
    s1 = solver.solve(model, t_eval=[0.0, t_on], t_interp=grid_after_step(t_on), inputs=inp)
    V1 = np.asarray(s1["Voltage [V]"].entries).copy()
    c_first = np.asarray(s1["R-averaged positive particle concentration [mol.m-3]"].entries)[:, 0].copy()
    p_first = np.asarray(s1["Positive electrode surface potential difference [V]"].entries)[:, 0].copy()
    term1 = s1.termination
    last = s1.last_state
    del s1
    gc.collect()
    d2 = dict(d)
    d2["I"] = 0.0
    s2 = solver.step(last, model, dt=t_off, t_interp=grid_after_step(t_off), inputs=to_pybamm_inputs(sim, d2))
    V2 = np.asarray(s2["Voltage [V]"].entries)[1:].copy()           # 첫 점 = 넘겨준 마지막 상태 (펄스 끝) — 옛 길과 같은 배치로
    c_last = np.asarray(s2["R-averaged positive particle concentration [mol.m-3]"].entries)[:, -1].copy()
    p_last = np.asarray(s2["Positive electrode surface potential difference [V]"].entries)[:, -1].copy()
    term2 = s2.termination
    del s2, last
    gc.collect()
    eps = d_inputs["eps_am"]
    a = 3.0 * eps / R_P
    n_x = c_first.size
    dx = L_PE / n_x
    dN = AREA * eps * dx * (c_last.sum() - c_first.sum())
    Qdl = AREA * a * d_inputs["c_dl"] * dx * (p_last - p_first).sum()
    q_in = I_A * t_on
    li = abs(F * dN - Qdl - q_in) / abs(q_in) if q_in != 0 else float("nan")
    return {"V": np.concatenate([V1, V2]), "n_pulse": int(V1.size), "li_rel_with_dl": float(li),
            "termination": [term1, term2]}


def li_balance(res: dict, d_inputs: dict, I_A: float, t_on: float) -> dict:
    """F·ΔN_Li,입자 + ΔQ_dl vs ∫I dt (펄스 + 휴지 끝 기준) — 상대 오차 (§3-2 S5)."""
    eps = d_inputs["eps_am"]
    a = 3.0 * eps / R_P
    cbar = res["R-averaged positive particle concentration [mol.m-3]"]   # (n_x, n_t) — 균일 격자
    dphi = res["Positive electrode surface potential difference [V]"]
    n_x = cbar.shape[0]
    dx = L_PE / n_x
    N = AREA * eps * dx * cbar.sum(axis=0)
    Qdl = AREA * a * d_inputs["c_dl"] * dx * (dphi - dphi[:, :1]).sum(axis=0)
    q_in = I_A * t_on
    lhs = F * (N[-1] - N[0]) - Qdl[-1]
    return {"rel_with_dl": abs(lhs - q_in) / abs(q_in), "rel_no_dl": abs(F * (N[-1] - N[0]) - q_in) / abs(q_in),
            "Qdl_end_C": float(Qdl[-1]), "q_in_C": q_in}


def li_balance_check(*, shape: str, Wa: float, x_mid: float, x0: float, I_A: float, t_pulse: float,
                     t_rest: float) -> dict:
    model, solver, sim = build_model(shape)
    b = base_inputs(shape=shape, Wa=Wa, x_mid=x_mid)
    res = run_pulse(model, solver, sim, b, x_start=x0, I_A=I_A, t_on=t_pulse, t_off=t_rest)
    return li_balance(res, b, I_A, t_pulse)


def run_cc(model, solver, sim, d_inputs: dict, *, x_start: float, I_A: float, t_max: float, dt_out: float = 10.0,
           V_lo: float = V_LOW, V_hi: float = V_HIGH, keep=("Voltage [V]",)) -> dict:
    """정전류 (I_A > 0 방전) — 컷오프 사건에서 끝난다. 출력 dt_out (§4-1 B0 · B2)."""
    d = dict(d_inputs)
    d.update({"I": I_A, "c0": x_start * C_MAX, "V_lo": V_lo, "V_hi": V_hi})
    inp = to_pybamm_inputs(sim, d)
    n = int(np.floor(t_max / dt_out))
    t_i = np.round(np.arange(n + 1) * dt_out, 6)
    t_i = t_i[t_i < t_max]
    s = solver.solve(model, t_eval=[0.0, t_max], t_interp=t_i, inputs=inp)
    out = {"t": np.asarray(s.t), "termination": s.termination, "sol": s}
    for k in keep:
        out[k] = np.asarray(s[k].entries)
    return out


def model_j0_at(*, shape: str, xs, x_mid: float, Wa: float = 10.0) -> np.ndarray:
    """균일 x · I = 0 의 t = 0 에서 모형이 계산한 양극 j₀ (x 격자 평균) — §8-4 S5′ 확인용."""
    model, solver, sim = build_model(shape)
    b = base_inputs(shape=shape, Wa=Wa, x_mid=x_mid)
    out = []
    for x in np.atleast_1d(xs):
        d = dict(b)
        d.update({"I": 0.0, "c0": float(x) * C_MAX, "V_lo": 0.0, "V_hi": 10.0})
        s = solver.solve(model, t_eval=[0.0, 1e-3], t_interp=np.array([0.0, 1e-3]),
                         inputs=to_pybamm_inputs(sim, d))
        j = np.asarray(s["Positive electrode exchange current density [A.m-2]"].entries)[:, 0]
        out.append(float(j.mean()))
    return np.array(out)


def common_max_abs_dv(t_a, v_a, t_b, v_b, *, ndig: int = 9) -> dict:
    """공통 출력 시각 (반올림 ndig 자리 일치) 에서만 max |V_a − V_b| (§8-4 S4′)."""
    ka = np.round(np.asarray(t_a, float), ndig)
    kb = np.round(np.asarray(t_b, float), ndig)
    common, ia, ib = np.intersect1d(ka, kb, return_indices=True)
    if common.size == 0:
        return {"max_abs_dv": float("nan"), "t_at_max": float("nan"), "n_common": 0}
    dv = np.abs(np.asarray(v_a, float)[ia] - np.asarray(v_b, float)[ib])
    i = int(np.argmax(dv))
    return {"max_abs_dv": float(dv[i]), "t_at_max": float(common[i]), "n_common": int(common.size)}


FEEDBACK_VARIANTS = (("D_e_x10", {"D_e": D_E * 10}), ("ce0_x2", {"ce0": CE0 * 2}))


def feedback_pulse(*, shape: str, Wa: float, x_mid: float, x0: float, I_A: float, kappa_ce_exp: float = 0.0,
                   t_on: float = 10.0, t_off: float = 60.0) -> dict:
    """S4′: 기준 · 진단 변형 (D_e × 10 · c_e0 × 2) 의 펄스 V 차 (공통 시각 max |ΔV|)."""
    b = base_inputs(shape=shape, Wa=Wa, x_mid=x_mid)
    m0, s0, sim0 = build_model(shape, kappa_ce_exp=kappa_ce_exp)
    r0 = run_pulse(m0, s0, sim0, b, x_start=x0, I_A=I_A, t_on=t_on, t_off=t_off, keep=("Voltage [V]",))
    per = {}
    for lab, kw in FEEDBACK_VARIANTS:
        m1, s1, sim1 = build_model(shape, kappa_ce_exp=kappa_ce_exp, **kw)
        r1 = run_pulse(m1, s1, sim1, b, x_start=x0, I_A=I_A, t_on=t_on, t_off=t_off, keep=("Voltage [V]",))
        per[lab] = common_max_abs_dv(r0["t"], r0["Voltage [V]"], r1["t"], r1["Voltage [V]"])
    return {"max_abs_dv": max(v["max_abs_dv"] for v in per.values()), "per_variant": per}


QF_KEEP = ("Voltage [V]", "X-averaged positive electrode surface potential difference [V]",
           "Average positive particle concentration [mol.m-3]")


def qf_and_li(res: dict, d_inputs: dict, I_A: float) -> dict:
    """§8-7 ②: Q_F(t) = I·t − Q_dl(t) (X-averaged Δφ̄ · 그 팔의 c_dl · a) · F·ΔN_Li (Average 입자 농도) · 상대 차 (규칙 4)."""
    from c1_observe import faradaic_charge
    t = np.asarray(res["t"], float)
    a = 3.0 * d_inputs["eps_am"] / R_P
    qf = faradaic_charge(t, I_A, res["X-averaged positive electrode surface potential difference [V]"], a=a,
                         c_dl=d_inputs["c_dl"], L=L_PE, area=AREA)
    cbar = np.asarray(res["Average positive particle concentration [mol.m-3]"], float)
    fdn = F * AREA * d_inputs["eps_am"] * L_PE * (cbar - cbar[0])
    q_cell = abs(I_A) * float(t[-1])
    return {"qf": qf, "rel": float(abs(fdn[-1] - qf[-1]) / q_cell) if q_cell > 0 else float("nan"),
            "Qdl_end_C": float(I_A * t[-1] - qf[-1])}


def qf_identity_check(*, shape: str, Wa: float, x_mid: float, x0: float, I_A: float, t_end: float) -> dict:
    model, solver, sim = build_model(shape)
    b = base_inputs(shape=shape, Wa=Wa, x_mid=x_mid)
    r = run_cc(model, solver, sim, b, x_start=x0, I_A=I_A, t_max=t_end, dt_out=1.0, V_lo=0.0, V_hi=10.0, keep=QF_KEEP)
    out = qf_and_li(r, b, I_A)
    return {"rel": out["rel"], "Qdl_end_C": out["Qdl_end_C"], "t_end": float(r["t"][-1])}


def seed_for(key: str, base: int = 101) -> int:
    """P3 규칙: seed = 기준값 + sha1(조건 키) 앞 6 자 (16 진)."""
    return base + int(hashlib.sha1(key.encode()).hexdigest()[:6], 16)


def timed(fn, *a, **k):
    t0 = time.time()
    r = fn(*a, **k)
    return r, time.time() - t0
