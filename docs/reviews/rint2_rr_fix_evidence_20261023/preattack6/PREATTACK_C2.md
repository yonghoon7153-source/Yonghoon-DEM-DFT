# 사전 공격 6 회차 — Rint ② PC5 수정 (`b9fd47d7b` · `6bb3c064f` · `43a8abcaa` · `87a00ef46`) · **중간 보고 (10-30 · 일시 중지)**

> ⏸ **중간 보고 (10-30 · 일시 중지)** — 메인 요청 (10-30 · 1저자 50kg 급한 작업에 CPU 전부) 으로 무거운 실행 (묶음 시험 · 변이) 을 멈추고 지금까지 잰 것만 적는다.
> 아직 안 돌린 것 = §5.  이 보고의 발견 · 판단은 **이 판 실측 + 코드 읽기** 까지이고, 변이 시험 (§3) 은 하나도 돌리지 않았다.

- 대상 = `4c69070ad` (PC5 수정 네 커밋 포함) · 코드 `scripts/rint_r_chain.py` · 시험 `scripts/test_rint_r_chain.py` · `scripts/test_rint_r_chain_e2e.py` · 문서 (등록 R §10-5 아 · Q9 개정 7 · 수정 계획 Q1–Q3).
- 방법 = 독립 작업 트리 (`preattack6-rint`) · 고친 사람 설명 (증거 README) 은 주장으로만 읽음 · 반례마다 실제 사슬 함수 · 실경로 (사슬 `main` · 가짜 러너 bash + 파이썬 · 실제 프로세스 그룹 · 실제 /proc · 실제 git 원장).  사슬 · 시험 파일은 고치지 않았다.
- 환경 = 이 컨테이너 · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · root · 커널 6.18.44 · `fs.suid_dumpable` 0 · BLAS 스레드 1 · nice 10.  uid 실측 (§1 PC6-01) 만 root 로 시작해 자식을 uid 65534 (nobody) 로 내렸다 (설치 · 시스템 설정 없음).
- 결론 한 줄 (중간) — **새 P1 하나 (조건부 · 거짓 수용 아님 · 캠페인 차단 위험) · P2 하나 · P3 여섯 (그중 둘 = 미실행 · 코드 읽기)**.  묶음 시험 두 개 (사슬 407 · 끝-끝 40) 는 이 판에서 다 통과했다 — 아래 반례는 그 시험들이 다루지 않는 꼴이다.

## 0. Codex 회차 ② 에서 닫을 수 있는 것 / 닫지 않는 것 (중간 판단)

| 구분 | 항목 | 근거 (이 회차) |
|---|---|---|
| 반례를 아직 못 찾음 (닫을 후보 · 범위 한정) | PC5-01 원 반례 (끝 줄 reset · amend · merge -s ours) · PC5-03 (산 사슬 recover 안 함) · PC5-04 (다른 부팅 = 미확인 + 운영자 표지) · PC5-05 (결과 전 재실행 건너뜀) · PC5-10 · X09 · X18 | 상주 시험 PC01 · PC01i · PC01m · PC02 · PC05 · PC06 · PC06b · GR08 · PC07 · PC16 · PC12 · PC13 = 전체 묶음 안에서 통과 (§4) · 코드 읽기에서 반례 없음 — ⚠ 이 넷에 대한 독립 변이 (§3) 는 미실행 |
| 닫지 않음 | PC5-07 (그룹 원 찾기) | **PC6-01** — 같은 실 uid 의 environ 못 읽는 무관 프로세스 (ssh 로그인 · setuid · agent 꼴) 가 끝난 런을 GROUP_UNCONFIRMED 로 · recover 도 막힘 |
| 닫지 않음 | PC5-02 · PC5-06 (같은 낱말 규칙) | **PC6-02** — 1저자 Q2 의 "그 밖 CUDA 오류 = 자동 재실행 없음" 이 러너 rc 1 길에서만 · 시간 초과 · 신호 · 그룹 미확인 · 부모 사망 길 = 재실행 자격 (42 중 36) · **PC6-03 · 05 · 06** |
| 닫지 않음 | PC5-08 (덧붙임 되돌림) | **PC6-04** — 덧붙임 중 SIGTERM · SIGHUP · SIGKILL = 되돌림 없음 → 원장 전체 멈춤 (등록 R ⑧ 의 "신호 = 되돌림" 은 SIGINT 만) |
| 그대로 한정 | PC5-09 (wontfix) | 이 회차 안 건드림 |
| 미확인 | 숫자 주장 중 first_result · census · ext_runner · 웹앱 · kgy 3.8 · 변이 32/32 | §2 · §5 (일시 중지로 안 돌림) |

