> 메인 반입 (10-26 · Claude): 에이전트 가지 `rr-fix-b` 의 11 커밋을 메인 `3056eef12` 위에 cherry-pick (`-x` · 메시지에 원 SHA) — 아래 SHA 는 전부 **메인 SHA 로 바꿔 적었다** (B1 `198f3a35c` · B2 `5497760cf` · B2x `39104710a` · B4 `7dc8dc647` · B3′ `9506a54dc` · B5 `6602b660c` · B6 `e4714241b` · B7 `74f84105c` · B1 후속 `8661d1d83` · B6 보강 `f9fc67c76` · B6 한정 꼴 `f38aec706`).  충돌 = `docs/reviews/findings.json` 하나 (B5) — 3-way (RCA2-02 · 03 = 에이전트 판 · RCA2-04 = 메인 판 + 에이전트 덧붙임).  본문의 "끝 `f38aec706`" · "시작 `20651fd36`" 의 시험 수는 에이전트 가지에서 잰 값이다 (메인 위 재확인 = 전체 게이트).

# 묶음 B 보고 — 같은 코드 · 같은 침대 · X6 · X3 · X5 · 결정 11 · 상자 ⑤ · RR1-01 · RR1-02 (Rint ② RR · 10-25 ~ 10-26)

> 원문 = 작업 트리 에이전트의 마지막 보고입니다.  지시서 = `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` §보고 · `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF_B.md`.  B6 · B7 = 회차 ① 수정 계획 `docs/reviews/rint2_rr1_fix_plan_20261026.md` Q1–Q3 (가).
> 숫자와 전칭은 에이전트 실행 출력입니다 (범위와 시험 판을 같이 적었습니다).

묶음 B 를 마쳤습니다.  끝 트리 회귀는 Python 3.11 에서 전부 rc 0 이고, kgy 판 (3.8.20) 11 묶음도 통과합니다.

끝 검증에서 내 결함 두 가지를 찾아 고쳤습니다.
- B1 시험 Y08 이 호스트에 따라 결과가 달랐습니다.  시험 쪽 결함이고, 사슬 동작은 옳았습니다.
- B6 시험에 빈자리 다섯이 있었습니다 (변이 생존).

| 항목 | 내용 |
|---|---|
| 가지 · 커밋 | `rr-fix-b` · 시작 `20651fd36` · 끝 `f38aec706` · 커밋 11 |
| 하지 않은 것 | push · fetch · `scripts/check_all.sh` · GPU · 킷 풀이 (SBE · DBE) |
| 봉인 32 파일 | `scripts/run_network_194_parallel.py` 의 CODE_FILES (AST 로 읽음) ∩ 바뀐 파일 22 = 0 |
| ⚠ 합칠 때 | 메인 `dc0a97212` (회차 ① 반입) 는 이 가지의 조상이 아닙니다.  fast-forward 불가 · `docs/reviews/findings.json` 이 양쪽에서 바뀌어 손 병합이 필요합니다 |
| 웹앱 | B6 의 SV 줄만 바꿨습니다.  나머지 항목은 웹앱에 해당 화면이 없습니다 (§9) |

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (claimed · 확인 = Codex) | 닫지 않는 것 |
|---|---|
| RCA2-02 같은 코드 (F1 · F2 · F5) — B1 | RR1-01 의 **생산 원천** (D1).  지금 사슬에는 원천이 없어 증서 구간 SV 모서리가 전부 `SV_UNCHECKED` (등록 R §5-6a 차단) |
| RCA2-03 같은 침대 (F8) — B2 | 증서 지문 칸까지 다시 조립한 값으로 고친 위조 (D2).  지문은 그래프 정체성이지 증서 수의 재증명이 아닙니다 |
| X6 — B2x · **X6 = census 외부 결합 · RR1-01 은 닫지 않음** | 묶음 C (재시도 봉인 · 실행 정책 칸 · Q9 구현 · RCA2-05 · 07) |
| X3 · X5 — B4 | 등록 R HOLD (그대로) · R 에 쓰는 S0 보고 재생성 (끝 핀 · 메인) |
| 결정 11 · 상자 ⑤ · 등록 R 자리 — B3′ | 다른 진단 합의 넘침 (B7 은 이 합 하나만) |
| RR1-01 끝 증서 ↔ 실제로 푼 가중 그래프 — B6 (+ 보강 · 한정 꼴).  생산자 지문 · 소비자 대조 · 원천 없음 = fail-closed | 회차 ② 조건 (B/C 통합 · 작은 실제 생산자 → 게시 · 판정 → 재판정 · 최종 핀 S0 · 환경 · 비용 자료) |
| RR1-02 KCL 진단 합 넘침 — B7 | |

## 1. 커밋

메시지 = `author 10-23 ratified Q2-Q3 Q20-Q21 (bundle B 10-25)` + 끝 두 줄.  B6 부터는 `author 10-26 Q1-Q3 (가)` 를 더했습니다.

