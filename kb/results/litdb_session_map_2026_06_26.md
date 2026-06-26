# litdb 세션 맵 (2026-06-26) — deck/논문용 1장 인덱스

이번 세션에 정리한 문헌 전체 + **우리 작업과의 연결 1줄** + 태그. URL은 모두 branch `claude/friendly-meitner-lldvar`.
base: `https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/claude/friendly-meitner-lldvar/litdb/papers/`

---

## A. 우리 그룹 [우리 그룹] — cathode-interface 3부작 + 동반실험 2
| 논문 | 축 | 우리 작업 연결 (1줄) | slug |
|---|---|---|---|
| **Kang 2026** (intertwined review) | 지붕 | electrochemo-mechanical coupling = cascade(기계)+SEI+산화의 통합 프레임 | `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` |
| **Kang 2025** (기생반응 이점) | 양극 B③ | "기생반응=passivation" = 우리 산화 ESW 분해산물·Nd cathode passivation과 같은 물리 | `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb` |
| **Cha 2024** (dual-compatible halide) | 양극 | dual-compatibility, **σ≠성능**(LIC σ1등/수명꼴찌); interface_reactivity 적용대상(Zr hull 추가 필요) | `cha2024_dualcompatible_halide_ncm_lpscl_interface` |
| **Kim 2026** (ICCF 공동충전재) | σ/SEI | 공동충전 σ 1.44→2.23 mS/cm; FEC→LiF SEI | `kim2026_iccf_molten_salt_sei_lpscl_sheet` |
| **Kim 2025** (도전재 SE-코팅) | σ_e | 도전재 형상(VGCF 1D vs Super P 0D)→σ_e; "lever=형상" | `kim2025_conductive_agent_se_coating_cathode` |

## B. 외부 — Cl/halide·계면 (우리 comp1/modelc Cl-rich 4축의 외부 대화)
| 논문 | 축 | 우리 작업 연결 (1줄) | slug |
|---|---|---|---|
| **Zuo 2022** (Cl→양극계면, Janek/Nazar) | B③ 양극 cycling | gas diversion; 우리 grand-potential 분해식 + XPS anchor(133.3/168.0/198.6/160.2) 3-도구 검증 | `zuo2022_chlorination_cathode_interface` |
| **Liu 2022** (Cl→음극·결정화, Zhejiang) | A·E 음극 kinetics | **Fig 2e–g = inter-cage 멘탈모델 시각증거**; 계면 RDF 시간추적 = 우리 grand-potential의 kinetic 짝 | `liu2022_cl_crystallization_interface_argyrodite` |
| **Li 2025** (CuBr₂ dual-doping, USTB) | A·D·G | **σ_e 실측 anchor**(우리 약점 보강); LiBr gap 5.07(우리 db에 없던 값); Cu–S>P–S = O-도핑 bonding-lock 원리 | `li2025_cubr2_dualdoping_argyrodite` |
| **Sundar 2025** (oxide-coating 스크린, Argonne) | D·G | InterfaceReactions = 우리 interface_reactivity와 동일도구; 분해산물-σ 철학; Li₂S<LiCl gap 재확인. ⚠코팅≠도핑 | `sundar2025_oxide_coating_screening_lpscl` |
| *(기존)* GilGonzalez 2022 | B② 기계구속 | Cl-rich K_eff=20서 창 확장 (Zuo B③와 다른 축) | `gilgonzalez2022_synergistic_cl_constricted_esw` |
| *(기존)* Lu 2025 | 음극 | Cl-rich 음극 LiCl passivation (Liu와 같은 진영) | `lu2025_tailoring_cl_rich_anode_licl` |
| **★ Banik 2022** (치환↔산화안정성, **Mo**+Zeier) | B① intrinsic | **우리 방법 본가(Mo=grand-potential 원저자)가 우리 결론 독립 발표**: 치환은 onset 못 옮김(S 3p가 pin)=comp1=modelc 2.14V; COHP가 우리 ICOHP/ELF 확증 | `banik2022_substitutions_oxidative_stability_argyrodite` |
| **Li 2025**(CuBr₂→Br) / **Rao 2025**(I) | A·D 할라이드 trend | Cl/Br/I: σ는 종류보다 **총량·비율·채널부피** 지배(=comp1→modelc trend). I→**4a**(site ΔE 0.35>Br); I가 E_hull↓·계면 ΔE_D↓(Br엔 없는 분석). **산화 onset엔 영향X**(Banik S-pin) | `rao2025_iodide_argyrodite` |

