#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lee2024 (J. Mater. Chem. A 2024, 12, 7272-7278) ESI 표 전수 전사 + 독립 검증.

원본: "2. Sup) Design of multicomponent argyrodite based on a mixed oxidation state
       as promising solid-state electrolyte using moment tensor potentials.pdf" (29 pp)

- Table S2 (pp.13-15) : 84 구조 + 모체 Li6PS5I 의 sigma_RT (mS/cm)
- Table S3 (pp.23-25) : 계면 반응에너지 dE_interface (meV) vs LNO / NCM811 / Li
- Table S4 (pp.26-28) : H2S 생성에너지 dE_H2S (eV)

세 표를 index 로 병합해 db/properties/lee2024_si_84_structures.csv 로 출력하고,
digest §11 의 미결 항목(N4 "36 의 내역", N5 "index -> 조성", C1 "군(4-2) 범위")을
표 실물로 재판정한다.

usage: python tools/litdb/lee2024_si_tables_transcribe.py
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PDF = os.path.join(
    ROOT, "litdb", "inbox",
    "2. Sup) Design of multicomponent argyrodite based on a mixed oxidation state "
    "as promising solid-state electrolyte using moment tensor potentials.pdf",
)
OUT_CSV = os.path.join(ROOT, "db", "properties", "lee2024_si_84_structures.csv")

# 표별 페이지(1-indexed, 양끝 포함)
PAGES = {"S2": (13, 15), "S3": (23, 25), "S4": (26, 28)}
NCOL = {"S2": 1, "S3": 3, "S4": 1}          # 조성 뒤에 오는 수치 열 개수

GROUP_RE = re.compile(r"^Group\s*$|^\(?4-[123]\)?$|^Group\s*\(([^)]+)\)$")
IDX_RE = re.compile(r"^(\d{1,2})$")
FORM_RE = re.compile(r"^Li[\d.]")
NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")

# 원소 산화수 (이 논문의 설계공간)
OX = {"Li": 1, "Si": 4, "Ge": 4, "Sn": 4, "P": 5, "Sb": 5, "W": 6, "Mo": 6,
      "S": -2, "Cl": -1, "Br": -1, "I": -1}


def lines(doc, p0, p1):
    out = []
    for p in range(p0 - 1, p1):
        for ln in doc[p].get_text().split("\n"):
            ln = ln.strip()
            if ln and not IDX_RE.match(ln) or ln:
                out.append(ln)
    return [l for l in out if l]


def parse_table(doc, tag):
    """(index, group, formula, [values...]) 리스트를 돌려준다. index 0 = 모체."""
    p0, p1 = PAGES[tag]
    raw = lines(doc, p0, p1)
    # 페이지 번호(단독 정수 13/14/... 로 표 index 와 충돌)를 제거하기 위해
    # "Table S..." 머리글과 페이지번호 줄을 걸러낸다.
    toks = []
    for ln in raw:
        if ln.startswith("Table S") or ln.startswith("Group") or ln.startswith("("):
            if ln.startswith("Group") or ln.startswith("("):
                toks.append(("GRP", ln))
            continue
        if ln in {str(p) for p in range(p0, p1 + 1)} and not toks[-1:] or ln == str(p0):
            pass
        toks.append(("TOK", ln))

    rows, cur_group, i = [], None, 0
    pending_group = ""
    while i < len(toks):
        kind, v = toks[i]
        if kind == "GRP":
            pending_group = (pending_group + " " + v).strip()
            m = re.search(r"\(([^)]+)\)", pending_group)
            if m:
                cur_group = m.group(1)
                pending_group = ""
            i += 1
            continue
        # 조성으로 시작하는 자리를 앵커로 삼는다 (페이지번호 오염에 강함)
        if FORM_RE.match(v):
            # 직전 토큰이 index (또는 '*')
            idx = None
            if i >= 1 and toks[i - 1][0] == "TOK":
                prev = toks[i - 1][1]
                if IDX_RE.match(prev):
                    idx = int(prev)
                elif prev == "*":
                    idx = 0
            vals = []
            j = i + 1
            while j < len(toks) and len(vals) < NCOL[tag]:
                k2, v2 = toks[j]
                if k2 == "GRP":
                    break
                if NUM_RE.match(v2) or re.match(r"^-?\d+(\.\d+)?-\d", v2):
                    vals.append(v2)
                    j += 1
                else:
                    break
            rows.append({"index": idx, "group": cur_group if idx else "pristine",
                         "formula": v, "values": vals})
            i = j
            continue
        i += 1
    return rows