| 항목 | 커밋 | 무엇 |
|---|---|---|
| B1 | `198f3a35c` | RCA2-02 + F5 — ① git 신원 엄격: rev-parse · status 종료코드를 보고, HEAD 40-hex · dirty 엄격 False 만 통과.  조회 실패 · git 밖 = 멈춤 · ignore 밖 untracked = dirty (가-1).  ② 한 단계 안 사슬 ↔ 러너 대조 (HEAD · 폴더 코드 지문 · 러너 파일).  ③ 코드 키 = 저장소 상대 경로 · CODE_FILES 12 → 18.  ④ 환경 지문 단위 = python 부 판 · numpy · scipy (나머지는 기록만).  ⑤ F5 = `commit:<40 hex>` + 그 커밋의 R 계획 blob sha256 |
| B2 | `5497760cf` | RCA2-03 — S0 schema v3 (`inputs.settings_sha256` · `raster.sid_off_fp`).  사슬이 inputs · raster 를 보존합니다.  R 런 직전 (사다리 = SBE · 예측 = SBE + DBE) 과 판정 · 다시 판정 (`--root` 필수) 에서 킷을 다시 해시합니다 (S0 와 같은 발견 함수 · 경로는 대조 밖).  arm 0 sid 지문 ↔ S0 off 격자 지문 (같은 규약만).  다르면 `S0_REPORT_MISMATCH` |
| B2x | `39104710a` | X6 — S0 schema v4 단계 2 에 봉인 `sv_census` 를 넣습니다.  R arm 0 과 같은 함수 (`cjunc_registry` → `_sv_split`) · 같은 off 격자 · `ca_ext_cjunc.registry_thresholds` · 봉인 R 계획의 s_min · tol_ff.  사슬이 같은 규약 DBE arm 0 SV 기록의 census 사본 · 증거 census 를 봉인 census 와 대조합니다 |
| B4 | `7dc8dc647` | X3 — 생산자가 위 끝에 새 칸 `n_reach_pairs_cut_vs_lower` 를 냅니다.  검증기 ⑨ = 위 ≠ 아래 위상 ⇔ 그 수 + 판 결합 > 0 · 꼴 · 아래 k + 그 수 ≤ 위 k.  X5 — 수 칸 꼴 · ⑦ · ⑧ 을 비를 싣는 끝이 있는 기록 전부에 적용 (computed 없음 · +∞ 포함 · 위 끝 상태 무관) |
| B3′ | `9506a54dc` | 결정 11 (b6 B · z3 O 에 SV 켬 꼴 셋 · 허용 행 세대 RR · 시험만).  상자 ⑤ (설명 페이지 · 등록 R §2-1b).  등록 R: 머리 줄 · §2-1 · §11 ④ (재압밀 = 새 S0) · §5-6 SV 행 · §10 멈춤 뜻 넓힘 (새 이름 없음) |
| B5 | `6602b660c` | 원장 · 변이 생존 넷에 시험 (Y11 · Y12 · Q07 · S8h⁗) |
| B6 | `e4714241b` | RR1-01 — 생산자 `carbon_junction.solved_graph_fp` (규칙 `solved_graph_dof_ids_pair_exact_sum_plates_v1` · sha256) 를 주 해 · 끝마다 증서 칸 `fp_cjunc_graph` 에 싣습니다.  조립만 = `step3_sigma.solve_sigma_z(cjunc_graph_only=True)`.  소비자 = `ca_ext_svcf.graph_problem` · `run_contract.ca_ext_record_ok(graphs=)`.  사슬 = `SV_GRAPH_SOURCE` (생산 = None → 미확인).  판정 = `sv_assess(require_graph=True)`.  웹앱 SV 줄 표지 · 등록 R |
| B7 | `74f84105c` | RR1-02 — `step3_conv_cert.target_bracket` 의 KCL 결손 진단 합 (`target_kcl_raw`) 이 넘치면 장부 문제 (certify `NOT_CERTIFIABLE` · RuntimeWarning 없음) |
| B1 후속 | `8661d1d83` | kgy 판에서 잡힌 Y08 호스트 의존 고침 (§4).  `env_record` 의 import 이름을 갈라 둠 (규율 경고 18 → 17 · 값은 같음) |
| B6 보강 | `f9fc67c76` | 변이 생존 다섯에 시험 (QG ⑥′ · ⑧ · ⑨ · ⑩ · 사슬 RG07 · 시험만) |
| B6 한정 꼴 | `f38aec706` | 남은 한정 꼴 여섯 + 봉인 원천 = 전부 거부 (QG ⑪ · 시험만) |

## 2. 시험 수 — 고치기 전 → 뒤

고치기 전 = 그 항목 직전 코드에 새 시험을 얹어 돌린 값입니다.

