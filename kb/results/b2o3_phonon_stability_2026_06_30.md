# B₂O₃-doped LPSCl1.6 챔피언의 동역학적 안정성 (UMA Γ-point phonon)

**날짜** 2026-06-30 · **방법** UMA(omat) Γ-point 유한변위 phonon (ASE Vibrations, δ=0.02 Å)
**구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀ 고정셀 relax, 128 atom) · **결과** `db/properties/b2o3_phonon_stability.json`, `tools/electronic/uma_phonon.py`

> **한 줄 결론.** B₂O₃-doped 챔피언은 **Γ에서 허수모드 0개 = 동역학적으로 안정한 진짜 국소최소**다. convex hull상 0K hull 위 **+37.5 meV/atom(준안정)** 이지만, 안장점이 아니라 **실재하는·합성가능한 상**임이 phonon으로 독립 확정된다. 게다가 최저 실수모드(~14 cm⁻¹)가 **soft-but-stable** → 무른 Li 부격자 = 높은 Li 전도(Ea 0.207)와 정합.

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
최저 실수모드가 **~14 cm⁻¹**로 매우 낮음(허수는 아님). 이 저진동 모드는 무른 Li 부격자/anion libration에서 옴 — **"무르지만 안정"** = Li가 쉽게 움직이되 구조는 안 무너짐. **낮은 Ea(0.207 eV)·높은 D**(MD 결과)와 일관된 그림: superionic conductor 특유의 soft 격자.

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
- **MD**(Ea 0.207, D↑) + **최저 soft 모드 ~14 cm⁻¹** → 무른 Li 부격자 = 빠른 전도.
- **배위 BS₃**(5중 확증) 구조가 동역학적으로도 안정 = 그 motif가 인위적 artifact가 아님을 재확인.

## 참고
- `db/properties/b2o3_phonon_stability.json`, `tools/electronic/uma_phonon.py`, `/data/work/runs/b2o3_phonon_freqs.txt`(gabia, 384 모드 전체)
- 관련: `kb/results/b2o3_convex_hull_2026_06_29.md`, `b2o3_champion_coordination_2026_06_29.md`, `db/properties/b2o3_md_arrhenius.json`
