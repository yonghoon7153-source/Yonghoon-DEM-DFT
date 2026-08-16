#!/usr/bin/env python3
"""esw_matched_factorial.py — Cl 치환분과 도펀트분을 **분해하는** 2×2 설계.

왜 필요한가
  캐스케이드 챔피언 표의 `delta_ox_vs_host_V` 는 같은 phase set 안의 값이라 **비교 가능**
  하지만, 후보와 host 가 여러 원자에서 동시에 다르므로 **귀속이 안 된다**.
  chain 변형(compound_set_chain)은 거기에 개입이 하나 더 들어가고, 17행 중 7행은
  치환 자리(P_4b → Li_24g)와 Li/P 화학량론까지 다르다.

  분해하려면 네 칸이 **같은 pinned entry set** 안에 있어야 한다:

      H_plain = Li24P4S20Cl4          4 f.u. host
      H_Cl    = Li23P4S19Cl5          S²⁻ 하나 → Cl⁻, 중성 유지로 Li⁺ 하나 빠짐
      D_plain = Li18M2P4S17Cl4O3      같은 자리 M₂O₃ 도핑
      D_Cl    = Li17M2P4S16Cl5O3      도핑 + 같은 Cl 치환

      baseline_cl_recipe_contrast    = f(H_Cl)    − f(H_plain)   ← 도펀트 없는 기준
      plain_dopant_recipe_contrast   = f(D_plain) − f(H_plain)
      conditional_cl_recipe_contrast = f(D_Cl)    − f(D_plain)   ← **도펀트가 있을 때**
      recipe_interaction             = conditional − baseline    (difference-in-differences)

  네 값이 같은 hull 에서 나와야 차가 의미를 갖는다. chemsys 는 후보마다 다르므로
  (도펀트 원소가 들어간다) **chemsys 마다 네 칸을 전부 다시 잰다** — host 를 84개
  chemsys 에서 다시 잰 것과 같은 이유다.

⛔⛔ 2026-08-16 (Codex 재감사) — 앞 판은 `H_Cl − f(H_plain)` 을 **main(Cl)** 이라 부르고
  그게 0 인 것을 "Cl 효과는 0" 이라고 썼다. **틀렸다.**
    · 그건 marginal main effect 가 아니라 **도펀트가 없는 기준점의 simple contrast** 다.
    · 도펀트가 있을 때의 recipe 효과는 `D_Cl − D_plain` 이고 Al +0.214 · B +0.283 ·
      Mo +0.216 · W +0.216 · Sc −0.017 로 **종마다 양·음·0** 이다.
    · 성립하는 문장은 **"Cl-rich 가 보편적으로 개선한다는 주장은 반증"** 까지이고
      **"Cl 효과가 0"** 은 아니다.
  또한 11종의 H 셀은 **모두 같은 두 조성**이다. 도펀트 원소는 H 분해에 참여할 수 없으므로
  11/11 은 독립 표본 11개가 아니라 **같은 host contrast 를 11개 확장 roster 에서 반복 확인**한
  것이다.

실행 (gabia — MP_API_KEY 필요, GPU 안 씀)
    python3 tools/oxidation/esw_matched_factorial.py \
        --out db/properties/oxidation_matched_factorial.json
    python3 tools/oxidation/esw_matched_factorial.py --selftest      # MP 없이

이 도구가 **못 하는 것**
  · 실제 구조를 만들지 않는다. grand-potential ESW 는 조성만 받으므로 조성식으로 충분하지만,
    그 조성이 **구조적으로 실현 가능한지**는 말하지 않는다. 자리 점유·배열은 이 계산 밖이다.
  · 그래서 여기서 나오는 것은 **조성 수준 operational contrast** 이지 원소 수준 인과 효과가
    아니다. 캐스케이드의 D_plain/D_Cl 과 조성은 맞춰도 **자리는 맞추지 못한다**
    (B/Mo/W 의 기존 plain 은 P_4b 라 이 설계의 D_plain 과 다른 물건이다).
  · 보편적 원소 효과로 승격하지 않는다 — 구조 생성 규약 안에서 정의된 대비다.
  · **전하 보상은 산화수를 검증하지 않는다.** 중성 M_xO_y 를 가정하고 양이온 총전하를
    `2·n_O` 로 잡는다. 현재 11종(중성 산화물)에는 맞지만 **일반 defect chemistry 규칙이
    아니다** — generator charge-compensation recipe 라고 부를 것.
  · **캐스케이드 값과 일치하는 것은 round-trip consistency 검사**이지 독립 물리 검증이
    아니다. 같은 조성·같은 entry roster·같은 알고리즘이면 같은 값이 나오는 게 당연하다.
  · Li 화학량론이 정수로 안 떨어지는 도펀트(1가·5가 등)는 **건너뛴다.** 억지로 반올림하면
    전하 중성이 깨진 조성을 재게 된다.
"""
import argparse, hashlib, json, os, sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