| 항목 | 묶음 | 고치기 전 | 뒤 |
|---|---|---|---|
| B1 | `scripts/test_rint_r_chain.py` | 237/250 (D10 · D12 · D14 · Y01–Y10) | 250/250 |
| B1 | `scripts/test_rint_r_chain_e2e.py` | 16/17 (E1c) | 17/17 |
| B2 | test_rint_r_chain | 249/260 | 260/260 |
| B2 | `scripts/test_ca_s0_census.py` | 152 PASS / 4 FAIL | 159/159 |
| B2 | test_rint_r_chain_e2e | 17/18 (E1d) | 18/18 |
| B2x | test_rint_r_chain | 260 + 새 시험 (Q01–Q05 실패 · Q06 통과) | 266/266 |
| B2x | test_ca_s0_census | 158 PASS / 2 FAIL | 163/163 |
| B2x | `scripts/test_carbon_junction.py` | 441 | 443/443 (QX6) |
| B2x | `scripts/test_ca_ext_b6.py --only Q` | 0/1 | 4/4 (전체 458/458) |
| B2x | test_rint_r_chain_e2e | 18 | 20/20 |
| B4 | test_carbon_junction `--only QD7,QX35` | 30/46 | 전체 448/448 |
| B4 | test_ca_ext_b6 `--only S` | 271 PASS / 14 FAIL | 전체 473/473 |
| B3′ | b6 `--old-scripts --only B` (`9bec6b764` · `49a1af626`) | 37/39 · 35/39 | 39/39 · 39/39 |
| B3′ | `scripts/test_ca_ext_z3.py --old-scripts --only O` (같은 두 기반) | 14/15 · 12/15 | 15/15 · 15/15 |
| B3′ | b6 B0u | 26 PASS / 1 FAIL | 27/27 |
| B3′ | `webapp/test_rint_explainer_page.py` | 61/71 | 71/71 |
| B5 | test_rint_r_chain (Y11 · Y12 · Q07) | 266 | 269/269 |
| B5 | test_ca_ext_b6 (S8h⁗) | 479 | 482/482 |
| B6 | test_carbon_junction QG | 1/2 | 13/13 (전체 448 → 461) |
| B6 | test_rint_r_chain RG01–RG06 | 1/6 | 6/6 (전체 269 → 275) |
| B6 | test_ca_ext_b6 `--only S` | 289/296 | 296/296 (전체 482 → 490) |
| B6 | `webapp/test_ca_ext_labels.py` | 88/92 | 92/92 |
| B7 | `scripts/test_step3_target_cert.py` T25 | 0/4 | 4/4 (빠른 판 260 → 264 · T24b 정상 회로 20 = `49a1af626` 증서와 비트 같음) |
| B1 후속 | kgy 판 test_rint_r_chain (3.8.20) | 274/275 (Y08) | 275/275 |
| B1 후속 | `scripts/check_method_discipline.py` | 0 오류 · 경고 18 | 0 오류 · 경고 17 |
| B6 보강 | test_carbon_junction · test_rint_r_chain | 461 · 275 | 465/465 · 276/276 |
| B6 한정 꼴 | test_carbon_junction | 465 | 466/466 (3.11 · 3.8.20) |

## 3. 회귀 — 묶음 시작 `20651fd36` → 끝 `f38aec706`

Python 3.11 · BLAS 1 · nice 19 · 전부 rc 0.

| 묶음 | 시작 | 끝 |
|---|---|---|
| `scripts/test_rint_r_chain.py` | 240/240 | 276/276 |
| `scripts/test_rint_r_chain_e2e.py` (실제 러너 · payload) | 16/16 | 20/20 |
| `scripts/test_ca_s0_census.py` | 152/152 | 163/163 |
| `scripts/test_carbon_junction.py` | 441/441 | 466/466 |
| `scripts/test_ca_ext_b6.py` | 454/454 | 490/490 |
| `scripts/test_ca_ext_runner.py` | 128/128 | 128/128 |
| `scripts/test_ca_ext_verdict.py` | 31/31 | 31/31 |
| `scripts/test_ca_ext_z1.py` · `scripts/test_ca_ext_z3.py` | 95 · 84 | 95 · 84 |
| `scripts/test_ptfe_face_alpha.py` | 242/242 | 242/242 |
| `scripts/test_step3_target_cert.py` 빠른 판 | 260/260 | 264/264 |
| `scripts/test_step3_conv_cert.py` | 30/30 | 30/30 |
| `scripts/run_contract.py --selftest` | 124/124 | 124/124 |
| `scripts/step3_sigma.py --selftest-rint` · `--selftest` | PASS · (시작 미측정) | PASS · PASS |
| `webapp/test_ca_ext_labels.py` | 84/84 | 92/92 |
| `webapp/test_rint_explainer_page.py` | 62/62 | 71/71 |
| `webapp/test_rint_scope_labels.py` | 31/31 | 31/31 |
| `scripts/check_method_discipline.py` | 0 오류 · 경고 17 (git blame — 끝 판 경고 18 중 17 줄이 묶음 B 전) | 0 오류 · 경고 17 |
| `scripts/check_method_discipline.py --selftest` | (시작 미측정) | 128/128 |

