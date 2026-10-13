<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md (이 논문이 ref 24 · S2 로 인용) · shi2019_high_am_loading_particle_size_assb.md (CUE 방법 원전).
     쪽 표기 = 본문 "p.N" (PDF N 쪽 = 학술지 103607 의 N 쪽) · SI "SI p.N" (SI PDF N 쪽 · 인쇄 쪽 번호와 같다).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 눈 판독 · 정밀도는 파일 머리) · [우리 산술] = 인쇄값으로
     우리가 다시 한 계산 · [추정] = 우리 해석 · [미확인] = 본문 12 쪽 + SI 31 쪽 전수에 없음.
     크롭 39 장 (Scheme 1 · 그림 1–5 · SI 그림 S1–S31 · SI 표 S1–S2) 전부 렌더로 열람 (SI 는 축소 모음 · 본문은 원 크기). -->

# 같은 총 SE (23 wt%) 에서 SE 를 얼마나 "입히느냐" 의 최적점 — 칼날 분쇄기 (blade mill) 건식 혼합 (MM) 으로 LNO-NCM811 에 LPSCl 을 일부만 입힌 NCM@10SE (껍질 ≈300–400 nm · 피복 < 100 %) + 3 µm 자유 SE = MM10 이 손 혼합 HM23 · 다 입힌 MM23 보다 σ_ion · 용량 · 수명이 좋다: σ_ion 5.81 / **6.53** / 2.69 ×10⁻⁵ S/cm · τ (= 우리 tau2) 9.65 / **8.62** / 20.8 · σ_e 6.2 / 4.13 / 3.34 mS/cm · 0.3 C 첫 용량 173 / **188** / 108 mAh/g — DEM (Hertz–Mindlin · E_LPSCl 22 GPa · 200 MPa) 으로 접촉 면적 · 이온 퍼콜레이션 이용률 (CUE) 을, FEA 로 SOC · 전류 · von Mises 응력을 같은 3D 구조 위에 — Yoon Jun Kim · Trung Dinh Hoang … Seoung-Ki Lee · Janghyuk Moon · Yoon-Cheol Ha · Byung Gon Kim (한국전기연구원 · 부산대 · 중앙대 · 경희대, Energy Storage Mater. 2024)

