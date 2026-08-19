#!/usr/bin/env python3
"""interface_reactivity_v2.py — VOLTAGE-RESOLVED electrolyte/cathode interface
reactivity (Richards/Ong 2016, Chem. Mater. 28, 266), the accurate upgrade of
interface_reactivity.py.

Why this is more accurate than v1
---------------------------------
v1 computed the SE/cathode mutual reaction at OCV (closed system). But the real
degradation happens during CHARGE, where the cathode is delithiated and the
local environment is strongly oxidizing (low mu_Li / high voltage). This tool
opens the system to a Li reservoir (GrandPotentialInterfacialReactivity) and
evaluates the most-exothermic SE/cathode reaction AS A FUNCTION OF the applied
voltage V (vs Li/Li+), via mu_Li = mu_Li(Li metal) - V. At high V the cathode
delithiates automatically, so we capture the charged-state reactivity.

  reaction energy more negative  ==  more reactive interface  ==  worse.

Outputs reaction_energy(V) for each electrolyte x cathode, and the comp1-vs-
modelc difference at each voltage (where they may diverge even though OCV is
identical).

Run on gabia/kserver116-27 (MP_API_KEY set, MP reachable, pymatgen+mp_api):
  python3 interface_reactivity_v2.py \
    --electrolytes "Li6PS5Cl:LPSCl" "Li5.4PS4.4Cl1.6:LPSCl1.6" \
    --cathodes LiCoO2 LiNiO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" \
    --voltages 2.5 3.0 3.5 4.0 4.3 \
    --out interface_reactivity_v2.json
"""
import argparse, json, os
from pathlib import Path


def get_entries(elements):
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    print(f"[mp_api] {len(entries)} entries in {'-'.join(sorted(elements))}")
    return entries


def li_metal_mu(entries):
    from pymatgen.core import Composition
    es = [e.energy_per_atom for e in entries
          if e.composition.reduced_formula == "Li"]
    return min(es)  # Li metal reference (eV/atom)


def min_rxn_grand(c1, c2, gpd, pd):
    from pymatgen.analysis.interface_reactions import GrandPotentialInterfacialReactivity
    gir = GrandPotentialInterfacialReactivity(
        c1, c2, gpd, pd_non_grand=pd,
        include_no_mixing_energy=True, use_hull_energy=True)
    min_e, min_rxn = 1e9, None
    for k in gir.get_kinks():
        e = float(k[2])
        if e < min_e:
            min_e, min_rxn = e, str(k[3])
    return min_e, min_rxn


# ── 캐스케이드 90종 일괄 (2026-08-19 신설) ───────────────────────────────────
#: ⛔ **한 chemsys 에 다 넣으면 안 된다.** 90종의 원소 합집합이 44개라
#:   get_entries_in_chemsys 가 부분 chemsys 를 전부 훑어 사실상 끝나지 않는다.
#:   종마다 따로 (Li,P,S,Cl,O + 그 도펀트 원소 + 상대 물질 원소) 로 돈다.
CASCADE_CSV = "db/properties/cascade_v23_all.csv"
#: MP `get_entries_in_chemsys` 가 받아 주는 원소 수 상한 (실측 2026-08-19:
#:   9원소 Ag-Cl-Co-Li-Mn-Ni-O-P-S 통과 · 10원소 Al-Br-Cl-Co-Li-Mn-Ni-O-P-S 에서
#:   `MPRestError: Please specify fewer elements`). 미리 걸러 MP 호출을 아낀다.
MAX_CHEMSYS = 9


def min_rxn_closed(c1, c2, pd):
    """닫힌계(0 V) 상호 반응 — Li 저장고를 **안 연다**.

    ⛔ 왜 따로 필요한가 (2026-08-19) — 상대가 **순수 Li 금속**이면 grand-potential 은
      정의가 안 된다(정규화 분모 0). Li 음극 쪽은 이 닫힌계 쪽으로 재야 하고,
      그게 Sundar 2025 Fig.2 의 Li-anode 판과 **같은 계산**이다.
    ⚠ 대신 **전압축이 없다.** 두 모드의 숫자를 같은 표에 섞으면 안 된다.
    """
    from pymatgen.analysis.interface_reactions import InterfacialReactivity
    ir = InterfacialReactivity(c1, c2, pd, use_hull_energy=True)
    min_e, min_rxn = 1e9, None
    for k in ir.get_kinks():
        e = float(k[2])
        if e < min_e:
            min_e, min_rxn = e, str(k[3])
    return min_e, min_rxn


