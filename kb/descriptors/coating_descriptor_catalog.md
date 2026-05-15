# 황화물 코팅 소재 Descriptor Catalog

> 전고체 복합양극 황화물 코팅 / argyrodite SE 시스템의 모든 가능한
> descriptor를 카테고리별로 정리. ML screening + mechanism 해석의 reference.

---

## 0. Descriptor 우선순위 (현재 paper 검증)

본 연구에서 **paper W_ad와 강한 상관 (|R| > 0.9)** 으로 검증된 descriptor:

| Descriptor | R vs paper | 부호 | 카테고리 |
|------------|-----------:|:---:|----------|
| **Cl-O density** | +0.975 | + | 표면 contact |
| **S-O density** | −0.973 | − | 표면 contact (Pauli) |
| **Li-O density** | +0.771 | + | 표면 contact (인력) |
| Vacancy ΔW_ad | (family split) | + (Li₅.₄) | 동적 (Li 이동성) |
| Bulk Cl content (Li₅.₄) | +0.97 | + | composition |

이들이 **Tier-1 descriptors**. 새 소재 평가 시 우선 계산.

---

## 1. 구조 (Structural) Descriptors

### 1.1 Bulk structure
| Descriptor | 계산 방법 | 도구 | 의미 |
|-----------|---------|------|------|
| Lattice constants (a, b, c) | DFT/UMA relax | ase, pymatgen | NCM과 mismatch 정량 |
| Cell volume / fu | V/Z | ase | 압력/strain 추정 |
| Bond lengths (Li-S, P-S, ...) | nn analysis | pymatgen NN | 결합 강도 indicator |
| Coordination numbers (CN) | Voronoi/cutoff | pymatgen, dscribe | 이온 환경 |
| Anion site occupancy (4a/4d) | XRD-like analysis | pymatgen SymmetryAnalyzer | disorder 정량 |
| Ionic radius matching | Shannon radii lookup | dscribe + lookup | site 호환성 |

### 1.2 Surface/Interface structure
| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| Surface energy γ | E_slab − N×E_bulk | UMA + ase | thermodynamic 표면 안정성 |
| Surface termination atoms | z-profile analysis | ase | "Li2S vs LiCl 종단" 등 |
| Lattice mismatch with NCM | (a_SE − a_NCM)/a_NCM | manual | strain 예측 |
| Interface atom density (per nm²) | 36-reg avg | bond_density_36reg_FAST.py | **검증됨** |
| **Cl-O, S-O, Li-O contact density** | 36-reg avg | 위 스크립트 | **★ Tier-1, 검증됨** |
| Halogen depth (Cl, Br z-position) | manual z analysis | comprehensive_FINAL_analysis.py | 표면 vs bulk |
| 14-pair contact density (Li-M, S-Li, ...) | 36-reg avg | 위 스크립트 | 추가 contacts |

### 1.3 Defect / disorder
| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| Li vacancy concentration | (6 − Li per fu) | from formula | Li₅.₄ vs Li₆ |
| Anion site disorder (S↔X) | DFT energy diff | UMA SCFs | 4a/4d swap energy |
| Defect formation energy | E_defect − E_perfect | UMA | dopant stability |
| Configurational entropy | k log(W) | combinatorics | mixed 조성 |

---

## 2. 전자 (Electronic) Descriptors

| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| Band gap (Eg) | DFT DOS | VASP/QE (HSE06) | 전기적 절연성 |
| Work function (Φ) | E_vac − E_F | DFT slab | Fermi level alignment |
| Electronic DOS at E_F | DOS analysis | pymatgen | 전자 전도성 |
| Madelung potential at site | sum k·q_i/r_i | manual / pymatgen | site-specific 안정성 |
| Bader charges | charge analysis | DFT + Bader | 실제 이온 전하 |
| Charge transfer at interface | Δρ analysis | DFT | 계면 chemistry |
| Dipole moment | dipole calc | DFT slab | 계면 전기장 |

