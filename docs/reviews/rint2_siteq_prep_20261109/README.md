# Rint ② R 사슬 — 현장 자격 (site qualification) 점검 도구 · kgy · gabia

> 작성 2026-11-09 (준비 = 서브 에이전트 · 리포 반입 = 메인 세션) · **현장 실행 0 건** — 결과는 1저자가 kgy · gabia 에서 짧은 블록 (§3) 을 돌려 보낸 JSON 으로 받는다.  이 커밋 = 도구 · 기록만 (사슬 · 계약 · 러너 · 원장 · 계획 · s_min · 봉인 무변경).
> **이 컨테이너는 kgy · gabia 가 아니다** (Ubuntu 24.04 · 커널 6.18 · root · ext4 로컬 디스크 · GPU 없음) — §4 결과는 블록이 끝까지 돌고 막아야 할 때 막는다는 확인이지 현장 자격이 아니다.
> 줄 번호 기준 = **`abf0911eb`** (`git show abf0911eb:scripts/rint_r_chain.py` · 8663 줄).  점검 도구 = `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` (1,147 줄 · ASCII · sha256 a490b9adc3eeb7468b051b32bdaa0110879b71322a3a2cfb3b723505a3df8588 = 준비 때 컨테이너에서 돌린 바이트 그대로).
> 결과의 범위: 점검 도구는 **블록이 고른 핀의 사슬 함수**로 현장 OS 를 본다.  봉인 핀에서 `scripts/rint_r_chain.py` (또는 계약 · 러너) 가 바뀌면 그 핀으로 다시 돌린다 (블록의 PIN 한 줄만 바뀜).  사슬 코드 키는 HEAD 를 담으므로 (`code_key` · RRC:1902) 두 기계 결과 대조 (§3-3) 는 같은 핀끼리만 뜻이 있다.
> "현장 자격" 이 남은 조건으로 적힌 자리: `docs/reviews/rint2_rr3_fix_plan_20261108.md` 67 · 122 줄 (프로세스 · 잠금 · 권한 · 파일 시스템 · FIFO · NFS) · `docs/reviews/codex_review_rint2_rr_round3_20261108.md` 81 줄 (PC6-05 "FIFO/실권한 현장 자격 별도") · 184 줄 · `docs/reviews/codex_review_rint2_rr_round4_20261109.md` 148 줄 · 162 줄 ("미실행: … Linux /proc/flock/NFS·실제 SIGKILL/호스트").
> **11-11 판** (계획 `docs/reviews/rint2_siteq_remaining_plan_20261110.md` §10 의 2 번): 틀 고침 (도구 해시 · fetch 가지 · 블록 종료 코드 파일 · umask 기록 · 모드 목록) · nohup 꼴 · 컨테이너 시험 = **§9**.  §2 · §3 의 블록 설명과 §4-5 시험은 11-09 판 (옛 틀) 이다 — 지금 틀로 돌릴 때는 §9 를 본다.

## 0. 이번에 하는 것 / 하지 않는 것

| 하는 것 | 하지 않는 것 |
|---|---|
| 사슬 (`scripts/rint_r_chain.py`) · 계약 (`scripts/run_contract.py`) · 러너 (`scripts/sdcp_gain_vox015_8arm.sh`) · 첫 결과 감싸개 (`scripts/rint_first_result.py`) 가 **실제로** 기대는 OS 기능을 코드에서 읽어 표로 (§1) | R 캠페인 숫자 (max_hours · max_attempts · allowed_machines · env_unit · s_min …) 고르기 |
| 기능마다 현장 점검 — 사슬 **자신의 함수**를 새 빈 폴더에서 부르는 점검 우선 + 일반 사실 기록 (§2) | 봉인 · 계획 · s_min · 원장 · 리포 파일 손대기 |
| kgy · gabia 짧은 블록 각 하나 (23 줄 · ASCII · `!` 없음 · TAB 없음 · 핀 작업 트리의 도구를 새 결과 폴더로 복사 · sha256 대조 뒤 실행) (§3) | LIGGGHTS · MPM · payload 풀이 · 작업 제출 · 네트워크 · sudo |
| 이 컨테이너에서 블록을 실제로 돌린 결과 · 막아야 할 때 막는지 · 변이 셋 검출 (§4) | 현장 자격 "통과" 선언 · GO (이 결과 = 봉인 전 확인 목록 ④ 의 증거 후보일 뿐 · rr3 수정 계획 §7 ④) |

상태 표지: **확인** = 코드 줄 또는 이 컨테이너 실행으로 본 것 · **추정** = 코드에서 추론 (실행으로 안 봄) · **미확인** = 모른다 (현장 값 · 경로 등).

## 1. 사슬이 기대는 OS 기능 (코드에서 읽음 · 파일:줄 = `abf0911eb`)

`RRC` = `scripts/rint_r_chain.py` · `RC` = `scripts/run_contract.py` · `RUN` = `scripts/sdcp_gain_vox015_8arm.sh` · `FR` = `scripts/rint_first_result.py`.

### 1-1 프로세스 · 신호

| # | 기능 | 자리 | 코드가 가정하는 것 | 가정이 깨진 현장에서 생기는 일 | 점검 |
|---|---|---|---|---|---|
| P1 | 러너 = 새 세션 · 프로세스 그룹 (`Popen(start_new_session=True)` · `os.getpgid`) | RRC:2906–2909 (`run_in_group` 2871) | setsid 가 되고 러너 pgid = 러너 pid · 러너 자손은 그 그룹 · env 표지 `RINT_RUN_TOKEN` 을 물려받음 | killpg 가 엉뚱한 그룹 / 빈 그룹 → 자식이 남음 → 끝 기록 확인 False → `GROUP_UNCONFIRMED` (그 런 팔을 읽지 않음) | C09 (pgid==pid) |
| P2 | 그룹 kill (`os.killpg(SIGKILL)` · 시간 초과 · 신호 · 예외 때) + 회수 (`p.wait(timeout=…)` · 30 s) | RRC:2918 · 2935 · 2939 · `GROUP_GONE_WAIT_S` 373 | 같은 uid 라 kill 권한 · SIGKILL 이 곧 먹음 | 자식이 다른 uid (sudo · setuid) · PID 제한 → EPERM 은 조용히 넘김 → 표지 스캔에 남음 → 미확인 | C10 · C11 |
| P3 | 표지 스캔 (`/proc` listdir · `<pid>/stat` · `environ` · `task/<tid>` · `status` Uid) | RRC:`group_members` 2654–2723 (listdir 2671 · environ 2705) · `_run_kin` 2618 · `_run_session_ours` 2607 · `proc_stat` 2554 · `_proc_ruid` 2584 · `PROC_DIR` 2550 | 같은 uid 프로세스의 environ 을 읽을 수 있다 · stat 형식 (22 째 칸 = 시작 틱) · 러너 · payload 가 env 를 지우지 않음 | ⓐ 못 읽는 같은 uid 프로세스가 러너 세션 · 계보 안이면 `unsure` → 대기 없이 미확인 (recover rc 3) ⓑ 반대로 **스캐너가 아무것도 못 보면 (blind)** 남은 자식이 있는데도 끝 기록 `confirmed True` 거짓 — 변이 M1 이 이 꼴 (§4-3) | C08 · C09–C12 (러너가 적은 pid 를 따로 대조) |
| P4 | 남은 표지 프로세스 SIGKILL + 사라질 때까지 기다림 (0.05 s 간격 · 30 s 상한) | RRC:`group_kill_pids` 2790–2795 (kill 2793) · `group_settle` 2798 · `GROUP_POLL_S` 374 | 죽인 프로세스가 /proc 에서 사라지거나 Z | 상한 넘김 → confirmed False → `GROUP_UNCONFIRMED` | C09–C12 |
| P5 | 시작 틱 (`/proc/uptime` × `SC_CLK_TCK` · `since` = 그룹 시작 − 2 s) | RRC:`boot_ticks` 2575–2581 · run_in_group 2892 | 틱 눈금이 /proc/<pid>/stat 과 같다 | since None → 오래된 못 읽는 프로세스도 unsure | C06 |
| P6 | 호스트 신원 (`/etc/machine-id` · `/proc/sys/kernel/random/boot_id` · `readlink /proc/self/ns/pid`) + 대조 | RRC:`host_ident` 2534–2546 · `host_seen` 2746 | 셋 다 읽힘 (boot_id · pidns 는 필수) | boot_id · pidns 못 읽음 → recover 가 늘 "여기서 볼 수 없음" → `--operator-confirm` 없이는 결과 줄 못 씀 | C05 |
| P7 | 사슬 부모 생존 (`chain_pid` + 시작 틱 · pid 재사용 판별) | RRC:`chain_parent_alive` 2726 · `start_chain_problem` 2760 | stat 22 째 칸으로 pid 재사용을 가른다 | 판별 실패 → 산 사슬의 그룹을 recover 가 건드리거나 반대로 못 닫음 | C07 |
| P8 | SIGTERM · SIGHUP 처리기 (주 스레드 · 기다리는 동안만 · 정리 중엔 미룸) | RRC:`_signal_handlers` 2842–2853 · `_signal_restore` 2856 · `ChainSignal` 2830 · run_in_group 2902–2925 | 사슬이 주 스레드 · 처리기를 걸 수 있다 | 다른 스레드면 처리 없음 → 기본 동작 (즉시 종료) → 끝 기록 없음 → recover 몫 · ⚠ `nohup` 의 SIGHUP 무시를 **덮는다** (§6 Q1 · 확인 · 1저자 11-09 = nohup 그대로) | C11 · C21 |
| P9 | 사슬 부모 SIGKILL 뒤 그룹은 산다 → `--stage recover` 가 /proc 로 찾아 죽이고 확인 | RRC:`stage_recover` 8290 · `recover_group` 8198 | 부모 죽음이 러너 그룹을 죽이지 않음 · recover 가 같은 부팅 · 이름공간에서 돈다 | 그룹이 부모와 함께 죽는 환경이면 recover 는 빈 확인 (무해) · 못 찾으면 미확인 rc 3 | C12 |
| P10 | 러너 = `bash <러너>` · payload = **PATH 의 `python3`** (러너가 venv 를 켜지 않게 `MPM_NO_VENV=1`) | RRC:Runner._execute 5663–5665 · `RUNNER_EXEC_ENV` 360 · RUN:665 | PATH 의 python3 = 사슬과 같은 환경 단위 (사슬은 런마다 대조하지 않는다 — RRC 355–359 주석 한정) | payload 가 다른 판 → 봉인 원천 env 불일치 (`GraphSourceError` · SV 미확인) · 결과 판 섞임 (추정) | C02b |

### 1-2 잠금

| # | 기능 | 자리 | 코드가 가정하는 것 | 깨지면 | 점검 |
|---|---|---|---|---|---|
| L1 | 원장 잠금 = `flock` (배타 · 공유 · `LOCK_NB` 0.05 s 폴링 · 대기 120 s) · 잠금 파일 = 원장 `.git/rint_r_ledger.lock` (`O_RDWR\|O_CREAT` 0644) | RRC:`ledger_lock` 3158–3185 (open 3166 · flock 3177) · `_ledger_lock_path` 3148 · `LEDGER_LOCK_WAIT_S` 3057 | 그 파일 체계에서 flock 이 **프로세스 사이** 배타 · 프로세스가 죽으면 풀린다 | NFS `nolock` · 로컬 전용 잠금 · FUSE (ENOLCK) → ⓐ 동시 `--add` 둘이 같은 번호 → 원장 꼴 깨짐 ⓑ OSError 로 단계 멈춤 · 다른 호스트끼리의 배타는 한 기계 점검으로 못 봄 (§5) | C13 (변이 M3 로 검출 확인) |
| L2 | 읽기 전용 원장 — 잠금 파일을 못 만들면 공유 = 잠금 없이 읽음 · 배타 = Stop | RRC:3166–3172 | — | (설계대로) 쓰기 단계가 멈춤 | C13b |
| L3 | 원장 git 의 `index.lock` (add · commit) — flock 이 감싼다 · 실패 = 작업 파일 · 색인 되돌림 | RRC:`ledger_append` 3362–3395 · `_ledger_rollback` 3342–3358 | 원장 저장소를 사슬 밖에서 동시에 git 하지 않음 | 덧붙임 실패 → 되돌림 → 단계 멈춤 | C14 |

### 1-3 파일 체계 · 권한 · FIFO · NFS

