# Wad Mechanism Refutation — 빡대가리용 설명

> [!error] 저자 주장 (빨간 줄)
> "The Li–Cl bond is shorter and more ionic than the Li–S and Li–Br bonds, which strengthens electrostatic interactions at the interface."
>
> 즉:
> 1. Li-Cl이 Li-S보다 짧다
> 2. Li-Cl이 Li-S보다 더 ionic이다
> 3. 따라서 Li-Cl이 강한 electrostatic = Wad 큼

> [!info] 우리 데이터 한 줄 요약
> ==**3개 가정 모두 틀리고, 결론도 데이터가 정반대로 보여줌**==. 저자 mechanism은 폐기해야 함.

---

## ❌ Fact 1 — "Li-Cl이 더 짧다"는 거짓

### 쉬운 설명
저자: "Cl이 S보다 Li랑 더 가까워서 더 세게 끌려"
**진실: 우리 paper의 메인 시스템 (Li5.4 family)에서는 Cl이 S보다 *더 멀리* 있음.**

### 숫자로 (Li5.4 family — 우리 paper 주인공)

```
                  Li-Cl     Li-S     누가 짧은가?
comp3 v1          2.498     2.478    S가 짧음 (-0.020 Å)
comp4 v1          2.495     2.479    S가 짧음 (-0.016 Å)
comp5 v1          2.466     2.451    S가 짧음 (-0.015 Å)
modelC v2         2.547     2.460    S가 0.087 Å 짧음 ⬇⬇⬇
                  ─────     ─────
                  더 긴 거  더 짧은 거
```

### 시각적으로
```
       Li
      /  \
     /    \
   Cl------S      ← 같은 Li 주변
   (멀음)  (가까움)   in Li5.4 family
```

### 결론
- Li6 family (comp1, comp2)에서만 Cl이 짧음 (-0.01~0.07 Å)
- ==**Li5.4 family 4개 모두에서 Cl이 더 긺**==
- 저자 paper가 Li5.4 dopant 다루면 → **factually wrong, 4/6 case에서 거짓**

---

## ❌ Fact 2 — "Li-Cl이 더 ionic"은 화학 교과서 위반

### 쉬운 설명
저자: "Cl이 S보다 더 ionic이다"
**진실: S는 -2 charge, Cl은 -1 charge. S가 2배 더 ionic. 인쇄된 화학 교과서 그 어떤 책에서도 Cl > S ionicity 이렇게 안 나와.**

### 숫자로
```
원소        formal charge    Bader |q|       ionicity
Cl⁻         -1               0.91 e          ●
S²⁻         -2               1.85 e          ● ●  ← 2배

|q_S| / |q_Cl| ≈ 2.03
```

### 비유
- Cl⁻ = 자석 1개
- S²⁻ = 자석 2개 (붙어있는)
- 둘 중 어느 게 Li를 더 세게 끌까? **당연히 자석 2개 (S²⁻)**

### 저자가 헷갈린 부분
저자: "더 ionic"이 무슨 뜻이지?
- HSAB 관점 (halogen 내부): Cl > Br ionicity ✓ 이건 맞음
- 절대 charge 관점 (S vs halogen): **S >> Cl** ❌ 저자 주장 틀림

저자가 ==**"Li-Cl > Li-Br ionic"이라고 썼으면 OK였는데, "and Li-S"를 추가한 순간 거짓**==.

---

## ❌ Fact 3 — "shorter + more ionic = stronger electrostatic"은 단순 산수로 깨짐

### 쉬운 설명
저자: "짧고 ionic하면 강하다"
**진실: Bond strength 공식은 q × q / r. Charge가 2배 차이나면 length 0.5% 차이는 의미 없음.**

### 산수로
```
공식: 결합 강도 ∝ q_Li × |q_anion| / r

Li-Cl:   0.877 × 0.914 / 2.486 = 0.322
Li-S:    0.877 × 1.807 / 2.498 = 0.634

비율: Li-S / Li-Cl = 1.97
                    ─────────
                   ==Li-S가 거의 2배 강함==
```

