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
- (07:5x) 넘겨받은 구현 그대로 (3.11): Q11 15/15 · store 35/35 (31 s) — logs/evac/handover/.
- ★★ 발견 (구현 살핌 · 커밋 전 고칠 것): 넘겨받은 cjunc_store 는 **instance 가 둘 이상인 원장을 저장하지 못한다** — `carbon_junction._merge_instances` 1620–1621 줄이 `[np.zeros(0)] * nI` (같은 빈 배열 객체를 nI 번) 을 pair_i · pair_j 에 넣는다 → `_Walk._once` 가 별칭으로 보고 Unsupported → built_write_skipped (⚠ 줄 · 팔 결과는 맞음 · **저장본은 영영 안 생김**).  시험 픽스처 넷 (f1 · f1_nosdcp · rand3 · rand7) · B6 · e2e 킷이 모두 instance 1 개라 시험이 못 잡았다.  확인 = work/dbg_alias2.py (F5 · F6 = instance 2 → Unsupported).  실침대 SBE = instance 117,583 (S0 보고 docs/data/rint2_s0_sbe_20261108) → 이대로면 Q2 이득 0.
- ★ 둘째: `_no_overlap` = 배열 쌍마다 np.shares_memory (O(n²)) — 실침대 원장은 instance 마다 작은 배열 넷 (seg_i · seg_j · self_A · self_B) = 약 47 만 개 → 끝나지 않는다.  → 주소 구간 정렬 (O(n log n) · 연속 배열만 받으므로 정확) 로.
- 고칠 방향 (carbon_junction.py 는 안 바꾼다 — 원장 코드 그대로): 저장 꼴이 **별칭을 그대로 싣는다** (되가리킴 노드 'r' · 엄격 지문에도) · 겹침 검사 O(n log n) · 작은 배열 수십만 개의 zip 비용은 재 본다 (합성 꼴).  시험 먼저: instance ≥ 2 픽스처 (F5 · F6 · 자기 접합 · 긴 접촉) 왕복 · 저장 → 넘겨받은 판에서 실패 확인 뒤 고침.  T3 의 "별칭 = 거부" 두 줄은 "별칭 = 그대로 복원" 으로 바꾼다 (설계 바뀜 · design.md 에 적는다).
- (08:2x) 새 시험 (구현 커밋에 실을 것 · scripts/test_cjunc_store.py): T1 (원장 F5 · 조밀 침대 둘 + 별칭 모둠 + 고리 목록 · 별칭 서명) · T2 (별칭 ↔ 사본 지문) · T3 (별칭 두 줄 빼고 보기 겹침 · 객체 배열 겹침 더함) · T5f (instance 여럿 지어 씀 → 적중 · 계획) · T13a · b (규모) · P5 (세 가닥 직렬 payload).  넘겨받은 구현에서 돌림 = 33 PASS · 8 FAIL (T1 둘 · T2 · T3 (객체 배열 겹침을 받음) · T5f (built_write_skipped) · T13a (shares_memory 4,006,002 번 / 배열 2,002) · T13b · P5 (instance 2 · ⚠ 저장 안 함)) — logs/evac/handover/store_newtests_on_handover_impl_py311.log.  넘겨받은 파일 사본 = work/handover/ (cjunc_store.py · test · tree diff).
- (08:5x) 고침 (scripts/cjunc_store.py · 아직 커밋 전): ① 별칭 = 되가리킴 노드 'r' (지문 b'R' + 처음 만난 차례 번호 · decode 가 같은 차례로 다시 둔다 · 고리도 끝난다) ② `_no_overlap` = 주소 구간 정렬 (객체 배열도 봄) ③ `encode_strict` (한 걸음) ④ 읽기 = `_read_members` (그릇 · 못 읽음) + `_content` (내용 · 뜻밖의 오류도 어긋남 · MemoryError 만 그대로) ⑤ 쓰기 쪽 뜻밖의 예외 = built_write_failed (팔 결과 무관) ⑥ 자리 어림 멤버당 4096 → 512 B.  ca_ext_cjunc: `_thr` → `_rthr` (가림 없앰).
- 결과 (3.11): store 42/42 (51 s · T13b 배열 120,004 지문 둘 + 싣기 + 풀기 2.9 s · T13c 멤버 120,006 파일 53.8 MB 쓰기 2.5 s · 읽기 6.6 s) — logs/evac/store_py311_try2.log.  어림 (추정): 실침대 47 만 멤버 = 쓰기 약 10 s · 읽기 약 26 s + 큰 배열 해시.
- 스크래치 덮임 (커밋 안 함 · work/cov_registry_roundtrip.py): test_carbon_junction 이 짓는 원장 488 개 (instance ≥ 2 = 109 · 자기 접합 60 · 미실현 67 · 거부 사유 18 · 고리 9 · 최대 instance 19) 전부 왕복 같음 (받지 않는 꼴 0 · 차이 0) · 그 시험 547/547 (67 s) — logs/evac/cov_registry_roundtrip_py311.log.
- (09:4x) 시험 더함 (T5g · h · T6b · T7 둘 + T7b · T11 둘 · C1 일곱 · R1 일곱 · P1 있는 상대 폴더) · 변이 도구 work/mutate.py (84 개 · 사본 work/mut · 한 번에 하나) 1 차 = 잡힘 81 · 안 잡힘 3 (R6 = testzip 건너뜀 — 작은 멤버는 첫 읽기에 CRC 가 걸려 못 가름 → T6b (큰 멤버 npy 머리) 더해 잡게 함 · W6b · P5 = 겹 방어) · N3b 는 잡힘 (개행은 grep 겹이 못 봄 = case 겹이 필수) → 기대 고침 + N3c · W2b 더함 (86 개).  기록 logs/evac/mut/run_py311.log (1 차 · 시험 고치기 전).
- ★ (09:5x) 구현 커밋 = f17ea8c6b (작업 트리 · push 없음 · 서명 없음 · 13 파일).  커밋 직전 3.11: Q11 15/15 · store 46/46 (52 s).
- 다음: 3.11 묶음 A (빠른 것들) → B (사슬 · e2e · 증서 · store e2e) → kgy 판 → 변이 다시 (끝 판) → GPU 블록 자리표 · 개정 초안.  묶음 기록 = logs/evac/py311_A · py311_B · kgy_A · kgy_B (_summary.txt).
- (대피 2 · 08:25Z) 3.11 묶음 A (HEAD f17ea8c6b · 작업 트리 깨끗) = 27 묶음 가운데 26 rc 0 · 1 rc 1:
  run_contract 124/124 (1 s) · cmd selftest 128/128 (90 s) · s3 selftest PASS · s3 rint PASS · cmd repo 0 오류 (37 s) · probe6 330/330 (216 s) ·
  carbon_junction 547/547 (61 s) · gpu_precond 15/15 (1 s) · cjunc_store 46/46 (55 s) · ca_ext_b6 502 (41 s) · ca_ext_runner 151 (143 s) ·
  ca_ext_verdict 31 (39 s) · z1 95 (32 s) · z3 84 (26 s) · ptfe_fa 242 (63 s) · target_cert 264/264 빠른 판 (27 s) · s0_census 186 (13 s) ·
  webapp provenance 284/284 (12 s) · rint_receipts 105 (65 s) · g2_am_iface 136 (5 s) · first_result 9/9 · webapp ca_ext_labels 93 · rint_scope 31 ·
  je_label 22 · temp_pressure ALL PASS · net_current ALL PASS · mpm_lab_cmp 23/23.
  rc 1 = undef (scripts/check_undefined_names.py 전체 훑기) 2 건 = scripts/generate_comparison_plots.py 6905 · 6906 (log_vuln · log_phi_logcn) —
  이 묶음이 손대지 않은 파일 (git diff af3cce37b HEAD 에 없음) · pyflakes 판 (스크래치 lintenv) 으로는 3 건 (+ viz_mixer_bed.py:90 npart) · 셋 다
  바꾼 · 새 파일 아님 · scripts/check_all.sh 에 이 검사 단계 없음 (grep 0 줄).  기록 logs/evac/py311_A/_summary.txt.
