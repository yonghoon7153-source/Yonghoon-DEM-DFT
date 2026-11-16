<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · he2026_dem_calendering_inhomogeneity_areal_density.md -->
# X-CT 실구조(Ebner 2013)를 초기형상으로 쓴 DEM 으로 NMC111 양극 캘린더링 — **박리(실은 수직 인장) 시험으로 입자–집전체 bond 강도 보정** · 30/60/200 MPa 가압–제하 · 힘사슬·응력텐서·집전체 매립·체적에너지밀도 — Zhang·Gao·Xiao·Ding (*JOM* 2026)

> slug `zhang2026_xct_dem_cathode_calendering_peel_calibration` · DOI `10.1007/s11837-026-08748-x` · type `DEM (Hertz–Mindlin + linear parallel bond · 코드 미명시 · X-CT 초기구조 · 박리 보정 · 액체계 LIB NMC111)` · PDF `2fa0a4ea-1._Investigation_into_Microstructural_and_Mechanical_Evolution_During_Lithium-Ion_Battery_Cathode_Calendering_via_X-ray_Tomography-Based_Discrete_Element_Method.pdf` · digested `2026-09-26` · status ✅

> elements: Al C Co F Li Mn Ni O
> methods: elastic, adhesion

> ⚠⚠ **한 줄 경고 — SE 가 없고, 대부분의 수치가 "하중 상태" 값이다.**
> 소재는 **NMC111 + C65 + PVDF (96:2:2)** 의 **액체계 LIB 양극**이다. 황화물 SE 가 없으니 우리 ASSB 침대
> (AM + LPSCl, SE 가 소성 유동 담당)의 **AM–CBD 골격 극한**으로만 읽는다. 그리고 논문이 헤드라인으로 쓰는
> **체적에너지밀도 2002 Wh L⁻¹ · 응력텐서 · (아마도) 배위수·FSA** 는 **플래튼이 눌러 놓은 상태**의 값이다 —
> 같은 논문의 DEM 이 200 MPa 에서 **하중 중 공극률 ≈ 0.152 를 제하 후 ≈ 0.319 로 되돌린다**(figure-read, §12 D1·D2). 실험과 맞춘 것은 **제하 후** 공극률뿐이다.

> ★★ **이 카드 값의 절반은 §12 파생 원장에 있다.** 논문이 인쇄한 값과 그림 판독값에 산술만 해서, 논문이 쓰지 않은 것을 꺼냈다 —
> ① **Fig 12 의 W_V 곡선은 하중 상태 공극률로 계산된 것**이다 (200 MPa 비율 검산 1.440 vs 판독 1.442). 200 MPa 를 **제하한 구조**로 다시 계산하면 **≈ 1,680 Wh L⁻¹** 다 — 하중 중 ≈ 2,050 보다 ≈ 18 % 낮다 (D1).
> ② **면내 이방성 σ_xx/σ_yy 는 30 MPa 에서 1.196, 200 MPa 에서 1.173 으로 일정**하다 — 논문의 *"200 MPa 에서 이방성이 시작된다"* 는 자기 수치와 어긋난다 (D3).
> ③ **평균 접촉력 7.3 mN 의 Hertz 평균면압 ≈ 6.4 GPa ≈ 0.75 H_NMC** (D50 급 6–6 µm 쌍 가정), 최대 177 mN 은 쌍 크기에 따라 **≈ 9.7–21 GPa ≈ 1.1–2.4 H** — 탄성 Hertz 가 경도를 넘는 접촉이 있다. 그리고 **같은 힘이면 큰 입자의 면압이 더 낮다** ⇒ *"큰 입자가 더 잘 깨진다"* 는 **힘만으로는 나오지 않는다** (D7).
> 정본 `wheatcroft2023_*` 의 이차입자 파괴강도 **σ_F = P_f/D²** 로 정규화하면 오히려 **큰 입자에 끼인 작은 입자**(163 mN 접촉의 4.7 µm 쪽 ≈ 7 GPa)가 가장 과응력이다 (D7b — Fig 9 가 각 접촉을 **두 입자 지름에 한 번씩 두 번** 찍는다는 판독이 이 짝짓기를 가능하게 했다).

---

## 0. 서지 · 출처 · 읽은 범위

| 항목 | 내용 | 등급 |
|---|---|---|
| 제목 | *Investigation into Microstructural and Mechanical Evolution During Lithium-Ion Battery Cathode Calendering via X-ray Tomography-Based Discrete Element Method* | stated (p.1) |
| 저자 | **Xiao Zhang**¹, **Tengteng Gao**¹ (공동 1저자, *"contributed to this work equally"*), Zhiqiang Xiao¹, **Yanhuai Ding**¹˒² (교신, yhding@xtu.edu.cn) | stated (p.1) |
| 소속 | ¹ School of Mechanical Engineering and Mechanics, **Xiangtan University**, Xiangtan 411105, China | stated (p.1) |
| 저널 | ***JOM*** (The Minerals, Metals & Materials Society) — 특집 *"Advances in Energy Materials Research: Fundamentals and Applications"* | stated (p.1 머리띠) |
| DOI | `10.1007/s11837-026-08748-x` | stated (p.1) |
| 권·호·쪽 | **[미확인]** — PDF 어디에도 인쇄돼 있지 않다 (1쪽 머리에 `JOM` + DOI + © 2026 TMS 뿐, 각 쪽 머리띠는 제목/저자명) | — |
| 이력 | 투고 **2026-05-01** · 게재확정 **2026-08-25** · 온라인 **2026-09-21** [정정 2026-11-16 · 원문 p.1: 인쇄된 것은 *"(Received May 1, 2026; accepted August 25, 2026)"* 뿐 — 온라인 날짜는 이 PDF 16 쪽 어디에도 없다 (텍스트 층 'online' · 'Published' 0 건 · PDF 메타데이터 생성일 2026-09-19) · '온라인 2026-09-21' 의 근거 [미확인]] | stated (p.1) — 온라인 날짜 제외 |
| 자금 | Natural Science Foundation of Hunan Province **2025JJ70094** | stated (p.16) |
| 데이터 | *"available from the corresponding authors on reasonable request"* — 원자료 비공개 | stated (p.16) |
| **SI** | **없다.** 본문 16쪽 전 텍스트에서 *Supplementary · Supporting · ESM · Electronic supplementary · Appendix* 검색 0건 ⇒ SI 가 존재한다는 근거가 없다 (SI 미확보가 아니라 **SI 언급 자체가 없음**) | 검색 결과 |
| **읽은 범위** | 16쪽 전부 (텍스트 층 + 쪽 렌더 육안). 그림 12장 + Table I 전부 크롭 후 육안 확인. Fig 2d·4b·4c·7·9·10·12 는 **원본 래스터 픽셀 판독**(축 눈금 픽셀 → 선형 환산)으로 값을 뽑았다 [보강 2026-11-16: 1저자가 다시 준 PDF (68-1 번 파일 · 16 쪽 · 같은 판) 로 전 16 쪽 재정독 · 카드 대조 · 판독 재확인 (`digitized.csv` 55 행) — 끝 절 '보강 기록'] | — |
| **안 읽은 것** | 이 논문이 기대는 **Ebner 2013 (ref 22, X-CT 데이터셋 원전)** · Ge 2022 (ref 18) · Lippke 2024 (ref 32) · Sonzogni 2024 (ref 21) · Srivastava 2020 (ref 28) · Stershic 2015 (ref 30) 원문은 **리포에 정본 카드가 없고 이번에 읽지 않았다** — 그들에 대한 서술은 전부 *"이 논문이 인용한 내용 (ref N)"* 이다 [보강 2026-11-16: 그 뒤 정본 카드가 생긴 것 = ref 22 `ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation` · ref 18 `ge2022_xct_initial_structure_dem_calendering_nmc333` · ref 30 `stershic2015_fabric_tensor_calendering_nmc_xct_dem` · ref 21 `sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811` (+ ref 8 `meyer2017_calendering_compaction_resistance_line_load_exponential_model`) · 아직 카드 없음 = Lippke 2024 (ref 32) · Srivastava 2020 (ref 28) · 2 차 서술 대조 = §14 · 참고문헌 원문 = §17] | — |

★ 정본 카드가 **있는** 피인용 문헌 (교차 확인에 썼다): ref 17 = `ngandjong2021_dem_calendering_digital_twin` · ref 19 = `sangros2019_dem_calendering_lib_electrode` ·
ref 20 = `sangros2020_lib_electrode_dem_mech_elec_ionic` · **ref 27 = `lyu2025_3d_dem_drying_calendering_lib`** (CBD 2.2 µm 의 출처) ·
**ref 29 = `xu2017_nmc532_nanoindentation_modulus_hardness_toughness`** (E_NMC 142 GPa 계보의 원전 후보).
이 논문이 인용하지 **않았지만** 대조 기준으로 쓴 정본 카드: `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` (NMC811 이차입자 파괴강도 σ_F = P_f/D², §12 D7b) ·
`he2026_dem_calendering_inhomogeneity_areal_density` (같은 부류 캘린더링 DEM).

---

## 1. 한 줄 요약

**Ebner 2013 의 싱크로트론 X-CT 로 분할된 *미압연* NMC 양극에서 100 × 100 × 75 µm³ 부분체적을 잘라, 입자를 등가 구로 바꿔
DEM 초기구조로 쓰고(NMC–NMC = Hertz–Mindlin, CBD = 2.2 µm 구 + linear parallel bond), 입자–집전체 bond 강도를 자체 박리(수직 인장)
시험의 피크 응력(0.0347 MPa)에 맞춘 뒤(7.2 × 10⁴ Pa), 30/60/200 MPa 가압–제하로 공극률(제하 후 0.411 vs 실험 0.412 @30 MPa)·
FSA·배위수(0.906 → 2.05)·집전체 매립(최대 0.937 µm)·힘사슬·응력텐서(σ_zz 198.5 MPa @200 MPa)·체적에너지밀도(1422 → ~2002 Wh L⁻¹)를 보고한다.**
신규성 주장의 핵심은 X-CT→DEM 자체가 아니라(그건 ref 18 Ge 2022 가 먼저 했다고 논문 스스로 인용한다) **입자–집전체 점착을 실측으로 정량 보정한 것**이다.
**수송(σ) 계산은 0건**, 입자 형상 소성 0, AM 파괴 모델 0 — `frame[5]` 로는 **DEM 의 역학·패킹 반쪽만** 가진 논문이다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| **소재계 (시뮬)** | NMC (Ebner 2013 X-CT 의 입자 좌표·부피 → 등가 구) + CBD (2.2 µm 단일 크기 구, **PVDF 50 : CB 50 wt%** 가정, ref 28) · **NMC : CBD = 96 : 4 wt** · Al 집전체(바닥 벽) |
| **소재계 (실험)** | **LiNi₁/₃Mn₁/₃Co₁/₃O₂ (NMC111) : C65 카본블랙 : PVDF = 96 : 2 : 2 wt** · NMP 용매 · 12 µm Al 박. ⚠ **DEM 구조(Ebner 전극)와 실험 전극(자체 NMC111)이 다른 전극이다** (§10 L3) |
| **연구유형** | **DEM 시뮬레이션** (가압–제하) + **박리(수직 인장) 시험**(보정 표적) + **공극률 비교**(검증) + **SEM**(집전체 표면·입자 균열 정성) |
| **코드** | **명시 안 됨 [미확인].** 용어(`ball-ball` / `ball-facet`, linear parallel bond, radius multiplier λ̄, 강성비 κ̄*)가 Itasca PFC 계열 어휘와 같고, CBD 크기의 출처인 ref 27 (Lyu 2025) 은 정본 카드 기준 **PFC3D 5.00** 을 썼다 — **추정일 뿐이다** [보강 2026-11-16 · 원문 16 쪽 텍스트 층 검색: 'PFC' · 'Itasca' · 'EDEM' · 'LIGGGHTS' · 'Rocky' · 'software' · 'code' 0 건 — 코드 · 입자 수 · 시간 간격 · 계산 시간 모두 원문에 없음 확인] |
| **액체/고체** | 액체 전해질 LIB. 공극 = 이온 통로(열어 둘 대상). 우리 ASSB 에서 공극 = 죽은 부피(닫을 대상) — **목표 부호가 반대** |
| **키워드 (저자)** | (JOM 은 키워드 란이 없다) |

### 2.1 계보 — 우리 litdb 안 LIB-calendering DEM peer 들과의 자리

| 카드 | 초기구조 | 접촉·bond | 집전체 점착 | 제하(springback) | 수송 σ | 형상소성 |
|---|---|---|---|---|---|---|
| `sangros2019_dem_calendering_lib_electrode` | 가상 패킹 | **Thornton–Ning**(나노압입 보정) + bond | ✗ (본 논문이 이 점을 지적) | ✅ ER 10.25 → ~17 % | ✗ | ✗ |
| `sangros2020_lib_electrode_dem_mech_elec_ionic` | 〃 (2부) | 〃 | **해석식 eq 5 + pull-off 1.78–2.78 MPa**(그 카드 digitized) | ✅ | 해석 균질화 | ✗ |
| `ngandjong2021_dem_calendering_digital_twin` | CGMD 건조 결과 | GH + SJKR | — | 압입 회복 | FEM 전기화학 | ✗ |
| `schreiner2020_dem_calendering_lib` | 가상 | **EEPA** + Bonding | — | 정성(roll section) | ✗ | ✗ |
| `lyu2025_3d_dem_drying_calendering_lib` (**ref 27**) | DEM 건조 결과 | PFC3D Hertz 류 + **parallel bond(CBD)** / contact bond(AM) | CBD–collector bond | — | 정성 | ✗ |
| `xu2023_realistic_am_shape_cgmd_calendering` | **X-CT 실형상**(CGMD) | LJ + JKR | — | 함의값만(그 카드 derived 0.3–3.5 %) | τ (TauFactor) | ✗(형상 고정) |
| `he2026_dem_calendering_inhomogeneity_areal_density` | 가상 | **EEPA** (bond 없음) + JKR 집전체 | JKR | — | ✗ | ✗ |
| **본 논문 Zhang 2026** | **X-CT → 등가 구**(Ebner 2013) | **Hertz–Mindlin(탄성, 항복 없음)** + **linear parallel bond(CBD)** | ★ **입자–Al bond 강도를 박리 피크에 보정** | ✅ (가압–제하 3회) | **✗** | **✗** |

⇒ **여덟 편 전부 강체 구(또는 고정 형상) + CONTACT 수준 모델, 입자 SHAPE 소성 0** = `frame[5]` 분업(DEM = 수송·패킹 / MPM = 형상 소성)의 또 한 번의 독립 확인.
본 논문의 **고유 lead 두 개**: ① **입자–집전체 bond 강도의 실측 보정** ② **집전체 쪽 관측량**(매립 깊이 지도 · 접촉면적 · SEM).
⚠ 반대로 접촉법칙은 이 계보에서 **가장 단순한 쪽**이다 — Sangrós(Thornton–Ning)·Schreiner/He(EEPA) 는 **접촉 소성**이 있는데, 여기 Hertz–Mindlin 은 **순수 탄성**이다.

---

## 2.5 논문 흐름 — 절별로 (읽는 순서 그대로)

1. **Introduction (pp.1–2).** 캘린더링은 공극·접촉·수송·에너지밀도를 바꾸지만 과압밀은 구조저항·응력 누적을 부른다(refs 4–6). [정정 2026-11-16 · 원문 p.1: refs 4–6 은 *"…it is essential to establish quantitative process–structure–performance relationships in order to identify an optimal processing window for electrode design.⁴⁻⁶"* 문장 끝에 붙는다 — '과압밀 → 구조저항 · 응력 누적' 문장 (*"excessive densification may increase structural resistance, hinder mass transport, and aggravate stress accumulation"*) 에는 인용 번호가 없다]
   선행 인용: Meyer (ref 8) 압밀력–공극감소 **지수 관계** · 과압연이 흑연 음극 젖음성을 해친다(ref 9) · CBD 는 캘린더링 중 나노다공 CBD 상으로 뭉친다(ref 10) ·
   Sim (ref 11) Co-free LiNi₀.₉Mn₀.₀₅Al₀.₀₅O₂ 에서 고압은 **입자 파쇄·융합**을 일으키나 장기 유지율은 오히려 좋다 ·
   Zhang (ref 12) 미세스크래치·박리: 캘린더링 하중↑ → 점착↑ 이지만 **Al 집전체 미세손상↑ → 전극 파괴에너지↓** ·
   X-CT 선행: Lu (ref 15) nano-CT 이중 스캔으로 CBD 가시화 · Pietsch (ref 16) in-situ 싱크로트론 + XRD · [보강 2026-11-16 · 원문 p.2: ref 15 문장과 ref 16 문장 사이에 인용 번호 없는 문장 *"In addition, in situ X-CT was used to monitor the evolution of porosity and tortuosity during successive calendering steps."* 이 있다 — 누구의 일인지 원문이 적지 않는다 (정본 `lu2020_insitu_nanoct_calendering_microstructural_evolution` = *Joule* 2020 · 이 목록에 없는 다른 Lu 논문이 같은 주제 [카드 관찰]) · ref 16 은 본문에 저자 이름 없이 번호만]
   DEM 선행: Ngandjong (ref 17) 3D DEM + CGMD + FEM 멀티스케일 · **Ge (ref 18) 가 이미 X-CT 미압연 구조를 DEM 에 넣어 공극·접촉망·응력을 분석** ·
   Sangrós (refs 19, 20) bond 파단 · Sonzogni (ref 21) **회전 롤 + 응집-소성 바인더 접촉법칙**. [보강 2026-11-16 · 원문 p.2 대조: refs 19, 20 = *"The coupled mechanical–electrochemical behavior of electrodes was investigated, highlighting the role of interparticle bond breakage in structural integrity degradation."* · ref 21 = *"…introduced rotating cylindrical rollers to more realistically represent the calendering process and proposed a novel contact law incorporating cohesive-plastic behavior of binder layers, thereby addressing limitations in previous models that neglected roller curvature and shear stresses."* — 카드 서술과 같다 (§14)]
   ⇒ 저자들의 문제 제기: *"대부분의 DEM 은 가상 패킹이고 실구조 검증이 없다"* → X-CT 구조 + 정량 보정.
   (전부 **이 논문이 인용한 내용**이며 원문 미확인.) [보강 2026-11-16: 그 뒤 ref 8 · 17 · 18 · 19 · 20 · 21 · 22 · 27 · 29 · 30 은 정본 카드가 있다 — 각 2 차 서술을 원문 문장과 대조한 표 = §14]
