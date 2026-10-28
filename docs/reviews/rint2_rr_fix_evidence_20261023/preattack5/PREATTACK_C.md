# 사전 공격 5 회차 — Rint ② RR 묶음 C + 10-28 결정 반영 (Codex 회차 ② 요청 전)

- 대상 = 가지 `claude/stoic-knuth-NObVQ` 의 `0c47df263` (기준 `5288ff3c4`) · 코드 `scripts/rint_r_chain.py` · `scripts/rint_first_result.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/check_all.sh` · 시험 다섯 · 문서 (Q9 개정 4–6 · 등록 R 10-28 블록 · §2-1 · §10-1 · §10-5 · kgy 명령 · 설명 페이지).
- 방법 = 독립 작업 트리 · 고친 사람 설명 없이 diff · 코드 · 시험 · 보고만 읽음 · 반례마다 실제 사슬 함수 또는 실경로 (사슬 `main` · bash 러너 꼴 · 가짜 payload · 실제 프로세스 그룹 · 실제 git 원장) · 설치 · 시스템 설정 · push · 게이트 실행 없음.
- 환경 = 이 컨테이너 Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · root · 4 코어.  모든 숫자 = 이 작업의 명령 출력 (로그 = 이 폴더 `logs/`).  실행으로 확인하지 않은 것 = "추정".
- 결론 한 줄 — **새 P1 은 찾지 못했다.  P2 여섯 (원장 끝 결과 줄 바꿔치기 · 자원 낱말 표 · 살아 있는 사슬의 recover · machine_id 재부팅 규칙 · 재실행 시도의 결과 전 관문 멈춤 · 요약 없는 시도 = parent_dead 고정) · P3 다섯.**  여섯 중 셋 (PC-01 · 02 · 06) 은 같은 보장 — "결과 뒤 멈춤은 자원 · 인프라 원인일 때만 재실행 · 코드 결함 꼴은 자동 재시도 안 함 (10-28)" — 을 서로 다른 길로 비켜 가고, 둘 (PC-03 · 04) 은 Codex ② "그룹 종료를 확인한 뒤에만 결과 줄 · 확인 못 하면 미확인" 을 비켜 간다.  묶음 시험 다섯은 이 판에서 다 통과했다 (§4).

## 1. 발견 (PC-NN · Codex 척도)