- GPU 블록 머리 자리표 채움 (Q11PIN = f17ea8c6b… · Q11REPO = $HOME/dem-mt (근거 KGY_BLOCK.md BASE 줄 · gabia 미확인)) · amend_drafts.md 2 판 씀.
- 다음: 3.11 묶음 B (사슬 · e2e · e2e12 · 증서 · store e2e) 백그라운드.
- (08:28Z) 묶음 B 를 nohup 으로 잘못 띄움 (SIGHUP 무시가 자식에 상속) → 몇 초 뒤 멈춤 · 남은 프로세스 0 확인 · 기록 폴더 py311_B_nohup_stopped_invalid (쓰지 않는다) · nohup 없이 다시 띄움.
- (대피 3 · 08:36Z · 사용량 한도로 한 번 끊김 → 본 세션 지시로 이어감) 상태 확인: 작업 트리 깨끗 · HEAD f17ea8c6b · 내 프로세스 = 묶음 B (run_bundle.sh pid 2415 —
  살아 있다 · rint_r_chain 506/506 390 s 끝 · rint_r_chain_e2e 도는 중) · 다른 check_all.sh · check_kgy_py38.sh = 본 트리 게이트 (본 세션 것 · 건드리지 않음).
  변이 도구에 끝-끝 변이 셋 (Z1 요약 칸 · Z2 ladder 배선 · Z3 predict 배선 · --e2e 일 때만) 더함 = 89 개 · 옛 글 자리 89/89 한 번씩 (사본 work/mut = 구현 커밋과 같음).
  남은 차례: B 끝 → 변이 (86 · 3.11) → kgy 판 묶음 → 끔 길 ↔ 바탕 커밋 산출 대조 (본 세션 지시 "기본 끔 경로 비트 같음") → 끝-끝 변이 셋 → GPU 하네스 CPU 흐름 확인 → 보고.
