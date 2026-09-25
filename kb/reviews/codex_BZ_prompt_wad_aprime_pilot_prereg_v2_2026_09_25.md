---
title: "리뷰 BZ 프롬프트 — A′ 파일럿 사전등록 카드 v2: BY NO-GO 재승인 최소조건 6 의 이행 재심"
date: 2026-09-25
updated: 2026-09-25
tags: [review, codex, adhesion, wad, prereg, estimand, lpscl, silver, graphite, uma, d3, pilot, re-review]
status: 발송 완료 · 회신 수령 2026-09-25 밤 **NO-GO** (`codex_BZ_reply_…`) → 카드 v3 + G2 재작성 → CA 재심 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 BZ — A′ 카드 v2 재심 (BY NO-GO → 재승인 최소조건 6 이행 여부)

> BY (`codex_BY_reply_wad_aprime_pilot_prereg_2026_09_25.md`) 가 v1 을 NO-GO 로 막았다 (봉인·본계산 보류 · A′ 경로 찬성). 이 프롬프트는 **v2 가 재승인 최소조건 6 을 실제로 이행했는지**만 묻는다 — 새 질문을 열지 않는다.
> 카드 v2: `db/properties/wad_aprime_pilot_prereg_v2_2026_09_25.json` (draft · content_digest 없음 · V2–V5 계산 0 · 기하 생성 0). 트랙 W_ad → 1저자 = 사용자 · 권고 5 는 1저자가 설명을 다시 듣고 비준했다 (`D-2026-09-25-wad-aprime-card-v2-choices` · 결정 7 개정 `…-amend-1` active).
> 정본 브랜치 `claude/friendly-meitner-lldvar`.

## §0. 재승인 최소조건 → v2 의 대응 (한 줄씩)

| # | BY 조건 | v2 에서 한 것 | 어디 |
|---|---|---|---|
| 1 | 4층 조성 · SE 고정/이완 정책 일치 | 조성 = Li₅₂P₈S₄₂Cl₈ (110) · Li₄₄P₈S₃₈Cl₈ (98) — manifest·PBE 이완 좌표 파일과 대조 ✅ · 정책 = **부분 고정 마스크** (계면 반대쪽 절반 고정 · 정본 PBE 이완 좌표 sha 504e0b08… / 7e0b1dae… · 계면 쪽 절반 + 흡착층 자유) · 결정 7 문구를 개정 (`…-amend-1`: 같은 면내 셀 · 같은 초기 좌표 · 같은 마스크 · 계면 쪽 최종 기하는 계면별) | 카드 §1b `host_기판` · `SE_고정_마스크` · 결정 원장 |
| 2 | G5 를 비자명한 W 쌍으로 · 실패·무효·미완료를 분모에서 안 지움 | 표본 5 = P1′ 결합·분리 끝점 쌍 5 (두 종결 × registry A/B 4 + S 바깥 A **+0.5 Å 인장**) · 분모 5 고정 · PASS/FAIL/INCOMPLETE/BLOCKED/RESOURCE_BLOCKED/NOT_TESTED · 교체 금지 · 4 로 줄이면 축소 파일럿 사전 개정 | `표본_G5` · G5 |
| 3 | Ag₁₃ 전자상태 · −TS 무효 규칙 | **Ag₁₃ 제외** (13×19 = 247 · 홀수) · Ag₄ 는 고립 스핀 편극 단일점 1 로 \|M\| < 0.05 μB 확인 · C₂₄H₁₂ 도 제외 (1×1 셀 영상 맞닿음) · −TS 규칙 **삭제** → W 에 쓰는 에너지 = `!` 자유에너지 F 고정 · E_int 병기 · smearing 민감도는 G4 대상군별 | `전자상태_정책` · §3 |
| 4 | 양쪽 주기 간격 · 쌍극자 보정 · 전자상태 포함 분리 끝점 | far = 강체 이동 Δ · **직접 간격 ≥ 8 Å 그리고 반대편 영상 간격 ≥ 8 Å** (둘 다 계산·기록) → c 결정 · 결합 끝점 같은 c · `tefield/dipfield/edir=3/eamp=0.0` · emaxpos·eopreg 셀 위끝 (두 끝점 빈 공간 검사) · 프로브는 분리 셀 · δ_add 한계(조각 중성 미보장) | `끝점_MoLE` · `쌍극자_보정` |
| 5 | G2 실제 검사 · G3/G4 적용 범위 · 자원별 한도 | **G2 구현** `se_sym_slab.py --interface_check` (PS₄·짝 · 흡착층 결합 목록 ±15 % · 비혼합 범위 = 첫 흡착층 평면 아래 1.5 Å · 법선·원자 ID·주기경계 정의 · 고정 마스크 변위) — 음성 5 · 돌연변이 4 빨간불 (09-25 실측) · 실행 허가 조건에 결박 · G3/G4 = 대상군 {V2·V3·V4·V5} 별 대표점 · 두 끝점 재계산 · ecutrho·k·smearing 명시 · 미확인 군 = 미검증 · 장치별 한도 gabia 44,000 / V100 31,000 MiB · CPU 추정 = 허가만 · GPU-h ≠ 경과시간 · RESOURCE_BLOCKED | G2·G3·G4 · `자원` |
| 6 | 미검증 계면 · V5 미실행 분기 허용 문구 | 1a: BY 가 준 두 문장 그대로 · P1′ 한정 · \|mean(ΔW)\| ≤ 0.05 · V5 없음 → **NOT_TESTED** · 갈래0 = **내부 전용 · DEM 전달 없음** (1저자 결정) · V2 문구 'Ag–C 계면 · P2 대조 아님 · 단층' · DFT@UMA 정의 문구 | 1a · 갈래0 |

