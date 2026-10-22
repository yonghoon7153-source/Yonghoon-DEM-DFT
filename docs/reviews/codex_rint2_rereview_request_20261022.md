# Codex 재검토 요청 — Rint ② 설계 + 구현 (10-21 HOLD 뒤 · 사전 리뷰 두 회차 반영 · S0 실측 전) (2026-10-22 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 10-21 판정 (`docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md` · 검토 핀 `5dc6f7f0b` · S2 v0 · 수렴 증서 · 등록 R 판정 캠페인 = HOLD) 의 최소 해결을 코드 · 등록에 넣고, 독립 사전 리뷰를 두 번 더 거쳐 고쳤다.  고친 판이 그 반례들을 닫는지, 그리고 "S0 단계 1 실측 → ⑥ 숫자 탐침 → 계획 하나 봉인 → S0 단계 2 → R 런" 으로 들어가도 되는지 (조건부 GO 의 조건) 판정해 달라.
> **리뷰 핀** = 이 요청서가 든 커밋 (`claude/sdcp-dem-manuscript-si-pqwtv8` · push 됨 · 번호 = ZIP 의 `PIN.txt`) · **비교 기준** = `5dc6f7f0b` (10-21 검토 핀).  ZIP 의 리포 파일은 리뷰 핀의 blob 그대로이고, 나머지 소스 · 시험은 원격 핀에서 읽으면 된다 (지난 회차와 같은 방식 · 지난 회차에 빠졌던 요청서 자신도 이번 ZIP 에 넣었다).
> **1저자 결정** — 10-21 Q1–Q13 *"권고대로 해"* · 10-21 사전 리뷰 1 회차 Q-A–Q-G · 10-22 사전 리뷰 2 회차 Q1 (다) · Q2 · Q3 *"권고대로"* (결정 · 쉽게 말하면 상자 = 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` §5 · §6) · 10-21 Q2 (나) = 재압밀이 늦으면 코드 · 문서 먼저 보내고 S0 실측은 보충 회차.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① 10-21 판정의 RCA-01–10 · 12 · 13 (원장 `claimed_fixed`) — 판정문의 최소 해결이 지금 코드 · 등록에서 성립하는가 (finding 마다 닫힘 / 부분 / 열림) | S0 실측 기하 — 재압밀 (kgy · 10-23 예정) 뒤 **보충 회차** (RCA-03 재방문 수 · RCA-05 L_c/L_par · RCA-11 s 분포 · ⑥ 반복 수) |
| ② 단계별 판정 갱신 — S2 v0 (HOLD) · 수렴 증서 (HOLD · 일반 인증 주장) · 등록 R 판정 캠페인 (HOLD) · S1 · S3 (조건부 GO) — 위 실행 순서로 들어가도 되는가 · 조건 | RCA-11 (원장 open — S0 자료 뒤) |
| ③ 사전 리뷰 2 회차 (10-22 · 독립 · 기반 `93d93bc02`) 결함 PRE2-impl-01–04 · PRE2-design-01–10 의 고침 (PF2) 이 같은 부류를 닫는가 — 특히 Q1 (다) SV 반사실 괄호 판정 · Q2 계획 해시 정확 대조 · 같은 판 (코드 지문 · dirty) 대조 | 결과 전 등록 숫자 셋 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) = 이 회신 뒤 · S0 단계 2 (DBE) 열람 전에 1저자 (Q-G) |
| | 런 결과 · 정량 판정 · 생산 GO · ①′ 정량 채택 (모두 0 건) |
| | `RIMPR-04` 전체 (open · ①′ 정량 채택 전) · `RINT2-B01` (Windows 시험 작성기 · open) |
| | 1저자 미결 30 자리 (지금 방식 유지 · `docs/reviews/rint2_pf2_fix_evidence_20261022/stage2_report.md` §6) — 결함이면 지적해 달라 · 선택이면 의견만 |
| | 사전 공격 리뷰 (단계 ③) 가 찾은 F1–F8 · O1 — 이 회차에는 고치지 않고 §8 에 한정으로 올렸다 (1저자 결정 전) |

## 1. 보내는 것 (ZIP · 리뷰 핀 blob 그대로 + `PIN.txt`)

| 묶음 | 파일 |
|---|---|
| 이 요청서 · 단계 ② 보고 · 사전 공격 리뷰 | `docs/reviews/codex_rint2_rereview_request_20261022.md` · `docs/reviews/rint2_pf2_fix_evidence_20261022/` (단계 ② 보고 `stage2_report.md` · 사전 공격 리뷰 `stage3_prereview/` = 판정 + 탐침) |
| 대상 문서 | 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (4 판 + PF2 개정) · 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · kgy 명령 `docs/reviews/rint2_kgy_commands_20261020.md` · 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` |
| 지난 판정 · 사전 리뷰 | `docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md` · 사전 리뷰 1 회차 `docs/reviews/rint2_prereview_20261021/` · 2 회차 `docs/reviews/rint2_prereview2_20261022/` (탐침 포함) |
| 원장 | `docs/reviews/findings.json` (RCA-01–13 · RINT2-B01 · RIMPR-04 · RINT-23) |
| 코드 (읽기 · 실행) | `scripts/carbon_junction.py` · `scripts/ca_ext_svcf.py` · `scripts/rint_r_chain.py` · `scripts/ca_s0_census.py` · `scripts/step3_sigma.py` · `scripts/step3_conv_cert.py` · `scripts/mpm_webapp_payload.py` · `scripts/run_contract.py` · `scripts/ptfe_face_alpha.py` · `webapp/templates/mpm_lab.html` · `webapp/static/explain/rint_overview_20261021.html` |
| 시험 | §5 표의 16 파일 |

## 2. 무엇이 바뀌었나 (`5dc6f7f0b` 뒤 · 세 회차)

| 회차 | 커밋 범위 | 무엇 |
|---|---|---|
| 10-21 최소 해결 (Q1–Q13) | `5dc6f7f0b..a76f59d0d` (이 범위에는 다른 트랙 커밋도 섞여 있다 · Rint 쪽 파일만 보면 된다) | S2 접합 = 가지 식별 · 포트 불변 · 긴 접촉 법칙 적용 범위 (RCA-03–05) · SV 반사실 가드 (RCA-06) · 목표량 증서 ⓓ (RCA-07) · 등록 R 3 판 (RCA-01 · 02 · 08–13) |
| 사전 리뷰 1 회차 고침 (Q-A–Q-G) | `a76f59d0d..93d93bc02` | 같은 섬유 조각 접촉 = 다른 섬유와 같은 규칙 · 모든 접촉 = 중심선 거리 · 덮인 접점 포트 옮김 금지 · SV 반사실 = 다른 섬유 사이 우회만 · origin 합집합 · 실행 순서 · 세 숫자 시점 · 등록 R 4 판 |
| 사전 리뷰 2 회차 고침 (PF2 · 단계 ②) | `93d93bc02..` 리뷰 핀 | A = Q1 (다) SV 괄호 · B = 계획 해시 정확 대조 + §11 순서 · C = §10-4 시간 · D = 코드 지문 + dirty · S0 census · registry 지문 · E = SV 기록 수 재대조 · 넘침 · 중복 칸 · 등급 칼날 · F = 문서 · 웹앱 · G = 원장 · H = 회귀 (`stage2_report.md`) |

## 3. 10-21 finding → 고친 자리 · 시험

| finding | 원장 | 고친 자리 (요지) | 시험 (지금 판 · §5) |
|---|---|---|---|
| RCA-01 (P1) 할선 기울기 ↔ 역상 폭 | claimed_fixed `3b3aa50e2` | 등록 §3-2 · §3-2b (보호 띠 · 끝 쪽 연장 간격 ≤ ×100 · PF2-Q1) | `test_rint_r_chain.py` U01 · U01e · U12 · L03 · L11 · M11 |
| RCA-02 (P1) 양끝 origin | claimed_fixed `3b3aa50e2` | 등록 §4-2 (양끝 8 팔 · origin 합집합 Q-E) | U02 · P05 · U13 · M15 · M32 · M33 |
| RCA-03 (P1) `(cell, fid)` 재방문 | claimed_fixed `3b3aa50e2` | 접합 가지 식별 (같은 셀 다른 가지 = 합치지 않음) · Q-A | `test_carbon_junction.py` RCA03 · GAP · RING · SELFD · KINK · CEN |
| RCA-04 (P1) 포트 동률 · 경로 반전 | claimed_fixed `3b3aa50e2` | 경로 반전 · 공선 세분 · fid 재명명 불변 포트 · 덮인 접점 안 옮김 (Q-C) | RCA04 · T1-11 · QC · `test_ca_ext_runner.py` N6 · N6b |
| RCA-05 (P1) 긴 접촉 집중 | claimed_fixed `3b3aa50e2` | 적용 범위 · 한정어 ⑫ · 분산판 = v1 | RCA05 · KBND |
| RCA-06 (P1) `SV_DOMINANT` 소산 가드 | claimed_fixed `eb571a458` | 반사실 비 (G 전체 / G 끊음) · 1 회차 = 다른 섬유 사이 우회만 끊음 (Q-D) · 2 회차 = 못 가른 덩어리 괄호 [아래, 위] (Q1 (다)) | RCA06 · QD · QD2 ①–⑪ · `test_rint_r_chain.py` V05 · V06 · U08 · U08b · V25–V27 · `test_ca_ext_b6.py` S8j–S8p · SP14–SP16 · `webapp/test_ca_ext_labels.py` W15 |
| RCA-07 (P2) 수렴 증서 일반 인증 | claimed_fixed `3b3aa50e2` | 경로 무관 목표량 증서 ⓓ · ⓑ 봉인 = OpenBLAS 경로 · 스레드별 경험값 (수정 계획 §5 Q3 결과) | `test_step3_target_cert.py` T1 · T3 · T4 · T21 · `test_step3_conv_cert.py` |
| RCA-08 (P2) P 법칙 빈틈 | claimed_fixed `3b3aa50e2` | `GAP_ENVELOPE_ONLY` | U03 · M16 · U07 |
| RCA-09 (P2) 감도 ↔ 주 판정 추정량 | claimed_fixed `f60bd56ed` | 감도 = 주 판정과 같은 판정 함수 · 감도 단계 = 주 판정 뒤 (`--after-main`) | U04 · U04b · V14 · U14 · V18 · V21–V24 · M17 · M35–M40 |
| RCA-10 (P2) DIA_UNCHECKED ↔ PASS 금지 | claimed_fixed `3b3aa50e2` | 차단 표지 = 닫힌 집합 (§5-6a) · `ASSUMED_UNVALIDATED` | U05 · U07 · V02 · V03 · M18 · M34 |
| RCA-11 (P2) S0 표본화 · s_min | **open** | S0 실측 뒤 (보충 회차) | — |
| RCA-12 (P2) 국소 탄성 ↔ Rc 부호 | claimed_fixed `9fa4fb18b` | 등록 §6 (문서 · 시험 없음) | — |
| RCA-13 (P2) 판정표 단위 · 영 | claimed_fixed `3b3aa50e2` | τ_mono = ln 차 · `VALID_ZERO_TOPOLOGY` · `ELECTRODE_SHORT` (§5-0) | U06 · Z01–Z05 · Z07 · `test_rint_r_chain_e2e.py` E9 · b6 SP9–SP13 · target_cert T3 |

## 4. 사전 리뷰 2 회차 (10-22) → PF2 고침

| finding | 등급 | 고침 (묶음 · 대표 커밋) |
|---|---|---|
| PRE2-impl-01 SV 반사실이 섬유 둘 이상이 함께 지나는 SDCP 덩어리 다리를 끊지 않음 (비 1.0 · 표지 없음 · 참 ∞) | P1 | A — 못 가른 덩어리가 있으면 덩어리 SDCP 셀 간선 · 판 결합을 뺀 판을 한 번 더 풀어 위 끝 · 아래 > 문턱 = `SV_DEPENDENT` · 위 ≤ 문턱 = 표지 없음 · 걸침 · 못 읽음 = `SV_UNCHECKED` (`eb571a458`) |
| PRE2-impl-02 `sv_cf_problem` 이 기록 안 수를 다시 대조하지 않음 | P3 | E — 비 = G_full/G_cut (상대 1e-12) · 비 ≥ (1−τ)/(1+τ) (τ = 1e-4 · 증서 폭 꼴) · 증서 ok · computed ↔ G 유한 양수 · 괄호 아래 ≤ 위 (`0d0f26812` · `368c49ce6`) |
| PRE2-impl-03 계획 읽기 넘침 · 중복 칸 | P3 | E — 10**400 = 구조화 멈춤 · 중복 칸 거부 (사슬 · S0) (`0d0f26812`) |
| PRE2-impl-04 SV 시험이 못 가른 덩어리 꼴을 안 봄 | P3 | A — QD2 ①–⑪ · 변이 J1 · J2 상주 (`8ca09822d` · `0ae9f9846`) |
| PRE2-design-01 계획 재등록 · 사슬 미대조 | P2 | B — ⑥ 숫자 탐침을 S0 단계 2 앞으로 · 계획 하나 봉인 · 사다리 · 예측 · 판정이 S0 단계 2 보고의 봉인 해시와 정확 대조 (새 멈춤 `S0_REPORT_MISMATCH`) (`10719d2b7` · `309098b31` · `3cfbba1c9`) |
| PRE2-design-02 같은 HEAD dirty 미검출 | P2 | D — 단계 요약에 git HEAD · dirty · 코드 파일 12 sha256 · 러너 sha256 · 다음 단계 · 판정 계산기가 대조 (`fca3a0519`) |
| PRE2-design-03 시간 어림 | P2 | C — §10-4 다시 어림 = 주 판정 ① ≈ 191–231 h (추정 · 합성 침대 반복 비) · 결과 전 문장 셋 (결정점 · 10-31 판정 없음 · 팔 안 줄임 · 기계 이름표) (`dd1907b9e`) |
| PRE2-design-04 낡은 "지금" 서술 | P3 | F — 판정문 표의 행 16 + 같은 사실 7 (`d0a5672fb`) |
| PRE2-design-05 kgy 명령 인자 | P3 | F — `--r-plan-path` · `--s0-plan` · `--after-main` · 시험 K01 (`27d0f17bb` · `7f358a55f`) |
| PRE2-design-06 등급 0.454 · 0.908 | P3 | E · F — 정확값 G0/2 · G0 칼날 시험 · 표시 반올림 문장 (`a4e1d1ac8`) |
| PRE2-design-07 §11 ④ 끊는 범위 · 묶기 | P3 | F — 끊는 범위 = Q-D 로 닫힘 · 모서리 묶기 = ㉟ (`a5a6871df`) |
| PRE2-design-08 R 런 census · registry 판 | P3 | D — R 런이 S0 단계 1 · 2 보고의 일곱 파일 지문과 대조 · DBE 열린 뒤 s_min 다시 고르기 금지 문장 (`fca3a0519`) |
| PRE2-design-09 웹앱 "10-25 목표" | P3 | F — 등록 §10-4 와 같게 · 상자 ① ② ③ (`b9de44d14`) |
| PRE2-design-10 §3-2b ③ 상계 문장 | P3 | F — 끝 쪽 연장 간격 (≤ ×100) · 다시 좁힐지 = PF2-Q1 (`9082a6fe0`) |

## 5. 실행 (리뷰 핀과 같은 코드 `5e95047fc` 에서 우리 실행 · Linux · Python 3.11.17 · NumPy 2.4.6 · SciPy 1.17.1 · `python3 -I <파일>`)

| 시험 파일 | 결과 |
|---|---|
| `scripts/test_rint_r_chain.py` | 218/218 |
| `scripts/test_rint_r_chain_e2e.py` (실제 러너) | 16 PASS · 0 FAIL |
| `scripts/test_ca_ext_b6.py` | 357 PASS |
| `scripts/test_carbon_junction.py` | 327/327 |
| `scripts/test_ca_s0_census.py` | 152 PASS |
| `scripts/test_ca_ext_runner.py` · `test_ca_ext_z1.py` · `test_ca_ext_z3.py` · `test_ca_ext_verdict.py` | 128 · 95 · 84 · 31 PASS |
| `scripts/test_step3_target_cert.py` (빠른 판) · `--long` | 252/252 · 296/296 (`--long` = PF2 F–H 에이전트 실행 · 한 검사 T17c3 = 이 기계에서 `OPENBLAS_CORETYPE` 가 실제 계산 경로를 안 바꿔 생략 · 원장 RCA-07 의 297 은 그 검사가 도는 환경) |
| `scripts/test_step3_conv_cert.py` · `test_ptfe_face_alpha.py` · `test_rint_receipts.py` | 27/27 · 242 · 102 PASS |
| `webapp/test_ca_ext_labels.py` · `test_rint_explainer_page.py` · `test_mpm_lab_cmp_absent_phase.py` | 68 · 55/55 · 23/23 |
| 전체 게이트 `scripts/check_all.sh` (묶음마다) | "✓ 전부 통과" (156 ✓ · 0 ✗) |

- 끈 경로 (`bf79d44c2` ↔ 단계 ② 끝 · payload 끝-끝 11 경우): σ 비트 같음 · 의도된 차이 = 접합 켬 때 `qualifiers` 한 칸 (한정어 10 번째 문장) + SV 노브 켬 때 괄호 새 칸 5.  "차이 0" 이 아니다 (`stage2_report.md` §3).
- 변이: A 19/19 · B–E 63/63 · F–G 23/32 (생존 9 = 기계 검사가 없는 산문 · 메모).

## 6. 사전 공격 리뷰 (CLAUDE.md ①–④)

| 단계 | 결과 |
|---|---|
| ① 숫자 · 전칭 ↔ 출처 | §5 의 시험 수 = 위 환경에서 리뷰 핀 코드로 다시 돌린 출력 · 커밋 범위 수 = `git rev-list --count` · RCA 원장 상태 = `findings.json` |
| ② 바뀐 함수에 지난 HOLD 부류 | 묶음마다 (NaN · ±inf · 넘침 · 빈 · 중복 · bool · 옛 칸만 있는 기록 · 다른 판본 계획 · 보고) — `stage2_report.md` · 시험 S8j–S8p · V25–V27 · M41 · B01 · D01 |
| ③ 독립 에이전트 (고친 사람 설명 없이 · 보장마다 작은 해석 반례 · 판정문 탐침 재실행) | 단계 ③ (10-22 11:37–12:15 UTC · 독립 에이전트 · 대상 `5e95047fc` · 기반 `93d93bc02` 대비 scripts · webapp 14 파일 · 고친 사람 설명 안 읽음) = 새 P1 0 · P2 1 · P3 7 · 관찰 1 — 지난 반례 (PRE2-impl-01 · 02 · 03 · PRE2-design-01 · 02 · 06 · 08) 는 이 트리에서 전부 거부 · 표지 · design 탐침 A · B · D = 지난 JSON 과 키별 차이 0 · 손 회로 괄호 S1 · S4 · S5 성립 · 변이 25 중 23 잡힘 (생존 R5 = F2 · C3 = 방어 갈래) + 더한 변이 C5 생존 (F4) · 찾은 것은 이 회차에 고치지 않고 §8 에 한정으로 올렸다 (1저자 결정 전 · 오늘 발송) · 전문 + 탐침 = `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/` |
| ④ 닫는 것 / 닫지 않는 것 | §0 |

## 7. 판정 요청 질문

| # | 질문 |
|---|---|
| C1 | §3 의 RCA 마다 닫힘 / 부분 / 열림 (최소 해결 ↔ 고친 자리 · 반례 재실행). |
| C2 | 단계별 판정 갱신 (S2 v0 · 수렴 증서 · 등록 R 판정 캠페인 · S1 · S3) — "S0 단계 1 → ⑥ → 계획 봉인 → S0 단계 2 → R 런" 진입 조건. |
| C3 | Q1 (다) 괄호 판정의 보장은 "지금 셀 그래프 안에서" 뿐이다 (등록 ㊱) — 판정 가드로 충분한가 · 섬유 길을 따로 그리는 (나) 역할 분리 표현이 필요한가.  모서리 묶기 = "하나라도" (㉟ · 두 표지 동시 가능 · 미결 1). |
| C4 | 계획 하나 봉인 + 해시 정확 대조 + 코드 지문 12 · dirty 대조가 "같은 판" 보장으로 충분한가 — 지문에서 뺀 파일은 HEAD + dirty 로만 막힌다 (미결 12 · 13 · 14). |
| C5 | §10-4 시간 문장 (결정점 · 10-31 판정 없음 · 팔 안 줄임 · 기계 이름표) 이 결과 뒤 선택을 막는가. |
| C6 | 미결 30 중 결함으로 보는 것 (특히 1 · 2 · 12 · 17). |
| C7 | 사전 공격 리뷰 F1 (git 밖 = 코드 핀 통과) 의 최소 해결 "HEAD 또는 dirty 가 None 이면 멈춤" 에 동의하는가 · F8 — S0 보고의 침대 ↔ R 런 팔을 묶는 "같은 침대" 대조가 필요한가 · F3 · F4 · F6 이 결함인가 한정인가. |
| C8 | 지난 회차에서 넘어온 질문 — 등록 R §13 R3-Q1–Q11 · §13-2 PF2-Q1 (끝을 늘린 뒤 다시 좁힐지) · origin 세 개로 충분한가 · DBE 의 R 단조 검사가 없는 것 · 멈춘 단계를 다시 돌리는 규칙. |

## 8. 알려진 한정

- S0 실측 · ⑥ 반복 수가 없다 → 시간 어림 (191–231 h) · RCA-03 · 05 · 11 의 실침대 크기는 보충 회차에서.
- 수렴 증서의 ⓑ 봉인 구간은 OpenBLAS 계산 경로 · 스레드에 따라 다르다 (RCA-07 · 수정 계획 §5 Q3 결과) — 판정은 경로 무관 목표량 증서 ⓓ 로 한다.
- **F1 (P2)** git 밖 실행이면 코드 핀이 걸리지 않는다 — `git_identity` 가 HEAD · dirty = None 을 내면 `code_dirty_problem` · `code_verdict_problem` 이 통과한다 (등록 ㊳ "git 밖 = 기록만").  그러면 지문 목록 12 밖 모듈 (`ca_ext_cjunc.py` 등) 의 변경이 단계 사이에 안 보인다.  운영 = kgy git 작업 트리라 발생 공산은 낮다 (추정).  최소 해결 후보 = HEAD 또는 dirty 가 None 이면 멈춤 (또는 지문 = 실제 import 집합) · 1저자 결정 전 (미결 13 과 같은 자리) → C7.
- **F2 (P3)** 한 단계 안에서 사슬 HEAD ↔ 러너 HEAD · `files` ↔ `runner_files` 를 대조하지 않는다 (변이 R5 생존).
- **F3 (P3)** SV 기록 검증기가 받는 꼴 다섯 — 위 끝 제거 수 ↔ 기록 덩어리 수 미대조 · computed 끝의 증서 없음 · 투영이 증서 구간을 버려 증서 ↔ G_cut 결합 불가 · `bracket_rule` 아무 낱말 · 덩어리 수 10**400.  생산자 정상 경로는 맞게 쓴다 (옮김 · 다른 판본 기록만 해당).
- **F4 (P3 · 시험 틈)** 덩어리가 둘 이상인 회로 시험이 없다 — 위 끝이 첫 덩어리만 빼는 변이가 시험을 지나가고, 같은 변이로 합성 침대 9 중 3 이 `SV_UNCHECKED` → 표지 없음이 된다 (지금 코드는 전부 뺀다).
- **F5 (P3)** `s0_stage2_problem` 이 `plan_source` 의 접두어 "commit:" 만 본다 (R 계획 sha ↔ 등록 줄 대조는 따로 있다).
- **F6 (P3)** census 불일치 갈래 — 생산자가 자기 검증기가 거부하는 기록을 내고 payload 가 게시를 거부한다 (fail-closed) · 시험 QD2 ⑧ 문구 ("사슬 = SV_UNCHECKED") 는 `sv_assess` 단독 결과 · `unsplit_census_mismatch` 가 `KNOWN_STATUSES` 에 없다.
- **F7 (P3)** 웹앱 SV 줄 Jinja ↔ JS 표기 차 (1.0 ↔ 1 · 지수 표기) — 뜻 같음.
- **F8 (P3 · 질문)** S0 보고의 침대 입력 ↔ R 런 팔 (sid · 입력 지문) 이 묶여 있지 않고 등록에 "같은 침대" 문장이 없다 → C7.
- **O1 (관찰)** 괄호 정보량 — 덩어리가 있으면 위 끝 = SDCP 구를 통째로 빼 섬유도 끊기므로 위 끝이 1e4 까지 간다 · 참 비 1 인 대칭 꼴도 [1, ∞].  합성 침대 9 (vox 0.15 · Ø1 µm SDCP · 합성 · 실침대 빈도 아님) 에서 못 가른 덩어리 9/9 · 문턱 2 가정 시 걸침 5 · 표지 없음 3 · 의존 1 → 실침대에서 PASS 문장이 대부분 `SV_UNCHECKED` 로 막힐 수 있다 (추정) → C3.
