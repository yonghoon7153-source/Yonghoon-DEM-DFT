# Codex 짧은 재확인 요청 — LHS214 FULL 모형 한계 범주 수정 (L214-01 · 02 · 03) (2026-10-15 · 초안 · 결과 0 건 · 발송 = 1저자)

> ⛔ **Codex 재검증 (10-15) = HOLD** — L214-01–03 부분 · 새 P2 `L214R-01`–`03` · P3 `L214R-04` · 판정문 `docs/reviews/codex_review_lhs214_fix_reverify_20261015.md` (증거 `docs/reviews/codex_lhs214_fix_reverify_evidence_20261015/`).

> **한 줄**: LHS214 실패 검토 (`docs/reviews/codex_review_lhs214_failures_20261014.md` · 검토 핀 `1087a9b2f` · 분류 분리 (가) 조건부 지지 · 새 214 · v1.3 HOLD) 의
> P2 셋 (`L214-01` · `02` · `03`) 을 판정문 §2 · §4 A1–A4 의 최소 처방대로 고쳤다 — "수치 인증 성공 / 출력 채택 거부" 를 명시 범주로 만들고, 생산자와 소비 경로 전부
> (일반 게시 · 정지 계약 · τ · 다시 읽기 · 인계 · 배포 · 웹앱 화면) 가 **공용 판정 한 쌍**을 쓰게 했다.  세 결함이 닫히는지 · 새 결함이 있는지 짧게 판정해 달라.
> ✅ **1저자 10-14** — 수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md` Q1–Q5 권고대로 (Q1 (가) 한 묶음 · Q2 (가) 분류 공통 · 배포 자격 역할별 · Q3 (가) 옛 13 건 unknown · Q4 등록 개정 문안 = 초안 · Q5 (가) 문턱 1.5 유지).
> **리뷰 핀** = 이 요청서 §9 가 든 본 가지 커밋 = `9e3ef54ca` (✅ 발송 10-15 · 1저자) · **기준** = `0c557e72a` (수정 직전 본 가지 — 검토 핀 `1087a9b2f` 와 봉인 32 · 인계 도구 바이트 같음 ·
> 그 사이 다른 변경 7 파일은 봉인 · 인계 밖: additives · check_selftest_inventory · make_mixer_deck · mpm3d_compaction · mpm_input_from_case · mpm_webapp_payload · phase_a_precompute).
> 수정 = 본 가지 커밋 (시험 먼저 `d0aa231d4` → 수정 `6d0bec3c3` → 문서 · 증거 → ★ (나′) 시험 먼저 `545d7d4fe` → 수정 · 이 요청서 §9 = 리뷰 핀).  증거 = `docs/reviews/lhs214_fix_evidence_20261015/README.md`.

## 0. 대상 · 지위

- 코드 diff = `git diff 0c557e72a <리뷰 핀> -- scripts/network_conductivity.py scripts/tau_flux.py webapp/pipeline_service.py webapp/app.py webapp/templates/single.html scripts/g2_network_reread.py scripts/lhs_design_dataset.py scripts/lhs_release_build.py scripts/supp20_input_receipt.py`
  + 시험 다섯 (`scripts/test_lhs214_model_limit.py` 신설 · `webapp/test_network_handover_chain.py` ⑤ · `scripts/test_network_solve_certificate.py` G4 · G4b · `scripts/test_lhs_release_v13.py` V2b · `webapp/test_pipeline_provenance.py` 침대 셋) + 등재 두 줄 (`docs/reviews/selftest_inventory.tsv` — 신설 시험 줄 · ★ (나′) 영수증 도구 줄 메모).
  ★ (나′) `scripts/supp20_input_receipt.py` = 봉인 32 · HANDOVER 밖 검사 도구 (code_fp 무관) — 대기 지문 선언 읽기 + selftest (§9).
- ⚠ **봉인 32 가 바뀐다** — 바뀐 봉인 파일 4 (`scripts/network_conductivity.py` · `scripts/tau_flux.py` · `webapp/app.py` · `webapp/pipeline_service.py`) ⇒
  `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` → **`code_fp acc7bfa335ec8fa8a7b76eb981135f16994b084ce0746476c5d05f61488af2ed`** (재봉인 아님 · 보고만 — §4 ·
  두 등록 초안에는 대기 지문 `code_fp_pending` 으로 선언 · 등록 §3 은 그대로 — §9).
- 문서 = 두 등록의 개정 **초안** (⬜ 1저자 비준 대기 · 결과 열람 뒤 정책 개정 이력 명시): `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §9-8 · `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` §9-3.
- 새 214 실행 · WSL · 수치 재계산 없음 · 원장 `docs/reviews/findings.json` 의 `L214-01`–`03` 갱신 = 병합 뒤 본 세션 (이 요청서는 원장을 고치지 않는다) · S3 = 별개 (봉인 수치 모듈 둘이 바뀜 → 재봉인 의무 · S3 HOLD 그대로).

