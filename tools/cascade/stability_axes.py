#!/usr/bin/env python3
"""stability_axes.py — T9·T10·T11 을 한 번에: 계면 4상대 + hull 합성가능성 + H2S 정량.

셋 다 M6(cathode_reactivity.py)의 기계를 그대로 재사용하므로 묶어서 돈다.
MP 엔트리 캐시를 공유해 추가 쿼리가 거의 없다.

축 3개
------
**T9 계면 반응성 4상대** — 우리 M6 초판은 양극만 봤다. 문헌 실물이 그게 쉬운 쪽임을 보였다:
  · Kim 2026 (Nano Convergence 13, 27) Table S1 — 산화물 다수가 NCM523 과는 dE_rxn = 0 인데
    LPSCl 과는 -50 ~ -99 meV/atom (Li2TiO3 0/-60 · Li3NbO4 0/-96 · Li2SO4 0/-99 · LiSrBO3 0/-96).
    본문: "many materials exhibited stable interfaces with the NCM523, a substantial fraction
    fail to maintain stability against LPSC".
  · Lee 2024 (JMCA 12, 7272) Table S3 — Li6PS5I 가 LNO -107.55 / NCM811 -424.46 / **Li -539.24 meV**.
    **Li 음극 쪽이 가장 가혹하다.**
  → 상대 = {양극 만충·반충, SE(LPSCl), Li 음극, 기존 코팅(LiNbO3)}

**T10 E_hull 합성가능성** — Lee 2024 Table 1 이 `E_hull < 50 meV/atom` 을 합성가능성 기술자로 쓴다.
  우리 cascade G1 은 hull 이 아니라 **host 상대 Δe** 라 아무도 못 떨어뜨린다(unique_kill 0, vacuous).
  근본 원인이 이것이므로 hull 축을 따로 세운다.
  ⚠ 이건 **코팅 화합물 자체의 hull** 이지 "LPSCl 에 도핑했을 때"의 hull 이 아니다 — 다른 질문이다.

**T11 pseudo-binary dE_H2S** — Lee 2024 ESI eq S9-S10: SSE + H2O 를 pseudo-binary 로 섞어
  가수분해 반응에너지를 구한다. M6 와 **완전히 같은 기계**(닫힌계 InterfacialReactivity)라 비용 0.
  우리 `air_hsab` 정성 tier 를 정량으로 바꾼다.
  ⚠ 이건 **열역학 구동력**이지 반응 속도가 아니고, 이상욱 랩의 반응 MD(SevenNet, 500 ps)와
    같은 것이 아니다. "H2S 가 나올 수 있는가"까지만 말한다.

실행
----
  python3 tools/cascade/stability_axes.py --targets           # 앵커 재현 검증만
  python3 tools/cascade/stability_axes.py --run               # 47종 전수
"""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cathode_reactivity import (  # noqa: E402  — M6 기계 재사용
    _find_api_key, _phase_diagram, min_rxn_closed, load_dopants, GATE_MEV,
)

# 계면 상대 4종 (T9). label:composition
COUNTERPARTS = [
    ("LCO_full", "LiCoO2",      "양극 만충 — Xiao F4 원형"),
    ("LCO_half", "Li0.5CoO2",   "양극 반충 — 탈리튬 상태"),
    ("LPSCl",    "Li6PS5Cl",    "고체전해질 — Kim 2026: 구속을 거는 쪽"),
    ("Li_metal", "Li",          "Li 음극 — Lee 2024: 가장 가혹(-539 meV)"),
    ("LNO",      "LiNbO3",      "기존 상용 코팅 — 대조군"),
]

# 문헌 앵커 (소환값 — 우리 값과 혼합 금지). Lee 2024 Table S3, Li6PS5I 기준.
LEE2024_LI6PS5I_ANCHOR = {"LNO": -107.55, "NCM811": -424.46, "Li_metal": -539.24}
HULL_GATE_MEV = 50.0            # Lee 2024 Table 1 합성가능성 기술자


def scan_pair(a, b, cache_dir):
    """닫힌계 pseudo-binary. 반환 (meV, rxn) 또는 (None, 'ERR ...')."""
    from pymatgen.core import Composition, Element
    elems = set(Composition(a).elements) | set(Composition(b).elements)
    elems.add(Element("Li"))
    try:
        pd = _phase_diagram([e.symbol for e in elems], cache_dir)
        return min_rxn_closed(Composition(a), Composition(b), pd)
    except Exception as ex:
        return (None, f"ERR {type(ex).__name__}: {ex}")


def hull_of(comp_str, cache_dir):
    """코팅 화합물 자체의 E_above_hull (meV/atom). MP 엔트리에서 직접.

    같은 조성의 엔트리 중 **가장 낮은** e_above_hull 을 쓴다(안정 다형 기준).
    엔트리가 없으면 None — 추측하지 않는다."""
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    c = Composition(comp_str)
    elems = {e.symbol for e in c.elements} | {"Li"}
    pd = _phase_diagram(sorted(elems), cache_dir)
    best = None
    for e in pd.all_entries:
        if e.composition.reduced_formula != c.reduced_formula:
            continue
        h = pd.get_e_above_hull(e) * 1000.0
        best = h if best is None else min(best, h)
    return best


def hydrolysis(comp_str, cache_dir):
    """T11: 화합물 + H2O pseudo-binary (Lee 2024 eq S9-S10). 반환 (meV, rxn)."""
    return scan_pair(comp_str, "H2O", cache_dir)


