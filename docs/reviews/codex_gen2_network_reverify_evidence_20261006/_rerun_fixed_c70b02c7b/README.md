# 고친 트리 재실행 — Codex 세대 2 재검증 탐침 (c70b02c7b · 2026-10-07 새벽 KST)

판정문 `docs/reviews/codex_review_gen2_network_reverify_20261006.md` 의 `probes/*.py` 다섯 개를 **무변경 사본**으로 고친 트리에서 다시 돌린 출력이다.
고친 커밋: G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` · G2RR-03 `6ac3af87e` · 열 사전 문구 `1651d3630` (전부 `c70b02c7b` 의 조상).

## 재현 방법

- `source/` = `git archive c70b02c7b` 전체 (6,937 파일) · `probes/` = 이 증거 폴더의 `probes/*.py` 바이트 사본 · `evidence/` · `tmp/` 빈 폴더 — 조립 = `tools/make_bundle.py`.
- 실행 = `tools/run_isolated.py` (`python3 -I -B` · 사용자 site 경로 하나만 명시 — 이 기계는 dateutil · requests 가 거기 있다 · 탐침은 `runpy` 로 자기 `__file__` 기준 묶음 뿌리를 그대로 쓴다 ·
  하위 프로세스 env = PYTHONDONTWRITEBYTECODE · 단일 스레드 BLAS · cwd = 빈 스크래치 폴더).  순서: acceptance → reread_extra → adversarial → numerics → real_beds.
- 비교 = `tools/compare.py <Codex evidence/> <우리 evidence/> real` → `compare_codex_vs_ours.md` · 게시 거부 사유 = `tools/attempt_reasons.py` (각 변이 폴더의 `network_attempt.json`) → `attempt_reasons.out`.
- 환경: Linux x86_64 · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · NetworkX 3.6.1 (이전 우리 재현 `docs/reviews/codex_gen2_network_reverify_evidence_20261006/_reproduction_ours/README.md` §4 와 같은 컨테이너 종류).
- ⚠ 이 커밋 (재검증 요청서를 담은 커밋) 이 바꾸는 코드 파일 = `scripts/run_network_194_parallel.py` · `scripts/wsl_network_smoke.py` · `scripts/g2_network_reread.py` (새) · `scripts/check_all.sh` —
  탐침이 import · 실행하는 모듈 (`app` · `pipeline_service` · `tau_flux` · `network_conductivity` · `lhs_design_dataset` · `lhs_webapp_batch` · `test_pipeline_provenance` ·
  `test_gen2_publication_handover` · `reread_v12.py`) 은 아니다 ⇒ 이 출력은 요청서 커밋의 그 모듈과 같은 바이트에서 나왔다.

## 결과 (Codex 보존 증거 ↔ 고친 트리)

| 탐침 | Codex (핀 165d0cf61 · 고치기 전) | 고친 트리 (c70b02c7b) |
|---|---|---|
| acceptance 게시 baseline | done · q 0.00400538 · I_bottom 0.0200268809166404 | **같음** (done · 같은 q · 같은 I_bottom · τ2 hertz 10.980805104698454 OK) |
| acceptance missing_full_cert | failed | failed — 사유 `solve_certificate_full: 증서 없음` |
| acceptance full_cert_from_cf | **done** (I_bottom 0.1963495408493623) | **failed** — `가지 'bulk_only' ≠ 자리 'full'` · 재구성 q 0.039269908169872456 ≠ 발행 0.00400538 · σ_dim 재구성 0.11780972450961737 ≠ 0.012016 |
| acceptance full_cert_from_h12 | **done** (I_bottom 0.025675122317963317) | **failed** — `역할 'H12' ≠ 'H0'` · 재구성 q 0.005135024463592675 · σ_dim 0.015405073390778025 |
| acceptance missing_cf_cert | done | **failed** — `solve_certificate_bulk_net: 증서 없음` (숫자를 싣는 CF 가지 · 1저자 결정 = 레코드 전체 거부) |
| acceptance cf_bad_conservation | done | **failed** — `solve_certificate_bulk_net: 전류 보존 실패 — \|I_b + I_t\| / max = 1 > 1e-06` |
| acceptance missing_constr_cert | done | **failed** — `solve_certificate_constr_net: 증서 없음` (이 합성 침대의 Hertz 협착-only 는 숫자 있음) |
| acceptance 도장 control | 통과 g2 | 통과 g2 |
| acceptance 도장 all_unknown · all_null · g2_declares_legacy | **통과 g2** | **거부** — τ P4 세대 도장 대조 (G2RR-01) · 첫 사유 = `도장 psi_placement_physics=… ≠ 레코드에서 유도한 'multiply'` |
| acceptance 도장 one_null_legacy_shape | **통과 inferred_legacy** | **거부** — `확인된 역사 도장 스키마 (194 v1.2 · 8 키) 가 아니다 — 남는 키 ['electrode_model']` |
| acceptance 도장 stamp_absent_keys | 거부 | 거부 — `도장에 psi_placement_physics 없음 (부분 결손)` … |
| reread_extra baseline | rc 0 PASS queue_n 194 | rc 0 PASS queue_n 194 (고유 194) |
| reread_extra queue_empty · plan_absent · queue_duplicate | **rc 0 PASS** (queue_n 0 · 0 · 194) | **rc 1 FAIL** (queue_n 0 · 0 · 195 · 고유 0 · 0 · 194) — C8 사유 `plan.queue 가 비었다` · `plan 이 없다` · `행 수 195 ≠ 194` |
| adversarial (G2R-02 · 03 · GEN2-01 회귀) | 막다른 간선 다섯 15000.5 (1e14 = certificate_failed → spsolve_fallback) · 직렬 1e16 = current_conservation_failed · zero_Rc = None · 옛 세대 변이 8 = NOT_COMPUTED + 정지 ⑨ | 같은 판정 · 같은 방법 · 1e8 G 15000.500000014901 (Codex 15000.5 · 상대 9.9e-13 — 이전 우리 재현과 같은 끝자리) |
| numerics (참 G 1.45 · 13 입력) | 최악 상대오차 1.6442660633053663e-07 · 방법 열 | **13/13 G 비트 동일** (float.hex) · 같은 방법 · 증서 문제 None |
| real_beds (실덤프 두 건 · build/solve) | real14 · case15 × 4 팔 × 3 가지 | 판정값 같음 — None 모양 같음 (g1 · g2 협착-only 만 None) · clamp · floor · 관통 Rc=0 수 같음 (real14 g2 2,607 · 22 · 2,628 · case15 g2 304 · 8 · 312 · g1 7,487 · 43 · 7,528 / 1,524 · 19 · 1,543) · 값 상대차 real14 ≤ 6.11e-15 · case15 ≤ 4.22e-09 (비트 동일은 None 행 넷뿐 — 이전 우리 재현과 같은 플랫폼 차) |

- `verify_evidence.py` 는 돌리지 않았다 — 그 스크립트는 **고치기 전 반례가 재현됨**을 PASS 로 센다 (Codex README) · 고친 트리에서는 그 항목들이 의도대로 FAIL 이다.
- 게시 실패 변이의 탐침 기록 `stop` 칸 (`① … 파일 없음`) 은 탐침이 게시 **뒤** 폴더에 정지 판정을 다시 부른 값이다 — 후보가 활성 세대가 되지 않아 모드 파일이 없다.  거부 사유는 `attempt_reasons.out` (각 폴더의 `network_attempt.json` `reason`).