2. **Experimental — Data (pp.2–3).** Ebner 2013 (ref 22) 의 싱크로트론 X-CT 데이터셋은 재구성·분할이 **이미 끝난 상태**이고, **입자 단위 좌표·부피 주석**을 준다. 저자들은 그걸 가져와 RVE 를 만들었다 (**CT 를 직접 찍지 않았다**). [보강 2026-11-16 · 원문 p.4: 같은 논문이 *"By applying image filtering and binarization to the tomographic images, the NMC particle phase was successfully identified and extracted."* 라고도 쓴다 (수동태 — 저자가 Ebner 분할을 다시 이진화했는지 · Ebner 의 분할 결과를 그대로 썼는지 원문이 가르지 않는다 [미확인]) · 'CT 를 직접 찍지 않았다' 는 그대로 (p.2 *"The tomography datasets were sourced from the experimental work of Ebner et al."*)]
3. **Experimental — 검증용 전극 (p.3).** NMC111 : C65 : PVDF = 96:2:2, NMP, **8 h 혼합** → **> 3 h 정치 탈포** → 자동 필름 도포기로 **12 µm Al** 에 도포 → **진공 80 °C 8 h** 건조 → **Ø 12 mm** 타발 → 박리 시험용.
   ⚠ **캘린더링 방법(롤/프레스)·조건·면적로딩·두께·공극률 측정법은 한 줄도 없다** [미확인].
4. **DEM Modeling Method (pp.3–4).** Hertz–Mindlin (eqs 1–6) + linear parallel bond (eqs 7–21) — §4.
5. **Structural Generation (pp.4–5).** RVE 100 × 100 × 75 µm³, CBD 2.2 µm 구, NMC 등가 구, PSD D10/D50/D90 = 3.39/6.04/11.1 µm, 주기경계 x·y, 바닥 = Al 집전체, 위 = 강체 플래튼, 0.01 m s⁻¹ 속도 구동, 목표 응력 도달 시 정지 후 같은 속도로 후퇴(탄성회복), Table I.
6. **Improvement of the Existing Model (pp.5–6).** Sangrós 2019 (ref 19) 모델은 계면 점착이 없어 **제하 때 코팅이 들뜰 수 있고**, Lippke 2024 (ref 32) 는 입자–집전체 응집을 넣었지만 **정량 보정을 안 했다** → 박리 시험 피크를 표적으로 `σ̄_Particle-Al` 을 반복 보정 → **7.2 × 10⁴ Pa**, 시뮬 피크 **0.0349 MPa** vs 실험 **0.0347 ± 0.0032 MPa** (< 1 %). Fig 3. [보강 2026-11-16 · 원문 p.6: ref 19 를 본문은 *"The model proposed by Giménez et al.¹⁹"* 로 부른다 (= 목록 [19] Sangrós Giménez) — *"does not take interfacial adhesion effects into account, which may lead to delamination of the electrode coating during unloading"* · ref 32 = *"Lippke et al.³² extended the adhesion model by incorporating cohesive interactions between particles and the current collector into the analytical framework, thereby suppressing coating detachment during calendering simulations. However, the interfacial adhesion parameters in their work were not quantitatively calibrated."* — 카드 서술과 같다]
7. **Results 1 — Calibration and Validation of Calendering Simulation (pp.7–8).** 법선·접선 파라미터를 **같은 전략**으로 설정해 보정 복잡도를 줄였다 → **Ē* = 0.3 GPa · σ̄_Particle-Particle = 3.6 × 10⁷ Pa · λ̄ = 2**. 공극률 0.432 → 0.333 (≈30 MPa, 하중) → **0.411 (제하)** vs 실험 **0.412**; 최대 상대오차 < 3 %. 후반부 편차는 **구 근사의 부피 손실** 탓으로 돌린다. Fig 4.
8. **Results 2 — Structural and Mechanical Properties (pp.8–15).** FSA·배위수 (Fig 5) → 집전체 매립·접촉면적 (Figs 6–7) → 힘사슬 (Fig 8) → 입자별 접촉력 (Fig 9) → 응력텐서 (Fig 10) → SEM (Fig 11) → 체적에너지밀도 (Fig 12). 200 MPa 는 **"최적 공정 조건으로 권하지 않는다 — 손상 거동을 드러내기 위한 조건"** 이라고 스스로 못박는다 (p.14).
9. **Conclusion (p.15).** 위 수치의 재진술 + *"성능 이득과 기계적 위험의 trade-off"*.

---

## 3. 핵심 수치 ★

> 등급: **stated** = 본문/표에 인쇄된 값 · **figure-read ≈** = 원본 래스터 픽셀 판독(추세용, 거짓 정밀 금지) · **derived(ours)** = 우리 산술(§12) · **[미확인]** = 논문에 없음

### 3.1 입력 파라미터 — NMC (Table 1 = 원문 표기 **Table I**, p.5; 출처 표기 refs 27, 29–31)

| 파라미터 | 값 | 등급 | 비고 |
|---|---|---|---|
| Young's modulus | **142 GPa** | stated | 정본 `xu2017_*` 카드: 미사용 NMC532 **이차입자 나노압입 142.5 ± 11.3 GPa** — 계보상 이 값으로 보인다(표는 4개 ref 를 한꺼번에 단다). 우리 E_AM **140 GPa** 와 사실상 같은 값 |
| Poisson ratio | **0.25** | stated | (xu2017 는 E 환산에 ν=0.3 을 가정 — 그 카드 기록) |
| friction factor | **0.12** | stated | ref 27 Lyu 2025 카드의 AM 미끄럼 마찰 0.12 와 같다 |
| Density | **4750 kg m⁻³** | stated | |
| Damping factor | **0.95** | stated | ⚠ **정의 미기재** — eq (1)의 β 인지, 반발계수 류인지 [미확인] |

### 3.2 입력 파라미터 — CBD · bond · 집전체 · 공정 (본문)

| 파라미터 | 값 | 등급 | 출처 쪽 |
|---|---|---|---|
| CBD 입자 지름 D_c | **2.2 µm** (단일 크기 구) | stated (ref 27 인용) | p.4 |
| CBD 조성 | **PVDF 50 : CB 50 wt%** 가정 | stated (ref 28 인용) | p.4 |
| NMC : CBD | **96 : 4 wt** | stated | p.4 |
| bond 유효 탄성률 Ē* | **0.3 GPa** | stated (보정값) | p.7 |
| 입자–입자 bond 강도 σ̄_Particle-Particle | **3.6 × 10⁷ Pa** (= 36 MPa) | stated (보정값) | p.7 |
| radius multiplier λ̄ | **2** | stated (*"fixed at 2"*) | p.7 |
| bond 형성 간격계수 ξ̄ | **1.5** → 간격 허용 **ξ̄·D_c = 3.3 µm** | stated / derived | p.4 |
| **입자–Al bond 강도 σ̄_Particle-Al** | **7.2 × 10⁴ Pa** (= 72 kPa) | stated (박리 보정값) | p.6 |
| Al 집전체 E / ν / ρ | **68.9 GPa / 0.3 / 2700 kg m⁻³** | stated | p.4 |
| 플래튼 속도 (가압·제하 동일) | **0.01 m s⁻¹** (ref 18 과 일관) [보강 2026-11-16 · 원문 p.4–5: 인용 18 은 속도 값에만 붙는다 — *"with the platen velocity set to 0.01 m s⁻¹, consistent with previous studies.¹⁸"* · 제하 (*"moved upward in the opposite direction at the same velocity to simulate elastic recovery"*) 는 이 논문 자신의 절차] | stated | p.4–5 |
| 목표 응력 | **30 · 60 · 200 MPa** (+ 0 MPa 초기) | stated | Fig 4a |
| bond 강성비 κ̄* · bond 전단강도 c̄ · CBD 의 E·ν·ρ·마찰 · 벽 마찰 · 시간간격 · 입자 수 · 시드 수 | **[미확인]** — 어디에도 없다 | — | — |

### 3.3 입도 (Fig 2d)

| 양 | 값 | 등급 |
|---|---|---|
| D10 / D50 / D90 | **3.39 / 6.04 / 11.1 µm** | stated (p.4) |
| ⚠ 무엇의 분위수인가 | Fig 2d x축 = **"Particle radius (µm)"** 이고, 누적 부피분율 곡선이 0.1·0.5 를 **반지름 ≈ 3.36 · ≈ 6.08 µm** 에서 지난다 | figure-read ≈ |
| ⇒ 해석 | 본문의 "D" 값은 **반지름 분위수**로 읽힌다 ⇒ 지름으로는 **≈ 6.8 / 12.1 / 22.2 µm** | derived(ours) |
| D90 의 작은 불일치 | 곡선의 0.9 교차는 **반지름 ≈ 10.1 µm** (표식 9.56 → 0.886, 10.48 → 0.909 사이 선형보간) — 본문 11.1 과 ≈ 1 µm 차 | figure-read ≈ |
| 최대 입자 | Fig 2d 끝점 반지름 **≈ 16 µm**, Fig 9 x축(**지름**) 끝 **≈ 32 µm** — 서로 정합 | figure-read ≈ |

### 3.4 박리(점착) 보정 (Fig 3, pp.6–7)

| 양 | 값 | 등급 |
|---|---|---|
| 시편 | Ø 12 mm, 코팅면·집전체면 양쪽에 고강도 구조용(순간) 접착제 → 경화 → 만능시험기 [보강 2026-11-16 · 원문 p.6 · Fig 3a: 본문 = *"peel-force tests were performed using a gel-type adhesive"* · *"Structural adhesive with high bonding strength was then applied to both the coating surface and the current collector surface"* · '(순간)' = Fig 3a 라벨 *"Instant adhesive"* · 시편 = *"the as-prepared and fully dried electrode sheets"* (아래 '내부 불일치' 줄)] | stated |
| 박리 속도 | **0.01 m min⁻¹** | stated |
| 반복 | **3회** | stated |
| 박리 "각도" | *"at a prescribed angle"* — **값 미기재** [미확인]. ⚠ Fig 3a 모식은 **면에 수직으로 당기는 인장(pull-off)** 배치다 | stated / figure |
| **박리강도 (~200 MPa 캘린더링 전극)** | **0.17 ± 15 % MPa** | stated (p.6) |
| **보정 표적 (실험 피크)** | **0.0347 ± 0.0032 MPa** | stated (p.6) |
| 시뮬 피크 | **0.0349 MPa** · 상대오차 **< 1 %** | stated |
| ⛔ 내부 불일치 | 같은 쪽에 **0.17 MPa** 와 **0.0347 MPa** 가 둘 다 "실험 박리값"으로 나온다 (**≈ 4.9배 차**). 어느 전극·어느 정의인지 논문이 가르지 않는다 [보강 2026-11-16 · 원문 p.6: 시편 상태도 문장끼리 어긋난다 — 시편 = *"the as-prepared and fully dried electrode sheets"* (같은 논문 Fig 11 캡션은 *"as-prepared (uncalendered)"* 로 쓴다) ↔ 값 = *"The obtained peel strength of the electrode with a calendering stress ∼ 200 MPa is 0.17 ± 15% MPa"* · 박리 시편이 압연 전극인지 [미확인]] | — |
| 곡선 형태 | 실험 = **오목**(초기 급상승 → 기울기 감소 → 평탄 → 급락), t ≈ 0.39 · ≈ 0.57 에 작은 하중 강하 · DEM = **거의 직선** 상승 후 피크에서 파단(점선 수직 강하) | figure-read |

### 3.5 ★ 공극률 — 가압·제하 경로 (Fig 4b, 4c)

| 압력 (MPa) | DEM **하중 중** ε (Fig 4b) | DEM **제하 후** ε (Fig 4c) | 실험 ε (Fig 4c) | 등급 |
|---|---|---|---|---|
| 0 | **0.432** | — | ≈ 0.424 | stated / figure-read |
| 30 | **0.333** (≈30 MPa) | **0.411** | **0.412** | **stated** |
| 60 | ≈ 0.280 | ≈ 0.370 | ≈ 0.359 | figure-read ≈ |
| 100 | ≈ 0.213 | — | — | figure-read ≈ |
| 140 | ≈ 0.174 | — | — | figure-read ≈ |
| 200 | ≈ 0.152 | ≈ 0.319 | ≈ 0.310 | figure-read ≈ |

- **Fig 4b 의 읽는 법 (범례가 없다 — 우리 해석)**: 곡선 세 색은 **세 번의 독립 런**(목표 30 = 자홍, 60 = 보라, 200 = 초록)이다.
  세 런은 같은 초기구조에서 출발하므로 **가압 경로가 겹치고**, 더 높은 목표의 런은 앞 런의 끝점부터만 보인다.
  각 색의 **아래 가지 = 제하 경로**. 끝점(P = 0) 부근은 **y축 위를 수직으로** 올라가 축선에 가려진다 ⇒ 제하 후 공극률은 Fig 4b 가 아니라 **Fig 4c 에서 읽어야 한다**.
- **제하 경로의 모양** (figure-read ≈): 200 MPa 런은 **5 MPa 에서 아직 ε ≈ 0.236**, 0 MPa 에서 0.319 ⇒ **회복의 절반가량이 5 MPa 아래에서** 일어난다. 30 MPa 런도 5 MPa 에서 ≈ 0.370 → 0.411.
- **가압 경로의 톱니**: 초록 가지에 ≈ 63–65 · ≈ 95 · ≈ 105 · ≈ 118 MPa 에서 **압력이 잠깐 떨어지며 공극률은 계속 준다** — 변위 제어 시험의 **하중 강하(구조 붕괴·bond 파단 류 사건)** 시그니처. 논문은 언급하지 않는다. Fig 12 곡선의 뒤로 꺾이는 고리도 같은 사건이다.
- 논문 주장: *"최대 상대오차 < 3 %"* (stated). 우리 판독으로는 0 MPa +1.9 % · 30 MPa −0.2 % · **60 MPa ≈ +3.1 %** · 200 MPa ≈ +2.9 % (§12 D11) — 60 MPa 가 판독 오차 안에서 경계.
- DEM 이 60·200 MPa 에서 실험보다 **체계적으로 약간 더 성기다**(+0.009–0.011) — 저자 설명은 *"구 근사가 부피 손실 오차를 들여온다"*.

### 3.6 FSA · 배위수 (Fig 5, p.9)

| 압력 (MPa) | FSA (m⁻¹) | ΔFSA (%) | 배위수 CN (N_c/N_p, NMC–NMC 만) | 등급 |
|---|---|---|---|---|
| 0 | **4.381 × 10⁵** | — | — | stated |
| 30 | **4.121 × 10⁵** | **5.9** | **0.906** | stated |
| 60 | **4.038 × 10⁵** | **7.8** | **1.29** | stated |
| 200 | **3.832 × 10⁵** | **12.5** | **2.05** | stated |

- **CN 정의**: *"NMC 입자 간 총 접촉 수 ÷ 전체 NMC 입자 수"* (stated) — **접촉을 한 번씩만 세면** 통상의 평균 배위수 Z = 2N_c/N_p 의 **절반**이다 ⇒ Z 환산 **≈ 1.81 / 2.58 / 4.10** (derived, §12 D4). Sangrós 2019 (정본 카드) 도 같은 `CN = n_c/n_p` 를 쓴다 (1.55 → 2.19).
- ΔFSA 재계산: (4.381 − 4.121)/4.381 = 5.93 % · 7.83 % · 12.53 % — **인쇄값과 정합** (D5).
- 해석(저자): 저압 = 점접촉·국소 접촉 우세, 자유표면 많고 배위수 낮음 → 고압 = *"자유 노출 표면 → 접촉 지배 계면"* 전환, 배위수 증가율은 둔화(포화 경향).
- ⚠ **하중 중 값인지 제하 후 값인지 미기재** [미확인]. 캡션 *"in the calendering stress condition"* 은 하중 상태를 시사한다.

### 3.7 집전체 매립 · 접촉면적 (Figs 6–7, p.10)

| 압력 (MPa) | 최대 매립 깊이 | 집전체–NMC 접촉면적 (Fig 7) | 발자국 대비 (100 × 100 µm²) | 등급 |
|---|---|---|---|---|
| 30 | ≈ 0.3 µm (지도 최고 색) | ≈ 113 µm² | ≈ 1.1 % | figure-read ≈ / derived |
| 60 | **≤ 0.4 µm** (*"does not exceed 0.4 µm"*) | ≈ 198 µm² | ≈ 2.0 % | stated / figure-read |
| 200 | **0.937 µm** | ≈ 490 µm² | ≈ 4.9 % | stated / figure-read |

- Fig 6 컬러바 **0.00–0.940 µm** (눈금 0.118 · 0.235 · 0.353 · 0.470 · 0.588 · 0.705 · 0.823 · 0.940). 지도는 **이산 접촉점을 매끈하게 보간한 등고선**이다 — 입자 사이 빈 곳의 "깊이"는 보간 인공물.
- ⚠ **"매립 깊이"의 정의 미기재.** DEM 의 벽은 변형하지 않으므로, 이 값은 **입자–벽 겹침 δ** 로 읽는 것이 유일하게 가능한 해석이다 (§10 L7). 그렇다면 제하 후에는 사라지는 **탄성** 양이다.
- 논문의 서사: 압력↑ → 매립↑·접촉면적↑ → 계면 전기저항↓(이득) 이지만 **집전체 변형·국부 손상 위험↑**(ref 36: 10–20 µm Al 박은 항복·인장강도가 뚜렷이 낮다 — 이 논문이 인용한 내용).

### 3.8 힘사슬 · 입자별 접촉력 (Figs 8–9, pp.11–12)

| 양 | 값 | 등급 |
|---|---|---|
| 평균 접촉력 @200 MPa | **> 7.3 mN** (*"exceeds 7.3 mN"*) | stated |
| 최대 NMC 접촉력 @30 / 60 / 200 MPa | **≈ 24.7 / ≈ 43 / ≈ 177 mN** | figure-read ≈ (Fig 9a–c 최고점) |
| 최대/평균 @200 MPa | ≈ 24 | derived |
| 플래튼 총하중 @30 / 60 / 200 MPa | **0.3 / 0.6 / 2.0 N** (= P × 10⁻⁸ m²) | derived |

