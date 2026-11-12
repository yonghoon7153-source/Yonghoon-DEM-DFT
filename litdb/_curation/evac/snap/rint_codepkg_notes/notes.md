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
- (09:49Z) kgy 판 묶음 끝 (logs/evac/kgy_all · HEAD 2f97617ef · 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 25 묶음 전부 rc 0 · 합 2,799 s):
  게이트 kgy 13 (run_contract 124 · s3_rint · ptfe_fa 242 · carbon_junction 547 · ca_ext_b6 502 · ca_ext_runner 151 · rint_r_chain 506 (560 s) · e2e 51 (618 s) ·
  e2e12 33 (287 s) · target_cert 264 · conv_cert 29 (68 s · K4b = scipy 1.10.1 설계상 건너뜀 · 세지 않음) · s0_census 186 · probe6 330 (272 s)) +
  새 셋 (gpu_precond 15/15 · cjunc_store 46/46 (64 s) · cjunc_store_e2e 6/6 (452 s)) + 덧 (s3_selftest · verdict 31 · z1 95 · z3 84 · first_result 9 ·
  rint_receipts 105 · g2_am_iface 136 · cmd_selftest 128 · cmd_repo 0 오류).
  3.11 합: 묶음 A 27 (1,067 s · undef 만 rc 1 = 묶음 밖 파일) + B (rint_r_chain 390 · e2e 849 · e2e12 438 · conv_cert 747 · store e2e 613 s).
- 끝-끝 변이: Z1 KILLED (Z5 — 요약 칸) · Z2 KILLED (Z4) · Z3 = 도는 중.
- (09:5xZ) 끝 HEAD 2f97617ef 트리에서 3.11 다시: store 46/46 (54 s · logs/evac/store_final_head_py311.log) · Q11 15/15.  undef 2 건 = 바탕 (스크래치 git 바탕) 에서도 같은 2 건 (logs/evac/undef_base_py311.log) = 묶음 밖 기존.
- (09:58Z) 끝-끝 변이 Z1 · Z2 · Z3 = 셋 다 KILLED (1,876 s · Z5 · Z4 가 잡음 · logs/evac/mut2_run_py311_e2e.log · 사본 시험 = HEAD 2f97617ef 와 같게 맞춘 뒤).
  ⇒ 변이 합 (끝 판 시험): 잡혀야 할 89 (Z 뺀 86 + Z 3) 전부 잡힘 · 겹 방어 3 (W6b · P5 · N3c) 안 잡힘 = 동등.
