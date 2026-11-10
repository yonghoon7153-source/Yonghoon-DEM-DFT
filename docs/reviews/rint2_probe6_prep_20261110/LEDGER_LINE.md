# 개발 탐침 원장 §3 에 넣을 줄 (초안 · ⑥ 시도 1)

- (본 세션 11-10) 이 초안을 원장 §3 에 옮겼다. 원장의 핀 칸은 40 자리 대신 "이 줄을 넣은 커밋" 으로 적었다 (줄이 자기가 든 커밋의 번호를 미리 담을 수 없다 · 까닭과 규칙은 원장 §3 아래 글). maxiter 는 1500000 으로 정했다 (README §6).

- 넣을 자리: `docs/reviews/rint2_dev_probe_ledger_20261026.md` §3 시도 표의 빈 줄 자리. 원장 파일은 본 세션이 고친다 (이 파일은 초안).
- 원장 §2 "시도" 칸: 시작 전에 줄을 커밋한다. `<PIN>` 은 본 세션이 준비물 커밋 뒤 40 자리로 채운다.
- 같은 커밋에서 원장 §2 "기계 / 환경" 칸의 ⬜ (첫 기계 = kgy) 도 닫는다 (권고).
- 시작 시각 · 환경의 GPU 드라이버 · CUDA 판 · 결과 · 폴더 sha256 은 발사 뒤 묶음 (meta · env · 보고 JSON) 에서 옮긴다. 손으로 고르지 않는다.
- 아래 줄의 기계 · 환경 값은 11-09 기계 조사 표 (`docs/reviews/rint2_siteq_prep_20261109/README.md` §7) 에서 옮긴 것이다. 발사 뒤 묶음 env.txt 의 값과 다르면 묶음 값이 맞다.

## 줄 (표 머리는 원장 §3 그대로)

| 번호 | 시작 (KST) | 명령 줄 | 핀 | 기계 · 환경 | 결과 (반복 · 잔차 · 판 전류 불균형 · 시간 · 메모리) | 폴더 sha256 |
|---|---|---|---|---|---|---|
| 1 | ⬜ (발사 뒤 · 묶음 meta 의 start_kst) | 아래 "명령 줄 전체" (감시 셸 한 줄 + 감시 셸이 내는 러너 명령 한 줄) | `<PIN>` | kgy · Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy-cuda12x 12.3.0 · RTX 3090 24 GB · OpenBLAS SkylakeX (11-09 기계 조사) · GPU 드라이버 · CUDA 판 = ⬜ (발사 뒤 · 묶음 env) | (결과 0 건) | (결과 0 건) |

## 명령 줄 전체

감시 셸 (블록이 nohup 으로 띄운다 · `<W>` = 핀 작업 트리 · `<O>` = 출력 폴더 (이름 끝 `_arm1`) · `<L>` = 로그 폴더):

    bash <W>/docs/reviews/rint2_probe6_prep_20261110/tools/run_probe6.sh <W> <O> <L> <PIN> 1500000

감시 셸이 킷 뿌리 (홈의 sdcp) 에서 내는 러너 명령 (등록 R §10-1 (2) 의 꼴 · 값 = 아래 표의 근거 · 실제로 돈 글자는 묶음의 command.txt 에 남는다):

    env VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4 CJUNC=1 CJUNC_RJ=1e6 CJUNC_LEN_LAW=len_scaled_v0 CJUNC_UNREG_LAW=cut CJUNC_S_MIN_UM=0.0 CJUNC_TOL_FF_UM=0.07381254285530132 CJUNC_PTFE_JLAW=P0 SDCP_MOD_C=0 STEP3_RTOL=1e-12 EXPECT_BACKEND=gpu KITS=kit_SBE_vgcf100 ARMS=1 LEAN=2 P2_EXTRA="--step3-maxiter 1500000" OUTDIR=<O> bash <W>/scripts/sdcp_gain_vox015_8arm.sh

- 러너 env 에 `SIGMA_VGCF_OVERRIDE` 는 없다 (감시 셸이 러너 축 이름꼴의 env 를 전부 걷어낸 뒤 위 값만 넣는다).
- `--show-results` 없음 (값 봉인).

## 등록 R 이 자리표로 둔 값의 근거

| 축 | 값 | 근거 |
|---|---|---|
| CJUNC_LEN_LAW | len_scaled_v0 | `scripts/carbon_junction.py` 상수 `CJUNC_LEN_LAW` (1저자 10-20 Q17) |
| CJUNC_S_MIN_UM | 0.0 | 등록 R §2-1b 11-09 줄 (1저자 11-09 · 0 µm · 바닥만) |
| CJUNC_TOL_FF_UM | 0.07381254285530132 | 채택된 S0 단계 1 계획 `docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.json` 의 values_um.tol_ff (계획 sha256 4da98863…0197bd) |
| STEP3_RTOL | 1e-12 | `scripts/step3_conv_cert.py` 봉인 상수 `CERT_RTOL_MAX` (등록 R §3-5 ⓐ) |
| P2_EXTRA 의 maxiter | 1500000 | 준비 폴더 README §6 (조수 제안 400000 → 본 세션 11-10 결정 1500000 · 바꾸면 이 줄과 블록의 MAXITER 를 같이) |

- 시험 `docs/reviews/rint2_probe6_prep_20261110/tools/test_probe6_read.py` 의 S03 · S05 가 이 줄의 축 이름 · 값을 감시 셸 · 등록 R §10-1 (2) · 코드 상수 · S0 계획과 대조한다.
