# Codex 봉인 전 묶음 1/2 — Rint ② 코드 묶음 (탄소 접합 원장 저장본 Q2 + GPU 전처리 C 꼴 Q11 + git 환경 격리) · S0 · GPU 측정 블록 설계 (2026-11-13 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 1저자 11-12 결정 (Q2 탄소 접합 준비 재사용 + Q11 GPU 전처리 C 꼴 = 한 코드 묶음 · `docs/reviews/rint2_time_reestimate_20261111/README.md` 428 줄 절 "1저자 결정 (11-12 · 결정 기록)") 의 코드 · 시험 (16 커밋) 과, 그 코드로 잴 측정 블록 둘의 **설계**를 반박해 달라.  측정 값 · 봉인 숫자는 2/2 다.
> **리뷰 핀** = 이 요청서가 든 커밋 (40 자리 = ZIP `PIN.txt` · 가지 `claude/sdcp-dem-manuscript-si-pqwtv8` · ZIP `PIN.txt`) · **코드 핀** = `56f4cfbb1` (측정 블록 둘의 핀 · 코드 핀 ↔ 리뷰 핀 차이 = ZIP extra/code_diff_codepin_to_pin.txt · §9) · **비교 기준** = `a0455e90b` (묶음 바로 앞 · 그 `scripts/step3_sigma.py` = `11a794674` 와 sha256 `8d428ff5…` 같음).
> **지위**: 결과 0 건.  이 묶음은 Codex 를 아직 거치지 않았다 — 거친 것은 내부 반박 리뷰 세 회 + 마지막 좁은 고침 (독립 조수 · Codex 아님 · 1저자 11-10 운영 결정 · §4).  회차 ⑥ (11-10 · 검토 핀 `aec8ca2f6`) 의 "전체 HOLD" 는 그대로다.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (2/2 또는 범위 밖) |
|---|---|
| ① Q2 원장 저장본 — 열쇠가 낡은 · 다른 원장을 돌려주지 않는가 · 실패 길 처분 · 동시 쓰기 · 켬 ↔ 끔 산출 바이트 같음 · 저장본 밖 독립 대조의 범위 (§2 · §3 B1–B7 · Q1–Q7) | 측정 값 — S0 단계 1 다시 + 저장본 실침대 재기 (kgy · 11-13 01:47:26 UTC 시작 · 결과 미열람 · 기록 = 진행 기록 `docs/session_20260923_progress.md` 11-13 [Rint ②] 줄) · GPU 확인 · ⑥ 시도 3 · 4 |
| ② Q11 GPU 전처리 C 꼴 — A 꼴과 같은 수 · 같은 정지 · 비트 같음 주장의 근거 · `LinearOperator` 없는 cupyx 처분 (§3 B8 · B9 · Q8) | 봉인 숫자 (maxiter ≥ 3,000,000 · 시간 상한 · 최대 시도 수 — 1저자 11-12 Q3 · Q4) · 시간 표 다시 · 계획 §10 개정 · 봉인 · R 런 |
| ③ git 환경 격리 (`SELF-169` 부류) — 생산 git 읽기 · selftest · 시험 고정물 · 게이트 머리 (§3 B10 · Q13) | ⑥ 시도 3 · 4 의 도구 — 지금 `run_probe6.sh` 는 시도 1 · 2 짝만 알고 (236–251 줄) 러너 env 의 `CJUNC*` 를 지운다 (430–438 줄) → 도구 고침 (시험 먼저) + 원장 줄이 먼저 · 리뷰 핀 커밋에 들어가면 §9 |
| ④ 측정 블록 설계 — 결과 전 기대 · 문턱 · 멈춤 · 쓰는 자리 (§5 · Q10 · Q11) | 회차 ⑥ 의 남은 조건 (현장 자격 §7④ 부분 수용 · Q5 순서 보완 · 판정문 5 줄 "전체 HOLD 유지") · `RR6-01` · `02` (claimed_fixed · Codex 확인 전) · 열린 원장 (`P6R3-01` · `02` · `03` · `05` · `RIMPR-04` · `RCA-11` 등 · 이 묶음과 무관) |
| ⑤ 게이트 배선 — `scripts/check_all.sh` 새 단계 넷 + 머리 한 줄 · `scripts/check_kgy_py38.sh` 17 묶음 (§3 B12) | 두 기계 조립 비트 같음 (1저자 11-12 Q10) 의 실측 — 질문 Q12 만 |
| | 생산 GO · 판정 · σ 값 (0 건) |

## 1. 보내는 것 (ZIP · 리뷰 핀 blob 그대로 + `extra/` + `PIN.txt` + `ZIP_MANIFEST.tsv`)

만드는 법 = `make_zip.sh <REVIEW_PIN> <출력.zip>` (리포 뿌리에서 · git 읽기 명령만 · repo/ 파일마다 git blob sha1 을 ls-tree 와 다시 대조 · 같은 입력 = 같은 바이트).  코드 핀으로 만든 시험 ZIP (요청서 없음) = 파일 64 (repo/ 51 · extra/ 11 · PIN.txt · ZIP_MANIFEST.tsv) · 3,356,303 B · 두 번 만들어 바이트 같음 (리뷰 핀이면 요청서 · 대조표가 더해져 수 · 바이트가 바뀐다).

| 묶음 | 파일 (리뷰 핀) |
|---|---|
| 이 요청서 | `docs/reviews/codex_rint2_codepkg_review_request_20261113.md` (+ 대조표가 커밋되면 `docs/reviews/codex_rint2_codepkg_claims_check_20261113.md`) |
| 코드 묶음이 바꾼 25 파일 (`git diff --name-only a0455e90b 8ace86a82`) | `scripts/cjunc_store.py` (새) · `step3_sigma.py` · `mpm_webapp_payload.py` · `ca_ext_cjunc.py` · `rint_r_chain.py` · `run_contract.py` · `sdcp_gain_vox015_8arm.sh` · `ca_s0_census.py` · `check_all.sh` · `check_kgy_py38.sh` · `check_method_discipline.py` · `check_review_findings.py` · 시험 11 (`test_cjunc_store.py` · `test_cjunc_store_e2e.py` · `test_step3_gpu_precond.py` · `test_git_env_isolation.py` (넷 새) · `test_ca_s0_census.py` · `test_rint_r_chain.py` · `test_rint_r_chain_e2e.py` · `test_rint_r_chain_e2e12.py` · `test_step3_conv_cert.py` · `webapp/test_pipeline_provenance.py` · `docs/reviews/rint2_probe6_prep_20261110/tools/test_probe6_read.py`) · S0 등록 `docs/reviews/rint2_s0_store_probe_20261112/` (README · 블록) |
| 읽기용 (안 바뀜) | `scripts/carbon_junction.py` (원장 · 열쇠 입력) · `scripts/fibre_segment_raster.py` (열쇠 코드 칸) · `docs/reviews/rint2_probe6_prep_20261110/tools/run_probe6.sh` (⑥ 도구 범위) |
| 내부 반박 리뷰 기록 | `docs/reviews/rint2_codepkg_20261113/` (README · SHA256SUMS · 기록 묶음 tgz 888,018 B · sha256 `887566e8…` · MANIFEST 233 + MANIFEST 자신 = 234 파일) |
| 결정 · 계획 · 원장 | `docs/reviews/rint2_time_reestimate_20261111/README.md` (+ `bench/results_20261112/`) · `docs/reviews/rint2_dev_probe_ledger_20261026.md` · `docs/reviews/rint2_siteq_remaining_plan_20261110.md` · 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · 회차 ⑥ 판정 `docs/reviews/codex_review_rint2_rr_round6_20261110.md` · `docs/reviews/findings.json` · S0 11-08 기준 `docs/data/rint2_s0_sbe_20261108/` (README · ADOPTION_CHECK · `docs/data/rint2_s0_sbe_20261108/tools/import_s0_tgz.py`) · ⑥ 시도 2 `docs/data/rint2_probe6_a2_20261111/README.md` |
| `extra/` (리포에 없음) | `kgy_2_gpu_check_block.txt` (GPU 확인 블록 · v7 본문 · Q11PIN = 코드 핀) · `kgy_1_s0_rerun_block.txt` (S0 블록 사본) · `s0_block_vs_registered.diff` · `code_diff_codepin_to_pin.txt` · `runs_56f4cfbb1/` (§7 우리 다시 돌림) · `wrapper_fixture_round2_code/` (감싸개 픽스처 대조 로그 · 2 회차 코드 · §8) · `README.txt` |

