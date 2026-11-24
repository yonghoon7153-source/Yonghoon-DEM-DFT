"""C1 시험 T1–T6 — 설계서 `followups/assb-contact-truth/DESIGN_v1.md` §5-7 (RED → GREEN). 진단 전용.

환경변수:
  C1_COPY   저장소 밖 버리는 사본의 degradation-degeneracy 경로 (읽기 재사용만 — `src/curves.py:add_noise`)
실행: <venv>/bin/python -I -m pytest -q -p no:cacheprovider test_c1.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
COPY = Path(os.environ["C1_COPY"]).resolve()
sys.path.insert(0, str(COPY))
sys.path.insert(0, str(HERE))

import c1_observe as ob  # noqa: E402
import c1_truth as tr  # noqa: E402

F_GRID = [2.0 ** (-k / 4) for k in range(9)]


# --------------------------------------------------------------------------------------------
# T1 — 노브 → 매개 덮어쓰기 (§2-2 · §2-3 · §2-4 · §2-5 · R3)
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def base():
    return tr.base_inputs(shape="G05", Wa=10.0, x_mid=0.6)


def test_t1_area_arm_scales_k0_and_cdl_only(base):
    for f in F_GRID:
        a = tr.knob_inputs("A", f, base=base)
        assert a["k0"] == pytest.approx(base["k0"] * f, rel=1e-15)
        assert a["c_dl"] == pytest.approx(base["c_dl"] * f, rel=1e-15)
        for key in ("D_s", "eps_am", "sigma_s", "kappa"):
            assert a[key] == base[key]


def test_t1_j0_arm_scales_k0_only(base):
    for f in F_GRID:
        k = tr.knob_inputs("K", f, base=base)
        assert k["k0"] == pytest.approx(base["k0"] * f, rel=1e-15)
        for key in ("c_dl", "D_s", "eps_am", "sigma_s", "kappa"):
            assert k[key] == base[key]


def test_t1_ad_proxy_scales_k0_cdl_and_D_by_f_squared(base):
    for f in F_GRID:
        d = tr.knob_inputs("AD", f, base=base)
        assert d["k0"] == pytest.approx(base["k0"] * f, rel=1e-15)
        assert d["c_dl"] == pytest.approx(base["c_dl"] * f, rel=1e-15)
        assert d["D_s"] == pytest.approx(base["D_s"] * f * f, rel=1e-15)


def test_t1_negative_control_A0_equals_K(base):
    """R5 를 끈 면적 팔 A0 (c_dl 보상) 의 매개 사전은 K 와 같다 (§5-2 둘째 점)."""
    for f in F_GRID:
        assert tr.knob_inputs("A0", f, base=base) == tr.knob_inputs("K", f, base=base)


def test_t1_dc_product_identical_between_A_and_K(base):
    """DC 곱 a·j₀ (a = 3 ε/R 는 노브가 바꾸지 않음 · k₀ 만) 이 같은 f 에서 같다 (§2-3 등가)."""
    for f in F_GRID:
        a = tr.knob_inputs("A", f, base=base)
        k = tr.knob_inputs("K", f, base=base)
        assert a["eps_am"] * a["k0"] == k["eps_am"] * k["k0"]
        assert a["c_dl"] == pytest.approx(f * k["c_dl"], rel=1e-15)   # 두 팔의 차는 이중층 하나


def test_t1_theta_reduces_connected_volume_and_keeps_se_fraction(base):
    for theta in (1.0, 0.96, 0.5):
        d = tr.knob_inputs("K", 1.0, base=base, theta=theta)
        assert d["eps_am"] == pytest.approx(theta * tr.EPS_CAM0, rel=1e-15)
        assert tr.porosity_of(d) == tr.EPS_SE                     # R3 — ε_SE 불변


def test_t1_lam_pe_with_d_lam(base):
    """LAM_PE: ε_CAM = θ·(1−LAM)·ε0 · 죽은 부피 → 불활성 (공극 아님) · d_LAM=1 이면 이중층 면적이 죽은 재료까지."""
    lam = 0.2
    d0 = tr.knob_inputs("K", 1.0, base=base, lam_pe=lam, d_lam=0.0)
    d1 = tr.knob_inputs("K", 1.0, base=base, lam_pe=lam, d_lam=1.0)
    assert d0["eps_am"] == pytest.approx((1 - lam) * tr.EPS_CAM0, rel=1e-15)
    assert d1["eps_am"] == d0["eps_am"]
    assert d0["c_dl"] == base["c_dl"]
    # 모형 안 이중층 = a·c_dl ∝ ε_am·c_dl — d_LAM = 1 이면 신품과 같은 총 이중층
    assert d1["eps_am"] * d1["c_dl"] == pytest.approx(tr.EPS_CAM0 * base["c_dl"], rel=1e-14)
    for d in (d0, d1):
        assert tr.porosity_of(d) == tr.EPS_SE                     # R3


def test_t1_se_fraction_invariant_for_every_knob(base):
    for arm in ("A", "K", "AD", "A0"):
        for f in (1.0, 0.5, 0.25):
            for theta in (1.0, 0.96):
                for fs in (1.0, 0.1):
                    d = tr.knob_inputs(arm, f, base=base, theta=theta, f_sigma=fs)
                    assert tr.porosity_of(d) == tr.EPS_SE
                    assert d["kappa"] == base["kappa"]            # κ 는 Wa 로만 정해진다
                    assert d["sigma_s"] == pytest.approx(base["sigma_s"] * fs, rel=1e-15)


def test_t1_unknown_arm_rejected(base):
    with pytest.raises(ValueError):
        tr.knob_inputs("Z", 0.5, base=base)
    with pytest.raises(ValueError):
        tr.knob_inputs("A", 1.5, base=base)          # f ∈ (0, 1]


def test_t1_j0_shape_normalised_at_x_mid():
    """두 g 가 x_mid 에서 같은 j₀ → 같은 신품 R_ct,기하 = 66 Ω cm² (§1-4 · §2-6).
    2 차 (§8-4 S5′ · 사후): 기준 함수 = PyBaMM 26.8 이 실제로 쓰는 정칙화된 g (g_reg) — k₀ 정규화도 g_reg 로."""
    for x_mid in (0.45, 0.6, 0.7):
        j = []
        for shape in ("G05", "G2"):
            b = tr.base_inputs(shape=shape, Wa=10.0, x_mid=x_mid)
            j.append(b["k0"] * tr.g_reg(shape, x_mid))
            rct = tr.VT / (tr.A_SURF0 * b["k0"] * tr.g_reg(shape, x_mid) * tr.L_PE)
            assert rct == pytest.approx(tr.RCT_GEO0, rel=1e-12)
        assert j[0] == pytest.approx(j[1], rel=1e-14)
    x = np.array([0.3, 0.5, 0.8])
    assert np.allclose(tr.g_shape("G05", x), np.sqrt(x * (1 - x)), rtol=0, atol=0)
    assert np.allclose(tr.g_shape("G2", x), (x * (1 - x)) ** 2, rtol=0, atol=0)


def test_t1_wa_definition_inverts_to_kappa():
    for Wa in (10.0, 0.1):
        b = tr.base_inputs(shape="G05", Wa=Wa, x_mid=0.6)
        k_eff = b["kappa"] * tr.EPS_SE ** tr.BRUGG_E
        wa_back = tr.RCT_GEO0 / (tr.L_PE / k_eff)
        assert wa_back == pytest.approx(Wa, rel=1e-12)


# --------------------------------------------------------------------------------------------
# T2 — F1 펄스 맞춤기 (§4-2)
# --------------------------------------------------------------------------------------------
def _f1_wave(t, I, V0, R0, Rp, tau, k):
    return V0 - I * (R0 + Rp * (1 - np.exp(-t / tau)) + k * np.sqrt(t))


def test_t2_f1_noise_free_recovers_parameters():
    rng = np.random.default_rng(7)
    for _ in range(6):
        R0, Rp, tau, k = rng.uniform(0.01, 0.1), rng.uniform(0.02, 0.2), rng.uniform(0.005, 0.3), rng.uniform(0.002, 0.05)
        I = rng.choice([-1.0, 1.0]) * rng.uniform(0.05, 2.0)
        dt = 1e-4
        W = min(max(0.5, 10 * tau), 10.0)
        t = np.arange(1, int(round(W / dt)) + 1) * dt
        V0 = 3.8
        v = _f1_wave(t, I, V0, R0, Rp, tau, k)
        r = ob.fit_f1(t, v, I=I, V0=V0, dt=dt)
        for name, val in (("R0", R0), ("Rp", Rp), ("tau", tau), ("k", k)):
            assert r[name] == pytest.approx(val, rel=1e-6), name
        assert r["C"] == pytest.approx(tau / Rp, rel=1e-6)
        assert r["Rp_over_k"] == pytest.approx(Rp / k, rel=1e-6)


def test_t2_f1_unresolved_tau_is_nan():
    """τ̂ < 2Δt → τ 미해상 (NaN) — 표본이 RC 를 못 본다."""
    dt = 0.1
    t = np.arange(1, 21) * dt
    v = _f1_wave(t, 1.0, 3.8, 0.05, 0.05, 0.01, 0.01)   # τ = 10 ms ≪ 2Δt
    r = ob.fit_f1(t, v, I=1.0, V0=3.8, dt=dt)
    assert np.isnan(r["tau"])


def test_t2_f1_too_few_samples_is_nan():
    t = np.array([1.0, 2.0, 3.0])
    v = _f1_wave(t, 1.0, 3.8, 0.05, 0.05, 0.5, 0.01)
    r = ob.fit_f1(t, v, I=1.0, V0=3.8, dt=1.0)
    assert np.isnan(r["tau"]) and np.isnan(r["Rp"])


def test_t2_f1_noise_95ci_covers_truth():
    """잡음 σ → 95 % 구간의 경험 포함률이 [0.88, 0.99] (M = 200)."""
    R0, Rp, tau, k, I, V0 = 0.03, 0.06, 0.05, 0.01, 1.0, 3.8
    dt = 1e-3
    t = np.arange(1, 501) * dt
    v = _f1_wave(t, I, V0, R0, Rp, tau, k)
    sig = 2e-4
    cover = {"tau": 0, "Rp": 0}
    M = 200
    for m in range(M):
        vn = v + np.random.default_rng(1000 + m).normal(0, sig, size=v.shape)
        r = ob.fit_f1(t, vn, I=I, V0=V0, dt=dt)
        for name, val in (("tau", tau), ("Rp", Rp)):
            if abs(r[name] - val) <= 1.96 * r["se_" + name]:
                cover[name] += 1
    for name in cover:
        assert 0.88 <= cover[name] / M <= 0.99, (name, cover[name])


# --------------------------------------------------------------------------------------------
# T3 — 정합 필터 z (§4-2)
# --------------------------------------------------------------------------------------------
def test_t3_two_rc_waveforms_closed_form():
    """프로파일 없음 (후보 하나) · ΔR0 없음: z = I·R·√S/σ, S = Σ (q_A^n − q_K^n)² (기하급수 닫힌 꼴)."""
    I, R, tA, tK, dt, N, sig = 1.5, 0.04, 0.02, 0.05, 1e-3, 3000, 1e-3
    n = np.arange(1, N + 1)
    t = n * dt
    vA = -I * R * (1 - np.exp(-t / tA))
    vK = -I * R * (1 - np.exp(-t / tK))
    qA, qK = np.exp(-dt / tA), np.exp(-dt / tK)

    def geo(q):
        return q * (1 - q ** N) / (1 - q)

    S = geo(qA * qA) - 2 * geo(qA * qK) + geo(qK * qK)
    z_closed = I * R * np.sqrt(S) / sig
    z = ob.z_profile(vA, np.array([vK]), np.array([0.0]), i_t=np.full(N, I), sigma=sig, dR0="none")
    assert z == pytest.approx(z_closed, rel=1e-10)


def test_t3_profile_over_log_f_quadratic_is_exact():
    """가족 V(s) = s²·w (s = log f) — 세 점 이차 보간이 정확 · 최소 잔차 = ‖u‖ (u ⟂ w, u ⟂ I)."""
    N = 400
    t = np.arange(1, N + 1) * 1e-2
    w = np.sin(2 * np.pi * t / t[-1])
    i_t = np.where(t <= 1.0, 1.0, 0.0)
    w = w - i_t * (w @ i_t) / (i_t @ i_t)
    u = np.cos(6 * np.pi * t / t[-1])
    for b in (w, i_t):
        u = u - b * (u @ b) / (b @ b)
    logf = np.log(np.array(F_GRID))
    fam = np.array([s * s * w for s in logf])
    c = (0.5 * (logf[3] + logf[4])) ** 2             # 격자 사이의 참값 → 보간이 필요
    r0 = 0.37
    target = c * w + u + i_t * r0
    sig = 1e-3
    z_free = ob.z_profile(target, fam, logf, i_t=i_t, sigma=sig, dR0="free")
    z_none = ob.z_profile(target, fam, logf, i_t=i_t, sigma=sig, dR0="none")
    assert z_free == pytest.approx(np.linalg.norm(u) / sig, rel=1e-6)
    assert z_none == pytest.approx(np.sqrt(u @ u + r0 * r0 * (i_t @ i_t)) / sig, rel=1e-6)


def test_t3_symmetric_takes_the_smaller():
    N = 200
    t = np.arange(1, N + 1) * 1e-2
    logf = np.log(np.array(F_GRID))
    famA = np.array([np.exp(s) * np.exp(-t) for s in logf])
    famK = np.array([np.exp(s) * np.exp(-t / 2) for s in logf])
    i_t = np.ones(N)
    zs = ob.z_cell(famA, famK, logf, idx=4, i_t=i_t, sigma=1e-3, dR0="none")
    zAK = ob.z_profile(famA[4], famK, logf, i_t=i_t, sigma=1e-3, dR0="none")
    zKA = ob.z_profile(famK[4], famA, logf, i_t=i_t, sigma=1e-3, dR0="none")
    assert zs == pytest.approx(min(zAK, zKA), rel=1e-12)


# --------------------------------------------------------------------------------------------
# T4 — GITT 비 연산자 (§4-2)
# --------------------------------------------------------------------------------------------
def test_t4_gitt_ratio_on_analytic_sqrt_wave():
    E0, IR0, b, tp, delta, tau_r = 3.75, 0.004, 3e-4, 600.0, 0.012, 120.0
    tp_s = np.arange(0, int(tp) + 1, 1.0)                  # 펄스 0..600 s (1 s)
    v_p = E0 - IR0 - b * np.sqrt(tp_s)
    v_p[0] = E0 - IR0
    tr_s = np.arange(1, 3601, 1.0)                         # 휴지 1 h
    E1 = E0 - delta
    v_end = v_p[-1]
    v_r = E1 + (v_end + IR0 - E1) * np.exp(-tr_s / tau_r)
    r = ob.gitt_ratio(t_pulse=tp_s, v_pulse=v_p, t_rest=tr_s, v_rest=v_r, v_pre=E0)
    dEt = -b * (np.sqrt(tp) - 1.0)
    dEs = v_r[-1] - E0
    assert r["dE_t"] == pytest.approx(dEt, rel=1e-12)
    assert r["dE_s"] == pytest.approx(dEs, rel=1e-12)
    assert r["ratio"] == pytest.approx(dEs / dEt, rel=1e-12)
    # 10 min 시점 (R6 기록)
    assert r["dE_s_10min"] == pytest.approx(v_r[599] - E0, rel=1e-12)
    # 변형 ÷ 기준
    assert ob.coverage_ratio(r, r) == pytest.approx(1.0, rel=1e-15)


# --------------------------------------------------------------------------------------------
# T5 — 첫 충전 상한 · 참 θ 몫 · C1b 관측 (§4-2 · §5-3)
# --------------------------------------------------------------------------------------------
def test_t5_first_charge_bound_matches_65_digest_arithmetic():
    Qch_ref, Qdis_ref = 100.0, 80.0
    Qch_var, Qdis_var = Qch_ref * (1 - 0.042), Qdis_ref * (1 - 0.197)
    ub = ob.first_charge_bound(Qch_ref=Qch_ref, Qch_var=Qch_var, Qdis_ref=Qdis_ref, Qdis_var=Qdis_var)
    assert ub == pytest.approx(0.042 / 0.197, rel=1e-12)           # ≈ 21.3 %


def test_t5_true_theta_share():
    Qdis_ref, Qdis_p_th1, Qdis_p_th096 = 80.0, 70.0, 67.0
    s = ob.true_theta_share(Qdis_theta1=Qdis_p_th1, Qdis_theta=Qdis_p_th096, Qdis_ref=Qdis_ref)
    assert s == pytest.approx(3.0 / 13.0, rel=1e-12)


def test_t5_c1b_observables_and_bands():
    ref = dict(Rp=0.010, gitt_ratio=0.5, Qdis=80.0, Qch=100.0)
    var = dict(Rp=0.0426, gitt_ratio=0.5 * 0.909, Qdis=80.0 * (1 - 0.197), Qch=100.0 * (1 - 0.042))
    o = ob.c1b_observables(ref, var)
    assert o["O1"] == pytest.approx(4.26, rel=1e-12)
    assert o["O2"] == pytest.approx(0.909, rel=1e-12)
    assert o["O3"] == pytest.approx(-0.197, rel=1e-12)
    assert o["O4"] == pytest.approx(-0.042, rel=1e-12)
    assert ob.in_bands(o) is True
    o_bad = dict(o, O2=1.0)
    assert ob.in_bands(o_bad) is False


# --------------------------------------------------------------------------------------------
# T6 — 장부 Li 보존 (§2-2 R2)
# --------------------------------------------------------------------------------------------
def test_t6_ledger_conserves_total_lithium():
    A, L, cmax = tr.AREA, tr.L_PE, tr.C_MAX
    for x_iso in (0.9998, 0.6):
        n_total = tr.EPS_CAM0 * L * A * cmax * x_iso
        for theta in (1.0, 0.96, 0.7):
            led = tr.ledger(theta=theta, xbar_iso=x_iso)
            n_model = theta * tr.EPS_CAM0 * L * A * cmax * x_iso
            assert led["N_iso"] + n_model == pytest.approx(n_total, rel=1e-14)
            assert led["V_iso"] == pytest.approx((1 - theta) * tr.EPS_CAM0 * L * A, rel=1e-14)
    assert tr.ledger(theta=1.0, xbar_iso=0.5)["N_iso"] == 0.0


def test_t6_model_lithium_balance_short_pulse():
    """모형 안 Li 보존 (§3-2 S5): F·ΔN_Li,입자 + ΔQ_dl = ∫ I dt — 상대 ≤ 1e-6."""
    rel = tr.li_balance_check(shape="G05", Wa=10.0, x_mid=0.6, x0=0.6, I_A=0.5, t_pulse=10.0, t_rest=20.0)
    assert rel["rel_with_dl"] <= 1e-6


# --------------------------------------------------------------------------------------------
# 2 차 (§8-4 · 결과를 본 뒤의 사후 규칙 변경) — S4′ (c_e 되먹임) · S5′ (정칙화 g)
# --------------------------------------------------------------------------------------------
def test_s5p_g_reg_matches_pybamm_regpower():
    """g_reg = PyBaMM RegPower(y = x(1−x), p) — y·(y² + δ²)^((p−1)/2) · 척도 1 · δ = settings reg_power."""
    import pybamm
    assert tr.REG_DELTA == pybamm.settings.tolerances["reg_power"]
    for shape, p in (("G05", 0.5), ("G2", 2.0)):
        for x in (1e-4, 0.0123, 0.261417, 0.5, 0.625854, 0.844516, 0.99, 0.999795):
            y = x * (1 - x)
            ref = float(pybamm.RegPower(pybamm.Scalar(y), p).evaluate())
            assert float(tr.g_reg(shape, x)) == pytest.approx(ref, rel=1e-14)
    # 정칙화는 x_mid 근처에서 작고 창 끝에서 커진다 (진단 — 크기만)
    assert abs(tr.g_reg("G05", 0.6) / tr.g_shape("G05", 0.6) - 1) < 1e-4
    assert abs(tr.g_reg("G2", 0.999795) / tr.g_shape("G2", 0.999795) - 1) > 1.0


def test_s5p_model_j0_equals_k0_g_reg_and_not_plain_g():
    """모형 j₀ (t = 0 · I = 0 · 균일 x) = k₀·g_reg (상대 ≤ 1e-12) · 음성 대조: k₀·g 와는 > 1e-7 다르다."""
    xs = np.array([0.30, 0.407192, 0.625854, 0.844516, 0.95])
    for shape in ("G05", "G2"):
        r = tr.model_j0_at(shape=shape, xs=xs, x_mid=0.625854)
        k0 = tr.base_inputs(shape=shape, Wa=10.0, x_mid=0.625854)["k0"]
        rel_reg = np.max(np.abs(r / (k0 * tr.g_reg(shape, xs)) - 1))
        rel_plain = np.max(np.abs(r / (k0 * tr.g_shape(shape, xs)) - 1))
        assert rel_reg <= 1e-12, (shape, rel_reg)
        assert rel_plain > 1e-7, (shape, rel_plain)


def test_s4p_common_max_abs_dv():
    """공통 출력 시각에서만 max |ΔV| — 끝 시각이 달라도 (사건 종료) 공통 구간만 본다."""
    t = np.arange(0, 100, 10.0)
    va = np.sin(t / 30.0)
    vb = va.copy()
    vb[3] += 2e-6
    tb = t.copy()
    out = tr.common_max_abs_dv(t, va, tb[:-2], vb[:-2])
    assert out["max_abs_dv"] == pytest.approx(2e-6, rel=1e-9)
    assert out["t_at_max"] == pytest.approx(30.0)
    assert out["n_common"] == 8
    out2 = tr.common_max_abs_dv(t, va, t + 5.0, va)     # 공통 시각 없음
    assert out2["n_common"] == 0 and np.isnan(out2["max_abs_dv"])


def test_s4p_feedback_pulse_below_threshold_and_negative_control():
    """S4′: t₊ = 1 truth 에서 D_e × 10 · c_e0 × 2 변형의 펄스 V 차 ≤ 1e-6 V.
    음성 대조: κ 를 c_e 에 의존시키면 (κ ∝ c_e) 같은 진단이 문턱을 넘는다 — 진단이 되먹임을 잡을 수 있다."""
    ok = tr.feedback_pulse(shape="G05", Wa=0.1, x_mid=0.625854, x0=0.625854, I_A=2.0)
    assert ok["max_abs_dv"] <= 1e-6, ok
    bad = tr.feedback_pulse(shape="G05", Wa=0.1, x_mid=0.625854, x0=0.625854, I_A=2.0, kappa_ce_exp=1.0)
    assert bad["max_abs_dv"] > 1e-6, bad


# --------------------------------------------------------------------------------------------
# 3 차 (§8-7 ② · 사전 등록) — DC 영 채널 보정: Faradaic 전하 축 Q_F(t) = I·t − Q_dl(t)
# --------------------------------------------------------------------------------------------
def test_dc_qf_faradaic_charge_definition():
    """Q_dl = area·a·c_dl·L·(Δφ̄(0) − Δφ̄(t)) (이중층이 내놓은 전하 · 방전에서 양) · Q_F = I·t − Q_dl."""
    t = np.array([0.0, 10.0, 20.0, 30.0])
    dphi = np.array([4.2, 4.1, 4.0, 3.9])
    qf = ob.faradaic_charge(t, 2.0, dphi, a=1000.0, c_dl=0.1, L=1e-4, area=0.5)
    assert np.allclose(qf, 2.0 * t - 5e-3 * np.array([0.0, 0.1, 0.2, 0.3]), rtol=0, atol=1e-15)


def test_dc_qf_common_grid_and_monotonic_guard():
    q1 = np.linspace(0, 100.0, 1001)
    q2 = np.linspace(0, 87.0, 871)
    g = ob.qf_common_grid([q1, q2], dq=10.0)
    assert np.allclose(g, 10.0 * np.arange(1, 8))          # ⌊87/10⌋ − 1 = 7 (한 칸 띄움 · 외삽 없음)
    v = ob.resample_on_qf(q1, np.sin(q1 / 30), g)
    assert np.allclose(v, np.interp(g, q1, np.sin(q1 / 30)), rtol=0, atol=0)
    bad = q1.copy()
    bad[500] = bad[499]
    with pytest.raises(ValueError):
        ob.resample_on_qf(bad, np.sin(q1 / 30), g)


def _dc_family(c_dl_charge, extra=None):
    """합성 DC 묶음: 같은 V(Q_F) 꼴 (동역학 몫 0.01/f 상수) · 팔마다 이중층 전하만 다름 (A: c0·f · K: c0)."""
    I, T = 1.0, 3000.0
    t = np.round(np.arange(0, int(T * 10) + 1) * 0.1, 6)     # 0.1 s — 보간 오차가 문턱 (1e-3) 의 1/10 아래가 되게 (RED 뒤 · 구현 전에 정함)
    out_t, out_q = {}, {}
    for arm in ("A", "K"):
        for lv, f in ((0, 1.0), (4, 0.5), (8, 0.25)):
            c = c_dl_charge * (f if arm == "A" else 1.0)
            qf = I * t - c * (1 - np.exp(-t / 50.0))
            V = 4.2 - 1.0 * qf / T - 0.5 * (qf / T) ** 12 - (0.01 / f) * (1 + qf / T)
            if extra is not None and (arm, lv) == ("K", 8):
                # 실제 차 = 국소 봉우리 — ΔR0 (상수) · f′ 프로파일이 흡수할 수 없는 꼴 (GREEN 1 회째: 기울기는 상수 동역학 몫과 겹쳐 흡수됐다)
                V = V + extra * np.exp(-(((qf / T) - 0.5) / 0.05) ** 2)
            key = ("fresh", 0) if lv == 0 else (arm, lv)
            out_t[key] = (t, V)
            out_q[key] = (qf, V)
    return out_t, out_q, I


def test_dc_qf_axis_removes_pure_dl_shift_but_keeps_real_difference():
    """이중층 전하만 다른 두 팔: 시간 축 z ≥ 2 (가짜 차) · Q_F 축 z ≈ 0. 음성 대조: K(0.25) 에 실제 차 (기울기 2 mV) → Q_F 축 z ≥ 2."""
    gt, gq, I = _dc_family(c_dl_charge=3.0)
    zt = ob.dc_z_time(gt, I=I, dt_grid=10.0, sigma=1e-3)
    zq = ob.dc_z_qf(gq, I=I, dt_equiv=10.0, sigma=1e-3)
    assert max(r["z"] for r in zt) >= 2.0
    assert max(r["z"] for r in zq) <= 1e-3
    gt2, gq2, _ = _dc_family(c_dl_charge=3.0, extra=2e-3)
    zq2 = ob.dc_z_qf(gq2, I=I, dt_equiv=10.0, sigma=1e-3)
    for dr in ("none", "free"):
        assert max(r["z"] for r in zq2 if r["dR0"] == dr) >= 2.0, dr


def test_dc_qf_identity_with_model_lithium():
    """모형 수준: Q_F (X-averaged Δφ 로) = F·ΔN_Li (Average positive particle concentration 로) — 상대 ≤ 1e-6 (같은 실행)."""
    r = tr.qf_identity_check(shape="G05", Wa=10.0, x_mid=0.625854, x0=0.625854, I_A=2.0, t_end=600.0)
    assert r["rel"] <= 1e-6, r
    assert r["Qdl_end_C"] > 0.0                           # 방전: 이중층이 전하를 내놓는다


# --------------------------------------------------------------------------------------------
# 5 차 (§8-11 · 사전 등록) — 메모리 경로 (수는 바뀌지 않아야 한다) · 점진 기록 · 메모리 경비
# --------------------------------------------------------------------------------------------
def test_mem_tree_rss_and_kill_targets_fake():
    """가짜 /proc 표: {pid: (ppid, rss_B)} — 뿌리 10 의 자손 합 (감시자 99 제외) · 죽일 대상 = 자손 − 뿌리 − 감시자."""
    import c1_memguard as mg
    table = {1: (0, 5), 10: (1, 100), 11: (10, 200), 12: (10, 300), 13: (12, 400), 99: (10, 50), 20: (1, 7000)}
    assert mg.tree_rss(10, table, exclude=(99,)) == 100 + 200 + 300 + 400
    assert sorted(mg.kill_targets(10, table, exclude=(99,))) == [11, 12, 13]


def test_mem_watcher_trips_on_first_exceed_and_tracks_peak():
    import c1_memguard as mg
    w = mg.Watcher(cap_bytes=12_000)
    trips = [w.observe(x) for x in (1_000, 5_000, 11_999, 12_001, 3_000)]
    assert trips == [False, False, False, True, False]
    assert w.peak == 12_001 and w.tripped and w.trip_value == 12_001


def test_inc_jsonl_roundtrip_and_truncated_tail(tmp_path):
    import c1_grid as cg
    p = tmp_path / "x.jsonl"
    for i in range(3):
        cg.append_jsonl(p, {"i": i, "v": 0.5 * i})
    with open(p, "a") as fh:
        fh.write('{"i": 3, "v": ')                       # 충돌로 잘린 마지막 줄
    rows = cg.read_jsonl(p)
    assert [r["i"] for r in rows] == [0, 1, 2]


LOWRES = {"var_pts": {"x_s": 20, "x_p": 20, "r_p": 20}, "rtol": 1e-8, "atol": 1e-8}


def test_lean_pulse_matches_old_full_state_path_low_res():
    """(a) 가벼운 길 = 옛 길 (펄스 + 휴지 이어 붙인 전체 상태): max |ΔV| ≤ 1e-12 V · Li 상대값 차 ≤ 1e-12 (20 · 1e-8)."""
    m, s, sim = tr.build_model("G05", **LOWRES)
    d = tr.base_inputs(shape="G05", Wa=0.1, x_mid=0.625847)
    for x, I in ((0.844504, 1.9989605), (0.407188, -1.9989605)):
        old = tr.run_pulse(m, s, sim, d, x_start=x, I_A=I, keep=("Voltage [V]",
                           "R-averaged positive particle concentration [mol.m-3]",
                           "Positive electrode surface potential difference [V]"))
        li_old = tr.li_balance(old, d, I, 10.0)["rel_with_dl"]
        new = tr.run_pulse_lean(m, s, sim, d, x_start=x, I_A=I)
        assert new["V"].shape == old["Voltage [V]"].shape
        assert np.max(np.abs(new["V"] - old["Voltage [V]"])) <= 1e-12
        assert abs(new["li_rel_with_dl"] - li_old) <= 1e-12
        assert new["n_pulse"] == old["n_pulse"]


def test_restricted_output_cc_matches_full_low_res():
    """(c) 제한 출력 (V · Δφ̄ · c̄) ↔ 전체 상태: 공통 시각 max |ΔV| ≤ 1e-10 V · |ΔQ_F 끝| ≤ 1e-10·I·t · |Δt_끝| ≤ 1e-6 s (20 · 1e-8)."""
    mf, sf, simf = tr.build_model("G05", **LOWRES)
    mr, sr, simr = tr.build_model("G05", output_variables=list(tr.QF_KEEP), **LOWRES)
    d = tr.base_inputs(shape="G05", Wa=10.0, x_mid=0.625847)
    I = 6.4477514 / 3.0
    rf = tr.run_cc(mf, sf, simf, d, x_start=0.261417, I_A=I, t_max=2000.0, dt_out=0.1, V_lo=3.0, V_hi=10.0, keep=tr.QF_KEEP)
    rr = tr.run_cc(mr, sr, simr, d, x_start=0.261417, I_A=I, t_max=2000.0, dt_out=0.1, V_lo=3.0, V_hi=10.0, keep=tr.QF_KEEP)
    c = tr.common_max_abs_dv(rf["t"], rf["Voltage [V]"], rr["t"], rr["Voltage [V]"])
    assert c["n_common"] > 10000 and c["max_abs_dv"] <= 1e-10
    qf_f = tr.qf_and_li(rf, d, I)
    qf_r = tr.qf_and_li(rr, d, I)
    assert abs(float(rf["t"][-1]) - float(rr["t"][-1])) <= 1e-6
    assert abs(qf_f["qf"][-1] - qf_r["qf"][-1]) <= 1e-10 * I * float(rf["t"][-1])
    assert qf_r["rel"] <= 1e-6
