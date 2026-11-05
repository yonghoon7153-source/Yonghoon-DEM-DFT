#!/usr/bin/env python3
"""analyze_cathode_reactivity.py — M6 결과 판정 + Li 흡수 축 추출.

cathode_reactivity.py 가 만든 94쌍 CSV 를 읽어 세 가지를 낸다.

1) **게이트 변별력 판정** — Xiao F4(|dE|<100 meV)가 우리 풀에서 vacuous 인지.
   cascade_screening_funnel.json 의 vacuous 판정 규약(unique_kill 기준)을 따른다.

2) **만충/반충 비대칭** — host LPSCl 은 반충이 더 발열(-323 -> -455, S 산화가 구동)인데
   산화물/불화물 코팅은 **반대**인 경우가 많다(Al2O3 -19.4 -> 0.0). 구동 화학이 다르다:
   host = S 산화, 코팅 = **Li 흡수(scavenging)**.

3) **Li 흡수 축** ★ — Xiao 게이트가 못 보는 위험.
   `Al2O3 -> LiAl5O8`, `WO3 -> Li2WO4`, `Nb2O5 -> LiNbO3`, `MgF2 -> LiF` 는 전부
   |dE| < 100 meV 로 **통과하지만 양극에서 Li 를 빼앗는다**. Al2O3 코팅의 Li inventory
   소모는 실험적으로 알려진 현상인데 dE_rxt 는 이를 "양성"으로 분류한다.
   → 반응식 좌변의 Li 함유 양극과 우변의 Li 함유 생성물을 비교해 **Li 이동 방향**을 센다.

   ⚠ 이 지표는 **화학량론 부호(sign)** 지 반응 속도가 아니다. "이 코팅은 열역학적으로
   Li 를 가져갈 수 있다"까지만 말하고, 얼마나·얼마나 빨리는 말하지 않는다.

실행:  python3 tools/cascade/analyze_cathode_reactivity.py

4) ⭐ **축 ① NCM 계면 분해 판독** (2026-11-04 · 카드 cascade_axis_ncm_interface_estimand_2026_11_04.json) —
   `--axis_ncm <run_dir>` 로 gabia 출력 (run_axis_ncm_gabia.sh) 을 읽어 게이트 G1–G6 · 호스트 대비 δ (R1) · 도펀트 행방 등급 (R2) ·
   양극 의존 (R4) · 산소/황 짝 (R5) 을 낸다. `--selftest` 는 이 판독기의 양성 · 음성 경로를 본다.
"""
import csv
import datetime
import hashlib
import json
import math
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"
SRC = PROP / "cathode_reactivity_cascade.csv"
OUT = PROP / "cathode_reactivity_verdict.json"

GATE_MEV = 100.0
HOST_ANCHOR = {"full": -322.7, "half": -454.9}      # 우리 계산 LPSCl vs LCO
XIAO_ANCHOR = {"full": -339, "half": -493}          # 문헌 소환값 (혼합 금지)


def rows():
    if not SRC.exists():
        sys.exit(f"{SRC} 없음 — gabia 에서 회수 후 실행")
    with open(SRC) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── Li 흡수 판정 ────────────────────────────────────────────────────────────
# 반응식 예: "0.3333 LiCoO2 + 0.6667 Al2O3 -> 0.2222 LiAl5O8 + 0.1111 Li(CoO2)2 + 0.1111 Al2CoO4"
TERM = re.compile(r"([\d.]+)?\s*([A-Z][A-Za-z0-9()]*)")


def li_count(formula):
    """화학식 문자열에서 Li 원자 수. 괄호 그룹 지원 — Li(CoO2)2 는 Li 1개."""
    n, i = 0, 0
    while i < len(formula):
        if formula[i] == "L" and formula[i:i + 2] == "Li" and \
                (i + 2 >= len(formula) or not formula[i + 2].islower()):
            j = i + 2
            num = ""
            while j < len(formula) and (formula[j].isdigit() or formula[j] == "."):
                num += formula[j]
                j += 1
            n += float(num) if num else 1.0
            i = j
        else:
            i += 1
    return n


def parse_side(side):
    """'0.33 LiCoO2 + 0.67 Al2O3' → [(coef, formula), ...]"""
    out = []
    for term in side.split("+"):
        term = term.strip()
        if not term:
            continue
        m = re.match(r"^([\d.]+)\s+(.+)$", term)
        if m:
            out.append((float(m.group(1)), m.group(2).strip()))
        else:
            out.append((1.0, term))
    return out


def li_transfer(reaction, cathode_comp):
    """양극이 잃는 Li 대비 **코팅 쪽 생성물이 가져가는 Li** 를 센다.

    반환 dict 또는 None(반응 없음/파싱 실패).
      lhs_cathode_li : 좌변 양극이 들고 온 Li
      rhs_cathodic_li: 우변 생성물 중 **Co 를 포함한** 상의 Li (양극에 남은 Li)
      scavenged_li   : lhs_cathode_li - rhs_cathodic_li  (>0 이면 코팅이 가져감)
    """
    if "->" not in reaction:
        return None
    lhs, rhs = reaction.split("->", 1)
    lhs_terms, rhs_terms = parse_side(lhs), parse_side(rhs)
    # 항등 반응 (X -> X) 은 반응 없음
    if len(lhs_terms) == 1 and len(rhs_terms) == 1 and \
            lhs_terms[0][1] == rhs_terms[0][1]:
        return None

    cath_metal = "Co"          # 현재 양극이 LiCoO2 / Li0.5CoO2 계열
    lhs_cath_li = sum(c * li_count(f) for c, f in lhs_terms if cath_metal in f)
    rhs_cath_li = sum(c * li_count(f) for c, f in rhs_terms if cath_metal in f)
    scav = lhs_cath_li - rhs_cath_li
    return {"lhs_cathode_li": round(lhs_cath_li, 4),
            "rhs_cathodic_li": round(rhs_cath_li, 4),
            "scavenged_li": round(scav, 4),
            "li_bearing_products_without_Co":
                sorted({f for c, f in rhs_terms
                        if li_count(f) > 0 and cath_metal not in f})}


def main():
    R = rows()
    by = {}
    for r in R:
        by[(r["coating"], r["lithiation"])] = r
    coatings = sorted({r["coating"] for r in R})

    # ── 1. 게이트 변별력 ────────────────────────────────────────────────
    passed = [r for r in R if r["gate_pass_100meV"] == "Y"]
    failed = [r for r in R if r["gate_pass_100meV"] == "N"]
    fail_coatings = sorted({r["coating"] for r in failed})
    # 코팅 단위: 어느 한 상태라도 탈락하면 그 코팅은 탈락
    coat_fail = {c for c in coatings
                 if any(by.get((c, s), {}).get("gate_pass_100meV") == "N"
                        for s in ("full", "half"))}

    # vacuous 판정은 **우리 깔때기 규약(unique_kill)** 을 따른다 — 임의 비율 문턱 금지.
    # G6 가 죽이는 코팅 중 기존 G1–G4 를 통과해 살아 있던 것이 하나도 없으면 완전 중복.
    fp = PROP / "cascade_screening_funnel.json"
    core_survivors, unique_kill, funnel_ok = [], None, fp.exists()
    if funnel_ok:
        core_survivors = json.loads(fp.read_text()).get("survivors_before_G5", [])
        unique_kill = sorted(coat_fail & set(core_survivors))
        vacuous = len(unique_kill) == 0
    else:
        vacuous = None      # 판정 불가 — 추측하지 않는다

    # ── 2. 만충/반충 비대칭 ─────────────────────────────────────────────
    asym = []
    for c in coatings:
        f, h = by.get((c, "full")), by.get((c, "half"))
        if not (f and h):
            continue
        fv, hv = fnum(f["dE_rxt_meV_per_atom"]), fnum(h["dE_rxt_meV_per_atom"])
        if fv is None or hv is None:
            continue
        asym.append({"coating": c, "full": fv, "half": hv,
                     "half_minus_full": round(hv - fv, 1),
                     "direction": ("half_worse" if hv < fv - 1e-9
                                   else "full_worse" if fv < hv - 1e-9 else "tie")})
    host_dir = "half_worse"   # -322.7 -> -454.9
    like_host = [a for a in asym if a["direction"] == host_dir]
    unlike_host = [a for a in asym if a["direction"] == "full_worse"]

    # ── 3. Li 흡수 축 ──────────────────────────────────────────────────
    scav_rows = []
    for r in R:
        lt = li_transfer(r["reaction"], r["cathode_composition"])
        if not lt or lt["scavenged_li"] <= 1e-6:
            continue
        mev = fnum(r["dE_rxt_meV_per_atom"])
        scav_rows.append({
            "coating": r["coating"], "lithiation": r["lithiation"],
            "dE_rxt_meV": mev, "gate_pass": r["gate_pass_100meV"],
            **lt, "reaction": r["reaction"][:160]})
    scav_rows.sort(key=lambda x: -x["scavenged_li"])
    # 게이트는 통과하는데 Li 를 가져가는 것 = 게이트가 못 보는 위험
    blind_spot = [s for s in scav_rows if s["gate_pass"] == "Y"]

    verdict = {
        "property": "cathode_reactivity_verdict",
        "date": "2026-07-28",
        "source_csv": "db/properties/cathode_reactivity_cascade.csv",
        "method": ("닫힌계 pseudo-binary dE_rxt (Richards/Ong 2016 eq 2, "
                   "InterfacialReactivity, norm=True, use_hull_energy=True, MP GGA_GGA+U). "
                   "축은 양극 리튬화 상태(full=LiCoO2 / half=Li0.5CoO2) — Xiao 2019 F4 와 동일 정의."),

        "honesty_header": [
            "⛔ **게이트 통과 수를 성과로 인용하지 말 것.** 아래 gate_discrimination 이 vacuous 판정이면 "
            "'N종이 계면 반응성 게이트를 통과했다'는 서술 자체가 정보가 없다.",
            "⛔ 컷 근처 ±20 meV 순위 주장 금지 — Xiao 100 meV 는 관례컷이고, Sundar 2025 의 "
            "'분해산물 전자전도도 미고려' 비판을 그대로 받는다.",
            "⛔ Xiao 소환값(-339/-493)은 문헌값이다. 우리 값(-322.7/-454.9)과 같은 표에 넣되 "
            "**출처를 반드시 병기**하고 평균/혼합 금지.",
            "⚠ li_scavenging 은 **화학량론 부호**지 속도가 아니다. '열역학적으로 Li 를 가져갈 수 있다'"
            "까지만 말하고 얼마나·얼마나 빨리는 말하지 않는다.",
        ],

        "anchors": {"ours_LPSCl_vs_LCO": HOST_ANCHOR,
                    "xiao2019_summoned": XIAO_ANCHOR,
                    "agreement_ratio": {k: round(abs(HOST_ANCHOR[k]) / abs(XIAO_ANCHOR[k]), 3)
                                        for k in HOST_ANCHOR},
                    "note": "0.92-0.95배 = MP hull 세대 차 감안 시 사실상 논문 재현"},

        "gate_discrimination": {
            "n_pairs": len(R), "n_pass": len(passed), "n_fail": len(failed),
            "n_coatings": len(coatings),
            "n_coatings_failing_any_state": len(coat_fail),
            "failing_coatings": sorted(coat_fail),
            "failing_rows": [{"coating": r["coating"], "lithiation": r["lithiation"],
                              "dE_rxt_meV": fnum(r["dE_rxt_meV_per_atom"])} for r in failed],
            "vacuous": vacuous,
            "vacuous_criterion": ("cascade_screening_funnel.json 의 unique_kill 규약 — "
                                  "G6 가 죽이는 코팅 중 G1–G4 를 통과해 살아 있던 것이 "
                                  "하나도 없으면 완전 중복(G2 와 동종). 임의 비율 문턱 쓰지 않음."),
            "core_survivors_G1_G4": core_survivors,
            "unique_kill_vs_core": unique_kill,
            "verdict": (
                f"{len(passed)}/{len(R)} 쌍 통과, 코팅 단위로는 {len(coatings) - len(coat_fail)}"
                f"/{len(coatings)}종 통과. " +
                ("판정 불가 — cascade_screening_funnel.json 이 없다." if vacuous is None else
                 (f"탈락 {len(coat_fail)}종({', '.join(sorted(coat_fail))})이 **전부 이미 "
                  f"G1–G4 에서 죽어 있다** → unique_kill = 0, **완전 중복 게이트**(G2 와 동종). "
                  "물리는 맞다 — 황화물 SE↔산화물 양극은 큰 구동력, 산화물 코팅↔산화물 양극은 "
                  "거의 0이고, 그게 코팅을 쓰는 이유 자체다. 하지만 우리 47종 안에서는 "
                  "**새로 거르는 것이 없다**. 깔때기에 넣되 vacuous 배지 필수, "
                  "'N종이 계면 반응성을 통과했다'는 서술 금지."
                  if vacuous else
                  f"**unique_kill = {len(unique_kill)}종({', '.join(unique_kill)})** — "
                  f"G1–G4 를 통과한 코어 생존자를 새로 거른다. 유의미한 게이트."))),
        },

        "s1_condition_2": {
            "question": "host LPSCl 보다 계면 반응성이 완화되는 코팅이 있는가",
            "answer": "YES — 전 코팅이 host 보다 완화됨",
            "detail": (f"host {HOST_ANCHOR['full']} meV/atom(만충) 대비 코팅들은 "
                       "-107 ~ 0 구간. 47/47."),
            "caveat": ("⚠ 이 '성공'은 **자명하다**. 비교가 '황화물 vs 산화물 양극' 대 "
                       "'산화물 vs 산화물 양극'이라 화학이 다르다. "
                       "코팅 개념 자체의 타당성을 재현한 것이지 후보 간 변별이 아니다.")
        },

        "lithiation_asymmetry": {
            "host_direction": host_dir,
            "host_values": HOST_ANCHOR,
            "n_like_host_half_worse": len(like_host),
            "n_unlike_host_full_worse": len(unlike_host),
            "unlike_host_examples": sorted(unlike_host, key=lambda a: a["half_minus_full"],
                                           reverse=True)[:12],
            "interpretation": (
                "**구동 화학이 다르다.** host LPSCl 은 탈리튬된 양극이 더 산화적이라 반충에서 나빠진다"
                "(S 산화가 구동). 산화물/불화물 코팅은 반대로 **Li 가 있을 때** 나빠지는 경우가 많다 — "
                "구동력이 **Li 흡수**(Li 함유 삼원상 형성)이기 때문. "
                "→ 두 계를 같은 '반응성' 언어로 묶어 서술하면 기구를 뭉갠다."),
            "all": sorted(asym, key=lambda a: a["full"])
        },

        "li_scavenging": {
            "what": ("반응식 좌변 양극(Co 함유)이 들고 온 Li 와 우변 Co 함유 상에 남은 Li 를 비교. "
                     "차이가 양수면 코팅 쪽 생성물이 Li 를 가져간 것."),
            "why_it_matters": (
                "**Xiao 게이트의 사각지대다.** Al2O3 -> LiAl5O8, WO3 -> Li2WO4, Nb2O5 -> LiNbO3, "
                "MgF2 -> LiF 는 전부 |dE| < 100 meV 로 통과하지만 양극에서 Li 를 빼앗는다. "
                "Al2O3 코팅의 Li inventory 소모는 실험적으로 알려진 현상인데 dE_rxt 는 이를 "
                "'양성'으로 분류한다. 게이트 통과 = 안전이 아니다."),
            "n_rows_with_scavenging": len(scav_rows),
            "n_gate_blind_spot": len(blind_spot),
            "blind_spot_top": blind_spot[:20],
            "all": scav_rows
        },

        "next": [
            "cascade 깔때기에 G6 로 편입 — 단 vacuous 배지 + 'Li 흡수 축은 별개'라는 각주 필수",
            "Li 흡수를 별도 진단축으로 등록(게이트 아님 — 화학량론 부호일 뿐)",
            "NCM 으로 확장 시 재판정 (Ni 계는 산화력이 더 커 결과가 달라질 수 있음)",
            "Nano Convergence 2026, 13, 27 (Li3Sc2(PO4)3, 17233종) 입수 후 대조 — 우리 1위 Sc2O3 와 원소 수렴"
        ]
    }

    OUT.write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n")

    g = verdict["gate_discrimination"]
    print("=" * 74)
    print(f"게이트 변별력: {g['n_pass']}/{g['n_pairs']} 쌍 통과 · "
          f"코팅 {g['n_coatings'] - g['n_coatings_failing_any_state']}/{g['n_coatings']}종 통과")
    print(f"  탈락: {', '.join(g['failing_coatings']) or '(없음)'}")
    print("  → " + ("⚠ VACUOUS (unique_kill=0, 완전 중복)" if g["vacuous"] else f"OK — unique_kill {len(g['unique_kill_vs_core'] or [])}종"))
    print(f"  코어(G1-G4) 생존자와 대조: {g['unique_kill_vs_core']}")
    print("-" * 74)
    a = verdict["lithiation_asymmetry"]
    print(f"리튬화 비대칭: host 와 같은 방향(반충이 더 나쁨) {a['n_like_host_half_worse']}종 · "
          f"반대(만충이 더 나쁨) {a['n_unlike_host_full_worse']}종")
    print("-" * 74)
    s = verdict["li_scavenging"]
    print(f"Li 흡수: {s['n_rows_with_scavenging']}행에서 검출 · "
          f"그중 **게이트를 통과하면서** 흡수 {s['n_gate_blind_spot']}행 (사각지대)")
    for b in s["blind_spot_top"][:10]:
        print(f"    {b['coating']:8s} {b['lithiation']:5s} "
              f"dE={b['dE_rxt_meV']:7.1f}  Li 흡수 {b['scavenged_li']:+.3f}  "
              f"→ {', '.join(b['li_bearing_products_without_Co']) or '-'}")
    print("=" * 74)
    print(f"→ {OUT}")


# ══════════════════════════════════════════════════════════════════════════════════════════════════
# 축 ① NCM 계면 분해 판독 — 카드 db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json
#   (결정 D-2026-11-04-cascade-axis-ncm-interface · 결과를 회수하기 **전에** 커밋한다 — 카드 §3b · §8 ③)
#   실행:  python3 tools/cascade/analyze_cathode_reactivity.py --axis_ncm <run_dir> [--out <json>]
#   ⛔ 이 판독기가 못 하는 것:
#     · 계산을 다시 하지 않는다 — gabia 출력 (designs_*.jsonl · host.jsonl · product_gaps.json · manifest.json) 만 읽는다.
#     · MP 갭은 외부 PBE 값 · 순서용 — 값을 고치지 않고 등급만 매긴다. 우리 DFT 띠틈과 섞지 않는다.
#     · 합치는 규칙이 없다 — 순위 · 거르기를 내지 않는다 (카드 §8 ⛔). 표는 종 이름 순이다.
#     · 반응식이 pymatgen 꼴 ('계수 화학식 + …') 이 아니거나 원자 수가 양변에서 안 맞으면 그 설계를 '판독 오류' 로 센다
#       (조용히 버리지 않는다).
#     · 도핑 격자의 초과 에너지는 원래 계산에 없다 (MP 평형 상 혼합) — 이 판독기도 보정하지 않는다 (카드 1c).
# ══════════════════════════════════════════════════════════════════════════════════════════════════
AXIS_CARD = PROP / "cascade_axis_ncm_interface_estimand_2026_11_04.json"
AXIS_DECISION = "D-2026-11-04-cascade-axis-ncm-interface"
AX_ROSTER_SRC = PROP / "cascade_interface_90.jsonl"   # 카드 개정 1 — 대상 91 종의 조성 = 1 단계 계면 표 그대로 (러너와 같은 출처)
AX_PHYS_TOOLS = ("tools/oxidation/interface_reactivity_v2.py", "tools/oxidation/sei_product_gaps.py")
AX = {"wide_eV": 2.0, "metal_eV": 0.1, "frac_metal": 0.01, "frac_wide": 0.90, "frac_und": 0.10,
      "delta_meV": 10.0, "iqr_meV": 10.0, "anchor_lo": 0.5, "anchor_hi": 2.0, "proxy_lo": 0.5, "proxy_hi": 2.0}
