# Section 2 — Bader Charge Cross-Composition: 4 Trends + 3 Anomaly Fingerprints + Br Effect on PS₄

> [!info] Status
> **Final Deep Dive** — comp2 v2 (post-anneal) Bader 정확값 확보 (Apr 30 2026).
> ==NEW finding== Br doping → **PS₄ covalent backbone 강화** (+0.207 e on P, +6.8% Coulomb).

---

## 2.1 왜 Bader charge가 mechanical property와 관련 있나

**Coulomb energy ↔ bond stiffness 직접 연결**:

```
E_Coul = (1/4πε₀) · q₁q₂/r
F = -∂E/∂r ∝ q₁q₂/r²
k = -∂F/∂r ∝ q₁q₂/r³    ← bond stiffness
```

> [!example] 논리 chain
> **Bader q (atomic) → q×|q|/r (bond pair) → bond stiffness → C_ij → B0/E**

**핵심 metric**: `q×|q|/r` (e²/Å, ×14.4 → eV) — *bond strength proxy*. 6 composition 전체 정확 계산됨.

---

## 2.2 Cross-composition Bader table (모든 anchor 확정)

| Comp | Li | P | S | Cl | Br | Family | Source |
|---|---|---|---|---|---|---|---|
| comp1 v1 | +0.874 | +4.396 | -1.518 | -0.925 | — | Li6 | DFT v1 |
| **comp1 v2** | **+0.877** | **+4.686** | **-1.807** | **-0.914** | — | **Li6** | DFT anneal V0 ⭐ |
| comp2 v1 | +0.873 | (~+4.4) | -1.843 | -0.925 | -0.840 | Li6 | DFT v1 BasinB |
| ⭐ **comp2 v2** | **+0.876** | ==**+4.893** ⬆== | **-1.850** | **-0.910** | **-0.891** | **Li6** | DFT anneal V0 (v103) |
| comp3 v1 | +0.880 | (~+4.4) | -1.760 | -0.903 | -0.915 ⚠️ | Li5.4 | DFT v1 |
| comp4 v1 | +0.853 | (~+4.4) | -1.551 ⚠️ | -0.884 | -0.882 | Li5.4 | DFT v1 |
| comp5 v1 | +0.879 | (~+4.4) | -1.752 | -0.913 | -0.896 | Li5.4 | DFT v1 |
| modelC v1 | +0.857 | +4.396 | -1.728 | -0.886 | — | Li5.4 | DFT v1 |
| **modelC v2** | **+0.883** | **+4.340** ⬇ | **-1.736** | **-0.918** | — | **Li5.4** | DFT anneal V0 ⭐ |

> [!note]
> **Bold = paper #1 main 인용 anchor (P 직접 측정)**

> [!star] 3개 P anchor — paper #1 narrative 핵심
> - `comp1 v2` P = **+4.686** (Li6, Cl-only) — *baseline*
> - `comp2 v2` P = **+4.893** (Li6, Cl/Br mixed) — ==NEW Br 효과== ⭐
> - `modelC v2` P = **+4.340** (Li5.4, Cl-only, vacancy)

---

## 2.3 4 Trends — 정량 + 메커니즘

### Trend 1: Li ionicity ← *family-invariant* (~+0.87)

```
Li6:    comp1 v2 +0.877, comp2 v2 +0.876
Li5.4:  modelC v2 +0.883, comp3 +0.880, comp5 +0.879, comp4 +0.853 (lowest)
```

- **Vacancy alone** 은 Li donating efficiency에 큰 영향 없음
- Anneal로 +0.02 e 회복 (modelC v1 +0.857 → v2 +0.883)
- **comp4 +0.853 lowest** = mixed Cl/Br + vacancy *frustration*

---

### Trend 2: Cl ionicity ← *Br dilution*

```
Cl-only:        modelC v2 (-0.918, Cl=1.6) > comp1 v2 (-0.914, Cl=1.0)
Cl+Br mixed:    comp2 v2 (-0.910), comp5 (-0.913), comp3 (-0.903), comp4 (-0.884)
```