## 1. 발견 (PC6-NN · 이 회차 척도: P1 = R 캠페인이 기대는 보장을 깸 · P2 = 반례가 관문을 지나거나 주장이 거짓 · P3 = 문구 · 견고성)

| id | 심각 | 한 줄 | 재현 (이 판 실측) | 깨는 보장 · 주장 | 최소 고침 |
|---|---|---|---|---|---|
| **PC6-01** | **P1 (조건부)** | **PC5-07 고침이 새 거짓 멈춤을 만들었다 — 사슬과 같은 실 uid 이고 environ 을 그 uid 가 못 읽는 무관 프로세스 하나가 런 도중 생기면, rc 0 으로 끝난 런의 그룹 확인이 미확인 (GROUP_UNCONFIRMED) 이 되고 그 프로세스가 사는 동안 recover 도 확인하지 못한다.**  `group_members` (:2399–2456) 는 못 읽는 프로세스를 pid 1 · 다른 실 uid (사슬 root 아님) · 그룹 시작 전 프로세스만 셈 밖으로 두고 나머지는 "확인 불가 (None)".  그런 프로세스 = ① ssh 로그인의 `sshd: user@pts/N` · scp/rsync 의 `sshd: user@notty` (root 에서 setresuid 로 사용자 uid · 자격 바꿈 = dumpable 0) ② setuid 프로그램을 사용자가 띄운 프로세스 (실 uid = 사용자 · 유효 uid 0) ③ `prctl(PR_SET_DUMPABLE, 0)` 하는 agent (ssh-agent · gpg-agent).  `group_settle` (:2487) 은 None 이면 그 자리에서 (False, None, …) 를 돌려 **읽을 수 있는 그룹 원도 죽이지 않는다**.  `Runner._execute` (:3999) 는 확인 False = Stop GROUP_UNCONFIRMED (팔을 읽지 않음) → `attempt_close` = 결과 줄 없음 (ATTEMPT_OPEN). | `probes/probe6_uid.py` (로그 `logs/probe6_uid.out`): 세 꼴 구경꾼 (실 uid 65534 · 표지 env 없음) 의 environ = uid 65534 가 읽으면 PermissionError errno 13 · `group_members` (그룹 시작 뒤 생김) = **None** 셋 다 · (그룹 시작 전) = [] · (구경꾼 없음) = [] · `run_in_group(bash sleep 4)` 도중 1.5 s 에 구경꾼 → rc 0 · 원인 None · **확인 False** · left None (대조 = 구경꾼 없음 → 확인 True) · 사슬 부모가 죽은 뒤 `--stage recover` (uid 65534) = **rc 3** · 끝 기록 by recover 확인 False · 사유 "/proc 를 못 읽는다 · environ 을 못 읽는 그룹 원 후보" (어느 pid 인지 없음) → 구경꾼을 죽인 뒤 recover = rc 0 확인 | `group_members` 설명문 (:2405–2408) "다른 실 uid 프로세스 = 셈 밖 … **다른 터미널의 sudo 같은 프로세스로 확인이 늘 막히지 않게**" — setuid 프로그램은 띄운 사용자의 실 uid 를 그대로 가진다 (②) · ssh · agent 도 같은 실 uid.  R 캠페인: 끝난 GPU 런이 GROUP_UNCONFIRMED 로 멈추면 등록 R §10-5 라 ("멈춘 GPU 런은 재실행하지 않는다 · 결과 뒤 멈춤 = 그 대상의 결과") 로 그 대상 = STOPPED → 주 판정 = 판정 없음.  ⚠ 조건 (추정 · kgy 실측 아님): kgy 사슬이 root 가 아닌 사용자로 돈다 · 런 (수 시간) 도중 그 사용자가 ssh · scp 로 들어온다 · sudo 의 실제 자격 이력은 실행 안 함.  보수 쪽 (거짓 수용 없음) · 활성 (liveness) 결함 | 못 읽는 프로세스를 uid 가 아니라 **계보로** 그룹에 붙인다 — 사슬 = `PR_SET_CHILD_SUBREAPER` (고아가 사슬로 붙음) · 그룹 = 표지 env ∪ 러너 pid 의 자손 (`/proc/<pid>/stat` ppid 사슬) · 못 읽는 프로세스는 자손일 때만 확인 불가 · None 이어도 찾은 그룹 원은 먼저 죽인다 · 사유에 pid 를 적는다 · 상주 시험 = 이 탐침 꼴 (root 일 때만 · 아니면 건너뜀 표지) |
| **PC6-02** | **P2** | **1저자 Q2 "그 밖 CUDA 오류 (클래스 이름만 있는 줄 포함) = 자동 재실행 없음 (runner_rc)" 이 요약 있는 길의 러너 rc ≠ 0 (그룹 원인 없음) 에서만 선다 — 시간 초과 · 신호 · 그룹 미확인 · 사슬 부모 사망 (recover) 길에서는 같은 로그 글이 재실행 자격이 된다.**  `stop_cause` (:3493) · `orphan_cause` (:3520) 는 그 길에서 `NOT_RESOURCE_WORDS` (잘못된 주소 둘) 만 본다.  PC5-06 (사전 공격 5 회차 P2) 이 잘못된 주소에 대해 막은 길을 Q2 가 늘린 부류 (assert · misaligned · illegal instruction · launch failed · invalid value) 는 그대로 지난다. | 단위 (`probes/probe6_unit.py` U1 · 실제 `attempt_result_line`): Q2 부류 여섯 × 길 일곱 = 42 → **36 이 resume_ok True** · False = "RUNNER_RC rc 1 · 그룹 원인 없음" 여섯뿐.  실경로 (`probes/probe6_real.py` R1): 표지 뒤 `CUDADriverError: CUDA_ERROR_LAUNCH_FAILED` 를 본 뒤 사슬 부모 SIGKILL → recover --ledger = `interrupted · post · parent_dead · resume_ok true` → `--add --resume 1` **rc 0** → 재실행 CALIBRATED → 채택 사슬 [1, 2] · effective 2 → 원장 판정 대조 통과 (멈춤 INPUT_MISSING = 사다리 하나만 넣음 · 원장 멈춤 아님).  대조 R1c (사슬 산 채 rc 1) = runner_rc · `--add --resume` rc 3.  R2 (같은 줄 뒤 사슬 SIGTERM) = `stopped · post · signal · true` → `--add --resume` **rc 0** | 수정 계획 Q2 · 등록 R §10-5 아 ② ("그 밖 CUDA 오류 … = 원인 runner_rc (자동 재실행 없음)" · "같은 낱말 규칙 = 요약 있는 길 · 요약 없는 길 (recover) 모두") — 다 ⑧ 의 뜻 (코드 결함일 수 있다 → 자동 재시도 안 함) | 분류기 하나 — 멈춘 런 로그에 다섯 메모리 · 디스크 낱말이 아닌 CUDA 오류 표지 (`CUDA_ERROR_\w+` · `cudaError\w+` · `CUDARuntimeError` · `CUDADriverError` 에서 다섯 낱말 뺀 것) 가 있으면 **모든 길** (rc · 시간 초과 · 신호 · 그룹 미확인 · recover by recover / by chain) 에서 runner_rc · U1 표 (42) 를 상주 시험으로 · R1 · R2 꼴 실경로 시험 |
| PC6-03 | P3 | **운영자 Ctrl-C (SIGINT) 가 그 대상을 영구히 잃게 한다 — SIGTERM · SIGKILL 은 재실행 자격인데 SIGINT 만 사슬 결함으로 읽힌다.**  `_signal_handlers` (:2519) 는 SIGTERM · SIGHUP 만 걸고, SIGINT = KeyboardInterrupt → `run_in_group` 원인 'exception' → (요약 없음) recover → `orphan_cause` = chain_exception.  PC5-06 앞 (옛 = 요약 없는 시도는 늘 parent_dead) 에는 재실행 자격이었다 (코드 읽기).  때에 따라 다르다 — 런 사이 (팔 읽기 중) Ctrl-C = 끝 기록이 다 rc 0 → parent_dead (자격). | `probes/probe6_real.py` R3 (보통 줄 · 러너 기다림 중 신호): SIGINT → 사슬 rc −2 · 결과 줄 없음 → recover = `interrupted · post · chain_exception · false` → `--add --resume` rc 3 / SIGTERM → `stopped · post · signal · true` → rc 0 / SIGKILL → recover = `interrupted · post · parent_dead · true` → rc 0 | 등록 R §10-5 나 ⑫ · 아 ⑥ (사슬 예외 = 코드 결함 · 재실행 불가) — 운영자 중단은 코드 결함이 아니다 · 같은 중단의 신호 셋이 다른 답 | SIGINT 도 `_signal_handlers` 에 (ChainSignal → 'signal') · 또는 `run_in_group` 이 KeyboardInterrupt 를 'signal' 로 · 시험 = R3 꼴 |
| PC6-04 | P3 | **원장 덧붙임 중 신호 (SIGTERM · SIGHUP · SIGKILL) = 되돌림 없음 → 커밋 안 된 줄이 색인에 남아 모든 원장 도구가 멈춘다.**  `ledger_append` (:2966) 의 되돌림은 파이썬 예외 (BaseException) 일 때만 돈다 · 사슬은 SIGTERM · SIGHUP 처리기를 런 기다림 중에만 건다 (덧붙임 중 = 기본 동작 = 즉시 종료). | `probes/probe6_real.py` R4 (로그 `logs/probe6_real_R4.out` · `--add` 의 `git commit` 직전에 그 신호): SIGTERM · SIGHUP · SIGKILL → 자식 rc −15 · −1 · −9 · `git status --porcelain` = `M  rint_r_attempts.jsonl` · `ledger_now` = ATTEMPT_LEDGER_MISMATCH (작업 파일 ≠ HEAD) · 다음 `--add` rc 3 (손으로 git 을 만지기 전까지) / SIGINT → 되돌림 · 깨끗 · 다음 `--add` rc 0 (n=1).  ⚠ `logs/probe6_real.out` 의 첫 R4 줄은 무효 (자식이 시험 고정물 HERE 없이 돌아 덧붙임 전 CODE_PIN_MISMATCH rc 3) — `probe6_real_R4.out` 이 대신한다 | 등록 R §10-5 아 ⑧ "`git add` · `commit` 실패 (index.lock · **신호**) = 작업 파일 · 색인을 읽은 판으로 되돌린다" — SIGINT 만 맞다 | 덧붙임 구간에서 SIGTERM · SIGHUP · SIGINT 를 막고 (`signal.pthread_sigmask`) 끝에서 풀기 + SIGKILL 꼴은 다음 배타 잠금 읽기가 고친다 (작업 파일 · 색인 = HEAD + 정준 한 줄이면 HEAD 로 되돌리고 기록) · 또는 git 배관 (hash-object · update-index · commit-tree · update-ref) 으로 커밋한 뒤 작업 파일을 원자적으로 |
| PC6-05 | P3 | **요약 있는 길에서 멈춘 런의 로그가 없거나 못 읽으면 낱말 규칙 없이 재실행 자격 — 요약 없는 길은 같은 꼴을 재실행 불가로 둔다.**  `run_log_text` (:3484) = 없음 · 못 읽음 → '' · `result_fields` 의 `readable` 은 요약 없는 길에만. | `probes/probe6_unit.py` U2: 로그 없음 · TIME_LIMIT (그룹 원인 timeout) → `timeout · post · true` · RUNNER_RC + signal → `signal · post · true` / 요약 없음 · by recover · 로그 없음 → `parent_dead · post · false` | 등록 R §10-5 아 ⑥ "기록 · 런 로그를 못 읽음 = resume_ok false (보수)" · ② "같은 낱말 규칙 = 두 길 모두" | 돈 런 (런 기록에 rc · seconds) 의 로그가 없거나 못 읽으면 요약 있는 길도 resume_ok false |
| PC6-06 | P3 | **사슬 자신의 메모리 부족 · 디스크 부족 = CHAIN_EXCEPTION (재실행 불가) — 러너의 같은 원인은 자원 (재실행 자격).** | `probes/probe6_unit.py` U3: `chain_exception_record` + `attempt_result_line` — MemoryError · OSError ENOSPC → 멈춤 CHAIN_EXCEPTION · 원인 chain_exception · resume_ok False | 수정 계획 Q2 의 이유 (메모리 · 디스크 = 자원) ↔ 등록 R §10-5 아 ⑥ ("기록 쓰기 결함" = chain_exception) — 이번 주 이 컨테이너 ENOSPC 이력 = 운영 위험 | `chain_exception_record` 에서 MemoryError · OSError ENOSPC · EDQUOT = 원인 resource (또는 `words_cause(str(e))`) |
| PC6-07 | P3 (추정 · 미실행) | 원 시도의 끝난 런을 복사한 재실행 시도는 늘 결과 뒤 (복사한 payload · 표지) — 첫 재실행 런이 표지 전에 러너 실패 (자원 낱말 없음) 이면 runner_rc · 재실행 자격 없음 → 사슬 끝 · 대상 멈춤.  같은 실패가 새 시도면 결과 전 (다시 할 수 있다). | 코드 읽기 (`ResumeRunner.run` · `_copy` :4065–4106 · `folder_side` :3035) · 탐침 R5 계획 (§5) | Q9 §3-5 개정 7 "결과 전으로 멈춘 재실행 = 건너뜀" 의 결과 전 판정이 복사본을 센다 | 재실행 시도의 결과 전 · 뒤 = 복사한 런 폴더를 뺀 새 흔적으로 (또는 한정으로 적기) |
| PC6-08 | P3 (코드 읽기 · 미실행) | 옆 파일 거부 기록 (`attempt_<n>.rejected.json` · 시도 폴더를 만들 수 없을 때) 을 쓰고 결과 줄 커밋 전에 죽으면 (`attempt_reject` :3235–3240 사이) `recover_ledger` (:6361 · 시도 **폴더** 만 훑음) 가 결과 줄을 못 쓴다 → 그 대상 다음 시도 ATTEMPT_ORDER_MISMATCH · 판정 "결과 줄이 없다" · 손 말고 길 없음.  (PC5 diff 밖 · 옛 결함 · X18 자리 · 두 쓰기 사이 죽음 부류) | 코드 읽기 | Q9 §3-5 "풀기 전 거부 기록이 있으면 결과 전" · 등록 R §10-5 아 ⑪ (X18 = 거부 기록 길) | `recover_ledger` 가 바탕의 옆 파일 거부 기록도 훑어 rejected 결과 줄 (attempt_reject 와 같은 칸) |

