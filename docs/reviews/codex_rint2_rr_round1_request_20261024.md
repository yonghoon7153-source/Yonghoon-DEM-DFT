# Codex 회차 ① 요청 — Rint ② RR 묶음 A (A · A′ · A″) + Q9 설계 개정 4 + kgy 실행 환경 (2026-10-24 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 10-22 재검토 판정 (`docs/reviews/codex_review_rint2_rereview_20261022.md` · 검토 핀 `0b3012460` · 등록 R 판정 캠페인 HOLD · S0 단계 1 + SBE 숫자 탐침 조건부 GO) 의 RCA2-01 · 04 · 06 · 08 · 09 를 묶음 A (A · A′ · A″) 로 고쳤고, 독립 사전 공격 리뷰를 코드 두 회차 · Q9 설계 네 회차 거쳤다.  ① 고친 판이 그 반례들을 닫는지 ② Q9 설계 (예측 단계를 여러 기계에 나누기 · 구현 전) 가 구현해도 되는 계약인지 ③ kgy 실행 환경 (Python 3.8) 호환 수정이 R 경로의 뜻을 바꾸지 않는지 판정해 달라.
> **리뷰 핀** = 이 요청서가 든 커밋 (`claude/sdcp-dem-manuscript-si-pqwtv8` · push 됨 · 번호 = ZIP 의 `PIN.txt`) · **비교 기준** = `0b3012460` (10-22 검토 핀 · 그 뒤 이 요청서 커밋 전까지 41 개 · Rint ② — `7799a2ff6` 에 트랙 나눔 인계 문서 · 쪽지 폴더가 같이 들어 있다 · 코드 아님).  ZIP 의 리포 파일은 리뷰 핀의 blob 그대로이고, 나머지 소스 · 시험은 원격 핀에서 읽으면 된다.
> **1저자 결정** — 10-23 Q1–Q8 (수정 계획 `docs/reviews/rint2_rereview_fix_plan_20261022.md` · 전부 (가)) · Q9 (가) 예측 12 단위 · Q10 · Q11 · Q12–Q16 (가) · Q17 · Q18 (가) · Q19 (가) · Q20–Q24 · 10-24 Q1–Q5 (py3.8 · Q9 개정 3) · Q1–Q7 (Q9 개정 4) — 결정 줄 = 진행 기록 `docs/session_20260923_progress.md` 의 10-23 · 10-24 줄.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① 10-22 판정의 RCA2-01 · 04 · 06 · 08 · 09 (원장 `claimed_fixed`) — 최소 해결이 지금 코드에서 성립하는가 (finding 마다 닫힘 / 부분 / 열림) · RCA-06 의 닫는 조건 (= RCA2-01 검증 · 원장 `partial_note`) | RCA2-02 (같은 코드) · RCA2-03 (같은 침대) = 묶음 B · RCA2-05 (시간 · 중단 · 재시도의 계획 봉인) · RCA2-07 (등록 ×100 문구 · 시간) = 묶음 C — 이 회차는 RCA2-05 의 **설계** (Q9 · ②) 만 |
| ② 사전 공격 1 회차 (C1–C5 · 묶음 A′) · A′ 의 C1 남은 것 (정상 FLOAT 기록 거짓 거부 · 묶음 A″) 의 고침이 같은 부류를 닫는가 | 2 차 사전 공격의 X6 (P2 · 기록 안 census 칸 일관 편집 → 거짓 clear) · X3 · X5 (P3) = 묶음 B (1저자 Q20 · Q21 (가)) — §8 한정 |
| ③ Q9 설계 개정 4 (`docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` · 구현 전) — 설계 §9 의 Q-A – Q-M | S0 실측 (kgy 단계 1 = 핀 `89fc47011` · 결과 대기) · 재압밀 침대 (10-23 kgy · 기록 `docs/data/rint2_recompaction_vgcf100_20261023/README.md`) · ⑥ 숫자 탐침 · 계획 봉인 · S0 단계 2 · R 런 = Codex 회차 ② (묶음 B · C + 끝-끝 + S0 + 봉인) |
| ④ kgy 실행 환경 수정 (`SELF-132` · `SELF-133` · 게이트 kgy 판 단계) — 3.11 계산 불변 주장 · scipy < 1.12 CG 대체의 뜻 같음 | 런 결과 · 정량 판정 · 생산 GO (모두 0 건) |
| | `RIMPR-04` · `RINT2-B01` · `RCA-11` (원장 open) |
| | 묶음 보고의 "결정 필요" 가운데 지금 동작을 유지한 자리 (§7 C6) — 결함이면 지적해 달라 · 선택이면 의견만 |

