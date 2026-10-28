---
title: NdO-LPSCl₁.₆ 원고 4.5 DFT calculations — 기록대로 · B₂O₃ 와 같은 꼴 (본문판 + SI 판)
date: 2026-10-28
updated: 2026-10-28
tags: [ndo, cei, manuscript, methods, neb, interface, band-gap]
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# NdO-LPSCl₁.₆ 원고 — 4.5. DFT calculations 초안 (2026-10-28)

**트랙**: CEI — 1저자는 **실험 쪽 박재현** 이고 사용자는 공저자 (계산 담당) 다 (CLAUDE.md §소통). 사용자 10-28
*'그냥 내 부분 method로 작성해줘라 · 저번 b2o3로 썼던 버전이랑 같은 형식으로'* → B₂O₃ 원고 Methods
(`kb/papers/b2o3_bo_lpsc16_methods_2026_10_20.md`) 와 같은 꼴: **우리 기록에 있는 실제 설정**으로 쓰고 옳고 그름은 따지지 않는다 ·
원고 숫자가 어디서 왔는지는 **위치만** 적는다 (원고 문장은 고치지 않는다 · 같이 읽기 규칙은 CLAUDE.md CEI 줄).

- 다루는 그림 넷 (원고 결과 순서 = Methods 문단 순서 · BML 가이드): **Fig. 3f,g** Li₂S · Li₃Nd CI-NEB → **Fig. 3h** SEI 성분 띠틈 (우리 QE · 8 월 체인 — 사용자 10-28 결정) →
  **Fig. 5e,f** NCM 계면 반응에너지 대 전위 (pymatgen · MP) → **Fig. SX** Nd 함유 CEI 성분 띠틈 (우리 QE · 9 월 체인 · NdP₅O₁₄ 포함).
- **Methods 에 결과 값은 안 쓴다** (사용자 10-28 *'method니까 값은 안써도 될듯'*) — 설정만 남기고 값 (띠틈 · 장벽 · 에너지) 은 그림 · 결과 몫이다.
  SI 에서 뺀 값 넷: Li₃Nd E_hull 0.197 eV/atom · Li₃Nd 끝점 이완 ≈ 1.4 eV/셀 (단서는 말로 남김) · μ_Li⁰ −1.909 eV/atom · LiCl hull 위 0.004 eV/atom (MP 띠틈 문단과 같이 빠짐).
  아래 두 표의 값은 기록이라 그대로 둔다.
- 원고 양식 = **Elsevier** (원고의 `[ref]` 자리 · 참고문헌 [1] 꼴): 본문 인용은 문장부호 **앞** `[n]` · 참고문헌은 `저자, 제목, 저널 권 (연도) 쪽. DOI` ·
  절 제목 이탤릭 *4.5. DFT calculations* · 'LPSCl₁.₆' 의 '1.6' 은 원고처럼 아래첨자. B₂O₃ (Wiley · 위첨자 [n] · 제목 없음) 와 이 점만 다르다.
- **Word 두 파일** — B₂O₃ 와 같은 방식 (사용자 method 템플릿 패키지 그대로 · 본문만 바꿈 · Times New Roman 12 pt · 2 줄 간격 · 첫 줄 들여쓰기 ·
  첨자는 Word 첨자 · SI 식 3 개는 Word 수식 개체): 본문판 `kb/papers/ndo_lpscl16_methods_main_2026_10_28.docx` · SI 판 `kb/papers/ndo_lpscl16_methods_SI_2026_10_28.docx`.
- 빌더 `tools/manuscripts/build_ndo_methods_docx.py` 가 **한 원본에서** Word 두 파일과 아래 md 본문 (`--md`) 을 같이 뽑는다 · `--check` = 인용 순서 · 누락 ·
  `--selftest` (일부러 깬 두 경우 — 첫 인용 순서 뒤바꿈 · 인용 빠짐 — 둘 다 잡음). 템플릿은 저장소의 B₂O₃ 본문판 docx (같은 패키지 · 본문만 갈아 끼운다).
- 참고문헌은 이 절 안에서 처음 인용 순서로 [1]–[14] · 본문판과 SI 판이 **같은 목록**이다 (원고 목록에 합칠 때 번호를 다시 매긴다).

---

## 본문 압축판 — 4.5 절 (약 440 단어 · Word `kb/papers/ndo_lpscl16_methods_main_2026_10_28.docx`)

> 계별 세부 (k 격자 · smearing 폭 · 문턱 · 끝점 이완 · PP 파일 이름 · MP ID · 식 셋 · 셀 크기 한계) 는 SI 판으로 보냈다. 같은 사실만 쓴다.

***4.5. DFT calculations***

DFT calculations were performed with Quantum ESPRESSO [1–3] using the Perdew–Burke–Ernzerhof (PBE) generalized gradient approximation (GGA) [4], with kinetic energy cutoffs of 60 and 480 Ry for the wavefunctions and charge density, respectively. The Brillouin zone was sampled with Γ-centered Monkhorst–Pack *k*-point grids [5]; the grids, smearing parameters, and convergence thresholds of each calculation are given in the Supplementary Material.

