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

## 7. 동적 (Dynamical) Descriptors

| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| MSD (Mean Squared Displacement) | MD simulation | UMA-MD or DFT-MD | 이온 mobility 직접 |
| Diffusion coefficient (D) | MSD slope | analysis | σ = nq²D/(kT) |
| Activation entropy (ΔS‡) | NEB at multiple T | NEB + statistics | 동적 자유도 |
| Phonon density of states | DFPT | phonopy + DFT | 진동 모드 |
| Debye temperature (θ_D) | from phonon DOS | phonopy | 열역학 |

---

## 8. ML/통계 Descriptors (derived)

| Descriptor | 계산 | 도구 | 의미 |
|-----------|------|------|------|
| SOAP fingerprint | local env | dscribe | structural ML feature |
| MBTR (many-body tensor) | many-body | dscribe | composition + structure |
| ACSF (atom-centered symmetry) | radial+angular | dscribe | atomic environment |
| OFM (orbital field matrix) | electron config | matminer | composition feature |
| Magpie features | elemental properties | matminer | quick composition descriptor |

---

## 9. 검증 절차 — 새 소재 평가 시 워크플로우

1. **Tier-1 빠른 평가** (~10분/소재):
   - Cl-O density, S-O density, Li-O density (UMA + bond_density_36reg_FAST.py)
   - Composite descriptor (Cl-O + Li-O − S-O)
   - Predicted W_ad rank
2. **Tier-2 정량 평가** (~1시간/소재):
   - 완전한 binding curve (UMA 36-reg × 16-gap)
   - α-corrected W_ad
   - Halogen depth profile
3. **Tier-3 robustness** (~3시간/소재):
   - Vacancy migration test
   - Li migration NEB
   - Surface termination γ sweep
4. **Tier-4 DFT spot check** (~24시간/소재, 새 chemistry만):
   - HSE06 single-point on UMA-relaxed structure
   - Band gap, work function
   - Validation against UMA

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
