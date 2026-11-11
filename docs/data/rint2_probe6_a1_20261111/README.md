# Rint ② 개발 탐침 ⑥ 시도 1 묶음 (kgy · 2026-11-11 · σ 봉인)

> 출처 = 1저자가 kgy 의 시도 1 로그 폴더에서 받아 대화에 올린 probe6_bundle.tgz (14,738 B · sha256 eadc906823823e2047690830aa00c0ecc37786d9567181b0410b71e8cd4b6792 = 감시 셸이 status.log 끝에 찍은 값과 같음 · 1저자가 붙여 준 status 끝 세 줄과도 같음).
> 이 폴더 = 그 tgz 를 빈 새 폴더에 풀어 둔 파일 12 개 (바이트 그대로 · 가림 없음 — 감시 셸이 홈을 ~ 로 접어 적고, 주소 · 호스트 이름 · 계정 이름은 풀린 파일에 없다 (훑어봄)). tgz 자체는 넣지 않았다 (tar 머리에 계정 이름이 든다).
> 지위 = 개발 탐침 사전 원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` §3 시도 1 의 결과 기록. 등록 R · 봉인 · R 런 · 실행 GO 가 아니다. σ 는 열지 않았다 — 묶음에 없고, 팔 JSON · 영수증 · runner.log 는 kgy 의 출력 · 로그 · 킷 런 폴더에 그대로 있다 (준비물 `docs/reviews/rint2_probe6_prep_20261110/README.md` §3 σ 비열람 칸).

## 1. 대조 (본 세션 · 11-11)

| 대조한 것 | 결과 |
|---|---|
| 묶음 안의 `SHA256SUMS` | 11/11 같음 (`sha256sum -c`) |
| meta 의 판독기 · 감시 셸 sha256 | 7293a43f… · d603b068… = 핀 `5bca50c88` 의 `docs/reviews/rint2_probe6_prep_20261110/tools/probe6_read.py` · `docs/reviews/rint2_probe6_prep_20261110/tools/run_probe6.sh` 와 같음 |
| meta 의 러너 sha256 | f964f3f3… = 핀의 `scripts/sdcp_gain_vox015_8arm.sh` 와 같음 |
| meta 의 S0 계획 sha256 | 4da98863… = 채택된 S0 단계 1 계획 (`docs/data/rint2_s0_sbe_20261108/README.md` 의 cjunc_plan.sha256 줄) 과 같음 |
| `command.txt` 의 러너 줄 | 원장 §3 시도 1 러너 줄에 출력 폴더 · 작업 트리 자리만 채운 글과 글자 같음 |
| meta 의 시도 · 한도 · 핀 | attempt 1 · maxiter 30000 (등록 짝) · pin 5bca50c8829b3845529bae4fb7bfe5952208b216 (발사 블록의 PIN = 그때 stoic 끝) |

## 2. 결과 (판독기 표 = `probe6_screen.txt` · `probe6_report.json`)

| 항목 | 값 |
|---|---|
| 판독 | rc 3 (PROBE_NOT_CONVERGED) = 시도 1 의 정상 끝 (한도에 닿음) · 문제 = 미수렴 하나뿐 · 같은 침대 · tol_ff · 핀 · R_j 등록값 (1e6) 대조 = 전부 참 · 영수증 arms 1 · origin 0 |
| 미지수 | 26,529,223 (판 접점 아래 11,769 · 위 9,578) |
| 반복 | 주 풀이 30,000 (한도) · ⓒ 이어 풀기 30,000 (한도) |
| 잔차 | 4.81885e-07 (주 풀이 rtol 1e-12) |
| 판 전류 불균형 | 1.02382 (증서 ⓑ 문턱 1e-4) |
| 증서 | conv-cert-v2 · 상태 POSITIVE_SOLVED · ⓐ ⓑ ⓒ ⓓ 모두 거짓 · 성분 상태 unconverged · 백엔드 gpu · Jacobi |
| 시간 | 전체 7,667 s (러너 rc 1 = 미수렴 팔 거부 · 러너 ABORT) · 런 전 101 s · 래스터 준비 4,487 s (그중 탄소 접합 준비 4,038 s · face_alpha 32 s) · CG + 증서 3,049 s |
| 반복당 | 0.0508 s (= 3,049 s / 60,000 반복 · ⓓ 증서의 CPU 계산이 들어 있어 위 한계) |
| 메모리 | 러너 그룹 RSS 최대 33,433,904 kB (끝 무렵 · 경과 7,586 s) · `time -v` 최대 34,978,676 kB · 감시 셸 상한 41 GB 에 안 닿음 |
| GPU | 전체 사용 최대 14,044 MiB (발사 전 다른 프로세스 5,727 MiB 포함) · 우리 몫 = 표본 없음 (nvidia-smi 가 프로세스별 사용량을 안 보여 줌) |
| 끝 표지 · meta | DONE · solve_started 1 · aborted 0 · cap_term 0 · orphans 0 · git_lines_after 0 · pythonpath_set 0 |
| 킷 런 폴더 새 파일 | 3 (생성 스크립트 · peak RSS 기록 · 미수렴 팔 .failed 129,561,005 B · 셋 다 로그 폴더에 바이트 사본) |

## 3. 시도 2

- 11-11 13:32:48 KST 발사 (1저자 · 같은 핀 · 같은 블록의 ATTEMPT=2 · 한도 1500000 · 감시 셸 상한 41 GB · 발사 전 GPU 사용 6,325 MiB = 다른 프로세스). 앞 조건 (풀이를 시작한 시도 1 의 DONE 하나 · 두 핀 사이 풀이 코드 같음) 은 블록 · 감시 셸이 확인하고 띄웠다. 결과 = 원장 §3 2 번 줄 (끝난 뒤).

## 4. 한정

- 한 점이다 (SBE · arm 0 · R_j 1e6 Ω · P0 · c 0 · 한도 3 만). 필요한 반복 수는 이 한 점으로 정하지 않는다 — 시도 2 의 한도 1500000 은 시도 1 을 보기 전에 정한 값 그대로다 (원장 §3).
- 반복당 초는 위 한계다. 같은 GPU 를 다른 프로세스가 함께 썼다 — 시간에 미친 영향은 미확인.
- 메모리 최대는 미수렴 경로의 값이다. 수렴한 팔의 끝 경로가 쓰는 메모리는 이 묶음으로 모른다.
- 실패 줄 6 개는 판독기가 수를 `#` 로 가린 꼴로만 있다 (`runner_filtered.log`).
