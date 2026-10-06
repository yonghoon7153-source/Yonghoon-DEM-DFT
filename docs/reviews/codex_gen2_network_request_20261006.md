# Codex 리뷰 요청 — 접촉망 세대 2 (ψ 곱셈 · Physics 면적 g2 · 정확 Dirichlet 전극 · CF 과전도 표지 · H12 민감도 팔) (2026-10-06)

- 직전 판정: `docs/reviews/codex_review_rglr3_reverify_20261006.md` (Codex 5차 — 고정 194 행 조건부 인계 GO · Physics = 면적 + 협착 규약의 결합 민감도 ·
  기본 학습 열 제외 · *"큰 면적이 접촉 저항을 지운다"* 거짓 (legacy ψ 는 s > 0.4 에서 R_c 증가 · s ≥ 0.998 절벽) · CF 망 자체가 과전도).
- 이번에 한 것: 그 판정이 짚은 협착식 · 면적 · 전극 · CF 문제를 **코드에서** 고쳤다 (세대 2).  고정 194 행 (v1.2 배포) 은 그대로 두고,
  새 코드로 194 를 다시 돌리는 것은 **이 리뷰와 병렬로** 새 등록 뒤 (1저자 순서 4).
- 1저자 비준 (10-06): ψ = 곱셈 (*"오늘이라도 코드 수정을 맞게 해야되는거 아니야? 내가 보고하면 되니까"* · *"lhs값까지 수정해서 줄 수 있음 좋겠네"*) ·
  C1 · C2 설계표 *"권고대로"* · 진행 순서 *"이것도 비준이야"* · *"중간에 codex 리뷰도 받고"*.
- 설계 기록 (결정표 · 근거 수치 · 구현 뒤 실측): `docs/reviews/gen2_network_design_20261006.md` · 근거 스크립트 `docs/data/gen2_design_20261006/`.
- 계약 개정: `docs/area_contract_20260913.md` (10-06 개정 노트 둘 — ψ 기본값 전환 · 세대 2 나머지).  S3 봉인은 리포에 없어 기본값 전환은 **개정**으로 했다 (09-17 창 지남).
- 검토 대상 = 이 요청서를 담은 커밋 (브랜치 `claude/stoic-knuth-NObVQ` · 1저자가 발송 때 sha 를 적는다).

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 | 시험 (구현 전 → 뒤) |
|---|---|---|---|
| `50de4e806` | L2-01 | `PSI_PLACEMENT_DEFAULT = PSI_MULTIPLY` (Physics R_c = ψ · R_H) · 세대 표기 `psi_placement` (이온 · 전자 · 열) · tau_flux 협착 라벨이 실제 ψ 를 따름 (`mikic_psi_multiply` / `mikic_psi_divide`) · 감사 · S3 · ρ 도구 = `PSI_DIVIDE` 명시 · 웹앱 `psi_placement_physics` 표기 | `test_psi_default_switch` 7/17 → 20/20 · `webapp/test_psi_generation_stamp` 2/9 → 9/9 · GOLD 세대 1 (명시 PSI_DIVIDE) + `GOLD_G2` |
| `a0a24c538` | L2-05 · L1-01 · L1-02 · L1-03 · DESC-03 · DESC-10 · (TAU-07 · 13 부분) | Physics 면적 `plastic_coverage.film_area_g2` (규칙 B · 원판 floor · 정확 lens · 쌍별 E* · µm) = 기본 `physics_g2` · 정확 Dirichlet 전극 · CF/협착-only q > 1.5 = 값 유지 + `model_over_conduction` · H12 짝 팔 (`hertz_h12`) · 세대 섞임 거부 (tau_flux · 인계 생성기 · 배포 빌더 `--appendix`) · 웹앱 provenance · 정지 계약 ⑨ · 툴팁 | `test_physics_area_g2` 6/15 → 27/27 · `test_network_dirichlet` 1/13 → 14/14 · `test_network_generation2` 2/8 → 18/18 · `lhs_design_dataset` 309/331 → 331/331 · `lhs_release_build` 10/15 → 15/15 |
| (이 커밋) | 기록 | 원장 claimed_fixed (`a0a24c538`) · 메모 · 새 P3 `GEN2-01` · 설계 기록 · 근거 스크립트 · CLAUDE.md 날짜 노트 · 이 요청서 | — |

