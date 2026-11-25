---
title: "리뷰 CB 프롬프트 — A′ 파일럿 사전등록 카드 v4: CA 최소 해제조건 5 이행 재심 (V2 측방 마스크 · 인덱스 타입 · G3 문구 · 프로브 예외 · registry 주기영상)"
date: 2026-09-25
updated: 2026-09-25
tags: [review, codex, adhesion, wad, prereg, estimand, lpscl, silver, graphite, uma, d3, pilot, re-review]
status: 발송 완료 · 회신 수령 2026-09-25 밤 **조건부 GO** (`codex_CB_reply_…`) → 조건 4 이행 → 카드 v5 봉인 후보 (1저자 비준 대기)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CB — A′ 카드 v4 재심 (CA NO-GO → 최소 해제조건 5 이행 여부)

> CA (`codex_CA_reply_wad_aprime_pilot_prereg_v3_2026_09_25.md`) 가 v3 를 NO-GO 로 막았다 — BZ 주요 수정은 이행 · 남은 것은 **V2 측방 마스크 선택 입력(P0) · 인덱스 자동 변환(P1) · G3/G5 문구 · CPU/GPU 프로브 예외 · registry 주기영상 명세**. 이 프롬프트는 그 다섯의 이행만 묻는다.
> 카드 v4: `db/properties/wad_aprime_pilot_prereg_v4_2026_09_25.json` (draft · content_digest 없음 · V2–V5 계산 0 · 기하 생성 0). 코드: `tools/wad/se_sym_slab.py`. 정본 브랜치 `claude/friendly-meitner-lldvar`.
> 트랙 W_ad → 1저자 = 사용자. 비준 5 선택(`D-2026-09-25-wad-aprime-card-v2-choices`)은 그대로.

## §0. CA 최소 해제조건 → v4 의 대응

| # | CA 조건 | 한 것 | 어디 |
|---|---|---|---|
| 1 | V2 측방 마스크 = 그래핀 전체 집합 · 누락·부분집합 우회 차단 | 금속 기판 모드에서 `lateral_fixed_idx` **필수** (None·빈 목록 → '필수' SlabError · CLI rc 2) · 초기 구조의 흡착층 전체 집합과 **일치** 검사 (빠짐·다른 몸체 → 깃발) · PS₄ 기판 모델에 측방 제약을 주면 '정책에 없는' 깃발 · 음성 6 (생략 · 빈 목록 · Ag 만 · 움직인 원자 제외 부분집합 · PS₄ 모델에 제공 · numpy 정수 양성) | `interface_check` 측방 정책 블록 · `_selftest_interface_check` |
| 2 | 소수·불리언 자동 변환 거부 | `_validate_idx` 는 **변환 없이** 타입 검사 — int·numpy 정수만 · bool/np.bool_·float·str → SlabError · 중복 → SlabError. CLI 는 형식만 푼다 (쉼표 토큰 `-?\d+` · JSON 목록은 그대로 넘겨 `_validate_idx` 가 거른다) — 파싱/검증 분리 · 음성 4 (0.9 · −0.9 · False/True · 중복) + CLI JSON 소수 rc 2 (실제 V3 형 입력으로 확인) | 같은 파일 |
| 3 | G3 절댓값·끝점별 기록 · G5 문구 '종결별' | G3: **|ΔW| ≤ 0.01 · |ΔE| ≤ 5 meV** · 검사마다 ΔE_far · ΔE_bound · ΔW 각각 기록 · ΔW 는 차이량이라 작아도 끝점 변화·상쇄 부재를 뜻하지 않음 · 허용 문구 = '지정한 두 간격 변화에 대한 W 민감도 통과' (1a `G3_통과시`) · 1a G5 문구에 **종결별** 명시 | 카드 G3 · 1a |
| 4 | CPU/GPU 프로브 예외 · 단일 SCF · 출력 사용 규칙 | S3 전 예외 ③ = **CPU/GPU 자원 프로브** · `calculation='scf'` 만 (`electron_maxstep` 은 SCF 단계 반복 상한 — 이완 종료 보장 아님) · 전용 폴더 + `ESPRESSO_TMPDIR` · CPU 정지 = RAM 추정 줄 뒤 PID kill · GPU 정지 = 2 반복 자동 종료 또는 KILL 가드 · **원출력 감사용 보존** · 프로브 에너지는 결과표·W·후보 선택·게이트 조정에 사용 금지 | 카드 §0 `S3_전_예외_작업.③` |
| 5 | registry 주기영상·중점·동률 | A 후보 집합 Σ = 표면 종 중 `z_max − z_i < 0.05 Å` · A = 인덱스 최소 · B 이웃 후보 = Σ∖{a} · 거리 = 면내 **최소영상** 변위 (이미지 오프셋 기록) · 동거리(< 1e-3 Å) = (원자 ID → 이미지 오프셋 사전순) · 중점 = r_a + ½Δ_mic → [0,1) 감기 · S2 에 a·j·오프셋·Δ·m·Σ 기록 · 좌표 평균(비최소영상) 금지 | 카드 §0 `registry_선택_규칙_결정적` |

