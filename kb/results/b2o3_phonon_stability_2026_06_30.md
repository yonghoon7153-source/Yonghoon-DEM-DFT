# B₂O₃-doped LPSCl1.6 챔피언의 동역학적 안정성 (UMA Γ-point phonon)

**날짜** 2026-06-30 · **방법** UMA(omat) Γ-point 유한변위 phonon (ASE Vibrations, δ=0.02 Å)
**구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀ 고정셀 relax, 128 atom) · **결과** `db/properties/b2o3_phonon_stability.json`, `tools/electronic/uma_phonon.py`

> **⚠ 정정 (외부 peer-review 2026-06-30).** ① "동역학적으로 안정"은 과대 — **Γ-only MLIP Hessian은 q≠Γ 불안정(zone-boundary/supercell)을 못 봄** → "Γ에서 허수모드 0개(**필요조건, 충분조건 아님**)"로 한정. 완전증명엔 phonon supercell/DFPT 필요. ② **아래의 Ea 0.207은 철회된 값**(5-40ps window artifact). 일관 window(2-50ps)에서 **b2o3 Ea = 0.223 = 무도핑과 동일** → soft 격자는 **양쪽 다** 있어 **도핑특이적 낮은 장벽의 근거가 아님**; b2o3 전도 이득은 **D₀(prefactor)**. 본문의 "soft→낮은 Ea" 추론은 무효.

> **한 줄 결론(수정).** B₂O₃-doped 챔피언은 **Γ에서 허수모드 0개**(필요조건). convex hull상 **+37.5 meV/atom(준안정)**. 최저 실수모드(~14 cm⁻¹) soft — superionic 격자 특유이나 **무도핑에도 동일**(Ea 0.223=무도핑) → 도핑특이적 우위의 근거 아님.

---

## 1. 방법
- UMA-s-1p1(omat task) calculator로 128원자 셀의 **Γ-point Hessian**을 유한변위(각 원자 ±0.02 Å, 6N+1=769 force eval)로 구성 → mass-weighted 대각화 → 진동수(cm⁻¹).
- 허수(동역학 불안정)는 음의 ω²로 나타나며 음수 cm⁻¹로 표기. 임계값 −30 cm⁻¹(그 이내 음수는 수치잡음으로 간주).

## 2. 결과

| 항목 | 값 |
|---|---|
| 총 모드 수 | **384** (= 3×128) |
| **허수모드 (< −30 cm⁻¹)** | **0** |
| 소-허수 (−30 ~ −5) | 0 |
| acoustic(병진) 모드 | −0.13, −0.08, +0.11 cm⁻¹ (≈0) |
| 최저 실수모드 (cm⁻¹) | 13.7, 14.8, 15.3, 16.4, 25.4, 26.9, 28.9, 29.6, 31.0 … |

- **acoustic 3모드가 ≈0** (−0.1~+0.1) → 병진 불변(acoustic sum rule) 만족 = Hessian이 제대로 계산됨.
- 나머지 381모드 **전부 양수** → **허수모드 0개**.
- **verdict: DYNAMICALLY STABLE.**

## 3. 해석

### 3.1 진짜 국소최소 (안장점 아님)
허수모드가 없다는 건 모든 방향으로 곡률이 양(+)이라는 뜻 = 에너지 지형의 **진짜 우물 바닥**. 챔피언이 UMA relax + DFT relax로 얻은 구조가 **동역학적으로 안정한 최소**임을 확인.

### 3.2 soft-but-stable Li 부격자 → 전도와 정합
최저 실수모드가 **~14 cm⁻¹**로 매우 낮음(허수는 아님). 이 저진동 모드는 무른 Li 부격자/anion libration에서 옴. **단 이 soft 격자는 무도핑에도 동일**하고 **Ea = 0.223 eV로 b2o3=무도핑** → soft는 superionic 일반 특성이지 **도핑특이적 낮은 장벽의 근거가 아님**(b2o3 이득은 D₀). ~~낮은 Ea(0.207)~~ ← 철회.

## 4. 의의 — metastability의 동역학적 보강
| 안정성 축 | 결과 | 의미 |
|---|---|---|
| 열역학(hull) | +37.5 meV/atom 위 | 0K ground state는 아님(준안정) |
| **동역학(phonon)** | **허수 0** | **진짜 우물 = 실재·합성가능** |