## 2. 수치 · 주장 대조

| 주장 | 자리 | 잰 것 (이 작업 · 명령 = §4) |
|---|---|---|
| `test_rint_r_chain` 407/407 | `87a00ef46` 메시지 · 수정 계획 진행 · 증거 SOURCE | **407/407 PASS (454.0 s)** · FAIL 줄 0 · PC 검사 21 개 다 통과 — ✓ |
| 끝-끝 40 (PASS · 0 FAIL) | 같은 곳 | **40 PASS · 0 FAIL (529.3 s)** — ✓ |
| first_result 9/9 · s0_census 167 · ext_runner 151 | 같은 곳 | **미실행** (일시 중지) |
| 웹앱 91/91 | `43a8abcaa` | **미실행** |
| kgy 판 11 묶음 통과 | `87a00ef46` | **미실행** (3.8 인터프리터는 있음 · 무거움) |
| 새 가드 변이 32/32 | `87a00ef46` · 수정 계획 | 증거 로그 글만 대조: `mut_pc5.log` = BASE 92/92 + 31 잡힘 + P01c 생존 · `mut_pc5_re.log` = P01c 잡힘 (PC01i) → 로그 글과 주장 같음 · **다시 돌리지 않음** · 범위 = 변이마다 그 가드의 시험 접두만 (전체 묶음 아님) |
| 고치기 전 판 7/26 PASS (`--only PC,GR08,AL12,RS06,K01`) | `b9fd47d7b` 메시지 | **미실행** |
| "다른 터미널의 sudo 같은 프로세스로 확인이 늘 막히지 않게" | `group_members` 설명문 | ✗ — PC6-01 (setuid · ssh · agent = 같은 실 uid) |
| "그 밖 CUDA 오류 … = 원인 runner_rc" · "같은 낱말 규칙 = 요약 있는 길 · 요약 없는 길 모두" | 등록 R §10-5 아 ② | ✗ — 42 중 36 이 재실행 자격 (PC6-02) |
| "`git add` · `commit` 실패 (index.lock · 신호) = 되돌린다" | 등록 R §10-5 아 ⑧ | 부분 ✗ — 신호는 SIGINT 만 (PC6-04) · index.lock · 동시 `--add` = PC15 통과 |
| "기록 · 런 로그를 못 읽음 = resume_ok false" | 등록 R §10-5 아 ⑥ | 요약 없는 길만 ✓ · 요약 있는 길 ✗ (PC6-05) |
| "자원 낱말 = 메모리 · 디스크 다섯" | 수정 계획 Q2 · 사슬 `RESOURCE_WORDS` | 사슬 표 = 다섯 그대로 ✓ (`probe6_unit.out` env 줄) · 그러나 재실행 자격은 다섯 낱말만이 아니다 (시간 초과 · 신호 · 그룹 미확인 · 부모 사망 = 원인만으로 자격 · PC6-02) |