## 1. 판정문 최소 처방 ↔ 수정

| 원장 · 판정문 | 수정 (자리) |
|---|---|
| `L214-01` ① 입력 · 경계 · 수치 검사 먼저 | `solve_network` — 풀이 **앞**에서 기하 넷 (plate_z · box_x · box_y · scale) · G→q 가 유한 양수가 아니면 (NaN · ±∞ · 0 · 음수 · bool · 문자열) `not_computed` + `invalid_geometry` · 곱이 넘친 비유한 q = `non_finite` (둘 다 `NOT_COMPUTED_SOLVE_REASONS` = 기술 실패 · 게시 차단) · `_net_sigma_status` 에서 비관통 판정보다 앞 (Codex 3 노드 plate_z = +∞ 반례 → `invalid_geometry`) |
| `L214-01` ② 적용 범위 · ③ 수치 사다리 그대로 | 단상 이온 · 전자 FULL 만 (`MODEL_LIMIT_CHANNELS` · 열 = 병렬 상한 가드 = 실패 그대로) · 문턱 = `FULL_Q_GUARD_MAX = 1.5` (옛 리터럴 · 비교 `>` 그대로) · 허용치 1e−6 · 사다리 · G > 0 · 1.1·Σg 무변경 · 증서 수준 판정 `model_limit_certificate_problem` = 가지 full · 가드 상태 · 사유 · 게시 값과 **같은** 수치 검사 (`_certificate_numeric_problem` 로 갈라냄) · 채택 단 = 마지막 시도 pass (방법 · 두 전류 같음) — 예외 · 미수렴 · 증서 실패 · 병렬 상한은 높은 q 로 구제 안 됨 |
| `L214-01` ④ 값 null · 진단 q 별도 키 · 증서 보존 · 유도값 없음 | FULL 거부 때 `solve_info` 에 `q_withheld` (원 값) · `q_guard_max` · `guard_policy` (`full_single_phase_q_gt_1p5/v1`) · `sum_g` — 결과 증서에도 (그 넷이 있을 때만 · 정상 · 실패 증서 바이트 그대로) · 가지 상태 `not_computed` + `full_over_conduction` · σ · 차원 σ null · 협착 전력 몫 = None + `CPS_MODEL_LIMIT_STATUS` · CF/FULL 비 없음 · 채널 상태 `model_limit` (`_channel_solve_failure` · `CHANNEL_STATES`) |
| `L214-01` ⑤ 생산자 → 소비자 같은 판정 | 생산자 `_net_sigma_status(…, channel)` 와 소비자 `tau_flux.full_model_limit_problem` 이 같은 증서 판정을 부른다 · q 재구성 = 솔버와 같은 식 · 순서 ((I_b/ΔV)·T)/A · 상대 16ε (§5 Q3) |
| `L214-02` 명시 분리 · 결합 전부 · 다른 실패 우선 | 레코드 수준 공용 판정 `tau_flux.full_model_limit_problem(rec, channel, mode)` — 상태 · 사유 정확히 · 값 · 유도값 null · 관통 분율 (0, 1] · 채널 상태 `model_limit` · 증서 판정 · 증서 채널 · 역할 (H0 · H12 · physics) · contact_mode · 전극 · σ₀ (이온 = 부모 `sigma_grain_S_cm` 정확히 · 전자 = `SIGMA_AM_ELECTRONIC`) · 자리 모드 · 열 = 거부 |
| `L214-02` 면제 상속 금지 (Codex 반례 셋) | ① `certificate_binding_problems` — FULL 모형 한계 가지는 보존된 실제 FULL 증서를 공용 판정으로만 받는다 (`_cert_unpublished_problem` 의 "숫자 없는데 해 주장" 대신) · 다른 가지 (CF · 협착-only) 는 기존 정책 그대로 (CF residual 1.0 = 거부) ② `_g2_mode_problems` — 표기 결손 면제 = 게시되지 않는 진짜 실패 레코드만 (모형 한계 레코드의 `bulk_model` 삭제 = 거부) ③ `ion_record_problem` (0b) — not_computed + `full_over_conduction` = 공용 판정 통과만 None · 실패 = `invalid_input` · 그 밖 not_computed = `solver_guard` 그대로 |
| `L214-02` 소비 경로 (판정문 §2 표) | 일반 게시 · 정지 계약 — `pipeline_service.channel_verdict(net, channel, mode)` 가 `model_limit` 을 공용 판정 통과일 때만 ok (이름만 = fail) · `network_stop_verdict` ③ 모형 한계 가지 · ④ · ⑦ 전력 몫 사유 · ⑨ H12 / τ — `ion_columns` NOT_COMPUTED + 정확한 사유 (`solver_guard` 로 뭉개지 않음 · 값 넷 빈칸 · 앞 게이트 우선) / 다시 읽기 — K6 (생산자 모형 한계 ↔ τ 정확한 사유 + 공용 판정) · K2 · K7 유지 / 인계 — P4 (정지 계약 다시) · 열 사전 문구 / 배포 — §1 `L214-02` 다음 줄 |
| `L214-02` 배포 (판정문 §3 Q2 · Q3) | `lhs_release_build` — 빈칸 코드 `NA_MODEL_LIMIT` (`v13_blank_reason`) · 관통 분류 = 1 (`_v13_class` — 미퍼콜 0 · 기술 실패와 구분) · **주 타깃 Hertz (H0) 모형 한계 = v1.3 주 타깃 배포 HOLD** (`v13_primary_model_limit_problems` — `build_v13` 실제 = ReleaseError · 진단 · dry-run = 경고 · `check_v13` 배포 대조 = 문제) · 재적합 제외 사유 · 상태 집계 = 모형 한계 별도 · README = Codex Q3 권장 문구 (모형 한계 칸이 있을 때만) |
| `L214-02` 전자 · 열 FULL 상태 · 사유 전파 | `_run_all_networks` 가 `electronic_sigma_full_status` · `_reason` · `thermal_…` 를 이온 중심 결과로 · `pipeline_service.NET_MERGE_KEYS` + 8 (physics 꼬리 포함) · physics 거울 + 4 → full_metrics 투영 · 시험 G4b · 체인 ⑤b2 |
| `L214-03` strict missing | `webapp/app.py` — `_dual_row` (한쪽 값이 없으면 그 칸 = `—` 또는 사유 · Δ = `—` · Hertz 복사 없음) · 기존 두 열 CSV 망 절 (`_MODE_DEP_CSV_ROWS` · `_csv_mode_row` — Physics = metrics 의 Physics 값 · 없으면 `—` + 사유) · Step 4 / 4b 파생비 (σ_brug/σ_ionic · CF/FULL · Constriction) · Pass D 기준 행 · Pass E R_brug · 상태 행 (망 상태 · τ 인계 상태 = 모형 한계 문구 · 기술 실패 문구 아님) · `single.html` 표지 · 툴팁 |

