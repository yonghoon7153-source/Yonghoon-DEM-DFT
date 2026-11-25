#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""분말 XRD 지문표 — 어느 상이 어느 2θ 에 나오고, 어느 창에서 갈라지는가.

용도 (2026-09-03, Zn ALZIB 협업 C1):
    Cu 집전체 위 pre-conditioning 층의 43° 부근 반사를 상에 귀속시키지 못하는 문제
    (`kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md` G1) 에 답하기 위한 도구.
    후보 상들의 피크 위치·상대강도를 계산하고, **겹치는 구간과 갈라지는 창**을 뽑는다.

계산 내용:
    · 일반 삼사정계 역격자 계량텐서로 d(hkl)  → 모든 결정계 지원
    · Cromer-Mann 4-Gaussian 원자산란인자 f(s), s = sinθ/λ = 1/(2d)
    · F(hkl) = Σ_j occ_j f_j(s) exp(2πi(hx+ky+lz)) · exp(-B_j s²)
    · 다중도는 **hkl 전수 나열 후 d 로 묶어** 자동 처리 (우연중첩도 물리적으로 올바르게 병합)
    · I ∝ Σ_group |F|² · LP(θ),  LP = (1+cos²2θ)/(sin²θ cosθ)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 이 도구가 **못 하는 것** (읽지 않고 쓰면 반드시 틀린다)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **정량상분석(Rietveld) 이 아니다.** 상대강도는 이상적 무작위 배향 분말 가정이다.
   전착 Zn 은 (002) 강한 texture 를 보이므로 **실측 강도비와 안 맞는 게 정상**이다.
   피크 **위치**는 쓰고, 강도는 "이 반사가 원래 센 편/약한 편" 정도로만 써라.
2. **격자상수를 스스로 못 구한다.** 입력한 a,b,c 를 그대로 쓴다. 기본값은 실험 문헌값이고
   DFT 이완값이 아니다 — 피크 위치 목적에는 실험값이 **더 정확하다**(DFT 격자상수 ~1 % 오차
   = 2θ 0.3–0.4 °, Cu(111)–Zn(101) 간격 0.1 ° 보다 크다).
3. **어느 상이 실제로 생기는지 못 말한다.** 열역학(convex hull)도 속도론도 여기 없다.
   후보와 그 지문만 준다. 상 동정의 최종 판정은 GI-XRD/XPS/TEM 이 한다.
4. **γ-brass(Cu₅Zn₈) 는 강도를 계산하지 않는다.** 52원자 basis 를 검증된 CIF 로 확보하지
   못해서 `basis=None`(위치 전용)로 넣었다. 위치는 a 와 I-centering 만으로 정확하지만
   강도는 `None` 이다 — 채우려면 검증된 CIF 가 먼저다.
5. **ZHS(Zn₄SO₄(OH)₆·nH₂O) 는 아예 계산하지 않는다.** 수화수 n 에 따라 기저면 간격이
   변하고 검증된 구조가 없다. 문헌 범위만 주석으로 싣는다 — 계산값이 아니다.
6. **B(Debye-Waller) 는 기본 0** 이다. 고각으로 갈수록 강도를 과대평가한다.
7. Kα2 이중선·기기 broadening·zero-shift·시료 변위·흡수·표면거칠기 **전부 없다.**
   실측과의 2θ 차이 0.05–0.2 ° 는 이 도구가 아니라 기기에서 온다.
8. **비정질/나노결정 broadening 없다.** 폭은 계산하지 않는다(위치와 상대강도만).

사용:
    python3 tools/xrd/phase_fingerprint.py --selftest
    python3 tools/xrd/phase_fingerprint.py --report --target 43.0 --window 1.0
    python3 tools/xrd/phase_fingerprint.py --report --csv --json --figure
    python3 tools/xrd/phase_fingerprint.py --depth        # GI-XRD 침투깊이 (덤)
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
import os
import sys

