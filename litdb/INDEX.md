# 📚 LITDB — DEM+MPM ASSB 압밀·전달 문헌 인덱스

> 갱신: 2026-06-23. 각 논문 상세는 `papers/<slug>.md` (digest), 우리 대비는 `comparison_vs_ours.md`,
> 기준값은 `our_dem_baseline.md`. 수치 CSV는 `docs/data/<slug>_*.csv`.

Status 범례: ✅ digest 완료 · ⬜ PDF만(미digest) · 📄 메타만

## DEM/MPM 압밀 · 전달 (composite ASSB)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Lee 2025** | Nat. Commun. 16, 4200 | **LPSCl + NCM811/82 + VGCF + PTFE** (= 우리 소재·도전제 전부) | **실험**(no sim) co-rolling 박막; ★PTFE 0.5/2/5 wt%→σ_e 34/4.5/0.011·σ_i 0.069/0.024/0.007 mS/cm; ★binder-VGCF fibril망(=우리 CBD); ★PC-NCM 깨짐/SC-NCM 무손상; 2 MPa>80% 500cyc; 310 Wh/kg | exp | ✅ | `lee2025_corolling_dryprocess_lpscl_ptfe` |
| **Bazzoun 2026** | J. Power Sources 661, 238682 | **LPSCl + NMC811** | DEM+FEM+RNM σ_eff,ion; 실험 0.137/0.101/0.065 mS/cm @f_CAM 70/75/80; RNM=Holm/Kirchhoff; E_SE=22.1 | DEM+FEM+RNM | ✅ | `bazzoun2026_dem_fem_rnm_ionic` |
| **Varkey 2026** | Adv. Powder Tech. 37, 105338 | halide Li₃YBrCl₆ + NMC811 | multi-contact 탄소성 DEM; separator floor 21% / cathode 37% @350MPa; E_SE=10.58; CONTACT-소성만(구) | DEM | ✅ | `varkey2026_multicontact_elastoplastic_dem` |
| **So 2021** | J. Power Sources 508, 230344 | LPS(Li₂S–P₂S₅) + Si음극 | 3D DEM(소성 cold-press, **H-cap real E=24**); rel.density 0.30→**0.98**@600MPa, φ_SE^crit=0.13, AM-AM 응력 5.9 GPa | DEM | ✅ | `so2021_dem_mold_pressure_assb_coldpress` |
| **Martin & Bouvard 2003** | Acta Mater. 51 | soft+hard 구 혼합 | DEM 냉간압밀; 2-메커니즘(force-network K_h + excluded-volume 과변형), Storåkers 소성접촉, 거시응력 E₂/E₁=10→100서 <3% | DEM | ✅ | `martinbouvard2003_dem_composite_cold_compaction` |
| **Bouvard 2000** | Powder Technol. 111, 231 | 경(세라믹)+연(금속) 혼합 | 압밀 2체제(재배열/연-변형) + percolation 임계 vs 크기비(0.32@r=1→0.18@r=2); SE+AM dip 원형 | exp+theory | ✅ | `bouvard2000_hard_soft_powder_densification` |

## 패킹 기하 (geometric packing — Furnas dip 근거)

| 논문 (제1저자 년) | 저널 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|
| **McGeary 1961** | J. Am. Ceram. Soc. 44(10) | 강체 구(금속 shot) bimodal/multimodal 충전 62.5→86→90→95.1%, 임계비 **7:1**(0.154·d_c); **소성변형 없음** = Furnas-dip 기하 원전 | exp | ✅ | `mcgeary1961_bimodal_sphere_packing` |

## 실험 1차 앵커 (EIS-TLM / 측정값)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **★ Minnmann 2021 JES** | J. Electrochem. Soc. 168, 040537 | **NCM-622 + LPSCl** (= 우리 소재계) | ★★ **우리 porosity/σ_ion/τ 앵커의 진짜 출처.** EIS-TLM 1차 측정: **복합 porosity 14 % (13–17 %, dry-mix 380 MPa)** · **σ_ion,eff 0.17 mS/cm @ 42 vol% NCM** · **τ_ion 2.07 (=√(τ²=4.3))** · σ_el,eff 0.56 (τ_el²=7.4) · LPSCl bulk 1.6 mS/cm · NCM 전자 10 mS/cm. CAM vol% 25–61 스윕(CAM↑→σ_ion↓/τ↑), 42 vol% 154 mAh/g 최적; carbon-free 고-CAM; fine SE→σ_ion,eff↑(packing/τ). | exp (EIS-TLM+cycling) | ✅(docs) | `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md` |