ZIP 밖 근거 (리뷰 핀에서 읽는다): E2 의 instance 수 = `docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/s0_stage1_kit_SBE_vgcf100.json:397` (`n_instances` 117583 · 6,286,674 B · 쓰는 값이 한 줄이라 ZIP 에 싣지 않았다) · B12 게이트 서술 = `docs/handoff_return_to_stoic_knuth_20261113.md:11` (비 Rint 인계 문서).

## 2. 무엇이 바뀌었나 (`a0455e90b..8ace86a82` · 16 커밋 · 25 파일 · +5,727 / −60 · 그 뒤 `30a9e937c` 기록 · `56f4cfbb1` 비 Rint 인계 = 코드 무변경)

| 회차 | 반입 커밋 (작업 트리 원 sha = 커밋 끝 줄 `cherry picked from`) | 무엇 |
|---|---|---|
| 시험 먼저 | `650ecaae5` | Q11 G1–G7 · Q2 T0–T11 · P · R · C · 끝-끝 Z0–Z6 |
| 구현 | `95cf418ee` | Q11 C 꼴 · Q2 저장본 + 배선 · 넘겨받은 판 결함 둘 고침 (instance ≥ 2 원장 = 별칭 → 저장 건너뜀 · 겹침 검사 n²) |
| 시험 보강 | `e32ac7f8e` | 열쇠 스키마 칸 · 폴더 다른 소유자 (Store · 사슬) |
| 내부 리뷰 1 | `0f2ecaa05` → `853672840` → `e4c51669f` | RCP-01 (열쇠 코드 칸에 `fibre_segment_raster` 빠짐) · 05 · 06 · 08 · 09 · 10 · 11 · 게이트 배선 |
| 내부 리뷰 2 | `410920bcb` → `5eba3628e` → `882f03a8d` → `caafce187` → `7173083c4` | RCP2-01 런 시작 코드 칸 · 02 경로 정규화 · 06 git 환경 · 04 S0 결과 전 등록 · 변이 보강 둘 |
| 같은 부류 | `ab33150e2` → `2bae2d936` | 시험 모듈 셋이 불러올 때 `GIT_*` 를 지운다 |
| 내부 리뷰 3 | `88ece7636` → `27ef82d24` → `8ace86a82` | RCP3-01–05 (S0 계획 시험 고정물 git · stat 신원 정확 대조 · import 차례 · 지우는 이름 좁힘 · 게이트 수준 셸 꼴) · 시험 맞춤 |

| 자리 (코드 핀 `56f4cfbb1` 의 줄) | 무엇 |
|---|---|
| `scripts/cjunc_store.py` (889 줄) | 열쇠 `Store.key_parts` 580–587 · 코드 칸 `CODE_MODULES` 85 (`carbon_junction` · `step3_sigma` · `fibre_segment_raster` · `cjunc_store`) · `code_file` 412–424 (find_spec · 불러오지 않음) · 환경 `env_paths_fp` 427–434 · 기계 `machine_fp` 391–401 · 런 시작 `_start_record` 470–481 / `_START` 484 · `code_drift` 487–507 · 직렬화 `_Walk` 142–239 · `_no_overlap` 242–252 · 읽기 `_read` 600–613 · `_content` 615–648 · `_read_members` 804–855 · 쓰기 `_publish` 651–732 · `get_or_build` 734–801 · 폴더 검사 `Store.__init__` 548–577 |
| 배선 | `scripts/ca_ext_cjunc.py` 35–36 (cjunc_store 를 carbon_junction 보다 먼저) · `payload_prepare(store=)` 219–270 · payload `--step3-cjunc-store` 1621 · 입구 계약 `_cjunc_entry_contract` 912–1023 (`STORE_GRAPH_ONLY` · `STORE_RASTERIZE_ONLY` · `STORE_PATH`) · 본 길 2491–2509 (`S2_CJUNC_STORE|INCONSISTENT|` · 화면 한 줄) · 러너 `CJUNC_STORE` 583–621 · 사슬 `cjunc_store_dir_problem` 5614–5637 · `Runner.env_delta` 5658–5662 · 봉인 원천 `env_delta` 의 `CJUNC_STORE` 지움 5852 · 단계 요약 `cjunc_store: true` 6597 · 6801 · `--cjunc-store` = ladder · predict 만 8629–8639 · CLI 회계 `run_contract.py:142` (mode) · 규율 검사기 격리 목록 `check_method_discipline.py:937` · 사슬 `CODE_FILES` 19 → 20 (`rint_r_chain.py:335–340` · `cjunc_store.py` = 340) |
| `scripts/step3_sigma.py` `_solve_cg` 535–629 | GPU 길만: `LinearOperator` 따로 import (없으면 사유 `no_linop`) 574–578 · `_dinv = 1.0 / cp.asarray(diag)` · `Mg = _LinOp(Lg.shape, matvec=lambda _r: _dinv * _r, dtype=np.float64)` 586–587 · 사유별 조치 글 (REQUIRE_GPU) 600–608 · 기록 `precond` = 'jacobi' 그대로 · 새 기록 키 없음 · CPU 길 그대로 |
| git 환경 | `run_contract.py` `GIT_DROP_NAMES` · `GIT_DROP_PREFIXES` · `GIT_DROP_SH` 1464–1469 · `git_env` 1477–1481 · `drop_git_env` 1484–1492 · `git_fixture_env` 1498–1516 · `normal_path_problem` 1519–1534 · selftest RCPT-sha 임시 저장소 (꼭대기 확인 뒤만 쓰기 · 2435–2471) · payload `_exec_env` 607–670 · `_code_sha` 678–743 · 사슬 `git_identity` 948–983 · `plan_commit_problem` 1767–1791 · `ledger_git` 3069–3079 · `_git_top` 3082–3088 · `ca_s0_census._git` 901–905 · `check_review_findings._git_env_clean` 744–750 · 셸 꼴 = `check_all.sh:19` · `check_kgy_py38.sh:12` · 러너 기각 영수증 1082 · S0 블록 heredoc 머리 · 시험 모듈 아홉 = 불러올 때 지움 (G6 목록 여덟 `test_git_env_isolation.py:431` + `test_step3_gpu_precond.py:45` = G4 가 봄) |
| 게이트 | `check_all.sh` 333 · 334 · 336 · 341 (전처리 · 저장본 · 저장본 끝-끝 · git 환경) · `check_kgy_py38.sh` 끝 넷 (17 묶음) |