def targets(cache_dir):
    """앵커 재현 — LPSCl(우리 host)을 문헌 앵커와 대조해 기계가 맞는지 확인."""
    print("=" * 76)
    print("앵커 재현: Li6PS5Cl vs 상대 4종  (문헌 앵커는 Lee 2024 의 Li6PS5**I** — 조성이 달라")
    print("           정량 일치가 아니라 **부호·크기 순서**만 본다)")
    print("=" * 76)
    got = {}
    for lab, comp, note in COUNTERPARTS:
        if comp == "Li6PS5Cl":
            print(f"  {lab:10s} {comp:12s}  (자기 자신 — 생략)")
            continue
        mev, rxn = scan_pair("Li6PS5Cl", comp, cache_dir)
        got[lab] = mev
        if mev is None:
            print(f"  {lab:10s} 실패: {rxn}")
            continue
        anc = LEE2024_LI6PS5I_ANCHOR.get(lab)
        atxt = f"   [Lee2024 Li6PS5I {anc:+.1f}]" if anc is not None else ""
        print(f"  {lab:10s} {mev:9.1f} meV/atom{atxt}   {rxn[:52]}")
        print(f"             ({note})")

    print("\n  ── 크기 순서 판정 ──")
    order = [(k, v) for k, v in got.items() if v is not None]
    order.sort(key=lambda kv: kv[1])
    print("   " + "  <  ".join(f"{k}({v:.0f})" for k, v in order))
    lit_order = ["Li_metal", "NCM811(우리는 LCO)", "LNO"]
    print(f"   문헌(Lee 2024, Li6PS5I) 순서: {' < '.join(lit_order)}")
    ok = bool(order) and order[0][0] == "Li_metal"
    print(f"   → Li 음극이 가장 가혹한가: {'OK' if ok else '⚠ 아님 — 확인 필요'}")
    print("=" * 76)
    return ok


def run_all(cache_dir, out_csv):
    dopants = load_dopants()
    cps = [(l, c) for l, c, _ in COUNTERPARTS]
    print(f"코팅 {len(dopants)}종 × [계면 {len(cps)}상대 + hull + H2S]")

    done = set()
    if Path(out_csv).exists():
        with open(out_csv) as f:
            for r in csv.DictReader(l for l in f if not l.startswith("#")):
                done.add(r["coating"])
        print(f"  기존 {len(done)}종 — skip")

    cols = (["coating", "e_above_hull_meV", "synthesizable_50meV",
             "dE_H2S_meV", "H2S_reaction"]
            + [f"dE_{l}_meV" for l, _ in cps]
            + [f"rxn_{l}" for l, _ in cps])
    exists = Path(out_csv).exists()
    n = 0
    with open(out_csv, "a" if exists else "w") as f:
        if not exists:
            f.write("# cascade 코팅 후보 안정성 3축 (T9 계면4상대 / T10 hull / T11 H2S).\n")
            f.write("# 전부 닫힌계 pseudo-binary (Richards/Ong 2016 eq 2), MP GGA_GGA+U.\n")
            f.write(f"# hull 게이트 {HULL_GATE_MEV:.0f} meV/atom = Lee 2024 (JMCA 12, 7272) Table 1 "
                    "합성가능성 기술자. 계면 게이트는 Xiao 2019 F4 100 meV.\n")
            f.write("# ⛔ dE_H2S 는 열역학 구동력이지 반응 속도가 아니다 — 'H2S 가 나올 수 있는가'까지만.\n")
            f.write("# ⛔ 문헌 앵커(Lee 2024 Li6PS5I: LNO -107.55 / NCM811 -424.46 / Li -539.24)는 "
                    "소환값 — 우리 값과 혼합 금지.\n")
        w = csv.DictWriter(f, fieldnames=cols)
        if not exists:
            w.writeheader()
        for i, d in enumerate(dopants, 1):
            if d in done:
                print(f"[{i}/{len(dopants)}] {d}: skip")
                continue
            print(f"[{i}/{len(dopants)}] {d}")
            row = {"coating": d}
            try:
                h = hull_of(d, cache_dir)
            except Exception as ex:
                print(f"    hull ERR {type(ex).__name__}: {ex}")
                h = None
            row["e_above_hull_meV"] = "" if h is None else f"{h:.1f}"
            row["synthesizable_50meV"] = "" if h is None else ("Y" if h < HULL_GATE_MEV else "N")

            mev, rxn = hydrolysis(d, cache_dir)
            row["dE_H2S_meV"] = "" if mev is None else f"{mev:.1f}"
            row["H2S_reaction"] = (rxn or "")[:200]

            for lab, comp in cps:
                m, r = scan_pair(d, comp, cache_dir)
                row[f"dE_{lab}_meV"] = "" if m is None else f"{m:.1f}"
                row[f"rxn_{lab}"] = (r or "")[:180]
                if m is not None:
                    print(f"    {lab:10s} {m:9.1f}  {'PASS' if abs(m) < GATE_MEV else 'fail'}")
            print(f"    hull {row['e_above_hull_meV'] or '?':>7s}  "
                  f"H2S {row['dE_H2S_meV'] or '?':>8s}")
            w.writerow(row)
            f.flush()
            n += 1
    print(f"\n→ {out_csv}  (+{n}행)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", action="store_true", help="앵커 재현 검증만")
    ap.add_argument("--run", action="store_true", help="47종 전수")
    ap.add_argument("--force", action="store_true", help="검증 실패해도 강행")
    ap.add_argument("--cache", default=str(Path.home() / ".cache" / "mp_entries"))
    ap.add_argument("--out", default=str(PROP / "cascade_stability_axes.csv"))
    a = ap.parse_args()
    if not (a.targets or a.run):
        ap.error("--targets 또는 --run 필요")
    _find_api_key()
    ok = targets(a.cache)
    if a.run:
        if not ok and not a.force:
            sys.exit("\n앵커 순서가 예상과 다름 — --force 없이는 전수 실행 안 함.")
        run_all(a.cache, a.out)


if __name__ == "__main__":
    main()
