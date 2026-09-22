# ⭐ 우리-랩 (Jong-Won Lee 그룹) — Model-informed design of microcrack-tolerant cathodes for fast-charging lithium-ion batteries — 3D 전기화학-역학 시뮬레이션이 지목한 "분리막 쪽 큰 다결정(LPC, ~12 µm) 입자의 균열" 을 소형 단결정(SSC, ~3 µm) 10 µm 상층 bilayer 로 막다 — W. Lee, S. Kim, S.Y. Yang, D.K. Kim, M.-S. Park\*, J.-W. Lee\* (Energy Storage Materials 2026)

> slug `lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging` · DOI `10.1016/j.ensm.2026.104985` · type `exp (LIB 액체계 CR2032 풀셀·반쪽셀 + FIB-SEM·nanoindentation·XRD·XPS·EIS equivalent-circuit) + 3D electrochemo-mechanical continuum simulation (입자-해상 3D 풀셀 기하, BV + Fick + Newman 전해질 + 선형탄성 von Mises; 솔버 미기재)` · PDF `6. Model-informed design of microcrack-tolerant cathodes for fast-charging lithium-ion batteries.pdf` (+ `6. Sup) ….docx` = SI: Note 1–2 · Table S1–S4 · Fig S1–S23) · digested `2026-09-22` · status ✅ (**본문 11 pp + SI 둘 다 수신·전수 정독**) · 태그 **[우리-랩 · ⚠ 액체계 LIB(1 M LiPF₆ EC/DMC) — 황화물 ASSB 아님 · 값 전이 금지, 방향·방법·설계논리만]**
>
> 저자 = **Woojae Lee, Siwon Kim, Soo Young Yang** (a: Division of Materials Science and Engineering, **Hanyang University**), **Dong Ki Kim, Min-Sik Park\*** (b: Kyung Hee University), **Jong-Won Lee\*** (a + c: Department of Battery Engineering, Hanyang University). Energy Storage Materials **86 (2026) 104985**; 접수 2025-11-23 / 수정 2026-02-02 / 수락 2026-02-11 / 온라인 2026-02-12. 지원 **Samsung SDI** + NST (GTL24012-000).
> ★ **Siwon Kim** = `kim2025_impedance_decoupling_tlm_assb`(우리 랩 EIS-TLM 분해) 의 1저자 — 이 카드는 그 자매편의 **LIB 급속충전·역학** 판이다. 자매 카드: `kang2025_toughened_bimodal_nca_lzo`(ASSB bimodal 균열, FEM Voronoi+CZM), `kim2025_impedance_decoupling_tlm_assb`(ASSB 임피던스 분해).
> 그림: `litdb/figures/lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging/` (본문 Fig 1–6 + SI Fig S1–S23 = 29 장; Table S1–S4 는 §SI 에 전사).
>
> elements: Co Li Mn Ni O

## 1. 한 줄 요약
NCM92 bimodal 양극(LPC 12 µm 다결정 : SSC 3 µm 단결정 = 6:4, 16.6 mg/cm², 3.45 g/cm³, 3.48 mAh/cm²) 의 **3C 급속충전 열화 = 분리막 쪽 LPC 의 입계 미세균열** 임을 **입자-해상 3D 전기화학-역학 모델**(3C 에서 LPC 표면 von Mises ~300 MPa vs 0.33C ~60 MPa; Δc = c_center − c_surface 가 분리막 쪽 1.5 vs 집전체 쪽 0.2 mmol cm⁻³) 로 지목하고 실험(균열 면적분율 분리막 쪽 3.4 % vs 집전체 쪽 1.2 %) 으로 확인 → **분리막 쪽 10 µm 를 SSC 만으로 덮는 bilayer(BLE-10)** 로 LPC 표면응력을 <150 MPa 로 낮춰 **3C 300 사이클 유지율 62.4 → 76.2 %**, 균열 면적분율 ~1 %. 우리에게는 (i) **z-방향 반응 불균일 → 입자별 응력 → 균열** 의 정량 체인, (ii) **층상(layered) 양극 설계 = 우리 5-phase Phase 5·A7 graded-z 의 실물 선례**, (iii) A10 사이클 chemo-mech 에 없는 **입자 내부 응력장** 축을 준다. ⚠ 액체계라 값은 못 옮긴다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| W. Lee, S. Kim, S.Y. Yang, D.K. Kim, M.-S. Park\*, J.-W. Lee\* (한양대 + 경희대) | Energy Storage Mater. 86 (2026) 104985 | 10.1016/j.ensm.2026.104985 | **Li[Ni₀.₉₂Co₀.₀₄Mn₀.₀₄]O₂ (NCM92)** LPC(~12 µm 다결정) + SSC(~3 µm 단결정) + SPC(소형 다결정, 대조) ; Super-P 3 / PVdF 3 wt% ; 음극 graphite/Si–C ; **1 M LiPF₆ EC:DMC 3:7 + 2.5 wt% FEC** | exp 주도 + 3D 전기화학-역학 시뮬 (설계 스윕 BLE-5/8/10/12/15/20) |

