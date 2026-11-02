<!-- 본문 = 사전 공격 7 회차 에이전트 반환문 (11-02 · 메인이 파일로 저장 · 고친 것 = 기준 커밋 표기 · P7 줄임 경로) -->
# 사전 공격 7 회차 — Rint ② PC6 고침 독립 재공격 (대상 `d6e8d1b44..0658c0ac6` · 사슬 · 시험 · 등록 R §10-5)

결론: **새 P1 후보 1 · P2 2 · P3 4.** 고침 자체는 고친 꼴(R10 · R6 · U4 · 표지 표)을 닫았다. 다만 닫힘 주장 셋이 실제 범위보다 넓다: PC6-09 는 같은 `--out` 에서만, PC6-12 는 꼴 맞는 attempt.json 이 있는 폴더에서만, PC6-13 의 "자리 전수" 는 하나가 빠졌다. 숫자 · 줄 번호 · 커밋 주장은 전부 git · 로그와 맞다.

- 작업 트리: `0658c0ac6` 에서 가지 `preattack7-review` → 커밋 `8a7d89df8` (push 안 함). 증거 폴더 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/` (SHA256SUMS 30).
- 환경: 이 컨테이너 · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · root · BLAS 스레드 1. 사슬 · 시험 · findings.json · CLAUDE.md 는 고치지 않았다.
- 기준 표기: 고침 에이전트의 기준 커밋 (`7d6…` 형제 가지 = d6e8d1b44 + 덱 커밋 1 · 본 가지 조상 아님) 은 대상 세 파일이 `d6e8d1b44` 와 diff 0 줄이라 범위가 같다 → 이 문서에서는 `d6e8d1b44` 로 적는다 (메인 · 반입 때 바꿈).
- 내가 다시 돌린 시험 (0658c0ac6): 사슬 **428/428 (435.6 s)** · 끝-끝 **40 PASS · 0 FAIL (525.3 s)**.

## 1. 지적 (PC7-NN · 척도 = 6 회차와 같음)

명령은 작업 트리 꼭대기에서 실행한다 (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`). `P7` = `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7`.

