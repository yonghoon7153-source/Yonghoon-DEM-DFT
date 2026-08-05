#!/usr/bin/env python3
"""build_cascade_themes.py — cascade v23 도펀트의 '테마별' 재구성 JSON.

테마 = 설계 질문 단위 12종. 각 도펀트에 테마별 정규화 점수 norm[theme]∈[0,1]
(방향 보정: 1=좋음)를 내장해 **임의 2+ 테마 조합**(기하평균·2D 산점도)을
프론트에서 바로 만들 수 있게 한다.

  oxidative_stability   산화 안정 (ox_V↑ + window)          [ESW CSV]
  reduction_anode       환원/음극 호환 (red_V↓)              [ESW CSV]
  electronic_insulation 전자 절연 (문헌 전형 갭↑)            [큐레이션]
  ionic_transport       Li 수송 (BVS proxy x005↑, blocking↓) [litransport]
  disorder_promotion    무질서 유도 (Li-Li disorder std↑)     [litransport]
  dose_robustness       농도 강건성 (BVS x002→x010 유지)      [litransport]
  lightweight           경량 (mass/cation↓)                  [화학식]
  low_cost              저비용 (가격 정성등급↓)              [큐레이션]
  mechanical_soft       연질 (E↓)                            [ranked]
  ductility             연성 (Pugh B/G↑)                     [ranked]
  air_stability         공기/수분 내성 (HSAB soft-S 친화+F)   [큐레이션]
  structure_stability   도핑 구조 안정 (Δe↓)                 [ranked]
  (+ balanced           기존 합성 score — 참고용)

큐레이션 항목(gap·cost·HSAB)은 문헌 전형값/정성 등급이며 우리 계산값 아님 —
필드에 명시. litdb 앵커: zhu2020(공기안정 설계), taklu2021/li2025(Cu–S 보호).

출력: db/properties/cascade_v23_themes.json
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"

MASS = {"H": 1.008, "Li": 6.94, "B": 10.81, "C": 12.011, "N": 14.007, "O": 15.999,
        "F": 18.998, "Na": 22.99, "Mg": 24.305, "Al": 26.982, "Si": 28.085,
        "P": 30.974, "S": 32.06, "Cl": 35.45, "K": 39.098, "Ca": 40.078,
        "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
        "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
        "Ga": 69.723, "Ge": 72.63, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
        "Nb": 92.906, "Mo": 95.95, "Ag": 107.868, "In": 114.818, "Sn": 118.71,
        "Sb": 121.76, "Ba": 137.327, "La": 138.905, "Nd": 144.242, "Sm": 150.36,
        "Gd": 157.25, "Hf": 178.49, "Ta": 180.948, "W": 183.84}

# 가격 정성 등급 (1 저가 ~ 5 고가). 2026 시장 감각 큐레이션 — 절대 시세 아님.
COST_TIER = {"Al": 1, "Mg": 1, "Ca": 1, "Na": 1, "Fe": 1, "Si": 1, "Mn": 1,
             "B": 2, "Ti": 2, "Zr": 2, "Zn": 2, "Cu": 2, "Cr": 2, "Ba": 2,
             "Sr": 2, "Li": 2, "Sn": 3, "Sb": 3, "Mo": 3, "V": 3, "Co": 3,
             "Ni": 3, "La": 3, "W": 4, "Nb": 4, "Y": 4, "Nd": 4, "Sm": 4,
             "Ag": 4, "Ge": 4, "Sc": 5, "Hf": 5, "Ta": 5, "Gd": 5, "In": 5,
             # ml-15: Ga 만 누락돼 .get(cat, 3) 기본값으로 조용히 tier 3 을 받고 있었다
             #   (큐레이션된 Sn/Sb/Mo/V/Co/Ni/La 과 구별 불가). Ga 는 값비싼 minor metal → 4.
             "Ga": 4}

# 문헌 전형 밴드갭 (eV, ±0.5 수준 큐레이션 — 우리 계산값 아님).
# kb/molecular_orbitals.json 부류와 정합.
GAP_LIT = {"LiF": 14, "MgF2": 12, "CaF2": 12, "AlF3": 11, "ScF3": 10, "YF3": 10,
           "LaF3": 10, "NdF3": 9, "ZrF4": 9, "TiF4": 7,
           "SiO2": 9, "Al2O3": 8.8, "MgO": 7.8, "Li2O": 7, "CaO": 7,
           "B2O3": 6.2, "Sc2O3": 6, "SrO": 6, "HfO2": 5.7, "Y2O3": 5.6,
           "La2O3": 5.5, "ZrO2": 5.5, "Gd2O3": 5.4, "Na2O": 5, "Nd2O3": 4.7,
           "Ga2O3": 4.8, "Sm2O3": 4.6, "GeO2": 4.5, "BaO": 4, "NiO": 4,
           "Ta2O5": 4, "MnO": 3.9, "SnO2": 3.6, "Cr2O3": 3.4, "Nb2O5": 3.4,
           "ZnO": 3.3, "TiO2": 3.2, "Sb2O5": 3.0, "MoO3": 3.0, "In2O3": 2.9,
           "WO3": 2.7, "CoO": 2.5, "V2O5": 2.3, "Fe2O3": 2.2, "Cu2O": 2.1,
           "CrO3": 2.0, "Ag2O": 1.3}

# HSAB: S²⁻(soft base)와 잘 결합해 PS₄를 보호하는 양이온 (taklu2021 Cu–S,
# li2025 CuBr₂ — soft/borderline acid가 황화물 공기내성↑). Pearson 분류 기반.
# ml-13: 원소 심볼만으로 키를 잡으면 산화수가 무시돼 SnO2(Sn(IV))·Sb2O5(Sb(V))·In2O3(In(III))가
# Pearson 이 Sn(II)/Sb(III) 에 주는 borderline 등급을 물려받는다. Pearson 상 Sn(IV)·Sb(V)·In(III)은
# hard acid 다. → (원소, 산화수) 로 키를 잡아 로스터가 늘어도 잘못된 등급을 조용히 상속하지 못하게.
# ⚠⚠ **이 등급의 이름과 근거가 부정확하다 — 2026-08-05 [Zhu20] SI 로 검산해서 확인.**
#   `air_hsab` 라는 이름은 "HSAB 로 공기안정을 판정한다" 는 뜻인데, 실제 구동변수는
#   **soft/hard 가 아니라 oxophilicity**(양이온이 S 대신 O 를 얼마나 원하나)다.
#   증거: 같은 원소가 산화수로 뒤집힌다(Sb³⁺ +0.535 ↔ Sb⁵⁺ −0.167, Δ0.70 eV) — HSAB 로는
#   설명 안 되고 산물 산화물의 안정성으로는 설명된다. Zn²⁺(+1.081) > Ag⁺(+1.040) 도 마찬가지.
#
#   **검산 결과 (36종 중 산화수까지 맞춰 대조 가능한 35종)**: 맞음 26 · **어긋남 9**.
#   어긋난 9종이 **전부 같은 방향** — 우리가 0.2(비보호)로 깎았는데 문헌은 보호적:
#     In³⁺ +0.599 · Sn⁴⁺ +0.441 · Ba²⁺ +0.422 · Na⁺ +0.416 · Ge⁴⁺ +0.412 ·
#     Ga³⁺ +0.362 · Sr²⁺ +0.359 · Ca²⁺ +0.264 (CaO·CaF₂)
#   즉 이 등급은 **Cu/Ag/Zn 밖의 양이온을 체계적으로 과소평가**한다.
#   ⚠ 특히 **In³⁺** — 문헌(InF₃ 치환 아지로다이트)이 효과를 보고하는 계열인데 우리 등급은 최하다.
#
#   ✅ 반대로 **산화수를 키로 쓴 결정(ml-13)은 검산으로 정당화됐다**:
#     Sb₂O₅→Sb⁵⁺ −0.167 · TiO₂→Ti⁴⁺ −0.304 · ZrO₂ −0.459 · SiO₂ −0.847 · B₂O₃ −0.901
#     전부 우리 0.2 등급과 일치. 원소 심볼만 썼으면 Sb 를 borderline 으로 잘못 올렸을 것이다.
#
#   → **처방은 `open_items` #12**: [Zhu20] 레시피로 ΔG_hyd 를 직접 계산해 이 정성 등급을
#     대체한다. 그전까지 이 열은 **Cu/Ag/Zn 계열 식별용**으로만 쓰고, 낮은 등급을
#     "공기 불안정" 으로 읽지 말 것(= 판정 없음).
#   상세: kb/open_items.md #13 · db/properties/zhu2020_si_hydrolysis_energies.csv
HSAB_SOFT_OX = {("Cu", 1), ("Cu", 2), ("Ag", 1)}
HSAB_BORDERLINE_OX = {("Zn", 2), ("Ni", 2), ("Co", 2), ("Sn", 2), ("Sb", 3), ("In", 1)}

FORMULA_RE = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_formula(f):
    out = {}
    for sym, n in FORMULA_RE.findall(f):
        if sym:
            out[sym] = out.get(sym, 0) + (int(n) if n else 1)
    return out


def cation_of(f):
    comp = parse_formula(f)
    for s in comp:
        if s not in ("O", "F"):
            return s, comp[s]
    return None, 0


def cation_oxidation_state(formula):
    """산화물/불화물 화학량론에서 양이온 산화수를 유도. 예: SnO2 -> ('Sn', 4), Sb2O5 -> ('Sb', 5).
    ml-13: HSAB 등급을 원소 심볼만으로 키잡으면 Sn(IV)/Sb(V)/In(III) 가 Pearson 이 Sn(II)/Sb(III) 에
    주는 borderline 을 조용히 물려받는다."""
    comp = parse_formula(formula)
    cat, ncat = cation_of(formula)
    if not cat or not ncat:
        return None, None
    anion_charge = 2 * comp.get("O", 0) + 1 * comp.get("F", 0)
    if not anion_charge:
        return cat, None
    ox = anion_charge / ncat
    return cat, (int(round(ox)) if abs(ox - round(ox)) < 1e-6 else round(ox, 2))


def hsab_grade(formula):
    """HSAB 등급 (soft 1.0 / borderline 0.6 / hard 0.2) — (원소, 산화수) 키."""
    cat, ox = cation_oxidation_state(formula)
    if (cat, ox) in HSAB_SOFT_OX:
        return 1.0
    if (cat, ox) in HSAB_BORDERLINE_OX:
        return 0.6
    return 0.2


def cost_tier_of(cat, comp):
    """ml-15: 미큐레이션 양이온은 조용한 기본값 대신 즉시 실패시킨다 (로스터가 고정 47종이라
    빌드타임 KeyError 가 잘못된 등급을 배포하는 것보다 싸다)."""
    if cat not in COST_TIER:
        raise KeyError(f"COST_TIER 에 없는 양이온 '{cat}' — 등급을 명시 등록할 것 "
                       f"(조용한 기본값 3 은 큐레이션 값과 구별 불가라 금지)")
    return COST_TIER[cat] + (0.5 if "F" in comp else 0.0)


def read_csv_rows(path):
    with open(path) as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── [Zhu20] 문헌 가수분해 ΔG (소환값 A층) ────────────────────────────────────
# db/properties/zhu2020_si_hydrolysis_energies.csv 는 Angew. Chem. 2020, 59, 17472 의
# SI xlsx 전수 전사본이다. **우리 계산이 아니다** — 소환값이므로 아래 3가지를 지킨다:
#   ① 필드 이름에 `_lit` 를 박는다 (우리 산출 열과 눈으로 구분).
#   ② 인용 시 방법(MP GGA-PBE 형성에너지 + NIST-JANAF 기체/수산화물 혼합 스킴)과
#      부분압 조건(x(H2O)=0.1 %, x(H2S)=x(HCl)=1 ppm)을 같이 적는다.
#   ③ **염화물 시트는 규약이 어긋난다** (논문이 HCl 1 ppm 보정을 빠뜨린 것으로 보임 —
#      CSV 머리말의 교차검증 3건 참조). 그래서 as_published 와 우리 환산값을 **둘 다** 낸다.
# 매칭 키 = (양이온 원소, 산화수). 산화수를 무시하면 Sb³⁺(+0.535) 와 Sb⁵⁺(−0.167) 가
# 0.70 eV 나 뒤집히는데 같은 값을 받는다 — ml-13 과 같은 이유로 산화수까지 맞춘다.
CATION_RE = re.compile(r"^([A-Z][a-z]?)(\d*)([+-])$")


def _cation_key(cation_str):
    """'In3+' -> ('In', 3).  CSV 의 cation 열 표기를 (원소, 산화수) 로."""
    m = CATION_RE.match((cation_str or "").strip())
    if not m:
        return None
    return m.group(1), int(m.group(2) or 1)


def load_zhu2020():
    """M-S(이성분 황화물) / M-Cl(이성분 염화물) 시트를 (원소, 산화수) 키로."""
    p = PROP / "zhu2020_si_hydrolysis_energies.csv"
    if not p.exists():
        return {}, {}
    ms, mcl = {}, {}
    for r in read_csv_rows(p):
        key = _cation_key(r.get("cation"))
        if not key:
            continue
        tgt = ms if r.get("system") == "binary_sulfide" else mcl
        # 같은 (원소, 산화수) 가 두 번 나오면 전사 오류다 — 조용히 덮지 않는다.
        if key in tgt:
            raise KeyError(f"[Zhu20] {r['source_sheet']} 시트에 {key} 가 중복 — CSV 전사 확인 필요")
        tgt[key] = r
    return ms, mcl


def main():
    ranked = read_csv_rows(PROP / "cascade_v23_ranked.csv")
    oxid = {r["dopant"]: r for r in read_csv_rows(PROP / "oxidation_stability_cascade.csv")}
    lit = {}
    for r in read_csv_rows(PROP / "cascade_v23_litransport.csv"):
        d, _, x = r["_dir"].rpartition("_x")
        lit.setdefault(d, {})[x] = r

    zhu_ms, zhu_mcl = load_zhu2020()

    rows = []
    for r in ranked:
        d = r["dopant"]
        cat, ncat = cation_of(d)
        comp = parse_formula(d)
        fmass = sum(MASS[s] * n for s, n in comp.items())
        ox = oxid.get(d, {})
        l2, l5, l10 = (lit.get(d, {}).get(x, {}) for x in ("002", "005", "010"))
        b2, b5, b10 = (fnum(l.get("bvs_li_proxy_score")) for l in (l2, l5, l10))
        hsab = hsab_grade(d)
        air = min(1.0, hsab + (0.25 if "F" in comp else 0.0))  # F 화학 내습 보너스
        zkey = cation_oxidation_state(d)
        zs, zc = zhu_ms.get(zkey), zhu_mcl.get(zkey)
        rows.append({
            "dopant": d, "group": r.get("group"), "cation": cat,
            "score": fnum(r.get("score")), "pareto": r.get("pareto", ""),
            "ox_V": fnum(ox.get("ox_V")) or fnum(r.get("ox_V")),
            "red_V": fnum(ox.get("red_V")) or fnum(r.get("red_V")),
            "window_V": fnum(ox.get("window_V")),
            "clrich_ox_V": fnum(ox.get("clrich_ox_V")),
            "esw_note": (ox.get("note") or "").strip(),
            "gap_lit_eV": GAP_LIT.get(d),
            "bvs_x002": b2, "bvs_x005": b5, "bvs_x010": b10,
            "bvs_slope": (round(b10 - b2, 4) if (b10 is not None and b2 is not None) else None),
            "blocking": fnum(l5.get("tier2_dopant_blocking_fraction")),
            "disorder_std": fnum(l5.get("tier2_li_li_disorder_std")),
            "mass_per_cation": round(fmass / ncat, 2) if ncat else None,
            "cost_tier": cost_tier_of(cat, comp),
            # ⚠ 이름 정정 진행 중 — 실제 구동변수는 HSAB softness 가 아니라 oxophilicity 다.
            #   기존 키(air_hsab)는 하위호환으로 남기고, 뜻이 맞는 이름을 같이 낸다.
            #   소비자(codoping_ml.py·webapp)를 옮긴 뒤 air_hsab 를 뺄 것 — open_items #13.
            "air_hsab": round(air, 2),
            "air_protect_tier": round(air, 2),
            # F 보너스를 뺀 **순수 HSAB 등급**. [Zhu20] 대조는 이 열로 해야 맞는다 —
            # 검증 대상이 "HSAB 로 공기안정을 판정할 수 있나" 이지 "F 화학이 좋은가" 가 아니다.
            "hsab_grade_raw": hsab,
            # ── 소환값 A층 ([Zhu20] SI) — 우리 계산 아님. `_lit` 접미사가 그 표식이다.
            #   같은 양이온·같은 산화수의 **이성분 황화물** 가수분해 ΔG (eV per H2O).
            #   양수 = 수분에 안정, 음수 = 자발 가수분해. 기준선 Li2S = +0.225.
            "dG_hyd_MS_lit": fnum(zs.get("dG_hyd_eV_per_H2O_as_published")) if zs else None,
            "dG_hyd_MS_ref": (f"{zs['compound']} ({zs['mp_entry_id']})" if zs else None),
            #   염화물 축 — 아지로다이트의 Cl 부격자에 대응. ⚠ 논문 값(pub)과 우리 환산값(ours)이
            #   다르다(HCl 1 ppm 보정 누락 추정). **둘을 같은 표에 섞어 쓰지 말 것.**
            "dG_hyd_MCl_lit_pub": fnum(zc.get("dG_hyd_eV_per_H2O_as_published")) if zc else None,
            "dG_hyd_MCl_preset_ours": fnum(zc.get("dG_hyd_eV_per_H2O_preset_OURS")) if zc else None,
            "dG_hyd_MCl_ref": (f"{zc['compound']} ({zc['mp_entry_id']})" if zc else None),
            "E_GPa": fnum(r.get("E_GPa")), "pugh": fnum(r.get("pugh")),
            "de": fnum(r.get("de")),
        })

    # (key, direction +1=클수록 좋음, gate) — norm 계산과 top 목록의 단일 정의
    THEMES = {
        "oxidative_stability": ("ox_V", +1, lambda r: (r.get("window_V") or 0) > 0.05),
        "reduction_anode": ("red_V", -1, lambda r: (r.get("window_V") or 0) > 0.05),
        "electronic_insulation": ("gap_lit_eV", +1, None),
        "ionic_transport": ("bvs_x005", +1, lambda r: (r.get("blocking") or 1) < 0.6),
        "disorder_promotion": ("disorder_std", +1, None),
        "dose_robustness": ("bvs_slope", +1, None),
        "lightweight": ("mass_per_cation", -1, None),
        "low_cost": ("cost_tier", -1, None),
        "mechanical_soft": ("E_GPa", -1, None),
        # ⚠ ml-1: 이 열은 Pugh B/G 가 아니라 **G/B** 다(champions csv 의 elastic_pugh_GoverB).
        #   +1 이면 "G/B 클수록 좋다" = 가장 취성인 것을 연성 1위로 올린다 — 실제로 배포된
        #   ductility top10 이 로스터에서 가장 취성인 10종이었다. 연성 = 낮은 G/B → -1.
        #   (score 쪽 plot_cascade_insights.py:70 은 norm(...,better_hi=False) 로 이미 올바르다.)
        "ductility": ("pugh", -1, None),
        # open_items #13 step2 — 소비자를 뜻이 맞는 키로 옮긴다(`air_hsab` 는 하위호환 유지).
        "air_stability": ("air_protect_tier", +1, None),
        # ★ 신설 — 정성 등급(`air_protect_tier`)의 **문헌 대조축**. 소환값이라 별도 테마로 둔다.
        #   ⚠ 47종 중 35종만 커버된다(M-S 표에 같은 산화수가 있는 것). 나머지 12종은 None →
        #   norm 도 None 이고, **프론트 조합에서 0 이 아니라 '제외'로 처리해야 한다**(cascade.html).
        "air_stability_lit": ("dG_hyd_MS_lit", +1, None),
        "structure_stability": ("de", -1, None),
        "balanced": ("score", +1, None),
    }

    # ── 정규화 ────────────────────────────────────────────────────────────────
    # ml-6: air_hsab 는 이미 [0.2, 1.0] 의 **절대 등급**(4단계)이다. 여기에 min-max 를 걸면
    #   최빈 등급 0.2("HSAB 보호 기대 없음", 47개 중 29개)가 정확히 0.0 으로 떨어지고,
    #   themes.json 이 스스로 문서화한 기하평균 combine 규칙에서 그 29종이 **말살**된다
    #   ("보호 없음" ≠ "실격"). → 이 축만 절대 등급을 그대로 norm 으로 쓴다.
    # ml-7: 게이트는 min(n, 0.05) **캡**이라, 게이트를 통과했는데 원값이 로스터 최소인 도펀트는
    #   0.0 이 되어 게이트 **탈락자 24종(0.05)보다 아래**로 밀렸다(ionic_transport 의 B2O3).
    #   → 통과자를 [GATE_FLOOR+EPS, 1.0] 로 재스케일하고 탈락자는 전부 GATE_FLOOR 로 평탄화해
    #   게이트 상태와 metric 값이 절대 교차하지 못하게 한다. 탈락자끼리의 가짜 순서도 사라진다.
    #   ⚠ 이 층(여기)에서만 바닥을 준다 — 프런트엔드 combine(cascade.html)에는 넣지 말 것(이중 바닥).
    GATE_FLOOR, GATE_EPS = 0.05, 0.05
    ABSOLUTE_GRADE = {"air_stability"}          # min-max 대신 원 등급을 그대로 쓰는 축

    for tkey, (mkey, sign, gate) in THEMES.items():
        vals = [r[mkey] for r in rows if r.get(mkey) is not None]
        lo, hi = min(vals), max(vals)
        span = (hi - lo) or 1.0
        for r in rows:
            v = r.get(mkey)
            if v is None:
                r.setdefault("norm", {})[tkey] = None
                continue
            if tkey in ABSOLUTE_GRADE:
                n = v if sign > 0 else (1.0 - v)
                n = min(max(n, 0.0), 1.0)
            else:
                n = (v - lo) / span
                if sign < 0:
                    n = 1.0 - n
            if gate:
                if gate(r):
                    n = GATE_FLOOR + GATE_EPS + n * (1.0 - GATE_FLOOR - GATE_EPS)
                else:
                    n = GATE_FLOOR      # 평탄 — 탈락자 사이엔 순서 없음
            r.setdefault("norm", {})[tkey] = round(n, 4)

    def top(tkey, n=10):
        pool = [r for r in rows if r["norm"].get(tkey) is not None]
        # 안정 정렬이라 동점 순서 = ranked.csv(=score) 순서 = 결정론적 2차 키.
        pool.sort(key=lambda r: r["norm"][tkey], reverse=True)
        return [r["dopant"] for r in pool[:n]]

    def tie_at_cut(tkey, n=10):
        """ml-14: 절단선 값이 동점인 도펀트 수 / 그 때문에 잘려나간 수."""
        pool = [r for r in rows if r["norm"].get(tkey) is not None]
        if len(pool) <= n:
            return {"tied_at_cut": 0, "dropped_by_tie": 0}
        pool.sort(key=lambda r: r["norm"][tkey], reverse=True)
        cut = pool[n - 1]["norm"][tkey]
        tied = [r["dopant"] for r in pool if r["norm"][tkey] == cut]
        shown = sum(1 for r in pool[:n] if r["norm"][tkey] == cut)
        return {"tied_at_cut": len(tied), "dropped_by_tie": max(0, len(tied) - shown),
                "cut_value": cut,
                "tie_break": "cascade score 순 (ranked.csv 행 순서, 안정 정렬)"}

    T = {
        "oxidative_stability": {"label": "산화 안정성", "icon": "🛡️",
            "question": "고전압 양극 계면에서 SE 산화를 막을 도펀트는?",
            "metric": "ox_V (V vs Li) ↑ · window>0.05 게이트",
            "caveat": "ox_V 축퇴(19개가 2.14, 호스트 pin) — 축퇴군 내 순위 무의미. F 화학 유리."},
        "reduction_anode": {"label": "환원 안정성 (음극측)", "icon": "🔻",
            "question": "Li 금속 쪽에서 환원 분해가 늦은 도펀트는?",
            "metric": "red_V (V vs Li) ↓ · collapse 게이트",
            "caveat": "낮은 red_V = Li까지 버티는 창. 후기 TM(Fe/Co/Ni/Mn)·V/Cr⁶⁺ 회피."},
        "electronic_insulation": {"label": "전자 절연", "icon": "⚡",
            "question": "전자 누설(덴드라이트 씨앗)을 막을 넓은 갭 도펀트는?",
            "metric": "문헌 전형 밴드갭 (eV) ↑ — 큐레이션 값(우리 계산 아님)",
            "caveat": "불화물≫폐각 산화물>d⁰>후기TM/d¹⁰(TCO·Ag₂O 위험). ±0.5 eV 등급용."},
        "ionic_transport": {"label": "Li 수송 유지", "icon": "🔋",
            "question": "도핑해도 Li 채널을 안 막는 도펀트는?",
            "metric": "BVS Li proxy (x=0.05) ↑ · blocking<0.6 게이트",
            "caveat": "BVSE·기하 프록시 — 절대 σ 아님."},
        "disorder_promotion": {"label": "음이온 무질서 유도 (anti-site)", "icon": "🌀",
            "question": "anti-site/자리 무질서를 키워 σ를 올릴 후보는?",
            "metric": "Li–Li disorder std (x=0.05) ↑",
            "caveat": "무질서→σ↑는 우리 comp2 disorder 캠페인과 같은 가설 축 — 프록시 단계."},
        "dose_robustness": {"label": "도핑 농도 내성", "icon": "📈",
            "question": "도핑량을 올려도(x0.02→0.10) 수송이 안 죽는 도펀트는?",
            "metric": "BVS proxy 기울기 (x010−x002) ↑",
            "caveat": "양수 = 농도 올릴 여지. 음수 크면 저농도 한정 도펀트."},
        "lightweight": {"label": "경량 원소", "icon": "🪶",
            "question": "코팅 질량 페널티(Wh/kg)를 최소화할 도펀트는?",
            "metric": "formula mass / cation (g/mol) ↓",
            "caveat": "B·Mg·Al·Si·Na 경량군 — 성능 게이트와 교차 필수."},
        "low_cost": {"label": "저비용", "icon": "💰",
            "question": "스케일업 원료비 부담이 없는 도펀트는?",
            "metric": "가격 정성등급 (1~5) ↓ — 2026 시장감각 큐레이션, 절대시세 아님",
            "caveat": "Sc/Hf/Ta/Gd/In 고가군은 성능 압도적일 때만."},
        "mechanical_soft": {"label": "연질 (저강성)", "icon": "🧲",
            "question": "낮은 E로 계면 접촉을 순응시킬 도펀트는?",
            "metric": "Young's E (GPa, UMA) ↓",
            "caveat": "절대값은 UMA 부풀림 — 내부 상대비교만."},
        "ductility": {"label": "연성 (Pugh)", "icon": "🥨",
            "question": "취성 파괴 대신 소성 변형으로 버틸 도펀트는?",
            "metric": "G/B ↓ (= Pugh B/G ↑)",
            "caveat": "열 이름은 pugh 지만 값은 **G/B**(champions csv elastic_pugh_GoverB)라 낮을수록 연성. "
                      "실제 B/G = 1/pugh 이고 로스터 범위가 0.98–1.59 라 **47종 어느 것도 B/G>1.75 연성 "
                      "경험칙을 못 넘는다**. 동점 다수 — tie_count_at_cut 참조. UMA 상대."},
        "air_stability": {"label": "공기/수분 내성 (정성 등급)", "icon": "🌫️",
            "question": "H₂S 발생·가수분해를 억제할 도펀트는?",
            "metric": "HSAB soft-S 친화 등급 + F 보너스 ↑ — 큐레이션",
            "caveat": "soft acid(Cu·Ag)가 S 보호(taklu2021·li2025) but 전자절연과 정면 상충 — co-doping 동기. "
                      "⚠⚠ **낮은 등급 = '판정 없음'이지 '공기 불안정' 아님** — [Zhu20] SI 대조에서 35종 중 9종이 "
                      "어긋났고 **전부 과소평가 방향**(In³⁺·Sn⁴⁺·Ba²⁺·Na⁺·Ge⁴⁺·Ga³⁺·Sr²⁺·Ca²⁺). "
                      "이 축으로 도펀트를 탈락시키지 말 것. **문헌 대조는 아래 `air_stability_lit` 를 볼 것.**"},
        "air_stability_lit": {"label": "공기/수분 내성 (문헌 ΔG_hyd)", "icon": "💧",
            "question": "같은 양이온의 이성분 황화물이 물과 만나면 실제로 어떻게 되나?",
            "metric": "ΔG_hyd (eV per H₂O) ↑ — **[Zhu20] 문헌 소환값, 우리 계산 아님**",
            "caveat": "★ 위 정성 등급의 **대조축**. 양수 = 수분에 안정, 음수 = 자발 가수분해. 기준선 **Li₂S = +0.225**. "
                      "⚠ **소환값 규율**: Angew. Chem. 2020, 59, 17472 SI 값이며 계산 수준이 우리와 다르다 "
                      "(MP GGA-PBE 형성에너지 + NIST-JANAF 기체/수산화물 혼합 스킴, x(H₂O)=0.1 % · x(H₂S)=1 ppm, 300 K). "
                      "우리 db 절대값과 같은 축에 놓지 말 것. "
                      "⚠ **커버리지 35/47** — 나머지 12종(Cr·W·Nb·Ta·Mo·Mg·V·Fe·Co·Ni 계열)은 M-S 표에 "
                      "같은 산화수가 없어 **판정 없음**이다. 조합 랭킹에서 0 이 아니라 **제외**로 처리한다. "
                      "⚠ 도펀트는 산화물/불화물인데 대조는 **이성분 황화물** 기준이다 — 'PS₄ 골격을 지킬 양이온인가' "
                      "라는 질문의 프록시이지 코팅 자체의 안정성이 아니다."},
        "structure_stability": {"label": "도핑 구조 안정", "icon": "🏗️",
            "question": "host에 넣었을 때 에너지 페널티가 없는(음수) 도펀트는?",
            "metric": "Δe (doped − host, UMA) ↓",
            "caveat": "Δe<0 = baseline보다 안정. UMA 상대값."},
        "balanced": {"label": "종합 균형 (기존 score)", "icon": "⚖️",
            "question": "전 항목 균형 후보는? (기존 cascade 가중합)",
            "metric": "score = 0.30 ox + 0.25 stable + 0.20 soft + 0.15 ductile + 0.10 window",
            "caveat": "score 차 ~0.02는 동점. DFT 검증은 Nd₂O₃·B₂O₃뿐."},
    }
    for tkey, meta in T.items():
        meta["key"] = tkey
        meta["metric_key"] = THEMES[tkey][0]
        meta["direction"] = "+" if THEMES[tkey][1] > 0 else "-"
        meta["top"] = top(tkey)
        meta.update(tie_at_cut(tkey))
        if meta.get("dropped_by_tie"):
            meta["caveat"] = (meta.get("caveat", "") +
                              f"  ⚠ 10위 값 동점 {meta['tied_at_cut']}종 중 {meta['dropped_by_tie']}종이 "
                              "표시에서 잘림 — 동점군 내 순위는 무의미(2차 키는 cascade score).").strip()

    out = {
        "property": "cascade_v23_themes",
        "date": "2026-07-27",
        "description": ("cascade v23 도펀트의 테마별 재구성(12+1 테마). 각 도펀트에 "
                        "norm[theme]∈[0,1](1=좋음, 방향보정·게이트 반영) 내장 — 임의 테마 "
                        "2+개 조합(기하평균/산점도)은 프론트에서 norm으로 계산."),
        "combine_rule": "combined = (∏ norm_i)^(1/n) 기하평균 — 한 테마라도 바닥이면 종합도 바닥 (AND 의미).",
        "source_files": ["cascade_v23_ranked.csv", "oxidation_stability_cascade.csv",
                         "cascade_v23_litransport.csv", "zhu2020_si_hydrolysis_energies.csv"],
        "curation_disclaimer": ("cost_tier(가격 등급)·gap_lit_eV(문헌 전형 갭)·air_hsab/air_protect_tier(정성 보호 등급 — "
                                "⚠ 이름과 달리 HSAB 로는 절반만 설명된다. [Zhu20] SI 대조 결과 35종 중 9종이 "
                                "어긋나며 전부 과소평가 방향(In³⁺·Sn⁴⁺·Ba²⁺·Na⁺·Ge⁴⁺·Ga³⁺·Sr²⁺·Ca²⁺). "
                                "낮은 등급을 '공기 불안정'으로 읽지 말 것 — open_items #13)는 "
                                "큐레이션 값 — 우리 계산/절대시세 아님. litdb 앵커: zhu2020, taklu2021, li2025."),
        "literature_disclaimer": {
            "_": "★ `dG_hyd_*_lit*` 열은 **문헌 소환값**이다 — 우리 계산이 아니다. "
                 "우리 db 절대값(electronic.json·bvse·MD σ 등)과 같은 표·같은 축에 놓지 말 것.",
            "source": "Zhu & Mo, Angew. Chem. Int. Ed. 2020, 59, 17472 — SI xlsx 전수 전사 "
                      "(db/properties/zhu2020_si_hydrolysis_energies.csv)",
            "level": "고체 대부분 = Materials Project GGA-PBE 형성에너지 소환 (엔트로피/PV 무시); "
                     "기체 H2O/H2S/HCl + 수산화물 19종 = NIST-JANAF 실험값. → DFT+실험 혼합 스킴, "
                     "절대값은 ~0.1 eV 급 스킴 의존성 예상.",
            "conditions": "T = 300 K, x(H2O) = 0.1 % (RH ~3 %), x(H2S) = x(HCl) = 1 ppm. "
                          "반응은 H2O 1몰 기준 정규화 후 최저 ΔG 경로 (tracer-H2O 극한).",
            "matching": "(양이온 원소, 산화수) 키. 산화수를 무시하면 Sb³⁺(+0.535)/Sb⁵⁺(−0.167) 가 "
                        "0.70 eV 뒤집히는데 같은 값을 받는다.",
            "coverage": "dG_hyd_MS_lit 35/47 · dG_hyd_MCl_* 41/47. 나머지는 null = **판정 없음**이며, "
                        "조합 랭킹에서 0 으로 깔지 말 것(= '가장 나쁨' 으로 읽힌다).",
            "chloride_convention_warning": "⚠ 논문의 chloride 시트는 SI 본문 식과 어긋난다 — HCl 1 ppm "
                                           "보정(0.357 eV/HCl)이 빠진 것으로 보인다. 그래서 원본값"
                                           "(`dG_hyd_MCl_lit_pub`)과 우리 환산값(`dG_hyd_MCl_preset_ours`)을 "
                                           "둘 다 낸다. **후자는 우리 추론이지 논문 값이 아니다.** "
                                           "두 열을 같은 표에 섞지 말고, 인용 시 어느 열인지 밝힐 것. "
                                           "근거·교차검증 3건은 CSV 머리말 참조.",
            "proxy_caveat": "도펀트는 산화물/불화물인데 대조 대상은 **이성분 황화물**이다. "
                            "'이 양이온이 PS₄ 골격을 지킬까'의 프록시이지 코팅 자체의 대기안정성이 아니다.",
        },
        "themes": T,
        "dopants": rows,
    }
    p = PROP / "cascade_v23_themes.json"
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    open(p, "a").write("\n")
    print(f"[themes] {p} — 도펀트 {len(rows)} × 테마 {len(T)}")
    for k, t in T.items():
        print(f"  {t['icon']} {t['label']}: {', '.join(t['top'][:5])}")

    # ── 공기축 대조 CSV (Origin-ready) — 정성 등급 vs [Zhu20] 문헌 ΔG_hyd ────────
    # open_items #13 의 검산을 **재생성 가능한 산출물**로 고정한다. 손으로 센 숫자를
    # 문서에만 적어 두면 다음 사람이 검증할 수 없다.
    LI2S_BASELINE = 0.225      # 기준선: Li2S 가수분해 ΔG (같은 표, 같은 조건)
    cpath = PROP / "cascade_air_axis_lit_vs_tier.csv"
    with open(cpath, "w", newline="") as fh:
        fh.write("# cascade 47 도펀트의 공기/수분 축 — 우리 정성 등급 vs [Zhu20] 문헌 ΔG_hyd 대조.\n")
        fh.write("# !! dG_hyd_* 열은 문헌 소환값이다 (Angew. Chem. 2020, 59, 17472 SI 전수 전사). 우리 계산 아님.\n")
        fh.write("#    조건 T=300K, x(H2O)=0.1%, x(H2S)=x(HCl)=1ppm. 계산수준·규약은\n")
        fh.write("#    db/properties/zhu2020_si_hydrolysis_energies.csv 머리말 참조.\n")
        fh.write(f"# 기준선: Li2S = +{LI2S_BASELINE} eV/H2O (같은 표). 양수=수분 안정, 음수=자발 가수분해.\n")
        fh.write("# hsab_grade_raw: 순수 HSAB 등급 (0.2 hard / 0.6 borderline / 1.0 soft) — **판정은 이 열로 한다**.\n")
        fh.write("#    검증 대상이 'HSAB 로 공기안정을 가릴 수 있나' 라서 F 보너스를 넣으면 축이 흐려진다.\n")
        fh.write("# air_protect_tier: 실제 사용 등급 = hsab_grade_raw + 0.25 (F 함유 시), 상한 1.0.\n")
        fh.write("#    ⚠ 낮은 등급 = '판정 없음' 이지 '공기 불안정' 이 아니다 — kb/open_items.md #13.\n")
        fh.write("# mismatch: hsab_grade_raw 가 0.2(비보호)인데 문헌 ΔG_hyd 가 Li2S 기준선을 **넘으면** UNDERRATED.\n")
        fh.write("#    (Li2O 는 대조 대상이 Li2S = 기준선 자기 자신이라 정의상 제외된다.)\n")
        fh.write("# chloride 열은 as_published(pub)과 우리 환산값(preset_ours)이 다르다 — 섞어 쓰지 말 것.\n")
        w = csv.writer(fh)
        w.writerow(["dopant", "group", "cation", "oxidation_state",
                    "hsab_grade_raw", "air_protect_tier",
                    "dG_hyd_MS_lit_eV_per_H2O", "MS_reference_compound",
                    "dG_hyd_MCl_lit_pub_eV_per_H2O", "dG_hyd_MCl_preset_ours_eV_per_H2O",
                    "MCl_reference_compound", "mismatch_vs_hsab"])
        n_under = n_ok = n_nodata = 0
        for r in rows:
            _c, _ox = cation_oxidation_state(r["dopant"])
            v = r["dG_hyd_MS_lit"]
            if v is None:
                verdict, n_nodata = "NO_LIT_DATA", n_nodata + 1
            elif r["hsab_grade_raw"] <= 0.2 and v > LI2S_BASELINE:
                verdict, n_under = "UNDERRATED_by_hsab", n_under + 1
            else:
                verdict, n_ok = "consistent", n_ok + 1
            w.writerow([r["dopant"], r["group"], _c, _ox,
                        r["hsab_grade_raw"], r["air_protect_tier"],
                        v, r["dG_hyd_MS_ref"],
                        r["dG_hyd_MCl_lit_pub"], r["dG_hyd_MCl_preset_ours"],
                        r["dG_hyd_MCl_ref"], verdict])
    print(f"[air-axis] {cpath} — 일치 {n_ok} · 과소평가 {n_under} · 문헌 없음 {n_nodata}")


if __name__ == "__main__":
    main()
