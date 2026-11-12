# Rint ② 코드 묶음 지시서 — 탄소 접합 준비 재사용 (Q2) + GPU 전처리 C 꼴 (Q11) · 시험 먼저

(본 세션 · 11-12 · 1저자 비준 = 11-12 *"나머지는 권고대로"* · *"ㅇㅇ 권고대로해"* · 결정 기록 = 본 리포 `docs/reviews/rint2_time_reestimate_20261111/README.md` 끝 쪽 "1저자 결정 (11-12)" 절 — 작업 트리에는 아직 없을 수 있다 · 본 리포 사본을 읽기만 한다)

## 0. 왜 · 목표

- Rint ② R 런은 GPU 팔이 **12 월 초까지 확실히** 끝나야 한다.  ⑥ 실측 (SBE 팔 한 점) = 팔 22,345 s = 준비 4,567 s (그 가운데 탄소 접합 준비 4,040 s) + 풀이 · 증서 17,748 s (CG 362,370 반복 × 약 0.048 s).
- 이 묶음이 하는 일 둘 (**한 묶음** · 1저자 Q11):
  - (가) **Q11 GPU 전처리 C 꼴** — `scripts/step3_sigma.py` `_solve_cg` 의 GPU 길 (565–582 줄 근처) 이 Jacobi 전처리를 `cupyx.scipy.sparse.diags(1.0 / diag)` (dia_matrix) 로 넘긴다.  합성 벤치 (1저자 11-12 · kgy RTX 3090 두 번 · gabia A6000 한 번) 에서 같은 수를 벡터 곱 연산자 `LinearOperator(shape, matvec=lambda r: dinv * r, dtype=float64)` (dinv = `1.0 / cupy.asarray(diag)`) 로 넘기면 반복당 3.40–3.79 배 빠르고 200 반복 뒤 해가 비트까지 같았다 (반복 시간의 약 75 % 가 dia 전처리 적용).  결과 · 블록 = 본 리포 `docs/reviews/rint2_time_reestimate_20261111/bench/` (results_20261112 는 아직 커밋 전일 수 있다 — 본 세션 scratch 사본 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint/gpu_bench_results_20261112.md` · 벤치 스크립트 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint/bench_raw/gabia/gpu_bench_cg.py` 302–306 줄).  전처리 종류 (Jacobi) · 수 · 정지 규칙은 그대로 — **표현만** 바꾼다.
  - (나) **Q2 탄소 접합 준비 재사용** — 탄소 접합 원장 (기하) 은 R_j · 법칙 · c 에 달리지 않는다 → 같은 침대 · 격자 · origin · 문턱이면 같은 원장이다.  지금은 팔마다 새 프로세스가 다시 만든다 (저장 · 읽기 코드 없음).  한 번 만들어 저장하고 다음 팔 · 봉인 원천 (조립만) 런이 **지문을 대조해** 읽게 한다.  계획 (R_j · 법칙 · c 에 달림) 은 팔마다 그대로 다시 만든다.
- 근거 표 = 본 리포 `docs/reviews/rint2_time_reestimate_20261111/README.md` 의 A-2 (탄소 접합 준비가 무엇에 달렸나) · E-2 의 4 번 (재사용 · 더 드는 일 ①–④ · S0 단계 1 다시 조건) · E-2 의 8 번 (전처리 꼴) · 약칭 표의 줄 번호.

## 1. 작업 자리 · 금지