## 3. 변이 — **미실행 (일시 중지)**

`mutate_pc5.py` 의 32 변이 밖 가드를 고를 계획이었다 (아래 "예측" = 코드 읽기로 짐작한 것 · 실측 아님 · 판정에 쓰지 않는다).

| 변이 (계획) | 끌 가드 | 예측 (추정) |
|---|---|---|
| M1 | `ledger_history_problem` 숨긴 커밋 셈에서 `--full-history` 뺌 | PC02 가 잡을 것 (경로 제한 기본 단순화가 -s ours 의 둘째 부모를 버린다) |
| M2a–e | `RECOUNT_KEYS` 에서 칸 하나씩 (status · stop · side · cause · resume_ok) | `resume_ok` 단독 제거 = 생존 가능 (그 칸만 바꾼 상주 시험 없음 · `_result_problem` 은 원인 ↔ 자격 어긋남을 안 본다 → 손 원장 줄 `cause runner_rc · resume_ok true` 가 꼴을 지난다) |
| M3 | `chain_parent_alive` 의 "부른 프로세스 자신 = False" → None | 같은 프로세스 recover 시험 (PC13 등) 이 잡을 것 |
| M4 | `run_in_group` 시작 기록 `chain_start` = None | 생존 가능 (pid 다시 쓰임을 실경로로 가리는 시험 없음 · `gr_fake_launch` 만) |
| M5 | `ledger_now` 공유 잠금 → 잠금 없음 | 생존 가능 (덧붙임 중 읽기 시험 없음) |
| M6 | `ledger_append` "커밋은 됐는데 git 실패" 길 → 늘 되돌림 | 생존 가능 |
| M7 | `_ledger_rollback` 의 색인 `git reset` 뺌 | 같은 동작 (다음 `git add` 가 색인을 덮음) = 동등 변이 후보 |
| M8 | 다시 판정 `keep` 에서 합친 예측의 단위 대상 뺌 | 생존 가능 (합친 예측 다시 판정 + 같은 대상 뒤 시도 시험 없음) |
| M9 | `resume_chain_problem` 다시 셈 = 원 시도만 (앞 재실행 뺌) | 생존 가능 (앞 재실행 결과 줄만 바꾼 시험 없음 · 판정이 뒤에서 잡음) |
| M10 | `GROUP_SINCE` 전달 끔 (since 늘 None) | 생존 가능 |