CU_KA1 = 1.540598  # Å, Cu Kα1
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Cromer-Mann 계수 (International Tables Vol C, 6.1.1.4) ────────────────────
#    f(s) = Σ_{i=1..4} a_i exp(-b_i s²) + c,   s = sinθ/λ [Å⁻¹]
#    검산: Σa_i + c ≈ Z  (selftest 가 확인한다)
CM = {
    "H":  ((0.493002, 0.322912, 0.140191, 0.040810),
           (10.5109, 26.1257, 3.14236, 57.7997), 0.003038, 1),
    "O":  ((3.0485, 2.2868, 1.5463, 0.8670),
           (13.2771, 5.7011, 0.3239, 32.9089), 0.2508, 8),
    "S":  ((6.9053, 5.2034, 1.4379, 1.5863),
           (1.4679, 22.2151, 0.2536, 56.1720), 0.8669, 16),
    "Cu": ((13.3380, 7.1676, 5.6158, 1.6735),
           (3.5828, 0.2470, 11.3966, 64.8126), 1.1910, 29),
    "Zn": ((14.0743, 7.0318, 5.1652, 2.4100),
           (3.2655, 0.2333, 10.3163, 58.7097), 1.3041, 30),
    "I":  ((20.1472, 18.9949, 7.5138, 2.2735),
           (4.3470, 0.3814, 27.7660, 66.8776), 4.0712, 53),
}


def f_atom(sym: str, s: float) -> float:
    """원자산란인자. 표에 없는 원소는 조용히 0 을 주지 않고 **예외**를 던진다."""
    if sym not in CM:
        raise KeyError("Cromer-Mann 계수 없음: %r — 표에 추가하기 전엔 못 쓴다" % (sym,))
    a, b, c, _z = CM[sym]
    return sum(ai * math.exp(-bi * s * s) for ai, bi in zip(a, b)) + c


# ── 구조 정의 ────────────────────────────────────────────────────────────────
#  basis: [(원소, 점유율, x, y, z), ...]  (분율좌표, 관용 셀)
#  basis=None → 위치 전용(강도 미계산). refl 은 소광규칙 (h,k,l)->bool.
def _fcc(sym):
    return [(sym, 1.0, 0, 0, 0), (sym, 1.0, 0, .5, .5),
            (sym, 1.0, .5, 0, .5), (sym, 1.0, .5, .5, 0)]


def _hcp(pairs):
    """pairs = [(sym, occ), ...] 를 hcp 2자리에 모두 얹는다 (치환형 고용체용)."""
    out = []
    for sym, occ in pairs:
        out.append((sym, occ, 1 / 3, 2 / 3, 0.25))
        out.append((sym, occ, 2 / 3, 1 / 3, 0.75))
    return out


STRUCTURES = {
    "Cu": dict(
        label="Cu (fcc)", cell=(3.6149, 3.6149, 3.6149, 90, 90, 90),
        basis=_fcc("Cu"),
        src="a=3.6149 Å, Fm-3m, 실험 문헌값 (RT)"),
    "Zn": dict(
        label="Zn (hcp)", cell=(2.6650, 2.6650, 4.9470, 90, 90, 120),
        basis=_hcp([("Zn", 1.0)]),
        src="a=2.6650 c=4.9470 Å (c/a=1.856), P6_3/mmc, 실험 문헌값"),
    "CuZn_beta": dict(
        label=r"CuZn ($\beta'$, CsCl)", cell=(2.9539, 2.9539, 2.9539, 90, 90, 90),
        basis=[("Cu", 1.0, 0, 0, 0), ("Zn", 1.0, .5, .5, .5)],
        src="a=2.9539 Å, Pm-3m 규칙상(β'). 무질서 β(A2)는 같은 위치, 초격자선만 사라짐"),
    "Cu5Zn8_gamma": dict(
        label=r"Cu$_5$Zn$_8$ ($\gamma$-brass)", cell=(8.8780, 8.8780, 8.8780, 90, 90, 90),
        basis=None, refl=lambda h, k, l: (h + k + l) % 2 == 0,
        src="a=8.8780 Å, I-43m. **위치 전용** — 52원자 basis 미확보(위 한계 §4)"),
    "CuZn5_eps": dict(
        label=r"CuZn$_5$ ($\varepsilon$)", cell=(2.7365, 2.7365, 4.2855, 90, 90, 120),
        basis=_hcp([("Cu", 1 / 6), ("Zn", 5 / 6)]),
        src="a=2.7365 c=4.2855 Å (c/a=1.566), P6_3/mmc, Cu/Zn 무질서 점유"),
    "CuI": dict(
        label=r"CuI ($\gamma$, marshite)", cell=(6.0510, 6.0510, 6.0510, 90, 90, 90),
        basis=_fcc("Cu") + [("I", 1.0, x + .25, y + .25, z + .25)
                            for _s, _o, x, y, z in _fcc("I")],
        src="a=6.0510 Å, F-43m zincblende"),
    "ZnO": dict(
        label="ZnO (wurtzite)", cell=(3.2495, 3.2495, 5.2069, 90, 90, 120),
        basis=[("Zn", 1.0, 1 / 3, 2 / 3, 0.0), ("Zn", 1.0, 2 / 3, 1 / 3, 0.5),
               ("O", 1.0, 1 / 3, 2 / 3, 0.3819), ("O", 1.0, 2 / 3, 1 / 3, 0.8819)],
        src="a=3.2495 c=5.2069 Å u=0.3819, P6_3mc"),
    "Cu2O": dict(
        label=r"Cu$_2$O (cuprite)", cell=(4.2696, 4.2696, 4.2696, 90, 90, 90),
        basis=[("Cu", 1.0, .25, .25, .25), ("Cu", 1.0, .25, .75, .75),
               ("Cu", 1.0, .75, .25, .75), ("Cu", 1.0, .75, .75, .25),
               ("O", 1.0, 0, 0, 0), ("O", 1.0, .5, .5, .5)],
        src="a=4.2696 Å, Pn-3m. **요청 목록 밖의 추가 후보** — Cu 집전체의 고전적 표면상"),
}