#: G5 — 판독기 상수가 카드 본문과 같은지 (카드 문자열에 이 조각이 다 있어야 한다)
AX_CARD_TEXT = ("MP 갭 ≥ 2.0 eV", "0.1 ≤ MP 갭 < 2.0 eV", "MP 갭 < 0.1 eV", "≥ 1 %", "≥ 90 %", "> 10 %",
                "|δ| ≥ 10 meV/atom", "(IQR) 가 10 meV/atom 미만", "0.5–2.0 배", "둘 다 0.5–2.0")
AX_HOST_ELEMS = frozenset({"Li", "P", "S", "Cl", "O"})
AX_TM_U = frozenset({"Co", "Cr", "Fe", "Mn", "Mo", "Ni", "V", "W", "Cu"})
#: ⭐ 사후 민감도 전용 스위치 (2026-11-05 · --sens_plusU_gap) — True 면 +U · Cu 분기를 건너뛰고 **같은 봉인 문턱** (AX wide_eV · metal_eV)
#: 으로 MP 갭 등급을 매긴다. 봉인 판독 (--axis_ncm · --axis_li · --axis_hyd) 은 늘 False 로 돈다 (sens_plusU 가 끝에 되돌린다).
AX_SENS = {"plusU_by_gap": False}
AX_4F = frozenset({"Nd", "Sm", "Gd"})
AX_NONMETAL = frozenset({"H", "B", "C", "N", "O", "F", "Si", "P", "S", "Cl", "Ge", "As", "Se", "Br", "Sb", "Te", "I"})
AX_CATH_TM = {"LNO": "Ni", "LCO": "Co", "NCM": None}
AX_XIAO = {"LCO_full": -339.0, "LCO_half": -493.0}     # 문헌 소환값 — G1b 비율 검사에만 (값을 섞지 않는다)
AX_M6 = {"LCO_full": -322.7, "LCO_half": -454.9}       # 8 월 M6 우리 값 — 차이만 기록 (판정에 안 쓴다)
AX_PAIRS = (("Al2O3", "Al2S3"), ("CaO", "CaS"), ("Ga2O3", "Ga2S3"), ("GeO2", "GeS2"), ("Li2O", "Li2S"),
            ("MgO", "MgS"), ("Na2O", "Na2S"), ("Sb2O5", "Sb2S3"), ("SiO2", "SiS2"), ("SnO2", "SnS2"))
AX_MANIFEST_KEYS = ("mp_db_version_before", "mp_db_version_after", "pymatgen", "mp_api", "thermo_types",
                    "correction_names_sample_Li-Ni-O", "tools_sha16", "repo_head", "lanes")
AX_LETTER = {"wide": "ⓐ", "metallic": "ⓑ", "intermediate": "ⓒ", "undetermined": "ⓓ", "no_reaction": "ⓔ", "na": "㉧",
             "fate_error": "⚠", "unconfirmed": "?"}


def _ax_pf(f):
    """화학식 → {원소: 수} — interface_reactivity_v2.parse_formula (괄호를 편다) 를 그대로 쓴다."""
    od = str(ROOT / "tools" / "oxidation")
    if od not in sys.path:
        sys.path.insert(0, od)
    from interface_reactivity_v2 import parse_formula
    return {k: float(v) for k, v in parse_formula(str(f)).items() if v}


def ax_tracked(formula, cathode_label):
    """추적 원소 — 도핑 조성에는 있고 Li · P · S · Cl · O 에는 없는 원소 · 그 양극의 전이금속은 뺀다 (카드 §2)."""
    tm = AX_CATH_TM.get(str(cathode_label).split("_")[0])
    return sorted(set(_ax_pf(formula)) - AX_HOST_ELEMS - ({tm} if tm else set()))


def ax_fate(rxn, tracked):
    """추적 원소마다 우변 산물로 가는 몫 — ({원소: [(산물, 몫)]}, None) · 문제면 (None, 이유)."""
    if not isinstance(rxn, str) or "->" not in rxn:
        return None, "반응식이 없다"
    lhs, rhs = rxn.split("->", 1)
    try:
        L, R = parse_side(lhs), parse_side(rhs)
        out = {}
        for E in tracked:
            nl = sum(c * _ax_pf(f).get(E, 0.0) for c, f in L)
            parts = [(f, c * _ax_pf(f).get(E, 0.0)) for c, f in R]
            parts = [(f, x) for f, x in parts if x > 0]
            nr = sum(x for _, x in parts)
            if nl <= 0 or nr <= 0 or abs(nr - nl) > 0.01 * nl:
                return None, f"{E} 원자 수가 양변에서 안 맞는다 (좌 {nl:.4g} · 우 {nr:.4g})"
            out[E] = [(f, x / nr) for f, x in sorted(parts, key=lambda t: -t[1])]
        return out, None
    except (ValueError, TypeError) as e:
        return None, f"반응식을 못 읽는다 ({type(e).__name__})"


def ax_product_class(f, gaps):
    """산물 MP 갭 등급 (카드 §2 R2_산물_등급) — (등급, 근거). 등급 = wide · narrow · metallic · undetermined."""
    el = _ax_pf(f)
    if not el:
        return "undetermined", "화학식을 못 읽는다"
    if len(el) == 1 and next(iter(el)) not in AX_NONMETAL:
        return "metallic", "원소 금속"
    if set(el) & AX_TM_U and not AX_SENS["plusU_by_gap"]:
        return "undetermined", "+U 전이금속 · Cu 포함 (자성 · +U 의존 · 금속 선언 아님)"
    g = gaps.get(f) if isinstance(gaps, dict) else None
    gap = g.get("band_gap_MP_eV") if isinstance(g, dict) else None
    if isinstance(gap, bool) or not isinstance(gap, (int, float)) or not math.isfinite(gap):
        return "undetermined", "MP 갭 없음"
    if set(el) & AX_4F:
        return ("wide", f"4f 하한 {gap:g} ≥ {AX['wide_eV']}") if gap >= AX["wide_eV"] else ("undetermined", f"4f 하한 {gap:g} < {AX['wide_eV']}")
    if gap < AX["metal_eV"]:
        return "metallic", f"MP 갭 {gap:g} < {AX['metal_eV']}"
    if gap < AX["wide_eV"]:
        return "narrow", f"MP 갭 {gap:g}"
    return "wide", f"MP 갭 {gap:g}"


def ax_design_class(row, tracked, gaps, classify=None):
    """한 행 (설계 × 양극 상태) → (등급, 세부). 우선순위 ⓑ 금속성 > ⓐ 넓은 갭 > ⓓ 미판정 > ⓒ 중간 · ⓔ 끝점 · ㉧ 추적 원소 없음.
    classify = 산물 등급 함수 (기본 ax_product_class · 축 ③ 은 li_product_class — 음이온 없는 금속간 = 금속성)."""
    if not tracked:
        return "na", {}
    ep = row.get("min_kink_at_endpoint")
    if ep is True:
        return "no_reaction", {"endpoint_basis": row.get("endpoint_basis")}
    fate, why = ax_fate(row.get("reaction"), tracked)
    if fate is None:
        return "fate_error", {"why": why}
    det, raw = {}, []
    for E, parts in fate.items():
        sh = {"wide": 0.0, "narrow": 0.0, "metallic": 0.0, "undetermined": 0.0}
        prods = []
        for f, x in parts:
            c, w = (classify or ax_product_class)(f, gaps)
            sh[c] += x
            prods.append({"product": f, "share": round(x, 4), "class": c, "basis": w})
        raw.append(sh)
        det[E] = {"shares": {k: round(v, 4) for k, v in sh.items()}, "products": prods}
    if any(s["metallic"] >= AX["frac_metal"] for s in raw):
        cls = "metallic"
    elif all(s["wide"] >= AX["frac_wide"] for s in raw):
        cls = "wide"
    elif any(s["undetermined"] > AX["frac_und"] for s in raw):
        cls = "undetermined"
    else:
        cls = "intermediate"
    if ep is None:
        det["⚠_endpoint_unseen"] = "끝점 판정이 기록에 없다 (None = 못 봤다)"
    return cls, det


def ax_load(run_dir):
    """gabia 출력 폴더 → 행 · 갭 · manifest. 못 읽은 줄은 problems 에 남긴다 (조용히 버리지 않는다)."""
    d, out = Path(run_dir), {"problems": []}
    for k in ("designs_lno", "designs_lco", "host"):
        p = d / f"{k}.jsonl"
        if not p.is_file():
            out[k] = None
            continue
        rows = []
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
                if not isinstance(r, dict):
                    raise ValueError("행이 객체가 아니다")
                rows.append(r)
            except ValueError as e:
                out["problems"].append(f"{k}.jsonl {i} 번째 줄을 못 읽는다 ({type(e).__name__})")
        out[k] = rows
    for k, nm in (("gaps", "product_gaps.json"), ("manifest", "manifest.json")):
        p = d / nm
        try:
            out[k] = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None
        except ValueError as e:
            out[k] = None
            out["problems"].append(f"{nm} 를 못 읽는다 ({type(e).__name__})")
    return out


def ax_index(rows):
    ix = {}
    for r in rows or []:
        ix.setdefault((r.get("species"), r.get("cathode")), []).append(r)
    return ix


def _ax_ok(r):
    """정상 닫힌계 행인가 — 오류 · 건너뜀 없음 · 유한한 dE · 반응식 · mode closed_0V."""
    v = r.get("dE_eV_per_atom") if isinstance(r, dict) else None
    return (isinstance(r, dict) and "error" not in r and "skipped" not in r and isinstance(v, (int, float))
            and not isinstance(v, bool) and math.isfinite(v) and isinstance(r.get("reaction"), str) and r.get("mode") == "closed_0V")


def _ax_one(ix, key):
    rs = ix.get(key) or []
    return rs[0] if len(rs) == 1 and _ax_ok(rs[0]) else None


def ax_roster(src=None):
    """카드 §1b 대상 91 — **1 단계 계면 표 (cascade_interface_90.jsonl) 의 조성 그대로** · {종: 조성} (카드 개정 1 · 러너와 같은 출처).
    ⛔ champion_formulas 를 지금 CSV 에 다시 돌리지 않는다 — 9 종이 다른 조성 (세 라벨 중 '먼저 나온 행' 이 바뀜) · As2S3 없음 (2026-11-04 실측)."""
    f = {}
    for ln in Path(src or AX_ROSTER_SRC).read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if r.get("cathode") in ("LCO", "LNO", "LMO") and r.get("formula"):
            if f.setdefault(r["species"], r["formula"]) != r["formula"]:
                raise ValueError(f"{r['species']}: 양극마다 조성이 다르다")
    return f


def _ax_decision():
    """(decision_state, card) — 결정 원장에서."""
    d = json.loads((ROOT / "db" / "governance" / "decisions.json").read_text(encoding="utf-8"))
    x = [y for y in d["decisions"] if y.get("id") == AXIS_DECISION]
    return (x[0].get("decision_state"), x[0].get("card")) if x else (None, None)


def ax_gates(L, expected, card_text, decision_state, decision_card):
    """G1 · G1b · G2 · G3 · G5 · G6 + 결정 (카드 §4). G4 는 δ 를 낸 뒤 ax_readout 이 잰다."""
    G = {"decision": {"ok": decision_state == "active" and decision_card == "db/properties/" + AXIS_CARD.name,
                      "state": decision_state, "card": decision_card}}
    man = L.get("manifest") if isinstance(L.get("manifest"), dict) else {}
    miss = [k for k in AX_MANIFEST_KEYS if man.get(k) in (None, "", [], {})]
    ts = man.get("tools_sha16")
    if not (isinstance(ts, dict) and len(ts) >= 3 and all(isinstance(v, str) and v for v in ts.values())):
        miss.append("tools_sha16 (도구 셋)")
    invs = man.get("invocations") if isinstance(man.get("invocations"), list) and man.get("invocations") else [man]
    phys = {t: {(x.get("tools_sha16") or {}).get(t) for x in invs if isinstance(x, dict)} for t in AX_PHYS_TOOLS}
    drift = [t for t, v in phys.items() if len(v) != 1 or None in v]
    if drift:
        miss.append(f"물리 도구 sha 가 실행마다 다르거나 없다 ({drift})")
    G["G1"] = {"ok": not miss and not L["problems"], "missing": miss, "load_problems": L["problems"][:10],
               "n_invocations": len(invs)}
    vb, va = man.get("mp_db_version_before"), man.get("mp_db_version_after")
    G["G3"] = {"ok": man.get("same_mp_version") is True and vb not in (None, "") and vb == va, "before": vb, "after": va}
    ixl, ixh = ax_index(L.get("designs_lno")), ax_index(L.get("host"))
    prob = [f"{nm} 없음" for nm, k in (("designs_lno.jsonl", "designs_lno"), ("host.jsonl", "host")) if L.get(k) is None]
    for sp in expected:
        for st in ("LNO_full", "LNO_half"):
            rs = ixl.get((sp, st)) or []
            if len(rs) != 1 or not _ax_ok(rs[0]):
                prob.append(f"{sp} × {st}: 행 {len(rs)} 개 · 정상 {sum(1 for r in rs if _ax_ok(r))}")
            elif rs[0].get("formula") != expected[sp]:
                prob.append(f"{sp} × {st}: 조성 {rs[0].get('formula')} ≠ 카드 대상 {expected[sp]}")
    extra = sorted({k[0] for k in ixl} - set(expected))
    if extra:
        prob.append(f"카드에 없는 종 {extra[:5]}")
    for st in ("LNO_full", "LNO_half"):
        if _ax_one(ixh, ("HOST", st)) is None:
            prob.append(f"HOST × {st}: 정상 행 하나가 아니다")
    G["G2"] = {"ok": not prob, "n_problems": len(prob), "problems": prob[:20], "n_expected": len(expected)}
    hf, hh = _ax_one(ixh, ("HOST", "LCO_full")), _ax_one(ixh, ("HOST", "LCO_half"))
    g1b = {"ok": False}
    if hf and hh:
        f_, h_ = hf["dE_eV_per_atom"] * 1000.0, hh["dE_eV_per_atom"] * 1000.0
        rf, rh = f_ / AX_XIAO["LCO_full"], h_ / AX_XIAO["LCO_half"]
        g1b = {"ok": bool(f_ < 0 and h_ < 0 and AX["anchor_lo"] <= rf <= AX["anchor_hi"]
                          and AX["anchor_lo"] <= rh <= AX["anchor_hi"] and h_ < f_),
               "host_LCO_meV": {"full": round(f_, 2), "half": round(h_, 2)},
               "ratio_to_Xiao": {"full": round(rf, 3), "half": round(rh, 3)}, "half_more_exothermic": h_ < f_,
               "diff_vs_M6_meV_기록만": {"full": round(f_ - AX_M6["LCO_full"], 2), "half": round(h_ - AX_M6["LCO_half"], 2)}}
    else:
        g1b["why"] = "호스트 × LCO 만충 · 반충 정상 행이 없다"
    G["G1b"] = g1b
    miss5 = [t for t in AX_CARD_TEXT if t not in (card_text or "")]
    G["G5"] = {"ok": not miss5, "missing_in_card": miss5,
               "card_sha256": hashlib.sha256((card_text or "").encode("utf-8")).hexdigest()}
    rat = {}
    for s_ in ("full", "half"):
        n_, l_ = _ax_one(ixh, ("HOST", f"NCM_{s_}")), _ax_one(ixh, ("HOST", f"LNO_{s_}"))
        rat[s_] = (round(n_["dE_eV_per_atom"] / l_["dE_eV_per_atom"], 4)
                   if n_ and l_ and l_["dE_eV_per_atom"] != 0 else None)
    ok6 = all(v is not None and AX["proxy_lo"] <= v <= AX["proxy_hi"] for v in rat.values())
    G["G6"] = {"ok": ok6, "ratio_NCM_over_LNO": rat, "label": "NCM 대리 (LiNiO₂)" if ok6 else "LiNiO₂ 계면"}
    return G


