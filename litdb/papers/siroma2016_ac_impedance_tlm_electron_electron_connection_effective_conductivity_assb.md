<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 S8 · 3 순위 N-76 · 정독 125) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴) · 같은 축 이웃 = siroma2015_transmission_line_model_porous_electrode_impedance.md (Z · T 연결형 해석해의 원전 [23]) · kaiser2018_… · asano2017_… · jung2019_….
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 키트의 다른 카드와 같은 꼴.
     원문 = 출판본 (J. Power Sources 316 (2016) 215–223 · 9 쪽) + Supporting information (4 쪽 PDF = 표지 1 + 그림 S1 (a)(b) · S1 (c) + 캡션 + 표 S1 · 그림 S2).
     쪽 표기 = 본문은 **인쇄 쪽 p.215–223** (PDF 쪽 = 인쇄 쪽 − 214).  SI 는 "SI p.n" = SI PDF 쪽 n (SI p.1 = 표지 · 인쇄 쪽 번호 없음).  크롭 파일 이름의 p 숫자는 인쇄 쪽, figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (이 논문의 그림은 전부 **벡터**라 PyMuPDF get_drawings 로 표지 중심 · 선 꼭짓점 좌표를 그대로 읽었다 — 재현 = litdb/figures/<slug>/digitized.csv 56 행 · 축 = 그림 틀의 pt 좌표 ↔ 눈금 · 정밀도는 대략 0.001 decade (그림 6) · ≈1 Ω cm² (나이퀴스트)) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (메인 리포 CLAUDE.md 출처) · [미확인] = 본문 9 쪽 + SI 4 쪽 전수에 없음.
     원문 13 쪽은 글자 층 추출 + 전 쪽 렌더로 전부 읽었다 (식은 수식 글꼴이 깨져 렌더에서 옮겼다).  DEM · MPM · 입자 계산 · 압밀 시뮬레이션은 없다 — 실험 (AC 임피던스 · DC) + 1D 등가회로 (전송선 모델 TLM) 이론. -->
# 황화물 유리 (75Li₂S·25P₂S₅) 전고체 전극 혼합층의 이온 · 전자 유효 전도도를 한 셀로 — 전자 저항이 있는 3 줄 전송선 모델 (TLM) 과 'electron-electron connection' (SUS | 시료 | SUS = Siroma 2015 의 T형) 의 물방울 (teardrop) 두 극한 (HFR = R_ion R_e/(R_ion + R_e) · LFR = R_e) · LiNbO₃ 코팅 NCM523 50–70 vol% 와 흑연 비교 · 30 MPa 펠릿 · 25 °C — Siroma · Sato · Takeuchi · Nagai · Ota · Ioroi (J. Power Sources 2016)