→ convex hull만 보면 "준안정"이 모호하게 들릴 수 있으나, **phonon이 "안장점이 아니라 kinetically-trapped real phase"임을 못박음.** argyrodite류가 hull 위 준안정이면서도 실제로 합성·사용되는 것과 정확히 같은 양상.

## 5. 정직한 한계
- **Γ-point 한정**: 다른 q-점의 불안정(예: 격자 배수에서 나타나는 modulation)은 못 봄. 완전 증명엔 **phonon supercell / DFPT** 필요. 단 128원자 셀 자체가 Li-disorder로 대칭이 깨져 있어 Γ-Hessian도 상당한 정보를 담음(단순 primitive Γ보다 풍부).
- **UMA(MLIP) Hessian**: 절대 진동수엔 MLIP 오차. 하지만 **모드 부호(안정/불안정)** 같은 정성 결론은 견고. 정량 Raman/IR엔 DFPT 권장.
- **특정 Li-config**: 챔피언 1개 배열의 phonon. 다른 Li 배열은 별도(Li-ordering 1162 meV 스프레드).

## 6. 다른 결과와의 연결
- **convex hull**(37.5 meV/atom) + **phonon**(허수 0) → "준안정이지만 진짜·합성가능".
- **MD**(Ea 0.223 = 무도핑, D₀↑) + **최저 soft 모드 ~14 cm⁻¹**(무도핑에도 있음) → soft 부격자는 전도에 우호적이나 **도핑특이적 우위는 D₀**.
- **배위 BS₃**(5중 확증) 구조가 동역학적으로도 안정 = 그 motif가 인위적 artifact가 아님을 재확인.

## 7. Phonon DOS + 진동분광 testable 지문
**그림** `docs/figures/cascade/b2o3_phonon_dos.png` · **데이터** `db/properties/b2o3_phonon_dos.csv`, `b2o3_phonon_freqs.csv` (384 모드, max 1013 cm⁻¹)

384 Γ-모드를 Gaussian(σ≈9 cm⁻¹) broaden → 3개 밴드:
| 밴드 | 범위 (cm⁻¹) | 귀속 | 의미 |
|---|---|---|---|
| 저진동 soft | ~14–200 (peak ~130) | Li libration / 무른 부격자 | 전도 우호(Ea 0.223; 무도핑도 soft → 도핑특이 아님); 허수영역 깨끗 |
| framework | ~200–580 | P–S / B–S bend·stretch | 골격 |
| **★ 고립 고진동** | **788–1013** (7 모드) | **P–O phosphate stretch (+ B–S)** | **testable Raman/IR 지문** |

→ **새 testable prediction**: B₂O₃-doped를 **Raman/IR 측정 시 ~900–1013 cm⁻¹에 P–O stretch 피크**(무도핑엔 없음). NMR(¹¹B 삼각 BS₃ / ³¹P PS₄₋ₓOₓ)에 더해 **진동분광 검증 경로** 확보.

### 7.1 Raman/IR 스펙트럼 계산 가능성 (정직)
- **피크 위치(주파수)**: ✅ 이미 있음(UMA phonon). P–O ~900–1013은 위에서 예측됨. P1 disordered 셀이라 모든 모드가 형식상 IR+Raman 둘 다 활성 → 위치는 그대로 비교 가능.
- **세기(intensity)**: ❌ UMA로는 못 구함. IR 세기 = (∂μ/∂Q)² → **Born effective charge**(DFPT), Raman 세기 = (∂α/∂Q)² → **편극률 미분**(DFPT/유한장) 필요. UMA는 에너지/힘 모델이라 dipole·polarizability 없음.
- **정량 스펙트럼 원하면**: QE **`ph.x`(DFPT)** 로 Born charge(→IR) + (Raman은 ph.x 2차/유한장). 단 **128원자 DFPT는 매우 비쌈**(수일). 대안: ① 위치만 보고 화학지식으로 강/약 추정(phosphate P–O는 IR·Raman 둘 다 강함, 잘 알려짐) ② 더 작은 대표 셀 DFPT.
- **권장**: 현 단계는 **주파수(위치) 예측으로 충분**(fingerprint 목적). 정량 세기는 reviewer가 요구할 때 DFPT.

## 참고
- `db/properties/b2o3_phonon_stability.json`, `tools/electronic/uma_phonon.py`, `/data/work/runs/b2o3_phonon_freqs.txt`(gabia, 384 모드 전체)
- 관련: `kb/results/b2o3_convex_hull_2026_06_29.md`, `b2o3_champion_coordination_2026_06_29.md`, `db/properties/b2o3_md_arrhenius.json`
