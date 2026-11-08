# 사전 공격 12 — `6a81f0c55` `scripts/rint_r_chain.py` 새 가드 (diff · 코드만 읽음)

대상: P2-A `rejected_in_folder` · P2-B `stop_record_problem`/`stopped_record_problem`/`record_outdir`/`chain_confirmed` · P3-5 `summary_shape_problem` · 같은 자리 `run_traces`/`end_record_known`/`run_exit_failed`.
HEAD 2b3c42c6c 의 이 파일 = 6a81f0c55 와 같음.  탐침 = 리포 모듈 읽기 전용 import · 실제 git 원장 경로는 시험 도우미 (`rc_recover_resume`) 그대로.
경로 앞자리 `P=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/preattack12` (출력 = 같은 이름 `.out`).

## 발견

**F1 (P2) 정확 출력 폴더 이름 대조가 같은 기록의 요청 칸에만 묶여 있다** — `stopped_record_problem` ② (4027–4033) · `record_outdir` (4773).
기대 이름 = 그 기록의 arms · arm_list 로 계산 → outdir 와 요청 칸을 함께 고치면 지난다.  범위 검사도 없다: arms 9 · 0 · −1 · 10**30,
arm_list [] · [0] (접두 목록) · [9] · [3,3] · [3,1] = 생산자가 쓰지 않는 값인데 받는다.  `check_trace(folder, od)` 는 없는 옆 폴더만 보고
진짜 L01_floor_arm1/.unchecked 의 검사 실패 흔적을 못 본다.
- 재현 `$P/p1_outdir_coedit.py` — 정직 (arms 1 · _arm1) = resume_ok False · CT06 꼴 (arms 1 · _arm9) = False · 함께 고침 11 가지 전부 **True** (TIME_LIMIT 도)
- 실제 원장 `$P/p2_real_ledger.py` (1b) — arms 9 + outdir _arm9: 결과 줄 resume_ok **True** · `--add --resume 1` **rc 0** (기대: 사유 · rc 3 = 1a 처럼)
- 생산자 범위 안 (arms 1→2 + _arm2) 도 지나므로 범위 검사만으로는 안 닫힌다 → 흔적 검사를 디스크의 `<런>` · `<런>_arm*` 전부로, 또는 od 밖 `<런>_arm*` 존재 = 모순.

**F2 (P2) GU 대조 ④ 는 chain_end.confirmed 만 본다 — 정직 GU 의 한 칸 (rc 1→0) 이 재실행 자격을 얻는다** — `chain_confirmed` (4044–4069) · 4037.
생산자 GU = by chain 끝 기록 확인 False → recover 가 by recover + chain_end {rc · cause · confirmed False} 로 갈아 씀.  러너가 스스로 rc 1 (Traceback)
로 끝났는데 그룹 미확인 → 정직 = runner_rc · False.  요약 런 기록 rc 1 → 0 **한 칸** → group_unconfirmed · **True** · resume rc 0.  같은 폴더의
chain_end.rc = 1 (chain_confirmed 가 이미 읽는 그 dict).  {timeout · null} 두 칸 꼴도 지남.
- 재현 `$P/p2_real_ledger.py` (2a 정직 rc 3 · 2b 한 칸 rc 0 · 2c)
- 커밋 글의 "한 칸 손질 넷 … GU 기록 rc … 닫음" 은 과장: CT06 `S2_forged_GU_rc0` 는 끝 기록 CHAIN_OK1 (by chain · 확인 True = GU 생산자가 남기지 않는 꼴)
  위에서만 시험됐다.  선언 한정 "런 기록 ↔ 끝 기록 (원인 · rc) 교차 대조" 의 사례지만, 요청서에 "닫힘" 으로 쓰면 SELF 부류 (전칭).

**F3 (P2) 런 기록 없는 TIME_LIMIT ('none') = 런 이름 꼴 · 그 이름 흔적만 — runs 는 안 본다** — 4000 · `stopped_record_problem` `if rr is None: return None` (4021).
생산자는 앞 런이 {None · 정확한 0} 으로 끝나 팔을 읽은 뒤에만 다음 런의 시간 상한 관문에 닿는다 (실패 = 그 자리 멈춤).  정직 RUNNER_RC L01 rc 1
(Traceback · runner_rc · False) → stop 객체 두 칸만 (code TIME_LIMIT · run = 다음 이름 L02_ceiling, 또는 생산자 꼴도 아닌 'zzz') → timeout · **True** ·
resume rc 0 · `ResumeRunner._src_done(L01)` = False ⇒ 재실행이 rc 1 런을 다시 돈다.  선언 한정 "런 전 TIME_LIMIT 이름 차례" 로 안 덮인다 (이름은 맞는 다음 이름).
- 재현 `$P/p4_tl_none_after_fail.py`
- 같은 부류 F3b (P2–P3): 멈춘 기록 앞의 기록이 exit_ok 인지 안 봄 — [L01 rc 1, 위조 L02 {timeout,null}] + 빈 L02 로그 = TIME_LIMIT True ·
  [L01 rc 1, L02 {None,0}] + GU (L02 그룹 기록 없음) = True (`$P/p5_misc_b.py` a1 · a2)