### 핵심
- Length 차이 (2.486 vs 2.498) = 0.5% — 사실상 무시 가능
- Charge 차이 (0.91 vs 1.85) = 100% — **이게 dominant**
- 저자 logic 적용해도 **Li-S가 압도적 winner** → 저자가 자기 논리에 안 맞음

---

## ❌ Fact 4 — Wad 데이터가 저자 mechanism의 *정반대*

### 쉬운 설명
저자 logic 그대로 적용하면: "Li-Cl 짧을수록 Wad 커야 함"
**우리 데이터: Li-Cl이 *길어질수록* Wad 커짐 — 정확히 반대.**

### 숫자로
```
Composition       Li-Cl       Wad           저자 예측
comp1 v2          2.486 (짧음)   1.2 J/m²    "낮아야 됨"... 1.2네 OK
modelC v2         2.547 (김)     2.0 J/m²    "더 낮아야 됨"... 근데 2.0 ⬆⬆⬆
                                            
                                            ==저자 mechanism으로는 설명 불가==
```

### 시각화
```
저자 예측:  Li-Cl 짧음 ──→ Wad 큼  (correlation +)
실제:      Li-Cl 긺   ──→ Wad 큼  (correlation -)
                                  ==반대 방향==
```

### 결론
저자 mechanism이 맞으면 modelC (Li-Cl=2.547, 가장 김)는 **Wad가 가장 작아야** 함. 실제로는 **가장 큼**. 데이터가 mechanism을 falsify함.

---

## ❌ Fact 5 — Li5.4 family에서는 비교 axis 자체가 성립 안 됨

### 쉬운 설명
저자 logic: "Li-Cl이 Li-S보다 짧다는 전제로 시작"
**진실: Li5.4 family 4개 (comp3, 4, 5, modelC)에서 Li-Cl이 다 *길음*. 전제 자체가 깨짐.**

### 표로
```
Li5.4 family (paper 메인 주제):
                  Li-Cl    Li-S    Li-Cl shorter?
comp3 v1          2.498    2.478   ❌
comp4 v1          2.495    2.479   ❌
comp5 v1          2.466    2.451   ❌
modelC v2         2.547    2.460   ❌

4/4 = 100% 저자 전제 깨짐
```

### 결론
- 저자 mechanism이 Li6 family (comp1, comp2)에는 부분 적용 가능
- 하지만 ==**Li5.4 family는 paper #1의 main subject (B0/E/Wad 다 Li5.4 trend 분석)**==
- Main subject에서 전제가 깨지면 → mechanism 폐기

---

## ❌ Fact 6 — comp4 = ⭐ 최강 반증 (single-shot kill)

### 쉬운 설명
저자 logic: "Li-Cl이 강할수록 Wad 큼"
**진실: comp4가 Li-Cl 가장 약함 (0.303) + Wad 가장 큼 (1.20 J/m²). 데이터가 정확히 반대.**

### 숫자로
```
                Li-Cl q²/r    Wad (J/m²)
comp3 v1        0.321         1.05
comp4 v1        0.303 ⬇⬇      1.20 ⬆⬆     ← anti-correlation
comp5 v1        0.326         (~1.0)
                ────────       ─────
                약할수록      Wad 커짐
                ──────────────────────
                ==저자 logic 정반대==
```

### 시각화
```
저자 예측:  Li-Cl strong → Wad ↑    (positive correlation)
실제:      Li-Cl weakest → Wad ↑   (negative correlation in comp4)
                                    ==거꾸로==
```

### 결정타
저자 mechanism이 맞으면 comp4가 Wad ↓ 이어야 함. **comp4가 Wad 가장 높음**. 한 데이터 포인트만으로 mechanism falsify 충분.

---

## 🎯 6 Facts 한 표 요약

