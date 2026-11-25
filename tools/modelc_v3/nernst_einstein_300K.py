#!/usr/bin/env python3
"""300 K Nernst-Einstein ionic conductivity from the paper-grade Arrhenius fits.

We have D(T) from MLIP-MD (UMA-s-1p1) at 600/800/1000 K and the Arrhenius fit
ln D = ln D0 - Ea/(kB T). This extrapolates D to 300 K and converts to an ionic
conductivity via the Nernst-Einstein (Einstein) relation, Haven ratio H_R = 1:

    sigma_NE = n_Li * z^2 * e^2 * D / (kB * T)        (z = +1 for Li)

n_Li = (# Li in MD cell) / (cell volume). This is the SAME convention used to
produce the stored modelc value (~14 mS/cm), so the two compositions are
directly comparable.

⛔ 2026-09-07 CORRECTION — this docstring used to say "Absolute sigma carries MLIP
overshoot (~3-5x) and the **H_R=1 inflation (~2x)**".  The second half had the SIGN
BACKWARDS, and it contradicted line ~234 of this very file, which already said it
correctly.  With H_R = D*/D_sigma and our MSD giving D*:

    sigma_NE = n q^2 D* /(kB T) = H_R * sigma_true      =>  H_R < 1 makes NE an
                                                            UNDER-estimate, not an upper bound.

Adeli 2019 measures H_R = 0.23 for Li5.5PS4.5Cl1.5 => sigma_true ~ 4.3x sigma_NE.
The "3-5x overshoot" number appears to come from comparing sigma_NE against
**cold-pressed pellet total EIS**, a comparison that already mixes (a) this Haven
factor and (b) grain-boundary/porosity loss in the pellet — which push in OPPOSITE
directions.  Compared like-for-like our D* is fine: D*(300 K, single-seed) 1.02e-7
vs Adeli 7Li PFG D* 1.01e-7 cm^2/s.
=> The robust quantities are Ea and D*; what is unsettled is the D* -> sigma step.
   See kb/concepts/md.md §6 and `--haven` in tools/ionic/msd_diffusive_check.py.

--segment  (2026-08-24 추가)
    ⛔ 위 기본 모드는 **600–1000 K 를 한 직선으로** 적합한 Ea·D0 를 쓴다. b2o3 는
      2026-08-23 에 그 가정이 깨졌다 (600→800 0.222 eV / 800→1000 0.077 eV, 145 meV
      굽음). 굽은 곡선을 평균낸 Ea 로 300 K 를 외삽하면 **저온을 실제보다 쉽게** 본다.
      300 K 로 내려가는 외삽에 쓸 수 있는 것은 **저온 구간(600→800)** 뿐이다.
    이 모드는 arrhenius json 의 시드별 D 를 읽어 **시드마다** 두 점 구간 적합을 하고,
    시드 분산을 그대로 전파한다 (평균을 먼저 내고 적합하지 않는다 — 그러면 분산이 사라진다).

이 도구가 **못 하는 것**
    · 굽음 자체를 설명하지 못한다. 구간을 나눠 쓸 뿐이다.
    · 600 K 아래 실측이 없으므로 0.222 eV 가 300 K 까지 이어진다는 **가정**을 검증 못 한다.
      db 의 supplementary 400/500 K 는 MSD 창이 달라(5-40) 바로 못 붙인다.
    · Haven 비를 1 로 둔다. σ 절대값은 CLAUDE.md 규율상 **인용 금지**다 (비율만).
"""
import argparse
import pathlib
import json
import sys

import numpy as np

# physical constants
kB_eV = 8.617333262e-5      # eV/K
kB_J = 1.380649e-23         # J/K
e = 1.602176634e-19         # C


def segment_fit(T_lo, D_lo, T_hi, D_hi):
    """두 점 아레니우스 구간 적합 → (Ea_eV, D0). 입력이 틀리면 **조용히 넘기지 않는다.**"""
    if T_lo <= 0 or T_hi <= 0:
        raise ValueError(f"온도는 양수여야 한다: {T_lo}, {T_hi}")
    if T_lo == T_hi:
        raise ValueError(f"두 온도가 같다 ({T_lo} K) — 구간 적합이 성립하지 않는다")
    if D_lo <= 0 or D_hi <= 0:
        raise ValueError(f"D 는 양수여야 한다: {D_lo}, {D_hi}")
    Ea = kB_eV * np.log(D_hi / D_lo) / (1.0 / T_lo - 1.0 / T_hi)
    D0 = D_lo * np.exp(Ea / (kB_eV * T_lo))
    return float(Ea), float(D0)


