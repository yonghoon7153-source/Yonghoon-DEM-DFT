---
title: "DO 프롬프트 — li2s-2 DN 고침 + DO 전 독립 리뷰 고침 확인 (802290db): 완료 필드 타입 · 첫 시드 녹음 fail 기록 순서 · 보존 폴더 판정 · MD 뒤 산출물 · 장부 꼴 — 첫 담금질 GO 여부"
date: 2026-11-04
updated: 2026-11-04
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DO
track: li2s
channel: codex
kind: prompt
status: 초안 → 발송 대기 · 기준 커밋 802290db
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DN (acc648b0 · NO-GO · DM P0 두 건 해제 · P1 1 · P2 1) 다음 편지다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `802290db` (브랜치 `claude/friendly-meitner-lldvar` · 기록까지 들어간 커밋). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DO_reply_li2s2_dn_fixes_2026_11_04.md` 로 원문 보존.

---

**[li2s-2] DN 고침 확인 + DO 전 독립 리뷰 고침 — 재승인 조건 (완료 필드 타입 오류의 러너 · 소비자 차단 · 대조군 유지) 이 닫혔나 · 고치면서 새로 생긴 구멍은 없나 · 발사 GO 여부**

## 0. 무엇을 묻나

DN 의 P1 · P2 를 고쳤다 (결과 0 건). 그 뒤 DO 를 보내기 전에 **우리 결론을 모르는 독립 리뷰 셋**을 따로 돌렸다.
- 방식은 Codex 와 같다: 진짜 판정 · 판독 함수로 손상 · 복구 상태를 만들어 재담금질이나 1 단계 통과로 새는지 본다.
- 영역: 드라이버 폴더 판독 · 러너 재시도와 비용 장부 · 소비자와 문구 대조.
- 결과: P0 3 갈래 · P1 셋 · P2 스무 건 남짓이 재현됐고, 이 커밋에서 고쳤다 (§2).

**물음: DN 지적 (P1 · P2) 이 닫혔는가 · DO 전 리뷰 고침이 맞게 닫혔는가 · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가 (GO / 조건부 GO / NO-GO).**
DN 이 해제로 본 항목 (DM P0-1 · P0-2 · 정상 중단 대조 · Q1–Q4) 은 다시 열지 않아도 된다.

**가능하면 DN 재현 (thermo 없음 · 궤적 완주 · FIRE 미완 → 꼬리 소실 → n:"130") 과 대조 (정상 incomplete · invalid · 진짜 plan 전 끊김 · 명확한 도중 끊김) 를 이 커밋에 다시 돌려 달라.**

## 1. 보는 범위

- `git diff acc648b0 802290db -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 카드 `개정_완료_기록_v6_2026_11_04` (DN) · `개정_DO_전_리뷰_v7_2026_11_04` (리뷰 고침 규칙 · 옛 문구 정정 · 못 하는 것) — 결과 0 건 · 카드 값은 안 바뀜
- 리뷰 기록 `db/raw/li2s2_pre_do_review_2026_11_04/README.md` (찾은 것 → 고침 → 시험 · 리뷰어 스크립트 재실행 결과)
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 220) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 100 · Linux)
  - Windows 에서는 러너의 POSIX 전용 3 개를 건너뛴다 (진짜 프로세스 그룹 2 · 띄우는 순간 신호 1) → 97 이 맞다. 드라이버는 그대로 220.
- 깨기 (변이) **222 / 222 빨강 (전체 실행 218 · 39c02ed7 + 시험 구멍 넷을 이유 검사로 고친 뒤 다시 4 / 4 · 0e0c8739)** — DN 판 174 개 (DM 판 165 + DN 9) 를 가져오되 이번에 자리가 바뀐 10 개를 옮기고 DO 자리 48 개 (`DO1_…` ~ `DO48_…`) 를 더했다 (222). `db/raw/li2s2_do_mutation_2026_11_04/`

## 2. 한 것

