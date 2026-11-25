#!/usr/bin/env python3
"""sei_product_gaps.py — band gaps of the SEI / decomposition product phases.

After esw_grand_potential.py gives the decomposition reactions for the
Nd2O3-doped composition, this looks up the MP band gap of each product phase
(lowest-energy entry per formula) to test the claim that the doped-cell
interphase is ELECTRONICALLY INSULATING (wide-gap) -> blocks e- leakage even
though the BULK gap narrowed.

Run on gabia/kserver116 where MP_API_KEY is set + MP reachable:
    python3 sei_product_gaps.py --formulas Li3PO4 Li4P2O7 NdPO4 Nd2O3 Nd2S3 \
        NdCl3 Li2S LiCl Li3P Li3PS4 Li2O S --out sei_product_gaps.json

NOTE (consistency with kb/physics/260318 PBE+U-4f note):
  MP gaps are PBE/PBE+U. For Nd-bearing phases (NdPO4, Nd2O3, Nd2S3, NdCl3)
  the 4f mis-placement => MP gap is a LOWER BOUND (real gap larger; e.g. exp
  Nd2O3 ~4.7, NdCl3 ~5 eV). Nd-FREE phases (Li3PO4 ~ exp 8, Li2S, LiCl) are
  reliable. The script flags Nd-bearing rows accordingly.
"""
import argparse, json, os
from pathlib import Path

DEFAULT = ["Li3PO4", "Li4P2O7", "NdPO4", "Nd2O3", "Nd2S3", "NdCl3",
           "Li2S", "LiCl", "Li3P", "Li3PS4", "Li2O", "S",
           # ⛔ 2026-09-13 추가 — 원장에 **Li3N 이 없었다.** 우리는 "Li3P 는 전자를
           #   샌다" 고 쓰면서, [Li26FDI] 가 그 대체재로 고른 Li3N 에 대해선 아무 말도
           #   안 하고 있었다 (그 논문 Fig.1g 에서 Li3N 이 최협갭이다).
           "Li3N"]
# rough experimental gaps for the key wide-gap insulators (sanity anchor, eV)
EXP_ANCHOR = {"Li3PO4": "~8 (exp)", "Li2O": "~7.99 (exp)", "LiCl": "~9.4 (exp)",
              "Nd2O3": "~4.7 (exp)", "NdCl3": "~5 (exp)", "NdPO4": "wide (monazite)",
              # ⛔ 값을 **지어내지 않는다** — 원전 확인 전까지 빈칸으로 둔다.
              "Li3N": "⚠ 미확인 — 원전 확인 후 채운다 (다형·측정법에 따라 갈린다)"}


def _hull_key(v):
    """E_hull 정렬 키. **None 만** 뒤로 보낸다 — 0.0 은 바닥상이지 결측이 아니다.

    ⛔ `v or 9e9` 를 쓰면 안 된다: 파이썬에서 `0.0` 은 거짓이라 바닥상이 밀린다
      (2026-09-13 실측 버그).
    """
    return 9e9 if v is None else float(v)


def _row(d):
    """MP doc 하나 → 기록 한 줄. 공간군까지 남긴다 (어느 다형인지 적으려면 필요하다)."""
    sym = getattr(d, "symmetry", None)
    return {"material_id": str(d.material_id),
            "formula": d.formula_pretty,
            "band_gap_MP_eV": round(float(d.band_gap), 3),
            "e_above_hull": round(float(d.energy_above_hull or 0), 4),
            "is_stable": bool(d.is_stable),
            "spacegroup_symbol": str(getattr(sym, "symbol", "?")),
            "spacegroup_number": int(getattr(sym, "number", 0) or 0)}


# ── 반응식에서 생성물 뽑기 (2026-08-19 신설) ─────────────────────────────────
#: 왜 — 계면 게이트의 자인된 약점이 "**분해산물 전자전도도 미고려**" 다
#:   (`cascade_stability_axes_verdict.json` honesty_header, Sundar 2025 비판 인용).
#:   반응식은 이미 다 있으니 산물 갭만 **조회**하면 그 구멍이 메워진다. 계산 아님.
#: 판정 규칙 — 한 반응의 병목은 **산물 중 최소 갭**이다. 하나라도 금속이면 그 층은
#:   전자를 통과시키므로 자기제한이 안 된다.
#: grand-potential 반응식에서 **저장고 원소는 산물이 아니다** — 균형식 부기로 나올 뿐
#:   석출상이 아니다. 이걸 세면 "금속 산물" 비율이 부풀려진다 (2026-08-19 실측: 73 → 69 %).
OPEN_ELEMENTS = ("Li",)