def sigma_NE(n_cm3, D_cm2s, T):
    """Nernst-Einstein (H_R = 1, z = +1) → S/cm."""
    return n_cm3 * e ** 2 * D_cm2s / (kB_J * T)


def run_segment(path, T_lo, T_hi, T_out, n_cm3=None):
    """arrhenius json 의 시드별 D 로 구간 외삽. 시드마다 적합해 분산을 전파한다."""
    d = json.load(open(path))
    ms, src = None, None
    for k, v in d.items():
        if isinstance(v, dict) and isinstance(v.get("multiseed_3x3"), dict):
            ms, src = v["multiseed_3x3"], k
            break
    if ms is None:
        raise SystemExit(f"⛔ {path} 에 multiseed_3x3 블록이 없다 — 시드별 D 가 있어야 한다")
    for T in (T_lo, T_hi):
        if str(T) not in ms:
            raise SystemExit(f"⛔ {T} K 의 시드별 D 가 없다 (있는 것: {sorted(ms)})")
    lo, hi = ms[str(T_lo)], ms[str(T_hi)]
    if len(lo) != len(hi):
        raise SystemExit(f"⛔ 시드 수가 다르다 ({T_lo} K {len(lo)}개 vs {T_hi} K {len(hi)}개) "
                         f"— 시드끼리 짝을 못 짓는다")
    if n_cm3 is None:
        n_cm3 = d.get("FINAL_for_paper", {}).get("n_Li_cm3")
        if n_cm3 is None:
            raise SystemExit("⛔ n_Li_cm3 가 db 에 없다 — --n_li 로 줄 것")

    print("=" * 74)
    print(f" 구간 아레니우스 외삽  {T_lo}→{T_hi} K  ⇒  {T_out} K   (시드별 적합)")
    print(f" 출처: {path}  ·  {src}.multiseed_3x3  ·  n_Li = {n_cm3:.4e} cm^-3")
    print("=" * 74)
    rows = []
    for i, (a, b) in enumerate(zip(lo, hi)):
        Ea, D0 = segment_fit(T_lo, a, T_hi, b)
        Dx = D0 * np.exp(-Ea / (kB_eV * T_out))
        sg = sigma_NE(n_cm3, Dx, T_out) * 1e3
        rows.append((Ea, D0, Dx, sg))
        print(f"  seed{i + 1}:  D({T_lo})={a:.4e}  D({T_hi})={b:.4e}  →  "
              f"Ea={Ea:.4f} eV  D({T_out})={Dx:.4e}  sigma={sg:.2f} mS/cm")
    Ea_v = np.array([r[0] for r in rows])
    Dx_v = np.array([r[2] for r in rows])
    sg_v = np.array([r[3] for r in rows])
    print("-" * 74)
    print(f"  Ea        = {Ea_v.mean():.4f} +/- {Ea_v.std(ddof=1):.4f} eV   "
          f"(시드 {len(rows)}개, ddof=1)")
    print(f"  D({T_out}K)  = {Dx_v.mean():.4e} +/- {Dx_v.std(ddof=1):.2e} cm^2/s")
    print(f"  sigma({T_out}K) = {sg_v.mean():.2f} +/- {sg_v.std(ddof=1):.2f} mS/cm   "
          f"[범위 {sg_v.min():.2f}–{sg_v.max():.2f}, {sg_v.max() / sg_v.min():.1f}배]")
    print("-" * 74)
    # ⛔⛔ BI-4 P1 (2026-09-09) — 종전에는 여기서 "비교는 비율로만" 이라고 **권했다.**
    #   그런데 정책 게이트를 우회해서 나온 출력에도 같은 문장이 붙었다. 마감 카드가
    #   그 축의 **수송 비교 자체**를 금지하는데 이 도구가 비교 방법을 안내한 것이다.
    #   ⇒ 권고를 지운다. 이 도구는 값을 내지 **쓰는 법을 말하지 않는다**.
    print("  ⛔ σ 절대값은 인용하지 않는다 (CLAUDE.md). MLIP D 과대 + H_R=1 이 겹쳐 있고,")
    print(f"     위 표대로 시드만 바꿔도 {sg_v.max() / sg_v.min():.1f}배 흔들린다.")
    print("     ⚠ 비율 비교가 허용되는지는 **그 축의 마감 카드가 정한다** — 여기서 권하지 않는다")
    print("       (`python3 tools/db/policy.py <원자료>` 로 확인해라).")
    print(f"  ⚠ {T_lo} K 아래 실측이 없다 — Ea={Ea_v.mean():.3f} 이 {T_out} K 까지")
    print("     이어진다는 것은 검증된 사실이 아니라 **가정**이다.")
    return dict(Ea_mean=float(Ea_v.mean()), Ea_std=float(Ea_v.std(ddof=1)),
                D_mean=float(Dx_v.mean()), D_std=float(Dx_v.std(ddof=1)),
                sigma_mScm_mean=float(sg_v.mean()), sigma_mScm_std=float(sg_v.std(ddof=1)),
                sigma_mScm_per_seed=[float(x) for x in sg_v],
                n_Li_cm3=float(n_cm3), T_lo=T_lo, T_hi=T_hi, T_out=T_out,
                n_seeds=len(rows))


