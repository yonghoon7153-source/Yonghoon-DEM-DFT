# 사전 공격 리뷰 S3 — 대상 `5e95047fc` (기반 `93d93bc02` → 바뀐 scripts · webapp) · 2026-10-22 11:37–12:15 UTC

**한 줄 결론: 새 P1 0 · 새 P2 1 (F1 — git 밖이면 코드 핀이 HEAD None == None 으로 통과 · 목록 밖 σ 모듈 변경 미검출) · P3 7 · 관찰 1.  지난 회차 결함 (PRE2-impl-01 · 02 · 03 · PRE2-design-01 · 02 · 06 · 08) 의 원 반례는 이 트리에서 전부 거부 · 표지된다.  변이 25 중 23 잡힘 + 내가 더한 3 중 1 잡힘 — 살아남은 것 중 C5 (위 끝이 첫 덩어리만 뺌) 는 합성 침대에서 틀린 "표지 없음" 을 만든다 (시험 틈 · F4).**

- 범위: `git diff 93d93bc02 5e95047fc -- scripts webapp` (14 파일) + 계약 = 등록 R §5-6 SV 행 · §2-1 · §2-1b · §10 · §10-2 ㊲–㊶ · kgy 명령 §2-2b · §2-3 · §3.
- 고친 사람 설명 (`stage2_report.md` · `pf2/REPORT*` · `PROMPT_*`) 은 읽지 않았다.  숫자 = 아래 실행 출력.
- 탐침 · 사본 · 출력 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/s3/work/` · 트리 무변경 (`git status --porcelain` 빈 출력 · 변이는 사본 `work/mut2` · `work/mut3` 에서 · 끝에 원본과 `cmp` 같음).
- 환경: python 3.11 · `-I` · `nice -n 19` · `OPENBLAS_NUM_THREADS=1` · 시험 사본 = scripts 복사 + docs · webapp 링크 · **git 밖** (그래서 접합 시험의 C0 · LEN-BIT 두 칸 = `git show` 실패 · 환경).

## 1. 지난 판정문 탐침 재실행 (이 트리)

| 탐침 | 지난 결과 (`93d93bc02`) | 지금 (`5e95047fc`) | 판정 |
|---|---|---|---|
| impl `probe2_sv_unsplit` 두 섬유가 같은 덩어리를 지남 (참 비 +∞) | 비 1.0 · computed · 사슬 표지 [] (PRE2-impl-01) | 아래 1.0 · 위 +∞ (`no_through_without_sv`) · 못 가른 덩어리 1 · 사슬 (문턱 2) `['SV_UNCHECKED']` | 닫힘 (등록 괄호 규칙대로 · 차단) |
| 같은 탐침 대조 ① (A 만 지남) | ∞ · `SV_DEPENDENT` | ∞ · 덩어리 0 · 위 = 아래 · `['SV_DEPENDENT']` | 그대로 |
| impl `probe2_svcf_record` (옛 꼴 6) | 5 꼴 받음 (PRE2-impl-02) | 6 꼴 모두 거부 (사유 = 괄호 칸 없음 · 값 검사 판별은 이 탐침으로 못 함 → §2-1 내 탐침) | 원 꼴 닫힘 |
| impl `probe2_plan_gate` (28 꼴) | 10**400 정수 3 = 잡히지 않은 OverflowError · 중복 칸 = 받음 (PRE2-impl-03) | 28 꼴 전부 구조화 멈춤 (`PLAN_INVALID` · `PLAN_NUMBER_UNREGISTERED`) · 정상 = 받음 | 닫힘 |
| impl `probe2_band_knife` · `item9_assemble` · `selfd_ii` · `degenerate` | (지난 출력) | 같은 숫자 (599.035 · 1e7 · 항목 9 문장 · d0 0.1 · 12.5 rel 1.7e-15) | 그대로 |
| design `probe_A` (157 키) · `probe_B` (34 키 · 무작위 20,000) · `probe_D` (18 키) | (지난 JSON) | 지난 JSON 과 키별 차이 **0 · 0 · 0** | 그대로 |
| design `probe_C` (같은 HEAD dirty) · `probe_E` (단계 2 뒤 계획 B) | 멈춤 없음 (PRE2-design-02 · 01) | 트리를 바꾸는 탐침 · 옛 CLI 라 직접 안 돌림 — 같은 꼴 시험 D01–D06 · B01 통과 (사본 사슬 시험 **218/218**) | 시험으로 닫힘 (git 밖 꼴 = F1) |

## 2. 바뀐 함수 — 지난 HOLD 부류

| 자리 | 넣은 것 | 결과 |
|---|---|---|
| `ca_ext_svcf.sv_cf_problem` (괄호 · 값 대조) · `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_svcf_validator.py` 22 꼴 | 비 ≠ G_full/G_cut (상대 3e-12) · 위 < 아래×(1−τ)/(1+τ) (17 %) · nu True / 1.0 · status_hi 끝 공백 · 위 no_through 인데 G_cut 1e-300 · 덩어리 0 인데 위 끝 기록 | 전부 거부 ✓ |
| 같은 곳 | 위 끝 `n_components_removed` 7 ↔ 기록 nu 1 · 위 끝 증서 None (아래는 있음) · 아래 끝 증서 None · 원 기록 증서 = 문자열 "failed" (투영이 None 으로 바꿈) · nu = 10**400 | **받음** → F3 |
| 사슬 `load_plan` · `load_s0_plan` · `read_s0_report` · `_num` · `_json_strict` | 10**400 · 1e400 · NaN 토큰 · 음수 · 글자 · bool · 중복 칸 | 전부 구조화 멈춤 ✓ (탐침 28 꼴 · 시험 N05–N07 · B04) |
| 사슬 `s0_stage2_problem` · `s0_stage1_problem` · `s0_code_problem` (직접 호출) | `plan_source` "commit:" · "commit:not-a-sha;rm -rf" | **받음** → F5 |
| 같은 곳 | 지문 목록 같은 이름 둘 · 러너 폴더에 일곱 파일 없음 | `CODE_PIN_MISMATCH` ✓ · 받음 (㊴ 공개 · 결함 아님) |
| 사슬 `sv_assess` | 아래 · 위 NaN · −∞ · 0 · bool · 빈칸 | 못 읽음 → `SV_UNCHECKED` ✓ (시험 U15 · 변이 R10 이 잡힘) |
| 웹앱 SV 줄 Jinja ↔ JS (`docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/webapp_sv.py` · jinja2 + node 로 같은 기록을 그려 글만 비교 · 5 꼴) | 괄호 · 덩어리 수 · 상태 · 위 끝 상태 · 표지 · HTML 이스케이프 | 같은 뜻 · 표기 차 셋 → F7 |

## 3. 보장마다 작은 해석 반례

| 보장 | 반례 (손으로 풀림) | 결과 |
|---|---|---|
| SV 괄호 아래 ≤ 참 ≤ 위 (셀 그래프 안) — `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_sv_producer.py` | S1 A · B 가 덩어리를 함께 지남 + 독립 섬유 C: 위 1.9782608695652213 ↔ 손 (I_AB + I_C)/I_C 1.9782608695650687 (상대 7.7e-14) · 아래 1.0 | ✅ 성립 · 참 = 위 · 사슬 (문턱 2) 표지 없음 (옳음) |
| 같은 보장 | S5 두 관통 섬유가 덩어리 공유 (대칭 · 참 비 = 1 정확) | ✅ 성립 [1, +∞] · 정보 0 → `SV_UNCHECKED` (관찰 O1) |
| 같은 보장 | S4 σ_SDCP = 0 | ✅ 위 = 아래 = 1.0 |
| census 불일치 = 위 끝 안 풂 (fail-closed) | S3a census 0 (참 1): 위 끝 `unsplit_census_mismatch` · 기록 nu 0 → 검증기 거부 · S3b census 2: 받음 · `SV_UNCHECKED` | ✅ fail-closed · 서술 차 → F6 |
| 합성 생산 단위 침대 9 (vox 0.15 · Ø1 µm SDCP · R_j 1e6 · `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_sv_randbeds.py` · 합성 · 실침대 빈도 아님) | 못 가른 덩어리 ≥ 1 = 9/9 · census 불일치 0/9 · 괄호 [1.0, 18.6] [1.0, 26.5] [1.0, 1.42] [1.0, 1.0] [3.25, 3.49] [1.0, 16167] [1.40, 11936] [1.02, 11943] [1.0, 1.78] | 문턱 2 → 걸침 5 · 표지 없음 3 · 의존 1 (관찰 O1) |
| 같은 코드 지문 (단계 · 판정) — `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_codepin_nogit.py` | git 밖 사본 · `ca_ext_cjunc.py` 한 줄 고침 | ❌ `code_key` 같음 · `code_dirty_problem` None · `code_verdict_problem` None → F1 |
| 한 핀 작업 트리 (§10 (0)) | 사슬 HEAD a… · 러너 HEAD b… · 러너 폴더 step3_conv_cert · ca_ext_svcf · run_contract 지문 다름 (일곱 파일 같음) | ❌ dirty · S0 보고 · 키 검사 모두 None → F2 |
| 계획 해시 정확 대조 · 단계 2 봉인 | 시험 B01–B12 (변이 R3 · R4 · R13 잡힘) | ✅ |
| 등급 경계 정확값 G0/2 · G0 | 시험 G01 (nextafter 양쪽) · 지난 생존 변이 Ml = 이제 M42 · G01 이 잡음 | ✅ |
| 기계 이름표 = 판정에 안 씀 | `code_key` 에 machine 없음 · 판정 단계 `--machine` = rc 2 (변이 R12 를 D11 이 잡음) | ✅ |

## 4. 찾은 것

| ID | P | 자리 | 최소 재현 | 기대 ↔ 실제 |
|---|---|---|---|---|
| **F1** | **P2** | `rint_r_chain.py:617` `git_identity` (실패 = head · dirty None) · `:1040` `code_dirty_problem` (dirty None = 통과) · `:1029` `code_key` · `:1056` `code_verdict_problem` (head None == None) · `CODE_FILES` 12 (`:154`) · 등록 ㊳ ("dirty null = 기록만" + "목록 밖 모듈은 HEAD + dirty 가 덮는다") | `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_codepin_nogit.py <git 밖 사본>`: `code_record` → HEAD None · dirty None → `scripts/ca_ext_cjunc.py` (payload 가 부르는 접합 배선 · R_j 계획 — `CODE_FILES` 밖) 한 줄 고침 → `code_key` 같음 · `code_verdict_problem` None | 기대: 단계 사이 코드 변경 = `CODE_PIN_MISMATCH` (§10 멈춤) ↔ 실제: git 밖이면 목록 밖 모듈 (`ca_ext_cjunc.py` · `additives.py` · `se_material.py` · `lens_geometry.py` · `step4_dyn.py` · `rint_cycle_traj.py`) 변경이 사다리 → 예측 → 판정 내내 안 보인다.  ㊳ 의 두 문장이 git 밖에서 서로 어긋난다 (운영 = kgy `git worktree` 라 발생 가능성은 낮음 · 추정).  같은 꼴의 단계 흐름: 사슬 시험 전체가 git 밖 사본 (HEAD None) 에서 218/218 그대로 통과 (고정물은 dirty 만 False 로 덮는다 · HEAD None 을 막는 시험 없음).  최소 해결: head 또는 dirty 가 None 이면 멈춤 (또는 지문 = 실제 import 집합) |
| F2 | P3 | `stage_ladder` (`:1858–1890`) · `code_record` (`:1017`) — 사슬 HEAD ↔ 러너 HEAD · `files` ↔ `runner_files` 대조 없음 · 등록 §10 (0) "한 핀 작업 트리" | 함수 호출 (§3 표): 두 트리 HEAD 다름 + 러너 폴더 `step3_conv_cert.py` · `ca_ext_svcf.py` · `run_contract.py` 다름 (일곱 파일 같음) → 모든 핀 검사 None · 변이 **R5** (러너 쪽 dirty 무시) = 사슬 시험 **218/218 PASS** (러너만 dirty 인 꼴 시험 없음 — `d_identity` 가 두 쪽을 함께 바꾼다) | payload 가 러너 폴더의 증서 · SV 투영 판으로 돌고 사슬은 자기 폴더 판으로 검증해도 멈추지 않는다 (같은 단계 안) |
| F3 | P3 | `ca_ext_svcf.py:192` `_bracket_problem` · `:234` `_end_values_problem` · `:67` `_end_proj` | `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_svcf_validator.py` | ① 위 끝 `n_components_removed` ↔ 기록 nu 미대조 ② computed 끝의 증서 있음을 요구하지 않음 (증서 켠 런에서 한 끝만 None 도 받음 · dict 아닌 증서는 투영이 None 으로 바꿔 "dict 이어야" 갈래가 죽은 코드) ③ 투영이 증서 구간을 버려 증서 ↔ G_cut 결합 불가 (다른 풀이의 플래그 증서도 받음) ④ `bracket_rule` = 아무 비지 않은 낱말 (`CJUNC_SV_CF_BRACKET_RULE` 와 미대조) ⑤ nu 10**400 받음.  생산자 정상 경로는 맞게 쓴다 → 옮김 · 다른 판본 기록만 해당 |
| F4 | P3 (시험 틈 · 회귀하면 P1 꼴) | `carbon_junction.py:2503` `_sv_unsplit_cells` (`:2491`) (`lins = … np.isin(g['labf'], labels)`) | 변이 **C5** `labels` → `labels[:1]` (첫 덩어리만 뺌): 접합 시험 전체 **323/325** (실패 2 = C0 · LEN-BIT `git show` 환경 · 기준선 대조 §5) · b6 S **173/173** · 사슬 = 생산자 안 부름.  같은 변이로 합성 침대 9: 위 18.6 → 1.0005 · 26.5 → 1.34 · 16167 → 1.37 → 문턱 2 에서 `SV_UNCHECKED` → **표지 없음 3/9** | 기대: 덩어리 둘 이상 = 전부 뺌 시험 ↔ 실제: QD2 ①–⑪ · SP14–16 = 덩어리 하나뿐 |
| F5 | P3 | `rint_r_chain.py:896` `s0_stage2_problem` (`plan_source.startswith('commit:')`) | `"commit:"` · `"commit:not-a-sha;rm -rf"` → 받음 | 꼴 검사가 접두어만 · (R 계획 sha ↔ 등록 줄 대조가 있어 값 오염은 아님) |
| F6 | P3 | `carbon_junction.py:2506` `sv_counterfactual` census 불일치 갈래 · 시험 QD2 ⑧ · `ca_ext_svcf.KNOWN_STATUSES` | S3a (census 0 · 참 1) | 생산자가 자기 검증기가 거부하는 기록을 낸다 → 실제 경로 = payload 가 게시 거부 (`mpm_webapp_payload.py:1256` `STEP3_CA_EXT` · exit 4 · `--allow-partial-step3` 아니면) · 사슬이 읽어도 `read_run` → `CA_EXT_RECORD` 멈춤 (fail-closed) ↔ QD2 ⑧ 문구 "사슬 = SV_UNCHECKED" 는 `sv_assess` 단독 결과 · 새 상태 `unsplit_census_mismatch` 가 `KNOWN_STATUSES` (문서용) 에 없음 |
| F7 | P3 | `webapp/templates/mpm_lab.html` 81 행 (Jinja) ↔ 233 행 (JS) SV 줄 | `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/webapp_sv.py` | 뜻 같음 · 표기 차: 1.0 ↔ 1 · 1e+16 ↔ 10000000000000000 · 2.0 ↔ 2 (비차단) |
| F8 | P3 · 질문 | `rint_r_chain.s0_report_record` (계획 · 코드 칸만) | 코드 읽기 | S0 보고의 침대 입력 (`inputs.files` · raster) ↔ R 런 팔 (`sid_fp` · 입력 지문) 미결합 — 킷 침대가 S0 뒤 다시 만들어지면 s_min · 단계 2 봉인이 다른 침대 위의 것이 된다 (등록에 "같은 침대" 문장 없음) |
| O1 | 관찰 | SV 괄호의 정보량 | §3 S5 · 합성 침대 9 | 덩어리가 있으면 위 끝 = SDCP 구 통째 삭제 → 섬유가 끊겨 위 끝 1e4 까지 · 참 비 1 인 대칭 꼴도 [1, ∞] · 문턱 2 에서 합성 5/9 `SV_UNCHECKED` (차단) — 실침대에서 PASS 문장이 대부분 막힐 수 있다 (추정 · 합성) · 요청서 "닫지 않는 것" 에 한 줄 권고 |

## 5. 변이 (사본에서 한 줄씩 → 시험 → 원본으로 되돌림 · 에이전트 작업 폴더의 mutations_result.json (리포에 안 넣음 · 결과 = 이 표))

기준선 (변이 없음 · 사본): 사슬 `--only B,D,G,U,V,N,C0,S0,M4` 109/109 · b6 `--only S` 173/173 · 접합 `--only QD2,QD,MUT-RCA2` 25/25 · 사슬 전체 218/218 · 접합 전체 323/325 (실패 2 = C0 · LEN-BIT `git show` — git 밖 사본 환경 · C5 변이 판과 같은 둘).

| # | 자리 | 바꾼 것 | 결과 |
|---|---|---|---|
| R1 | `s0_code_problem` | 러너 폴더 지문 대조 끔 | 잡힘 D16 |
| R2 | `s0_stage1_problem` | plan_source 검사 끔 | 잡힘 D08 |
| R3 | `load_ladders` | 두 사다리 S0 보고 기록 같음 끔 | 잡힘 B10 |
| R4 | `verdict_compute` | 단계끼리 S0 보고 기록 같음 끔 | 잡힘 B11 |
| **R5** | `code_dirty_problem` | 러너 쪽 dirty 무시 | **생존** (부분 109/109 · 전체 218/218) → F2 |
| R6 | `code_verdict_problem` | HEAD 대조 끔 | 잡힘 V15 |
| R7 | `code_verdict_problem` | 파일 지문 대조 끔 | 잡힘 D02 |
| R8 | `_json_strict` | 중복 칸 거부 끔 | 잡힘 N05 · N06 · N07 |
| R9 | `sv_assess` | 걸침 → 표지 없음 | 잡힘 V25 · U08b · M41 · U15 |
| R10 | `_sv_readable` | 0 · 음수 읽음 | 잡힘 U15 |
| R11 | `check_after_main` | 코드 키 대조 끔 | 잡힘 D13 |
| R12 | `main` | 판정 단계 `--machine` 허용 | 잡힘 D11 |
| R13 | `s0_stage2_problem` | S0 계획 sha 대조 끔 | 잡힘 B03 |
| R14 | `load_ladders` | 사다리 기록 dirty 무시 | 잡힘 D18 |
| V1 | `_bracket_problem` | 위 끝 칸 ↔ 위 끝 풀이 기록 끔 | 잡힘 S8l |
| V2 | `_values_problem` | 괄호 순서 (위 ≥ 아래×여유) 끔 | 잡힘 S8n |
| V3 | `_end_values_problem` | 비 ≥ (1−τ)/(1+τ) 끔 | 잡힘 S8n |
| V4 | `_end_values_problem` | no_through ↔ G_cut 0 끔 | 잡힘 S8n |
| V5 | `_end_view` | inf 꼴에 수가 실려도 읽음 | 잡힘 S8p |
| V6 | `_bracket_problem` | 덩어리 0 ⟹ 위 = 아래 끔 | 잡힘 S8l |
| V7 | `_end_values_problem` | 증서 = ok 플래그만 | 잡힘 S8n |
| C1 | `_assemble` | 아래 판 결합 안 뺌 | 잡힘 QD2 ⑪ (수 칸) |
| C2 | `sv_counterfactual` | census 불일치 검사 끔 | 잡힘 QD2 ⑧ |
| **C3** | `_piece_pos_of` (`carbon_junction.py:1893`) | 조각 연속 검사 (raise) 끔 | **생존** (25/25) — 방어 갈래 · 깨지면 census 불일치로 fail-closed 공산 (추정) |
| C4 | `_sv_cf_bracket` | status_hi = 아래 상태 | 잡힘 QD2 ① |
| (더함) **C5** | `_sv_unsplit_cells` | 첫 덩어리만 뺌 | **생존** (접합 전체 323/325 · 실패 2 = 환경 · b6 S 173/173) → F4 |
| (더함) C7 | `_assemble` | 덩어리 간선 한쪽 끝 (U) 만 | 잡힘 QD2 ⑪ |
| (더함) C8 | `_assemble` | 위 판 결합 안 뺌 | 생존 (25/25 · b6 173/173) — 값은 같은 변이 (간선을 다 뺀 셀은 판 결합만 남아 전류 0) · 수 칸만 다름 · 결함 아님 |

## 6. 확인했는데 결함 아닌 자리
- 위 끝 조립: 판 결합 빼기 = 주인 고르기 전 셀 dof · 간선 빼기 = 축약 전 dof · σ_SDCP 0 이면 뺄 dof 0 (위 = 아래) · 덮인 위치 dof = SDCP 셀 dof 라 섬유 축 간선도 함께 빠짐 (위 ⊂ 참) — 코드 읽기 + S1 · S4 · S5 숫자.
- 값 봉인: 덩어리 있으면 아래 끝이 ∞ 여도 위 끝을 푼다 (QD2 ⑦ 솔브 3) · 주 해 미수렴 · 주 전류 ≤ 0 = 위 끝도 같은 상태 (QD2 ⑨ ⑩).
- `step3_sigma` 훅: 위 끝 풀이가 주 σ · 주 증서 · 매니페스트 backend 를 안 바꿈 (SP16) · backend 전역은 finally 로 되돌림.
- 사슬 `sv_assess`: 아래 > 문턱 = 의존 (위 무관) · 두 끝 읽고 위 ≤ 문턱 = 없음 · 그 밖 = `SV_UNCHECKED` (아래 못 읽고 위 ≤ 문턱이어도 차단 — 등록보다 보수) · 문턱 비교 = 여유 없음 (등록 ③ 문장 그대로).
- kgy §3 명령 블록 = 사슬 CLI (사다리 `--s0-stage2-report` · `--s0-stage1-report` · 감도 `--after-main` · 예측 · 판정에 S0 인자 없음) — 인자 이름 대조.
- 등록 ㊵ 러너 경로가 코드 키에 들어 기계마다 경로가 다르면 멈춤 = 등록 §10-4 496 행에 공개 (Q3-b).
- 실제 `ca_s0_census` 단계 1 보고 (리포 시험의 픽스처 킷을 `kit_SBE_vgcf100` 이름으로 · `docs/reviews/rint2_pf2_fix_evidence_20261022/stage3_prereview/my_real_s0_report.py`) → 사슬 `read_s0_report` · `s0_stage1_problem` · `s0_code_problem` 모두 통과 · NaN · Infinity 토큰 없음 (사슬 시험 · e2e 의 S0 보고는 전부 손으로 만든 것이라 생산자 ↔ 사슬 결합을 따로 봤다 · 단계 2 실제 보고는 임시 git 저장소가 필요해 못 봄).

## 7. 못 본 것
- `test_ca_s0_census.py` (임시 git 저장소) · e2e · `--long` · GPU · 실침대 — 메인 게이트 몫 · 돌리지 않음.
- design `probe_C` · `probe_E` 직접 재실행 (트리를 바꾸거나 옛 CLI) — 같은 꼴 리포 시험 (D01–D06 · B01) 통과로 대신.
- 실제 단계 2 보고 (개정 커밋 · 임시 git 저장소) → 사슬 결합 · 실침대 보고의 NaN 여부.
- 사본 (`work/mut` · `mut2` · `mut3` · `nogit` · `realrep` · `impl_c5`) 은 끝나고 지웠다 (탐침 스크립트 · 로그 · JSON 은 남김).
