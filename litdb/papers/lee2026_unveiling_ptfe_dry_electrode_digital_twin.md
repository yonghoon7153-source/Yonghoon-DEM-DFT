<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = miss2026_insitu_conductivity_porosity_pressure_compaction.md · 같은 연구실 계보 = hong2026_sulfide_cathode_binder_digitaltwin.md · kim2025_conductive_agent_se_coating_cathode.md.
     쪽 표기 = 본문 "p.N" (본문 PDF N 쪽 = 인쇄 "N of 16") · SI "SI p.N" (SI PDF N 쪽 = SI 아래쪽 인쇄 번호).
     값 표지: [인쇄] = 본문 · SI · 그림 범례에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 손 판독, 막대 ±0.5 %p · 용량 ±2 mAh/g) ·
     [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · 다른 카드 · 메인 리포 값과 엮은 계산 · [미확인] = 원문 (본문 + SI 전수) 에 없음 · [추정] = 우리 해석.
     원문 36 쪽 (본문 16 + SI 20) = 텍스트 층 전수 대조 + 그림 33 · 표 3 = 크롭 36 장 전부 렌더로 열람.  1저자 요청: 팔로우하는 랩의 논문 — insight · 브리핑 강화. -->

# PTFE 건식 양극의 구조적 이점을 FIB-SEM 3D 디지털 트윈으로 정량 — 0.2 wt% PTFE 가 LPSCl 을 NCM 위에 in situ 코팅 (NCM 표면 LPSCl 몫 35 → 59 %) · 상 분산 균질화 · 이온/전자 경로 개선 (기하 τ 2.16 → 1.75 · σ_ion 시뮬 +57 % / 실측 +61 % · σ_e 약 2 배) — Jongjun Lee · Rakhwi Hong · Hyeon-Ji Shin · … · Matthew T. McDowell · Hun-Gi Jung · Yong Min Lee (Small 2026, "Unveiling … via 3D Microstructure-Resolved Analysis")

> slug `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · DOI `10.1002/smll.75974` · type `exp + voxel-sim (FIB-SEM 3D 재구성 · U-Net 분할 · GeoDict ConductoDict FVM σ_e/σ_ion · BatteryDict/BEST 반쪽셀 2 C; DEM/MPM 없음)` · PDF `aadb168b-4._Unveiling_the_Structural_Advantages_in_PTFE_Based_Dry_Processed_Electrodes_for_Sulfide_Based_All_Solid_State_Batteries_via_3D_Microstructure_Resolved_Analysis.pdf` · SI `29772169-4._Sup_Unveiling_the_Structural_Advantages_in_PTFE_Based_Dry_Processed_Electrodes_for_Sulfide_Based_All_Solid_State_Batteries_via_3D_Microstructure_Resolved_Analysis.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Unveiling the Structural Advantages in PTFE-Based Dry-Processed Electrodes for Sulfide-Based All-Solid-State Batteries via 3D Microstructure-Resolved Analysis* (p.1)
> **저자 (본문 p.1 · SI p.1 이 같다)**: Jongjun Lee¹˒² · Rakhwi Hong³ · Hyeon-Ji Shin⁴ · Hyemin Kim³ · Jaejin Lim¹ · Seungwon Jung³ · **Matthew T. McDowell²˒⁵\*** · **Hun-Gi Jung⁴˒⁶\*** · **Yong Min Lee¹˒³˒⁷\*** (\* 교신 3 인 · J. Lee · R. Hong · H.-J. Shin 공동 1저자 — p.1)
> ¹ Department of Chemical and Biomolecular Engineering, Yonsei University, Seoul, Republic of Korea · ² George W. Woodruff School of Mechanical Engineering, Georgia Institute of Technology, Atlanta, Georgia, USA · ³ Department of Battery Engineering, Yonsei University, Seoul, Republic of Korea · ⁴ Energy Storage Research Center, Korea Institute of Science and Technology, Seoul, Republic of Korea · ⁵ School of Materials Science and Engineering, Georgia Institute of Technology, Atlanta, Georgia, USA · ⁶ Department of Energy Science, KIST-SKKU Carbon-Neutral Research Center, Sungkyunkwan University, Suwon, Republic of Korea · ⁷ Department of Battery Conflation Engineering, Yonsei University, Seoul, Republic of Korea
> **어느 랩인가**: 교신 = **이용민 (연세대 화공생명 · 배터리공학 · 배터리융합공학)** · **Hun-Gi Jung (KIST 에너지저장연구센터 · KIST-SKKU)** · **Matthew T. McDowell (Georgia Tech 기계 · 재료)**.  이용민 그룹 = litdb 정본 연구실 트리아지 `yonsei_dtbl_lab_triage_2026.md` 가 "Digital Twin Battery Lab" 으로 적은 그룹 (논문 자체에는 연구실 이름이 없다).  1저자 J. Lee 는 연세 + Georgia Tech 겸 소속 · 같은 사람의 이전 카드 = `lee2023_sicspe_digitaltwin_assb` (1저자) · `kim2025_conductive_agent_se_coating_cathode` (공동 1저자).  저자 기여 (p.14): 개념화 = J. Lee · Y. M. Lee / 소프트웨어 = R. Hong · J. Lim · S. Jung / 조사 · 데이터 = H.-J. Shin · H. Kim / 감수 = McDowell · H.-G. Jung.
> *Small* **2026**, 0:e75974 (조기 공개 · 권 미정 · 본문 16 쪽 + SI 20 쪽, SI 원본 = `smll75974-sup-0001-SuppMat.docx`) · 접수 2026-07-28 · 수정 09-06 · 승인 09-18 (p.1) · Open Access **CC BY-NC** (p.1) · 연구비 NST GTL24012-000 (MSIT) · KIAT RS-2024-00436106 (MOTIE) (p.14) · 이해상충 없음 · 데이터 = 요청 시 (p.14).
> **같은 연구실 계보 카드 (링크만 — 내용 베끼지 않음)**: [`park2020_digitaltwin_assb_foundational`](park2020_digitaltwin_assb_foundational.md) (본문 ref 13 · 같은 LiNbO₃-NCM711 + LPSCl 계) · [`lee2023_sicspe_digitaltwin_assb`](lee2023_sicspe_digitaltwin_assb.md) (ref 14) · [`kim2024_digital_twin_acsenergyletters`](kim2024_digital_twin_acsenergyletters.md) (ref 41 · top-down/bottom-up 분류) · [`lim2025_virtual_calendering_framework`](lim2025_virtual_calendering_framework.md) (ref 50) · [`kim2025_conductive_agent_se_coating_cathode`](kim2025_conductive_agent_se_coating_cathode.md) (인용 안 됨 · **같은 NCM711 · LPSCl 로 일부러 한 SE 선코팅 50–500 nm**) · [`hong2026_sulfide_cathode_binder_digitaltwin`](hong2026_sulfide_cathode_binder_digitaltwin.md) (인용 안 됨 · PTFE 1 wt% 건식 vs NBR 습식 · GrainGeo 합성 트윈) · [`oh2026_bimodal_composite_cathode`](oh2026_bimodal_composite_cathode.md) (Hun-Gi Jung 교신 · H.-J. Shin 공저).
> **판독 원자료**: `litdb/figures/lee2026_unveiling_ptfe_dry_electrode_digital_twin/digitized.csv` (손 판독 · 정밀도는 파일 머리말) · 크롭 36 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 조성 (NCM : LPSCl : VGCF = 85 : 13 : 2 wt%) 에서 PTFE 0.2 wt% 를 넣고 100 °C 손 혼합 · 압연한 건식 양극을 FIB-SEM (화소 20.83 nm · 슬라이스 50 nm · 25 µm 정육면체) 으로 재구성하면, **재구성 LPSCl 부피분율은 그대로 (23.5 ↔ 23.6 %)** 인데 NCM 표면의 LPSCl 몫이 35 → 59 % · LPSCl 하위부피 SD 15.0 → 13.6 · 무작위 추출 Li⁺ 경로의 기하 τ 2.16 → 1.75 · 전류가 거의 없는 LPSCl 복셀 14.4 → 4.2 % 로 바뀌고, **같은 재구성 위 복셀 FV 가 σ_ion +57 % · σ_e +101 % 를 준다** (실측 +61 % · +105 %) — 부피가 아니라 **배치**가 수송을 바꿨다는 근거다 (p.4 · p.7–9 · Table S2).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 이종기술 논지 (코팅 → 분산 → 압축 뒤 3D 이온 경로) 의 실험 짝? | **방향은 짝이다** — in situ SE 코팅 + LPSCl 국소 응집 감소 + 이온 경로 개선이 같은 재구성 안에서 정량된다.  단 코팅을 만든 것은 **PTFE 섬유의 가둠 + 전단** (Fig. S7) 이지 표면 에너지 (논지 §2) 가 아니고, 논문 해석은 **활성 계면 면적** (논지의 "하지 않는 말") 을 앞세운다 | [인쇄] p.4 · p.7–9 · §8-1 |
| ② 그들 "tortuosity" 2.16 / 1.75 는 우리 어느 양? | **기하학적 tortuosity (τ_geo)** = 무작위로 뽑은 Li⁺ 경로 20 개의 평균 길이 ÷ 25 µm.  수송 tortuosity 가 아니다.  같은 논문 숫자로 계산한 **수송 tortuosity (tau2) = 5.34 / 3.42** (시뮬) · 실측 기준 7.8 / 4.9 (σ₀ 1.0 mS/cm 가정) | [인쇄] p.7–8 · [우리 산술] §3-12 |
| ③ 복셀 FV (= 우리 `CONTACT_FREE` 가지, CL-81) 의 실측 격차는? | 실제 재구성 위 σ_ion 시뮬 ÷ 실측 = **1.46 · 1.42** (계면 · 입계 · 미해상 기공 몫 ≈ 30 %) — **입력 σ_LPSCl 0.1 S/m (1.0 mS/cm, 출처 미기재) 에 조건부**.  같은 구조에 우리 σ₀ 1.5 · 3.0 을 넣으면 2.1–2.2 · 4.3–4.4 배 | [인쇄] Fig. 4g · Table S2 · [우리 산술] |
| ④ PTFE 규약 (CL-60 centerline) · Lee 2025 대조 (R = 2.074 · Q = 0.840)? | PTFE 의 지배 효과가 ≤ 0.2 wt% 에서는 **구조 (분산 · 치밀화 · SE 코팅)**, 0.5–1.0 wt% 에서는 0.2 wt% 정점 대비 손실 (1.0 wt% 의 σ_e 는 0.0 wt% 보다도 낮다).  0.5 → 1.0 wt% σ_e 비 **0.70** (밀도 −4.3 %p 포함) = 우리 모델 Q 0.840 과 Lee 곡선 보간 0.44 **사이**.  재구성은 PTFE 를 분할하지 않았다 (Table S1 "−") | [인쇄] Table S2 · Table S1 · [우리 산술] |
| ⑤ σ_VGCF (CL-47) · σ_NCM 입력? | GeoDict 입력 **VGCF 8300 S/m (= 83 S/cm) · NCM 0.9 S/m (= 0.9 × 10⁻² S/cm)** · VGCF 를 복셀로 해상 → σ_e 시뮬 ÷ 실측 0.99 · 0.97.  두 입력 출처는 미기재 | [인쇄] p.13 · Fig. 3g · [미확인] 출처 |
| ⑥ 대칭셀 계획 (`docs/symmetric_cell_ionic_plan_20261013.md`) 에 쓸 것? | 전자 차단 Li/LPSCl/전극/LPSCl/Li EIS + 이온 차단 Ti/전극/Ti DC 50 mV 의 두 셀 분리 규약 · NCM 85 wt% 에서 σ_ion 0.030–0.049 mS/cm.  측정 중 압력 · 반복 수 · 적합 회로 · 순수 LPSCl 펠릿 σ₀ 는 **없다** | [인쇄] p.13 · Table S2 · [미확인] |
| ⑦ 후막 ("건식 후막") 에서 이점이 커지나? | 45 mg cm⁻² (139 µm) 에서 100 회 유지율 86.8 vs 74.8 % (격차 12.0 %p) — 25 · 35 mg cm⁻² 에서는 3.9 · 1.5 %p (단조 아님).  미세구조 시뮬은 **25 µm 두께만** | [인쇄] p.11 · [우리 산술] |

⛔ **한정어 (떼지 말 것)**: ① NCM 은 **LiNbO₂-피복 (원문 표기) Li(Ni₀.₇Co₀.₁₅Mn₀.₁₅)O₂, D50 7 µm 단봉** — 우리 PC 9 µm + SC 4 µm 바이모달과 다르다 ② 재구성 = **전극마다 25 µm 정육면체 1 개** (NCM D50 의 약 3.6 배) — 반복 · RVE 수렴 [미확인] ③ PTFE · VGCF 분산 · 밀도 (상대밀도 84.6 → 87.4 %) 가 함께 바뀐다 — 시뮬은 재구성 안 부피분율이 같아 배치 효과를 떼지만, 실측 +61 % 에는 밀도 몫이 섞인다 (§10-6) ④ Fig. 1c ("0.0PTFE 안의 NCM") = Fig. S7a ("예비 혼합 분말") **같은 사진** (§10-1) ⑤ 전도도 측정 압력 · 시료 수 [미확인].

---

## 1. 한 줄 요약

PTFE 를 **0.2 wt%** 만 넣고 건식으로 반죽 · 압연하면, 섬유화된 PTFE 가 LPSCl 입자를 NCM 근처에 **가둬** 전단으로 부수고 문질러 **100–500 nm LPSCl 코팅을 그 자리에서 만든다** (Fig. 1 · S3 · S7).  FIB-SEM 디지털 트윈 (GeoDict) 으로 재면 NCM 표면의 LPSCl 몫이 35 → 59 %, VGCF · NCM · LPSCl 분포가 고르게 되고 (하위부피 SD 감소), 같은 재구성 위 FV 계산에서 σ_e 는 0.92 → 1.85 × 10⁻² S cm⁻¹, σ_ion 은 4.4 → 6.9 × 10⁻⁵ S cm⁻¹ 로 오른다 (실측 0.93 → 1.91 × 10⁻² · 3.01 → 4.85 × 10⁻⁵).  전지는 첫 방전 180.2 → 189.5 mAh g⁻¹, 200 회 유지율 90.2 → 97.5 %, 45 mg cm⁻² 에서 3.6 mA cm⁻² 에 6.42 mAh cm⁻².  PTFE 를 0.5 · 1.0 wt% 로 늘리면 밀도 · σ_e · σ_ion · 용량이 다시 내려간다 (Table S2 · Fig. S16).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM/CA/바인더) | 연구유형 |
|---|---|---|---|---|
| J. Lee · R. Hong · H.-J. Shin (공동 1) · H. Kim · J. Lim · S. Jung · **M. T. McDowell\*** · **H.-G. Jung\*** · **Y. M. Lee\*** (연세 · Georgia Tech · KIST · 성균관) | *Small* 2026, 0:e75974 · CC BY-NC | 10.1002/smll.75974 | **Li₆PS₅Cl** (POSCO JK Solid Solution, D50 1 µm) · **LiNbO₂-피복 NCM (Ni 0.7 · Co 0.15 · Mn 0.15, D50 7 µm, 원문 표기)** · **VGCF** (Showa Denko) · **PTFE** 0 · 0.2 · 0.5 · 1.0 wt% | 실험 (건식 전극 · SEM/EDS · FIB-SEM · 전도도 · 반쪽셀 · OEP · XPS) + **측정 구조 위 복셀 시뮬** (GeoDict 2025 MatDict · ConductoDict · BatteryDict + BESTmicro).  **DEM · MPM · 공정 시뮬 없음** |