## 설계 Perspective (정성 — 수치 앵커 아님)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Minnmann 2022** | Adv. Energy Mater. 12, 2201425 | NCM/LFP/LMO/conv + sulfide/halide SE (우리 LPSCl+NCM 설계공간) | ★ **설계 Perspective(1차데이터 아님)**; porosity/σ **측정값 0개**(전부 정성); 설계임계만: CAM 60–70 vol% 최적·3–5 µm CAM·작은 SE+큰 CAM/SE비·tailored PSD·SE 고tortuosity(C(τ) 정당화)·§5.4 결합 mech-echem-thermal 모델 호명. **★ 우리 "Minnmann porosity 14 %/13–17 %/τ 2.07" 앵커는 이 논문 아님 → Minnmann 2021 JES 040537 / Sakuda 2013** (digest §0) | review | ✅(docs) | `docs/lit_minnmann2022_designing_cathodes_solidstate.md` |

> ★ **PROVENANCE 확정 (2026-06-26, Minnmann 2021 PDF 직접 확인):** porosity 13–17 %·σ_ion_eff 0.17·τ_ion 2.07 = **Minnmann *2021 JES* 040537**(NCM622+LPSCl, **압밀 380 MPa**, EIS-TLM **측정 40 MPa**, **42 vol% NCM** 기준). 세 앵커 전부 PDF 본문서 stated 확인 (τ_ion 2.07 = √(tortuosity factor τ²=4.3) — τ vs τ² 구분 필수). 밀도 87 %@300 MPa = **Sakuda 2013**; pure-SE 10 % = 우리 MPM 보정 수렴값(이 논문은 *복합* porosity만 줌, pure-SE 아님). 2022 AEM Perspective는 **정량 데이터 없음.** + `refs.bib @Minnmann2021`이 엉뚱한 040502/abf3a3을 가리킴 → **040537/abf8d7**로 정정 권고. 저자 = Philip Minnmann, **Lars Quillman**, Simon Burkhardt, Felix H. Richter, Jürgen Janek.

## 통합된 기존 노트 (→ papers/ digest로 흡수)
- `docs/lit_varkey2026_multicontact_dem.md` (한국어 노트) → `papers/varkey2026_*` ✅ + `docs/data/{densification_porosity_db,varkey2026_ionic_vs_pressure}.csv`
- `docs/lit_bazzoun2026_dem_fem_rnm.md` (한국어 노트) → `papers/bazzoun2026_*` ✅ + `docs/data/bazzoun2026_sigma_ionic.csv`
- **Lee 2025** (실험 앵커) → `papers/lee2025_*` ✅ + `docs/data/lee2025_transport_anchors.csv` (PTFE% σ 페널티 + 조성별 σ + bulk 앵커); CBD 검증 → `docs/cbd_morphology_roadmap.md`
- `docs/literature_coverage/` json DB: contact_mechanics_db, coverage_db, packing_regime_db (수치 참조용 유지)

## 주제별 종합 문서
- `elasto_plastic_feasibility.md` — elasto-plastic 접촉모델 실행가능성·적용·우리 모델 대비 장단점
  (Varkey/So/M&B 종합; ★ So 2021 H-cap = 18× 연화 대체 경로).

## 현황
papers/ digest 7편 ✅ (**Lee2025**(실험 앵커, =우리 소재 전부) · Bazzoun · Varkey · So2021 · Martin-Bouvard2003 · Bouvard2000 · McGeary1961)
+ docs/ digest: **Minnmann 2021 JES**(★ porosity/σ_ion/τ 앵커 진짜 출처, EIS-TLM) · Minnmann 2022(설계 Perspective).
새 PDF 업로드 후 "논문 에이전트 실행해줘"로 추가.