def parse_formula(f):
    """조성식 -> {element: amount}. 'S5I', 'S4.5Cl1.0Br0.5' 등 처리."""
    f = f.rstrip("s")  # Table S2 idx43 의 오타 'S5Is'
    out = defaultdict(float)
    for el, amt in re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", f):
        if el not in OX:
            return None
        out[el] += float(amt) if amt else 1.0
    return dict(out)


def charge(f):
    d = parse_formula(f)
    if d is None:
        return None
    return sum(OX[e] * n for e, n in d.items())


def halogen_class(f):
    d = parse_formula(f) or {}
    tot = d.get("Cl", 0) + d.get("Br", 0) + d.get("I", 0)
    kinds = [e for e in ("Cl", "Br", "I") if d.get(e, 0)]
    return tot, "+".join(kinds)


def cation_core(f):
    """할로겐/S 를 뺀 [A][B][C] 골격 (할로겐 짝 매칭용)."""
    d = parse_formula(f) or {}
    return "".join(f"{e}{d[e]:g}" for e in ("Si", "Ge", "Sn", "P", "Sb", "W", "Mo")
                   if d.get(e, 0))


def main():
    if not os.path.exists(PDF):
        sys.exit(f"PDF 없음: {PDF}")
    doc = fitz.open(PDF)

    tabs = {t: parse_table(doc, t) for t in PAGES}
    for t, rows in tabs.items():
        print(f"[Table {t}] parsed rows = {len(rows)}")

    # ---- index 로 병합 ----
    merged = {}
    for t in ("S2", "S3", "S4"):
        for r in tabs[t]:
            if r["index"] is None:
                print(f"  ! index 미상 ({t}): {r['formula']}")
                continue
            m = merged.setdefault(r["index"], {"index": r["index"],
                                               "group": r["group"],
                                               "formula": r["formula"]})
            if t == "S2":
                m["sigma_RT_mS_cm"] = r["values"][0] if r["values"] else ""
                m["group"] = r["group"]
                m["formula"] = r["formula"]
            elif t == "S3":
                for k, v in zip(("dE_int_LNO_meV", "dE_int_NCM811_meV",
                                 "dE_int_Li_meV"), r["values"]):
                    m[k] = v
            else:
                m["dE_H2S_eV"] = r["values"][0] if r["values"] else ""

    rows = [merged[i] for i in sorted(merged)]
    print(f"\n병합 행 수 = {len(rows)}  (기대: 85 = 모체 1 + 84)")

    # ---- 검증 1: 군별 구조 수 ----
    print("\n=== 검증 1. 군별 구조 수 (Table S2 기준) ===")
    cnt = Counter(r["group"] for r in rows)
    for g in ("pristine", "1", "2", "3", "4-1", "4-2", "4-3"):
        print(f"  group {g:9s} : {cnt.get(g, 0)}")
    g4 = sum(cnt.get(g, 0) for g in ("4-1", "4-2", "4-3"))
    print(f"  -> 군(4) 합계 = {g4}  (본문 'total 36 structures')")
    print(f"  -> 군(1)+(2)+(3) = {sum(cnt.get(g,0) for g in ('1','2','3'))} (Fig 2 x축 48)")

    # ---- 검증 2: 전하중성 ----
    print("\n=== 검증 2. 전하중성 (모든 조성식) ===")
    bad = [(r["index"], r["formula"], charge(r["formula"])) for r in rows
           if charge(r["formula"]) is None or abs(charge(r["formula"])) > 1e-6]
    print(f"  중성 아님/파싱 실패: {len(bad)} 건")
    for b in bad:
        print(f"    idx {b[0]}: {b[1]} -> net {b[2]}")

    # ---- 검증 3: 군(4) 의 36 내역 (N4 미결) ----
    print("\n=== 검증 3. 군(4) 36 구조의 화학적 내역 (digest N4 미결 항목) ===")
    cls = Counter()
    for r in rows:
        if r["group"] not in ("4-1", "4-2", "4-3"):
            continue
        tot, kinds = halogen_class(r["formula"])
        cls[(round(tot, 2), kinds)] += 1
    for (tot, kinds), n in sorted(cls.items()):
        print(f"  할로겐 총량 D{tot:<5g} ({kinds:9s}) : {n} 구조")

    # 단일 할로겐 16종이 Table 1 의 8 코어 x (Cl,Br) 인지
    single = [r for r in rows if r["group"] in ("4-1", "4-2", "4-3")
              and halogen_class(r["formula"])[0] == 1.0]
    cores = Counter(cation_core(r["formula"]) for r in single)
    print(f"\n  단일 할로겐(D1.0) 구조 = {len(single)} / 서로 다른 양이온 코어 = {len(cores)}")
    for c, n in sorted(cores.items()):
        print(f"    {c:28s} x {n}")
    # Table 1 의 8 후보 (군 1-3 에서 뽑힌 idx 27-30, 45-48)
    t1 = {cation_core(r["formula"]) for r in rows if r["index"] in (27, 28, 29, 30, 45, 46, 47, 48)}
    print(f"  Table 1 8종의 코어와 일치? {set(cores) == t1}  (미일치: {set(cores) ^ t1})")

    # ---- 검증 4: 군(4-1)/(4-2) 경계 = 화학인가 sigma 인가 (C1 재판정) ----
    print("\n=== 검증 4. 군(4-1)/(4-2) 경계의 정체 (digest C1 재판정) ===")
    for g in ("4-1", "4-2", "4-3"):
        sub = [r for r in rows if r["group"] == g]
        sig = [float(r["sigma_RT_mS_cm"]) for r in sub if r.get("sigma_RT_mS_cm")]
        idxs = [r["index"] for r in sub]
        print(f"  군({g}): idx {min(idxs)}-{max(idxs)} ({len(sub)}점) "
              f"sigma {min(sig):.2f} - {max(sig):.2f} mS/cm")
        mixed = [r["index"] for r in sub if halogen_class(r["formula"])[0] > 1.0]
        singl = [r["index"] for r in sub if halogen_class(r["formula"])[0] == 1.0]
        print(f"      단일할로겐 idx {singl}")
        print(f"      혼합할로겐 idx {mixed}")

    # sigma 단조성
    print("\n  [sigma 단조 증가 구간 점검]")
    for lo, hi, label in ((1, 12, "군(1)"), (13, 30, "군(2)"), (31, 48, "군(3)"),
                          (49, 79, "군(4-1)+(4-2)"), (80, 84, "군(4-3)")):
        seq = [float(merged[i]["sigma_RT_mS_cm"]) for i in range(lo, hi + 1)
               if merged.get(i, {}).get("sigma_RT_mS_cm")]
        mono = all(seq[k] <= seq[k + 1] for k in range(len(seq) - 1))
        print(f"    {label:16s} idx {lo}-{hi}: 단조증가 {mono}")

    # ---- 검증 5: Cl/Br/I 짝의 계면·H2S 에너지 중복 ----
    print("\n=== 검증 5. 같은 양이온 코어의 할로겐 변종끼리 에너지가 구분되는가 ===")
    bycore = defaultdict(list)
    for r in rows:
        tot, kinds = halogen_class(r["formula"])
        if tot == 1.0:                      # 단일 할로겐만 (I / Cl / Br)
            bycore[cation_core(r["formula"])].append(r)
    dup_int, dup_h2s, tot_pairs = 0, 0, 0
    for core, group in sorted(bycore.items()):
        if len(group) < 2:
            continue
        sig = {r["formula"][-2:]: r.get("sigma_RT_mS_cm") for r in group}
        key_int = defaultdict(list)
        key_h2s = defaultdict(list)
        for r in group:
            key_int[(r.get("dE_int_LNO_meV"), r.get("dE_int_NCM811_meV"),
                     r.get("dE_int_Li_meV"))].append(r["index"])
            key_h2s[r.get("dE_H2S_eV")].append(r["index"])
        for k, v in key_int.items():
            if len(v) > 1:
                dup_int += 1
                halos = [merged[i]["formula"] for i in v]
                print(f"  [계면 3값 완전동일] {core:26s} idx {v} -> {k}")
                print(f"      조성: {halos}")
                print(f"      그런데 sigma_RT 는 {[merged[i]['sigma_RT_mS_cm'] for i in v]}")
        for k, v in key_h2s.items():
            if len(v) > 1:
                dup_h2s += 1
        tot_pairs += 1
    print(f"\n  -> 계면 3값이 완전히 같은 할로겐 변종 묶음: {dup_int} 개 (코어 {tot_pairs} 개 중)")

    # ---- 검증 6: 전체 표에서 dE_int 3값 튜플 중복도 ----
    print("\n=== 검증 6. Table S3 전체의 값 중복도 ===")
    trip = Counter((r.get("dE_int_LNO_meV"), r.get("dE_int_NCM811_meV"),
                    r.get("dE_int_Li_meV")) for r in rows)
    multi = {k: v for k, v in trip.items() if v > 1}
    print(f"  고유 3값 튜플 {len(trip)} 개 / 전체 {len(rows)} 행 "
          f"-> 2행 이상 공유 튜플 {len(multi)} 개, 관련 행 {sum(multi.values())} 개")
    lno = Counter(r.get("dE_int_LNO_meV") for r in rows)
    print(f"  LNO 열 고유값 {len(lno)} 개뿐 (85 행) — 상위 중복:")
    for v, n in lno.most_common(6):
        print(f"    {v:>9s} meV x {n} 행")

    # ---- 검증 7: sigma vs 안정성 상관 (본문 trade-off 주장) ----
    print("\n=== 검증 7. sigma 상위 10 vs H2S 안정성 ===")
    top = sorted((r for r in rows if r.get("sigma_RT_mS_cm")),
                 key=lambda r: -float(r["sigma_RT_mS_cm"]))[:10]
    for r in top:
        print(f"  idx {r['index']:>2} {r['formula']:44s} "
              f"sigma {float(r['sigma_RT_mS_cm']):6.2f}  dE_H2S {r.get('dE_H2S_eV','?'):>6}  "
              f"dE_int(Li) {r.get('dE_int_Li_meV','?'):>9}")

    # ---- CSV 출력 ----
    cols = ["index", "group", "formula", "sigma_RT_mS_cm", "dE_int_LNO_meV",
            "dE_int_NCM811_meV", "dE_int_Li_meV", "dE_H2S_eV",
            "halogen_total", "halogen_kinds", "cation_core", "net_charge"]
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            tot, kinds = halogen_class(r["formula"])
            w.writerow({**{c: r.get(c, "") for c in cols},
                        "halogen_total": f"{tot:g}", "halogen_kinds": kinds,
                        "cation_core": cation_core(r["formula"]),
                        "net_charge": f"{charge(r['formula']):+.3f}"})
    print(f"\n[written] {os.path.relpath(OUT_CSV, ROOT)}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