## 3. 핵심 수치
| 항목 | 값 | 조건 | stated / digitized / derived | 비고 |
|---|---|---|---|---|
| 전극 (SLE = 단층) | NCM92 94 wt% (LPC:SSC **6:4**) / Super-P 3 / PVdF 3; 로딩 **16.6 mg cm⁻²**, 밀도 **3.45 g cm⁻³**, **3.48 mAh cm⁻²** | | stated | 두께 = 16.6e-3/3.45 = **48 µm** (derived) ↔ 모델 50 µm ✓ |
| 음극 | graphite/Si–C 9.65 mg cm⁻², 1.58 g cm⁻³, 3.65 mAh cm⁻², N/P 1.05 | | stated | 두께 61 µm (derived) = Table S1 61 µm ✓ |
| LPC:SSC 비 스크리닝 (Fig S1) | 밀도 5:5 3.40 / **6:4 3.45** / 7:3 3.25 / 8:2 3.10 g cm⁻³ ; 용량 3.39 / **3.48** / 3.29 / 3.24 mAh cm⁻² | 단층 | digitized (6:4 는 stated) | 6:4 = 밀도·에너지 최대 → 기준 조성 |
| 단독 LPC vs SSC (Fig S2, 반쪽셀) | 0.2C 2.01 vs 1.96; **5C 1.76 vs 1.65** mAh cm⁻²; 3C 100 cyc 1.70→1.47 vs 1.64→1.46 | | digitized | SSC 가 고율에서 열세(고체확산 느림) — 본문 서술 일치 |
| 셀 프로토콜 | CR2032; 화성 0.04C ×2 (1C = 3.5 mAh cm⁻²), 2.8–4.25 V; 사이클 충전 0.33C 또는 **3C** / 방전 1C; 율 시험 충전 0.2/0.5/1/2/5C(3 cyc 씩)·방전 0.2C; RPT 0.1C 매 25 cyc; EIS 5 mV, 7 MHz–10 mHz | | stated | |
| 모델 셀 (Table S1) | 20×20 µm 단면; 음극 61 / 양극 **50** / 분리막 15 µm; 기공률 양극 **0.30**, 음극 0.40, 분리막 0.40; 음극 고체분율 0.59 | | stated | |
| 모델 파라미터 (Table S2) | c_max NCM92 50,060 mol m⁻³ [S4]; graphite 31,507 [S5]; Si–C 278,000 (Assumed); **i₀ SSC 2 (Assumed) / LPC 20 [S6]** / graphite 1 [S6] / Si–C 0.1 (Assumed) mA cm⁻²; 전해질 σ 10 mS cm⁻¹ [S7], t⁺ 0.35 [S6], c₀ 1000 mol m⁻³ (Assumed), D_e 2.5×10⁻⁶ m² s⁻¹ [S6]; **D_s SSC 1×10⁻¹⁴ (Assumed) / LPC 5×10⁻¹³ [S4]** / graphite 1.45×10⁻¹³ [S8] / Si–C 1×10⁻¹² [S9] m² s⁻¹; C-rate 0.33, 3; **E(NCM92) 191 GPa, ν 0.25** [S10 Cheng 2017 = NMC333 값] | | stated | ⚠ SSC 의 i₀·D_s 는 **가정값**(LPC 대비 1/10 · 1/50) — 측정 아님 |
| 3C 말 CC 단계 (SLE) | Li 농도 10.1–20.4 mmol cm⁻³ (색축), 분리막 쪽 우선 탈리튬; von Mises **0.33C ≤ ~60 MPa** vs **3C ~300 MPa** (LPC, 분리막 쪽) | Fig 1b,c | stated | 300 MPa 는 색축 상한 |
| Δc = c_center − c_surface (3C) | ① **1.5** ② 0.6 (분리막 쪽) / ③ 0.7 ④ 0.3 (중간) / ⑤ 0.4 ⑥ 0.2 (집전체 쪽) mmol cm⁻³ | Fig 1e | stated(그림 값) | 홀수 = LPC, 짝수 = SSC 로 읽힘(본문: "LPC particle near the separator (1)") |
| 반경 방향 von Mises (LPC) | 분리막 쪽 표면 ≈ **285** vs 집전체 쪽 ≈ 60 MPa; 중심 ≈ 0–10 | Fig 1f | digitized | 표면 집중 (Δc 구동) |
| SLE 풀셀 사이클 | 0.33C: 손실 미미 (3.15→2.77 mAh cm⁻², digitized); **3C 300 cyc 유지율 62.4 %** (2.85→1.85, digitized) | Fig 1g–i | stated + digitized | |
| 미세균열 면적분율 (SLE, 300 cyc 3C) | 분리막 쪽 **3.438 %** vs 집전체 쪽 **1.174 %** (~3×) | Fig S8; 본문 "~3.4 vs ~1.2" | stated | 그레이스케일 이진화 |
| Nanoindentation (Fig S9, "cathodes") | E_IT LPC **5.17** vs SSC **6.02 GPa**; H_IT **0.086** vs **0.18 GPa** | 5 mN | stated(그림 값) | ⚠ 전극/입자 유효값 — 모델 E 191 GPa 와 **다른 양** (§10) |
| BLE 스윕 (모델) | SSC 층 5/10/15/20 µm (+8, 12); CC 충전분율 SLE ≈77 · BLE-5 ≈77 · BLE-10 ≈77 · BLE-15 ≈75 · BLE-20 ≈74 % | Fig 2b,c | digitized | 15 µm 이상에서 CC 분율↓ (전해질 Li⁺ 수송 병목) |
| LPC(분리막 쪽) 표면 응력 | SLE ~300 · BLE-5 ~270 · **BLE-10/15/20 < 150 MPa** (stated); 반경 프로파일 표면값 BLE-5 ≈270 / BLE-10 ≈145 / BLE-15 ≈130 / BLE-20 ≈95 MPa | Fig 2f, S11 | stated + digitized | 최적 = **BLE-10** (응력 완화 ∧ 수송 무손실) |
| 전해질 Li⁺ 농도 (3C 말) | 1.14–2.73 mmol cm⁻³ (색축); BLE-15/20 은 급한 구배 | Fig 2e | stated(색축) | **액체 전해질 농도분극** — SSB 에는 없는 항 |
| BLE-10 실물 | SSC 상층 ~10 µm, 층간 혼합 없음(Fig S13), pOCV 동일(Fig 3d) | | stated | 캐스팅: 하층 300 mm min⁻¹·60 °C 6 h → 상층 1000 mm min⁻¹ → 캘린더링 |
| EIS 등가회로 (pristine, Table S3) | SLE R1 2.58 / R2 1.52 / R3 **4.14** ; BLE-10 3.16 / 1.54 / **3.99** Ω cm² | R1-(R2∥CPE1)-(R3∥CPE2)-W | stated | R3(전하전달) BLE-10 < SLE |
| EIS (300 cyc 3C, Table S4) | SLE 1.75 / 2.58 / **8.79 / 12.79** ; BLE-10 2.45 / 1.97 / **7.94 / 5.81** Ω cm² | R1-…-(R4∥CPE3)-W | stated | R3+R4: SLE 21.6 (×5.2 vs pristine R3) vs BLE-10 13.8 (×3.4) (derived) |
| 풀셀 유지율 | **3C 300 cyc: BLE-10 76.2 % vs SLE 62.4 %** (BLE-10 2.93→2.23, digitized); 4C 100 cyc ≈82 vs ≈62 %; 6C 50 cyc ≈80 vs ≈66 % | Fig 4c, S15 | stated / digitized | |
| 열화 모드 (300 cyc 3C, Dubarry dV/dQ) | **LAMc 22.8 → 16.1 %**, **LLI 30.4 → 25.8 %**, LAMa 12.7 / 13.7 % (~13) | Fig 4f | stated | |
| 율 특성 (풀셀) | 사이클 전 5C/0.2C: 82.3 (SLE) / 83.6 % (BLE-10); 300 cyc 후 0.2C: 80.3 / **89.8 %**, 5C: 53.5 / **70.6 %** (원용량 대비) | Fig 4h,i | stated | |
| 온도 | BLE-10: 45 °C·3C 100 cyc **83.9 %** (3.19→2.67, digitized); −10 °C·1C 100 cyc **86.7 %** (2.58→2.25) | Fig S17 | stated + digitized | |
| 대조군 | 단층 LPC:SSC 5:5 (BLE 의 SSC 함량 ~52 wt% 와 등가): 개선 없음; 2:8: 악화 (3C 100 cyc 2.80→2.10) ; **SPC 상층 bilayer: 개선 없음 + SPC 균열** (3.0→2.15 vs BLE-10 2.95→2.57) | Fig S18–S20 | stated + digitized | ⇒ 효과의 원천 = **공간 배치 + 단결정성**, 조성 아님 |
| 사후 분석 | BLE-10 LPC 균열 면적분율 **1.186 / 0.912 %** (Fig S21); XRD (003)↓각·(104)↑각 이동이 BLE-10 에서 작음; XPS Ni²⁺ **52.5 % (SLE) vs 43.9 % (BLE-10 하층)**, 상층 SSC Ni²⁺ 47.5 % (Fig S23) | Fig 5, S21–S23 | stated | 균열↓ → 전해질 침투·부반응↓ → 양이온 혼합↓ |