- Fig 8: 선 굵기 ∝ 접촉력, **빨강 = Hertz–Mindlin(NMC–NMC 직접 접촉), 파랑(청록) = bond**. 초기에는 bond 가 망을 지배하고, 압력↑ → Hertz 접촉 수↑·힘사슬 뚜렷. *"힘사슬은 주로 NMC 가 지고, NMC–NMC 힘이 bond 로 전달되는 힘보다 훨씬 크다."*
- Fig 9: x = 입자 **지름**(0–35 µm), y = 접촉력. **같은 x 에 세로로 늘어선 점열** = 한 큰 입자의 여러 접촉(≈ 32 · 25 · 23 · 20 µm 입자들). 저자 결론: *"큰 입자일수록 접촉점이 많고 힘이 커서 파쇄에 더 취약하다 — X-CT 에서도 관측(ref 30)"*. ⚠ 이 추론의 한계는 §12 D7·D7b. [정정 2026-11-16 · 원문 p.12 (그대로): *"For a given external load, larger particles typically exhibit a greater number of contact points and sustain substantially higher contact forces than smaller particles. The resulting interfacial stresses may induce surface defects and crack initiation, making larger particles more susceptible to fracture. In contrast, smaller particles tend to alleviate stress concentration through local rearrangement or sliding. This phenomenon was observed in X-CT, further confirming that larger particles exhibit a higher tendency to fracture during the calendering process.³⁰"* — 인용 30 은 **마지막 문장 (X-CT 에서 큰 입자 파쇄가 보였다) 끝에만** 붙는다 · '접촉점이 많고 힘이 크다' · '작은 입자는 재배열 · 미끄럼으로 응력 집중을 푼다' 는 이 논문 자신의 DEM 서술 (인용 없음) → 옛 요약 *"…힘이 커서 파쇄에 더 취약하다 — X-CT 에서도 관측(ref 30)"* 은 ref 30 의 귀속 범위가 넓다 · ref 30 원문 쪽 내용 = `stershic2015_fabric_tensor_calendering_nmc_xct_dem` §0-1 (그 카드 기록)]
- ★ **판독으로 드러난 작도 규칙**: 최고점들이 **같은 힘 값으로 짝지어** 나온다 — 200 MPa 에서 176.5 mN @ 18.3 · 32.0 µm, 163 mN @ 23.2 · 4.7 µm, 112.7 mN @ 8.9 · 13.8 µm … (30·60 MPa 도 같음, figure-read). ⇒ **각 접촉을 두 입자의 지름에 한 번씩 두 번 찍었다**. 그래서 점 개수 = 접촉 수 × 2 이고, 한 접촉의 **두 입자 크기를 같이 읽을 수 있다** (논문은 이 규칙을 적지 않았다).

### 3.9 응력텐서 대각성분 (Fig 10, pp.12–13; Love–Weber/Christoffersen eq 24)

| 목표 압력 | σ_xx | σ_yy | σ_zz | 등급 |
|---|---|---|---|---|
| 30 MPa | **13.4** | **11.2** | **30.4** | stated |
| 60 MPa | ≈ 35.5 | ≈ 30 | ≈ 66.5 | figure-read ≈ (±1) |
| 200 MPa | **145.6** | **124.1** | **198.5** | stated |

- 저자 해석: 주기경계라 σ_xx ≈ σ_yy 추세가 같고, **~200 MPa 에서 σ_xx 가 σ_yy 보다 약간 커져 "방향 이방성 개시"**, 원인은 실구조 RVE 의 x·y 불균질. σ_zz 는 두께 감소로 항상 면내보다 크다.
- ★ **우리 산술 (§12 D3)**: σ_xx/σ_yy = **1.196 (30) → ≈ 1.18 (60) → 1.173 (200)** — **상대 이방성은 압력 내내 일정**하다. 커진 것은 절대 차(2.2 → 21.5 MPa)뿐 ⇒ "고압에서 이방성이 **시작**" 이 아니라 **RVE 고유의 고정된 직물(fabric) 이방성**이 처음부터 있었다고 보는 편이 자기 수치와 맞는다.
- ★ **측압계수 K = σ_면내/σ_zz**: 평균 **0.40 (30) → ≈ 0.49 (60) → 0.68 (200)** (derived) — 압밀될수록 등방 쪽으로.
- ★ **자기 일관 검사**: σ_zz(RVE 평균) / 목표 = **1.013 (30) · ≈ 1.11 (60) · 0.993 (200)** — 30·200 은 플래튼 응력과 1 % 안, **60 MPa 만 ≈ 11 % 초과**(figure-read; 원인 미기재).

### 3.10 체적에너지밀도 (Fig 12, pp.14–15)

| 압력 (MPa) | W_V (Wh L⁻¹) | 등급 |
|---|---|---|
| 0 | **1422** | stated |
| 30 | ≈ 1650 | figure-read ≈ |
| 60 | ≈ 1770 | figure-read ≈ |
| 100 | ≈ 1917 | figure-read ≈ |
| ~140 | **≈ 2002** (*"approaches approximately 2002"*) | stated (판독 ≈ 2001) |
| 200 | ≈ 2050 | figure-read ≈ |

- 정의 eq (25): **W_V = U·m·q / V**, **U = 3.7 V**, **q = 170 mAh g⁻¹** (ref 41 — 이 논문이 인용한 값), m = RVE 안 NMC 입자 총부피 × 밀도, V = 해당 압력 상태의 **RVE 총부피** — 단면 코팅이라 **집전체 두께의 절반**을 포함 (stated).
- 저자 해석: < 140 MPa 에서 급증, > 140 MPa 에서 **"plateau effect"**. ⚠ 판독상 140 → 200 MPa 에도 **+2.4 %** 더 오른다 — "평탄"이 아니라 "둔화".
- ⛔ **§12 D1 — 이 곡선은 하중 상태의 두께로 계산됐다.** 제하 후 구조로는 30 / 60 / 200 MPa 에서 **≈ 1470 / ≈ 1565 / ≈ 1680 Wh L⁻¹** (derived). 헤드라인 2002 는 전극이 **유지하지 못하는** 상태의 값이다.

### 3.11 SEM (Fig 11, pp.13–14)

- (a) 미압연 단면: Al 박 윗면이 비교적 평평 · (b) **150 MPa** 압연: 박 표면이 **물결치고 국부 압흔** · (c) (b) 확대(5 µm 바): 박에 파고든 입자, PVDF 섬유상 가닥, NMC 이차입자의 1차 결정립이 보인다 · (d) **200 MPa** 압연 전극 윗면: **노란 점선 원**(캡션 설명 없음 — 문맥상 균열/파쇄 입자로 읽힌다).
- ⚠ **150 MPa 는 DEM 에서 돌리지 않은 조건**이다 (DEM = 30/60/200). 정성 비교만.
- 우리 판독(매우 거침): 박 윗면 굴곡 진폭 (a) **≲ 2 µm** · (b) **≈ 5–7 µm** (20 µm 바 ≈ 163 px 로 환산, 단면 원근·절단 아티팩트 미보정 — **TREND only**). DEM 최대 매립 0.937 µm @200 MPa 보다 **자릿수에 가깝게 크다** (§10 L7).

---

## 4. 시뮬레이션 방법 ★ (paper-level 재현 수준)

### 4.1 코드 · 솔버 · 도메인
- **코드**: **미명시 [미확인]** (PFC 계열 어휘 — §2 참조, 추정).
- **RVE**: Ebner 2013 미압연 데이터셋의 부분체적 → **100 × 100 × 75 µm³**. **x·y 주기경계**, 바닥 = Al 집전체(벽), 위 = 강체 플래튼.
- **실현 수**: **1 RVE** — 시드 앙상블·RVE 크기 수렴 검사 **보고 없음**. 최대 입자 지름 ≈ 32 µm ⇒ 측면 100 µm ≈ **3 d_max**.
- **입자 수·시간간격·총 계산시간**: [미확인].

### 4.2 NMC–NMC 접촉: Hertz–Mindlin (eqs 1–6)

```
F^n_ij = (4/3) E* √R* · δ_n^1.5 + 2β √(m* k_n) · δ̇_n                       (1)
F^t_ij = −k_t δ_t + 2β √(m* k_t) · δ̇_t                                      (2)
1/E* = (1−ν_i²)/E_i + (1−ν_j²)/E_j        1/R* = 1/R_i + 1/R_j              (3)(4)
k_n = 2E* √(R* δ_n)                        k_t = 8G* √(R* δ_n)               (5)(6)
```
- **순수 탄성 Hertz** — 항복압(p_y 또는 H) 캡이 **없다**. 겹침 δ 는 소성의 기하 프록시일 뿐, **입자 형상은 변하지 않는다**.
- eq (1)의 감쇠항 부호가 **+** 로 인쇄돼 있다(통상은 −) — 조판 수준의 문제로 보이며 결과에 대한 함의는 판단하지 않는다.
- NMC–Al 벽 접촉도 Hertz(벽 E 68.9 GPa, ν 0.3 이 eq 3 에 들어간다)로 읽힌다 — 명시 문장은 없다.

### 4.3 CBD–CBD · CBD–NMC · 입자–Al: linear parallel bond (eqs 7–21, Fig 1; Potyondy & Cundall 2004 = ref 26)
- 두 메커니즘: ① **유한 크기 선형탄성 접촉**(압축·마찰, 힘만 전달) + ② **결합(bond) 접촉**(힘 + **모멘트** 전달, 상대 회전에 저항).
```
F̄ = −F̄_n n̂_c + F̄_t              M̄ = M̄_t n̂_c + M̄_b                        (7)(8)
F̄_n = (F̄_n)_0 + k̄_n Ā Δδ_n       F̄_t = (F̄_t)_0 − k̄_t Ā Δδ_t               (9)(10)
M̄_t = (M̄_t)_0 − k̄_t J̄ Δθ_t       M̄_b = (M̄_b)_0 − k̄_n Ī Δθ_b              (11)(12)
k̄_n = Ē*/L                          k̄_t = k̄_n/κ̄*                            (13)(14)
σ̄ = F̄_n/Ā + ‖M̄_b‖R̄/Ī            τ̄ = ‖F̄_t‖/Ā + ‖M̄_t‖R̄/J̄                 (15)(16)
R̄ = λ̄·min(R⁽¹⁾,R⁽²⁾) (ball-ball)  ·  λ̄·R⁽¹⁾ (ball-facet)                    (17)
Ā = πR̄²     Ī = ¼πR̄⁴     J̄ = ½πR̄⁴                                           (18)(19)(20)
bond 생성:  ‖O⁽¹⁾ − O⁽²⁾‖ ≤ R⁽¹⁾ + R⁽²⁾ + ξ̄·D_c ,  ξ̄ = 1.5                   (21)
```
- **L** = bond 길이 (Fig 1 에 회색 bond 원기둥의 길이로 그려져 있고 본문 정의는 없다).
- **파단 판정**: 피크 법선응력 σ̄ (eq 15) 와 피크 전단응력 τ̄ (eq 16) 을 강도와 비교 — 본문에 인장강도 σ̄ 만 값(3.6 × 10⁷ Pa)이 있고 **전단강도 c̄ 값은 없다** [미확인]. *"법선·접선 파라미터를 같은 전략으로 설정"* (p.7) 이 **c̄ = σ̄ · κ̄* = 1** 을 뜻하는지는 **추정**이다. [보강 2026-11-16 · 원문 p.4: 식 15 · 16 은 *"The peak normal stress σ̄ and peak shear stress τ̄ acting on the parallel bond are determined using the Eqs. 15 and 16"* 까지만 — 이 응력을 강도와 견주는 파단 판정 문장 · 파단 뒤 처리 (bond 삭제 여부) 는 원문에 없다 (PFC parallel bond 관례로 읽은 것 [추정]) · 강도 값은 p.7 *"the bond strength (σ̄_Particle-Particle) was set to 3.6 × 10⁷ Pa"* 하나]
- **ξ̄ = 1.5** 는 *"모든 입자가 결합돼 떨어진 입자가 없도록"* 고른 값 (stated) — 즉 **초기 상태에서 CBD 망이 전 입자를 한 덩어리로 묶는다**.
- ⚠ **λ̄ = 2** 이면 bond 반지름이 **작은 입자 반지름의 2배**(벽에 붙은 입자는 자기 반지름의 2배)다 — bond 원판이 입자 단면보다 크다. 인장 파단력은 σ̄·Ā ∝ σ̄·λ̄² 이므로 **σ̄ 와 λ̄ 는 (인장 항에 대해) 서로 대체**된다 ⇒ **σ̄ = 36 MPa 를 재료 물성으로 읽으면 안 된다** (§10 L4).

### 4.4 ★★ 입자 처리 (우리 "무질서 처리"의 DEM 대응) — **강체 구 · 순수 탄성 접촉 · 형상소성 0**
- **NMC**: X-CT 분할(Ebner)의 **입자별 좌표·부피 → 같은 부피의 구**. 근거: *"NMC 입자가 매우 구형이라"* (stated). 실제 SEM(Fig 11c)은 1차 결정립이 뭉친 **울퉁불퉁한 이차입자**다.
- **PSD**: X-CT 가 주는 **실제 다분산**(반지름 ≈ 0.5–16 µm) — mono/bimodal 설계가 아니라 **측정 분포 그대로**.
- **CBD**: 실제 형상·넓은 크기분포를 **2.2 µm 단일 구**로 단순화(계산비용). *"주 기능은 입자간 점착과 기계적 구속"* 이라는 이유.
- **변형의 층위**: NMC–NMC = **탄성 CONTACT(Hertz)** — Thornton–Ning/EEPA 같은 **접촉 소성조차 없다**. 비가역성은 ① bond **취성 파단** ② 마찰 미끄럼·재배열 뿐 ⇒ **영구 압밀(제하 후 남는 공극 감소)은 구조 재배열이 bond·마찰에 잠긴 것**이지 입자 소성이 아니다.
- **집전체**: 변형하지 않는 **벽**. "매립" = 겹침 프록시.

### 4.5 ★ 캘린더링 프로토콜 — **롤이 아니라 평판이다**
- *"top was set as a rigid platen to simulate the roller"* (p.4, ref 19 방식). **속도 구동 0.01 m s⁻¹** 로 하강하며 **매 시간스텝 플래튼 응력**을 계산 → **목표 압축응력 도달 시 정지 → 같은 속도로 상승(제하, 탄성회복)** (pp.4–5).
- 즉 **정지 = 응력 도달 순간의 변위 정지** 후 곧바로 **후퇴**. 목표 응력에서의 **유지(dwell)는 없다**. 롤 곡률·전단(ref 21 Sonzogni 가 다룬 것)은 **없다**.
- 준정적성 (derived, §12 D8): 마하수 v/c ≈ **1.8 × 10⁻⁶** (c = √(E/ρ) of NMC) ~ **3 × 10⁻⁵** (bond 급 강성 추정) · 관성수 I ≈ **2 × 10⁻⁵ (30 MPa)** ⇒ 준정적 영역.

### 4.6 보정 절차 (pp.5–7)
1. **σ̄_Particle-Al** — 박리 피크(0.0347 MPa)에 맞게 **반복 보정** → 7.2 × 10⁴ Pa. 보정 구조(몇 MPa 로 압연한 DEM 구조인지)·DEM 박리의 경계조건(무엇을 당겼나)은 **미기재** [미확인].
2. **Ē*, σ̄_Particle-Particle, λ̄** — *"거시 기계응답이 실험과 잘 맞도록"* 조정 → 0.3 GPa / 3.6 × 10⁷ Pa / 2. ⚠ **어떤 실험량이 표적이었는지 미기재** — 공극률이라면 **그 공극률이 곧 검증 표적(Fig 4c)** 이다 (§10 L4).
3. **검증**: 제하 후 공극률 **4점**(0/30/60/200 MPa) vs 실험 (Fig 4c) + Ebner 데이터(ref 22) 와도 비교했다고 쓰지만 **그림에는 실험 계열이 하나뿐**이다.

### 4.7 수송 (transport) — **없다**
- σ_ion · σ_e · κ 계산 **0건**. *"치밀화는 전자 경로를 개선한다"*, *"접촉면적↑ → 계면저항↓"* 는 전부 **정성 논증**.

### 4.8 ⛔ 미기재 목록 (재현 불가 지점)
코드명 · 입자 수(NMC·CBD) · 시간간격 · κ̄* · c̄ · CBD 재료물성(E·ν·ρ·마찰) · 벽 마찰 · 감쇠 정의 · 공극률 계산 관례(겹침 부피 처리) ·
DEM 박리 시뮬 설정 · 보정 표적 · 실험 캘린더링 방법·조건 · 실험 공극률 측정법 · 전극 두께·로딩 · SEM 장비 · 시험기 모델 · Fig 5·6·7 이 하중 중인지 제하 후인지.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | linear parallel bond 모식 — 두 구 R⁽¹⁾·R⁽²⁾ 사이 bond 원기둥(회색, 길이 L), 법선력 F̄_n · 접선력 F̄_t · 모멘트 M̄ | CBD bond 청사진(backlog A3). 모멘트 전달 bond 의 정의도 — ref 27 Lyu 2025 카드 Fig 1 과 같은 계열 |
| 2 | 구조 생성: (a) Ebner X-CT 이진화 단면(흰 = NMC) (b) 같은 단면의 구 근사 (c) DEM RVE — 빨강 NMC · 청록 CBD · 위 플래튼 · 아래 집전체 (d) **누적 부피분율 vs 입자 반지름** | ★ **reconstruct-then-compress** 의 입력 단계가 한 장에. (d) 의 x축이 **반지름**이라는 것이 D-값 해석의 열쇠 (§3.3) |
| 3 | (a) 박리 모식 — **위아래 순간접착제 + 수직으로 당김** (b) 박리응력 vs 무차원 시간: 실험(검정, 오목) vs DEM(빨강, 직선) — 피크 0.0347 vs 0.0349 MPa | ★ 입자–집전체 bond 의 **강도 보정** 선례. ⚠ 시간축 무차원화 → **에너지(G_c) 비교 불가**. 우리 §I 박리 트랙의 대조 사양 |
| 4 | (a) 0/30/60/200 MPa RVE 측면 (b) **공극률 vs 압력 — 세 런의 가압·제하 루프**(범례 없음) (c) **제하 후** 최종 공극률 DEM vs 실험 | ★★ 하중 중 vs 제하 후를 **한 그림에서** 볼 수 있는 드문 자료 — 우리 at-load 공극률 해석의 경고등 (§8 ①) |
| 5 | ΔFSA 막대(좌축) + 배위수 점선(우축) @30/60/200 MPa | FSA_p 정의(ref 19)·CN = N_c/N_p 정의 확인용. **Z 로 쓰려면 ×2** |
| 6 | 집전체 표면의 NMC 매립 깊이 지도 (a) 30 (b) 60 (c) 200 MPa, 공통 컬러바 0–0.940 µm | 우리 STEP3 집전체 접촉 밴드 · R_collector 와 대응하는 **공간 지도** 형식. ⚠ 값은 탄성 겹침 |
| 7 | 집전체–NMC 접촉면적 막대 @30/60/200 MPa (≈113/198/490 µm²) · y축 라벨 오타 *"paticles"* | 발자국 대비 1.1 → 4.9 % — 집전체 접촉이 **극히 희박**하다는 규모 감각 |
| 8 | 30/60/200 MPa 힘사슬 망 — 빨강 Hertz–Mindlin, 청록 bond, 굵기 ∝ 힘 (범례·힘 척도 없음) | 하중이 **bond 망 → NMC 직접 접촉**으로 넘어가는 전환의 시각 증거. 우리 AM 하중분담 서사와 같은 질문 |
| 9 | NMC 입자별 접촉력 vs 입자 지름 산점도 (a) 30 (b) 60 (c) 200 MPa — **각 접촉이 두 입자 지름에 한 번씩 두 번 찍힘**(판독) | ★ 최대 ≈24.7/43/177 mN. **힘 ≠ 파괴 위험** — P_f/D²(Wheatcroft)·Auerbach(F_c ∝ R) 같은 크기 정규화가 필요 (§12 D7·D7b) |
| 10 | RVE 응력텐서 대각성분 σ_xx·σ_yy·σ_zz 막대 @30/60/200 MPa | ★ σ_zz ≈ 인가 압력(자기 일관 검사) · 측압계수 K 0.40 → 0.68 · σ_xx/σ_yy 일정 (§12 D3) |
| 11 | SEM: (a) 미압연 단면 (b) 150 MPa 단면 (c) (b) 확대 (d) 200 MPa 윗면(노란 점선 원) | 실제 Al 박의 **소성 굴곡**(수 µm) vs DEM 탄성 겹침(<1 µm) — 모델 한계의 실험 증거 |
| 12 | 체적에너지밀도 vs 압력 (1422 → ~2002 @140 → ≈2050 @200 Wh L⁻¹) | ⛔ **하중 상태 값** (§12 D1). 인용 시 반드시 "under load" 한정 |
| Table 1 (원문 Table I) | NMC 입력 파라미터: E 142 GPa · ν 0.25 · 마찰 0.12 · 밀도 4750 kg m⁻³ · 감쇠 0.95 (refs 27, 29–31) | E_AM 142 ≈ 우리 140 (둘 다 연화 안 한 실측 계열) |