## 2. 시험 (시험 먼저 — 고치기 전 코드에서 실패 확인)

| 시험 | 고치기 전 (기준 코드 + 새 시험) | 고친 뒤 |
|---|---|---|
| `scripts/test_lhs214_model_limit.py --selftest` (신설 · A2 행렬) | 13/54 | **55/55** |
| `webapp/test_network_handover_chain.py` (⑤a–⑤k · A3 끝-끝) | 21/34 | **34/34** |
| `scripts/test_network_solve_certificate.py` (G4 더한 키 넷 제외 · G4b) | 27/28 | **28/28** |
| `scripts/test_lhs_release_v13.py` (V2b 닫힌 어휘 + `NA_MODEL_LIMIT`) | 255/256 | **256/256** |
| `webapp/test_pipeline_provenance.py` (침대 셋 더함 · 검사 무변경) | 284/284 | 284/284 |

- ⚠ 신설 시험의 분모 54 ↔ 55 — 고치기 전 코드에서는 예외로 멈춘 묶음 하나가 FAIL 하나로 세진다 (`_guard`).
- 그대로인 묶음 (고친 뒤 · 깨끗한 트리): `test_tau_flux` 55/55 · `test_gen2_role_contract` 44/44 · `test_network_generation2` 18/18 · `test_reread_v12` 22/22 · `g2_network_reread --selftest` 29 ✓ ·
  `lhs_design_dataset --selftest` 391/391 · `lhs_release_build --selftest` 31/31 · `network_conductivity --selftest` · `--selftest-status` 31/31 · `--selftest-temp` · `seal_s3_prerun --selftest` 69 PASS · `run_s3_psi --selftest` PASS ·
  핵심 21 실행 (스크립트 11 · 웹앱 10 · 증거 `final/final_core_summary.log`) + 회귀 묶음 47 실행 (스크립트 13 · 웹앱 34 · `final/sweep_summary.log`) 전부 rc 0 · `check_method_discipline` 0 오류 · `check_selftest_inventory --quiet` ✓.