추가로 한 것 (BY 본문의 나머지 지적): V5 표현 → "자원 제한 아래 선택한 2층 주기 대조 모델" · V3/V4 = 주기 반복 조각 (측방 영상 거리 기록) · 집계 = "검색한 배치 중 가장 약한 분리일" · 분모 n_if 모델별 검사 (한 면 흡착 1) · PP Ag/C/**H** 해시 + z_valence 결박 · UMA 체크포인트·D3 매개변수·구현 결박 검사 · V2 registry 좌표 고정 + 그래핀 z 만 이완(측방 제약) + E(d) 5점 통일 + a_PBE 뒤 3 % 규칙 · 갈래3 문구 교체 · **단계별 봉인 S1–S4** (S1 설계 → S2 기하 생성·프로브 → S3 좌표·끝점 봉인 → S4 DFT).

## §1. 자원 현실 (v2 §⑤ · 새로 계산해 넣은 것)

부피 × 밴드 스케일 (기준 SE|SE 4층 SCF 110 원자 · 3,610 Å³ · V100 실측 32.0 GB · Ag PP z_valence 19 실측):

| 모델 | 원자 | 밴드 | 추정 |
|---|---|---|---|
| V5 P1′ SE 2층 1×2 + Ag(111) 3층 | 196 | ~1,270 | **≈ 246 GB** |
| V5′ Ag 2층 | 168 | ~950 | ≈ 171 GB |
| V3 Ag₄ \| SE 4층 1×1 (진공 16) | 114 | ~350 | ≈ 42 GB (gabia 만 · 44,000 kill 과 2 GB 차) |
| V4 C₆H₆ \| SE 4층 1×1 | 122 | ~320 | ≈ 37 GB (gabia 만) |
| V2 Ag(111) 4층 + graphene 2×2 | 20 | ~160 | ≈ 3 GB |

⇒ V5 는 **RESOURCE_BLOCKED 를 예상**한다 (CPU 프로브는 기록용으로 돌린다). 그러면 이 카드가 낼 수 있는 것은 V2 직접 DFT · V3/V4 진단 · 전체 계면 미검증 예측(내부) 이다 — 1저자가 이를 인정했고 더 줄인 V5 로 대체하지 않는다.

## §2. 질문 (재심 — 항목별 GO / NO-GO / 조건부 · 봉인 전 필수 수정만)

- **Q1** 재승인 조건 1–6 각각: 이행됐는가. 특히 (1) 부분 마스크 + 결정 7 개정문이 "같은 기판" 주장을 좌표 수준에서 성립시키는가 · (2) 표본 ⑤(+0.5 Å 인장)가 비자명한 W 로 인정되는가.
- **Q2** G2 구현의 정의(첫 흡착층 평면 · 1.5 Å · 결합 목록 ×1.15 · 마스크 1e-3 Å)가 봉인 가능한 수준인가. 빠진 실패 경로는?
- **Q3** 분리 끝점 8 Å (직접·영상 둘 다) — D3 2체 꼬리·쌍극자 보정 위치와 함께 충분한가. G3 의 8 → 10 Å 대표점 검사가 대상군별로 맞게 걸렸는가.
- **Q4** 자원: V5 추정 246 GB 를 "RESOURCE_BLOCKED 예상" 으로 미리 적는 것이 사전등록 규율에 맞는가 (결과 전에 결론을 적는 것이 아닌가) — 아니면 프로브 결과 뒤에만 적어야 하는가.
- **Q5** 갈래0 (내부 전용 · DEM 전달 없음) 과 DEM 3차 회신의 부탁 2 (시나리오 초안은 DEM · 합의 뒤 사용) 가 충돌 없이 맞물리는가.
- **Q6** 단계별 봉인 S1–S4 의 경계 — 선행 배치(Ag·그래핀 a₀ · comp1 D3 응력 · `db/inputs/wad_aprime_prep_2026_09_25` · 읽는 규칙 결과 전 등록)를 **카드 밖**으로 두고 S1 전에 돌리는 것이 허용되는가.
- **Q7** S1 봉인 형식: content_digest 에 넣을 것 (카드 본문 · PP 해시 · 결정 ID) 과 S3 로 미룰 것 (좌표 sha · 마스크 인덱스 · registry 좌표 · UMA 체크포인트 sha) 의 경계가 맞는가.

형식: 항목별 GO / NO-GO / 조건부 + 봉인 전 필수 수정. 새 문턱 제안은 결과 전이므로 그대로 채택 가능하다는 점을 명시해 달라.

## 첨부 (repo 경로)

- 카드 v2 `db/properties/wad_aprime_pilot_prereg_v2_2026_09_25.json` · v1 (superseded) `wad_aprime_pilot_prereg_2026_09_25.json`
- 결정 `D-2026-09-25-wad-aprime-card-v2-choices` · `D-2026-09-25-wad-lattice-matching-rule-a-amend-1` · `D-2026-09-25-wad-lattice-matching-rule-a` · `D-2026-09-25-wad-reference-state-policy` · `D-2026-09-23-wad-a-prime-scope`
- G2 구현 `tools/wad/se_sym_slab.py` (`interface_check` · `_selftest_interface_check`) · 선행 배치 집계 `aprime_prep_collect`
- 선행 배치 입력 `db/inputs/wad_aprime_prep_2026_09_25/jobs.json`
- BY 회신 · BX 회신 · BW 회신 (`kb/reviews/`)
