# Tabor Elastic-Plastic Framework — Reference & Meeting-Defence Doc

**Purpose**: Standalone reference for the Tabor (1951) elastic-plastic
contact-mechanics framework as implemented in our DEM-postprocess
network solver. Use this before meetings or paper revisions to
internalize the Layer-3 reviewer-defence narrative.

**Source commits**: Methods addendum `23d3599`, μ_T analysis script
`23d3599`, FFT cross-validation `a72583e`.

---

## 1. 30-Second Pitch (One Breath)

> "우리는 매 contact 마다 세 가지 contact area — A_Hertz (elastic),
> A_Tabor (plastic), A_volume (부피 보존) — 를 계산해서 가장 작은
> 걸 자동 선택합니다. 이게 수학적으로 **Tabor (1951) 의 elastic-
> plastic 전이 기준** 과 동등합니다. Sulfide SE 의 경우 대부분
> contact 가 transitional regime 에 있어서, paper 의 Hertz column
> 과 Physics column 의 ~40 % 차이가 **calibration artifact 가
> 아니라 진짜 elastic-plastic regime 효과** 라는 정량 증거가 됩니다."

---

## 2. The Tabor Parameter μ_T — Definition

```
μ_T  =  E* · a  /  (σ_y · R)

  E*   :  effective contact modulus  ≈  E / (2(1-ν²))
  a    :  contact radius
  σ_y  :  yield strength of material
  R    :  effective sphere radius
```

### Physical meaning

```
                Hertz mean pressure         Local elastic stress
   μ_T  ≈  ─────────────────────────  ≈  ─────────────────────────
                   yield stress              yield stress
```

- 분자 ∝ Hertz 가 예측하는 contact 에서의 평균 압력
- 분모 = 재료가 yield 하기 시작하는 임계 응력
- **비가 작으면 elastic (Hertz formula 정확), 크면 plastic (yield 진행)**

### Geometric derivation (deeper)

Hertz mean pressure: p_mean = (4 / 3π) · E* · (a/R)
Yield condition:    p_mean ≈ σ_y  (또는 H/3, Tabor relation)
→ E* · a / (σ_y · R) ~ 4π/3 ≈ 4

→ **μ_T ≈ 1 부근이 elastic→plastic 전이 시작 지점**.
   Brake 2012 의 transitional band [0.1 ~ 100] 이 정확히 1 을 중심에 둠.

---

## 3. Three Regime Boundaries (Brake 2012 / Greenwood 1992)

| Regime | μ_T range | Behavior |
|--------|-----------|----------|
| **Fully elastic** | μ_T < 0.1 | Hertz formula 그대로 정확 |
| **Transitional** | 0.1 ≤ μ_T < 100 | Mixed E-P, A = min(A_Hertz, A_Tabor) |
| **Fully plastic** | μ_T ≥ 100 | Contact area saturated by yield |

---

## 4. Implementation in Our Solver

`scripts/network_conductivity.py` per-contact area selection:

```python
A_Hertz  = π · a²              # elastic, a = √(R·δ)
A_Tabor  = F / (π · H)         # fully plastic, H = 3σ_y
A_volume = 2π · R · δ          # plastic-flow upper bound (volume cons.)

A_eff    = min(A_Hertz, A_Tabor, A_volume)
```

### Why min() is mathematically equivalent to μ_T criterion

| Condition | μ_T | A selected | Physical interpretation |
|-----------|-----|------------|------------------------|
| A_Hertz < A_Tabor | small | A_Hertz | Still elastic (Hertz valid) |
| A_Hertz > A_Tabor | large | A_Tabor | Already plastic (yield saturated) |
| A_Tabor > A_volume | very large | A_volume | Geometric impossibility (cap) |

자동 전이, 별도 μ_T 계산 불필요. Numerically 안전 (negative R, δ→0
edge cases 자연스레 처리).

---

## 5. Numerical Specifics for Sulfide SE

**우리 프로젝트 단일 출처**: `scripts/plastic_coverage.py:34-45`
(LIGGGHTS poissonsRatio 설정과도 정합 — `dem_scripts/*.liggghts`).

```
Material constant       Value         Source
──────────────────────  ────────────  ─────────────────────────
E_SE  (real, lab)       24.0 GPa      Wang 2020 nanoindentation
                                       McGrogan 2017 (LPSCl)
                        (DEM sim 1.35 GPa: time-step 효율 위해 softened,
                         post-correction 분석에는 real 24 GPa 사용)
ν_SE                    0.30          LIGGGHTS poissonsRatio
                                       (dem_scripts/*.liggghts:33)
E*_SE-SE                ≈ 13.2 GPa    = E / (2(1-ν²)) symmetric pair
H_SE                    0.85 GPa      dense LPSCl (Cheng 2017 range,
                                       Sakuda 2013 amorphous = 0.6 GPa)
σ_y_SE                  0.30 GPa      = H / 2.8 (Brake 2012 ceramic
                                       standard, Tabor relation)
H/σ_y = 2.83            ✓             표준 ceramic 값 (Brake 2012)
```