**F4 (P3) 단계 요약 읽기 = 느슨한 json.loads (중복 칸 = 뒤 값 · NaN 받음)** — `read_summary_state` (5625).  새 가드가 읽는 arms · outdir · rc 가
`"arms":1,"outdir":"L01_floor_arm1", … "arms":9,"outdir":"L01_floor_arm9"` 꼴이면 사람 = 앞 값 · 코드 = 뒤 값 → F1 이 겉보기 정직한 기록으로 (`$P/p5_misc_b.py` b:
읽기 ok · 다시 셈 resume_ok True).  거부 기록 · 계획 · 원장은 이미 `_json_strict`.

**F5 (P3) 폴더 안 거부 기록 code = 글자 꼴만** — `rejected_form_problem` 4303.  'XYZ' (STOPS 밖) · 'CALIBRATED' · 'GENERATION' · 'OUTDIR_NOT_EMPTY' (옆 기록 전용)
= rejected · 결과 줄 멈춤 이름 그대로 (채택 영향 없음 · 표시만).  `code in STOPS` (폴더 안이면 OUTDIR_NOT_EMPTY 제외) 권고.  `$P/p6_rejected.py`

## 버틴 것 (한 줄씩)
- 거부 기록: 칸 더 · 빠짐 · schema · n 1.0/true/"1"/1e400(inf) · NaN · 중복 칸 · BOM · 끝 줄바꿈 · 전각 · 커밋 대소문자 · 숨은 폴더 · 그 밖 파일 = Stop (`p6`) · 링크 = Stop (CT05)
- rejected.json 이 폴더 = 거부로 안 셈 (interrupted · pre · False) — 채택 제외 효과 없음
- 요약 꼴: 무작위 30,000 (stop · runs · 기록 칸 = None · bool · 2**70 · NaN · 글 · 경로 · NUL · 목록 · 객체) → result_fields 의 Stop 아닌 예외 0 (`p3`)
- outdir 정규화: 끝 '/' · './' · '../x' · 빈칸 · 대소문자 · 유니코드 숫자 · 절대 경로 = 거부 (RUN_DIR_RE + 접두)
- run_record_shape: rc bool · 0.0 · 글 · NaN · group_cause 대소문자 · 빈칸 · falsy (False · '' · 0) = bad = 거부
- arms bool · "1" · 1.0 · NaN = '' = 거부 · chain_confirmed: confirmed 1 · null · chain_end 목록 · by 이상 = 거부
- 생산자 꼴 (timeout · signal · signal_after · GU→recover chain_end False · 8 팔 · _arml · 재실행 복사 뒤 · 런 전 TIME_LIMIT) = 받음 — 거짓 fail-closed 못 찾음
- STOPS 60 개 이름 전부 STOP_CODE_RE 일치 (거부 기록 거짓 fail-closed 없음) · 봉인 원천 G… RUNNER_RC = 읽음 False (선언 · 안전 쪽)

## 선언된 한정 (닿는 것만 확인 · 발견으로 세지 않음)
arms 칸 없음 → 접두만 (`p5` c1 True) · arms_read 칸 없음 = [] · GU 시작 기록 없음 · chain_end 없는 옛 recover 끝 기록 → ④ 건너뜀 (`p5` c2 True vs c3 False) ·
RUNNER_RC 정직 rc 1 → 기록 {signal,null} 두 칸 (`p5` c4 True) · 결과를 지운 폴더 + 생산자 꼴 거부 기록 · utc 시각 꼴.

## 권고 (짧게)
① arms 1–8 · arm_list (정렬 · 중복 없음 · 0–7 · 길이 = arms · 접두 아님) + 흔적 검사를 그 런의 모든 출력 폴더로  ② 멈춘 런 기록 (group_cause, rc) ↔ 사슬 쪽
(by chain 끝 기록 · recover chain_end) 생산자 대응표 대조 (signal_after = 디스크 원인 None)  ③ 멈춘 기록 앞 기록 전부 exit_ok · 'none' 이면 runs 마지막도 exit_ok
+ arms_read 비지 않음  ④ 결과 줄 길의 요약 읽기 = `_json_strict` 꼴 (중복 · NaN = unreadable)  ⑤ 거부 기록 code ∈ STOPS.