## C. 외부 — 이론/방법 백본
| 논문 | 유형 | 우리 작업 연결 (1줄) | slug |
|---|---|---|---|
| **Ishikawa 2025** (site-percolation) | theory | blocking=Li망 site-dilution(pc≈0.2); **Nd=connectivity-blocking**. ⚠완만감소지 pc붕괴 아님 | `ishikawa2025_site_percolation_cooperative_ion_conduction` |
| **Dyre 2004** (hopping models) | theory | σ/Ea 어휘; inter-cage hop=percolation 병목=dc Ea; Nd σ-drop=prefactor-blocking | `dyre2004_hopping_models_ion_conduction_noncrystals` |
| **He 2019** (DFT for battery) | methods-review | 우리 방법=표준 battery-DFT 인용처; ⚠grand-potential은 He19 아님(Mo2012) | `he2019_dft_for_battery_materials_review` |
| **Whitten 2023** (UPS best-practice) | methods | UPS=VBM/IE=산화안정성 valence-side probe (상한, 진짜 onset은 grand-potential) | `whitten2023_ups_practical_best_practices` |
| **Choi 2025** (MLIP 계면접착) | methods | W_ad **SMD+PMF** = 우리 rigid-분리 100–1000× 과대 처방; MLIP B0 DFT 5%내 앵커 | `choi2025_mlip_cu_taxn_interfacial_adhesion` |
| **★ Torii 2025** (LPSCl 기계물성·이방성, Osaka) | C 기계 | **외부 full-DFT가 vacancy paradox 판정**: relaxed-ion(E27.4/G10.0)=우리 relaxed(22/8), clamped(52/20)의 2× 아래 → **relaxed가 옳다 외부확증**. 전단취성 Cl→Li₄Cl 원자기구 | `torii2025_lpscl_mechanical_anisotropy_dft` |

## D. external / off-topic (analogy only)
| 논문 | 우리 작업 연결 | slug |
|---|---|---|
| **Liu 2013** (메탄-수화물 cage) | ⚠analogy만: cage 창크기→inter-cage 통과 = 멘탈모델 (수치전이 0) | `liu2013_cage_methane_adsorption_hydrate_nucleation` |

---

## ★ 교차-논문 synthesis (deck 슬라이드 후보)
1. **cathode-interface 3레버** (우리 그룹): Cha=할라이드코팅(차단) / Kang25=SE코팅(기생반응 균일화) / cascade=SE도핑(절연CEI). 지붕 = Kang26 리뷰.
2. **"lever = interphase/형상, not bulk σ"**: Cha(σ역상관)·KimICCF·KimCA·Li2025(σ_e실측) — 4중 증거.
3. **이론 백본 (Percolation+Hopping)**: dopant blocking 2모드 = (i) Ea-blocking vs (ii) connectivity-blocking. **우리 Nd σ-drop = (ii)**, 양 논문 교차확증. 단 완만감소(망 유지), pc붕괴 아님.
4. **inter-cage 서사 3단**: 이론(Ishikawa/Dyre) + 시각증거(Liu2022 Fig2e-g) + analogy(Liu2013 cage).
5. **Cl-rich 산화 4축 정명**: B①intrinsic onset(무승부, S²⁻-limited 2.14V) · B②기계구속(GG) · B③양극cycling(Zuo) · 음극(Liu/Lu). 섞으면 틀림.
6. **방법 엄밀성**: 우리=표준 battery-DFT(He19) + ESW는 grand-potential로 *상회*(band-edge 2–3×과대) + W_ad는 SMD개선(Choi) + UPS로 VBM실측.
7. **★ S-pin 산화 명제 (Banik=외부 정답지)**: "치환은 S-limited 산화 onset 못 옮긴다"가 이제 **Zeier 실험 + Mo 계산**(우리 grand-potential 본가)의 검증을 가짐. 우리 차별화 = Banik이 닫은 문 *위*: (i) Cl-rich 4축, (ii) onset 옮기는 예외도판트(B₂O₃ 2.317·Sc/Cr/In/Ga₂O₃ 2.356, ≤0.2V), (iii) Nd passivation. + "치환 안 되니 코팅 필요"가 우리그룹 cathode-interface 라인을 외부 정당화.
8. **★ vacancy paradox 외부 판정 (Torii)**: 독립 full-DFT(PBE-D3 relaxed-ion)가 E=27.4/G=10.0 → 우리 **relaxed-ion(22/8)에 산다, clamped(52/20)의 2× 아래** = "clamped는 frozen-framework baseline, relaxed가 물리적"이 외부확증. B0는 동물질(격자 10.04≈10.055)·절대값은 D3+정의차(우리 PBE B_VRH 25.51≈EOS 26.23). 전단취성(ε0.7%, Cl→Li₄Cl)이 우리 낮은 C₄₄/G의 *원자기구*(Kang 리뷰 chemo-mechanical과 연결). deck "paradox" 슬라이드 외부 인용처.

## ✅ 배치 완료 (2026-06-26)
이번 세션 총 **18편** digest (우리그룹 5 · 외부 Cl/계면·산화 8 · 이론/방법 5 — 일부 중복 카운트 / analogy 1). #18 Banik·#19 Rao 포함 전부 커밋·푸시됨. 동반 figure: `docs/figures/cascade/cascade_oxidation_vs_banik.png` (Banik S-pin vs 우리 예외 6 M³⁺ 산화물).

> **할라이드 한 줄(Cl/Br/I)**: σ는 *할라이드 종류*보다 **총량·비율·무질서·채널부피**가 지배(Rao·우리 trend 일치). 산화 onset은 셋 다 **S²⁻가 pin**(Banik) — 할라이드는 전도·계면·상안정 레버이지 산화창 레버 아님.