| # | 기능 | 자리 | 코드가 가정하는 것 | 깨지면 | 점검 |
|---|---|---|---|---|---|
| F1 | 원자적 쓰기 = 같은 폴더 `<이름>.tmp.<pid>` → `fsync` → `os.replace` (폴더 fsync 없음) — 그룹 시작 · 끝 기록 · attempt.json · 단계 요약 | RRC:`write_json_atomic` 2523–2531 · `write_summary` 6482 · `_write_new_json` 3623 | 같은 폴더 rename 원자 · fsync 가 내용을 남김 | 비원자 rename (일부 FUSE · 네트워크) · 전원 손실 때 rename 미영속 → 반쯤 쓴 / 사라진 기록 → 읽기 `unreadable` → 재실행 자격 False (보수 쪽) | C15 |
| F2 | 비원자 쓰기 `Path.write_bytes` — 판정 `verdict.json` 등 | RRC:`write_json` 6434–6435 | 판정 프로세스가 쓰는 중 죽지 않음 | 잘린 JSON (다시 판정으로 드러남) · 기록만 | — (코드 사실) |
| F3 | 첫 풀이 끝 표지 = 임시 → fsync → replace → **폴더 fsync** (폴더 fsync 실패는 무시) · 쓰기 실패 = `os._exit(5)` | FR:`write_mark` 29–50 (exists 33 · replace 42 · 폴더 fsync 46 · `_exit` 65) | 폴더 fsync 지원 (아니면 rename 영속 미보장 · 기록만) | 표지 영속성 약함 (결과 전 · 뒤 판정 근거) | C15 (dir fsync) |
| F4 | 원장 덧붙이기 `open('ab')` + fsync · 원장 시작 `open('xb')` (O_EXCL) + fsync | RRC:3376–3379 · `stage_ledger` 8452–8456 | append · 배타 생성 정확 | 줄 겹침 · 이중 시작 | C14 |
| F5 | 배타 폴더 생성 (`attempt_<n>` = `mkdir()` · 있으면 FileExistsError) · 빈 출력 폴더 요구 | RRC:`attempt_open` 3693 · `outdir_empty_or_stop` 6421 · Runner._execute 5652–5653 | mkdir 원자 | 두 시도가 한 폴더 | C15 (`_write_new_json` 거부) · 블록 자체 (`mkdir` 없는 -p) |
| F6 | **일반 파일만** 읽기 = `os.open(O_RDONLY\|O_NONBLOCK\|O_NOCTTY)` → `fstat` `S_ISREG` → 그 fd 로 읽기 — 런 로그 · 그룹 기록 · 단계 요약 · attempt.json | RRC:`read_regular_file` 4081–4104 (open 4086 · S_ISREG 4092) · `run_log_text` 4107 · `_read_group_json` 3902 · `read_summary_state` 6442 | FIFO 를 O_NONBLOCK 으로 열면 막히지 않는다 · fstat 정확 | FIFO 에 막혀 recover · 재실행 판단 · 결과 줄이 **멈춤 (hang)** | C16 (변이 M2 로 검출 확인) |
| F7 | `lstat` 일반 파일 검사 (거부 기록 폴더) | RRC:`rejected_folder_problem` 5076 (lstat 5090) | — | — | C16 (같은 부류) |
| F8 | 폴더 요약 `folder_digest` = 링크 · 특수 파일이 있으면 None · os.walk · 파일마다 sha256 | RRC:3398–3423 | 폴더에 숨은 파일이 생기지 않음 | NFS silly-rename `.nfsXXXX` 가 생기면 요약 sha 가 원장과 달라짐 · 빈 폴더 검사 실패 (추정) | C16 · C16b · C19 |
| F9 | 복사 = `shutil.copytree(symlinks=True)` · `copy2` — 재실행 (실패 = `RESUME_NOT_ALLOWED`) · 합치기 (사본 요약 = 원장 sha 대조 · 실패 = `ATTEMPT_LEDGER_MISMATCH`) | RRC:ResumeRunner._copy 5752–5765 (copytree 5756 · copy2 5761) · MergeFetch._copy 7016–7031 (7023 · 7025) | copystat 가능 · 바이트 그대로 | 재실행 · 합치기 멈춤 | C19 |
| F10 | 값 봉인 파일 권한 `chmod 0600` (`verdict_results.json` · 실패는 무시) | RRC:8118–8122 (chmod 8120) | chmod 가 먹는다 | CIFS · drvfs 등이 조용히 무시 → 값 파일이 다른 사용자에게 읽힘 | C17 |
| F11 | umask — 기록 · 로그 파일 모드는 프로세스 umask (사슬이 정하지 않음) | (전역) | — | 공유 기계에서 남이 읽음 (운영) | C18 (기록) |
| F12 | 임시 폴더 `tempfile.mkdtemp` (다시 판정의 봉인 원천 런 · 읽은 뒤 rmtree) · 러너 `mktemp` | RRC:RunnerGraphSource 5832 · 5841 · RUN:684 | TMPDIR 쓰기 · 공간 | 다시 판정 · 러너 관문 실패 | C20 (쓰지 않고 사실만) |
| F13 | 경로 정규화 — `HERE` resolve · git 신원 resolve · 시작 기록 `base.resolve()` ↔ recover 의 `f.resolve().parent` · 원장 top `realpath` | RRC:224 · 956 · 1896 · 3727 · 8376 · 3084 · 3093 | 같은 폴더를 늘 같은 실경로로 본다 | 바탕을 다른 마운트 경로로 보면 recover 가 "다른 바탕" → 결과 줄 안 씀 (보수) | C26 (realpath 기록) |
| F14 | 러너 쪽: `.unchecked/<팔>` → OUTDIR 로 `mv` (같은 폴더 안 rename) | RUN:801 · 948 · 961 | 같은 파일 체계 | (실질 위험 낮음 · 추정) | — |

### 1-4 git

| # | 기능 | 자리 | 코드가 가정하는 것 | 깨지면 | 점검 |
|---|---|---|---|---|---|
| G1 | 체크아웃 신원 `rev-parse HEAD` · `--show-prefix` · `status --porcelain --untracked-files=normal` — **시간 상한 없음** · `text=True` (로케일 디코드) | RRC:`git_identity` 947–980 (959 · 965 · 971) · `code_record` 1889 · `code_dirty_problem` 1945 · `code_key` 1902 | git 이 곧 답함 · 소유자 검사 (`safe.directory`) 통과 · ignore 밖 추적 안 된 파일 없음 | 미확인 = 멈춤 (`CODE_PIN_MISMATCH`) · 느린 FS (NFS · 큰 트리 · fsmonitor) 에서 **끝없이 기다림** (상한 없음 · 추정) | C03 · C04 · C22 |
| G2 | 계획 출처 커밋 `cat-file -e` · `show` (상한 없음) | RRC:`plan_commit_problem` 1763–1790 (1775 · 1779) | 그 커밋이 체크아웃 저장소에 있다 (fetch) | `S0_REPORT_MISMATCH` (봉인 뒤 몫 · 이 점검 밖) | — |
| G3 | 원장 git (`GIT_*` env 지움 · 고정 신원 · `commit.gpgsign=false` · `core.autocrlf=false` · 120 s) · `rev-parse --show-toplevel` (60 s) · 역사 · `bundle create` | RRC:`ledger_git` 3065–3076 · `LEDGER_GIT_CFG` 2990 · `_git_top` 3078 · `ledger_history_problem` 3119 · `ledger_bundle` 7198 (7202) | 사용자 전역 설정 (hooks · `core.hooksPath` · fsmonitor) 이 커밋을 바꾸지 않음 | 훅 실패 · 지연 → 덧붙임 실패 → 되돌림 → 멈춤 | C14 |

### 1-5 환경 · 자원 · 시간

| # | 기능 | 자리 | 코드가 가정하는 것 | 깨지면 | 점검 |
|---|---|---|---|---|---|
| E1 | 환경 같음 단위 = python 부 판 · numpy · scipy 판 문자열 | RC:`env_unit_now` 1455 · RRC:`env_record` 1070 | kgy = 3.8 · 1.24.4 · 1.10.1 (1저자 10-24 출력) · gabia 를 같은 판으로 (10-24 결정) | 계획 봉인 판과 다르면 `CODE_PIN_MISMATCH` · 두 기계 단위 합치기 불가 | C02 · C02b |
| E2 | 기록만 칸: `nvidia-smi` (20 s) · BLAS 탐침 (`python -I` 새 프로세스 · 120 s) · `/proc/cpuinfo` | RRC:`_env_gpu` 999–1003 · `_env_blas` 1019–1040 (1021) · `_env_cpu` 1042 | 곧 답함 | 단계 시작이 느려짐 (판정 무관) · 드라이버 멈춤이면 20 s | C22 · C28 |
| E3 | 자원 낱말 (메모리 · 디스크 다섯) · CUDA 오류 표지 · 재실행 자격 원인 | RRC:`RESOURCE_WORDS` 3033 · `NOT_RESOURCE_WORDS` 3037 · `CUDA_ERROR_WORDS` 3047 · `RESUME_CAUSES` 3027 · `words_cause` 3976 | 자원 실패는 로그에 그 낱말을 남긴다 | **OOM killer 의 SIGKILL 은 로그에 낱말을 남기지 않는다** → 러너 rc 길 = `runner_rc` = 자동 재실행 없음 (추정 · 실측 아님 · §5) · `No space left on device` = 재실행 자격 | C24 · C25 · C26 (기록) |
| E4 | 시간 상한 = **벽시계** (`deadline = time.time() + max_hours·3600` → 런마다 `left`) | RRC:7297 · 5654 | 시계가 크게 뛰지 않음 | NTP 계단 이동이면 남은 시간이 그만큼 변함 (추정) | C29 (NTP 기록) |
| E5 | 화면 = 한국어 · 기호 `print` (`line_buffering`) | RRC:`main` 8520 (reconfigure 8522) | stdout 인코딩이 UTF-8 (또는 C 로케일의 UTF-8 모드) | `UnicodeEncodeError` 로 단계가 죽을 수 있다 (추정) | C23 |
| E6 | 러너: `set -uo pipefail` · `P2_ATTEMPT` · `/usr/bin/time -v` (있으면 최대 RSS) | RUN:34 · 629 · 910 | bash · coreutils | (러너 관문) | C22 (bash 판 · /usr/bin/time) |

## 2. 현장 점검 — 무엇을 · PASS 출력 · FAIL 의 뜻

블록 (§3) 이 하는 일, 순서대로:

1. **아무것도 쓰기 전 관문 (bash)** — `PIN` = 40 자 소문자 hex · 새 작업 트리 자리 (홈 아래 `dem-siteq-<핀 앞 9 자리>`) 와 결과 폴더 (홈 아래 `rint_siteq_<기계>_<UTC 날짜>`) 가 **없음** · venv 있음 → 아니면 `[siteq] STOP: … (nothing written)` · 종료 코드 2.
2. 기준 체크아웃에서 `git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8` → `git worktree add --detach <새 자리> <PIN>` (새 폴더 · 기존 체크아웃 · 런 폴더 무변경 · 기준 저장소에는 받아 온 커밋과 작업 트리 등록만 늘어난다) → 새 자리 HEAD = PIN 확인 (어긋나면 STOP).
3. 결과 폴더 `mkdir` (배타) → 핀의 `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` 를 복사 → **sha256 대조** (a490b9ad…) → 어긋나면 `STOP: probe sha256 differs (probe not run)` (작업 트리 · 도구 사본만 든 결과 폴더는 남음).
4. venv 켜기 → 결과 폴더에서 `python3 -I -B -u siteq_probe.py …` (pyc 안 씀 · 입력 /dev/null) → 화면 + `siteq.log` → `siteq_result.json` (ASCII · 원자적 쓰기) → `sha256sum siteq_result.json` (화면 + `siteq_result.json.sha256`) → 종료 코드 = 점검 도구 rc (0 = FAIL · ERROR 없음 · 1 = 있음 · 2 = 준비 문제).

준비 때 만든 긴 블록 (도구 전체를 블록 안에 품은 1,216 줄 판 · §4-2 · §4-3 시험 대상) 은 관문이 하나 더 있었다 — `git status` 로 체크아웃이 깨끗한지 · 결과 폴더가 체크아웃 밖인지.  짧은 블록은 **새로 만든 작업 트리**를 쓰므로 깨끗함이 만들 때 정해지고, 결과 폴더는 홈 아래 따로다 (도구 자신도 `--out` = 도구가 든 새 폴더 · 체크아웃 밖인지 다시 본다 · 아니면 rc 2).  끝의 C99 가 체크아웃이 그대로인지 확인한다.

점검 줄 꼴: `[siteq] <ID> <상태> <제목> -- <세부>`.  상태: **PASS** · **FAIL** (현장 결함 또는 기준 불일치) · **WARN** (권고 · 결함 단정 아님) · **INFO** (기록만 · 기준 없음) · **SKIP** (해당 없음) · **ERROR** (점검 도구 자체 예외 — 현장 결함 여부 **미확인** · 세부를 보고 판단).  점검마다 시간 예산 (30–300 s) · 넘으면 FAIL "no answer within … s (hang on this site?)".