> slug `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` · DOI `10.1016/j.ensm.2024.103607` · type `exp + DEM + FEA (건식 MM SE 코팅 · 피복률 설계 계산 · 에탄올 용해 코팅량 · CP-SEM 두께 · PSA · EIS σ_ion · DC 분극 σ_e · DEM 접촉 면적 · A* 퍼콜레이션 CUE · FEA SOC/전류/응력 · In-Li · Li 금속 셀 · 건식 전극 · 파우치)` · PDF `9673bc77-28._Exploring_optimal_cathode_composite_design_for_high-performance_all-solid-state_batteries.pdf` · SI `3f432922-28._Sup_Exploring_optimal_cathode_composite_design_for_high-performance_all-solid-state_batteries.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Exploring optimal cathode composite design for high-performance all-solid-state batteries* (p.1)
> **저자 · 소속 (p.1 · SI p.1)**: Yoon Jun Kim¹ · Trung Dinh Hoang¹ (¹ 동등 기여) · Su Cheol Han · Joo An Bang · Ho Won Kang · Jaehyun Kim · Heetaek Park · Jun-Ho Park · Jun-Woo Park · Gumjae Park · You-Jin Lee · Doohun Kim · Seung-Wook Eom · Jeong-Hee Choi · **Seoung-Ki Lee\*** · **Janghyuk Moon\*** · **Yoon-Cheol Ha\*** · **Byung Gon Kim\*** — **한국전기연구원 (KERI) 전지연구본부, 창원** · 부산대 재료공학부 · 중앙대 에너지시스템공학부 (Hoang · Jaehyun Kim · Moon) · 경희대 응용화학과 (Bang · Kang · B. G. Kim) · UST (교신 ifriend@pusan.ac.kr · jhmoon84@cau.ac.kr · ycha@keri.re.kr · byunggonkim@khu.ac.kr)
> *Energy Storage Materials* **71** (2024) 103607 · 접수 2024-03-16 · 수정 2024-06-08 · 승인 2024-06-29 · 온라인 2024-07-01 (p.1) · 연구비 NRF (MSIT) RS-2024-00353531 · NRF-2021R1C1C1008383 · KERI Primary Research Program 24A01017 (NST) · Technology Innovation Program 20009957 (MOTIE) (p.11) · 이해상충 없음 · 데이터 = 요청 시 (p.11)
> **같은 축 카드 (링크만)**: [`kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact`](kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md) (ref 24 · S2 — 같은 τ 식 · 껍질 두께 산식의 원전) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (ref 29 · S1 — DEM 압축 · CUE 정의 원전) · [`yun2023_deciphering_degradation_halide_vs_sulfide`](yun2023_deciphering_degradation_halide_vs_sulfide.md) (S4 — 같은 FEA 계열 · 공저자 Hoang · Moon) · [`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`](kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md) (ref 46 — σ_ion 셀) · [`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`](asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity.md) (ref 47 — σ_e DC 분극) · [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) (ref 23) · [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (ref 37) · [`hippauf2019_dry_film_ptfe_sulfide_cathode_sheet`](hippauf2019_dry_film_ptfe_sulfide_cathode_sheet.md) (S9 — 건식 전극 제조법).
> **판독 원자료**: `litdb/figures/kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage/digitized.csv` (14 행 — Fig 3f · 5g 용량 · Fig 4f 응력 끝점 · 눈 판독) · 크롭 39 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 피복률 계산 (같은 SE 무게라도 껍질이 얇을수록 더 넓게 덮는다 · 375 nm 껍질이면 SE 8.76 wt% 로 다 덮인다) 에 따라 LNO-NCM811 (13.5 µm) 에 1 µm LPSCl 을 **10 wt%** 만 칼날 분쇄기 (4000 rpm · 60 s × 15 회) 로 입히면 실제 8.56 wt% 가 붙어 **NCM 표면이 100 % 는 덮이지 않고** (전자 경로 유지), 여기에 3 µm 자유 SE 를 더해 **총 SE 23 wt%** 로 맞춘 MM10 이, 같은 23 wt% 를 손으로 섞은 HM23 이나 SE 를 다 입힌 MM23 (두꺼운 껍질 · 남는 SE 덩어리 · 성긴 충전) 보다 σ_ion · 용량 · 수명이 좋다 — 즉 **같은 총 SE 에서 "입히는 몫" 에는 최적점이 있다** (p.2–6).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도) | 예비 혼합 = 음향 혼합기 (Resodyn PharmaRAM1) **10 min** → **칼날 분쇄기 KBM-L (KM tech) · 초퍼 4000 rpm · 60 s 가동 + 90 s 휴지 × 15 회** · 프레스 헤드–벽 좁은 틈 (전단 · 압축) · **40 g (≈50 mL)** · Ar 밀봉 · **15 °C** · host:guest = 95:5 · 90:10 · 77:23 / 비교 HM = 마노 막자 **40 min** · 에너지 · 선속도 [미확인] | [인쇄] p.10 |
| ② 피복 · 두께를 어떻게 쟀나 · 값 | **에탄올로 SE 를 녹여 무게 감소** → NCM@10SE 실제 **8.56 wt%** (나머지는 칼날 · 벽에 붙음) · MM15 실제 **13.29 wt%** · CP-SEM 두께 **≈300–400 nm (10 wt%) · ≈400–1200 nm 불균일 (23 wt%) · ≈200 nm (5 wt%)** (본문 단위는 "μm" 로 오기 — §10-1) · PSA 평균 지름 NCM 13.58 → MM@10SE 14.33 · MM@23SE 14.94 µm · 피복률은 계산 (Fig 1a) + XPS (Nb · Ni · Co 피크 잔존 = 100 % 아님) · SEM 의 드러난 면 (SI S5) | [인쇄] p.3–4 · SI S1 · S4 · S5 |
| ③ 코팅이 SE 를 얼마나 쓰나 | 10 wt% 넣어 8.56 wt% 붙음 (손실 ≈14 %) · [우리 산술] MM10 의 총 SE 23 g (100 g 양극당) 중 **껍질 몫 ≈7–8 g (30–36 %)** · 나머지 15–16 g 은 3 µm 자유 SE · MM23 은 SE ≈전부가 껍질 + 남는 덩어리 | [인쇄] p.3 · p.10 · [우리 산술] |
| ④ σ_ion · σ_e · 기공 · 용량 (총 SE 23 wt% · NCM:LPSCl:VGCF 75:23:2) | σ_ion **HM23 5.81 · MM10 6.53 · MM23 2.69 ×10⁻⁵ S/cm** · τ (식 = Φ_SE·σ_LPSCl/σ_eff = **우리 tau2**) **9.65 · 8.62 · 20.8** · σ_e (DC) **6.2 · 4.13 · 3.34 mS/cm** · 충전 밀도 2.682 · 2.693 · 2.676 g/cm³ · 입자 사이 기공 22.3 · 22.0 · 22.5 % · 0.3 C 첫 방전 **173 · 188 · 108 mAh/g** · 400 사이클 유지 26.8 · **86.3** · 30.6 % (MM10 1000 사이클 53.2 %) | [인쇄] p.4–6 · SI 표 S1 |
| ⑤ DEM · 모델 | ★ **DEM (Hertz–Mindlin · 코드 [미확인])**: NCM 13.5 µm (E 175 GPa) · LPSCl 3 µm (**E 22 GPa** · ν 0.3) · VGCF = 결합 입자 10 개 섬유 (BPM) · 중력 침강 · x·y 주기 · 상자가 **0.01 m/s** 로 내려와 **200 MPa** · 코팅 = NCM 표면에 묶인 (BPM) 작은 SE 입자 + 무작위로 뚫은 노출 반점 · 접촉 면적 = 구 캡 식 · **CUE = 위쪽 SE 에 A\* 경로로 이어진 NCM 부피 몫** · **FEA**: Fick + 전하 보존 + Butler–Volmer + 확산 변형 탄성 (SOC · 전해질 전류 · von Mises) | [인쇄] SI p.2–6 · Table S2 |
| ⑥ "같은 총 SE 에서 코팅 상태" 실험에 주는 것 | ★★ **가장 직접적인 선례** — 같은 총 SE 23 wt% 에서 "입힌 몫" 0 % (HM23) → ≈30–36 % (MM10) → ≈100 % (MM23) 을 비교했고 결과가 **단조가 아니다**: σ_ion 은 가운데가 최대 (+12 %) · 다 입히면 −54 % · σ_e 는 입힐수록 단조 감소 (−33 · −46 %).  ⇒ 우리 V1 (코팅 상태) 은 "있다 / 없다" 두 수준이 아니라 **입힌 몫의 축**으로 두고, 자유 SE 의 크기 (여기 3 µm) 도 같이 정해야 한다 [추정] | [인쇄] · [우리 산술] · §7-3 |
| ⑦ 이종기술 논지의 응집 | HM23 단면: *"agglomeration of SE particles in certain areas due to uneven distribution"* (Fig 2b) · MM23: *"Agglomerated residual SE"* (Fig 2a · SI S9 — *"when the amount of SE exceeds a certain ratio compared to the NCM, causing the more numerous guest SE particles to aggregate"*) — 정성 | [인쇄] p.4 · Fig 2 |

⛔ **한정어 (떼지 말 것)**: ① NCM = **LNO 코팅 다결정 NCM811 13.5 µm** (EcoPro BM · Wonik PNE) · 게스트 SE 1 µm (POSCO-JK) · 자유 SE 3 µm (출처 [미확인]) · VGCF 2 wt% ② 셀 시험 대부분 **55 °C** · In-Li 음극 · 0.3 C (실온 Li 금속 시험은 1 C 에서 용량이 ≈63 mAh/g 수준 [판독]) ③ σ_ion 의 τ 계산은 **문헌 σ_LPSCl 1.7 mS/cm** (ref S15) 를 썼다 — 같은 분말 측정값이 아니다 ④ DEM 은 **실제 E (22 GPa) 의 탄성 구** · 접촉 면적 상자는 **14 × 14 µm (NCM 하나 폭)** · FEA 는 SE 를 탄성으로 둔다 (소성 없음) ⑤ 셀 수 · 오차 막대 [미확인].

---

## 1. 한 줄 요약

손 혼합 (HM) 은 SE 가 고르게 퍼지지 않고, 용액 코팅은 극성 용매로 SE 가 상한다는 두 문제에서, **건식 기계 혼합 (MM)** 으로 SE 를 양극에 직접 입히되 **피복률이 100 % 를 넘지 않게** 설계하자는 논문.  먼저 껍질 두께 · SE 무게비 · 피복률의 관계를 계산하고 (Fig 1a · S30–S31), 10 wt% SE 로 ≈375 nm 껍질이 표면 대부분을 덮되 다 덮지 않게 만든 NCM@10SE 를 실측 (에탄올 용해 · SEM · XPS · PSA) 으로 확인했다 (Fig 1).  자유 SE (3 µm) 를 보태 총 SE 23 wt% 로 맞춘 세 양극 (HM23 · MM10 · MM23) 을 비교하니 MM10 이 치밀하고 SE 가 고르며 σ_ion 이 가장 높고 σ_e 는 적당히 남았다 (Fig 2).  DEM 구조 위 접촉 면적은 MM 코팅이 NCM–VGCF 접촉을 줄이고 NCM–SE 접촉을 늘림을 보였다 (Fig 2e–f).  셀은 MM10 이 용량 · 수명 · 율속 · 내부 압력 변화 · 실온 Li 금속 1000 사이클 (80.6 %) 모두에서 앞섰고 (Fig 3), FEA 는 MM10 의 전류 · SOC 가 고르고 과전압 · 응력이 작으며 NCM 이 많은 양극 (83 · 92 wt%) 에서도 이용률이 유지됨을 보였다 (Fig 4).  사이클 뒤 HM23 은 공극 확대 · 균열 · 박리가 생기고 MM10 은 유지 (Fig 5) · SE 15 wt% · 7 wt% · 고로딩 · 건식 전극 · 파우치에서도 MM 이 나았다 (Fig 5 · S26–S29).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (AM / SE / 도전재) | 연구유형 |
|---|---|---|---|---|
| Y. J. Kim¹ · T. D. Hoang¹ · … · S.-K. Lee\* · J. Moon\* · Y.-C. Ha\* · B. G. Kim\* (KERI · 부산대 · 중앙대 · 경희대 · UST) | *Energy Storage Mater.* 71 (2024) 103607 | 10.1016/j.ensm.2024.103607 | LNO 코팅 NCM811 13.5 µm / LPSCl 1 µm (게스트) + 3 µm (자유) / VGCF 2 wt% | 실험 + DEM + FEA |

- 키워드 (p.1): Mechanical mixing · Core-shell structure · Cathode composite · Solid state battery · Finite element analysis.
- ⚠ **소속 확인**: KERI = 한국**전기**연구원 — 한국전자기술연구원 (KETI) 이 아니다 (`lee2024_shear_force_dry_process_cathode_coverage` 카드의 "KETI 단서" 와 대조할 때).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 (p.9–10 · SI 표 S2)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| NCM | LiNi₀.₈Co₀.₁Mn₀.₁O₂ (EcoPro BM) **지름 13.5 µm** · LiNbO₃ 코팅 NCM (Wonik PNE 제공) · 다결정 (1 차 입자로 된 2 차 입자) · 수은 압입 겉보기 밀도 **3.945 g/cm³** (자체 측정) | [인쇄] p.3 · p.10 · SI 표 S2 |
| 게스트 SE | Li₆PS₅Cl **평균 1 µm** (POSCO-JK 고용체) | [인쇄] p.10 |
| 자유 (추가) SE | **3 µm** LPSCl (1 · 3 · 8 µm 비교에서 3 µm 가 1 µm 와 비슷한 용량 · 입계 저항 감소 고려 — SI S11) · 출처 [미확인] | [인쇄] p.4 · SI S11 |
| SE 막 (분리막) 용 | Li₂S · P₂S₅ · LiCl 화학량 볼밀 (Pulverisette 7) **600 rpm 10 h** — 열처리 언급 없음 [미확인] | [인쇄] p.10 |
| 도전재 | VGCF (Resonac) | [인쇄] p.10 |
| 기타 | Li 박 20 µm (Honjo) · SS 박 10 µm | [인쇄] p.9 |

### 3-2. ★ MM 공정 · 피복 설계 (p.2–4 · p.10 · Fig 1 · SI S1–S10 · S30–S31)

- **장치 · 조건** [인쇄 p.10]: 음향 혼합 10 min → **칼날 분쇄기 KBM-L** — 초퍼 **4000 rpm** 의 원심력으로 입자가 벽에 밀리며 프레스 헤드–벽 틈에서 전단 · 압축 · **60 s 가동 + 90 s 휴지 × 15** · 40 g (≈50 mL) · Ar 밀봉 · 15 °C 냉각 · 바인더 · 용매 없음.
- **피복률 계산** (Fig 1a · SI p.2–3 · S30–S31) [인쇄]: 껍질 무게비 = 껍질 부피 / ((4/3)πR³) × ρ_LPSCl/ρ_NCM (R = 6.75 µm) · 피복률 = 껍질 면적 / 4πR² · 몬테카를로로 계산 · SE 입자를 표면에 "고르게 (uniform)" 또는 "무작위 (random)" 로 놓는 두 방식 — 고르게 놓으면 피복률이 빨리 포화해 과대평가.
  - 375 nm 껍질은 **8.76 wt%** 로 다 덮임 · 800 nm 는 **≈19.7 wt%** 필요 · 200 nm 는 **4.51 %** 가 완전 피복 상한 [인쇄 p.3 · SI S31].
  - [우리 산술] 얇은 껍질 근사 3t/R · ρ_SE/ρ_NCM (1.87/3.945): 375 nm → 7.9 % · 800 nm → 16.9 % · 200 nm → 4.2 % (무게비 SE/NCM) — 인쇄값보다 조금 작다 (입자 껍질의 빈 틈 · 정확한 껍질 부피 차) · 같은 자릿수.
- **실측** [인쇄 p.3–4]:

| 시료 | 실제 SE 양 | 껍질 두께 (CP-SEM) | PSA 평균 지름 |
|---|---|---|---|
| bare NCM | — | — | 13.58 µm |
| NCM@5SE | — | **≈200 nm** (SI S10) | — |
| NCM@10SE (MM) | **8.56 wt%** (에탄올 용해 · SI S4) | **≈300–400 nm** (그림 표지 330 · 360 nm) | **14.33 µm** |
| NCM@15SE (MM) | **13.29 wt%** | 두꺼움 · 완전 피복 (SI S19) | — |
| NCM@23SE (MM) | [미확인] | **≈400–1200 nm 불균일** (그림 표지 400 · 630 nm · 1.17 µm) + 남는 SE 덩어리 | **14.94 µm** |
| HM-NCM@10SE · @23SE | — | 고르지 않음 · 거의 안 덮인 입자 · 남는 SE (SI S6 · S12) | 13.96 · 14.18 µm |

- [우리 산술] PSA 지름 증가의 절반 = 껍질 두께: MM@10SE (14.33 − 13.58)/2 = **0.375 µm** · MM@23SE (14.94 − 13.58)/2 = **0.68 µm** — Fig 1a 의 375 · 680 nm 선이 바로 이 값 (SI S1 *"The data for this trend line was derived from the PSA data in Fig. 1h"*).
- 피복 < 100 % 의 증거: XPS 에서 SE 10 wt% 일 때 Nb (LNO) · Co · Ni 피크가 남고 23 wt% 에서 사라짐 (Fig 1f · SI S8) · SEM/EDS 의 드러난 면 (SI S5) [인쇄 p.3–4].
- XRD · XPS S 2p: 새 상 · 부반응 피크 없음 [인쇄 p.4 · SI S7].
- MM 이 NCM 을 깨지 않음: NCM@5SE 단면에 균열 없음 (SI S10 주석) [인쇄].

### 3-3. ★ 세 양극 (총 SE 23 wt% · NCM:LPSCl:VGCF = 75:23:2) 의 구조 · 전도도 (Fig 2 · SI 표 S1 · S13–S16)

**SI 표 S1** [인쇄 SI p.26]:

| 항목 | HM23 | MM10 | MM23 |
|---|---|---|---|
| 접촉 면적비 VGCF/NCM (%, DEM) | 0.012 | 0.0017 | 0 |
| 접촉 면적비 SE/NCM (%, DEM) | 9.09 | 97 | 100 |
| σ_e (mS/cm, DC 분극) | **6.2** | **4.13** | **3.34** |
| 전자 저항 (Ω) | 9.8 | 14.6 | 18.1 |
| σ_ion (S/cm, EIS) | **5.81 × 10⁻⁵** | **6.53 × 10⁻⁵** | **2.69 × 10⁻⁵** |
| 부피분율 NCM · SE · VGCF · 입자 사이 기공 · NCM 내부 기공 (%) | 33.00 · 32.99 · 2.68 · 22.34 · 8.99 | 33.14 · 33.13 · 2.69 · 22.01 · 9.03 | 32.93 · 32.92 · 2.68 · 22.5 · 8.97 |
| "Ionic tortuosity" τ = (σ_LPSCl/σ_eff) × Φ_SE | **9.65** | **8.62** | **20.8** |
| 충전 밀도 (g/cm³) | 2.682 | 2.693 | 2.676 |

- [우리 산술] τ 재현: 1.7 × 0.3299 / 0.0581 = **9.65** · 1.7 × 0.3313 / 0.0653 = **8.62** · 1.7 × 0.3292 / 0.0269 = **20.8** (σ_LPSCl = 1.7 mS/cm = 표 S2 의 문헌값) — **식은 우리 수송 tortuosity (tau2 = φ_SE · σ₀ / σ_eff) 와 같다** (이름만 τ — §10-3).
- [우리 산술] f = σ_eff / 1.7: HM23 0.034 · MM10 0.038 · MM23 0.016.
- [우리 산술] 상대 변화: σ_ion MM10 **+12 %** · MM23 **−54 %** (HM23 대비) · σ_e MM10 **−33 %** · MM23 **−46 %**.
- 충전 밀도 측정 (SI S13): 0.1 g · 0.785 cm² · 두께 475 · 473 · 476 µm (마이크로미터) [인쇄].
- 구조 (Fig 2a–b · S14 · S16): HM23 = 공극 · SE 덩어리 · 덜 덮인 NCM · MM10 = 치밀 · SE 고르게 · 자유 SE 가 빈 곳 채움 · MM23 = 두꺼운 껍질로 커진 입자 사이를 채울 자유 SE 가 적어 공극 · **고립된 NCM** · 남는 SE 덩어리 [인쇄 p.4].
- 껍질이 있어도 연성 SE 가 냉간 압축에서 옆으로 퍼져 NCM 끼리 닿는다 (SI S15 — NCM@5SE) [인쇄 p.4].
- σ_ion 셀 (p.10): Li \| SE \| 양극 \| SE \| Li · SE 100 mg + 양극 100 mg 를 ⌀10 mm 몰드에서 **2 t · 1 min** → Li 20 µm · 지그 토크 5 N·m · R_electrode = R − 2L_SE/(σ_SE·A) [인쇄].  [우리 산술] 2 t / 0.785 cm² ≈ **250 MPa**.
- σ_e 셀: SS \| 양극 100 mg \| SS · 2 t · 1 min · DC **1 V** [인쇄 p.10].

### 3-4. ★ DEM · CUE · FEA (Fig 2e–f · 4 · SI p.2–6 · S18 · S22–S23 · S25 · 표 S2)

- **DEM** [인쇄 SI p.2]: 입자를 영역 안에 만들어 중력으로 쌓음 · x·y 주기 경계 · **Hertz–Mindlin** · VGCF = **결합 입자 모델 (BPM)** 로 구 10 개를 이은 휘는 섬유 (반지름 150 nm · 접촉 반지름은 그 2 배로 섬유 끊김 방지) · 압축 = 상자가 **0.01 m/s** 로 내려와 **200 MPa** 에서 멈춤 · 접촉 면적용 영역 **14 × 14 × 58 µm** · CUE 용 **35 × 35 × 120 µm** (VGCF 제외) · 시간 간격 = 레일리 시간의 5 % · 코드 이름 [미확인].
- **물성 (표 S2)** [인쇄]: NCM811 E **175 GPa** · ν 0.3 · ρ 3.945 g/cm³ · D 13.5 µm · LPSCl E **22 GPa** · ν 0.3 · ρ 1.87 · D 3 µm · σ_e (이온) **1.7 × 10⁻³ S/cm** · VGCF E 760 GPa · ν 0.3 · ρ 2 · L 3 µm · D 0.3 µm · 도전재 σ 1 × 10² S/cm · c_max 50060 mol/m³ · D_s 5.5 × 10⁻¹⁴ m²/s · i₀,ref 0.05 A/m² · α 0.5/0.5 · Ω 1.6 × 10⁻⁶ m³/mol.
- **코팅 표현**: NCM 표면에 게스트 SE 입자를 무작위로 놓고 BPM 으로 묶음 · 표면에 무작위 점을 찍어 그 근처 SE 를 지워 **노출 반점** 을 만들고, 점 수 · 거리를 정해진 코팅 무게비가 될 때까지 조정 · 무작위 배치는 껍질 입자 반지름 = 두께/2 [인쇄 SI p.2–3 · S30].
- **접촉 면적**: 겹친 두 구의 구 캡 면적 A = 2πR(R − (d² − r² + R²)/(2d)) · NCM 면적으로 정규화 (Fig 2f · 표 S1) [인쇄 SI p.3].
- **CUE** θ = V_NCM,active / V_NCM · 위쪽 LPSCl 과 적어도 한 전도 경로로 이어지면 활성 · **A\* 알고리즘**으로 최단 경로 [인쇄 SI p.5]:

| NCM wt% | 75 | 83 | 92 |
|---|---|---|---|
| HM | 100 % | **96.67 %** | **26.67 %** |
| MM (NCM@10 · 10 · 5 SE) | 100 % | **100 %** | **93.33 %** |

- **FEA** [인쇄 SI p.3–6]: 활물질 Fick 확산 · SE 전하 보존 ∇·i_e = 0 · Butler–Volmer · 반쪽 셀 (Li 금속 평면) · **1 C · 초기 SOC 0.1 · 3 V 컷** · 확산 변형 ε_ch = Ω(c − c₀)/3 · 훅 법칙 · 롤러 경계 (x · y = 0 · 16 µm) · 코드 [미확인].
  - 과전압 (Fig 4b · S18b): **HM23 −0.321 V · MM10 −0.207 · MM23 −0.213** (MM5 −0.22 · MM15 −0.21) [인쇄 그림 안].
  - von Mises 끝점 (Fig 4f) [판독 · ±40 MPa]: NCM 안 HM23 ≈1180 · MM10 ≈450 · MM23 ≈150 MPa / SE 안 HM23 ≈640 · MM10 ≈455 · MM23 ≈650 MPa.
  - 해석: MM10 은 SE 망이 "코팅층끼리 · 코팅층–SE · SE–SE" 로 이어져 Li 농도 · 전류가 고르고, HM23 은 표면 국부 농도 · 응력 집중, MM23 은 공극 때문에 두께 방향 농도 차가 크다 [인쇄 p.8].

### 3-5. ★ 셀 성능 (Fig 3 · 5 · SI S17–S29)

- 셀 (p.10): ⌀14 mm PEEK 몰드 · SE 173 mg **0.5 t · 1 min** → 양극 20.5 / 47.2 mg (**10 / 23 mg_NCM/cm²**) **4 t · 3 min** → In-Li 음극 · 55 °C · 2.38–3.68 V vs Li/Li⁺ · 0.1 C 전처리 1 회 · 1 C = 200 mA/g · EIS 10 mHz–7 MHz (25 °C) [인쇄].  [우리 산술] 0.5 t → ≈32 MPa · 4 t → ≈255 MPa.
- 0.3 C · 10 mg/cm² · 55 °C (Fig 3a): 첫 방전 **HM23 173 · MM10 188 · MM23 108 mAh/g** · 400 사이클 유지 **26.8 · 86.3 · 30.6 %** · MM10 1000 사이클 **53.2 %** [인쇄 p.6].
- 율속 0.1 → 4 C (Fig 3e): 4 C 에서 **HM23 17 · MM23 ≈0 · MM10 35 mAh/g** (0.1 C 대비 20 %) · MM23 은 2 C 에서 ≈0 [인쇄 p.7].
- 실온 (23 °C) Li 금속 (흑연 보호 Li · LPSCl/LGPS/LPSCl 삼중 SE) 1 C · 5 mg/cm² (Fig 3f · g): HM23 은 55 사이클 뒤 급감 · MM10 **1000 사이클 80.6 %** [인쇄] — 단 용량 수준 **≈63 → ≈51 mAh/g** [판독 ±3].
- 내부 압력 (Fig 3c–d): MM10 의 셀 압력 변화가 HM23 보다 크다 — In-Li 부피 변화 = 더 많은 Li 이동 = 높은 CUE 해석 [인쇄 p.7].
- 총 SE 15 wt% (NCM 83 wt%): σ_ion HM15 **2.32** · MM10 **2.95 × 10⁻⁵ S/cm** (SI S24 그림 안) · HM15 는 250 사이클 뒤 급감 · MM10 1000 사이클 유지 · 23 mg/cm² (≈4 mAh/cm²) 에서 **800 사이클 93.3 %** [인쇄 p.8 · Fig 5e–f].
- 총 SE 7 wt% (NCM 92 wt% · 92:7:1 · NCM@5SE): σ_ion **2.86 × 10⁻⁵ S/cm** · MM5 110 사이클 안정 (≈150 mAh/g [판독]) · HM7 ≈72 → ≈45 mAh/g [판독] [인쇄 p.8 · Fig 5g].
- 같은 총 SE 23 % 에서 MM5 · MM10 · MM15 비교 (분산기 · 45 °C, SI S19): MM10 이 가장 좋음 — MM5 는 분산이 덜 되고 MM15 는 두꺼운 완전 피복 [인쇄 p.6].
- 손 혼합 대신 분산기 (Thinky ARE-310) · 혼련기 (KM tech NEP-0.5K) 로 만들어도 같은 경향 (SI S20 · S26) · 건식 전극 (NCM:LPSCl:VGCF:PTFE 75:21.5:2:1.5 · 막자 10 min 박편 → 손 롤러 150 µm · Hippauf 2019 방식) · 파우치 (77:18.5:3:1.5 · SE 층 LPSCl:NBR 98:2 · Ag/C 음극 · 30 mg/cm² · 6 mAh/cm²) 에서도 MM 쪽이 낫다 [인쇄 SI S26–S27].
- 사후 (Fig 5 · S14): 500 사이클 뒤 HM23 · MM23 = 공극 확대 · 균열 · 양극–SE 층 박리 · 고립 입자 / MM10 = 처음과 비슷 [인쇄 p.8].

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
피복률 계산 (껍질 두께 × 무게비) → MM (NCM + 1 µm SE) → 에탄올 용해 (실제 코팅량) · SEM/EDS · XPS · CP-SEM · PSA → 자유 SE (3 µm) · VGCF 와 손 혼합해 총 SE 23 % 양극 → 충전 밀도 · σ_ion (EIS) · σ_e (DC) · τ → In-Li 셀 (55 °C) · Li 금속 셀 (23 °C) · 율속 · 내부 압력 · EIS 변화 · 사후 SEM / 병행 DEM (접촉 면적 · CUE) → FEA (SOC · 전류 · 응력).

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **실험**: SE 가 MM 의 전단 · 압축으로 NCM 위에 **소성 퍼짐 · 껍질** · 냉간 압축에서 껍질이 옆으로 퍼져 NCM 끼리 닿는다 (SI S15).
- **DEM (이 논문)**: 실제 E (LPSCl 22 GPa · NCM 175 GPa) 의 **탄성 구 (Hertz–Mindlin)** · 껍질 = 표면에 묶인 작은 구들 · 소성 · 형상 변화 없음 → frame [2] 가 말하는 "강체 / 탄성 구 + 실제 E 는 덜 치밀해진다" 쪽 (기공은 보고 안 함).
- **FEA (이 논문)**: 선형 탄성 (SE 소성 없음) — SE 안 von Mises 가 ≈0.45–0.65 GPa [판독] 로 LPSCl 항복 범위 (0.05–0.30 GPa, 우리 frame [1] 의 문헌 범위) 를 넘는다 → 실제라면 SE 는 항복했을 것 [추정].
- **우리 대응**: 우리 압축 DEM 은 SE 를 **연화 E (1.35 GPa)** 의 구로 두고 겹침 δ 로 소성 몫을 대신한다 (frame [2]) · 코팅 팔은 아직 "표면 성질 (점착)" 대리뿐 — 이 논문의 **BPM 껍질 + 무작위 노출 반점** 은 껍질을 입자로 표현하는 구체적 방법이다.

### 4-3. 기법 미니 용어집
- **MM (mechanical mixing)**: 여기서는 칼날 분쇄기 (초퍼) 의 원심력 · 헤드–벽 틈의 전단 · 압축으로 게스트를 호스트에 입히는 건식 공정.
- **피복률 (surface coverage)**: 껍질이 덮은 면적 / NCM 표면적 (계산값).
- **BPM (bonded particle model)**: DEM 입자들을 결합 (bond) 으로 묶어 섬유 · 껍질 같은 덩어리를 만드는 방법.
- **CUE (cathode utilization efficiency)**: 위쪽 SE 와 이온 경로로 이어진 활물질 부피 몫 (실험 쪽 정의는 사용한 Li 용량 / 이론 용량 — ref 53).
- **A\* 알고리즘**: 그래프 최단 경로 탐색.
- **ionic tortuosity (이 논문의 τ)**: Φ_SE · σ_LPSCl / σ_eff — **우리 수송 tortuosity (tau2) 와 같은 양** (제곱근 아님).

---

## 5. Figure set ★ (크롭 39 장 = `litdb/figures/kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| Scheme 1 | (a) HM vs MM 양극 (이온 · 전자 전도 표시) (b) MM 장치 사진 · 모식 | 개념도 |
| 1 | (a) 피복률 vs SE 무게비 (껍질 200–800 nm) (b–d) SEM/EDS (e) XRD (f) XPS (g) CP-SEM 껍질 두께 (h) PSA | ★ 피복 설계 도표 · 실측 |
| 2 | (a) 윗면 SEM/EDS (b) 단면 (c) σ_ion EIS (d) σ_e DC (e) DEM 3D 구조 (f) DEM 접촉 면적비 | ★ 같은 총 SE · 세 코팅 상태 |
| 3 | (a–b) 0.3 C 사이클 · 곡선 (c–d) 내부 압력 (e) 율속 (f–g) 실온 Li 금속 1000 사이클 | 성능 |
| 4 | (a) FEA SOC · 전해질 전류 (b) 과전압 · 피복률 (c) 활성 / 비활성 NCM (d) CUE vs NCM wt% (e–f) von Mises | ★ DEM → 퍼콜레이션 → FEA 의 문헌 그림 (우리 STEP3/4 와 같은 층) |
| 5 | (a–d) 500 사이클 뒤 SEM (e–g) SE 15 · 7 wt% 사이클 | 사후 · 고 NCM |
| S1 · S2 | 껍질 두께 vs 무게비 (PSA 유래) · 껍질 시각화 | 설계 |
| S3–S10 | NCM · LNO-NCM · 에탄올 세척 무게 · 드러난 면 · HM 시료 · XPS · 남는 SE 덩어리 · NCM@5SE | ★ 코팅량 · 피복 < 100 % 증거 |
| S11 | 자유 SE 1 · 3 · 8 µm | 자유 SE 크기 |
| S12–S16 | HM-NCM@23SE · 충전 밀도 사진 · MM23 SEM · 껍질 퍼짐 · 고립 NCM | 구조 |
| S17 | 사이클 중 Nyquist | — |
| S18 · S19 | MM5 · MM15 FEA · 사이클 | ★ 입힌 몫의 최적점 |
| S20–S21 | 분산기 시료 · 율속 곡선 | 공정 강건성 |
| S22 · S23 | DEM 구조 (NCM 75–92 wt%) · 충전 상태 응력 | DEM 그림 |
| S24 · S25 | SE 15 % σ_ion · FEA | — |
| S26 · S27 | 건식 전극 · 파우치 | 실용 |
| S28 · S29 | SE 7 % 단면 · 곡선 | — |
| S30 · S31 | 고르게 / 무작위 껍질 · 피복률 | ★ 껍질 DEM 표현법 |
| 표 S1 · S2 | 세 양극 성질 · 시뮬 물성 | ★ 원자료 |

