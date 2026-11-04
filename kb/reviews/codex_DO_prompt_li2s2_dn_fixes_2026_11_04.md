---
title: "DO 프롬프트 — li2s-2 DN 고침 확인 (__BASE__): 판정 기록의 완료 판단 필드 — 타입 오류 = 해석할 수 없는 기록 (보류) · NUL 꼬리 문구 — 첫 담금질 GO 여부"
date: 2026-11-04
updated: 2026-11-04
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DO
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

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DN (acc648b0 · NO-GO · DM P0 두 건 해제 · P1 1 · P2 1) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `__BASE__` (브랜치 `claude/friendly-meitner-lldvar` · 기록까지 들어간 커밋). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DO_reply_li2s2_dn_fixes_2026_11_04.md` 로 원문 보존.

---

**[li2s-2] DN 고침 확인 — 재승인 조건 (완료 필드 타입 오류의 러너 · 소비자 차단 · 정상 incomplete · invalid 대조군 유지) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DN 의 P1 · P2 를 고쳤다 (결과 0 건). **지적마다 닫혔는가 (GO / 조건부 GO / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DN 이 해제로 본 항목 (DM P0-1 · P0-2 · 정상 중단 대조 · 같은 갈래의 정상 타입 완료 흔적 · Q1–Q4 판단) 은 다시 열지 않아도 된다.

**가능하면 DN 때의 재현 (`probe_results.json` — thermo 없음 · 궤적 완주 · FIRE 미완을 진짜 판정한 뒤 완료 기록 · 궤적 꼬리 소실 · n:130 → n:"130") 과 대조 (정상 incomplete · invalid) 를 이 커밋에 다시 돌려 달라.**

## 1. 보는 범위

- `git diff acc648b0 __BASE__ -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_완료_기록_v6_2026_11_04` (결과 0 건 · 카드 값은 안 바뀜)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 212) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 83 · Linux)
- 깨기 (변이) **__MUT__** — DM 판 165 개를 가져오되 plan 전 판정 이유 검사를 다시 써서 자리가 바뀐 `O9_prerun_reasons_off` 를 새 자리로 옮기고, DN 자리 9 개 (`DN1_completion_fields_off` ~ `DN9_n_not_checked`) 를 더했다 (174 · 전체 이름이 모두 다르다). `db/raw/li2s2_dn_mutation_2026_11_04/`

## 2. DN 지적별로 한 것

**P1 — 완료 판단 필드의 타입 오류 = 해석할 수 없는 기록 (보류).** 새 함수 `_completion_fields_problem(r, partial, where)` 를 `_verdict_evidence` 의 도중 끊김 후보 갈래가 상태 검사 바로 뒤에 부른다:
- 필드가 **없거나 None** 이면 허용 (그 흔적이 없다) · **있는데 타입이 틀리면** 보류 — 정수로 바꿔 읽지 않는다 (n:"130" 은 130 이 아니라 못 읽는 값).
- 기대하는 꼴: `provenance` · `files_sha256` = 객체 · `final.xyz` · `result.json` 지문 = 64 자리 16진수 글자 (빈 글자 · 다른 글자 = 보류 · 맞는 지문은 전처럼 '최종 산출물 지문' 으로 보류).
- 전체 기록 (현재 판정 · 이력의 이전 판정) 만: `gate_check` · `checks` · `traj_frames` = 객체 · `schedule_complete` = 참거짓 · `n` · `expected` = 정수 (참거짓은 정수 자리에서 타입 오류) · `n ≥ 0` · `expected ≥ 1`.
- 이력의 새 판정 지문 (`new_provenance`) 은 **쓰인 그대로** 넘긴다 — 전에는 객체가 아니면 None 으로 바꿨다 (타입 오류를 없는 값으로 만들던 자리).
- plan 전 판정 (`_verdict_is_pre_run`) 의 이유는 **정확히** `{"incomplete": ["plan.json 없음"]}` 이어야 한다 — 전에는 다른 열쇠의 빈 값 (`"fail": ""` 등) 을 받아 줬다.

**시험** (드라이버 단위 · 러너 발사 · 재시도 자격 단위 · 소비자):
- 드라이버 fixture 14 — 보류: 이력의 이전 판정 n:"5" · expected:"5" · n:True · expected 0 · schedule_complete:"true" · gate_check 글자 · checks 목록 · traj_frames 정수 · provenance 글자 · files_sha256 글자 · final.xyz 빈 지문 · 이력의 새 판정 지문 글자 · plan 전 판정 이유에 `"fail": ""` / 대조: gate_check None · n · expected None → 미완 (재시도). 보류 이유 문구도 본다 ('n 타입이 str' · '말이 안 된다' · '64 자리 16진수' 등 — 다른 갈래의 보류와 구별).
- 러너 = **DN 재현 그대로** — 보존된 MD 완료 · FIRE 미완 폴더에서 thermo 를 지우고 seed 이름 아래에서 **진짜 판정** (incomplete · 일정 없음 · 프레임 다 참 — 이 꼴인지 fixture 뜻도 시험한다) → 완료 기록 · 궤적 꼬리 소실 → ① n 정수 그대로 · ② n 만 글자로. 둘 다 선언이 맞아도 재담금질 0 · 보류 rc 24 · 폴더 파일 해시 그대로.
- 재시도 자격 단위 · 소비자 (`--stage1_summary` 이력 검사): n 이 글자인 같은 폴더 → 보류 · 재시도 무효 (이유에 'n 타입이 str').
- 대조 유지: 정상 incomplete · invalid 판정 · 일정 미완 판정 · 진짜 판정 함수로 두 번 판정한 plan 전 끊김 · 명확한 도중 끊김 → 재시도 1 · rc 0 (DM · DN 때와 같은 시험).

**P2 — NUL 꼬리 문구.** 구현은 그대로다. 문구를 맞췄다 (docstring `_junk` · `md_last_recorded_step` · 드라이버 시험 문구 · 카드 v6 — v4 · v5 의 'NUL 덩어리도 센다' 를 고친다고 적었다): **시각의 유효한 앞부분이 남은 꼬리는 센다 (예 `12\0\0` → 12 ps). NUL 만 남은 꼬리는 건너뛰어 진행량을 복원하지 못한다** (예 0–11 ps 뒤 NUL 만 → 11 ps · 이미 받아들인 손실 한계).

**Q2 · Q4 판단을 한계로 적었다** (docstring · 카드 v6): 두 파일 중 큰 값은 보수적 판독이지 완전성 증명이 아니다 · 이력이 통째로 없는 폴더를 '과거 완료가 없었다' 의 증명으로 쓰지 않는다.

**인터페이스가 바뀐 곳**:
- 드라이버: `_completion_fields_problem` (새) · `_verdict_evidence` 가 부른다 · `_verdict_records` 의 새 판정 지문을 그대로 · `_verdict_is_pre_run` 이유 정확히 같음 · 이유 문구
- 러너: 고정 드라이버 sha16 `ebaff2f3d2237ac8`

## 3. 이것을 특히 봐 달라

1. **꼴 검사의 범위** — 완료 판단에 쓰는 필드만 본다 (위 목록). 판정 기록의 다른 필드 (`reasons` · `run_id` · `melt_window_check` · 카드 · 도구 지문) 는 도중 끊김 판단에 안 쓰여 꼴을 안 본다. 완료 판단에 쓰이는데 빠진 필드가 있는가.
2. **지문 자리 규칙** — 도중 끊김 후보에서 `final.xyz` · `result.json` 지문 자리에 None 이 아닌 값이 있으면 형식이 맞든 틀리든 보류다. 넘친 보류로 볼 경우가 있는가.
3. **값 범위** (`n ≥ 0` · `expected ≥ 1`) 를 타입 오류와 같이 '해석할 수 없는 기록' 으로 본다 — 진짜 판정 함수는 프레임을 못 세면 None 을 쓴다 (`_xyz_frames`). 받아들일 만한가.
4. **plan 전 판정 이유 '정확히 같음'** — 진짜 판정 함수가 plan.json 없는 폴더에 쓰는 꼴이 그것뿐이라서 좁혔다 (selftest 대조: 진짜 함수로 두 번 판정한 폴더는 그대로 no_plan).
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DN 지적 (P1 · P2) 과 DJ 남은 항목 (Q2 · Q5) 마다 닫힘 여부 한 줄.