## 3. 내세우는 보장 (보장마다 시험 · 수 · 고치기 전 → 뒤)

수 = 코드 핀에서 우리가 다시 돌린 것 (§7 · Python 3.11.18) 또는 기록 (표지).  "고치기 전 → 뒤" = 그 시험 먼저 커밋의 메시지 (고친 사람의 실행 · 커밋 sha).

| # | 보장 | 시험 (지금) | 고치기 전 → 뒤 | 한정 |
|---|---|---|---|---|
| B1 | 열쇠가 원장 입력 전부에 묶인다 — 다른 침대 · lo · vox · 점 · phase · fid · kind · 문턱 열 칸 (s_min None 포함) · 코드 · 환경 · 기계 · 꼴 판 · 모델 판 · 스키마 = 다른 열쇠 · 같은 값 = 같은 열쇠 (메모리 차례 · 정수 폭 무관) | `test_cjunc_store.py` T4 (넷 · 27 갈래) · T5h · T8 · T14 · T14a–d (짓는 동안 돈 파일 ⊆ 표준 · numpy · scipy · 열쇠 넷 · 원장 모듈 import AST · 리뷰 반례 CE1) | 저장본 시험 40 PASS · 14 FAIL (실패 = 새 검사뿐) → 54/54 (`0f2ecaa05` → `853672840`) | 같은 기계 · venv 의 실행 env (BLAS · SIMD 선택) 는 열쇠 밖 (Q2) |
| B2 | 못 읽음 (CRC 를 지난 멤버 바이트를 얻기 전 실패) = 다시 짓기 · 파일 그대로 · ⚠ 줄 | T6 (7 갈래) · T6b · P3 | 저장본 시험 0/21 → 46/46 (`650ecaae5` → `95cf418ee` · 넘겨받은 판 33 PASS · 8 FAIL) | 그 파일은 덮어쓰지 않는다 (`cjunc_store.py:774`) → 운영자가 지울 때까지 그 열쇠의 팔마다 다시 짓기 + ⚠ (이득 0) |
| B3 | 어긋남 (그 뒤 전부 · 소유자 · 그룹 · 남 쓰기 · 링크 · 뜻밖의 내용 오류) = 멈춤 `S2_CJUNC_STORE|INCONSISTENT|` · 쓰기 쪽 실패 · 뜻밖의 예외 = 기록만 · 읽기 MemoryError = 그대로 | T7 (17 갈래) · T7b · T7c · T11 (8 갈래) · T12 · P4 · P1 (일곱) · P1b · R1 (열셋) · C1 (열넷) | 위와 같은 사슬 + 2 회차 51 PASS · 11 FAIL → 62/62 (`410920bcb` → `5eba3628e`) | 경로 기준 (fd 아님) · 링크 판정 = 마지막 성분 (중간 링크 따름) |
| B4 | 동시 쓰기 · 끊김 — 단일 작성자 (O_EXCL 임시 → fsync → 같은 읽기 길로 다시 읽어 엄격 지문 → 0444 → 코드 칸 다시 셈 → `os.link` · 덮어쓰기 없음) · EEXIST = 남의 파일 대조 (같음 = `built_peer_same` · 다름 = 멈춤) | T9a–c (실제 프로세스 둘) · T10a–b (PID 이름공간 SIGKILL) | — | 링크 수 안 봄 (`cjunc_store.py:819`) · 끊긴 쓰기의 임시 파일은 남는다 (T10a · RCP-07 = 한정) · 공유 파일계 (NFS 등) 미검토 |
| B5 | 켬 ↔ 끔 산출 바이트 같음 (팔 JSON · 매니페스트 · 영수증 · OUTDIR · 이름) | P2 · P5 (instance 2) · R2 · T5c · T5d · `test_cjunc_store_e2e.py` Z1–Z6 (사다리 · 예측 · 판정 · 다시 판정 · 단위 = 켬 ↔ 끔 바이트 · 봉인 원천 · 저장본 폴더 · 적중 런) | e2e: Z0 실패 → 6/6 (`650ecaae5` 메시지 9 줄 → 기록: 3.11 511.4 s · kgy 판 412.4 s · `logs_r5`) | 합치기 (`--merge`) 시험 없음 (e2e 머리 한정) · 저장본 상태는 화면 한 줄 + 요약 `cjunc_store: true` 뿐 (RCP-07) |
| B6 | 봉인 원천 (조립만 · `RunnerGraphSource`) 은 저장본을 읽지 않는다 = 저장본으로 지은 팔의 그래프 지문을 저장본 없이 다시 조립한 원천과 견준다 | C3 · Z4 · payload `STORE_GRAPH_ONLY` · 러너 ABORT | — | 이 대조 = SV 모서리 팔만 · 사다리 · 비 SV 예측 · 단위 팔은 저장본 밖 독립 대조 없음 (대조 길 = 1저자 결정 Q-A · 기록 7 판 = 열린 질문 · 지금 = 한정 그대로 `cjunc_store.py:33–38` · Q6) |
| B7 | 런 도중 코드 바뀜 = 읽지도 쓰지도 않음 (`_START` ↔ get_or_build 시작 · 발행 직전 · 자리 · sha256 · stat 신원 [dev · ino · size · mtime_ns · ctime_ns] 정확 · Store 칸 = 시작 칸) | T15a–m (13) · P6 · P6b (`python -X importtime` = cjunc_store 가 원장 모듈보다 먼저) | 3 회차 `--only T15,P` 13 PASS · 6 FAIL → 19/19 (`88ece7636` → `27ef82d24`) · 지금 70/70 | §8 한정 (가)–(마) |
| B8 | C 꼴 = A 꼴 같은 산술 (가짜 cupy = cupy 12.3.0 `cg` · `_make_system` 동작) — 해 바이트 · info · 반복 수 · LAST_BACKEND 같음 · 바이트 차이는 (C = −0 ∧ A = +0) 칸뿐 · 생산 꼴 b 에서 CG 의 r 에 −0 없음 | `test_step3_gpu_precond.py` G1 · G1r · G2 (새 배열 · dtype 탐침 없음) · G3 (옛 `11a794674` ↔ 지금 · 24 짝 · 수렴 · maxiter) · G4a–c · G7 (`solve_sigma_z` 끝-끝) | 10/13 → 15/15 (`650ecaae5` → `95cf418ee`) · 18/19 → 19/19 (`0f2ecaa05` → `853672840`) | 가짜는 GPU 반올림을 흉내 내지 않는다 · 실기계 = GPU 확인 블록 (§5-2 · [미확인]) |
| B9 | CPU 길 · 폴백 그대로 · `LinearOperator` 없는 cupyx = 옛 A 꼴로 되돌리지 않음 (CPU 폴백 · REQUIRE_GPU = 사유별 조치 글) | G5 · G6 · G6b | 위와 같음 | — |
| B10 | git 을 부르는 생산 · selftest · 시험 고정물 · 게이트가 부르는 쪽의 저장소 고르는 `GIT_*` 여덟 + 설정 주입을 물려받지 않는다 · 격리 변수 (`GIT_CEILING_DIRECTORIES` · `GIT_CONFIG_NOSYSTEM` · `GIT_CONFIG_GLOBAL`) 는 산다 | `test_git_env_isolation.py` G1–G8c (적대 꼴 넷 = GIT_DIR · +WORK_TREE+INDEX_FILE · OBJECT_DIRECTORY+COMMON_DIR · 훅 꼴 GIT_INDEX_FILE 하나 → 일회용 저장소 V) | 4 PASS · 6 FAIL → 10/10 (`410920bcb` → `5eba3628e`) · 9 · 1 → 10/10 (`ab33150e2` → `2bae2d936`) · 9 · 8 → 17/17 (`88ece7636` → `27ef82d24`) → 19/19 (`8ace86a82`) | §8 (바)–(타) |
| B11 | 끔 길 = 바탕 — 바탕 `af3cce37b` (`a0455e90b` 와 scripts 차이 = 믹서 둘) ↔ 끝 (8b59b9618 (작업 트리 커밋 · 원격에 없음) = 반입 `8ace86a82`) · payload 넷 (b6 · series3 × 접합 켬 · 끔) + 러너 (SBE · DBE) · rc 0 · σ_e 같음 · 다른 잎 = 코드 신원뿐 (manifest `code_sha` · `project_module_digest` · `loaded_project_modules` (접합 켬 +1 = cjunc_store) · 영수증 `code_sha` · `receipt_digest` → OUTDIR `_r` 꼬리) | 기록 `logs_r5/off_vs_base_py311.log` · `_py38.log` (기록 묶음 · 고친 쪽 스크립트 · 두 판 같은 요약) | — | CPU 길만 (GPU 길은 Q11 이 일부러 바꿈 → B8 · §5-2) |
| B12 | 게이트 · kgy 판 배선 | `check_all.sh` 단계 넷 (run 줄 187 · 기록 `logs_r5/check_all_split.log` 1 줄 "원문 run 187") · `check_kgy_py38.sh` 17 묶음 · `56f4cfbb1` 의 게이트 = 두 조각 1–125 · 126–187 fail 0 (11-13 · 출력 원본 리포 밖 · 기록 = 진행 기록 `docs/session_20260923_progress.md` 11-13 [Rint ②] 줄) | 183 → 186 (`e4c51669f`) → 187 (`882f03a8d`) | kgy 판 17 묶음 = 한 번에 돈 기록 아님 (§8) |

