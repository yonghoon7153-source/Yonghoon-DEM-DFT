<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = miss2026_insitu_conductivity_porosity_pressure_compaction.md · 주제 이웃 = zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md (이 논문 ref [3]).
     쪽 표기 = 학술지 인쇄 쪽 (Materials Today 99 (2026) 103484 — 본문 PDF 쪽 = 인쇄 쪽 1–10).  SI 는 "SI p.n" (SI PDF 쪽 1–8, 인쇄 쪽 번호 없음).
     값 표지: [인쇄] = 본문 · SI · 그림 범례 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (축 보정, 대략 — TREND 전용) ·
     [우리 산술] = 인쇄값으로 우리가 다시 계산한 값 · 이 논문 밖 우리 값과 엮은 계산 · [추정] = 논문이 말하지 않은 해석 · [미확인] = 본문 + SI 전수에 없음.
     원문 18 쪽 (본문 10 + SI 8) 전부 렌더 이미지로 읽고 pdftotext 로 인용문 대조.  그림 13 장 = 크롭 13 장 전부 열람. -->
# 후막 (≈150 µm · >6 mAh cm⁻²) NMC811–LPSCl 양극의 **"가운데 반응대"** — operando 중성자 투과 영상 + 사후 중성자 단층 + 단면 Raman 지도로 본 두께 방향 Li 재분포와 촉매전해질 (thiophosphate) 분해 위치 · 전류를 올리면 반응이 SE 계면 쪽으로 몰린다 — Kim · Adam · Li · Torres · Zhang · Li · Bilheux · Yang (Materials Today 2026)