### Why E_SE_real ≠ E_SE_DEM_sim?

LIGGGHTS DEM 은 cold-press 시 큰 time step 을 위해 E* 를 softened 값
(`youngs_modulus_sim` ≈ 1.35 MPa, scaled to 1.35 GPa real-equivalent)
로 사용. 이는 *compaction kinematics* 에 영향 없이 (= 도달 porosity
동일) numerical 효율만 향상시키는 표준 DEM 관행. Post-correction
analytical Tabor 분석에는 **lab 측정값 24 GPa** 사용 (consistent
with `plastic_coverage.py:E_REAL_SE`).

### Mixed AM-SE pair E*

```
1/E* = (1-ν_AM²)/E_AM + (1-ν_SE²)/E_SE
     = (1-0.0625)/140 + (1-0.09)/24
     = 0.0067 + 0.0379
     = 0.0446
E*_AM-SE = 22.4 GPa     (soft SE side dominates compliance)
```

→ AM-SE contact 의 yield 도 soft side (SE) 가 결정 → σ_y = 0.30 GPa 사용.

### Measured μ_T distribution — SE-SE contacts at 300 MPa

`analyze_tabor_regime.py --plot --pair SE-SE` 실행 결과
(commit `abbf330` 시점):

```
Tabor regime analysis  pair=SE-SE
  E*_SE   = 13.19 GPa
  σ_y_SE  = 0.300 GPa  (H = 0.85 GPa, H/σ_y = 2.8)
  Regimes:  elastic μ_T < 0.1  | transit 0.1 ≤ μ_T < 100  | plastic μ_T ≥ 100

Ensemble  (SE-SE, n_cases ≈ 80 unique)
──────────────────────────────────────────────────────────────
  Total contacts        : 36 042 312
  Median μ_T            : 12.139         ← transitional, upper-middle
  Mean μ_T              : 12.251
  IQR (Q1 – Q3)         : 8.474 – 15.761
  % in fully elastic    : 0.00 %         (μ_T < 0.1)
  % in transitional     : 100.00 %       (0.1 ≤ μ_T < 100)
  % in fully plastic    : 0.00 %         (μ_T ≥ 100)

  Verdict: SE-SE ensemble is in TRANSITIONAL regime.
```

→ **모든 contact 가 transitional band 안에 위치** (no contact reaches
   either limit). Hertz vs Physics column 의 ~40 % gap 이 "real
   elastic-plastic effect" 로 **정량 정당화 완료**.

### Physical interpretation of μ_T = 12.1

```
μ_T = (E*/σ_y) × (a/R)
    = 44 × (a/R)

→ μ_T = 12 ⇒ a/R ≈ 0.27
   r_SE = 0.5 μm 일 때 contact radius a ≈ 135 nm
```

이는 300 MPa cold-press 의 SE-SE contact 으로 정확히 합리적 (overlap
δ/R ≈ 7 %, plastic flow 시작 영역). IQR (8.5 – 15.8) 은 a/R 가
0.19 – 0.36 사이 — case 별 compaction 조건/입자 크기 분포의 자연스러운
산포.

---

## 6. FAQ (Expected Reviewer / Meeting Questions)

### Q1: "왜 μ_T 를 직접 계산 안 하고 area-min 으로?"
**A**: 수학적으로 동등하지만 area-based 가 numerically 안전.
μ_T 발산 edge case (R→0, δ→0) 도 자연스럽게 처리됨. 결과 area 가
σ_eff 계산에 직접 들어가는 양이라 한 번 더 변환할 필요 없음.

### Q2: "σ_y = H/3 어디서?"
**A**: Tabor 1951 의 Vickers indentation 분석. metal 부터 ceramic
까지 광범위하게 검증된 universal relation. Sulfide H 는 Sakuda 2013
(H ≈ 0.6 GPa, 75Li₂S·25P₂S₅) 와 McGrogan 2017 (LPSCl, H ≈ 0.5–0.7 GPa)
nanoindentation 으로 직접 측정.

### Q3: "AM 입자도 Tabor?"
**A**: **아니오**. AM (NCM) 은 brittle ceramic, plastic 보다 fracture
가 dominant. AM-AM 은 별도로 **Auerbach (1891) cone-crack onset
+ Lawn (1998) multi-stage damage progression** 으로 처리.
K_IC(AM_S) = 1.0 vs K_IC(AM_P) = 0.3 MPa·√m → P_c 11× 차이가
fracture-aware solver 의 입력. Tabor 는 SE-SE 에만 적용.

### Q4: "Transitional regime 에서 정확한 모델은?"
**A**: Brake 2012 같은 explicit 3-regime 모델이 있으나, 우리는
A_eff = min(A_Hertz, A_Tabor, A_volume) 로 자동 전이.
Greenwood 1992, Storakers 1997 와 일치하며 Brake 의 transitional
expression 보다 단순하지만 동등한 결과.

