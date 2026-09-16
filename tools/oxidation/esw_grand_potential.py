#!/usr/bin/env python3
"""esw_grand_potential.py — REAL electrochemical stability window (ESW)
via the grand-potential phase-diagram method (Ong 2008; Mo/Ong/Ceder 2012,
Chem. Mater. 24, 15; Zhu/He/Mo 2015, JMCA).

This is the genuine ESW — NOT the qualitative "competing-phase energy span"
hint from tools/doping/esw_check.py. The Li reservoir is opened (grand
canonical) and the composition's Li-grand-potential decomposition is tracked
as the applied potential (= μ_Li) is scanned, using pymatgen's standard
`PhaseDiagram.get_element_profile`.

Why get_element_profile (and not "place compound at hull energy + scan")
-----------------------------------------------------------------------
For these argyrodite electrolytes the ordered phase is itself slightly
metastable (~tens of meV/atom above hull) and, more importantly, a
non-stoichiometric composition (modelc Li5.4PS4.4Cl1.6) has NO MP entry and
no MP-scale total energy of its own. get_element_profile needs only the
*composition* and the MP convex hull: it returns, as the Li chemical
potential is swept, the sequence of equilibrium decomposition reactions and
the critical μ_Li at which they switch. That makes comp1 (in MP) and modelc
(not in MP) directly comparable on the same footing.

Voltage convention
------------------
V (vs Li/Li+) = μ_Li(metal) − μ_Li ,  with e = 1, energies in eV.
V = 0  → μ_Li = Li-metal reference (most reducing).
High V → low μ_Li (most oxidizing).

  • Reduction (cathodic) limit = lowest V above which NO further Li is taken
    up (below it the composition is reduced — Li3P / Li2S / Li metal form).
  • Oxidation (anodic) limit  = highest V below which NO Li is released
    (above it the composition is oxidized — S / P2S5 / Cl2 form).
  • ESW width = anodic − cathodic.

생성에너지 표 · 균형반응 (2026-09-16 추가)
------------------------------------------
`--formation` 은 **이미 받아 놓은 같은 hull** 에서 상별 생성에너지를 뽑는다(MP 재조회
없음). `--reaction` 은 사람이 고른 반응식을 `ComputedReaction` 으로 균형 잡아 ΔE 를 낸다.
'Nd 인산염 싱크' 가설처럼 *"P 가 어디로 가는 게 더 이로운가"* 를 재려고 붙였다.

⛔ 이 도구가 **못 하는 것**
  · `--formation` 의 `E_f_per_P` 는 **반응에너지가 아니다** — 순위 힌트다.
  · `--reaction` 의 반응물·생성물은 **사람이 고른 것**이다. hull 이 고르는 판정은
    tools/oxidation/interface_reactivity_v2.py 쪽이다.
  · 둘 다 0 K · MP2020 보정 에너지다 — 온도·엔트로피·pO₂ 를 안 본다.
  · 반응이 **일어나는지**(운동학·핵생성·경로)는 아무것도 말하지 않는다.
  · 실제 합성 가능성을 말하지 않는다.

Usage (run where MP_API_KEY is set, e.g. gabia/kserver116-27):
    python3 esw_grand_potential.py \
        --target "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" \
        --out esw_lpscl_results.json

    # 생성에너지만 (인산염 싱크 정량화) — --target 없이도 돈다
    python3 esw_grand_potential.py --elements Li P S Cl Nd O \
        --formation --reaction "P2S7,Nd2O3 > NdPO4,S" \
        --out cei_formation_2026_09_16.json
"""
import argparse
import json
import os
from pathlib import Path


def get_chemsys_entries(elements):
    """MP2020-corrected entries for the chemsys, pinned to the classic
    GGA/GGA+U mixed hull (avoids R2SCAN mixing noise; matches the Mo/Ong
    literature numbers)."""
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    chemsys = "-".join(sorted(elements))
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements,
            additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    print(f"[mp_api] {len(entries)} entries in {chemsys} (GGA_GGA+U hull)")
    return entries


def rxn_to_str(reaction):
    try:
        return str(reaction)
    except Exception:
        return repr(reaction)


# ── 열린 원소별 해석 (2026-09-07 추가) ───────────────────────────────────────
#: `evolution` 은 저장소와 **주고받은 몰수**다. 부호의 물리적 뜻이 **원소마다 다르다** —
#: 이걸 헷갈리면 산화를 환원이라 부르게 된다.
#:   Li 를 열면:  받아들임(+) = **환원**   · 내보냄(−) = **산화**
#:   O  를 열면:  받아들임(+) = **산화**   · 내보냄(−) = 환원(탈산소)
#: 그래서 결과 키를 `reduction/oxidation` 으로 박지 않고 **uptake/release** 로 중립화하고,
#: 원소별 해석 문자열을 결과에 같이 실어 보낸다.
OPEN_ELEMENT_MEANING = {
    "Li": {"uptake": "환원 (cathodic) — Li 를 받아들인다",
           "release": "산화 (anodic) — Li 를 내놓는다",
           "axis": "V_vs_Li"},
    "O":  {"uptake": "**산화** — 저장소(O₂)에서 O 를 받아들인다",
           "release": "환원/탈산소 — O 를 내놓는다",
           "axis": "dmu_O_eV"},
    "S":  {"uptake": "황화 (sulfidation)", "release": "탈황", "axis": "dmu_S_eV"},
}

#: ⛔⛔ O 를 열 때 반드시 같이 나가야 하는 경고. 데이터에 붙여 보낸다 — 화면에만 찍으면
#:   JSON 만 받은 사람이 μ_O 축을 절대값으로 읽는다.
O2_REFERENCE_CAVEAT = (
    "⛔ μ_O 축의 절대값을 믿지 말 것. (1) PBE 는 O₂ 분자를 ~1 eV 과결합하고, "
    "MP 는 anion correction 으로 보정한다 — 그래서 이 축은 **MP 보정 기준계**의 것이다. "
    "(2) UMA 등 다른 방법의 에너지와 **섞으면 축이 통째로 밀린다**. "
    "(3) pO₂·온도 환산은 이 도구가 하지 않는다 — 환산은 기준 선택이 결과를 지배하는 자리라 "
    "고체 기준반응(예: Li₂O 생성)에 앵커한 뒤 별도로 한다. "
    "여기서 인용 가능한 것은 **Δμ_O 축 위의 순서와 분해산물 정체**다."
)