## 4. 이 작업이 돌린 것 (명령 · 결과)

| 명령 (작업 트리 꼭대기 · `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10` · TMPDIR = 스크래치) | 결과 | 로그 |
|---|---|---|
| `python3 scripts/test_rint_r_chain.py` | 407/407 PASS · 454.0 s · rc 0 | `logs/suites_summary.txt` (원 로그 sha256 `e9d579e2…`) |
| `python3 scripts/test_rint_r_chain_e2e.py` | 40 PASS · 0 FAIL · 529.3 s · rc 0 | 같은 파일 (원 로그 sha256 `bd42cbe8…`) |
| `python3 -I …/preattack6/probes/probe6_unit.py <임시> U1,U2,U3` | U1 36/42 자격 · U2 · U3 (§1) | `logs/probe6_unit.out` |
| `python3 -I …/preattack6/probes/probe6_real.py <임시> R1,R1c,R2,R3,R4` | R1 · R1c · R2 · R3 (§1) · R4 무효 판 (§1 PC6-04 ⚠) · 16 s | `logs/probe6_real.out` |
| `python3 -I …/preattack6/probes/probe6_real.py <임시> R4` (고친 판 · 자식에 고정물 HERE) | SIGTERM · SIGHUP · SIGKILL = 원장 멈춤 · SIGINT = 되돌림 | `logs/probe6_real_R4.out` |
| `python3 -I …/preattack6/probes/probe6_uid.py` (root · 자식 uid 65534 · 임시 폴더 = 작업 트리 `.pa6_uid_<pid>` 0777 · 끝에 지움) | U1 · U2 · U3 (§1 PC6-01) | `logs/probe6_uid.out` |