변이 (내부 리뷰 · 고친 쪽 · 기록 묶음): 구현 판 = 잡혀야 할 89 전부 잡힘 · 겹 방어 3 (W6b · P5 · N3c) / 1 회차 뒤 = 리뷰어 31 → 30 + MS7 (동등) · 구현 쪽 107 → 104 + 겹 방어 3 · F1–F18 18/18 · 끝-끝 Z 3/3 / 2 회차 뒤 = N 21/21 · H 32 → 29 + 겹 방어 3 · 구현 쪽 W14 생존 → 시험 보강 `7173083c4` 뒤 잡힘 / 3 회차 = J1–J32 → 31 잡힘 · J22 (stat 신원에서 inode 뺌) = 미리 적은 겹 방어 (ctime 이 덮음) · 3.11 · 3.8 같음 · 기록 메모: J21 (ctime 뺌) 은 이 파일계가 지운 파일의 inode 번호를 새 파일에 다시 써서 T15i 에서도 잡혔다 → 결정적 판 = T15l (다른 파일계에서는 T15i 의 판별이 다를 수 있다 [추정]).
(출처 = 기록 묶음 `notes.md` 77–79 · 103–104 · 145–157 · 171 · 206–213 · 237 · 289–291 · 같은 묶음 `review/` · `logs_r5/mut/`.)

## 4. 내부 반박 리뷰 요약 (배경 · 닫힘 근거 아님 · Codex verified 로 올리지 않았다)

| 회차 | 대상 (작업 트리 sha) | 지적 | 처분 |
|---|---|---|---|
| 1 review/review_codepkg.md | `af3cce37b..2f97617ef` | P1 1 · P2 3 · P3 7 (RCP-01–11) — P1 = 열쇠 코드 칸에 `fibre_segment_raster.py` 빠짐 (선분 → 셀 차례만 바뀐 코드에서 옛 원장 적중 · 반례 CE1) | 고침 01 · 02 · 05 · 06 · 08 · 09 (시험만 = G4 다시 씀) · 10 · 11 / 한정 03 · 07 / 단계 04 (S0 실침대 재기 블록) — 기록 `notes.md` 169 |
| 2 review/rereview_codepkg.md | `2f97617ef..0ac6edf3c` | RCP 닫힘 7 · 일부 3 (03 · 04 · 06) · 안 닫힘 1 (07 = 한정) · 새 P1 0 · P2 2 · P3 4 (RCP2-01–06 · 01 = 런 도중 코드 바뀌면 옛 원장이 새 열쇠로 저장 · 06 = selftest 의 git 이 부르는 쪽 GIT_* 를 물려받음 = `SELF-169` 뿌리) | 고침 01 · 02 · 06 · 시험 03 · 05 · 등록 04 · ⚠ 이 회차 리뷰어의 변이 21 (20 잡힘) 은 GIT_DIR 이 샌 환경에서 돌았다 (`SELF-169` 사고) → 쓰지 않음 · 고친 쪽이 깨끗한 환경에서 N 21/21 |
| 3 review/recheck2_codepkg.md | `0ac6edf3c..ea3b13b89` | 닫힘 6 · 부분 3 · 안 됨 0 · 새 P1 0 · P2 1 · P3 4 (RCP3-01–05) | 마지막 좁은 고침 (다섯 다) · 이 뒤 재확인 없음 → 이 요청 |

(파일 = 기록 묶음 `rint2_codepkg_records_20261113.tgz` 안 · 기록 README 의 "리뷰 (RCP-01–08)" 는 리뷰 원문의 RCP-01–11 과 다르다 — 원문이 맞다 · 대조표.  RCP · RCP2 · RCP3 은 원장 `findings.json` 에 줄이 없다 (내부 기록만 · 원장에 있는 것 = `SELF-169` claimed_fixed).)

## 5. 측정 블록 설계 (이번엔 설계만 · 값 = 2/2)

### 5-1. S0 단계 1 다시 + 원장 저장본 실침대 재기 (kgy · CPU 약 1.5 h)