> slug `siroma2016_ac_impedance_tlm_electron_electron_connection_effective_conductivity_assb` · DOI `10.1016/j.jpowsour.2016.03.059` · type `experiment + equivalent-circuit theory (AC impedance 10 mHz–1 MHz · two- and three-rail TLM as a 1D continuum ladder · Z-type (ion-electron) vs T-type (electron-electron) connection after Siroma 2015 · DC 10 mV · glass-sulfide composite pellets 30 MPa — no particle simulation)` · PDF `e958c227-76._AC_impedance_analysis_of_ionic_and_electronic_conductivities_in_electrode_mixture_layers_for_an_all-solid-state_lithium-ion_battery.pdf` · SI `781a0ada-76._Sup_AC_impedance_analysis_of_ionic_and_electronic_conductivities_in_electrode_mixture_layers_for_an_all-solid-state_lithium-ion_battery.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **Zyun Siroma\*** ᵃ · Tomohiro Sato ᵇ · Tomonari Takeuchi ᵃ · Ryo Nagai ᵇ · Akira Ota ᵇ · Tsutomu Ioroi ᵃ — ᵃ Research Institute of Electrochemical Energy, National Institute of Advanced Industrial Science and Technology (AIST), Midorigaoka, Ikeda, Osaka 563-8577 · ᵇ Lithium Ion Battery Technology and Evaluation Center (LIBTEC), 같은 주소 — \* 교신 (siroma.z@aist.go.jp) · *J. Power Sources* **316** (**2016**) **215–223** · 접수 2015-12-22 · 수정 2016-02-26 · 수락 2016-03-17 · 온라인 2016-04-04 · © Elsevier B.V. (CC 아님) · 키워드 *Electrochemical impedance · All-solid-state lithium-ion battery · Effective ionic conductivity · Effective electronic conductivity · Transmission-line model* · 연구비 = NEDO "Leading-edge, Innovative Battery Material Evaluation Technology Development" (원문 표기 "New Energy and Industrial Technology **Department** Organization").
> **이웃 카드 (링크만)**: [`siroma2015_transmission_line_model_porous_electrode_impedance`](siroma2015_transmission_line_model_porous_electrode_impedance.md) (이 논문 ref [23] = 식 (10) · (16) 과 Z · T 연결형 이름의 원전 · 그 카드 L549 가 이 논문을 "정본 카드 없음 · 원문 미확인" 으로 가리켰다) · [`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`](kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md) (ref [13] · L157 · L393 — 'Siroma τ ≈3 → ≈10') · [`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`](asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity.md) (ref 2 · L149 · L151 · L323 · L348) · [`jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb`](jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb.md) (ref 22 · L218 · L415 · L433) · [`bong2023_linbo3_thickness_uniformity_ncm523`](bong2023_linbo3_thickness_uniformity_ncm523.md) ('Siroma 법' [32]) · [`otani2023_ionic_conductivity_path_resistance_separation_model`](otani2023_ionic_conductivity_path_resistance_separation_model.md) (ref 17) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (ref [26]).
> **판독 원자료**: `litdb/figures/siroma2016_ac_impedance_tlm_electron_electron_connection_effective_conductivity_assb/digitized.csv` (56 행 — 그림 6 꺾은선 꼭짓점 12 · 그림 5 점근선 · 교점 · HFR 7 · 그림 3b · 4b 곡선 양 끝 6 · 그림 8a · 7 · S1a–c 의 맞춤 곡선 끝 · 자료 끝 · 꼭대기 31) · 그림 크롭 **65 장** (도구 12 중 다시 자름 3 + 손 크롭 53 = 그래픽 초록 1 · 패널 15 · 식 18 · 근거 문단 19) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 75Li₂S·25P₂S₅ 유리 (평균 25.5 µm) 와 LiNbO₃ 코팅 LiNi₀.₅Co₀.₂Mn₀.₃O₂ (11.6 µm) 를 막자로 섞어 **30 MPa** 로 누른 1 cm 펠릿 (331–392 µm) 을 **SUS 판 둘 사이**에 끼우고 AC 임피던스를 재면 (이 논문의 이름 **'electron-electron connection'** = Siroma 2015 의 **T형**), 저주파 반원이 전송선 모델의 **물방울** 꼴이 되고 그 두 끝 — **HFR = R_ion R_e/(R_ion + R_e)** (식 18) · **LFR = R_e** (식 17) — 에서 **이온 · 전자 유효 전도도를 한 번에** 얻는다 (p.215 · p.218–219 · p.222–223).  NCM 50 · 60 · 70 vol% 에서 σ_ion **8.9 · 4.0 · 1.6 × 10⁻⁵** · σ_e **3.2 · 9.7 · 18 × 10⁻⁵ S cm⁻¹** (표 S1 의 1/r [카드 산술]) 이고, σ_e 는 같은 펠릿의 DC (10 mV · 10 s) 값과 **1–2 % 안**에서 같다 [카드 산술].  흑연 전극 (σ_e 9.5 × 10⁻¹ S cm⁻¹) 은 전통적인 대칭 셀 (substrate | sample | SE | sample | substrate = Z형) 의 (1/3) R_ion 법으로 충분하다 (식 7 · 오차 < 10 % · p.221).  **τ 는 원문에 없다** ('tortuos' 0 회) — Kaiser 2018 의 'Siroma τ ≈3 → ≈10' 은 표 S1 의 NCM σ_ion 과 SE 펠릿 5.5 × 10⁻⁴ S cm⁻¹ · 공칭 SE 부피분율로 **3.09 · 5.52 · 10.4** 로 재현된다 [카드 산술].  ⚠ 그런데 본문이 *"obtained with the model shown in Fig. 8(a)"* 라 적은 **그림 6 (b) 의 σ_ion 은 그 표 S1 값보다 16.8 · 22.0 · 39.1 % 낮다** (벡터 좌표 [판독] — 50 % 점은 그림 8 (b) 모형의 r_ion 13 510 Ω cm 와 0.1 % 안) — 같은 논문의 두 판본이 NCM 70 % 에서 1.64 배 갈린다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 측정 축 · 재료 | **황화물 (75Li₂S·25P₂S₅ 비정질 유리 · 25.5 µm · 가정 밀도 1.90 g cm⁻³)** + **NCM523 (LiNi₀.₅Co₀.₂Mn₀.₃O₂ · 11.6 µm · LiNbO₃ ≈5 nm · 4.72)** 또는 **흑연 (20.5 µm · 2.26)** · 무탄소 · 무바인더 · AM : SE = **50 : 50 – 70 : 30 vol%** (가정 진밀도로 맞춘 **고체 부피비** — 펠릿 기공 미보고) · 막자 혼합 | [인쇄] p.219 · 표 1 |
| ② ★ 성형 · 측정 조건 | 펠릿 = 혼합물 ca. 100 mg · **30 MPa 1 분** · 지름 1 cm · 331–392 µm (NCM) · 586 µm (흑연) · 870 µm (NCM 100 %) · SUS 판 둘 · 측정 전 **ca. 30 MPa** 로 다시 누름 (측정 중 유지 여부 [미확인]) · 대칭 셀 = 10 MPa 차례 적층 → **30 MPa 1 분** · SE 층 ca. 700 µm · 전극층 ca. 70 µm (NCM_50 은 49 µm) · AC 10 mV · 10 mHz–1 MHz · 20 점/decade · **25 °C** · DC 10 mV · 10 s · 실온 | [인쇄] p.220–221 · 그림 7 캡션 |
| ③ ★ 이온 · 전자 유효 전도도 (조성별) | NCM: r_ion **11 230 · 25 110 · 63 210** · r_e **31 490 · 10 280 · 5 620 Ω cm** (50 · 60 · 70 vol%) → σ_ion **8.90 · 3.98 · 1.58 × 10⁻⁵** · σ_e **3.18 · 9.73 · 17.8 × 10⁻⁵ S cm⁻¹** [표 S1 인쇄 → 카드 산술] · DC σ_e **3.2 × 10⁻⁵ · 9.7 × 10⁻⁵ · 1.8 × 10⁻⁴ · 1.0 × 10⁻³** (NCM_100) [표 1] · 흑연 σ_ion **5.71 · 1.90 · 0.863 × 10⁻⁵** (그림 6 a [판독]) · 흑연_50 σ_e 9.5 × 10⁻¹ · SE 펠릿 σ **5.5 × 10⁻⁴ S cm⁻¹** | [인쇄] SI p.3 · p.220 · p.221 · [판독] 그림 6 |
| ④ ★ τ (Kaiser 2018 의 'Siroma τ') | 원문 τ **없음** · Kaiser 식 2 (τ_eff = ε σ_SE/σ_eff = 우리 **tau2**) 로 표 S1 → **3.09 · 5.52 · 10.4** (ε = 0.5 · 0.4 · 0.3 공칭) / 그림 6 (b) → 3.71 · 7.08 · 17.1 / 흑연 (그림 6 a) → 4.81 · 11.6 · 19.1 | [카드 산술] |
| ⑤ 해석의 뼈대 (식) | 두 줄 TLM 식 (4) · 저주파 (1/3) R_ion 식 (7) · 세 줄 TLM (Z형) 식 (10) · 극한 (12) (1/3)(R_ion + R_e) · (13) R_ion R_e/(R_ion + R_e) · 과소 평가 비 **α = (1 − K + K²)/(1 + K)** · K = r_e/r_ion (14)–(15) · T형 **식 (16)** · 극한 (17)–(18) | [인쇄] p.216–219 |
| ⑥ 원문이 정한 쓰임 | 전자 저항이 **작으면** (흑연) Z형 대칭 셀 + 식 (7) · **비교적 크면** (NCM) T형 (SUS \| 시료 \| SUS) + 식 (17)–(18) — *"complementary choices depending on the sample"* · T형의 이점 = 전해질 층의 기생 HFR 이 없다 (*"one of the greatest benefits"*) | [인쇄] p.218–219 · p.223 |
| ⑦ 원문의 한계 | 고주파 반원의 원인 **미정** (전자 경로 입계 · 접촉 (모형 b) ↔ 이온 경로 입계 (모형 c) — 두 모형 값 차 **최대 2 % (전자) · 22 % (이온)**) · *"a judgment based only on impedance measurements is limited"* · 조립 그대로 (**최저 SOC**) 라 R_ct 가 커서 쉬운 경우 — 충방전 중에는 모형을 더 다듬어야 · 유한 길이 Warburg 미포함 | [인쇄] p.219 · p.222–223 |
| ⑧ 압밀 · 기공 · 기계 | **없음** — 기공 · 진밀도 기공 · 압력별 측정 · 탈압 · 입자 계산이 없다 ('porosity' 0 회).  성형압은 30 MPa 하나 | — |

⛔ **한정어 (떼지 말 것)**: ① 조성의 vol% 는 **가정 진밀도로 맞춘 고체 부피비**다 — 30 MPa 펠릿의 기공은 인쇄되지 않았고 ("ca. 100 mg" 과 표 1 두께로는 상대밀도가 0.98–1.05 로 나와 계산이 서지 않는다 [카드 산술]) · τ · f 는 그 공칭 ε 위의 값 ② SE 는 **유리 75Li₂S·25P₂S₅** (아지로다이트 LPSCl 아님) · AM 은 **NCM523** (811 아님) · **탄소 · 바인더 없음** · 입경 SE 25.5 µm > AM 11.6 µm (우리 SE ≈1 µm 와 반대) ③ σ_ion 은 **모형 의존** — 같은 NCM_50 스펙트럼에서 세 모형 11 230 · 13 510 · 11 070 Ω cm (22 %) · 같은 논문의 그림 6 (b) 와 표 S1 이 70 % 에서 1.64 배 다르다 ④ 전극은 **조립 그대로 (최저 SOC)** · 25 °C · 측정 중 가압 [미확인] ⑤ 'τ ≈3 → ≈10' 은 **원문 값이 아니라 Kaiser 2018 이 이 논문 자료로 낸 값** (표 S1 로 재현).
⇒ **절대값 전이: 0 건** (재료 · 조성 · 성형압 · 탄소 모두 다르다).  전이되는 것은 **측정 · 해석 규칙** (연결형 Z ↔ T · 식 (14) 의 오차 기준 · AC LFR ≡ DC · 고주파 반원 처리 · 모형 의존 표지) 과 **조성 방향** (AM ↑ → σ_e ≈ φ_AM^5 꼴로 오르고 σ_ion 은 SE 부피분율보다 빠르게 떨어진다 [카드 산술]) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-76 의 '왜' 칸)

의도 원문: *"수송 실험 대조 — 황화물 ASSB 전극 임피던스 τ (ε 0.5 → 0.3 에서 ≈3 → ≈10) = kaiser 이전 유일한 같은 축 자료 · jung2019 의 셀 구성 문장 · R_ct · Warburg 제외 근거 (셀 구성이 jung 의 SUS 와 달라 원문 확인 필요) · "Siroma 법" σ_e 분리 측정 (siroma2015) · asano2017 의 연결형 (T형 open–open) 대응 = 카드 판독"* (가리킨 카드 = kaiser2018 L157 · L393 · jung2019 L218 · L415 · L433 · asano2017 L151 · siroma2015 L549)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "수송 실험 대조 — 황화물 ASSB 전극 임피던스" | **채움** | 75Li₂S·25P₂S₅ 유리 SE 의 흑연 · NCM523 전극 혼합층 AC 임피던스 + TLM (p.215 초록 · p.219–223) · **25 °C** · 펠릿 **30 MPa 1 분** 성형 · 측정 전 ca. 30 MPa 재가압 (측정 중 유지 [미확인]) · 진밀도 = 가정값 (흑연 2.26 · NCM 4.72 · SE 1.90 g cm⁻³) |
| "τ (ε 0.5 → 0.3 에서 ≈3 → ≈10)" | **일부** | 원문에 τ **없음** (값 · 낱말 0) — 원문은 σ_eff 만 (그림 6 · 표 S1).  Kaiser 식 2 (τ_eff = ε σ_SE/σ_eff) 에 표 S1 NCM σ_ion · SE 펠릿 5.5 × 10⁻⁴ S cm⁻¹ (p.221) · 공칭 ε 0.5 · 0.4 · 0.3 을 넣으면 **3.09 · 5.52 · 10.4** [카드 산술] = '≈3 → ≈10' 재현.  같은 논문 그림 6 (b) 로는 3.71 · 7.08 · 17.1 · 흑연 (그림 6 a) 4.81 · 11.6 · 19.1 [카드 산술 · 판독].  ε 은 **고체 기준 공칭값** (펠릿 기공 미보고 · 30 MPa) |
| "= kaiser 이전 유일한 같은 축 자료" | **없음 (이 원문으로 판정 불가)** | '유일' 은 Kaiser 의 문헌 판단 — 이 논문 서론은 액체 전극 Ogihara [10] 을 출발점으로 들 뿐 다른 ASSB 전극 τ 자료를 들지 않는다 (p.216) |
| "jung2019 의 셀 구성 문장" (*"Au/NCM + SE composite/Au configuration"* [22]) | **없음** | 원문 셀 = **SUS 판** — *"Each pellet was set between two SUS plates as current collectors"* (Scheme 3) · 대칭 셀도 *"between two SUS plates"* (Scheme 2) (p.220) · 'Au' 낱말 0 회.  ⇒ Jung 의 Au 문장은 이 원문에서 오지 않았다 — 셀 구성은 오히려 **Jung 의 SUS 와 같다** |
| "R_ct · Warburg 제외 근거" | **채움** (근거의 뜻은 다름) | R_ct: *"each NCM electrode was used as prepared, i.e., with the lowest SOC. Therefore, the charge-transfer resistance should be high"* (p.223) · *"probably due to the relatively high charge-transfer resistances of our electrodes"* (p.219).  Warburg: *"a finite-length Warburg impedance should be added to r_ct in series … beyond the scope of this paper, since our experimental results do not show such an additional semicircle"* (p.219).  10 mV 는 AC **진폭** (p.221) — 원문은 'R_ct 가 큰 이유 = 10 mV 진폭' 이라 하지 않는다 (이유 = 최저 SOC) |
| "(셀 구성이 jung 의 SUS 와 달라 원문 확인 필요)" | **확인 끝** | 원문도 SUS (위) — 다르지 않다.  다른 것은 Jung 의 **인용 문장** (Au) 이다 |
| "'Siroma 법' σ_e 분리 측정 (siroma2015)" | **채움** (σ_ion 도 함께) | SUS \| 시료 \| SUS 의 LFR = **r_e L = R_e** (식 17) → σ_e = 1/r_e · HFR (식 18) 과 함께 σ_ion — *"which gives both the ionic and electronic conductivities"* (p.215) · 같은 셀의 DC (10 mV · 10 s) σ_e (표 1) 가 AC 1/r_e 와 0.992 · 1.003 · 0.989 배 [카드 산술] · 적용 조건 = *"only effective for a sample with a relatively low electronic conductivity"* (p.216) · siroma2015 = 식 (16) 의 원전 [23] |
| "asano2017 의 연결형 (T형 open–open) 대응 = 카드 판독" | **채움** (판독 → 원문 확인) | *"This type of connection corresponds to a 'T-type connection' in Ref. [23], and is hereafter referred to as 'electron-electron connection'"* · ion-electron = *"'Z-type connection' in Ref. [23]"* (p.218) · 식 (16) = 단자 레일 (전자) 계수 2 z_C² · 이온 레일 양 끝 열림 (그림 1 c) |

**가리킨 카드 · 같은 논문을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `kaiser2018_…` L157 | *"Siroma [13] \| 비정질 Li₂S-P₂S₅ + NCM523 또는 흑연 (ASSB) \| 0.5 → 0.3 \| ≈ 3 → ≈ 10 \| 임피던스 — 미지의 고주파 과정 때문에 저 ε 에서 불확도 큼"* (Kaiser 서론의 재인용 · 카드가 "원 논문과 대조 안 함" 표지) | 재료 ✓ (75Li₂S·25P₂S₅ 비정질 유리 · LiNi₀.₅Co₀.₂Mn₀.₃O₂ · 흑연) · ε 0.5 → 0.3 = 공칭 SE 부피분율 ✓ · τ ≈3 → ≈10 = 표 S1 로 3.09 → 10.4 ✓ [카드 산술] · 고주파 반원 원인 미정 ✓ (p.222–223) · **"저 ε 에서 불확도 큼" = 원문 문장 없음** — 단 그림 S1 b (NCM_70) 의 물방울이 폭 15 Ω cm² 뿐이고 그림 6 (b) ↔ 표 S1 차가 −39 % 로 커지는 것이 그 말을 뒷받침한다 [카드 산술 · 판독] | **일부** (카드 오류 아님 — Kaiser 문장을 그대로 옮김) |
| `kaiser2018_…` L393 | 서지 *"… J. Power Sources 316 (2016) 215–223"* · *"황화물 ASSB 전극의 임피던스 τ (ε 0.5 → 0.3 에서 ≈ 3 → ≈ 10) — 이 논문 이전의 유일한 같은 축 자료"* · *"Siroma 2015 와 다른 논문"* | 서지 ✓ · 다른 논문 ✓ · **τ 는 원문 값이 아니다** (Kaiser 산출) · '유일' = Kaiser 판단 | **일부** (τ 귀속 · 아래 카드 문제 ③) |
| `jung2019_…` L218 | *"the charge transfer resistance is expected to be large under the experimental conditions of 10 mV amplitude in the Au/NCM + SE composite/Au configuration [22] (… 셀은 SUS 인데 문장은 Au — §10)"* | 원문 = SUS 판 (p.220) · R_ct 가 큰 이유 = 최저 SOC (p.223) · 10 mV = 진폭 (p.221) | 카드는 Jung 원문을 바르게 옮겼다 — **Jung 문장이 이 원문과 다르다** (Au · 이유) |
| `jung2019_…` L415 | *"셀 구성 Au/NCM + SE composite/Au (p.22969, [22] 인용 문장 — 인용 문헌의 셀 구성을 빌린 서술로 읽히나 구분 없음)"* | 인용 문헌 (= 이 논문) 도 **Au 가 아니라 SUS** | **카드 해석이 원문과 안 맞음** → 카드 문제 ① |
| `jung2019_…` L433 | 서지 ✓ · *"이 논문의 R_ct · Warburg 제외 근거와 'Au/…/Au' 문장의 출처 · Kaiser 카드도 같은 논문을 '없음' 으로 기록"* | 서지 ✓ (J. Power Sources, 2016, 316, 215–223) · R_ct · Warburg 근거 ✓ · **'Au/…/Au' 는 원문에 없다** | **일부** → 카드 문제 ① |
| `asano2017_…` L149 | Asano 문장 *"… teardrop shape … high and low frequency limit values … r_ion·r_e·L/(r_ion + r_e) and r_e·L"* | 식 (17) · (18) ✓ · 결론 p.223 ✓ | **채움** |
| `asano2017_…` L151 | *"연결형 … T형 open–open … 2015 표와의 대응은 우리 판독이다"* | 원문 p.218 이 직접 T-type 대응을 적는다 · 식 (16) [23] | **채움** (판독 확인) |
| `asano2017_…` L323 | *"서론의 Siroma 2016 재료 표기 'LiNi0.5Mn0.2Co0.3O2' (p.A3960) — Siroma 2016 원문 미대조"* | 원문 = **LiNi₀.₅Co₀.₂Mn₀.₃O₂** (p.215 · p.216 · p.219) | **다름 — Asano 의 인용 오기 (Co ↔ Mn 자리)** · 카드는 옮긴 그대로 · [미확인] 해소 → 카드 문제 ② (정보) |
| `asano2017_…` L348 | *"AC 법 … 연결형 (T형 판독) · 고주파/저주파 극한의 유도 · 적용 조건 (r_e ≳ r_ion) 확인"* | 연결형 ✓ · 극한 ✓ · 적용 조건은 원문에서 **정성** (*"relatively low electronic conductivity"* p.216 · *"effective when the electronic resistance is high"* p.219) — 원문은 r_e/r_ion = 0.089 (NCM_70) 에도 적용했다 [카드 산술] | **일부** ('r_e ≳ r_ion' 은 Asano 쪽 문장) |
| `siroma2015_…` L549 | *"T형을 복합 전극에 적용 · σ_e 분리 측정 ('Siroma 법' — bong2023 카드 [32] 와 같은 논문) · 정본 카드 없음 · 이 카드에서 원문 미확인"* | T형 ✓ · σ_e ✓ (+ σ_ion) · 같은 논문 ✓ | **채움** — 이제 카드 있음 |
| `bong2023_…` L769 · L706 | *"Li⁺ 차단 / 전자 전도 전극 (스테인리스) 을 써서 복합전극의 **전자** 전도만 분리 측정하는 AC 임피던스법 · σ_e = L/r_e"* | 원문 방법은 **이온 · 전자 둘 다** (p.215 · p.223) · r_e 는 Ω cm (σ_e = 1/r_e = L/R_e) | **일부** (Bong 의 쓰임 = 전자만) → 카드 문제 ④ (용어) |
| `otani2023_…` L63 · L128 · L263 · `hlushkou2018_…` L362 · `kato2018_…` L458 · `minnmann2021_…` L833 · `kawaguchi2026_…` L252 | SUS 사이 전자–전자 연결형 EIS · 서지 · 'T-type TLM 을 복합 전극에 적용한 선행' · 'Z. Shiroma' (Kawaguchi 원문 표기) | ✓ (저자 로마자 = **Siroma**) | **채움** |

⇒ **의도 대조 결과: 일부** — 황화물 ASSB 전극 임피던스 · 'Siroma 법' (σ_e + σ_ion) · T형 대응 · R_ct/Warburg 근거는 **채움**; 'τ ≈3 → ≈10' 은 원문 값이 아니라 Kaiser 가 이 논문의 표 S1 로 낸 값 (재현됨 · 그림 6 으로는 3.7 → 17) 이라 **일부**; Jung 의 'Au/…/Au' 셀 구성은 **원문에 없다** (원문 = SUS) · 'kaiser 이전 유일' 은 이 원문으로 판정 불가.

---

## 1. 한 줄 요약
전고체 전극 혼합층은 전자 전도도가 낮을 수 있어 (NCM + 유리 SE, 무탄소) 액체 전극에서 쓰던 '전자 저항 0 인 두 줄 TLM + 저주파 (1/3) R_ion' 법이 틀릴 수 있다 — 저자들은 전자 저항 줄을 넣은 세 줄 TLM 의 나이퀴스트 꼴을 계산으로 먼저 보이고 (그림 2–4), 이온 단자 ↔ 전자 단자 (**ion-electron = Z형**) 대신 **전자 단자 양 끝 (electron-electron = T형 · SUS | 시료 | SUS)** 으로 재면 저주파에 **물방울** 이 생기고 그 두 실수 끝에서 R_ion · R_e 를 함께 풀 수 있음을 보인 뒤, 흑연 전극 (Z형으로 충분) 과 NCM 전극 (T형) 의 σ_ion 이 SE 부피비에 대해 **같은 꼴로** 움직인다는 것을 근거로 방법을 검증한다.
저자의 결론: *"the ionic and electronic conductivities of an electrode mixture layer with a relatively low electronic conductivity can be obtained by the measurement with the electron-electron connection"* (p.223).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Z. Siroma\* · T. Sato · T. Takeuchi · R. Nagai · A. Ota · T. Ioroi (AIST RIECEN · LIBTEC) | J. Power Sources 316 (2016) 215–223 · Elsevier | 10.1016/j.jpowsour.2016.03.059 | **75Li₂S·25P₂S₅ 비정질 유리** (25.5 µm) + **LiNi₀.₅Co₀.₂Mn₀.₃O₂** (11.6 µm · LiNbO₃ ≈5 nm) 또는 **흑연** (20.5 µm) · 무탄소 · 무바인더 | 실험 (AC 임피던스 · DC) + 등가회로 이론 (1D TLM · Z형 / T형 연결) |

- **1저자 메모와의 대조**: 저자 6 명 · 제목 · 학술지 · 권 316 · 쪽 215–223 · 2016 · DOI (PDF 문서 정보 · 첫 쪽) — **같다**.  덧붙임 ① 후보 표의 "(DOI 카드에 없음)" → DOI = **10.1016/j.jpowsour.2016.03.059** (p.215 아래) ② 저자 로마자 = **Siroma** (다른 논문 원문이 'Shiroma' 로 적기도 한다 — kawaguchi2026 카드 L252 · otani2023 카드 L249) ③ SI 는 Word 원고 (2016-02-25) 4 쪽.
- **글의 꼴**: 1 서론 (Scheme 1–3 = 번호 붙은 셀 구성 줄 (1)–(3)) → 2 이론 (2.1 전자 저항 없는 TLM 식 (4)–(9) · 2.2 전자 저항 있는 TLM 식 (10)–(18)) → 3 실험 → 4 결과 (4.1 흑연 · Z형 · 4.2 NCM · T형) → 5 결론 → 참고문헌 31.  그림 8 · 표 1 · 식 18 (번호 셀 구성 3 포함) / SI: 그림 S1 (a)(b)(c) · S2 · 표 S1.
- 그룹 맥락: 1저자의 TLM 해석해 전집 Siroma 2015 (Electrochim. Acta 160, 313 = ref [23] · 정본 카드 있음) 의 응용편.  LIBTEC = 일본 전지 평가 컨소시엄 (같은 랩 계열의 LPSCl 복합 측정 = otani2023 · kawaguchi2026 카드).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 시편 · 측정 (p.219–221 · 표 1 · `txt_p219_experimental_materials.png` · `txt_p220_pellets_30mpa_dc_symmetric.png` · `txt_p221_eis_conditions_fitting.png` · `tab_1.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | **75Li₂S·25P₂S₅ amorphous glass powder** · 평균 입경 **25.5 µm** · 가정 진밀도 **1.90 g cm⁻³** | [인쇄] p.219 |
| AM | **LiNi₀.₅Co₀.₂Mn₀.₃O₂** · 평균 **11.6 µm** · **LiNbO₃ ≈5 nm** (Nb(OEt)₅ + LiOEt 에탄올 용액 · 회전 유동층 조립 코팅기 분무 → 산소 **400 °C 30 분**) · 가정 진밀도 **4.72** / 흑연 · 평균 **20.5 µm** · **2.26** | [인쇄] p.219 |
| 혼합 · 조성 | 막자 (mortar) · AM : SE = **50 : 50 – 70 : 30 vol%** (*"under the assumptions that the actual densities … were 2.26, 4.72, and 1.90 g cm⁻³"*) · 탄소 · 바인더 없음 | [인쇄] p.219 |
| T형 펠릿 (Scheme 3) | 혼합물 **ca. 100 mg** · **30 MPa 1 분** · 지름 **1 cm** · 두께 *"typical … ca. 400 µm"* · **SUS 판 둘** (집전체) · 측정 전 셋업 (시료 + SUS) 을 **ca. 30 MPa** 로 다시 누름 | [인쇄] p.220 |
| 두께 (표 1) | graphite_50 **586** · NCM_50 **392** · NCM_60 **342** · NCM_70 **331** · NCM_100 **870 µm** (NCM_100 은 임피던스 안 잼) | [인쇄] p.220 |
| ⚠ 펠릿 밀도 · 기공 | **[미확인]** — 'ca. 100 mg' 를 그대로 쓰면 이론 밀도 (가정 진밀도 가중) 대비 상대밀도 **0.981 (NCM_50) · 1.036 (NCM_60) · 0.993 (NCM_70) · 1.045 (graphite_50) · 0.310 (NCM_100)** — 1 을 넘는 값이 있어 질량이 근사값임이 드러난다 · 기공을 낼 수 없다 [카드 산술: ρ_th = Σ vol% × ρ · V = π (0.5 cm)² × 두께].  같은 조성 유리 순수 펠릿은 **≈30 MPa 에서 상대밀도 ≈50 %** 라는 다른 카드의 판독이 있다 [다른 카드 · `sakuda2013_sulfide_mechanical_property` L53 · Fig 2a 추세 판독 · 복합 · 다른 배치라 그대로 옮기지 않는다] | [카드 산술] · [카드 해석] |
| Z형 대칭 셀 (Scheme 2) | 가운데 SE 층 + 양옆 전극층을 **10 MPa** 로 차례 적층 → **30 MPa 1 분** · **SUS 판 둘 사이** · SE 층 ca. **700 µm** · 전극층 ca. **70 µm** (NCM_50 = **49 µm** · 그림 7 캡션) | [인쇄] p.220 · p.221 |
| DC | 10 mV 를 **10 s** 건 뒤 전류 · 실온 · *"a rough estimate of the electronic resistance"* · 기하 크기로 σ | [인쇄] p.220 |
| AC | 진폭 **10 mV** · **10 mHz–1 MHz** · Solartron SI 1287 + SI 1260 · 로그 **20 점/decade** · **25 °C** | [인쇄] p.221 |
| 맞춤 | Microsoft Excel Solver · **상대 편차 제곱합** 최소 · 매개변수 **4 개 (모형 a) 또는 7 개 (모형 b · c)** · NCM 은 **저주파 반원 꼭대기 아래 주파수** 자료만 (NCM_50: **0.01–0.35 Hz**) | [인쇄] p.221 · p.222 · SI p.3 |
| SE 펠릿 σ | SE 만으로 만든 펠릿의 HFR → **5.5 × 10⁻⁴ S cm⁻¹** (그림 6 의 0 % 점 = log σ −3.258 → **5.52 × 10⁻⁴** [판독]) · 그 펠릿의 성형압 · 두께 **[미확인]** | [인쇄] p.221 · [판독] 그림 6 |