- 키워드 (p.1): composite electrode · digital twin · dry electrode · FIB-SEM tomography · PTFE · solid-state batteries · sulfide electrolyte.
- 트리아지 목록 (`yonsei_dtbl_lab_triage_2026.md` #260–286) **밖** — 2026-09 승인 논문이라 목록 작성 뒤.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 조성 · 공정 · 셀

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| CAM | **LiNbO₂-coated** Li(Ni₀.₇Co₀.₁₅Mn₀.₁₅)O₂ "NCM", D50 7 µm — Table S3 은 "NCM711".  ⚠ "LiNbO₂" 는 p.2 · p.13 두 곳 다 아래첨자 2 (렌더 확인) — 같은 연구실의 같은 NCM711 을 `park2020_digitaltwin_assb_foundational` · `kim2025_conductive_agent_se_coating_cathode` 는 LiNbO₃ 피복으로 적는다 → 오식 가능성 [추정] | [인쇄] p.2 · p.13 · SI p.18 |
| SE | Li₆PS₅Cl (POSCO JK Solid Solution) D50 **1 µm** (전극용) · SE 층용 LPSCl D50 **5 µm** | [인쇄] p.13 |
| CA | VGCF (Showa Denko) — 지름 · 길이 [미확인] (재구성 · 크롭에서 지름 ≈ 0.1–0.2 µm 로 보임 [판독, 정성]) | [인쇄] p.13 |
| 바인더 | PTFE powder (공급사 · 입경 [미확인]) 0.0 · 0.2 · 0.5 · 1.0 wt% — 이름 xPTFE | [인쇄] p.2 · p.13 |
| 조성 | NCM : LPSCl : VGCF = **85 : 13 : 2 wt%** + PTFE (위에 더함 → 0.2PTFE 의 NCM 84.83 wt% [우리 산술] = Table S3 "84.8 wt%") | [인쇄] p.2 · p.13 · SI p.18 |
| 혼합 · 성형 | 막자 사발 예비 혼합 10 min → PTFE 추가 → **손 혼합 100 °C · 20 min** → 반죽 → 원하는 두께로 압연 → 자립 막 (p.13).  p.2 는 "additional 20 min of mortar mixing" (온도 없음) · Fig. 1a 모식은 혼합기 + 롤 (실제 공정과 다른 그림) | [인쇄] p.2 · p.13 |
| 자립 막 | 접어도 균열 없음 (Fig. S1 — 약 4 × 4 cm [판독]) · XRD 상 부반응 없음 (Fig. S2) | [인쇄] p.2–3 |
| 상 밀도 | NCM 4.44 · LPSCl 1.86 · VGCF 2.10 · PTFE 2.06 g cm⁻³ → 0.2PTFE 이론 밀도 **3.686 g cm⁻³** [우리 산술] | [인쇄] SI p.17 |
| 셀 | LPSCl 150 mg (D50 5 µm) → ⌀13 mm PEEK 몰드 70 MPa 펠릿 → 전극 올려 **370 MPa · 5 min** → Li 200 µm (Honjo) → **적층압 50 MPa** 로 시험 | [인쇄] p.13 |
| σ_e 셀 | **이온 차단** Ti/전극/Ti (전극 370 MPa 펠릿) · DC **50 mV** (BioLogic VSP-300) | [인쇄] p.13 |
| σ_ion 셀 | **전자 차단** Li/LPSCl/전극/LPSCl/Li (전극 370 MPa → 양쪽 LPSCl 분말 → 다시 370 MPa) · EIS 14.1 mV · 5 MHz–10 mHz | [인쇄] p.13 |
| 측정 중 압력 · 시료 수 · 등가회로 · 전극 지름 · 두께 | [미확인] (본문 · SI 전수) | — |

### 3-2. 3D 재구성 · 부피분율 (Fig. 2a–c · Table S1 · p.4 · SI p.17)

| 시료 · 방법 | NCM | LPSCl | VGCF | PTFE | 기공 | SE/고체 [우리 산술] |
|---|---|---|---|---|---|---|
| 0.0PTFE · 밀도 기반 (bulk) | 59.8 | 21.8 | 3.0 | 0.0 | **15.4** | 25.8 % |
| 0.0PTFE · 3D 재구성 | 60.1 | 23.5 | 3.5 | − | **12.9** | 27.0 % |
| 0.2PTFE · 밀도 기반 | 61.5 | 22.5 | 3.1 | 0.3 | **12.6** | 25.7 % |
| 0.2PTFE · 3D 재구성 | 61.2 | 23.6 | 3.3 | − | **11.9** | 26.8 % |

- 단위 vol% [인쇄].  Table S1 의 시료 칸 "0.02TFE" 는 원문 오타 (= 0.2PTFE).
- 저자 판정: *"matched well … validating the reliability of the reconstruction"* (p.4).  [우리 산술] 기공 차 = **−2.5 %p (0.0PTFE) · −0.7 %p (0.2PTFE)** · LPSCl 차 +1.7 · +1.1 %p — 재구성이 기공을 적게 · LPSCl 을 많이 잡는 방향 (Minnmann 2024 의 "분할 기공 < 기하 기공" 과 같은 방향 — `minnmann2024_microstructure_porosity_visualization`).
- **PTFE 는 분할되지 않았다** (네 상 = NCM · LPSCl · VGCF · 기공) → 시뮬 격자에 PTFE 상이 없다 (PTFE 가 어느 상으로 분류됐는지 [미확인]).
- 기하: FIB 밀링 50 nm 간격 · SEM 화소 **20.83 nm** · 약 500 회 → **25 × 25 × 25 µm³** (폭 × 두께 × 깊이) · 두께 방향 = y · 밀링 방향 = z (p.4 · p.13 · Fig. 2a).  Fig. 2a 범례는 "Voxel size: 20 nm" — 실제 복셀은 20.83 × 20.83 × 50 nm 비등방 [우리 산술].
- 재구성 시료: 0.0 · 0.2PTFE 를 **370 MPa · 5 min** 가압 뒤 (p.13) — 시료 질량 로딩 · 원 전극 두께 [미확인].

### 3-3. NCM 표면 피복 · in situ LPSCl 코팅 (Fig. 1 · Fig. 2d–f · S3–S7 · p.3–4)

| 지표 | 0.0PTFE | 0.2PTFE | 표지 · 쪽 |
|---|---|---|---|
| NCM 표면 중 LPSCl 몫 | **35 %** | **59 %** | [인쇄] p.4 · Fig. 2d |
| NCM 표면 중 VGCF 몫 | 3 % | 2 % | [인쇄] p.4 |
| NCM 표면 중 기공 몫 | **62 %** | **39 %** | [인쇄] p.4 |
| NCM–LPSCl 계면 면적 비 | 1 | **1.69 ("69 % larger")** | [인쇄] p.4 · 59/35 = 1.686 [우리 산술] |
| SE 코팅층 두께 | 없음 (LPSCl 드문드문 부착, Fig. S4) | **100–500 nm** (본문) · Fig. S3 주석 44 개 = 중앙 **229 nm** · 평균 236 ± 105 · IQR 148–298 · 범위 67–449 nm | [인쇄] p.3–4 · [판독 — 주석 옮김 + 우리 산술] |
| PTFE 섬유 지름 | — | **20–50 nm** (입자 사이, Fig. 1e) | [인쇄] p.3 |
| PTFE 0.5 · 1.0 wt% 의 코팅 | — | 0.5 · 1.0PTFE 도 같은 100–500 nm — *"its content does not significantly influence the resulting coating layer morphology or thickness"* (Fig. S5) | [인쇄] p.4 |

- **세 몫 (LPSCl · VGCF · 기공) 합 = 100 %** → NCM–NCM 맞닿음 면은 분모에 없다 (같은 상으로 합쳐져 면이 안 생긴다) — 피복 정의 · 인접 판정 거리 [미확인 · 추정].
- 코팅 형성 기전 (Fig. S7 · p.4): 예비 혼합 분말 = LPSCl · VGCF 가 NCM 위에 고르지 않게 (S7a) → PTFE 추가 2 min = LPSCl · VGCF 가 섬유화된 PTFE 와 함께 NCM 주위에 얽힘 (S7b) → 10 min = 부서진 LPSCl 이 덩어리로 NCM 에 붙음 (S7c — *"not observed in the pre-mixed powder or 0.0PTFE powder"*) → 20 min = 코팅층 (S7d).  저자 해석: *"PTFE fibrils confined the LPSCl particles near the NCM through entanglement, preventing them from escaping the NCM surface and subjecting them to continuous shear deformation"* (p.4).
- 표면 SEM/EDS (Fig. S6 · p.4): 0.0PTFE (⚠ **70 MPa 로 누른 분말**) = 각진 NCM 표면 많음 · VGCF (C 지도) 뭉침 / PTFE 전극 (압연 막) = 매끈한 NCM · VGCF 고르게.  ⚠ 0.0PTFE 와 PTFE 전극의 성형 경로가 달라 표면 사진 비교에는 성형 차가 섞인다 [추정].
- 같은 랩의 다른 피복값: `hong2026_sulfide_cathode_binder_digitaltwin` (PTFE **1 wt%** · 75 : 22.5 : 1.5 · **GrainGeo 합성 트윈**, σ_ion 으로 보정) = 분말 35 % → PTFE 36 % (거의 그대로) — 이 논문 (측정 재구성 · PTFE 0.2 wt%) 의 35 → 59 % 와 **크게 다르다** (§10-11).

### 3-4. 상 분산 균질도 (하위부피 · z 투영) — VGCF · NCM · LPSCl (Fig. 3a–c · Fig. 4a–c · S8–S10 · S13 · p.6–7)

하위부피 = 25 µm 정육면체를 **10 × 10 × 10 = 1000 개의 2.5 µm 정육면체**로 나눈 것 (Fig. S8 · p.6).

| 지표 | 0.0PTFE | 0.2PTFE | 표지 · 쪽 |
|---|---|---|---|
| VGCF vol% 평균 / 중앙 / SD | 5.1 / 2.9 / **7.0** | 5.2 / 4.3 / **4.5** | [인쇄] p.7 · Fig. S9 |
| VGCF vol% CV (SD/평균) | 1.37 | 0.87 | [우리 산술] |
| VGCF 꼬리 (최댓값 근처) | **≈50 %** | **≈27 %** | [인쇄] p.7 |
| NCM vol% SD | 19.0 | 17.0 | [인쇄] p.7 · Fig. S10 |
| NCM–VGCF 접촉 영역 vol% 평균 / 중앙 / SD | 0.5 / 0.4 / 0.4 | 0.2 / 0.2 / 0.2 | [인쇄] p.7 · Fig. 3c |
| LPSCl z 투영 SVF 의 SD | 0.10 | **0.07** (0.15–0.30 SVF 에 **72.4 %**) | [인쇄] p.7 · Fig. S13 |
| LPSCl vol% SD (하위부피) | **15.0** | **13.6** | [인쇄] p.7 · Fig. 4c |

- 저자 판정: VGCF 탈응집 · 재분배 (*"continuous stretch–fold cycle appears to promote the dispersion of VGCF"* p.7) · NCM 분포 균일 · **LPSCl 국소 응집 억제** (*"the reduced frequency of the high-vol% regions reflects the suppression of local LPSCl aggregation"* p.7).
- 0.2PTFE 는 NCM–VGCF 접촉 **총량이 적은데도** 고르게 퍼져 전자 경로가 잘 이어진다 (p.7).
- ⚠ 정규화 문제 둘 [우리 산술 · §10-3]: (i) 같은 크기 정육면체 1000 개가 전체를 덮으면 하위부피 평균 = 전체 분율이어야 하는데 **VGCF 평균 5.1 · 5.2 vs 전체 3.5 · 3.3 vol%** (ii) S13 막대 가중 평균 ≈0.28 (0.0PTFE) · ≈0.24 (0.2PTFE) [판독] vs 재구성 LPSCl 0.235 · 0.236.  어느 쪽도 분모 정의가 없다.
- ⚠ 2.5 µm 정육면체 < NCM D50 7 µm → NCM vol% 는 정육면체마다 0 또는 100 에 가깝게 갈라지기 쉽다 = SD 가 **입자 크기 ÷ 칸 크기**에 크게 걸린다.  무작위 혼합 기준 (S_R²) · 완전 분리 기준 (S₀²) 이 없어 15.0 → 13.6 같은 차이를 "무작위에서 얼마나 먼가" 로 옮길 수 없다 (§8-2).
- [판독] Fig. 4b (0.2PTFE) 의 x ≈ 21–23 µm · y ≈ 10–13 µm 에 SVF ≈0.6–0.75 국소 LPSCl 기둥이 하나 있다 (0.0PTFE 지도에는 그만한 점이 없다) — 본문 무언급.

### 3-5. 전자 수송 (Fig. 3d–g · S11 · S12 · p.7)

| 지표 | 0.0PTFE | 0.2PTFE | 표지 · 쪽 |
|---|---|---|---|
| σ_e 시뮬 (ConductoDict) | **0.92 × 10⁻² S cm⁻¹** | **1.85 × 10⁻² S cm⁻¹** ("approximately twice") | [인쇄] p.7 · Fig. 3g |
| σ_e 실측 (DC 50 mV) | 0.93 × 10⁻² | 1.91 × 10⁻² | [인쇄] Table S2 · Fig. S12 |
| 시뮬 ÷ 실측 | 0.99 | 0.97 | [우리 산술] |
| NCM 안 전류밀도 0–1 × 10⁴ A m⁻² 칸 | ≈26.7 % | ≈16.3 % | [판독] Fig. 3f (전 칸 = digitized.csv) |
| NCM 안 전류밀도 1–4 × 10⁴ A m⁻² 칸 합 | ≈61.6 % | ≈71.0 % | [판독] Fig. 3f |
| DC 전류 (50 mV) | ≈25.6 mA | ≈54.6 mA | [판독] Fig. S12 |

- Fig. 3d · S11: 0.0PTFE 는 높은 전류 (주황 = 색 상한 10 × 10⁴ A m⁻²) 가 정육면체 한 면 (y 작은 쪽) 근처 NCM · VGCF 덩어리에 몰린다 · 0.2PTFE 는 VGCF 망 (S11 주황 실) 이 고르게 퍼져 있다 [판독].
- [우리 산술] 평균 겉보기 전류 J = σ_eff · ΔV / L = 3.7 × 10⁴ (0.0) · 7.4 × 10⁴ A m⁻² (0.2) (ΔV 1 V · L 25 µm).  NCM 만으로 갈 수 있는 상한 (Wiener 병렬) = φ_NCM × 0.9 S m⁻¹ = 0.54 · 0.55 × 10⁻² S cm⁻¹ < 시뮬값 ⇒ **VGCF 가 낀 경로가 σ_e 의 41 % 이상 (0.0) · 70 % 이상 (0.2)** 을 낸다.

### 3-6. 이온 수송 (Fig. 4 · S13–S15 · p.7–9)

| 지표 | 0.0PTFE | 0.2PTFE | 표지 · 쪽 |
|---|---|---|---|
| Li⁺ 경로 (무작위 추출 n = 20) 평균 길이 | **54.1 µm** | **43.8 µm** | [인쇄] p.7–8 · Fig. S14 |
| 그 "tortuosity" (= 길이 ÷ 25 µm, **기하 τ**) | **2.16** | **1.75** | [인쇄] p.8 |
| 경로 길이 SD | 8.9 | 5.9 | [인쇄] p.8 |
| 경로 길이 분포 (5 µm 칸, 경로 수) | 40–75 µm (4 · 3 · 4 · 3 · 4 · 1 · 1) | 30–60 µm (3 · 1 · 9 · 5 · 1 · 1) | [판독] Fig. S14b — 칸 평균 · SD 가 인쇄값을 재현 |
| 전류가 거의 없는 LPSCl 복셀 (< 0.1 × 10³ A m⁻²) | **14.4 %** | **4.2 %** | [인쇄] p.8 · Fig. 4f |
| σ_ion 시뮬 | **4.4 × 10⁻⁵ S cm⁻¹** | **6.9 × 10⁻⁵ S cm⁻¹** (+57 %) | [인쇄] p.9 · Fig. 4g |
| σ_ion 실측 (전자 차단 EIS) | 3.01 × 10⁻⁵ | 4.85 × 10⁻⁵ (+61 %) | [인쇄] Table S2 · p.9 |
| 시뮬 ÷ 실측 | **1.46** | **1.42** | [우리 산술] |
| 전자 차단 셀 호 끝 | ≈1.8 kΩ | ≈1.1 kΩ | [판독] Fig. S15 |

- 저자 문장: σ_e 는 *"good agreement with the experimentally measured values"* (p.7) · σ_ion 은 *"experimentally measured conductivities also followed a consistent trend"* (p.9) — **이온은 절대 일치를 주장하지 않는다** (경향만).
- Fig. 4f x 축 칸 이름이 "< 0.1 · 0.1-1 · 2-3 · 3-4 · 4-5 · > 5" — **1–2 칸이 없고** 막대 합 ≈97 % [판독] → 칸 이름 오기로 보인다 [추정] · 이 카드는 인쇄된 < 0.1 칸 값 (14.4 · 4.2 %) 만 쓴다.
- [우리 산술] 문턱 0.1 × 10³ A m⁻² 의 상대 크기: LPSCl 상 안 평균 전류의 하한 J/φ = 749 (0.0) · 1169 A m⁻² (0.2) → 문턱 = 평균의 **0.13 · 0.09 배 이하** — 같은 절대 문턱이라 σ 가 큰 전극이 "비활성" 을 덜 세는 쪽으로 기운다 (§10-5).
- Fig. S14a: 경로 20 개가 위 → 아래로 가지 치며 내려가는 선 — 추출 알고리즘 (시작점 선택 · 최단 여부) [미확인].

### 3-7. PTFE 함량 계열 (Table S2 · Fig. S16 · S17 · p.9)

| PTFE wt% | 상대밀도 % | σ_e (S cm⁻¹) | σ_ion (S cm⁻¹) | 0.1 C 첫 방전 (mAh g⁻¹) |
|---|---|---|---|---|
| 0.0 | 84.6 | 0.93 × 10⁻² | 3.01 × 10⁻⁵ | 180.2 [인쇄] |
| **0.2** | **87.4** | **1.91 × 10⁻²** | **4.85 × 10⁻⁵** | **189.5** [인쇄] |
| 0.5 | 86.8 | 1.03 × 10⁻² | 3.40 × 10⁻⁵ | ≈186 [판독 S16] |
| 1.0 | 82.5 | 0.72 × 10⁻² | 2.95 × 10⁻⁵ | ≈183 [판독 S16] |

- 밀도 · 전도도 · 용량 모두 0.2 wt% 에서 최대 [인쇄 Table S2 · p.9].  저자: *"excessive PTFE increased electrode porosity and impeded mass transport"* (p.9).
- [우리 산술] 비: σ_e 0.2/0.0 = **2.05** · 0.5/0.0 = 1.11 · 1.0/0.0 = 0.77 · **1.0/0.5 = 0.70** / σ_ion 0.2/0.0 = **1.61** · 0.5/0.0 = 1.13 · 1.0/0.0 = 0.98 · 1.0/0.5 = 0.87.
- 재구성 · 시뮬은 0.0 · 0.2PTFE 두 개뿐 (0.5 · 1.0 없음).

### 3-8. 반쪽셀 전기화학 (Fig. 5 · S18 · p.9–10 · 프로토콜 p.14)

| 지표 | 0.0PTFE | 0.2PTFE | 표지 |
|---|---|---|---|
| 0.1 C 첫 방전 · 첫 쿨롱효율 | 180.2 mAh g⁻¹ · 83.5 % | **189.5 mAh g⁻¹ · 86.9 %** | [인쇄] p.9 · Fig. 5a |
| dQ/dV | H1→M (3.4–3.9 V) · H2→H3 (4.15–4.3 V) 봉우리에서 0.2PTFE 가 전류 크고 전압차 작음 | | [인쇄] p.9 · Fig. 5b |
| GITT 분극 (평탄 구간) | ≈0.22 V | ≈0.15 V | [판독] Fig. 5c |
| DC-IR 기울기 (ΔV vs i, 그림 인쇄 적합식) | ±0.1069 (충 · 방) | 0.0601 (충) · −0.0617 (방) | [인쇄] Fig. 5d — 본문 "약 0.11 · 0.06" (p.9) |
| DC-IR 면저항 | ≈107 Ω cm² | ≈60–62 Ω cm² | [우리 산술 — V per mA cm⁻² = kΩ cm²] |
| EIS 호 끝 (Li 반쪽셀) | ≈220 Ω | ≈85 Ω | [판독] Fig. 5e |
| DRT | D3 (CEI, 10²–10⁴ Hz) · D4 (양극 전하이동, 10¹–10² Hz) 세기 낮고 주파수 높음 · 방전 내내 유지 (in situ DRT) | | [인쇄] p.9–10 · Fig. 5f–h |
| 율속 (0.1 · 0.2 · 0.5 · 1 · 2 C) | ≈174 · 168 · 157 · 141 · 101 | ≈190 · 184 · 176 · 168 · 140 mAh g⁻¹ | [판독] Fig. 5i |
| 0.5 C 방전 (0.2 C 충전) 200 회 유지율 | 90.2 % | **97.5 %** | [인쇄] p.9 · Fig. 5j |

- DRT 칸 정의 (p.9): D1 10⁵–10⁷ Hz SE 벌크 · 입계 / D2 10⁴–10⁵ 음극 SEI / D3 10²–10⁴ CEI / D4 10¹–10² 양극 전하이동 / D5 10⁰–10¹ Li 금속 표면 / D6 10⁻²–10⁰ Warburg (MATLAB DRTtools, Wan 2015).
- 프로토콜 (p.14): 예비 사이클 0.1 C · 2.5–4.3 V · 4 회 (CC/CV 충전 · CC 방전 · 25 °C) · DC-IR = SOC 50 % 에서 10 s 펄스 + 30 min 휴지 (0.025 → 1 C) · GITT 0.5 C 60 s + 2 h 휴지 (3.0 V 까지) · 율속 = 0.1 C 충전 · 0.1–2.0 C 방전 · 수명 = 0.2 C 충전 / 0.5 C 방전 · 사이클러 WonAtech WBCS3000Le32.
- Fig. 5 셀의 질량 로딩 [미확인] — Fig. 5i 판독값은 Fig. S27 의 25 mg cm⁻² 계열과 같다 [판독].

### 3-9. 사이클 뒤 · OEP · XPS (Fig. S19–S21 · p.9–11)

- **OEP** (NCM/LTO, LTO 음극 = LPSCl : LTO : VGCF 45 : 47 : 8 wt% · 0.2 C · 25 °C · **10 MPa** · 압력센서 분해능 0.1 kg — p.9 · p.14): 첫 사이클 ΔP 최저 ≈ −0.44 MPa (0.0) · ≈ −0.22 MPa (0.2) · 방전 끝 ≈ −0.33 · −0.12 MPa [판독 Fig. S19].  저자: 0.2PTFE 가 *"notably smaller pressure decrease"* — 큰 활성 면적 · 고른 분포가 응력을 고르게 나눈다는 해석 (p.9–10).  용량당 정규화 없음 [미확인].
- 주 전기화학은 **적층압 50 MPa** · 저압 (10 MPa) 거동은 후속 (p.10).
- **사이클 뒤 단면** (Fig. S20 — 200 회 뒤): 0.0PTFE = LPSCl 덜 보임 · 기공 많음 · NCM–LPSCl 접촉 불량 · **NCM 균열** / 0.2PTFE = 코팅층 유지 · 기공 적음 · *"no noticeable cracks"* (p.10–11).
- **XPS** (Fig. S21 — SI 캡션 "after 20 cycles"): S 2p · P 2p 에서 0.0PTFE 는 P₂Sₓ · Li₂S (· "Li_{x−1}P") 분해 성분이 크고 0.2PTFE 는 PS₄³⁻ 위주 (p.11).  SI 캡션의 "(b) 0.0PTFE … (d) 0.0PTFE" 는 오기 (패널 제목 = 0.2PTFE).

### 3-10. 측정 구조 위 반쪽셀 시뮬 — 2 C 방전 (Fig. S22–S26 · p.11 · p.13–14)

- 모델: 재구성 양극 (25 µm) + 가상 Cu 집전체 · Li 금속 · SE 층 · Al 집전체 (GeoDict 2025 BatteryDict) · **2 C 정전류 · 2.5 V 끝** · 풀이기 BESTmicro (Fraunhofer ITWM) (p.13–14 · Fig. S22).  SE 층 두께 · 반응 상수 · 확산계수 · OCP 등 입력 [미확인].
- 결과 (방전 끝): 0.0PTFE = 집전체 쪽 전자 전류 몰림 (S23a) · 이온 전류가 굵은 몇 통로에 몰림 (S23b) · 표면 과전압 더 음 (S24) · 집전체 쪽에 덜 리튬화된 영역 (S25) · 두께 방향 Li⁺ 농도 경사 (S26: DoD 90 에서 ≈35.8 → 30.5 × 10³ mol m⁻³ [판독]) / 0.2PTFE = 고른 전류 · 과전압 작음 · 고른 리튬화 · 경사 작음 (DoD 90 에서 ≈36.0 → 32.2, 가운데 혹 [판독]).
- 저자: *"Given that these simulations were performed on a 25 µm thick model, these behaviors will be exacerbated as electrode loading increases"* (p.11) — **두꺼운 전극 시뮬은 하지 않았다**.

### 3-11. 후막 (Fig. 6 · S27 · Table S3 · p.11–12)

| 면적 로딩 (mg cm⁻²) | NCM 로딩 | 두께 (0.2PTFE) | 겉보기 밀도 · 상대밀도 [우리 산술] | 첫 면적 용량 0.2 / 0.0 (mAh cm⁻²) | 100 회 유지율 0.2 / 0.0 |
|---|---|---|---|---|---|
| 25 | 21.2 | 78 µm | 3.21 g cm⁻³ · 0.87 | **3.98** / 3.69 | **99.2** / 95.3 % |
| 35 | 29.7 | 109 µm | 3.21 · 0.87 | **5.72** / 5.22 | **95.2** / 93.7 % |
| 45 | 38.2 | 139 µm | 3.24 · 0.88 | **7.24** / 6.58 | **86.8** / 74.8 % |

- [인쇄] p.11 · Fig. 6a–d · g–h.  유지율 격차 3.9 · 1.5 · **12.0 %p** [우리 산술] — 단조 아님.  면적 용량 비 1.08 · 1.10 · 1.10 [우리 산술].
- 45 mg cm⁻²: 0.0PTFE 는 0.2 C (1.3 mA cm⁻²) 넘어서 급락 · 0.2PTFE 는 0.5 C (3.6 mA cm⁻²) 까지 완만 (p.11 · Fig. 6e).  0.2PTFE 45 mg cm⁻² = **7.26 · 6.42 · 3.93 mAh cm⁻² @ 0.7 · 3.6 · 7.2 mA cm⁻²** (p.11 · Table S3 0.72 · 3.62 · 7.24) = 190 · 168 · 103 mAh g⁻¹ [우리 산술].
- S27 율속 [판독, mAh g⁻¹, 0.1 · 0.2 · 0.5 · 1 · 2 C]: 0.0PTFE 45 = 174 · 168 · 134 · 61 · 20 / 0.2PTFE 45 = 190 · 184 · 168 · **103** · 44 (400 dpi 재판독 — 오른쪽 CE 축과 혼동 주의).  Fig. 6e · f 에는 2 C 점이 없다.
- [우리 산술] C-rate 기준 = **셀마다 자기 0.1 C 용량**: 7.24 mAh cm⁻² × 0.1 · 0.5 · 1 = 0.72 · 3.62 · 7.24 mA cm⁻² (Table S3) · 0.0PTFE 의 0.2 C = 6.58 × 0.2 = 1.32 mA cm⁻² (본문 "1.3").  ⇒ 같은 C-rate 에서 0.0PTFE 가 **약 9 % 낮은 전류**로 시험됐다 (그림 6e · f 는 전류밀도 축이라 공정).
- Table S3 (SI p.18) 비교 9 편 — 같은 연구실 [4] Hong 2022 (Y. M. Lee 공저) · KIST [7] Shin 2025 · [9] D. Lee 2024 Nat Commun 포함.  "this work" 행 = NCM711/Li · Li₆PS₅Cl · 45.0 · 38.2 (84.8 wt%) · 25 °C.

### 3-12. 우리 산술 묶음 (이 논문 숫자만으로)

| 양 | 0.0PTFE | 0.2PTFE | 식 · 가정 |
|---|---|---|---|
| f (시뮬) = σ_eff / σ_LPSCl 입력 | 0.044 | 0.069 | σ_LPSCl 입력 0.1 S m⁻¹ = 1.0 mS cm⁻¹ (p.13) |
| **수송 tortuosity (tau2) — 시뮬** | **5.34** | **3.42** | φ·σ₀/σ_eff, φ = 재구성 LPSCl 0.235 · 0.236 |
| √tau2 (시뮬) | 2.31 | 1.85 | 제곱근 — 수송 tortuosity 아님 |
| tau2 ÷ τ_geo² | 1.14 | 1.12 | τ_geo = 2.16 · 1.75 (경로 20 개 평균) |
| 수송 tortuosity — 실측 (재구성 φ · bulk φ) | 7.81 · 7.24 | 4.87 · 4.64 | σ₀ = 1.0 mS cm⁻¹ **가정** (순수 LPSCl 펠릿 측정 없음) |
| σ_ion 시뮬 ÷ 실측 · 빠진 저항 몫 | 1.46 · 32 % | 1.42 · 30 % | 1 − 실측/시뮬 · σ₀ 1.0 조건부 |
| 같은 비 · σ₀ 1.5 · 3.0 이었다면 | 2.19 · 4.39 | 2.13 · 4.27 | 시뮬 σ 가 σ₀ 에 정비례 |
| σ_e 시뮬 ÷ 실측 | 0.99 | 0.97 | — |
| VGCF 낀 경로의 σ_e 몫 하한 | ≥ 0.41 | ≥ 0.70 | 1 − φ_NCM·0.9 S m⁻¹ / σ_e,sim |
| 밀도만으로 σ_ion 이 오를 수 있는 폭 (실측 +61 % 와 대조) | — | ×1.05 (Bruggeman 1.5) · ×1.14 (우리 생산 폼의 (φ − φc)^½, φc 0.195) · ×1.70 (지수 2) | bulk LPSCl 21.8 → 22.5 vol% · 문턱 근처 가정 [추정] |
| SE/고체 부피비 | 27.0 % (재구성) · 25.8 % (bulk) | 26.8 % · 25.7 % | Table S1 |

---

## 4. ★ 방법 — 영상 · 분할 · 지표 · 시뮬 · 입자 처리

### 4-1. FIB-SEM 토모그래피 (p.4 · p.13 · Fig. 2a)
- 장비 FEI **Helios NanoLab 600** · 밀링 50 nm 간격 · SEM 화소 **20.83 nm** · 약 500 장 · 25 × 25 × 25 µm³.  시료는 370 MPa · 5 min 가압 뒤 (전지 조립 압력과 같다).
- 표면 SEM/EDS = Hitachi S-4800 FE-SEM/EDX (p.13).

### 4-2. 분할 · 재구성 (p.4 · p.13)
- 대표 슬라이스를 **손으로 라벨** → **U-Net CNN** 학습 (회색조 + 국소 질감 입력) → 전 슬라이스 자동 분할 → 쌓아 3D (ref 46–48).  상 = NCM · LPSCl · VGCF · 기공 (PTFE 없음).
- 검증 = 부피분율 대 밀도 기반 계산 (Table S1) **하나**.  분할 정확도 지표 (IoU 등) · 학습 슬라이스 수 · 커튼 무늬 보정 [미확인].

### 4-3. 구조 지표 (GeoDict 2025 MatDict + MATLAB R2024a · p.4–8 · p.13)
- 상 부피분율 · NCM 표면 피복 (LPSCl/VGCF/기공 몫) · NCM–LPSCl 계면 시각화 (Fig. 2e–f).
- z 투영 SVF 지도 (VGCF · LPSCl) + 그 히스토그램 (S13).
- **하위부피 (2.5 µm × 1000) vol% 히스토그램** → 평균 · 중앙 · SD · 꼬리 (VGCF · NCM · LPSCl · NCM–VGCF 접촉 영역) — 근거 ref 51 · 52 (Müller 2021 · Kellers 2023 REV 흐름).
- **Li⁺ 퍼콜레이션 경로**: LPSCl 상 안에서 무작위로 20 개 추출 → 길이 히스토그램 → 길이 ÷ 25 µm = "tortuosity" (S14).

### 4-4. 유효 전도도 · 전류 분포 — ConductoDict (p.13)
- **FVM** · y (두께) 방향 Dirichlet **ΔV = 1 V** · σ_eff = J·L / (φ_in − φ_out) (J = 입출구 면 평균 전류).
- 고유 전도도 (298.15 K): **NCM 0.9 S m⁻¹ · VGCF 8300 S m⁻¹ (전자) · LPSCl 0.1 S m⁻¹ (이온)** — 출처 [미확인].  전자 풀이에서 LPSCl · 이온 풀이에서 NCM 의 값 (0 으로 둔 것으로 읽힘) [추정].
- 계면 · 입계 저항 항 없음 (같은 상 복셀은 이어 붙음) — 우리 STEP3 와 같은 범주 (`CONTACT_FREE`, CL-81).

### 4-5. 반쪽셀 전기화학 시뮬 — BatteryDict + BESTmicro (p.13–14)
- 측정 구조 그대로 (25 µm) + 가상 집전체 · Li · SE 층 → 2 C 정전류 방전 · 2.5 V 끝.  전기화학 입력 · 검증 [미확인].

### 4-6. 전기화학 · 기계 측정 — §3-1 · §3-8 · §3-9 참조.

### 4-7. 입자 처리 ★ (우리 축 언어로)
- **모델 입자 없음** — 측정한 실제 입자 모양 (각진 다면체 NCM 이차입자 · 부서지고 문질러진 LPSCl · 섬유 VGCF) 을 복셀로 그대로 쓴다.
- 변형 양식 (SEM 근거): LPSCl = **진짜 형상 소성 · 파쇄** (부서진 LPSCl 이 NCM 에 붙어 100–500 nm 막으로 펴짐 — 우리 frame[1] MPM 쪽 물리, 그리고 **혼합 단계의 전단**에서 생긴다) · NCM = 사이클 뒤 균열 (0.0PTFE) · PTFE = 20–50 nm 섬유 (분할 안 됨).
- ⇒ 우리 DEM 의 강체 구 + 접촉 소성 (겹침 δ 대리) 으로는 **코팅을 만들 수 없다** — 코팅 상태는 우리 쪽에서 입력 (LC 팔의 같은 γ 표면) 이지 결과가 아니다.

### 4-8. 기법 미니 용어집
- **디지털 트윈 (이 논문)** = 측정 (FIB-SEM) 재구성 구조 = Kim 2024 (`kim2024_digital_twin_acsenergyletters`) 분류의 **하향식 (top-down / reconstruction)** · 우리 DEM+MPM = 상향식 (bottom-up / formation).
- **SVF (solid volume fraction) 투영 지도** = 각 (x, y) 열에서 한 상이 차지하는 z 방향 분율.
- **하위부피 분포 분석** = 큰 부피를 같은 정육면체로 나눠 칸마다 상 분율을 히스토그램으로 — 우리 믹서의 Lacey 칸 분산과 같은 계열 (단 정규화 없음).
- **OEP (operando electrochemical pressiometry)** = 일정 체적 셀의 압력 변화로 전극 부피 변화를 읽는 법 (영변형 LTO 음극).
- **DRT** = 임피던스를 이완 시간 분포로 풀어 과정별 저항을 가르는 법.
- **GITT · DC-IR** = 펄스 뒤 전압 변화로 분극 · 내부저항.

---

## 5. Figure set ★ (크롭 36 장 = `litdb/figures/lee2026_unveiling_ptfe_dry_electrode_digital_twin/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 건식 공정 모식 (PTFE 섬유화 · stretch-folding · 얽힘 → in situ 코팅 · 균질 분포 → 막 · 적층 · 캘린더) (b) 맨 NCM (c) 0.0PTFE 안 NCM (⚠ = S7a 예비 혼합 사진) (d) 0.2PTFE 안 NCM (= S7d) (e) 0.2PTFE 단면 (점선 = 코팅층) (f) Ni (g) S EDS | 코팅 형태 정성 · 우리 LC (코팅) 팔의 실물 그림 |
| 2 | (a) FIB-SEM → 분할 → 재구성 흐름 (b) 0.0 · 0.2PTFE 트윈 + 상별 (c) 부피분율 (d) **NCM 표면 피복 35/3/62 vs 59/2/39** (e, f) NCM–LPSCl 계면 (빨강) 3D + 2D 단면 | ★ 피복 정의 · 단면 — 우리 coverage 와 정의 대조 (§7-3) |
| 3 | (a, b) VGCF z 투영 SVF (c) NCM–VGCF 접촉 영역 하위부피 히스토그램 (d, e) NCM 안 전자 전류 3D · 2D (f) 전류 히스토그램 (g) σ_e 시뮬 막대 + 실측 점 | ★ VGCF 분산 → σ_e 2 배 — Lee 2025 대조 R 의 다른 후보 (§8-5) |
| 4 | (a, b) LPSCl z 투영 SVF (c) LPSCl 하위부피 히스토그램 (d, e) LPSCl 안 이온 전류 3D · 2D (f) 이온 전류 히스토그램 (⚠ 1–2 칸 없음) (g) σ_ion 시뮬 + 실측 | ★ "비활성 SE" 지표 · 실구조 FV ↔ EIS 격차 1.4–1.5 배 |
| 5 | (a) 0.1 C 첫 충방전 (b) dQ/dV (c) GITT + 분극 (d) DC-IR ΔV–i (적합식 인쇄) (e) Nyquist (f) DRT (g, h) 방전 중 DRT 지도 (i) 율속 (j) 200 회 수명 | 성능 지표 (우리 STEP4 대조용 정성) |
| 6 | (a–c) 25 · 35 · 45 mg cm⁻² 단면 + S 지도 (78 · 109 · 139 µm) (d) 로딩별 첫 충방전 (e) 비용량 vs 전류밀도 (f) 면적 용량 vs 전류밀도 (g, h) 100 회 면적 용량 (i) 문헌 비교 | 후막 — 우리 6 mAh (≈111 µm) 침대와 같은 두께대 |
| S1 | 0.2PTFE 자립 막 (준비 · 접음 · 편 뒤) | 막 성형성 |
| S2 | XRD (NCM · LPSCl · 0.0 · 0.2PTFE) — 부반응 없음 | — |
| S3 | 0.2PTFE 단면 SEM 4 시야 + BSE · **코팅 두께 주석 44 개** | ★ 코팅 두께 분포 (중앙 229 nm) — MPM SE 막 두께의 실물 표적 |
| S4 | 0.0PTFE NCM 단면 + Ni · S (⚠ 캡션 패널 표지 f · g ↔ 실제 b · c) | 코팅 없는 기준 |
| S5 | 0.2 · 0.5 · 1.0PTFE 단면 + Ni · S — 코팅 모두 있음 | PTFE 함량과 코팅 두께 무관 |
| S6 | 표면 SEM + Ni · S · C 지도 (0.0 · 0.2 · 0.5 · 1.0PTFE) — 0.0 = VGCF 뭉침 (⚠ 0.0 은 70 MPa 분말) | VGCF 분산 정성 |
| S7 | 0.2PTFE 혼합 시간 열 (예비 · 2 · 10 · 20 min) | ★ 코팅 형성 경로 — 우리 믹서 DEM 에 없는 기전 (§8-1) |
| S8 | 하위부피 분할 모식 (10 × 10 × 10 · 2.5 µm) | ★ 우리 침대에서 같은 지표 계산 설계 (§7-3) |
| S9 | VGCF 하위부피 vol% 히스토그램 | 정규화 질문 (§10-3) |
| S10 | NCM 하위부피 vol% 히스토그램 | 칸 < 입자 크기 문제 |
| S11 | NCM–VGCF 상 전자 전류 3D · 2D | VGCF 망이 전류를 실어 나름 |
| S12 | DC 분극 (50 mV) 0.0 · 0.2PTFE | σ_e 실측 원자료 |
| S13 | LPSCl 투영 SVF 히스토그램 | 72.4 % 재현 · 평균 정규화 질문 |
| S14 | (a) LPSCl → Li⁺ 경로 추출 모식 (b) 경로 길이 히스토그램 (위 축 = 기하 τ) | ★ τ_geo 정의 — 우리 `tortuosity_SE_wall` 대조 |
| S15 | 전자 차단 셀 Nyquist | σ_ion 실측 원자료 |
| S16 | PTFE 4 종 0.1 C 첫 충방전 | PTFE 최적 0.2 wt% |
| S17 | (a) PTFE 4 종 DC 분극 (b) 전자 차단 Nyquist — 범례에 σ 값 | Table S2 원자료 |
| S18 | DC-IR 펄스 전압 (0.0 · 0.2) | — |
| S19 | NCM/LTO OEP 전압 + ΔP | ΔP −0.44 vs −0.22 MPa [판독] |
| S20 | 200 회 뒤 단면 + Ni · S | 0.0PTFE NCM 균열 · LPSCl 분해 |
| S21 | XPS S 2p · P 2p (20 회 뒤) (⚠ 캡션 오기) | 분해 성분 정성 |
| S22 | 반쪽셀 트윈 모델 (음극 · LPSCl 층 · 건식 전극 · 집전체) | 우리 STEP4 대응 |
| S23 | 2 C 방전 끝 전자 · 이온 전류 지도 | 집전체 쪽 몰림 (0.0PTFE) |
| S24 | 표면 과전압 지도 (흐림 — 정성만) | — |
| S25 | 리튬화 상태 지도 | 0.0PTFE 집전체 쪽 미리튬화 |
| S26 | 두께 방향 Li⁺ 농도 (DoD 10–90) | 25 µm 모델만 |
| S27 | 로딩별 율속 (0.0 · 0.2PTFE) | 후막 율속 판독 |
| Table S1 | 부피분율 bulk vs 재구성 (⚠ "0.02TFE") | ★ 재구성 검증의 유일한 정량 |
| Table S2 | PTFE 4 종 상대밀도 · σ_e · σ_ion | ★ 실측 앵커 (§8-6 · §8-8) |
| Table S3 | 문헌 9 편 대비 면적 용량 · 전류 · CAM 로딩 | 성능 위치 |

## 6. Post-processing ★
- **무엇을**: 분할 (U-Net) → 부피분율 · 피복 · 투영 SVF · 하위부피 히스토그램 (평균 · 중앙 · SD · 꼬리) · 무작위 경로 길이 → τ_geo · FV 전류장 → σ_eff · 전류 히스토그램 · "비활성" 복셀 분율 · 반쪽셀 전기화학 장 (과전압 · 리튬화 · 농도).
- **도구**: GeoDict 2025 (MatDict · ConductoDict · BatteryDict) · BESTmicro · MATLAB R2024a · DRTtools (Wan 2015) · 그림 = 히스토그램 + 커널 밀도선 (S9 · S10 · Fig. 3c · 4c) [판독].
- **안 한 것**: 무작위 혼합 기준 정규화 · RVE 수렴 · 재구성 반복 · 분할 오차 · 전도도 반복 · 측정 압력 · 순수 LPSCl σ₀ · 두꺼운 전극 시뮬 · 0.5 · 1.0PTFE 재구성.
- **우리 후처리 (이 카드)**: §3-12 산술 (f · tau2 · 격차 · Wiener · 문턱 상대 크기 · 밀도 몫) · S3 코팅 두께 통계 · S13 · S14 칸 재현 · Fig. 1c = S7a 상관 0.967 (회색조 · 240 × 180 축소 · 교차 대조 −0.03).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 구조의 출처 | 측정 (FIB-SEM, 압축 뒤) — **하향식** | DEM 압밀 (강체 구 · hooke/hysteresis · E_eff 1.35 GPa) + MPM (J2 · E 1.53 · σ_y 0.30 3D) — **상향식** | 그들 = 실물 · 1 침대 / 우리 = 예측 · 많은 침대 (`positioning_vs_geodict.md`) |
| SE 형상 변화 | 진짜 형상 소성 · 파쇄 → 100–500 nm 코팅 | DEM = 없음 (겹침 δ 가 대리) · MPM = 압축 중 공극 채움 흐름 (혼합 전단 없음) | ⛔ 코팅은 frame[1] (MPM) 쪽 물리 + **혼합 단계** — 우리 둘 다 혼합 전단 소성은 없다 |
| 공극 (압축 뒤) | 재구성 11.9–12.9 % · 밀도 기반 12.6–15.4 % (370 MPa) | real_14 실험 15.6 % @ 300 MPa · 강체 구 하한 ≈20 % (소성 없이는 못 내려감) | 그들 값은 소성 흐름이 있는 실물 — E 연화가 그 대리라는 우리 frame[2] 서술과 정합 · 조성 · 입경 다름 |
| SE/고체 | 25.7–27.0 vol% | real_14 ≈27 % (CLAUDE.md 2026-06-17) · ps45 ≈35 % (AM 고체 64.7–64.9 %, `PS45E-01`) | real_14 와 거의 같은 SE 몫 — 피복 비교의 짝은 real_14 |
| 피복 | NCM 표면 LPSCl 몫 35 % (0.0) · 59 % (0.2) — 20.83 nm 복셀 인접 · NCM–NCM 면 제외 [추정] | real_14 기하 (Fibonacci 표면 + SE 중심): 맞닿음 (gap ≤ 0) **16 %** ≈ Hertz 18 % · 0.14 µm 띠 **49 %** ≈ Tabor 52 % · MPM 소성 AM_P 52 / 74 % (Hertz · Tabor 띠) | 그들 무코팅 35 % 는 우리 맞닿음 (16–18 %) 과 띠 (49–52 %) **사이** · 코팅 59 % 는 띠보다 위 — 정의 (판정 거리 · 분모) 다름 [우리 산술] |
| σ_ion 해법 | 복셀 FVM (ConductoDict) · 계면 항 없음 | (가) 접촉망 Kirchhoff + Holm/Maxwell 협착 (Hertz 주 · Physics/Tabor 감도) (나) STEP3 복셀 FV (`CONTACT_FREE`, CL-81) | 그들 = 우리 (나) 와 같은 범주 · 우리 (가) 의 협착 항은 그들에게 없다 |
| σ_ion 크기 | 실측 0.030–0.049 mS cm⁻¹ (NCM 85 wt%, 370 MPa, PTFE 0–1 wt%) | ps45 Hertz 0.0587–0.0893 mS cm⁻¹ (σ₀ 1.5 보고 기준 · NCM 81.6 wt% · 300 MPa · 바인더 · 탄소 없음) | 같은 자릿수 · CAM 많은 쪽이 낮은 방향 [추정] |
| 수송 tortuosity (tau2) | 시뮬 3.42–5.34 · 실측 4.6–7.8 (σ₀ 1.0 가정) [우리 산술] | ps45 Hertz 5.03–7.24 · Tabor (감도) 2.78–4.12 · 협착 뺀 CF 1.25–1.79 (φ_SE 0.28–0.30) | 그들 시뮬 값이 우리 Tabor–Hertz 띠 **안** — φ · 조성 다름 · 자릿수 대조까지 |
| 기하 τ | 무작위 경로 20 개 평균 길이 / 25 µm = 2.16 · 1.75 | `tortuosity_SE_wall` = 접촉망 Dijkstra 벽-벽 최단 (LHS 130 범위 1.29–4.15) | 둘 다 τ_geo 계열 · 그들은 무작위 · 우리는 최단 — 같은 이름으로 섞지 않는다 |
| σ_e | 시뮬 = 실측 (±3 %) · VGCF 해상 · VGCF 83 S/cm · NCM 0.9 × 10⁻² S/cm | STEP3: σ_VGCF 100 (vox 0.15 에서 직경보존 78.54) · σ_NCM 1.0 × 10⁻² S/cm (CL-92 각주) · 접촉망 σ_AM 50 mS/cm (모델 기준값, CL-92) | STEP3 입력은 그들과 **같은 자릿수** · 우리 VGCF 는 격자 아래 (선 스탬프) |
| PTFE | 분할 안 됨 (0.3 vol%) · 섬유 20–50 nm | centerline 한 셀 절연 (CL-60) · 실제 PTFE 부피의 0.40–0.41 · 표면 코팅 없음 · PTFE_D 0.25 µm = rope 계급 (CL-66) | 그들은 PTFE 를 아예 안 넣었다 → 우리 규약이 더 많이 표현한다 · 둘 다 PTFE 의 **구조 효과**는 없다 |
| 두께 | 시뮬 25 µm · 전극 78–139 µm | ps45 ≈111 µm 전체 두께 침대 | 우리 = 전체 두께 해상 수송 가능 (§8-7) |
| 반복 | 재구성 · 측정 n 미기재 | ps45 조성마다 시드 1 · LHS 194 | 둘 다 반복 산포 약함 |

### 7-2. 3D 미세구조 분석 방법 — 그들 vs 우리 (단계별)
| 단계 | 이 논문 (하향식) | 우리 DEM → 접촉망 | 우리 MPM → STEP3 복셀 | 메모 |
|---|---|---|---|---|
| 구조 획득 | FIB-SEM 500 장 · 20.83 × 20.83 × 50 nm · 25 µm³ 정육면체 1 개 | LIGGGHTS 압밀 덤프 (구 중심 · 반지름) · 전체 두께 · 주기 측면 | MPM 상 격자 (예: n_grid 384 · vox 0.15 µm 계열) + 첨가제 씨앗 | vox 0.15 µm 대비 면 안 약 7 배 · 슬라이스 방향 3 배 곱다 [우리 산술] — VGCF · 코팅 · 목 해상 |
| 분할 | U-Net (손 라벨 학습) · 4 상 | 필요 없음 (상 = 라벨) | 필요 없음 · PTFE = centerline 스탬프 | 분할 오차 = 그들만의 불확도 원천 (Table S1 기공 −2.5 %p) |
| 부피 · 공극 | 복셀 계수 · 밀도 기반 대조 | `porosity_union_exact_pct` (정확 합집합 MC) · ε_sphere | 격자 계수 | 관례 차 (union ↔ 구 부피 합) 를 늘 병기 (CLAUDE.md 2026-08-12 정정) |
| 피복 | NCM 표면 인접 상 몫 (판정 거리 = 1 복셀 [추정]) | `coverage_AM_*_hertz_pct` (접촉 원판) · 기하 띠 (real_14) | MPM 변형 SE 점 근접 (plastic vs rigid) | 판정 거리 · 분모 정의를 맞춰야 수가 같은 양이 된다 |
| 연결성 | 무작위 경로 20 개 · 비활성 (저전류) 복셀 | 퍼콜레이션 (관통) · `top_reachable_pct` · `ionic_active_pct` · `se_largest_comp_frac` (위상 기준) | 복셀 연결 성분 | 그들 = 전류 기준 · 우리 = 위상 기준 (§8-3) |
| 수송 | FVM ΔV 1 V · σ_eff = J·L/Δφ | Kirchhoff 망 · Holm 협착 (FULL / CF / 협착만 세 가지) → f · tau2 | FV ∇·(σ∇φ) = 0 (계면 항 0 · ① r_int 기구는 기본 끔) | 우리 (가) 만 접촉 단위 협착을 가진다 |
| 전기화학 | BatteryDict + BEST 2 C (25 µm) | — | STEP4 (BV + 구형 확산 · PyBaMM 패리티 대기) | 그들 = 측정 구조 위 · 우리 = 예측 구조 위 |
| 공정 | 측정만 (혼합 시간 열은 SEM 정성) | DEM 믹서 (SJKR 점착 · Lacey) · 압밀 | MPM 압밀 | 우리만 공정 → 구조를 계산한다 · 혼합 중 SE 파쇄 · 문지름은 둘 다 없다 |

### 7-3. ★ 그들 지표 중 우리 침대로 계산할 수 있는 것
| 그들 지표 | 우리 대응 · 이미 있는 키 / 도구 | DEM 침대 | STEP2/3 격자 | 해야 할 일 |
|---|---|---|---|---|
| 상 부피분율 · 공극 | `porosity_union_exact_pct` · `phi_se_mass_conserving` · `se_of_solid_vol` | ✅ 있음 | ✅ 있음 | 그들 표 형식 (bulk 대 구조) 으로 나란히 |
| NCM 표면 LPSCl · VGCF · 기공 몫 | `coverage_AM_*_hertz_pct` · real_14 기하 띠 · MPM 변형 coverage | ✅ (판정 거리를 20–50 nm 로 바꿔 한 번 더) | ✅ (1 복셀 인접 · NCM–NCM 면 제외 분모로) | 정의를 그들에 맞춘 판을 **추가** (기존 정의는 그대로) |
| 하위부피 vol% 히스토그램 (2.5 µm × 1000) | 없음 (믹서에는 Lacey 칸 분산이 있다) | ⬜ 구를 복셀화해 계산 가능 | ⬜ 바로 가능 | 무작위 혼합 S_R² · 분리 S₀² 를 같은 칸 크기로 함께 (§8-2) |
| z 투영 SVF 지도 · 히스토그램 | 없음 | ⬜ 가능 | ⬜ 가능 | 평균 = 부피분율 검산을 같이 |
| NCM–VGCF 접촉 영역 분포 | STEP3 VGCF 스탬프 격자 | ✗ (DEM 침대에 VGCF 없음) | ⬜ Lee · Phase A 침대 | §8-5 |
| Li⁺ 경로 길이 → τ_geo | `tortuosity_SE_wall` (Dijkstra · 중앙값 판 `tortuosity_SE_wall_median`) | ✅ 있음 (최단) | ⬜ 복셀 경로 | 무작위 시작점 판 + **전류 가중 경로 길이** (ps45 README ② — 결과 전 등록 먼저) |
| 유효 σ (FV) | STEP3 σ_ion · σ_e | — | ✅ 있음 | CL-81 한정어 유지 |
| 전류 히스토그램 · 비활성 SE 분율 | `scripts/network_current.py dump` (간선 전류) · STEP3 전류장 | ⬜ 노드 처리량으로 계산 가능 | ⬜ 가능 | 문턱 = 평균 대비 비율로 (§8-3) |
| 반쪽셀 전기화학 장 | STEP4 | — | ✅ (BV · 확산) | 25 µm 대신 전체 두께로 (§8-7) |
| 코팅 두께 분포 | 없음 | ✗ (강체 구) | △ MPM SE 막 두께는 원리상 가능 · 혼합 전단 없음 | 표적 = 중앙 229 nm (S3) |
| OEP ΔP | 없음 (A10 원장 후처리만) | ✗ | ✗ | — |

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실측 구조 (압축 뒤) · 그 위 복셀 수송 (σ_e · σ_ion) · 상 분포 통계 · 반쪽셀 장 · 실측 전도도 · 전기화학 · OEP.
- **없는 것**: 공정 → 구조 예측 (혼합 · 압축 모델 없음) · 접촉 단위 저항 · 응력 · 변형장 · 두꺼운 전극 해상 시뮬 · 반복 통계 · PTFE 상.
- ⇒ 우리 DEM (접촉망 수송 · 패킹 · 혼합) 과 MPM (형상 소성) 각각에 **실측 대조 지표**를 준다 — 특히 "같은 부피분율에서 배치만 바뀌면 σ 가 얼마나 바뀌나" 의 실물 크기 (σ_ion +57 % · σ_e +101 % 시뮬).

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 이종기술 논지의 실험 짝 — 단 프레이밍은 빌리지 않는다.**
- 논문: 같은 SE 총량 (13 wt%) 에서 0.2 wt% PTFE 가 in situ LPSCl 코팅 (100–500 nm · S3 중앙 229 nm) 을 만들고 (p.3–4), 재구성 LPSCl 부피분율이 같은데 (23.5 ↔ 23.6 %) LPSCl 국소 응집 감소 (하위부피 SD 15.0 → 13.6 · 투영 SD 0.10 → 0.07, p.7) · 기하 τ 2.16 → 1.75 (p.8) · 비활성 SE 복셀 14.4 → 4.2 % (p.8) · σ_ion 시뮬 +57 % / 실측 +61 % (p.9).
- 우리에게 뜻: 메인 리포 `docs/hetero_thesis.md` 비준 블록 (2026-10-05) 의 사슬 "SE 선코팅 → 혼합 응집 감소 → 분산 → 압축 뒤 3D 이온 경로" 와 **방향이 같은 3D 정량 사례**다 — 특히 예측 P3 (혼합 상태 차이가 압축 뒤 SE 경로 · σ_ion 차이로 이어진다) 의 실물 쪽 근거.  그러나 ① 코팅을 만든 것은 **PTFE 섬유의 가둠 + 전단** (Fig. S7) 이고 논지 §2 의 표면 에너지 차가 아니다 ② 논문의 설명 축은 **활성 계면 면적** — 논지의 "하지 않는 말" (계면 면적 · 보호막 효과) 이다 ③ P1 (비코팅에서 혼합 시간을 늘려도 SE–SE 응집이 무작위보다 크게 남는다) 은 시험하지 못한다 — 0.0PTFE 혼합 시간 열이 없고 Fig. 1c 가 예비 혼합 사진이다 (§10-1) ④ γ_NCM/γ_SE (논지 §2-8 판가름 수) 정보 없음.  [추정]
- ★ 새 함의 [추정]: 논지의 무대는 "건식" 이고 우리 랩 건식 전극은 PTFE 를 쓴다 — **PTFE 자체가 in situ SE 코팅을 만든다면, 실험의 "비코팅" 대조군은 이미 부분 코팅 상태**일 수 있다.  선코팅 효과의 실측 크기는 PTFE 함량에 따라 작아질 수 있다.
- 할 일: (a) 논지 관련 문장에는 이 논문의 **이온 경로 지표 (τ_geo · 비활성 분율 · 같은 φ 에서의 σ_ion)** 만 인용하고 활성 면적 서술은 빌리지 않는다 (b) 실험 설계 시 선코팅 유무 비교를 **PTFE 함량 고정 + PTFE 없는 분말 대조** 두 축으로 (c) `hetero_thesis.md` §6 배경 문헌 후보로 올릴지 = 1저자 (이 카드는 고치지 않는다) (d) P3 시험 때 LC ↔ 비코팅 팔의 압축 침대에 이 논문 지표 (§7-3) 를 같이 계산 — Otani 2025 (`otani2025_dem_se_dispersion_aggregation_compression`) 의 "응집 상태를 심고 누르기" 설계와 짝.

**8-2. 균질도 지표는 무작위 기준으로 정규화해야 크기를 말할 수 있다 — 우리 믹서 교훈 그대로.**
- 논문: 2.5 µm 하위부피 SD — LPSCl 15.0 → 13.6 · NCM 19.0 → 17.0 · VGCF 7.0 → 4.5 (p.7).  무작위 혼합 · 완전 분리 기준 없음 · 칸 (2.5 µm) 이 NCM D50 (7 µm) 보다 작다 · VGCF 평균 5.1 · 5.2 ≠ 전체 3.5 · 3.3 vol% (정규화 미기재).
- 우리에게 뜻: 메인 리포 믹서 캠페인이 같은 함정을 밟았다 — 칸 분산에는 위 상한 (Popoviciu 0.25/S_R²) 과 무작위 바닥 (S_R²) 이 있어 16 × 16 × 4 칸에서 천장 3.94–4.10 이 문턱 5 아래였다 (CLAUDE.md 믹서 줄 · 2026-09-23).  SD 차 1.4 (15.0 → 13.6) 가 "응집 억제" 인지, 칸 크기 대비 입자 크기 효과의 변동인지 이 자료로는 갈리지 않는다.  논지 §2-3 ⚠ 의 "응집은 무작위 대비로 잰다" 와 같은 요구다.
- 할 일: 우리 침대 (DEM 구 복셀화 · STEP2 격자) 에서 같은 지표를 낼 때 **원 SD + 같은 칸 크기의 S_R² · S₀² + Lacey M** 을 함께 · 평균 = 전체 분율 검산 · 칸 크기 사다리 (1.25 · 2.5 · 5 µm) 로 크기 의존 보고.  저자에게 정규화 질문 (§10-3).

**8-3. 그들의 "tortuosity" 는 기하 τ — 같은 논문 숫자로 수송 tortuosity 를 내면 우리 Hertz–Tabor 띠 안이다.**
- 논문: "tortuosity" 2.16 · 1.75 = 무작위 Li⁺ 경로 20 개 평균 길이 ÷ 25 µm (p.7–8 · S14).  σ_ion 시뮬 4.4 · 6.9 × 10⁻⁵ S cm⁻¹ (σ_LPSCl 입력 0.1 S m⁻¹).
- 우리 산술: 수송 tortuosity (tau2 = φ·σ₀/σ_eff) = **5.34 · 3.42** (시뮬) · 실측 기준 7.8 · 4.9 (σ₀ 1.0 가정) · tau2 ÷ τ_geo² = 1.14 · 1.12.
- 우리에게 뜻 (τ 명명 규약 · CLAUDE.md ★★ τ 블록): ① 그들 1.75–2.16 을 우리 "수송 tortuosity 5.0–7.2" 옆에 두면 다른 양을 비교하는 것 — **기하학적 tortuosity (τ_geo)** 로 표기한다 ② 실제 재구성 (목이 해상된 구조 · 계면 항 없음) 에서는 tau2 ≈ 1.1 × τ_geo² — 경로 길이가 대부분을 설명한다.  우리 ps45 Hertz 망은 저항 전력의 **73–75 %** 가 SE–SE 협착이고 협착 뺀 CF tau2 는 1.25–1.79 다 (`docs/data/ps45_r45_network_g2_20261007/README.md` 끝 절).  그들 시뮬 tau2 (3.4–5.3) 는 우리 Tabor (감도) 2.78–4.12 ~ Hertz 5.03–7.24 **띠 안** (0.2PTFE 3.42 = Tabor 쪽 · 0.0PTFE 5.34 = Hertz 쪽) — "강체 구 Hertz 목이 실물보다 좁다 (frame[1] 소성 흐름 없음)" 는 ps45 README 의 추정 (a) 과 **방향이 맞는 외부 정황** [추정 · φ_SE 0.235 ↔ 0.28–0.30 · 조성 · 압력 다름].
- 할 일: (a) 덱 · 표에서 그들 값은 "기하학적 tortuosity (무작위 경로)" 로 (b) ps45 README ② 의 **전류 가중 경로 길이**를 결과 전 등록 뒤 계산해 tau2 vs τ_geo² 평면에 우리 다섯 침대 + 그들 두 점을 같이 그리기 (c) "수송 tortuosity 5–7" 을 보일 때 이 논문의 실구조 tau2 3.4–5.3 을 자릿수 대조 괄호로 (같은 φ 가 아님을 각주로).

**8-4. 복셀 FV (= 우리 `CONTACT_FREE` 가지) 의 실측 격차 크기 — 약 1.4–1.5 배, 단 σ₀ 입력에 조건부.**
- 논문: 실제 재구성 위 ConductoDict σ_ion ÷ EIS = 1.46 · 1.42 (Fig. 4g · Table S2) · σ_e 는 0.99 · 0.97.  σ_LPSCl 입력 1.0 mS cm⁻¹ 의 출처 없음 · 순수 LPSCl 펠릿 측정 없음.
- 우리에게 뜻 (CL-81 · CL-91): 계면 저항 항이 없는 복셀 FV 가 실구조에서 EIS 를 **약 1.4–1.5 배 과대** (빠진 저항 몫 ≈30 %) 하는 첫 같은 계 (LPSCl + NCM) 실례 — Minnmann 2024 (FIB-SEM 100 nm · GeoDict flux τ, 실측 τ > 시뮬) 와 같은 방향 · Ketter 2025 (합성 2 µm 복셀 저항망, NCM ≥ 60 vol% 에서 10–58 배) 보다 훨씬 작다 = **구조가 실물이냐가 격차를 지배** [추정].  그러나 같은 구조에 우리 σ₀ 3.0 (솔버 상수) 을 넣으면 4.3–4.4 배 · 1.5 (보고 기준) 면 2.1–2.2 배 — **σ₀ 선택이 계면 물리보다 격차를 더 움직인다**.
- 할 일: (a) STEP3 σ_ion 절대값을 실험 옆에 둘 때 CL-81 한정어에 "실구조 FV ÷ EIS = 1.4–1.5 (σ₀ 1.0 · 이 논문)" 를 참고로 (b) 대칭셀 계획의 **순수 LPSCl 펠릿 기준 시료** (같은 성형 · 측정 조건) 는 필수 — 이 논문은 그것이 없어서 f · tau2 비교가 출처 없는 σ₀ 에 걸린다 (c) CL-91 의 "펠릿 잔류기공 ↔ STEP3 명시 기공 이중계상" 크기 논의에 이 논문은 직접 도움이 안 된다 (σ₀ 출처 없음).

**8-5. VGCF 실효 σ 83 S/cm 의 외부 선례 + "분산 상태만으로 σ_e 2 배" — Lee 2025 대조 R = 2.074 의 다른 후보.**
- 논문: VGCF 입력 **8300 S m⁻¹ = 83 S cm⁻¹** · NCM 0.9 S m⁻¹ (p.13) · VGCF 를 복셀로 해상 (공칭 지름 150 nm 를 쓰면 면 안 약 7 화소 [우리 산술 — 지름은 이 논문에 없음]) · 시뮬 σ_e = 실측 ±3 % · VGCF 분포가 고르게 되자 (하위부피 SD 7.0 → 4.5 · 꼬리 50 → 27 %) **거의 같은 VGCF 부피 (3.5 ↔ 3.3 %) 에서 σ_e 0.92 → 1.85 × 10⁻²** · NCM 만으로는 0.54–0.55 × 10⁻² 상한 → VGCF 경로 몫 ≥ 41 · 70 % [우리 산술].
- 우리에게 뜻: ① CL-47 읽기 (ii) "σ_VGCF 는 섬유–섬유 접촉을 품은 유효 망 상수 (10² S/cm 급)" 에 **실측과 맞은 독립 복셀 FV 선례**가 생겼다 (그들 83 의 출처는 미기재 — 데이터시트 분말값과 같은 수일 뿐 확인 안 됨) ② 그들 NCM 0.9 × 10⁻² S cm⁻¹ ≈ 우리 STEP3 σ_NCM 1.0 × 10⁻² (CL-92 각주) — **입력은 같은 자릿수**인데 우리 Lee 조성 STEP3 는 실측의 2.07 배 (R) 다 ③ 우리 R 의 해석은 "PTFE 코팅 물리 없음 + PTFE 부피 0.40–0.41 만 표현" 이었는데, 이 논문은 **VGCF 분산 상태 하나로 σ_e 가 2 배** 움직임을 보인다 → 우리 씨앗 VGCF 가 "0.2PTFE 처럼 고른" 상태라면 실물 (어느 정도 뭉친) 보다 높게 나오는 것이 자연스럽다 [추정].
- 할 일: Lee STEP2 침대 (VGCF 3 / PTFE 0.5) 에서 그들 지표 그대로 — VGCF 하위부피 vol% 평균 · 중앙 · SD · 꼬리 · NCM–VGCF 접촉 영역 분포 — 를 계산해 0.0 · 0.2PTFE 값과 나란히 (계산 = 결과 전 등록 뒤 · 판정 기준 미리 적기).

**8-6. PTFE 규약 (CL-60 centerline) — 무엇을 표현하고 무엇을 못 하나.**
- 논문: PTFE 섬유 지름 **20–50 nm** (p.3) · 재구성은 PTFE 를 분할하지 않음 (Table S1 "−") · PTFE 0 · 0.2 · 0.5 · 1.0 wt% 에서 σ_e 0.93 · 1.91 · 1.03 · 0.72 × 10⁻² · σ_ion 3.01 · 4.85 · 3.40 · 2.95 × 10⁻⁵ S cm⁻¹ · 상대밀도 84.6 · 87.4 · 86.8 · 82.5 % (Table S2).
- 우리에게 뜻: ① 20–50 nm 는 Lee 2025 EES (`lee2025_dual_fibrous_ptfe_dry_electrode`) 의 **fibre 계급 Ø 0.048 µm** 과 같은 크기 — 우리 PTFE_D 0.25 µm 는 rope 계급 (CL-66) · 계층 해석과 정합 ② PTFE 의 **≤ 0.2 wt% 지배 효과는 구조 (분산 · 치밀화 · SE 코팅)** 이고, 사후 절연 스탬프인 우리 규약은 이 쪽을 표현할 수 없다 ③ 0.5 → 1.0 wt% 의 σ_e 비 **0.70** (밀도 −4.3 %p 포함) 는 우리 모델 Q 0.840 (PTFE 1 / 0.5, centerline) 과 Lee 2025 Nat Commun 곡선 보간 0.44 **사이** → PTFE 손실의 세기는 공정 의존이고, Q 0.84 가 이 논문 기준으로는 크게 어긋나지 않는다 [추정 · VGCF 2 vs 3 wt% · NCM · 공정 다름] ④ `hong2026_sulfide_cathode_binder_digitaltwin` 은 PTFE 1 wt% 에서 σ_ion 이 분말보다 **낮았다** (0.064 vs 0.087 mS cm⁻¹) — "PTFE = 이득" 도 "PTFE = 손실" 도 일반화할 수 없다.
- 할 일: (a) 0.5 ↔ 1 wt% 비교에는 centerline 을 지금 한정어대로 유지 (b) **"PTFE 있음 vs 없음" 주장은 우리 모델로 하지 않는다** (c) PTFE 의 구조 효과를 다룰 날이 오면 그 자리는 혼합 · MPM 쪽 (코팅 형성 · 치밀화) 이지 복셀 스탬프가 아니다.

**8-7. 두꺼울수록 이점이 커진다 (단 단조 아님) — 미세구조 시뮬이 못 간 두께를 우리는 간다.**
- 논문: 25 · 35 · 45 mg cm⁻² (78 · 109 · 139 µm) 에서 100 회 유지율 격차 3.9 · 1.5 · **12.0 %p** · 45 mg cm⁻² 0.5 C 비용량 ≈168 vs ≈134 mAh g⁻¹ [판독 S27] · 미세구조 시뮬은 25 µm 만 (*"will be exacerbated as electrode loading increases"* p.11).
- 우리에게 뜻: 논지의 "건식 후막" 범위 · 우리 6 mAh ps45 침대 (≈111 µm) 와 같은 두께대다.  하향식 (FIB-SEM) 은 25 µm 정육면체에 묶이지만, 우리 DEM/MPM 은 **전체 두께 침대**를 만든다 — 두께 방향 전류 · 비활성 분율 · 리튬화 깊이 프로파일은 우리가 더할 수 있는 몫 (`positioning_vs_geodict.md` 의 상향식 이점이 구체화되는 자리) [추정].
- 할 일: P3 시험 · 대칭셀 해석 때 망 / STEP3 결과를 **두께 깊이별** (분리막 쪽 → 집전체 쪽) 로 보고 · 그들 Fig. S23 · S26 의 "집전체 쪽 몰림" 이 100 µm 급에서 어떻게 되는지를 우리 침대로 (STEP4 는 PyBaMM 패리티 전이라 정성).

**8-8. 대칭셀 계획 (`docs/symmetric_cell_ionic_plan_20261013.md`) 에 바로 쓸 측정 규약과 자릿수.**
- 논문: σ_ion = 전자 차단 Li/LPSCl/전극/LPSCl/Li (370 MPa) · EIS 14.1 mV · 5 MHz–10 mHz / σ_e = 이온 차단 Ti/전극/Ti · DC 50 mV (p.13) · 조성마다 상대밀도 (Table S2) · NCM 85 wt% 에서 σ_ion **0.030–0.049 mS cm⁻¹**.  측정 중 압력 · 시료 수 · 적합 모델 · 순수 LPSCl σ₀ [미확인].
- 우리에게 뜻: 계획 §4 의 "전자 차단 구성 (양쪽 LPSCl 층)" 과 같은 구성의 같은 연구실 계보 실례 · 계획 §2 모델 예측 (81.6 wt%, σ₀ 1.5 에서 0.059–0.089 mS cm⁻¹) 은 이 논문 85 wt% 값보다 높다 = CAM 이 적은 쪽이 높은 방향으로 자릿수 정합 [추정 · 조성 · 압력 · 첨가제 다름].
- 할 일: 계획대로 하되 이 논문이 **빠뜨린 것** — 순수 LPSCl 펠릿 σ₀ (같은 성형 · 측정) · 측정 중 적층압 · 반복 n ≥ 3 · 적합 회로 · 가압 중 / 놓은 뒤 두께 — 를 기록 항목으로 명시.  σ_e 는 이온 차단 DC 로 따로 재면 TLM 의 레일 구분 문제 (`malifarge2017_tortuosity_symmetric_cell_impedance_tlm` · `comparison_vs_ours_DEM.md` J 절) 를 피한다.

---

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "FIB-SEM reconstructions of PTFE-based dry-processed NCM–Li₆PS₅Cl cathodes (Lee et al., *Small* 2026) show that 0.2 wt% PTFE raises the LPSCl share of the NCM surface from 35 % to 59 % at an unchanged reconstructed LPSCl volume fraction (23.5 vs 23.6 vol%), and that finite-volume simulations on the same reconstructions raise the effective ionic conductivity by 57 % (measured: +61 %)."
- "In that work the reported 'tortuosity' (2.16 → 1.75) is a geometric path-length ratio from 20 randomly extracted Li⁺ paths; the corresponding transport tortuosity from their own simulated conductivity is 5.3 → 3.4 (our calculation, assuming their input σ_LPSCl = 1.0 mS cm⁻¹)."
- 국문: *"PTFE 0.2 wt% 건식 양극은 같은 LPSCl 부피에서 NCM 표면 LPSCl 몫이 35 → 59 % 로 늘고, 같은 재구성 위 계산 이온전도도가 57 % 오른다 (실측 61 %) — 부피가 아니라 배치가 바뀐 결과다 (Lee 등 2026, FIB-SEM 25 µm 정육면체 1 개씩)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **Fig. 1c = Fig. S7a 같은 사진** (회색조 상관 0.967 · 교차 대조 −0.03 [우리 산술]) — 라벨은 "NCM within 0.0PTFE" ↔ "pre-mixed powder".  Methods (p.13) 는 0.0PTFE 도 100 °C · 20 min 혼합을 거친다고 읽히는데, 그 상태의 0.0PTFE 사진은 따로 없다 → PTFE 효과와 혼합 시간 효과의 분리가 Methods 문장 하나에 걸린다.  (Fig. 1d = S7d 는 라벨 일치 · 0.958.)
2. **재구성 1 개씩 · 25 µm** (NCM D50 의 약 3.6 배) — RVE 수렴 · 재구성 반복 · 분할 오차 없음.  재구성 공극은 밀도 기반보다 2.5 %p (0.0) · 0.7 %p (0.2) 낮다 (Table S1) — 두 전극의 분할 편향이 다르다.
3. **정규화 미기재 둘**: VGCF 하위부피 평균 5.1 · 5.2 ≠ 전체 3.5 · 3.3 vol% · S13 막대 평균 ≈0.28 · 0.24 ≠ 재구성 LPSCl 0.235 · 0.236 [우리 산술 · 판독].
4. **칸 < 입자**: 2.5 µm 하위부피 < NCM 7 µm — 무작위 기준 없는 SD 비교 (§8-2).
5. **비활성 문턱이 절대값** (0.1 × 10³ A m⁻² 를 두 전극에 같게) — σ 가 큰 전극에서 상대 문턱이 낮아진다 (평균의 0.13 → 0.09 배 이하) · Fig. 4f 칸 이름에 1–2 칸 없음 · 막대 합 ≈97 %.
6. **실측 +61 % 의 밀도 몫**: 상대밀도 84.6 → 87.4 % · bulk LPSCl 21.8 → 22.5 vol% — 문턱 근처라면 밀도만으로 ×1.14 (우리 생산 폼 지수 ½) ~ ×1.70 (지수 2) [우리 산술 · 추정].  시뮬 +57 % 는 재구성 부피가 같아 배치 효과를 떼지만, 실측과 시뮬의 일치 (57 ↔ 61 %) 를 "배치가 전부" 로 읽지 않는다.
7. **σ 입력 출처 없음**: NCM 0.9 · VGCF 8300 · LPSCl 0.1 S m⁻¹ (p.13) · 순수 LPSCl σ₀ 측정 없음 → σ_ion 절대 일치 판단 불가 (저자도 경향만 주장).
8. **"Voxel size: 20 nm" (Fig. 2a) ↔ 20.83 × 20.83 × 50 nm** (p.13) — 슬라이스 방향 해상도가 2.4 배 거칠다 · VGCF 지름은 이 논문에 없다 — 제품 공칭 ≈150 nm (CL-47 · `kim2025_conductive_agent_se_coating_cathode`) 를 쓰면 슬라이스 3 장 · 면 안 7 화소 정도 [우리 산술].
9. **PTFE 상 없음**: 0.2 wt% (0.3 vol%) 는 무시 가능할 수 있으나 PTFE 복셀이 어느 상으로 갔는지 [미확인] — VGCF 로 갔다면 σ_e 를 부풀릴 수 있다 [추정].
10. **측정 조건 결손**: 전도도 측정 압력 · 시료 수 · 등가회로 · 전극 두께 · Fig. 5 셀 로딩 [미확인] · 오차 막대 없음.
11. **같은 연구실 계보 사이 긴장**: `hong2026_sulfide_cathode_binder_digitaltwin` (PTFE 1 wt% · 합성 GrainGeo 트윈 · σ_ion 으로 보정) 은 PTFE 가 LPSCl 피복을 거의 안 바꾸고 (35 → 36 %) σ_ion 을 낮춘다 (0.087 → 0.064 mS cm⁻¹) — 이 논문 (측정 트윈 · 0.2 wt%) 과 반대 방향.  조성 · 함량 · 혼합 (막자 30 min · 롤프레스 vs 100 °C 손 혼합) · 트윈 방식이 다르다 — 어느 쪽도 "PTFE 일반" 이 아니다.
12. **C-rate 기준이 셀마다 다름** (자기 0.1 C 용량) — 같은 C-rate 의 0.0PTFE 전류가 약 9 % 낮다 (§3-11).  OEP ΔP 는 용량당 정규화 없음 (0.2PTFE 가 용량이 더 크다).
13. **원문 오식 · 불일치**: "LiNbO₂" (p.2 · p.13 — LiNbO₃ 오식 가능성) · Table S1 "0.02TFE" · Fig. S4 캡션 패널 표지 · Fig. S21 캡션 "(b)/(d) 0.0PTFE" · Fig. S14 y 축 "%" (값은 분율) · Fig. 1a "Flim" · p.2 혼합 서술 (온도 없음) ↔ p.13 (100 °C) · 본문 코팅 "100–500 nm" ↔ S3 주석 최소 67 nm (44 개 중 3 개 < 100 nm).
14. **전이 한계**: NCM711 (Ni 0.7) 단봉 D50 7 µm ≠ 우리 NCM (PC + SC) · VGCF 2 wt% · PTFE 포함 ≠ ps45 (탄소 · 바인더 없음) · 370 MPa ≠ 300 MPa · 같은 SE (Li₆PS₅Cl, D50 1 µm) 는 같다.
15. **25 µm 미세구조 전기화학 시뮬**: 입력 미기재 · 실험 검증 없음 — 정성 그림으로만.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 12 | A. Bielefeld, D. A. Weber, J. Janek, *J. Phys. Chem. C* 123 (2019) 1626–1634 | 정본 카드 `bielefeld2019_microstructural_modeling_composite_cathode` |
| 13 | J. Park, K. T. Kim, D. Y. Oh, et al., *Adv. Energy Mater.* 10 (2020) 2001563 | 정본 카드 `park2020_digitaltwin_assb_foundational` — 계보 시조 · 같은 NCM711 |
| 14 | J. Lee, S. Byun, H. Lee, et al., *Battery Energy* 2 (2023) 20220061 | 정본 카드 `lee2023_sicspe_digitaltwin_assb` — 같은 1저자 |
| 15 | P. Minnmann, F. Strauss, A. Bielefeld, et al., *Adv. Energy Mater.* 12 (2022) 2201425 | 정본 카드 `minnmann2022_designing_cathodes_solidstate` |
| 16 | T. Shi, Q. Tu, Y. Tian, et al., *Adv. Energy Mater.* 10 (2020) 1902881 | 정본 카드 `shi2019_high_am_loading_particle_size_assb` |
| 17 | D. Hlushkou, A. E. Reising, N. Kaiser, et al., *J. Power Sources* 396 (2018) 363–370 | 정본 카드 `hlushkou2018_void_space_ion_transport_assb_cathode` |
| 33 | F. Hippauf, B. Schumm, S. Doerfler, et al., *Energy Storage Mater.* 21 (2019) 390–398 | 카드 없음 — PTFE 0.1–1 wt% 건식 6.5 mAh cm⁻² · "PTFE 가 무바인더보다 균일" 선행 (p.2) |
| 36 | J. Mun, T. Song, M.-S. Park, J. H. Kim, *Adv. Mater.* 37 (2025) 2506123 | 정본 카드 `mun2025_dry_electrode_technology_assb_review` |
| 37 | D. Lee, Y. Shim, Y. Kim, et al., *Nat. Commun.* 15 (2024) 4763 | 카드 없음 — 건식 전단이 CAM–SE 피복을 늘린다 (p.2 · Table S3 [9]) · ★ 다음 디제스트 후보 |
| 38 | J. Park, K. T. Bae, D. Kim, et al., *Nano Energy* 79 (2021) 105456 | 카드 없음 — 산화물 SE 트윈 (같은 연구실) |
| 39 | J. Y. Kim, J. Choi, J. Choi, et al., *Carbon Energy* 7 (2025) 70046 | 카드 없음 — Si 분산 트윈 (같은 연구실) |
| 40 | J. Lim, J. Choi, K.-G. Kim, et al., *Small* 22 (2025) 07883 | 카드 없음 — Si 열화 트윈 (같은 연구실) |
| 41 | S. Kim, H. Lee, J. Lim, J. Park, Y. M. Lee, *ACS Energy Lett.* 9 (2024) 5225–5239 | 정본 카드 `kim2024_digital_twin_acsenergyletters` |
| 42 · 45 | J. Kim et al., *Adv. Funct. Mater.* 33 (2023) 2211355 · J. T. Kim, H.-J. Shin, et al., *J. Mater. Chem. A* 11 (2023) 20549 | 카드 없음 — SE 코팅 CAM (KIST 계보) |
| 44 | H. Nakamura, T. Kawaguchi, T. Masuyama, et al., *J. Power Sources* 448 (2020) 227579 | 카드 없음 — 건식 SE 코팅 |
| 50 | J. Lim, J. Song, K.-G. Kim, et al., *Small* 21 (2025) 2410485 | 정본 카드 `lim2025_virtual_calendering_framework` |
| 51 · 52 | S. Müller et al., *Nat. Commun.* 12 (2021) 6205 · B. Kellers et al., *Batteries* 9 (2023) 390 | 카드 없음 — 딥러닝 분할 · 국소 REV (하위부피 방법의 근거) |
| 61 | D. Lee, Y. Shim, E. Choi, et al., *Joule* 9 (2025) 102046 | 카드 없음 — 국소 접촉 → 박리 전기화학-역학 모델 |
| 63 | H.-J. Shin, J. T. Kim, A. Y. Kim, et al., *Adv. Energy Mater.* 13 (2023) 2301220 | 카드 없음 — 저압 열화 (공동 1저자 H.-J. Shin) |
| SI [4] | S.-B. Hong, Y.-J. Lee, …, Y. M. Lee, …, D.-W. Kim, *ACS Energy Lett.* 7 (2022) 1092–1100 | 카드 없음 — 건식 양극 이오노머 바인더 (Table S3) |
| SI [7] | H.-J. Shin, …, H.-G. Jung, *Adv. Energy Mater.* 15 (2025) 2403247 | 카드 없음 — 그래핀 유사 탄소 코팅 SE (Table S3) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 16 쪽 · SI 20 쪽 텍스트 층 전수 (pdftotext raw · layout · 쪽별) · 저자 · 소속 · 위첨자 = p.1 렌더로 대조 · 방법 (고유 전도도 · σ_eff 식 · LiNbO₂ 아래첨자) = p.2 · p.13 렌더로 대조.
- 그림 · 표 36 장 = 캡션 36 개 (본문 Figure 1–6 · SI Figure S1–S27 · Table S1–S3; 본문 표 없음) · **36 장 전부 손 재크롭** (자동 bbox: 본문 = 여백 과다 · SI = 머리 로고 포함 + 래스터 아래 ≈12 pt 잘림 · Table S1/S2 한 장에 섞임) → 래스터 경계 그대로 · 원본 해상도 (본문 300 · SI 220 dpi) · 표 300 dpi · `figures.json` 의 `auto_bbox` · `recrop` · `note`.
- 400 dpi 재렌더로 다시 읽은 것: Fig. 3f · 4f · S13 · S14b · S27 (S27 의 1 C 값은 첫 판독이 오른쪽 축과 섞였다가 바로잡힘).
- Fig. 1c ↔ S7a · Fig. 1d ↔ S7d 상관 = 회색조 · 240 × 180 축소 상관계수 (scratch 계산 · 저장 안 함).
- Table S2 값 = 텍스트 층 + `tab_S2.png` 칸마다 대조 · S17 범례 값과도 같다.
- 정본 litdb 중복 확인: DOI `10.1002/smll.75974` · 제목 낱말 · 1저자 이름으로 `litdb/papers/*.md` 전수 grep — 없음 (같은 연구실 다른 논문만).

## 🔗 관련 카드
- 같은 연구실 계보: `park2020_digitaltwin_assb_foundational` · `lee2023_sicspe_digitaltwin_assb` · `kim2024_digital_twin_acsenergyletters` · `choi2024_digital_twin_review_echem` · `lim2025_virtual_calendering_framework` · `kim2025_conductive_agent_se_coating_cathode` · `hong2026_sulfide_cathode_binder_digitaltwin` · `hong2026_cbd_viscoelasticity_springback` (R. Hong 1저자) · `nam2026_primer_layer_dry_electrode_collector` (R. Hong 공저) · `koo2025_cnt_wrapped_sc_nca_dry_cathode` · `oh2026_bimodal_composite_cathode` (Hun-Gi Jung 교신) · 연구실 트리아지 `../yonsei_dtbl_lab_triage_2026.md` · 위치 `../positioning_vs_geodict.md`.
- PTFE 건식 전극: `lee2025_corolling_dryprocess_lpscl_ptfe` (Lee 2025 Nat Commun — 우리 σ_e 절대 대조 A 의 34 mS/cm) · `lee2025_dual_fibrous_ptfe_dry_electrode` (fibre 0.048 · rope 0.248 µm, CL-66) · `matthews2024_ptfe_nanofibril_network` · `kang2025_bollard_anchored_binder_dry_electrode` · `mun2025_dry_electrode_technology_assb_review` · `liu2025_dry_processing_high_energy_li_batteries_review`.
- 3D 미세구조 · 복셀 수송: `minnmann2024_microstructure_porosity_visualization` (FIB-SEM 100 nm · GeoDict flux τ) · `ketter2025_resistor_network_models_predict_transport_properties` (합성 복셀 저항망) · `bielefeld2019_microstructural_modeling_composite_cathode` · `park2020_dimension_controlled_se_percolation_contact_area` · `bazzoun2026_dem_fem_rnm_ionic`.
- SE 분산 · 응집: `otani2025_dem_se_dispersion_aggregation_compression` (응집 상태를 심고 누르는 DEM).
- 측정 규약 · 기준 상태: `miss2026_insitu_conductivity_porosity_pressure_compaction` · `minnmann2021_jes_charge_transport_bottlenecks`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