| 칸 | 내용 |
|---|---|
| 등록 (결과 전) | `docs/reviews/rint2_s0_store_probe_20261112/README.md` · 블록 같은 폴더 (275 줄 · md5 `39c4b975…`) · 1저자 11-12 밤 Q-B (가) = 공식 S0 단계 1 다시를 감싸개로 (`PROBE=1`) · 문턱 T1–T3 채택 |
| 왜 다시 | 사슬 `S0_SAME_FILES` 일곱 가운데 셋이 이 묶음에서 바뀜 (`step3_sigma.py` · `mpm_webapp_payload.py` · `ca_s0_census.py` (`_git` · git 환경만)) — 원장 코드 (`carbon_junction.py` · `fibre_segment_raster.py`) 는 11-08 S0 핀 `f47bde0f6` 뒤 그대로 |
| 이번 사본 | extra/kgy_1_s0_rerun_block.txt = 등록 블록에서 두 줄 (30 · 34) — `PIN='56f4cfbb1…'` · `BR=claude/sdcp-dem-manuscript-si-pqwtv8` (등록 블록의 BR = stoic · 사본을 만든 때 원격 추적 ref = `af3cce37b` 동결 → 시작 관문 'PIN = fetch 뒤 가지 끝' (블록 56 줄) 에서 멈춘다 · 그 뒤 본 세션의 stoic 앞당김 여부 = [미확인]) · 안쪽 md5 관문 둘 (감싸개 `86e9bf4b…` · 감시 셸 `ff385531…`) 그대로 · ASCII · 탭 · CR · 느낌표 0 · `bash -n` 통과 · 차이 = `extra/s0_block_vs_registered.diff` |
| 감싸개 | S0 이 지은 원장 직후 같은 프로세스에서 ① `encode_strict` ② `Store.get_or_build` (짓고 씀 · 발행 전 다시 읽기 대조) ③ 새 Store 로 다시 = 적중 ④ 읽은 원장 = 지은 원장 (엄격 지문 · `registry_fp`) ⑤ VmRSS · VmHWM → `store_probe.json` · S0 에는 **지은 그 원장 객체**를 돌려준다 · 재기 실패 = 기록 · S0 계속 |
| 결과 전 기대 | E1 S0 rc 0 · 여섯 출력 · 반입 도구 채택 후보 · git_head = PIN · git_dirty False / E2 감싸개 호출 1 번 · instance **117,583** (11-08 SBE 보고 `n_instances` · §1 ZIP 밖 근거) / E3 encode ok · 쓰기 `built_written` · 읽기 `hit` · 엄격 True · registry_fp True · `store_start` preloaded `[]` · error None · `code_drift` `[]` / E4 S0 계획 · 배열 = 11-08 (코드 지문 · 시각 칸 빼고) |
| 문턱 (넘으면 보고 · R 계획이 정함) | T1 쓰기 ≤ 600 s · 읽기 ≤ 300 s · 읽기 ≤ 짓기의 10 % / T2 메모리 증가 ≤ 4 GiB / T3 파일 ≤ 2 GiB |
| E3 어긋남 처분 | R 에서 `--cjunc-store` 를 쓰지 않는다 · 본 세션 알림 · 고친 뒤 다시 잰다 (`disabled` = `code_changed` 또는 machine-id 못 읽음 포함) |
| 멈춤 (rc 2 · S0 안 띄움) | PIN 자리표 · PROBE · TAG 꼴 · 새 폴더 넷 중 있는 것 · venv · 킷 · BASE 비 git · 끝 표지 없는 앞 로그 폴더 · fetch 실패 · PIN ≠ fetch 뒤 끝 · worktree 실패 · HEAD ≠ PIN · 더러움 · `cjunc_store.py` 없음 · md5 둘 · 감시 셸 30 s |
| 쓰는 자리 | 새 로그 폴더 · 새 S0 출력 폴더 · 새 저장본 폴더 (재기 전용 · 단계 1 문턱 (s_min None) 이 R 과 달라 R 은 그 파일을 읽지 않는다) · tgz (+ sha256) · BASE 의 FETCH_HEAD · 원격 추적 ref · worktree 관리 항목 · 핀 작업 트리 |

### 5-2. GPU 확인 다섯 짝 (kgy · GPU · 킷 · σ 없음 · 시간 상한 5,400 s)

생산 함수 `scripts/step3_sigma.py` `_solve_cg` 를 두 커밋에서 (`git show` 로 꺼낸 사본 · 옛 `11a794674` = A 꼴 sha256 `8d428ff5…` · 새 = 코드 핀 C 꼴 `859310da…`) 같은 합성 SPD 계 (298³ = 26,463,592 미지수 · 그래프 라플라시안 + 판 결합 · 전도도 10^−1..10^1 · 시드 20261112) 에 돌린다.

| 짝 | 정지 | 결과 전 기대 |
|---|---|---|
| 대조 옛 · 옛 | 200 반복 고정 (rtol 1e-300) | 해 바이트 · info · 반복 수 · LAST_BACKEND 같음 (이 기계 결정성) |
| 대조 새 · 새 | 200 반복 고정 | 같음 |
| 짧게 옛 · 새 | 200 반복 고정 | 같음 |
| 주 풀이 옛 · 새 | 0 에서 rtol 1e-12 (생산 정지) · 증서 켬 (callback) · maxiter 60,000 | 같음 |
| 이어 풀기 옛 · 새 | x0 = 옛 주 해 · rtol 1e-14 (증서 ⓒ 바닥) | 같음 |

+ 새 꼴이 반복당 빠름 (합성 벤치 A / C = 3.40 gabia · 3.79 kgy · `docs/reviews/rint2_time_reestimate_20261111/bench/results_20261112/README.md` 12–14 줄).  다르면 그대로 보고 (시험을 고치지 않는다).  관문 = 새 폴더 · 하네스 md5 `acfeb4b4…` · Q11PIN 40 hex · 두 커밋 있음 · 두 모듈 sha256 (하네스 175–176 줄) · venv.  쓰는 곳 = 새 폴더 하나 (두 모듈 사본 · CuPy 캐시 포함).  블록 자신은 fetch 하지 않는다 (머리 6 줄).  11-12 벤치 때 kgy GPU 에 다른 부하 (util 83–93 % · 같은 README 13–14 줄) · 지금 부하 = [미확인] → 반복당 시간 = 참고만 · 비트 같음 판정과 무관.  gabia 판 블록 (Q11REPO 자리) = [미확인].

### 5-3. ⑥ 시도 3 · 4 (2/2 · 도구 고침 먼저)

시도 3 = 저장본 켬 · 빗나감 (짓고 씀) · 시도 4 = 적중 — 기록 7 판 2 절 = ⬜ 1저자 결정 (가) 저장본 끔 그대로 · (나) 켬 두 줄 · 권고 (나) · 1저자가 (나) 를 골랐다 = 11-12 20:0x KST *"다 권고대로해줘"* (기록 = 진행 기록 `docs/session_20260923_progress.md` 11-13 [Rint ②] 줄).  명령 = 시도 2 줄 그대로 (한도 권고 1,500,000).  지금 도구로는 못 돈다 (§0) → 원장 줄 · 도구 고침 = 리뷰 핀 커밋 또는 그 뒤 (§9).