| id | 등급 | 자리 (0658c0ac6) | 반례 → 실측 | 영향 | 고침 제안 |
|---|---|---|---|---|---|
| **PC7-01** | **P1 (후보 · 메인 판단)** · PC6-09 범위 | `attempt_open` :3389 (새 바탕이면 `folder.mkdir()` 성공 → PC6-09 가지를 안 탐) · `recover_ledger` :6603–6604 (결과 줄이 있으면 폴더를 대조하지 않고 넘어감) | `python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_real.py <tmp> C` → 원 시도 1 = 결과 뒤 · 부모 SIGKILL 뒤에도 그룹 삶 → 같은 `--attempt 1` 을 **다른 `--out`** 으로 → rc 0 · CALIBRATED (처음부터 다시 돎 · 옛 그룹 여전히 삶) → 결과 줄 1 = completed · 새 폴더 → 판정 원장 대조 통과 (INPUT_MISSING · `ladder:P0` 시도 [1] 채택 1) → 옛 바탕 recover = rc 0 · 고아 1 죽임 · 경고 없음 | 원장도 폴더도 고치지 않고 `--out` 만 바꿔 같은 항목을 다시 굴린다 (또는 env 가 같은 다른 기계에서). 결과 본 첫 런이 조용히 사라진다. Codex ② "결과 줄 = 그룹 종료 확인 뒤" 도 비켜 간다. 6 회차 PC6-09 는 판정이 남은 폴더를 잡았는데 (폴더를 옮겨야 통과), 이 꼴은 그 단계 없이 통과한다. 문서 명령은 대상마다 `--out` 이 고정이라 운영자 이탈이 필요하다. 재실행 항목 꼴 (미실행 · 코드 읽기): 새 바탕엔 원천이 없어 RESUME_NOT_ALLOWED → 결과 뒤였던 시도에 rejected · 결과 전 결과 줄이 써진다 (R6 꼴) | ① attempt_open 이 런 전에 원장에 시작 줄 (n · 바탕 절대 경로 · host_ident · boot) 을 커밋하고, 결과 줄 없는 같은 n 의 두 번째 입구는 화면만 (recover 먼저) ② recover_ledger: 결과 줄이 있는데 이 폴더 ≠ 결과 줄의 폴더 · 요약 sha 이면 rc 3 + 사유 ③ 못 고치면 요청서 한정 |
| **PC7-02** | **P2** · PC6-12 닫힘 주장 | `found_attempts_problem` :3825–3827 (attempt.json 없음 · 꼴 틀림 = `continue`) · PD12u 가 이 너그러움을 설계로 단언 | `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_real.py <tmp> A` → 6 회차 R10 (끝 두 커밋 reset + 항목 1 대상만 FIBRE) 위에서: a0 (손 없음) = 판정 · 예측 모두 MISMATCH (고침 동작) / **a1 `rm attempt_1/attempt.json`** · **a2 attempt.json 에 칸 하나 (`"note"`)** = 판정 원장 대조 통과 (시도 [2] 채택) · 예측 입력 통과 (러너 24 회 · completed) / a3 같은 바탕에서 `attempt_1.old` 로 이름 바꿈 = 같음 (Q-D 꼴). 단위 U7: attempt.json 이 심볼릭 링크여도 건너뜀 | 등록 ⑦ "찾은 시도 폴더 전부 … ↔ 원장 항목" 은 거짓이다. 파일 하나만 지워도 PC6-12 닫힘을 비켜 간다. ① 이 내보낸 "폴더 증거까지 맞춰 고친 손" 보다 작은 손이다. 다만 "시도 폴더 쓰기 권한 = 운영 규칙" 우산 안이라 P1 은 아니다 | 원장 항목이 있는 `attempt_<n>` 폴더에 꼴 맞는 attempt.json 이 없으면 MISMATCH. 예외는 그 항목 결과 줄 = rejected · 폴더 = `attempt_<n>.rejected.json` 일 때만 (AL07 남의 폴더). 변이 K09 (엄격) 는 PD12 · PC01 · PC12 · PC13 · AL07 · AL12 · UM · GR 52 중 **PD12u 하나만** 깬다 (설계 단언) → 싸다. a3 는 한정 (바탕 안 `attempt_*` 꼴 밖 이름 = 경고만이라도) |
| **PC7-03** | **P2** · PC6-13 "자리 전수" | `orphan_cause` :3713–3714 (chain_end 는 원인 None + 실패 rc 만 봄) · `recover_group` :6469–6472 (chain_end 에 원인 exception 을 남기지만 쓰지 않음) | `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_real.py <tmp> B` (구동기 = PD13 꼴 group_settle 미확인) → 러너 기다림 중 SIGINT · 그룹 **미확인** → 끝 기록 by chain {exception · −9 · False} · 요약 없음 → recover → 결과 줄 interrupted · post · **parent_dead · True** → `--add --resume 1` **rc 0** / 대조 b_conf (그룹 확인) → **chain_exception · False** → rc 3. 단위 U2 도 같음 | 같은 사건이 그룹 확인 여부만으로 재실행 자격이 갈린다. 등록 ⑥ "기다림 중 사슬 예외 = chain_exception (재실행 불가)" 은 미확인 → recover 길에서 거짓이고, 보고의 "자리 전수 ①–⑤" 에 이 자리가 없다. 현실의 계기 = 전경 Ctrl-C (백그라운드 실행은 SIGINT 무시) → 빈도 낮음. SIGINT 의 뜻 자체는 PC6-03 (열림) 과 겹친다 | recover 길에서 chain_end 원인 exception 이면 chain_exception (by chain 길과 같게). PC6-03 결정과 묶어 두 길을 맞춘다 |
| PC7-04 | P3 · 묵은 · 다른 판 기록 | `recover_group` :6469–6470 (표지 · 이름 대조 없음) | `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_unit.py <tmp> U6` → 끝 기록 표지 `eee…` ≠ 시작 기록 표지 → chain_end (rc 0) 를 그대로 옮김 → parent_dead | 손 고침 · 부분 복사 때만 생긴다. 다른 런의 rc 가 원인을 정할 수 있다 | prev 의 token · name 이 시작 기록과 같을 때만 chain_end |
| PC7-05 | P3 · 문구 | 등록 R ⑫ · ⑦ PC6-13 "정리 중 신호 = 런 기록 rc None = group_unconfirmed 그대로" | `probe7_unit.py <tmp> U8` → 요약 있는 길 = group_unconfirmed · True / 요약 없는 길 (디스크 끝 기록 원인 None · rc 1 · 미확인 → chain_end) = **runner_rc · False** | 보수 쪽이다. 고침 보고의 "닫지 않는 것" 에는 있고 등록 R 에는 없다 | 등록 ⑦ 에 한 줄 (요약 없는 길은 정리 중 신호를 못 가른다) |
| PC7-06 | P3 · 시험 공백 (변이 생존) | `_run_kin` :2439–2440 · :2448–2449 · `recover_group` :6491 · PC6-09 `mine` :3397 | 변이 §3: K01 · K02 · K05 생존 (보수 쪽) · K07 · K08 생존 (PD09b 는 시작 커밋 · 대상만 바꿈). U1: ppid 칸을 못 읽으면 (a None) 셈 밖. 설명문은 "계보를 끝까지 못 봄 = 보수" 라고 한다 (합성 · 실제 /proc 은 늘 ppid 가 있다) | hidepid=2 주장 ("숨은 조상 = 없어진 것") · 세션 번호 다시 쓰임 recover · PC6-09 의 기계 · 재실행 원 시도 칸을 시험이 묶지 않는다 | 가짜 /proc 행 셋 (부모 없음 · 부모 칸 없음 · recover 세션 다시 쓰임) + PD09b 에 machine · resume_of 꼴 |
| PC7-07 | P3 · 쓰기 창 | `attempt_open` :3389 (mkdir) → :3412 (attempt.json) 사이 | `probe7_unit.py <tmp> U4` → 빈 attempt_1 에서 같은 `--attempt` → 옆 거부 (rejected · pre) → 새 시도 뒤 판정 = "원장에 없는 시도 폴더 ['attempt_1']" (손 정리 전까지) | 거짓 수용은 없다 (보수). 창은 드물다 | 빈 폴더 = 이 항목 것으로 (화면만 + recover = interrupted · pre) 또는 빈 폴더 지우기 |

