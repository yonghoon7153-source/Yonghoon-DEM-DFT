#!/usr/bin/env python3
"""cascade_v23_candidates.py — v23 unified dataset -> 논문 후보군 추출기.

gabia에서:
  python3 cascade_v23_candidates.py --csv /data/work/runs/multi_category_2026_05_26_v23/unified_dataset_273.csv --schema
  python3 cascade_v23_candidates.py --csv .../unified_dataset_273.csv > v23_candidates_report.txt

출력 5부:
  [1] 단일 도펀트 랭킹 (형성 dE / 연성 E_VRH / 저변형 |dV| / 종합점수)
  [2] 농도 추세표 + 과잉도핑 플래그 (비단조 dE, |dV|>6%, EOS핏 실패, x010 경화)
  [3] 카테고리 분해 (oxide/halide/nitride/sulfide별 요약 — 화학 일반화의 근거)
  [4] co-doping 시너지 후보 (메커니즘 상보 페어링 + Clrich-부스트 실측 반영)
  [5] DFT-EOS 승격 후보군 (건강 필터 통과 top-N; modelc-1.6 브리지 프로토콜용)
컬럼명은 자동 매핑(스키마가 달라도 동작); 없는 지표는 해당 분석만 생략.
"""
import argparse
import csv as _csv
import math
import re
import sys
from collections import defaultdict

ALIAS = {  # 표준키: 후보 컬럼명 정규식 (첫 매치 사용)
    "compound": r"^(compound|dopant|name)$",
    "x":        r"^(x|conc|concentration|x_compound)$",
    "de":       r"(de_post|de_anneal|dE|delta_e|e_form)",
    "dv":       r"(dv|dV|vol.*(pct|change)|delta_v)",
    "b0":       r"(eos.*b0|b0.*gpa|^b0$)",
    "evrh":     r"(e_vrh|evrh|young)",
    "site":     r"(site|champion_site)",
    "variant":  r"(variant|chain)",
    "conv":     r"(converg)",
}
ANION_CAT = [("F", "fluoride"), ("Cl", "chloride"), ("Br", "bromide"), ("I", "iodide"),
             ("N", "nitride"), ("O", "oxide"), ("S", "sulfide")]


def catg(compound):
    # 화학식 끝쪽 음이온으로 분류 (O보다 F/Cl 우선 검사; Li2O vs LiF 등)
    for sym, name in ANION_CAT:
        if re.search(sym + r"\d*$", compound) or (sym in ("F", "Cl", "Br", "I", "N") and sym in compound):
            return name
    return "other"


