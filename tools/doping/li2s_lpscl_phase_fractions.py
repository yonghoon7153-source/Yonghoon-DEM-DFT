#!/usr/bin/env python3
"""li2s_lpscl_phase_fractions.py — Li₂S + LPSCl 볼밀 복합체의 **상 분율 장부**(전환율 ξ 의 함수) + 유효매질 σ 추정.

질문 (재민, 2026-09-11): 3:5 wt 로 밀링하면 Li₂S · LPSCl · Li₃PS₄ · LiCl 이 어떤 질량비(몰비)로 있게 되나, 전도도는?

반응 (0층 hull · Cronk 2026 실측과 정합): Li₆PS₅Cl → Li₃PS₄ + LiCl + Li₂S  (Li₂S 는 소모되지 않는다)
  전환율 ξ ∈ [0,1] 은 **기계화학적 양**이라 계산으로 못 정한다 — 실험(XRD Rietveld LiCl wt% · XANES S K-edge LCF)에서 읽는다.
  이 도구는 ξ 를 받아 질량·몰 장부를 내고, 반대로 관측된 LPSCl 의 S 분율(LCF)에서 ξ 를 역산한다.

유효매질 σ (선택): SE 망(LPSCl + Li₃PS₄-like + LiCl)만 3D 대칭 Bruggeman 으로 푼다 — **입력 σ 는 사용자가 준다**
  (예: Cronk 2026 자기 실측 LPSCl 2e-3 · 밀링 LPS 4e-5 S/cm, LiCl ≈ 0). 활물질·탄소는 SE 망 밖의 부피로 취급(희석 인자).
  ⛔ 이것은 **상한 성격의 어림**이다 — 미세구조(코팅 vs 분산 · 접촉)를 모른다. DEM/FEM 이 그 다음이다.

⛔ 이 도구가 못 하는 것
  · ξ 를 예측하지 않는다 (밀링 에너지·시간 의존) · 비정질 LPS 의 조성이 정확히 Li₃PS₄ 인지 보증 못 한다 (Cl 잔류 가능 — 1층이 답한다)
  · σ 절대값을 만들지 않는다 — 입력값의 산술이다 · 미세구조를 모른다 · 이온전도 '향상' 여부의 물리적 판단을 대신하지 않는다

  python3 tools/doping/li2s_lpscl_phase_fractions.py --ratio 3 5 --xi 0.25 0.5 1.0
  python3 tools/doping/li2s_lpscl_phase_fractions.py --ratio 3 5 --lcf_lpscl_S 0.332
  python3 tools/doping/li2s_lpscl_phase_fractions.py --ratio 3 5 --xi 0.45 --sigma 2e-3 4e-5 1e-9 --rho 1.64 1.87 2.07 --inert_wt 0.2
  python3 tools/doping/li2s_lpscl_phase_fractions.py --selftest
"""
from __future__ import annotations
import argparse, json, sys

M = {"Li2S": 45.947, "LPSCl": 268.398, "Li3PS4": 180.034, "LiCl": 42.394}
S_ATOMS = {"Li2S": 1, "LPSCl": 5, "Li3PS4": 4, "LiCl": 0}
M_S = 32.06


def ledger(w_li2s, w_lpscl, xi):
    """질량 w(g) 출발, 전환율 ξ → 상별 mol · g · wt% · mol%."""
    if not (0.0 <= xi <= 1.0):
        raise SystemExit(f"⛔ ξ 는 [0,1] 이어야 한다 — 받은 것 {xi}")
    n0 = {"Li2S": w_li2s / M["Li2S"], "LPSCl": w_lpscl / M["LPSCl"]}
    conv = n0["LPSCl"] * xi
    n = {"LPSCl": n0["LPSCl"] - conv, "Li3PS4": conv, "LiCl": conv, "Li2S": n0["Li2S"] + conv}
    g = {k: n[k] * M[k] for k in n}
    tot_g = sum(g.values()); tot_n = sum(n.values())
    return {"xi": xi, "mol": n, "g": g, "wt_pct": {k: 100 * g[k] / tot_g for k in g},
            "mol_pct": {k: 100 * n[k] / tot_n for k in n}, "total_g": tot_g}


def s_fraction(led):
    """상별 S 원자 분율 (XANES S K-edge LCF 가중치에 대응)."""
    s = {k: led["mol"][k] * S_ATOMS[k] for k in led["mol"]}
    tot = sum(s.values())
    return {k: s[k] / tot for k in s}


