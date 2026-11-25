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

5) ⭐ **묶음 2 판독** (2026-11-10 · 카드 cascade_axes_bundle2_estimand_2026_11_10.json · 결정 D-2026-11-10-cascade-axes-bundle2) —
   `--bundle2 <run_dir>` (AXIS=vol · win 출력) → 축 ④ ⑤ ⑥ · G1–G8 · R7–R13 (약점 순위 · Pareto 층 · 선택 · R12 기록) ·
   `--bundle1_repro` → 묶음 1 판독 · 합치기 (V2O5) · +U 민감도 (Sb2O5 · SiO2) 재현만. 못 하는 것은 그 절 머리 주석 (pymatgen 필요).
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


def ax_design_class(row, tracked, gaps, classify=None, extra_classes=()):
    """한 행 (설계 × 양극 상태) → (등급, 세부). 우선순위 ⓑ 금속성 > ⓐ 넓은 갭 > ⓓ 미판정 > ⓒ 중간 · ⓔ 끝점 · ㉧ 추적 원소 없음.
    classify = 산물 등급 함수 (기본 ax_product_class · 축 ③ 은 li_product_class — 음이온 없는 금속간 = 금속성).
    extra_classes = 산물 등급 이름을 더한다 (묶음 2 '휘발' — 그 몫은 넓은 갭 · 금속성 · 미판정 어디에도 안 들어가 우선순위 셈에서 빠진다).
    기본 () 이면 몫 사전 · 판정이 묶음 1 판과 같다 (봉인 판독 재현이 본다)."""
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
        sh = {"wide": 0.0, "narrow": 0.0, "metallic": 0.0, "undetermined": 0.0, **{k: 0.0 for k in extra_classes}}
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


# ══════════════════════════════════════════════════════════════════════════════════════════════════
# 묶음 2 판독 — 카드 db/properties/cascade_axes_bundle2_estimand_2026_11_10.json (결정 D-2026-11-10-cascade-axes-bundle2 · active)
#   실행:  python3 tools/cascade/analyze_cathode_reactivity.py --bundle2 <run_dir> [--out <json>]
#          python3 tools/cascade/analyze_cathode_reactivity.py --bundle1_repro   (묶음 1 판독 · 합치기 V2O5 · +U 민감도 재현만 · 상시 절차)
#   축 ④ 작동창 도펀트 행방 · ⑤ 분해 부피 변화 · ⑥ Li 쪽 산물 품질 (새 원자료) + 축 ① · ③ · 표시 ② (묶음 1 봉인 판독을 sha 로 결속 ·
#   다시 계산 · 다시 판정하지 않는다) → 게이트 G1 · G1b · G1c · G2 · G3 · G3b · G4 · G5 · G7 · G8 → R7–R13 (약점 순위 · Pareto 층 · 선택).
#   ⛔ 이 판독기가 못 하는 것:
#     · 계산 · MP 조회를 하지 않는다 — run_dir 의 designs_vol · host_vol · designs_win · host_win · product_gaps_vol · product_gaps_win ·
#       manifest 와 묶음 1 봉인 판독 · 원자료만 읽는다.
#     · pymatgen 없이 돌지 않는다 — 반응식 · 휘발 목록 · 기체 목록을 Composition 으로 대조한다 (카드 §2 · G1c · 문자열로 세지 않는다).
#     · ⑤ ⑥ 의 부피 회계는 부피 기록의 정확한 계수 (kink_terms · 같은 Reaction 객체) 로 한다 — 기록 문자열 (4 유효숫자) 은 반응 확인 ·
#       G3b · ④ 등급 (축 ① · ③ 과 같은 ax_fate 몫) 에만 쓴다. 정확한 계수가 없거나 문자열과 반올림 폭 밖이면 그 값은 내지 않는다.
#       G1c 원자 보존 = 문자열 1e-3 상대 (반올림) · 정확한 계수 1e-8 상대.
#     · ΔV/V 를 응력 · 균열 · 공극으로, φ_wide 를 부동태로, MP 갭 등급을 전자 전도도로, 순위를 '좋은 도펀트' 로 바꾸지 않는다 (카드 §5b).
#     · 동률 폭 · 방향 · 휘발 · 기체 목록 · 문턱은 카드에 봉인된 것만 쓴다 (G5 가 카드 본문 · 방향 표 · 목록과 대조) — 새 숫자 없음.
#     · 목록 밖 분자 결정 산물은 카드가 예로 든 넷 (PCl5 · AlCl3 · NbCl5 · I2) 만 '기록만' 표시 (판정에 안 쓴다 · 목록이 아니다).
#     · 모름 설계 · 표시 모름 설계는 순위 셈에 넣지 않고 끼워 넣은 구간만 적는다 (남의 순위를 밀지 않는다 · R10).
#     · R12 판은 주 판의 순위 축 집합을 그대로 두고 그 판이 바꾸는 것 하나만 바꾼다 (판마다 G4 · G7 · G8 을 다시 걸지 않는다 · 기록만).
# ══════════════════════════════════════════════════════════════════════════════════════════════════
B2_CARD = PROP / "cascade_axes_bundle2_estimand_2026_11_10.json"
B2_DECISION = "D-2026-11-10-cascade-axes-bundle2"
B2_CLOSURE = PROP / "cascade_axes_bundle_closed_2026_11_05.json"
#: 묶음 1 봉인 판독 — 마감 기록 (cascade_axes_bundle_closed_2026_11_05.json) 이 적은 sha16 으로 결속한다
B2_SEALED = {"ncm": (PROP / "cascade_axis_ncm_readout_2026_11_04.json", "6b84dbb3dbb55c39"),
             "hyd": (PROP / "cascade_axis_hyd_readout_2026_11_04.json", "510e00e6a8cfaa5a"),
             "li": (PROP / "cascade_axis_li_readout_2026_11_05.json", "c330f604eed85bdd"),
             "sens": (SENS_OUT, "c5bce8851f854e7b")}
B2_B1_RAW = {"ncm": ROOT / "db" / "raw" / "cascade_axis_ncm_v2_2026_11_04", "li": ROOT / "db" / "raw" / "cascade_axis_li_2026_11_04"}
B2_B1_REF = (("ncm", "designs_lno.jsonl"), ("ncm", "host.jsonl"), ("li", "designs_li.jsonl"), ("li", "host_li.jsonl"))
B2_V = (2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25)
B2_PARTNERS = {"LNO_half": "Li0.5NiO2", "LNO_full": "LiNiO2", "Li": "Li"}
#: G7 순서 (카드 §4 G7: ① → ③ → ⑤ NCM → ⑤ Li → ⑥ Li → ④)
B2_AXES = ("d_ncm", "d_li", "sv_ncm", "sv_li", "dphi_li", "f_ins")
B2_NEW = ("sv_ncm", "sv_li", "dphi_li", "f_ins")
B2_W = {"d_ncm": 10.0, "d_li": 10.0, "sv_ncm": 1.0, "sv_li": 1.0, "dphi_li": 0.01, "f_ins": 0.125}
#: ⭐ 방향 표 — 하나만 두고 R9 · R11 · G7 · G8 이 이것만 읽는다 (카드 합치는_규칙_묶음_2 방향_표 · G5 가 카드와 대조).
#:   *_signed 두 줄은 R12 '부호 있는 판' (Xin Li 해석 — 양의 분해 변형률이 낫다) 전용 · 카드 여섯 축이 아니다.
B2_DIR = {"d_ncm": "larger", "d_li": "larger", "sv_ncm": "smaller", "sv_li": "smaller", "dphi_li": "larger", "f_ins": "larger",
          "sv_ncm_signed": "larger", "sv_li_signed": "larger"}
B2_DIR_CARD = {"d_ncm": "축_①_δ_NCM", "d_li": "축_③_δ_Li", "sv_ncm": "축_⑤_s_V_NCM", "sv_li": "축_⑤_s_V_Li",
               "dphi_li": "축_⑥_δφ_wide_Li", "f_ins": "축_④_f_ins"}
B2_DIR_WORD = {"larger": "클수록", "smaller": "작을수록"}
#: 휘발 · 분자 산물 목록 (카드 §2 축 ④ 휘발_분자_산물_ED_P1_5 '목록 (결과 전 봉인)' 그대로 · G5 가 순서까지 대조) — Composition 으로 대조
B2_VOLATILE = ("O2", "N2", "Cl2", "Br2", "BrCl", "SO2", "SO3", "H2S", "PH3", "PF5", "PCl3", "POCl3", "SF4", "SF6", "S2Cl2", "SCl2",
               "SOCl2", "BF3", "BCl3", "SiF4", "SiCl4", "GeF4", "GeCl4", "SnCl4", "TiCl4", "VCl4", "AsCl3", "SbCl5", "MoF6", "WF6",
               "SO2Cl2", "PSCl3", "VOCl3", "CrO2Cl2")
#: ⑤ 기체 판 (카드 §2 축 ⑤ 회계 (iii)) — 반응식에 있으면 표시 · 그 부피 0 판은 기록만 · 상대 혼합에 끼면 부피 갈래를 읽지 않는다
B2_GAS = ("O2", "SO2", "SO3", "Cl2", "N2", "H2S", "PH3")
#: 목록 밖 분자 결정 (카드가 예로 든 넷 · '기록만' 표시 — 목록이 아니다 · 판정에 안 쓴다)
B2_MOLECULAR = ("PCl5", "AlCl3", "NbCl5", "I2")
B2_T = {"x": 1e-6, "dE_eV": 1e-5, "tie_dE_eV": 1e-5, "near_kink_eV": 0.010, "g1c": 1e-9, "phi_und": 0.01,
        "anchor_lo_pct": -30.0, "anchor_hi_pct": -10.0, "rho": 0.8, "top_n": 10}
B2_PHYS_TOOLS = ("tools/oxidation/interface_reactivity_v2.py", "tools/oxidation/esw_grand_potential.py", "tools/oxidation/sei_product_gaps.py")
B2_LANES = ("designs_vol", "host_vol", "designs_win", "host_win")
B2_FLAGS = ("축①F1_금속성", "축①F2_반응증가", "축②F1_가수분해증가", "축②F2_H2S증가", "축③F1_Li금속성", "축③F2_Li반응증가",
            "축④F_win_금속성")
#: G5 — 판독기 상수가 카드 본문과 같은지 (이 조각이 카드 문자열에 다 있어야 한다 · 방향 표 · 휘발 목록은 따로 구조로 대조)
B2_CARD_TEXT = ("w_④ = 1/8", "w_⑤ = 1 %p", "w_⑥ = 0.01", "w = 10 meV/atom (축 ① 카드의 '다르다' 문턱)",
                "w = 10 meV/atom (축 ③ 카드의 '다르다' 문턱)", "V = 2.50 · 2.75 · 3.00 · 3.25 · 3.50 · 3.75 · 4.00 · 4.25 V",
                "1 mV 안이면 V − 0.001 V 를 읽고 기록한다", "V_k ≤ V < V_{k+1}", "−30 % ~ −10 %", "φ_und > 0.01",
                "|Δx| ≤ 1e-6 · |ΔdE| ≤ 1e-5 eV/atom", "|ΔdE| ≤ 1e-5 eV/atom 인 kink", "10 meV/atom 안 kink",
                "statistics.quantiles(n=4, method='inclusive')", "ρ ≥ 0.8 만 겹침", "ρ ≤ −0.8 은 '상충'", "≥ 0.8 (G7 과 같은 수)",
                "|Δ| ≤ 1e-9", "{O2 · SO2 · SO3 · Cl2 · N2 · H2S · PH3}", "휘발 몫이 10 % 를 넘으면 그 점은 ⓐ 가 될 수 없다",
                "① → ③ → ⑤ NCM → ⑤ Li → ⑥ Li → ④", "비관 끝 = 모름 축 r = 1 + (줄의 설계 수)",
                "낙관 끝 = 모름 축 r = 1 · 표시 모름이면 무리 A", "표시 모름이면 무리 B", "한 축 이상에서 값이 그 축 동률 폭을 넘게 낫다",
                "문턱 2.0 eV · 0.1 eV · 1 % · 90 % · 10 %", "release onset (max μ | evolution < 0)", "IQR ≥ 그 축의 동률 폭",
                "새 연속 축이 하나도 순위에 못 들어가면 (G4 · G7 · G8) R10 · R11 을 내지 않는다", "같은 조성은 한 줄",
                "CaCl2 ≡ CaS · MgCl2 ≡ MgS", "reduced formula Li6PS5Cl 인 에너지 최저 엔트리",
                "f_ins = 8 점 중 설계 등급이 ⓐ 넓은 갭인 점의 비율", "R6c", "hull 원소에 Cl 이 없으면 원자 부피 판은 해당 없음")


def _b2_mod(name):
    """tools/oxidation 의 물리 도구 모듈 (반응식 파서 · G3b 대조기 · 구간 규칙 — 판독기가 따로 다시 쓰지 않는다)."""
    od = str(ROOT / "tools" / "oxidation")
    if od not in sys.path:
        sys.path.insert(0, od)
    import importlib
    return importlib.import_module(name)


def _b2_has_pm():
    try:
        import pymatgen.core  # noqa: F401
        return True
    except ImportError:
        return False


def _b2_key(f):
    """화학식 → 조성 열쇠 (pymatgen Composition 원자 분율 · interface_reactivity_v2.comp_key_pm)."""
    from pymatgen.core import Composition
    return _b2_mod("interface_reactivity_v2").comp_key_pm(Composition(f))


_B2_KS = {}


def b2_in_list(f, lst):
    """f 의 조성이 목록 lst (화학식들) 의 어느 조성과 같은가 — reduced Composition 대조 (S2Cl2 ≡ MP 'SCl' · 문자열 대조 아님)."""
    k = tuple(lst)
    if k not in _B2_KS:
        _B2_KS[k] = {_b2_key(x) for x in lst}
    try:
        return _b2_key(f) in _B2_KS[k]
    except Exception:
        return False


def b2_product_class(f, gaps):
    """묶음 2 산물 등급 (축 ④ · ⑥) — 휘발 목록이면 'volatile' (넓은 갭 몫에 안 넣는다) · 아니면 축 ③ 규칙 li_product_class 그대로."""
    if b2_in_list(f, B2_VOLATILE):
        return "volatile", "휘발 · 분자 산물 (상온 기체 · 액체 · 카드 목록)"
    return li_product_class(f, gaps)


def _b2_sides(row, rxn):
    """반응식 rxn 의 (좌변, 우변) [(계수, 화학식, Composition)] — 부피 기록의 **정확한 계수** (kink_terms · 같은 실행의 같은 Reaction 객체)
    를 기록 문자열과 대조해서 (interface_reactivity_v2.rxn_exact_sides). 4 유효숫자 문자열 계수로 회계하지 않는다 — 같은 반응도
    정규화가 다르면 반올림이 달라 Li2S ≡ 호스트 (G1c · |Δ| ≤ 1e-9) 가 깨진다. 기록이 없거나 문자열과 다르면 ValueError."""
    kt = (((row.get("volumes") or {}).get("kink_terms") or {}).get(rxn)) if isinstance(row, dict) else None
    if not isinstance(kt, dict) or not isinstance(kt.get("terms"), list):
        raise ValueError("이 반응식의 정확한 계수 기록 (volumes.kink_terms) 이 없다")
    return _b2_mod("interface_reactivity_v2").rxn_exact_sides(rxn, kt["terms"])


def _b2_argy_possible(f, cf):
    """설계 f · 상대 cf 의 hull 원소에 Li6PS5Cl 의 원소 (Li · P · S · Cl) 가 다 있는가 — 같은 hull 에 아지로다이트가 있을 수 있는가
    (카드 개정 2 · 2026-11-11). 판독기가 화학식에서 따로 판정한다 (기록기의 '해당 없음' 사유 문자열을 믿지 않는다)."""
    from pymatgen.core import Composition
    have = {e.symbol for e in Composition(f).elements} | {e.symbol for e in Composition(cf).elements}
    return {e.symbol for e in Composition("Li6PS5Cl").elements} <= have


def b2_argy_problem(f, cf, vol):
    """G2 — 아지로다이트 원자 부피 (⑤ 기록만 판) 의 꼴 (카드 개정 2). None = 정상 · 아니면 사유.
    원소가 다 있으면: 부피가 있어야 하고 '해당 없음' 이 없어야 한다 (예전과 같다 — MP 결손은 거부).
    원소가 모자라면 (Cl 을 F · Br 로 다 바꾼 설계): 아지로다이트 기록이 없어야 하고 '해당 없음' 사유가 있어야 한다 —
    그 설계의 원자 부피 판 ⑤ 는 모름 (주 판은 그대로 · G8 은 두 판이 다 있는 설계만)."""
    ag = vol.get("argyrodite_Li6PS5Cl")
    has_v = isinstance(ag, dict) and isinstance(ag.get("volume_per_atom_A3"), (int, float))
    na = vol.get("argyrodite_not_applicable")
    if _b2_argy_possible(f, cf):
        if not has_v:
            return "아지로다이트 원자 부피 없음"
        if na not in (None, ""):
            return "아지로다이트 원자 부피와 '해당 없음' 사유가 같이 있다"
        return None
    if ag is not None:
        return "hull 원소에 Cl 이 없는데 아지로다이트 기록이 있다"
    if not (isinstance(na, str) and na.strip()):
        return "아지로다이트 원자 부피 없음 (Cl 없는 설계인데 '해당 없음' 사유도 없다)"
    return None


def b2_dv(row, rxn=None, acc="hull"):
    """⑤ ΔV/V [%] = [V(산물) − V(반응물)] / V(반응물) — 그 반응식의 정확한 계수 (닫힌계 · 국소 x*). (값, 세부) | (None, 사유).
    acc 'hull' (주: 반응물 SE · 상대 = 같은 hull 의 평형 상 혼합 원자 부피) · 'atom' (기록만: SE = 아지로다이트 원자 부피) ·
    'gas0' (기록만: 기체 목록 산물 부피 0). 산물 부피 = 같은 hull 안정 엔트리 원자 부피 × 계수 × 원자 수."""
    vol = row.get("volumes") if isinstance(row, dict) else None
    if not (isinstance(vol, dict) and vol.get("ok") is True):
        return None, "부피 기록이 없거나 거부됐다"
    if acc == "atom" and not isinstance((vol.get("argyrodite_Li6PS5Cl") or {}).get("volume_per_atom_A3"), (int, float)):
        return None, "원자 부피 판 해당 없음 — " + str(vol.get("argyrodite_not_applicable") or "아지로다이트 원자 부피가 없다")
    ir = _b2_mod("interface_reactivity_v2")
    rxn = row.get("reaction") if rxn is None else rxn
    try:
        L, R = _b2_sides(row, rxn)
        k1, k2 = _b2_key(row["formula"]), _b2_key(row["cathode_formula"])
        rc = vol["reactants"]
        v1 = float(vol["argyrodite_Li6PS5Cl"]["volume_per_atom_A3"] if acc == "atom" else rc["c1"]["mixture_volume_per_atom_A3"])
        v2 = float(rc["c2"]["mixture_volume_per_atom_A3"])
    except (ValueError, KeyError, TypeError) as ex:
        return None, f"반응식 · 반응물 부피를 못 읽는다 ({type(ex).__name__}: {ex})"
    VR = VSE = 0.0
    for c, f, comp in L:
        k, n = ir.comp_key_pm(comp), c * float(comp.num_atoms)
        if k == k1:
            VR, VSE = VR + n * v1, VSE + n * v1
        elif k == k2:
            VR += n * v2
        else:
            return None, f"좌변 {f} 가 반응물 (SE · 상대) 이 아니다"
    pv, VP, gas = vol.get("products") or {}, 0.0, []
    for c, f, comp in R:
        p = pv.get(comp.reduced_formula) or pv.get(f)
        if not isinstance(p, dict) or not isinstance(p.get("volume_per_atom_A3"), (int, float)):
            return None, f"산물 {f} 의 부피가 없다"
        g = b2_in_list(f, B2_GAS)
        if g:
            gas.append(f)
        VP += c * float(comp.num_atoms) * (0.0 if (acc == "gas0" and g) else float(p["volume_per_atom_A3"]))
    if not VR > 0:
        return None, "반응물 부피가 0 이다"
    return 100.0 * (VP - VR) / VR, {"V_reactants_A3": VR, "V_products_A3": VP, "gas_products": gas,
                                     "dV_per_SE_pct_기록만": (100.0 * (VP - VR) / VSE) if VSE > 0 else None}