# 계산하지 않는 상 — 문헌 범위만 (위 한계 §5)
NOT_COMPUTED = {
    "ZHS": dict(
        label="ZHS  Zn4SO4(OH)6·nH2O",
        note=("수화수 n 에 따라 기저면 간격이 달라져 검증된 구조 없이는 계산 불가. "
              "문헌 보고 기저면 d(00l) ≈ 8–11 Å → 2θ(Cu Kα1) ≈ 8–11 °, "
              "그 고차선이 ~16–18 °, ~25 °. **43 ° 부근에는 주선이 없다.**"),
        window_2theta=(8.0, 11.0)),
}


# ── 결정학 ────────────────────────────────────────────────────────────────────
def recip_metric(cell):
    """직접격자 (a,b,c,α,β,γ) → 역격자 계량텐서 G*  (1/d² = h G* hᵀ)."""
    a, b, c, al, be, ga = cell
    if min(a, b, c) <= 0:
        raise ValueError("격자상수는 양수여야 한다: %r" % (cell,))
    if not all(0 < ang < 180 for ang in (al, be, ga)):
        raise ValueError("격자각은 (0,180) 안이어야 한다: %r" % (cell,))
    ca, cb, cg = (math.cos(math.radians(x)) for x in (al, be, ga))
    # 직접격자 계량텐서
    G = [[a * a, a * b * cg, a * c * cb],
         [a * b * cg, b * b, b * c * ca],
         [a * c * cb, b * c * ca, c * c]]
    det = (G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1])
           - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0])
           + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0]))
    if abs(det) < 1e-12:
        raise ValueError("퇴화된 격자(부피 0): %r" % (cell,))
    inv = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            m = [[G[r][c] for c in range(3) if c != i] for r in range(3) if r != j]
            cof = m[0][0] * m[1][1] - m[0][1] * m[1][0]
            inv[i][j] = ((-1) ** (i + j)) * cof / det
    return inv


def d_spacing(Gs, h, k, l):
    v = (h, k, l)
    q = sum(v[i] * Gs[i][j] * v[j] for i in range(3) for j in range(3))
    if q <= 0:
        return None
    return 1.0 / math.sqrt(q)


def two_theta(d, lam):
    if lam <= 0:
        raise ValueError("파장은 양수여야 한다: %r" % (lam,))
    x = lam / (2.0 * d)
    if x > 1.0:
        return None            # 브래그 불가 (d < λ/2)
    return 2.0 * math.degrees(math.asin(x))


def lp_factor(tt_deg):
    th = math.radians(tt_deg / 2.0)
    s, c = math.sin(th), math.cos(th)
    if s < 1e-9 or c < 1e-9:
        return 0.0
    return (1.0 + math.cos(math.radians(tt_deg)) ** 2) / (s * s * c)