def xi_from_lcf_lpscl(w_li2s, w_lpscl, f_lpscl_S):
    """관측된 LPSCl 의 S 분율 → ξ (닫힌 식: f = f0·(1−ξ), f0 = ξ=0 일 때 LPSCl S 분율)."""
    f0 = s_fraction(ledger(w_li2s, w_lpscl, 0.0))["LPSCl"]
    if not (0 < f_lpscl_S <= f0):
        raise SystemExit(f"⛔ LPSCl S 분율 {f_lpscl_S} 이 (0, {f0:.3f}] 밖이다 — ξ=0 에서도 그보다 클 수 없다")
    return 1.0 - f_lpscl_S / f0


def bruggeman(phi, sigma, iters=200):
    """3D 대칭 Bruggeman: Σ φ_i (σ_i − σ_e)/(σ_i + 2σ_e) = 0 을 이분법으로. φ 는 합 1."""
    if abs(sum(phi) - 1) > 1e-9 or any(s < 0 for s in sigma) or any(p < 0 for p in phi):
        raise SystemExit("⛔ 부피분율 합 1 · σ ≥ 0 · φ ≥ 0 이어야 한다")
    lo, hi = 0.0, max(sigma)
    f = lambda se: sum(p * (s - se) / (s + 2 * se) for p, s in zip(phi, sigma) if p > 0)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if mid <= 0:
            break
        (lo, hi) = (mid, hi) if f(mid) > 0 else (lo, mid)
    return 0.5 * (lo + hi)


def sigma_eff(led, sigma, rho, inert_wt=0.0):
    """SE 망(LPSCl · Li3PS4 · LiCl) Bruggeman → 활물질(Li2S)·불활성(탄소 등)을 부피 희석으로 곱한 어림."""
    keys = ["LPSCl", "Li3PS4", "LiCl"]
    vol = {k: led["g"][k] / rho[k] for k in keys}
    v_se = sum(vol.values())
    phi = [vol[k] / v_se for k in keys]
    se = bruggeman(phi, [sigma[k] for k in keys])
    v_li2s = led["g"]["Li2S"] / rho["Li2S"]
    tot_g = led["total_g"] / (1 - inert_wt) if inert_wt < 1 else led["total_g"]
    v_inert = (tot_g - led["total_g"]) / rho.get("inert", 2.0)
    dilution = v_se / (v_se + v_li2s + v_inert)
    return {"phi_SE": dict(zip(keys, phi)), "sigma_SE_network": se, "SE_volume_fraction_of_composite": dilution,
            "sigma_composite_dilution_bound": se * dilution ** 1.5,   # Bruggeman 유효매질의 절연 희석 근사 (φ^1.5)
            "⛔": "미세구조 미지 — 상한 성격 어림. 코팅/접촉은 DEM/FEM 이 답한다"}


