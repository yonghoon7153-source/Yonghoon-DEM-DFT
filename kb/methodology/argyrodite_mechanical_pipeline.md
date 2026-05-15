# Argyrodite Mechanical Properties — Multi-scale Computational Pipeline (v2)

**작성일**: 2026-05-15
**상태**: pipeline v1 문서 (사용자 제공) + Pustorino 2025 / D'Amore 2022 / doping 파이프라인
경험까지 통합한 확장본
**적용 범위**: Li₆PS₅X (X = Cl, Br, I) argyrodite, 도핑 변종 (Nd, Mg, Al, Ag, O, F …),
그리고 LPSCl/NCM 계면 adhesion

---

## 0. Pre-flight Checklist — 가정과 사실의 분리

본격 step에 들어가기 전, 결과 해석의 분산을 최소화하기 위해 baseline 가정을 먼저
fix한다.

### 0.1 LPSCl baseline polymorph 선택 (D'Amore 2022 reference)

| Polymorph | 출처 | Phonon | B₀(298K) | 권장 용도 |
|-----------|------|--------|----------|-----------|
| F-43m cubic (mp-985592) | Materials Project default | imag (−146, −115 cm⁻¹) ⚠ | n/a | 비교용/논문 인용용만, 절대 baseline 금지 |
| P1 pseudo-cubic (Model 2, 24개 degenerate) | D'Amore Table 2 | real | **18.7 GPa** | 일반 screening (UMA 일관성 우선) |
| Pm monoclinic (Model 4) | D'Amore Table 2 | real | **~26 GPa** | true ground state, 정밀 B₀ 보고용 |

→ 본 repo는 `data/lpscl_bulk.cif` = pseudo-cubic P1 (UMA-relaxed, V/f.u. = 255 Å³,
`pseudo_cubic_P1` 라벨)을 기본으로 사용. monoclinic Pm으로 baseline 교체 시 모든
ΔE/atom, ΔV/V₀ 결과 재계산 필요.

### 0.2 Li ordering ensemble 선택 (Pustorino 2025 reference)

| Ordering | ΔE vs 24G (eV/f.u.) | V/f.u. (Å³) | 비고 |
|----------|----------------------|-------------|------|
| 24G (all 24g) | 0.00 (ref) | 269.3 | metastable, 단일 relax는 절대 금지 |
| 48H (all 48h) | −0.72 | 248.4 | stable |
| **48HR (48h, 50% 점유)** | **−0.80** | **254.1** | **ground state, 권장** |
| 48HR^inv (S/Cl 50% inv) | −0.73 | 241.8 | NMR 일치, B₀ 다르게 나옴 |

→ 본 repo는 48H_low (V/f.u. = 254.2) baseline 사용 (Pustorino 48HR 와 V 거의 동일).
ensemble 평균 보고 시 `--method random --n_seeds 5` (이상)으로 5 configurations.

### 0.3 EOS strain window 결정 (양 논문 공통)

| 윈도우 | 안전성 | 근거 |
|--------|--------|------|
| ±1% (elastic) | ✅ | Pustorino: ±1% 이상에서 24g→48h Li hop이 "shear instability"로 잘못 보고됨 |
| ±6% (BM EOS fit) | ⚠ | comp5 v108(+8%) 사례: 62 원자 중 31개 재배열, basin 전환 — fit 범위 v94~v106 제한 |
| ±8% (V₀ tail 확인용) | ❌ | 새 basin 진입 위험 → fit에 포함 금지, 좌표 cross-check만 |

### 0.4 Disorder 정의 (혼동 방지)

Argyrodite Li₆PS₅Cl는 **두 종류의 disorder**가 동시에 존재:

| Disorder type | site | 처리 step |
|---------------|------|-----------|
| **Anion site disorder** (S²⁻ ↔ Cl⁻) | 4a (S free) ↔ 4d (Cl) | Step 1 enumerate |
| **Li ordering disorder** (48h half-occupancy) | 48h site 24/48 occupancy | Step 2b screen + Step 3 anneal |

(주의: 문헌마다 "4a/4c" vs "4a/4d" 표기가 다름. Cubic F-43m 표준 Wyckoff는 **4a /
4d** — 본 문서는 4d 사용. comp5 등 본 그룹 내부 용어 "4c"는 4d와 동의어.)