### 5.1 크롭 검수 원장 (2026-09-26, 13장 전부 육안 확인)

| 파일 | 자동 크롭 상태 | 조치 | 원본 래스터 결함 (크롭으로 복구 불가) |
|---|---|---|---|
| `fig_1.png` | **본문 식 (7)·(8) 과 단 구분선이 섞임** | 임베디드 래스터 경계(xref 29) ± 1.5 pt 로 재크롭 | — |
| `fig_2.png` | 쪽 너비 띠 (내용 완전) | 래스터 경계로 조임 | — |
| `fig_3.png` | 좌우 여백 ≈ 65 pt | 래스터 경계로 조임 | (a) 두 모식 아래 **흐린 회색 얼룩** |
| `fig_4.png` | 쪽 너비 띠 (내용 완전) | 래스터 경계로 조임 | (b) **범례 없음** — 세 색 곡선의 의미는 우리 해석 (§3.5) |
| `fig_5.png` | **쪽 구분선이 위에 섞임** + 넓은 여백 | 재크롭 | — |
| `fig_6.png` | **쪽 구분선이 위에 섞임** | 재크롭 | — |
| `fig_7.png` | 좌우 여백 ≈ 65 pt | 재크롭 | y축 라벨 오타 *"paticles"* |
| `fig_8.png` | 좌우 여백 ≈ 65 pt | 재크롭 | **색 범례·힘 척도 없음** (의미는 본문에만) |
| `fig_9.png` | 쪽 너비 띠 (내용 완전) | 래스터 경계로 조임 | — |
| `fig_10.png` | 좌우 여백 ≈ 65 pt | 재크롭 | — |
| `fig_11.png` | 쪽 너비 띠 (내용 완전) | 래스터 경계로 조임 | (d) 노란 점선 원 — **캡션 설명 없음** |
| `fig_12.png` | 좌우 여백 ≈ 65 pt | 재크롭 | — |
| `tab_1.png` | **추출 0건** (로마숫자 "Table I" — 도구는 아라비아 숫자만 인식) | 5쪽 벡터 텍스트 표를 **윗 굵은 괘선 + 캡션 … 아래 괘선** 으로 수동 크롭 | — |

⚠ **재추출 주의**: `extract_figures.py --slug … --clean` 을 다시 돌리면 쪽 너비 크롭이 돌아오고 `tab_1.png` 가 사라진다. 기록 = `figures.json` 의 `recrop` / `manual_crop` / `note` + `litdb/pdf_map.tsv` 주석.

---

## 6. Post-processing ★ — 무엇을 어떻게 수치화했나

| 지표 | 정의 | 어떻게 보고 | 우리 대응물 |
|---|---|---|---|
| 공극률 | 정의식 없음 — **겹침 부피 처리 관례 미기재** [미확인] | 가압–제하 연속 곡선(Fig 4b) + 끝점(Fig 4c) | ε_sphere (구 부피 합) 통일 규율 |
| FSA_p (eq 22) | (4πr_p² − Σ A_c,i) / (4/3 πr_p³) — 입자 표면에서 접촉면적 합을 뺀 자유표면 ÷ 부피 (ref 19 정의) | 전체 FSA + ΔFSA (eq 23) 막대 | 우리 coverage(AM 표면 중 SE 접촉 분율)의 **여집합** 개념 |
| 배위수 | N_c(NMC–NMC) / N_p(NMC) | Fig 5 우축 | 우리 CN (정의 대조 선행 — §8 ⑥) |
| 매립 깊이 | 미정의 (겹침으로 해석) | 보간 등고선 지도 (Fig 6) | — |
| 집전체 접촉면적 | 미정의 (Hertz 면적 합으로 추정) | 막대 (Fig 7) | STEP3 집전체 접촉 밴드 |
| 힘사슬 | 접촉·bond 선분, 굵기 ∝ 힘 | 3D 렌더 (Fig 8) | DEM 고유(frame[5]) |
| 입자별 접촉력 | 입자 지름별 접촉력 산점 | Fig 9 | Auerbach 판정 입력 |
| 응력텐서 (eq 24) | σ = (1/V) Σ_c F^(c) ⊗ L^(c) (Christoffersen 1981 = ref 39; Love–Weber 형) | 대각성분 막대 (Fig 10) | 우리 DEM `c_strs` / phase-virial `f_AM` · MPM 응력장 |
| 체적에너지밀도 (eq 25) | U·m·q/V, V 에 집전체 두께 절반 포함 | 연속 곡선 (Fig 12) | (없음 — 우리는 용량 grade 축) |
| 박리응력 | 힘/면적, 시간 무차원화 | 곡선 (Fig 3b) | §I DEM 박리 트랙 (G = (F/b)(1 − cos θ)) |

- 도구: 명시 없음. 통계(오차막대·반복)는 **박리 시험 3회**에만 있고, DEM 쪽은 **단일 런** 값이다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⚠ 정본 `litdb/our_dem_baseline.md` 는 **값이 없는 자리표시**다(2026-09-09). 아래 "우리" 열의 수치는 **CLAUDE.md(규범·정본)** 에 적힌 값을 인용한 것이고,
> 그 파일이 승격되기 전까지 **이 브랜치에서 파일로 대조할 수 없다**.

| 축 | 이 논문 (Zhang 2026) | 우리 | 판정 — **진짜 차이 vs 방법 인공물** |
|---|---|---|---|
| **소재계** | NMC111 + CBD(PVDF/CB), **SE 없음**, 액체계 LIB | LPSCl SE + NMC811 (+VGCF/PTFE/SDCP), ASSB | ⛔ **값 전이 불가.** 공극의 역할이 정반대(그들: 전해액 통로 / 우리: 죽은 부피). porosity 절대값을 나란히 놓지 말 것 |
| **(1) 입자 탄성률** | **E_NMC 142 GPa 그대로**(연화 없음) · 대신 **CBD bond Ē* 0.3 GPa** 가 보정된 유연상 | **E_AM 140 GPa 그대로** · **E_SE 24 → 1.35 GPa (18배 연화, DEM)** · MPM 1.53 GPa + ν 0.49 | ★★ **같은 인식론의 LIB 판이다.** 둘 다 "강체 AM + **보정된 유효 탄성률을 가진 유연상**" 구조이고, 유연상의 유효 모듈러스는 거시 압밀에 맞춘 **lumping** 이지 측정 물성이 아니다(frame[2]). 대상 상이 다를 뿐(그들 CBD bond / 우리 SE) ⇒ ⛔ **0.3 vs 1.35 를 숫자로 비교하지 말 것** — 하나는 bond 원판의 모듈러스, 하나는 Hertz 접촉의 모듈러스 |
| **(2) 접촉법칙** | NMC–NMC **Hertz–Mindlin (탄성, 항복 캡 없음)** | LIGGGHTS **hooke/hysteresis** + **Stage-E**(Tabor F/H · volume 캡) 사후 면적 보정 | 같은 **no-cap 층**. 우리는 Stage-E 로 소성 **면적**을 따로 보정하고 그들은 없다 — §12 D7 이 보이듯 그들 접촉의 일부는 **H_NMC 를 넘는 면압**을 탄성으로 버틴다 |
| **(2) bond / 바인더** | **CBD 를 2.2 µm 구로 명시 + linear parallel bond(힘+모멘트, 취성 파단)** + **입자–Al bond** | PTFE/VGCF 는 STEP2/3 의 **부피·전도 격자**에만 있고 **기계 기여 0** (PTFE centerline 스탬프 규약), 명시 bond **없음** (backlog A3) | ★ **그들이 앞선다(구조적 바인더 기계).** 단 그들 bond 는 **취성 선형**이라 PVDF 의 점탄소성·섬유 연신(Fig 11c)은 없다. 우리 건식 PTFE 섬유망엔 Lyu(ref 27) 의 모멘트-bond + 재형성 결합이 더 가깝다 |
| **(3) 보정 표적** | σ̄_Particle-Al ← **박리 피크 1점** · (Ē*, σ̄, λ̄) ← *"거시 기계응답"*(표적 미기재) · 검증 = **제하 후** 공극률 4점 | E_eff ← **porosity @300 MPa** (real_14) + pure-SE Cronau 겹침 11–12 % · MPM σ_y ← Minnmann pure-SE 10 % @300 [정정 2026-11-16 · 우리 쪽: 'Minnmann 순수 SE 10 % @300' 귀속은 CLAUDE.md 원장 `CL-94` (2026-10-03) 로 출처 철회 — 10 % 는 우리 MPM 보정 표적 (외부 앵커 아님) · 지금 기준 = 랩 표준 순수 SE 기공률 10–13 % (고정 · 판정하지 않음)] | ★ **그들은 다압력 검증점 4개가 있다**(우리 복합 침대엔 없음 — 우리 다압력 Heckel 은 pure-SE DEM). ⚠ 반대로 그들 **보정/검증 분리가 불명**하고 **박리 <1 % 는 보정 잔차**다 |
| **(4) 응력·힘사슬** | Love–Weber 대각성분(σ_zz ≈ P 로 자기 일관) · 힘사슬 렌더 · 입자별 힘 산점 | DEM AM-AM 하중분담 **0.517/0.598/0.675/0.620** (P = 100/200/300/600) · phase 규약 **0.726/0.768/0.794/0.763** · MPM 응력장 | 그들 전환 서사(**bond 지배 → NMC 직접 접촉 지배**)는 우리 AM 골격 하중분담 증가와 **같은 방향의 정성**. ⛔ 수치 비교는 불가(그들엔 SE 상이 없다) |
| **(4) AM 파괴** | **모델 없음** — "큰 입자일수록 힘이 커서 더 취약" (힘 기반 정성) + SEM 정성 | **Auerbach** 파괴 판정 + `f_intact`·`frac_severe` 가 σ 에 되먹임 | ★★ **우리가 앞선다.** 그리고 D7: 같은 힘이면 큰 입자의 면압이 **낮다** — 크기 효과는 Auerbach(F_c ∝ R) · Wheatcroft P_f/D² 같은 **크기 정규화 기준**이 있어야 판정된다. D7b: 그렇게 정규화하면 가장 과응력인 것은 **작은** 입자 쪽이다 |
| **(5) 입자 형상** | **X-CT → 등가 구**(실제 좌표·부피·PSD, 형상은 구) | DEM 생성 패킹(구) · MPM scaffold 는 **DEM 압밀 후 AM 좌표**를 얼린다 | 둘 다 **구**. 그들의 가치는 **초기 배치가 실측**이라는 점 — 우리 scaffold 의 순환성(씨앗이 DEM 정답을 담는다, CLAUDE.md 정정 2026-08-12)을 끊을 **독립 초기구조 경로**의 선례 (§8 ⑤) |
| **(6) 공정** | **캘린더링을 평판으로 근사** · 속도 구동 0.01 m s⁻¹ · 도달 즉시 정지 → **제하** | **단축 냉간압착 300 MPa** · DEM 서보 / MPM `hold`(도달 후 고정·이완) · `servo` · **제하 없음** | ⚠ 둘 다 결국 평판 단축이라 **프로토콜 수준 비교는 선다**. 차이는 ① 그들은 **제하까지** 푼다(우리 F-SB1 공백) ② 우리는 dwell/hold 가 있다 ③ 압력창 30–200 vs 300 |
| **(6) 액체 LIB vs 황화물 ASSB** | 공극 = 이온 통로, CBD = 전자 경로, 캘린더링 후 **자유 상태** | 공극 = 결손, SE = 이온 경로, 운전 중 **적층압**(수–수십 MPa) | ★ D2: 그들 DEM 에서 **회복의 절반이 5 MPa 아래**에서 일어난다 ⇒ **적층압 아래 ASSB 전극은 자유 상태보다 훨씬 치밀하게 남을 수 있다** — 방향만 전이, 크기는 전이 금지 |
| **재하율** | Mach ≈ 1.8 × 10⁻⁶ – 3 × 10⁻⁵ (derived) | MPM `--platen-mach` 기본 0.03, real_14 V/c_S 0.22–0.75 | 그들이 준정적성은 낫다 (He 2026 과 같은 결론) |
| **수송** | **없음** | Kirchhoff/Holm 접촉망 + STEP3 복셀 FV 삼중항 | ✅ 우리 완승. 이 논문은 역학 전용 |
| **porosity 관례** | 미기재 | ε_sphere 통일 | ⚠ 하중 중 0.152 는 겹침 관례에 따라 달라질 수 있다 |
| **RVE·통계** | 1 RVE, 시드 없음, 측면 ≈ 3 d_max | 다중 시드 · prereg 판정선 | 우리가 앞선다 (§10 L10) |

### 7.1 frame[5] 위치
- **이 논문이 가진 반쪽**: DEM 역학·패킹 — 재배열, bond 망 → 접촉망 하중 전환, 힘사슬, RVE 응력텐서, 집전체 접촉.
- **없는 반쪽**: ① DEM 의 **수송**(Kirchhoff/Holm σ 삼중항) ② MPM 의 **형상 소성·void-fill·소성 변형장** ③ AM **파괴**.
- **frame[4] 관점**: 그들의 DEM 은 **자기 실험에 보정**됐고(박리·공극률), 우리 모델과 교차보정할 대상이 아니다. 쓸 수 있는 것은 **방향·구조·방법**이다.

### 7.2 전이 가능 / 불가능 — 한 장 요약

| ✅ 전이 가능 (방법·구조·방향) | ⛔ 전이 불가 (값) |
|---|---|
| 하중 중 vs 제하 후 공극률을 **구분해서** 보고해야 한다는 규율 | 공극률 절대값(0.432/0.333/0.411…) · springback 크기 |
| 회복이 **저압 구간에 몰린다**는 제하 곡선 모양 → 적층압 효과의 방향 | W_V 1422–2050 Wh L⁻¹ |
| RVE σ_zz ≈ 플래튼 응력 **자기 일관 검사** · 측압계수 K 를 기술자로 | E_NMC 외 모든 보정값(Ē*, σ̄, λ̄, σ̄_Particle-Al) |
| 입자–집전체 bond 를 **거시 점착 측정**에 묶는 보정 절차 | 매립 깊이 0.4/0.937 µm (탄성 겹침) · 접촉면적 113/198/490 µm² |
| 힘 → 파괴 판정에는 **크기 정규화**가 필요하다는 교훈 | 접촉력 7.3/177 mN (소재·E·PSD 종속) |
| X-CT 좌표를 **독립 초기구조**로 쓰는 경로 | FSA·CN 절대값 (정의·소재 종속) |

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

### ① ★★★ "하중 중 값" 과 "제하 후 값" 을 섞지 말 것 — 우리 at-load 공극률의 경고등
- 우리 DEM(서보)·MPM(`hold`) 공극률은 **압력이 걸린 상태** 값이고, 실험 공극률은 대부분 **다이 밖(제하 후)** 값이다. CLAUDE.md 가 이미 *"그들 ε 는 springback 후(out-of-die)라 in-die Heckel 인 우리 P_y = 138 과 같은 양이 아니다"* 라고 적었다.
- 이 논문은 **같은 모델 안에서** 그 차이의 크기를 보여준다: 200 MPa 하중 중 **≈ 0.152** vs 제하 후 **≈ 0.319** (figure-read) — ≈ 0.17 차. 그리고 **W_V 헤드라인이 하중 중 값**이라, 200 MPa 에서 하중 중 ≈ 2,050 이 제하 후 구조의 ≈ 1,680 Wh L⁻¹ 보다 **≈ 22 % 크다** (D1).
- ⇒ 우리 산출물에 **"at-load" 라벨을 상주**시키고, 실험 대조 때 상대가 in-die 인지 out-of-die 인지를 **먼저** 적는다. 크기는 전이하지 않는다(그들 회복은 취성 bond + 탄성 Hertz 의 산물 — 우리 SE 는 소성이라 회복이 훨씬 작을 것으로 **예상**만 한다; 우리 `--protocol release` 팔은 미실행, F-SB1).

### ② ★★ 적층압 아래 ASSB — 회복이 저압에 몰린다는 모양은 전이된다
- 그들 제하 곡선: 200 MPa 런이 **5 MPa 에서 ε ≈ 0.236**, 0 MPa 에서 0.319 (figure-read). 회복의 **절반가량이 5 MPa 아래**.
- ASSB 는 운전 중 적층압(수–수십 MPa)이 걸린다 ⇒ **"제조압 제하 후 공극률" 이 아니라 "적층압 하 공극률" 이 운전 구조**다. 이 모양(Hertz 류 비선형 제하)은 소재와 무관한 **접촉역학의 형태**라 방향은 전이된다. 크기는 우리 모델로 직접 재야 한다 — 우리 DEM 에 **제하 → 적층압 유지** 팔을 두는 것이 가장 싼 확인.

### ③ ★★ 입자–집전체 점착 보정의 선례 — 단 **강도 보정 ≠ 인성 보정** (§I 박리 트랙과 연결)
- 그들은 **피크 응력 한 점**에 bond 강도를 맞췄다. 실험 곡선은 오목(소산이 있다), DEM 은 직선(취성 선형 bond) — **피크는 같아도 곡선 아래 면적(에너지)은 다르다**. 시간축이 무차원이라 G_c 는 원리적으로 못 낸다.
- 우리 §I 트랙의 전제 *"W_ad ≠ G_c"* 에 한 줄을 더한다: **"피크 강도 ≠ G_c"**. 우리 DEM 박리는 **피크 응력 + G(F/b·(1 − cos θ)) + 파괴 위치**를 함께 기록해야 비교가 선다.
- ⚠ 식별성: 인장 파단력 ∝ σ̄·λ̄² ⇒ 한 점 보정으로는 σ̄ 와 λ̄ 를 가를 수 없다. 우리가 sjkr/bond 를 보정할 때도 **"무엇이 식별되는가"** 를 먼저 적는다.

