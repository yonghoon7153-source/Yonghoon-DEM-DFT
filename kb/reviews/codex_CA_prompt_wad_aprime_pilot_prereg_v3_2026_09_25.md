---
title: "리뷰 CA 프롬프트 — A′ 파일럿 사전등록 카드 v3: BZ NO-GO 항목(G2 우회 4경로 · G5 집계 · S1/S3 경계) 이행 재심"
date: 2026-09-25
updated: 2026-09-25
tags: [review, codex, adhesion, wad, prereg, estimand, lpscl, silver, graphite, uma, d3, pilot, re-review]
status: 발송 대기 (1저자) — 카드 v3 는 draft · 봉인 전 · 계산 0 (선행 배치는 카드 밖 · 진행 중)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CA — A′ 카드 v3 재심 (BZ NO-GO → 이행 여부)

> BZ (`codex_BZ_reply_wad_aprime_pilot_prereg_v2_2026_09_25.md`) 가 v2 를 NO-GO 로 막았다 (봉인·S2 보류 · 설계·비준 5 선택은 유지). 이 프롬프트는 **v3 가 BZ 의 필수 수정을 실제로 이행했는지**만 묻는다.
> 카드 v3: `db/properties/wad_aprime_pilot_prereg_v3_2026_09_25.json` (draft · content_digest 없음 · V2–V5 계산 0 · 기하 생성 0). 코드: `tools/wad/se_sym_slab.py` (`interface_check` 재작성 · `fixed_mask_policy` · `normal_sign` · `--mask_policy`). 정본 브랜치 `claude/friendly-meitner-lldvar`.
> 트랙 W_ad → 1저자 = 사용자. 비준한 5 선택(`D-2026-09-25-wad-aprime-card-v2-choices`)은 그대로다.

## §0. BZ 필수 수정 → v3 의 대응

| BZ 항목 | 한 것 | 어디 |
|---|---|---|
| **P0 G5 종결별 평균** | v1 기준 복구 — 표본별 \|Δ\| ≤ 0.10 **그리고 종결별** \|mean(Δ)\| ≤ 0.05 (S 군 ①②⑤ · Li 군 ③④) · 전체 평균은 참고 · 표본 ①·⑤ 상관 → 독립 표본 주장 금지 (분모 5) | 카드 G5 · `표본_G5.상관_주의` |
| **Q2 G2 경로 ① 마스크** | 마스크 **필수** (생략 → SlabError · CLI 도 오류 종료 rc 2) · 정수·범위(`[-1]` → 오류) · 흡착층 원자 포함 → 깃발 · `fixed_mask_policy(init, 'far_half')` 집합과 일치하지 않으면 깃발 | `_validate_idx` · `interface_check` |
| **경로 ② NaN** | 셀·좌표 유한성을 **비교 전** 검사 (`_finite_or_die` · init·final 둘 다) → SlabError | 같은 파일 |
| **경로 ③ 흡착면 뒤집힘** | 법선은 **초기 구조에서만** (`normal_sign(init)`) · 최종 구조에서 흡착층 평균 z 가 반대쪽이거나 흡착 원자가 기판 중심면을 넘으면 깃발 | 같은 파일 |
| **경로 ④ V2** | 역할 선언 (`substrate_elements`·`ads_elements`) · V2 = 기판 Ag · 흡착층 C · SE 항목(PS₄·Li 침투)은 **'해당 없음'** 으로 구분 · Ag 고정층(far_half = 아래 2층) · 그래핀 **측방 제약** (`lateral_fixed_idx` · 면내 변위 < 1e-3 Å) · 셀·유한성·Ag–Ag·C–C 결합 검사 **수행** · SE 기본값으로 V2 를 부르면 오류 (조용히 통과 아님) | 같은 파일 · 카드 `V2.G2_V2_모드` |
| 시험 | selftest **110/110** · BZ 4 경로 음성 9 · 돌연변이 5 (유한성 제거 · 법선을 최종에서 · 정책 대조 제거 · 측방 검사 제거 · 마스크 필수 해제) **전부 빨간불** (09-25 실측) | `_selftest_interface_check` |
| **Q3 G3 조작** | 기준 셀 A (직접 8 · 영상 8 — 최종 좌표에서 잰 간격 · Δ 와 구분) · (i) 영상 검사 c+2 · 흡착층 그대로 (8/10) · (ii) 거리 검사 c+2 · 흡착층 +2 (10/8) · 각 셀에서 **두 끝점 재계산** · 둘 다 ΔW ≤ 0.01 → 그 군 PASS · 자원 초과 → '끝점 미검증' | 카드 G3 |
| **Q3 G5↔G3/G4** | G5 PASS 는 대상군 G3·G4 PASS 전제 · 미검증이면 'INCOMPLETE (G3/G4 미검증)' · 갈래1 안 열림 | 카드 G5 · 갈래1 |
| **Q1-3 Ag₄** | nspin 2 · starting_magnetization 0.5 (비영) · 자유 수렴 · 총자화·절대자화 기록 · \|M_tot\| < 0.05 → 비편극 채택 · 절대자화 > 0.2 주석 · 범위 = 고립 조각만 | 카드 `전자상태_정책.스핀` · S3 전 예외 ④ |
| **Q4** | 'RESOURCE_BLOCKED (예상)' ↔ '(실측 · 근거)' 구분 · CPU 통과 ≠ GPU 허가 | 카드 V5 |
| **Q5** | DEM 회신 4 §3 → "같은 초기 기판·고정 마스크 · 계면 쪽 최종 기하 상이 — 면적가중 적용 가정 유지 여부 DEM 확인 요청 · 합의 전 숫자 전달·사용 없음" | `wad_dem_reply_draft_2026_09_23.md` §회신 4 |
| **Q6** | `S1_전에_이미_본_것` (SE\|SE · 벌크 민감도 · 선행 배치 — 값은 S1 봉인 시점에) · `S3_전_예외_작업` 넷 (선행 배치 · D3 결박 · GPU 프로브 electron_maxstep 2 · Ag₄ 스핀) 각각 입력·정지·읽는 출력·금지 사용 · '본 검증 W 금지' ≠ '모든 pw.x 금지' | 카드 §0 |
| **Q7 S1/S3** | S1 에 PP·UMA 체크포인트 sha/버전/추론 설정·D3 구현·매개변수·코드 커밋·**마스크 생성 규칙**·**registry 선택 규칙(결정적 · 동률 = 인덱스 최소)**·**결정 내용 digest** 고정 · S2 는 최적화 전 마스크·registry·입력 좌표 기록 · S3 는 생성 좌표·끝점·마스크 해시 + 계보 | 카드 §0 · `decisions_content_digest_S1_봉인에_넣는_것` |