## 1. 보내는 것 (ZIP · 리뷰 핀 blob 그대로 + `PIN.txt`)

| 묶음 | 파일 |
|---|---|
| 이 요청서 · 우리 실행 로그 | `docs/reviews/codex_rint2_rr_round1_request_20261024.md` · `docs/reviews/rint2_rr_fix_evidence_20261023/codex_r1_runs_20261024/` (§5) |
| 묶음 보고 · 지시서 | `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_A.md` · `REPORT_A2.md` · `REPORT_A3.md` · `BRIEF.md` · `BRIEF_A2.md` · `BRIEF_A3.md` |
| 사전 공격 리뷰 (보고 + 탐침 + 로그) | `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/` (1 회차 · 묶음 A diff + Q9 원판) · `preattack2/` (2 회차 · A′ · A″ diff + Q9 개정 1) · `preattack3/` (3 회차 · Q9 개정 2) · `preattack4/` (4 회차 · Q9 개정 3) |
| Q9 설계 · 시간 | `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` (개정 4) · `q9_time_budget.py` · `q9_time_budget.json` |
| kgy 실행 환경 | `docs/reviews/rint2_py38_compat_evidence_20261024/` (README · 도구 · 로그) · `scripts/check_kgy_py38.sh` · `scripts/setup_kgy_py38.sh` |
| 대상 문서 · 지난 판정 · 계획 | 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · kgy 명령 `docs/reviews/rint2_kgy_commands_20261020.md` · 수정 계획 `docs/reviews/rint2_rereview_fix_plan_20261022.md` · 지난 판정 `docs/reviews/codex_review_rint2_rereview_20261022.md` · 재압밀 기록 `docs/data/rint2_recompaction_vgcf100_20261023/README.md` |
| 원장 | `docs/reviews/findings.json` (RCA2-01–09 · RCA-06 · SELF-129 · 132 · 133 · 134) |
| 코드 (`0b3012460` 뒤 바뀐 것) | `scripts/ca_ext_svcf.py` · `scripts/carbon_junction.py` · `scripts/rint_r_chain.py` · `scripts/step3_conv_cert.py` · `scripts/step3_sigma.py` · `scripts/ptfe_face_alpha.py` · `scripts/check_all.sh` · `webapp/templates/mpm_lab.html` · `webapp/static/explain/rint_overview_20261021.html` |
| 코드 (읽기 · 바뀌지 않음) | `scripts/sdcp_gain_vox015_8arm.sh` (러너 · Q9 §3-5) · `scripts/run_contract.py` · `scripts/mpm_webapp_payload.py` · `scripts/ca_s0_census.py` · `scripts/test_ca_s0_census.py` |
| 시험 (바뀐 것) | `scripts/test_ca_ext_b6.py` · `test_ca_ext_runner.py` · `test_carbon_junction.py` · `test_rint_r_chain.py` · `test_rint_r_chain_e2e.py` · `test_step3_conv_cert.py` · `test_step3_target_cert.py` · `webapp/test_ca_ext_labels.py` · `webapp/test_rint_explainer_page.py` |

## 2. 무엇이 바뀌었나 (`0b3012460` 뒤 · 범위는 `git log --oneline 0b3012460..` 그대로)

