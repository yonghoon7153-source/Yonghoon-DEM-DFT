# Codex 재검증 요청 — 접촉망 세대 2 수정 (G2R-01 · 02 · 03 · 04 · GEN2-01) (2026-10-06 밤)

- 직전 판정: `docs/reviews/codex_review_gen2_network_20261006.md` (핀 `c13da95a3` · 새 194 생산 · v1.3 주 학습 인계 HOLD · 계산 교정 지지) ·
  증거 `docs/reviews/codex_gen2_network_review_evidence_20261006/` (우리 트리 재현 `_reproduction_ours_7a5976602/` · 고친 트리 재실행 `_rerun_fixed_8727aa85e/`).
- 1저자 비준 (10-06 밤): 수정 계획 표 그대로 (*"이것도 비준이야"*) · v1.3 = 세대 2 수정 · 재검증 · 194 재실행까지 끝낸 완전판 (*"v1.4 보낸다는 느낌으로 v1.3 준비"*).
- 검토 대상 = 이 요청서를 담은 커밋 (브랜치 `claude/stoic-knuth-NObVQ` · 1저자가 발송 때 sha 를 적는다).

## 1. 패치

| 커밋 | 원장 | 내용 | 시험 (고치기 전 → 뒤) |
|---|---|---|---|
| `05c60ae2d` | G2R-01 · 02 | 공용 세대 계약 `tau_flux.network_generation_contract` — 모드마다 닫힌 표 (아래 §2) · 세대 2 = 표기 전부 필수 · 모르는 값 · 부분 결손 거부 · 옛 세대 추론 = 세대 2 표지가 **하나도 없는** 레코드만 (`inferred_legacy` 표지) · 행마다 먼저 (같은 결함 코호트도 거부) · 게시 전 (정지 ⑨ · 일반 경로) · τ 소비자 · 인계 생성기 · 배포 빌더가 같은 함수 · 새 열 `ion_net_generation` · provenance `P4_model_generation` · 웹앱 "망 세대" 행 | `test_gen2_role_contract` 5/24 → 24/24 · `webapp/test_gen2_publication_handover` 2/12 → 12/12 · `test_tau_handover_status` 38/41 → 41/41 · `lhs_release_build` 27/31 → 31/31 |
| `05977e94a` | G2R-03 · GEN2-01 | 풀이마다 증서 (`I_bottom` · `I_top` · `conservation_rel` · `residual_rel` · `method` · `attempts`) · 허용치 `DIRICHLET_CONSERVATION_REL_MAX = DIRICHLET_RESIDUAL_REL_MAX = 1e-6` · 실패면 사다리 · 다 실패 = not_computed `current_conservation_failed` · 레코드 `solve_certificate_{full,bulk_net,constr_net}` (세 채널 · H12) · 협착-only 에 R_c ≤ 0 이면 그 가지만 not_computed `zero_resistance_requires_contraction` | `test_network_solve_certificate` 5/23 → 23/23 (고치기 전 모듈) |
| `5627a74a6` | G2R-03 · 04 · GEN2-01 | 증서 → 계약: 게시되는 FULL σ (`sigma_full_status` computed) 는 통과 증서 필수 (판정 = 생산자 `certificate_problem` 하나) · 증서 키 = 세대 2 표지 · G2R-04 문구 (열 사전 · 배포 빌더 · tau_flux · 설계 기록) · 배치 열 `sigma_constr_net_status/_reason` | `test_gen2_role_contract` X2–X5 25/30 → 30/30 · W1 · W2 (G2R-04) · `test_pipeline_provenance` 픽스처 (증서) 267/284 → 284/284 |
| `8727aa85e` | 원장 | G2R-01~04 · GEN2-01 claimed_fixed | — |

## 2. 계약 표 (생산자 실 출력에서 읽은 필드 · 값)

| 필드 | hertz (H0) | hertz_h12 | physics |
|---|---|---|---|
| contact_mode | hertzian | hertzian | physics |
| resistance_model | maxwell | mikic | mikic |
| hertz_constriction | maxwell | mikic_psi_multiply | 없음 / null |
| bulk_model | cylinder_half_d | sphere_segment | cylinder_half_d |
| electrode_model | dirichlet_exact | dirichlet_exact | dirichlet_exact |
| area_rule | hertz_ccpl22 | hertz_ccpl22 | physics_g2 |
| area_rule_physics | physics_g2 | physics_g2 | physics_g2 |
| psi_placement | multiply | multiply | multiply |
| sensitivity_mode | 없음 | hertz_h12 | 없음 |
| solve_certificate_full | computed 이면 통과 필수 | 같음 | 같음 |

옛 세대 (194 v1.2 원천의 실제 모양): resistance_model (hertz maxwell · physics mikic) 필수 · contact_mode 있으면 자리와 같아야 · ψ = legacy_divide 또는 없음 · H12 없음.