## 6. Codex 질문 (반증 가능한 꼴)

| # | 질문 |
|---|---|
| Q1 | **열쇠 — 코드.**  열쇠 코드 칸 = 넷 (find_spec 파일 sha256) ⊇ 원장 짓기가 실제로 부르는 프로젝트 파일 (T14a sys.setprofile · T14b import AST · T14c CE1).  같은 열쇠인데 다른 원장이 나오는 코드 변화 꼴이 있나 (동적 import · getattr · 부르는 쪽이 모듈 전역을 바꿈 · 낡은 .pyc = 한정 (다)). |
| Q2 | **열쇠 — 침대 · origin · s_min · 문턱 · 기계 · 환경.**  `key_parts` (580–587) 가 원장 비트를 정하는 입력을 다 덮나.  (a) 같은 기계 · 같은 venv 에서 원장 비트를 바꿀 수 있는데 열쇠 밖인 실행 env — `OPENBLAS_CORETYPE` · `NPY_DISABLE_CPU_FEATURES` · BLAS 스레드 (사슬 `env_record` 는 BLAS 경로 · OPENBLAS_CORETYPE · CPU 모델 · numpy SIMD 를 기록만 · `rint_r_chain.py:1072–1096`) · 원장 길 = `np.einsum` (`carbon_junction.py:247`) · `np.linalg.norm(axis=1)` (276 · 331 · 384 · 1100 · 1130 · 1179) · 1 차원 `np.linalg.norm` = BLAS dot (`fibre_segment_raster.py:76` · 173 · `cjunc_store.py` `env_paths_fp` 머리 글 428–430) · `cKDTree` (1003–1004 · 1129–1135 · 1178–1195) (b) machine-id 를 열쇠에 넣는 것 (못 읽음 = 꺼짐 · 복제 기계 (같은 id) 못 가림) 이 맞나 · 더 넣을 것 (CPU 모델 · numpy SIMD) 이 있나 (c) kgy · gabia 의 machine-id 유무 = [미확인] (S0 재기의 `store_machine_id_read` 가 kgy 를 잰다). |
| Q3 | **실패 길 처분.**  없음 → 지어 씀 · 못 읽음 → 다시 지음 + ⚠ · 어긋남 → 멈춤 · 쓰기 쪽 실패 → 기록만 · 읽기 MemoryError → 그대로 · 기계 id 못 읽음 · 런 도중 코드 바뀜 → 꺼짐 (`disabled`) · 열쇠 못 셈 (`Exception` 전부 · MemoryError 포함) → 그냥 짓기 (`key_unavailable` · `cjunc_store.py:761–766`).  CLAUDE.md "재개 규칙 지적 처분 기준" 꼴로 (a) 정직한 흐름 (끊긴 복사 · 디스크 · 권한 · 다른 파일계 · numpy 판 · 언어 로캘) 이 멈춤으로 가는 꼴 (거짓 멈춤) (b) 손으로 고친 · 어긋난 파일이 '다시 지음' 이나 '적중' 으로 가는 꼴이 있나. |
| Q4 | **동시 쓰기 · 발행.**  B4 의 단일 작성자 · EEXIST 대조 · 한정 (링크 수 안 봄 · 경로 기준 · 마지막 성분 · 공유 파일계 미검토) 이 R 운영 (기계마다 이 사용자만 쓰는 폴더 · 두 기계) 에서 틀린 결과로 이어지는 꼴이 있나 · 공유 파일계를 막아야 하나. |
| Q5 | **런 도중 코드 바뀜.**  `_START` (cjunc_store 를 처음 불러온 때) ↔ get_or_build 시작 · 발행 직전 (stat 신원 정확 · Store 칸 = 시작 칸).  한정 (가)–(마) (§8) 가 충분한가 · (마) 정직한 다시 씀 = 꺼짐이 R 동안 (git pull · checkout 없음 전제) 이득을 지울 만큼 잦을 꼴이 있나. |
| Q6 | **저장본 밖 독립 대조의 범위.**  저장본을 읽지 않는 봉인 원천 재조립 (B6) = SV 모서리 팔만.  사다리 · 비 SV 예측 · 단위 팔은 같은 코드 · 환경 결정성 + 열쇠 + 폴더 · 파일 권한에 기댄다 (자기 일관 위조는 저장본 혼자 못 가림 · 대조 길 = 1저자 결정 Q-A 열림 · 지금 한정 그대로 `cjunc_store.py:33–38`).  등록 R 판정에 이 한정을 받을 수 있나 · 아니면 봉인 전에 최소 대조 (예: S0 단계 2 원장 지문 ↔ DBE arm 0 · 저장본 팔 하나의 저장본 없는 재조립) 가 필요한가. |
| Q7 | **기록 · 합치기 · 재개.**  (a) 합치기 (`--merge` · 12 단위 · 두 기계) 가 켬 · 끔 섞인 단위를 받는가 (시험 없음) (b) 재개 (`ResumeRunner` 5750–5787 · 남은 payload 바이트 대조) 가 원 시도와 다른 `--cjunc-store` (켬 ↔ 끔 · 다른 폴더) 를 받는가 · 받는 것이 맞나 (c) 팔 기록에 저장본 상태가 없는 것 (RCP-07) 이 출처 요구 (어느 팔이 적중 원장으로 풀었나) 에 충분한가. |
| Q8 | **C 꼴 ↔ A 꼴 비트 같음 (부호 있는 0).**  논증 = C 는 `(1/diag) * r` 원소 곱 · A 는 dia → csc → csr 변환 뒤 CSR 곱 (+0 에서 시작하는 합) → 차이 = r 의 −0 칸뿐 · 생산 꼴 (b = 0 + 양수 · x0 = 0 또는 앞 해) 에서 r 에 −0 이 생기지 않음 (G4b · 가짜 산술).  (a) 실제 cuSPARSE / cupy CSR spMV 산술 (FMA · alpha · beta · cupy 판) 에서 이 논증의 빈틈 (b) matvec `lambda _r: _dinv * _r` (586–587) 은 (N, 1) 입력이면 브로드캐스트로 (N, N) 을 만들려 한다 (실침대면 메모리 오류 · 가짜 cupy 머리 글 (`test_step3_gpu_precond.py:89–91`) = cupyx `LinearOperator.matvec` 이 결과를 (N,) · (N, 1) 로 맞춘다 = 조용한 오답은 아니라고 본다 [추정 · 실제 cupy 소스 대조 안 함]) — cupy 12.3.0 cg 가 M 에 1-D 만 넘긴다는 가정에 기댄다 (c) 기록 `precond` 'jacobi' 그대로 = 런 기록으로는 A / C 를 코드 신원으로만 가른다 — 시간 표 · ⑥ 견줌에 충분한가. |
| Q9 | **끔 길 = 바탕 (B11).**  이것을 '저장본 끔 = 옛 결과 그대로' 의 증거로 받을 수 있나 · 빠진 길 (SV 반사실 켬 · face_alpha · 극한 런 · 사슬 단계 단위) 이 있나. |
| Q10 | **S0 감싸개가 S0 출력을 바꿀 수 있나.**  감싸개 = cjunc_store → carbon_junction 먼저 import · `CJ.cjunc_registry` 바꿔 끼움 · `runpy.run_path` · 같은 원장 객체를 돌려줌 · 실패 = 기록 · S0 계속 (BaseException 잡음 · KeyboardInterrupt 만 다시 올림).  (a) 출력을 바꿀 길 (import 차례 · sys.modules · 메모리 2 배 · SystemExit 삼킴 · 다른 신호 · 알려진 것 = S0 보고 `elapsed_s` 에 재기 초 · 감시 셸 rss.log 표본 최대에 재기 몫이 섞임 = 등록 README 한정 55–56 줄) (b) 공식 S0 다시를 감싸개로 (Q-B (가)) 받을 수 있나 (c) 픽스처 대조 (출력 같음) 가 2 회차 cjunc_store 에서만 돌았다 (§8) — E4 대조 (S0 계획 · 배열 = 11-08) 가 그 빈칸을 메우나 (d) T1–T3 · VmHWM 되돌림 자리 (§8) 가 판정에 쓸 만한가. |
| Q11 | **GPU 다섯 짝이 충분한가.**  (a) 합성 298³ · 전도도 대비 10² (log-uniform 10^−1..10^1) · 한 시드가 실침대 (26,529,223 미지수 · 대비는 합성보다 클 것 · 접합 간선으로 행 길이 고르지 않음 [둘 다 추정 · 잰 적 없음]) 의 A ↔ C 비트 같음을 받치나 (b) 실침대 대조를 결과 전 기대로 더할까 — ⑥ 시도 3 · 4 (C 꼴 · 같은 kgy · 같은 명령) 의 주 풀이 · 이어 풀기 반복 수 · 잔차 · 판 전류 불균형 = 시도 2 (A 꼴 · 277,885 · 84,485 · 1.0519e-12 · 9.63612e-07) 와 같음 · 시도 3 = 시도 4 (두 핀 `5bca50c88` ↔ `56f4cfbb1` 사이 풀이 경로 코드 차이 = 이 묶음 + 풀이 밖 믹서 둘 · 같은 기계 실침대 결정성은 [미확인]) (c) gabia 에서도 돌려야 하나. |
| Q12 | **두 기계 조립 비트 같음 (1저자 11-12 Q10).**  SBE 킷 조립만 런 (풀이 · σ 없음 · `cjunc_graph_only_record`) 을 kgy · gabia 에서 한 번씩 돌려 가중 그래프 지문을 견주려 한다.  이것이 개발 탐침 원장 §2 · Q9 §3-5 의 '원장 밖 킷 풀이 금지' 에 걸리나 · 원장 줄을 먼저 커밋해야 하나 · 견줄 칸으로 충분한가.  (저장본은 기계마다 따로라 이 대조와 무관하다고 본다 — 맞나.) |
| Q13 | **git 환경 격리.**  (a) 남긴 `GIT_*` 가운데 생산 읽기 (payload code_sha · 사슬 git_identity · F5 · 원장 커밋 · S0 git_head) 를 다른 객체로 돌리는 이름 (`GIT_REPLACE_REF_BASE` · `GIT_NO_REPLACE_OBJECTS` · `GIT_GRAFT_FILE` · `GIT_SHALLOW_FILE` · `GIT_QUARANTINE_PATH` …) 이 정직한 흐름 (훅 · 래퍼) 에서 들어오나 (b) 반대로 설정 주입 (`GIT_CONFIG_COUNT` · `KEY_n` · `VALUE_n`) 을 지워서 정직한 흐름이 거짓 멈춤하는 꼴 — 부르는 쪽이 env 로 넣은 `safe.directory` 가 사라져 git 읽기 실패 → 코드 신원 None (이 컨테이너도 env 로 git 설정 셋을 넣는다 — 키 = `credential.interactive` · `url.<…>.insteadOf` 둘 · 로컬 읽기와 무관한 키) (c) GPU · ⑥ 블록에 셸 꼴이 없는 것 (한정 (차)) 을 받을 수 있나. |
| Q14 | **순서.**  1/2 판정이 HOLD 면 2/2 (측정 값 · 봉인 숫자) 를 그 고침 뒤로 미뤄야 하나, 아니면 이미 시작한 S0 다시와 다음 측정을 개발 자료로 두고 2/2 에서 함께 볼 수 있나 (고침이 S0 일곱 · 열쇠 코드 칸 · `_solve_cg` 를 건드리면 다시 잰다). |