#: 축을 읽을 수 있게 만드는 **기준 반응**. `환원형,산화형` 쌍으로 준다.
#:   `2 Li + ½O₂ → Li₂O` 의 평형 μ_O 를 **같은 hull 위에서** 내면, 우리 개시점을
#:   *"Li/Li₂O 평형보다 얼마나 위/아래"* 로 말할 수 있다 — **기준이 양쪽에서 지워져서**
#:   PBE O₂ 과결합·MP anion correction 이 차이에서 상쇄된다.
#: ⚠ 완전 상쇄는 아니다: 두 반응의 O 결합환경이 다르면 보정 오차가 완전히는 안 지워진다.
#:   그래도 **원소 기준 절대값보다는 훨씬 낫다** — 그것이 이 기능의 전부다.
DEFAULT_LANDMARKS = ("Li,Li2O", "Li2S,Li2SO4", "Li3PS4,Li3PO4")


class _BadFormula(ValueError):
    """화학식을 못 읽었다 — 예외로 죽지 않고 사유로 돌려주기 위한 내부 신호."""


def landmark_mu(entries, red_formula, ox_formula, open_symbol="O"):
    """`A + n/2 X₂ → B` 의 평형 μ_X. 비-X 조성이 맞도록 A 를 스케일한다.

    μ_X = [E(B) − s·E(A)] / [n_X(B) − s·n_X(A)]   (s = 비-X 조성을 맞추는 배수)

    ⛔ 못 하는 것
      · 두 상이 **hull 위에 있는지 확인하지 않는다.** 준안정상을 주면 그 값이 나온다.
      · 비-X 조성이 **비례하지 않으면** 계산하지 않고 None 을 낸다 (억지로 균형 안 잡는다).
      · 실험 생성에너지와 대조하지 않는다 — 그건 부르는 쪽 몫이다.
    """
    from pymatgen.core import Composition, Element
    X = Element(open_symbol)

    def best(f):
        # ⚠ 2026-09-07 — 여기서 그냥 Composition(f) 를 불러 **예외로 죽었다**.
        #   사용자가 오타를 내면 도구가 traceback 을 뱉는다. 못 읽는 것은 사유를 말한다.
        try:
            c = Composition(f)
        except Exception as ex:
            raise _BadFormula(f"화학식을 못 읽는다: {f!r} ({type(ex).__name__})") from ex
        cand = [e for e in entries
                if e.composition.reduced_formula == c.reduced_formula]
        if not cand:
            return None, None
        e = min(cand, key=lambda x: x.energy_per_atom)
        n = c.num_atoms                       # 요청한 화학식 단위로 환산
        return e.energy_per_atom * n, c

    try:
        E_red, c_red = best(red_formula)
        E_ox, c_ox = best(ox_formula)
    except _BadFormula as ex:
        return None, str(ex)
    if E_red is None or E_ox is None:
        return None, f"hull 에 없다: {red_formula if E_red is None else ox_formula}"

    others = sorted({el for el in list(c_red) + list(c_ox) if el != X})
    if not others:
        return None, "비-O 원소가 없다"
    ratios = []
    for el in others:
        a, b = c_red[el], c_ox[el]
        if a < 1e-9:
            if b > 1e-9:
                return None, f"{el} 가 환원형에 없다 — 균형이 안 잡힌다"
            continue
        ratios.append(b / a)
    if not ratios or max(ratios) - min(ratios) > 1e-6:
        return None, f"비-{open_symbol} 조성이 비례하지 않는다 (배수 {ratios})"
    s = ratios[0]
    dn = c_ox[X] - s * c_red[X]
    if abs(dn) < 1e-9:
        return None, f"{open_symbol} 개수가 안 변한다 — 산화반응이 아니다"
    return (E_ox - s * E_red) / dn, None


# ── 생성에너지 표 · 균형반응 (2026-09-16 추가) ──────────────────────────────
#: '인산염 싱크' 가설을 재려고 기본으로 훑는 상들. §B 산물 인구조사에서 실제로 나온
#: 상 + 대조 앵커(Li₃PO₄·P₂S₇)다. 여기 없는 상을 보려면 `--formation` 에 직접 준다.
DEFAULT_P_SINKS = (
    # Nd 인산염 — 가설이 말하는 싱크
    "NdPO4", "Nd(PO3)3", "NdP5O14", "LiNd(PO3)4",
    # Li 인산염 — O 축 단독이 만드는 싱크 (문헌 앵커)
    "Li3PO4", "LiPO3", "Li4P2O7", "P2O5",
    # 티오인산염 — 싱크가 없을 때 P 가 가는 곳
    "Li3PS4", "P2S7", "P2S5",
    # Nd 의 비-인산염 경쟁상 — Nd 가 인산염을 **고르는지** 보려면 같이 있어야 한다
    "Nd2O3", "NdCl3", "Nd2S3", "NdOCl",
)


def _ground_state(entries, reduced_formula):
    """같은 조성의 엔트리 중 **최저 에너지** 하나. 없으면 None. (순수 함수)

    ⛔ `min(..., key=lambda e: e.energy_per_atom or 9e9)` 로 쓰지 않는다 —
       0.0 은 유효한 에너지고 `or` 가 그걸 '없음' 으로 둔갑시킨다
       (`e_above_hull or 9e9` 가 81 일 살아남은 자리와 같은 함정).
    """
    cand = [e for e in entries
            if getattr(e.composition, "reduced_formula", None) == reduced_formula]
    if not cand:
        return None
    return min(cand, key=lambda e: e.energy_per_atom)


