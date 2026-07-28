#!/usr/bin/env python3
"""build_screening_funnel.py — 문헌식 '순차 게이트 깔때기'로 cascade v23 도펀트를 재표현.

⚠ 정직성 선언 (이 파일의 존재 이유이자 한계):
  우리 47종은 **큐레이션된 후보군**이지 대규모 발견 풀이 아니다. Xiao 2019(104,082),
  Sendek 2017(12,831), Kahle 2020(15,855)는 DB 전수에서 출발한 *발견 깔때기*고,
  이 스크립트가 만드는 것은 **이미 선별된 47종을 문헌 표준 게이트 순서로 재표현한 뷰**다.
  "우리가 N만 개를 걸렀다"는 서술은 결함이다. 산출 JSON의 pool_provenance 블록이
  이 구분을 스스로 들고 다니게 설계했다 — 그 블록을 떼고 인용하지 말 것.

게이트 (G1–G5). G1–G4는 문헌 대응이 있고, G5(기계)는 문헌 3편 전부에 없는 우리 고유 축이다.
  G1 structural_stability  Δe < 0            ← Xiao F2 (E_hull<5 meV/atom) · Sendek 전제조건 (E_hull=0)
  G2 electrochemical_window window_V > 0.05 V ← Xiao F3 · Zhu 2015 grand-potential 원전
  G3 oxidation_onset       ox_V ≥ 2.14 V(host) ← Xiao F3의 V_ox≥4.0 V (단 우리는 host 상대)
  G4 li_transport          ionic_transport norm > 0.30 ← Xiao F6 (CI-NEB E_m) · Kahle pinball D 랭킹
  G5 mechanical            E ≤ median & G/B ≤ median   ← **문헌 대응 없음** (Kahle는 명시적으로 배제)

산출: db/properties/cascade_screening_funnel.json
결정론: 난수 없음, 표준 라이브러리만, 정렬된 리스트만 출력 → 2회 실행 md5 동일.
"""
import csv
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"
OUT = PROP / "cascade_screening_funnel.json"

BUILD_DATE = "2026-07-28"

# ── host 앵커 (임계값 유도의 물리적 기준점) ────────────────────────────────────
# oxidation_stability_cascade.csv 헤더 주석: "ref undoped: comp1/modelc ox=2.14 red=1.24 ocv=1.72"
HOST_OX_V = 2.14
# 같은 CSV 헤더: "collapse = window<0.05 V (avoid, late-TM Fe/Co/Ni/Mn)"
COLLAPSE_WINDOW_V = 0.05
# build_cascade_themes.py 의 ionic_transport 게이트 규약
BLOCKING_GATE = 0.60
GATE_FLOOR, GATE_EPS = 0.05, 0.05
# G4 컷 — 통과자 분포의 최대 공백(natural break)에서 취함. 근거는 threshold_sensitivity 블록에서 재확인.
TRANSPORT_CUT = 0.30


def read_csv_rows(path):
    with open(path) as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── 데이터 로드 + ionic_transport norm 재계산 ────────────────────────────────
def load_pool():
    ranked = read_csv_rows(PROP / "cascade_v23_ranked.csv")
    oxid = {r["dopant"]: r for r in read_csv_rows(PROP / "oxidation_stability_cascade.csv")}
    lit = {}
    for r in read_csv_rows(PROP / "cascade_v23_litransport.csv"):
        d, _, x = r["_dir"].rpartition("_x")
        lit.setdefault(d, {})[x] = r

    rows = []
    for r in ranked:
        d = r["dopant"]
        ox = oxid.get(d, {})
        l5 = lit.get(d, {}).get("005", {})
        rows.append({
            "dopant": d,
            "group": r.get("group"),
            "de": fnum(r.get("de")),
            "ox_V": fnum(ox.get("ox_V")) if ox else fnum(r.get("ox_V")),
            "window_V": fnum(ox.get("window_V")),
            "esw_note": (ox.get("note") or "").strip(),
            "bvs_x005": fnum(l5.get("bvs_li_proxy_score")),
            "blocking": fnum(l5.get("tier2_dopant_blocking_fraction")),
            "E_GPa": fnum(r.get("E_GPa")),
            "GoverB": fnum(r.get("pugh")),   # ⚠ 열 이름은 pugh 지만 값은 G/B (champions csv 유래)
            "score": fnum(r.get("score")),
        })

    # ionic_transport norm — build_cascade_themes.py 와 **같은 규약**을 여기서 재계산한다
    # (themes.json 의존을 피해 자기완결적으로 감사 가능하게 하되, 아래에서 값 일치를 강제 검증).
    vals = [r["bvs_x005"] for r in rows if r["bvs_x005"] is not None]
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    for r in rows:
        v = r["bvs_x005"]
        if v is None:
            r["transport_norm"] = None
            continue
        n = (v - lo) / span
        if (r["blocking"] if r["blocking"] is not None else 1.0) < BLOCKING_GATE:
            n = GATE_FLOOR + GATE_EPS + n * (1.0 - GATE_FLOOR - GATE_EPS)
        else:
            n = GATE_FLOOR
        r["transport_norm"] = round(n, 4)

    # 교차검증: 배포된 themes.json 과 한 종이라도 어긋나면 즉시 실패 (조용한 분기 금지)
    tpath = PROP / "cascade_v23_themes.json"
    if tpath.exists():
        ref = {t["dopant"]: t["norm"]["ionic_transport"] for t in json.load(open(tpath))["dopants"]}
        bad = [r["dopant"] for r in rows
               if r["dopant"] in ref and ref[r["dopant"]] != r["transport_norm"]]
        if bad:
            raise ValueError(f"ionic_transport norm 이 themes.json 과 불일치: {sorted(bad)} "
                             "— 두 빌더의 규약이 갈라졌다. 먼저 정합시킬 것.")
    return rows