def why_skip(e_formula, c_formula, open_elements=("Li",), closed=False):
    """이 (전해질, 상대) 쌍을 **돌리기 전에** 막아야 하는 이유. 없으면 None.

    ⛔ 왜 필요한가 (2026-08-19 실측) — 두 실패가 조용하지 않게 하려고.
      ① 상대가 **순수 Li 금속**이면 grand-potential 이 정의되지 않는다.
         pymatgen 이 `grand_potential /= sum(comp[el] for el in comp
         if el not in chempots)` 로 정규화하는데, Li 저장고를 열어 두면 분모가 0 이라
         ZeroDivisionError 가 난다. **Li 음극 쪽은 닫힌계(0 V) InterfacialReactivity**
         로 따로 재야 한다 — 이 도구의 일이 아니다.
      ② chemsys 가 MAX_CHEMSYS 를 넘으면 MP 가 거절한다. NCM811 처럼 전이금속을
         셋 얹는 상대가 그렇다 → **LiCoO2 · LiNiO2 · LiMn2O4 처럼 하나씩** 쓴다.
    """
    from pymatgen.core import Composition
    cc = Composition(c_formula)
    rest = [el.symbol for el in cc.elements if el.symbol not in open_elements]
    if not rest and not closed:
        return ("상대가 순수 " + "/".join(open_elements) +
                " 이라 grand-potential 이 정의되지 않는다 "
                "(정규화 분모 0). 닫힌계 0 V InterfacialReactivity 로 따로 잴 것")
    n = len(set(el.symbol for el in Composition(e_formula).elements)
            | set(el.symbol for el in cc.elements) | set(open_elements))
    if n > MAX_CHEMSYS:
        return f"chemsys {n} 원소 > {MAX_CHEMSYS} — MP 가 거절한다 (상대를 단일 전이금속으로)"
    return None


def champion_formulas(csv_path):
    """rank_combined==1 행에서 **종당 하나**의 조성식을 만든다.

    이 함수가 **못 하는 것**: 어느 라벨(x020/x050/x100)의 챔피언인지 고르지 않는다 —
      먼저 나온 것을 쓴다. 세 라벨은 실제 농도가 전부 0.25 로 같으므로 조성 자체는
      비슷하나 **자리·시드가 다르다** (kb/results/site_preference_bar_meaning_2026_08_18.md).
    """
    import csv as _csv, io as _io, os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "cascade"))
    from cascade_ids import base_species
    rows = [r for r in _csv.DictReader(_io.open(csv_path, encoding="utf-8"))
            if r.get("rank_combined") == "1"]
    if not rows:
        return {}
    cols = [c for c in rows[0] if c.startswith("composition_")]
    out = {}
    for r in rows:
        sp = base_species(r["dopant"])
        if sp in out:
            continue
        parts = []
        for c in cols:
            v = r.get(c)
            if v in ("", None):
                continue
            try:
                n = float(v)
            except ValueError:
                continue
            if n > 0:
                parts.append(f"{c.split('_')[1]}{n:g}")
        if parts:
            out[sp] = "".join(parts)
    return out


