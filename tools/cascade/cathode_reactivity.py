#!/usr/bin/env python3
"""cathode_reactivity.py — cascade 도펀트 × 양극 계면 반응성 게이트 (open_items M6).

문헌 근거
---------
Richards/Ong 2016 (Chem. Mater. 28, 266) pseudo-binary: 두 상의 혼합 분율 x에 대해
반응에너지를 최소화. 전위 하에서는 grand potential(Li 저장소 개방), mu_Li = mu_Li(metal) - V.
Xiao/Ceder 2019 (Joule 3, 1252) F4 게이트: |dE_rxt| < 100 meV/atom (vs Li3PS4 및 만충 양극)을
통과해야 코팅 후보. 우리 cascade에 없던 마지막 축(litdb/papers/xiao2019_cathode_coating_screening.md).

기계는 tools/oxidation/interface_reactivity_v2.py 와 동일(GrandPotentialInterfacialReactivity,
use_hull_energy=True, MP GGA_GGA+U). 이 스크립트는 그것을 **47 도펀트 × 양극**으로 돌리는 래퍼 +
문헌 정답지 검증 게이트다.

2단 구조
--------
  1) --validate : LPSCl(우리 host) vs 양극만 먼저 계산 → Xiao 소환값과 대조.
     기대 앵커(xiao2019 digest): LPSCl/LCO -339(만충)/-493(반충), LPSCl/NCM -330/-471 meV/atom.
     ⚠ Xiao의 "만충/반충"이 어느 전위에 대응하는지는 digest에 명시가 없다. 따라서 이 단계의 판정은
     "자릿수·부호·순서(반충이 더 발열)가 재현되는가"이지 소수점 일치가 아니다. 불일치 시 원인
     후보를 출력하고 **생산 실행을 막는다**(--force 로만 우회).
  2) (검증 통과 후) --run : 47 도펀트 전수 → db/properties/cathode_reactivity_cascade.csv

비용 주의
--------
도펀트마다 chemsys가 달라 MP 쿼리가 도펀트당 1회. LCO(=Li-Co-O + 도펀트원소)는 4~5원소라 가볍고,
NCM811(Li-Ni-Co-Mn-O + 도펀트)은 6~7원소라 PhaseDiagram 구성이 급격히 비싸진다. 기본은 LCO,
NCM은 --cathodes 로 명시할 때만. 엔트리는 --cache 디렉터리에 저장되어 재실행 시 재사용된다.

실행 (gabia/kgy, MP_API_KEY 설정된 셸)
  python3 tools/cascade/cathode_reactivity.py --validate
  python3 tools/cascade/cathode_reactivity.py --run
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"

# Xiao 2019 소환값 (meV/atom) — 우리 계산값과 절대 혼합 금지, 검증 대조용
XIAO_ANCHOR = {
    ("LPSCl", "LCO"): {"charged": -339, "half": -493},
    ("LPSCl", "NCM"): {"charged": -330, "half": -471},
}
GATE_MEV = 100.0          # Xiao F4: |dE_rxt| < 100 meV/atom
DEFAULT_V = [3.0, 3.9, 4.3]   # 반충~만충 구간 (LCO 3.9 V 라인 = Xiao 본문 기준선)


# ── MP 엔트리 (캐시) ────────────────────────────────────────────
def get_entries(elements, cache_dir):
    key = "-".join(sorted(elements))
    cp = Path(cache_dir) / f"{key}.json"
    if cp.exists():
        from monty.json import MontyDecoder
        entries = json.loads(cp.read_text(), cls=MontyDecoder)
        print(f"[cache] {len(entries):5d} entries  {key}")
        return entries
    api = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not api:
        sys.exit("MP_API_KEY(또는 PMG_MAPI_KEY) 환경변수가 없습니다.")
    from mp_api.client import MPRester
    with MPRester(api) as mpr:
        entries = mpr.get_entries_in_chemsys(
            sorted(elements), additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    cp.parent.mkdir(parents=True, exist_ok=True)
    from monty.json import MontyEncoder
    cp.write_text(json.dumps(entries, cls=MontyEncoder))
    print(f"[mp_api] {len(entries):5d} entries  {key}  → cached")
    return entries


def li_metal_mu(entries):
    es = [e.energy_per_atom for e in entries
          if e.composition.reduced_formula == "Li"]
    if not es:
        sys.exit("Li metal 엔트리를 못 찾음 — chemsys에 Li가 빠졌나 확인")
    return min(es)


def min_rxn(c_coat, c_cath, gpd, pd):
    """Richards eq 3-4: 혼합 분율 x 최소화. 반환 (meV/atom, 반응식)."""
    from pymatgen.analysis.interface_reactions import GrandPotentialInterfacialReactivity
    gir = GrandPotentialInterfacialReactivity(
        c_coat, c_cath, gpd, pd_non_grand=pd,
        include_no_mixing_energy=True, use_hull_energy=True)
    best_e, best_rxn = 1e9, None
    for k in gir.get_kinks():
        e = float(k[2])
        if e < best_e:
            best_e, best_rxn = e, str(k[3])
    return best_e * 1000.0, best_rxn      # eV/atom → meV/atom


def scan(coat_str, cath_str, voltages, cache_dir):
    """한 (코팅, 양극) 쌍을 전위 스캔. 반환 {V: (meV, rxn)}."""
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram
    elems = set(Composition(coat_str).elements) | set(Composition(cath_str).elements)
    elems.add(Element("Li"))
    entries = get_entries([e.symbol for e in elems], cache_dir)
    pd = PhaseDiagram(entries)
    mu0 = li_metal_mu(entries)
    c1, c2 = Composition(coat_str), Composition(cath_str)
    out = {}
    for V in voltages:
        gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu0 - V})
        try:
            out[V] = min_rxn(c1, c2, gpd, pd)
        except Exception as ex:
            out[V] = (None, f"ERR {type(ex).__name__}: {ex}")
    return out


# ── 1단계: 문헌 정답지 검증 ────────────────────────────────────
def validate(cathodes, voltages, cache_dir):
    print("=" * 72)
    print("검증: LPSCl vs 양극 — Xiao 2019 소환값과 대조")
    print("  ⚠ 판정 기준은 '자릿수·부호·순서'이지 소수점 일치가 아님 (digest에 SOC↔전위 대응 미명시)")
    print("=" * 72)
    ok = True
    for cstr, clab in cathodes:
        res = scan("Li6PS5Cl", cstr, voltages, cache_dir)
        anchor = XIAO_ANCHOR.get(("LPSCl", clab))
        print(f"\n## LPSCl | {clab} ({cstr})")
        vals = []
        for V in voltages:
            mev, rxn = res[V]
            if mev is None:
                print(f"  V={V:.2f}  실패: {rxn}"); ok = False; continue
            vals.append(mev)
            print(f"  V={V:.2f}  {mev:9.1f} meV/atom   {rxn[:78]}")
        if anchor:
            print(f"  [Xiao 소환값] 만충 {anchor['charged']} / 반충 {anchor['half']} meV/atom")
            if vals:
                lo, hi = min(vals), max(vals)
                band = (-700 <= lo <= -150)
                mono = vals == sorted(vals, reverse=True)  # V↑ → 더 발열(더 음수)
                print(f"  → 우리 범위 [{lo:.0f}, {hi:.0f}]  "
                      f"자릿수대 {'OK' if band else '⚠ 벗어남'} · "
                      f"전위 단조성 {'OK' if mono else '⚠ 비단조'}")
                if not band:
                    ok = False
        else:
            print("  (이 양극은 소환 앵커 없음 — 참고 출력만)")
    print("\n" + "=" * 72)
    print("검증 " + ("통과 — --run 진행 가능" if ok else "실패 — 원인 확인 전 --run 금지"))
    if not ok:
        print("  원인 후보: (a) MP hull 세대 차 (Xiao 2019 당시 DB vs 현재)")
        print("             (b) SOC↔전위 대응 가정 불일치 (Xiao는 조성 기반일 수 있음)")
        print("             (c) NCM 대리조성(LiNi0.8Co0.1Mn0.1O2) 차이")
        print("             (d) use_hull_energy/include_no_mixing_energy 옵션 차")
    print("=" * 72)
    return ok


# ── 2단계: 47 도펀트 전수 ──────────────────────────────────────
def load_dopants():
    p = PROP / "cascade_v23_ranked.csv"
    with open(p) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    return [r["dopant"] for r in rows]


def run_all(cathodes, voltages, cache_dir, out_csv):
    dopants = load_dopants()
    print(f"도펀트 {len(dopants)}종 × 양극 {len(cathodes)}종 × 전위 {len(voltages)}점")
    done = {}
    if Path(out_csv).exists():          # resume-safe
        with open(out_csv) as f:
            for r in csv.DictReader(l for l in f if not l.startswith("#")):
                done[(r["dopant"], r["cathode"], r["V_vs_Li"])] = True
        print(f"  기존 {len(done)}행 — 완료분 skip")
    newrows = []
    for i, d in enumerate(dopants, 1):
        for cstr, clab in cathodes:
            if all((d, clab, f"{V:.2f}") in done for V in voltages):
                print(f"[{i}/{len(dopants)}] {d} | {clab}: skip"); continue
            print(f"[{i}/{len(dopants)}] {d} | {clab}")
            try:
                res = scan(d, cstr, voltages, cache_dir)
            except Exception as ex:
                print(f"    ERR {type(ex).__name__}: {ex}"); continue
            for V in voltages:
                mev, rxn = res[V]
                newrows.append({
                    "dopant": d, "cathode": clab, "cathode_composition": cstr,
                    "V_vs_Li": f"{V:.2f}",
                    "dE_rxt_meV_per_atom": ("" if mev is None else f"{mev:.1f}"),
                    "gate_pass_100meV": ("" if mev is None else
                                         ("Y" if abs(mev) < GATE_MEV else "N")),
                    "reaction": (rxn or "")[:200],
                })
                if mev is not None:
                    print(f"    V={V:.2f}  {mev:9.1f} meV/atom  "
                          f"{'PASS' if abs(mev) < GATE_MEV else 'fail'}")
    if not newrows:
        print("새로 계산된 행 없음"); return
    cols = ["dopant", "cathode", "cathode_composition", "V_vs_Li",
            "dE_rxt_meV_per_atom", "gate_pass_100meV", "reaction"]
    exists = Path(out_csv).exists()
    with open(out_csv, "a" if exists else "w") as f:
        if not exists:
            f.write("# cascade 도펀트 x 양극 계면 반응성 (open_items M6). "
                    "GrandPotentialInterfacialReactivity (Richards/Ong 2016), "
                    "mu_Li = mu_Li(metal) - V, use_hull_energy=True, MP GGA_GGA+U.\n")
            f.write(f"# 게이트: |dE_rxt| < {GATE_MEV:.0f} meV/atom (Xiao 2019 F4). "
                    "더 음수 = 더 반응성 = 코팅으로 부적합. "
                    "Xiao 소환값(LPSCl/LCO -339/-493)은 문헌값 — 우리 값과 혼합 금지.\n")
        w = csv.DictWriter(f, fieldnames=cols)
        if not exists:
            w.writeheader()
        w.writerows(newrows)
    print(f"\n→ {out_csv}  (+{len(newrows)}행)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true", help="LPSCl 정답지 검증만")
    ap.add_argument("--run", action="store_true", help="47 도펀트 전수 (검증 통과 후)")
    ap.add_argument("--force", action="store_true", help="검증 실패해도 강행")
    ap.add_argument("--cathodes", nargs="+", default=["LiCoO2:LCO"],
                    help='comp:label. NCM은 원소 수가 많아 비쌈 — 예 "LiNi0.8Co0.1Mn0.1O2:NCM"')
    ap.add_argument("--voltages", nargs="+", type=float, default=DEFAULT_V)
    ap.add_argument("--cache", default=str(Path.home() / ".cache" / "mp_entries"))
    ap.add_argument("--out", default=str(PROP / "cathode_reactivity_cascade.csv"))
    a = ap.parse_args()

    cathodes = []
    for c in a.cathodes:
        cs, _, cl = c.partition(":")
        cathodes.append((cs, cl or cs))

    if not (a.validate or a.run):
        ap.error("--validate 또는 --run 중 하나는 필요")
    ok = True
    if a.validate or a.run:
        ok = validate(cathodes, a.voltages, a.cache)
    if a.run:
        if not ok and not a.force:
            sys.exit("\n검증 실패 — --force 없이는 전수 실행하지 않습니다.")
        run_all(cathodes, a.voltages, a.cache, a.out)


if __name__ == "__main__":
    main()