## 4. 시뮬레이션 방법 ★
- **기하**: 실험과 같은 **실 입자 형상·전극 미세구조**로 3D bimodal 양극(LPC ~12 µm 구형 다결정 + SSC ~3 µm 다면체 단결정) 을 구성, 20×20 µm 단면 × 양극 50 µm; 음극(graphite/Si–C) 은 **균일 분산 구형 단순화** [44]; 분리막 15 µm; 풀셀 도메인 (Fig 1a). 입자 생성 알고리즘·메시·솔버 **미기재** (COMSOL 등 명시 없음).
- **CBD + 기공 = 하나의 전해질-충전 다공상**(이온·전자 동시 전도) [42,43] — CBD 를 따로 해상하지 않는다.
- **전기화학** (SI Note 2): BV (eq 2–3, α_a/α_c), 고체 Fick (eq 4–6), 전해질 이온전류 보존(σ_e, t⁺, 활동도) (eq 7), 전해질 Li⁺ 질량보존 (eq 8, 기공률·D_e), 고체상 전하보존 (eq 9). LPC / SSC 에 **서로 다른 i₀·D_s** (표 S2).
- **역학** (SI Note 2): 준정적 평형 `∇·σ = 0`, 체력 0 (eq 10); 총변형 = 탄성 + **탈리튬 화학변형** (eq 11, [S3] Yuan/Lu/Xu 2023 = **ASSB 복합양극 chemo-mech 논문**의 정식화 차용); 등방 선형탄성 Hooke (eq 12–13); 화학변형 등방·국소 Li 농도 비례 (eq 14–15, Ω = 완전 탈리튬 시 상대 부피변화 — **값 미기재**). **모든 입자 선형탄성·소변형; 소성·크리프·파괴 없음** (본문 2.4 명시). von Mises 는 응력장 요약 지표.
- **프로토콜**: CC–CV 충전 0.33C / 3C (Fig S3: 3C 는 ~14.7 min 에 4.25 V 도달 후 CV). 필드는 **CC 단계 말** 스냅샷.
- **설계 스윕**: BLE-5/10/15/20 (+8/12, Fig S10·S12); **이상적 층간 계면**(완전 접촉·균일 두께) 가정 — 본문이 한계로 명시.
- **입자 처리 ★**: 입자-해상 3D 연속체(각 입자가 메시 도메인). 형상 변화 없음(소변형), 접촉 역학 없음(입자 간 힘 전달은 연속체 결합으로 암묵), 균열 없음. ⇒ 우리 층위 지도에서 **"입자 내부 응력장" 은 있고 "접촉/형상/파괴" 는 없음** — 우리 DEM(접촉망)·MPM(형상소성)·A10(접촉 CZM) 과 **정확히 상보적**.

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | (a) 3D 풀셀 모델 (b) 0.33C vs 3C 말 Li 농도장 (c) von Mises 장 (d,e) Δc 정의·6 입자 값 (f) LPC 반경 응력 프로파일(분리막 쪽 vs 집전체 쪽) (g,h) 0.33C/3C 전압곡선 1/100/200/300 cyc (i) 사이클 (j,k) 300 cyc 후 SEM: 분리막 쪽 LPC 입계균열 I, 집전체 쪽 경미 II, SSC 무균열 III | ★ **z-반응 불균일 → 입자별 Δc → 응력 → 균열 위치** 의 한 장 요약. 우리 STEP4 hot-spot 맵 + A10 이 합쳐져야 나오는 그림 |
| 2 | (a) BLE 개념 (b) 3C 전압 (c) CC/CV 분율 (d) Li 농도 (e) 전해질 Li⁺ 농도 (f) von Mises — BLE-5/10/15/20 | 설계 스윕 = 우리 Phase 5 "층상 양극" 의 설계변수(상층 두께) 스윕 선례; (e) 는 액체 전용 |
| 3 | (a) 층별 캐스팅 공정 (b) BLE-10 단면 (c) 상면 SSC (d) pOCV 동일 (e) Nyquist + 회로 (f) 반쪽셀 율 | 제조 실현성 + "상층이 접촉저항을 안 만든다" (R1 동급) |
| 4 | BLE-10 (a,b) 전압곡선 (c) 사이클 (d,e) dQ/dV 1–300 cyc (H2–H3 4번째 피크 유지) (f) LAMc/LAMa/LLI (g) 300 cyc Nyquist R1–R4 (h,i) 사이클 전후 율 | **열화모드 분해(Dubarry)** + **R_ct(N) 실측** = A10/A11 `rint_cycle_traj` 의 LIB 판 앵커(형태만) |
| 5 | (a) BLE-10 300 cyc 후 SEM (b–d) XRD (003)/(104) 이동 (e–h) XPS C/O/F/Ni | 균열 억제 → 계면 부반응 억제의 화학 증거 |
| 6 | 기전 모식: SLE = 집중 반응 → 불균일 탈리튬 → 균열; BLE = SSC 층이 균일 탈리튬 + 기계 완충 | 발표용 논리도 |

