# Argyrodite 기계적 물성 예측을 위한 Multi-scale Computational Pipeline

> [!important] CANONICAL PIPELINE — 모든 향후 계산은 이 protocol 따름
> 이 document는 paper #1 (halogen substitution) + paper #2 (Nd-doping) 둘 다 적용되는 ==**표준 multi-scale pipeline**==. 단계 생략 없이 Step 1 → 8 모두 수행.

Argyrodite 고체전해질은 두 가지 disorder를 갖고 있다. 첫째, 4a/4c site에서 S²⁻와 halogen(Cl⁻/Br⁻)의 배치가 여러 가지 가능하고, 둘째, 48h site에서 Li⁺가 절반만 채워져 있어서 어떤 site를 차지하느냐에 따라 물성이 달라진다. 이 두 disorder를 체계적으로 처리하기 위해 MLIP와 DFT를 결합한 단계적 pipeline을 설계하였다.

---

## Step 1. Halogen Site Enumeration

pymatgen을 이용하여 4a/4c site에 S, Cl, Br을 배치하는 모든 경우의 수를 열거한다 (조성에 따라 56~70개 configuration). 이 단계에서 Li는 건드리지 않는다 — halogen 배치만 체계적으로 탐색한다.

예: Li₆PS₅Cl (conventional cell, 4 f.u.) → 4a 4개 + 4c 4개 = 8 free sites 중 Cl 4개 배치 → C(8,4) = 70 configs.

## Step 2. Two-Stage MLIP Screening — Halogen → Li

Halogen과 Li의 disorder를 동시에 탐색하면 경우의 수가 폭발하므로 (halogen 70개 × Li C(48,24) = 12억), 2-stage 분리 전략을 사용한다.

**Stage 2a: Halogen screening.** 대표 Li 배열 1개를 고정한 상태에서 70개 halogen config를 MLIP relaxation으로 비교하고 가장 안정한 halogen 배치를 선택한다. 이 단계는 halogen site preference (4c vs 4a)를 결정한다.

**Stage 2b: Li screening.** Best halogen 배치를 고정한 상태에서 48h site 중 24개 (Li₆ 경우) 또는 27개 (Li₅.₄ 경우)를 random으로 선택한 20개 Li 배열을 MLIP relaxation으로 비교한다. Li 배열에 따른 에너지 차이 (energy spread)를 정량화하며, 이 값은 해당 조성의 Li ordering sensitivity를 나타낸다.

Li₆PS₅Cl에서 실측한 Li energy spread = 1162 meV — Li 배열에 따라 에너지가 1.2 eV까지 차이나며, 이는 Li ordering이 물성에 미치는 영향이 크다는 것을 의미한다.

## Step 3. Li Annealing — Thermal Li Re-optimization

Step 2에서 얻은 top 5 Li 배열에 대해 MLIP MD annealing (500K, 50~100ps)을 수행한다. 500K에서 Li⁺는 활발히 hopping하지만 (activation energy ~0.2 eV << kT = 0.043 eV), PS₄ framework (P-S 결합 ~3.5 eV >> kT)와 halogen (이온결합 cage)은 진동만 한다. 따라서 halogen 배치를 보존하면서 Li sublattice만 선택적으로 재최적화할 수 있다.

Annealing 후 MLIP relaxation을 수행하여 최종 에너지를 비교한다. 이 과정에서 screening ranking과 annealing ranking이 역전될 수 있다 — 실제 Li₆PS₅Cl에서 screening 4위였던 배열이 annealing 후 1위로 올라서는 현상이 관찰되었다. 이는 0K relaxation (screening)이 local minimum에 갇히는 반면, thermal annealing이 더 깊은 basin을 탐색하기 때문이다. Annealing 후 가장 에너지가 낮은 구조를 champion structure로 선택한다.

온도 선택 근거: 500K에서 Li⁺만 선택적으로 이동하고 (Ea ~0.2 eV), S²⁻는 PS₄ 내 공유결합 유지 (P-S ~3.5 eV), Cl⁻/Br⁻는 이동하지 않는다. 800K 이상에서는 Cl/Br hop이 시작되어 halogen enumerate 결과가 무너지고, 1500K 이상에서는 PS₄ framework 자체가 파괴될 수 있다.