> **참고**: UMA는 energy/force만 직접 제공. 전자 정보는 DFT 보조 필요.

---

## 3. 전기화학 (Electrochemical) Descriptors

| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| Li migration barrier (Ea) | NEB | ase NEB + UMA | 이온 전도성 |
| Ionic conductivity (σ) | NEB + Arrhenius | NEB → KMC | 핵심 SE 지표 |
| Decomposition energy | grand potential phase diagram | pymatgen analyzer | 화학적 안정성 |
| Electrochemical window (V vs Li/Li⁺) | phase diagram | pymatgen | 사용 가능 전압 범위 |
| Voltage vs Li | ΔG/nF | DFT formation energies | 활성화 전위 |
| Mixed conductivity (ionic + electronic) | combined | 위 둘 결합 | 종합 SE 성능 |
| Coulombic efficiency (proxy) | reactivity at interface | DFT reaction E | 사이클 안정성 추정 |

---

## 4. 기계 (Mechanical) Descriptors

| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| Bulk modulus (B) | E(V) fit | DFT + Birch-Murnaghan | 압축 저항 |
| Shear modulus (G) | strain-stress | DFT | sliding 저항 |
| Young's modulus (E) | from B, G | E = 9BG/(3B+G) | 강도 |
| Poisson's ratio (ν) | from B, G | ν = (3B−2G)/(2(3B+G)) | 변형 거동 |
| Anisotropy index (A_U) | tensor analysis | aelas / pymatgen | 방향 의존성 |
| Hardness (Vickers proxy) | empirical | from G/B | scratch 저항 |
| Fracture toughness | empirical | 추정 | crack 저항 |

> UMA + ase로 elastic tensor 계산 가능. 자세한 건 `scripts/descriptors/elastic.py` (구현 예정).

---

## 5. 계면 (Interfacial) Descriptors — 본 연구 핵심

| Descriptor | 계산 | 도구 | 검증 상태 |
|-----------|------|------|----------|
| **Adhesion energy W_ad** | UMA binding curve | adhesion/ scripts | ★ R=+0.989 검증됨 |
| Equilibrium gap d_eq | Morse fit | plot_R0988_TIGHT_FIT.py | ★ 검증됨 |
| Strain correction ΔW_strain | E_NCM(SE cell) − E_NCM(NCM cell) | run_v30u_1L_correct_eiso_fix.py | ★ 검증됨 |
| Surface anion-O contact ratio | 위 14-pair | bond_density_36reg_FAST.py | ★ 검증됨 |
| Family-uniform dW vs per-comp dW | comparison | alpha_sensitivity_FINAL.py | ★ 검증됨 |
| Vacancy-driven ΔW_ad | rigid migration test | run_li_migration_FINAL_combo.py | ★ 검증됨 |
| Composite descriptor (Cl-O + Li-O − S-O) | weighted sum | derived | ★ 검증됨 (paper rank) |

---

## 6. 조성 (Compositional) Descriptors

| Descriptor | 계산 | 의미 |
|-----------|------|------|
| Halogen ratio (Cl/Br/I/F) | from formula | 표면 chemistry 결정 |
| Li content (per fu) | from formula | vacancy density |
| Cation diversity (Shannon entropy) | -Σ p_i log p_i | configurational entropy |
| Cation electronegativity (Pauling) | weighted avg | bonding character |
| Ionic radius weighted avg | weighted Shannon | lattice strain 예측 |
| Polarizability sum | weighted | through-space 효과 |
| Z_eff (effective nuclear charge) | empirical | core-electron 효과 |

---

## 7. 동적 (Dynamical) Descriptors — ★ MLIP-AIMD가 핵심

UMA의 진짜 가치 = **DFT-AIMD 대비 10,000배 빠름** → 스크리닝 가능.
DFT-AIMD: ~100,000 CPU-h/system → 무리. UMA-AIMD: ~1-10 GPU-h/system → ✅.

### 7.1 MLIP-AIMD 핵심 descriptor (Tier-1.5 — bond density 다음으로 중요)