## 6. Post-processing ★
- **필드 → 지표**: Δc = c_center − c_surface (입자별), 반경 방향 von Mises 프로파일, CC/CV 용량 분율.
- **실험**: 그레이스케일 FIB-SEM 단면 이진화 → **미세균열 면적분율** (분리막 쪽 vs 집전체 쪽; Fig S8·S21); nanoindentation E_IT/H_IT; **dQ/dV(ICA) + pOCV 스케일링·시프트(Dubarry [S1], SI Note 1: 전극 SOC = α·SOC_cell + β) → LAMc/LAMa/LLI**; EIS 등가회로 R1-(R2∥CPE1)-(R3∥CPE2)-W (pristine) / +R4∥CPE3 (cycled); XRD 피크 이동; XPS Ni²⁺/Ni³⁺ 분율.
- **도구**: 시뮬 솔버 미기재; Biologic SP-300(EIS); Anton Paar NHT3; Bruker D8; Thermo K-Alpha.
- **우리 검산 (derived)**: 로딩/밀도 → 두께 48 µm(양극)·61 µm(음극) = 모델 두께 ✓ — 모델 기하가 실험 전극과 정합. 3C 15 min CC 종료 시 CC 분율 ≈77 % = 3C×(14.7/60 h) ≈ 0.735 → 0.735/0.95(3.48 대비 3.3 도달) 급 — 그림값과 정합.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 전해질 | 액체 (σ 10 mS cm⁻¹, t⁺ 0.35, 농도분극 있음 — Fig 2e) | 황화물 SE = 단일이온 도체 (t⁺≈1): 농도분극 **없음**, 대신 SE 망 옴 강하 (STEP4 2C: 이온 84–90 mV vs 전자 0.01–0.03 mV) | 분리막 쪽 우선 탈리튬의 **원인 항이 다르다** (액체: c_e 구배 + 이온 옴; SSB: SE 망 옴/협착). 방향 같음, 크기 전이 금지 |
| 입자별 kinetics 분리 | i₀ LPC 20 / SSC 2 mA cm⁻² (SSC 가정), D_s LPC 5×10⁻¹³ [S4] / SSC 1×10⁻¹⁴ (가정) | STEP4 `--d-s-poly/--d-s-sc/--i0-poly/--i0-sc` (반경 문턱 3.5 µm) 보유; 앵커 `docs/ncm_sc_poly_electrochem_anchors.md`: 액체 PC 1e-14–1e-13 · SC 1e-15–1e-14; **ASSB 에선 역전**(poly 4e-15 Chen2020 … 3e-14 Kang&Shin) | 그들 LPC 5e-13 은 액체 PC 밴드 상단(18650 모델값), SSC 1e-14 는 가정. **ASSB 로 이식 금지** (Ruess/Jung: SE 는 균열 침투 불가). i₀ 10× 대비도 가정 |
| AM 탄성 | E 191 GPa · ν 0.25 (NMC333 문헌값) | DEM NMC811 E 140 (강체 골격) / NCA 175 (A8, "assumed"+Koerver) | 세 번째 출처. 140 vs 175 vs 191 = 출처-방법 산포; 우리 결론엔 무영향(AM 강체) |
| 역학 층위 | 입자 내부 **연속 응력장**(Δc 구동), 소성·파괴·접촉 없음, 층간 계면 이상 | A10 `cycle_contact_ledger.py`: 강체구 반경진동 + Bucci CZM(G_c 2.8±1.8 J m⁻², ΔV≈3 % 개시, Γ<1000) = **접촉 박리**만, 입자 내부 응력 없음; DEM Auerbach 파괴는 **압밀** 시점 | **정확히 상보**: 그들 = 입자 안, 우리 = 입자 사이. 둘을 합쳐야 "균열 위치 + 접촉 손실" 이 닫힌다 (§G 입자 내부 축) |
| 균열 z-분포 | 분리막 쪽 3.4 % vs 집전체 쪽 1.2 % (실측) | A10 f_broken(N) 은 전체 합만 출력 — **z-프로파일 없음** | 흡수 대상: f_broken(z) 출력 (§F) |
| bimodal 배치 | 상층 SSC-only 10 µm + 하층 6:4 | DEM/MPM bimodal 은 **균질 혼합**(P:S, AM%) 만; A7 graded-z 는 기공률 구배; Phase 5 층상 양극은 계획 | 그들 실증: **같은 SSC 함량(5:5) 단층은 무효, 배치가 효과** ⇒ 조성 스윕만으로는 못 보는 자유도 |
| 균열 억제 기전 | 단결정성(SPC 상층은 실패) + 작은 크기 + 완충 | `jung2023_single_crystal_ncm_morphology`·`trevisanello2021`: ASSB 에서 SC 유리; `kang2025`: 큰 입자 균열, Li 농도·응력 구배 ~10× | 방향 일치 (SC·소립 유리). ASSB 에서는 SE 가 균열에 못 들어가 **결과의 크기가 다르다** |
| R_ct(N) | R3+R4 5.2× (SLE) / 3.4× (BLE-10) @300 cyc 3C (derived) | Kang&Shin ASSB 4.4× / 1.5× @100 cyc; A10 v1 mono 1.05× / bimodal 1.51×(shrink-proxy, 재해석 대상) | 배수는 액체·황화물이 다른 물리(전해액 침투 vs SE 계면 분해) — **형태(단조 증가·bimodal 배치 민감)** 만 |
| 응력 크기 vs SE | LPC 표면 300 MPa (AM 내부) | MPM SE σ_y 0.15–0.30 GPa | ASSB 라면 AM 300 MPa 급 응력 옆의 SE 가 **항복/흐름**(J2) 하며 하중을 재분배 — 그들 액체계엔 없는 완화 경로 (정성) |
| 나노인덴테이션 | E_IT 5–6 GPa · H_IT 0.09–0.18 GPa (전극/입자 유효) | `wang2026` AFM 압입 1.26–3.06 GPa(전극), DEM E_eff 1.35 GPa(재배열 프록시) | **다른 양들** — 일치/불일치 표현 금지; SSC/LPC 경도비 ≈2.1 만 ASSUMED 파괴문턱 비 후보 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **Phase 5(층상 복합양극)의 첫 설계 문제로 채택**: "분리막 쪽 상층 = 소형 SC-NCM, 하층 = bimodal" 을 DEM 침대로 만들어(STEP1 층별 조성) STEP3 σ 삼중항 + STEP4 3C 반응분포·hot-spot 을 **상층 두께 {5,10,15,20 µm}** 로 스윕. 판정 변수 = 분리막 쪽 AM 표면 SOC 구배(Δc 상당)·SE 망 옴 강하·CC 분율. ⚠ ASSB 에선 소립 SC 층이 **SE 망 percolation/CN** 을 바꾸므로(Furnas·CN² 항) 액체계의 "굴곡도 병목(BLE-15/20)" 과 다른 병목이 나올 수 있다 — 그것 자체가 결과.
- ② **A10 확장**: f_broken·A_rel 을 **z-빈**으로 출력해 "분리막 쪽 vs 집전체 쪽" 비를 낸다. 그들 3.4/1.2 ≈ 2.9 는 액체계 값이라 표적이 아니라 **형태 대조**(단조 감소 여부).
- ③ **STEP4 검증 표적(형태)**: 3C 에서 Δc(분리막 쪽 LPC) ≫ Δc(집전체 쪽) 인가 — 우리 per-particle SOC(t) 출력으로 즉시 계산 가능. 우리 SSB 는 이온 옴 지배라 구배가 **더 가파를** 가능성 — 사전 예측으로 등록해 두고 확인.
- ④ **dQ/dV 열화모드 분해(Dubarry)** 를 `eis_drt_ica.py` ICA 뒤에 붙일 수 있다(SI Note 1 의 α·β 스케일링) — 랩 데이터(`cycling_data_ingest.py` sulfide 게이트) 로 LAMc/LLI 를 뽑아 `rint_cycle_traj` 와 나란히.
- ⑤ **"조성이 아니라 배치"** — 5:5 단층 무효 실증은 우리 predictor(설계→구조 ML) 의 입력에 **z-배치 변수**가 없다는 한계의 외부 증거. 백로그 등재.