| id | 심각 | 한 줄 | 최소 재현 | 깨는 보장 |
|---|---|---|---|---|
| PC-01 | P2 | **원장 끝 결과 줄 바꿔치기가 판정까지 통과한다.**  판정 · 합치기 · 풀기 전 대조 (`target_ledger_problem` :3331 · `adoption` :2871) 는 결과 줄의 폴더 이름 · 요약 sha · 결과 전/뒤만 폴더와 맞추고 `status` · `stop` · `cause` · `resume_ok` 는 폴더 (요약 · 로그 · `.unchecked/`) 에서 다시 셈하지 않는다.  덧붙이기만 검사 (`ledger_history_problem` :2627) 는 첫 부모 사슬이 덧붙이기만인지 볼 뿐이라 끝 커밋 교체 (`git reset --hard HEAD~1` + 새 줄 · 또는 `merge -s ours` 로 정직한 커밋을 둘째 부모로 숨김) 를 못 본다.  실측: 정직한 결과 줄 = `stopped · post · runner_rc · resume_ok false` (ILLEGAL_ADDRESS · 10-28 "자동 재시도 안 함") → 원장 정직본에서 `--add --resume 1` = rc 3 · 끝 줄만 `cause resource · resume_ok true` 로 바꾸면 역사 검사 None · `--add --resume 1` = rc 0 · 재실행 시도 CALIBRATED (런 L01 다시 · 결정성 가정) · `ledger_verdict_check` 통과 (채택 사슬 [1, 2] · effective 2) · 원장 판정 = 원장 대조 지난 뒤 INPUT_MISSING (사다리 하나만 넣음).  `-s ours` 꼴도 역사 검사 None · 정직한 결과 커밋 = HEAD 의 조상 True · 재실행 항목 차례 문제 None.  폴더는 바이트 그대로 (한 사본만 고침).  상주 시험 AL12 의 같은 reset 꼴은 `side` 를 바꿔 잡혔다 — `cause` · `resume_ok` · `status` 만 바꾼 꼴은 시험이 없다. | `probe_real.py … R1` (출력 = `logs/` 의 probe_real.out) | Q9 §3-5 "막는 것: 결과 줄만 고쳐 쓰기" · 재실행 자격 = 원인 (등록 R §10-5 다 ⑧) · 덧붙이기만 |
| PC-02 | P2 | **자원 낱말 표가 거의 모든 cupy CUDA 오류를 `resource` 로 읽는다.**  표 (:2560) 의 `CUDARuntimeError` · `CUDADriverError` = cupy 오류 **클래스 이름**이라 모든 CUDA 오류 줄에 들어 있다 · `NOT_RESOURCE_WORDS` (:2565) 는 잘못된 주소 둘뿐.  실측 (실경로 · 가짜 러너 · 표지 뒤 rc 1): device-side assert (`cudaErrorAssert`) · `CUDA_ERROR_MISALIGNED_ADDRESS` · `CUDA_ERROR_LAUNCH_FAILED` · `cudaErrorInvalidValue` = 원인 `resource` · `resume_ok true` · `--add --resume` rc 0 · assert 꼴은 재실행 CALIBRATED · 대조 ILLEGAL_ADDRESS = `runner_rc` · rc 3.  단위 시험 (`attempt_result_line`) 에서 `CUDA_ERROR_ILLEGAL_INSTRUCTION` 도 resource.  10-28 결정의 이유 ("코드 결함일 수 있다 → 자동 재시도 안 함") 가 같은 부류에 적용되지 않는다 · 추정: CUDA 설명상 `LAUNCH_FAILED` = 커널 실행 중 예외 (잘못된 포인터 · 범위 밖 접근) 로 ILLEGAL_ADDRESS 와 같은 부류 (이 작업에서 NVIDIA 원문 대조 안 함). | `probe_unit.py … U1` · `probe_real.py … R2` | 등록 R §10-5 다 ⑧ (자동 재시도 안 함의 뜻) · REPORT_C_decisions §4 #1 보다 넓다 |
| PC-03 | P2 | **`--stage recover` 가 사슬 부모가 살아 있는지 보지 않는다.**  시작 기록에 `chain_pid` (:2453) 가 있는데 `stage_recover` (:5864) · `recover_group` (:5832) 는 끝 기록이 없거나 미확인인 시작 기록마다 표지로 찾아 SIGKILL.  실측: 살아 있는 "사슬" 프로세스 (`run_in_group` · 15 s 러너) 를 두고 recover → rc 0 · killed 1 · 끝 기록 = by recover · parent_dead · 그 사슬은 rc −9 · 원인 None · 확인 True 로 읽음 (실제 사슬이면 RUNNER_RC → 원인 `runner_rc`).  같은 바탕 폴더에서 두 시도가 돌 때 하나를 고치려고 `--out <바탕>` 으로 돌리면 살아 있는 런을 죽인다 · `--ledger` 와 함께면 recover 결과 줄 (interrupted · parent_dead) 과 사슬 결과 줄이 다툰다 (뒤 것이 "결과 줄 둘" 로 멈춤 · 폴더 sha 어긋남) — 이 뒷부분 = 추정 (코드 읽기 · 실행 안 함). | `probe_unit.py … U6` | Codex ② "부모 사망 뒤 별도 recovery" 의 전제 · 원인 기록 |
| PC-04 | P2 | **"같은 machine_id · 다른 boot_id = 재부팅 = 확인" 이 증거 없이 확인을 낸다.**  `recover_group` :5856.  machine_id (`/etc/machine-id`) 는 기계 정체가 아니다 — 복제 디스크 이미지 · 같은 이미지의 컨테이너는 같은 값을 가진다 (이 컨테이너에도 그 파일이 있다).  실측: 이 컨테이너에서 표지 프로세스 하나 (`sleep 20`) 를 띄우고 시작 기록의 host = 내 machine_id + 다른 boot_id → `confirmed true` · `why 재부팅` · `killed 0` · 표지 프로세스 그대로 살아 있음.  다른 호스트에서 도는 그룹을 공유 폴더 · 복사본에서 recover 하면 "확인" 결과 줄 → 다음 시도 · 재실행이 열린다.  추정: kgy · gabia 의 machine-id 가 같은지는 모름. | `probe_unit.py … U2` | Codex ② "확인 못 한 호스트 = 미확인 · 다음 시도 채택을 막는다" · REPORT_C_decisions §4 #6 ("구현 그대로") 보다 넓다 |
| PC-05 | P2 | **재실행 시도가 단계 안 관문 (결과 전) 에서 멈추면 재실행 사슬이 그대로 끝난다 (보수 쪽 오거부 · 대상 영구 멈춤).**  `adoption` 의 재실행 사슬 (:2897) 은 거부 (`rejected`) 만 건너뛰고, 돈 재실행은 결과 전 (`side pre`) 이어도 사슬 끝으로 넣는다.  풀기 전 대조 (`attempt_open`) 밖의 단계 안 관문 (`exec_check_or_stop` :4469 의 `--max-hours` · 그 밖 `ENV_SIGMA_VGCF_OVERRIDE` · 계획 숫자 블록 · 등록 해시 · S0 보고 경로 · 킷 경로 · dirty 트리 …) 에서 멈추면 `stopped · pre · gate · resume_ok false` = "마지막으로 돈 재실행이 자격 없이 멈춤" → 다시 재실행 불가 · 새 시도는 ATTEMPT_AFTER_ADOPTED.  실측: OOM 뒤 (resource · 자격) 재실행 시도에 `--max-hours 3` (계획 2) 오타 → NOT_REGISTERED · 결과 전 → 바른 인자로 `--add --resume 1` = rc 3 RESUME_NOT_ALLOWED · 대조 = 기계 오타 (풀기 전 대조 = 거부 = 건너뜀) → 다시 재실행 rc 0 · CALIBRATED.  Q9 §3-5 :140 은 "풀기 전 거부된 재실행만 건너뛴다" 라 구현은 글자 그대로다 — 단계 안 결과 전 멈춤의 처분이 설계에 없다. | `probe_real.py … R5` | "결과 전 멈춤 = 다시 할 수 있다" (Q9 §3-2 :70 · §3-5 :138) ↔ 재실행 사슬 규칙 (:140) |
| PC-06 | P2 | **요약 없는 시도의 결과 줄은 원인 = `parent_dead` 고정 — 런 로그 · 러너 rc 를 보지 않는다.**  `attempt_result_line(s=None)` :3244 (recover 가 쓴다) 는 `stop_cause` 의 낱말 대조 (`NOT_RESOURCE_WORDS`) 를 건너뛴다.  실측 ① (실경로 · 사슬을 따로 프로세스로): 런 로그에 `CUDADriverError: CUDA_ERROR_ILLEGAL_ADDRESS` 가 찍힌 것을 본 뒤 사슬 부모를 SIGKILL → recover = `interrupted · post · parent_dead · resume_ok true` → `--add --resume 1` rc 0 → 재실행 CALIBRATED — 같은 오류가 사슬이 살아 있을 때면 `runner_rc` · rc 3 (AL19c).  파일 · 원장 편집 없이 10-28 "잘못된 주소 = 자동 재시도 안 함" 을 비켜 간다 (운영자 SIGKILL · 접속 끊김 · OOM 으로 사슬만 죽어도 같다).  ② 단계 함수는 `Stop` 만 잡는다 (`stage_ladder` :4516–4523) → 팔 읽기 중 사슬 예외 (KeyError 주입) = 요약 없음 → 같은 `parent_dead · resume_ok true` (결정적 결함이면 재실행도 같은 곳에서 죽어 시도 수만 쓴다 = 추정). | `probe_real.py … R6` · `… R3` · `probe_unit.py … U5` | 등록 R §10-5 다 ⑧ (자동 재시도 안 함) · 원인 기록 |
| PC-07 | P3 | **그룹 원 찾기가 "주 스레드만 끝난 프로세스" 를 못 본다.**  `group_members` (:2345) 는 상태 Z 를 버리고 (:2361) environ 을 못 읽는 프로세스를 그냥 건너뛴다 (:2364).  실측: 러너가 뒤로 띄운 파이썬 (주 스레드 `pthread_exit` · 다른 스레드는 2 s 뒤 파일) → `run_in_group` rc 0 · `confirmed true` · `left []` · `killed 0` 뒤에 그 파일이 생김.  (env 를 지운 자식 = 이미 적힌 한정 · rc 0 경로는 원 pgid `killpg` 를 하지 않으니 그 한정이 그대로 남는다.)  권한으로 environ 을 못 읽는 그룹 원 (setuid) = 없음으로 셈 — root 라 재현 못 함 (추정).  실제 payload 에서 가능성은 낮다 (추정).  REPORT_C §7 MG04 의 "동작이 같다" 는 맞지만 그 밑에 이 구멍. | `probe_unit.py … U3` | Q-K "종료된 그룹의 snapshot" · 끝 기록 = 그룹 종료 확인 |
| PC-08 | P3 | **원장 덧붙임이 잠금 · 되돌림 없이 "파일에 쓰기 → git add → commit" 이다.**  `ledger_append` :2750.  (a) 동시 `--add` 둘 = 12 회 중 1 회 HEAD 에 같은 번호 항목 둘 (원장 영구히 못 읽음 · 한쪽은 rc 3 인데 줄은 커밋됨) (b) `git add` 실패 (index.lock) 뒤 작업 파일에 커밋 안 된 줄이 남아 다음 모든 원장 읽기 = ATTEMPT_LEDGER_MISMATCH ("커밋하지 않은 고침") — 손으로 git 을 만지는 것 말고 길이 없다.  여러 기계가 한 원장을 쓰는 방식은 문서에 없다 (추정 · 두 대 단위 나눔 §6). | `probe_unit.py … U4` · `… U7` | 원장 = 덧붙이기만 · 운영 연속성 |
| PC-09 | P3 | **"검사 실패 흔적" 이 쓰는 중 · 검사 전에 죽은 payload 도 센다.**  `result_trace_name` :2796 = `p2_*` + `.json` 포함이면 다 → `.unchecked/` 의 `p2_….json.part` (payload 원자적 쓰기 중 시간 초과 · 신호) · 러너 검사 전에 죽은 완성 `p2_….json` = `resume_ok false` (원인 `timeout` 그대로) → 결과 뒤 채택 · 재실행 없음 = 대상을 잃는다 (보수 쪽 · 거짓 수용 없음). | `probe_unit.py … U8` | 재실행 자격 (자원 · 인프라 원인) |
| PC-10 | P3 | **다시 판정이 같은 바탕 폴더의 나중 시도 하나로 깨진다.**  `ledger_verdict_check` :3414 = 원 판정 커밋의 원장에 없는 폴더 = 멈춤.  실측: 원장 주 캠페인 판정 → 다시 판정 REVERIFY_SAME → 같은 바탕에 다른 대상 (`ladder:P0:FIBRE`) 시도 하나 (풀기 전 거부) → 다시 판정 REVERIFY_DIFF (rc 1) · 원인 "원장에 없는 시도 폴더 ['attempt_4'] (항목 4)".  판정 입력 · 원장 접두는 그대로 · 보수 쪽.  ㉕ (경로 묶임) 와 다른 원인. | `probe_real.py … R4` | 다시 판정 = 같은 입력 → 같은 판정 |
| PC-11 | P3 | **보고 숫자의 원자료가 리포 밖이다.**  변이 207 · kgy 2 회차 11 묶음 · 결정성 9/9 · 회귀 21 묶음 = 메인 스크래치 (`docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_C.md` §13 스스로 "컨테이너가 바뀌면 없다").  이 작업은 같은 컨테이너라 읽어 대조했고 다 맞았다 (§3) — Codex 는 못 본다. | — | 증거 귀속 |