- 실행 판: 먼저 `74f84105c` 에서 전 묶음을 돌렸습니다.  그 뒤 바뀐 파일은 `scripts/rint_r_chain.py` (env_record) 와 시험 둘입니다.  그 파일을 불러오는 묶음 (사슬 · e2e · carbon_junction · b6 · s0) 과 규율 검사는, 그 파일이 끝 트리와 같은 판에서 다시 돌린 값을 끝 칸에 적었습니다.
- 3.8 판 수 차이: test_step3_conv_cert = 29/29.  기존 kgy 단계와 같은 수입니다 (`docs/reviews/rint2_py38_compat_evidence_20261024/`).

## 4. kgy 판 — `scripts/check_kgy_py38.sh`

Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1.

| 실행 | 트리 | 결과 |
|---|---|---|
| 1 | `74f84105c` | 10/11 — test_rint_r_chain 274/275 · Y08 실패 |
| 2 | `8661d1d83` | 11/11 (사슬 275/275) |
| 3 | `f9fc67c76` | 11/11 (사슬 276/276 · carbon_junction 465/465) |
| 4 | `f38aec706` (끝) | 11/11 — run_contract 124 · step3 rint PASS · ptfe 242 · carbon_junction 466 · b6 490 · runner 128 · 사슬 276 · e2e 20 · target_cert 264 · conv_cert 29 · s0 163 |

- Y08 원인은 시험이었습니다.
  - 감도 사다리 꼴 h 는 "주 예측과 다른 환경" 이어야 하는데, 그 자리에 KGY_UNIT 을 썼습니다.
  - 주 예측은 이 프로세스의 환경으로 돕니다.  호스트가 kgy 판이면 두 환경이 같아지고, 사슬은 (옳게) 멈추지 않았습니다.
- 고침: h 단위의 numpy 칸 = 이 프로세스 판 + 꼬리표.  어느 호스트에서도 다릅니다.
  - 변이 B1-env-unknown-ok · B1-key-no-env 는 고친 Y08 에도 그대로 걸립니다 (사슬 `--only Y,D1` 각각 21/22).
- 이 결함은 B1 에서 들어와 kgy 단계를 돌리기 전까지 보이지 않았습니다.  묶음 중간에 kgy 단계를 돌리지 않은 것이 내 빈틈입니다.

## 5. 끈 경로

기반 = `9bec6b764` · `49a1af626` 사본 (`--old-scripts`) · 트리 = `74f84105c`.  그 뒤 커밋은 payload 밖입니다.

| 꼴 (b6 B) | 허용된 칸 (9bec) | 허용된 칸 (49a) |
|---|---|---|
| off LEAN2 · centerline LEAN2 · off LEAN3 · face_alpha LEAN2 · rtol 1e-12 · face_alpha + rtol | 0 | 0 |
| off + 접합 | 1 (RCA1 · 한정어 문장) | 1 |
| 접합 + SV (rtol 없음 · 진단 기록) | 1 | 6 |
| 접합 + SV + rtol (증서 구간) | 4 | 29 |
| 두 섬유 덩어리 + 접합 + SV + rtol (위 끝 풀이) | 6 | 53 |

- 결과: b6 B 39/39 · 39/39 · z3 O 15/15 · 15/15.
- σ · n_dof 는 허용 표에 없어서 다르면 늘 실패합니다.  열 꼴 모두 같았습니다.
- B6 의 새 칸 (`fp_cjunc_graph` · sv_cf 경우 · '+' 만) 은 허용 행 RR 두 줄로 받습니다.

## 6. 변이 표

새 규칙 줄을 하나씩 되돌린 작업 트리 사본에 새 시험 부분집합을 돌렸습니다.

| 묶음 | 변이 수 | 첫 판 | 생존 → 시험 | 끝 |
|---|---|---|---|---|
| B1 같은 코드 | 13 | 11/13 | 사슬↔러너 HEAD 줄 → Y11 · 러너 sha256 줄 → Y12 | 13/13 |
| B2 같은 침대 + X6 | 15 | 13/15 | 증거 census 줄 → Q07 · 기록 사본 줄 = 동등 (먼저 도는 기록 계약 (사본 = 증거) 과 증거 줄이 함의) | 14/15 + 두 줄 변이 잡힘 |
| X3 · X5 | 12 | 10/12 | 꼴 원장 줄 → S8h⁗ · ⑧ 옛 자리 줄 = 동등 (사유 순서만 다름) | 11/12 |
| B6 소비자 | 6 | 3/6 | 주 계 대조 → ⑧ · 위 끝 지움 → ⑨ · 원천 꼴 → ⑩ | 6/6 |
| B6 사슬 | 6 | 5/6 | 주 해 증서 사본 ↔ 런 주 증서 지문 → RG07 | 6/6 |
| B6 생산자 (지문 · step3) | 7 | 6/7 | dof 식별 집합 칸 → ⑥′ | 7/7 |
| B7 | 2 | 2/2 | — | 2/2 |

- 합계: B1–B5 34/40 → 38/40 (동등 2) · B6 · B7 16/21 → 21/21.
- 끝 증서 대조 줄을 끈 변이 (G-end-off) 는 QG ① · ⑦ · ⑪ 에 걸립니다.
- ⑥′ 의 한정: 생산 그래프 (판에 닿는 성분) 의 dof 는 늘 간선이나 판 결합에 나옵니다.  그래서 그 칸은 생산 경로에서는 동등입니다.  ⑥′ 은 함수 문서의 보장 (고립 dof) 을 지키는 시험입니다.

