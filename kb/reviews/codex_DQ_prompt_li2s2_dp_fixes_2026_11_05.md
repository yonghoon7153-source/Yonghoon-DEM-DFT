---
title: "DQ 프롬프트 — li2s-2 DP 고침 (⏳BASE): 저장 경계의 신호 (바깥 구간 · 교체 뒤 실패) · 현재 폴더 미해결 기록 (written False · 요약) · 독립 요약의 장부 검사 · 직접 진입 엄격 판독 시험 · 변이 제외 설명 좁힘 — 첫 담금질 GO 여부"
date: 2026-11-05
updated: 2026-11-05
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DQ
track: li2s
channel: codex
kind: prompt
status: draft — 발송 대기 · 기준 커밋 ⏳BASE
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DP (4a269bac · NO-GO · P0 1 · P1 2 · P2 2) 다음 편지다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `⏳BASE` (브랜치 `claude/friendly-meitner-lldvar` · 기록까지 들어간 커밋). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DQ_reply_li2s2_dp_fixes_2026_11_05.md` 로 원문 보존.

---

**[li2s-2] DP 고침 확인 — 재승인 조건 셋이 닫혔나 · 새 구멍은 없나 · 발사 GO 여부**

## 0. 무엇을 묻나

DP 의 P0-1 · P1-1 · P1-2 · P2-1 · P2-2 를 고쳤다 (091353ed · e1455a2d · ⏳FIXC). 결과 0 건 · 카드 값 그대로 (값 지문 086de59c484f9c32).
고치면서 DP 가 짚은 자리만이 아니라 **같은 꼴** (기록 쓰기와 메모리 확정이 둘로 나뉜 자리 · 러너가 거부하는데 요약은 받는 기록) 을 같이 찾아 고쳤다.

**물음: DP 재승인 조건 셋이 닫혔는가 · DP P2 둘이 닫혔는가 · 고치면서 새 구멍이 생겼는가 · 1 단계를 띄워도 되는가 (GO / 조건부 GO / NO-GO).**

DP 의 재승인 조건 (원문 그대로):
1. 성공한 저장 뒤 신호가 와도 관측한 실패가 끝 저장에서 사라지지 않을 것 (확인 · 재시도 × 첫째 · 뒤 시드).
2. 현재 폴더의 미해결 판정 · 이력 · 임시 파일을 새 실행 전에 막을 것 (일부 시드만 완료된 묶음에서도 추가 실행 0).
3. 독립 요약도 같은 기록을 거부할 것 (장부 · STOP 임시 파일과 같은 run_id 의 판정 충돌에서 통과 · 2 단계 선정 없음).

DP 가 닫힘으로 본 항목 (DO P1-2 · DO P2-1 기존 결함 · DO P2-2 코드상 · DJ Q2 기존 경계) 은 다시 열지 않아도 된다.
**가능하면 DP 재현 (`dp_records_consumer` · `q6_mutation_controls` 포함) 을 이 커밋에 다시 돌려 달라.**

## 1. 보는 범위

- `git diff 4a269bac ⏳BASE -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_DP_회신_고침_v10_2026_11_05` (규칙 · 못 하는 것) — 결과 0 건 · 카드 값은 안 바뀜
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 233) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 120 · Linux)
  - Windows 에서는 러너의 POSIX 전용 6 개를 건너뛴다 (DP 때 5 개 + 교체 뒤 디렉터리 fsync 실패 1 — Windows 는 디렉터리 fsync 를 안 한다) → **114** 가 맞다. 드라이버는 그대로 233.
  - 새 '미룬 신호' 시험은 OS 신호를 쓰지 않는다 — 처리기가 쓰기 구간 안에서 불린 상태 (`_PENDING`) 를 교체 직후에 만든다 (Codex DP 주입 자리) → Windows 에서도 돈다.
- 깨기 (변이) ⏳MUT — `db/raw/li2s2_dq_mutation_2026_11_05/` (README · 하네스 · 로그 · SHA256SUMS).

## 2. 한 것

**DP P0-1 · P2-1 — 저장 경계의 신호: 쓰기와 메모리 확정을 한 바깥 구간으로 · 교체 뒤 실패를 따로.**
- `persist_observed`: 메모리 변경 → 장부 저장 → 성공 확정을 한 `_critical` 구간으로 묶었다. 구간 안에서 온 TERM · HUP · INT 는 구간이 **끝난 뒤** 던진다 → 이미 확정된 뒤라 '저장 실패 → 메모리 되돌림' 으로 가지 않는다.
- `_write_json_atomic`: 이름 교체 뒤의 실패 (디렉터리 fsync) 를 `_AfterReplace` (OSError 하위) 로 따로 알린다 — 디스크에 새 내용이 있으니 부르는 쪽은 **메모리를 되돌리지 않는다** (persist 는 그래도 멈춘다: 확인 경로 = 거부 · 재시도 · 재판정 = invalid · 장부 행은 디스크 · 메모리 같음).
- `stop()`: STOP 쓰기와 `stopped` 확정을 한 구간으로 · `_AfterReplace` 면 `stopped` 를 확정한 뒤 다시 던진다 → 끝 처리가 terminal STOP 을 interrupted 로 덮지 않는다.
- 같은 꼴 (DP 가 직접 짚지 않은 곳): 확인 (`--ack_stop`) 의 확인 기록 저장 → STOP 지우기 → `stop_pending` 끝 = 한 구간 · 시드 폴더 · 실행 전 기록 (`stage1_attempt.json`) · 장부 행 만들기 = 한 구간 (그 사이 신호로 장부에 없는 폴더가 안 남는다).
- 시험 (Codex 재현 순서): 확인 · 재시도 × 첫 · 둘째 시드 넷 — 교체가 끝나는 순간 미룬 신호 → 장부 행이 남고 (첫 시드는 closes_system) · 궤적을 망가뜨린 뒤 다시 띄워도 추가 담금질 0 · stage1_pass 없음 / terminal STOP (melt) 교체 직후 미룬 신호 → STOP 그대로 melt / 교체 뒤 실패 (디렉터리 fsync · POSIX) → 확인 = 거부 · 루프 = invalid · 장부 melt_check fail 유지 · terminal STOP 유지 / 실행 전 기록 교체 직후 미룬 신호 → 장부 행이 있고 끝남 (interrupted) · 발사 0.

**DP P1-1 — 현재 폴더의 미해결 기록 (새 실행 전에 막는다).**
- 러너: ①-4 재판정에서 `stage1_verdict` 가 `written: False` (판정 임시 파일이 남은 폴더) 면 다음 시드로 가지 않고 **invalid 로 멈춘다** (디스크의 옛 판정으로 가지 않는다). 담금질이 끝난 뒤의 판정도 같은 규칙.
- 드라이버 요약 (`_stage1_summary_core`): 현재 시드 폴더의 판정 기록을 다시 읽어 — 판정 임시 파일 · 깨진 이력 줄 · 상태 없는 이전 판정 (재판정 뒤 원문만 남은 것 · `raw_b64`) 이 있으면 그 시드 invalid ("미해결 판정 기록"). `run_kind` 가 과학적 판정을 먼저 돌려줘도 이 검사를 건너뛰지 않는다.
- 시험 (Codex 재현): 8 실행까지만 끝난 묶음 (상한 멈춤) 에서 A11 에 판정 임시 파일 · 깨진 이력 줄 · 같은 열쇠 판정 → 상한을 올려 확인하고 이어가도 **새 실행 0** · invalid 멈춤 (임시 파일 경우는 '다시 쓰지 못했다' 이유) · 요약 invalid / 담금질 끝 판정 `written: False` → 다음 시드로 안 감 (invalid · 발사 1).

**DP P1-2 — 독립 요약도 러너가 거부하는 장부를 거부한다.**
- 장부 꼴 검사 한 곳 `ledger_shape_problems` (러너 · 소비자가 같이 쓴다): 객체 · `runs` 와 `stop_history` 가 **있고** 둘 다 객체 목록 — 소비자도 없는 열쇠를 `[]` 로 채워 읽지 않는다.
- `record_tmp_problems`: run_root 의 장부 · STOP 임시 파일 = invalid (자동 승격 안 함).
- 같은 실행 충돌: 장부 `verdict` 와 폴더 판정이 pass / fail 로 다르면 invalid · 장부 녹음 fail 인데 폴더 판정 pass 면 invalid (incomplete · invalid 는 충돌로 안 본다 — DP Q2 의 incomplete → pass 구분).
- 시험 (Codex 재현): 다 통과한 묶음에 장부 임시 파일 (A11 녹음 fail · 닫힘) · STOP 임시 파일 · 같은 실행의 장부 fail ↔ 폴더 pass · 장부 녹음 fail ↔ 폴더 pass · stop_history 누락 · **stop_history 빈 객체 `{}`** → 요약 invalid · 2 단계 없음 (손 안 댄 묶음은 stage1_pass).

**DP P2-2 — 변이 제외 설명을 좁혔다 · 직접 진입 시험.**
- 드라이버 시험: 카드 `기계_판독_값` · G4 밴드 카드 · `gate_check` · `seed_gate` 의 plan 에 같은 열쇠 둘 (마지막 값이 정본이어도) → 직접 진입에서도 거부 → 변이 DQ14–DQ17 로 깬다 (더는 '같은 결과' 로 빼지 않는다).
- 남은 제외 넷 (하네스 머리글 · 범위를 좁혀 적었다):
  1. `persist_observed` 의 즉시 저장 끄기 — **같은 프로세스 안에서만** 같은 결과 (끝 처리가 같은 장부를 저장). 급작스러운 종료 (kill -9 · 정전) 에서는 다르다 — 즉시 저장은 그 경우를 위한 것이고 이 시험 틀 (한 프로세스) 로는 재현하지 않는다.
  2. 시드 루프의 판정 상태 엄격 판독 끄기 — **조건부**: 바로 앞 ①-4 가 그 판정을 원자료로 다시 썼을 때만 같은 열쇠 둘이 남을 수 없다. 다시 못 쓰면 (`written: False`) ①-4 가 멈춘다 (DQ7 이 그 멈춤을 깬다).
  3. 확인 경로의 '적기 실패 → 거부' return 끄기 — DP 동의 그대로.
  4. 확인 구간 (확인 기록 저장 · STOP 지우기 · 확인 끝 표시) 끄기 — 그 사이 신호로 끊겨도 확인 기록은 저장됐고 STOP 이 남아 (`stop_pending` 이라 끝 처리가 안 덮는다) 다음 확인이 같은 stop_id 의 기록을 다시 쓰지 않고 지운다 (같은 결과).
- ⭐ 깨기를 설계하다 내 설명 하나가 또 틀린 것을 찾았다 — `_ledger_check` 의 꼴 검사 끄기를 '뒤 원소 검사가 같은 장부를 invalid 로' 라고 빼려 했는데, **빈 객체 `stop_history` (`{}`)** 는 뒤 원소 검사가 못 본다. 요약 시험을 더하고 DQ18 (소비자) · DQ19 (러너) 로 깬다.

**인터페이스가 바뀐 곳**
- 드라이버: `ledger_shape_problems` · `record_tmp_problems` · `RECORD_TMP_NAMES` · `_stage1_summary_core` (현재 폴더 미해결 기록 · 같은 실행 충돌) · `_ledger_check` (공통 꼴 검사 · 임시 파일).
- 러너: `_AfterReplace` · `_write_json_atomic` (교체 뒤 실패를 따로) · `HELD_SIGNALS` 는 있는 신호만 건다 (Windows 에 SIGHUP 없음) · 고정값 `EXPECTED_DRIVER_SHA16 = 3a876a9322e4a52e` (`EXPECTED_VALUES_SHA16` 그대로).

## 3. 이것을 특히 봐 달라

1. **바깥 구간이 덮는 범위** — persist · stop · 확인 · 실행 전 기록. 이 밖에 '기록 쓰기 + 메모리 확정' 이 둘로 나뉜 자리가 남았는가 (끝 처리 `finish` · 고아 마감 · 증언 · 실행 중 상한 · 녹음 판정 기록).
2. **`_AfterReplace` 를 '저장됨' 으로 본다** — 디렉터리 fsync 실패는 내구성이 불확실할 뿐 내용은 새 것이다. 그 뒤 멈추는 코드 (확인 = refused · 루프 = invalid) 가 맞는가. 디렉터리 fsync 가 늘 실패하는 파일 시스템이면 첫 저장부터 멈춘다 (전과 같음) — 받아들일 만한가.
3. **미룬 신호와 예외** — 구간이 예외로 끝나면 미룬 신호를 버리고 그 예외를 둔다. 구간 안 예외를 잡고 **계속 도는** 호출자가 있으면 신호를 잃는다 — 내가 본 범위에서는 없다 (예외는 모두 멈춤 · 거부 · 끝 처리로 간다). 빠진 자리가 있는가. 또 끝 처리 쓰기 구간 안에 두 번째 신호 (Ctrl-C 두 번) 가 오면 끝 처리가 STOP interrupted 를 못 쓰고 예외로 나간다 — 시험으로 확인한 것: 조용히 이어가지 않고 · 장부 행은 끝남 (interrupted) · 잠금 풀림 · 다음 시작은 판정 없는 폴더를 보고 그 실행에 묶인 resume STOP 으로 멈춘다 (발사 0 · 덮지 않음 — 한 번 Ctrl-C 때와 같은 자리에 STOP 하나 덜 거쳐 온다). 이 처리가 맞는가 (끝 처리에서 미룬 신호를 버려야 하는가).
4. **요약의 '미해결 판정 기록'** — 판정 임시 파일 · 깨진 이력 줄 · 상태 없는 이전 판정. 다른 미해결 꼴이 있는가.
5. **같은 실행 충돌의 범위** — pass / fail 끼리만 충돌로 본다 (incomplete · invalid 는 아님). 장부 판정이 incomplete 인데 폴더가 pass 인 정상 경로 (끝까지 돈 뒤 다시 판정) 를 막지 않으려는 것이다. 맞는가.
6. **변이 제외 넷** (위) — 범위를 좁힌 설명이 맞는가.
7. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DP 지적 (P0-1 · P1-1 · P1-2 · P2-1 · P2-2) 과 재승인 조건 셋 · DJ Q5 마다 닫힘 여부 한 줄.