## §1. 아직 비어 있는 것 (S1 봉인 전 채움 · 재심 대상 아님)

- UMA 체크포인트 sha · fairchem 버전 · 추론 설정 — gabia/kgy uma env 에서 읽어 넣는다.
- 선행 배치 08–13 결과 (Ag·그래핀 a₀ · comp1 D3 응력) — V100 진행 중 → `S1_전에_이미_본_것` 에 값.
- 흡착층 빌더 (V2 · V3/V4 · V5) 코드 + selftest — 커밋으로 S1 에 고정.

## §2. 질문 (재심 — 항목별 GO / NO-GO / 조건부 · 봉인 전 필수 수정만)

- **Q1** BZ 필수 수정 각각(P0 · Q2 ①–④ · Q3 · Q6 · Q7): 이행됐는가. 특히 G2 의 정책 집합 대조가 "마스크 누락·잘못된 마스크" 경로를 닫는가 · V2 모드가 실제 검사를 수행하는가.
- **Q2** G3 의 두 셀 조작 (i)/(ii) 가 직접 거리와 영상 효과를 **분리**하는가 — 상쇄를 배제하는 데 충분한가 (둘 다 개별 통과 요구).
- **Q3** G5 의 종결별 평균 복구 — S 군이 3 표본(①②⑤ · ①⑤ 상관)이고 Li 군이 2 표본인 것이 문제인가 (분모·독립성 주장 없음).
- **Q4** S3 전 예외 작업 넷의 정의(입력·정지·읽는 출력·금지 사용)가 충분히 닫혀 있는가 — 특히 GPU 프로브 (electron_maxstep 2 · 에너지 기록 금지).
- **Q5** registry 선택 규칙(표면 원자 z 최대 · 동률 인덱스 최소 · 같은 종 최근접 이웃 중점)이 결정적이고 S2 결과에 의존하지 않는가.
- **Q6** S1 digest 구성 (카드 본문 + PP 해시 + UMA/D3/코드 결박 + 결정 내용 digest) 이 BZ Q7 의 경계와 맞는가.

형식: 항목별 GO / NO-GO / 조건부 + 봉인 전 필수 수정. 새 문턱을 제안하면 결과 전이므로 채택 가능하다는 점을 명시해 달라.

## 첨부 (repo 경로)

- 카드 v3 `db/properties/wad_aprime_pilot_prereg_v3_2026_09_25.json` (v2 · v1 은 superseded · 내용 보존)
- `tools/wad/se_sym_slab.py` — `interface_check` · `fixed_mask_policy` · `normal_sign` · `_selftest_interface_check` · CLI `--interface_check --fixed_idx … --substrate_elements … --lateral_fixed_idx … --mask_policy`
- 결정 `D-2026-09-25-wad-aprime-card-v2-choices` · `…-lattice-matching-rule-a-amend-1` (active)
- BZ · BY · BX · BW 회신 (`kb/reviews/`) · DEM 회신 4 초안 (`kb/projects/wad_dem_reply_draft_2026_09_23.md`)