def _selftest():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += c; bad += (not c)
    L0 = ledger(3, 5, 0.0); L1 = ledger(3, 5, 1.0); L5 = ledger(3, 5, 0.5)
    chk(abs(L0["total_g"] - 8) < 1e-9 and abs(L1["total_g"] - 8) < 1e-3 and abs(L5["total_g"] - 8) < 1e-3, "질량 보존 (ξ 0 · 0.5 · 1)")
    chk(L0["g"]["Li3PS4"] == 0 and L0["g"]["LiCl"] == 0 and abs(L0["g"]["LPSCl"] - 5) < 1e-12, "ξ=0 → 출발 조성")
    chk(L1["g"]["LPSCl"] < 1e-12 and abs(L1["mol"]["Li3PS4"] - L1["mol"]["LiCl"]) < 1e-12, "ξ=1 → LPSCl 0 · Li3PS4 = LiCl (mol)")
    chk(abs(L1["mol"]["Li2S"] - (3 / M["Li2S"] + 5 / M["LPSCl"])) < 1e-12, "ξ=1 → Li2S = 초기 + 전환 LPSCl 몰수")
    for el, n_el in (("Li", lambda n: 2*n["Li2S"] + 6*n["LPSCl"] + 3*n["Li3PS4"] + n["LiCl"]),
                     ("S", lambda n: n["Li2S"] + 5*n["LPSCl"] + 4*n["Li3PS4"]),
                     ("Cl", lambda n: n["LPSCl"] + n["LiCl"]), ("P", lambda n: n["LPSCl"] + n["Li3PS4"])):
        chk(abs(n_el(L0["mol"]) - n_el(L5["mol"])) < 1e-12 and abs(n_el(L0["mol"]) - n_el(L1["mol"])) < 1e-12, f"원소 보존 {el}")
    f = s_fraction(L5)["LPSCl"]
    chk(abs(xi_from_lcf_lpscl(3, 5, f) - 0.5) < 1e-9, "LCF 역산 왕복: ξ=0.5 의 LPSCl S 분율 → 0.5")
    try:
        ledger(3, 5, 1.2); ok_x = False
    except SystemExit:
        ok_x = True
    chk(ok_x, "⛔음성: ξ > 1 거부")
    try:
        xi_from_lcf_lpscl(3, 5, 0.9); ok_f = False
    except SystemExit:
        ok_f = True
    chk(ok_f, "⛔음성: ξ=0 보다 큰 LPSCl S 분율은 역산 거부")
    chk(abs(bruggeman([1.0, 0.0], [2e-3, 4e-5]) - 2e-3) < 1e-9, "Bruggeman: 단일상이면 그 σ")
    chk(abs(bruggeman([0.5, 0.5], [1.0, 1.0]) - 1.0) < 1e-9, "Bruggeman: 같은 σ 두 상이면 그 σ")
    chk(bruggeman([0.2, 0.8], [1.0, 0.0]) < 1e-9, "Bruggeman: 도체 20 % 는 3D 문턱(1/3) 아래라 0 (퍼컬레이션)")
    chk(0 < bruggeman([0.5, 0.5], [1.0, 0.0]) < 1.0, "Bruggeman: 도체 50 % 는 0 과 1 사이")
    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="Li2S+LPSCl 볼밀 상 분율 장부 · 유효매질 σ 어림")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--ratio", type=float, nargs=2, default=[3, 5], metavar=("W_LI2S", "W_LPSCL"), help="질량비 (기본 3 5)")
    ap.add_argument("--xi", type=float, nargs="*", default=[], help="전환율 ξ 목록")
    ap.add_argument("--lcf_lpscl_S", type=float, help="XANES LCF 의 LPSCl S 분율 → ξ 역산")
    ap.add_argument("--sigma", type=float, nargs=3, metavar=("LPSCL", "LI3PS4", "LICL"), help="S/cm (사용자 입력 — 소환값이면 출처 명시)")
    ap.add_argument("--rho", type=float, nargs=3, default=[1.64, 1.87, 2.07], metavar=("LPSCL", "LI3PS4", "LICL"), help="g/cm³ (기본: 결정 밀도 어림)")
    ap.add_argument("--rho_li2s", type=float, default=1.66)
    ap.add_argument("--inert_wt", type=float, default=0.0, help="SE 망 밖 불활성(탄소 등) 질량분율 (예: 0.2)")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    w1, w2 = a.ratio
    xis = list(a.xi)
    if a.lcf_lpscl_S is not None:
        xi = xi_from_lcf_lpscl(w1, w2, a.lcf_lpscl_S)
        print(f"LCF LPSCl S 분율 {a.lcf_lpscl_S} → ξ = {xi:.3f}")
        xis.append(xi)
    if not xis:
        ap.error("--xi 또는 --lcf_lpscl_S 를 주어라")
    print(f"출발 {w1:g} g Li2S + {w2:g} g LPSCl  (x_Li2S = {(w1/M['Li2S'])/(w1/M['Li2S']+w2/M['LPSCl']):.3f} mol frac)")
    print(f"{'ξ':>5s} | {'LPSCl':>13s} | {'Li3PS4':>13s} | {'LiCl':>13s} | {'Li2S':>13s}   (g / wt% / mol%)")
    for xi in xis:
        L = ledger(w1, w2, xi)
        cells = [f"{L['g'][k]:.3f}/{L['wt_pct'][k]:.1f}/{L['mol_pct'][k]:.1f}" for k in ("LPSCl", "Li3PS4", "LiCl", "Li2S")]
        print(f"{xi:5.2f} | " + " | ".join(f"{c:>13s}" for c in cells))
        if a.sigma:
            sig = dict(zip(("LPSCl", "Li3PS4", "LiCl"), a.sigma)); rho = dict(zip(("LPSCl", "Li3PS4", "LiCl"), a.rho)); rho["Li2S"] = a.rho_li2s
            r = sigma_eff(L, sig, rho, a.inert_wt)
            print(f"        SE 망 φ {', '.join(f'{k} {v:.2f}' for k, v in r['phi_SE'].items())} → σ_SE {r['sigma_SE_network']:.2e} S/cm"
                  f" · SE 부피분율 {r['SE_volume_fraction_of_composite']:.2f} → 희석 어림 {r['sigma_composite_dilution_bound']:.2e} S/cm")


if __name__ == "__main__":
    main()
