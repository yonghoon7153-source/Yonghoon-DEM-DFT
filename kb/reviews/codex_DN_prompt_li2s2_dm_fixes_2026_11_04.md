---
title: "DN 프롬프트 — li2s-2 DM 고침 확인 (acc648b0): thermo 꼬리의 시각 · 판정 기록을 내용으로 (plan 전 끊김 · 도중 끊김 후보) — 첫 담금질 GO 여부"
date: 2026-11-04
updated: 2026-11-04
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DN
track: li2s
channel: codex
kind: prompt
status: 발송 · 회신 수령 2026-11-04 (NO-GO · P1 1 · P2 1 · `codex_DN_reply_li2s2_dm_fixes_2026_11_04.md`) · 기준 커밋 acc648b0 (깨기 165/165)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DM (04555774 · NO-GO · P0 2) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `acc648b0` (브랜치 `claude/friendly-meitner-lldvar` · 기록까지 들어간 커밋). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DN_reply_li2s2_dm_fixes_2026_11_04.md` 로 원문 보존.

---

**[li2s-2] DM 고침 확인 — 재승인 조건 (두 반례의 러너 · 소비자 차단 · 정상 plan 전 끊김과 명확한 도중 끊김은 여전히 허용되는 대조) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DM 의 P0 둘을 고쳤다 (결과 0 건). 같은 갈래로 하나를 더 막았다 (§2 끝). **지적마다 닫혔는가 (GO / 조건부 GO / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DM 이 해제로 본 항목 (DL P1-1 저장 순서 · DL P1-2 FIRE 순서 시험 · DL P0 기존 두 반례 · Q3 · Q4) 은 다시 열지 않아도 된다.

**가능하면 DM 때의 재현 (`probe_results.json` 의 세 상태 — 끝 시각 행이 남은 thermo · pass 판정이 있던 폴더의 재판정 · 임시 파일에만 남은 pass 판정) 과 대조 (정상 plan 전 끊김 · 명확한 도중 끊김) 를 이 커밋에 다시 돌려 달라.** 인터페이스가 바뀐 곳은 §2 끝.

## 1. 보는 범위

- `git diff 04555774 acc648b0 -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_완료_기록_v5_2026_11_04` (결과 0 건 · 카드 값은 안 바뀜)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 211) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 83 · Linux)
- 깨기 (변이) **165 / 165 빨강** — 저장소 밖 복사본에서 DG · DH · DI · 정전 복구 · DJ · DK · DL · DM 고친 곳을 하나씩 되돌려 해당 시험이 빨개지는지. DL 판 147 개 중 thermo 판독을 다시 써서 자리가 바뀐 4 개 (N3 · N6 · N8 · N9) 는 새 자리로 옮겼고, DM 자리 13 개 (`O1_tail_time_mismatch_ok` ~ `O13_history_new_part_off`) 와 같은 갈래 자리 5 개 (`O14_mid_status_check_off` ~ `O18_invalid_held`) 를 더했다 (165 · 앞 번호가 정전 복구 판의 O6 · O9–O13 과 겹쳐 전체 이름으로 가른다). 본 판은 빨강 163 · **초록 2 = 시험 구멍** — `N18_header_check_off` (머리 없는 thermo fixture 를 새 꼬리 시각 규칙이 대신 잡아 머리 검사를 안 봤다) · `O12_mid_pass_fail_off` (같은 갈래의 상태 화이트리스트가 pass 도 잡아 결과 단계가 같았다) → 시험 둘을 더했고 (머리 이름이 다른 thermo · pass 이력의 보류 이유 문구) 둘 다 다시 빨강. `db/raw/li2s2_dm_mutation_2026_11_04/` (README)

## 2. DM 지적별로 한 것

**P0-1 — thermo 마지막 줄 (꼬리) 의 시각.** `_thermo_last_step` 이 꼬리를 '덜 써진 행' 과 '온전하지만 순서가 다른 행' 으로 가른다:
- 첫 칸 (시각) 이 다 써졌다 (쉼표가 있다) → 그 시각이 다음 기록 시각 (k · 저장 간격) 과 같을 때만 시작된 기록으로 센다 · **다르면 보류** (그 줄의 시각이 끝 시각일 수 있다 — 버리지 않는다). DM 반례 (온전한 0 · 1 · 129 ps 행 · 궤적 앞부분 · 완료 기록 없음) → 보류.
- 첫 칸이 쓰이다 말았다 (쉼표 없음) → 다음 기록 시각 문자열 (드라이버가 쓰는 꼴 `%.3f`) 의 앞부분일 때만 센다 · 아니면 보류 (예: 다음이 `2.000` 인데 `1.0` → 보류).
- NUL 뒤에 다른 글자가 있다 · 꼬리가 앞 줄과 이어지지 않는다 → 보류.
- 정전 꼬리 (NUL 덩어리만 · 앞부분이 맞는 덜 써진 첫 칸) 는 전처럼 시작된 기록으로 센다. 꼬리가 아닌 자리의 깨짐은 전과 같이 보류.

**P0-2 — 판정 기록은 이름이 아니라 내용으로.** `_verdict_is_pre_run` · `_verdict_records` · `_verdict_evidence` (새 함수) 를 `folder_stage_detail` 이 쓴다:
- **no_plan 후보** (plan 없음 · `NON_MD_FILES` 밖 파일 없음): 현재 판정 · 이력의 이전 판정이 모두 plan 전 판정 꼴 (status `incomplete` · 이유 incomplete = `["plan.json 없음"]` 하나 · 원자료 지문 `PROVENANCE_FILES` 가 다 있고 다 None) · 이력의 새 판정은 상태 incomplete + 지문 전부 None 이어야 no_plan · 아니면 보류.
- **판정 임시 파일** (`stage1_verdict.json.tmp`) 이 남았거나 판정 · 이력을 못 읽으면 보류 (no_plan · 도중 끊김 후보 둘 다).
- **도중 끊김 후보** (plan 있음 · 진행 기록이 끝 경계 앞): 어느 판정 기록에 과학적 판정 (pass · fail) · 최종 산출물 (final.xyz · result.json) 지문이 있으면 보류.
- DM 반례 1 (pass 판정이 있던 폴더에서 원자료 소실 뒤 진짜 `stage1_verdict` 로 재판정 · 이력에 이전 pass · final.xyz 지문) → 보류 · 반례 2 (pass 판정이 `.tmp` 에만) → 보류.

**같은 갈래로 더 막은 것 (DM 이 재현하지 않은 것 · 3d97d145).** DM 최소 수정 문구 ('완료 흔적이나 해석할 수 없는 기록이 있으면 보류') 를 도중 끊김 후보에도 그대로 적용했다. 도중 끊김 후보의 판정 기록이 아래면 보류:
- 상태를 해석할 수 없다 — **못 읽은 이전 판정** (이전 판정 파일이 깨진 채 재판정하면 이력에 status None + raw_text 로 남는다 · raw_text 안에 pass 가 있을 수 있다) · 모르는 상태.
- **MD 완료 흔적** (전체 기록 — 현재 판정 · 이력의 이전 판정): gate_check `schedule_complete` · `checks.traj_frames` n ≥ 계획. MD 가 끝나고 FIRE 만 못 마친 폴더의 판정은 `incomplete` (final.xyz 없음) 인데 이 둘을 담는다 → 그 뒤 완료 기록 · 꼬리가 사라지면 진행 기록만으로는 도중 끊김으로 보였다.
- `invalid` 는 막지 않는다 — 과학적 판정이 아니고, 원인을 고친 재시도 경로 (선언 `invalid_cause_fixed` · 다시 판정 못 하는 이유) 가 따로 있다. invalid 판정에 위 흔적이 있으면 보류.

**시험** (드라이버 단위 · 러너 발사 · 재시도 자격 단위 · 소비자):
- P0-1: 끝 시각 행 · 마지막 행 시각 틀림 · 앞부분이 아닌 조각 · NUL 뒤 글자 · 이어지지 않는 꼬리 → 보류 / 앞부분이 맞는 조각 · NUL 꼬리 → 미완 (대조).
- P0-2: pass 이력 재판정 · 임시 판정 · 지문 없는 `{"status": "incomplete"}` 한 줄 · 다른 이유의 incomplete · 원자료 지문이 남은 plan 전 꼴 · 깨진 이력 · 이력의 새 판정 pass → 보류 / 진짜 판정 함수로 한 번 · 두 번 판정한 plan 전 끊김 → no_plan (대조).
- 같은 갈래: 못 읽은 이전 판정 · 모르는 상태 · 일정 끝 · 프레임 다 참 → 보류 / invalid 만 · 일정 미완이 적힌 incomplete → 미완 (대조). 러너 쪽은 **진짜 판정 함수**로 만들었다 — MD 완료 · FIRE 미완 폴더를 seed 이름 아래에서 판정 (incomplete · 일정 끝 · 프레임 다 참 · 이 꼴인지 fixture 뜻도 시험한다) → 보존 → 완료 기록 · 꼬리 소실.
- 러너 발사 시험 (보존 폴더 · 진짜 판독 함수): DM 세 반례 + 같은 갈래 → 선언이 맞아도 재담금질 0 · 보류 rc 24 · 폴더 파일 해시 그대로 / 대조 둘 (진짜 판정 함수로 두 번 판정한 plan 전 끊김 · 명확한 도중 끊김) → 재시도 1 · rc 0.
- 재시도 자격 단위 · 소비자 (`--stage1_summary` 이력 검사): 반례 → 보류 · 재시도 무효 / 대조 (plan 전 판정만) → 재시도 · stage1_pass.
- 고치면서 드러난 시험 쪽 결함 넷 (고침 · 뒤 둘은 깨기가 드러냄 — §1): ① 대조 'plan 전 끊김 판정' 을 처음에 pass 였던 폴더에서 만들어 이력에 pass 가 남았다 (새 판독이 보류로 잡았다) → 실행 전 기록만 남긴 폴더로 · ② 새 fixture 검사가 why = None 일 때 TypeError 로 죽었다 (변이 O17 에서 보임 · 빨강은 맞았지만 깔끔하지 않음) → None 안전 · ③ 머리 없는 thermo fixture 만 있어 머리 검사가 따로 안 시험됐다 → 머리 이름이 다른 thermo · ④ pass 이력 보류를 단계로만 봐서 pass 전용 검사가 따로 안 시험됐다 → 보류 이유 문구.

**인터페이스가 바뀐 곳**:
- 드라이버: `_thermo_last_step` 꼬리 규칙 · `_verdict_is_pre_run` · `_verdict_records` · `_verdict_evidence(folder, pre_run_only)` (새) · `folder_stage_detail` 이 판정 기록을 본다 (no_plan · 도중 끊김 둘 다) · 이유 문구
- 러너: 고정 드라이버 sha16 `c2744b7927da30cf` · selftest 가 예외로 끝나도 임시 폴더를 지운다 (2d1c3a7b — 변이 실행 중 450 MB × 105 개로 디스크가 찼다)

## 3. 이것을 특히 봐 달라

1. **꼬리 규칙의 경계** — '첫 칸이 다 써졌는가' 를 쉼표로 가른다. 덜 써진 첫 칸이 다음 시각과 끝 시각의 공통 앞부분이면 (예: `12` ↔ 다음 `12.000` · 끝 `129.000`) 다음 기록으로 센다 — 정상 꼬리의 꼴이고 끝 시각이 읽히지 않아서다. 이게 '완료 시각이 남아 있는데 버린다' 에 해당하는가.
2. **traj 프레임에는 시각이 없다** — 프레임 수만 센다. 온전하지만 순서가 다른 프레임 (앞 · 끝) 은 thermo 시각으로만 가른다 (thermo 가 없거나 앞부분만이면 못 가른다 · 카드 v5 '못 하는 것'). thermo · traj 의 기록 수가 서로 크게 다를 때 보류하는 검사를 더할 만한가 — 정전 때 두 파일이 다른 양의 꼬리를 잃을 수 있어 문턱을 정하기 어렵다고 봤다.
3. **판정 기록 허용 범위** — no_plan 은 '모든 기록이 plan 전 판정 꼴' (화이트리스트) · 도중 끊김 후보는 'incomplete · invalid 이고 완료 흔적이 없음'. 완료 흔적을 일정 끝 · 프레임 다 참 · 최종 지문으로 잡았다 — 빠진 흔적이 있는가.
4. **이력이 통째로 지워진 폴더** — 없는 기록은 못 읽는다 (docstring · 카드에 적은 한계). 받아들일 만한가.
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DM 지적 (P0-1 · P0-2) 과 DJ 남은 항목 (Q2 · Q5) 마다 닫힘 여부 한 줄.