def ax_readout(run_dir, expected=None, card_text=None, decision=None):
    """카드 §2 · §4 대로 판독 — 막는 게이트 (결정 · G1 · G1b · G2 · G3 · G5) 가 하나라도 불통과면 표를 내지 않는다."""
    L = ax_load(run_dir)
    if expected is None:
        expected = ax_roster()
    if card_text is None:
        card_text = AXIS_CARD.read_text(encoding="utf-8")
    if decision is None:
        decision = _ax_decision()
    G = ax_gates(L, expected, card_text, *decision)
    blocking = [k for k in ("decision", "G1", "G1b", "G2", "G3", "G5") if not G[k]["ok"]]
    res = {"card": "db/properties/" + AXIS_CARD.name, "decision": AXIS_DECISION, "run_dir": str(run_dir), "constants": AX,
           "gates": G, "blocking": blocking, "label": G["G6"]["label"],
           "⛔": "상대값 · 등급만 — 순위 · 거르기는 합치는 규칙 비준 뒤 (카드 §8) · MP 갭은 외부 PBE 값 (순서용)"}
    if blocking:
        res["⛔_표_없음"] = f"막는 게이트 불통과 {blocking} — 표를 내지 않는다 (카드 §4)"
        return res
    ixl, ixc, ixh = ax_index(L["designs_lno"]), ax_index(L.get("designs_lco")), ax_index(L["host"])
    host = {st: r["dE_eV_per_atom"] * 1000.0 for st in ("LNO_full", "LNO_half", "LCO_full", "LCO_half")
            for r in [_ax_one(ixh, ("HOST", st))] if r}
    gaps = (L.get("gaps") or {}).get("gaps") or {}
    rows = []
    for sp in sorted(expected):
        r_lf, r_lh = ixl[(sp, "LNO_full")][0], ixl[(sp, "LNO_half")][0]
        formula = r_lh.get("formula")
        trk_l, trk_c = ax_tracked(formula, "LNO"), ax_tracked(formula, "LCO")
        d_lf = r_lf["dE_eV_per_atom"] * 1000.0 - host["LNO_full"]
        d_lh = r_lh["dE_eV_per_atom"] * 1000.0 - host["LNO_half"]
        cls_l, det_l = ax_design_class(r_lh, trk_l, gaps)
        rc = _ax_one(ixc, (sp, "LCO_half"))
        if rc is not None and "LCO_half" in host:
            d_ch = rc["dE_eV_per_atom"] * 1000.0 - host["LCO_half"]
            cls_c, det_c = ax_design_class(rc, trk_c, gaps)
        else:
            d_ch, cls_c, det_c = None, "unconfirmed", {}
        if cls_c == "unconfirmed" or "na" in (cls_l, cls_c):
            r4 = None
        else:
            r4 = bool(cls_c != cls_l or (abs(d_lh) >= AX["delta_meV"] and abs(d_ch) >= AX["delta_meV"] and (d_lh > 0) != (d_ch > 0)))
        rows.append({"species": sp, "formula": formula, "tracked_LNO": trk_l,
                     "delta_LNO_full_meV": round(d_lf, 2), "delta_LNO_half_meV": round(d_lh, 2),
                     "differs_from_host": abs(d_lh) >= AX["delta_meV"],
                     "class_LNO_half": cls_l, "letter_LNO_half": AX_LETTER[cls_l], "fate_LNO_half": det_l,
                     "endpoint_LNO_half": r_lh.get("min_kink_at_endpoint"), "reaction_LNO_half": r_lh.get("reaction"),
                     "delta_LCO_half_meV": None if d_ch is None else round(d_ch, 2), "class_LCO_half": cls_c,
                     "fate_LCO_half": det_c, "R4_cathode_dependent": r4})
    ds = [r["delta_LNO_half_meV"] for r in rows]
    if len(ds) >= 4:
        q1, _, q3 = statistics.quantiles(ds, n=4, method="inclusive")
        g4 = {"q1_meV": round(q1, 2), "q3_meV": round(q3, 2), "iqr_meV": round(q3 - q1, 2), "discriminates": (q3 - q1) >= AX["iqr_meV"]}
    else:
        g4 = {"iqr_meV": None, "discriminates": False, "why": "설계가 4 개 미만"}
    g4.update({"n": len(ds), "method": "statistics.quantiles(n=4, method='inclusive')",
               "use": "R1 을 합치는 규칙에 넣을 수 있다" if g4["discriminates"] else "R1 은 이 축에서 갈리지 않는다 — 합치는 규칙에 넣지 않고 R2 만 남긴다"})
    G["G4"] = g4
    by = {r["species"]: r for r in rows}
    pairs = []
    for o, s_ in AX_PAIRS:
        if o in by and s_ in by:
            dd = by[o]["delta_LNO_half_meV"] - by[s_]["delta_LNO_half_meV"]
            co, cs = by[o]["class_LNO_half"], by[s_]["class_LNO_half"]
            pairs.append({"oxide": o, "sulfide": s_, "delta_O_minus_S_meV": round(dd, 2), "class_O": co, "class_S": cs,
                          "differs": bool(abs(dd) >= AX["delta_meV"] or co != cs)})
        else:
            pairs.append({"oxide": o, "sulfide": s_, "missing": True})
    cnt = {}
    for r in rows:
        cnt[r["class_LNO_half"]] = cnt.get(r["class_LNO_half"], 0) + 1
    res.update({"rows": rows, "pairs_R5": pairs,
                "summary": {"n_designs": len(rows), "class_LNO_half": cnt,
                            "n_differs_from_host": sum(r["differs_from_host"] for r in rows),
                            "n_R4_flag": sum(1 for r in rows if r["R4_cathode_dependent"]),
                            "n_pairs_differ": sum(1 for p_ in pairs if p_.get("differs"))}})
    return res


def ax_write_csv(res, path):
    """Origin 용 CSV — 열 이름을 명시한다 (상대값 · 등급만)."""
    cols = ["species", "formula", "tracked_LNO", "delta_LNO_full_meV", "delta_LNO_half_meV", "differs_from_host",
            "class_LNO_half", "delta_LCO_half_meV", "class_LCO_half", "R4_cathode_dependent"]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("# cascade 축 ① NCM 계면 (카드 " + res["card"] + ") — δ = 설계 − 호스트 [meV/atom · MP 닫힌계 · 상대값만] · "
                 "등급 = 도펀트 행방 MP 갭 등급 · 라벨 " + res["label"] + "\n")
        w = csv.writer(fh)
        w.writerow(cols)
        for r in res["rows"]:
            w.writerow(["/".join(r[c]) if isinstance(r[c], list) else ("" if r[c] is None else r[c]) for c in cols])


def ax_main(argv):
    i = argv.index("--axis_ncm")
    run_dir = argv[i + 1] if i + 1 < len(argv) else None
    if not run_dir:
        print("⛔ --axis_ncm <run_dir>")
        return 2
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else \
        PROP / f"cascade_axis_ncm_readout_{datetime.date.today().strftime('%Y_%m_%d')}.json"
    res = ax_readout(run_dir)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k in ("decision", "G1", "G1b", "G2", "G3", "G5", "G6", "G4"):
        g = res["gates"].get(k)
        if g is not None:
            print(f"  {k:8s} {'⭕' if g.get('ok', g.get('discriminates')) else '⛔'}  "
                  + json.dumps({x: y for x, y in g.items() if x not in ("problems", "load_problems")}, ensure_ascii=False)[:160])
    if res["blocking"]:
        print(f"⛔ 막는 게이트 불통과 {res['blocking']} — 표 없음 → {out}")
        return 2
    ax_write_csv(res, out.with_name(out.stem + "_designs.csv"))
    sm = res["summary"]
    print(f"라벨 {res['label']} · 설계 {sm['n_designs']} · 등급 (LNO 반충) {sm['class_LNO_half']} · "
          f"호스트와 다름 {sm['n_differs_from_host']} · 양극 의존 {sm['n_R4_flag']} · 짝 다름 {sm['n_pairs_differ']}/{len(AX_PAIRS)}")
    print(f"→ {out} · {out.with_name(out.stem + '_designs.csv')}")
    return 0