| ID | 사슬 함수 · 방법 | PASS 일 때 세부 (판정에 쓰는 칸) | FAIL · WARN 의 뜻 |
|---|---|---|---|
| C01 | 체크아웃의 `scripts/rint_r_chain.py` import (`-B`) | `imported <REPO>/scripts/rint_r_chain.py` | ERROR = 그 핀 · 그 파이썬에서 사슬이 안 뜬다 (뒤 점검 전부 SKIP) |
| C02 | `RR.env_record()['unit']` ↔ 기대 (kgy 기준 3.8 · 1.24.4 · 1.10.1) | `env unit {"numpy": "1.24.4", "python_minor": "3.8", "scipy": "1.10.1"} vs expected {…같음…}` | 다른 판 = 계획 봉인 판 대조에서 `CODE_PIN_MISMATCH` 될 환경 (gabia = venv 를 kgy 판으로 · 10-24 결정) |
| C02b | PATH 의 `python3` 로 같은 단위를 다시 잼 (러너 → payload 길 · `MPM_NO_VENV=1`) | `PATH python3 env unit {…} (probe {…})` 두 단위 같음 | 다르면 payload 가 사슬과 다른 판으로 돈다 (봉인 원천 env 불일치 · 판 섞임) |
| C03 | `RR.git_identity(<REPO>/scripts/rint_r_chain.py)` | `head <PIN> dirty False rel scripts/rint_r_chain.py error None` | 소유자 검사 (`dubious ownership`) · 느린 git · 더러운 트리 → 사슬 멈춤 원인 |
| C04 | `RR.code_record(러너)` + `RR.code_dirty_problem` + `RR.code_key_sha` · CODE_FILES 19 개 다 있음 | `code_key_sha256 <64 hex>` | 한 단계 안 사슬 ↔ 러너 다름 · 파일 결손.  **kgy · gabia 의 이 값이 같아야** 두 기계 단계를 합칠 수 있다 (§3-3 비교) |
| C05 | `RR.host_ident()` · `RR.host_seen(자기, 자기)` | `machine_id, boot_id, pidns readable` | boot_id · pidns 못 읽음 = recover 가 늘 미확인 (FAIL) · machine_id 만 없음 = WARN |
| C06 | `RR.proc_stat` (pid · task) · `RR.boot_ticks` · `RR._proc_ruid` · `getppid` · `getpgrp` · `getsid` 와 맞춤 | `proc_stat/boot_ticks/_proc_ruid consistent` | /proc 형식 · 틱 눈금이 사슬 가정과 다름 |
| C07 | `RR.chain_parent_alive` — 산 부모 · 회수한 자식 · 시작 틱 다른 같은 pid | `live parent True, reaped child False, parent with other start tick False` | pid 재사용 판별 실패 |
| C08 | `RR.group_members(새 표지, since=지금−2 s, run=끝난 러너)` (생산 꼴) · 옛 규칙 (since · run 없음) 은 기록만 | `fresh token -> [] in … s (N processes); old rule … unsure K` | 새 표지에 `None` / 프로세스 = 실제 런에서 미확인 · K (옛 규칙) 는 기록만 (예: ssh 세션 · setuid 프로그램 수) |
| C09 | `RR.run_in_group` — 러너가 rc 0 으로 끝나며 같은 그룹 자식 · setsid 자식 · 3 s 뒤 파일 쓰는 자식을 남김 · **러너가 적은 pid 4 개를 /proc 로 따로 대조** | `rc 0 cause None confirmed True killed ≥2 pgid==pid True late_file False left_now []; runner-reported pids [4 개] still alive []` | 남은 자식 · 늦은 파일 · 끝 기록 거짓 확인 (스캐너가 못 봄) |
| C10 | `RR.run_in_group` 시간 초과 (2 s) → killpg + 표지 스캔 | `cause timeout … confirmed True killed ≥1 left_now [] …; pids [2 개] still alive []` | 시간 초과 뒤 정리 실패 |
| C11 | 사슬 꼴 자식 프로세스 (`run_in_group` 기다리는 중) 에 SIGTERM | `child rc 0 cause signal signal SIGTERM confirmed True killed ≥1 left_now []; … still alive []` | 신호 처리 · 정리 실패 |
| C12 | 사슬 꼴 자식을 SIGKILL → 끝 기록 없음 · 그룹 생존 확인 → **실제 CLI** `rint_r_chain.py --stage recover --out <폴더>` | `end record before recover False; group alive after parent SIGKILL ≥1; recover rc 0; end by recover cause parent_dead confirmed True …; still alive []` | recover 가 이 기계에서 고아 그룹을 못 찾거나 못 닫음 (rc 3) |
| C13 | `RR.ledger_lock` 두 프로세스 (새 git 저장소 · 이 폴더의 파일 체계): 배타↔배타 · 공유↔배타 · 잡은 쪽 SIGKILL 뒤 · 공유↔공유 · 배타↔공유 | `lock_path_in_git_dir=True ex_vs_ex=stop:ATTEMPT_LEDGER_MISMATCH sh_vs_ex=stop:… ex_after_holder_sigkill=acquired sh_vs_sh=acquired ex_vs_sh=stop:…` | `acquired` 가 나와야 할 자리에 stop 이거나 그 반대 = flock 이 이 파일 체계에서 배타가 아니다 · `oserror:<errno>` = flock 미지원 |
| C13b | `.git` 0555 인 원장에서 배타 · 공유 | (root 아님) `exclusive=stop:… shared=acquired` · (root · 권한 무시 FS) INFO | 읽기 전용 원장 처리 어긋남 |
| C14 | 새 git 저장소 (`scratch_ledger_NOT_PRODUCTION`) 에 사슬 함수로 머리 · 항목 덧붙이기 · 역사 · 조상 · 낡은 expect 거부 · bundle | `init/commit/append/history/ancestor/stale-refusal/bundle ok` | git 판 · 전역 설정 · 파일 체계가 원장 연산을 막음 · WARN = 훅 (`core.hooksPath` · 템플릿 훅) 이 원장 커밋마다 돈다 |
| C15 | `RR.write_json_atomic` 두 번 (만들기 · 덮기) · 임시 파일이 남지 않음 · `RR._write_new_json` 이 있는 파일을 거부 · 폴더 fsync | `write/replace ok, no temp leftovers, new-file refusal ok, directory fsync ok` | 원자 교체 · 배타 생성 실패 · WARN = 폴더 fsync 미지원 (`FR` 이 무시하는 자리) |
| C16 | 자식 프로세스 (30 s 상한) 에서 `RR.read_regular_file` · `run_log_text` · `_read_group_json` · `read_summary_state` · `read_attempt` · `folder_digest` — 일반 · 빈 · 없음 · 끊긴 링크 · 폴더 · **FIFO** · `/dev/null` · 모드 000 | `all special-file cases as expected` (모드 000 의 기대 = 커널이 읽기를 허락하는지 `os.access` 로 정함) | **막힘 (30 s)** = FIFO 가 이 현장에서 막힌다 → recover · 재실행 판단 멈춤 · 상태 어긋남 · SKIP = 이 파일 체계에 FIFO 를 못 만든다 (FIFO 위협도 없음) |
| C16b | 열린 파일을 지운 뒤 목록 | `unlink of an open file leaves no visible entry` | WARN = `.nfsXXXX` (NFS silly-rename) → `folder_digest` · 빈 폴더 검사가 흔들릴 수 있다 |
| C17 | `chmod 0600` 뒤 모드 | `mode after chmod 0600 = 600` | 모드가 안 먹는 FS (값 봉인 파일이 남에게 보임) |
| C19 | `copytree(symlinks=True)` · `copy2` → `RR.folder_digest` 같음 | `copytree/copy2 ok, folder_digest equal True, …` | 재실행 · 합치기 사본이 실패하거나 요약이 달라짐 |
| C21 | `RR._signal_handlers` / `_signal_restore` (주 스레드) | `handlers installed for ['SIGHUP', 'SIGTERM'], restored True` | 처리기 설치 · 복원 실패 |
| C23 | 비 ASCII (한글 · `·` `→` `≠` `✓` `σ` `★` `ⓐ`) 를 파이프로 — `-I` 자식 · 생산 꼴 (`-I` 없음) 자식 | `isolated rc 0, production-like rc 0 (encoding=utf-8 …)` | 사슬 화면 출력이 이 로케일에서 죽을 수 있다 |
| C26 | 실경로 · 파일 체계 종류 (mountinfo · 마운트 출처 = 호스트 이름이 있을 수 있어 **기록 안 함** · 옵션은 허용 목록만) · 남은 공간 · inode · 쓰기 가능 — 새 폴더 · 체크아웃 · HOME · 계획 폴더 (`--plan-dirs`) | `out=<fs>, repo=<fs>, home=<fs>, plan_dir=<fs>` | WARN = 네트워크 · FUSE FS / tmpfs · ramfs (재부팅에 사라짐) / 계획 폴더가 새 폴더와 다른 파일 체계 (C13–C19 가 그 FS 를 대표 못 함 → 결과 폴더를 그 FS 에 두고 다시) / 쓰기 불가 |
| C99 | 끝에 다시 `rev-parse` · `status` · `scripts/__pycache__` mtime | `checkout still at pin and clean` | FAIL = 끝날 때 HEAD ≠ PIN · 더러움 · WARN = `__pycache__` 가 바뀜 (이 도구는 `-B` → 다른 프로세스가 쓴 것) |
| C98 | (끝 정리) 사슬과 **따로** 만든 표지 스캔 (environ 에 표지가 **확인된** 프로세스만 SIGKILL) | (없으면 줄이 안 나온다) | WARN = 사슬 정리가 남긴 프로세스를 마지막에 죽였다 (= 사슬 스캐너가 이 현장에서 못 본 것) |

기록만 (INFO · 기준 없음 · 1저자가 본다): **C18** umask · 새 파일 모드 · **C20** TMPDIR 실경로 · FS · 남은 공간 (쓰지 않음) · **C22** nvidia-smi · BLAS 탐침 · git 시간 (WARN = 상한 20 s · 120 s 에 가까움) · git · bash 판 · `/usr/bin/time` · **C24** rlimit (WARN = AS · DATA · CPU · FSIZE 상한 있음) · **C25** MemTotal · MemAvailable · swap · cgroup `memory.max` · `memory.oom.group` · `pids.max` · `vm.overcommit_memory` · `pid_max` (할당 없음) · **C27** /proc 마운트 옵션 (`hidepid` · `subset`) · **C28** `nvidia-smi` GPU 이름 · 드라이버 · 메모리 + cupy 배포 (CUDA 문맥 안 만듦 · WARN = GPU 또는 cupy 없음 — 등록 R 런 = `EXPECT_BACKEND=gpu`) · **C29** OS · CPU 수 · affinity · NTP 동기 · 띄우기 도구 (tmux · screen · setsid · nohup).

⚠ 점검 도구 자체의 한정: 표지 스캔 · 잠금 · 파일 점검은 **블록을 돌린 사용자 · 그 셸 환경 · 새 폴더의 파일 체계** 에서 본 것이다 — 실제 사슬을 다른 사용자 · 다른 띄우기 (tmux · nohup · cron) · 다른 FS 의 폴더로 돌리면 그 조건으로 다시 돌려야 대표한다.  점검 도구는 `python3 -I -B` 로 돌고 생산 명령은 `python3 <스크립트>` 다 (PYTHON* env 차이 — 인코딩은 C23 이 두 꼴 다 본다).

## 3. 현장에서 돌리는 법 — 짧은 블록 (리포 핀에서 도구를 꺼내 돌림)

준비 때는 도구 전체를 블록 안에 넣은 긴 블록 (≈ 59 KB · 1,216 줄) 을 만들었다 (§4-2 · §4-3 시험 = 그 블록).  도구가 리포에 들어간 뒤로는 블록이 **핀의 작업 트리에서 도구를 복사**하므로 23 줄이면 된다 (도구 바이트 = 같은 sha256 · §4-5 시험).  블록 틀 = `docs/reviews/rint2_siteq_prep_20261109/container_test/short_block.tmpl` (자리 넷 = PIN · 기계 · 기준 체크아웃 · 계획 폴더) — 채운 블록은 기계마다 경로가 달라 1저자에게 대화로 준다 (주소 · 기계 이름 · 사용자 이름 · 리포 밖 경로는 리포에 쓰지 않는다).

### 3-1 쓰는 법

1. 사슬을 실제로 돌릴 **같은 사용자 · 같은 venv** 의 bash 프롬프트에 통째로 붙인다 (블록 = `bash <<'SITEQ' … SITEQ` — 안에서 `exit` 해도 내 셸은 닫히지 않는다 · 바깥 셸 bash · `bash -i` 확인 (§4-5 S9) · zsh = 미확인).  생산 런의 띄우기 방식 (1저자 11-09 Q1 = `nohup`) 과 무관하게 붙인 셸에서 돈다.
2. 블록에서 고칠 칸 = 없음 (PIN · 기계 · 기준 체크아웃 · venv · 계획 폴더가 채워져 온다).  kgy = 기준 체크아웃 = 10-24 에 만든 작업 트리 (S0 단계 1 블록과 같은 자리) · venv = dem-venv · 계획 폴더 = sdcp.  gabia = 기준 체크아웃 = 홈의 리포 클론 · venv = dem-venv (11-09 새로 만듦 · §7) · 계획 폴더 = 없음 (R 런 자리 미정 → 정하면 그 자리로 다시).
3. 새 작업 트리 = 그 핀 전체 체크아웃 (≈ 1.1 GB · 이 리포 11-09 기준) · 걸리는 시간 ≈ fetch + 체크아웃 + 15–45 s (추정 · 이 컨테이너 점검 13–15 s).
4. 같은 날 다시 = 새 작업 트리 · 결과 폴더를 옮긴 뒤 (블록은 덮지 않는다 · §4-5 S3).
5. 보낼 것 = `siteq_result.json` + sha256 줄 (+ `siteq.log`).  JSON 은 ASCII · 약 24 KB · 마운트 출처 · 호스트 이름 · env 덤프 없음 (machine-id · boot-id · 표지 = 사슬 기록에도 있는 칸).
6. 끝나면 새 작업 트리는 지워도 된다 (`git -C <기준 체크아웃> worktree remove <새 자리>`) — 결과 폴더는 남긴다.

### 3-2 무엇을 보면 되나

- 끝 줄 `[siteq] rc 0` = FAIL · ERROR 없음.  `rc 1` = 화면의 `[siteq] FAIL …` · `[siteq] ERROR …` 줄과 JSON 을 그대로 보낸다 (원인 판단 = Claude · 1저자 · FAIL · ERROR · WARN 마다 원인 한 줄).  `rc 2` = STOP (돌리기 전 멈춤 · 메시지 그대로).
- 현장 기대 (추정): C02 = PASS (3.8 · 1.24.4 · 1.10.1 · §7) · C28 = INFO (GPU · cupy 있음) · gabia 는 root 라 C13b = INFO (권한 무시 · §6) · C26 = 로컬 FS 면 PASS.
- 도구 메시지의 `SITEQ_BASE` (C26) = 긴 블록의 칸 이름이다 (도구 바이트를 바꾸지 않으려고 그대로 둠) — 짧은 블록에서는 결과 폴더 자리 (홈) 를 뜻한다 · 계획 폴더가 다른 FS 면 블록의 OUT 을 그 FS 로 바꿔 다시 돌린다.
- 결과 (11-09 밤 반입) = `docs/data/rint2_siteq_20261109/` — kgy · gabia 둘 다 rc 0 · §3-3 세 줄 SAME · 위 현장 기대와 다른 칸 0.
- 결과의 쓰임 (1저자 11-09 *"나머지는 권고대로"*): kgy · gabia 두 JSON + sha256 → `docs/reviews/rint2_rr3_fix_plan_20261108.md` §7 ④ "현장 자격" 칸의 근거 · Codex 짧은 확인 때 동봉.

### 3-3 두 기계 결과 나란히 보기 (어느 기계에서든 · 두 JSON 을 모은 뒤)

