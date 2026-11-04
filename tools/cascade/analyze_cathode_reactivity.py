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
    if set(el) & AX_TM_U:
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


def ax_design_class(row, tracked, gaps):
    """한 행 (설계 × 양극 상태) → (등급, 세부). 우선순위 ⓑ 금속성 > ⓐ 넓은 갭 > ⓓ 미판정 > ⓒ 중간 · ⓔ 끝점 · ㉧ 추적 원소 없음."""
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
            c, w = ax_product_class(f, gaps)
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


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(ax_selftest())
    if "--axis_ncm" in sys.argv:
        raise SystemExit(ax_main(sys.argv))
    main()