def ax_selftest():
    """축 ① 판독기 — 양성 하나 + 음성 경로 (막는 게이트마다 · 등급 문턱 경계 · 끝점 · 원자 수 불일치 · 대리 점검 · R4 · R5)."""
    import tempfile
    ok_all, n = True, [0, 0]
    def chk(c, msg):
        nonlocal ok_all
        n[0 if c else 1] += 1
        ok_all &= bool(c)
        print(("  ⭕ " if c else "  ⛔ ") + msg)
    card = AXIS_CARD.read_text(encoding="utf-8")
    EXP = ["Ag2O", "Al2O3", "Al2S3", "CoO", "Cu2O", "GeO2", "Li2O", "Li2S", "NdF3", "NiO", "SiO2"]
    FORM = {"Ag2O": "Li22Ag2P4S19Cl4O", "Al2O3": "Li21AlP4S19Cl4O", "Al2S3": "Li21AlP4S20Cl4", "CoO": "Li22CoP4S19Cl4O",
            "Cu2O": "Li22Cu2P4S19Cl4O", "GeO2": "Li20GeP4S18Cl4O2", "Li2O": "Li24P4S19Cl4O", "Li2S": "Li24P4S20Cl4",
            "NdF3": "Li21NdP4S20Cl3F", "NiO": "Li22NiP4S19Cl4O", "SiO2": "Li20SiP4S18Cl4O2"}
    # 반충 LNO 반응식 — 도펀트 산물만 의미가 있다 (나머지 산물은 같은 꼴)
    RXN = {"Ag2O": "0.5 Li0.5NiO2 + 0.1 Li22Ag2P4S19Cl4O -> 0.0985 Ag2S + 0.003 Ag + 0.3 NiS2 + 0.4 Li3PO4",
           "Al2O3": "0.5 Li0.5NiO2 + 0.1 Li21AlP4S19Cl4O -> 0.1 LiAlO2 + 0.3 NiS2",
           "Al2S3": "0.5 Li0.5NiO2 + 0.1 Li21AlP4S20Cl4 -> 0.1 LiAlS2 + 0.3 NiS2",
           "CoO": "0.5 Li0.5NiO2 + 0.1 Li22CoP4S19Cl4O -> 0.1 CoS2 + 0.3 NiS2",
           "Cu2O": "0.5 Li0.5NiO2 + 0.1 Li22Cu2P4S19Cl4O -> 0.2 Cu + 0.3 NiS2",
           "GeO2": "0.5 Li0.5NiO2 + 0.1 Li20GeP4S18Cl4O2 -> 0.3 Li4GeO4 + 0.3 NiS2",          # Ge 0.1 → 0.3 (원자 수 불일치)
           "Li2O": "0.5 Li0.5NiO2 + 0.1 Li24P4S19Cl4O -> 0.3 NiS2 + 0.4 Li3PO4",
           "Li2S": "0.5 Li0.5NiO2 + 0.1 Li24P4S20Cl4 -> 0.3 NiS2 + 0.4 Li3PO4",
           "NdF3": "0.5 Li0.5NiO2 + 0.1 Li21NdP4S20Cl3F -> 0.1 NdPO4 + 0.1 LiF + 0.3 NiS2",
           "NiO": "0.5 Li0.5NiO2 + 0.1 Li22NiP4S19Cl4O -> 0.4 NiS2",
           "SiO2": "Li20SiP4S18Cl4O2 -> Li20SiP4S18Cl4O2"}
    DE = {"Ag2O": -0.420, "Al2O3": -0.380, "Al2S3": -0.385, "CoO": -0.430, "Cu2O": -0.395, "GeO2": -0.360,
          "Li2O": -0.402, "Li2S": -0.398, "NdF3": -0.415, "NiO": -0.390, "SiO2": 0.0}
    GAPS = {"Ag2S": {"band_gap_MP_eV": 2.5}, "LiAlO2": {"band_gap_MP_eV": 5.0}, "LiAlS2": {"band_gap_MP_eV": 1.5},
            "Li4GeO4": {"band_gap_MP_eV": 4.0}, "NdPO4": {"band_gap_MP_eV": 1.5}, "LiF": {"band_gap_MP_eV": 8.7},
            "Li3PO4": {"band_gap_MP_eV": 5.9}, "NiS2": {"band_gap_MP_eV": 0.0}, "CoS2": {"band_gap_MP_eV": 0.0}}
    MAN = {"mp_db_version_before": "2025.09.25", "mp_db_version_after": "2025.09.25", "same_mp_version": True,
           "invocations": [{"tools_sha16": {AX_PHYS_TOOLS[0]: "1" * 16, AX_PHYS_TOOLS[1]: "2" * 16}},
                           {"tools_sha16": {AX_PHYS_TOOLS[0]: "1" * 16, AX_PHYS_TOOLS[1]: "2" * 16}}],
           "pymatgen": "2025.6.14", "mp_api": "0.45.7", "thermo_types": ["GGA_GGA+U"],
           "correction_names_sample_Li-Ni-O": ["MP2020 anion correction (oxide)"],
           "tools_sha16": {"a": "1" * 16, "b": "2" * 16, "c": "3" * 16}, "repo_head": "f" * 40,
           "lanes": {"designs_lno": {"rc": 0}}}
    HOST = {"LNO_full": -0.300, "LNO_half": -0.400, "LCO_full": -0.320, "LCO_half": -0.455, "NCM_full": -0.310, "NCM_half": -0.420}
    def row(sp, st, de, rxn, **k):
        r = {"species": sp, "formula": FORM.get(sp, "Li6PS5Cl"), "cathode": st, "mode": "closed_0V", "dE_eV_per_atom": de,
             "reaction": rxn, "min_kink_at_endpoint": rxn.split("->")[0].strip() == rxn.split("->")[1].strip()}
        r.update(k)
        return r
    def build(td, mut=None):
        d = Path(td)
        D = {"lno": [], "lco": [], "host": []}
        for sp in EXP:
            D["lno"].append(row(sp, "LNO_full", DE[sp] + 0.1, RXN[sp]))
            D["lno"].append(row(sp, "LNO_half", DE[sp], RXN[sp]))
            rx_c = RXN[sp].replace("Li0.5NiO2", "Li0.5CoO2")
            de_c = DE[sp] - 0.055
            if sp == "Al2O3":                    # R4 — 같은 등급 · δ 부호 반대 (둘 다 |δ| ≥ 10)
                de_c = HOST["LCO_half"] - 0.020
            if sp == "Al2S3":                    # R4 — 등급이 다르다 (LCO 에서는 넓은 갭)
                rx_c = rx_c.replace("LiAlS2", "LiAlO2")
            D["lco"].append(row(sp, "LCO_half", de_c, rx_c))
        for st, v in HOST.items():
            D["host"].append(row("HOST", st, v, "0.5 X + 0.5 Y -> 0.5 Z"))
        G_ = {"gaps": dict(GAPS)}
        M_ = dict(MAN)
        if mut:
            mut(D, G_, M_)
        for k, nm in (("lno", "designs_lno"), ("lco", "designs_lco"), ("host", "host")):
            (d / f"{nm}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in D[k]), encoding="utf-8")
        (d / "product_gaps.json").write_text(json.dumps(G_), encoding="utf-8")
        (d / "manifest.json").write_text(json.dumps(M_), encoding="utf-8")
        return d
    def run(mut=None, card_text=card, decision=("active", "db/properties/" + AXIS_CARD.name), post=None):
        with tempfile.TemporaryDirectory() as td:
            d = build(td, mut)
            if post:
                post(d)
            return ax_readout(d, expected={k: FORM[k] for k in EXP}, card_text=card_text, decision=decision)
    r0 = run()
    by = {x["species"]: x for x in r0.get("rows", [])}
    want = {"Ag2O": "metallic", "Al2O3": "wide", "Al2S3": "intermediate", "CoO": "undetermined", "Cu2O": "metallic",
            "GeO2": "fate_error", "Li2O": "na", "Li2S": "na", "NdF3": "undetermined", "NiO": "na", "SiO2": "no_reaction"}
    got = {k: v["class_LNO_half"] for k, v in by.items()}
    chk(not r0["blocking"] and got == want,
        f"양성: 막는 게이트 통과 · 등급 (Ag 1.5 % 금속 → ⓑ · LiAlO2 → ⓐ · LiAlS2 1.5 eV → ⓒ · CoS2 → ⓓ · Cu → ⓑ · Ge 원자 수 불일치 → 판독 오류 · "
        f"Li2O/Li2S/NiO → ㉧ · NdPO4 4f 하한 1.5 → ⓓ · 끝점 → ⓔ) ({ {k: (got.get(k), v) for k, v in want.items() if got.get(k) != v} })")
    chk(by["Al2O3"]["delta_LNO_half_meV"] == 20.0 and by["SiO2"]["delta_LNO_half_meV"] == 400.0 and by["Li2O"]["differs_from_host"] is False
        and by["Ag2O"]["differs_from_host"] is True and r0["summary"]["n_differs_from_host"] == sum(abs(DE[s] * 1000 + 400) >= 10 for s in EXP),
        "δ = 설계 − 호스트 (반충 LNO · meV/atom) · |δ| ≥ 10 일 때만 '다르다' (Li2O 2 → 같다 · Ag2O 20 → 다르다 · 끝점 SiO2 = 0 − 호스트)")
    fa = by["Ag2O"]["fate_LNO_half"]["Ag"]
    chk(abs(fa["shares"]["metallic"] - 0.015) < 1e-4 and abs(fa["shares"]["wide"] - 0.985) < 1e-4,
        f"도펀트 행방 = 계수 × 산물 속 원자 수의 몫 (Ag: Ag2S {fa['shares']['wide']} · Ag {fa['shares']['metallic']})")
    chk(by["Al2O3"]["R4_cathode_dependent"] is True and by["Al2S3"]["R4_cathode_dependent"] is True
        and by["Ag2O"]["R4_cathode_dependent"] is False and by["NiO"]["R4_cathode_dependent"] is None
        and by["CoO"]["R4_cathode_dependent"] is None,
        "R4: 등급이 다르거나 (Al2S3) 둘 다 |δ| ≥ 10 인데 부호가 반대 (Al2O3) 면 양극 의존 · 같으면 아님 · 한쪽이 ㉧ 이면 비교 안 함")
    pr = {(p_["oxide"], p_["sulfide"]): p_ for p_ in r0["pairs_R5"]}
    chk(pr[("Al2O3", "Al2S3")]["differs"] is True and pr[("Li2O", "Li2S")]["differs"] is False
        and pr[("CaO", "CaS")].get("missing") is True,
        "R5: Al 짝은 |δ_O − δ_S| 5 < 10 이어도 등급이 달라 '다르다' · Li 짝은 |δ_O − δ_S| 4 < 10 · 등급 같음 → '같다' · 없는 짝은 missing")
    chk(r0["gates"]["G6"]["label"] == "NCM 대리 (LiNiO₂)" and r0["gates"]["G4"]["discriminates"] is True
        and r0["gates"]["G1b"]["ok"] and r0["gates"]["G1b"]["ratio_to_Xiao"]["full"] == round(-320 / -339, 3),
        "G6 비 1.03 · 1.05 → 'NCM 대리' · G4 IQR ≥ 10 → R1 사용 가능 · G1b 비율 = 호스트 / Xiao")
    # 음성 — 막는 게이트
    def drop(k):
        return lambda D, G_, M_: M_.pop(k)
    neg = {
        "manifest_no_head": (run(drop("repo_head")), "G1"),
        "manifest_tools_two": (run(lambda D, G_, M_: M_.update(tools_sha16={"a": "1", "b": "2"})), "G1"),
        "mp_version_moved": (run(lambda D, G_, M_: M_.update(mp_db_version_after="2026.01.01")), "G3"),
        "mp_same_flag_false": (run(lambda D, G_, M_: M_.update(same_mp_version=False)), "G3"),
        "anchor_positive": (run(lambda D, G_, M_: D["host"].__setitem__(2, row("HOST", "LCO_full", 0.01, "x -> y"))), "G1b"),
        "anchor_ratio": (run(lambda D, G_, M_: D["host"].__setitem__(2, row("HOST", "LCO_full", -0.15, "x -> y"))), "G1b"),   # 비 0.44 · 순서는 맞음
        "anchor_order": (run(lambda D, G_, M_: D["host"].__setitem__(3, row("HOST", "LCO_half", -0.300, "x -> y"))), "G1b"),
        "row_missing": (run(lambda D, G_, M_: D["lno"].pop(3)), "G2"),
        "row_error": (run(lambda D, G_, M_: D["lno"].__setitem__(3, {**D["lno"][3], "error": "x"})), "G2"),
        "row_dup": (run(lambda D, G_, M_: D["lno"].append(dict(D["lno"][3]))), "G2"),
        "row_open_mode": (run(lambda D, G_, M_: D["lno"].__setitem__(3, {**D["lno"][3], "mode": "grand_potential"})), "G2"),
        "row_extra_species": (run(lambda D, G_, M_: D["lno"].append(row("ZrO2", "LNO_half", -0.4, "a -> b"))), "G2"),
        "host_lno_missing": (run(lambda D, G_, M_: D["host"].pop(1)), "G2"),
        "row_other_formula": (run(lambda D, G_, M_: D["lno"].__setitem__(3, {**D["lno"][3], "formula": "Li20AlP4S19Cl4O"})), "G2"),
        "phys_tool_drift": (run(lambda D, G_, M_: M_.update(invocations=[{"tools_sha16": {AX_PHYS_TOOLS[0]: "a", AX_PHYS_TOOLS[1]: "b"}},
                                                                        {"tools_sha16": {AX_PHYS_TOOLS[0]: "c", AX_PHYS_TOOLS[1]: "b"}}])), "G1"),
        "jsonl_garbled": (run(post=lambda d: open(d / "designs_lno.jsonl", "a").write("{\"species\": \x00\n")), "G1"),
        "decision_proposed": (run(decision=("proposed", "db/properties/" + AXIS_CARD.name)), "decision"),
        "decision_other_card": (run(decision=("active", "db/properties/other.json")), "decision"),
        "card_threshold_changed": (run(card_text=card.replace("MP 갭 ≥ 2.0 eV", "MP 갭 ≥ 2.5 eV")), "G5"),
    }
    bad = {k: v[0]["blocking"] for k, v in neg.items() if v[1] not in v[0]["blocking"] or "rows" in v[0]}
    chk(not bad, f"⛔음성: 막는 게이트마다 깨면 표를 안 낸다 — manifest 필드 · 도구 sha · MP 판 이동 · 앵커 부호 · 비율 · 순서 · "
                 f"행 빠짐 · 오류 행 · 중복 · 열린계 행 · 카드 밖 종 · 호스트 행 · 다른 조성 · 실행 사이 물리 도구 바뀜 · 깨진 줄 · 결정 proposed · "
                 f"다른 카드 · 카드 문턱 변경 ({bad})")
    ro = ax_roster()
    chk(len(ro) == 91 and ro.get("As2S3") == "As2Cl4Li28P2S20" and ro.get("LiCl") == "Cl5Li24P4S19",
        f"대상 = 카드 §1b · 개정 1 의 91 종 = 1 단계 계면 표의 조성 그대로 (As2S3 · LiCl = Cl5Li24P4S19 — 지금 CSV 를 다시 뽑으면 "
        f"호스트와 같은 조성이 나오는 종) — {len(ro)} 종")
    with tempfile.TemporaryDirectory() as tdr:
        pr_ = Path(tdr) / "r.jsonl"
        pr_.write_text(json.dumps({"species": "X", "cathode": "LNO", "formula": "A"}) + "\n"
                       + json.dumps({"species": "X", "cathode": "LCO", "formula": "B"}) + "\n", encoding="utf-8")
        try:
            ax_roster(pr_); bad_r = False
        except ValueError:
            bad_r = True
    chk(bad_r, "⛔음성: 같은 종의 조성이 양극마다 다르면 대상 표를 만들지 않는다")
    # 음성 — 판정 쪽
    r_iqr = run(lambda D, G_, M_: [x.update(dE_eV_per_atom=-0.401) for x in D["lno"] if x["cathode"] == "LNO_half"])
    chk(r_iqr["gates"]["G4"]["discriminates"] is False and "갈리지 않는다" in r_iqr["gates"]["G4"]["use"],
        "⛔음성 G4: δ 가 다 1 meV/atom 안이면 IQR < 10 → 'R1 은 이 축에서 갈리지 않는다' 선언")
    r_g6 = run(lambda D, G_, M_: D["host"].__setitem__(5, row("HOST", "NCM_half", -1.2, "x -> y")))
    r_g6b = run(lambda D, G_, M_: D["host"].pop(5))
    chk(r_g6["gates"]["G6"]["label"] == "LiNiO₂ 계면" and r_g6b["gates"]["G6"]["label"] == "LiNiO₂ 계면" and not r_g6["blocking"],
        "⛔음성 G6: NCM / LNO 비 3 · NCM 행 없음 → 'LiNiO₂ 계면' 으로만 (막지는 않는다)")
    r_b = run(lambda D, G_, M_: [x.update(reaction="0.5 Li0.5NiO2 + 0.1 Li22Ag2P4S19Cl4O -> 0.0992 Ag2S + 0.0016 Ag + 0.3 NiS2")
                                 for x in D["lno"] if x["species"] == "Ag2O" and x["cathode"] == "LNO_half"])
    r_c = run(lambda D, G_, M_: [x.update(reaction="0.5 Li0.5NiO2 + 0.1 Li22Ag2P4S19Cl4O -> 0.0981 Ag2S + 0.0038 Ag + 0.3 NiS2")
                                 for x in D["lno"] if x["species"] == "Ag2O" and x["cathode"] == "LNO_half"])
    cb = {x["species"]: x for x in r_b["rows"]}["Ag2O"]
    cc = {x["species"]: x for x in r_c["rows"]}["Ag2O"]
    chk(cb["class_LNO_half"] == "wide" and cc["class_LNO_half"] == "metallic",
        f"⛔음성 문턱 경계: 금속성 몫 0.8 % → ⓐ (≥ 90 % 넓은 갭) · 1.9 % → ⓑ ({cb['fate_LNO_half']['Ag']['shares']} · {cc['fate_LNO_half']['Ag']['shares']})")
    r_w = run(lambda D, G_, M_: [x.update(reaction="0.5 Li0.5NiO2 + 0.1 Li21AlP4S19Cl4O -> 0.088 LiAlO2 + 0.012 LiAlS2 + 0.3 NiS2")
                                 for x in D["lno"] if x["species"] == "Al2O3" and x["cathode"] == "LNO_half"])
    r_m = run(lambda D, G_, M_: G_["gaps"].pop("LiAlO2"))
    cw = {x["species"]: x for x in r_w["rows"]}["Al2O3"]["class_LNO_half"]
    cm = {x["species"]: x for x in r_m["rows"]}["Al2O3"]["class_LNO_half"]
    chk(cw == "intermediate" and cm == "undetermined",
        f"⛔음성: 넓은 갭 88 % → ⓐ 아님 (ⓒ) · 갭을 못 찾은 산물 → 미판정 ({cw} · {cm})")
    r_g0 = run(lambda D, G_, M_: G_["gaps"].update(LiAlS2={"band_gap_MP_eV": 0.05}))
    r_g1 = run(lambda D, G_, M_: G_["gaps"].update(LiAlS2={"band_gap_MP_eV": 0.1}))
    c0 = {x["species"]: x for x in r_g0["rows"]}["Al2S3"]["class_LNO_half"]
    c1 = {x["species"]: x for x in r_g1["rows"]}["Al2S3"]["class_LNO_half"]
    chk(c0 == "metallic" and c1 == "intermediate",
        f"⛔음성 문턱 경계: TM 없는 산물 MP 갭 0.05 eV → 금속성 (ⓑ) · 0.1 eV → 좁은 갭 (ⓒ) ({c0} · {c1})")
    r_nd = run(lambda D, G_, M_: G_["gaps"].update(NdPO4={"band_gap_MP_eV": 2.4}))
    chk({x["species"]: x for x in r_nd["rows"]}["NdF3"]["class_LNO_half"] == "wide",
        "4f 하한 ≥ 2.0 이면 넓은 갭 (NdPO4 2.4 → F · Nd 둘 다 넓은 갭 → ⓐ)")
    print(f"axis_ncm selftest: ⭕ {n[0]} · ⛔ {n[1]}")
    return 0 if ok_all else 1


# ══════════════════════════════════════════════════════════════════════════════════════════════════
# 축 ② 가수분해 판독 — 카드 db/properties/cascade_axis_hydrolysis_estimand_2026_11_04.json (결정 D-2026-11-04-cascade-axis-hydrolysis)
#   실행:  python3 tools/cascade/analyze_cathode_reactivity.py --axis_hyd <run_dir> [--out <json>] [--ncm <축 ① 판독 json>]
#   + 합치는 규칙 (D-2026-11-04-cascade-axes-combination-rule) R1 · R2 · R3 · R4 — 축 ① 판독과 합쳐 선택 집합 (또는 표시만)
#   ⛔ 못 하는 것: 계산을 다시 하지 않는다 · H₂S 를 '발생량' 으로 바꾸지 않는다 · Zhu 2020 대조는 기록만 (판정 · 게이트 아님) ·
#     합치는 규칙에 새 숫자를 넣지 않는다 (축 카드에 봉인된 표시 · 방향만).
# ══════════════════════════════════════════════════════════════════════════════════════════════════
HYD_CARD = PROP / "cascade_axis_hydrolysis_estimand_2026_11_04.json"
HYD_DECISION = "D-2026-11-04-cascade-axis-hydrolysis"
NCM_READOUT = PROP / "cascade_axis_ncm_readout_2026_11_04.json"
ZHU_CSV = PROP / "zhu2020_si_hydrolysis_energies.csv"
HY = {"delta_meV": 10.0, "iqr_meV": 10.0, "df_flag": 0.10, "pair_df": 0.10, "rho_overlap": 0.8}
HY_CARD_TEXT = ("|δ_hyd| ≥ 10 meV/atom", "IQR < 10", "Δf ≥ +0.10", "|ρ| ≥ 0.8", "δ_hyd ≤ −10 meV/atom", "|f_O − f_S| ≥ 0.10")


def _norm_comp(c):
    t = sum(c.values())
    return {k: v / t for k, v in c.items()} if t > 0 else {}


def hy_h2s_share(row, formula):
    """조성의 S 중 H₂S 로 가는 몫 f — (f | None, 문제 | None). 끝점 (반응 없음) 이면 0.
    좌변의 설계 항 = 조성 비율이 formula 와 같은 항 (없으면 판독 오류) · 우변 H₂S = 조성이 정확히 {H: 2, S: 1} 인 항."""
    if row.get("min_kink_at_endpoint") is True:
        return 0.0, None
    rxn = row.get("reaction")
    if not isinstance(rxn, str) or "->" not in rxn:
        return None, "반응식이 없다"
    try:
        lhs, rhs = rxn.split("->", 1)
        want = _norm_comp(_ax_pf(formula))
        L = [(c, f, _ax_pf(f)) for c, f in parse_side(lhs)]
        hit = [(c, comp) for c, f, comp in L if comp and all(abs(_norm_comp(comp).get(k, 0.0) - want.get(k, 0.0)) <= 1e-6
                                                           for k in set(want) | set(comp))]
        if len(hit) != 1 or not hit[0][1].get("S"):
            return None, "좌변에서 설계 항을 하나로 못 찾는다"
        c_se, comp_se = hit[0]
        n_s = c_se * comp_se["S"]
        n_h2s = sum(c for c, f in parse_side(rhs) if _ax_pf(f) == {"H": 2.0, "S": 1.0})
        return n_h2s / n_s, None
    except (ValueError, TypeError) as e:
        return None, f"반응식을 못 읽는다 ({type(e).__name__})"


def _spearman(xs, ys):
    """Spearman ρ (평균 순위 · 동률 처리) — 표본 3 미만이면 None."""
    if len(xs) < 3:
        return None
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
                j += 1
            for k in range(i, j + 1):
                r[o[k]] = (i + j) / 2.0 + 1.0
            i = j + 1
        return r
    rx, ry = rk(xs), rk(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else None


def _hy_decision():
    d = json.loads((ROOT / "db" / "governance" / "decisions.json").read_text(encoding="utf-8"))
    x = [y for y in d["decisions"] if y.get("id") == HYD_DECISION]
    return (x[0].get("decision_state"), x[0].get("card")) if x else (None, None)


def hy_gates(L, expected, card_text, decision_state, decision_card):
    """결정 · G1 · G1b · G2 · G3 · G5 (축 ② 카드 §4) — G4 · G7 은 hy_readout 이 δ 를 낸 뒤 잰다."""
    G = {"decision": {"ok": decision_state == "active" and decision_card == "db/properties/" + HYD_CARD.name,
                      "state": decision_state, "card": decision_card}}
    man = L.get("manifest") if isinstance(L.get("manifest"), dict) else {}
    miss = [k for k in AX_MANIFEST_KEYS if man.get(k) in (None, "", [], {})]
    invs = man.get("invocations") if isinstance(man.get("invocations"), list) and man.get("invocations") else [man]
    for t in AX_PHYS_TOOLS:
        v = {(x.get("tools_sha16") or {}).get(t) for x in invs if isinstance(x, dict)}
        if len(v) != 1 or None in v:
            miss.append(f"물리 도구 sha 가 실행마다 다르거나 없다 ({t})")
    G["G1"] = {"ok": not miss and not L["problems"], "missing": miss, "load_problems": L["problems"][:10]}
    vb, va = man.get("mp_db_version_before"), man.get("mp_db_version_after")
    G["G3"] = {"ok": man.get("same_mp_version") is True and vb not in (None, "") and vb == va, "before": vb, "after": va}
    ixd, ixh = ax_index(L.get("designs_hyd")), ax_index(L.get("host_hyd"))
    prob = [f"{nm} 없음" for nm, k in (("designs_hyd.jsonl", "designs_hyd"), ("host_hyd.jsonl", "host_hyd")) if L.get(k) is None]
    for sp in expected:
        rs = ixd.get((sp, "H2O")) or []
        if len(rs) != 1 or not _ax_ok(rs[0]):
            prob.append(f"{sp} × H2O: 행 {len(rs)} 개 · 정상 {sum(1 for r in rs if _ax_ok(r))}")
        elif rs[0].get("formula") != expected[sp]:
            prob.append(f"{sp} × H2O: 조성 {rs[0].get('formula')} ≠ 카드 대상 {expected[sp]}")
    extra = sorted({k[0] for k in ixd} - set(expected))
    if extra:
        prob.append(f"카드에 없는 종 {extra[:5]}")
    h = _ax_one(ixh, ("HOST", "H2O"))
    if h is None:
        prob.append("HOST × H2O: 정상 행 하나가 아니다")
    G["G2"] = {"ok": not prob, "n_problems": len(prob), "problems": prob[:20], "n_expected": len(expected)}
    g1b = {"ok": False, "why": "호스트 × H2O 정상 행이 없다"}
    if h is not None:
        fh, why = hy_h2s_share(h, h.get("formula") or "Li6PS5Cl")
        g1b = {"ok": bool(h["dE_eV_per_atom"] < 0 and fh is not None and fh > 0),
               "host_dE_negative": h["dE_eV_per_atom"] < 0, "host_H2S_share": None if fh is None else round(fh, 4),
               "host_reaction": h.get("reaction"), **({"why": why} if why else {})}
    G["G1b"] = g1b
    miss5 = [t for t in HY_CARD_TEXT if t not in (card_text or "")]
    G["G5"] = {"ok": not miss5, "missing_in_card": miss5, "card_sha256": hashlib.sha256((card_text or "").encode("utf-8")).hexdigest()}
    return G


def _zhu_dg():
    """Zhu 2020 SI — 화합물 → dG_hyd (eV/H₂O · 발표값 · + = 수분 안정). 기록만."""
    if not ZHU_CSV.is_file():
        return {}
    out = {}
    rows = [ln for ln in ZHU_CSV.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    for r in csv.DictReader(rows):
        try:
            out.setdefault(r["compound"], float(r["dG_hyd_eV_per_H2O_as_published"]))
        except (KeyError, ValueError):
            continue
    return out


def hy_readout(run_dir, expected=None, card_text=None, decision=None, ncm=None):
    """카드 §2 · §4 대로 판독 — 막는 게이트 (결정 · G1 · G1b · G2 · G3 · G5) 가 하나라도 불통과면 표를 내지 않는다."""
    L = ax_load(run_dir)
    for k in ("designs_hyd", "host_hyd"):           # ax_load 는 축 ① 이름만 읽는다 — 축 ② 파일을 더 읽는다
        p = Path(run_dir) / f"{k}.jsonl"
        rows = []
        if p.is_file():
            for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if not ln.strip():
                    continue
                try:
                    r = json.loads(ln)
                    if not isinstance(r, dict):
                        raise ValueError
                    rows.append(r)
                except ValueError as e:
                    L["problems"].append(f"{k}.jsonl {i} 번째 줄을 못 읽는다 ({type(e).__name__})")
            L[k] = rows
        else:
            L[k] = None
    expected = ax_roster() if expected is None else expected
    card_text = HYD_CARD.read_text(encoding="utf-8") if card_text is None else card_text
    decision = _hy_decision() if decision is None else decision
    G = hy_gates(L, expected, card_text, *decision)
    blocking = [k for k in ("decision", "G1", "G1b", "G2", "G3", "G5") if not G[k]["ok"]]
    res = {"card": "db/properties/" + HYD_CARD.name, "decision": HYD_DECISION, "run_dir": str(run_dir), "constants": HY,
           "gates": G, "blocking": blocking,
           "⛔": "상대값만 — 순위 · 거르기는 합치는 규칙대로 (R3 · R4) · H₂S 몫은 발생량이 아니다 · Lee 2024 · Zhu 2020 과 섞지 않는다"}
    if blocking:
        res["⛔_표_없음"] = f"막는 게이트 불통과 {blocking} — 표를 내지 않는다 (카드 §4)"
        return res
    ixd, ixh = ax_index(L["designs_hyd"]), ax_index(L["host_hyd"])
    h = _ax_one(ixh, ("HOST", "H2O"))
    e_h = h["dE_eV_per_atom"] * 1000.0
    f_h = G["G1b"]["host_H2S_share"]
    rows = []
    for sp in sorted(expected):
        r = ixd[(sp, "H2O")][0]
        d_ = r["dE_eV_per_atom"] * 1000.0 - e_h
        f_, why = hy_h2s_share(r, expected[sp])
        df_ = None if f_ is None else f_ - f_h
        rows.append({"species": sp, "formula": expected[sp], "delta_hyd_meV": round(d_, 2), "differs_from_host": abs(d_) >= HY["delta_meV"],
                     "H2S_share": None if f_ is None else round(f_, 4), "dH2S_share": None if df_ is None else round(df_, 4),
                     "endpoint": r.get("min_kink_at_endpoint"), "reaction": r.get("reaction"),
                     "F1_hyd": d_ <= -HY["delta_meV"], "F2_H2S": bool(df_ is not None and df_ >= HY["df_flag"]),
                     "unknown": f_ is None, **({"why": why} if why else {})})
    ds = [x["delta_hyd_meV"] for x in rows]
    q1, _, q3 = statistics.quantiles(ds, n=4, method="inclusive")
    G["G4"] = {"q1_meV": round(q1, 2), "q3_meV": round(q3, 2), "iqr_meV": round(q3 - q1, 2), "discriminates": (q3 - q1) >= HY["iqr_meV"],
               "method": "statistics.quantiles(n=4, method='inclusive')"}
    nc = ncm if ncm is not None else (json.loads(NCM_READOUT.read_text(encoding="utf-8")) if NCM_READOUT.is_file() else None)
    nd = {x["species"]: x for x in (nc or {}).get("rows", [])}
    common = [x["species"] for x in rows if x["species"] in nd]
    rho = _spearman([nd[s_]["delta_LNO_half_meV"] for s_ in common], [x["delta_hyd_meV"] for x in rows if x["species"] in nd])
    G["G7"] = {"rho_spearman": None if rho is None else round(rho, 4), "n": len(common),
               "overlap": None if rho is None else abs(rho) >= HY["rho_overlap"],
               "use": ("판정 불가 (축 ① 판독 없음)" if rho is None else
                       "겹침 — Pareto 에는 축 ① δ 만 · 축 ② 는 위험 표시로만" if abs(rho) >= HY["rho_overlap"] else
                       "안 겹침 — 두 축 다 Pareto 에 넣는다 (G4 통과 축만)")}
    by = {x["species"]: x for x in rows}
    pairs = []
    for o, s_ in AX_PAIRS:
        a, b = by.get(o), by.get(s_)
        if not (a and b):
            pairs.append({"oxide": o, "sulfide": s_, "missing": True}); continue
        dd = a["delta_hyd_meV"] - b["delta_hyd_meV"]
        dfp = None if (a["H2S_share"] is None or b["H2S_share"] is None) else a["H2S_share"] - b["H2S_share"]
        pairs.append({"oxide": o, "sulfide": s_, "delta_O_minus_S_meV": round(dd, 2),
                      "f_O_minus_S": None if dfp is None else round(dfp, 4),
                      "differs": bool(abs(dd) >= HY["delta_meV"] or (dfp is not None and abs(dfp) >= HY["pair_df"]))})
    zd = _zhu_dg()
    zz = [(x["delta_hyd_meV"], zd[x["species"]]) for x in rows if x["species"] in zd]
    res.update({"rows": rows, "pairs_R5": pairs,
                "R6_zhu_기록만": {"n": len(zz), "rho_spearman": (None if len(zz) < 3 else round(_spearman([a for a, _ in zz], [b for _, b in zz]), 4)),
                                 "⛔": "다른 양 (이진 황화물 ΔG · 기체 분압) — 판정 · 게이트에 안 쓴다"},
                "summary": {"n_designs": len(rows), "n_differs_from_host": sum(x["differs_from_host"] for x in rows),
                            "n_F1_hyd": sum(x["F1_hyd"] for x in rows), "n_F2_H2S": sum(x["F2_H2S"] for x in rows),
                            "n_unknown": sum(x["unknown"] for x in rows), "host_H2S_share": f_h,
                            "n_pairs_differ": sum(1 for p_ in pairs if p_.get("differs"))}})
    return res


def ax_combine(ncm, hyd, li=None):
    """합치는 규칙 (D-2026-11-04-cascade-axes-combination-rule) — 새 숫자 없음.
    R1 위험 표시 (축 ① F1 금속성 · F2 δ ≤ −10 · 축 ② F1_hyd · F2_H2S) 가 하나라도 있으면 선택 집합에서 뺀다 (표에는 남긴다).
    R3 연속 축 = G4 통과 축 (축 ② 는 G7 겹침이면 빼고 표시로만) · 둘 이상이면 Pareto 비지배 집합 (모두 '클수록 좋다') · R4 하나면 표시만.
    반환 {"axes_in_pareto", "selection" | None, "rows"}."""
    if ncm.get("blocking") or hyd.get("blocking"):
        return {"⛔": "막는 게이트 불통과 축이 있다 — 합치지 않는다", "selection": None}
    if li is not None and li.get("blocking"):              # 축 ③ (2026-11-04 · D-2026-11-04-cascade-axis-li-anode)
        return {"⛔": "막는 게이트 불통과 축이 있다 (축 ③) — 합치지 않는다", "selection": None}
    nd = {x["species"]: x for x in ncm["rows"]}
    hd = {x["species"]: x for x in hyd["rows"]}
    ld = {x["species"]: x for x in li["rows"]} if li is not None else None
    sp = sorted(set(nd) & set(hd))
    if ld is not None:
        sp = sorted(set(sp) & set(ld))
    axes = []
    if ncm["gates"].get("G4", {}).get("discriminates"):
        axes.append(("delta_NCM_LNO_half_meV", lambda s_: nd[s_]["delta_LNO_half_meV"]))
    g7 = hyd["gates"].get("G7", {})
    if hyd["gates"].get("G4", {}).get("discriminates") and g7.get("overlap") is False:
        axes.append(("delta_hyd_meV", lambda s_: hd[s_]["delta_hyd_meV"]))
    if ld is not None:
        g7l = li["gates"].get("G7", {})
        if li["gates"].get("G4", {}).get("discriminates") and g7l.get("overlap") is False:     # 축 ③ 카드 G4 · G7
            axes.append(("delta_Li_meV", lambda s_: ld[s_]["delta_Li_meV"]))
    rows = []
    for s_ in sp:
        fl = [f for f, c in (("축①F1_금속성", nd[s_]["class_LNO_half"] == "metallic"),
                             ("축①F2_반응증가", nd[s_]["delta_LNO_half_meV"] <= -AX["delta_meV"]),
                             ("축②F1_가수분해증가", hd[s_]["F1_hyd"]), ("축②F2_H2S증가", hd[s_]["F2_H2S"])) if c]
        unk = [u for u, c in (("축①R2", nd[s_]["class_LNO_half"] in ("undetermined", "na")), ("축②H2S", hd[s_]["unknown"])) if c]
        if ld is not None:                                   # 축 ③ 위험 표시 · 모름 (카드 합치는_규칙_연결 — 세 축 표시를 모두 쓴다)
            fl += [f for f, c in (("축③F1_Li금속성", ld[s_]["F1_Li"]), ("축③F2_Li반응증가", ld[s_]["F2_Li"])) if c]
            unk += ["축③R2"] if ld[s_]["unknown"] else []
        rows.append({"species": s_, "flags": fl, "unknown": unk, **{a: f(s_) for a, f in axes}})
    out = {"axes_in_pareto": [a for a, _ in axes], "n_designs": len(rows), "n_flagged": sum(1 for r in rows if r["flags"])}
    if len(axes) < 2:
        out.update({"selection": None, "rule": "R4 — 연속 축이 하나 이하라 표시만 (고르지 않는다)", "rows": rows})
        return out
    cand = [r for r in rows if not r["flags"]]
    keys = [a for a, _ in axes]
    def dominated(r):
        return any(all(o[k] >= r[k] for k in keys) and any(o[k] > r[k] for k in keys) for o in cand if o is not r)
    sel = sorted(r["species"] for r in cand if not dominated(r))
    for r in rows:
        r["pareto"] = r["species"] in sel
    out.update({"selection": sel, "rule": "R3 — 표시 없는 설계의 Pareto 비지배 집합 (가중치 없음 · 순위 없음)", "rows": rows})
    return out


def hy_main(argv):
    i = argv.index("--axis_hyd")
    run_dir = argv[i + 1] if i + 1 < len(argv) else None
    if not run_dir:
        print("⛔ --axis_hyd <run_dir>")
        return 2
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else \
        PROP / f"cascade_axis_hyd_readout_{datetime.date.today().strftime('%Y_%m_%d')}.json"
    ncm_p = Path(argv[argv.index("--ncm") + 1]) if "--ncm" in argv else NCM_READOUT
    ncm = json.loads(ncm_p.read_text(encoding="utf-8")) if ncm_p.is_file() else None
    res = hy_readout(run_dir, ncm=ncm)
    if not res["blocking"] and ncm is not None:
        res["combination"] = ax_combine(ncm, res)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k in ("decision", "G1", "G1b", "G2", "G3", "G5", "G4", "G7"):
        g = res["gates"].get(k)
        if g is not None:
            print(f"  {k:8s} {'⭕' if g.get('ok', g.get('discriminates', g.get('overlap') is False)) else '⛔'}  "
                  + json.dumps({x: y for x, y in g.items() if x not in ("problems", "load_problems", "host_reaction")}, ensure_ascii=False)[:160])
    if res["blocking"]:
        print(f"⛔ 막는 게이트 불통과 {res['blocking']} — 표 없음 → {out}")
        return 2
    sm = res["summary"]
    with open(out.with_name(out.stem + "_designs.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# cascade 축 ② 가수분해 (카드 " + res["card"] + ") — δ_hyd = 설계 − 호스트 [meV/atom · MP 닫힌계 · 상대값] · "
                 "H2S_share = 조성의 S 중 H₂S 로 가는 몫 (발생량 아님)\n")
        w = csv.writer(fh)
        cols = ["species", "formula", "delta_hyd_meV", "differs_from_host", "H2S_share", "dH2S_share", "F1_hyd", "F2_H2S", "unknown"]
        w.writerow(cols)
        for r in res["rows"]:
            w.writerow(["" if r.get(c) is None else r.get(c) for c in cols])
    cmb = res.get("combination") or {}
    print(f"설계 {sm['n_designs']} · 호스트와 다름 {sm['n_differs_from_host']} · F1_hyd {sm['n_F1_hyd']} · F2_H2S {sm['n_F2_H2S']} · "
          f"모름 {sm['n_unknown']} · 호스트 H₂S 몫 {sm['host_H2S_share']} · 짝 다름 {sm['n_pairs_differ']}/{len(AX_PAIRS)}")
    print(f"합치는 규칙: {cmb.get('rule')} · Pareto 축 {cmb.get('axes_in_pareto')} · 표시 {cmb.get('n_flagged')} · "
          f"선택 {None if cmb.get('selection') is None else len(cmb['selection'])}")
    print(f"→ {out}")
    return 0


def hy_selftest():
    """축 ② 판독기 + 합치는 규칙 — 양성 · 음성 경로."""
    import tempfile
    ok_all, n = True, [0, 0]
    def chk(c, msg):
        nonlocal ok_all
        n[0 if c else 1] += 1
        ok_all &= bool(c)
        print(("  ⭕ " if c else "  ⛔ ") + msg)
    card = HYD_CARD.read_text(encoding="utf-8")
    FORM = {"Al2O3": "Li21AlP4S19Cl4O", "Al2S3": "Li21AlP4S20Cl4", "Li2O": "Li24P4S19Cl4O", "Li2S": "Li24P4S20Cl4",
            "SnO2": "Li22SnP4S19Cl4O2", "SnS2": "Li22SnP4S21Cl4", "Ag2O": "Li22Ag2P4S19Cl4O"}
    # 반응식 — 설계 항 계수 c · S 원자 수 × 몫 f 로 H₂S 계수를 맞춘다
    def rx(sp, c, f, extra="0.2 LiOH + 0.01 LiHS"):      # LiHS = H–S 산물이지만 H₂S 가 아니다 (세지 않는다)
        S = _ax_pf(FORM[sp])["S"]
        return f"{c} {FORM[sp]} + 1.0 H2O -> {round(c * S * f, 6)} H2S + {extra}"
    F_ = {"Al2O3": 0.40, "Al2S3": 0.52, "Li2O": 0.42, "Li2S": 0.40, "SnO2": 0.25, "SnS2": 0.38, "Ag2O": 0.40}
    DE = {"Al2O3": -0.300, "Al2S3": -0.340, "Li2O": -0.305, "Li2S": -0.310, "SnO2": -0.280, "SnS2": -0.282, "Ag2O": -0.312}
    HOST = {"dE": -0.310, "f": 0.40}
    MAN = {"mp_db_version_before": "2026.09.28", "mp_db_version_after": "2026.09.28", "same_mp_version": True, "pymatgen": "x",
           "mp_api": "y", "thermo_types": ["GGA_GGA+U"], "correction_names_sample_Li-Ni-O": ["c"],
           "tools_sha16": {"a": "1", "b": "2", "c": "3"}, "repo_head": "f" * 40, "lanes": {"x": 1},
           "invocations": [{"tools_sha16": {AX_PHYS_TOOLS[0]: "1", AX_PHYS_TOOLS[1]: "2"}}]}
    def row(sp, de, rxn, form=None, **k):
        r = {"species": sp, "formula": form or FORM.get(sp, "Li6PS5Cl"), "cathode": "H2O", "mode": "closed_0V",
             "dE_eV_per_atom": de, "reaction": rxn, "min_kink_at_endpoint": False}
        r.update(k)
        return r
    def build(td, mut=None):
        d = Path(td)
        D = {"des": [row(sp, DE[sp], rx(sp, 0.05, F_[sp])) for sp in FORM],
             "host": [row("HOST", HOST["dE"], f"0.2 Li6PS5Cl + 1.0 H2O -> {0.2 * 5 * HOST['f']} H2S + 0.1 Li3PO4", form="Li6PS5Cl")]}
        M_ = json.loads(json.dumps(MAN))
        if mut:
            mut(D, M_)
        (d / "designs_hyd.jsonl").write_text("".join(json.dumps(r) + "\n" for r in D["des"]), encoding="utf-8")
        (d / "host_hyd.jsonl").write_text("".join(json.dumps(r) + "\n" for r in D["host"]), encoding="utf-8")
        (d / "manifest.json").write_text(json.dumps(M_), encoding="utf-8")
        return d
    NCM = {"blocking": [], "gates": {"G4": {"discriminates": True}},
           "rows": [{"species": sp, "delta_LNO_half_meV": v, "class_LNO_half": c} for sp, v, c in
                    (("Al2O3", 2.1, "wide"), ("Al2S3", -71.9, "wide"), ("Li2O", 11.4, "na"), ("Li2S", 0.0, "na"),
                     ("SnO2", 49.9, "intermediate"), ("SnS2", 27.2, "wide"), ("Ag2O", 30.0, "metallic"))]}
    def run(mut=None, card_text=card, decision=("active", "db/properties/" + HYD_CARD.name), ncm=NCM):
        with tempfile.TemporaryDirectory() as td:
            return hy_readout(build(td, mut), expected=dict(FORM), card_text=card_text, decision=decision, ncm=ncm)
    r0 = run()
    by = {x["species"]: x for x in r0.get("rows", [])}
    chk(not r0["blocking"] and abs(by["Al2S3"]["delta_hyd_meV"] - (-30.0)) < 1e-6 and abs(by["SnO2"]["delta_hyd_meV"] - 30.0) < 1e-6
        and abs(by["Al2S3"]["H2S_share"] - 0.52) < 1e-4 and abs(by["Al2S3"]["dH2S_share"] - 0.12) < 1e-4
        and r0["gates"]["G1b"]["host_H2S_share"] == 0.4,
        f"양성: 게이트 통과 · δ_hyd = 설계 − 호스트 · H₂S 몫 = H₂S 계수 / (설계 항 계수 × S 수) ({ {k: (v['delta_hyd_meV'], v['H2S_share']) for k, v in by.items()} })")
    chk(by["Al2S3"]["F1_hyd"] and by["Al2S3"]["F2_H2S"] and not by["Al2O3"]["F1_hyd"] and not by["SnO2"]["F2_H2S"],
        "위험 표시: δ_hyd ≤ −10 → F1_hyd (Al2S3 −30) · Δf ≥ +0.10 → F2_H2S (Al2S3 +0.12) · 나머지는 표시 없음")
    pr = {(p_["oxide"], p_["sulfide"]): p_ for p_ in r0["pairs_R5"]}
    chk(pr[("Al2O3", "Al2S3")]["differs"] and pr[("Li2O", "Li2S")]["differs"] is False and pr[("SnO2", "SnS2")]["differs"]
        and pr[("CaO", "CaS")].get("missing"),
        "R5: Al 짝 (δ 차 30) · Sn 짝 (δ 차 2 이지만 f 차 0.13) 다름 · Li 짝 (δ 차 5 · f 차 0.02) 같음 · 없는 짝 missing")
    ncm_rank = {x["species"]: x["delta_LNO_half_meV"] for x in NCM["rows"]}
    r_ov = run(lambda D, M_: [x.update(dE_eV_per_atom=HOST["dE"] + ncm_rank[x["species"]] / 1000.0 / 3.0) for x in D["des"]])
    chk(r_ov["gates"]["G7"]["overlap"] is True and abs(r_ov["gates"]["G7"]["rho_spearman"] - 1.0) < 1e-9,
        f"⛔음성 G7: δ_hyd 순서가 축 ① 과 같으면 ρ = 1 → 겹침 ({r_ov['gates']['G7']})")
    neg = {
        "host_positive": (run(lambda D, M_: D["host"].__setitem__(0, {**D["host"][0], "dE_eV_per_atom": 0.01})), "G1b"),
        "host_no_H2S": (run(lambda D, M_: D["host"].__setitem__(0, {**D["host"][0], "reaction": "0.2 Li6PS5Cl + 1.0 H2O -> 0.1 Li3PO4 + 0.2 LiOH"})), "G1b"),
        "row_missing": (run(lambda D, M_: D["des"].pop(0)), "G2"),
        "row_other_formula": (run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "formula": "Li20AlP4S19Cl4O"})), "G2"),
        "row_open_mode": (run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "mode": "grand_potential"})), "G2"),
        "host_missing": (run(lambda D, M_: D["host"].pop(0)), "G2"),
        "mp_moved": (run(lambda D, M_: M_.update(mp_db_version_after="2027.01.01")), "G3"),
        "manifest_head": (run(lambda D, M_: M_.pop("repo_head")), "G1"),
        "tool_drift": (run(lambda D, M_: M_["invocations"].append({"tools_sha16": {AX_PHYS_TOOLS[0]: "9", AX_PHYS_TOOLS[1]: "2"}})), "G1"),
        "decision_proposed": (run(decision=("proposed", "db/properties/" + HYD_CARD.name)), "decision"),
        "card_changed": (run(card_text=card.replace("Δf ≥ +0.10", "Δf ≥ +0.20")), "G5"),
    }
    bad = {k: v[0]["blocking"] for k, v in neg.items() if v[1] not in v[0]["blocking"] or "rows" in v[0]}
    chk(not bad, f"⛔음성: 막는 게이트마다 깨면 표를 안 낸다 — 호스트 반응 양수 · 호스트 H₂S 없음 · 행 빠짐 · 다른 조성 · 열린계 행 · MP 판 이동 · "
                 f"manifest · 도구 바뀜 · 결정 proposed · 카드 문턱 변경 ({bad})")
    r_term = run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "reaction": "1.0 H2O + 0.05 Li20AlP4S19Cl4O -> 0.3 H2S"}))
    cu = {x["species"]: x for x in r_term["rows"]}["Al2O3"]
    chk(cu["unknown"] and cu["H2S_share"] is None and not r_term["blocking"],
        "⛔음성: 좌변에 대상 조성 항이 없으면 H₂S 몫 = 모름 (판독 오류 · 0 으로 안 그린다)")
    r_ep = run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "min_kink_at_endpoint": True, "dE_eV_per_atom": 0.0,
                                                      "reaction": "Li21AlP4S19Cl4O -> Li21AlP4S19Cl4O"}))
    ce = {x["species"]: x for x in r_ep["rows"]}["Al2O3"]
    chk(ce["H2S_share"] == 0.0 and abs(ce["delta_hyd_meV"] - 310.0) < 1e-6, "끝점 (반응 없음) → H₂S 몫 0 · δ = 0 − 호스트")
    chk(r0["gates"]["G7"]["overlap"] is not None and r0["gates"]["G7"]["n"] == 7, f"G7: 축 ① 과 Spearman ρ 를 공통 7 종에서 ({r0['gates']['G7']})")
    # 합치는 규칙
    cmb = ax_combine(NCM, r0)
    chk(set(cmb["axes_in_pareto"]) == ({"delta_NCM_LNO_half_meV", "delta_hyd_meV"} if r0["gates"]["G7"]["overlap"] is False else {"delta_NCM_LNO_half_meV"}),
        f"합치는 규칙 R3: G4 통과 · 안 겹친 축만 Pareto 에 ({cmb['axes_in_pareto']} · G7 {r0['gates']['G7']['rho_spearman']})")
    syn = {"blocking": [], "gates": {"G4": {"discriminates": True}, "G7": {"overlap": False}},
           "rows": [{"species": sp, "delta_hyd_meV": v, "F1_hyd": f1, "F2_H2S": False, "unknown": False} for sp, v, f1 in
                    (("Al2O3", 5.0, False), ("Al2S3", -30.0, True), ("Li2O", 20.0, False), ("Li2S", 0.0, False),
                     ("SnO2", 30.0, False), ("SnS2", 1.0, False), ("Ag2O", 40.0, False))]}
    c2 = ax_combine(NCM, syn)
    chk(c2["selection"] == ["SnO2"] and "Ag2O" not in c2["selection"] and "Al2S3" not in c2["selection"]
        and {r["species"]: r["flags"] for r in c2["rows"]}["Ag2O"] == ["축①F1_금속성"],
        f"합치는 규칙: 위험 표시 (Ag2O 금속성 · Al2S3 반응 · 가수분해 증가) 는 빼고 · 남은 것의 Pareto 비지배 = SnO2 하나 ({c2['selection']})")
    c3 = ax_combine({**NCM, "gates": {"G4": {"discriminates": False}}}, syn)
    c4 = ax_combine(NCM, {**syn, "gates": {"G4": {"discriminates": True}, "G7": {"overlap": True}}})
    chk(c3["selection"] is None and c4["selection"] is None and "R4" in c3["rule"] and c4["axes_in_pareto"] == ["delta_NCM_LNO_half_meV"],
        "⛔음성 합치는 규칙: 축 ① G4 불통과 · 축 ② 겹침 → 연속 축 하나 → R4 (표시만 · 고르지 않음)")
    print(f"axis_hyd selftest: ⭕ {n[0]} · ⛔ {n[1]}")
    return 0 if ok_all else 1



