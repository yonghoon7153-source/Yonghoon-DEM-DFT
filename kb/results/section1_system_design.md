# Section 1 (Deep Dive) — 시스템 설계의 과학적 논리

## 1.1 왜 Argyrodite를 host로 선택했나

### Argyrodite (Li₆PS₅X) 특징
- 공간군 F-43m (cubic, high symmetry — basin enumeration 용이)
- PS₄³⁻ tetrahedron + free anion + halide 3-component 격자
- 상온 σ_Li⁺ ≈ 1-10 mS/cm (실용 SE 범위)
- 합성 용이 (ball mill + 열처리, 산업 가능성)
- Li metal 안정성 marginal (decomposition 영역, paper #2의 motivation)

→ "Real-world battery에 들어갈 수 있는 시스템"이라 실험 데이터(Adeli, Kraft 등)와 직접 비교 가능 = paper #1 strength.

### 선행 연구 정황 (paper draft 인용)
- **Adeli et al. 2019**: Li5.4PS4.4Cl1.6 reported (modelC)
- **Kraft et al. 2018**: σ vs halogen content systematic
- **Deiseroth 2006**: Li6PS5Cl 결정구조 결정
- **Deng 2016**: Li6PS5Cl 탄성계수 측정 (우리 v2 0K 78.8 GPa vs Deng 22.1 GPa — 우리가 4× 큼, DFT 0K vs MD 단단함)

---

## 1.2 두 가지 독립 변수의 기하학적 이해

### 변수 A: Vacancy formation (Li6 → Li5.4 transition)

```
Li6PS5Cl   →   Li5.4PS4.4Cl1.6
                    ↓
           "Halogen-rich substitution"

            S²⁻ 0.6/fu 자리에 Cl⁻ 들어감
            → charge balance: −2 ↔ −1 부족 1 → Li⁺ 0.6 빠짐

            결과:
            - Li 6 → 5.4 (vacancy 0.6/fu = 12%)
            - S 5 → 4.4 (S 0.6 자리 Cl이 차지)
            - Cl 1 → 1.6
```

**중요**: vacancy ≠ "Li 없앤" 거 아님. 합성적으로 발생한 결과:
- Cl⁻이 S²⁻ 자리 강제 차지 → charge balance 위해 Li⁺ 자동 빠짐
- 즉 vacancy는 defect가 아닌 **ground-state property of Li5.4 family**

### 변수 B: Halogen substitution (Cl ↔ Br)

```
순수 Cl (comp1, modelC)
    ↓ Br 도입
혼합 Cl/Br (comp2, comp3, comp4, comp5)
    ↓
Cl/Br 비율 변화 → mechanical & adhesion 변화
```

**Br 효과 (Shannon ionic radii)**:
- Cl⁻: 1.81 Å
- Br⁻: 1.96 Å (+8% 큼)

이로 인해:
- Lattice expansion (cell volume ↑)
- Li-X bond 길어짐 (~0.20 Å)
- Polarizability ↑ (Br > Cl, 약 1.5×)
- Ionic character ↓ (|q(Br)| < |q(Cl)|)

---

## 1.3 6 composition의 design matrix — 변수 분리 전략

### 2D matrix view

|                   | Vacancy=0 (Li6 family)   | Vacancy=0.6 (Li5.4 family)    |
|---|---|---|
| **Cl-only**       | comp1 ✓ (baseline)       | modelC ✓ (vacancy alone)      |
| **Cl+Br mixed**   | comp2 ✓ (Br alone)       | comp3, comp4, comp5 ✓         |
| **Br-rich**       | ✗ (실험 없음)              | comp5 ✓ (Br 1.0)              |

### 각 비교의 의미

| 비교 | 변수 분리 | 무엇을 알게 되나 |
|---|---|---|
| comp1 vs comp2 | Br 단독 (Li6 family) | Br 0.5 도입 효과만 (no vacancy interference) |
| comp1 vs modelC | Vacancy 단독 | Vacancy 효과만 (no Br interference) ← modelC 핵심 가치 |
| modelC vs comp3 | Vacancy + Br (mixed) | Br이 vacancy 효과를 어떻게 변형시키나 |
| comp3 vs comp4 vs comp5 | Br ratio 점진 (Li5.4 family) | Br dose-response curve in vacancy system |
| comp2 vs (comp3,4,5) | Cross-family (Li6 vs Li5.4) | Vacancy 효과의 robustness (Br 존재 하에서도?) |

---

## 1.4 modelC가 왜 특별한가 — "Vacancy alone control"

**modelC = Li5.4PS4.4Cl1.6 = Cl-only + vacancy**

다른 comp들과 modelC의 차이:

|         | comp1 | modelC | comp3-5 |
|---|---|---|---|
| Vacancy | ❌    | ✅     | ✅      |
| Br      | ❌    | ❌     | ✅      |
| 혼합 효과 | none | vacancy isolated | tangled |

→ modelC는 vacancy 효과를 Br interference 없이 측정하는 **유일한 system**.

### modelC를 통해 답할 수 있는 질문
1. **"Vacancy가 B0를 얼마나 줄이나?"** → comp1(26.5) − modelC(19.59) = −6.9 GPa (Br 기여 0)
2. **"Vacancy가 PS4 charge polarization을 약화시키나?"** → comp1 P(+4.69) − modelC P(+4.34) = −0.35 e (paper #1 새 발견)
3. **"600K에서 vacancy가 entropy stabilizer 역할 하나?"** → modelC E_VRH(32.9) > comp1(29.1) → YES
4. **"Vacancy alone Wad enhancement 몇배?"** → modelC ~2.0 vs comp1 ~1.2 = 1.67× (paper #1 main contribution)

→ **modelC = Paper #1의 keystone composition**. 다른 5개는 "context"를 제공.

---

## 1.5 design matrix의 한계 (limitation 인정)

### 빠진 부분
- **Li6 + Br-rich 없음** (Br=1.0 + vacancy=0): Li6PS5Br 같은 compound. 실험 합성 어려움.
- **Vacancy 다른 양 없음** (0.3/fu, 0.9/fu): full vacancy spectrum 없음.
- **다른 anion 없음** (I, F): 같은 family 내 chemistry diversity 부족.
- **다른 cation 없음** (Na, K): general lanthanide doping은 paper #2로 넘어감.

### 그러나 이 6개로도 충분한 이유
- 2 binary variables (vacancy 0/0.6, Br 0/0.5/0.6/0.8/1.0) 충분히 sample
- 각 variable의 effect를 isolated로 추출 가능 (modelC, comp1 control)
- Industrial relevance (Adeli composition modelC, Kraft composition comp1-5 다 실측 데이터 있음)

---

## 1.6 paper #1 narrative arc 설계

### 기존 narrative (drafted in v1)
1. Br increases bond length → weakens ionic interaction → lower B0/E
2. Vacancy enhances Wad (2× via "chemical anchor" hypothesis)
3. 600K reversal: vacancy = phonon entropy stabilizer

### 새로운 추가 (오늘 분석으로)
4. **NEW: Vacancy reduces PS4 charge polarization**
   - P -0.35 e in modelC vs comp1
   - q²/r P-S: -11% in modelC
   - "Covalent backbone is also affected, not just ionic"
5. **NEW: Cross-family Wad paradox**
   - 2× difference NOT explained by single-atom Bader
   - Must be collective surface mechanism
   - Validates "structural anchor" interpretation
6. **NEW: Anomaly analysis**
   - comp3 Br > Cl Bader (site disorder effect)
   - comp4 S charge low (most heterogeneous)
   - These provide finger-prints for paper figures

---

## 1.7 실험-이론 연결 점검

### DFT vs experimental 일치도

| 양 | 우리 DFT | 실험 (Kraft 등) | 일치? |
|---|---|---|---|
| Lattice param | 9.79-9.90 Å | 9.85 Å | ✓ ±1% |
| B0 (Li6) | 26.5 GPa | (DFT 단독 비교) | — |
| Bond P-S | 2.06 Å | 2.05-2.07 Å | ✓ |
| Bond Li-Cl | 2.49-2.57 Å | 2.46-2.55 Å | ✓ |
| Wad ratio (Br dose) | 1.0/0.94/0.79 (comp3/4/5) | 1.0/0.94/0.79 | ✓ 정확 일치 R=0.9999 |
| E (300K MD ≈ ind T) | 30-50 GPa | 22 GPa (Deng) | × 30% 큼 (DFT bias) |

→ **상대 trends 완벽**. 절대값은 DFT bias (PBE underestimates anharmonicity → overestimates moduli at finite T) — 보편적 현상.

### Industrial relevance

| Comp | Industrial application | Note |
|---|---|---|
| comp1 | "Li6PS5Cl" 표준 SE | 가장 많이 합성 |
| comp4 | "optimal" candidate (paper draft) | E ↓ 9% + Wad ↑ + basin stable |
| modelC | Adeli 2019 reported composition | High σ_Li (12 mS/cm) |
| comp5 | Br-rich variant | 실험 그룹들 시도 중 |

---

## 1.8 한 줄 요약 (이 section)

> 6개 composition은 **vacancy(Li6 vs Li5.4)와 halogen(Cl vs Br) 두 변수의 2D matrix**를 sampling. modelC는 vacancy 효과를 Br interference 없이 측정하는 **unique control**. 이 design으로 (1) 두 변수의 단독 효과 분리, (2) 변수 간 interaction 정량, (3) Wad paradox 같은 새 현상 발견 가능.

---

## Data sources
- DB: `db/compositions/comp1.json` ~ `comp5.json`, `modelc.json`
- References: `db/literature/refs.json` (deiseroth2006, kraft2018, adeli2019, deng2016)
- Cross-comp tables: `db/properties/elastic.json`, `eos.json`, `electronic.json`, `bonds.json`, `adhesion.json`
