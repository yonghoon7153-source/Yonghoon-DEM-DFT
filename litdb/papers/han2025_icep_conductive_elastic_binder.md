# 이온전도성 탄성 고분자(ICEP) 바인더로 초고로딩 NCM811 전극 — Han (Adv. Mater. 2025)

> slug `han2025_icep_conductive_elastic_binder` · DOI `10.1002/adma.202506266` · type `exp (+DFT 흡착)` ·
> PDF `docs/literature_coverage/pdfs/Han_2025_AdvMater_ICEP_IonicConductiveElasticBinder_UltrahighLoading.pdf` ·
> digested `2026-07-08` · status ✅ · 수치 CSV `docs/data/han2025_icep_binder_anchors.csv`
>
> ⚠ **시스템 최상위 주의: 액체 전해질 LIB(습식 슬러리 캐스팅, NCM811+카보네이트+Li-metal) — ASSB 아님, LPSCl 없음,
> 압밀/porosity 데이터 없음.** 우리에겐 **바인더 물성 앵커**(SDCP 전도성 바인더 모델링 / A3 `--coh` / W2 binder-σ 클래스 /
> coat-vs-fibril 시딩)로 소비하는 논문. 절대값 전이는 각 행의 caveat 준수.

## 1. 한 줄 요약
PVDF(비극성 vdW-only, 취성, 이온 절연)를 **삼중블록 공중합체 ICEP** [P(AN-co-AMPS)]₂-b-PEO — **탄성**(연신 283 %) +
**수소결합 접착**(DFT −1.8~−2.2 eV, SAICAS 4~7×) + **이온전도**(0.135 mS/cm, PVDF의 2.1×) 3기능 동시 —
로 바꾸면, 습식 후막의 3대 병목(건조 균열·박리 / 불균일 binder 분포 / 두께방향 이온수송)이 동시에 풀려
**62.4 mg/cm² (12.5 mAh/cm²) 초고로딩**이 크랙 없이 성립하고 94.6 %@60 cyc 유지 + 파우치 377.6 Wh/kg·1016.8 Wh/L를 달성한다.
바인더가 NCM811 위 **~7 nm 균일 코팅층**(coat형)을 이뤄 CEI 안정화·TM 용출 킬레이션·rock-salt 상전이 억제(3.1 vs 11.3 nm)까지 담당.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| Dong-Yeob Han, Masud, Yeongseok Kim, Saehyun Kim, Dong Gyu Lee, Junhyeok No, Hee Cheul Choi, Tae Kyung Lee, **Youn Soo Kim\*, Soojin Park\*** (POSTECH 화학/신소재 + 동국대 + 경상국립대) | Adv. Mater. 2025, 37, 2506266 (OA, 2025-07-07 online) | 10.1002/adma.202506266 | **NCM811** LiNi₀.₈Co₀.₁Mn₀.₁O₂ + 액체 카보네이트 전해질(LiPF₆) + Li-metal 100 µm; binder = **ICEP vs PVDF** | 실험 (합성 RAFT + 기계/전기화학/구조 분석) + DFT(흡착에너지만) — **시뮬레이션 없음** |

**ICEP 설계**: [P(AN-co-AMPS)]₂-b-PEO₄₆ 삼중블록, RAFT 중합(PEO₄₆-MCTA 이관능 macro-CTA), Mw ≈ **100 kDa** (GPC).
기능 분담 — **AN**(아크릴로니트릴): 강성/기계강도 + C≡N 극성 친화; **AMPS**(2-acrylamido-2-methylpropane sulfonic acid):
−SO₃H 이온전도 + 수소결합; **PEO 중간블록**: 유연성 + 에터 O 이온수송. [AN]/[AMPS] 비 x/y ≈ 5/8/19 → ICEP-5/-8/-19
3종 합성, **ICEP-8이 챔피언**(중간비 = 강성·이온성·탄성 균형). PS-b-PI-b-PS 열가소 엘라스토머 개념 차용 + 이온 관능기.

## 3. 핵심 물성 (수치) — ★ 바인더 물성 앵커 (사용자 우선순위 1)

