# 사전 공격 6 회차 — 마무리 (최종 · 11-02) · Rint ② PC5 수정 (`b9fd47d7b` · `6bb3c064f` · `43a8abcaa` · `87a00ef46`)

- 대상 = 가지 `claude/stoic-knuth-NObVQ` 의 `d6e8d1b44` (11-02 · 이 작업 트리) · 사슬 · 시험 바이트 = 중간 보고 대상 `4c69070ad` 와 같음 (`git diff 4c69070ad HEAD -- scripts/rint_r_chain.py scripts/test_rint_r_chain.py scripts/test_rint_r_chain_e2e.py` = 0 줄 · sha256 `d444a671…` · `6285b0b6…` · `4db09fa3…`) · 등록 R · Q9 · kgy 명령 문서 · 설명 페이지도 같음.
- 중간 보고 = `PREATTACK_C2.md` (10-30 · 고치지 않음 · 이 파일이 대신한다).  이 회차 새 탐침 · 변이 틀 = `final/probes/` · 출력 = `final/logs/`.
- 방법 = 독립 작업 트리 · 고친 사람 설명 (증거 README · 커밋 메시지) 은 주장으로만 읽음 · 반례마다 실제 사슬 함수 · 실경로 (사슬 `main` · 가짜 러너 bash + 파이썬 · 실제 프로세스 그룹 · 실제 /proc · 실제 git 원장) · 사슬 · 시험 파일은 고치지 않았다 (변이 = 스크래치 사본 트리).
- 환경 = 이 컨테이너 · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · root · 4 코어 · 커널 6.18.44 · `fs.suid_dumpable` 0 · BLAS 스레드 1 · nice 10 · 메인 세션 시험이 같은 때 돌았다 (부하 3–4).  uid 실측만 root 로 시작해 자식을 uid 65534 (nobody) 로 내렸다 (설치 · 시스템 설정 없음).  `scripts/check_all.sh` · kgy 3.8 판은 돌리지 않았다 (메인 게이트 몫).
- 결론 한 줄 — **P1 둘 (PC6-01 조건부 · PC6-12 후보) · P2 둘 (PC6-02 · PC6-09) · P3 여섯 (PC6-03 · 04 · 05 · 06 · 08 · 10) + 변이 공백 묶음 PC6-11 · 철회 하나 (PC6-07)**.  PC5 새 가드 변이 32 = 다시 32/32 잡힘 · 옳은 이유 32 (§3-1).  이 회차가 더한 PC5 가드 변이 20 중 잡힘 5 · 생존 15 — 결정 동등 3 · 뒤 판정이 막음 (재실행은 돎) 2 · 시험 공백 10 (§3-2) · 생존 15 를 한 사본에 합쳐도 상주 사슬 시험 407 · 끝-끝 40 이 다 통과 (사본 환경 Y13 하나 뺌 · §3-3) · 대조 변이 (C2b 가드) = 잡힘.

## 0. 판정 요약

| 구분 | 항목 | 근거 (이 회차) |
|---|---|---|
| **새로 깨짐 (P1 후보)** | PC5-01 다시 셈의 범위 — 결과 줄 대신 **항목 줄의 대상** 을 바꾼 끝 커밋 교체 (원장만 · 시도 폴더 그대로) = 판정 원장 대조 통과 · 결과 본 시도 (runner_rc · 재실행 불가) 대신 새 시도 채택 | **PC6-12** (R10 · 두 꼴 다 통과) — PC5 diff 밖 (옛 고리) 이지만 PC5-01 이 닫았다고 적은 부류 |
| 확인 · 넓힘 (P1 조건부) | PC5-07 — 같은 실 uid 의 environ · stat 못 읽는 무관 프로세스 하나 = 끝난 런 GROUP_UNCONFIRMED · recover 도 막힘 | **PC6-01** — 중간 탐침 다시 = 같은 값 + 새 R8a (0.7 s 구경꾼으로 충분 · 대기 상한 30 s 안 씀) · R8b (운영자 자기 세션 아래 recover = rc 3 · 고아 러너 안 죽임) · R8c (다른 사용자 stat 못 읽음 = 미확인) |
| 확인 · 넓힘 (P2) | PC5-02 · 06 같은 낱말 규칙 — "그 밖 CUDA 오류 = 자동 재실행 없음" 이 러너 rc 길에서만 | **PC6-02** — 42 중 36 (다시 같음) + 새 U4: GROUP_UNCONFIRMED 가 러너 rc 1 (파이썬 KeyError 포함) 을 가려 재실행 자격 |
| 새로 깨짐 (P2) | Codex ② "결과 줄 = 그룹 종료 확인 뒤" — 사슬 부모 사망 뒤 **같은 --attempt 명령을 다시 치면** 결과 뒤 시도에 rejected · 결과 전 결과 줄 · 새 시도 열림 | **PC6-09** (R6) |
| 반례를 못 찾음 (닫을 후보 · 범위 한정) | PC5-03 (산 사슬) · PC5-04 (다른 부팅 · 운영자 표지 범위) · PC5-05 (결과 전 재실행 = 원 시도와 같은 뜻 · R5) · PC5-10 · X09 · X18 · 원 반례 PC5-01 (끝 줄 reset · amend · merge -s ours · resume_ok 만 · git replace = R7) | 상주 시험 · 변이 (§3) · R5 · R7 · R11 |
| 변이 (§3) | 10-28 의 32 = 다시 32/32 (옳은 이유) · 이 회차 새 PC5 가드 20 = 잡힘 5 · 생존 15 (결정 동등 3 · 뒤 판정이 막음 2 · 시험 공백 10 — M2e 는 끄면 판정 원장 대조까지 통과) · 생존 15 를 합쳐도 상주 사슬 시험 407 · 끝-끝 40 통과 · 대조 변이 잡힘 | PC6-11 · `final/logs/mutation_summary.json` · `probe6f_mut_paths.out` |
| 닫지 않음 (P3) | PC5-08 (신호 = SIGINT 만) · PC5-06 일부 (SIGINT · 로그 없음 · 사슬 자신의 자원 결함) · X18 옆 파일 길 · 운영자 사유 꼴 | PC6-03 · 04 · 05 · 06 · 08 · 10 |
| 철회 | 중간 PC6-07 (복사한 재실행 = 늘 결과 뒤) | R5 — 같은 자리 원 시도와 같은 답 (§4) |
| 그대로 한정 | PC5-09 (wontfix) | 이 회차 안 건드림 |
| 미확인 | kgy 3.8 판 11 묶음 (게이트 몫 · 증거 로그 글만 대조) · kgy 실제 사용자 · ssh 세션 자격 · /proc 마운트 옵션 (PC6-01 조건) · 실제 GPU 결함 뒤 프로세스 D 상태 (PC6-02 조건) · 생존 변이 분류의 일부 = 코드 읽기 (M2a · M2b · M4 · M5 · M6 · M7 · M8 · M10a · M10b · M11 · M12 · M15 · 실경로로 잰 것 = M2e · M2c · M9) | §1 · §2 · §3-2 |

## 1. 숫자 · 전칭 대조