## Step 4. MLIP EOS — V₀ 범위 파악

Champion structure에서 체적을 96%~108%로 균일하게 scaling하며 MLIP 에너지를 계산한다. Birch-Murnaghan fitting으로 평형 체적(V₀)의 예비값과 대략적인 B₀를 얻는다. 이 단계는 ~5분이면 끝나며, 다음 DFT 계산의 volume grid를 설정하는 데 사용한다.

## Step 5. DFT Relax — Basin 탐색

MLIP 좌표를 출발점으로 각 volume point에서 DFT relaxation (cell fixed, atoms free)을 수행한다. 여기서 핵심은 basin 일관성 확인이다 — 서로 다른 volume에서 relaxed된 좌표를 cross-check하여 같은 energy basin에 있는지 검증한다. 만약 다른 basin이 발견되면 (예: comp5에서 421 meV 더 안정한 Basin A 발견), 해당 좌표로 전체 EOS를 재계산한다. 각 volume point에 약 3시간 소요된다.

특히 volume을 크게 확장하면 (v108, +8%) 격자가 넓어지면서 여러 원자가 동시에 재배열되어 새로운 basin으로 전환할 수 있다. 본 연구에서 comp5 v108에서 62개 원자 중 31개가 이동하는 전체 재배열이 관찰되었으며, Model C에서도 28/62 원자가 재배열되었다. 이는 BM EOS fitting 범위를 v106(+6%)까지로 제한하는 근거가 된다.

Step 3의 Li annealing을 통해 champion structure가 이미 깊은 basin에 있으므로, DFT relax 단계에서 basin 전환 위험이 줄어든다. 이것이 pipeline v1 (annealing 없음)에서 심각했던 basin 문제를 완화하는 핵심 메커니즘이다.

## Step 6. DFT EOS — B₀ 결정

DFT relaxed 좌표와 Step 4에서 파악한 volume 범위로 E-V 곡선을 구성하고, 3rd-order Birch-Murnaghan EOS fitting으로 B₀, B₀', V₀를 결정한다. Basin이 일관된 volume point만 사용하며 (R² > 0.9999 목표), basin 전환이 발생한 점은 제외한다.

## Step 7. V₀ 좌표 확정

EOS fitting에서 결정된 V₀에 가장 가까운 volume point의 좌표를 최종 구조로 확정한다. 해당 volume에서 DFT relax가 수행되지 않았다면, 인접 volume의 좌표를 V₀ cell에 넣고 추가 DFT relax를 수행한다. 확정된 좌표에서 tight SCF (conv_thr = 1×10⁻¹⁰)를 수행하여 정밀한 charge density를 얻는다.

## Step 8. Post-processing

확정된 좌표에서 일련의 post-processing을 수행한다.

**전자구조**: NSCF 계산 (동일 prefix 필수)으로 eigenvalue를 구한 뒤, DOS로 band gap을, PDOS(projwfc.x)로 원소별 전자구조 기여를 분석한다.

**전하 분석**: Bader charge analysis (pp.x → bader)로 원자별 유효 전하를 구하여 이온성 변화를 정량화한다. Rhombohedral cell에서는 FFT grid 문제로 all-electron charge (plot_num=21) 사용을 권장한다.

**결합 분석**: 좌표에서 PBC 거리 계산으로 Li-S, Li-Cl, Li-Br, P-S bond length를 측정한다.

**탄성 물성**: DFT finite strain (±0.005, 6 strain patterns × positive/negative = 12 SCF)으로 0K clamped-ion elastic tensor를 계산한다. 이 값은 Li ordering에 민감하며 (comp5에서 ΔC44 = 12.7 GPa, 47%), 특히 shear resistance에서 변동이 크다. 보다 실험에 가까운 값을 얻기 위해 MLIP MD snapshot method (600K MD → 5 snapshots → quench → relaxed-ion Cij → VRH average)로 finite-temperature elastic constants를 계산한다. 이 방법은 thermal Li disorder를 자연스럽게 포함하여 C44 과대평가 문제를 해소한다.

---

## Appendix: NCM/SE 계면 접착 에너지 (Wad) 계산

