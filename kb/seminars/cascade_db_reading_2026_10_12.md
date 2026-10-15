---
title: "cascade 원장 정독 — 단계별 커버리지 · 9월 재건 · 세미나 덱 정정 (2026-10-12)"
date: 2026-10-12
updated: 2026-10-12
tags: [cascade, ledger, audit, coverage, seminar, rebuild]
status: 진행
kind: seminars
system: cascade
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# cascade 원장 정독 — 2026-10-12

> **트랙 cascade · 1저자 = 사용자.** 결정이 그 자리에서 나고 통지할 제3자가 없다.
> 계기: 사용자 10-12 — 대본의 *"91개 전구체 중 89개 … 3,615개"* 를 보고 *"2개는 왜 빠졌지? 우리 추가하지 않았었나 다시 봐봐"* ·
> *"예전 cascade 관련해서 db 정독하고 와"* · *"최신화 된 내용들이 많고 지금 돌아가고 있는 cascade script들도 그 이후의 것들이라서 확실하게 갱신해야돼"*.
> 이 노트는 **숫자를 담지 않는다** — 숫자는 경로로만 가리킨다 (아래 셈은 전부 원장 파일에서 직접 셌고, 같은 셈을 `kb/seminars/export_cascade_briefing_csvs_2026_10.py` 의 p06 · p07 이 한다).

## 0. 한 줄

- **Stage 1(v23 탐색 스크린)은 91 전구체 전부 완화했다** — 8월 재실행(`as2s3_recover`)이 As₂S₃ · AlI₃ 를 채웠다. 3,615 + 60 = **3,675 구성** · 담금질 **693**.
- 그런데 **뒤 단계 표는 재실행 전에 만들어져** 90 (안정창 · 계면) · 89 (별도 상 · 게이트 평가) 에 멈춰 있다. 옛 대본의 "89/91" 은 이 89 를 '계산한 수' 로 읽은 것이다.
- Stage 1 은 **09-19 에 탐색 자료로 강등**됐고, 지금의 틀은 **9월 재건**이다 — 주 보고량 D_rel · 설계 목록 237 · S1 생성 계약 · 대표 = ΔE 중앙값 (09-12 비준) · S3 순위 규약 (09-19 제안 · δ 빈칸).
- **지금 kgy 에서 도는 cascade 스크립트(v7 본 라운드)는 그 재건 위의 파일럿**이다 (1000 K · 40 런 · `cascade_v7_main_runlog_2026_10_07.json`).

## 1. 시간순 (무엇이 언제 생겼나)