- 작업 트리 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint/codepkg/tree` (본 리포 `11a794674` 에서 detached · 이 트리에서만 읽고 쓰고 커밋한다 · push 없음 · `git -c commit.gpgsign=false commit`).  커밋 메시지 끝 두 줄:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`
- ⛔ `/home/user/Yonghoon-DEM-DFT` (본 리포) 에는 아무것도 쓰지 않는다 (읽기만 · 그 트리에서 시험 게이트가 돈다).
- ⛔ 킷 풀이 · GPU 실행 · σ 열람 없음 (이 컨테이너에는 GPU 가 없다).  개발 탐침 원장 (`docs/reviews/rint2_dev_probe_ledger_20261026.md`) 의 규칙을 건드리지 않는다 — 원장 줄 · 등록 R · 계획 문서는 **고치지 않고** 필요한 문장을 보고에 초안으로만 적는다.
- ⛔ 봉인 상수 · 증서 문턱 (`scripts/step3_conv_cert.py` 65–74 줄 등) · rtol · maxiter · 판정 규칙 · 등록 팔은 바꾸지 않는다.  AMG · 초기값 넘기기 · 준비와 풀이 겹치기 (E-2 의 5–7 번) 는 범위 밖.
- 신호를 보내는 시험 · 실험은 PID 이름공간 안에서만: `unshare -pf --mount-proc --kill-child <명령>`.  kill 에 넘기는 번호 = 직접 만든 자식 · > 1 · 자기 · 부모 아님 · pid 파일이 없으면 건너뜀 · -1 · 0 · 빈 값 · pkill · killall 금지.
- 같은 기계에서 본 리포 시험 게이트 (약 2 시간) 와 논문 조수 하나가 돈다 (CPU 4 · 메모리 15 GB · 디스크 여유 약 6 GB).  시험 · 변이는 **한 번에 프로세스 하나씩** 차례로 · 큰 임시 파일은 쓰고 지운다.
- 코드는 kgy 판 (Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy 12.3.0) 에서도 돈다 (`SELF-132` · `SELF-133` 의 부류 — 3.9+ 문법 · 새 라이브러리 함수 금지).  kgy 판 시험 = `scripts/setup_kgy_py38.sh` · `scripts/check_kgy_py38.sh` (게이트의 그 단계 · 본 리포에서 이미 만들어진 환경이 있으면 그대로 쓴다).
- 진행 메모를 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint/codepkg/notes.md` 끝에 그때그때 덧붙인다 (재시작 대비).  시험 기록은 같은 폴더 `logs/` 아래.

## 2. 먼저 읽을 것

1. 본 리포 `docs/reviews/rint2_time_reestimate_20261111/README.md` 요지 · A-1 · A-2 · E-2 (4 · 8 번) · 한정 · 결정 절.
2. 개발 탐침 원장 §2 (규칙 일곱 칸) · §3 (시도 1 · 2 · "풀이 코드 목록") — 이 묶음은 그 목록의 파일을 바꾼다 → ⑥ 다시 재기 (시도 3) 가 뒤따른다 (Q5).
3. 코드: `scripts/step3_sigma.py` `_solve_cg` · `LAST_BACKEND` 기록 자리 · `scripts/carbon_junction.py` (원장 · 계획 · 2172–2253 줄 근처 · 지문 2181 줄) · `scripts/ca_ext_cjunc.py` (배선 213–250 줄) · `scripts/mpm_webapp_payload.py` (2456–2470 · 2488 줄 근처) · `scripts/sdcp_gain_vox015_8arm.sh` (팔 차례 · env 전달) · `scripts/rint_r_chain.py` (S0 일곱 파일 지문 344–345 · 1817–1840 줄 · R 출력 자리 규칙 · 봉인 원천 런) · `scripts/step3_conv_cert.py` (ⓒ 이어 풀기 = x0 길).
4. 매니페스트 · 회계 규칙: `scripts/check_method_discipline.py` (규칙 M · J · 매니페스트 전수 훑기 — 새 매니페스트 키 · 새 CLI 옵션 · 새 env 는 분류하지 않으면 HOLD) · 해당 시험.

## 3. 해야 할 것 (차례)

### 3-1. 설계 메모 먼저 (코드 전에 · 30–80 줄)

`/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint/codepkg/design.md` — 다음을 정한다 (근거 = 줄 번호):
- (가) 바꿀 자리 · CPU 길도 바꿀지 (권고 출발점: **GPU 길만** — CPU 길은 R 에 안 쓰이고 이미 dia matvec 이 빠르다 · 바꾸면 그 까닭) · `LAST_BACKEND['precond']` 표기 ('jacobi' 유지 권고 — 봉인 · 기대값 대조가 이 글자를 보는지 먼저 확인) · 새 기록 키를 넣을지 (넣으면 매니페스트 분류 · 넣지 않으면 C 꼴을 무엇으로 증명하나) · `tol=` / `rtol=` 두 호출 길 둘 다 · x0 길 (ⓒ) · callback 길.
- (나) 재사용: 무엇을 저장하나 (원장만 · 계획은 아님) · 저장본의 결속 (입력 = 침대 파일 해시 · 격자 · origin · 문턱 · 원장 만드는 코드 판 · 무엇을 지문에 넣나) · 어디에 두나 (R 출력 자리 규칙 · 권한 · 단일 작성자) · 누가 만들고 누가 읽나 (사다리 팔 · 단위 · 봉인 원천 런) · 저장본이 없거나 · 잘렸거나 · 지문이 다르거나 · 다른 기계에서 왔을 때 (정직한 흐름 = 다시 만든다 · 손으로 고친 · 서로 어긋난 기록 = 멈춤 (fail-closed) — CLAUDE.md "재개 규칙 지적 처분 기준" 과 같은 꼴) · 읽은 원장이 새로 만든 것과 **비트 같음** 을 무엇으로 보증하나 · 고칠 자리가 S0 일곱 파일 안이면 S0 단계 1 다시 (CPU 약 1.5 h · kgy) 가 필요하다는 것을 적는다.
- (다) 등록 R · 원장 · 계획에 필요한 개정 문장 초안 (고치지 않는다 · 초안만): 새 산출물 = 저장한 원장 · 봉인 원천이 같은 저장본을 읽어도 되는지 · ⑥ 시도 3 줄 · S0 단계 1 다시 여부.
- (라) GPU 확인 블록 설계 (1저자가 kgy · gabia 에서 돌림 · 합성 계 · 킷 없음 · σ 없음): 바꾸기 전 커밋 (`11a794674`) 의 `_solve_cg` 와 바꾼 뒤 커밋의 `_solve_cg` 를 **같은 합성 SPD 계** (실측 규모 약 2,650 만 미지수 · 수렴까지 · 생산 rtol · CONV_CERT 켬 · x0 길 포함) 에서 돌려 해 · 반복 수 · info 가 비트까지 같은지 + 반복당 시간.  결과 전 기대 (같음) 를 블록 설명에 먼저 적는다.  블록 꼴 = 본 리포 `docs/reviews/rint2_time_reestimate_20261111/bench/gpu_bench_kgy_busy.txt` 와 같은 관문 (md5 · 새 폴더 · venv · 느낌표 · 탭 · CR 없음).

### 3-2. 시험 먼저 (고치기 전 코드에서 옳은 이유로 실패하는 것을 본다)

- (가) 전처리: 가짜 cupy (numpy · scipy 로 흉내 · 시험 안에서만) 로 `_solve_cg` GPU 길을 돌려 — 넘긴 M 이 벡터 곱 연산자인지 (고치기 전 = dia_matrix 라 실패) · A 꼴 (고치기 전 코드) 과 C 꼴의 해 · 반복 수 · info 가 비트 같은지 (CPU scipy 에서 · 수렴까지 · x0 있음 / 없음 · tol / rtol 두 호출 길) · `LAST_BACKEND` · `LAST_CG` 기록이 그대로인지 · 매니페스트 키 변화 0 (또는 분류됨).
- (나) 재사용: 같은 입력 → 저장본을 읽은 원장 = 새로 만든 원장 (비트 · 지문) · 계획 · 조립 행렬 · 풀이 결과 (작은 픽스처 · CPU) 가 재사용 끔과 비트 같음 · 저장본 없음 · 0 바이트 · 잘림 · 한 바이트 바뀜 · 지문 다름 · 다른 침대 / 격자 / origin / 문턱의 저장본 · 다른 코드 판의 저장본 · 읽는 도중 끊김 · 두 팔이 같은 자리에 동시에 씀 → 각각 기대 동작 (다시 만든다 / 멈춘다 · 사유 기록) · 사슬의 S0 · 단위 · 합치기 · 판정 · 다시 판정 길 (기존 끝-끝 시험 `scripts/test_rint_r_chain_e2e.py` · `scripts/test_rint_r_chain_e2e12.py` 의 꼴) 에서 재사용 켬 / 끔 결과가 같음.
- 항목마다 고치기 전 판에서 실패 수 → 고친 뒤 통과 수를 적는다.

### 3-3. 고친다 · 기존 시험 전부 · 변이

- 고친 뒤 관련 기존 시험 전부 (step3 · carbon_junction · ca_ext_* · rint_r_chain (+e2e · e2e12) · step3_conv_cert · probe6 · 규율 검사 `scripts/check_method_discipline.py`) 를 Python 3.11 + kgy 판에서 차례로 → 통과 수 · 걸린 시간.
- 새 규칙 (지문 대조 · 저장본 거부 · C 꼴) 마다 변이를 하나 이상 넣어 시험이 잡는지 본다 (사본에서 · 이전 판 변이 도구 꼴 참고).
- 커밋 = 시험 먼저 커밋 하나 → 구현 커밋 하나 (이 트리 · push 없음).  고치지 않은 것 · 미확인은 보고에 적는다.

## 4. 끝내는 것 (이 조수의 범위)

설계 메모 · 시험 먼저 커밋 · 구현 커밋 · GPU 확인 블록 초안 (파일 · 돌리지 않음) · 개정 문장 초안 · 진행 메모.  그 뒤 = 본 세션이 내부 반박 리뷰 (독립 조수 · Codex 아님) → 고침 → 본 리포 반입 · 게이트 → 원장 시도 3 줄 → kgy 에서 S0 단계 1 다시 (필요하면) · ⑥ 시도 3 · GPU 확인 블록 (1저자) → Codex 봉인 전 묶음 → 계획 §10 개정 → 봉인 → R.

## 5. 답장 (12 줄 안 · 한국어)

커밋 sha 둘 · 바꾼 파일 · 시험 고치기 전 → 뒤 (항목별) · 기존 시험 통과 수 · 시간 (3.11 · kgy 판) · 변이 결과 · S0 단계 1 다시 필요 여부 · 등록 · 원장 개정 초안 자리 · GPU 확인 블록 자리 · 고치지 않은 것 · 미확인.
