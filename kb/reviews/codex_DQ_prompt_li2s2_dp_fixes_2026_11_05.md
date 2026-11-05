---
title: "DQ 프롬프트 — li2s-2 DP 고침 + DQ 전 독립 리뷰 고침 (⏳BASE): 저장 경계의 신호 (바깥 구간 · 교체 뒤 실패) · 현재 폴더 미해결 기록 · 독립 요약 = 러너와 같은 규칙 (같은 실행 충돌 공통 함수 · STOP · 장부 지문 · 이력 꼴) · 판정 쓰기 구간 · 낡은 요약 — 첫 담금질 GO 여부"
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

DP 의 P0-1 · P1-1 · P1-2 · P2-1 · P2-2 를 고쳤다 (091353ed · e1455a2d · 698e1a8d). 그 판을 바로 보내지 않고 **결과를 모르는 독립 리뷰어 하나**에게
DP 재승인 조건 셋을 반례로 깨 보라고 줬고, 리뷰어가 **조건 ③ 이 아직 안 닫혔다** (요약의 같은 실행 규칙이 러너보다 좁다 · P1) 와 P2 일곱 · P3 둘을
재현했다 — 그것도 같은 꼴 전체로 고쳤다 (⏳FIXC · §2 끝). 결과 0 건 · 카드 값 그대로 (값 지문 086de59c484f9c32).

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

**DQ 전 독립 리뷰 (2026-11-05 · 결과 모름 · 재현으로 확인) — 지적과 고침** (`db/raw/li2s2_dq_mutation_2026_11_05/README.md` 에 표)
- **P1-A 같은 실행 규칙이 요약에서 좁았다** (재현: 장부 판정 invalid · incomplete · 'PASS' ↔ 폴더 pass · 장부 invalid ↔ 폴더 fail → 요약 stage1_pass + 2 단계 · 러너는 27).
  → **한 함수** `ledger_verdict_conflict(row, folder_status)` 를 러너 ①-4 · persist · 소비자 `_ledger_check` 가 같이 쓴다: 장부 판정이 허용 값 밖이면 문제 · 폴더 판정이
  pass · fail 이고 장부 판정이 있는데 다르면 (incomplete · invalid 포함) 충돌 · 장부 녹음 fail ↔ 폴더 pass 충돌. 요약은 판정 파일이 없는 행의 모르는 판정 값도 invalid.
- **P2-B 러너가 '장부에 적었다' 고 말했는데 아무것도 안 적혔다** (장부 판정이 이미 있으면 덮지 않음). → 충돌이면 덮지 않고 그 행에 `verdict_observed_conflict`
  (상태 · 어디서 · 시각 · 이유) 로 남기고 멈춘다 · 로그는 한 일을 그대로 (적음 · 충돌 관측 · 이미 같음) · 요약도 충돌 관측이 있는 행 = invalid.
- **P2-A 시작 점검 도중 신호가 확인 안 된 닫는 STOP 을 interrupted 로 덮었다** (재현: STOP melt + `_leftover_tmps` 안 SIGTERM → rc 26 · STOP 바뀜).
  → `stop_pending` 을 잠금 직후 · 처리기를 걸기 **전에** 켠다 (잠금 뒤라 다른 러너가 새 STOP 을 못 쓴다).
- **P2-C 요약의 미해결 기록 검사가 `_run_kind` 보다 좁았다** (이력 줄 prev null · 없음 · 모르는 상태 → 요약 통과). → `_verdict_records` 가 이력 줄의 prev 꼴 ·
  이전 · 새 판정 상태를 본다 (상태 없는 원문 판정은 기록으로 남겨 요약이 따로 본다).
- **P2-D 러너는 거부하는데 요약은 통과** (잘린 STOP · 기록은 통과인데 닫는 STOP · 첫 시드가 아닌 실행의 closes_system). → 소비자가 STOP.json 을 읽는다
  (`stop_record`): 못 읽음 = invalid · 닫는 STOP (melt · track · terminal) 인데 기록 판정이 닫힘이 아니면 invalid · 그 밖의 확인 안 된 멈춤 = pending (통과로 안 올림) —
  러너는 invalid 코드를 기록 오류에도 '과학적 결과가 있어 재시도 거부' 같은 운영 멈춤에도 써서, 코드로 기록 오류를 가르지 않는다. 첫 시드 아닌 closes_system 은
  러너 ①-3 · 요약 (장부 · 판정 파일) 둘 다 **기록 오류 (invalid)** 로 본다 (전에는 러너가 닫는 STOP melt 로 받았다 — 카드: 첫 시드 녹음만 계를 닫는다).
- **P2-E 판정 파일 쓰기가 `_critical` 밖이었다** (재현: 끝 판정 교체 직전 SIGTERM → 판정 임시 파일이 남아 그 뒤 시작마다 resume). → 러너가 판정을 쓰는 네 자리
  (담금질 끝 · 시작 전 재판정 · 첫 시드 녹음 멈춤 · 실행 중 상한) 를 구간 안에서.
- **P2-F 거부해도 낡은 통과 요약 파일이 남았다**. → 러너가 잠금을 잡으면 먼저 기존 `stage1_summary.json` 을 '지금 판정 아님' (pending · `not_current` · 2 단계 없음)
  으로 바꾼다 — 다시 판정하면 새 요약이 덮는다.
- **P2-G 요약에 카드 · 도구 고정이 없었다** (카드 값만 바꿔 모든 시드를 다시 판정하면 요약은 통과 · 러너는 고정값으로 거부). → 장부의 `card_values_sha16` ·
  `driver_sha16` 를 지금 판정에 쓰는 카드 값 · 도구와 대조 (러너는 불러온 도구 모듈의 지문을 장부에 적고, 시작 때 바로 저장한다 — ①-4 요약이 디스크 장부를 읽는다).
