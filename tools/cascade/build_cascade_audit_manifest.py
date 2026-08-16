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
      "도펀트 없는 Cl-only host(Li23P4S19Cl5) 기준이 없어 Cl 분해 불가"],
     "regenerated by esw_cascade_batch.py --annotate (2026-08-16)", PINNED_SOURCE_COMMIT,
     "f9 재감사: composition_family_audit · matched_transform · dft_deep_composition_collision"),
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
    ("b2o3_esw.json", "historical", "archive_only",
     "legacy B2O3 ESW (DFT-deep 셀 Li58P8S41Cl16B2O3, onset 2.03 V)",
     ["method_status **unverified** — phase_set_id·entry_ids·MP 버전 없음",
      "캐스케이드 챔피언(Li17B2P4S16Cl5O3, 2.317 V)과 **다른 조성**이다",
      "부호 반전은 관측됐지만 원인을 조성 하나로 확정할 수 없다 (Codex f9 P0-2)",
      "도펀트 라벨(B2O3)만으로 validation join 금지"],
     "손으로 압축한 요약 (2026-06-29) — 생성기 없음", None,
     "f9 재감사: composition_collision_2026_08_16 로 '순전히 조성 차이' 철회"),
    ("cascade_screening_funnel.json", "historical", "archive_only",
     "47종 게이트 감사", ["G3 phase set 미기록", "G4 순환", "G5 로스터 상대"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_screening_funnel_v2.json", "recovered_unvalidated", "diagnostic_only",
     "89종 게이트 감사", ["위와 동일 + 풀 상대 정규화 재계산됨"],
     PINNED_SOURCE_COMMIT, None, None),
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


def selftest() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '✗'} {name}")

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
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
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