### 3a. 바인더 필름 (free-standing / 필름 레벨)
| 물성 | ICEP-8 | PVDF | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|---|
| **σ_ionic (필름)** | **1.35×10⁻⁴ S/cm = 0.135 mS/cm** | 0.65×10⁻⁴ = 0.065 mS/cm | RT, SS\|film\|SS EIS | stated | ⚠ 필름 전처리(전해질 함침 여부) 본문 미기재 — **PVDF 0.065는 건식으로 불가능한 값 → 전해질-swollen 필름으로 추정**(SI 확인 필요). LPSCl 1.6 대비 **~1/12** |
| **E (나노압입, 필름)** | **6.03 GPa** | 3.73 GPa | 0.1 mN, 깊이 96.5 vs 120.0 nm | stated | 표면/유리질 hard-block 지배 + Oliver-Pharr 고분자 과대 경향 — 벌크 인장과 층위 다름(§10) |
| 경도 H (필름) | 0.42 GPa | 0.34 GPa | 동일 | stated | |
| **연신율 (인장)** | **283 %** | 31.8 % | free-standing 필름 S-S | stated | ICEP-5: 212 % / ICEP-19: 167 % |
| **toughness** | 601.2 "J m⁻³" | 151.8 | 동일 | stated ⚠단위 | ⚠ stated 단위 J/m³는 plateau 2.7 MPa×2.83과 모순(면적 ~7 **M**J/m³) → **MJ/m³ 오기 개연**, 비(4.0×)만 신뢰 |
| 인장 flow stress | **≈2.7 MPa plateau** (PVDF: ≈9 MPa 피크 후 조기파단) | | Fig 1a | **digitized(추세)** | ★ MPM binder σ_y 스케일 후보. 초기 기울기 → E_tensile ~10–25 MPa(digitized, 엘라스토머 스케일) |
| Tg (DSC) | PEO −56 ℃ / P(AN-co-AMPS) +85.2 ℃, PEO 결정성 완전 억제 | (—) | | stated | 2-Tg = 미세상분리 물리 가교; ICEP-5/-19는 PEO Tg −18/−25 ℃ + 부분 결정성 |
| Mn²⁺ 킬레이션 | 126 ppm | 27 ppm | 0.01 M Mn(ClO₄)₂ 6 h, ICP-MS | stated | 극성기(아마이드·설폰산) TM 포획 |
| Li⁺ 배위 | ⁷Li NMR 0.00→+0.05 ppm; FT-IR C−S 626→629, O=S=O 1215/1037→1220/1042 cm⁻¹ | | 전해질 접촉 후 | stated | Li⁺–SO₃H/에터O 배위 = 전도 메커니즘 근거 |

### 3b. DFT 흡착에너지 (NCM811 (001) 표면, 분자 세그먼트)
| 세그먼트 | E_bind | 비고 |
|---|---|---|
| ICEP_AMPS(-H) | **−2.243 eV** | 설폰산–표면 O 수소결합 |
| ICEP_AMPS | −1.819 eV | |
| PVDF | −0.703 eV | vdW-only |
| ICEP_AN | −0.162 eV | AN 자체는 약함 — 접착은 AMPS 몫 |

### 3c. 전극(캐소드) 레벨 — ★ 접착/역학 앵커
| 물성 | ICEP-8 캐소드 | PVDF 캐소드 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|---|
| **SAICAS cohesion(절삭)** | **0.29 N** (≈290 N/m†) | 0.07 N (≈70 N/m†) | blade 폭 1 mm, shear 45°/rake 20°/clearance 10° | stated (†N/m 환산=우리 계산 F/폭) | 전극 내부 결합력(슬라이싱 저항) |
| **SAICAS adhesion(박리)** | **0.27 N** (≈270 N/m†) | 0.04 N (≈40 N/m†) | 동일, 집전체 계면 | stated (†환산 우리) | **6.8×**; N/m=J/m² 차원의 *apparent* peel(소성 소산 포함) — Bucci 고유 G_c(≥4 J/m²)와 직접 비교 금지 |
| **E (전극 나노압입)** | **1.57 GPa** | 0.11 GPa | 2.0 mN, 깊이 936.1 vs 3345.2 nm | stated | ★ 우리 MPM champion E_eff 1.53 GPa와 수치 인접(§7-6, 물리 다름 주의) |
| H (전극) | 0.15 GPa | 0.014 GPa | 동일 | stated | >10× |
| 탄성 회복률 | 48.0 % | 35.8 % | 동일 | stated | 탄성 binder → 소성변형 최소 |
| **binder 분포/형상** | **NCM811 위 ~7 nm 균일 코팅층 (coat형)** | 불균일 산발 응집(aggregate형) | TEM | stated | ★ 시딩 형상 근거(§8-③) |
| 전극 두께 | ≈230 µm (ICEP) / ≈190 µm (PVDF) | | 단면 SEM(ion-mill) | stated | ⚠ 어느 로딩과 짝인지 미기재 → **밀도/porosity 도출 불가** |
| 표면 균일도 | PVDF 두께편차 ≈7.3 µm·응집; ICEP 평탄(confocal 1×1 mm) | | | stated | 건조 segregation 억제 증거(간접) |
| porosity / 캘린더링 / 조성비 / 용매 | **n/a — 본문 없음 (SI Experimental)** | | | | 1 wt% binder 저감 전극(19.5/37.3/60.9 mg/cm²)도 정상 작동 → 표준 조성은 binder >1 wt% |