### 3-2. ★ 이론 — 연결형 · 식 · 극한 (p.216–219 · 그림 1–4 · `eq_04_…` – `eq_18_…` · `txt_p217_dimensions_zA_zB.png` · `txt_p218_*` · `txt_p219_ee_no_parasitic_rct_warburg.png`)
- **단위 규약** (p.217): z_A (이온 줄) = 비저항 **[Ω cm]** = 1/σ · ×L → **[Ω cm²]** = TLM 전체와 같은 차원 · 실측 [Ω] = Ω cm² ÷ 기하 면적 S · z_B (계면) = **단위 부피당 계면 임피던스 [Ω cm³]** = z_IF [Ω cm²] ÷ 부피당 비표면적 s [cm² cm⁻³] · ÷L → Ω cm² · c_dl (또는 c_dl\*) 은 **주파수 위치만** 바꾸고 나이퀴스트 꼴은 안 바꾼다.  원문 표기 *"Oh the other hand"* (오식).
- **두 줄 TLM (전자 저항 없음 · 그림 1 a)**: 식 (4) **Z = √(z_A z_B) coth(L √(z_A/z_B))** [15] · 식 (5) **z_A = r_ion = 1/σ_ion^eff** · 식 (6) z_B = 1/(jω c_dl) → 45° 선 + 수직선 · 식 (7) **lim(ω→0) Z′ = (1/3) r_ion L = (1/3) R_ion** ('폭' = 유효 이온 전도도 [13,14]) · 식 (8) z_B = 1/(jω c_dl + 1/r_ct) (그림 2 b · 저주파가 호로 휨) · 식 (9) z_B = 1/((jω)^ψ c_dl\*) (CPE · 그림 2 c).  일그러짐이 작으면 45° 선 ↔ 수직선 (호) 의 **전이점**으로 R_ion 을 어림한다 [10].
- **세 줄 TLM (전자 저항 · 그림 1 b · Z형)**: 식 (10) **Z = z_A z_C L/(z_A + z_C) + √z_B/(z_A + z_C)^{3/2} · [(z_A² + z_C²) cosh β + 2 z_A z_C]/sinh β**, β = L √((z_A + z_C)/z_B) [21–23] · 식 (11) **z_C = r_e = 1/σ_e^eff** · 극한 식 (12) **lim(ω→0) Z′ = (1/3)(r_ion + r_e) L** [31] · 식 (13) **lim(ω→∞) Z = r_ion r_e L/(r_ion + r_e)** (= HFR ≠ 0).  [카드 산술 — 식 (10) 을 작은 β 로 펼치면 실수부가 정확히 (z_A + z_C) L/3 → 식 (12) 확인.]
- **HFR 의 문제** (p.217): 실측에서는 대칭 셀의 전해질 층 (Scheme 2) 이나 보상 안 된 저항이 HFR 에 늘 더해진다 → *"it is difficult to use Eq. (13), since the parasitic resistance outside the TLM must be estimated exactly"*.
- **과소 평가 기준** (p.218): 전자 저항을 무시하고 식 (7) 을 쓰면 얻는 r_ion 의 비 **α ≡ [(1/3)(r_ion + r_e)L − r_ion r_e L/(r_ion + r_e)] / [(1/3) r_ion L] = (1 − K + K²)/(1 + K)**, **K = r_e/r_ion** (식 14–15 · 인쇄 글자 α · PDF 글자 층은 'a').  [카드 산술: α < 1 ⇔ **0 < K < 2** · 최소 **0.464 @ K = √3 − 1 = 0.732** · K = 2 에서 1 · **K > 2 이면 α > 1 = 과대 평가** (K = 2.80 → 1.59) — 원문의 *"an underestimation will result"* 는 그림 3 의 범위 (K ≤ 1.5) 에서만 참]
- **연결형 이름** (p.218): 식 (4) · (10) = 이온 줄 한 끝 ↔ 반대편 전자 줄 끝 = **"ion-electron connection" = Ref. [23] 의 "Z-type"** (3 전극 또는 대칭 셀) · 전자 줄 양 끝 = **"electron-electron connection" = "T-type"** (SUS 둘 사이 = Scheme 3) · 이점 = *"the ambiguity of the obtained HFR is minimized"*.
- **T형 해** 식 (16): **Z_e−e = z_A z_C L/(z_A + z_C) + 2 z_C² √z_B/(z_A + z_C)^{3/2} · [cosh β − 1]/sinh β** [23] → r_e = 0 이면 값이 없고 (*"self-evident"*), r_e 가 클수록 **물방울 (반원 + 45° 선)** 이 커진다 · 극한 식 (17) **lim(ω→0) Z_e−e = r_e L = R_e** (LFR · 실수) · 식 (18) **lim(ω→∞) Z_e−e = r_ion r_e L/(r_ion + r_e)** (= 식 13).  기생 저항이 없다 = *"one of the greatest benefits of using the electron-electron connection"* (p.219).
- **비이상 z_B 의 영향** (그림 4 · p.219): CPE 로 바꿔도 **LFR 불변** (그림 4 d) · r_ct 를 넣으면 LFR 이 **조금** 움직인다 (그림 4 b) — 벡터 판독 **500.0 → 490.2 → 481.1 Ω cm²** (r_ct⁻¹ = 0 · 10 · 20 mS cm⁻³) [판독] = 식 (16) 에 z_B = r_ct 를 넣은 직류값 **500 · 490.1 · 481.1** 과 같다 [카드 산술].  원문 해석: 이것은 *"model-derived error"* — 실제 전하 이동은 용량이 유한해 DC 에서 멎으므로 LFR 은 r_e 에서만 온다 · 그것을 모형에 넣으려면 r_ct 에 **유한 길이 Warburg** 를 직렬로 넣어야 하고 저주파에 반원이 하나 더 생긴다 → 실험에 그 반원이 없어 **범위 밖** (높은 R_ct 때문으로 봄).
- **쓰임의 정리** (p.219): *"the electron-electron connection is effective when the electronic resistance is high, which is opposite the case for the ion-electron connection … complementary choices depending on the sample"* · *"if the magnitude of the LFR is experimentally detectable, some feature on the Nyquist plot originated from the TLM will surely be observed, unless the ionic resistance is extremely large compared with the electronic resistance"*.
- **계산 조건** (그림 2–4 표준): L = **0.5 mm** · r_ion = **10 kΩ cm** · c_dl = **10 mF cm⁻³** · r_ct = ∞ · ψ = 1 (그림 4: r_e = **10 kΩ cm**).  그림 3 (b) 벡터 판독: HFR 166.8 · 250.4 · 300.8 · LFR 249.7 · 499.9 · 750.1 Ω cm² (r_e 5 · 10 · 15 kΩ cm) [판독] = 식 (17)–(18) 값 166.7 · 250 · 300 / 250 · 500 · 750 [카드 산술] ✓.
- ⚠ **그림 2 캡션** 은 *"TLMs with electronic resistance"* 라 적지만 그림 · 삽입 회로 · 2.1 절은 **전자 저항이 없는** 두 줄 TLM 이다 [카드 해석 — 캡션 낱말 오기로 보인다].