전체 게이트 (`scripts/check_all.sh`): `50de4e806` ✓ 102 ✗ 0 · `a0a24c538` ✓ 105 ✗ 0 (새 시험 셋 등록 · 푸시됨).

## 2. 무엇이 바뀌고 무엇이 그대로인가

| 축 | 세대 1 (옛 산출물 · 표기 없음 = 이것) | 세대 2 (기본) | 그대로 |
|---|---|---|---|
| Physics ψ 배치 | 분모 (`legacy_divide`) | 곱 (`mikic_psi_multiply`) | ψ = (1 − a/r_min)^1.5 · floor ψ < 1e-4 → R_c 0 (동결 · SELF-28) |
| Physics 면적 | `physics_g1` (옛 5-regime · V 식 · AM–SE E* 공용 · 5 nm 단위 혼용) | `physics_g2` 규칙 B = max(c_cpl[22] 원판, min(Tabor · 정확 lens/h · π r_min²)) | Hertz 면적 = c_cpl[22] 원판 |
| 전극 | 가상 전원/싱크 g_b (`virtual_source_legacy`) | 정확 Dirichlet (`dirichlet_exact` · B∩T = `boundary_overlap` 미풀이 · 떠 있는 섬 제외) | 경계 띠 규칙 L0/L1/L2 |
| bulk | 원기둥 반지름 r · 길이 d/2 (`cylinder_half_d`) | 기본 그대로 · H12 팔만 구 조각 | Hertz 기본 H0 = Maxwell + 원기둥 (간선 비트 동일 — ⑨ float.hex) |
| q > 1.5 가드 | FULL · CF · 협착-only 모두 거부 (None) | FULL 만 거부 · CF / 협착-only = 값 + `model_over_conduction` | 열 = 병렬 상한 G ≤ 1.1·Σg |

- 불변식 (설계 ②b): 간선마다 A_physics ≥ A_disc 이고 ψ ≤ 1 ⇒ **R_c(physics) ≤ R_c(hertz)** — real_14 열 · 전자 107,223 간선 위반 0 (HEAD 322 · 최악 1.412).
- 옛 산출물은 표기가 없으므로 = 세대 1 (`physics_g1` · `virtual_source_legacy` · `cylinder_half_d` · ψ 는 `psi_placement` 가 있으면 그것).  세대가 섞인 표는 거부.
- LHS 배포 v1.2 (`docs/data/lhs_release_20261006_v12/`) 의 Physics 부록 = **세대 1** (README 경고 있음) — v1.3 에서 교체 (새 194 배치 뒤).

## 3. 증거

- 실측 (real_14 이온): 설계 기록 §3 표 — Hertz H0 전극만 ×1.0000219 · Physics g2/g1 0.850 · g2/H0 1.505 · H12/H0 1.187 · CF H12/H0 0.6905.
- 독립 대조: `test_network_boundary_rule` ⑨ — 옛 모듈 (`eedada5d3`) 간선 = 지금 모듈의 명시 세대 1 간선 float.hex (3 픽스처 × 2 면적 × 3 풀이) · 지금 해 = 독립 numpy Dirichlet 해 (1e-12).
- 봉인 셀프테스트 (`seal_s3_prerun` · `run_s3_psi`) 는 작업트리가 수치 모듈을 고치는 동안 거부한다 (설계대로) — 커밋 뒤 게이트에서 통과.
- 게이트 `a0a24c538`: ✓ 105 ✗ 0 — "✓ 전부 통과" (봉인 셀프테스트 포함 · 깨끗한 트리).

## 4. 열린 것 · 결정 대기 (숨기지 않음)