---

## Step 1. Halogen Site Enumeration (Anion disorder)

pymatgen으로 4a/4d site에 S²⁻와 halogen(Cl⁻/Br⁻)을 배치하는 모든 조합을 열거.
**Li sublattice는 건드리지 않음** — halogen 배치만 체계적 탐색.

| 조성 | free anion sites | 배치 경우의 수 | 비고 |
|------|------------------|----------------|------|
| Li₆PS₅Cl (conv. cell, 4 f.u.) | 4a×4 + 4d×4 = 8 | C(8,4) = **70** | full Cl/S 교환 |
| Li₆PS₅Br | 동일 | 70 | Br 대체 |
| Li₆PS₅Cl₀.₅Br₀.₅ | 동일 + halogen 종 | ~210 | halogen sub-enum 추가 |
| Li₅.₄PS₄.₆Cl₁.₄ | Cl-rich | ~140 | Li vacancy 고려는 Step 2b |

도구: pymatgen `EnumlibAdaptor` 또는 ATAT SQS (special quasi-random structure)
→ 50% S/Cl inversion 표적인 경우 SQS 사용 (D'Amore 2022 §2 Methods).

**구현 위치 (repo)**: 별도 스크립트 없음 (Phase 1 build-out 항목).
→ TODO: `scripts/disorder/enumerate_anion.py` 신설 필요.

---

## Step 2. Two-Stage MLIP Screening — Halogen → Li

Halogen disorder × Li ordering disorder 동시 탐색은 경우의 수 폭발
(70 × C(48,24) ≈ 12억). 따라서 **2-stage 분리 전략**.

### Stage 2a — Halogen screening (대표 Li 1개 고정)

70개 halogen config × **1개 representative Li 배열** → UMA full relax + energy 비교.

- 도구: `fairchem.core` UMA-s-1p1, `FrechetCellFilter` + `FIRE`
- 수렴: fmax ≤ 0.05 eV/Å, max 300 steps
- 출력: 4d vs 4a Cl/S 우선 점유 비율 (site preference fraction)
- 시간: 70 구조 × ~10s/구조 ≈ **12분** (A100)

**구현 위치 (repo)**: `scripts/doping/run_uma_screening.py` 의 framework 재활용
가능 (현재 dopant-by-dopant loop, halogen-by-halogen으로 일반화 필요).

### Stage 2b — Li ordering screening (best halogen 고정)

Best halogen 배치 고정 → **48h site의 24개 (Li₆) 또는 27개 (Li₅.₄) random 점유** ×
**20개 seed** → UMA relax + 에너지 비교.

| 조성 | Li occupancy | random seeds | total relax |
|------|--------------|--------------|-------------|
| Li₆PS₅Cl | 24 of 48h | 20 | 20 |
| Li₅.₄PS₄.₆Cl₁.₄ | ~27 of 50h | 20 | 20 |

핵심 metric: **Li energy spread** (max − min over 20 seeds).
- Li₆PS₅Cl 실측: **1162 meV** (= Li ordering 영향 ≈ B₀ ±50%, Pustorino 2025와 정합)
- → 이 값이 큰 조성일수록 Step 3 anneal이 더 critical

**구현 위치 (repo)**: `scripts/doping/substitute_struct.py --method random --n_seeds N`
→ Li ordering ensemble 생성 기능은 이미 있음 (Pustorino 흡수). dopant 없는 순수
Li ordering 스크리닝은 `--dopant ""` 또는 신규 스크립트 필요.

---

## Step 3. Li Annealing — Thermal Re-optimization

Step 2b top-5 Li 배열에 대해 **MLIP MD annealing**.

### Protocol

| Phase | 온도 (K) | 시간 (ps) | 목적 |
|-------|---------|-----------|------|
| Heat | 0 → 500 | 5 | linear ramp |
| Anneal | **500** | 50~100 | Li hopping 활성화 |
| Quench | 500 → 0 | 10 | linear cool |
| Final relax | static | — | UMA relax fmax ≤ 0.05 |

### 온도 선택 근거 (정량)

| 종 | 결합 / hopping Eₐ | kT @ 500K | 500K 동작 | 안전 한계 |
|----|---------------------|-----------|-----------|-----------|
| **Li⁺** (48h ↔ 24g) | ≈ 0.2 eV | 0.043 eV | 활발 hop ✅ | ~300K부터 시작 |
| S²⁻ (PS₄ 내) | P-S 공유결합 ≈ 3.5 eV | — | 진동만 ✅ | T > 1500K → PS₄ 파괴 |
| Cl⁻ (4d cage) | 이온 결합 cage | — | 진동만 ✅ | **T > 800K → Cl hop** ⚠ |

→ **500K 권장**, 800K 이상 사용 금지 (halogen enumerate 결과 무너짐), 1500K 이상
PS₄ framework 파괴 (구조 비물리적).

### Annealing의 효과

- Screening 0K relax는 local minimum trap → ranking 부정확
- Anneal은 더 깊은 basin 탐색 → ranking 역전 가능
- **사례 (Li₆PS₅Cl)**: screening 4위 → anneal 후 1위 (champion structure)
- 이는 Step 5 DFT relax 단계의 basin 전환 위험을 사전 차단하는 효과

**구현 위치 (repo)**: 미구현. TODO: `scripts/doping/run_li_anneal.py` 신설.
ASE `LangevinNVT` + UMA calc 조합으로 50ps 정도 (A100에서 ~15분/구조).

---

## Step 4. MLIP EOS — V₀ 범위 파악

Champion structure 1개에 대해 volume scaling sweep.

| 항목 | 값 |
|------|-----|
| Volume grid | 96, 98, 100, 102, 104, 106, 108% of V₀ (7점) |
| 각 점 | isotropic strain, atoms full relax (cell fixed) |
| Fit | 3rd-order Birch-Murnaghan |
| 산출 | V₀ (Å³), B₀ (GPa), B₀' (unitless), R² |
| 시간 | 7 × ~30s = **3~5분** |

→ DFT EOS의 volume grid 사전 결정 + B₀ 1st guess (UMA의 PBE 일관성).

**구현 위치 (repo)**: `scripts/adhesion/uma_eos_pre_dft.py` (Nd doped EOS에 사용 중).

---

## Step 5. DFT Relax — Basin 탐색

각 volume point에서 DFT relax (cell fixed, atoms free). **핵심 = basin 일관성 확인**.

### Basin cross-check protocol

1. 모든 volume의 relaxed 좌표를 V₀ cell로 normalize
2. Pairwise atomic displacement (RMSD) 계산
3. **임계값 RMSD > 0.5 Å** → 다른 basin 진입 의심
4. 의심 케이스: 해당 좌표를 다른 volume에서 재시작 → 더 안정하면 새 basin
5. 새 basin 발견 시 전체 EOS 재계산

### 실측 basin 전환 사례 (본 그룹 기록)

| 사례 | volume | 재배열 원자 비율 | 에너지 차 | 처리 |
|------|--------|------------------|-----------|------|
| comp5 Basin A | v100 | — | **−421 meV** | 해당 좌표로 EOS 재시작 |
| comp5 v108 | +8% | **31/62 (50%)** | 새 basin | fit 범위 제한 (v94~v106) |
| Model C | +6% | **28/62 (45%)** | 새 basin | 동일 |

→ **BM EOS fit은 ±6% (v94~v106) 이내로 제한**. v108 좌표는 sanity check용으로만.

### 시간

- 각 volume × 약 **3시간** (QE-GPU, 52 atoms, K=2×2×1)
- 7 volumes × 2 GPUs (rank1+rank2 병렬) → **~24시간/pair**

Step 3 annealing이 깊은 basin을 사전에 잡기 때문에 v1 (annealing 없음) 대비 basin
전환 빈도 ↓. 이 부분이 v2 pipeline의 핵심 개선.

**구현 위치 (repo)**: `scripts/adhesion/sbatch_dft_eos_nd.sh` + `run_dft_eos_pair.sh`
+ `prepare_dft_eos_nd.py`. 현재 Nd 케이스 KISTI에서 진행 중.

---

## Step 6. DFT EOS — B₀ 결정

3rd-order BM fit on (V, E) points.

| 항목 | 기준 |
|------|------|
| Fit 범위 | v94 ~ v106 (basin 일관성 점만) |
| R² 목표 | **> 0.9999** |
| Outlier 처리 | basin 전환 점 제외 (Step 5 cross-check 결과 기반) |
| 산출 | V₀, B₀ (GPa), B₀' |

### 보고 시 필수 명시

1. **Polymorph** (pseudo_cubic_P1 / monoclinic_Pm)
2. **Li ordering** (24G / 48H / 48HR / 48HR_inv)
3. **Ensemble**: N seeds + mean ± std (Li ordering 분산이 B₀ ±15 GPa 가능)
4. **Strain window** (±6% basin-consistent)
5. **Reference**: Pustorino 2025 (Li ordering), D'Amore 2022 (polymorph), 그리고 본
   group v0 paper

→ 단일 baseline 의 B₀ 절대값 보고는 metric으로서 **신뢰성 부족**. 항상 ensemble
mean ± std 또는 dopant relative ΔB₀로 보고.

---

## Step 7. V₀ 좌표 확정

EOS V₀에 가장 가까운 grid point 좌표 채택. 없으면:
1. 인접 volume의 relaxed 좌표 → V₀ cell에 삽입
2. DFT relax 1회 추가
3. Tight SCF: `conv_thr = 1×10⁻¹⁰`, dense FFT grid

→ Step 8 post-processing 출발 좌표.

---

## Step 8. Post-processing — Properties

| 카테고리 | 계산 | 도구 | 산출 |
|----------|------|------|------|
| 전자구조 | NSCF (same prefix) → DOS + PDOS | QE projwfc.x | band gap, 원소별 기여 |
| 전하 분석 | pp.x (plot_num=21) → bader | Henkelman bader | 원자별 effective charge |
| 결합 길이 | PBC 거리 (좌표) | ase / pymatgen | Li-S, Li-X, P-S 분포 |
| 정적 elastic | DFT finite strain ±0.005 (6×2=12 SCF) | QE thermo_pw | C_ij at 0K clamped-ion |
| 동적 elastic | UMA-MD snapshot (600K → 5 snapshots → quench → C_ij → VRH) | ase + UMA | C_ij at finite T |

### 정적 vs 동적 elastic 비교 (comp5 실측)

| 방법 | C₄₄ (GPa) | 메시지 |
|------|-----------|--------|
| Static DFT clamped-ion | **27.2** | Li ordering 단일 snapshot에 매우 민감 |
| MD snapshot-averaged (600K) | **14.5** | thermal Li disorder 자연 포함 |
| ΔC₄₄ | **12.7 (47%)** | static이 shear resistance 과대평가 |

→ Shear modulus를 실험과 비교할 땐 **snapshot 방법 권장** (정적 DFT는 Li ordering
한 점 기준이라 변동 ±50% 가능, Pustorino 2025 정합).

### Rhombohedral cell 주의

- Bader charge: FFT grid 잘못되면 잘못된 charge → **all-electron charge (plot_num=21)
  사용 필수**, plot_num=0 (valence)는 비추.
- C_ij: cell 대칭 깨진 상태에서 strain pattern 적용하면 mode mixing 발생 → 6
  Voigt strain 모두 적용 필요 (단축 strain만 안 됨).

**구현 위치 (repo)**: `scripts/adhesion/sbatch_dft_eos_nd.sh` 안에 post-processing
phase 일부 + 미구현 (elastic snapshot은 별도 스크립트 필요).

---

## Appendix A. NCM/SE 계면 Wad 계산

본 그룹 v0 paper (R = +0.989) 검증된 protocol — 도핑 변종에도 그대로 적용.

### A.1 Cell 선택 (lattice mismatch 최소화)

| 조성 | SE primitive a (Å) | SE 2×2×1 | NCM hex a (Å) | NCM 5×5×1 | strain |
|------|---------------------|----------|----------------|------------|--------|
| Li₆ (comp1/2) | 6.97 cubic | 52 atoms | 2.86 | 300 atoms | **+3.3%** |
| Li₅.₄ (comp3/4/5) | 7.12 rhombo | 248 atoms | 2.86 | 300 atoms | **+1.1%** |

→ 두 조성 모두 NCM 5×5×1 공통 → cross-comp 공정 비교 OK.

### A.2 Surface-only MQA Protocol (Melt-Quench-Anneal)

전통적 3000K melt는 vacancy를 파괴 → 본 그룹 발견: lattice match 확보 시 melt
**불필요**. Surface-only MQA로 표면만 부드럽게 재배치:

| Phase | T (K) | t (ps) | 목적 |
|-------|-------|--------|------|
| 1. Stacking | — | 0 | SE 2×2×1 위 NCM 5×5×1, gap **2.5 Å** |
| 2. Surface softening | **800** | 2 | 표면 Li hop + S²⁻ 미세 이동; bulk 보존 (2 ps < bulk reorganization timescale) |
| 3. Quench | 300 | 2 | 표면 동결 |
| 4. Li anneal | **500** | 3 | Li sublattice 최적, vacancy 보존 |
| 5. Cool | 100 | 2 | 최종 안정화 |
| 6. UMA relax | static | — | fmax ≤ 0.05 eV/Å |

⚠ v3/v4에서 800K artifact 발생했던 진짜 원인은 **온도가 아니라 lattice mismatch
±20%**였음 → v5 (mismatch ≤ 3.3%)에서는 800K 안전.

### A.3 z-cut sampling (vacancy chemical anchor 통계)

SE slab z 방향 5등분 → 서로 다른 layer를 NCM 접촉면으로 노출:

| z-shift | 노출 layer | Li₆ (vacancy 없음) | Li₅.₄ (vacancy 있음) |
|---------|-----------|---------------------|----------------------|
| 0.0 | top | Wad ≈ ⟨W⟩ | vacancy 노출 → **W↑** |
| 0.2 | upper-mid | 동일 | partial 노출 |
| 0.4 | middle | 동일 | bulk-like |
| 0.6 | lower-mid | 동일 | partial |
| 0.8 | bottom | 동일 | vacancy 노출 → **W↑** |

→ **Li₆: 분산 작음**, **Li₅.₄: 분산 큼** (vacancy ⨯ z-cut interaction).

이 분산 자체가 **vacancy = chemical anchor**의 증거 (단순 평균만 보면 evidence가
약함). v0 paper §3.4의 핵심 신호.

### A.4 Wad 계산식 + correction

$$W_{ad}^{\text{raw}} = (E_{SE} + E_{NCM} - E_{SE/NCM}) / A$$

**Strain correction** (이종 SE에서 NCM이 받는 strain):
$$\Delta W_{strain} = E_{NCM}(\text{SE cell}) - E_{NCM}(\text{NCM cell})$$

**Cl-coherent termination + uniform Li5.4 dW = 0.44 J/m²** (v0 paper 검증된 값,
comp4 50:50 Cl/Br outlier 처리 포함).

$$W_{ad}^{\text{corrected}} = W_{ad}^{\text{raw}} - \alpha \cdot \Delta W_{strain}$$

→ **R = +0.989, ρ = +1.000** (5-comp 실험 vs UMA 검증, v0 paper Figure 5).

---

## Appendix B. Pipeline 단계별 구현 상태 (현 repo)

| Step | 설명 | 구현 위치 | 상태 |
|------|------|-----------|------|
| 0.1 Polymorph baseline | metadata + 라벨 | `scripts/doping/substitute_struct.py --polymorph` | ✅ |
| 0.2 Li ordering ensemble | random seed loop | `substitute_struct.py --method random --n_seeds N` | ✅ |
| 1. Halogen enumerate | C(8,4)=70 | (미구현) | 🔲 TODO `scripts/disorder/enumerate_anion.py` |
| 2a. Halogen screen | UMA relax loop | `scripts/doping/run_uma_screening.py` 재활용 가능 | 🔲 일반화 필요 |
| 2b. Li screen | random Li × 20 seeds | `substitute_struct.py + run_uma_screening.py` 조합으로 가능 | △ wrap script 필요 |
| 3. Li anneal | UMA-MD 500K 50ps | (미구현) | 🔲 TODO `scripts/doping/run_li_anneal.py` |
| 4. MLIP EOS | volume sweep + BM fit | `scripts/adhesion/uma_eos_pre_dft.py` | ✅ |
| 5. DFT relax (basin cross-check) | sbatch + RMSD check | `scripts/adhesion/sbatch_dft_eos_nd.sh` (basin check 수동) | △ RMSD 자동화 미구현 |
| 6. DFT EOS BM fit | scipy curve_fit | `scripts/adhesion/uma_eos_pre_dft.py` 재활용 | ✅ |
| 7. V₀ 좌표 확정 + tight SCF | post-relax + SCF | (수동) | 🔲 자동화 가능 |
| 8.a Electronic (DOS/PDOS) | NSCF + projwfc | `comp5_lpscbr/` 다수 .py | ✅ (KISTI 전용) |
| 8.b Bader charge | pp.x → bader | 동일 | ✅ |
| 8.c Bond length | PBC dist | 동일 | ✅ |
| 8.d Elastic static | finite strain ±0.005 | `comp5_lpscbr/mlip_elastic_0K_v2.py` | ✅ |
| 8.e Elastic MD-snapshot | 600K → 5 snap → quench | `comp5_lpscbr/mlip_elastic_300K_v2.py` 등 | ✅ |
| Appendix A: Wad | MQA + z-cut | `scripts/adhesion/run_adhesion_*.py` (v0 paper) | ✅ |
| Appendix A: α correction | strain | `scripts/adhesion/alpha_sensitivity_FINAL.py` | ✅ |

**TODO 우선순위** (가장 큰 빈 칸):
1. `scripts/doping/run_li_anneal.py` — Step 3 (이게 가장 critical)
2. `scripts/disorder/enumerate_anion.py` — Step 1
3. Basin cross-check 자동화 — Step 5

---

## Appendix C. 핵심 정량 reference (인용용)

| 수치 | 의미 | 출처 |
|------|------|------|
| F-43m imag phonon (−146, −115 cm⁻¹) | cubic LPSCl dynamically unstable | D'Amore PCCP 2022 |
| ΔE(Pm−P1) = −0.310 eV/f.u. | monoclinic이 true ground state | D'Amore Table 2 |
| ΔE(48HR−24G) = −0.80 eV/f.u. | 48HR ground state, mp-985592 metastable | Pustorino Table 2 |
| B₀ spread = 13.7 ~ 29.6 GPa | Li ordering + S/Cl inv 분산 | Pustorino Table 3 |
| B₀(pseudo-cubic) ≈ 18.7 GPa, B₀(monoclinic) ≈ 26 GPa | polymorph 분산 | D'Amore Fig 4 |
| α_LPSCl(298K) = 6.55×10⁻⁵ K⁻¹ | NCM α (~1×10⁻⁵)의 6× → CTE mismatch | D'Amore Fig 3 |
| (110) Wulff 점유 81% | dominant cleavage facet | D'Amore Fig 8 |
| γ((100)-Li2S-def) = 0.20 J/m² | LPSCl 가장 약한 cleavage | Pustorino Table 4 |
| Li energy spread (Li₆PS₅Cl) = 1162 meV | Li ordering sensitivity | 본 그룹 측정 |
| ΔC₄₄ (static − MD) = 12.7 GPa (47%) | static elastic 과대평가 | 본 그룹 comp5 |
| W_ad R = +0.989, ρ = +1.000 | UMA vs experimental Wad 검증 | 본 그룹 v0 paper |

---

## 변경 이력

| 날짜 | 변경 | 출처 |
|------|------|------|
| 2026-05-15 | v2 초안 (사용자 제공 v1 + Pustorino/D'Amore/doping 흡수) | this conversation |
| (TODO) | Step 1/3 코드화 후 Appendix B 상태 갱신 | future |

---

**관련 문서**:
- `kb/literature_db/pustorino_2025_lpscl_li_ordering_mechanical.md`
- `kb/literature_db/damore_2022_lpscl_symmetry_breaking_qha.md`
- `kb/literature_db/sundar_2025_lpscl_coating.md`
- `kb/descriptors/coating_descriptor_catalog.md` §4 (mechanical descriptors)
- `kb/methodology/doping_substitution_algorithm.md`
- `kb/papers/mechanism_anion_O_descriptor.md` (v0 paper 메커니즘)
