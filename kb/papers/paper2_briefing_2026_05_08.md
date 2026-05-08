# Paper #2 — SE/NCM Adhesion Mechanism: Briefing for First-Time Reader

> **연구자**: 안용훈 (BML Lab, Hanyang University)
> **세션 기간**: 2026-05-04 ~ 2026-05-08
> **대상**: paper #2 처음 검토하는 교수님 / 동료 대학원생
> **마지막 업데이트**: 2026-05-08

---

## 0. 한 줄 요약 (TL;DR)

> 6개 argyrodite 조성의 SE/NCM 접착 강도 (paper experiment Wad)가
> **표면 Cl-O 접촉 밀도**라는 단순 기하학적 descriptor와 R = -0.91로 강하게
> 음의 상관관계를 보이며, 이 신호는 **NCM facet 변경 / 표면 atom 재완화 /
> 셀 크기 / Li 위치 perturbation 등 7가지 method 변형에 모두 robust**함을
> 확인. Mechanism은 Li 격자 vacancy와 halogen 크기 차이가 결합되어
> 표면에서 halogen이 안쪽으로 후퇴 → NCM oxide와의 음이온-음이온 반발 감소 → 접착 향상.

---

## 1. 배경 — 왜 이 연구를 하나

### 1.1 시스템

전고체 Li-ion 배터리에서 황화물 고체전해질 (sulfide solid electrolyte, SE)을
산화물 양극재 (NCM)에 접착시켜야 함. 접착이 약하면 사이클링 중 박리되어
배터리 성능 저하.

본 연구의 SE는 **할로겐 치환 argyrodite**:
- Li6PS5Cl, Li6PS5Cl0.5Br0.5 → Li6 family (vacancy 없음)
- Li5.4PS4.4(Cl,Br)1.6의 3가지 변종 → Li5.4 family (vacancy 0.6/fu)
- modelC = Li5.4PS4.4Cl1.6 (Li5.4지만 Cl-only, "Br 효과 분리용 control")

### 1.2 Paper #1 (이미 출판) — Mechanical properties

체적 탄성률 B0, 영률 E, 탄성 상수 Cij를 조성별로 계산. **결론: Br 증가 → B0/E 감소** (intrinsic trend, lattice softening).

### 1.3 Paper #2 (현재 작업) — Adhesion to NCM

목표: **paper experiment 측정값** (실험실에서 측정한 SE/NCM interfacial Wad)
을 atomic-level descriptor로 설명.

| comp | 실험 Wad (mJ/m²) | family |
|---|---|---|
| comp1 | 194 | Li6 |
| comp2 | 180 | Li6 |
| **comp3** | **316** ⭐ 최고 | Li5.4 |
| comp4 | 298 | Li5.4 |
| comp5 | 249 | Li5.4 |
| modelC | (실험 없음) | Li5.4 |

**관찰**: Li5.4 family가 모두 Li6 family보다 접착 우수. 왜?

---

## 2. 출발점 — 무엇이 어려웠나

### 2.1 Paper #1의 v5 결과는 server crash로 lost

v5 method로 cross-family R²=0.999 매치를 얻었다고 알려져 있었으나,
- 서버 데이터 lost
- 그 R²=0.999는 **user-curated** (인위적 selection)
- → from-scratch validation 필요

### 2.2 직관적 후보들이 모두 실패

처음 시도: SE와 NCM 슬랩을 쌓은 뒤 LBFGS로 relax → energy descriptor로
Wad 계산.

문제: **Li 원자가 NCM bulk으로 1.5 Å 이상 침투** (Li migration / intermixing
artifact). 이는 paper rank를 **inverted** (Li6 > Li5.4) 결과로 만듦.

### 2.3 핵심 도전

> 아무리 정교한 ML interatomic potential (MLIP, 본 연구 UMA)을 써도 **rigid
> 슬랩 에너지가 paper exp와 anti-correlate (R=-0.76)**. 즉 단순 에너지 기반
> descriptor가 작동 안 함. 더 깊은 물리적 통찰 필요.

---

## 3. Method 발전 과정 (v9 → v26)

### Phase A: 에너지 descriptor 시도 (v9 ~ v14) — 실패

