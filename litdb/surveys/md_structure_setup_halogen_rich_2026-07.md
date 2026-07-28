# MD 이온전도(σ/Ea) 계산의 구조 세팅 관행 서베이 — halogen-rich 중심 (2026-07)

> type `survey` · 작성 2026-07-27 · 근거: litdb/papers/ digest 전수 + 웹 보강(⚠ PDF 미보유 딱지) ·
> 목적: **comp2(Li₆PS₅Cl₀.₅Br₀.₅, 혼합 할라이드)·disorder ensemble 셀 제작의 기준 문서**
> ⚠ 2026-07-27 정정: 이 문서는 comp2 조성식을 Li5.4PS4.4Cl1.6 으로 3곳에서 오기했었다.
>   Li5.4PS4.4Cl1.6 은 **modelc**다. comp2 는 Li₆PS₅Cl₀.₅Br₀.₅ (Li6, 공공 없음, Cl→Br 등가 치환).
>
> 규율: 이 문서의 모든 문헌 수치는 **소환값**이다. 방법 명시 없이 우리 db(db/properties/) 절대값과
> 혼용하지 않는다. 웹 보강 항목은 원문 PDF 미보유 — 인용 전 원문 확인 필수. INDEX.md는 갱신하지 않음
> (관련 다이제스트는 본문 링크로만 연결).

---

## 1. 한눈 비교표

### 1a. 본대 — σ/Ea 목적 MD가 있는 논문 (litdb 보유)