| 묶음 | 커밋 범위 (첫 → 끝) | 무엇 |
|---|---|---|
| 판정 반입 · 재현 · 계획 | `3ab757457` · `a68abe3ed` · `49a1af626` | 10-22 판정 · 증거 반입 · 우리 트리 재현 (판정값 차이 0) · 수정 계획 Q1–Q8 · 비준 · 지시서 |
| 묶음 A (Q1 · Q8 · RCA2-01 · 04 · 06 · 08 · 09) | `ddbb6cee3` → `bd0e85ce6` (병합 기록 `2a093e5da`) | A1 RCA2-08 · A2 RCA2-01 · 04 · A3 RCA2-09 · A4 RCA2-06 · A5 원장 · A6 변이 생존 상주 시험 (`REPORT_A.md`) |
| 사전 공격 1 회차 반입 | `fdb48d378` | 코드 P2 1 · P3 4 · Q9 설계 P2 4 (`docs/reviews/rint2_rr_fix_evidence_20261023/preattack/PREATTACK_A.md`) |
| 묶음 A′ (C1–C5 · Q12–Q14) | `5182fb1fc` → `e07d8c63b` (병합 기록 `7799a2ff6` · Q9 개정 1) | A7 C1 · A8 C2 · A9 C3 · A10 C4 · A11 C5 · A12 원장 · A12b 상주 시험 (`REPORT_A2.md`) |
| 묶음 A″ (Q17 · Q18) | `e91a1f65e` → `a32fcf32f` (병합 기록 `fe1be7960`) | A13 C1 핵심 조건 = 판에 닿는 성분 안에서 끊은 쌍 수 (새 칸 `n_reach_pairs_cut` · FLOAT 거짓 거부 고침) · A13b 상주 시험 · A14 원장 (`REPORT_A3.md`) |
| 재압밀 기록 | `46abdde9e` | VGCF E 100 GPa 두 침대 (kgy · 기록만 · `SELF-130` · `131`) |
| 사전 공격 2 회차 · Q9 개정 2 | `919906a3e` · `9a72d65c6` | 코드 P2 1 (X6) · P3 3 · Q9 P2 1 · P3 4 (`docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/PREATTACK_A2.md`) · Q20–Q24 |
| kgy 실행 환경 · Q9 개정 3 | `89fc47011` (`SELF-132`) · `c8056df9c` (`SELF-133` · 게이트 kgy 판 단계 · Q9 개정 3) | §4 |
| 10-24 결정 · 사전 공격 3 · 4 회차 · Q9 개정 4 | `89fc47011` (3 회차 반입) · `4040e4388` (10-24 결정 = 채택 뒤 시도는 멈춤 · gabia = kgy 판 · `SELF-133` claimed_fixed) · `dcde5cd96` (4 회차 반입) · `17b89a983` (개정 4) · `f4ac30491` (Q7) | §6 |

## 3. 10-22 finding → 고친 자리 · 시험