```bash
python3 -I - KGY/siteq_result.json GABIA/siteq_result.json <<'PYCMP'
import json, sys
a, b = [json.load(open(p)) for p in sys.argv[1:3]]
def get(d, cid):
    return next((c for c in d['checks'] if c['id'] == cid), {}).get('data', {})
rows = [('pin', a['pin'], b['pin']),
        ('env unit C02', get(a, 'C02').get('unit'), get(b, 'C02').get('unit')),
        ('code_key_sha256 C04', get(a, 'C04').get('code_key_sha256'), get(b, 'C04').get('code_key_sha256'))]
for name, x, y in rows:
    print('%-20s %s  %s | %s' % (name, 'SAME' if x == y else 'DIFF', x, y))
for d in (a, b):
    bad = ['%s=%s' % (c['id'], c['status']) for c in d['checks'] if c['status'] in ('FAIL', 'ERROR', 'WARN')]
    print('%-6s %s %s' % (d['machine'], json.dumps(d['counts'], sort_keys=True), ' '.join(bad)))
PYCMP
```

기대: 세 줄 모두 `SAME` (같은 핀 · 같은 판 · 같은 코드 키 = 사슬이 두 기계 단계를 같은 코드로 받는 조건 · `code_key` 는 저장소 상대 경로라 체크아웃 자리가 달라도 같다).  이 컨테이너에서 kgy · gabia 꼴 두 결과 (같은 핀 `abf0911eb` · py3.8) = 세 줄 SAME (확인) · 핀이 다른 두 결과 = pin · code key 둘 다 DIFF (확인).

### 3-4 (선택) 기존 합성 시험의 실제 프로세스 묶음을 현장에서

블록과 따로 · 1저자가 원할 때만 (블록이 만든 작업 트리 W · 결과 폴더 D · dem-venv 를 켠 셸에서).  `scripts/test_rint_r_chain.py --only GR` (14 개 · 가짜 러너 bash · 실제 `run_in_group` · 실제 SIGTERM · 사슬 부모 SIGKILL + `--stage recover` · 풀이 없음) 을 현장 사용자 · 현장 커널에서 돌리면 같은 부류를 한 번 더 본다.  이 컨테이너 (시작 핀 `7cdc78111` · py3.11) = **14/14 PASS · 29.2 s** (`work/gr_run.log`).

```bash
W="<블록이 만든 작업 트리>"; D="<블록이 만든 결과 폴더>"; mkdir "$D/tmp_gr" && cd "$D" && TMPDIR="$D/tmp_gr" python3 "$W/scripts/test_rint_r_chain.py" --only GR 2>&1 | tee "$D/gr.log"
```

⚠ 한정: 합성 시험이다 (현장 자격을 대신하지 않는다 · Codex 판정 그대로) · 시험이 띄우는 자식 파이썬은 `-I` 라 체크아웃 `scripts/__pycache__` 에 그 인터프리터 판의 `.pyc` 를 쓸 수 있다 (gitignore · 사슬을 돌려도 생기는 것 — 블록의 "새 폴더에만 쓴다" 약속 밖) · 블록이 만든 결과 폴더가 있어야 한다 · 자식 `.pyc` 는 새 작업 트리에만 생긴다 (기존 체크아웃 무관).

## 4. 이 컨테이너에서 돌린 결과 (kgy · gabia 아님)

### 4-1 환경 (사실)

Ubuntu 24.04.5 · 커널 6.18 · **root (uid 0)** · 4 CPU · 메모리 16 GB · swap 0 · `/` = ext4 로컬 · `/proc` 기본 옵션 · pid_max 32768 · GPU · cupy 없음 · git 2.43.0 · bash 5.2.21 · 파이썬 둘: 3.11.17 (numpy 2.4.6 · scipy 1.17.1 = 게이트 판) · uv CPython **3.8.20 + numpy 1.24.4 + scipy 1.10.1** (= kgy 판 재현 · `scripts/setup_kgy_py38.sh` · PATH 심으로 `python3` 자리에 둠 · kgy 의 3.8.10 과 패치 판만 다름).  **같은 시간에 메인 세션의 게이트 (`scripts/check_all.sh` · py3.8 시험) 가 같은 리포에서 돌고 있었고 커밋도 했다** (아래 4-4).

### 4-2 긴 블록 시나리오 (준비 판 · 시험 도구 = 스크래치 · 요약 `container_test/summary.txt`)

| # | 조건 | 결과 (블록 종료 코드 · 요약) | 판단 |
|---|---|---|---|
| A1 | py3.11 · 실제 리포 · kgy 기본 EXPECT | rc 1 · FAIL 1 = **C02** (3.11 · 2.4.6 · 1.17.1 ≠ kgy 판) · WARN C28 (GPU 없음) · C99 (아래) · 나머지 PASS/INFO · 14.3 s | 기대대로 (이 컨테이너 ≠ kgy) |
| A2 | py3.8 심 (kgy 판) · 실제 리포 | rc 0 · PASS 23 · INFO 8 · WARN 2 (C28 · C99) · 13.6 s | 기대대로 |
| A3 | PIN = 맞는 꼴의 틀린 커밋 | rc 2 · `STOP: HEAD … differs from PIN … (nothing written)` · 새 폴더 없음 | 막힘 확인 |
| A4 | 출력 폴더가 이미 있음 (표지 파일) | rc 2 · `STOP: output folder already exists` · 그 폴더 트리 해시 전후 같음 | 막힘 확인 |
| A5 | PIN 자리표 (`SET_ME_40_HEX_PIN`) 그대로 | rc 2 · `STOP: PIN must be the full 40-character …` · 폴더 없음 | 막힘 확인 |
| A6 | 블록 안 점검 도구 한 글자 바꿈 | rc 2 · `STOP: probe text changed in transit (sha256 …, want a490b9ad…)` · 결과 JSON 없음 (폴더 · 바뀐 도구 파일은 남음) | 막힘 확인 |
| A7 · A7b | A1 · A2 를 `strace -f` (열기 쓰기 · 만들기 · 이름 바꾸기 · 지우기 · 링크 · chmod · truncate · utimensat) 아래 | 리포 경로 아래 **변경 연산 0 건** (추적한 파일 연산 각 약 3 만 개 중) | 블록 · 점검 도구가 체크아웃에 안 씀 (확인) |
| A8 | `bash -i` 로 블록 읽기 (붙여 넣기 꼴 · 히스토리 확장 켬) | A1 과 같은 결과 · 화면 되풀이 줄에 readline 표시 찌꺼기 (예 `2026-11-009`) — 내용은 sha256 관문 통과 = 바이트 같음 | 문제 없음 |
| A9 | 바깥 셸 = `dash` (A3 꼴) | rc 2 · 같은 STOP · 폴더 없음 | 바깥 셸 무관 |
| A10 | 합성 체크아웃 (`git archive HEAD scripts` → 새 저장소) + 추적 안 된 파일 | rc 2 · `STOP: checkout is not clean …` · 폴더 없음 | 막힘 확인 |
| A11 | 합성 체크아웃 깨끗 · py3.8 · **능력 (capability) 다 뺀 uid 0** (`setpriv --bounding-set=-all`) | rc 0 · PASS 25 · INFO 7 · WARN 1 · C13b **PASS** (배타 stop · 공유 acquired) · C16 모드 000 = unreadable · C08 옛 규칙 unsure 12 | 권한 경로가 비 root 처럼 동작하는 것 확인 (진짜 비 root 사용자 아님 · §5) |
| A12 | gabia 블록 · py3.8 | rc 0 · PASS 24 · INFO 8 · WARN 1 (C28) | gabia 블록 동작 |
| A13 | `PLAN_DIRS=/dev/shm` (tmpfs · 다른 FS · stat 만) | rc 0 · C26 **WARN** "plan dirs on another filesystem … rerun with SITEQ_BASE on that filesystem; volatile filesystem" | WARN 길 확인 |

### 4-3 점검이 실제로 실패할 수 있는지 — 사슬 변이 셋 (합성 체크아웃 사본에만 · 커밋해 깨끗한 트리로)

| 변이 | 바꾼 것 | 걸린 점검 | 판단 |
|---|---|---|---|
| M1 | `group_members` 가 늘 `[]` (보지 못하는 스캐너) | **C09 · C10 · C11 · C12 FAIL** (사슬 끝 기록은 `confirmed True` 라고 거짓 확인 · 러너가 적은 pid 대조가 살아 있는 자식을 잡음) · C98 WARN (끝 정리가 남은 7 개를 죽임) · C08 은 PASS (새 표지 = 빈 목록이 정상이라 C08 하나로는 못 가린다) | 따로 대조가 값을 했다 |
| M2 | `read_regular_file` 을 막히는 열기 (`O_NONBLOCK` 없음) 로 | **C16 FAIL** "reader blocked for 30 s" (42.9 s) | FIFO 막힘 검출 |
| M3 | `ledger_lock` = 아무것도 안 잠금 | **C13 FAIL** (`ex_vs_ex=acquired` …) | flock 부재 검출 |

점검별 상태 (최종 판 점검 도구 `a490b9ad…`):

| ID | A1 | A2 | A11 | A12 | A13 | M1 | M2 | M3 |
|---|---|---|---|---|---|---|---|---|
| C01 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C02 | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C02b | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C03 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C04 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C05 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C06 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C07 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C08 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C09 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS |
| C10 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS |
| C11 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS |
| C12 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS |
| C13 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL |
| C13b | INFO | INFO | PASS | INFO | INFO | INFO | INFO | INFO |
| C14 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C15 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C16 | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS |
| C16b | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C17 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C18 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C19 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C20 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C21 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C22 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C23 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C24 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C25 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C26 | PASS | PASS | PASS | PASS | WARN | PASS | PASS | PASS |
| C27 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C28 | WARN | WARN | WARN | WARN | WARN | WARN | WARN | WARN |
| C29 | INFO | INFO | INFO | INFO | INFO | INFO | INFO | INFO |
| C99 | WARN | WARN | PASS | PASS | PASS | PASS | PASS | PASS |
| C98 | — | — | — | — | — | WARN | — | — |
| 핀 | `7cdc78111` | `7cdc78111` | 0abf4965e | `abf0911eb` | `abf0911eb` | 954623ca4 | 60e510332 | d96ba6417 |
| 점검 도구 sha256 | a490b9ad | a490b9ad | a490b9ad | a490b9ad | a490b9ad | a490b9ad | a490b9ad | a490b9ad |
| 초 | 14.3 | 13.6 | 13.0 | 13.3 | 13.4 | 13.2 | 42.9 | 10.0 |

(A11 = 합성 체크아웃 커밋 0abf4965e (`7cdc78111` 의 scripts/) · M1–M3 = 그 사본에 변이를 커밋한 핀 · C98 은 정리할 것이 있을 때만 나온다 · 0abf4965e · 954623ca4 · 60e510332 · d96ba6417 = 스크래치 커밋 · push 안 함)

### 4-4 정직하게 적어 둘 것

- **root 로만 돌았다** — C13b 는 root 라 INFO (권한 무시) · C16 모드 000 의 기대는 `os.access` 로 정했다 (A11 의 능력 뺀 uid 0 에서 unreadable 길 확인).  진짜 비 root 사용자 (kgy · gabia 의 실행 사용자일 것 · 미확인) 로는 못 돌렸다 — 스크래치 폴더가 root 0700 이라 다른 uid 가 못 들어간다.
- **C99 WARN (A1 · A2)** = 그 13 s 사이 메인 세션 게이트가 `scripts/__pycache__/test_ca_ext_runner.cpython-38.pyc` 등을 썼다 (점검 도구가 import 하지 않는 시험 모듈) · strace 감사 (A7 · A7b) 로 이 블록의 쓰기 0 건 확인 — 다른 프로세스가 같은 체크아웃을 쓰면 현장에서도 같은 WARN 이 난다.
- **실행 중 HEAD 가 바뀌었다** — 메인 세션이 `7cdc78111` → … → `abf0911eb` 로 커밋 (그 사이 `db8322e70` 이 `scripts/rint_r_chain.py` 를 고침).  첫 판 A12 · A7b · A13 은 처음 읽은 PIN 으로 돌아 `STOP: HEAD abf0911eb… differs from PIN 7cdc78111… (nothing written)` 으로 막혔다 (원 출력 = 스크래치 · 커밋 안 함) — 그 뒤 PIN 을 다시 읽어 돌린 결과가 위 표.  A1 · A2 · A7 · A8 = `7cdc78111` · A12 · A13 · A7b = `abf0911eb` — 두 핀 모두에서 점검 도구가 돈다.
- 이 블록이 리포에 남긴 것: 없음 (git status 깨끗 · `.git/index` mtime 그대로 · strace 0 건).  리포 HEAD 변화 = 메인 세션 커밋 (이 작업 아님).
- 첫 탐색 때 `scripts/test_rint_r_chain.py --only GR` 을 `-B` 없이 한 번 돌렸다 (출력 = 스크래치 · 커밋 안 함) — 그 직후 `scripts/__pycache__` 폴더 mtime 이 그 실행 전 값 (05:43:16 UTC) 그대로였다 = 새 · 바뀐 `.pyc` 없음 (pyc 를 만들면 폴더 mtime 이 바뀐다).  그 밖 리포 접근 = `git show` · `git archive` · `git diff` · `git log` · `git status` (`GIT_OPTIONAL_LOCKS=0`) 읽기뿐.
- 이 컨테이너에는 NFS · CIFS · FUSE 가 없다 — 네트워크 FS 길 (C26 WARN 분류 · 마운트 옵션 거르기 · C16b) 은 단위 확인만 (`is_netfs('nfs4') = True` · `ext4 = False` · `addr=` · `clientaddr=` 옵션 제거) · 실제 NFS 동작은 안 봤다.
- GPU 없음 → C28 WARN (현장에서는 INFO 가 기대).

### 4-5 짧은 블록 시험 (11-09 · 리포 반입 판 · 시험 도구 = 스크래치 · 요약 `container_test/summary_short.txt`)

