# codepkg 진행 메모 (재시작 대비)

- 11-12 시작.  트리 = scratchpad/rint/codepkg/tree (detached 11a794674 · 깨끗).  본 리포 쓰기 금지.
- 차례: design.md → 시험 먼저 커밋 → 구현 커밋 → 기존 시험 (3.11 + kgy) → 변이 → GPU 블록 초안 · 개정 초안.
- cupy 12.3.0 소스 (github raw · 데이터만 · codepkg/cupy_src_v1230/): cg = _iterative.py 14 (tol= 만 · rtol= 없음 → TypeError) · _make_system 301–349 (M: csr 이면 fast spMV · 아니면 aslinearoperator) · dia → MatrixLinearOperator → _matvec 기본 = matmat(x.reshape(-1,1)) → A.dot → __mul__ = tocsr() (= tocsc().tocsr() · _dia.py 178–190 · 매 적용마다 변환) → 75 % 원인 확인.  C 꼴 = _CustomLinearOperator · dtype 주면 탐침 호출 없음 (_init_dtype).  cg 루프 iter0 `p = z` (별칭) → matvec 은 새 배열을 내야 한다 (제자리 버퍼 금지 · 변이 후보).
- 주의: dia→csc 가 data==0 을 버림 (마스크) · CSR 합은 +0 에서 시작할 수 있어 r=-0 자리에서 부호 있는 0 만 다를 수 있다 (값 같음 · 바이트 다름 가능) → 시험 · GPU 블록에서 바이트 / 값 따로 센다.
- design.md 작성 (11-12).  핵심 결정: Q11 = GPU 길만 · 'jacobi' 그대로 · 새 키 없음.  Q2 = 새 모듈 scripts/cjunc_store.py · npz+skeleton JSON · 엄격 지문 · os.link 단일 작성자 · 팔 JSON 무변경 (ResumeRunner 바이트 대조 때문) · 옆 파일 cjstore_<팔 JSON> · 사슬 --cjunc-store (ladder·predict) · RunnerGraphSource 금지 3 겹 · CLI 회계 mode · CODE_FILES += cjunc_store.py · S0 단계 1 다시 필요 (step3_sigma · payload 둘 다 일곱 파일).
- 다음: 시험 먼저 — scripts/test_step3_gpu_precond.py (가짜 cupy) + scripts/test_cjunc_store.py (저장본) + e2e 켬/끔 (E19 꼴) → 고치기 전 실패 확인 → 시험 커밋.
- (11-12 04:4x) 워커 재시작 — 파일 다 남음 · 기준 e2e (3.11) 는 죽음 (logs/base/e2e_py311.log 부분) · 다음 = Q11 시험을 고치기 전 판에서 한 번 돌려 실패 확인 → 저장본 시험 작성.
- (11-12 05:xx) 시험 먼저 작성: scripts/test_step3_gpu_precond.py (Q11 · 13 검사) · scripts/test_cjunc_store.py (T0–T11 · P · R · C = 21 검사) · scripts/test_cjunc_store_e2e.py (Z0–Z6).  고치기 전 판: Q11 10/13 (실패 3 = G1 · G1r · G2 — M 이 dia_matrix) · store 0/21 (모듈 없음 · payload/러너/사슬이 선택지를 모름 · 봉인 원천이 env 를 그대로 넘김) · e2e Z0 실패 (사슬 선택지 없음).  로그 = logs/before/.
- 설계 바뀜: 저장본 결과 = 화면 한 줄만 (옆 파일 없음) · 요약 cjunc_store True (켬일 때만) · design.md 기록 줄 고침.
- (11-12) 시험 먼저 커밋 = 71b0d145f (트리 · push 없음).
- (11-12 05:3x) 구현 (아직 커밋 전 · 트리 작업 중): step3_sigma GPU 길 LinearOperator (Q11 시험 15/15) · 새 scripts/cjunc_store.py · ca_ext_cjunc store= (+ 모듈 상단 import cjunc_store — 아래 발견) · payload --step3-cjunc-store (입구 STORE_PATH · STORE_GRAPH_ONLY · 멈춤 S2_CJUNC_STORE|INCONSISTENT|) · run_contract CLI_ACCOUNTING mode · 러너 CJUNC_STORE (ABORT 여섯) · 사슬 --cjunc-store (ladder · predict · 합치기 아님) · Runner env · RunnerGraphSource pop · CODE_FILES 20 (+ test_rint_r_chain D10 · D14 핀 19→20) · _RUNNER_AXES.
- ★ 발견 (P2 가 잡음): 매니페스트 exec_env (loaded_project_modules · project_module_digest = 로드된 프로젝트 모듈 내용 해시) 가 저장본 켬 런에서만 cjunc_store 를 세어 팔 JSON 바이트가 끔과 갈렸다 → ca_ext_cjunc 상단에서 cjunc_store 를 늘 부른다 (접합 런마다 같은 모듈 집합) → 끔 = 켬 바이트 같음.  store 시험 34/34 (3.11).
- 기존 시험 묶음 (3.11) 백그라운드 = logs/after/py311/_summary.txt (트리 고치지 말 것 — 도는 중).
- (11-12 05:4x) 3.11 묶음 중간: run_contract 124/124 · cmd_selftest 128/128 · s3 selftest · rint · cmd_repo 0 오류 · carbon_junction 547/547 · gpu_precond 15/15 · cjunc_store 34/34 · ca_ext_b6 502/0.
- ★ probe6 시험 R2a 실패 (317/318) = 그 시험의 cupy 대역 (`fakemods/cupyx/scipy/sparse/linalg`) 에 LinearOperator 가 없어 새 GPU 길이 ImportError → REQUIRE_GPU 멈춤 → 대역에 scipy LinearOperator 를 더함 (test_probe6_read.py 2101 줄).  같은 부류 = webapp/test_pipeline_provenance.py 59e 의 가짜 cupyx (돌리기 전 고침).  다시 돌릴 것: probe6 · webapp provenance.
- T12 (발행 전 대조) 를 시험 파일에 더함 (구현 커밋에서) · e2e Z4 = 판정 표지 SV_UNCHECKED 없음 + 원천 런 ok 로 (ARM_PUBLIC 에 sv_graph 없음).
- 변이 25 개 준비 = work/mutate.py (묶음 끝난 뒤 git worktree 사본에서).  cjunc_store.py 의 안 쓰는 import io = 묶음 끝난 뒤 지움 (동작 무관).
- GPU 확인 블록 = gpu_check_block.txt (자리표 Q11REPO · Q11PIN · 새 sha256 = 구현 커밋 뒤 다시 확인) · 하네스 gpu_check/q11_gpu_check.py · 개정 초안 = amend_drafts.md.
- (11-12 06:4x) 3.11 묶음 끝 (logs/after/py311/_summary.txt): run_contract 124/124 · cmd_selftest 128/128 · s3 selftest · s3 rint · cmd_repo 0 오류 · probe6 317/318 (대역 고침 전) · carbon_junction 547/547 · gpu_precond 15/15 · cjunc_store 34/34 · ca_ext_b6 502 · ca_ext_runner 151 · ca_ext_verdict 31 · ca_ext_z1 95 · ca_ext_z3 84 · rint_r_chain 506/506 (540 s) · e2e 51/51 (1043 s) · e2e12 33/33 (463 s) · conv_cert 30/30 (175 s) · cjunc_store_e2e 6/6 (692 s · 끔 · 켬 길 각 ~307 s · 팔 91 바이트 같음 · 단위 3 · 저장본 11 파일).
- io import 지움 (동작 무관) · 덧 묶음 (3.11) 백그라운드 = logs/after/py311_extra (undef · gpu_precond · cjunc_store 35 · probe6 다시 · webapp provenance · ptfe_fa · target_cert · s0_census).

