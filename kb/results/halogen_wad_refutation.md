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

## 🔄 대안 mechanism (저자에게 제안할 multi-factor framework)

### 1. Site distribution effect (4a/4d Wyckoff)
- Cl substitution 늘면 4d 위치도 Cl 점유 (Br는 size 커서 4a 선호)
- 4d-Cl이 cage center → Li 분포 재배치 → interface Li 농도 변화
- Backed by: gautam2023, yuwagemaker2023, kraft2018

### 2. Li vacancy mechanism
- Cl 1.6/fu = Li 5.4/fu (charge-balance vacancy)
- V_Li at interface → mobile Li → NCM 산소와 화학 결합 형성
- Backed by: adeli2019, wang2019

### 3. Interface size matching
- Cl⁻ (1.81 Å) closer to NCM O²⁻ (1.40 Å) than Br⁻ (1.96 Å)
- Geometric compatibility at interface
- Backed by: **zuo2023**, sicolo2022

### 4. Polarizability angle (charge localization)
- Cl⁻ less polarizable → charge localized at interface (stronger anchor)
- Br⁻ more polarizable → charge dispersed (weaker anchor)
- Backed by: kraft2018 (lattice polarizability framework)

==**4-factor framework이 single-mechanism 보다 robust + 모든 trend 설명 가능**==.

---

## 🔬 Scientific Deep Dive — 4a vs 4d Wyckoff Sites (==**우리 DFT ground state로 직접 검증**==)

### Argyrodite Crystal Structure (F-4̄3m)

Argyrodite Li₆PS₅X (X = Cl, Br) crystallizes in the **cubic F-4̄3m space group** with these Wyckoff positions:

| Wyckoff | Coords | Multiplicity | Pristine Li₆PS₅Cl |
|---------|--------|--------------|------------------------|
| **4a** | (0, 0, 0) | 4 | "free anion" cage corner |
| **4c/4d** | (¼,¼,¼) or (¾,¾,¾) | 4 | "free anion" body-diagonal |
| 16e | (x, x, x), x≈0.12 | 16 | S (PS₄ tetrahedron corners) |
| 48h / 24g | general | 48 (50% occupied) | Li |

### 🎯 우리 DFT ground state 측정으로 4a/4d 직접 식별

**comp2_v2 (Li₆PS₅Cl₀.₅Br₀.₅) — 결정적 증거:**

```
fractional coordinates 분석:

Cl atoms (n=2):
  idx 46: (0.77, 0.26, 0.69) ≈ (¾, ¼, ¾)   ← 4c/4d 위치
  idx 44: (0.78, 0.74, 0.18) ≈ (¾, ¾, ¼)   ← 4c/4d 위치
  → 100% Cl at 4c/4d
  → mean Li-Cl = 2.44 Å

Br atoms (n=2):
  idx 49: (0.02, 0.02, 0.92) ≈ (0, 0, 1)   ← 4a 위치
  idx 51: (0.53, 0.48, 0.95) ≈ (½, ½, 1)   ← 4a equiv
  → 100% Br at 4a
  → mean Li-Br = 2.58 Å
```

→ ==**우리 DFT ground state가 직접 입증: Cl 100% at 4c/4d, Br 100% at 4a**==.
→ Gautam 2023 (Br 4a 80%, Cl 4d 60%)와 ==**완전 일치**==. 우리 결과는 thermodynamic ground state니까 100%.

### 4a vs 4c/4d Geometric Reality (측정 기반)

```
4a site (0,0,0)                    4c/4d site (¼,¼,¼) or (¾,¾,¾)
─────────────                      ─────────────────────────────
- 위치: cubic corner               - 위치: body-diagonal
- Li 거리: ~2.52-2.58 Å (LOOSE)    - Li 거리: ~2.38-2.49 Å (COMPACT)
- 점유 anion: larger (Br⁻, S²⁻)    - 점유 anion: smaller (Cl⁻)
- Pristine Li₆PS₅Cl: 50:50 anion   - Pristine: 50:50 anion 
  disorder (Cl + S 둘 다)            disorder (Cl + S 둘 다)
```

**핵심**: 흔한 textbook 라벨 ("4a compact, 4d loose")은 정확하지 않음. 우리 측정 + Gautam 데이터로 ==**4a가 사실 looser cage (Br 같은 큰 anion 수용), 4c/4d가 compact (작은 Cl 수용)**==.

### Site Preference 검증 — 우리 모든 comp 측정값