## 7. 탐침 재실행

끝 = `f38aec706` 의 git 밖 사본 · 시작 = `20651fd36` 사본.

| 탐침 | 시작 | 끝 |
|---|---|---|
| `provenance_probe.py` F1 git 밖 | 받음 (HEAD · dirty None 을 기록만) | 멈춤 (rev-parse rc 128 = 미확인) · 판정도 멈춤 |
| F1 status 실패 | 받음 (dirty False) | 멈춤 (status rc 128) |
| F2 사슬 ≠ 러너 | 받음 | 멈춤 (HEAD · 러너 폴더 지문).  탐침의 verdict_problem 칸은 지금 사슬 쪽만 보는 함수라 (설계) null 그대로 |
| F5 `commit:` (빈 sha) | 받음 | 멈춤 |
| F8 원 입력 손실 | 옛 보고 받음 | `S0_REPORT_MISMATCH`.  단 사유는 합성 보고에 역할 파일이 없어서입니다 (꼴 거부).  침대 대조의 증거가 아닙니다 → 우리 W01 · W02 · W06 이 증거 |
| `s0_integration_probe.py --fixture-argv` 침대 바뀜 | 옛 보고 관문 통과 | `S0_REPORT_MISMATCH`.  단 사유는 F5 (고정물 커밋 `aaaa…` 이 저장소에 없음) 로, 침대 대조보다 앞 관문입니다 |
| `atk2_census.py` (X6 · 계약 수준) | census 까지 0 = 계약 받음 · UNCHECKED → [] | 그대로 (설계 — 계약에는 원천이 없음).  사슬 시험 Q01–Q05 · Q07 = 멈춤 · 원천 대조 = QG ⑨ 거부 |
| `atk2_sv.py` (X3 · X5 · C1) | 652 잎 | 19 잎이 바뀜 = X3 1 (QDX 아래 ← 위 · 거부) + X5 18 (꼴 · 관계 · 거부).  나머지는 같음 |
| 1 회차 `atk_sv.py` | — | B5 뒤 출력과 바이트 같음 |
| 회차 ① `probe_actual.py` · `probe_weighted.py` | — | rc 0.  매니페스트 새 잎은 qualifiers[9] 와 conv_cert · conv_cert_full 의 `fp_cjunc_graph` 뿐.  `k0_assembled_systems.json` 1,251 잎 같음.  원천 없는 판정값 그대로 (설계) |
| 회차 ① `probe_diagnostic_overflow.py` | 기본 = 경고 1 · 장부 ok · kcl inf · `POSITIVE_SOLVED` ok False.  경고 = 오류면 RuntimeWarning 예외 | 두 모드 모두 경고 0 · 장부 문제 · kcl None · `NOT_CERTIFIABLE` ok False |

- 끝 트리의 출력 다섯 (provenance · s0 · atk2_census · atk2_sv · atk_sv) 은 B5 뒤 출력과 바이트 같습니다.  B6 · B7 · 후속 커밋의 영향은 없습니다.
- 회차 ① 탐침 셋은 `8661d1d83` 트리에서 돌렸습니다 (그 뒤 커밋은 시험만).
- 판정문 기하를 끝 코드로 대조했습니다.
  - 원천 = 주 `e5afc9eae437…` · 아래 `99f8bdf9f151…` · 위 없음.
  - 정직한 기록 + 원천 = 받음.  바꿔 끼운 기록 + 원천 = 거부 (아래 끝 지문 = 주 계).
  - 문턱 1.01: 원천으로 확인된 정직한 기록 = `SV_DEPENDENT` · 원천 없음 = `SV_UNCHECKED` · 그래프 문 없는 단위 판정 = `[]` (RR1-01 의 거짓 clear).

## 8. B6 · B7 상세

**B6 (RR1-01) — 무엇을 보장하나 · 한정**

- 지문에 들어가는 것:
  - dof 식별 집합.
  - 쌍 (min, max) 마다 병렬 항 전도도의 정확 합.  binary64 를 정확값으로 받아, 합이 binary64 로 표현되면 그 binary64, 아니면 정준 (홀수 N, E).
  - 아래 · 위 판 결합 (dof 마다 정확 합).
- 같은 전기 회로 = 같은 지문.  비유한 전도도 · 음수 dof = 거부.
- Fraction 독립 대조 (끝 코드): 3,000 짝 (같음 1,194 · 다름 1,806) · 놓침 0 · 충돌 0.  최대 + 최대 ≠ 최대 한 항 · 비유한 거부 3/3.
- 생산자:
  - 실제로 푼 계 (판에 닿는 성분 · 영값 증서가 증명한 무관통 끝 포함) 를 지문합니다.  단락 끝은 지문이 없습니다.
  - CONV_CERT + SV 켬 런만 지문을 싣습니다.  노브 끔 = 바이트 그대로 (끈 경로).  증서 없는 SV 기록 = 지문 없음.
