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
import argparse, json, os, re
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


#: 최소 kink 의 x 가 이 안쪽으로 끝점(0 또는 1)에 붙으면 **섞이지 않은 것**으로 본다.
ENDPOINT_TOL = 1e-6


def is_endpoint(x, tol=ENDPOINT_TOL):
    """최소 kink 가 x=0/1 끝점인가 — **두 상이 안 섞였다**는 뜻이다.

    ⛔⛔ **끝점의 뜻은 모드마다 다르다. 한 덩이로 읽으면 틀린다** (2026-09-16 실측).
      · **닫힌계** (`min_rxn_closed`, `use_hull_energy=True`): 반응물을 hull 에너지로
        재므로 끝점 값은 **구성상 정확히 0** 이다. 그래서 *끝점 = 섞어도 hull 밑으로
        안 내려간다 = **상호반응 없음*** 이라는 **정상적이고 의미 있는 판정**이다.
        찍히는 반응식은 그 끝점 상의 **자기 hull 분해**라 좌변에 상대가 없다 — 표시 부작용.
      · **열린계** (`min_rxn_grand`, `include_no_mixing_energy=True`): 끝점 값이 0 이
        아니다. 순수상의 **grand-potential 자체 분해 에너지**가 그 자리에 들어간다.
        그래서 끝점이면 그 숫자는 **계면량이 아니다** — 상대를 한 번도 안 본 값이다.
      실측: 산물 6 종(NdP₅O₁₄·Nd(PO₃)₃·Nd₂(SO₄)₃·NdCl₃·Li₃PO₄·LiPO₃)을 상대로 LPSCl1.6 을
      3.5–4.3 V 열린계로 돌렸더니 **여섯 다 같은 숫자**(−0.6535 / −1.0392 / −1.2706)가 나왔고
      반응식 좌변에 상대가 **없었다**. 전해질 혼자 분해되는 에너지를 여섯 번 다시 잰 것이다.
      오류는 안 났고 값은 그럴듯했다 — 전형적인 조용히 틀린 경로.
      (열린계에서 상대가 **이미 산화가 끝난 안정한 인산염**이면 어떤 혼합도 SE 자체 분해보다
       덜 음수라 최소가 항상 끝점으로 간다. §B 처럼 상대가 **환원 가능한 양극**일 땐 안 그렇다.)
    ⚠ 이 함수가 **안 하는 것**: ① 끝점이 c1 쪽인지 c2 쪽인지 구분하지 않는다 — 판정이 같다.
      ② 모드를 모른다. 뜻풀이는 `endpoint_meaning()` 이 한다. ③ 값을 버리지 않는다 —
      깃발만 단다 (조용히 버리면 "왜 안 나오지" 가 된다).
    """
    if x is None:
        return False
    return float(x) <= tol or float(x) >= 1.0 - tol


def endpoint_meaning(closed):
    """끝점 깃발의 **뜻풀이 문자열** — 기록에 같이 박아 다음 사람이 모드를 안 헷갈리게."""
    if closed:
        return ("끝점(x=0/1) — 닫힌계라 **상호반응 없음**이라는 정상 판정이다 "
                "(use_hull_energy 로 끝점 값은 구성상 0). 반응식 좌변에 상대가 없는 것은 "
                "그 상의 자기 hull 분해가 찍힌 표시 부작용이다.")
    return ("⛔ 끝점(x=0/1) — 열린계에서는 이 숫자가 **계면량이 아니다**. 순수상의 "
            "grand-potential 자체 분해 에너지이고, 상대는 계산에 들어가지 않았다. "
            "호환성 판정에 쓰지 말 것. 산물 인구조사에서도 뺀다.")


