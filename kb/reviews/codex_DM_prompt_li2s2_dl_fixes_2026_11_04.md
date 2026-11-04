---
title: "DM 프롬프트 — li2s-2 DL 고침 확인 (04555774): 완료 증거가 남은 폴더는 보류 · 완료 기록 저장 순서 (fsync) · FIRE 진입 순서 시험 — 첫 담금질 GO 여부"
date: 2026-11-04
updated: 2026-11-04
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DM
track: li2s
channel: codex
kind: prompt
status: 발송 · 회신 수령 2026-11-04 (NO-GO · P0 2 · `codex_DM_reply_li2s2_dl_fixes_2026_11_04.md`) · 기준 커밋 04555774
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DL (390441c4 · NO-GO · P0 1 · P1 2) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `04555774` (브랜치 `claude/friendly-meitner-lldvar` · 기록까지 들어간 커밋). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DM_reply_li2s2_dl_fixes_2026_11_04.md` 로 원문 보존.

---

**[li2s-2] DL 고침 확인 — 재승인 최소조건 셋 (완료 증거가 남은 폴더를 재담금질 대상으로 내리지 않기 · 완료 기록 저장 범위와 실패 → 보류 · FIRE 진입 순서 회귀시험) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DL 의 P0 하나 · P1 둘을 고쳤다 (결과 0 건). **지적마다 닫혔는가 (GO / 조건부 GO / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DL 이 해제로 본 항목 (DK P0-2 · DK P1-2 · DJ Q4 · Q3 정책) 은 다시 열지 않아도 된다.

**가능하면 DL 때의 재현 (`probe_results.json` 의 두 상태 · 순서 시험) 을 이 커밋에 다시 돌려 달라.** 인터페이스가 바뀐 곳은 §2 끝.

## 1. 보는 범위

- `git diff 390441c4 04555774 -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_완료_기록_v4_2026_11_04` (결과 0 건 · 카드 값은 안 바뀜)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 210) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 81 · Linux)
- 깨기 (변이) ****147 / 147 빨강**** — 저장소 밖 복사본에서 DG · DH · DI · 정전 복구 · DJ · DK · DL 고친 곳을 하나씩 되돌려 해당 시험이 빨개지는지. DK 판 125 개 중 folder_stage 를 다시 써서 자리가 없어진 2 개 (L6 · L7) 는 새 자리 (N22 · N23) 로 옮겼고 DL 자리 24 개를 더했다 (147). 본 판은 빨강 146 · **초록 1 (N6 — thermo 의 덜 써진 꼬리를 '시작된 기록' 으로 세지 않음)** 이었다 — 시험 구멍: 그 경우의 조각 `4.0` 이 다음 시각과 같아 온전한 행으로 읽혀 꼬리 규칙을 안 거쳤다 → 조각을 NUL 섞인 정전 꼬리로 바꾸고 N 계열 24 개를 다시 돌려 24/24. 나머지 123 개는 바뀐 시험 한 줄과 무관한 코드라 다시 돌리지 않았다. 스크립트 · 로그 · 해시 · README = `db/raw/li2s2_dl_mutation_2026_11_04/`

## 2. DL 지적별로 한 것

**P0 + Q2 — 완료 증거가 남은 폴더를 재담금질 대상으로 내리지 않는다.** 드라이버 `folder_stage_detail(folder)` → (단계, 이유) 하나를 러너 재시도 자격 · 확인 때 선언 검사 · 소비자 이력 검사가 같이 쓴다 (`folder_stage` 는 첫 값).
- `final`: result.json · final.xyz 가 있음 (판정하라)
- `md_complete`: 완료 기록이 맞음 (FIRE 보류 · DK 그대로)
- `unreadable` (보류) — 새로 넣은 것:
  - **임시 기록 `md_done.json.tmp` 가 남음** (정식 기록 유무와 무관 · 완료로 승인하지 않음)
  - **plan.json 이 없는데 MD 산출물이 아닌 기록 밖의 파일이 하나라도 있음** — 허용 목록 `NON_MD_FILES` = 러너의 실행 전 기록 (`stage1_attempt.json` · `.tmp`) · 판정 기록 (`stage1_verdict.json` · `.tmp` · `stage1_verdict_history.jsonl`)
  - **FIRE 로그 (`final_relax.log`) 가 있는데 완료 기록이 없음**
  - **완료 기록 없이 시작된 마지막 기록이 끝 경계에 닿음** — 끝 경계 = 계획 스텝 N 안의 마지막 저장 스텝 `(N // save_int) · save_int` · '시작된 마지막 기록' = thermo.csv · traj.xyz 에서 온전한 마지막 행 · 프레임, **덜 써진 마지막 줄 · 프레임도 시작된 것으로 센다** (보수적 · 둘 중 큰 값)
  - 진행 기록을 못 읽음 — thermo 머리 없음 · 꼬리가 아닌 자리의 깨진 줄 · 시각이 저장 간격대로 아님 · traj 프레임 머리가 꼬리 아닌 자리에서 깨짐 · plan 에 save_ps 없음
- `md_incomplete` (재시도 대상) — **명확한 도중 끊김만**: plan 이 있고 위 보류 조건이 없고 시작된 마지막 기록이 끝 경계 앞이거나 MD 기록이 아예 없음 (사전 이완 중)
- `no_plan` (재시도 대상) — plan.json 이 없고 폴더에 `NON_MD_FILES` 밖의 것이 없음
- 정전 꼬리 (NUL 덩어리 · 덜 써진 마지막 줄) 는 받아 준다 — 그게 정전 때 정상으로 생기는 모양이라서. 프레임 · 시각은 완료 **승인** 에 안 쓰고 **보류** 판단에만 쓴다 (DL Q2 의 구별).
- 시험 (드라이버 단위 39 경우 · 러너 · 소비자):
  - DL 반례 1 — MD 완료 폴더에서 plan.json 만 지움 → 보류 · 러너 rc 24 · 발사 0 · 폴더 파일 해시 그대로 · 소비자는 그 뒤 재시도를 무효로 본다
  - DL 반례 2 — 완료 기록을 임시 이름으로만 (os.replace 직전 끊김) → 같은 셋
  - Q2 — 완료 기록 없이 끝까지 (1 ps 일정) · 0.7 ps 일정 1,750 스텝 (= 끝 경계) → 보류 (DK 때는 미완이었다 — DL Q2 대로 바꿨다) · 0.7 ps 일정 700 스텝 · 1 ps 일정 1 ps → 미완
  - plan 없고 실행 전 기록만 · 판정 기록까지 → no_plan / plan 없이 궤적 · 모르는 파일 → 보류 / FIRE 로그만 → 보류
  - thermo NUL 꼬리 · 덜 써진 마지막 줄 (도중) → 미완 · 덜 써진 마지막 줄이 끝 경계 → 보류 · 중간 깨진 줄 · 시각 어긋남 · 머리 없음 · traj 중간 깨짐 → 보류
- 고치면서 드러난 시험 쪽 결함 둘 (고침): ① 러너 시험의 보존 폴더 fixture 가 궤적은 1/3 로 자르면서 thermo 는 전부 복사했다 (새 판독은 thermo 끝 경계 → 보류로 읽었다) → 궤적과 같은 행 수로 · ② 가짜 드라이버 (FakeQuench) 가 '0 번 프레임 종 바뀜' 시나리오에서 thermo 0 행을 빼먹었다 (진짜 드라이버는 쓴다 · 새 판독이 '꼬리 아닌 자리에서 시각 어긋남' 으로 잡았다) → 진짜처럼

**P1-1 — 완료 기록 저장 범위.** `write_md_done`:
- 순서: traj.xyz · thermo.csv fsync → 두 해시 → 임시 기록 쓰기 · fsync → `os.replace` → 부모 디렉터리 fsync (Windows 는 디렉터리 fsync 가 없어 건너뛴다 · 생산은 Linux 뿐)
- 어느 단계든 실패하면 예외가 올라가고 FIRE 를 안 한다. 그때 폴더는 보류 갈래 셋 중 하나다 — 데이터 fsync 실패 = 기록 없음 + 끝 경계 (보류) · 임시 기록 fsync 실패 = 임시 기록 (보류) · 디렉터리 fsync 실패 = 기록 있음 (md_complete 보류)
- docstring · 카드: '몇 ms' 한정을 뺐다. fsync 가 저장장치에 닿는지는 파일시스템 · 장치 캐시에 달렸고 kgy 에서 전원을 끊어 본 적이 없으니 **정전 뒤 기록이 남는다고 보증하지 않는다** — 기록이 없을 때는 끝 경계 규칙이 보류로 받친다
- 시험: 저장 순서 (교체 전 임시 기록 fsync · 교체 뒤 디렉터리 fsync 를 그 시점의 파일 상태로 확인) · 세 단계 실패 주입 → 예외 + 보류

**P1-2 — FIRE 전 기록 순서의 회귀시험.** selftest 가 진짜 MD 루프 (LJ) 를 돌리며 `ase.optimize.FIRE` 를 탐침으로 바꿔, final_relax 용 FIRE 가 **생성되는 순간** `folder_stage` 가 이미 `md_complete` 이고 final.xyz 가 없는지 본 뒤 멈춘다. 변이 N17 (기록 호출을 FIRE 뒤로) 은 빨강이다 (FIRE 진입 탐침이 `unreadable` 을 본다).

**Q1 · Q3** — 카드에 적었다: 완료 기록은 종료 구조의 복구 수단이 아니다 (FIRE 복구는 새 결정 · 그때 저장 간격 조건을 확인하거나 종료 구조를 따로 저장) · 상한 인상은 결과 열람 후 운영 개정 (미완결 기록 보존 · 이유 · 한도 · 남은 실행 목록을 재개 전에 고정 · 계 · 시드 골라 추가 금지).

**인터페이스가 바뀐 곳**:
- 드라이버: `MD_DONE_TMP` · `NON_MD_FILES` · `save_interval_steps(plan)` · `_fsync_file` · `_fsync_handle` · `_fsync_dir` · `md_last_recorded_step(folder, plan)` (+ `_thermo_last_step` · `_traj_last_step`) · `folder_stage_detail(folder)` · `folder_stage` = 그 첫 값 · 소비자 메시지에 이유
- 러너: 재시도 자격의 보류 메시지에 이유 · 고정 드라이버 sha16 `b0f8a1ecbaafe029`

## 3. 이것을 특히 봐 달라

1. **끝 경계의 정의** — `(N // save_int) · save_int` 와 '시작된 마지막 기록 (덜 써진 꼬리 포함 · thermo · traj 중 큰 값)'. 완료됐는데 기록이 없는 실행이 '명확한 도중 끊김' 으로 읽히는 경로가 남았는가 (정전으로 fsync 안 된 꼬리가 사라지는 경우는 DL Q2 가 받아들인 한계로 적었다).
2. **plan 없는 폴더의 허용 목록** — 판정 기록 (`stage1_verdict.json` · 이력) 을 'MD 산출물이 아닌 기록' 으로 넣었다 (러너가 plan 전 끊긴 런도 판정할 수 있어서). 이게 완료 증거를 숨길 수 있는가.
3. **fsync 범위** — MD 중에는 fsync 를 안 하고 완료 기록을 쓸 때만 데이터 · 기록 · 디렉터리를 동기화한다. 이걸로 '저장 실패 → 보류' 가 충분히 이어지는가.
4. **넘친 보류** — plan.json 이 깨진 채 (시작 때 덮어쓰기 중 끊김) MD 산출물이 없는 폴더도 보류다 (DK 때와 같다 · 재담금질해도 되는 경우를 사람이 보게 된다). 받아들일 만한가.
5. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DL 지적 (P0 · P1-1 · P1-2) 과 DJ 남은 항목 (Q2 · Q5) 마다 닫힘 여부 한 줄.
