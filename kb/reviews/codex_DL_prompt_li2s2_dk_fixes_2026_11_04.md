---
title: "DL 프롬프트 — li2s-2 DK 고침 확인 (__BASE__): MD 완료 기록 (프레임 셈 대신) · 실행 상태 한 곳 · 정전 추가 예산 없앰 · 증언 양수 — 첫 담금질 GO 여부"
date: 2026-11-04
updated: 2026-11-04
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DL
track: li2s
channel: codex
kind: prompt
status: 초안 (2026-11-04) — 사용자 발송 대기 · 기준 커밋 __BASE__
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DK (7ac0be8e · NO-GO · P0 2 · P1 2) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `__BASE__` (브랜치 `claude/friendly-meitner-lldvar` · **기록까지 들어간 커밋** — DK 때 runlog 가 한 커밋 뒤처졌던 것을 고침). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DL_reply_li2s2_dk_fixes_2026_11_04.md` 로 원문 보존.

---

**[li2s-2] DK 고침 확인 — 재승인 핵심 둘 (손상된 완료 궤적을 재담금질 대상으로 내리지 않는다 · 폴더와 장부의 같은 판정이 같은 답을 낸다) + 0 h 소비자 검사가 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DK 의 P0 둘 · P1 둘을 고쳤다 (결과 0 건). **지적마다 닫혔는가 (GO / 조건부 GO / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DK 가 해제로 본 DJ 항목 (P0-1 · P0-2 기존 반례 · P1-4 · Q1 · Q3 필드) 은 다시 열지 않아도 된다.

**가능하면 DK 때의 재현 (`probe_results.json` 의 시나리오) 을 이 커밋에 다시 돌려 달라.** 인터페이스가 바뀐 곳은 §2 끝.

## 1. 보는 범위

- `git diff 7ac0be8e __BASE__ -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_정전_복구_v3_2026_11_04` (결과 0 건)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 207) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 80 · Linux)
- 깨기 (변이) __MUT__

## 2. DK 지적별로 한 것

**P0-1 손상된 궤적이 md_incomplete → 재담금질 · 정전 예산** · **P1-1 프레임 수는 MD 완료를 증명하지 않음** — 둘을 같이 고쳤다: **MD 완료의 증거를 프레임 수에서 완료 기록으로 바꿨다.**
- 드라이버 `run_melt_quench` 가 MD 루프가 끝난 **직후 (FIRE 전)** `md_done.json` 을 원자적으로 쓴다 — `run_id` · 계획 스텝 · 실제 스텝 · `traj.xyz` · `thermo.csv` sha256 (`write_md_done`).
- `folder_stage` 는 프레임을 세지 않는다:
  - `final`: result.json · final.xyz 가 있음
  - `md_complete`: 기록이 맞음. run_id = plan · 계획 = 실제 = plan 일정의 스텝 (`planned_md_steps`) · 두 해시 일치 → FIRE 미완 = 보류
  - `md_incomplete`: plan 은 있는데 기록이 없음 (궤적 상태와 무관) → 사유가 맞으면 재담금질 1 회
  - `unreadable`: 기록을 못 읽음 · plan 과 다름 · 스텝 모자람 · plan 에 run_id 나 dt 없음 · **기록 뒤 궤적 · thermo 가 바뀜** → 보류 (재담금질하지 않는다)
- 시험 (DK 재현 그대로):
  - MD 완료 · FIRE 미완 폴더에서 궤적 첫 원자 수만 120 → 121, 또는 첫 줄을 NUL 로 → 러너 rc 24 · '완료 단계를 못 읽는다' · 발사 0
  - save 0.7 ps 일정을 1,750 스텝에서 끊음 (6 프레임 = 완주와 같은 수) → 기록이 없어 미완
  - 진짜 MD 루프 (LJ) 가 FIRE 전에 기록을 쓴다 — 스텝 = 계획 · 궤적 해시 · final.xyz 를 지우면 `md_complete`
  - 드라이버 단위: thermo 바뀜 · 궤적 없음 · 다른 run_id · 스텝 모자람 · 기록 잘림 · plan run_id 없음 · dt 없음 → 판독 불가
- ⛔ 남는 한계 (docstring): 마지막 스텝과 기록 사이 (몇 ms) 에 끊기면 MD 가 끝났어도 '미완' 으로 읽혀 재담금질 쪽으로 간다 — 창이 짧아 받아들였다.

**P0-2 재시도 분류와 정전 예산 집계가 다른 판정을 읽음** —
- **실행 상태를 한 곳에서 정한다** — 드라이버 `run_kind(row, folder)`: 장부 판정과 보존 폴더 판정을 같이 본다.
  - 어느 쪽이든 pass · fail → `scientific`
  - 폴더 판정을 못 읽거나 장부 값이 모르는 값 → `unreadable`
  - 어느 쪽이든 invalid → `invalid`
  - 그 밖 (판정 없음 · incomplete) → `interrupted`
  - 러너 재시도 자격 · 확인 때 선언 검사 · 소비자 이력 검사가 이 함수를 같이 쓴다. 과학적 · 판독 불가 실행은 **확인 단계에서** 선언을 거부한다.
- **정전 추가 예산 (45 h) 을 없앴다** (카드 v3) — 상한 = 카드 `stage1_cap_gpu_h` (230) 그대로. 예산 혜택 경로 자체가 없어서 '판정을 어디에 적었나에 따라 예산이 달라지는' 길이 없다.
  - 정책 판단: 시드당 견적 15–21 h × 10 = 150–210 h. 정전 한 번의 버린 런 (≤ 21 h · 보통 그 절반) 을 더해도 대개 230 안이라 실익이 작다.
  - 넘으면 기존 상한 규칙 그대로다 (새 시드를 안 띄우거나 그 담금질을 멈추고 미완결 · 상한 인상은 카드 개정 = 결정).
  - 끊긴 런 재시도 (시드마다 1 회) 는 남겼다. kgy 10 월 끊김이 셋이라 1 단계 동안 한 번 이상 끊길 확률이 45–60 % 다.
  - 검사기는 없앤 두 값 (`outage_reasons` · `stage1_outage_extra_budget_gpu_h`) 이 카드에 남아 있으면 거부한다.
- 시험:
  - DK 표 그대로 — 같은 파일 · 이력 · 비용에서 invalid 를 **폴더에만** 적은 것과 **장부에도** 적은 것 → 같은 track (stage1_pass) · 같은 상한 (230) · 같은 총비용
  - 카드 상한 50.5 h 에서 B12 가 정전으로 2 h 를 잃어도 상한 50.5 그대로 → 러너가 마지막 시드를 안 띄우고 미완결 · 소비자 상한도 50.5
  - `run_kind` 단위: 장부에만 · 폴더에만 · 둘 다 invalid → 같은 답 / 폴더 판정 잘림 · 장부 값 모름 → 판독 불가
  - 확인 단위: 폴더 pass · 판정 잘림 실행에 선언 → 거부

**P1-2 소비자가 0 h 증언 상한을 받음** — 소비자도 `attested_upper_bound` 에 유한한 **양수** 를 요구한다 (측정 비용 0 은 따로 허용).
- 시험: 하한 · heartbeat 0 인 고아 런에 0 h 증언 행 → 무효 · 0.5 h 는 통과.

**인터페이스가 바뀐 곳**:
- 드라이버: `MD_DONE_NAME` · `planned_md_steps(plan)` · `write_md_done(out, run_id, n_steps_planned, n_steps_done)` · `run_melt_quench(..., run_id=None)` · `folder_stage` (완료 기록 기준) · `run_kind(row, folder)`
- 드라이버에서 없앤 것: `effective_cap` · `_cut_short` · `CUT_SHORT_STATUSES` · `ledger_check` 의 `cap_info` (반환 `cap_h` = 카드 상한)
- 카드: `outage_reasons` · `stage1_outage_extra_budget_gpu_h` 없앰
- 러너: 실효 상한 없음 · 고정 드라이버 sha16 `931564744093955d`

## 3. 이것을 특히 봐 달라

1. **완료 기록의 결박** — 기록은 run_id · 스텝 · 두 해시만 묶는다 (마지막 구조 좌표를 따로 담지 않는다 — 궤적 해시가 그 자리를 대신한다). 이걸로 '이 실행의 MD 가 끝까지 돌았다' 가 충분히 결박되는가.
2. **기록 없는 완주** — 기록을 쓰기 직전 (마지막 스텝 뒤 몇 ms) 에 끊긴 런은 '미완' 으로 읽혀 재담금질 대상이 된다. 이 창을 남겨도 되는가 (궤적 프레임 수가 완주와 같으면 보류로 돌리는 보조 규칙이 필요한가 — 다만 그러면 DK P1-1 의 '프레임 수 ≠ 완주' 문제로 돌아간다).
3. **정전 추가 예산을 없앤 판단** — 정책 단순화가 DJ Q4 ('가능하면 사전 규정') 와 어긋나는가. 넘을 때는 카드 개정 (결정) 으로만 상한을 올리는데, 그 결정이 결과를 일부 본 뒤에 나온다는 점을 어떻게 보나.
4. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DK 지적 (P0-1 · P0-2 · P1-1 · P1-2) 과 DJ 남은 항목 (Q2 · Q4 · Q5) 마다 닫힘 여부 한 줄.