def _selftest():
    """양성 1 · 음성 5. 음성이 없으면 이 selftest 는 아무것도 보증하지 못한다."""
    ok, neg = True, 0

    def say(good, msg):
        nonlocal ok
        print(("  ✓ " if good else "  ✗ ") + msg)
        if not good:
            ok = False

    # ① 양성: 알려진 Ea·D0 로 두 점을 만들면 정확히 되돌아와야 한다
    Ea0, D00 = 0.2500, 1.0e-3
    a = D00 * np.exp(-Ea0 / (kB_eV * 600))
    b = D00 * np.exp(-Ea0 / (kB_eV * 800))
    Ea, D0 = segment_fit(600, a, 800, b)
    say(abs(Ea - Ea0) < 1e-9 and abs(D0 / D00 - 1) < 1e-9,
        f"① 왕복: Ea {Ea:.6f} (={Ea0}) · D0 {D0:.4e} (={D00:.1e})")
    # ② 양성: 온도 의존이 없으면 Ea = 0
    say(abs(segment_fit(600, 1e-5, 800, 1e-5)[0]) < 1e-15, "② D 가 같으면 Ea = 0")
    # ③ 음성: 같은 온도 두 개
    for name, args in (("③ 같은 온도", (600, 1e-5, 600, 2e-5)),
                       ("④ D ≤ 0", (600, 0.0, 800, 1e-5)),
                       ("⑤ 음수 D", (600, 1e-5, 800, -1e-5)),
                       ("⑥ 0 K", (0, 1e-5, 800, 1e-5))):
        neg += 1
        try:
            segment_fit(*args)
            say(False, f"{name}: 예외가 안 났다 — 조용히 틀린 값을 낸다")
        except ValueError:
            say(True, f"{name}: ValueError 로 막힌다")
    # ⑦ 음성: 굽음을 무시하면 안 된다는 것을 수치로 — 두 구간 Ea 가 다르면
    #    전구간 단일적합은 어느 구간과도 다르다 (평균이 저온을 과소평가한다)
    neg += 1
    D6, D8, D10 = 1.041e-5, 3.044e-5, 3.809e-5
    Ea_lo = segment_fit(600, D6, 800, D8)[0]
    Ea_hi = segment_fit(800, D8, 1000, D10)[0]
    x = np.array([1 / 600, 1 / 800, 1 / 1000])
    Ea_all = -kB_eV * np.polyfit(x, np.log([D6, D8, D10]), 1)[0]
    say(Ea_lo > Ea_all > Ea_hi and (Ea_lo - Ea_hi) > 0.10,
        f"⑦ 굽음: 저온 {Ea_lo:.4f} > 전구간 {Ea_all:.4f} > 고온 {Ea_hi:.4f} eV "
        f"(차 {Ea_lo - Ea_hi:.3f}) — 단일적합은 저온을 {Ea_lo - Ea_all:.3f} eV 과소평가")
    print(f"\n  {'✅ selftest 통과' if ok else '⛔ selftest 실패'} (음성 {neg}건 포함)")
    return 0 if ok else 1