시험 핀 = 스크래치 사본 커밋 0a7f77f80 (push 안 함) = `abf0911eb` + 이 폴더의 `tools/siteq_probe.py` 하나 (README · 기록 없음 — 이 커밋과는 문서만 다르고 사슬 · 도구 바이트 같음).  기준 체크아웃 = 이 리포의 `git clone --no-checkout` 사본 (원격 = 이 리포 경로 · 블록의 fetch · worktree add 를 그대로 탐) · venv = PATH 심 (uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 = kgy 판) · 홈 = 시험마다 새 폴더.

| # | 조건 | 결과 | 판단 |
|---|---|---|---|
| S1 | kgy 블록 · py3.8 | rc 0 · PASS 24 · INFO 8 · WARN 1 (C28 · GPU 없음) · 14.6 s · 끝난 뒤 작업 트리 깨끗 · HEAD = 시험 핀 | 기대대로 |
| S2 | gabia 블록 · py3.8 · 계획 폴더 없음 | rc 0 · PASS 24 · INFO 8 · WARN 1 (C28) · 13.1 s | 기대대로 |
| S3 | S1 다음 같은 날 같은 홈에서 다시 | rc 2 · `STOP: … dem-siteq-<핀> already exists (nothing written)` · 홈 목록 전후 같음 | 막힘 확인 |
| S4 | PIN 자리표 그대로 | rc 2 · `STOP: PIN is not a 40-hex commit (nothing written)` · 홈 그대로 | 막힘 확인 |
| S5 | 맞는 꼴의 없는 커밋 | rc 2 · `STOP: git worktree add failed` · 홈 그대로 (작업 트리 · 결과 폴더 없음) | 막힘 확인 |
| S6 | venv 없음 | rc 2 · `STOP: venv not found … (nothing written)` · 홈 그대로 · fetch 전 | 막힘 확인 |
| S7 | 커밋 안 도구 한 글자 바뀐 핀 (스크래치 380c06f8c) | rc 2 · `STOP: probe sha256 differs (probe not run)` · 결과 JSON 없음 · 남은 것 = 새 작업 트리 + 도구 사본만 든 결과 폴더 | 막힘 확인 (도구는 안 돌았다) |
| S8 | py3.11 (venv 가 PATH 를 안 바꿈) | rc 1 · FAIL 1 = **C02** (kgy 판 아님) · PASS 23 | 기대대로 |
| S9 | `bash -i` 가 블록을 표준입력으로 읽음 (붙여 넣기 꼴) | rc 0 · PASS 24 · INFO 8 · WARN 1 | 문제 없음 |

- 끝난 뒤 시험 폴더 아래 남은 프로세스 0 · 이 리포 HEAD · 상태 무변경 (`abf0911eb` · 상태 줄 0).
- C04 코드 키: S1 (kgy) = S2 (gabia) = a25e1f2c… (같은 핀 · 같은 판) · 긴 블록 A12 (핀 `abf0911eb`) = 431ba14b… — 사슬 파일 바이트가 같아도 **핀이 다르면 키가 다르다** (`code_key` 가 HEAD 를 담음 · 의도된 설계) ⇒ 두 기계는 같은 핀으로 돌려야 §3-3 대조가 SAME 이 된다.

## 5. 현장 자격으로도 증명하지 못하는 것 (남는 몫)

| 남는 것 | 왜 점검이 못 보나 | 그대로 남는 위험 (추정) |
|---|---|---|
| 실제 **쓰는 도중** SIGKILL · 전원 손실 (원장 `ab` 덧붙임 · `os.replace` · 첫 결과 표지) | 블록은 쓰기 사이에 사슬 부모를 죽이지 않는다 (C12 = 기다리는 중 SIGKILL) · 전원 손실은 흉내 못 냄 | 반쯤 쓴 원장 줄 → 원장 꼴 멈춤 (사람 처리) · rename 미영속 (폴더 fsync 없음 · F1) |
| 실제 **OOM kill** (커널 OOM killer · cgroup `memory.max`) | 메모리를 일부러 다 쓰지 않는다 (C25 = 기록만) | 로그에 자원 낱말 없음 → `runner_rc` → 자동 재실행 없음 (E3) · 부분 payload |
| 실제 **디스크 가득** (ENOSPC) | 채우지 않는다 (C26 = 남은 공간 기록만) | `No space left on device` 가 로그에 남는지 · 원장 git 이 반쯤 커밋되는지 |
| **여러 시간** 런 | 블록 = 15–45 s | 벽시계 상한 (E4) · 시계 이동 · 장시간 /proc 스캔 · 로그 크기 · 잠금 대기 120 s 넘김 |
| **두 기계가 한 원장을 같이 쓰는** 경우 (NFS 공유 · git push/pull) | 한 기계의 flock 만 본다 · 원장 공유 방법이 문서에 없다 (**미확인**) | 호스트 사이 배타 없음 · 갈라진 원장 (사슬이 조상 대조로 멈추게 함 — 코드상) |
| 실제 **러너 · payload · GPU** (CUDA 오류 · `.unchecked` → `mv` · 첫 결과 표지 · cupy 메모리) | 풀이 금지 (블록 = 가짜 러너 bash) · e2e (`scripts/test_rint_r_chain_e2e.py` E13 · E15 = 실제 러너 kill · recover · 재실행) 은 payload 를 돌려 이 블록에서 뺐다 | CUDA 오류 낱말 분류 (E3) · 표지 영속성 (F3) |
| **진짜 비 root 사용자 · 진짜 ssh 세션 · tmux · cron** 아래 표지 스캔 | 블록은 붙인 그 셸 하나에서만 본다 (C08 옛 규칙 unsure 수는 그 순간 기록) | 다른 띄우기에서 보이는 프로세스 · environ 읽기 다름 |
| setsid 로 세션을 벗어나고 부모까지 끝났으며 environ 도 못 읽는 자손 | 사슬 자신의 한정 (RRC `group_members` 머리말 2667–2668) | 그런 자손은 못 본다 (러너 · payload 는 그러지 않는다 — 코드 주석) |
| pid 재사용 경합 (짧은 창) | 블록은 몇 초 · pid_max 기록만 | `chain_parent_alive` · `_run_session_ours` 판별의 경합 |
| 메인 세션 · 다른 사용자 프로세스가 **동시에** 같은 체크아웃 · 원장을 쓰는 경우 | 블록 시간에 우연히 겹친 것만 보인다 (C99) | 코드 지문 · 원장 경합 |
| Codex 가 따로 남긴 것 | 이 블록 범위 밖 | S0 단계 1 실침대 채택 (SELF-155) · 12 단위 끝-끝 · 합치기 · 새 계획 / 핀 봉인 · 숫자 · 실행 정책 · 연구 실행 승인 (round3 판정문 184 줄 · round4 148 줄) |
| 봉인 핀에서 사슬 · 계약 · 러너가 바뀐 경우 | 점검은 블록이 고른 핀의 사슬 함수로 본다 | 그 핀을 대표하지 않는다 → 봉인 핀으로 짧은 블록을 다시 (PIN 한 줄) |

## 6. 준비 중 찾은 사실 · 1저자 결정 (11-09)

1저자 11-09 *"q1 nohup으로 하면돼 이런건 신경안써도돼 / 나머지는 권고대로 하고 q5 관련해서 각각 필요한 명령어 있으면 주고"*.

| # | 찾은 것 (상태) | 1저자 결정 | 남는 한정 |
|---|---|---|---|
| Q1 | **`nohup` 만으로 띄우면 ssh 끊김 SIGHUP 을 막지 못한다 (확인)** — 사슬은 러너를 기다리는 동안 SIGTERM · SIGHUP 처리기를 건다 (RRC:2842–2853 · 2902 — 무시 (SIG_IGN) 여도 덮어씀).  이 컨테이너 확인: `nohup python3 …` 아래 SIGHUP = 무시 → 기다리는 동안 사슬 처리기 → 끝나면 무시로 복원 | **nohup 그대로** (권고였던 tmux 대신 · *"신경안써도돼"*) | ssh 가 끊기면 그 런은 원인 `signal` 로 멈추고 끝 기록을 남긴다 (틀린 결과를 받아들이는 길 아님 · 재실행 자격 원인) → 재개로 이어 간다 · 시간만 잃는다 |
| Q2 | **실제 커널 OOM kill (추정)** — OOM killer 는 러너 로그에 `MemoryError` 등 자원 낱말을 남기지 않음 → 러너 rc 길 → `runner_rc` (자동 재실행 자격 없음) | **권고대로 = 그대로 · 한정** (멈추는 쪽 = 11-09 처분 기준상 고칠 대상 아님) | rc 137 로 끊긴 런은 사람이 `dmesg` 를 보고 재실행을 정한다 (자동 아님) · 자원 낱말 규칙 (등록 R §10-5) 무변경 |
| Q3 | **`git_identity` · `plan_commit_problem` 의 git 호출에 시간 상한이 없다 (코드 사실 · RRC:959 · 965 · 971 · 1775 · 1779)** — 원장 git (120 s) · `_git_top` (60 s) 과 다르다 | **권고대로 = 한정만** (고치지 않음 · 리포 무변경) | 느린 FS 에서 단계가 끝없이 기다릴 수 있다 (추정) · 현장 점검 C22 가 git 시간을 기록 → 느린 FS 가 나오면 그때 고친다 |
| Q4 | 언제 돌릴까 | **권고대로 = 지금 · Codex 회차 ⑤ 와 나란히** — 이 커밋 push 뒤 짧은 블록 (§3) | 봉인 핀에서 사슬이 바뀌면 그 핀으로 다시 (머리 · §5) |
| Q5 | gabia 의 리포 자리 · venv 는 kgy 와 같다고 가정했다 (미확인) | **명령 줌 → 1저자가 두 기계에서 돌림** (조사 · gabia venv 만들기 · 패키지 맞춤 · §7) | gabia 사슬 venv 는 11-09 새로 만든 것 (kgy 와 판 같음 · 빌드 다름) |

기록만 (결정 거리 아님):
- 판정 `verdict.json` 은 원자적 쓰기가 아니다 (`write_json` RRC:6434–6435 · 단계 요약 · 그룹 기록은 원자적).
- 점검 도구는 `-I -B` 로 돈다 — 생산 명령 (`python3 <체크아웃>/scripts/rint_r_chain.py …`) 과 PYTHON* env 처리만 다르다 (C23 이 두 꼴을 다 본다).
- **gabia 는 root 로 돈다 (확인 · §7)** — C13b (읽기 전용 원장) · C16 모드 000 같은 권한으로 막는 보호는 root 에서 뜻이 없다 (권한 무시 · INFO) · 표지 스캔은 모든 프로세스의 environ 을 읽을 수 있어 `unsure` 가 줄어든다 (추정).  §4-4 "root 로만 돌았다" 한정과 같은 부류 — kgy (일반 사용자) 결과가 비 root 길을 대표한다.

## 7. 기계 조사 기록 (11-09 · 1저자가 두 기계에서 돌려 붙여 넣은 출력 · 기계 이름 · 주소 · 사용자 이름은 쓰지 않음)

| 칸 | kgy | gabia |
|---|---|---|
| 실행 사용자 | 일반 사용자 (root 아님) | root |
| CPU | Intel Core i9-11900K · 16 논리 코어 · avx512f 있음 | Intel Xeon Silver 4210R · 20 논리 코어 · avx512f 있음 |
| 메모리 | 62 GB | 62 GB |
| 홈 디스크 남음 | 98 GB (사용 89 %) | 199 GB (사용 51 %) |
| GPU | RTX 3090 24 GB | RTX A6000 48 GB · 드라이버 595.58.03 |
| git · 띄우기 도구 | 2.25.1 · setsid · tmux | 2.43.0 · setsid · tmux |
| 사슬 파이썬 | dem-venv = Python 3.8.10 (우분투 빌드) | dem-venv = Python 3.8.10 (conda-forge 빌드 · 11-09 새로 만듦 · 시스템 python3 = miniforge 3.13 · numpy 2.4.4 는 사슬에 안 씀) |
| numpy · scipy | 1.24.4 · 1.10.1 | 1.24.4 · 1.10.1 |
| numpy BLAS | 휠 openblas64_ · OpenBLAS Core = SkylakeX | 휠 openblas64_ · OpenBLAS Core = SkylakeX |
| pip freeze | 22 개 (아래) + pkg_resources 0.0.0 (우분투 venv 흔적) | 22 개 (아래 · 이름 · 판 같음 · Pygments 표기만 소문자) |
| cupy · taichi | cupy-cuda12x 12.3.0 · taichi 1.7.0 | 같음 · cupy GPU 1 · 합 시험 45.0 · taichi (1, 7, 0) |

pip 22 개 (두 기계 같음): astunparse 1.6.3 · colorama 0.4.6 · cupy-cuda12x 12.3.0 · dill 0.4.0 · fastrlock 0.8.3 · imageio 2.35.1 · markdown-it-py 3.0.0 · mdurl 0.1.2 · networkx 3.1 · numpy 1.24.4 · packaging 26.2 · pillow 10.4.0 · pyamg 4.2.3 · pyflakes 3.2.0 · Pygments 2.19.2 · PyWavelets 1.4.1 · rich 14.3.4 · scikit-image 0.19.3 · scipy 1.10.1 · six 1.17.0 · taichi 1.7.0 · tifffile 2023.7.10.

- 두 기계 BLAS 계산 경로 = 같음 (OpenBLAS Core SkylakeX 둘 다 · `OPENBLAS_VERBOSE=2` 출력) ⇒ RCA-07 칼날 (OpenBLAS AVX-512 ↔ AVX2 경로 차이) 은 이 두 기계 사이에는 생기지 않는다 (관찰) · `OPENBLAS_CORETYPE` 고정 = 불필요 (기록 · 결정 아님).
- 파이썬 빌드는 다르다 (우분투 ↔ conda-forge) — 사슬의 환경 같음 단위 (`env_unit` = 파이썬 minor · numpy · scipy) 는 같다 · 패치 판 · 빌드 차이가 숫자에 미치는지는 R 런 · 12 단위 끝-끝 몫 (미확인).
- 기준 체크아웃: kgy = 10-24 작업 트리 (S0 단계 1 블록과 같은 자리) · gabia = 홈의 리포 클론 (다른 가지에 체크아웃돼 있음 · 블록은 그 작업 트리를 건드리지 않고 fetch · worktree add 만).

