#!/usr/bin/env python3
"""li_nd_alloy_check.py — "Li–Nd 합금이 음극 계면에 생긴다"는 주장을 열역학으로 판정한다.

배경 (2026-08-11)
  Xu 2026 (Nano Energy) 는 Nd–O 공도핑 argyrodite 의 음극 계면에 **Li–Nd alloy** 가 생겨
  이온전도·전자절연 계면을 만든다고 주장한다. 근거는 XPS 995 eV 소피크 하나이고
  본문이 스스로 "plausible" 이라고 적었다.

무엇을 묻나 — 세 가지를 분리한다
  ① Li–Nd **이원계**에 껍질 위(hull) 안정상이 존재하나?
  ② 존재하지 않는다면, 얼마나 멀리 떨어져 있나(최소 hull 거리)? 준안정도 없나?
  ③ 음극 조건(μ_Li = Li 금속, 즉 0 V)에서 Li–Nd–S–P–Cl–O 계의 볼록껍질에
     Li–Nd 이원상이 **등장하나**? — 실제 계면 조건은 이원계가 아니다.

⚠ 이 도구는 판정을 **대조군과 함께** 낸다. Li–Al·Li–Si(합금 확실) · Li–La·Li–Ce(같은
  경희토류) 를 같이 조회해, "쿼리가 안 돌아서 0개" 와 "정말 없어서 0개" 를 구분한다.
  대조군에서도 0 이 나오면 그건 판정이 아니라 도구 고장이다.

⚠ MP(GGA/GGA+U) 에너지다. 우리 QE 값과 섞지 말 것. 상들 사이 비교에만 쓴다.
⚠ 이 환경(원격 세션)에서는 MP API 가 프록시에 막힌다 — **gabia 에서 실행**할 것.

  export MP_API_KEY=...
  python3 tools/sei/li_nd_alloy_check.py
"""
import argparse
import json
import os
import sys

