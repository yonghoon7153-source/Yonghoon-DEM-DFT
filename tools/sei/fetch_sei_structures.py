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
  python3 tools/sei/fetch_sei_structures.py --get Li3Nd=mp-976264      # 금속 · theoretical

--pick (2026-10-27 · CEI 생성물 갭 카드) — 규칙을 **카드에 먼저 박고** 한 번에 받는다
  규칙 = '실험 관측(theoretical=False) 중 E_hull 최저' — 위 --list 의 '기본 권장' 과 같다.
  사람이 눈으로 고르던 단계를 규칙으로 바꾼 것이라, 후보 표 전부와 **E_hull 최저 엔트리
  (반응 원장이 쓴 hull 상)** 를 같이 기록한다 — 둘이 다르면 그 사실이 남아야 한다.
  같이 받는 것:
    · --with_magnetism : MP 자성 배치(ordering · 자리별 모멘트) → `<base>.magmom.json`.
      모멘트는 구조의 site_properties['magmom'] 을 먼저 쓰고(자리 순서가 구조와 같다),
      없으면 magnetism 문서의 목록을 **길이가 맞을 때만** 쓴다. 안 맞으면 안 쓴다.
    · --with_es_origin : MP 갭이 **어느 계산에서 왔나** (origins → task calc_type).
      ⛔ 2026-09-30 NdP5O14 '−0.943 eV 미재현' 은 비교한 MP 갭이 r2SCAN 구조최적화 값이라
      같은 근사 비교가 아니었다 (D-2026-09-30-cei-ndp5o14-reference-mismatch). 그래서
      참조 갭마다 GGA · GGA+U · r2SCAN 꼬리표를 받을 때 같이 단다.
  MPRester(use_document_model=False) — 09-30 에 문서 모델 불일치(pydantic)로 조회가 끊겼다.

  python3 tools/sei/fetch_sei_structures.py --pick Li2SO4 SCl SO2 CoS2 NiS2 "Ni(PO3)2" \
      --with_magnetism --with_es_origin --outdir db/structures/cei_gap_tm \
      --prov db/properties/cei_gap_tm_structures_2026_10_27.json --prefix ""
  python3 tools/sei/fetch_sei_structures.py --selftest      # 규칙 · 정렬 · 꼬리표 (음성 포함)

⛔ 이 도구가 못 하는 것
  · 고른 다형이 **물리적으로 맞는지** 판정하지 않는다 — 규칙대로 고를 뿐이다. MP 의
    theoretical 꼬리표가 틀리면 같이 틀린다. 후보 표를 사람이 본다.
  · MP 자성 배치가 **바닥상태인지** 보지 않는다. 'MP 가 계산한 상태' 를 옮길 뿐이다.
  · calc_type 꼬리표는 MP 가 적은 문자열을 분류할 뿐이다 — 'GGA' 라도 MP 의 U·PP 규약이다.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

# ⚠ Li3Nd 는 SEI 분해 산물이 아니라 **Xu 2026 §2.6 의 "Li–Nd alloy 계면상" 주장을
#   우리가 직접 재기 위한** 대상이다 (2026-08-11 저자 요청). 다른 6종과 성격이 다르다:
#   · **금속**이라 갭·NEB 규약이 갈린다 (db/properties/sei_electronic_class.json)
#   · 우리 P2 감사에서 Li–Nd 안정 ordered 상은 0개, mp-976264 는 hull +0.197 eV/atom ·
#     theoretical=True 다 — **실험 보고가 없는 예측 구조**임을 반드시 밝히고 인용한다.
FORMULAS = ["Li2O", "Li2S", "LiCl", "Li3P", "Li3PO4", "LiNdO2", "Li3Nd"]
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
            # ⚠ `x or 9e9` 를 쓰면 **E_hull 이 0.0 일 때 falsy 라 9e9 로 밀려난다** —
            #   바닥상태가 목록 맨 뒤로 가고 "관측 중 최저" 선택이 통째로 틀린다
            #   (2026-08-06 실측: Li2S 가 Fm-3m 0.0 대신 Pnma 0.0615 로 뽑혔다).
            docs = sorted(docs, key=lambda d: 9e9 if d.energy_above_hull is None
                          else d.energy_above_hull)
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
            if d.theoretical:
                prov[f]["theoretical_warning"] = (
                    "⚠ 실험 보고가 없는 **예측 구조**다. 이 구조로 낸 값은 "
                    "'MP 에 등록된 예측 구조 기준' 이라고 반드시 밝혀 인용한다.")
            flag = "⚠ 예측만" if d.theoretical else "✅ 관측"
            print(f"✓ {f:8s} {mid:14s} {d.symmetry.symbol:12s} {d.nsites:3d}원자 "
                  f"E_hull {d.energy_above_hull:.4f}  {flag}")
    os.makedirs(os.path.dirname(PROV), exist_ok=True)
    json.dump(prov, open(PROV, "w"), ensure_ascii=False, indent=2)
    print(f"\n출처 기록 → {PROV}")
    print("⚠ 논문·발표에 이 표(mp-id·공간군·실험확인 여부)를 그대로 실을 것.")