# ══════════════════════════════════════════════════════════════════════════════════════════════════
# 축 ③ Li 금속 음극 판독 — 카드 db/properties/cascade_axis_li_anode_estimand_2026_11_04.json (결정 D-2026-11-04-cascade-axis-li-anode)
#   실행:  python3 tools/cascade/analyze_cathode_reactivity.py --axis_li <run_dir> [--out <json>] [--ncm <축 ① 판독 json>] [--hyd <축 ② 판독 json>]
#   + 합치는 규칙 (ax_combine · 세 축 위험 표시 · G4 를 넘고 G7 안 겹친 연속 축만 Pareto)
#   ⛔ 이 판독기가 못 하는 것:
#     · 계산을 다시 하지 않는다 — designs_li.jsonl · host_li.jsonl · product_gaps.json · manifest.json 만 읽는다.
#     · '음이온 없는 금속간 (Li–M 합금 포함)' 의 음이온 = 축 ① 판독기의 비금속 · 준금속 목록 AX_NONMETAL (Si · Ge · As · Sb · Te 포함) —
#       그 원소가 든 Li 화합물 (Li3Sb · Li15Si4 …) 은 합금 규칙이 아니라 MP 갭으로 등급을 매긴다 (카드에 목록이 없어 판독기가 정했다 · 회수 전 커밋).
#     · 완전 환원 끝점 산물 (R3) 은 행에 kink 기록 ('kinks' · 러너 --record_kinks) 이 있을 때만 · 기록만 — 등급 · 게이트에 안 쓴다.
#     · 축 ② 와의 ρ 는 기록만 (축 ② 는 G4 불통과 · 카드 G7).
#     · MP 갭은 외부 PBE 값 · 순서용 · 도핑 격자 초과 에너지 · 계면 동역학 · SEI 성장 · 전자 터널링은 원래 계산에 없다.
# ══════════════════════════════════════════════════════════════════════════════════════════════════
LI_CARD = PROP / "cascade_axis_li_anode_estimand_2026_11_04.json"
LI_DECISION = "D-2026-11-04-cascade-axis-li-anode"
HYD_READOUT = PROP / "cascade_axis_hyd_readout_2026_11_04.json"
LIA = {"delta_meV": 10.0, "iqr_meV": 10.0, "rho_overlap": 0.8}
LI_CARD_TEXT = ("MP 갭 ≥ 2.0 eV", "0.1 ≤ MP 갭 < 2.0 eV", "MP 갭 < 0.1 eV", "≥ 1 %", "≥ 90 %", "> 10 %",
                "|δ_Li| ≥ 10 meV/atom", "IQR < 10", "|ρ| ≥ 0.8", "δ_Li ≤ −10 meV/atom", "Li2S · Li3P · LiCl")