## 6. Post-processing ★
- **무엇을**: 피복률 몬테카를로 · 에탄올 용해 무게 · CP-SEM 두께 (10 회 측정 표준오차) · PSA · 충전 밀도 (마이크로미터) · 부피분율 (수은 압입 겉보기 밀도) · EIS σ_ion · DC σ_e · τ · DEM 접촉 면적 (구 캡) · A\* CUE · FEA.
- **안 한 것**: τ 의 σ_bulk 를 같은 분말로 측정 · DEM 기공 보고 · DEM 코드 · FEA 코드 이름 · 셀 반복 통계 · 오차 막대 (두께 외) · 공정 에너지.
- **우리 후처리 (이 카드)**: τ · f · 상대 변화 재계산 · PSA → 껍질 두께 · 피복 무게비 근사 · 셀 압력 환산 · 껍질 몫 산술 · 눈 판독 14 행.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 `docs/data/ps45_r45_network_g2_20261007/README.md` · CLAUDE.md 의 ps45 · σ_e 앵커 줄을 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| DEM 접촉 · 강성 | Hertz–Mindlin · **E_LPSCl 22 GPa · E_NCM 175 GPa** (실제 탄성) · 200 MPa · 상자 0.01 m/s | LIGGGHTS hooke/hysteresis · **E_SE 1.35 GPa (연화 대리)** · 300 MPa · 판 속도 0.01 mm/s | ⛔ 같은 "DEM" 이지만 frame [2] 반대편 — 실제 E 의 탄성 구는 덜 겹치고 덜 치밀하다 (이 논문은 DEM 기공을 보고하지 않아 대조 불가) · 판 속도가 1000 배 빠르다 (준정적 여부 [미확인]) |
| 영역 크기 | 접촉 면적 14 × 14 × 58 µm (**NCM 13.5 µm 하나 폭**) · CUE 35 × 35 × 120 µm | RVE 수십–백 µm (침대마다) | 접촉 면적비 (0.012 % · 97 %) 는 NCM 몇 개짜리 기둥의 값 — 통계적 대표성 약함 [추정] |
| 코팅 표현 | BPM 으로 묶은 작은 SE 껍질 입자 + 무작위 노출 반점 (코팅 무게비 맞춤) | 이종기술 논지 대조 = 표면 성질 (점착) 만 바꾼 대리 · 껍질 부피 없음 | ★ 이 논문의 방법이 우리 "코팅 팔" 에 껍질 부피를 줄 수 있는 가장 가까운 처방 [추정] |
| 퍼콜레이션 | CUE = 위쪽 SE 와 A\* 경로로 이어진 NCM 부피 몫 | 접촉망 `ionic_active_pct` · `am_ionic_isolated_pct` (같은 규칙의 경로 기준 고립) | 같은 개념 — 숫자 대조는 조성 · 입경이 달라 안 함 |
| tau2 (같은 정의) | HM23 9.65 · MM10 8.62 · MM23 20.8 (Φ_SE ≈0.33 · SE 23 wt% · σ₀ = **문헌 1.7**) | ps45 Hertz 7.24–5.03 · Tabor 4.12–2.78 (φ_SE ≈0.29 · SE 18.4 wt%) | 우리 Hertz 보다 높다 — 반면 `kim2023_…` 은 2.2–2.4 (SE 19.4 wt% · σ₀ 1.40 측정) — **비슷한 SE 함량의 실험 τ² 가 연구실마다 2.2 → 9.7 (4 배)** 로 갈린다 · 우리 Hertz 는 그 사이 |
| σ_e (VGCF 포함) | VGCF 2 wt% · 6.2 · 4.13 · 3.34 mS/cm (DC 1 V) | SDCP 캠페인 σ_e 실험 앵커 SBE 4.47 · DBE 12.4 mS/cm (kgy DC 분극) | 같은 자릿수 — VGCF 함량 · 공정 · 측정이 달라 1:1 아님 |
| 기공 | 입자 사이 22.0–22.5 % + NCM 내부 9 % (계산) | ε_sphere 15.0–19.2 % (ps45 · 내부 기공 없음) | NCM 내부 기공 9 % 를 따로 세는 회계 — 우리 침대는 NCM 을 꽉 찬 구로 둔다 |
| FEA 역학 | 탄성 SE · NCM 확산 변형 → SE 안 σ_v ≈0.45–0.65 GPa [판독] | MPM: SE J2 소성 (σ_y 0.30 GPa · 연화 E) | 이 논문 SE 응력은 항복을 넘는 탄성 값 — 소성을 넣으면 줄었을 것 [추정] |