- (대피 4 · 08:41Z · 새 조수가 이어받음) 상태: 작업 트리 깨끗 · HEAD f17ea8c6b · 묶음 B (py311_B) 는 E14 FAIL (cause=signal · 08:37:41Z · 앞 조수 정지와 같은 때 = 끊김 산물로 봄) 뒤 E15 에서 시험 프로세스가 죽음 (run_bundle.sh · 시험 둘 다 없음) ·
  E15 의 따로 세션 사슬 (e15_stage_driver · pid 22969 · 부모 1) 만 고아로 남아 사다리를 끝까지 돈다 (내가 만든 자식 아님 → kill 하지 않고 끝나기를 기다린다 · 쓰는 곳 = 옛 tmp/rint_r_chain_e2e_lwue6x6a 뿐).
  → 묶음 B 를 처음부터 다시 (py311_B2 · e2e · e2e12 · conv_cert · cjunc_store_e2e · rint_r_chain 은 506/506 끝났으므로 빼고).  변이 사본 work/mut = HEAD scripts 와 diff 0 확인.
- (08:44Z) 줄 1 = 3.11 묶음 B 다시 (logs/evac/py311_B2 · py311_B2.out · 백그라운드) · 줄 2 = work/lane2.sh (고아 끝 기다림 → 변이 바탕선 → 변이 86 (Z 뺌 · logs/evac/mut2) → kgy 판 묶음 (logs/evac/kgy_all · 게이트 13 + 새 시험 셋 + 덧) · lane2.out).
- (08:43Z) GPU 하네스: 블록에서 꺼낸 파일 md5 = acfeb4b4… (블록 관문 값과 같음) · 탭 · CR · 느낌표 0 · 두 모듈 sha256 = 블록 값 (git show 다시 셈) ·
  CPU 흐름 (--backend numpy · n-side 24 · 13,824 미지수): 3.11 · kgy 판 3.8 둘 다 다섯 짝 비트 같음 · 주 풀이 267 반복 · 이어 풀기 37 (CPU 길은 Q11 이 안 바꿈 = 흐름 확인일 뿐) ·
  블록 셸 관문 모의 (HOME = 스크래치 · dem-mt = 작업 트리 심볼릭 · 빈 activate): md5 · PIN · 두 커밋 · git show · sha256 관문 통과 → cupy 없음 ERROR rc 1 (기대).  work/gpu_check · work/blk_home.