### 3d. 로딩·전기화학 (액체 LIB — 추세 컨텍스트용)
| 항목 | 값 | 비고 |
|---|---|---|
| 로딩 시리즈 | **18.8 (3.4 mAh/cm²) / 36.9 (6.6) / 45.3 (8.8) / 52.3 (10.5) / 62.4 mg/cm² (12.5 mAh/cm²)**, 2.7–4.2 V | ICEP 전 구간 크랙-프리(SEM S23); PVDF는 **31.7 mg/cm² 이후 에너지밀도 하락, 40.7 mg/cm²에서 균열+박리 실패** |
| 18.8 mg/cm² 반쪽셀 | ICEP 193.8 mAh/g·ICE 90.8 %·첫 과전압 3.77 V vs PVDF 181.9·86.2 %·3.89 V | |
| 0.5C 장기 | ICEP **85.5 %@170 cyc** vs PVDF 28.9 %@80 (CE 99.8 vs 99.2 %) | |
| 2C/2C | ICEP 153 mAh/g·90.0 %@120 vs PVDF ~99·39.4 %@40 | |
| GITT (30 cyc 후) | R_internal **31.0 vs 57.2 Ω**; D_Li⁺ **0.42 vs 0.18 ×10⁻⁷ cm²/s** (>2×) | binder 이온전도의 셀-레벨 발현 |
| 고로딩 풀셀 (Li 100 µm≈20 mAh/cm², N/P 1.6–5.9, 0.1C) | 52.3→**96.3 %**, 62.4→**94.6 %**@60 cyc; PVDF 37.3→54.7 % | |
| 코인 중량 에너지밀도 | **424.4 Wh/kg @62.4 mg/cm²** (패키지 제외, plateau) | |
| 파우치 (2-stack, 62.5 mg/cm²·12.7 mAh/cm², N/P 1.57, E/C 2.5 g/Ah) | 304 mAh, **377.6 Wh/kg_cell·1016.8 Wh/L_cell**(패키징 포함), 96.7 %@40 cyc | >40 cyc 급락 = **Li/lean-전해질 열화**(재조립 검증으로 캐소드 무죄 입증); 10/20/30-stack 추산 451.3/462.3/466.1 Wh/kg |
| 셀 중량 구성 | cathode 47.2 / electrolyte 25.0 / package 18.6 / Li 4.6 / CC 3.5 / separator 1.1 wt% | |

### 3e. 열화-구조 (사이클 후)
| 항목 | ICEP-8 | PVDF | 방법 |
|---|---|---|---|
| 입자 균열 | **무손상** | 심한 분쇄(pulverization)+미세균열 | 싱크로트론 nano-CT (PAL 7C, FOV 76 µm, 픽셀 44 nm) + TXM + 단면 SEM |
| rock-salt 상전이층 | **≈3.1 nm** | ≈11.3 nm | STEM-FFT/EELS (O-K ΔE, Ni L₃/L₂) |
| 내부 CEI 두께 | 스퍼터 108 s | 283 s | TOF-SIMS 깊이 프로파일 (LiF₂⁻·CP⁻·PO₂⁻·MnF₂⁻·NiF₂⁻ 전부 PVDF↑) |
| Li 음극 TM 침적 | Ni 73.9 / Co 7.1 / Mn 9.2 ppm | 대폭 높음 (Fig 4a, Ni ~500 급, digitized) | ICP-MS |
| 두께방향 redox 균일성 | E_g/A₁g 충전 후 top 0.98 / **bottom 0.99** (균일) | top 0.99 / bottom 0.84 (**바닥 미탈리튬** — pristine 0.83과 동일) | confocal Raman(A₁g 530·E_g 440 cm⁻¹), top/bottom |
| DRT/GEIS | R_SEI·R_ct 미미, 전 완화시간 짧음 | P1(R_SEI) 피크 분열 = 불균일 SEI 다중 저항 | ex-situ DRT(P1–P4) + in-situ GEIS-DRT 맵 |

