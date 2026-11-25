#!/usr/bin/env python3
"""build_cascade_audit_manifest.py — cascade 감사 원장의 **단독 소유자**.

왜 이 도구가 생겼나 (2026-08-14, Codex Round-3 P0-1)
  `plot_cascade_audit_2026_08.py` 와 `rebuild_pool_inputs.py` 가 **같은**
  `db/properties/cascade_audit_manifest.json` 을 서로 다른 깊이로 통째로 덮어썼다.
  나중에 돈 쪽이 이겨서, 그 커밋의 manifest 에는 플로터의 핵심 계약 블록
  (`datasets`·`metric_contract`·`source_hashes`·`recovered_artifacts`)이 통째로 없었다.
  `--validate-only` 는 schema/source/headline 과 figure·support 해시만 보므로 **그 결손을
  못 잡는다**. 두 생산자가 한 파일을 쓰는 구조 자체가 결함이었다.

  → 지금 규약: **생산자는 sidecar 만 쓴다. 최종 manifest 는 이 도구만 쓴다.**

      rebuild_pool_inputs.py  → cascade_pool_audit_v2.json          (sidecar)
                              → cascade_audit_artifacts_sidecar.json (sidecar)
      plot_cascade_audit.py   → cascade_audit_*.csv / *.png          (sidecar)
                              ↓
              **이 도구** → cascade_audit_manifest.json  (유일한 writer)

artifact 별 provenance (Codex Round-3 P0-2)
  최상위 `source_commit` 하나로 전부를 덮으면 거짓말이 된다 — Na₂S 정정으로
  `ranked_v2` 만 뒤 커밋 산출물이 됐는데 원장은 `9abe5105` 이라고 적고 있었다.
  이제 artifact 마다 `source_commit` · `derived_from` · `override_reason` 을 싣는다.

  python3 tools/cascade/build_cascade_audit_manifest.py
  python3 tools/cascade/build_cascade_audit_manifest.py --check     # 쓰지 않고 검증만
  python3 tools/cascade/build_cascade_audit_manifest.py --selftest

이 도구가 못 하는 것
  · 값을 검증하지 않는다. 파일의 해시·바이트·행수와 **선언된 지위**만 굳힌다.
  · 그림을 만들지 않는다 (plot_cascade_audit_2026_08.py 담당).
  · status 를 추론하지 않는다 — ARTIFACTS 표에 사람이 적은 값을 쓴다.
  · G3 의 phase-set 정체성을 복구하지 못한다. 그건 재계산이 필요하다.
"""
import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"
FIGD = ROOT / "docs" / "figures" / "cascade"
OUT = PROP / "cascade_audit_manifest.json"

#: 고정 소스 — 감사 패널이 만들어진 커밋.
PINNED_SOURCE_COMMIT = "9abe5105cacafa22ab3e185f09e2a4c37118b9a9"
#: Na₂S 정정 커밋. `ranked_v2` 만 이쪽 산출물이다.
NA2S_FIX_COMMIT = "922332c0"

#: ── status 어휘 통일 (Codex Round-3 P1) ──────────────────────────────────
#  전에는 세 축이 뒤섞여 있었다: manifest 5종 · 최상위 `audit_current__…` ·
#  figure 의 `audit-current`. **릴리스 지위**와 **artifact 승인 지위**를 나눈다.
RELEASE_STATUS = "audit_current__leaderboard_unavailable"   # 릴리스 전체의 지위 (1개)
#: artifact 승인 지위 (artifact 마다 1개) — loader 가 이 어휘 밖 값을 만나면 fail-closed
APPROVAL_STATUS = ("historical", "recovered_unvalidated", "approved",
                   "superseded", "invalid", "audit_current")
#: 사용 범위 — 승인 지위와 **직교**한다 (Codex: "approved/unvalidated 와 use-scope 를 나눠라")
USE_SCOPE = ("default_visible",      # 기본 화면 노출 가능
             "archive_only",         # ?archive=1 필요
             "diagnostic_only",      # ?view=diagnostic 필요 (acquisition 용)
             "blocked")              # 어떤 경로로도 표시 금지