| Descriptor | 계산 방법 | 정량 | 의미 |
|-----------|---------|------|------|
| **Diffusion coefficient D** | MSD slope (NVT MD) | Å²/ps | 이온 mobility 직접 |
| **Ionic conductivity σ** | Nernst-Einstein: σ=nq²D/kT | mS/cm | **핵심 SE 지표** |
| **Activation energy Ea** | Arrhenius (multi-T MD) | eV | 온도 의존성 |
| **Anion site disorder** | 4a/4d swap 통계 (50:50 sampling) | swap/ns | **comp4 frustration 해결** |
| **Interface stability under T** | RDF 변화, atom drift | qualitative | 분해 없는지 |
| **Vacancy migration rate** | real dynamics (NEB 보다 정확) | hops/ns | barrier에 의한 kinetic |

### 7.2 MLIP-AIMD 표준 protocol

| 단계 | 목적 | 시간 | T |
|------|------|------|---|
| Equilibration | 안정화 | **5-10 ps NVT** | target T |
| Production | sampling | **50-200 ps NVT** | target T |
| Multi-T sweep (Arrhenius) | Ea 추출 | 위 × 3-5 온도 | 300, 500, 700, 900 K |
| Time step | numerical stability | 1-2 fs | — |
| Thermostat | NVT | Langevin or Nose-Hoover | — |

### 7.3 MLIP-AIMD 도구

```python
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units

calc = make_uma_calc()  # UMA-s-1p1
atoms.calc = calc
MaxwellBoltzmannDistribution(atoms, temperature_K=600)
dyn = Langevin(atoms, 1*units.fs, temperature_K=600, friction=0.01/units.fs)
dyn.run(100000)  # 100 ps
```

또는 **atomate2 통합** (자동화):
```python
from atomate2.forcefields.flows.md import MDMaker
flow = MDMaker(force_field_name="UMA",
               n_steps=100000, time_step=1.0,
               temperature=600).make(structure)
```

### 7.4 우리 프로젝트 활용 사례

1. **Comp4 frustration 해결**: 50:50 Cl/Br의 anion site disorder를 UMA-MD
   sampling으로 평균화 → static frame artifact 제거 (paper의 기존 한계 해소).
2. **Ionic conductivity 직접 계산**: 모든 100+ 도핑 후보의 σ를 NEB 대신 직접
   AIMD로 측정 → screening 정확도 ↑.
3. **Interface 열적 안정성**: 600K NVT 100 ps로 LPSCl/coating 계면이
   유지되는지 직접 관찰.
4. **vacancy migration dynamics**: NEB의 single-path 한계 극복, multi-path
   sampling.

### 7.5 추가 dynamical (선택)

| Descriptor | 계산 | 도구 |
|-----------|------|------|
| Phonon DOS | DFPT (DFT) | phonopy + DFT |
| Debye temperature θ_D | from phonon DOS | phonopy |
| Thermal conductivity κ | Boltzmann transport | phono3py (DFT 비쌈) |
| Specific heat C_v | from phonon DOS | phonopy |

---

## 7.6 MLIP-AIMD 후처리 분석 (post-processing)

MLIP-AIMD trajectory에서 추가로 추출 가능한 핵심 정량값:

### 구조 분석
| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| **RDF (Radial Distribution Function)** | g(r) of atom pairs | ase.geometry, MDAnalysis | local ordering, phase change |
| **Pair correlation g(r,t)** | time-dependent g(r) | scipy + custom | dynamic ordering |
| **Coordination number evolution** | nearest-neighbor count vs t | pymatgen Voronoi | bond breaking/forming |
| **Bond angle distribution** | angle of triplets | custom | structural distortion |
| **Local order parameter (q4, q6)** | Steinhardt | freud | crystal vs amorphous |