LI_HOST_PRODUCTS = {"Li2S": {"Li": 2.0, "S": 1.0}, "Li3P": {"Li": 3.0, "P": 1.0}, "LiCl": {"Li": 1.0, "Cl": 1.0}}


def li_product_class(f, gaps):
    """축 ③ 산물 등급 (카드 §2 R2_산물_등급) — 원소 금속 · **음이온 없는 금속간 (Li–M 합금 포함)** 은 MP 갭 · +U 와 상관없이 금속성.
    나머지는 축 ① 규칙 그대로 (ax_product_class — +U · Cu 가 든 음이온 산물은 미판정 · 4f 하한 · MP 갭)."""
    el = _ax_pf(f)
    if el and not (set(el) & AX_NONMETAL):
        return "metallic", ("원소 금속" if len(el) == 1 else "음이온 없는 금속간 (합금)")
    return ax_product_class(f, gaps)


def li_rhs_products(rxn):
    """반응식 우변의 산물 화학식 목록 — 못 읽으면 None."""
    if not isinstance(rxn, str) or "->" not in rxn:
        return None
    try:
        return [f for _, f in parse_side(rxn.split("->", 1)[1])]
    except (ValueError, TypeError):
        return None


def _li_has(products, target):
    """산물 목록에 조성 비율이 target 과 같은 상이 있나 (원소 집합 · 비율 둘 다)."""
    want = _norm_comp(target)
    for f in products or []:
        try:
            c = _norm_comp(_ax_pf(f))
        except (ValueError, TypeError):
            continue
        if c and set(c) == set(want) and all(abs(c[k] - want[k]) <= 1e-6 for k in want):
            return True
    return False


def li_full_reduction(row):
    """R3 기록 — kink 기록이 있으면 끝점을 뺀 가장 작은 x (Li 쪽) 의 반응식 = 완전 환원 끝점. 기록이 없으면 None (못 봤다)."""
    ks = row.get("kinks") if isinstance(row, dict) else None
    if not isinstance(ks, list):
        return None
    inner = [k for k in ks if isinstance(k, dict) and isinstance(k.get("x"), (int, float)) and not isinstance(k.get("x"), bool)
             and 1e-6 < k["x"] < 1.0 - 1e-6 and isinstance(k.get("reaction"), str)]
    if not inner:
        return {"x": None, "reaction": None, "products": [], "why": "안쪽 kink 없음 (반응 없음)"}
    k = min(inner, key=lambda d: d["x"])
    return {"x": k["x"], "reaction": k["reaction"], "products": li_rhs_products(k["reaction"])}


def _li_decision():
    d = json.loads((ROOT / "db" / "governance" / "decisions.json").read_text(encoding="utf-8"))
    x = [y for y in d["decisions"] if y.get("id") == LI_DECISION]
    return (x[0].get("decision_state"), x[0].get("card")) if x else (None, None)


def li_load(run_dir):
    """ax_load (gaps · manifest) + 축 ③ 갈래 둘 — 못 읽은 줄은 problems 에 (조용히 버리지 않는다)."""
    L = ax_load(run_dir)
    for k in ("designs_li", "host_li"):
        p = Path(run_dir) / f"{k}.jsonl"
        if not p.is_file():
            L[k] = None
            continue
        rows = []
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
                if not isinstance(r, dict):
                    raise ValueError("행이 객체가 아니다")
                rows.append(r)
            except ValueError as e:
                L["problems"].append(f"{k}.jsonl {i} 번째 줄을 못 읽는다 ({type(e).__name__})")
        L[k] = rows
    return L


def li_gates(L, expected, card_text, decision_state, decision_card):
    """결정 · G1 · G1b · G2 · G3 · G5 (축 ③ 카드 §4) — G4 · G7 은 li_readout 이 δ_Li 를 낸 뒤 잰다."""
    G = {"decision": {"ok": decision_state == "active" and decision_card == "db/properties/" + LI_CARD.name,
                      "state": decision_state, "card": decision_card}}
    man = L.get("manifest") if isinstance(L.get("manifest"), dict) else {}
    miss = [k for k in AX_MANIFEST_KEYS if man.get(k) in (None, "", [], {})]
    invs = man.get("invocations") if isinstance(man.get("invocations"), list) and man.get("invocations") else [man]
    for t in AX_PHYS_TOOLS:
        v = {(x.get("tools_sha16") or {}).get(t) for x in invs if isinstance(x, dict)}
        if len(v) != 1 or None in v:
            miss.append(f"물리 도구 sha 가 실행마다 다르거나 없다 ({t})")
    G["G1"] = {"ok": not miss and not L["problems"], "missing": miss, "load_problems": L["problems"][:10]}
    vb, va = man.get("mp_db_version_before"), man.get("mp_db_version_after")
    G["G3"] = {"ok": man.get("same_mp_version") is True and vb not in (None, "") and vb == va, "before": vb, "after": va}
    ixd, ixh = ax_index(L.get("designs_li")), ax_index(L.get("host_li"))
    prob = [f"{nm} 없음" for nm, k in (("designs_li.jsonl", "designs_li"), ("host_li.jsonl", "host_li")) if L.get(k) is None]
    for sp in expected:
        rs = ixd.get((sp, "Li")) or []
        if len(rs) != 1 or not _ax_ok(rs[0]):
            prob.append(f"{sp} × Li: 행 {len(rs)} 개 · 정상 {sum(1 for r in rs if _ax_ok(r))}")
        elif rs[0].get("formula") != expected[sp]:
            prob.append(f"{sp} × Li: 조성 {rs[0].get('formula')} ≠ 카드 대상 {expected[sp]}")
    extra = sorted({k[0] for k in ixd} - set(expected))
    if extra:
        prob.append(f"카드에 없는 종 {extra[:5]}")
    h = _ax_one(ixh, ("HOST", "Li"))
    if h is None:
        prob.append("HOST × Li: 정상 행 하나가 아니다")
    if not (isinstance(L.get("gaps"), dict) and isinstance(L["gaps"].get("gaps"), dict)):
        prob.append("product_gaps.json 이 없거나 꼴이 아니다 (산물 갭 조회가 안 돌았다 — '갭 없음' 미판정과 다르다)")
    G["G2"] = {"ok": not prob, "n_problems": len(prob), "problems": prob[:20], "n_expected": len(expected)}
    g1b = {"ok": False, "why": "호스트 × Li 정상 행이 없다"}
    if h is not None:
        prods = li_rhs_products(h.get("reaction"))
        have = {k: _li_has(prods, v) for k, v in LI_HOST_PRODUCTS.items()}
        gaps = (L.get("gaps") or {}).get("gaps") if isinstance(L.get("gaps"), dict) else None
        g1b = {"ok": bool(h["dE_eV_per_atom"] < 0 and prods is not None and all(have.values())),
               "host_dE_negative": h["dE_eV_per_atom"] < 0, "host_products_have": have, "host_reaction": h.get("reaction"),
               "host_product_classes_기록만": {f: li_product_class(f, gaps or {})[0] for f in (prods or [])},
               "host_full_reduction_기록만": li_full_reduction(h)}
    G["G1b"] = g1b
    miss5 = [t for t in LI_CARD_TEXT if t not in (card_text or "")]
    G["G5"] = {"ok": not miss5, "missing_in_card": miss5, "card_sha256": hashlib.sha256((card_text or "").encode("utf-8")).hexdigest()}
    return G


def li_readout(run_dir, expected=None, card_text=None, decision=None, ncm=None, hyd=None):
    """카드 §2 · §4 대로 판독 — 막는 게이트 (결정 · G1 · G1b · G2 · G3 · G5) 가 하나라도 불통과면 표를 내지 않는다."""
    L = li_load(run_dir)
    expected = ax_roster() if expected is None else expected
    card_text = LI_CARD.read_text(encoding="utf-8") if card_text is None else card_text
    decision = _li_decision() if decision is None else decision
    G = li_gates(L, expected, card_text, *decision)
    blocking = [k for k in ("decision", "G1", "G1b", "G2", "G3", "G5") if not G[k]["ok"]]
    res = {"card": "db/properties/" + LI_CARD.name, "decision": LI_DECISION, "run_dir": str(run_dir), "constants": {**LIA, **{
               k: AX[k] for k in ("wide_eV", "metal_eV", "frac_metal", "frac_wide", "frac_und")}},
           "anion_elements_for_alloy_rule": sorted(AX_NONMETAL), "gates": G, "blocking": blocking,
           "⛔": "상대값 · 등급만 — 순위 · 거르기는 합치는 규칙대로 (R3 · R4) · MP 갭은 외부 PBE 값 (순서용)"}
    if blocking:
        res["⛔_표_없음"] = f"막는 게이트 불통과 {blocking} — 표를 내지 않는다 (카드 §4)"
        return res
    ixd, ixh = ax_index(L["designs_li"]), ax_index(L["host_li"])
    e_h = _ax_one(ixh, ("HOST", "Li"))["dE_eV_per_atom"] * 1000.0
    gaps = L["gaps"]["gaps"]
    rows = []
    for sp in sorted(expected):
        r = ixd[(sp, "Li")][0]
        d_ = r["dE_eV_per_atom"] * 1000.0 - e_h
        trk = ax_tracked(expected[sp], "Li")
        cls, det = ax_design_class(r, trk, gaps, classify=li_product_class)
        prods = li_rhs_products(r.get("reaction")) or []
        dop = [f for f in prods if set(_ax_pf(f)) & set(trk)]
        rows.append({"species": sp, "formula": expected[sp], "tracked": trk, "delta_Li_meV": round(d_, 2),
                     "differs_from_host": abs(d_) >= LIA["delta_meV"], "class": cls, "letter": AX_LETTER[cls], "fate": det,
                     "endpoint": r.get("min_kink_at_endpoint"), "reaction": r.get("reaction"),
                     "products_with_dopant": dop, "products_other": [f for f in prods if f not in dop],
                     "full_reduction_기록만": li_full_reduction(r),
                     "F1_Li": cls == "metallic", "F2_Li": d_ <= -LIA["delta_meV"],
                     "unknown": cls in ("undetermined", "na", "fate_error")})
    ds = [x["delta_Li_meV"] for x in rows]
    if len(ds) >= 4:
        q1, _, q3 = statistics.quantiles(ds, n=4, method="inclusive")
        G["G4"] = {"q1_meV": round(q1, 2), "q3_meV": round(q3, 2), "iqr_meV": round(q3 - q1, 2),
                   "discriminates": (q3 - q1) >= LIA["iqr_meV"], "method": "statistics.quantiles(n=4, method='inclusive')"}
    else:
        G["G4"] = {"iqr_meV": None, "discriminates": False, "why": "설계가 4 개 미만"}
    nc = ncm if ncm is not None else (json.loads(NCM_READOUT.read_text(encoding="utf-8")) if NCM_READOUT.is_file() else None)
    hy = hyd if hyd is not None else (json.loads(HYD_READOUT.read_text(encoding="utf-8")) if HYD_READOUT.is_file() else None)
    nd = {x["species"]: x for x in (nc or {}).get("rows", [])}
    hd = {x["species"]: x for x in (hy or {}).get("rows", [])}
    cn = [x for x in rows if x["species"] in nd]
    rho = _spearman([nd[x["species"]]["delta_LNO_half_meV"] for x in cn], [x["delta_Li_meV"] for x in cn])
    ch = [x for x in rows if x["species"] in hd]
    rho_h = _spearman([hd[x["species"]]["delta_hyd_meV"] for x in ch], [x["delta_Li_meV"] for x in ch])
    G["G7"] = {"rho_spearman": None if rho is None else round(rho, 4), "n": len(cn),
               "overlap": None if rho is None else abs(rho) >= LIA["rho_overlap"],
               "rho_vs_hyd_기록만": None if rho_h is None else round(rho_h, 4), "n_hyd": len(ch),
               "use": ("판정 불가 (축 ① 판독 없음)" if rho is None else
                       "겹침 — Pareto 에는 축 ① δ 만 · 축 ③ 은 위험 표시로만" if abs(rho) >= LIA["rho_overlap"] else
                       "안 겹침 — 두 축 다 Pareto 에 넣는다 (G4 통과 축만)")}
    by = {x["species"]: x for x in rows}
    pairs = []
    for o, s_ in AX_PAIRS:
        a, b = by.get(o), by.get(s_)
        if not (a and b):
            pairs.append({"oxide": o, "sulfide": s_, "missing": True})
            continue
        dd = a["delta_Li_meV"] - b["delta_Li_meV"]
        pairs.append({"oxide": o, "sulfide": s_, "delta_O_minus_S_meV": round(dd, 2), "class_O": a["class"], "class_S": b["class"],
                      "differs": bool(abs(dd) >= LIA["delta_meV"] or a["class"] != b["class"])})
    cnt = {}
    for x in rows:
        cnt[x["class"]] = cnt.get(x["class"], 0) + 1
    res.update({"rows": rows, "pairs_R5": pairs,
                "summary": {"n_designs": len(rows), "class": cnt, "n_differs_from_host": sum(x["differs_from_host"] for x in rows),
                            "n_F1_Li": sum(x["F1_Li"] for x in rows), "n_F2_Li": sum(x["F2_Li"] for x in rows),
                            "n_unknown": sum(x["unknown"] for x in rows), "n_fate_error": cnt.get("fate_error", 0),
                            "n_pairs_differ": sum(1 for p_ in pairs if p_.get("differs"))}})
    return res