이번에 넓지 않은 것 (§4 "표가 정하지 않은 어긋남" 의 열린 넷 = #4 · #5 · #8 · #9): 범위가 적힌 그대로임을 코드로 확인 (#4 = 판정 `--ledger` 필수는 규칙 · 사슬 인자는 선택 · 등록 R :580 이 스스로 적음 · #5 = 시험 고정물 `reg_with` 가 등록 사본 끝에 블록을 덧붙임 · #8 = `MergeFetch.finish` 가 요청 안 된 대상의 대조 실패를 UNIT_EXTRA · #9 = 등록 R 의 "구현 = 묶음 C 코드 (진행 중)").  #3 (GPU `--resume` 규칙만) 은 PC-02 의 재실행 실측에서 그대로 확인.  넓어진 것 = #1 → PC-02 · #6 → PC-04.

## 2. 변이 — 살아남은 것 (REPORT_C §7 의 207 목록에 없는 가드만 골라 23 · 기존 시험 부분집합)

23 개 중 잡힘 3 (X10 = AL19c · X13 = EP04 · X23 = AL16) · **살아남음 20**.  변이마다 원본에서 다시 쓰고 `scripts/test_rint_r_chain.py --only <접두>` (사본 트리 · 결과 = `logs/mut_pa5_res.json`).  "뒤 방어" = 같은 일을 뒤 단계 (판정 · 덧붙이기 전 parse) 가 다시 막는다고 코드를 읽어 판단한 것 (실행 확인 아님 = 추정).

| 변이 | 끈 가드 (자리) | 돌린 시험 | 결과 | 판단 |
|---|---|---|---|---|
| X01 | 합치기 — 원장 역사 (덧붙이기만) 검사 (`stage_merge`) | UM 23 | 생존 | 뒤 방어 (판정 역사 검사 ML45) · 합치기 단계 자체는 시험 없음 |
| X02 | 합치기 — `--max-hours` · 기계 허용 · 판 봉인 (`exec_check_or_stop`) | UM · EP 34 | 생존 | 판정이 단계 기계 · 판을 다시 봄 · 합치기 `--max-hours` 는 시험 없음 |
| X03 | 합치기 — 계획 숫자 블록 대조 | UM · EP 34 | 생존 | 뒤 방어 (판정 M13) |
| X04 | 합치기 — 원장 머리 계획 = 사다리 계획 | UM 23 | 생존 | 뒤 방어 (원장 항목 계획 = 머리 · 풀기 전 대조) |
| X05 | 판정 — 최대 시도 수 (ATTEMPT_LIMIT) | AL · UM 53 | 생존 | `--add` · 풀기 전 대조가 먼저 막음 · 손 원장에만 뜻 · 시험 없음 |
| X06 | 판정 — 같은 대상 입력 둘 (DUPLICATE_RUN) | AL 30 | 생존 | 뒤 방어 추정 (판정 계산기의 같은 법칙 둘) |
| X07 | `--add` — `--plan` sha = 머리 계획 | AL 30 | 생존 | 같은 동작 (덧붙이기 전 `ledger_parse` 가 같은 이름으로 멈춤) |
| X08 | `--init` — 봉인 전 계획 거부 | AL · EP 41 | 생존 | 다음 `--add` 가 거부 · 한 번뿐인 `--init` 을 버린다 · 시험 없음 |
| **X09** | 결과 줄 꼴 — `rejected` 인데 결과 뒤 · 재실행 자격 | AL 30 | **생존** | **실제 구멍** — 이 가드가 PC-01 류 (끝 줄 교체) 로 채택 시도를 `rejected` 로 지우는 길을 막는 유일한 자리 · 시험 없음 |
| X11 | recover `--ledger` — 폴더 ↔ 원장 항목 (대상 · 시작 커밋 조상) | AL13 · AL14 · RS02 | 생존 | 뒤 방어 (판정 attempt.json 대조) |
| X12 | 원장 꼴 — 항목 `resume_of` (같은 대상 앞 항목) | AL · RS 36 | 생존 | `--add` 가 먼저 막음 · 손 원장에만 뜻 |
| X14 | 재실행 복사 — 복사 자리가 이미 있음 | RS 6 | 생존 | 같은 동작 (copytree 실패 = RESUME_NOT_ALLOWED) |
| X15 | 원장 읽기 — 원장 파일이 링크 | AL 30 | 생존 | 시험 없음 |
| X16 | 합친 예측 판정 — 단위 런 두 번 사용 | UM 23 | 생존 | 요청 칸 대조가 대신 막을 것으로 추정 |
| X17 | 합치기 — 사다리 입력 = 이 원장 채택 사다리 시도 | UM 23 | 생존 | 뒤 방어 (판정 입력 사다리 = 원장 채택 · PREDICT_LADDER_MISMATCH) |
| **X18** | recover `--ledger` — 거부 기록 폴더 → `rejected` 결과 줄 | AL · RS · GR 50 | **생존** | **실제 구멍** — 거부 기록만 쓰고 결과 줄 전에 죽은 **재실행** 시도를 `interrupted · pre` 로 쓰면 PC-05 처럼 재실행 사슬이 끝난다 · 시험 없음 |
| X19 | 넘침 점 풀기 전 — 결정 기록 변이 | UM 23 | 생존 | 끝 합치기의 변이 대조 (X21) 에 기댐 |
| X20 | 넘침 점 풀기 전 — 결정 기록 계획 sha | UM 23 | 생존 | 끝 합치기 대조에 기댐 |
| X21 | 끝 합치기 — 결정 기록 변이 · 계획 · 사다리 요약 sha | UM 23 | 생존 | 점 풀기 전 대조 (X19 · X20 · MU28) 에 기댐 — 서로 기대어 둘 다 시험 없음 |
| X22 | `--add` — 지금 코드 dirty · 판 봉인 | AL · EP 41 | 생존 | 단계 안 관문이 다시 봄 (그 멈춤이 재실행 시도면 PC-05) |

REPORT_C §7 의 생존 둘 (코드 읽기 · 실행 안 함): MG04 = 같은 동작 판단 맞음 (Z 프로세스는 environ 이 비어 표지가 안 보인다 · 그러나 PC-07 의 구멍은 그 밑) · ML09 = 같은 동작 판단 맞음 (끝 줄바꿈 없으면 마지막 줄 JSON 이 깨져 같은 멈춤).

## 3. 주장 대조 (파일:줄 · 주장 · 잰 것)

| 파일:줄 | 주장 | 잰 것 |
|---|---|---|
| `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md`:151 | "막는 것: … 결과 줄만 고쳐 쓰기 …" | 끝 결과 줄의 `cause` · `resume_ok` 만 바꿔 다시 커밋 = 판정 원장 대조 통과 (PC-01) |
| 같은 파일 :152 · `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_C.md`:213 | "못 막는 것: 사람이 폴더 파일 · 멈춤 기록 · 결과 줄을 **함께** …" · "Q-D: 그림자 런 · **모든 사본**의 일관 편집은 못 막습니다" | 원장 한 사본 (끝 줄) 만으로 충분 · 폴더 바이트 그대로 (PC-01) — 한정 문구가 실제보다 좁다 |
| 같은 파일 :70 · :138 · :140 | "… (그 시도는 결과 전이라 다시 할 수 있다)" · "결과 전 시도 … 는 재실행이 아니라 새 시도다" · "풀기 전 거부된 재실행 항목은 건너뛴다 … 마지막으로 돈 시도가 … 재실행 자격 없이 멈췄으면 더 재실행할 수 없다" | 세 문장이 재실행 시도의 단계 안 결과 전 멈춤에서 서로 다른 답 — 구현 = :140 (재실행 사슬 끝 · 다시 못 함 · 새 시도도 ATTEMPT_AFTER_ADOPTED) (PC-05) |
| `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`:591 | ⑧ "… 표에 없는 낱말 = 재실행 불가 쪽" · ILLEGAL_ADDRESS = 코드 결함일 수 있다 → 자동 재시도 안 함 | cupy CUDA 오류 줄은 늘 표 낱말 (클래스 이름) 을 담는다 · assert · misaligned · launch failed · invalid value = resource (PC-02) |
| 같은 파일 :585 | ⑥ "같은 기계 (machine_id) 의 다른 부팅 = 확인 (재부팅 — 그 부팅의 프로세스는 없다)" | 같은 machine_id · 다른 boot_id · 살아 있는 표지 프로세스 → confirmed true (PC-04) |
| `scripts/rint_r_chain.py`:2441 (run_in_group docstring) · `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_C.md` §0 표 | 끝 기록 = 그룹 종료 확인 뒤 · Codex ② 닫음 (claimed) | 주 스레드만 끝난 프로세스 = 확인 true 뒤 파일 (PC-07) · 살아 있는 사슬도 recover 가 죽임 (PC-03) · machine_id 규칙 (PC-04) — ② 는 부분 |

맞은 것 (이 작업의 명령 출력): 묶음 C 커밋 `2c1308bb2`..`db97d0644` = 15 · 다 `author 10-27 approved bundle C` · 공동 저자 줄 · `cherry picked` 줄 (15/15) · 바뀐 파일 9 (다 `scripts/`) · 봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) ∩ 바뀐 파일 = 0 · S0_SAME_FILES 7 ∩ = 0 · chain 검사 284 → 384 (+100 = AL 28 · EP 11 · GR 14 · NP 8 · OR 6 · RS 6 · RV 4 · UM 23) → 386 (AL19b · AL19c) · RESOURCE_WORDS 10 → 9 (`191ad37b6`) · 등록 R 의 계획 숫자 블록 표지 = 0 개 · 시험 시간 (chain 393.1 s ↔ 주장 392 s · e2e 517.5 s ↔ 517 s) · 스크래치 원자료 대조: 변이 207 · 잡힘 205 · 생존 2 (MG04 · ML09) · kgy 2 회차 11 묶음 통과 (chain 384/384 · e2e 39/39 · Python 3.8.20) · 결정성 sid_fp 9/9 · σ 비트 같음 9/9.

