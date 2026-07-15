# STEP4-v2 설계 — 시간적분 + 구형확산 + 비선형 BV (voxel-DFN, SSB) (2026-07-15 draft)

v1(저율 선형 BV·균일 SOC·RELATIVE 스냅샷, `step3_sigma.solve_reaction_current`) → v2 =
갈바노스타틱 **시간 전개**.  같은 복셀 미세구조 위에서 방전을 실제로 굴린다.

## 0. 산출물 (왜 하는가)

- **V(t) 방전곡선** (half-cell vs Li counter), C-rate sweep → **capacity@cutoff vs rate**
- **입자별 SOC(t)** → 활용 불균일의 시간 전개 (v1 hot-spot 스냅샷의 동역학판)
- **분극 분해**: ohmic(전자/이온) vs kinetic(BV) vs diffusion(구형) — 시점별
- **SBE vs DBE 같은-침대 rate 비교** = SDCP의 rate-capability 가치 정량 (manuscript 다음 축;
  σ_SDCP 4점 곡선과 접합 — 브리지가 고율에서 언제 결정적이 되는가)

## 1. 물리 (SSB-특화 단순화 2개는 근사가 아니라 물리)

- **SE = 단일이온 전도체(t⁺≈1)** → 전해질 농도분극·염 확산 없음 → 이온망은 시종 옴익.
  액체 DFN 대비 "생략"이 아니라 황화물 SSB의 **정확한** 거동.
- **전위 준정적**: 전기장 이완시간 ≪ 확산시간 → 각 시점 (φ_e, φ_i) 정상상태 결합해.
- **입자 내부**: c_s(r,t) 구형 1D Fick — ∂c/∂t = D_s·(1/r²)∂/∂r(r²∂c/∂r).
  BC: 표면 flux = (그 입자의 BV 면전류 합)/(표면적), 중심 대칭.  입자별 독립(1271개).
- **BV 면** (v1과 같은 rasterized AM|ion 면): i = i0(c_surf)·[e^{0.5Fη/RT} − e^{−0.5Fη/RT}],
  η = φ_e − φ_i − U_ocp(c_surf).  SDCP는 v1처럼 자기-BV 없음(비인터칼레이션, 배달만).
- **갈바노스타틱**: I_tot = C-rate × (AM 질량 × 비용량) 고정.
  V(t) = φ_e(집전체) − φ_i(분리막) 기준 — Li counter/anode 과전압은 범위 밖 명시(half-cell).

## 2. 수치

- 시간 루프(adaptive Δt): 스텝마다 **Newton** on (φ_e, φ_i) — 면별 g_ct = ∂i/∂η만 갱신하면
  v1의 결합 SPD 조립을 그대로 재사용, CG(CuPy)는 이전 해 warm-start (스텝간 Δ 작음 → 수 iter).
- 구형확산: 입자별 tridiagonal **Crank–Nicolson**, (1271 입자)×(Nr≈20 셸) 벡터화 — 비용 무시급.
- 격자: 동역학 1차는 **vox 0.8µm**(dof ~1/8)로 개발/스윕, 결론 런만 0.4 확인.
- 성능 추정: ~50 steps × 2-3 Newton × warm CG ≈ V100에서 케이스당 십분~시간 단위 — 실행 가능.
- 저율 극한 회귀: C→0에서 v2 첫 스텝 ≡ v1 (선형화 일치) = 필수 selftest.

## 3. §F1 입력 3개 (앵커 — 사용자 확인 후 확정)

| 입력 | 계획 | 상태 |
|---|---|---|
| U_ocp(SOC) NMC811 | pybamm 내장 Chen2020 OCP를 테이블 export → `docs/data/` 체크인 (provenance 깨끗, 날조 0) | 승인 대기 |
| D_s (NCM811) | 문헌 범위 1e-14–1e-13 m²/s → `--d-s` 입력 노출(기본 3e-14 = Kang&Shin FEM 값 인용) | 승인 대기 |
| i0 | v1 훅 유지(2 A/m², ⚠F1) + `--i0` 스윕 | 유지 |

## 4. pybamm 앵커 (frame[4] — 독립 참조와 대조, cross-fit 금지)

- **균질 트윈**: pybamm DFN(/SPMe)에 우리 STEP3 산출 σ_e_eff·σ_ion_eff·ε·두께 + 동일
  OCP/D_s/i0/대표입경 입력 → V(t)·분극 대조.
- 프로토콜: (a) **균일-구조 극한**(합성 uniform 침대)에서 voxel-v2 ≈ pybamm 수 % 이내 = 솔버
  검증; (b) 실제 침대의 편차 = **미세구조 효과의 정량**(이게 부가가치 — 균질모델이 못 보는 것).
- 실행 위치: pybamm은 WSL/V100 (cloud 컨테이너 미설치).

## 5. 구현 순서 (각 단계 selftest + 물리 2-agent 리뷰)

1. `scripts/step4_dyn.py` 구형확산 코어 — 해석 selftest: 정상상태 flux 프로파일 일치,
   질량보존 기계정밀도, 초기 반무한 √t 침투.
2. 비선형 BV Newton (v1 조립 재사용) — 저율 극한 v1 재현 회귀 + KCL 잔차.
3. 갈바노 시간 루프 + V(t)/SOC(t)/분극 출력 (npz + payload `step4_dyn` 키).
4. pybamm 앵커 스크립트(`scripts/step4_pybamm_anchor.py`) + OCP export.
5. V100 스모크: DBE 침대 0.1C/1C → SBE 재압밀 후 rate 비교 셋.

## 6. 범위 밖 (정직 선언)

열/부피변화/열화 커플 없음(A10), anode 없음(half-cell), SE 농도분극 없음(물리적으로 부재),
입자균열 진행 없음(Auerbach는 압밀 스냅샷).  v2는 **transport→kinetics→diffusion** 3층까지.