_ap = argparse.ArgumentParser(description=__doc__,
                              formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--selftest", action="store_true")
_ap.add_argument("--segment", metavar="JSON",
                 help="시드별 D 가 든 arrhenius json 으로 **구간** 외삽 "
                      "(굽은 계는 전구간 단일적합을 쓰면 안 된다)")
_ap.add_argument("--T_lo", type=int, default=600)
_ap.add_argument("--T_hi", type=int, default=800)
_ap.add_argument("--T_out", type=int, default=300)
_ap.add_argument("--n_li", type=float, default=None, help="Li 수밀도 cm^-3 (기본: db 값)")
_ap.add_argument("--json_out", default=None, help="결과를 json 으로 떨군다")
#: ⛔ BI-3 P0-4 (2026-09-09) — 마감된 축의 원자료를 받으면 **시작하지 않는다.**
#:   실측 사고: 이 도구에 `b2o3_md_arrhenius.json` 을 주면 정상 종료하면서
#:   `Ea = 0.2241 eV` 와 300 K 외삽 D·σ 를 다시 만들고 "비교는 비율로만" 이라고 권했다.
#:   마감 카드가 그 축의 **수송 비교와 300 K 외삽을 둘 다 금지**하는데도.
#:   원인은 이 도구가 개명된 필드가 아니라 **다른 가지**(`⛔_RETRACTED….multiseed_3x3`)를
#:   키 이름으로 훑기 때문 — 원자료 정정이 하류에 안 닿았다.
_ap.add_argument("--policy_override", metavar="사유",
                 help="마감된 축을 **그래도** 돌린다 (이력·진단 목적). 사유가 필수이고 "
                      "출력·json 에 우회 스탬프가 박힌다.")
_a = _ap.parse_args()

if _a.selftest:
    sys.exit(_selftest())

if _a.segment:
    # ⛔ 정책 먼저 — 계산 뒤에 물으면 이미 숫자가 화면에 나가 있다.
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "db"))
    import policy as _pol                                              # noqa: E402
    _stamp = _pol.require_open(_a.segment, override=_a.policy_override)
    _pol_state = _pol.policy_for_file(_a.segment)
    # ⛔ BI-4 Q5 — 파일 게이트는 "이 파일이 닫혔나" 만 안다. 이 도구가 **무엇을 만드는지**
    #   (Ea · D · σ)를 알고 있으므로 **축 단위 금지**도 claim 이름으로 직접 묻는다.
    #   그래야 레지스트리에 없는 파생량(`MD_D_cm2s@b2o3` 등)도 걸린다.
    _sys = pathlib.Path(str(_a.segment)).name.split("_")[0]
    _axis_hits = []
    for _m in ("MD_Ea_eV", "MD_D_cm2s", "MD_sigma_mScm"):
        for _h in _pol.axis_blocked(f"{_m}@{_sys}"):
            if _h not in _axis_hits:
                _axis_hits.append(_h)
    if _axis_hits:
        print(f"  ⛔ 축 단위 금지가 이 계({_sys})의 D·Ea·σ 를 덮는다: "
              + " / ".join(f"{h.get('id')}({h.get('level')})" for h in _axis_hits),
              file=sys.stderr)
    _r = run_segment(_a.segment, _a.T_lo, _a.T_hi, _a.T_out, _a.n_li)
    # ⛔⛔ BI-4 P1 — 종전 반환값에는 **숫자만** 있었다. 스탬프는 화면에만 찍히고
    #   json 을 읽는 쪽은 이 값이 인용 가능한지 알 방법이 없었다. 정책을 값과 같이 낸다.
    _r["citable"] = (_pol_state["state"] == "open") and not _axis_hits
    _r["policy"] = {"state": _pol_state["state"], "why": _pol_state["why"],
                    "target": str(_a.segment),
                    "axis_blocked": _axis_hits,
                    "checked_by": "tools/db/policy.py policy_for_file() + axis_blocked()"}
    if _stamp:
        _r["⛔_POLICY_OVERRIDE"] = _stamp
        print("\n" + "=" * 74 + f"\n {_stamp}\n" + "=" * 74)
    if not _r["citable"]:
        print(f"  ⛔ citable=false — 이 산출물은 인용 금지다 (state={_pol_state['state']}).")
    if _a.json_out:
        json.dump(_r, open(_a.json_out, "w"), ensure_ascii=False, indent=1)
        print(f"\n  → {_a.json_out}")
    sys.exit(0)