- 무거운 것 (한 번씩 · 단독 · `OMP_NUM_THREADS=1`): `run_network_194_parallel --selftest` 139/139 (133.8 s) · `wsl_network_smoke --selftest` 16/16 · **`--selftest-real` 4/4 (155.2 s — case15 음성 대조 계속 거부: 원자료 6 조합 · 게시 차단 · 검사 일곱 PASS · 다시 읽기 S0b)**.
- 행렬 (A2) 의 자리: 3 노드 실회로 q = 2 · 경계 1.5 · 1.49999998 · 1.50000002 (원 정밀도) · H0 · H12 · Physics · 이온 · 전자 · 열 예외 · CF · 협착 진단 유지 · 비관통 valid_zero · 경계 중첩 · 첫 사다리 예외 · 미수렴 ·
  증서 실패 · 병렬 상한 · 0 전도 · NaN · ±∞ · bool · 문자열 기하 · 높은 q + 나쁜 증서 · 모형 한계 + 다른 채널 실패 · 세대 결손 · 틀린 q 재구성 · 사유만 위조 · 남의 증서 · 모르는 사유 · 위조 · 결손 33 · 실제 `lhsx_054` 증서
  (Codex 묶음 tgz · q 재구성 1.5370331988867805 = 솔버 순서 · 판정문 값 …802 = g_to_q 곱 · 3 ulp) · 옛 레코드 (solve_failed) 계속 차단 · 배포 빈칸 · 주 타깃 HOLD — Codex 증거 묶음의 스크립트는 실행하지 않고 반례만 우리 시험으로 옮겼다.

## 3. A4 무영향 대조 (`docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py` · 기준 `0c557e72a` ↔ 고친 트리 · 32/32 통과 · 216.9 s)

| 묶음 | 무엇 ↔ 무엇 | 양 | 결과 |
|---|---|---|---|
| N 생산자 | 합성 넷 (SE + AM · GEN2-01 · 비관통 · CF 과전도) × 두 모드 · real_14 세 채널 × 두 모드 · case15 (실패 침대) × 두 모드 — `_run_all_networks` 결과 JSON 전체 | 12 실행 · 실행마다 수 89–339 · 문자 · null 칸 전부 | **비트 같음** (더한 기록 키 넷만 빼고) · 증서 진단 키 (q_withheld …) 0 |
| N 생산자 | real_14 이온 `run_decomposition` × 두 모드 · 격자 둘 (cg 34×34×30 · spsolve 3×3×6) 의 G · q · solve_info | 4 | 비트 같음 (`G` `0x1.16d424c7fc346p+5` 등) |
| T τ 소비자 | 커밋된 v1.2 τ 원천 194 케이스 `case_row` (세대 1) | 9,894 칸 | 같음 |
| T τ 소비자 | 새 생산자 레코드 4 (ion_columns 50 칸 + 세대 계약 · 0b · 증서 결합) · 옛 생산자 `lhsx_054` 진단 레코드 (physics = `solver_guard` 그대로 — 사후 재분류 없음) | 5 | 같음 |
| R 배포 | v1.2 인계표 lhs 130 × 251 · lhsx 64 × 253 — 칸마다 빈칸 뜻 · 관통 분류 · 상태 집계 · 주 타깃 관문 | 48,822 칸 | 같음 · 관문 [] |
| W 웹앱 | `transform_network_summary_4col` 새 표 — 정상 · 비관통 (BASE 트리 ↔ 고친 트리 · 따로 프로세스) | 2 | 같음 |
| W 웹앱 (의도 변경) | 기존 두 열 CSV 표 (정상 · 비관통) · Hertz 만 있는 옛 케이스 (두 경로) · 모형 한계 (두 경로) | 6 쌍 · 34 행 | Physics · Δ 칸만 바뀜 (Hertz 복사 · Δ 0 % → 실제 Physics 값 · 또는 `—` + 사유) · 행 · 이름 · Hertz 칸 불변 |