def li_main(argv):
    i = argv.index("--axis_li")
    run_dir = argv[i + 1] if i + 1 < len(argv) else None
    if not run_dir:
        print("⛔ --axis_li <run_dir>")
        return 2
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else \
        PROP / f"cascade_axis_li_readout_{datetime.date.today().strftime('%Y_%m_%d')}.json"
    ncm_p = Path(argv[argv.index("--ncm") + 1]) if "--ncm" in argv else NCM_READOUT
    hyd_p = Path(argv[argv.index("--hyd") + 1]) if "--hyd" in argv else HYD_READOUT
    ncm = json.loads(ncm_p.read_text(encoding="utf-8")) if ncm_p.is_file() else None
    hyd = json.loads(hyd_p.read_text(encoding="utf-8")) if hyd_p.is_file() else None
    res = li_readout(run_dir, ncm=ncm, hyd=hyd)
    if not res["blocking"]:
        res["combination"] = (ax_combine(ncm, hyd, res) if ncm is not None and hyd is not None
                              else {"⛔": "축 ① · ② 판독 파일이 없다 — 합치지 않는다", "selection": None})
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k in ("decision", "G1", "G1b", "G2", "G3", "G5", "G4", "G7"):
        g = res["gates"].get(k)
        if g is not None:
            print(f"  {k:8s} {'⭕' if g.get('ok', g.get('discriminates', g.get('overlap') is False)) else '⛔'}  "
                  + json.dumps({x: y for x, y in g.items() if x not in ("problems", "load_problems", "host_reaction",
                                                                        "host_product_classes_기록만", "host_full_reduction_기록만")},
                               ensure_ascii=False)[:160])
    if res["blocking"]:
        print(f"⛔ 막는 게이트 불통과 {res['blocking']} — 표 없음 → {out}")
        return 2
    sm = res["summary"]
    with open(out.with_name(out.stem + "_designs.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# cascade 축 ③ Li 금속 음극 (카드 " + res["card"] + ") — δ_Li = 설계 − 호스트 [meV/atom · MP 닫힌계 · 상대값] · "
                 "class = 도펀트 행방 MP 갭 등급 (합금 · 원소 금속 = metallic)\n")
        w = csv.writer(fh)
        cols = ["species", "formula", "tracked", "delta_Li_meV", "differs_from_host", "class", "F1_Li", "F2_Li", "unknown",
                "products_with_dopant"]
        w.writerow(cols)
        for r in res["rows"]:
            w.writerow(["/".join(r[c]) if isinstance(r.get(c), list) else ("" if r.get(c) is None else r.get(c)) for c in cols])
    cmb = res.get("combination") or {}
    print(f"설계 {sm['n_designs']} · 호스트와 다름 {sm['n_differs_from_host']} · 등급 {sm['class']} · F1_Li {sm['n_F1_Li']} · "
          f"F2_Li {sm['n_F2_Li']} · 모름 {sm['n_unknown']} (판독 오류 {sm['n_fate_error']}) · 짝 다름 {sm['n_pairs_differ']}/{len(AX_PAIRS)}")
    print(f"합치는 규칙: {cmb.get('rule', cmb.get('⛔'))} · Pareto 축 {cmb.get('axes_in_pareto')} · 표시 {cmb.get('n_flagged')} · "
          f"선택 {None if cmb.get('selection') is None else len(cmb['selection'])}")
    print(f"→ {out}")
    return 0


def li_selftest():
    """축 ③ 판독기 + 세 축 합치기 — 양성 · 음성 경로."""
    import tempfile
    ok_all, n = True, [0, 0]
    def chk(c, msg):
        nonlocal ok_all
        n[0 if c else 1] += 1
        ok_all &= bool(c)
        print(("  ⭕ " if c else "  ⛔ ") + msg)
    card = LI_CARD.read_text(encoding="utf-8")
    FORM = {"Al2O3": "Li21AlP4S19Cl4O", "Al2S3": "Li21AlP4S20Cl4", "Li2O": "Li24P4S19Cl4O", "Li2S": "Li24P4S20Cl4",
            "SnO2": "Li22SnP4S19Cl4O2", "SnS2": "Li22SnP4S21Cl4", "Ag2O": "Li22Ag2P4S19Cl4O", "CuO": "Li22CuP4S19Cl4O",
            "Sb2S3": "Li21SbP4S21Cl4"}
    TAIL = " + 0.9 Li2S + 0.2 Li3P + 0.2 LiCl"
    RX = {"Al2O3": "0.05 LiAlO2", "Al2S3": "0.05 LiAl", "Li2O": "0.05 Li2O", "Li2S": "0.05 Li2S", "SnO2": "0.05 Li4SnS4",
          "SnS2": "0.0125 Li17Sn4", "Ag2O": "0.1 Ag", "CuO": "0.05 LiCuS", "Sb2S3": "0.05 Li3Sb"}
    DE = {"Al2O3": -0.480, "Al2S3": -0.530, "Li2O": -0.505, "Li2S": -0.500, "SnO2": -0.470, "SnS2": -0.475, "Ag2O": -0.520,
          "CuO": -0.488, "Sb2S3": -0.497}
    GAPS = {"LiAlO2": 4.5, "LiAl": 1.5, "Li4SnS4": 1.5, "Li3Sb": 0.7, "LiCuS": 1.2, "Li2S": 3.4, "Li3P": 0.7, "LiCl": 6.3}
    HOST_RX = "0.0769 Li6PS5Cl + 0.6154 Li -> 0.3846 Li2S + 0.0769 Li3P + 0.0769 LiCl"
    HOST_K = [{"x": 0.0, "dE_eV_per_atom": 0.0, "reaction": "Li -> Li"}, {"x": 0.2, "dE_eV_per_atom": -0.5, "reaction": HOST_RX},
              {"x": 0.6, "dE_eV_per_atom": -0.3, "reaction": "0.1 Li6PS5Cl + 0.2 Li -> 0.1 LiP + 0.5 Li2S + 0.1 LiCl"},
              {"x": 1.0, "dE_eV_per_atom": 0.0, "reaction": "Li6PS5Cl -> Li6PS5Cl"}]
    MAN = {"mp_db_version_before": "2026.09.28", "mp_db_version_after": "2026.09.28", "same_mp_version": True, "pymatgen": "x",
           "mp_api": "y", "thermo_types": ["GGA_GGA+U"], "correction_names_sample_Li-Ni-O": ["c"],
           "tools_sha16": {"a": "1", "b": "2", "c": "3"}, "repo_head": "f" * 40, "lanes": {"x": 1},
           "invocations": [{"tools_sha16": {AX_PHYS_TOOLS[0]: "1", AX_PHYS_TOOLS[1]: "2"}}]}
    def row(sp, de, rxn, form=None, **k):
        r = {"species": sp, "formula": form or FORM.get(sp, "Li6PS5Cl"), "cathode": "Li", "mode": "closed_0V",
             "dE_eV_per_atom": de, "reaction": rxn, "min_kink_at_endpoint": False}
        r.update(k)
        return r
    def build(td, mut=None):
        d = Path(td)
        D = {"des": [row(sp, DE[sp], f"0.05 {FORM[sp]} + 1.0 Li -> {RX[sp]}{TAIL}") for sp in FORM],
             "host": [row("HOST", -0.500, HOST_RX, form="Li6PS5Cl", kinks=HOST_K)],
             "gaps": {"gaps": {f: {"band_gap_MP_eV": g} for f, g in GAPS.items()}}}
        M_ = json.loads(json.dumps(MAN))
        if mut:
            mut(D, M_)
        (d / "designs_li.jsonl").write_text("".join(json.dumps(r) + "\n" for r in D["des"]), encoding="utf-8")
        (d / "host_li.jsonl").write_text("".join(json.dumps(r) + "\n" for r in D["host"]), encoding="utf-8")
        (d / "manifest.json").write_text(json.dumps(M_), encoding="utf-8")
        if D["gaps"] is not None:
            (d / "product_gaps.json").write_text(json.dumps(D["gaps"]), encoding="utf-8")
        return d
    NCM = {"blocking": [], "gates": {"G4": {"discriminates": True}},
           "rows": [{"species": sp, "delta_LNO_half_meV": v, "class_LNO_half": c} for sp, v, c in
                    (("Al2O3", 2.1, "wide"), ("Al2S3", -71.9, "wide"), ("Li2O", 11.4, "na"), ("Li2S", 0.0, "na"),
                     ("SnO2", 49.9, "intermediate"), ("SnS2", 27.2, "wide"), ("Ag2O", 30.0, "metallic"),
                     ("CuO", 5.0, "undetermined"), ("Sb2S3", -3.0, "intermediate"))]}
    HYD = {"blocking": [], "gates": {"G4": {"discriminates": False}, "G7": {"overlap": False}},
           "rows": [{"species": sp, "delta_hyd_meV": v, "F1_hyd": False, "F2_H2S": False, "unknown": False} for sp, v in
                    (("Al2O3", 1.0), ("Al2S3", -2.0), ("Li2O", 3.0), ("Li2S", 0.0), ("SnO2", 4.0), ("SnS2", -1.0),
                     ("Ag2O", 2.0), ("CuO", 0.5), ("Sb2S3", -0.5))]}
    def run(mut=None, card_text=card, decision=("active", "db/properties/" + LI_CARD.name), ncm=NCM, hyd=HYD):
        with tempfile.TemporaryDirectory() as td:
            return li_readout(build(td, mut), expected=dict(FORM), card_text=card_text, decision=decision, ncm=ncm, hyd=hyd)
    r0 = run()
    by = {x["species"]: x for x in r0.get("rows", [])}
    chk(not r0["blocking"] and abs(by["Al2S3"]["delta_Li_meV"] - (-30.0)) < 1e-6 and abs(by["SnO2"]["delta_Li_meV"] - 30.0) < 1e-6
        and r0["gates"]["G1b"]["host_products_have"] == {"Li2S": True, "Li3P": True, "LiCl": True},
        f"양성: 게이트 통과 · δ_Li = 설계 − 호스트 · 호스트 산물 Li2S · Li3P · LiCl ({ {k: v['delta_Li_meV'] for k, v in by.items()} })")
    want = {"Al2O3": "wide", "Al2S3": "metallic", "Li2O": "na", "Li2S": "na", "SnO2": "intermediate", "SnS2": "metallic",
            "Ag2O": "metallic", "CuO": "undetermined", "Sb2S3": "intermediate"}
    got = {k: v["class"] for k, v in by.items()}
    chk(got == want, f"R2 등급: 합금 LiAl (갭 1.5 이 있어도) · Li17Sn4 · 원소 Ag = 금속성 · 음이온 + Cu (LiCuS) = 미판정 · "
                     f"Li3Sb (Sb = 음이온 목록) 는 갭 0.7 → 중간 · LiAlO2 넓은 갭 · 추적 원소 없음 ㉧ ({got})")
    chk({k for k, v in by.items() if v["F1_Li"]} == {"Al2S3", "SnS2", "Ag2O"} and {k for k, v in by.items() if v["F2_Li"]} == {"Al2S3", "Ag2O"}
        and {k for k, v in by.items() if v["unknown"]} == {"CuO", "Li2O", "Li2S"},
        "위험 표시: F1_Li = 금속성 등급 · F2_Li = δ_Li ≤ −10 (Li2O −5 는 아님) · 모름 = 미판정 · 해당 없음")
    chk(by["Al2S3"]["products_with_dopant"] == ["LiAl"] and "Li3P" in by["Al2S3"]["products_other"]
        and by["Al2S3"]["full_reduction_기록만"] is None,
        "R3: 도펀트 든 산물 / 아닌 산물을 나눈다 · kink 기록이 없으면 완전 환원 끝점 = None (못 봤다)")
    fr = r0["gates"]["G1b"]["host_full_reduction_기록만"]
    chk(fr["x"] == 0.2 and fr["reaction"] == HOST_RX and "LiP" not in (fr["products"] or []),
        f"R3: kink 기록 → 끝점을 뺀 가장 작은 x (Li 쪽) = 완전 환원 끝점 (x 0.6 의 LiP 쪽이 아니다) ({fr})")
    chk(r0["gates"]["G4"]["discriminates"] is True and abs(r0["gates"]["G4"]["iqr_meV"] - 25.0) < 1e-6,
        f"G4: δ_Li IQR (inclusive 사분위) ≥ 10 → 갈린다 ({r0['gates']['G4']})")
    pr = {(p_["oxide"], p_["sulfide"]): p_ for p_ in r0["pairs_R5"]}
    chk(pr[("Al2O3", "Al2S3")]["differs"] and pr[("Li2O", "Li2S")]["differs"] is False and pr[("SnO2", "SnS2")]["differs"]
        and pr[("CaO", "CaS")].get("missing"),
        "R5: Al 짝 (δ 차 50) 다름 · Sn 짝 (δ 차 5 < 10 이지만 등급 중간 ↔ 금속성) 다름 · Li 짝 (δ 차 −5 · 둘 다 ㉧) 같음 · 없는 짝 missing")
    neg = {
        "host_positive": (run(lambda D, M_: D["host"].__setitem__(0, {**D["host"][0], "dE_eV_per_atom": 0.01})), "G1b"),
        "host_no_Li3P": (run(lambda D, M_: D["host"].__setitem__(0, {**D["host"][0], "reaction":
                         "0.1 Li6PS5Cl + 0.2 Li -> 0.1 LiP + 0.5 Li2S + 0.1 LiCl"})), "G1b"),
        "row_missing": (run(lambda D, M_: D["des"].pop(0)), "G2"),
        "row_other_formula": (run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "formula": "Li20AlP4S19Cl4O"})), "G2"),
        "row_open_mode": (run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "mode": "grand_potential"})), "G2"),
        "host_missing": (run(lambda D, M_: D["host"].pop(0)), "G2"),
        "gaps_missing": (run(lambda D, M_: D.__setitem__("gaps", None)), "G2"),
        "mp_moved": (run(lambda D, M_: M_.update(mp_db_version_after="2027.01.01")), "G3"),
        "manifest_head": (run(lambda D, M_: M_.pop("repo_head")), "G1"),
        "tool_drift": (run(lambda D, M_: M_["invocations"].append({"tools_sha16": {AX_PHYS_TOOLS[0]: "9", AX_PHYS_TOOLS[1]: "2"}})), "G1"),
        "decision_proposed": (run(decision=("proposed", "db/properties/" + LI_CARD.name)), "decision"),
        "card_changed": (run(card_text=card.replace("δ_Li ≤ −10 meV/atom", "δ_Li ≤ −20 meV/atom")), "G5"),
    }
    bad = {k: v[0]["blocking"] for k, v in neg.items() if v[1] not in v[0]["blocking"] or "rows" in v[0]}
    chk(not bad, f"⛔음성: 막는 게이트마다 깨면 표를 안 낸다 — 호스트 반응 양수 · 호스트 산물에 Li3P 없음 (LiP 는 아니다) · 행 빠짐 · "
                 f"다른 조성 · 열린계 행 · 호스트 행 없음 · 산물 갭 파일 없음 · MP 판 이동 · manifest · 도구 바뀜 · 결정 proposed · "
                 f"카드 문턱 변경 ({bad})")
    r_fe = run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "reaction": f"0.05 {FORM['Al2O3']} + 1.0 Li -> 0.02 LiAlO2{TAIL}"}))
    ce = {x["species"]: x for x in r_fe["rows"]}["Al2O3"]
    chk(ce["class"] == "fate_error" and ce["unknown"] and not ce["F1_Li"] and not r_fe["blocking"],
        "⛔음성: 추적 원소가 양변에서 안 맞으면 판독 오류 → 모름 (통과 · 표시로 둔갑하지 않는다)")
    r_ep = run(lambda D, M_: D["des"].__setitem__(0, {**D["des"][0], "min_kink_at_endpoint": True, "dE_eV_per_atom": 0.0,
                                                      "reaction": f"{FORM['Al2O3']} -> {FORM['Al2O3']}"}))
    cp = {x["species"]: x for x in r_ep["rows"]}["Al2O3"]
    chk(cp["class"] == "no_reaction" and cp["letter"] == "ⓔ" and abs(cp["delta_Li_meV"] - 500.0) < 1e-6 and not cp["unknown"],
        "끝점 (반응 없음) → ⓔ · δ = 0 − 호스트 · 모름 아님")
    r_flat = run(lambda D, M_: [x.update(dE_eV_per_atom=-0.500 + 0.001 * i) for i, x in enumerate(D["des"])])
    chk(r_flat["gates"]["G4"]["discriminates"] is False, f"⛔음성 G4: δ_Li 가 0–8 meV/atom 에 몰리면 IQR < 10 → 안 갈린다 ({r_flat['gates']['G4']})")
    ncm_rank = {x["species"]: x["delta_LNO_half_meV"] for x in NCM["rows"]}
    r_ov = run(lambda D, M_: [x.update(dE_eV_per_atom=-0.500 + ncm_rank[x["species"]] / 1000.0 / 3.0) for x in D["des"]])
    chk(r_ov["gates"]["G7"]["overlap"] is True and abs(r_ov["gates"]["G7"]["rho_spearman"] - 1.0) < 1e-9 and r_ov["gates"]["G7"]["n"] == 9,
        f"⛔음성 G7: δ_Li 순서가 축 ① 과 같으면 ρ = 1 → 겹침 ({r_ov['gates']['G7']})")
    chk(r0["gates"]["G7"]["overlap"] is False and r0["gates"]["G7"]["rho_vs_hyd_기록만"] is not None,
        f"G7: 축 ① 과 안 겹침 (ρ {r0['gates']['G7']['rho_spearman']}) · 축 ② ρ 는 기록만 ({r0['gates']['G7']['rho_vs_hyd_기록만']})")
    # 세 축 합치기
    syn = {"blocking": [], "gates": {"G4": {"discriminates": True}, "G7": {"overlap": False}},
           "rows": [{"species": sp, "delta_Li_meV": v, "F1_Li": f1, "F2_Li": v <= -10, "unknown": u} for sp, v, f1, u in
                    (("Al2O3", 40.0, False, False), ("Al2S3", -30.0, True, False), ("Li2O", -5.0, False, True), ("Li2S", 0.0, False, True),
                     ("SnO2", 30.0, False, False), ("SnS2", 5.0, True, False), ("Ag2O", -20.0, True, False), ("CuO", 12.0, False, True),
                     ("Sb2S3", 3.0, False, False))]}
    c3 = ax_combine(NCM, HYD, syn)
    fl = {r["species"]: r["flags"] for r in c3["rows"]}
    chk(c3["axes_in_pareto"] == ["delta_NCM_LNO_half_meV", "delta_Li_meV"] and c3["selection"] == ["Al2O3", "SnO2"]
        and "축③F1_Li금속성" in fl["SnS2"] and fl["Al2S3"] and {r["species"]: r["unknown"] for r in c3["rows"]}["CuO"] == ["축①R2", "축③R2"],
        f"합치기: 축 ① · ③ 이 G4 · G7 을 지나면 Pareto 두 축 · 세 축 위험 표시는 빼고 (SnS2 축 ③ 금속성) · 비지배 = Al2O3 · SnO2 ({c3['selection']})")
    c4 = ax_combine(NCM, HYD, {**syn, "gates": {"G4": {"discriminates": True}, "G7": {"overlap": True}}})
    c5 = ax_combine(NCM, HYD, {**syn, "gates": {"G4": {"discriminates": False}, "G7": {"overlap": False}}})
    chk(c4["selection"] is None and c5["selection"] is None and c4["axes_in_pareto"] == ["delta_NCM_LNO_half_meV"]
        and "R4" in c5["rule"] and "축③F1_Li금속성" in {r["species"]: r["flags"] for r in c4["rows"]}["SnS2"],
        "⛔음성 합치기: 축 ③ 겹침 · G4 불통과 → 연속 축 하나 → R4 (표시만) · 그래도 축 ③ 위험 표시는 붙는다")
    c6 = ax_combine(NCM, HYD, {**syn, "blocking": ["G1b"]})
    chk(c6["selection"] is None and "⛔" in c6, "⛔음성 합치기: 축 ③ 이 막는 게이트 불통과면 합치지 않는다")
    print(f"axis_li selftest: ⭕ {n[0]} · ⛔ {n[1]}")
    return 0 if ok_all else 1