def products_of(rxn, drop_open=True):
    """'0.5 A + 0.5 B -> 0.3 C + 0.2 D' → ['C', 'D'] (계수 제거).

    이 함수가 **못 하는 것**: 화살표가 없으면 빈 목록을 낸다 (좌변을 산물로
      착각하지 않는다). 수화물 점(·) 표기는 다루지 않는다.
    """
    import re as _re
    if not rxn or "->" not in rxn:
        return []
    out = []
    for tok in rxn.split("->", 1)[1].split("+"):
        t = _re.sub(r"^\s*[0-9]*\.?[0-9]+\s+", "", tok.strip())
        if t and _re.match(r"^[A-Z]", t):
            if drop_open and t in OPEN_ELEMENTS:
                continue
            out.append(t)
    return out


def reactions_in(path):
    """CSV(rxn_* 열) 또는 JSONL(reaction 필드)에서 (라벨, 반응식) 목록."""
    import csv as _csv, io as _io
    out = []
    if path.endswith(".jsonl"):
        for ln in _io.open(path, encoding="utf-8"):
            try:
                d = json.loads(ln)
            except Exception:
                continue
            base = f"{d.get('species','?')}|{d.get('cathode','?')}"
            if d.get("reaction"):
                out.append((base, d["reaction"]))
            for V, v in (d.get("by_voltage") or {}).items():
                if v.get("reaction"):
                    out.append((f"{base}|{V}V", v["reaction"]))
        return out
    lines = [l for l in _io.open(path, encoding="utf-8") if not l.startswith("#")]
    for r in _csv.DictReader(lines):
        for k, v in r.items():
            if k and k.startswith("rxn_") and v:
                out.append((f"{r.get('coating', r.get('dopant', '?'))}|{k[4:]}", v))
    return out


# ── 다형 맞추기 (2026-09-17 신설) ────────────────────────────────────────────
#: 왜 — **바닥상이 우리 구조와 다를 수 있다.** 실측 두 건이 같은 날 나왔다:
#:   · Nd₂O₃ — MP 바닥상 Ia-3 3.708 / 우리 옛 실측은 P-3m1 (다른 상, 3.9479)
#:   · P₂O₅ — MP 바닥상 Pnma 4.85 / §C 표적은 **Fdd2** (다형 12개)
#:   조성만 맞춰 갭을 가져오면 "우리 계산이 MP 를 재현했나" 의 기준이 딴 상이 된다.
def match_spacegroup(gaps, targets):
    """{조성: MP row} × {이름: 표적} → 표적 공간군과 **같은 다형**을 골라 준다.

    ⛔ 못 찾으면 **바닥상으로 대체하지 않는다.** "못 찾음"과 "없음"을 구분해
      `matched: null` + `why` 로 남긴다 (조용히 딴 상을 기준으로 삼는 것이
      정확히 우리가 막으려는 사고다).
    ⛔ 이 함수가 못 하는 것: 공간군 기호가 같으면 같은 구조로 **본다**. 셀 크기·
      원자수는 확인하지 않는다 (호출부가 n_atoms 를 같이 보고해야 한다).
    """
    out = {}
    for name, t in targets.items():
        f = t.get("formula", name)
        row = gaps.get(f)
        if not isinstance(row, dict) or "band_gap_MP_eV" not in row:
            out[name] = {"matched": None, "why": f"MP 조회에 {f} 가 없다"}
            continue
        want = str(t.get("spacegroup", "")).strip()
        polys = row.get("polymorphs") or [row]
        hit = [r for r in polys if str(r.get("spacegroup_symbol", "")).strip() == want]
        gs = row  # 바닥상 (lowest e_above_hull)
        rec = {"formula": f, "our_spacegroup": want, "our_mp_id": t.get("mp_id"),
               "our_n_atoms": t.get("n_atoms"),
               "mp_ground_state": {"spacegroup": gs.get("spacegroup_symbol"),
                                   "material_id": gs.get("material_id"),
                                   "band_gap_MP_eV": gs.get("band_gap_MP_eV")},
               "n_polymorphs_in_MP": row.get("n_polymorphs_in_MP")}
        if not hit:
            rec.update({"matched": None,
                        "why": f"MP 다형 {len(polys)}개 중 공간군 '{want}' 가 없다 — "
                               "바닥상으로 대체하지 않는다. 표적 구조를 다시 확인할 것"})
        else:
            m = min(hit, key=lambda r: _hull_key(r.get("e_above_hull")))
            rec.update({"matched": m,
                        "band_gap_MP_eV": m.get("band_gap_MP_eV"),
                        "is_mp_ground_state":
                            m.get("material_id") == gs.get("material_id")})
            if len(hit) > 1:
                rec["⚠"] = f"같은 공간군 다형이 {len(hit)}개 — E_hull 최소를 골랐다"
            if not rec["is_mp_ground_state"]:
                rec["⚠_바닥상_아님"] = (
                    f"MP 바닥상은 {gs.get('spacegroup_symbol')} "
                    f"({gs.get('band_gap_MP_eV')} eV) 다. 우리 표적과 **다른 상**이므로 "
                    "재현 판정은 여기 matched 값으로만 한다.")
        out[name] = rec
    return out