def run_batch(a):
    """종마다 자기 chemsys 로 계면 반응성을 잰다. JSONL 이라 **이어달리기 가능**."""
    import time
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram

    forms = champion_formulas(a.batch_from)
    out = Path(a.out if a.out.endswith(".jsonl") else a.out + "l")
    done = set()
    if a.resume and out.exists():
        for ln in out.read_text().splitlines():
            try:
                done.add((json.loads(ln)["species"], json.loads(ln)["cathode"]))
            except Exception:
                pass
        print(f"[resume] 이미 끝난 (종,상대) 쌍 {len(done)}개는 건너뛴다")

    todo = sorted(forms)[: a.limit] if a.limit else sorted(forms)
    print(f"종 {len(todo)}개 x 상대 {len(a.cathodes)}개 = {len(todo) * len(a.cathodes)} 쌍")
    for i, sp in enumerate(todo, 1):
        for cat in a.cathodes:
            cstr, _, clab = cat.partition(":")
            clab = clab or cstr
            if (sp, clab) in done:
                continue
            t0 = time.time()
            skip = why_skip(forms[sp], cstr, closed=a.closed)
            if skip:
                rec = {"species": sp, "cathode": clab, "skipped": skip, "seconds": 0.0}
                with out.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"[{i}/{len(todo)}] {sp:10s} vs {clab:8s} SKIP {skip[:56]}")
                continue
            try:
                elems = set(Composition(forms[sp]).elements) | set(Composition(cstr).elements)
                elems.add(Element("Li"))
                chem = sorted(e.symbol for e in elems)
                entries = get_entries(chem)
                pd = PhaseDiagram(entries)
                mu0 = li_metal_mu(entries)
                rec = {"species": sp, "formula": forms[sp], "cathode": clab,
                       "cathode_formula": cstr, "chemsys": chem,
                       "mode": "closed_0V" if a.closed else "grand_potential",
                       "mu_Li_metal_eV": round(mu0, 4)}
                if a.closed:
                    e, rxn = min_rxn_closed(Composition(forms[sp]), Composition(cstr), pd)
                    rec["dE_eV_per_atom"] = round(e, 5)
                    rec["reaction"] = rxn
                else:
                    rec["by_voltage"] = {}
                    for V in a.voltages:
                        gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu0 - V})
                        e, rxn = min_rxn_grand(Composition(forms[sp]), Composition(cstr), gpd, pd)
                        rec["by_voltage"][f"{V:.2f}"] = {"dE_eV_per_atom": round(e, 5),
                                                         "reaction": rxn}
                rec["seconds"] = round(time.time() - t0, 1)
            except Exception as ex:
                rec = {"species": sp, "cathode": clab, "error": f"{type(ex).__name__}: {ex}",
                       "seconds": round(time.time() - t0, 1)}
            with out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if "error" in rec:
                bad = "ERR " + rec["error"][:40]
            elif "dE_eV_per_atom" in rec:
                bad = "%+.4f (0 V)" % rec["dE_eV_per_atom"]
            else:
                bad = "%+.4f" % min(v["dE_eV_per_atom"] for v in rec["by_voltage"].values())
            print(f"[{i}/{len(todo)}] {sp:10s} vs {clab:8s} {bad}  ({rec['seconds']:.0f}s)")
    print(f"\n→ {out}")


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    import tempfile, os as _os
    root = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    csvp = _os.path.join(root, CASCADE_CSV)
    if _os.path.exists(csvp):
        f = champion_formulas(csvp)
        chk(len(f) == 90, f"[양성] 챔피언 조성 90종 (얻은 것 {len(f)})")
        chk(all(("Li" in v and "P" in v and "S" in v) for v in f.values()),
            "[양성] 모든 조성에 host 원소 Li·P·S 가 있다")
        chk("Ag2O" in f and "O1" in f["Ag2O"],
            f"[양성] Ag2O 챔피언에 O 가 있다 ({f.get('Ag2O')})")
    else:
        chk(False, f"[전제] {CASCADE_CSV} 가 있어야 한다")
    # ── why_skip: 두 실패를 **돌리기 전에** 막는가 ────────────────────────
    try:
        chk(why_skip("Li6PS5Cl", "LiCoO2") is None,
            "[양성] LCO 는 통과 (chemsys 7)")
        chk("순수" in (why_skip("Li6PS5Cl", "Li") or ""),
            "[음성] 순수 Li 상대는 막는다 (ZeroDivisionError 예방)")
        chk(why_skip("Li6PS5Cl", "Li", closed=True) is None,
            "[양성] --closed 면 순수 Li 도 통과 (닫힌계엔 그 문제가 없다)")
        chk("chemsys" in (why_skip("Cl4Li21P4S17Al1Br3", "LiNi0.8Co0.1Mn0.1O2") or ""),
            "[음성] 10원소 NCM811 조합은 막는다 (MPRestError 예방)")
        chk(why_skip("Cl4Li21P4S17Al1Br3", "LiNiO2") is None,
            "[양성] 같은 종도 단일 전이금속 상대면 통과")
    except ImportError:
        print("  ⚠ pymatgen 없음 — why_skip 시험 건너뜀 (여기선 정상)")
    with tempfile.TemporaryDirectory() as d:
        p = _os.path.join(d, "empty.csv")
        open(p, "w").write("dopant,rank_combined\nMgO,2\n")
        chk(champion_formulas(p) == {},
            "[음성] rank_combined==1 이 없으면 빈 dict (엉뚱한 조성을 만들지 않는다)")
        p2 = _os.path.join(d, "nocomp.csv")
        open(p2, "w").write("dopant,rank_combined\nMgO,1\n")
        chk(champion_formulas(p2) == {},
            "[음성] composition_* 열이 없으면 빈 dict")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolytes", nargs="+",
                    help='comp:label, e.g. "Li6PS5Cl:LPSCl"')
    ap.add_argument("--batch_from", nargs="?", const=CASCADE_CSV,
                    help="캐스케이드 CSV 에서 90종 챔피언을 읽어 **종마다 따로** 돈다")
    ap.add_argument("--resume", action="store_true", help="JSONL 에 이미 있는 쌍은 건너뛴다")
    ap.add_argument("--limit", type=int, help="앞 N 종만 (시범용)")
    ap.add_argument("--closed", action="store_true",
                    help="닫힌계 0 V (Li 저장고 안 엶) — **Li 음극 쪽은 이걸 써야 한다**")
    ap.add_argument("--cathodes", nargs="+", default=["LiCoO2", "LiNiO2"],
                    help='comp[:label] cathodes')
    ap.add_argument("--voltages", nargs="+", type=float,
                    default=[2.5, 3.0, 3.5, 4.0, 4.3])
    ap.add_argument("--out", default="interface_reactivity_v2.json")
    if "--selftest" in __import__("sys").argv:
        raise SystemExit(_selftest())
    a = ap.parse_args()
    if a.batch_from:
        return run_batch(a)
    if not a.electrolytes:
        ap.error("--electrolytes 또는 --batch_from 중 하나는 있어야 한다")

    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram

    elems = set()
    for s in a.electrolytes + a.cathodes:
        elems |= set(Composition(s.split(":")[0]).elements)
    elems.add(Element("Li"))
    elements = sorted(e.symbol for e in elems)
    print("chemsys =", elements)
    entries = get_entries(elements)
    pd = PhaseDiagram(entries)
    mu0 = li_metal_mu(entries)
    print(f"mu_Li(metal) = {mu0:.4f} eV/atom")

    results = {}
    for cat in a.cathodes:
        cstr, _, clab = cat.partition(":"); clab = clab or cstr
        cc = Composition(cstr)
        results[clab] = {"composition": cstr, "by_voltage": {}}
        print(f"\n######## cathode {clab} ({cstr}) ########")
        for V in a.voltages:
            mu = mu0 - V
            gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu})
            row = {}
            for spec in a.electrolytes:
                estr, _, elab = spec.partition(":"); elab = elab or estr
                try:
                    e, rxn = min_rxn_grand(Composition(estr), cc, gpd, pd)
                    row[elab] = round(e, 5)
                    print(f"  V={V:.2f}  {elab:9s}: {e:.4f} eV/atom")
                except Exception as ex:
                    row[elab] = None
                    print(f"  V={V:.2f}  {elab}: ERR {type(ex).__name__}: {ex}")
            results[clab]["by_voltage"][f"{V:.2f}"] = row

    Path(a.out).write_text(json.dumps({
        "method": "GrandPotentialInterfacialReactivity (Richards/Ong 2016), "
                  "open to Li reservoir; mu_Li = mu_Li(metal) - V; "
                  "use_hull_energy=True; MP GGA_GGA+U. More negative = more "
                  "reactive interface at that voltage.",
        "mu_Li_metal_eV": round(mu0, 4),
        "voltages_V": a.voltages,
        "results": results,
    }, indent=2))
    print(f"\n→ {a.out}")


if __name__ == "__main__":
    main()