def b2_phi(row, rxn=None, gaps=None):
    """⑥ Li 쪽 산물 부피 분율 (카드 §2 축 ⑥ R6a · R6b · R6c) — 산물마다 등급 (b2_product_class · 추적 원소와 상관없이 모든 산물) ·
    부피 = 계수 × 원자 수 × 같은 hull 안정 엔트리 원자 부피. 휘발 산물은 분모에만 (φ_volatile). (사전, None) | (None, 사유)."""
    vol = row.get("volumes") if isinstance(row, dict) else None
    if not (isinstance(vol, dict) and vol.get("ok") is True):
        return None, "부피 기록이 없거나 거부됐다"
    try:
        _, R = _b2_sides(row, row.get("reaction") if rxn is None else rxn)
    except ValueError as ex:
        return None, f"반응식 · 정확한 계수를 못 읽는다 ({ex})"
    pv = vol.get("products") or {}
    V = {"wide": 0.0, "narrow": 0.0, "metallic": 0.0, "undetermined": 0.0, "volatile": 0.0}
    wh = wt = 0.0
    prods = []
    for c, f, comp in R:
        p = pv.get(comp.reduced_formula) or pv.get(f)
        if not isinstance(p, dict) or not isinstance(p.get("volume_per_atom_A3"), (int, float)):
            return None, f"산물 {f} 의 부피가 없다"
        v = c * float(comp.num_atoms) * float(p["volume_per_atom_A3"])
        cls, why = b2_product_class(f, gaps or {})
        V[cls] += v
        host_el = {e.symbol for e in comp.elements} <= AX_HOST_ELEMS
        if cls == "wide":
            if host_el:
                wh += v
            else:
                wt += v
        prods.append({"product": f, "class": cls, "basis": why, "volume_A3": v, "host_elements_only": host_el,
                      "material_id_hull": p.get("material_id"), "material_id_gap": ((gaps or {}).get(f) or {}).get("material_id")})
    tot = sum(V.values())
    if not tot > 0:
        return None, "산물 부피가 0 이다"
    out = {f"phi_{k}": V[k] / tot for k in V}
    out.update({"phi_wide_host_el": wh / tot, "phi_wide_tracked": wt / tot, "V_products_A3": tot, "products": prods})
    return out, None


def b2_kinks(row, q):
    """최소 kink 와 거의 겹치는 kink (|ΔdE| ≤ 1e-5 eV/atom · 카드 §2 축 ⑤ 거의_겹치는_kink) · 10 meV/atom 안 kink (R12) 에서 q(반응식) 값.
    ({min_index, tie: [(i, 값)], near: [(i, 값)]}, None) | (None, 사유). 최소 kink 는 (x · 반응식) 이 같은 kink 하나여야 한다."""
    ks = row.get("kinks") if isinstance(row, dict) else None
    if not isinstance(ks, list) or not ks:
        return None, "kink 기록이 없다"
    x0, d0, r0 = row.get("mixing_x"), row.get("dE_eV_per_atom"), row.get("reaction")
    try:
        hit = [i for i, k in enumerate(ks) if k.get("reaction") == r0 and abs(float(k["x"]) - float(x0)) <= B2_T["x"]]
    except (TypeError, ValueError, KeyError, AttributeError):
        return None, "kink 기록을 못 읽는다"
    if len(hit) != 1:
        return None, f"최소 kink 가 kink 목록에 {len(hit)} 번 있다 (하나여야 한다)"
    tie, near = [], []
    for i, k in enumerate(ks):
        dd = abs(float(k["dE_eV_per_atom"]) - float(d0))
        if dd <= B2_T["near_kink_eV"] + 1e-12:
            near.append((i, q(k["reaction"])))
        if i != hit[0] and dd <= B2_T["tie_dE_eV"] + 1e-12:
            tie.append((i, q(k["reaction"])))
    return {"min_index": hit[0], "tie": tie, "near": near}, None


def b2_row5(row, acc="hull"):
    """한 행 (설계 · 호스트 × 상대) 의 ⑤ — {dv, abs, value (= |ΔV/V| · 모름이면 None), why, n_tie, tie_spread, near_spread}.
    거의 겹치는 kink 의 |ΔV/V| 가 최소 kink 와 w_⑤ 를 넘게 다르면 그 행의 값은 모름 (카드 §2 · ED P2-1)."""
    dv, info = b2_dv(row, None, acc)
    if dv is None:
        return {"dv": None, "abs": None, "value": None, "why": info}
    kk, why = b2_kinks(row, lambda rx: b2_dv(row, rx, acc)[0])
    if kk is None:
        return {"dv": dv, "abs": abs(dv), "value": None, "why": why, **info}
    ta = [None if v is None else abs(v) for _, v in kk["tie"]]
    na = [abs(v) for _, v in kk["near"] if v is not None]
    out = {"dv": dv, "abs": abs(dv), "n_tie": len(ta), "n_near": len(kk["near"]),
           "tie_spread": max((abs(v - abs(dv)) for v in ta if v is not None), default=None),
           "near_spread_기록만": (max(na) - min(na)) if na else None, "n_near_unreadable": sum(1 for _, v in kk["near"] if v is None), **info}
    if any(v is None for v in ta):
        out.update(value=None, why="거의 겹치는 kink 의 ΔV/V 를 못 낸다")
    elif out["tie_spread"] is not None and out["tie_spread"] > B2_W["sv_ncm"]:
        out.update(value=None, why=f"거의 겹치는 kink (|ΔdE| ≤ 1e-5) 와 |ΔV/V| 차 {out['tie_spread']:.3f} %p > w_⑤")
    else:
        out.update(value=abs(dv), why=None)
    return out


def b2_row6(row, gaps):
    """한 행 (설계 · 호스트 × Li) 의 ⑥ — φ 들 + value (= φ_wide · 모름이면 None). φ_und > 0.01 이면 모름 (≤ 0.01 이면 미판정 산물은
    '넓은 갭 아님') · 거의 겹치는 kink 의 φ_wide 가 w_⑥ 를 넘게 다르거나 그 kink 의 φ_und > 0.01 이면 모름."""
    ph, why = b2_phi(row, None, gaps)
    if ph is None:
        return {"value": None, "why": why}
    out = dict(ph)
    if ph["phi_undetermined"] > B2_T["phi_und"]:
        out.update(value=None, why=f"미판정 산물 부피 분율 {ph['phi_undetermined']:.4f} > 0.01")
        return out
    kk, why = b2_kinks(row, lambda rx: b2_phi(row, rx, gaps)[0])
    if kk is None:
        out.update(value=None, why=why)
        return out
    tv = [v for _, v in kk["tie"]]
    nv = [v["phi_wide"] for _, v in kk["near"] if v is not None]
    out.update(n_tie=len(tv), near_spread_기록만=(max(nv) - min(nv)) if nv else None)
    if any(v is None or v["phi_undetermined"] > B2_T["phi_und"] for v in tv):
        out.update(value=None, why="거의 겹치는 kink 의 φ 를 정할 수 없다 (못 읽음 · 미판정 > 0.01)")
    elif tv and max(abs(v["phi_wide"] - ph["phi_wide"]) for v in tv) > B2_W["dphi_li"]:
        out.update(value=None, why="거의 겹치는 kink 와 φ_wide 차 > w_⑥")
    else:
        out.update(value=ph["phi_wide"], why=None)
    return out


def b2_win(row, formula, gaps):
    """④ 격자 전압 8 점 (카드 §2 축 ④ R4a–R4d) — ({'2.50': 점, …}, 요약). 점 = ax_design_class (축 ③ 산물 규칙 · 휘발 목록 ·
    같은 우선순위) · f_ins = ⓐ 점 비율 (한 점이라도 ⓓ · ㉧ · 판독 오류면 모름) · F_win = 어느 점이든 ⓑ (없고 ⓓ · 오류가 있으면 모름)."""
    trk = ax_tracked(formula, "WIN")
    pts = {}
    for V in B2_V:
        key = f"{V:.2f}"
        p = (row.get("by_voltage") or {}).get(key) or {}
        cls, det = ax_design_class({"reaction": p.get("reaction"), "min_kink_at_endpoint": False}, trk, gaps,
                                   classify=b2_product_class, extra_classes=("volatile",))
        lam = None
        if isinstance(p.get("li_released_per_fu"), (int, float)) and isinstance(row.get("n_atoms_fu"), (int, float)) and row["n_atoms_fu"] > 0:
            lam = p["li_released_per_fu"] / row["n_atoms_fu"]
        pts[key] = {"class": cls, "letter": AX_LETTER.get(cls), "fate": det,
                    "volatile_share": {E: d["shares"].get("volatile", 0.0) for E, d in det.items() if isinstance(d, dict) and "shares" in d},
                    "molecular_crystal_기록만": [f for f in (p.get("products") or []) if b2_in_list(f, B2_MOLECULAR)],
                    "lambda_Li_per_atom": lam, "products": p.get("products"), "V_read": p.get("V_read"), "shifted_1mV": p.get("shifted_1mV")}
    cl = [v["class"] for v in pts.values()]
    f_ins = None if any(c in ("undetermined", "na", "fate_error") for c in cl) else sum(c == "wide" for c in cl) / len(B2_V)
    F = True if "metallic" in cl else (None if any(c in ("undetermined", "fate_error") for c in cl) else False)
    return pts, {"tracked": trk, "f_ins": f_ins, "F_win": F, "n_wide": sum(c == "wide" for c in cl), "classes": cl,
                 "f_ins_why": None if f_ins is not None else "한 점 이상 ⓓ 미판정 · ㉧ 해당 없음 · 판독 오류 (R2 — 모름)",
                 "release_onset_V_기록만": row.get("release_onset_V")}


def b2_win_check(row):
    """④ 한 행의 교차 검사 (G1b_④) — 다른 곳 목록. ① 도구가 고른 줄을 profile 에서 구간 규칙 (esw interval_index) 으로 다시 고른다
    ② 그 줄 산물 = 기록 산물 ③ 기록 산물 = GrandPotentialPhaseDiagram 교차 산물 (Composition 열쇠) ④ 반응식 산물 = 기록 산물."""
    esw, ir = _b2_mod("esw_grand_potential"), _b2_mod("interface_reactivity_v2")
    prob = []
    prof = row.get("profile") or []
    try:
        vks = [float(s["V_vs_Li_exact"]) for s in prof]
    except (KeyError, TypeError, ValueError):
        return ["profile 에 V_vs_Li_exact 가 없다"]
    for V in B2_V:
        key = f"{V:.2f}"
        p = (row.get("by_voltage") or {}).get(key)
        if not isinstance(p, dict) or "error" in p:
            prob.append(f"{key} V 점이 없다 · 오류")
            continue
        k, vr, sh = esw.interval_index(vks, V)
        if k is None or k != p.get("row_index") or abs(vr - float(p.get("V_read", -1))) > 1e-9 or bool(sh) != bool(p.get("shifted_1mV")):
            prob.append(f"{key} V: 구간 규칙 줄 {k} ≠ 기록 {p.get('row_index')} (V_read · 1 mV 이동 포함)")
            continue
        try:
            ks = lambda fs: sorted(_b2_key(f) for f in fs if f != "Li")
            mine = ks(e["phase"] for e in prof[k].get("entries") or [])
            rec, gp = ks(p.get("products") or []), ks(p.get("gp_products") or [])
            _, R = ir.rxn_sides_pm(p.get("reaction"))
            rx = sorted(ir.comp_key_pm(c) for _, f, c in R if f != "Li")
        except Exception as ex:
            prob.append(f"{key} V: 산물 · 반응식을 못 읽는다 ({type(ex).__name__})")
            continue
        if mine != rec:
            prob.append(f"{key} V: 구간 줄 산물 ≠ 기록 산물")
        if rec != gp:
            prob.append(f"{key} V: 기록 산물 ≠ GrandPotentialPhaseDiagram 교차 산물")
        if rx != rec:
            prob.append(f"{key} V: 반응식 산물 ≠ 기록 산물")
    return prob


def _b2_jsonl(p, problems, tag):
    rows = []
    if not p.is_file():
        return None
    for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not ln.strip():
            continue
        try:
            r = json.loads(ln)
            if not isinstance(r, dict):
                raise ValueError("행이 객체가 아니다")
            rows.append(r)
        except ValueError as e:
            problems.append(f"{tag} {i} 번째 줄을 못 읽는다 ({type(e).__name__})")
    return rows


def b2_load(run_dir):
    """묶음 2 출력 폴더 → 네 갈래 행 · 산물 갭 둘 · manifest · problems (조용히 버리지 않는다)."""
    d, L = Path(run_dir), {"problems": []}
    for k in B2_LANES:
        L[k] = _b2_jsonl(d / f"{k}.jsonl", L["problems"], f"{k}.jsonl")
    for k, nm in (("gaps_win", "product_gaps_win.json"), ("gaps_vol", "product_gaps_vol.json"), ("manifest", "manifest.json")):
        p = d / nm
        try:
            L[k] = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None
        except ValueError as e:
            L[k] = None
            L["problems"].append(f"{nm} 를 못 읽는다 ({type(e).__name__})")
    return L


def b2_sealed(spec=None):
    """묶음 1 봉인 판독 넷 — sha16 결속 (마감 기록이 적은 값 · 그 기록 본문에도 같은 sha16 이 있어야 한다). ({이름: dict}, 문제 목록)."""
    spec = spec or B2_SEALED
    out, prob = {}, []
    clo = B2_CLOSURE.read_text(encoding="utf-8") if B2_CLOSURE.is_file() else ""
    for k, (p, sha) in spec.items():
        p = Path(p)
        if not p.is_file():
            prob.append(f"{k}: {p.name} 없음")
            continue
        got = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        if got != sha:
            prob.append(f"{k}: {p.name} sha16 {got} ≠ 봉인 {sha}")
        if spec is B2_SEALED and sha not in clo:
            prob.append(f"{k}: 봉인 sha16 {sha} 가 마감 기록에 없다")
        out[k] = json.loads(p.read_text(encoding="utf-8"))
    return out, prob


def b2_b1_ref():
    """G3b 원자료 (묶음 1 닫힌계 jsonl 넷) · G3 MP 판 (묶음 1 manifest 둘) — {rows, versions, problems}."""
    prob, rows, vers = [], [], set()
    for k, nm in B2_B1_REF:
        got = _b2_jsonl(B2_B1_RAW[k] / nm, prob, nm)
        if got is None:
            prob.append(f"{nm} 없음")
        rows += got or []
    for k, d in B2_B1_RAW.items():
        try:
            m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            prob.append(f"{k} manifest 를 못 읽는다")
            continue
        for x in (m.get("invocations") or [m]):
            vers |= {x.get("mp_db_version_before"), x.get("mp_db_version_after")}
    return {"rows": rows, "versions": sorted(v for v in vers if v is not None), "has_none": None in vers, "problems": prob}


def _b2_strip(d, path=()):
    if isinstance(d, dict):
        return {k: _b2_strip(v, path + (k,)) for k, v in d.items()
                if not (k == "run_dir" or (path[-2:] == ("gates", "G5") and k == "card_sha256"))}
    if isinstance(d, list):
        return [_b2_strip(x, path) for x in d]
    return d