def _emit_match(gaps, targets_path, out_path, src_path=None):
    """맞추기 결과를 화면 표 + JSON 으로 낸다. 화면이 정본이 아니라 JSON 이 정본이다."""
    import hashlib
    t = json.loads(Path(targets_path).read_text(encoding="utf-8"))
    targets = t.get("targets") or t
    m = match_spacegroup(gaps, targets)
    print(f"\n── 공간군 맞추기 ({targets_path}) ──")
    print(f"  {'상':11s} {'우리 공간군':11s} {'갭[eV]':>7s}  {'MP 바닥상':11s} 비고")
    for name, r in sorted(m.items()):
        g = r.get("band_gap_MP_eV")
        gs = (r.get("mp_ground_state") or {}).get("spacegroup") or "?"
        note = ("⛔ " + r["why"]) if r.get("matched") is None else (
            "" if r.get("is_mp_ground_state") else "⚠ 바닥상 아님")
        print(f"  {name:11s} {str(r.get('our_spacegroup','?')):11s} "
              f"{(f'{g:.3f}' if isinstance(g,(int,float)) else '—'):>7s}  {gs:11s} {note}")
    rec = {"property": "cei_gap_targets_mp_reference",
           "purpose": "§C 판별종의 **우리 표적 다형과 같은 공간군** MP 참조갭. "
                      "우리 fixed-occ nscf 의 검증 표적이다.",
           "⛔": "MP PBE 값이다 — 우리 db 갭 표에 넣지 않는다 (문헌·db 분리 규율). "
                 "재현 판정은 '같은 자릿수·같은 순위' 로만 한다.",
           "targets_file": str(targets_path), "source_file": str(src_path or ""),
           "matched": m}
    if src_path and Path(src_path).is_file():
        rec["source_sha256"] = hashlib.sha256(Path(src_path).read_bytes()).hexdigest()
    Path(out_path).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
    print(f"\n-> {out_path}")
    bad = [k for k, v in m.items() if v.get("matched") is None]
    if bad:
        print(f"⛔ 공간군을 못 찾은 상 {len(bad)}개: {', '.join(bad)} — "
              "바닥상으로 대체하지 않았다. 표적 구조를 확인할 것")
    return 1 if bad else 0


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    chk(products_of("0.57 Sc2O3 + 0.43 Li6PS5Cl -> 0.036 Li3Sc2(PO4)3 + 1.07 LiScS2 "
                    "+ 0.32 Li3PO4 + 0.43 LiCl")
        == ["Li3Sc2(PO4)3", "LiScS2", "Li3PO4", "LiCl"],
        "[양성] 계수를 떼고 산물만 뽑는다 (괄호 조성 포함)")
    chk(products_of("Sc2O3 -> Sc2O3") == ["Sc2O3"], "[양성] 무반응식도 산물 하나")
    chk(products_of("A -> 28 Li + P2S7") == ["P2S7"],
        "[음성] 저장고 원소 Li 는 산물이 아니다 (grand-potential 부기)")
    chk(products_of("A -> 28 Li + P2S7", drop_open=False) == ["Li", "P2S7"],
        "[양성] drop_open=False 면 그대로 (닫힌계용)")
    chk(products_of("0.5 A + 0.5 B") == [],
        "[음성] 화살표가 없으면 빈 목록 (좌변을 산물로 착각하지 않는다)")
    chk(products_of("") == [] and products_of(None) == [],
        "[음성] 빈 입력은 빈 목록")
    chk(products_of("A -> 0.5 li3po4") == [],
        "[음성] 대문자로 시작 안 하면 조성이 아니다")
    import tempfile, os as _os
    with tempfile.TemporaryDirectory() as d:
        p = _os.path.join(d, "x.jsonl")
        open(p, "w").write(json.dumps({"species": "MgO", "cathode": "LCO",
                                       "by_voltage": {"4.30": {"reaction": "A -> B + C"}}}) + "\n")
        r = reactions_in(p)
        chk(r == [("MgO|LCO|4.30V", "A -> B + C")], f"[양성] JSONL 의 전압별 반응식 ({r})")
    # ⛔⛔음성 (2026-09-13) — 바닥상(E_hull=0.0)이 선택되는가. `or 9e9` 가 돌아오면 잡힌다.
    _docs = [("Pnma", 0.084), ("Fm-3m", 0.0), ("P6_3mc", 0.004)]
    _pick = min(_docs, key=lambda x: _hull_key(x[1]))
    _c = _pick[0] == "Fm-3m"
    print(("  ✓ " if _c else "  ⛔ ") + "⛔⛔음성: E_hull=0.0 인 **바닥상**이 선택된다 "
          f"(고른 것: {_pick[0]} {_pick[1]})")
    ok = ok and _c
    _c2 = min([("A", None), ("B", 0.5)], key=lambda x: _hull_key(x[1]))[0] == "B"
    print(("  ✓ " if _c2 else "  ⛔ ") + "⛔음성: E_hull 이 None 인 항목만 뒤로 간다 (0.0 과 구분)")
    ok = ok and _c2
    # ── 다형 맞추기 (2026-09-17) ──────────────────────────────────────────
    _gaps = {"P2O5": {"band_gap_MP_eV": 4.85, "spacegroup_symbol": "Pnma",
                      "material_id": "mp-gs", "e_above_hull": 0.0,
                      "n_polymorphs_in_MP": 3,
                      "polymorphs": [
                          {"spacegroup_symbol": "Pnma", "material_id": "mp-gs",
                           "band_gap_MP_eV": 4.85, "e_above_hull": 0.0},
                          {"spacegroup_symbol": "Fdd2", "material_id": "mp-fdd2",
                           "band_gap_MP_eV": 5.11, "e_above_hull": 0.012},
                          {"spacegroup_symbol": "Fdd2", "material_id": "mp-fdd2b",
                           "band_gap_MP_eV": 5.40, "e_above_hull": 0.031}]},
             "NdCl3": {"band_gap_MP_eV": 4.2998, "spacegroup_symbol": "P6_3/m",
                       "material_id": "mp-a", "e_above_hull": 0.0}}
    _m = match_spacegroup(_gaps, {
        "P2O5": {"formula": "P2O5", "spacegroup": "Fdd2", "mp_id": "x", "n_atoms": 14},
        "NdCl3": {"formula": "NdCl3", "spacegroup": "P6_3/m"},
        "NdPS4": {"formula": "NdPS4", "spacegroup": "I4_1/acd"},
        "Bogus": {"formula": "P2O5", "spacegroup": "Pm-3m"}})
    chk(_m["P2O5"]["band_gap_MP_eV"] == 5.11,
        f"양성: 조성이 아니라 **공간군**으로 고른다 (Fdd2 5.11, 바닥상 Pnma 4.85 아님) "
        f"— 고른 값 {_m['P2O5'].get('band_gap_MP_eV')}")
    chk(_m["P2O5"].get("is_mp_ground_state") is False and "⚠_바닥상_아님" in _m["P2O5"],
        "양성: 바닥상이 아니면 그렇다고 **표시한다** (재현 판정 기준이 갈리므로)")
    chk("⚠" in _m["P2O5"], "양성: 같은 공간군 다형이 둘이면 E_hull 최소를 고르고 알린다")
    chk(_m["NdCl3"]["band_gap_MP_eV"] == 4.2998 and _m["NdCl3"]["is_mp_ground_state"],
        "양성: polymorphs 가 없으면 행 자체를 다형 하나로 본다")
    chk(_m["NdPS4"]["matched"] is None and "MP 조회에" in _m["NdPS4"]["why"],
        "⛔음성: MP 조회에 없는 상은 **없다고 적는다** (0 이나 바닥상으로 때우지 않는다)")
    chk(_m["Bogus"]["matched"] is None and "Pm-3m" in _m["Bogus"]["why"],
        "⛔음성: 공간군이 다형 목록에 없으면 **바닥상으로 대체하지 않는다** "
        "(Nd₂O₃·P₂O₅ 사고의 형태)")
    chk(_m["Bogus"].get("band_gap_MP_eV") is None,
        "⛔음성: 못 찾았는데 갭 값이 달려 나오지 않는다")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formulas", nargs="+", default=DEFAULT)
    ap.add_argument("--from_reactions", nargs="+",
                    help="CSV(rxn_* 열) / JSONL(reaction) 에서 산물을 뽑아 쓴다")
    ap.add_argument("--all_polymorphs", action="store_true",
                    help="조성마다 **모든 다형**을 같이 기록한다 (α/β 처럼 갭이 갈리는 계에 필요)")
    ap.add_argument("--out", default="sei_product_gaps.json")
    ap.add_argument("--match_spacegroup",
                    help="표적 구조 JSON(targets:{이름:{formula,spacegroup,mp_id,n_atoms}}) — "
                         "조성이 아니라 **공간군까지** 맞는 다형을 골라 따로 낸다")
    ap.add_argument("--match_from",
                    help="MP 를 다시 조회하지 않고 기존 --out JSON 을 읽어 맞추기만 한다")
    if "--selftest" in __import__("sys").argv:
        raise SystemExit(_selftest())
    args = ap.parse_args()

    rxns = []
    if args.from_reactions:
        for p in args.from_reactions:
            got = reactions_in(p)
            rxns += got
            print(f"[{p}] 반응식 {len(got)}개")
        seen, forms = set(), []
        for _, rx in rxns:
            for f in products_of(rx):
                if f not in seen:
                    seen.add(f); forms.append(f)
        args.formulas = forms
        print(f"고유 산물 조성 {len(forms)}개 → MP 조회")

    # --match_from: MP 를 다시 조회하지 않는다 (키도 필요 없다). 맞추기만 한다.
    if args.match_from:
        if not args.match_spacegroup:
            raise SystemExit("⛔ --match_from 은 --match_spacegroup 과 같이 쓴다")
        src = json.loads(Path(args.match_from).read_text(encoding="utf-8"))
        return _emit_match(src.get("gaps") or src, args.match_spacegroup,
                           args.out, src_path=args.match_from)

    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("Set MP_API_KEY (run on gabia/kserver116).")
    from mp_api.client import MPRester

    rows = {}
    with MPRester(key) as mpr:
        for f in args.formulas:
            try:
                docs = mpr.materials.summary.search(
                    formula=f,
                    fields=["material_id", "formula_pretty",
                            "energy_above_hull", "band_gap", "is_stable",
                            # ⛔ 2026-09-13 — 공간군이 없으면 **어느 다형인지 못 적는다.**
                            #   Li3N 은 α(P6/mmm) 와 β(P6₃/mmc) 가 있고, 갭이 다르다.
                            #   "Li3N gap" 이라고만 쓰면 두 값 중 뭔지 알 수 없다.
                            "symmetry"])
                if not docs:
                    rows[f] = {"error": "no MP entry"}
                    continue
                # pick the ground state (lowest e_above_hull)
                # ⛔⛔ 2026-09-13 — `x.energy_above_hull or 9e9` 였다. **파이썬에서 0.0 은
                #   거짓**이라 `0.0 or 9e9` → 9e9 다. 즉 E_hull == 0 인 **바닥상이 항상
                #   꼴찌로 밀려 한 번도 선택되지 않았다.** 이 파일의 _method 는
                #   "ground-state (lowest e_above_hull) entry" 라고 적혀 있었는데 코드는
                #   정확히 그 반대를 했다. 다형이 하나뿐인 조성만 우연히 맞았다.
                #   실측: Li2O → Pnma(0.084) · Li2S → Pnma(0.062) · LiCl → P6_3mc(0.004) ·
                #        Li3N → P6_3/mmc(β, 0.004)  전부 바닥상이 아니다.
                d = min(docs, key=lambda x: _hull_key(x.energy_above_hull))
                has_nd = "Nd" in f
                rows[f] = {**_row(d), "Nd_bearing_gap_is_LOWER_BOUND": has_nd,
                           "exp_anchor": EXP_ANCHOR.get(f, ""),
                           "selection": "lowest_e_above_hull",
                           "n_polymorphs_in_MP": len(docs)}
                if args.all_polymorphs:
                    # ⛔ 다형을 **전부** 남긴다 — 바닥상만 적으면 "다른 다형은 갭이 다르다" 를
                    #   나중에 확인할 수 없다. 어느 것을 골랐는지는 selection 이 말한다.
                    rows[f]["polymorphs"] = sorted(
                        (_row(x) for x in docs),
                        key=lambda r: (r["e_above_hull"], r["material_id"]))
                tag = "  (Nd: LOWER BOUND)" if has_nd else ""
                print(f"  {f:10s}  {d.formula_pretty:12s}  "
                      f"{rows[f]['spacegroup_symbol']:10s} "
                      f"gap_MP={float(d.band_gap):5.2f} eV  "
                      f"E_hull={float(d.energy_above_hull or 0):.3f}  "
                      f"다형 {len(docs)}개{tag}")
            except Exception as e:
                rows[f] = {"error": str(e)[:160]}
                print(f"  {f:10s}  [error] {str(e)[:80]}")

    # 반응별 병목 = 산물 중 **최소 갭**. 하나라도 금속이면 그 층은 전자를 통과시킨다.
    per_rxn = {}
    for lab, rx in rxns:
        gs = [rows[f]["band_gap_MP_eV"] for f in products_of(rx)
              if isinstance(rows.get(f), dict) and "band_gap_MP_eV" in rows[f]]
        if gs:
            per_rxn[lab] = {"min_product_gap_eV": round(min(gs), 3),
                            "n_products": len(gs),
                            "metallic_product": bool(min(gs) <= 0.01),
                            "reaction": rx}
    Path(args.out).write_text(json.dumps({
        "note": "MP PBE/PBE+U band gaps of decomposition/SEI product phases. "
                "Nd-bearing gaps are lower bounds (4f mis-placement). "
                "Wide gaps => electronically insulating interphase.",
        "caveat": "PBE gaps underestimate systematically - use ORDER, not absolute eV. "
                  "min_product_gap is the bottleneck: one metallic product makes the "
                  "whole interphase electronically leaky (no self-limiting passivation).",
        "gaps": rows,
        "per_reaction": per_rxn,
    }, indent=2))
    if per_rxn:
        leak = sum(1 for v in per_rxn.values() if v["metallic_product"])
        print(f"\n반응 {len(per_rxn)}개 · 금속 산물을 포함하는 반응 **{leak}개** "
              f"({100 * leak / len(per_rxn):.0f} %)")
    print(f"\n-> {args.out}")
    if args.match_spacegroup:
        return _emit_match(rows, args.match_spacegroup,
                           str(args.out).replace(".json", "_matched.json"),
                           src_path=args.out)


if __name__ == "__main__":
    # ⚠ main() 의 반환값을 버리면 "공간군 못 찾음" 이 exit 0 으로 나간다 —
    #   러너·CI 가 성공으로 읽는다 (2026-09-17).
    raise SystemExit(main() or 0)