| 날짜 | 일 | 원장 |
|---|---|---|
| 05-26 → 06 | v23 본 배치 (multi_category_2026_05_26_v23) — 90 전구체 · 3,615 구성 · 681 담금질 | `db/properties/cascade_v23_all.csv` |
| 06-25 | O/F 47 종 스냅샷 (37 + 10) — 08-18 덱의 "47" 의 정체 | `cascade_v23_all_20260629_47species.csv` (파일 날짜 06-29) |
| 07-28 | 문헌식 게이트 깔때기 (G1–G5) · 89 종 — 미검증 진단물 | `cascade_screening_funnel.json` · `_v2.json` |
| 08-14 | 풀 감사 v2 — ESW 90 → 게이트 평가 89 (AlI₃ 전부 빠짐 · MgI₂ 부분) | `cascade_pool_audit_v2.json` |
| 08-16 | 라벨 · 배치 흩어짐 감사 — x 라벨 셋 = 같은 수준 · 축별 within/between | `cascade_label_scatter_audit.json` |
| 08-18 | 세미나 덱 (사용자 업로드 · repo 밖) | — |
| 08-19 | 계면 표 90 종 (도핑 조성 vs 양극 · Li · 탄소) | `cascade_interface_90.jsonl` · `_li.jsonl` · `_carbon.jsonl` |
| 08-20~25 | **As₂S₃ · AlI₃ 재실행** — 원자가 표에 As(+5, +3) 추가 (`substitute_compound.py` 주석) · 60 구성 · 정본 표 자동 갱신 안 함 | `tools/doping/run_as2s3_recover.sh` |
| 08-25 | 302 캐스케이드 통합 표 — v23 3,615 + dualx 450 + 재실행 60 = 4,125 | `cascade_all_302_2026_08_25.csv` · `.json` |
| 09-08 | D_rel 보고량 카드 비준 | `cascade_d_rel_estimand_2026_09_08.json` · `D-2026-09-08-cascade-d-rel-estimand` |
| 09-09 | 별도 상 표 이름 변경 (`separate_phase` · 회신 BJ NO-GO · BK) — 도핑 자료가 아니다 | `cascade_stability_axes.csv` 머리말 |
| 09-12 | **재건 개정 넷 비준** (주목적 — 10-15 정정: 2단계 주 보고량 · 237 · S1 · 대표) + 축 전역 감사 + 재앵커 | `cascade_primary_objective_amendment_2026_09_12.json` · `cascade_design_roster_amendment_2026_09_12.json` · `cascade_s1_contract_amendment_2026_09_12.json` · `cascade_d_rel_amendment_2026_09_12.json` · `cascade_axis_global_audit_2026_09_12.json` · `cascade_reanchor_comp1k444_2026_09_12.json` |
| 09-13 | 파일럿 v4 (→ v5 로 대체) · §4b 셀 정책 '준비 미확보' 마감 · v5 E′ 카드 | `cascade_rebuild_estimand_card_v4/v5_*.json` · `cascade_pilot_4b_closed_2026_09_13.json` |
| 09-19 | **v23 강등 원장화** · v6 카드 (10 부모 · 600 K) · S3 순위 규약 **제안** · v5 라운드 1 (자격 0/30 · 궤적 미저장) | `cascade_v23_demoted_2026_09_19.json` · `cascade_estimand_card_v6_10parents_2026_09_19.json` · `cascade_s3_protocol_amendment_2026_09_19.json` |
| 09-22 / 09-23 | ESW 정정 A (356 행 재유도) · 산물 갭 HOLD | `oxidation_stability_cascade_v3_pinned.json` `⛔_window_V_정정_2026_09_22` · `HZ-cascade-product-gaps-nonground-polymorph` |
| 10-01 | **v6 마감 (방법상 무효 · 자격 0/40)** · OCV 빈칸 = 안정창 없음 (82 행 · 깔때기 21) · v7 탐침 카드 | `cascade_d_rel_closed_2026_10_01.json` · `D-2026-10-01-cascade-esw-no-stable-window` · `D-2026-10-01-cascade-v7-probe-card` |
| 10-03 → 10-06 | v7 개정 CP · 탐침 → T* = 1000 K | `cascade_estimand_card_v7_probe_amendment_cp_2026_10_03.json` · `D-2026-10-03-cascade-v7-amend-cp` |
| 10-07 → 10-12 | v7 본 라운드 상한 비준 · 발사 · kgy 재부팅 뒤 이어받기 (12/40) | `D-2026-10-07-cascade-v7-main-round-cap` · `cascade_v7_main_runlog_2026_10_07.json` |

## 2. 원장 지도 — 무엇이 어느 층인가

| 층 | 원장 | 지위 |
|---|---|---|
| Stage 1 구성 (구조 · 지표) | `cascade_all_302_2026_08_25.csv` (통합 · 정본 셈) · `cascade_v23_all.csv` (본 배치만) | 탐색 자료 (09-19 강등) |
| Stage 1 파생 (순위 · 챔피언 · 테마) | `cascade_v23_ranked_v2.csv` · `_champions_v2.csv` · `_litransport_v2.csv` · `cascade_v23_themes.json` · `cascade_screening_funnel_v2.json` | 탐색 · 깔때기는 *미검증 진단물* (머리말이 게이트 통과 수 인용 금지) |