SE/NCM 계면의 work of adhesion을 MLIP (UMA)으로 계산한다. 핵심 과제는 (1) SE와 NCM의 lattice mismatch 최소화, (2) Li₅.₄ 조성의 vacancy를 계면 모델에 보존하는 것이다.

### Cell 선택

Argyrodite SE cell과 NCM (LiNiO₂) hexagonal cell의 lattice mismatch를 최소화하기 위해, SE를 2×2×1로 repeat하고 NCM을 5×5×1로 확장한다.
- comp1/2 (Li₆, cubic primitive a ≈ 6.97 Å): SE prim 2×2×1 (52 atoms) + NCM 5×5×1 (300 atoms), strain = +3.3%
- comp3/4/5 (Li₅.₄, rhombo a ≈ 7.12 Å): SE 2×2×1 (248 atoms) + NCM 5×5×1 (300 atoms), strain = +1.1%

두 경우 모두 NCM 5×5×1을 사용하므로 cross-composition 비교가 공정하다.

### Surface-only MQA Protocol

종래의 melt-quench 방법 (3000K)은 SE를 완전히 녹여 amorphous 계면을 생성하지만, vacancy site를 파괴한다. 본 연구에서는 lattice match가 확보되었으므로 melt가 불필요하며, 대신 surface-only MQA (Melt-Quench-Anneal)를 적용한다.

1. SE 2×2×1 slab을 NCM 5×5×1 위에 gap 2.5 Å로 stacking
2. **800K surface softening (2 ps)** — 표면 원자만 약간 재배치. Li⁺는 hopping하고 표면 S²⁻가 미세 이동하지만, bulk 구조와 vacancy는 2 ps 내 변하지 않음.
3. **300K quench (2 ps)** — 표면 구조 동결
4. **500K Li anneal (3 ps)** — Li sublattice 최적화. Vacancy 보존.
5. **100K cool (2 ps)** + MLIP relaxation

이전 v3/v4에서 800K가 artifact를 유발한 원인은 온도가 아니라 lattice mismatch (±20%)였다. Lattice match가 확보된 v5에서는 800K surface softening이 안전하다.

### 통계: z-cut sampling

SE slab의 z 방향을 5등분하여 서로 다른 layer를 NCM 접촉면으로 노출한다 (z-shift = 0.0, 0.2, 0.4, 0.6, 0.8). 각 z-cut에서 vacancy 노출 정도가 다르므로:
- Li₆ (vacancy 없음): 모든 z-cut에서 Wad 유사 → 분산 작음
- Li₅.₄ (vacancy 있음): vacancy가 표면에 노출되는 z-cut에서 Wad 증가 → 분산 큼

Wad의 조성 간 평균 차이와 함께, Li₅.₄의 큰 분산 자체가 vacancy chemical anchor 효과의 증거이다.

---

## 🚨 모든 후속 작업 — 이 pipeline 따름

### Paper #1 (halogen substitution)
- comp1, comp2, comp3, comp4, comp5, modelC 모두 Step 1-8 적용
- v2 anneal champion 사용
- DFT EOS 11 points + BM3 fit
- Adhesion: surface-only MQA + xy-shift sampling

### Paper #2 (Nd-doping in modelC)
- O placement candidates (categories A-G):
  - **A**: 3 PS3O distributed
  - **B**: 2 PS3O + 1 free O
  - **C**: 1 PS3O + 2 free O
  - **D**: 3 free O (Track 1B)
  - **E**: 1 PS2O2 + 1 PS3O (cis/trans)
  - **F**: 1 PS2O2 + 1 free O
  - **G**: 1 PSO3 alone
- ==**모든 candidates Step 1-7 수행**== (Step 8 post-processing은 winner만)
- 단계 생략 없음

### 절대 skip 금지 단계
- Step 3 (Li annealing) — basin convergence 위해 필수
- Step 4 (MLIP EOS) — V0 estimate 필수
- Step 5-6 (DFT EOS basin check) — paper-quality essential
- Step 7 (V0 coordinate 확정) — 모든 post-processing의 foundation

---

#pipeline #canonical #protocol #multi-scale #DFT #MLIP #argyrodite
