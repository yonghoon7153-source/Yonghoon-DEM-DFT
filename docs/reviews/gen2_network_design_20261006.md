# 접촉망 세대 2 — 설계 기록 (C1 · C2 · 2026-10-06)

- 1저자 비준 (10-06): ψ 배치 = 곱셈 (`L2-01` · *"그럼 lhs는 lhs고 오늘이라도 코드 수정을 맞게 해야되는거 아니야?"* → 비준) → `50de4e806`.
  나머지 묶음 = C1 · C2 설계표 *"권고대로"* + 진행 순서 *"이것도 비준이야"* (1. C1-1 · 3 · 5 와 C2 ①–⑤ 시험 먼저 + 원장 `L2-01` → 2. 게이트 →
  커밋 → 푸시 → Codex 요청서 → 3. A · B 코드 + C2-⑥ → 4. 194 배치 새 등록 + WSL 명령 → 5. LHS v1.3).  D (HND-03 새 DEM) 는 제외 (*"D는 굳이"*).
- 구현 커밋: `a0a24c538` (C1-1 · C1-3 · C1-5 · C2 ①–⑤).  C1-4 (공유-코어 bulk) = 사전등록 뒤 (오늘 아님) · C2-⑥ = 다음 커밋 (망과 독립) · ⑦ HOLD.
- 설계 근거 스크립트 · 출력: `docs/data/gen2_design_20261006/` (c1 · c2 — 실행 당시 사본 · 아래 §4).

## 1. C1 — 전극 · Hertz 협착 · CF 가드 (설계 표 그대로)

근거 = real_14 · case15 실덤프 + 같은 기하 FV 기준 (구 사슬 · SC/BCC/FCC 격자 · 무작위 충전).

| # | 항목 | 판정 | 결정 (비준) |
|---|---|---|---|
| 1 | L2-05 전극 | 가상 전원/싱크 g_b (모든 간선 의존) → 정확 Dirichlet (B = 1 · T = 0 고정 · spsolve ≤ 30k / CG rtol 1e-10 + ILU) | ✅ 세대 2 포함 · 배포값 변화 ≤ 1.5e-4 (194 행 5–6 째 자리) · 시험 `test_network_dirichlet` · 메타 `electrode_model = dirichlet_exact` |
| 2 | TAU-13 Hertz ψ 단독 (H1) | 모든 기하에서 과전도 +6 … +50 % (원기둥 bulk 과전도가 드러남) | ⛔ 기각 |
| 3 | H1 + 구 조각 bulk (H12) | 시험한 기하 (FV 기준 SC · BCC · FCC 격자 · 무작위 충전) 에서 z ≤ 10 개선 (±5 %) · z ≈ 12 · s ≳ 0.3 (LHSx 고밀) +20–28 % 과전도 — ⚠ 배위수만으로 보증 아님: 구 사슬 z = 2 · s 0.30 / 0.45 / 0.50 / 0.70 에서 H12 −2.0 / −5.6 / −6.4 / −7.4 % · 참값이 [H0, H12] 밖 (Codex G2R-04 · 10-06 밤 정정) | Hertz 기본 = H0 유지 (주 값 그대로) · H12 = 짝 팔 + 194 재실행에 `_h12` 민감도 열 (기본 학습 제외 · 행마다 H0 와 짝인 두 규약의 시나리오 — 오차막대 · 구간 아님 · G2R-04) · H1 단독 조합 거부 |
| 4 | 공유-코어 bulk | 간선별 bulk 의 원리적 한계 (T_CF = V_구 / (V_막대 · Σcos²θ): 원기둥 4/z · 구 조각 6/z) | 사전등록 (z 4–12 무작위 · AM 장애물 · 실침대 복셀 \|f_망/f_FV − 1\| ≤ 10 % 통과 전 기본 불변) — 오늘 아님 |
| 5 | CF q > 1.5 가드 | LHSx CF 29 행 solve_failed = 모형 과전도 오분류 (q = −0.222 + 0.233·φ·CN, R² 0.985) | ✅ 가드는 FULL 만 · CF / 협착-only 는 값 유지 + `model_over_conduction` (진단 열만) |

- 실침대 s = a/r (Hertz): real_14 중앙 0.27 (전력가중 0.22) · case15 전력가중 0.07 · 194: LHS s_A 0.20–0.45 · LHSx 0.42–0.46 · SE–SE CN LHS 중앙 4.7 · LHSx 6.9–11.2.
- H12 효과 (설계 추정): real_14 σ ×1.186 · case15 ×1.060 · 194 추정 LHS ×1.20 · LHSx ×1.21 (×1.03–1.37).

## 2. C2 — Physics 접촉면적 (설계 표 그대로)

근거 = real_14 (접촉 106,563) · case15 (182,995) 커밋 덤프 + 합성 쌍 · HEAD 재계산 비트 동일.

