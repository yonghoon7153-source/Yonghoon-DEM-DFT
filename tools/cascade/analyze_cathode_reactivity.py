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
"""
import csv
import json
import re
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


if __name__ == "__main__":
    main()