#: 4 f.u. 아지로다이트 host. 캐스케이드 챔피언 조성과 같은 기준이다.
HOST = {"Li": 24, "P": 4, "S": 20, "Cl": 4}

#: 이번 귀속에 필요한 최소 집합 — chain 챔피언 17행이 걸린 종.
#: (기호, 산화수, 화학식 라벨) — M₂O₃ 계열은 M 2개 + O 3개.
DEFAULT_DOPANTS = [
    ("Al2O3", {"Al": 2, "O": 3}), ("B2O3", {"B": 2, "O": 3}),
    ("Sc2O3", {"Sc": 2, "O": 3}), ("Y2O3", {"Y": 2, "O": 3}),
    ("Nd2O3", {"Nd": 2, "O": 3}), ("Sm2O3", {"Sm": 2, "O": 3}),
    ("MgO", {"Mg": 1, "O": 1}), ("ZnO", {"Zn": 1, "O": 1}),
    ("MoO3", {"Mo": 1, "O": 3}), ("WO3", {"W": 1, "O": 3}),
    ("La2O3", {"La": 2, "O": 3}),
]


def cl_swap(comp):
    """S²⁻ 하나를 Cl⁻ 로. 전하 중성을 위해 Li⁺ 하나가 빠진다 → 없으면 None."""
    c = dict(comp)
    if c.get("S", 0) < 1 or c.get("Li", 0) < 1:
        return None
    c["S"] -= 1
    c["Cl"] = c.get("Cl", 0) + 1
    c["Li"] -= 1
    return c


#: 이 recipe 가 가정하는 형식 전하. **일반 defect chemistry 규칙이 아니다** —
#: 캐스케이드 compound_set generator 의 charge-compensation recipe 를 재현한 것이다.
FORMAL_CHARGE = {"Li": +1, "P": +5, "S": -2, "Cl": -1, "O": -2}
#: 검산: Li24(+24) + P4(+20) + S20(-40) + Cl4(-4) = 0 ✓  (PS4³⁻ 의 P⁵⁺)


def formal_charge(comp, cation_charges):
    """조성의 형식 전하 총합. 모르는 원소가 있으면 (None, 사유)."""
    tot = 0.0
    for e, n in comp.items():
        z = FORMAL_CHARGE.get(e)
        if z is None:
            z = cation_charges.get(e)
        if z is None:
            return None, f"{e} 의 형식 전하를 모른다"
        tot += z * n
    return tot, None