### 3-3. ★ 흑연 전극 — Z형 (대칭 셀) + 식 (7) (p.221 · 그림 5 · 그림 6 a · `fig_5.png` · `txt_p221_graphite_ion_electron_results.png` · `txt_p221_graphite_error_ncm_intro.png`)
- **근거** [인쇄 p.221]: 흑연 전극 σ_e 가 높다 (graphite_50 DC **9.5 × 10⁻¹ S cm⁻¹** · 60 · 70 은 안 잼) ↔ SE 펠릿조차 **5.5 × 10⁻⁴ S cm⁻¹** → 두 줄 TLM (그림 1 a) 로 해석.
- **그림 5 (graphite_50 · Scheme 2 · 두 전극이라 값 ÷ 2)** [판독 · 벡터 · digitized.csv fig5]: 자료의 실수축 교차 (HFR) **Z′ ≈ 64.5 Ω cm²** · 두 점근선 (빨강 고주파 · 파랑 저주파) 교점 **Z′ ≈ 106.5 Ω cm²** → 폭 **≈42.0** → R_ion (전극 하나) **≈126 Ω cm²** [카드 산술 · 식 7].  원문 문장 *"the real part of the intersection of two asymptotic lines can be used to estimate the effective ionic conductivity by Eq. (7), after subtraction of the HFR"*.
  [카드 산술 — 검산]: 전극층 'ca. 70 µm' 이면 σ_ion = 0.0070/126 = **5.5 × 10⁻⁵** (인쇄 최대값 5.7 × 10⁻⁵ 에는 L ≈ 72 µm) · HFR × 2 = 129 Ω cm² = SE 층 (ca. 700 µm) 저항이라면 σ_SE ≈ **5.4 × 10⁻⁴** (인쇄 5.5 × 10⁻⁴) — 그림 5 의 두 값이 본문 숫자와 서로 맞는다.  ⚠ 흑연 전극층의 실제 두께는 시료마다 인쇄되지 않았다 [미확인].
- **흑연 σ_ion (그림 6 a)** [판독 · 벡터]: **5.71 × 10⁻⁵ (50 %) · 1.90 × 10⁻⁵ (60 %) · 8.63 × 10⁻⁶ S cm⁻¹ (70 %)** — 50 % 값 = 본문 *"the highest value of the ionic conductivity was 5.7 × 10⁻⁵ S cm⁻¹"* 와 같다.
- **오차 판정** [인쇄 p.221]: *"the ratio (K in Eqs. (14) and (15)) does not exceed 0.057, which corresponds to an α of 0.90 … the error … is less than 10%"*.  [카드 산술] α(0.057) = 0.895 ✓ · 그런데 **K = 0.057 = 5.7 × 10⁻⁵ / 1.0 × 10⁻³** — 즉 σ_e ≥ **1.0 × 10⁻³ S cm⁻¹** 을 놓은 값이다 (표 1 의 graphite_50 9.5 × 10⁻¹ 을 쓰면 K ≈ 6 × 10⁻⁵ · α ≈ 0.9999) · 1.0 × 10⁻³ 의 출처는 원문에 없다 (NCM_100 값과 같은 숫자 [카드 해석]) — 결론 (오차 < 10 %) 은 더 보수적인 쪽이라 바뀌지 않는다.

