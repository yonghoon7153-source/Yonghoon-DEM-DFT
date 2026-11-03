---
title: "DK 프롬프트 — li2s-2 DJ 고침 확인 (2c36eac9): 재시도 이력 대조 · 판독 불가 · 보존 누락 차단 · 증언 하한 · 잠금 안 증언 · 결과와 무관한 재시도 사유 · MD/FIRE 구분 · 정전 추가 예산 — 첫 담금질 GO 여부"
date: 2026-11-03
updated: 2026-11-03
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DK
track: li2s
channel: codex
kind: prompt
status: 초안 (2026-11-03) — 사용자 발송 대기 · 기준 커밋 2c36eac9
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DJ (0f51518d · NO-GO · P0 3 · P1 1 · Q1–Q4) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `2c36eac9` (브랜치 `claude/friendly-meitner-lldvar`). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DK_reply_li2s2_dj_fixes_2026_11_03.md` 로 원문 보존.

---

**[li2s-2] DJ 고침 확인 — 재승인 최소조건 다섯 (① 재시도 이력 · STOP · 영수증 대조 ② 판독 불가 · 보존 누락 차단 ③ 증언 하한 검증 ④ 잠금 안에서 비용 읽기 · 검사 · 쓰기 ⑤ 결과와 무관한 재시도 사유 · MD/FIRE 구분 사전 명시) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DJ 의 P0 셋 · P1 하나 · Q1–Q4 를 고쳤다 (결과 0 건). **지적마다 닫혔는가 (GO / 조건부 GO / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DJ 가 해제로 본 DI 지적 (P0-1 · P0-2 · P0-3 · P1-4 · P1-5 기존 경로) 은 다시 열지 않아도 된다.

**가능하면 DJ 때의 재현 (`probe_results.json` · `probe_finish.json` 의 시나리오) 을 이 커밋에 다시 돌려 달라.** 인터페이스가 바뀐 곳은 §2 끝.

## 1. 보는 범위

- `git diff 0f51518d 2c36eac9 -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_정전_복구_v2_2026_11_03` · 기계값 `retry_reasons` · `outage_reasons` · `cap_retry_reasons` · `stage1_outage_extra_budget_gpu_h` (45) · `attestation_required_fields`
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 207) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 76 · Linux)
- 깨기 (변이) __MUT__ — 저장소 밖 복사본에서 DG · DH · DI · 정전 복구 · DJ 고친 곳을 하나씩 되돌려 해당 시험이 빨개지는지

## 2. DJ 지적별로 한 것 (재현 → 지금 막는 시험)

**P0-1 재시도 필드가 빠지면 소비자 한도 검사가 꺼짐** — 소비자 `ledger_check` 가 같은 계 · 시드의 실행을 장부 순서로 보고 **두 번째 실행부터**:
- `retry_of` = 바로 앞 실행의 run_id (없으면 무효 — '있을 때만 검사' 를 없앴다)
- `retry_kind` = 앞 실행의 종류 (앞 실행 판정이 invalid 면 invalid · 아니면 interrupted — 필드가 아니라 앞 실행에서 정한다)
- `retry_stop_id` → `stop_history` 의 그 STOP 이 **확인됐고 · 앞 실행 run_id 에 묶였고 · code 가 그 종류의 묶는 code** 이고 · 그 확인에 붙은 **재시도 선언** 이 맞아야 (Q1)
- 그 실행 폴더의 `stage1_attempt.json` 재시도 필드 = 장부 (실행 전 기록이 없으면 무효)
- 끊긴 런 재시도 수는 **앞 실행 종류로** 센다 — 필드를 지워도 줄지 않는다 · 첫 실행에 재시도 필드가 있으면 무효
- 시험 (모든 면에서 맞는 이력을 만든 양성 대조 → 한 가지씩만 깸): 양성 대조 통과 / 장부 재시도 필드 + STOP 이력 지움 → 무효 / 실행 전 기록까지 맞춰 지움 → 무효 / 두 번 재시도 → 한도 / **그 두 번 재시도에서 retry_kind 만 지움 → 여전히 한도** / 기록 ≠ 장부 · 기록 없음 · 선언 없음 · 다른 런에 묶임 → 무효 / **지운 자료를 러너에 다시 줌 → rc 27 (invalid) · 발사 0** (DJ: rc 0)

**P0-2 판독 불가 · 보존 누락에도 재시도** —
- `verdict_file_status`: 판정 파일 **없음 (None)** 과 **있는데 못 읽음 · 모르는 상태 · 객체 아님 (`unreadable`)** 을 가른다 → 러너 재시도 자격 · 소비자 둘 다 못 읽음을 차단 ('판정 없음' 으로 읽지 않는다)
- 러너 `retry_eligibility` 가 **invalid 런을 포함한 모든 이전 실행** 에 보존 폴더 (같은 계 폴더 안 · 실행 전 기록의 run_id) · 폴더 판정 · 비용 · 완료 단계를 본다 (invalid 분기의 조기 continue 를 없앴다)
- 소비자에 **장부 → 보존 폴더** 방향 (장부 런의 폴더가 run_root 의 계 폴더 안에 없으면 무효 · '보존 누락')
- MD 까지 (또는 끝까지) 돈 invalid 런은 재시도 선언에 **'있는 파일을 고쳐 다시 판정할 수 없는 이유'** (`--rejudge_impossible_reason`) 가 있어야 영수증이 된다 (확인 때 바로 검사)
- 시험: DJ 재현 그대로 — 끊긴 B12 보존 폴더 판정 JSON 잘림 + 정전 선언 확인 → 러너 rc 27 · 발사 0 · 소비자 무효 / 기술적 invalid A11 폴더를 run_root 밖으로 + 원인 고침 선언 확인 → rc 27 (묶음 '보존 누락') · 발사 0 / final.xyz 5 원자 invalid 런 → 이유 없는 선언은 확인 거부 (STOP 그대로) · 이유를 적으면 다시 돌아 1 단계 통과

**P0-3 하한 미상 · NaN · 음수면 0 h 증언을 확정 비용으로** —
- `--attest_cost` 는 하한 (`wall_h_lower`) 과 heartbeat (`wall_h_so_far`) 가 **유한한 비음수 · 하한 ≥ heartbeat** 일 때만 받는다 — 아니면 **하한 미상 → 증언을 받지 않고 비용은 미확정 그대로** (`dict.get(key, fallback)` 대체 경로를 없앴다) · H 는 유한 · **양수** · 하한 이상
- 증언 기록에 그때의 하한 · heartbeat (`lower_at_attest` · `heartbeat_at_attest`) 를 남기고 · 소비자가 장부와 대조 · 하한 검사를 생략하는 길 (`_fin(lo)` 일 때만) 을 없앴다 · 증언 상한은 **고아 런 (orphaned)** 에만
- 시험: DJ 재현 그대로 — 하한 null · NaN · −1 (heartbeat 5) 에 0 h · 6 h → 둘 다 거부 · 장부 바이트 그대로 / heartbeat 미만 하한 (4 < 5) → 거부 / 하한 0 (첫 heartbeat 전 끊김) 에 0 h → 거부 · 0.5 h → 받음 / 소비자: 그 셋에 0 h 증언 행 → 무효 · 정상 끝 행을 증언 상한으로 바꿈 → 무효 · 양성 대조 (하한 5 · 상한 6 · 고아 런) 통과

**P1-4 증언이 잠금 전에 읽은 장부로 덮어씀** — 쓰는 경로는 **잠금을 먼저 잡고 · 그 안에서 장부를 다시 읽어 · 자격 검사부터 저장까지** 한다 · 이미 증언 · 확정된 런이면 두 번째 쓰기 거부 (근거 보기 — hours 없음 — 는 읽기만 · 쓰지 않음).
- 시험: DJ 재현 순서 그대로 — 잠금 전에 다른 기록자가 8 h 증언 + STOP 확인을 저장 → 우리 호출 (2 h) 거부 · 장부는 8 h · 확인 그대로 / 잠금이 잡혀 있으면 아무것도 안 씀 / 두 번째 증언 거부

**Q1 결과와 무관한 재시도 사유** — 카드 `retry_reasons`: 끊긴 런 = `power_outage` · `host_crash_or_reboot` · `hardware_fault` · `budget_cap_raised` / invalid 런 = `invalid_cause_fixed`. 확인 (`--ack_stop`) 때 선언을 붙인다: `--retry_reason` · `--retry_event` · `--retry_evidence` · `--declared_by` (+ `--rejudge_impossible_reason`) · 선언 시각 자동 · 확인 때 바로 검사 (허용 밖 사유 · 빈 칸 · 그 code 가 영수증이 될 종류 · 상한 규칙 · 다시 판정 못 하는 이유) → 어기면 확인 자체를 거부 (STOP 그대로).
- Ctrl-C · abnormal · resume 는 기술 상태일 뿐 사유가 아니다 — **선언 없는 확인은 영수증이 아니다** (러너가 '선언이 맞는 확인이 없다' 로 그 run_id 에 묶인 STOP 을 다시 낸다).
- 결과를 보고 멈춘 런 · 원인 미확정 런은 맞는 사유를 선언할 수 없으므로 자동 대체되지 않는다 (보류 · 새 결정).
- 채택 순서: 재시도한 실행이 그 시드의 공식 표본 — 앞 실행은 판정이 없거나 invalid 라 '둘 중 좋은 것' 을 고를 일이 없다 (과학적 판정이 난 시드는 다시 안 돌린다 · DI 그대로).
- 시험: 선언 없는 확인 → 멈춤 (rc 24 · 발사 0) / Ctrl-C 사유 · 상한 아닌 런에 상한 사유 · 선언자 빈칸 → 확인 거부 (rc 10 · STOP 그대로) / 정전 선언 확인 → 한 번 다시 · 영수증 · 실행 전 기록 · 장부 일치 · 통과

**Q2 MD 완료 · FIRE 미완 구분** — `folder_stage`: `final` (result.json · final.xyz) · `md_complete` (traj 가 계획 프레임까지 · final 없음) · `md_incomplete` · `no_plan` · `unreadable` (plan · traj 머리를 못 읽음 · 끝의 반쪽 프레임은 안 셈 · 빈 / NUL 만 있는 traj = 프레임 0).
- 끊긴 런: MD 미완 → 사유가 맞으면 재담금질 1 회 / **MD 완료 · FIRE 미완 → 재담금질하지 않고 보류** (그 마지막 구조에서 정해진 FIRE 만 다시 하는 복구는 새 결정) / 최종 → 재시도가 아니라 판정 / 판독 불가 → 보류
- 프레임 수는 드라이버와 **같은 스텝 셈** (단계마다 반올림한 스텝 수 · save 간격 → N // save_int + 1 · 끝 record 포함 · plan 의 dt_fs 필요 — 없으면 판독 불가 = 보류) — 발송 전 자체 점검에서 고쳤다 (2c36eac9): 처음엔 round(총 ps / save_ps) + 1 이라 save 간격이 나누어떨어지지 않으면 끝난 MD 를 미완으로 읽어 재담금질 길이 열렸다
- 시험: MD 완료 · FIRE 미완 폴더 + 맞는 선언 → 러너 보류 (rc 24 · 'FIRE') / 소비자: MD 완료 · 최종 뒤 재담금질 → 무효 / 드라이버 단위: save 0.7 ps 에서 6 프레임 = MD 완료 · 5 = 미완 · dt 없는 plan = 판독 불가

**Q3 증언 필드** — 카드 `attestation_required_fields` = 사건 (`--attest_event`) · 시각 기준 (`--attest_time_reference`) · 불확실성 h (`--attest_uncertainty_h` · 유한 비음수) · H 산출 방식 (`--attest_derivation`) · 확인자 (`--attest_confirmer`) · 확인 시각 (자동) + OS 사용자 · 호스트 (기록용 — 확인자 신원 증명은 아니다). 고정 문구 `by` 를 없앴다. 소비자가 필드 · 하한 대조를 다시 본다.
- 시험: 필드 다섯 중 하나라도 없거나 불확실성 NaN → 거부 (비용 미확정 그대로)

**Q4 cap 재시도 조건 · 정전 추가 예산** —
- 실효 상한 = 카드 `stage1_cap_gpu_h` (230) + min(정전 손실, 카드 `stage1_outage_extra_budget_gpu_h` (45)) · 정전 손실 = 정전 사유 (`outage_reasons`) 로 선언된 **도중에 끊긴** 런 (판정 없음 · interrupted · orphaned · rc ≠ 0) 중 폴더가 MD 미완인 것의 확정 비용. 45 = 최악의 끊긴 런 둘 (시드당 견적 상단 21 h × 2) + 여유. 러너의 확인 · 사전 · 실행 중 · 사후 상한 검사와 소비자가 같은 값을 쓴다.
- 상한으로 멈춘 런 (장부 상태 cap) 의 재시도 사유는 `cap_retry_reasons` (= `budget_cap_raised`) 뿐 · 그 사유는 상한 런에만 — 정전 사유로 상한을 늘리는 길을 막았다 · 상한 멈춤 확인은 실효 상한이 올라가야 (카드 개정 = 결정) · 같은 재시도 횟수 · 완료 단계 규칙 · 기존 비용 · 실패 · 시드 목록은 그대로.
- 시험: 카드 상한 50.5 h · B12 가 정전으로 2 h 손실 → 실효 52.5 h — 러너가 마지막 시드까지 띄우고 (누적 52 h) 묶음 통과 · 추가 예산 0 이면 소비자 상한 50.5 / 상한 런에 정전 사유 → 소비자 무효 · 러너 거부 / 드라이버 단위: 정상 끝 · 상한 런 · 확인 안 된 선언 · MD 완료 폴더는 손실로 안 셈

**Q5 값이 없으면 검사가 약해지는 자리** — 재시도 한도 (`int(values[...])` — 카드 검사가 0 이상 정수를 보장 · 없으면 멈춤) · 실효 상한의 카드 값 (`values[...]` 필수) · 하한 (위 P0-3) · 첫 실행 이외의 재시도 필드 (위 P0-1).

**인터페이스가 바뀐 곳**: 드라이버 `RETRY_BIND_CODES` · `folder_stage` · `verdict_file_status` · `declaration_problems(decl, kind, values, rejudge_needed, prev_status)` · `effective_cap(runs, stop_history, values, inventory)` · `attempt_inventory` 원소에 `attempt` (재시도 필드) · `ledger_check` 반환 `cap_h` = 실효 상한 + `cap_info` · 카드 검사가 새 기계값 다섯을 본다 / 러너 `retry_eligibility(attempts, stop_history, inventory, values, mq)` · `declaration_from_args` · `ack_declaration_problems` · `attest_cost(run_root, run_id, values, hours, fields, deps)` · CLI `--retry_reason` · `--retry_event` · `--retry_evidence` · `--declared_by` · `--rejudge_impossible_reason` · `--attest_event` · `--attest_time_reference` · `--attest_uncertainty_h` · `--attest_derivation` · `--attest_confirmer` (`--attest_note` 없앰) · 러너 고정 드라이버 sha16 `9bb45bdda464b23e`.

## 3. 이것을 특히 봐 달라

1. **영수증 검사 위치** — 선언은 확인 때 (러너) · 재시도 직전 (러너 `retry_eligibility`) · 묶음 (소비자) 세 곳에서 같은 함수 (`declaration_problems`) 로 본다. 확인 때 검사의 '다시 판정 못 하는 이유' 판단은 그 run_id 의 폴더를 실행 목록 (`attempt_inventory`) 에서 찾아 완료 단계를 잰다 — 폴더를 못 찾으면 (아직 옮기기 전 · 밖으로 옮김) 그 요구를 못 건다 (뒤 두 곳이 다시 막는다). 이 순서가 맞는가.
2. **정전 손실 산정** — '정전 사유로 선언됐고 도중에 끊겼고 MD 미완' 이면 그 런 비용 전부를 손실로 센다 (상한 45 h). 사람이 정전이 아닌 끊김을 정전으로 선언하면 예산이 최대 45 h 늘어난다 — 선언 (사건 · 근거 · 선언자) 이 감사 기록으로 충분한가, 더 필요한가 (예: 사건 시각과 장부 last_seen 대조).
3. **MD 완료 판정** — 계획 프레임 수 = (단계별 반올림 스텝 합) // save_int + 1 (드라이버 `run_melt_quench` 의 `record` — 끝 `record(T_final)` 은 총 스텝이 save 간격의 배수일 때만 쓰인다 — 와 같은 셈이라고 읽었다) · 끝의 반쪽 프레임은 안 센다. 이 셈이 실제 드라이버 출력과 맞는가.
4. **잠금과 러너** — 증언은 러너와 같은 flock 을 잡는다 (러너가 돌면 증언 거부). 러너 밖에서 사람이 장부를 손으로 고치는 것은 못 막는다 (도구 한계로 적음).
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DJ 지적 (P0-1 · P0-2 · P0-3 · P1-4 · Q1–Q5) 마다 닫힘 여부 한 줄.