- 메타 (따로): 더한 기록 키 넷 (`electronic_sigma_full_status` · `_reason` · `thermal_…`) — 정상 = computed / None · 비관통 = valid_zero / no_through_path · case15 = not_computed / boundary_overlap (Hertz 전자 · 열) · BASE 결과에는 없음.

## 4. 코드 신원 (재봉인 아님 · 보고)

| 항목 | 기준 (`0c557e72a`) | 고친 트리 |
|---|---|---|
| CODE_FILES 32 `code_fp` | `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` | **`acc7bfa335ec8fa8a7b76eb981135f16994b084ce0746476c5d05f61488af2ed`** |
| `scripts/network_conductivity.py` sha256 | `da9ecfefd8dc4b84…` | `5bb703dbd8242938862708920f82e1e25704e905cb0b7b4e561d4688ba6cd73e` |
| `scripts/tau_flux.py` sha256 | `eb9388ec8bd2d40b…` | `679967215b10fd20c15e33647e4185a8fb86cf510fff8789aad219ec13368d8d` |
| `webapp/app.py` sha256 | `bd4c25e507e3c7a2…` | `1664590ea55e3ebf120be4d92cd5630c691c78f52648704f38f2f1fd9970ddd9` |
| `webapp/pipeline_service.py` sha256 | `33a700300e8c650c…` | `9fe9d01794a2ecd8c12245af4469e13f1ce2d9561d92693b2f343208e72a2da4` |
| HANDOVER `scripts/lhs_design_dataset.py` sha256 | `ed8944dc2507a648…` | `ff6af63cc11f3270c430f970e2c2ef599b23afd45db2e99a4bf3c190679dca5d` |
| HANDOVER `scripts/g2_network_reread.py` sha256 | `1487ea0116aee5f6…` | `0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8` |

- 실행기 `code_fp(code_hashes())` (증거 `code_fp_report.py` · `code_fp_report.log`) · 봉인 목록 · 전이 닫힘 · 지연 import 분류 = 무변경 (새 import 없음 — `tau_flux` 는 기존 `_nc_mod` 로 생산자 판정을 부른다 · `pipeline_service` 는 기존 `_scripts_import` 로 tau_flux).

## 5. 설계 선택 — 판정해 달라 (계획과 다르거나 계획이 정하지 않은 것)

1. **무효 기하 우선** — 비관통 침대라도 기하가 무효면 `invalid_geometry` (옛: 비관통이면 valid_zero no_through_path) — "무효 입력을 증명된 0 으로 읽지 않는다".
2. **q 재구성 허용** — 솔버와 같은 식 · 순서 ((I_b/ΔV)·T)/A 와 상대 16ε (저장 원 값 · JSON 왕복 비트 보존이라 실제로는 0 차) · 재구성 q 와 기록 q **둘 다** 엄격 > 1.5 · 판정문 값 (g_to_q 곱 · 3 ulp 차) 도 허용 안에 든다.
3. **Σg 를 증서에** — 병렬 상한 0 < G ≤ 1.1·Σg 를 소비자가 다시 보려고 `sum_g` 를 싣는다 (새 진단 키 · 정상 증서에는 없음).
4. **H0 모형 한계 = 게시 + 배포 HOLD** — 정지 계약은 H0 모형 한계 레코드도 done 으로 게시하고 (진단 레코드 · τ 세 모드 NOT_COMPUTED · 인계표 행 유지) 배포 빌더가 실제 v1.3 을 거부한다 (진단 · dry-run 은 경고) — 게시 단계에서 막는 편이 맞나.
5. **관통 분류** — H0 모형 한계 행의 `ion_net_percolates` = 1 (그래프 관통 · 값만 미제공 · 배포는 HOLD).
6. **K2 위임** — 공용 판정 (0b) 을 못 넘은 모형 한계 주장 (위조 q_withheld ×1.01) 은 K2 (세대 계약 · 증서 결합) 가 아니라 K4 (정지 계약 다시) · K6 이 잡는다 — G2RR-02 이후 설계 (`certificate_binding_problems` 가 0b 실패 레코드를 그 검사에 맡김) 를 그대로 따랐다.
   ⚠ 시험 기대를 고친 자리: 체인 ⑤f2 의 기대 {K2 · K4} → {K4 · K6} (첫 고친 실행 뒤 · 결과는 같은 거부) · v1.3 V2b 닫힌 어휘에 `NA_MODEL_LIMIT` — 둘 다 시험 먼저 커밋에 넣고 고치기 전 코드에서 다시 쟀다 (§2 표).
