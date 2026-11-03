---
title: "DJ 프롬프트 — li2s-2 DI 고침 적용 확인 (Linux) + 정전 복구 개정 (0f51518d): 끊긴 런 시드마다 1 회 재시도 · 재부팅 고아 런 증언 상한 — 첫 담금질 GO 여부"
date: 2026-11-03
updated: 2026-11-03
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DJ
track: li2s
channel: codex
kind: prompt
status: 발송 · 회신 수령 2026-11-03 (NO-GO · `codex_DJ_reply_li2s2_outage_rule_2026_11_03.md`) · 기준 커밋 0f51518d
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DI (dad10ecf · NO-GO · P0 3 · P1 2 → Codex 고침 묶음) 다음 편지다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `0f51518d` (브랜치 `claude/friendly-meitner-lldvar`). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DJ_reply_li2s2_outage_rule_2026_11_03.md` 로 원문 보존.

---

**[li2s-2] DI 고침 적용 확인 (Linux) + 정전 복구 개정 — 첫 담금질 GO 여부**

## 0. 무엇을 묻나

두 가지다.
1. **DI 고침 묶음을 그대로 적용했고 (`b7d11f81` · 두 파일 = 묶음 사본 바이트 일치), DI 가 남긴 승인 보류 사유 (Linux 실제 프로세스 종료 시험) 를 Linux 에서 돌렸다** — 이걸로 DI 가 닫혔는가.
2. **정전 복구 개정** (`0f51518d` · 사용자 결정 · 결과 0 건) — DI 규칙으로는 kgy 정전 한 번이면 1 단계가 막힌다 (끊긴 런은 판정이 없어 재시도 대상이 아니고 · 재부팅 고아 런은 비용 미확정). 그래서 좁은 복구 규칙을 넣었다. **이 규칙이 DI 가 막은 구멍 (fail 재담금질 · 보존 실행 비용 · 조회 불가 · 시간) 을 다시 열지 않는가 · 선택 효과 (결과를 보고 고른 재시도) 를 막는가.**

판정 (GO / 조건부 GO / NO-GO) 을 달라. GO 면 결정 활성 → kgy 1 단계 발사다 (cascade v7 끝난 뒤).

## 1. 보는 범위

- `git diff dad10ecf 0f51518d -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
  - `dad10ecf → b7d11f81` = DI 묶음 패치 그대로 (`db/raw/codex_DI_patch_li2s2_2026_11_03/li2s2_DI_fixes.patch`)
  - `b7d11f81 → 0f51518d` = 정전 복구 개정 (아래 §3)
- 카드 `개정_정전_복구_2026_11_03` · 기계값 `stage1_max_interrupt_retries_per_seed` (= 1)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 193) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 65 · Linux)
- 깨기 (변이) 72 개 진행 중 (DG · DH · DI · 정전 개정 — 저장소 밖 복사본 · 결과는 끝나는 대로 실행 기록 `정전_복구_개정_2026_11_03` 에 · 앞선 판 53/53 빨강) — 저장소 밖 복사본

## 2. DI 고침 적용 확인 (Linux)

- 패치 적용 → 두 파일 SHA = 묶음 `after_sha256` (`ca81a6c3…` · `f52cf9fd…`).
- 드라이버 191/191 · 러너 **58/58** — 묶음이 Windows 에서 못 돌린 POSIX 시험 포함: 진짜 프로세스 그룹 셋 (TERM 이 손자까지 · 대표 TERM 사망 + TERM 무시 일꾼 → KILL · 대표 rc 0 + TERM 무시 일꾼 → KILL) · flock. 시험 뒤 남은 프로세스 0.
- DI 의 다섯 지적 ↔ 패치 ↔ 시험 대응표 = `kb/reviews/codex_DI_reply_li2s2_dh_fixes_2026_11_03.md` §지적 ↔ 적용한 고침.

## 3. 정전 복구 개정 (b7d11f81 → 0f51518d)

**왜** — kgy 는 10 월에 정전 두 번 (10-16 · 10-30) · 1 단계는 6–9 일. DI 규칙: 판정 없는 끊긴 런 = 'invalid 아님' → 재시도 금지 · 재부팅을 넘긴 고아 런 = 같은 부팅 시계 근거 없음 → 비용 미확정 → 묶음 무효. 정전 한 번이면 1 단계가 끝나지 못한다.

