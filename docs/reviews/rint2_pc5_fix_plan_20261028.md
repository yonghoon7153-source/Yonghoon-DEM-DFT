# Rint ② 사전 공격 5 회차 고칠 계획 (10-28) — PC5-01–11 · 변이 구멍 X09 · X18 · 봉인 전 남은 넷

- 근거: 보고 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/PREATTACK_C.md` (대상 `0c47df263` · 새 P1 0 · P2 6 · P3 5 · 변이 23 중 20 생존) · 원장 `PC5-01`–`11` · 봉인 전 남은 넷 = `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_C_decisions_20261028.md` §4 (#4 · #5 · #8 · #9).
- ✅ **1저자 10-28 밤 *"rint는 권고대로"*** = Q1 · Q2 · Q3 권고대로 (질문 원문 = 10-28 저녁 보고).

## 결정

| Q | 결정 |
|---|---|
| Q1 | 회차 ② 전 고칠 범위 = P2 여섯 (PC5-01–06) + 변이 구멍 둘 (X09 · X18) + P3 넷 (PC5-07 · 08 · 10 · 11) + 봉인 전 남은 넷 (§4 #4 · #5 · #8 · #9).  **PC5-09 = 고치지 않음** (쓰는 중 · 검사 전 죽은 payload 를 검사 실패 흔적으로 세는 것 = 보수 쪽 오거부 · 거짓 수용 없음 → 한정으로 적음 — 회차 ② 요청서 · 등록 R §10-5) |
| Q2 | 자원 낱말 (`RESOURCE_WORDS` · 자동 재실행 자격) = **메모리 · 디스크 다섯만**: `OutOfMemoryError` · `CUDA_ERROR_OUT_OF_MEMORY` · `cudaErrorMemoryAllocation` · `MemoryError` · `No space left on device`.  나머지 CUDA 오류 (cupy 클래스 이름 `CUDARuntimeError` · `CUDADriverError` 만 있는 줄 포함) = 자동 재실행 없음 (`runner_rc`) · `NOT_RESOURCE_WORDS` 는 그대로 먼저 본다 |
| Q3 | 다른 부팅 뒤 `--stage recover` = **기본 미확인** (다음 시도 채택을 막는다) · 운영자 확인 표지 (예: 시도 · 사유를 받는 인자) 를 붙이면 그 기록과 함께 확인으로 넘긴다 · machine_id 는 기계 정체로 쓰지 않는다 |

## 항목별 고침 방향 (시험 먼저 — 탐침 `probe_real.py` R1–R6 · `probe_unit.py` U1–U8 을 상주 시험으로 옮기고 고치기 전 판에서 옳은 이유로 실패 확인)

| 항목 | 고침 방향 |
|---|---|
| PC5-01 | 판정 · 합치기 · 풀기 전 대조가 원장 결과 줄의 `status` · `stop` · `cause` · `resume_ok` 를 폴더 증거 (요약 · 로그 · `.unchecked/`) 에서 다시 셈해 대조 · 덧붙이기만 검사 = 끝 커밋 교체 (`reset` 뒤 새 줄) · `merge -s ours` 숨김도 거부 (정직한 결과 커밋이 원장 첫 부모 역사에서 사라지면 거부) |
| PC5-02 | Q2 |
| PC5-03 | `recover` = 시작 기록의 사슬 부모 (`chain_pid` · 같은 부팅) 가 살아 있으면 거부 |
| PC5-04 | Q3 |
| PC5-05 | 재실행 시도가 풀기 전 대조 밖 단계 안 관문에서 결과 전으로 멈추면 재실행 사슬을 끝내지 않는다 (다시 재실행 가능) · Q9 §3-2 · §3-5 문장 셋 맞춤 |
| PC5-06 | 요약 없는 시도의 결과 줄 (recover) 도 런 로그 · 러너 rc 를 읽어 원인을 같은 낱말 규칙으로 분류 · 못 읽으면 `resume_ok false` (보수) · 단계 함수 밖 사슬 예외도 원인 기록 |
| X09 | 결과 줄 꼴 검사 (`rejected` 인데 결과 뒤 · 재실행 자격) 상주 시험 |
| X18 | `recover --ledger` 의 거부 기록 폴더 → `rejected` 결과 줄 길 상주 시험 (재실행 시도가 거부 기록 뒤 죽은 꼴) |
| PC5-07 | 그룹 원 찾기 = 상태 Z 라도 살아 있는 스레드 (`/proc/<pid>/task`) 를 본다 · environ 을 못 읽는 프로세스 = 미확인 |
| PC5-08 | 원장 덧붙임 = 잠금 + `git add` / `commit` 실패 시 작업 파일 되돌림 |
| PC5-10 | 다시 판정 = 원 판정 원장의 대상 밖 시도 (다른 대상) 는 다시 판정을 흔들지 않는다 |
| PC5-11 | 보고 숫자의 원자료 (변이 207 · kgy 11 묶음 · 결정성 9/9 · 회귀 21 묶음) 를 리포 증거 폴더로 |
| §4 #4 | 등록 R §10-1 · kgy 문서 §3 의 사다리 · 예측 명령을 원장 시도 꼴로 (판정 `--ledger` 와 맞게) · 두 문서 인자 집합 시험 (K01) 함께 |
| §4 #5 | 시험 고정물 (`reg_with` · `make_plan_and_reg`) 이 계획 숫자 블록을 등록 사본 끝에 덧붙이지 않게 (§2-1 자리 · 표지 하나) |
| §4 #8 | Q9 §3-2 "요청되지 않은 단위 대조 = 기록만" 문장 = 구현 (`UNIT_EXTRA` 멈춤) 에 맞춤 |
| §4 #9 | 등록 R §10-4 상자 ⑥ 주석 · 설명 페이지 10-27 주석의 "진행 중" → 날짜 표지 (웹앱 시험 먼저) |

## 순서

시험 먼저 → 고침 (작업 트리 에이전트) → 회귀 (사슬 · 끝-끝 · first_result · census · ext_runner · kgy 3.8 판) → 메인 통합 · 사전 공격 6 회차 (고친 diff 만 · 독립) → 게이트 → push → Codex 회차 ② 요청서.

## 진행

- ✅ 1저자 10-28 밤 Q1–Q3 권고대로 · 원장 PC5-09 = wontfix (결정 기록) · ▶ 수정 = 작업 트리 에이전트.
- ✅ 수정 10-28 밤 (작업 트리 에이전트 → 통합 가지로 옮김) — 시험 먼저 `b9fd47d7b` · 구현 `6bb3c064f` (PC5-01–08 · 10 · #5) · 문서 · 웹앱 `43a8abcaa` (#4 · #8 · #9 · PC5-09 한정 한 줄 · PC5-11 원자료 `report_c_raw/`) · 증거 폴더 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/fix_pc5_20261028/` (`SOURCE.txt` · `SHA256SUMS`) · 사슬 시험 407/407 · 끝-끝 40 PASS · 0 FAIL · first_result 9/9 · s0_census 167 · ext_runner 151 · 웹앱 91/91 · kgy 판 11 묶음 통과 · 새 가드 변이 32/32 잡힘 (첫 판 생존 P01c → 시험 PC01i 더한 뒤 잡힘) · 봉인 파일 (194 실행기 CODE_FILES 32 · S0_SAME_FILES 7) 과 바뀐 파일 교집합 0 · 원장 PC5-01–08 · 10 · 11 = claimed_fixed.
- 구현 중 정한 것 (계획 밖 · 메인 확인 · 사전 공격 6 회차 대상): 운영자 확인 표지 = `--stage recover --ledger L --operator-confirm <n> --operator-why "<사유>"` (둘 함께 · `--ledger` 와만 · 범위 = 그 시도 폴더의 "여기서 볼 수 없는 그룹" 만 · 끝 기록에 operator 칸) · machine_id 다르면 미확인 (같아도 같은 기계 증거로 안 씀 · boot_id · pid 이름공간 · machine_id 셋 다 같을 때만 /proc) · 다시 셈 범위 (판정 · 합치기 = 입력 대상 모든 시도 · 재실행 풀기 전 = 원 시도 + 같은 바탕 앞 재실행 · 원장 파일을 바꾼 병합 아닌 커밋 = 첫 부모 역사 위) · 잘못된 주소 낱말 = 원인이 시간 초과 · 신호 · 그룹 미확인이어도 `runner_rc` · 새 멈춤 `CHAIN_EXCEPTION` (재실행 불가) · PC5-07 셈 밖 = pid 1 · 다른 실 uid · 그룹 시작 전 프로세스 (한정: su · sudo -u 로 실 uid 를 바꾼 그룹 원은 못 찾는다) · 원장 잠금 `rint_r_ledger.lock` (flock · 120 s) · 옛 시험 기대값 · 고정물 바꿈 = GR08 · AL12d · AL12c · RS06 · `gr_fake_launch` · UM19.
- ▶ 사전 공격 6 회차 (고친 diff 만 · 독립 에이전트) → 게이트 → push → Codex 회차 ② 요청서.
