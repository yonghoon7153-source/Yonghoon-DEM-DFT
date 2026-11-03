# Codex 회차 ② 요청 — Rint ② RR 묶음 B · B″ · C + 사전 공격 5 · 6 · 7 회차 고침 + Q9 설계 개정 5–7 + 등록 R §10-5 + kgy 3.8 판 (2026-11-03 · 초안 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 회차 ① (`docs/reviews/codex_review_rint2_rr_round1_20261026.md` · 리뷰 핀 `9bec6b764` · 등록 R 판정 캠페인 HOLD · 새 P1 없음 · 묶음 B 진행 가능 (끝 가중 그래프 귀속 추가) · 묶음 C 조건부 (같은 프로세스 문구 · 부모 사망 종료 확인 · `REVERIFY_DIFF`)) 뒤 RR1-01 · RR1-02 · RCA2-02 · 03 · 04 · 05 · 07 · X6 · X3 · X5 를 묶음 B · B″ · C 로 고쳤고, 그 고침을 독립 사전 공격 세 회차 (5 · 6 · 7) 로 다시 깨서 나온 PC5 · PC6 · PC7 을 고쳤다.  ① 고친 판이 회차 ① 의 finding 과 조건 셋을 닫는지 ② 사전 공격 5–7 회차 고침이 같은 부류를 닫는지 ③ Q9 설계 개정 5–7 · 등록 R §10-5 의 규칙이 사슬 구현과 같은지 ④ 빠진 물리 원장 (§6) 의 한정 행으로 판정 문장이 서는지 판정해 달라.
> **리뷰 핀** = PIN = (push 뒤 채움) · **비교 기준** = `9bec6b764` (회차 ① 리뷰 핀) — 그 사이 커밋에는 Rint ② 밖 트랙 (50kg · LHS214 · 믹서 · 웹앱 그림 · 주간보고) 이 섞여 있다 · Rint ② 범위 = §2 표.
> **지위** — 11-03 작업 트리 초안.  PC7 고침 14 커밋의 본 가지 번호 · 리뷰 핀 · ZIP 지문 · 리뷰 핀 실행 로그 (§5 ⬜ 칸) = 메인 반입 · 전체 게이트 · push 뒤 채운다.  발송 = 1저자.
> **1저자 결정 (시간 순 · 정본 = `docs/handoff_return_to_stoic_knuth_20261103.md` §2-1-2 · 진행 기록 `docs/session_20260923_progress.md`)** — 10-26 *"권고대로해"* (회차 ① 수정 계획 `docs/reviews/rint2_rr1_fix_plan_20261026.md` Q1–Q7) · 10-26 *"다 권고대로 해도 되고 kgy에서 돌리면될듯"* (B″) · 10-27 *"Rint는 권고대로 해도돼"* (묶음 C · 11 월 전체 · 범위 그대로 · 깊이만) · 10-28 *"Rint 권고대로"* (묶음 C 결정 25 + C3) · 10-28 밤 *"rint는 권고대로"* (사전 공격 5 회차 Q1–Q3) · 11-02 *"권고대로해요"* (PC6-13 선택지 A · CUDA 라이브러리 상태 문자열 표지) · 11-02 밤 *"ㅇㅇ 권고대로"* (PC7-01–05 = Codex 전에 고침 · PC7-06 · 07 = 이 요청서 한정 · PC6-13 열린 질문 셋 = 한정) · 11-02 밤 2 *"다 권고대로"* (다음 트랙 = 전해질끼리 이온 계면 · MPM 수치 갱신 = 그 트랙 묶음) · 11-03 (빠진 물리 원장 §6 · 문헌 근거 §7 (Q1–Q3) · 일정 §10 — 메인 전달 · 리포 기록 = 메인 몫 · 이 초안 커밋 때 진행 기록에 줄 없음).

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① 회차 ① 새 finding — RR1-01 (P2 · 끝 증서 ↔ 실제로 푼 가중 그래프) · RR1-02 (P3 · KCL 진단 합 넘침) · RCA2-04 (재개방 · 닫는 조건 = RR1-01) — 묶음 B6 · B7 · B″ (생산 봉인 원천 = 러너 조립만) | 등록 R 판정 캠페인 HOLD 해제 · R 런 · 정량 판정 · 생산 GO (모두 0 건) |
| ② 회차 ① 묶음 C 조건 셋 — 같은 프로세스 문구 · 부모 사망 종료 확인 · `REVERIFY_DIFF` (§3-1 표 · 문서 잔존 다섯 = 한정) | 숫자 칸 (등록 R 의 ⬜ 전부) — 기하 문턱 다섯 (tol_ff · L_par · r_port · tol_P · tol_sj · 식 고정 · 숫자 = S0 단계 1) · s_min · 세 숫자 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) + 세 R 여부 (`sv_cf_scope`) · 실행 정책 넷 (`max_hours` · `max_attempts` · `allowed_machines` · `env_unit`) · 전처리 · maxiter · 시간 상한 (⑥) · 정지 rtol · ε_I · ⓒ (등록 R §11 ⑤) = 봉인 커밋 때 (§10) |
| ③ 10-22 판정의 남은 RCA2-02 (같은 코드) · RCA2-03 (같은 침대) · RCA2-05 (시간 · 중단 · 재시도 봉인) · RCA2-07 (×100 문구 · 시간) + 2 차 사전 공격 X6 · X3 · X5 — 묶음 B · C | S0 단계 1 실측 (10-24 kgy 실행 = STEP3 격자 시작 직후 끊김 · 재실행 전 · 인계 §2-1-1) · ⑥ SBE 숫자 탐침 (개발 탐침 사전 원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` 시도 0 건) · S0 단계 2 · 계획 봉인 |
| ④ 사전 공격 5 · 6 · 7 회차 고침 — PC5-01–08 · 10 · 11 · PC6-01 · 02 · 09 · 12 · 13 · PC7-01–05 (원장 `claimed_fixed`) | 판정 · 재판정의 실물 끝-끝 (실제 러너 · payload → 판정 → 재판정) — 지금 판정 · 재판정 시험 = 가짜 러너 세계뿐 (§3-2 · Q6) |
| ⑤ Q9 설계 개정 5 · 6 · 7 (`docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` §10 · §7 · §3-2 · §3-5) + 등록 R §10-5 가–아 의 규칙 · 이름 · 한정이 사슬 구현과 같은가 | 열린 원장 (§8-1) — PC6-03 · 04 · 05 · 06 · 08 · 10 · PC6-11 (부분) · PC7-06 · 07 · RIMPR-04 · RINT2-B01 · RINTG-01 · RINTG-11 · RINTV-03 · RINT-21 · RINT-22 · RCA-11 · RIMP-02 · SELF-147 · PC5-09 (wontfix) |
| ⑥ kgy 실행 환경 판 (Python 3.8 · numpy 1.24.4 · scipy 1.10.1) 게이트 단계가 새 코드에서도 11 묶음 통과 (§5) | 빠진 물리 (§6) — v0 범위 동결 · 고치지 않는다 · 한정 행으로만 |
| ⑦ 빠진 물리 원장 (§6) 의 한정 행 · 문헌 근거 (§7 · 가져온 것 / 가져오지 않는 것) 로 등록 R 판정 문장 (등록 R §7-1 · §7-2 · §8) 이 서는가 (의견) | 다음 트랙 (전해질끼리 이온 계면 · `MPMC-01`–`03` 고침 · STEP3 σ₀ 1.5 · AM 상 · 계면 항) 설계 |
| | 위조 한정 (등록 R §13-3 B2-Q1 · 회차 ① Q-D) — 원장 밖 그림자 런 · 모든 사본 (원장 · 폴더 · 결과 줄) 의 일관 편집 · 증서 칸 지문까지 원천 값으로 고친 편집 (Q3 로 물음) |
| | TauFactor 외부 대조 (r = 0 복셀 기준선을 다른 FV 코드로 · Codex 10-03 제안) = **미실행** (1저자 11-03 Q3 · §7 e) |
| | 문헌이 빈 자리 (§7 d · 계단 면적 보정 · 섬유–섬유 접합 저항 실측 · MPM 피복 띠) = "문헌 없음 · 모형 내부값" 표지만 · 원문 PDF = 1저자 (11-03 Q2) |

## 1. 보내는 것 (ZIP · 리뷰 핀 blob 그대로 + `PIN.txt`)

| 묶음 | 파일 |
|---|---|
| 이 요청서 · 실행 로그 | 이 파일 · 리뷰 핀 실행 로그 (§5 · 발송 전 메인) · PC7 고침 증거 `docs/reviews/rint2_rr_fix_evidence_20261023/pc7_fix/` (`SHA256SUMS` 76) |
| 회차 ① 판정 · 반입 · 수정 계획 | `docs/reviews/codex_review_rint2_rr_round1_20261026.md` · `docs/reviews/codex_rint2_rr_round1_evidence_20261026/` (우리 트리 재현 `docs/reviews/codex_rint2_rr_round1_evidence_20261026/_repro_ours_20261026/README.md`) · `docs/reviews/rint2_rr1_fix_plan_20261026.md` · `docs/reviews/rint2_dev_probe_ledger_20261026.md` |
| 묶음 보고 · 지시서 (모두 `docs/reviews/rint2_rr_fix_evidence_20261023/` 아래) | `REPORT_B.md` · `REPORT_B2.md` · `REPORT_C.md` · `REPORT_C_decisions_20261028.md` · `BRIEF_B.md` · `BRIEF_C_code.md` · `BRIEF_C_docs.md` · 원자료 `report_c_raw/` |
| 사전 공격 · 고침 (같은 폴더) | 5 회차 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/PREATTACK_C.md` · 고침 증거 `preattack5/fix_pc5_20261028/` · 수정 계획 `docs/reviews/rint2_pc5_fix_plan_20261028.md` · 6 회차 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/PREATTACK_C2_final.md` · 고침 `docs/reviews/rint2_rr_fix_evidence_20261023/pc6_fix/REPORT_PC6_FIX.md` · `docs/reviews/rint2_rr_fix_evidence_20261023/pc6_13_fix/REPORT_PC6_13_FIX.md` · 7 회차 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/PREATTACK_7.md` · 고침 `pc7_fix/` |
| 설계 · 등록 · 명령 · 침대 | Q9 설계 (개정 7) · 시간 `q9_time_budget.json` · `q9_time_budget.py` · 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · kgy 명령 `docs/reviews/rint2_kgy_commands_20261020.md` · 재압밀 기록 `docs/data/rint2_recompaction_vgcf100_20261023/README.md` |
| 원장 | `docs/reviews/findings.json` |
| 코드 (`9bec6b764` 뒤 바뀐 Rint ② 파일) | `scripts/rint_r_chain.py` · `scripts/rint_first_result.py` (새) · `scripts/ca_ext_svcf.py` · `scripts/ca_ext_cjunc.py` · `scripts/carbon_junction.py` · `scripts/ca_s0_census.py` · `scripts/run_contract.py` · `scripts/step3_conv_cert.py` · `scripts/step3_sigma.py` · `scripts/mpm_webapp_payload.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/check_all.sh` (Rint 단계 줄) · `.gitignore` |
| 시험 (바뀐 것) | `scripts/test_rint_r_chain.py` · `scripts/test_rint_r_chain_e2e.py` · `scripts/test_rint_first_result.py` (새) · `scripts/test_ca_ext_b6.py` · `scripts/test_ca_ext_runner.py` · `scripts/test_ca_ext_z3.py` · `scripts/test_ca_s0_census.py` · `scripts/test_carbon_junction.py` · `scripts/test_rint_receipts.py` · `scripts/test_step3_target_cert.py` · `webapp/test_ca_ext_labels.py` · `webapp/test_rint_explainer_page.py` |
| 웹앱 | `webapp/templates/mpm_lab.html` (SV 줄) · `webapp/static/explain/rint_overview_20261021.html` (상자 ⑤ · ⑥ · 날짜 표지) |
| kgy 판 | `scripts/check_kgy_py38.sh` · `scripts/setup_kgy_py38.sh` · `docs/reviews/rint2_py38_compat_evidence_20261024/` |

## 2. 무엇이 바뀌었나 (`9bec6b764` 뒤 · Rint ② 범위만)

| 묶음 | 커밋 (메인 번호 · 첫 → 끝) | 무엇 | 보고 |
|---|---|---|---|
| 회차 ① 반입 · 계획 | `dc0a97212` · `2c9da106b` | 판정 · 증거 · 우리 트리 재현 (판정값 차이 0) · 수정 계획 Q1–Q7 비준 · Q9 개정 5 · 개발 탐침 사전 원장 | 수정 계획 §4 |
| 묶음 B (11) | `198f3a35c` → `f38aec706` (반입 기록 `ce1be4cdc`) | B1 RCA2-02 같은 코드 · B2 RCA2-03 같은 침대 · B2x X6 · B4 X3 · X5 · B3′ 결정 11 · 상자 ⑤ · B5 원장 · 변이 보강 · B6 RR1-01 · B7 RR1-02 · B6 보강 · 한정 꼴 | `REPORT_B.md` |
| 묶음 B″ (9) | `fafd95693` → `0315b085a` (반입 기록 `40d80e97b`) | RR1-01 생산 봉인 원천 = 러너 조립만 (payload `--step3-cjunc-graph-only` · 러너 `CJUNC_GRAPH_ONLY=1` · 사슬 `SV_GRAPH_SOURCE`) · `MPM_NO_VENV=1` · `.venv/` · 메모리 확인 줄 · 위조 한정 · 엄격 검사 셋 | `REPORT_B2.md` |
| 묶음 C3 (문서 · 10-27) | `e743d50c9` → `3c108bba9` | RCA2-07 문구 · §10-4 시간표 (Q9 §6 꼴) · 허용 기계 · 상자 ⑥ · 웹앱 SV 줄 | 등록 R 머리 10-27 줄 |
| 묶음 C1 · C2 (코드 15) | `2c1308bb2` → `db97d0644` | C1a 실행 정책 칸 · C2a no-op = 사다리 끝 · 새 예측 순서 · 이른 R 단조 · C2b 러너 프로세스 그룹 · recover · 첫 풀이 끝 표지 · C1b 시도 원장 · C1b-2 재실행 · C2d 12 단위 · 합치기 · C2e 다시 판정 보고 | `REPORT_C.md` |
| 묶음 C 결정 (10-28) | `f3c84ad7c` → `32455d9c0` (7) | 자원 낱말 표 · `NOT_RESOURCE_WORDS` · 설명 페이지 날짜 표지 · 등록 R §10-5 가–사 · Q9 개정 6 · kgy 개정 4 | `REPORT_C_decisions_20261028.md` |
| 사전 공격 5 회차 · 고침 | 반입 `112a44efe` · `26e9007c6` · 고침 `b9fd47d7b` (시험 먼저) · `6bb3c064f` · `43a8abcaa` · 증거 `87a00ef46` · 원장 `f33e880bd` | PC5-01–08 · 10 · 11 · X09 · X18 · 봉인 전 #4 · #5 · #8 · #9 · Q9 개정 7 · 등록 R §10-5 아 | 수정 계획 · `preattack5/` |
| 사전 공격 6 회차 · 고침 | 중간 `55ac9876b` · 마무리 `8bf1fd6ad` · 고침 `483cf413e` → `f3f6de276` (8) · 반입 기록 `e89243595` · PC6-13 `c738a6826` → `2c1a06c57` (5) · 반입 기록 `0658c0ac6` | PC6-01 · 02 · 09 · 12 · 13 · PC6-11 일부 시험 · CUDA 라이브러리 상태 문자열 표지 · 등록 R §10-5 아 ② · ⑦ | `pc6_fix/` · `pc6_13_fix/` |
| 사전 공격 7 회차 | `3658fa2be` · `2992ab131` · 결정 기록 `c26e72be5` | PC7-01 (P1 후보) · 02 · 03 (P2) · 04–07 (P3) | `docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/PREATTACK_7.md` |
| PC7 고침 (14) | (반입 뒤 메인 번호 · 원 가지 `pc7-fix` = 인계 §3 bundle) | PC7-01 원장 시작 기록 · PC7-02 찾은 폴더 엄격 · PC7-03 recover 길 `chain_exception` · PC7-04 chain_end 표지 · 이름 대조 · PC7-05 등록 R 문구 · 변이 보강 시험 · 증거 | `pc7_fix/` (commit 메시지 · 로그) |

## 3. 회차 ① 조건 — 닫혔나

### 3-1. 묶음 C 조건 셋 (판정문 §7 ① ② ③ · §10)

| 조건 | 판정 | 자리 (문서 · 구현 · 시험) | 남은 것 (한정 · 잔존 문구) |
|---|---|---|---|
| ① "같은 프로세스" → 같은 사슬 부모가 동결한 실행 환경 · 재개 = 새 프로세스 + 원 시도 전체 환경 지문 · 남은 payload 바이트 대조 · 없으면 결정성 가정 | **닫힘 주장 (구현 · 시험)** · 문서 = 부분 | Q9 개정 5 §10 ① (판정문 권고 문구 그대로) · §2-1 40 행 정정 · §7 ㊵ 줄 (201 행) · 구현 C2a `63d092e18` → `db39116f8` (no-op = 사다리 단계 끝 · `scripts/rint_r_chain.py` docstring = "같은 사슬 부모가 동결한 실행 환경 · 런마다 새 러너 자식") · 재개 C1b-2 `a45603c01` → `8b2bc633a` (ResumeRunner · 원 시도 환경 지문 모든 칸 = 풀기 전 대조 · 남은 payload 바이트 `RESUME_MISMATCH`) · 시험 `scripts/test_rint_r_chain.py` NP01–NP08 · RS01–RS06 · 끝-끝 E15 | 옛 꼴 문장 넷 (정정 표지 없음 · 이 요청서 작성 중 발견): Q9 §0 21 행 "no-op 의 자리 (개정 3 = 사다리 단계 끝 · 같은 프로세스)" · Q9 §7 202 행 "사다리 확인 팔을 낸 프로세스가 이어서 돌고" · 등록 R §4-1 136 행 "예측 단계가 법칙마다 SBE c 1 런 하나 (+2 런)" (10-21 사슬 동작 · Q9 §7 이 예고한 §4-1 문구 개정 미반영) · 등록 R §10-4 558 행 "지금 코드는 예측 단계 첫머리에서 no-op 을 돌려" (10-27 시점) — 봉인 전 문서 묶음 (Q2) |
| ② 부모 사망에도 그룹 종료 확인 — 별도 recovery 가 종료를 확인한 뒤 표지 · payload · 폴더 해시 · 확인 못 한 호스트 = 미확인 · 다음 시도 채택 막음 · 러너만 죽이는 시험 ↔ 사슬 부모를 죽이는 시험 분리 | **닫힘 주장 (구현 · 시험)** · 한정 남음 | Q9 개정 5 §10 ② · 구현 C2b `a95d8177d` → `4ed966b5d` (`run_in_group` · 그룹 기록 `.launch.json` · `.end.json` · 종료 확인 뒤에만 팔 읽음 `GROUP_UNCONFIRMED` · `--stage recover`) · 보강 = PC5-03 (산 사슬 recover 안 함) · PC5-04 (다른 부팅 = 기본 미확인 + 운영자 표지) · PC5-07 (Z 지도자 산 스레드 · environ 못 읽음 = 미확인) · PC6-01 (러너 세션 · 계보) · PC6-09 · PC7-01 (원장 시작 기록 · 다른 `--out` · 다른 기계의 두 번째 입구 = 화면만) · PC7-03 · PC7-04 · 시험 GR01–GR14 (GR06 = 사슬 부모 SIGKILL · GR07 = 미확인 rc 3) · PC05 · PC06 · PC06b · PC14 · PD01 · PD01r · PD09 · PD09b · PE01–PE04 계열 · 끝-끝 E13b · E13c (러너만 SIGKILL) ↔ E13e · E13f (사슬 부모 SIGKILL · 따로 프로세스) · E15 | PC6-01 한정 (hidepid=1 = 늘 미확인 · hidepid=2 숨은 조상 = 없어진 것 · setsid + 부모 끝남 + environ 못 읽음 = 놓침 · kgy 실제 = 미확인) · PC7-06 (시험 공백 K01 · K02 · K05 · K07 · K08) · PC7-07 (mkdir → attempt.json 창) · PC6-03 · 04 · 08 · 운영자 표지의 확인 내용 (그 부팅이 끝났음) = 사슬이 검사 못 함 · 실경로 kill = 이 컨테이너의 같은 pid 이름공간뿐 (REPORT_C §12) |
| ③ 구조 (넘침 목록 · 시도 sha · 원장 접두) 가 같아도 최종 등급이 다르면 `REVERIFY_DIFF` · 원 판정 보존 | **닫힘 주장 (구현 · 시험)** · 문서 = 부분 | Q9 개정 5 §10 ③ · 구현 C2e `3529ebf6d` → `f1698cf83` (`verdict_env.json` · `--reverify --out` → `reverify_report.json` · 결과 칸 = 이름만) · 시험 RV01–RV04 (RV02 = 주 판정 · RV03 = 합친 예측 · 구조 대조 통과 + 등급 다름 → rc 1 `REVERIFY_DIFF` · 원 판정 폴더 바이트 그대로) · PC16 (판정 입력 대상 밖 시도는 다시 판정을 흔들지 않음) | Q9 §8 256 행 (개정 3 음성 "첫 합치기와 끝 합치기 (또는 판정) 의 환경 지문 다름") · 259 행 (개정 4 양성 "다른 환경의 다시 판정 = 넘침 목록이 같으면 통과") — §10 이 "함께 정리한다" 고 적었으나 원문 줄 그대로 · 259 행에 "최종 등급이 같을 때만" 이 없다 (구현 RV03 은 등급을 본다) · 실물 끝-끝 다시 판정 시험 없음 (§3-2) |

### 3-2. 회차 ② 진입 조건 (판정문 §10 표 "Codex 회차② / 최종 계획 봉인" 칸)

| 조건 | 지금 | 근거 |
|---|---|---|
| B/C 통합 | 됨 — B · B″ · C · PC5 · PC6 = 메인 가지 · PC7 = 반입 전 (이 초안 작업 트리에만) · 사슬 440 · 끝-끝 40 · kgy 판 11 묶음 = PC7 포함 판 | §5 |
| 작은 실제 producer → 게시 / 판정 → 재판정 | **부분** — 실물 러너 · payload → 팔 계약 · 사슬 `read_run` · 원장 · 재실행 · 합치기 fetch · 봉인 원천 = 끝-끝 E1 · E10–E16 · 판정 · 재판정 = 가짜 러너 세계 (`scripts/test_rint_r_chain.py` RV · U · V · PC16) 뿐 · `scripts/test_rint_r_chain_e2e.py` 에 판정 단계 없음 ("verdict" 0 건) | Q6 |
| 최종 핀 S0 | 없음 — S0 단계 1 재실행 전 (10-24 kgy 실행 = STEP3 격자 시작 직후 끊김 · 1저자 10-28 *"Rint C 끝나고 하자"*) | 인계 §2-1-1 · §2-1-4 #3 |
| 환경 · 비용 자료 | 없음 — ⑥ 시도 0 건 · kgy `pip freeze` · gabia 판 = 기록 없음 (미확인) · 비용 = 합성 침대 어림 (`q9_time_budget.json` · 추정) | §10 |
| 미결 문턱 · 시도 수 · 시간 값 | 봉인 때 (§0 오른쪽 둘째 칸) | 등록 R §2-1 · §11 ④–⑥ · §10-5 가 ② · 나 ③ |

## 4. finding → 고친 자리 · 시험

| finding | 원장 · 커밋 | 고친 자리 (요지) | 시험 · 증거 |
|---|---|---|---|
| RR1-01 (P2) | claimed_fixed `e4714241b` (B6) · 보강 `f9fc67c76` · 한정 꼴 `f38aec706` · 원천 B″ `dccd4b323` · `aba86a2a2` · `75a1f3411` | 끝 증서 = 그 끝에서 실제로 푼 가중 그래프 지문 (`fp_cjunc_graph`) 에 묶임 · 소비자 = 봉인 원천 (러너 조립만 · 같은 env · 풀이 없음) 으로 끝 그래프를 다시 조립해 대조 · 원천 없음 · 실패 = 미확인 → `SV_UNCHECKED` (fail-closed) · 지문 ≠ 증서 = `CA_EXT_RECORD` | `scripts/test_carbon_junction.py` QG · `scripts/test_rint_r_chain.py` RG01–RG13 (RG08–RG13 = B″ 원천) · `scripts/test_ca_ext_b6.py` S · SGF · 끝-끝 E12 · E12a–E12d · E12g · `webapp/test_ca_ext_labels.py` · `REPORT_B.md` §8 · `REPORT_B2.md` §8 |
| RR1-02 (P3) | claimed_fixed `74f84105c` (B7) | 목표량 증서의 raw KCL 진단 합 = 넘침 보호 → 구조화 `NOT_CERTIFIABLE` · 경고 없음 | `scripts/test_step3_target_cert.py` T25 (고치기 전 0/4 → 4/4) |
| RCA2-04 (P3 · 재개방) | claimed_fixed `e4714241b` | 닫는 조건 = RR1-01 (위 행) | 위 행 |
| RCA2-02 (P2) | claimed_fixed `198f3a35c` (B1) · `8661d1d83` | git 신원 엄격 (rev-parse · status 종료코드 · HEAD 40-hex · dirty 엄격 · ignore 밖 untracked = dirty) · 한 단계 사슬 ↔ 러너 대조 · 저장소 상대 코드 키 · CODE_FILES 12 → 18 | `scripts/test_rint_r_chain.py` Y01–Y12 · 끝-끝 E1c |
| RCA2-03 (P2) | claimed_fixed `5497760cf` (B2) | S0 보고 v3 원 입력 · 격자 지문 · R 런 전 · 판정 때 킷 다시 해시 · 다르면 `S0_REPORT_MISMATCH` · 판정 `--root` | `scripts/test_rint_r_chain.py` W01–W10 · B10 · B11 · `scripts/test_ca_s0_census.py` B0 · 끝-끝 E1d |
| X6 (P2) · X3 · X5 (P3) | (RCA2-03 · RCA2-04 원장 메모) `39104710a` (B2x) · `7dc8dc647` (B4) | X6 = SV census ↔ S0 단계 2 봉인 census 외부 결합 (census 결합만 · 그래프 지문 결합 = RR1-01) · X3 · X5 = 위 끝 끊은 쌍 ↔ 아래 끝 그래프 (생산자 칸) · 비를 싣는 기록마다 수 칸 대조 | `scripts/test_rint_r_chain.py` Q01–Q07 · `scripts/test_ca_s0_census.py` E7x0–E7x4 · `scripts/test_carbon_junction.py` QX6 · 끝-끝 E10 · E10a · E10b |
| RCA2-05 (P2) | claimed_fixed `fcf20b822` (C1a) · C1b `ae8ea5ebd` · C1b-2 `8b2bc633a` | 계획 `rint-r-plan-v3` 실행 정책 칸 (값 넷 null = `PLAN_NUMBER_UNREGISTERED`) · `--max-hours` = 계획 값 · `--machine` 필수 · 시도 원장 (git · 덧붙이기만) · `attempt_<n>` · 풀기 전 대조 · 결과 줄 · 채택 · 재실행 | `scripts/test_rint_r_chain.py` EP · AL · RS · `scripts/test_ca_s0_census.py` L3ep · 끝-끝 E1m · E14 · E15 · `REPORT_C.md` §2 · §7 |
| RCA2-07 (P3) | claimed_fixed `e743d50c9` · `3a5143985` · `3c108bba9` (C3) | 등록 R ③ ③′ = 각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음 · §10-4 시간표 = Q9 §6 꼴 (all3) | 문서 (등록 R §3-2b · §10-4) |
| PC5-01–08 · 10 · 11 (P2 6 · P3 4) | claimed_fixed `6bb3c064f` · `43a8abcaa` (시험 먼저 `b9fd47d7b`) | 결과 줄 다시 셈 · 원장 첫 부모 역사 · 자원 낱말 = 메모리 · 디스크 다섯 · 산 사슬 recover 안 함 · 다른 부팅 = 기본 미확인 + 운영자 표지 · 결과 전 멈춘 재실행 = 건너뜀 · 요약 없는 시도 · 사슬 예외 원인 · Z 지도자 산 스레드 · 원장 잠금 · 되돌림 · 다시 판정 = 입력 대상 밖 시도 무관 · 원자료 `report_c_raw/` | `scripts/test_rint_r_chain.py` PC01–PC20 · 변이 32/32 (`preattack5/fix_pc5_20261028/`) · 등록 R §10-5 아 ①–⑫ |
| PC6-01 (P1) · 12 (P1) · 02 · 09 (P2) · 13 (P2) | claimed_fixed `93d8c3d34` · `db2e1b2b4` · `4499f3ffd` | 그룹 원 찾기 = 러너 세션 · 계보 · CUDA 표지 = 모든 길 (+ 라이브러리 상태 문자열 `CUBLAS_STATUS_` · `CUSOLVER_STATUS_` · `CUSPARSE_STATUS_` · `CUFFT_` · `CUDA error:`) · 같은 `--attempt` 재입력 = 화면만 · 찾은 시도 폴더 ↔ 원장 항목 = 한 함수 (호출자 넷) · 그룹 미확인 + 러너 실패 rc = 러너 rc 길 낱말 규칙 | PD01 · PD01r · PD02 · PD02r · PD02c · PD02cr · PD09 · PD09b · PD12 · PD12m · PD12u · PD13 · PD13o · PD13g · PD13r · PD13d · PD11 · PD11m · PD11p · PD11g · PD11s · 변이 49 중 47 (`pc6_fix/`) · 19/19 (`pc6_13_fix/`) · 등록 R §10-5 아 ② · ⑦ |
| PC7-01 (P1 후보) · 02 · 03 (P2) · 04 · 05 (P3) | claimed_fixed (반입 뒤 메인 번호) | 원장 시작 기록 (kind start · 시도 폴더 + attempt.json 뒤 · 러너 전 커밋 · 못 쓰면 rc 3) · 결과 줄 없는 같은 번호의 두 번째 입구 = 바탕 · 기계 무관 화면만 · recover = 결과 줄 폴더 · 요약 sha · 시작 기록 바탕 대조 · 찾은 시도 폴더에 꼴 맞는 attempt.json 없음 (없음 · 꼴 틀림 · 링크) = `ATTEMPT_LEDGER_MISMATCH` (예외 = rejected + 옆 거부 기록) · recover 길 chain_end 원인 exception = `chain_exception` (by chain 길과 같은 표 · 바뀐 칸 = 44 칸 중 exception 행 12) · chain_end 옮김 = 표지 · 이름이 시작 기록과 같을 때만 (다르면 미확인) · 등록 R 나 ⑫ 문구 (정리 중 신호 = 요약 있는 길만) | PE01 · PE01h · PE01r · PE01p (0/4 → 4/4) · PE02 · PE02x · PD12u (0/3 → 3/3) · PE03 · PE03u (0/2 → 2/2) · PE04 (0/1 → 1/1) · 보강 PE01s · PE01c · PE01f · 변이 23/23 (`docs/reviews/rint2_rr_fix_evidence_20261023/pc7_fix/logs/mutation_pc7fix.json` · `mutation_pc7fix_boost.json`) · 등록 R §10-5 나 ⑫ · 아 ⑥ · ⑦ |
| 이어 확인 (회차 ① 표에 없던 claimed_fixed) | SELF-129 `2a093e5da` · SELF-134 `f4ac30491` · SELF-137 `db97d0644` · RINT-23 `d8295601f` | 시간 어림 정정 · 원장 밖 킷 풀이 금지 · 끝-끝 E13 명령줄 자름 (시험 도구) · 탄소 접합 지문 `_fp` 객체 배열 | 원장 각 항목 evidence |

## 5. 실행

- PC7 고침 증거 (11-02 · 고침 작업 트리 · Python 3.11.17 · `pc7_fix/logs/` · 시험한 파일 = `docs/reviews/rint2_rr_fix_evidence_20261023/pc7_fix/logs/tested_code_sha256.txt` 다섯 · 실행 기록 `regression_env.txt` 의 커밋 칸은 cherry-pick 뒤 바뀌어 지웠다 · `SELF-116`).
- 11-03 반입 확인 (이 초안을 쓴 작업 트리 · cherry-pick 14 · 충돌 0 · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · BLAS 스레드 1 · `docs/reviews/rint2_rr_fix_evidence_20261023/pc7_fix/run_regression.sh` 그대로) — 시험한 다섯 파일 sha256 = `tested_code_sha256.txt` 와 같음 (5/5) · `pc7_fix/SHA256SUMS` 76/76 · 로그 = 리포 밖 (작업 트리 스크래치 · 리뷰 핀 실행이 대신한다).

| 묶음 | 파일 · 인자 | PC7 증거 (11-02) | 11-03 반입 확인 | 리뷰 핀 (발송 전 메인) |
|---|---|---|---|---|
| 사슬 | `scripts/test_rint_r_chain.py` | 440/440 PASS (460.1 s) | 440/440 PASS (485.0 s) | ⬜ |
| 사슬 끝-끝 (실제 러너 · payload · CPU) | `scripts/test_rint_r_chain_e2e.py` | 40 PASS · 0 FAIL (502.8 s) | 40 PASS · 0 FAIL (525.9 s) | ⬜ |
| kgy 판 (uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1) | `scripts/check_kgy_py38.sh` | 11 묶음 통과 — 계약 124 · rint PASS · S1 242 · 접합 466 · b6 501 · 러너 151 · 사슬 440 · 끝-끝 40 · 목표 증서 264 · 수렴 증서 29 · S0 167 | 11 묶음 통과 — 열한 수 전부 증거와 같음 (사슬 440/440 · 793.9 s · 끝-끝 40 PASS · 0 FAIL · 426.1 s) | ⬜ |
| PC7 부분 묶음 (고치기 전 → 뒤 · `--only`) | `scripts/test_rint_r_chain.py --only …` | 0/4 → 4/4 · 0/3 → 3/3 · 0/2 → 2/2 · 0/1 → 1/1 · AL 30/30 · PC · PD 42/42 · 사전 공격 7 변이 K09 꼴 52/52 · PE03 묶음 11/11 · PE04 묶음 32/32 · RS 등 9/9 · 문서 7/7 · 3.8 PE 14/14 | 같은 이름 전부 위 전체 실행에서 PASS (부분 묶음 12 개 = 증거와 같은 수 · 고치기 전 판은 다시 안 돌림) | — |
| 변이 (PC7 가드마다) | `docs/reviews/rint2_rr_fix_evidence_20261023/pc7_fix/mutate_pc7fix.py` | 23/23 (첫 판 22 = 잡힘 20 · 생존 F13 · G04 · 약함 F11 → 보강 시험 뒤 F11 · F13 · G04 + 새 F14 잡힘) | 23/23 잡힘 — 한 판 (보강 시험이 이미 들어 있음 · 생존 0 · 변이 없는 BASE 23/23 PASS · 사본 트리 · 리포 밖 로그) | — |
| 원장 · 참조 · 철회 스윕 | `scripts/check_review_findings.py` · `scripts/check_doc_refs.py` · `--ban-sweep` | rc 0 · rc 0 · 등록 42 × 파일 9188 누수 0 | rc 0 (원장 953 · open 331 · claimed_fixed 368 · verified 244 · wontfix 10) · rc 0 | ⬜ |
| 회차 ① 요청서 §5 의 나머지 묶음 | z1 · z3 · verdict · receipts · first_result · target_cert `--long` · 웹앱 표지 · 설명 페이지 · 범위 표지 | (묶음 보고의 수 · 에이전트 출력) | — | ⬜ |
| 전체 게이트 | `scripts/check_all.sh` | (고침 작업 트리 = 안 돌림) | 안 돌림 (이 작업 트리 규칙) | ⬜ |

- 끈 경로 (묶음 보고): 묶음 C = 가짜 러너 세계 두 장면 비트 대조 · b6 B 39/39 · z3 O 15/15 · 러너 NB 2/2 차이 0 (`REPORT_C.md` §4) · 기계 간 결정성 = 같은 컨테이너 CPU 3.11 ↔ 3.8 SBE o0 + DBE o0–7 `sid_fp` 9/9 · σ 9/9 비트 같음 (`REPORT_C.md` §6 · 다른 하드웨어 · GPU · kgy 기계 = 시험 안 함).
- 실경로 kill (묶음 C · 이 컨테이너 같은 pid 이름공간): E13b · E13c · E13d · E13e · E13f · E14 · E15 · E16 (`REPORT_C.md` §8).

## 6. 빠진 물리 원장 (1저자 11-03 · v0 범위 동결 · 새 물리 없음)

> 원칙 — Rint ② v0 는 물리를 더하지 않는다.  빠진 물리는 고치지 않고 **한정 행**으로 적는다 (등록 R §8 "빠진 물리의 크기 = 정보" · 해석 금지 셋 그대로).  보정 손잡이 = R_j,0 하나 (SBE 1.63 mS/cm 한 점 · 법칙 P0 · P1 마다) · DBE 4.68 mS/cm = **비교** (맞춤 대상 아님 · 현 세대 보정에 이미 쓰인 값 = 맹검 아님 · 등록 R §1).  1저자 11-03: Rint 와 MPM 모형 설계는 같이 간다 — 아래 6-2 = 두 쪽이 같이 쓰는 면 · 계면 정의, 6-3 = MPM 쪽 가정이 Rint 로 흘러드는 한정.

### 6-1. 면 · 계면 부류마다 — Rint ② v0 가 표현하는 것 / 안 하는 것

| 면 · 계면 | v0 처리 | 저항 | 근거 | 보고 · 다음 |
|---|---|---|---|---|
| VGCF–VGCF (등록 접합 · VV) | 접합 간선 · 길이 비례 분산판 G_j = max(1, L_c/L_par)/R_j,0 · PTFE 덮임 (P0 · P1) · SDCP 근접 (c 0 · 1) | **보정 R_j,0 하나** — 모형 내부값 (물성 아님 · 격자에 묶임 · 포트 반셀 몫 포함) | 등록 R §2 · 설계 §1-2 · §4-1 · §4-5 | 등록 R §8 늘 보고 |
| VGCF–VGCF (미등록 면) | 융합 (두 셀 σ 조화평균) | 0 | 등록 R §2 (감도 `UNREG` = fused) | 변이 판정 |
| PTFE 가 덮은 면 | 면 개구율 α (S1 · face_alpha · K = 8 구적) · 불투과 | 면적만 줄임 | 등록 R §2 (가정 고정 · `DIA_UNCHECKED`) | — |
| **SDCP–VGCF (SV)** | 융합 | **0 가정 · 보정 안 함** | 설계 §0 K5 (N13) · §4-5 (SV 우회 = DBE 에만 · SBE 보정이 제약 못 함) | 크기 = SV 반사실 비 **두 끝** (아래 끝 = 못 가른 덩어리 그대로 · 위 끝 = 그 덩어리 SDCP 셀 면 전부 끊음 · 등록 R §5-6 SV 행) 으로만 보고 · `SV_DEPENDENT` · `SV_UNCHECKED` · `SV_DOMINANT` 표지 · 필수 한정어 ⑧ *"SDCP–VGCF 접촉 저항 0 가정"* (등록 R §7-1) |
| SDCP 접점 축 c | VV 접합의 시나리오 끝 (c = 1 = 근접 접합 축약) | SDCP 자신의 접촉 저항이 아니다 | 설계 §5-1 (N11) | 같은 P 일관 검사 |
| SDCP–AM (SA) · VGCF–AM (VA) | 융합 | 0 가정 | 설계 §0 K5 · 등록 R §2 | VA 면 소산 몫 · SV 면 · SDCP 셀 소산 보고 (등록 R §8) |
| **AM–AM** | 생산 브리지 (DEM 접촉 쌍 중점 공 · 0.48 µm 고정 · 러너 기본) · ①′ 막 = 끔 (생산 HOLD) | 0 (융합) | 설계 §1-2 #7 · §0 K5 · §5-1 끝 줄 | 활물질끼리 계면 실측 (탄소 없는 전극 σ_e) = 실험 쪽 요청 (1저자 11-02 밤 2) · ①′ 열린 원장 `RINTG-01` · `RINTG-11` · `RINTV-03` · `RINT-21` |
| **AM–SE** | 전자 = SE 전자 σ 0 (탄소–SE 전자 0) · 이온 = 판정 밖 | 계면 항 없음 | 설계 §0 K5 · 등록 R §2 "채널 밖 보정 (이온 · 판정 밖)" | — |
| **SE–SE (이온)** | 융합 (`CONTACT_FREE` 가지 · 계면 항 0) | 0 | `docs/voxel_contact_free_gap.md` · `CL-81` · 설계 §1-1 하지 않는 것 "SE 입계 ③" | **다음 트랙 = 전해질끼리 이온 계면** (첫 침대 50kg D1–D3 · SE 번호 = atom dump 승계 · 1저자 11-02 밤 2) |
| 판 (집전체) | 판 규칙 p2 | 판 결합 그대로 | 등록 R §2 | — |

### 6-2. 두 쪽이 같이 쓰는 정의 (MPM · STEP3 → Rint ②)

| 정의 | 만드는 쪽 | Rint ② 쓰임 | 다음 트랙과 같이 바뀌는 것 |
|---|---|---|---|
| 상 · sid 격자 (vox 0.15 · 감도 GRID 0.125) | STEP3 rasterize — AM 골격 (DEM 최종 좌표 · MPM 이 움직이지 않음) · SE · VGCF · PTFE · SDCP 위치 = MPM 최종 점 (재압밀 README §2 상 표) · SDCP 구 스탬프 Ø0.30 · 우선순위 (SE 가 가장 낮음 · SDCP 가 VGCF 셀을 덮음 · 등록 R §2 N14) | 모든 면 부류의 바탕 | SE 입자 번호 승계 (`scripts/mpm3d_compaction.py --save-se-id` · 50kg 키트 런 = 안 켬) |
| 면 전도 = 두 셀 σ 조화평균 (계면 항 0) | `scripts/step3_sigma.py` `solve_sigma_z` | 그 위에 VV 접합 간선 · α · SV 반사실만 바꾼다 | 이온 계면 항 = 같은 면 연산자 위 (①′ 기구 = 기본 끔 · 정량 채택 · 생산 HOLD) |
| AM–AM 브리지 (DEM 접촉 쌍 · 중점 공) | STEP3 | AM–AM 전자 경로 | ①′ 막 위치 결함 (`RINT-06` · `RINT-21`) |
| 판 · z 위 · 아래 | MPM 판 · STEP3 판 규칙 p2 | 단자 G | — |
| 비주기 격자 (주기 영상 없음 · 측면 = 절연) | STEP3 raster · 정량 모드 `--periodic` 거부 (설계 §3-3 · §3-4 F6 · `scripts/mpm_webapp_payload.py`) | σ_z 해 | MPM 압밀 = x,y 주기 ↔ raster 비주기 (6-3 M4) |

### 6-3. MPM 쪽 가정이 Rint 로 흘러드는 한정 (고치지 않음)

| # | 한정 | 근거 · 원장 | Rint ② σ_e 에서의 크기 |
|---|---|---|---|
| M1 | 격자 ↔ 접촉 크기 — 1 µm 접촉 하나 ≈ 0.093 µm² < 복셀 면 0.16 µm² (vox 0.4 µm 면 · 50kg 키트 기록) · Rint ② vox 0.15 면 = 0.0225 µm² [산술] · 계면 면적 정의가 격자에 묶인다 · R_j,0 = 격자에 묶인 모형 내부값 | 인계 §2-1-2 (11-02 밤 2) · 설계 §4-5 · 등록 R §9 (GRID 필수) · `CL-41` (SDCP 이득 격자 미수렴 · 외삽 불가) | GRID 변이 (vox 0.125) 로만 · 수렴 주장 없음 |
| M2 | MPM coverage (`deformed_coverage` · `geometric_coverage`) = 띠 근접 비율 (닿은 면적 아님) | `MPMC-01` | σ 풀이의 입력이 아니다 — Rint 사슬 · 접합 · SV · S0 코드 여섯 파일 (`scripts/rint_r_chain.py` · `scripts/carbon_junction.py` · `scripts/ca_ext_svcf.py` · `scripts/ca_ext_cjunc.py` · `scripts/ptfe_face_alpha.py` · `scripts/ca_s0_census.py`) 에 "coverage" 0 건 · 같은 payload 런의 다른 출력 · 보고에 안 쓴다 |
| M3 | 점 구름 이산화 치우침 (씨앗 상태 소성 − 강체 +2.3 … +5.1 %p) | `MPMC-02` | SE 셀 점유가 같은 점 구름에서 온다 · σ_e 영향 = 미측정 (SE 전자 σ 0 · 점유만) |
| M4 | x,y 주기 영상 — MPM coverage 두 함수가 경계 너머 SE 를 못 봄 (`MPMC-03`) · Rint raster 도 주기 영상을 만들지 않는다 · Rint 두 킷의 MPM 압밀 = `xy=periodic` · 경계를 넘은 점 SBE SE 7,288 · VGCF 77 · PTFE 12 / DBE SE 5,721 · VGCF 69 · PTFE 6 · SDCP 1 | `MPMC-03` · 설계 §3-3 · §3-4 F6 · `docs/data/rint2_recompaction_vgcf100_20261023/README.md` §2 | 미측정 (측면 절연 해 · 경계를 넘는 섬유 · 접합이 끊긴 꼴) |
| M5 | 압밀 등급 — `quasistatic_violation` True · `platen_mach_VcS` 2.9602 · `stop_mode` legacy_moving (킷 = `--allow-fast-platen` 등급 B · 옛 런도 True) | 재압밀 README §1 | 침대 기하의 지위 (σ 런 아님) · 두 킷 같은 등급 · 크기 미측정 |
| M6 | AM 골격 고정 (DEM 최종 좌표 · MPM 이 AM 을 움직이지 않음) · AM–AM 접촉 = DEM 기하 + 브리지 규약 | `docs/mpm_scaffold_reliability_and_am_freeze.md` | 6-1 AM–AM 행 |
| M7 | 섬유 접촉 역학 없음 — VV 접합 instance = 관통 포함 기하 근접 (MPM 은 섬유 접촉 역학을 풀지 않는다) · 중심선 위치 불확도 | 등록 R §7-1 ⑩ · 설계 §4-5 | 접합 수 · 위치 = S0 표현 원장 (RCA-11 열림) · R_j,0 가 흡수 |

### 6-4. 문장 규칙

- SDCP: *"SDCP–VGCF 접촉 저항 0 가정 (보정 안 함) · 크기 = SV 반사실 비 두 끝"* 을 판정 문장마다 붙인다 · SV 몫을 접촉 저항 값으로 부르지 않는다.
- DBE 4.68: 비교 대상 · 맞춤 대상 아님 · 판정에 한 번만 · 현 세대 보정에 이미 쓰인 값 (등록 R §1 다섯 규칙 그대로).
- AM–AM · AM–SE · SE–SE: *"Rint ② v0 에 없음"* · 불합격이어도 *"접합 저항이 없다"* · *"SDCP 효과가 없다"* · *"PTFE 효과가 없다"* 로 쓰지 않는다 (등록 R §8).
- MPM 상속 M1–M7: 크기 미측정은 미측정으로 적는다 · 격자 수렴 · 외삽 주장 없음.

## 7. 문헌 근거 (1저자 11-03 · 숫자 = litdb 정본 카드 원문 · 정본 `eeb8d13d9`)

> 1저자 11-03 비준 (Q1–Q3) — 문서만 · 새 계산 없음.  숫자는 아래 카드의 원문 줄에서만 옮기고 인용은 `litdb-canon:<slug>` 로 한다.  문헌이 빈 곳은 **"문헌 없음 · 모형 내부값"** 표지만 단다 — 원문 PDF = 1저자가 줄 예정 (Q2) · 후보 서지는 쓰지 않는다 (CLAUDE.md 규율 ⑥).  [인쇄] = 논문에 적힌 값 · [우리 산술] = 카드가 그 값으로 한 계산 (카드 표지 그대로).

| # | 자리 (우리) | 문헌이 주는 것 | 가져오지 않는 것 · 한정 | 출처 |
|---|---|---|---|---|
| a | `CL-81` 출발점 — 복셀 FV 에 계면 저항 항이 없어 σ 가 높게 나오는 쪽 (`CONTACT_FREE` 가지 · `docs/voxel_contact_free_gap.md`) | **실험 지지** — FIB-SEM 재구성 위 복셀 FV 의 σ_ion 시뮬 ÷ 실측 = **1.46 · 1.42** (PTFE 0.0 · 0.2 wt% · 시뮬 4.4 × 10⁻⁵ · 6.9 × 10⁻⁵ S cm⁻¹ ↔ 실측 3.01 × 10⁻⁵ · 4.85 × 10⁻⁵ S cm⁻¹ [인쇄] · 비 = [우리 산술] · 카드 머리 표 ③ · §3-6) | *"계면 · 입계 · 미해상 기공 몫 ≈ 30 %"* = **카드의 해석** (1 − 실측/시뮬 · 원문 주장 아님) · 입력 σ_LPSCl 0.1 S m⁻¹ (= 1.0 mS cm⁻¹ · 출처 미기재) 에 조건부 — 같은 구조에 σ₀ 1.5 · 3.0 이면 2.1–2.2 · 4.3–4.4 배 (카드 [우리 산술]) · 저자는 σ_ion 의 절대 일치를 주장하지 않는다 (경향만 · 카드 §3-6) | `litdb-canon:lee2026_unveiling_ptfe_dry_electrode_digital_twin` (머리 표 ③ · §3-6 · §8-4) |
| b | ① 면 직렬 시트 저항 (`scripts/step3_sigma.py` `solve_sigma_z(rint=)` · ①′ AM–AM 막) | **출판 선례 (형식만)** — 같은 이산화 (6 이웃 면 · 반 복셀 직렬 = 조화평균 · 접촉 · 협착 없음 = 우리 STEP3 의 짝 · 카드 §7-3) 에 Eq. S3 `(0.5/κ_a + 0.5/κ_b + R_int/dx)⁻¹` — 면마다 시트저항 R_int 를 직렬로 (카드 §4-1 · §7-6) | 가져오지 않는 것 ① **값 2 × 10⁻⁶ m² K W⁻¹** — 열 채널 (LPSCl \| NCM83 이종상 링크에만) · *"it is found empirically that better agreement … can be achieved"* (p. 5 · 카드 §3-3) · 해상도에 묶인 적합 상수 (카드 §7-6) ② **전하 채널 R_int** — 그 논문은 전하 채널에 R_int 를 쓰지 않았다 (그 논문 밖 · 카드 §7-6) · **우리가 더한 것 = 문헌 지지 없음**: 같은 상 다른 입자 면 (AM–AM · Eq. S3 는 이종상 링크만) · 계단 면적 보정 (CNC 법칙 r·N_ref·h²/A — 카드 §7-6 ③ 도 "계단 근사가 계면 면적을 부풀린다" 고만 적는다) | `litdb-canon:ketter2025_resistor_network_models_predict_transport_properties` (§4-1 · §7-3 · §7-6 · Eq. S3) |
| c | 탄소 — VGCF 접합 (S2 · 등록 R §2) | **문헌 관행 = 접합 저항을 유효 σ 에 묶는다** — Lee 2026: VGCF 를 복셀로 해상 · 입력 8300 S m⁻¹ (= 83 S cm⁻¹ · 출처 미기재) → σ_e 시뮬 ÷ 실측 **0.99 · 0.97** (카드 머리 표 ⑤ · §3-5) · Ketter 2025: VGCF 를 저항망으로 모사하지 않았다 — *"additives that cannot be simply modelled by a voxel approach"* (p. 6 · 카드 §3-4) | 우리 다음 세대 = 단섬유 σ (등록 R §2 문헌 고정 행 · `litdb-canon:endo2001_vgcf_basic_properties_battery_applications`) + 명시 접합 R_j,0 (SBE 1.63 mS/cm 한 점 보정) ⇒ 접합 법칙 (길이 비례 분산판 G_j = max(1, L_c/L_par)/R_j,0 포함) = **문헌 없음 · 모형 내부값** | 위 두 카드 · 등록 R §2 |
| d | **문헌 없음** (메인의 litdb 정본 `eeb8d13d9` 검색 기준) — 한정어 · 원장으로만 · v0 값 채택 없음 | 계단 면적 보정 (복셀 표면적 추정) · 섬유–섬유 접합 저항 실측 · MPM 피복 띠 0.13 / 0.26 µm (`MPMC-01`) | 원문 PDF = 1저자 (Q2) · 후보 서지 = 쓰지 않음 | — |
| e | TauFactor 외부 대조 — r = 0 (계면 항 끔) 복셀 기준선을 다른 FV 구현으로 같은 격자에서 대조 (Codex 10-03 판정문 Q6 `docs/reviews/codex_review_rint_stage1_20261003.md` — 경계조건 · 전극 셀 · 축 방향 · 상별 σ · pruning · 판을 맞춰야 한다 · 우리 10-03 요청서 §6 `docs/reviews/codex_rint_stage1_request_20261003.md` 외부 대조 후보 줄) | **미실행** (1저자 11-03 Q3) | §0 "닫지 않는 것" | — |

## 8. 알려진 한정 (닫지 않는 것 · 요청서 꼴)

### 8-1. 열린 원장 (Rint ② · 이 회차 고치지 않음)

| 원장 | 한 줄 | 처분 |
|---|---|---|
| PC7-06 (P3) | 시험 공백 (변이 생존) — `_run_kin` 부모 없음 · ppid 없음 (K01 · K02) · recover 의 `runner_start` 무시 (K05) · PC6-09 `mine` 의 기계 · 재실행 원 시도 칸 (K07 · K08) — K01 · K02 · K05 = 보수 쪽 공백 (K02 = 합성 전용) · K07 · K08 = 시험 공백 (사전 공격 7 회차 §3) | 1저자 11-02 밤 = 한계 (고치지 않음) |
| PC7-07 (P3) | `attempt_open` 의 mkdir → attempt.json 쓰기 사이 창 — 빈 `attempt_<n>` 에서 같은 `--attempt` = 옆 거부 · 새 시도 뒤 판정 = "원장에 없는 시도 폴더" (손 정리 전까지 멈춤 · 거짓 수용 없음) | 1저자 11-02 밤 = 한계 |
| PC6-03 · 04 · 05 · 06 · 08 · 10 (P3) | SIGINT = `chain_exception` (재실행 불가) · 원장 덧붙임 중 SIGTERM · SIGHUP · SIGKILL = 되돌림 없음 · 요약 있는 길 런 로그 없음 = 자격 · 사슬 자신의 MemoryError · ENOSPC = `CHAIN_EXCEPTION` · 옆 거부 기록 + 결과 줄 전 죽음 = 그 대상 영구 멈춤 · `--operator-why` 줄바꿈 꼴 · 번호 인자 | 열림 (사전 공격 6 회차 §5 한정 문장 그대로) |
| PC6-11 (P3 · 부분) | PC5 가드 변이 생존 중 M2e · M2c · M9 · M8 · M11 · M12 · M15 = 시험 PD11 계열로 닫음 · 남은 M4 · M5 · M6 · M10a · M10b (보수 쪽 · 작은 fixture 로 못 닿음) | 열림 |
| PC5-09 (P3) | 쓰는 중 · 검사 전 죽은 payload 도 검사 실패 흔적 = 재실행 자격 뺌 (보수 쪽 오거부) | wontfix (1저자 10-28 밤 Q1) |
| SELF-147 (P3) | 11-02 메인 설명 "메모리 부족은 그대로 자원" — 자원 낱말 다섯이 없는 메모리 실패 꼴 (`*_ALLOC_FAILED` · `CUSPARSE_STATUS_INSUFFICIENT_RESOURCES` · 맨 `CUDA error: out of memory`) = `runner_rc` (보수 · 1저자 11-02 밤 = 지금대로) | 열림 (설명 오기) |
| RIMPR-04 · RINT2-B01 · RINTG-01 · RINTG-11 · RINTV-03 · RINT-21 · RINT-22 · RCA-11 · RIMP-02 | 조인 관문 넘침 · 시험 작성기 CRLF · ①′ 순열 · 행 순서 크기 · T2-2b 짝 · r1 위치 · payload `--no-step3` + `--fibre` · S0 표본화 · s_min · 조인 관문 손상 입력 | 열림 (회차 ① 범위 밖 그대로 · RCA-11 = S0 단계 1 뒤) |
| (인계 목록 밖 · 같은 계열) RINT-06 · 07 · 08 · 09 · 15 · 16 · SELF-127 · SELF-128 | ①′ 막 설계 반증 · 단위 · fallback · 불변식 · 캐시 태그 · 소산 버킷 · 사전 리뷰 탐침 숫자 · PB1 기록 문장 | 열림 (①′ = Rint ② v0 에서 끔 · 범위 밖) |

### 8-2. 규칙뿐인 자리 · 구현 한정

- 위조 한정 (B2-Q1) — 증서 칸 지문 (`fp_cjunc_graph`) 까지 봉인 원천 값으로 고친 편집 (증서 수는 다른 끝 그대로) 은 원천 대조로 못 가린다 (지문 = 그래프 정체성 · 증서 수의 재증명 아님 · Q3).
- 원장 (Q-D) — 원장 안 시도끼리만 막는다 · 원장 밖 그림자 런 · 모든 사본 (폴더 · 결과 줄 · 원장) 을 함께 고친 손 · 꼴 밖 이름으로 옮긴 폴더 (`attempt_1.old`) · 바탕 밖으로 옮긴 폴더 = 못 본다 · 원장 · 시도 폴더 쓰기 권한 = 운영 규칙.
- 원장 저장소의 `git replace` · grafts 를 끄지 않는다 (`core.useReplaceRefs=false` 없음 · 결과 줄은 다시 셈이 잡음 · 항목 줄은 위 Q-D 한정) — 사전 공격 6 회차 §5 #9 · 원장 항목 없음.
- GPU 런 재실행 금지 = 등록 규칙뿐 (사슬은 GPU 시도의 `--resume` 을 막지 않는다 · 남은 payload 가 없으면 결정성 가정 · 등록 R §10-5 라).
- 원장 하나 = 경로 하나 (`predict` ↔ `unit:*` · `point:*` 함께 두지 않음) = 규칙 (등록 R §10-5 가 ⑮).
- 운영자 확인 표지의 내용 (그 부팅 · 컨테이너가 끝났음) = 사슬이 검사 못 함 (등록 R §10-5 아 ④).
- 원인 분류의 남은 경계 (1저자 11-02 밤 · PC6-13 열린 질문 셋 = 한정) — 자원 낱말 없는 메모리 실패 꼴 = `runner_rc` · 사슬이 끝 기록 전에 죽은 런 = `parent_dead` (로그에 파이썬 traceback 이 있어도 · traceback 낱말 규칙 없음) · 정리 중 신호 (`signal_after`) = 요약 있는 길 `group_unconfirmed` ↔ 요약 없는 길 `runner_rc` (보수) · CUDA 표지 = 부분 문자열 · 대소문자 그대로 (무해한 언급도 재실행 막음 · `CUDA Error:` 못 잡음).
- PC7-03 고침 범위 — 표의 exception 행만 바꿨다 · timeout · signal · signal_after · rc 0 · rc None 행을 by chain 표에 맞추는 것 = 결정 밖 (커밋 메시지 · 원장 메모).
- Q9 §7 한정 ⑯ · ㉓ · ㉔ · ㉕ — 합치기 사본 = 통째 바이트 복사 (보관 = 그 기계의 캠페인 폴더 · 판정 전 지우지 않음) · 감도 변이의 단위 합치기 시험 = SVORDER 만 · 합치기 = 러너 · 킷이 있는 기계에서만 · 다시 판정 = 입력 폴더 · 원장 절대 경로에 묶임.
- Q9 개정 7 "결과 전 멈춘 재실행 = 건너뜀" = 복사 전 (단계 관문) 에서 멈춘 재실행만 — 끝난 런을 복사한 재실행은 원 시도와 같이 결과 뒤 (사전 공격 6 회차 §5 #12).
- 표지 "덮지 않기" = 확인 뒤 replace · 짧은 창 (시도 폴더 · 런 이름 규칙이 막음 · 기계적 원자 보장 아님 · `REPORT_C.md` §12).

### 8-3. 환경 · 수치

- kgy 판 — 게이트 단계 = uv CPython 3.8.20 (kgy 3.8.10) · numpy · scipy 판은 같다 · 나머지 패키지 = kgy `pip freeze` 기록 없음 · gabia 판 = 기록 없음 (다르면 kgy 판 venv · 1저자 10-24) · kgy 실제 조건 (비 root · ssh · /proc 옵션 · hidepid) = 미확인 (PC6-01 한정과 겹침).
- BLAS 계산 경로 — 같은 코드 · 같은 스레드 수라도 `OPENBLAS_CORETYPE` 만 바뀌면 σ 가 상대 1.3e-10 – 5.8e-10 다르다 (회차 ① 요청서 §8) → float 같음 대조 = 한 프로세스 · 한 동결 환경 안에서만.
- 기계 간 결정성 = 같은 컨테이너 CPU 의 두 인터프리터 판만 (`REPORT_C.md` §6) · AVX-512 ↔ AVX2 (RCA-07 칼날) · GPU · kgy 기계 자체 = 시험 안 함.

## 9. 사전 공격 리뷰 (CLAUDE.md ①–④)

| 회차 | 대상 | 결과 | 처분 |
|---|---|---|---|
| 5 (10-28) | 묶음 C + 10-28 결정 (`0c47df263`) | 새 P1 0 · P2 6 · P3 5 · 변이 23 중 20 생존 | PC5-01–08 · 10 · 11 고침 · PC5-09 wontfix (수정 계획 Q1–Q3) |
| 6 (10-30 중간 · 11-02 마무리) | PC5 고침 (`d6e8d1b44` · 사슬 = `4c69070ad`) | P1 둘 (PC6-01 조건부 · PC6-12 후보) · P2 둘 (PC6-02 · 09) · P3 여섯 + 변이 공백 PC6-11 · 철회 하나 · PC5 새 가드 변이 32/32 다시 잡힘 | PC6-01 · 02 · 09 · 12 · 13 고침 · P3 = 열림 (§8-1) |
| 7 (11-02) | PC6 고침 (`0658c0ac6`) | 새 P1 후보 1 (PC7-01) · P2 2 · P3 4 · 숫자 · 줄 번호 · 커밋 주장 = git · 로그와 맞음 | PC7-01–05 고침 (시험 먼저 · 변이 23/23) · PC7-06 · 07 = 한정 |

- ① 숫자 · 전칭 ↔ 출처 (이 요청서) — 커밋 번호 = 이 작업 트리 `git log` 대조 (§2 표 32 개 = 전부 `9bec6b764` 뒤 · 요청서 전체 64 개 = HEAD 조상 63 + litdb 정본 가지의 `eeb8d13d9` 하나 · HEAD 조상 중 4 개 = 회차 ① 핀 자신과 그 전에 claimed_fixed 된 SELF-129 · SELF-134 · RINT-23 · PC7 번호 = 아직 없음) · §7 숫자 = 카드 원문 줄과 한 줄씩 대조 (`git show eeb8d13d9:litdb/papers/<slug>.md`) · 경로 = `scripts/check_doc_refs.py` 깨진 참조 0 · §5 수 = `pc7_fix/logs/` 와 11-03 반입 확인 출력 · 원장 수 = `scripts/check_review_findings.py` 출력 · 묶음 보고의 수 = 그 보고의 에이전트 출력 (메인 재실행은 각 보고의 메인 메모) · 회차 ① 조건 셋의 "닫힘 주장" = 구현 · 시험 기준 (문서 잔존 다섯 = §3-1 오른쪽 칸).
- ② 바뀐 함수마다 지난 HOLD 부류 (NaN · ±inf · 넘침 · 빈 · 중복 · 꼴 틀림 · 링크 · 다른 판본 · 바꿔 끼우기 · 손 고침 · 부분 복사) — 사전 공격 5–7 회차 탐침 · 변이 (`preattack5/` · `preattack6/` · `preattack7/`) · 고침 변이 (`fix_pc5_20261028/` · `pc6_fix/` · `pc6_13_fix/` · `pc7_fix/`).
- ③ 독립 에이전트 (고친 사람 설명 없이 diff · 보장마다 작은 해석 반례) = 5 · 6 · 7 회차 · 7 회차는 PC6 고침의 닫힘 주장 셋이 실제 범위보다 넓음을 찾았다 (PC6-09 = 같은 `--out` 에서만 · PC6-12 = 꼴 맞는 attempt.json 이 있는 폴더에서만 · PC6-13 자리 전수 = 하나 빠짐) → PC7-01 · 02 · 03.
- ④ 닫는 것 / 닫지 않는 것 = §0.
- 이 요청서 자체를 독립 에이전트로 다시 공격하지는 않았다 (초안) — 발송 전 메인 몫.

## 10. 일정 (1저자 11-03 · 메인 전달)

| 날짜 | 무엇 | 먼저 있어야 하는 것 |
|---|---|---|
| ≤ 11-20 | **Codex GO** (이 회차 · 코드 · 설계 · 문서 범위) | 이 요청서 발송 (1저자) · 리뷰 핀 실행 (§5 ⬜) |
| ≤ 11-21 | **숫자 봉인** — 등록 R §2-1 개정 커밋 하나 (§0 오른쪽 둘째 칸의 숫자 전부 · S0 계획 해시 · R 런 계획 해시 + `--stage plan-doc` 블록 · 1저자 비준 = 등록 R §11 ⑧) | S0 단계 1 (kgy · SBE 기하 · 새 핀) → s_min 개발 단계 → ⑥ 숫자 탐침 (개발 탐침 사전 원장 · σ 비열람) → 기하 + 반복 수 확인 (개발 탐침 원장 §1 순서의 Codex 요청 · 범위 = Q8) — 이 순서가 봉인 전에 끝나야 한다 (1저자 지시 때 시작 · 지금 0 건) |
| 11-22 – 11-29 | **R 런** (kgy · gabia) — S0 단계 2 (DBE) → 사다리 · 예측 (원장 시도 꼴) | 봉인 · gabia 판 확인 (다르면 kgy 판 venv) |
| 11 월 안 | **판정** (주 판정 · 감도는 그 뒤 — 등록 R §10-4 순서 · 해석 = 1저자 확인 전) | — |

- 시간 어림 (추정 · `docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json`) — all3 · 두 대 · 12 단위 나눔 110.1 – 159.4 h · 한 대 220.2 – 318.8 h · 넘침 모서리 하나 = +86.7 – 104.9 h (한 기계) · 합성 침대 반복 비 · 기계 속도 같음 · 감도 · 재시도 · 재실행 밖 · 하한은 낙관적 (Q9 §6) — 11-22 – 11-29 (8 일 = 192 h) 안은 넘침 · 재시도 없는 두 대 나눔 어림일 때만 (추정).

## 11. 판정 요청 질문

| # | 질문 |
|---|---|
| Q1 | §4 의 finding 마다 닫힘 / 부분 / 열림 — RR1-01 · RR1-02 · RCA2-04 (닫는 조건 = RR1-01) · RCA2-02 · 03 · 05 · 07 · X6 · X3 · X5 · PC5-01–08 · 10 · 11 · PC6-01 · 02 · 09 · 12 · 13 · PC7-01–05 · 이어 확인 넷 (SELF-129 · SELF-134 · SELF-137 · RINT-23) (최소 해결 ↔ 고친 자리 · 반례 재실행). |
| Q2 | §3-1 회차 ① 조건 셋 — 구현 · 시험으로 닫혔는가 · 문서 잔존 다섯 (① 넷 = Q9 §0 21 행 · Q9 §7 202 행 · 등록 R §4-1 136 행 · 등록 R §10-4 558 행 / ③ 하나 = Q9 §8 256 · 259 행 짝) 을 봉인 전 문서 묶음으로 미뤄도 되는가 · 아니면 GO 전에 고쳐야 하는가. |
| Q3 | 위조 한정 (등록 R §13-3 B2-Q1) — 이 한정을 둔 채 증서 구간 SV 모서리를 판정 입력으로 받아도 되는가 · 아니면 끝마다 φ 를 남겨 다시 조립한 그래프 위에서 증서를 다시 검사 (끝마다 ≈ 0.2 GB · 추정) 하거나 소비자가 다시 푸는 것 (CG 비용) 이 필요한가. |
| Q4 | recover · 원장 계열 (PC5-03 · 04 · 07 · PC6-01 · 09 · 12 · PC7-01 · 02 · 04) — 원장 시작 기록 + 두 번째 입구 화면만 + recover 바탕 대조가 판정문 ② "확인 못 한 호스트 = 미확인 · 다음 시도 채택 막음" 을 다른 바탕 · 다른 기계 입구에서도 지키는가 · 남은 창 (PC7-07 · 시작 기록 커밋 전 사망 = PC6-09 꼴 화면만) 과 PC7-06 시험 공백을 한정으로 받을 수 있는가. |
| Q5 | 원인 분류 (자원 낱말 다섯 · `NOT_RESOURCE_WORDS` · CUDA 표지 (+ 라이브러리 상태 문자열) · `runner_rc` · `group_unconfirmed` · `chain_exception` · `parent_dead` · `signal_after`) — 재실행 자격을 막는 쪽으로 기운 지금 표가 결과 뒤 선택을 막기에 충분한가 · §8-2 의 남은 경계 (PC6-13 열린 질문 셋 · PC7-03 범위 · PC6-03 · 05 · 06) 중 봉인 전에 막아야 할 것이 있는가. |
| Q6 | 회차 ② 진입 조건의 "작은 실제 producer → 게시 / 판정 → 재판정" (§3-2) — 판정 · 재판정이 가짜 러너 세계 시험뿐인 지금, 봉인 전 실물 작은 사슬 (합성 킷 · 실제 러너 · payload → 사다리 · 예측 → 판정 → 다른 프로세스 다시 판정) 끝-끝 시험이 필요한가 · 필요하면 최소 꼴. |
| Q7 | 빠진 물리 원장 (§6) — v0 범위 동결 · SDCP 접촉 저항 0 가정 + SV 반사실 두 끝 · AM–AM · AM–SE · SE–SE 계면 없음 · MPM 상속 M1–M7 — 이 한정으로 등록 R §7-1 · §7-2 · §8 문장이 서는가 · 빠진 행 (특히 R_j,0 하나가 흡수하는 몫 · VA 우회 · 비주기 측면) 이 있는가 · 6-2 의 공유 정의 중 다음 트랙 (이온 계면 · MPM 수치 갱신) 전에 바꾸면 Rint ② 판정이 흔들리는 것이 있는가 · §7 문헌 근거의 구분 (가져온 것 = Eq. S3 형식 · 실구조 FV 실험 지지 / 가져오지 않는 것 = 열 채널 값 · 전하 채널 R_int · 우리가 더한 AM–AM 면 · 계단 면적 보정 · 접합 법칙) 이 맞는가. |
| Q8 | 숫자 봉인 순서 (S0 단계 1 → s_min → ⑥ → 기하 + 반복 수 확인 → 세 숫자 + 실행 정책 넷 → 봉인 → S0 단계 2 → R) — 일정 (§10) 에 맞추려면 S0 단계 1 · ⑥ 을 이 회차 검토와 나란히 돌려도 되는가 (개발 자료 · 원장 · σ 비열람 규칙 그대로) · 이 회차 판정을 "코드 · 설계 · 문서 GO + 봉인 전 짧은 확인" 꼴로 줄 수 있는가 · 그 짧은 확인의 범위 (S0 기하 · 반복 수 · 숫자 · 계획 해시 · 리뷰 핀 ↔ 봉인 핀 차이 · §3-1 문서 잔존). |
| Q9 | kgy 판 — 게이트 단계 (uv 3.8.20 · 부 판 + numpy · scipy 정확) 가 새 코드 (그룹 · recover · 원장 · /proc 읽기) 에도 충분한가 · 첫 kgy 실행 전에 실제 기계에서 확인할 최소 항목 (사슬 사용자 · /proc 옵션 · hidepid · ssh 세션 · `pip freeze`). |

## 12. 묻지 않는 것

- 등록 R 판정 캠페인 GO · R 런 결과 · 정량 판정 · 생산 GO · 숫자 칸의 값.
- 다음 트랙 설계 (전해질끼리 이온 계면 · `MPMC-01`–`03` 고침 · STEP3 σ₀ 1.5 · AM 상 · 계면 항) — 이 회차는 §6 한정 행의 충분성만.
- 회차 ① 에서 닫힌 RCA2-01 · 06 · 08 · 09 · RCA-06 · SELF-132 · 133 의 다시 판정 (회귀가 깨졌을 때만).
- 등록 R §13 (R3-Q1–Q11) · §13-2 (PF2-Q1) 의 옛 질문 = 10-22 판정문이 답함 · §13-1 (R4-Q1–Q12) = 10-22 판정문에 그 이름으로 나오지 않는다 (답한 자리 미확인 — 남은 것이 있으면 지적만) — 새로 묻는 것 = §13-3 B2-Q1 (Q3) 뿐.
- Rint ② 밖 트랙 (50kg · LHS214 · 믹서 · 웹앱 그림 · 주간보고).