### ④ ★ 싸게 얻는 자기 일관 검사 두 개
- **RVE 응력 σ_zz(Love–Weber) ÷ 플래튼 응력** — 그들 30·200 MPa 에서 1 % 안. 우리 DEM `c_strs[3]` 합 / 벽 반력, MPM `sigzz` / `wallP` 에 같은 검사를 **상주 selftest** 로 둘 수 있다 (MPM 은 CLAUDE.md 기록상 ν = 0.49 에서 wallP ≈ 부피평균 σ_zz 를 이미 확인했다).
- **측압계수 K = σ_면내/σ_zz** — 그들 0.40 → 0.68. 우리 MPM(J2, ν_SE 0.49) 과 DEM 이 **각자** 내는 K 를 새 비교 기술자로 쓸 수 있다(frame[4] — 서로 맞추지 않고 차이를 정량 한계로 읽는다).

### ⑤ ★ X-CT 좌표 = scaffold 순환성을 끊는 독립 초기구조 경로
- CLAUDE.md 2026-08-12 정정: MPM scaffold 의 SE 씨앗이 **DEM 압밀 후 좌표**라 *"porosity 일치는 순환"* 이다. 이 논문은 **실측 좌표(X-CT)** 를 DEM 초기구조로 썼다.
- ⇒ 우리에게 **복합양극 X-CT 분할 데이터**가 생기면 AM 골격을 **DEM 이 아닌 측정**에서 가져올 수 있다 — 그때 MPM 결과는 DEM 과 **독립**이 된다. ⚠ 황화물 전극은 측정 자체가 구조를 바꾼다는 경고(YMLee26 덱, 정본 미확보)가 있어 **실행 가능성은 미정** — 경로로만 기록.

### ⑥ 배위수 정의부터 맞출 것
- 그들 CN = N_c/N_p (한 번씩 셈) = 통상 Z 의 절반. 같은 계보의 Sangrós 2019 도 같은 정의, He 2026 카드는 Z 를 **파생**으로 복원했다. ⇒ 문헌 CN 을 우리 CN 과 **같은 줄에 놓기 전에 정의를 먼저 확인**한다 (우리 CN 정의는 이 카드에서 재확인하지 않았다).

---

## 9. 인용 가능 문장 (deck/paper용)

- "Zhang et al. (JOM 2026) calibrated the particle–current-collector bond strength of an X-ray-tomography-based DEM of an NMC111 cathode to a measured pull-off peak stress (0.0347 MPa; bond strength 7.2 × 10⁴ Pa) and reproduced the post-unloading porosity after 30 MPa calendering (0.411 vs 0.412)." — **stated 값만**.
- "In the same model the porosity under load at 200 MPa (≈0.15, read from Fig. 4b) relaxes to ≈0.32 after unloading (Fig. 4c), illustrating that at-load and out-of-die porosities are not interchangeable." — ⚠ figure-read 값, **"≈" 와 그림 번호를 떼지 말 것**.
- ⛔ **쓰지 말 것**: *"calendering raises the volumetric energy density to 2002 Wh L⁻¹"* 를 전극 물성처럼 — **하중 상태 값**이다 (D1).
- ⛔ **쓰지 말 것**: *"stress anisotropy develops at high calendering pressure"* — 그들 수치로는 상대 이방성이 일정하다 (D3).

---

## 10. 주의 / 한계 (over-claim 방지) — **비판적으로**

- **L1 · 소재계.** NMC111 + CBD 액체계 LIB. SE 가 없어 우리 복합 침대의 **AM–바인더 골격 극한**일 뿐이다. 공극 목표의 부호가 반대.
- **L2 · 재현 불가 수준의 미기재** (§4.8). 코드명조차 없다. κ̄*·c̄·CBD 물성이 없으면 같은 모델을 다시 세울 수 없다.
- **L3 · 구조와 실험이 다른 전극이다.** DEM 초기구조 = **Ebner 2013 의 전극**(조성 미기재 [미확인]) · 실험 = **자체 NMC111 96:2:2**. DEM 은 CBD 비율만 자체 조성(96:4)으로 맞췄다. Fig 4c 의 "Experiment" 가 **자체 측정인지 Ebner 값인지** 그림·본문이 가르지 않는다(본문은 둘 다와 비교했다고 쓰는데 계열은 하나). 실험 캘린더링 방법·공극률 측정법 **미기재**.
  (0/30/60/200 MPa 라는 압력 집합이 Ebner 데이터셋의 압밀 조건과 같은지는 **[미확인]** — Ebner 원문 미보유.) [보강 2026-11-16 · 원문 대조: Zhang 원문 (p.2–4 · p.8 · 그림 캡션 전수) 은 Ebner 전극의 조성 · 압연 압력을 적지 않는다 → 이 카드 안에서는 '원문에 없음' 으로 닫는다 · 값은 다른 카드 `ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation` 의 기록 (NMC : C65 : PVDF = 96:2:2 · 94:3:3 · 92:4:4 · 90:5:5 × 0 · ≈300 · ≈600 · ≈2000 bar — 이 PDF 로 확인한 것 아님) · Fig 4c 'Experiment' 계열이 자체 측정인지 Ebner 값인지도 Zhang 원문이 가르지 않는다 (p.8 *"…compared with the experimental data reported by Ebner et al."* + 그림은 한 계열)]
- **L4 · 보정과 검증이 분리되지 않았다.** 박리 < 1 % 는 **보정 잔차**다(피크에 맞춰 반복 보정했다고 스스로 쓴다). (Ē*, σ̄, λ̄) 의 표적은 *"거시 기계응답"* — 그게 공극률이면 30 MPa 의 0.411 vs 0.412 는 검증이 아니라 보정 결과일 수 있다. λ̄ = 2 이면 bond 단면적 Ā 가 4배라, 인장 파단력 σ̄·Ā 와 법선 bond 강성 k̄_n·Ā = Ē*·Ā/L 이 **모두 λ̄² 에 곱해진다** ⇒ **σ̄ = 36 MPa · Ē* = 0.3 GPa 는 물성이 아니라 이 λ̄ 에 묶인 유효값**이다 (모멘트 항은 λ̄ 의 다른 거듭제곱이라 완전한 퇴화는 아니다).
- **L5 · 박리값의 내부 불일치와 시험 정의.** 0.17 ± 15 % MPa vs 0.0347 ± 0.0032 MPa (≈ 4.9배). "± 15 %" 와 "± 0.0032(≈ 9 %)" 도 맞지 않는다. Fig 3a 는 **수직 인장(pull-off)** 배치인데 본문은 *"prescribed angle"* 의 박리라 한다(각도 미기재). 비교 맥락: 정본 `sangros2020_*` 카드의 NMC 코팅 pull-off 접착강도는 **≈ 1.78–2.78 MPa**(그 카드 digitized, 다른 전극·다른 방법) — 이 논문 값보다 **10–80배** 크다. 어느 쪽이 맞는지 판단할 근거는 없고, **이 논문의 박리 수치는 정의가 확정될 때까지 절대값 인용 금지**.
- **L6 · 헤드라인의 대부분이 하중 상태 값.** W_V(확정, D1) · 응력텐서(σ_zz ≈ P 로 확정) · FSA/CN(시사) · 매립·접촉면적(탄성 겹침이면 하중 중일 수밖에 없다). 전극이 유지하는 상태(제하 후)로 검증된 것은 **공극률 하나뿐**이다.
- **L7 · "집전체 변형"을 모델이 표현하지 못한다.** 벽은 변형하지 않고, Hertz 접촉은 탄성이다 ⇒ "매립 깊이 0.937 µm" 는 **탄성 겹침**이지 소성 압흔이 아니다. 실제 SEM 굴곡은 수 µm 급(판독 거침)으로 **자릿수 가깝게 크다**. 벽 Hertz 로 환산하면 0.937 µm 겹침의 평균 면압은 **≈ 5–12 GPa**(입자 반지름 16–3 µm, derived) — Al 이 탄성으로 버틸 수 있는 수준이 아니다(Al 항복값은 이 논문에 없음). ⇒ 매립 지도는 **"어디가 세게 눌리나"의 정성 지도**로만.
- **L8 · 이방성 해석.** "200 MPa 에서 이방성 개시" 는 자기 수치와 어긋난다 — σ_xx/σ_yy 1.196 → 1.173 로 **상대값 일정** (D3). 원인도 저자가 스스로 제시한 **RVE 유한 크기·직물**이 더 설득력 있다.
- **L9 · "큰 입자가 더 잘 깨진다" 는 이 모델이 판정하지 못한다.** 파괴 모델이 없고, 힘만 봤다. 같은 177 mN 에서 16–16 µm 쌍의 Hertz 평균면압 ≈ 9.7 GPa, 6–6 µm 쌍 ≈ 18.6 GPa (D7) — **힘이 크다고 면압이 큰 것이 아니다**. 정본 Wheatcroft 2023 의 σ_F = P_f/D² 로 정규화하면 가장 과응력인 것은 **큰 입자에 끼인 작은 입자**다 (D7b, 방향 감각만). X-CT 관측으로 확인됐다는 근거는 ref 30 (원문 미확인). SEM Fig 11d 의 원은 캡션 설명이 없다. [보강 2026-11-16: ref 30 원문 카드 = `stershic2015_fabric_tensor_calendering_nmc_xct_dem` (그 카드 §0-1 기록: CT 큰 입자 파쇄 = 정성 그림 한 장 · '힘이 크다' · 크기별 접촉 수 통계 없음) · Zhang 원문의 ref 30 귀속 범위 = §3.8 L222 정정 표지]
- **L10 · 단일 RVE, 시드 없음, 측면 ≈ 3 d_max.** 수렴 검사 없음. σ_xx ≠ σ_yy 자체가 유한 크기의 증거일 수 있다.
- **L11 · 60 MPa 의 σ_zz ≈ 66.5 MPa (+11 %, figure-read).** 30·200 MPa 는 1 % 안인데 60 만 벗어난다 — 정지 오버슈트인지 측정 시점 차인지 논문은 말하지 않는다.
- **L12 · 배위수 정의** — N_c/N_p (Z 의 절반). 다른 문헌 Z 와 섞지 말 것.
- **L13 · W_V 정의** — 집전체 두께 절반 포함, 이론 용량 170 mAh g⁻¹ · 3.7 V — **셀 수준 에너지밀도가 아니다**.
- **L14 · 그림 결함** — Fig 4b 범례 없음 · Fig 8 범례·힘 척도 없음 · Fig 7 라벨 오타 · Fig 11d 원 미설명 (§5.1).
- **L15 · 서지** — 권·쪽 미인쇄 [미확인]. SI 없음.
- **L16 · "~20 % 강체구 floor" 와의 관계.** 하중 중 0.152 는 CLAUDE.md 의 "강체구 floor ~20 %" 아래다 — **넓은 실측 PSD(반지름 ≈ 0.5–16 µm) + CBD 소구 + 하중 중 탄성 겹침 + 미기재 공극률 관례**가 겹친 값. 제하 후 0.319 는 floor 위. ⇒ 우리 "~20 % floor" 를 **PSD·관례·하중상태 무관 상수로 쓰지 말 것** — 이 논문이 그 조건부성을 보여준다.

---

## 11. 용어 미니 사전

| 용어 | 뜻 (이 논문 맥락) |
|---|---|
| **linear parallel bond** | 두 입자 사이에 유한 크기 원판(반지름 R̄)을 두고 힘과 **모멘트**를 선형 탄성으로 전달하는 결합. 피크 법선응력/전단응력이 강도를 넘으면 **취성 파단** (Potyondy & Cundall 2004) |
| **radius multiplier λ̄** | bond 원판 반지름 = λ̄ × (작은 입자 반지름). 1 이 관례, 이 논문은 **2** |
| **κ̄*** | bond 의 법선/접선 강성비 (k̄_t = k̄_n/κ̄*) — 값 미기재 |
| **ball-ball / ball-facet** | 입자–입자 / 입자–벽(면) 결합 구분 (PFC 계열 어휘) |
| **ξ̄ (bond 형성 간격계수)** | 중심거리 ≤ R⁽¹⁾ + R⁽²⁾ + ξ̄·D_c 면 결합 생성. 1.5 × 2.2 µm = 3.3 µm 간격까지 묶는다 |
| **Hertz–Mindlin** | 법선 Hertz(δ^1.5) + 접선 Mindlin 탄성 접촉. 항복 없음 |
| **FSA_p** | 입자의 (표면적 − 접촉면적 합)/부피 [m⁻¹]. 활성(전해액 노출) 표면의 비표면적 |
| **배위수 (이 논문)** | N_c/N_p — 접촉 한 번씩 세면 통상 Z 의 절반 |
| **Love–Weber (Christoffersen) 응력** | RVE 평균 응력 = (1/V) Σ 접촉력 ⊗ 가지벡터 |
| **pull-off vs peel** | pull-off = 면에 수직 인장(응력 MPa) / peel = 각도 박리(단위폭당 힘 N m⁻¹ 또는 에너지 J m⁻²). 이 논문 모식은 pull-off, 용어는 peel |
| **springback (탄성회복)** | 하중 제거 후 두께·공극 회복. 이 논문 DEM 은 제하 곡선으로 직접 보여준다 |
| **체적에너지밀도 W_V** | U·m·q/V — 여기서는 NMC 질량 × 이론 비용량 × 평균 전위 / (코팅 + 집전체 절반) 부피 |

---

## 12. 🧮 파생 계산 원장 (`derived(ours)`) — 논문 인쇄값·그림 판독값에 산술만 한 것

> 판독 방법: 원본 임베디드 래스터(300 dpi)에서 축 눈금 픽셀을 찾고 선형 환산. 막대 끝 판독은 외곽선 두께 때문에 **≈ −0.4 MPa** 계통 편향이 있었고 보정했다(Fig 10 의 stated 값 3점으로 확인).

### D1 · ★★★ Fig 12 는 **하중 상태** 두께로 계산된 W_V 다
- 가정: 초기 코팅 두께 h₀ = RVE 높이 75 µm, 집전체 몫 6 µm(12 µm 의 절반, stated), 고체부피 보존 ⇒ h(P) = h₀·(1 − 0.432)/(1 − ε(P)), W_V(P) = W_V(0)·(h₀ + 6)/(h(P) + 6).
- **하중 중 ε (Fig 4b 판독)** 로: 30 MPa 1649 · 60 MPa 1767 · 100 MPa 1916 · 140 MPa 2001 · 200 MPa **2048** Wh L⁻¹ ↔ Fig 12 판독 **1650 · 1770 · 1917 · 2001 · 2050** — **다섯 점 모두 0.2 % 안**. (200 MPa 비율 1.440 vs 판독 1.442.)
- 강건성: h₀ 를 70 · 80 µm 로 바꿔도 200 MPa 비율 1.437 · 1.443 — 결론 불변. 제하 후 ε 로는 비율이 ≈ 1.18 이라 **판독과 전혀 안 맞는다**.
- ⇒ **제하 후 구조의 W_V**: 30 MPa ≈ **1470** · 60 MPa ≈ **1565** · 200 MPa ≈ **1680** Wh L⁻¹ (ε 0.411 / ≈ 0.370 / ≈ 0.319). 200 MPa 에서 헤드라인 대비 **≈ −18 %**, 초기 대비 이득은 +44 % 가 아니라 **+18 %**.

### D2 · springback — 같은 DEM 안의 가압–제하 차
| 목표 | 하중 중 ε | 제하 후 ε | Δε | 두께 회복 ER = (h_제하 − h_하중)/h₀ | 영구 압밀 몫 |
|---|---|---|---|---|---|
| 30 MPa | 0.333 (stated) | 0.411 (stated) | **0.078** | **11.3 %** | 0.021 / 0.099 = **21 %** |
| 60 MPa | ≈ 0.280 | ≈ 0.370 | ≈ 0.090 | ≈ **11.3 %** | ≈ 0.062 / 0.152 = ≈ 41 % |
| 200 MPa | ≈ 0.152 | ≈ 0.319 | ≈ 0.167 | ≈ **16.4 %** | ≈ 0.113 / 0.280 = ≈ 40 % |
- ER 는 Sangrós 2019 (정본 카드) 의 **10.25 → ~17 %** 와 같은 밴드다 — **같은 부류 DEM(강체구 + bond)의 공통 거동**으로 읽힌다. 실측 springback 과 비교된 것은 아니다.
- 제하 곡선 모양: 200 MPa 런 ε ≈ 0.236 @5 MPa → 0.319 @0 ⇒ **회복의 ≈ 50 % 가 5 MPa 아래** (figure-read).

### D3 · 응력텐서 — 이방성은 일정하고 등방성은 커진다
| 목표 | σ_xx/σ_yy | K_xx = σ_xx/σ_zz | K_yy = σ_yy/σ_zz | 평균 K | p = tr/3 | q = σ_zz − (σ_xx+σ_yy)/2 | σ_zz/목표 |
|---|---|---|---|---|---|---|---|
| 30 | **1.196** | 0.441 | 0.368 | **0.40** | 18.3 | 18.1 | **1.013** |
| 60 | ≈ 1.18 | ≈ 0.53 | ≈ 0.45 | **≈ 0.49** | ≈ 44 | ≈ 33.8 | **≈ 1.11** |
| 200 | **1.173** | 0.733 | 0.625 | **0.68** | 156.1 | 63.7 | **0.993** |
(단위 MPa; 60 MPa 행은 figure-read 기반.) q/p 는 0.99 → 0.41 로 떨어진다 — 압밀될수록 **정수압 성분이 지배**.

### D4 · 배위수 → Z 환산
Z = 2·CN (접촉을 한 번씩 셌다고 볼 때) = **1.81 / 2.58 / 4.10** (30/60/200 MPa). 30·60 MPa 에서 Z < 3 ⇒ **NMC 골격만으로는 하중망이 서지 않는다** — 하중을 bond 망이 진다는 저자 서술(Fig 8)과 정합.

### D5 · ΔFSA 재계산
(4.381 − 4.121)/4.381 = **5.93 %** · (4.381 − 4.038)/4.381 = **7.83 %** · (4.381 − 3.832)/4.381 = **12.53 %** — 인쇄값 5.9/7.8/12.5 와 정합.
참고: 자유 구의 FSA = 3/r ⇒ 4.381 × 10⁵ m⁻¹ 은 r ≈ **6.8 µm** 급 — PSD 가 반지름 분위수라는 §3.3 해석과 같은 방향(평균 방식 미기재라 검증은 아니다).