# ── 게이트 정의 ──────────────────────────────────────────────────────────────
def build_gates(rows):
    e_med = statistics.median([r["E_GPa"] for r in rows if r["E_GPa"] is not None])
    gb_med = statistics.median([r["GoverB"] for r in rows if r["GoverB"] is not None])

    return {
        "G1": {
            "id": "G1",
            "name": "structural_stability",
            "label": "구조 안정 (도핑 형성 favorability)",
            "metric": "de = E(doped champion) − E(host), UMA 상대 (eV, cascade_v23_ranked.csv)",
            "threshold": "de < 0",
            "predicate": lambda r: r["de"] is not None and r["de"] < 0.0,
            "threshold_basis": (
                "0 은 임의 컷이 아니라 **host 자신**(Δe = doped − undoped baseline)이다 — "
                "'host보다 안정한가'라는 이분 질문의 물리적 기준점. 273-cascade 전체가 같은 "
                "undoped 정형셀 기준으로 계산돼 랭킹이 성립한다(kb/projects/cascade_v23_review_2026_07_11.md §1)."),
            "literature_analog": {
                "papers": ["xiao2019_cathode_coating_screening (Filter 2)",
                           "sendek2017_ml_screening_12k_conductors (전제조건 1)"],
                "their_threshold": "Xiao: E_hull < 0.005 eV/atom (절대 DFT hull) / Sendek: E_hull = 0 (엄격 절대)",
                "mapping": "'합성 가능한 만큼 안정한가'라는 같은 질문 — 좌표계만 절대 hull ↔ host 상대.",
            },
            "engine": "UMA(MLIP) 상대 에너지. 절대값 인용 금지(CLAUDE.md) — 부호/순위만 사용.",
        },
        "G2": {
            "id": "G2",
            "name": "electrochemical_window",
            "label": "전기화학 창 붕괴 회피",
            "metric": "window_V = ox_V − red_V (grand-potential ESW, MP GGA/GGA+U hull)",
            "threshold": f"window_V > {COLLAPSE_WINDOW_V} V",
            "predicate": lambda r: (r["window_V"] or 0.0) > COLLAPSE_WINDOW_V,
            "threshold_basis": (
                f"0.05 V 는 oxidation_stability_cascade.csv 가 이미 명문화한 **collapse 규약**"
                "('window<0.05 V = collapse, avoid, late-TM Fe/Co/Ni/Mn')이며 "
                "build_cascade_themes.py 의 oxidative/reduction 테마 게이트와 동일 상수다. "
                "이 빌더가 새로 만든 숫자가 아니라 기존 db 규약의 승계."),
            "literature_analog": {
                "papers": ["zhu2015_esw_grand_potential_origin (방법 원전)",
                           "xiao2019_cathode_coating_screening (Filter 3)"],
                "their_threshold": "Xiao: V_red ≤ 2.7 V & V_ox ≥ 4.0 V (창의 절대 위치 지정)",
                "mapping": ("Zhu 2015 의 μ_Li(φ) grand-potential 창을 그대로 쓰되, 문헌은 창의 "
                            "**위치**를 규정하고 우리는 창의 **존재**(붕괴 여부)를 본다."),
            },
            "engine": "MP hull 기반 절대 열역학 (UMA 무관) — 이 축만 절대값 인용 가능.",
        },
        "G3": {
            "id": "G3",
            "name": "oxidation_onset",
            "label": "산화 onset 비열화 (host 이상)",
            "metric": "ox_V (V vs Li, grand-potential onset)",
            "threshold": f"ox_V ≥ {HOST_OX_V} V (undoped host onset)",
            "predicate": lambda r: r["ox_V"] is not None and r["ox_V"] >= HOST_OX_V - 1e-9,
            "threshold_basis": (
                f"{HOST_OX_V} V = undoped comp1/modelc 의 grand-potential 산화 onset "
                "(oxidation_stability_cascade.csv 헤더에 명시된 ref). 즉 '도펀트를 넣어서 "
                "host보다 나빠지지 않는가'라는 상대 기준 — 임의 전압이 아니다. "
                "주의: 19종이 정확히 2.14 V에 pin 돼 있다(S²⁻-limited onset 축퇴) → "
                "이 게이트는 '초과'가 아니라 '비열화' 판정이며 축퇴군 내 순위는 무의미."),
            "literature_analog": {
                "papers": ["xiao2019_cathode_coating_screening (Filter 3, V_ox ≥ 4.0 V)",
                           "richards2016_interface_stability_pseudobinary (음이온이 onset을 결정)"],
                "their_threshold": "V_ox ≥ 4.0 V (양극 작동 상한 기준 절대 문턱)",
                "mapping": ("같은 grand-potential onset, 다른 좌표계. 그들은 코팅 물질이라 절대 4 V를 "
                            "넘을 수 있지만, 우리 host는 황화물(S²⁻-limited)이라 절대 4 V 게이트를 걸면 "
                            "생존자 0 — literature_absolute_variants 블록에서 실제로 계산해 보였다."),
            },
            "engine": "MP hull 기반 절대 열역학.",
        },
        "G4": {
            "id": "G4",
            "name": "li_transport",
            "label": "Li 수송 유지 (채널 미폐색)",
            "metric": ("ionic_transport norm ∈[0,1] = min-max(bvs_li_proxy_score @x=0.05) "
                       f"with blocking<{BLOCKING_GATE} 게이트, 탈락자 {GATE_FLOOR} 평탄화"),
            "threshold": f"transport_norm > {TRANSPORT_CUT}",
            "predicate": lambda r: (r["transport_norm"] or 0.0) > TRANSPORT_CUT,
            "threshold_basis": (
                "두 겹. ① blocking<0.60 은 build_cascade_themes.py 가 이미 쓰는 db 규약(승계). "
                "② 0.30 컷은 통과자 분포 **하위 꼬리의 공백 구간**(MoO3 0.2863 ↔ MnO 0.3844, 폭 0.098) "
                "안에 놓았다. ⚠ 정확히 말하면 이건 분포 전체의 최대 공백이 아니다"
                "(최대는 0.6842↔0.845 = 0.161, 그 다음이 0.1827↔0.2863 = 0.104, 이게 3번째). "
                "즉 '하위 꼬리를 자르는 자연스러운 위치 중 하나'이지 유일해가 아니다. "
                "host 앵커가 없는 축이라 G1–G3 만큼 강한 유도가 아님 → "
                "threshold_sensitivity.G4 스윕(코어 기준)을 반드시 함께 볼 것."),
            "literature_analog": {
                "papers": ["xiao2019_cathode_coating_screening (Filter 6, CI-NEB E_m)",
                           "kahle2020_ht_aimd_screening (pinball D(1000 K) 상위 200 → FPMD 132)"],
                "their_threshold": ("Xiao: E_m 절대 문턱 없이 대표 6종만 NEB 정밀 / "
                                    "Kahle: D 절대 문턱 대신 **랭킹 상위 200** 컷 + 검출하한 1e-8 cm²/s"),
                "mapping": ("문헌도 이 축만은 절대 문턱을 못 세우고 랭킹/선별로 처리했다 — "
                            "우리 natural-break 컷도 같은 성격(랭킹 컷)이다. Kahle 자신의 교훈: "
                            "surrogate(pinball)는 랭킹 분류기로만 유효하고 정량 D 재현엔 실패 "
                            "→ 우리 BVSE 프록시도 동일 지위, 절대 σ 로 읽지 말 것."),
            },
            "engine": "BVSE·기하 정적 프록시 (MD 아님). 챔피언만 MLIP-MD 로 별도 검증.",
        },
        "G5": {
            "id": "G5",
            "name": "mechanical",
            "label": "기계 (연질 + 연성) — 우리 고유 축",
            "metric": "E_young (GPa, UMA) ↓ AND G/B ↓ (champions csv elastic_pugh_GoverB)",
            "threshold": f"E_GPa ≤ {e_med:.4g} (roster median) AND G/B ≤ {gb_med:.4g} (roster median)",
            "predicate": (lambda r: (r["E_GPa"] is not None and r["GoverB"] is not None
                                     and r["E_GPa"] <= e_med + 1e-9 and r["GoverB"] <= gb_med + 1e-9)),
            "threshold_basis": (
                "⚠ **G1–G4 와 달리 host 앵커가 없다.** UMA 탄성값은 절대 인용 금지 규율 대상이고, "
                "같은 방법(UMA)으로 계산된 undoped host 의 E/(G/B) 항목이 cascade 산출물에 없다 "
                "(elastic.json 의 host 값은 DFT — 교차 인용 불가). 따라서 median split = "
                "**로스터 내부 상대 컷**이며 이 게이트만 자의성이 남는다(arbitrariness_flag). "
                "문헌 절대 기준(Pugh B/G > 1.75)을 걸면 생존자 0 — literature_absolute_variants 참조."),
            "literature_analog": {
                "papers": [],
                "their_threshold": None,
                "mapping": ("**대응 없음.** Xiao/Sendek 는 기계 축을 아예 안 봤고, Kahle 2020 은 "
                            "명시적으로 배제했다(p930: dendrite 억제는 결함 지배라 스크리닝 기준으로 "
                            "이해되지 않음). 즉 이 게이트는 우리가 문헌 대비 **추가**한 축이지 "
                            "문헌을 재현한 축이 아니다 — 서술 시 이 구분을 지킬 것. "
                            "(참고 문헌 앵커는 스크리닝이 아닌 물성 논문: deng2016_elastic_superionic_electrolytes_dft)"),
            },
            "engine": "UMA 상대 탄성 (E_VRH·G/B). 절대값 인용 금지.",
            "arbitrariness_flag": True,
        },
    }