| 논문 | 조성 | 구조 출처 | 무질서 처리 | supercell/nat | 할라이드 자리 배정 | Li 배치·보상 | 엔진·T·시간 | σ/Ea 추출 | 출처 |
|---|---|---|---|---|---|---|---|---|---|
| gilgonzalez2022 | LPSCl 1.0/1.5/2.0 | n/a(다이제스트 미기재) | 미명시 — 메커니즘 서술만(Cl↑→4c 무질서) | n/a | 초과 Cl→4c 점유(cage Li 상호작용 약화→inter-cage jump↑) | n/a | AIMD(ecut 300 eV, Γ-only), NVT Nose-Hoover 900 K, 100 ps, dt 2 fs | Arrhenius Ea = 0.43(Fig S3; 본문 325.48 meV — 원문 내부 불일치)/0.230/0.293 eV(x=1.0/1.5/2.0); σ는 900 K 외삽(1.5 peak 14.55 mS/cm); Li 확률밀도 iso 0.0015 a0⁻³ | [litdb](../papers/gilgonzalez2022_synergistic_cl_constricted_esw.md) |
| liu2022_cl | Li6PS5Cl·Li5.5PS4.5Cl1.5 | 자체 Rietveld 파라미터(4d Cl 13.3→61.7%) | 대칭구별 배열 전수 enumeration(Li/vac + S/Cl) → **lowest-Ewald 단일 배열**(SQS 아님, AIMD 비용) | n/a | Cl은 4a·4d 양쪽 부분점유(도식: 4a 90%/4d 60%, LPSCl 기준); Cl-rich에서 4d 무질서 61.7% | Li/vacancy 부분점유를 enumeration에 포함 | AIMD(VASP류, Γ-only, lower ecut), NVT; 계면 300 K / bulk 900 K, 총 50 ps, 2 fs | bulk σ/Ea 절대값 **미보고** — MSD 상대비교(1.5 ≈3×, 3방향)·확률밀도·RDF만 | [litdb](../papers/liu2022_cl_crystallization_interface_argyrodite.md) |
| rao2025 | Li5.5PS4.5Cl1.5₋ₓIₓ | ICSD Li6PS5Cl(48h occ 0.5 조정); hull/계면은 MP·pymatgen 소환 | pymatgen enumeration + Ewald 최소E 단일 배열(SQS 아님); **4a/4d antisite disorder 의도적 회피**(계산비용, 저자 자인) | 1×1×1 argyrodite(격자 ~10 Å, ~52원자급) | 할라이드 4a만 배치(digest L79 "4a만 고려"·L140 "only 4a, not 4d") — ⚠ 단 다이제스트 무질서 처리 필드(L78)엔 "4d 자리에서만"으로 기재, digest 내부 표기 충돌(원문 확인 필요). site-preference DFT: Br 4a>4d ΔE 0.14 / I 0.35 eV/atom | Li 48h 0.5를 enumeration+Ewald iterative 제거 | AIMD(VASP, Γ), NVT 600–1000 K 5점(100 K 간격), 총 110 ps(평형 10 + MSD 100), 2 fs | D=MSD/(2NdΔt), σ=Nernst–Einstein, Arrhenius 300 K 외삽(변동 저자 자인); Ea 최소 0.18 eV(등량 I/Cl) | [litdb](../papers/rao2025_iodide_argyrodite.md) |
| son2025 | Li2TiF6(+Cl 치환) — 비아지로다이트지만 enumerate 노선 참고 | MP mp-7603; 실험 동정 ICSD 256029 | enumeration: TopographyAnalyzer로 Li 자리 preselect(16 tet) → 30 config lowest-Ewald → DFT relax 후 lowest-E 채택 | AIMD 1×1×1(Γ; relax 2×2×1, a=b=9.20152/c=8.84076 Å) | Cl 치환은 48 F 자리에서 비율 맞춰 enumerate | Ewald→DFT lowest-E에 포함 | AIMD(VASP/PBE, ecut 520 eV), NVT NH(period 80 fs), 1000–1400 K, 온도당 200 ps, 2 fs | D=MSD 선형피팅(pymatgen) → Arrhenius Ea; Zeo++ 채널 분석 | [litdb](../papers/son2025_fivevolt_assb.md) |
| liang2025 | argyrodite(준층상 재해석) | cubic F-43m(#216) 표준 구조에서 자체 구성 | 단일 결정학적 배열 decorate — **4a/4c disorder 0/25/50/75/100% 스캔**(SQS/enumerate 아님); 50%에서 P2mm/P222₁ 두 배열 구성 후 P2mm 채택 | n/a(SI) | 50% disorder에서 halide(4a)·S(4c) 자리 교환 → P2mm 준층상; Mayer 결합차수 4a-Cl–Li < 4c-S–Li | n/a | AIMD+CI-NEB(코드 미명시, GTH-PBE-q3→CP2K 계열 시사), 500/700/900 K, 궤적 20 ps, dt n/a | T별 σ → Arrhenius 300 K 외삽 + Ea(AIMD 0.088 / NEB inter-cage 0.12 eV); 층별 MSD 분리; σ 절대값은 외삽 인공물 가능(1.18 S/cm 등) | [litdb](../papers/liang2025_quasilayered_argyrodite_li_migration.md) |
| schneider2023 | t-Li7SiPS8 | 결정구조(+BV iso-energy 채널) | n/a(AIMD는 ref 38·48 별도 수행, 보조) | n/a | 해당 없음 | n/a | AIMD(VASP류) — 앙상블·T·시간·dt 전부 n/a | MSD→D→σ(NE); 격자 scaling f=1.00/0.99/0.98 → ΔV 1.7–2.0 cm³/mol; 장벽 0.22(1D)/0.28(3D) eV = BV+AIMD | [litdb](../papers/schneider2023_particle_size_pressure_transport.md) |
| ke2025 | MgClO 도핑 계면 | n/a | n/a | n/a(Li/SE slab) | Mg→48h(Li 자리), O→4d(free-S 자리) — 실험 Rietveld 진화 | n/a | AIMD(VASP 추정, PBE/PAW, 300 eV, k 1×1×1), NVT NH, dt 1 fs; T·시간 n/a | **수송 아님** — 계면 안정성/ELF·PDOS용 | [litdb](../papers/ke2025_orbital_hybridization_mgclo.md) |

### 1b. 방법론 참고 — 비AIMD·비아지로다이트 (litdb 보유)

| 논문 | 시스템 | 무질서/초기구조 처리 | 엔진·조건 | σ/Ea 추출 | 출처 |
|---|---|---|---|---|---|
| ishikawa2025 | rock-salt telluride 격자(LixPb1-2xBixTe), N=13,824 | cation **단일 무작위 배열**(랜덤 decorate; SQS/enumerate/실험점유 아님 — N이 커서 단일 배열로 통계 충분이 근거) | 자체 고전 MD(WCA+Coulomb), NPT→PR-stress+NH, 295 K, E=2.1, Δt=0.002(환산) | **σ=⟨J⟩/E(field-driven) vs σ_NE 별도 산출 — σ_NE가 ~2 orders 작음**(cooperative 판정) | [litdb](../papers/ishikawa2025_site_percolation_cooperative_ion_conduction.md) |
| choi2025_mlip | Cu/TaxN 계면(접착; σ 해당 없음) | 비정질 = melt-quench-anneal AIMD **ensemble, 조성당 10구조**(RDF/ADF로 DFT 대비 검증); bulk 학습셋 ICSD ±5% strain 441구조 | SevenNet MLIP(LAMMPS) + 참조 AIMD VASP(400 eV, Γ, 2 fs); MLIP-MD 3100원자 7.7 ns | 해당 없음(W_ad는 SMD+Jarzynski PMF) | [litdb](../papers/choi2025_mlip_cu_taxn_interfacial_adhesion.md) |
| rao2011 | Li6PS5X BVSE | **실험 점유 decorate** — 자체 Rietveld(GSAS)+Deiseroth 단결정+Pecher Li 분포를 BV grid에 그대로 반영(half-occupied Li, S/halide 혼합 점유; Br 케이지 84% S/16% Br) | BVSE(bond-valence + Morse-type, 0 K, relaxation 무시 — 저자 명시) | 경로별 Ea 0.15–0.35 eV(BV grid <0.1 Å); σ·Ea 실측은 임피던스 | [litdb](../papers/rao2011_argyrodite_se_studies_bvse.md) |
| ma2024 | Sb-doped LPSC | n/a — decorate 방법 미공개, single-config 추정; DFT 파라미터 전부 미기재 → digest가 "재현·검증 불가" 명시 | 정적 확산좌표 에너지곡선만(AIMD·MLIP 없음) | intra 0.873→0.496 / inter 0.976→0.592 eV — ordered 단일경로는 무질서·다경로·concerted 무시로 과대, **절대값 비교 금지** | [litdb](../papers/ma2024_sb_doping_lpsc_conductivity.md) |
| dyre2004 | 격자 hopping 모델(비결정) | 무질서를 SQS decorate가 아니라 장벽 확률밀도 p(E)를 link별 무작위 샘플(quenched disorder) | hopping MC/master-equation(RBM) | dc σ = 영-장 MSD(fluctuation-dissipation) | [litdb](../papers/dyre2004_hopping_models_ion_conduction_noncrystals.md) |
| liu2013 | 메탄 하이드레이트 cage(도메인 밖, 구속 MD 기법만 참고) | 초기구조 = 선행 MD 궤적에서 FSICA로 cage 8종 추출 | GROMACS, NPT NH+PR, 258.5 K·30 MPa; 56 구속점×20 독립시뮬 | 구속력 적분→PMF→Ea(엔트로피 보정) | [litdb](../papers/liu2013_cage_methane_adsorption_hydrate_nucleation.md) |
| kang2025_bollard | binder fragment/NMC 슬랩 | fragment 흡착 배치(15개 배향) | MLP-MD(세부 SI=n/a), Langevin NVT 400 K, 10 ps | 해당 없음(탈착 hold-test 거리 시계열) | [litdb](../papers/kang2025_bollard_anchored_binder_dry_electrode.md) |
| DEM/CGMD 군(ngandjong2021·wet_processing·duquesnoy2023) | 전극 공정 | 랜덤 배치를 그대로 쓰지 않고 **공정(평형→건조→압연)으로 구조 형성** — 우리 DEM '랜덤 비중첩 삽입'과 대비되는 초기구조 철학 | LAMMPS CGMD/DEM | MD에서 σ 추출 안 함(GeoDict/COMSOL/TauFactor) | [litdb](../papers/ngandjong2021_dem_calendering_digital_twin.md) 외 |

### 1c. 웹 보강 — halogen-rich·argyrodite MD 계보 (⚠ 전부 PDF 미보유, 인용 전 원문 확인)

| 논문 | 조성 | 무질서/decorate | supercell/nat·시간 | σ/Ea 추출 | 출처 |
|---|---|---|---|---|---|
| ✅ de Klerk 2016 (Chem. Mater. 28, 7955) — **digest 확보 2026-07-28** | Li6PS5X (X=Cl/Br/I) | Cl 4c(=우리 4d) 점유 **0/25/50/75/100% 5단계, 각 %당 배열 1개**(복수 배열·선택기준 언급 전무); Li는 48h 쌍당 1개 제거(24 Li), 공공 배치 규칙 없음 | **1×1×1 (52원자)**, velocity-rescale NVT, dt 2 fs, 총 100 ps(equil 2.5 ps), T 300/450/600 K, VASP PBE 280 eV | 75% 최적 = **450 K 단일점·Cl1.0 전용·min-jump-rate 지표**(σ 직접 아님); **비단조**(0%·100% 모두 저전도 — 100%는 doublet 붕괴로 새 율속) | [digest](../papers/deklerk2016_diffusion_site_disorder_argyrodite.md) |
| ⚠ Deng 2016 (JES 163, A67) | 23종 SICE 탄성 | **"SQS 아지로다이트"로 지목 — 웹 확인 실패, torii2025 2차 귀속만 확보**(보유 PDF [torii2025](../papers/torii2025_lpscl_mechanical_anisotropy_dft.md) digest L28 'ref10 Deng 2016, SQS'·L109 '그들이 명시적으로 대비'); Ong 그룹 관행은 enumerate+Ewald 최저 배열 — 단 Deng 원문 직접 확인은 여전히 필요 | — | 탄성텐서(σ/Ea 아님) | [IOP](https://iopscience.iop.org/article/10.1149/2.0061602jes) |
| ⚠ Deng 2017 (Chem. Mater. 29, 281) | Li6PS5Cl | 열거 후 최저에너지 배열 선택으로 서술 | 세부 미인용(웹 요약 혼입 위험) | 상안정성+ESW+AIMD σ 워크플로 | [ACS](https://pubs.acs.org/doi/10.1021/acs.chemmater.6b02648) |
| ⚠ Stamminger 2019 (Chem. Mater. 31, 8673) | Li6PS5X(X=Br,Cl,I) | 질서형 vs 무질서형 구조유형별 AIMD — 결론: **확산도는 할로겐 종이 아니라 무질서 정도가 지배** | 웹 미확인 | AIMD 확산도; antisite 결함 형성E로 설명 | [ACS](https://pubs.acs.org/doi/10.1021/acs.chemmater.9b02047) |
| ⚠ Morgan 2021 (Chem. Mater. 33, 2004) | Li6PS5I(+Cl) | **S/X site-inversion 0/50/100% 명시 스캔** | production 70 ps, PBEsol | 무질서 배열 = percolating 3D + string-like 협동; 질서 = 경로 단절 | [chemrxiv](https://chemrxiv.org/engage/chemrxiv/article-details/60c7556c702a9ba9f218c6e0) |
| ⚠ He/Zhu/Mo 2018 (npj Comput. Mater. 4, 18) | (방법론) | — | — | AIMD 오차 정량화 원전: 분산 = 관측 확산 이벤트 수로 정량, **MSD 선형(확산) 구간만 피팅**(ballistic 제외), 빠른 전도체에만 AIMD 적용 가능 | [Nature](https://www.nature.com/articles/s41524-018-0074-y) |
| ⚠ Baktash 2020 (npj Comput. Mater. 6, 162) | Li6PS5Cl + **Li5PS4Cl2**(halogen-rich 끝단) | — | Li5PS4Cl2는 300/600/800/1000 K | EMD+NEMD 병행; LPSCl 상온 σ는 EMD 통계 부족으로 color-field AI-NEMD | [Nature](https://www.nature.com/articles/s41524-020-00432-1) |
| ⚠ Adeli 2019 (Angew. 58, 8681) | **Li5.5PS4.5Cl1.5 실험 원전** | (실험) 4a/4c SOF를 Li6PS5Cl과 비교 — 사이트 무질서↑+Li 공공↑+Li-framework 약화가 기작 | — | cold-pressed σ(298 K)=9.4±0.1 / 소결 12.0±0.2 mS/cm; PGSE-NMR D=1.01×10⁻¹¹ m²/s; Vegard 준수 | [Wiley](https://onlinelibrary.wiley.com/doi/10.1002/anie.201814222) |
| ⚠ Zhou 2025 (JMCC, D5TC00529A) | Li5.5PS4.5Cl1.5(-I) | **Adeli 조성을 계산 셀로 옮긴 decorate 실례**: MP Li6PS5Cl에서 출발, 4a는 전부 Cl·4d는 S/Cl 혼합 — 실험 SOF(4a/4d 부분점유)와 다른 이상화 | VASP PAW-PBE 520 eV | AIMD σ=18.86 mS/cm(Cl1.5), 최댓값 23.5(Cl0.75I0.75) | [RSC](https://pubs.rsc.org/en/content/articlehtml/2025/tc/d5tc00529a) |
| ⚠ Lee 2024 (ACS AMI 16, 46442) | Li6PS5Cl | MLP로 disorder-% 스캔 — **σ 최대는 Cl이 4c의 25%일 때**(50%가 아님) | σ 수렴(오차 10% 이내)에 **5×5×5 supercell(6500원자)·25 ns** | 300 K 직접 계산; >400 K non-Arrhenius | [ACS](https://pubs.acs.org/doi/10.1021/acsami.4c08865) |
| ⚠ Jang 2025 (JMCA 13, 16547) | Li6PS5Cl | 사전학습 SevenNet-021 fine-tune(PES softening 해소); high-entropy 음이온 무질서 → site-energy 균일화 → inter-cage jump 촉진 | 300 K MSD가 **4×4×4(3328원자)에서 수렴** | MLIP-MD | [RSC](https://pubs.rsc.org/en/content/articlelanding/2025/ta/d5ta02205c) |
| ⚠ Kim 2024 (Nano Energy 124, 109436) | Li6PS5X(X=Cl,Br,I)+GB | MTP; site disorder를 3×3×3(>1000원자)에 **무작위 배열 6개 configuration으로 표본화** | 3×3×3 supercell | GB에서 Li 축적으로 σ 지연 | [SD](https://www.sciencedirect.com/science/article/abs/pii/S2211285524001848) |
| ⚠ Ou 2024 (PRM 8, 115407) | Li6PS5Cl | MTP+active learning; **anion-ordered vs 50% Cl/S disordered 벌크 정량 비교** | >16,000원자·5 ns | 300 K D: 질서 1.2×10⁻⁹(σ~0.2 mS/cm) vs 50% 무질서 2.2×10⁻⁷ cm²/s(~29.8 mS/cm) — **decorate가 σ 두 자릿수를 좌우** | [arXiv](https://arxiv.org/html/2407.04126v2) |
| ⚠ Nazar group 2024 (Cell Rep. Phys. Sci. 5) | **Li5.3PS4.3Cl1.7**(halide-rich 한계) | (실험→계산) NPD로 Li의 T4(16e) interstitial 점유 확인; DFT-MD 해석: 4a/4d 무질서 유지 + Cl/S 비 증가가 기작 | — | σ_RT=11.4±0.7 mS/cm; 국소 장벽 0.08 eV(3-site Li 분포) | [Cell](https://www.cell.com/cell-reports-physical-science/fulltext/S2666-3864(24)00628-3) |
| ⚠ Energies 2022 리뷰(15, 7288) | argyrodite 분자모델링 총람 | de Klerk/Stamminger/Baktash 등 셋업 비교의 진입점(오픈액세스); 저자명 웹 미확정 | — | — | [MDPI](https://www.mdpi.com/1996-1073/15/19/7288) |

### 1d. n/a 그룹 — MD 셋업이 없는 논문 (필드 기록만)

- **리뷰(자체 계산 0)**: [bai2020](../papers/bai2020_argyrodite_review_progress.md) ·
  [fan2026](../papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md)(소환: Li/LGPS AIMD 0→11.7 ps, 3층 MD 0→100 ps — 앙상블·dt·셀 미기재) ·
  [kang2026](../papers/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md)(소환: Banerjee LPSCl–NCA AIMD 50 ps) ·
  [he2019](../papers/he2019_dft_for_battery_materials_review.md)(일반 지침만: 고온·수백 원자·수십~수백 ps, MSD=6Dt→Arrhenius→NE 노선).
- **계산 있으나 MD 없음**: [sundar2025](../papers/sundar2025_oxide_coating_screening_lpscl.md)(CI-NEB만) ·
  [torii2025](../papers/torii2025_lpscl_mechanical_anisotropy_dft.md)(0 K static) ·
  [shi2017](../papers/shi2017_hbn_interfacial_layer_li_anode.md)(NEB만) ·
  [banik2022](../papers/banik2022_substitutions_oxidative_stability_argyrodite.md) ·
  [zhu2020](../papers/zhu2020_air_stable_se_design_principles.md) ·
  [choi2026](../papers/choi2026_bzox_dry_zro2x_nmc_shell_coating.md)(보조 pDOS DFT만).
- **계산 0(실험)**: taklu2021 · yang2025 · hikima2022 · wang2022 · lee2026 · liu2022_hbn · kang2025_highvoltage ·
  kim2025 · kim2026 — σ·Ea는 EIS Arrhenius 등 실험값.

---

## 2. halogen-rich 셀 만들기 관행 정리

### 2.1 초과 Cl은 어느 자리로 가나 — **완전한 합의는 없다**

방향성 합의는 하나뿐이다: **초과 할라이드는 free-S 부격자(4d 또는 4c 표기)로 들어가 음이온 무질서를
키우고, 이것이 σ 상승의 구조적 기작**이라는 것 (liu2022 Rietveld 4d 13.3→61.7%, gilgonzalez2022 AIMD
4c 무질서→inter-cage jump↑, bai2020 리뷰의 de Klerk 예측 확인, kim2021 리뷰의 Cl=최강 disorder 서열,
⚠ Adeli·Stamminger·Nazar 계보 동일). 그러나 **정확한 4a/4d 분배는 논문마다 갈린다**:

| 진영 | 주장 | 근거 유형 |
|---|---|---|
| [lu2025](../papers/lu2025_tailoring_cl_rich_anode_licl.md) | Cl15에서 초과 Cl이 **4d를 거의 채움**: 4a 56.32% / 4d 90.01% (4d>4a) | 실험 NPD Rietveld (Rw 2.19%) |
| [liu2022](../papers/liu2022_cl_crystallization_interface_argyrodite.md) | Cl은 4a·4d **양쪽 부분점유**(도식 4a 90/4d 60%), Cl-rich에서 양쪽↑ | 실험 XRD Rietveld |
| [taklu2021](../papers/taklu2021_cucl_dualdoping_air_stability_argyrodite.md) | 초과 Cl → **4a+4c** | 싱크로트론 Rietveld(자리귀속 완전 확정은 어려움 — digest 주의) |
| ⚠ Zhou 2025 (계산 decorate) | **4a 전부 Cl + 4d 혼합** — 실험 SOF와 다른 이상화임을 유의 | 웹 소환값 |
| ✅ de Klerk 2016 (계산, digest) | Li6PS5Cl은 Cl 4c(=4d) 75%에서 **limiting jump rate 2×**(50:50 대비, 450 K) — σ 직접 계산 아님, 비단조 | digest 확보. ⚠ 2024 MTP-MLIP(INDEX 계산#8, 미digest)는 **25% 피크** 보고 — '최적 %'는 방법 의존, 안전 인용은 '양 끝 나쁨·중간 최적'까지 |
| [rao2025](../papers/rao2025_iodide_argyrodite.md) (계산) | 할라이드 본질 선호는 **4a**(Br ΔE 0.14 / I 0.35 eV/atom) — 단 disorder 자체를 회피한 단순화 | DFT 단일배열 |

에너지 지형 근거로는 lu2025의 DFT가 결정적이다: **4a+4d 분산 점유가 최안정(−192.1 eV), 4d 완전점유는
metastable(+15.2 eV, 자기분해→LiCl 구동력)**. 즉 "초과 Cl을 4d에 몰아넣는 단일 배열"은 물리적으로
준안정 상태를 모사하는 것이며, halogen-rich 셀은 **4a/4d 분산 배치가 기본값**이어야 한다.

표기 주의: free-S 자리를 4c로 쓰는 논문(gilgonzalez, taklu, liang, ⚠ de Klerk·Adeli·Lee2024)과 4d로
쓰는 논문(kraft, liu2022, lu2025, rao2025, 우리)이 섞여 있다 — 원점 선택 차이. 인용 시 원문 표기 병기.

무질서 크기의 실험 기준값(계산 셀의 target으로 쓸 수 있는 소환값):
- x=1.0 (Li6PS5Cl): 4d 무질서 **~62%** ([kraft2017](../papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md), 중성자 Rietveld) / **13.3%**(liu2022 LPSCl-550°C — 합성조건 의존).
- x=1.5 (Li5.5PS4.5Cl1.5): 4d 무질서 **61.7%**(liu2022) / Cl 점유 4a 56.32·4d 90.01%(lu2025).
- 계열 규칙: Cl ~62% > Br ~22% > I 0% (kraft2017; 이온반경 논리 — Cl 1.81·Br 1.96 ≈ S²⁻ 1.84 Å, I 2.2 Å 과대).

### 2.2 Li vacancy 보상 — 계산은 Ewald, 실험은 자리 재배치

- **계산 관행**: Li/vacancy를 음이온 무질서와 함께 enumeration에 넣고 lowest-Ewald로 뽑는다
  (liu2022 전수 enumeration, rao2025 iterative Ewald 제거, son2025 Ewald→DFT lowest-E).
  이 표본에서 Li 보상을 실험 점유율로 매칭한 계산 사례는 **없다**.
- **실험 관측** (계산이 아직 안 담는 물리): 48h→24g 재배치(kraft2017: Cl→I에서 48h 0.500→0.391,
  24g 0→0.219), 추가 Li→24g bridge(taklu2021), Li cluster 재분포(lu2025 ⁷Li NMR),
  ⚠ T4(16e) interstitial 점유(Nazar 2024, NPD).
- 반례 경고: yang2025는 Rietveld 표가 명목-고정 템플릿(Li 48h 0.5 고정=명목과 불일치) — 점유율
  인용 시 정련인지 가정인지 확인 필수.

### 2.3 실험 점유율 매칭 vs 임의 배열 — 분포 지도

argyrodite 문헌의 무질서 처리 분포(종합 패턴, [_TEMPLATE.md](../papers/_TEMPLATE.md) 표준 필드 기준):

1. **enumerate→lowest-Ewald→단일 배열**: liu2022, rao2025, son2025 — 지배적 관행. 우리 modelc와 동일 철학.
2. **ordered single-config**: torii2025(ASE 생성), choi2026(MP 정합 셀) — 대조군 성격.
3. **실험 점유 decorate**: rao2011(BV grid에 Rietveld 점유 그대로), lu2025(NPD 점유 반영 단일 배열).
4. **disorder-% 명시 스캔**: liang2025(0–100%), ⚠ Morgan 2021(0/50/100%), ⚠ Lee 2024(MLP, 최적 25%).
5. **무작위 배열**: ishikawa2025(단일, N=13,824), ⚠ Kim 2024(6 config), choi2025(비정질 MQA 10구조).
6. **미명시(n/a)**: sundar2025, banik2022, ma2024, li2025, taklu2021(DFT측) — 단일 배열 추정,
   **절대값 비교 금지**가 digest 공통 규율.

**SQS는 이 표본에서 Deng 2016 귀속 하나뿐인데, 그마저 웹 확인 실패, torii2025 2차 귀속만 확보** —
SQS 귀속의 2차 출처는 torii2025 본문(ref10 대비, 보유 PDF; digest L28·L109) — 단 Deng 원문 직접 확인은
여전히 필요 (⚠).
즉 "argyrodite 무질서 = SQS"는 문헌 실태가 아니다 — 실태는 enumerate-Ewald 단일 배열이 다수,
스캔·앙상블이 소수, 실험 매칭이 극소수다. **표준이 없으므로, 무엇을 택하든 근거 명시가 의무다.**

### 2.4 구조 선택이 결론을 움직인 문서화 사례 (셀 제작이 왜 중요한가)

- **탄성 이방성 부호 반전**: torii2025(ordered) Zener A=1.09>1 vs ⚠ Deng 2016(무질서 처리 상이) A=0.92<1
  (torii2025 digest L28 소환) — 무질서 처리 선택이 부호를 뒤집음 ([torii2025](../papers/torii2025_lpscl_mechanical_anisotropy_dft.md)).
- **σ 두 자릿수**: ⚠ Ou 2024 — 질서 vs 50% 무질서에서 300 K D가 1.2×10⁻⁹ → 2.2×10⁻⁷ cm²/s.
- **Ea 자릿수** (우리 내부 사례, dyre2004 digest 인용 — 우리 db 값 소환 주의): ⚠ **여기서 'ordered'는
  d = 0.00 완전질서 *구성셀***(n_configs 1, li_transport.json `disorder_ensemble_2026_06_09`)이고,
  **canonical 자연 4 f.u. comp1 셀과 다른 대상**이다 — canonical comp1은 같은 프로토콜에서 Ea **0.253 eV**로
  정상이다(즉 1.17은 '질서의 귀결'이 아니라 그 특정 셀의 저온 undersampling 아티팩트).
  그 d = 0.00 셀은 600–800 K에서 얼어붙어 Ea 1.17 eV로 인위 폭발, 현실적 Cl/S anti-site 도입 시 0.177 eV
  ([dyre2004](../papers/dyre2004_hopping_models_ion_conduction_noncrystals.md) L166-167).
- **안정성 판정**: lu2025 — 4a/4d Cl 배치에 따라 −192.1 eV(최안정) ↔ +15.2 eV(metastable).
- **공간군 재해석**: liang2025 — 50% 배치가 F-43m→P2mm 준층상을 만들고 P2mm/P222₁ 선택이 σ 결론 좌우.
- **hull 상 선택**: gilgonzalez2022 — LiS4 등 3상 제외 여부로 산화 onset이 2.14→2.26 V 이동(우리 재현).

---

## 3. σ/Ea 추출 관행 — 문헌 vs 우리 규율

우리 규율(CLAUDE.md·tools/ionic/ 표준): UMA-s-1p1(omat) Langevin NVT, dt 2 fs, friction 0.02,
equilib 5 ps / prod 200 ps, **MSD 창 2–50 ps 고정**, Arrhenius **600/800/1000 K 3점**(400/500 K 제외 판정),
σ는 NE(Haven=1) — **절대값 인용 금지, 비율도 멀티시드 판정만**, Ea 오차막대는 600 K 3-시드.

| 항목 | 문헌 관행 (표본 범위) | 우리 규율 | 정직한 판정 |
|---|---|---|---|
| MSD 창 | 명시 고정 창은 드묾. rao2025: 평형 10 ps + MSD 100 ps. ⚠ He 2018: "선형 구간만 피팅"(원칙만, 창 미고정). liang2025: 궤적 20 ps(통계 부족 위험) | **2–50 ps 고정** | 우리가 더 엄격 — 창 고정은 재현성·차원에서 문헌 다수보다 명시적 |
| 온도점 | 900 K 단일(gilgonzalez, liu2022 bulk) / 1000–1400 K(son2025) / 500·700·900 K(liang) / **600–1000 K 5점**(rao2025) / ⚠ 300–1000 K(Baktash) | 600/800/1000 K 3점, 400/500 K 제외 판정 | 단일-온도 외삽 논문보다 엄격. rao2025 5점보다는 점 수가 적음 — 대신 저온 undersampling 제외 사유를 명문화한 건 우리 쪽 |
| 300 K 외삽·σ 절대값 | 대부분 외삽 절대값 보고: gilgonzalez 14.55 mS/cm(900 K 외삽), liang 1.18 S/cm(**외삽 인공물 가능 — digest 판정, 저자 자인 아님**; digest L48), rao2025 외삽 변동 자인(이쪽은 진짜 저자 자인), ⚠ Zhou 18.86 mS/cm. 예외: liu2022는 절대값 미보고(상대만) — 우리와 같은 태도 | **σ 절대값 인용 금지**, 비율만 | 우리가 훨씬 엄격. 문헌 σ 절대값은 전부 소환값 취급, 우리 값과 한 표에 섞지 않기 |
| 통계·시드 | 대부분 단일 궤적·단일 배열. ⚠ He 2018: 이벤트 수 기반 오차 정량(원전). ⚠ Kim 2024: 6-config 표본화 | **멀티시드 판정 의무**(단일시드 1.33× 철회, SEMIFINAL 2026-07-09), Ea 오차막대 600 K 3-시드 | 우리가 더 엄격 — 문헌 대부분은 시드 반복 없음 |
| σ 공식 | NE 지배적(rao2025 eqn 2, schneider2023, he2019 노선). **예외: ishikawa2025 field-driven σ=⟨J⟩/E vs σ_NE가 ~2 orders 차이**(cooperative계) | NE, Haven=1 | **우리가 느슨한 지점** — Haven=1 가정은 협동 확산이 강하면 깨질 수 있음(ishikawa가 경고 사례). 절대값 금지 규율이 위험을 부분 상쇄하지만, 비율 인용 시에도 조성 간 Haven 비 변화 가능성은 명시할 것 |
| 셀 크기·시뮬 길이 | AIMD: 1 unit cell급(rao2025 ~52원자, ⚠ de Klerk 4 f.u.) + 50–200 ps. MLIP: **수렴 명시가 표준화 중** — ⚠ Lee 5×5×5·6500원자·25 ns(σ 오차 10%), ⚠ Jang 4×4×4·3328원자, ⚠ Ou >16,000원자·5 ns | prod 200 ps(MLIP-MD) — 셀 크기 수렴 기준은 우리 표준 문서에 별도 명시 없음 | **우리가 느슨할 수 있는 지점** — MLIP를 쓰면서 AIMD급 셀에 머물면 300 K 직접 계산 문헌 대비 약점. comp2 캠페인에서 셀-크기 체크 1회 기록 권고(§5) |
| 저온 직접 계산 | ⚠ Lee 2024·Ou 2024는 300 K 직접(외삽 회피, >400 K non-Arrhenius 보고) | 600 K 이상만, 300 K 외삽·절대값 자체를 안 함 | 방향이 다름 — 우리는 외삽 오류를 "절대값 비인용"으로 차단, 문헌 최전선은 "저온 직접 계산"으로 해소. 장기적으로 후자가 상위 호환 |

---

## 4. 우리 위치 — comp2 ordered baseline + d=0.50 ensemble

**조성**: ⚠ **축 주의** — 아래 '스윗스팟' 논거는 전부 **Cl 함량 축**(Li6PS5Cl → Li5.4PS4.4Cl1.6)이라
**modelc** 에 적용되는 이야기이고, **comp2(Li₆PS₅Cl₀.₅Br₀.₅)는 할라이드 *종류* 축**(Cl→Br 등가 치환,
Li6 공공 없음)이라 그대로 이식되지 않는다. 소환 문헌(gilgonzalez2022 LPSCl1.5 · Feng x=0.7 ·
⚠Adeli Cl1.5 · ⚠Nazar Cl1.7)이 모두 Cl 함량 축이다. comp2 무질서 목표치는 Cl 기준 ~62%가 아니라
**Br 기준 ~22%(kraft2017)** 로 잡아야 하고, 현 d=0.50 앙상블 설정이 Cl 62%에서 왔다면 재검토 대상.
modelc = Li5.4PS4.4Cl1.6은 문헌 halogen-rich 스윗스팟 한가운데다 — gilgonzalez2022 Ea 최저는
LPSCl1.5(0.230 eV), bai2020이 소환한 Feng의 Ea 최저는 x=0.7(Li5.3PS4.3Cl1.7), ⚠ Adeli(Cl1.5)·⚠ Nazar
2024(Cl1.7) 실험 계보 사이. 비교 대상 실험 원전(⚠ Adeli σ 9.4–12.0 mS/cm, ⚠ Nazar 11.4 mS/cm)과
decorate 실례(⚠ Zhou 2025)가 모두 확보돼 있다(전부 소환값).

**지형상 위치**:

1. **ordered baseline** — torii2025·choi2026 부류의 대조군 관행과 같은 역할. 단 ordered 셀로 수송을
   판정하면 안 된다는 것이 우리 내부 사례(**d = 0.00 완전질서 *구성셀*** Ea 1.17 eV 인위 폭발 →
   disorder 도입 시 0.177 eV, §2.4)와 ⚠ Ou 2024(두 자릿수 차이)·⚠ Morgan(경로 단절)의 일치된 교훈.
   ⚠ 여기서 'ordered'는 **d = 0.00 구성셀**이지 canonical 자연 4 f.u. comp1 셀이 아니다 — 후자는
   같은 프로토콜에서 Ea **0.253 eV**로 정상이라, 정확한 교훈은 "질서가 수송을 죽인다"가 아니라
   "**완전질서 극한은 동역학적으로 접근 불가라 그 셀의 수송값은 못 믿는다**"이다. baseline은
   "disorder 효과의 분모"로만 쓴다.
2. **d=0.50** — 문헌이 가장 자주 찍는 대표 무질서점(liang2025 50% 채택, ⚠ Morgan 50%, ⚠ Ou 50%)과
   정렬. 관행적으로 방어 가능. 단 ⚠ Lee 2024는 σ 최대가 4c 25%(50% 아님)라고 보고 — d=0.50이
   σ-최적이라는 가정은 하지 말 것(우리는 "대표점" 논리로만 방어).
3. **다중 config 앙상블(cfg0/1/2)** — **litdb 보유 논문 중 벌크 σ용 다중 config 앙상블은 없다**(전부
   단일 배열). 유사 사례는 웹 보강의 ⚠ Kim 2024(무작위 6 config)와 비정질 쪽 choi2025(MQA 10구조)뿐.
   즉 config-분산을 σ/Ea 오차막대에 반영하는 것은 이 지형에서 우리 고유 기여로 남는 지점 — 논문에서
   명시적으로 팔 것. 단 신규성 주장은 ⚠ Kim 2024 원문 확보·확인 후에만 원고에 기재(6-config가
   config-분산을 오차막대로 보고했는지는 웹 요약만으로 판정 불가) — 그 전까지는 "litdb 표본 내 부재"로만
   서술(§5 마지막 항목의 ⚠ 인용 금지 규율과 일관).
4. **UMA anneal+relax로 배열 생성** — 문헌 지배 노선(enumerate→lowest-Ewald→DFT)과 다른 경로다.
   Ewald-최저 단일 배열이 "가장 안정한 하나"를 고르는 반면, 우리는 anneal로 물리적으로 접근 가능한
   배열을 표본화한다. 방법 서술에서 이 차이를 명시해야 문헌과의 비교가 성립한다.

**문헌이 하는데 우리가 안 한 것 — 실험 점유율 매칭 decorate**: rao2011(BV grid)·lu2025(NPD 반영)
노선이다. Kraft ~62%(x=1.0), Liu 61.7%(x=1.5), Lu 4a 56.32/4d 90.01%(x=1.5)라는 실측 %가 이미 digest에
있으므로, comp2 앙상블에 **"Rietveld-매칭 cfg"(d≈0.6 부근, 또는 lu2025식 4d-편중+4a 부분 배치) 1개를
추가**하면 d=0.50 임의성 비판을 선제 차단할 수 있다. 반대로 4d-완전점유 배열은 metastable(lu2025
+15.2 eV)이므로 앙상블에 넣더라도 "준안정 참조"로만 라벨링.

**우리가 하는데 문헌이 잘 안 하는 것**: MSD 고정 창, 멀티시드, 절대값 비인용, 저온점 제외 판정 —
§3 표의 엄격 항목들. 반대로 취약 지점은 Haven=1과 셀-크기 수렴 명시(§3)다.

---

## 5. 실무 권고 박스 — 다음 halogen-rich 셀 제작 체크리스트

> comp2(Li₆PS₅Cl₀.₅Br₀.₅) 및 후속 disorder ensemble 셀에 적용. 각 항목은 셀 메타데이터
> (db/structures/ 등록 시)에 기록한다.

- [ ] **표기 규약 선언**: free-S 자리는 우리 관례대로 **4d**로 표기. 문헌 인용 시 원문이 4c면 병기
      ("4c(=우리 4d)"). liang2025 §12·⚠ de Klerk 요약의 표기 충돌을 답습하지 않기.
- [ ] **초과 Cl 배치 규칙 명시**: 기본값은 **4a/4d 분산 배치**(lu2025 DFT 최안정 −192.1 eV; liu2022
      Rietveld 양쪽 부분점유). 4d-완전점유 배열은 metastable(+15.2 eV) — 만들면 "준안정 참조" 라벨.
      어떤 규칙을 썼는지(분산/4d-편중/4a-포화)와 근거 문헌을 메타데이터에 남긴다.
- [ ] **무질서 % 근거 의무**: d 값은 셋 중 하나로 정당화 — ① 실험 Rietveld 매칭(x=1.0: ~62% kraft /
      x=1.5: 61.7% liu2022·4a 56/4d 90 lu2025), ② 명시적 스캔(0/25/50/75/100 부분집합; ⚠ Lee 2024의
      25%-최적 보고 때문에 0.25 포함 권장), ③ 문헌 대표점(0.50 — liang·⚠ Morgan·⚠ Ou 정렬).
      "그냥 0.50"은 금지 — 반드시 ③으로라도 근거를 적는다.
- [ ] **Li 보상 절차 기록**: vacancy 배치 방법(enumerate-Ewald인지, 무작위+UMA anneal인지)을 명시.
      24g·16e 점유 허용 여부도 기록 — 실험은 48h↔24g 재배치(kraft)·⚠ T4(16e) 점유(Nazar)를 보므로,
      48h-only 강제는 그 자체가 가정임을 남긴다.
- [ ] **config ≥3 + 멀티시드**: config 앙상블(cfg0/1/2 이상, ⚠ Kim 2024의 6개가 상한 참고) × MD
      멀티시드. 단일시드 비율 판정 금지(1.33× 철회 사례). config-분산과 시드-분산을 구분해 보고.
      **선행 작업: ⚠ Kim 2024 PDF 확보** — config-앙상블 신규성 주장(§4-3)은 그 후에만 원고 기재.
- [ ] **σ/Ea 규율 유지**: MSD 2–50 ps 고정, 600/800/1000 K 3점(400/500 K 제외 판정), NE(Haven=1)
      비율만·절대값 비인용, Ea 오차막대 600 K 3-시드. 조성 간 비교 시 Haven 비 변화 가능성 1줄 명시
      (ishikawa2025의 field-driven vs NE ~2 orders 사례).
- [ ] **셀 크기 체크 1회**: MLIP-MD이므로 AIMD급 셀에 머물 이유가 없다 — 문헌 수렴 기준
      (⚠ Lee 5×5×5·6500원자, ⚠ Jang 4×4×4·3328원자)을 참고해 최소 한 번 셀-크기 민감도를 기록.
- [ ] **문헌 수치 격리**: 이 문서의 모든 값은 소환값 — 우리 db 절대값과 같은 표·같은 그림에 방법
      명시 없이 섞지 않는다. ⚠ 항목은 원문 PDF 확보 전 인용 금지.

---

*관련 문서: [comparison_vs_ours.md](../comparison_vs_ours.md) · [our_dft_baseline.md](../our_dft_baseline.md) ·
digest 표준 필드 [_TEMPLATE.md](../papers/_TEMPLATE.md) §4(무질서 처리)*