**검사했지만 지적 아님**
- U3: runner_rc_failed 값 표가 설명문과 같다.
- U5: "앞선 OOM 폴백 문구 + 뒤 traceback = resource" 꼴은 생기지 않는다. 러너가 기본 `--step3-require-gpu` 를 주기 때문이다 (`scripts/sdcp_gain_vox015_8arm.sh:272`).
- 러너 · payload 원문에는 CUDA 표지 · 자원 낱말이 없다. payload 는 cupyx cuSPARSE · cuBLAS 를 쓰며, 둘 다 표지에 들어 있다.
- U1 d: 부모 stat 오류는 주 루프가 부모 자신을 확인 불가로 센다 → N01l "결정 동등" 에 동의한다.

## 2. 숫자 · 전칭 대조 (`docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/logs/claims_check.out` · 내 시험 실행)

| 주장 | 자리 | 판정 |
|---|---|---|
| 본 가지 커밋 9 (`483cf413e`…`8bf1fd6ad`) · 5 (`c738a6826`…`2c1a06c57`) 있음 · cherry-pick -x · 기준 `d6e8d1b44` · `e12756051` | 두 보고 | 맞음 (7d6 = 형제 가지 · 대상 파일 diff 0) |
| 바뀐 코드 = 사슬 · 시험 둘 · 봉인 S0 7 · CODE_FILES 32 와 겹침 ∅ | PC6_FIX | 맞음 |
| 줄 번호 14 개 (db2e1b2b4) · 11 개 (4499f3ffd) | 두 보고 | 맞음 (25/25) · 4499 판 사슬 = HEAD 사슬과 바이트 같음 |
| 고치기 전 0/4 → 98/98 · 0/4 → 11/11 · 415/415 → 421/421 · 끝-끝 40/40 · PD 14/14 (3.11) · Y13,PD 15/15 (3.8) · 3.8 PD,PC 34/35 → 고침 · 사본 420/421 (Y13) | PC6_FIX | 로그 글과 맞음 (실행 판은 로그로 못 봄 · 시험 수는 판마다 맞음: 428 − 7 = 421 · 421 − 6 = 415) |
| 변이 49 = 47 + N01l · N12d 생존 · a3 9 중 8 생존 · 10-28 의 32 = 29 + 3 ERROR | PC6_FIX | 맞음 (JSON) |
| 새 7 고치기 전 0/7 → 7/7 · 전체 428/428 · 끝-끝 40/40 · 3.8 PD,PC 42/42 · 변이 19/19 · BASE 7/7 | PC6_13 | 맞음 (로그) + 내 실행 428/428 · 40/0 |
| 웹앱 grep 7 낱말 = 0 건 | PC6_13 | 맞음 |
| check_doc_refs · check_review_findings rc 0 · ban-sweep | PC6_13 | 잴 수 없음 (미실행 · 메인 게이트 몫) |
| PC6-12 "찾은 시도 폴더 attempt.json ↔ 원장 · 넷이 같은 함수" | 보고 · 등록 ⑦ | 호출 넷 = 맞음 · **"찾은 폴더 전부" = 다름** (PC7-02) |
| PC6-09 "같은 --attempt 재입력 = 화면만" | 보고 · 등록 ⑦ | 같은 `--out` = 맞음 · **다른 `--out` = 처음부터 다시** (PC7-01) |
| PC6-01 세션 · 계보 · 깊이 64 · 부모 stat 못 읽음 = 확인 불가 · 찾은 원 죽임 · runner_start · unsure | 보고 · 등록 ⑦ | 코드 · PD01 · PD01r 과 맞음 (hidepid=2 · ppid 없음 가지는 시험 밖 = PC7-06) |
| PC6-13 "GROUP_UNCONFIRMED 가 원인 · 자격을 정하는 자리 전수 ①–⑤" | PC6_13 | **다름** (chain_end 원인 exception 자리 · PC7-03) |
| 등록 ⑥ "기다림 중 사슬 예외 = chain_exception" | 등록 R | **미확인 → recover 길에서 다름** (PC7-03) |
| 등록 ⑦ PC6-13 "정리 중 신호 = group_unconfirmed 그대로" | 등록 R | 요약 있는 길 = 맞음 · 요약 없는 길 = 다름 (PC7-05) |
| 등록 ② "한 함수를 모든 길이 부른다" · 머리 시험 이름 16 | 등록 R | 맞음 |