# --- paper-grade fits (db/properties/li_transport.json) + actual MD cells ---
systems = {
    "LPSCl  (Li6PS5Cl, comp1 4fu natural)": dict(
        Ea=0.2532, D0=4.110e-4,      # arrhenius_fit PAPER_GRADE
        n_Li=24, V_A3=1016.62,       # comp1_v3_4fu_natural MD cell
        D600_ref=3.086e-6),
    "LPSCl1.6 (Li5.4PS4.4Cl1.6, modelc 5fu)": dict(
        Ea=0.2234, D0=5.745e-4,      # CSV fit slope/intercept (reproduces stored 1.014e-7)
        n_Li=27, V_A3=1216.38,       # exact V from db/structures/modelc_V0_k663.xyz lattice vectors
        D600_ref=7.90e-6),
}

# atom-count cross-check: composition x Z must equal the MD-cell atom count
_check = {
    "LPSCl  (Li6PS5Cl, comp1 4fu natural)":   (dict(Li=24, P=4, S=20, Cl=4), 52),
    "LPSCl1.6 (Li5.4PS4.4Cl1.6, modelc 5fu)": (dict(Li=27, P=5, S=22, Cl=8), 62),
}
for nm, (comp, ntot) in _check.items():
    assert sum(comp.values()) == ntot, f"{nm}: atoms sum {sum(comp.values())} != {ntot}"
    assert comp["Li"] == systems[nm]["n_Li"], f"{nm}: n_Li mismatch"
print("atom-count check OK:  comp1 24+4+20+4=52 (Z=4) ;  modelc 27+5+22+8=62 (Z=5)\n")

print("=" * 74)
print(" 300 K extrapolation + Nernst-Einstein sigma (H_R = 1, z = +1)")
print("=" * 74)
out = {}
for name, s in systems.items():
    # number density of Li (carriers) in cm^-3
    n = s["n_Li"] / (s["V_A3"] * 1e-24)        # A^3 -> cm^3
    # D extrapolated to 300 K
    D300 = s["D0"] * np.exp(-s["Ea"] / (kB_eV * 300.0))
    # check: reproduce D(600 K) from the fit
    D600 = s["D0"] * np.exp(-s["Ea"] / (kB_eV * 600.0))
    # Nernst-Einstein conductivity (S/cm) at 300 K
    sigma = n * e**2 * D300 / (kB_J * 300.0)
    out[name] = dict(n=n, D300=D300, sigma_mScm=sigma * 1e3)
    print(f"\n  {name}")
    print(f"    n_Li         = {n:.3e} cm^-3   ({s['n_Li']} Li / {s['V_A3']:.1f} A^3)")
    print(f"    fit          : Ea = {s['Ea']:.4f} eV,  D0 = {s['D0']:.3e} cm^2/s")
    print(f"    D(600K) fit  = {D600:.3e} cm^2/s   (ref MD {s['D600_ref']:.2e})")
    print(f"    D(300K) extrap = {D300:.3e} cm^2/s")
    print(f"    sigma_NE(300K) = {sigma*1e3:.2f} mS/cm   ({sigma:.3e} S/cm)")

names = list(out)
r_sig = out[names[1]]["sigma_mScm"] / out[names[0]]["sigma_mScm"]
r_D = out[names[1]]["D300"] / out[names[0]]["D300"]
print("\n" + "-" * 74)
print(f"  RATIO LPSCl1.6 / LPSCl  @300K :  sigma {r_sig:.2f}x   (D {r_D:.2f}x)")
print(f"  (at 600 K the D ratio is {7.90e-6/3.086e-6:.2f}x — gap widens at low T because Ea differs)")
print("-" * 74)
print("\n  experiment (RT): LPSCl ~1-3.2 mS/cm ; LPSCl1.6/Cl-rich ~7-9.9 mS/cm")
print("  NE is right order, ~1.5-2x high: MLIP D-overshoot (~2-5x) + bulk-vs-pellet resistance.")
print("  Haven H_R=1 is the TRACER->charge assumption; real H_R<1 => true intrinsic sigma = sigma_NE/H_R")
print("  is even HIGHER (opposite sign), so H_R does NOT cause the overshoot. Robust: Ea + ratio.")