| 결정 | 항목 | 결정 (비준) | 근거 · 영향 |
|---|---|---|---|
| ① | L1-02 겹침 부피 | 정확 lens (`lens_volume`) | 옛 V 식 = lens 의 0.49 배 · δ 0.95 에서 음수.  σ −0.04 … −0.23 % |
| ② | L1-01 상 · 하한 충돌 | 규칙 B: A = max(A_disc, min(A_Tabor, V_lens/h, cap)) | 규칙 A 는 SE–SE 22.8 % (case15 49.7 %) 를 원판 아래로 · 비단조 7/7 · 이온 −9.6 / −49.7 %.  규칙 B 연속 · 단조 7/7 |
| ②b | floor | = 원판 c_cpl[22] (= Hertz 모드 면적) | ⇒ 간선마다 R_c(Physics) ≤ R_c(Hertz) 불변식.  πR*δ floor 면 이온 −9.3 % · 불변식 소멸 |
| ③ | L1-03 쌍별 E* | SE–SE 13.19 · AM–SE 22.41 GPa · AM–AM = 원판 + `native_unsupported_pair` | real_14 g2 = ψ 곱셈 대비 이온 −15 % · 전자 −38 % · 열 −17 % |
| ④ | L1-08 h_film 5 nm | 값 유지 + [미확인] 표지 | h 1–10 nm 에서 σ 6 자리 동일 · 20 nm −2.8 % · 50 nm −10 % |
| ⑤ | SELF-28 floor (ψ < 1e-4 → R_c 0) | 동결 유지 (곱셈에선 연속 끝점) | floor on/off \|Δσ\|/σ ≤ 6.6e-7 |
| ⑥ | LHS-25 Coverage 분모 · 100 % 클립 | 합집합 cap 피복 (`*_physics_union` 새 키) — **다음 커밋** | Coverage 를 바꾸는 유일한 수정: real_14 51.5 → 43.2 % (×0.84) · case15 ×0.87 |
| ⑦ | LHS-26 rough 모양 인자 | HOLD | 모양 인자 값 자체가 가정 |

- DESC-03 (단위 1000 배) · DESC-10 (옛 V 경로 활성화) = ①②③ 과 같은 커밋으로 g2 함수 안에서 닫힘.
- ⚠ 세대 3 질문 (오늘 아님): Tabor 계산용 real-E 재구성 힘이 DEM 자신의 힘의 2.5–3.2 배 (SE–SE ×4.9 · AM–SE ×6.6 중앙).  DEM 힘을 쓰면 SE–SE 100 % floor · σ_ion −11 % ⇒ Physics = 부록 opt-in 유지 + 한정어.

## 3. 구현 뒤 실측 (`a0a24c538` · real_14 이온 · SE–SE 74,604 간선)

| 변형 | σ_ratio | 비 |
|---|---|---|
| Hertz H0 — 옛 전극 → Dirichlet | 0.0210206 → 0.02102106 | ×1.0000219 |
| Physics g1 — 옛 전극 → Dirichlet | 0.03721034 → 0.03721112 | ×1.0000210 |
| Physics g2 (새 기본) | 0.03164009 | g2/g1 0.8503 · g2/H0 1.505 |
| H12 | 0.02494138 | H12/H0 1.1865 |
| CF — H12 대 H0 | — | 0.6905 (≈ 4/6 · 원기둥 → 구 조각 bulk) |

- 협착 0 간선 (physics): g2 clamp 2,607 + floor 22 (g1 7,487 + 43) — `SELF-28` 열림 유지.
- 간선 불변식 R_c(physics) ≤ R_c(hertz) (열 · 전자 107,223 간선): g2 위반 0 · HEAD 322 (최악 1.412) · 규칙 A 였으면 15,235.
- 시험 (구현 전 → 뒤): `test_physics_area_g2` 6/15 → 27/27 · `test_network_dirichlet` 1/13 → 14/14 · `test_network_generation2` 2/8 → 18/18 ·
  `webapp/test_psi_generation_stamp` ⑤c 에서 멈춤 → 18/18 · `lhs_design_dataset` selftest 309/331 → 331/331 · `lhs_release_build` 10/15 → 15/15.
- GOLD 이동 (새 코드로 다시 뜬 값 · 손으로 치지 않음): 전극만 바뀐 값 상대 +1.16e-4 … +5.69e-4 (예 L0 Hertz σ_full 0.00400388 → 0.00400538) ·
  Physics 기본 (g2) L0 0.00955206 → 0.00692755 · `test_constriction_power_share` C1d 0.0916787 → 9/110 (정확).
- 194 배치 봉인 `CODE_FILES` 중 sha 가 바뀐 것 5/19: `network_conductivity.py` · `plastic_coverage.py` · `audit_constriction_deleted.py` · `tau_flux.py` ·
  `webapp/pipeline_service.py` ⇒ 194 재실행 = 새 등록 문서 + 새 ROOT.

## 4. 근거 스크립트 (`docs/data/gen2_design_20261006/`)

- 실행 당시 사본 그대로 (경로 · 상수를 고치지 않았다).  리포 모듈 사본 (`lib/` · `head/`) 과 덤프 사본 (`data/`) 은 넣지 않았다 —
  모듈 = `git show <sha>:scripts/<모듈>` (C1 은 `docs/data/gen2_design_20261006/c1/LIB_HEAD_SHA.txt` 의 sha) · 덤프 = `docs/data/real14_reference_20260928/` · `docs/data/case15_corner_20261001/` 의 `.gz` 를 푼 것.
- c1: `fv_sphere_chain.py` (구 사슬 FV · 표 `fv_sphere_chain_table.txt`) · `fv_lattice3d*.py` · `fv_oct.py` · `fv_random.py` (격자 · 무작위 충전 FV) ·
  `net_beds*.py` (실침대 망 · H0/H1/H12/CF) · `l205_demo.py` (L2-05 막다른 가지) · `lhs194_estimates.py` (194 행 효과 추정) · `sc_codex_check.py`.
- c2: `eval_bed*.py` (규칙 A/B · floor 후보 · 쌍별 E*) · `cov_union*.py` (⑥ 합집합 피복) · `force_*.py` · `eval_fdem.py` (세대 3 질문) · `g2lib.py` (제안 함수) ·
  `lhs26_fixture/` (⑦ 모양 인자 픽스처).