## 4. 이 판에서 돌린 시험 (`0c47df263` · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · BLAS 스레드 1 · nice 19 · 한 번씩)

| 시험 | 결과 | 초 |
|---|---|---|
| `scripts/test_rint_first_result.py` | 9/9 PASS | 1 |
| `scripts/test_ca_s0_census.py` | 167 PASS · 0 FAIL | 22 |
| `scripts/test_ca_ext_runner.py` | 151 PASS · 0 FAIL | 158 |
| `scripts/test_rint_r_chain.py` | 386/386 PASS | 393.1 |
| `scripts/test_rint_r_chain_e2e.py` | 39 PASS · 0 FAIL | 517.5 |
| `webapp/test_rint_explainer_page.py` (덤) | 88/88 PASS | — |
| `webapp/test_ca_ext_labels.py` (덤) | 93 PASS · 0 FAIL | — |

## 5. 원장 등재 후보 (적용 안 함)

```text
{"id": "PC5-01", "severity": "P2", "status": "open", "owner": "claude", "found_by": "사전 공격 5 회차 (10-28 · 0c47df263 · 독립 작업 트리)", "opened_in": "docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/PREATTACK_C.md", "title": "원장 끝 결과 줄 바꿔치기 (reset · amend · merge -s ours) = 판정 통과 — 결과 줄의 status · stop · cause · resume_ok 를 폴더에서 다시 셈하지 않고 역사 검사는 첫 부모 끝 커밋 교체를 못 본다 (runner_rc → resource · --resume 받음 · 채택 사슬 [1, 2])", "note": "닫는 조건 후보 = 판정 · 합치기 · 풀기 전 대조가 attempt_result_line 을 폴더에서 다시 셈해 결과 줄 (utc · by 뺀 칸) 과 대조 + 시험 (끝 줄 교체 · -s ours)"}
{"id": "PC5-02", "severity": "P2", "status": "open", ..., "title": "자원 낱말 표의 CUDARuntimeError · CUDADriverError (cupy 클래스 이름) 가 모든 CUDA 오류를 resource 로 — device-side assert · misaligned · illegal instruction · invalid value · launch failed = 재실행 자격 (10-28 '코드 결함 = 자동 재시도 안 함' 의 부류)"}
{"id": "PC5-03", "severity": "P2", "status": "open", ..., "title": "--stage recover 가 시작 기록의 chain_pid 생존을 보지 않고 살아 있는 사슬의 러너 그룹을 죽인다 (끝 기록 parent_dead ↔ 사슬은 rc −9 · 원인 None)"}
{"id": "PC5-04", "severity": "P2", "status": "open", ..., "title": "recover 호스트 규칙 '같은 machine_id · 다른 boot_id = 재부팅 = 확인' — machine_id 는 기계 정체가 아님 (복제 이미지 · 컨테이너) · 살아 있는 표지 프로세스를 두고 confirmed true"}
{"id": "PC5-05", "severity": "P2", "status": "open", ..., "title": "재실행 시도가 단계 안 관문 (결과 전 · 예 --max-hours 오타 NOT_REGISTERED) 에서 멈추면 재실행 사슬 끝 = 자격 없음 → 대상 영구 멈춤 (풀기 전 대조 거부는 건너뜀 · adoption 이 side pre 재실행을 사슬에 넣음)"}
{"id": "PC5-06", "severity": "P2", "status": "open", ..., "title": "요약 없는 시도의 결과 줄 (recover) = 원인 parent_dead 고정 · 런 로그의 NOT_RESOURCE 낱말 · 러너 rc 를 보지 않음 — ILLEGAL_ADDRESS 를 본 뒤 사슬 부모 SIGKILL → resume_ok true · 재실행 CALIBRATED · 사슬 예외 (Stop 아님) 도 같은 줄"}
{"id": "PC5-07", "severity": "P3", "status": "open", ..., "title": "group_members 가 상태 Z (주 스레드만 끝남 · 다른 스레드 삶) · environ 못 읽는 그룹 원을 없음으로 셈 · rc 0 경로는 원 pgid killpg 없음 → 확인 true 뒤 늦은 파일"}
{"id": "PC5-08", "severity": "P3", "status": "open", ..., "title": "ledger_append 잠금 · 되돌림 없음 — 동시 --add 둘이 같은 번호 항목 둘을 커밋 (1/12) · git add 실패 뒤 커밋 안 된 줄이 남아 원장 전체 멈춤"}
{"id": "PC5-09", "severity": "P3", "status": "open", ..., "title": "검사 실패 흔적 = .unchecked/ 의 p2_*.json* 전부 — 쓰는 중 (.part) · 러너 검사 전 죽음도 resume_ok false (원인 timeout)"}
{"id": "PC5-10", "severity": "P3", "status": "open", ..., "title": "다시 판정이 같은 바탕 폴더의 나중 시도 (다른 대상) 하나로 REVERIFY_DIFF (원 판정 커밋의 원장에 없는 폴더)"}
{"id": "PC5-11", "severity": "P3", "status": "open", ..., "title": "REPORT_C 숫자 (변이 207 · kgy 11 묶음 · 결정성 9/9 · 회귀 21 묶음) 의 원자료가 리포 밖 (메인 스크래치)"}
```

