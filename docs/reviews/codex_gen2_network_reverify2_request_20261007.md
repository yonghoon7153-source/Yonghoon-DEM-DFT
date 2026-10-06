# Codex 재검증 요청 2 — 접촉망 세대 2 (G2RR-01 · 02 · 03 + 재개방 G2R-02 · G2R-03 · SELF-91) · 새 실행 봉인 · 실덤프 사전 점검 (2026-10-07 새벽 KST)

- 직전 판정: `docs/reviews/codex_review_gen2_network_reverify_20261006.md` (핀 `165d0cf61` · **HOLD** · 기존 P1 G2R-01 닫힘 · 새 P1 없음 · 새 P2 G2RR-01 · 02 · 03) ·
  증거 `docs/reviews/codex_gen2_network_reverify_evidence_20261006/` (우리 트리 재현 `_reproduction_ours/` · ★ 고친 트리 재실행 `_rerun_fixed_c70b02c7b/` — 이 요청서와 같은 커밋).
- 1저자 비준 (10-06 밤 · *"권고대로"*): 판정문 §7 ①–⑤ + G2RR-03 + 문서 · 새 194 = Codex GO 뒤 (병렬 안 함) · v1.3 = GO 뒤 한 번에.
- 1저자 결정 (10-07 · *"권고대로해"*): G2RR-02 의 숫자를 싣는 CF · 협착-only 증서가 없거나 어긋나면 **레코드 전체 거부** 유지 (§4 — 수용 여부만 묻는다).
- 검토 대상 = 이 요청서를 담은 커밋 (브랜치 `claude/stoic-knuth-NObVQ` · 1저자가 발송 때 sha 를 적는다).  이 커밋 앞의 코드 커밋 = `c70b02c7b` (탐침 재실행 트리).

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 | 시험 (고치기 전 → 뒤 · 커밋 메시지 · 원장 note) |
|---|---|---|---|
| `e1dab4265` | G2RR-01 (G2R-02 잔여) | `pipeline_service.generation_stamp_values` (게시자가 도장에 쓰는 네 세대 값을 레코드에서 유도 · 게시 · 대조가 한 함수) · `provenance_generation_problem` (g2 = 네 키 전부 · 값 = 유도 기대값 (JSON 정규형 · 타입까지) = 세대 2 값 · inferred_legacy = 확인된 역사 도장 스키마 (194 v1.2 실측 194/194 · 8 키) 와 정확히 같을 때만) · 옛 두 도우미 삭제 · `load_tau_results(expected_generation=)` · CLI `--tau-batch-manifest` (manifest `expected_network_generation` — 선언 없음 · 모르는 값 = 거부) · 웹앱 망 세대 행 (어긋날 때만 경고) | `webapp/test_gen2_stamp_record.py` 옛 코드 6/23 → 23/23 · `lhs_design_dataset --selftest` 376 → 377 (옛 픽스처가 도장을 망 JSON 앞에서 찍어 all_null 모양이던 것 고침 — 옛 코드 + 새 픽스처 376/376) |
| `f3f720985` | G2RR-02 (G2R-03 잔여) | 생산자 = 증서마다 결합 정보 (`branch` · `channel` · `role` · `contact_mode` · `delta_V` · `geometry` · `g_to_q` · `sigma_bulk_S_cm` — 기록만 · σ 비트 동일) · 공용 검사 `tau_flux.certificate_binding_problems` (가지 · 채널 · 역할 · 전극 · contact_mode = 자리 · ΔV 1 · G→q = 기하 · 한 실행 = 한 기하 · q = I_bottom/ΔV × T/A = 저장 σ_ratio (반폭 5e-9) · σ_dim 저장 정밀도) — 정지 계약 ⑨ · 승격 전 기록 검사 · τ 소비자 · 인계 P4 가 같은 함수 · 정책 `CERT_BRANCH_POLICY` · 문서 Q3 (첫 단 예외 = 사다리 안 탐 · 250 k = 시도 상한 · 메모리 보증 아님 · 1e-6 = 수용 문턱) · Q4 (CF = 모형 내부 관계 · 출력 표지 `CONTACT_FREE (R_c=0)`) | `test_gen2_role_contract` 34/40 → 40/40 · `test_network_solve_certificate` 24/27 → 27/27 · `webapp/test_gen2_publication_handover` 13/18 → 18/18 · `webapp/test_pipeline_provenance` 픽스처 267/284 → 284/284 |
| `6ac3af87e` | G2RR-03 | 검산기 `reread_v12.py` `registration_queue()` — 큐를 dict 로 바꾸기 전에 검사 (비지 않은 목록 · 형식 · 194 행 · 중복 0 · 코호트 = 인계표) · 빈 큐에서도 집합 비교 · 인계표 코호트 대체 없음 | `scripts/test_reread_v12.py` 13 → 22 (새 9 사례가 옛 검산기에서 17 PASS · 5 FAIL) → 22/22 |
| `1651d3630` | G2RR-01 문구 | 인계 열 사전 `ion_net_generation` 의 낡은 문장 ("도장이 세대 2 게시를 말하면 추론하지 않는다") → 확인된 역사 도장 스키마 규칙 | `test_gen2_stamp_record` W5 23/24 → 24/24 |
| (이 커밋) | §7-3 · §7-4 · G2RR-01 실행기 쪽 | ① 194 실행기 `run_network_194_parallel.py`: manifest `expected_network_generation` (+ `seal` 안 사본) = 워커 체크아웃의 봉인 코드에서 **유도** (`derive_generation` — 생산자 `_run_all_networks` 를 망 CLI 기본값으로 21 구 사슬에 · 같은 체크아웃의 세대 계약 · `python -I -B` 하위 프로세스) · g2 · 문제 0 아니면 발사 안 함 · retry = 값 ≠ 봉인 사본 · 다시 유도한 세대 ≠ 값 → rc 2 (넘김 불가) · audit = 같은 대조 + done 케이스마다 레코드 세대 · 옛 manifest (선언 없음) = 그대로 읽음 ② 전이 의존 — `CODE_FILES` 19 → 29 (워커 망 정지 경로의 정적 import 닫힘 27 ⊆ 29 를 발사 사전 점검이 확인) ③ 입력 지문 `input_digest` (ID · 코호트 · 원자료 sha256) · audit 재계산 ④ 후속 명령 = `--tau-batch-manifest` · 다시 읽기 · v1.3 이름 ⑤ 새 도구 `scripts/g2_network_reread.py` (게시 다시 읽기 · 읽기 전용) ⑥ 스모크 `wsl_network_smoke.py` 에 case15 ⑦ 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` ⑧ 탐침 재실행 기록 | 실행기 `--selftest` 고치기 전 52 ✓ · 11 ✗ (새 ㉗–㉛ 만 — 예외로 끊긴 시나리오 줄 2 포함) → 66/66 · ㉜ (입력 지문) 추가 뒤 66 ✓ · 2 ✗ → **68/68** · `g2_network_reread --selftest` 9/9 (새 도구 — 양성 셋 · 음성 넷 · launcher-root 양성 · 음성) · `wsl_network_smoke --selftest` 11/11 (커밋 뒤 깨끗한 트리 · 새 줄 = 참조 침대 두기 real14 · case15 sha256 = README · 상 매핑 · 음성 대조 C1 · C1b · C2 · C3 PASS) |

## 2. Codex 탐침 다섯 — 무변경 사본 재실행 (고친 트리 `c70b02c7b` · 이 커밋은 탐침이 import 하는 모듈을 바꾸지 않는다)

전부 `docs/reviews/codex_gen2_network_reverify_evidence_20261006/_rerun_fixed_c70b02c7b/README.md` (방법 · 환경) · 같은 폴더의 비교 표 (`compare_codex_vs_ours.md`) · 게시 거부 사유 원문 (`attempt_reasons.out`) 에 있다.  요약:

| 탐침 · 변이 | Codex 보존 증거 (고치기 전) | 고친 트리 |
|---|---|---|
| acceptance 게시 baseline | done · q 0.00400538 · I_bottom 0.0200268809166404 | 같음 · τ2 hertz 10.980805104698454 OK |
| full_cert_from_cf | **done** | **failed** — 정지 계약 ⑨: `가지 'bulk_only' ≠ 자리 'full'` · 재구성 q 0.039269908169872456 ≠ 발행 0.00400538 · σ_dim 0.11780972450961737 ≠ 0.012016 |
| full_cert_from_h12 | **done** | **failed** — `역할 'H12' ≠ 'H0'` · 재구성 q 0.005135024463592675 · σ_dim 0.015405073390778025 |
| missing_full_cert | failed | failed (`solve_certificate_full: 증서 없음`) |
| missing_cf_cert · cf_bad_conservation · missing_constr_cert | done (판정문 §3 Q4 — 계약이 FULL 에만) | **failed** — `solve_certificate_bulk_net: 증서 없음` · `전류 보존 실패 — \|I_b + I_t\| / max = 1 > 1e-06` · `solve_certificate_constr_net: 증서 없음` (§4 결정) |
| 도장 all_unknown · all_null · g2_declares_legacy | **인계 통과 g2** | **인계 거부** τ P4 (G2RR-01) — `도장 psi_placement_physics=… ≠ 레코드에서 유도한 'multiply'` … |
| 도장 one_null_legacy_shape | **통과 inferred_legacy** | **거부** — `확인된 역사 도장 스키마 (194 v1.2 · 8 키) 가 아니다 — 남는 키 ['electrode_model']` |
| 도장 control · stamp_absent_keys | 통과 g2 · 거부 | 같음 |
| reread_extra queue_empty · plan_absent · queue_duplicate | **rc 0 PASS** (queue_n 0 · 0 · 194) | **rc 1 FAIL** (queue_n 0 · 0 · 195 · 고유 0 · 0 · 194) · baseline rc 0 PASS 194 |
| adversarial (회귀) | 막다른 간선 1e14 → certificate_failed → spsolve_fallback 15000.5 · 직렬 1e16 거부 · zero_Rc None · 옛 세대 변이 8 NOT_COMPUTED + ⑨ | 같은 판정 · 같은 방법 (1e8 G 끝자리만 — 상대 9.9e-13) |
| numerics (회귀 · 참 G 1.45) | 최악 상대오차 1.6442660633053663e-07 | G 13/13 비트 동일 · 같은 방법 · 증서 문제 None |
| real_beds (회귀) | real14 · case15 × 4 팔 × 3 가지 | None 모양 · clamp · floor · 관통 Rc=0 수 같음 · 값 상대차 real14 ≤ 6.11e-15 · case15 ≤ 4.22e-09 (플랫폼 차 — 이전 우리 재현과 같은 크기) |

- 탐침 기록의 `stop` 칸 (게시 실패 변이의 `① … 파일 없음`) 은 탐침이 게시 **뒤** 폴더에 정지 판정을 다시 부른 값이다 (후보가 활성 세대가 되지 않아 모드 파일이 없다) — 거부 사유는 `attempt_reasons.out`.
- `verify_evidence.py` 는 돌리지 않았다 — 고치기 전 반례 재현을 PASS 로 세는 스크립트다 (Codex README).
- 회귀 진입점 (Codex `run_tests.py` 의 14 + `test_gen2_stamp_record`) 이 워크트리 재실행: §6 표.

## 3. 판정 §7 해제 목록 대응

| 항목 | 상태 · 근거 |
|---|---|
| ① G2RR-01 도장 ↔ 레코드 | ✅ `e1dab4265` · `1651d3630` — 탐침 도장 변이 다섯 거부 · control 통과 (§2) · 진짜 역사 194 = 194/194 inferred_legacy (`test_gen2_stamp_record` H4) · **새 배치 manifest 기대 세대 = 이 커밋의 실행기가 쓴다** (실행기 ㉗ — 인계 생성기 `tau_manifest_expected_generation` 이 그 값을 읽는다) |
| ② G2RR-02 증서 ↔ 가지 · 역할 · 발행값 | ✅ `f3f720985` — CF → FULL · H12 → H0 거부 (사유 = 가지 · 역할 + 재구성 q · σ_dim) · 숫자를 싣는 CF · 협착-only 증서 결손 · 보존 실패 = 레코드 거부 (§4 결정) · 해 없는 가지는 증서 요구 없음 (비관통 · GEN2-01 양성 — 다시 읽기 selftest · `test_gen2_publication_handover` ⑤) |
| ③ 새 실행 봉인 | ✅ 초안 (`docs/reviews/lhs_network_batch_registration_20261007_g2.md` · 발사 = GO 뒤) — 새 ROOT · ID · 코호트 · 원자료 sha256 지문 (194 · `a04282d7…` · `da7c93f9…` · manifest `input_digest` · audit 재계산 ㉜) · 전이 의존 29 (닫힘 27 ⊆ 29 · ㉚) · 기대 세대 `g2` (유도 · retry 넘김 불가 · audit 케이스별 ㉗–㉙) · 기대 조합 · 증서 문턱 · 실패 정책 = 봉인 파일 안 상수 (`tau_flux.G2_MODE_CONTRACT` · `CERT_BRANCH_POLICY` · `network_conductivity.DIRICHLET_*_REL_MAX`) — 코드 봉인이 고정하고 실행기는 다시 선언하지 않는다 · S3 재봉인 = 열림 (§5) |
| ④ 실덤프 사전 점검 | ⬜ 명령 등록 (등록 문서 §1) · **1저자 WSL 진행 (이 리뷰와 병렬)** — real14 · case15 = 스모크 (실제 `run_pipeline(stop_after='network')` → 게시 → 다시 읽기 K1–K7 · H1) · LHS 셋 (관통 bimodal `lhs00_055` · 정상 비관통 `lhs00_128` · `lhsx_007`) = 스모크 + **실행기 시범** (진짜 배치 기록 · manifest 기대 세대 · audit · 다시 읽기 M0–M2 · H1).  결과는 등록 문서 §9 덧붙임 · 이 요청서 보충으로 |
| ⑤ 구멍의 음성 대조 | 아래 표 |
| G2RR-03 (별건 검산기) | ✅ `6ac3af87e` — 탐침 셋 rc 1 · 정상 rc 0 (§2) |

**⑤ 어디에서 멈추나** (변이 → 멈춤 자리 · 시험):

| 변이 | 멈춤 자리 | 시험 |
|---|---|---|
| H12 를 주 Hertz 자리에 (G2R-01) | 게시 전 (정지 ⑨ · 일반 경로 기록 검사) · 강제 폴더 = 인계 P4 | `webapp/test_gen2_publication_handover` (판정문 §1 verified) |
| 도장 네 값 unknown · null · legacy · 한 키 결손 · 타입 · 역사 스키마 밖 | 인계 P4 · 웹앱 망 세대 행 경고 · 다시 읽기 K3 · H1 | `test_gen2_stamp_record` S1–S4 · H2 · H3 · W2 · `g2_network_reread --selftest` (all_null) |
| 증서: CF → FULL · H12 ↔ H0 · physics · 채널 · g_to_q · 판 높이 · ΔV · 숫자만 · CF 숫자만 · CF 보존 · CF / 협착 증서 삭제 · CF 상태 모순 · 결합 키 없음 | 정지 ⑨ · 승격 전 기록 검사 · τ 소비자 NOT_COMPUTED · 인계 P4 · 다시 읽기 K2 · H1 | `test_gen2_role_contract` Y · `test_gen2_publication_handover` ⑤ · 탐침 acceptance (§2) · `g2_network_reread --selftest` (CF → FULL) |
| manifest 기대 세대 선언 없음 · 모르는 값 · 레코드와 다름 | 인계 (`tau_manifest_expected_generation` · P4) · 다시 읽기 M0 · H1 | `test_gen2_stamp_record` M1–M4 · `g2_network_reread --selftest` |
| manifest 기대 세대 변조 (값 · 봉인 사본 · 삭제) · 코드가 다른 세대를 냄 | 실행기 retry rc 2 (넘김 불가) · audit rc 1 | 실행기 ㉘ |
| 케이스 레코드 세대 ≠ 선언 (옛 모양 dual) | 실행기 audit rc 1 | 실행기 ㉘ |
| 봉인 모듈에 새 import (봉인 밖 의존) | 발사 사전 점검 중단 | 실행기 ㉚ |
| 발사 뒤 수확 JSON 원자료 sha 변경 | 실행기 audit rc 1 | 실행기 ㉜ |
| 양성: 정상 관통 · 진짜 비관통 (세 모드 valid_zero · NOT_PERCOLATING) · GEN2-01 (physics · H12 협착-only not_computed · FULL · CF 게시) | 게시 done · 다시 읽기 K1–K7 · H1 통과 | `g2_network_reread --selftest` 양성 셋 · `test_gen2_publication_handover` ⑤ 양성 (비관통 · GEN2-01) |
| ⬜ 양성: 한 진단 가지만 정직하게 풀이 실패 (그 가지 not_computed + 사유 · FULL 게시) | 계약 규칙만 (`_cert_unpublished_problem` — 숫자 없음 · 해 주장 없음 · 사유 일치) | **실 생산자 사례 시험 없음** — 그런 침대를 만들지 못했다 |

## 4. 1저자 결정 — G2RR-02 의 진단 가지 정책 (수용 여부만 묻는다)

- 판정문 §3 Q4: *"해당 가지 증서 실패는 그 진단 가지의 NOT_COMPUTED 와 사유로 처리한다.  정상 FULL 까지 자동으로 폐기할 필요는 없다."*
- 1저자 결정 (10-07 · *"권고대로해"*): **숫자가 실린 CF · 협착-only 가지의 증서가 없거나 결합이 어긋나면 레코드 전체를 거부한다 (fail-closed · 지금 구현 그대로).**
  사유: 생산자는 증서를 못 넘은 가지에 숫자를 싣지 않는다 (그 가지만 `not_computed` + 사유 · FULL 유지 — 정직한 개별 풀이 실패는 "숫자 없는 가지" 규칙으로 통과) ⇒
  숫자가 실렸는데 증서가 없거나 바뀐 경우는 증서 결손 · 바꿔치기 (레코드 조립 · 편집 모순) 일 때만 생긴다 — 판정문 §6 의 "모드 정체성 자체의 모순" 부류로 보아 그 레코드의 다른 숫자도 받지 않는다.
- 질문: 이 정책을 받아들이는가 (가지별 보류 대신).  ⚠ 위 ⑤ 마지막 줄 — 정직한 한 가지 실패의 **실 생산자 양성 대조는 없다** (계약 규칙 수준만).

## 5. 남는 것 · 알려진 부작용 (숨기지 않음)

- **S3 재봉인 필요** — `scripts/network_conductivity.py` sha256 `61f00fef…` → `da9ecfef…` (`f3f720985`) · S3 의 `seal_s3_prerun.NUMERIC_MODULES` (넷) 에는 `lens_geometry.py` 가 없다
  (`plastic_coverage.py:1144` 가 모듈 수준에서 `intersection_disc_area` 를 import — physics g2 원판 floor) — 194 실행기는 이번에 봉인했다 (10-05 판 19 파일에도 없었다 · 그 파일은 `11fcf91e8` 뒤 바뀌지 않았다).
- **G2RR-02 이전 세대 2 웹앱 케이스** (`05977e94a` – `70a6d91a4` 코드로 계산) = 증서 결합 키가 없어 숫자 게시 가지에서 거부 → 망 재계산 전 τ NOT_COMPUTED (194 배치와 무관 · 지운 것과 옛 것을 구별할 수 없어 받지 않는다).
- **`webapp/app.py` 는 봉인 파일** — 망과 무관한 화면 라우트 커밋 (`761e32645` · `92839aeb7` — 3D 뷰어) 도 지문을 바꾼다.  194 봉인 표 (등록 §3) 는 이 커밋의 app.py 기준 · 발사 뒤 그 체크아웃에서 app.py 를 고치면 retry 가 거부한다.
- **옛 ROOT retry** — 이 실행기로 194 v1.2 ROOT (19 파일 봉인 · 기대 세대 선언 없음) 를 retry 하면 봉인 집합이 달라 거부된다 (감사는 그대로 읽는다 — 실행기 ㉙).
- **실행기의 세대 유도 = 표기 계약** — 21 구 사슬 탐침이 내는 레코드의 세대 계약 판정이다 (값의 물리 정확성 아님).  manifest · 도장 · 레코드 · 모든 사본을 한 실행 안에서 일관되게 함께 바꾼 전면 위조는 재계산 없이 못 잡는다 (`TAU_SAME_GEN_BASIS` · 판정문 §3 "보증 아님").
- **다시 읽기 도구의 H1 (smoke · case-dir)** = 그 폴더에서 만든 한 케이스 배치 기록으로 부른다 — P1 · P3 은 자기 대조가 된다 (도구 표지 `synth_batch`).  진짜 배치 기록 대조는 launcher-root (시범 · 194).
- **전이 의존 닫힘 = 정적** (모듈 수준 import + 적어 둔 경로 위 지연 import 다섯) — 함수 안 import 를 새로 경로에 넣으면 그 줄을 `DEP_LAZY` 에 적어야 잡힌다.  app.py 의 화면 라우트 지연 import (뷰어 · 믹서 등) 는 망 정지 경로가 아니라 닫힘 밖이다.
- **SELF-91 (정오표)** — 직전 요청서 §4 결정 8 의 "real14 · case15 … 2,607" 은 real14 전체 망 clamp 수다 · 관통 풀이 대상 Rc=0 = real14 2,628 · case15 312 (탐침 재실행도 같은 수 · §2).
- 회귀 진입점 재실행 = 이 워크트리 (커밋 전 · 코드 변경 = 실행기 · 스모크 · 새 도구 · check_all.sh 만) — §6.  전체 `check_all.sh` 는 돌리지 않았다 (메인 세션 게이트 몫).

## 6. 회귀 진입점 재실행 (이 워크트리 · Codex `run_tests.py` 의 14 + `test_gen2_stamp_record`)

워크트리 (HEAD `c70b02c7b` + 이 커밋의 작업트리 변경 — 실행기 · 스모크 · 새 도구 · check_all.sh · 문서만) 에서 하나씩 · cwd = 리포 · PYTHONPATH = scripts · webapp ·
단일 스레드 BLAS · PYTHONDONTWRITEBYTECODE · git 객체 있음 (Codex 묶음의 SKIP 3 = 옛 모듈 `git show` 대조가 여기서는 돈다).  Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1.

| 진입점 | Codex (핀 165d0cf61) | 이 워크트리 |
|---|---|---|
| `scripts/test_gen2_role_contract.py` | 32/32 | 40/40 (rc 0) |
| `scripts/test_network_solve_certificate.py` | 20/20 · 3 SKIP | 27/27 (rc 0) |
| `webapp/test_gen2_publication_handover.py` | 12/12 | 18/18 (rc 0) |
| `webapp/test_tau_handover_status.py` | 41/41 | 41/41 (rc 0) |
| `scripts/lhs_release_build.py --selftest` | 29/29 | 31/31 (rc 0) |
| `scripts/test_reread_v12.py` | 13/13 | 22 PASS · 0 FAIL (rc 0) |
| `scripts/test_physics_area_g2.py` | 27/27 | 27/27 (rc 0) |
| `scripts/test_network_dirichlet.py` | 14/14 | 14/14 (rc 0) |
| `scripts/test_network_generation2.py` | 18/18 | 18/18 (rc 0) |
| `scripts/test_psi_default_switch.py` | 21/21 | 21/21 (rc 0) |
| `scripts/test_tau_flux.py` | 55/55 | 55/55 (rc 0) |
| `scripts/test_constriction_power_share.py` | 17/17 | 17/17 (rc 0) |
| `webapp/test_psi_generation_stamp.py` | 18/18 | 18/18 (rc 0) |
| `webapp/test_pipeline_provenance.py` | 281/281 | 284/284 (rc 0) |
| `webapp/test_gen2_stamp_record.py` (새 · G2RR-01) | — | 24/24 (rc 0) |
| 합계 | 598 통과 · 3 SKIP (14 진입점) | **657 통과 · 실패 0 (15 진입점 · rc 0 × 15)** — `test_network_solve_certificate` 전체 출력을 다시 받아 'skip' 0 건 확인 |

- 이 커밋의 새 · 바뀐 도구: 실행기 `--selftest` 68/68 · `g2_network_reread --selftest` 9/9 (둘 다 위 표 밖).

## 7. 질문

1. G2RR-01 · 02 · 03 이 닫히는가 (범위 포함).  G2R-02 (닫는 조건 = G2RR-01 + 새 배치 manifest 기대 세대 봉인) · G2R-03 (닫는 조건 = G2RR-02) 이 닫히는가.
2. §4 1저자 결정 (숫자를 싣는 CF · 협착-only 증서 결손 · 불일치 = 레코드 전체 거부) 을 받아들이는가.
3. 새 실행 봉인 (등록 문서 §2 · §3 + 실행기 ⓕ ⓖ ⓗ) 이 §7-3 을 채우는가 — 특히 (a) 기대 세대를 **유도**하는 방식 (21 구 사슬 탐침 · 같은 체크아웃의 계약) (b) 전이 의존을 정적 닫힘 + 적어 둔 지연 import 로 재는 것 (c) 계약 상수를 실행기가 다시 선언하지 않고 코드 봉인에 맡기는 것.
4. §7-4 사전 점검 설계 (real14 · case15 = 스모크의 실제 `run_pipeline` 경로 · LHS 셋 = 실행기 시범) 가 충분한가 — real14 · case15 는 LHS 코호트가 아니라 194 실행기에 넣을 수 없다.
5. 새 194 를 발사하기 전에 더 막아야 할 것이 있는가 (S3 재봉인을 194 앞에 둘지 포함).