### 7-2. 이종기술 논지 (`docs/hetero_thesis.md` 비준 블록 2026-10-05) 와의 관계
- **P1 · P2 의 실험 쪽 정성 단서 둘**: HM23 단면의 SE 덩어리 (*"agglomeration of SE particles in certain areas"*) · MM10 의 고른 SE 분포 (Fig 2).  ⚠ 그러나 **MM23 에서는 입힌 쪽에서도 남는 SE 가 뭉친다** (*"Agglomerated residual SE"* · SI S9) — "코팅하면 응집이 사라진다" 는 **입히는 몫이 적당할 때만** 맞는다.  SE 가 호스트보다 너무 많으면 게스트끼리 뭉친다는 저자 해석은 논지 §2-3 (작은 SE 끼리의 응집) 과 같은 방향 [추정].
- **P3 (혼합 상태 → SE 경로)**: σ_ion · τ 가 입힌 몫에 따라 **비단조** (0 → ≈30–36 % → ≈100 % 에서 5.81 → 6.53 → 2.69 ×10⁻⁵) — 혼합 상태 · 충전 상태 · 공극이 함께 바뀐다 · 논지 사슬 (응집 ↓ → 경로 ↑) 의 "중간 고리" 만으로는 MM23 의 하락을 설명 못 한다 (충전 · 공극 · 고립 NCM 몫).
- **"하지 않는 말"** (계면 면적 · 보호막): 이 논문의 설명에 SE/NCM 접촉 면적 (9 → 97 %) · LNO 보호막이 들어간다 — 논지가 쓰지 않기로 한 축 · 이온 경로 (σ_ion · τ · CUE) 만 빌린다.