# ── --pick (2026-10-27) ─────────────────────────────────────────────────────
def label_of(formula):
    """화학식 → 파일 이름에 쓸 라벨. 괄호를 뺀다: `Ni(PO3)2` → `NiPO32` (09-17 `NdPO33` 와 같은 꼴)."""
    return re.sub(r"[^A-Za-z0-9]", "", str(formula))


def _g(d, k, default=None):
    """문서 모델(속성)과 dict(use_document_model=False) 둘 다 읽는다."""
    if isinstance(d, dict):
        return d.get(k, default)
    return getattr(d, k, default)


def _sym(d):
    s = _g(d, "symmetry") or {}
    return str(_g(s, "symbol", "?")), int(_g(s, "number", 0) or 0)


def _ehull(r):
    """E_hull 정렬 키 — **None 만** 뒤로. 0.0 은 바닥상이지 결측이 아니다 (`or 9e9` 금지)."""
    v = r.get("e_above_hull")
    return 9e9 if v is None else float(v)


def pick_observed_lowest(rows):
    """후보 행들 → (고른 행, E_hull 최저 행, 메모).

    규칙: theoretical=False 중 E_hull 최저 · 동률이면 원자수 적은 쪽 · 그다음 mp-id 문자열 —
    정렬이 임의로 고르지 않게 결정론으로 끊는다 (2026-08-06 '동률이면 정렬이 임의로 고른다').
    관측 다형이 없으면 **고르지 않는다** (None) — 예측 구조로 조용히 내려가지 않는다.
    """
    key = lambda r: (_ehull(r), int(r.get("nsites") or 0), str(r.get("material_id")))
    allr = sorted(rows, key=key)
    hull = allr[0] if allr else None
    obs = [r for r in allr if r.get("theoretical") is False]
    if not obs:
        return None, hull, "관측 다형 없음 — 고르지 않는다 (예측 구조로 내려가지 않는다)"
    pick, note = obs[0], ""
    ties = [r for r in obs[1:] if abs(_ehull(r) - _ehull(pick)) < 1e-4]
    if ties:
        note = ("⚠ E_hull 동률 관측 다형 " + ", ".join(str(r["material_id"]) for r in ties)
                + f" — 원자수·id 로 끊었다 ({pick['material_id']})")
    if hull is not pick:
        note = (note + " · " if note else "") + (
            f"E_hull 최저(반응 원장 hull 상)는 {hull['material_id']} {hull.get('spacegroup')} "
            f"(theoretical={hull.get('theoretical')}) — 고른 관측 다형과 **다르다**")
    return pick, hull, note


def classify_calc_type(ct):
    """MP task calc_type 문자열 → 'GGA' · 'GGA+U' · 'r2SCAN' · 'unknown'.

    ⚠ 순서가 중요하다 — 'GGA+U …' 는 'GGA' 로 시작한다. r2SCAN 을 먼저 거른다.
    """
    s = str(ct or "").strip().lower()
    if not s:
        return "unknown"
    if "r2scan" in s:
        return "r2SCAN"
    if s.startswith("gga+u"):
        return "GGA+U"
    if s.startswith("gga"):
        return "GGA"
    return "unknown"


def align_magmoms(nsites, struct_magmom=None, doc_magmoms=None):
    """자리별 모멘트를 구조 순서에 맞춰 돌려준다 → (목록 또는 None, 출처 메모).

    구조의 site_properties['magmom'] 이 있으면 그게 정답이다(같은 객체의 자리 순서).
    없으면 magnetism 문서 목록을 **길이가 같을 때만** 쓴다 — 길이가 다르면 어느 자리가
    어느 값인지 모른다. 그때는 None (모르는 것을 지어내지 않는다).
    """
    if struct_magmom is not None and len(struct_magmom) == nsites:
        return [float(x) for x in struct_magmom], "structure.site_properties['magmom']"
    if doc_magmoms is not None and len(doc_magmoms) == nsites:
        return [float(x) for x in doc_magmoms], "materials.magnetism.magmoms (길이 일치)"
    n_doc = None if doc_magmoms is None else len(doc_magmoms)
    return None, f"⛔ 정렬 불가 — 자리 {nsites} · 구조 모멘트 " \
                 f"{'없음' if struct_magmom is None else len(struct_magmom)} · 문서 모멘트 {n_doc}"