- **Cl-rich + dense** (modelC, Cl 1.6/fu): Madelung field 가장 강함 → strongest ionic
- **Br 도입** → charge competition → Cl 약화
- **comp4** (mixed 50:50) 가장 약함 = *maximum frustration*

---

### Trend 3: P cationicity — vacancy AND Br 두 효과 분리 ==(NEW)==

> [!important] 3-point comparison (정확 측정 anchor만)
> ```
> comp1 v2 (Li6, Cl-only):     P = +4.686   ← baseline
> comp2 v2 (Li6, Cl+Br):       P = +4.893   ← +0.207 e (Br alone, +4.4%)
> modelC v2 (Li5.4, Cl-only):  P = +4.340   ← -0.346 e (vacancy alone, -7.4%)
> ```

**두 변수가 P에서 reverse**:
- **Vacancy → P 약화** (PS₄ covalent backbone 약화)
- **Br → P 강화** (PS₄ covalent backbone 강화)

> [!quote] Br 효과 메커니즘 ==(NEW finding)==
> - Br radius +8% (1.96 vs 1.81 Å) → *lattice expansion* (a₀ +0.6%)
> - Br의 큰 polarizability → 인접 PS₄ environment의 local field 변화
> - PS₄가 Br로 둘러싸이면 더 polarized → P→S transfer 더 efficient
> - 즉 ==**Cl 약화는 Br의 ionic side, P 강화는 covalent side**== (anti-correlation)

**Cross-product prediction** (Li5.4 + Cl/Br):
- `comp1 + vacancy + Br = 4.686 - 0.346 + 0.207 =` **+4.547** *(예측)*
- comp3/4/5 P 정확 측정시 검증 필요 (~+4.4 추정 in line)

---

### Trend 4: Cl/Br ionicity ratio — anneal로 정상 trend 회복

| Comp | \|q(Cl)\| | \|q(Br)\| | Cl > Br? |
|---|---|---|:-:|
| `comp2 v1` | 0.925 | 0.840 | ✅ +10% (anneal 전, 큰 차이) |
| **`comp2 v2`** | **0.910** | **0.891** | ✅ +2.1% (anneal 후, 차이 줄어듦) |
| `comp3 v1` | 0.903 | 0.915 | ❌ Br 더 ionic (-1.3%) ⚠️ |
| `comp4 v1` | 0.884 | 0.882 | ≈ same |
| `comp5 v1` | 0.913 | 0.896 | ✅ +1.9% |

> [!tip] comp2 anneal 효과
> Br ordering 개선 → Br effective ionic +0.051 e 증가, Cl 약간 감소 (+0.015 e). **Cl/Br 차이 균등화.**

> [!warning] comp3 anomaly
> anneal 전 *site disorder*. v2 anneal하면 정상 복귀 가능 (`TODO`).

---

## 2.4 Anomaly fingerprints — 3개 정량

### ⚠️ Anomaly 1 — comp3 Br > Cl ionicity (Trend 4)

> [!warning]
> - **Origin**: Site disorder + minority anion strong-field effect (anneal 전)
> - **Likely fix**: comp3 v2 anneal (comp2 v1→v2 사례 입증)

### ⚠️ Anomaly 2 — comp4 S charge unusually low (-1.551)

> [!warning]
> - 다른 comp들: |q(S)| = **1.74 ~ 1.85**
> - comp4: |q(S)| = **1.551** (Δ −0.20 e, ==−12%==)
> - **Origin**: Cl=0.8/Br=0.8 *maximum frustration* → S charge "smeared"
> - **Paper 활용**: comp4 mechanical 약화 (E ↓ 9%) ↔ Li-S q²/r −17% **직접 연결**

### ⚠️ Anomaly 3 — comp2 v2 P unusually high (+4.893) ==(NEW)==