def min_rxn_grand(c1, c2, gpd, pd, want_kinks=False):
    """최소 kink 의 (에너지, 반응식, x). `want_kinks` 면 **전 kink** 도 같이 준다.

    ⛔ 2026-09-16 — 종전 판은 `get_kinks()` 를 돌면서 **최소만 남기고 나머지를 버렸다.**
      그래서 Richards/Ong 논문식 *"반응에너지 vs x"* 곡선(LiPOF Fig. 1b–f 형태)을
      그릴 수 없었다. 계산은 이미 다 해 놓고 결과만 버린 것이다.
    ⚠ 이 함수가 못 하는 것: kink 의 x 가 **원자분율**인지 몰분율인지 판정하지 않는다 —
      pymatgen 이 주는 값을 그대로 옮긴다 (`x_atomic_frac` 로 이름 붙인 v1 관례를 따른다).
    ⚠ 반환하는 `min_x` 는 **호출부가 `is_endpoint()` 로 봐야** 의미가 생긴다. 이 값을 읽는
      게이트는 `run_batch`(`endpoint_degenerate` 기록) 와 `product_census`(대상에서 제외)다.
    """
    from pymatgen.analysis.interface_reactions import GrandPotentialInterfacialReactivity
    gir = GrandPotentialInterfacialReactivity(
        c1, c2, gpd, pd_non_grand=pd,
        include_no_mixing_energy=True, use_hull_energy=True)
    min_e, min_rxn, min_x, kinks = 1e9, None, None, []
    for k in gir.get_kinks():
        e = float(k[2])
        if want_kinks:
            kinks.append({"x_atomic_frac": round(float(k[1]), 6),
                          "reaction_energy_eV_per_atom": round(e, 6),
                          "reaction": str(k[3])})
        if e < min_e:
            min_e, min_rxn, min_x = e, str(k[3]), float(k[1])
    return (min_e, min_rxn, min_x, kinks) if want_kinks else (min_e, min_rxn, min_x)


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
    ⚠ 세 번째 반환값 `min_x` 는 `is_endpoint()` 로 봐야 뜻이 생긴다 — 여기선 끝점이
      **정상 판정**("상호반응 없음")이다. `endpoint_meaning(closed=True)` 참조.
    """
    from pymatgen.analysis.interface_reactions import InterfacialReactivity
    ir = InterfacialReactivity(c1, c2, pd, use_hull_energy=True)
    min_e, min_rxn, min_x = 1e9, None, None
    for k in ir.get_kinks():
        e = float(k[2])
        if e < min_e:
            min_e, min_rxn, min_x = e, str(k[3]), float(k[1])
    return min_e, min_rxn, min_x


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

    forms = champion_formulas(a.batch_from) if a.batch_from is not True else {}
    if a.only:
        # 기준선용 — 캐스케이드 밖의 조성을 같은 기계로 돌린다 (resume·차단 그대로).
        forms = {}
        for spec in a.only:
            lab, _, f = spec.partition(":")
            forms[lab] = f or lab
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
                    e, rxn, x = min_rxn_closed(Composition(forms[sp]), Composition(cstr), pd)
                    rec["dE_eV_per_atom"] = round(e, 5)
                    rec["reaction"] = rxn
                    rec["mixing_x"] = None if x is None else round(x, 6)
                    rec["min_kink_at_endpoint"] = is_endpoint(x)
                    if rec["min_kink_at_endpoint"]:
                        rec["endpoint_meaning"] = endpoint_meaning(True)
                else:
                    rec["by_voltage"] = {}
                    for V in a.voltages:
                        gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu0 - V})
                        e, rxn, x = min_rxn_grand(Composition(forms[sp]), Composition(cstr),
                                                  gpd, pd)
                        cell = {"dE_eV_per_atom": round(e, 5), "reaction": rxn,
                                "mixing_x": None if x is None else round(x, 6),
                                "min_kink_at_endpoint": is_endpoint(x)}
                        if cell["min_kink_at_endpoint"]:
                            cell["endpoint_meaning"] = endpoint_meaning(False)
                        rec["by_voltage"][f"{V:.2f}"] = cell
                rec["seconds"] = round(time.time() - t0, 1)
            except Exception as ex:
                rec = {"species": sp, "cathode": clab, "error": f"{type(ex).__name__}: {ex}",
                       "seconds": round(time.time() - t0, 1)}
            with out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if "error" in rec:
                bad = "ERR " + rec["error"][:40]
            elif "dE_eV_per_atom" in rec:
                # 닫힌계 끝점 = **상호반응 없음**이라는 정상 판정 → 조용한 표시
                bad = "%+.4f (0 V)%s" % (rec["dE_eV_per_atom"],
                                         "  [끝점 = 반응없음]"
                                         if rec.get("min_kink_at_endpoint") else "")
            else:
                bad = "%+.4f" % min(v["dE_eV_per_atom"] for v in rec["by_voltage"].values())
                # 열린계 끝점 = **계면을 안 쟀다** → 시끄럽게
                ne = sum(1 for v in rec["by_voltage"].values()
                         if v.get("min_kink_at_endpoint"))
                if ne:
                    bad += f"  ⛔끝점 {ne}/{len(rec['by_voltage'])} — 계면량 아님(자체분해)"
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
    # ⛔음성 (2026-09-16 실측 사고) — `--closed --electrolytes` 는 **조용히 무시됐다.**
    #   오류도 경고도 없이 열린계를 돌리고 전압 쓸이가 찍힌 출력을 냈다. 7 종을 그렇게
    #   돌려 놓고 전압줄을 보고서야 알아챘다. 이제 **시작을 막는다.**
    import subprocess as _sp
    import sys as _sys
    _r = _sp.run([_sys.executable, __file__, "--closed",
                  "--electrolytes", "Li6PS5Cl:x", "--cathodes", "LiCoO2"],
                 capture_output=True, text=True)
    chk(_r.returncode != 0 and "구현돼" in (_r.stderr + _r.stdout),
        "[음성] `--closed --electrolytes` 는 **조용히 돌지 않고 거절한다** "
        f"(rc={_r.returncode})")
    chk("--only" in (_r.stderr + _r.stdout),
        "[음성] 거절하면서 **대안 경로(--only)를 알려 준다** — 막기만 하면 사람이 헤맨다")
    with tempfile.TemporaryDirectory() as d:
        p = _os.path.join(d, "empty.csv")
        open(p, "w").write("dopant,rank_combined\nMgO,2\n")
        chk(champion_formulas(p) == {},
            "[음성] rank_combined==1 이 없으면 빈 dict (엉뚱한 조성을 만들지 않는다)")
        p2 = _os.path.join(d, "nocomp.csv")
        open(p2, "w").write("dopant,rank_combined\nMgO,1\n")
        chk(champion_formulas(p2) == {},
            "[음성] composition_* 열이 없으면 빈 dict")
    # ── 산물 파서·인구조사 (2026-09-16 신설) ────────────────────────────────
    #   왜: 종전 판이 `min_rxn` 을 계산해 놓고 **버렸다**. 숫자만 남아 갭 단계(§C)의
    #   입력을 JSON 에서 못 읽었는데, 화면에는 찍혀서 '되는 것처럼' 보였다.
    def chk(c, n):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + n)
        ok = ok and bool(c)

    chk(rhs_products("0.74 A + 0.26 B -> 0.08247 Co9S8 + 0.1134 Li2SO4 + LiCl")
        == ["Co9S8", "Li2SO4", "LiCl"], "산물 파서: 계수를 떼고 산물만")
    chk(rhs_products("A -> 1.5e-2 P2S7") == ["P2S7"], "산물 파서: 지수 계수")
    chk(rhs_products("A -> LiCl + 2 Li2S") == ["LiCl", "Li2S"], "산물 파서: 계수 없는 항")
    chk(rhs_products("LiCoO2 + Li6PS5Cl") == [], "[음성] `->` 가 없으면 빈 목록 (왼쪽을 산물로 삼지 않는다)")
    chk(rhs_products(None) == [] and rhs_products(123) == [], "[음성] 문자열이 아니면 죽지 않고 빈 목록")
    chk(rhs_products("A ->") == [], "[음성] 오른쪽이 비면 빈 목록")
    _r = {"C": {"reactions": {"4.30": {"m": "x -> 0.1 Co9S8 + LiCl", "c": "x -> LiCl"}}}}
    _c = product_census(_r)
    chk(_c["n_unique"] == 2 and _c["counts"]["LiCl"] == 2, "인구조사: 중복을 센다")
    chk(_c["first_seen"]["Co9S8"] == "C@4.30V/m", "인구조사: 처음 나온 곳을 기록한다")
    chk(product_census({})["n_unique"] == 0 and product_census(None)["n_unique"] == 0,
        "[음성] 빈 입력에 죽지 않는다")
    chk(product_census({"C": {"by_voltage": {"4.30": {"m": -1.0}}}})["n_unique"] == 0,
        "[음성] `reactions` 가 없으면 0 — 숫자만 있는 옛 JSON 을 산물로 지어내지 않는다")
    _lr = {"C": {"reactions": {"4.30": {"m": "x -> 6 Li + SCl"}}}}
    _lc = product_census(_lr)
    chk("Li" not in _lc["counts"] and _lc["reservoir_excluded"].get("Li") == 1,
        "[음성] 열린 원소 홑원소(Li)를 산물로 세지 않는다 — 저장소 회계다")
    chk(_lc["counts"].get("SCl") == 1, "같은 반응의 진짜 산물은 센다")
    chk(product_census(_lr, open_elements=())["counts"].get("Li") == 1,
        "[음성] open_elements 를 비우면 Li 도 센다 (제외가 인자로 제어된다)")
    # ── 끝점 퇴화 (2026-09-16 신설) ─────────────────────────────────────────
    #   왜: dual-compat 실행에서 열린계 최소 kink 가 여섯 상대 **전부** x=0 에 걸려
    #   전해질 자체분해 산물(PCl₅·P₂S₇·SCl)이 48 회씩 §C 후보로 올라왔다. 값은
    #   그럴듯했고 오류도 안 났다 — 조용히 틀린 경로.
    chk(is_endpoint(0.0) and is_endpoint(1.0), "끝점 판정: x=0·x=1 을 잡는다")
    chk(not is_endpoint(0.5) and not is_endpoint(0.0001),
        "[음성] 안쪽 x 는 끝점이 아니다 (0.0001 도 통과시키면 진짜 계면을 버린다)")
    chk(not is_endpoint(None), "[음성] x 가 None 이면 깃발을 세우지 않는다 (모르는 것 ≠ 퇴화)")
    chk("계면량이 아니다" in endpoint_meaning(False)
        and "상호반응 없음" in endpoint_meaning(True),
        "뜻풀이가 모드마다 다르다 — 닫힌계 끝점은 정상 판정, 열린계 끝점은 무효")
    _dr = {"C": {"reactions": {"3.50": {"m": "x -> PCl5 + SCl", "c": "x -> LiCl"}},
                 "endpoint_degenerate": {"3.50": {"m": True, "c": False}}}}
    _dc = product_census(_dr)
    chk("PCl5" not in _dc["counts"] and "SCl" not in _dc["counts"],
        "[음성] 끝점 퇴화 칸의 산물은 **세지 않는다** (자체분해라 계면 산물이 아니다)")
    chk(_dc["counts"].get("LiCl") == 1,
        "같은 전압의 퇴화 아닌 칸은 그대로 센다 (통째로 버리지 않는다)")
    chk(_dc["endpoint_degenerate_excluded"] == ["C@3.50V/m"],
        "뺀 칸을 **이름으로 남긴다** — 조용히 버리면 '왜 안 나오지' 가 된다")
    chk(product_census({"C": {"reactions": {"3.50": {"m": "x -> PCl5"}}}})
        ["counts"].get("PCl5") == 1,
        "[하위호환] endpoint_degenerate 필드가 없는 옛 JSON 은 전부 유효로 센다")
    chk("Li2S" in product_census({"C": {"reactions": {"0": {"m": "x -> Li2S"}}}})["counts"],
        "[음성] Li 화합물은 홑원소가 아니므로 남는다 (Li2S 를 Li 로 오인하지 않는다)")

    # ── parse_formula / p_host_ladder (2026-09-17) ──────────────────────────
    chk(parse_formula("Li3PO4") == {"Li": 3.0, "P": 1.0, "O": 4.0},
        "간단한 식을 센다")
    chk(parse_formula("LiNd(PO3)4")["P"] == 4.0
        and parse_formula("LiNd(PO3)4")["O"] == 12.0,
        "[음성] 괄호를 편다 — LiNd(PO3)4 는 P 4·O 12 다 (안 펴면 P 1 로 보인다)")
    chk(parse_formula("LiNd(PO3)4")["Li"] / parse_formula("LiNd(PO3)4")["P"] == 0.25,
        "[음성] 그래서 Li/P 가 1 이 아니라 0.25 다 (2026-09-17 실제 오독)")
    chk(parse_formula("Ni(PO3)2")["P"] == 2.0,
        "괄호 곱수가 안쪽 원소 전부에 걸린다 (Ni(PO3)2 → P 2)")
    chk("Li" not in parse_formula("Ni(PO3)2"),
        "[음성] 없는 원소를 0 으로 만들어 넣지 않는다 (키 자체가 없다)")
    chk(parse_formula("Co9S8") == {"Co": 9.0, "S": 8.0},
        "두 자리 원소기호를 한 글자로 쪼개지 않는다")

    import tempfile as _tf, os as _os
    _hdr = "cathode,electrolyte,voltage_V,x_atomic_frac,is_minimum,reaction\n"
    _body = ("LiCoO2,m,2.5,0.5,1,a -> 0.3 Li3PO4 + 0.7 CoS2\n"
             "LiCoO2,m,4.5,0.5,1,a -> 0.1 CoP4O11 + 0.5 P2S7\n"
             "LiCoO2,m,4.5,1.0,1,a -> 0.5 PCl5\n"            # 끝점 — 빠져야 한다
             "LiCoO2,m,3.0,0.5,0,a -> 9 Li3PO4\n")           # 최소 아님 — 빠져야 한다
    _fd, _pth = _tf.mkstemp(suffix=".csv"); _os.close(_fd)
    Path(_pth).write_text(_hdr + _body, encoding="utf-8")
    _L = p_host_ladder(_pth)
    _os.unlink(_pth)
    chk(_L["n_conditions"] == 2,
        "[음성] is_minimum 이 거짓인 행과 끝점 행은 세지 않는다")
    chk(_L["endpoint_excluded"] == ["m@4.5V/LiCoO2"],
        "[음성] 뺀 끝점을 이름으로 남긴다 (조용히 버리지 않는다)")
    chk(_L["by_electrolyte_voltage"]["m@2.5"]["rung_max"] == 3.0
        and _L["by_electrolyte_voltage"]["m@4.5"]["rung_max"] == 0.0,
        "사다리 칸(max Li/P) 이 전압과 함께 내려간다")
    chk(_L["by_electrolyte_voltage"]["m@4.5"]["cathodes_with_P_S_host"] == ["LiCoO2"]
        and _L["by_electrolyte_voltage"]["m@2.5"]["cathodes_with_P_S_host"] == [],
        "[음성] P-S 수용상(P2S7)이 있는 칸만 표시한다 — 인산염만 있는 칸은 비운다")
    chk(all(h["anion"] == "P-O" for d in _L["rows"] for h in d["p_hosts"]
            if h["formula"] in ("Li3PO4", "CoP4O11")),
        "P-O / P-S 구분이 실제로 붙는다")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1



def rhs_products(rxn: str) -> list:
    """반응식 문자열 → **오른쪽(산물) 화학식 목록**. 계수는 버린다.

    예: `0.74 LiCoO2 + 0.26 Li6PS5Cl -> 0.08 Co9S8 + 0.11 Li2SO4` → ['Co9S8','Li2SO4']

    ⛔ 이 함수가 못 하는 것
      · 화학식이 유효한지 확인하지 않는다 (pymatgen 에 안 물어본다). 문자열을 자를 뿐이다.
      · `->` 가 없으면 **빈 목록**을 준다 — 추측해서 왼쪽을 산물로 삼지 않는다.
    """
    if not isinstance(rxn, str) or "->" not in rxn:
        return []
    out = []
    for term in rxn.split("->", 1)[1].split("+"):
        t = term.strip()
        if not t:
            continue
        # 앞에 붙은 계수(숫자/소수/지수)를 떼어 낸다. 없으면 그대로.
        m = re.match(r"^[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?\s+(.+)$", t)
        out.append((m.group(1) if m else t).strip())
    return [x for x in out if x]


def product_census(results: dict, open_elements=("Li",)) -> dict:
    """모든 (양극, 전압, 전해질) 의 **최소 kink 반응**에 나온 산물을 센다.

    이것이 갭 단계(§C)의 대상 목록이다 — 카드 G2 의 선별 규칙
    (*"각 조합의 최소 반응E kink 에 등장하는 산물만"*) 을 그대로 구현한다.

    ⛔ **열린 원소(기본 Li)의 홑원소는 산물이 아니다** (2026-09-16 정정).
      grand-potential 은 Li 를 저장소로 빼는 회계를 우변에 `6 Li` 처럼 쓴다.
      그건 **상(phase)이 아니라 전기화학 장부**다. 첫 판이 이걸 세서 `Li` 가 96 회로
      1위였고, 갭 대상 목록이 그만큼 부풀었다. `reservoir` 에 따로 담아 **보이되
      대상에서 뺀다** — 조용히 버리면 "왜 안 나오지" 가 된다.
    ⛔ **끝점 퇴화 칸은 센서스에서 뺀다** (2026-09-16 정정). 열린계 최소 kink 가 x=0/1 이면
      그 반응식은 **전해질이 혼자 분해된 것**이고 상대는 계산에 들어가지도 않았다 — 계면
      산물이 아니다. 첫 판이 이걸 세서 dual-compat 실행에서 PCl₅·P₂S₇·SCl 이 48 회씩,
      `처음 나온 곳 Li3PO4@3.50V/LPSCl1.6` 이라는 **거짓 꼬리표**를 달고 §C 후보로 올라왔다.
      `results[cathode]["endpoint_degenerate"][V][electrolyte]` 를 읽어 거른다 —
      **이 필드를 읽는 게이트가 여기다** (없으면 전부 유효로 보는 하위호환).
    ⚠ 이 함수가 **안 하는 것**: 기체·홑원소(S·SO₂·PCl₅ 등)를 가려내지 않는다.
      그건 화학 판단이라 사람·카드 몫이다. 세어서 보여줄 뿐이다.
    """
    opens = {str(x) for x in (open_elements or ())}
    cnt, where, reservoir, skipped = {}, {}, {}, []
    for clab, cd in (results or {}).items():
        deg = cd.get("endpoint_degenerate") or {}
        for V, row in (cd.get("reactions") or {}).items():
            for elab, rxn in (row or {}).items():
                if (deg.get(V) or {}).get(elab):        # 끝점 퇴화 — 계면 산물 아님
                    skipped.append(f"{clab}@{V}V/{elab}")
                    continue
                for f in rhs_products(rxn):
                    if f in opens:                      # 저장소 회계 — 산물 아님
                        reservoir[f] = reservoir.get(f, 0) + 1
                        continue
                    cnt[f] = cnt.get(f, 0) + 1
                    where.setdefault(f, set()).add(f"{clab}@{V}V/{elab}")
    return {"n_unique": len(cnt),
            "counts": dict(sorted(cnt.items(), key=lambda kv: -kv[1])),
            "first_seen": {k: sorted(v)[0] for k, v in where.items()},
            "reservoir_excluded": reservoir,
            "endpoint_degenerate_excluded": sorted(skipped),
            "⛔": "열린 원소의 홑원소는 저장소 회계라 대상에서 뺐다 (reservoir_excluded). "
                 "끝점 퇴화 칸(상대가 계산에 안 들어간 자체분해)도 뺐다 "
                 "(endpoint_degenerate_excluded). "
                 "기체·홑원소(S·SO₂ 등)는 **안 걸렀다** — 화학 판단은 카드·사람 몫이다."}


def parse_formula(f: str) -> dict:
    """화학식 → {원소: 개수}. **괄호를 편다** (`LiNd(PO3)4` → P 4, O 12).

    ⛔ 이 함수가 못 하는 것
      · 화학식이 실재하는지 모른다 — 문자열을 셀 뿐이다.
      · 수화물 점표기(`CaSO4.2H2O`)·전하(`SO4^2-`)·동위원소는 안 읽는다.
      · 닫는 괄호가 모자라면 **거기서 끝난 것으로 본다** (예외를 안 낸다).
    ⚠ 괄호를 안 펴면 `LiNd(PO3)4` 가 P 1·Li/P 1 로 보인다(참값 P 4·Li/P 0.25).
      2026-09-17 에 이 버그로 Li 예산 사다리를 한 칸 틀리게 찍었다.
    """
    def blk(s, i):
        c = {}
        def add(el, n):
            c[el] = c.get(el, 0.0) + n
        while i < len(s):
            ch = s[i]
            if ch == "(":
                sub, i = blk(s, i + 1)
                n = re.match(r"[0-9]*\.?[0-9]*", s[i:]).group(0)
                i += len(n)
                k = float(n) if n else 1.0
                for el, v in sub.items():
                    add(el, v * k)
            elif ch == ")":
                return c, i + 1
            elif ch.isupper():
                el = re.match(r"[A-Z][a-z]?", s[i:]).group(0)
                i += len(el)
                n = re.match(r"[0-9]*\.?[0-9]*", s[i:]).group(0)
                i += len(n)
                add(el, float(n) if n else 1.0)
            else:
                i += 1
        return c, i
    return blk(f or "", 0)[0]


def p_host_ladder(csv_path, p_element="P", ladder_element="Li"):
    """최소 kink 반응의 **P 를 받은 상**과 그 Li:P 를 (전해질, 전압, 양극) 별로 뽑는다.

    §2 가설 카드의 1·2·4 번(*"저전압엔 P 가 PS4 에 갇혀 있다가 전압이 오르며 풀려나고,
    풀려난 양이 늘어 Nd 이득이 커진다"*)을 **산물로 직접 검사**하는 자리다.
    공급(풀려난 P 의 양)이 느는지, 아니면 **받아 줄 방의 Li 값이 내려가는지**를 가른다.

    입력은 `cei_x_scan_panels.csv` 꼴 — cathode·electrolyte·voltage_V·x_atomic_frac·
    is_minimum·reaction 열. `is_minimum` 이 참인 행만 본다.

    rung = 그 조건에서 **P 를 받은 상 중 Li/P 가 가장 큰 값** = 아직 살아 있는
    가장 비싼 방. 여러 상이 P 를 나눠 가질 수 있으므로 min·max 를 둘 다 남긴다.

    ⛔ 이 함수가 못 하는 것
      · **최소 꺾임 하나만** 본다. 나머지 꺾임은 안 본다 (Fig. 2 와 같은 한정).
      · 계수를 안 본다 — "P 가 몇 mol 갔나" 가 아니라 "어느 상으로 갔나" 다.
        그래서 *공급량*을 직접 재지 못한다. 방의 Li 값만 잰다.
      · 끝점(x=0/1) 행은 **세지 않고 이름으로 남긴다** (자체분해라 계면 산물이 아니다).
      · 어느 상이 실제로 생기는지는 hull 이 정한다 — 이 함수는 읽기만 한다.
    """
    import csv as _csv
    rows, skipped = [], []
    with open(csv_path, encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            if str(r.get("is_minimum", "")).strip() not in ("1", "True", "true"):
                continue
            try:
                x = float(r.get("x_atomic_frac", "nan"))
            except ValueError:
                x = None
            tag = f'{r["electrolyte"]}@{r["voltage_V"]}V/{r["cathode"]}'
            if is_endpoint(x):
                skipped.append(tag)
                continue
            hosts = []
            for f in rhs_products(r.get("reaction", "")):
                c = parse_formula(f)
                nP = c.get(p_element, 0.0)
                if nP <= 0:
                    continue
                hosts.append({
                    "formula": f,
                    "li_per_P": round(c.get(ladder_element, 0.0) / nP, 4),
                    "anion": ("P-O" if c.get("O", 0) > 0 else
                              "P-S" if c.get("S", 0) > 0 else
                              "P-Cl" if c.get("Cl", 0) > 0 else "P-only"),
                })
            rows.append({
                "electrolyte": r["electrolyte"], "cathode": r["cathode"],
                "voltage_V": float(r["voltage_V"]), "x_atomic_frac": x,
                "p_hosts": hosts,
                "rung_max_li_per_P": max((h["li_per_P"] for h in hosts), default=None),
                "rung_min_li_per_P": min((h["li_per_P"] for h in hosts), default=None),
                "has_P_S_host": any(h["anion"] == "P-S" for h in hosts),
            })
    rows.sort(key=lambda d: (d["electrolyte"], d["voltage_V"], d["cathode"]))
    by_ev = {}
    for d in rows:
        k = f'{d["electrolyte"]}@{d["voltage_V"]:g}'
        b = by_ev.setdefault(k, {"n_cathodes": 0, "rung_max": None,
                                 "cathodes_with_P_S_host": []})
        b["n_cathodes"] += 1
        if d["rung_max_li_per_P"] is not None:
            b["rung_max"] = (d["rung_max_li_per_P"] if b["rung_max"] is None
                             else max(b["rung_max"], d["rung_max_li_per_P"]))
        if d["has_P_S_host"]:
            b["cathodes_with_P_S_host"].append(d["cathode"])
    import datetime as _dt
    return {"generated_by": "tools/oxidation/interface_reactivity_v2.py --p_host_ladder",
            "generated_at": _dt.date.today().isoformat(),
            "method": ("최소 kink 반응식의 우변에서 P 를 포함한 상을 뽑고 그 상의 Li:P 를 센다. "
                       "rung = 그 조건에서 가장 큰 Li/P (아직 살아 있는 가장 비싼 방). "
                       "MP·pymatgen 을 안 쓴다 — 이미 기록된 반응식 문자열만 읽는 후처리다."),
            "source_csv": str(csv_path), "n_conditions": len(rows),
            "endpoint_excluded": sorted(skipped), "rows": rows,
            "by_electrolyte_voltage": by_ev,
            "⛔": "최소 꺾임 하나만 본다 (Fig. 2 와 같은 한정). 계수를 안 보므로 "
                 "'풀려난 P 의 양' 이 아니라 '어느 상이 P 를 받았나' 를 잰다. "
                 "끝점 행은 endpoint_excluded 로 뺐다."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolytes", nargs="+",
                    help='comp:label, e.g. "Li6PS5Cl:LPSCl"')
    ap.add_argument("--batch_from", nargs="?", const=CASCADE_CSV,
                    help="캐스케이드 CSV 에서 90종 챔피언을 읽어 **종마다 따로** 돈다")
    ap.add_argument("--resume", action="store_true", help="JSONL 에 이미 있는 쌍은 건너뛴다")
    ap.add_argument("--limit", type=int, help="앞 N 종만 (시범용)")
    ap.add_argument("--only", nargs="+",
                    help='캐스케이드 대신 지정 조성만 — "label:formula" '
                         '(기준선용: "LPSCl:Li6PS5Cl")')
    ap.add_argument("--closed", action="store_true",
                    help="닫힌계 0 V (Li 저장고 안 엶) — **Li 음극 쪽은 이걸 써야 한다**")
    ap.add_argument("--cathodes", nargs="+", default=["LiCoO2", "LiNiO2"],
                    help='comp[:label] cathodes')
    ap.add_argument("--voltages", nargs="+", type=float,
                    default=[2.5, 3.0, 3.5, 4.0, 4.3])
    ap.add_argument("--out", default="interface_reactivity_v2.json")
    ap.add_argument("--p_host_ladder", metavar="PANELS_CSV",
                    help="x-scan 패널 CSV 를 읽어 최소 꺾임의 P 수용상·Li:P 사다리를 뽑는다 "
                         "(MP·pymatgen 불필요 — 이미 나온 반응식만 읽는다)")
    if "--selftest" in __import__("sys").argv:
        raise SystemExit(_selftest())
    a = ap.parse_args()
    if a.p_host_ladder:
        # 순수 후처리다 — MP 도 pymatgen 도 안 쓴다. 그래서 여기서 바로 끝낸다.
        out = p_host_ladder(a.p_host_ladder)
        Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2),
                               encoding="utf-8")
        csv_out = Path(a.out).with_suffix(".csv")
        with open(csv_out, "w", encoding="utf-8", newline="") as fh:
            w = __import__("csv").writer(fh)
            w.writerow(["electrolyte", "cathode", "voltage_V", "p_host_formula",
                        "li_per_P", "anion"])
            for d in out["rows"]:
                for h in d["p_hosts"]:
                    w.writerow([d["electrolyte"], d["cathode"], d["voltage_V"],
                                h["formula"], h["li_per_P"], h["anion"]])
        print(f'{out["n_conditions"]} 조건 · 끝점 제외 {len(out["endpoint_excluded"])} '
              f'→ {a.out} · {csv_out}')
        for k, b in sorted(out["by_electrolyte_voltage"].items()):
            ps = f' · P-S 수용상: {",".join(b["cathodes_with_P_S_host"])}' if b["cathodes_with_P_S_host"] else ""
            print(f'  {k:>18}  rung(max Li/P) = {b["rung_max"]}{ps}')
        return 0
    if a.batch_from or a.only:
        if a.only and not a.batch_from:
            a.batch_from = True
        return run_batch(a)
    if not a.electrolytes:
        ap.error("--electrolytes 또는 --batch_from 중 하나는 있어야 한다")
    # ⛔ 2026-09-16 실측 — `--closed` 는 `run_batch` 안에서만 읽힌다(`a.closed` 는
    #   199·215·217·218 행에만 있다). 아래 경로는 그 플래그를 **한 번도 안 본다.**
    #   그래서 `--closed --electrolytes ...` 는 오류 없이 **열린계를 돌려 놓고**
    #   전압 쓸이가 찍힌 출력을 낸다 — 닫힌계 0 V 인 척하는 그럴듯한 결과다.
    #   (2026-09-16 에 7 종을 그렇게 돌렸고, 전압줄을 보고서야 알아챘다.)
    #   조용히 무시하지 않고 **시작을 막는다** — kb/methodology/silent_wrong_path_2026_09_13.md
    if a.closed:
        ap.error("⛔ --closed 는 이 경로(--electrolytes)에서 **구현돼 있지 않다** — "
                 "지금까지 조용히 무시됐다. 닫힌계는 배치 경로에만 있으니 "
                 "`--only \"라벨:조성\"` (또는 --batch_from) 으로 돌릴 것. 예: "
                 "--closed --only \"Nd:Li4.8Nd0.2P1S4.4Cl1.6\" --cathodes LiCoO2 "
                 "--out db/properties/x.jsonl")

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
        results[clab] = {"composition": cstr, "by_voltage": {}, "reactions": {},
                         "kinks": {}, "endpoint_degenerate": {}}
        print(f"\n######## cathode {clab} ({cstr}) ########")
        for V in a.voltages:
            mu = mu0 - V
            gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu})
            row, rxn_row, kink_row, deg_row = {}, {}, {}, {}
            for spec in a.electrolytes:
                estr, _, elab = spec.partition(":"); elab = elab or estr
                try:
                    e, rxn, x, kinks = min_rxn_grand(Composition(estr), cc, gpd, pd,
                                                     want_kinks=True)
                    row[elab] = round(e, 5)
                    rxn_row[elab] = rxn          # ⭐ 2026-09-16: 버리지 않는다 (아래 주석)
                    kink_row[elab] = kinks       # ⭐ x-스캔 곡선용 전 kink
                    deg_row[elab] = is_endpoint(x)
                    # ⛔ 끝점이면 상대가 계산에 안 들어간 값이다 — 조용히 넘기지 않는다.
                    mark = "  ⛔끝점 x=%.3g — 계면량 아님(자체분해)" % x if deg_row[elab] else ""
                    print(f"  V={V:.2f}  {elab:9s}: {e:.4f} eV/atom   {rxn}{mark}")
                except Exception as ex:
                    row[elab] = None
                    rxn_row[elab] = None
                    kink_row[elab] = []
                    deg_row[elab] = False
                    print(f"  V={V:.2f}  {elab}: ERR {type(ex).__name__}: {ex}")
            results[clab]["by_voltage"][f"{V:.2f}"] = row
            results[clab]["endpoint_degenerate"][f"{V:.2f}"] = deg_row
            # ⛔ 2026-09-16 — 종전 판은 `min_rxn` 을 **계산해 놓고 버렸다.** 숫자만 남아서
            #   "어떤 상으로 분해되나" 를 JSON 에서 못 읽었고, 그게 갭 단계(§C)의 입력이다.
            #   화면에는 찍혔으니 '되는 것처럼' 보였다 — 조용히 틀린 경로.
            results[clab]["reactions"][f"{V:.2f}"] = rxn_row
            results[clab]["kinks"][f"{V:.2f}"] = kink_row

    cen = product_census(results)
    print(f"\n══ 산물 인구조사 — 갭(§C) 대상 후보 {cen['n_unique']} 종 ══")
    for f, n in cen["counts"].items():
        print(f"  {f:16s} {n:3d} 회   처음 나온 곳 {cen['first_seen'][f]}")
    if cen.get("reservoir_excluded"):
        print(f"  (저장소 회계로 제외: {cen['reservoir_excluded']} — 상이 아니라 전기화학 장부다)")
    _deg = cen.get("endpoint_degenerate_excluded") or []
    if _deg:
        _tot = sum(len(r or {}) for cd in results.values()
                   for r in (cd.get("reactions") or {}).values())
        print(f"  ⛔ 끝점 퇴화로 제외: {len(_deg)}/{_tot} 칸 — 전해질 자체분해라 계면 산물이 아니다")
        if len(_deg) == _tot:
            print("  ⛔⛔ **전부 퇴화했다 — 이 실행은 계면을 한 번도 안 쟀다.** "
                  "상대가 이미 산화가 끝난 상이면 열린계로는 못 잰다. 닫힌계(--closed --only)로 갈 것.")
    print("  ⛔ 이 목록은 **최소 kink 산물**만이다. 다른 kink 의 상은 여기 없다 (카드 G2).")
    print("  ⚠ 기체·홑원소(S·SO₂·PCl₅)는 **안 걸렀다** — 갭 대상인지는 카드·사람이 정한다.")

    Path(a.out).write_text(json.dumps({
        "product_census": cen,
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
