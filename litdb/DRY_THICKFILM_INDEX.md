# 📑 건식 후막 Bimodal 복합양극 — 관련 문헌 큐레이션 (이 브랜치 작업용)

> stoic-knuth에서 이식된 문헌 중 **이 실험 프로젝트(건식·후막·바이모달·단결정/다결정·구배·도전재·바인더·digital-twin)**에
> 직결되는 것만 추림. 상세 노트 = `../docs/lit_<slug>.md`. 정식 digest로 승격 시 `papers/`로 옮기고 `INDEX.md`에 행 추가.
> ⭐ = 우리 작업과 직결도 최상. 신규 PDF는 **"논문 에이전트 실행해줘"** 로 추가.

## A. Bimodal / 단결정-다결정 packing (★ porosity dip 핵심)
| 논문 | 한 줄 | 우리 연결 | 노트 |
|---|---|---|---|
| ⭐⭐⭐ **Oh 2026** (ACS Energy Lett. 11, 2103) | 큰 다결정 + 작은 단결정 CAM bimodal 복합양극 → packing·porosity·tortuosity 최적화 | **우리와 거의 동일한 소재계·조건.** 우리 P:S dip(7:3 최소 19.7%)의 직접 문헌 검증 | `lit_oh2026_bimodal_composite_cathode` |
| **Trevisanello 2021** (AEM 11, 2003400) | 다결정 vs 단결정 NCM: 입자균열·활성표면적·Li 확산 | No.1/No.2(단결정) vs Poly(다결정) 거동·열화 근거 | `lit_trevisanello2021_sc_pc_ncm_cracking_diffusion` |
| **McGeary 1961 / Bouvard 2000** (papers/) | 강체 구 bimodal 충전·Furnas dip 원전 | DEM dip 이론 기반 | `papers/mcgeary1961_*`, `papers/bouvard2000_*` |

## B. 건식(dry process) 후막 전극 + PTFE 섬유화
| 논문 | 한 줄 | 우리 연결 | 노트 |
|---|---|---|---|
| ⭐⭐⭐ **Lee 2025** (Nat. Commun. 16, 4200) | LPSCl+NCM+VGCF+PTFE co-rolling 건식 박막; PTFE%↑→σ 페널티 | **우리 소재·도전제 전부 동일.** PTFE σ 경향(우리 0.062/0.057/0.019) 검증 | `papers/lee2025_corolling_dryprocess_lpscl_ptfe` |
| ⭐ **Koo 2026** (Joule 10, 102392) | 연속 SWCNT sheath → 두꺼운 dry 전극 초고에너지밀도+급속충전 | 후막 건식 + 도전재망 | `lit_koo2026_swcnt_sheath_thick_electrode` |
| **Koo 2025** (ESM 78, 104270) | MWCNT 감싼 단결정 SC-NCA dry 양극 (99.6 wt%, 4.0 g/cm³) | 단결정 dry 고밀도 양극 | `lit_koo2025_cnt_wrapped_sc_nca_dry_cathode` |
| **Nam 2026** (Mater. Horiz. REVIEW 13, 3149) | 건식전극(DPE) 미세구조 엔지니어링 리뷰 | 프로젝트 framework/positioning | `lit_nam2026_dpe_microstructure_review` |
| **Lim 2025** (Small 21, 2410485) | Virtual calendering: 3D재구성→가상 캘린더링·설계최적화 | 우리 롤프레스/압축 방법론 형제 | `lit_lim2025_virtual_calendering_framework` |

## C. 다층 / 구배 구조 + Primer 집전체 (★ 2차년도 설계전략)
| 논문 | 한 줄 | 우리 연결 | 노트 |
|---|---|---|---|
| ⭐ **Yoo 2026** (ESM 105331) | Porosity-구배 건식 전극 + 변형성 Primer Layer | **우리 다층/구배 + 프라이머 코팅 집전체 직결** | `lit_yoo2026_porosity_gradient_dry_electrode` |
| ⭐ **Bak 2024** (CEJ 483, 148913) | 바인더 z-분포 제어 다층 모델전극 + digital-twin | 우리 상/하부 구배 설계 | `lit_bak2024_binder_distribution_multilayer` |

## D. 도전재 / 바인더 (CBD)
| 논문 | 한 줄 | 우리 연결 | 노트 |
|---|---|---|---|
| ⭐ **Kim 2025** (Battery Energy 4, e70044) | SE-coating CAM 도전재 Super P(0D) vs VGCF(1D) → LPSCl ASSB 좌우 | 우리 VGCF 선택 근거 | `lit_kim2025_conductive_agent_se_coating_assb` |
| **Hong 2026** (ESM 86, 104930) | 황화물 복합양극 열화 digital-twin: Dry(PTFE) vs Wet(NBR) | 우리 소재계 PTFE 건식 | `lit_hong2026_sulfide_cathode_binder_digitaltwin` |
| **Hong 2026** (ESM 105321) | CBD 점탄성 → 단결정 cathode spring-back 억제 | 단결정+CBD 기계거동 | `lit_hong2026_cbd_viscoelasticity_springback` |
| **Park 2026** (AFM 36, e16017) | Thiol-ene SBR 바인더 개질, 저압 ASSB | 바인더 화학 | `lit_park2026_thiolene_sbr_binder_assb` |

## E. 모델링 / Digital-Twin / Electrochemo-mechanical (P2D 연계)
| 논문 | 한 줄 | 노트 |
|---|---|---|
| **Song 2025** (EES 18, 3129) | 미세전극 electrochemo-mechanical digital-twin, 셀전압 >98% | `lit_song2025_electrochemo_mechanical_microelectrode_ees` |
| **Park 2020** (AEM 10, 2001563) | Digital-twin ASSB 시조 | `lit_park2020_digitaltwin_assb_foundational` |
| **Kim 2024** (ACS Energy Lett.) / **Choi 2024** (E.Chem) | Digital-twin positioning 리뷰 | `lit_kim2024_*`, `lit_choi2024_*` |
| **Lee 2023** (Battery Energy 2) | SIC-SPE vs LPSCl 복합양극 구조·전기화학 | `lit_lee2023_sicspe_digitaltwin_assb` |

## F. 전달/압밀 시뮬 앵커 (DEM/MPM 브랜치 공유)
Bazzoun2026(LPSCl+NMC811 σ_ion DEM+FEM+RNM) · Varkey2026 · So2021 · Minnmann2021(EIS-TLM 앵커) ·
Doux2020(작동압) · Cronau2021. → `papers/`, `../docs/lit_minnmann2021_*`, `../docs/lit_doux2020_*` 등.

## 5/12 미팅 다층설계 인용문헌 (digest 후보 — 아직 litdb에 없을 수 있음)
- Batteries & Supercaps 2024, 7, e202300522 · ACS Energy Lett. 2025, 10, 1664–1670
- Nat. Commun. 2025, 16, 7667 (SE bimodal) · Adv. Mater. 2024, 36, 2309306