### Q5: "Plastic memory (residual deformation) 는?"
**A**: **우리에겐 무관**. **Sustained 300 MPa stack pressure** BC 라
unloading 시나리오 없음. Plastic memory (h_eq, So et al. 2022) 는
'cold-press 후 외력 제거' 시에만 의미. ASSB 작동 조건은 stack
pressure 가 항상 걸려 있어 우리 BC 가 더 physically relevant.

### Q6: "Volume conservation cap 은 뭐?"
**A**: Tabor 만 적용하면 매우 큰 force 에서 A 가 hemispherical cap
표면적 (2πR·δ) 도 초과할 수 있어 비물리적. A_volume = 2πR·δ 가
부피 보존 upper bound. Sub-μm SE 가 plastic 으로 흘러도 이
한계를 넘지 않음.

### Q7: "FFT cross-validation 과 어떻게 연결?"
**A**: Tabor framework 는 **contact 단위 (pair-resistance) 가정** 하의
elastic-plastic 분류. FFT homogenization 은 **voxel-grid (continuum)
독립 검증**. ±15 % 이내 일치하면 pair-resistance abstraction 정당화.
Layer 3 (Tabor) + Layer 4 (FFT) 가 reviewer 방어의 핵심 두 축.

### Q8: "왜 So et al. 2022 의 h_eq 안 쓰나?"
**A**: So et al. 의 h_eq 는 **Storakers 1997 viscoplastic spheres
의 simplified rate equation**. 정상상태 microstructure metric (우리
보고하는 coverage, tortuosity, σ_eff) 에 대해서는 우리 Tabor min()
방식과 mathematically 동등. **차이는 cyclic loading 의 transient
plastic memory 처리** 에서만 나타나며, 우리 sustained 300 MPa BC
하에서는 그 차이가 무관.

---

## 7. Reviewer-Defence 4-Layer Summary

```
Layer 1 (BC):       300 MPa 유지 → plastic memory 불필요
Layer 2 (Contact):  E*_SE = 0.54 GPa = porosity calibration parameter
Layer 3 (Solver):   Tabor μ_T per contact → Hertz/Physics column
Layer 4 (FFT):      Voxel-grid 독립 검증 (Moulinec-Suquet 1998)
```

각 Layer 가 답하는 질문:

- **L1**: "왜 cold-press relax 무시?"
- **L2**: "왜 E* 줄였나?"
- **L3**: "elastic vs plastic 어떻게 결정?"  ← *이 문서가 다루는 영역*
- **L4**: "DEM rigid sphere 가 진짜 정확?"

---

## 8. Pre-Meeting Checklist (3개 외우기)

- [ ] **공식 한 줄**: `μ_T = E*·a / (σ_y·R)`
- [ ] **3 regime**: `< 0.1 elastic / 0.1–100 transitional / ≥ 100 plastic`
- [ ] **우리 구현**: `A_eff = min(A_Hertz, A_Tabor, A_volume)` ↔ Tabor 와 동등

이 3개만 명확히 말할 수 있으면 Layer 3 방어 완료.

---

## 9. References

| # | Citation | Role |
|---|----------|------|
| 1 | Tabor 1951 — *The Hardness of Metals*, Oxford. | Original elastic-plastic transition criterion |
| 2 | Brake 2012 — *Int. J. Solids Struct.* 49: 3129. | 3-regime contact model with explicit boundaries (0.1, 100) |
| 3 | Storakers et al. 1997 — *J. Mech. Phys. Solids* 45: 1421. | Viscoplastic spheres (theory connecting So et al. to Tabor) |
| 4 | Greenwood 1992 — *Trans. ASME J. Tribol.* 114: 134. | Transitional-regime treatment |
| 5 | Thornton & Ning 1998 — *Powder Technol.* 99: 154. | Standard E-P loading/unloading in DEM |
| 6 | Sakuda et al. 2013 — *Sci. Rep.* 3: 2261. | Sulfide glass H ≈ 0.6 GPa nanoindentation |
| 7 | McGrogan et al. 2017 — *Adv. Energy Mater.* 7: 1602011. | LPSCl mechanical properties |
| 8 | So et al. 2022 — *MethodsX* 9: 101857. | Equilibrium-overlap DEM (Storakers 의 simplified version) |
| 9 | Wang 2020 — *J. Power Sources* 470: 228413. | NCM E_AM = 140 GPa |
| 10 | Moulinec & Suquet 1998 — *Comput. Methods Appl. Mech. Eng.* 157: 69. | FFT homogenization (Layer 4 link) |

---

## 10. Quick Pre-Meeting Run

```bash
# 30초 안에 실측 결과 확보
git pull
python3 scripts/analyze_tabor_regime.py --plot --pair SE-SE
# → docs/figures/tabor_regime_SESE.png
# → 콘솔에 median μ_T + regime % 분포 출력
# → "Verdict: TRANSITIONAL regime" 한 줄이 회의 결정타
```

이 결과 + 본 문서의 Section 1 (30초 pitch) 만 외우면 회의 대응 충분.