- 정리: 사본 work/mut · t_add · ovb* · ovb_base_repo · blk_home · gpu_check 산출 · tmp/* 지움 (돌던 내 프로세스 0 확인 뒤) · 남김 = work/before (앞 조수 · 고치기 전 판) · 스크립트 · logs.
  amend_drafts.md 3 판 (0-b 절 · 2 절 앞 조건 고침 · 4-b 절) · design.md (마) 표에 시험 보강 줄.  ⚠ 시험 임시 폴더 (s3base_gp_* 등) 를 지우지 않는 꼴 = 기존 시험들과 같은 버릇 (고치지 않음).
- 끝.  작업 트리 = 깨끗 · HEAD 2f97617ef (← f17ea8c6b ← ebb0e9f80 ← af3cce37b).

## 리뷰 고침 회차 (11-12 · 내부 반박 리뷰 review/review_codepkg.md 대응 · 작업 트리 /home/user/rint-codepkg)
- (11:1xZ) 시험 먼저 커밋 = 4557a30c2 (← 2f97617ef).  고치기 전 판 (2f97617ef 코드) 결과: Q11 18/19 (실패 G6b REQUIRE 조치 글 = 옳은 이유) ·
  store 40 PASS · 14 FAIL (실패 = 새 검사뿐: T4 ×2 (환경 자리) · T5i (host) · T7 (0666) · T7c (파일 소유자) · T11 (심볼릭 셋) · T14a–d · P1 (rasterize-only 만) ·
  P1b (둘 다 traceback) · R1 (심볼릭 둘) · C1 (심볼릭 둘)).  T14c = 리뷰 CE1 그대로 재현 (같은 열쇠 dbfa9d249e29 · hit · 옛 f24cbd6245dc ↔ 새로 지음 202eb91e965d).
  기록 logs/r2/before/.  G4a · G4b = 시험 질 고침 (RCP-09) 이라 고치기 전에도 통과 (코드 결함 아님 · 커밋 메시지에 적음).
- RCP-01 처분 = (가) 를 고름: 열쇠 코드 칸 = 모듈 넷 (carbon_junction · step3_sigma · fibre_segment_raster · cjunc_store) + 측정 시험 (T14a 동적 =
  sys.setprofile 로 원장 짓기 동안 돈 파일 · T14b 정적 = 원장 모듈 둘의 import 문 AST 전수).  (나) CODE_FILES 전체를 안 고른 까닭 ① 목록 정본이
  rint_r_chain 에 있다 — payload 프로세스에서 사슬 모듈을 부르면 매니페스트 exec_env (로드 모듈 · 내용 해시) 가 바뀌고 (켬 ↔ 끔 팔 바이트) · AST 로 꺼내거나
  사본을 두는 것은 규율 ① 위반 ② 러너 셸 · 사슬 · 판정 코드처럼 원장에 안 닿는 파일까지 묶는다 (과결속 — 캠페인 안에서는 비용 0 이지만 뜻이 틀린다)
  ③ (가) 는 측정 시험이 앞으로의 표류 (원장 코드가 새 모듈을 부르기 시작함) 를 잡는다 — (나) 는 목록 밖 모듈이 생기면 다시 조용히 샌다.
  코드 칸 파일 경로 = importlib.util.find_spec (불러오지 않는다 — 불러온 모듈이면 그 __spec__ · 아니면 import 가 찾을 자리) → 저장본 켬 런의 로드 모듈
  집합이 끔과 같다 (T14d).
- (11:2xZ) 고침 커밋 = 94765bed3 (RCP-01 · 03 한정 · 05 · 06 · 08 · 10 · 11) · 게이트 배선 커밋 = 0ac6edf3c (RCP-02 · check_all 183 → 186 단계 · kgy 13 → 16 묶음 ·
  CI 는 Rint test_*.py 줄이 없어 안 넣음).  고친 뒤 (3.11): store 54/54 (61 s · logs/r2/after/store_py311.log) · Q11 19/19 · 빠른 묶음 (run_contract 124 ·
  s3 selftest · rint · 규율 selftest 128 · repo 0 오류 · ca_ext_runner 151 · ca_ext_b6 502) 통과 (logs/r2/quick) · 리뷰 CE1 다시 = mut 판 다른 열쇠 (7d086 ↔ 4fe10) ·
  built_written · 원장 202eb (옛 hit · f24cb).  check_selftest_inventory 전부 분류 · pyflakes 0 · kgy 3.8 컴파일 · bash -n.
- 다음: 묶음 A · B (3.11) → kgy 판 → 리뷰 변이 31 (도구 review/mutate.py · 사본 다시 만듦) → 구현 쪽 변이 (work/mutate.py · 바뀐 줄 고쳐 씀) → 끔 길 ↔ 바탕 →
  RCP-04 초안 (S0 저장본 재기 블록) · amend 4 판 · design (바).
- (11:4xZ) 묶음 A (3.11 · HEAD 0ac6edf3c · logs/r2/py311_A) = 27 묶음 rc 0 (gpu_precond 19/19 · cjunc_store 54/54 (69 s) · carbon_junction 547 · probe6 330 ·
  ca_ext_b6 502 · runner 151 · verdict 31 · z1 95 · z3 84 · ptfe_fa 242 · target_cert 264 · s0_census 186 · webapp 넷 + provenance 284 · rint_receipts 105 ·
  g2_am_iface 136 · first_result 9 · run_contract 124 · 규율 selftest 128 · repo 0 오류) · undef rc 1 = generate_comparison_plots.py 2 건 (바탕부터 있음 · 묶음 밖).
  묶음 B (3.11) 띄움 (logs/r2/py311_B).
- RCP-04 초안: 감싸개 s0probe/s0_store_probe_en.py (ASCII · 3.8 꼴 · 기록에 절대 경로 · 기계 지문 없음) · 감시 셸 s0probe/mon.sh (run2.sh 꼴 rss.log + rc= 한 줄 ·
  끝에 out_sha256 · 묶음 tgz · DONE · `$!` 대신 jobs -p (느낌표 금지)) · 블록 조립 s0probe/make_s0_block.py → s0probe/s0_rerun_probe_block.txt (md5 관문 둘 ·
  PROBE 0/1 · TAG).  확인: 픽스처 kit_J 감싸개 있음 ↔ 없음 (같은 --out · 3.11 · 3.8) = 다른 잎 elapsed_s 하나 · 재기 instance 2 built_written → hit · 같음 ·
  감싸개 실패 (0777 폴더) = 기록 · S0 rc 0 · 가짜 HOME 블록 모의 (3.8.20 · 스크래치 git = scripts 사본 한 커밋 · 픽스처 킷 = kit_SBE_vgcf100 이름 · 복사본 두 줄 =
  PIN · --vox 0.1): rc 0 · DONE · tgz → 반입 도구 import_s0_tgz.py = ADOPT_CANDIDATE · S0 git_head = 핀 · dirty False · PROBE=0 길 rc 0 · 멈춤 셋 rc 2.
- GPU 블록 4 판: Q11PIN 0ac6edf3c · 새 모듈 sha256 859310da (리뷰 고침이 step3_sigma.py 를 다시 바꿈) · 하네스 md5 그대로 · CPU 흐름 3.11 · 3.8 다섯 짝 같음 (267 · 37) ·
  셸 관문 모의 = cupy ERROR rc 1 (기대).  3 판 사본 gpu_check_block_v3.txt · amend 3 판 사본 amend_drafts_v3.md.
- amend_drafts 4 판 (0-c 처분 표 · 1-1 · 1-2 · 1-4 · 2-b 새 절 (기대 E1–E4 · 문턱 T1–T3 [제안] · Q-B) · 3 · 4-c).
- 변이 준비: 리뷰 31 = review/muts_v4.json (MS10 · MS16 자리만 4 판 글로 — 뜻 그대로) · 사본 review/work/new (git archive 0ac6edf3c scripts webapp + docs 셋) ·
  review/work/mut (cp -al) · 구현 쪽 = work/mutate.py (P5 자리 고침 + 새 규칙 F1–F18 · T14 무리 · 110 개 · 옛 글 110/110 한 번씩 · 3 판 사본 mutate_v3.py) ·
  사본 work/mut (따로 풀기 · 하드링크 아님 — 이 하네스는 제자리 쓰기).  끔 길 바탕 = work/ovb_base_repo (alternates = 본 저장소 객체 읽기만 · HEAD af3cce37b ·
  sparse = scripts · docs/reviews · anchors csv · .gitignore · status 깨끗).
- (12:37Z) 묶음 B (3.11 · logs/r2/py311_B) = rint_r_chain 506/506 (441 s) · e2e 51/51 (784 s) · e2e12 33/33 (378 s) · conv_cert 30/30 (966 s · 부하 load 5) ·
  cjunc_store_e2e 6/6 (618 s).  작업 트리 깨끗.
- 리뷰 변이 31 (review/muts_v4.json · 사본 review/work/{new,mut} = git archive 0ac6edf3c scripts webapp + docs 넷) = 잡힘 30 · 안 잡힘 MS7 (리뷰어 판정대로 동등 —
  발행 전 대조의 엄격 지문 줄 = _read → _content 가 같은 대조를 이미 함) · ★ MS16 (열쇠 코드에서 step3_sigma 뺌 · 고치기 전 = 동등) → 이제 T14a · b · d 가 잡음.
  ⚠ 첫 판은 사본에 docs/reviews/rint2_probe6_prep_20261110/tools 가 없어 T5e 가 사본 탓으로 실패 (MS9 · 12 · 16 의 잡힘이 섞일 수 있음) → 더해 다시
  (바탕선 = store 54/54 · Q11 19/19 · 첫 판 결과 = logs/r2/mut_review/mut_results_muts_v4_first_missing_probe6.json · 다시 = review/mut_results_muts_v4.json ·
  186 s).
- 구현 쪽 변이 (work/mutate.py · 끝-끝 Z 뺀 107 · 사본 work/mut · 603 s · logs/r2/mut_impl/run_py311.log) = 잡힘 104 · 안 잡힘 3 = W6b · P5 · N3c (셋 다 미리
  적은 겹 방어 'redundant') · 새 규칙 F1–F18 18/18 잡힘 (F1 · F2 · F3 = T14 · F4 = T4 · F5 · F6 = T7 · F7 · F8 = T11 · F9 · F10 = C1 · F11 · F12 = R1 ·
  F13–F15 = P1 · P1b · F16 = T5i · F17 · F18 = G6b).  바탕선 D (test_rint_r_chain D10 · D14) 는 사본에 등록 R 문서가 없어 실패 → 넣고 다시 2/2 · D 를 쓰는
  변이는 C6 하나이고 C 가 먼저 잡음 (영향 없음).
- 끔 길 ↔ 바탕 (3.11 · work/off_vs_base.py · 바탕 = work/ovb_base_repo (HEAD af3cce37b) · logs/r2/off_vs_base_py311.log): payload 넷 (b6 · series3 × 접합
  켬 · 끔) + 러너 (CJ_RT_ENV · SBE · DBE) rc 전부 0 · σ_e 같음 · 다른 잎 = 코드 신원 칸뿐 (code_sha · project_module_digest · 접합 켬이면
  loaded_project_modules +1 · 러너 영수증 code_sha · receipt_digest → OUTDIR 접미사) · payload 인자 (scripts 경로 뺀) · 팔 이름 같음 — 11-12 오전 결과와 같은 꼴.
- 끝-끝 변이 Z1–Z3 (3.11 · 1,994 s · logs/r2/mut_impl/run_py311_e2e.log) = 3/3 잡힘 (Z5 · Z4) · 사본 되돌림 diff 0.
- 끔 길 ↔ 바탕 kgy 판 (3.8.20 · logs/r2/off_vs_base_kgy.log) = 3.11 과 같은 꼴 (rc 전부 0 · σ_e 같음 · 다른 잎 = code_sha · project_module_digest ·
  loaded_project_modules +1 (접합 켬) · 영수증 code_sha · receipt_digest).  kgy 판 묶음 25 띄움 (logs/r2/kgy_all).
- (14:16Z) kgy 판 묶음 (3.8.20 · numpy 1.24.4 · scipy 1.10.1 · OPENBLAS 1 스레드 · HEAD 0ac6edf3c · logs/r2/kgy_all) = 25 묶음 전부 rc 0 · 합 2,629 s:
  게이트 kgy 16 (run_contract 124 · s3_rint · ptfe_fa 242 · carbon_junction 547 · ca_ext_b6 502 · ca_ext_runner 151 · rint_r_chain 506 (489 s) · e2e 51 (597 s) ·
  e2e12 33 (310 s) · target_cert 264 · conv_cert 29 (K4b = scipy 1.10.1 설계상 건너뜀) · s0_census 186 · probe6 330 (209 s) · gpu_precond 19/19 · cjunc_store 54/54
  (63 s) · cjunc_store_e2e 6/6 (452 s)) + 덧 (s3_selftest · verdict 31 · z1 95 · z3 84 · first_result 9 · rint_receipts 105 · g2_am_iface 136 · 규율 selftest 128 ·
  repo 0 오류).  작업 트리 깨끗 · 돌던 내 프로세스 0 · tmp 비움 · 지운 사본 = work/ovb_base_repo · work/mut · review/work · s0blk_home (다시 만들기 = 같은
  git archive · alternates 절차 · 위 줄).

## 리뷰 고침 회차 — 끝 (11-12)
- 커밋 (작업 트리 · 서명 없음 · push 없음): 4557a30c2 시험 먼저 → 94765bed3 고침 → 0ac6edf3c 게이트 배선 (← 2f97617ef).
- 처분: 고침 = RCP-01 · 02 · 05 · 06 · 08 · 09 · 10 · 11 / 한정 = 03 (+ 1저자 Q-A) · 07 / 단계 넣음 = 04 (+ 1저자 Q-B · 블록 s0probe/s0_rerun_probe_block.txt).
- 시험: store 40/54 → 54/54 · Q11 18/19 → 19/19 · 3.11 A 27 (undef 2 = 바탕부터 · 묶음 밖) + B 5 · kgy 3.8 25 — 전부 rc 0.
- 변이: 리뷰 31 → 30 잡힘 (MS7 동등 · MS16 = 고치기 전 동등 → 이제 T14) · 구현 쪽 110 → 107 잡힘 · 안 잡힘 3 = 미리 적은 겹 방어 · 새 F1–F18 18/18.
- 끔 경로 ↔ 바탕 af3cce37b (3.11 · 3.8): 다른 잎 = 코드 신원 칸뿐 · σ_e 같음 · rc 0.
- 초안 (스크래치): amend_drafts.md 4 판 · gpu_check_block.txt 4 판 · s0probe/ (감싸개 · 감시 셸 · 조립기 · 블록 · 시험 꼴) · design.md (바).
- 남은 [미확인]: 실침대 저장 · 읽기 (S0 재기 전) · GPU 길 실기계 (블록) · kgy 총 메모리 · 기계 사이 원장 지문 결정성 · gabia Q11REPO · S0 단계 2 (DBE) 가
  이미 돌았는지.

## 2 회차 고침 (11-12 오후 · 재리뷰 review/rereview_codepkg.md · 지시서 BRIEF_fix2_codepkg.md · 작업 트리 /home/user/rint-codepkg)
- 커밋 (서명 없음 · push 없음 · 바탕 0ac6edf3c): f8077a51d 시험 먼저 → 4e1e5b6c6 고침 → ac7e1c58d 게이트 배선 · 결과 전 등록.
- 고치기 전 (0ac6edf3c 코드 · 3.11): store 51 PASS · 11 FAIL (T0 · T11 · T15a–f · P1 · R1 · C1) · git_env 실패 = V 에 커밋 (GIT_DIR 꼴) · selftest 122/124
  (RCPT-sha-clean · untracked) — logs/r3/before_{store,git_env}_py311.log.  고친 뒤: store 62/62 (74 s) · git_env 10/10 · run_contract 125/125 · Q11 19/19 ·
  probe6 330/330 · 규율 repo 0 오류 (17 경고) — logs/r3/after_*.
- 처분: RCP2-01 = 런 시작 코드 칸 (_START · cjunc_store 불러온 때) ↔ 짓기 전 · 발행 직전 다시 셈 (sha · 자리 · 수정 시각 > 시작 + 1 s) → 'disabled' /
  'built_write_skipped' · why 'code_changed: …' (T15 = CE-A 꼴 · 짓는 도중 · 쓰는 도중 · touch · 정직 흐름 적중).  RCP2-06 = run_contract.git_env /
  drop_git_env (GIT_ 접두 전부) · payload _code_sha · _exec_env · 사슬 git_identity · F5 · ledger · selftest 임시 저장소 (꼭대기 확인 뒤만 쓰기) ·
  시험 모듈 넷 + probe6 불러올 때 지움 · 새 시험 test_git_env_isolation.py (G1–G6 · 일회용 V · 자식에만 적대 환경).  RCP2-02 = 정규화 (빈 · . · .. 성분 거부 ·
  끝 빗금만 걷음) Store · 사슬 · 러너.  RCP2-03 = T7 그룹 쓰기만 넷 · T11 ow2 0757.  RCP2-04 = docs/reviews/rint2_s0_store_probe_20261112/ (README +
  블록 · 감싸개 v2 = cjunc_store 먼저 불러옴 · store_start · code_drift).  RCP2-05 = T14 재작성 (실행 파일 전수 분류 · 'other' 0 · import 허용 목록 ·
  변이 코드 폴더 subprocess).  RCP-03 · 04 · 06 남은 몫 = 한정 문장 (cjunc_store 머리).
- 봉인 확인: 손댄 파일 = 194 CODE_FILES 32 · 언로딩 키트 SHA256SUMS · 믹서 봉인 어디에도 없음 · run_contract · payload · 사슬 · 러너 = 사슬 CODE_FILES (봉인 전) ·
  payload = S0_SAME_FILES (S0 단계 1 다시 = 끝 핀).
- (15:47Z) 검증 묶음 (work/run_r3_all.sh · 백그라운드 bm3t4w6o2) = 3.11 A → B → kgy_all · logs/r3/.  A (중간): run_contract 125 · 규율 selftest 128 ·
  s3 · rint · repo 0 오류 · git_env 10 · Q11 19 · store 62 (78 s).
- 변이 도구 work/mutate_r3.py (GIT_DIR 없음 · 사본 = git archive + git init + alternates (공용 객체 읽기만) + 커밋 하나 = precond 의 git show 가 사본 안에서
  돈다) · 사본 work/mut3 (ac7e1c58d) · 자리 확인 rev2 21 · new 28 · rev1 31 · impl 110 = 문제 0.
- 미리 돌림 (가벼움): H20 KILLED (G5) · H21 SURVIVED (= 빈틈 — G5 가 사슬 F5 plan_commit_problem 을 안 부름) → 묶음 끝난 뒤 G5 보강 커밋 (4 번째) 예정.
- (17:37Z) 검증 묶음 끝 (HEAD ac7e1c58d · 작업 트리 바뀐 파일 0 · logs/r3/{py311_A,py311_B,kgy_all}/_summary.txt):
  3.11 A = 28 rc 0 (run_contract 125 · 규율 selftest 128 · repo 0 오류 · git_env 10 · Q11 19 · store 62 · carbon_junction 547 · probe6 330 ·
  ca_ext_b6 502 · runner 151 · verdict 31 · z1 95 · z3 84 · ptfe_fa 242 · target_cert 264 · s0_census 186 · rint_receipts 105 · g2_am_iface 136 ·
  first_result 9 · webapp provenance 284 · 웹앱 여섯) + undef rc 1 = generate_comparison_plots.py 6905 · 6906 (바탕부터 · 묶음 밖 · 같은 2 건).
  3.11 B = rint_r_chain 506 (385 s) · e2e 51 (768 s) · e2e12 33 (408 s) · conv_cert 30 (684 s) · store e2e 6 (684 s).
  kgy 3.8.20 = 26 rc 0 (git_env 10 · Q11 19 · store 62 (89 s) · rint_r_chain 506 (520 s) · e2e 51 · e2e12 33 · conv_cert 29 (K4b 설계상 건너뜀) ·
  store e2e 6 (448 s) · probe6 330 · …).
- (17:3xZ) 변이 보강 커밋 8cc3fe462 (G5 에 사슬 plan_commit_problem — H21 이 앞 판 시험에서 SURVIVED (logs/r3/mut_probe) · 고친 G5 사본에서
  KILLED (logs/r3/mut_probe_g5)) · 3.11 · 3.8 둘 다 10/10 · pyflakes 깨끗.  사본 work/mut4 = 8cc3fe462 (scripts 나무 같음 · 변이 자리 194/194).
- GPU 블록 5 판 = gpu_check_block.txt (Q11PIN 8cc3fe462… · 새 모듈 sha256 859310da 그대로 = 2 회차가 step3_sigma.py 안 바꿈 · 하네스 md5
  acfeb4b4 그대로 · 느낌표 · 탭 · CR 0 · bash -n) · 4 판 사본 gpu_check_block_v4.txt.
