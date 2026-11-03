---
title: "DI 프롬프트 — li2s-2 DH 고침 확인 (dad10ecf): 장부 = 실행 목록 · 실행 식별자 run_id · 그룹 정리 (대표와 따로) · invalid ≠ 과학적 종료 · 재판정 이력 — 첫 담금질 GO 여부"
date: 2026-11-03
updated: 2026-11-03
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DI
track: li2s
channel: codex
kind: prompt
status: 초안 (2026-11-03) — 사용자 발송 대기 · 기준 커밋 dad10ecf
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DH (7abe7929 · NO-GO · P0 3 · P1 2) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `dad10ecf` (브랜치 `claude/friendly-meitner-lldvar`). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DI_reply_li2s2_dh_fixes_2026_11_03.md` 로 원문 보존.

---

**[li2s-2] DH 고침 확인 — 첫 발사 전 조건 (비용 누락을 0 으로 통과 · 같은 실행을 여러 시드로 · 그룹 일부 잔존 · invalid 의 영구 종료 · 재판정 증거 소실) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DH 의 P0 셋 · P1 둘을 고쳤다 — **지적마다 닫혔는가 (GO / 조건부 / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DH 가 해제로 본 것 (DG P1-6 ~ P2 · 일반 예외 · Ctrl-C 경로 · 9×20 h + 60 h 상한 반례 · 5 원자 final · 판정만 복사) 은 다시 열지 않아도 된다.

**가능하면 DH 때의 반례 스크립트 (`dh_probe_vx67j051`) 를 이 커밋에 다시 돌려 달라.** 인터페이스가 바뀐 곳은 §2 끝.

## 1. 보는 범위

- `git diff 7abe7929 dad10ecf -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py`
- 결정 `D-2026-11-03-li2s2-dense-window` (아직 proposed) · 실행 기록 `db/properties/lpscl_glass_dense_window_runlog_2026_11_03.json` 의 `회신_DH_2026_11_03`
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 191) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 49 · Linux: flock · 진짜 프로세스 그룹 셋)
- 깨기 (변이) 53/53 빨강 (DG 36 다시 + DH 17 · R16 은 고아 런 시험이 하한 · 상한을 가르게 고친 뒤) — 저장소 밖 복사본에서 고친 곳을 하나씩 되돌려 해당 시험이 빨개지는지

## 2. DH 지적별로 한 것 (반례 재현 → 지금 막는 시험)

**P0-1 장부 = 실행 목록** —
- 러너: 산출물 (`<계>/seed*`) 은 있는데 장부가 없으면 **빈 장부를 만들지 않고 거부** (10). 
- 런 비용 근거 `cost_basis` = `measured` (러너가 끝까지 잰 벽시계 — 정상 끝 · 상한 · 녹음 · 중단 멈춤) 또는 `upper_bound` (고아 런: **그룹이 죽은 것을 본 시각 − 시작** · heartbeat · 파일 시각은 `wall_h_lower` 로만).
- 소비자 `ledger_check` (stage1_summary 가 부름): 판정 (이 out_root 의 시드 판정) 마다 그 `run_id` 의 장부 런이 있어야 하고 그 런의 (계, 시드) 가 판정 자리와 같아야 한다 · 장부 런 비용은 유한한 비음수 · 근거 측정 · 보수 상한 · run_id 중복 없음 — 어기면 묶음 **무효** · 안 끝난 런 (`end` 없음 — running · stop_failed) 은 **대기** (heartbeat 는 하한이라 확정 비용 아님). total_h 는 확정 비용만 더한다.
- 시험 (진짜 판독 함수 · 완결 10 런 복제본): `{"runs": []}` · 한 행 누락 · 모든 행 −10 h · `cost_basis` 하한 → 무효 / 모든 행 끝 없음 → 대기 / 빈 장부로 러너 → 27 · `--ack_stop` 으로 확인해도 27 · 발사 0 / 장부 없는 산출물 → 거부 · 장부 파일 안 생김 / 고아 런 → 보수 상한 (≥ 하한) / 장부 행 시드 표시 바꿈 (A11 ↔ A12) → 무효.

**P0-2 실행 식별** — 러너가 담금질마다 `run_id` (uuid4 hex) 를 만들어 드라이버 `--run_id` 로 넘긴다 → plan.json · 장부 런 · 시드 판정에 같은 값.
- 시드 판정 (`identity_check`): 폴더 (계, 시드) = plan (계, 시드) · plan 에 run_id (32 hex) 가 있다 — 아니면 무효 (러너 밖 담금질은 장부에 안 잡히므로 통과 못 한다).
- 묶음: 자리 (계, 시드) ≠ 판정 (계, 시드) → 무효 · 판정끼리 run_id 중복 (한 실행을 여러 시드로) → 무효 · 장부 대조 (위).
- 시험: DH 재현 그대로 (A11 폴더 → A12) → 묶음 무효 · 러너 재판정 무효 · 27 · 발사 0 / 계마다 다섯 자리 복사 → 무효 / plan 시드까지 12 로 고침 → 시드 판정은 통과지만 run_id 가 A11 과 같고 장부에서 A11 런 → 묶음 무효 / A12 · A13 판정 자리 바꿈 → 무효.

**P0-3 그룹 정리** — `_Proc.stop` 이 대표 (직접 자식) 의 종료와 **그룹 잔존** 을 따로 본다: 그룹에 남은 것 (Linux `/proc` pgrp · 좀비 제외) 이 있거나 대표가 살아 있으면 그룹에 TERM → grace 동안 대표를 거두며 그룹이 빌 때까지 → 남으면 그룹에 KILL → 다시 확인 → `{"leader_rc", "group_empty", "signals", "left"}`.
러너는 정상 종료 (대표 rc) 뒤에도 그룹을 정리하고, **그룹을 못 비우면 런 항목을 닫지 않는다** (`stop_failed` · `end` 없음 · 비용 미확정 → 재시작은 그룹이 사는 동안 거부 · 죽은 뒤 보수 상한) · STOP `abnormal` · 다음 시드 안 띄움 · 중단 경로의 STOP 사유도 그룹을 비웠는지에 따라 다르게 쓴다.
- 시험 (진짜 Linux 프로세스): TERM 이 그룹 전체 (손자) 에 가서 KILL 없이 빈다 · 그룹 밖 프로세스는 산다 / **대표는 TERM 에 죽고 일꾼은 TERM 무시** → 그룹 KILL · 빔 / **대표가 rc 0 으로 먼저 끝나고 TERM 무시 일꾼이 남음** → 그룹을 보고 KILL · 빔. 가짜: 녹음 멈춤 · 정상 끝 각각 그룹이 안 비는 경우 → stop_failed · 끝 없음 · 23 · 재시작 거부 (그룹 살아 있음).

**P1-4 invalid ≠ 과학적 종료** — 첫 시드 녹음 판정이 invalid 이거나 시드 판정이 closes_system 이 아니면 STOP code `invalid` (종료코드 27 · terminal 아님 · 사유 "자료 · 판독 오류로 멈춘 것이지 그 계가 기준을 못 넘었다는 증거가 아니다"). 묶음 invalid 도 `invalid` (예전엔 terminal `track`). terminal 은 과학적 종료 둘 (`melt` = 첫 시드 녹음 fail ∧ closes_system · `track` = stop_track) 뿐.
재개 절차를 나눴다: invalid → 원인을 고치고 그 시드 폴더를 옆으로 (`seed11 → seed11.invalid_<날짜>`) 옮긴 뒤 `--ack_stop` (앞 런 비용은 장부에 남는다) / 과학적 종료 → 새 카드 · 새 run_root 만.
- 시험: DH 재현 그대로 (0 번 프레임 종 바뀜) → 판정 invalid · closes 아님 · STOP invalid · terminal 아님 / 폴더를 옆으로 + ack → 10 런 다시 · 장부 11 런 · 1 단계 통과.

**P1-5 재판정 이력** — `stage1_verdict(…, reason=…)` 가 덮어쓰기 **전에** `<시드>/stage1_verdict_history.jsonl` 에 한 줄: 이전 판정 **전체** · 이전 · 새 지문 (원자료 · 카드 값 · 도구) · 무엇이 바뀌었나 (상태 · 파일 · 카드 값 · 도구 · run_id) · 사유 (러너 재시작 · 담금질 끝 · 첫 시드 녹음 멈춤 · 상한 멈춤 · 수동). 러너 로그에도 지문 변화를 적는다.
- 시험: DH 재현 그대로 (final.xyz 에 빈 줄) → 묶음 무효 → 러너 재판정 pass → pass · rc 0 · 이력에 이전 판정 · 바뀐 파일 ["final.xyz"] · 이전 ≠ 새 지문 · 사유.

**인터페이스가 바뀐 곳**: 드라이버 `--run_id` (32 hex · plan.json run_id) · `stage1_verdict(..., reason=)` · `ledger_cost` → `ledger_check(out_root, verdicts, values)` (반환에 invalid · pending 목록) · 판정에 `run_id` · `history` · 묶음에 `identity_problems` · 러너 RC 27 (`invalid`) · `_Proc.stop()` 이 dict 를 돌려준다 · 장부 런에 `run_id` · `cost_basis` · (고아) `wall_h_lower` · (실패) `cleanup` · `stop_failed`.

## 3. 이것을 특히 봐 달라

1. 고아 런의 보수 상한 = "그룹이 죽은 것을 본 시각 − 시작" — 러너가 오래 죽어 있었으면 상한이 크게 잡혀 상한 회계가 '미완결' 쪽으로 기운다. 안전 쪽이라 받아들였는데, 이 정도면 되는가 (더 좋은 종료 기록 — 예: 드라이버가 끝에 쓰는 시각 — 을 요구해야 하는가).
2. `ledger_check` 가 판정이 **없는** 장부 런 (예: invalid 로 옆으로 옮긴 런 · 상한 멈춤 런) 은 비용으로만 더하고 판정과는 안 잇는다 — 맞는가.
3. 그룹 잔존 판정이 Linux `/proc` 의 pgrp 에 기댄다 (좀비 제외) — 자기 pgid 를 바꾼 손자 (setsid · setpgid) 는 못 본다 (도구 docstring 에 한계로 적었다). UMA 담금질 (python · torch) 에서 이 가정이 맞는가.
4. 시드 판정이 run_id 없는 plan 을 무효로 한다 — 손 실행 (`--print_cmd`) 은 이제 1 단계 판정에 못 들어간다 (러너 전용). 맞는가.
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DH 지적마다 닫힘 여부 한 줄.
