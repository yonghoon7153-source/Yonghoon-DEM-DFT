# Vacancy + Halogen Distribution → Adhesion: Corrected Mechanism

> 2026-05-08 정정. 이전 (kb/physics/vacancy_effects.md, db/properties/adhesion.json)
> 에서 "Li6 = no vacancy → no hopping"으로 단순화한 부분을 literature
> (Adeli 2019, Yu/Wagemaker 2016, Hanghofer 2019, D'Amore 2022, Rao 2020)
> 으로 검증 후 수정.

## 핵심 정정

**틀린 framing**: "Li6는 vacancy 없어서 hopping 안 됨"
**올바른 framing**: Li6PS5Cl도 superionic이다 (~3 mS/cm at 300 K). 다만 Li5.4
는 stoichiometric 추가 vacancy + halogen rich anion sublattice로 더 빠르다.

## 1. Argyrodite 구조 사실들 (literature 검증)

### Wyckoff 부분 점유 (Rao 2020, D'Amore 2022)

Li6PS5Cl에서 Li가 차지할 수 있는 결정학적 site:
- **24g** (T5a): cage center 사이
- **48h** (T5, T5'): 가장 favorable
- 가끔 **16e**

Nominal "Li 6/fu"임에도 **24g와 48h site들은 ~50% 부분 점유**. 즉 Li6PS5Cl
도 Wyckoff-level에서는 vacancy site가 잔뜩 있음 (Rao 2020 neutron PDF로 직접
확인됨).

### Anion sublattice S²⁻/Cl⁻ 혼합 (Hanghofer 2019)

S와 Cl도 두 개의 anion site (4a, 4d)에서 혼합됨:
- Li6PS5Cl: 4a에 60% Cl, 4d에 50% (Hanghofer 2019)
- 이 anion disorder가 conductivity를 더 boost

### Li6 vs Li5.4 — 실제 차이

| | Li6PS5Cl | Li5.4PS4.4Cl1.6 |
|---|---|---|
| Li per formula unit | 6 | 5.4 |
| Halogen per fu | 1.0 | 1.6 |
| **Wyckoff 부분 점유** | ~50% (24g, 48h) | ~45% (24g, 48h) |
| **추가 stoichiometric Li vacancy** | **0** | **0.6/fu** |
| Anion S²⁻/X⁻ inversion | medium | high |
| Conductivity (300 K) | ~3 mS/cm | ~9 mS/cm (Li5.5PS4.5Cl1.5, Adeli 2019) |
| Intracage hopping Ea | ~0.12–0.14 eV | 더 낮음 |
| Intercage hopping Ea | ~0.17–0.20 eV | 더 낮음 |

**둘 다 superionic. Li5.4가 ~3× 빠른 이유**: stoichiometric Li vacancy 추가 +
S²⁻ → Cl⁻ 치환으로 Li-anion 상호작용 약화 (Adeli 2019 mechanism).

## 2. Paper #1의 1162 meV는 무엇이었나

Paper #1이 enumeration으로 측정한 "Li ordering spread":

- 한 unit cell 안에서 가능한 distinct Li occupation patterns 사이의 **total
  energy 차이**
- D'Amore 2022: Li6PS5Cl unit cell에 가능한 ordering ~10¹³ 개
- Li6의 1162 meV: 다양한 ordering의 ground-state energy 분포 폭
- Li5.4의 0.1 meV: vacancy를 가장 unfavorable site에 두면 거의 unique GS

**중요**: 이 spread는 PES 위 distinct local minima의 **세로 분포**이고,
인접 minima 사이의 **saddle barrier (= hopping Ea)**와는 다른 양. 둘 다
PES 정보지만 서로 다른 측면.

- Li6의 큰 spread = configurationally frustrated (어느 ordering이 GS인지
  애매함)
- Li6의 hopping Ea ~0.12-0.32 eV = 별개로 측정된 양 (NMR, NEB)

## 3. SE/NCM 인터페이스에서의 실제 메커니즘

### 표면 termination 측정 (v25 Y2)

| comp | Cl_surf 비율 | Br_surf 비율 | family | paper Wad |
|---|---|---|---|---|
| comp1 | 42% | — | Li6 (Cl-only) | 194 |
| comp2 | 33% | 33% | Li6 (Cl+Br) | 180 |
| **comp3** | **20%** | 33% | Li5.4 (Cl-rich) | **316** |
| comp4 | 25% | 50% | Li5.4 (Cl=Br) | 298 |
| comp5 | 33% | 40% | Li5.4 (Br-rich) | 249 |
| **modelC** | **38%** | — | **Li5.4 (Cl-only)** | — |

### modelC가 던지는 의문

modelC는 Li5.4 family (vacancy 0.6/fu) **인데도 Cl_surface=38%로 Li6
family와 비슷**. 즉 단순한 "vacancy → halogen retreat"가 아님.

**올바른 메커니즘 (수정)**: 표면 halogen 후퇴는 **(i) stoichiometric Li
vacancy + (ii) Cl/Br 사이즈 mismatch 둘 다** 필요.

- Cl만 있으면 (modelC): vacancy를 Cl만으로 페어링해도 사이즈 차별화 없음
  → 표면 vs bulk 선호 약함
- Cl+Br 혼합 (comp3-5): 작은 Cl이 vacancy 인근 site 선호 (charge density
  high), 큰 Br이 다른 곳 → 결과적으로 표면에서 Cl 후퇴
- Li6 (vacancy 없음): 페어링 driving force 없음 → 표면 분포가 bulk 분포
  와 비슷

### NCM 표면에서의 Coulomb

NCM 산화물 표면 = O²⁻ 노출. SE 표면 ions과의 상호작용:
- Li⁺ ↔ O²⁻: 인력
- Cl⁻/Br⁻ ↔ O²⁻: 반발 (둘 다 음이온)

Cl-O contact density가 높을수록 paper exp Wad 낮음 (R=-0.91, p=0.03).
이게 우리가 측정한 mechanism의 직접 quantification.

## 4. v9-v22 LBFGS migration artifact의 정정된 설명

### 잘못된 framing (이전)
"Li6는 hopping 못 하지만 LBFGS가 가짜로 밀어서 NCM에 박힘"

### 올바른 framing
1. Li6와 Li5.4 **둘 다 bulk hopping은 정상** (둘 다 superionic).
2. **인터페이스에서**: NCM oxide의 Li-O coordination이 SE Wyckoff site보다
   에너지 낮음 → Li가 SE에서 NCM으로 흘러 들어가는 gradient 존재.
3. Unconstrained LBFGS는 saddle을 무시하고 gradient를 따라가 Li를 NCM bulk
   으로 끌어들임. 이건 **interface-specific drift**이지 bulk hopping이 아님.
4. **Li6가 Li5.4보다 더 심한 이유**:
   - Frustrated configuration → 시작 시점 atomic gradient magnitude 큼
   - Stoichiometric Li 양 자체가 더 많아 인터페이스 이주 후보 atom 더 많음
5. M2 (FixAtoms로 NCM + bottom 70% SE 잠금) → Type-a (0.1-0.5 Å) relax만
   허용 → migration 차단 → bond density 보존, R(Cl-O) = -0.91 회복.

## 5. 수정된 한 줄 요약

> **Li6PS5Cl과 Li5.4PS4.4(Cl,Br)1.6 둘 다 bulk superionic conductor.** Li5.4가
> 더 빠른 이유는 stoichiometric Li vacancy 추가 + S²⁻ → Cl⁻ 치환으로 Li-anion
> 상호작용 약화 (Adeli 2019).
>
> **SE/NCM 인터페이스에서의 contact chemistry는 별개의 axis**: Li5.4 family
> 의 Cl+Br mix 조성에서 vacancy + halogen size pairing이 표면 halogen을
> 안쪽으로 후퇴시킴. 이게 표면 Cl-O density를 줄여서 NCM-O와의 anion-anion
> 반발을 약화 → 더 강한 접착.
>
> **modelC (Li5.4 + Cl-only)가 보여주는 한계**: vacancy alone으로는 부족,
> halogen 사이즈 mix가 필요.
>
> **v9-v22 LBFGS artifact**는 bulk Li mobility와 무관: NCM-O의 Li 끌림력이
> 인터페이스에서 발현된 gradient drift. M2 FixAtoms로 차단 가능 (RMS<0.2A).

## 참고 문헌 (db/literature/refs.json에 추가됨)

- **Deiseroth 2006**: Li6PS5X synthesis, structure, conductivity
- **Adeli 2019**: Halide substitution → Li5.5PS4.5Cl1.5 conductivity 9.4 mS/cm
- **Yu/Wagemaker 2016**: Li6PS5Cl bulk vs interface diffusion, NMR + DFT-MD
- **Hanghofer 2019**: Substitutional disorder, NMR Ea = 0.17–0.32 eV (Cl)
- **D'Amore 2022**: Argyrodite enumeration ~10¹³ orderings, Coulomb selection
- **Rao 2020**: Neutron PDF + NMR, direct Wyckoff partial occupancy
- **Kraft 2018**: Lattice polarizability + ionic conductivity

#paper2 #vacancy-mechanism #correction #2026-05-08 #literature-validated