Li migration barriers (Fig. 3f,g) were calculated with the climbing-image nudged elastic band method [6] using seven images, for a Li vacancy hopping between nearest-neighbor Li sites. Li₂S was modeled with a 3 × 3 × 3 supercell of antifluorite Li₂S (mp-1153 in the Materials Project database [7]) containing a negatively charged Li vacancy compensated by a uniform background charge, and the Li–Nd alloy with a 2 × 2 × 2 supercell of an ordered BiF₃-type Li₃Nd model (mp-976264) containing a neutral Li vacancy. Ultrasoft pseudopotentials from the GBRV library were used for Li and S [8], and a projector augmented-wave (PAW) dataset from PSlibrary with the Nd 4*f* electrons frozen in the core was used for Nd [9]. Gaussian smearing was applied to Li₂S and Marzari–Vanderbilt smearing [10] to the metallic Li₃Nd.

The band gaps of Li₂S, Li₃P, Li₂O, Li₃PO₄, and LiCl (Fig. 3h) were calculated for structures taken from the Materials Project database [7], with GBRV ultrasoft pseudopotentials for Li, S, and Cl [8] and PSlibrary datasets for P and O [9]. The lattice parameters and atomic positions were fully relaxed, and the band gaps were obtained from the Kohn–Sham eigenvalues at the valence band maximum and conduction band minimum of non-self-consistent calculations with fixed occupations on denser *k*-point grids.

Interfacial reaction energies between the SEs and NCM (LiNi₀.₈Co₀.₁Mn₀.₁O₂) were calculated as a function of voltage (Fig. 5e,f) following the approach of Richards et al. [11], as implemented in pymatgen [12], with the mixed GGA/GGA+*U* energies of the Materials Project database [7,13]. LPSCl₁.₆ (Li₅.₄PS₄.₄Cl₁.₆) and NdO-LPSCl₁.₆ (Li₅.₄₄Nd₀.₀₂P₀.₉₈S₄.₃₇O₀.₀₃Cl₁.₆) were represented by the convex-hull energies at their compositions. The interface was treated as open to Li at a chemical potential *μ*<sub>Li</sub>(*φ*) = *μ*<sub>Li</sub>⁰ − *eφ* [14], where *μ*<sub>Li</sub>⁰ is the chemical potential of Li metal, *e* is the elementary charge, and *φ* is the applied voltage vs. Li/Li⁺ (2.5–4.5 V). At each voltage, the reaction energy was taken as the most negative grand-potential reaction energy over all SE/NCM mixing ratios, normalized per atom excluding Li, and the corresponding reaction products were identified.

The band gaps of the Nd-containing CEI components (Fig. SX) were calculated with the same procedure, but with PAW datasets from PSlibrary for all elements [9], with the Nd 4*f* electrons frozen in the core.

## SI 전체판 — Computational details (약 890 단어 · Word `kb/papers/ndo_lpscl16_methods_SI_2026_10_28.docx`)

> 본문판과 같은 참고문헌 14 개 · 식 셋 (S1–S3) 은 Word 에서 수식 개체다 (아래 LaTeX 는 같은 식).

**Computational details** (Supplementary Material)

DFT calculations were performed with Quantum ESPRESSO [1–3] using the Perdew–Burke–Ernzerhof (PBE) generalized gradient approximation (GGA) [4]. In all calculations, kinetic energy cutoffs of 60 and 480 Ry were used for the wavefunctions and charge density, respectively, the Brillouin zone was sampled with Γ-centered Monkhorst–Pack *k*-point grids [5], and self-consistent field (SCF) calculations were converged to 10⁻⁸ Ry with a mixing factor of 0.3.

Li migration barriers were calculated with the climbing-image nudged elastic band (CI-NEB) method [6] for a Li vacancy hopping between nearest-neighbor 8*c* sites. Antifluorite Li₂S (*Fm*3̅*m*; mp-1153 in the Materials Project database [7]) and an ordered BiF₃-type Li₃Nd model (*Fm*3̅*m*; mp-976264, a hypothetical phase above the convex hull) were first relaxed with variable cell. Ultrasoft pseudopotentials from the GBRV library (v1.4) were used for Li and S [8], and the PAW dataset Nd.pbe-spdn-kjpaw_psl.1.0.0 from PSlibrary, in which the Nd 4*f* electrons are frozen in the core, was used for Nd [9]. Supercells of the primitive cells were then constructed, 3 × 3 × 3 for Li₂S (80 atoms after vacancy creation, shortest lattice translation 12.1 Å, hop distance 2.85 Å) and 2 × 2 × 2 for Li₃Nd (31 atoms, shortest lattice translation 10.4 Å, hop distance 3.67 Å), and both were sampled with a 3 × 3 × 3 *k*-point grid. Because Li₂S is an insulator, its vacancy was modeled in the negatively charged state (V<sub>Li</sub>⁻; one extra electron per supercell compensated by a uniform background charge, without a finite-size correction) with Gaussian smearing of 0.005 Ry, whereas the vacancy in metallic Li₃Nd was modeled as neutral with Marzari–Vanderbilt smearing [10] of 0.02 Ry.

The two vacancy endpoints were relaxed at fixed cell until all force components were below 10⁻³ Ry bohr⁻¹. The minimum-energy path was represented by seven images and optimized with the Broyden scheme, with the climbing image selected automatically, until the force component perpendicular to the path fell below 0.05 eV Å⁻¹. For Li₃Nd, both vacancy endpoints reconstructed substantially on relaxation from the ideal lattice, so the barrier refers to this locally reconstructed 2 × 2 × 2 model. A check with a 3 × 3 × 3 supercell (107 atoms) was attempted, but its vacancy endpoints also reconstructed substantially and the CI-NEB between them did not converge; the Li₃Nd barrier is therefore not converged with respect to cell size.