### 7-3. ★ "같은 총 SE 에서 코팅 상태" 실험 (`docs/mixer_paper_pipeline_draft_20261013.md` V1 · V2 · V3) 에 주는 것
1. **코팅 상태 = 입힌 몫의 연속 축** — 같은 총 SE 23 wt% 에서 입힌 몫 0 (HM) · ≈30–36 % (MM10) · ≈100 % (MM23) 의 결과가 비단조 (σ_ion 최대가 가운데).  V1 을 두 수준 (코팅 / 비코팅) 으로 두면 최적점을 놓친다 → **세 수준 이상** (예: 0 · 1/3 · 전부) 을 권한다 [추정].
2. **자유 SE 의 크기 · 몫을 같이 고정** — MM10 의 이득은 껍질 + **3 µm 자유 SE 가 빈 곳을 채운 것** 의 합 (저자 해석) · 자유 SE 크기 (1 · 3 · 8 µm, SI S11) 가 용량을 바꾼다 → 코팅 팔 · 비코팅 팔의 자유 SE 입경 분포를 맞춘다.
3. **σ_e 는 입힐수록 단조 감소** (−33 · −46 %) — 도전재가 있어도 · 우리 SDCP σ_e 축과 같은 측정 (DC 분극) 으로 함께 잰다.
4. **실제 코팅량 측정법** — 에탄올 용해 무게 (8.56 vs 10 wt%) · PSA 지름 증가 / 2 = 껍질 두께 — 값싸고 정량적인 방법 두 개.
5. **우리 계산 쪽 할 일** — 압축 DEM 에서 "입힌 몫" 을 (가) 표면 성질 대리 (지금) 와 (나) 이 논문식 BPM 껍질 두 방식으로 두 수준 이상 만들어 tau2 · 이온 활성 몫의 비단조가 나오는지 보는 것이 이 논문과 맞대는 가장 직접적인 시험 [추정 · 제안].

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실험 사슬 + DEM (탄성 · 접촉 면적 · 퍼콜레이션) + FEA (전기화학 · 탄성 응력) — 우리 DEM → STEP3 → STEP4 와 같은 층의 문헌 그림 (`comparison_vs_ours_DEM.md` 가 위시리스트로 표시했던 그림).
- **없는 것**: SE 소성 (MPM 몫) · 실제 E 탄성 DEM 의 치밀화 검증 (기공 대조 없음) · 협착 저항 (Holm) 기반 σ — FEA 의 전해질은 연속체 σ (CONTACT_FREE 쪽, `CL-81`).

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 같은 총 SE 에서 "입힌 몫" 에 최적점이 있다.**
- 논문: HM23 → MM10 → MM23 = σ_ion 5.81 → **6.53** → 2.69 ×10⁻⁵ · 용량 173 → **188** → 108 · 400 사이클 유지 26.8 → **86.3** → 30.6 %.
- 뜻: 논지 P2 · P3 을 "코팅 = 좋다" 로 단순화하면 틀릴 수 있다 — 입힌 몫과 자유 SE 가 함께 정한다.
- 할 일: 파이프라인 V1 을 연속 축 (0 · 중간 · 전부) 으로 · 계산 (DEM) 과 실험을 같은 세 점에서.