> [!star]
> - 다른 v2 anchor: comp1 v2 P=+4.686, modelC v2 P=+4.340
> - **comp2 v2: P = +4.893** *(가장 높음)*
> - **Origin**: Br 도입이 PS₄ covalent backbone 강화 (lattice expansion + polarizability)
> - **Paper 활용**: ==Br의 양면 효과== (ionic Cl 약화 + covalent P 강화) → 두 효과 *partial cancellation* = mechanical net 변화 작아 보이는 이유

---

## 2.5 Bond Strength Proxy (q×|q|/r) — 정량

### 5-comp 합산표 *(e²/Å × 14.4 = eV)*

| Bond | comp1 v2 | ⭐ comp2 v2 | comp2B v1 | comp3 v1 | comp4 v1 | comp5 v1 |
|---|---|---|---|---|---|---|
| **P-S** | 59.0 | ==**63.3** ⬆== | — | — | — | — |
| Li-Cl | 4.64 | 4.69 | 4.45 | 4.56 | 4.32 | 4.69 |
| Li-Br | — | 4.46 | 4.19 | 4.22 | 4.00 | 4.16 |
| Li-S | 9.13 | 9.31 | 9.40 | 8.86 | ==**7.57** ⬇== | 8.99 |

> [!important] 핵심 비교
> - `comp2 v2 P-S = 63.3 eV` vs `comp1 v2 P-S = 59.0 eV` → ==**+7.3% (Br effect on PS4)**==
> - `comp2 v2 P-S` vs `modelC v2 P-S = 52.5` → ==**+20.2%**== (Br + no-vacancy combined)
> - **comp4 Li-S = 7.57** (lowest) — *S charge anomaly의 mechanical 직결*

### Cl vs Br (anneal 후)

| Comp | Li-Cl | Li-Br | Cl > Br |
|---|---|---|:-:|
| **comp2 v2** | 4.69 | 4.46 | ✅ +5.2% |
| comp2B v1 | 4.45 | 4.19 | ✅ +5.9% |
| comp3 v1 | 4.56 | 4.22 | ✅ +7.5% |
| comp4 v1 | 4.32 | 4.00 | ✅ +7.4% |
| comp5 v1 | 4.69 | 4.16 | ✅ ==+11%== |

→ **q²/r metric**으로는 Cl bond 항상 더 strong (comp3 anomaly가 q²/r에서 평균화).

---

## 2.6 PS₄ polarization deep dive — 두 효과 분리

### Vacancy alone (`comp1 v2 → modelC v2`)

```
P (Bader)    +4.686 → +4.340    Δ -0.346 e (-7.4%)
S (Bader)    -1.807 → -1.736    Δ +0.071 e
P-S q×|q|/r  4.11 e²/Å → 3.66   Δ -11%
```

> [!fail] vacancy → PS₄ ==**−11% softer**==

### Br alone (`comp1 v2 → comp2 v2`) ==(NEW)==

```
P (Bader)    +4.686 → +4.893    Δ +0.207 e (+4.4%)
S (Bader)    -1.807 → -1.850    Δ -0.043 e
P-S q×|q|/r  4.11 e²/Å → 4.39   Δ +6.8%
```

> [!success] Br → PS₄ ==**+6.8% stiffer**== *(anti-trend!)*

### Combined prediction

- vacancy(−11%) + Br(+6.8%) = **net −4.2%** in Li5.4 + Cl/Br systems
- 실측 (comp3-5) **Wad 2× 증가**는 Bader 단일 원자로 안 풀림 → *collective surface* (Section 2.7)

### B0 macroscopic 영향

> [!quote] PS₄ Coulomb 분석
> - ΔB0/B0 (comp1 → modelC) = **−26%**
> - PS₄ q²/r 손실 −11% × 4 P-S × 6 S-S = ~**−10% 합산**
> - **PS₄ Coulomb이 ΔB0의 1/3 설명**, 나머지 2/3 = *phonon entropy* (Section 3 후보)

---

## 2.7 Wad paradox — Bader로 설명 가능한가?