### 동적 분석
| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| **VAF (Velocity Autocorrelation)** | <v(0)·v(t)> | numpy | dynamics, vibrational |
| **VDOS (vibrational DOS from MD)** | FT(VAF) | scipy.fft | phonon-like info (DFPT 없이!) |
| **MSD (Mean Square Disp)** | <|r(t)-r(0)|²> | numpy | ★ 이온 mobility (Tier-1) |
| **Non-Gaussian parameter α2** | <r⁴>/<r²>² − 3/5 | custom | jump diffusion vs liquid |
| **Van Hove correlation** | self-part Gs(r,t) | freud, MDAnalysis | hop dynamics |

### 자유에너지 (선택, 비쌈)
| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| Free energy ΔF | Thermodynamic Integration (TI) | i-PI, plumed | phase transition |
| Free energy surface (FES) | Metadynamics (MTD) | plumed + MD | reaction coordinate |
| Umbrella sampling | window biasing | plumed + WHAM | activation barriers |

### 반응 / 화학 (advanced)
| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| **Bond breaking events** | bond cutoff dynamics | custom + ase | reaction kinetics |
| Reaction rates | counting + Arrhenius | custom | k(T) |
| Decomposition products | composition over time | ase + Voronoi | interface stability |

---

## 7.7 정적 (Static) DFT 후처리 — 전자 구조 + 결합 분석

### 7.7.1 전자 구조
| 항목 | 도구 | 의미 |
|------|------|------|
| **DOS / PDOS** (총/원자별/orbital별) | sumo, pymatgen, LOBSTER | metallic vs insulator + 원자 기여 |
| **Band structure** | sumo-bandplot | direct vs indirect gap, dispersion |
| **Band gap E_g** | bandstr 분석 | 전자 절연성 핵심 |
| **Work function Φ** | E_vac − E_Fermi (planar avg) | Fermi level alignment |
| **Born effective charges Z*** | DFPT | dielectric response |
| **Dielectric tensor ε** | DFPT or LR | polarization |

### 7.7.2 전하 / 결합 분석 (★ BML 슬라이드 핵심)

| 항목 | 도구 | 측정 방식 | 의미 |
|------|------|----------|------|
| **Bader charge** | Henkelman bader + chgsum | basin (전하 basin 적분) | 정확한 원자 charge, 이온성 정량 |
| **Mulliken charge** | LOBSTER, VASP/QE 직접 | atomic orbital projection | 전통적 charge, 빠름 |
| **Löwdin charge** | LOBSTER, QE | symmetric orthogonalization | Mulliken 대비 basis 의존성 ↓ |
| **DDEC6 charge** | chargemol | combined basin + AO | charge + bond order 동시 |
| **COHP (★ BML)** | **LOBSTER** | bonding vs antibonding | **bond strength 정량** (음 = bonding, 양 = antibonding) |
| **ICOHP (integrated to E_F)** | LOBSTER | COHP 적분 | **bond strength 단일값** (eV/bond) |
| **COBI / COOP** | LOBSTER | 다른 분해 방식 | bond order 추가 |
| **ELF (★ BML)** | VASP + ELFCAR | 전자 localization (0~1) | 공유결합(>0.5) vs 이온결합(<0.3) |
| **Charge density Δρ** | ρ_AB − ρ_A − ρ_B | arithmetic on chgcar | 계면 charge transfer |

### 7.7.3 이온 전도 사전 분석 (★ BML 슬라이드 핵심)

| 항목 | 도구 | 의미 |
|------|------|------|
| **BVSE (Bond Valence Site Energy)** | **softBV, pymatgen.bvse** | Li⁺ migration 경로 가시화 (qualitative, 빠름, no DFT) |
| **BVS (Bond Valence Sum)** | pymatgen | site별 valence 일치 정도 |
| **Migration percolation analysis** | BVSE iso-surface | 3D 연결성 (1D/2D/3D pathway) |
| **NEB barrier (Tier-3, 정확)** | atomate2 NEB | 정량 Ea (BVSE 후속 검증) |

→ **워크플로우**: BVSE로 후보 path 식별 (분 단위) → NEB로 정량 (시간 단위)
→ 비싸지 않은 dry-run으로 NEB 시간 절약.