**8-2. 실험 τ² 의 연구실 간 산포가 우리 모델 차이보다 크다.**
- 논문: τ² 8.62–20.8 (σ₀ 문헌 1.7) vs `kim2023_…` 2.21–4.28 (σ₀ 측정 1.40) — 비슷한 SE 함량.
- 뜻: 우리 Hertz (5.0–7.2) vs Tabor (2.8–4.1) 를 문헌 하나로 판정하면 연구실 선택이 답을 정한다.
- 할 일: 대칭 셀 계획에서 **같은 날 · 같은 분말** 의 σ₀ · 셀 기공 · σ_eff 를 함께 재 τ² 를 우리 망과 대조 (`docs/symmetric_cell_ionic_plan_20261013.md`).

**8-3. 껍질을 DEM 입자로 넣는 처방.**
- 논문: BPM 으로 묶은 작은 SE 입자 껍질 + 무작위 노출 반점 → 코팅 무게비 · 피복률을 맞춤 (SI S30–S31).
- 뜻: 우리 압축 DEM 의 코팅 팔에 껍질 부피를 주는 현실적 방법 · 단 껍질 입자 크기 (두께/2 ≈ 0.19 µm) 가 우리 SE 1 µm 보다 작아 입자 수 · 시간 간격 비용이 크다 [추정].