def _formation_row(pd, entry, per_element="P"):
    """엔트리 하나의 생성에너지 행. (순수 함수 — `pd` 는 `get_form_energy` 와
    `get_e_above_hull` 만 있으면 된다.)

    ⚠ `E_f_eV_per_<X>` 는 **X 원자 하나당으로 환산한 생성에너지**다. X 가 없으면
      0 이 아니라 **None** 이다 (없는 값을 0 으로 그리지 않는다).
    """
    comp = entry.composition
    n_at = float(comp.num_atoms)
    ef_tot = float(pd.get_form_energy(entry))
    n_x = float(comp[per_element]) if per_element else 0.0
    try:
        hull = float(pd.get_e_above_hull(entry))
    except Exception as ex:                       # hull 밖 엔트리 등
        hull, hull_why = None, f"{type(ex).__name__}: {ex}"
    else:
        hull_why = None
    return {
        "reduced_formula": getattr(comp, "reduced_formula", None),
        "n_atoms": round(n_at, 4),
        f"n_{per_element}": round(n_x, 4),
        "E_f_eV_per_atom": round(ef_tot / n_at, 5) if n_at > 1e-9 else None,
        f"E_f_eV_per_{per_element}": (round(ef_tot / n_x, 5) if n_x > 1e-9 else None),
        "e_above_hull_eV_per_atom": (None if hull is None else round(hull, 5)),
        "e_above_hull_why_none": hull_why,
        "entry_id": str(getattr(entry, "entry_id", "") or ""),
    }


def formation_rows(pd, formulas, per_element="P"):
    """요청한 화학식들의 **MP 생성에너지**를 §B 와 **같은 hull** 에서 뽑는다.

    ⛔ 이 함수가 못 하는 것
      · **반응에너지가 아니다.** `E_f_per_P` 는 O:P 비가 다른 상들을 한 줄에 놓으면
        P–O 결합 수 차이를 P 하나당으로 뭉갠다 — **순위 힌트**지 판정이 아니다.
        판정은 `--reaction` 의 균형반응이 한다.
      · 온도·엔트로피·pO₂ 를 안 본다 (0 K · MP2020 보정 에너지).
      · 그 조성이 실제로 합성되는지 말하지 않는다.
      · hull 에 없는 화학식은 **지어내지 않고** `found: false` 로 남긴다.
    """
    from pymatgen.core import Composition
    ents = list(pd.all_entries)
    rows = {}
    for f in formulas:
        try:
            want = Composition(f).reduced_formula
        except Exception as ex:
            rows[f] = {"found": False,
                       "why": f"화학식을 못 읽는다: {f!r} ({type(ex).__name__})"}
            continue
        e = _ground_state(ents, want)
        if e is None:
            rows[f] = {"found": False, "reduced_formula": want,
                       "why": "이 chemsys hull 에 없다 "
                              "(--elements 를 넓히거나, MP 에 없는 상이다)"}
            continue
        row = _formation_row(pd, e, per_element=per_element)
        row["found"] = True
        rows[f] = row
    return rows


def parse_reaction_spec(spec):
    """`"P2S7,Nd2O3 > NdPO4,S"` → (['P2S7','Nd2O3'], ['NdPO4','S']). (순수 함수)

    ⛔ 계수를 받지 않는다 — 균형은 `ComputedReaction` 이 잡는다. 계수를 쓰면 조용히 무시되는
       대신 여기서 **거절한다** (읽는 사람이 자기 계수가 반영된 줄 알면 안 된다).
    """
    if ">" not in spec:
        return None, None, "형식이 아니다 — '반응물,… > 생성물,…' 로 준다"
    lhs, _, rhs = spec.partition(">")
    L = [t.strip() for t in lhs.split(",") if t.strip()]
    R = [t.strip() for t in rhs.split(",") if t.strip()]
    if not L or not R:
        return None, None, "반응물 또는 생성물이 비었다"
    for t in L + R:
        head = t.split()[0]
        if head.replace(".", "", 1).isdigit():
            return None, None, (f"계수를 직접 주지 않는다 ({t!r}) — 균형은 도구가 잡는다")
    return L, R, None


def balanced_reaction(pd, lhs, rhs, per_element="P"):
    """`ComputedReaction` 으로 균형을 잡고 반응에너지를 낸다.

    내는 값: 식 그대로의 총 에너지(eV) · 반응물 원자당 · **반응물 쪽 X 하나당**.

    ⛔ 못 하는 것
      · 반응이 **일어나는지** 말하지 않는다 (운동학·경로 없음, 0 K).
      · 균형이 안 잡히면 억지로 잡지 않고 사유를 낸다.
      · 반응물/생성물 집합은 **사람이 고른 것**이다 — hull 이 고른 게 아니다.
        hull 이 고르는 것은 `interface_reactivity_v2.py` 쪽이다.
    """
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.reaction_calculator import ComputedReaction
    ents = list(pd.all_entries)
    picked = {}
    for side in (lhs, rhs):
        for f in side:
            if f in picked:
                continue
            try:
                want = Composition(f).reduced_formula
            except Exception as ex:
                return {"ok": False, "why": f"화학식을 못 읽는다: {f!r} ({type(ex).__name__})"}
            e = _ground_state(ents, want)
            if e is None:
                return {"ok": False, "why": f"hull 에 없다: {f} ({want})"}
            picked[f] = e
    try:
        rxn = ComputedReaction([picked[f] for f in lhs], [picked[f] for f in rhs])
        E = float(rxn.calculated_reaction_energy)
    except Exception as ex:
        return {"ok": False, "why": f"균형이 안 잡힌다: {type(ex).__name__}: {ex}"}

    X = Element(per_element)
    n_x = n_at = 0.0
    for c in list(getattr(rxn, "reactants", []) or []):
        try:
            k = abs(float(rxn.get_coeff(c)))
        except Exception:
            k = 0.0
        n_x += k * float(c[X])
        n_at += k * float(c.num_atoms)
    return {
        "ok": True,
        "reaction": str(rxn),
        "E_eV_as_written": round(E, 5),
        "E_eV_per_reactant_atom": round(E / n_at, 5) if n_at > 1e-9 else None,
        f"E_eV_per_{per_element}": round(E / n_x, 5) if n_x > 1e-9 else None,
        f"n_{per_element}_reactant_side": round(n_x, 4),
        "entry_ids": {f: str(getattr(e, "entry_id", "") or "") for f, e in picked.items()},
    }