7. **띠 폴백 우선** — τ 에서 L1 · L2 띠 폴백 + 모형 한계 = `BAND_FALLBACK` (앞 게이트 우선 · K6 도 BAND_FALLBACK 을 받는다).
8. **웹앱 표시 변경 범위** — strict missing 이 모형 한계뿐 아니라 Physics 가 없는 옛 케이스 · 기존 두 열 CSV 망 절의 정상 케이스 (Physics 값이 있는데 Hertz 복사로 보이던 것) 도 바꾼다 (§3 W 의도 변경).
9. **`non_finite` 사유** — 극단 기하 곱 넘침의 비유한 q 를 기술 실패 사유로 `NOT_COMPUTED_SOLVE_REASONS` 에 더했다 (옛: FULL = over_conduction_guard · CF = 값 ∞ 유지).
10. **재적합 · 상태 집계** — 주 타깃 모형 한계 행의 재적합 제외 사유 `NOT_COMPUTED:full_over_conduction` · README 상태 집계 별도 줄 (실제 배포에서는 HOLD 라 진단 묶음에서만 보인다).

## 6. 범위 밖 · 남은 것

- B6 등록 개정 = **초안** (두 등록 §9-8 · §9-3 · ⬜ 1저자 비준) — 범주 · 공용 판정 · 예외 범위 · 공란 의미 · Hertz 주 타깃 · 결과 열람 뒤 개정 이력 · 바꾸지 않는 것 (문턱 1.5 · 허용치 · ID 집합 · 원 입력).
- B7 새 승인 핀 (fast16 · real4 · 전체 사전 점검 로그 + 완료 영수증 · §2 손 대조 · 1저자 발사 승인) · C8 194 + 20 전부 새 실행 · C9 인계 · 배포 실물 — 이 요청 밖 (판정문 §4 B · C 그대로).
- A5 옛 13 건 = unknown (Q3 (가)) · 10-14 ROOT · 실패 기록 보존 · 옛 14 건 사후 전환 없음 (A4 T 의 lhsx_054 옛 레코드 = 그대로 차단).
- 물리 근거 가드 (q ≤ φ 계열) = v1.3 뒤 다음 세대 등록 (Q5 (가)) · S3 재봉인 = 별개 HOLD.

## 7. 질문

- **Q1.** `L214-01` (판정문 §2 최소 ①–⑤) · `L214-02` (명시 분리 · 결합 전부 · 공용 판정 · 소비 경로 표 · 전자 · 열 전파) · `L214-03` (strict missing · 새 표 / 기존 표 · 이온 / 전자 · 원 / 병합) 이 이 수정으로 닫히나.
- **Q2.** §5 의 1–10 중 바꿔야 할 것 — 특히 4 (H0 모형 한계를 게시할지) · 6 (K2 위임) · 8 (옛 케이스 표시 변경 범위).
- **Q3.** A4 (§3) 가 판정문 §4 A4 "같은 환경 정상 사례 타깃 수치 비트 동일 · 메타 · 사유 변경 따로" 의 증거로 충분한가 — 빠진 대조가 있나.
- **Q4.** 두 등록 개정 초안 (§9-8 · §9-3) 이 판정문 §4 B6 (코드 해시 · 결과 자격 · 공란 의미 · 예외 범위 · Hertz 주 타깃 · 결과 열람 뒤 이력 · 바꾸지 않는 것) 을 다 담나.
- **Q5.** 새 결함이 있나 — 있으면 등급 · 반례.
- **Q6.** ★ (나′) 대기 지문 선언 (도구는 발사 대조를 등록 값만으로 · 시험만 선언된 대기 상태를 정확한 실패 집합으로 받는다) 이 맞나 · 빠진 반례가 있나 (§9).