## 5. 아직 안 한 것 (일시 중지 · 다시 시작할 때 차례)

1. 숫자 주장 나머지: `scripts/test_rint_first_result.py` · `scripts/test_ca_s0_census.py` · `scripts/test_ca_ext_runner.py` · `webapp/test_rint_explainer_page.py` · `bash scripts/check_kgy_py38.sh` (11 묶음 · 3.8.20 인터프리터 읽기만).
2. "고치기 전 판 7/26" — `b9fd47d7b` 사본에서 `--only PC,GR08,AL12,RS06,K01`.
3. 변이: `mutate_pc5.py` 표본 다시 (잡힘의 이유 대조) + §3 M1–M10 (각 변이 = PC · AL · RS · UM · GR 넓은 접두).
4. 탐침 R5 (PC6-07 실경로 — 원 시도 L02 OOM · 재실행이 L01 복사 뒤 L02 에서 표지 전 rc 2 → 결과 뒤 · runner_rc · `--add --resume` 거부 ↔ 같은 실패의 새 시도 = 결과 전) · PC6-08 실경로 (옆 파일 거부 기록 + 결과 줄 전 죽음 → recover).
5. PC5-01 독립 공격 넓히기 (끝 줄 바꿈과 폴더 증거를 함께 맞춘 꼴은 한정 그대로 · `git replace` · grafts 로 역사 검사 · 조상 대조를 속이는 꼴 — 결정 칸은 폴더 다시 셈이 묶으므로 영향 = 항목 줄 (env · machine · resume_of) 에 한정될 것 (추정)).
6. PC6-01 의 kgy 쪽 확인 (사슬 실행 사용자 · ssh 세션 프로세스의 environ 읽기 · sudo 프로세스 자격) — 1저자 · kgy 에서만.
7. `scripts/check_doc_refs.py` · `scripts/check_review_findings.py` (이 보고는 원장을 고치지 않았다).