def steps_from_profile(profile, open_symbol, mu_ref, rxn=rxn_to_str):
    """profile(dict 리스트) → steps. **순수 함수** — pymatgen·MP 없이 시험할 수 있다.

    ⚠ `V_vs_Li` 는 **Li 를 열었을 때만** 낸다. 'V vs Li/Li⁺' 는 Li 저장소에서만 뜻이 있고,
      O 를 연 프로파일에 전압 칸을 붙이면 읽는 사람이 산소압을 전압으로 읽는다.
    """
    steps = []
    for p in profile:
        mu = float(p["chempot"])
        s = {
            f"mu_{open_symbol}_eV": round(mu, 4),
            f"dmu_{open_symbol}_eV": round(mu - mu_ref, 4),
            f"evolution_{open_symbol}": round(float(p["evolution"]), 4),
            "reaction": rxn(p["reaction"]),
        }
        if open_symbol == "Li":
            s["V_vs_Li"] = round(mu_ref - mu, 3)
        if p.get("energy") is not None:
            s["energy_per_atom"] = round(float(p["energy"]), 5)
        steps.append(s)
    return steps


def limits_from_steps(steps, open_symbol):
    """교환 경계를 μ 축에서 찾는다. **원소에 무관한 한 가지 규칙**을 쓴다.

      받아들이기(uptake)는 μ 가 **높을수록** 일어난다 ⇒ 개시점 = `min(μ | evolution>0)`
      내보내기(release)는 μ 가 **낮을수록** 일어난다 ⇒ 개시점 = `max(μ | evolution<0)`

    Li 로 환산하면 V = μ_ref − μ 라 부호가 뒤집혀, 종전의
    `reduction_limit = max(V over pos)` · `oxidation_limit = min(V over neg)` 와 **같은 값**이다.
    (그래서 Li 경로는 동작이 안 바뀐다 — selftest 가 이걸 본다.)
    """
    mk = f"mu_{open_symbol}_eV"
    ek = f"evolution_{open_symbol}"
    pos = [s for s in steps if s[ek] > 1e-6]
    neg = [s for s in steps if s[ek] < -1e-6]
    neu = [s for s in steps if abs(s[ek]) <= 1e-6]
    return {
        "uptake_onset_mu_eV": min((s[mk] for s in pos), default=None),
        "release_onset_mu_eV": max((s[mk] for s in neg), default=None),
        # 중립(자기분해) 지점은 μ 가 제일 높은 쪽을 택한다 — Li 경로의 min(V) 와 같다
        "neutral_mu_eV": max((s[mk] for s in neu), default=None),
    }


