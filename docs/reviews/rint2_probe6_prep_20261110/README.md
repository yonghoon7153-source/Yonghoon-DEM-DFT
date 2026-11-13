# Rint ② 개발 탐침 ⑥ (SBE 수치 탐침 · σ 봉인) 준비물

작성 2026-11-10 (작업 트리 에이전트) · 같은 날 내부 반박 리뷰 (P6R-01–12) 고침 + 두 시도 (1저자 11-10) · 같은 날 내부 반박 리뷰 2 회차 (P6R2-01–08 · Codex 아님) 고침 (1저자 11-10 Q1 · Q2 (가) · Q3 · 원장 §3 글도 같이). 결과 0 건. kgy 실행 0 건. 이 폴더는 도구와 기록뿐이고 러너 · payload · step3 · 사슬 · 등록 R 은 고치지 않았다.

## 1. 무엇을 왜

- ⑥ 은 실침대 SBE 에서 반복 수 · 잔차 · 판 전류 불균형 · 시간 · 메모리를 재는 탐침이다. σ 는 봉인 파일 (팔 JSON) 에만 남기고 화면 · 로그 요약 · 보고에 내지 않는다 (원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` §1 · §2, 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §11 ⑥).
- 쓰는 곳은 R 런 계획의 전처리 · maxiter · 시간 상한 숫자와 시간 결정점 (등록 R §10-4 결과 전 문장 1) 뿐이다.
- 시도는 둘이다 (1저자 11-10): 시도 1 = 짧은 확인 (한도 30000 · 한도에 닿아 끝나는 것이 정상 · 반복당 초와 한도에서의 잔차를 얻고 kgy 에서 전 과정을 한 번 확인) → 시도 2 = 본 한도 1500000 (§6).
- 러너 화면에는 반복 수가 없고, 판 전류 불균형은 수렴 증서가 실패할 때의 줄에만 찍힌다 (§5). 두 값은 팔 JSON 안에 있고 팔 JSON 에는 σ 도 있다. 그래서 사람이 파일을 여는 대신 닫힌 허용 칸만 꺼내는 판독기를 둔다.
- 1저자가 할 일은 시도마다 블록 하나를 붙이고 끝난 뒤 묶음 파일 하나를 보내는 것이다.

## 2. 파일

| 파일 | 무엇 |
|---|---|
| `KGY_BLOCK.md` | 1저자가 kgy 에 붙일 블록 하나 (ASCII · `<PIN>` 자리 하나 · `ATTEMPT=1` 줄 하나) 와 화면에 나오는 것 / 안 나오는 것 · 멈추는 조건 · 끝 표지 |
| `LEDGER_LINE.md` | 원장 §3 시도 표에 넣을 줄 초안 (시도 1 · 시도 2 · 명령 줄 넷 · 자리표 값의 근거) |
| `tools/run_probe6.sh` | kgy 감시 셸 (ASCII · bash). 블록이 nohup 으로 띄운다 |
| `tools/probe6_read.py` | σ 비열람 판독기 (ASCII · 표준 라이브러리 · Python 3.8) |
| `tools/test_probe6_read.py` | 시험 (게이트 단계 `rint probe6 reader` · kgy 판 게이트 `scripts/check_kgy_py38.sh` 의 `probe6`) |

## 3. 원장 §2 규칙 일곱 칸과 준비물

| 칸 | 지키는 자리 | 기계가 막는가 |
|---|---|---|
| 허용 입력 (SBE 새 침대만 · DBE 금지) | 감시 셸은 킷 이름을 인자로 받지 않는다 (`KITS=kit_SBE_vgcf100` 고정). 킷 런 폴더 이름이 채택된 S0 단계 1 계획의 run_dir_name 과 다르면 러너를 띄우지 않는다. 판독기는 팔의 입력 지문 6 개 (sha256 앞 16 자리) 를 그 계획의 inputs_sha256 과 대조하고 (로그 폴더 · S0 계획이 있으면 증거가 없어도 PROBE_OK 아님), 이름에 DBE 가 든 팔은 읽지 않고 rc 5 를 낸다 | 예 (시험 F08 · T08b · T16a · T21 · R2b · R2e) |
| 핀 | 블록이 fetch 뒤 PIN = 가지 끝인지 보고 핀 작업 트리를 만든다. 감시 셸이 HEAD = 핀 · 트리 깨끗함 (추적 안 된 파일 포함) · 자기 자신이 그 트리 안의 사본인지를 본다. 판독기는 팔의 code_sha 가 핀의 앞자리인지 본다 (없음 = PROBE_OK 아님). 묶음 meta 에 핀과 도구 sha256 | 예 (F08 · B02 · T16c · T21 · R2b) |
| 기계 / 환경 | 감시 셸이 환경 지문을 적는다: python · numpy · scipy · cupy · CUDA 런타임 · BLAS 이름과 계산 경로 · GPU 이름 · 드라이버 · CUDA 판 · 커널 · OS · CPU · 메모리 · git · bash. meta 에 env 이름 여섯 (`CUDA_VISIBLE_DEVICES` · `OMP_NUM_THREADS` · `OPENBLAS_NUM_THREADS` · `OPENBLAS_CORETYPE` · `PYTHONUNBUFFERED` · `BASH_ENV`) 의 있음 / 없음 (값은 숫자 · 짧은 이름일 때만 · 감시 셸 자신의 env = 부르는 셸의 것 · 러너는 `env -u BASH_ENV -u SHELLOPTS` 로 BASH_ENV 를 받지 않는다) 과 발사 전 GPU 사용량 · 디스크 여유. PYTHONPATH 는 감시 셸이 venv 활성화 뒤 python 을 처음 부르기 전에 걷어낸다 (meta `pythonpath_removed` · 러너 시작 때 남았으면 `pythonpath_set=1` = 판독기 rc 4). 판만 적고 호스트 이름 · 주소 · 계정은 적지 않는다 (폴더는 홈을 `~` 로 접는다) | 기록 (F04 · F06) · PYTHONPATH · BASH_ENV · SHELLOPTS 걷기는 예 (F02f · F21 · T28 · T29) |
| 시도 (한 줄 · 시작 전 커밋 · 고르지 않는다) | `LEDGER_LINE.md` 가 두 줄 초안. 시도 번호는 블록의 `ATTEMPT` 줄 하나로 정하고 한도는 블록 안의 표에서 나온다 (1 → 30000 · 2 → 1500000 · 감시 셸 · 판독기도 이 짝을 본다). 폴더 이름에 시도 번호가 들고 (감시 셸이 출력 · 로그 폴더의 번호가 같은지 본다) meta · 보고에 적힌다. 시도 2 는 풀이를 시작한 시도 1 (`solve_started=1`) 의 DONE 뒤에만 블록 · 감시 셸이 띄우고 (그런 시도 1 폴더가 정확히 하나), 두 핀 사이에 풀이 코드 (§9 목록) 가 같아야 한다. 끝난 시도 번호 (`DONE` + `solve_started=1` · `WATCHER_FAILED` + 러너 시작 줄) 는 다시 띄우지 않고 시도 1 은 끝난 시도 2 뒤에 띄우지 않는다. 실제로 돈 명령은 묶음의 command.txt 에 남는다. 비어 있지 않은 출력 폴더 · 새것이 아닌 로그 폴더 · 홈 바로 밑이 아닌 로그 폴더 · 앞 로그 폴더에 끝 표지 없음 · 같은 계정의 러너 / payload 가 돌고 있음 · 감시 셸 잠금 (`~/.probe6.lock`) 이 있음 = 멈춤 | 폴더 · 번호 · 짝 · 앞 시도 · 풀이 코드 · 동시 실행은 예 (F08 · F19 · F20 · B02 · B06 · B11–B14 · T26 · T27). 줄을 먼저 커밋하는 것은 사람 |
| 실패 보존 | 감시 셸은 아무것도 지우거나 덮지 않는다. 러너가 실패하거나 한도에 닿아도 보고와 묶음을 만들고 DONE 을 쓴다. 러너가 킷 런 폴더에 쓰는 파일 (생성 스크립트 · time 기록 · 받아들이지 않은 팔 JSON) 은 같은 이름이면 다음 시도에 덮이므로, 감시 셸이 시작 전 것은 로그 폴더의 kit_run_before 로, 이번 시도 것은 kit_run_new 로 바이트 사본을 둔다. 판독기는 출력 폴더의 요약 sha256 둘과 남은 파일의 sha256 을 낸다 | 예 (F09 · B05 · B07 · R3d · R5b) |
| σ 비열람 | 러너의 화면 출력은 전부 로그 폴더의 runner.log 로만 간다 (stdout · stderr 둘 다). 판독기는 맨 위 닫힌 표의 칸만 낸다. 로그 줄은 옮기지 않고, 아는 줄은 읽은 수로 다시 적고, 실패 줄은 수를 `#` 로 가린다. 묶음에는 팔 JSON · 영수증 · runner.log 가 없다 | 예 (T02 · T11 · T15 · T23 · F01 · B09 · R1f · R2c · R3c · 판독기 변이 76) |
| 채택 불가 | 판독기 보고에는 σ · 전류 · 구간이 없어 R 판정 · 보정 · 예측 값으로 쓸 재료가 없다. 붙잡아 둔 상대 칸 넷은 이름만 낸다 | 일부 (값이 보고에 없다는 것까지) |

## 4. 판독기가 읽는 칸 (실제 파일 · 키)

출력 폴더의 팔 파일 하나 (`p2_SBE_vgcf100_sph_fa_cj1000000_78c44437_c0_rt1em12_fb10000_a0.json` · 이 컨테이너에서 같은 축으로 실제 러너를 돌려 확인한 이름) 의 `mpm_metrics.step3` 아래:

| 무엇 | 키 | 쓰는 코드 |
|---|---|---|
| 반복 수 (주 풀이) | `cg_iters` · `conv_cert.iters` | `scripts/step3_sigma.py` 504 · 2355 · 2391 행, `scripts/mpm_webapp_payload.py` 2631 행 |
| 반복 수 (ⓒ 이어 풀기) | `conv_cert.resolve_iters` · `conv_cert.resolve_info` | `scripts/step3_sigma.py` 2356 행 |
| 잔차 | `cg_resid` · `conv_cert.resid` | `scripts/mpm_webapp_payload.py` 2598 행 |
| 판 전류 불균형 | `conv_cert.imbalance` | `scripts/step3_conv_cert.py` 의 `_certify_abc` |
| 수렴 여부 | `cg_info` · `unconverged` · `conv_cert.status` · `ok` · `pass_a`–`pass_d` · `manifest.components.electronic.status` | 같은 파일들 |
| 미지수 수 | `n_dof` | `scripts/mpm_webapp_payload.py` 2595 행 |
| 백엔드 | `manifest.backend_last_solve` 의 requested · used · precond · rtol, `manifest.components.electronic.backend.used` (미수렴 팔에는 이 칸이 없다 · 실물 확인) | `scripts/mpm_webapp_payload.py` 3648 행 |
| 신원 | `manifest.physics_protocol_id` · `code_sha` · `input_digest` · `input_files` (S0 계획과 대조만) · `origin_shift_um` (0 인지만) | `scripts/mpm_webapp_payload.py` 2151–2164 · 3545 · 3546 행 |

- 영수증 (출력 폴더의 run_receipt.json): receipt_digest · code_sha · arms · expect_backend · step3_rtol · vox_um · ptfe_stamp 와 파일 sha256.
- 로그 (runner.log · 다시 적은 꼴): STEP3 풀이 시작 줄의 dof · 판 접점 수 · 백엔드, 결과 줄의 dof · 잔차 · STEP3 경과 초 (값 자리가 봉인 표지인지 확인), maxiter · rtol 줄, face_alpha · 접합 준비 초, 러너의 팔 최대 RSS 줄, 미수렴 줄 (info · 잔차), 증서 실패 줄 (상태 · ⓐⓑⓒⓓ · 불균형).
- 시간: 감시 셸이 잰 전체 초와 러너 종료 코드. 표본 (기본 10 초 간격) 에 로그 줄 수를 같이 적어 "풀이 시작 줄 → 결과 줄" 사이의 초 (주 풀이 + 증서) 를 표본 간격 정밀도로 낸다. 반복당 초 = 그 구간 / (주 반복 + 이어 풀기 반복) 은 위 한계다 (ⓓ 증서의 CPU 계산이 들어 있다). 결과 줄 없이 끝난 시도 (일찍 멈춤 · 한도 뒤 멈춤) 는 "풀이 시작 줄 → 끝 시각" 초를 `solve_to_end_s` 로 따로 낸다.
- 메모리: 러너 프로세스 그룹의 RSS 합과 가장 큰 한 프로세스의 표본 최대, `/usr/bin/time -v` 가 있으면 그 값, 러너가 팔마다 남기는 time 기록, GPU 메모리 표본 최대 (전체 · 우리 프로세스 몫).
- 붙잡아 둔 칸 (이름만 내고 값은 안 낸다): `conv_cert.dsigma_rel` · `target_err_bound_rel` · `target_width_rel` · `target_in_bracket`. σ 가 아닌 상대 수렴 진단이지만 원장의 "읽는 것" 목록 밖이라 뺐다 (§9 정할 것 2).
- PROBE_OK 조건 (로그 폴더가 있을 때 · P6R-06 · P6R2-03 · 04 · 05): 수렴 표지 전부 · 반복 수 둘이 같음 · origin 0 · 같은 침대 · tol_ff · 핀 대조 셋이 True (로그 폴더 + S0 계획이 있으면 증거 없음도 PROBE_OK 아님) · 등록 R_j 대조 True (`rj_matches_registered` = 영수증 `ca_ext_request.cjunc.R_j_ohm` = meta `expect_rj` (1e6) · 팔 이름에 `_cj1000000_`) · 영수증 `arms` = 1 (없음도 아님) · 러너가 받아들인 팔 · 러너 rc 0 · 캐시 아님 · 결과 줄 있음 · 풀이 백엔드 = 영수증 기대 = meta 기대 (gpu) · 영수증 · 증서 rtol = meta 기대 (1e-12) · 로그의 CG maxiter = meta maxiter · meta 의 시도 번호 ↔ 한도 = 등록 짝 (1 → 30000 · 2 → 1500000) · 시도 2 면 meta `attempt1_pin` 있음 · `code_same_as_attempt1=1` (시도 1 이면 그 둘이 없음) · meta 의 aborted 0 · cap_term 0 · git_lines_after 0 · orphans 0 · kit_run_matches_s0 1 · solve_started 1 · pythonpath_set 0. 기대값은 감시 셸이 자기가 넣은 값을 meta 에 적은 것이다.
- 미수렴 (rc 3 · 시도 1 의 정상 끝) 에도 같은 신원 · 등록 값 · 기록 대조를 건다 (P6R2-05): 침대 · tol_ff · 핀 · R_j · 영수증 arms · 로그 maxiter = meta · 짝 · 시도 2 칸 · 영수증 rtol · 영수증 백엔드 · meta 의 깨끗함 (aborted · cap_term · git_lines_after · orphans · kit_run_matches_s0 · solve_started · pythonpath_set) 과 앞의 기록 문제 (모르는 파일 · 영수증 없음 · meta 못 읽음 …) 가 하나라도 어긋나면 rc 4. 미수렴 팔에 없을 수 있는 칸 (증서 rtol · 풀이 백엔드) 은 있을 때만 대조한다 (있는데 다르면 rc 4). rc 0 에만 거는 것 = 러너 rc 0 · 출력 폴더의 팔 · 결과 줄 · 반복 수 둘 같음 · origin 0 · 성분 백엔드.
- 반환 코드: 0 PROBE_OK · 3 미수렴 (반복 수는 그대로 보고 · 잔차 · 불균형이 null 이어도 팔이 미수렴이라고 말하면 3 · 위 대조가 다 맞을 때만) · 4 빠졌거나 꼴이 다름 (그 칸 = NONE + 사유 · 보고 파일을 못 쓰면 화면 표 + `READER_CRASH` 줄 + rc 4) · 5 거부 (거부 표지 · DBE 팔 · 로그의 봉인 깨짐 · 결과 줄 꼴이 바뀌어 봉인 표지가 없는 것 포함) · 2 인자.
- 가린 실패 줄: 앞 30 줄 + 뒤 30 줄 (가운데 버린 수 = `masked_lines_dropped` · 화면에도). 가림 = ASCII 숫자 · 전각 숫자 · 위 / 아래 첨자 · hex float 를 `#` 하나로.

새로 내는 수 (11-10 고침) 마다 그 수로 σ 를 되짚을 수 없는 까닭:

- `not_converged_info` · `not_converged_resid` (payload 의 "CG not converged (info=…, resid=…)" 줄): info 는 멈춘 반복 수 (= 한도) 라 셈 값이고, resid 는 상대 잔차 ‖r‖/‖b‖ 라 오차의 비율이다. σ 는 판 전류 (해의 적분 · 절대 크기) 가 있어야 나오는데 두 수에는 해의 크기가 없다.
- `solve_to_end_s` (풀이 시작 표본 → 끝 시각): 두 사건 사이의 초다. 해의 값과 무관하다.
- `masked_lines_dropped`: 버린 가린 줄의 수 (줄 셈).
- `gpu_used_start_mib` · `disk_free_gb_kit` · `disk_free_gb_log`: 발사 전 GPU 메모리 사용량 · 디스크 여유 (기계 상태 · 풀이 전).
- `orphans` · `orphans_left`: 러너가 끝난 뒤 그 프로세스 그룹에 남은 프로세스 수 (셈).
- `env_<이름>` 여섯 (`unset` · `empty` · `set` · `value:<짧은 값>`): 설정 이름의 있음 / 없음 · 스레드 수 · GPU 번호 · BLAS 계산 경로 이름. 결과가 아니다.
- `attempt` · `expect_rtol` · `expect_backend` · `solve_started` · `pregate`: 시도 번호 · 감시 셸이 넣은 등록 값 · 표지 (0 / 1).
- (2 회차 고침) `attempt1_pin` · `code_same_as_attempt1` (시도 2 만): 시도 1 폴더 meta 의 핀 (커밋 번호) · 두 핀 사이에 풀이 코드가 같다는 표지 (1). 코드 판의 식별자이지 풀이 값이 아니다. `expect_rj`: 감시 셸이 넣은 등록 접합 저항 (1e6 Ω · 입력 값이지 결과가 아니다). `pythonpath_removed`: 부르는 셸에 PYTHONPATH 가 있어 걷었는지 (0 / 1). `rj_matches_registered` (보고 fields): 영수증 · 팔 이름의 R_j 가 그 등록 값인지 (참 / 거짓). 다섯 다 셈 · 표지 · 입력 식별자라 해의 크기가 없다 (σ 를 되짚을 수 없다).
- (11-13 · 시도 3 · 4 = 탄소 접합 원장 저장본 켬) `attempt2_pin` (시도 3) · `attempt3_pin` · `code_same_as_attempt3` (시도 4): 앞 시도 폴더 meta 의 핀 · 풀이 코드 같음 표지 (코드 판의 식별자).  `store` · `store_listing_before` · `store_listing_after`: 저장본 폴더 (홈을 ~ 로 접은 꼴) · 들어 있는 파일 이름 (`cjreg_<열쇠>.npz`) 과 sha256: 원장 파일의 신원이다 (원장 = 풀이 전 기하 · 접합 목록 · 풀이 결과 σ 를 담지 않는다).  보고 `store` 블록 (`audit_file` · `audit_sha256` · `status` · `key` · `file` · `file_sha256`): audit 곁 파일의 신원 글과 상태 이름뿐 (곁 파일의 초 · 바이트 수 · 실행 환경은 옮기지 않는다).

## 5. 러너가 화면 · 로그에 σ 를 찍는가 (코드에서 확인)

- 결과 σ 는 기본이 가림이다. payload 는 `--show-results` 가 없으면 σ 자리에 봉인 표지를 찍는다: `scripts/mpm_webapp_payload.py` 1097–1103 행 (규칙) · 1154–1162 행 (`_blind` · `_sig_str`) · 2716–2720 행 (σ_e 결과 줄) · 2757–2766 행 (집전체 시나리오 줄). dof · 잔차 · 초는 가리지 않는다. 감시 셸은 킷 payload 줄에 `--show-results` 가 있으면 러너를 띄우지 않는다 (러너는 킷의 기본 명령을 이어 쓴다).
- 러너는 킷이 SDCP 기본 둘이 아니면 봉인도 원값 덤프도 돌리지 않는다: `scripts/sdcp_gain_vox015_8arm.sh` 1007–1011 행. 원값 표를 찍는 가지 (1051–1055 행) 는 기본 킷 + 팔 수가 8 이 아닐 때만이라 `KITS=kit_SBE_vgcf100` 에서는 닿지 않는다.
- 이 컨테이너에서 같은 축으로 실제 러너와 실제 payload 를 픽스처 킷에 돌려 확인했다 (시험 R1b · R1c · R2c): 화면에 봉인 표지가 있고, 팔 JSON 의 σ 류 수가 러너 로그에 없다 (유효숫자 7 자리 이상 소수로 찾음 · 양성 대조 포함).
- 그래도 runner.log 에 수가 남는 자리가 있다 (내부 반박 리뷰가 더 찾았다 · P6R-11 4). 입력 σ_VGCF 가 찍힌다 (러너 779 · 902 행 · 등록 값 1e4 에서 직경 보존으로 나온 입력이지 결과가 아니다). 실패 경로에서는 러너의 팔 검사 사유가 찍히는데 (러너 951–959 행), σ 가 유한한 양수가 아닐 때 그 값이 사유 글에 들어가고 (`scripts/run_contract.py` 1783 행), 증서 결속 사유 `CERT|sigma|` · `CERT|d|` 에 σ · 게시 판 전류 · scale 이 들어간다 (`scripts/run_contract.py` 906 · 913 행). 미수렴 때 증서 실패 줄에는 상대 Δσ 와 ⓓ 의 목표량 구간 (lo · hi) 이 찍히고 (`scripts/step3_sigma.py` 2363–2365 행 · `scripts/step3_conv_cert.py` 601–613 행의 `target_why` 는 게시 판 전류 G 도 찍는다), 증서 실패 줄과 미수렴 줄에는 판 전류 불균형 · 상대 잔차가 찍힌다.
- 그래서 묶음에는 runner.log 원본을 넣지 않는다. 판독기가 아는 줄은 읽은 수 (dof · 잔차 · 초 · 한도 · 불균형 · 통과 표지) 로 다시 적고, 그 밖의 실패 줄은 수를 `#` 로 가린 꼴만 보고 · 걸러 낸 로그에 넣는다 (시험 T12 · T22 · T23 · R3c). runner.log 는 로그 폴더에 그대로 두고 sha256 만 meta 에 적는다.
- 반복 수는 러너 화면에 없다 (팔 JSON 에만 · §4). kgy 명령 문서 `docs/reviews/rint2_kgy_commands_20261020.md` §2-2b 의 "러너 화면의 반복 수 · 판 전류 불균형 줄" 은 화면이 아니라 이 판독기의 표로 읽어야 한다.

## 6. maxiter: 두 시도와 근거

결정: 시도 1 = 30000 (1저자 11-10 · 짧은 확인) → 시도 2 = 1500000 (본 세션 11-10 · 조수 제안 400000 에서). 블록의 표 · 원장 줄 초안이 이 두 값이다 (시험 S04e · S05 가 대조한다). 감시 셸 (다른 짝 = 띄우기 전 STOP) 과 판독기 (meta 의 짝이 다름 = rc 4) 도 이 짝을 본다 (2 회차 P6R2-04 · 원장의 감시 셸 줄을 손으로 불러도 어긋나지 않게 · 시험 F08 · T26).

- 시도 1 의 뜻: 30000 은 조건수가 나쁜 이 침대에서 한도에 닿아 끝나는 것이 정상이다 (아래 산술 · 필요한 수는 18 만 초과). 그때 얻는 것 = 반복당 초 (풀이 + 증서 구간 / 반복 수 · 위 한계) · 한도에서의 잔차와 판 전류 불균형 (팔이 .failed 로 남고 판독기가 거기서 읽는다 · rc 3) · 메모리 · GPU 표본 · kgy 에서 블록 → 감시 셸 → 러너 → payload → 판독 → 묶음 전 과정이 한 번 도는지. 한도에 닿은 시도 1 은 정상 끝이다 (DONE · 묶음).
- 시도 2 의 한도 1500000 은 시도 1 의 결과를 보기 전에 정한 값이다. 시도 1 을 본 뒤 바꾸지 않는다. 바꾸려면 새 원장 줄을 먼저 커밋한다 (원장 §2 "시도" 칸 · 결과를 보고 고르지 않는다).
- 1500000 의 까닭: 아래 산술로 필요한 수는 rtol 1e-12 주 풀이 기준 18 만 초과 121 만 이하다. 400000 은 N8 이 5.4 만–6.6 만 이하일 때만 모이고 (N8 의 범위 3 만–20 만의 아래쪽), 한도에 닿으면 필요한 반복 수를 얻지 못한 채 최악 2 배를 쓴다. 1500000 은 그 위 끝을 덮는다.
- 1500000 의 비용 [추정]: 모이면 그 반복 수만큼만 돈다 (한도가 커도 더 돌지 않는다). 아래 시간 어림 (반복당 0.10 초는 위 한계) 으로 필요한 수가 18 만–121 만이면 주 풀이 약 5–34 시간이다. 안 모이면 최악 300 만 반복 (약 83 시간) 이다. 시도 1 의 반복당 초가 이 어림을 실측으로 바꾼다 (한도는 그대로).
- 일찍 멈추면 (블록의 stop early 줄 · 메모리 상한) 남는 것 = 전체 초 · 메모리 · GPU 표본 · `solve_to_end_s`. 반복 수 · 잔차 · 판 전류 불균형은 남지 않는다 (풀이가 끝나야 팔 JSON 에 쓰인다). 주 풀이가 한도에 닿은 뒤 (이어 풀기 중) 에 멈췄으면 payload 의 "CG not converged" 줄의 info · 상대 잔차가 남는다. payload 는 그 줄을 flush 없이 찍으므로 감시 셸이 러너에 `PYTHONUNBUFFERED=1` 을 준다 (물리 축 아님 · `stdbuf` 류는 python 의 자체 버퍼에 닿지 않는다 · 원장 §3 러너 명령 줄에 한 낱말 · §9).
- 아래 표와 산술은 제안 때의 글 그대로다.

| 후보 | 근거 (파일 · 줄) | 걸리는 점 |
|---|---|---|
| 200000 | 러너 주석의 예시 (`scripts/sdcp_gain_vox015_8arm.sh` 320 행). σ_VGCF 7854 꼴 (대비 785,400 배 · rtol 1e-8 · 08 월 침대 · 접합 없음) 이 30000 에서 못 모이고 (`scripts/step3_sigma.py` 481–486 행) 200000 에서 모였다 (`docs/reviews/a_track_verdict_20260829.md` 51 · 61 행). 등록 스윕도 이 값을 썼다 (`docs/reviews/sigma_closure_sweep_prereg_20260902.md` 173 행: 모이는 점에는 영향 없음) | 아래 산술로는 필요한 수의 아래 끝 근처다 |
| 400000 | 다음 세대 꼴 (섬유 7,853.98 · AM 0.0041 · 접합 R_j 1e6 · rtol 1e-14 까지) 을 실제로 푼 유일한 자리인 증서 봉인 표의 한도 (`scripts/step3_conv_cert.py` 110 행 `PROBE_MAXITER`) | 합성 41,472 dof 표의 한도다. 실침대를 보증하지 않는다 |
| 1000000 | 문서 근거 없음 (아래 산술의 위쪽을 덮으려는 값) | 안 모이면 낭비가 가장 크다 |

- 산술 [우리 산술 · 추정]: σ_VGCF 7854 꼴의 rtol 1e-8 반복 수 N8 은 30000 초과 200000 이하다 (위 두 기록). 합성 표의 반복 비 (접합 꼴 rtol 1e-12 는 접합 없는 꼴 1e-8 의 6.05 배 · 1e-14 까지는 7.37 배 · 등록 R §10-4 표) 를 곱하면 필요한 수는 18 만–22 만 초과, 121 만–147 만 이하다. 200000 은 그 아래 끝이고 400000 은 N8 이 5.4 만–6.6 만 이하일 때까지 덮는다.
- 이 산술의 약한 곳: N8 의 근거는 다른 침대 세대 · 다른 AM σ 의 기록이고 (대비 785,400 배 · 지금 꼴은 7,853.98 / 0.0041 = 약 192 만 배), 반복 비는 합성 침대의 것이다. 실침대는 더 클 수도 작을 수도 있다. 이 탐침이 재려는 값이다.
- 한도에 닿으면 얻는 것 (실물로 확인 · 시험 R3): 주 풀이가 한도에서 끝나고 (`cg_iters` = 한도 · `cg_info` = 한도) payload 가 팔을 `.failed` 로 킷 런 폴더에 남기며 러너는 받아들이지 않는다. 판독기가 거기서 반복 수 · 잔차 · 불균형 · 시간을 읽는다 (rc 3). 반복당 시간은 나오지만 필요한 반복 수는 안 나온다. 다음 시도는 그 남은 파일이 있는 채로 SKIP 없이 새로 푼다 (시험 R5 · 새 출력 폴더).
- 한도에 닿을 때의 비용 (실물로 확인 · R3): ⓒ 이어 풀기는 주 풀이가 안 모여도 같은 한도로 한 번 더 돈다 (`scripts/step3_conv_cert.py` 216 행 · `scripts/step3_sigma.py` 2347–2351 행 · 픽스처에서 한도 2 일 때 이어 풀기 반복 수 2). 최악은 한도의 2 배 반복이다 (시도 1 은 최대 6 만 반복).
- 시간 어림 [추정]: 10-20 SDCP 최종 16 팔의 DBE 팔 (접합 없는 꼴 · rtol 1e-8) 이 30000 반복을 3,054 초 안에 돌았다 (`docs/session_20260923_progress.md` 1130 행 · raster 포함이라 반복당 0.10 초는 위 한계). 그 값이면 20 만 반복 약 5.6 시간, 40 만 약 11 시간이고 최악 (2 배) 은 그 두 배다. 시도 1 (CG 최대 6 만 반복) 은 그 어림으로 CG 만 약 1.7 시간이다 (raster · 준비 시간은 따로). 발사 전에는 모른다.
- GPU 경로의 전처리는 Jacobi 고정이다 (`scripts/step3_sigma.py` 485 · 579 행). AMG 는 CPU 경로뿐이다.

## 7. 시험

- 시험 먼저 (1 회차 · P6R-01–12): 고친 시험을 고치기 전 도구 (판독기 · 감시 셸 · 블록 · 원장 줄 초안 · README) 에 돌린 결과 = 152 PASS · 102 FAIL (S 10 · T 50 · M 17 · F 11 + 실행 단계 실패 · B 9 · R 5 실패).
- 시험 먼저 (2 회차 · P6R2-01–08 · 11-10): 새 시험을 넣고 고치기 전 도구 (판독기 · 감시 셸 · 블록 · 원장 · README · 원장 줄 초안) 에 돌린 결과 = 196 PASS · 112 FAIL (S 9 · T 73 · F 15 · B 12 · R 3 실패 · 3.11 · 171 초). 실패 112 가운데 75 = 새 닫힌 칸 `rj_matches_registered` 가 없어 구조 검사가 걸린 연쇄 (T 대부분 · F01d · F09a · F18 · R1f · R2c). 나머지 = 항목마다 옳은 이유: P6R2-01 (B13 · B02 · F08 s27 · F19) · 02 (B11 · B12 · B02 · F19) · 03 (B02 · B14 · F20 · F09e · T27) · 04 (F08 s24 · s25 · T26) · 05 (T25b · T28 · T29 · F02f · F04a) · 06 (F21a · b · c · F02f · F05 · S03h) · 07 (B01 · S04h · S14) · 문서 · 명령 줄 (S03i · S04e · S04g · S05a · S11 · S13) 과 옛 블록 · 감시 셸이 멈추지 않아 띄운 감시 셸의 연쇄 (B03 · B05 · B07 · B10 · F08b). R 은 실행 단계 1 (R3 = 짝 표를 고친 사본 · 시험 전용 · 고치기 전 코드에 그 표가 없다).
- 고친 뒤 (2 회차): Python 3.11.18 (numpy 2.4.6 · scipy 1.17.1) 과 kgy 판 Python 3.8.20 (numpy 1.24.4 · scipy 1.10.1) 둘 다 330 PASS · 0 FAIL (S 39 · T 127 · M 86 · F 42 · B 14 · R 22 · 3.11 209 초 · 3.8 214 초 · 이름공간 안 `unshare -pf --mount-proc`). 감시 셸 변이 W 65/65 잡힘 (3.11 · 1458 초 · 리뷰어 13 포함 · 2 회차 새 15 · 게이트 기본 실행에 없다). 그 뒤 문법이 깨졌던 변이 하나 (meta 의 attempt1 칸 · 빈 then 절 · 그때는 F01a 가 구문 오류로 잡았다) 를 `:` 로 고쳐 따로 다시 돌렸다 = F20b 가 잡음 · S15 가 이 꼴을 막는다. 리뷰어 재현 스크립트를 고친 트리에 그대로: 실패 꼴 18 (failopen) 이 전부 rc 4 · 풀이 0 뒤 시도 2 · 끝난 시도 다시 · 풀이 코드 바뀜 · 짝 어긋남 = 전부 STOP · 작업 제어 켠 감시 셸 = 러너가 끝난 뒤 DONE.
- 묶음: S 정적 (S15 = 변이 사본 W · M 이 모두 문법이 성립한다 · 깨진 사본이 엉뚱한 까닭 (구문 오류) 으로 "잡히는" 것을 막는다 · 2 회차 고침 중 W 변이 하나가 그 꼴이었다) · T 판독기 합성 폴더 · M 판독기 변이 86 (리뷰어 변이 33 · 2 회차 새 10 포함 = 새 9 + 옛 rtol 변이 하나를 영수증 · 증서 둘로 나눔 · 하나라도 못 잡으면 실패) · F 감시 셸 + 가짜 러너 (시도 1 마다 새 홈 · 끝난 시도 1 은 같은 홈의 다음 시도 1 을 막는다) · B 블록 그대로 시도 1 → 시도 2 · R 실제 러너 + 실제 payload + 픽스처 킷. 고를 때만 = W 감시 셸 변이 65 (리뷰어 변이 13 · 2 회차 새 15 포함 · `--only W`).
- 시험 기반의 바뀐 점 (2 회차): 합성 meta 의 기본 = 시도 2 꼴 (한도 1500000 · `attempt1_pin` · `code_same_as_attempt1=1`) · 시도 1 꼴 = `meta_a1()` (한도 30000) · 정직한 꼴의 한도는 등록 값뿐이다 (짝 · P6R2-04). 가짜 venv 의 python3 가 가짜 cupy 를 스스로 찾는다 (감시 셸이 PYTHONPATH 를 걷으므로 · 진짜 venv 의 site-packages 꼴). R3 = 짝 표 (시도 1 → 한도 2) 만 고친 사본 (감시 셸 · 판독기 · 시험 전용 · 픽스처 침대는 30000 안에서 모인다) · 새 홈 · R5 = 같은 사본의 시도 2.
- 누출 검사 (P6R-01 고침): ① 구조: 보고 JSON 의 키는 닫힌 목록 · 칸마다 꼴 · 팔 칸 값 = 팔의 그 자리 값 · 화면 줄마다 보고의 같은 값 · 걸러 낸 로그 줄 꼴 · 묶음 파일마다 꼴. ② 수 찾기: σ 류 값과 그 변형 (단위 · ×10^k · 1/σ · 2σ · log10 · ln · 유효숫자 3 자리 이상 반올림 · 버림 · 지수 표기 · 자리 띄움 · float.hex) 을 화면 · 보고 · 걸러 낸 로그 · 묶음에서 찾는다. 합성 폴더는 σ 류 자리마다 표식 0.00713331… 을 심었다. 실물 (R) 은 실제 팔 JSON 의 σ 류 수를 과녁으로 유효숫자 7 자리 이상 소수만 찾는다 (우연히 맞을 확률을 줄이려고 · 양성 대조 = 그 수를 흔한 꼴로 적은 글은 잡힌다).
- 시험이 잡지 못하는 꼴 (값이 새는 꼴이 아닌 것 제외): σ 를 유효숫자 2 자리 이하로 적거나 다른 수에 섞어 (예: 더하기) 적는 판독기. 구조 검사는 그 글이 닫힌 칸 밖에 있으면 잡는다 (보고 · 화면 · 걸러 낸 로그의 칸 · 줄 꼴이 닫혀 있다).
- (2 회차 P6R2-08 · 한정만 · 코드 고침 없음) 값 출처 · 값 단언이 없는 허용 칸 (`log.done_vox_um` · `receipt.receipt_vox_um` · `timing.resolution_s` · `timing.pre_step3_s` · `resources.n_samples` · `gpu_util_max_pct` · `rss_proc_max_kb` · `time_v_elapsed_s` · `log.n_lines` 같은 수 칸) 에 일부러 계산한 꼴 (0.37σ · √σ · σ² · L/σ · 정수 꼴 int(σ·3.7e9)) 을 넣으면 통과한다 (2 회차 새 변이 82 중 15 · 고친 트리에서 리뷰어 스크립트를 그대로 다시 돌려도 같은 15). 일부러 계산해야 생기는 꼴이고 정직한 흐름 (원값 복사 · 반올림 · 단위 · 지수 · 새 칸) 에서는 안 생긴다. 그 실수 꼴은 수 찾기 · 구조 검사가 잡는다.
- 실물 묶음 (R) 은 `scripts/test_rint_r_chain_e2e.py` 의 픽스처 침대와 `scripts/test_ca_ext_runner.py` 의 가짜 python3 (규율 관문 둘만 건너뜀 · 감시 셸의 미리 돌리기도 같다) 을 그대로 쓴다. R3 = 시도 1 꼴 (한도 2 · 미수렴 실물) · R5 = 시도 2 꼴 (R3 의 남은 .failed 가 있는 채 새 출력 · 로그 폴더).
- 시험하지 못한 것: 진짜 GPU 풀이. 실침대 크기 (팔 JSON 수십 MB 이상) 에서 판독기가 걸리는 시간. kgy 의 nvidia-smi 출력 꼴 (가짜 nvidia-smi 로 시험했다). D 상태 (커널에 묶여 KILL 이 안 듣는) 프로세스가 그룹에 남는 경우 (DONE 은 그룹이 빌 때까지 기다린다 · 그 기다림은 시험하지 못했다). kgy 의 진짜 `ps` (시험은 이 시험의 프로세스만 보이는 가짜 ps 로 동시 실행 가드를 본다).

## 8. 한정 · 이 탐침이 닫지 않는 것

- 원장 밖에서 돈 그림자 런을 기계적으로 막지 못한다 (원장 §4 그대로). 이 준비물이 막는 것은 감시 셸을 거친 시도 안에서의 일이다. 동시 실행 가드는 같은 계정의 러너 · payload 이름이 든 프로세스와 감시 셸 잠금 (`~/.probe6.lock` · `mkdir` 잠금 · 킷 폴더에는 아무것도 만들지 않는다) 만 본다.
- S0 단계 1 의 "새 SV 계약이 모두 닫혔다" 는 결론을 이 탐침에서 뽑지 않는다 (원장 §4).
- 탐침은 한 점이다: SBE · arm 0 · R_j 1e6 Ω · P0 · c 0. 사다리의 다른 R_j (바닥 · 천장 포함) · 다른 origin · DBE 침대의 반복 수는 다를 수 있다. 그래서 등록 R 은 maxiter 를 넉넉하게 두라고 한다 (§11 ④).
- 감시 셸이 러너를 띄우기 전에 멈추는 조건 (화면 · status.log 에 `STOP: … (runner not started)` · 종료 코드 2 · 로그 폴더를 받은 뒤면 `STOPPED` 표지): 인자 꼴 · 로그 폴더가 새것이 아님 · 경로 글자 · 로그 폴더가 홈 바로 밑이 아님 · 폴더 이름의 시도 번호 (없음 · 출력 · 로그 폴더가 다름) · 시도 번호 ↔ 한도가 등록 짝 (1 → 30000 · 2 → 1500000) 이 아님 · 잠금이 있음 · 앞 로그 폴더 (`~/p6log_*`) 에 끝 표지가 없음 · 이 시도 번호가 이미 끝남 (`DONE` + `solve_started=1` · `WATCHER_FAILED` + 러너 시작 줄) · 시도 1 인데 끝난 시도 2 가 있음 · 시도 2 인데 풀이를 시작한 시도 1 의 DONE 폴더가 정확히 하나가 아님 · 그 핀이 이 핀이거나 그 앞 커밋이 아님 · 두 핀 사이에 풀이 코드 (§9 목록) 가 바뀜 · 같은 계정의 러너 / payload 가 돌고 있음 · 출력 폴더가 비어 있지 않음 · 핀 다름 · 작업 트리가 깨끗하지 않음 · 감시 셸이 핀 작업 트리 밖의 사본 · venv · setsid 없음 · 킷이나 압밀 런 폴더 없음 · S0 계획 · 그 tol_ff 가 등록 명령 값과 다름 · 킷 런 폴더 이름이 S0 계획과 다름 · 킷 payload 줄에 `--joule-heat` · `--save-step4-grid` · `--show-results` 가 있음 · `--step3-gpu` 가 없음 · nvidia-smi 없음 · cupy 를 못 불러옴 · 여유 메모리 부족 · 러너 글에서 런 전 관문 명령을 못 읽음 · 러너의 런 전 관문 (규율 검사 · 미정의 이름 검사) 이 실패 · 시작 전 신호 · 시작 전 뜻밖의 끝 (예: 정의 안 된 변수). 이때는 아무것도 풀지 않았다. 로그 폴더를 받기 전의 멈춤 (인자 꼴 · 로그 폴더 · 그 경로 글자) 만 표지 없이 화면 줄뿐이다.
- 블록의 멈춤 (`[p6] STOP:`) 은 `KGY_BLOCK.md` 의 목록. fetch 전 멈춤은 아무것도 쓰지 않는다. fetch 뒤 멈춤은 fetch 만 했다.
- 러너가 시작된 뒤 감시 셸 자신이 뜻밖에 끝나면 (EXIT 덫) 러너 그룹을 끝내고 `WATCHER_FAILED` 표지를 쓰고 잠금을 남긴다 (사람이 본다). 러너가 자기 세션의 우두머리가 아닐 때 (작업 제어가 켜진 채 `setsid` 가 fork 한 꼴 · 감시 셸은 머리에서 `set +m` 으로 작업 제어를 끄고 러너를 `env -u BASH_ENV -u SHELLOPTS` 로 띄우므로 둘째 겹) 도 러너 시작 줄 뒤 같은 길로 `WATCHER_FAILED` (`reason=` 줄) 가 된다 (블록은 `runner started` 줄을 찍고 돌아오므로 그 뒤의 이 실패는 status.log · 끝 표지에서 본다). 그 러너는 감시 그룹 밖에서 돌 수 있으므로 같은 계정의 ps 를 본다. 메모리 상한 · 신호 · 러너 실패는 정상 끝 (DONE) 이다. 좁은 틈 (코드를 읽은 판단 · 시험하지 않음): 러너를 띄우는 바로 그 순간 (`setsid` 가 새 세션을 만들기 전후 몇 ms) 에 받은 stop early 는 러너 그룹이 아직 없으면 러너에 닿지 않고 (러너가 끝까지 돈다 · 두 번째 신호도 그룹을 다시 멈추지 않는다 · meta `aborted=1` 이라 판독 rc 4), 신호가 러너 그룹에 닿아 러너가 세션 확인 전에 끝나면 세션 확인 실패 (`WATCHER_FAILED` · 러너 시작 줄이 있으니 끝난 시도로 센다) 로 적힌다. 어느 쪽이든 status.log 의 러너 시작 줄 바로 앞뒤에 신호 줄 (`signal received`) 이 있다 (본 세션이 그 줄을 보고 정한다).
- 킷 payload 줄의 조건은 헛도는 시도를 막으려는 것이다. `--joule-heat` · `--save-step4-grid` 는 다음 세대 payload 가 입구에서 거부한다 (`scripts/mpm_webapp_payload.py` 942–945 · 1830–1833 행 · 시험 R1h). kgy 의 새 킷은 그 두 토큰을 뺀 것으로 기록돼 있다 (`docs/reviews/rint2_kgy_commands_20261020.md` §1-1 73 · 82 · 83 행). `--show-results` 는 봉인을 연다. `--step3-gpu` 가 없으면 payload 가 CPU 로 풀고 러너가 그 팔을 받지 않는다 (같은 검사 = `scripts/sr01_stamp_ab.sh` 92 행 · 킷 생성기는 늘 넣는다 = `scripts/mpm_input_from_case.py` 906 행).
- 러너의 런 전 관문 (러너 685 · 697 행 · 규율 검사 · 미정의 이름 검사) 은 감시 셸이 러너 글에서 그 명령을 읽어 같은 env · 같은 자리에서 한 번 미리 돌린다. 러너도 자기 관문을 다시 돈다 (러너는 고치지 않았다 · 규율 검사가 두 번 돈다 · 그 검사 한 번 = 게이트 기계에서 약 90 초 · `scripts/test_ca_ext_runner.py` 머리 주석 · 이 컨테이너 약 74 초 (11-10 내부 반박 리뷰 실측) · kgy 실측 없음). 그 미리 돌리기 중에 온 stop early (TERM) 는 관문이 끝난 뒤 처리된다 (`STOPPED`).
- 상태가 VALID_ZERO_TOPOLOGY 나 ELECTRODE_SHORT 이면 그 이름이 곧 σ 의 상태 (0 · 게시 안 됨) 를 말한다. 그때 판독기는 상태 이름만 내고 rc 3 을 낸다. CG 가 돌지 않으므로 반복 수는 없다.
- 실패 줄은 수를 `#` 하나로 가려 보고에 넣는다. 수의 크기 · 자릿수는 남지 않지만 부호와 `nan` · `None` 같은 낱말은 남는다.
- 명령 줄의 입력 값 (0.0041 · 256.6 · 1e4 · 1e6 등) 은 등록 R 에 적힌 입력이지 결과가 아니다. command.txt 와 원장 줄에는 그대로 적는다.
- 판독기는 팔 파일의 값이 옳은지 판정하지 않는다. 수렴 증서의 판정은 payload 와 러너의 계약 검사 (`check_arm`) 가 한 것이고, 판독기는 그 결과 칸을 옮기고 등록 값 · 신원을 대조할 뿐이다.
- 감시 셸의 메모리 상한 (기본 = min(46, 시작 때 여유 − 6) GB · 11-06 S0 감시 셸과 같은 규칙) 에 닿으면 러너 그룹을 끝낸다. 그 시도는 정상 끝 (DONE · 판독 rc 4) 으로 보존된다. 시간 상한은 없다.
- 이 준비물은 실행 승인이 아니다. 발사는 1저자 GO 와 원장 줄 커밋 뒤다.

## 9. 문서와 다른 점 · 정한 것 · 미확인

문서와 다른 점 (러너 코드로 확인):

1. 등록 R §10-1 (2) 와 kgy 명령 문서 §2-2b 의 블록은 러너를 킷 뿌리에서 띄우지 않는다 (앞 줄이 다른 폴더로 cd 한다). 러너는 `KITS` 를 현재 폴더 기준으로 찾아 "~/sdcp 에서 돌릴 것" 으로 멈춘다 (`scripts/sdcp_gain_vox015_8arm.sh` 973–974 행). 감시 셸은 킷 뿌리로 cd 한 뒤 띄운다.
2. 같은 블록의 `OUTDIR=~/sdcp/ca1_probe` 는 그대로 쓰이지 않는다. 팔 수가 8 이 아니면 러너가 이름에 `_arm1` 을 붙인다 (594–597 행). 감시 셸은 이름이 `ca1_probe6_a<시도>_…_arm1` 인 출력 폴더만 받는다.
3. 러너는 킷 런 폴더에 쓴다: 생성 스크립트 (842 행) · time 기록 (909 행) · payload 출력 (924 행 · 검사 통과 뒤 961 행에서 출력 폴더로 옮김). 킷의 역할 파일은 건드리지 않는다. 같은 이름의 앞 시도 파일은 덮인다 (§3 실패 보존 칸의 사본이 그 대비다).
4. 러너 명령 줄에 `PYTHONUNBUFFERED=1` 이 더해졌다 (§6). 등록 R §10-1 (2) 에 없는 한 낱말이다 (원장 §3 의 러너 명령 줄에는 들어갔다).
5. (2 회차 고침 · P6R2-06) 러너 명령 줄 머리에 `-u BASH_ENV -u SHELLOPTS` 가 더해졌다 (감시 셸이 러너와 미리 돌리는 런 전 관문을 `env -u BASH_ENV -u SHELLOPTS …` 로 띄운다 · 물리 축 아님). 원장 §3 · `LEDGER_LINE.md` · 아래 사본의 러너 줄 둘이 같이 바뀌었다 (감시 셸 줄 둘은 그대로 · 시험 S04e · S05a · S11 · S14 가 셋을 대조한다).

정함 (11-10) (본 세션 · 1저자 · 원장 §3 의 "본 세션 정함" 글):

1. maxiter 두 값 = 시도 1 30000 · 시도 2 1500000 (정함 · §6). 바꾸면 블록의 표 · 감시 셸 · 판독기의 짝 표와 원장 줄의 값을 같이 바꾼다 (시험 S04e · S05 · S11 · T26 · F08 이 대조한다).
2. 붙잡아 둔 상대 칸 넷 = 허용 칸에 넣지 않는다 (정함 · 닫아 둔다).
3. 감시 셸의 메모리 상한 규칙 = 그대로 · 시간 상한 = 없음 (정함).
4. 블록의 `BASE` = 그대로 (정함 · 발사 전에 본 세션이 `<PIN>` 과 함께 확인).
5. 원장 §3 두 줄 · 명령 줄 넷 = 원장에 들어갔다 (정함 · 시험 S11 이 원장 파일을 읽는다). 남은 것 = `<PIN>` 채우기 (발사 직전의 stoic 끝 · 원장 §3 핀 칸 글).
6. 시도 2 의 핀 규칙 = 시도 1 의 핀이거나 그 뒤 커밋 (`git merge-base --is-ancestor` 그대로 · 정함) + 두 핀 사이에 풀이 코드가 같아야 한다 (1저자 11-10 Q2 (가) · P6R2-03 · 아래 목록).
7. `WATCHER_FAILED` 셈 = status.log 에 러너 시작 줄 (`runner started - maxiter …`) 이 있으면 끝난 시도 · 없으면 STOP 과 같다 · 남은 잠금은 1저자가 같은 계정에 감시 셸 · 러너 · payload 가 없음을 본 뒤에만 지운다 (정함). 따라 나오는 것 (2 회차): 끝난 시도 1 이 `WATCHER_FAILED` 이면 시도 1 은 다시 못 띄우고 시도 2 의 앞 조건 (`DONE` + `solve_started=1`) 도 서지 않는다 (블록 · 감시 셸 둘 다 멈춘다) → 그다음은 본 세션이 정한다.
8. (2 회차 · P6R2-05 · 구현에서 고름) PYTHONPATH = 감시 셸이 걷어낸다 (venv 활성화 뒤 · python 을 처음 부르기 전 · meta `pythonpath_removed`). 판독기는 러너 시작 때 PYTHONPATH 가 남았다는 meta `pythonpath_set=1` 을 받지 않는다 (둘째 겹 · 정직한 흐름에서는 늘 0). 부르는 셸에 PYTHONPATH 가 있어도 시도가 버려지지 않는다.
9. (2 회차 · P6R2-02 · 구현에서 고름) "시도 1 은 쓰인 a2 폴더가 있어도 STOP" 의 "쓰인" = 끝난 시도 2 폴더 (`DONE` + `solve_started=1` · `WATCHER_FAILED` + 러너 시작 줄 · 시도 번호를 세는 규칙과 같다). `STOPPED` · `DONE` + `solve_started=0` 인 a2 폴더는 세지 않는다 (멈춘 시도 2 가 시도 1 을 영영 막지 않게). 끝난 시도 1 의 다시 띄우기는 그 번호 규칙이 따로 막는다.

풀이 코드 목록 (P6R2-03 · 블록 `CODE` · 감시 셸 `CODE_PATHS` · 원장 §3 이 같은 목록):

- `scripts/` · `docs/reviews/rint2_probe6_prep_20261110/tools/` · `docs/data/rint2_s0_sbe_20261108/` · `docs/data/rint_eis_anchors.csv` · `docs/reviews/sdcp_gain_prereg_v2_20260816.md`
- 정한 법: 실물 러너 + 실물 payload 를 픽스처 침대 (`scripts/test_rint_r_chain_e2e.py`) · 등록 축 (백엔드만 cpu) · 진짜 규율 관문으로 돌리고 strace 로 연 파일을 셌다 (11-10). scripts/ 밖에서 연 리포 파일 = 러너 bash 의 사전등록 (`[ -f ]` 로 있는지만 · 672 행) · payload 의 EIS 앵커 표 (`scripts/mpm_webapp_payload.py` 2676 행 · 집전체 시나리오 값) · 규율 검사 (관문) 의 `docs/reviews/claims.json` · `docs/manuscript/methods_simulation_v7_draft.md` · `.github/workflows/discipline.yml` · `.git`. 관문의 입력은 통과 / 멈춤만 정하고 감시 셸이 러너보다 먼저 같은 관문을 돌리므로 (실패 = 띄우기 전 STOP) 목록에 넣지 않았다. scripts/ 는 통째로 넣었다 (넓게 · import 를 하나씩 세다 빠뜨리지 않게).
- 목록 밖: 원장 · 진행 기록 같은 문서 (두 시도 사이에 본 세션이 시도 1 결과 줄을 커밋한다) · 준비 폴더의 README · 블록 · 원장 줄 초안.
- 따라 나오는 것 (운영): scripts/ 를 통째로 넣었으므로 두 시도 사이에 scripts/ 의 어느 파일이든 (탐침과 관계없는 도구여도) 바꾼 커밋이 가지에 오르면 시도 2 는 멈춘다 (블록이 PIN = 가지 끝을 요구하므로 피해 갈 수 없다). 그 사이에는 목록의 경로를 건드리는 커밋을 가지에 올리지 않는다 (올렸다면 시도 2 는 본 세션이 정한다).

원장 §3 의 시도 표 · 명령 줄 · 규칙 글 (11-10 · 원장 파일이 정본 · 아래는 그 사본 · 명령 줄 넷은 글자 그대로):

```text
| 번호 | 시작 (KST) | 명령 줄 | 핀 | 기계 · 환경 | 결과 (반복 · 잔차 · 판 전류 불균형 · 시간 · 메모리) | 폴더 sha256 |
|---|---|---|---|---|---|---|
| 1 | ⬜ (발사 뒤 · 묶음 meta 의 start_kst) | 아래 "시도 1 · 2 의 명령 줄" 의 시도 1 (감시 셸 한 줄 + 감시 셸이 내는 러너 명령 한 줄 · 한도 30000 · 짧은 확인) | 이 줄을 넣은 커밋 (stoic 가지 · 발사 블록의 PIN 이 그 40 자리다 · 감시 셸이 작업 트리 HEAD = PIN 을 확인하고 묶음 meta 에 적는다 · 40 자리는 발사 뒤 이 칸에 옮긴다 · 아래 글) · 발사 전 고침 커밋 = 2 회차 반박 리뷰 고침 = `420da6bb33890965717510d1a4167d597718b2d1` (11-10 push) → 핀 = 발사 직전의 stoic 끝 | kgy · Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy-cuda12x 12.3.0 · RTX 3090 24 GB · OpenBLAS SkylakeX (11-09 기계 조사) · GPU 드라이버 · CUDA 판 = ⬜ (발사 뒤 · 묶음 env) | (결과 0 건) | (결과 0 건) |
| 2 | ⬜ (풀이를 시작한 시도 1 (`solve_started=1`) 의 DONE 뒤 · 묶음 meta 의 start_kst) | 아래 "시도 1 · 2 의 명령 줄" 의 시도 2 (한도 1500000) | 시도 2 발사 직전의 stoic 끝 (시도 1 의 핀이거나 그 뒤 커밋 · 두 핀 사이에 풀이 코드 (아래 목록) 가 같아야 한다 · 블록 · 감시 셸이 시도 1 의 DONE 폴더 meta 의 핀을 보고 대조한다 · 40 자리는 발사 뒤 이 칸에) | 시도 1 과 같은 기계 (kgy) · ⬜ (발사 뒤 · 묶음 env) | (결과 0 건) | (결과 0 건) |

### 시도 1 · 2 의 명령 줄 (11-10 등록 · 결과 0 건 · 시작 전 커밋)

시도 1 (블록 `ATTEMPT=1` · 한도 30000 · 한도에 닿아 끝나는 것이 정상):

    bash <W>/docs/reviews/rint2_probe6_prep_20261110/tools/run_probe6.sh <W> <O> <L> <PIN> 30000

    env -u BASH_ENV -u SHELLOPTS VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4 CJUNC=1 CJUNC_RJ=1e6 CJUNC_LEN_LAW=len_scaled_v0 CJUNC_UNREG_LAW=cut CJUNC_S_MIN_UM=0.0 CJUNC_TOL_FF_UM=0.07381254285530132 CJUNC_PTFE_JLAW=P0 SDCP_MOD_C=0 STEP3_RTOL=1e-12 EXPECT_BACKEND=gpu KITS=kit_SBE_vgcf100 ARMS=1 LEAN=2 P2_EXTRA="--step3-maxiter 30000" OUTDIR=<O> PYTHONUNBUFFERED=1 bash <W>/scripts/sdcp_gain_vox015_8arm.sh

시도 2 (블록 `ATTEMPT=2` · 한도 1500000 · 풀이를 시작한 시도 1 (`solve_started=1`) 의 DONE 뒤):

    bash <W>/docs/reviews/rint2_probe6_prep_20261110/tools/run_probe6.sh <W> <O> <L> <PIN> 1500000

    env -u BASH_ENV -u SHELLOPTS VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4 CJUNC=1 CJUNC_RJ=1e6 CJUNC_LEN_LAW=len_scaled_v0 CJUNC_UNREG_LAW=cut CJUNC_S_MIN_UM=0.0 CJUNC_TOL_FF_UM=0.07381254285530132 CJUNC_PTFE_JLAW=P0 SDCP_MOD_C=0 STEP3_RTOL=1e-12 EXPECT_BACKEND=gpu KITS=kit_SBE_vgcf100 ARMS=1 LEAN=2 P2_EXTRA="--step3-maxiter 1500000" OUTDIR=<O> PYTHONUNBUFFERED=1 bash <W>/scripts/sdcp_gain_vox015_8arm.sh

- 러너 env 에 `SIGMA_VGCF_OVERRIDE` 는 없다.  `--show-results` 없음 (값 봉인).  `PYTHONUNBUFFERED=1` 은 물리 축이 아니다 (감시 셸이 러너에 준다 · 일찍 멈출 때 payload 의 한도 줄이 버퍼에 갇히지 않게).  `-u BASH_ENV -u SHELLOPTS` 도 물리 축이 아니다 (러너 bash 가 시작 파일 BASH_ENV 와 셸 선택 SHELLOPTS (작업 제어 monitor 등) 를 물려받지 않게 · 2 회차 P6R2-06 · 감시 셸은 러너의 런 전 관문을 미리 돌릴 때도 같은 env 로).  감시 셸은 PYTHONPATH 를 걷어낸 뒤 python 을 부른다 (P6R2-05 · meta `pythonpath_removed` · 판독기는 러너 시작 때 PYTHONPATH 가 남았다는 meta `pythonpath_set=1` 을 PROBE_OK · 미수렴 어느 쪽에서도 받지 않는다).  자리표 값의 근거와 두 한도의 까닭 = `docs/reviews/rint2_probe6_prep_20261110/LEDGER_LINE.md` 끝 표 · `docs/reviews/rint2_probe6_prep_20261110/README.md` §6.
- 시도 2 의 한도 1500000 은 시도 1 의 결과를 보기 전에 정한 값이다.  시도 1 을 본 뒤 바꾸지 않는다 (바꾸려면 새 줄을 먼저 커밋한다).  **시도 번호 ↔ 한도 짝** (1 → 30000 · 2 → 1500000) 은 감시 셸이 본다 (다른 짝 = 띄우기 전 STOP) · 판독기도 본다 (meta 의 짝이 다르면 rc 4 · P6R2-04).
- **핀 칸**: 줄이 자기가 든 커밋의 번호를 미리 담을 수 없어 1 번 줄은 "이 줄을 넣은 커밋" 으로 적는다.  발사 전에 줄이나 준비물을 고치는 커밋이 더 생기면 핀 = 발사 직전의 stoic 끝이고 (블록이 fetch 뒤 PIN = 가지 끝인지 본다), 그 사실을 줄에 적은 뒤 발사한다.  2 번 줄의 핀 = 시도 2 발사 직전의 stoic 끝이다.  어느 쪽이든 발사 블록의 PIN (40 자리) 과 묶음 meta 의 pin 이 같아야 하고, 발사 뒤 그 칸에 40 자리를 옮긴다.  (11-10) 2 회차 반박 리뷰 고침 커밋 (`420da6bb33890965717510d1a4167d597718b2d1` · 11-10 push) 이 1 번 줄을 넣은 커밋 뒤에 들어간다 → 1 번 줄의 핀 칸에 그 sha 를 적고 핀 = 발사 직전의 stoic 끝.
- **띄우기 전 STOP · 풀이 0**: 풀이가 시작되기 전에 끝난 경우 (블록의 멈춤 · 감시 셸의 발사 전 확인 실패 · 러너 시작 전 신호 · 러너가 자기 런 전 관문에서 멈춤 · payload 가 풀이 시작 줄 전에 멈춤 · 풀이 0) 는 새 시도로 세지 않고 그 줄의 결과 칸에 사유를 적는다 (다음 발사도 같은 번호).  판별 = 로그 폴더의 `STOPPED` 표지 (감시 셸이 러너를 띄우지 않았다 · `runner_started=0` · 화면 · status.log 에 `STOP: … (runner not started)`) 또는 `DONE` 이어도 meta 의 `solve_started=0` (러너는 돌았지만 풀이 시작 줄이 없다).  블록 자신의 멈춤 (`[p6] STOP:` · 로그 폴더를 만들기 전) 은 폴더가 없다.  meta `solve_started=1` 이면 그 시도는 끝난 것이고 (일찍 멈춤 · 실패 · 한도 포함 · 폴더 그대로) 다음은 다음 번호 줄이다.  `WATCHER_FAILED` 표지 (러너 시작 뒤 감시 셸 자신의 실패 · 러너가 자기 세션의 우두머리가 아님 · meta 가 없을 수 있다) 는 본 세션이 그 폴더의 status.log 를 보고 정한다.
  → 본 세션 정함 (11-10 · README §9 의 정할 것 6 · 7): 시도 2 의 핀 = 시도 1 의 핀이거나 그 뒤 커밋 (블록의 merge-base 조건 그대로 · 두 시도 사이에 시도 1 결과 줄을 커밋하므로) · `WATCHER_FAILED` 는 status.log 에 러너 시작 줄이 있으면 끝난 시도로 센다 (다음 = 다음 번호 · 폴더 그대로) · 러너 시작 줄이 없으면 위 STOP 과 같다 (새 시도로 세지 않음) · 남은 잠금 (`~/.probe6.lock`) 은 1저자가 같은 계정에 감시 셸 · 러너 · payload 프로세스가 없음을 본 뒤에만 지운다 · 붙잡아 둔 상대 칸 넷은 그대로 닫아 둔다 · 메모리 상한 규칙 · BASE 그대로.
- **시도 2 의 앞 조건** (2 회차 P6R2-01): 풀이를 시작한 시도 1 (`solve_started=1`) 의 DONE 뒤: `~/p6log_a1_*` 가운데 `DONE` 이 있고 meta 에 `solve_started=1` 인 폴더가 정확히 하나 (블록 · 감시 셸 둘 다 본다).  풀이 0 인 시도 1 (`STOPPED` · `DONE` + `solve_started=0`) 뒤에는 시도 2 블록이 멈추고, 시도 1 블록을 다시 붙인다 (같은 번호).
- **끝난 시도 번호** (2 회차 P6R2-02): `~/p6log_a<N>_*` 에 `DONE` + `solve_started=1` 이나 `WATCHER_FAILED` + status.log 의 러너 시작 줄 (`runner started - maxiter …`) 이 하나라도 있으면 그 번호는 다시 띄우지 않는다 (블록 · 감시 셸 둘 다 · 원장의 감시 셸 줄은 손으로도 부를 수 있다).  시도 1 은 끝난 시도 2 폴더가 있어도 멈춘다.  `STOPPED` · `DONE` + `solve_started=0` 은 세지 않는다 (같은 번호 다시).  감시 셸은 로그 폴더가 홈 바로 밑 (`~/p6log_a<N>_…`) 일 때만 받고, 앞 로그 폴더에 끝 표지가 없으면 멈춘다 (블록과 같다).
- **풀이 코드** (2 회차 P6R2-03 · 1저자 11-10 Q2 (가)): 두 시도의 핀 사이에 다음 경로가 바뀌면 시도 2 는 띄우지 않는다: `scripts/` · `docs/reviews/rint2_probe6_prep_20261110/tools/` · `docs/data/rint2_s0_sbe_20261108/` · `docs/data/rint_eis_anchors.csv` · `docs/reviews/sdcp_gain_prereg_v2_20260816.md` (러너 · payload 가 읽거나 import 하는 리포 파일 = 실물 러너 + payload 를 픽스처 침대에서 strace 로 돌려 셌다 · scripts/ 밖 = 러너가 있는지 보는 사전등록 · payload 가 읽는 EIS 앵커 표 · 그 밖에 탐침 도구 폴더 · S0 단계 1 자료 · 규율 검사의 입력 (`docs/reviews/claims.json` 등) 은 통과 / 멈춤만 정하고 감시 셸이 미리 돌리므로 목록 밖 · 이 원장 · 진행 기록 같은 문서도 목록 밖 · 두 시도 사이에 본 세션이 시도 1 결과 줄을 커밋한다).  두 겹: 블록이 `git diff --quiet <시도 1 의 핀> <PIN> -- <목록>` 이 아니면 멈추고 바뀐 파일 앞 다섯 개를 찍는다 · 감시 셸 (시도 2) 이 시도 1 폴더에서 그 핀을 스스로 찾아 다시 보고 meta 에 `attempt1_pin` · `code_same_as_attempt1=1` 을 적는다 · 판독기는 시도 2 에 그 둘이 없거나 다르면 rc 4.
- 검토 = 내부 반박 리뷰 (독립 조수 · Codex 아님) 를 발사 전에 거친다 (1저자 11-10 · Codex 회차는 봉인 전 묶음 한 번).  → 1 회차 (11-10 · 보고 = 본 세션 scratch · 원장 P6R-01–12) = P1 0 · P2 5 · P3 7 (σ 새는 길 없음 · 킷 원 입력 해시 대조를 깨지 않음) → 고침 = 이 줄을 넣은 커밋 (두 시도 · 시험 먼저) → 고친 곳만 짧은 재리뷰 (독립 조수) 뒤 시도 1 발사 GO 요청.
  → 2 회차 (11-10 · 내부 반박 · Codex 아님) = P1 0 · P2 3 · P3 5 (P6R2-01–08) → 고침 = 이 고침을 넣은 커밋 → 고친 곳만 3 회차 짧은 재리뷰 → 시도 1 GO 요청.
```

미확인:

- kgy 에 `/usr/bin/time` 이 있는지. 없으면 time 칸은 NONE 이고 표본 RSS 가 남는다. 있으면 묶음에는 time 기록의 세 줄 (최대 RSS · 경과 · 종료 코드) 만 들어간다 (명령 줄 · 홈 경로는 들어가지 않는다).
- kgy 의 nvidia-smi 가 프로세스별 GPU 메모리를 보여 주는지. 안 보이면 "우리 몫" 은 0 이고 전체 사용량은 남는다.
- kgy 킷의 payload 줄이 지금도 기록대로인지 (`--step3-gpu` 있음 · 세 토큰 없음). 아니면 감시 셸이 러너를 띄우지 않고 멈춘다.
- 실침대 팔 JSON 의 크기와 판독 시간.
- 핀에서 러너의 런 전 관문 (규율 검사 · 미정의 이름 검사) 이 kgy venv 로 통과하는지. 감시 셸이 러너보다 먼저 같은 명령으로 확인한다 (실패하면 러너를 띄우지 않는다).
- kgy 에 `setsid` · `timeout` 이 있는지 (util-linux · coreutils). setsid 가 없으면 감시 셸이 멈춘다. timeout 이 없으면 nvidia-smi 호출에 상한이 없다.