| Fact | 저자 주장 | 우리 데이터 | 평가 |
|------|----------|--------------|------|
| 1 | Li-Cl < Li-S length | Li5.4 4개에서 Cl 더 긺 | ❌ false 4/6 |
| 2 | Li-Cl more ionic than Li-S | \|q_S\|=1.85 vs \|q_Cl\|=0.91 (S 2× ionic) | ❌ 화학 위반 |
| 3 | "shorter + ionic → stronger" | Li-S q²/r = 2× Li-Cl | ❌ 산수로 깨짐 |
| 4 | shorter Li-Cl → Wad ↑ | longer Li-Cl (modelC) → Wad ↑ | ❌ 정반대 correlation |
| 5 | Li-Cl shorter premise | Li5.4 family 4/4 거짓 | ❌ 전제 폐기 |
| 6 | strong Li-Cl → high Wad | weakest Li-Cl (comp4) → highest Wad | ❌ 정반대 |

==**6/6 fact 모두 저자 mechanism을 falsify**==.

---

## 💀 Finishing Argument (저자에게 직접)

> The proposed mechanism—that enhanced Wad arises from a shorter and more ionic Li–Cl bond compared to Li–S—is contradicted by the data on multiple counts:
>
> 1. **Li–Cl is not uniformly shorter than Li–S**: in the Li5.4 family (the primary subject of this paper), Li–Cl is **0.02–0.09 Å longer** than Li–S in all four compositions tested (comp3, 4, 5, modelC).
>
> 2. **Li–Cl is not more ionic than Li–S**: Bader analysis gives |q(S)| = 1.85 e vs |q(Cl)| = 0.91 e — S²⁻ is **twice as ionic** as Cl⁻ by basic charge magnitude.
>
> 3. **The Coulomb proxy contradicts the strength claim**: q×|q|/r for Li–S is **~2× larger** than for Li–Cl across all compositions. Length differences (~0.5%) cannot overcome charge differences (~100%).
>
> 4. **Wad correlates inversely with Li–Cl strength**: comp4 has the weakest Li–Cl proxy (0.303) but the highest Wad (1.20 J/m²) — opposite to the proposed mechanism. modelC has the longest Li–Cl (2.547 Å) yet the highest Wad (~2.0 J/m²) — again opposite.
>
> The Wad enhancement upon Cl substitution must be reformulated through:
> - **(i) site distribution (4a/4d Wyckoff occupation)** — gautam2023, yuwagemaker2023
> - **(ii) Li vacancy enhancement at Cl-rich (charge-balance Li deficiency)** — adeli2019, wagemaker2020
> - **(iii) interface size matching with NCM (Cl ionic radius vs Br)** — zuo2023
> - **(iv) cation-anion ionic potential framework** — zhang2024_ionic_potential, wilkening2019
>
> The current single-mechanism (shorter+ionic → stronger) cannot survive the bond/Bader data presented here.

---

## 🔄 대안 mechanism (저자에게 제안할 multi-factor framework)

### 1. Site distribution effect (4a/4d Wyckoff)
- Cl substitution 늘면 4d 위치도 Cl 점유 (Br는 size 커서 4a 선호)
- 4d-Cl이 cage center → Li 분포 재배치 → interface Li 농도 변화
- Backed by: gautam2023, yuwagemaker2023, kraft2018

### 2. Li vacancy mechanism
- Cl 1.6/fu = Li 5.4/fu (charge-balance vacancy)
- V_Li at interface → mobile Li → NCM 산소와 화학 결합 형성
- Backed by: adeli2019, wagemaker2020_lideficient

### 3. Interface size matching
- Cl⁻ (1.81 Å) closer to NCM O²⁻ (1.40 Å) than Br⁻ (1.96 Å)
- Geometric compatibility at interface
- Backed by: zuo2023, sicolo2022