- 소비자:
  - 원천이 없는 문맥에서는 꼴 (hex64) 만 봅니다.
  - 원천이 있으면 주 해 · 비를 싣는 끝마다 대조합니다.  원천에 위 끝이 있는데 기록에 없으면 거부합니다.
  - 금지 셋 (사본끼리 비교 · `G_cut != G_full` · 원시 간선 수) 은 쓰지 않았습니다.  그래서 정직한 FLOAT (아래 = 주) 와 등전위 다리 (G 같음) 를 받습니다.
- 사슬:
  - 원천 없음 · 원천 실패 = 미확인 → 판정 `SV_UNCHECKED` (clear 도 의존도 아님).
  - 대조 불일치 = `CA_EXT_RECORD`.
  - 판정은 단계 요약을 믿지 않고 원 팔을 다시 읽습니다 (RG06).
- 한정 꼴:
  - 남은 한정 꼴 여섯 ((a) (b) (c) (a′) (b′) k 0) 은 원천 없는 계약이 받습니다 (전과 같음).  원천 대조로는 전부 거부됩니다 (QG ⑪).
  - X6 꼴 다섯 + 원천 = "위 끝을 지운 기록" 으로 거부됩니다 (QG ⑨).
  - 단 지금 사슬에는 원천이 없습니다.  이 거부들은 원천이 생긴 뒤의 일이고, 그 전까지는 SV 축 전체가 `SV_UNCHECKED` (차단) 입니다.
- 위조 한정 (D2): 증서 지문 칸까지 원천 값으로 고친 기록은 가리지 못합니다.

**B7 (RR1-02) — 한정**
- 범위는 이 합 하나 (`target_kcl_raw`) 입니다.
- 무작위 30,000 회로 탐색은 고치기 전에도 0 회였습니다 → 판별력이 없어 증거가 아닙니다.
- 다른 진단 합의 넘침 = 미확인.

**조립 · 지문 비용**

| 크기 | 지문 시간 | 최대 RSS 증가 |
|---|---|---|
| 픽스처 QG PAR (7×3×10) · QD2 ① (5×3×9) | 조립만 9.6 · 4.3 ms ↔ SV 켬 전체 풀이 7.4 · 5.1 ms (오버헤드 지배) | — |
| 합성 0.25 M dof · 0.75 M 간선 (병렬 0.5 %) | 0.35–0.37 s | +55–57 MB |
| 합성 1 M · 3 M | 2.1–2.5 s | +217–230 MB |
| 합성 4 M · 12 M | 10.9–12.7 s | +919–923 MB (≈ 77 B/간선) |
| SBE vox 0.15 · n_dof 26,438,766 · 간선 ≤ 3·n_dof ≈ 79 M **(추정)** | ≈ 70–85 s | ≈ 6 GB 일시 |
| DBE vox 0.15 · n_dof 26,796,346 · ≤ 80 M **(추정)** | 같은 자릿수 | 같은 자릿수 |

- 각 범위는 두 번 잰 값입니다.  큰 값은 다른 시험과 같이 돈 판입니다.
- n_dof 출처 = `docs/data/w4b_ptfe_off_20260827/p2_SBE_sph_a0.json` · `p2_DBE_sph_a0.json` (08-27 침대).  지금 R 침대의 수 · 실침대 병렬 간선 비율 = 미확인.
- SV 팔마다 지문 2–3 개 (주 · 아래 · 위) ≈ 2.3–4.3 분 → all3 12 팔 ≈ 28–51 분 · R_j0 4 팔 ≈ 9–17 분 (CPU 한 줄기 · 추정).
- 소비자 원천을 (가) 로 하면 SV 팔마다 payload 의 CG 밖 부분 (미측정) 과 같은 지문 비용이 더해지고, 판정 때 다시 듭니다.

## 9. 문서 · 웹앱 고친 자리

| 자리 | 항목 | 무엇 |
|---|---|---|
| `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` | B2 · B2x · B3′ · B6 | S0 schema v3 → v4 줄 · 머리 줄 (묶음 B · B6) · §2-1 끝 줄 · §11 ④ (재압밀 · 재생성 침대 = 새 S0) · §2-1b (같은 코드 · 상자 ⑤) · §5-6 SV 행 (census 외부 결합 · X3 · X5 · 끝 증서 가중 그래프 귀속) · §10 멈춤 뜻 넓힘 (`CODE_PIN_MISMATCH` · `S0_REPORT_MISMATCH` · `CA_EXT_RECORD` · 새 이름 없음) · 결과 0 건 |
| `docs/reviews/rint2_kgy_commands_20261020.md` | B2 | 판정 · 다시 판정 명령에 `--root ~/sdcp` + 설명 |
| `webapp/static/explain/rint_overview_20261021.html` | B3′ | 상자 ⑤ (수정 계획 §2 문안 그대로) · 머리 줄 |
| `webapp/templates/mpm_lab.html` | B6 | SV 줄 (Jinja · JS) 에 "그래프 귀속 = 사슬 대조 (봉인 원천 · 없음 = SV_UNCHECKED)" + 제목 |
| `scripts/carbon_junction.py` CJUNC_QUALIFIERS | B6 | 10 번째 한정어 (SV 반사실 그래프 귀속 · 원천 없음 = SV_UNCHECKED · 지문 = 그래프 정체성) |
| 웹앱 해당 화면 없음 | B1 · B2 · B2x · B4 · B7 | 같은 코드 · 같은 침대 멈춤 · census · X3 · X5 칸 · KCL 진단은 웹앱 화면에 없습니다 (SV 줄은 그 칸을 보이지 않음) |

