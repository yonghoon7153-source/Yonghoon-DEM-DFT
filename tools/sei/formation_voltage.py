#!/usr/bin/env python3
"""formation_voltage.py — SEI 상이 **몇 V 에서 안정한가**를 대분배(grand-potential)로 낸다.

왜 이 방식인가
  "형성되는 전위" 를 `V = −[E(LiₓX) − E(X) − x·E(Li)]/x` 로 내려면 기준 X 를 골라야 하는데,
  Li₂S ← S, Li₃P ← P 는 자연스럽지만 **Li₃PO₄·LiNdO₂ 는 그런 X 가 없다**. 삼원계는
  단일 리튬화 반응으로 정의되지 않는다.
  → 대신 **Li 화학퍼텐셜 μ_Li 를 훑으며 그 상이 볼록껍질 위에 있는 구간**을 찾는다.
    그 구간의 경계가 곧 "이 전위 아래/위에서 이 상이 나타난다" 이다.
    V(vs Li/Li⁺) = −(μ_Li − μ_Li⁰)/e   (μ_Li⁰ = Li 금속)
  이건 우리 cascade 의 산화 ESW 와 같은 틀이고(grand-potential), 문헌 표준이다.

⚠ 에너지는 **Materials Project(PBE/PBE+U, MP 보정 적용)** 값이다. 우리 QE 계산과 섞지 말 것.
  한 데이터베이스 안에서 일관되므로 상들 사이 비교에는 유효하다.

  export MP_API_KEY=...
  python3 tools/sei/formation_voltage.py
  python3 tools/sei/formation_voltage.py --dv 0.02      # 더 촘촘히
"""
import argparse
import json
import os
import sys

