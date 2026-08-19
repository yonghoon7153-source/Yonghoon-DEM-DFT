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
           "Li2S", "LiCl", "Li3P", "Li3PS4", "Li2O", "S"]
# rough experimental gaps for the key wide-gap insulators (sanity anchor, eV)
EXP_ANCHOR = {"Li3PO4": "~8 (exp)", "Li2O": "~7.99 (exp)", "LiCl": "~9.4 (exp)",
              "Nd2O3": "~4.7 (exp)", "NdCl3": "~5 (exp)", "NdPO4": "wide (monazite)"}


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
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formulas", nargs="+", default=DEFAULT)
    ap.add_argument("--from_reactions", nargs="+",
                    help="CSV(rxn_* 열) / JSONL(reaction) 에서 산물을 뽑아 쓴다")
    ap.add_argument("--out", default="sei_product_gaps.json")
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
                            "energy_above_hull", "band_gap", "is_stable"])
                if not docs:
                    rows[f] = {"error": "no MP entry"}
                    continue
                # pick the ground state (lowest e_above_hull)
                d = min(docs, key=lambda x: (x.energy_above_hull or 9e9))
                has_nd = "Nd" in f
                rows[f] = {
                    "material_id": str(d.material_id),
                    "formula": d.formula_pretty,
                    "band_gap_MP_eV": round(float(d.band_gap), 3),
                    "e_above_hull": round(float(d.energy_above_hull or 0), 4),
                    "is_stable": bool(d.is_stable),
                    "Nd_bearing_gap_is_LOWER_BOUND": has_nd,
                    "exp_anchor": EXP_ANCHOR.get(f, ""),
                }
                tag = "  (Nd: LOWER BOUND)" if has_nd else ""
                print(f"  {f:10s}  {d.formula_pretty:12s}  "
                      f"gap_MP={float(d.band_gap):5.2f} eV  "
                      f"E_hull={float(d.energy_above_hull or 0):.3f}{tag}")
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


if __name__ == "__main__":
    main()