### 3-4. ★ NCM 전극 — T형 (SUS | 시료 | SUS) (p.221–223 · 그림 7 · 8 · S1 · S2 · 표 S1 · `fig_7.png` · `fig_8a–c.png` · `fig_S1*.png` · `tab_S1.png` · `txt_p222_*` · `txt_p223_*`)
- **그림 7 (NCM_50)** [인쇄 캡션 · 판독]: (a) Z형 (49 µm 전극 둘 · ÷ 2) = *"rather featureless"* — 45° → 수직선 전이점을 못 찾음 · (b) T형 (392 µm) = **두 반원** — 첫 점 (최고 주파수) Z′ ≈ 43 · 끝 (0.01 Hz) Z′ ≈ 1220 · Z″ ≈ −42 · 저주파 반원 꼭대기 ≈ (867, −298) Ω cm² [판독].  그림 범례 철자 *"ion-electoron"* (원문).
- **저주파 반원 = TLM 물방울이라는 가정** (p.222): 그림 4 (d) 삽입 회로 (CPE z_B) 로 0.01–0.35 Hz 자료만 맞춤 → **모형 (a)**: r_ion **11 230 Ω cm** · r_e **31 490 Ω cm** · ψ_cpe **0.84** · cpe_dl **0.0914 F cm⁻³ s⁻⁰·¹⁶** [인쇄].  그림 8 (a) 맞춤선의 실수축 끝 **Z′ ≈ 325.9** [판독] = 식 (18) HFR **324.5 Ω cm²** [카드 산술 · L 0.0392 cm] · R_e = r_e L = **1234 Ω cm²** (자료 끝 1220 은 아직 실수축 위 −42) [카드 산술 · 판독].
- **고주파 반원의 두 설명** (p.222):
  - **모형 (b) 전자 경로에 구조** — *"some of the electronic path is accompanied by capacitance in parallel. A possible example … is a grain boundary or contacts between particles. Since the samples were made just by pressing of the powders, it seems to be quite possible that the major part of the electronic resistance is due to the contact resistance between particles"* → r_ion **13 510** · r_e,bulk **860** · r_e,gb **31 230 Ω cm** (gb 몫 **97.3 %** [카드 산술]).
  - **모형 (c) 이온 경로에 구조** → r_ion,bulk **350** · r_ion,gb **10 720** · r_e **31 530 Ω cm** (gb 몫 **96.8 %** [카드 산술]).
  - *"the total of the electronic or ionic resistance is almost the same among the three models. The discrepancies among the models are at most 2% and 22%"* — [카드 산술] 전자 31 490 · 32 090 · 31 530 (최대/최소 **1.019**) · 이온 11 230 · 13 510 · 11 070 (**1.220**) = NCM_50 세 모형으로 2 % · 22 % 가 정확히 재현된다 · NCM_60 · 70 은 모형 (b) · (c) 값이 인쇄되지 않아 '모든 NCM 에서 최대 22 %' 는 확인할 수 없다 [미확인].
  - 그림 S2: 모형 (b) · (c) 를 Z형으로 계산하면 둘 다 그림 7 (a) 처럼 *"featureless"* 하고 서로 비슷 → *"a judgment based only on impedance measurements is limited, and some other experiment will be required"* (p.223).
- **표 S1 (모형 a · SI p.3)** [인쇄] + 유도값 [카드 산술: L = 표 1 두께]:

| 시료 | r_ion (Ω cm) | r_e (Ω cm) | c_dl\* (F s^(ψ−1) cm⁻³) | ψ | σ_ion = 1/r_ion | σ_e = 1/r_e (DC 표 1) | R_ion · R_e (Ω cm²) | HFR · 물방울 폭 (Ω cm²) | K = r_e/r_ion |
|---|---|---|---|---|---|---|---|---|---|
| NCM_50 | **11 230** | **31 490** | **0.0914** | **0.84** | 8.90 × 10⁻⁵ | 3.18 × 10⁻⁵ (3.2 × 10⁻⁵) | 440 · 1234 | 324.5 · 910 | 2.80 |
| NCM_60 | **25 110** | **10 280** | **0.0635** | **0.84** | 3.98 × 10⁻⁵ | 9.73 × 10⁻⁵ (9.7 × 10⁻⁵) | 859 · 352 | 249.5 · 102 | 0.409 |
| NCM_70 | **63 210** | **5 620** | **0.0688** | **0.69** | 1.58 × 10⁻⁵ | 1.78 × 10⁻⁴ (1.8 × 10⁻⁴) | 2092 · 186 | 170.8 · 15.2 | 0.089 |

  그림 S1 판독 (벡터): NCM_60 맞춤선 끝 ≈247 · 자료 끝 ≈351 Ω cm² · NCM_70 맞춤선 끝 ≈170–171 · 자료 끝 ≈185 Ω cm² — 위 계산 HFR · R_e 와 ±2 Ω cm² 안 [판독 · 카드 산술].  NCM_70 의 저주파 물방울은 **높이 ≈3.9 · 폭 ≈15 Ω cm²** 로, 고주파 반원 (꼭대기 ≈27 Ω cm² · Z′ 34 → 171) 끝에 붙은 꼬리다 (그림 S1 b · c) [판독].
- **AC ↔ DC**: σ_e (1/r_e) ÷ DC = **0.992 · 1.003 · 0.989** [카드 산술] — LFR (식 17) 이 DC 값과 1–2 % 안에서 같다 = 물방울 귀속의 독립 검산 (원문은 *"the behavior of the electronic conductivity is also reasonable, i.e., a higher SE ratio shows a lower electronic conductivity"* 까지만 적는다).
- **HFR 오차의 증폭** [카드 산술: R_ion = HFR·R_e/(R_e − HFR) · R_e 고정 → dR_ion/R_ion = R_e/(R_e − HFR) · dHFR/HFR]: NCM_50 **×1.36** · NCM_60 **×3.44** · NCM_70 **×12.3** (HFR 1 Ω cm² 오차 → R_ion **7.2 %**) — 전자 저항이 이온 저항보다 훨씬 작으면 (K ≪ 1) T형 의 이온값은 작은 물방울 하나에 매달린다 (원문 p.219 *"unless the ionic resistance is extremely large compared with the electronic resistance"* 의 정량판).
- **원문 쪽 조성 의존** (p.222): *"the carbon electrodes and NCM electrodes exhibit a similar dependency of the ionic conductivity on the SE volume ratio. This strongly supports the validity of the assumption that the semicircle of the lower frequency originates from the TLM"*.

### 3-5. ⚠ 그림 6 (b) ↔ 표 S1 — 같은 '모형 (a)' 값이 다르다 (`fig_6.png` · digitized.csv fig6)
- 본문 (p.222): *"Lines (b) and (c) in Fig. 6 are the ionic and electronic conductivities obtained with the model shown in Fig. 8(a)"* · 표 S1 = *"Fitted parameters in the TLM shown in the insert in Fig. 8(a)"*.
- 벡터 좌표 (꺾은선 꼭짓점 · 정밀도 ≈0.001 decade) [판독]: (b) NCM σ_ion **7.41 × 10⁻⁵ · 3.11 × 10⁻⁵ · 9.64 × 10⁻⁶ S cm⁻¹** · (c) NCM σ_e **3.20 × 10⁻⁵ · 9.73 × 10⁻⁵ · 1.80 × 10⁻⁴ · 9.99 × 10⁻⁴** (50 · 60 · 70 · 100 %).
- [카드 산술]: (b) ÷ 표 S1 1/r_ion = **0.832 · 0.780 · 0.609** (−16.8 · −22.0 · −39.1 %) · (c) ÷ 표 S1 1/r_e = 1.008 · 1.000 · 1.014 (DC 표 1 과는 2 자리에서 같다).  **50 % 점 = 1/13 510 (모형 b 의 r_ion) 과 0.08 % 안** → 그림 6 (b) 는 적어도 50 % 에서 **모형 (b) 값**으로 그려진 것으로 읽힌다 [카드 해석].  60 · 70 % 도 모형 (b) 라면 그 r_ion 은 ≈32 200 · ≈103 800 Ω cm (모형 a 대비 +28 · +64 %) — 원문의 '모형 차 최대 22 %' 와 맞지 않는다 [카드 산술 · 해석].  NCM_70 에서 그 차이를 HFR 로 바꾸면 170.8 → 176.5 Ω cm² (3 %) 이다 [카드 산술] — 위 ×12.3 증폭과 같은 이야기.
- ⇒ 이 논문의 NCM σ_ion 을 인용할 때는 **판본 (그림 6 / 표 S1) 을 적는다**.  Kaiser 의 'τ ≈3 → ≈10' 은 표 S1 판이다 (§3-6).

### 3-6. ★ τ · f 로 바꾸면 (우리 규약 · `kaiser2018_…` 대조)
- 정의: f = σ_eff/σ₀ · **tau2 (수송 tortuosity) = φ σ₀/σ_eff = φ/f** (Kaiser 식 2 의 τ_eff 와 같은 양 [다른 카드 · `kaiser2018_…` §4-1 · 정본 J 절]) · σ₀ = SE 펠릿 5.5 × 10⁻⁴ S cm⁻¹ · φ = 공칭 SE 부피분율.

| 출처 | φ_SE 0.5 | 0.4 | 0.3 | 표지 |
|---|---|---|---|---|
| NCM · 표 S1 | f **0.162** · tau2 **3.09** | f **0.0724** · tau2 **5.52** | f **0.0288** · tau2 **10.4** | [카드 산술] — Kaiser '≈3 → ≈10' 재현 |
| NCM · 그림 6 (b) | 0.135 · 3.71 | 0.0565 · 7.08 | 0.0175 · 17.1 | [카드 산술 · 판독] |
| 흑연 · 그림 6 (a) | 0.104 · 4.81 | 0.0346 · 11.6 | 0.0157 · 19.1 | [카드 산술 · 판독] |
| Bruggeman φ^1.5 (비교) | 0.354 | 0.253 | 0.164 | 표 S1 의 2.2 · 3.5 · 5.7 배 [카드 산술] |

- 아치 꼴 f = φ^n 의 n: 표 S1 **2.63 · 2.87 · 2.95** [카드 산술].
- 같은 φ 에서 흑연이 NCM 보다 1.3–2.1 배 낮다 (판본에 따라) — 원문은 이 차이를 다루지 않고 '꼴이 비슷하다' 만 쓴다 [카드 해석].
- ⚠ φ 기준: 공칭 고체 부피비 (기공 미포함).  펠릿 기공 p 가 있으면 실제 φ_SE = (1 − p) × 공칭 → tau2 도 (1 − p) 배 [카드 산술] — p 는 [미확인].

### 3-7. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① 고주파 반원의 원인 미정 · 두 가설이 거의 같은 곡선 (p.222–223) ② *"a judgment based only on impedance measurements is limited, and some other experiment will be required to interpret the impedance results completely"* (p.223) ③ 조립 그대로 (최저 SOC) 라 R_ct 가 커서 쉬운 경우 — *"a lower charge-transfer resistance makes the analysis more difficult. The model might need to be refined further for the analysis during the charge-discharge process"* (p.223) ④ 유한 길이 Warburg 미포함 — R_ct 가 낮은 전극에는 다듬어야 (p.219) ⑤ T형은 전자 전도도가 비교적 낮은 시료에만 (p.216).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. 그림 6 (b) σ_ion ↔ 표 S1 1/r_ion: −16.8 · −22.0 · −39.1 % (§3-5).
2. '모형 차 최대 22 %' 는 NCM_50 세 모형으로만 확인된다 — 60 · 70 % 의 모형 (b) · (c) 값 미인쇄.
3. K ≤ 0.057 (흑연) 의 σ_e 기준 = 1.0 × 10⁻³ (표 1 의 흑연 값 0.95 S cm⁻¹ 아님) (§3-3).
4. 'underestimation' 은 K < 2 에서만 (NCM_50 은 K = 2.80) (§3-2).
5. 그림 2 캡션 'with electronic resistance' ↔ 내용 = 전자 저항 없음 (§3-2).
6. 'ca. 100 mg' ↔ 표 1 두께 → 상대밀도 ≥ 1 (질량 근사) (§3-1).
7. 표기 · 오식: 식 (14) 글자 α ↔ PDF 글자 층 'a' · *"Oh the other hand"* (p.217) · *"graphte_50"* (p.221) · 그림 7 *"ion-electoron"* · *"these tow models"* · *"each hypotheses"* (p.223) · 감사 *"Industrial Technology Department Organization"* · 참고문헌 **[19] = [27]** (둘 다 C.H. Chen, J. Liu, K. Amine, J. Power Sources 96 (2001) 321) · [7] *"Colclaure"* · [8] *"Phys. Chem. Lett."* · [29] *"Schelder"* (원문 그대로).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **시편 셋**: (i) T형 펠릿 (혼합물만 · 30 MPa · 331–392 µm) → DC (10 mV 10 s) + AC · (ii) Z형 대칭 셀 (SUS | 전극 | SE | 전극 | SUS · 10 → 30 MPa · 전극 ≈49–70 µm · SE ≈700 µm) → AC · (iii) SE 펠릿 → AC HFR.  흑연 = (ii) 만 · NCM = (i) (+ 그림 7 a 의 (ii) 비교).
- **해석**: 흑연 = 그림에서 점근선 두 개를 긋고 교점 − HFR = R_ion/3 (식 7) · NCM = 저주파 반원 꼭대기 아래 자료를 세 줄 T형 TLM (CPE z_B) 에 맞춤 → r_ion · r_e · CPE 둘 (모형 a: 4 개) · 고주파 반원을 포함한 전 범위는 모형 (b) · (c) (7 개).
- **정규화**: r = R·S/L (기하 단면 · 두께) — σ_eff 는 **전극 전체 단면** 기준 (p.217 단위 규약).