## 4. 시뮬레이션 방법 ★ (이 논문은 실험 — 해당 없음 / DFT만)
- **DEM/MPM/RNM/연속체 압밀·수송 시뮬레이션 없음.** 유일한 계산 = **DFT 흡착에너지**(ICEP 관능기 세그먼트 vs PVDF를
  NCM811 (001) 표면에 얹은 분자 흡착; 코드/함수 등 세부 SI(Fig S12) — 본문 n/a). 분자 스케일 → 연속체 접착(--coh)으로
  직접 환산 불가, *서열 근거*로만.
- **입자 처리** ★: 해당 없음 (실험). NCM811은 다결정 2차입자(TEM/nano-CT에서 입계균열 관찰 = 우리 AM_P 클래스).
- **합성**: RAFT (bis(dodecylsulfanylthiocarbonyl)disulfide → PEO₄₆-MCTA → AN+AMPS DMSO 80 ℃ 20 h).
- **측정 스택**: 인장(free-standing), 나노압입(필름 0.1 mN / 전극 2.0 mN), DSC, AFM 위상, FT-IR, ⁷Li NMR, EIS(필름 σ),
  ICP-MS(킬레이션·TM 침적), SAICAS, TEM/SEM/confocal, GITT, DRT/GEIS, TOF-SIMS, XPS, 싱크로트론 nano-CT/TXM,
  STEM-EELS, confocal Raman(z-분해 redox).

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| Scheme 1 | a) PVDF vs ICEP 캐소드 개념도(균열·박리·전도경로) b) RAFT 합성 경로 + 관능기 기능 지도 | binder 3기능(탄성·접착·이온전도) 분해 프레임 — SDCP 요구사양 체크리스트로 사용 |
| **Fig 1** | a) 인장 S-S(283 % vs 31.8 %) b) 나노압입 load-depth c) **E 6.03/H 0.42 GPa** d) FT-IR(전해질 배위) e) **σ_ion 0.135 vs 0.065 mS/cm** f) Mn²⁺ 킬레이션 | ★ binder 물성 앵커 원천. e)가 "이온전도 binder 클래스"의 수치 |
| **Fig 2** | a,d) TEM: PVDF 응집 vs **ICEP ~7 nm 균일 코팅** b,e) SEM c,f) 3D 프로파일 g) **DFT 흡착에너지 4종** h,i) **SAICAS**(깊이별 F_h) j) **전극 E 1.57 vs 0.11 GPa** | ★ coat-vs-aggregate 형상 근거 + 접착·전극강성 앵커. i) 깊이별 접착 = binder z-분포 간접 프로브(Bak2024 A7 결) |
| Fig 3 | a) 0.5C 사이클(85.5 vs 28.9 %) b) rate c) **GITT R_int·D_Li(SOC/DOD 분해)** d) ex-situ DRT P1–P4 e,f) in-situ GEIS-DRT 맵 | c) D_Li 0.42 vs 0.18e-7 = binder-σ가 셀 kinetics로 발현되는 정량 사슬; DRT는 Kim2025 TLM과 상보(분해 철학 동일, 회로-비의존) |
| Fig 4 | a) Li 음극 TM 침적 ICP-MS b,c) TOF-SIMS 깊이 프로파일 d) 3D TOF-SIMS 재구성 | CEI 화학축 — 우리 미보유(계면화학, Kang/Kim 랩 축과 동류) |
| Fig 5 | a,b) **nano-CT 3D**: PVDF 분쇄+균열 vs ICEP 무손상 c,d) STEM rock-salt 11.3 vs 3.1 nm e,f) EELS | ★ "binder가 입자 균열을 막는다"의 직접 구조 증거 — binder 유무가 AM 파괴율을 바꾼다는 실험 근거(우리 fracture 모델에 binder 항 없음) |
| **Fig 6** | a) 로딩별 프로파일 b) 로딩 비교(문헌 대비) c) **에너지밀도 vs 로딩(PVDF 31.7 하락·40.7 실패)** d–f) **z-분해 Raman E_g/A₁g** g) 고로딩 사이클 h) 파우치 중량 파이 i) 스택 추산 j) 파우치 96.7 %@40 | c) = "binder 역학이 로딩 상한을 정한다" 정량 곡선; d–f) = **두께방향 반응 균일성의 z-분해 실측** — 우리 Phase-5 graded-z가 예측해야 할 관측량의 실험 원형 |