## 10. 원장

- 이 가지 (B5 `6602b660c`) — 새 ID 없음:
  - RCA2-02 → claimed_fixed `198f3a35c`.
  - RCA2-03 → claimed_fixed `5497760cf` (note 에 X6 `39104710a` · B3′ `9506a54dc`).
  - RCA2-04 → note 에 X3 · X5 `7dc8dc647` · S8h⁗ (status · `claimed_fixed_sha` 그대로).
- 메인 몫 (RR1-01 · RR1-02 는 메인 `dc0a97212` 에만 있습니다):
  - RR1-01 → claimed_fixed `e4714241b` (보강 `f9fc67c76` · `f38aec706`).
  - RR1-02 → claimed_fixed `74f84105c`.
  - RCA2-04 (메인에서 부분 · 닫는 조건 RR1-01) 의 status.
- Y08 호스트 의존 (내 시험 결함 · 끝 검증에서 잡음) 을 SELF 로 올릴지 = 메인.

## 11. S0_SAME_FILES · 옮긴 시험 · 작업 트리

- `S0_SAME_FILES` 일곱 중 바뀐 셋:
  - `scripts/ca_s0_census.py` (B2 · B2x) · `scripts/carbon_junction.py` (B4 · B6) · `scripts/step3_sigma.py` (B6).
  - 안 바뀐 넷: ptfe_face_alpha · mpm_webapp_payload · fibre_segment_raster · sr01_stamp_compare.
  - → R 에 쓰는 S0 보고 (단계 1 · 2) 는 끝 핀에서 다시 만들어야 합니다.  kgy 단계 1 (핀 `89fc47011`) = 개발 자료.
  - S0 보고 schema = `ca-s0-census-v4`.  사슬이 v4 를 요구하므로 옛 보고 = `S0_REPORT_MISMATCH`.
- git 고정물로 옮긴 시험 (B1) — 검사는 약하게 하지 않았습니다:
  - test_rint_r_chain: 사슬 폴더 + 러너 = 임시 git 저장소 · F5 용 매달린 계획 커밋.
  - D16: clone.
  - test_rint_r_chain_e2e: scripts 사본 + 사전등록 문서 + `.gitignore`.
  - `scripts/check_kgy_py38.sh` 는 저장소 안에서 돌기 때문에 바꿀 것이 없습니다.
- 작업 트리 안 ignore 밖 파일:
  - 러너 출력 = 트리 밖 (`~/sdcp/…`) · 러너 규율 로그 = mktemp.
  - `__pycache__` 는 ignore 안입니다 (kgy 단계의 3.8 이 씀).
  - ⚠ `.venv/` 는 ignore 밖입니다 (D5).

## 12. 회차 ① 결과와 이 묶음

| 회차 ① (`docs/reviews/codex_review_rint2_rr_round1_20261026.md`) | 이 묶음 |
|---|---|
| RCA2-01 · 06 · 08 · 09 · RCA-06 닫힘 · RCA2-04 부분 · S0 단계 1 개발 조건부 GO · 등록 R HOLD | 바꾸지 않음 |
| RR1-01 [P2] k = 0 끝 증서 바꿔치기 (병렬 간선) = 거짓 clear · census 외부 결합만으론 안 닫힘 | B2x = census 만 (RR1-01 안 닫음) · B6 = 끝 가중 그래프 귀속 (원천 · 위조 한정 · D1 · D2) |
| X6 (P2) · X3 · X5 (P3) | B2x · B4 (+ B6 원천 대조 QG ⑨ · ⑪) |
| RR1-02 [P3 · 비차단] 진단 합 넘침 | B7 (이 합만) |
| 회차 ② 조건 = B/C 통합 · 작은 실제 생산자 → 게시 · 판정 → 재판정 · 최종 핀 S0 · 환경 · 비용 자료 | 미충족 (원천 D1 · 묶음 C 남음) · 비용 자료 = §8 (추정) |

## 13. 결정 필요 (고르지 않은 자리)