> 2026-10-14: 순위 표는 같은 도구로 8월 입력에서 바이트까지 재현된다. 재실행 둘 (As₂S₃ · AlI₃) 을 더한 91 판 = `seminar_2026_10_13_cascade/p07_stage1_composite_score_91.csv` (탐색 · 진단 전용 · 머리말에 결함 목록). 8월 챔피언 행은 지금 원장 순위 1 행과 89 개 중 43 개에서 다르다 (안 바꿨다). 에너지 항 `de` 는 원자당 에너지를 호스트와 바로 뺀 값이라 조성이 다른 전구체끼리는 넣은 원소의 결합 세기가 섞인다.
| 안정창 | `oxidation_stability_cascade_v3_pinned.json` | 정정 정의 (ox − OCV · 빈칸 = 창 없음) |
| 계면 (도핑 조성) | `cascade_interface_90.jsonl` · `_li.jsonl` · `_carbon.jsonl` | 반응에너지 · 계산 끝 |
| 별도 상 (전구체 자체) | `cascade_stability_axes.csv` · 산물 갭 `cascade_product_gaps.json` | 코팅·이차상 후보 목록 · 산물 갭 **HOLD** |
| 농도 세트 | `cascade_all_302_2026_08_25.csv` family `dualx_v23` | 탐색 · 미완 (§4) |
| 재건 규칙 | 위 09-12 개정 넷 · S3 제안 | 비준 넷 · S3 제안 |
| 파일럿 | v4 → v5 E′ → v6 (마감) → v7 (진행) | v7 만 살아 있다 |
| 화면 | `/cascade` — 강등 기록을 화면이 읽는다 | — |

## 3. 커버리지 — 91 중 각 표가 담은 수 (원장에서 직접 셈)

정본 셈은 `db/properties/seminar_2026_10_13_cascade/p07_stage1_coverage_by_ledger.csv` (생성기가 매번 원장에서 다시 센다). 요약:

| 단계 · 표 | 전구체 | As₂S₃ | AlI₃ |
|---|---|---|---|
| 배치 열거 + MLIP 완화 (본 배치 + 재실행) | 91 | ✅ | ✅ |
| 짧은 담금질 | 91 | ✅ | ✅ |
| 안정창 (`v3_pinned` + 10-14 As₂S₃ 보충) | 91 | ✅ | ✅ |
| 계면 · 도핑 조성 vs 양극 / Li / 탄소 | 91 | ✅ | ✅ |
| 별도 상 (`stability_axes`) | 89 | ❌ | ❌ |
| 게이트 깔때기 (`funnel_v2`) | 89 | ❌ | ❌ |

- ✅ **10-14 보충** (gabia · MP db 2026.04.13 = 90 종과 같은 판 · `db/inputs/cascade_as2s3_mp_2026_10_13/run_gabia.sh` · 결과 커밋 9225dd9): As₂S₃ 안정창 (rank 1 세 행 · `oxidation_stability_cascade_as2s3_addendum_2026_10_13.json`) · 계면 (양극 셋 · Li · 탄소 — `--only As2S3:As2Cl4Li28P2S20`) · 계면 산물 밴드갭 재생성 (HOLD 유지 — `HZ-cascade-product-gaps-nonground-polymorph` ✅_재생성_2026_10_14_gabia). AlI₃ 1순위 배치의 UMA 지표는 GPU 일이라 남았다.

- As₂S₃ 가 처음 빠진 이유: 원자가 표(`ALTERNATIVE_VALENCES`)에 As 가 없어 +5 로만 가정 → As₂S₃ 단위 전하 +4 → stage-01 구조 0 개. **물리 판정이 아니라 사전 누락**이었다 (`tools/doping/substitute_compound.py` 주석). 재실행: 45 구성 (P 4b × Cl 4d / S 16e / S 4a) · 전부 수렴 · 9 담금질.
- AlI₃: 본 배치 15 + 재실행 15. 순위 1 배치에 탄성 · EOS · BVS 가 없다 (순위 2 에는 있다) — `cascade_pool_accounting.csv` `drop_reason`.
- `cascade_pool_accounting.csv` 는 재실행 **전** 상태를 적은 집계표다 — 10-12 에 머리말 주석으로 표시했다 (TOTAL 89 는 '게이트 평가 수' 로 읽는다).