def peaks(key, lam=CU_KA1, tt_max=70.0, hkl_max=None, biso=0.0, imin=0.5):
    """한 상의 (2θ, 상대강도, 대표 hkl, 다중도) 목록."""
    st = STRUCTURES[key]
    Gs = recip_metric(st["cell"])
    if hkl_max is None:
        # 요청한 2θ_max 를 확실히 덮는 지수 상한 — 조용한 절단 금지 (한계 §7 아님, 진짜 함정)
        dmin = lam / (2.0 * math.sin(math.radians(min(tt_max, 179.0) / 2.0)))
        amax = max(st["cell"][0], st["cell"][1], st["cell"][2])
        hkl_max = int(math.ceil(amax / dmin)) + 1
    basis, refl = st.get("basis"), st.get("refl")
    groups = {}
    N = hkl_max
    for h in range(-N, N + 1):
        for k in range(-N, N + 1):
            for l in range(-N, N + 1):
                if h == k == l == 0:
                    continue
                if refl is not None and not refl(h, k, l):
                    continue
                d = d_spacing(Gs, h, k, l)
                if d is None:
                    continue
                tt = two_theta(d, lam)
                if tt is None or tt > tt_max or tt < 1e-6:
                    continue
                g = groups.setdefault(round(d, 7), {"d": d, "tt": tt, "m": 0,
                                                    "F2": 0.0, "hkl": (h, k, l)})
                g["m"] += 1
                if basis is not None:
                    s = 1.0 / (2.0 * d)
                    F = 0j
                    for sym, occ, x, y, z in basis:
                        if not (0.0 <= occ <= 1.0):
                            raise ValueError("점유율은 [0,1]: %s occ=%r" % (sym, occ))
                        ph = 2.0 * math.pi * (h * x + k * y + l * z)
                        F += occ * f_atom(sym, s) * math.exp(-biso * s * s) * cmath.exp(1j * ph)
                    g["F2"] += abs(F) ** 2
                # 대표 hkl 은 사전순으로 가장 '양수·큰' 것
                if (h, k, l) > g["hkl"]:
                    g["hkl"] = (h, k, l)
    out = []
    for g in groups.values():
        inten = None if basis is None else g["F2"] * lp_factor(g["tt"])
        out.append({"two_theta": g["tt"], "d": g["d"], "hkl": g["hkl"],
                    "mult": g["m"], "I_raw": inten})
    out.sort(key=lambda r: r["two_theta"])
    scale = max([r["I_raw"] for r in out if r["I_raw"] is not None] or [0.0])
    for r in out:
        r["I_rel"] = None if r["I_raw"] is None else (100.0 * r["I_raw"] / scale if scale else 0.0)
    if basis is not None and imin > 0:
        out = [r for r in out if (r["I_rel"] or 0.0) >= imin]
    return out


# ── GI-XRD 침투깊이 (덤) ──────────────────────────────────────────────────────
MU_CU_LIN = 8.96 * 52.7   # cm⁻¹ — Cu 금속, Cu Kα1(8.048 keV, Cu K edge 8.979 keV 아래)


def info_depth_um(omega_deg, tt_deg=43.3, mu=MU_CU_LIN):
    """고정 입사각 ω 의 1/e 정보깊이 τ = sinω·sin(2θ−ω) / (μ[sinω + sin(2θ−ω)])."""
    w, e = math.radians(omega_deg), math.radians(tt_deg - omega_deg)
    if math.sin(w) <= 0 or math.sin(e) <= 0:
        return None
    tau_cm = math.sin(w) * math.sin(e) / (mu * (math.sin(w) + math.sin(e)))
    return tau_cm * 1e4


# ── selftest ─────────────────────────────────────────────────────────────────
def _ok(c, n, fails):
    if not c:
        fails.append(n)
    return c