## 대피 세션 이어받기 (11-12 07:2x UTC · 작업 트리 /home/user/rint-codepkg · 시험 먼저 ebb0e9f80 · 구현 = 커밋 전)
- (07:2x) 지시서 둘 · design · notes · amend · gpu 블록 읽음.  상태: 추적 12 수정 + 새 scripts/cjunc_store.py (scratch 사본과 바이트 같음).  기록 자리 = logs/evac/ · 임시 = tmp/ (TMPDIR) · 사본 = work/.
- 차례: ① 고치기 전 판 실패 확인 (ebb0e9f80 scripts 를 work/before 에 꺼내) → ② 구현 살핌 · 마무리 → 구현 커밋 → ③ 3.11 → kgy 묶음 → ④ 변이 → ⑤ GPU 블록 자리표 · 개정 초안.
- (07:3x) ① 고치기 전 판 (ebb0e9f80 의 scripts + probe6_read.py + 사전등록 문서 한 장 → work/before · 3.11): Q11 10/13 (실패 G1 · G1r · G2 = M 이 dia_matrix) · store 0/21 (T0–T11 = 모듈 없음 · P1 · P2 = payload 가 선택지 모름 (argparse) · R1 · R2 = 옛 env 게이트 "읽지 않는 축" (끔 런 r0 은 rc 0) · C1–C5) · e2e Z0 실패.  기록 = logs/evac/before/.  ⚠ 첫 두 번은 내 실수 (GIT_DIR 을 env 로 줌 → 러너 관문이 딴 길 · 사전등록 문서 없음) — 무효 표지 로그로 남김.  GIT_DIR env 는 Q11 시험 (git show) 에만 쓴다.