## 6. Post-processing ★
- **SAICAS 절삭/박리 2모드**: cutting(전극 내부 cohesion) / peeling(집전체 adhesion) 분리 — F_h(N)를 전극 깊이 %와
  시간축으로 기록(blade 1 mm). 우리 계산으로 N/m 환산 가능(F/폭).
- **z-분해 confocal Raman**: E_g/A₁g 강도비를 SOC 프록시로, top/bottom 위치별 → **두께방향 반응 불균일의 정량화**.
  (PVDF bottom 0.84 = pristine 0.83 → 바닥 완전 미반응.)
- **DRT (distribution of relaxation times)**: EIS를 완화시간 스펙트럼으로 — P1(계면반응)~P4(전하이동+고상확산) 4피크
  귀속, in-situ GEIS로 사이클 중 맵. 회로-모델 비의존 = Kim2025 modified-TLM의 대안 분해법.
- **TOF-SIMS 깊이/3D 재구성**: CEI 2층 구조(외곽 금속유래 / 내부 전해질 분해물), 스퍼터 시간→두께 프록시.
- **nano-CT/TXM**: 76 µm FOV·44 nm 픽셀 3D 균열 시각화(균열 정량 %는 미보고 — 정성).
- **GITT**: SOC/DOD별 R_internal·D_Li⁺ 분해.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| ① 시스템 | **액체 LIB, 습식 슬러리, NCM811+LiPF₆+Li** | ASSB LPSCl+NMC811, 건식 cold-press 300 MPa | **이온 위상 역전**: 그들 pore=전해질(전도체), binder는 *계면 필름/kinetics 보조*; 우리 pore=죽은 공간, SE망=전도체, binder는 *SE망 차단자*. 절대값 전이 전면 금지, 물성 앵커만 |
| ② binder 클래스 | **이온전도 binder σ_b=0.135 mS/cm** (swollen 추정) | PTFE σ_b≈0 (절연; Lee2025 5 wt%→σ_i −90 %, Hong#271 −26 %) | ★ 새 클래스. σ_b/σ_LPSCl ≈ **1/12** → binder-voxel σ를 0이 아니라 유한값으로 두는 W2 파라미터 축 신설 근거. 단 ICEP 전도는 액체-swollen 메커니즘 개연 → **건식 ASSB로 값 그대로 전이 금지**(SDCP는 자체 측정 필요) |
| ③ binder 형상 | **coat형 ~7 nm 균일**(습식, H-bond 흡착 구동) vs PVDF aggregate형 | PTFE **fibril/bridge형**(건식 전단; cbd_morphology_roadmap curl+nucleate+shear-draw) | 3-morphology 분류 완성: **coat(습식 흡착) / aggregate(습식 약흡착) / fibril(건식 전단)** — 형상은 화학(흡착에너지)+공정(전단)이 결정. 시딩 시나리오 분기 근거 |
| ④ 7 nm coat의 수송 결말 | "충분히 얇아 Li⁺ 접근 유지" (정성) | (우리 계산†) film ASR = t/σ_b: ICEP 7 nm → **~5×10⁻³ Ω·cm²** (무시) vs 같은 7 nm PTFE-급(σ≤1e-10 S/cm) → **≥10³–10⁴ Ω·cm²** (차단) | †우리 정량화. Bielefeld2020 AM/SE 계면저항 40 Ω·cm²·Kim2025 R_ct 22–453과 비교하면 **전도-coat는 계면저항 예산에서 사실상 0, 절연-coat는 지배** — "binder 화학이 coat 허용여부를 정한다"의 스케일 논증 |
| ⑤ binder 역학 | 필름 E 6.03 GPa(압입)/E_tensile ~10–25 MPa(digitized)/flow ~2.7 MPa/연신 283 % | MPM `--coh`(SE cold-weld 인력항, 수치 앵커 부재), binder 역학상 미모델(A3) | ★ **--coh/A3 앵커 후보**: binder-bridge 인장 스케일 = **σ ~ 2.7 MPa**(필름 flow) × 접촉면 binder 면적분율. E는 프로브 의존 3-decade 스프레드 → MPM binder상에 6 GPa 그대로 넣지 말 것(§10) |
| ⑥ 접착 | SAICAS **270 N/m**(박리, apparent) vs PVDF 40 | 명시적 binder bond 없음(A3 백로그; Sangrós/Lyu bond 모델 digest만) | apparent peel(소성 소산 포함) ≫ 고유 G_c — Bucci G_c 4 J/m²와 층위 다름. A3 bond 강도 캘리브레이션의 *상한측* 실험 앵커 |
| ⑦ 전극 유효 E | **1.57 GPa** (NCM811+binder 전극, 나노압입) | MPM champion E_eff **1.53 GPa** (연화 SE 프록시) | **수치 인접 = 우연이되 유익**: 실측 복합전극-스케일 유효강성이 O(1 GPa) 밴드라는 외부 확인 — 우리 "전극 스케일 유효 E ~1.5 GPa" 서사의 실측 동반자. 단 물리 기원 다름(그들 다공 폴리머-복합 압입 vs 우리 granular 연화 프록시) — 동일시 금지 |
| ⑧ 고로딩 균열 driver | **습식 건조 모세관 응력**(binder 이동/segregation→균열·박리; PVDF 40.7 mg/cm² 실패) | **압밀 접촉응력**(Auerbach) + 사이클 축은 미보유(frame[5]) | driver 다름: 건조응력은 우리 건식 공정에 없음. 전이되는 건 "**binder 탄성·접착이 전극 파괴 한계를 정한다**"는 역학 역할뿐 |
| ⑨ 두께방향 균일성 | z-분해 Raman E_g/A₁g 실측(PVDF 바닥 미반응) | Phase-5 graded-z(A7) 설계 예정 — 예측 readout 후보 | 그들 = *관측*, 우리 = *구조 예측* — graded-z 출력을 "z별 반응도 프록시"로 내보내면 이런 실험과 접점 |
| ⑩ transport 방법 | 셀-레벨 kinetics(GITT D_Li, DRT R) — 구조-분해 σ 없음 | Kirchhoff/Holm 접촉망 σ 삼중항 + Stage-E | 그들은 구조→σ 솔버 없음(우리 고유); 우리는 R_ct/D_Li/CEI kinetics 없음(그들·Kim2025 영역) — frame[5] 그대로 |
| ⑪ AM 파괴 | binder가 입자 균열 억제(nano-CT 직접) — **binder→AM 파괴 커플링** | Auerbach 파괴에 binder 항 없음 | 사이클-driver(Li 구배)라 직접 흡수 불가하나, "binder 접착이 균열 전파·박리를 막는다"는 A3 bond 도입 시 fracture 쪽 기대효과 방향 근거 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **(W2/A3/SDCP) "이온전도 binder" 클래스 신설**: binder-voxel/접촉 차단 모델에 σ_b 파라미터 도입 —
  PTFE=0, ICEP-급=0.1 mS/cm 오더(σ_SE의 ~1/12). 우리 voxel σ-블로킹(SuperP/VGCF·Hong#271·Lee2025 페널티)을
  σ_b>0으로 재실행하면 "**전도성 binder가 binder 페널티를 얼마나 되돌리나**"가 즉시 정량화됨 — SDCP 논증의 시뮬 축.
- ② **(A3 --coh 앵커)** binder-bridge 인력 스케일: **σ_coh ~ 2.7 MPa**(ICEP flow stress; PTFE와 자릿수 비슷한 soft-폴리머
  스케일) — MPM `--coh`가 "porosity엔 무영향, wallP/인장 무결성에 영향"임은 이미 확인됐으므로, binder --coh는
  **인장/박리·springback 축**의 물성으로 캘리브레이션(접착 270 N/m는 bond-파괴 에너지 상한측 참고).
- ③ **(시딩 형상)** coat형 binder는 **7 nm = sub-voxel**(우리 복셀 ~0.14 µm의 1/20) → resolved 상으로 깔지 말고
  **계면 성질**(AM|SE 접촉 conductance 수정 / coverage modifier)로 넣는 게 옳음; fibril(PTFE)만 resolved 시딩.
  "coat=interface property, fibril=resolved phase" 이분법을 CBD 파이프라인 규칙으로.
- ④ **(SDCP 요구사양 템플릿)** ICEP가 정의한 3기능 목표수치: σ_ion ≳0.1 mS/cm(swollen), 연신 ≳200 %,
  접착 SAICAS 수백 N/m, TM 킬레이션, Tg<RT 연질상+물리가교 경질상(2-Tg). SDCP 실측치를 이 표에 나란히 놓으면 됨.
- ⑤ **(z-균일성 readout)** Phase-5 graded-z 출력에 "z별 활용도/반응도" 프록시를 추가하면 E_g/A₁g류 z-분해 실험과
  직접 비교 가능한 관측량이 생김.

## 9. 인용 가능 문장 (deck/paper용)
- "Han et al. (Adv. Mater. 2025) demonstrate an ionically conductive elastic binder (σ≈0.135 mS/cm, 283 % elongation,
  ~7 nm conformal coating on NCM811) that enables crack-free 62.4 mg/cm² electrodes — defining a binder class whose
  ionic conductivity is finite rather than insulating, in contrast to PTFE."
- "A 7-nm ion-conducting binder film adds only ~5×10⁻³ Ω·cm² of interfacial ASR (t/σ), negligible against reported
  AM/SE interface resistances of 22–453 Ω·cm² — whereas the same film of an insulating binder would dominate them.
  (film-ASR figures derived by us from Han's stated t and σ.)"
- "실측 복합전극-스케일 유효강성(나노압입 1.57 GPa, Han 2025)은 우리 전극-스케일 유효 E(1.35–1.53 GPa) 밴드와
  같은 오더 — 구성상 벌크 E(수십~수백 GPa)가 전극 스케일에서 O(1 GPa)로 내려온다는 서사의 외부 실측점."

## 10. 주의/한계 (over-claim 방지)
- **액체 LIB·습식 공정 — ASSB/LPSCl/건식 아님.** 압밀 porosity·Heckel·σ_eff(복합) 데이터 전무 → 우리 압밀·수송
  절대축과 비교 불가. binder *물성 앵커*로만.
- **σ_ion 0.135 mS/cm의 조건 불명(본문)**: 필름 전처리(전해질 swelling) 미기재 — PVDF 0.065 mS/cm는 건식 PVDF로
  불가능한 값(건식 ~1e-9 이하)이라 **swollen/겔 상태 추정**. 건식 ASSB 바인더(SDCP dry) σ로 그대로 이식 금지.
- **toughness 단위 의심**: stated "J m⁻³"는 S-S 면적(~7 MJ/m³)과 3자릿수 불일치 — MJ/m³ 오기 개연. 절대값 인용 금지,
  ICEP/PVDF 비(≈4×)만.
- **E 3-decade 스프레드**: 나노압입 6.03 GPa(표면 유리질 hard-block·소변형) vs 인장 초기 기울기 ~10–25 MPa(digitized,
  벌크 엘라스토머 망). 모순 아님(프로브 다름) — 그러나 **MPM binder상 E로 6 GPa를 쓰면 안 됨**(bulk 거동은 MPa-급).
- **SAICAS N/m 환산·film-ASR 계산·σ_b/σ_SE 비는 전부 우리 유도값** — 논문 stated 아님, 인용 시 명시.
- **digitized 값**(flow 2.7 MPa, E_tensile, PVDF TM 침적 ~500 ppm)은 추세용(±).
- **조성비·용매·캘린더링·porosity·carbon 종류 = SI-only** (본문 n/a). 전극 두께 230/190 µm의 로딩 짝 미기재 →
  전극 밀도/porosity 역산 불가.
- **DFT는 분자 흡착에너지**(eV) — 연속체 접착강도(N/m·MPa)로 직접 환산 불가, 서열(AMPS≫PVDF≫AN)만.
- 시뮬레이션 없음(순수 실험) → frame[4] 교차검증 상대가 아니라 **frame[5] binder-화학/계면 절반의 실험 앵커**.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