---

## 7.8 표면 / 형태 (Surface / Morphology)

| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| **Surface energy γ(hkl)** | E_slab − N×E_bulk | atomate2 surface workflow | facet stability |
| **Wulff construction** | min γ에 따른 equilibrium 형태 | pymatgen.analysis.wulff | particle shape |
| **Adsorption energies** | ΔE for species on surface | atomate2 ads workflow | reactivity sites |
| **Surface stress σ_surf** | strain derivative | DFT slab | structural relaxation |
| **Surface reconstruction** | comparison stoich vs reconstructed | DFT relax | metastability |

---

## 7.9 결함 (Defects) — Sundar paper의 핵심 영역

| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| **Vacancy formation energy** | E[X−v] − E[X] − μ_atom | atomate2 defects | thermodynamic stability |
| **Charged defect E_form (q)** | + Freysoldt correction | pymatgen-analysis-defects | charge-state diagrams |
| **Defect transition levels** | crossover q1/q2 | pymatgen Defect Compatibility | trap states |
| **Migration barrier (NEB)** | CI-NEB | atomate2 NEB workflow | ionic conductivity input |
| **Migration multiple paths** | NEB + AIMD comparison | both | most likely path |

---

## 7.10 실험 비교 (Experimental fingerprints)

| 항목 | 계산 | 도구 | 의미 |
|------|------|------|------|
| **XRD pattern** | 구조 → 회절 | pymatgen.analysis.diffraction | 실험 비교 |
| **Phonon dispersion** | DFPT or finite displacement | phonopy | dynamic stability + 적외선/Raman |
| **NMR shielding** | GIPAW | QE-GIPAW | 실험 NMR |
| **Mössbauer** | hyperfine | DFT EFG | Fe/Sn 동위원소 |
| **EELS / XAS** | core-hole DFT | corelevel codes | edge spectra |
| **STEM-EDS density profile** | atomic position 비교 | ase + custom | 실험 STEM |

---

## 7.11 Pareto 다목적 평가 (Multi-objective)

ML screening 마지막 단계 — 모든 descriptor 종합 ranking:

| 목적 함수 | 방향 | 가중치 (suggested) |
|----------|------|------------------|
| **W_ad (UMA)** | maximize (강한 결합) | 0.30 |
| **σ_ionic** (AIMD) | maximize (전도성) | 0.25 |
| **σ_electronic** (DOS) | minimize (절연성) | 0.20 |
| **ΔE 분해 (Tier-0)** | minimize |ΔE| (안정) | 0.10 |
| **Bandgap E_g** | maximize (전자 절연) | 0.05 |
| **Cost / safety** | composition-based filter | 0.10 |

도구: BoTorch + Ax (NSGA-II 또는 qEHVI) → Pareto front.



| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| SOAP fingerprint | local env | dscribe | structural ML feature |
| MBTR (many-body tensor) | many-body | dscribe | composition + structure |
| ACSF (atom-centered symmetry) | radial+angular | dscribe | atomic environment |
| OFM (orbital field matrix) | electron config | matminer | composition feature |
| Magpie features | elemental properties | matminer | quick composition descriptor |

---

## 7.12 BML 슬라이드 매핑 (직접 1:1)

본 catalog가 BML 발표 슬라이드의 모든 항목을 cover함을 명시:

### LPSCl / LPSCl₁.₆ Bulk Comparison