| finding | 원장 | 고친 자리 (요지) | 시험 (지금 판 · §5) |
|---|---|---|---|
| RCA2-01 (P2) SV 문턱이 nominal 비를 판정 | claimed_fixed `df0f6f01c` | SV 판정 = 증서 구간 (`ca_ext_svcf.cert_interval` · 아래비 = Gfull_lo / Gcut_lower_hi (내림) > 문턱 = `SV_DEPENDENT` · 위비 = Gfull_hi / Gcut_upper_lo (올림) ≤ 문턱 = 표지 없음 · 그 밖 = `SV_UNCHECKED` · nominal 비 = 기록 · 보고만 · 증서 없는 진단 기록 = 판정 입력 아님) · 웹앱 SV 줄 = 증서 구간 (`584472daf`) · 등록 §5-6 SV 행 (`435e73732`) · A′ C1 (`5182fb1fc` · 끝 증서 ↔ 끊은 그래프 위상 수) · A″ (`e91a1f65e`) | `test_carbon_junction.py` QD5 · QD6 · QD7 · `test_ca_ext_b6.py` S8h′ · S8h″ · S8q–S8t · S8w · S8w′ · `webapp/test_ca_ext_labels.py` |
| RCA2-04 (P3) SV 기록의 증서 · 규칙 · 제거 수 결합 | claimed_fixed `e91a1f65e` | 기록 계약 조임 (`_pos_cert_problem` · `_topo_problem` ①–⑧ · `CERT_TOPO_KEYS`) · `read_run` 이 기록의 주 증서 · 위상 수를 런의 주 증서와 대조 (다르면 `CA_EXT_RECORD`) · kind · rule = `SV_CF_KIND` · `SV_CF_RULE` 만 (A′ C5 `5cf848157`) · 새 칸 `n_reach_pairs_cut` (A″) | `test_carbon_junction.py` QD5 · QD7 · `test_ca_ext_b6.py` S8n · S8q–S8t · S8w · S8w′ · SM2 · `test_rint_r_chain.py` V32 · V35 |
| RCA2-06 (P3) F4 첫 성분만 제거 변이 · F6 census 불일치 경로 | claimed_fixed `afa5cad8b` | F4 = 두 성분 상주 시험 QD4 (코드 변경 없음) · F6 = 검증기가 `unsplit_census_mismatch` 를 자기 꼴로 받음 (`_mismatch_problem`) · 사슬 사유에 상태 이름 (`sv_corner_label`) · 시험 = `run_contract.ca_ext_record_ok` 경로 | `test_carbon_junction.py` QD4 · `test_ca_ext_b6.py` SM0–SM4 |
| RCA2-08 (P3) 유한 중간값 합산 넘침 → 예외 | claimed_fixed `ddbb6cee3` | `step3_conv_cert` 최종 U · W 합 넘침 → `NOT_CERTIFIABLE` (구조화) · 원장 허용폭 넘침 = 원장 문제 | `test_step3_target_cert.py` T24 (고치기 전 1/7) |
| RCA2-09 (P3) DBE R 단조 방어 검사 부재 | claimed_fixed `720e401eb` | `Predict` 안 R 단조 검사 · 새 멈춤 `R_MONOTONE_VIOLATION` (`aa2bf5a73`) · A′ C3 = 이미 구한 origin 마다 (`7603139b6`) · C4 = 띠 = 증서 구간 [scale·target_lo, scale·target_hi] · 증서 칸 없음 = `ARM_UNREADABLE` (`720e401eb`) | `test_rint_r_chain.py` U17 · U17b · U19 · U20 · M44–M50 · V33 · V34 |
| RCA-06 (P1 · 부분) | claimed_fixed `eb571a458` (부분 메모) | 닫는 조건 = RCA2-01 검증 (원장 `partial_note`) | 위 RCA2-01 행 |

## 4. kgy 실행 환경 (10-24 · `SELF-132` · `SELF-133`)

- 발견: kgy `~/dem-venv` = Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 (1저자 출력).  개발 · 게이트 · 지난 Codex 회차는 3.11 · numpy 2.4.6 · scipy 1.17.1 에서만 돌았다.  kgy S0 단계 1 (핀 `fe1be7960`) 이 `ptfe_face_alpha.capsule_summary` 의 dict `|` (3.9+) 에서 멈췄다 (잘못된 숫자 없음 · 폴더 보존).
- `89fc47011` (`SELF-132`) = 최소 수정: dict `|` → `{**a, …}` · `ca_ext_svcf._div_dir` 의 `math.nextafter` (3.9+) → `_nextafter` (3.9+ 는 `math.nextafter` 그대로 · 3.8 은 IEEE 754 한 칸 · 1,600,144 쌍 차이 0 = `docs/reviews/rint2_py38_compat_evidence_20261024/logs/check_nextafter.out` · 상주 시험 `test_carbon_junction.py` QD6x) · 시험 넷 (접합 · b6 · 사슬 · 목표 증서) 의 같은 꼴 · 러너 · 끝-끝 시험의 가짜 `python3` 심 = `abspath(sys.executable)` (`realpath` 면 venv 밖).
- `c8056df9c` (`SELF-133`) = scipy < 1.12 의 `cg(tol=…)` (legacy 정지) 를 피함: `step3_sigma` 의 모듈 이름 `cg` = scipy ≥ 1.12 이면 scipy `cg` 그대로 · 옛 판이면 `_cg_v112` (scipy 1.17.1 `cg` 반복을 옮긴 것) · 시험 먼저 K4b–K4d (3.11 에서 `_cg_v112` 와 scipy 1.17.1 `cg` 의 해 바이트 · info · callback 수 같음 · 네 계) · 옛 커밋 기반 모듈과 끈 경로를 비트 대조하는 세 시험은 3.8 에서만 기반 모듈에도 같은 `cg` 를 넣는다 (3.11 = 아무것도 안 바꿈).
- 재발 방지 = 게이트 단계 `scripts/check_kgy_py38.sh` (R 경로 11 묶음 · uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 판이 다르거나 없으면 실패).  ⚠ kgy 는 3.8.10 — 패치 판이 다르다 (Q9 Q3 = 부 판까지 같음 규칙) · 다른 패키지 판은 kgy `pip freeze` 대기.
- 3.11 계산 불변 주장의 근거 = 3.11 에서 바뀐 자리가 같은 함수를 부른다 (`math.nextafter` · scipy `cg`) + 옛 커밋 모듈과 비트 대조하는 상주 시험 (`test_carbon_junction` C0 = 기반 `d1768cf0c` · `test_step3_conv_cert` K1 · `test_step3_target_cert` T12 · T23 — §5 에서 통과) + 게이트 (`f4ac30491` = 156 ✓ · 0 ✗).