## 7. 다시 돌리는 법 · 우리 다시 돌림

리포 뿌리 · 깨끗한 트리 · 원격 핀 체크아웃 (Q11 시험은 `git show 11a794674:…` 를 부른다 — ZIP 만으로는 안 돈다):

    python3 scripts/test_step3_gpu_precond.py          # 가짜 cupy · 수 초
    python3 scripts/test_git_env_isolation.py          # 일회용 저장소 · 약 20 s
    python3 scripts/test_cjunc_store.py                # 약 90 s ·  --only T15,P = 빠른 부분
    python3 scripts/test_cjunc_store_e2e.py            # 실제 러너 · 사슬 · CPU · 기록 412 s (kgy 판) · 511 s (3.11)
    bash scripts/check_kgy_py38.sh                     # kgy 판 (uv CPython 3.8 · numpy 1.24.4 · scipy 1.10.1) 17 묶음

| 시험 (코드 핀 `56f4cfbb1` · 2026-11-13 · Python 3.11.18 · numpy 2.4.6 · scipy 1.17.1 · git 2.43.0 · 전 · 뒤 작업 트리 깨끗) | 결과 | 초 |
|---|---|---|
| `scripts/test_step3_gpu_precond.py` | 19/19 PASS | 2 |
| `scripts/test_git_env_isolation.py` | 19 PASS · 0 FAIL | 19 |
| `scripts/test_cjunc_store.py` | 70 PASS · 0 FAIL | 94 |

로그 = ZIP `extra/runs_56f4cfbb1/`.  무거운 시험 (e2e · e2e12 · 사슬 · 증서 · kgy 판) 은 다시 돌리지 않았다 — 기록 = 기록 묶음 `logs_r5/` (py311/_summary.txt · HEAD 0db6dee6d (작업 트리 커밋 · 원격에 없음) = `27ef82d24` 의 작업 트리 · 그 뒤 `8ace86a82` = 시험 두 파일만 · 3.11 = 사슬 506/506 · e2e 51 · e2e12 33 · conv_cert 30/30 · 저장본 e2e 6/6 · probe6 330 · b6 502 · 러너 151 · 계약 125 · 규율 selftest 128 · repo 0 오류 (17 경고) · undef 2 건 = 묶음 밖 기존 `generate_comparison_plots.py` 6905 · 6906 (`a0455e90b` 에도 같은 줄) · 그 판의 저장본 시험 = 67 PASS · 1 FAIL (T8) → 8b59b9618 (작업 트리 커밋 · 원격에 없음) 에서 70/70 · `mutfix/`).

