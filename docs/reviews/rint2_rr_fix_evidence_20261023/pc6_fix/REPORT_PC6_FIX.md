# Rint ② 사전 공격 6 회차 고침 — PC6-01 · 02 · 09 · 12 · 11 (11-02 · 작업 트리 에이전트)

기준 `7d6ea1e6f` · 바꾼 파일 `scripts/rint_r_chain.py` · `scripts/test_rint_r_chain.py` · 보고 (읽기만) `docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/PREATTACK_C2.md` · 마무리 판 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/PREATTACK_C2_final.md`
봉인 대조: 바뀐 둘 ∩ S0 같음 7 = ∅ · ∩ 194 CODE_FILES 32 = ∅ (R 사슬 코드 키 19 = rint_r_chain.py 포함 · 설계상)

본 가지 커밋 (11-02 `cherry-pick -x` · 충돌 0 · 원 작업 트리 커밋 = 각 커밋 메시지의 "cherry picked from commit" 줄): `483cf413e` (시험 먼저 01 · 02) · `93d8c3d34` (고침 01 · 02) · `dde41fb2f` (시험 먼저 09 · 12) · `db2e1b2b4` (고침 09 · 12) · `ac888877d` (PC6-11 시험) · `7f1d7dde3` (보강 시험) · `b309f0b78` (PD01r 시험 고침) · `f3f6de276` (증거) · 마무리 보고 `8bf1fd6ad`.  아래 줄 번호 = 이 판 `scripts/rint_r_chain.py`.

## 이번에 닫는 것

- PC6-01: environ 못 읽는 같은 실 uid 프로세스 = 러너 세션 · 그룹 번호 (stat) + 계보 (ppid) 로 가름 — 안 · 자손 · 계보 위 표지 env = 확인 불가 (보수) · 밖 = 셈 밖 · 세션 번호 다시 쓰임 = 지도자 시작 틱 · 고리 · 깊이 64 · 부모 stat 못 읽음 = 확인 불가 · 확인 불가여도 찾은 원은 죽임 · 시작 기록 runner_start · 끝 기록 unsure (proc_stat :2357 · _run_session_ours :2410 · _run_kin :2421 · group_members :2457 · group_settle :2557 · run_in_group :2630 · recover_group :6411)
- PC6-02: CUDA_ERROR_WORDS (CUDA_ERROR_ · cudaError · CUDARuntimeError · CUDADriverError · :2787) — words_cause 한 곳 (:3590 · 잘못된 주소 → 자원 → CUDA 표지 → 기본) · words_keep (:3603) 을 stop_cause (:3619) · orphan_cause (:3646) 모든 길이 부름
- PC6-09: 같은 --attempt 재입력 · 이 항목 시도 폴더 (attempt.json n · 대상 · 기계 · 재실행 원 시도 = 원장 · 시작 커밋 = 원장 조상) = 화면만 ATTEMPT_LEDGER_MISMATCH rc 3 (recover 안내 · 원장 · 폴더 무변경) · 남의 폴더 = 옛 그대로 (attempt_open :3349)
- PC6-12: found_attempts_problem (:3780) — 찾은 시도 폴더 attempt.json ↔ 원장 항목 · 판정 · 예측 입력 · 합치기 · 합친 예측 판정 넷이 같은 함수
- PC6-11 (부분): M2e · M2c · M9 · M8 · M11 · M12 · M15 = 시험 PD11 · PD11m · PD11p · PD11g · PD11s

## 시험 (로그 = logs/)

PD01 · PD01r · PD02 · PD02r 0/4 → b1 4/4 (before_PD_0102 · after_b1_subset 98/98) · PD09 · PD12 · PD12m · PD12u 0/4 → b2 4/4 (before_PD_0912 · after_b2_PD 11/11)
전체 415/415 · 끝-끝 40/40 (`db2e1b2b4`) → 421/421 · 40/40 (`7f1d7dde3`) · PD 14/14 (3.11) · Y13,PD 15/15 (3.8 · `b309f0b78`)
3.8: PD,PC 34/35 (PD01r — root + /root 아래 uv 인터프리터) → `b309f0b78` 고침 뒤 통과 · 사본 전체 420/421 (Y13 = git 아님)

## 변이 (mutate_pc6fix.py · mut_*_res.json)

49 = 잡힘 47 · 생존 N01l (결정 동등) · N12d (이중 방어 · 미시험) · PC6-11 일곱 잡힘 (옳은 이유 · mut_pc611_re) · 보강 전 a3 판 아홉 중 여덟 생존 → 아홉 잡힘 · 10-28 의 32 = 29 잡힘 + 3 ERROR (옛 글 옮김 · 같은 가드 P02b2 · P06b2 · P07b2 잡힘).  PC6-11 일곱의 "고치기 전 생존" = 6 회차 마무리 보고 값 (이 에이전트가 다시 재지 않음).

## 닫지 않는 것

M4 · M5 · M6 · M10a · M10b (작은 fixture 로 못 닿음) · U4 (그룹 미확인이면 러너 0 아닌 종료 코드 무시 → 파이썬 traceback 도 재실행 자격 · 선택지 A 권고 / B = 1저자 · 원장 PC6-13) · CUDA 라이브러리 상태 문자열 (CUBLAS_STATUS_ 등 · 'CUDA error:') = 표지 아님 (1저자) · 표지 = 부분 문자열 (무해한 언급도 자동 재실행 막음 = 보수 쪽) · hidepid=1 (남 stat 못 읽음 → 늘 미확인 · PC5 와 같음) · hidepid=2 (숨은 조상 = 없어진 것) · setsid + 부모 끝남 + environ 못 읽음 = 놓침 · 러너 세션 안 확인 불가 = 즉시 (대기 중 다시 안 봄) · PC6-12 = 호출자가 훑는 폴더 범위 (Q-D 한정 · N12f · N12g 는 단위 시험 PD12u 로만) · P3 PC6-03 · 04 · 05 · 06 · 08 · 10 · 등록 R §10-5 아 ② (CUDA 표지 · 모든 길) · ⑦ (러너 세션 · 계보 · PC6-09 화면만 · PC6-12) 문구 · 웹앱 = 바뀐 화면 없음 · kgy 실제 (Python 3.8.10 · 비 root · ssh · /proc 옵션) · 실제 GPU 결함 뒤 D 상태 = 미확인
