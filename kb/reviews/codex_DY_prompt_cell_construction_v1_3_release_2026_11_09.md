---
title: "DY 프롬프트 — 셀구축 v1.3 · b2o3 B·O 배치 카드 개정 1 v1.3: DX 고침 확인 (실행 목적 · 계획 항목 보존 · EOS 입력 유효성) · 1 단계 GO 여부 (계산 0 건)"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, readout, pilot, runner, eos, codex, prompt, letter]
letter: DY
track: b2o3
channel: codex
kind: prompt
status: 발송 전 (사용자가 보낸다) · 기준 커밋 12b8bdef (브랜치 claude/evac-2026-11-08) · 앞 편지 DX (NO-GO)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_DY_reply_cell_construction_v1_3_release_2026_11_09.md` 로 원문 보존.
> ⚠ DX 확인 목록 4 대로 GO 가 와도 **고친 판 카드는 사용자가 새로 비준**한다 (리뷰 진행 승인 ≠ 카드 비준).

---

**[b2o3 · 셀구축 v1.3] DX 고침 확인 — 1 단계 (UMA) GO 여부 (계산 0 건)**

## 0. 무엇을 묻나

DX 회신 (`kb/reviews/codex_DX_reply_cell_construction_v1_2_release_2026_11_09.md` · 기준 93937466) 은 NO-GO 였다 — DW 지적은 다 닫혔고 새로 P1-1 (파일럿 런 기록을 8 단계 결과로 끼워 넣어도 통과 — 실행 목적 구분 없음) · P2-1 (실행기가 시작 바이트가 같은 서로 다른 계획 항목을 하나로 합침 · 18 → 17) · P2-2 (EOS 입력이 NaN · 음수 부피 · 가족 누락이어도 '생략 가능' · DFT 전 조건). 확인 목록: ① 목적 구별 + 파일럿 복사 거부 / 새 실행 허용 ② 같은 바이트 계획 항목을 수 · 이름 그대로 실행기에 ③ 정상 경로와 두 반례 재확인 ④ 사용자 새 비준.

브랜치 `claude/evac-2026-11-08` · b2o3 변경은 **커밋 12b8bdef 하나** (93937466 뒤의 다른 커밋은 DX 프롬프트 · DX 회신 원문 보존 · kgy 기록 오독 줄 되돌림 — b2o3 도구 · 카드와 무관). 생산 UMA · DFT · MD 는 안 돌았다.

**묻는 것**: DX P1-1 · P2-1 · P2-2 가 닫혔나 → 1 단계 (생성 → UMA 이완 거름 → 연속 파일럿 → 어닐 → 판독) 를 사용자 새 비준 뒤 시작해도 되나 (GO / 조건부 GO / NO-GO).

## 1. 항목별 고침 (DX → 어디)

| DX | 고침 | 시험 |
|---|---|---|
| P1-1 실행 목적 | `tools/doping/run_anneal.py` — `--purpose` (실행 목적) 를 **줄 때만** 정체성에 넣는다 (안 주면 옛 정체성 · identity_sha 그대로 — 다른 파이프라인 영향 없음) · `--check_results --expect_purpose`. 판독기 `screen --plan_dir` 가 쓰는 계획 manifest 에 `purpose` (파일럿 = `b2o3_bo/pilot_run` · 8 단계 = `b2o3_bo/stage8_anneal`) → 실행기 (`run_uma_kgy.sh`) 가 manifest 의 purpose 를 `--purpose` · `--expect_purpose` 로 넘김 → 판독기 `extract` / `pilot` 은 파일럿 런에 pilot_run, `anneal` 은 8 단계 기록에 stage8_anneal 을 요구 (CONTRACT `purpose_pilot` · `purpose_stage8` · 카드 기계값) | 판독기 음성: **파일럿 런 기록 · 산출물을 8 단계 결과로 끼워 넣기** (t_a 100 · 같은 시작 · 100 ps · 500 K · 같은 base seed → 이유 '실행 목적' 으로 거부) · 8 단계 목적 없음 · 파일럿 목적 기록 · 파일럿 런 목적 없음 · 8 단계 목적 기록을 파일럿 런으로. 양성: **같은 입력 · 100 ps · 산출물 바이트까지 파일럿과 같은** 새 8 단계 기록 (목적 stage8) 통과 — 산출물 해시 차이로 가르지 않는다. run_anneal ⑩ (목적은 줄 때만 · 목적이 다르면 재개가 멈춤 · 결과 검사 대조) · 실행기 큐 자가시험 6/6 (목적이 실행 · 결과 검사 둘 다로 간다) |
| P2-1 계획 항목 보존 | 실행기 입력 목록 블록을 함수 `list_inputs` 로 — 계획 manifest (`b2o3_bo_plan/v1`) 는 **경로** 기준으로만 중복 제거 (서로 다른 항목은 바이트가 같아도 따로) · 옛 후보 manifest (Nd · B host 공통 파일) 는 내용 기준 그대로 · 후보 폴더끼리 실행 목적이 섞이면 멈춤 (5) | 실행기 입력 자가시험 3/3 (같은 바이트 계획 항목 둘 → 입력 둘 · 옛 공통 파일 → 하나 · 목적 섞임 → 5) · 발사 전 ③ 에서 돈다 |
| P2-2 EOS 입력 | `eos_robust` 계산 전에 — 가족이 정확히 셋 · E · P · V 유한 · V > 0 · B 범위 유한 양수 (아니면 멈춤 · CLI 종료 1) | 음성: F_B 에너지 NaN · 세 가족 부피 음수 · F_free 빠짐 · 압력 inf. 양성: 유효 입력 그대로 판정 |
| (Q3 운영 조건) | [제안] 8 단계 기록마다 seed − crc(이름) 이 **하나** (한 단계 = 한 base seed · 실행기 SEED 하나) 여야 판독 — seed 값 자체는 대조하지 않는다 | 음성: 한 기록만 다른 base seed → 거부 (기록을 다른 이름으로 옮겨도 여기서 걸린다) |

**깨기**: 검사 22 개 (DW 때 13 + 이번 9) 를 하나씩 끄고 판독기 · run_anneal · 실행기 자가시험을 다 돌려 **22 개 모두 빨간불** (고친 판 그대로는 빨간불 0 · 끝나고 원본 복원 확인). 새 9: 판독기 목적 대조 5 · base seed 1 · EOS 가족 집합 1 · EOS 유한 2 · EOS 부피 1 · run_anneal 정체성 목적 3 · 실행기 경로 기준 중복 제거 1 · 실행기 --purpose 전달 1 · 실행기 목적 섞임 1. 자가시험 지금 값: 판독기 69/69 · run_anneal 통과 (⑩ 포함) · 실행기 큐 6/6 · 입력 3/3. 음성 시험은 거부 이유 문자열까지 본다 (예외로 터지면 빨간불).

## 2. 일부러 안 한 것 (판단 요청)

- 실행 목적은 **파일럿 런 · 8 단계** 에만 요구한다. 6 단계 (시작 = 생성 CIF) · 스냅숏 이완 (시작 = 스냅숏) 은 시작 파일이 단계마다 유일해서 목적 없이도 섞이지 않는다고 봤다 (그 둘의 manifest 에는 purpose 가 없다).
- 목적은 manifest 에서만 온다 — 실행기 환경변수로 덮어쓰는 길은 만들지 않았다.
- 운영체제 사이 경로 이동 (Windows ↔ Linux 상대경로) 은 시험하지 않았다 — 같은 OS 안 이동만.

## 3. 질문

- **Q1** DX P1-1 · P2-1 · P2-2 가 닫혔나 — DX 의 같은 반례 (파일럿 기록 끼워 넣기 · 같은 바이트 계획 항목 18 → 17 · EOS NaN / 음수 부피 / 가족 누락) 와 정상 연결 경로 (screen → extract → pilot → anneal) 로.
- **Q2** 8 단계 base seed 하나 [제안] 가 결과 전 규칙으로 괜찮나 (정상 재시도 · 나눠 돌린 묶음이 같은 SEED 를 쓰는 한 걸리지 않는다)?
- **Q3** §2 의 선택 (목적은 파일럿 · 8 단계만 · manifest 에서만) 에 남은 구멍이 있나?
- **Q4** 1 단계 시작 전에 더 닫을 것이 있나 — 없으면 사용자 새 비준만 남는가?

## 4. 회신 형식

GO / 조건부 GO / NO-GO 한 줄 → P0–P3 (파일:줄 · 재현 · 최소 수정) → Q1–Q4 → 1 단계 시작 전 마지막 확인 목록.
