---
title: "DP 프롬프트 — li2s-2 DO 고침 확인 (__BASE__): 복구 때 본 녹음 fail 을 장부에 · 모든 기록 엄격 판독 · 못 읽은 장부를 다시 쓰지 않음 · 요약 fail-closed · 자식 신호 마스크 — 첫 담금질 GO 여부"
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

**[li2s-2] DO 고침 확인 — 재승인 조건 셋 (복구에서 본 fail 영구 기록 · 판정 기록 엄격 판독과 원문 보존 · 무효 비용 장부 덮어쓰기 금지) 이 닫혔나 · 새 구멍은 없나 · 발사 GO 여부**

## 0. 무엇을 묻나

DO 의 P0 1 · P1 2 · P2 2 를 고쳤다 (결과 0 건). 지적된 자리만 고치지 않고 **같은 꼴 전체**를 훑었다:
- 본 과학적 결과를 그 자리에서 장부에 남기지 않는 곳 (P0).
- 기록을 느슨하게 읽는 곳 — 같은 열쇠 둘을 마지막 값으로 (P1-1 · P1-2). 두 파일의 JSON 읽기를 전부 뽑아 정했다.
- 못 읽은 원본을 정상 꼴로 다시 쓰는 곳 (P1-2).

**물음: DO 재승인 조건 셋이 닫혔는가 · P2 둘이 닫혔는가 · 고치면서 새 구멍이 생겼는가 · 1 단계를 띄워도 되는가 (GO / 조건부 GO / NO-GO).**
DO 가 닫힘으로 본 항목 (DN P1 · P2 · 실시간 첫 시드 fail 보존 · 보존 폴더 식별 · 끊긴 런 분류 · MD 뒤 산출물) 은 다시 열지 않아도 된다.

**가능하면 DO 재현 셋 (do_melt_policy · do_consumer_records · do_runner_recovery) 과 대조를 이 커밋에 다시 돌려 달라.**

## 1. 보는 범위

- `git diff 802290db __BASE__ -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_DO_고침_v8_2026_11_04` (규칙 · 못 하는 것) — 결과 0 건 · 카드 값은 안 바뀜 (값 지문 086de59c484f9c32 그대로)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 223) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 105 · Linux)
  - Windows 에서는 러너의 POSIX 전용 4 개를 건너뛴다 (진짜 프로세스 그룹 2 · 띄우는 순간 신호 1 · 자식 신호 마스크 1) → 101 이 맞다. 드라이버는 그대로 223.
- 깨기 (변이) **__MUT__** — DO 판 222 개 중 이번에 자리가 바뀐 5 개 (K14 · K28 · L12 · L13 · DO43) 를 옮기고 DP 자리 27 개를 더했다 (249). `db/raw/li2s2_dp_mutation_2026_11_04/`

## 2. 한 것

**DO P0 — 복구 · 확인 경로가 계산한 녹음 fail 을 거부 전에 장부에.**
- `run_kind_detail(row, folder, values)` — `run_kind` 와 같은 분류에 그 근거를 붙인다. 보존 폴더의 녹음 판정으로 정해졌으면 그 판정 (verdict · message · D · 창 · 프레임 수) 을 돌려준다. `run_kind` 는 그 첫 값이다.
- 러너의 재시도 자격 검사 (`retry_eligibility`) · 확인의 선언 검사 (`ack_declaration_problems`) 가 그것을 위로 넘긴다.
- `run()` 의 `persist_observed_melt` — 거부하기 전에 그 실행의 장부 행에 `melt_check` fail (`observed_in` · 시각) 을 적고 저장한다.
  - 계의 첫 시드면 `closes_system` (실시간 감시 경로와 같다).
  - 장부에 다른 `melt_check` 가 있으면 `melt_check_history` 로 옮긴다.
- 재시도 자격 경로에서 첫 시드면 STOP melt (terminal) · 뒤 시드면 지금처럼 멈춘다. 확인 경로는 적고 거부한다 — 다음 시작에서 '장부에 계를 닫은 사건' 검사가 닫힘을 잇는다.
- 그 뒤 궤적 원소를 손상해 녹음 판정이 invalid 가 돼도, 장부로 실행 종류는 과학적이다.

**DO P1-1 · P1-2 — 같은 열쇠 둘 = 못 읽음 (모든 기록).**
- 드라이버: 판정 (현재 · 이력 줄 · 재판정 때 이전 판정) · 판정 상태 · 실행 전 기록 (보존 폴더 식별 · 목록) · plan (단계 판독 · 판정 · 녹음 · gate · seed gate) · MD 완료 기록 · 카드 · G4 밴드 카드 → `loads_strict`.
- 재판정 때 이전 판정을 엄격히 못 읽으면 원문을 `raw_text` 로 이력에 남긴다 (상태 None — 그 폴더는 보류). 마지막 값으로 정규화하지 않는다.
- 러너: 장부 (`run()` · 증언 근거 보기 · 증언 적기) · 결정 원장 · 실행 전 기록 · 판정 상태 → 러너 자체 `_loads_strict` (드라이버를 싣기 전에도 쓴다 · 같은 뜻).
- 러너는 장부를 엄격히 못 읽으면 `state` 에 넣지 않고 거부한다 → 끝 처리 (`save_ledger`) 가 원본을 다시 쓰지 않는다. 증언도 원본을 안 건드린다.

