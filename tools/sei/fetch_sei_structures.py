#!/usr/bin/env python3
"""fetch_sei_structures.py — SEI 분해상 구조를 MP 에서 **다형체를 눈으로 고른 뒤** 받는다.

왜 자동 선택을 안 하나 (2026-08-06)
  `energy_above_hull` 최솟값으로 자동 선택했더니 이렇게 나왔다:
      LiCl    → P6_3mc   (우르차이트형)   ← LiCl 은 **암염(Fm-3m)** 이 정답이다
      LiNdO2  → P2_1/c                     ← 통상 보고는 α-NaFeO2형 계열
      Li3PO4  → Pmn2_1 (β)                 ← γ(Pnma)가 통상 안정상
  e_above_hull 이 0 으로 동률이면 정렬이 임의로 고르고, **MP 에는 실험 미확인 예측
  구조가 많이 섞여 있다**(`theoretical=True`).
  ⚠ 다형체가 틀리면 **Li 확산장벽이 통째로 달라진다** — 캠페인 전체가 무의미해진다.

  그래서 이 도구는 **먼저 후보를 전부 보여 주고**(--list), 사람이 mp-id 를 확정한 뒤
  받는다(--get). 받은 구조에는 mp-id·공간군·e_hull·theoretical 을 출처로 기록한다.

  export MP_API_KEY=...                       # ⚠ 파일에 넣지 말 것
  python3 tools/sei/fetch_sei_structures.py --list
  python3 tools/sei/fetch_sei_structures.py --get Li2O=mp-1960 LiCl=mp-22905 ...
"""
import argparse
import json
import os
import sys
from datetime import datetime

FORMULAS = ["Li2O", "Li2S", "LiCl", "Li3P", "Li3PO4", "LiNdO2"]
OUTDIR = "db/structures"
PROV = "db/properties/sei_structures_provenance.json"


def rester():
    if not os.environ.get("MP_API_KEY"):
        sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...  (⚠ 파일에 넣지 말 것)")
    from mp_api.client import MPRester
    return MPRester(os.environ["MP_API_KEY"])


def do_list(formulas):
    fields = ["material_id", "formula_pretty", "symmetry", "energy_above_hull",
              "theoretical", "nsites", "density"]
    with rester() as m:
        for f in formulas:
            print(f"\n═══ {f} ═══")
            docs = m.materials.summary.search(formula=f, fields=fields)
            if not docs:
                print("  (MP 에 없음)"); continue
            docs = sorted(docs, key=lambda d: (d.energy_above_hull or 9e9))
            print(f"  {'mp-id':16s} {'공간군':12s} {'E_hull':>9s} {'원자':>5s}  실험확인")
            for d in docs[:8]:
                exp = "✅ 관측" if not d.theoretical else "⚠ 예측만"
                print(f"  {d.material_id:16s} {d.symmetry.symbol:12s} "
                      f"{d.energy_above_hull:9.4f} {d.nsites:5d}  {exp}")
            obs = [d for d in docs if not d.theoretical]
            if obs:
                b = obs[0]
                print(f"  → **실험 관측 중 최저**: {b.material_id} ({b.symmetry.symbol}, "
                      f"E_hull {b.energy_above_hull:.4f})   ← 기본 권장")
            else:
                print("  ⚠ 실험 관측 구조가 하나도 없다 — 이 상은 예측 구조뿐이다. "
                      "논문에 그 사실을 밝힐 것.")
    print("\n⚠ 고른 뒤:  python3 tools/sei/fetch_sei_structures.py --get "
          "Li2O=mp-XXXX LiCl=mp-XXXX ...")


def do_get(pairs):
    from pymatgen.io.ase import AseAtomsAdaptor
    from ase.io import write
    os.makedirs(OUTDIR, exist_ok=True)
    prov = json.load(open(PROV)) if os.path.isfile(PROV) else {}
    fields = ["material_id", "formula_pretty", "symmetry", "energy_above_hull",
              "theoretical", "nsites"]
    with rester() as m:
        for f, mid in pairs:
            d = m.materials.summary.search(material_ids=[mid], fields=fields)
            if not d:
                print(f"⛔ {mid} 를 못 찾았다"); continue
            d = d[0]
            st = m.get_structure_by_material_id(mid)
            at = AseAtomsAdaptor.get_atoms(st)
            base = f"sei_{f.lower()}_{mid}"
            write(os.path.join(OUTDIR, base + ".vasp"), at, format="vasp", direct=True)
            write(os.path.join(OUTDIR, base + ".cif"), at)
            prov[f] = {
                "material_id": mid, "spacegroup": d.symmetry.symbol,
                "energy_above_hull_eV_per_atom": d.energy_above_hull,
                "theoretical": bool(d.theoretical), "nsites": d.nsites,
                "files": [f"{OUTDIR}/{base}.vasp", f"{OUTDIR}/{base}.cif"],
                "source": "Materials Project (mp_api)", "fetched": datetime.now().strftime("%Y-%m-%d"),
            }
            flag = "⚠ 예측만" if d.theoretical else "✅ 관측"
            print(f"✓ {f:8s} {mid:14s} {d.symmetry.symbol:12s} {d.nsites:3d}원자 "
                  f"E_hull {d.energy_above_hull:.4f}  {flag}")
    os.makedirs(os.path.dirname(PROV), exist_ok=True)
    json.dump(prov, open(PROV, "w"), ensure_ascii=False, indent=2)
    print(f"\n출처 기록 → {PROV}")
    print("⚠ 논문·발표에 이 표(mp-id·공간군·실험확인 여부)를 그대로 실을 것.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="다형체 후보를 전부 보여 준다")
    ap.add_argument("--get", nargs="*", metavar="화학식=mp-id",
                    help="확정한 것만 받는다 (예: LiCl=mp-22905)")
    ap.add_argument("--formulas", nargs="*", default=FORMULAS)
    a = ap.parse_args()
    if a.get:
        do_get([tuple(x.split("=", 1)) for x in a.get])
    else:
        do_list(a.formulas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