def dope(host, dopant):
    """host 에 도펀트 산화물을 넣는다 — 캐스케이드 compound_set 규약과 같은 형태.

    O 는 S 자리를 채우고, 양이온은 Li 자리를 대체한다. 전하 중성은 Li 개수로 맞춘다.
    정수로 안 떨어지거나 **중성이 안 맞으면** (None, 사유) 를 돌려준다 — 반올림하지 않는다.

    ⛔ 2026-08-16 (Codex 재감사 B) — 앞 판은 `n_o_replaces_s` 라는 **쓰이지 않는 인자**를
      달고 있었고, "정수가 아니면 거부" 분기는 정수 O 개수에서 **도달 불가능**했다.
      이제 산화물이 중성이라는 가정에서 양이온 전하를 유도하고(2·n_O / n_cation),
      결과 조성의 형식 전하 총합이 0 인지 **실제로 검산한다**.
    """
    c = dict(host)
    n_o = dopant.get("O", 0)
    cations = {k: v for k, v in dopant.items() if k != "O"}
    n_cat = sum(cations.values())
    if not n_cat:
        return None, "양이온이 없는 도펀트"
    if n_o and c.get("S", 0) < n_o:
        return None, "S 가 O 개수보다 적다"
    if n_o:
        c["S"] -= n_o
        c["O"] = c.get("O", 0) + n_o
    # 중성 M_xO_y 이므로 양이온 총전하 = 2·n_O. 종당 전하가 정수가 아니면 거부한다.
    total_cation_charge = 2 * n_o
    per_cation = total_cation_charge / n_cat
    if abs(per_cation - round(per_cation)) > 1e-9:
        return None, (f"양이온 형식 전하가 정수가 아니다 "
                      f"({total_cation_charge}/{n_cat} = {per_cation})")
    if c.get("Li", 0) < total_cation_charge:
        return None, "Li 가 부족해 전하 보상이 안 된다"
    c["Li"] -= int(total_cation_charge)
    for k, v in cations.items():
        c[k] = c.get(k, 0) + v
    # 검산: 형식 전하 총합이 0 이어야 한다
    z, why = formal_charge(c, {k: int(round(per_cation)) for k in cations})
    if z is None:
        return None, why
    if abs(z) > 1e-9:
        return None, f"형식 전하 총합이 0 이 아니다 ({z:+g})"
    return c, None


def formula(comp):
    return "".join(f"{e}{int(n) if float(n).is_integer() else n}"
                   for e, n in sorted(comp.items()) if n)


def build_cells(host=None, dopants=None):
    """(라벨, 조성, 건너뛴 사유) 목록. MP 없이 돌아간다 — selftest 가 이걸 검사한다."""
    host = dict(host or HOST)
    out, skipped = [], []
    h_cl = cl_swap(host)
    if h_cl is None:
        raise SystemExit("host 에서 Cl 치환이 불가능하다")
    out.append(("__H_plain__", None, dict(host)))
    out.append(("__H_Cl__", None, dict(h_cl)))
    for name, dop in (dopants or DEFAULT_DOPANTS):
        d_plain, why = dope(host, dop)
        if d_plain is None:
            skipped.append((name, why)); continue
        d_cl = cl_swap(d_plain)
        if d_cl is None:
            skipped.append((name, "도핑 후 Cl 치환 불가")); continue
        out.append((f"{name}__D_plain", name, d_plain))
        out.append((f"{name}__D_Cl", name, d_cl))
    return out, skipped


def decompose(vals, eps=1e-9):
    """{라벨: onset} → 종마다 네 contrast. 값이 하나라도 없으면 그 종은 None.

    ⛔⛔ 2026-08-16 (Codex 재감사 P0-1) — 앞 판은 `H_Cl − H_plain` 을 **main(Cl)** 이라
      불렀다. 그건 2×2 factorial 의 marginal main effect 가 아니라 **도펀트가 없는
      기준점에서의 simple contrast** 다. 도펀트가 있을 때의 Cl-rich recipe 효과는
      `D_Cl − D_plain = (그 simple contrast) + interaction` 이고, Al/B/Mo/W 에서 **양수**다.
      그래서 "Cl 효과가 0" 은 성립하지 않는다. 성립하는 것은
      **"undoped 기준에서 이 recipe 는 onset 을 안 움직인다"** 까지다.

      이름을 바꿨다 (main → contrast):
        baseline_cl_recipe_contrast    = f(H_Cl)   − f(H_plain)   ← 도펀트 없는 기준
        plain_dopant_recipe_contrast   = f(D_plain)− f(H_plain)
        conditional_cl_recipe_contrast = f(D_Cl)   − f(D_plain)   ← **도펀트가 있을 때**
        recipe_interaction             = conditional − baseline   (difference-in-differences)

      difference-in-differences 자체는 비선형 응답에도 유효하다. 문제는 'main effect' 라는
      **이름**이 원소 수준 인과를 함의한 것이었다.
    """
    hp, hc = vals.get("__H_plain__"), vals.get("__H_Cl__")
    out = {}
    for k in vals:
        if not k.endswith("__D_plain"):
            continue
        sp = k[: -len("__D_plain")]
        dp, dc = vals.get(k), vals.get(f"{sp}__D_Cl")
        if None in (hp, hc, dp, dc):
            out[sp] = {"complete": False,
                       "missing": [n for n, v in (("H_plain", hp), ("H_Cl", hc),
                                                  ("D_plain", dp), ("D_Cl", dc)) if v is None]}
            continue
        out[sp] = {
            "complete": True,
            "H_plain_V": hp, "H_Cl_V": hc, "D_plain_V": dp, "D_Cl_V": dc,
            "baseline_cl_recipe_contrast_V": round(hc - hp, 4),
            "plain_dopant_recipe_contrast_V": round(dp - hp, 4),
            "conditional_cl_recipe_contrast_V": round(dc - dp, 4),
            "recipe_interaction_V": round((dc - dp) - (hc - hp), 4),
            "total_D_Cl_vs_host_V": round(dc - hp, 4),
            "isolated_element_effect": False,
            "scope": ("네 조성점 사이의 operational contrast 다. 특정 원자의 인과 효과가 아니다 "
                      "— 자리·구조·배열은 이 계산 밖이다."),
        }
    return out