def selftest():
    f = []
    P = 0

    # ══ 양성 ═════════════════════════════════════════════════════════════════
    for sym, (a, b, c, z) in CM.items():
        P += 1
        _ok(abs(sum(a) + c - z) < 0.02, "CM Σa+c≈Z (%s: %.4f vs %d)" % (sym, sum(a) + c, z), f)

    Gs = recip_metric(STRUCTURES["Cu"]["cell"])
    aCu = STRUCTURES["Cu"]["cell"][0]
    P += 1; _ok(abs(d_spacing(Gs, 1, 1, 1) - aCu / math.sqrt(3)) < 1e-9, "d(111)=a/√3", f)
    P += 1; _ok(abs(d_spacing(Gs, 2, 0, 0) - aCu / 2.0) < 1e-9, "d(200)=a/2", f)
    d111 = aCu / math.sqrt(3)
    tt = two_theta(d111, CU_KA1)
    P += 1; _ok(abs(tt - 43.32) < 0.05, "Cu(111) 2θ≈43.32 (got %.3f)" % tt, f)
    P += 1; _ok(abs(2 * math.degrees(math.asin(CU_KA1 / (2 * d111))) - tt) < 1e-9, "Bragg 왕복", f)

    # 육방정 d 를 닫힌형과 대조 (계량텐서 경로 검증)
    Gz = recip_metric(STRUCTURES["Zn"]["cell"])
    az, cz = 2.6650, 4.9470
    for (h, k, l) in [(1, 0, 1), (0, 0, 2), (1, 0, 0), (1, 1, 0)]:
        want = 1.0 / math.sqrt(4.0 / 3.0 * (h * h + h * k + k * k) / az ** 2 + l * l / cz ** 2)
        P += 1
        _ok(abs(d_spacing(Gz, h, k, l) - want) < 1e-9, "hcp d%s 닫힌형 일치" % (str((h, k, l))), f)

    # 알려진 위치
    for key, hkl, want in [("Cu", (1, 1, 1), 43.32), ("Zn", (1, 0, 1), 43.21),
                           ("Zn", (0, 0, 2), 36.30), ("CuI", (1, 1, 1), 25.47),
                           ("ZnO", (1, 0, 1), 36.25), ("CuZn_beta", (1, 1, 0), 43.34)]:
        g = recip_metric(STRUCTURES[key]["cell"])
        got = two_theta(d_spacing(g, *hkl), CU_KA1)
        P += 1; _ok(abs(got - want) < 0.10, "%s %s 2θ≈%.2f (got %.3f)" % (key, hkl, want, got), f)

    # 소광: fcc 는 혼합지수 금지 / hcp 는 h+2k=3n & l 홀수 금지 / zincblende (200) 은 살아있음
    pc = {tuple(r["hkl"]) for r in peaks("Cu", tt_max=90)}
    P += 1; _ok(not any((h % 2) != (k % 2) for h, k, l in pc), "fcc 혼합지수 소광", f)
    P += 1; _ok((1, 1, 1) in pc and (2, 0, 0) in pc, "fcc (111)(200) 생존", f)
    pz = {tuple(r["hkl"]) for r in peaks("Zn", tt_max=90)}
    P += 1; _ok((0, 0, 1) not in pz, "hcp (001) 소광", f)
    P += 1; _ok((0, 0, 2) in pz, "hcp (002) 생존", f)
    pi = {tuple(r["hkl"]) for r in peaks("CuI", tt_max=90)}
    P += 1; _ok((2, 0, 0) in pi, "zincblende (200) 약하지만 생존", f)
    pg = {tuple(r["hkl"]) for r in peaks("Cu5Zn8_gamma", tt_max=50)}
    P += 1; _ok(all((h + k + l) % 2 == 0 for h, k, l in pg), "I-centering h+k+l 짝수", f)

    # γ-brass 는 강도가 없어야 한다 (한계 §4 가 코드에 실제로 반영됐는지)
    P += 1; _ok(all(r["I_rel"] is None for r in peaks("Cu5Zn8_gamma", tt_max=50)),
                "γ-brass 강도 None", f)
    P += 1; _ok(all(r["I_rel"] is not None for r in peaks("Cu", tt_max=50)),
                "Cu 강도 존재", f)

    # 최강선 상식
    top = max(peaks("Cu", tt_max=90), key=lambda r: r["I_rel"])
    P += 1; _ok(tuple(top["hkl"]) == (1, 1, 1), "Cu 최강선 = (111)", f)
    P += 1; _ok(peaks("Cu", tt_max=90)[0]["mult"] == 8, "Cu(111) 다중도 8", f)

    # ══ 음성 — 틀린 입력을 실제로 잡아내는가 ═══════════════════════════════════
    def raises(fn, exc=Exception):
        try:
            fn()
        except exc:
            return True
        return False

    P += 1; _ok(raises(lambda: f_atom("Nd", 0.1), KeyError), "N: 미등록 원소 → 예외", f)
    P += 1; _ok(raises(lambda: recip_metric((0, 1, 1, 90, 90, 90))), "N: a=0 → 예외", f)
    P += 1; _ok(raises(lambda: recip_metric((-3, 3, 3, 90, 90, 90))), "N: a<0 → 예외", f)
    P += 1; _ok(raises(lambda: recip_metric((3, 3, 3, 0, 90, 90))), "N: 각도 0 → 예외", f)
    P += 1; _ok(raises(lambda: recip_metric((3, 3, 3, 90, 90, 180))), "N: 각도 180 → 예외", f)
    P += 1; _ok(raises(lambda: two_theta(2.0, 0.0)), "N: λ=0 → 예외", f)
    P += 1; _ok(raises(lambda: two_theta(2.0, -1.0)), "N: λ<0 → 예외", f)

    # 점유율 범위
    bad = dict(STRUCTURES["Cu"]); bad = dict(bad, basis=[("Cu", 1.7, 0, 0, 0)])
    STRUCTURES["_BAD_OCC"] = bad
    P += 1; _ok(raises(lambda: peaks("_BAD_OCC", tt_max=50), ValueError), "N: 점유율>1 → 예외", f)
    STRUCTURES["_BAD_OCC"] = dict(bad, basis=[("Cu", -0.1, 0, 0, 0)])
    P += 1; _ok(raises(lambda: peaks("_BAD_OCC", tt_max=50), ValueError), "N: 점유율<0 → 예외", f)
    STRUCTURES["_BAD_OCC"] = dict(bad, basis=[("Xx", 1.0, 0, 0, 0)])
    P += 1; _ok(raises(lambda: peaks("_BAD_OCC", tt_max=50), KeyError), "N: 가짜 원소 → 예외", f)
    del STRUCTURES["_BAD_OCC"]

    # 소광 검사가 공허하지 않은가 — 면심을 떼면 (100) 이 **살아나야** 한다
    STRUCTURES["_P_CU"] = dict(label="P-Cu", cell=(3.6149,) * 3 + (90, 90, 90),
                               basis=[("Cu", 1.0, 0, 0, 0)], src="음성시험용")
    pp = {tuple(r["hkl"]) for r in peaks("_P_CU", tt_max=90)}
    P += 1; _ok((1, 0, 0) in pp, "N: 면심 제거하면 (100) 부활 (소광검사 공허하지 않음)", f)
    P += 1; _ok((1, 0, 0) not in pc, "N: 면심 있으면 (100) 소광 — 대조", f)
    del STRUCTURES["_P_CU"]

    # 단원자 bcc 는 (100) 이 죽고, CsCl 로 두 원소를 넣으면 살아난다(약하게)
    STRUCTURES["_BCC1"] = dict(label="bcc1", cell=(2.9539,) * 3 + (90, 90, 90),
                               basis=[("Cu", 1.0, 0, 0, 0), ("Cu", 1.0, .5, .5, .5)],
                               src="음성시험용")
    pb = {tuple(r["hkl"]) for r in peaks("_BCC1", tt_max=90)}
    P += 1; _ok((1, 0, 0) not in pb, "N: 단원자 bcc (100) 소광", f)
    pcs = {tuple(r["hkl"]) for r in peaks("CuZn_beta", tt_max=90, imin=0.0)}
    P += 1; _ok((1, 0, 0) in pcs, "N: CsCl 초격자 (100) 부활 (f_Cu≠f_Zn)", f)
    del STRUCTURES["_BCC1"]

    # 지수 상한이 조용히 자르지 않는가 — 상한을 키워도 2θ_max 안의 개수가 안 변해야 한다
    n1 = len(peaks("Cu", tt_max=80))
    n2 = len(peaks("Cu", tt_max=80, hkl_max=9))
    P += 1; _ok(n1 == n2, "N: 자동 hkl 상한이 절단하지 않음 (%d vs %d)" % (n1, n2), f)

    # d < λ/2 는 브래그 불가 → None
    P += 1; _ok(two_theta(CU_KA1 / 2.0 * 0.9, CU_KA1) is None, "N: d<λ/2 → None", f)

    # 침투깊이 단조성 + 비물리 입력
    P += 1; _ok(info_depth_um(1.0) < info_depth_um(5.0) < info_depth_um(15.0),
                "GI 깊이 ω 증가시 단조증가", f)
    P += 1; _ok(info_depth_um(0.0) is None, "N: ω=0 → None", f)
    P += 1; _ok(info_depth_um(43.3) is None, "N: ω=2θ → None (출사각 0)", f)

    print("selftest: %d/%d 통과" % (P - len(f), P))
    for n in f:
        print("  ✗ " + n)
    return 1 if f else 0