### D6 · 박리 피크 / bond 강도
0.0349 MPa / 0.072 MPa = **0.485** — 모든 입자–Al bond 가 **동시에 순수 인장 파단**한다고 보면, 집전체 발자국의 **≈ 48 % 가 bond 원판으로 덮인** 셈이다 (λ̄ = 2 라 원판이 크다). 모멘트 항·순차 파단을 무시한 해석 — 크기 감각만.
그리고 σ̄_Particle-Particle / σ̄_Particle-Al = 3.6 × 10⁷ / 7.2 × 10⁴ = **500** ⇒ 모델은 **집전체 계면을 설계상 가장 약한 고리**로 만든다.

### D7 · ★★ Hertz 면압 — 탄성 가정의 유효범위와 "큰 입자" 추론
가정: E 142 GPa, ν 0.25 ⇒ NMC–NMC E* = 75.7 GPa (NMC–Al E* = 50.5 GPa).
| 경우 | a (µm) | 평균면압 p_m (GPa) | 최대면압 p₀ (GPa) | δ (µm) |
|---|---|---|---|---|
| 평균 힘 7.3 mN, 6–6 µm 쌍 | 0.60 | **6.4** | 9.7 | 0.12 |
| 7.3 mN, 16–16 µm 쌍 | 0.83 | 3.3 | 5.0 | 0.09 |
| 최대 힘 177 mN, 6–6 µm 쌍 | 1.74 | **18.6** | 27.9 | 1.01 |
| 177 mN, 16–16 µm 쌍 | 2.41 | **9.7** | 14.5 | 0.73 |
| 177 mN, 16–3 µm 쌍 | 1.64 | 20.9 | 31.3 | 1.07 |
- 기준: 정본 `xu2017_*` 카드의 NMC532 이차입자 경도 **H = 8.6 ± 1.3 GPa** (나노압입). ⇒ 평균 접촉은 **≈ 0.75 H**, 최대 접촉은 **≈ 1.1–2.4 H** — **탄성 Hertz 가 경도를 넘는 접촉이 존재**한다. 같은 xu2017 카드에 Berkovich 압입에서 **≈ 2.4 · 5.2 · 7.2 mN 에 균열성 급락**이 기록돼 있다(기하가 달라 크기 감각만).
- ★ **같은 힘이면 큰 입자 쌍의 면압이 낮다** (177 mN: 16–16 µm 9.7 GPa vs 6–6 µm 18.6 GPa). 큰 입자가 더 큰 힘을 받는 것(Fig 9)과 더 잘 깨지는 것은 **다른 명제**이고, 둘을 잇는 것은 **크기 정규화된 파괴 기준**(Auerbach: 임계하중 ∝ R, 또는 Weibull 크기효과)이다 — 이 논문엔 없다.

### D7b · ★★ 정본 `wheatcroft2023_*` 의 이차입자 파괴강도 σ_F = P_f/D² 로 정규화하면
- 기준 (그 카드): pristine NMC811 이차입자 **평판 압축 207 ± 49 MPa · 원뿔-구형 팁 67 ± 21 MPa** (stated), P_f ∝ D^1.51 (평판) · D^1.19 (원뿔) (그 카드 digitized).
  원뿔 팁은 *"작은 입자가 더 강하다"*, 평판은 *"입경에 거의 둔감"* (그 카드 stated).
- Fig 9 의 **짝지은 점**(§3.8 — 같은 접촉이 두 입자 지름에 두 번 찍힘)으로 한 접촉의 두 입자를 읽어 P/D² 를 매긴다 (figure-read × 산술):

| 압력 | 접촉 | P/D² — 작은 쪽 | P/D² — 큰 쪽 | 작은 쪽 ÷ 평판 207 |
|---|---|---|---|---|
| 30 MPa | 24.3 mN, D 10.3 · 11.9 µm | ≈ 229 MPa | ≈ 172 MPa | ≈ 1.1 |
| 30 MPa | 24.7 mN, D 25.0 · 32.0 µm | ≈ 40 MPa | ≈ 24 MPa | ≈ 0.2 |
| 60 MPa | 42.9 mN, D 13.8 · 17.8 µm | ≈ 225 MPa | ≈ 135 MPa | ≈ 1.1 |
| 200 MPa | 176.5 mN, D 18.3 · 32.0 µm | ≈ 527 MPa | ≈ 172 MPa | ≈ 2.5 |
| 200 MPa | 112.7 mN, D 8.9 · 13.8 µm | ≈ 1,420 MPa | ≈ 590 MPa | ≈ 6.9 |
| 200 MPa | 163 mN, D 4.7 · 23.2 µm | **≈ 7,400 MPa** | ≈ 303 MPa | **≈ 36** |
| 200 MPa | 평균 7.3 mN, D ≈ 12 µm 가정 | ≈ 51 MPa | — | ≈ 0.2 |

- ⇒ (i) **평균 접촉은 파괴강도 아래**지만 **꼬리**(최대/평균 ≈ 24)가 **30 MPa 에서 이미 평판 강도에 닿고**, 200 MPa 에서는 수 배–수십 배 넘는다 — 파괴 없는 탄성 모델의 유효범위 밖이다 (저자도 200 MPa 를 "손상 조건"이라 부른다).
  (ii) **정규화하면 가장 과응력인 것은 큰 입자에 끼인 작은 입자**다 (163 mN 접촉의 4.7 µm 쪽) — 논문의 *"큰 입자가 더 취약"* 과 **반대 방향**.
- ⚠ 한정: NMC811(Targray) 기준을 이 논문의 NMC(111 계)에 댔다 · **단일 직경 압축**용 P/D² 를 다접촉 층상에 적용했다 · 그림 판독 × 산술 ⇒ **순위의 방향 감각만**, 값 인용 금지.

### D8 · 재하율
c = √(E/ρ) = √(142 × 10⁹ / 4750) ≈ 5,470 m s⁻¹ ⇒ Mach = 0.01/5470 ≈ **1.8 × 10⁻⁶**. bond 급 강성(0.3 GPa, ρ ≈ 2,700)으로 잡아도 c ≈ 333 m s⁻¹ ⇒ **3 × 10⁻⁵**.
관성수 I = γ̇·d·√(ρ/P), γ̇ = v/h = 0.01/75 µm ≈ 133 s⁻¹, d ≈ 12 µm ⇒ **I ≈ 2.0 × 10⁻⁵ (30 MPa) · 7.8 × 10⁻⁶ (200 MPa)** — 준정적(I ≪ 10⁻³).

### D9 · 집전체 접촉면적 분율
113 / 198 / 490 µm² ÷ 10⁴ µm² = **1.1 / 2.0 / 4.9 %** (figure-read 기반).
벽 Hertz 로 δ = 0.937 µm 겹침을 환산하면 한 접촉당 면적 ≈ 8.8 (R = 3 µm) – 47 µm² (R = 16 µm), 힘 ≈ 106 – 244 mN — Fig 9 의 최대 NMC 접촉력(≈ 177 mN)과 같은 급.

### D10 · σ_zz 자기 일관 — D3 의 마지막 열.

### D11 · Fig 4c 상대오차 (figure-read)
0 MPa (0.432 − 0.424)/0.424 = **+1.9 %** · 30 MPa (0.411 − 0.412)/0.412 = **−0.2 %** · 60 MPa **≈ +3.1 %** · 200 MPa **≈ +2.9 %**. 판독 불확도 ≈ ±0.002 (≈ ±0.5 %p).

### D12 · W_V(0) 역산 (가정 의존 — 참고만)
1422 = 3.7 V × 170 mAh g⁻¹ × 4.75 g cm⁻³ × φ_NMC × 75/81 ⇒ **φ_NMC ≈ 0.514** (고체 0.568 중 **≈ 90.5 %**) ⇒ 96:4 wt 와 맞추려면 **ρ_CBD ≈ 1.9 g cm⁻³** (미기재 값의 함의). PVDF/CB 50:50 로 그럴듯한 범위 — 내부 정합 확인일 뿐.

---

## 13. 이 논문이 우리 백로그에 여는 것

- ⬜ **F-SB1 보강**: 우리 `--protocol release` 팔의 첫 규모 비교 표적으로 **강체구+bond DEM 의 ER 11–16 %** (이 카드 D2 · Sangrós 2019) — ⛔ 값 인용 금지, **"같은 부류 모델이 내는 크기"** 로만.
- ⬜ **제하 → 적층압 유지 팔** (§8 ②): 300 MPa 압밀 후 P_stack ∈ {0, 5, 10, 50} MPa 로 내려 공극률·σ 를 재는 것. 이 논문 곡선 모양이 방향 가설.
- ⬜ **σ_zz(RVE) / 플래튼 응력 상주 검사** + **측압계수 K** 출력 (§8 ④).
- ⬜ **§I 박리 트랙 사양 보강**: 피크 응력 · G · 파괴 위치 동시 기록, 식별성(σ̄·λ̄²) 표기 (§8 ③).
- ⬜ **파괴 판정의 크기 정규화 점검**: 우리 Auerbach 판정이 입경을 어떻게 쓰는지 확인하고, "큰 입자 우선 파괴" 를 **힘이 아니라 정규화 기준**으로 보고하는지 (§12 D7). 정본 대조 기준 = `wheatcroft2023_*` 의 σ_F = P_f/D² (§12 D7b) — 우리 DEM 접촉력 덤프에 같은 정규화를 걸어 **"어느 크기가 먼저 깨지나"** 를 문헌과 같은 척도로 낼 수 있다.
- ⬜ (장기) **X-CT 기반 독립 초기구조** 경로 (§8 ⑤) — 실행 가능성 미정.
- 🔗 **관련 카드 (2026-11-12 한 줄 추가)**: [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) — 자기 시료의 in situ CT (누른 채 · 화소 0.5 µm) 입자를 등가 구 942 개로 옮긴 결합 DEM · 위 '크기 정규화' 항목 (D7 · D7b) 이 요구한 판정을 실제로 쓴 논문 (σm = f_max/d² · 문턱 ≈200 MPa — 다만 근거는 인용 한 점 · 깨진 입자와의 수 대조 없음) · 다른 그룹 (BIT).
- 🔗 **관련 카드 (2026-11-16 한 줄 추가)**: [`ge2022_xct_initial_structure_dem_calendering_nmc333`](ge2022_xct_initial_structure_dem_calendering_nmc333.md) = 이 카드의 ref 18 (L38 · L54 · L96 · L139) 의 원문 카드 — 같은 Ebner 미압연 CT 에서 입자 5106 개를 구로 옮긴 EEPA (n 1.5) + Potyondy–Cundall 결합 DEM · 판 0.01 m s⁻¹ 은 원문에서 **가압만** (제하 단계 없음 — L139 의 '가압·제하 동일' 은 이 논문 자신의 절차이고 ref 18 은 속도에만 붙는다) · 공극은 AM 밖 부피 (CBD = 빈 곳 · 0 bar 0.628) 라 이 카드 0.432 (CBD 고체) 와 정의가 다르다 · 원문 표 1 NMC μ 0.25 · μr 0.01 · e 0.5 · E 144 GPa (이 논문 μ 0.12 · E 142).
- 🔗 **관련 카드 (2026-11-16 한 줄 추가)**: [`stershic2015_fabric_tensor_calendering_nmc_xct_dem`](stershic2015_fabric_tensor_calendering_nmc_xct_dem.md) = 이 카드의 ref 30 (L38 · L222) 의 원문 카드 — 원문에 있는 것은 '큰 입자는 접촉이 많은 경향 (서술 · 교과서 [36])' · 'X-CT 에서 큰 입자 파쇄가 보인다 (정성 · Fig 8 한 장 · 원 관측 Ebner 2013)' 까지이고, L222 의 '힘이 커서' 와 Zhang 원문 같은 문단의 '작은 입자는 재배열 · 미끄럼으로 푼다' 는 그 원문에 없다 (그 카드 §0-1).
- 🔗 **관련 카드 (2026-11-16 한 줄 추가)**: [`sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811`](sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811.md) = 이 카드의 ref 21 (L38 · L97 · L307) 의 원문 카드 — 실제 크기 회전 롤 (R_c 10 cm · 마찰 구동) + 결합재 껍질 (R_p 0.34 µm) 응집-소성 법선 법칙 (항복 겹침 δ_e + 경화 지수 ζ · 제하 = 코어 강성 k₂ · 최대 겹침에 따른 당김 한계) · 강체 구 24 425 개 · 3D · 액체 LIB NMC811 96-2-2 · L97 · L307 의 서술은 원문과 같다 (단 전단장 · 미끄럼은 그 논문도 재지 않고 할 일로 남김 · 되돌아옴 C_r − C_f 2.2–3.7 %p [판독]).

---

## 14. ★ 보강 의도 대조 — 이 논문의 참고문헌 = 후보 표 · wishlist 의 원 인용처 (68-1 번 파일 · 2026-11-16)

**보강 의도** (1저자 11-12 · 지시서 X-68-1): 이 논문의 참고문헌이 후보 표 여러 행의 **원 인용처**다 — N-55 Meyer 2017 = [8] · N-66 Ebner 2013 = [22] · N-67 Ge 2022 = [18] · N-68 Sonzogni 2024 = [21] · N-69 Stershic 2015 = [30] · 그리고 [27] Lyu 2025 · [28] Srivastava 2020 · [32] Lippke 2024.
그래서 (가) 참고문헌 41 개를 원문 그대로 §17 에 옮기고 (나) 후보 표 · wishlist 와 닿는 참고마다 **이 논문이 그 참고에 대해 한 말** (원문 문장 · 쪽) 과 **이 카드의 2 차 서술** (줄 번호 = 보강 전 판 · 커밋 `74847e528` · 보강은 줄을 더하지 않고 같은 줄 끝에 표지를 붙였으므로 번호가 그대로 맞는다) 을 한 줄씩 견준다.
판정: **같음** = 카드 서술이 원문 문장의 범위 안 · **일부 다름** = 귀속 범위 · 위치가 넓거나 어긋남 (그 줄에 정정 표지) · **해당 없음** = 카드가 그 참고를 따로 다루지 않음.