**DO P2-1 — 요약 fail-closed.** `_verdict_shape_problem` (중첩 꼴) → 그 시드 invalid · 그래도 예외면 `_summary_failed` 로 invalid 요약 · 요약 파일은 임시 파일 → 이름 교체.

**DO P2-2 — 자식 신호 마스크.** 띄우는 코드를 `_held(fn)` 으로 뺐다 (부모만 막는다). `_Proc` 은 `preexec_fn=_child_restore_mask` 로 자식이 exec 전에 막기 전 마스크로 돌아간다.

**시험 (selftest 에 Codex 재현 순서 그대로)**
- P0: 확인 경로 · 재시도 자격 경로 × 첫 시드 · 둘째 시드. 순서는 녹음 창이 다 찬 직후 정전 → 거부 + 장부 확인 → 궤적 첫 프레임 원소 손상 → 원인 고침 선언 → 거부 유지 · 발사 0 · 소비자 통과 아님 (첫 시드는 stop_track).
- P1-1: 판정 `n` 130 · 71 (프레임만 남은 폴더) · 이력 `schedule_complete` true · false (+ 프레임 수 둘) · 같은 열쇠 둘 위에 재판정 → 원문 보존 · 보류. 드라이버 fixture: 판정 · 이력 · plan · MD 완료 기록 · 실행 전 기록 · 판정 상태 · 기록 목록.
- P1-2: 장부 `wall_h` 둘 → 러너 거부 · 원본 바이트 그대로 · 두 번째 실행도 거부 · 소비자 무효 그대로 / 고아 런 `wall_h_lower` 둘 → 근거 보기 · 증언 거부 · 원본 그대로 / 결정 원장 `decision_state` 둘 → '모름'.
- P2: 중첩 꼴 다섯 (provenance [1] · software [1] · run_id {} · reasons [] · files_sha256 [1]) → 그 시드 invalid · 이전 stage1_pass 파일을 invalid 로 덮음 · 요약 중 예외 → invalid 요약 / 진짜 프로세스: `_held` 안에서 부모는 TERM 을 막지만 자식 SigBlk 0x0 · TERM 만으로 그룹이 빈다.
- 깨기가 시험이 못 보던 자리 둘을 드러냈다 (실행 전 기록 목록 · 결정 원장의 같은 열쇠 둘) → 시험을 더했다.

**인터페이스가 바뀐 곳**
- 드라이버: `run_kind_detail` · `MELT_OBSERVED_KEYS` · `VERDICT_SHAPE` · `_verdict_shape_problem` · `_summary_failed` · `_stage1_summary_core` (요약 본체).
- 러너: `_loads_strict` · `_held` · `HELD_SIGNALS` · `_child_restore_mask` · `ack_declaration_problems(…, observed=None)` · `retry_eligibility` 반환에 `observed_melt` · 고정값 `EXPECTED_DRIVER_SHA16 = 0d945e790c7bb8b7` (`EXPECTED_VALUES_SHA16` 그대로).

## 3. 이것을 특히 봐 달라

1. **확인 경로의 닫힘** — 첫 시드의 녹음 fail 을 확인 (--ack_stop) 때 보면 장부에 `closes_system` 을 적고 거부만 한다 (STOP.json 을 덮지 않는다). 다음 시작에서 STOP 을 확인하면 '장부에 계를 닫은 사건' 으로 STOP melt 가 된다. 이 두 단계가 빈틈 없이 닫히는가.
2. **뒤 시드의 복구 fail** — 장부에 적고 멈춘다. 그 시드를 묶음에 fail 로 넣는 것은 사람이 보존 폴더를 되돌려 `--stage1_verdict` 하는 운영 단계다. 이 운영 단계 전 · 중에 다른 우회 (예: 그 시드를 새로 띄움) 가 있는가.
3. **엄격 판독 범위** — 일부러 엄격하게 하지 않은 자리: 옛 li2s1 `melt_check` · 다른 카드 판독 (gb2 · NEB · MC · EOS — li2s-2 경로 밖). 빠진 li2s-2 경로가 있는가.
4. **변이에서 뺀 셋** (하네스 머리글): `persist_observed_melt` 의 저장 끄기 (끝 처리가 어차피 저장) · 시드 루프의 판정 상태 엄격 판독 끄기 (바로 앞 ①-4 가 그 판정을 원자료로 다시 쓴다) · 카드 · gate · seed gate 의 plan 엄격 판독 끄기 (판정이 plan 을 먼저 엄격히 읽는다). 같은 결과라는 판단이 맞는가.
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DO 지적 (P0 · P1-1 · P1-2 · P2-1 · P2-2) · DJ 남은 항목 (Q2 · Q5) 마다 닫힘 여부 한 줄.