**DN P1 — 완료 판단 필드의 타입 오류 = 해석할 수 없는 기록 (보류).**
- `_completion_fields_problem` — 필드가 없거나 None 이면 허용 · 있는데 타입이 틀리면 보류 · 정수로 바꿔 읽지 않는다.
  - 객체: provenance · files_sha256 · gate_check · checks · traj_frames
  - 참거짓: schedule_complete
  - 정수 (참거짓 아님): n ≥ 0 · expected ≥ 1
  - 지문: 64 자리 16진수
- 이력의 새 판정 지문은 쓰인 그대로 본다.
- plan 전 판정의 이유는 정확히 같아야 한다.

**DN P2** — 문구를 맞췄다: 시각의 유효한 앞부분이 남은 꼬리는 센다 · NUL 만 남은 꼬리는 진행량을 복원하지 못한다 (카드 v6 · docstring).

**DO 전 리뷰 P0-1 — 첫 시드 녹음 fail 이 지워짐 (러너).**
- 재현:
  - 정리 실패 (그룹이 남음) → abnormal 로 멈춰 판정 · 닫힘 기록이 없음 → 재부팅 · 증언 · 보존 → A11 재담금질 · stage1_pass.
  - 판정 도중 Ctrl-C → 같은 결과.
  - 녹음 invalid + 정리 실패 → 끊긴 런으로 바뀜.
- 고침:
  - 녹음 판정 결과를 **담금질을 멈추기 전에** 장부에 적는다 (`melt_check` · fail 이면 `closes_system`).
  - 정리에 실패해도 멈춤은 melt (닫힘 · 확인으로 못 넘김).
  - 고아 마감은 앞 상태 · rc 를 남긴다 (`status_before_orphan` · `rc_before_orphan`).
  - 실행 종류: 장부 흔적이면 과학적, melt_check invalid 면 invalid.
  - 소비자도 장부의 첫 시드 닫힘을 그 계의 닫힘으로 센다.

**DO 전 리뷰 P0 — 녹음 결과가 정해졌는데 정전 재시도 (정책 · 러너 · 소비자).**
- 재현: 녹음 창이 다 찼고 fail 인 채 (판정 전) 정전 → 정전 선언으로 재시도 → pass. 첫 시드 · 둘째 시드 모두 그랬다.
- 고침 (규칙 M):
  - 녹음 창이 다 찼고 fail 이면 그 시드는 fail 이다. 일정 미완 · 최종 파일 없음보다 앞선다.
  - `run_kind(row, folder, values)` 가 보존 폴더의 녹음 판정을 본다 (fail = 과학적 · invalid = invalid).

**DO 전 리뷰 P0 — 보존 · 끊긴 폴더 판정이 invalid 로 세탁 (소비자).**
- 재현:
  - 보존 폴더 이름 때문에 판정이 invalid → invalid 재시도는 끊긴 런 한도 밖 → 세 번째 발사.
  - 끝까지 돈 PS₄ fail 을 제자리 판정 → invalid → 원인 고침 재실행 → pass.
  - SIGTERM 반쪽 프레임 → invalid → 첫 시드 닫힘이 꺼짐.
- 고침:
  - 보존 폴더 `seed<N>.<붙임>` 은 실행 전 기록의 계 · 시드 · run_id 가 plan 과 같으면 같은 실행으로 식별한다.
  - 프레임 수는 NUL 꼬리 · 덜 써진 마지막 프레임을 빼고 온전한 것만 센다.
  - **invalid 판정은 끝난 런 (status ended · 녹음 invalid 로 멈춤) 일 때만 실행 종류를 invalid 로 바꾼다.** 끊긴 런 폴더의 invalid 판정은 끊긴 런이다.
  - 판정 기록 (현재 · 이력) 어디든 pass · fail 이면 과학적이다.

**DO 전 리뷰 P0 — plan 이 있는 폴더가 MD 뒤 산출물을 안 봄 (드라이버).**
- 재현: md_init_raw.xyz (끝 시각 129 ps) · gate_check.json · seed_gate.json · final.vasp 가 남아도, 꼬리가 사라지면 도중 끊김으로 읽혀 재담금질 · pass.
  - 러너의 대조 시험 `ctrl_mid_cut` 자체가 이 상태였다.