def ladder_cells(host=None, n=5):
    """host 에서 −Li−S+Cl 을 n 번 반복한 사다리. 분기 전환이 **어디서** 일어나는지 본다.

    Li24P4S20Cl4 → Li23P4S19Cl5 → Li22P4S18Cl6 → …
    2×2 의 두 host 칸은 이 사다리의 처음 두 계단이다.
    """
    host = dict(host or HOST)
    out, c = [("__ladder0__", None, dict(host))], dict(host)
    for i in range(1, n + 1):
        nxt = cl_swap(c)
        if nxt is None:
            break
        out.append((f"__ladder{i}__", None, nxt))
        c = nxt
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="db/properties/oxidation_matched_factorial.json")
    ap.add_argument("--exclude", nargs="*", default=[],
                    help="경쟁상에서 뺄 reduced formula (예: --exclude LiS4). "
                         "기전 주장을 하려면 LiS4 제외판을 같이 돌려 부호가 유지되는지 봐야 한다")
    ap.add_argument("--ladder", type=int, default=0, metavar="N",
                    help="host 에서 -Li-S+Cl 을 N 번 반복한 사다리를 같이 잰다 "
                         "(분기 전환 지점을 찾는다). 0 이면 안 한다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("Set MP_API_KEY (gabia 에서 실행).")
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    from mp_api.client import MPRester
    Li = Element("Li")

    cells, skipped = build_cells()
    if a.ladder:
        # 사다리는 host 전용 칸이라 종 루프의 hosts 에 그대로 얹힌다
        cells = cells + [c for c in ladder_cells(n=a.ladder) if c[0] != "__ladder0__"]
        print(f"  사다리 {a.ladder}칸 추가 (host 에서 -Li-S+Cl 반복)")
    excl = {x.strip() for x in a.exclude if x.strip()}
    if excl:
        print(f"  ⚠ 경쟁상 제외: {sorted(excl)} — **다른 phase set 이다.** "
              f"기본판과 절대값을 섞지 말 것")
    for name, why in skipped:
        print(f"  ⏭ {name} 건너뜀 — {why}")

    # chemsys 는 **네 칸의 합집합**이다. 그래야 H/C/D/DC 가 한 hull 에 들어간다.
    by_species = defaultdict(list)
    for label, sp, comp in cells:
        by_species[sp].append((label, comp))
    hosts = by_species.pop(None)

    results, phase_sets, decomposed = {}, {}, {}
    for sp, items in sorted(by_species.items()):
        els = sorted({e for _l, c in items + hosts for e in c})
        with MPRester(key) as mpr:
            entries = mpr.get_entries_in_chemsys(
                els, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
        if excl:
            n0 = len(entries)
            entries = [e for e in entries
                       if e.composition.reduced_formula not in excl]
            print(f"    제외 {n0 - len(entries)}개 entry 제거")
            try:
                db_version = mpr.get_database_version()
            except Exception:
                db_version = None
        pd = PhaseDiagram(entries)
        muref = pd.el_refs[Li].energy_per_atom
        eids = sorted(str(getattr(e, "entry_id", "") or "") for e in entries)
        psid = hashlib.sha256("|".join(eids).encode()).hexdigest()[:16]
        # ★ 2026-08-16 (Codex 재감사 A) — entry ID 만 hash 하면 MP 가 **같은 ID 로 에너지나
        #   보정을 바꿔도** 지문이 안 변한다. energy_per_atom·correction 까지 묶은 별도
        #   지문을 같이 싣는다. 둘이 같아야 진짜 같은 hull 이다.
        payload = []
        for e in sorted(entries, key=lambda x: str(getattr(x, "entry_id", "") or "")):
            eid = str(getattr(e, "entry_id", "") or "")
            try: epa = f"{float(e.energy_per_atom):.9f}"
            except Exception: epa = "?"
            try: corr = f"{float(getattr(e, 'correction', 0.0)):.9f}"
            except Exception: corr = "?"
            payload.append(f"{eid}:{e.composition.reduced_formula}:{epa}:{corr}")
        efid = hashlib.sha256("|".join(payload).encode()).hexdigest()[:16]
        phase_sets[psid] = {"chemsys": "-".join(els), "n_entries": len(entries),
                            "entry_ids": eids, "db_version": db_version,
                            "thermo_types": ["GGA_GGA+U"], "exclusions": sorted(excl),
                            "energy_fingerprint": efid,
                            "fingerprint_contract": (
                                "phase_set_id = sha256(sorted entry_ids) — 목록 동일성. "
                                "energy_fingerprint = sha256(entry_id:formula:energy_per_atom:"
                                "correction) — **값 동일성**. 둘 다 같아야 같은 hull 이다."),
                            "n_duplicate_entry_ids": len(eids) - len(set(eids)),
                            "n_empty_entry_ids": sum(1 for x in eids if not x)}
        if len(eids) != len(set(eids)) or any(not x for x in eids):
            print(f"  ⚠ [{'-'.join(els)}] entry_id 중복 {len(eids)-len(set(eids))} · "
                  f"빈 값 {sum(1 for x in eids if not x)} — 지문 신뢰도 낮음")
        vals = {}
        for label, comp in hosts + items:
            try:
                prof = pd.get_element_profile(Li, Composition(comp))
                steps = [{"V": round(muref - float(p["chempot"]), 3),
                          "evo": round(float(p["evolution"]), 4),
                          "rxn": str(p["reaction"])} for p in prof]
                neg = [s for s in steps if s["evo"] < -1e-6]
                # ⛔ 2026-08-16 (Codex 재감사) — 앞 판은 onset 전압을 정한 뒤 **모든 step**
                #   중 |V-ox| 가 최소인 것을 다시 찾아 반응식을 골랐다. 같은 전압에 여러
                #   step 이 있으면(축퇴) onset 을 만든 negative-evolution step 이 아닌
                #   반응이 잡힐 수 있다. onset step 자체를 보존한다.
                onset_step = min(neg, key=lambda s: s["V"]) if neg else None
                ox = onset_step["V"] if onset_step else None
                n_tied = sum(1 for s in steps
                             if ox is not None and abs(s["V"] - ox) < 1e-9)
                vals[label] = ox
                results[f"{sp}/{label}"] = {
                    "species": sp, "cell": label, "formula": formula(comp),
                    "composition": comp, "oxidation_limit_V": ox,
                    "phase_set_id": psid, "n_entries": len(entries),
                    "oxidation_onset_rxn": onset_step["rxn"] if onset_step else None,
                    "oxidation_onset_evolution": onset_step["evo"] if onset_step else None,
                    "n_steps_at_onset_V": n_tied,
                    "onset_step_is_negative_evolution": bool(onset_step)}
            except Exception as e:
                vals[label] = None
                results[f"{sp}/{label}"] = {"species": sp, "cell": label,
                                            "formula": formula(comp),
                                            "phase_set_id": psid, "error": str(e)[:120]}
        d = decompose(vals)
        for k, v in d.items():
            v["phase_set_id"] = psid
        decomposed.update(d)
        print(f"  [{'-'.join(els)}] {len(entries)} entries · phase_set {psid}")
        if sp in d and d[sp].get("complete"):
            x = d[sp]
            print(f"    {sp:8s} main(Cl) {x['main_Cl_V']:+.3f} · "
                  f"main(dopant) {x['main_dopant_V']:+.3f} · "
                  f"interaction {x['interaction_V']:+.3f}")

    doc = {
        "method": ("matched 2x2 operational contrast, grand-potential ESW "
                   "(get_element_profile, MP GGA_GGA+U). 네 칸이 chemsys 마다 같은 "
                   "pinned entry set 안에 있다."),
        "exclusions": sorted(excl),
        "ladder_steps": a.ladder,
        "design": {"H_plain": formula(HOST), "H_Cl": formula(cl_swap(HOST)),
                   "D_plain": "host + M_xO_y (O→S 자리, 양이온 전하만큼 Li 제거)",
                   "D_Cl": "D_plain 에 같은 S→Cl 치환 (Li 하나 더 제거)",
                   "contrasts": {"main_Cl": "f(H_Cl) - f(H_plain)",
                                 "main_dopant": "f(D_plain) - f(H_plain)",
                                 "interaction": "[f(D_Cl)-f(D_plain)] - [f(H_Cl)-f(H_plain)]"}},
        "limits": [
            "조성 수준 열역학 대비다 — 자리 점유·구조 실현 가능성은 계산 밖이다",
            "캐스케이드의 B2O3·MoO3·WO3 plain 챔피언은 P_4b 자리라 이 설계의 D_plain 과 "
            "다른 물건이다. 조성은 맞춰도 자리는 못 맞춘다",
            "보편적 원소 효과가 아니라 이 구조 생성 규약 안의 대비다",
            "Li 전하 보상이 정수로 안 떨어지는 도펀트는 건너뛴다 (반올림 금지)",
        ],
        "skipped": [{"species": n, "why": w} for n, w in skipped],
        "phase_sets": phase_sets,
        "decomposition": decomposed,
        "results": results,
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
    print(f"\n-> {a.out}")
    print(f"   종 {len(decomposed)} · phase_set {len(phase_sets)} · 건너뜀 {len(skipped)}")


def selftest():
    """조성 산술과 분해식. **음성 경로 포함** — MP 없이 돈다."""
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            try: print(f"  ✗ {name}")
            except Exception: print(f"  FAIL {name}")

    # ── Cl 치환: S−1 · Cl+1 · Li−1 (전하 중성) ──────────────────────────────
    c = cl_swap(HOST)
    chk("H_Cl = Li23P4S19Cl5", c == {"Li": 23, "P": 4, "S": 19, "Cl": 5})
    chk("H_Cl 조성식", formula(c) == "Cl5Li23P4S19")
    # 음성 ①: S 가 없으면 치환 불가
    chk("음성: S 0 이면 None", cl_swap({"Li": 5, "S": 0, "Cl": 1}) is None)
    chk("음성: Li 0 이면 None", cl_swap({"Li": 0, "S": 5, "Cl": 1}) is None)
    # 음성 ②: 전하가 안 맞는 치환(Li 를 안 빼는 것)을 만들면 안 된다
    chk("음성: Li 를 유지하지 않는다", cl_swap(HOST)["Li"] == HOST["Li"] - 1)

    # ── 도핑: M2O3 → O 3개가 S 자리, Li 6개 제거 ────────────────────────────
    d, why = dope(HOST, {"Al": 2, "O": 3})
    chk("D_plain(Al2O3) = Li18Al2P4S17Cl4O3",
        d == {"Li": 18, "P": 4, "S": 17, "Cl": 4, "Al": 2, "O": 3})
    # 캐스케이드 실측 plain 챔피언(Al2O3)과 조성이 같아야 한다
    chk("캐스케이드 plain Al2O3 와 일치", formula(d) == "Al2Cl4Li18O3P4S17")
    dc = cl_swap(d)
    chk("D_Cl(Al2O3) = Li17Al2P4S16Cl5O3",
        dc == {"Li": 17, "P": 4, "S": 16, "Cl": 5, "Al": 2, "O": 3})
    # 캐스케이드 실측 chain 챔피언과도 일치해야 한다 (Al 은 exact 변환 종)
    chk("캐스케이드 chain Al2O3 와 일치", formula(dc) == "Al2Cl5Li17O3P4S16")
    d2, _ = dope(HOST, {"Mo": 1, "O": 3})
    chk("D_plain(MoO3) = Li18MoP4S17Cl4O3",
        d2 == {"Li": 18, "P": 4, "S": 17, "Cl": 4, "Mo": 1, "O": 3})
    # 음성 ③: S 가 O 보다 적으면 거부
    _bad, w = dope({"Li": 24, "P": 4, "S": 2, "Cl": 4}, {"Al": 2, "O": 3})
    chk("음성: S 부족이면 거부", _bad is None and "S" in w)
    # 음성 ④: Li 가 부족하면 거부 (전하 보상 불가)
    _bad2, w2 = dope({"Li": 2, "P": 4, "S": 20, "Cl": 4}, {"Al": 2, "O": 3})
    chk("음성: Li 부족이면 거부", _bad2 is None and "Li" in w2)
    # ── 형식 전하 검산 (2026-08-16 Codex 재감사 B) ──────────────────────────
    # host 자체가 중성이어야 한다: 24(+1) + 4(P는 PS4로 +5) ... P 는 FORMAL_CHARGE 에 없다
    z, why = formal_charge(HOST, {})
    chk("host 형식 전하 = 0", z is not None and abs(z) < 1e-9)
    chk("H_Cl 도 중성", abs(formal_charge(cl_swap(HOST), {})[0]) < 1e-9)
    # 음성 ⑦: 모르는 원소면 값을 만들지 않는다
    _z, _w = formal_charge({"Li": 1, "Xx": 1}, {})
    chk("음성: 모르는 원소 → None + 사유", _z is None and "Xx" in _w)
    # 음성 ⑧: 양이온당 전하가 정수가 아니면 거부 (M3O4 계열)
    _b3, w3 = dope(HOST, {"Fe": 3, "O": 4})
    chk("음성: 양이온당 전하 비정수면 거부", _b3 is None and "정수가 아니다" in w3)
    # 음성 ⑨: 양이온 없는 도펀트 거부
    _b4, w4 = dope(HOST, {"O": 2})
    chk("음성: 양이온 없으면 거부", _b4 is None and "양이온" in w4)
    # 양성: M2O3 는 양이온당 +3, MO 는 +2
    chk("M2O3 → 양이온당 +3", dope(HOST, {"Al": 2, "O": 3})[0]["Li"] == 24 - 6)
    chk("MO   → 양이온당 +2", dope(HOST, {"Mg": 1, "O": 1})[0]["Li"] == 24 - 2)
    chk("MO3  → 양이온당 +6", dope(HOST, {"Mo": 1, "O": 3})[0]["Li"] == 24 - 6)
    # 음성 ⑩: 안 쓰이는 인자가 남아 있으면 안 된다
    import inspect
    chk("음성: dope() 에 미사용 인자 없음",
        list(inspect.signature(dope).parameters) == ["host", "dopant"])

    # ── 셀 목록 ──────────────────────────────────────────────────────────────
    cells, skipped = build_cells()
    labels = [l for l, _s, _c in cells]
    chk("host 두 칸이 먼저", labels[:2] == ["__H_plain__", "__H_Cl__"])
    chk("종마다 두 칸", len(cells) == 2 + 2 * (len(DEFAULT_DOPANTS) - len(skipped)))
    chk("Al2O3 두 칸 존재",
        "Al2O3__D_plain" in labels and "Al2O3__D_Cl" in labels)

    # ── 사다리 (2026-08-16) ─────────────────────────────────────────────────
    lad = ladder_cells(n=4)
    chk("사다리 0칸 = host", lad[0][2] == HOST)
    chk("사다리 1칸 = H_Cl", lad[1][2] == {"Li": 23, "P": 4, "S": 19, "Cl": 5})
    chk("사다리 4칸", lad[4][2] == {"Li": 20, "P": 4, "S": 16, "Cl": 8})
    chk("사다리 라벨", [l for l, _s, _c in lad][:3]
        == ["__ladder0__", "__ladder1__", "__ladder2__"])
    # 음성 ⑪: S 가 바닥나면 더 안 만든다 (무한 생성 금지)
    short = ladder_cells({"Li": 3, "P": 1, "S": 2, "Cl": 1}, n=10)
    chk("음성: S 바닥나면 멈춘다", len(short) == 3)

    # ── 분해식 ───────────────────────────────────────────────────────────────
    v = {"__H_plain__": 2.140, "__H_Cl__": 2.200,
         "X__D_plain": 2.300, "X__D_Cl": 2.500}
    d3 = decompose(v)["X"]
    chk("baseline Cl contrast = +0.060",
        abs(d3["baseline_cl_recipe_contrast_V"] - 0.060) < 1e-9)
    chk("plain dopant contrast = +0.160",
        abs(d3["plain_dopant_recipe_contrast_V"] - 0.160) < 1e-9)
    chk("conditional Cl contrast = +0.200",
        abs(d3["conditional_cl_recipe_contrast_V"] - 0.200) < 1e-9)
    chk("interaction = +0.140", abs(d3["recipe_interaction_V"] - 0.140) < 1e-9)
    chk("총 대비 = +0.360", abs(d3["total_D_Cl_vs_host_V"] - 0.360) < 1e-9)
    # 음성 ⑤: baseline 이 0 이어도 conditional 은 0 이 아닐 수 있다 (Codex 재감사 P0-1)
    v0 = {"__H_plain__": 2.140, "__H_Cl__": 2.140,
          "AL__D_plain": 2.140, "AL__D_Cl": 2.354}
    d0 = decompose(v0)["AL"]
    chk("음성: baseline 0 인데 conditional 은 +0.214",
        abs(d0["baseline_cl_recipe_contrast_V"]) < 1e-9
        and abs(d0["conditional_cl_recipe_contrast_V"] - 0.214) < 1e-9)
    chk("음성: 'Cl 효과 0' 으로 읽히는 단일 필드가 없다",
        "main_Cl_V" not in d0 and "main_dopant_V" not in d0)
    chk("음성: 원소 수준 인과를 주장하지 않는다", d0["isolated_element_effect"] is False)
    # 음성 ⑥: 상호작용 0 이면 conditional == baseline
    v2 = {"__H_plain__": 2.0, "__H_Cl__": 2.1, "Y__D_plain": 2.3, "Y__D_Cl": 2.4}
    d4 = decompose(v2)["Y"]
    chk("음성: 가법이면 interaction 0",
        abs(d4["recipe_interaction_V"]) < 1e-9
        and abs(d4["conditional_cl_recipe_contrast_V"]
                - d4["baseline_cl_recipe_contrast_V"]) < 1e-9
        and abs(d4["total_D_Cl_vs_host_V"] - (d4["baseline_cl_recipe_contrast_V"]
                                              + d4["plain_dopant_recipe_contrast_V"])) < 1e-9)
    # 음성 ⑥: 값 하나가 없으면 계산하지 않는다 (0 으로 때우면 안 된다)
    d5 = decompose({"__H_plain__": 2.0, "__H_Cl__": None,
                    "Z__D_plain": 2.3, "Z__D_Cl": 2.4})["Z"]
    chk("음성: 결측이면 complete False", d5["complete"] is False)
    chk("음성: 무엇이 없는지 말한다", d5["missing"] == ["H_Cl"])
    chk("음성: 결측인데 값을 만들지 않는다", "recipe_interaction_V" not in d5)

    try: print(f"\nselftest: {ok} passed, {fail} failed")
    except Exception: print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