# ── 리포트 ───────────────────────────────────────────────────────────────────
def report(target, window, lam, tt_max, imin, want_csv, want_json, want_fig):
    allp = {k: peaks(k, lam=lam, tt_max=tt_max, imin=imin) for k in STRUCTURES}

    print("■ 후보 상 지문 (Cu Kα1 %.6f Å, 2θ ≤ %.0f°, I_rel ≥ %.1f%%)\n" % (lam, tt_max, imin))
    hit = []
    for k, rows in allp.items():
        st = STRUCTURES[k]
        near = [r for r in rows if abs(r["two_theta"] - target) <= window]
        for r in near:
            hit.append((r["two_theta"], k, st["label"], r["hkl"], r["I_rel"]))
    hit.sort()

    print("● %.1f° ± %.1f° 안에 들어오는 반사 — **여기가 문제의 창**" % (target, window))
    print("   %-9s %-26s %-10s %8s" % ("2θ(°)", "상", "hkl", "I_rel"))
    for tt, k, lab, hkl, ir in hit:
        s = "  n/a" if ir is None else "%5.1f" % ir
        print("   %-9.2f %-26s %-10s %8s" % (tt, k, "(%d%d%d)" % hkl, s))
    if len(hit) >= 2:
        print("   → **%d 개 상이 %.2f° 폭 안에 겹친다.** 2θ 분해만으로는 못 가른다."
              % (len(hit), max(h[0] for h in hit) - min(h[0] for h in hit)))

    # Cu 가 비어 있는 창 = 진단창
    cu_tt = sorted(r["two_theta"] for r in allp["Cu"])
    print("\n● Cu 반사가 없는 구간 (진단창 후보), 2θ ≤ %.0f°" % tt_max)
    prev = 0.0
    gaps = []
    for t in cu_tt + [tt_max]:
        if t - prev > 5.0:
            gaps.append((prev, t))
        prev = t
    for lo, hi in gaps:
        inside = []
        for k, rows in allp.items():
            if k == "Cu":
                continue
            for r in rows:
                if lo + 0.5 < r["two_theta"] < hi - 0.5 and (r["I_rel"] or 0) >= 10:
                    inside.append((r["two_theta"], k, r["hkl"], r["I_rel"]))
        if inside:
            inside.sort()
            print("   %.1f–%.1f° :" % (lo, hi))
            for tt, k, hkl, ir in inside:
                print("       %6.2f°  %-14s (%d%d%d)  I=%.0f" % (tt, k, hkl[0], hkl[1], hkl[2], ir))

    print("\n● 계산하지 않은 상")
    for k, v in NOT_COMPUTED.items():
        print("   %-8s %s" % (k, v["note"]))

    rows_out = []
    for k, rows in allp.items():
        for r in rows:
            rows_out.append(dict(phase=k, label=STRUCTURES[k]["label"],
                                 h=r["hkl"][0], k_=r["hkl"][1], l=r["hkl"][2],
                                 two_theta_deg=round(r["two_theta"], 4),
                                 d_A=round(r["d"], 5), multiplicity=r["mult"],
                                 I_rel=None if r["I_rel"] is None else round(r["I_rel"], 2)))
    if want_csv:
        p = os.path.join(REPO, "db", "properties", "zn_cu_phase_fingerprint_2026_09_03.csv")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("phase,label,h,k,l,two_theta_deg,d_A,multiplicity,I_rel_percent\n")
            for r in sorted(rows_out, key=lambda x: (x["phase"], x["two_theta_deg"])):
                fh.write("%s,%s,%d,%d,%d,%.4f,%.5f,%d,%s\n" % (
                    r["phase"], r["label"].replace(",", ";"), r["h"], r["k_"], r["l"],
                    r["two_theta_deg"], r["d_A"], r["multiplicity"],
                    "" if r["I_rel"] is None else "%.2f" % r["I_rel"]))
        print("\nCSV → %s" % os.path.relpath(p, REPO))
    if want_json:
        p = os.path.join(REPO, "db", "properties", "zn_cu_phase_fingerprint_2026_09_03.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({
                "generated": "2026-09-03", "wavelength_A": lam, "source": "Cu Ka1",
                "tool": "tools/xrd/phase_fingerprint.py",
                "purpose": ("Zn ALZIB 협업 C1 — pre-conditioned Cu 의 43도 부근 반사 귀속 "
                            "(kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md G1)"),
                "lattice_source": "실험 문헌 격자상수 (DFT 이완값 아님)",
                "limits": ["Rietveld 정량 아님 · 무작위 배향 가정 (전착 Zn 은 002 texture)",
                           "어느 상이 실제 생기는지 말하지 않음 (열역학·속도론 없음)",
                           "Cu5Zn8 gamma 는 위치 전용 (52원자 basis 미확보) — 강도 null",
                           "ZHS 는 미계산 (수화수 n 미정) — 문헌 범위만",
                           "B_iso=0 · Ka2/기기 broadening/zero-shift 없음"],
                "structures": {k: {"label": v["label"], "cell": v["cell"], "source": v["src"]}
                               for k, v in STRUCTURES.items()},
                "not_computed": NOT_COMPUTED,
                "peaks": sorted(rows_out, key=lambda x: (x["phase"], x["two_theta_deg"])),
            }, fh, ensure_ascii=False, indent=1)
        print("JSON → %s" % os.path.relpath(p, REPO))
    if want_fig:
        _figure(allp, target, window, lam)
    return 0