> slug `kim2026_operando_neutron_thick_nmc811_interior_hotspot` · DOI `10.1016/j.mattod.2026.103484` · type `experiment (dry-process 후막 복합양극 · operando 중성자 투과 영상 + 사후 중성자 단층 + 단면 operando Raman 지도 + DRT impedance — 이 논문 안에 시뮬레이션 결과 없음 · 모델 주장은 자기 그룹 ref [26] 인용)` · PDF `1._Interior_transport_degradation_hotspots_in_high-loading_NMC811_sulfide_all-solid-state_batteries_revealed_by_operando_neutron_imaging.pdf` · SI `1._Sup_Interior_transport_degradation_hotspots_in_high-loading_NMC811_sulfide_all-solid-state_batteries_revealed_by_operando_neutron_imaging.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: **Chanho Kim**ᵃ'¹ · **Andre Adam**ᵃ'ᵇ'¹ (공동 1저자) · Yuanshun Liᵃ'ᶜ · James Torresᵈ · Yuxuan Zhangᵈ · Xianglin Liᵉ · Hassina Bilheuxᵈ · **Guang Yang**ᵃ'ᶠ'\* (ᵃ ORNL Chemical Sciences Division · ᵇ Univ. of Kansas 기계공학 · ᶜ Univ. of Tennessee Knoxville 화공 · ᵈ ORNL Neutron Scattering Division · ᵉ Washington Univ. in St. Louis · ᶠ UT Bredesen Center) · 교신 yangg@ornl.gov · *Materials Today* **99** (2026) 103484 (본문 10 쪽 + SI 8 쪽) · 접수 2026-05-25 · 수정 07-27 · 승인 08-05 · 온라인 **2026-08-15** · © 2026 Elsevier (UT-Battelle 정부 이용 고지) · 연구비 DOE CMEI / TTO **BMR** 프로그램 · 빔타임 HFIR **MARS** (IPTS-34509.1) · SNS **VENUS** (IPTS-35566) · CNMS2025-A-02967 · 자료 = *"Data will be made available on request"* [인쇄 p.10].
> **세미나 맥락**: 1저자 논문세미나 (2026-10) 에서 나온 두 편 중 하나 — 짝 카드 = `liu2024_sc_ni90_sulfur_coating_sulfide_assb` (단결정 Ni90 양극).
> **정본 litdb 이웃 (링크만)**: [`zhang2023_pfib_multiscale_imaging_4d_thick_cathode`](zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md) (= 이 논문 ref [3], 후막 NMC811 6 mAh cm⁻² · 4D Newman) · [`lee2025_corolling_dryprocess_lpscl_ptfe`](lee2025_corolling_dryprocess_lpscl_ptfe.md) (거의 같은 조성 80:17:3 + PTFE 0.5 — 복합체 σ_ion · σ_e 실측) · [`wang2026_dryprocess_thick_cathode_failure_ncm94`](wang2026_dryprocess_thick_cathode_failure_ncm94.md) (건식 후막 실패기전 · DRT) · [`luan2025_graded_cathode_400whkg_pouch`](luan2025_graded_cathode_400whkg_pouch.md) (graded 양극) · [`kang2025_toughened_bimodal_nca_lzo`](kang2025_toughened_bimodal_nca_lzo.md) (우리 랩 · 바이모달 대칭셀 EIS).

---

## 0. 결론 먼저 — 우리 질문 (6 mAh cm⁻² 후막 바이모달 NMC811–LPSCl 양극의 두께 방향 수송) 에 대한 답

**한 문장**: 실용 면용량 (충전 6.11 mAh cm⁻²) 의 Si/LPSCl/NMC811 전셀을 **operando 중성자 투과 영상**으로 보면, 0.5 mA cm⁻² 에서 양극의 Li 변화는 SE 쪽 → 집전체 쪽으로 단조 감소하는 기울기가 아니라 **양극 가운데 띠 (SE 계면에서 ≈37.5–75 µm)** 에서 가장 크고, 1.0 mA cm⁻² 로 올리면 전체 진폭이 줄면서 **NMC811–LPSCl 계면 쪽에 Li 결핍 띠**가 생긴다.  단면 Raman 은 **같은 가운데 영역**에서 S–S 분해 신호 (460/425 cm⁻¹ 비) 가 가장 크다고 보고한다.
⇒ 우리에게 주는 것 = **"후막 양극에서 반응이 어디서 일어나는가" 의 실측 지도 (상대값)** 와 **"전류를 2 배 올리면 반응이 분리막 쪽으로 몰린다"** 는 정성 증거.  주지 않는 것 = 복합체 σ_ion · σ_e · tortuosity · 공극률 · NMC 입경 · 단결정/다결정 여부 · 성형압 — **전부 [미확인]**.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 6 mAh cm⁻² 급 후막의 두께 방향 반응 분포 | 0.5 mA cm⁻² (그림 표기 "C/10"): 최대 Li 변화 = 양극 **가운데 띠** — 초록 *"about 37.5–75 µm from the LPSCl interface"* · 본문 *"a band located about 50 um from that interface"* · Fig. 4a 판독: 충전 끝 −50 % 등고선이 집전체에서 ≈42–136 µm, 가장 깊은 곳 ≈83 µm (SE 쪽에서 ≈67 µm) | [인쇄] p.1 · p.3 · Fig. 4a [판독] |
| ② 반응이 **어디서 시작**하나 | 충전 시작 (*"Delithiation Onset"*) = **집전체 쪽** 37.5–75 µm (Fig. 4a 타원 ≈9–83 µm, 0.3–2.9 h) → 가운데 (75–112.5 µm) 로 이동.  방전도 **집전체 쪽에서 먼저** 재리튬화 → SE 쪽으로 번짐 | [인쇄] p.4 · p.5 · p.6 · Fig. 4 [판독] |
| ③ 전류를 올리면 | 1.0 mA cm⁻² ("C/5"): 전 두께 진폭 감소 + **NMC811–LPSCl 계면 Li 결핍 띠** (*"interfacial Li starvation"*) · 그림 시간축 × 전류 = 충전 ≈4.65 → ≈2.8 mAh cm⁻² · 방전 ≈4.6 → ≈2.05 mAh cm⁻² (형성 뒤 사이클) | [인쇄] p.4 · Fig. 3a/e [판독 + 우리 산술] |
| ④ 저자의 기전 설명 | *"an interior location where ionic and electronic transport resistances are optimally balanced"* — 자기 그룹 TWIF-Li 모델 [26] 이 *"parameter-free"* 로 재현했다고 **서술만** (이 논문에 모델 그림 · 수치 없음) | [인쇄] p.5–6 · 모델 결과 [미확인] |
| ⑤ 촉매전해질 분해 위치 | Raman 460/425 cm⁻¹ 비 (정규화 %): 가운데 10 → 30 → 44 → 44 → **47** · SE 쪽 6 → 29 → 41 → 39 → 41 · 집전체 쪽 9 → 20 → 37 → (75 % 칸 누락, 판독 ≈36) → 34 (pristine → 100 % SoC) — ⚠ 오차막대가 세 영역에서 겹친다 | [인쇄] p.7–8 · Fig. 6h [판독] |
| ⑥ 복합체 σ_ion · σ_e · tortuosity · 공극률 | **측정 · 보고 없음** | [미확인] |
| ⑦ NMC811 단결정 / 다결정 · 입경 · 성형압 | **기재 없음** — "LiNbO₃-coated NMC811" 만.  FIB 단면 (Fig. S5) 에 구형 입자 ≈5–25 µm 원형 단면 | [미확인] · Fig. S5 [판독] |
| ⑧ 운전 중 스택 압력 | 다른 (같은 구성) 셀의 압력 센서: 1 사이클 **20.8–21.5 MPa** → 이후 **20.2–21.0 MPa** | [인쇄] p.9 · Fig. S4 |

**우리 모델과 엮으면 (요약 — 상세 §7)**:
- 이 조성 (NMC811 : LPSCl : VGCF : PTFE = **80 : 16 : 3 : 1** wt%) 은 정본 카드 Lee 2025 (80 : 17 : 3 + PTFE 0.5) 와 거의 같고, 그 카드의 실측 **σ_e 33–34 mS/cm ↔ σ_ion 0.069–0.076 mS/cm** (전자가 이온보다 ≈450–490 배) [우리 산술 · 교차 논문].  고전 다공전극 그림에서는 σ_e ≫ σ_ion 이면 반응이 **분리막 (SE) 쪽**에 몰린다 [추정 — 교과서 그림, 이 논문 밖].  ⇒ 1.0 mA cm⁻² 의 계면 결핍 띠는 그 그림과 맞고, **0.5 mA cm⁻² 의 "집전체 쪽 시작 + 가운데 최대" 는 벌크 유효 전도도 비만으로는 설명되지 않는다** — 저자의 "이온 · 전자 저항 균형" 설명은 이 논문 자료로 검증되지 않는다 (§10-1).
- 우리 ps45 침대 (6 mAh cm⁻², 300 MPa, 모델 두께 ≈111 µm, 탄소 없음) 의 Hertz σ_ion 0.0587–0.0893 mS/cm 로 양극 이온 저항을 어림하면 **124–189 Ω·cm²** → 1 mA cm⁻² 에서 두께 전체 옴 강하 상한 **0.12–0.19 V** [우리 산술] — 이 논문이 2 배 전류에서 용량을 ≈40 % 잃은 크기와 같은 방향 (§7-3).
- 우리 DEM 망은 **유효 σ · 수송 tortuosity (한 값)** 를 낼 뿐, **두께 방향 · 시간 방향 반응 분포**는 안 낸다 → 이 논문의 Fig. 4 같은 지도와 대조하려면 STEP4 (BV 반응분포 · 갈바노 시간전개) 가 필요하다 (CLAUDE.md STEP 파이프라인 · 수치 패리티 런 대기) — §7-5 · §8.

---

## 1. 한 줄 요약
Si (N/P ≈ 1.1) / LPSCl 시트 / **LiNbO₃ 코팅 NMC811 건식 복합양극 (25 mg cm⁻², ⌀4 mm)** 전셀을 PTFE 몸통 operando 셀에 넣고 HFIR **MARS** 빔라인에서 5 분마다 중성자 투과 영상을 찍어 (유효 화소 7.75 µm · 기하 흐림 ≈40 µm) pristine 대비 투과 비로 **두께 방향 상대 Li 변화**를 본다 → 0.5 mA cm⁻² 에서 **가운데 반응대**, 1.0 mA cm⁻² 에서 **SE 계면 Li 결핍**; 사후 단층 (방전 · 충전 뒤) 은 가운데의 잔류 대비, C/50 operando Raman 은 가운데의 S–S 분해 신호가 가장 크다 → *"interior transport–degradation hotspot"* · 설계 목표를 계면 공학에서 **내부 이용률 제어**로 옮기자는 주장.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| C. Kim, A. Adam (공동 1저자), Y. Li, J. Torres, Y. Zhang, X. Li, H. Bilheux, **G. Yang\*** (ORNL 외) | Materials Today 99 (2026) 103484 | 10.1016/j.mattod.2026.103484 | **LPSCl (Li₆PS₅Cl)** 촉매전해질 + SE 시트 (LPSCl d50 5 µm + PIB 5 wt%) · **LiNbO₃ 코팅 NMC811** (형상 · 입경 [미확인]) · VGCF · PTFE · 음극 = µm 급 Si (PVDF 0.1 wt%) | 실험 — operando 중성자 투과 영상 · 사후 중성자 단층 · operando 단면 Raman 지도 · DRT · 압력 센서.  **시뮬레이션 없음** (모델 주장 = ref [26] 인용) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 셀 · 재료 상수
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 셀 구성 | Si / LPSCl / **LiNbO₃-NMC811** 전셀 · 양극 집전체 = 탄소 코팅 Al 박 · Si 는 Cu 박 위 | [인쇄] p.2 · p.9 |
| 양극 조성 (건식) | **LiNbO₃-NMC811 : LPSCl : VGCF : PTFE = 80 : 16 : 3 : 1** (wt) — 건식 혼합 → 압연 → ⌀**4 mm** 펀칭 | [인쇄] p.9 |
| 양극 로딩 | operando 중성자 셀 **25 mg cm⁻²** (*"practical-loading cathodes"*) · DRT 셀 **10 mg cm⁻²** · ⚠ SI Appendix A 계산은 **30 mg cm⁻²** 로 함 · 로딩 기준 (복합체 / NMC) 미기재 | [인쇄] p.9 · SI p.2 |
| 양극 두께 | **≈150 µm** (*"FIB-SEM benchmark"*, Fig. S5 화살표 *"~150 µm"* · SI 계산 *"estimated roughly 150 µm"*) · 투과 선 단면 (Fig. 2d) 의 양극 띠 ≈250–415 µm = ≈165 µm (흐림 포함) | [인쇄] SI p.2 · Fig. S5 · Fig. 2d [판독] |
| SE 시트 | poly(isobutylene) (평균 분자량 ≈1270 kg mol⁻¹) : LPSCl (**d50 = 5 µm**) = 5 : 95 질량, 톨루엔 54 wt% 고형분 · 지르코니아 저속 볼밀 18 h · 닥터블레이드 (Mylar) · 밀봉 파우치 안 **상온 냉간 압연** · 밤새 진공 건조 · ⌀6 mm 원판 **2 장 적층 후 압축** (압력 [미확인]) · Fig. 2d 의 SE 띠 ≈175 µm | [인쇄] p.9 · [판독] |
| Si 음극 | µm 급 Si : PVDF = 99.9 : 0.1 (NMP, 24 h 교반) · Cu 박 캐스팅 · 70 °C 건조 → 80 °C 진공 2 h · ⌀6 mm · **N/P ≈ 1.1** (이전 연구에서 최적화 · 과량 Li 는 Si 쪽에 금속 Li 로 석출된다고 서술) | [인쇄] p.9 |
| 셀 몸통 | PTFE 몰드 + 스테인리스 플런저 + 압력 유지 프레임 · 세라믹 절연체 (Fig. 1b) | [인쇄] p.2 · p.9 |
| 운전 중 스택 압력 (별도 같은 구성 셀) | 1 사이클 **≈20.8 → 21.5 MPa** · 이후 **20.2–21.0 MPa** · 사이클마다 충전 시 +≈0.7 MPa (Si 리튬화 팽창 방향) | [인쇄] p.9 · Fig. S4 [판독] |
| 성형압 · 양극 공극률 · 온도 | **[미확인]** (본문 · SI 전수) | — |
| NMC811 형상 (SC/PC) · 입경 · LPSCl 촉매전해질 입경 | **[미확인]** — 참고문헌 [9] (자기 그룹) 이 *"dry-processed single-crystal NMC811"* 이지만 이 논문 양극이 그것인지 서술 없음 | [미확인] |

### 3-2. 전기화학
| 조건 | 값 | 표지 · 쪽 |
|---|---|---|
| 첫 사이클 (형성) 0.5 mA cm⁻², 2.6–4.3 V | 충전 **6.11** · 방전 **4.37 mAh cm⁻²** → 쿨롱효율 **71.5 %** | [인쇄] p.2 · [우리 산술] |
| 그 시간축 (Fig. 2a, "C/10 (0.5 mA cm⁻²)") | 충전 끝 ≈12.8 h · 방전 끝 ≈22.0 h | [판독] |
| 형성 뒤 저전류 (Fig. 3a, "C/10 (0.5 mA cm⁻²)") | 충전 끝 ≈9.3 h → ≈4.65 mAh cm⁻² · 방전 끝 ≈18.5 h → ≈4.6 mAh cm⁻² · 전류 반전 시 전압 계단 4.3 → ≈3.97 V (휴지 여부 [미확인]) | [판독 + 우리 산술] |
| 형성 뒤 고전류 (Fig. 3e, "C/5 (1 mA cm⁻²)") | 충전 끝 ≈2.8 h → ≈2.8 mAh cm⁻² · 방전 곡선 끝 ≈4.85 h (≈2.85 V — 2.6 V 하한 전에 끝남) → ≈2.05 mAh cm⁻² · 반전 계단 4.3 → ≈3.85 V | [판독 + 우리 산술] |
| 사후 단층용 셀 (0.05 mA cm⁻²) | 첫 충전 **218 mAh g⁻¹** · 방전 **177 mAh g⁻¹** (→ 81.2 %) | [인쇄] p.6 · [우리 산술] |
| 비용량 환산 (형성 6.11 / 4.37 mAh cm⁻²) | 25 mg cm⁻² 를 복합체로 (NMC 80 %) 읽으면 **305.5 / 218.5** mAh g⁻¹ · NMC 질량으로 읽으면 **244.4 / 174.8** · SI 의 30 mg cm⁻² (NMC 질량 — SI 계산이 그렇게 씀) 면 203.7 / 145.7 | [우리 산술] — 기준 미기재라 판정 못 함 |
| C-rate 대응 | DRT 셀 (10 mg cm⁻²) 0.2 · 0.4 mA cm⁻² ↔ 중성자 셀 (25 mg cm⁻²) 0.5 · 1.0 mA cm⁻² = *"comparable C-rates (approximately C/10 and C/5)"* (전류/로딩 비 0.02 로 같다) · 6.11 mAh cm⁻² 기준이면 0.5 mA cm⁻² = 12.2 h (≈C/12) | [인쇄] p.9 · [우리 산술] |
| operando Raman 셀 | **C/50** 충전 (Fig. S3: ≈3.5 → 4.3 V, ≈3050 min ≈ 50.8 h) | [인쇄] p.6 · Fig. S3 [판독] |

### 3-3. 중성자 영상 사양 (MARS @ HFIR · p.9–10)
| 항목 | 값 | 표지 |
|---|---|---|
| 빔 | 다색 중성자 **0.8–6 Å**, 피크 **2.6 Å** · 핀홀 **11 mm** · 핀홀–검출기 **6.59 m** (L/D ≈ 599 [우리 산술]) | [인쇄] p.9 |
| 검출기 | QHY600M Pro sCMOS + 20 µm Gd₂O₂S:Tb (20 % ⁶LiF:ZnS 포함) 섬광체 · 5 분마다 영상 (전송 ≈2.5 s) | [인쇄] p.9–10 |
| 화소 · 해상도 | ≈0.5× 배율 × 고유 화소 3.76 µm → **유효 화소 7.75 µm** (⚠ 3.76/0.5 = 7.52 [우리 산술]) · 명목 해상도 **≈25 µm (≈3 화소)** · **기하 흐림 ≈40 µm** (시료–검출기 거리 지배 · 최대 불확도) · 내부 반응대 명목 폭 ≈50 µm | [인쇄] p.10 |
| 화소로 환산 | 양극 150 µm ≈ 19 화소 · 37.5 µm ≈ 4.8 화소 · 흐림 40 µm ≈ 5.2 화소 | [우리 산술] |
| 처리 | 배경 정규화 · 빔 세기 요동 보정 · 영상 정합 → 투과 영상 · **pristine 대비 투과 비 (ratio) 영상** · 선 단면 = 셀 가운데 영역에서 두께 방향 평균 | [인쇄] p.2–3 · p.10 |
| 단층 | 방전 뒤 (Fig. 5) · 충전 뒤 (Fig. S2) · ImageJ 로 세 영역 대비 비교 (*"middle region consistently exhibited the highest"*) — **수치 미보고** · 단층 빔라인 (사사에 VENUS) · 획득 조건 [미확인] | [인쇄] p.6 |

### 3-4. ★ 반응대 위치 — 인쇄 문장과 Fig. 4 판독
- 인쇄 문장 셋 (기준면이 다르다 — §10-6):
  - 초록: *"a persistent interior reaction zone emerges about 37.5–75 µm from the LPSCl interface and exhibits the largest attenuation change throughout the first cycle"* [p.1]
  - 결과: *"a band located about 50 um from that interface [NMC811|LPSCl] exhibits the strongest signal evolution throughout cycling"* [p.3]
  - 결과: *"the onset of lithium depletion is … approximately 37.5–75 μm from the current collector, with the preferential reaction zone subsequently evolving toward the middle region of the cathode (75–112.5 μm)"* [p.6]
- Fig. 4 축: 거리 0 = 집전체 · 150 µm = SE 쪽 (눈금 37.5 · 75 · 112.5) · ΔC_Li 색 0 → **−54.4 %** · 등고선 = 20 % · 35 % · 50 % Li 감소.
- **충전 (Fig. 4a, 0–12.9 h, SOC 0–100 %)** [판독]: 시작 타원 ≈9–83 µm (중심 ≈46 µm) · 0.3–2.9 h → −20 % 등고선 첫 등장 ≈4.4 h @ ≈56 µm → −35 % ≈6.9 h @ ≈72 µm → −50 % ≈10.3 h @ ≈70 µm → 충전 끝 −50 % 영역 ≈42–136 µm, 가장 깊은 곳 ≈83 µm.  윗 경계 (SE 쪽 135–150 µm) 는 −40…−47 %, 아래 (집전체 0–3 µm) 는 −20 % 보다 얕다.
- **방전 (Fig. 4b, 0–8 h, DoD 0–100 %)** [판독]: −50 % 영역 ≈44–134 µm 에서 시작해 ≈2.3 h 에 사라짐 · −35 % 꼬리 ≈5.7 h @ ≈120 µm · −20 % 꼬리 ≈7.7 h @ ≈120 µm — **가장 늦게 다시 채워지는 곳 ≈110–120 µm (SE 쪽에서 ≈30–40 µm)** · 방전 끝 색: 집전체 쪽 −5…−10 % · 가운데 ≈−20 % · SE 쪽 ≈−15 % (잔류 결핍).
- 3D 곡면 (Fig. 4c): 같은 자료 — 충전 끝 최저 ≈−55…−60 % (z 축 판독) · *"the most pronounced concentration drop occurring in the middle region"* [인쇄 p.5].
- ⚠ Fig. 4b 시간축 0–8 h ↔ Fig. 2a 방전 ≈9.2 h · Fig. 3a 방전 ≈9.2 h — **어느 사이클의 자료인지 미기재** [미확인].

### 3-5. Raman 분해 신호 (Fig. 6 · Table 1 · p.6–8)
- 측정: Horiba XploRA 공초점 · **405 nm** · < 500 µW · 지도 ≈**200 µm × 25 µm**, **40 × 10** 스펙트럼 (간격 5 µm × 2.5 µm [우리 산술]) · 300–800 cm⁻¹ · ball-rolling 배경 · 391 · 425 · 460 cm⁻¹ 세기 → **460/425 비** 지도 [인쇄 p.9].
- 띠 귀속 (Table 1 중): 391 = P₂S₇⁴⁻, ν(P–S_b)+ν(P–S_t) · **425 = PS₄³⁻ ν₁ 대칭 신축** · **460 = Li₂Sₓ 의 S–S 굽힘** · 488 = 비정질 Si · 520 = 결정 Si TO · 575 = PS₄³⁻ [인쇄 p.7].
- 영역 평균 정규화 비 (Fig. 6h, pristine → 25 → 50 → 75 → 100 % SoC) [인쇄 p.7–8]:

| 영역 | pristine | 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|---|
| 집전체 쪽 | 9 % | 20 % | 37 % | **(인쇄 누락 — 판독 ≈36 %)** | 34 % |
| 가운데 | 10 % | 30 % | 44 % | 44 % | **47 %** |
| SE 쪽 | 6 % | 29 % | 41 % | 39 % | 41 % |

  - 본문: *"The average intensity ratio on the current collector side increased from 9 % to 20 %, 37 %, and 34 % with increasing SoC"* — 다섯 상태에 네 값만 인쇄 [인쇄 p.7].  그림 y 축은 "Normalized Intensity (a.u.)" (눈금 숫자 없음) · 판독 격자 = 10 %/칸 으로 인쇄값 14 개를 ±1 %p 안에서 재현 [판독].
  - ⚠ **오차막대가 세 영역에서 크게 겹친다** (예: 100 % SoC 가운데 ≈27–60 % · SE 쪽 ≈31–51 %, 판독 · 집전체 쪽 막대는 다른 막대에 가려 판독 불가 — 축 격자 10 %/칸 은 인쇄값 14 개로 확인) · 오차막대의 뜻 (표준편차 · 화소 수) [미확인] · 시료 1 개.
- Fig. 6b 지도 축: *"Cathode Thickness (um)"* 0 → ≈195 µm · 빨간 점선 *"Active zone"* ≈92–157 µm [판독] — 광학상 (Fig. 6a) 의 양극 ≈160 µm (50 µm 막대 기준, 판독) · 왼쪽 = 플런저 (집전체 쪽) · 오른쪽 = 전해질.
- 스펙트럼 (Fig. 6c–g): pristine 은 391 · 425 cm⁻¹ 뚜렷 (SE 쪽이 가장 강함) → 충전하며 약해지고 넓어짐 · 460 cm⁻¹ 표지 *"S-S species"* · SE 쪽 스펙트럼은 25–100 % SoC 에서 ≈395–400 cm⁻¹ 의 강한 띠 (그림 판독 — 본문 설명 없음).

### 3-6. DRT (Fig. S1 · p.4 · p.9)
- 셀 = 10 mg cm⁻² · 충전 중 여러 SoC · **0.2 · 0.4 mA cm⁻²** (색 = SOC 2.77–100 % · 3.68–100 %) [인쇄 SI p.4].
- 판독: τ ≈10⁻⁶ s 봉우리 γ ≈430 (두 전류 · 전 SoC 같음) · τ ≈3×10⁻³ s 봉우리 0.2 mA: ≈175 → ≈275 (SoC↑, 긴 τ 쪽으로 이동) · 0.4 mA: ≈160 → ≈225 · τ > 0.1 s 꼬리 0.4 mA 의 낮은 SoC (3.68 %) 에서 τ ≈1 s ≈140 · 10 s ≈190 [판독].
- 저자 읽기: 저전류 = 중간 τ 전하이동 특성이 SoC 에 따라 변함 · 고전류 = 긴 τ 확산 기여가 지배해 SoC 의존을 *"largely mask"* [인쇄 p.4].  ⚠ 판독상 0.4 mA 에서도 중간 봉우리가 SoC 따라 ≈40 % 변한다 — "가린다" 보다 "줄어든다" 가 그림에 맞다.
- ⚠ **획득 조건 · 맞춤 세부 미보고**: Methods 문장이 *"the acquisition parameters and fitting details should be reported consistently with the cycling conditions used in the main text and Supporting Information"* [인쇄 p.10] — 지시문처럼 읽히고 실제 값 (주파수 범위 · 진폭 · 정규화 · 휴지) 은 어디에도 없다 [미확인].

### 3-7. 사후 단층 (Fig. 5 · Fig. S2)
- 방전 뒤 (0.05 mA cm⁻² 셀): Si 는 *"comparatively uniform"* · 양극은 가운데 (Fig. 5e) 가 가장 붉다 (재구성 대비 색 0.939–2.535–4.131, 단위 미기재) [인쇄 p.6 · 판독].
- 충전 뒤 (Fig. S2): *"asymmetric contrast across both electrodes"* [인쇄 p.6].  ⚠ Fig. S2 캡션은 (c) = 양극 SE 쪽 · (d) = 집전체 쪽인데 **그림 속 글자는 (c) Cathode (CC side) · (d) Cathode (SE side)** — 서로 바뀌었다.
- 저자 단서: 끝점 영상은 Li 뿐 아니라 밀도 · 미세구조 변화도 담으므로 *"Li-sensitive rather than arising solely from lithium distribution"* [인쇄 p.6–7].

### 3-8. 압력 (Fig. S4)
- 압력 축 ≈20–21.6 MPa · 매 사이클 톱니 (충전 상승) · 봉우리 21.6 → 21.35 → 21.2 → 21.1 → 20.95 · 골 20.6 → 20.45 → 20.3 → 20.2 → 20.1 MPa [판독].
- ⚠ 같은 그림의 전압이 **≈1.7–3.7 V** 사이를 오간다 [판독] — 본문 *"identical cell configuration and cycling protocol"* (2.6–4.3 V) 과 맞지 않는다 (축 표기 오류인지 다른 셀인지 [미확인]).

### 3-9. SI Appendix A · B — ΔC_Li 환산 식 (SI p.2–3, 렌더 대조)
- **A (초기 Li 농도)**: NMC 만 Li 를 잃는다고 가정 (부반응 · SE 변화 무시) · *"LiNi₀.₈Mo₀.₁Co₀.₁O₂"* (⚠ Mn 오기) 의 Li = 질량의 **7.10 %** · 로딩 **30 mg cm⁻²** · ⌀4 mm → 쓸 수 있는 Li **0.268 mg** · 두께 ≈150 µm → **C_Li ≈ 2.0572 × 10⁴ mol m⁻³** [인쇄].
  - 재계산: NMC811 (Mn) 의 Li 질량분율 7.135 % (Mo 오기면 6.846 %) · Li 0.2677 mg · C_Li **2.046 × 10⁴** (인쇄값과 0.6 % 차) · 이 Li 가 전부 나오면 **8.23 mAh cm⁻²** → 형성 충전 6.11 = 그 **74.3 %** (25 mg cm⁻² 로 하면 6.85 mAh cm⁻² · 89.1 %) [우리 산술].
- **B (투과 → Li 변화)**: Beer–Lambert **T = I/I₀ = e^(−µx)** (Eq. S1) · **µᵢ = σᵢ cᵢ N_A** (Eq. S2, ⚠ 본문 단위 "mol/m²" 는 mol/m³ 오기) · Li 외 원소 불변 가정 → **T_t/T₀ = e^(−x σ_Li N_A Δc_Li)** (Eq. S4) · **σ_Li = 71 barn** · 빔 방향 평균 두께 **x = ½πr** (⌀4 mm 원판의 평균 현 길이) [인쇄].
  - 재계산: x = 3.14 mm · x σ_Li N_A = 1.343 × 10⁻⁵ m³ mol⁻¹ → Li 20 / 35 / 50 / 54.4 % 감소 = 투과 비 **1.057 / 1.102 / 1.148 / 1.162** [우리 산술].
  - 저자 단서 (SI 에 노란 강조 = 수정 표시가 남아 있다): *"allowing neutron attenuation to serve as a relative indicator of lithium redistribution rather than an absolute measurement of lithium content"* [인쇄 SI p.3].

---

## 4. ★ 방법 — 실험 사슬 · 입자 처리

### 4-1. 셀 · 제조 (p.9)
- SE 시트 (슬러리 → 냉간 압연) · 양극 (건식 혼합 → 압연 → ⌀4 mm) · Si 음극 (슬러리 → ⌀6 mm) — §3-1 표.
- 조립: PTFE 몰드 · 스테인리스 플런저 · 압력 유지 프레임 · SE 원판 2 장 → 압축 → 한쪽에 양극, 반대쪽에 Si · 양극 집전체 탄소 코팅 Al.
- 스택 압력 실측 셀은 **따로** (같은 구성 · 같은 프로토콜이라 서술 — 그러나 Fig. S4 전압 범위 불일치 §3-8).

### 4-2. Operando 중성자 투과 영상 (p.2–6 · p.9–10)
- PTFE 몸통 = 기생 감쇠 최소 + 고체–고체 접촉용 압력 유지 (Fig. 1b).  고니오미터 스테이지 · 시준 빔 · 고해상 검출기 (Fig. 1a).
- 투과 영상 (정적 대비) → **pristine 영상으로 나눈 비 영상** (변화만) → 색 지도 (Fig. 2b–c, 3b/f) · 셀 가운데 영역 두께 방향 평균 **선 단면** (Fig. 2d–f, 3c–d/g–h) · 반경 방향 평균 → **시공간 지도** ΔC_Li(z, t) (Fig. 4, Eq. S4 환산).
- 중성자는 Li 에 민감 (σ_Li 71 barn) → 투과 증가 = Li 감소 (양극 충전) · 투과 감소 = Li 증가 (Si 충전) · Si 층 두께 증가 (팽창) 도 영상에 보임.

### 4-3. 사후 중성자 단층 (p.6)
- 방전 뒤 (0.05 mA cm⁻² 셀) · 충전 뒤 — 재구성 볼륨에서 직교 단면 · 같은 재구성 조건 · 같은 색 스케일로 세 영역 (SE 쪽 · 가운데 · 집전체 쪽) 대비 ImageJ 비교 (수치 미보고).

### 4-4. Operando 단면 Raman (p.6–9)
- 단면 시료를 C/50 으로 충전하며 pristine · 25 · 50 · 75 · 100 % SoC 에서 지도 · 지도를 두께 방향 세 영역으로 나눠 평균 (Fig. 6h).
- 저전류를 쓴 이유: 레이저 조사 영역의 상 변화를 풀 만큼 스펙트럼 획득 시간을 확보 (p.9).

### 4-5. DRT · 압력 (p.4 · p.9)
- DRT = 저로딩 (10 mg cm⁻²) 셀 · 같은 C-rate 대응 전류 (0.2 · 0.4 mA cm⁻²) — 측정 시간 절약 목적 (p.9).  획득 · 맞춤 조건 [미확인].
- 압력 = 같은 구성 별도 셀의 내장 압력 센서 (Fig. S4).

### 4-6. 입자 처리 ★ · 시뮬레이션 · frame[5]
- **시뮬레이션 없음** — 입자 모델 · 접촉 법칙 · 망 · 연속체 어느 것도 이 논문에 없다.  TWIF-Li ([26], *"parameter-free transport–kinetics framework … integrating image-derived FIB-SEM microstructures, GITT-derived concentration-dependent Li diffusion, and tortuosity-weighted interfacial kinetics"*) 는 **인용만** [인쇄 p.5–6].
- 실제 입자 (판독 · 서술): NMC811 = FIB 단면의 원형 단면 ≈5–25 µm (구형 2 차입자처럼 보임 [추정]) · LPSCl = SE 시트용 d50 5 µm (양극 쪽 입경 [미확인]) · VGCF 3 wt% · PTFE 1 wt% (건식 피브릴 바인더 — 피브릴 형상 미관찰).
- frame[5]: 이 논문은 **수송의 결과 (반응 분포 · 이용률)** 를 실측한다 — 우리 DEM 이 맡는 **접촉망 수송** (σ_ion · σ_e · 퍼콜레이션 · τ) 의 **하류 관측량**이다.  없는 반쪽 = 미세구조 · 접촉망 · 유효 전도도 · 기계 (형상 변화) — 전부.

### 4-7. 기법 미니 용어집
- **중성자 투과 영상 (radiography)** — 시료를 지나온 중성자 세기 지도.  Li (특히 ⁶Li) 가 중성자를 잘 흡수해 Li 함량 변화가 대비로 보인다.  X 선과 달리 가벼운 원소에 민감.
- **투과 비 (ratio) 영상** — 각 시점 영상 / pristine 영상.  1 보다 크면 Li 감소 (투과 증가).
- **Beer–Lambert** — T = e^(−µx) · µ = Σ σᵢ cᵢ N_A (원소별 단면적 × 농도).
- **기하 흐림 (geometric unsharpness)** — 핀홀 크기 D 와 시료–검출기 거리 때문에 경계가 퍼지는 폭 (여기 ≈40 µm) — 해상도의 실제 한계.
- **중성자 단층 (tomography)** — 여러 각도의 투과 영상으로 3D 재구성.
- **SoC / SoD** — 충전 상태 / 방전 상태 (이 논문의 단계 표기).
- **DRT (distribution of relaxation times)** — 임피던스를 이완 시간 τ 의 분포 γ(τ) 로 풀어 과정 (전하이동 · 확산 등) 을 시간 척도로 가르는 해석.
- **ν₁ PS₄³⁻ (425 cm⁻¹)** — LPSCl 의 대표 Raman 띠.  **460 cm⁻¹ S–S** — 산화 분해로 생기는 다황화물 (Li₂Sₓ) 계 신호.  비 460/425 = 분해 지표.
- **N/P 비** — 음극 용량 / 양극 용량 (여기 ≈1.1).
- **catholyte (촉매전해질)** — 양극 복합체 안의 SE (여기 LPSCl).
- **LiNbO₃ 코팅** — 산화물 양극과 황화물 SE 사이의 반응 · 공간전하층 완화용 얇은 피막.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) MARS 실험 배치 — 카메라 · operando 셀 · CT 셀 · 고니오미터 (b) PTFE operando 셀 (플런저 · 집전체 · 절연체) (c) 조립 셀 중성자 사진 (d) 투과 영상 (NMC811 쪽 / Si 쪽, 회색 0–1) (e) 상대 세기 색 영상 (0.61–1.28) | operando 셀 설계 (PTFE 몸통 · 압력 유지) — 우리 실험 협업 시 참고 |
| 2 | 형성 사이클 0.5 mA cm⁻² — (a) 전압–시간 + 선택 상태 (b, c) 충전 · 방전 비 지도 (400 µm 막대) (d, e) 두께 방향 투과 단면 (집전체 · 양극 · SE · Si 띠 표시) (f) pristine · 충전 · 방전 비교 — *"Irreversible capacity loss"* (양극) · *"Trapped Li"* (Si) | ★ 두께 방향 반응 분포의 실측 모양 · 첫 사이클 비가역이 **양극 안에서 고르지 않다** |
| 3 | 형성 뒤 저전류 (a–d, 0.5) vs 고전류 (e–h, 1.0 mA cm⁻²) — 전압 (시간 세로축) · 비 지도 · 충전/방전 단면 | ★ **전류 2 배 → 용량 ≈40 % 감소 + SE 계면 결핍 띠** — 후막 이온 수송 제한의 정성 증거 (우리 R_ion 어림과 대조, §7-3) |
| 4 | (a) 충전 · (b) 방전 시공간 지도 ΔC_Li(거리, 시간) — 집전체 0 · SE 150 µm · 20/35/50 % 등고선 · *"Delithiation Onset"* 타원 (c) 3D 곡면 | ★★ 이 논문의 핵심 그림 — 반응 시작 (집전체 쪽) ↔ 최대 (가운데) ↔ 마지막 재리튬화 (SE 쪽 30–40 µm) 의 **비대칭**이 정보 (§10-2) · STEP4 깊이 프로파일 대조 표적 |
| 5 | 방전 뒤 중성자 단층 — Si (a 집전체 · b 가운데 · c SE 쪽) · 양극 (d SE 쪽 · e 가운데 · f 집전체 쪽) | 양극 가운데의 잔류 대비 (정성) — Li 와 밀도 · 미세구조가 섞인 신호 |
| 6 | 단면 Raman — (a) 광학상 + 지도 영역 (b) 460/425 비 지도 (pristine → 100 % SoC, "Active zone") (c–g) 세 위치 스펙트럼 (h) 영역 평균 비 vs SoC | ★ 분해 신호의 위치 — 가운데 최대 (단 오차막대 겹침) · 우리 SE 분해 (탄소–SE 면적) 훅과의 위치 대조 표적 |
| Table 1 | Raman 띠 귀속 17 줄 (232–805 cm⁻¹) — PS₄³⁻ · P₂S₇⁴⁻ · Li₂Sₓ S–S · Li–Si 상 · Si | 띠 귀속 참고표 |
| 7 | 모식: 충전하며 가운데 NMC 부터 탈리튬 · S–S 종 생성 (촉매전해질) · Li⁺ 는 SE 층으로 | 개념 그림 — 수치 없음 |
| S1 | DRT γ(τ) — 0.2 · 0.4 mA cm⁻², SoC 색 | 저/고전류 과정 분리 (정성) · 획득 조건 없음 |
| S2 | 충전 뒤 단층 — Si (SE · 집전체 쪽) · 양극 (⚠ 캡션과 패널 글자 (c)/(d) 뒤바뀜) | 비대칭 대비 (정성) |
| S3 | Raman 셀 C/50 충전 전압 (≈3050 min) | Raman 조건 (중성자 셀과 다른 전류 · 다른 셀) |
| S4 | 전압 + 내부 스택 압력 vs 사이클 (5 사이클) — 20–21.6 MPa 톱니 | ★ 운전 중 압력 ≈20–21.5 MPa 실측 · ⚠ 전압 범위 불일치 |
| S5 | FIB-SEM 단면 — 양극 *"~150 µm"* (50 µm 막대) | 두께 앵커 · NMC 입자 단면 (구형 ≈5–25 µm, 판독) |

## 6. Post-processing ★
- **무엇을**: 투과 영상 → 배경 · 빔 요동 보정 · 정합 → pristine 비 → (i) 색 지도 (ii) 가운데 영역 두께 방향 평균 선 단면 (iii) 반경 평균 시공간 지도 → Eq. S4 로 ΔC_Li (%) (Appendix A 의 C_Li 기준) → 등고선 · 3D 곡면.  단층 = ImageJ 영역 대비 (수치 없음).  Raman = 배경 제거 → 391 · 425 · 460 cm⁻¹ 세기 → 460/425 비 지도 → 세 영역 평균 (Fig. 6h).  DRT = γ(τ) (방법 미기재).
- **도구**: ImageJ (단층 대비) · 나머지 그림 도구 · 정합 · DRT 소프트웨어 [미확인].
- **안 한 것**: 흐림 (≈40 µm) 디컨볼루션 또는 균일 반응 + 흐림 대조 모의 · 반복 셀 · 오차막대 (중성자 단면) · 쿨롱 기준 ΔC_Li 검산 · 복합체 σ_ion/σ_e 측정 · 단층 대비의 수치화 결과 공개.
- **우리 후처리 (이 카드)**: 비용량 · 쿨롱효율 · C_Li · 투과 비 재계산 · Fig. 3 · 4 · 6 판독 · R_ion 어림 (§7-3) — 전부 §3 · §7 표에 식과 함께.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (우리 수치는 정본 브랜치 밖 `docs/` 출처를 병기)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 면용량 · 두께 | 형성 충전 **6.11 mAh cm⁻²** · 양극 **≈150 µm** (25 mg cm⁻²) | ps45 침대 **6 mAh cm⁻²** · 모델 두께 **≈111 µm** (300 MPa) (`docs/symmetric_cell_ionic_plan_20261013.md` §1) | 같은 "실용 후막" 급 · 두께 차 ≈35 % (조성 · 성형압 · 공극 다름) |
| 조성 | NMC811 : LPSCl : VGCF : PTFE = 80 : 16 : 3 : 1 (건식) | ps45 = NCM : LPSCl **81.6 : 18.4** · **탄소 · 바인더 없음** · Phase A / Lee 조성 침대 (MPM 복셀) = VGCF · PTFE 포함 | 같은 Ni-rich + LPSCl · 우리 ps45 는 전자 경로가 AM 접촉망뿐 |
| NMC 형상 · 입경 | **[미확인]** (LiNbO₃ 코팅 · FIB 구형 ≈5–25 µm 판독) | **PC 9 µm + SC 4 µm** (지름) 바이모달 5 조성 · LPSCl 1 µm | ⛔ PC:SC 비교 근거 없음 — 이 논문은 바이모달을 말하지 않는다 |
| 측정 / 모델 상태 | 운전 중 스택 **20–21.5 MPa** · 성형압 [미확인] | DEM = 300 MPa 압축 → 판 고정 이완 | 운전 압력 축은 우리 모델에 없다 |
| 복합체 σ_ion · σ_e | **미측정** | ps45 Hertz σ_ion **0.0587–0.0893 mS/cm** (σ₀ 1.5) · σ_e (Hertz · 기준 4.1 · PC 인자 끔) **0.375–0.467 mS/cm** (`docs/data/ps45_r45_network_g2_20261007/README.md`) | 그들 쪽 값은 Lee 2025 (거의 같은 조성) 로만 대리 가능 — §7-2 |
| 수송 tortuosity | **미측정** | ps45 Hertz **5.03–7.24** · 그 중 협착 전력 몫 **73–75 %** · 협착 뺀 같은 망 1.25–1.79 (같은 README 끝 절) | 그들의 "반응대" 를 정할 **망 성질**을 그들은 재지 않았다 |
| 반응 분포 (두께 · 시간) | **실측 (상대)** — Fig. 4 | DEM 망 = 유효값 한 개 · **두께 방향 분포 없음** · STEP4 (MPM 킷, BV 반응분포 · 갈바노 시간전개) 는 수치 패리티 런 대기 (CLAUDE.md STEP 파이프라인) | ★ 우리가 **아직 검증 못 한 축** (§7-5) |
| 촉매전해질 분해 위치 | Raman 가운데 최대 (오차막대 겹침) | 탄소–SE 면적 기반 분해 훅 (STEP3 carbon–SE 면적 + STEP5 SPLIT, CLAUDE.md 2026-07-23 #30) — 깊이 분포 없음 | 위치 대조 표적 하나 생김 (정성) |

### 7-2. ★ "이온 · 전자 균형" 설명 ↔ 같은 조성 문헌의 전도도 비 (판정 아님 — 정량 재료)
- 이 논문 조성 80 : 16 : 3 : 1 ↔ 정본 `lee2025_corolling_dryprocess_lpscl_ptfe` (Nat. Commun. 2025): CAM : SSE : VGCF = 80 : 17 : 3 + PTFE **0.5 wt%** → **σ_ion 0.069–0.076 · σ_e 33–34 mS/cm** · PTFE **2 wt%** → σ_ion 0.024 · σ_e 4.5 mS/cm (75 MPa, 그 카드 SI Fig 5 · Fig 4e/f).  PTFE 1 wt% 는 그 사이 → **σ_e/σ_ion ≈ 190–490** [우리 산술 · 교차 논문 — 이 논문의 셀 값이 아니다].
- 고전 다공전극 그림 (선형 동역학 · 정상 상태) 에서는 **σ_e ≫ σ_ion 이면 반응이 분리막 (SE) 쪽 면에**, σ_e ≪ σ_ion 이면 집전체 쪽 면에 몰리고, 비슷하면 **양 끝** 이 커진다 — **가운데 최대**는 그 그림만으로 나오지 않는다 [추정 — 교과서 그림, 이 논문 · 이 카드 밖 수치 없음].
  ⇒ (i) 1.0 mA cm⁻² 의 **SE 계면 결핍 띠** = σ_ion 제한 그림과 맞다.  (ii) 0.5 mA cm⁻² 의 **"집전체 쪽 시작"** 은 그 그림에서는 **전자 경로 제한**의 모양인데, 같은 조성 문헌의 σ_e/σ_ion ≈ 10²–10³ 와 어긋난다.  (iii) 저전류에서는 옴 강하가 작아 **국소 동역학 · OCV 기울기 · 미세구조 · 집전체 접촉** 같은 다른 항이 분포를 정할 수 있다 (저자 ref [23] Wang & Tang 의 *"thermodynamic origin"* 이 그 계열) [추정].
- ⇒ 이 논문의 *"ionic and electronic transport resistances are optimally balanced"* 는 **σ 측정 없이** 다른 논문의 모델 [26] 에 기댄 서술이다.  우리 쪽에서 가를 수 있는 질문: **같은 조성 침대에서 σ_e/σ_ion 와 두께 방향 반응 분포 (STEP4) 를 함께 내면, 저전류 가운데 최대가 나오는가?** (§8-1).

### 7-3. ★ 후막 이온 저항 어림 — 그들의 rate 손실 ↔ 우리 ps45
- 우리 ps45 (6 mAh cm⁻², 두께 ≈111 µm, Hertz σ_ion 0.0587–0.0893 mS/cm, σ₀ 1.5 보고 기준): **R_ion,양극 = L/σ = 124–189 Ω·cm²** → 1 mA cm⁻² 에서 두께 전체 옴 강하 **0.12–0.19 V** (반응이 두께에 고르게 퍼지면 그 1/3 쯤) [우리 산술 · 모델 값 = 탄소 없는 침대 · 자릿수 대조].
- 이 논문 양극에 Lee 2025 σ_ion (0.069–0.076) 을 대입하면 150 µm 에서 **197–217 Ω·cm²** → 1 mA cm⁻² 에서 ≈0.2 V [우리 산술 · 교차 논문 가정].
- 그들의 실측 (판독): 전류 반전 순간 전압 계단 ≈0.33 V (0.5 mA cm⁻², 전류 변화 1.0) · ≈0.45 V (1.0 mA cm⁻², 전류 변화 2.0) → 겉보기 ≈330 · ≈225 Ω·cm² (SE 층 · Si · 계면 포함 · 휴지 [미확인]) — **양극 이온 저항 어림과 같은 자릿수** [판독 + 우리 산술].
- 용량: 0.5 → 1.0 mA cm⁻² 에서 충전 ≈4.65 → ≈2.8 mAh cm⁻² (−40 %) · 방전 ≈4.6 → ≈2.05 (−55 %) [판독].  ⇒ **6 mAh 급 후막에서 C/5 만 돼도 이온 경로가 용량을 깎는다** — 우리 "후막 = 이온 수송 지배" 서사와 같은 방향 (정성).
- ⛔ 한정어: 조성 (탄소 · 바인더) · 두께 · 공극 · 온도 · 셀 구성이 다르다 · 판독값은 TREND 전용 · 겉보기 저항에 무엇이 들었는지 이 논문은 분해하지 않았다.

### 7-4. 6 mAh 후막 · PC:SC · 단결정/다결정 — 이 논문이 **못** 주는 것
- 바이모달 · PC:SC 비 · 입경 · 단결정 여부가 **전부 미기재** ⇒ 우리 ps45 의 PC:SC 경향 (σ_ion 0:10 → 7:3 1.52 배 · 수송 tortuosity 7.24 → 5.03) 이나 대칭셀 계획 (`docs/symmetric_cell_ionic_plan_20261013.md`) 에 **직접 쓸 숫자는 없다**.
- 간접 연결 [추정]: 우리 모델 기전 = *"작은 NCM 이 많을수록 활물질 표면이 넓어 SE 가 그 표면을 덮는 데 쓰이고 SE–SE 길이 끊긴다"* (같은 문서 §2) — 그들의 *"interfacial contact"* 를 포함한 내부 반응대 설명과 같은 어휘권이지만, 그들은 표면적 · SE 덮임을 재지 않았다.
- 이종기술 논지 (`docs/hetero_thesis.md` — 건식 후막 바이모달에서 SE 선코팅 → 분산 → 3D 이온 경로) 의 P3 (*"혼합 상태 차이가 압축 뒤 SE 경로 차이로"*) 를 **두께 방향 이용률**로 읽는 실험 방법 (operando 중성자) 의 선례로만 쓸 수 있다 — 논지 근거는 아니다 [추정].

### 7-5. frame[5] — 어느 반쪽을 가졌나 · 우리 검증 표적
- **가진 것**: 수송의 **결과** (두께 · 시간 반응 분포, 상대) + 화학 결과 (분해 위치) — 실험.
- **없는 것**: 미세구조 · 접촉망 · σ_ion/σ_e/τ · 기계 — 우리 DEM (접촉망 수송) 과 MPM (형상 · 공극) 이 둘 다 다루는 입력 쪽 전부.
- **우리 검증 표적 (정성 · 상대)**: ① 0.5 vs 1.0 mA cm⁻² 에서 반응대가 가운데 → SE 계면으로 옮겨 가는가 ② 충전 시작 위치 (집전체 쪽) ③ 방전 마지막 재리튬화 위치 (SE 쪽 30–40 µm).  ⛔ 절대 ΔC_Li (상대 지표 · §10-4) 와 위치의 µm 값 (흐림 40 µm) 은 표적으로 쓰지 않는다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **STEP4 깊이 프로파일 대조 실험 설계** — 같은 조성 (80 : 16 : 3 : 1 급) 침대에서 STEP4 갈바노 (0.5 · 1.0 mA cm⁻² 상당 C-rate) 로 두께 방향 SoC(z, t) 를 내고 Fig. 4 의 **정성 모양** (시작 위치 · 최대 위치 · 전류 의존 이동) 과 대조.  예측 [추정]: 우리 모델은 σ_e ≫ σ_ion 이라 **SE 쪽 시작**이 나올 가능성이 크다 → 저전류 "집전체 쪽 시작" 이 재현되지 않으면 그 차이가 **벌크 유효 전도도만으로는 안 되는 항** (OCV · 동역학 · 접촉) 의 크기 = frame[4] 의 정보.
2. **후막 이온 수송 서사의 실험 증거 한 줄** — "6 mAh cm⁻² · ≈150 µm 양극에서 전류 2 배 (≈C/10 → C/5) 에 용량 ≈40 % 감소 + SE 계면 쪽 반응 집중" (판독 · 정성).  우리 R_ion 어림 124–189 Ω·cm² (ps45) 와 같은 자릿수.
3. **대칭셀 · 전셀 실험 협업 시 기록 항목** — 이 논문이 빠뜨린 것 (복합체 σ_ion/σ_e · 공극률 · 성형압 · NMC 형상/입경 · 반복) 을 우리 실험 계획 (`docs/symmetric_cell_ionic_plan_20261013.md` §4) 은 이미 요구한다 — 그 목록이 맞다는 반례 사례.
4. **분해 위치 ↔ 반응 위치** — 우리 SE 분해 훅 (탄소–SE 면적) 은 위치가 없다.  깊이별 반응 분포 (STEP4) × 탄소–SE 면적 국소값을 곱하면 "어디서 분해가 많을까" 를 낼 수 있다 [추정 — 미구현].
5. **운전 압력 20–21.5 MPa** — 우리 모델의 성형 300 MPa 와 다른 축.  운전 압력에서의 접촉 상태 (이완 뒤 접촉 손실) 는 우리 DEM 제하 팔 부재 (F-SB1) 와 같은 빈칸.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Operando neutron radiography of a practical-loading Si|LPSCl|NMC811 full cell (6.11 mAh cm⁻² first charge, ≈150 µm cathode) shows that at 0.5 mA cm⁻² the largest Li change occurs in an interior band about 37.5–75 µm from the LPSCl interface, while at 1.0 mA cm⁻² a Li-depleted region forms at the NMC811|LPSCl interface (Kim et al., *Mater. Today* 2026)."
- "Cross-sectional operando Raman mapping in the same work reports the highest 460/425 cm⁻¹ (S–S/PS₄³⁻) intensity ratio in the cathode center (47 % at 100 % SoC vs 41 % near the electrolyte and 34 % near the current collector), although the error bars of the three regions overlap."
- 국문: *"실용 후막 (≈150 µm) NMC811–LPSCl 양극에서 저전류 반응은 양극 가운데에 몰리고, 전류를 두 배로 올리면 분리막 계면 쪽으로 옮겨 간다 (operando 중성자, 상대 Li 지표 · 흐림 ≈40 µm · 복합체 전도도 미측정)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **기전 주장의 근거가 이 논문 밖**: "이온 · 전자 저항 균형" 은 σ_ion · σ_e · τ 측정 없이 자기 그룹 모델 [26] (*"parameter-free"*, 이 논문에 결과 없음) 에 기댄다.  같은 조성 문헌 (Lee 2025) 의 σ_e/σ_ion ≈ 10²–10³ 와 함께 보면 "균형" 은 벌크 유효 전도도의 균형일 수 없다 (§7-2) [추정].
2. **해상도 ↔ 양극 두께**: 유효 화소 7.75 µm · 명목 25 µm · **기하 흐림 ≈40 µm** 인데 양극은 ≈150 µm (흐림 길이의 ≈3.75 배).  양쪽 경계 (집전체 · SE) 에서 신호가 깎이면 **고르게 반응하는 층도 "가운데가 가장 크게 변한" 모양**으로 보일 수 있다 — 저자는 *"fine boundary profiles inherently include convolution effects"* 라고만 쓰고 균일 반응 + 흐림 대조나 디컨볼루션을 보이지 않았다 [우리 해석].  ⇒ "가운데 최대" 자체보다 **비대칭** (충전 시작 = 집전체 쪽 · 방전 마지막 = SE 쪽 30–40 µm · 고전류 SE 계면 결핍) 이 더 믿을 만한 정보다.
3. **로딩 불일치**: 본문 25 mg cm⁻² ↔ SI 계산 30 mg cm⁻² · 기준 (복합체 / NMC) 미기재 → 비용량이 145.7–305.5 mAh g⁻¹ 로 갈린다 (§3-2).  NMC 질량 기준 25 면 244 mAh g⁻¹ (같은 논문 저전류 0.05 mA cm⁻² 단층 셀 218 보다 큼).
4. **ΔC_Li 의 절대값**: SI 스스로 상대 지표라 한다.  σ_Li 한 값 (71 barn) 을 다색 빔 (0.8–6 Å, 피크 2.6 Å) 에 쓴 것은 흡수 단면적의 파장 의존을 무시한 근사 [추정].  충전 끝 지도 평균 ≈−45 % (판독, 거칠게) ↔ 쿨롱 기준 74 % (SI 30 mg) / 89 % (본문 25 mg) — 지도가 작다 (충전 전하에 촉매전해질 산화 같은 기생 전하가 섞였을 수도 있어 분리 불가) [판독 + 우리 산술].
5. **Fig. 4 의 출처 사이클**: 방전 시간축 0–8 h 가 Fig. 2a (≈9.2 h) · Fig. 3a (≈9.2 h) 어느 것과도 안 맞는다 — 어느 셀 · 어느 사이클인지 미기재.
6. **위치 문장 셋의 기준면**: 초록 *"37.5–75 µm from the LPSCl interface"* (지속 반응대) ↔ p.6 *"37.5–75 μm from the current collector"* (시작) ↔ p.3 *"about 50 um from that interface"* — **같은 숫자 범위가 다른 기준면 · 다른 대상**에 쓰였다.  또 p.3 *"delithiation appears to initiate earlier within the cathode interior"* ↔ p.4 *"the earliest measurable delithiation appears near the current-collector side"* — 표현이 어긋난다.  인용 시 기준면을 병기.
7. **Raman**: 다른 셀 · 다른 전류 (C/50) · 단면 시료 · 오차막대가 세 영역에서 겹침 · 오차막대 정의 미기재 · 집전체 쪽 75 % 값 인쇄 누락 · 지도 두께축 ≈195 µm ↔ 중성자 양극 150 µm — "같은 가운데 영역" 의 동일성은 정성.
8. **Fig. S2 캡션 (c)/(d) 뒤바뀜** · **Fig. S4 전압 범위 (≈1.7–3.7 V) ↔ 본문 2.6–4.3 V** · SI 의 *"Mo"* (Mn) · *"mol/m²"* (mol/m³) 오기 · 유효 화소 7.75 ↔ 3.76/0.5 = 7.52 µm.
9. **DRT 조건 미보고** — Methods 의 해당 문장이 지시문 형태로 남았다 (§3-6).  고전류 DRT 의 "SoC 의존을 가린다" 도 판독상 "줄어든다" 수준.
10. **반복 없음** — 조건마다 셀 1 개로 읽힘 · 중성자 단면에 오차막대 없음 · 단층 대비 정량 (ImageJ) 수치 미공개.
11. **고전류 방전 곡선이 2.6 V 전에 끝남** (Fig. 3e, ≈2.85 V · ≈4.85 h, 판독) — 하한 도달 여부 [미확인].
12. **전이 한계 (우리 쪽)**: NMC 형상 · 입경 · 공극 · 성형압 미상 · Si 전셀 (N/P 1.1, 첫 사이클 Li 소모 큼) · 운전 20 MPa — 우리 300 MPa 침대 · 반쪽 (Li) 가정과 다르다 · 반응 분포는 상대값.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 3 | M. Zhang, et al., Coupling of multiscale imaging analysis and computational modeling for understanding thick cathode degradation mechanisms, Joule 7 (2023) 201–220 | 정본 카드 있음 (`zhang2023_pfib_multiscale_imaging_4d_thick_cathode`) — 후막 NMC811 4D 모델 |
| 18 | Li, Z. et al. Synchrotron operando depth profiling studies of state-of-charge gradients in thick Li(Ni0.8Mn0.1Co0.1)O2 cathode films. Chemistry of Materials 32, 6358-6364 (2020) | 170 µm NMC811 의 깊이별 SoC — 액체계 대조 |
| 19 | A.M. Stavola, et al., Lithiation gradients and tortuosity factors in thick NMC111-argyrodite solid-state cathodes, ACS Energy Lett. 8 (2023) 1273–1280 | ★ 아지로다이트 후막의 리튬화 기울기 **+ tortuosity factor** — 우리 수송 tortuosity 의 직접 실험 대조 후보 (미 digest) |
| 20 | T. Ji, et al., Operando neutron imaging-guided gradient design of Li-ion solid conductor for high-mass-loading cathodes, Nat. Commun. 16 (2025) 7667 | 같은 방법 · 단조 기울기 + graded 촉매전해질 — 이 논문의 대립 선행 (미 digest) |
| 21 | Y. Li, et al., Effects of catholyte aging on high-nickel NMC cathodes in sulfide all-solid-state batteries, Mater. Horiz. 12 (2025) 119–130 | 촉매전해질 열화 (같은 그룹) |
| 23 | F. Wang, M. Tang, Thermodynamic origin of reaction non-uniformity in battery porous electrodes and its mitigation, J. Electrochem. Soc. 167 (2020) 120543 | ★ 저전류 반응 분포를 OCV 열역학으로 — §7-2 (iii) 후보 기전 |
| 26 | A. Adam, et al., Operando neutron radiography validates a parameter-free transport–kinetics model for thick solid-state battery Cathodes, Mater. Horiz. (2026) | ★★ 이 논문 기전 주장의 실제 근거 (TWIF-Li) — 모델 입력 · σ 값 확인 필요 |
| 27 | N. Sharma, L.S.D. Vasconcelos, S. Hassan, K. Zhao, Asynchronous-to-synchronous transition of Li reactions in solid-solution cathodes, Nano Lett. 22 (2022) 5883–5890 | tortuosity 지배 반응 전이 |
| 28 | R. Bradbury, et al., Visualizing reaction fronts and transport limitations in solid-state Li–S batteries via operando neutron imaging, Adv. Energy Mater. 13 (2023) 2203426 | 이온 · 전자 유효 전도도 균형 → 반응 위치 (Li–S) |
| 29 | N.-Y. Park, et al., High-energy, long-life Ni-rich cathode materials with columnar structures for all-solid-state batteries, Nat. Energy 10 (2025) 479–489 | 탈리튬 표면 ↔ 황화물 산화 결합 |
| 9 | C. Kim, et al., Self-generated phosphate/oxysulfide passivation from dry-processed single-crystal NMC811 stabilizes argyrodite sulfide interfaces, Energy Storage Mater. 105009 (2026) | 같은 그룹 건식 **단결정** NMC811 — 이 논문 양극의 형상 확인용 |
| 15 | C. Xu, et al., Operando neutron imaging of lithium flux and gradient cathode design for enhanced kinetics in high-loading all-solid-state Li─S batteries, Adv. Mater. 38 (2026) e11553 | 중성자 Li 흐름 + graded 양극 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 10 쪽 · SI 8 쪽 전부 렌더 (100 dpi 전 쪽 · 그림 300 dpi) 로 정독 · `pdftotext` 로 인용문 대조 · DOI = 1 쪽 인쇄 · 서지 = PDF 메타 + 1 쪽.
- 그림 크롭 13 장 = 캡션 13 개 (본문 Fig. 1–7 · Table 1 · SI Fig. S1–S5) 와 번호 대조 · 그림은 임베드 래스터 1 장씩이라 clip = 래스터 bbox (여백 · 캡션 · 본문 없음) · Table 1 은 텍스트 표 (머리 ~ 아래 괘선) · `figures.json` 에 bbox (pt) · 원본 쪽 · 캡션 원문.
- Fig. 3a/e · Fig. 4a/b 는 확대 크롭으로 축 보정 판독 (Fig. 4: 시간 112.2 · 180.6 px/h, 거리 2.047 px/µm) · Fig. 6h 는 인쇄값 14 개로 축 격자 (10 %/칸) 를 확인한 뒤 누락 1 칸 판독.
- SI Appendix 식 (Eq. S1–S4) 은 렌더 이미지로 기호 대조 · 수치 (0.268 mg · 2.0572×10⁴) 재계산.
- 정본 litdb 전수 검색 (papers/ 파일 목록 + DOI · 제목 · 저자 · "neutron radiograph/imaging" grep): 같은 논문 카드 없음 · operando 중성자 영상 카드 없음 (이 카드가 처음).

## 🔗 관련 카드
- 후막 · 반응 불균일: `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` (ref [3]) · `wang2026_dryprocess_thick_cathode_failure_ncm94` · `zhang2026_dryprocess_electrode_architecture_cell_level` · `luan2025_graded_cathode_400whkg_pouch` · `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` · `minnmann2022_designing_cathodes_solidstate`.
- 같은 조성 전도도: `lee2025_corolling_dryprocess_lpscl_ptfe` (σ_ion · σ_e 실측) · `lee2025_dual_fibrous_ptfe_dry_electrode` · `ketter2025_resistor_network_models_predict_transport_properties` · `minnmann2021_jes_charge_transport_bottlenecks`.
- 우리 랩 · 바이모달: `kang2025_toughened_bimodal_nca_lzo` · `shi2019_high_am_loading_particle_size_assb`.
- 세미나 짝: `liu2024_sc_ni90_sulfur_coating_sulfide_assb`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