## 5. 실행 (리뷰 핀과 같은 코드에서 우리 실행 · 로그 = `docs/reviews/rint2_rr_fix_evidence_20261023/codex_r1_runs_20261024/`)

- 코드 = `f4ac30491` (요청서 커밋은 문서만 더한다 · `env.txt` 의 `code_clean=yes` = scripts · webapp 이 HEAD 와 같음) · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · `OPENBLAS_NUM_THREADS=1` · `python3 -I <파일>` · 2026-10-24 08:58 UTC 시작 · 묶음마다 rc = `rc.txt` (20/20 rc 0).

| 묶음 | 파일 · 인자 | 결과 (로그 끝 줄) | 초 |
|---|---|---|---|
| 사슬 | `scripts/test_rint_r_chain.py` | 240/240 PASS | 105 |
| 사슬 끝-끝 (실제 러너 · payload · CPU) | `scripts/test_rint_r_chain_e2e.py` | 16 PASS · 0 FAIL | 115 |
| B6 payload 배선 | `scripts/test_ca_ext_b6.py` | 454 PASS · 0 FAIL | 38 |
| 탄소 접합 | `scripts/test_carbon_junction.py` | 441/441 PASS | 13 |
| S0 표현 원장 | `scripts/test_ca_s0_census.py` | 152 PASS · 0 FAIL | 15 |
| 러너 | `scripts/test_ca_ext_runner.py` | 128 PASS · 0 FAIL | 62 |
| Z1 | `scripts/test_ca_ext_z1.py` | 95 PASS · 0 FAIL | 26 |
| Z3 | `scripts/test_ca_ext_z3.py` | 84 PASS · 0 FAIL | 24 |
| 판정기 소비자 | `scripts/test_ca_ext_verdict.py` | 31 PASS · 0 FAIL | 26 |
| 목표량 증서 (빠른 판) | `scripts/test_step3_target_cert.py` | 260/260 PASS | 13 |
| 목표량 증서 (긴 판) | `scripts/test_step3_target_cert.py --long` | 309/309 PASS (T18 변이 37 · T17c3 생략 = 이 기계에서 `OPENBLAS_CORETYPE` 이 경로를 안 바꿈) | 856 |
| 수렴 증서 | `scripts/test_step3_conv_cert.py` | 30/30 PASS (K4b–K4d 포함) | 71 |
| S1 PTFE 면 개구율 | `scripts/test_ptfe_face_alpha.py` | 242 PASS · 0 FAIL | 57 |
| 계면 영수증 | `scripts/test_rint_receipts.py` | 102 PASS · 0 FAIL | 26 |
| 실행 계약 | `scripts/run_contract.py --selftest` | 124/124 PASS | 0 |
| STEP3 rint 자체시험 | `scripts/step3_sigma.py --selftest-rint` | PASS | 1 |
| 웹앱 표지 | `webapp/test_ca_ext_labels.py` | 84 PASS · 0 FAIL | 0 |
| 웹앱 설명 페이지 | `webapp/test_rint_explainer_page.py` | 62/62 PASS | 1 |
| 웹앱 비교표 | `webapp/test_mpm_lab_cmp_absent_phase.py` | 23/23 | 1 |
| kgy 판 (uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1) | `scripts/check_kgy_py38.sh` (로그 `kgy_py38/`) | 11 묶음 통과 — 계약 124 · rint PASS · S1 242 · 접합 441 · b6 454 · 러너 128 · 사슬 240 · 끝-끝 16 · 목표 증서 260 · 수렴 증서 29 (K4b = 비교 대상 `cg(rtol=)` 없어 건너뜀 · 세지 않음) · S0 152 | 490 |