## 8. 파일

- `docs/reviews/rint2_siteq_prep_20261109/README.md` — 이 문서 (준비 문서 SITEQ_PREP.md 에서 긴 블록 둘을 빼고 §3 · §4-5 · §6 · §7 을 새로 씀 · §1 · §2 표 · §4-1 – §4-4 · §5 = 준비 문서 그대로)
- `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` — 점검 도구 (sha256 a490b9ad… · 1,147 줄 · ASCII · `!` · TAB 없음 · pyflakes 0)
- `docs/reviews/rint2_siteq_prep_20261109/container_test/short_block.tmpl` — 짧은 블록 틀 (자리 넷 · 대화로 주는 블록 = 이 틀에 채운 것)
- `docs/reviews/rint2_siteq_prep_20261109/container_test/summary.txt` — 긴 블록 컨테이너 시험 요약 원문 (§4-2 · §4-3)
- `docs/reviews/rint2_siteq_prep_20261109/container_test/summary_short.txt` — 짧은 블록 컨테이너 시험 요약 원문 (§4-5)
- `docs/reviews/rint2_siteq_prep_20261109/SHA256SUMS` — 위 파일들 (자기 빼고)
- 11-10 (Codex Rint ② 회차 ⑥ `RR6-01` · `RR6-02`): `SHA256SUMS` 를 지금 바이트로 다시 썼다 — `tools/siteq_probe.py` = RR6-01 고침 (C02b 가 자식 rc 0 을 요구 · `path_python3_rc` 기록) · `tools/test_siteq_c02b.py` 추가 (고치기 전 5/10 → 뒤 10/10 · 게이트 단계) · 이 README = 이 줄과 결과 안내가 더해진 판.  두 현장 기록 (kgy · gabia 11-09 · `docs/data/rint2_siteq_20261109/`) 이 쓴 판은 역사로 남긴다: 도구 `a490b9adc3eeb7468b051b32bdaa0110879b71322a3a2cfb3b723505a3df8588` · README `6401d4f9a2850946588e4929326c13ff319827720f47f55165f69c748f7859f2` (db86ce9b9).  그 두 기록의 C02b 는 자식 rc 를 기록하지 않은 판의 결과라 PATH python3 자식의 정상 종료 증서가 아니다 (판정문 `docs/reviews/codex_review_rint2_rr_round6_20261110.md` §4).
- 리포 밖 (스크래치 · 커밋 안 함): 긴 블록 둘 · 블록 생성기 · 시험 도구 · strace 원 로그 · 시나리오 출력 · 결과 JSON · 줄 번호 기준 사본
- 11-11 (계획 §10 의 2 번 · 1저자 11-10 Q1 · Q6 · Q8): 틀 고침 + nohup 꼴 + 컨테이너 시험 = §9 · `SHA256SUMS` 를 지금 바이트로 다시 썼다 (새 파일 셋 더함 · §9-9).  11-09 판 틀 (sha256 bc117ba6…) 은 리포 이력 (`db86ce9b9`) 에 그대로 남는다.

## 9. 11-11 판 — 틀 고침 · nohup 꼴 · 컨테이너 시험

> 할 일의 자리 = `docs/reviews/rint2_siteq_remaining_plan_20261110.md` §10 의 2 번 · 1저자 11-10 결정 Q1 (kgy 실행 셸 umask 022 + 실제 파일 · 폴더 모드 확인) · Q6 (현장 확인을 nohup 문맥으로도) · Q8 (블록 종료 코드를 파일로도) = 같은 문서 §0-2.
> 바뀐 것 = 이 폴더의 틀 · 시험 · 이 README · `SHA256SUMS` 뿐.  점검 도구 `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` (sha256 c455c792…) · `scripts/` · 계획 · 원장 무변경.  풀이 · 값 (σ) 과 무관하다 (블록 = 읽기 전용 현장 점검).
> 11-09 기록 (§2 – §7 · 결과 `docs/data/rint2_siteq_20261109/` · 핀 `db86ce9b9`) 은 그대로 둔다 — 그 기록은 옛 틀 (§9-1 의 "앞" 칸) 로 돈 것이다.  §2 · §3 의 블록 설명 (fetch 가지 · 해시 · 채우는 칸 넷) 도 그 판의 설명이다.

### 9-1. 틀에서 바뀐 줄 (앞 = 11-09 판 23 줄 → 뒤 = 96 줄)

| 자리 | 앞 | 뒤 | 까닭 |
|---|---|---|---|
| 도구 해시 줄 | PROBE_SHA = a490b9ad… (11-09 도구) | c455c792… (지금 도구 · 직접 잰 값 = 이 폴더 `SHA256SUMS` 의 tools/siteq_probe.py 줄) | 계획 §2-2 C8 · §9 어긋남 1 |
| fetch 가지 | `claude/sdcp-dem-manuscript-si-pqwtv8` | `claude/stoic-knuth-NObVQ` | 계획 §9 어긋남 2 |
| 채우는 칸 | 넷 (PIN · 기계 · 기준 체크아웃 · 계획 폴더) | 일곱 (+ 원장 저장소 · 출력 바탕 · 계획 파일 · §9-2) | 계획 §2-3 A2 · §5-2 "도구 밖" 행 |
| 작업 트리 · 결과 폴더 이름 | dem-siteq-<핀 9 자리> · rint_siteq_<기계>_<UTC 날짜> | 같은 이름 + 끝에 `${SITEQ_TAG:-}` (짧은 꼴 = 빈 값 → 이름 그대로 · nohup 꼴 = _nohup) | 두 꼴을 같은 날 같은 홈에서 (N4) |
| STOP | 화면 한 줄 · rc 2 | 같음 + 결과 폴더가 생긴 뒤의 STOP 이면 rc 파일도 | Q8 |
| 끝 | 화면 끝 줄 `[siteq] rc …` | 화면 끝 줄은 글자 그대로 · 그 바로 앞에서 rc 파일을 쓴다 | Q8 |
| 새로 든 줄 | — | 머리: 블록 시작 때 umask 를 기억 · 꼴 B 자리 (주석 한 줄) / 도구 앞: 모드 목록 (파이썬 63 줄 · 읽기 전용 · 화면에도 찍음) · 환경 기록 한 줄 (umask · SIGHUP 무시 여부) | Q1 · Q6 |
| 그대로 | 같은 줄 | 관문 셋 (PIN 꼴 · 자리 없음 · venv) · worktree add · HEAD 대조 · 해시 대조 · **도구 호출 줄** · 결과 sha256 줄 · exit · ASCII · `!` 없음 · TAB 없음 | — |

### 9-2. 채우는 칸 (기계마다 채운 블록을 대화로 준다 · 주소 · 사용자 이름 · 리포 밖 경로는 리포에 쓰지 않는다)

| 칸 | 뜻 | 블록이 쓰는 곳 | 비었을 때 |
|---|---|---|---|
| @@PIN@@ | 40 자리 커밋 = 단일 개정 커밋 그 자체 (계획 §0-2 Q1) | 작업 트리 · 도구 --pin | STOP (S4) |
| @@MACHINE@@ | kgy · gabia | 결과 폴더 이름 · 도구 --machine | — |
| @@BASE@@ | 기준 체크아웃 (kgy = 10-24 작업 트리 · gabia = 홈의 리포 클론 · §3-1 그대로) | fetch · worktree add | — |
| @@PLAN@@ | 계획 폴더 (여럿이면 `:` 로 잇기) — 뜻은 11-09 와 같다 | 도구 --plan-dirs (C26) **와** 모드 목록 | not-given 줄 · C26 계획 폴더 행 없음 (S2) |
| @@LEDGER@@ | 원장 git 저장소 | 모드 목록만 | not-given 줄 |
| @@OUTBASE@@ | R 런 출력 바탕 | 모드 목록만 | not-given 줄 |
| @@PLANFILE@@ | 계획 파일 (봉인할 JSON 의 사본) | 모드 목록만 | not-given 줄 |

- 경로는 $HOME/… 꼴로 채운다 — 블록이 큰따옴표 안에서 펼친다.  ~ 로 채우면 펼쳐지지 않아 missing 으로 적힌다.
- kgy 의 문서 꼴 (계획 §4-3 · 명령 문서 `docs/reviews/rint2_kgy_commands_20261020.md` 487 · 501 – 506 · 531 줄): 계획 사본 = sdcp 아래 ca1_plan.json · 원장 = sdcp 아래 ca1_ledger · 한 기계 predict 바탕 = sdcp 아래 ca1_predict.  12 단위 시도 바탕 이름 · gabia 의 자리 = 문서에 없음 (계획 §8) → 1저자가 정해 채운다.
- 원장 · 출력 바탕의 파일 체계도 C26 으로 보려면 PLAN 에 `:` 로 이어 넣는다 (계획 §2-1 R3).  그 경로가 아직 없으면 C26 detail 에 plan dirs missing 이 붙어 계획 R1 의 통과 기준과 맞물린다 → 있는 경로만 넣는다.

### 9-3. 결과 폴더에 새로 생기는 파일 (돌려받을 것)

| 파일 (결과 폴더 안) | 언제 · 누가 | 내용 (한 줄 · ASCII) | 돌려받나 |
|---|---|---|---|
| siteq_result.json · siteq_result.json.sha256 · siteq.log | 도구 · 블록 (11-09 와 같음) | — | 예 |
| siteq_block_rc.txt | 블록 끝 (화면 끝 줄 바로 앞) · 결과 폴더가 생긴 뒤의 STOP | rc=<종료 코드> end_utc=<UTC 시각> · STOP 이면 끝에 " stop=<STOP 문구>" · 임시 이름으로 쓴 뒤 mv (반쯤 쓴 파일이 보이지 않는다) | 예 |
| siteq_block_env.txt | 도구를 띄우기 바로 앞 · 같은 셸 | umask_start=<블록 시작 때> umask_probe=<도구를 띄울 때> sighup_ignored=yes·no·unknown (블록 셸의 /proc/<pid>/status SigIgn 에서 SIGHUP 비트) | 예 |
| siteq_block_modes.txt | 도구 앞 (읽기 전용) | §9-4 | 예 |
| siteq_probe.py · c09_… – c19_… 폴더 | 블록 · 도구 | — | 아니오 (11-09 와 같음) |

- rc 파일의 값 = 블록 종료 코드 = 화면 끝 줄의 값 (도구 rc 0 · 1 또는 STOP 2 · S1 · S8 · S7).
- rc 파일이 없는 경우 = ① 결과 폴더가 생기기 전의 STOP (화면 메시지만 · 11-09 와 같은 "nothing written") ② 블록이 신호 · 메모리 부족 등으로 죽음 (S10).  rc 파일 하나로는 둘을 가르지 못한다 (① 이면 결과 폴더도 없다).  nohup 꼴은 발사 폴더의 nohup_rc.txt 가 ① 을 덮는다 (§9-5).
- 도구의 C18 은 같은 셸에서 띄운 도구가 잰 값이다 → umask_probe 와 같아야 한다 (S1 · S1b · S1c 에서 같음 · 시험이 숫자로 대조).

### 9-4. 모드 목록 (siteq_block_modes.txt)

머리 줄 하나 (`# siteq block modes v1 utc=… runner=root|non-root …`) + 경로마다 한 줄.  칸 = 공백으로 나눈 key=value · path 는 맨 끝 (경로에 공백이 있어도 앞 칸이 흔들리지 않게).  S1 의 실제 출력:

```
tag=plan kind=dir mode=0775 owner=self group=self-primary group_write=yes other_write=no acl_extra=0 acl_default=0 group_others=0 link=no path=~/sdcp
tag=ledger kind=missing path=~/sdcp/ca1_ledger
tag=outbase kind=dir mode=0777 owner=other group=other group_write=yes other_write=yes acl_extra=0 acl_default=5 group_others=0 link=no path=~/sdcp/scripts
tag=planfile kind=file mode=0664 owner=other group=other group_write=yes other_write=no acl_extra=2 acl_default=- group_others=1 link=no path=~/sdcp/ca1_plan.json
tag=siteq_out kind=dir mode=0755 owner=self group=self-primary group_write=no other_write=no acl_extra=0 acl_default=0 group_others=0 link=no path=~/rint_siteq_kgy_20261111
```

| 칸 | 뜻 |
|---|---|
| tag | 칸 이름 (plan · ledger · outbase · planfile) · siteq_out = 블록이 이번에 만든 결과 폴더 (지금 umask 가 새 폴더에 준 모드 — 계획 §0-3 "새 출력 폴더 · 파일의 모드를 목록으로") |
| kind | dir · file · other · missing (없음 — 멈추지 않는다) · not-given (칸이 비었음) |
| mode | 4 자리 8 진 (setgid · sticky 비트 포함) |
| owner | self = 실행 UID 와 같음 · root = UID 0 · other — 이름도 숫자도 찍지 않는다 |
| group | self-primary = 실행 사용자의 주 그룹 · self-member = 보조 그룹 · root = GID 0 · other — 이름 · 숫자 없음 |
| group_write · other_write | 모드 비트 g+w · o+w |
| acl_extra | 접근 ACL 항목 수 − 기본 셋 (소유자 · 그룹 · 기타) · 0 = 추가 없음 (ls -l 의 + 표시 없음) · unsupported = 그 파일 체계가 POSIX ACL 을 모름 (확장 속성 system.posix_acl_access 를 읽는다) |
| acl_default | 폴더의 기본 ACL 항목 수 — 있으면 그 안에 새로 생기는 파일 · 폴더가 umask 대신 이것을 물려받는다 · 파일은 - |
| group_others | 그 그룹에 든 다른 계정 수 = 그룹 항목의 구성원 + /etc/passwd 에서 그 그룹이 주 그룹인 계정 − 실행 계정 · 숫자 하나만 (계획 §8 의 "그룹의 다른 구성원 [미확인]" 에 쓰는 칸) |
| link | 경로 자체가 심볼릭 링크인지 (모드 · 소유는 따라간 대상의 것) |
| path | 홈 아래면 ~ 로 바꿔 적는다 |