The band gaps of the interphase components in Fig. 3h were calculated for Li₂S (mp-1153, *Fm*3̅*m*), Li₃P (mp-736, *P*6₃/*mmc*), Li₂O (mp-1960, *Fm*3̅*m*), β-Li₃PO₄ (mp-13725, *Pmn*2₁), and rock-salt LiCl (mp-22905, *Fm*3̅*m*), whose structures were taken from the Materials Project database [7]. Ultrasoft GBRV pseudopotentials (v1.4) were used for Li, S, and Cl [8], and PSlibrary datasets were used for P (ultrasoft, P.pbe-n-rrkjus_psl.1.0.0) and O (PAW, O.pbe-n-kjpaw_psl.0.1) [9]. The structures were relaxed with respect to both lattice parameters and atomic positions with Marzari–Vanderbilt smearing [10] of 0.01 Ry and a *k*-point spacing of at most 0.30 Å⁻¹ (including the factor 2π). After an SCF calculation on the relaxed structure, a non-self-consistent calculation with fixed occupations was performed on a denser *k*-point grid (spacing of at most 0.15 Å⁻¹) with at least 35% more bands than occupied states, and the band gap was taken as the difference between the Kohn–Sham eigenvalues at the conduction band minimum and the valence band maximum.

Interfacial reaction energies between the SEs and NCM (LiNi₀.₈Co₀.₁Mn₀.₁O₂) were calculated following the approach of Richards et al. [11], with the GrandPotentialInterfacialReactivity class of pymatgen [12]. For each SE/NCM pair, the entries of the corresponding chemical system (Li–Ni–Co–Mn–P–S–O–Cl, with Nd added for NdO-LPSCl₁.₆) were retrieved from the Materials Project database [7] with mixed GGA/GGA+*U* energies [13] (queried with the mp_api client in September 2026). LPSCl₁.₆ (Li₅.₄PS₄.₄Cl₁.₆) and NdO-LPSCl₁.₆ (Li₅.₄₄Nd₀.₀₂P₀.₉₈S₄.₃₇O₀.₀₃Cl₁.₆), which are not in the database, were represented by the convex-hull energies at their compositions. The interface was treated as open to a Li reservoir whose chemical potential was set by the applied voltage *φ* (vs. Li/Li⁺) through Eq. (S1) [14], where *μ*<sub>Li</sub>⁰ is the energy per atom of Li metal (the lowest-energy elemental Li entry) and *e* is the elementary charge. With the grand potential of each phase defined by Eq. (S2), where *E* is its energy and *N*<sub>Li</sub> is its number of Li atoms, the reaction energy at each voltage was obtained from Eq. (S3), where *x* (0 ≤ *x* ≤ 1) is the fraction of SE in the SE/NCM mixture, *Φ*<sub>eq</sub>(*x*) is the grand potential of the equilibrium phases at the composition of the mixture, and *Φ*<sub>SE</sub> and *Φ*<sub>NCM</sub> are the grand potentials of the unreacted SE and NCM evaluated from their convex-hull energies; all grand potentials were normalized per atom excluding Li. The calculations were performed at *φ* = 2.5, 3.0, 3.5, 4.0, 4.3, and 4.5 V, and the reaction products were taken from the equilibrium phases at the minimizing *x*. At every voltage, the minimum for both SEs lies at an intermediate mixing fraction (0 < *x* < 1), that is, the reaction involves both the SE and NCM.

```latex
\mu_{\mathrm{Li}}(\varphi) = \mu_{\mathrm{Li}}^{0} - e\varphi \qquad (\mathrm{S}1)
```

```latex
\Phi = E - \mu_{\mathrm{Li}} N_{\mathrm{Li}} \qquad (\mathrm{S}2)
```

```latex
\Delta E_{\mathrm{rxn}}(\varphi) = \min_{x}\left[\Phi_{\mathrm{eq}}(x) - x\,\Phi_{\mathrm{SE}} - (1-x)\,\Phi_{\mathrm{NCM}}\right] \qquad (\mathrm{S}3)
```

The band gaps of the Nd-containing CEI components, including NdP₅O₁₄ (mp-560681, *Pmna*), were calculated with the same procedure, but with PAW datasets from PSlibrary for all elements [9] (Li.pbe-sl-kjpaw_psl.1.0.0, P.pbe-n-kjpaw_psl.1.0.0, S.pbe-nl-kjpaw_psl.1.0.0, Cl.pbe-nl-kjpaw_psl.1.0.0, O.pbe-n-kjpaw_psl.0.1, and Nd.pbe-spdn-kjpaw_psl.1.0.0). Because the Nd 4*f* electrons are frozen in the core of the Nd dataset, the calculations were non-spin-polarized and no Hubbard *U* correction was applied. After relaxation, the residual pressures were within ±1 kbar.

## 참고문헌 — 14 개 (Elsevier 꼴 · 본문판 = SI 판)

원고 (`ms.docx` · 사용자 10-27 업로드 · 저장소 밖) 의 [1] 꼴 그대로 (`저자, 제목, 저널 권 (연도) 쪽. https://doi.org/…`) · 저자는 전부 적었다 (원고 [1] 도 전부).
QE 는 공식 인용 안내대로 셋 (2020 = GPU 판 · gabia NEB 가 `qe-7.4.1-gpu` neb.x · B₂O₃ 와 같은 판단) · PP 는 쓴 라이브러리 원 논문 (GBRV · PSlibrary — SSSP 를 거치지 않았다).

[1] P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso, S. de Gironcoli, S. Fabris, G. Fratesi, R. Gebauer, U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri, L. Martin-Samos, N. Marzari, F. Mauri, R. Mazzarello, S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, G. Sclauzero, A. P. Seitsonen, A. Smogunov, P. Umari, R. M. Wentzcovitch, QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials, J. Phys.: Condens. Matter 21 (2009) 395502. https://doi.org/10.1088/0953-8984/21/39/395502.
[2] P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. Buongiorno Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, N. Colonna, I. Carnimeo, A. Dal Corso, S. de Gironcoli, P. Delugas, R. A. DiStasio Jr., A. Ferretti, A. Floris, G. Fratesi, G. Fugallo, R. Gebauer, U. Gerstmann, F. Giustino, T. Gorni, J. Jia, M. Kawamura, H.-Y. Ko, A. Kokalj, E. Küçükbenli, M. Lazzeri, M. Marsili, N. Marzari, F. Mauri, N. L. Nguyen, H.-V. Nguyen, A. Otero-de-la-Roza, L. Paulatto, S. Poncé, D. Rocca, R. Sabatini, B. Santra, M. Schlipf, A. P. Seitsonen, A. Smogunov, I. Timrov, T. Thonhauser, P. Umari, N. Vast, X. Wu, S. Baroni, Advanced capabilities for materials modelling with Quantum ESPRESSO, J. Phys.: Condens. Matter 29 (2017) 465901. https://doi.org/10.1088/1361-648X/aa8f79.
[3] P. Giannozzi, O. Baseggio, P. Bonfà, D. Brunato, R. Car, I. Carnimeo, C. Cavazzoni, S. de Gironcoli, P. Delugas, F. Ferrari Ruffino, A. Ferretti, N. Marzari, I. Timrov, A. Urru, S. Baroni, Quantum ESPRESSO toward the exascale, J. Chem. Phys. 152 (2020) 154105. https://doi.org/10.1063/5.0005082.
[4] J. P. Perdew, K. Burke, M. Ernzerhof, Generalized gradient approximation made simple, Phys. Rev. Lett. 77 (1996) 3865–3868. https://doi.org/10.1103/PhysRevLett.77.3865.
[5] H. J. Monkhorst, J. D. Pack, Special points for Brillouin-zone integrations, Phys. Rev. B 13 (1976) 5188–5192. https://doi.org/10.1103/PhysRevB.13.5188.
[6] G. Henkelman, B. P. Uberuaga, H. Jónsson, A climbing image nudged elastic band method for finding saddle points and minimum energy paths, J. Chem. Phys. 113 (2000) 9901–9904. https://doi.org/10.1063/1.1329672.
[7] A. Jain, S. P. Ong, G. Hautier, W. Chen, W. D. Richards, S. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder, K. A. Persson, Commentary: The Materials Project: A materials genome approach to accelerating materials innovation, APL Mater. 1 (2013) 011002. https://doi.org/10.1063/1.4812323.
[8] K. F. Garrity, J. W. Bennett, K. M. Rabe, D. Vanderbilt, Pseudopotentials for high-throughput DFT calculations, Comput. Mater. Sci. 81 (2014) 446–452. https://doi.org/10.1016/j.commatsci.2013.08.053.
[9] A. Dal Corso, Pseudopotentials periodic table: From H to Pu, Comput. Mater. Sci. 95 (2014) 337–350. https://doi.org/10.1016/j.commatsci.2014.07.043.
[10] N. Marzari, D. Vanderbilt, A. De Vita, M. C. Payne, Thermal contraction and disordering of the Al(110) surface, Phys. Rev. Lett. 82 (1999) 3296–3299. https://doi.org/10.1103/PhysRevLett.82.3296.
[11] W. D. Richards, L. J. Miara, Y. Wang, J. C. Kim, G. Ceder, Interface stability in solid-state batteries, Chem. Mater. 28 (2016) 266–273. https://doi.org/10.1021/acs.chemmater.5b04082.
[12] S. P. Ong, W. D. Richards, A. Jain, G. Hautier, M. Kocher, S. Cholia, D. Gunter, V. L. Chevrier, K. A. Persson, G. Ceder, Python Materials Genomics (pymatgen): A robust, open-source python library for materials analysis, Comput. Mater. Sci. 68 (2013) 314–319. https://doi.org/10.1016/j.commatsci.2012.10.028.
[13] A. Jain, G. Hautier, S. P. Ong, C. J. Moore, C. C. Fischer, K. A. Persson, G. Ceder, Formation enthalpies by mixing GGA and GGA+U calculations, Phys. Rev. B 84 (2011) 045115. https://doi.org/10.1103/PhysRevB.84.045115.
[14] Y. Zhu, X. He, Y. Mo, Origin of outstanding stability in the lithium solid electrolyte materials: Insights from thermodynamic analyses based on first-principles calculations, ACS Appl. Mater. Interfaces 7 (2015) 23685–23693. https://doi.org/10.1021/acsami.5b07517.

확인 방법: doi.org · crossref 는 이 세션 프록시가 막았다 (403 · 우회하지 않음). [1]–[5] · [8]–[10] 은 B₂O₃ 문서에서 대조한 저자·권·쪽 그대로 (DOI 는 표준 인용) ·
[6] Henkelman 2000 · [7] MP 2013 (11 명 · DOAJ 목록) · [11] Richards 2016 (MIT DSpace) · [12] pymatgen (MIT DSpace · LBL) · [13] Jain 2011 (LBL · APS 수락본) 은 웹 검색 목록으로 저자·권·쪽·DOI 대조 ·
[14] Zhu 2015 는 검색에 DOI 가 안 떴고 **litdb `zhu2015_esw_grand_potential_origin` 의 PDF 실물 풋터** (`10.1021/acsami.5b07517` · 옛 메모의 `5b01004` 는 오기) 로 확인했다.

## 빈칸 · 확인할 것

1. **Li₃Nd NEB 의 k 격자 (3 × 3 × 3) · Li PP** — repo 에 실행 입력이 없다 (gabia `/data/work/runs/sei_neb_v2_ccpath/li3nd/`). k 는 생성기 규칙
   (`tools/sei/build_neb_inputs.py` `kmesh` · `--kdens` 기본 0.04 · 2×2×2 면 높이 8.47 Å → ⌈2.95⌉ = 3) 으로 다시 셌고 Li PP 는 같은 pseudo 폴더 (`/data/work/pseudo` · GBRV li v1.4) 로 적었다.
   NEB 를 돌린 QE 판도 기록에 없다. 같은 김에 **09-19 Nd CEI 띠틈 입력의 스핀 · U** 도 본다 — SI 의 *'non-spin-polarized and no Hubbard U'* 는 원장 선언
   (`sei_electronic_class.json` *'`--nd_u 0 --no_nd_spin` 필수'*) 과 8 월 frozen-4f 런 (`sei_electronic.json` `spin_polarized` false) 이 근거이고 09-19 실행 입력은 안 봤다.
   확인 블록 (gabia · 읽기만 · 둘째 줄이 아무것도 안 찍으면 nspin 1 · U 없음):
   ```
   D=/data/work/runs/sei_neb_v2_ccpath/li3nd; ls $D | head -20; for f in $D/*.in; do echo "== $f"; grep -a -A1 K_POINTS "$f"; grep -a -A3 ATOMIC_SPECIES "$f"; done 2>/dev/null | head -60; grep -a -h -m1 "Program NEB\|Program PWSCF" $D/*.out 2>/dev/null | sort -u
   grep -a -h -i "nspin\|hubbard\|tot_magnetization" /data/work/runs/cei_gap/*/0*.in 2>/dev/null | sort | uniq -c; ls -d /data/work/runs/cei_gap/*/ | wc -l
   ```
2. ✅ ~~Fig. 3h MP 띠틈의 계산 종류~~ — **해당 없음** (10-28 · Fig. 3h 를 우리 QE 값으로 바꿔서 MP 띠틈의 출처는 안 따진다 · 확인 블록은 이력 `cc966284` 에 있다).
3. ✅ **Fig. 3h 숫자 ↔ Methods 문장** — 사용자 10-28 *'우리 qe 값으로 하는게 맞는듯'* → 그림을 우리 QE 값으로 바꾼다 (Origin CSV `db/properties/ndo_fig3h_sei_gaps_qe_origin.csv`) ·
   Methods 3 문단 = 8 월 SEI 체인. 새 그림 값을 1저자에게 넘기는 건 사용자. 역할 분류 (넓은 띠틈 · 중간 · 전도성) 는 MP 판과 같다.
4. **MP 데이터베이스 판 · pymatgen · mp_api 판** — 기록에 없다. SI 에는 '2026 년 9 월 조회' 만 적었다 (띠틈 09-13 · 반응에너지 09-28). MP2020 보정 (mp_api 기본) 을 적을지는 판 확인 뒤.
5. **Fig. 5e,f 의 그림 구성 (원고 빈칸)** — Methods 는 NCM (NMC811) × LPSCl₁.₆ · NdO-LPSCl₁.₆ 로 썼다. 다른 양극 (LiCoO₂ · LiNiO₂ · LiMnO₂) 이나 다른 조성 (LPSCl · O only · Nd only …) 을 그리면
   SE · 양극 문장을 넓힌다 (값은 `db/properties/cei_figs/cei_reaction_energy_by_cathode_x002.csv` 에 다 있다 · LiMnO₂ 4.5 V 두 점은 끝점 = SE 자체 분해).
6. **Fig. SX 의 Nd CEI 성분 (원고 빈칸)** — NdP₅O₁₄ 는 09-19 체인으로 계산했다 (사용자 10-28 *'ndp5o14도 계산하지 않았나'* → 맞다 · *Pmna* mp-560681 · SI 문단에 이름을 넣었다).
   값을 원고에 넣으면 단서 문장 (`HZ-cei-gap-ndp5o14-unreproduced`) 이 캡션이나 결과 쪽에 같이 가야 한다 (Methods 에는 값이 없다). 다른 후보 값 위치는 아래 출처 표.
7. ✅ **SI 의 셀 크기 문장** — 사용자 10-28 *'우리 안한거는 빼도 되는거 아니야?'* → '안 한 것' 두 문장 (3×3×3 시도가 안 된 경위 · Li₂S 셀 수렴 미시험) 을 뺐다.
   Li₃Nd 의 *'재구성된 2×2×2 모델 · 셀 크기에 수렴 안 됨'* 한 문장은 남겼다 — 안 한 일이 아니라 장벽 숫자가 어떤 모델 값인지이고, `D-2026-10-26-li3nd-neb-si-conditional`
   (0.229 는 SI 에 단서와 같이) 의 조건이다. 이 줄까지 빼려면 그 결정을 바꿔야 한다 (사용자 · 비준된 SEI 트랙 결정).
   ⏩ 사용자 10-28 *'li3nd 한해서 3*3*3은 크게 이완돼서 못했다 부분 추가할까?'* → Li₃Nd 만 3×3×3 시도 경위를 다시 넣었다 (해 봤는데 안 된 일 · 결정 SI 문장과 같은 뜻):
   *'A check with a 3 × 3 × 3 supercell (107 atoms) was attempted, but its vacancy endpoints also reconstructed substantially and the CI-NEB between them did not converge'*
   (`li3nd_p333_control_runlog_2026_10_11.json` `결정_실험_NEB_끝점_2026_10_26` — 3×3×3 끝점 이완 수렴 · 2×2×2 보다 더 큰 재배열 · 그 사이 NEB 30 스텝 미수렴 `neb_cc333_force_history_2026_08_27.json`).
8. 참고문헌 번호를 원고 목록에 합치기 · 붙인 뒤 첨자 · italic · minus 다시 보기 (BML) · *'Fig. SX'* · *'Supplementary Material'* 은 원고 자리표시 그대로 뒀다.
9. 10-27 CEI 생성물 11 종 띠틈 (kgy 진행 중 · 1저자 요청) 을 SI 에 넣게 되면 전이금속 상 문단 (스핀 · U · GBRV Co/Ni/Mn · Mn 상 90/1080 Ry) 을 더한다 —
   카드 `db/properties/cei_product_gap_card_2026_10_27.json` + 개정 1.
10. **PP 세트가 그림마다 다르다** — Fig. 3h (8 월 SEI · Li · S · Cl GBRV + P · O psl) 와 Fig. SX (9 월 CEI · 전부 PAW psl) — SI 에 각각 적었다. 한 세트로 맞추려면
    10-27 kgy 체인 (LiCl · Li₃PO₄ 만 PAW 로 다시 잰다) 에 Li₂S · Li₂O · Li₃P 를 더해야 한다 (사용자 결정 · 지금은 안 한다).

## 원고 숫자의 출처 — Methods 와 맞추려면 볼 곳 (판단 없이 위치만)

| 원고 | 숫자 | 우리 기록에서 나온 곳 | Methods 문장과의 관계 |
|---|---|---|---|
| 결과 ms 32 · Fig. 3h | Li₂S 3.90 · Li₃P 0.70 · Li₂O 5.24 · Li₃PO₄ 5.73 · LiCl 6.65 eV | `db/properties/sei_products.json` `sei_product_band_gaps_MP_eV` 의 `gap_MP_previous` (MP 요약 띠틈 · 06-24 조회 · 정렬 버그로 최소 E_hull 이 **아닌** 다형이 실린 판) · `HZ-sei-gaps-pre-20260913-nonground-polymorph` (CONDITIONAL) · 그림 대조 (10-28): 원고 막대 다섯 = 6 월 그림 `docs/figures/nd_sei/sei_product_gaps_O.png` (x 축 *'band gap (eV, Materials Project)'* · `tools/figures/plot_nd_sei_gaps.py` 하드코딩) 의 같은 다섯 값 · 우리 QE DOS 체인 (8 월 · `db/properties/sei_dos/`) 의 값이 **아니다** (DOS 문턱 판독이었다면 고유값 갭보다 작게 나와 3.90 · 5.24 처럼 우리 값보다 클 수 없다) | ✅ 사용자 10-28 *'우리 qe 값으로'* → 그림을 우리 QE fixed-occupation 값으로 바꾼다 (GBRV 세트 · `sei_electronic.json`): Li₂S 3.44 · Li₃P 0.71 · Li₂O 4.99 · Li₃PO₄ 5.91 (β mp-13725) · LiCl 6.26 (암염 mp-22905) — Origin CSV `db/properties/ndo_fig3h_sei_gaps_qe_origin.csv` · Methods 3 문단 = 이 체인 (그 전 판의 MP 문장과 정정본 3.39 · 0.70 · 4.90 · 5.82 · 6.65 대조는 이력 `cc966284`) |
| 결과 ms 32 · Fig. 3g | Li₂S 0.305 eV | `db/properties/sei_neb.json` `v2/li2s` (Ea 0.305025 · 3×3×3 · V_Li⁻ · jellium) · `HZ-sei-neb-retracted` (BLOCKED) | Methods 2 문단 · SI 의 Li₂S 설정 = 이 런 (`db/inputs/li2s_neb_cellconv_2026_10_09/v2_li2s_meta_gabia.json`) |
| 결과 ms 32 · Fig. 3g | Li₃Nd 0.229 eV | `sei_neb.json` `v2_ccpath/li3nd` (0.228981 · 2×2×2 · 중성 공공) · `HZ-li3nd-neb-si-conditional` (CONDITIONAL · SI + 단서 문장) · `D-2026-10-26-li3nd-neb-si-conditional` | Methods 2 문단 · SI 의 Li₃Nd 설정 = 이 런 · 원고의 비교 문장은 사용자 10-27 *'원고 그대로'* |
| 결과 ms 32 | *'Representative bulk structures of Li2S and Li–Nd alloy'* | Li₂S mp-1153 (Fm-3m · vc-relax · `geometry_source` `/data/work/runs/sei_dft/li2s_mp-1153/01_vcrelax.out`) · Li₃Nd mp-976264 (BiF₃ 꼴 · MP 이론 구조 · E_hull 0.197 eV/atom · `db/structures/sei_li3nd_mp-976264.vasp`) | Methods 2 문단 · SI 2 문단 |
| 결과 ms 42 · Fig. 5e,f | 반응에너지 (빈칸) | `db/properties/cei_figs/cei_reaction_energy_by_cathode_x002.csv` — NMC811 행 · 열 `modelc` = LPSCl₁.₆ · `nd_p_002_asused` = NdO-LPSCl₁.₆ (원고 x = 0.02 조성 그대로) · 2.5–4.5 V 여섯 점 · 원장 `db/properties/cei_interface_V_x002_2026_09_28.json` · 읽는 법 = CEI 화면 (`db/properties/cei_figs/index.html`) Fig. 8 · S1 (세로축 절대값은 다른 논문 값 옆에 두지 않음 · x = 0.02 에서 LPSCl₁.₆ 계열은 0.01–0.04 eV/atom 안에 붙어 양극마다 순서가 바뀜) | Methods 4 문단 · SI 4 문단 = 이 계산 |
| 결과 ms 42 | *'formation of an Nd-containing CEI is thermodynamically favorable in the high-voltage region'* | 같은 원장 NMC811 × `nd_p_002_asused` 최소 반응식의 Nd 생성물: NdPO₄ (2.5 · 3.0 V) → LiNd(PO₃)₄ (3.5 V) → Nd(PO₃)₃ (4.0 V) → NdP₅O₁₄ (4.3 · 4.5 V) | Methods 4 문단 끝 ('reaction products were identified') |
| 결과 ms 42 · Fig. SX | Nd CEI 성분 · 띠틈 (빈칸) | `db/properties/cei_gap_results_2026_09_19.json` `rows` (PBE · fixed-occ nscf · citable true): NdPO₄ 5.799 · LiNd(PO₃)₄ 5.993 · Nd(PO₃)₃ 5.497 · NdP₅O₁₄ 5.393 (`HZ-cei-gap-ndp5o14-unreproduced` CONDITIONAL) · Nd₂(SO₄)₃ 5.548 · NdCl₃ 4.337 · Nd₃PO₇ 4.352 · Nd₂O₃ 3.827 · NdPS₄ 2.264 · 화면 그림 `db/properties/cei_figs/cei_gap_briefing_2026_09_28.png` (+ Origin CSV) | Methods 5 문단 · SI 5 문단 = 이 체인 (NdP₅O₁₄ 포함 — 사용자 10-28 확인) |

## 문장별 근거 (기록 위치)

| 문장 | 값 | 근거 |
|---|---|---|
| QE PBE · 60/480 Ry · SCF 10⁻⁸ Ry · 섞음 0.3 | 모든 우리 계산 | `tools/sei/build_neb_inputs.py` (`ECUTWFC`/`ECUTRHO` · `conv_thr = 1.0d-8` · `mixing_beta = 0.3`) · `tools/sei/build_dft_inputs.py` 37 · 780–783 행 · `db/properties/sei_neb.json` `method` |
| Γ 중심 Monkhorst–Pack | `K_POINTS automatic … 0 0 0` | `build_dft_inputs.py` 801 행 · `build_neb_inputs.py` 723 · 818 · 913 행 |
| QE 2020 (GPU 판) 인용 | gabia NEB = `qe-7.4.1-gpu` neb.x | CLAUDE.md §계산 자원 (gabia GPU 줄) — 런별 판은 기록에 없음 (확인할 것 1) |
| CI-NEB · 7 이미지 · CI 자동 · Broyden · 경로 문턱 0.05 eV/Å · 끝점 고정셀 이완 10⁻³ Ry/bohr | | `sei_neb.json` `results` (`num_of_images` 7 · `CI_scheme` auto) · `build_neb_inputs.py` 708 행 (`forc_conv_thr`) · 877 · 891 행 (`opt_scheme='broyden'` · `path_thr`) · 1585–1595 행 argparse 기본값 (images 7 · path_thr 0.05 · `--ci_scheme` 기본은 no-CI 라 v2 는 auto 를 줘서 돌렸다 — 기록 `CI_scheme` auto) |
| Li₂S 3×3×3 · 80 원자 · λ₁ 12.1 Å · 홉 2.85 Å · V_Li⁻ (tot_charge −1) · jellium · gaussian 0.005 Ry · k 3×3×3 · 끝점 이완 · vc-relax 구조 | | `db/inputs/li2s_neb_cellconv_2026_10_09/v2_li2s_meta_gabia.json` · `sei_neb.json` `v2/li2s` (`cell_size_gate_metric` · `neighbor_shells`) |
| Li·S GBRV v1.4 USPP | `li_pbe_v1.4.uspp.F.UPF` · `s_pbe_v1.4.uspp.F.UPF` | `db/inputs/li2s_neb_cellconv_2026_10_09/pseudo/` |
| 보정 없음 (하전 공공) | | `sei_neb.json` `v2/li2s` `why_not_absolute` ② (jellium 근사 · 장벽은 neb.x 출력 그대로 — `tools/sei/collect_neb.py`) |
| Li₃Nd 2×2×2 · 31 원자 · λ₁ 10.37 Å · 홉 3.67 Å (c→c) · 중성 · mv 0.02 Ry | | `sei_neb.json` `v2_ccpath/li3nd` · `build_neb_inputs.py` 637–649 행 (금속 분기) |
| Li₃Nd k 3×3×3 | 생성기 규칙으로 다시 셈 | `build_neb_inputs.kmesh` (`--kdens` 0.04) × `db/structures/sei_li3nd_mp-976264.vasp` 2×2×2 (이 세션 계산 · 실행 입력 미확인 — 확인할 것 1) |
| Nd frozen-4f PAW (z 11) | `Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF` | `build_neb_inputs.py` `PP_PIN` (sha256 18a3835e…35101) · `build_dft_inputs.py` 69 행 · `db/properties/sei_electronic.json` `pseudo_Nd` |
| Li₃Nd = 가상 BiF₃ 꼴 (hull 위) · 끝점이 이상 격자에서 크게 재배열 · 3×3×3 NEB 미수렴 · 3×3×3 셀 재배열 | E_hull 0.197 eV/atom · 끝점 ≈ 1.4 eV/셀 (값은 SI 에 안 씀) | `D-2026-10-26-li3nd-neb-si-conditional` (SI 문장) · `db/properties/li3nd_p333_control_runlog_2026_10_11.json` `결정_실험_NEB_끝점_2026_10_26` · `kb/questions/li3nd_pristine_reconstruction_2026_09_02.md` |
| Li₂S 셀 수렴 미시험 (10-28 SI 에서 뺌 — 사용자 · 기록만) | `cell_convergence_status: untested` | `sei_neb.json` `v2/li2s` |
| Fig. 3h = 우리 QE · 8 월 SEI 체인 (MP 구조 → vc-relax → scf → fixed-occ nscf) · β-Li₃PO₄ mp-13725 · 암염 LiCl mp-22905 | Li₂S 3.4379 · Li₃P 0.7092 · Li₂O 4.9860 · Li₃PO₄ 5.9121 · LiCl 6.2603 | `db/properties/sei_electronic.json` `results` (`method` *'fixed-occupation nscf eigenvalues (NOT DOS threshold)'* · `collected` 2026-08-07 · `source_dir` gabia `/data/work/runs/sei_dft`) · 구조 `db/properties/sei_structures_provenance.json` (MP · 2026-08-06) |
| 8 월 체인 = 9 월과 같은 도구 규칙 (k 간격 · 밴드 수) | 밴드 수 5/5 규칙값 (16 · 16 · 26 · 59 · 35) · LiCl nk 35 = 9×9×9 Oh 기약 개수 | `sei_electronic.json` `nbnd` · `nk` 를 `build_dft_inputs.py` 규칙 (0.15 Å⁻¹ · 1.35 배 + 8) 과 대조 (10-28 이 세션) |
| 8 월 SEI PP = Li · S · Cl GBRV v1.4 USPP · P psl rrkjus · O psl 0.1 PAW | | `cei_product_gap_card_2026_10_27.json` `12_개정_1_2026_10_27_결과_전` `A1_PP_세트` 끝 (*'08 SEI 세트'*) · NEB 와 같은 pseudo 폴더 `/data/work/pseudo` |
| 반응에너지 = Richards 법 · `GrandPotentialInterfacialReactivity` · `use_hull_energy=True` · `include_no_mixing_energy=True` · MP `GGA_GGA+U` | | `cei_interface_V_x002_2026_09_28.json` `method` · `tools/oxidation/interface_reactivity_v2.py` `get_entries` · `min_rxn_grand` (141–154 행) |
| μ_Li⁰ = 최저 Li 항목 · φ 2.5–4.5 V 여섯 점 | −1.9089 eV/atom (값은 SI 에 안 씀) | 같은 원장 `mu_Li_metal_eV` · `voltages_V` · 도구 `li_metal_mu` |
| 원자당 정규화 (Li 제외) | | `interface_reactivity_v2.py` 1426 행 주석 (pymatgen `norm=True` = 저장고 원소 뺀 원자수) |
| NCM = LiNi₀.₈Co₀.₁Mn₀.₁O₂ · SE 조성 둘 | | 같은 원장 `results.NMC811.composition` · `reactions` (Li5.4P1S4.4Cl1.6 · Li5.44Nd0.02P0.98S4.37Cl1.6O0.03) · 원고 ms 16 · 18 의 조성식 |
| 모든 전위에서 최소가 중간 x (0 < x < 1) | NMC811 × 두 SE 12 점 | 같은 원장 `endpoint_degenerate` 전부 false (LiMnO₂ 4.5 V 만 true — 이 원고 양극 아님) |
| Nd CEI 띠틈 = PAW psl 세트 · frozen-4f · 비스핀 · U 없음 (비스핀 · U = 선언 + 8 월 frozen-4f 런 · 09-19 입력은 확인할 것 1) | Li sl · P n · S nl · Cl nl 1.0.0 · O n 0.1 · Nd spdn 1.0.0 | `cei_product_gap_card_2026_10_27.json` `12_개정_1_2026_10_27_결과_전` `A1_PP_세트` (09-19 세트) · md5 `db/raw/cei_product_gap_2026_10_27/pseudo_md5.txt` · `build_dft_inputs.py` 686–699 행 (frozen-4f 에 U 를 주면 멈춘다 · 스핀은 `--no_nd_spin` 을 줘야 꺼진다) · `db/properties/sei_electronic_class.json` declared 줄 (*'`--nd_u 0 --no_nd_spin` 필수'*) · `sei_electronic.json` `*_frozen4f` (`spin_polarized` false) |
| vc-relax mv 0.01 · k 간격 0.30 / nscf 0.15 Å⁻¹ (2π 포함) · 밴드 1.35 배 + 8 · fixed 점유 (8 월 SEI · 9 월 CEI 같은 규칙) | | `build_dft_inputs.py` 37–42 · 261–266 · 717 · 720–787 행 · `cei_gap_results_2026_09_19.json` `방법` |
| 잔류 압력 ±1 kbar | −0.93 ~ +0.22 kbar (10 종) | `cei_gap_results_2026_09_19.json` `⛔_NdP5O14_미재현` `확인한_것_전부_정상` `수렴` |
| MP 구조에서 시작 | 10 종 표적 | `db/properties/cei_gap_structures_2026_09_17.json` `targets` |