## 6. 원장 등재 후보 (적용 안 함 · 메인 판단)

```text
{"id": "PC6-01", "severity": "P1", "status": "open", "owner": "claude", "found_by": "사전 공격 6 회차 (10-30 · 4c69070ad · 독립 작업 트리 · 중간 보고)", "opened_in": "docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/PREATTACK_C2.md", "title": "PC5-07 그룹 원 찾기 — 사슬과 같은 실 uid 이고 environ 을 못 읽는 무관 프로세스 (ssh 로그인 sshd 세션 · setuid 프로그램 · ssh-agent 꼴) 가 런 도중 생기면 rc 0 런 = GROUP_UNCONFIRMED · recover 도 그 프로세스가 사는 동안 미확인 rc 3 · 찾은 그룹 원도 안 죽임 — GPU 런이면 규칙 라로 그 대상 STOPPED (조건부 · 보수 쪽)"}
{"id": "PC6-02", "severity": "P2", "status": "open", ..., "title": "Q2 '그 밖 CUDA 오류 = 자동 재실행 없음' 이 rc ≠ 0 (그룹 원인 없음) 길에서만 — 시간 초과 · 신호 · 그룹 미확인 · 부모 사망 길에서 assert · misaligned · illegal instruction · launch failed · invalid value = 재실행 자격 (42 중 36 · 실경로 LAUNCH_FAILED + 부모 SIGKILL → --add --resume rc 0 · 재실행 CALIBRATED)"}
{"id": "PC6-03", "severity": "P3", "status": "open", ..., "title": "SIGINT (Ctrl-C) = run_in_group 원인 exception → chain_exception · 재실행 불가 (SIGTERM = signal · SIGKILL = parent_dead 는 자격) — 운영자 중단이 대상을 잃게 함 · PC5-06 앞은 parent_dead"}
{"id": "PC6-04", "severity": "P3", "status": "open", ..., "title": "원장 덧붙임 중 SIGTERM · SIGHUP · SIGKILL = 되돌림 없음 → 색인에 커밋 안 된 줄 · ledger_now 멈춤 · 다음 --add rc 3 (등록 R ⑧ '신호 = 되돌림' 은 SIGINT 만)"}
{"id": "PC6-05", "severity": "P3", "status": "open", ..., "title": "요약 있는 길 · 멈춘 런 로그 없음 · 못 읽음 + 시간 초과 · 신호 = 재실행 자격 (요약 없는 길은 같은 꼴 = 불가 · 등록 R ⑥ '못 읽음 = false' 가 한 길만)"}
{"id": "PC6-06", "severity": "P3", "status": "open", ..., "title": "사슬 자신의 MemoryError · ENOSPC = CHAIN_EXCEPTION · 재실행 불가 (러너의 같은 원인 = resource) — Q2 의 메모리 · 디스크 = 자원 과 어긋남"}
{"id": "PC6-07", "severity": "P3", "status": "open", ..., "title": "(추정 · 실경로 미실행) 복사한 재실행 시도 = 늘 결과 뒤 → 첫 재실행 런의 표지 전 러너 실패 (runner_rc) 가 재실행 사슬을 끝냄 (새 시도의 같은 실패 = 결과 전)"}
{"id": "PC6-08", "severity": "P3", "status": "open", ..., "title": "(코드 읽기 · PC5 diff 밖) 옆 파일 거부 기록 attempt_<n>.rejected.json + 결과 줄 전 죽음 = recover_ledger (폴더만 훑음) 가 못 고침 → 그 대상 막힘"}
```

(`...` = found_by · opened_in · owner 는 PC6-01 과 같다.)

## 7. 근거 파일 (이 폴더)

- 탐침: `probes/probe6_unit.py` (U1–U3 · 실제 사슬 함수 · 합성 시도 폴더) · `probes/probe6_real.py` (R1 · R1c · R2 · R3 · R4 · 시험 틀 `scripts/test_rint_r_chain.py` 의 고정물 · 가짜 러너 고장 `msg_sleep_after_mark` · `msg_after_mark` 를 그대로 · 시험 파일은 고치지 않음) · `probes/probe6_uid.py` (root 로 · 자식 uid 65534 · 실제 /proc · `run_in_group` · `--stage recover`).
- 다시 돌리기: 작업 트리 꼭대기에서 `python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/probes/probe6_unit.py <임시 폴더>` · `… probe6_real.py <임시 폴더> R1,R1c,R2,R3,R4` · (root) `… probe6_uid.py`.
- 로그: `logs/` (탐침 출력 JSON 줄 · 묶음 시험 요약 `suites_summary.txt`).