## 4. dualx — 진짜 농도를 바꾼 작은 세트

- 16 f.u. 셀(2×2×1)에서 x = 0.0625 (305 구성) · 0.25 (145 구성) · 13 전구체 · 17 조성 (Cl-rich 포함 · TiF₄ 빼면 산화물) · 담금질 65.
- 지표가 덜 찼다 (BVSE 48/450 행 · EOS 31 행). 같은 부피 앵커(27.478)를 썼다 (`cascade_base_strain_2026_09_12.json` '27478 을 쓴 캠페인').
- ⇒ 탐색 · 미완. 세미나에서는 질문이 올 때만 말하고 '농도 효과' 로 말하지 않는다.

## 5. 9월 재건 — 지금의 틀 (요지만 · 원문은 각 개정)

1. **주목적** (⚠ 10-15 정정 `D-2026-10-15-cascade-objective-scope`: **2단계 주 보고량** — cascade 는 수송 한정이 아니고 D_rel 은 한 축) = `D_rel(design, host) = D*(design)/D*(host)` 의 설계 간 내부 비교 하나. B1(분해 산물 이동장벽)은 주축에서 빼고 목록으로 보존. 예측 점수 검증(ρ̂ + Fisher CI + 유효 표본수)은 별도 축.
2. **설계 목록 237** — 세는 단위 = 조성. 이름 문자열 단위 229 는 기각 (chain_Cl x 라벨 넷이 Cl 5·6·6·7 의 서로 다른 조성을 담고 있었다). ⛔ 237 ≠ 실행 — 실행 범위는 #7.
3. **S1 생성 계약** — 부모 자리 동결 승계 · 전체 보상 수지 (아니면 거부) · 농도 분자·분모 · 거부는 `is_physics_elimination: false` 로 따로 셈. 실측 결함 셋을 회귀시험으로 박았다. 구현 `tools/cascade/s1_contract.py` (`select_representative` 포함).
4. **대표 구조** = ΔE 중앙값을 낸 실제 행 (짝수 → 좌표 sha256 순) · 호스트도 같은 규칙. 최저는 탐색 예산의 함수 · 점수 중앙값은 검증 축과 순환.
5. **S3 순위 규약** — 제안 · δ 빈칸 · 1저자 결정. ⛔ 안의 E′ 수치는 다른 보고량의 산포라 인용 금지.
6. 파일럿 사슬: v4 (대체) → §4b 마감 → v5 E′ (0/30 · 궤적 없음) → v6 (0/40 · 방법상 무효 · 10-01 마감) → **v7** (무도핑 탐침 T* = 1000 K → 본 라운드 40 런 · 진행).

## 6. 세미나 덱 · 문서에서 고친 것 (10-12)