def _figure(allp, target, window, lam):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, REPO)
    from tools.figures.house_style import INK, MUT

    order = ["Cu", "Zn", "CuZn_beta", "Cu5Zn8_gamma", "CuZn5_eps", "CuI", "ZnO", "Cu2O"]
    col = {"Cu": "#b45309", "Zn": "#0d9488", "CuZn_beta": "#7c3aed",
           "Cu5Zn8_gamma": "#9ca3af", "CuZn5_eps": "#2563eb", "CuI": "#65a30d",
           "ZnO": "#be123c", "Cu2O": "#0284c7"}
    fig, ax = plt.subplots(figsize=(8.4, 5.6))
    for i, k in enumerate(order):
        base = len(order) - 1 - i
        for r in allp[k]:
            h = 0.80 * ((r["I_rel"] or 35.0) / 100.0)
            ax.plot([r["two_theta"]] * 2, [base, base + h], lw=1.5,
                    color=col[k], solid_capstyle="butt",
                    ls="-" if r["I_rel"] is not None else ":")
        ax.text(70.6, base + 0.30, STRUCTURES[k]["label"], color=col[k],
                fontsize=9, va="center", ha="left")
    ax.axvspan(target - window, target + window, color="#fef9c3", zorder=0)
    ax.axvline(target, color="#2563eb", ls="--", lw=1.1, zorder=1)
    ax.text(target, len(order) - 0.28, "  ambiguous 43° window",
            color="#2563eb", fontsize=9, va="top", ha="left")
    ax.set_xlim(20, 70); ax.set_ylim(-0.15, len(order) - 0.1)
    ax.set_xlabel(r"2$\theta$ (deg), Cu K$\alpha_1$ %.4f $\AA$" % lam, color=INK)
    ax.set_yticks([])
    ax.tick_params(colors=MUT)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUT)
    ax.set_title("Candidate phases on pre-conditioned Cu — simulated powder XRD",
                 color=INK, fontsize=11)
    ax.text(20.4, len(order) - 0.30, "dotted = positions only (no intensity)",
            color=MUT, fontsize=8, va="top")
    fig.tight_layout()
    p = os.path.join(REPO, "docs", "figures", "zn", "zn_cu_phase_fingerprint.png")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    fig.savefig(p, dpi=300)
    print("FIG  → %s" % os.path.relpath(p, REPO))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--depth", action="store_true", help="GI-XRD 정보깊이 vs 입사각 ω")
    ap.add_argument("--target", type=float, default=43.0)
    ap.add_argument("--window", type=float, default=1.0)
    ap.add_argument("--lam", type=float, default=CU_KA1)
    ap.add_argument("--tt-max", type=float, default=70.0)
    ap.add_argument("--imin", type=float, default=1.0, help="상대강도 컷 (%%)")
    ap.add_argument("--csv", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--figure", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.depth:
        print("■ GI-XRD 1/e 정보깊이 (Cu 금속, Cu Kα1, μ=%.0f cm⁻¹, 2θ=43.3°)" % MU_CU_LIN)
        print("  ⚠ Cu 만의 값이다. 층이 Zn/CuI 면 μ 가 달라진다 — 대략의 눈금으로만 써라.")
        for w in (0.3, 0.5, 1, 2, 3, 5, 8, 10, 15):
            d = info_depth_um(w)
            print("   ω = %5.1f°   τ ≈ %7.3f µm" % (w, d))
        print("  → 2–4 µm 층 전체를 보려면 ω ≈ 8–15°, 최표면(<0.5 µm)만 보려면 ω ≲ 1–2°.")
        return 0
    if a.report:
        return report(a.target, a.window, a.lam, a.tt_max, a.imin, a.csv, a.json, a.figure)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
