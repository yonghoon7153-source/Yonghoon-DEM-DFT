---
title: "DP 프롬프트 — li2s-2 DO 고침 + DP 발송 전 독립 리뷰 둘 고침 (__BASE__): 복구 · 확인 · 재판정에서 본 과학적 결과를 장부에 · 모든 기록 엄격 판독 · 못 읽은 장부를 다시 쓰지 않음 · 남은 임시 파일 · 요약 fail-closed · 신호 — 첫 담금질 GO 여부"
date: 2026-11-04
updated: 2026-11-04
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DP
track: li2s
channel: codex
kind: prompt
status: 초안 → 발송 대기 · 기준 커밋 __BASE__
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DO (802290db · NO-GO · P0 1 · P1 2 · P2 2) 다음 편지다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `__BASE__` (브랜치 `claude/friendly-meitner-lldvar` · 기록까지 들어간 커밋). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DP_reply_li2s2_do_fixes_2026_11_04.md` 로 원문 보존.

---

**[li2s-2] DO 고침 + 발송 전 독립 리뷰 둘의 고침 확인 — 재승인 조건 셋이 닫혔나 · 새 구멍은 없나 · 발사 GO 여부**

## 0. 무엇을 묻나

DO 의 P0 1 · P1 2 · P2 2 를 고쳤다 (115aa9eb). 그 판을 바로 보내지 않고 **서로 모르는 리뷰어 둘**에게 같은 질문 ("고친 자리가 같은 꼴 전체를 덮었나 · 새로 생긴 조용히 틀린 경로가 있나") 을 따로 줬고, 둘이 더 찾은 것 (첫째 P0 1 · P1 2 · P2 2 · 둘째 P1 2 · P2 4 · 잔 항목) 도 고쳤다. 결과 0 건 · 카드 값 그대로 (값 지문 086de59c484f9c32).

**물음: DO 재승인 조건 셋이 닫혔는가 · DO P2 둘이 닫혔는가 · 고치면서 새 구멍이 생겼는가 · 1 단계를 띄워도 되는가 (GO / 조건부 GO / NO-GO).**
DO 가 닫힘으로 본 항목 (DN P1 · P2 · 실시간 첫 시드 fail 보존 · 보존 폴더 식별 · 끊긴 런 분류 · MD 뒤 산출물) 은 다시 열지 않아도 된다.

**가능하면 DO 재현 셋 (do_melt_policy · do_consumer_records · do_runner_recovery) 과 대조를 이 커밋에 다시 돌려 달라.**

## 1. 보는 범위

- `git diff 802290db __BASE__ -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_DO_고침_v8_2026_11_04` · `개정_DP_전_리뷰_v9_2026_11_04` (규칙 · 못 하는 것) — 결과 0 건 · 카드 값은 안 바뀜
- 리뷰 둘의 지적과 처리: `db/raw/li2s2_pre_dp_review_2026_11_04/README.md`
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 231) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ __RUN_N__ · Linux)
  - Windows 에서는 러너의 POSIX 전용 5 개를 건너뛴다 (진짜 프로세스 그룹 2 · 띄우는 순간 신호 1 · 자식 신호 마스크 2) → __WIN_N__ 이 맞다. 드라이버는 그대로 231.
- 깨기 (변이) **__MUT__** — DO 판 222 개 · 자리가 바뀐 8 개 (K14 · K28 · L12 · L13 · DO43 · DO23 · DO47 · R4) 를 옮기고 DP 자리 65 개를 더했다 (287). `db/raw/li2s2_dp_mutation_2026_11_04/`

## 2. 한 것

**DO P0 — 복구 · 확인 경로가 본 과학적 결과를 거부 전에 장부에 (리뷰 첫째 F1 · F2 로 넓힘).**
- `run_kind_detail(row, folder, values)` — `run_kind` 와 같은 분류에 근거를 붙인다: 보존 폴더 녹음 판정 (verdict · D · 창 · 프레임 수) · **폴더 판정 기록 (상태 pass · fail · closes_system)**.
- 러너의 재시도 자격 검사 · 확인 (`--ack_stop`) 의 선언 검사가 그것을 위로 넘기고, `run()` 의 `persist_observed` 가 거부 전에 그 실행의 장부 행에 적는다:
  - 녹음 → `melt_check` fail (`observed_in` · 시각) · 다른 `melt_check` 는 `melt_check_history` 로.
  - 판정 기록 → 장부 `verdict` 가 비었을 때만 그 상태 (`verdict_observed` 에 경로 · 시각) — 이미 있으면 덮지 않는다.
  - 계의 첫 시드면 `closes_system` (녹음 fail · 판정의 closes_system).
- 시작 전 재판정 (①-4) 의 pass · fail 도 같은 방식으로 장부에 · 장부에 이미 다른 판정이 있으면 덮지 않고 **invalid 로 멈춘다**.
- 재시도 자격 경로에서 첫 시드면 STOP melt (terminal) · 뒤 시드면 멈춤 · 확인 경로는 적고 거부.
- 적다가 실패하면 (행 꼴 · 저장 예외) 메모리의 장부도 되돌리고 (끝 처리가 반쯤 적은 것을 쓰지 않게) 확인 경로는 거부 · 재시도 · 재판정 경로는 invalid.
- 못 읽은 이전 판정 (상태 없음 · 원문만) 은 '흔적 없음' 이 아니라 판독 불가 · 끊긴 런의 녹음 invalid 는 끊긴 런 (끝난 런만 invalid — 끊긴 런 재시도 한도 우회 막기).

**DO P1-1 · P1-2 — 같은 열쇠 둘 = 못 읽음 (모든 기록) · 못 읽은 원본을 다시 쓰지 않음.**
- 드라이버: 판정 (현재 · 이력 줄 · 재판정 때 이전 판정) · 판정 상태 · 실행 전 기록 · plan · MD 완료 기록 · 카드 · G4 밴드 카드 → `loads_strict`.
- 재판정 때 이전 판정을 엄격히 못 읽으면 원문을 **바이트 그대로** (`raw_b64` · sha256) 이력에 남긴다 (상태 None — 그 폴더는 보류). 이력은 `\n` 으로만 나눈다 (글자 안 U+2028 · U+0085 에서 안 자름).
- 러너: 장부 (`run()` · 증언 근거 보기 · 증언 적기) · 결정 원장 · 실행 전 기록 · 판정 상태 → `_loads_strict`. 못 읽은 장부는 `state` 에 넣지 않고 거부 (끝 처리가 다시 쓰지 않는다).
- 장부는 `runs` · `stop_history` 가 **있고** 객체 목록일 때만 받는다 (채워 넣지 않음 · 둘째 F1).

**남은 임시 파일 (둘째 F2).** 장부 · STOP 의 `*.json.tmp` 가 남아 있으면 러너 · 증언이 거부 · 원자 쓰기는 O_EXCL (남은 것을 덮지 않고, 실패하면 자기 것만 지움) · 판정도 판정 임시 파일이 남은 폴더에는 아무것도 쓰지 않고 invalid (쓰지 않음).

**신호 (DO P2-2 · 둘째 F4 · F6).**
- 자식: `_Proc` preexec 가 막기 전 마스크로 돌아간 뒤 TERM · HUP · INT 를 **늘** 푼다 (러너가 TERM 막힌 채 시작해도). `_held` 를 겹쳐 불러도 바깥 값을 지우지 않는다.
- ⭐ 고치다가 selftest 가 잡은 것: `pthread_sigmask` 는 주 스레드만 막는다 — 다른 스레드가 받은 신호도 파이썬 처리기는 주 스레드에서 돌아서, 임시 파일을 만든 **직후** (try 밖) 처리기가 돌았다 → 임시 파일이 남아 다음 저장이 O_EXCL 로 막혔다. 쓰기 · 띄우고 손잡이 적기를 `_critical` 구간으로 묶어 그 안에서 온 TERM · HUP · INT 는 구간이 끝난 뒤 던진다.
- 확인 중 (STOP 을 지우기 전) 예외가 나도 끝 처리가 앞 STOP 을 '중단' STOP 으로 덮지 않는다 · 끝 저장이 실패해도 멈춤 코드를 낸다.

**요약 fail-closed (DO P2-1 · 둘째 F3).** 중첩 꼴 → 그 시드 invalid · 예외면 invalid 요약 · 신호면 invalid 요약 쓰고 다시 던짐 · 쓰기 실패면 이전 요약을 지우고 다시 던짐 (낡은 stage1_pass 가 안 남는다).

**앞 프레임 깨짐 (둘째 F5).** 녹음 창 안 앞 프레임 한 곳이 깨지면 (온전한 프레임이 그 뒤로 더 있거나 머리가 깨짐) '쓰는 중' 이 아니라 invalid · 계의 첫 시드가 녹음 미정으로 끝나면 러너가 다음 시드로 넘어가지 않고 invalid.

**잔 항목.** `--melt_window_check` CLI 는 판정을 화면에만 (런 폴더에 파일을 안 남긴다) · 소비자: 장부에 녹음 fail 로 적힌 실행 (판정 없이) 을 다른 실행으로 대체해도 잡는다 · stop_history 의 같은 stop_id 둘 = invalid · melt_check_history 꼴 검사.

**시험 (selftest)** — DO 재현 순서 그대로 (확인 · 재시도 자격 × 첫 · 둘째 시드 · 궤적 손상 · 원인 고침 선언 · 거부 유지 / 같은 열쇠 둘 / 장부 둘 / 중첩 꼴 / 진짜 프로세스 마스크) + 리뷰 둘의 재현 (폴더 판정 fail × 확인 · 재시도 × 첫 · 둘째 시드 · ①-4 기록 · 판정 다름 · 행 꼴 · 일시 · 남은 임시 파일 저장 실패 × 확인 · 재시도 · 장부 꼴 넷 · 남은 임시 파일 · O_EXCL · 증언 · 확인 중 예외 · 첫 시드 녹음 미정 · 요약 쓰기 실패 · 신호 · 앞 프레임 · 원문 바이트 · U+2028 · CLI · 소비자 대체 · 진짜 프로세스 물려받은 막힘 · 겹친 `_held`).

**인터페이스가 바뀐 곳**
- 드라이버: `run_kind_detail` (근거에 상태 · closes_system) · `MELT_OBSERVED_KEYS` · `VERDICT_SHAPE` · `_verdict_shape_problem` · `_summary_failed` · `_summary_write_or_drop` · `_stage1_summary_core` · `stage1_verdict` 반환 `written: False` (임시 파일이 남은 폴더).
- 러너: `_loads_strict` · `_held` · `HELD_SIGNALS` · `_child_restore_mask` · `_critical` · `_PersistFailed` · `_leftover_tmps` · `ack_declaration_problems(…, observed=None)` (원소에 `kind`) · `retry_eligibility` 반환 `observed` (kind melt · verdict) · 고정값 `EXPECTED_DRIVER_SHA16 = __DRV_SHA__` (`EXPECTED_VALUES_SHA16` 그대로).

## 3. 이것을 특히 봐 달라

1. **확인 경로의 닫힘** — 첫 시드의 과학적 결과 (녹음 fail · 판정 기록 closes_system) 를 확인 때 보면 장부에 `closes_system` 을 적고 거부만 한다 (STOP 을 덮지 않는다). 다음 시작에서 STOP 을 확인하면 '장부에 계를 닫은 사건' 으로 STOP melt. 빈틈이 있는가.
2. **재판정 다름 → invalid 멈춤** — 장부 판정이 있는데 ①-4 재판정이 다른 pass · fail 을 내면 멈춘다 (도구 · 원자료 변경을 사람이 본다). 정상 운영에서 이 멈춤이 나올 수 있는 경로가 있는가 (재시작 사이에 드라이버 고정값이 바뀐 경우 말고).
3. **뒤 시드의 복구 관측** — 장부에 적고 멈춘다. 그 시드를 묶음에 넣는 것은 사람이 보존 폴더를 되돌려 `--stage1_verdict` 하는 운영 단계 (리뷰 첫째 F5 를 고치지 않고 한계로 적었다). 이 운영 단계 전 · 중에 다른 우회 (예: 그 시드를 새로 띄움) 가 있는가.
4. **남은 임시 파일 = 거부** — 정전으로 남으면 사람이 정리할 때까지 시작하지 않는다 (진행 비용). 그 대신 덮지 않는 쪽을 골랐다. 맞는 쪽인가 · 덮어도 되는 경우가 있는가.
5. **`_critical` 신호 미룸** — 구간 안 TERM · HUP · INT 는 구간 끝에서 던진다 (예외로 나가는 중이면 그 예외를 둔다). 구간이 길어져 정리 · 멈춤이 늦어지는 자리 · 미룬 신호를 잃는 자리가 있는가.
6. **변이에서 뺀 것** (하네스 머리글): `persist_observed` 의 저장 끄기 (끝 처리가 어차피 저장) · 시드 루프의 판정 상태 엄격 판독 끄기 (바로 앞 ①-4 가 원자료로 다시 씀) · plan 엄격 판독 끄기 (카드 · gate · seed gate — 판정이 plan 을 먼저 엄격히 읽음) · 확인 경로의 '적기 실패 → 거부' return 끄기 (선언 문제 목록이 늘 비어 있지 않아 바로 아래가 같은 코드로 거부). 같은 결과라는 판단이 맞는가.
7. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DO 지적 (P0 · P1-1 · P1-2 · P2-1 · P2-2) · DJ 남은 항목 (Q2 · Q5) 마다 닫힘 여부 한 줄.