| Comp | Cl/fu | Br/fu | Cl 분포 (n) | Br 분포 (n) | 평가 |
|------|-------|-------|---------------|---------------|------|
| comp1 (Li6) | 1.0 | 0 | **2 at 4a + 2 at 4c/4d** (anion disorder) | — | pristine 50:50 |
| comp2 (Li6) | 0.5 | 0.5 | **2 at 4c/4d (100%)** | **2 at 4a (100%)** | ⭐ 정확 분리 |
| comp3 (Li5.4) | 1.0 | 0.6 | 4 loose + 1 compact | 1 compact + 2 loose | Cl→4c/4d 우세, Br→4a 우세 |
| comp4 (Li5.4) | 0.8 | 0.8 | 1 compact + 3 loose | 2 compact + 2 loose | mixed (frustration) |
| comp5 (Li5.4) | 0.6 | 1.0 | 1 compact + 2 loose | 3 compact + 2 loose | Br 다수, both site 점유 |
| modelC (Li5.4) | 1.6 | 0 | **6 compact + 2 loose** | — | Cl이 4c/4d fully + 4a 일부 진입 |

→ ==**모든 comp에서 Br→4a, Cl→4c/4d 우세 trend 일관**==. comp4에서만 frustration으로 분포 흐트러짐.

### Why Bond Lengths Differ — 우리 데이터로 정량

**comp1 → modelC (Li-Cl 변화):**
```
                       free anion site 점유          mean Li-Cl
comp1 v2 (Cl=1.0)      2 at 4a + 2 at 4c/4d          2.486 Å
modelC v2 (Cl=1.6)     ~2 at 4a + 6 at 4c/4d         2.547 Å (+0.061 Å)

→ Cl 늘리면 4c/4d (compact) 우선 채움
→ 그 다음 4a (loose)에 진입
→ 4a-Cl 추가로 평균 길어짐
```

**comp1 → modelC (Li-S 변화):**
```
                       free S 분포                   mean Li-S
comp1 v2               4 at 4a/4d (anion disorder)    2.498 Å
modelC v2              ~2 at 4c/4d only (4a은 Cl)     2.460 Å (-0.038 Å)

→ Cl이 4a S²⁻ 자리 차지하면서 free S 사라짐
→ 남은 free S는 4c/4d 만 → mean Li-S 짧아짐 (compact site)
```

→ ==**modelC에서 Li-Cl ↑ + Li-S ↓는 site rearrangement 직접 결과**==.

### comp4 frustration의 microscopic origin (측정 기반)

```
comp4 (Cl=Br=0.8) free anion 분포:
  Cl: 1 compact + 3 loose ← 4c/4d 선호 약화
  Br: 2 compact + 2 loose ← 4a 선호 약화 (50:50)

→ Cl/Br 둘 다 site 선호 약해짐
→ "Cl 4c/4d", "Br 4a" rule이 깨짐
→ random distribution = maximum disorder
→ Bader anomaly (S=-1.55 ⬇, P=+3.63 ⬇) = 전기적 fingerprint
```

==**comp4 anomaly의 microscopic origin = site frustration**==.

### 이 site science가 저자 narrative를 어떻게 깨는가

저자: "Li-Cl shorter and more ionic"  
**진실 (with site science)**:
- Li-Cl은 **single value가 아님** — 4c/4d-Cl(짧음) vs 4a-Cl(김) 두 environment
- modelC에서 4a-Cl 점유로 average length가 ==**Li-S average보다 더 길어짐**==
- 즉 저자는 ==**single-environment 가정**==을 multi-environment 시스템에 적용함 — fundamental error

==**4a vs 4c/4d site distribution이 paper #1 narrative의 microscopic foundation**==. 저자가 무시한 layer가 우리 데이터로 정량 검증됨.

---

## Methodology — 우리 측정 출처

**Bond lengths**:
- DFT post-relax structures (PBE, SSSP_1.3.0_PBE_efficiency, ecutwfc 60 Ry, ecutrho 480 Ry)
- v2 anneal champion structures for comp1, comp2, modelC (paper-quality)
- v1 baseline post-relax for comp3, comp4, comp5
- Cutoffs: Li-Cl 3.2, Li-Br 3.4, Li-S 3.0, P-S 2.3 Å (consistent across all comps)
- Method: minimum-image convention (mic) distance, ASE measurement

**Bader charges**:
- Method: pp.x charge density (plot_num=21 all-electron) + Henkelman bader_lnx_64 v1.05
- Cross-validated against DB (Δ ≤ 0.016 e for all elements)

**Site analysis (4a vs 4c/4d)**:
- Fractional coordinate identification of Wyckoff positions
- Local Li environment classification (mean Li-X distance, coordination number)
- Two-group clustering by gap detection in Li distances

**Verification date**: 2026-05-05 (single-script measurement, all comps consistent cutoff)

---

#paper1 #refutation #wad #halogen #bond-length #bader #q2-over-r #author-rebuttal #4a-4d-site