- 준 경로 그 자체만 본다 — 하위 폴더 · 파일은 훑지 않는다.  계획 §0-3 의 "이미 있는 777 폴더는 R 출력 자리로 쓰지 않는다" 는 그 자리를 칸에 넣었을 때 other_write=yes 로 드러난다 (S1 의 outbase).
- 기준 숫자는 정하지 않는다 (계획 §2-3 A2 "모드 숫자 기준 문서에 없음" 그대로) — 판단 = 1저자.

### 9-5. nohup 꼴 (`docs/reviews/rint2_siteq_prep_20261109/container_test/short_block_nohup.tmpl` · 105 줄)

하는 일:

1. 붙이면 홈 아래 새 발사 폴더 (rint_siteq_nohup_<UTC 시각>) 를 만들고, 짧은 꼴의 안쪽 94 줄을 글자 그대로 block.sh 로 쓴다 (채운 칸도 같은 자리 · 같은 값).
2. 발사 폴더에서 `SITEQ_TAG=_nohup nohup setsid bash -c '…'` 로 띄운다 — 입력 /dev/null · 출력 nohup.log · 자기 pid → nohup_pid.txt · block.sh 가 끝나면 그 종료 코드 → nohup_rc.txt (임시 이름 → mv).
3. pid 파일이 생기면 (최대 10 s) 한 줄 (`[siteq] nohup start: pid … - log … - finished when …/nohup_rc.txt exists …`) 을 찍고 셸로 돌아온다 → 셸을 닫아도 된다.
4. 끝났나 = 발사 폴더에 nohup_rc.txt 가 있나 · 진행 = nohup.log · 결과 = 결과 폴더 rint_siteq_<기계>_<날짜>_nohup (작업 트리도 …_nohup).
5. 보낼 것 = 그 결과 폴더의 파일 (§9-3) + 발사 폴더의 nohup.log · nohup_rc.txt.

| 조건 (지시서) | 어떻게 | 확인 (§9-7) |
|---|---|---|
| (가) 출력이 핀 작업 트리 밖에 남는다 | 발사 폴더 · 결과 폴더 = 홈 아래 · 띄우는 자리 = 발사 폴더 · 출력을 nohup.log 로 직접 돌린다 (nohup.out 이 생기지 않는다) | N1 – N4: 작업 트리 깨끗 · 홈 아래 nohup.out 0 개 · 발사 폴더 = 파일 넷뿐 · C5 확인 = 사례 NO |
| (나) 끝났는지 · 종료 코드를 파일로 | 발사 폴더 nohup_rc.txt (결과 폴더가 생기기 전의 STOP 도 덮는다) + 결과 폴더 siteq_block_rc.txt | N1 – N4: 둘 다 rc=0 |
| (다) 붙인 셸이 끊겨도 끝까지 | nohup = SIGHUP 무시를 물려줌 · setsid = 작업이 처음부터 다른 세션 · 다른 프로세스 그룹 (끊김 신호가 그룹 단위로 닿지 않는다) | N2 · N3 PASS · 대조: S10 (짧은 꼴은 끊김에 죽는다) · M4 · M5 · 관찰 O1 |
| (라) 도구 호출 줄 · 검사 집합이 같다 | 본문 = 짧은 꼴의 안쪽 줄 그대로 (꼴의 차이 = 본문 앞뒤의 발사 줄뿐 · SITEQ_TAG 도 발사 줄에서 준다) | T0 (줄 단위로 같음 · 도구 호출 줄 1 개씩 같음) · S1 ↔ N1 검사 ID 33 개 같은 순서 |

**setsid 를 넣은 까닭 (관찰 · O1 = 이 컨테이너에서 돌린 다섯 번 모두 같은 꼴 · 요약 파일 = 마지막 한 번 · 앞선 넷 = 스크래치 · 커밋 안 함)**: nohup 만으로 띄운 작업의 프로세스 그룹에 SIGHUP 이 오면 (N2 꼴 — 발사 셸이 세션 우두머리였다가 끝남) 블록 bash · 파이썬은 무시하지만, `git worktree add` 가 띄운 자식 git reset 이 신호 1 로 죽었다 — nohup.log: `error: reset died of signal 1` → `[siteq] STOP: git worktree add failed` · rc 2.  nohup 은 "무시" 를 물려줄 뿐이고, 스스로 신호 처리기를 거는 프로그램 (git · 사슬의 run_in_group = §6 Q1) 이 exec 로 띄운 자식은 기본 동작 (종료) 으로 돌아간다 (POSIX exec 규칙 · 메시지는 관찰 그대로).  setsid 를 더하면 같은 시험 (N2) 에서 끝까지 돈다.  M5 (nohup 빼고 setsid 만) 도 끝까지 돌지만 SIGHUP 무시 문맥이 없어진다 (sighup_ignored=no).
⚠ 생산 발사 줄 (nohup · 줄의 꼴은 문서에 없음 · 계획 §8) 에도 같은 일이 생길 수 있다 — 끊김 SIGHUP 이 사슬의 프로세스 그룹에 닿으면 사슬은 원인 signal 로 멈추고 (§6 Q1) git 의 자식도 죽을 수 있다 (멈추는 쪽 · 시간만 잃는다 · 추정).  발사 줄을 정할 때 함께 본다 (setsid · 출력 명시 돌림 · 작업 트리 밖에서 띄우기).

**계획 §2-2 C5 의 추정 → 확인 (NO)**:

| # | 조건 | 결과 |
|---|---|---|
| NO1 | 핀 작업 트리 안에서 · 출력이 터미널인 채로 nohup true | nohup: ignoring input and appending output to 'nohup.out' · 작업 트리에 nohup.out 이 생김 · `git status --porcelain --untracked-files=normal` = ?? nohup.out (dirty) · 리포 `.gitignore` 에 없음 (check-ignore rc 1) |
| NO2 | 같은 자리 · 출력을 다른 파일로 돌림 (> log 2>&1 < /dev/null) | nohup.out 없음 · 깨끗 |

⇒ 추정이 맞다: 출력이 터미널이면 nohup 은 지금 폴더에 nohup.out 을 만들고, 그 폴더가 핀 작업 트리면 사슬 · 도구가 쓰는 같은 git status 명령에 추적 안 된 파일로 잡힌다 (사슬 = CODE_PIN_MISMATCH · 도구 = C99 FAIL 의 꼴 · 계획 §2-2 C5 근거 줄).  nohup 꼴은 출력을 돌리고 작업 트리 밖에서 띄워 이를 피한다.

**같은 날 두 꼴**: 이름 끝의 `${SITEQ_TAG:-}` 로 짧은 꼴 (rint_siteq_kgy_<날짜>) 과 nohup 꼴 (…_nohup) 이 겹치지 않는다 — N4 = S1 뒤 같은 홈 · 같은 날 nohup 꼴 PASS · 짧은 꼴의 결과 파일 다섯 바이트 그대로.  같은 꼴을 같은 날 다시 = 11-09 와 같이 STOP (S3).

### 9-6. umask — 두 꼴 (틀 = 꼴 A · 꼴 B = 주석 한 줄 자리 · 1저자가 정한다)

| | 꼴 A — 기록만 (틀 지금) | 꼴 B — 블록 머리에서 umask 022 |
|---|---|---|
| 하는 일 | 붙인 셸의 umask 를 바꾸지 않는다 · umask_start = umask_probe (S1 · S1b) | 머리 주석 줄 (`# umask 022  # form B …`) 의 맨 앞 '# ' 두 글자를 지우면 블록이 022 로 둔다 · umask_start = 셸 값 · umask_probe = 022 (S1c: 0002 → 0022) |
| 도구 C18 이 보는 것 | 실행 셸의 값 그대로 (S1 = 022 · 새 파일 644 / S1b = 002 · 664) | 늘 022 (S1c: 셸 002 인데 C18 = 022 · 644) |
| 좋은 점 | 1저자 Q1 의 확인 대상 ("kgy 실행 셸 umask 022") 을 그대로 본다 · 계획 §5-1 의 선행 ("kgy 실행 셸에 umask 022") 이 지켜졌는지 드러난다 · 블록이 고쳐 놓고 숨기지 않는다 | 생산 발사 블록 머리에 umask 줄을 두는 꼴 (계획 §3 Q1 행) 과 같은 문맥 · 셸 설정을 잊어도 블록이 만든 폴더 · 파일 = 755 · 644 |
| 나쁜 점 | 셸에 022 를 먼저 두지 않으면 kgy 에서 C18 = 002 → 계획 A1 통과 기준 (umask 022, new file mode 644) 미달 → 셸을 고치고 블록을 다시 | C18 이 셸 상태의 증거가 아니게 된다 (블록이 둔 값) · 머리 줄이 없는 다른 실행 (손으로 다시 돌림 · recover 등) 은 셸 값으로 돈다 — 그것은 umask_start 로만 보인다 |
| 권고 | **꼴 A** — 셸 설정 (계획 §5-1 선행) 은 블록이 확인하고, 생산 발사 줄의 umask 줄 (계획 §3 Q1) 은 따로 둔다.  두 겹이면 어느 한쪽이 빠져도 드러난다. | |

### 9-7. 컨테이너 시험 (11-11 · 이 컨테이너 ≠ kgy · gabia)

돌리는 법 (PID 이름공간 안에서만 — 시험 스크립트는 자기가 PID 1 이 아니면 거부한다):

```bash
unshare -pf --mount-proc --kill-child python3 -I -B docs/reviews/rint2_siteq_prep_20261109/container_test/run_block_tests.py --work <리포 밖 새 빈 폴더> --summary <요약 파일>
```

| 칸 | 내용 |
|---|---|
| 스크립트 | `docs/reviews/rint2_siteq_prep_20261109/container_test/run_block_tests.py` (표준 라이브러리만 · root 필요 = chown · ACL 사례 · 리포는 git archive · git show 로 읽기만 · 쓰는 곳 = --work 와 --summary 뿐 · `--only` 로 사례 골라 돌림) |
| 환경 | Ubuntu 24.04 · 커널 6.18 · root · ext4 (POSIX ACL 됨) · GPU 없음 · git 2.43.0 · bash 5.2.21 · venv = uv CPython 3.8.20 에 --system-site-packages (numpy 1.24.4 · scipy 1.10.1 = kgy 단위 · 네트워크 0) · S8 용 venv = 3.11 (numpy 2.4.6 · scipy 1.17.1) |
| 가짜 origin | 리포 HEAD 의 `.gitignore` · `scripts/` · 도구 파일로 만든 저장소 · 커밋 셋 (날짜 · 이름 고정 → 같은 리포 판이면 같은 해시): O = scripts 만 · 가지 claude/sdcp-dem-manuscript-si-pqwtv8 (옛 틀이 받는 가지) → X = + 도구 c455c792… (정상 사례의 PIN) → Z = 도구 1 바이트 바꿈 · 가지 claude/stoic-knuth-NObVQ 의 끝 |
| 기준 체크아웃 | 사례마다 git clone --no-local --no-checkout — 보통 = 옛 가지만 받은 클론 (현장처럼 새 가지를 받은 적이 없는 체크아웃) · R2 · NO = 가지 전부 |
| 홈 | 사례마다 새 폴더 · kgy 꼴 = dem-ca1-89fc4 (기준) · dem-venv · sdcp (775 · 그 아래 scripts = 777 · 이름 없는 UID 소유 · 기본 ACL 5 항목 · ca1_plan.json = 664 · 이름 있는 계정 소유 · 접근 ACL 추가 2 항목 · ca1_ledger 는 만들지 않음) / gabia 꼴 = Yonghoon-DEM-DFT · dem-venv |
| 끊김 흉내 | pty 를 만들어 그 셸에 블록을 붙인 뒤 pty 의 주 쪽을 닫는다 (ssh 끊김과 같은 부류 · 같지는 않다) · 스크립트는 어떤 프로세스에도 신호를 보내지 않는다 (kill 호출 0 · 부모를 잃고 이 스크립트 (PID 1) 에 넘어온 프로세스는 waitpid 로 거두기만) |
| 요약 | `docs/reviews/rint2_siteq_prep_20261109/container_test/summary_short_20261111.txt` (작업 폴더 = <WORK> · 사례 홈 = ~ 로 가림) · 전체 287 s · overall PASS |

사례 (11-09 짝 = §4-5 표의 같은 번호):