REPRESENTATIVE_ORDER = ["G1", "G2", "G3", "G4", "G5"]

PERMUTATIONS = [
    {"key": "P0_literature_order", "order": ["G1", "G2", "G3", "G4", "G5"],
     "rationale": "대표 순서 — Xiao F2→F3→F6 의 열역학→전기화학→수송 순서에 우리 기계 축을 뒤에 붙임."},
    {"key": "P1_sendek_preconditions_first", "order": ["G1", "G3", "G2", "G5", "G4"],
     "rationale": "Sendek 2017: '전제조건(안정·gap·ESW)을 먼저, 전도도 모델을 마지막' — 수송을 맨 뒤로."},
    {"key": "P2_kahle_transport_first", "order": ["G4", "G1", "G2", "G3", "G5"],
     "rationale": "Kahle 2020: 확산(동역학) 자체를 1차 스크리닝 변수로 — 수송을 맨 앞으로."},
    {"key": "P3_our_mechanics_first", "order": ["G5", "G4", "G3", "G2", "G1"],
     "rationale": "우리 고유 축(기계) 우선 — 저탄성 soft-contact 코팅이 1차 목표였던 v23 2차 목적 순서."},
]


def run_sequence(rows, gates, order):
    alive = list(rows)
    steps = []
    for gid in order:
        g = gates[gid]
        passed = [r for r in alive if g["predicate"](r)]
        failed = [r for r in alive if not g["predicate"](r)]
        steps.append({
            "gate": gid,
            "gate_name": g["name"],
            "n_in": len(alive),
            "n_pass": len(passed),
            "n_fail": len(failed),
            "failed_here": sorted(r["dopant"] for r in failed),
            "vacuous": len(failed) == 0,
        })
        alive = passed
    return steps, sorted(r["dopant"] for r in alive)


