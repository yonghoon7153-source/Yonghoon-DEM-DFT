---
title: B₂O₃ 원고 (BO-LPSC1.6 · paper #2) Computational Methods 초안 — 기록대로 쓴 것
date: 2026-10-20
updated: 2026-10-20
tags: [b2o3, manuscript, methods, paper2]
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---

# B₂O₃ 원고 (BO-LPSC1.6) — Computational Methods 초안 (2026-10-20)

**트랙**: B₂O₃ 원고는 **사용자가 1저자가 아니다** (CLAUDE.md §소통). 이 문서는 사용자가 원고에 넣을
**계산 방법 절**을 사용자의 요청 (10-20 *'맞고 틀린거 여부 따지지말고 한 부분 관련해서 method 작성'*) 대로
**우리 기록에 있는 실제 설정**으로 쓴 초안이다. 결과의 옳고 그름은 여기서 다루지 않는다.
형식은 사용자가 준 method docx 의 *"2.5. Computational Methods"* 단락 (수동태 · 문단형 · 참고문헌 위첨자) 을 따랐다.

- `[ ]` 안은 원고에 넣기 전에 채우거나 확인할 자리다.
- 참고문헌 자리는 `[QE]` 같은 꼬리표로 두었다 (번호는 원고 쪽에서 매긴다).

---

## 본문 (붙여넣기용)

**2.X. Computational Methods**

First-principles calculations were performed using Quantum ESPRESSO (QE) within the Perdew–Burke–Ernzerhof (PBE) form of the generalized gradient approximation (GGA).[QE][PBE] Pseudopotentials from the SSSP efficiency library (ultrasoft for Li, B, P, S, and Cl; projector augmented-wave (PAW) for O) were employed with a plane-wave kinetic energy cutoff of 60 Ry and a charge density cutoff of 480 Ry.[SSSP] Brillouin zone sampling was conducted using Γ-centered Monkhorst–Pack grids, and Marzari–Vanderbilt smearing with a width of 0.01 Ry was applied. Ionic positions were relaxed until the residual forces were below 10⁻⁴ Ry bohr⁻¹ (10⁻³ Ry bohr⁻¹ for O-LPSC1.6), with a convergence threshold of 10⁻⁸ Ry for the self-consistent field (SCF) cycles.

LPSC1.6 was modeled with a 62-atom supercell (Li27P5S22Cl8, five formula units), in which the primitive argyrodite cell (a ≈ 7.0 Å, α = 60°) is stacked five times along the c axis. To account for anion and Li⁺ disorder, representative configurations were obtained through atomistic sampling using the Universal Model for Atoms (UMA) machine-learning interatomic potential.[UMA] All 45 distributions of S²⁻ and Cl⁻ over the free-anion (4a/4d) sites were evaluated with UMA, Li⁺ configurations were sampled for the lowest-energy anion arrangements, and the lowest-energy candidate was annealed by UMA-based molecular dynamics (MD) at 500 K for 50 ps before DFT optimization. O-LPSC1.6 was modeled by replacing one S²⁻ with O²⁻ in the same cell (Li27P5S21OCl8, corresponding to Li5.4PS4.2O0.2Cl1.6); among four candidate sites (one free S²⁻ site and three PS4 corner sites), the configuration with the lowest UMA energy was adopted. BO-LPSC1.6 was modeled by doubling the LPSC1.6 supercell along the c axis and incorporating one B2O3 unit, in which two B³⁺ ions occupy P⁵⁺ (4b) sites, three O²⁻ ions occupy S²⁻ sites, and four additional Li⁺ ions compensate for the charge difference (Li58P8B2S41O3Cl16, 128 atoms, corresponding to Li5.8P0.8B0.2S4.1O0.3Cl1.6). The dopant configurations were pre-screened by their Ewald electrostatic energies and relaxed with UMA, and the lowest-energy configuration was then optimized by DFT. Because one B2O3 unit is the smallest substitution that can be represented in this cell, the model corresponds to x = 0.2, which is higher than the dopant content of the synthesized BO-LPSC1.6 (x = 0.03).

To obtain the equilibrium volume (V0) and bulk modulus (B0), each DFT-optimized cell was isotropically scaled to a series of volumes (V/Vref = 0.96–1.06 in 11 steps for LPSC1.6, 0.94–1.06 in 7 steps for O-LPSC1.6, and 0.96–1.04 in 5 steps for BO-LPSC1.6), and the ionic positions were relaxed at each volume with the cell shape and volume fixed. The energy–volume data were fitted to the third-order Birch–Murnaghan equation of state,[BM] and the ionic positions were finally relaxed at the fitted V0. Variable-cell relaxation was not used because a single static configuration of the disordered argyrodite does not retain the cubic symmetry of its time-averaged structure. The V0 structures were used for all subsequent analyses.

The density of states (DOS) and projected DOS (PDOS) of BO-LPSC1.6 were obtained from a non-self-consistent calculation using the optimized tetrahedron method[TET] followed by projection onto atomic orbitals, and were broadened with a Gaussian function of 0.05 eV for display. The valence band maximum (VBM) was taken from the Kohn–Sham eigenvalues of a non-self-consistent calculation with fixed occupations, and energies are referenced to the VBM. The electron localization function (ELF)[ELF] was calculated from the SCF valence charge density, and the ELF value at the midpoint of each bond was averaged over all bonds of the same type, identified with distance cutoffs of 2.15 (B–S), 1.9 (P–O), 2.3 (P–S), 2.9 (Li–S), and 2.95 Å (Li–Cl). Crystal orbital Hamilton population (COHP) analysis[COHP] was performed with LOBSTER 5.1.1.[LOBSTER] Because LOBSTER requires PAW wavefunctions, the SCF and non-self-consistent (no symmetry, 960 bands) calculations were repeated for the same structure using PAW datasets from PSlibrary,[PSL] and the wavefunctions were projected onto the pbeVaspFit2015 basis (Li 1s, 2s, 2p; B and O 2s, 2p; P, S, and Cl 3s, 3p), resulting in a charge spilling of 1.19%. The integrated COHP (ICOHP) up to the Fermi level was averaged over each bond type. Bond lengths were averaged over first-coordination-shell pairs in the V0 structures (P–S 1.8–2.5, P–O 1.3–1.9, B–S 1.5–2.2, Li–S 1.9–3.2, and Li–Cl 2.0–3.4 Å).

Li⁺ transport was simulated by MD using the UMA-s-1p1 model (OMat task) combined with the Atomic Simulation Environment (ASE).[UMA][ASE] The V0 cells (62 atoms for LPSC1.6 and O-LPSC1.6 and 128 atoms for BO-LPSC1.6) were simulated in the NVT ensemble using a Langevin thermostat with a time step of 2 fs and a friction coefficient of 0.02 (ASE units) at 600, 800, and 1000 K. At each temperature, a 5 ps equilibration was followed by a 200 ps production run, and independent runs with different random seeds were performed (three for LPSC1.6 and BO-LPSC1.6, and four for O-LPSC1.6). The Li⁺ diffusion coefficient (D) was obtained from a linear fit of the Li⁺ mean square displacement (MSD), MSD(t) = 6Dt + c, over 2–50 ps with a free intercept c. The activation energy (Ea) was determined from the Arrhenius relation, D = D0 exp(−Ea/kBT), and the ionic conductivity was estimated from the Nernst–Einstein relation, σ = nq²D/(kBT), assuming a Haven ratio of 1, with D extrapolated to [XXX K].

Li⁺ migration pathways were analyzed by the bond valence site energy (BVSE) approach on the V0 structures.[BVSE][softBV] On a real-space grid with a spacing of ~0.25 Å, the bond valence sum of a Li⁺ probe, VLi = Σ exp[(R0 − R)/b], was evaluated over anions within 5 Å using the softBV parameters (R0 = 2.105, 2.249, and 1.466 Å for Li–S, Li–Cl, and Li–O, respectively; b = 0.37 Å), and the site-energy landscape was approximated by the squared bond valence mismatch, (VLi − 1)². The Li⁺-accessible volume fraction was defined as the fraction of grid points whose value lies within 0.5 (valence units)² of the global minimum of the periodic map. For visualization, the periodic maps were resampled into ~9.9 Å near-cubic boxes.

---

## 참고문헌 후보 (꼬리표 → 서지)

| 꼬리표 | 서지 | 상태 |
|---|---|---|
| [QE] | P. Giannozzi et al., *J. Phys.: Condens. Matter* 21, 395502 (2009) | paper #1 Methods 에서 확정 (`kb/papers/computational_methods_draft.md`) |
| [PBE] | J. P. Perdew, K. Burke, M. Ernzerhof, *Phys. Rev. Lett.* 77, 3865 (1996) | 같음 |
| [SSSP] | G. Prandini et al., *npj Comput. Mater.* 4, 72 (2018) | 같음 |
| [UMA] | B. M. Wood et al., arXiv:2506.23971 (2025) | 같음 |
| [BM] | F. Birch, *Phys. Rev.* 71, 809 (1947) | 같음 |
| [BVSE] | R. P. Rao, S. Adams, argyrodite BVSE (2011) | litdb 있음 `litdb/papers/rao2011_argyrodite_se_studies_bvse.md` — 권·쪽은 그 digest 에서 |
| [softBV] | H. Chen, S. Adams, *IUCrJ* 4, 614 (2017) | ⚠ 로컬 PDF 없음 — 서지 확인 필요 |
| [ASE] | A. H. Larsen et al., *J. Phys.: Condens. Matter* 29, 273002 (2017) | ⚠ 서지 확인 필요 |
| [TET] | M. Kawamura, Y. Gohda, S. Tsuneyuki, *Phys. Rev. B* 89, 094515 (2014) | ⚠ 서지 확인 필요 |
| [ELF] | A. D. Becke, K. E. Edgecombe, *J. Chem. Phys.* 92, 5397 (1990) | ⚠ 서지 확인 필요 |
| [COHP] | R. Dronskowski, P. E. Blöchl, *J. Phys. Chem.* 97, 8617 (1993) | ⚠ 서지 확인 필요 |
| [LOBSTER] | S. Maintz et al., *J. Comput. Chem.* 37, 1030 (2016) (pbeVaspFit2015 기저도 여기) | ⚠ 서지 확인 필요 |
| [PSL] | A. Dal Corso, *Comput. Mater. Sci.* 95, 337 (2014) | ⚠ 서지 확인 필요 |

CLAUDE.md §원고 작성: 레퍼런스는 로컬 PDF / litdb digest 기준 · 인용 역할 확인 후 삽입 — ⚠ 표시는 그 확인을 아직 안 한 것이다.

---

## 빈칸 · 확인할 것

1. **`[XXX K]`** — Nernst–Einstein 외삽 온도. 아래 '원고 숫자의 출처' 2 번과 같이 본다.
2. **B·O 유사포텐셜 파일 이름** — b2o3 SCF 의 `ATOMIC_SPECIES` 는 저장소에 없다 (KISTI 백업 `b2o3_eos/` 에만).
   근거로 쓴 것: Li·P·S·Cl 은 modelc 입력 (`tools/electronic/standard_dos/modelc/modelc_scf.in`) 에서 확인 ·
   B 는 `tools/electronic/icohp_paw_kisti.sh` 머리 주석 *"the champion SCF used USPP (P/S/B)"* ·
   O 는 우리 세트의 O 가 모두 `O.pbe-n-kjpaw_psl.0.1.UPF` (PAW). 이 조합이 SSSP efficiency 세트와 같다.
   ⇒ 원본 입력의 B·O 두 줄이 `b_pbe_v1.4.uspp…` · `O.pbe-n-kjpaw_psl.0.1…` 이면 본문 그대로 확정.
3. 절 번호 `2.X` · 참고문헌 번호.

## 원고 숫자의 출처 — Methods 와 맞추려면 볼 곳 (판단 없이 위치만)

| 원고 | 숫자 | 우리 기록에서 나온 곳 | Methods 문장과의 관계 |
|---|---|---|---|
| 8 번 문단 MD | *"for 60 ps"* | 생산 200 ps · MSD 맞춤 창 2–50 ps (`tools/ionic/run_lpsocl_md.sh` `--prod_ps 200` · `md_protocol_generations.json` gen0 생산길이 200) | 60 ps 와 200 ps 중 하나로 맞춘다 |
| 8 번 문단 MD | RT σ 8.7 (BO) · 6.5 (LPSC1.6) mS cm⁻¹ | **273 K** 외삽 · 단일 시드 판 (`b2o3_vs_modelc_md.json` `comparison.verdict_SUPERSEDED` *"sigma273 8.7 vs 6.5"* · 그 판의 Ea 0.2234/0.2235) | 같은 문단의 Ea 0.197/0.198 (3-시드 판) 과 판이 다르다 · 외삽 온도 칸 |
| 8 번 문단 MD | Ea · σ 전체 | `citation_hazards.json` **HZ-b2o3-md-ea (BLOCKED)** | 같이 읽기 때 8 번 문단에서 본다 (open_items z19 줄) |
| 9 번 문단 BVSE | 4.37 · 3.40 · 6.74 % | 4.37 (LPSC1.6) · 3.40 (O-LPSC1.6) = **표시용 입방 상자** 값 · 6.74 (BO) = **원래 주기 셀** 값 (`bvse_cubic_approx/bvse_orig_vs_cubic.json` `_key_numbers_iso0.5_pct` · `bvse_b2o3/b2o3_orig_bvse_summary.json`) | 원래 셀로 통일하면 3.32 / 4.74 / 6.73 % (CLAUDE.md BVSE 규율: 정량·순위는 원래 셀 값만 · 상자 ±1.3 %p) |
| 12 번 문단 EOS | *"Murnaghan equation of state"* | 3 차 Birch–Murnaghan (`b2o3_eos_dft_result.json` `method` · `eos.json` modelc_v3) | Methods 는 Birch–Murnaghan 으로 썼다 |
| 3 번 문단 · 모델 | O-LPSC1.6 이 BO 와 *"same amount of O"* | 실험 시료 이야기다 — 모델은 O 0.2 /f.u. (O-LPSC1.6) vs 0.3 /f.u. (BO-LPSC1.6) | Methods 에 모델 조성을 그대로 적었다 |

## 문장별 근거 (기록 위치)

| 문장 | 값 | 근거 |
|---|---|---|
| QE PBE · 60/480 Ry · MV 0.01 Ry · conv_thr 1e-8 · forc 1e-4 | b2o3 EOS 입력 생성기 | `tools/doping/b2o3_dft_eos.py` (`ecutwfc=60` · `degauss=0.01` · `forc_conv_thr=1.0d-4`) · `db/properties/b2o3_dos_gap.json` `method` *"USPP 60/480 Ry"* |
| O-LPSC1.6 힘 문턱 1e-3 | | `db/properties/lpsocl_eos_dft_result.json` `method` *"forc_conv_thr 1e-3"* |
| LPSC1.6 62 원자 · a 7.007 · c 35.036 · 60° | | `db/structures/modelc_V0_k663.xyz` |
| 45 음이온 배열 · Li 표본 · 500 K 50 ps 어닐 | | `db/compositions/modelc.json` `pipeline_v2` · `modelc_v3.json` `pipeline_v2_lineage_full` |
| O-LPSC1.6 후보 4 자리 (free-S 1 · PS₄ 꼭짓점 3) · UMA 최저 | | `db/structures/lpsocl_candidates/README.md` |
| BO-LPSC1.6 128 원자 · B@P 2 · O@S 3 · +4 Li · Ewald → UMA → DFT | | `kb/results/b2o3_champion_coordination_2026_06_29.md` §1 · `kb/methodology/b2o3_doping_chemistry.md` §5.7 |
| EOS 부피 범위 · 점 수 | 11 / 7 / 5 | `db/properties/eos.json` (modelc_v3 · v096–v106) · `lpsocl_eos_dft_result.json` (0.94–1.06) · `b2o3_eos_dft_result.json` (0.96–1.04) |
| 고정셀 이유 | | `kb/methodology/computational_methods_canonical.md` §3-1 |
| DOS tetrahedra_opt · 0.05 eV 표시 · VBM 고정점유 nscf | | `b2o3_dos_gap.json` `method` · `tools/electronic/standard_dos/b2o3/fig_b2o3_dos.py` |
| ELF pp.x plot_num 8 · 결합 중점 · 거리 문턱 | | `db/properties/b2o3_elf_bonds.csv` 꼬리 줄 · `tools/figures/sample_elf_bonds.py` `CUT` |
| LOBSTER 5.1.1 · PAW · 960 밴드 · pbeVaspFit2015 · spilling 1.19 % | | `db/properties/b2o3_icohp.json` `method` · `tools/electronic/icohp_paw_kisti.sh` |
| 결합 길이 창 | | `tools/comp1_v3/b2o3_all_bond_lengths.py` `cat_anion` |
| MD UMA-s-1p1 omat · Langevin 2 fs · 0.02 · 5 + 200 ps · 600/800/1000 K · 시드 3/4/3 · 2–50 ps 자유절편 · NE Haven 1 | | `tools/modelc_v3/disorder_ensemble_diffusion.py` 인자 · `tools/ionic/run_lpsocl_md.sh` · `db/properties/b2o3_md_arrhenius.json` `FINAL_for_paper.method` · `b2o3_vs_lpscl16_msd.csv` · `lpsocl_md_arrhenius.json` |
| BVSE softBV R0 · b 0.37 · 5 Å · ~0.25 Å · iso 0.5 · 9.9 Å 상자 | | `bvse_cubic_approx/bvse_orig_vs_cubic.json` `_method` · `bvse_b2o3/b2o3_orig_bvse_summary.json` |