## 8. 재현 (리뷰 핀 · 컨테이너 Linux · Python 3.11)

```bash
git diff 0c557e72a <리뷰 핀> --stat -- scripts/ webapp/                      # 수정 8 파일 + 시험 다섯 + a4 · code_fp 도구 (docs/)
OMP_NUM_THREADS=1 python3 scripts/test_lhs214_model_limit.py --selftest      # 55/55
OMP_NUM_THREADS=1 python3 webapp/test_network_handover_chain.py              # 34/34
OMP_NUM_THREADS=1 python3 scripts/test_network_solve_certificate.py          # 28/28 (~70 s)
OMP_NUM_THREADS=1 python3 scripts/test_lhs_release_v13.py                    # 256 PASS (~130 s)
OMP_NUM_THREADS=1 python3 scripts/test_tau_flux.py                           # 55/55
OMP_NUM_THREADS=1 python3 scripts/g2_network_reread.py --selftest           # 전부 통과
OMP_NUM_THREADS=1 python3 scripts/run_network_194_parallel.py --selftest     # 139/139 (~2–3 분)
OMP_NUM_THREADS=1 python3 scripts/wsl_network_smoke.py --selftest-real       # 4/4 (case15 · ~2.5 분)
OMP_NUM_THREADS=1 python3 docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py --base 0c557e72a   # A4 PASS 32/32 (~4 분)
python3 docs/reviews/lhs214_fix_evidence_20261015/code_fp_report.py --base 0c557e72a                    # code_fp acc7bfa3… · 바뀐 봉인 파일 4
OMP_NUM_THREADS=1 python3 scripts/supp20_input_receipt.py --selftest         # ★ (나′) 99/99 · 상태 pending (~17 s · §9)
# 시험 먼저 확인 (고치기 전 코드 + 새 시험): 시험 먼저 커밋을 체크아웃해 위 다섯 시험 → §2 표의 "고치기 전" (13/54 · 21/34 · 27/28 · 255/256 · 284/284)
# ★ (나′) 시험 먼저 커밋 545d7d4fe 를 체크아웃해 영수증 selftest → 81/99 (상태 undeclared · 고치기 전 도구 + 옛 초안 꼴 등록 문서)
```

## 9. 봉인 지문 대기 선언 (1저자 10-15 Q1 (나′))

- **무엇이 실패했나** — 본 가지에 합친 게이트에서 `scripts/supp20_input_receipt.py --selftest` 가 실패했다.  수정이 봉인 32 의 네 파일을 바꿔 체크아웃 지문 = `acc7bfa3…` (§4) 인데,
  보충 20 등록 초안 §9-3 표가 새 지문을 등록 값과 **같은 꼴** (`` `code_fp <hex>` ``) 로 적었다 → 도구 `registration_values()` 가 값 둘을 보고 등록 §3 = None → R0 · D1 실패 ·
  시험 S0 (커밋된 실물 = rc 0 기대) 실패 · S0b 는 None 에서 AttributeError (시험 코드 결함).