- ⚠ 끈 경로 비트 대조 (b6 B · Z3 O · 러너 NB · S1 B) 는 **이 실행에서 건너뛰었다** — 기반 커밋 사본 인자 (`--old-scripts` · `--old-runner`) 를 주지 않아 각 시험이 "건너뜀" 으로 적었다.  아래 끈 경로 수 = 묶음 보고의 기록 (에이전트 실행).

- 끈 경로 (묶음마다 · 묶음 보고 §4 · §5): b6 `--old-scripts --only=B` 30/30 · z3 `--old-scripts --only=O` 11/11 · SV 켬 세 fixture = σ · n_dof 같음 · 차이 = 더해진 칸만 (A′ = 투영의 `target_n_*` 넷 + `rule` · A″ = `n_reach_pairs_cut`).  "차이 0" 이 아니다.
- 변이 (묶음 보고): A 34/41 → 상주 시험 뒤 41/41 · A′ 25/29 → 29/29 · A″ 22/24 → 24/24 · 2 차 사전 공격 33 중 32 (남은 1 = 동등 변이).

## 6. 사전 공격 리뷰 (CLAUDE.md ①–④)

| 회차 | 대상 | 결과 | 처분 |
|---|---|---|---|
| 1 (10-23) | 묶음 A diff + Q9 원판 | 코드 P2 1 · P3 4 · Q9 P2 4 | C1–C5 = 묶음 A′ (Q12–Q14) · D1–D7 = Q9 개정 1 (Q15 · Q16) |
| 2 (10-23) | A′ · A″ diff + Q9 개정 1 | 코드 P1 0 · P2 1 (X6) · P3 3 · 변이 33 중 32 · Q9 P2 1 · P3 4 · 질문 2 | X6 · X3 · X5 = 묶음 B (Q20 · Q21) · Q9 개정 2 (Q22–Q24) |
| 3 (10-24) | Q9 개정 2 | P1 0 · P2 5 · P3 15 · 질문 6 | Q9 개정 3 (1저자 10-24) |
| 4 (10-24) | Q9 개정 3 + 10-24 결정 | P1 0 · P2 4 · P3 9 · 질문 5 · 3 회차 26 = 닫힘 22 · 부분 4 | Q9 개정 4 (Q1–Q7) — 5 회차 없이 이 회차로 (1저자 Q6) |

- ① 숫자 · 전칭 ↔ 출처: §5 의 시험 수 = 위 환경에서 리뷰 핀 코드로 다시 돌린 출력 · 커밋 범위 = `git log` · 원장 상태 = `findings.json` · 묶음 보고의 수 = 그 보고의 에이전트 출력 (메인이 다시 돌린 것은 각 보고의 메인 메모).
- ② 바뀐 함수에 지난 HOLD 부류 (NaN · ±inf · 넘침 · 빈 · 중복 · bool · 옛 칸만 · 다른 판본 · 바꿔 끼우기) — 묶음 보고 §2 · §5 · 2 차 사전 공격 X1–X7.
- ③ 독립 에이전트 (고친 사람 설명 없이 · 보장마다 작은 해석 반례 · 판정문 탐침 재실행) — 네 회차 · 메인 재현 = 각 폴더 README · 4 회차 메인 재현 = `docs/reviews/rint2_rr_fix_evidence_20261023/preattack4/logs/_repro_main/` (다섯 탐침 판정값 같음).
- ④ 닫는 것 / 닫지 않는 것 = §0.

## 7. 판정 요청 질문