1. **[B6 · 급함] 생산 그래프 원천** (`scripts/rint_r_chain.py` 의 `SV_GRAPH_SOURCE` · 지금 None).
   - 정하기 전까지는 증서 구간 SV 모서리가 전부 `SV_UNCHECKED` 이고, R 판정이 SV 축에서 막힙니다.
   - 선택지:
     - (가) 사슬이 러너로 payload 를 조립만 하는 꼴로 다시 부른다 (`solve_sigma_z(cjunc_graph_only=True)`).  같은 코드 · 같은 킷 입력에서 다시 조립합니다.  러너 env 축과 payload 인자가 새로 필요합니다 · 비용 §8.
     - (나) 생산자가 raster 옆 파일을 S0 봉인 `sid_off_fp` 에 묶어 남기고, 사슬이 킷에서 원장 · 계획을 다시 만들어 조립한다.
     - (다) 원천 없이 fail-closed 를 유지한다.
2. **[B6] 위조 한정** — 증서 지문 칸까지 고친 기록.
   - 선택지: 한정으로 둔다 (지금) / 끝마다 φ 를 남겨 소비자가 다시 조립한 그래프 위에서 증서를 다시 검사한다 (끝마다 ≈ 0.2 GB · 추정) / 소비자가 다시 푼다 (CG 비용).
3. **[B6] 메모리** — 지문 하나에 ≈ 6 GB 가 일시로 듭니다 (추정).  쪼개 셈 (열쇠 범위 흐름) 을 할지 정해야 합니다.  kgy 호스트의 RAM 여유는 미확인입니다.
4. **[B1] 러너 venv** — `VIRTUAL_ENV` 가 비고 `MPM_NO_VENV` 가 없으면 `scripts/sdcp_gain_vox015_8arm.sh` 가 `$HOME/dem-venv` · `$SCR/../venv` · `$SCR/../.venv` 를 켭니다.
   - 그러면 환경 지문 (사슬 프로세스) 과 payload 의 실제 환경이 다를 수 있습니다.
   - 선택지: 그때 사슬이 멈춘다 / 사슬이 러너에 `MPM_NO_VENV=1` 을 준다 / 러너가 자기 환경 단위를 기록하고 사슬이 대조한다 / 그대로 둔다 (venv 를 켠 뒤 사슬 · 명령 문서).
5. **[B1] `.venv/` 가 `.gitignore` 밖** — 저장소 뿌리에 `.venv` 가 있으면 (가-1) 로 dirty → `CODE_PIN_MISMATCH` 입니다 (러너가 찾는 venv 자리 중 하나).  kgy 는 `~/dem-venv` (트리 밖) 입니다.
6. **[B4] X3 가 한정 일부를 막음** — BRIEF 는 "한정 = 지금처럼 받는다" 였습니다.
   - 그런데 (c) 와 아래 끝 = 주 해 기록의 (b) · (b′) 는, 수 칸을 그대로 두면 이제 거부됩니다.  X3 iff 의 자연한 결과이고, 한정을 따로 막는 규칙은 없습니다.
   - 새 칸까지 0 으로 맞춘 일관 편집은 계약이 여전히 받습니다.
   - 거부가 늘어난 것을 받아들일지 확인해 주세요.
7. **[B4] 관계 `k + kul ≤ ku`** (아래 끝 끊은 쌍 + 위 끝의 아래 대비 끊은 쌍 ≤ 위 끝 끊은 쌍 · `kul ≤ n_edges_cut` 을 함의) 를 "같은 원리" 로 넣었습니다.  Q21 (가) 범위 안인지 확인이 필요합니다.
8. **[B4] ⑦ (위 끝 `n_sv_faces_cut` = 아래 끝) 도 X5 와 함께 앞으로 옮겼습니다.**  진단 · 비 없는 기록은 `_removed_problem` 만 봅니다 (그대로).
9. **[변이] 동등 판정 셋** — X6 기록 사본 줄 · X5 ⑧ 옛 자리 줄 · (생산 경로 한정) 지문 dof 식별 집합 칸 (함수 보장은 ⑥′ 이 지킴).  Codex 확인이 필요합니다.
10. **[탐침] Codex 탐침 꼴** — F8 · s0 침대 바뀜의 "고친 뒤 거부" 는 앞 관문 (역할 파일 없음 · F5 고정물 커밋 없음) 때문입니다.  침대 대조의 증거는 우리 W01 · W02 · W06 입니다.  탐침 꼴을 고칠지는 Codex 몫입니다.
11. **[B7] 범위** = 이 합 하나입니다.  다른 진단 합의 무경고 보장은 미확인이고, 전칭으로 쓰지 않았습니다.
12. **[B6 · 웹앱]** 웹앱 SV 줄은 표지 문구만 바꿨습니다.  대조는 사슬이 하고, 웹앱 화면에는 원천 대조가 없습니다.

- 메모 (결정 아님): B5 때 `--expect-identical` (바로 앞 커밋 기반 전용 인자) 을 `9bec6b764` 기반에 쓰니 B4 새 칸이 차이로 나왔습니다 (예상 · 끈 경로 판정은 허용 표 RR 행).  B6 뒤로는 그 인자로 돌리지 않았습니다.
- scratch 의 묶음 B 사본 · 로그는 다 지웠습니다.  작업 트리도 깨끗합니다 (`git status --ignored` 출력 없음 · HEAD `f38aec706`).