def analyze(pd, comp, mu_ref, label, comp_str, open_symbol="Li"):
    """Run get_element_profile for the opened element and extract the limits."""
    from pymatgen.core import Element
    X = Element(open_symbol)

    # evolution profile of the OPEN element for this composition.
    # {'chempot','evolution','reaction','energy'}, sorted by DECREASING chempot.
    profile = pd.get_element_profile(X, comp)
    n_nominal = comp[X] if X in comp else 0.0

    steps = steps_from_profile(profile, open_symbol, mu_ref)
    lim = limits_from_steps(steps, open_symbol)
    mean = OPEN_ELEMENT_MEANING.get(
        open_symbol, {"uptake": f"{open_symbol} 를 받아들인다",
                      "release": f"{open_symbol} 를 내놓는다",
                      "axis": f"dmu_{open_symbol}_eV"})
    mk = f"mu_{open_symbol}_eV"
    ek = f"evolution_{open_symbol}"

    def reaction_at(mu):
        if mu is None:
            return None
        return min(steps, key=lambda s: abs(s[mk] - mu))["reaction"]

    def fmt(mu):
        if mu is None:
            return "—"
        if open_symbol == "Li":
            return f"{mu_ref - mu:+.2f} V"
        return f"Δμ {mu - mu_ref:+.3f} eV"

    print(f"\n=== {label}  {comp_str}  (열린 원소: {open_symbol}) ===")
    print(f"  nominal n_{open_symbol} = {float(n_nominal):.3f}"
          f"   ·  μ_ref({open_symbol}) = {mu_ref:.4f} eV/atom")
    print(f"  중립(자기분해)     @ {fmt(lim['neutral_mu_eV'])} → {reaction_at(lim['neutral_mu_eV'])}")
    print(f"  받아들임 개시      @ {fmt(lim['uptake_onset_mu_eV'])}  [{mean['uptake']}]")
    print(f"                     → {reaction_at(lim['uptake_onset_mu_eV'])}")
    print(f"  내보냄 개시        @ {fmt(lim['release_onset_mu_eV'])}  [{mean['release']}]")
    print(f"                     → {reaction_at(lim['release_onset_mu_eV'])}")
    print(f"  전체 프로파일 ({len(steps)} 분기점):")
    for s in steps:
        print(f"    {fmt(s[mk]):>14}  n={s[ek]:>7.3f}  {s['reaction']}")

    out = {
        "composition": comp_str,
        "label": label,
        "open_element": open_symbol,
        f"n_{open_symbol}_nominal": float(n_nominal),
        f"mu_{open_symbol}_ref_eV": round(mu_ref, 4),
        "meaning": mean,
        "uptake_onset_rxn": reaction_at(lim["uptake_onset_mu_eV"]),
        "release_onset_rxn": reaction_at(lim["release_onset_mu_eV"]),
        "neutral_rxn": reaction_at(lim["neutral_mu_eV"]),
        "profile": steps,
        **lim,
    }
    if open_symbol == "Li":
        # 종전 키 유지 — 이 이름으로 인용된 기존 결과(b2o3_esw.json 등)가 있다
        V = lambda mu: (None if mu is None else round(mu_ref - mu, 3))
        out.update({
            "n_Li_nominal": float(n_nominal),
            "mu_Li_ref_eV": round(mu_ref, 4),
            "reduction_limit_V": V(lim["uptake_onset_mu_eV"]),
            "oxidation_limit_V": V(lim["release_onset_mu_eV"]),
            "ocv_self_decomposition_V": V(lim["neutral_mu_eV"]),
            "ocv_self_decomposition_rxn": reaction_at(lim["neutral_mu_eV"]),
            "oxidation_onset_rxn": reaction_at(lim["release_onset_mu_eV"]),
        })
    if open_symbol == "O":
        out["⛔_caveat"] = O2_REFERENCE_CAVEAT
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # ⚠ 2026-09-07 — required=True 였다. 그래서 `--selftest` 만으로는 **selftest 가
    #   안 돌았다**(더미 --target 을 줘야 했다). 시험을 돌리기 어렵게 만드는 것은
    #   시험을 안 돌리게 만드는 것과 같다. 아래에서 손으로 검사한다.
    ap.add_argument("--target", nargs="+",
                    help='comp:label, e.g. "Li6PS5Cl:comp1" '
                         '"Li5.4P1S4.4Cl1.6:modelc"')
    ap.add_argument("--elements", nargs="+", default=["Li", "P", "S", "Cl"])
    ap.add_argument("--open_element", default="Li",
                    help="저장소를 여는 원소. 기본 Li(전기화학 ESW). **O 를 주면 산소 노출** "
                         "(LPSCl + O₂) 의 μ_O staircase 가 나온다. ⚠ 부호의 뜻이 원소마다 "
                         "다르다 — O 는 받아들임(+)이 **산화**다.")
    ap.add_argument("--out", default="esw_grand_potential_results.json")
    ap.add_argument("--landmarks", nargs="*", default=list(DEFAULT_LANDMARKS),
                    help="축을 읽을 기준 반응. '환원형,산화형' 쌍 (예: Li,Li2O). "
                         "빈 목록을 주면 끈다.")
    ap.add_argument("--exclude_phases", nargs="*", default=[],
                    help="Phases to drop from the hull, by reduced FORMULA or MP-id "
                         "(Gil-González 2022 set: LiS4 SCl3 Li5PS4Cl2). Formula match "
                         "is robust to MP re-ids.")
    ap.add_argument("--formation", nargs="*", default=None, metavar="FORMULA",
                    help="**생성에너지 표**를 같은 hull 에서 같이 낸다. 인자 없이 주면 "
                         f"기본 목록({len(DEFAULT_P_SINKS)}종: Nd 인산염·Li 인산염·티오인산염·"
                         "Nd 비-인산염 경쟁상). ⚠ 반응에너지가 아니라 **순위 힌트**다.")
    ap.add_argument("--reaction", nargs="*", default=None, metavar="SPEC",
                    help='균형반응 에너지. 형식 "반응물,… > 생성물,…" '
                         '(예: "P2S7,Nd2O3 > NdPO4,S"). 계수는 도구가 잡는다.')
    ap.add_argument("--per_element", default="P",
                    help="생성에너지·반응에너지를 **이 원소 하나당**으로도 환산한다 (기본 P).")
    ap.add_argument("--selftest", action="store_true",
                    help="MP·pymatgen 없이 판정 논리만 시험 (음성 경로 포함)")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    # --formation/--reaction 만으로도 돌 수 있다 (열린 원소 프로파일은 건너뛴다)
    if not args.target and args.formation is None and args.reaction is None:
        ap.error("--target 이 필요하다 "
                 "(--formation/--reaction/--selftest 를 쓸 때만 생략 가능)")

    # ⛔ 열 원소가 chemsys 에 없으면 hull 에 그 원소가 아예 없다 — 조용히 빈 프로파일이
    #   나오지 않게 여기서 멈춘다 (fail-closed).
    if args.open_element not in args.elements:
        raise SystemExit(
            f"⛔ --open_element {args.open_element} 가 --elements {args.elements} 에 없다. "
            f"O 를 열려면 --elements Li P S Cl O 처럼 chemsys 에 넣어야 한다.")

    from pymatgen.core import Element, Composition
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    entries = get_chemsys_entries(args.elements)
    if args.exclude_phases:
        ex = set(args.exclude_phases)
        def _ids(e):
            # match by entry_id OR material_id OR reduced formula (MP re-ids phases,
            # so formula match is the robust one, e.g. --exclude_phases LiS4 SCl3 Li5PS4Cl2)
            return (str(getattr(e, "entry_id", "")) + "|"
                    + str((getattr(e, "data", {}) or {}).get("material_id", "")) + "|"
                    + e.composition.reduced_formula)
        dropped = [_ids(e) for e in entries if any(x in _ids(e) for x in ex)]
        entries = [e for e in entries if not any(x in _ids(e) for x in ex)]
        print(f"[exclude] dropped {len(dropped)} entries {sorted(ex)}: {dropped}")
    pd = PhaseDiagram(entries)
    X = Element(args.open_element)
    mu_ref = pd.el_refs[X].energy_per_atom
    print(f"μ_{args.open_element}(element reference) = {mu_ref:.4f} eV/atom")
    if args.open_element == "O":
        print(f"  {O2_REFERENCE_CAVEAT}")

    # ── 기준 반응(landmark) — 축을 읽을 수 있게 만든다 ──────────────────────
    landmarks = {}
    for spec in (args.landmarks or []):
        if "," not in spec:
            print(f"  [landmark] 건너뜀 — '환원형,산화형' 형식이 아니다: {spec}"); continue
        red, ox = [t.strip() for t in spec.split(",", 1)]
        mu, why = landmark_mu(entries, red, ox, args.open_element)
        landmarks[f"{red}->{ox}"] = (None if mu is None else
                                     {"mu_eV": round(mu, 4),
                                      f"dmu_{args.open_element}_eV": round(mu - mu_ref, 4)})
        if mu is None:
            print(f"  [landmark] {red}→{ox}: 못 냄 — {why}")
        else:
            print(f"  [landmark] {red:>10s} → {ox:<10s}  "
                  f"μ_{args.open_element} = {mu:+.4f}  (Δμ {mu - mu_ref:+.4f} eV)")
    if landmarks:
        print("  ⇒ 개시점을 이 기준 대비로 읽으면 **기준이 양쪽에서 지워진다** "
              "(절대값보다 훨씬 낫다. 완전 상쇄는 아니다 — O 결합환경이 다르면 잔차가 남는다)")
        print()

    results = {}
    for spec in (args.target or []):
        comp_str, _, label = spec.partition(":")
        label = label or comp_str
        comp = Composition(comp_str)
        try:
            results[label] = analyze(pd, comp, mu_ref, label, comp_str,
                                     open_symbol=args.open_element)
        except Exception as e:
            print(f"  [error] {label}: {type(e).__name__}: {e}")
            results[label] = {"composition": comp_str, "error": str(e)}

    # ── 생성에너지 표 (2026-09-16) ────────────────────────────────────────
    formation = None
    if args.formation is not None:
        want = list(args.formation) or list(DEFAULT_P_SINKS)
        X = args.per_element
        formation = formation_rows(pd, want, per_element=X)
        print(f"\n══ 생성에너지 (같은 hull · MP2020 보정) — {X} 하나당 환산 같이 ══")
        print(f"  {'formula':<14s} {'E_f eV/at':>10s} {f'E_f eV/{X}':>11s} "
              f"{'hull eV/at':>11s}  entry")
        for f in want:
            r = formation[f]
            if not r.get("found"):
                print(f"  {f:<14s} {'—':>10s} {'—':>11s} {'—':>11s}  "
                      f"⛔ {r.get('why')}")
                continue
            px = r.get(f"E_f_eV_per_{X}")
            print(f"  {f:<14s} {r['E_f_eV_per_atom']:>10.4f} "
                  f"{('—' if px is None else f'{px:.4f}'):>11s} "
                  f"{r['e_above_hull_eV_per_atom']:>11.4f}  {r['entry_id']}")
        print("  ⚠ 이 표는 **반응에너지가 아니다** — O:P 비가 다른 상을 한 줄에 놓으면 "
              "P–O 결합 수를 P 하나당으로 뭉갠다. 순위 힌트로만 읽는다.")

    # ── 균형반응 (2026-09-16) ─────────────────────────────────────────────
    reactions = None
    if args.reaction is not None:
        reactions = {}
        X = args.per_element
        print(f"\n══ 균형반응 (ComputedReaction · 같은 hull) ══")
        for spec in args.reaction:
            L, R, why = parse_reaction_spec(spec)
            if why:
                reactions[spec] = {"ok": False, "why": why}
                print(f"  ⛔ {spec}: {why}"); continue
            out = balanced_reaction(pd, L, R, per_element=X)
            reactions[spec] = out
            if not out.get("ok"):
                print(f"  ⛔ {spec}: {out['why']}"); continue
            px = out.get(f"E_eV_per_{X}")
            print(f"  {out['reaction']}")
            print(f"     ΔE = {out['E_eV_as_written']:+.4f} eV (식 그대로) · "
                  f"{out['E_eV_per_reactant_atom']:+.4f} eV/반응물원자 · "
                  + ("—" if px is None else f"{px:+.4f} eV/{X}"))

    payload = {
        "method": "grand-potential element profile via PhaseDiagram.get_element_profile "
                  f"(Mo/Ong/Ceder 2012); MP GGA_GGA+U corrected hull; **{args.open_element} opened**.",
        "open_element": args.open_element,
        "elements": args.elements,
        "landmarks": landmarks,
        "excluded_phases": args.exclude_phases,
        f"mu_{args.open_element}_ref_eV": round(mu_ref, 4),
        "axis_convention": (
            "V = mu_Li(metal) - mu_Li; 0 V = Li metal" if args.open_element == "Li"
            else f"dmu_{args.open_element} = mu - mu_ref(element); 0 = 원소 기준상태. "
                 f"⚠ 전압(V vs Li/Li+)이 **아니다.**"),
        "results": results,
    }
    if formation is not None:
        payload["formation"] = formation
        payload["formation_per_element"] = args.per_element
        payload["⛔_formation_caveat"] = (
            "이 표는 **반응에너지가 아니다.** `E_f_per_P` 는 O:P 비가 다른 상들을 한 줄에 놓으면 "
            "P–O 결합 수 차이를 P 하나당으로 뭉갠다 — **순위 힌트**다. 판정은 균형반응(`reactions`)이 "
            "한다. 0 K · MP2020 보정 에너지이고 온도·엔트로피·pO₂ 를 안 본다. "
            "여기 상들이 실제로 합성/석출된다는 뜻도 아니다.")
    if reactions is not None:
        payload["reactions"] = reactions
        payload["⛔_reaction_caveat"] = (
            "반응물·생성물 집합은 **사람이 고른 것**이다 — hull 이 고른 게 아니다. "
            "hull 이 고르는 판정은 interface_reactivity_v2.py 쪽이다. "
            "반응이 **일어나는지**(운동학·경로)는 말하지 않는다.")
    if args.open_element == "Li":
        payload["mu_Li_ref_eV"] = round(mu_ref, 4)     # 종전 키 유지
    if args.open_element == "O":
        payload["⛔_caveat"] = O2_REFERENCE_CAVEAT
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\n→ {args.out}")