### 4-2. 입자 처리 ★
- **입자를 풀지 않는다** — 전극을 **1D 연속 사다리** (*"The model is actually continuous with an infinite number of infinitesimal steps"*, p.216) 로 본다: 이온 줄 · 전자 줄 · 그 사이 계면 (단위 부피 z_B).  입자 모양 · 접촉 · 입계는 줄 저항 안에 뭉친다; 모형 (b) · (c) 는 그중 한 줄을 'bulk + (gb ∥ CPE)' 로 쪼갠 것.
- DEM 처럼 구 · 점접촉을 두는 부분은 **없다**.  다만 원문이 접촉을 말하는 곳은 둘: 서론 *"Contact among the grains of the solid electrolyte might also be a serious problem … Insufficient contact causes a low effective ionic conductivity in the electrode and inhomogeneous discharge in the direction of thickness"* (p.216) · 모형 (b) 의 *"contact resistance between particles"* 가설 (p.222).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계** — **말 없음** (DEM · discrete element · particle simulation 0 회 · 'Discrete points' 는 그림 캡션의 '실험 점' 뜻).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **말 없음** ('plastic' 0 회).  성형은 30 MPa 1 분 · 소성 · 치밀화 언급 없음.  접촉 저항이 전자 저항의 대부분일 수 있다는 가설 (모형 b · 97 %) 이 유일하게 '눌러 만든 분말' 을 언급한다 (p.222).
3. **2D / 3D** — 모형은 **1D** (두께 방향 사다리) · 시료는 3D 펠릿 · 2D → 3D 전이에 대한 말 **없음**.  (자매 이론 Siroma 2015 는 1D object ↔ 3D object 단위 규약을 따로 둔다 — `siroma2015_…` 표 1.)
4. **압력을 뺄 때의 거동** — **다루지 않았다**.  측정 전 재가압 ca. 30 MPa 뒤 측정 · 가압 유지 여부 [미확인] · 압력 의존 측정 없음.

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| TLM (전송선 모델) | 이온 줄 z_A · (전자 줄 z_C) · 계면 z_B 의 무한 사다리를 연속체로 푼 등가회로 — 두 줄 = 전자 저항 0 |
| ion-electron connection (Z형) | 이온 줄 한 끝 ↔ 반대편 전자 줄 끝 단자 — 3 전극 셀 · 대칭 셀 (substrate \| sample \| SE \| sample \| substrate) |
| electron-electron connection (T형) | 전자 줄 양 끝 단자 · 이온 줄 양 끝 열림 — substrate \| sample \| substrate (SUS 둘) |
| HFR · LFR | 고주파 · 저주파 극한의 실수 저항.  T형 HFR = R_ion R_e/(R_ion + R_e) · LFR = R_e |
| 물방울 (teardrop) | T형 의 저주파 꼴 — 반원 + 45° 선.  두 실수 끝 = HFR · LFR |
| 폭 (width) | Z형 에서 저주파 극한 − 고주파 극한 = (1/3) R_ion (전자 저항 0) |
| α · K | 식 (7) 로 얻은 r_ion ÷ 참 r_ion · K = r_e/r_ion (식 14–15) — 이 논문의 α 는 Bruggeman 지수 · CPE 지수와 다른 기호 |
| CPE | 상수 위상 소자 z_B = 1/((jω)^ψ c_dl\*) — ψ = 1 이면 축전기 |
| r_ion,gb · r_e,gb | 줄 저항 중 CPE 와 병렬인 몫 (고주파 반원) — 입계 · 입자 간 접촉 가설 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **그래픽 초록** (`fig_GA.png`) | 기판 사이 전극 혼합층 (이온 전류 · 전자 전류 그림) → T형 세 줄 TLM → 물방울과 두 끝 표기 | 측정 · 해석 한 장 요약 (발표 · 실험 동료 전달용) |
| **그림 1** (`fig_1.png`) | (a) 두 줄 TLM (b) 세 줄 Z형 (ion-electron) (c) 세 줄 T형 (electron-electron) 사다리 | ★ 연결형 그림 — 우리 실험 앵커의 셀 구성을 적을 때 |
| **그림 2** (`fig_2.png` · `fig_2a–c`) | 두 줄 TLM 의 나이퀴스트: (a) r_ion 10 · 15 · 20 kΩ cm (b) r_ct⁻¹ 0 · 10 · 20 mS cm⁻³ (c) ψ 1 · 0.9 · 0.8 · 화살표 = (1/3) r_ion L (캡션 낱말 '…with electronic resistance' 는 오기로 보임) | 식 (7) 이 무너지는 꼴 (R_ct · CPE) |
| **그림 3** (`fig_3.png` · `fig_3a` · `3b`) | 같은 r_ion 에서 r_e 0 · 5 · 10 · 15 kΩ cm: (a) Z형 = HFR 이 0 이 아니고 폭이 좁아짐 (b) T형 = 물방울이 커짐 | ★ (b) 물방울 두 끝 = 식 (17)–(18) — 벡터 판독으로 재현 |
| **그림 4** (`fig_4.png` · `fig_4a–d`) | r_ct · CPE 일그러짐: Z형 (a)(c) ↔ T형 (b)(d) — T형 은 LFR 이 거의 안 움직임 | T형 이 덜 민감하다는 근거 · r_ct 직류 효과 500 → 481 Ω cm² |
| **그림 5** (`fig_5.png`) | graphite_50 Z형 대칭 셀 (÷2) · 점근선 둘 · 1 kHz · 100 Hz 표지 | 식 (7) 실례 — HFR 64.5 · 교점 106.5 Ω cm² [판독] |
| **그림 6** (`fig_6.png`) | ★ log σ vs AM vol%: (a) 흑연 σ_ion (b) NCM σ_ion (c) NCM σ_e · 0 % = SE 펠릿 | ★ 조성 축 σ_ion · σ_e — (b) 는 표 S1 과 다름 (§3-5) |
| **그림 7** (`fig_7.png`) | NCM_50: (a) Z형 (밋밋) (b) T형 (두 반원) | 같은 시료에서 연결형이 정보량을 가른다 |
| **그림 8** (`fig_8.png` · `fig_8a–c`) | NCM_50 T형 맞춤: (a) 구조 없음 (저주파만) (b) 전자 줄 구조 (c) 이온 줄 구조 | 고주파 반원 처리 = 모형 의존 22 % |
| **SI 그림 S1** (`fig_S1.png` · `fig_S1a–c`) | NCM_60 · NCM_70 T형 맞춤 · (c) = (b) 확대 | NCM_70 물방울 폭 15 Ω cm² — 이온값의 취약점 |
| **SI 그림 S2** (`fig_S2.png`) | 모형 (b) · (c) 를 Z형으로 계산 (밋밋 · 서로 비슷) | 임피던스만으로는 모형을 못 가른다 |
| **표 1** (`tab_1.png`) · **표 S1** (`tab_S1.png`) | DC 전도도 · 두께 / 모형 (a) 맞춤값 | §3-1 · §3-4 |
| 식 크롭 18 (`eq_01`–`eq_18`) · 근거 문단 19 (`txt_p*`) | 셀 구성 (1)–(3) · 식 (4)–(18) · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **흑연 (Z형)**: 나이퀴스트에서 고주파 45° 선과 저주파 선의 **점근선 교점** − HFR (전해질 층) = R_ion/3 → σ_ion = L/R_ion (식 7) · 대칭 셀은 ÷2.
- **NCM (T형)**: 저주파 반원 꼭대기 아래 자료 (NCM_50 0.01–0.35 Hz) 를 **식 (16) + CPE z_B** 에 Excel Solver (상대 편차 제곱합) 로 맞춤 → r_ion · r_e · cpe_dl · ψ · σ = 1/r.
- **DC**: 10 mV · 10 s 전류 → 기하 크기로 σ_e (거친 어림).
- **비교**: 흑연 σ_ion 곡선과 NCM σ_ion 곡선의 꼴 일치를 '저주파 반원 = TLM' 귀속의 근거로 씀 (그림 6).
- **판독 (이 카드)**: 그림이 벡터라 PyMuPDF get_drawings 로 표지 중심 · 꺾은선 꼭짓점 · 맞춤선 끝을 직접 읽음 · 축 = 그림 틀 pt ↔ 눈금 · digitized.csv note 열에 방법 전부.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md 출처를 병기)