def main():
    rows = load_pool()
    gates = build_gates(rows)
    pool_names = sorted(r["dopant"] for r in rows)
    by_name = {r["dopant"]: r for r in rows}

    # ── 게이트별 블록 (대표 순서 기준 + standalone) ──────────────────────────
    steps, survivors = run_sequence(rows, gates, REPRESENTATIVE_ORDER)
    step_by_gid = {s["gate"]: s for s in steps}

    gate_blocks = []
    for gid in REPRESENTATIVE_ORDER:
        g = gates[gid]
        s = step_by_gid[gid]
        standalone_fail = sorted(r["dopant"] for r in rows if not g["predicate"](r))
        vac_interp = None
        if s["vacuous"]:
            vac_interp = (
                f"⚠ VACUOUS — 대표 순서에서 이 게이트에 들어온 {s['n_in']}종이 전원 통과했다. "
                "이는 '우리가 이 조건으로 걸렀다'가 아니라 **우리 풀이 이미 그 조건을 만족하도록 "
                "큐레이션돼 있었다**는 뜻이다. 문헌 깔때기에서는 같은 게이트가 수천~수만 종을 "
                "떨어뜨린다(Xiao F2: 62,437→1,600 = 97.4% 제거; Sendek E_hull=0: 12,831→1,472 = 88.5% 제거). "
                "발견력의 증거로 인용하면 과장이다.")
        elif len(standalone_fail) == 0:
            vac_interp = "standalone 으로도 전원 통과 — 사실상 무효 게이트."
        gate_blocks.append({
            "id": gid,
            "name": g["name"],
            "label": g["label"],
            "metric": g["metric"],
            "threshold": g["threshold"],
            "threshold_basis": g["threshold_basis"],
            "literature_analog": g["literature_analog"],
            "engine": g["engine"],
            "arbitrariness_flag": g.get("arbitrariness_flag", False),
            "in_representative_order": {
                "n_in": s["n_in"], "n_pass": s["n_pass"], "n_fail": s["n_fail"],
                "eliminated_here": s["failed_here"],
            },
            "standalone": {
                "n_pass": len(rows) - len(standalone_fail),
                "n_fail": len(standalone_fail),
                "eliminated": standalone_fail,
            },
            "vacuous": s["vacuous"],
            "vacuous_interpretation": vac_interp,
        })

    # ── 게이트 위력/중복 분석 ────────────────────────────────────────────────
    fail_sets = {gid: {r["dopant"] for r in rows if not gates[gid]["predicate"](r)}
                 for gid in REPRESENTATIVE_ORDER}
    power = []
    for gid in REPRESENTATIVE_ORDER:
        others = set().union(*[fail_sets[o] for o in REPRESENTATIVE_ORDER if o != gid])
        unique = sorted(fail_sets[gid] - others)
        without = [r for r in rows
                   if all(gates[o]["predicate"](r) for o in REPRESENTATIVE_ORDER if o != gid)]
        power.append({
            "gate": gid,
            "name": gates[gid]["name"],
            "standalone_kill": len(fail_sets[gid]),
            "marginal_kill_in_P0": step_by_gid[gid]["n_fail"],
            "unique_kill": len(unique),
            "unique_kill_list": unique,
            "survivors_if_gate_removed": len(without),
            "redundant_given_others": len(unique) == 0,
        })

    # ── 순서 민감도 ──────────────────────────────────────────────────────────
    perms = []
    for p in PERMUTATIONS:
        st, surv = run_sequence(rows, gates, p["order"])
        perms.append({
            "key": p["key"], "order": p["order"], "rationale": p["rationale"],
            "waterfall": [len(rows)] + [s["n_pass"] for s in st],
            "steps": [{"gate": s["gate"], "n_in": s["n_in"], "n_pass": s["n_pass"],
                       "n_fail": s["n_fail"], "vacuous": s["vacuous"]} for s in st],
            "final_survivors": surv,
        })
    all_sets = [set(p["final_survivors"]) for p in perms]
    identical = all(s == all_sets[0] for s in all_sets)
    inter = sorted(set.intersection(*all_sets))
    union = sorted(set.union(*all_sets))

    order_sensitivity = {
        "permutations": perms,
        "final_sets_identical": identical,
        "intersection": inter,
        "union": union,
        "symmetric_difference": sorted(set(union) - set(inter)),
        "why": ("게이트가 전부 **정적·per-dopant boolean 술어**라 최종 생존자는 집합 교집합이고 "
                "순서에 불변이다. 순서가 바꾸는 것은 (a) 중간 단계 숫자(깔때기 그림의 모양)와 "
                "(b) 어느 게이트에 탈락의 '공'이 돌아가는가(marginal kill)뿐 — "
                "이 불변성은 주장이 아니라 위 4개 순열에서 실제로 계산해 확인했다."),
        "sendek_analog_verdict": (
            "Sendek 2017 은 '전제조건(안정·gap·ESW)이 전도도 모델보다 세게 거른다'고 결론했다"
            "(전제조건 12,831→317 vs LR 모델 단독 12,831→1,408). **우리 풀에서는 정반대다**: "
            f"standalone 제거 수 = G1 {len(fail_sets['G1'])} · G2 {len(fail_sets['G2'])} · "
            f"G3 {len(fail_sets['G3'])} · G4 {len(fail_sets['G4'])} · G5 {len(fail_sets['G5'])} "
            "→ 수송(G4)이 최강 단일 필터이고 안정성(G1)은 아무도 못 떨어뜨린다. "
            "이 역전은 우리 풀의 성질에서 온다 — 47종은 애초에 '넣을 만한' 도펀트로 큐레이션돼 "
            "안정성·ESW 전제조건을 이미 통과한 상태로 시작하므로, 남은 구속조건이 수송으로 옮겨간다. "
            "즉 Sendek 명제의 반증이 아니라 **'전제조건이 이미 소진된 풀에서는 축이 이동한다'는 따름정리**다."),
    }

    # ── 임계값 민감도 스윕 ───────────────────────────────────────────────────
    # ⚠ 스윕은 **코어(G1–G4)** 기준으로 읽는다. G5 를 함께 걸면 median 컷이 결과를 지배해
    #   다른 게이트의 민감도가 전부 가려진다(실제로 전 스윕이 WO3 하나로 붕괴). 두 값을 병기한다.
    CORE = ["G1", "G2", "G3", "G4"]

    def survivors_with(overrides, order=REPRESENTATIVE_ORDER):
        preds = [overrides.get(gid, gates[gid]["predicate"]) for gid in order]
        return sorted(r["dopant"] for r in rows if all(p(r) for p in preds))

    g4_sweep = []
    for cut in [0.05, 0.10, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]:
        ov = {"G4": (lambda r, c=cut: (r["transport_norm"] or 0.0) > c)}
        core = survivors_with(ov, CORE)
        g4_sweep.append({"cut": cut, "n_core_G1_G4": len(core), "core_survivors": core,
                         "n_full_with_G5": len(survivors_with(ov))})

    e_sorted = sorted(r["E_GPa"] for r in rows if r["E_GPa"] is not None)
    gb_sorted = sorted(r["GoverB"] for r in rows if r["GoverB"] is not None)

    def pct(vals, q):
        i = max(0, min(len(vals) - 1, int(round(q * (len(vals) - 1)))))
        return vals[i]

    g5_sweep = []
    for q in [0.25, 0.40, 0.50, 0.60, 0.75, 1.00]:
        ecut, gcut = pct(e_sorted, q), pct(gb_sorted, q)
        s = survivors_with({"G5": (lambda r, e=ecut, g=gcut:
                                   r["E_GPa"] is not None and r["GoverB"] is not None
                                   and r["E_GPa"] <= e + 1e-9 and r["GoverB"] <= g + 1e-9)})
        g5_sweep.append({"percentile": q, "E_cut_GPa": round(ecut, 4),
                         "GoverB_cut": round(gcut, 4), "n_final": len(s), "survivors": s})

    g3_sweep = []
    for off in [-0.20, -0.10, -0.05, 0.0, 0.05, 0.10]:
        cut = HOST_OX_V + off
        ov = {"G3": (lambda r, c=cut: r["ox_V"] is not None and r["ox_V"] >= c - 1e-9)}
        core = survivors_with(ov, CORE)
        g3_sweep.append({"offset_vs_host_V": off, "ox_cut_V": round(cut, 4),
                         "n_core_G1_G4": len(core), "core_survivors": core,
                         "n_full_with_G5": len(survivors_with(ov))})

    # 통과자 분포의 natural break 근거 (G4)
    passers = sorted([r["transport_norm"] for r in rows
                      if (r["transport_norm"] or 0.0) > GATE_FLOOR], reverse=True)
    gaps = sorted(((round(passers[i] - passers[i + 1], 4), passers[i + 1], passers[i])
                   for i in range(len(passers) - 1)), reverse=True)[:3]

    threshold_sensitivity = {
        "how_to_read": ("G3·G4 스윕은 **n_core_G1_G4**(문헌 대응 코어)를 보라. G5 를 함께 걸면 "
                        "median 컷이 결과를 지배해 다른 축의 민감도가 전부 가려진다 "
                        "(n_full_with_G5 열이 그 붕괴를 보여준다)."),
        "G3_oxidation_onset": {"sweep": g3_sweep,
                               "note": ("host 2.14 V 앵커에서 ±0.2 V 이동. onset 축퇴(19종 @2.14 V) 때문에 "
                                        "+0.05 V 만 올려도 코어 생존자가 급감하는 **계단 함수** — "
                                        "'host 이상'이라는 판정 자체는 견고하지만 '얼마나 이상'은 해상도가 없다.")},
        "G4_li_transport": {"sweep": g4_sweep,
                            "largest_gaps_in_passer_distribution":
                                [{"gap": g, "below": lo, "above": hi} for g, lo, hi in gaps],
                            "note": ("0.30 컷은 0.2863–0.3844 공백 안에 있어 ±0.05 이동에 코어 생존자 집합이 "
                                     "불변이다(0.25 로 내리면 MoO3 가 복귀). 자의적이지만 국소적으로 안정.")},
        "G5_mechanical": {"sweep": g5_sweep,
                          "note": ("percentile 1.00 = 게이트 무효화 → G1–G4 코어 생존자 11종과 동일. "
                                   "0.25→1.00 사이에서 최종 생존자가 0→11 로 전 구간을 훑는다 = "
                                   "**최종 숫자가 이 컷 하나에 지배됨**. G5 결과를 결론처럼 인용하지 말 것.")},
    }

    # ── 문헌 절대 임계값을 그대로 걸어본 변형 (정직성 진단) ──────────────────
    lit_variants = [
        {"variant": "xiao_absolute_V_ox_ge_4.0V",
         "gate": "G3", "threshold": "ox_V ≥ 4.0 V (Xiao 2019 Filter 3 원문 값)",
         "n_pass_standalone": sum(1 for r in rows if (r["ox_V"] or 0) >= 4.0),
         "verdict": ("생존자 0 = **empty gate**. 황화물 SE의 grand-potential 산화 onset은 "
                     "구조적으로 ~2.0–2.5 V(Zhu 2015: LPSCl 1.71–2.01 V; 우리 host 2.14 V)라 "
                     "코팅 물질용 절대 문턱을 도펀트 스크린에 이식하면 전멸한다. "
                     "→ G3 을 host 상대로 재정의한 이유의 정량 근거.")},
        {"variant": "pugh_absolute_BoverG_gt_1.75",
         "gate": "G5", "threshold": "Pugh B/G > 1.75 (연성 경험칙; 우리 열은 G/B → G/B < 0.5714)",
         "n_pass_standalone": sum(1 for r in rows if (r["GoverB"] or 9) < 0.5714),
         "verdict": ("생존자 0 = **empty gate**. 로스터 G/B 범위 "
                     f"{min(gb_sorted):.2f}–{max(gb_sorted):.2f} (B/G {1/max(gb_sorted):.2f}–{1/min(gb_sorted):.2f}) "
                     "→ 47종 어느 것도 연성 경험칙을 못 넘는다(themes.json ductility caveat과 동일 사실). "
                     "따라서 G5 는 절대 기준이 아니라 로스터 내부 상대 컷일 수밖에 없다.")},
        {"variant": "xiao_absolute_E_hull_lt_5meV",
         "gate": "G1", "threshold": "E_hull < 5 meV/atom (절대 hull)",
         "n_pass_standalone": None,
         "verdict": ("계산 불가 — cascade 47종에는 도핑 챔피언의 **절대 E_hull 이 없다**"
                     "(UMA 상대 Δe 만 존재; e-hull 은 Nd₂O₃/B₂O₃ 등 승격 후보에만). "
                     "'우리가 문헌 게이트를 재현했다'가 아니라 '대응 축을 상대 좌표로 대체했다'가 정확한 서술.")},
    ]

    # ── 전자절연 진단 (게이트 아님) ──────────────────────────────────────────
    # Xiao F1(Eg>0.5 eV)·Sendek(Eg≥1 eV)에 대응하는 축을 우리는 게이트로 쓰지 않는다
    # (47종 전수의 우리 계산 gap 이 없고, themes.json 의 gap_lit_eV 는 문헌 전형값 큐레이션이라
    #  게이트로 쓰면 "우리 계산으로 걸렀다"는 오독을 만든다). 대신 **사후 진단**으로만 붙인다.
    core_names = sorted(r["dopant"] for r in rows
                        if all(gates[g]["predicate"](r) for g in ["G1", "G2", "G3", "G4"]))
    gap_lit = {}
    tpath = PROP / "cascade_v23_themes.json"
    if tpath.exists():
        gap_lit = {t["dopant"]: t.get("gap_lit_eV") for t in json.load(open(tpath))["dopants"]}
    diag_rows = sorted(({"dopant": n, "gap_lit_eV": gap_lit.get(n)} for n in core_names),
                       key=lambda d: (d["gap_lit_eV"] is None, d["gap_lit_eV"], d["dopant"]))
    ei_diagnostic = {
        "status": "DIAGNOSTIC_ONLY — 게이트 아님",
        "why_not_a_gate": ("① 47종 전수의 우리 계산 gap 이 없다(canonical gap 은 fixed-occ nscf 로 "
                           "host/챔피언 소수만). ② themes.json 의 gap_lit_eV 는 문헌 전형값 ±0.5 eV 큐레이션 "
                           "— 게이트로 쓰면 큐레이션 값이 스크리닝 결과를 만든 것처럼 보인다."),
        "core_survivors_gap_lit_eV": diag_rows,
        "if_applied": {
            "xiao_F1_gap_gt_0.5eV": sum(1 for d in diag_rows
                                        if d["gap_lit_eV"] is not None and d["gap_lit_eV"] > 0.5),
            "sendek_gap_ge_1eV": sum(1 for d in diag_rows
                                     if d["gap_lit_eV"] is not None and d["gap_lit_eV"] >= 1.0),
            "verdict": ("코어 생존자 전원이 두 문헌 문턱을 통과 → 이 축을 넣어도 **또 하나의 vacuous 게이트**가 "
                        "될 뿐이다. 다만 절대 수준은 갈린다(불화물 10–14 eV vs Ag₂O 1.3 · WO₃ 2.7 eV) — "
                        "'통과'와 '안심'은 다르며, 후기 TM/d⁰ 산화물 생존자는 전자 누설 관점에서 별도 검토 대상."),
        },
    }

    # ── 문헌 대비표 ──────────────────────────────────────────────────────────
    lit_table = [
        {"axis": "풀 크기 / 성격",
         "literature": ("Xiao 2019 104,082 (ICSD+data-mined, Li-함유) → 62,437 → 1,600 → 302 → 184 → 66 → 3 / "
                        "Sendek 2017 12,831 (MP Li-함유) → 317 → 21 / "
                        "Kahle 2020 15,855 entries → 4,963 unique → 1,362 → 1,016 → 796 → FPMD 132 → 5"),
         "ours": "47 (큐레이션 도펀트 후보군) → 43 → 25 → 11 → G5 적용 후 최종",
         "difference_reason": ("근본적으로 다른 물건. 문헌 셋은 **발견 깔때기**(DB 전수에서 미지 물질 발굴), "
                               "우리는 **재표현 뷰**(이미 고른 47종을 문헌 게이트 순서로 다시 그림). "
                               "다만 Ong 2013(11 조성)·Fujimura 2013(92 조성) 같은 **조성족 스캔** 계보로 보면 "
                               "47은 정상 체급 — 우리 위치는 그쪽이다.")},
        {"axis": "구조 안정",
         "literature": "Xiao F2: E_hull < 5 meV/atom (절대) · Sendek: E_hull = 0 (절대, 최강 단일 필터 88.5% 제거)",
         "ours": "G1: Δe < 0 (host 상대, UMA)",
         "difference_reason": ("① 절대 hull 을 47종 도핑 챔피언에 대해 계산하지 않았다(UMA 상대 Δe 만 보유). "
                               "② 애초에 질문이 다르다 — 문헌은 '이 물질이 존재 가능한가', 우리는 "
                               "'이 도펀트가 host 를 안정화하는가'. ③ 결과적으로 우리 게이트는 vacuous(47/47).")},
        {"axis": "전기화학 창",
         "literature": "Xiao F3: V_ox ≥ 4.0 & V_red ≤ 2.7 V (Zhu 2015 grand-potential 그대로)",
         "ours": "G2: window > 0.05 V (붕괴 회피) + G3: ox_V ≥ 2.14 V (host)",
         "difference_reason": ("같은 grand-potential 방법(Zhu 2015 직계), 다른 좌표계. 황화물 host는 "
                               "S²⁻-limited 라 onset 이 2.14 V 에 pin 되고 도펀트가 이를 크게 못 옮긴다 "
                               "→ 절대 4 V 문턱은 empty gate(위 lit_variants 에서 실측). "
                               "대신 우리는 '창 붕괴(late-TM)'와 'onset 비열화'라는 두 개의 상대 판정으로 분해.")},
        {"axis": "화학 반응성 (계면)",
         "literature": "Xiao F4: |ΔE_rxt| < 100 meV/atom vs Li₃PS₄ & 만충 NCM (Richards 2016 pseudo-binary)",
         "ours": "게이트 없음 (공백)",
         "difference_reason": ("우리 interface_reactivity 는 vs LCO 만 있고 47종 전수 ΔE_rxt 가 없다. "
                               "**문헌에 있고 우리에 없는 축** — 향후 추가 1순위.")},
        {"axis": "Li 수송",
         "literature": ("Xiao F6: CI-NEB vacancy E_m, 대표 6/66 종만 / "
                        "Kahle: pinball D(1000 K) 랭킹 상위 200 → FPMD 132, 검출하한 1e-8 cm²/s"),
         "ours": "G4: BVSE Li proxy norm > 0.30 (47종 전수) + blocking < 0.60",
         "difference_reason": ("문헌도 절대 문턱을 못 세우고 랭킹 컷을 썼다(공통). 차이는 비용 배분 — "
                               "그들은 소수만 정밀(NEB/FPMD), 우리는 전수 프록시(BVSE) + 챔피언만 MLIP-MD. "
                               "Kahle 의 자기검증(surrogate는 랭킹용, 값은 상위 이론으로)이 우리 BVSE 에 그대로 적용된다.")},
        {"axis": "전자 절연",
         "literature": "Xiao F1: KS gap > 0.5 eV (하한으로만) · Sendek: E_gap ≥ 1 eV · Kahle: PBE 점유 기준 절연 판정",
         "ours": "게이트 없음 (host 가 wide-gap 2.1 eV 전제; gap_lit_eV 는 큐레이션 문헌값이라 게이트 부적격)",
         "difference_reason": ("우리 canonical gap 은 fixed-occ nscf 로 host/champion 소수만 있고 47종 전수가 없다. "
                               "themes.json 의 gap_lit_eV 는 문헌 전형값 큐레이션 — 게이트로 쓰면 "
                               "'우리 계산으로 걸렀다'는 오독을 만든다. 의도적 미채택.")},
        {"axis": "기계",
         "literature": "**없음**. Kahle 2020 은 명시 배제(p930), Xiao·Sendek 은 축 자체가 없음",
         "ours": "G5: E ≤ median AND G/B ≤ median (UMA 상대)",
         "difference_reason": "우리가 추가한 축. 문헌 재현이 아니라 **확장**이며, host 앵커가 없어 유일하게 자의적.",
         },
        {"axis": "스코어링 철학",
         "literature": "순차 hard gate → 통과/탈락 (경계값 정보 소실)",
         "ours": "본체는 가중합 score(0.30 ox + 0.25 stable + 0.20 soft + 0.15 ductile + 0.10 window); 이 깔때기는 **부가 뷰**",
         "difference_reason": ("우리 1차 산출물은 랭킹이고 깔때기는 문헌 대조를 위한 사후 재표현이다. "
                               "깔때기 숫자를 우리 방법론의 정의처럼 인용하면 안 된다.")},
    ]

    # ── pool provenance ─────────────────────────────────────────────────────
    pool_provenance = {
        "pool_size": len(rows),
        "what_it_is": ("**큐레이션된 도펀트 후보군**. 화학적 사전지식(코팅 문헌·합성 전구체·발란스 다양성)으로 "
                       "사람이 고른 목록이지, 어떤 DB를 전수로 훑어 남은 잔존군이 아니다."),
        "selection_history": [
            "Round 1/2 reviewer 권장 = oxide 9–12종 (화학 일관성·Sundar 2025 코팅 문헌 근거)",
            "사용자 지적('ZrCl4·LiBr 같은 non-oxide 후보가 많다')으로 4-카테고리 22종으로 확장 "
            "(kb/projects/MULTI_CATEGORY_BATCH_PLAN_v22.md)",
            "master_batch_273.sh (v4.5.20) 로 91 화합물 × 농도 3종(x=0.02/0.05/0.10) = 273 cascade 실행 "
            "(kb/projects/cascade_v23_review_2026_07_11.md: 273/273 완료)",
            "그 중 ESW·탄성·BVSE 3축이 모두 채워진 47종이 cascade_v23_ranked.csv 에 등재 = 이 풀",
        ],
        "attrition_is_not_screening": (
            "91 → 47 의 감소는 **물리 게이트가 아니라 파이프라인 탈락**이다(구조 seed 생성 실패 등, "
            "예: As₂S₃ 3종은 stage-01 n_structures=0 으로 정직 종료). "
            "이 44종은 '떨어뜨린' 것이 아니라 '판정하지 못한' 것 — 깔때기 숫자에 합산하면 안 된다."),
        "literature_pool_comparison": {
            "discovery_funnels_we_are_NOT": {
                "xiao2019_cathode_coating_screening": "104,082 (ICSD + data-mined 치환 신조성, Li-함유)",
                "sendek2017_ml_screening_12k_conductors": "12,831 (MP 2016 스냅샷 Li-함유)",
                "kahle2020_ht_aimd_screening": "15,855 entries → 4,963 unique (ICSD+COD)",
            },
            "family_scans_we_ARE_LIKE": {
                "ong2013_lgps_family_substitution": "11 조성 (LGPS 골격 M×X 치환족)",
                "fujimura2013_ml_conductivity_origin": "92 조성 (γ-LISICON 족) + 실험 σ 95점",
            },
            "verdict": ("47은 발견 깔때기 체급이 아니라 **조성족 스캔** 체급이다(Ong 11 < 우리 47 < Fujimura 92). "
                        "이 계보로 위치를 잡으면 정직하면서도 문헌적으로 정당하다."),
        },
        "not_a_discovery_funnel": (
            "❗ 이 JSON의 게이트 통과 수는 **발견 성능 지표가 아니다**. 'N만 개에서 걸러냈다'는 서술은 "
            "우리 데이터로 지지되지 않는다. 정확한 서술: "
            "'큐레이션된 47종 도펀트 후보를 문헌(Xiao/Sendek/Kahle) 표준 게이트 순서로 재표현하면 "
            "어디서 몇 종이 떨어지는지를 보인 뷰'."),
        "related_but_different_funnel": (
            "kb/methodology/dopant_screening_funnel_2026_06_13.md 는 **한 도펀트 내부의 배치(config) 깔때기**"
            "(Nd₂O₃ 342 configs → cfg141)다. 여기 깔때기는 **도펀트 종(species) 수준** — 층이 다르니 "
            "두 숫자를 섞어 '수백 종을 걸렀다'로 합치지 말 것."),
    }

    out = {
        "property": "cascade_screening_funnel",
        "date": BUILD_DATE,
        "description": ("cascade v23 도펀트 47종을 문헌 표준(Xiao 2019 F1–F6 · Sendek 2017 전제조건→ML · "
                        "Kahle 2020 pinball→FPMD)의 순차 게이트 깔때기로 재표현한 뷰. "
                        "게이트별 통과/탈락 명단·임계값 근거·문헌 대응, vacuous 게이트 플래그, "
                        "게이트 순서 민감도, 문헌 대비표를 포함."),
        "honesty_header": pool_provenance["not_a_discovery_funnel"],
        "pool_provenance": pool_provenance,
        "host_anchors": {
            "host_ox_V": HOST_OX_V,
            "collapse_window_V": COLLAPSE_WINDOW_V,
            "blocking_gate": BLOCKING_GATE,
            "note": ("G1·G2·G3 의 임계값은 전부 host 값 또는 기존 db 규약에서 나왔다(새 상수 없음). "
                     "G4 는 db 규약(blocking) + 분포 natural break, G5 만 로스터 median = 자의적."),
        },
        "representative_order": REPRESENTATIVE_ORDER,
        "waterfall": {
            "counts": [len(rows)] + [s["n_pass"] for s in steps],
            "labels": ["pool(curated 47)"] + [f"{s['gate']} {gates[s['gate']]['name']}" for s in steps],
        },
        "gates": gate_blocks,
        "literature_comparable_endpoint": {
            "gate": "G4",
            "n": len(core_names),
            "survivors": core_names,
            "why": ("G1–G4 만이 문헌(Xiao/Sendek/Kahle) 게이트에 대응한다. 문헌과 나란히 인용할 숫자는 "
                    "**여기까지**(47 → 43 → 25 → 11)다. G5 는 우리가 추가한 축이라 문헌 대비에 넣으면 "
                    "사과와 오렌지가 된다."),
        },
        "final_survivors": survivors,
        "final_survivors_warning": (
            f"G5 까지 걸면 {len(survivors)}종({', '.join(survivors)})만 남지만 이는 **결론이 아니다**. "
            "G5 의 median 컷은 host 앵커가 없는 자의적 컷이고, percentile 을 0.25→1.00 으로 훑으면 "
            "최종 생존자가 0→11 로 전 구간을 움직인다(threshold_sensitivity.G5_mechanical). "
            "'우리 깔때기의 최종 승자'로 인용하지 말 것 — 인용할 숫자는 "
            "literature_comparable_endpoint(11종)이고, G5 는 그 11종을 기계 축으로 정렬한 부가 정보다."),
        "electronic_insulation_diagnostic": ei_diagnostic,
        "survivors_before_G5": core_names,
        "gate_power": {
            "rows": power,
            "reading": ("standalone_kill = 그 게이트만 47종에 걸었을 때 탈락 수 (그 축의 선택압). "
                        "marginal_kill_in_P0 = 대표 순서에서 실제로 그 게이트가 떨어뜨린 수(앞 게이트에 "
                        "이미 잡힌 것 제외). unique_kill = 그 게이트가 없으면 최종 생존자로 살아 돌아올 종 수 "
                        "→ 0 이면 다른 게이트에 완전히 포섭된 **중복 게이트**."),
        },
        "order_sensitivity": order_sensitivity,
        "threshold_sensitivity": threshold_sensitivity,
        "literature_absolute_variants": lit_variants,
        "literature_comparison_table": lit_table,
        "caveats": [
            "게이트 통과 수는 발견 성능이 아니다 (pool_provenance 참조).",
            "G1 은 vacuous(47/47) — 우리 풀이 그 조건으로 이미 큐레이션됐다는 뜻.",
            "G2 는 unique_kill 을 확인할 것 — 우리 풀에서 window collapse 4종이 전부 late-TM 이라 "
            "G3(ox onset)에 완전히 포섭된다.",
            "G3 의 ox_V 는 19종이 2.14 V 에 축퇴(S²⁻-limited) — 통과/탈락 판정만 유효, 축퇴군 내 순위 무의미.",
            "G4 의 BVSE proxy 는 정적 기하 프록시다. 절대 σ·D 로 읽지 말 것; MLIP-MD 절대값 인용 금지 규율 유지.",
            "G5 의 E·G/B 는 UMA 상대값 — 절대 인용 금지. 로스터 median 컷이라 유일하게 자의적(arbitrariness_flag). "
            "게다가 이 컷 하나가 최종 숫자를 지배한다 → 문헌 대비 인용은 G4 까지(11종)로 끊을 것.",
            "전자절연·계면 반응성 두 축은 문헌에 있고 우리 게이트엔 없다 — '문헌 게이트를 전부 재현했다'고 "
            "쓰면 틀린다(electronic_insulation_diagnostic · literature_comparison_table 참조).",
            "문헌 수치(104,082 / 12,831 / 15,855 등)는 소환값이며 우리 db 값과 섞어 계산하지 않았다.",
        ],
        "source_files": ["db/properties/cascade_v23_ranked.csv",
                         "db/properties/oxidation_stability_cascade.csv",
                         "db/properties/cascade_v23_litransport.csv",
                         "db/properties/cascade_v23_themes.json (norm 교차검증용)"],
        "literature_sources": ["litdb/papers/xiao2019_cathode_coating_screening.md",
                               "litdb/papers/sendek2017_ml_screening_12k_conductors.md",
                               "litdb/papers/kahle2020_ht_aimd_screening.md",
                               "litdb/papers/zhu2015_esw_grand_potential_origin.md",
                               "litdb/papers/richards2016_interface_stability_pseudobinary.md",
                               "litdb/papers/ong2013_lgps_family_substitution.md",
                               "litdb/papers/fujimura2013_ml_conductivity_origin.md"],
        "pool": [{"dopant": r["dopant"], "group": r["group"], "de": r["de"], "ox_V": r["ox_V"],
                  "window_V": r["window_V"], "transport_norm": r["transport_norm"],
                  "blocking": r["blocking"], "E_GPa": r["E_GPa"], "GoverB": r["GoverB"],
                  "esw_note": r["esw_note"],
                  "gates_passed": [g for g in REPRESENTATIVE_ORDER if gates[g]["predicate"](r)],
                  "gates_failed": [g for g in REPRESENTATIVE_ORDER if not gates[g]["predicate"](r)]}
                 for r in sorted(rows, key=lambda x: x["dopant"])],
        "pool_names": pool_names,
    }

    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1, sort_keys=False)
    open(OUT, "a").write("\n")

    md5 = hashlib.md5(OUT.read_bytes()).hexdigest()
    print(f"[funnel] {OUT}  md5={md5}")
    print(f"  waterfall {out['waterfall']['counts']}  ({' → '.join(out['waterfall']['labels'])})")
    for g in gate_blocks:
        v = " [VACUOUS]" if g["vacuous"] else ""
        print(f"  {g['id']} {g['name']:<22} in {g['in_representative_order']['n_in']:>2} "
              f"→ pass {g['in_representative_order']['n_pass']:>2} "
              f"(standalone kill {g['standalone']['n_fail']:>2}){v}")
    for p in power:
        print(f"    power {p['gate']}: standalone {p['standalone_kill']:>2} · "
              f"marginal {p['marginal_kill_in_P0']:>2} · unique {p['unique_kill']:>2} "
              f"{'(REDUNDANT)' if p['redundant_given_others'] else ''}")
    print(f"  ★ literature-comparable endpoint = G4 ({len(core_names)}): {', '.join(core_names)}")
    print(f"  final after G5 ({len(survivors)}): {', '.join(survivors)}  "
          f"[⚠ G5 median 컷이 지배 — 결론으로 인용 금지]")
    print(f"  order sensitivity: final sets identical = {identical}; "
          f"waterfalls = " + " | ".join(f"{p['key']}:{p['waterfall']}" for p in perms))


if __name__ == "__main__":
    main()