## 9. 인용 가능 문장 (deck/paper용)
- "Lee et al. (Energy Storage Mater. 2026) show, with a particle-resolved 3D electrochemo-mechanical model validated by FIB-SEM, that fast-charge cracking in a bimodal Ni-rich cathode localizes in the large polycrystalline particles nearest the separator (crack areal fraction 3.4 % vs 1.2 % at the current collector), and that a 10 µm single-crystal top layer — not a higher single-crystal fraction — suppresses it (retention 62.4 → 76.2 % after 300 cycles at 3C)."
- "Their result that spatial placement, not composition, controls the stress hot-spot is a direct motivation for layered electrode design variables that homogeneous bimodal sweeps cannot capture."

## 10. 주의/한계 (over-claim 방지)
- **액체계 LIB** (LiPF₆ EC/DMC, 25 °C): 농도분극·전해액 침투·SEI/CEI 화학 전부 SSB 와 다르다. **어떤 수치도 우리 ASSB 앵커로 승격 금지** — 방향·방법·설계논리만.
- **모델 검증은 정성**: 응력·농도장은 실측되지 않았다(본문 스스로 "advanced techniques … would enable more direct validation"). 균열 위치 정합만 검증.
- **SSC 파라미터(i₀ 2 mA cm⁻², D_s 1×10⁻¹⁴) 는 "Assumed"** — LPC 와의 10×/50× 대비는 입력이지 결과가 아니다. Ω(부피변형률)·솔버·메시·입자 생성법 미기재 ⇒ 재현 불가.
- **선형탄성·소변형·이상 층간 계면**: 균열·소성·크리프 없음 → 300 MPa 는 "탄성 상한" 성격(우리 Cronk 카드 §F U1 와 같은 논점).
- **Nanoindentation 5–6 GPa 는 재료 E(191 GPa) 가 아니다** — SI 캡션이 "cathodes" 로, 전극/다공 2차입자 유효값. E_AM 앵커로 쓰지 말 것.
- 온도 시험은 BLE-10 단독(SLE 대조 없음, Fig S17). 6C 는 50 cyc 뿐.
- 유지율 62.4/76.2 % 는 **풀셀 3C 충전·1C 방전** 조건값 — 조건 없이 인용 금지.
- **남은 누락(본문·SI 둘 다 수신 후)**: 데이터셋 "available on request"(원시 필드·SEM 세트 없음); 참고문헌 PDF 미보유 — 특히 **[S3]/[49] Yuan, Lu, Xu ESM 60 (2023) 102834 (ASSB 복합양극 electrochemical-mechanical coupling failure)** 은 그들 역학 정식화의 원출처이자 **우리 축(황화물 복합양극) 그 자체**라 확보 1순위; [S4] Sturm 2019 (D_s LPC 출처), [46] Kang 2023 ESM(우리 랩, `kim2023_chemomech_failure_highstrain_anode` 계열) 대조.