**(a) 끊긴 런 재시도 — `retry_eligibility(attempts, stop_history, inventory, max_interrupt, cost_bases)`** (폴더가 아니라 그 시드의 **실행 이력 전체** 로 가른다):
- 거부: 이전 실행 어느 하나라도 과학적 판정 (장부 `verdict` **또는** 보존 폴더 `stage1_verdict.json` 이 pass · fail) · 비용 미확정 (`end` 없음 · 근거가 측정 · 보수 상한 · 증언 상한 아님) · 보존 폴더를 못 찾음 (같은 계 폴더 안 보존 · `attempt_inventory`) · **끝까지 돈 런** (보존 폴더에 result.json · final.xyz — 재시도가 아니라 `--stage1_verdict` 로 판정) · 끊긴 런 재시도 수 > 카드 한도 (1) · 마지막 실행의 run_id 에 묶여 **확인된** STOP 이 없음.
- 묶는 STOP: 마지막 실행이 invalid → code `invalid` · 끊긴 런 → `interrupted` · `abnormal` · `resume` · `cap` (상한 멈춤은 원래대로 카드 상한이 올라야 ack 가 된다).
- 모든 STOP 에 그 런의 `run_id` (중단 · 비정상 · 상한 · 녹음 · resume — resume 은 폴더의 stage1_attempt.json 에서).
- 새 실행의 attempt · 장부에 `retry_of` · `retry_stop_id` · `retry_kind`. 앞 런 비용은 장부에 그대로.
- DI 가 고친 것과의 관계: fail 재담금질 금지 (DI P0-1) 는 그대로 — 폴더 판정까지 본다. 보존 실행 비용 대조 (DI P0-2) 는 그대로 — 재시도 전에 비용 확정을 요구한다.

**(b) 재부팅 고아 런 비용 — 자동으로는 미확정 그대로 (DI P1-5 · Q1)**:
- 러너가 미확정 고아 런을 보면 그 run_id 와 명령을 알려 주고 `resume` 으로 멈춘다.
- `--attest_cost RUN_ID` = 근거만 본다 (마지막 heartbeat = 하한 · 시작 시각 · 시작 boot 시계 · 지금 부팅 시각 /proc/stat btime · 보존 폴더 파일 마지막 시각 − 시작 · 제안값 '지금 부팅 시각 − 시작' 은 **재부팅 뒤 시계가 맞을 때만** 상한이라는 경고와 함께).
- `--attest_cost RUN_ID --attest_hours H --attest_note '근거'` = 잠금을 잡고 · 그 런이 orphaned · unknown 일 때만 · H 유한 · **하한 이상** · 근거 글 필수 → `cost_basis: attested_upper_bound` + `attestation {note, by, at, evidence}`.
- 소비자 `ledger_check`: 증언 상한은 근거 (note · by) 와 하한 이상이어야 · 묶음 판정 `cost.attested` 에 드러난다.
- ⚠ 설계 중 고친 것: 처음엔 '이전 부팅 마지막 시스템 로그 시각' 을 상한으로 쓰려 했다 — 정전 때 디스크에 안 쓴 마지막 로그가 사라지므로 그 시각은 **하한**이다. 그래서 자동 상한을 버리고 사람의 증언으로 바꿨다.

**(c) 소비자 이력 검사 (`ledger_check`)**: 같은 시드에서 과학적 판정 뒤 실행 · `retry_of` 가 같은 시드의 앞선 실행이 아님 · 끊긴 런 재시도 > 한도 → 무효.

**시험 (Linux 러너 65)**: B12 Ctrl-C → STOP 에 run_id → 폴더 보존 + ack → 한 번 다시 · 11 런 · 통과 / 같은 시드 두 번 끊김 → 세 번째 거부 (27) / 끝까지 돈 런 (결과 파일 · 판정 없음) → '판정하라' 로 거부 / 다른 run_id 에 묶인 확인 → 거부 / 재부팅 고아 런 → 미확정 · attest 명령 안내 → 하한 미만 · 근거 없음 거부 → 증언 상한 → 폴더 보존 + 그 run_id 의 resume STOP 확인 → 한 번 다시 → 통과 (증언 비용이 묶음에 드러남) / 소비자: 판정 뒤 같은 시드 행 · 재시도 한도 초과 · 근거 없는 증언 상한 → 무효.

## 4. 이것을 특히 봐 달라

1. **선택 효과** — 끊긴 런 재시도가 '결과를 보고 고른 재시도' 로 쓰일 길이 남는가. 첫 시드가 아닌 시드는 담금질 중 녹음 판정을 하지 않지만, 사람이 진행 중 파일 (traj) 을 보고 Ctrl-C 할 수는 있다 — 한도 1 · 모든 시도와 확인이 장부 · 보존 폴더에 남는 것으로 충분한가, 더 필요한가.
2. **'끝까지 돈 런' 판별** — result.json · final.xyz 유무로 가른다. 드라이버는 FIRE 완화 뒤 final.xyz · 그 뒤 result.json 을 쓴다. 담금질이 끝나고 FIRE 중에 끊기면 '끊긴 런' 이 된다 — 맞는가.
3. **증언 상한** — 사람의 증언을 비용 확정으로 받는 것이 DI Q1 ('신뢰할 종료 기록이나 보수적 상한으로 확인하기 전에는 통과 안 됨') 과 맞는가 · 근거 필드가 충분한가.
4. **cap 으로 묶인 재시도** — 상한으로 끊긴 런도 '끊긴 런' 으로 한 번 다시 돌 수 있다 (상한이 결정 · 카드로 올라야 ack 가 됨). 맞는가.
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 5. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DI 지적마다 닫힘 여부 한 줄.