### 7-1. 비교표 (모든 행에서 **재료 · 성형압 · 조성 · 정의가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 복합체 σ 의 정규화 | σ_eff = 1/r · r = R·S/L (**전극 전체 단면**) | 접촉망 σ_full = **전체 단면 정규화** (`network_conductivity.py` · 정본 J 절) [우리] | **같은 정규화** — 비교 가능한 꼴 (값은 아님) |
| 이온 · 전자 채널 | TLM 두 줄 (이온 r_ion · 전자 r_e) + 계면 z_B — DC 극한에서 두 줄이 갈라진다 (LFR = R_e) | 망 · 복셀 모두 이온 · 전자 채널을 **따로 DC** 로 푼다 [우리] | 우리 채널 σ 는 TLM 의 **1/r_ion · 1/r_e 자리** (줄 저항 = bulk + 입계 · 접촉 전부) |
| 접촉 · 입계 몫 | 고주파 반원 = 전자 줄 gb 97 % (모형 b) **또는** 이온 줄 gb 97 % (모형 c) — 못 가름 | ps45 Hertz 망: 수송 tortuosity 의 73–75 % = SE–SE 접촉 협착 [우리 · CLAUDE.md 10-13] · 복셀 STEP3 = CONTACT_FREE (Holm 항 0 · CL-81) [우리] | **같은 질문** (접촉 · 입계가 줄 저항을 지배하는가) · 이 논문은 30 MPa · 유리 SE · 무탄소 — 크기 대조 불가 |
| σ_ion 조성 의존 | NCM: f 0.162 → 0.0288 (φ_SE 0.5 → 0.3 · 공칭) · tau2 3.09 → 10.4 [카드 산술] | ps45 Hertz tau2 **5.03–7.24** · σ_ion (σ₀ 1.5) 0.0587–0.0893 mS/cm [우리 · CLAUDE.md] | **다른 계** (유리 SE 25.5 µm · 30 MPa ↔ LPSCl ≈1 µm · 압밀) — 숫자 대조 아님 · 방향 (SE 줄면 f 가 φ 보다 빨리 떨어짐 · 아치 n ≈2.6–2.95) 만 |
| σ_e 조성 의존 | DC σ_e ∝ φ_AM^≈5 (50 → 100 % · 지수 4.97 · 50 → 70 % 5.13 [카드 산술]) · σ_e(50 %)/σ_e(100 %) = 0.032 | Stage 22.5 σ_e ∝ **φ_AM⁴** (잠금 · 코퍼스 φ_AM 0.37–0.88 · φ_AM < 0.3 외삽 금지) [우리 · CLAUDE.md] | 지수 크기 감각만 — 이 논문 = **무탄소** · NCM523 · LiNbO₃ · 30 MPa · 공칭 고체 φ (우리 = 상자 기준 φ · 탄소 · AM 크기 분포) |
| AM 압분체 σ_e | NCM523 (LiNbO₃) 100 % 압분체 **1.0 × 10⁻³ S cm⁻¹** (30 MPa · 870 µm · 조립 그대로 · DC) | NCM811 측정 4.1–5.2 mS/cm (원장 CL-92) · 모델 기준 σ_AM 50 mS/cm [우리 · CLAUDE.md] | **랩 표준과 다른 문헌 값** · 재료 (523 ↔ 811) · 코팅 · 압력 · SOC 다름 — 같은 표에 넣지 않는다 |
| SE 펠릿 σ₀ | 75Li₂S·25P₂S₅ 펠릿 **5.5 × 10⁻⁴ S cm⁻¹** (25 °C · 성형 [미확인]) | σ₀ 보고 **1.5** · 풀이기 3.0 mS cm⁻¹ (펠릿 · CL-91) [우리] | 다른 SE — tau2 를 견주기 전 σ₀ 기준을 맞춘다 (정본 J 절) |
| 진밀도 | 가정 SE 1.90 · NCM 4.72 · 흑연 2.26 g cm⁻³ | 랩 표준 LPSCl **1.64 g/cm³** (고정 · 판정 대상 아님) [우리] | 랩 표준과 다른 문헌 값 (유리 SE) |

### 7-2. ★ 연결형 · 오차 기준을 우리 실험 앵커에 대면 (흐름 밖: Rint ② · σ_e 앵커)
- 우리 σ_e 앵커 = **DC 분극** SBE 1.63 · DBE 4.68 mS/cm (10-16 · kgy) · 이온 σ₀ 앵커 = Bazzoun 2026 CAM 70 wt% EIS 0.137 mS/cm [우리 · CLAUDE.md].  이 둘로 K = σ_ion/σ_e ≈ **0.029–0.084** [카드 산술 · 다른 시편의 값을 섞은 어림].
- 그 K 에서: Z형 + 식 (7) 의 σ_ion 오차 α = **0.94 (DBE) · 0.85 (SBE)** → 전자 저항을 무시하면 이온 저항을 6–15 % 낮게 읽는다 [카드 산술 · 식 14] · T형 물방울 폭 = R_e·K/(1+K) = R_e 의 **2.8–7.8 %** → T형 으로 이온을 재기엔 물방울이 너무 작다 (이 논문의 NCM_70 (K 0.089) 이 바로 그 경계 — 폭 8 % · HFR 오차 ×12 증폭) [카드 산술].
- ⇒ 우리 탄소 첨가 복합체는 원문 분류로 **'전자 저항이 작은 쪽'** — 이온은 Z형 (대칭 셀) + K 보정 (식 14), 전자는 DC (이 논문에서 AC LFR 과 1–2 % 안) 가 맞는 짝이다 [카드 해석].  탄소 없는 펠릿 (예: bong2023 의 Siroma 법 펠릿) 이면 T형 이 맞다.

### 7-3. τ 규약 (CLAUDE.md 2026-10-03 · "tortuosity factor = τ² (tau2) 에만")
- 원문에 τ 가 없다.  Kaiser 의 'Siroma τ' 는 **tau2 (수송 tortuosity)** 자리 (τ_eff = ε σ₀/σ_eff · 제곱근 아님) — 보고 · 덱에 옮길 때 이름 = **수송 tortuosity** · σ₀ = SE 펠릿 5.5 × 10⁻⁴ · φ = 공칭 고체 SE 부피분율 (기공 0 기준) 을 함께 적는다.
- 원문 r_ion 은 TLM 이온 줄 비저항 z_A 하나다 — 균질 1D 면 Z형 (대칭 셀 · 저주파 (1/3) R_ion · 식 7 = 정본 J 표 τ_e 행의 'Siroma Z/E형 L·z_A/3') 과 T형 (식 18 HFR · 고주파 = 두 줄 병렬) 이 **같은 z_A** 를 준다 (정본 J 절 10-03 메모 · `siroma2015_…` 표 2–4).  두 길이 갈리는 것은 균질 가정이 깨질 때이고, 이 논문에서는 그것이 고주파 반원의 맞춤 모형 차 (22 %) 로 나타난다 [카드 해석].  ⇒ τ 를 옮길 때 **연결형 (Z · T) · 맞춤 모형** 을 함께 적는다 (J 절 규칙).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **수송의 측정 · 해석 쪽** (복합체의 이온 · 전자 유효 전도도를 한 셀에서) — 우리 분업의 DEM 쪽 (접촉망 σ · 이온 / 전자 채널) 의 **실험 대조 짝**.
- 없는 반쪽: 압밀 (30 MPa 하나 · 기공 없음) · 미세구조 (영상 · 접촉 수 없음) · 기계 · 탈압 · 입자 모델 전부.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = 75Li₂S·25P₂S₅ 유리 + NCM523 (LiNbO₃) / 흑연 · 무탄소 — **계가 다르고** 압밀 · 기계 자료가 없다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 반면교사 둘 — ① **조성 vol% 가 가정 진밀도로 맞춘 고체 비** 이고 펠릿 기공이 없다 → 문헌 f · tau2 를 등록할 때 **φ 기준 (고체 / 상자) 칸**을 둔다 (기공 p 면 tau2 가 (1 − p) 배) ② **같은 양의 판본 둘** (그림 6 ↔ 표 S1, 70 % 에서 1.64 배) → 결과 전 대조 항목에 **그림 / 표 판본 · 맞춤 모형**을 같이 적는다 | 압력별 기공 · 진밀도 기공 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (순수 SE 기공 · 항복 없음).  SE 펠릿 σ 5.5 × 10⁻⁴ (성형 [미확인]) 만 | 맞춤 표적 아님 |
| **단계 5** (3D 복합 압밀) | 없음 (성형 30 MPa 하나 · 기공 없음) | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ **수송 결과 전 대조 (방향 · 꼴)**: 같은 펠릿에서 σ_ion (SE ↓ 에 f ∝ φ^≈2.6–2.95) 과 σ_e (AM ↑ 에 ∝ φ_AM^≈5) 가 반대로 움직이고 NCM 60 % 근처에서 엇갈린다 (σ_ion = σ_e 교차 [카드 해석 · 그림 6]) · ★ **측정 규칙**: 연결형 (Z · T) · 오차 기준 α(K) · AC LFR ≡ DC (1–2 %) · 고주파 반원은 모형 의존 (22 %) | 절대값 (계가 다름) · 미세구조 · 피복 · 접촉 수 없음 |
| **후보 D0** (지금 DEM) | 망 이온 · 전자 채널 σ 의 실험 쪽 정의 (줄 저항 = bulk + 입계 · 접촉 · 전체 단면 정규화) — 우리 FULL (Holm 포함) 이 견줄 자리, CONTACT_FREE 는 아님 | 같은 재료 · 압력의 값 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 (압밀 없음).  다만 TLM 자체가 '균질화 1D 수송 모델' 이라 균질화 수송 쪽 (유효 매질) 의 측정 짝 | 압밀 맞춤 표적 아님 |
| **U0–U6** | 기계 단위 시험 없음.  **흐름 밖 수송 단위 시험** (아래 §9-3): 식 (16)–(18) · 식 (16) + z_B = r_ct 의 직류값 (500 / 490.1 / 481.1 Ω cm²) = 우리 두 채널 + 계면 풀이기 (STEP4 선형 BV) 의 해석 검산 | U0–U6 해당 없음 |
| **R1–R7** | 없음 — 고주파 반원의 '입자 간 접촉 저항' 가설 (모형 b) 은 R2 (미끄럼 · 분리) · R3 (입자 경계 기억) 의 수송 쪽 결과와 닿지만 자료가 못 가른다 | — |
| **결과 전 대조 항목** | ① (방향) SE 부피비 0.5 → 0.3 에 f 가 Bruggeman (φ^1.5) 보다 2.2 → 5.7 배 빨리 떨어진다 (표 S1 · 공칭 φ) ② (방향) σ_e 가 AM 부피비에 φ^≈5 로 오른다 (무탄소) ③ (측정) AC LFR = DC σ_e (1–2 %) — 맞추는 데 쓰지 않음 | 우리 LPSCl · NCM811 · 탄소 계와 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: SE = 75Li₂S·25P₂S₅ 유리 (LPSCl 아님 · 25.5 µm) · AM = NCM523 LiNbO₃ (11.6 µm) / 흑연 · 무탄소 · 무바인더 · **30 MPa** 성형 (우리 300 MPa 급) · 공칭 고체 vol% · 25 °C · 조립 그대로 (최저 SOC) · 1D 모형 · 3D 시료.