## 3. 판정 §8 해제 목록 대응

| 항목 | 상태 |
|---|---|
| H0/H12 역할 격리 | ✅ 게시 전 거부 + 강제 폴더 인계 거부 (실 생산자 사슬) · 정상 세 모드 · 역사 194 통과 |
| 유효 세대 vs 후방 호환 | ✅ 모르는 값 · 부분 결손 · 같은 결함 코호트 거부 · 진짜 옛 레코드 = inferred_legacy |
| 수치 증서 보존 | ✅ 허용치 사전 고정 1e-6 · 모드별 증서 직렬화 · 반례 1e14 = 15,000.5 회복 (`spsolve_fallback`) · 정상 큰 망 (≈ 32 k 자유 노드) CG 그대로 · 실침대 16/18 비트 동일 |
| GEN2-01 정책 | ✅ NOT_COMPUTED 우선 (권고) · 진단 열 빈칸 |
| 새 배치 봉인 | ⬜ 새 194 등록 문서에서 (전 의존성 · 기대 모델 조합 · 원 dump · 케이스 · ROOT) — 이 재검증 뒤 |
| 인계 역할과 문구 | ✅ G2R-04 · 부록 정책 = 열 사전 · 배포 빌더 · 시험 (README 만이 아님) |

## 4. 우리가 내린 결정 (확인 요청)

1. 한 모드라도 계약 위반이면 그 케이스 **모든 모드 NOT_COMPUTED** (RGLR2-02 선례).
2. 게시는 옛 모양 후보를 거부 (현행 생산물은 세대 2 여야) · 인계 재확인만 `legacy_ok` (출처 도장이 세대 2 를 주장하지 않을 때) · 반대 방향 (옛 도장 + 세대 2 레코드) 도 거부.
3. 생산자 실패 레코드 (not_computed) 는 **실린 표기만** 대조 (값이 없어 공용 기술 검사가 막는다).
4. contact_mode 없는 수작업 레코드 = 옛 세대 허용 · resistance_model 은 필수.
5. 증서 허용치 1e-6 (실침대 ≤ 1.4e-13 · case15 FULL ≤ 6.4e-9 · CF ≤ 1.1e-10 → 150 배 이상 여유 · 반례 ≈ 1) · 내부 잔차는 보조 (반례에서 1.7e-12 — Codex 지적 그대로).
6. 사다리: 작은 망 (≤ 30 k 자유 노드) `spsolve` → `cg+jacobi` → `gmres+ilu` / 큰 망 `cg` → `spsolve_fallback` (≤ 250 k) → `cg+jacobi` → `gmres+ilu` · ILU 는 GMRES 와만 · 옛 `cg+ilu` 제거.
7. 증서 요구 = 게시되는 FULL σ 에만 (비관통 · 생산자 실패는 해가 없다) · 전자 · 열 채널 증서는 기록만 (τ 인계에 안 쓴다 · 표지 아님).
8. real14 · case15 physics g2 협착-only = not_computed (R_c = 0 간선 2,607 · 진단 열 빈칸).

## 5. 남는 것 (숨기지 않음)

- 계약은 **표기만** 본다 — 숫자를 바꿔치고 표기를 그대로 둔 레코드 · 모든 사본과 도장을 일관되게 고친 편집은 재계산 없이 못 잡는다.
- 배치 영수증에 기대 세대 봉인 = 새 194 등록 (봉인 194 러너 변경).
- `network_conductivity.py` = S3 수치 모듈 → S3 전 재봉인 · `measure_rho` 의 CG 라벨 (`cg+ilu`) 은 미관.
- 케이스 페이지에 증서 표시는 없다 (망 세대 행만 · 증서는 dual JSON 영구 산출물).

## 6. 질문

1. §3 의 다섯 ✅ 가 해제 조건을 닫는가 (특히 G2R-01 · 02 의 게시 전 + 인계 두 길 · 실 생산자 사슬 시험).
2. §4-1 (한 모드 위반 = 케이스 전체) · §4-2 (게시 = 세대 2 만 · 인계만 legacy_ok) 가 맞는가.
3. 증서 허용치 1e-6 과 사다리 순서 (§4-5 · 6) 에 반례가 있나.  내부 잔차를 보조로 두는 것이 충분한가.
4. 증서를 FULL 에만 요구 (§4-7) 하는 것이 194 인계 (τ = FULL 만) 에 충분한가.  CF · 협착-only 진단 열에도 요구해야 하나.
5. 새 194 를 돌리기 전 남은 것 = §3 "새 배치 봉인" 하나로 보는가.  덤프 몇 개로 생산 → 게시 → 인계를 먼저 통과시키는 순서 (1저자 비준) 에 더할 것이 있나.
6. TAU-13 · SELF-28 · TAU-07 의 메모 (판정 §6 · §7) 처리에 이의가 있나.