| 사례 | 조건 | 기대 | 결과 |
|---|---|---|---|
| T0 | 정적: 두 틀 · 해시 · 본문 | PROBE_SHA = 도구 = `SHA256SUMS` · fetch 가지 = stoic · ASCII · `!` · TAB 없음 · 칸 일곱 · nohup 본문 = 짧은 꼴 안쪽 94 줄 · 도구 호출 줄 같음 · 발사 줄 꼴 · 꼴 B 줄은 주석 · 옛 틀 sha256 bc117ba6… 의 해시 · 가지 = 옛 값 | 14/14 |
| S1 | kgy · 셸 umask 022 · 칸 일곱 채움 | rc 0 · 끝 줄 그대로 · FAIL · ERROR 0 · WARN = C28 (GPU 없음) 뿐 · rc 파일 rc=0 · umask 0022 = C18 022 · 새 파일 644 · sighup no · 작업 트리 깨끗 · C26 계획 폴더 행 (있음 · 쓰기 가능 · 같은 FS · missing 주석 없음) · 모드 목록 다섯 줄 (§9-4) · 이름 · 숫자 · 홈 경로 없음 | 14/14 · PASS 24 · INFO 8 · WARN 1 (11-09 S1 과 같은 꼴) |
| S1b | kgy · 셸 umask 002 | S1 과 같음 · umask 0002 = C18 002 · 새 파일 664 · siteq_out 0775 | 14/14 |
| S1c | 꼴 B (주석 줄을 켬) · 셸 002 | umask_start 0002 · umask_probe 0022 = C18 022 · siteq_out 0755 | 14/14 |
| S2 | gabia · 계획 · 원장 · 출력 바탕 · 계획 파일 칸 빔 | rc 0 · not-given 넷 + siteq_out · C26 계획 폴더 행 없음 | 14/14 |
| S3 | S1 뒤 같은 홈 · 같은 날 · 같은 꼴 | STOP (dem-siteq-… already exists) · 홈 목록 그대로 · S1 의 rc 파일 바이트 그대로 | 4/4 |
| N4 | S1 뒤 같은 홈 · 같은 날 · nohup 꼴 | …_nohup 폴더로 끝까지 · rc 0 · S1 결과 파일 다섯 바이트 그대로 | 20/20 |
| S4 | PIN 자리표 그대로 | STOP (PIN is not a 40-hex commit) · 홈 그대로 · rc 파일 없음 | 3/3 |
| S5 | 꼴은 맞고 없는 커밋 | STOP (git worktree add failed) · 홈 그대로 | 3/3 (git: invalid reference) |
| S6 | venv 없음 | STOP (venv not found) · 홈 그대로 | 3/3 |
| S7 | 도구가 1 바이트 다른 PIN (Z) | STOP (probe sha256 differs) · 결과 폴더 = 도구 사본 + rc 파일 (rc=2 · stop=probe sha256 differs (probe not run)) · 결과 JSON 없음 | 4/4 |
| S8 | venv = 3.11 (kgy 단위 아님) | rc 1 · FAIL = C02 뿐 · rc 파일 rc=1 · 끝 줄 rc 1 | 14/14 · PASS 23 · FAIL 1 · INFO 8 · WARN 1 |
| S9 | bash -i 가 블록을 표준입력으로 읽음 (붙여 넣기 꼴) | rc 0 · rc 파일 rc=0 | 14/14 |
| R1 | **옛 틀** · 새 가지를 받은 적 없는 기준 체크아웃 | STOP (git worktree add failed) — 옛 가지를 받아도 PIN 이 없다 (가지 까닭) · 홈 그대로 | 3/3 (git: invalid reference) · 같은 꼴의 기준 체크아웃 (옛 가지만) 에서 새 틀 = S1 PASS |
| R2 | **옛 틀** · PIN 을 이미 가진 기준 체크아웃 | STOP (probe sha256 differs) — 도구가 c455c792… 로 바뀜 (해시 까닭) · 결과 폴더 = 도구 사본뿐 · rc 파일 없음 (옛 틀) | 4/4 |
| NO | 계획 §2-2 C5 | §9-5 표 | 3/3 |
| N1 | nohup 꼴 · 터미널 없이 띄움 | 발사 줄 · nohup_rc.txt rc=0 · 결과 폴더 rc 파일 rc=0 · sighup_ignored yes · 작업 트리 깨끗 · nohup.out 없음 · 발사 폴더 파일 넷 · 모드 목록 S1 과 같은 꼴 | 20/20 |
| N2 | nohup 꼴 · 발사 셸 = pty 세션 우두머리 (끝날 때 커널이 그 그룹에 SIGHUP) + pty 끊음 | 끝까지 · rc 0 | 20/20 |
| N3 | nohup 꼴을 pty 의 대화형 셸에 붙인 뒤 시작 줄이 나오면 pty 끊음 | 붙인 셸은 끊김으로 끝남 · 작업은 끝까지 · rc 0 | 20/20 |
| S10 | **대조**: 짧은 꼴을 pty 대화형 셸에 붙이고 도구가 도는 중 (C01 – C08 아홉 줄이 찍힌 뒤) pty 끊음 | 붙인 셸 끝남 · 30 s 뒤 rc 파일 · 결과 JSON 없음 (짧은 꼴은 끊김에 죽는다 = N2 · N3 시험이 끊김을 실제로 만든다) | 4/4 |
| (S1 ↔ N1) | 검사 집합 | 검사 ID 목록 같음 | 33 개 같은 순서 |

변이 (틀을 일부러 고장 내고 같은 시험 · 겨냥한 단언만 실패하고 나머지는 모두 성립해야 "옳은 까닭"):

| 변이 | 바꾼 것 | 실패해야 할 단언 | 결과 |
|---|---|---|---|
| M1 | 끝의 rc 파일 쓰기 줄 (`rcfile "$RC"`) 지움 · S1 꼴 | rc_file | rc_file 하나만 실패 (rc 파일 없음) · 옳은 까닭 |
| M2 | 해시 대조 줄 지움 · S7 꼴 (PIN = Z) | outer_rc · stop_message · rc_file · out_files | 넷만 실패 (바뀐 도구가 끝까지 돌아 rc 0 · STOP 없음 · rc 파일 rc=0 · 결과 폴더에 도구 산출물) · 옳은 까닭 |
| M3 | 모드 목록이 소유자 이름을 찍음 (이름 없으면 숫자) · S1 꼴 | modes_no_names | 그것 하나만 실패 (owner=root · 43219 · daemon 이 찍힘) · 옳은 까닭 |
| M4 | 발사 줄에서 nohup · setsid 둘 다 지움 · N2 꼴 | job_completes | 그것 하나만 실패 (nohup_rc.txt 없음 · 감싼 bash 사라짐) · 옳은 까닭 |
| M5 | 발사 줄에서 nohup 만 지움 (setsid 둠) · N2 꼴 | sighup_record | 그것 하나만 실패 (끝까지 돌지만 sighup_ignored=no) · 옳은 까닭 |

관찰 (판정 없음): O1 = 발사 줄에서 setsid 만 지움 (nohup 둠) · N2 꼴 → nohup_rc.txt rc=2 · nohup.log `error: reset died of signal 1` · `[siteq] STOP: git worktree add failed` (§9-5 setsid 까닭).  결과는 SIGHUP 이 올 때 작업이 무엇을 하고 있었는지에 달려 판정으로 쓰지 않는다 (이 컨테이너에서는 다섯 번 모두 같은 꼴).

### 9-8. 이 블록 · 이 시험이 못 보는 것 (한정)

| 한정 | 뜻 |
|---|---|
| 모드 목록 = 준 경로 그 자체 | 하위 폴더 · 파일 (원장 저장소 안 · 시도 폴더 · 앞으로 사슬이 만들 파일) 은 보지 않는다 — 새 파일의 모드는 C18 (umask) · siteq_out (새 폴더) 로만 짐작 · 단일 작성자 정책 (계획 A5) 의 증거는 목록 + 운영 규칙이다 |
| 등급만 | gabia (root) 에서는 root 소유가 owner=self 로 적힌다 (머리 줄 runner=root 로 가린다) · 이름 · UID 숫자는 일부러 없다 |
| group_others | 그룹 항목 + /etc/passwd 만 센다 — LDAP · SSSD 에만 있는 계정은 빠질 수 있다 · ACL 로 들어온 사용자는 acl_extra 로만 보인다 |
| ACL | 확장 속성 system.posix_acl_* 만 읽는다 — NFSv4 ACL 은 보지 않는다 (0 또는 unsupported) |
| 시각 | 목록 · umask 는 도구를 띄우기 전 한 순간 |
| 모드 목록이 실패하는 길 | 목록 파이썬이 죽으면 화면에 한 줄 (mode listing failed) 을 찍고 도구는 그대로 돈다 (`||`) — 이 길은 시험하지 않았다 (없는 경로 · 빈 칸은 시험함) |
| rc 파일 없음 | 결과 폴더 전 STOP 과 블록 죽음을 가르지 못한다 (§9-3) · nohup 꼴은 nohup_rc.txt 가 앞의 것을 덮는다 · 감싼 bash 까지 죽으면 nohup_rc.txt 도 없다 (pid 파일의 프로세스가 살아 있는지로 본다) |
| nohup 꼴의 git fetch | 터미널 없이 돈다 — 기준 체크아웃이 비밀번호 · 열쇠 문구를 물으면 STOP (git fetch failed) · 11-09 두 현장의 fetch 가 묻지 않았는지는 기록에 없다 [미확인] → 물으면 짧은 꼴을 쓰거나 fetch 를 먼저 손으로 |
| nohup 꼴의 발사 폴더 | 본문이 결과 폴더 전에 STOP 해도 발사 폴더 (block.sh · nohup.log · pid · rc) 는 남는다 — 본문 STOP 문구의 "nothing written" 은 작업 트리 · 결과 폴더를 뜻한다 |
| nohup 꼴의 문맥 | SIGHUP 무시 + 자기 세션 (setsid) — 생산 발사 줄 (nohup · 셸의 작업으로 남음) 과 같지 않다 · 생산 줄의 꼴 = 문서에 없음 (계획 §8) |
| 꼴 B 를 켜면 | C18 이 셸의 umask 를 보이지 않는다 (umask_start 로만) |
| 컨테이너 | root 로만 돌았다 — 비 root 실행 (kgy) 의 등급 계산은 "다른 UID 소유 파일" 쪽만 시험됨 · 11-09 의 A11 꼴 (능력 뺀 uid 0) 은 다시 돌리지 않았다 · kgy · gabia 의 커널 · 셸 · 터미널 · ssh 가 아니다 · pty 주 쪽 닫기 = ssh 끊김의 흉내 · 11-09 §4-4 · §5 의 한정 그대로 |
| 도구 결과 | 이 시험은 블록 틀의 동작을 본다 — 현장 자격 (C01 – C29) 의 판정은 현장 실행 몫 (계획 §5) |

### 9-9. 파일 (11-11 판)

| 파일 | 상태 |
|---|---|
| `docs/reviews/rint2_siteq_prep_20261109/container_test/short_block.tmpl` | 고침 (23 → 96 줄 · ASCII · `!` · TAB 없음) |
| `docs/reviews/rint2_siteq_prep_20261109/container_test/short_block_nohup.tmpl` | 새 파일 (105 줄 · 같은 조건) |
| `docs/reviews/rint2_siteq_prep_20261109/container_test/run_block_tests.py` | 새 파일 (컨테이너 시험 · PID 1 이 아니면 거부) |
| `docs/reviews/rint2_siteq_prep_20261109/container_test/summary_short_20261111.txt` | 새 파일 (§9-7 의 원문 요약) |
| `docs/reviews/rint2_siteq_prep_20261109/container_test/summary.txt` · `docs/reviews/rint2_siteq_prep_20261109/container_test/summary_short.txt` · `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` · `docs/reviews/rint2_siteq_prep_20261109/tools/test_siteq_c02b.py` | 그대로 |
| `docs/reviews/rint2_siteq_prep_20261109/SHA256SUMS` | 지금 바이트로 다시 씀 (줄 6 → 9) |
| 11-09 판 틀 | 리포 이력에 그대로 (`db86ce9b9` · sha256 bc117ba6…) — 시험의 R1 · R2 가 git show 로 꺼내 쓴다 |

### 9-10. 지시 밖으로 더한 것 · 1저자가 정할 것 (11-11)

지시 (계획 §10 의 2 번 · 본 세션 지시서) 밖으로 더한 것 — 빼도 되며 까닭은 아래:

| 더한 것 | 까닭 |
|---|---|
| nohup 꼴의 setsid | 관찰 O1: nohup 만이면 작업 그룹에 온 SIGHUP 에 git 의 자식이 죽어 (다) 를 지키지 못한다 |
| 이름 끝 `${SITEQ_TAG:-}` | 두 꼴을 같은 날 같은 홈에서 돌리게 (없으면 둘째가 already exists 로 STOP → 작업 트리 지우기 · 폴더 이름 바꾸기를 손으로) · 짧은 꼴은 빈 값이라 이름 그대로 |
| 모드 목록의 group 등급 · group_others · acl_default · link | 계획 §2-3 A2 "그룹 쓰기를 남기려면 그룹 구성 근거" · §8 "그룹의 다른 구성원 [미확인]" · 기본 ACL 은 umask 를 덮는다 |
| 환경 기록의 sighup_ignored | 결과만 보고 어느 꼴 (문맥) 로 돌았는지 안다 · M5 가 이것으로 잡힌다 |
| 사례 S1c · N4 · M4 · M5 · 관찰 O1 | 꼴 B 동작 · 같은 날 두 꼴 · 끊김 시험이 실제로 무는지 · setsid 의 근거 |

| # | 1저자가 정할 것 | 권고 |
|---|---|---|
| Q1 | umask 꼴 A (기록만 · 틀 지금) / 꼴 B (블록이 022) | 꼴 A (§9-6) |
| Q2 | nohup 꼴을 nohup setsid 로 둘까 (지시 = nohup) | 둔다 — O1 · 작업은 그대로 SIGHUP 무시 문맥 (sighup_ignored=yes) |
| Q3 | 생산 발사 줄에도 setsid · 출력 명시 돌림 · 작업 트리 밖에서 띄우기를 넣을까 | 계획 §10 의 4 번 (명령 블록 · 실행 정책) 에서 함께 정한다 — 넣는 쪽 (O1 · C5 확인) |
| Q4 | 현장에서 두 꼴의 순서 | 짧은 꼴 먼저 → 같은 날 nohup 꼴 (이름이 겹치지 않는다 · N4) |
| Q5 | group_others (그 그룹의 다른 계정 수 · 이름 없음) 를 둘까 — 11-10 에 "묻지 않음" 이던 칸 | 둔다 (계획 A2 근거 · 숫자만) · 원치 않으면 그 칸만 뺀다 |
| Q6 | gabia 의 PLAN · LEDGER · OUTBASE · PLANFILE 자리 · kgy 의 12 단위 OUTBASE 이름 | 계획 §10 의 4 번에서 정한 뒤 채운다 · gabia = kgy 와 같은 홈 아래 꼴 (계획 §7 Q2) |