# ══════════════════════════════════════════════════════════════════════════════════════════════════
# ⑤ +U 산물 사후 민감도 (2026-11-05 · 사용자 'V 산물 확인 카드' 선택 → 결과를 이미 본 뒤라 **사후 민감도** 로 기록)
#   실행:  python3 tools/cascade/analyze_cathode_reactivity.py --sens_plusU_gap [--out <json>]
#   한 규칙만 바꾼다: 축 ① · ③ 의 '+U 전이금속 · Cu 가 든 음이온 산물 = 미판정' 을 빼고 **같은 봉인 문턱** 으로 MP 갭 등급.
#   그 밖 (문턱 · 몫 규칙 · 합금 규칙 · 4f 하한 · 위험 표시 · Pareto) 은 그대로 · 모든 설계에 같이 (V 만 고르지 않는다).
#   ⛔ 이 민감도가 못 하는 것:
#     · 맹검이 아니다 — V12P7 · Li3VO4 등의 MP 갭은 회수 파일 (product_gaps.json) 에 이미 있었고 선택 뒤에 읽었다.
#     · MP 갭이 +U 산물에서 믿을 만한지는 말하지 않는다 — MP 는 산화물 · 불화물의 +U 원소에만 U 를 건다 (그 밖은 일반 GGA ·
#       'MP_U_적용_추정' 은 화학식에 O · F 가 있는지로만 어림한 것 · 엔트리의 실제 계산 설정을 확인하지 않았다) · 자성 바닥상태도 확인 안 했다.
#     · 봉인 판독 · 봉인 선택을 고치지 않는다 — 나란히 적는 기록이다. 봉인 판독을 같은 도구로 재현하지 못하면 아무것도 내지 않는다.
# ══════════════════════════════════════════════════════════════════════════════════════════════════
SENS_SEALED = {"ncm": PROP / "cascade_axis_ncm_readout_2026_11_04.json", "hyd": PROP / "cascade_axis_hyd_readout_2026_11_04.json",
               "li": PROP / "cascade_axis_li_readout_2026_11_05.json"}
SENS_OUT = PROP / "cascade_axes_plusU_gap_sensitivity_2026_11_05.json"
SENS_CMP = {"ncm": ("class_LNO_half", "delta_LNO_half_meV", "class_LCO_half", "fate_LNO_half"),
            "li": ("class", "delta_Li_meV", "F1_Li", "F2_Li", "unknown", "fate"),
            "comb": ("flags", "unknown", "pareto")}


def _sens_repro(sealed, mine, keys, tag):
    """봉인 판독 rows 와 지금 도구의 rows 가 같은가 — 다른 곳 목록 (빈 목록 = 재현)."""
    if not isinstance(sealed, dict) or not isinstance(sealed.get("rows"), list) or not isinstance(mine, dict) or not isinstance(mine.get("rows"), list):
        return [f"{tag}: rows 가 없다"]
    a = {r.get("species"): r for r in sealed["rows"]}
    b = {r.get("species"): r for r in mine["rows"]}
    out = [f"{tag}: 설계 목록이 다르다 ({sorted(set(a) ^ set(b))})"] if set(a) != set(b) else []
    out += [f"{tag}: {sp} {k} 봉인 {a[sp].get(k)!r} ≠ 지금 {b[sp].get(k)!r}" for sp in sorted(set(a) & set(b)) for k in keys
            if a[sp].get(k) != b[sp].get(k)]
    return out


def _sens_mp_u(formula):
    """MP 가 그 산물에 U 를 걸었을지 어림 — +U 원소 (Cu 제외) 가 있고 O · F 가 있으면 True (MP 혼합 규약의 문서 기준 · 엔트리 설정 확인 아님)."""
    el = set(_ax_pf(formula))
    return bool(el & (AX_TM_U - {"Cu"}) and el & {"O", "F"})


def _sens_changes(base, sens, ckey, fkey, gaps):
    """등급이 바뀐 설계 — 종 · 전 · 후 · 도펀트 산물 (MP id · 갭 · MP U 어림)."""
    a = {r["species"]: r for r in base["rows"]}
    out = []
    for r in sens["rows"]:
        b0 = a[r["species"]]
        if b0[ckey] == r[ckey]:
            continue
        prods = []
        for E, d in (r.get(fkey) or {}).items():
            for p_ in (d.get("products") or []) if isinstance(d, dict) else []:
                g = gaps.get(p_["product"]) if isinstance(gaps, dict) else None
                prods.append({"element": E, "product": p_["product"], "share": p_.get("share"), "class_after": p_.get("class"),
                              "basis_after": p_.get("basis"), "material_id": (g or {}).get("material_id"),
                              "band_gap_MP_eV": (g or {}).get("band_gap_MP_eV"), "MP_U_적용_추정": _sens_mp_u(p_["product"])})
        out.append({"species": r["species"], "before": b0[ckey], "after": r[ckey], "products": prods})
    return out


def sens_plusU(ncm_dir, li_dir, hyd, sealed_ncm, sealed_li, _ax=None, _li=None, _gaps=None):
    """사후 민감도 — 봉인 판독을 먼저 재현하고 (못 하면 ⛔ · 아무것도 안 냄) 그 다음 +U 규칙 하나만 바꿔 다시 판독 · 합치기.
    _ax · _li · _gaps 는 selftest 용 (기본 = 진짜 판독 함수 · 회수 파일의 갭). 스위치는 예외가 나도 끝에 False 로 되돌린다."""
    _ax = _ax or ax_readout
    _li = _li or li_readout
    AX_SENS["plusU_by_gap"] = False
    try:
        bn = _ax(ncm_dir)
        bl = _li(li_dir, ncm=bn, hyd=hyd)
        if bn.get("blocking") or bl.get("blocking"):
            return {"⛔": f"막는 게이트 불통과 (축 ① {bn.get('blocking')} · 축 ③ {bl.get('blocking')}) — 민감도를 내지 않는다"}
        bc = ax_combine(bn, hyd, bl)
        rep = (_sens_repro(sealed_ncm, bn, SENS_CMP["ncm"], "축 ①") + _sens_repro(sealed_li, bl, SENS_CMP["li"], "축 ③")
               + _sens_repro((sealed_li or {}).get("combination"), bc, SENS_CMP["comb"], "합치기"))
        if (sealed_li or {}).get("combination", {}).get("selection") != bc.get("selection"):
            rep.append(f"합치기: 선택 봉인 {(sealed_li or {}).get('combination', {}).get('selection')} ≠ 지금 {bc.get('selection')}")
        if rep:
            return {"⛔": "봉인 판독을 지금 도구로 재현하지 못했다 — 민감도를 내지 않는다", "problems": rep}
        AX_SENS["plusU_by_gap"] = True
        sn = _ax(ncm_dir)
        sl = _li(li_dir, ncm=sn, hyd=hyd)
        sc = ax_combine(sn, hyd, sl)
    finally:
        AX_SENS["plusU_by_gap"] = False
    g1 = _gaps["ncm"] if _gaps else ((ax_load(ncm_dir).get("gaps") or {}).get("gaps") or {})
    g3 = _gaps["li"] if _gaps else (li_load(li_dir)["gaps"]["gaps"])
    cb = {r["species"]: r for r in bc["rows"]}
    flag_ch = [{"species": r["species"], "flags_before": cb[r["species"]]["flags"], "flags_after": r["flags"],
                "unknown_before": cb[r["species"]]["unknown"], "unknown_after": r["unknown"]}
               for r in sc["rows"] if (r["flags"], r["unknown"]) != (cb[r["species"]]["flags"], cb[r["species"]]["unknown"])]
    return {"reproduced_sealed": True, "rule_changed": "축 ① · ③ '+U 전이금속 · Cu 가 든 음이온 산물 = 미판정' → 같은 봉인 문턱으로 MP 갭 등급",
            "thresholds_unchanged": {k: AX[k] for k in ("wide_eV", "metal_eV", "frac_metal", "frac_wide", "frac_und")},
            "axis1_class_changes": _sens_changes(bn, sn, "class_LNO_half", "fate_LNO_half", g1),
            "axis3_class_changes": _sens_changes(bl, sl, "class", "fate", g3),
            "flag_changes": flag_ch,
            "selection_sealed": bc["selection"], "selection_sensitivity": sc["selection"],
            "axes_in_pareto": sc.get("axes_in_pareto"), "rule": sc.get("rule"),
            "pareto_rows_sensitivity": [{k: r.get(k) for k in ("species", "unknown", *sc.get("axes_in_pareto", []))}
                                        for r in sc["rows"] if r.get("pareto")],
            "counts": {"axis1_class_sealed": bn["summary"]["class_LNO_half"], "axis1_class_sensitivity": sn["summary"]["class_LNO_half"],
                       "axis3_class_sealed": bl["summary"]["class"], "axis3_class_sensitivity": sl["summary"]["class"],
                       "n_flagged_sealed": bc.get("n_flagged"), "n_flagged_sensitivity": sc.get("n_flagged")}}


def _sens_out_refused(out):
    """봉인 판독 파일 (또는 '_readout_' 이름) 에는 민감도를 쓰지 않는다."""
    return "_readout_" in Path(out).name or Path(out).resolve() in {p.resolve() for p in SENS_SEALED.values()}


def sens_main(argv):
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else SENS_OUT
    if _sens_out_refused(out):
        print(f"⛔ --out {out} — 봉인 판독 파일 이름에는 쓰지 않는다 (민감도는 따로)")
        return 2
    sealed = {k: json.loads(p.read_text(encoding="utf-8")) for k, p in SENS_SEALED.items()}
    res = sens_plusU(sealed["ncm"]["run_dir"], sealed["li"]["run_dir"], sealed["hyd"], sealed["ncm"], sealed["li"])
    if "⛔" in res:
        print(res["⛔"]); [print("   ", x) for x in res.get("problems", [])[:20]]
        return 2
    res = {"kind": "post_hoc_sensitivity", "tool": "tools/cascade/analyze_cathode_reactivity.py --sens_plusU_gap",
           "sealed_readouts": {k: "db/properties/" + p.name for k, p in SENS_SEALED.items()}, **res}
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"봉인 재현 ⭕ · 축 ① 등급 바뀜 {len(res['axis1_class_changes'])} · 축 ③ 등급 바뀜 {len(res['axis3_class_changes'])} · "
          f"표시 바뀜 {len(res['flag_changes'])} · 선택 봉인 {res['selection_sealed']} → 민감도 {res['selection_sensitivity']}")
    print(f"→ {out}")
    return 0


def sens_selftest():
    """+U 사후 민감도 — 스위치 · 재현 검사 · 되돌림 · 봉인 파일 보호 (양성 · 음성)."""
    ok_all, n = True, [0, 0]
    def chk(c, msg):
        nonlocal ok_all
        n[0 if c else 1] += 1
        ok_all &= bool(c)
        print(("  ⭕ " if c else "  ⛔ ") + msg)
    G = {"V12P7": {"band_gap_MP_eV": 0.0, "material_id": "mp-1"}, "Li3VO4": {"band_gap_MP_eV": 4.034, "material_id": "mp-2"},
         "Cu2S": {"band_gap_MP_eV": 0.5}}
    chk([ax_product_class(f, G)[0] for f in ("V12P7", "Li3VO4", "Cu2S", "Mo3P")] == ["undetermined"] * 4,
        "기본 (봉인 판독): +U · Cu 산물은 MP 갭과 상관없이 미판정")
    AX_SENS["plusU_by_gap"] = True
    try:
        got = [ax_product_class(f, G)[0] for f in ("V12P7", "Li3VO4", "Cu2S", "Mo3P")]
        li_alloy = li_product_class("LiV2", G)[0]
    finally:
        AX_SENS["plusU_by_gap"] = False
    chk(got == ["metallic", "wide", "narrow", "undetermined"] and li_alloy == "metallic",
        f"스위치 켜면 같은 문턱으로 MP 갭 등급 (V12P7 0 → 금속성 · Li3VO4 4.034 → 넓음 · Cu2S 0.5 → 좁음 · 갭 없음 → 미판정 · 합금 규칙 그대로) {got}")
    chk(AX_SENS["plusU_by_gap"] is False and ax_product_class("V12P7", G)[0] == "undetermined", "⛔음성: 스위치는 끝나면 꺼진다")
    chk(_sens_mp_u("Li3VO4") and not _sens_mp_u("V12P7") and not _sens_mp_u("Cu2O") and _sens_mp_u("MoO2F2"),
        "MP U 어림: +U 원소 (Cu 제외) + O · F 일 때만")

    def mk_ncm(cls_v):
        return {"blocking": [], "gates": {"G4": {"discriminates": True}}, "summary": {"class_LNO_half": {}},
                "rows": [{"species": sp, "class_LNO_half": c, "delta_LNO_half_meV": d, "class_LCO_half": c, "fate_LNO_half": {}}
                         for sp, c, d in (("V2O5", cls_v, 100.0), ("SiO2", "intermediate", 30.0), ("Sb2O5", "intermediate", 90.0))]}

    def mk_li(cls_v):
        return {"blocking": [], "gates": {"G4": {"discriminates": True}, "G7": {"overlap": False}}, "summary": {"class": {}},
                "rows": [{"species": sp, "class": c, "delta_Li_meV": d, "F1_Li": c == "metallic", "F2_Li": d <= -10,
                          "unknown": c == "undetermined",
                          "fate": {"V": {"products": [{"product": "V12P7", "share": 1.0, "class": c}]}} if sp == "V2O5" else {}}
                         for sp, c, d in (("V2O5", cls_v, 150.0), ("SiO2", "intermediate", 80.0), ("Sb2O5", "intermediate", 70.0))]}
    HYD = {"blocking": [], "gates": {"G4": {"discriminates": False}, "G7": {"overlap": None}},
           "rows": [{"species": sp, "delta_hyd_meV": 0.0, "F1_hyd": False, "F2_H2S": False, "unknown": False} for sp in ("V2O5", "SiO2", "Sb2O5")]}
    fa = lambda d: mk_ncm("wide" if AX_SENS["plusU_by_gap"] else "undetermined")
    fl = lambda d, ncm=None, hyd=None: mk_li("metallic" if AX_SENS["plusU_by_gap"] else "undetermined")
    s_n, s_l = mk_ncm("undetermined"), mk_li("undetermined")
    s_l["combination"] = ax_combine(s_n, HYD, s_l)
    GG = {"ncm": {}, "li": G}
    r = sens_plusU("n", "l", HYD, s_n, s_l, _ax=fa, _li=fl, _gaps=GG)
    chk(r.get("reproduced_sealed") and r["selection_sealed"] == ["V2O5"] and r["selection_sensitivity"] == ["Sb2O5", "SiO2"]
        and [c["species"] for c in r["axis3_class_changes"]] == ["V2O5"] and r["axis3_class_changes"][0]["products"][0]["band_gap_MP_eV"] == 0.0
        and r["flag_changes"][0]["flags_after"] == ["축③F1_Li금속성"] and AX_SENS["plusU_by_gap"] is False,
        f"합성 계: V2O5 축 ③ 금속성 → 빠지고 선택 {r.get('selection_sensitivity')} · 봉인 {r.get('selection_sealed')} · 스위치 꺼짐")
    bad = mk_li("undetermined"); bad["rows"][1]["class"] = "wide"; bad["combination"] = s_l["combination"]
    r2 = sens_plusU("n", "l", HYD, s_n, bad, _ax=fa, _li=fl, _gaps=GG)
    chk("⛔" in r2 and any("SiO2 class" in x for x in r2["problems"]), "⛔음성: 봉인 판독과 지금 도구가 한 칸이라도 다르면 민감도를 내지 않는다")
    bad2 = {**s_l, "combination": {**s_l["combination"], "selection": ["SiO2"]}}
    r3 = sens_plusU("n", "l", HYD, s_n, bad2, _ax=fa, _li=fl, _gaps=GG)
    chk("⛔" in r3 and any("선택" in x for x in r3["problems"]), "⛔음성: 봉인 선택이 다르면 내지 않는다")

    fa_b = lambda d: {**mk_ncm("undetermined"), "blocking": ["G1"]}
    r4 = sens_plusU("n", "l", HYD, s_n, s_l, _ax=fa_b, _li=fl, _gaps=GG)
    chk("⛔" in r4 and "막는 게이트" in r4["⛔"] and "selection_sensitivity" not in r4,
        "⛔음성: 축 ① · ③ 중 막는 게이트 불통과가 있으면 민감도를 내지 않는다")

    def boom(d, ncm=None, hyd=None):
        if AX_SENS["plusU_by_gap"]:
            raise RuntimeError("selftest")
        return mk_li("undetermined")
    try:
        sens_plusU("n", "l", HYD, s_n, s_l, _ax=fa, _li=boom, _gaps=GG)
        raised = False
    except RuntimeError:
        raised = True
    chk(raised and AX_SENS["plusU_by_gap"] is False, "⛔음성: 민감도 판독 중 예외가 나도 스위치는 꺼진다 (봉인 판독이 켜진 채로 돌지 않는다)")
    import tempfile
    with tempfile.TemporaryDirectory() as td:                # ⚠ 진짜 봉인 경로로 sens_main 을 부르지 않는다 (거부가 깨지면 덮어쓴다)
        q_ = Path(td) / "cascade_axis_li_readout_2099_01_01.json"
        rc = sens_main(["x", "--out", str(q_)])
        made = q_.exists()
    chk(rc == 2 and not made and _sens_out_refused(SENS_SEALED["li"]) and _sens_out_refused(SENS_SEALED["ncm"])
        and _sens_out_refused(SENS_SEALED["hyd"]) and not _sens_out_refused(SENS_OUT),
        "⛔음성: 봉인 판독 파일 · '_readout_' 이름에는 쓰지 않는다 (rc 2 · 파일 안 생김 · 민감도 기본 경로는 허용)")
    print(f"sens_plusU selftest: ⭕ {n[0]} · ⛔ {n[1]}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(max(ax_selftest(), hy_selftest(), li_selftest(), sens_selftest()))
    if "--sens_plusU_gap" in sys.argv:
        raise SystemExit(sens_main(sys.argv))
    if "--axis_ncm" in sys.argv:
        raise SystemExit(ax_main(sys.argv))
    if "--axis_hyd" in sys.argv:
        raise SystemExit(hy_main(sys.argv))
    if "--axis_li" in sys.argv:
        raise SystemExit(li_main(sys.argv))
    main()