관찰 (우리 다시 돌림 · 판정 무관): `test_step3_gpu_precond.py` `load_base` (70–75) 가 기반 모듈 사본 임시 폴더 `s3base_gp_*` (사본 + .pyc · 약 0.8 MB) 를 지우지 않는다 — 게이트마다 TMPDIR 에 하나씩 남는다.  우리 다시 돌림은 무시 파일 `scripts/__pycache__/*.pyc` 를 만들었다 (`.gitignore:2` · `git status --porcelain` 0 줄).

## 8. 한정 (알려진 것 — 새 결함으로 다시 세지 말고 받을 수 있는지만)

- **런 시작 코드 칸 (가)–(마)** — (가) cjunc_store 보다 먼저 열쇠 모듈을 부르는 쪽 (시험 · 손 실행) 의 import 전 바뀜 = 못 가림 (`preloaded` 에 적힘 · payload 두 꼴 · S0 감싸개 = 그런 모듈 없음 · P6 · P6b) (나) 시스템 시계를 되돌리고 같은 inode · 크기 · 시각으로 다시 쓰기 = 못 가림 (다) 낡은 .pyc (라) 같은 프로세스 안 함수 바꿔 끼우기 (마) 정직한 다시 씀 (git checkout · touch · cp -p · rsync) = 그 런은 꺼짐 (보수 · 미래 수정 시각 정직한 런 = 켜짐 · T15j).
- **git 환경 (바)–(파)** (기록 7 판 `amend_drafts.md` 0-f 101–112 줄) — (바) 지우는 목록 밖 `GIT_*` 는 남는다 (QUARANTINE_PATH · 대체 ref · graft · shallow · 신원 AUTHOR · COMMITTER …) · 원장 고정 신원을 부르는 쪽 AUTHOR · COMMITTER 가 덮을 수 있다 (사슬은 author 를 안 봄) (사) 생산 git 은 부르는 쪽 전역 · 시스템 설정을 따른다 (고정물 env 는 시험만) (아) 천장 없는 git 아닌 사본 = 바깥 저장소 HEAD 를 적는다 (옛 판과 같음) (자) `check_review_findings._commit_exists` 는 부르는 쪽 env (게이트 = 머리 셸 꼴이 지움) (차) GPU 확인 · ⑥ 블록에 셸 꼴 없음 (카) 시험 G6 · G7e 목록 = 손 목록 (이 묶음 밖 시험 안 봄 · G6 여덟에 `test_step3_gpu_precond` 없음 = G4 가 봄) · G7e = 정적 (타) kgy git 판 [미확인] (`GIT_CONFIG_GLOBAL` = git ≥ 2.32 · 옛 git 이면 HOME 끊기가 대신) · 셸 꼴 = bash 전용 (파) 시험 T8 '다른 코드' 의 뜻이 바뀜 (Store 칸만 바꾼 꼴 = 이제 꺼짐 · 다른 코드 = 다른 열쇠는 T4 · T14c · T15a).
- **독립 대조 · 기록** — B6 의 범위 (SV 모서리 팔만 · Q6) · 저장본 상태 = 화면 한 줄 + 요약 `cjunc_store: true` 뿐 (RCP-07) · 합치기 미시험.
- **감싸개** — 픽스처 대조 (있음 ↔ 없음 출력 같음 · 3.11 · 3.8.20 · `extra/wrapper_fixture_round2_code/`) 는 cjunc_store sha256 `e175d475…` (2 회차) 에서 돌았다 · 끝 핀 `5468e68d…` (3 회차 = stat 신원 · Store 칸 대조 · ca_ext_cjunc import 차례) 에서는 다시 돌지 않았다 [미확인] · 감싸개 머리 글 "VmHWM 은 ② 앞에 되돌린다" (등록 블록 79 줄) ↔ 코드 = ① (`encode_strict`) 앞에서 되돌림 (`_reset_hwm` 165 줄 · `encode_strict` 168 줄) → 기록 VmHWM 은 ①–④ 를 덮는다 (T2 를 ②–④ 보다 크거나 같게 잼 = 보수 쪽) · 등록 README E2 근거 칸 "S0 일곱 가운데 바뀐 것 = 둘" ↔ 3 회차 뒤 셋 (`ca_s0_census.py` `_git` · `27ef82d24`) — 기대값 무관 · 등록 README "PIN 한 줄만 채운다" ↔ 이번 사본 = PIN · BR 두 줄 (§5-1 · 기록 = 본 세션 §9).
- **kgy 판 17 묶음** = 0db6dee6d (작업 트리 커밋 · 원격에 없음) (작업 트리 · 코드 = 끝과 같음) 에서 16 ✓ + `cjunc_store` ✗ (T8 한 줄) → 8b59b9618 (작업 트리 커밋 · 원격에 없음) (시험만 바뀜) 에서 `cjunc_store` 70/70 · `git_env` 19/19 다시 — 17 묶음을 한 번에 돈 기록은 아니다.
- **GPU 블록 7 판 (4-f)** — 셸 관문 모의 (가짜 HOME · cupy 없음 → rc 1) 만 · CPU 흐름 (`--backend numpy` · n-side 24 · 다섯 짝 비트 같음 · 주 풀이 267 · 이어 37) 은 5 판까지 (하네스 · 두 모듈 바이트 같음) · GPU 길 = [미확인].
- **실기계 [미확인]** — 실침대 원장의 저장 꼴 · 시간 · 메모리 (S0 재기 대기) · GPU 비트 같음 · kgy · gabia machine-id · kgy 총 메모리 · 기계 사이 원장 지문 결정성 · gabia Q11REPO.
- **S0 재기 = 보수 어림** — 단계 1 원장 (s_min None) 은 R 팔 원장 (봉인 s_min) 보다 instance 가 같거나 많다.
- **결과 0 건** — σ · 판정 · R 런 없음.

## 9. 리뷰 핀 커밋에서 채운 것 (11-13 · 발송 전)

- 리뷰 핀 = 이 요청서가 든 커밋 (ZIP `PIN.txt`) · ZIP sha256 = 발송 메시지에 적는다 (ZIP 이 자기 sha 를 담을 수 없다).
- 세션 메모 표지 셋 (S0 시작 시각 · ⑥ 시도 3 · 4 저장본 켬 = (나) · `56f4cfbb1` 게이트 출력) = 진행 기록 `docs/session_20260923_progress.md` 11-13 [Rint ②] 줄 로 옮김.
- 등록 README (`docs/reviews/rint2_s0_store_probe_20261112/README.md`) 정정 표지 둘 (E2 근거 '둘' → 셋 · '한 줄만 채운다' → 이번 실행 두 줄 PIN · BR) + 11-13 실행 기록 절 = 이 커밋.
- ⑥ 시도 3 · 4 의 도구 고침 · 원장 줄 = 이 커밋에 넣지 않음 (2/2 · 따로 시험 먼저) → 코드 핀 ↔ 리뷰 핀 사이 코드 바뀜 없음 (extra/code_diff_codepin_to_pin.txt = 빈 파일).
- 감싸개 픽스처의 끝 핀 재실행 = 하지 않음 (§8 한정 그대로 · 실침대 S0 의 E4 를 2/2 에서 본다).