| # | 질문 |
|---|---|
| C1 | §3 의 finding 마다 닫힘 / 부분 / 열림 (최소 해결 ↔ 고친 자리 · 반례 재실행) · RCA-06 닫는 조건. |
| C2 | A′ C1–C5 · A″ 의 고침이 같은 부류를 닫는가 — 특히 C1 관계 집합 (⑥ 새 칸 0 ⇔ 위상 수 = 주 해 · ⑧ 생산자 보장 부등식만) 과 §8 의 한정 (a) (b) (c) (a′) (b′) · k = 0 경계가 한정으로 충분한가 · 결함인가. |
| C3 | X6 (P2) · X3 · X5 를 묶음 B (census 세 칸을 기록 밖 출처에 묶음 · RCA2-03 과 같은 자리) 로 미룬 것이 S0 단계 1 · ⑥ 숫자 탐침 전에 막아야 할 결함인가 (R 런 전에는 묶음 B 가 먼저다). |
| C4 | Q9 설계 개정 4 — 설계 §9 Q-A – Q-M (합치기 = 같은 판정 함수 다시 계산 · 부분 채택 · 시도 원장 차례 · 조상 · 접두 · 첫 풀이 끝 표지 · 재실행 자격 · 환경 · 칼날 목록 · 순서 변경 우선순위 · 구조 칸 대조 · 사다리 시도 원장). |
| C5 | kgy 실행 환경 수정 (§4) — 3.11 계산 불변 · `_cg_v112` 가 scipy ≥ 1.12 `cg` 와 뜻이 같다는 주장 · 게이트 단계 (uv 3.8.20 · 부 판까지) 가 kgy 3.8.10 의 증거로 충분한가. |
| C6 | 묶음 보고의 "결정 필요" 가운데 지금 동작을 유지한 자리 — REPORT_A §10 1–10 (1저자 10-23 *"ㄱ"* = 지금 동작) · REPORT_A2 §8 4–9 (메인 메모 = 지금 동작 + 이 요청서) · REPORT_A3 §9 2–4 (판에 닿음 = 끊기 전 그래프 · 칸 이름 `n_reach_pairs_cut` · 새 칸 꼴 검사 = 옛 칸과 같은 대우).  예: 주 증서 불일치 = 기존 `CA_EXT_RECORD` 재사용 · 위비 넘침 → None · 아래비 넘침 → 최대 float · R 단조 띠 = 증서 오차만 (τ_mono 안 더함) · `R_MONOTONE_VIOLATION` = 멈춤 · C4 σ 환산 = 증서 scale · C3 기록 꼴 (`origins` · 넘친 모서리) — 결함으로 보는 것만 지적해 달라 (선택이면 의견). |
| C7 | 판정문 탐침 호환 — ⓐ registration 탐침 (`probe_registration_current.py`) 의 `dbe_nonmonotone` · `dbe_origin` · `sv_origin_scope` 는 합성 팔에 증서 칸 (`target_lo` · `target_hi` · `scale`) 이 없어 지금 트리에서 `ARM_UNREADABLE` 로 멈춘다 (C4 계약 · 2 차 사전 공격 X 표 P3) — 같은 증서 칸을 넣은 사본 = 옛 ↔ 끝 466 exact · 다름 0 · Codex JSON 대비 464 exact · R 단조 절 키만 다름 = `R_MONOTONE_VIOLATION` (REPORT_A2 §6) · 칸을 싣는 기록 꼴 예 = `docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/tools/atk2_rmono.py` 의 `rec()`  ⓑ geometry 탐침이 증거를 census · `I_bot_code` · fp 없이 만들어, 조여진 기록 계약이 그 정상 기록을 칸 없음으로 거부한다 (REPORT_A §6) — 다음 탐침에 그 칸들을 넣어 줄 수 있는가 (REPORT_A §10 결정 12 · 1저자 10-23 *"ㄱ"* = 이 요청서에서 묻는다). |
| C8 | 다음 순서 — kgy S0 단계 1 (핀 `89fc47011` 이상 · 개발 자료) → 묶음 B (RCA2-02 · 03 · X6 · X3 · X5 · 시험 먼저) → 묶음 C (Q4 재시도 봉인 · Q9 구현 · RCA2-07) → Codex 회차 ② (B · C + 끝-끝 + S0 + 봉인).  S0 단계 1 결과를 읽기 전에 막아야 할 것이 있나. |

## 8. 알려진 한정