## Supplementary Information (docx, 전수 전사)
**Note 1 — 열화모드 정량(Dubarry [S1])**: 풀셀 dV/dQ 를 신선/노화 반쪽셀 dV/dQ 의 스케일·시프트로 재구성. 전극 SOC ↔ 셀 SOC: 선형 스케일 α_c, α_a 와 시프트 β_c, β_a (eq 1; 수식 본문은 docx 수식 객체라 텍스트 추출에서 소실 — 형식만). 세 모드 LAMc / LAMa / LLI.
**Note 2 — 전기화학-역학 방정식** (eq 2–15): BV; Fick; 전해질 전류·질량보존; 고체 전하보존; 평형; 변형 분해 ε = ε_el + ε_ch [S3]; Hooke(E, ν); ε_ch = (ε_v/3)·c̃·I, ε_v = Ω 기반 (Ω = 완전 탈리튬 상대부피변화, 값 미기재).

| Table S1 | 값 |
|---|---|
| 셀 폭 × 길이 | 20 × 20 µm |
| 두께 음극 / 양극 / 분리막 | 61 / 50 / 15 µm |
| 기공률 양극 / 음극 / 분리막 | 0.30 / 0.40 / 0.40 |
| 음극 고체분율 | 0.59 |

| Table S2 | 값 | 출처 |
|---|---|---|
| c_max NCM92 (LPC, SSC) / graphite / Si–C | 50,060 / 31,507 / 278,000 mol m⁻³ | [S4] / [S5] / Assumed |
| i₀ SSC / LPC / graphite / Si–C | 2 / 20 / 1 / 0.1 mA cm⁻² | Assumed / [S6] / [S6] / Assumed |
| 전해질 σ / t⁺ / c₀ / D_e | 10 mS cm⁻¹ / 0.35 / 1000 mol m⁻³ / 2.5×10⁻⁶ m² s⁻¹ | [S7] / [S6] / Assumed / [S6] |
| D_s SSC / LPC / graphite / Si–C | 1×10⁻¹⁴ / 5×10⁻¹³ / 1.45×10⁻¹³ / 1×10⁻¹² m² s⁻¹ | Assumed / [S4] / [S8] / [S9] |
| C-rate | 0.33, 3 | |
| E / ν NCM92 | 191 GPa / 0.25 | [S10] |