## 9. 적용 인사이트 (행동)
1. **연결형을 먼저 적는다 (흐름 밖: 실험 앵커 · Rint ②)**: 우리 이온 · 전자 앵커를 받을 때 셀이 Z형 (대칭 셀 · 3 전극) 인지 T형 (집전체 | 시료 | 집전체) 인지 · DC 인지 AC 인지를 결과 칸 옆에 둔다 — 같은 시료가 연결형에 따라 '밋밋' (그림 7 a) ↔ '두 반원' (7 b) 이 된다.
2. **K = σ_ion/σ_e 로 방법을 고른다**: K ≪ 1 (탄소 첨가 · 우리 SBE/DBE 어림 0.03–0.08) → 이온은 Z형 + 식 (14) 보정 (α 0.85–0.94), 전자는 DC.  K ~ 0.4–3 (무탄소 펠릿) → T형 이 둘 다 준다.  K 가 0.7 근처면 식 (7) 만 쓴 이온값이 최대 54 % 낮다 (α 0.464) [카드 산술].
3. **수송 풀이기 해석 검산 (흐름 밖: STEP4 · 망 결합)**: 균질 1D 막대에 이온 · 전자 두 줄 + 계면 저항 (선형 BV 의 r_ct) 을 두고 우리 풀이기의 직류 단자 저항을 식 (16) (z_B = r_ct) 의 직류값과 비교 — 예: L 0.5 mm · r_ion = r_e = 10 kΩ cm · r_ct⁻¹ 0 / 10 / 20 mS cm⁻³ → **500 / 490.1 / 481.1 Ω cm²** (그림 4 b 벡터 판독 500.0 / 490.2 / 481.1 과 일치) [카드 산술 · 판독].  Z형 직류 극한 (식 10, z_B = r_ct) 도 같은 방식.
4. **문헌 σ_ion 인용 꼬리표**: 'TLM 맞춤 · 모형 (a)/(b)/(c) · 그림 / 표 판본 · 공칭 φ · σ₀ (SE 펠릿) · 성형압 · SOC' — 이 논문은 같은 시료 σ_ion 이 판본 · 모형에 따라 22–64 % 흔들린다.
5. **Kaiser 'Siroma τ' 를 쓸 때**: '원문 τ 아님 · Siroma 표 S1 + Kaiser 식 2 · 공칭 고체 φ · σ₀ 5.5 × 10⁻⁴' 를 함께 적는다 · 그림 6 판이면 3.7 → 17 (§3-6).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For sulfide-glass (75Li₂S·25P₂S₅) composite electrodes with low electronic conductivity, impedance measured between two electronically conducting current collectors (substrate | sample | substrate; the 'electron-electron', i.e. T-type, connection of a three-rail transmission-line model) yields both effective conductivities from the two real-axis limits of the low-frequency teardrop, R_ionR_e/(R_ion + R_e) and R_e (Siroma et al., *J. Power Sources* 316 (2016) 215–223)."
- "In that study the AC electronic conductivity (1/r_e) agreed with the DC value of the same pellet within 1–2 %, whereas the ionic value depended on the fitted model by up to 22 % (Siroma et al., 2016)."
- 국문 (한정어와 함께): *"Siroma 2016 은 τ 를 내지 않았다 — 'ε 0.5 → 0.3 에서 τ ≈3 → ≈10' 은 Kaiser 2018 이 Siroma 의 표 S1 (NCM523 · 75Li₂S·25P₂S₅ 유리 · 30 MPa · 공칭 고체 부피비) 과 SE 펠릿 5.5 × 10⁻⁴ S cm⁻¹ 로 계산한 수송 tortuosity (= φσ₀/σ_eff) 이며, 같은 논문의 그림 6 으로 계산하면 ≈3.7 → ≈17 이다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-7 의 ①–⑤.
**카드가 본 한계**
1. **기공 · 진밀도 미보고** — vol% = 가정 진밀도 고체 비 · 'ca. 100 mg' 로는 계산 불가 · 30 MPa 펠릿 (같은 조성 순수 유리는 다른 카드 판독으로 ≈50 % 상대밀도) → f · tau2 의 φ 기준이 흔들린다.
2. **판본 · 모형 의존** — 그림 6 (b) ↔ 표 S1 (−39 % @ 70 %) · 모형 (a)(b)(c) 22 % · 60 · 70 % 모형 (b)(c) 미인쇄.
3. **NCM_70 이온값의 취약성** — 물방울 폭 15 Ω cm² · HFR 1 Ω cm² 오차가 R_ion 7 % (×12.3).
4. **재료 · 상태** — 유리 SE · NCM523 · 무탄소 · 30 MPa · 최저 SOC · 25 °C — LPSCl · NCM811 · 탄소 · 300 MPa 급 계로 절대값 전이 0.
5. **흑연 쪽 두께 · K 기준** — 전극층 두께는 'ca. 70 µm' 뿐 · K ≤ 0.057 의 σ_e 기준 1.0 × 10⁻³ 출처 없음.
6. **고주파 반원** — 원인 미정 · '입자 간 접촉 저항' 은 가설 (모형 c 도 같은 곡선).
7. **식 (14) 의 '과소'** — K < 2 에서만 (NCM_50 K 2.80 은 과대 쪽).
8. **측정 중 압력 · SE 펠릿 성형 조건** [미확인].

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [23] | Z. Siroma, N. Fujiwara, S. Yamazaki, M. Asahi, T. Nagai, T. Ioroi, Electrochim. Acta 160 (2015) 313. | 식 (10) · (16) · Z / T 연결형 이름의 원전 — ✅ 정본 카드 `siroma2015_…` |
| [24] | Z. Siroma, T. Ioroi, Electrochemistry 83 (2015) 425. | *"few reports about the behaviors of their Nyquist plots depending on the ionic and electronic resistance [24]"* — 전자 저항 있는 TLM 의 나이퀴스트 꼴 (제목은 원문 목록에 없음) — 카드 없음 |
| [10] | N. Ogihara, S. Kawauchi, C. Okuda, Y. Itou, Y. Takeuchi, Y. Ukyo, J. Electrochem. Soc. 159 (2012) A1034. | 대칭 셀 + TLM 으로 유효 이온 전도도 (액체) — 이 논문이 출발점으로 삼은 방법 · τ_e 계보 — 카드 없음 (landesfeind2016 · 2018 · malifarge2017 · pouraghajan2018 카드가 인용만) |
| [6] | T. Takeuchi, H. Kageyama, K. Nakanishi, T. Ohta, A. Sakuda, T. Sakai, H. Kobayashi, H. Sakaebe, K. Tatsumi, Z. Ogumi, Solid State Ion. 262 (2014) 138. | 전극 혼합층의 AM–전해질 접촉 문제 (서론의 인용처 · 같은 AIST 그룹) — 카드 없음 |
| [31] | X. Ren, P.G. Pickup, J. Electroanal. Chem. 420 (1997) 251. | 식 (12) · (13) 극한값의 출처 — 카드 없음 |
| [13] · [14] | M.C. Lefebvre, R.B. Martin, P.G. Pickup, Electrochem. Solid-State Lett. 2 (1999) 259. · R. Jiang, C.K. Mittelsteadt, C.S. Gittleman, J. Electrochem. Soc. 156 (2009) B1440. | 식 (7) '(1/3) R_ion = 폭' 의 인용처 [13,14] (원문 p.216) — 둘 다 카드 없음 |
| [21] · [22] · [15] | Bisquert 외 Electrochem. Commun. 1 (1999) 429 · Tröltzsch · Kanoun Electrochim. Acta 75 (2012) 347 · Bisquert 외 J. Phys. Chem. B 104 (2000) 2287 | TLM 일반해 계보 — siroma2015 카드가 인용 · 카드 없음 |
| [19] = [27] | C.H. Chen, J. Liu, K. Amine, J. Power Sources 96 (2001) 321. | 원문 목록에 **두 번** 실림 (대칭 셀 [19] · LIB 의 CPE [27]) |

## 13. [미확인] 목록 (본문 9 쪽 + SI 4 쪽 전수에 없음)
1. 펠릿 질량 (정확값) · 밀도 · 기공 · 진밀도 측정 (가정값만).
2. 측정 중 가압 유지 여부 · 그 압력.
3. SE 펠릿 (σ 5.5 × 10⁻⁴) 의 성형압 · 두께 · 지름.
4. 흑연 전극층의 시료별 두께 · graphite_60 · 70 의 σ_e.
5. NCM_60 · NCM_70 의 모형 (b) · (c) 맞춤값 · 맞춤 주파수 범위 (NCM_50 만 0.01–0.35 Hz).
6. 그림 6 (b) 가 어느 모형 값인지 (본문 = 모형 a · 판독 = 50 % 는 모형 b 값).
7. K ≤ 0.057 에 쓴 σ_e 1.0 × 10⁻³ 의 출처.
8. 반복 시편 수 · 오차 막대.
9. [24] 의 제목 (원문 목록에 없음).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 본문 9 쪽 + SI 4 쪽을 글자 층 추출 + 전 쪽 렌더로 읽음.  서지 = p.215 (제목 · 저자 6 명 · 소속 · 접수일 · DOI · 쪽 머리 "Journal of Power Sources 316 (2016) 215–223") · SI p.1 = 같은 제목 · 저자 · 소속.  낱말 셈 (본문 · 대소문자 구분): 'tortuos' 0 · 'porosity' 0 · 'plastic' 0 · 'DEM' 0 · 'Au' 0 · 'SUS' 3 · 'MPa' 4.
- 그림 크롭 **65 장** = 도구 12 (그림 1–8 · 표 1 · 그림 S1 · S2 · 표 S1 — **다시 자름 3**: tab_1 (쪽 전체) · tab_S1 (그림 S1 c 와 캡션 섞임) · fig_S1 (패널 c 만 → SI 2 · 3 쪽 이어 붙임)) + 손 크롭 53 (그래픽 초록 · 패널 15 · 식 18 · 근거 문단 19).  본 뒤 다시 렌더 = fig_2a · 2b (x 축 글자 잘림 → 이웃 패널 '600' 경계까지) · fig_2c (위 두 패널 x 축 글자 섞임) · 근거 문단 2 (이웃 문단 줄 끝 섞임).  65 장 전부 Read 로 열어 확인.
- 판독: digitized.csv 56 행 — 벡터 좌표 (그림 틀 pt ↔ 눈금) · 그림 3 b · 4 b 곡선 끝이 식 (16)–(18) 계산값과 0.2 Ω cm² 안 · 그림 6 (a) 50 % 가 인쇄 5.7 × 10⁻⁵ · 0 % 가 5.5 × 10⁻⁴ · (c) 가 표 1 DC 를 재현 → 축 보정 확인 · 그림 6 (b) 만 표 S1 과 다름 (§3-5).
- 2 차 인용 대조: kaiser2018 (L157 · L393) · jung2019 (L218 · L415 · L433) · asano2017 (L149 · L151 · L323 · L348) · siroma2015 (L549) · bong2023 (L706 · L769) · otani2023 · hlushkou2018 · kato2018 · minnmann2021 · kawaguchi2026 — 고치지 않았다 (카드 문제 = 정독 출력 batch_125 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (jpowsour.2016.03.059) · '316 (2016)' · '316, 215' · 'electrode mixture layers' · 'siroma' grep — 카드 없음 (인용만 10 장 · `siroma2015_…` = 다른 논문 · 다른 해) (2026-11-16).

## 🔗 관련 카드
- 이론 원전 · TLM 해석해: `siroma2015_transmission_line_model_porous_electrode_impedance` · `cooper2017_simulated_impedance_diffusion_porous_media` · `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` · `landesfeind2016_tortuosity_eis_electrodes_separators` · `landesfeind2018_tortuosity_impedance_vs_tomography` · `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` · `nguyen2020_electrode_tortuosity_factor`.
- 황화물 ASSB 복합 전극 임피던스 · 이온 / 전자 분리: `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` · `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` · `minnmann2021_jes_charge_transport_bottlenecks` · `bong2023_linbo3_thickness_uniformity_ncm523` · `otani2023_ionic_conductivity_path_resistance_separation_model` · `kawaguchi2026_se_size_soc_dependent_cathode_resistance` · `kim2025_impedance_decoupling_tlm_assb` · `interfacial_impedance_formulation_assb_cathode` · `koenig2023_wet_milling_se_ion_tortuosity_composite_cathode` · `islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell` · `ketter2025_resistor_network_models_predict_transport_properties`.
- 같은 조성 유리 (75Li₂S·25P₂S₅) 의 압밀 · σ: `sakuda2013_sulfide_mechanical_property`.
- 🔗 **관련 카드 (2026-11-16 한 줄 추가)**: [`sakuda2016_se_particle_size_electrode_morphology_ncm111_li2s_p2s5_cracking`](sakuda2016_se_particle_size_electrode_morphology_ncm111_li2s_p2s5_cracking.md) — 같은 해 · 같은 AIST 그룹 (공저자 T. Takeuchi) · 같은 75Li₂S·25P₂S₅ 유리 + LiNbO₃ 코팅 NCM (그쪽은 NCM111 · 무탄소 · 75 : 25 wt · 330 MPa) — SE 입경 (d50 16 vs 3.8 µm) 이 단면 분포 · NCM 균열 · 율속에 주는 영향 (σ 측정 없음 · 단면 정성).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