추가: Ag₄ 절차 문구에 "선언한 비편극 모델을 쓰는 정책 — 흡착 끝점의 비자성 검증 아님" (CA Q1) · S1 봉인 조건에 "UMA 체크포인트·환경·빌더가 빈 상태로는 봉인 불가" (CA Q6).

시험: selftest **120/120** · 돌연변이 **8** (유한성 제거 · 법선을 최종에서 · 정책 대조 제거 · 측방 검사 제거 · 마스크 필수 해제 · **측방 집합 대조 제거 · V2 측방 필수 해제 · 타입 검사→int 변환**) 전부 빨간불 (09-25 실측).

## §1. 아직 비어 있는 것 (S1 봉인 전 채움 · 재심 대상 아님 · CA Q6 조건 유지)

- UMA 체크포인트 sha · fairchem 버전 · 추론 설정.
- 선행 배치 08–13 결과 (Ag·그래핀 a₀ · comp1 D3 응력) → `S1_전에_이미_본_것` 에 값.
- 흡착층 빌더 (V2 · V3/V4 · V5) + registry 규칙 구현 + selftest — 커밋으로 S1 에 고정.

## §2. 질문 (재심 — GO / NO-GO / 조건부 · 봉인 전 필수 수정만)

- **Q1** 조건 1·2: 측방 마스크 정책(필수 · 전체 집합)과 인덱스 타입 검사가 CA 가 재현한 경로(생략 · Ag 만 · 부분집합 · 소수 JSON · 불리언)를 닫는가. 남은 우회가 있는가.
- **Q2** 조건 3: G3 의 기록 항목(ΔE_far · ΔE_bound · ΔW)과 허용 문구가 CA Q2 의 한정과 맞는가.
- **Q3** 조건 4: 프로브 예외의 `scf` 한정 · 정지 조건 · 출력 사용 규칙이 닫혀 있는가.
- **Q4** 조건 5: registry 규칙이 CA Q5 반례(x 0.1 · 9.9)에서 하나의 좌표를 주는가 · 동률 순서가 완전한가.
- **Q5** 이 상태에서 (빈 항목 셋을 채운 뒤) S1 봉인이 가능한가 — 아니면 봉인 전 필수 수정이 더 있는가.

형식: 항목별 GO / NO-GO / 조건부 + 봉인 전 필수 수정. 새 문턱 제안은 결과 전이므로 채택 가능하다는 점을 명시해 달라.

## 첨부 (repo 경로)

- 카드 v4 `db/properties/wad_aprime_pilot_prereg_v4_2026_09_25.json` (v3·v2·v1 superseded · 내용 보존)
- `tools/wad/se_sym_slab.py` — `_validate_idx` · `interface_check` (측방 정책) · CLI `_idx`
- CA · BZ · BY · BX · BW 회신 (`kb/reviews/`)