OUT = "db/properties/sei_formation_voltage.json"
PROV = "db/properties/sei_structures_provenance.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vmax", type=float, default=5.0, help="훑을 최대 전위 [V vs Li/Li+]")
    ap.add_argument("--dv", type=float, default=0.05, help="전위 격자 [V]")
    a = ap.parse_args()

    if not os.environ.get("MP_API_KEY"):
        sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...")
    if not os.path.isfile(PROV):
        sys.exit(f"⛔ {PROV} 가 없다 — fetch_sei_structures.py --get 을 먼저 돌릴 것")

    import numpy as np
    from mp_api.client import MPRester
    from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram
    from pymatgen.core import Composition, Element

    prov = json.load(open(PROV))
    res = {}
    with MPRester(os.environ["MP_API_KEY"]) as mpr:
        for name, p in prov.items():
            mid = p["material_id"]
            comp = Composition(name.rstrip("bg") if name.startswith("Li3PO4") else name)
            els = sorted({str(e) for e in comp.elements} | {"Li"})
            print(f"\n═══ {name}  ({mid}) · 화학계 {'-'.join(els)} ═══")
            if "Li" not in [str(e) for e in comp.elements]:
                print("  ⏭  Li 를 안 가진 상이다 — 'Li 형성 전위' 가 정의되지 않는다.")
                print("     (Nd₂O₃·Nd₂S₃ 는 Li 저장상이 아니라 골격/부산물이다.)")
                res[name] = {"status": "skipped", "reason": "no Li in phase"}
                continue

            # ⚠⚠ thermo_type 을 **고정**한다 (2026-08-06). MP 기본이 GGA_GGA+U 에서
            #   GGA_GGA+U_R2SCAN 혼합 껍질로 바뀌었는데, 섞인 껍질에서 E_hull 이
            #   터무니없이 나왔다(실측: Li2S 0.1139, LiNdO2 **3.8787** eV/atom —
            #   MP 페이지의 0.008 과 완전히 다르다). 한 종류로 통일해야 껍질이 성립한다.
            entries = mpr.get_entries_in_chemsys(
                els, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
            pd = PhaseDiagram(entries)
            # ⚠ `mid in str(entry_id)` 는 **부분문자열 매칭**이라 mp-1153 이 mp-11530 에도
            #   걸린다. material_id 로 정확히 맞춘다.
            def _mid(e):
                # ⚠ `.get(k, "") ` 는 **키가 있고 값이 None 이면 None 을 준다**(기본값이 아니라).
                #   그러면 str(None) == "None" 이 truthy 라 모든 엔트리가 "None" 이 됐다
                #   (2026-08-06: 전 항목에서 "mp-XXXX 를 못 찾았다" 가 뜬 원인).
                raw = (getattr(e, "data", None) or {}).get("material_id")
                if raw:
                    return str(raw)
                return str(e.entry_id).split("-GGA")[0].split("-R2SCAN")[0]
            tgt = [e for e in entries if _mid(e) == mid]
            if not tgt:
                print(f"  ⚠ {mid} 를 엔트리에서 못 찾았다 — 같은 조성의 최저 엔트리로 대체")
                tgt = sorted([e for e in entries
                              if e.composition.reduced_formula == comp.reduced_formula],
                             key=lambda e: pd.get_e_above_hull(e))
            if not tgt:
                print(f"  ⛔ {mid} 를 화학계 엔트리에서 못 찾았다")
                res[name] = {"status": "failed", "reason": "entry not found"}
                continue
            t = tgt[0]
            ehull = pd.get_e_above_hull(t)

            mu0 = pd.el_refs[Element("Li")].energy_per_atom
            vs, stable = np.arange(0.0, a.vmax + 1e-9, a.dv), []
            for v in vs:
                # V vs Li/Li+ 가 높을수록 μ_Li 가 낮다 (탈리튬 쪽)
                gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu0 - v})
                names = {e.original_entry.composition.reduced_formula
                         for e in gpd.stable_entries}
                stable.append(comp.reduced_formula in names)
            stable = np.array(stable)
            if not stable.any():
                print(f"  ⚠ 0–{a.vmax} V 어디서도 껍질 위에 없다 "
                      f"(E_hull {ehull:.4f} eV/atom) — 준안정상이다.")
                res[name] = {"status": "never_stable", "e_above_hull": float(ehull),
                             "material_id": mid}
                continue
            # ⚠ min/max 만 쓰면 구간이 끊겨 있어도 하나로 뭉뚱그려진다 — 연속 구간별로 낸다
            segs, i = [], 0
            while i < len(stable):
                if stable[i]:
                    j = i
                    while j + 1 < len(stable) and stable[j + 1]:
                        j += 1
                    segs.append((float(vs[i]), float(vs[j])))
                    i = j + 1
                else:
                    i += 1
            lo, hi = segs[0][0], segs[-1][1]
            txt = " , ".join(f"{x:.2f}–{y:.2f}" for x, y in segs)
            print(f"  안정 구간 **{txt} V** vs Li/Li⁺   (E_hull {ehull:.4f} eV/atom)")
            print(f"  → **{hi:.2f} V 이하 전 구간에서 안정** (Li 금속 전위까지 버틴다)"
                  if lo <= 1e-9 and len(segs) == 1 else
                  f"  → {hi:.2f} V 이하로 내려가면 나타나고, {lo:.2f} V 아래에서는 "
                  f"더 환원된 상으로 넘어간다")
            res[name] = {"status": "ok", "material_id": mid,
                         "stable_segments_V": segs,
                         "stable_V_min": lo, "stable_V_max": hi,
                         "e_above_hull_eV_per_atom": float(ehull),
                         "chemsys": "-".join(els)}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({
        "property": "sei_formation_voltage",
        "method": ("Grand-potential phase diagram (pymatgen) over Materials Project entries "
                   "(**thermo_types=GGA_GGA+U 로 고정** — 혼합 R2SCAN 껍질에서 E_hull 이 "
                   "터무니없이 나왔다). "
                   "μ_Li 를 훑으며 그 상이 볼록껍질 위에 있는 전위 구간을 찾는다. "
                   "V(vs Li/Li+) = −(μ_Li − μ_Li⁰)/e."),
        "warning": ("에너지는 **MP(PBE/PBE+U, MP 보정)** 값이다 — 우리 QE 계산과 섞지 말 것. "
                    "한 데이터베이스 안에서 일관되므로 상들 사이 비교에만 쓴다."),
        "grid_V": a.dv, "vmax_V": a.vmax, "results": res,
    }, open(OUT, "w"), ensure_ascii=False, indent=2)

    print("\n" + "═" * 68)
    print(f"{'상':14s} {'안정 구간 (V vs Li/Li+)':>26s} {'E_hull':>10s}")
    for k, v in res.items():
        if v.get("status") == "ok":
            print(f"{k:14s} {v['stable_V_min']:10.2f} – {v['stable_V_max']:<10.2f} "
                  f"{v['e_above_hull_eV_per_atom']:10.4f}")
        else:
            print(f"{k:14s} {v.get('status'):>26s} "
                  f"{v.get('e_above_hull', float('nan')):10.4f}")
    print(f"\n→ {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