- **P3** 요약 로그 문구 ('지문 불일치' → '판정 무효 (지문 · 미해결 기록 · 꼴)') · 이 실행이 STOP 을 쓴 뒤 끊기면 (교체 뒤 실패 · 미룬 신호) 그 STOP 의 코드로 끝낸다
  (전에는 26 · 디스크 STOP 은 맞았다).
- 리뷰어가 괜찮다고 본 것 (재현): 조건 ① (실제 `os.kill` 을 교체 직후에 · 확인 · 재시도 × 첫 · 둘째 시드) · 조건 ② (판정 임시 파일 · 깨진 이력 · 원문 판정 × A11 · B14) ·
  확인 구간 · 교체 뒤 실패 처리 · 공통 꼴 검사.

**인터페이스가 바뀐 곳**
- 드라이버: `ledger_shape_problems` · `record_tmp_problems` · `RECORD_TMP_NAMES` · `_stage1_summary_core` (현재 폴더 미해결 기록) · `_ledger_check` (공통 꼴 검사 · 임시 파일 ·
  장부 지문 · STOP · 첫 시드 아닌 닫힘 · 충돌 관측) · `LEDGER_VERDICTS` · `ledger_verdict_conflict` · `STOP_TERMINAL_CODES` · `stop_record` · `mark_summary_not_current` ·
  `summarize_stage1` (닫는 STOP ↔ 기록 대조 · 첫 시드 아닌 판정의 closes_system) · `_verdict_records` (이력 줄 prev · 상태 꼴).
- 러너: `_AfterReplace` · `_write_json_atomic` (교체 뒤 실패를 따로) · `HELD_SIGNALS` 는 있는 신호만 건다 (Windows 에 SIGHUP 없음) · `state["stop_code"]` ·
  장부 `driver_sha16` = 불러온 도구 모듈의 지문 (시작 때 저장) · 고정값 `EXPECTED_DRIVER_SHA16 = ⏳DRV` (`EXPECTED_VALUES_SHA16` 그대로).

## 3. 이것을 특히 봐 달라

1. **바깥 구간이 덮는 범위** — persist · stop · 확인 · 실행 전 기록. 이 밖에 '기록 쓰기 + 메모리 확정' 이 둘로 나뉜 자리가 남았는가 (끝 처리 `finish` · 고아 마감 · 증언 · 실행 중 상한 · 녹음 판정 기록).
2. **`_AfterReplace` 를 '저장됨' 으로 본다** — 디렉터리 fsync 실패는 내구성이 불확실할 뿐 내용은 새 것이다. 그 뒤 멈추는 코드 (확인 = refused · 루프 = invalid) 가 맞는가. 디렉터리 fsync 가 늘 실패하는 파일 시스템이면 첫 저장부터 멈춘다 (전과 같음) — 받아들일 만한가.
3. **미룬 신호와 예외** — 구간이 예외로 끝나면 미룬 신호를 버리고 그 예외를 둔다. 구간 안 예외를 잡고 **계속 도는** 호출자가 있으면 신호를 잃는다 — 내가 본 범위에서는 없다 (예외는 모두 멈춤 · 거부 · 끝 처리로 간다). 빠진 자리가 있는가. 또 끝 처리 쓰기 구간 안에 두 번째 신호 (Ctrl-C 두 번) 가 오면 끝 처리가 STOP interrupted 를 못 쓰고 예외로 나간다 — 시험으로 확인한 것: 조용히 이어가지 않고 · 장부 행은 끝남 (interrupted) · 잠금 풀림 · 다음 시작은 판정 없는 폴더를 보고 그 실행에 묶인 resume STOP 으로 멈춘다 (발사 0 · 덮지 않음 — 한 번 Ctrl-C 때와 같은 자리에 STOP 하나 덜 거쳐 온다). 이 처리가 맞는가 (끝 처리에서 미룬 신호를 버려야 하는가).
4. **요약의 '미해결 판정 기록'** — 판정 임시 파일 · 깨진 이력 줄 · 상태 없는 이전 판정. 다른 미해결 꼴이 있는가.
5. **같은 실행 충돌의 범위 (리뷰 P1-A 뒤 넓힘)** — 장부 판정이 있으면 (incomplete · invalid 포함) 폴더의 pass · fail 과 다를 때 충돌이다 (러너 ①-4 와 같다). 그래서
   장부가 incomplete · invalid 인 실행을 사람이 원자료를 고쳐 pass 로 다시 판정하면 러너 · 요약 둘 다 멈춘다 (사람이 장부를 보고 정한다). DP Q2 의 'incomplete → pass 는
   구분' 을 이렇게 (멈추고 사람이 본다) 읽었다 — 맞는가, 아니면 incomplete → pass 를 두 쪽 같이 허용해야 하는가.
6. **확인 안 된 STOP 의 요약 처리** — 닫는 STOP 은 기록과 대조 (안 맞으면 invalid) · 그 밖은 pending. 확인 안 된 멈춤이 있는 동안 요약이 통과로 안 오르는 것이
   운영상 맞는가 (끝난 뒤 신호로 interrupted STOP 이 남으면 사람이 확인해야 통과가 된다).
7. **시작 때 바로 저장하는 것** — 러너는 잠금 뒤 낡은 요약을 '지금 판정 아님' 으로 바꾸고 · 장부 지문을 바로 저장한다 (거부로 끝나도). 시작 점검의 부작용이 이 둘뿐인 것이 맞는가.
8. **변이 제외 넷** (위) — 범위를 좁힌 설명이 맞는가.
9. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DP 지적 (P0-1 · P1-1 · P1-2 · P2-1 · P2-2) 과 재승인 조건 셋 · DJ Q5 마다 닫힘 여부 한 줄.