| 슬라이드 항목 | 본 catalog 위치 | 도구 / 방법 | Tier |
|--------------|---------------|-----------|------|
| **Structure** (relax) | §1.1, §3 | atomate2 RelaxMaker (UMA / DFT) | 1 |
| **BVSE** | §7.7.3 | softBV, pymatgen.bvse | 1.5 |
| **PDOS / DOS** | §7.7.1 | sumo, pymatgen | 2 |
| **ELF** | §7.7.2 | VASP + ELFCAR | 2 |
| **Band gap** | §7.7.1, §2 | bandstructure 분석 | 2 |
| **Mulliken / Löwdin Charge** | §7.7.2 | LOBSTER | 2 |
| **COHP (Bond strength)** | §7.7.2 | LOBSTER (ICOHP integrated) | 2 |
| **Bader Charge** | §7.7.2 | Henkelman bader | 2 |
| **Young's Modulus** (Hard) | §4 | DFT elastic + B,G,E,ν | 3 |
| **NEB** (Hard) | §3 (electrochem), §7.7.3 | atomate2 NEB | 3 |
| **AIMD** (Hard) | §7.1-7.6 | UMA-MD (10⁴× faster than DFT-AIMD) | 1.5 |

### Li / LPSCl Interface

| 슬라이드 항목 | 본 catalog 위치 | 도구 / 방법 | Tier |
|--------------|---------------|-----------|------|
| **Structure** (interface relax) | §1.2 | atomate2 + slab generation | 1 |
| **Adhesion energy W_ad** | §5 | UMA W_ad ★ R=+0.989 검증 | 1 |
| **SEI (decomposition products)** | §7.13 (다음 절) | DFT 반응 + 산물 식별 | 3 |

---

## 7.13 SEI / 분해 산물 분석 (★ BML 슬라이드 명시)

LPSCl + Coating + Li 사이에서 형성될 수 있는 SEI 분해 산물 평가.

### 단계 1 — 후보 산물 enumeration (Materials Project + DFT)
| 항목 | 도구 | 의미 |
|------|------|------|
| **반응 enthalpy ΔE** | MP API + Reaction Calculator | thermodynamic driving force |
| **Phase diagram (compositional)** | pymatgen.analysis.phase_diagram | 안정 상 식별 |
| **Decomposition pathways** | grand potential PD | 다단계 반응 가능성 |
| **Charged species** | electrochemical phase diagram | 산화 환원 환경 |

### 단계 2 — 각 산물 properties (Sundar 2025 흡수)
| 산물별 평가 | 도구 | 의미 |
|------------|------|------|
| **Bandgap E_g** | DFT (HSE06) | 전자 절연성 |
| **Li migration barrier** (NEB) | atomate2 NEB | 이온 전도성 |
| **Bulk modulus B + Young E** | DFT elastic | 기계적 안정성 |
| **Bader / COHP / ELF** | LOBSTER + bader | 결합 character + 이온성 |

### 단계 3 — 종합 SEI quality score
$$S = w_1 \cdot \log(\sigma_{Li}) + w_2 \cdot E_g - w_3 \cdot |\Delta E| + w_4 \cdot B$$

좋은 SEI: 높은 σ_Li (이온 전도), 큰 E_g (전자 절연), 작은 |ΔE| (안정), 적당한 B (mechanical).

### Nd₂O₃ → SEI 산물 catalog (BML 슬라이드)

| 산물 | 형성 가능성 | E_g (예상) | σ_Li (예상) | 평가 |
|------|-----------|----------|-----------|------|
| Li₂O | 매우 높음 | ~7 eV | 낮음 | bandgap 좋음, σ 부족 |
| Li₂S | 매우 높음 | ~3 eV | 낮음 | LPSCl 자체 종단과 유사 |
| LiCl | 매우 높음 | ~10 eV | 매우 낮음 | 절연체, σ 매우 낮음 |
| Li₃P | 가능 | ~3 eV | 매우 높음 (Li-rich) | ★ Li 전도 좋음 |
| LiP | 가능 | ~2 eV | 중간 | |
| Li₃PS₄ | 가능 | ~3 eV | 중간 | LPS 자체와 유사 |
| Li₃PO₄ | 가능 | ~7 eV | 낮음 | 산소 첨가 필요 |
| NdP | Nd 환원 | ? (계산 필요) | ? | metallic 가능성 |
| NdCl₃ | Nd-Cl 친화 | ~5 eV | 낮음 | ionic |
| NdOCl | mixed | ~4 eV | 낮음 | Cl + O 둘 다 |
| LiNdO₂ | Li-Nd-O | ~4 eV | 중간 | layered, Li 전도 가능 |
| Nd₂S₃ | Nd-S 친화 | ~2 eV | 낮음 | semicond |