OUT = "db/properties/li_nd_alloy_check.json"
#: (계, 왜 대조군인가) — 합금이 확실한 계와 같은 족의 희토류를 섞는다
CONTROLS = [
    ("Li-Al", "합금 확실 (LiAl 등) — 쿼리 건전성 확인"),
    ("Li-Si", "합금 확실 (Li15Si4 등) — 애노드 표준"),
    ("Li-La", "같은 경희토류 — Nd 와 같은 거동을 기대"),
    ("Li-Ce", "같은 경희토류"),
    ("Li-Mg", "고용체계 — 화합물이 적은 쪽 대조"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--interface_chemsys", default="Li-Nd-P-S-Cl-O",
                    help="음극 계면 조건에서 볼 계 (③)")
    ap.add_argument("--skip_interface", action="store_true",
                    help="③ 을 건너뛴다 (6원계 조회는 무거울 수 있다)")
    a = ap.parse_args()

    key = os.environ.get("MP_API_KEY")
    if not key:
        sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...")
    from mp_api.client import MPRester

    res = {"property": "li_nd_alloy_check",
           "question": "Xu 2026 의 'Li–Nd alloy 가 음극 계면에 형성' 주장을 열역학으로 판정",
           "warning": "MP(GGA/GGA+U) 에너지 — 우리 QE 값과 섞지 말 것. "
                      "열역학 판정이지 동역학 판정이 아니다(준안정상은 실제로 생길 수 있다).",
           "binary": {}, "controls": {}, "interface": None}

    with MPRester(key) as m:
        def survey(cs):
            docs = m.materials.summary.search(
                chemsys=cs, fields=["material_id", "formula_pretty", "symmetry",
                                    "energy_above_hull", "formation_energy_per_atom",
                                    "theoretical", "is_stable", "nsites"])
            rows = []
            for d in docs:
                rows.append({
                    "material_id": d.material_id, "formula": d.formula_pretty,
                    "spacegroup": d.symmetry.symbol if d.symmetry else None,
                    "e_above_hull_eV_per_atom": d.energy_above_hull,
                    "formation_energy_eV_per_atom": d.formation_energy_per_atom,
                    "is_stable": d.is_stable, "theoretical": d.theoretical,
                    "nsites": d.nsites})
            rows.sort(key=lambda r: (r["e_above_hull_eV_per_atom"] is None,
                                     r["e_above_hull_eV_per_atom"]))
            return rows

        # ① · ② Li–Nd 이원계
        rows = survey("Li-Nd")
        # 순물질(Li, Nd 단독)은 '화합물'이 아니다 — 이원 화합물만 센다
        compounds = [r for r in rows
                     if not (set(r["formula"]) & set("0123456789") == set()
                             and r["formula"] in ("Li", "Nd"))]
        binaries = [r for r in rows if r["formula"] not in ("Li", "Nd")]
        stable_bin = [r for r in binaries if r["is_stable"]]
        res["binary"] = {
            "chemsys": "Li-Nd", "n_entries": len(rows), "n_binary_compounds": len(binaries),
            "n_stable_binary_compounds": len(stable_bin),
            "stable": stable_bin,
            "closest_metastable": binaries[:5],
            "entries": rows}

        # 대조군
        for cs, why in CONTROLS:
            r = survey(cs)
            b = [x for x in r if x["formula"] not in cs.split("-")]
            res["controls"][cs] = {
                "why": why, "n_entries": len(r), "n_binary_compounds": len(b),
                "n_stable_binary_compounds": sum(1 for x in b if x["is_stable"]),
                "stable_formulas": [x["formula"] for x in b if x["is_stable"]][:10]}

        # ③ 음극 조건 — Li 금속과 평형(μ_Li = μ_Li⁰)에서 볼록껍질에 무엇이 있나
        if not a.skip_interface:
            try:
                from pymatgen.analysis.phase_diagram import PhaseDiagram
                els = a.interface_chemsys.split("-")
                entries = m.get_entries_in_chemsys(els, additional_criteria={
                    "thermo_types": ["GGA_GGA+U"]})
                pd = PhaseDiagram(entries)
                stable = [e.composition.reduced_formula for e in pd.stable_entries]
                li_nd_only = sorted({f for f, e in
                                     ((e.composition.reduced_formula, e) for e in pd.stable_entries)
                                     if set(e.composition.chemical_system.split("-")) <= {"Li", "Nd"}
                                     and len(set(e.composition.chemical_system.split("-"))) == 2})
                res["interface"] = {
                    "chemsys": a.interface_chemsys, "n_entries": len(entries),
                    "n_stable_phases": len(stable),
                    "stable_Li_Nd_binaries_on_hull": li_nd_only,
                    "note": "볼록껍질 위에 Li–Nd 이원상이 있으면 그 계면에서 합금이 "
                            "열역학적으로 생길 수 있다는 뜻이다. 비어 있으면 없다는 뜻."}
            except Exception as exc:
                res["interface"] = {"status": "failed", "error": str(exc)[:300],
                                    "note": "판정 아님 — 조회 실패다"}

    # ── 판정 ─────────────────────────────────────────────────────────────────
    ctrl_ok = sum(1 for v in res["controls"].values() if v["n_stable_binary_compounds"] > 0)
    b = res["binary"]
    if ctrl_ok == 0:
        res["verdict"] = "TOOL_FAILURE"
        res["verdict_text"] = ("⛔ 대조군에서도 안정 화합물이 0개다 — 쿼리가 고장난 것이지 "
                               "판정이 아니다. Li–Nd 결과를 쓰면 안 된다.")
    elif b["n_stable_binary_compounds"] > 0:
        res["verdict"] = "ALLOY_EXISTS"
        res["verdict_text"] = ("Li–Nd 이원계에 껍질 위 안정 화합물이 있다 — "
                               "Xu 2026 의 합금 주장이 열역학적으로 가능하다.")
    else:
        near = b["closest_metastable"][0]["e_above_hull_eV_per_atom"] if b["closest_metastable"] else None
        res["verdict"] = "NO_STABLE_ALLOY"
        res["verdict_text"] = (
            f"Li–Nd 이원계에 껍질 위 안정 화합물이 **없다** (대조군 {ctrl_ok}/{len(CONTROLS)} 계는 있다). "
            f"가장 가까운 준안정상도 hull +{near:.3f} eV/atom. "
            "→ 'Li–Nd alloy 형성'은 열역학적 근거가 약하다. "
            "⚠ 단 이는 **열역학** 판정이다 — 동역학적으로 준안정상이 생길 여지는 남는다. "
            "XPS 995 eV 소피크만으로는 어느 쪽도 확정 못 한다.")

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

    print(f"=== Li–Nd 이원계 ===  엔트리 {b['n_entries']} · 이원화합물 {b['n_binary_compounds']} "
          f"· **껍질 위 안정 {b['n_stable_binary_compounds']}**")
    for r in b["closest_metastable"]:
        print(f"   {r['material_id']:14s} {r['formula']:10s} {str(r['spacegroup']):10s} "
              f"hull +{r['e_above_hull_eV_per_atom']:.4f}  theo={r['theoretical']}")
    print("=== 대조군 (쿼리 건전성) ===")
    for cs, v in res["controls"].items():
        print(f"   {cs:7s} 이원화합물 {v['n_binary_compounds']:3d} · 안정 "
              f"{v['n_stable_binary_compounds']:2d}  {','.join(v['stable_formulas'][:5])}")
    if res["interface"]:
        i = res["interface"]
        if i.get("status") == "failed":
            print(f"=== 계면 조건 === ⚠ 조회 실패 (판정 아님): {i['error'][:120]}")
        else:
            print(f"=== 계면 조건 ({i['chemsys']}) === 안정상 {i['n_stable_phases']}개 중 "
                  f"**Li–Nd 이원상: {i['stable_Li_Nd_binaries_on_hull'] or '없음'}**")
    print(f"\n판정: {res['verdict']}\n{res['verdict_text']}")
    print(f"\n→ {a.out}")
    return 0 if res["verdict"] != "TOOL_FAILURE" else 2


if __name__ == "__main__":
    sys.exit(main())