| 참고 (원문 목록 · 줄임) | 이 논문이 그 참고에 대해 한 말 (원문 그대로 · 쪽) | 이 카드의 2 차 서술 (보강 전 줄) | 판정 | 후보 표 · wishlist · 정본 카드 |
|---|---|---|---|---|
| **[8]** Meyer · Bockholt · Haselrieder · Kwade, *J. Mater. Process. Technol.* 249, 172 (2017) | p.1: *"Meyer et al.⁸ studied graphite anodes and nickel–cobalt–manganese cathodes, analyzing the interdependence between coating density, calendering speed, and applied load, and proposed an exponential relationship between compaction force and porosity reduction."* | L92 "Meyer (ref 8) 압밀력–공극감소 **지수 관계**" | **같음** (코팅 밀도 · 속도 · 하중의 상호 관계 부분은 줄임) | 후보 **N-55** · 정본 `meyer2017_calendering_compaction_resistance_line_load_exponential_model` (그 카드 정독 batch_104 도 L92 = 원문과 같음) |
| **[12]** J. Zhang · J. Sun · H. Huang · C. Ji · M. Yan · Z. Yuan, *Appl. Energy* 373, 123900 (2024) | p.2: *"Zhang et al.¹² investigated coating–current collector interactions through microscratch and peel tests, revealing that increasing calendering load enhances coating adhesion while simultaneously increasing the susceptibility of aluminum current collectors to microscale damage, ultimately reducing the overall fracture energy of the electrode."* · p.10: *"…enlarges the effective contact area between the active material and the current collector.¹²"* | L94 "Zhang (ref 12) 미세스크래치·박리 … Al 집전체 미세손상↑ → 전극 파괴에너지↓" | **같음** (p.10 쓰임은 카드에 없음) | wishlist L241 · 카드 없음 |
| **[14]** R. Ge · A.M. Boyce · Y.S. Zhang · P.R. Shearing · D.J. Cumming · R.M. Smith, *Chem. Eng. J.* 465, 142749 (2023) | p.2: *"…X-ray computed tomography (X-CT) has become a widely used characterization technique in LIB research.¹⁴"* — X-CT 일반 서술의 근거로만 | 없음 | 해당 없음 | wishlist L326 (같은 서지) · 카드 없음 · 후보 표 L270 의 '같은 그룹 2023 CEJ 후속' 과 같은 논문으로 보인다 [카드 관찰] |
| **[15]** X. Lu · A. Bertei · D.P. Finegan · … · P.R. Shearing, *Nat. Commun.* 11, 2079 (2020) | p.2: *"Lu et al.¹⁵ employed a novel X-ray nano-computed tomography dual-scan superimposition technique to capture the characteristics of the CBD phase and demonstrated how microstructural heterogeneity significantly affects ionic and electronic transport under high-rate conditions."* | L95 "Lu (ref 15) nano-CT 이중 스캔으로 CBD 가시화" | **같음** (수송 영향 부분은 줄임) | wishlist L74 · 카드 없음 (정본 `lu2020_insitu_nanoct_calendering_microstructural_evolution` = *Joule* 2020 · 이 목록에 없는 다른 Lu 논문) |
| (인용 번호 없음) | p.2: *"In addition, in situ X-CT was used to monitor the evolution of porosity and tortuosity during successive calendering steps."* — 누구의 일인지 원문이 적지 않는다 | 없음 → L95 보강 표지 | 해당 없음 | 주제는 `lu2020_insitu_nanoct_…` 와 같다 [카드 관찰] · 귀속 [미확인] |
| **[16]** P. Pietsch · M. Hess · W. Ludwig · J. Eller · V. Wood, *Sci. Rep.* 6, 27994 (2016) | p.2: *"Furthermore, in-situ synchrotron radiation X-ray tomographic microscopy combined with X-ray diffraction (XRD) were utilized to dynamically track phase transformations and macroscopic deformation phenomena, such as crack formation and volumetric expansion…¹⁶"* (본문에 저자 이름 없음) | L95 "Pietsch (ref 16) in-situ 싱크로트론 + XRD" | **같음** | 없음 · 카드 없음 |
| **[17]** A.C. Ngandjong · T. Lombardo · E.N. Primo · M. Chouchane · A. Shodiev · O. Arcelus · A.A. Franco, *J. Power. Sources* 485, 229320 (2021) | p.2: *"Ngandjong et al.¹⁷ developed a 3D DEM calendering model incorporating both active material particles and CBD phases, and coupled it with coarse-grained molecular dynamics simulations of slurry drying and electrochemical finite-element models to achieve multiscale simulation of cathode manufacturing processes."* · p.8: *"Since calendering is essentially a particle rearrangement process, particle-scale simulations are capable of revealing the underlying mechanisms of structural evolution and mechanical response…¹⁷"* | L40 · L96 "Ngandjong (ref 17) 3D DEM + CGMD + FEM 멀티스케일" | **같음** (p.8 쓰임은 카드에 없었다 → §15 (i)) | 정본 `ngandjong2021_dem_calendering_digital_twin` |
| **[18]** R. Ge · D.J. Cumming · R.M. Smith, *Powder Technol.* 403, 117366 (2022) | p.2: *"Ge et al.¹⁸ imported uncalendered electrode microstructures obtained from X-ray computed tomography into DEM simulations, enabling quantitative analysis of porosity evolution, particle contact networks, and internal stress distributions under different calendering conditions."* · p.4–5: *"…with the platen velocity set to 0.01 m s⁻¹, consistent with previous studies.¹⁸"* | L54 "X-CT→DEM … 그건 ref 18 Ge 2022 가 먼저 했다고 논문 스스로 인용" · L96 · L139 "플래튼 속도 (가압·제하 동일) 0.01 m s⁻¹ (ref 18 과 일관)" | **같음** (L139: 인용 18 은 **속도 값에만** — 제하는 이 논문 자신의 절차 → 보강 표지 · L54 의 '먼저' = 앞선 문헌이라는 뜻 · 원문에 'first' 주장 없음) | 후보 **N-67** · 정본 `ge2022_xct_initial_structure_dem_calendering_nmc333` (batch_119: L54 · L96 · L139 = 원문과 같음) |
| **[19]** C. Sangrós Giménez · B. Finke · C. Schilde · L. Froböse · A. Kwade, *Powder Technol.* 349, 1 (2019) | p.2 (refs 19, 20): *"The coupled mechanical–electrochemical behavior of electrodes was investigated, highlighting the role of interparticle bond breakage in structural integrity degradation.¹⁹˒²⁰"* · p.4: *"…the top was set as a rigid platen to simulate the roller used during the calendering process.¹⁹"* · p.6: *"The model proposed by Giménez et al.¹⁹ does not take interfacial adhesion effects into account, which may lead to delamination of the electrode coating during unloading."* · p.9: FSA_p 정의 *"FSAp,¹⁹"* | L74 · L97 "Sangrós (refs 19, 20) bond 파단" · L105 · L306 · L369 | **같음** (본문은 'Giménez et al.' 로 부른다 · '결합 기계–전기화학' 부분은 줄임) | 정본 `sangros2019_dem_calendering_lib_electrode` |
| **[20]** C. Sangrós Giménez · C. Schilde · L. Froböse · S. Ivanov · A. Kwade, *Energy Technol.* 8, 1900180 (2020) | p.2: 위 refs 19, 20 문장 하나 | L40 · L97 | **같음** | 정본 `sangros2020_lib_electrode_dem_mech_elec_ionic` |
| **[21]** M. Sonzogni · J.-M. Vanson · Y. Reynier · S. Martinet · K. Ioannidou · F. Radjai, *Powder Technol.* 442, 119891 (2024) | p.2: *"Sonzogni et al.²¹ introduced rotating cylindrical rollers to more realistically represent the calendering process and proposed a novel contact law incorporating cohesive-plastic behavior of binder layers, thereby addressing limitations in previous models that neglected roller curvature and shear stresses."* | L97 "Sonzogni (ref 21) **회전 롤 + 응집-소성 바인더 접촉법칙**" · L307 "롤 곡률·전단(ref 21 Sonzogni 가 다룬 것)은 없다" | **같음** | 후보 **N-68** · 정본 `sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811` (2026-11-16 · 그 카드 정독 batch_122: L97 · L307 = Sonzogni 원문과도 같음) |
| **[22]** M. Ebner · F. Geldmacher · F. Marone · M. Stampanoni · V. Wood, *Adv. Energy Mater.* 3, 845 (2013) | p.2: *"The tomography datasets were sourced from the experimental work of Ebner et al.²²"* · p.2–3: *"…Ebner et al.,²² in which X-ray tomography, image reconstruction, and segmentation had already been completed. The resulting database also provides particle-level annotations, including spatial coordinates and volumetric information."* · p.4: *"Based on database literature,²² a subvolume of an uncalendered electrode structure was selected…"* · Fig 2 캡션 *"(a) data from Ebner et al. 22"* · p.8: *"…the DEM simulation results were compared with the experimental data reported by Ebner et al.²²"* | L38 · L50 · L100 · L265 · L299 · L313 · L465–466 | **같음** (L100 에 p.4 '이진화' 문장 보강 · L465–466 의 조성 · 압력은 Zhang 원문에 없음으로 닫음) | 후보 **N-66** · 정본 `ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation` (batch_118: 틀린 값 없음) |
| **[27]** Y. Lyu · S. Dong · L.T. Gao · Z.-S. Guo, *Int. J. Electr. Power Energy Syst.* 165, 110521 (2025) | p.4: *"…the particle diameter was set to 2.2 µm.²⁷"* · p.5 Table I *"…NMC particles²⁷˒²⁹⁻³¹"* | L41 "ref 27 = lyu2025 (CBD 2.2 µm 의 출처)" · L66 · L122 · L130 | **같음** (Table I 의 어느 값이 [27] 인지는 원문이 가르지 않는다 — L122 '마찰 0.12 = lyu2025 카드의 0.12' 는 카드 대조) | 정본 `lyu2025_3d_dem_drying_calendering_lib` |
| **[28]** I. Srivastava · D.S. Bolintineanu · J.B. Lechman · S.A. Roberts, *ACS Appl. Mater. Interfaces* 12, 34919 (2020) | p.4: *"The CBD particles were assumed to consist of 50% PVDF and 50% carbon black by weight.²⁸"* | L63 · L131 "PVDF 50 : CB 50 wt% 가정 (ref 28)" | **같음** | 후보 표 · wishlist 없음 (정독 batch_119 · 이 batch_123 의 n) · 카드 없음 |
| **[29]** R. Xu · H. Sun · L.S. de Vasconcelos · K. Zhao, *J. Electrochem. Soc.* 164, A3333 (2017) | Table I 출처 묶음 (27, 29–31) 의 하나 — 본문에 따로 말 없음 | L42 · L120 "E_NMC 142 GPa 계보의 원전 후보 … 보인다" | **같음** (카드도 추정 표지) | 정본 `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` |
| **[30]** A.J. Stershic · S. Simunovic · J. Nanda, *J. Power. Sources* 297, 540 (2015) | p.12: *"For a given external load, larger particles typically exhibit a greater number of contact points and sustain substantially higher contact forces than smaller particles. The resulting interfacial stresses may induce surface defects and crack initiation, making larger particles more susceptible to fracture. In contrast, smaller particles tend to alleviate stress concentration through local rearrangement or sliding. This phenomenon was observed in X-CT, further confirming that larger particles exhibit a higher tendency to fracture during the calendering process.³⁰"* | L222 "큰 입자일수록 접촉점이 많고 힘이 커서 파쇄에 더 취약하다 — X-CT 에서도 관측(ref 30)" · L472 | **일부 다름** — 원문은 인용 30 을 **마지막 문장 (X-CT 에서 큰 입자 파쇄가 보였다) 끝에만** 붙인다 · '접촉점이 많고 힘이 크다' 는 이 논문 자신의 DEM 서술 (인용 없음) · 같은 문단의 '작은 입자는 재배열 · 미끄럼으로 응력 집중을 푼다' 는 카드에 없었다 → L222 정정 표지 | 후보 **N-69** · 정본 `stershic2015_fabric_tensor_calendering_nmc_xct_dem` (그 카드 §0-1 · batch_120 카드 문제 1: 'higher contact forces' · 'rearrangement or sliding' 은 Stershic 원문에 없다 = Zhang 원문의 인용 문제) |
| **[31]** C. Sangrós Giménez · B. Finke · C. Nowak · C. Schilde · A. Kwade, *Adv. Powder Technol.* 29, 2312 (2018) | Table I 출처 묶음 (27, 29–31) 의 하나 — 본문에 따로 말 없음 | 따로 없음 (L116 · L340 'refs 27, 29–31') | 해당 없음 | wishlist L328 · 카드 없음 |
| **[32]** M. Lippke · T. Ohnimus · F. Frankenberg · C. Schilde · A. Kwade, *Powder Technol.* 444, 119984 (2024) | p.6: *"To address this issue, Lippke et al.³² extended the adhesion model by incorporating cohesive interactions between particles and the current collector into the analytical framework, thereby suppressing coating detachment during calendering simulations. However, the interfacial adhesion parameters in their work were not quantitatively calibrated."* | L38 · L105 "Lippke 2024 (ref 32) 는 입자–집전체 응집을 넣었지만 정량 보정을 안 했다" | **같음** | 후보 표 · wishlist 없음 · 카드 없음 (정본 `lippke2023_dem_drying_structure_formation_lib` = *Energy Technol.* 2023 · 다른 논문) → batch_123 n |
| **[34]** Y. Song · K. Gao · C. He · Y. Wu · S. Yang · N. Li · L. Yang · Y. Mao · W.-L. Song · H. Chen, *Appl. Energy* 351, 121904 (2023) | p.10: *"Since the electrode coating is directly bonded to the current collector surface, the current collector is required not only to possess adequate mechanical strength but also to maintain structural integrity.³⁴"* | 없음 | 해당 없음 | wishlist L107 · L238 · 카드 없음 (정본 `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` = 같은 그룹 다른 논문) |
| **[36]** P. Zhu · D. Gastol · J. Marshall · R. Sommerville · V. Goodship · E. Kendrick, *J. Power. Sources* 485, 229321 (2021) | p.10–11: *"…aluminum foils with thicknesses of 10–20 µm exhibit a pronounced reduction in yield strength and tensile strength,³⁶ making them more sensitive to surface roughness and localized defects."* | L210 | **같음** | 없음 |
| **[37]** J. Zhang · H. Huang · J. Sun, *Powder Technol.* 409, 117828 (2022) | p.11: *"Interparticle friction and compressive contact interactions are among the key factors that limit the extent of compressive deformation during electrode calendering.³⁷"* | 없음 | 해당 없음 | wishlist L232 · 카드 없음 |
| **[39]** J. Christoffersen · M.M. Mehrabadi · S. Nemat-Nasser, *J. Appl. Mech.* 48, 339 (1981) | p.12: *"Within the DEM, the contact forces and relative displacements between particles can be explicitly calculated. These microscopic mechanical quantities enable an accurate description of the mechanical behavior of particulate assemblies at the microscale.³⁹"* → 식 24 | L375 "Christoffersen 1981 = ref 39" | **같음** | 없음 · 카드 없음 → batch_123 n |
| **[41]** E.J. Berg · C. Villevieille · D. Streich · S. Trabesinger · P. Novák, *J. Electrochem. Soc.* 162, A2468 (2015) | p.14: *"q is the specific capacity (170 mAh g⁻¹),⁴¹"* | L249 | **같음** | 없음 |

- 후보 표 행 (`S8_candidates.md`) 대조: N-66 · N-67 · N-68 · N-69 의 '왜' 칸은 이 카드 L38 · L50 · L96 · L97 · L139 · L222 · L265 · L307 을 옮긴 것 — 위 표대로 **L222 만 귀속 범위가 넓다**.  N-55 의 '왜' 칸 (*"Heckel 지수 기반 … compaction impedance"*) 은 이 카드가 아니라 `he2026_dem_calendering_inhomogeneity_areal_density` 에서 온 것이고 (batch_104 카드 문제), 이 논문 p.1 의 [8] 서술에는 Heckel · impedance 낱말이 없다.
- 서지: 후보 표 L276–277 (대피 세션 11-12) 이 이 원문 목록으로 확정한 [8] · [18] · [21] · [22] · [30] 은 §17 과 권 · 쪽 · 연도까지 같다.  지시서 메모 ([21] · [18] · [22] · [30] · [8]) 도 같다.

⇒ **보강 의도 대조 결과: 일부 다름** — 23 행 가운데 카드에 2 차 서술이 있는 18 행 중 **17 행 같음 · 1 행 ([30] · L222) 귀속 범위가 넓다** (정정 표지).  의도 밖에서 L91 (refs 4–6 위치) 한 줄을 더 고쳤다.

---

## 15. ★ 원문 문장 대조 — DEM 한계 · 소성 · 차원 · 탈압 (정독 질문 k · l 의 근거 · 2026-11-16 원문에서)

인용 서지 = X. Zhang · T. Gao · Z. Xiao · Y. Ding, *JOM* (2026), DOI 10.1007/s11837-026-08748-x (권 · 쪽 미인쇄).

**(i) DEM 한계 — 원문이 직접 한 말**
- p.8 (구 근사 → 부피 손실): *"Slight discrepancies were observed during the later stages of calendering, which can be mainly attributed to the spherical particle approximation adopted in the DEM framework, introducing a certain degree of volumetric loss error."* — 저자가 **자기 모델**에 대해 적은 유일한 한계 문장 · 크기 · 정의 없음 (60 · 200 MPa 에서 DEM 이 실험보다 +0.009–0.011 성기다 [판독 §3.5 · `digitized.csv`]).
- p.4 (구 근사의 정당화): *"Given the highly spherical morphology of the NMC particles, they were represented as equivalent spheres in the numerical modeling."* — 같은 논문 SEM (Fig 11c) 은 1 차 결정립이 뭉친 이차입자.
- p.4 (형상 단순화 = 비용): *"If the real morphology was directly used in the DEM simulation, the computational cost would increase substantially."* (CBD 를 2.2 µm 단일 구로 · 비용 숫자 없음)
- p.8 (캘린더링 = 재배열이라는 전제 · ref 17): *"Since calendering is essentially a particle rearrangement process, particle-scale simulations are capable of revealing the underlying mechanisms of structural evolution and mechanical response, which facilitates a deeper understanding of the overall calendering behavior of electrodes.¹⁷"* — 입자 형상 변화 · 소성을 계산 밖에 두는 전제 [카드 해석].
- p.2 (남의 DEM 의 한계): *"Despite these advances, most DEM studies still rely on virtual particle packing and lack validation based on realistic microstructural data, leading to uncertainties in parameter calibration and model reliability."* · 앞선 모델은 롤 곡률 · 전단을 무시했다 ([21] 문장 · §14).
- p.13 (파괴는 다음 일): *"Based on these results, subsequent studies can utilize the extracted stress information to evaluate the critical stress conditions for particle fracture and to further establish quantitative relationships between calendering pressure and particle fragmentation behavior."*
- **말 없음**: 믿을 수 있는 겹침 · 상대밀도 · 변형률의 상한 · 접촉 독립 가정이 깨지는 밀도 · 보정값이 물성이 아니라는 고백 (§10 L4 는 이 카드의 해석) · 해상도 · RVE 크기 · 시드 수렴.

**(ii) 소성변형 — 원문의 처리**
- 모델 안에 소성이 없다: NMC–NMC = 탄성 Hertz–Mindlin (식 1–6 · 항복 캡 없음) · CBD = 선형 탄성 parallel bond (식 7–21 · 파단 판정 문장은 원문에 없음 · §4.3 L294 보강) · 입자 형상 고정 · 집전체 = 변형하지 않는 벽.
- 그래도 본문은 '변형' 을 쓴다: p.10 *"As the applied pressure increases, particles experience more extensive contact, deformation, and local rearrangement, leading to a substantial increase in both contact area and contact number."* · p.11 *"Given the small particle size and low deformation resistance of CBD…"* · p.10 *"…it simultaneously introduces more severe deformation of the current collector."* — 모델의 '변형' = 겹침 δ (집전체 '매립 깊이' 도 벽 겹침) [카드 관찰 · §4.4 · §10 L7].
- 소성을 넣기 어려운 **이유는 원문에 없다**.  우회도 없다 — 대신 bond 세 값 (Ē* 0.3 GPa · σ̄ 3.6 × 10⁷ Pa · λ̄ 2) 을 *"the macroscopic mechanical responses predicted by the numerical model are in good agreement with experimental measurements"* 가 되게 맞추고 (표적 미기재 · p.7) 입자–Al bond 강도 1 값 (7.2 × 10⁴ Pa) 을 박리 피크에 맞춤 (p.6) = **맞춘 값 4 개**.  검증 = 제하 뒤 공극 4 점 (Fig 4c).  계산 비용 · 입자 수 · 시간 간격 = 원문에 없음.

**(iii) 차원** — 3D 만 (RVE 100 × 100 × 75 µm³ · x · y 주기).  Fig 2a · 2b 의 2D 단면은 설명용 · 2D 계산 · 2D → 3D 전이에 대한 말 없음.

**(iv) 탈압 — 다뤘다** (같은 속도로 판을 올려 '탄성 회복'):
- p.5: *"Once the target compressive stress was reached, the platen stopped further compression and subsequently moved upward in the opposite direction at the same velocity to simulate elastic recovery."*
- p.7–8: *"During the subsequent unloading stage, the electrode exhibited a certain degree of elastic recovery, resulting in a partial rebound of thickness and a corresponding increase in porosity. Consequently, the final porosity after unloading recovered to 0.411, while the experimentally measured final porosity was 0.412."*
- p.6 (제하 때 코팅 들뜸 → 입자–Al bond 를 넣은 이유): *"…unrealistic phenomena may occur, such as delamination or interfacial separation between the coating and the current collector during unloading or under low-pressure conditions."*
- 크기: 30 MPa 0.333 → 0.411 [인쇄 p.7–8] · 200 MPa ≈0.152 → ≈0.319 [판독 · `digitized.csv`] · 회복의 ≈절반이 5 MPa 아래 [판독].  실험 쪽 되돌아옴 측정 · 실험 캘린더링 방법은 원문에 없음.

---