→ **모든 후보를 atomate2 + UMA로 자동 평가** → SEI quality score 비교 →
가장 안정 + 전도성 좋은 산물 식별.

---

## 9. 검증 절차 — 새 소재 평가 시 워크플로우

1. **Tier-0 사전 필터** (~1초/소재) ★ Sundar 2025 흡수:
   - Materials Project API로 ΔE 추출 (LPSCl||Coating, Li||Coating, Cathode||Coating)
   - ΔE > -0.5 eV/atom 후보만 통과
2. **Tier-1 표면 contact density** (~10분/소재):
   - Cl-O density, S-O density, Li-O density (UMA + bond_density_36reg_FAST.py)
   - Composite descriptor (Cl-O + Li-O − S-O)
   - Predicted W_ad rank
3. **Tier-1.5 MLIP-AIMD** (~3-10시간/소재) ★ NEW:
   - **Diffusion D + ionic σ** (50-200 ps NVT @ 600K)
   - **Anion site disorder sampling** (frustrated 조성 해결)
   - **Interface thermal stability** (RDF, atom drift)
4. **Tier-2 정량 평가** (~1시간/소재):
   - 완전한 binding curve (UMA 36-reg × 16-gap)
   - α-corrected W_ad
   - Halogen depth profile
   - **Multi-T MLIP-AIMD → Arrhenius Ea** (~10-30시간 if 3-5 T)
5. **Tier-3 robustness** (~3시간/소재):
   - Vacancy migration test (rigid)
   - Li migration NEB barrier
   - Surface termination γ sweep
   - **Bandgap (HSE06 spot check)** ★ Sundar 흡수
6. **Tier-4 DFT validation** (~24-48시간/소재, top 후보만):
   - VASP HSE06 SCF on UMA-relaxed structure
   - **3-interface ΔE 정밀 계산** (vs. Materials Project Tier-0)
   - **DFT-AIMD spot validation** (10-20 ps, UMA-AIMD와 비교)
   - Bandgap, work function 정확값

---

## 10. 참고 — 우선순위 정당화

본 catalog에서 **Tier-1 descriptors (Cl-O, S-O, Li-O density)** 가 가장 중요한 이유:
- Paper 5-comp 검증에서 |R| > 0.97 확인됨
- 계산이 빠름 (no SCF, geometry만)
- Mechanism 해석 가능 (인력/반발 구분)
- 다른 SE/coating 시스템에 일반화 가능

**Tier-2 (vacancy migration, halogen depth)** 는 family-level mechanism 보강.

**Tier-3 (mechanical, electrochemical)** 은 실제 응용 검증 시 필수.

**Tier-4 (DFT)** 는 새 chemistry에서 UMA 신뢰도 의심될 때만.

---

## 도구 매핑 한눈에

| Descriptor 종류 | 1차 도구 | 2차 도구 |
|---------------|----------|----------|
| Structural | ase, pymatgen | spglib |
| Electronic | VASP, QE | sumo, pymatgen-analyzer |
| Electrochemical | NEB + UMA | pymatgen.analysis |
| Mechanical | DFT elastic | aelas |
| Surface contact (★) | bond_density_36reg_FAST.py | 우리 검증 도구 |
| Compositional | matminer | dscribe |
| Dynamic | MD (lammps + UMA) | phonopy |
| ML fingerprint | dscribe, matminer | modnet |

---

## 다음 단계

`scripts/descriptors/` 에 다음 구현 예정:
- `compute_tier1_descriptors.py` — 모든 Tier-1 자동 계산 (new material → R, ρ score)
- `compute_elastic.py` — UMA 기반 elastic tensor
- `compute_neb_barrier.py` — Li migration NEB
- `compute_surface_gamma.py` — surface energy z-shift sweep
- `compute_madelung.py` — site-specific Madelung potential
