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

--audit_raw <캠페인루트>  (2026-08-13 추가)
  이 파일은 "91 → 47 은 물리 게이트가 아니라 파이프라인 탈락" 이라고 **주장**하는데,
  정작 그 근거인 원자료(273 실행 디렉터리)는 repo 에 없다. 세미나에서 "왜 염화물이
  0/19 냐" 를 물으면 CSV 요약을 되읽는 것 말고 답할 게 없었다.
  이 모드는 gabia 의 캠페인 루트를 훑어 **종별로 어느 축이 비었는지**를 세고
  계열별로 집계한다. 판정을 만들지 않고 파일 존재 여부만 센다.

  python3 tools/cascade/build_screening_funnel.py --audit_raw /data/work/runs/multi_category_2026_05_26_v23
  python3 tools/cascade/build_screening_funnel.py --selftest

이 도구가 못 하는 것
  · 축이 빈 **이유**를 말하지 못한다 — 로그를 읽지 않고 산출물 유무만 본다.
    (n_structures=0 처럼 stage-01 이 정직 종료한 경우만 예외적으로 집어낸다.)
  · 원자료가 없는 종에 대해서는 아무 말도 하지 않는다. 없는 것은 없다고 찍는다.
"""
import csv
import hashlib
import itertools
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"
# 경로 env 오버라이드 (2026-08-14) — 회수분(90종) 풀로 정본을 덮지 않고 병렬 생성한다.
import os as _os
_SUF = _os.environ.get("CASCADE_SUFFIX", "")
OUT = PROP / f"cascade_screening_funnel{_SUF}.json"

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


CONC_KEYS = ["002", "005", "010"]
CONC_LABEL = {"002": "x=0.02", "005": "x=0.05", "010": "x=0.10"}


def read_csv_rows(path):
    with open(path) as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── 농도별 챔피언 원자료 (G1·G5 가 평균한 3점을 되돌려 보기 위함) ──────────────
def load_champion_by_x():
    """champions.csv → {dopant: {"002": {...}, "005": {...}, "010": {...}}}.

    ⚠ ranked.csv 의 de / E_GPa / pugh 는 **이 3점의 산술평균**이다(전 47종 검증됨).
    G1·G5 는 그 평균값에 컷을 걸므로, 농도별 원값을 함께 보여주지 않으면
    '이 도펀트가 모든 농도에서 통과한다'는 오독을 만든다.
    """
    out = {}
    for r in read_csv_rows(PROP / "cascade_v23_champions.csv"):
        d, _, x = r["_dir"].rpartition("_x")
        out.setdefault(d, {})[x] = {
            "champion_label": (r.get("dopant") or "").strip(),
            "de": fnum(r.get("rerank_de_post_anneal")),
            "E_GPa": fnum(r.get("elastic_E_young_GPa")),
            "GoverB": fnum(r.get("elastic_pugh_GoverB")),
        }
    return out


# ── 데이터 로드 + ionic_transport norm 재계산 ────────────────────────────────
def load_pool():
    ranked = read_csv_rows(PROP / f"cascade_v23_ranked{_SUF}.csv")
    oxid = {r["dopant"]: r for r in read_csv_rows(PROP / f"oxidation_stability_cascade{_SUF}.csv")}
    lit = {}
    for r in read_csv_rows(PROP / f"cascade_v23_litransport{_SUF}.csv"):
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

    # ── ox_V 가 어느 조성족에서 온 값인가 (2026-08-16) ─────────────────────────
    # 챔피언 슬롯은 combined_score 최대값이 가져가는데 풀에 plain(compound_set) 과
    # Cl-rich(compound_set_chain) 두 변형이 같이 있다. 라벨은 그걸 감춘다.
    # 단일 출처는 pinned ESW 의 composition_family — 여기선 **옮겨 싣기만** 한다.
    pinned_path = PROP / "oxidation_stability_cascade_v3_pinned.json"
    fam_by_base = {}
    if pinned_path.is_file():
        pinned = json.load(open(pinned_path, encoding="utf-8"))
        for k, v in pinned.get("results", {}).items():
            if k.startswith("__HOST__") or "HOST" in k.split("_"):
                continue
            b, f, o = v.get("dopant_base"), v.get("composition_family"), v.get("oxidation_limit_V")
            if b and f and o is not None:
                fam_by_base.setdefault(b, {}).setdefault(f, []).append(o)
    for r in rows:
        fams = fam_by_base.get(r["dopant"], {})
        hit = sorted(f for f, vals in fams.items()
                     if r["ox_V"] is not None and any(abs(v - r["ox_V"]) <= 1e-6 for v in vals))
        r["ox_composition_family"] = (
            "unresolved" if not fams else
            "unmatched" if not hit else
            "degenerate" if len(hit) > 1 else hit[0])
        r["ox_family_confounded"] = r["ox_composition_family"] == "Clrich"
        r["plain_champion_exists"] = ("plain" in fams) if fams else None

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
    tpath = PROP / f"cascade_v23_themes{_SUF}.json"
    if tpath.exists():
        ref = {t["dopant"]: t["norm"]["ionic_transport"] for t in json.load(open(tpath))["dopants"]}
        bad = [r["dopant"] for r in rows
               if r["dopant"] in ref and ref[r["dopant"]] != r["transport_norm"]]
        if bad:
            raise ValueError(f"ionic_transport norm 이 themes.json 과 불일치: {sorted(bad)} "
                             "— 두 빌더의 규약이 갈라졌다. 먼저 정합시킬 것.")
    return rows


def transport_gaps(rows, top=3):
    """G4 통과자(=blocking 게이트를 넘은 종) 분포의 최대 공백 top-N.

    반환 (gap, below_value, above_value, below_name, above_name) — 산문에 박아 넣던 숫자를
    전부 여기서 뽑는다(입력이 바뀌면 문장도 같이 바뀌게).
    """
    ps = sorted([r for r in rows if (r["transport_norm"] or 0.0) > GATE_FLOOR],
                key=lambda r: (-r["transport_norm"], r["dopant"]))
    return sorted(((round(ps[i]["transport_norm"] - ps[i + 1]["transport_norm"], 4),
                    ps[i + 1]["transport_norm"], ps[i]["transport_norm"],
                    ps[i + 1]["dopant"], ps[i]["dopant"])
                   for i in range(len(ps) - 1)), reverse=True)[:top]


# ── 게이트 정의 ──────────────────────────────────────────────────────────────
def build_gates(rows):
    e_med = statistics.median([r["E_GPa"] for r in rows if r["E_GPa"] is not None])
    gb_med = statistics.median([r["GoverB"] for r in rows if r["GoverB"] is not None])

    # G4 선택압 분해 — blocking 상수가 죽인 것 vs bvs 컷이 죽인 것 (문자열 하드코딩 금지)
    _g4_fail = [r for r in rows if not ((r["transport_norm"] or 0.0) > TRANSPORT_CUT)]
    _g4_blocking_kill = [r["dopant"] for r in _g4_fail
                         if (r["blocking"] if r["blocking"] is not None else 1.0) >= BLOCKING_GATE]
    _g4_bvs_only_kill = sorted(r["dopant"] for r in _g4_fail
                               if r["dopant"] not in set(_g4_blocking_kill))
    _gaps = transport_gaps(rows)
    _g1, _g2, _g3 = _gaps[0], _gaps[1], _gaps[2]

    return {
        "G1": {
            "id": "G1",
            "name": "structural_stability",
            "label": "구조 안정 (도핑 형성 favorability)",
            "metric": ("de = E(doped champion) − E(host), UMA 상대 (eV). "
                       "⚠ cascade_v23_ranked.csv 의 de 는 단일 챔피언 값이 아니라 "
                       "**x∈{0.02, 0.05, 0.10} 챔피언 3점의 산술평균**이다(47/47 검증). "
                       "일부 도펀트는 plain·Cl-rich 조성족이 섞인 3점이며(B2O3 는 +Clrich 만 존재) "
                       "→ concentration_convention 블록 참조."),
            "threshold": "mean_x(de) < 0",
            "predicate": lambda r: r["de"] is not None and r["de"] < 0.0,
            "missing": lambda r: r["de"] is None,
            "concentration_convention": ("라벨 x002/x005/x010 3점 평균. ⛔ 이 라벨은 농도가 아니다 — "
                                         "1×1×1·4 f.u. 셀의 정수 치환 때문에 셋 다 **실측 x = 0.25** 다. "
                                         "농도 스윕도 반복실험도 아니므로 '2/5/10% 농도 의존성' 으로 읽으면 안 된다."),
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
            "threshold": f"window_V ≥ {COLLAPSE_WINDOW_V} V",
            "predicate": lambda r: r["window_V"] is not None and r["window_V"] >= COLLAPSE_WINDOW_V - 1e-12,
            "missing": lambda r: r["window_V"] is None,
            "concentration_convention": ("champion composition 단일 (농도 평균 아님). "
                                         "실측 x = 0.25 — 라벨 x002/x005/x010 은 농도값이 아니다."),
            "threshold_basis": (
                f"0.05 V 는 oxidation_stability_cascade.csv 가 이미 명문화한 **collapse 규약**"
                "('window<0.05 V = collapse, avoid, late-TM Fe/Co/Ni/Mn')이며 "
                "build_cascade_themes.py 의 oxidative/reduction 테마 게이트와 동일 상수다. "
                "이 빌더가 새로 만든 숫자가 아니라 기존 db 규약의 승계 — "
                "규약이 'collapse = window<0.05' 이므로 경계값(정확히 0.05)은 **통과**시킨다(≥). "
                "현재 데이터에는 경계값이 없어 판정은 동일(collapse 4종 최대 MnO 0.039, "
                "비-collapse 최소 Cu2O 0.113)."),
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
            "missing": lambda r: r["ox_V"] is None,
            "concentration_convention": ("champion composition 단일 (농도 평균 아님). "
                                         "실측 x = 0.25 — 라벨 x002/x005/x010 은 농도값이 아니다."),
            "composition_family_caveat": (
                "⚠ 챔피언 슬롯은 combined_score 최대값이 가져가고, 후보 풀에는 같은 도펀트의 두 "
                "설계 변형이 있다(compound_set=plain · compound_set_chain=Cl-rich, S 하나가 Cl 로 치환). "
                "그래서 이 게이트의 ox_V 중 일부는 plain 이 아닌 Cl-rich 조성 값이다. "
                "**B2O3 는 plain 챔피언 자체가 없어 3점 모두 +Clrich 다** — 그 2.317 V 는 "
                "도펀트 효과가 아니라 (도펀트 + 음이온 치환) 의 합이다. "
                "Al2O3·MoO3·WO3 는 plain 챔피언이 정확히 host(2.140) 이고 Cl-rich 형제만 넘는다. "
                "행별 판정은 oxidation_stability_cascade_v3_pinned.json 의 composition_family / "
                "delta_ox_vs_host_V_confounded 를 보라."),
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
            # ⛔ 2026-08-14 — 라벨에서 "Li 수송" 을 뺐다. 전도도·확산을 잰 것처럼 읽혔는데
            #    입력은 정적 프록시 두 개뿐이다(legacy BVS + 4 Å foreign-center count).
            #    MD·NEB 는 이 축에 하나도 안 들어갔다. name 은 하위호환 때문에 유지.
            "label": "정적 Li-환경 프록시 (BVS + 4 Å foreign-center)",
            "label_note": ("⛔ 이온전도 측정이 아니다. 옛 라벨 'Li 수송 유지' 는 폐기 — "
                           "이 게이트에 MD 확산계수·NEB 장벽·σ 는 하나도 들어가지 않는다."),
            "metric": ("ionic_transport norm ∈[0,1] = min-max(bvs_li_proxy_score @ 라벨 x005) "
                       f"with blocking<{BLOCKING_GATE} 게이트, 탈락자 {GATE_FLOOR} 평탄화. "
                       "⛔ **순환**: blocking 컷을 못 넘으면 BVS 값을 버리고 norm 을 "
                       f"{GATE_FLOOR} 로 강제한다 — 컷 {TRANSPORT_CUT} 보다 낮으므로 "
                       "blocking 탈락 = G4 탈락이 결정론적으로 따라온다. "
                       "'두 독립 신호가 일치했다'로 읽으면 안 된다. "
                       "⚠ 라벨 x002/x005/x010 은 셋 다 실측 x=0.25 다 — 'x=0.05' 가 아니다. "
                       "⚠ bvs_li_proxy_score 는 tools/doping/bvse_proxy.py 의 Adams-2003 "
                       "파라미터(R₀ Li–S 1.94 · Li–Cl 1.91 · b_S 0.40) — 정본 softBV(2.105/2.249/0.37)와 "
                       "다르므로 comp1 BVSE 결과와 같은 표에 올리지 말 것. "
                       "blocking 은 도펀트 4 Å 내 Li 비율이라 도펀트 원자 수에 거의 비례한다 "
                       "(host 원소만 든 종은 0.0 으로 자동 통과 — 판정 아님)."),
            "threshold": f"transport_norm > {TRANSPORT_CUT}",
            "predicate": lambda r: r["transport_norm"] is not None and r["transport_norm"] > TRANSPORT_CUT,
            "missing": lambda r: r["transport_norm"] is None,
            "concentration_convention": "x=0.05 단일 (litransport *_x005 — 농도 평균 아님)",
            "threshold_basis": (
                f"두 겹이고, **선택압의 거의 전부가 첫 겹에서 나온다**. "
                f"① blocking<{BLOCKING_GATE} 은 build_cascade_themes.py 가 이미 쓰는 db 규약(승계)이지만 "
                f"host 앵커도 문헌 대응도 없는 **상속 상수**다 — G4 단독 탈락 {len(_g4_fail)}종 중 "
                f"{len(_g4_blocking_kill)}종이 이 상수에 죽고, bvs 컷({TRANSPORT_CUT}) 단독 기여는 "
                f"{len(_g4_bvs_only_kill)}종({', '.join(_g4_bvs_only_kill)})뿐이다. "
                f"② {TRANSPORT_CUT} 컷은 통과자 분포 **하위 꼬리의 공백 구간**"
                f"({_g3[3]} {_g3[1]:.4g} ↔ {_g3[4]} {_g3[2]:.4g}, 폭 {_g3[0]:.4g}) 안에 놓았다. "
                f"⚠ 정확히 말하면 이건 분포 전체의 최대 공백이 아니다"
                f"(최대는 {_g1[1]:.4g}↔{_g1[2]:.4g} = {_g1[0]:.4g}, "
                f"그 다음이 {_g2[1]:.4g}↔{_g2[2]:.4g} = {_g2[0]:.4g}, 이게 3번째). "
                f"즉 '하위 꼬리를 자르는 자연스러운 위치 중 하나'이지 유일해가 아니다. "
                f"→ threshold_sensitivity 의 G4_li_transport(bvs 컷) **와 G4_blocking(상속 상수) 스윕을 "
                f"반드시 함께 볼 것** — 코어 생존자 수는 blocking 컷만 흔들어도 6↔21 로 움직인다."),
            "arbitrariness_flag": True,
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
            "metric": ("E_young (GPa, UMA) ↓ AND G/B ↓. "
                       "⚠ cascade_v23_ranked.csv 의 E_GPa·pugh(=G/B) 는 단일 챔피언 값이 아니라 "
                       "**x∈{0.02, 0.05, 0.10} 챔피언 3점의 산술평균**이다(47/47 검증, "
                       "champions csv elastic_E_young_GPa · elastic_pugh_GoverB 유래). "
                       "일부 도펀트는 plain·Cl-rich 조성족이 섞인 3점(B2O3 는 +Clrich 만 존재) "
                       "→ concentration_convention 블록 참조."),
            "threshold": (f"mean_x(E_GPa) ≤ {e_med:.4g} (roster median) AND "
                          f"mean_x(G/B) ≤ {gb_med:.4g} (roster median)"),
            "predicate": (lambda r: (r["E_GPa"] is not None and r["GoverB"] is not None
                                     and r["E_GPa"] <= e_med + 1e-9 and r["GoverB"] <= gb_med + 1e-9)),
            "missing": lambda r: r["E_GPa"] is None or r["GoverB"] is None,
            "concentration_convention": ("라벨 x002/x005/x010 3점 평균. ⛔ 이 라벨은 농도가 아니다 — "
                                         "1×1×1·4 f.u. 셀의 정수 치환 때문에 셋 다 **실측 x = 0.25** 다. "
                                         "농도 스윕도 반복실험도 아니므로 '2/5/10% 농도 의존성' 으로 읽으면 안 된다."),
            "threshold_basis": (
                "⚠ **G1–G4 와 달리 host 앵커가 없다.** UMA 탄성값은 절대 인용 금지 규율 대상이고, "
                "같은 방법(UMA)으로 계산된 undoped host 의 E/(G/B) 항목이 cascade 산출물에 없다 "
                "(elastic.json 의 host 값은 DFT — 교차 인용 불가). 따라서 median split = "
                "**로스터 내부 상대 컷**이다(arbitrariness_flag). "
                "게다가 컷이 걸리는 값 자체가 3농도 평균이라 **농도 산포가 게이트 폭과 맞먹는다** "
                "(E_young 농도 산포: NdF3 17.8 · WO3 17.0 · MgF2 16.8 GPa) → "
                "threshold_sensitivity.per_concentration_application 을 반드시 함께 볼 것. "
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


# vacuous 는 한 종류가 아니다 — 어떤 뜻의 0-kill 인지 라벨을 나눈다.
#   pool_curated       💤 : 이 게이트를 전체 풀에 걸어도 아무도 안 죽는다 = 풀이 이미 그 조건으로 큐레이션됨
#   subsumed_by_upstream ⊂ : 죽일 대상은 있었는데 상류 게이트가 먼저 가져갔다 (순서의 산물)
#   pool_exhausted      ∅ : 들어온 게 없다
VACUOUS_KIND_LABEL = {
    "pool_curated": "💤 풀 큐레이션 — 전체 풀에 단독 적용해도 0종 탈락",
    "subsumed_by_upstream": "⊂ 상류 게이트에 포섭 — 이 게이트가 죽일 종을 앞 게이트가 먼저 잡아감",
    "pool_exhausted": "∅ 풀 소진 — 들어온 종이 0",
}


def run_sequence(rows, gates, order, standalone_kill=None):
    alive = list(rows)
    steps = []
    seen = []
    for gid in order:
        g = gates[gid]
        passed = [r for r in alive if g["predicate"](r)]
        failed = [r for r in alive if not g["predicate"](r)]
        missing = sorted(r["dopant"] for r in alive if g.get("missing", lambda _r: False)(r))
        vac = len(failed) == 0
        kind = None
        if vac:
            sk = (standalone_kill or {}).get(gid)
            if not alive:
                kind = "pool_exhausted"
            elif sk == 0:
                kind = "pool_curated"
            else:
                kind = "subsumed_by_upstream"
        steps.append({
            "gate": gid,
            "gate_name": g["name"],
            "n_in": len(alive),
            "n_pass": len(passed),
            "n_fail": len(failed),
            "failed_here": sorted(r["dopant"] for r in failed),
            # ⚠ 판정 불가(입력 결측)는 '탈락'과 다르다 — attrition_is_not_screening 규율을 게이트 층에도 적용
            "n_missing": len(missing),
            "missing": missing,
            "vacuous": vac,
            "vacuous_kind": kind,
            "upstream_gates": list(seen),
        })
        seen.append(gid)
        alive = passed
    return steps, sorted(r["dopant"] for r in alive)


# ── 원자료 감사 (--audit_raw) ────────────────────────────────────────────────
#: 캠페인 산출물 → 3축 매핑. 값은 glob 패턴이고, **하나라도 맞으면 그 축은 채워진 것**.
#:  축 이름은 pool_provenance 의 "ESW·탄성·BVSE 3축" 과 같은 이름을 쓴다.
AXIS_GLOBS = {
    "ESW": ["**/esw*.json", "**/*oxidation*.json", "**/*window*.json"],
    "elastic": ["**/elastic*.json", "**/*cij*.json", "**/eos*.json", "**/*B0*.json"],
    "BVSE": ["**/bvse*.json", "**/*litransport*.json", "**/*blocking*.json"],
}
#: stage-01 이 자리 열거를 못 해 정직 종료한 흔적 (As₂S₃ 선례).
SEED_FAIL_KEYS = ("n_structures", "n_seeds", "n_candidates")


def _family_map():
    """attrition CSV 에서 종 → 계열. 없으면 빈 dict (감사는 계열 없이도 돈다)."""
    p = PROP / "cascade_seminar_pool_attrition_273_to_47.csv"
    if not p.is_file():
        return {}
    return {r["candidate"]: r["family"] for r in read_csv_rows(p)}


def _species_of(dirname):
    """`ZrCl4_x002` → `ZrCl4`. 라벨 접미사만 떼고 나머지는 그대로 둔다."""
    import re
    return re.sub(r"_x0\d\d.*$", "", dirname)


def audit_raw(root):
    """캠페인 루트를 훑어 종별 축 충족·seed 실패를 센다. 판정하지 않고 존재만 센다."""
    import collections
    import re
    root = Path(root)
    if not root.is_dir():
        print(f"⛔ 캠페인 루트가 없다: {root}")
        return 1
    fam = _family_map()
    per = {}                                   # species → {axis: bool, seed0: bool, n_dirs}
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        sp = _species_of(d.name)
        rec = per.setdefault(sp, {"axes": {a: False for a in AXIS_GLOBS},
                                  "seed0": False, "n_dirs": 0})
        rec["n_dirs"] += 1
        for axis, pats in AXIS_GLOBS.items():
            if rec["axes"][axis]:
                continue
            rec["axes"][axis] = any(next(d.glob(pat), None) is not None for pat in pats)
        # stage-01 정직 종료 흔적: n_structures 류가 0 으로 적힌 json
        for j in list(d.glob("**/*.json"))[:60]:
            try:
                t = j.read_text(errors="ignore")
            except OSError:
                continue
            if any(re.search(rf'"{k}"\s*:\s*0\b', t) for k in SEED_FAIL_KEYS):
                rec["seed0"] = True
                break

    by_fam = collections.defaultdict(lambda: collections.Counter())
    for sp, rec in per.items():
        f = fam.get(sp, "?")
        by_fam[f]["species"] += 1
        by_fam[f]["dirs"] += rec["n_dirs"]
        if all(rec["axes"].values()):
            by_fam[f]["all3"] += 1
        if rec["seed0"]:
            by_fam[f]["seed0"] += 1
        for a, ok in rec["axes"].items():
            if not ok:
                by_fam[f][f"no_{a}"] += 1

    print(f"캠페인 루트: {root}")
    print(f"실행 디렉터리 {sum(r['n_dirs'] for r in per.values())}개 · 종 {len(per)}개\n")
    hdr = f"{'family':12s} {'종':>4s} {'실행':>5s} {'3축완비':>7s} {'seed0':>6s} " \
          f"{'ESW없음':>8s} {'탄성없음':>9s} {'BVSE없음':>9s}"
    print(hdr); print("-" * len(hdr))
    for f in sorted(by_fam, key=lambda x: -by_fam[x]["species"]):
        c = by_fam[f]
        print(f"{f:12s} {c['species']:4d} {c['dirs']:5d} {c['all3']:7d} {c['seed0']:6d} "
              f"{c['no_ESW']:8d} {c['no_elastic']:9d} {c['no_BVSE']:9d}")
    print("\n⚠ 이 표는 **산출물 유무**만 센다. 축이 빈 이유(수렴 실패·파라미터 부재·미실행)는")
    print("  로그를 따로 봐야 한다. seed0 = stage-01 이 자리를 못 만들고 정직 종료한 종.")
    miss = sorted(sp for sp, r in per.items() if not all(r["axes"].values()))
    if miss:
        print(f"\n3축 미완 종 {len(miss)}개: {' '.join(miss[:40])}"
              + (" …" if len(miss) > 40 else ""))
    return 0


def _selftest():
    """양성 + **음성**. 가짜 캠페인 트리를 만들어 축 감지와 seed0 을 확인한다."""
    import shutil
    import tempfile
    td = Path(tempfile.mkdtemp(prefix="funnel_audit_st_"))
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok &= bool(cond)

    def mk(name, axes=(), seed0=False):
        d = td / name
        (d / "stage01").mkdir(parents=True)
        for a in axes:
            (d / f"{a.lower()}_result.json").write_text("{}")
        (d / "stage01" / "summary.json").write_text(
            '{"n_structures": 0}' if seed0 else '{"n_structures": 12}')
        return d

    mk("Al2O3_x002", axes=("esw", "elastic", "bvse"))
    mk("ZrCl4_x002", axes=("esw",))                      # 2축 결손
    mk("As2S3_x002", axes=(), seed0=True)                # seed 실패
    per = {}
    for d in sorted(p for p in td.iterdir() if p.is_dir()):
        sp = _species_of(d.name)
        r = {a: any(next(d.glob(g), None) is not None for g in gs)
             for a, gs in AXIS_GLOBS.items()}
        per[sp] = r
    chk(_species_of("ZrCl4_x002") == "ZrCl4" and _species_of("Li2O") == "Li2O",
        "라벨 접미사만 떼어낸다")
    chk(all(per["Al2O3"].values()), f"3축 완비 감지 ({per['Al2O3']})")
    # ★ 음성: 일부만 있는 종을 '완비' 로 세면 안 된다
    chk(not all(per["ZrCl4"].values()) and per["ZrCl4"]["ESW"],
        f"부분 충족은 미완으로 (ZrCl4 {per['ZrCl4']})")
    chk(not any(per["As2S3"].values()), "산출물 없는 종은 전 축 미충족")
    # ★ 음성: 없는 루트를 조용히 통과시키지 않는다
    chk(audit_raw(td / "nope") == 1, "없는 루트 → 종료코드 1")
    shutil.rmtree(td, ignore_errors=True)
    # ── --volume_gate 쪽 (2026-08-19) ────────────────────────────────────────
    fake = [{"dopant": "X2O3", "screen_dV_over_V0": v, "tier2_lattice_angle_dev_deg": "0.5",
             "tier2_lattice_aspect_ratio": "1.02"} for v in ("-0.30", "-0.29", "-0.28")]
    fake += [{"dopant": "Li2S", "screen_dV_over_V0": v, "tier2_lattice_angle_dev_deg": "0.4",
              "tier2_lattice_aspect_ratio": "1.01"} for v in ("0.00", "-0.01", "0.01")]
    st = vg_stats(fake)
    chk(st["by_species"]["X2O3"]["dropped_abs25"] == 3,
        "[양성] −29 % 계열은 현행 25 % 게이트에 전멸한다")
    chk(st["by_species"]["X2O3"]["dropped_resid"] == 0,
        "[양성] 같은 계열이 종내잔차 게이트에서는 전원 생존 (계통 이동은 벌하지 않는다)")
    # ★ 음성 1 — 무해 도펀트를 실수로 떨어뜨리면 안 된다
    chk(st["by_species"]["Li2S"]["dropped_abs25"] == 0,
        "[음성] ΔV≈0 인 Li2S 를 떨어뜨리지 않는다")
    # ★ 음성 2 — 종 안에서 혼자 튀는 놈은 잔차 게이트가 **잡아야** 한다
    fake2 = fake + [{"dopant": "X2O3", "screen_dV_over_V0": "-0.02",
                     "tier2_lattice_angle_dev_deg": "0.5", "tier2_lattice_aspect_ratio": "1.02"}]
    chk(vg_stats(fake2)["by_species"]["X2O3"]["dropped_resid"] == 1,
        "[음성] 종 안에서 혼자 27 %p 벗어난 씨드는 잔차 게이트가 잡는다")
    # ★ 음성 3 — 셀이 찌그러진 것을 모양 게이트가 놓치면 안 된다
    fake3 = [dict(fake[0], tier2_lattice_angle_dev_deg="9.0")] + fake[1:]
    chk(vg_stats(fake3)["by_species"]["X2O3"]["dropped_shape"] == 1,
        "[음성] 각도 9° 로 찌그러진 셀은 모양 게이트가 잡는다")
    chk(vg_stats(fake)["by_species"]["X2O3"]["dropped_shape"] == 0,
        "[양성] 등방 수축(각도 정상)은 모양 게이트가 통과시킨다")
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# ── 부피 게이트 재검토 (2026-08-19) ───────────────────────────────────────────
# 왜: 세미나 Step 3 의 `|ΔV| ≤ 25 %` 가 B₂O₃ plain 을 30/30 떨어뜨렸는데, 같은 치환의
#   우리 DFT 구조는 원자당 −2 % 밖에 안 움직였다. 1저자 질문("우리 b2o3 dft 는 어떻게
#   살아남았나")에서 시작해 게이트 정의를 원본까지 따라갔다.
#
#   ⛔ 앞서 두 번 **틀린 진단**을 냈다. 기록으로 남긴다:
#     (1) "생성기가 출발 셀을 25 % 부풀린다" — 아니다. V0 는 출발 셀이 아니다.
#     (2) "기준 셀 자체가 원자당 ~24 Å³ 로 크다"  — 아니다. 아래 null 대조가 반박한다.
#   실제 정의 (origin/claude/unified-2026-05-15:tools/doping/run_uma_screening.py):
#     dV = (V_doped/n_doped) / (V_base/n_base) − 1,   두 V 모두 **UMA 이완 후**
#     base = db/structures/lpscl_F43m_24G_canonical.cif (52원자, a=10.2493 Å,
#            20.705 Å³/atom **이완 전**) 를 cell_relax=True 로 이완한 것.
#   ⇒ 정의는 대칭이고 건전하다. 남은 문제는 정의가 아니라 **셀 크기**다:
#     SUPERCELL=1,1,1 (52원자 = 4 f.u.) 이라 n_units=max(1,round(4·x))=1 →
#     x 라벨 0.02/0.05/0.10 이 전부 0.25 로 뭉갠다. 4 f.u. 중 1 f.u. 치환이다.
#
#: 현행 게이트 (select_winners.py Stage 03)
VG_ABS_CUT = 0.25
#: ③ 대안 A — 종내 잔차. 계통적 수축(화학)은 봐주고 **씨드 하나만 튀는 것**(이완 실패)을 잡는다.
VG_RESID_MAD_K = 6.0
#: ③ 대안 B — 모양. 등방 치밀화는 물리, 전단·찌그러짐은 깨진 것.
VG_ANGLE_DEV_MAX = 5.0     # deg, 입방에서 벗어난 정도
VG_ASPECT_MAX = 1.25       # 축비


def _mad(xs, med):
    """중앙절대편차. 0 이면 (전원 동일) 하한을 준다 — 0 으로 나누지 않기 위해."""
    m = statistics.median([abs(x - med) for x in xs])
    return max(m, 0.005)


def vg_stats(rows, by_variant=False):
    """세 게이트를 같은 행 집합에 걸어 **종별 탈락 수**를 센다.

    rows: dopant · screen_dV_over_V0 · tier2_lattice_angle_dev_deg ·
          tier2_lattice_aspect_ratio 를 가진 dict 목록.
    by_variant=True 는 `variant_key` (raw 라벨) 로 묶는다. **왜 base 가 아닌가**:
      `B2O3` (P_4b 치환) 와 `B2O3+Clrich` (Li_24g + Cl 과잉) 는 원자 배치가 다른
      **다른 치환**이라 부피 반응도 다르다 — 합치면 30/30 전멸이 30/60 으로 희석돼
      게이트가 무엇을 죽였는지 안 보인다. 판정·순위 인용은 base 쪽을 쓴다.
    """
    from cascade_ids import base_species, variant_key
    key = variant_key if by_variant else base_species
    by = {}
    for r in rows:
        v = fnum(r.get("screen_dV_over_V0"))
        if v is None:
            continue
        by.setdefault(key(r.get("dopant")), []).append((v, r))
    out = {}
    for sp, items in sorted(by.items()):
        vs = [v for v, _ in items]
        med = statistics.median(vs)
        mad = _mad(vs, med)
        d_abs = d_res = d_shp = 0
        for v, r in items:
            if abs(v) > VG_ABS_CUT:
                d_abs += 1
            if abs(v - med) > VG_RESID_MAD_K * mad:
                d_res += 1
            ang, asp = fnum(r.get("tier2_lattice_angle_dev_deg")), fnum(
                r.get("tier2_lattice_aspect_ratio"))
            if (ang is not None and ang > VG_ANGLE_DEV_MAX) or (
                    asp is not None and asp > VG_ASPECT_MAX):
                d_shp += 1
        out[sp] = {"n": len(items), "median_dV_pct": round(100 * med, 2),
                   "mad_pct": round(100 * mad, 2),
                   "min_dV_pct": round(100 * min(vs), 2),
                   "max_dV_pct": round(100 * max(vs), 2),
                   "dropped_abs25": d_abs, "dropped_resid": d_res,
                   "dropped_shape": d_shp}
    return {"by_species": out}


def volume_gate(all_csv=None):
    """②재정량 ③대안 ④재채점을 한 번에 찍고 JSON 으로 남긴다."""
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    src = Path(all_csv or (PROP / "cascade_v23_all.csv"))
    if not src.exists():
        print(f"⛔ 없다: {src}")
        return 1
    rows = read_csv_rows(src)
    st = vg_stats(rows)["by_species"]
    vs = [fnum(r["screen_dV_over_V0"]) for r in rows
          if fnum(r.get("screen_dV_over_V0")) is not None]
    n = len(vs)
    tot = {k: sum(v[k] for v in st.values())
           for k in ("dropped_abs25", "dropped_resid", "dropped_shape")}

    # null 대조 — 화학적으로 host 와 사실상 같은 도펀트. 기준이 맞으면 ΔV≈0 이어야 한다.
    NULL = ("Li2S", "LiCl", "LiBr", "Li3N")
    nulls = {k: st[k]["median_dV_pct"] for k in NULL if k in st}

    print(f"── 부피 게이트 재검토  ({src.name}, {n}행, {len(st)}종)")
    print(f"   정의: dV = (V_doped/n) ÷ (V_base/n) − 1, 둘 다 UMA 이완 후 (대칭)")
    print(f"   전체 중앙 {100*statistics.median(vs):+.2f} %  "
          f"[{100*min(vs):+.1f} … {100*max(vs):+.1f}]")
    print(f"\n② null 대조 (기준의 영점) — 화학적으로 host 와 같은 도펀트:")
    for k, v in nulls.items():
        print(f"     {k:6s} 중앙 dV {v:+6.2f} %")
    print(f"   ⇒ |중앙| 최대 {max(abs(v) for v in nulls.values()):.2f} %p — "
          f"**기준 셀은 어긋나지 않았다.** 앞선 '기준이 24 Å³' 진단은 철회.")
    print(f"\n③ 게이트별 탈락 (같은 {n}행):")
    for k, lab in (("dropped_abs25", f"현행 |ΔV|>{100*VG_ABS_CUT:.0f} %"),
                   ("dropped_resid", f"대안A 종내잔차 >{VG_RESID_MAD_K:.0f}·MAD"),
                   ("dropped_shape", f"대안B 모양 (각도>{VG_ANGLE_DEV_MAX:.0f}° 또는 "
                                     f"축비>{VG_ASPECT_MAX})")):
        print(f"     {lab:44s} {tot[k]:5d} / {n}  ({100*tot[k]/n:.2f} %)")
    # ④ 는 **변형 단위**로 본다 — base 로 묶으면 B2O3(30/30 전멸)가
    #   B2O3+Clrich(0/30)와 합쳐져 30/60 으로 희석되어 아무것도 안 보인다.
    sv = vg_stats(rows, by_variant=True)["by_species"]
    wiped = sorted((k for k, v in sv.items() if v["dropped_abs25"] == v["n"]),
                   key=lambda k: sv[k]["median_dV_pct"])
    # 겹침 — 현행 게이트가 "이완 실패"를 실제로 잡고 있나. 잡는다면 대안과 겹쳐야 한다.
    flags = {"abs": set(), "resid": set(), "shape": set()}
    from cascade_ids import variant_key as _vk
    grp = {}
    for i, r in enumerate(rows):
        v = fnum(r.get("screen_dV_over_V0"))
        if v is not None:
            grp.setdefault(_vk(r.get("dopant")), []).append((i, v, r))
    for _k, items in grp.items():
        med = statistics.median([v for _, v, _ in items])
        mad = _mad([v for _, v, _ in items], med)
        for i, v, r in items:
            if abs(v) > VG_ABS_CUT:
                flags["abs"].add(i)
            if abs(v - med) > VG_RESID_MAD_K * mad:
                flags["resid"].add(i)
            ang, asp = fnum(r.get("tier2_lattice_angle_dev_deg")), fnum(
                r.get("tier2_lattice_aspect_ratio"))
            if (ang is not None and ang > VG_ANGLE_DEV_MAX) or (
                    asp is not None and asp > VG_ASPECT_MAX):
                flags["shape"].add(i)
    ov = {"abs&resid": len(flags["abs"] & flags["resid"]),
          "abs&shape": len(flags["abs"] & flags["shape"]),
          "resid&shape": len(flags["resid"] & flags["shape"])}
    print(f"   겹침: 현행∩대안A {ov['abs&resid']}행 · 현행∩대안B {ov['abs&shape']}행 · "
          f"대안A∩대안B {ov['resid&shape']}행")
    print(f"\n④ 재채점 — 현행 게이트에 **전멸**하던 치환 변형 (dropped_abs25 == n):")
    for k in wiped:
        v = sv[k]
        print(f"     {k:12s} n={v['n']:3d}  중앙 {v['median_dV_pct']:+7.2f} %  "
              f"→ 대안A 탈락 {v['dropped_resid']}  대안B 탈락 {v['dropped_shape']}")
    if not wiped:
        print("     (없음)")
    part = sorted(((v["dropped_abs25"], k) for k, v in sv.items()
                   if 0 < v["dropped_abs25"] < v["n"]), reverse=True)[:6]
    print(f"   부분 탈락 상위 (현행 게이트):")
    for c, k in part:
        v = sv[k]
        print(f"     {k:12s} {c:3d}/{v['n']:<3d}  중앙 {v['median_dV_pct']:+7.2f} %  "
              f"→ 대안A {v['dropped_resid']}  대안B {v['dropped_shape']}")
    out = PROP / f"cascade_volume_gate_review{_SUF}.json"
    out.write_text(json.dumps({
        "what": "Review of the cascade screening volume gate (|dV| <= 25 %).",
        "definition": ("dV = (V_doped/n_doped) / (V_baseline/n_baseline) - 1, both "
                       "volumes AFTER UMA relaxation with FrechetCellFilter "
                       "(cell_relax=True, same fmax/steps). Source: "
                       "origin/claude/unified-2026-05-15:tools/doping/"
                       "run_uma_screening.py"),
        "baseline_structure": {
            "file": "db/structures/lpscl_F43m_24G_canonical.cif",
            "n_atoms": 52, "a_angstrom": 10.2493, "V_per_atom_before_relax": 20.705,
            "note": "This is the INPUT to the baseline relaxation, not the reference "
                    "itself; the reference is its UMA-relaxed volume."},
        "retracted_claims": [
            "The generator inflates the starting cell by ~25 % -- FALSE, the starting "
            "cell never enters dV.",
            "The baseline itself is ~24 A^3/atom, ~30 % too large -- FALSE, the "
            "null-dopant controls below put the zero point within 1.6 %p."],
        "null_dopant_controls_median_dV_pct": nulls,
        "cell_size_finding": {
            "supercell": "1,1,1", "n_atoms": 52, "n_fu": 4,
            "why_it_matters": "n_units = max(1, round(n_fu * x)) = 1 for every x label, "
                              "so x=0.02/0.05/0.10 all collapse to x_actual = 0.25. "
                              "One of four formula units is substituted."},
        "gates": {
            "current_abs": {"cut_abs_dV": VG_ABS_CUT, "dropped": tot["dropped_abs25"]},
            "alt_A_within_species_residual": {
                "k_mad": VG_RESID_MAD_K, "dropped": tot["dropped_resid"],
                "rationale": "A systematic shrink shared by every seed of a species is "
                             "chemistry, not a broken relaxation. Flag the seed that "
                             "leaves its own species."},
            "alt_B_shape": {
                "angle_dev_max_deg": VG_ANGLE_DEV_MAX, "aspect_max": VG_ASPECT_MAX,
                "dropped": tot["dropped_shape"],
                "rationale": "Isotropic densification is physical; a sheared or "
                             "elongated cell is a failed relaxation."},
            "overlap_rows": ov,
            "verdict": ("The 25 % gate and the two failure-mode gates are nearly "
                        "disjoint: the rows it kills are systematic, isotropic "
                        "contractions shared by every seed of their species, i.e. "
                        "chemistry, not failed relaxations.")},
        "wiped_by_current_gate": {k: sv[k] for k in wiped},
        "by_species": st,
        "by_variant": sv,
    }, ensure_ascii=False, indent=2))
    print(f"\n→ {out}")
    return 0


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit_raw", metavar="ROOT",
                    help="캠페인 실행 루트를 훑어 종별 3축 충족 현황을 센다 (gabia)")
    ap.add_argument("--volume_gate", nargs="?", const="", metavar="ALL_CSV",
                    help="부피 게이트(|ΔV|≤25 %) 재검토 — 정의·영점·대안·재채점")
    ap.add_argument("--selftest", action="store_true")
    a, _unknown = ap.parse_known_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.audit_raw:
        raise SystemExit(audit_raw(a.audit_raw))
    if a.volume_gate is not None:
        raise SystemExit(volume_gate(a.volume_gate or None))

    rows = load_pool()
    gates = build_gates(rows)
    pool_names = sorted(r["dopant"] for r in rows)
    by_name = {r["dopant"]: r for r in rows}

    # ── 게이트별 블록 (대표 순서 기준 + standalone) ──────────────────────────
    standalone_kill_n = {gid: sum(1 for r in rows if not gates[gid]["predicate"](r))
                         for gid in REPRESENTATIVE_ORDER}
    steps, survivors = run_sequence(rows, gates, REPRESENTATIVE_ORDER, standalone_kill_n)
    step_by_gid = {s["gate"]: s for s in steps}

    # ── G3 귀속 감사 (Codex f9 P0-3) ─────────────────────────────────────────
    #   경고만 붙이고 species-level pass 를 유지하면 fail-open 이다. 알고리즘 count 는
    #   보존하되(역사 감사), 현재 과학적 판정은 pass/fail/unresolved 셋으로 나눈다.
    _g2 = [r for r in rows if gates["G2"]["predicate"](r)]
    _g3p = [r for r in _g2 if gates["G3"]["predicate"](r)]
    _unres = sorted(r["dopant"] for r in _g3p if r.get("ox_family_confounded"))
    gates["G3"]["_attribution_audit"] = {
        "g2_survivors": len(_g2),
        "algorithmic_g3": {"pass": len(_g3p), "fail": len(_g2) - len(_g3p)},
        "attribution_audit": {"supported_pass": len(_g3p) - len(_unres),
                              "fail": len(_g2) - len(_g3p),
                              "unresolved": len(_unres)},
        "unresolved_species": _unres,
        "why": ("unresolved 는 method-comparability 문제가 아니다 — 43행 모두 같은 실행의 "
                "phase set 안에서 host 와 비교된다. 문제는 **종 수준 효과 귀속**이다: "
                "이 종의 챔피언 3슬롯이 전부 chain generator 산물이고 plain 챔피언이 없다. "
                "역사 count(알고리즘 pass)는 archive 로 보존하고 현재 판정은 NA/not assessed 다."),
    }

    gate_blocks = []
    for gid in REPRESENTATIVE_ORDER:
        g = gates[gid]
        s = step_by_gid[gid]
        standalone_fail = sorted(r["dopant"] for r in rows if not g["predicate"](r))
        standalone_missing = sorted(r["dopant"] for r in rows
                                    if g.get("missing", lambda _r: False)(r))
        vac_interp = None
        if s["vacuous_kind"] == "pool_curated":
            vac_interp = (
                f"💤 VACUOUS (풀 큐레이션) — 이 게이트를 **전체 {len(rows)}종에 단독으로** 걸어도 "
                "0종이 떨어진다. 즉 '우리가 이 조건으로 걸렀다'가 아니라 **우리 풀이 이미 그 조건을 "
                "만족하도록 큐레이션돼 있었다**는 뜻이다. 문헌 깔때기에서는 같은 게이트가 수천~수만 종을 "
                "떨어뜨린다(Xiao F2: 62,437→1,600 = 97.4% 제거; Sendek E_hull=0: 12,831→1,472 = 88.5% 제거). "
                "발견력의 증거로 인용하면 과장이다.")
        elif s["vacuous_kind"] == "subsumed_by_upstream":
            vac_interp = (
                f"⊂ VACUOUS (상류 포섭) — 이 게이트는 단독으로는 {len(standalone_fail)}종을 떨어뜨리지만, "
                f"대표 순서에서는 앞 게이트({' · '.join(s['upstream_gates']) or '—'})가 그 종을 이미 "
                "가져가서 0-kill 이 됐다. **풀 큐레이션의 증거가 아니라 순서의 산물**이다.")
        elif s["vacuous_kind"] == "pool_exhausted":
            vac_interp = "∅ VACUOUS (풀 소진) — 이 게이트에 들어온 종이 0. 판정 자체가 없다."
        gate_blocks.append({
            "id": gid,
            "name": g["name"],
            "label": g["label"],
            "metric": g["metric"],
            "threshold": g["threshold"],
            "concentration_convention": g.get("concentration_convention"),
            "composition_family_caveat": g.get("composition_family_caveat"),
            "attribution_audit": g.get("_attribution_audit"),
            "threshold_basis": g["threshold_basis"],
            "literature_analog": g["literature_analog"],
            "engine": g["engine"],
            "arbitrariness_flag": g.get("arbitrariness_flag", False),
            "in_representative_order": {
                "n_in": s["n_in"], "n_pass": s["n_pass"], "n_fail": s["n_fail"],
                "eliminated_here": s["failed_here"],
                "n_missing": s["n_missing"], "missing": s["missing"],
            },
            "standalone": {
                "n_pass": len(rows) - len(standalone_fail),
                "n_fail": len(standalone_fail),
                "eliminated": standalone_fail,
                # 결측 = '떨어뜨린 것'이 아니라 '판정하지 못한 것' (지금은 0 이지만 규율상 항상 노출)
                "n_missing": len(standalone_missing),
                "missing": standalone_missing,
            },
            "vacuous": s["vacuous"],
            "vacuous_kind": s["vacuous_kind"],
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
    # 서사용 4개(P0–P3)는 UI 카드로 보여주고, 교집합/합집합 주장은 **120 순열 전수**로 증명한다.
    # (표본 4개로 뽑은 교집합은 '확인'이지 '증명'이 아니다 — 비용이 사실상 0 이라 전수로 간다.)
    exhaustive = []
    for order in itertools.permutations(REPRESENTATIVE_ORDER):
        st, surv = run_sequence(rows, gates, list(order), standalone_kill_n)
        exhaustive.append({"order": list(order),
                           "waterfall": [len(rows)] + [s["n_pass"] for s in st],
                           "final_survivors": surv})
    ex_sets = [set(e["final_survivors"]) for e in exhaustive]
    identical = all(s == ex_sets[0] for s in ex_sets)
    inter = sorted(set.intersection(*ex_sets))
    union = sorted(set.union(*ex_sets))
    distinct_waterfalls = sorted({tuple(e["waterfall"]) for e in exhaustive})

    perms = []
    for p in PERMUTATIONS:
        st, surv = run_sequence(rows, gates, p["order"], standalone_kill_n)
        perms.append({
            "key": p["key"], "order": p["order"], "rationale": p["rationale"],
            "waterfall": [len(rows)] + [s["n_pass"] for s in st],
            "steps": [{"gate": s["gate"], "n_in": s["n_in"], "n_pass": s["n_pass"],
                       "n_fail": s["n_fail"], "n_missing": s["n_missing"],
                       "vacuous": s["vacuous"], "vacuous_kind": s["vacuous_kind"],
                       "vacuous_label": VACUOUS_KIND_LABEL.get(s["vacuous_kind"]),
                       "upstream_gates": s["upstream_gates"]} for s in st],
            "final_survivors": surv,
        })

    # ── G4 선택압 분해: 상속 상수(blocking) vs BVSE 컷, 어느 쪽이 죽였나 ──────────
    # transport_norm 규약상 blocking >= BLOCKING_GATE 인 종은 GATE_FLOOR(0.05)로 눌려
    # TRANSPORT_CUT(0.30)을 자동 실패한다. 따라서 G4 탈락을 두 원인으로 완전 분할할 수 있다.
    _g4_fail_rows = [r for r in rows if r["dopant"] in fail_sets["G4"]]
    _g4_blocking_kill = sorted(r["dopant"] for r in _g4_fail_rows
                               if (r["blocking"] if r["blocking"] is not None else 1.0)
                               >= BLOCKING_GATE)
    g4_blocking_kill_n = len(_g4_blocking_kill)
    g4_bvs_only_names = sorted(r["dopant"] for r in _g4_fail_rows
                               if r["dopant"] not in set(_g4_blocking_kill))
    g4_bvs_only_n = len(g4_bvs_only_names)
    assert g4_blocking_kill_n + g4_bvs_only_n == len(fail_sets["G4"]), \
        "G4 탈락 분할이 전체를 덮지 않음 — blocking/bvs 분해 규약 확인"

    _bvs_vals = [r["bvs_x005"] for r in rows if r["bvs_x005"] is not None]
    lo_bvs = min(_bvs_vals)
    span_bvs = (max(_bvs_vals) - lo_bvs) or 1.0

    def _core_survivors_at_blocking(cut):
        """blocking 컷만 바꿔 transport_norm 을 재계산하고 코어(G1–G4) 생존자 수를 센다.
        load_pool() 의 norm 규약을 그대로 복제한다 — 규약이 갈라지면 여기부터 틀어진다."""
        n = 0
        for r in rows:
            if r["bvs_x005"] is None:
                continue
            t = (r["bvs_x005"] - lo_bvs) / span_bvs
            blk = r["blocking"] if r["blocking"] is not None else 1.0
            t = (GATE_FLOOR + GATE_EPS + t * (1.0 - GATE_FLOOR - GATE_EPS)) if blk < cut \
                else GATE_FLOOR
            if (gates["G1"]["predicate"](r) and gates["G2"]["predicate"](r)
                    and gates["G3"]["predicate"](r) and round(t, 4) > TRANSPORT_CUT):
                n += 1
        return n

    g4_blocking_sweep = [{"blocking_cut": c, "n_core_G1_G4": _core_survivors_at_blocking(c)}
                         for c in (0.50, 0.55, 0.60, 0.65, 0.70, 0.80, 1.00)]

    order_sensitivity = {
        "n_permutations_tested": len(exhaustive),
        "exhaustive": True,
        "narrative_permutations": perms,
        # 하위호환: 기존 소비자(webapp 템플릿)가 읽는 키 — 서사용 4개를 그대로 노출
        "permutations": perms,
        "final_sets_identical": identical,
        "intersection": inter,
        "union": union,
        "symmetric_difference": sorted(set(union) - set(inter)),
        "n_distinct_waterfalls": len(distinct_waterfalls),
        "distinct_waterfalls": [list(w) for w in distinct_waterfalls],
        "why": (f"게이트가 전부 **정적·per-dopant boolean 술어**라 최종 생존자는 집합 교집합이고 "
                f"순서에 불변이다. 순서가 바꾸는 것은 (a) 중간 단계 숫자(깔때기 그림의 모양)와 "
                f"(b) 어느 게이트에 탈락의 '공'이 돌아가는가(marginal kill)뿐. "
                f"이 불변성은 표본 확인이 아니라 **{len(exhaustive)} 순열 전수 계산**으로 증명했다 "
                f"— 최종 집합은 {len(exhaustive)}/{len(exhaustive)} 전부 동일하고 "
                f"깔때기 모양(waterfall)만 {len(distinct_waterfalls)}가지로 갈린다. "
                f"⚠ 단, '술어'라는 전제는 게이트마다 **농도 규약이 다르다**는 사실을 덮는다 "
                f"— concentration_convention 블록을 함께 읽을 것."),
        "sendek_analog_verdict": (
            "Sendek 2017 은 '전제조건(안정·gap·ESW)이 전도도 모델보다 세게 거른다'고 결론했다"
            "(전제조건 12,831→317 vs LR 모델 단독 12,831→1,408). **우리 풀에서는 순위가 뒤집힌다**: "
            f"standalone 제거 수 = G1 {len(fail_sets['G1'])} · G2 {len(fail_sets['G2'])} · "
            f"G3 {len(fail_sets['G3'])} · G4 {len(fail_sets['G4'])} · G5 {len(fail_sets['G5'])}. "
            "⚠ 다만 정확히 말하면 **'수송축이 최강'이 아니라 '수송축 안의 blocking 상수가 최강'**이다 — "
            f"G4 단독 탈락 {len(fail_sets['G4'])}종 중 {g4_blocking_kill_n}종은 상속 상수 "
            f"blocking<{BLOCKING_GATE} 이 죽인 것이고, BVSE 컷({TRANSPORT_CUT}) 자체의 단독 기여는 "
            f"{g4_bvs_only_n}종({', '.join(g4_bvs_only_names)})뿐이다. "
            "즉 축(axis)의 선택압이 아니라 **상수(constant)의 선택압**이며, 그 상수는 host 앵커도 "
            "문헌 대응도 없다(threshold_sensitivity.G4_blocking 스윕: 0.50→0.55→0.60→0.65→0.70→0.80→1.00 "
            f"에서 코어 생존자 {'/'.join(str(x['n_core_G1_G4']) for x in g4_blocking_sweep)}종). "
            "그리고 안정성(G1)이 아무도 못 떨어뜨리는 것은 큐레이션 풀의 성질이다 — 47종은 애초에 "
            "'넣을 만한' 도펀트로 골라져 안정성·ESW 전제조건을 통과한 상태로 시작한다. "
            "따라서 Sendek 명제의 반증이 아니라 **'전제조건이 이미 소진된 풀에서는 남은 구속이 "
            "가장 임의적인 상수로 옮겨간다'는 따름정리**로 읽어야 한다."),
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
                               "note": ("host 2.14 V 앵커에서 ±0.2 V 이동. onset 축퇴(19종이 정확히 2.14 V) 탓에 "
                                        "**완전한 계단 함수**다 — 컷을 2.19 V 로 0.05 V 만 올리면 코어 생존자가 "
                                        "11 → **0**. 즉 '도펀트가 host onset 을 유지하는가'는 견고한 이분 판정이지만 "
                                        "'얼마나 개선하는가'에는 해상도가 사실상 없다(S²⁻-limited). "
                                        "예외적으로 onset 을 올리는 소수(B2O3 2.317·Cr2O3/Ga2O3/In2O3/Sc2O3 2.356·"
                                        "Y2O3 2.282)는 G4 에서 탈락해 코어에 남지 않는다 = 산화안정과 수송의 정면 trade-off.")},
        "G4_li_transport": {"sweep": g4_sweep,
                            "largest_gaps_in_passer_distribution":
                                [{"gap": g, "below": lo, "above": hi} for g, lo, hi in gaps],
                            "note": ("코어 생존자는 0.30–0.40 구간에서 11종 불변, 0.25 로 내리면 MoO3 가 복귀해 12종, "
                                     "0.50 에서 10종, 0.60 에서 5종. 즉 컷을 **올리는** 쪽으로는 둔감하고 "
                                     "**내리는** 쪽으로 민감하다 — 0.30 은 공백 상단이라 그렇다. "
                                     "'자의적이지만 국소적으로 안정'이 정확한 표현이고, 비대칭이라는 점까지 붙여야 정직하다.")},
        "G4_blocking": {"sweep": g4_blocking_sweep,
                        "inherited_constant": BLOCKING_GATE,
                        "kill_decomposition": {
                            "g4_total_standalone_kill": len(fail_sets["G4"]),
                            "killed_by_blocking_constant": g4_blocking_kill_n,
                            "killed_by_bvse_cut_only": g4_bvs_only_n,
                            "bvse_only_names": g4_bvs_only_names,
                        },
                        "note": ("**G4 의 실제 선택압은 BVSE 컷이 아니라 상속 상수 blocking<0.60 이다** — "
                                 f"단독 탈락 {len(fail_sets['G4'])}종 중 {g4_blocking_kill_n}종이 blocking 에, "
                                 f"{g4_bvs_only_n}종({', '.join(g4_bvs_only_names)})만 BVSE 컷에 죽는다. "
                                 "transport_norm 규약상 blocking≥컷 인 종은 GATE_FLOOR(0.05)로 눌려 "
                                 "TRANSPORT_CUT(0.30)을 자동 실패하므로 두 원인은 완전 분할된다. "
                                 "이 상수는 build_cascade_themes.py 에서 승계한 것이고 host 앵커도 문헌 대응도 "
                                 "없다 — 코어 생존자가 0.50→1.00 에서 6→21종으로 3.5배 움직이므로 "
                                 "**G4 통과 수를 결론으로 인용할 때는 반드시 이 상수를 함께 밝힐 것**.")},
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
    tpath = PROP / f"cascade_v23_themes{_SUF}.json"
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
    # ⚠ 2026-08-14 — 풀 크기를 문자열에 **하드코딩하지 않는다.** _v2 로 돌리면 89 인데
    #    설명문만 "47종" 으로 남아 화면이 스스로 모순됐다 (Codex 감사). NP 로 통일.
    NP = len(rows)
    pool_provenance = {
        "pool_size": NP,
        "what_it_is": ("**큐레이션된 도펀트 후보군**. 화학적 사전지식(코팅 문헌·합성 전구체·발란스 다양성)으로 "
                       "사람이 고른 목록이지, 어떤 DB를 전수로 훑어 남은 잔존군이 아니다."),
        "selection_history": [
            "Round 1/2 reviewer 권장 = oxide 9–12종 (화학 일관성·Sundar 2025 코팅 문헌 근거)",
            "사용자 지적('ZrCl4·LiBr 같은 non-oxide 후보가 많다')으로 4-카테고리 22종으로 확장 "
            "(kb/projects/MULTI_CATEGORY_BATCH_PLAN_v22.md)",
            "master_batch_273.sh (v4.5.20) 로 91 화합물 × **라벨** 3종(x002/x005/x010) = 273 cascade 실행 "
            "— ⛔ 라벨이지 농도가 아니다. 실측은 셋 다 x=0.25 "
            "(kb/projects/cascade_v23_review_2026_07_11.md: 273/273 완료)",
            (f"그 중 gate 입력이 채워진 {NP}종이 cascade_v23_ranked{_SUF or ''}.csv 에 등재 = 이 풀"
             + ("  ⚠ 47 은 물리 판정이 아니라 **2026-06-29 에 멈춘 취합 경계**였다 "
                "(계산은 7-11 에 270/273 완주). kb/methodology/cascade_pipeline_anatomy_2026_08_13.md"
                if NP <= 47 else
                "  ← 90종 회수분. AlI₃ 1종은 gate 입력 전면 결측이라 빠졌고, 18종은 일부 라벨 "
                "결측 상태로 남은 라벨 평균으로 평가됐다 (cascade_pool_audit_v2.json)")),
        ],
        "attrition_is_not_screening": (
            f"91 → {NP} 의 감소는 **물리 게이트가 아니라 파이프라인/취합 탈락**이다(구조 seed 생성 실패 등, "
            "예: As₂S₃ 3종은 stage-01 n_structures=0 으로 정직 종료). "
            "이들은 '떨어뜨린' 것이 아니라 '판정하지 못한' 것 — 깔때기 숫자에 합산하면 안 된다."),
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
            "verdict": (f"{NP}은 발견 깔때기 체급이 아니라 **조성족 스캔** 체급이다"
                        f"(Ong 11 < 우리 {NP} < Fujimura 92 / Kahle 4,963). "
                        "이 계보로 위치를 잡으면 정직하면서도 문헌적으로 정당하다."),
        },
        "not_a_discovery_funnel": (
            "❗ 이 JSON의 게이트 통과 수는 **발견 성능 지표가 아니다**. 'N만 개에서 걸러냈다'는 서술은 "
            "우리 데이터로 지지되지 않는다. 정확한 서술: "
            f"'큐레이션된 {NP}종 도펀트 후보를 문헌(Xiao/Sendek/Kahle) 표준 게이트 순서로 재표현하면 "
            "어디서 몇 종이 떨어지는지를 보인 뷰'."
            + ("  ⛔ 그리고 이 판(_v2)은 **미검증 진단물**이다 — 막는 것은 결측이 아니라 "
               "**게이트 정의**다: G3 는 phase-set comparable 270/270 이지만 효과 귀속 0/17 "
               "(phase_set_id 미기록), G4 는 blocking 이 BVS 를 덮어쓰는 순환, "
               "G5 는 로스터 상대 median 이다. 순위·통과 수를 결과로 인용하면 안 된다."
               if _SUF else
               "  ⛔ 그리고 이 판은 **superseded** 다 — 2026-06-29 취합 경계의 47종이고, "
               "완주분은 90종이다.")),
        "related_but_different_funnel": (
            "kb/methodology/dopant_screening_funnel_2026_06_13.md 는 **한 도펀트 내부의 배치(config) 깔때기**"
            "(Nd₂O₃ 342 configs → cfg141)다. 여기 깔때기는 **도펀트 종(species) 수준** — 층이 다르니 "
            "두 숫자를 섞어 '수백 종을 걸렀다'로 합치지 말 것."),
    }

    out = {
        "property": "cascade_screening_funnel",
        "date": BUILD_DATE,
        "description": (f"cascade v23 도펀트 {NP}종을 문헌 표준(Xiao 2019 F1–F6 · Sendek 2017 전제조건→ML · "
                        "Kahle 2020 pinball→FPMD)의 순차 게이트 깔때기로 재표현한 뷰. "
                        "게이트별 통과/탈락 명단·임계값 근거·문헌 대응, vacuous 게이트 플래그, "
                        "게이트 순서 민감도, 문헌 대비표를 포함."
                        + ("  [_v2 · 90종 회수분 — 미검증 진단물]" if _SUF else "  [superseded · 47종 취합 경계판]")),
        "status": ("recovered_unvalidated_diagnostic" if _SUF else "superseded_47species"),
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
        "key_findings": [
            "G1(Δe<0)은 47/47 vacuous — 우리 풀이 이미 그 조건으로 큐레이션됐다는 증거이지 "
            "우리 스크린의 발견력이 아니다.",
            "G2(window collapse)는 unique_kill=0 = **완전 중복 게이트**. 창이 붕괴한 4종"
            "(Fe2O3·CoO·NiO·MnO)이 전부 late-TM 이라 G3(ox onset)에도 걸린다 → "
            "우리 풀에서 '창 붕괴'와 '낮은 onset'은 같은 화학(후기 TM d-band)의 두 얼굴이다.",
            "Sendek 2017 의 '전제조건 > 전도도' 순위가 우리 풀에서는 역전된다 "
            "(standalone kill: 안정 0 · 창 4 · onset 22 · 수송 27 · 기계 32) — "
            "전제조건이 이미 소진된 큐레이션 풀에서는 구속조건이 수송/기계로 이동한다.",
            "게이트가 전부 정적 boolean 이라 최종 생존자 집합은 순서 불변(4개 순열에서 실측 확인). "
            "순서가 바꾸는 것은 중간 숫자와 '탈락의 공' 배분뿐 — 깔때기 그림의 모양은 서사 선택이지 결과가 아니다.",
            "host onset(2.14 V)을 **올리는** 6종(B2O3·Cr2O3·Ga2O3·In2O3·Sc2O3·Y2O3)이 전부 "
            "G4(수송)에서 탈락한다 = 산화 안정과 Li 수송의 정면 trade-off. "
            "Xiao 2019 의 'V_ox ↔ Li 함량 내재 trade-off'(Fig 7)의 우리판 대응.",
            "문헌 절대 문턱을 그대로 이식하면 두 개가 empty gate 가 된다: V_ox≥4.0 V(Xiao) → 0종, "
            "Pugh B/G>1.75 → 0종. 우리가 host 상대·로스터 상대 좌표를 쓰는 이유의 정량 근거.",
            "문헌에 있고 우리 게이트엔 없는 축 2개: 계면 화학 반응성(Richards pseudo-binary ΔE_rxt)과 "
            "전자 절연(우리 계산 gap 전수 부재). 전자는 추가 1순위, 후자는 진단으로만 붙였다.",
        ],
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
                  "ox_composition_family": r["ox_composition_family"],
                  "ox_family_confounded": r["ox_family_confounded"],
                  "plain_champion_exists": r["plain_champion_exists"],
                  "gates_passed": [g for g in REPRESENTATIVE_ORDER if gates[g]["predicate"](r)],
                  "gates_failed": [g for g in REPRESENTATIVE_ORDER if not gates[g]["predicate"](r)]}
                 for r in sorted(rows, key=lambda x: x["dopant"])],
        "pool_names": pool_names,
    }

    # ⛔⛔ 2026-08-13 — 손으로 붙인 블록을 **재생성이 지운다**. `_provenance_audit` 는
    #   2026-08-12 provenance sweep 이 사후 추적으로 넣은 것이고 이 생성기가 만들지
    #   않는다. 그래서 아무 생각 없이 재빌드하면 조용히 사라진다 (실제로 당했다).
    #   → 기존 파일의 `_` 로 시작하는 최상위 키는 **그대로 승계**한다.
    if OUT.is_file():
        try:
            prev = json.load(open(OUT, encoding="utf-8"))
        except (OSError, ValueError):
            prev = {}
        carried = {k: v for k, v in prev.items()
                   if k.startswith("_") and k not in out}
        if carried:
            out.update(carried)
            print(f"[funnel] 손편집 블록 승계: {' '.join(sorted(carried))}")

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