**8-4. 탄성 FEA 의 SE 응력은 항복 위.**
- 논문: SE 안 σ_v ≈0.45–0.65 GPa [판독] (탄성).
- 뜻: SE 소성이 있는 MPM (우리 frame [1]) 이 이 응력 분포를 다시 계산하면 크기가 크게 달라질 것 — "코팅이 SE 응력을 줄인다" 는 결론의 크기는 탄성 가정에 묶인다 [추정].

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "At a fixed total Li₆PS₅Cl content of 23 wt%, Kim et al. (*Energy Storage Mater.* 2024) found a non-monotonic optimum in the fraction of SE pre-coated on NCM811 by dry mechanical mixing: partial coating (NCM@10SE, ≈300–400 nm, coverage < 100 %) plus free SE gave the highest composite ionic conductivity (6.53 × 10⁻⁵ vs 5.81 × 10⁻⁵ S cm⁻¹ hand-mixed and 2.69 × 10⁻⁵ S cm⁻¹ fully coated), while electronic conductivity fell monotonically with coating (6.2 → 4.13 → 3.34 mS cm⁻¹)."
- 국문: *"같은 총 SE 에서 SE 를 활물질에 입히는 몫에는 최적점이 있다 — 일부만 입히고 자유 SE 로 빈 곳을 채운 경우가 이온 전도 · 수명이 가장 좋았다 (Kim 2024, ESM)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **두께 단위 오기**: 본문 *"when the SE coating thickness is 375 μm"* · *"approximately 300 to 400 μm"* · *"400 to 1200 μm"* · *"approximately 375 μm thick SE layer"* (p.3–4) — 그림 · SI 는 nm (375 nm · 330/360 nm · 1.17 µm) — 본문의 μm 는 nm 의 오기.
2. **τ² 의 σ_bulk 가 문헌값**: σ_LPSCl = 1.7 × 10⁻³ S/cm (ref S15 리뷰) — 같은 분말 (POSCO-JK 1 µm · 3 µm) 측정값이 아니다 → 절대 τ 는 σ_bulk 오차만큼 흔들린다.
3. **이름**: 표 S1 은 이 양을 *"Ionic tortuosity τ"* 라 부르지만 식은 Φ_SE · σ_bulk/σ_eff (= τ²) — 우리 규약으로는 **수송 tortuosity (tau2)** · 제곱근 τ 와 섞지 말 것.
4. **부피분율 표의 NCM ≈ SE**: 세 열 모두 NCM 과 SE 부피분율이 0.01 %p 차로 같다 (33.00 · 32.99 등).  [우리 산술] SE 33 % 는 23 wt% × 2.682 / 1.87 로 재현되지만, NCM 33 % 는 75 wt% × 2.682 / 0.33 = 고체 밀도 ≈6.1 g/cm³ 를 뜻해 NCM (≈4.7–4.8) 과 맞지 않는다 — 옮겨 적기 오류 가능성 [추정].
5. **DEM 영역**: 접촉 면적 계산 상자 14 × 14 µm 는 NCM (13.5 µm) 하나 폭 — 0.012 % · 97 % 같은 값은 입자 몇 개 기둥의 값.  DEM 코드 · 기공 · 겹침 [미확인].
6. **판 속도 0.01 m/s**: 우리 판 속도 (0.01 mm/s) 의 1000 배 · 준정적 확인 [미확인].
7. **탄성 FEA**: SE 를 탄성 (22 GPa) 으로 두어 σ_v 가 LPSCl 항복을 넘는다 — 응력 크기 결론은 가정에 묶인다.
8. **실온 1000 사이클의 용량 수준**: 80.6 % 는 ≈63 → ≈51 mAh/g [판독] 의 유지 — 초록의 *"improved capacity retention during 1000 cycles"* 만 읽으면 용량 수준이 안 보인다.
9. **55 °C · In-Li**: 저자도 *"differs somewhat from practical test conditions"* 라고 적음.
10. **비교 팔의 공정 차**: HM = 막자 40 min · MM = 칼날 분쇄기 + 손 혼합 — 공정 에너지가 다르다 (`frankenberg2025_…` 의 교락 축) · 분산기 · 혼련기 대조 (SI S20 · S26) 가 일부 보완.
11. **자유 SE 출처 · 셀 반복 · 오차 [미확인]**.
12. **Fig 1h 범례 철자**: *"MM@10SE"* (본문 NCM@10SE) · *"Redisual SE"*.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 19 | S.W. Park, H.J. Choi, Y. Yoo, H.-D. Lim, J.-W. Park, Y.-J. Lee, Y.-C. Ha, S.-M. Lee, B. G. Kim, Stable cycling of all-solid-state batteries with sacrificial cathode and lithium-free indium layer, Adv. Funct. Mater. 32 (2022) 2108203. | 카드 없음 — 같은 그룹 In 층 · 내부 압력 측정 |
| 24 · S2 | J. Kim, M.J. Kim, J. Kim, J.W. Lee, J. Park, S.E. Wang, S. Lee, Y.C. Kang, U. Paik, D.S. Jung, T. Song, … Adv. Funct. Mater. 33 (2023) 2211355. | 정본 카드 `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` |
| 29 · S1 | T. Shi, Q. Tu, Y. Tian, Y. Xiao, L.J. Miara, O. Kononova, G. Ceder, High active material loading in all-solid-state battery electrode via particle size optimization, Adv. Energy Mater. 10 (2020) 1902881. | 정본 카드 `shi2019_high_am_loading_particle_size_assb` — DEM · CUE 원전 |
| 36 | L. Zheng, C. Wei, M.D.L. Garayt, J. MacInnis, M.N. Obrovac, Spherically smooth cathode particles by mechanofusion processing, J. Electrochem. Soc. 166 (2019) A2924. | 카드 없음 — 메카노퓨전 일반 |
| 46 | N. Kaiser, S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato, B. Roling, Ion transport limitations in all-solid-state lithium battery electrodes containing a sulfide-based electrolyte, J. Power Sources 396 (2018) 175–181. | 정본 카드 `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` |
| 47 | T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, M. Tatsumisago, Electronic and ionic conductivities of LiNi1/3Mn1/3Co1/3O2-Li3PS4 positive composite electrodes for all-solid-state lithium batteries, J. Electrochem. Soc. 164 (2017) A3960. | 정본 카드 `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` |
| 53 | X. Guo, L. Hao, Y. Yang, Y. Wang, Y. Lu, H. Yu, High cathode utilization efficiency through interface engineering in all-solid-state lithium-metal batteries, J. Mater. Chem. A 7 (2019) 25915–25924. | 카드 없음 — CUE 실험 정의 |
| S4 | J. Yun, H.R. Shin, T.D. Hoang, S. Kim, J.H. Choi, B. Kim, H. Jung, J. Moon, J.-W. Lee, Deciphering the critical degradation factors of solid composite electrodes with halide electrolytes: Interfacial reaction versus ionic transport, Energy Storage Mater. 59 (2023) 102787. | 정본 카드 `yun2023_deciphering_degradation_halide_vs_sulfide` — 같은 FEA 계열 |
| S8 | A. Bielefeld, D.A. Weber, R. Rueß, V. Glavas, J. Janek, Influence of Lithium Ion Kinetics, Particle Morphology and Voids on the Electrochemical Performance of Composite Cathodes for All-Solid-State Batteries, J. Electrochem. Soc. 169 (2022) 020539. | 카드 없음 (같은 1저자의 2019 · 2020 카드는 있음) — i₀,ref 0.05 A/m² 출처 |
| S11 | S.-Y. Park, J. Jeong, H.-C. Shin, Geometrical Effect of Active Material on Electrode Tortuosity in All-Solid-State Lithium Battery, Appl. Sci. 12 (2022) 12692. | 카드 없음 — τ 식 출처 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 12 쪽 · SI 31 쪽 텍스트 층 전수 · 저자 · 소속 · 날짜 · DOI = p.1 · 연구비 = p.11 · 공정 · 셀 · 측정 = p.9–10 · 표 S1 · S2 = 텍스트 층 + 크롭 영상 대조.
- 그림 · 표 39 장: Scheme 1 + 그림 5 (래스터 원본 300 dpi) · SI 그림 31 (원본 200–220 dpi · 업샘플 없음) · SI 표 2 (벡터 300 dpi) — 본문 그림은 원 크기, SI 는 축소 모음으로 열어 축 · 범례 · 패널 표지 확인.
- 재계산: τ (표 S1) 세 값 · PSA → 껍질 두께 (375 · 680 nm) · 셀 압력 · 피복 무게비 근사 — 인쇄값과 맞거나 같은 자릿수.
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI · 제목 낱말 grep — 이 논문 카드 없음 (`comparison_vs_ours_DEM.md` 에 위시리스트 언급만).

## 🔗 관련 카드
- 같은 축 (건식 SE 코팅): `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` · `lee2026_lpscl_coating_thickness_ncm811` · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure`.
- DEM · 퍼콜레이션 · FEA: `shi2019_high_am_loading_particle_size_assb` · `yun2023_deciphering_degradation_halide_vs_sulfide` · `bielefeld2019_microstructural_modeling_composite_cathode`.
- 측정: `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` · `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