- (08:47Z) 줄 1b = work/lane1b.sh (B2 끝 기다림 → off_vs_base.py all (바탕 = work/before/scripts = ebb0e9f80 scripts · git hash-object 666/666 같음 확인) → 줄 2 변이 끝 기다림 → 끝-끝 변이 Z1–Z3) · lane1b.out.
  S0 단계 1 다시 = 필요 (바뀐 파일 가운데 step3_sigma.py · mpm_webapp_payload.py 가 S0_SAME_FILES 일곱 안 — rint_r_chain.py 345 줄).
- (08:50Z) 끝 판 시험 파일 (f17ea8c6b) 을 바탕 코드 (work/before_final = ebb0e9f80 scripts + 끝 판 시험 넷) 에서: Q11 10/13 (G1 · G1r · G2 = dia_matrix · 끝 판에서 15 검사) ·
  store 0 PASS · 24 FAIL (T0–T13 = 모듈 없음 · P1 · P2 · P5 · R1 · R2 · C1–C5 · 끝 판 46 검사) · store e2e 0/1 (Z0 = 사슬 선택지 없음) — logs/evac/before/final_tests_*_on_base_py311.log.
- (08:55Z) ★ 빈틈 발견 (변이 목록 대조): 새 규칙 셋에 시험 · 변이가 없었다 — ① 열쇠의 스키마 칸 (T4 가 안 바꿈 · 코드 sha 와 겹 방어) ② 저장본 폴더 소유자 (Store ·
  cjunc_store.py 432) ③ 사슬 폴더 소유자 (rint_r_chain.cjunc_store_dir_problem) — 시험 파일에 소유자 문자열 0.  → 스크래치 사본 work/t_add 에서 시험 보강
  (T4 스키마 갈래 · T11 다른 소유자 · C1 여덟째 다른 소유자 · 도우미 other_owner = root 면 진짜 chown · 아니면 os.getuid 를 잠깐 바꿈) → HEAD 코드에서 통과 ·
  변이 셋 (K13 · W19 · C10) 을 그 사본에서 넣으면 셋 다 잡힘 · chown 실패 길 (root 아님 흉내) 도 T11 · C 통과.  mutate.py 에 K13 · W19 · C10 더함 (92 개) —
  줄 2 변이 (HEAD 시험) 에서는 안 잡힐 것 = 빈틈 증거 · 시험 보강 커밋 (줄 1 · 2 가 트리를 다 쓴 뒤) 뒤 셋만 다시 = 잡힘 확인.
- (09:0xZ) ★ 시험 보강 커밋 = 2f97617ef (작업 트리 · scripts/test_cjunc_store.py 하나 · 서명 없음 · push 없음 · 꼬리 = Claude Opus 5.5 (이 조수 모델) + 같은 세션 줄).
  변이 셋 = 앞 판 시험 (f17ea8c6b · 줄 2 변이 run) 에서 K13 · W19 SURVIVED (C10 = 줄 2 결과 기다림) → 보강 판 (work/t_add = HEAD 2f97617ef scripts) 에서
  K13 · W19 · C10 셋 다 KILLED (logs/evac/mut3_after_testadd).  HEAD 코드 46/46 (77 s · logs/evac/t_add_store_full_py311.log).
  ⚠ 기록: 줄 1 B2 의 rint_r_chain_e2e (51/51 · 849 s) 끝 무렵 ~ e2e12 시작 때 트리에 그 시험 파일 수정이 (커밋 전) 있었다 — 사슬 · 러너 · payload 가 읽는
  CODE_FILES 밖 (시험 파일) 이라 결과 무관 · B2 의 뒤 묶음 (e2e12 · conv_cert · cjunc_store_e2e) 은 HEAD 2f97617ef 에서 돈 셈.
  rint_r_chain_e2e (3.11) = 51/51 · 849 s (앞 조수 판의 E14 FAIL = 끊김 산물 확정 — 같은 HEAD 다시 = E14 · E15 PASS).