def _b2_diff(a, b, p="", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append(f"{p}/{k}: 한쪽에만")
            else:
                _b2_diff(a[k], b[k], f"{p}/{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{p}: 길이 {len(a)} ≠ {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            _b2_diff(x, y, f"{p}[{i}]", out)
    elif a != b:
        out.append(f"{p}: 봉인 {a!r} ≠ 지금 {b!r}")
    return out


def b2_b1_repro(sealed):
    """묶음 1 재현 (CLAUDE.md 상시 절차 · 카드 §3b 판독기) — 지금 도구로 축 ① · ② · ③ 판독 · 합치기 · +U 사후 민감도를 원자료에서 다시 내서
    봉인 파일과 통째로 비교 (run_dir · G5 카드 sha 만 뺀다 — 카드 본문에 판독 기록이 뒤에 붙었다). {problems, selection, selection_sensitivity}."""
    rt = lambda x: json.loads(json.dumps(x, ensure_ascii=False))
    prob = []
    n = rt(ax_readout(ROOT / sealed["ncm"]["run_dir"]))
    h = hy_readout(ROOT / sealed["hyd"]["run_dir"], ncm=sealed["ncm"])
    h["combination"] = ax_combine(sealed["ncm"], h)
    l_ = li_readout(ROOT / sealed["li"]["run_dir"], ncm=sealed["ncm"], hyd=sealed["hyd"])
    l_["combination"] = ax_combine(sealed["ncm"], sealed["hyd"], l_)
    s_ = sens_plusU(ROOT / sealed["ncm"]["run_dir"], ROOT / sealed["li"]["run_dir"], sealed["hyd"], sealed["ncm"], sealed["li"])
    s_ = {"kind": "post_hoc_sensitivity", "tool": "tools/cascade/analyze_cathode_reactivity.py --sens_plusU_gap",
          "sealed_readouts": {k: "db/properties/" + p.name for k, p in SENS_SEALED.items()}, **s_}
    for tag, a, b in (("축 ①", sealed["ncm"], n), ("축 ②", sealed["hyd"], rt(h)), ("축 ③", sealed["li"], rt(l_)), ("+U 민감도", sealed["sens"], rt(s_))):
        d = _b2_diff(_b2_strip(a), _b2_strip(b))
        prob += [f"{tag} {x}" for x in d[:10]] + ([f"{tag}: 다른 곳 {len(d)}"] if len(d) > 10 else [])
    return {"problems": prob, "selection": rt(l_)["combination"].get("selection"), "selection_sensitivity": rt(s_).get("selection_sensitivity")}


def b2_b1_plusU(sealed):
    """R12 '+U 산물을 MP 갭으로 등급한 판' 의 축 ① · ③ 쪽 — 묶음 1 원자료를 같은 스위치로 다시 판독 (sens_plusU 와 같은 바꿈 · 스위치는 꼭 끈다)."""
    AX_SENS["plusU_by_gap"] = True
    try:
        n = ax_readout(ROOT / sealed["ncm"]["run_dir"])
        l_ = li_readout(ROOT / sealed["li"]["run_dir"], ncm=n, hyd=sealed["hyd"])
    finally:
        AX_SENS["plusU_by_gap"] = False
    return n, l_


def b2_flags(nr, hr, lr, F_win):
    """R8 — (확정 표시, 모름 표시). 묶음 1 여섯 (봉인 판독 그대로) + 축 ④ F_win. 모름 = ⓓ 미판정 · 판독 오류 때문에 정할 수 없는 표시
    (축 ① R2 · 축 ③ R2 · 축 ② H₂S 모름 · 축 ④ 의 점) · ㉧ 해당 없음은 F1 이 정의상 거짓 (모름 아님 · ED P1-3)."""
    fl, unk = [], []
    def put(name, v):
        (fl if v is True else unk if v is None else []).append(name)
    cn, cl = nr.get("class_LNO_half"), lr.get("class")
    put(B2_FLAGS[0], True if cn == "metallic" else (None if cn in ("undetermined", "fate_error") else False))
    put(B2_FLAGS[1], nr["delta_LNO_half_meV"] <= -AX["delta_meV"])
    put(B2_FLAGS[2], bool(hr.get("F1_hyd")))
    put(B2_FLAGS[3], True if hr.get("F2_H2S") else (None if hr.get("unknown") else False))
    put(B2_FLAGS[4], True if cl == "metallic" else (None if cl in ("undetermined", "fate_error") else False))
    put(B2_FLAGS[5], bool(lr.get("F2_Li")))
    put(B2_FLAGS[6], F_win)
    return fl, unk


# ── 순위 기계 (합치는_규칙_묶음_2 R9 · R10 · R11 · R13) — 방향 표 B2_DIR 하나만 읽는다 ─────────────────────────────────────
def b2_better(a, x, y, w):
    """축 a 에서 x 가 y 보다 동률 폭 w 를 **넘게** 낫다 (방향 = B2_DIR · R9 · R11 · G7 · G8 이 이 함수만 쓴다)."""
    return (x - y) > w if B2_DIR[a] == "larger" else (y - x) > w


def b2_aligned(a, v):
    """좋은 방향으로 맞춘 값 (클수록 좋게) — G7 · G8 의 Spearman ρ 는 이 값으로 낸다."""
    return v if B2_DIR[a] == "larger" else -v


def b2_ranks(line, axes, W):
    """R9 — 줄 안에서 r_a(i) = 1 + #{j : 축 a 에서 j 가 i 보다 w_a 를 넘게 낫다}. line = [(열쇠, {축: 값})]."""
    return {k: {a: 1 + sum(1 for _, v2 in line if b2_better(a, v2[a], v[a], W[a])) for a in axes} for k, v in line}


def b2_lex(rv):
    """leximin 비교 열쇠 — 순위 벡터를 나쁜 것 (큰 r) 부터 정렬 (작은 쪽이 앞)."""
    return tuple(sorted(rv.values(), reverse=True))


def b2_positions(lex):
    """동률은 같은 번호 · 다음 번호는 건너뛴다 (1, 2, 2, 4)."""
    return {k: 1 + sum(1 for l2 in lex.values() if l2 < l) for k, l in lex.items()}


def b2_dominates(rj, ri, vj, vi, axes, W):
    """R11 지배 — 모든 순위 축에서 r 이 크지 않고 · 한 축 이상에서 **값** 이 그 축 동률 폭을 넘게 낫다 (순위 벡터만 · ε-지배 아님)."""
    return all(rj[a] <= ri[a] for a in axes) and any(b2_better(a, vj[a], vi[a], W[a]) for a in axes)


def b2_layers(line, ranks, axes, W):
    """R11 비지배 정렬 — {열쇠: 층}. 순환이 생기면 (일어나면 안 된다 · 카드 증명) RuntimeError."""
    vals, left, layer, n = dict(line), [k for k, _ in line], {}, 0
    while left:
        n += 1
        front = [i for i in left if not any(b2_dominates(ranks[j], ranks[i], vals[j], vals[i], axes, W) for j in left if j != i)]
        if not front:
            raise RuntimeError("R11 지배에 순환이 있다 — 일어나면 안 된다 (판독기 결함)")
        for i in front:
            layer[i] = n
        left = [i for i in left if i not in front]
    return layer


def b2_weakest(rv):
    m = max(rv.values())
    return sorted(a for a, r in rv.items() if r == m)


def b2_insert(uv, line, ranks, layers, axes, W, mode):
    """모름 설계 u 를 줄 L 에 끼워 넣은 자리 (R10 · R11 구간 끝 · u 는 남의 r 을 세지 않는다).
    모름 축: 낙관 'opt' → r = 1 · 그 축에서 누구도 u 보다 낫지 않다 / 비관 'pess' → r = 1 + |L| · 누구나 u 보다 넘게 낫다."""
    n = len(line)
    ru = {a: ((1 if mode == "opt" else 1 + n) if uv.get(a) is None else
              1 + sum(1 for _, v in line if b2_better(a, v[a], uv[a], W[a]))) for a in axes}
    lu = b2_lex(ru)
    def bj(a, vj):
        return (mode == "pess") if uv.get(a) is None else b2_better(a, vj[a], uv[a], W[a])
    dom = [k for k, v in line if all(ranks[k][a] <= ru[a] for a in axes) and any(bj(a, v) for a in axes)]
    return {"r": ru, "weakest_axes": b2_weakest(ru), "position": 1 + sum(1 for k, _ in line if b2_lex(ranks[k]) < lu),
            "layer": 1 + max((layers[k] for k in dom), default=0)}


def b2_rank(rows, axes, W=None, vkey="values", top_n=None):
    """R10 약점 순위 · R11 Pareto 층 · R13 선택 — rows = 설계 기록 (comp_key · group 'A'|'B'|'?' · vkey 값 사전).
    줄 = 모든 순위 축에 값이 있고 표시가 확정된 설계 · 같은 조성은 한 줄 · 무리 A 줄 먼저 · 무리 B 줄은 같은 규칙으로 따로 (번호는 A 뒤).
    모름 설계 (축 모름 · 표시 모름 '?') 는 셈에 안 넣고 구간 (낙관 끝 · 비관 끝) 만 · 표시 모름 = 낙관 무리 A · 비관 무리 B."""
    W, top_n = dict(W or B2_W), top_n or B2_T["top_n"]
    units = {}
    for r in rows:
        u = units.setdefault(r["comp_key"], {"key": r["comp_key"], "species": [], "group": r["group"], "vals": {a: r[vkey].get(a) for a in axes}})
        u["species"].append(r["species"])
        if u["group"] != r["group"] or any(u["vals"][a] != r[vkey].get(a) for a in axes):
            raise ValueError(f"같은 조성 {u['species']} 의 무리 · 값이 다르다 (G1c 가 먼저 막아야 한다)")
    known = lambda u: all(u["vals"][a] is not None for a in axes)
    lines = {}
    for g in ("A", "B"):
        L = [(u["key"], u["vals"]) for u in units.values() if u["group"] == g and known(u)]
        rk = b2_ranks(L, axes, W)
        lines[g] = {"line": L, "ranks": rk, "pos": b2_positions({k: b2_lex(rk[k]) for k, _ in L}), "layers": b2_layers(L, rk, axes, W)}
    nA = len(lines["A"]["line"])
    per = {}
    for u in units.values():
        k = u["key"]
        if u["group"] in ("A", "B") and known(u):
            t = lines[u["group"]]
            per[k] = {"species": sorted(u["species"]), "group": u["group"], "in_line": True, "ranks": t["ranks"][k],
                      "weakest_axes": b2_weakest(t["ranks"][k]), "position_in_group": t["pos"][k],
                      "position": t["pos"][k] + (nA if u["group"] == "B" else 0), "pareto_layer": t["layers"][k]}
            continue
        go, gp = ("A" if u["group"] in ("A", "?") else "B"), ("B" if u["group"] in ("B", "?") else "A")
        io = b2_insert(u["vals"], lines[go]["line"], lines[go]["ranks"], lines[go]["layers"], axes, W, "opt")
        ip = b2_insert(u["vals"], lines[gp]["line"], lines[gp]["ranks"], lines[gp]["layers"], axes, W, "pess")
        per[k] = {"species": sorted(u["species"]), "group": u["group"], "in_line": False,
                  "unknown_axes": [a for a in axes if u["vals"][a] is None],
                  "interval": {"optimistic": {"group": go, "position": io["position"] + (nA if go == "B" else 0), "layer": io["layer"],
                                              "r": io["r"], "weakest_axes": io["weakest_axes"]},
                               "pessimistic": {"group": gp, "position": ip["position"] + (nA if gp == "B" else 0), "layer": ip["layer"],
                                               "r": ip["r"], "weakest_axes": ip["weakest_axes"]}}}
    A = lines["A"]
    sel = sorted(s for k, _ in A["line"] for s in per[k]["species"] if A["layers"][k] == 1)
    top = [k for k, _ in A["line"] if A["pos"][k] <= top_n]
    return {"axes": list(axes), "widths": {a: W[a] for a in axes}, "line_A_length": nA, "line_B_length": len(lines["B"]["line"]),
            "per": per, "selection": sel, "layer1_keys": sorted((k for k, _ in A["line"] if A["layers"][k] == 1), key=str),
            "top_keys": sorted(top, key=lambda k: (A["pos"][k], str(k))),
            "top": sorted((s for k in top for s in per[k]["species"]), key=lambda s: s),
            "top_share_of_line_pct": (100.0 * len(top) / nA) if nA else None,
            "dft_resolve_candidates": sorted(({"species": per[u["key"]]["species"], "interval": per[u["key"]]["interval"]}
                                              for u in units.values() if u["group"] == "?"), key=lambda d: d["species"])}


def b2_iqr(vals):
    if len(vals) < 4:
        return None
    q1, _, q3 = statistics.quantiles(vals, n=4, method="inclusive")
    return q3 - q1


def b2_g4(recs, a):
    """G4 — 91 설계 (값 있는 설계) 의 IQR ≥ 동률 폭이면 '갈린다' · 무리 A 안 IQR · 값마다 설계 수 (분포) 기록 (ED P1-2 라)."""
    v = [r["values"][a] for r in recs if r["values"][a] is not None]
    vA = [r["values"][a] for r in recs if r["values"][a] is not None and r["group"] == "A"]
    iqr, iqrA = b2_iqr(v), b2_iqr(vA)
    cnt = {}
    for x in v:
        cnt[round(x, 6)] = cnt.get(round(x, 6), 0) + 1
    return {"n": len(v), "iqr": iqr, "w": B2_W[a], "discriminates": iqr is not None and iqr >= B2_W[a],
            "iqr_group_A_기록만": iqrA, "n_group_A": len(vA), "distribution": [[x, c] for x, c in sorted(cnt.items())],
            "method": "statistics.quantiles(n=4, method='inclusive')"}


def b2_rho(recs, a, b, vkey_b="values", group=None):
    """좋은 방향으로 맞춘 Spearman ρ (G7 · G8) — 두 값이 다 있는 설계 · group 'A' 면 무리 A 안."""
    pr = [(b2_aligned(a, r["values"][a]), b2_aligned(b if vkey_b == "values" else a, r[vkey_b][b]))
          for r in recs if r["values"][a] is not None and r[vkey_b].get(b) is not None and (group is None or r["group"] == group)]
    rho = _spearman([x for x, _ in pr], [y for _, y in pr])
    return rho, len(pr)


def b2_g8(recs, a):
    """G8 (⑤ 회계 강건) — 91 설계에서 주 판 (hull 혼합) · 원자 부피 판 s_V 의 Spearman ρ (좋은 방향) ≥ 0.8 이면 통과 ·
    두 판에서 ⑤ r 이 달라지는 무리 A 설계 수 (같은 조성은 한 줄 · w_⑤)."""
    rho, n = b2_rho(recs, a, a, vkey_b="values_atom")
    A, seen = [], set()
    for r in recs:
        if r["group"] == "A" and r["values"][a] is not None and r["values_atom"].get(a) is not None and r["comp_key"] not in seen:
            seen.add(r["comp_key"])
            A.append(r)
    r1 = b2_ranks([(r["comp_key"], {a: r["values"][a]}) for r in A], (a,), B2_W)
    r2 = b2_ranks([(r["comp_key"], {a: r["values_atom"][a]}) for r in A], (a,), B2_W)
    return {"rho": rho, "n": n, "passes": rho is not None and rho >= B2_T["rho"],
            "n_group_A_rank_differs": sum(1 for r in A if r1[r["comp_key"]][a] != r2[r["comp_key"]][a]), "n_group_A": len(A),
            "n_main_only": sum(1 for r in recs if r["values"][a] is not None and r["values_atom"].get(a) is None)}


def _b2_decision():
    d = json.loads((ROOT / "db" / "governance" / "decisions.json").read_text(encoding="utf-8"))
    x = [y for y in d["decisions"] if y.get("id") == B2_DECISION]
    return (x[0].get("decision_state"), x[0].get("card")) if x else (None, None)


def b2_card_check(card_text):
    """G5 — 카드 본문 조각 · 방향 표 · 휘발 목록이 판독기 상수와 같은가 (결과를 보고 바꾸면 여기서 걸린다)."""
    miss = [t for t in B2_CARD_TEXT if t not in (card_text or "")]
    try:
        c = json.loads(card_text or "")
        dt = c["합치는_규칙_묶음_2"]["방향_표"]
        vl = c["2_그것을_재는_양"]["축_④_작동창_도펀트_행방"]["휘발_분자_산물_ED_P1_5"]["목록 (결과 전 봉인)"]
    except (ValueError, KeyError, TypeError):
        return {"ok": False, "missing_in_card": miss, "why": "카드 JSON 의 방향 표 · 휘발 목록을 못 읽는다"}
    bad_dir = [a for a, k in B2_DIR_CARD.items() if dt.get(k) != B2_DIR_WORD[B2_DIR[a]]]
    bad_vol = list(vl) != list(B2_VOLATILE)
    return {"ok": not miss and not bad_dir and not bad_vol, "missing_in_card": miss, "direction_mismatch": bad_dir,
            "volatile_list_mismatch": bad_vol, "card_sha256": hashlib.sha256((card_text or "").encode("utf-8")).hexdigest()}


def b2_gates_static(L, expected, card_text, decision, sealed, bind_prob, b1_ref, b1_repro):
    """값을 안 보는 게이트 — 결정 · B1 (봉인 결속 · 묶음 1 재현 · 표시 일치) · G1 · G2 · G3 · G3b · G5."""
    G = {"decision": {"ok": decision[0] == "active" and decision[1] == "db/properties/" + B2_CARD.name,
                      "state": decision[0], "card": decision[1]}}
    # B1 — 묶음 1 봉인 판독을 sha 로 결속 · 지금 판독기로 재현 · 봉인 합치기 표시 = 여기서 다시 읽은 표시
    fc = []
    try:
        nd, hd, ld = ({x["species"]: x for x in sealed[k]["rows"]} for k in ("ncm", "hyd", "li"))
        for c in (sealed["li"].get("combination") or {}).get("rows") or []:
            s_ = c["species"]
            fl, _ = b2_flags(nd[s_], hd[s_], ld[s_], False)
            if fl != list(c.get("flags") or []):
                fc.append(f"{s_}: 봉인 합치기 표시 {c.get('flags')} ≠ 다시 읽은 표시 {fl}")
        miss1 = sorted(set(expected) - (set(nd) & set(hd) & set(ld)))
        if miss1:
            fc.append(f"봉인 판독에 없는 설계 {miss1[:5]}")
        for k, g in (("ncm", "G4"), ("li", "G4")):
            if not sealed[k]["gates"].get(g, {}).get("discriminates"):
                fc.append(f"봉인 판독 {k} {g} 가 '갈린다' 가 아니다 (축 ① · ③ 이 순위 축이 될 수 없다)")
        if sealed["li"]["gates"].get("G7", {}).get("overlap") is not False:
            fc.append("봉인 축 ③ G7 이 '안 겹침' 이 아니다")
    except (KeyError, TypeError) as ex:
        fc.append(f"봉인 판독을 못 읽는다 ({type(ex).__name__}: {ex})")
    G["B1"] = {"ok": not bind_prob and not b1_repro["problems"] and not fc, "binding_problems": bind_prob,
               "reproduction_problems": b1_repro["problems"][:20], "flag_consistency_problems": fc[:20],
               "selection_bundle1": b1_repro.get("selection"), "selection_bundle1_plusU_sensitivity": b1_repro.get("selection_sensitivity")}
    # G1 — manifest · 실행 사이 물리 도구 sha 같음 · 두 갈래 (vol · win) 실행
    man = L.get("manifest") if isinstance(L.get("manifest"), dict) else {}
    miss = [k for k in AX_MANIFEST_KEYS if man.get(k) in (None, "", [], {})]
    invs = man.get("invocations") if isinstance(man.get("invocations"), list) and man.get("invocations") else []
    if not invs:
        miss.append("invocations")
    for t in B2_PHYS_TOOLS:
        v = {(x.get("tools_sha16") or {}).get(t) for x in invs if isinstance(x, dict)}
        if len(v) != 1 or None in v:
            miss.append(f"물리 도구 sha 가 실행마다 다르거나 없다 ({t})")
    axes_run = {x.get("axis") for x in invs if isinstance(x, dict)}
    if not {"vol", "win"} <= axes_run:
        miss.append(f"실행 기록에 vol · win 두 갈래가 다 없다 ({sorted(a for a in axes_run if a)})")
    lanes = man.get("lanes") if isinstance(man.get("lanes"), dict) else {}
    bad_l = [k for k in B2_LANES if not isinstance(lanes.get(k), dict) or lanes[k].get("rc") != 0]
    if bad_l:
        miss.append(f"갈래 rc ≠ 0 또는 없음 {bad_l}")
    G["G1"] = {"ok": not miss and not L["problems"], "missing": miss, "load_problems": L["problems"][:10], "n_invocations": len(invs)}
    # G3 — 모든 실행의 MP 판 = 묶음 1 원자료 판
    vs = {x.get(k) for x in invs if isinstance(x, dict) for k in ("mp_db_version_before", "mp_db_version_after")}
    ref = set(b1_ref["versions"])
    G["G3"] = {"ok": bool(vs) and None not in vs and len(ref) == 1 and not b1_ref["has_none"] and vs == ref
                     and man.get("same_mp_version") is True,
               "new_versions": sorted(v for v in vs if v), "bundle1_versions": sorted(ref)}
    # G2 — 완결성 (91 + 호스트 × 두 갈래 · 조성 · 부피 · 갭 열쇠)
    exp = dict(expected)
    exp["HOST"] = "Li6PS5Cl"
    prob = [f"{k}.jsonl 없음" for k in B2_LANES if L.get(k) is None]
    ixv = ax_index((L.get("designs_vol") or []) + (L.get("host_vol") or []))
    ixw = ax_index((L.get("designs_win") or []) + (L.get("host_win") or []))
    gv = (L.get("gaps_vol") or {}).get("gaps") if isinstance(L.get("gaps_vol"), dict) else None
    gw = (L.get("gaps_win") or {}).get("gaps") if isinstance(L.get("gaps_win"), dict) else None
    if not isinstance(gv, dict):
        prob.append("product_gaps_vol.json 이 없거나 꼴이 아니다 (Li 쪽 kink 산물 갭 조회가 안 돌았다)")
    if not isinstance(gw, dict):
        prob.append("product_gaps_win.json 이 없거나 꼴이 아니다 (창 산물 갭 조회가 안 돌았다)")
    ir = _b2_mod("interface_reactivity_v2")
    for sp, f in sorted(exp.items()):
        for cat, cf in B2_PARTNERS.items():
            rs = ixv.get((sp, cat)) or []
            if len(rs) != 1 or not _ax_ok(rs[0]):
                prob.append(f"{sp} × {cat}: 행 {len(rs)} 개 · 정상 {sum(1 for r in rs if _ax_ok(r))}")
                continue
            r = rs[0]
            if r.get("formula") != f or r.get("cathode_formula") != cf:
                prob.append(f"{sp} × {cat}: 조성 {r.get('formula')} · 상대 {r.get('cathode_formula')} ≠ 대상 {f} · {cf}")
            vol = r.get("volumes")
            if not (isinstance(vol, dict) and vol.get("ok") is True):
                prob.append(f"{sp} × {cat}: 부피 기록이 없거나 거부 ({(vol or {}).get('refused', ['없음'])[:2] if isinstance(vol, dict) else '없음'})")
                continue
            if not isinstance(r.get("kinks"), list) or not r["kinks"]:
                prob.append(f"{sp} × {cat}: kink 목록이 없다")
                continue
            try:
                ps = {c.reduced_formula for k in r["kinks"] for _, _, c in ir.rxn_sides_pm(k["reaction"])[1]}
                ps |= {c.reduced_formula for _, _, c in ir.rxn_sides_pm(r["reaction"])[1]}
                rk = {_b2_key(f), _b2_key(cf)}
                odd = sorted({ff for rx in [r["reaction"]] + [k["reaction"] for k in r["kinks"]]
                              for _, ff, c in ir.rxn_sides_pm(rx)[0] if ir.comp_key_pm(c) not in rk})
            except (ValueError, KeyError, TypeError):
                prob.append(f"{sp} × {cat}: kink 반응식을 못 읽는다")
                continue
            if odd:
                prob.append(f"{sp} × {cat}: 좌변에 반응물 (SE · 상대) 이 아닌 항 {odd[:3]}")
            nov = sorted(p for p in ps if p not in (vol.get("products") or {}))
            if nov:
                prob.append(f"{sp} × {cat}: 산물 구조 부피 없음 {nov[:4]}")
            kt = vol.get("kink_terms") if isinstance(vol.get("kink_terms"), dict) else {}
            not_t = [k.get("reaction") for k in r["kinks"] if k.get("reaction") not in kt] + ([] if r["reaction"] in kt else ["(최소 kink)"])
            if not_t:
                prob.append(f"{sp} × {cat}: 정확한 계수 기록 (kink_terms) 없는 반응식 {len(not_t)}")
            for t in ("c1", "c2"):
                if not isinstance(((vol.get("reactants") or {}).get(t) or {}).get("mixture_volume_per_atom_A3"), (int, float)):
                    prob.append(f"{sp} × {cat}: 반응물 {t} 부피 없음")
            ap = b2_argy_problem(f, cf, vol)
            if ap:
                prob.append(f"{sp} × {cat}: {ap}")
            if cat == "Li" and isinstance(gv, dict):
                nog = sorted(p for p in ps if p != "Li" and p not in gv)
                if nog:
                    prob.append(f"{sp} × Li: Li 쪽 산물 갭 조회 없음 {nog[:4]}")
        rs = ixw.get((sp, "WIN")) or []
        if len(rs) != 1 or "error" in rs[0] or rs[0].get("mode") != "grand_potential_window":
            prob.append(f"{sp} × 창: 정상 행 하나가 아니다 ({len(rs)})")
            continue
        r = rs[0]
        if r.get("formula") != f:
            prob.append(f"{sp} × 창: 조성 {r.get('formula')} ≠ 대상 {f}")
        bv = r.get("by_voltage") or {}
        for V in B2_V:
            p = bv.get(f"{V:.2f}")
            if not isinstance(p, dict) or "error" in p or not isinstance(p.get("reaction"), str):
                prob.append(f"{sp} × 창 {V:.2f} V: 점이 없다 · 오류")
                continue
            if isinstance(gw, dict):
                nog = sorted(x for x in (p.get("products") or []) if x != "Li" and x not in gw)
                if nog:
                    prob.append(f"{sp} × 창 {V:.2f} V: 산물 갭 조회 없음 {nog[:4]}")
    extra = sorted({k[0] for k in list(ixv) + list(ixw)} - set(exp))
    if extra:
        prob.append(f"카드에 없는 종 {extra[:5]}")
    G["G2"] = {"ok": not prob, "n_problems": len(prob), "problems": prob[:30], "n_expected": len(exp)}
    # G3b — 부피 갈래 최소 kink 반응식 · x* · dE = 묶음 1 원자료 (interface_reactivity_v2.closed_repro_compare)
    keys = [(sp, cat) for sp in exp for cat in B2_PARTNERS]
    g3b = ir.closed_repro_compare((L.get("designs_vol") or []) + (L.get("host_vol") or []), b1_ref["rows"],
                                  labels=tuple(B2_PARTNERS), expected=keys)
    G["G3b"] = {**g3b, "ok": bool(g3b["ok"]) and not b1_ref["problems"] and g3b["n_keys"] == len(exp) * len(B2_PARTNERS),
                "ref_problems": b1_ref["problems"][:5]}
    G["G5"] = b2_card_check(card_text)
    return G


def b2_design_values(L, expected, sealed, gaps_vol, gaps_win):
    """설계 · 호스트 기록 — ④ ⑤ ⑥ 값 (주 · 기록만 판) · 축 ① · ③ 봉인 값 · 표시 · 무리. G2 를 지난 뒤에만 부른다."""
    ixv = ax_index((L["designs_vol"] or []) + (L["host_vol"] or []))
    ixw = ax_index((L["designs_win"] or []) + (L["host_win"] or []))
    def five(sp):
        return {cat: {acc: b2_row5(ixv[(sp, cat)][0], acc) for acc in ("hull", "atom", "gas0")} for cat in B2_PARTNERS}
    host = {"w5": five("HOST"), "w6": b2_row6(ixv[("HOST", "Li")][0], gaps_vol)}
    hp, hs = b2_win(ixw[("HOST", "WIN")][0], "Li6PS5Cl", gaps_win)
    host.update(w4_points=hp, w4=hs, win_row=ixw[("HOST", "WIN")][0])
    nd, hd, ld = ({x["species"]: x for x in sealed[k]["rows"]} for k in ("ncm", "hyd", "li"))
    recs = []
    for sp in sorted(expected):
        f = expected[sp]
        w5 = five(sp)
        w6 = b2_row6(ixv[(sp, "Li")][0], gaps_vol)
        pts, w4 = b2_win(ixw[(sp, "WIN")][0], f, gaps_win)
        def sv(cat, acc, signed=False):
            a, b = w5[cat][acc], host["w5"][cat][acc]
            if a.get("value") is None or b.get("value") is None:
                return None
            return (a["dv"] - b["dv"]) if signed else (a["value"] - b["value"])
        dphi = None if (w6.get("value") is None or host["w6"].get("value") is None) else w6["value"] - host["w6"]["value"]
        fl, unk = b2_flags(nd[sp], hd[sp], ld[sp], w4["F_win"])
        wr = ixw[(sp, "WIN")][0]
        hr_ = host["win_row"]
        dl = {}
        for V in B2_V:
            a, b = pts[f"{V:.2f}"]["lambda_Li_per_atom"], hp[f"{V:.2f}"]["lambda_Li_per_atom"]
            dl[f"{V:.2f}"] = None if (a is None or b is None) else a - b
        on, onh = wr.get("release_onset_V"), hr_.get("release_onset_V")
        recs.append({
            "species": sp, "formula": f, "comp_key": _b2_key(f), "flags": fl, "flags_unknown": unk,
            "group": "B" if fl else ("?" if unk else "A"),
            "class_ncm_bundle1": nd[sp].get("class_LNO_half"), "class_li_bundle1": ld[sp].get("class"),
            "values": {"d_ncm": nd[sp]["delta_LNO_half_meV"], "d_li": ld[sp]["delta_Li_meV"], "sv_ncm": sv("LNO_half", "hull"),
                       "sv_li": sv("Li", "hull"), "dphi_li": dphi, "f_ins": w4["f_ins"],
                       "sv_ncm_signed": sv("LNO_half", "hull", True), "sv_li_signed": sv("Li", "hull", True)},
            "values_atom": {"sv_ncm": sv("LNO_half", "atom"), "sv_li": sv("Li", "atom")},
            "values_gas0": {"sv_ncm": sv("LNO_half", "gas0"), "sv_li": sv("Li", "gas0")},
            "record_only": {"sv_ncm_LNO_full_pp": sv("LNO_full", "hull"), "dphi_met_Li": (None if w6.get("phi_metallic") is None or
                            host["w6"].get("phi_metallic") is None else w6["phi_metallic"] - host["w6"]["phi_metallic"]),
                            "dphi_wide_host_el_Li": (None if dphi is None else w6["phi_wide_host_el"] - host["w6"]["phi_wide_host_el"]),
                            "dphi_wide_tracked_Li": (None if dphi is None else w6["phi_wide_tracked"] - host["w6"]["phi_wide_tracked"]),
                            "d_lambda_by_V": dl, "release_onset_shift_V": None if (on is None or onh is None) else on - onh,
                            "sv_near_spread_LNO_half_pp": w5["LNO_half"]["hull"].get("near_spread_기록만"),
                            "sv_near_spread_Li_pp": w5["Li"]["hull"].get("near_spread_기록만"),
                            "phi_near_spread_Li": w6.get("near_spread_기록만")},
            "w5": w5, "w6": w6, "w4": w4, "w4_points": pts})
    return host, recs


def b2_gates_values(L, expected, host, recs, sealed):
    """값을 쓰는 막는 게이트 — G1b (⑤ 앵커 · 상대 혼합 기체 · ④ 앵커 · 교차 · 구간 재현) · G1c (Li2S ≡ 호스트 · 같은 조성 · 원자 보존)."""
    ir = _b2_mod("interface_reactivity_v2")
    G = {}
    a5 = host["w5"]["Li"]["hull"]
    gas_p = []
    for r in (L["designs_vol"] or []) + (L["host_vol"] or []):
        dec = ((((r.get("volumes") or {}).get("reactants") or {}).get("c2") or {}).get("decomposition") or [])
        g = [d.get("phase") for d in dec if b2_in_list(d.get("phase", ""), B2_GAS)]
        if g:
            gas_p.append(f"{r.get('species')} × {r.get('cathode')}: {g}")
    ok5 = a5.get("dv") is not None and a5["dv"] < 0 and B2_T["anchor_lo_pct"] <= a5["dv"] <= B2_T["anchor_hi_pct"]
    hw, hp = host["win_row"], host["w4_points"]
    rel_all = all(isinstance(((hw.get("by_voltage") or {}).get(f"{V:.2f}") or {}).get("li_released_per_fu"), (int, float))
                  and hw["by_voltage"][f"{V:.2f}"]["li_released_per_fu"] > 1e-9 for V in B2_V)
    onset = hw.get("release_onset_V")
    licl = any(_b2_key(f) == _b2_key("LiCl") for f in (hp["2.50"]["products"] or []))
    xc = []
    for r in (L["designs_win"] or []) + (L["host_win"] or []):
        xc += [f"{r.get('species')}: {x}" for x in b2_win_check(r)]
    ok4 = rel_all and isinstance(onset, (int, float)) and onset < B2_V[0] and licl and not xc
    h425 = hp["4.25"]["products"] or []
    G["G1b"] = {"ok": bool(ok5 and not gas_p and ok4),
                "⑤_host_Li_dV_pct": a5.get("dv"), "⑤_anchor_window_pct": [B2_T["anchor_lo_pct"], B2_T["anchor_hi_pct"]], "⑤_ok": bool(ok5),
                "⑤_partner_mixture_gas": gas_p[:10],
                "④_host_releases_Li_all_8": rel_all, "④_host_release_onset_V": onset, "④_host_LiCl_at_2.50": licl,
                "④_crosscheck_problems": xc[:20], "④_n_crosscheck_problems": len(xc), "④_ok": bool(ok4),
                "기록만_host_4.25V_products": h425,
                "기록만_host_4.25V_has_Li_phase": any(any(e == "Li" for e, _ in _b2_key(f)) for f in h425),
                "기록만_host_LNO_half_dV_pct": host["w5"]["LNO_half"]["hull"].get("dv")}
    # G1c
    prob = []
    hk = _b2_key("Li6PS5Cl")
    same_h = [r for r in recs if r["comp_key"] == hk]
    if "Li2S" in expected and not any(r["species"] == "Li2S" for r in same_h):
        prob.append("Li2S 설계의 조성이 호스트 (Cl4Li24P4S20 ≡ Li6PS5Cl) 와 다르다")
    def num_eq(a, b):
        if a is None or b is None:
            return a is None and b is None
        return abs(a - b) <= B2_T["g1c"]
    for r in same_h:
        for cat in B2_PARTNERS:
            for acc in ("hull", "atom", "gas0"):
                if not num_eq(r["w5"][cat][acc].get("dv"), host["w5"][cat][acc].get("dv")):
                    prob.append(f"{r['species']} ≢ 호스트: ⑤ {cat} {acc}")
        for k in ("phi_wide", "phi_metallic", "phi_undetermined", "phi_volatile"):
            if not num_eq(r["w6"].get(k), host["w6"].get(k)):
                prob.append(f"{r['species']} ≢ 호스트: ⑥ {k}")
        for V in B2_V:
            a, b = r["w4_points"][f"{V:.2f}"], host["w4_points"][f"{V:.2f}"]
            if a["class"] != b["class"] or not num_eq(a["lambda_Li_per_atom"], b["lambda_Li_per_atom"]) \
                    or sorted(map(_b2_key, a["products"] or [])) != sorted(map(_b2_key, b["products"] or [])):
                prob.append(f"{r['species']} ≢ 호스트: ④ {V:.2f} V")
        if r["w4"]["f_ins"] != host["w4"]["f_ins"] or r["w4"]["F_win"] != host["w4"]["F_win"] \
                or not num_eq(r["w4"]["release_onset_V_기록만"], host["w4"]["release_onset_V_기록만"]):
            prob.append(f"{r['species']} ≢ 호스트: ④ f_ins · F_win · 개시")
    groups = {}
    for r in recs:
        groups.setdefault(r["comp_key"], []).append(r)
    nd, hd, ld = ({x["species"]: x for x in sealed[k]["rows"]} for k in ("ncm", "hyd", "li"))
    dup = []
    for ck, rs in groups.items():
        if len(rs) < 2:
            continue
        dup.append(sorted(r["species"] for r in rs))
        a = rs[0]
        for b in rs[1:]:
            for k in a["values"]:
                if not num_eq(a["values"][k], b["values"][k]):
                    prob.append(f"{a['species']} ≢ {b['species']}: {k}")
            for vk in ("values_atom", "values_gas0", "record_only"):
                if json.dumps(a[vk], sort_keys=True, default=str) != json.dumps(b[vk], sort_keys=True, default=str):
                    prob.append(f"{a['species']} ≢ {b['species']}: {vk}")
            if (a["flags"], a["flags_unknown"]) != (b["flags"], b["flags_unknown"]):
                prob.append(f"{a['species']} ≢ {b['species']}: 표시")
            if a["w4"]["classes"] != b["w4"]["classes"]:
                prob.append(f"{a['species']} ≢ {b['species']}: ④ 등급")
            for k_, dd in (("delta_LNO_half_meV", nd), ("delta_hyd_meV", hd), ("delta_Li_meV", ld)):
                if dd[a["species"]].get(k_) != dd[b["species"]].get(k_):
                    prob.append(f"{a['species']} ≢ {b['species']}: 묶음 1 {k_}")
    nb, worst, worst_x = 0, 0.0, 0.0
    for r in (L["designs_vol"] or []) + (L["host_vol"] or []):
        for rx in [r.get("reaction")] + [k.get("reaction") for k in r.get("kinks") or []]:
            ok_, w_, why = ir.rxn_balance_pm(rx)
            nb += 1
            worst = max(worst, w_ or 0.0)
            if not ok_:
                prob.append(f"{r.get('species')} × {r.get('cathode')}: 원자 보존 ({why})")
            try:
                Lx, Rx = _b2_sides(r, rx)
                el = {}
                for sgn, side in ((1.0, Lx), (-1.0, Rx)):
                    for c, _, comp in side:
                        for e, n_ in comp.items():
                            el.setdefault(e.symbol, [0.0, 0.0])[0 if sgn > 0 else 1] += c * float(n_)
                wx = max((abs(a - b) / max(abs(a), abs(b)) for a, b in el.values() if max(abs(a), abs(b)) > 0), default=0.0)
                worst_x = max(worst_x, wx)
                if wx > 1e-8:
                    prob.append(f"{r.get('species')} × {r.get('cathode')}: 정확한 계수 원자 보존 {wx:.2e} > 1e-8")
            except ValueError as ex:
                prob.append(f"{r.get('species')} × {r.get('cathode')}: 정확한 계수를 못 읽는다 ({ex})")
    for r in (L["designs_win"] or []) + (L["host_win"] or []):
        rxs = [v.get("reaction") for v in (r.get("by_voltage") or {}).values()] + [s.get("reaction") for s in r.get("profile") or []]
        for rx in rxs:
            ok_, w_, why = ir.rxn_balance_pm(rx)
            nb += 1
            worst = max(worst, w_ or 0.0)
            if not ok_:
                prob.append(f"{r.get('species')} × 창: 원자 보존 ({why})")
    G["G1c"] = {"ok": not prob, "problems": prob[:30], "n_problems": len(prob), "same_as_host": [r["species"] for r in same_h],
                "same_composition_groups": sorted(dup), "n_reactions_checked": nb, "worst_relative_imbalance_string": worst,
                "worst_relative_imbalance_exact": worst_x,
                "rule": "Li2S ≡ 호스트 · 같은 조성 설계 ≡ (모든 축) · 반응식 원자 보존 (pymatgen Composition · 문자열 1e-3 · 정확한 계수 1e-8 상대)"}
    return G


def b2_admission(recs, sealed):
    """R7 · G4 · G8 · G7 — 순서 (① → ③ → ⑤NCM → ⑤Li → ⑥Li → ④) 대로 새 축을 넣는다. (순위 축, 게이트 기록)."""
    adm = [a for a, k in (("d_ncm", "ncm"), ("d_li", "li")) if sealed[k]["gates"].get("G4", {}).get("discriminates")]
    G4, G7, G8 = {}, {"d_li_vs_d_ncm_bundle1": sealed["li"]["gates"].get("G7")}, {}
    for a in B2_NEW:
        G4[a] = b2_g4(recs, a)
        if a in ("sv_ncm", "sv_li"):
            G8[a] = b2_g8(recs, a)
        rh = {}
        for b in adm:
            rho, n = b2_rho(recs, a, b)
            rA, nA = b2_rho(recs, a, b, group="A")
            rh[b] = {"rho_aligned": rho, "n": n, "rho_aligned_group_A_기록만": rA, "n_group_A": nA,
                     "overlap": None if rho is None else rho >= B2_T["rho"], "conflict": None if rho is None else rho <= -B2_T["rho"]}
        ok = (G4[a]["discriminates"] and (a not in G8 or G8[a]["passes"]) and all(v["rho_aligned"] is not None for v in rh.values())
              and not any(v["overlap"] for v in rh.values()))
        G7[a] = {"vs_admitted": rh, "admitted": bool(ok), "conflicts": [b for b, v in rh.items() if v["conflict"]],
                 "why_not": None if ok else ("G4 — 못 가른다" if not G4[a]["discriminates"] else
                                             "G8 — 두 회계 판 순위가 다르다" if a in G8 and not G8[a]["passes"] else
                                             "G7 — 이미 들어간 축과 겹친다 (ρ ≥ 0.8)" if any(v["overlap"] for v in rh.values()) else "G7 — ρ 를 못 낸다")}
        if ok:
            adm.append(a)
    return adm, {"G4": G4, "G7": G7, "G8": G8}


def b2_r12(recs, axes, main, plus_u=None):
    """R12 강건성 (기록만) — 판마다 무리 A 상위 10 겹침 · 선택. 판은 순위 축 집합을 그대로 두고 그 판이 바꾸는 것 하나만 바꾼다."""
    top0 = set(main["top_keys"])
    def summ(r):
        return {"axes": r["axes"], "widths": r["widths"], "line_A_length": r["line_A_length"], "top": r["top"],
                "overlap_top_with_main": len(top0 & set(r["top_keys"])), "selection": r["selection"]}
    out = {"leave_one_axis_out": {a: summ(b2_rank(recs, [x for x in axes if x != a])) for a in axes},
           "all_widths_x0.5": summ(b2_rank(recs, axes, {a: B2_W[a] * 0.5 for a in axes})),
           "all_widths_x2": summ(b2_rank(recs, axes, {a: B2_W[a] * 2.0 for a in axes})),
           "one_width_at_a_time": {f"{a}_x{f}": summ(b2_rank(recs, axes, {**B2_W, a: B2_W[a] * f}))
                                   for a in axes if a in B2_NEW for f in (0.5, 2.0)},
           "pareto_layer1_vs_top": {"layer1": main["selection"], "top": main["top"],
                                    "overlap": len(set(main["layer1_keys"]) & top0)}}
    sv = [a for a in axes if a in ("sv_ncm", "sv_li")]
    if sv:
        sg_axes = [a + "_signed" if a in sv else a for a in axes]
        out["signed_dV_Xin_Li_기록만"] = summ(b2_rank(recs, sg_axes, {**B2_W, **{a + "_signed": B2_W[a] for a in sv}}))
        out["gas0"] = summ(b2_rank([{**r, "values": {**r["values"], **{a: r["values_gas0"][a] for a in sv}}} for r in recs], axes))
        out["atom_volume"] = summ(b2_rank([{**r, "values": {**r["values"], **{a: r["values_atom"][a] for a in sv}}} for r in recs], axes))
        out["atom_volume"]["n_designs_main_only"] = sum(1 for r in recs if any(r["values"][a] is not None and r["values_atom"].get(a) is None
                                                                                for a in sv))
    else:
        out["signed_dV_Xin_Li_기록만"] = out["gas0"] = out["atom_volume"] = {"why": "⑤ 가 순위 축이 아니다"}
    if plus_u is not None:
        out["plusU_by_gap"] = summ(b2_rank(plus_u, axes))
    return out


def b2_readout(run_dir, expected=None, card_text=None, decision=None, sealed=None, b1_ref=None, b1_repro=None, plus_u_b1=None):
    """카드 §2 · §4 · 합치는_규칙_묶음_2 대로 판독 — 막는 게이트 (결정 · B1 · G1 · G1b · G1c · G2 · G3 · G3b · G5) 하나라도 불통과면
    표를 내지 않는다 · 새 연속 축이 하나도 순위에 못 들면 (G4 · G7 · G8) R10 · R11 · R12 · R13 을 내지 않는다 (§9).
    expected · card_text · decision · sealed · b1_ref · b1_repro · plus_u_b1 는 selftest 용 (기본 = 저장소의 진짜 파일)."""
    res = {"card": "db/properties/" + B2_CARD.name, "decision": B2_DECISION, "run_dir": str(run_dir),
           "constants": {"widths": B2_W, "directions": {a: B2_DIR[a] for a in B2_AXES}, "voltages_V": list(B2_V),
                         "volatile_list": list(B2_VOLATILE), "gas_list": list(B2_GAS), "thresholds": B2_T},
           "⛔": "상대값 · 등급 · 순위 (줄 안 상대 위치) 만 — 순위는 DFT 확인 후보 목록이지 결론이 아니다 (R13) · MP 갭 · 부피는 외부 PBE 값"}
    if not _b2_has_pm():
        res.update(blocking=["pymatgen"], **{"⛔_표_없음": "pymatgen 이 없다 — Composition 대조 없이 판독하지 않는다"})
        return res
    L = b2_load(run_dir)
    expected = ax_roster() if expected is None else expected
    card_text = B2_CARD.read_text(encoding="utf-8") if card_text is None else card_text
    decision = _b2_decision() if decision is None else decision
    bind = []
    if sealed is None:
        sealed, bind = b2_sealed()
    b1_ref = b2_b1_ref() if b1_ref is None else b1_ref
    b1_repro = b2_b1_repro(sealed) if b1_repro is None else b1_repro
    G = b2_gates_static(L, expected, card_text, decision, sealed, bind, b1_ref, b1_repro)
    recs = host = None
    if G["G2"]["ok"]:
        gv, gw = L["gaps_vol"]["gaps"], L["gaps_win"]["gaps"]
        host, recs = b2_design_values(L, expected, sealed, gv, gw)
        G.update(b2_gates_values(L, expected, host, recs, sealed))
    else:
        G["G1b"] = G["G1c"] = {"ok": False, "why": "G2 불통과 — 값을 내지 않는다 (부분 판독 금지)"}
    res["gates"] = G
    res["blocking"] = [k for k in ("decision", "B1", "G1", "G1b", "G1c", "G2", "G3", "G3b", "G5") if not G[k]["ok"]]
    if res["blocking"]:
        res["⛔_표_없음"] = f"막는 게이트 불통과 {res['blocking']} — 판독하지 않는다 (멈춘다 · 닫는 것이 아니다 · 카드 §9)"
        return res
    adm, gg = b2_admission(recs, sealed)
    G.update(gg)
    new_in = [a for a in adm if a in B2_NEW]
    res["axes_ranking"] = adm
    res["host"] = {"w5": host["w5"], "w6": {k: v for k, v in host["w6"].items() if k != "products"}, "w4": host["w4"]}
    cnt = {"A": 0, "B": 0, "?": 0}
    for r in recs:
        cnt[r["group"]] += 1
    res["summary"] = {"n_designs": len(recs), "groups": cnt, "n_F_win": sum(1 for r in recs if B2_FLAGS[6] in r["flags"]),
                      "n_F_win_unknown": sum(1 for r in recs if B2_FLAGS[6] in r["flags_unknown"]), "new_axes_in_ranking": new_in}
    if not new_in:
        res["ranking"] = None
        res["⛔_순위_없음"] = "새 연속 축이 하나도 순위에 못 들었다 (G4 · G7 · G8) — R10 · R11 을 내지 않는다 (카드 §9 · 축 ① · ③ 만의 순위는 묶음 1 마감의 '⛔ 순위를 매겨 보려는 것')"
        res["rows"] = [{k: r[k] for k in ("species", "formula", "group", "flags", "flags_unknown", "values", "record_only")} for r in recs]
        return res
    main_ = b2_rank(recs, adm)
    pu = b2_plus_u_rows(L, sealed, recs, plus_u_b1)
    res["ranking"] = {k: v for k, v in main_.items() if k != "per"}
    res["R12"] = b2_r12(recs, adm, main_, pu)
    per = main_["per"]
    res["rows"] = []
    for r in recs:
        p = per[r["comp_key"]]
        res["rows"].append({**{k: r[k] for k in ("species", "formula", "group", "flags", "flags_unknown", "values", "values_atom",
                                                 "values_gas0", "record_only", "class_ncm_bundle1", "class_li_bundle1")},
                            "unknown_why": {a: w for a, w in (("sv_ncm", r["w5"]["LNO_half"]["hull"].get("why")), ("sv_li", r["w5"]["Li"]["hull"].get("why")),
                                                              ("dphi_li", r["w6"].get("why")), ("f_ins", r["w4"].get("f_ins_why"))) if w},
                            "same_composition_as": [s for s in p["species"] if s != r["species"]],
                            **{k: p.get(k) for k in ("in_line", "ranks", "weakest_axes", "position", "position_in_group", "pareto_layer",
                                                     "interval", "unknown_axes")},
                            "selected": r["species"] in main_["selection"], "top": r["species"] in main_["top"],
                            "w4": {k: v for k, v in r["w4"].items()}, "w4_points": {V: {k: v for k, v in pt.items() if k != "fate"}
                                                                                   for V, pt in r["w4_points"].items()},
                            "w5": r["w5"], "w6": {k: v for k, v in r["w6"].items()}})
    return res


def b2_plus_u_rows(L, sealed, recs, plus_u_b1=None):
    """R12 +U 판의 설계 기록 — 축 ① · ③ 표시 · 등급은 같은 스위치로 다시 읽은 묶음 1 (plus_u_b1 = (축 ① 판독, 축 ③ 판독)) ·
    ④ ⑥ 는 같은 스위치로 다시 등급 · 값 (⑤ · 축 ① · ③ δ 는 그대로). 스위치는 꼭 끈다."""
    if plus_u_b1 is None:
        plus_u_b1 = b2_b1_plusU(sealed)
    nU, lU = ({x["species"]: x for x in plus_u_b1[i]["rows"]} for i in (0, 1))
    hd = {x["species"]: x for x in sealed["hyd"]["rows"]}
    gv, gw = L["gaps_vol"]["gaps"], L["gaps_win"]["gaps"]
    ixv = ax_index((L["designs_vol"] or []) + (L["host_vol"] or []))
    ixw = ax_index((L["designs_win"] or []) + (L["host_win"] or []))
    AX_SENS["plusU_by_gap"] = True
    try:
        h6 = b2_row6(ixv[("HOST", "Li")][0], gv)
        out = []
        for r in recs:
            sp = r["species"]
            w6 = b2_row6(ixv[(sp, "Li")][0], gv)
            _, w4 = b2_win(ixw[(sp, "WIN")][0], r["formula"], gw)
            fl, unk = b2_flags(nU[sp], hd[sp], lU[sp], w4["F_win"])
            v = dict(r["values"])
            v["f_ins"] = w4["f_ins"]
            v["dphi_li"] = None if (w6.get("value") is None or h6.get("value") is None) else w6["value"] - h6["value"]
            out.append({"species": sp, "comp_key": r["comp_key"], "group": "B" if fl else ("?" if unk else "A"), "values": v})
    finally:
        AX_SENS["plusU_by_gap"] = False
    return out


def b2_write_csv(res, path):
    """Origin 용 CSV — 열 이름 명시 (상대값 · 등급 · 순위). 막는 게이트를 지난 판독에서만 부른다."""
    adm = res.get("axes_ranking") or []
    cols = ["species", "formula", "group", "flags", "flags_unknown", "delta_NCM_LNO_half_meV", "delta_Li_meV", "sV_NCM_LNO_half_pp",
            "sV_Li_pp", "dphi_wide_Li", "f_ins_window", "sV_NCM_LNO_full_pp_record", "dV_signed_NCM_LNO_half_pp_record",
            "dV_signed_Li_pp_record", "sV_NCM_atomvol_pp_record", "sV_Li_atomvol_pp_record", "dphi_met_Li_record",
            "dphi_wide_host_elements_Li_record", "dphi_wide_tracked_Li_record", "release_onset_shift_V_record",
            *[f"r_{a}" for a in adm], "weakest_axes", "leximin_position", "position_optimistic", "position_pessimistic",
            "pareto_layer", "layer_optimistic", "layer_pessimistic", "selected_layer1", "top10"]
    def g(r, c):
        v, ro, iv = r.get("values") or {}, r.get("record_only") or {}, (r.get("interval") or {})
        m = {"species": r["species"], "formula": r["formula"], "group": r["group"], "flags": "/".join(r["flags"]),
             "flags_unknown": "/".join(r["flags_unknown"]), "delta_NCM_LNO_half_meV": v.get("d_ncm"), "delta_Li_meV": v.get("d_li"),
             "sV_NCM_LNO_half_pp": v.get("sv_ncm"), "sV_Li_pp": v.get("sv_li"), "dphi_wide_Li": v.get("dphi_li"), "f_ins_window": v.get("f_ins"),
             "sV_NCM_LNO_full_pp_record": ro.get("sv_ncm_LNO_full_pp"), "dV_signed_NCM_LNO_half_pp_record": v.get("sv_ncm_signed"),
             "dV_signed_Li_pp_record": v.get("sv_li_signed"), "sV_NCM_atomvol_pp_record": (r.get("values_atom") or {}).get("sv_ncm"),
             "sV_Li_atomvol_pp_record": (r.get("values_atom") or {}).get("sv_li"), "dphi_met_Li_record": ro.get("dphi_met_Li"),
             "dphi_wide_host_elements_Li_record": ro.get("dphi_wide_host_el_Li"), "dphi_wide_tracked_Li_record": ro.get("dphi_wide_tracked_Li"),
             "release_onset_shift_V_record": ro.get("release_onset_shift_V"), "weakest_axes": "/".join(r.get("weakest_axes") or []),
             "leximin_position": r.get("position"), "position_optimistic": (iv.get("optimistic") or {}).get("position"),
             "position_pessimistic": (iv.get("pessimistic") or {}).get("position"), "pareto_layer": r.get("pareto_layer"),
             "layer_optimistic": (iv.get("optimistic") or {}).get("layer"), "layer_pessimistic": (iv.get("pessimistic") or {}).get("layer"),
             "selected_layer1": r.get("selected"), "top10": r.get("top")}
        for a in adm:
            m[f"r_{a}"] = (r.get("ranks") or {}).get(a)
        x = m.get(c)
        return "" if x is None else x
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("# cascade 묶음 2 (카드 " + res["card"] + ") — 상대값 · 등급 · 순위 (줄 안 상대 위치 · 결론 아님) · "
                 "delta = 설계 − 호스트 · sV = |ΔV/V| 설계 − 호스트 [%p] · dphi = φ_wide 설계 − 호스트 · f_ins = 창 8 점 중 ⓐ 비율 · "
                 "순위 축 " + "/".join(adm) + " · 무리 A 줄 먼저\n")
        w = csv.writer(fh)
        w.writerow(cols)
        for r in res["rows"]:
            w.writerow([g(r, c) for c in cols])


def _b2_out_refused(out):
    """묶음 1 봉인 판독 · 민감도 파일에는 쓰지 않는다."""
    o = Path(out).resolve()
    return o in {p.resolve() for p, _ in B2_SEALED.values()} or "bundle2" not in Path(out).name


def b2_main(argv):
    i = argv.index("--bundle2")
    run_dir = argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else None
    if not run_dir:
        print("⛔ --bundle2 <run_dir>")
        return 2
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else \
        PROP / f"cascade_axes_bundle2_readout_{datetime.date.today().strftime('%Y_%m_%d')}.json"
    if _b2_out_refused(out):
        print(f"⛔ --out {out} — 묶음 1 봉인 파일 · 'bundle2' 가 없는 이름에는 쓰지 않는다")
        return 2
    res = b2_readout(run_dir)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    for k in ("decision", "B1", "G1", "G1b", "G1c", "G2", "G3", "G3b", "G5"):
        g = (res.get("gates") or {}).get(k)
        if g is not None:
            print(f"  {k:8s} {'⭕' if g.get('ok') else '⛔'}  " + json.dumps(
                {x: y for x, y in g.items() if x not in ("problems", "load_problems", "failures", "④_crosscheck_problems")},
                ensure_ascii=False, default=str)[:160])
    if res.get("blocking"):
        print(f"⛔ 막는 게이트 불통과 {res['blocking']} — 표 없음 → {out}")
        return 2
    b2_write_csv(res, out.with_name(out.stem + "_designs.csv"))
    sm = res["summary"]
    rk = res.get("ranking")
    print(f"설계 {sm['n_designs']} · 무리 {sm['groups']} · F_win {sm['n_F_win']} (모름 {sm['n_F_win_unknown']}) · 순위 축 {res['axes_ranking']}")
    print("순위: " + ("없음 — 새 연속 축 0 개 (§9)" if rk is None else
                     f"줄 A {rk['line_A_length']} · 선택 (층 1) {len(rk['selection'])} · 상위 {len(rk['top'])} ({rk['top_share_of_line_pct']:.0f} % of 줄)"))
    print(f"→ {out} · {out.with_name(out.stem + '_designs.csv')}")
    return 0


#: selftest 용 가상 묶음 2 세계 (지어낸 수 · MP 아님) — 종: (조성, Li 쪽 도펀트 산물, LNO 쪽 도펀트 산물, 창 세 띠의 도펀트 산물)
_B2S_D = {
    "Li2S": ("Cl4Li24P4S20", [], [], ([], [], [])),
    "CaCl2": ("Cl4Li22P4S20Ca1", ["CaS"], ["CaSO4"], (["CaS"], ["CaCl2"], ["CaCl2"])),
    "CaS": ("Cl4Li22P4S20Ca1", ["CaS"], ["CaSO4"], (["CaS"], ["CaCl2"], ["CaCl2"])),
    "MgO": ("Li22MgP4S19Cl4O", ["MgS"], ["MgSO4"], (["MgS"], ["MgCl2"], ["MgCl2"])),
    "Al2O3": ("Li21AlP4S19Cl4O", ["LiAl"], ["LiAlO2"], (["LiAlS2"], ["AlCl3"], ["AlCl3"])),
    "SiO2": ("Li20SiP4S18Cl4O2", ["Li15Si4"], ["SiO2"], (["SiS2"], ["SiS2"], ["SiCl4"])),
    "LiF": ("Li24P4S20Cl3F", ["LiF"], ["LiF"], (["LiF"], ["LiF"], ["PF5"])),
    "BaO": ("Li22BaP4S19Cl4O", ["BaS"], ["BaSO4"], (["BaS"], ["BaCl2"], ["BaCl2"])),
    "ZnO": ("Li22ZnP4S19Cl4O", ["LiZn"], ["ZnS"], (["ZnS"], ["ZnS"], ["ZnCl2"])),
    "V2O5": ("Li19VP4S19Cl4O2", ["V"], ["LiVO2"], (["VS4"], ["VS4"], ["VS4"])),
    "Ag2O": ("Li22Ag2P4S19Cl4O", ["Ag"], ["Ag2S"], (["Ag"], ["Ag2S"], ["AgCl"])),
    "SnO2": ("Li22SnP4S19Cl4O2", ["Li17Sn4"], ["SnO2"], (["SnS2"], ["SnS2"], ["SnCl4"])),
    "GeS2": ("Li20GeP4S20Cl4", ["Li15Ge4"], ["GeO2"], (["GeS2"], ["GeS2"], ["GeS2"])),
    "NaCl": ("Cl4Li22Na2P4S20", ["Na2S"], ["Na2SO4"], (["NaCl"], ["NaCl"], ["NaCl"]))}
_B2S_B1 = {"Li2S": (0.0, "na", 0.0, "na"), "CaCl2": (-2.66, "wide", -6.82, "wide"), "CaS": (-2.66, "wide", -6.82, "wide"),
           "MgO": (5.0, "wide", 12.0, "wide"), "Al2O3": (2.1, "wide", 8.0, "wide"), "SiO2": (30.0, "wide", 40.0, "intermediate"),
           "LiF": (0.5, "wide", 3.0, "wide"), "BaO": (15.0, "wide", 20.0, "wide"), "ZnO": (-5.0, "wide", -8.0, "metallic"),
           "V2O5": (100.0, "undetermined", 150.0, "undetermined"), "Ag2O": (12.0, "metallic", -15.0, "metallic"),
           "SnO2": (25.0, "intermediate", 18.0, "metallic"), "GeS2": (20.0, "wide", 22.0, "intermediate"), "NaCl": (1.0, "wide", 4.0, "wide")}
_B2S_VPA = {"Li": 20.3, "Li3P": 15.0, "Li2S": 15.8, "LiCl": 17.0, "Li2O": 12.4, "Li3PS4": 22.0, "S": 26.0, "P2S7": 24.0, "SCl": 30.0,
            "Li3PO4": 12.8, "Ni3S2": 13.0, "Li2SO4": 13.5, "Ni": 10.9, "CaS": 21.0, "CaSO4": 13.0, "CaCl2": 25.0, "MgS": 16.0,
            "MgSO4": 11.5, "MgCl2": 22.0, "LiAl": 16.0, "LiAlO2": 9.5, "LiAlS2": 18.0, "AlCl3": 25.0, "Li15Si4": 17.0, "SiO2": 15.0,
            "SiS2": 20.0, "SiCl4": 35.0, "LiF": 8.2, "PF5": 20.0, "BaS": 30.0, "BaSO4": 15.0, "BaCl2": 28.0, "LiZn": 15.0, "ZnS": 20.0,
            "ZnCl2": 22.0, "V": 13.5, "LiVO2": 11.0, "VS4": 18.0, "Ag": 17.8, "Ag2S": 19.0, "AgCl": 22.0, "Li17Sn4": 19.0, "SnO2": 12.0,
            "SnS2": 23.0, "SnCl4": 30.0, "Li15Ge4": 17.0, "GeO2": 11.0, "GeS2": 22.0, "Na2S": 23.0, "Na2SO4": 13.5, "NaCl": 22.5}
_B2S_GAP = {"Li3P": 0.7, "Li2S": 3.4, "LiCl": 6.3, "Li2O": 5.0, "Li3PS4": 2.5, "S": 2.2, "P2S7": 2.1, "SCl": 2.4, "Li3PO4": 5.9,
            "Li2SO4": 5.5, "Ni3S2": 0.0, "CaS": 3.5, "CaSO4": 6.0, "CaCl2": 5.8, "MgS": 3.0, "MgSO4": 6.0, "MgCl2": 6.0, "LiAlO2": 5.0,
            "LiAlS2": 4.0, "AlCl3": 5.2, "Li15Si4": 0.3, "SiO2": 5.5, "SiS2": 2.6, "SiCl4": 6.5, "LiF": 8.7, "PF5": 7.0, "BaS": 3.0,
            "BaSO4": 6.0, "BaCl2": 6.0, "ZnS": 2.5, "ZnCl2": 4.5, "LiVO2": 2.0, "VS4": 1.0, "Ag2S": 0.9, "AgCl": 3.0, "SnO2": 2.6,
            "SnS2": 1.2, "SnCl4": 4.0, "Li15Ge4": 0.0, "GeO2": 4.0, "GeS2": 2.6, "Na2S": 2.4, "Na2SO4": 5.5, "NaCl": 5.0, "LiAl": 0.0,
            "LiZn": 0.0, "Ag": 0.0, "V": 0.0, "Li17Sn4": 0.0, "Ni": 0.0}
_B2S_SEV = {"Li2S": 0.0, "CaCl2": 0.3, "CaS": 0.3, "MgO": -0.2, "Al2O3": -0.4, "SiO2": 0.2, "LiF": -0.1, "BaO": 0.6, "ZnO": 0.1,
            "V2O5": -0.3, "Ag2O": 0.4, "SnO2": 0.5, "GeS2": 0.25, "NaCl": 0.45}
_B2S_PART = {"LNO_half": ("Li0.5NiO2", 11.0, ["Li3PO4", "Ni3S2", "LiCl", "Li2SO4", "Ni"]),
             "LNO_full": ("LiNiO2", 10.6, ["Li2S", "Li3PO4", "Ni3S2", "LiCl", "Li2SO4"]), "Li": ("Li", 20.3, ["Li3P", "Li2S", "LiCl"])}
_B2S_BANDS = ((2.0, ["Li3PS4", "LiCl", "S"]), (3.4, ["P2S7", "LiCl", "S"]), (3.9, ["P2S7", "SCl", "S"]))
_B2S_WOV = {"SiO2": {2: ["P2S7", "S"]}, "SnO2": {2: ["P2S7", "S"]}, "V2O5": {2: ["P2S7", "LiCl", "S"]}, "GeS2": {2: ["P2S7", "SCl"]}}


def _b2_synth(td, mut=None):
    """가상 묶음 2 출력 폴더 + 봉인 판독 + G3b 원자료 — (폴더, sealed, b1_ref, expected). 반응식은 pymatgen Reaction 이 균형을 잡는다
    (원자 보존 · 정확한 계수 = kink_terms). mut(W) 로 쓰기 전에 고친다 (W = rows · gaps · man · ref · sealed)."""
    from pymatgen.core import Composition
    from pymatgen.analysis.reaction_calculator import Reaction
    ir, esw = _b2_mod("interface_reactivity_v2"), _b2_mod("esw_grand_potential")
    mix = (8 * 22.0 + 3 * 15.8 + 2 * 17.0) / 13
    def rx(lhs, rhs, norm, val):
        r = Reaction([Composition(x) for x in lhs], [Composition(x) for x in rhs])
        r.normalize_to(Composition(norm), val)
        return r
    def vol_row(sp, f, cat):
        pf, pv, base = _B2S_PART[cat]
        o = "O" in Composition(f).as_dict()
        dop = [] if sp == "HOST" else (_B2S_D[sp][1] if cat == "Li" else _B2S_D[sp][2])
        prods = list(base) + (["Li2O"] if (cat == "Li" and o) else []) + list(dop)
        r = rx([f, pf], prods, f, 0.1)
        s = str(r)
        x, dE = {"Li": (0.6, -0.5), "LNO_half": (0.35, -0.62), "LNO_full": (0.48, -0.42)}[cat]
        vol = {"schema": "closed_volumes/v1", "ok": True,
               "products": {Composition(p).reduced_formula: {"phase": Composition(p).reduced_formula, "entry_id": f"syn-{p}",
                                                             "material_id": f"syn-{p}", "volume_per_atom_A3": _B2S_VPA[p], "nsites": 4}
                            for p in prods},
               "reactants": {"c1": {"formula_given": f, "basis": "hull_mixture", "decomposition": [{"phase": "Li3PS4", "amount_atom_frac": 1.0}],
                                    "mixture_volume_per_atom_A3": mix + (_B2S_SEV.get(sp, 0.0) if sp != "HOST" else 0.0)},
                             "c2": {"formula_given": pf, "basis": "stable_entry",
                                    "decomposition": [{"phase": Composition(pf).reduced_formula, "amount_atom_frac": 1.0}],
                                    "mixture_volume_per_atom_A3": pv}},
               "argyrodite_Li6PS5Cl": {"phase": "Li6PS5Cl", "volume_per_atom_A3": 18.4, "e_above_hull_eV_per_atom": 0.01},
               "kink_terms": {s: {"x": x, "terms": ir.reaction_terms_exact(r)}}}
        return {"species": sp, "formula": f, "cathode": cat, "cathode_formula": pf, "mode": "closed_0V", "dE_eV_per_atom": dE,
                "reaction": s, "mixing_x": x, "min_kink_at_endpoint": False, "kinks": [{"x": x, "dE_eV_per_atom": dE, "reaction": s}],
                "volumes": vol}
    def win_row(sp, f):
        o = "O" in Composition(f).as_dict()
        red = rx([f, "Li"], ["Li3P", "Li2S", "LiCl"] + (["Li2O"] if o else []) + ([] if sp == "HOST" else _B2S_D[sp][1]), f, 1.0)
        prof = [(0.0, red, [c.reduced_formula for c in red.products])]
        for i, (vk, base) in enumerate(_B2S_BANDS):
            prods = list(_B2S_WOV.get(sp, {}).get(i, base)) + (["Li3PO4"] if o else []) + ([] if sp == "HOST" else _B2S_D[sp][3][i])
            prof.append((vk, rx([f], prods + ["Li"], f, 1.0), [Composition(p).reduced_formula for p in prods]))
        steps, evo = [], []
        for vk, r, ps in prof:
            e = -float(r.get_coeff(Composition("Li"))) if Composition("Li") in r.all_comp else 0.0
            evo.append(e)
            steps.append({"evolution_Li": round(e, 4), "reaction": esw.rxn_str_fixed(r), "V_vs_Li": vk, "V_vs_Li_exact": vk,
                          "entries": [{"phase": p, "entry_id": f"syn-{p}"} for p in ps]})
        vks = [s["V_vs_Li_exact"] for s in steps]
        by = {}
        for V in B2_V:
            k, vr, sh = esw.interval_index(vks, V)
            ps = sorted(e["phase"] for e in steps[k]["entries"])
            by[f"{V:.2f}"] = {"V_grid": V, "V_read": vr, "shifted_1mV": sh, "row_index": k, "products": ps, "gp_products": list(ps),
                              "gp_same": True, "reaction": steps[k]["reaction"], "evolution_Li": evo[k], "li_released_per_fu": -evo[k]}
        return {"species": sp, "formula": f, "cathode": "WIN", "mode": "grand_potential_window", "n_atoms_fu": float(Composition(f).num_atoms),
                "profile": steps, "by_voltage": by, "release_onset_V": 2.0}
    Wd = {"rows": {"designs_vol": [vol_row(s, d_[0], c) for s, d_ in _B2S_D.items() for c in _B2S_PART],
                   "host_vol": [vol_row("HOST", "Li6PS5Cl", c) for c in _B2S_PART],
                   "designs_win": [win_row(s, d_[0]) for s, d_ in _B2S_D.items()], "host_win": [win_row("HOST", "Li6PS5Cl")]},
          "gaps": {k: {"band_gap_MP_eV": v, "material_id": f"syn-{k}"} for k, v in _B2S_GAP.items()}}
    inv = lambda ax: {"axis": ax, "tools_sha16": {t: "1" * 16 for t in B2_PHYS_TOOLS}, "mp_db_version_before": "2026.09.28",
                      "mp_db_version_after": "2026.09.28"}
    Wd["man"] = {"mp_db_version_before": "2026.09.28", "mp_db_version_after": "2026.09.28", "same_mp_version": True, "pymatgen": "x",
                 "mp_api": "y", "thermo_types": ["GGA_GGA+U"], "correction_names_sample_Li-Ni-O": ["c"], "tools_sha16": {"a": "1", "b": "2", "c": "3"},
                 "repo_head": "f" * 40, "lanes": {k: {"rc": 0} for k in B2_LANES}, "invocations": [inv("vol"), inv("win")]}
    Wd["ref"] = [{k: r[k] for k in ("species", "formula", "cathode", "cathode_formula", "mode", "dE_eV_per_atom", "reaction", "mixing_x")}
                 for r in Wd["rows"]["designs_vol"] + Wd["rows"]["host_vol"]]
    B = _B2S_B1
    ncm = {"blocking": [], "gates": {"G4": {"discriminates": True}},
           "rows": [{"species": s, "formula": _B2S_D[s][0], "delta_LNO_half_meV": B[s][0], "class_LNO_half": B[s][1]} for s in _B2S_D]}
    hyd = {"blocking": [], "gates": {"G4": {"discriminates": False}, "G7": {"overlap": False}},
           "rows": [{"species": s, "delta_hyd_meV": 0.0, "F1_hyd": False, "F2_H2S": False, "unknown": False} for s in _B2S_D]}
    li = {"blocking": [], "gates": {"G4": {"discriminates": True}, "G7": {"overlap": False, "rho_spearman": 0.5}},
          "rows": [{"species": s, "formula": _B2S_D[s][0], "delta_Li_meV": B[s][2], "class": B[s][3], "F1_Li": B[s][3] == "metallic",
                    "F2_Li": B[s][2] <= -10, "unknown": B[s][3] in ("undetermined", "na", "fate_error")} for s in _B2S_D]}
    li["combination"] = ax_combine(ncm, hyd, li)
    Wd["sealed"] = {"ncm": ncm, "hyd": hyd, "li": li, "sens": {}}
    if mut:
        mut(Wd)
    d = Path(td)
    for k, v in Wd["rows"].items():
        (d / f"{k}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in v), encoding="utf-8")
    for nm in ("product_gaps_vol.json", "product_gaps_win.json"):
        (d / nm).write_text(json.dumps({"gaps": Wd["gaps"]}), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps(Wd["man"]), encoding="utf-8")
    return d, Wd["sealed"], {"rows": Wd["ref"], "versions": ["2026.09.28"], "has_none": False, "problems": []}, \
        {s: _B2S_D[s][0] for s in _B2S_D}


def _b2_leftodd(r):
    """selftest — 좌변에 반응물이 아닌 항 (0.001 Ni) 을 넣되 정확한 계수 · kink 목록은 그 문자열에 맞춘다 (G2 좌변 검사만 걸리게)."""
    old = r["reaction"]
    lhs, rhs = old.split(" -> ")
    new = lhs + " + 0.001 Ni -> " + rhs
    terms = [list(t) for t in r["volumes"]["kink_terms"][old]["terms"]] + [["Ni", -0.001]]
    r["reaction"] = new
    r["kinks"] = [{**k, "reaction": new} if k["reaction"] == old else k for k in r["kinks"]]
    r["volumes"]["kink_terms"] = {new: {"x": r["mixing_x"], "terms": terms}}


def b2_selftest():
    """묶음 2 판독기 — 순위 기계 (R9 · R10 · R11 · 구간 · 방향 표) · 게이트 (G4 분위수 · G5 · G7 맞춘 ρ · 휘발 · 기체 · 거의 겹친 kink ·
    φ_und) 단위 시험 + 가상 원자료 끝까지 (양성 · 막는 게이트마다 음성 · '새 축 0 개면 순위 없음') + 묶음 1 재현.
    ⛔ pymatgen 이 없으면 안 돈 것 — 통과로 세지 않는다."""
    import copy
    import tempfile
    ok_all, n = True, [0, 0]
    def chk(c, msg):
        nonlocal ok_all
        n[0 if c else 1] += 1
        ok_all &= bool(c)
        print(("  ⭕ " if c else "  ⛔ ") + msg)
    if not _b2_has_pm():
        chk(False, "[전제] 묶음 2 판독기 시험은 pymatgen 이 있어야 돈다 — 안 돈 것은 통과가 아니다")
        print(f"bundle2 selftest: ⭕ {n[0]} · ⛔ {n[1]}")
        return 1
    W1 = {a: 1.0 for a in B2_AXES}
    # ── R9 · R10 · R11 순위 기계 (카드 · ED 예) ────────────────────────────────────────────────
    L3 = [("a", {"d_ncm": 0.0}), ("b", {"d_ncm": 0.001}), ("c", {"d_ncm": 1.0005})]
    rk = b2_ranks(L3, ("d_ncm",), W1)
    rk_s = b2_ranks([(k, {"sv_li": v["d_ncm"]}) for k, v in L3], ("sv_li",), W1)
    chk([rk[k]["d_ncm"] for k in "abc"] == [2, 1, 1] and [rk_s[k]["sv_li"] for k in "abc"] == [1, 1, 2],
        "R9: r = 1 + #(w 를 넘게 나은 설계) — w = 1 · 값 0 · 0.001 · 1.0005 → 2 · 1 · 1 (w 안 차이도 제3 설계로 갈린다) · '작을수록' 축은 반대")
    rf = b2_ranks([(k, {"f_ins": v}) for k, v in (("x", 1.0), ("y", 0.875), ("z", 0.75))], ("f_ins",), B2_W)
    chk([rf[k]["f_ins"] for k in "xyz"] == [1, 1, 2],
        "R9 · w_④ = 1/8: 한 점 차이 (0.125) 는 '넘게 낫다' 가 아니다 — 두 점 이상만 순위를 가른다 (1 · 0.875 · 0.75 → 1 · 1 · 2)")
    P5 = [(i, {"d_ncm": float(5 - i), "d_li": float(1 + i)}) for i in range(5)]
    r5 = b2_ranks(P5, ("d_ncm", "d_li"), W1)
    chk(set(b2_layers(P5, r5, ("d_ncm", "d_li"), W1).values()) == {1},
        "R11 지배 = 순위 벡터 + 한 축 이상 값이 w 를 넘게 나음 — (5,1) · (4,2) · (3,3) · (2,4) · (1,5) · w = 1 은 한 층 (순위 벡터만이면 이웃이 밀린다)")
    E3 = [("A", {"d_ncm": 0.0, "d_li": 0.0, "f_ins": 0.0}), ("B", {"d_ncm": -1.5, "d_li": 0.9, "f_ins": 0.9}),
          ("C", {"d_ncm": -0.6, "d_li": 1.5, "f_ins": -0.5})]
    ax3 = ("d_ncm", "d_li", "f_ins")
    eps = lambda x, y: all(x[a] >= y[a] - 1.0 for a in ax3) and any(x[a] > y[a] + 1.0 for a in ax3)
    V3 = dict(E3)
    try:
        lay3 = b2_layers(E3, b2_ranks(E3, ax3, W1), ax3, W1)
    except RuntimeError:
        lay3 = None
    chk(eps(V3["A"], V3["B"]) and eps(V3["B"], V3["C"]) and eps(V3["C"], V3["A"]) and lay3 == {"A": 1, "B": 1, "C": 1},
        "R11: 카드의 ε-지배 순환 (A ≻ B ≻ C ≻ A · w = 1) 이 우리 지배에서는 순환 없이 한 층")
    X5 = [(i, {"d_ncm": float(10 - i), "d_li": float(6 + i)}) for i in range(5)]
    def pos(W):
        r_ = b2_ranks(X5, ("d_ncm", "d_li"), W)
        return [b2_positions({k: b2_lex(r_[k]) for k, _ in X5})[i] for i in range(5)]
    p11, p25, p2x = pos(W1), pos({**W1, "d_ncm": 2.5}), pos({a: 2.0 for a in B2_AXES})
    chk(p11 == [4, 2, 1, 2, 4] and p25 == [5, 3, 1, 1, 3] and [i for i in sorted(range(5), key=lambda i: p2x[i])][0] == 2,
        f"R10 leximin (나쁜 r 부터 사전식 · 동률 같은 번호 · 다음 건너뜀) · 동률 폭이 무게처럼 작동 (축 ① 폭만 2.5 → 순서 바뀜) {p11} · {p25}")
    L4 = [(i, {"d_ncm": v}) for i, v in enumerate((0.0, 0.2, 0.4, 0.6))]
    r4 = b2_ranks(L4, ("d_ncm",), W1)
    lay4 = b2_layers(L4, r4, ("d_ncm",), W1)
    io = b2_insert({"d_ncm": None}, L4, r4, lay4, ("d_ncm",), W1, "opt")
    ip = b2_insert({"d_ncm": None}, L4, r4, lay4, ("d_ncm",), W1, "pess")
    chk(set(x["d_ncm"] for x in r4.values()) == {1} and io["r"]["d_ncm"] == 1 and ip["r"]["d_ncm"] == 5 and io["position"] == 1
        and ip["position"] == 5 and ip["layer"] == 2 and io["layer"] == 1,
        "R10 모름 구간: 값 있는 넷이 다 w 안 (r 1 · 1 · 1 · 1) — 낙관 끝 r = 1 · 비관 끝 r = 1 + 줄 길이 = 5 (그 무리 최댓값 + 1 이 아니다)")
    def recs_of(spec):
        return [{"species": s, "comp_key": ck, "group": g, "values": v} for s, ck, g, v in spec]
    V6 = [("p0", "k0", "A", {"d_ncm": 5.0, "d_li": 1.0}), ("p1", "k1", "A", {"d_ncm": 4.0, "d_li": 2.0}), ("p2", "k2", "A", {"d_ncm": 3.0, "d_li": 3.0}),
          ("p3", "k3", "A", {"d_ncm": 2.0, "d_li": 4.0}), ("p4", "k4", "A", {"d_ncm": 1.0, "d_li": 5.0}),
          ("u", "ku", "?", {"d_ncm": 100.0, "d_li": 150.0}), ("p2b", "k2", "A", {"d_ncm": 3.0, "d_li": 3.0})]
    rr = b2_rank(recs_of(V6), ("d_ncm", "d_li"), W1)
    pu = rr["per"]["ku"]["interval"]
    chk(rr["line_A_length"] == 5 and rr["selection"] == ["p0", "p1", "p2", "p2b", "p3", "p4"] and "u" not in rr["selection"]
        and pu["optimistic"] == {**pu["optimistic"], "group": "A", "position": 1, "layer": 1} and pu["pessimistic"]["group"] == "B"
        and pu["pessimistic"]["position"] == 6 and rr["dft_resolve_candidates"][0]["species"] == ["u"]
        and rr["per"]["k2"]["species"] == ["p2", "p2b"],
        "R8 · R10 · R13: 표시 모름 (모든 축에서 제일 나은 설계) 은 무리 A 셈에서 빠져 남의 층을 안 덮는다 · 구간 = 낙관 무리 A 1 등 · 비관 무리 B · "
        "선택에서 빼고 'DFT 로 모름을 풀 후보' · 같은 조성은 한 줄 (줄 길이 5)")
    H0 = {"F1_hyd": False, "F2_H2S": False, "unknown": False}
    f_u = b2_flags({"class_LNO_half": "undetermined", "delta_LNO_half_meV": 5.0}, H0, {"class": "wide", "F2_Li": False}, False)
    f_na = b2_flags({"class_LNO_half": "na", "delta_LNO_half_meV": 0.0}, H0, {"class": "na", "F2_Li": False}, False)
    f_m = b2_flags({"class_LNO_half": "metallic", "delta_LNO_half_meV": -12.0}, {**H0, "unknown": True},
                   {"class": "undetermined", "F2_Li": True}, None)
    chk(f_u == ([], ["축①F1_금속성"]) and f_na == ([], [])
        and f_m == (["축①F1_금속성", "축①F2_반응증가", "축③F2_Li반응증가"], ["축②F2_H2S증가", "축③F1_Li금속성", "축④F_win_금속성"]),
        "R8 표시: ⓓ 미판정 → 그 표시는 모름 (무리 A 아님) · ㉧ 해당 없음 → 정의상 거짓 (무리 A) · H₂S 모름 · F_win 모름 · 확정 표시는 따로")
    ML = recs_of([("a", "ka", "A", {"d_ncm": 5.0, "d_li": 5.0}), ("b", "kb", "A", {"d_ncm": 1.0, "d_li": 1.0}),
                  ("c", "kc", "A", {"d_ncm": 5.0, "d_li": 1.0}), ("d", "kd", "B", {"d_ncm": 9.0, "d_li": 9.0}),
                  ("e", "ke", "B", {"d_ncm": 0.0, "d_li": 0.0})])
    rml = b2_rank(ML, ("d_ncm", "d_li"), W1)
    pm = rml["per"]
    chk(rml["selection"] == ["a"] and [pm[k]["pareto_layer"] for k in ("ka", "kc", "kb")] == [1, 2, 3]
        and (pm["kd"]["position"], pm["ke"]["position"], pm["kd"]["position_in_group"]) == (4, 5, 1) and "d" not in rml["selection"]
        and rml["line_A_length"] == 3 and rml["line_B_length"] == 2,
        "R11 · R13: 층 1 · 2 · 3 이 갈리는 줄에서 선택 = 무리 A 층 1 만 · 무리 B 줄은 같은 규칙으로 따로 (번호는 A 줄 뒤 4 · 5) · B 는 선택 밖")
    sv5 = recs_of([(f"s{i}", f"k{i}", "A", {"d_ncm": float(i), "sv_li": float(4 - i) * 3}) for i in range(5)])
    base_pos = [b2_rank(sv5, ("d_ncm", "sv_li"))["per"][f"k{i}"]["position"] for i in range(5)]
    B2_DIR["sv_li"] = "larger"
    try:
        flip_pos = [b2_rank(sv5, ("d_ncm", "sv_li"))["per"][f"k{i}"]["position"] for i in range(5)]
        rho_flip = b2_rho([{**r, "values": {**r["values"]}} for r in sv5], "sv_li", "d_ncm")[0]
    finally:
        B2_DIR["sv_li"] = "smaller"
    rho_ok = b2_rho(sv5, "sv_li", "d_ncm")[0]
    chk(base_pos == [5, 4, 3, 2, 1] and flip_pos == [1, 2, 3, 4, 5] and abs(rho_ok - 1.0) < 1e-12 and abs(rho_flip + 1.0) < 1e-12,
        f"⛔음성 방향 표: '작을수록' 축 하나를 뒤집으면 순위 ({base_pos} → {flip_pos}) 와 맞춘 ρ (+1 → −1) 가 바뀐다 — R9 · R11 · G7 이 표 하나를 읽는다")
    # ── G4 분위수 · G7 맞춘 ρ ────────────────────────────────────────────────────────────────
    pl = lambda k6: [{"species": f"q{i}", "comp_key": f"q{i}", "group": "A", "values": {"f_ins": 0.75 if i < k6 else 1.0}} for i in range(25)]
    g7_, g6_ = b2_g4(pl(7), "f_ins"), b2_g4(pl(6), "f_ins")
    chk(g7_["discriminates"] is True and g6_["discriminates"] is False and g6_["iqr"] == 0.0 and g6_["distribution"] == [[0.75, 6], [1.0, 19]],
        "G4: statistics.quantiles(n=4, inclusive) — 25 중 7 이 0.75 면 IQR 0.25 ≥ 1/8 (갈린다) · 6 이면 IQR 0 (안 갈린다 · exclusive 면 0.125 로 갈린다) · 값마다 설계 수 기록")
    up = recs_of([(f"t{i}", f"t{i}", "A", {"d_ncm": float(i), "sv_li": float(i)}) for i in range(6)])
    rho_c = b2_rho(up, "sv_li", "d_ncm")[0]
    chk(abs(rho_c + 1.0) < 1e-12, "G7: ρ 는 좋은 방향으로 맞춘 값 — 원값이 같이 오르는 '작을수록' 축과 '클수록' 축은 ρ = −1 (상충 · 겹침 아님)")
    def adm_recs(fv):
        out = []
        for i in range(8):
            v = {"d_ncm": 10.0 * i, "d_li": float((i * 5) % 8) * 10.0, "sv_ncm": None, "sv_li": None, "dphi_li": None, "f_ins": fv(i)}
            out.append({"species": f"a{i}", "comp_key": f"a{i}", "group": "A", "values": v, "values_atom": {"sv_ncm": None, "sv_li": None}})
        return out
    SEALED_OK = {"ncm": {"gates": {"G4": {"discriminates": True}}}, "li": {"gates": {"G4": {"discriminates": True}, "G7": {"overlap": False}}}}
    a_con, g_con = b2_admission(adm_recs(lambda i: (7 - i) / 7.0), SEALED_OK)
    a_ovl, g_ovl = b2_admission(adm_recs(lambda i: i / 7.0), SEALED_OK)
    chk("f_ins" in a_con and g_con["G7"]["f_ins"]["conflicts"] == ["d_ncm"] and "f_ins" not in a_ovl
        and g_ovl["G7"]["f_ins"]["why_not"].startswith("G7") and a_con[:2] == ["d_ncm", "d_li"],
        "G7 (순서 ① → ③ → … → ④): 맞춘 ρ ≤ −0.8 (상충) 은 순위에 넣고 적는다 · ρ ≥ 0.8 (겹침) 은 기록만 · 축 ① · ③ 이 먼저 들어 있다")
    a_pl, g_pl = b2_admission(adm_recs(lambda i: 0.5 if i == 7 else 1.0), SEALED_OK)
    a_b1, _ = b2_admission(adm_recs(lambda i: (7 - i) / 7.0),
                           {"ncm": SEALED_OK["ncm"], "li": {"gates": {"G4": {"discriminates": False}, "G7": {"overlap": False}}}})
    chk("f_ins" not in a_pl and g_pl["G7"]["f_ins"]["why_not"].startswith("G4") and g_pl["G4"]["f_ins"]["iqr"] == 0.0
        and abs(g_pl["G7"]["f_ins"]["vs_admitted"]["d_ncm"]["rho_aligned"]) < 0.8 and "d_li" not in a_b1 and a_b1[0] == "d_ncm",
        "⛔음성 R7: 한 값에 몰린 축 (8 중 7 같음 · IQR 0) 은 ρ 가 낮아도 G4 로 기록만 · 축 ③ 은 묶음 1 G4 가 '갈린다' 일 때만 순위 축")
    # ── G5 카드 대조 ────────────────────────────────────────────────────────────────────────
    card = B2_CARD.read_text(encoding="utf-8")
    cj = json.loads(card)
    cj_dir = copy.deepcopy(cj)
    cj_dir["합치는_규칙_묶음_2"]["방향_표"]["축_⑤_s_V_Li"] = "클수록"
    cj_vol = copy.deepcopy(cj)
    cj_vol["2_그것을_재는_양"]["축_④_작동창_도펀트_행방"]["휘발_분자_산물_ED_P1_5"]["목록 (결과 전 봉인)"].remove("SiCl4")
    g5 = [b2_card_check(card)["ok"], b2_card_check(card.replace("w_⑤ = 1 %p", "w_⑤ = 2 %p"))["ok"],
          b2_card_check(json.dumps(cj_dir, ensure_ascii=False))["ok"], b2_card_check(json.dumps(cj_vol, ensure_ascii=False))["ok"]]
    chk(g5 == [True, False, False, False],
        f"G5: 진짜 카드 통과 · ⛔음성 동률 폭 바꿈 · 방향 표 한 줄 뒤집음 · 휘발 목록 한 줄 뺌 → 불통과 ({g5})")
    # ── 휘발 · 기체 · 분자 결정 (Composition 대조) · 휘발 몫과 설계 등급 ────────────────────────────
    chk(b2_in_list("SCl", B2_VOLATILE) and b2_in_list("S2Cl2", B2_VOLATILE) and b2_in_list("SCl2", B2_VOLATILE)
        and not b2_in_list("PCl5", B2_VOLATILE) and b2_in_list("PCl5", B2_MOLECULAR) and b2_in_list("Cl2", B2_GAS)
        and not b2_in_list("Li2S", B2_GAS) and b2_product_class("SCl", {"SCl": {"band_gap_MP_eV": 2.4}})[0] == "volatile",
        "휘발 목록: MP 'SCl' ≡ S2Cl2 (reduced Composition · 문자열 대조 아님) · SCl2 따로 · PCl5 는 목록 밖 분자 결정 (기록만) · 기체 목록 Cl2")
    gx = {"SiS2": {"band_gap_MP_eV": 2.6}, "SiCl4": {"band_gap_MP_eV": 6.5}}
    c15 = ax_design_class({"reaction": "Li20SiP4S18Cl4O2 -> 0.85 SiS2 + 0.15 SiCl4 + 10 Li", "min_kink_at_endpoint": False}, ["Si"], gx,
                          classify=b2_product_class, extra_classes=("volatile",))
    c05 = ax_design_class({"reaction": "Li20SiP4S18Cl4O2 -> 0.95 SiS2 + 0.05 SiCl4 + 10 Li", "min_kink_at_endpoint": False}, ["Si"], gx,
                          classify=b2_product_class, extra_classes=("volatile",))
    c00 = ax_design_class({"reaction": "Li20SiP4S18Cl4O2 -> 0.95 SiS2 + 0.05 SiCl4 + 10 Li", "min_kink_at_endpoint": False}, ["Si"], gx)
    chk(c15[0] == "intermediate" and abs(c15[1]["Si"]["shares"]["volatile"] - 0.15) < 1e-9 and c05[0] == "wide"
        and "volatile" not in c00[1]["Si"]["shares"] and c00[0] == "wide",
        "휘발 몫 15 % → ⓐ 될 수 없다 (ⓒ) · 5 % → ⓐ · extra_classes 없이 부르면 몫 사전이 묶음 1 판과 같다 (휘발 열쇠 없음)")
    # ── 아지로다이트 원자 부피 판 '해당 없음' (카드 개정 2 · 2026-11-11 · Cl 을 F · Br 로 다 바꾼 설계) ─────────────────
    AG = {"phase": "Li6PS5Cl", "volume_per_atom_A3": 18.4}
    NA = "이 hull 의 원소에 Cl 가 없다 — Li6PS5Cl 가 있을 수 없다 (원자 부피 판 해당 없음)"
    ap_ok = [b2_argy_problem("Li25P3S20F4Ti1", "Li", {"argyrodite_Li6PS5Cl": None, "argyrodite_not_applicable": NA}),
             b2_argy_problem("Li25P3S20Br4Zr1", "Li0.5NiO2", {"argyrodite_Li6PS5Cl": None, "argyrodite_not_applicable": NA}),
             b2_argy_problem("Li24P4S20Cl3F", "Li", {"argyrodite_Li6PS5Cl": AG, "argyrodite_not_applicable": None}),
             b2_argy_problem("Li24P4S20Cl3F", "LiNiO2", {"argyrodite_Li6PS5Cl": AG})]
    ap_bad = [b2_argy_problem("Li24P4S20Cl3F", "Li", {"argyrodite_Li6PS5Cl": None, "argyrodite_not_applicable": NA}),
              b2_argy_problem("Li25P3S20F4Ti1", "Li", {"argyrodite_Li6PS5Cl": None, "argyrodite_not_applicable": None}),
              b2_argy_problem("Li25P3S20F4Ti1", "Li", {"argyrodite_Li6PS5Cl": None, "argyrodite_not_applicable": "  "}),
              b2_argy_problem("Li25P3S20F4Ti1", "Li", {"argyrodite_Li6PS5Cl": AG, "argyrodite_not_applicable": NA}),
              b2_argy_problem("Li25P3S20F4Zr1", "Li", {"argyrodite_Li6PS5Cl": AG}),
              b2_argy_problem("Li24P4S20Cl3F", "Li", {"argyrodite_Li6PS5Cl": AG, "argyrodite_not_applicable": NA}),
              b2_argy_problem("Li24P4S20Cl3F", "Li", {"argyrodite_Li6PS5Cl": {"phase": "Li6PS5Cl"}}),
              b2_argy_problem("Li25P3S20F4Ti1", "LiCl", {"argyrodite_Li6PS5Cl": None, "argyrodite_not_applicable": NA})]
    chk(ap_ok == [None] * 4 and all(isinstance(x, str) and x for x in ap_bad),
        "아지로다이트 원자 부피 판 (카드 개정 2): Cl 없는 설계 (TiF4 · ZrBr4 꼴) 는 기록 없음 + '해당 없음' 사유일 때만 통과 · "
        "⛔음성 Cl 있는 설계의 '해당 없음' · 사유 없음 · 빈 사유 · Cl 없는데 기록 있음 · 부피와 사유가 같이 · 부피 숫자 없음 · "
        f"상대 쪽 Cl (hull 원소 = 설계 ∪ 상대) → G2 사유 ({[x is not None for x in ap_bad]})")
    # ── 가상 원자료 끝까지 ─────────────────────────────────────────────────────────────────────
    DEC = ("active", "db/properties/" + B2_CARD.name)
    def run(mut=None, card_text=card, decision=DEC, b1_repro=None):
        with tempfile.TemporaryDirectory() as td:
            d, sealed, ref, exp = _b2_synth(td, mut)
            return b2_readout(d, expected=exp, card_text=card_text, decision=decision, sealed=sealed, b1_ref=ref,
                              b1_repro=b1_repro or {"problems": []}, plus_u_b1=(sealed["ncm"], sealed["li"]))
    r0 = run()
    by = {r["species"]: r for r in r0.get("rows", [])}
    rk0 = r0.get("ranking") or {}
    h5 = (r0.get("host") or {}).get("w5", {}).get("Li", {}).get("hull", {}).get("dv")
    want_h5 = 100.0 * (331.0 - (257.4 + 162.4)) / (257.4 + 162.4)
    chk(not r0["blocking"] and h5 is not None and abs(h5 - want_h5) < 1e-9 and r0["gates"]["G1c"]["same_as_host"] == ["Li2S"]
        and r0["gates"]["G1c"]["same_composition_groups"] == [["CaCl2", "CaS"]] and r0["gates"]["G3b"]["n_keys"] == 45,
        f"양성 (가상 원자료): 막는 게이트 통과 · 호스트 + Li ΔV/V = 손 계산 (Li6PS5Cl + 8 Li → Li3P + 5 Li2S + LiCl · {want_h5:.4f} %) · "
        f"Li2S ≡ 호스트 (문자열 정규화가 달라도 정확한 계수로 |Δ| ≤ 1e-9) · CaCl2 ≡ CaS · G3b 15 × 3 쌍 ({r0['blocking']})")
    chk(by and by["SiO2"]["values"]["f_ins"] == 0.75 and by["LiF"]["values"]["f_ins"] == 0.75 and by["SnO2"]["values"]["f_ins"] == 0.0
        and by["Ag2O"]["group"] == "B" and "축④F_win_금속성" in by["Ag2O"]["flags"] and by["V2O5"]["group"] == "?"
        and "축④F_win_금속성" in by["V2O5"]["flags_unknown"] and by["Li2S"]["values"]["f_ins"] is None and by["Li2S"]["group"] == "A"
        and by["Li2S"]["flags_unknown"] == []
        and abs(by["SiO2"]["w4_points"]["4.25"]["volatile_share"]["Si"] - 1.0) < 1e-9 and by["SiO2"]["w4_points"]["4.25"]["class"] == "intermediate",
        "④: SiCl4 · PF5 (휘발) 점은 ⓐ 아님 → f_ins 0.75 · Ag 금속 점 → F_win (무리 B) · VS4 (+U · ⓓ) → F_win 모름 (표시 모름 '?') · Li2S ㉧ → f_ins 모름")
    chk(rk0 and set(rk0["selection"]) <= {s for s, r in by.items() if r["group"] == "A" and r.get("in_line")} and "V2O5" not in rk0["selection"]
        and [c["species"] for c in rk0["dft_resolve_candidates"]] == [["V2O5"]] and by["CaCl2"]["position"] == by["CaS"]["position"]
        and by["CaCl2"]["pareto_layer"] == by["CaS"]["pareto_layer"] and by["Li2S"]["in_line"] is False and by["Li2S"]["interval"]
        and set(r0["R12"]) >= {"leave_one_axis_out", "all_widths_x0.5", "all_widths_x2", "one_width_at_a_time", "plusU_by_gap",
                               "signed_dV_Xin_Li_기록만", "gas0", "atom_volume", "pareto_layer1_vs_top"},
        f"R10–R13: 선택 = 무리 A 줄의 층 1 ({rk0.get('selection')}) · 표시 모름 V2O5 는 'DFT 로 모름을 풀 후보' · CaCl2 ≡ CaS 같은 자리 · "
        f"Li2S (④ 모름) 는 구간 · R12 판 다 있음 · 순위 축 {r0.get('axes_ranking')}")
    chk(r0["gates"]["G8"]["sv_ncm"]["passes"] is False and "sv_ncm" not in r0["axes_ranking"]
        and r0["gates"]["G7"]["sv_ncm"]["why_not"].startswith("G8") and set(r0["axes_ranking"]) >= {"d_ncm", "d_li"},
        f"G8: 두 회계 판 (hull 혼합 · 원자 부피) ρ < 0.8 이면 ⑤ 축은 순위에 안 든다 (ρ {r0['gates']['G8']['sv_ncm']['rho']:.3f}) · 축 ① · ③ 은 묶음 1 G4 그대로")
    with tempfile.TemporaryDirectory() as td:
        pth = Path(td) / "x_bundle2_designs.csv"
        b2_write_csv(r0, pth)
        hdr = pth.read_text(encoding="utf-8").splitlines()
    chk(len(hdr) == 2 + len(by) and "sV_Li_pp" in hdr[1] and "r_f_ins" in hdr[1] and "leximin_position" in hdr[1],
        "Origin 용 CSV: 머리줄 · 열 이름 명시 · 설계마다 한 줄")
    # 카드 개정 2 배선 — 가상 LiF 를 'Cl 없는 설계' 로 보게 하고 (판독기 원소 판정만 바꿈) 그 부피 기록을 기록기의 '해당 없음' 꼴로 →
    # G2 통과 · 주 판 값 그대로 · 원자 부피 판 ⑤ 만 모름 · G8 은 두 판이 다 있는 설계만 (n − 1) · 사유 없는 기록은 G2 로 막힌다
    real_ap = globals()["_b2_argy_possible"]
    try:
        globals()["_b2_argy_possible"] = lambda f, cf: f != _B2S_D["LiF"][0] and real_ap(f, cf)
        r_na = run(lambda W: [r["volumes"].update(argyrodite_Li6PS5Cl=None, argyrodite_not_applicable="이 hull 의 원소에 Cl 가 없다 (selftest)")
                              for r in W["rows"]["designs_vol"] if r["species"] == "LiF"])
        r_na_bad = run(lambda W: [r["volumes"].update(argyrodite_Li6PS5Cl=None) for r in W["rows"]["designs_vol"] if r["species"] == "LiF"])
    finally:
        globals()["_b2_argy_possible"] = real_ap
    bn = {x["species"]: x for x in r_na.get("rows", [])}
    g8a, g8b = r0["gates"].get("G8", {}), r_na["gates"].get("G8", {})
    chk(not r_na["blocking"] and bool(bn) and bn["LiF"]["values"] == by["LiF"]["values"]
        and bn["LiF"]["values_atom"] == {"sv_ncm": None, "sv_li": None}
        and str(bn["LiF"]["w5"]["Li"]["atom"].get("why")).startswith("원자 부피 판 해당 없음")
        and all(bn[s_]["values_atom"] == by[s_]["values_atom"] for s_ in by if s_ != "LiF")
        and all(g8b[a]["n"] == g8a[a]["n"] - 1 and g8b[a]["n_main_only"] == 1 and g8a[a]["n_main_only"] == 0 for a in ("sv_ncm", "sv_li"))
        and "G2" in r_na_bad["blocking"] and "rows" not in r_na_bad,
        "카드 개정 2 배선: Cl 없는 설계 (가상 LiF) 는 G2 통과 · 주 판 값 그대로 · 원자 부피 판 ⑤ 만 모름 ('해당 없음' 사유) · "
        "G8 은 두 판이 다 있는 설계만 (n − 1 · n_main_only 1) · ⛔음성 사유 없는 기록은 G2 로 막힌다")
    # 음성 — 막는 게이트마다
    def rows_of(W, lane, sp, cat=None):
        return [r for r in W["rows"][lane] if r["species"] == sp and (cat is None or r["cathode"] == cat)]
    def m_vol(sp, cat, fn):
        return lambda W: [fn(r) for r in rows_of(W, "designs_vol" if sp != "HOST" else "host_vol", sp, cat)]
    def m_win(sp, fn):
        return lambda W: [fn(r) for r in rows_of(W, "designs_win" if sp != "HOST" else "host_win", sp)]
    def setp(r, V, **kw):
        r["by_voltage"][V].update(kw)
    neg = {
        "결정 proposed": (run(decision=("proposed", DEC[1])), "decision"),
        "카드 문턱 바꿈": (run(card_text=card.replace("φ_und > 0.01", "φ_und > 0.02")), "G5"),
        "묶음 1 재현 실패": (run(b1_repro={"problems": ["축 ① x"]}), "B1"),
        "봉인 합치기 표시 불일치": (run(lambda W: W["sealed"]["li"]["combination"]["rows"][0].update(flags=["축①F1_금속성"])), "B1"),
        "manifest repo_head 없음": (run(lambda W: W["man"].pop("repo_head")), "G1"),
        "vol · win 물리 도구 sha 다름": (run(lambda W: W["man"]["invocations"][1]["tools_sha16"].update({B2_PHYS_TOOLS[1]: "2" * 16})), "G1"),
        "win 실행 기록 없음": (run(lambda W: W["man"]["invocations"].pop(1)), "G1"),
        "MP 판 다름": (run(lambda W: W["man"]["invocations"][1].update(mp_db_version_after="2026.11.01")), "G3"),
        "G3b 산물 바꿈 (원자료)": (run(lambda W: W["ref"][0].update(reaction=W["ref"][0]["reaction"].replace("LiCl", "LiClO4"))), "G3b"),
        "G3b x + 2e-6": (run(lambda W: W["ref"][1].update(mixing_x=W["ref"][1]["mixing_x"] + 2e-6)), "G3b"),
        "G3b dE + 2e-5": (run(lambda W: W["ref"][2].update(dE_eV_per_atom=W["ref"][2]["dE_eV_per_atom"] + 2e-5)), "G3b"),
        "창 행 빠짐": (run(lambda W: W["rows"]["designs_win"].pop(3)), "G2"),
        "부피 기록 거부": (run(m_vol("MgO", "Li", lambda r: r.update(volumes={"ok": False, "refused": ["x"]}))), "G2"),
        "Cl 있는 설계의 아지로다이트 '해당 없음'": (run(m_vol("MgO", "Li", lambda r: r["volumes"].update(argyrodite_Li6PS5Cl=None, argyrodite_not_applicable="x"))), "G2"),
        "창 산물 갭 조회 없음": (run(lambda W: W["gaps"].pop("SiCl4")), "G2"),
        "정확한 계수 없음": (run(m_vol("BaO", "LNO_half", lambda r: r["volumes"].update(kink_terms={}))), "G2"),
        "좌변에 반응물 아닌 항": (run(m_vol("NaCl", "Li", lambda r: _b2_leftodd(r))), "G2"),
        "⑤ 앵커 밖 (호스트 + Li)": (run(m_vol("HOST", "Li", lambda r: r["volumes"]["reactants"]["c2"].update(mixture_volume_per_atom_A3=9.0))), "G1b"),
        "상대 혼합에 O2": (run(m_vol("ZnO", "LNO_half", lambda r: r["volumes"]["reactants"]["c2"]["decomposition"].append({"phase": "O2", "amount_atom_frac": 0.0}))), "G1b"),
        "④ 호스트 4.25 V Li 안 내놓음": (run(m_win("HOST", lambda r: setp(r, "4.25", li_released_per_fu=0.0))), "G1b"),
        "④ 호스트 개시 ≥ 2.50": (run(m_win("HOST", lambda r: r.update(release_onset_V=2.6))), "G1b"),
        "④ 교차 경로 다름": (run(m_win("MgO", lambda r: setp(r, "3.50", gp_products=["MgS", "P2S7"]))), "G1b"),
        "④ 가장 가까운 줄로 읽음": (run(m_win("BaO", lambda r: setp(r, "3.75", row_index=3))), "G1b"),
        "G1c Li2S ≢ 호스트": (run(m_vol("Li2S", "Li", lambda r: r["volumes"]["products"]["Li3P"].update(volume_per_atom_A3=15.2))), "G1c"),
        "G1c CaCl2 ≢ CaS": (run(m_vol("CaS", "LNO_full", lambda r: r["volumes"]["reactants"]["c1"].update(mixture_volume_per_atom_A3=19.0))), "G1c"),
        "G1c 원자 보존 (창 반응식)": (run(m_win("LiF", lambda r: setp(r, "2.50", reaction=r["by_voltage"]["2.50"]["reaction"].replace(" + ", " + 2 ", 1)))), "G1c"),
    }
    bad = {k: v[0]["blocking"] for k, v in neg.items() if v[1] not in v[0]["blocking"] or "rows" in v[0]}
    chk(not bad, f"⛔음성: 막는 게이트마다 깨면 표를 안 낸다 — 결정 · G5 · B1 (재현 · 표시) · G1 (manifest · 도구 sha · 실행) · G3 · "
                 f"G3b (산물 · x 2e-6 · dE 2e-5) · G2 (행 · 부피 · 갭 · 정확한 계수 · 좌변) · G1b (⑤ 앵커 · O2 · ④ Li · 개시 · 교차 · 가장 가까운 줄) · "
                 f"G1c (Li2S · CaS · 원자 보존) ({bad})")
    # 비-막는 판정 — 거의 겹친 kink · φ_und · 새 축 0 개면 순위 없음
    from pymatgen.core import Composition as _C
    from pymatgen.analysis.reaction_calculator import Reaction as _R
    def tie(W):
        r = rows_of(W, "designs_vol", "BaO", "Li")[0]
        r2 = _R([_C(r["formula"]), _C("Li")], [_C(p) for p in ("LiP", "Li2S", "LiCl", "Li2O", "BaS")])
        r2.normalize_to(_C(r["formula"]), 0.1)
        s2 = str(r2)
        r["kinks"].append({"x": r["mixing_x"] + 0.01, "dE_eV_per_atom": r["dE_eV_per_atom"] + 5e-6, "reaction": s2})
        r["volumes"]["kink_terms"][s2] = {"x": r["mixing_x"] + 0.01, "terms": _b2_mod("interface_reactivity_v2").reaction_terms_exact(r2)}
        r["volumes"]["products"]["LiP"] = {"phase": "LiP", "volume_per_atom_A3": 18.0}
        W["gaps"]["LiP"] = {"band_gap_MP_eV": 0.5}
    r_t = run(tie)
    bt = {x["species"]: x for x in r_t.get("rows", [])}
    chk(not r_t["blocking"] and bt["BaO"]["values"]["sv_li"] is None and "거의 겹치는 kink" in bt["BaO"]["unknown_why"].get("sv_li", "")
        and bt["BaO"]["w5"]["Li"]["hull"]["n_tie"] == 1,
        "거의 겹친 kink (|ΔdE| ≤ 1e-5) 의 ΔV/V 를 못 내거나 w_⑤ 를 넘게 다르면 그 설계 ⑤ Li 는 모름 (구간 · 순위 셈 밖)")
    r_u = run(lambda W: W["gaps"].update({"BaS": {"error": "no MP entry"}}))
    bu = {x["species"]: x for x in r_u.get("rows", [])}
    chk(not r_u["blocking"] and bu["BaO"]["values"]["dphi_li"] is None and "미판정" in bu["BaO"]["unknown_why"].get("dphi_li", ""),
        "⑥: 갭을 못 찾은 산물 (미판정) 부피 분율 > 0.01 → δφ_wide 모름")
    real_adm = globals()["b2_admission"]
    try:
        globals()["b2_admission"] = lambda recs, sealed: (["d_ncm", "d_li"], {"G4": {}, "G7": {}, "G8": {}})
        r_n = run()
    finally:
        globals()["b2_admission"] = real_adm
    chk(not r_n["blocking"] and r_n.get("ranking") is None and "R12" not in r_n and "⛔_순위_없음" in r_n
        and all("position" not in x and "pareto_layer" not in x for x in r_n["rows"]) and r_n["summary"]["groups"]["B"] == 3,
        "⛔음성 §9: 새 연속 축이 하나도 못 들면 R10 · R11 · R12 · R13 을 내지 않는다 (축 ① · ③ 만의 순위 금지) — 게이트 · 표시 · 무리만")
    chk(_b2_out_refused(SENS_SEALED["li"]) and _b2_out_refused(PROP / "x_readout.json") and not _b2_out_refused(PROP / "cascade_axes_bundle2_readout_x.json"),
        "⛔음성: 묶음 1 봉인 판독 · 'bundle2' 없는 이름에는 쓰지 않는다")
    # ── 묶음 1 재현 (상시 절차 — 고친 판독기로 과거 마감부터) ───────────────────────────────────
    sealed_r, bind = b2_sealed()
    rep = b2_b1_repro(sealed_r)
    chk(not bind and not rep["problems"] and rep["selection"] == ["V2O5"] and rep["selection_sensitivity"] == ["Sb2O5", "SiO2"],
        f"묶음 1 재현: 봉인 sha16 결속 · 축 ① · ② · ③ 판독 · 합치기 (선택 {rep['selection']}) · +U 민감도 (선택 {rep['selection_sensitivity']}) "
        f"를 지금 판독기로 그대로 ({len(rep['problems'])} 곳 다름)")
    with tempfile.TemporaryDirectory() as td:
        q = Path(td) / "ncm.json"
        q.write_text(B2_SEALED["ncm"][0].read_text(encoding="utf-8").replace('"G4"', '"G4" ', 1), encoding="utf-8")
        _, bind2 = b2_sealed({**B2_SEALED, "ncm": (q, B2_SEALED["ncm"][1])})
    chk(any("sha16" in x for x in bind2), "⛔음성 결속: 봉인 판독 파일이 한 글자라도 바뀌면 sha16 결속이 깨진다")
    print(f"bundle2 selftest: ⭕ {n[0]} · ⛔ {n[1]}")
    return 0 if ok_all else 1


def b1_repro_main(argv):
    """--bundle1_repro — 묶음 1 판독 (축 ① · ② · ③) · 합치기 (선택 V2O5) · +U 민감도 (Sb2O5 · SiO2) 를 지금 판독기로 재현해 보인다."""
    sealed, bind = b2_sealed()
    r = b2_b1_repro(sealed)
    print(f"봉인 결속 (sha16): {'⭕' if not bind else '⛔ ' + '; '.join(bind)}")
    print(f"재현: {'⭕ 다른 곳 0' if not r['problems'] else '⛔ ' + str(len(r['problems']))} · 선택 {r['selection']} · +U 민감도 선택 {r['selection_sensitivity']}")
    for x in r["problems"][:20]:
        print("   ", x)
    return 0 if not bind and not r["problems"] and r["selection"] == ["V2O5"] and r["selection_sensitivity"] == ["Sb2O5", "SiO2"] else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(max(ax_selftest(), hy_selftest(), li_selftest(), sens_selftest(), b2_selftest()))
    if "--bundle2" in sys.argv:
        raise SystemExit(b2_main(sys.argv))
    if "--bundle1_repro" in sys.argv:
        raise SystemExit(b1_repro_main(sys.argv))
    if "--sens_plusU_gap" in sys.argv:
        raise SystemExit(sens_main(sys.argv))
    if "--axis_ncm" in sys.argv:
        raise SystemExit(ax_main(sys.argv))
    if "--axis_hyd" in sys.argv:
        raise SystemExit(hy_main(sys.argv))
    if "--axis_li" in sys.argv:
        raise SystemExit(li_main(sys.argv))
    main()