> [!fail] No.

```
            comp1 v2 (Li6)     comp3 v1 (Li5.4)
Wad         1.2 J/m²           2.0 J/m²       (2×!)
Bader Li    +0.877             +0.880         (같음)
Bader Cl    -0.914             -0.903         (거의 같음)
Bader S     -1.807             -1.760         (거의 같음)
```

**Bader 단일 원자로 Wad 2× 설명 불가능**.
ΔE_Coul/m² ~ 0.1–0.3 J/m² < ==실측 0.8 J/m²==.

> [!summary] Wad는 collective surface mechanism
> 1. **Surface termination 자유도** (vacancy 가까운 surface easier reorganization)
> 2. **Surface vacancy = NCM anchor** (구조적, charge 아님)
> 3. **NCM cohesion vacancy compatibility**

→ **Section 4 후보** (surface analysis).

---

## 2.8 Anneal 효과 정량 ==(NEW from comp2 v1 → v2)==

```
comp2 v1 → v2:
  Li:  +0.873 → +0.876   Δ +0.003 e   (거의 동일)
  Cl:  -0.925 → -0.910   Δ +0.015 e   (약화)
  Br:  -0.840 → -0.891   Δ -0.051 e   (강화, ordering 회복)
  S:   -1.843 → -1.850   Δ -0.007 e   (거의 동일)
  P:    ~+4.4  → +4.893  Δ +0.493 e   (P 측정값 v2에서 처음 정확)
```

- **Cl/Br ionicity 차이 균등화** (Br ordering 개선)
- **PS₄ polarization 강화**

> [!tip] paper #1 narrative
> v1 → v2 anneal이 **atomic-level에서도 measurable 변화**.

---

## 2.9 narrative arc 연결

```
Section 1 (시스템 설계: 6 compositions, modelC keystone)
   ↓
Section 2 (Bader Cross-Comp — 지금)
   ↓
   ✓ 4 trends + 3 anomaly fingerprints
   ✓ Br의 양면 효과 (NEW: P +0.207 e, Cl -0.005 e)
   ✓ Vacancy effect on PS4 (-0.346 e, -11% q²/r)
   ✓ Wad paradox unresolved → Section 4
   ↓
Section 3 (다음) — Mechanical trends:
   - B0/E/Cij cross-comp + 600K reversal
   - q×|q|/r vs B0 scatter (R² 검증)
   - Br의 ionic↓/covalent↑ → mechanical net 작은 변화 설명
   - comp4 S↓ → Li-S q²/r -17% → mechanical 약화 origin
```

---

## 2.10 한 줄 요약

> [!summary] Section 2 TL;DR
> 6개 composition × Bader 분석에서 ==**4 trends + 3 anomaly fingerprints + anneal 효과**== 확인.
> ==**새 핵심 발견**==: comp2 v2 P=+4.893 > comp1 v2 P=+4.686 = **Br 도입이 PS₄ covalent backbone 강화** (+0.207 e, +6.8% Coulomb stiffness).
> Vacancy 효과(−7.4% P)와 Br 효과(+4.4% P)가 PS₄에서 ==reverse==.
> 두 효과 *partial cancellation* 이 mechanical net 변화 작아 보이는 이유.
> **comp4 S anomaly (−0.20 e)** = mechanical 약화의 microscopic origin.
> ==**Wad paradox는 Bader로 안 풀림**== → collective surface mechanism (Section 4).
> q×|q|/r metric이 **Section 3에서 mechanical trend 직접 plot 입력**.

---

## Data sources

- DB: `db/compositions/comp1.json` ~ `comp5.json`, `modelc.json`
- Cross-table: `db/properties/electronic.json`
- Working pipeline: `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/run_comp1v2_postproc.sh` *(paper #1 reference)*
- comp2 v2 ACF.dat: `/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/ACF.dat`

---

#paper1 #bader #cross-composition #PS4-polarization #Br-effect #vacancy-effect #wad-paradox #anneal-effect