## 3. 변이 (독립 · `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/mutate_pc7.py` · 사본 트리 · BASE 63/63)

| 변이 | 바꾼 가드 | 결과 | 판정 |
|---|---|---|---|
| K01 | `_run_kin` 부모 없음 → 확인 불가 | 생존 | 보수 쪽 공백 (hidepid=2 주장 시험 없음) |
| K02 | ppid 없음 → 확인 불가 | 생존 | 보수 쪽 공백 (합성 전용) |
| K03 | 계보 고리 대조 뺌 | 생존 | 결정 동등 (깊이 상한이 같은 답) |
| K04 | a == me → 확인 불가 | 잡힘 PD01r (run · recover 뒤집힘) | 옳은 이유 |
| K05 | recover 가 runner_start 무시 | 생존 | 보수 쪽 공백 |
| K06 | scan 의 GROUP_SCAN.pop 뺌 | 생존 | 생산에서 결정 동등 |
| K07 · K08 | PC6-09 mine 의 기계 · 재실행 원 시도 칸 하나씩 뺌 | 생존 | 시험 공백 |
| K09 | (정보) attempt.json 없는 찾은 폴더 = 사유 | PD12u 만 실패 (52 중) | 고침 방향이 싸다 (PC7-02) |
| K10 · K11 · K12 · K13 | chain_end rc 칸 · words_keep 바꿈 · 꼴 틀린 rc · 멈춤 문장 rc | 잡힘 (PD13g · PD13d / PD13 · PD13r / PD13 / PD13r) | 옳은 이유 |
| K14 | 표지 `CUDA error:` 뺌 | 잡힘 PD02c (길 행 18 개 · 표만이 아님) | 옳은 이유 |

이전 회차 변이 49 · 19 · 32 는 다시 돌리지 않았다 (로그 · JSON 대조만).

## 4. 요청서 맨 위 초안 — "이번에 닫는 것 / 닫지 않는 것" (Codex 회차 ②)