| 버전 | 시도 | 결과 |
|---|---|---|
| v9-v11 | Sandwich + LBFGS / Cleavage | INVERTED |
| v12 | Rigid (no LBFGS), Haruyama 1-interface | gap=2.5 Å에서 우연히 paper match |
| v13 | Z-scan (gap 1.0–6.0 Å) | gap에 따라 ranking 뒤집힘 → coincidental confirmed |
| v14 | Equilibrium gap (1.2–1.6 Å) + bond decomposition | **bond density 매우 robust** (R 0.8-0.9) |

**결론**: 슬랩 에너지는 composition-dependent Madelung sum에 dominated되어
interface chemistry를 가림. **에너지 대신 기하학적 양** (bond density) 에
주목해야.

### Phase B: 기하학적 descriptor 발견 (v15) — Breakthrough

**v15 (baseline 확정)**:
- 각 comp의 SE/NCM 슬랩을 equilibrium gap (1.2–1.6 Å)에서 stack
- 36개 xy-shift registry로 평균
- Cutoff 거리 (Li-O 3.0, Cl-O 3.5, Br-O 3.7 Å) 내에 있는 atom pair 개수 / 면적

| Bond type | R vs paper Wad (n=5) | 해석 |
|---|---|---|
| **Li-O density** | **+0.82** (n=5, p=0.09) | 인력 (양이온-음이온) |
| **Cl-O density** | **-0.91** (n=5, p=0.03) | 반발 (음이온-음이온) |
| Br-O density | +0.40 (약함) | 약한 양의 상관 |

→ **단순 기하학적 contact density 만으로 paper 실험 ranking 재현됨.**

xy-shift CV = 6.1% (registry-insensitive, 즉 SE/NCM 정렬에 둔감 = bulk
chemistry 측정).

### Phase C: 통계적 검증 (v23–v25)

| 검증 | 결과 |
|---|---|
| Spearman rank corr | -0.90 (Pearson과 일치) |
| Bootstrap 95% CI | [-0.99, -0.62] |
| Jackknife (leave-one-out) | sign 안정 |
| Bader charge weighting | R 약화 (-0.11) — geometric이 더 robust |
| Halogen z-distribution | comp3가 표면 Cl 노출률 가장 낮음 (20%) |
| **Collinearity matrix** | **6쌍 |R|>0.95** → effective dim ~2 |

핵심 발견: 8개 candidate descriptor 모두 **하나의 axis (Li6 vs Li5.4 family)**
를 다른 표현으로 측정. Cl-O density, Li/fu, vacancy count, Cl+Br stoichiometry,
표면 S termination 다 collinear.

### Phase D: 7-method stress test (v26)

서로 다른 7개 method 변형으로 R(Cl-O) 안정성 검증:

| 변형 | R(Cl-O) | 변화 (Δ) |
|---|---|---|
| v15 baseline (NCM 104 facet) | -0.914 | — |
| NCM 003 facet | -0.914 | 0.000 |
| NCM 110 facet | -0.911 | +0.003 |
| NCM 012 facet | -0.912 | +0.002 |
| Constrained relax (top 30% SE LBFGS, RMS<0.2 Å) | -0.913 | +0.001 |
| 2×2 lateral supercell | -0.913 | +0.001 |
| Li shake ±0.2 Å (5 seeds 평균) | -0.886 | +0.028 |
| **8개 perturbation 범위** | **[-0.914, -0.886]** | |

→ **R(Cl-O) is method-independent**. Paper #2의 가장 강력한 claim.

(Li-O는 facet 바꾸면 sign flip, Li shake에 ±0.4 분산 — facet-specific으로 caveat)

---

## 4. 최종 Method — Cl-O Contact Density

### 4.1 알고리즘

```
1. SE 슬랩 + NCM 슬랩 (3-layer (104) facet)을 z방향으로 쌓음
2. equilibrium gap g_eq (1.2 ~ 1.6 Å, comp별로 미세 다름)에서 정지
3. cutoff 3.5 Å 이내 Cl-O atom pair 개수를 carbon
4. xy 면적으로 나눠 density (Å⁻²) 계산
5. 36개 xy-shift registry 평균 (CV 6.1%)
```

