#!/usr/bin/env python3
"""li_nd_alloy_check.py — **MP DB 감사**: 안정한 ordered Li–Nd 결정상이 등록돼 있는가.

★ 2026-08-11 역할 축소 (Codex 검토 채택)
  초판은 이 도구를 "Li–Nd alloy 형성 여부 판정"으로 썼는데 **과했다**. 두 가지가 틀렸다:
  ① 6원계 "interface" 계산이 그냥 closed convex hull 이었다 — Li 를 open reservoir 로 두지도,
     μ_Li = Li metal 을 적용하지도 않았다. **0 V 계면 계산이 아니다.**
  ② `ALLOY_EXISTS` / `NO_STABLE_ALLOY` 라는 이름이 고용체·비정질·준안정 나노상까지
     포함하는 것처럼 읽힌다. DB 에 없는 것과 자연에 없는 것은 다르다.

  → 이 도구는 이제 **"선택한 MP release 의 0 K hull 에 stable ordered Li–Nd 결정상이
     등록돼 있는가"** 만 답한다. 그 이상은 말하지 않는다.

⛔ 0 V 계면 산물은 이 도구가 아니라 **기존 open-Li 결과**를 인용할 것:
     tools/oxidation/anode_interface_stability.py · db/properties/oxidation_stability.json
   그쪽 예측(0 V): Li₂O + Li₃P + Li₂S + **NdP** + LiCl — Li–Nd 금속간화합물이 아니라 NdP 다.
   Xu 2026 의 "Li–Nd alloy" 반박은 **그 결과가 주 근거**이고 이 감사는 보조다.

⚠ MP(GGA/GGA+U) 0 K 값이다. 우리 QE 값과 섞지 말 것. 온도·엔트로피·준안정 경로는 다루지 않는다.
⚠ 이 원격 환경은 MP API 가 프록시에 막힌다 — **gabia 에서 실행**할 것.

  export MP_API_KEY=...
  python3 tools/sei/li_nd_alloy_check.py
"""
import argparse
import datetime
import json
import os
import sys