def _summary_row(d):
    sg, num = _sym(d)
    org = {}
    for o in (_g(d, "origins") or []):
        n = _g(o, "name")
        if n:
            org[str(n)] = str(_g(o, "task_id"))
    eh = _g(d, "energy_above_hull")
    gap = _g(d, "band_gap")
    th = _g(d, "theoretical")
    return {"material_id": str(_g(d, "material_id")), "formula": _g(d, "formula_pretty"),
            "spacegroup": sg, "spacegroup_number": num,
            "e_above_hull": None if eh is None else round(float(eh), 4),
            "theoretical": None if th is None else bool(th),
            "nsites": int(_g(d, "nsites") or 0),
            "band_gap_MP_eV": None if gap is None else round(float(gap), 4),
            "ordering": _g(d, "ordering"), "total_magnetization": _g(d, "total_magnetization"),
            "origins": org}


def do_pick(formulas, outdir, prov_path, prefix, with_mag, with_es):
    from mp_api.client import MPRester
    from pymatgen.io.ase import AseAtomsAdaptor
    from ase.io import write
    if not os.environ.get("MP_API_KEY"):
        sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...  (⚠ 파일에 넣지 말 것)")
    os.makedirs(outdir, exist_ok=True)
    prov = json.load(open(prov_path)) if os.path.isfile(prov_path) else {}
    fields = ["material_id", "formula_pretty", "symmetry", "energy_above_hull", "theoretical",
              "nsites", "band_gap", "ordering", "total_magnetization", "origins"]
    bad = 0
    with MPRester(os.environ["MP_API_KEY"], use_document_model=False) as m:
        def calc_type_of(tid):
            if not tid:
                return None
            try:
                t = m.materials.tasks.search(task_ids=[tid],
                                             fields=["task_id", "calc_type", "task_type", "run_type"])
            except Exception as e:                       # noqa: BLE001 — 조회 실패는 기록한다
                return f"조회 실패: {type(e).__name__}"
            return str(_g(t[0], "calc_type")) if t else None

        for f in formulas:
            lab = label_of(f)
            print(f"\n═══ {f} ({lab}) ═══")
            docs = m.materials.summary.search(formula=f, fields=fields)
            rows = [_summary_row(d) for d in docs]
            if not rows:
                print("  ⛔ MP 에 없음"); bad += 1; continue
            print(f"  {'mp-id':16s} {'공간군':11s} {'E_hull':>8s} {'원자':>4s} {'갭':>7s} {'자성':5s} 관측")
            for r in sorted(rows, key=_ehull):
                eh = "None" if r["e_above_hull"] is None else f"{r['e_above_hull']:.4f}"
                gp = "None" if r["band_gap_MP_eV"] is None else f"{r['band_gap_MP_eV']:.3f}"
                print(f"  {r['material_id']:16s} {r['spacegroup']:11s} {eh:>8s} {r['nsites']:4d} "
                      f"{gp:>7s} {str(r['ordering'])[:5]:5s} "
                      f"{'✅' if r['theoretical'] is False else '⚠ 예측'}")
            pick, hull, note = pick_observed_lowest(rows)
            if note:
                print("  " + note)
            if pick is None:
                bad += 1; continue
            mid = pick["material_id"]
            st = m.get_structure_by_material_id(mid)
            at = AseAtomsAdaptor.get_atoms(st)
            base = f"{prefix}{lab}_{mid}"
            write(os.path.join(outdir, base + ".vasp"), at, format="vasp", direct=True)
            write(os.path.join(outdir, base + ".cif"), at)
            rec = {"formula": f, "label": lab, "rule": "observed_lowest_e_hull",
                   "pick": pick, "hull_entry": hull, "same_as_hull": hull is pick,
                   "n_candidates": len(rows),
                   "candidates": sorted(rows, key=_ehull),
                   "files": [f"{outdir}/{base}.vasp", f"{outdir}/{base}.cif"],
                   "nsites_written": len(at),
                   "source": "Materials Project (mp_api · use_document_model=False)",
                   "fetched": datetime.now().strftime("%Y-%m-%d")}
            if note:
                rec["note"] = note
            if with_es:
                for r in ([pick] if hull is pick else [pick, hull]):
                    tid = r["origins"].get("electronic_structure")
                    ct = calc_type_of(tid)
                    r["es_task"] = tid
                    r["es_calc_type"] = ct
                    r["es_functional"] = classify_calc_type(ct)
                print(f"  갭 출처: {pick.get('es_task')} = {pick.get('es_calc_type')} "
                      f"→ {pick.get('es_functional')}")
            if with_mag:
                smag = st.site_properties.get("magmom")
                dmag, dord = None, None
                try:
                    md = m.materials.magnetism.search(
                        material_ids=[mid], fields=["ordering", "magmoms", "total_magnetization"])
                    if md:
                        dmag, dord = _g(md[0], "magmoms"), _g(md[0], "ordering")
                except Exception as e:                   # noqa: BLE001
                    print(f"  ⚠ magnetism 조회 실패: {type(e).__name__}")
                mags, how = align_magmoms(len(at), smag, dmag)
                rec["magnetism"] = {"ordering_summary": pick.get("ordering"),
                                    "ordering_magnetism_doc": dord, "aligned_from": how,
                                    "total_magnetization": pick.get("total_magnetization")}
                if mags is not None:
                    side = {"material_id": mid, "ordering": dord or pick.get("ordering"),
                            "magmoms": mags, "symbols": at.get_chemical_symbols(),
                            "aligned_from": how, "sum_muB": round(sum(mags), 3)}
                    json.dump(side, open(os.path.join(outdir, base + ".magmom.json"), "w"),
                              ensure_ascii=False, indent=1)
                    rec["files"].append(f"{outdir}/{base}.magmom.json")
                    big = [round(x, 2) for x in mags if abs(x) > 0.1]
                    print(f"  자성 {side['ordering']} · Σ {side['sum_muB']} μB · |m|>0.1 자리 "
                          f"{len(big)} · {how}")
                else:
                    print(f"  {how}")
                    bad += 1
            prov[lab] = rec
            print(f"  ✓ {base} · {pick['spacegroup']} · {len(at)} 원자 · E_hull {pick['e_above_hull']}"
                  f" · MP 갭 {pick['band_gap_MP_eV']}")
    os.makedirs(os.path.dirname(prov_path) or ".", exist_ok=True)
    json.dump(prov, open(prov_path, "w"), ensure_ascii=False, indent=1)
    print(f"\n출처 기록 → {prov_path}  ({'⛔ 문제 ' + str(bad) + ' 건' if bad else '문제 0 건'})")
    return 1 if bad else 0