- 고침:
  - 완료 기록이 없는 폴더는 MD 루프 중 파일 (plan.json · initial.xyz · prerelax.log · traj.xyz · thermo.csv) 과 실행 전 · 판정 기록만 있어야 도중 끊김 후보다 (`MID_RUN_FILES`). 그 밖이면 보류.
  - 대조는 진짜 도중 끊김 폴더로 다시 만들었다.

**P1 · P2 (요약 · 자세한 것은 카드 v7 · 리뷰 README).**
- 드라이버:
  - '모름' 을 값으로 쓰지 않는다: gate 오류는 schedule_complete None + 오류 기록 = 보류 · thermo 의 NUL 꼬리는 건너뛴다.
  - 수 판정은 수 타입만 (`_fin` — 숫자 글자 · 참거짓 · 큰 정수 아님).
  - plan 일정 값은 타입 · 범위 검사.
  - final 자리에 디렉터리 · 깨진 링크가 있으면 보류.
  - 판독 예외 (깊은 JSON 등) 는 죽지 않고 보류.
  - 크기는 있는데 NUL 뿐인 파일은 보류.
  - 판정 기록 흔적 확장: 최종 구조 · 시드 게이트 흔적 · plan 기준 프레임 수 · 이력 줄 사본 일치 · plan 전 판정 열쇠 집합.
- 소비자:
  - 장부 꼴 검사: 계 · 시드 · end · closes · melt_check · 측정 행의 자기 하한.
  - 같은 JSON 열쇠가 둘이면 못 읽음.
  - 잘린 현재 판정에 죽지 않고 무효.
- 러너:
  - STOP — 못 읽거나 stop_id 가 없으면 원본을 덮어쓰지 않고 거부 · 확인 때 정해진 열쇠만 옮김 · 저장한 뒤 지움.
  - 카드 값 지문 고정 (`EXPECTED_VALUES_SHA16`) · 명령줄로 드라이버 고정값을 못 바꿈.
  - `--python` 을 시작 전에 점검한다.
  - 띄우는 동안 종료 신호는 손잡이를 적은 뒤에 받는다.
  - 다른 부팅이면 장부의 pgid 는 죽은 것으로 본다.
  - 실행 중 상한 검사가 상한보다 늦지 않다.
  - 장부 · STOP · 실행 전 기록 · 판정 쓰기는 fsync.
  - nvidia-smi 는 60 s 제한.

**시험**
- 리뷰어 재현을 진짜 판정 · 판독 함수로 selftest 에 넣었다. 러너 통합 시험 열여섯 · 드라이버 fixture 서른 가까이.
- 고친 코드에 **리뷰어 스크립트를 그대로 다시 돌렸다** → 모두 막힘 (발사 0 · stage1_pass 없음).
- 깨기 (변이) 가 시험 구멍 일곱을 드러냈다 — 코드는 맞고 시험이 그 자리를 안 봤다. 대부분은 이번에 넣은 새 검사가 같은 입력을 먼저 잡아 가렸다. 시험을 더했다:
  - DO6: final 자리 디렉터리 · 깨진 링크 검사를 꺼도, 같은 폴더를 MD 중 파일 목록 검사가 잡아 몰랐다 → 보류 이유 문구까지 본다.
  - DO19: gate 오류를 쓰는 쪽 (`stage1_verdict`) 을 안 봤다 → gate_check 를 예외로 바꿔 진짜 판정 함수로 기록 · 보류를 본다.
  - DO24: 꼴 틀린 장부 melt_check 가 글자 하나뿐이었다 → dict · 빈 목록 · 0 을 더했다.
  - D22 · D23: 장부에서 빠진 행의 판정 · 음수 비용을 넓힌 보존 폴더 검사 · 새 '자기 하한' 검사가 먼저 잡았다 → 각자의 무효 이유까지 본다.
  - N5 · DN8: FIRE 로그만 남은 폴더 · 꼴 틀린 gate_check 를 MD 중 파일 목록 검사 · 새 '판독 예외 → 보류' 감싸개가 먼저 잡았다 → 각자의 보류 이유까지 본다.