| Table S3 (pristine) | R1 | R2 | R3 (Ω cm²) |
|---|---|---|---|
| SLE | 2.58 | 1.52 | 4.14 |
| BLE-10 | 3.16 | 1.54 | 3.99 |

| Table S4 (300 cyc 3C) | R1 | R2 | R3 | R4 (Ω cm²) |
|---|---|---|---|---|
| SLE | 1.75 | 2.58 | 8.79 | 12.79 |
| BLE-10 | 2.45 | 1.97 | 7.94 | 5.81 |

| SI Fig | 내용 (수치는 digitized) |
|---|---|
| S1 | 단층 LPC:SSC 5:5/6:4/7:3/8:2 밀도·용량 (§3) |
| S2 | LPC vs SSC 반쪽셀 전압곡선·율·3C 100 cyc |
| S3 | SLE 모델 충전 V(t): 0.33C ~2.85 h / 3C CC ~14.7 min → CV |
| S4 | 3C 말 전해질 Li⁺ 분포 (분리막 쪽 고갈) |
| S5 | SLE 단면 SEM, 상면 SEM/EDS (Ni·Co·Mn), 음극 EDS (C·Si·N) |
| S6 | SLE 300 cyc 3C 추가 단면 — 분리막 쪽 LPC 균열, 집전체 쪽 경미 |
| S7 | 원 LPC 입자 SEM: 구형 ~10 µm, sub-µm 1차입자 |
| S8 | SLE 균열 면적분율 3.438 / 1.174 % |
| S9 | E_IT 5.17 / 6.02 GPa, H_IT 0.086 / 0.18 GPa |
| S10 | BLE-5/10/15/20 3D 기하 |
| S11 | LPC(분리막 쪽) 반경 von Mises: 표면 ≈270 / 145 / 130 / 95 MPa |
| S12 | BLE-8·BLE-12 필드 (추세 일관) |
| S13 | BLE-10 캘린더링 전 상면·단면 (층간 혼합 없음) |
| S14 | pristine BLE-10 단면 (SSC 층 / LPC+SSC 층) |
| S15 | 4C 100 cyc ≈82 vs ≈62 %; 6C 50 cyc ≈80 vs ≈66 % (BLE-10 vs SLE) |
| S16 | 음극 pOCV (0.04C 2nd formation) |
| S17 | BLE 풀셀 45 °C·3C / −10 °C·1C 100 cyc |
| S18 | SLE vs 5:5 (동급) vs 2:8 (악화): 3C 사이클 + 율 |
| S19 | SPC 상층 BLE vs BLE-10: SPC 3.0→2.15 vs 2.95→2.57 (3C 100 cyc) |
| S20 | SPC 상층 100 cyc 후 균열 SEM |
| S21 | BLE-10 균열 면적분율 1.186 / 0.912 % |
| S22 | BLE-10 SSC 층 300 cyc 후 — 무균열, 계면 유지 |
| S23 | 상층 SSC XPS (C/O/F/Ni): Ni³⁺ 52.5 / Ni²⁺ 47.5 % |

