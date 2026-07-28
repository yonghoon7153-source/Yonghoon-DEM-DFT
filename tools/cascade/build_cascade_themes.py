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


def main():
    ranked = read_csv_rows(PROP / "cascade_v23_ranked.csv")
    oxid = {r["dopant"]: r for r in read_csv_rows(PROP / "oxidation_stability_cascade.csv")}
    lit = {}
    for r in read_csv_rows(PROP / "cascade_v23_litransport.csv"):
        d, _, x = r["_dir"].rpartition("_x")
        lit.setdefault(d, {})[x] = r

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
            "air_hsab": round(air, 2),
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
        "air_stability": ("air_hsab", +1, None),
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
        "air_stability": {"label": "공기/수분 내성", "icon": "🌫️",
            "question": "H₂S 발생·가수분해를 억제할 도펀트는?",
            "metric": "HSAB soft-S 친화 등급 + F 보너스 ↑ — 큐레이션",
            "caveat": "soft acid(Cu·Ag)가 S 보호(taklu2021·li2025) but 전자절연과 정면 상충 — co-doping 동기. zhu2020 설계원칙 앵커."},
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
                         "cascade_v23_litransport.csv"],
        "curation_disclaimer": ("cost_tier(가격 등급)·gap_lit_eV(문헌 전형 갭)·air_hsab(HSAB 등급)는 "
                                "큐레이션 값 — 우리 계산/절대시세 아님. litdb 앵커: zhu2020, taklu2021, li2025."),
        "themes": T,
        "dopants": rows,
    }
    p = PROP / "cascade_v23_themes.json"
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    open(p, "a").write("\n")
    print(f"[themes] {p} — 도펀트 {len(rows)} × 테마 {len(T)}")
    for k, t in T.items():
        print(f"  {t['icon']} {t['label']}: {', '.join(t['top'][:5])}")


if __name__ == "__main__":
    main()