#: (파일, 승인지위, use_scope, 설명, 한계, source_commit, derived_from, override_reason)
ARTIFACTS = [
    ("cascade_v23_all.csv", "recovered_unvalidated", "diagnostic_only",
     "완주 원자료 (unified_dataset_273.csv 회수분)",
     ["UMA 상대값", "일부 열은 재계산 세대가 섞여 있을 수 있음"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_champions_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "champion 270행 (rank_combined==1)",
     ["champion 재선정 안 함",
      "Na2S_x100 은 B_hill 음수 — 탄성 계산 실패 행 (소비자가 걸러야 한다)"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_litransport_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "G4 정적 프록시 270행",
     ["legacy Adams-2003 BVS — 정본 softBV 아님",
      "blocking 은 4 Å foreign-center count", "min–max 정규화라 풀 상대값"],
     PINNED_SOURCE_COMMIT, None, None),
    ("oxidation_stability_cascade_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "grand-potential ESW 90종 — **record-complete 90 · phase-set comparable 270/270 · 효과 귀속 0/17**",
     ["phase_set_id·mp-ID·MP 스냅샷 미기록 — 재현 불가",
      "host onset 2.140 V 는 phase set 의존 (LiS4 제외 시 2.256 V)",
      "270 회수 반응 중 124건에 LiS4 가 들어 있다"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_ranked_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "합성점수 랭킹 89종 (AlI3 제외) — acquisition 전용",
     ["G4 순환 (blocking 이 BVS 를 덮어씀)", "G5 median 컷은 로스터 상대",
      "가중치 수작업", "min-max 정규화라 풀이 바뀌면 값이 바뀜"],
     NA2S_FIX_COMMIT, PINNED_SOURCE_COMMIT,
     "Na2S ductility retraction — Na2S_x100 has B_hill = -36.27 GPa (failed elastic "
     "calculation) and was averaged in, producing a false B/G = 2.50. "
     "plot_cascade_insights.py now drops non-positive Hill moduli; Na2S is B/G 1.22. "
     "Only unphysical row in 270. No audit panel reads this file."),
    ("cascade_v23_all_20260629_47species.csv", "historical", "archive_only",
     "2026-06-29 취합 경계판 (47종)", ["캠페인 커버리지 기준으로 superseded"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_ranked.csv", "superseded", "archive_only",
     "47종 랭킹 — 역사 스냅샷", ["결과로 인용 금지", "90종 회수 이전 판"],
     PINNED_SOURCE_COMMIT, None, None),
    # ★ 2026-08-16 (Codex f9 webapp P0-4) — 재감사의 정본 산출물 두 건을 원장에 올린다.
    #   등록이 안 돼 있으면 artifact_policy 가 판단할 근거가 없고, 화면은 정책 없이 노출한다.
    ("oxidation_stability_cascade_v3_pinned.json", "audit_current", "diagnostic_only",
     "G3 v3 pinned — 후보·host 를 같은 실행·같은 entry set 에서 (phase_set_id 기록) + 조성족 감사",
     ["후보 identity 포함 — 공개 금지, acquisition/diagnostic 전용",
      "phase-set 비교는 270/270 닫힘 · **효과 귀속은 0/17 열림**",
      "chain 17행 중 exact 대응 10 · multi-transform 7 (B2O3·MoO3·WO3 는 치환 자리까지 다름)",
      "onset 초과율 9.63배·2.59배는 둘 다 사후 기술통계 — 인과 효과 아님",
      "도펀트 없는 Cl-only host(Li23P4S19Cl5) 기준이 없어 Cl 분해 불가",
      "window_V 는 2026-09-22 재유도본(ox − ocv · 356 행) · 나머지 82 행은 교환 0 구간이 없어 안정창 없음"
      "(window_V null · 2026-10-01 정정 — 09-22 의 '재유도 불가' 표시는 오해) · 옛 값은 legacy 필드"],
     "regenerated by esw_cascade_batch.py --annotate (2026-08-16) · window_V 재유도 2026-09-22 (8a0e202d3) · "
     "82 행 안정창 없음 정정 2026-10-01",
     PINNED_SOURCE_COMMIT,
     "f9 재감사: composition_family_audit · matched_transform · dft_deep_composition_collision · "
     "09-22 ESW 환원 가장자리 정정 (HZ-esw-reduction-limit-label) · D-2026-10-01-cascade-esw-no-stable-window"),
    # ★ 2026-08-16 — 효과 귀속을 실제로 닫은 산출물. main(Cl)=0.000 in 11/11.
    ("oxidation_matched_factorial.json", "audit_current", "default_visible",
     "matched 2x2 operational contrast — H_plain/H_Cl/D_plain/D_Cl 을 chemsys 마다 같은 pinned entry set 에서",
     ["조성 수준 operational contrast — **원소 수준 인과 아님**",
      "baseline(undoped) contrast 0 ≠ Cl 효과 0. 조건부(D_Cl−D_plain)는 종마다 양·음·0",
      "11종의 H 셀은 같은 두 조성 — 독립 표본 11개가 아니라 11개 확장 roster 반복",
      "캐스케이드 B2O3·MoO3·WO3 의 plain 챔피언은 P_4b 자리라 여기 D_plain(Li_24g)과 다른 물건",
      "캐스케이드 값과의 일치는 round-trip consistency 검사이지 독립 물리 검증 아님",
      "onset 반응식은 tie 영향 가능 — 재실행 전까지 기전 근거로 쓰지 말 것",
      "LiS4 포함/제외 phase-roster 민감도(2.140 vs 2.256)는 그대로 열려 있다",
      "structural realization 0/11"],
     "c0c879ac", None,
     "operational factorial 17/17 · element causality not_claimed · structural 0/11"),
    ("oxidation_matched_factorial_nolis4.json", "audit_current", "diagnostic_only",
     "matched 2x2 — **LiS4 제외 phase set**. contrast 가 roster 의존인지 보는 robustness 판",
     ["⛔ **다른 phase set 이다** — 기본판과 절대 onset 을 섞지 말 것 (host 2.256 vs 2.140)",
      "conditional contrast 가 크게 움직인다: WO3 +0.216→0.000 · Al2O3 +0.214→+0.098 · MoO3 +0.216→+0.129",
      "B2O3 만 +0.283 불변 · Sc2O3 -0.017→-0.046",
      "부호는 대체로 유지되나 크기는 안 버틴다 — 인용 시 roster 를 반드시 같이 적을 것",
      "사다리 없음 (ladder_steps=0) — 사다리는 기본판에만 있다"],
     "17d9a373", "db/properties/oxidation_matched_factorial.json",
     "phase-roster robustness 1차 — 기전을 본문 결론으로 못 올리는 이유"),
    ("cascade_label_scatter_audit.json", "audit_current", "diagnostic_only",
     "세 농도 라벨의 실체 + 3점 집계가 게이트 축에 넣는 배치 잡음",
     ["⛔ 2026-08-16 재감사로 **앞 판 수치 철회**: base 종이 아니라 raw dopant 로 묶어 "
      "81종만 봤다(정확히는 90종) · 조성 불일치 22 → **31** · 교차 칸 0 → **7**",
      "'조성 동일 여부가 자리 종류로 완전히 결정된다' 는 **성립하지 않는다** (교차 7종)",
      "G1 열이 screen_de_per_atom 이 아니라 rerank_de_post_anneal — 비 0.08 → **0.205**",
      "G4 는 3점 평균이 아니라 **x005 한 점**을 임의 대표로 쓴다 (평균이 망친 게 아니다)",
      "eos_B0_GPa 는 게이트 입력이 아니다 — 참고용",
      "비는 경고선이지 통계 문턱이 아니다 (표본 3점 · 종내에 자리·조성·anneal 잡음이 섞임) "
      "— '살았다/죽었다' 판정 금지",
      "흩어짐이 물리(자리 의존성)인지 수치(국소최소)인지 구별 못 한다"],
     "9afe33c3 → 재감사 정정본", None,
     "Codex 재감사 P0 3건 반영: base 그룹핑 · 실제 G1 열 · G4 단일선택"),
    ("b2o3_esw.json", "historical", "archive_only",
     "legacy B2O3 ESW (DFT-deep 셀 Li58P8S41Cl16B2O3, onset 2.03 V)",
     ["method_status **unverified** — phase_set_id·entry_ids·MP 버전 없음",
      "캐스케이드 챔피언(Li17B2P4S16Cl5O3, 2.317 V)과 **다른 조성**이다",
      "부호 반전은 관측됐지만 원인을 조성 하나로 확정할 수 없다 (Codex f9 P0-2)",
      "도펀트 라벨(B2O3)만으로 validation join 금지"],
     "손으로 압축한 요약 (2026-06-29) — 생성기 없음 · 2026-09-22 머리 경고(⛔_window_V)만 추가 · 데이터 불변", None,
     "f9 재감사: composition_collision_2026_08_16 로 '순전히 조성 차이' 철회"),
    ("cascade_screening_funnel.json", "historical", "archive_only",
     "47종 게이트 감사", ["G3 phase set 미기록", "G4 순환", "G5 로스터 상대",
                     "창은 옛 정의(ox − 마지막 환원 계단 · 계통적으로 넓다) — 2026-09-22 머리 경고만 추가 · 재생성 안 함 (역사 스냅샷)"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_screening_funnel_v2.json", "recovered_unvalidated", "diagnostic_only",
     "89종 게이트 감사", ["위와 동일 + 풀 상대 정규화 재계산됨",
                     "G2 = 정정 창(ox − ocv) — 교환 0 구간이 없는 21종은 안정창 없음(탈락) (2026-10-01)"],
     "regenerated by build_screening_funnel.py (2026-10-01 · ESW 정정 창)", PINNED_SOURCE_COMMIT,
     "ESW 환원 가장자리 정정을 G2 에 적용 — D-2026-10-01-cascade-funnel-esw-corrected-window · "
     "D-2026-10-01-cascade-esw-no-stable-window (트랙 ESW · 사용자 = 1저자)"),
    # ⛔ Round-3 — 종명이 든 G3/G4 감사본. 공개판은 익명 seminar round3 쪽이다.
    ("cascade_audit_g3_phase_set.csv", "audit_current", "diagnostic_only",
     "G3 phase-set 감사 (종명 포함)", ["공개 금지 — 후보 identity 는 acquisition 전용"],
     "regenerated by plot_cascade_audit_2026_08.py (2026-08-14)", PINNED_SOURCE_COMMIT,
     "Round-3 P1: synthetic phase_set_id 제거 + phase_set_assumption 분리"),
    ("cascade_audit_g4_rescore.csv", "audit_current", "diagnostic_only",
     "G4 재점수 감사 (종명 포함)", ["공개 금지 — 후보 identity 는 acquisition 전용",
                          "min–max 정규화라 풀 상대값 (pool_id 열 참조)"],
     "regenerated by plot_cascade_audit_2026_08.py (2026-08-14)", PINNED_SOURCE_COMMIT,
     "Round-3 P1: pool_id·normalization_n·BVS min/max·actual_x 추가"),
    ("cascade_seminar_g3_sensitivity_round3.csv", "audit_current", "default_visible",
     "G3 host 민감도 — 공개판 (후보 phase_set_id 없음)",
     ["Scenario A/B 는 host-only 민감도다. 후보 비교로 쓰면 안 된다"],
     "codex round3 package (2026-08-14)", None, None),
    ("cascade_seminar_g4_anonymized_round3.csv", "audit_current", "default_visible",
     "G4 분해 — 공개 익명판 (Case A–F)",
     ["후보 identity 는 acquisition 전용이라 익명화됐다",
      "historical 47종 정규화 · 실측 x=0.25 · 전도도가 아니다"],
     "codex round3 package (2026-08-14)", None, None),
    ("cascade_seminar_gate_denominators_round3.csv", "audit_current", "default_visible",
     "게이트 분모 계약 — record_present ≠ method_valid",
     ["G3 는 record 90 인데 method_valid 0 이다"],
     "codex round3 package (2026-08-14)", None, None),
    ("cascade_pool_audit_v2.json", "recovered_unvalidated", "default_visible",
     "gate 입력 ingestion 감사 (행 존재만 본다)",
     ["값의 물리성은 안 본다 — validity-aware 판정은 gate_completeness 표를 볼 것"],
     PINNED_SOURCE_COMMIT, None, None),
]

#: 5개 감사 패널 — 계약상 기본 공개가 허용된 유일한 그림
#: 2026-08-14 Codex Round-3 P1 반영으로 **생성기가 바뀐** 감사 CSV.
#:  손으로 고친 게 아니라 plot_cascade_audit_2026_08.py 가 지금 이 내용을 만든다
#:  (재현 가능). 다만 고정 커밋 `9abe5105` 시점 산출물과는 다르므로 provenance 를 분리한다.
AMENDED_CSV = {
    "cascade_audit_g3_phase_set.csv":
        ("recovered 행의 synthetic phase_set_id 를 비우고 phase_set_assumption 으로 분리했다. "
         "합성 ID 를 남기면 method-complete=0 판정과 정면으로 충돌한다 — 반응식에 LiS4 가 "
         "들어 있다는 사실은 method identity 가 아니다. 그림은 host onset 두 값과 LiS4 "
         "수만 표시하므로 영향 없음."),
    "cascade_audit_g4_rescore.csv":
        ("pool_id · normalization_n · BVS pool min/max · actual_x · concentration_label 추가. "
         "min–max 점수를 고정 물성처럼 읽지 못하게 하는 메타다 — B2O3 는 historical 47 풀에서 "
         "0.1000, recovered 88 풀에서 0.1998 (둘 다 fail). 기존 값 열은 안 건드렸다."),
    "cascade_audit_gate_completeness.csv":
        ("completeness_basis 열과 G5 validity-aware 열 추가. presence 로 세면 88/1/1 이지만 "
         "비물리 탄성(B_hill·G_hill ≤ 0)을 거르면 86 / AlBr3·MgI2·Na2S / AlI3 / usable 89 다. "
         "기존 presence 수치는 그대로 두고 옆에 병기했다."),
}

#: 공개 패널 5종 — (stem, csv stem, 제목).
#  ⛔ 2026-08-14 Round-3 정책: **후보 이름은 acquisition 전용**이다. 그래서 G3·G4 의
#  공개판은 seminar round3 익명본(Case A–F · Scenario A/B)을 쓰고, 종명이 든 판은
#  diagnostic_only 로 내린다. 앞 판은 기본 화면에 B2O3·Cr2O3… 를 그대로 띄우고 있었다.
FIGURES = [
    ("cascade_audit_campaign_status", "cascade_audit_campaign_status", "캠페인 현황"),
    ("cascade_seminar_g3_sensitivity_round3", "cascade_seminar_g3_sensitivity_round3",
     "G3 host 민감도 (공개판 — 후보 phase_set_id 없음)"),
    ("cascade_seminar_g4_anonymized_round3", "cascade_seminar_g4_anonymized_round3",
     "G4 분해 (공개판 — 익명 Case A–F)"),
    ("cascade_audit_interface_axes", "cascade_audit_interface_axes", "계면 축 (47종 post-hoc)"),
    ("cascade_audit_ml_validation", "cascade_audit_ml_validation", "ML 검증 · acquisition"),
]
#: 공개 표 — Round-3 의 gate denominator 계약이 정본이다 (record_present ≠ method_valid).
SUPPORTING = ["cascade_seminar_gate_denominators_round3.csv",
              "cascade_audit_gate_completeness.csv"]
#: 종명이 들어간 감사 산출물 — 공개 금지, acquisition 전용
DIAGNOSTIC_ONLY_AUDIT = [
    ("cascade_audit_g3_phase_set.csv", "G3 phase-set (종명 포함)"),
    ("cascade_audit_g4_rescore.csv", "G4 재점수 (종명 포함)"),
]

#: 플로터가 쓰던 계약 블록 — 이제 여기가 원본이다 (전엔 두 도구가 각자 썼다).
METRIC_CONTRACT = {
    "G3": {
        "display_name": "MP phase-set onset",
        "historical_host_onset_V": 2.140,
        "alternate_host_onset_V": 2.256,
        "rule": "compare candidate and host within the same phase_set_id",
        # ★ 2026-08-16 — 세 층을 따로 센다. 옛 판은 셋을 'method-comparable 0' 하나로 뭉쳤다.
        "record_present_species": 90,
        "phase_set_comparable_pairs": "270/270",
        # ★ 2026-08-16 재감사 — 한 숫자로 덮지 않는다. 세 축이 서로 다른 상태다.
        "operational_factorial_coverage": "17/17 chain rows",
        "element_level_causal_attribution": "not_claimed",
        "structural_realization_validated": "0/11",
        "matched_transform": {"exact": 10, "multi_transform": 7,
                              "multi_transform_species": ["B2O3", "MoO3", "WO3"]},
        "record_vs_comparable": ("'기록이 있다' ≠ '같은 방법으로 비교했다' ≠ '효과를 귀속할 수 있다'. "
                                 "phase_set_id 기록 + 같은 실행 host 로 두 번째 층은 닫혔다. "
                                 "세 번째 층은 열려 있다 — chain generator 17행 중 10행만 plain 형제와 "
                                 "정확히 ΔLi=-1·ΔS=-1·ΔCl=+1 이고, 7행(B2O3·MoO3·WO3)은 치환 자리와 "
                                 "Li/P 화학량론까지 다르다. plain 도 host 대비 여러 원자가 함께 바뀌므로 "
                                 "'dopant effect' 가 아니라 'recipe-level host contrast' 다."),
        "lis4_exposure": {"onset_reactions_containing_LiS4": 124, "of_records": 270},
    },
    "G4": {
        "display_name": "legacy BVS + 4A foreign-center composite",
        "blocking_definition": "fraction of Li within 4 A of atoms outside {Li,P,S,Cl}",
        "historical_rule": "blocking<0.60 ? 0.10+0.90*minmax(BVS) : 0.05",
        "circularity": ("blocking 컷 탈락자는 BVS 값이 버려지고 norm 이 0.05 로 강제된다. "
                        "컷 0.30 보다 낮으므로 blocking 탈락 = G4 탈락이 결정론적으로 따라온다. "
                        "두 독립 신호의 AND 로 읽으면 안 된다."),
        "pool_relative": ("min-max 정규화라 같은 종의 점수가 로스터에 따라 움직인다 — "
                          "B2O3 blocking-free 는 historical 47 풀에서 0.1000, "
                          "recovered 88 풀에서 0.1998 이다 (둘 다 fail)."),
        "not_equivalent_to": ["canonical BVSE", "migration barrier", "diffusivity", "conductivity"],
    },
    "G5": {
        "display_name": "UMA relaxed-ion elastic screen",
        "presence_vs_validity": ("field presence 로 세면 88/1/1 이지만, 비물리 탄성"
                                 "(B_hill·G_hill ≤ 0) 을 거르면 all-label-valid 86 · "
                                 "partial AlBr3|MgI2|Na2S · dropped AlI3 · usable 89 다."),
        "reciprocal_metric_warning": ("열 이름은 pugh 지만 값은 G/B 다. B/G 는 행별로 뒤집은 뒤 "
                                      "통계를 내야 한다 — 1/mean(G/B) ≠ mean(B/G)."),
    },
}
DATASETS = {
    "historical_47": {
        "approval_status": "historical", "use_scope": "archive_only",
        "species_count": 47, "slot_count": 141, "actual_x": 0.25,
        "pool_id": "cascade-v23-o37-f10-2026-06",
        "phase_set_id": None,
        "phase_set_assumption": "mp-gga-gga-u__lis4-included (가정 — 행 단위 기록 없음)",
        "limitations": ["historical campaign snapshot", "pool-relative ranks",
                        "not current campaign coverage"],
    },
    "recovered_90_gp": {
        "approval_status": "recovered_unvalidated", "use_scope": "diagnostic_only",
        "species_count": 90, "actual_x": 0.25,
        "pool_id": "cascade-v23-completed-90-2026-07",
        "phase_set_id": None,
        "phase_set_assumption": "mp-gga-gga-u__lis4-included (가정 — 행 단위 기록 없음)",
        "overlap_with_historical": 141, "overlap_oxidation_drift_count": 0,
        "limitations": ["not fully re-ranked or re-gated", "G3 phase-set identity absent",
                        "G4 must be rebuilt with canonical softBV"],
    },
    "current_approved_leaderboard": {
        "approval_status": "approved", "use_scope": "blocked",
        "species_count": 0,
        "limitations": ["존재하지 않는다 — 승인된 current ranking 은 0종이다"],
    },
}


def _pinned_source_hashes() -> dict:
    """고정 커밋 blob 의 해시 — 패널 입력이 조용히 바뀌지 않았는지의 근거."""
    import subprocess
    out = {}
    for rel in ("db/properties/oxidation_stability_cascade_v2.json",
                "db/properties/cascade_v23_all.csv",
                "db/properties/oxidation_stability_cascade.json"):
        try:
            b = subprocess.check_output(["git", "show", f"{PINNED_SOURCE_COMMIT}:{rel}"],
                                        cwd=ROOT, stderr=subprocess.DEVNULL)
            out[rel] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                        "sha256_lf": hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()}
        except Exception as e:
            out[rel] = {"error": f"고정 blob 을 못 읽었다: {type(e).__name__}"}
    return out


# ══════════════════════════════════════════════════════════════════════════
# 실행 **전** 봉인 (회신 AL 해제조건 #7 · 2026-09-08)
#
#   왜 이 도구냐 — 이 파일이 cascade 원장의 **단독 소유자**다. 봉인을 딴 데 두면
#   원장이 둘로 갈라진다(이 도구가 생긴 이유가 정확히 그 사고였다).
#
#   ⛔ **봉인은 실행보다 시간상 앞설 때만 의미가 있다.** 돌린 뒤에 해시를 뜨면 그건
#     "지금 이 순간의 코드" 지문이고, 그 사이 코드가 바뀌었을 수도 — 더 나쁘게는
#     결과가 이상해서 손댔을 수도 — 있다. 그래서 `--seal` 은 실행 **전에** 부른다.
#
#   ⛔ 이 봉인이 **못 하는 것**
#     · 규칙이 옳은지 판정하지 않는다. repo 에 적힌 것을 그대로 옮길 뿐이다.
#     · 없는 규칙을 만들어내지 않는다 — 안 정해진 것은 `"미정"` 으로 봉인한다.
#       (없는 걸 있는 것처럼 적는 것이 봉인을 무의미하게 만드는 제일 빠른 길이다.)
#     · 실행이 실제로 이 코드를 썼는지 보장하지 않는다. 대조는 회수 단계 몫이다.

#: 봉인 대상 코드 — 구조 builder · 런처 · 원장 생성기 (AL #7)
SEAL_SOURCES = (
    "tools/doping/tier_cascade.sh",
    "tools/doping/master_batch_273.sh",
    "tools/doping/run_anneal.py",
    "tools/doping/b2o3_enumerate.py",
    "tools/doping/collect_dataset.py",
    "tools/doping/axis_corr_csv.py",
    "tools/doping/combine_rankings.py",
    "tools/cascade/build_cascade_audit_manifest.py",
    "tools/ionic/msd_diffusive_check.py",
)

#: 봉인 대상 **규칙** — AL #7 이 지목한 다섯. 값은 repo 실물에서 옮긴다.
#:   ⚠ `상태` 가 "미정" 인 것은 **정말로 정해진 게 없는 것**이다. 채워 넣지 않는다.
def _seal_rules() -> dict:
    return {
        "framework_retention": {
            "상태": "정해짐",
            "출처": "tools/ionic/msd_diffusive_check.py:307-311 · framework_check()",
            "규칙": ("원소별 severity 의 최대로 판정한다. β ≥ 0.60 또는 ratio_to_Li ≥ 0.25 → "
                     "framework_melting · β ≥ 0.30 또는 ratio ≥ 0.10 → framework_mobile · "
                     "그 외 framework_rigid. 원자 8개 미만 원소는 판정에서 빼되 보고는 한다."),
            "문턱": {"BETA_RIGID": 0.30, "BETA_MELT": 0.60, "MIN_N": 8,
                     "WARN_RATIO": 0.10, "FAIL_RATIO": 0.25},
            "⚠": "종별 MSD 가 없으면 **판정 불가**(None)다. traj.xyz 없는 런은 원리적으로 못 본다.",
        },
        "phase_melting": {
            "상태": "정해짐 (2026-09-08 결정)",
            "출처": "framework_check() + 비준 카드 cascade_d_rel_estimand_2026_09_08.json §1",
            "규칙": ("골격 판정이 `framework_mobile` 또는 `framework_melting` 이면 "
                     "**그 설계는 `no_value`** 다."),
            "왜_이렇게_되나": ("비준 카드가 보고량을 **600 K 단일 온도**로 한정했다. 온도가 하나라 "
                              "'그 온도를 아레니우스에서 뺀다'(다온도 규칙)가 성립하지 않는다 — "
                              "뺄 온도가 그 설계의 전부이므로 값이 없는 것이다."),
            "⚠": "다온도 규칙(D-2026-09-04-lpsocl-box331-400ps-uniform)은 **이 캠페인에 해당 없음**.",
        },
        "beta_hop": {
            "상태": "정해짐 (2026-09-08 결정 · LPSOCl 문턱 승계)",
            "출처": "kb/concepts/beta-gate.md §7-5(2026-08-26) · §7-8b(회신 F) + "
                    "lpsocl_box331_closure_conditions_2026_09_07.json C2",
            "규칙": ("판정축은 ① D_inc plateau ② 창 안정성 ③ 홉 수. **β 는 경보로만.** "
                     "plateau 문턱은 LPSOCl 을 승계한다 — 4창 "
                     "`((2,50),(10,50),(25,100),(50,100))` **전부**에서 상대산포 ≤ **10 %**."),
            "⛔_생산시간_단서": ("생산시간이 4창을 다 덮어야 한다(≥100 ps). 안 덮으면 그 창은 "
                                "**조용히 빠지는 것이 아니라 '판정 불가'로 센다.** "
                                "LPSOCl 200 ps 에서 `_covers` 가 `(50,100)` 을 조용히 빼는 바람에 "
                                "온도마다 창 수가 달랐고, 그걸 모른 채 세 점을 한 직선에 올렸다."),
            "⛔_폐기": ("`β ≥ 0.80` 고정문턱을 **판정으로 인용 금지**. 우리 운영점에서 "
                        "거짓탈락률 50 % 다 (citation_hazards: HZ-beta-hard-gate)."),
        },
        "mlip_applicability": {
            "상태": "정해짐 (2026-09-08 결정 — **서술 범위를 낮추는 쪽으로**)",
            "출처": "kb/concepts/md.md:36-37 · CLAUDE.md 데이터 규율 + 비준 카드 §6",
            "규칙": ("UMA-s-1p1(omat)은 LPSCl 계열 MD 의 검증된 표준이고 **Li₃N 에는 사용 금지**. "
                     "cascade 도판트 30종에 대한 UMA 검증은 **없다** — 따라서 이 캠페인의 결과는 "
                     "**'UMA 내부 순위'로만 서술한다.** 물리 예측(실제 확산 순위)으로 올리지 않는다."),
            "⚠_왜_이_선택인가": ("점수(UMA)와 검증 D(UMA-MD)가 같은 퍼텐셜이라, UMA 가 이 화학에서 "
                                "계통적으로 틀리면 둘이 함께 틀리고 **상관은 오히려 좋아진다**. "
                                "그 구멍을 계산 없이 메울 방법은 없으므로, 메우는 대신 **주장을 낮춘다.**"),
            "재개_조건": ("cascade 도판트 화학의 대표 부분집합에서 **UMA vs DFT 힘 대조**를 통과하면 "
                          "그때 서술을 물리 예측으로 올린다. 도구는 이미 있다 "
                          "(`generate_dft_inputs.py --from_traj` + `mlip_committee.py force_contrast`)."),
        },
        "invalid_run": {
            "상태": "정해짐 (2026-09-08 결정 — 신설)",
            "출처": ("(repo 에 없어서 신설) 선례: 힘 대조 카드 §8 '20점 중 하나라도 실패한 채 "
                     "19점으로 판정하지 않는다' · LPSOCl 닫힘조건의 값/HOLD/no_value 3분법"),
            "규칙": ("설계마다 **생산자가** 3상태를 붙인다. "
                     "`ok`(4축 전부 성공 → front 후보) · "
                     "`partial`(일부 축 실패 → **front 후보에서 제외**, 실패 축을 기록) · "
                     "`failed`(구조/어닐 단계 실패 → 제외). "
                     "재실행은 **1회만**, 사전 선언한 것만. "
                     "그리고 **제외된 개수와 사유를 반드시 같이 보고한다** — 227 중 몇이 살아남았는지가 "
                     "front 해석에 필요하다."),
            "⛔_폐기한_옛_관행": ("*'소비자가 걸러야 한다'*. 산출물 원장이 "
                                 "`cascade_v23_champions_v2.csv` 한계에 그렇게 적어 뒀는데, 실제로는 "
                                 "안 걸러져서 **B_hill 음수 행(Na2S_x100)이 거짓 B/G = 2.50 을 만들어** "
                                 "랭킹에 들어갔고 연성 주장을 철회해야 했다. "
                                 "실패는 **생산자가 표시하고 구조적으로 제외**한다."),
        },
    }


def build_seal(label: str) -> dict:
    """실행 전 봉인 — 코드 지문 + 규칙 문장. → dict"""
    src = {}
    for rel in SEAL_SOURCES:
        p = ROOT / rel
        if not p.is_file():
            src[rel] = {"error": "파일 없음 — 봉인 대상 목록이 실물과 어긋났다"}
            continue
        b = p.read_bytes()
        src[rel] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    rules = _seal_rules()
    undecided = [k for k, v in rules.items() if "미정" in str(v.get("상태", ""))]
    partial = [k for k, v in rules.items() if any("미정" in x for x in v)]
    return {
        "schema": "cascade_prerun_seal/v1",
        "label": label,
        "sealed_at": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "⛔_봉인의_뜻": ("이 시각 **이후**의 cascade 실행은 이 봉인에 귀속된다. 봉인 뒤에 "
                         "아래 파일이나 규칙이 바뀌면 그 실행은 이 봉인으로 설명되지 않는다 — "
                         "새로 봉인하고 다시 돌려야 한다."),
        "provenance": _render_provenance(),
        "sources": src,
        "rules": rules,
        "⚠_미정_규칙": undecided,
        "⚠_부분미정_규칙": sorted(set(partial) - set(undecided)),
        "⛔_이_봉인이_보장하지_않는_것": [
            "규칙의 물리적 타당성 (repo 에 적힌 것을 옮겼을 뿐)",
            "실행이 실제로 이 코드를 썼는지 (대조는 회수 단계 몫)",
            "미정 규칙이 나중에 어떻게 정해질지",
        ],
    }


def _recovered_artifact_status() -> dict:
    """회수 sidecar 의 현재 상태 — 행수·해시와 **무엇이 결측인지**."""
    out = {}
    audit_p = PROP / "cascade_pool_audit_v2.json"
    audit = json.loads(audit_p.read_text(encoding="utf-8")) if audit_p.is_file() else {}
    gc = PROP / "cascade_audit_gate_completeness.csv"
    per_gate = {}
    if gc.is_file():
        import csv as _csv
        for r in _csv.DictReader(gc.read_text(encoding="utf-8").splitlines()):
            per_gate[r["gate"]] = {
                "all_label_complete_species": r["all_label_complete_species"],
                "partial": r["partial_species"], "dropped": r["dropped_species"],
                "approved_for_current_ranking": r["approved_for_current_ranking"],
                "method_status": r["method_status"],
                "completeness_basis": r.get("completeness_basis", ""),
                "validity_aware_all_label_species": r.get("validity_aware_all_label_species", ""),
            }
    for fn in ("cascade_v23_champions_v2.csv", "cascade_v23_litransport_v2.csv",
               "oxidation_stability_cascade_v2.csv", "cascade_v23_ranked_v2.csv"):
        p = PROP / fn
        if p.is_file():
            out[f"db/properties/{fn}"] = _meta(p, csv_rows=True)
    out["_gate_completeness"] = per_gate
    out["_ingestion_audit"] = {k: audit.get(k) for k in
                               ("n_esw", "n_evaluable", "n_complete", "dropped", "partial")}
    out["_note"] = ("행이 있다 ≠ 비교 가능하다. G3 는 record-complete 90 인데 "
                    "phase-set comparable 270/270 이지만 효과 귀속은 0/17 이다 "
                    "(chain generator 17행 중 exact 대응 10 · multi-transform 7).")
    return out


def _render_provenance() -> dict:
    """어느 폰트로 그렸는지. 폰트가 바뀌면 PNG 바이트가 바뀌므로 무결성의 전제다."""
    try:
        import sys as _s
        _s.path.insert(0, str(ROOT))
        from tools.figures.plot_cascade_audit_2026_08 import resolved_font
        font = resolved_font()
    except Exception as e:
        font = f"확인 불가 ({type(e).__name__})"
    return {"figure_font": font,
            "note": ("옛 판은 C:/Windows/Fonts/arial.ttf 하나에 묶여 있어 Linux 에서 "
                     "도구가 아예 안 돌았다. 지금은 Arial → Liberation Sans(메트릭 호환) "
                     "→ DejaVu Sans 폴백이다. 폰트가 다르면 PNG 해시가 달라지므로 "
                     "재생성 시 원장을 같이 갱신해야 한다.")}


def _meta(path: Path, csv_rows=False) -> dict:
    """sha256 · bytes (· 주석 제외 데이터 행수).

    ⚠ CRLF 이식성 (Codex Round-3 P1): 깨끗한 Windows checkout 에서 CSV 가 CRLF 로
    변환되면 바이트 해시가 달라진다. `.gitattributes` 로 `db/properties/*.csv|json` 을
    `eol=lf` 로 고정했고, 여기서는 **정규화 해시**도 같이 실어 둘 다로 검증할 수 있게 한다.
    """
    b = path.read_bytes()
    it = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
          "sha256_lf": hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()}
    if csv_rows:
        lines = [x for x in b.decode("utf-8-sig").splitlines()
                 if x and not x.startswith("#")]
        it["rows"] = max(0, len(lines) - 1)
    return it


def build(audit: dict) -> dict:
    arts = []
    for fn, appr, scope, desc, lims, src, derived, why in ARTIFACTS:
        p = PROP / fn
        if not p.is_file():
            continue
        assert appr in APPROVAL_STATUS, f"알 수 없는 approval_status: {appr}"
        assert scope in USE_SCOPE, f"알 수 없는 use_scope: {scope}"
        a = {"artifact_id": f"cascade-v23-{p.stem}",
             "source_path": f"db/properties/{fn}",
             "approval_status": appr, "use_scope": scope, "description": desc,
             "actual_x": 0.25, "campaign_labels": ["x002", "x005", "x010"],
             "source_commit": src, "limitations": lims, **_meta(p, csv_rows=fn.endswith(".csv"))}
        if derived:
            a["derived_from"] = derived
            a["override_reason"] = why
        arts.append(a)

    figs = []
    for name, csvname, title in FIGURES:
        img, tab = FIGD / f"{name}.png", PROP / f"{csvname}.csv"
        if not (img.is_file() and tab.is_file()):
            continue
        im, tb = _meta(img), _meta(tab, csv_rows=True)
        fig = {"panel": name, "title": title,
               "image": f"docs/figures/cascade/{img.name}",
               "csv": f"db/properties/{tab.name}",
               "approval_status": "audit_current", "use_scope": "default_visible",
               "source_commit": PINNED_SOURCE_COMMIT}
        if tab.name in AMENDED_CSV:
            fig["csv_source_commit"] = "regenerated by plot_cascade_audit_2026_08.py (2026-08-14)"
            fig["csv_derived_from"] = PINNED_SOURCE_COMMIT
            fig["csv_override_reason"] = AMENDED_CSV[tab.name]
        figs.append({**fig,
                     "image_sha256": im["sha256"], "image_bytes": im["bytes"],
                     # ⚠ 2026-08-16 — companion CSV 는 **텍스트**다. Windows 깨끗한 checkout
                     #   에서 CRLF 로 나오므로 artifact 처럼 LF 정규화 해시를 같이 싣는다.
                     #   PNG 은 바이너리라 원문 해시만이 맞다.
                     "csv_sha256": tb["sha256"], "csv_sha256_lf": tb["sha256_lf"],
                     "csv_bytes": tb["bytes"], "csv_rows": tb["rows"]})

    # 종명이 든 진단 PNG — **미등록 거부**가 아니라 diagnostic_only 로 명시한다.
    #  (미등록이면 "왜 막혔는지" 가 '원장에 없다' 로만 나와서 정책 의도가 안 보인다.)
    for stem, title in (("cascade_audit_g3_phase_set", "G3 phase-set (종명 포함)"),
                        ("cascade_audit_g4_rescore", "G4 재점수 (종명 포함)")):
        img = FIGD / f"{stem}.png"
        if img.is_file():
            arts.append({"artifact_id": f"cascade-v23-{stem}-png",
                         "source_path": f"docs/figures/cascade/{stem}.png",
                         "approval_status": "audit_current", "use_scope": "diagnostic_only",
                         "description": f"{title} — 공개 금지, acquisition 전용",
                         "actual_x": 0.25, "campaign_labels": ["x002", "x005", "x010"],
                         "source_commit": "regenerated by plot_cascade_audit_2026_08.py (2026-08-14)",
                         "derived_from": PINNED_SOURCE_COMMIT,
                         "override_reason": "Round-3: 후보 identity 는 acquisition 전용. 공개판은 익명본.",
                         "limitations": ["후보 이름이 그림에 그대로 있다"],
                         **_meta(img)})

    sup = []
    for fn in SUPPORTING:
        p = PROP / fn
        if p.is_file():
            it = {"path": f"db/properties/{fn}",
                  "approval_status": "audit_current", "use_scope": "default_visible",
                  "source_commit": PINNED_SOURCE_COMMIT, **_meta(p, csv_rows=True)}
            if fn in AMENDED_CSV:
                it["source_commit"] = "regenerated by plot_cascade_audit_2026_08.py (2026-08-14)"
                it["derived_from"] = PINNED_SOURCE_COMMIT
                it["override_reason"] = AMENDED_CSV[fn]
            sup.append(it)

    return {
        "property": "cascade_audit_manifest",
        "schema_version": 2,
        "artifact_id": "cascade-audit-2026-08-14",
        "owner": "tools/cascade/build_cascade_audit_manifest.py",
        "owner_note": ("이 파일의 writer 는 위 도구 **하나뿐**이다. plot_cascade_audit_2026_08.py 와 "
                       "rebuild_pool_inputs.py 는 sidecar 만 쓴다 (Codex Round-3 P0-1)."),
        "status": RELEASE_STATUS,
        "source_commit": PINNED_SOURCE_COMMIT,
        "source_commit_note": ("패널 고정 커밋. **artifact 마다 자기 source_commit 이 있고 "
                               "그쪽이 우선한다** — ranked_v2 는 Na₂S 정정 이후 산출물이다."),
        "source_of_truth": "docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md",
        "approval_status_vocabulary": list(APPROVAL_STATUS),
        "use_scope_vocabulary": list(USE_SCOPE),
        "headline": {
            "planned_slots": 273, "completed_slots": 270,
            "completed_species": audit["n_esw"],
            "historical_snapshot_species": 47,
            "approved_current_leaderboard_species": 0,
            "explicit_pair_property_labels": 0,
        },
        "headline_basis": ("273 = master_batch_273.sh 의 **91종 계획 입력 로스터** × 3 라벨. "
                           "⛔ 91종은 PLANNED INPUT ROSTER 이지 shortlist 가 아니다. "
                           "270 = enabled-workflow 완주 슬롯(As₂S₃ 3건 seed 실패). "
                           "completed_species 는 ESW 회수분에서 센다. "
                           "approved = 0 은 판정이다 — 결측이 아니라 점수·게이트 타당성이 미해결."),
        "actual_x": 0.25,
        "actual_x_note": ("라벨 x002/x005/x010 은 1×1×1 · 4 f.u. 셀의 정수 치환 때문에 "
                          "셋 다 실측 x=0.25 다. 농도 스윕도 반복실험도 아니다."),
        "host": {"formula_hint": "Li₆PS₅Cl 계열 (Cl:P = 1.0)",
                 "evidence": "ESW 반응식 좌변 Li22P4(S5Cl)4 계열",
                 "not": "Model C (Li₅.₄PS₄.₄Cl₁.₆) 가 아니다"},
        "datasets": DATASETS,
        "metric_contract": METRIC_CONTRACT,
        # ⬇ 2026-08-14 — 전엔 플로터 sidecar 에만 있던 두 블록. 원장이 단독 소유자이므로
        #   여기로 옮긴다. 없으면 "원장만 보면 된다" 가 성립하지 않는다.
        "source_hashes": _pinned_source_hashes(),
        "recovered_artifacts": _recovered_artifact_status(),
        "render_provenance": _render_provenance(),
        "artifacts": arts,
        "figures": figs,
        "supporting_tables": sup,
    }


def check(man: dict) -> list:
    """원장이 실제 파일과 맞는지. 반환값이 비어 있어야 통과."""
    bad = []
    for a in man.get("artifacts", []) + man.get("supporting_tables", []):
        rel = a.get("source_path") or a.get("path")
        p = ROOT / rel
        if not p.is_file():
            bad.append(f"{rel}: 파일 없음"); continue
        m = _meta(p)
        if m["sha256"] != a.get("sha256") and m["sha256_lf"] != a.get("sha256_lf"):
            bad.append(f"{rel}: 해시 불일치 (원문·LF정규화 둘 다)")
        if a.get("approval_status") not in APPROVAL_STATUS:
            bad.append(f"{rel}: 알 수 없는 approval_status {a.get('approval_status')!r}")
        if a.get("use_scope") not in USE_SCOPE:
            bad.append(f"{rel}: 알 수 없는 use_scope {a.get('use_scope')!r}")
    for f in man.get("figures", []):
        for key, hk, lfk in (("image", "image_sha256", None),
                             ("csv", "csv_sha256", "csv_sha256_lf")):
            p = ROOT / f[key]
            if not p.is_file():
                bad.append(f"{f[key]}: 파일 없음"); continue
            m = _meta(p)
            if m["sha256"] == f.get(hk):
                continue
            # 텍스트 companion 만 LF 정규화로 후퇴한다 (PNG 은 원문 해시가 정답)
            if lfk and f.get(lfk) and m["sha256_lf"] == f[lfk]:
                continue
            bad.append(f"{f[key]}: 해시 불일치"
                       + (" (원문·LF정규화 둘 다)" if lfk else ""))
    if len(man.get("figures", [])) != 5:
        bad.append(f"감사 패널이 {len(man.get('figures', []))}개다 — 정확히 5개여야 한다")
    return bad


def _selftest_seal(chk):
    """실행 전 봉인 (AL #7). ⛔음성 포함 — 봉인이 **거짓말하지 않는지**가 요점이다."""
    s = build_seal("_selftest")
    chk("봉인: 대상 코드 전부 지문이 떠진다",
        s["sources"] and all("sha256" in v for v in s["sources"].values()))
    chk("봉인: 규칙 5개가 실린다 (AL #7 목록)", len(s["rules"]) == 5)
    # 2026-09-08 결정으로 다섯 규칙이 전부 정해졌다 — 미정 목록은 비어 있어야 한다.
    #   ⚠ 이 시험은 "지금 다 정해졌나" 를 본다. 나중에 규칙을 새로 늘리면서 미정으로 두면
    #     여기서 걸린다 (그게 목적이다 — 미정인 채로 봉인하고 잊는 것을 막는다).
    chk("규칙 5개가 전부 정해졌다 (미정 0)", s["⚠_미정_규칙"] == [])
    chk("각 규칙에 출처가 달려 있다 (지어낸 규칙 금지)",
        all(str(v.get("출처", "")).strip() for v in s["rules"].values()))
    # ⛔음성 ①: **미정 탐지 기계가 살아 있어야 한다.** 위가 비었다고 검사가 죽으면 안 되므로
    #   합성 규칙으로 경로를 직접 친다 (특정 규칙에 묶으면 그 규칙이 정해지는 순간 시험이 죽는다).
    _orig_rules = globals()["_seal_rules"]
    globals()["_seal_rules"] = lambda: {"__synthetic__": {"상태": "⛔ **미정**",
                                                          "출처": "(없음)", "규칙": None}}
    try:
        s_syn = build_seal("_selftest_syn")
        chk("⛔음성: 미정 규칙이 있으면 미정 목록에 실린다 (탐지 기계 생존)",
            s_syn["⚠_미정_규칙"] == ["__synthetic__"])
        globals()["_seal_rules"] = lambda: {"__partial__": {"상태": "정해짐", "출처": "x",
                                                            "규칙": "y", "⚠_미정": "일부 없음"}}
        s_par = build_seal("_selftest_par")
        chk("⛔음성: 부분미정을 '정해짐' 으로 뭉개지 않는다",
            s_par["⚠_부분미정_규칙"] == ["__partial__"] and s_par["⚠_미정_규칙"] == [])
    finally:
        globals()["_seal_rules"] = _orig_rules
    # ⛔음성 ③: 폐기된 문턱(β ≥ 0.80)이 **판정 규칙 본문에 들어가면 안 된다.**
    #   ⚠ 초판은 값만 훑어서, 폐기 표시가 **키 이름**(`⛔_폐기`)에만 있으면 통과했다.
    #     키·값을 같이 보고, 그리고 "0.80 이 규칙 본문에 없는지" 를 직접 친다.
    _bh = s["rules"]["beta_hop"]
    chk("⛔음성: 폐기된 β 0.80 이 **규칙 본문**에 없다", "0.80" not in str(_bh.get("규칙", "")))
    chk("⛔음성: 폐기 사실이 봉인에 남는다 (키·값 어디든)",
        any("폐기" in str(k) or "폐기" in str(v) for k, v in _bh.items()))
    chk("β/hop 규칙이 승계 문턱(plateau ≤10 %)을 싣는다", "10 %" in str(_bh.get("규칙", "")))
    # ⛔음성 ④: 봉인이 자기 한계를 적는다 (무엇을 보장하지 않는가)
    chk("⛔음성: 봉인이 보장하지 않는 것을 명시한다",
        len(s.get("⛔_이_봉인이_보장하지_않는_것", [])) >= 3)
    # ⛔음성 ⑤: 없는 파일을 목록에 두면 error 로 드러나야 한다 (조용히 빠지면 안 된다)
    _orig = globals()["SEAL_SOURCES"]
    globals()["SEAL_SOURCES"] = _orig + ("tools/__없는파일__.py",)
    try:
        s2 = build_seal("_selftest2")
        chk("⛔음성: 봉인 목록에 없는 파일이 있으면 error 로 드러난다",
            "error" in s2["sources"].get("tools/__없는파일__.py", {}))
    finally:
        globals()["SEAL_SOURCES"] = _orig


def selftest() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '✗'} {name}")

    _selftest_seal(chk)

    # 양성
    audit = json.loads((PROP / "cascade_pool_audit_v2.json").read_text(encoding="utf-8"))
    man = build(audit)
    chk("빌드가 5개 패널을 싣는다", len(man["figures"]) == 5)
    chk("플로터 계약 블록이 전부 있다",
        all(k in man for k in ("datasets", "metric_contract", "artifacts",
                               "figures", "supporting_tables")))
    chk("headline 키가 플로터가 대조하는 6개다",
        set(man["headline"]) == {"planned_slots", "completed_slots", "completed_species",
                                 "historical_snapshot_species",
                                 "approved_current_leaderboard_species",
                                 "explicit_pair_property_labels"})
    rk = [a for a in man["artifacts"] if a["source_path"].endswith("ranked_v2.csv")][0]
    chk("ranked_v2 에 자기 source_commit 이 있다", rk["source_commit"] == NA2S_FIX_COMMIT)
    chk("ranked_v2 에 derived_from·override_reason 이 있다",
        rk.get("derived_from") == PINNED_SOURCE_COMMIT and rk.get("override_reason"))
    chk("승인된 current ranking 은 0", man["headline"]["approved_current_leaderboard_species"] == 0)
    chk("정상 원장은 check 를 통과한다", check(man) == [])

    # ── 음성 (틀린 입력을 잡아내는지) ──
    bad = json.loads(json.dumps(man))
    bad["artifacts"][0]["sha256"] = "0" * 64
    bad["artifacts"][0]["sha256_lf"] = "0" * 64
    chk("[음성] 해시 위조를 잡는다", any("해시" in x for x in check(bad)))

    bad2 = json.loads(json.dumps(man))
    bad2["artifacts"][0]["approval_status"] = "approved_by_nobody"
    chk("[음성] 어휘 밖 approval_status 를 잡는다",
        any("approval_status" in x for x in check(bad2)))

    bad3 = json.loads(json.dumps(man))
    bad3["artifacts"][0]["use_scope"] = "everyone_can_see_it"
    chk("[음성] 어휘 밖 use_scope 를 잡는다", any("use_scope" in x for x in check(bad3)))

    bad4 = json.loads(json.dumps(man))
    bad4["figures"] = bad4["figures"][:3]
    chk("[음성] 패널이 5개가 아니면 잡는다", any("패널" in x for x in check(bad4)))

    bad5 = json.loads(json.dumps(man))
    bad5["figures"][0]["image_sha256"] = "0" * 64
    chk("[음성] 그림 해시 위조를 잡는다", any("해시" in x for x in check(bad5)))

    # CRLF 이식성: LF 정규화 해시로도 통과해야 한다
    crlf = json.loads(json.dumps(man))
    p = ROOT / crlf["artifacts"][0]["source_path"]
    if p.suffix == ".csv":
        crlf["artifacts"][0]["sha256"] = hashlib.sha256(
            p.read_bytes().replace(b"\n", b"\r\n")).hexdigest()
        chk("[CRLF] 원문 해시가 달라도 LF 정규화로 통과한다", check(crlf) == [])
    # figure companion CSV 도 같은 규칙이어야 한다 (2026-08-16 — 여기만 raw 였다)
    figs = [f for f in man.get("figures", []) if (ROOT / f["csv"]).is_file()]
    if figs:
        cf = json.loads(json.dumps(man))
        cf["figures"][0]["csv_sha256"] = hashlib.sha256(
            (ROOT / figs[0]["csv"]).read_bytes().replace(b"\n", b"\r\n")).hexdigest()
        chk("[CRLF] figure companion CSV 도 LF 정규화로 통과한다", check(cf) == [])
        cf2 = json.loads(json.dumps(man))
        cf2["figures"][0]["csv_sha256"] = "0" * 64
        cf2["figures"][0]["csv_sha256_lf"] = "0" * 64
        chk("음성: figure CSV 둘 다 틀리면 잡는다", check(cf2) != [])
        cf3 = json.loads(json.dumps(man))
        cf3["figures"][0]["image_sha256"] = "0" * 64
        chk("음성: PNG 은 LF 후퇴가 없다", check(cf3) != [])

    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="쓰지 않고 기존 원장만 검증")
    ap.add_argument("--seal", metavar="LABEL",
                   help="실행 **전** 봉인을 쓴다 (AL 해제조건 #7). "
                        "예: --seal v2_2026_09_08 → db/properties/cascade_seal_<LABEL>.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.seal:
        seal = build_seal(a.seal)
        p = PROP / f"cascade_seal_{a.seal}.json"
        if p.exists():
            print(f"⛔ 이미 있다: {p}\n   봉인을 덮어쓰지 않는다 — 덮어쓰면 '언제 봉인했나' 가 "
                  "사라지고 봉인이 무의미해진다. 새 LABEL 을 쓰거나 옛 봉인을 보존한 채 두어라.")
            return 1
        p.write_text(json.dumps(seal, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        miss = [k for k, v in seal["sources"].items() if "error" in v]
        print(f"[봉인] {p}")
        print(f"       코드 {len(seal['sources']) - len(miss)}개 지문"
              + (f" · ⛔ 못 찾은 파일 {len(miss)}: {miss}" if miss else ""))
        print(f"       규칙 {len(seal['rules'])}개 — "
              f"⛔ 미정 {seal['⚠_미정_규칙']} · ⚠ 부분미정 {seal['⚠_부분미정_규칙']}")
        print("       ⚠ 이 시각 **이후**의 실행만 이 봉인에 귀속된다.")
        return 1 if miss else 0
    if a.check:
        if not OUT.is_file():
            print(f"⛔ 원장이 없다: {OUT}"); return 1
        bad = check(json.loads(OUT.read_text(encoding="utf-8")))
        print("\n".join(f"  ⛔ {b}" for b in bad) if bad else "  ✓ 원장이 파일과 일치한다")
        return 1 if bad else 0

    audit_p = PROP / "cascade_pool_audit_v2.json"
    if not audit_p.is_file():
        print("⛔ cascade_pool_audit_v2.json 이 없다 — rebuild_pool_inputs.py 를 먼저 돌릴 것")
        return 1
    man = build(json.loads(audit_p.read_text(encoding="utf-8")))
    bad = check(man)
    if bad:
        print("⛔ 빌드 직후 검증 실패 (쓰지 않는다):")
        print("\n".join(f"   {b}" for b in bad))
        return 1
    OUT.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[manifest] {OUT}")
    print(f"           artifact {len(man['artifacts'])} · 패널 {len(man['figures'])} · "
          f"supporting {len(man['supporting_tables'])} · 승인 ranking "
          f"{man['headline']['approved_current_leaderboard_species']}종")
    return 0


if __name__ == "__main__":
    sys.exit(main())