## 우리 DEM+MPM 프레임 대비 · 적용 후보
| # | 리포 훅 | 이 논문이 주는 것 | 라벨 |
|---|---|---|---|
| ① | **A10 사이클 chemo-mech** — `docs/a10_cycle_chemomech_design.md`, `scripts/cycle_contact_ledger.py` (Bucci CZM G_c 2.8±1.8 J m⁻², ΔV≈3 % 개시, Γ<1000 게이트) | 우리에게 없는 **입자 내부 Δc → von Mises** 체인과 그 **z-분포**(분리막 쪽 집중). 흡수: f_broken·A_rel 의 z-빈 출력; 입자 내부 응력은 STEP4 per-particle SOC 프로파일에서 Δc 프록시로 (구형확산 c(r) 이미 있음) | 적용 후보 (형태 대조; 3.4/1.2 %·300 MPa 값은 액체계 — 앵커 금지) |
| ② | **Auerbach 파괴** — `fracture_aware_excluded_pct`, `frac_severe_force_pct` (압밀 시 AM 파괴, 힘 기준) | 그들 균열은 **사이클 구동**(H2–H3 격자변형)이라 우리 압밀 파괴와 다른 사건. 단 **"큰 다결정이 깨지고 작은 단결정은 안 깨진다"** 는 크기·결정성 서열은 같은 방향. SSC/LPC 경도비 ≈2.1 (Fig S9) | ASSUMED(§F1) — 파괴문턱 비 후보로만 |
| ③ | **poly vs SC 앵커** — `docs/ncm_sc_poly_electrochem_anchors.md` (ASSB 에선 SC 유리, poly = 입계 내부 void) | 액체계에서도 SC 상층이 이기지만 이유가 **기계 완충 + 균일 탈리튬**; 그들 D_s/i₀ 대비(50×/10×)는 **가정**이라 우리 §1 "액체 PC-빠름 GITT 이식 금지" 규율을 강화 | 해당 없음(값) / 규율 근거 |
| ④ | **STEP4 rate** — `docs/step4_v2_design.md`, `scripts/step4_dyn.py` (CCCV, per-particle D_s/i₀ 분리, hot-spot 맵) | 3C 에서 분리막 쪽 우선 탈리튬·CC 분율↓ 를 우리 SSB 침대에서 재현 가능 여부 = **형태 검증 표적**; 상층 두께 스윕(5/10/15/20 µm) 을 STEP4 설계 스윕으로 | 적용 후보 (Phase 5 층상 양극 첫 문제) |
| ⑤ | **황화물 SE 기계 앵커** — `docs/sulfide_se_mechanical_anchors.md` (K_IC 0.2–0.4 MPa m^½, SE 입경 >3 µm 파쇄 / <1 µm 협동변형) | 그쪽은 **SE 입자** 창, 이 논문은 **AM 입자**(12 µm 균열 / 3 µm 무균열) — 두 창을 겹치면 ASSB 상층 설계는 "소형 SC-AM + sub-µm SE" 로 수렴. 또 AM 300 MPa 급 응력 옆 SE 는 항복(σ_y 0.15–0.30 GPa) → 하중 재분배 | 적용 후보 (정성) |
| ⑥ | `scripts/eis_drt_ica.py` (Randles + Wo, ICA dQ/dV) · `docs/data/rint_eis_anchors.csv` · `rint_cycle_traj` | R1–R4 등가회로 값(Table S3/S4) = R_ct(N) 성장 **형태** 앵커(LIB); Dubarry LAMc/LLI 분해 절차(SI Note 1) 를 ICA 뒤에 배선 | 형태만 (액체계) |
| ⑦ | **Phase 5 층상 복합양극 · A7 graded-z** (`--poro-grad`, 설계 프로파일) | 기공률 구배가 아닌 **조성/입경 구배** 층상 설계의 실증; "같은 조성 단층은 무효" | 적용 후보 (설계 변수 추가) |
| ⑧ | `cycling_data_ingest.py` (chemistry 게이트: liquid = FORM/METHOD-ONLY) | 이 논문 사이클 데이터는 게이트상 **FORM/METHOD-ONLY** — 절대값 학습 금지 규약 그대로 | 해당 없음(값) |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
