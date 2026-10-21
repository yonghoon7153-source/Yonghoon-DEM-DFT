---
title: B₂O₃ 원고 (BO-LPSC1.6 · paper #2) Computational Methods — 기록대로 · compact 판 (BML 가이드 반영)
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
형식은 사용자가 준 method docx 의 *"2.5. Computational Methods"* 단락을 따르고, 같은 날 받은 **BML 작성 가이드**
(`Writing_scientific_papers_BML_v1.docx` — 업로드 · 저장소 밖) 와 **교수님 어록 13 항** (시제 규칙 · 변수 italic · 빈칸 없이 ·
reference 정리 · 정의를 정확하게 · compact) 을 맞췄다 (적용 표는 Docs 문서 4 절).

- 빈칸 없음 — 외삽 온도는 기록대로 273 K. 남은 것은 아래 '확인할 것' 3 · 4 (원고 번호 합치기 · LPSC1.6/O-LPSC1.6 k 격자).
- 참고문헌은 이 절 안에서 처음 인용 순서로 [1]–[19] (원고 목록에 합칠 때 번호를 다시 매긴다).

---

## 본문 — compact 판 (2026-10-20 · Docs 문서와 같은 글)

> ⏩ **정본 편집본은 Docs 문서다**: https://claude.ai/artifact/T1VW5kXxfbi1ToVH7GxyuM
> (BML 작성 가이드 `Writing_scientific_papers_BML_v1.docx` + 교수님 어록 13 항 + method docx 형식 반영 · 문장별 설명 표 · 참고문헌 19 개 · 원고 숫자 출처 표).
> 첫 초안 (981 단어) 은 이 파일의 git 이력 (`5fcea55e`) 에 있다. 이 판은 891 단어.
> **Word 파일**: `kb/papers/b2o3_bo_lpsc16_methods_2026_10_20.docx` — 사용자가 준 method 템플릿 (`method___.docx`) 의 패키지를 그대로 쓰고 본문만 바꿨다: Times New Roman 12 pt · 2 줄 간격 · 첫 줄 들여쓰기 · italic 절 제목 '2.5.' · 인용은 문장부호 뒤 위첨자 [n] (원고 양식 · 10-21) · 첨자는 Word 첨자 · 수식 3 개는 Word 수식 개체 (OMML). 이 md 의 [n] 표기는 Word 에서 위첨자다.

**2.5. Computational Methods**

First-principles density functional theory (DFT) calculations were performed using Quantum ESPRESSO with the Perdew–Burke–Ernzerhof generalized gradient approximation.[1–4] Pseudopotentials from the SSSP efficiency library (ultrasoft for Li, B, P, S, and Cl; projector augmented-wave (PAW) for O) were used with kinetic energy cutoffs of 60 Ry for the wavefunctions and 480 Ry for the charge density.[5–7] The Brillouin zone was sampled with Γ-centered Monkhorst–Pack *k*-point grids (6 × 6 × 3, 2 × 2 × 1, and 3 × 3 × 1 for LPSC1.6, O-LPSC1.6, and BO-LPSC1.6, respectively),[8] and Marzari–Vanderbilt smearing of 0.01 Ry was applied (0.02 Ry for the structural relaxations of BO-LPSC1.6).[9] Ionic positions were relaxed until all force components fell below 10⁻⁴ Ry bohr⁻¹ (10⁻³ Ry bohr⁻¹ for O-LPSC1.6), with a self-consistent field (SCF) convergence threshold of 10⁻⁸ Ry.

Three structural models were constructed. LPSC1.6 was represented by a 62-atom supercell (Li₂₇P₅S₂₂Cl₈, five formula units) obtained by stacking the primitive argyrodite cell (*a* ≈ 7.0 Å, *α* = 60°) five times along the *c* axis. Its anion and Li⁺ disorder was sampled with the Universal Model for Atoms (UMA) machine-learning interatomic potential:[10] the 45 distributions of S²⁻ and Cl⁻ over the free-anion (4a/4d) sites were ranked by UMA energy, Li⁺ arrangements were sampled for the lowest-energy anion distributions, and the lowest-energy configuration was annealed by UMA-based molecular dynamics (MD) at 500 K for 50 ps. O-LPSC1.6 (Li₂₇P₅S₂₁OCl₈, i.e., Li₅.₄PS₄.₂O₀.₂Cl₁.₆) was obtained by replacing one S²⁻ with O²⁻ at the lowest-UMA-energy site among four candidates (one free S²⁻ site and three PS₄ corners). BO-LPSC1.6 (Li₅₈P₈B₂S₄₁O₃Cl₁₆, i.e., Li₅.₈P₀.₈B₀.₂S₄.₁O₀.₃Cl₁.₆; 128 atoms) was built by doubling the LPSC1.6 cell along *c* and introducing one B₂O₃ unit, with two B³⁺ on P⁵⁺ (4b) sites, three O²⁻ on S²⁻ sites, and four additional Li⁺ for charge compensation; its dopant configurations were pre-screened by Ewald electrostatic energy and relaxed with UMA. Because one B₂O₃ unit is the smallest substitution this cell can accommodate, the model corresponds to *x* = 0.2, which is higher than the experimental *x* = 0.03.

For each model, the UMA-optimized cell was isotropically scaled to 0.96–1.06 (LPSC1.6, 11 volumes), 0.94–1.06 (O-LPSC1.6, 7 volumes), or 0.96–1.04 (BO-LPSC1.6, 5 volumes) of its volume, and the ionic positions were relaxed by DFT at each fixed cell. The energy–volume data were fitted to the third-order Birch–Murnaghan equation of state to obtain the equilibrium volume (*V*₀) and bulk modulus (*B*₀),[11] and the ions were finally relaxed at *V*₀; these structures were used in all subsequent analyses. Variable-cell relaxation was not used because a single static configuration of disordered argyrodite does not retain the cubic symmetry of its time-averaged structure.

Li⁺ transport was simulated by MD with the UMA-s-1p1 model (OMat task) in the Atomic Simulation Environment (ASE).[10,12] The *V*₀ cells (62, 62, and 128 atoms for LPSC1.6, O-LPSC1.6, and BO-LPSC1.6, respectively) were simulated in the *NVT* ensemble with a Langevin thermostat (time step 2 fs, friction 0.02 in ASE units) at 600, 800, and 1000 K, with 5 ps of equilibration followed by 200 ps of production. At each temperature, three (LPSC1.6 and BO-LPSC1.6) or four (O-LPSC1.6) independent runs with different random seeds were performed. The Li⁺ diffusion coefficient (*D*) was obtained from a linear fit of the mean square displacement (MSD), MSD = 6*Dt* + *c*, over 2–50 ps with a free intercept *c*. The activation energy (*E*ₐ) was obtained by fitting Eq. (1) to *D* at the three temperatures, and the ionic conductivity (*σ*) was estimated from Eq. (2) with a Haven ratio of 1 and *D* extrapolated to 273 K by Eq. (1), where *n* is the Li⁺ number density and *q* is the Li⁺ charge.

```latex
D = D_{0}\exp\left(-\frac{E_{\mathrm{a}}}{k_{\mathrm{B}}T}\right) \qquad (1)
```

```latex
\sigma = \frac{n q^{2} D}{k_{\mathrm{B}} T} \qquad (2)
```

Li⁺ migration pathways were mapped with the bond valence site energy (BVSE) approach on the *V*₀ structures.[13,14] On a grid with ~0.25 Å spacing, the bond valence sum of a Li⁺ probe was computed over all anions within 5 Å using the softBV parameters (*R*₀ = 2.105, 2.249, and 1.466 Å for Li–S, Li–Cl, and Li–O, respectively; *b* = 0.37 Å), and the site energy was approximated by Eq. (3), where *R* is the Li⁺–anion distance. The Li⁺-accessible volume fraction was defined as the fraction of grid points within 0.5 (valence units)² of the global minimum of the periodic map; for display, the maps were resampled into ~9.9 Å near-cubic boxes.

```latex
E_{\mathrm{BV}} = \left(V_{\mathrm{Li}} - 1\right)^{2}, \quad V_{\mathrm{Li}} = \sum_{X} \exp\left(\frac{R_{0} - R}{b}\right) \qquad (3)
```

The density of states (DOS) and projected DOS (PDOS) of BO-LPSC1.6 were calculated non-self-consistently with the optimized tetrahedron method and projections onto atomic orbitals,[15] and were broadened with a 0.05 eV Gaussian for display. Energies were referenced to the valence band maximum (VBM), which was taken from the Kohn–Sham eigenvalues of a fixed-occupation calculation. The electron localization function (ELF) was calculated from the SCF valence density,[16] and its value at the bond midpoint was averaged over all bonds of each type (bonds identified within 2.15, 1.9, 2.3, 2.9, and 2.95 Å for B–S, P–O, P–S, Li–S, and Li–Cl, respectively).

Crystal orbital Hamilton population (COHP) analysis[17] was performed with LOBSTER 5.1.1.[18,19] Because LOBSTER requires PAW wavefunctions, the SCF and non-self-consistent (no symmetry, 960 bands) calculations were repeated on the same structure with PAW datasets from PSlibrary,[7] and the wavefunctions were projected onto the pbeVaspFit2015 basis (Li 1*s*, 2*s*, 2*p*; B and O 2*s*, 2*p*; P, S, and Cl 3*s*, 3*p*), with a charge spilling of 1.19%. Integrated COHP (ICOHP) values up to the Fermi level were averaged over each bond type. Bond lengths were averaged over first-shell pairs in the *V*₀ structures (P–S 1.8–2.5, P–O 1.3–1.9, B–S 1.5–2.2, Li–S 1.9–3.2, and Li–Cl 2.0–3.4 Å).

---

## 참고문헌 (원고 양식 · 19 개 · 2026-10-21)

원고 (`Manuscript.docx`, 사용자 10-21 업로드 · 저장소 밖) 의 Literature 양식: `번호.<tab>저자, *저널* 연도, *권*, 쪽.` — 제목·DOI 없음 · 본문 인용은 문장부호 뒤 위첨자 `[n]` (Wiley 꼴).
QE 는 공식 인용 안내 (https://www.quantum-espresso.org/cite/) 대로 2009 · 2017 · **2020 (GPU 판을 써서)** 셋 — 사용자 10-21 *'권고대로 해'*.
SSSP 는 고른 세트라 **원 라이브러리도 같이 인용** — 백업 입력으로 확인한 대응: Li·B·S·Cl = GBRV (6) · P·O = PSlibrary (7) — 사용자 10-21 *'권고대로 해줘'*.
Brillouin 영역 격자는 **Monkhorst–Pack 원 논문 (8)** 을 같이 인용 — 사용자 10-21 *'권고대로 해줘'* (3 번 문장).

1. P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso, S. de Gironcoli, S. Fabris, G. Fratesi, R. Gebauer, U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri, L. Martin-Samos, N. Marzari, F. Mauri, R. Mazzarello, S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, G. Sclauzero, A. P. Seitsonen, A. Smogunov, P. Umari, R. M. Wentzcovitch, *J. Phys.: Condens. Matter* 2009, *21*, 395502.
2. P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. Buongiorno Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, N. Colonna, I. Carnimeo, A. Dal Corso, S. de Gironcoli, P. Delugas, R. A. DiStasio Jr., A. Ferretti, A. Floris, G. Fratesi, G. Fugallo, R. Gebauer, U. Gerstmann, F. Giustino, T. Gorni, J. Jia, M. Kawamura, H.-Y. Ko, A. Kokalj, E. Küçükbenli, M. Lazzeri, M. Marsili, N. Marzari, F. Mauri, N. L. Nguyen, H.-V. Nguyen, A. Otero-de-la-Roza, L. Paulatto, S. Poncé, D. Rocca, R. Sabatini, B. Santra, M. Schlipf, A. P. Seitsonen, A. Smogunov, I. Timrov, T. Thonhauser, P. Umari, N. Vast, X. Wu, S. Baroni, *J. Phys.: Condens. Matter* 2017, *29*, 465901.
3. P. Giannozzi, O. Baseggio, P. Bonfà, D. Brunato, R. Car, I. Carnimeo, C. Cavazzoni, S. de Gironcoli, P. Delugas, F. Ferrari Ruffino, A. Ferretti, N. Marzari, I. Timrov, A. Urru, S. Baroni, *J. Chem. Phys.* 2020, *152*, 154105.
4. J. P. Perdew, K. Burke, M. Ernzerhof, *Phys. Rev. Lett.* 1996, *77*, 3865–3868.
5. G. Prandini, A. Marrazzo, I. E. Castelli, N. Mounet, N. Marzari, *npj Comput. Mater.* 2018, *4*, 72.
6. K. F. Garrity, J. W. Bennett, K. M. Rabe, D. Vanderbilt, *Comput. Mater. Sci.* 2014, *81*, 446–452.
7. A. Dal Corso, *Comput. Mater. Sci.* 2014, *95*, 337–350.
8. H. J. Monkhorst, J. D. Pack, *Phys. Rev. B* 1976, *13*, 5188–5192.
9. N. Marzari, D. Vanderbilt, A. De Vita, M. C. Payne, *Phys. Rev. Lett.* 1999, *82*, 3296–3299.
10. B. M. Wood, M. Dzamba, X. Fu, M. Gao, M. Shuaibi, L. Barroso-Luque, K. Abdelmaqsoud, V. Gharakhanyan, J. R. Kitchin, D. S. Levine, K. Michel, A. Sriram, T. Cohen, A. Das, A. Rizvi, S. J. Sahoo, Z. W. Ulissi, C. L. Zitnick, *arXiv* 2025, arXiv:2506.23971.
11. F. Birch, *Phys. Rev.* 1947, *71*, 809–824.
12. A. H. Larsen, J. J. Mortensen, J. Blomqvist, I. E. Castelli, R. Christensen, M. Dułak, J. Friis, M. N. Groves, B. Hammer, C. Hargus, E. D. Hermes, P. C. Jennings, P. B. Jensen, J. Kermode, J. R. Kitchin, E. L. Kolsbjerg, J. Kubal, K. Kaasbjerg, S. Lysgaard, J. B. Maronsson, T. Maxson, T. Olsen, L. Pastewka, A. Peterson, C. Rostgaard, J. Schiøtz, O. Schütt, M. Strange, K. S. Thygesen, T. Vegge, L. Vilhelmsen, M. Walter, Z. Zeng, K. W. Jacobsen, *J. Phys.: Condens. Matter* 2017, *29*, 273002.
13. R. P. Rao, S. Adams, *Phys. Status Solidi A* 2011, *208*, 1804–1807.
14. H. Chen, S. Adams, *IUCrJ* 2017, *4*, 614–625.
15. M. Kawamura, Y. Gohda, S. Tsuneyuki, *Phys. Rev. B* 2014, *89*, 094515.
16. A. D. Becke, K. E. Edgecombe, *J. Chem. Phys.* 1990, *92*, 5397–5403.
17. R. Dronskowski, P. E. Blöchl, *J. Phys. Chem.* 1993, *97*, 8617–8624.
18. S. Maintz, V. L. Deringer, A. L. Tchougréeff, R. Dronskowski, *J. Comput. Chem.* 2016, *37*, 1030–1035.
19. R. Nelson, C. Ertural, J. George, V. L. Deringer, G. Hautier, R. Dronskowski, *J. Comput. Chem.* 2020, *41*, 1931–1940.

확인 방법: api.crossref.org 는 이 세션 프록시가 막았다 (403 · 우회하지 않음) → 웹 검색 목록 (출판사·기관 저장소·PMC·arXiv) 으로 저자·권·쪽을 대조했다. QE 2017 (50 명 · Paderborn·Princeton 기록 순서) · QE 2020 (15 명 · DOI 10.1063/5.0005082) · UMA (18 명 · arXiv 순서 — NeurIPS 판은 뒤 다섯 명 순서가 달라 arXiv 판으로 인용) 확인. 13 은 litdb `rao2011_argyrodite_se_studies_bvse` · 4 · 8 · 11 은 표준 인용이라 재확인 안 함 · GBRV (6) 는 Rutgers GBRV 페이지·arXiv 1305.5973 으로 대조 (DOI 10.1016/j.commatsci.2013.08.053).

## 빈칸 · 확인할 것

1. ✅ **B·O 유사퍼텐셜 확인됨 (2026-10-21)** — 사용자가 외장 SSD 백업 A 에서 직접 확인:
   `D:\v100\kisti_backup_2026-07-14\kgy_b2o3_eos_2026-07-14\b2o3_eos\b2o3_nscf_dos.in` 22–27 행 (`b2o3_scf_atomic.in` 도 같음) —
   Li `li_pbe_v1.4.uspp.F.UPF` · P `P.pbe-n-rrkjus_psl.1.0.0.UPF` · B `b_pbe_v1.4.uspp.F.UPF` · S `s_pbe_v1.4.uspp.F.UPF` · O `O.pbe-n-kjpaw_psl.0.1.UPF` · Cl `cl_pbe_v1.4.uspp.F.UPF`
   ⇒ Li·B·S·Cl = GBRV v1.4 USPP · P = PSlibrary 1.0.0 USPP · O = PSlibrary 0.1 PAW — 2 번 문장 (SSSP efficiency · O 만 PAW) 그대로 맞다.
   ⚠ 같은 폴더 `nscf_lobster.out` 도 이 USPP 세트를 읽었다 — LOBSTER 가 USPP 를 거부해서 버린 첫 시도이고, 보고한 ICOHP 는 all-PAW 로 다시 돌린 계산이다
   (`db/properties/b2o3_icohp.json` `method` · `tools/electronic/icohp_paw_kisti.sh`). 그 출력 (`b2o3_paw_scf.out` · `nscf_paw.out`) 의 PseudoPot 줄을 보면 마지막 문단도 같은 방식으로 확정된다.
2. ✅ UMA 저자 18 명 — arXiv 순서로 다 적음 (10-21).
3. 참고문헌 번호를 원고 목록에 합치기 (Word 파일은 템플릿대로 2.5 절 · 위첨자 인용) · 붙여 넣은 뒤 첨자·italic·minus 다시 보기 (BML [3]).
4. ✅ **3 번 문장 k 격자 · smearing (10-21)** — 세 계 다 실행 입력으로 확인 (위 근거 표 · LPSC1.6 6×6×3 · O-LPSC1.6 2×2×1 · BO-LPSC1.6 3×3×1) → 본문에 계별 격자를 넣었다 (권고 ② · 사용자 *'권고대로 해줘'*). ✅ `smearing='mv'` 다섯 입력 모두 (10-21 WSL·gabia: `modelC_v2_eos_v100.in` · `modelC_v3/V0_relax.in` · `lpsocl_eos/v100/relax.in` · gabia `lpsocl_dft/01_relax_v0.in` · `b2o3_eos/relax_v0.in`) · 2 번 문장도 세 계 다 맞다 (GBRV v1.4 USPP · P psl 1.0.0 · O psl 0.1 PAW · 60/480 — O-LPSC1.6 은 밑줄 이름 사본 `cl_pbe_v1_4_uspp_F.UPF` 등 · 파일 내용 대조는 안 함). ⚠ ELF 예외: O-LPSC1.6 ELF 러너 (`tools/electronic/run_lpsocl_elf_gabia.sh`) 머리말 = *NC ONCV · 80/320 Ry · fixed · k444 · conv 1e-10* (comp1/modelc 전자구조 계열) — ELF 문장에서 따로 적는다. BO-LPSC1.6 은 백업 A 실행 입력으로 ✅: 구조 이완 (EOS 5 점 · V₀) `degauss=0.02` · 전자구조 SCF `0.01` · k 3×3×1 · DOS/gap nscf 7×7×1.
   ⚠ 10-20 초안의 *'smearing of 0.01 Ry'* 는 생성기 (`tools/doping/b2o3_dft_eos.py`) 값을 실행값으로 읽은 내 실수였다 → 본문을 *0.01–0.02 Ry* 로 고쳤다 (사용자 10-21 *'권고대로 해줘'*).
   **남은 것: LPSC1.6 · O-LPSC1.6 의 K_POINTS · degauss** — repo 기록에 값이 없다. 실행 입력 위치: LPSC1.6 V₀ = `/home/ubuntu/work/runs/modelC_v3/V0_relax.in` (`db/structures/modelc_V0_k663.xyz` provenance) · EOS = `…/runs/lpscl16_verify_20260520/modelC_v2_eos_v096–v106.in` (`db/compositions/modelc_v3.json`) · O-LPSC1.6 = KISTI `/scratch/x3430a02/kgy/lpsocl_eos` (`lpsocl_eos_dft_result.json` `data_source` → 백업 A `kgy_lpsocl_eos_2026-07-14\lpsocl_eos\`). 사용자 10-21: gabia · kgy 에도 있을 수 있다. 값이 오면 3 번 문장에 계별 k 격자를 넣는다 (권고 ②).
5. ⏳ **4 번 문장 힘 문턱 (10-21 입력)** — BO-LPSC1.6 V₀ 이완 `relax_v0.in` 은 `forc_conv_thr=1.0d-3` 인데 본문은 BO 를 10⁻⁴ 로 적었다 (생성기 `b2o3_dft_eos.py` 의 1.0d-4 를 실행값으로 읽은 내 실수 · smearing 과 같은 원인). LPSC1.6 1e-4 (EOS·V₀) · O-LPSC1.6 1e-3 (EOS·V₀) ✓. SCF `conv_thr`: EOS 셋 다 1e-8 · LPSC1.6 V₀ 1e-10 · O·BO V₀ 1e-8 → *'10⁻⁸ Ry or tighter'* 로 덮인다. `etot_conv_thr` 1e-6 (O-LPSC1.6 V₀ 만 1e-5). BO EOS 5 점의 `forc_conv_thr` 는 아직 안 봤다.
6. ⚠ **ELF 계산 설정이 계마다 다르다 (10-21 입력)** — LPSC1.6 `modelC_v3/elf_scf.in`: ONCV 1.0 NC · 80/320 Ry · mv 0.01 · 6×6×3 · conv 1e-10 / O-LPSC1.6 gabia `lpsocl_elf/scf.in`: ONCV 1.2 (O 1.0) NC · 80/320 · fixed · 4×4×4 · conv 1e-10 / BO-LPSC1.6 `b2o3_eos/pp_elf.in` = prefix `'b2o3'` · outdir `'./tmp'` (`b2o3_elf_bonds.csv` 머리 *'KISTI, tmp/b2o3.save'*) → 2 번 문장의 USPP 세트 SCF 로 보인다 (어느 입력인지 확인 중). 원고 ELF 문단이 LPSC1.6 과 BO-LPSC1.6 의 ELF 를 비교한다 (Fig. 2f · Table S2) → ELF 문장에서 계별로 적고 NC 대 USPP 차이를 짚는다 (판단 없이 위치만).
7. ⚠ **모델 이름을 앞당겨 쓰는 문제 (사용자 10-21 질문)** — 원고 v1 은 3 절의 전도도 문단에서 *'hereafter denoted as BO-LPSC1.6'* 로 이름을 정하고 O-LPSC1.6 도 거기서 처음 나온다 (2.5 절보다 뒤 · 2.1–2.4 는 못 봄). 2.5 안에서도 모델 (원자 수·셀) 은 2 번 문단에서 정의된다 → 1 번 문단은 계와 무관한 설정만 두고 계별 k 격자 · BO smearing 0.02 · 힘 문턱을 3 번 문단 (EOS·이완) 으로 옮기는 안을 권고했다 (사용자 결정 대기).

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
| QE PBE · 60/480 Ry · conv_thr 1e-8 · forc 1e-4 | b2o3 EOS 입력 생성기 | `tools/doping/b2o3_dft_eos.py` (`ecutwfc=60` · `forc_conv_thr=1.0d-4`) · `db/properties/b2o3_dos_gap.json` `method` *"USPP 60/480 Ry"* |
| k 격자 · smearing (LPSC1.6) | 6×6×3 · `degauss=0.01` | **실행 입력** — 백업 B `D:\v100, kisti 백업\runs\lpscl16_verify_20260520\modelC_v2_eos_v096–v106.in` (EOS 11 점) · `runs\modelC_v3\V0_relax.in` (V₀) · `elf_scf.in` 도 6×6×3 · 0.01 (사용자 10-21 PowerShell·WSL · 구조 이름 `modelc_V0_k663` 의 k663 = 이 격자) |
| k 격자 · smearing (O-LPSC1.6) | 2×2×1 · `degauss=0.01` | **실행 입력** — 백업 A `kgy_lpsocl_eos_2026-07-14\lpsocl_eos\v094–v106\relax.in` (EOS 7 점) · V₀ 이완 = gabia `/data/work/runs/lpsocl_dft/01_relax_v0.in` (`tools/elastic/run_lpsocl_suite_gabia.sh` 머리말 *'ecut 60/480, mv 0.01, k 2 2 1'* — 입력 자체는 아직 안 읽음) |
| MV smearing 0.01–0.02 Ry · k 격자 (BO-LPSC1.6) | 구조 이완 0.02 · 전자구조 SCF 0.01 · k 3×3×1 (SCF·이완) · 7×7×1 (DOS·gap nscf) | **실행 입력** — 백업 A `kgy_b2o3_eos_2026-07-14\b2o3_eos\` (사용자 10-21 PowerShell): `eos_v0.96–1.06.in` · `relax_v0.in` `degauss=0.02` · `b2o3_scf.in` · `b2o3_paw_scf.in` · `nscf_paw.in` `degauss=0.01` · `b2o3_nscf_dos.in` `tetrahedra_opt` · `b2o3_nscf_gap.in` `fixed` · K_POINTS 3 3 1 / 7 7 1. ⚠ 생성기 `b2o3_dft_eos.py` 의 `degauss=0.01` 은 실행 입력과 다르다 (10-20 초안이 이 값을 썼다) |
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