def fnum(v):
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--schema", action="store_true", help="컬럼/샘플만 출력")
    ap.add_argument("--topn", type=int, default=12)
    ap.add_argument("--dv_flag", type=float, default=6.0, help="|dV|%% 과잉도핑 플래그 문턱")
    a = ap.parse_args()

    rows = list(_csv.DictReader(open(a.csv)))
    cols = list(rows[0].keys()) if rows else []
    if a.schema or not rows:
        print(f"rows={len(rows)}  columns={len(cols)}")
        for c in cols:
            print(" ", c)
        for r in rows[:3]:
            print(r)
        return

    m = {}
    for key, pat in ALIAS.items():
        for c in cols:
            if re.search(pat, c, re.I):
                m[key] = c
                break
    missing = [k for k in ("compound", "x", "de") if k not in m]
    if missing:
        sys.exit(f"필수 컬럼 자동매핑 실패: {missing} — --schema로 컬럼명 확인 후 ALIAS 보강 필요")
    print("컬럼 매핑:", {k: m.get(k) for k in ALIAS})

    # ---- 수집: (compound, x) -> metrics ----
    D = defaultdict(dict)
    for r in rows:
        c = r[m["compound"]].strip()
        x = r[m["x"]].strip()
        rec = D[c].setdefault(x, {})
        rec["de"] = fnum(r.get(m.get("de", ""), None))
        rec["dv"] = fnum(r.get(m.get("dv", ""), None))
        rec["b0"] = fnum(r.get(m.get("b0", ""), None))
        rec["evrh"] = fnum(r.get(m.get("evrh", ""), None))
        rec["site"] = r.get(m.get("site", ""), "")
        rec["variant"] = r.get(m.get("variant", ""), "")

    xs_order = sorted({x for d in D.values() for x in d})
    print(f"\n화합물 {len(D)}종 × 농도 {xs_order}")

    # ---- [1] 단일 랭킹 ----
    def best_of(c):
        recs = [(x, d) for x, d in D[c].items() if d.get("de") is not None]
        return min(recs, key=lambda t: t[1]["de"]) if recs else (None, None)

    singles = []
    for c in D:
        x, d = best_of(c)
        if d:
            singles.append((c, x, d))
    print(f"\n===== [1] 단일 도펀트 랭킹 (각 화합물 최적 x 기준, top {a.topn}) =====")
    print("-- 형성 favorability (dE 최저) --")
    for c, x, d in sorted(singles, key=lambda t: t[2]["de"])[:a.topn]:
        print(f"  {c:12s}@{x}  dE {d['de']:+.3f}  dV {d['dv'] if d['dv'] is not None else '–'}%  "
              f"E_VRH {d['evrh'] if d['evrh'] is not None else '–'}  [{catg(c)}]")
    soft = [t for t in singles if t[2].get("evrh")]
    if soft:
        print("-- 연성 (E_VRH 최저 = soft-contact/coating 후보) --")
        for c, x, d in sorted(soft, key=lambda t: t[2]["evrh"])[:a.topn]:
            print(f"  {c:12s}@{x}  E_VRH {d['evrh']:.1f}  dE {d['de']:+.3f}  [{catg(c)}]")
    strain = [t for t in singles if t[2].get("dv") is not None]
    if strain:
        print("-- 저변형 (|dV| 최소 = 격자 스트레인 최소) --")
        for c, x, d in sorted(strain, key=lambda t: abs(t[2]["dv"]))[:a.topn]:
            print(f"  {c:12s}@{x}  dV {d['dv']:+.2f}%  dE {d['de']:+.3f}  [{catg(c)}]")

    # ---- [2] 농도 추세 + 과잉도핑 플래그 ----
    print("\n===== [2] 과잉도핑 진단 (농도 3점 보유 화합물) =====")
    over = []
    for c in sorted(D):
        des = [D[c].get(x, {}).get("de") for x in xs_order]
        if None in des or len(des) < 3:
            continue
        flags = []
        if not (des[0] >= des[1] <= des[2]) and not (des[0] <= des[1] <= des[2]) \
           and not (des[0] >= des[1] >= des[2]):
            flags.append("dE 비단조")
        if des[2] > des[0]:
            flags.append("x010에서 dE 후퇴")
        dvs = [D[c].get(x, {}).get("dv") for x in xs_order]
        if dvs[-1] is not None and abs(dvs[-1]) > a.dv_flag:
            flags.append(f"|dV|@x010 {dvs[-1]:+.1f}%")
        b0s = [D[c].get(x, {}).get("b0") for x in xs_order]
        if any(b == 0.0 for b in b0s if b is not None):
            flags.append("EOS핏 실패 있음")
        if flags:
            over.append((c, des, flags))
    for c, des, flags in over:
        print(f"  ⚠ {c:12s} dE({','.join(xs_order)}) = {['%+.3f' % d for d in des]}  → {'; '.join(flags)}")
    print(f"  (플래그 {len(over)}종 / 3점 보유 화합물)")

    # ---- [3] 카테고리 분해 ----
    print("\n===== [3] 카테고리별 요약 =====")
    bycat = defaultdict(list)
    for c, x, d in singles:
        bycat[catg(c)].append(d["de"])
    for cat, vals in sorted(bycat.items(), key=lambda t: min(t[1])):
        print(f"  {cat:9s} n={len(vals):3d}  best dE {min(vals):+.3f}  median {sorted(vals)[len(vals)//2]:+.3f}")

    # ---- [4] co-doping 시너지 후보 ----
    print("\n===== [4] co-doping 시너지 후보 (메커니즘 상보 페어링) =====")
    de_rank = sorted(singles, key=lambda t: t[2]["de"])[:8]
    strain_rank = sorted(strain, key=lambda t: abs(t[2]["dv"]))[:8] if strain else []
    soft_rank = sorted(soft, key=lambda t: t[2]["evrh"])[:8] if soft else []
    clboost = [c for c in D for x, d in D[c].items() if "clrich" in (d.get("variant") or "").lower()]
    print("  (i) 형성-강자 × 저변형 짝 (에너지 이득 + 스트레인 상쇄):")
    for (c1, x1, d1) in de_rank[:4]:
        for (c2, x2, d2) in strain_rank[:4]:
            if c1 != c2 and catg(c1) != catg(c2):
                print(f"      {c1}@{x1} (dE {d1['de']:+.2f}) + {c2}@{x2} (dV {d2['dv']:+.1f}%)")
    if clboost:
        print(f"  (ii) Clrich-부스트 실측 화합물 (변형 체인이 챔피언): {sorted(set(clboost))}")
        print("      → cation-도펀트 + Cl-풍부화 = Type-C co-substitution의 캐스케이드 내 증거;")
        print("        이들의 modelc-1.6 (Cl-rich host) 재검이 co-doping 1순위 실험")
    print("  (iii) 문헌 Type-C (precursor review): aliovalent cation@Li + halide@S 명시 조합")
    print("        예: Al+Cl (Li5.4Al0.1PS4.7Cl1.3 문헌 실재), Mg+F (MgF2 = Tier-B 재료)")

    # ---- [5] DFT-EOS 승격 후보 ----
    print("\n===== [5] DFT-EOS 승격 후보군 (건강 필터: 3점 dE 단조·|dV|<{:.0f}%·EOS핏 정상) =====".format(a.dv_flag))
    flagged = {c for c, _, _ in over}
    healthy = [(c, x, d) for c, x, d in singles if c not in flagged]
    n = 0
    for c, x, d in sorted(healthy, key=lambda t: t[2]["de"]):
        n += 1
        if n > a.topn:
            break
        print(f"  {n:2d}. {c:12s}@{x}  dE {d['de']:+.3f}  dV {d['dv'] if d['dv'] is not None else '–'}%  "
              f"E_VRH {d['evrh'] if d['evrh'] is not None else '–'}  [{catg(c)}]")
    print("\n  승격 프로토콜(pipeline v2): 챔피언 xyz → (필요시 modelc-1.6 브리지 재치환) → UMA EOS →")
    print("  KISTI 고정셀 v094–106 체인(sbatch_dft_eos_*_chain.sh, carry 패치) → llm_fitting_bm.py")


if __name__ == "__main__":
    main()