## 16. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정하지 않는다.  이 논문의 공극은 액체 LIB NMC111 + CBD 전극의 값이라 '랩 표준과 다른 문헌 값' 이다 — 나란히 적되 견주어 판정하지 않는다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 같은 RVE 의 **하중 중 ε (Fig 4b)** 과 **제하 뒤 ε (Fig 4c)** 이 0.08–0.17 벌어진다 (30 MPa 0.333 → 0.411 [인쇄] · 200 MPa ≈0.152 → ≈0.319 [판독]) → 연산자 등록에 '상태 (하중 중 / 제하 뒤)' 칸이 필수라는 근거 · 겹침 처리 관례 미기재라 같은 수를 다시 낼 수 없다 → 우리 등록에 겹침 관례 (ε_sphere / ε_union) 를 함께 | 공극 정의식 · CBD 를 고체로 셌는지 · 진밀도 [미확인] (같은 Ebner 자료의 `ge2022_*` 는 'AM 밖 부피' 0.628 로 다른 정의 — L598) |
| **단계 1** (3D 메모리 · 장 수) | 없음 | 입자 수 · 시간 간격 미기재 |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 | SE 없음 · 순수 상 압축 자료 없음 |
| **단계 5** (3D 복합 압밀) | 출발 상태를 **실측 CT 좌표 · 부피 → 등가 구** 로 (실측 PSD 반지름 ≈0.5–16 µm · 주기 x · y · 바닥 벽 · 위 판 · 판 속도 0.01 m s⁻¹ · 목표 응력 도달 즉시 정지 · 후퇴) · 자기 점검 = RVE σ_zz (식 24) ÷ 판 응력 1.013 · ≈1.11 · 0.993 [카드 산술 D3] · 측압계수 K 0.40 → 0.68 · 하중이 bond 망 → NMC 직접 접촉으로 옮겨 감 (Fig 8 · 정성) | 값 전이 금지 (액체 LIB · NMC111 · SE 없음) · 우리 300 MPa 단축 냉간 압착 ↔ 30–200 MPa |
| **단계 6** (탈압 · 되돌아옴) | ★ 같은 DEM 안의 가압–제하 루프 (Fig 4b) — 회복의 ≈절반이 5 MPa 아래 · ER 11–16 % [카드 산술 D2] · 기전 = 탄성 Hertz + 취성 bond (소성 없음) · 입자–집전체 bond 가 없으면 제하 때 코팅이 들뜬다 (p.6) = 판 · 벽 분리를 계산할 때 벽 점착을 넣은 선례 | 우리 SE (소성) 회복 크기의 근거 아님 · 실험 되돌아옴 측정 없음 · 적층압 유지 단계 없음 |
| **단계 7** (형상 · 피복 · 수송) | FSA_p (식 22 · ref 19) · ΔFSA (식 23) = 접촉 면적 합을 뺀 자유 표면 → 우리 피복 (coverage) 의 여집합 꼴 · 집전체 접촉 면적 ≈113 / 198 / 490 µm² [판독 · 재판독 114 / 199 / 492] = 발자국의 1.1–4.9 % | 수송 σ 계산 0 · 접촉 면적 정의 미기재 (Hertz 면적 합 추정) |
| **후보 D0** (지금 DEM) | 같은 인식론의 LIB 판 — 탄성 접촉 + 거시 응답에 맞춘 유효 상 (그들 bond Ē* 0.3 GPa ↔ 우리 E_eff 1.35 GPa · 18 배 연화) · 둘 다 물성이 아니라 보정값 | ⛔ 0.3 ↔ 1.35 숫자 비교 금지 (bond 원판 모듈러스 ↔ Hertz 접촉 모듈러스) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 입자–벽 bond 강도 1 값 (7.2 × 10⁴ Pa) 을 박리 피크 (0.0347 ± 0.0032 MPa) 에 맞춘 선례 · λ̄ 와 σ̄ 가 인장 항에서 서로 바뀐다 (식별성 · §10 L4) | 시간축 무차원 → 박리 에너지 (G_c) 없음 · 박리 시편의 압연 여부가 원문 문장끼리 어긋남 (L164) |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C** (MDR) | 없음 (Hertz 탄성) | — |
| **후보 C′** (항복 캡 · 다접촉) | 반례로 쓸 수치 — 항복 캡 없는 Hertz 로 200 MPa 까지 누르면 접촉 면압이 NMC 경도를 넘는 접촉이 생긴다 (최대 ≈1.1–2.4 H [카드 산술 D7]) = 캡이 필요한 영역 | 캡 · 다접촉 보정 없음 |
| **후보 M0** (균질화 · Heckel) | 하중 중 ε–P 연속 곡선 (Fig 4b 가압 가지) — Heckel 꼴로 바꿀 수 있는 DEM 자료 | 실험은 제하 뒤 4 점뿐 · DEM 산물 |
| **U0–U6** | **U4** (판 분리) — DEM 박리 피크 ↔ 실험 피크 대조 꼴 (0.0349 ↔ 0.0347 MPa · 이 잔차는 보정 잔차) · **U6** — 단일 RVE (측면 ≈3 d_max) · 시드 · 크기 수렴 없음 = U6 가 왜 필요한지 보여 주는 반례 | 해석해 시험 없음 |
| **R1–R7** | **R1** 하중이 bond 망 → NMC 직접 접촉으로 (Fig 8 · 정성 · 몫 숫자 없음) · **R2** 마찰 0.12 (Table I) · 입자–Al bond 파단 · **R4** = 단계 6 · **R5** 반례 — 보정값 4 (σ̄_Particle-Al + Ē* · σ̄ · λ̄) · **R7** 파괴 모델 없음 · '큰 입자 = 접촉 · 힘 많음 → 파쇄 취약' 은 이 논문 자신의 서술 + X-CT 관찰 인용 [30] (§14) · 크기로 정규화하면 반대 방향 (D7b) | R3 · R6 없음 |
| **결과 전 대조 항목** | Fig 4c 4 점 (실험 · 압연 뒤 · 측정법 미기재 · 자체 / Ebner 미분) · σ_zz ÷ 판 응력 · K · ER — '액체 LIB NMC111 · CBD · 다른 재료' 표지와 함께 (`digitized.csv`) | 우리 랩 표준 (순수 SE 10–13 %) 과 같은 양이 아니다 |

- **재료 · 차원 · 조건 차이**: NMC111 + C65 + PVDF (액체 LIB) ↔ 우리 NCM811 + LPSCl (ASSB · SE 가 소성 유동) · 3D = 같음 · 30 / 60 / 200 MPa 평판 (속도 구동 · 도달 즉시 후퇴) ↔ 우리 300 MPa 서보 / hold · 공극의 뜻이 반대 (그들 = 전해액 통로 / 우리 = 결손).
- **나란히 놓을 숫자 (판정 없음)**: 이 논문 제하 뒤 공극 0.411 (30 MPa · 실험 0.412) · ≈0.319 (200 MPa) ↔ 랩 표준 순수 SE 300 MPa 기공 10–13 % — 다른 재료 · 다른 상 (복합 액체 LIB 전극) 이라 같은 줄의 비교 대상이 아니다.

---

## 17. 참고문헌 목록 (원문 그대로 · p.16 · 41 개)
(인쇄 그대로 — 원문 기울임은 옮기지 않았다 · 줄 끝 하이픈만 이었다 · 합자 'ﬂ' · 'ﬁ' 와 분리된 발음 부호 (´ · ¨) 는 글자로 합쳤다.  인쇄 특이점은 고치지 않는다: [7] [17] [30] [36] *'J. Power. Sources'* · [24] 권 자리에 '1882' · [25] *'J. Appl. Mech. 20, 327 (2021)'* — 권 20 과 연도 2021 의 짝은 [미확인].)

1. A. Manthiram, ACS Cent. Sci. 3, 1063 (2017).
2. J.M. Tarascon and M. Armand, Nature 414, 359 (2001).
3. J. Xu, X. Cai, S. Cai, Y. Shao, C. Hu, S. Lu, and S. Ding, Energy Environ. Mater. 6, e12450 (2023).
4. M. Abdollahifar, H. Cavers, S. Scheffler, A. Diener, M. Lippke, and A. Kwade, Adv. Energy Mater. 13, 2300973 (2023).
5. B.L. Trembacki, D.R. Noble, M.E. Ferraro, and S.A. Roberts, J. Electrochem. Energy Convers. Storage 17, 041001 (2020).
6. D. Wang, G. Wang, C. Xu, and H. Liu, J. Energy Storage 87, 111521 (2024).
7. H. Zheng, L. Tan, G. Liu, X. Song, and V.S. Battaglia, J. Power. Sources 208, 52 (2012).
8. C. Meyer, H. Bockholt, W. Haselrieder, and A. Kwade, J. Mater. Process. Technol. 249, 172 (2017).
9. Y. Sheng, C.R. Fell, Y.K. Son, B.M. Metz, J. Jiang, and B.C. Church, Front. Energy Res. 2, 56 (2014).
10. L. Zielke, T. Hutzenlaub, D.R. Wheeler, I. Manke, T. Arlt, N. Paust, R. Zengerle, and S. Thiele, Adv. Energy Mater. 4, 1301617 (2014).
11. R. Sim, S. Lee, W. Li, and A. Manthiram, ACS Appl. Mater. Interfaces 13, 42898 (2021).
12. J. Zhang, J. Sun, H. Huang, C. Ji, M. Yan, and Z. Yuan, Appl. Energy 373, 123900 (2024).
13. A. Luglio, K. Fink, F. Usseglio-Viretta, A. Colclasure, P. Walker, J.S. Mangum, and R. Brow, MRS Bull. 50, 1013 (2025).
14. R. Ge, A.M. Boyce, Y.S. Zhang, P.R. Shearing, D.J. Cumming, and R.M. Smith, Chem. Eng. J. 465, 142749 (2023).
15. X. Lu, A. Bertei, D.P. Finegan, C. Tan, S.R. Daemi, J.S. Weaving, K.B. O’Regan, T.M.M. Heenan, G. Hinds, E. Kendrick, D.J.L. Brett, and P.R. Shearing, Nat. Commun. 11, 2079 (2020).
16. P. Pietsch, M. Hess, W. Ludwig, J. Eller, and V. Wood, Sci. Rep. 6, 27994 (2016).
17. A.C. Ngandjong, T. Lombardo, E.N. Primo, M. Chouchane, A. Shodiev, O. Arcelus, and A.A. Franco, J. Power. Sources 485, 229320 (2021).
18. R. Ge, D.J. Cumming, and R.M. Smith, Powder Technol. 403, 117366 (2022).
19. C. Sangrós Giménez, B. Finke, C. Schilde, L. Froböse, and A. Kwade, Powder Technol. 349, 1 (2019).
20. C. Sangrós Giménez, C. Schilde, L. Froböse, S. Ivanov, and A. Kwade, Energy Technol. 8, 1900180 (2020).
21. M. Sonzogni, J.-M. Vanson, Y. Reynier, S. Martinet, K. Ioannidou, and F. Radjai, Powder Technol. 442, 119891 (2024).
22. M. Ebner, F. Geldmacher, F. Marone, M. Stampanoni, and V. Wood, Adv. Energy Mater. 3, 845 (2013).
23. P.A. Cundall and O.D.L. Strack, Géotechnique 29, 47 (1979).
24. H. Hertz, J. für die reine und angewandte Mathematik 1882, 156 (1882).
25. R.D. Mindlin and H. Deresiewicz, J. Appl. Mech. 20, 327 (2021).
26. D.O. Potyondy and P.A. Cundall, Int. J. Rock Mech. Min. Sci. 41, 1329 (2004).
27. Y. Lyu, S. Dong, L.T. Gao, and Z.-S. Guo, Int. J. Electr. Power Energy Syst. 165, 110521 (2025).
28. I. Srivastava, D.S. Bolintineanu, J.B. Lechman, and S.A. Roberts, ACS Appl. Mater. Interfaces 12, 34919 (2020).
29. R. Xu, H. Sun, L.S. de Vasconcelos, and K. Zhao, J. Electrochem. Soc. 164, A3333 (2017).
30. A.J. Stershic, S. Simunovic, and J. Nanda, J. Power. Sources 297, 540 (2015).
31. C. Sangrós Giménez, B. Finke, C. Nowak, C. Schilde, and A. Kwade, Adv. Powder Technol. 29, 2312 (2018).
32. M. Lippke, T. Ohnimus, F. Frankenberg, C. Schilde, and A. Kwade, Powder Technol. 444, 119984 (2024).
33. J. Zhang, J. Qiao, K. Sun, and Z. Wang, Particuology 61, 18 (2022).
34. Y. Song, K. Gao, C. He, Y. Wu, S. Yang, N. Li, L. Yang, Y. Mao, W.-L. Song, and H. Chen, Appl. Energy 351, 121904 (2023).
35. A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Ning, J. Marrow, F.H. Richter, J. Janek, and A. Latz, ACS Appl. Mater. Interfaces 12, 9277 (2020).
36. P. Zhu, D. Gastol, J. Marshall, R. Sommerville, V. Goodship, and E. Kendrick, J. Power. Sources 485, 229321 (2021).
37. J. Zhang, H. Huang, and J. Sun, Powder Technol. 409, 117828 (2022).
38. N. Iqbal, I.U. Haq, and S. Lee, Int. J. Mech. Sci. 216, 107034 (2022).
39. J. Christoffersen, M.M. Mehrabadi, and S. Nemat-Nasser, J. Appl. Mech. 48, 339 (1981).
40. Y.-T. Liu, S. Liu, G.-R. Li, and X.-P. Gao, Adv. Mater. 33, 2003955 (2021).
41. E.J. Berg, C. Villevieille, D. Streich, S. Trabesinger, and P. Novák, J. Electrochem. Soc. 162, A2468 (2015).

---

## 보강 기록 (2026-11-16 작업 · 1저자 2026-11-12 요청 · 68-1 번 파일)

| 항목 | 내용 |
|---|---|
| 이번에 쓴 PDF | `b73aa282-68-1._Investigation_into_Microstructural_and_Mechanical_Evolution_During_Lithium-Ion_Battery_Cathode_Calendering_via_X-ray_Tomography-Based_Discrete_Element_Method.pdf` (16 쪽 · sha256 `617be4da097af013b2bc9482beee8604c6e6ebadaefee5bafbeb9e6e2d5b1712` · PDF 메타데이터 생성 2026-09-19) — 메타 줄의 옛 파일 (`2fa0a4ea-1._…`) 과 그림 래스터 xref 12 개 (29 · 52 · 65 · 73 · 80 · 89 · 98 · 106 · 107 · 112 · 119 · 123) 가 모두 같은 판 · 옛 파일의 sha 는 기록이 없어 바이트 동일은 [미확인] |
| 서지 대조 | 첫 쪽 (제목 · 저자 넷 · Xiangtan University · *JOM* · DOI · © 2026 TMS · 특집 *Advances in Energy Materials Research: Fundamentals and Applications* · Received May 1, 2026 · accepted August 25, 2026) = 카드 §0 · 지시서 메모와 같다 · 권 · 쪽은 여전히 인쇄 없음 · **다른 점 하나 — 카드 L33 '온라인 2026-09-21' 은 이 PDF 에 없다** (정정 표지) |
| 대조한 범위 | 원문 16 쪽 전부 (텍스트 층 + 식 · 그림 · 표 쪽 렌더) ↔ 카드 §0 · §1 · §2 · §2.5 · §3.1–3.11 · §4.1–4.8 · §5 · §6 · §10 의 인쇄값 · 원문 인용 · 귀속 (한 줄씩) · 식 1–25 기호 (렌더 대조 · 카드 §4.2–4.3 · §6 의 식과 같음 — 식 2 의 −k_t · 식 1 감쇠항 + · 식 21 의 ξ̄ 확인) · Table I 다섯 값 · 그림 판독값 재판독 (Fig 2d 15 점 · 4b 17 점 · 4c 8 점 · 7 셋 · 10 일곱 · 12 다섯 = `digitized.csv` 55 행 — 카드 판독과 공극 ±0.002 (빨간 원에 가려 74 px 만 보이는 30 MPa 실험 점 제외) · 접촉 면적 ±2 µm² · 응력 ±0.4 MPa (막대 끝 편향 보정 뒤) · 에너지 밀도 ±2 Wh L⁻¹ 안에서 같다) · 참고문헌 41 개 (§17) · 같은 날 다른 카드 정독 기록의 zhang2026 지적 (batch_104 L92 · batch_118 L465–466 · L313 · L148–149 · batch_119 L54 · L96 · L139 · batch_120 L38 · L222 · batch_122 L97 · L307) 을 이 PDF 로 다시 확인 |
| 고친 것 (정정 표지 · 옛 표기 남김 · 4 곳) | L33 (온라인 날짜 — 원문에 없음) · L91 (refs 4–6 이 붙은 문장) · L222 (ref 30 귀속 범위 · 원문 문단 그대로) · L394 (우리 쪽 'Minnmann 순수 SE 10 % @300' 귀속 철회 = CLAUDE.md 원장 `CL-94`) |
| 더한 것 (보강 표지 · 14 곳 · 줄 수 그대로) | L37 · L38 (그 뒤 생긴 정본 카드) · L66 (코드 이름 검색 0 건) · L95 (인용 번호 없는 in situ CT 문장) · L97 (refs 19–21 원문) · L99 · L100 (p.4 '이진화' 문장) · L105 (Giménez · Lippke 원문) · L139 (인용 18 = 속도 값에만) · L157 (gel-type · *Instant adhesive* · as-prepared) · L164 (박리 시편의 압연 여부 불일치) · L294 (파단 판정 문장 없음) · L466 (Ebner 조성 · 압력 = Zhang 원문에 없음) · L472 (ref 30 원문 카드) |
| 새 절 | §14 보강 의도 대조 (참고 23 행) · §15 원문 문장 대조 (DEM 한계 · 소성 · 차원 · 탈압) · §16 자세한 분석 (계획 이름별) · §17 참고문헌 목록 (원문 그대로 41 개) · 이 절 |
| [미확인] 을 닫은 것 | L465 'Ebner 전극 조성 미기재' · L466 '압력 집합이 Ebner 와 같은지' → **Zhang 원문에 없음** 으로 닫음 (값 = `ebner2013_*` 카드 기록) · L472 'ref 30 원문 미확인' → `stershic2015_*` 카드 · L38 '안 읽은 것' 가운데 넷 (Ebner · Ge · Stershic · Sonzogni) → 정본 카드 |
| 새로 연 [미확인] | 온라인 날짜의 근거 (L33) · 저자가 Ebner 분할을 다시 이진화했는지 (L100) · 박리 시편이 압연 전극인지 (L164) · 인용 번호 없는 in situ CT 문장의 귀속 (L95) · 참고 [25] 의 권 · 연도 짝 (§17) |
| 남은 [미확인] (원문에 없음) | 권 · 쪽 · 코드 · 입자 수 · 시간 간격 · κ̄* · c̄ · CBD 물성 · 벽 마찰 · 감쇠 계수 정의 · 공극 계산 관례 · DEM 박리 경계 조건 · (Ē*, σ̄, λ̄) 의 보정 표적 · 실험 캘린더링 방법 · 실험 공극 측정법 · Fig 4c 'Experiment' 출처 · Fig 5–7 이 하중 중인지 |
| 크롭 | **13 → 62** — 원래 13 장 (Fig 1–12 + Table I) 을 모두 다시 열어 봄 (잘린 축 · 캡션 섞임 · 빠진 그림 · 표 없음 → 다시 자른 것 0) · 더한 것 = 식 **25** 장 (식 1–25 · 400 dpi) + 근거 문단 **20** 장 (400 dpi · 카드가 인용한 문장만) + 패널 **4** 장 (Fig 2d · 3b · 4b · 4c) · `figures.json` f2 캡션에 섞여 있던 본문 글을 걷어 냄 (옛 문자열은 `caption_original_auto`) · `digitized.csv` 55 행 (새 파일) |
| 정독 출력 | `litdb/_curation/reading/batch_123.tsv` · `batch_123_findings.md` (질문 a–n · 카드 문제) |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