OUT = "db/properties/li_nd_alloy_check.json"
#: API 건전성 **양성 대조** — 여기서 안정상이 안 나오면 쿼리가 고장난 것이다.
#: (Li–La/Ce/Mg 는 과학 비교군이지 양성 대조가 아니다 — 없어도 정상일 수 있다.)
POSITIVE_CONTROLS = {"Li-Al": "LiAl", "Li-Si": "Li15Si4"}
SCIENCE_COMPARISONS = ["Li-La", "Li-Ce", "Li-Mg"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--thermo", default="GGA_GGA+U",
                    help="thermo type 고정 — release 마다 우선순위가 달라질 수 있다")
    a = ap.parse_args()

    key = os.environ.get("MP_API_KEY")
    if not key:
        sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...")
    from mp_api.client import MPRester

    prov = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "thermo_type": a.thermo}
    for mod in ("mp_api", "pymatgen", "emmet"):
        try:
            import importlib.metadata as md
            prov[f"{mod}_version"] = md.version(mod if mod != "emmet" else "emmet-core")
        except Exception:
            prov[f"{mod}_version"] = "unknown"

    res = {"property": "li_nd_alloy_check",
           "scope": "MP DB 감사 — 선택한 release 의 0 K hull 에 stable ordered Li–Nd "
                    "결정상이 등록돼 있는가. **형성 여부 판정이 아니다.**",
           "not_this_tool": "0 V 계면 분해 산물은 tools/oxidation/anode_interface_stability.py "
                            "· db/properties/oxidation_stability.json 을 인용할 것 "
                            "(그 결과의 0 V 산물에는 NdP 가 있고 Li–Nd 금속간화합물은 없다).",
           "warning": "MP(GGA/GGA+U) 0 K. 우리 QE 값과 섞지 말 것. 고용체·비정질·준안정 "
                      "나노상·온도 효과는 이 감사의 범위 밖이다.",
           "provenance": prov, "binary": {}, "positive_controls": {}, "science_comparisons": {}}

    with MPRester(key) as m:
        try:
            res["provenance"]["mp_database_version"] = m.get_database_version()
        except Exception as exc:
            res["provenance"]["mp_database_version"] = f"unavailable: {str(exc)[:80]}"

        def survey(cs):
            docs = m.materials.summary.search(
                chemsys=cs, fields=["material_id", "formula_pretty", "symmetry",
                                    "energy_above_hull", "formation_energy_per_atom",
                                    "theoretical", "is_stable", "nsites"])
            elems = set(cs.split("-"))
            rows = []
            for d in docs:
                if d.formula_pretty in elems:          # 순물질은 '화합물'이 아니다
                    continue
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

        try:
            binaries = survey("Li-Nd")
        except Exception as exc:
            sys.exit(f"⛔ Li-Nd 조회 실패 — 판정 아님: {str(exc)[:200]}")
        stable = [r for r in binaries if r["is_stable"]]
        res["binary"] = {"chemsys": "Li-Nd", "n_binary_compounds": len(binaries),
                         "n_stable": len(stable), "stable": stable,
                         "closest_metastable": binaries[:5], "entries": binaries}

        ctrl_fail = []
        for cs, expect in POSITIVE_CONTROLS.items():
            try:
                r = survey(cs)
            except Exception as exc:
                res["positive_controls"][cs] = {"status": "query_failed", "error": str(exc)[:120]}
                ctrl_fail.append(cs); continue
            st = [x["formula"] for x in r if x["is_stable"]]
            ok = len(st) > 0
            res["positive_controls"][cs] = {"expected_example": expect, "n_stable": len(st),
                                            "stable_formulas": st[:10], "healthy": ok}
            if not ok:
                ctrl_fail.append(cs)

        for cs in SCIENCE_COMPARISONS:
            try:
                r = survey(cs)
            except Exception as exc:
                res["science_comparisons"][cs] = {"status": "query_failed",
                                                  "error": str(exc)[:120]}
                continue
            st = [x["formula"] for x in r if x["is_stable"]]
            res["science_comparisons"][cs] = {"n_binary_compounds": len(r),
                                              "n_stable": len(st), "stable_formulas": st[:10]}

    # ── 판정 ─────────────────────────────────────────────────────────────────
    b = res["binary"]
    if ctrl_fail:
        res["verdict"] = "QUERY_INCONCLUSIVE"
        res["verdict_text"] = (f"⛔ 양성 대조 {ctrl_fail} 에서 안정상이 안 나왔다 — "
                               "쿼리가 고장난 것이지 판정이 아니다. Li–Nd 결과를 쓰면 안 된다.")
    elif b["n_stable"] > 0:
        res["verdict"] = "STABLE_ORDERED_LI_ND_PHASE_IN_MP"
        res["verdict_text"] = ("이 MP release 의 0 K hull 에 안정한 ordered Li–Nd 결정상이 "
                               f"{b['n_stable']}개 등록돼 있다: "
                               + ", ".join(r["formula"] for r in b["stable"]))
    else:
        near = b["closest_metastable"][0] if b["closest_metastable"] else None
        # ⚠ 후보가 정말 0개일 때 포맷이 죽지 않게 (Codex 지적 — 이 도구가 확인하려는 바로 그 경로)
        neartxt = (f"가장 가까운 준안정상은 {near['formula']}({near['material_id']}) "
                   f"hull +{near['e_above_hull_eV_per_atom']:.3f} eV/atom"
                   + (", theoretical(실험 보고 없음)" if near.get("theoretical") else "")
                   if near else "Li–Nd 이원 화합물 엔트리 자체가 하나도 없다")
        res["verdict"] = "NO_STABLE_ORDERED_LI_ND_PHASE_IN_MP"
        res["verdict_text"] = (
            f"이 MP release 의 0 K hull 에 안정한 ordered Li–Nd 결정상이 **없다**. {neartxt}. "
            "같은 경희토류 Li–La·Li–Ce 도 같은 양상이면 계통적 성질로 읽을 수 있다. "
            "⚠ 이것은 **DB 감사**다 — 고용체·비정질·준안정 나노상·동역학 경로를 배제하지 않고, "
            "XPS 피크 귀속을 반증하지도 않는다. 0 V 계면 산물 주장은 open-Li 결과를 인용할 것.")
    res["overall_status"] = ("ok" if res["verdict"] != "QUERY_INCONCLUSIVE" else "inconclusive")

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

    print(f"MP db {res['provenance'].get('mp_database_version')} · thermo {a.thermo} · "
          f"mp_api {res['provenance'].get('mp_api_version')}")
    print(f"=== Li–Nd === 이원화합물 {b['n_binary_compounds']} · **안정 {b['n_stable']}**")
    for r in b["closest_metastable"]:
        print(f"   {r['material_id']:14s} {r['formula']:10s} {str(r['spacegroup']):10s} "
              f"hull +{r['e_above_hull_eV_per_atom']:.4f}  theo={r['theoretical']}")
    print("=== 양성 대조 (쿼리 건전성 — 여기서 0 이면 판정 무효) ===")
    for cs, v in res["positive_controls"].items():
        print(f"   {cs:7s} 안정 {v.get('n_stable', '?')}  {','.join(v.get('stable_formulas', [])[:4])}"
              f"  {'✔' if v.get('healthy') else '⛔'}")
    print("=== 과학 비교군 (없어도 정상) ===")
    for cs, v in res["science_comparisons"].items():
        print(f"   {cs:7s} 이원화합물 {v.get('n_binary_compounds', '?')} · 안정 {v.get('n_stable', '?')}")
    print(f"\n판정: {res['verdict']}\n{res['verdict_text']}")
    print(f"\n→ {a.out}")
    return 0 if res["overall_status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