- (09:02Z) 변이 (3.11 · 사본 work/mut = f17ea8c6b scripts · 끝-끝 Z 뺀 89 · 490 s · logs/evac/mut2 · mut2_run_py311.log · 바탕선 17 묶음 rc 0):
  잡힘 83 · 안 잡힘 6 = 겹 방어 3 (W6b · P5 · N3c — 미리 redundant 로 적음) + 빈틈 3 (K13 · W19 · C10 — 시험 보강 2f97617ef 뒤 셋 다 잡힘 · mut3_after_testadd).
  ⇒ 끝 판 시험 기준: 잡혀야 할 86 = 86 잡힘 · 겹 방어 3 = 안 잡힘 (동등 — 같은 것을 다른 겹이 막는다).
- (09:02Z) kgy 판 묶음 시작 (logs/evac/kgy_all · HEAD 2f97617ef · 바뀐 파일 0 · 3.8.20 · numpy 1.24.4 · scipy 1.10.1).
- (09:26Z) 3.11 묶음 B2 끝 (logs/evac/py311_B2 · 머리 HEAD = f17ea8c6b 로 시작 · e2e 끝 무렵 시험 보강 커밋 2f97617ef — 그 뒤 묶음은 2f97617ef 트리):
  rint_r_chain_e2e 51/51 (849 s) · e2e12 33/33 (438 s) · conv_cert 30/30 (747 s · 부하 load 6–8) · cjunc_store_e2e 6/6 (613 s · 팔 91 · 단위 3 끔 = 켬 바이트).
  (rint_r_chain 506/506 = 앞 판 py311_B · 390 s.)  → 3.11 묶음 A (27) + B 다 통과 · undef rc 1 = 이 묶음 밖 파일 (generate_comparison_plots.py 6905 · 6906).
- kgy 판 (지금까지 · logs/evac/kgy_all · HEAD 2f97617ef): run_contract 124 · s3_rint · s3_selftest · gpu_precond 15/15 · cjunc_store 46/46 (64 s) · carbon_junction 547 (75 s) ·
  ptfe_fa 242 · ca_ext_b6 502 · ca_ext_runner 151 · verdict 31 · z1 95 · z3 84 · target_cert 264 · s0_census 186 · first_result 9 · rint_receipts 105 · g2_am_iface 136 ·
  probe6 330/330 (272 s) · cmd_selftest 128/128 · cmd_repo 0 오류 (17 경고) · rint_r_chain 506/506 (560 s) — 다 rc 0.  남은 것 = e2e · e2e12 · conv_cert · cjunc_store_e2e.
- (09:30Z) 끔 길 ↔ 바탕 대조 (work/off_vs_base.py · 3.11): 첫 판 (바탕 = work/before 그대로 = git 아님 · docs/data 없음) 은 설정 산물 넷이 더 갈렸다
  (collector.anchors_source · pristine_precision = 바탕 사본에 rint_eis_anchors.csv 없음 · code_sha None · untracked_codelike None · risk 'untracked scan unavailable')
  → 바탕을 스크래치 git 저장소로 (work/ovb_base_repo = before scripts + docs/reviews + docs/data/rint_eis_anchors.csv + .gitignore · 커밋 하나 cf69811) 다시:
  payload 픽스처 둘 (b6 = instance 1 · series3 = instance 2) × (접합 켬 · 끔) 넷 + 실제 러너 (CJ_RT_ENV · 팔 SBE · DBE) — rc 전부 0 · σ_e 같음 ·
  다른 잎 = 코드 신원 칸뿐: code_sha (커밋) · exec_env.project_module_digest · (접합 켬이면) loaded_project_modules +1 (cjunc_store — ca_ext_cjunc 가 늘 부른다) ·
  러너 영수증 code_sha → receipt_digest → OUTDIR 접미사.  payload 인자 (scripts 경로 뺀) 같음 · 팔 이름 같음.  logs/evac/off_vs_base_gitbase_py311.log (첫 판 = off_vs_base_py311.log).
- (09:33Z) 끔 길 ↔ 바탕 kgy 판 (3.8 · 같은 스크립트 · logs/evac/off_vs_base_gitbase_kgy.log) = 3.11 과 같음 — 다른 잎 = code_sha · project_module_digest ·
  loaded_project_modules (접합 켬 +1) · 영수증 code_sha · receipt_digest 뿐 · rc 전부 0 · σ_e 같음.