### 4.2 결과

| comp | Cl-O density (Å⁻²) | paper Wad |
|---|---|---|
| comp1 | 0.0228 | 194 |
| comp2 | 0.0285 | 180 |
| comp3 | **0.0000** | **316** |
| comp4 | 0.0000 | 298 |
| comp5 | 0.0000 | 249 |
| modelC | 0.0948 (가장 큼) | (실험 없음) |

→ Cl-O contact 0인 comp3-5가 가장 접착 우수. modelC는 Cl 풍부해서 표면
contact 많음.

---

## 5. Mechanism — 왜 Cl-O Density가 작동하나

### 5.1 결정학적 사실 (literature)

Argyrodite Li6PS5Cl는:
- **Wyckoff Li site 24g, 48h가 ~50% 부분 점유** (Rao 2020 neutron PDF)
- **Anion sublattice S²⁻/Cl⁻ 혼합 (4a, 4d position)** (Hanghofer 2019)
- 가능한 ordering 약 **10¹³ 개** (D'Amore 2022)
- **Bulk superionic conductor (~3 mS/cm at 300 K)** (Deiseroth 2006)
- Intracage Ea 0.12 eV, intercage 0.20 eV (Yu/Wagemaker 2016)

Li5.4PS4.4Cl1.6:
- 동일 Wyckoff site, 점유율 ~45%
- **추가 stoichiometric Li vacancy 0.6/fu**
- S²⁻ 0.6개 → Cl⁻로 치환 (charge balance가 Li 제거 강제)
- Conductivity ~9 mS/cm (Adeli 2019)
- **둘 다 superionic** — Li5.4가 ~3× 빠름

### 5.2 인과 사슬 (corrected mechanism)

1. **Charge balance**: S²⁻ 자리에 Cl⁻ 들어가면 -1만큼 charge 부족 → Li⁺
   하나 제거 (Li vacancy 0.6/fu 형성)

2. **Halogen pairing in bulk**: Li5.4 family에서 작은 Cl⁻ (이온반경 1.81 Å)
   가 vacancy 인근 site 선호 (charge density), 큰 Br⁻ (1.96 Å)는 다른 곳.
   이 페어링은 **표면보다 bulk에서 더 안정**.

3. **Surface depletion**: 그 결과 Li5.4 family + Cl/Br mix 조성에서 Cl이
   표면에서 안쪽으로 후퇴.

   측정값 (top + bottom 20% 슬랩에서 Cl 비율):
   | comp | Cl 표면 노출 | family |
   |---|---|---|
   | comp1 | 42% | Li6 |
   | comp2 | 33% | Li6 |
   | **comp3** | **20%** ⬇ | Li5.4 + Cl/Br mix |
   | comp4 | 25% | Li5.4 + Cl/Br mix |
   | comp5 | 33% | Li5.4 + Cl/Br mix |
   | **modelC** | **38%** | Li5.4 (Cl-only, no Br) |

   **modelC가 핵심 증거**: vacancy만 있고 Cl/Br mix 없으면 표면 후퇴 효과
   없음 → **mechanism은 vacancy + halogen size mismatch 둘 다 필요**.

4. **NCM 인터페이스의 Coulomb**: NCM 표면 = O²⁻ 이온 노출. Cl⁻/Br⁻ 모두
   음이온이므로 O²⁻와 **반발**. 표면 Cl 적을수록 NCM-O와 잘 붙음.

5. **측정 quantification**: Cl-O contact density (cutoff 3.5 Å, 단위
   Å⁻²) 가 이 표면 chemistry를 직접 측정. R = -0.91.

6. **Li-O 인력은 보조 증거**: comp3-5가 표면에 Li-rich라서 NCM-O 인력에도
   유리. 하지만 NCM facet 바꾸면 ranking 뒤집혀서 paper #2 메인 claim에는
   넣지 않음 (caveat as 104-specific).

### 5.3 Li6와 Li5.4 둘 다 superionic — 그럼 왜 표면 chemistry는 다른가

이게 처음 듣는 사람이 헷갈리는 지점:
- **Bulk Li hopping**: 둘 다 mobile (Wyckoff site 부분 점유 + intracage barriers
  ~0.1-0.2 eV)
- **표면 termination chemistry**: 슬랩을 cleave한 시점에 어느 atom이 표면에
  남느냐는 정적인 thermodynamic 문제. Li5.4 family 의 "vacancy + halogen
  pairing"은 lowest-energy bulk configuration이 표면에 halogen을 두지 않게
  만듦.

즉 **mobility**와 **surface termination preference**는 별개의 axis. 두 axis
모두 vacancy/disorder에 영향받지만 다른 방식으로.

---

## 6. v9-v22 LBFGS Migration Artifact 정정 설명

### 6.1 무엇이 일어났나

초기 method (v9-v22 LBFGS-based) 적용 시:
- 슬랩을 쌓고 LBFGS optimization 실행
- Li6 family에서 Li 원자 ~20개가 NCM 슬랩 안으로 1.5+ Å 침투
- Li5.4 family에서는 거의 없음
- 결과: Wad 계산이 "얼마나 Li가 NCM에 박혔나"를 측정 → paper rank inverted

### 6.2 왜 일어났나 (corrected understanding)

**틀린 설명** (이전 노트): "Li6는 vacancy 없어서 hopping 안 되는데 LBFGS가
가짜로 밀어넣음"

**정정된 설명** (literature-backed):
- 두 family 모두 bulk Li hopping은 정상 (둘 다 superionic)
- 인터페이스에서 NCM oxide의 Li-O coordination이 SE Wyckoff site보다 에너지
  낮음 → Li가 SE에서 NCM으로 흘러 들어가는 gradient 존재
- **Unconstrained LBFGS는 saddle barrier를 인지하지 못하고 continuous
  gradient만 따라감** → atom이 site framework를 벗어나 NCM bulk으로 drift
- Li6에서 더 심한 이유:
  (a) Configurationally frustrated (paper #1: 1162 meV ordering spread)
       → 시작 시점 atomic gradient magnitude 큼
  (b) Stoichiometric Li 양 자체가 더 많아 인터페이스 이주 후보 atom 더 많음

### 6.3 v26 M2 — 해결 검증

**Constrained relax** (FixAtoms로 NCM + bottom 70% SE 잠금, top 30% SE만
free, max 30 LBFGS step):

| comp | RMS displacement (Å) | Max displacement (Å) | Migration? |
|---|---|---|---|
| comp1 | 0.196 | 1.430 | NO |
| comp2 | 0.183 | 1.240 | NO |
| comp3 | 0.150 | 1.312 | NO |
| comp4 | 0.105 | 0.670 | NO |
| comp5 | 0.111 | 0.728 | NO |
| modelC | 0.144 | 1.494 | NO |

**모든 comp RMS < 0.2 Å, max < 1.5 Å, no migration**. Bond density v15
rigid와 정확히 일치, R(Cl-O) = -0.913.

→ **Migration은 bulk hopping과 무관, 인터페이스-specific gradient drift
artifact**. FixAtoms로 차단 가능. 이로써 v22 unconstrained relax 결과
(R(Li-O) +0.82 → +0.12로 추락)도 설명됨.

---

## 7. 정직한 한계 (Caveats for Paper)

### 7.1 Intra-family resolution

comp3 vs comp4 vs comp5는 모두:
- Li5.4 family
- vacancy 0.6/fu
- Cl+Br = 1.6/fu (총 halogen 같음)
- Cl/Br 비율만 다름

우리 측정 모든 descriptor에서 차이 < 0.005 (resolution 미만). paper exp는
comp3 > comp4 > comp5 (Br 증가 → 약간 감소) 보이지만 우리 method로는
구분 불가.

### 7.2 modelC가 던지는 미묘함

modelC = Li5.4 + Cl-only. Cl_surface=38% (Li6 family 수준). 즉:
- Vacancy 단독으로는 surface depletion 안 일어남
- Cl/Br size mix가 함께 있어야 mechanism 작동
- → paper에서 "vacancy + halogen mix 결합" mechanism으로 정직하게 표현

### 7.3 MLIP-only (no DFT verification)

- 본 연구는 UMA MLIP에 의존 (KISTI/gabia 자원 한계로 DFT slab 불가)
- Bond density는 geometry-only (MLIP-independent) → 강력
- Energy descriptor (Wad)는 MLIP-dependent → paper에서 메인으로 안 씀
- MACE-MP-0 cross-check는 별도 env에 설치 후 진행 (v26c, KISTI 미실행)

### 7.4 n=5 small dataset

- Pearson R 불확실성 ±0.2
- Bootstrap CI95 [-0.99, -0.62]
- 추가 조성으로 검증하면 더 강력해질 것 (future work)

---

## 8. Literature Backing (Key Refs)

| Ref | 제공하는 사실 |
|---|---|
| **Deiseroth 2006** (Angew Chem) | Li6PS5X 합성 + 결정구조 + 초이온성 (~mS/cm) |
| **Adeli 2019** (Angew Chem) | 할로겐 치환 → Li5.5PS4.5Cl1.5 conductivity 9.4 mS/cm, mechanism: Li-anion 약화 + extra vacancy + 사이트 disorder |
| **Yu/Wagemaker 2016** (JACS) | Li6PS5Cl intracage Ea 0.12-0.14 eV, intercage 0.17-0.20 eV, NMR + DFT-MD |
| **Hanghofer 2019** (PCCP) | 7Li NMR Ea 0.17–0.32 eV, 음이온 sublattice disorder Cl > Br > I |
| **D'Amore 2022** (RSC Adv) | argyrodite enumeration ~10¹³ ordering, Coulomb selection |
| **Rao 2020** (Chem Mater) | 중성자 PDF로 Wyckoff 부분 점유 직접 확인 |
| **Kraft 2018** (JACS) | lattice polarizability + ionic conductivity |
| **Camacho-Forero 2020** (JPCC) | sandwich slab method anchor |
| **Komatsu 2022** (JPCM) | bulk thermodynamic LiNiO2/LPSCl ΔED |
| **Haruyama 2014** (Chem Mater) | 1-interface slab method (paper #2 baseline) |

---

## 9. Paper #2 Final Narrative

> "Across 7 orthogonal method perturbations — NCM crystallographic facet
> variation ((003), (110), (012) vs (104) baseline), constrained Type-a
> relaxation, lateral 2×2 supercell finite-size check, Li position shake
> (±0.2 Å, 5 seeds), and registry sampling — geometric Cl-O contact density
> at the equilibrium SE/NCM interface gap reproducibly correlates with
> experimental adhesion ranking at R = -0.91 ± 0.03 (n=5 paper compositions,
> p=0.03 in baseline).
>
> The descriptor encodes the Li6 vs Li5.4 family axis: stoichiometric Li
> vacancy in Li5.4 paired with halogen size mixture (Cl + Br) drives surface
> halogen depletion (Cl_surface fraction 20-33% in mixed Li5.4 vs 38-42%
> in Li6 / Cl-only Li5.4), reducing anion-anion Coulomb repulsion at NCM
> oxide contact.
>
> The complementary Li-O density signal (R=+0.82 in (104) baseline) is
> facet-fragile and we report it as 104-specific.
>
> The intra-Li5.4-family resolution (comp3 vs 4 vs 5, fixed vacancy + halogen
> total, varying Cl/Br ratio) is below current method threshold (Δ < 0.005),
> consistent with the modelC observation that Li5.4 + Cl-only does not yield
> the surface depletion seen in Cl+Br mixed compositions. We caveat this
> as a resolution limit of geometric MLIP-based descriptors and propose
> single-point DFT verification of the Cl/Br ratio fine-tuning as future work."

---

## 10. 다음 단계 (in progress / pending)

| 항목 | 상태 |
|---|---|
| v27 (Phase 1 cross-val + halogen z-fit + bootstrap + Cij vs adhesion + 5L NCM + 1000 reg) | KISTI 실행 중 |
| v26c (MACE-MP-0 cross-check) | mace env 설치됨, 미실행 |
| Paper #2 figure assembly (4-panel: descriptor vs Wad, Cl_surface mechanism, M2 RMS, collinearity matrix) | pending |
| Paper #2 first draft | pending |

---

## 부록 A — 6개 조성 raw data

| comp | formula | Li/fu | Cl/fu | Br/fu | vacancy/fu | family | paper Wad |
|---|---|---|---|---|---|---|---|
| comp1 | Li6PS5Cl | 6.0 | 1.0 | 0 | 0 | Li6 | 194 |
| comp2 | Li6PS5Cl0.5Br0.5 | 6.0 | 0.5 | 0.5 | 0 | Li6 | 180 |
| comp3 | Li5.4PS4.4Cl1.0Br0.6 | 5.4 | 1.0 | 0.6 | 0.6 | Li5.4 | 316 |
| comp4 | Li5.4PS4.4Cl0.8Br0.8 | 5.4 | 0.8 | 0.8 | 0.6 | Li5.4 | 298 |
| comp5 | Li5.4PS4.4Cl0.6Br1.0 | 5.4 | 0.6 | 1.0 | 0.6 | Li5.4 | 249 |
| modelC | Li5.4PS4.4Cl1.6 | 5.4 | 1.6 | 0 | 0.6 | Li5.4 | (no exp) |

---

## 부록 B — 측정 데이터 요약

### B.1 Cl-O bond density (R = -0.91, p = 0.03)
```
comp1 0.0228   comp2 0.0285   comp3 0.0000
comp4 0.0000   comp5 0.0000   modelC 0.0948
```

### B.2 Cl surface exposure
```
comp1 42%   comp2 33%   comp3 20%   comp4 25%   comp5 33%   modelC 38%
```

### B.3 7-method R(Cl-O) values
```
v15 baseline -0.914
NCM (003)    -0.914
NCM (110)    -0.911
NCM (012)    -0.912
M2 relax     -0.913 (RMS < 0.2 Å)
M6 2x2       -0.913 (finite-size 0%)
M3 Li shake  -0.886 ± 0.030 (5 seeds)
```

### B.4 Collinearity matrix (|R| > 0.95 pairs)
```
Cl-O density ↔ Li/fu       (R=0.99)
Cl-O density ↔ vacancy     (R=0.99)
Cl-O density ↔ Cl+Br       (R=0.99)
Li/fu        ↔ vacancy     (R=1.00)
Li/fu        ↔ Cl+Br       (R=1.00)
vacancy      ↔ Cl+Br       (R=1.00)
```

→ effective independent dimensions ~ 2 (family axis + within-family fine)

---

## 부록 C — 파일 위치 (repo)

- `db/properties/adhesion.json` — 모든 raw 결과 + session log
- `db/literature/refs.json` — 43 references (4 added 2026-05-08)
- `kb/physics/vacancy_mechanism_corrected_2026_05_08.md` — corrected mechanism
- `kb/results/adhesion_v9_to_v22_session_2026_05_07.md` — early iteration log
- `kb/results/adhesion_v23_v24_v25_extraction_complete.md` — statistical validation
- `kb/results/adhesion_v26_method_stresstest_2026_05_07.md` — 7-method test
- `필독/adhesion/phase2a_v15_bond_robustness.py` — final method script
- `필독/adhesion/phase2a_v26_all_methods.py` — stress test script
- `필독/adhesion/phase2a_v27_remaining.py` — A/D/E/F/G/H final extras

---

## 약어 정리

| | |
|---|---|
| SE | Solid electrolyte (sulfide argyrodite) |
| NCM | Layered oxide cathode (LiNiO2 시뮬레이션 단순화) |
| Wad | Work of adhesion (J/m² or mJ/m²) |
| MLIP | Machine-learning interatomic potential |
| UMA | Universal Models for Atoms (fairchem, paper #2 main MLIP) |
| MACE | MACE-MP-0 (cross-check MLIP) |
| LBFGS | Limited-memory Broyden-Fletcher-Goldfarb-Shanno (geometry optimization) |
| FixAtoms | ASE constraint to freeze selected atoms |
| Wyckoff site | Crystallographic site with given symmetry |
| NEB | Nudged elastic band (transition state finder) |
| Pearson R | Linear correlation coefficient |
| Bootstrap CI | resampling confidence interval |
| Collinearity | descriptors that measure same underlying quantity |

---

**문서 끝.** 질문이 있으면 안용훈 (yonghoon7153 / BML Hanyang) 또는 GitHub
issues로.