- Windows 에서 시험이 죽지 않게 했다 (시험만 · Linux 동작 같음):
  - 띄우는 순간 신호 시험은 `pthread_sigmask` 가 있는 OS 만 돈다. Windows 는 `os.kill(자기, SIGTERM)` 이 프로세스를 바로 끝낸다.
  - fsync 개수는 POSIX 만 디렉터리까지 2 번으로 본다.
  - 깨진 링크 fixture 는 링크를 못 만드는 계정이면 디렉터리로 같은 검사 ('파일이 아닌 것') 를 본다.
- 드러난 시험 쪽 결함을 고쳤다:
  - 대조 `ctrl_mid_cut` 이 MD 뒤 파일이 남은 폴더였다 → 진짜 도중 끊김으로.
  - 일부 반례 fixture 가 엉뚱한 검사에 막히고 있었다 → MD 뒤 파일을 빼서 각자의 검사로 막히게.
  - invalid 종류 fixture 에 '끝난 런' 상태가 없었다.

**인터페이스가 바뀐 곳**
- 드라이버:
  - 새 함수: `_completion_fields_problem` · `_plan_num` · `loads_strict` · `RUN_STATUSES_ENDED` · `MID_RUN_FILES` · `PRE_RUN_VERDICT_KEYS`
  - 시그니처가 바뀜: `run_kind(row, folder, values=None)`
  - 동작이 바뀜:
    - `identity_check` 반환에 `preserved` 가 붙는다.
    - `_xyz_frames` 는 온전한 프레임만 센다.
    - `read_thermo` 는 junk 줄을 건너뛴다.
    - `combine_stage1` 의 녹음 fail 우선순위가 바뀌었다.
    - `ledger_check` 가 `closing` 을 돌려준다.
    - `folder_stage_detail` 은 예외에 죽지 않는다.
- 러너:
  - 고정값 `EXPECTED_DRIVER_SHA16 = e0ab597b426158d6` · `EXPECTED_VALUES_SHA16 = 086de59c484f9c32` · `STOP_KEYS`
  - `--expect_sha` 명령줄 옵션을 없앴다.
  - selftest 에 `LI2S2_SELFTEST_FAILFAST=1` (변이 실행용 · 첫 빨강에서 멈춤 · 기본은 끔).

## 3. 이것을 특히 봐 달라

1. **실행 종류 규칙** — invalid 판정은 끝난 런일 때만 종류를 바꾼다. 끊긴 런이 다른 이유로 정말 invalid 인 경우도 '끊긴 런' 재시도 (한도 1 · 정전 선언) 로만 다시 돈다. 이 규칙이 막는 것 · 놓치는 것이 맞는가.
2. **규칙 M** — 녹음 창이 다 찼고 fail 이면 일정 미완이어도 그 시드는 fail. 끊긴 런의 보존 폴더 녹음 판정을 재시도 자격에 쓴다. 녹음 판정이 끝난 뒤 자료가 손상되면 invalid 로 바뀔 수 있다 — 그 경로가 과학적 fail 을 피하는 길이 되는가.
3. **첫 시드 닫힘의 근거** — 러너가 녹음 판정 fail 을 장부에 먼저 적으면, 나중 시드 판정이 다른 말 (예: 카드와 다른 실행 = invalid) 을 해도 닫힘을 그대로 둔다 (fail-closed · `verdict_disagrees` 기록). 받아들일 만한가.
4. **MID_RUN_FILES 허용 목록** — 드라이버가 MD 루프 전 · 중에 쓰는 파일만 넣었다. 빠졌거나 지나치게 넓은 것이 있는가.
5. **남긴 한계** (카드 v7 '못 하는 것'):
   - 발사 자체가 예외로 실패하면 끊긴 시도로 남아 재시도 한 번을 쓴다 (실행할 수 없는 `--python` 은 시작 전 점검이 막는다).
   - 확인 기록 저장과 STOP 지우기 사이에 끊기면 다시 확인한다.
   - nvidia-smi 실패면 interrupted 로 멈춘다.
   - 이것들이 P0 · P1 인가.
6. 새로 생긴 조용히 틀린 경로가 있는가.

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DN 지적 (P1 · P2) · DO 전 리뷰 갈래 (첫 시드 녹음 · 규칙 M · 보존 폴더 판정 · MD 뒤 산출물) · DJ 남은 항목 (Q2 · Q5) 마다 닫힘 여부 한 줄.