- **C1 한정 (기록 편집 꼴 · 1저자 Q18 · Q19 (가))** — (a) 아래 끝 ← 주 해 증서 · (b) 위 끝 ← 주 해 증서 = 옛 칸 (`n_sv_faces_cut` · `n_edges_cut`) 과 새 칸 (`n_reach_pairs_cut`) 을 **모두** 0 으로 맞춘 편집만 받는다 · (c) 위 끝 ← 아래 끝 증서 = 받는다 (생산자 보장 = 위 ≤ 아래 · 같음 허용) · (a′) (b′) 새 칸만 0 으로 맞춘 편집 = 정직한 FLOAT · 위 끝 FLOAT 기록과 같은 꼴이라 기록 안에서 못 가른다 (위 끝 풀이 기록이 있으면 ⑧ 이 아래 끝 편집을 잡는다) · **k = 0 경계** (2 차 사전 공격 §A 끝) = k = 0 (끊은 쌍 0) 기록은 편집 없이도 바꿔 끼우기가 받아진다 — 해가 되려면 k = 0 이면서 병렬 간선 때문에 G 가 실제로 줄어야 하는데 그런 기록은 찾지 못했다 (추정: 원리상 가능) · 위상 수 자체를 지어 낸 위조는 이 대조 밖.
- **X6 (P2 · 묶음 B)** — 못 가른 덩어리 수 `n_unsplit_bridging_components` 와 증거 `census` 의 같은 칸을 **둘 다** 0 으로 고치고 위 끝을 지우면 계약을 지나 `SV_UNCHECKED` → `[]` (거짓 clear) · 생산자 기록 5 (QD2-3 · QDX · RAIL5 · QD2-1 · QD4) · census 를 안 고치면 5/5 거부 · 메인 재현 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/logs/main_recheck_atk2_census.json`.  기록 안 여러 칸을 일관되게 고치는 편집은 기록만으로 못 막는다 → 묶음 B 가 census 를 기록 밖 출처 (같은 침대 S0 보고) 에 묶는다.
- **X3 (P3 · 묶음 B)** 아래 끝 ← 위 끝 증서 (QDX · 판정은 보수 쪽 UNCHECKED → DEPENDENT) · **X5 (P3 · 묶음 B)** 새 칸 꼴 · 관계 검사가 비를 싣는 끝이 있을 때만 돈다 (판정 영향 없음).
- **BLAS 계산 경로** — 같은 코드 · 같은 스레드 수라도 `OPENBLAS_CORETYPE` 만 바뀌면 σ 가 상대 1.3e-10 – 5.8e-10 다르다 (1 회차 사전 공격 D2 · 실측) → float 같음 대조는 한 프로세스 안에서만 뜻이 있다 (Q9 개정 3 이 no-op 을 사다리 단계 끝 같은 프로세스로 옮긴 이유) · `test_step3_target_cert.py --long` 의 T17c3 은 이 기계에서 경로가 안 바뀌어 생략된다.
- **kgy 판** — 게이트의 kgy 판 = uv CPython 3.8.20 (kgy 3.8.10) · numpy · scipy 판은 같다 · 나머지 패키지 = kgy `pip freeze` 대기 · gabia 판 = 1저자 출력 대기 (다르면 kgy 판 venv · 1저자 10-24).
- **Q9 = 설계만** — 원장 · 합치기 · 첫 풀이 끝 표지 · 프로세스 그룹 kill · 시도 폴더 안 payload 는 구현 전 (묶음 C · 시험 먼저) · 원장 밖 그림자 런 = 규칙 (원장 밖 킷 풀이 금지 · Q7) 으로만 막는다.
- **S0 실측 없음** — kgy 단계 1 결과 대기 · RCA-11 (S0 표본화 · s_min) open · 단계 1 (핀 `89fc47011`) = 개발 자료 — `S0_SAME_FILES` 일곱 가운데 `step3_sigma.py` 가 그 뒤 `c8056df9c` (K4 · 3.11 계산 같음) 에서 바뀌었으므로 R 에 쓰는 S0 보고는 R 끝 핀에서 다시 만든다 (REPORT_A §9 · REPORT_A3 메인 메모와 같은 규칙).
- **결과 0 건** — R 런 · 판정 결과는 없다.