| 주장 | 자리 | 잰 것 (이 회차 · 명령 = §7) | 판정 |
|---|---|---|---|
| 사슬 시험 407/407 | `87a00ef46` · 계획 진행 · 증거 SOURCE | 중간 보고 실측 407/407 (454.0 s · `4c69070ad`) · 지금 HEAD 와 사슬 · 시험 바이트 같음 → 다시 돌리지 않음 | ✓ |
| 끝-끝 40 PASS · 0 FAIL | 같은 곳 | 중간 보고 실측 40 · 0 (529.3 s) · 바이트 같음 | ✓ |
| first_result 9/9 | 같은 곳 | `test_rint_first_result: 9/9 PASS` | ✓ |
| s0_census 167 | 같은 곳 | `167 PASS · 0 FAIL` (22 s) | ✓ |
| ext_runner 151 | 같은 곳 | `151 PASS · 0 FAIL` (131 s) | ✓ |
| 웹앱 91/91 | `43a8abcaa` | `test_rint_explainer_page: 91/91 PASS` | ✓ |
| kgy 판 11 묶음 통과 | `87a00ef46` | **미실행** (게이트 몫) · 증거 `logs/kgy_check.out` 글 = 11 ✓ (chain 407/407 · e2e 40 · runner 151 · census 167 …) — 로그 글과 주장 같음 | 미확인 (로그 글만) |
| 고치기 전 판 7/26 (`--only PC,GR08,AL12,RS06,K01`) | `b9fd47d7b` 메시지 | `b9fd47d7b` 사본 (scripts + 문서 셋 · docs/data 링크) = **7/26** · 실패 19 · PC12 · PC13 통과 (변이 구멍 시험 = 가드가 있어 통과) | ✓ |
| B 커밋 판 82/84 (K01 · PC20) | `6bb3c064f` 메시지 · SOURCE | `6bb3c064f` 사본 = **82/84** · 실패 = K01 · PC20 (문서 커밋 몫) | ✓ |
| 봉인 파일 무변경 (CODE_FILES 32 · S0_SAME_FILES 7) | `6bb3c064f` · 계획 | CODE_FILES 32 · S0_SAME_FILES 7 · 네 커밋 바뀐 파일 134 ∩ = **0** (바뀐 코드 = 사슬 · 시험 둘 · 웹앱 둘) | ✓ |
| 새 가드 변이 32/32 잡힘 | `87a00ef46` · 계획 | 다시 **32/32** · 잡은 시험 · 사유 = §3-1 (옳은 이유 32 · 둘은 사유 줄 600 자 잘림 → 코드 읽기) | 숫자 ✓ · ⚠ "새 가드" 전칭 ✗ — 고른 32 에 한정 (이 회차 PC5 가드 20 개 더 · 생존 15 · §3-2) |
| "변이 32 = 새 가드 30 + X09 · X18" | `6bb3c064f` 메시지 | PC5 diff 의 가드는 30 보다 많다 (§3-2 의 M1–M15) | ✗ (범위) |
| `group_members` "다른 터미널의 sudo 같은 프로세스로 확인이 늘 막히지 않게" | `scripts/rint_r_chain.py:2405–2408` | setuid · ssh 세션 · agent = 같은 실 uid → 막힌다 (PC6-01) | ✗ |
| `run_in_group` "끝 기록 = 표지 프로세스가 0 임을 확인한 뒤 (대기 상한 안에 못 하면 confirmed False)" | `:2548` 설명문 | 못 읽는 후보 하나면 대기 상한을 쓰지 않고 곧바로 False (R8a · 2.08 s) | 문구 ✗ |
| 등록 R §10-5 아 ① "끝 커밋 교체 (reset · --amend 뒤 원인 · 재실행 자격만 바꾼 줄) = ATTEMPT_LEDGER_MISMATCH" · "입력 대상의 모든 시도 … 다시 셈" | 등록 R :613 | 원인 · 자격만 바꾼 줄 = 잡힘 (PC01 · R11) · **항목 대상을 바꾼 끝 커밋 교체 = 통과** (R10) — "입력 대상의 시도" 를 원장이 정한다 | ✗ (PC6-12) |
| 아 ② "그 밖 CUDA 오류 = runner_rc (자동 재실행 없음)" · "같은 낱말 규칙 = 요약 있는 길 · 없는 길 모두" | 등록 R :614 | 낱말 규칙은 같지만 기본값이 길마다 다름 → 42 중 36 자격 · GROUP_UNCONFIRMED 가 rc 1 을 가림 (U4) | ✗ (PC6-02) |
| 아 ④ "사유 = 빈 글 아님 · 줄바꿈 없음 · 300 자 안 · 아니면 rc 2" | 등록 R :616 | \n · \r 만 · U+2028 · U+0085 · \v · \f · \x1c · ESC 통과 (U5) | 부분 ✗ (PC6-10) |
| 아 ⑥ "기록 · 런 로그를 못 읽음 = resume_ok false (보수)" | 등록 R :618 | 요약 없는 길만 (그 문장의 범위) · 요약 있는 길 = 로그 없음 → 자격 | 범위 (PC6-05) |
| 아 ⑧ "`git add` · `commit` 실패 (index.lock · 신호) = 되돌린다" | 등록 R :620 | index.lock · SIGINT ✓ · SIGTERM · SIGHUP · SIGKILL ✗ (R4 다시 같음) | 부분 ✗ (PC6-04) |
| 아 ③ "산 사슬은 recover 하지 않는다" | 등록 R :615 | ✓ (PC05 · 변이 P03a–c · M3 잡힘) | ✓ |
| 아 ⑤ / Q9 개정 7 "결과 전 멈춘 재실행 = 건너뜀" | 등록 R :617 | ✓ — 복사 뒤 재실행은 원 시도와 같은 자리 같은 답 (R5) | ✓ |
| 자원 낱말 = 메모리 · 디스크 다섯 | 계획 Q2 · `RESOURCE_WORDS` | 표 = 다섯 그대로 (`probe6_unit.out` env 줄) | ✓ (표) · 재실행 자격은 다섯 낱말만이 아님 (PC6-02) |

## 2. 지적 (PC6-NN · 이 회차 척도: P1 = R 캠페인이 기대는 보장을 깸 · P2 = 반례가 관문을 지나거나 주장이 거짓 · P3 = 문구 · 견고성 · 시험 공백)