# ── selftest ────────────────────────────────────────────────────────────────
def selftest():
    """판정 논리만 시험한다 (MP·pymatgen 불필요).

    ⛔ 여기서 **보증하지 못하는 것**: MP 엔트리 회수, hull 구성, `get_element_profile`
       자체의 정확도. 이 시험이 보는 것은 **프로파일을 받은 뒤 우리가 하는 해석**뿐이다.
    """
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += bool(c); bad += (not c)

    # μ 가 감소하는 순서 (pymatgen 관례). Li: μ 높음 = 저전압.
    prof = [{"chempot": -1.0, "evolution":  2.0, "reaction": "R_uptake_hi"},
            {"chempot": -2.0, "evolution":  1.0, "reaction": "R_uptake_lo"},
            {"chempot": -3.0, "evolution":  0.0, "reaction": "R_neutral"},
            {"chempot": -4.0, "evolution": -1.5, "reaction": "R_release"}]

    s_li = steps_from_profile(prof, "Li", mu_ref=-1.0)
    chk("V_vs_Li" in s_li[0], "Li 를 열면 전압축을 낸다")
    chk(s_li[3]["V_vs_Li"] == 3.0, f"V = μ_ref − μ (기대 3.0, 실제 {s_li[3]['V_vs_Li']})")
    L = limits_from_steps(s_li, "Li")
    chk(L["uptake_onset_mu_eV"] == -2.0, "받아들임 개시 = min(μ | evolution>0)")
    chk(L["release_onset_mu_eV"] == -4.0, "내보냄 개시 = max(μ | evolution<0)")
    # 종전 Li 공식과 같은 값인가 — 리팩터가 값을 바꾸지 않았다는 증거
    chk(round(-1.0 - L["uptake_onset_mu_eV"], 3) == 1.0,
        "⛔음성: 종전 `reduction_limit = max(V over pos)` 와 **같은 값**이 나온다")
    chk(round(-1.0 - L["release_onset_mu_eV"], 3) == 3.0,
        "⛔음성: 종전 `oxidation_limit = min(V over neg)` 와 **같은 값**이 나온다")

    s_o = steps_from_profile(prof, "O", mu_ref=-4.5)
    chk("V_vs_Li" not in s_o[0],
        "⛔음성: **O 를 열면 전압축을 안 낸다** (산소압을 전압으로 읽게 만들면 안 된다)")
    chk("dmu_O_eV" in s_o[0] and s_o[0]["dmu_O_eV"] == 3.5, "Δμ_O = μ − μ_ref")
    chk("evolution_O" in s_o[0] and "evolution_Li" not in s_o[0], "키가 열린 원소를 따라간다")
    O = limits_from_steps(s_o, "O")
    chk(O["uptake_onset_mu_eV"] == -2.0 and O["release_onset_mu_eV"] == -4.0,
        "경계 공식은 원소에 무관하다 (같은 프로파일 → 같은 μ)")
    chk("산화" in OPEN_ELEMENT_MEANING["O"]["uptake"]
        and "환원" in OPEN_ELEMENT_MEANING["Li"]["uptake"],
        "⛔음성: **O 의 받아들임은 산화, Li 의 받아들임은 환원** — 뜻이 뒤집혀 있다")

    # 경계: 교환이 한 방향뿐이면 반대쪽은 None (0 이 아니다)
    one = steps_from_profile([{"chempot": -1.0, "evolution": 1.0, "reaction": "r"}], "O", -1.0)
    chk(limits_from_steps(one, "O")["release_onset_mu_eV"] is None,
        "⛔음성: 없는 경계를 **0 으로 지어내지 않는다** (None)")
    chk(limits_from_steps([], "O")["uptake_onset_mu_eV"] is None, "빈 프로파일도 안 죽는다")
    chk("μ_O" in O2_REFERENCE_CAVEAT and "pO₂" in O2_REFERENCE_CAVEAT,
        "O₂ 기준 경고문이 데이터에 실려 나간다")

    # ── landmark (2026-09-07) — 축을 읽게 만드는 기준 반응 ───────────────────
    chk(len(DEFAULT_LANDMARKS) >= 3 and all("," in x for x in DEFAULT_LANDMARKS),
        "기본 기준 반응 목록이 '환원형,산화형' 형식이다")

    # ── 생성에너지·균형반응 (2026-09-16) — pymatgen 없이 도는 순수 부분 ──────
    class _C(dict):
        """Composition 대역 — `reduced_formula`·`num_atoms`·`c['P']` 만 쓴다."""
        def __init__(self, rf, d):
            super().__init__(d); self.reduced_formula = rf
        @property
        def num_atoms(self):
            return sum(self.values())
        def __missing__(self, k):
            return 0.0

    class _E:
        def __init__(self, rf, d, epa, eid=""):
            self.composition = _C(rf, d); self.energy_per_atom = epa
            self.entry_id = eid

    class _PD:
        """pd 대역 — form/hull 을 손으로 박아 **정규화만** 시험한다."""
        def __init__(self, ents, form, hull):
            self.all_entries = ents; self._f = form; self._h = hull
        def get_form_energy(self, e):
            return self._f[e.entry_id]
        def get_e_above_hull(self, e):
            v = self._h[e.entry_id]
            if v is None:
                raise ValueError("hull 밖")
            return v

    #: NdPO4 (6 원자 · P 1) · 같은 조성의 준안정 다형체 둘 · P 없는 Nd2O3
    e_lo = _E("NdPO4", {"Nd": 1, "P": 1, "O": 4}, -7.0, "mp-lo")
    e_hi = _E("NdPO4", {"Nd": 1, "P": 1, "O": 4}, -6.5, "mp-hi")
    e_zero = _E("Nd", {"Nd": 1}, 0.0, "mp-zero")          # ⛔ `or` 함정 표적
    e_nop = _E("Nd2O3", {"Nd": 2, "O": 3}, -8.0, "mp-nd2o3")
    ents = [e_hi, e_lo, e_zero, e_nop]

    chk(_ground_state(ents, "NdPO4") is e_lo,
        "같은 조성이 여럿이면 **최저 에너지** 다형체를 고른다")
    chk(_ground_state(ents, "NdPO4") is not e_hi,
        "⛔음성: 목록 순서(먼저 나온 준안정상)를 고르지 않는다")
    chk(_ground_state(ents, "Nd") is e_zero,
        "⛔음성: `energy_per_atom == 0.0` 을 **없음으로 둔갑시키지 않는다** "
        "(`x or 9e9` 함정)")
    chk(_ground_state(ents, "LiNd(PO3)4") is None,
        "⛔음성: 없는 조성에 **아무거나 돌려주지 않는다** (None)")

    pdf = _PD(ents, form={"mp-lo": -36.0, "mp-nd2o3": -25.0, "mp-zero": 0.0},
              hull={"mp-lo": 0.0, "mp-nd2o3": 0.0, "mp-zero": None})
    r = _formation_row(pdf, e_lo, per_element="P")
    chk(r["E_f_eV_per_atom"] == -6.0, f"E_f/atom = 총/원자수 (기대 −6.0 · 얻음 {r['E_f_eV_per_atom']})")
    chk(r["E_f_eV_per_P"] == -36.0, f"E_f/P = 총/P수 (기대 −36.0 · 얻음 {r['E_f_eV_per_P']})")
    chk(r["e_above_hull_eV_per_atom"] == 0.0 and r["e_above_hull_why_none"] is None,
        "⛔음성: hull 0.0 을 **결측으로 읽지 않는다**")
    r2 = _formation_row(pdf, e_nop, per_element="P")
    chk(r2["E_f_eV_per_P"] is None,
        "⛔음성: P 가 없는 상의 'P 하나당' 은 **0 이 아니라 None** 이다")
    r3 = _formation_row(pdf, e_zero, per_element="P")
    chk(r3["e_above_hull_eV_per_atom"] is None and r3["e_above_hull_why_none"],
        "⛔음성: hull 을 못 내면 **0 으로 그리지 않고 사유를 남긴다**")

    chk(len(DEFAULT_P_SINKS) >= 12 and "P2S7" in DEFAULT_P_SINKS
        and "Nd2O3" in DEFAULT_P_SINKS,
        "기본 목록에 **대조상**(티오인산염·Nd 비-인산염)이 같이 들어 있다")

    L, R, why = parse_reaction_spec("P2S7,Nd2O3 > NdPO4,S")
    chk(why is None and L == ["P2S7", "Nd2O3"] and R == ["NdPO4", "S"],
        "반응식 파싱 — 양쪽을 쉼표로 가른다")
    chk(parse_reaction_spec("P2S7 + Nd2O3")[2] is not None,
        "⛔음성: '>' 없는 문자열을 **반응으로 받지 않는다**")
    chk(parse_reaction_spec(" > NdPO4")[2] is not None,
        "⛔음성: 반응물이 빈 식을 받지 않는다")
    chk(parse_reaction_spec("2 P2S7 > NdPO4")[2] is not None,
        "⛔음성: **계수를 직접 주면 거절한다** (조용히 무시하면 자기 계수가 반영된 줄 안다)")

    try:
        from pymatgen.core import Composition          # noqa: F401
    except ImportError:
        print("  ⚠ landmark 계산 시험 **건너뜀** — pymatgen 이 없다.")
        print("     ⛔ 이건 통과가 아니라 **안 돈 것**이다. gabia 에서 반드시 다시 돌린다:")
        print("        python3 tools/oxidation/esw_grand_potential.py --selftest")
    else:
        class _FakeEntry:
            def __init__(self, formula, e_per_atom):
                self.composition = Composition(formula)
                self.energy_per_atom = e_per_atom

        # Li −1.0/atom · Li2O −5.0/atom(3원자 ⇒ f.u. −15.0)
        #   2Li + ½O₂ → Li2O ⇒ μ_O = E(Li2O) − 2E(Li) = −15.0 − (−2.0) = **−13.0**
        # Li2S(3원자 ⇒ −9.0) → Li2SO4(7원자 ⇒ −42.0), O 4개
        #   ⇒ μ_O = (−42.0 + 9.0)/4 = **−8.25**
        ents = [_FakeEntry("Li", -1.0), _FakeEntry("Li2O", -5.0),
                _FakeEntry("Li2S", -3.0), _FakeEntry("Li2SO4", -6.0)]

        mu, why = landmark_mu(ents, "Li", "Li2O", "O")
        chk(why is None and abs(mu - (-13.0)) < 1e-9,
            f"Li→Li2O 평형 μ_O 를 정확히 낸다 (기대 −13.0 · 얻음 {mu})")
        mu2, why2 = landmark_mu(ents, "Li2S", "Li2SO4", "O")
        chk(why2 is None and abs(mu2 - (-8.25)) < 1e-9,
            f"비-O 조성이 같으면 스케일 1 로 낸다 (기대 −8.25 · 얻음 {mu2})")
        _, w3 = landmark_mu(ents, "Li", "Li2SO4", "O")
        chk(w3 is not None, "⛔음성: 비-O 조성이 비례하지 않으면 **억지로 균형 잡지 않는다** "
                            "(Li→Li2SO4 는 S 가 환원형에 없다)")
        # ⚠ 2026-09-07 — 이 시험이 처음엔 "Nonexistent2O3" 하나로 **두 경로를 섞었다.**
        #   파싱을 고치자 실패 모드가 '화학식을 못 읽는다' 로 바뀌었고 시험은 옛 문구('hull')를
        #   찾다 죽었다. **코드가 아니라 시험이 틀린 것**이고, 갈라야 맞다.
        _, w4a = landmark_mu(ents, "Li", "Li2SO3", "O")     # 읽히지만 hull 에 없다
        chk(w4a is not None and "hull" in w4a,
            "⛔음성: **읽히지만 hull 에 없는 상**은 사유를 말하고 None")
        _, w4b = landmark_mu(ents, "Li", "Nonexistent2O3", "O")   # 아예 안 읽힌다
        chk(w4b is not None and "못 읽는다" in w4b,
            "⛔음성: **아예 못 읽는 화학식**에 예외로 죽지 않고 사유를 말한다 (오타 방어)")
        _, w5 = landmark_mu(ents, "Li2O", "Li2O", "O")
        chk(w5 is not None, "⛔음성: O 개수가 안 변하면 산화반응이 아니라고 말한다")

    print(f"  selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    main()