| 고친 것 | 전 | 후 |
|---|---|---|
| 완화 수 | 89 of 91 (As₂S₃ 유효 배치 없음 · AlI₃ 불완전) | 91 전부 (8월 재실행) · 뒤 단계 표 90 / 89 |
| 구성 · 담금질 수 | 3,615 · 681 | 3,675 · 693 (열지도 그림은 본 배치 3,615 그대로 · 캡션에 +60 표시) |
| 흐름 장 | 'Simulation workflow' 8 행 (수송 MD 포함) | 'Stage 1 — exploration screen' 7 행 + 재실행 · 강등 줄 |
| 새 장 | — | 11장 **September audit → Stage 2** (감사 넷 · 결과 전 규칙 다섯) |
| 안정창 | 89 조성 재계산 | 안정창 표 90 전구체 재계산 |
| 계면 | "dopant phase vs Li₆PS₅Cl, Li, cathodes" | 도핑 조성 vs LiCoO₂ · LiNiO₂ · LiMn₂O₄ · Li · 탄소 + 별도 상 표는 따로 (코팅 관점 · 도핑 자료 아님) |
| 다음 단계 | 축 합치는 선택 규칙 | 실행 범위(#7) · 순위 여유 δ · 예측 점수 검증 축 · As₂S₃ 전파 |
| CSV | p06 (89) · p12 · p17 | p06 (계획 · 완화 · 게이트) · **p07 커버리지** · p13 · p18 (감사 장 때문에 번호 이동) |

감사 장의 둘째 줄은 원장에서 **확정된 것까지만** 썼다: '기준 부피가 같은 조성의 DFT 평형보다 ~40 % 컸다' (27.478 vs 19.55 Å³/원자 · 재앵커 기록). '가짜 basin' 확정은 아니다 — 회신 BO 가 해석 절반을 가설로 강등했고, DFT 단일점이 남아 있다.

## 7. cascade 가 아닌 것 (덱에 안 넣음)

- **3가 도펀트 다축 비교 (09-16)** — `dopant_multiaxis_result_2026_09_16.json` · `dopant_screen_*_2026_09_16.json` 은 `system: cathode_cei` 다. CEI 트랙 (1저자 = 실험 쪽).
- `doping_cascade_trivalent_M3.json` · `doping_cascade_verified.json` 은 v23 의 부분 집합 (Stage 1 · 탐색 자료) — 강등을 같이 받는다.
- 6월 자리선호 배치 (`site_preference_raw_78.csv` · 백업 18장) 는 v23 와 **다른 계산**이다 (antisite 교환 · 세 점은 서로 다른 적재량 — 원자료 주석).

## 8. 열린 결정 (사용자 = 1저자)

1. **AlI₃ 순위 2 사용 여부** — 쓰면 AlI₃ 만 다른 배치에서 고른 종이 된다.
2. **As₂S₃ 하류 전파** — 안정창 · 계면 · 별도 상 · 깔때기 재실행 (MP API · gabia uma env · 생성기는 각 원장 머리말의 도구 — 산물 갭은 `tools/oxidation/run_cascade_extras.sh`).
3. **S3 순위 여유 δ** — D_rel 결과 전에.
4. **#7 실행 범위** — 237 목록 중 무엇을 얼마나 (예산).
5. **산물 갭 재생성** (HOLD 해제 심사) — 고친 `sei_product_gaps.py` 로.
6. **탄성 modelc_2x 60-BFGS 게이트** — 13_m · 23_p 가 넘었다: 측정 불가로 닫기 / 게이트 개정 (결과 본 뒤임을 기록). ✅ **10-14 사용자 *'bgfs는 계속 끝날떄까지 보자'* = 게이트 개정** — 넘은 점도 수렴할 때까지 계속 · 결과 본 뒤의 개정 (`D-2026-10-14-elastic-60bfgs-gate-continue`).
7. **dualx 처리** — 탐색으로 둘지, 마감 기록을 남길지.

## 9. 이 노트가 못 하는 것

- **판정이 아니다.** 강등 · 재건 · 마감은 각 원장이 정본이고, 이 노트는 그 위치와 관계만 적는다.
- v7 진행 숫자는 10-12 runlog 기준이다 — 원격 실측이 아니다 (발표 전에 watch 로 갱신).
- 재실행 60 구성이 본 배치와 **같은 앵커 · 같은 생성기 (S1 이전)** 를 썼다는 것까지는 원장에 있다 (`cascade_base_strain_2026_09_12.json`). 재실행 행이 감사 결함(부모 자리 · 보상 수지)에 얼마나 걸렸는지는 따로 세지 않았다.
- dualx 의 지표 결측 원인은 보지 않았다 (행 수만 셌다).