경로 약칭: `P6/` = `docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/` · 사슬 = `scripts/rint_r_chain.py` · `<tmp>` = 아무 빈 임시 폴더 · 명령은 작업 트리 꼭대기에서 (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`).

| id | 등급 | 위치 (사슬 줄) | 재현 명령 → 실측 (이 회차) | 왜 문제 | 최소 고침 |
|---|---|---|---|---|---|
| **PC6-12** | **P1 (후보)** · 새 · PC5 diff 밖 (옛 고리) | `ledger_verdict_check` `:3795–3807` (`:3801–3803`) — 찾은 시도 폴더의 번호가 원장 항목이면 `continue` (attempt.json 의 대상 · 시작 커밋 조상 · 다시 셈 = 입력 대상의 항목에만 `target_ledger_problem` `:3710`) | `python3 -I P6/final/probes/probe6f_real.py <tmp> R10` → 정직한 원장 (항목 1 ladder:P0 · 결과 줄 stopped · post · runner_rc · resume_ok false = 채택) 에서 같은 대상 `--add` = rc 3 ATTEMPT_AFTER_ADOPTED (대조) · clone 에서 `git reset --hard HEAD~2` + 항목 1 의 **대상만** `ladder:P0:FIBRE` 로 바꾼 줄 (+ 결과 줄 그대로 · 또는 없음) → 역사 검사 None · `--add ladder:P0` rc 0 (n 2) · 시도 2 CALIBRATED · 판정 원장 대조 **통과** (targets `ladder:P0` = attempts [2] · chain [2] · 멈춤 = INPUT_MISSING (사다리 하나만 넣음 · 원장 멈춤 아님)) · 시도 1 폴더 (attempt.json 대상 ladder:P0 · 시작 커밋 = 조상 아님) 는 같은 바탕에 그대로 · 두 꼴 다 같음 | PC5-01 의 다시 셈 · 등록 R 아 ① "끝 커밋 교체 = ATTEMPT_LEDGER_MISMATCH" 를 **결과 줄이 아니라 항목 줄의 대상** 을 바꿔 비켜 간다 — 원장만 고침 (시도 폴더 · 결과 줄 증거 그대로) · 결과를 본 시도 (재실행 불가) 를 지우고 새 시도를 채택 = 원장이 막으려던 "결과를 본 뒤 고르는 길" 그 자체 · Q-D 한정 ("모든 사본을 함께 고친 손") 보다 좁은 손 (원장 두 커밋) · 5 회차 PC-01 (같은 부류 · 원장만 · 판정 통과) 은 P2 로 매겼다 — 이번엔 그 고침의 주장 범위를 비켜 가므로 P1 후보 (메인 판단) · 합치기 (`MergeFetch`) · 합친 예측 (`merged_ledger_check` `:3847`) · 예측 입력 (`ledger_inputs_check`) 도 대상을 원장에서 읽는다 (같은 꼴 = 추정 · 실행 안 함) | 판정 · 합치기 · 합친 예측 · 예측 입력 대조에서 **찾은 시도 폴더 전부** 의 attempt.json (n · 대상 · 기계 · resume_of) = 원장 항목 · 시작 커밋 = 원장 조상 · 바이트 접두 (지금 입력 대상에만 하는 대조) · 폴더의 대상이 입력 대상이면 원장이 다른 대상이라 해도 그 대상의 시도로 센다 → 어긋남 = ATTEMPT_LEDGER_MISMATCH · 상주 시험 = R10 두 꼴 (고치기 전 판에서 통과하는지 먼저) |
| **PC6-01** | **P1 (조건부)** · 확인 · 넓힘 | `group_members` `:2444–2452` (environ 못 읽음 = 셈 밖 셋 (pid 1 · 다른 실 uid · 그룹 시작 전) 말고 확인 불가 · `:2451–2452` stat · status 못 읽음 = 곧바로 확인 불가) · `group_settle` `:2495–2496` (None 이면 곧바로 (False, None) — 대기 상한 안 씀 · 보이는 그룹 원도 안 죽임) · `Runner._execute` `:3999` · `recover_group` `:6270` · `:6286` (운영자 표지 = 다른 부팅 · 이름공간 가지에서만) | (root) `python3 -I P6/probes/probe6_uid.py` → 중간 값과 같음 (세 꼴 구경꾼 = 실 uid 65534 · environ PermissionError · group_members None · run_in_group rc 0 · confirmed False · recover rc 3 → 구경꾼 죽인 뒤 rc 0) · (root) `python3 -I P6/final/probes/probe6f_uid.py` → **R8a** 러너 (sleep 2) 끝 무렵 1.8 s 에 생겨 0.7 s 만 사는 구경꾼 = confirmed False · run_in_group 2.08 s 에 반환 (GROUP_GONE_WAIT_S 30 s 안 씀) · 대조 (끝 전 사라짐) = True · **R8b** 사슬 SIGKILL 뒤 (러너 고아 `sleep 30` 삶 · 끝 기록 없음) 그 뒤 생긴 "세션" 구경꾼 S 아래 자식 O (exec · dumpable) 의 recover = rc 3 · S 밖 recover (S 삶) = rc 3 · 그동안 고아 러너 **안 죽음** (killed 0) · S 끝낸 뒤 recover = rc 0 · killed 1 · **R8c** 가짜 /proc — 다른 사용자 (root) 프로세스 stat · status 못 읽음 = None (대조 읽힘 = []) | (1) 같은 실 uid · non-dumpable 무관 프로세스 = ssh 로그인 세션 (`sshd: user@pts/N` · scp/rsync `@notty`) · setuid 프로그램 (sudo …) · agent (ssh-agent · gpg-agent) — kgy 사슬이 사용자 계정으로 돌면 (kgy 명령 문서 = `~/` 경로) 1저자가 그 런 도중 ssh 로 들어와 그 런 끝까지 접속해 있는 것만으로 끝난 런 = GROUP_UNCONFIRMED → 결과 줄 없음 (ATTEMPT_OPEN) (2) recover 도 막힌다 — 런 시작 뒤에 연 ssh 세션에서 친 recover 는 **자기 세션 프로세스** 때문에 늘 rc 3 (R8b) · 같은 호스트엔 운영자 표지도 없음 → root 로 돌리거나 접속을 다 끊고 비대화형으로만 (3) 못 읽는 후보 하나 (0.7 s 짜리 sudo · scp 도) 면 곧바로 미확인 (4) recover 가 끝 기록을 by recover · rc None 으로 다시 써 재실행 (`ResumeRunner._src_done` `:4055` = 끝 기록 rc 0 만 복사) 은 끝난 런을 다시 돈다 → GPU 런 = 등록 R §10-5 라 (멈춘 GPU 런 재실행 안 함) → 그 대상 STOPPED → 주 판정 없음 (5) /proc `hidepid=1` 이면 다른 사용자 프로세스 stat 이 EACCES → 사용자 사슬은 **모든 런** 미확인 (R8c 꼴 · hidepid 동작 = 기억 · 이 컨테이너에서 /proc 재마운트 안 함 = 추정) (6) 봉인 원천 런 (`RunnerGraphSource._run` `:4201`) 도 같은 미확인 → SV_UNCHECKED (코드 읽기) · 거짓 수용 없음 = 활성 결함 · 조건 (미확인) = kgy 사슬 실행 사용자 · ssh 세션 프로세스 자격 (OpenSSH 동작 = 기억 · kgy 실측 아님) · kgy /proc 마운트 옵션 | ① 못 읽는 후보가 있어도 대기 상한 안에서 다시 본다 (곧바로 미확인 아님) ② 그동안 보이는 그룹 원은 먼저 죽인다 ③ 사유에 pid · 이름 · 실 uid ④ 후보를 계보로 좁힌다 (사슬 `prctl(PR_SET_CHILD_SUBREAPER)` + 러너 pid 의 자손 = ppid 사슬 · 무관한 로그인 세션 · agent 는 후보 아님) · stat 못 읽는 프로세스도 같은 계보 기준 ⑤ 상주 시험 = R8a · R8b · R8c 꼴 (root 일 때만 · 아니면 건너뜀 표지) · `group_members` 설명문 문장 고침 |
| **PC6-02** | **P2** · 확인 · 넓힘 | `stop_cause` `:3493–3517` (`:3513` GROUP_UNCONFIRMED → 기본 group_unconfirmed · `:3517` 잘못된 주소 둘만 덮음) · `orphan_cause` `:3556` · `:3562` · `Runner._execute` `:3999` (확인 실패를 rc `:4009` 보다 먼저 · 런 rc 를 원인에 안 씀) | `python3 -I P6/probes/probe6_unit.py <tmp> U1` → 42 중 36 resume_ok True (다시 같음 · False = "RUNNER_RC rc 1 · 그룹 원인 없음" 여섯뿐) · `python3 -I P6/probes/probe6_real.py <tmp> R1,R1c,R2` → R1 LAUNCH_FAILED 뒤 사슬 부모 SIGKILL → recover = interrupted · post · parent_dead · true → `--add --resume 1` rc 0 → 재실행 CALIBRATED → 채택 [1, 2] · R1c (사슬 산 채 rc 1) = runner_rc · rc 3 · R2 (SIGTERM) = signal · true → rc 0 · **새** `python3 -I P6/final/probes/probe6f_unit.py <tmp> U4` → 멈춤 GROUP_UNCONFIRMED + 런 기록 rc 1 + 로그 = LAUNCH_FAILED · device-side assert · **파이썬 KeyError traceback** = 원인 group_unconfirmed · resume_ok **True** (rc 0 · 1 같음) · 대조 잘못된 주소 = runner_rc · false | 1저자 Q2 · 등록 R 아 ② "그 밖 CUDA 오류 = runner_rc (자동 재실행 없음) · 같은 낱말 규칙 = 두 길 모두" — 낱말 규칙은 두 길에 같지만 **기본값이 길마다** 다르다 (rc 길 = runner_rc · 시간 초과 · 신호 · 그룹 미확인 · 부모 사망 길 = 자격 원인) → 잘못된 주소 둘 밖의 코드 결함 꼴은 rc 길에서만 막힌다 · 특히 GROUP_UNCONFIRMED 가 **러너 rc ≠ 0 을 가린다** (러너가 파이썬 결함으로 죽었어도 그룹 확인이 실패하면 재실행 자격) — 그룹 확인 실패 = PC6-01 구경꾼 · GPU 결함 뒤 드라이버 안에서 30 s 넘게 D 상태로 남은 프로세스 (추정 · 실측 아님) · 러너는 한 팔 실패 = exit 1 (`scripts/sdcp_gain_vox015_8arm.sh:978–981`) 이라 시간 초과 · 신호 길은 "오류 줄 뒤 걸림" 일 때 (추정) | ① 그룹 확인 실패 · 시간 초과 · 신호여도 런 rc ≠ 0 (원인 None) 이 기록에 있으면 그 런 = 낱말 규칙 + 기본 runner_rc ② 모든 길에서 "자원 낱말 없음 + CUDA 오류 표지 (`CUDA_ERROR_\w+` · `cudaError\w+` · `CUDA(Runtime|Driver)Error`) 또는 파이썬 traceback" = runner_rc ③ U1 (42) · U4 를 상주 시험으로 · R1 · R2 꼴 실경로 시험 |
| **PC6-09** | **P2** · 새 | `attempt_open` `:3275–3282` (시도 폴더가 이미 있으면 누구 폴더든 옆 거부 기록 + 결과 줄) · `attempt_reject` `:3230–3248` (그룹 확인 없음) | `python3 -I P6/final/probes/probe6f_real.py <tmp> R6` → 시도 1 (바닥 런 표지 뒤 · 러너 25 s 잠) 사슬 부모 SIGKILL → (recover 대신) **같은 `--attempt 1` 명령** 다시 → rc 3 `ATTEMPT_REJECTED n=1 code=OUTDIR_NOT_EMPTY` · 결과 줄 {rejected · pre · presolve · folder attempt_1.rejected.json · by chain} 커밋 — 그때 시도 1 폴더 = 결과 뒤 (`folder_side` post) · 그 그룹 끝 기록 없음 · 고아 러너 **삶** → 같은 대상 `--add` rc 0 (n 2) → 시도 2 CALIBRATED (고아 아직 삶) → 채택 [2] → 판정 = ATTEMPT_LEDGER_MISMATCH "원장에 없는 시도 폴더 ['attempt_1'] (항목 1 의 결과 줄 폴더 = attempt_1.rejected.json)" → 그 폴더를 옮긴 뒤 판정 = 원장 대조 **통과** (INPUT_MISSING) · 옮긴 폴더 recover = 고아 1 죽임 | (1) 사슬 스스로 결과 뒤 시도에 "rejected · 결과 전" (= 풀기 전 거부 · 러너 0 회의 뜻) 결과 줄을 쓴다 (2) Codex ② "결과 줄 = 그룹 종료를 확인한 뒤 · 확인 못 하면 다음 시도 채택을 막는다" 를 비켜 간다 (그룹 산 채 결과 줄 · 다음 시도 열림 · 고아 GPU 런과 새 시도 동시) (3) `--add` · 풀기 전 대조가 "채택 뒤 새 시도" 를 못 막고 판정의 "원장에 없는 시도 폴더" 하나만 남는다 — 그 화면을 보고 폴더를 치우면 결과 본 시도가 사라지고 새 시도 채택 · 운영자 실수 한 번 (recover 대신 같은 명령) 이 시작 | 시도 폴더가 이미 있고 그 안 attempt.json = 이 항목 (n · 대상 · 시작 커밋 = 원장 조상) 이면 **화면만 거부** (원장 · 폴더 무변경 · "--stage recover 먼저" 안내) · 옆 거부 기록은 남의 폴더 (attempt.json 없음 · 다른 번호) 일 때만 · 상주 시험 = R6 꼴 |
| PC6-03 | P3 · 확인 | `_signal_handlers` `:2519–2531` (SIGTERM · SIGHUP 만) · `run_in_group` `:2594` (KeyboardInterrupt = 원인 exception) · 단계 `:4927` (`except Exception` = KeyboardInterrupt 못 잡음 → 요약 없음) | `python3 -I P6/probes/probe6_real.py <tmp> R3` → SIGINT = 사슬 rc −2 · 결과 줄 없음 → recover = interrupted · post · chain_exception · false → `--add --resume` rc 3 / SIGTERM = stopped · post · signal · true → rc 0 / SIGKILL = recover parent_dead · true → rc 0 (다시 같음) | 운영자 중단 신호 셋이 다른 답 · Ctrl-C 가 그 대상을 잃게 한다 (사슬 예외 = 코드 결함 뜻) · 런 사이 (팔 읽기 중) Ctrl-C = 끝 기록 다 rc 0 → parent_dead (자격) (코드 읽기) = 때에 따라 다른 답 · 실제 R 은 `setsid nohup` 꼴이 많아 빈도 낮음 | SIGINT 도 ChainSignal (처리기에 넣기) 또는 run_in_group 이 KeyboardInterrupt = 'signal' · 시험 = R3 꼴 |
| PC6-04 | P3 · 확인 | `ledger_append` `:2966–2999` (되돌림 = 파이썬 예외 때만 `:2986`) · 사슬은 런 기다림 밖에서 기본 신호 처리 (결과 줄 덧붙임 `attempt_close` 도) | `python3 -I P6/probes/probe6_real.py <tmp> R4` → `git commit` 직전 SIGTERM · SIGHUP · SIGKILL = 자식 rc −15 · −1 · −9 · `git status` = `M  rint_r_attempts.jsonl` · `ledger_now` ATTEMPT_LEDGER_MISMATCH · 다음 `--add` rc 3 / SIGINT = 되돌림 · 다음 `--add` rc 0 (n 1) (다시 같음) | 등록 R 아 ⑧ "(index.lock · 신호) = 되돌린다" = SIGINT 만 참 · 원장 전체가 손 git 전까지 멈춤 (보수 · 거짓 수용 없음) | 덧붙임 구간 `signal.pthread_sigmask` 로 SIGTERM · SIGHUP · SIGINT 막기 + 다음 배타 잠금 읽기가 "작업 파일 = HEAD + 정준 한 줄 · 색인만 다름" 을 HEAD 로 되돌리고 기록 (SIGKILL 꼴) · 등록 R ⑧ 문장 고침 |
| PC6-05 | P3 · 확인 | `run_log_text` `:3484–3491` (없음 · 못 읽음 = '') · `result_fields` `:3573–3592` (`readable` = 요약 없는 길만) | `python3 -I P6/probes/probe6_unit.py <tmp> U2` → 요약 있는 길 · 로그 없음 · TIME_LIMIT = timeout · post · true · RUNNER_RC + signal = signal · post · true / 요약 없는 길 · by recover · 로그 없음 = parent_dead · post · false (다시 같음) | 두 길 비대칭 (요약 있는 길 = 로그 없음 → 낱말 없음 → 자격) · 아 ⑥ 의 "못 읽음 = false" 는 요약 없는 길 문장 · 사슬이 로그를 스스로 만들므로 빈도 낮음 (지움 · 디스크 결함) | 돈 런 (런 기록에 rc · seconds) 의 로그가 없거나 못 읽으면 요약 있는 길도 resume_ok false |
| PC6-06 | P3 · 확인 · 뉘앙스 | `chain_exception_record` `:4810–4820` · `stop_cause` `:3507` (CHAIN_EXCEPTION 먼저) · 요약 쓰기 `:4934` (try 밖) | `python3 -I P6/probes/probe6_unit.py <tmp> U3` → 사슬 자신의 MemoryError · OSError ENOSPC = 멈춤 CHAIN_EXCEPTION · 원인 chain_exception · resume_ok false (다시 같음) | Q2 의 뜻 (메모리 · 디스크 = 자원 = 재실행 자격) ↔ 사슬 자신의 같은 원인 = 재실행 불가 · 같은 ENOSPC 가 요약 쓰기 (`:4934` try 밖) 에서 나면 요약 · 결과 줄 없음 → recover = 끝난 런뿐 → parent_dead · 자격 (코드 읽기 · 미실행) = 자리마다 다른 답 | `chain_exception_record` 에서 MemoryError · OSError (ENOSPC · EDQUOT) = 원인 resource (또는 `words_cause(str(e))`) |
| PC6-08 | P3 · 확인 (PC5 diff 밖 · X18 자리) | `attempt_reject` `:3230–3248` (옆 파일 쓰기 → 결과 줄 덧붙임 사이) · `recover_ledger` `:6366` (시도 **폴더** 만 훑음) | `python3 -I P6/final/probes/probe6f_real.py <tmp> R9` → 옆 파일 (`attempt_1.rejected.json`) + 결과 줄 전 죽음 → recover **rc 0** · "그룹 기록 0 개 정리 · 미확인 0" (아무것도 안 함) · 결과 줄 없음 · 같은 대상 `--add` = ATTEMPT_ORDER_MISMATCH · 같은 명령 다시 = rc 3 (옆 파일이 이미 있어 덮지 않음 = AL07b) → 손 말고 길 없음 · 대조 (폴더 안 rejected.json · PC13 꼴) = recover 가 rejected 결과 줄 · 다음 `--add` rc 0 | recover 가 rc 0 ("다 정리") 로 끝나면서 그 시도를 열어 둔다 · 그 대상 영구 멈춤 · 창 = 두 쓰기 사이 죽음 (드묾) | `recover_ledger` 가 바탕의 `attempt_<n>.rejected.json` 도 훑어 결과 줄 없는 항목에 rejected 결과 줄 (attempt_reject 와 같은 칸) · 못 고친 항목이 있으면 rc ≠ 0 |
| PC6-10 | P3 · 새 | `main` 인자 검사 `:6584–6589` (`'\n' in why or '\r' in why`) · `--operator-confirm` · `--attempt` · `--resume` = `type=int` | `python3 -I P6/final/probes/probe6f_unit.py <tmp> U5` → `--operator-why` \n · \r = rc 2 / U+2028 · U+0085 · \v · \f · \x1c · ESC (`\x1b[2J`) = 통과 (`str.splitlines` 2 조각) · `--operator-confirm` `１` (전각) · `+1` · ` 1 ` → 1 · `1_0` → 10 통과 | 등록 R 아 ④ "줄바꿈 없음" 이 \n · \r 만 · 끝 기록 · 화면에 줄 경계 · 터미널 제어 글자 그대로 (결정 영향 없음) · 번호의 유니코드 숫자 · 밑줄 = 같은 정수라 영향 없음 (한정) | `len(why.splitlines()) == 1 and why.isprintable()` · 번호 = ASCII 숫자 정규식 |
| PC6-11 | P3 · 새 (시험 공백 묶음) | §3-2 의 생존 변이 — 시험 공백 10 (덜 보수 쪽 M2e · M8 · M11 · M12 · M15 · 보수 쪽 M4 · M5 · M6 · M10a · M10b) + 풀기 전 층 2 (M2c · M9 — 뒤 판정이 막지만 재실행이 돎) | `python3 P6/final/probes/mutate_pc6.py <원 트리> <사본 트리> <결과 json> <로그 폴더> new` (사본 트리 = scripts 사본 · docs · webapp 링크) · 합친 넓은 확인 = `combine_survivors.py` + 전체 사슬 시험 · 끝-끝 (§3-3 · 406/407 = 변이 없는 사본과 같은 Y13 하나 · 40/40) · 뜻 실경로 = `python3 -I P6/final/probes/probe6f_mut_paths.py <tmp>` → 지금 사슬 = M2e · M2c · M9 꼴 셋 다 풀기 전 거부 (러너 0) / 변이 = 셋 다 재실행 **돎** (러너 14 · rc 0) · 판정 = M2c · M9 MISMATCH · **M2e = 원장 대조 통과** (INPUT_MISSING · 채택 [1, 2]) | 가드는 지금 동작하지만 (R11 · probe6f_mut_paths 의 지금 사슬 줄) 그 가드를 끄면 상주 사슬 시험 407 · 끝-끝 40 이 다 통과 → 다음 고침이 조용히 되돌려도 모른다 (5 회차 X09 · X18 과 같은 부류) · 특히 M2e 는 끄면 **판정 원장 대조까지 통과** (거짓 수용) · M2c · M9 는 끄면 재실행이 GPU 를 쓴 뒤에야 판정이 막음 (PC5-01 "풀기 전 거부 · 러너 0 회" 가 재실행 2 이상 사슬에서 시험 밖) | 생존 변이마다 상주 시험 (R11 = M2e · 실경로 pid 다시 쓰임 = M4 · 덧붙이는 중 읽기 = M5 · "커밋은 됐는데 git 실패" = M6 · 합친 예측 다시 판정 + 같은 단위 뒤 시도 = M8 · 재실행 2 이상 사슬의 끝 줄 바꿈 (probe6f_mut_paths 의 M2c · M9 꼴 · 풀기 전 거부 · 러너 0) · 그룹 시작 전 못 읽는 프로세스 실경로 = M10a · M10b · 가짜 /proc stat EACCES = M11 · chain_pid 없는 시작 기록 = M12 · 예측 단계 사슬 예외 (PC10 의 예측 쪽) = M15 · 결정 동등 M2a · M2b · M7 은 시험 불요) |

## 3. 변이 시험

방법 — 스크래치 사본 트리 (`scripts/` 사본 · `docs` · `webapp` 링크 · `.gitignore`) 에 변이 하나씩 (`final/probes/mutate_pc6.py` · 옛 글 정확히 한 번 · 파이썬 문법 검사) → 접두 시험 (`scripts/test_rint_r_chain.py --only …`) · 기준 (변이 없음) `PC,AL,RS,UM,GR` = **94/94** (180 s).  "잡힘" = 그 시험이 FAIL · "옳은 이유" = FAIL 줄의 값이 그 가드가 막는 결과 쪽으로 바뀌었는가 (시험 틀이 값 글을 600 자에서 자른다 `scripts/test_rint_r_chain.py:10423` → 자른 뒤에 결정 칸이 있으면 시험 식을 읽어 판단 = "코드 읽기").  요약 = `final/logs/mutation_summary.json` (변이 · 가드 · 접두 · 실패 시험 · 사유 앞 400 자 · 초) · 화면 전문 = 스크래치.

### 3-1. 10-28 의 32 (`docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/fix_pc5_20261028/mutate_pc5.py` 를 그대로 불러 씀) — 다시 **32/32 잡힘 · 옳은 이유 32** (값으로 30 · 코드 읽기 2)

| 변이 | 가드 | 잡은 시험 | 실패 값 요지 | 옳은 이유 |
|---|---|---|---|---|
| P01a | 판정 · 합치기 결과 줄 다시 셈 끔 | PC01 · PC01m | 판정 honest · reset · amend 다 INPUT_STAGE_STOPPED (기대 = reset · amend MISMATCH) · 합치기 TIME_LIMIT (기대 MISMATCH) | ✓ |
| P01b | 재실행 풀기 전 다시 셈 끔 | PC01 | 판정 reset · amend = MISMATCH 그대로 → 남은 실패 칸 = `refused` (재실행 시도 rc · 거부 기록 · 러너 수 — 600 자 밖) | ✓ (코드 읽기 · 시험 `:9673–9674`) |
| P01c | 예측 입력 다시 셈 끔 | PC01i | 예측 rc 0 · 멈춤 없음 · 러너 24 회 (기대 MISMATCH · 0 회) | ✓ |
| P01d | 원장 역사 첫 부모 밖 검사 끔 | PC02 | 역사 None · 판정 INPUT_MISSING (기대 사유 · MISMATCH) | ✓ |
| P02a | cupy 클래스 이름 둘 자원 낱말에 되살림 | PC03 · PC04 | assert · misaligned = resource · 자격 True (기대 runner_rc · False) | ✓ |
| P02b | 잘못된 주소를 자원 낱말 뒤에 봄 | PC03 | OOM + 잘못된 주소 = resource · True | ✓ |
| P03a | recover 산 사슬 검사 끔 | PC05 | 산 사슬인데 recover rc 0 · 끝 기록 씀 (기대 rc 3) | ✓ |
| P03b | 사슬 부모 시작 시각 대조 끔 | PC05 | pid 다시 쓰임 = 산 사슬 → rc2 3 (기대 0) | ✓ |
| P03c | 시작 시각 칸 없음 = 죽은 사슬 | PC05 | rc3 0 (기대 3 · 보수) | ✓ |
| P04a | 다른 부팅을 볼 수 있는 쪽으로 | GR08 · PC06 · PC06b | 재부팅 · 모르는 기계 재부팅 = 확인 · rc 0 (기대 미확인) | ✓ |
| P04b | machine_id 다름 검사 끔 | GR08 | 다른 기계 = 확인 (기대 미확인) | ✓ |
| P04c | 운영자 표지 시도 폴더 범위 끔 | PC06b | rc 0 · 시도 2 의 그룹도 표지 (기대 rc 3 · 시도 1 만) | ✓ |
| P04d | 쓰이지 않은 표지 = rc 3 끔 | PC06b | 첫 rc 3 그대로 → 남은 실패 칸 = rc3 (볼 수 있는 그룹만 가진 시도의 표지 — 600 자 밖) | ✓ (코드 읽기 · 시험 `:9914–9916`) |
| P04e | 운영자 번호 · 사유 꼴 검사 끔 | PC06 | 꼴 틀린 표지가 rc 2 로 안 막힘 | ✓ |
| P05a | 결과 전 멈춘 재실행 건너뜀 끔 | PC07 | 바른 인자 재실행 `--add --resume` rc 3 (기대 0) | ✓ |
| P06a | 요약 없는 시도 원인 = 늘 parent_dead · 읽음 | PC08 · PC09 | 잘못된 주소 로그 → parent_dead · 자격 True (기대 runner_rc · False) | ✓ |
| P06b | 요약 있는 길 잘못된 주소 낱말 끔 | PC11 | 신호 + 잘못된 주소 = signal · 자격 True | ✓ |
| P06c | 사다리 사슬 예외 = 요약 · 결과 줄 없이 다시 올림 | PC10 | 요약 없음 · 다음 `--add` = 앞 결과 줄 없음 rc 3 | ✓ |
| P06d | 런 로그 못 읽음 = 읽음으로 | PC09 | 로그 없음 → 자격 True (기대 False) | ✓ |
| P06e | 못 읽음을 자격에서 뺌 | PC09 | 같음 | ✓ |
| P07a | Z 지도자의 산 스레드 끔 | PC14 | 그 프로세스 못 봄 · 늦은 파일 생김 · left_after_exit 0 | ✓ |
| P07b | environ 못 읽음 = 건너뜀 (옛) | PC14 | unread [] (기대 None) | ✓ |
| P07c | 그룹 시작 전 거름 끔 | PC14 | old_since None (기대 []) | ✓ |
| P07d | 다른 실 uid 거름 끔 | PC14 | other_uid None (기대 []) | ✓ |
| P07e | pid 1 셈 밖 끔 | PC14 · PC05 | pid1 None (기대 []) · PC05 = 이 컨테이너의 실제 pid 1 environ 못 읽음 → 미확인 (환경이 더 잡음) | ✓ |
| P08a | 덧붙임 실패 뒤 되돌림 끔 | PC15 | index.lock 뒤 작업 파일 ≠ HEAD · 다음 `--add` rc 3 | ✓ |
| P08b | 배타 잠금 끔 | PC15 | 동시 `--add` 둘 = 둘 다 멈춤 (기대 하나 성공 · 하나 멈춤) — 경합 꼴은 "둘 다 실패" (같은 번호 둘 커밋은 이 실행에서 안 나옴) | ✓ |
| P08c | `--init` git 실패 뒤 되돌림 끔 | PC15 | init 실패 뒤 남은 파일 · 다음 init rc 3 | ✓ |
| P10a | 다시 판정 다른 대상 너그러움 끔 (옛) | PC16 | REVERIFY_DIFF (기대 SAME) | ✓ |
| P10b | 같은 대상 뒤 시도도 너그럽게 | PC16 | REVERIFY_SAME (기대 DIFF) | ✓ |
| X09 | 결과 줄 꼴 rejected ↔ 결과 뒤 · 자격 검사 끔 | PC12 | rejected · post 손 줄 = 원장 꼴 통과 | ✓ |
| X18 | recover 의 rejected.json 폴더 = rejected 결과 줄 끔 | PC13 | recover 결과 줄 = interrupted · parent_dead (기대 rejected) | ✓ |

### 3-2. 이 회차가 더한 PC5 가드 변이 20 (`M1`–`M15` · 옛 글이 PC5 앞 판 `32455d9c0` 사슬에 없음 = PC5 가 들인 글 · 20/20 확인) + 대조 1 (`M16` · PC5 전 C2b 가드) — 접두 `PC,AL,RS,UM,GR` (94)

| 변이 | 가드 (사슬 줄) | 결과 | 잡은 시험 · 사유 | 판정 |
|---|---|---|---|---|
| M1 | `ledger_history_problem` 숨긴 커밋 셈 `--full-history` 뺌 (`:2777`) | 잡힘 92/94 | PC02 (역사 None · 판정 INPUT_MISSING) · AL12d (다시 판정 REVERIFY_DIFF — 역사 검사 결과가 달라짐) | 옳은 이유 ✓ |
| M2a | `RECOUNT_KEYS` 에서 status 뺌 (`:2692`) | **생존** 94/94 | — | **결정 동등** (코드 읽기 — 원장 꼴 검사 `:2872–2885` 가 status 를 stop · side · resume_ok 와 묶고 채택 · 자격은 status 의 completed · rejected 만 본다 → 남은 칸이 다시 세지면 status 만 바꿀 수 있는 꼴 = stopped ↔ interrupted · 요약 없는 interrupted ↔ completed 뿐 · 그 둘 = 채택 · 자격 · 합치기 거부 같음 · U6 = 채택 함수 한정 실측) |
| M2b | stop 뺌 | **생존** | — | **결정 동등** (코드 읽기 — 결과 줄 stop 칸 = 꼴 검사 · 화면에만 · 원인 · 판정은 폴더 요약에서) |
| M2c | side 뺌 | **생존** | — | **뒤 판정이 막음 · 재실행은 돎** — `probe6f_mut_paths.py` M2c: 재실행 2 (결과 뒤 · runner_rc · 자격 False) 끝 줄의 side 만 pre → 지금 = 풀기 전 거부 (러너 0) / 변이 = 재실행 3 돎 (러너 14 · rc 0 · 채택 [1, 3]) · 판정 = MISMATCH (`target_ledger_problem` `:3735–3737` 폴더 결과 전 · 뒤 대조) |
| M2d | cause 뺌 | 잡힘 93/94 | PC01i (원인 칸만 바꾼 끝 줄 → 예측이 돎) | 옳은 이유 ✓ |
| M2e | resume_ok 뺌 | **생존** | — | **시험 공백 · 거짓 수용** — `probe6f_mut_paths.py` M2e: 끝 줄 resume_ok 만 True → 지금 = 풀기 전 거부 · 판정 MISMATCH / 변이 = 재실행 돎 (러너 14 · rc 0) · **판정 원장 대조 통과** (INPUT_MISSING · 채택 [1, 2]) |
| M3 | `chain_parent_alive` 자기 자신 = False → None (`:2466`) | 잡힘 92/94 | AL13 · RS02 (같은 프로세스 recover = 미확인 rc 3) | 옳은 이유 ✓ (중간 예측 = PC13 · 실제 = AL13 · RS02) |
| M4 | `run_in_group` 시작 기록 chain_start = None (`:2570`) | **생존** | — | **시험 공백 · 보수 쪽** (코드 읽기 — 사슬 pid 가 다시 쓰이면 산 사슬로 보아 recover rc 3 이 그 pid 가 끝날 때까지 · 시작 시각 대조 시험 (PC05) 은 손으로 만든 시작 기록 (`gr_fake_launch`) 만 — 생산자 칸 미검사) |
| M5 | `ledger_now` 공유 잠금 끔 (`:2844`) | **생존** | — | **시험 공백 · 보수 쪽** (코드 읽기 — 덧붙이는 중 읽기 = 반쯤 쓴 작업 파일 → 거짓 MISMATCH · 그런 시험 없음) |
| M6 | `ledger_append` 커밋은 됐는데 git 실패 → 늘 되돌림 (`:2991`) | **생존** | — | **시험 공백 · 보수 쪽** (코드 읽기 — HEAD = 새 줄 · 작업 파일 = 옛 → 원장 멈춤 · PC15 는 커밋 전 실패 (index.lock) 만) |
| M7 | `_ledger_rollback` 색인 `git reset` 뺌 (`:2962`) | **생존** | — | **결정 동등** (코드 읽기 — `_ledger_now` `:2828` 는 작업 파일 ↔ HEAD 만 · 다음 덧붙임의 `git add` + 경로 커밋이 색인을 덮음 · 설명문 스스로 "실패해도 넘어간다") — 색인에 커밋 안 된 줄이 남는 위생 차이만 |
| M8 | 다시 판정 `keep` 에서 합친 예측 단위 · 점 대상 뺌 (`:3799`) | **생존** | — | **시험 공백 · 거짓 수용 쪽** (코드 읽기 — 합친 예측 다시 판정 뒤 같은 단위 대상의 뒤 시도를 너그럽게 = 거짓 REVERIFY_SAME · PC16 은 사다리 판정만) |
| M9 | `resume_chain_problem` 다시 셈 = 원 시도만 (`:3351`) | **생존** | — | **뒤 판정이 막음 · 재실행은 돎** — `probe6f_mut_paths.py` M9: 재실행 2 끝 줄의 cause · resume_ok → resource · True → 지금 = 풀기 전 거부 (러너 0) / 변이 = 재실행 3 돎 (러너 14 · 채택 [1, 2, 3]) · 판정 = MISMATCH (다시 셈) |
| M10a | `run_in_group` 이 GROUP_SINCE 안 넣음 (`:2613`) | **생존** | — | **시험 공백 · 보수 쪽** (코드 읽기 — 그룹 시작 전의 못 읽는 같은 uid 프로세스도 미확인 → PC6-01 이 넓어짐 (런 전에 연 ssh 세션도) · PC14 는 since 를 손으로 넘긴다) |
| M10b | `recover_group` 이 GROUP_SINCE 안 넣음 (`:6276`) | **생존** | — | 같음 (recover 쪽) |
| M11 | `group_members` stat 못 읽음 = 건너뜀 (`:2451`) | **생존** | — | **시험 공백 · 거짓 확인 쪽** (코드 읽기 — stat 못 읽는 그룹 원을 셈에서 빼 확인 True · 같은 uid 의 stat 은 보통 읽혀 빈도 낮음 = 추정) |
| M12 | `chain_parent_alive` chain_pid 칸 없음 = 죽은 것 (`:2464`) | **생존** | — | **시험 공백 · 덜 보수** (코드 읽기 — chain_pid 없는 옛 시작 기록 (PC5 전 · 고정물) 이면 산 사슬의 그룹도 recover 가 정리 · 지금 사슬의 시작 기록엔 늘 있다) |
| M13 | `orphan_cause` 끝 기록 원인 exception → parent_dead (`:3564`) | 잡힘 93/94 | PC09 (chain_exception 끝 기록 → parent_dead · 자격 True) | 옳은 이유 ✓ |
| M14 | `stop_cause` CHAIN_EXCEPTION 가지 뺌 (`:3500`) | 잡힘 93/94 | PC10 (요약 = STOPPED · CHAIN_EXCEPTION 인데 결과 줄 원인이 chain_exception 아님) | 옳은 이유 ✓ |
| M15 | 예측 단계 사슬 예외 = 요약 · 결과 줄 없이 다시 올림 (`:5143` · P06c 의 예측 쪽) | **생존** (접두 94 · 전체 407 · 끝-끝 40 = §3-3) | — | **시험 공백 · 덜 보수** (코드 읽기 — 예측 쪽 PC5-06 ② 시험 없음 (PC10 = 사다리만) → 요약 · 결과 줄 없음 → recover → 끝 기록 rc 만 → parent_dead (자격) 길) |
| M16 (대조) | C2b 끝 기록 `confirmed` 를 늘 True (`:2618` · PC5 전 글) | 잡힘 89/94 | GR10 · GR11 · AL13 · AL13b · RS02 | 틀이 잡을 수 있음 ✓ |

정리 — 새 20 중 **잡힘 5** (M1 · M2d · M3 · M13 · M14 · 옳은 이유 5) · **생존 15** = 결정 동등 3 (M2a · M2b · M7) · 뒤 판정이 막음 (재실행은 돎) 2 (M2c · M9) · 시험 공백 10 (거짓 수용 · 덜 보수 쪽 M2e · M8 · M11 · M12 · M15 / 보수 쪽 M4 · M5 · M6 · M10a · M10b).  실경로로 뜻을 잰 것 = M2e · M2c · M9 (`final/logs/probe6f_mut_paths.out`) · 나머지 분류 = 코드 읽기.

### 3-3. 생존 15 를 한 사본에 합친 넓은 확인 (`final/probes/combine_survivors.py` · RECOUNT_KEYS = ('cause',) + 나머지 11 변이 · 문법 검사)

| 묶음 | 합친 사본 | 변이 없는 사본 (기준) | 판정 |
|---|---|---|---|
| `scripts/test_rint_r_chain.py` 전체 | **406/407** · 실패 = Y13 하나 (443 s) | **406/407** · 실패 = 같은 Y13 하나 (574 s · 같은 값 = 무시 검사 rc 128 · CODE_PIN_MISMATCH) | Y13 = 사본 트리가 git 저장소가 아님 (`git check-ignore --no-index` rc 128 · 사본 환경) → 변이 탓 아님 · 나머지 406 이 생존 15 를 다 못 잡음 |
| `scripts/test_rint_r_chain_e2e.py` 전체 | **40 PASS · 0 FAIL** (553 s) | (중간 보고 실측 40 · 0 = 리포 작업 트리) | 생존 15 를 다 못 잡음 |

⇒ 생존 15 는 상주 사슬 시험 407 · 끝-끝 40 어디에도 안 걸린다 (합쳐 넣어도 · 사본 환경 Y13 뺌).  하나씩 넣은 꼴은 접두 94 만 돌렸다 — 서로 가리는 일은 드물다고 보아 합친 판의 통과를 하나씩의 통과로 읽는다 (추정).

## 4. 중간 보고 대비

| 중간 id | 중간 등급 | 이 회차 | 이유 (이 회차 실측) |
|---|---|---|---|
| PC6-01 | P1 (조건부) | **확인 · 넓힘** (P1 조건부 그대로) | 중간 탐침 다시 = 같은 값 · 새 R8a (구경꾼 0.7 s 로 충분 · 대기 상한 30 s 안 씀) · R8b (운영자 자기 ssh 세션 아래의 recover 도 rc 3 · 고아 러너 안 죽임 · 같은 호스트엔 운영자 표지 없음) · R8c (다른 사용자 stat 못 읽음 = 미확인 → hidepid=1 이면 늘) — 조건 (kgy 사용자 · ssh 세션 자격 · /proc 옵션) 은 여전히 미확인 |
| PC6-02 | P2 | **확인 · 넓힘** (P2 그대로) | U1 42 중 36 · R1 · R1c · R2 다시 같음 · 새 U4 = GROUP_UNCONFIRMED 가 러너 rc 1 (파이썬 KeyError traceback 포함) 을 가려 재실행 자격 — CUDA 부류만의 일이 아니다 |
| PC6-03 | P3 | 확인 | R3 다시 같음 (SIGINT = chain_exception · false / SIGTERM = signal · true / SIGKILL = parent_dead · true) |
| PC6-04 | P3 | 확인 | R4 (고친 판 = 지금 탐침 파일) 다시 같음 — SIGTERM · SIGHUP · SIGKILL = 원장 멈춤 · SIGINT = 되돌림 |
| PC6-05 | P3 | 확인 | U2 다시 같음 · 빈도 낮음 (사슬이 로그를 만든다) 을 덧붙임 |
| PC6-06 | P3 | 확인 · 뉘앙스 | U3 다시 같음 · 요약 쓰기 (`:4934` try 밖) 의 ENOSPC 는 parent_dead · 자격으로 갈 것 (코드 읽기 · 미실행) |
| PC6-07 | P3 (추정 · 미실행) | **철회** | R5 실측 — (a) 원 시도 = 바닥 완주 · 천장 표지 전 rc 2 → runner_rc · post · false · `--add --resume` rc 3 · 새 `--add` rc 3 (ATTEMPT_AFTER_ADOPTED) (b) 재실행 = 바닥 복사 (`resume.copied = [L01_floor]`) 뒤 천장 표지 전 rc 2 → 같은 줄 · 다시 재실행 rc 3 (c) 새 시도 첫 런 표지 전 rc 2 → pre → 새 `--add` rc 0.  재실행은 **같은 자리의 원 시도와 같은 답** — 중간 보고는 다른 자리 (첫 런 ↔ 둘째 런) 를 비교했다.  Q9 개정 7 "결과 전 멈춘 재실행 = 건너뜀" 은 복사 전 단계 관문 멈춤에만 닿는다 (한정 한 줄이면 충분 · §5) |
| PC6-08 | P3 (코드 읽기) | **확인 (실경로)** | R9 — 옆 파일 + 결과 줄 전 죽음 → recover rc 0 인데 아무것도 안 함 · 그 대상 영구 멈춤 (중간 보고보다 나쁜 점 = recover 가 성공으로 끝남) |
| (중간 §3 계획 M1–M10) | — | 실행 | §3-2 (M1 · M2d · M3 잡힘 · 나머지 M2a · M2b · M2c · M2e · M4 · M5 · M6 · M7 · M8 · M9 · M10a · M10b 생존) · 중간 예측은 방향이 다 맞음 — M1 = PC02 (+ AL12d) · M2e 생존 · M3 잡힘 (예측 PC13 → 실제 AL13 · RS02) · M4 · M5 · M6 · M8 · M9 · M10 생존 · M7 동등 · 예측에 없던 것 = M2a · M2b (결정 동등) · M2c (뒤 판정이 막음) 생존 · M2d 잡힘 (PC01i) · 이 회차가 더 넣은 M11 · M12 · M15 생존 · M13 · M14 잡힘 |
| (중간 §5 의 남은 일) | — | 실행 | 숫자 주장 다섯 (§1) · 고치기 전 판 7/26 (§1) · 변이 (§3) · R5 (PC6-07) · PC6-08 실경로 (R9) · PC5-01 독립 공격 넓히기 = R7 (git replace) · R10 (항목 대상 바꿈 = **PC6-12**) · R11 (resume_ok 만) · kgy 쪽 확인 (PC6-01 조건) = 안 함 (kgy 접속 없음) |

## 5. Codex 회차 ② 요청서에 한정으로 적을 것

고치지 않고 회차 ② 로 가면 아래를 **요청서 맨 위 "닫지 않는 것"** 에 적는다 (고치면 그 줄은 "닫는 것 + 시험 이름" 으로 바꾼다).

| # | 한정 문장 (요청서 꼴) | 근거 |
|---|---|---|
| 1 | PC5-01 다시 셈은 **원장이 그 대상의 시도라고 적은 항목** 에만 돈다 — 원장 항목 줄 (대상) 을 바꾼 역사 고침 (끝 두 커밋 reset + 대상만 다른 항목) 은 결과 본 시도를 입력 대상 밖으로 숨겨 판정을 통과한다 (PC6-12 · 고치기 전까지 "끝 커밋 교체 = 거부" 는 결과 줄 칸 (원인 · 재실행 자격 · status · stop · side) 을 바꾼 꼴에 한정) | R10 |
| 2 | "그 밖 CUDA 오류 = 자동 재실행 없음 (runner_rc)" 은 러너 rc ≠ 0 · 그룹 원인 없음 길에서만 — 시간 초과 · 신호 · 그룹 미확인 · 사슬 부모 사망 길에선 잘못된 주소 둘만 runner_rc · GROUP_UNCONFIRMED 는 러너 rc ≠ 0 (파이썬 결함 포함) 도 재실행 자격으로 만든다 (PC6-02) | U1 · U4 · R1 · R2 |
| 3 | 그룹 종료 확인 = 사슬과 같은 실 uid 이고 environ (또는 stat) 을 못 읽는 프로세스가 그룹 시작 뒤 생겨 그룹 끝에 살아 있으면 미확인 (GROUP_UNCONFIRMED · recover rc 3) — ssh 로그인 세션 · setuid · agent 꼴 · 운영자의 그 ssh 세션 자신 포함 · 같은 호스트엔 운영자 표지 없음 · 거짓 수용 없음 = 활성 결함 · kgy 조건 (사슬 사용자 · ssh 세션 자격 · /proc hidepid) 미확인 (PC6-01) | probe6_uid · R8a–c |
| 4 | 사슬 부모 사망 뒤엔 반드시 `--stage recover --out <시도 폴더> --ledger` 먼저 — 같은 `--attempt` 명령을 다시 치면 결과 뒤 시도가 rejected · 결과 전으로 적히고 (그룹 확인 없이) 다음 시도가 열린다 (PC6-09 · 고치기 전까지 운영 규칙) | R6 |
| 5 | 원장 덧붙임의 되돌림 = 파이썬 예외 (index.lock · SIGINT) 에서만 · SIGTERM · SIGHUP · SIGKILL = 작업 파일 · 색인에 커밋 안 된 줄 → 손 git 전까지 원장 멈춤 (PC6-04 · 등록 R 아 ⑧ 문장) | R4 |
| 6 | 운영자 중단 신호의 원인 = SIGTERM · SIGHUP = signal (자격) · SIGKILL = parent_dead (자격) · **SIGINT = chain_exception (재실행 불가)** (PC6-03) · 사슬 자신의 MemoryError · ENOSPC = chain_exception (재실행 불가 · 자리에 따라 parent_dead) (PC6-06) · 요약 있는 길의 런 로그 없음 = 낱말 없음 (자격) (PC6-05) | R3 · U3 · U2 |
| 7 | 옆 거부 기록 (`attempt_<n>.rejected.json`) 을 쓰고 결과 줄 전에 죽으면 recover 가 고치지 못한다 (rc 0 으로 끝남) — 그 대상 = 손으로만 (PC6-08) | R9 |
| 8 | GPU 런 재실행 금지 = 등록 규칙뿐 (사슬은 GPU 시도의 `--resume` 을 막지 않는다 · REPORT_C_decisions §4 #3 그대로) — PC6-01 · 02 와 겹치면 "끝났는데 미확인" · "코드 결함인데 자격" 이 규칙 판단으로 넘어간다 | REPORT_C_decisions §4 #3 |
| 9 | 원장 저장소의 `git replace` · grafts 를 끄지 않는다 (`ledger_git` 에 `core.useReplaceRefs=false` 없음) — 같은 sha 에 다른 내용을 읽힐 수 있다 · 결과 줄은 다시 셈이 잡는다 (R7 = 잡힘) · 항목 줄은 1 번과 같은 한정 · replace 참조가 없는 clone 에서 다시 판정하면 다른 내용 (보수 쪽) | R7 |
| 10 | 변이 "32/32" = 10-28 에 고른 32 가드 · 이 회차가 더한 PC5 가드 변이 20 중 15 생존 (결정 동등 M2a · M2b · M7 · 뒤 판정이 막음 M2c · M9 · 시험 공백 M2e · M4 · M5 · M6 · M8 · M10a · M10b · M11 · M12 · M15 — 합쳐도 상주 사슬 시험 407 · 끝-끝 40 통과) — 다시 셈 다섯 칸 중 상주 시험이 따로 묶는 칸 = cause (PC01i) 뿐 · resume_ok 는 지금 동작 (R11) 하지만 시험이 없고 끄면 판정 원장 대조까지 통과 (probe6f_mut_paths M2e) | §3-2 |
| 11 | PC5-09 = 고치지 않음 (1저자 Q1 · wontfix) — 쓰는 중 · 검사 전 죽은 payload 도 검사 실패 흔적 (보수 쪽 오거부) | 계획 Q1 |
| 12 | Q9 개정 7 "결과 전 멈춘 재실행 = 건너뜀" = 복사 전 (단계 관문) 에서 멈춘 재실행만 — 끝난 런을 복사한 재실행은 원 시도와 같이 결과 뒤 (R5 · 같은 자리 원 시도와 같은 답) | R5 |
| 13 | `--operator-why` 의 "줄바꿈 없음" = \n · \r 만 (U+2028 · U+0085 · \v · \f · ESC 통과 · 결정 영향 없음) · 번호 인자 = 파이썬 int (전각 숫자 · 밑줄 · ± · 빈칸 받음 · 같은 정수) (PC6-10) | U5 |
| 14 | 이 회차 = 이 컨테이너 3.11.17 만 · kgy 3.8 판 · 게이트 = 메인 · 실제 GPU · 실제 sshd · kgy /proc · 다른 호스트 확인 없음 | §0 미확인 |

## 6. 원장 등재 후보 (적용 안 함 · 메인 판단 · 중간 보고 §6 을 대신한다)

```text
{"id": "PC6-12", "severity": "P1", "status": "open", "owner": "claude", "found_by": "사전 공격 6 회차 마무리 (11-02 · d6e8d1b44 = 사슬 4c69070ad 와 같음 · 독립 작업 트리)", "opened_in": "docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/PREATTACK_C2_final.md", "title": "판정 원장 대조가 찾은 시도 폴더의 attempt.json (대상 · 시작 커밋) 을 원장 항목과 대조하지 않는다 (입력 대상 항목만) — 끝 두 커밋 reset + 항목 1 의 대상만 바꾼 줄 (원장만 고침) 이면 결과 본 시도 (runner_rc · 재실행 불가) 가 입력 대상 밖으로 숨고 새 시도가 채택 · 판정 통과 (PC5-01 다시 셈 비켜 감 · 5 회차 PC-01 은 같은 부류를 P2 로 매김 — 등급 메인 판단)"}
{"id": "PC6-01", "severity": "P1", "status": "open", ..., "title": "PC5-07 그룹 원 찾기 — 같은 실 uid 이고 environ · stat 을 못 읽는 무관 프로세스 (ssh 로그인 세션 · setuid · agent · 운영자 자기 ssh 세션) 가 그룹 끝에 있으면 끝난 런 GROUP_UNCONFIRMED · 대기 상한 안 씀 (0.7 s 구경꾼으로 충분) · 보이는 고아 런 안 죽임 · recover 도 rc 3 · 같은 호스트엔 운영자 표지 없음 → GPU 런이면 규칙 라로 그 대상 STOPPED (조건부 · 보수 쪽)"}
{"id": "PC6-02", "severity": "P2", "status": "open", ..., "title": "Q2 '그 밖 CUDA 오류 = 자동 재실행 없음' 이 러너 rc 길에서만 — 시간 초과 · 신호 · 그룹 미확인 · 부모 사망 길 = 재실행 자격 (42 중 36) · GROUP_UNCONFIRMED 는 러너 rc 1 (파이썬 결함 포함) 도 가려 자격 (U4)"}
{"id": "PC6-09", "severity": "P2", "status": "open", ..., "title": "사슬 부모 사망 뒤 같은 --attempt 명령을 다시 치면 attempt_open 이 이미 있는 자기 시도 폴더를 남의 폴더처럼 옆 거부 기록 + rejected · 결과 전 결과 줄 (그룹 확인 없이 · 결과 뒤 시도) → 같은 대상 새 시도 열림 · 고아 런과 동시 · 판정은 '원장에 없는 시도 폴더' 하나로만 막힘 (폴더를 치우면 통과)"}
{"id": "PC6-03", "severity": "P3", "status": "open", ..., "title": "SIGINT (Ctrl-C) = run_in_group 원인 exception → chain_exception · 재실행 불가 (SIGTERM = signal · SIGKILL = parent_dead 는 자격)"}
{"id": "PC6-04", "severity": "P3", "status": "open", ..., "title": "원장 덧붙임 중 SIGTERM · SIGHUP · SIGKILL = 되돌림 없음 → 색인에 커밋 안 된 줄 · 원장 멈춤 (등록 R ⑧ '신호 = 되돌림' 은 SIGINT 만)"}
{"id": "PC6-05", "severity": "P3", "status": "open", ..., "title": "요약 있는 길 · 멈춘 런 로그 없음 · 못 읽음 + 시간 초과 · 신호 = 재실행 자격 (요약 없는 길은 같은 꼴 = 불가)"}
{"id": "PC6-06", "severity": "P3", "status": "open", ..., "title": "사슬 자신의 MemoryError · ENOSPC = CHAIN_EXCEPTION · 재실행 불가 (러너의 같은 원인 = resource · 요약 쓰기 자리의 ENOSPC = parent_dead 로 갈 것 · 코드 읽기)"}
{"id": "PC6-08", "severity": "P3", "status": "open", ..., "title": "옆 거부 기록 attempt_<n>.rejected.json + 결과 줄 전 죽음 = recover_ledger (폴더만 훑음) 가 못 고치고 rc 0 으로 끝남 → 그 대상 영구 멈춤 (실경로 R9)"}
{"id": "PC6-10", "severity": "P3", "status": "open", ..., "title": "--operator-why 꼴 검사 = \\n · \\r 만 (U+2028 · U+0085 · \\v · \\f · \\x1c · ESC 통과) · 번호 인자 = 파이썬 int (전각 숫자 · 밑줄 받음)"}
{"id": "PC6-11", "severity": "P3", "status": "open", ..., "title": "PC5 가드 변이 생존 (시험 공백) — M2e (resume_ok 다시 셈 · 끄면 판정 원장 대조까지 통과) · M8 · M11 · M12 · M15 (덜 보수 쪽) · M4 · M5 · M6 · M10a · M10b (보수 쪽) + 풀기 전 층 M2c · M9 (뒤 판정이 막지만 재실행이 돎) — 가드는 지금 동작 · 생존 15 를 합쳐 꺼도 상주 사슬 시험 407 · 끝-끝 40 이 다 통과 (사본 환경 Y13 뺌)"}
```

(`...` = found_by · opened_in · owner 는 PC6-12 와 같다.  중간 PC6-07 = 철회 — 등재하지 않는다.)

## 7. 근거 파일 · 다시 돌리기

- 이 회차 새 탐침 (`P6/final/probes/`): `probe6f_real.py` (R5 · R6 · R7 · R9 · R10 · R11 · 시험 틀 고정물 · 가짜 러너 그대로 · 시험 · 사슬 파일 무변경) · `probe6f_unit.py` (U4 · U5 · U6) · `probe6f_uid.py` (root · R8a · R8b · R8c · 중간 `probes/probe6_uid.py` 의 구경꾼 꼴을 불러 씀) · `probe6f_mut_paths.py` (생존 변이 M2e · M2c · M9 를 같은 프로세스 안에서 · 지금 사슬 ↔ 변이 · 판정 = 재실행 시도가 있는 바탕) · `probe6f_m2e.py` (첫 판 · 대신함 — 판정에 원 바탕만 넣어 "폴더 없음" MISMATCH 가 났다 = 원장 대조의 뜻이 아님 · 기록으로 둠) · 변이 틀 `mutate_pc6.py` (10-28 `mutate_pc5.py` 의 32 를 그대로 불러 + M1–M16) · `combine_survivors.py` (생존 변이 합친 사본) · `mut_summary.py` (변이 요약 JSON).
- 중간 탐침 다시 (`P6/probes/`): `probe6_unit.py <tmp> U1,U2,U3` · `probe6_real.py <tmp> R1,R1c,R2,R3,R4` · (root) `probe6_uid.py` — 값 = 중간 보고와 같음.
- 출력 (`P6/final/logs/`): 탐침 JSON 줄 · 묶음 시험 끝 줄 (`suites_summary.txt`) · 변이 요약 (`mutation_summary.json`) · 합친 생존 넓은 확인 (`combined_survivors.txt`) — 변이마다 화면 전문 · 사본 트리는 스크래치 (리포 밖 · 다시 돌리기 = 위 명령).
- 사본 트리 만들기 (변이 · 고치기 전 판): 변이 = 스크래치에 `scripts/` 사본 + `docs` · `webapp` 링크 + `.gitignore` · 고치기 전 판 = `git archive <커밋> scripts .gitignore docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md docs/reviews/rint2_kgy_commands_20261020.md docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` + `docs/data` 링크.