| 항목 | 상태 |
|---|---|
| `GEN2-01` (P3 · 새) | 협착-only 진단 가지: R_c = 0 간선 = 열림 (g = 0) → 떠 있는 섬 제외 뒤 유한값 = 그 가지의 하한 (HEAD 는 특이 → physics NaN) · real_14 g2 0.054176 · g1 0.071330 · 떠 있는 노드 29 · 쓰임 = 194 진단 열 `sigma_constr_net_mScm_<m>` 뿐 · 처리 (단락 수축 / not_computed) = 1저자 |
| `TAU-13` | 세대 표기 + H12 팔 + 섞임 거부 들어감 · H0 = 세대 1 Maxwell 은 설계상 유지 → 닫을지 = 1저자 (open) |
| `TAU-07` · `TAU-08` | CF 지위 · 문구 고침 · "geom" 오명 · CF 원기둥 bulk 는 남음 (open) |
| `L1-08` · `SELF-28` | 5 nm [미확인] 유지 · floor 동결 + clamp/floor 수 기록 (open) |
| H12 표시 | 케이스 페이지에 없음 (툴팁 · 인계 부록만) |
| Physics 부록 규칙 | README 로만 강제 · 배포 빌더 `--appendix` 는 H12 열만 막는다 |
| 옛 배치의 H12 | H12 레코드가 없어 `_h12` 열 = NOT_COMPUTED (`missing_input`) — 인계의 "NOT_COMPUTED 없음" 규칙의 유일한 예외 (문서화) · 값은 새 194 배치에서 |
| C1-4 공유-코어 bulk | 사전등록 뒤 (오늘 아님) |
| C2-⑥ 합집합 피복 · ⑦ 모양 인자 | ⑥ 다음 커밋 (Coverage ×0.84–0.87) · ⑦ HOLD |

## 5. 질문

1. **ψ 곱셈 전환을 계약 개정으로** (S3 봉인 없이 · 09-17 창 지남) 한 것이 계약 · 원장 절차상 받아들일 만한가.  `L2-01` claimed_fixed 의 증거 (`test_psi_default_switch` · `test_psi_generation_stamp` + `constriction_reference.py` FV 10 점) 로 충분한가.
2. **g2 규칙 B** (floor = c_cpl[22] 원판 · 상한은 소성 연장분만 묶음) 가 L1-01 · 02 · 03 · DESC-03 · 10 을 닫는가.  불변식 R_c(physics) ≤ R_c(hertz) 를 기본 Physics 의 정의로 삼는 것에 반례가 있나.
3. **정확 Dirichlet 전극** 구현 (`solve_network` · 떠 있는 섬 · B∩T 거부 · 직접해 ↔ CG ↔ ILU 사다리 · G ≤ 1.1·Σg 가드) 에 결함이 있나.  `GEN2-01` 의 두 처리 중 어느 쪽이 맞나.
4. **CF 가드를 FULL 에만** 두고 CF / 협착-only 를 `model_over_conduction` 값으로 남기는 것이 Codex 5차의 "CF 망 자체가 과전도" 판정과 맞나 (인계 열에는 CF 가 없다).
5. **H12 = 민감도 짝 팔** (기본 학습 제외 · 부록 전용 · H1 단독 거부) 의 지위 · 게이트가 충분한가.  `TAU-13` 을 닫아도 되나.
6. **세대 섞임 거부** (tau_flux `generation_mixing_problem` · 인계 `load_tau_results` · `build_handover` · 정지 계약 ⑨) 에 새는 경로가 있나 (옛 산출물의 표기 없음 = 세대 1 추론 포함).
7. **새 194 배치** (봉인 CODE_FILES 5/19 변경 · 새 등록 · 새 ROOT) 를 돌리기 전에 막아야 할 것이 있나.  Physics 부록 (세대 2) · `_h12` 열의 인계 지위 (Codex 5차 §6 사용 설명) 를 어떻게 적어야 하나.
8. Physics T < 1 (MODEL_BELOW_CONTINUUM_BOUND) 은 곱셈 + g2 로 늘 것으로 예상된다 (설계 추정 LHS 0–7/106 · LHSx 30–59/64 · 외삽) — 상태 열 · 한정어 외에 더 할 것이 있나.