def selftest():
    """--pick 의 순수 함수들. **음성 경로 포함** — 옛 함정이 다시 들어오면 빨갛게."""
    bad = []

    def chk(c, m):
        if not c:
            bad.append(m)

    chk(label_of("Ni(PO3)2") == "NiPO32", "라벨: 괄호 제거")
    chk(label_of("Li2SO4") == "Li2SO4", "라벨: 그대로")
    R = lambda mid, eh, th, n=12, sg="X": {"material_id": mid, "e_above_hull": eh,
                                            "theoretical": th, "nsites": n, "spacegroup": sg}
    # ① 관측 중 최저 — hull(예측) 과 다르면 메모에 남는다
    rows = [R("mp-1", 0.0, True, sg="P2_1/c"), R("mp-2", 0.012, False, sg="Pa-3"),
            R("mp-3", 0.05, False)]
    p, h, note = pick_observed_lowest(rows)
    chk(p["material_id"] == "mp-2", "관측 최저를 고른다")
    chk(h["material_id"] == "mp-1", "E_hull 최저(hull 상)를 따로 기록한다")
    chk("다르다" in note, "hull 상과 다르면 메모")
    # ② 음성: E_hull 0.0 이 falsy 로 밀리면 안 된다 (`or 9e9` 함정)
    rows = [R("mp-5", 0.03, False), R("mp-4", 0.0, False)]
    chk(pick_observed_lowest(rows)[0]["material_id"] == "mp-4", "[음성] 0.0 이 밀리지 않는다")
    # ③ 음성: None 은 맨 뒤
    rows = [R("mp-7", None, False), R("mp-6", 0.2, False)]
    chk(pick_observed_lowest(rows)[0]["material_id"] == "mp-6", "[음성] None 은 뒤로")
    # ④ 음성: 관측 다형이 없으면 고르지 않는다
    p, h, note = pick_observed_lowest([R("mp-8", 0.0, True)])
    chk(p is None and h["material_id"] == "mp-8" and "고르지 않는다" in note,
        "[음성] 예측뿐이면 None")
    # ⑤ theoretical=None(모름) 은 관측으로 치지 않는다
    chk(pick_observed_lowest([R("mp-9", 0.0, None)])[0] is None, "[음성] theoretical None ≠ 관측")
    # ⑥ 동률 — 원자수 적은 쪽, 결정론
    rows = [R("mp-11", 0.0, False, n=24), R("mp-10", 0.0, False, n=12)]
    p, _, note = pick_observed_lowest(rows)
    chk(p["material_id"] == "mp-10" and "동률" in note, "동률은 원자수로 끊고 메모")
    # ⑦ calc_type 꼬리표 — GGA+U 가 GGA 로 새면 안 된다 · r2SCAN 먼저
    chk(classify_calc_type("GGA NSCF Line") == "GGA", "GGA")
    chk(classify_calc_type("GGA+U NSCF Uniform") == "GGA+U", "[음성] GGA+U 가 GGA 로 새지 않는다")
    chk(classify_calc_type("r2SCAN Structure Optimization") == "r2SCAN", "r2SCAN (09-30 사례)")
    chk(classify_calc_type(None) == "unknown" and classify_calc_type("조회 실패: X") == "unknown",
        "[음성] 모르면 unknown")
    # ⑧ 모멘트 정렬 — 구조 우선 · 길이 불일치는 None
    m, how = align_magmoms(3, [1, -1, 0], [9, 9, 9])
    chk(m == [1.0, -1.0, 0.0] and "structure" in how, "구조 모멘트 우선")
    m, how = align_magmoms(3, None, [2, 2, 0])
    chk(m == [2.0, 2.0, 0.0], "문서 모멘트 (길이 일치)")
    m, how = align_magmoms(4, None, [2, 2, 0])
    chk(m is None and "정렬 불가" in how, "[음성] 길이 불일치는 None")
    m, how = align_magmoms(4, [1, 1], None)
    chk(m is None, "[음성] 구조 모멘트 길이 불일치도 None")
    # ⑨ dict/객체 둘 다 읽는다
    class O:  # noqa: E701
        symmetry = {"symbol": "Pa-3", "number": 205}
    chk(_sym(O()) == ("Pa-3", 205) and _sym({"symmetry": {"symbol": "C2/c", "number": 15}})
        == ("C2/c", 15), "_sym 은 dict·객체 둘 다")
    row = _summary_row({"material_id": "mp-2070", "formula_pretty": "CoS2",
                        "symmetry": {"symbol": "Pa-3", "number": 205}, "energy_above_hull": 0.0,
                        "theoretical": False, "nsites": 12, "band_gap": 0.0,
                        "origins": [{"name": "electronic_structure", "task_id": "mp-99"}]})
    chk(row["e_above_hull"] == 0.0 and row["band_gap_MP_eV"] == 0.0
        and row["origins"]["electronic_structure"] == "mp-99",
        "[음성] 0.0 갭·E_hull 이 None 으로 둔갑하지 않는다")
    print("\n".join("⛔ " + b for b in bad) if bad else "✓ selftest 통과 (20)")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="다형체 후보를 전부 보여 준다")
    ap.add_argument("--get", nargs="*", metavar="화학식=mp-id",
                    help="확정한 것만 받는다 (예: LiCl=mp-22905)")
    ap.add_argument("--formulas", nargs="*", default=FORMULAS)
    ap.add_argument("--pick", nargs="*", metavar="화학식",
                    help="규칙(관측 중 E_hull 최저)으로 골라 받는다 — 후보 표·hull 상을 같이 기록")
    ap.add_argument("--with_magnetism", action="store_true",
                    help="--pick: MP 자성 배치 → <base>.magmom.json")
    ap.add_argument("--with_es_origin", action="store_true",
                    help="--pick: MP 갭의 출처 task calc_type (GGA·GGA+U·r2SCAN)")
    ap.add_argument("--outdir", default=OUTDIR)
    ap.add_argument("--prov", default=PROV)
    ap.add_argument("--prefix", default="sei_",
                    help="--pick 파일 이름 접두 (기본 'sei_' · CEI 표적은 '')")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.pick:
        return do_pick(a.pick, a.outdir, a.prov, a.prefix, a.with_magnetism, a.with_es_origin)
    if a.get:
        do_get([tuple(x.split("=", 1)) for x in a.get])
    else:
        do_list(a.formulas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