**이번에 닫는 것** (PC7 처리에 따라 줄을 고친다)
- PC6-01: 같은 실 uid 무관 프로세스 = 러너 세션 · 계보 밖이면 셈 밖. 세션 · 계보 안 = 확인 불가. 확인 불가여도 찾은 표지 프로세스는 죽인다 (PD01 · PD01r).
- PC6-02: CUDA 표지 = 모든 길 · 라이브러리 상태 문자열 · 차례 = 잘못된 주소 → 자원 → 표지 (PD02 · PD02r · PD02c · PD02cr).
- PC6-09: **같은 `--out`** 에서 같은 `--attempt` 재입력 = 화면만 (PD09 · PD09b).
- PC6-12: **꼴 맞는 attempt.json 이 있는** 찾은 시도 폴더 ↔ 원장 항목 · 호출자 넷 (PD12 · PD12m · PD12u).
- PC6-13: 그룹 미확인 + 러너 실패 rc = 러너 rc 길 낱말 규칙. recover 의 chain_end (원인 None + 실패 rc) (PD13 · PD13o · PD13g · PD13r · PD13d).
- PC6-11 일부: M2e · M2c · M9 · M8 · M11 · M12 · M15 시험.

**닫지 않는 것**
- PC7-01: 부모 사망 뒤 **다른 `--out` · 다른 기계** 의 같은 `--attempt` = 처음부터 다시 · 판정 통과 (원장에 시작 기록이 없다) — 운영 규칙 "recover 먼저 · 같은 `--out`".
- PC7-02: attempt.json 없는 · 꼴 틀린 · 링크 찾은 폴더 = 건너뜀 (R10 + 파일 하나 = 통과).
- PC7-03: 기다림 중 사슬 예외 + 그룹 미확인 → recover = parent_dead (재실행 받음) — PC6-03 과 함께 결정.
- PC6-01 한정: hidepid=1 = 늘 미확인 · hidepid=2 숨은 조상 = 없어진 것 · setsid + 부모 끝남 + environ 못 읽음 = 놓침 · 세션 안 확인 불가 = 곧바로 미확인 · kgy 실제 (3.8.10 · 비 root · ssh · /proc 옵션) · 실제 GPU D 상태 = 미확인.
- PC6-02 한정: 부분 문자열 · 대소문자 그대로 · 자원 낱말 없는 메모리 실패 꼴 = runner_rc (SELF-147 · 1저자 Q1 열림) · 커널 OOM killer (rc −9 / 137 · 로그 낱말 없음) = runner_rc.
- PC6-13 한정: 사슬이 끝 기록 전에 죽은 런 = parent_dead · 정리 중 신호 두 길 차이 (PC7-05) · chain_end 표지 대조 없음 (PC7-04) · 옛 판 결과 줄 다시 셈 차이.
- 시험 공백: PC6-11 남은 M4 · M5 · M6 · M10a · M10b + 이 회차 K01 · K02 · K05 · K07 · K08 (PC7-06).
- 열린 P3: PC6-03 · 04 · 05 · 06 · 08 · 10 · PC7-04 · 05 · 07.
- Q-D: 원장 밖 그림자 런 · 모든 사본을 함께 고친 손 · 바탕 밖으로 옮기거나 이름을 바꾼 폴더.
- 환경: 이 컨테이너 3.11.17 · root 만. kgy 3.8 판 · 게이트 = 메인.

## 5. 미확인 · 다시 돌리기

**미실행:** kgy 3.8 판 · check_doc_refs · check_review_findings · ban-sweep · PC7-01 재실행 항목 꼴 (코드 읽기) · 실제 GPU · sshd · hidepid · 이전 회차 변이 다시 돌림.

**탐침:** `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_real.py` (A · B · C) · `probe7_unit.py` (U1–U8) · `mutate_pc7.py` · `claims_check.py`.
- `probe7_unit.out` = U1–U7 (그 뒤 U8 함수만 덧붙임 · `probe7_unit_U8.out`).
- `probe7_real` 의 A · B 를 돌린 뒤 C 함수만 덧붙였다.

**diff 다시 보기:** `git diff d6e8d1b44 0658c0ac6 -- scripts/rint_r_chain.py scripts/test_rint_r_chain.py docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`