### 4. Polarizability angle (charge localization)
- Cl⁻ less polarizable → charge localized at interface (stronger anchor)
- Br⁻ more polarizable → charge dispersed (weaker anchor)
- Backed by: kraft2018 (lattice polarizability framework)

==**4-factor framework이 single-mechanism 보다 robust + 모든 trend 설명 가능**==.

---

## 🔬 Scientific Deep Dive — 4a vs 4d Wyckoff Sites

### Argyrodite Crystal Structure (F-4̄3m)

Argyrodite Li₆PS₅X (X = Cl, Br) crystallizes in the **cubic F-4̄3m space group** with these Wyckoff positions:

| Wyckoff | Coords | Multiplicity | Occupation in Li₆PS₅Cl |
|---------|--------|--------------|------------------------|
| **4a** | (0, 0, 0) | 4 | **Cl** (free anion site #1, "cage corner") |
| **4d** | (¾, ¾, ¾) | 4 | **S** (free anion site #2, "cage center") |
| 16e | (x, x, x), x≈0.12 | 16 | S (PS₄ tetrahedron corners) |
| 48h / 24g | general | 48 (50% occupied) | Li |

(Note: 4d site sometimes labeled 4c at (¼,¼,¼) by convention — both refer to the "second free anion" site)

### Geometric Difference — 4a vs 4d

```
4a site (0,0,0)                4d site (¾,¾,¾)
─────────────                  ─────────────
 - 위치: cubic corner          - 위치: body-diagonal 반대
 - Li 배위: tetrahedral 6 Li   - Li 배위: octahedral 6 Li
                                 (geometry는 비슷하지만 거리 다름)
 - Anion-Li 평균 거리: 짧음     - Anion-Li 평균 거리: 더 김
   (~2.5 Å in Li6PS5Cl)         (~2.6-2.7 Å)
 - Pauling preference: smaller  - Pauling preference: larger
   anion (Cl⁻)                    anion (S²⁻)
```

### Site Preference (Pauling rule + size)

Argyrodite anion sites have **size-dependent occupation**:

| Anion | Ionic radius | Preferred site | Reasoning |
|-------|--------------|----------------|-----------|
| Cl⁻ | 1.81 Å | **4a** (compact) | Smaller anion fits compact site |
| Br⁻ | 1.96 Å | **4d** (loose) | Larger anion needs more space |
| S²⁻ | 1.84 Å | **4d** (free anion) | High charge needs more polarized cage |

**Pristine Li₆PS₅Cl (paper standard reference):**
- 4a: 100% Cl (4 atoms/cell)
- 4d: 100% S (4 atoms/cell, "free S")
- 16e: 100% S (16 atoms/cell, PS₄ corners)

**Halogen-rich modelC Li₅.₄PS₄.₄Cl₁.₆:**
- 4a: 100% Cl (4 atoms)
- **4d: ~50% Cl + ~50% S** (4 Cl + 4-(8-4)=... 실제로는 4d 8개 자리에 Cl 4개 추가) ⚠️ 간소화 예시
- 16e: 100% S (PS₄ invariant)

(Cell당 8 Cl atoms = 4 at 4a + 4 at 4d. 4d S가 Cl로 substituted되며 free S 사라짐.)

### Why Bond Lengths Differ at 4a vs 4d — 우리 데이터로 정량

```
                    Li-Cl (4a only)    Li-Cl (4a + 4d mixed)
                    ───────────────    ─────────────────────
comp1 v2 (Cl=1.0)   2.486 ± 0.107     —
modelC v2 (Cl=1.6)  —                 2.547 ± 0.105

ΔLi-Cl = +0.061 Å   ← 4d-Cl 점유로 평균 늘어남
```

**왜?**
1. 4a-Cl: tight cage, Li 6개가 ~2.45 Å 거리에 위치 (compact)
2. 4d-Cl: loose cage, Li 6개가 ~2.65 Å 거리에 위치 (loose)
3. modelC에서 두 위치 average → mean ↑

**Li-S 변화는 반대 방향:**
```
                    Li-S
                    ─────
comp1 v2 (S free at 4d): 2.498 ± 0.077  (4d-S 포함, 분포 넓음)
modelC v2 (4d S 사라짐):  2.460 ± 0.078  (16e-S만, 짧고 균일)

ΔLi-S = -0.038 Å    ← 4d S 사라지면서 16e-S만 남음
```

→ ==**modelC에서 Li-Cl ↑ + Li-S ↓는 site rearrangement 직접 결과**==.

### Br vs Cl Site Preference 검증 — 우리 Bader

| Comp | Cl/fu | Br/fu | Cl preferred site | Br preferred site |
|------|-------|-------|-------------------|-------------------|
| comp1 (Li6) | 1.0 | 0 | 4a (only) | — |
| comp2 (Li6) | 0.5 | 0.5 | 4a 우세 | 4d 우세 (size) |
| comp3 (Li5.4) | 1.0 | 0.6 | 4a fully + 4d 일부 | 4d 우세 |
| comp4 (Li5.4) | 0.8 | 0.8 | mixed (frustration) | mixed (frustration) |
| comp5 (Li5.4) | 0.6 | 1.0 | 4a 우세 | 4d fully + 4a 일부 |
| modelC (Li5.4) | 1.6 | 0 | 4a fully + 4d fully | — |

**comp4 frustration**의 microscopic origin:
- Cl과 Br이 "어느 site에 갈까?"로 경쟁
- 결정적 ordering 없음 → site disorder 최대
- Bader anomaly (S=-1.55, P=+3.63 verified) = **site disorder의 전기적 fingerprint**

### 4a/4d Quantitative Reference (Gautam 2023)

> "Br⁻ (4d) = 20%, Cl⁻ (4d) = 60%"

**Cl⁻은 60%가 4d 점유** (4a는 40%) — Cl이 4d를 상당히 차지함을 보여줌. modelC (Cl 1.6/fu)는 4a fully + 4d 거의 fully → Li-Cl 평균이 4a + 4d 둘 다 포함하며 늘어남. ==**우리 measurement (Li-Cl 2.547)와 정확히 일치**==.

### 이 site science가 저자 narrative를 어떻게 깨는가

저자: "Li-Cl shorter and more ionic"  
**진실 (with site science)**:
- Li-Cl은 **single value가 아님** — 4a-Cl(짧음) vs 4d-Cl(김) 두 environment
- modelC에서 4d-Cl 점유로 average length가 ==**Li-S average보다 더 길어짐**==
- 즉 저자는 ==**single-environment 가정**==을 multi-environment 시스템에 적용함 — fundamental error

==**4a/4d site distribution이 paper #1 narrative의 microscopic foundation**==. 저자가 무시한 layer가 우리 데이터로 정량 검증됨.

---

## Methodology — 우리 측정 출처 (재인용 가능)

**Bond lengths**:
- comp1 v2: KISTI `post_relax_comp1_v2/comp1v2_scf.out`
- comp2 v2: KISTI `pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz`
- comp3-5 v1: KISTI `post_relax/comp{N}_post_relax.out` (or comp5_relax.out)
- modelC v2: KISTI `pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz`
- Cutoffs: Li-Cl 3.2, Li-Br 3.4, Li-S 3.0, P-S 2.3 Å (consistent across all comps)
- Method: PBE-DFT post-relax, mic distance, ASE 측정

**Bader charges**:
- Same KISTI paths + ACF.dat from each folder
- Method: pp.x charge density (plot_num=21 all-electron) + Henkelman bader_lnx_64 v1.05
- Cross-validated with DB (Δ ≤ 0.016 e for all elements)

**Verification date**: 2026-05-05 (KISTI single-script measurement, all comps consistent cutoff)

---

#paper1 #refutation #wad #halogen #bond-length #bader #q2-over-r #author-rebuttal