- **결정 (나′)** — 새 지문은 등록 초안에 **대기 지문** 으로 따로 선언한다 (`` `code_fp_pending <64 hex>` `` · 194 §9-8 · 보충 20 §9-3 표 · "비준 · 재등록 때 §3 이 이 값으로 바뀌고
  이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로").  발사 대조 (컨테이너 D1 · 사전 점검 E2 · 발사 manifest F5 · G5) = **등록 §3 값만** — 대기 선언이 통과시키지 않는다
  (비준 · 재등록 전 발사 불가 유지).  시험만 선언된 대기 상태를 **정확한 실패 집합** 으로 받는다.
- **도구** (봉인 32 · HANDOVER 밖 검사 도구 — code_fp 무관): `registration_values()` 에 선택 항목 `code_fp_pending` (정규식 `` `code_fp_pending ([0-9a-f]{64})` `` · 0 개 = None · 문제 아님 ·
  서로 다른 값 둘 이상 = R0 문제 · 등록 §3 과 같음 = 모순 = R0 문제 · 문제면 값 None) · D1 판정식 그대로 (체크아웃 = 등록 §3) · D1 상세에 `pending` 만 더함 · E2 · F5 · G5 · 그 밖 동작 무변경.
  등록 문서의 `code_fp` 를 읽는 코드 = 이 도구뿐 (리포 grep · 194 쪽 §3 대조 = 손 대조).
- **시험** (selftest 만 · 시험 먼저 `545d7d4fe`):
  - 상태 판정 (selftest 안 · 작은 함수): registered (체크아웃 = 등록 §3) · pending (대기 선언 하나 · 체크아웃 = 대기 ≠ 등록) · undeclared (그 밖 = 시험 실패 · 사유 출력).
  - 양성 대조의 pending 기대 실패 집합 (정확히 같음 · ⊆ 아님) — 기록이 싣는 지문으로 정했다:
    컨테이너 S0 = {D1} (D1 상세 now = 대기 · registered = 등록 · pending = 대기) ·
    진짜 실행기 사전 점검 영수증 S7 · S7j = {D1 · E2} (영수증 = 체크아웃 지문 · E2 상세 receipt = 체크아웃 · registered = 등록 · P7 = 영수증 = 체크아웃이라 같음 · S7j 의 P10 같음) ·
    합성 발사 manifest 둘 S8 · S8k = {D1 · F5 · G5} (code_hashes = 이 체크아웃 → 봉인 = 체크아웃 지문 · F5 · G5 상세 = 봉인 · dirty false · H1 = 두 봉인이 같아 같음 · S8k 의 F7 · G7 같음).
    정확한 집합을 쓰는 음성 대조 (S7a · S7a2 · S7k1 · S7k2 · S8g2) = 원래 집합 ∪ 같은 pending 집합.
  - 음성 대조 판별력 (두 상태 모두 · 이미 실패 중인 칸으로 통과시키지 않는다): code_fp 오타 S4 = D1 상세 registered = 문서에서 읽은 오타 값 · now = 체크아웃 ·
    E2 · F5 를 겨눈 S7l · S8e · S8f = 상태가 registered 가 아니면 **비준 쌍둥이** (등록 문서 사본 — 등록 §3 := 체크아웃 지문 · 대기 선언 없음) 에서 판별 (쌍둥이의 정상 기록 = rc 0 · S11f · f2 · f3).
  - 새 반례 (등록 문서 사본 · 지문 토큰만 바꿈 · 모의 등록 값 = 체크아웃과 다름):
    ⓐ 옛 초안 꼴 (`` `code_fp <새 hex>` `` 둘째 값) = 정확히 {R0 · D1} · 상태 undeclared · 시험 충돌 없음 (S11a) ·
    ⓑ 대기 선언 값 둘 (서로 다름) = {R0} (S11b) · ⓒ 대기 = 등록 (모순) = {R0} (S11c) ·
    ⓓ 대기 선언 + 체크아웃 = 대기 = 상태 pending · 도구 D1 = 거짓 {D1} · 사전 점검 {D1 · E2} · 발사 {D1 · F5 · G5} (S11d · d2 · d3 — 발사 대조 엄격) ·
    ⓔ 대기 선언 없음 + 체크아웃 ≠ 등록 = undeclared {D1} · ⓔ′ 다른 코드의 대기 선언 = undeclared (S11e · e2) ·
    ⓕ 정상 비준 상태 (합성 — 대기 없음 · 체크아웃 = 등록) = rc 0 (컨테이너 · 사전 점검 · 발사 — S11f · f2 · f3).
  - S0b = None 안전 · 등록 §3 = `e8b2496b…` 그대로 · 대기 선언이 있으면 = `acc7bfa3…` (`code_fp_report.log` 의 고친 트리 값).
- **수** — 시험 먼저 (고치기 전 도구 + 옛 초안 꼴 등록 문서 · 상태 undeclared) **81/99** (FAIL 18 · 증거 `docs/reviews/lhs214_fix_evidence_20261015/before_napr/`) →
  고친 뒤 (상태 pending) **99/99** (`docs/reviews/lhs214_fix_evidence_20261015/final/scripts__supp20_input_receipt.py_selftest.log`).
- **바꾸지 않은 것** — 봉인 32 · HANDOVER 파일 (`6d0bec3c3` 그대로) · 등록 §2 · §3 값 (`code_fp e8b2496b…` 그대로 — 비준 · 재등록은 1저자) · 194 실행기 · 웹앱 (이 도구에 해당 화면 없음).