(`...` = found_by · opened_in · owner 는 PC5-01 과 같다.)

## 6. 확인하지 못한 것 · 이유

- 실제 GPU · cupy 오류 문구 (PC-02 의 오류 줄 = cupy 꼴로 만든 가짜 · 이 컨테이너에 GPU 없음) · CUDA 오류 뜻 = 기억 (NVIDIA 원문 대조 안 함 = 추정).
- kgy · gabia 의 `/etc/machine-id` 가 같은지 (PC-04 의 실제 가능성) — 다른 호스트에 접속하지 않았다.
- 권한 다른 그룹 원 (setuid · 다른 사용자) 의 environ 읽기 실패 (PC-07 둘째 반) — 이 컨테이너는 root.
- PC-03 의 원장 쪽 결과 (recover 결과 줄 ↔ 살아 있는 사슬 결과 줄 다툼) — 실경로로 두 프로세스를 겹쳐 돌리지 않았다 (코드 읽기 = 추정).
- 실침대 · 실제 러너 · payload 의 `.part` 창 크기 (PC-09 빈도) · 동시 사용 빈도 (PC-08).
- Python 3.8 (kgy 판) 에서 묶음 시험 · 탐침 — 지시대로 3.11 한 번만.  kgy 판 결과는 메인 스크래치 기록만 대조 (§3).
- Q9 시간표 산술 (`q9_time_budget.py`) · 웹앱 다른 시험 · 규율 검사 — 범위 밖으로 두었다.
- 변이는 고른 23 개 · 그 가드를 볼 법한 시험 접두만 돌렸다 (전체 시험 아님).
- `scripts/check_review_findings.py --ban-sweep` 전체 = 이 컨테이너에서 900 s (nice 19) 안에 끝나지 않아 끊겼다 → 대신 이 폴더 파일만 `docs/reviews/claims.json` 의 금지 문자열 42 개와 대조 (붙여 쓴 꼴 포함) = 0 건.  `scripts/check_doc_refs.py --quiet` · `scripts/check_review_findings.py` = rc 0.

## 7. 근거 파일 (이 폴더)

- 탐침: `probe_unit.py` (U1–U8 · 실제 사슬 함수) · `probe_real.py` (R1–R6 · 시험 틀 `scripts/test_rint_r_chain.py` 의 고정물 · 가짜 러너를 불러 쓴다 · 그 파일은 고치지 않음 · 가짜 러너 원문에 고장 둘만 이 프로세스 안에서 더함) · 변이: `mutate_pa5.py`.
- 다시 돌리기: `python3 docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/probe_unit.py <임시 폴더> [U1,…]` · `python3 docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/probe_real.py <임시 폴더> [R1,…]` (리포 꼭대기에서 · probe_real 한 번 실측 2.9–9.7 s).
- 로그: `logs/` (시험 요약 · 탐침 출력 · 변이 결과 JSON).
