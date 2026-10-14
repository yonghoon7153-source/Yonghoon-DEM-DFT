<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = lee2025_heckel_argyrodite_powder_densification_nanoindentation.md · miss2026_insitu_conductivity_porosity_pressure_compaction.md.
     쪽 표기 = 논문 인쇄 쪽 "n of 18" = PDF 쪽 n (p.1–18).  ⚠ SI (Figure S1–S7 · Table S1) 는 이 PDF 에 없다 — 우리 미확보.
     값 표지: [인쇄] = 본문 · 표 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (경향 전용 — 정밀도 주장 금지) ·
     [우리 산술] = 이 논문 값 + 이 논문 밖 값 (정본 카드 · 우리 문서) 으로 한 계산 · [추정] = 우리 해석 ·
     [미확인] = 본문에 없음 — SI 를 못 봤으므로 "원문에 없다" 로 쓰지 않는다.
     원문 18 쪽 전부 텍스트 층 (PyMuPDF · pdftotext) + 그림 10 · 표 7 을 300 dpi 렌더로 읽었다.  그림은 전부 래스터 (원 해상도 300 dpi). -->
# 황화물 전고체전지 코인셀 (CR2032) 조립 · 시험의 4 기관 round robin — Li₆PS₅Cl (NEI "LPSCl fine" ≈1 µm) 펠릿 100 mg · ⌀10 mm · 360 MPa → 겉보기 밀도 1.49–1.60 g/cm³ ("crystallographic 1.64" 기준 상대밀도 > 90 % — 결정학 산술 1.86 이면 80–86 %, porosity 14–20 %) · σ_ion 0.3–0.4 mS/cm (SS · Al/C 차단 전극, 4 기관) ↔ 1.0–1.8 mS/cm (Al/C co-press) · Li 대칭 175 – > 200 h · CCD 200 µA/cm² · NMC90505 전지 C/20 102–144 mAh/g — Beutl · Orue · López-Aranguren · Pitillas Martinez · Braga · Kekkonen · Tron (Electrochem. Sci. Adv. 2024)

> slug `beutl2024_round_robin_coin_cell_sulfide_assb` · DOI `10.1002/elsa.202400004` · type `experiment (interlab round robin · CR2032 coin cell · EIS impedance (SS · Al/C 차단 전극 · Li 대칭) · DC 분극 · powder cold-press 펠릿 겉보기 밀도 · porosity · electrode contact · 전지 시험 · 시뮬레이션 없음)` · PDF `main.pdf` · digested `2026-10-14` · status ✅
>
> **저자 (7 인 · p.1 인쇄 순서)**: Alexander Beutl¹ · Ander Orue²‡ · Pedro López-Aranguren² · Andrea Itziar Pitillas Martinez³ · Maria Helena Braga⁴ · Ville Kekkonen⁵ · Artur Tron¹‡ — ‡ *"Artur Tron and Ander Orue - equal contribution in this work"* · 교신 = **Artur Tron · Alexander Beutl** (AIT) · **Ander Orue** (CIC energiGUNE).
> ¹ AIT Austrian Institute of Technology GmbH, Center for Low-Emission Transport, Battery Technologies (Vienna) · ² CIC energiGUNE, Basque Research and Technology Alliance (Vitoria-Gasteiz) · ³ Avesta Battery & Energy Engineering (ABEE, Diegem, Belgium) · ⁴ University of Porto, Engineering Physics Dept. · ⁵ Pulsedeon Ltd (Ii, Finland).
> *Electrochemical Science Advances* **2024**, 4, e2400004 (Research Article · 18 쪽 · 호 6 = PDF 쪽 여백 Wiley 다운로드 띠 "26985977, 2024, 6") · 접수 2024-01-21 · 수정 2024-03-15 · 승인 2024-03-18 · CC BY-NC-ND · Horizon Europe grant 101069686 (PULSELiON) [인쇄 p.1 · p.16].
> **PDF**: 묶음 10-14b `pdf_rr/main.pdf` (본문 18 쪽 · SI 없음).
> **이웃 카드 (링크만)**: [`ohno2020_interlab_ionic_conductivity_argyrodite`](ohno2020_interlab_ionic_conductivity_argyrodite.md) (= 이 논문 ref [63] · 같은 "round robin" 장르 · 이론밀도 1.86) · [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) · [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) (NEI LPSCl · 370 MPa · 1.522 g/cm³) · [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) (TD 1.64 의심 §3-4) · [`frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure`](frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure.md) (같은 이름 NEI "fine" 진밀도 1.87 · x50 17 µm) · ⏳ 같은 묶음 10-14b `tron2023_lpscl_ccd_ambient_pressure` (= 이 논문 ref [15] · 0.2 MPa 의 출처 · 정본 미등록 — 이름만).

---

## 0. 결론 먼저 — 우리 질문 (10-14b ①–⑤) 에 대한 답

**한 문장**: 같은 NEI Li₆PS₅Cl 분말 · NMC90505 · C65 · Li 박을 네 기관 (대학 1 · 연구소 2 · 산업체 1) 에 나눠 보내 같은 지시서로 **CR2032 코인셀 (작동 압력 ≈0.2 MPa — ref [15] 인용)** 을 만들어 잰 round robin 이다 — 저자 결론은 *"parameters for the electrolyte, like the ionic conductivity, are rather reproducible, others, like cell performance or cycling stability are not"* (p.16).
우리에게 값진 것은 그 결론보다 둘이다: **(i)** 펠릿 상대밀도의 분모 **"crystallographic density of Li6PS5Cl is 1.64 g cm−3" [10,37]** (p.9) 가 결정학 산술 (Z = 4 · a ≈ 9.86 Å → **1.86 g/cm³**) 과 12 % 어긋난다 — 정본 litdb 에서 1.64 를 인쇄한 카드들 가운데 **"결정학" 라벨과 인용 번호가 함께 붙은 첫 사례** (정본 grep 기준 · §3-3) · **(ii)** 같은 펠릿을 **전극 접촉 규약만 바꿔** 재면 σ_ion 이 0.3–0.4 → 1.0–1.8 mS/cm 로 움직인다 — **기관 차 (×1.33) 보다 규약 차 (×2.5–5.5) 가 크다** (Table 2 · p.9).

| 우리 질문 (10-14b) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① SE 진밀도 1.64 의 출처 | **라벨 = "crystallographic"** (두 번: p.5 [37] · p.9 [10,37]) · **측정 없음** (비중병 · 기체 없음 — 펠릿은 질량 / 기하 부피 겉보기 밀도만) · 격자상수 정련 없음 (XRD 를 Li₇PS₆ JCPDS 34-0688 카드와 대조만) · [37] = Zhou … Nazar, *ACS Energy Lett* 2019, 4, 265 · [10] = Tron, Hamid, Zhang, Beutl, *Nanomaterials* 2023, 13, 327 — **두 원문 미확보 → 1.64 의 계산 근거 [미확인]** · 결정학 산술 1.859–1.860 g/cm³ (Z 4 · a 9.8591–9.8614 Å) → **1.64 는 결정학 밀도가 아니다** (a 10.28 Å 이어야 1.64) · 같은 이름 NEI "fine" 진밀도 1.87 (Frankenberg 2025) · Ohno 2020 비중병 1.874 · Ohno 랩 D 펠릿 기하 밀도 1.655 > 1.64 | [인쇄] p.3 · p.5 · p.9 · [우리 산술] §3-3 |
| ② 펠릿 제작 · 측정 조건 | NEI "LPSCl fine" · "∼1 µm particle size" (D50 [미확인]) · **100 mg · ⌀10 mm 경화강 다이 · 360 MPa · 3 min (본문) / ">2.9 tons for 2 mins" (Fig 4) · 실온 냉간 · Ar** · hot press 없음 · 두께 ≈0.8 mm = **다이에서 꺼낸 뒤** 자유 펠릿 (측정 도구 [미확인]) · 겉보기 밀도 "1.6–1.50" (p.5) / "at least 1.49" (p.9) g/cm³ · 상대밀도 >91 · >94 · >93 · >93 % (Table 2, 1.64 기준) · 공극 숫자 없음 → **ε = 2.4–9.1 % (TD 1.64) ↔ 14.0–19.9 % (TD 1.86)** | [인쇄] p.3–5 · p.9 · Fig 4 · [우리 산술] §3-2 |
| ③ σ_ion ↔ 압력 · 온도 | **압력 · 온도 계열 없음** (성형 360 MPa 한 값 · bilayer 예압 50 MPa · 측정 25 °C 한 값 · Ea 없음) · 측정 중 압력 = 코인셀 ≈0.2 MPa ([15] 인용) · 봉합 4.9 MPa 는 크림퍼 설정 · **pressure-invariant 주장 없음** · 대신 **전극 접촉 효과**: SS · Al/C 0.3–0.4 → Al/C 360 MPa co-press 1.8 (Table 2) / "1 × 10⁻³" (본문) mS/cm · Li 전극 R_b+gb → 0.51–0.70 mS/cm [우리 산술] | [인쇄] p.3 · p.8–10 · Table 2 · 4 |
| ④ 측정 재현성 | 기관당 **한 값** · **SD · 오차막대 없음 · 기관당 시료 수 n [미확인]** (그림은 "Cell 1") · σ_SS 4 기관 0.3 · 0.4 · 0.3 · 0.3 → 평균 0.325 ± 0.050 (CV 15 %) — ⚠ **한 자리 반올림 해상도** · 셀 쪽 CV: C/20 15 % → C/10 32 % → C/5 이상 덴드라이트 · EIS 1 MHz–1 Hz · 50 mV · ZView · R_b + (R_gb‖CPE) + (R_int‖CPE) + W · 정상 상태 판정 기준 [미확인] · **σ_e (DC 분극) 측정 없음** — SBE/DBE 비 2.77 에 직접 자료는 없고, **접촉 규약 차 (×2.5–5.5) 가 2.77 과 같은 크기**라는 것이 주는 교훈 (§7-2 ④) | [인쇄] Table 1–7 · p.8–16 · [우리 산술] §3-8 |
| ⑤ 우리 DEM/MPM | 세대 2 순수 SE 보정 표적 (300 MPa + 이완 끝 ε_union 10–13 % · 1.64 기준) 의 **같은 기하 (0.1 g · ⌀10 mm) 외부 이웃점** — 360 MPa · 다이 밖 · 질량 기반 ε (= ε_sphere 연산자 꼴) **2.4–9.1 % (1.64) / 14.0–19.9 % (1.86)** · **밀도로 비교하면** 표적 창 (TD 1.64 정의 시 ρ 1.43–1.48) 이 이 논문 계열 300 MPa 어림 (≈1.41–1.54) 안 — 값은 모순 없음 · 같은 펠릿의 결정학 공극은 **21–23 %** → 갈리는 것은 TD · **다압력 Heckel 점 없음** (한 압력) · 랩 펠릿의 1.64 반증 경계 (0.776 mm) 를 이 논문 펠릿 (0.80–0.85 mm 함축) 은 넘지 않는다 | [우리 산술] §7-2 ⑤ |

⛔ **한정어 (떼지 말 것)**: ① σ 값은 **한 자리 유효숫자** (0.3 · 0.4) — "기관 간 15 %" 는 반올림 해상도와 같은 크기 ② 기관당 n · SD 없음 · 그림은 기관당 한 셀 ③ **0.2 MPa 는 이 논문이 잰 값이 아니다** (ref [15], 두께 1.9 mm 기준) ④ 펠릿 두께 측정 도구 · 오차 [미확인] · 두께는 꺼낸 뒤 (스프링백 · 취출 포함) ⑤ **SI (Table S1 = 기관별 프레스 · 다이 · 코인셀 공급사 · Fig S5 = 기관별 EIS 원 스펙트럼 · Fig S6 = 2400 h) 미확보** ⑥ 본문 안 불일치가 많다 (§10 — 1.8 vs 1 × 10⁻³ · 3 min vs 2 min · −25 °C · 단위 mA/µA · vol% 순서 · RC1 수명 그림 = 율 시험 그림 [판독]).

---

## 1. 한 줄 요약
황화물 전고체전지 연구에서 셀 · 지그가 기관마다 달라 자료를 비교할 수 없다는 문제에, **가장 흔한 상용 셀 (CR2032 코인셀)** 로 조립 지시서를 만들고 네 기관 (RC1 ABEE · RC2 AIT · RC3 CIC energiGUNE · RC4 U. Porto) 이 같은 원료로 **이온전도도 (EIS) · Li|LPSCl|Li 박리-도금 · 계면 EIS · CCD · NMC90505|LPSCl|Li 율 · 수명**을 재 비교했다.
전해질 값 (σ_ion 0.3–0.4 mS/cm · 상대밀도 하한 91–94 %) 은 기관 사이에 모이고, 셀 값 (Li|Li 175 – > 200 h · C/20 방전 102–144 mAh/g · C/10 50–118) 은 흩어진다 → *"with increasing amount of components and parameters, the measurements become less reproducible"* (p.16) · "cell history" 를 전부 보고하라는 권고.
낮은 작동 압력 (≈0.2 MPa) 때문에 성능은 문헌보다 낮지만 *"more realistic outlook"* 이라는 것이 저자의 자리매김 (p.13 · p.16).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| A. Beutl, A. Orue‡, P. López-Aranguren, A. I. Pitillas Martinez, M. H. Braga, V. Kekkonen, A. Tron‡ (AIT · CIC energiGUNE · ABEE · U. Porto · Pulsedeon) | Electrochem. Sci. Adv. 4 (2024) e2400004 | 10.1002/elsa.202400004 | **Li₆PS₅Cl** (NEI "LPSCl fine") + **NMC90505** 단결정 비코팅 (Chengdu B&M) + C65 + Li 박 | 실험 — 4 기관 round robin (코인셀) · 시뮬레이션 없음 |

| RRT 이름 | 기관 | 성격 | 이 논문의 자료 |
|---|---|---|---|
| RC1 | ABEE — Avesta Battery & Energy Engineering (Belgium) | 산업체 | σ (SS) · 밀도 · Li\|Li · 율 · 수명 |
| RC2 | AIT — Austrian Institute of Technology (Austria) | 연구소 | σ (SS · Al/C) · 밀도 · Li\|Li (175 h 단락) · 계면 EIS · CCD · 율 · 수명 · **다른 다이** (Fig 2 사진 = RC2) |
| RC3 | CICe — CIC energiGUNE (Spain) | 연구소 | σ (SS · Al/C · **co-press**) · Fig 5 · Li\|Li · 계면 EIS (480 h) · CCD · 율 · 수명 |
| RC4 | UPORTO — University of Porto (Portugal) | 대학 | σ (SS · Al/C) · 밀도 · Li\|Li (Table 3 만) · 율 · 수명 (Table 7 만) |

(기관 대응 = p.3 인쇄 · 저자 소속 Pulsedeon (핀란드) 은 RC 가 아니다 · *"1 university, 2 research facilities, and 1 industrial entity"* p.2–3.)

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 셀 부품 (p.3 · p.6 · Fig 1)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | Li₆PS₅Cl *"LPSCl fine, NEI Corp., ∼1 µm particle size"* · 받은 그대로 · Ar 글러브박스에서만 개봉 | [인쇄] p.3 |
| CAM | LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂ (NMC90505) · **단결정 · 비코팅** · Chengdu B&M Science and Technology · 실용 방전용량 **210 mAh/g** (공급사 값 — C-rate 환산 기준) | [인쇄] p.3 · p.8 |
| 도전재 | C65 (Imerys) · 진공 100 °C 건조 | [인쇄] p.3 |
| Li | Goodfellow 박 (폭 38.1 mm · 두께 0.2 mm) → ⌀8 mm 디스크 | [인쇄] p.3 · p.6 |
| 코인셀 부품 | CR2032 (X2lab · Hohsen 등 — Table S1 [SI 미확보]) · SS 스페이서 0.5 mm × ⌀15.5 mm (두 장) · 물결 스프링 ⌀15.4 × 1.1 mm · PP 개스킷 | [인쇄] p.3 · p.6 |
| 봉합 | **4.9 MPa** (*"50 kg cm−2/750 psi"*) — 크림퍼 압력 [우리 산술: 50 kgf/cm² = 4.90 MPa · 750 psi = 5.17 MPa] | [인쇄] p.6 |
| 작동 (적층) 압력 | **≈0.2 MPa** — *"In a recent study, the pressure inside a CR2032 setup was determined as 0.2 MPa,[15] considering a total sample thickness of 1.9 mm (without the spring)"* · ⚠ **이 논문 측정 아님** | [인쇄] p.3 · p.8 · p.12 |
| 글러브박스 | Ar · H₂O = 0.3 ppm · O₂ ≤ 0.1 ppm (모든 RC) · 취급 · 폐기 지침 = Fig S2 · S3 [SI 미확보] | [인쇄] p.3 |
| XRD | NMC = R-3m (α-NaFeO₂ · LiNiO₂ JCPDS 74-0919 로 지수) · LPSCl = argyrodite (*"matched well with a standard card of Li7PS6 [JCPDS No. 34-0688]"*) — **격자상수 정련 · 상 정량 없음** · LPSCl 패턴의 2θ ≈20° 넓은 언덕 = 기밀 홀더 배경으로 보임 [판독 · 추정] | [인쇄] p.3 · Fig 1a |
| SEM | NMC: *"microsized granules with polygonal shapes … particle sizes of approximately 10–15 µm"* · LPSCl: *"particle sizes of approximately 1 µm"* | [인쇄] p.3 |
| [판독] SEM | 눈금 막대 NMC **2 µm** · LPSCl **5 µm** → NMC 단결정 ≈1–4 µm (**본문 10–15 µm 와 맞지 않음**) · LPSCl = 미세 입자가 뭉친 **응집체 (수 – ≈20 µm)** | [판독] Fig 1b |
| EDS | Fig 1c 표: LPSCl P 14 · S 71 · Cl 14 wt% (15 · 71 · 13 at%) · NMC Ni 89.8 · Mn 4.6 · Co 5.6 wt% (89.6 · 4.7 · 5.6 at%) — 본문 *"approximately 9:05:05 … 1:5:1"* · LPSCl 스펙트럼에 O · C 봉우리 (표에는 없음) | [인쇄] Fig 1c · p.3 · [판독] |
| 보관 안정성 | 글러브박스 6 개월 넘게 보관 뒤 XRD · SEM · EDS 변화 없음 (Fig S4) | [인쇄] p.3–4 · SI 미확보 |

### 3-2. ★ 펠릿 제작 · 밀도 (p.4–5 · p.9 · Fig 2 · Fig 4 · Table 2)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 질량 · 다이 | **100 mg** · **⌀10 mm** 다이 — RC2 사진: 경화강 (Across International, W18Cr4V) · *"All RCs were using the same die set … except for RC2"* | [인쇄] p.4 · p.10 |
| 프레스 | 유압 일축 — 본문 *"Maassen MP15"* · 사진 표기 **"MP150"** | [인쇄] p.4 · [판독] Fig 2a |
| 예압 | *"0.4 tons for seconds"* (= **50 MPa** [우리 산술 · 0.4 t × 9.81 / 78.54 mm²]) | [인쇄] Fig 4a · b |
| 성형압 · 유지 | 본문 **360 MPa · 3 min** (*"maintained for 3 min using a conventional hydraulic uniaxial press device"*) · 그림 **"realize > 2.9 tons for 2 mins = 800 um"** (2.9 t = **362 MPa** [우리 산술]) — **유지 시간 3 ↔ 2 min 불일치** | [인쇄] p.4 · Fig 4a · b |
| 온도 · 분위기 | **실온 냉간** (*"dry-pellets … are prepared by cold-pressing of the pristine materials within an Ar filled glovebox"*) · 온도 숫자 [미확인] · **hot pressing 없음** | [인쇄] p.3 |
| 두께 · 상태 | **≈0.8 mm** — *"After removing the sample from the die set a free-standing pellet with a thickness of approximately 0.8 mm is obtained. The thickness of the pellet might change due to losses of the electrolyte powder during filling and assembly of the die set."* → **다이에서 꺼낸 뒤** (하중 제거 · 취출 회복 포함) · 측정 도구 · 오차 [미확인] | [인쇄] p.4 · Fig 2 캡션 |
| 밀도 측정법 | *"use the weight and geometric volume of the sample to calculate its apparent density and further compare it with the reported crystallographic one"* — **비중병 없음** | [인쇄] p.4 |
| 겉보기 밀도 | p.5: *"dense pellets with densities in the range of 1.6–1.50 g cm−3 … crystallographic density of 1.64 g cm−3.[37]"* · p.9: *"the density of the obtained pellets is at least 1.49 g cm−3, which means that their relative density is higher than 90% (crystallographic density of Li6PS5Cl is 1.64 g cm−3).[10,37]"* — **범위 하한 1.50 ↔ 1.49 불일치** | [인쇄] p.5 · p.9 |
| 상대밀도 (기관별) | RC1 **>91** · RC2 **>94** · RC3 **>93** · RC4 **>93 %** (1.64 기준) | [인쇄] Table 2 |
| 다이 재료 경고 | *"compressive strength of PEEK is around 118–130 MPa[38]"* — 자작 PEEK 다이는 고압 치밀화를 못 견딜 수 있다 | [인쇄] p.5 |

**[우리 산술] 같은 펠릿을 두 진밀도로** (100 mg · ⌀10.00 mm → A = 0.7854 cm² · ε = 1 − ρ/TD · t = m/(ρA)):

| 겉보기 밀도 ρ (g/cm³) | 어디서 | 함축 두께 t (mm) | 상대밀도 · ε (TD 1.64) | 상대밀도 · ε (TD 1.86) |
|---|---|---|---|---|
| 1.49 | p.9 "at least" | 0.855 | 90.9 % · **9.1 %** | 80.1 % · **19.9 %** |
| 1.50 | p.5 범위 하단 | 0.849 | 91.5 % · 8.5 % | 80.6 % · 19.4 % |
| > 1.492 · > 1.525 · > 1.542 | Table 2 하한 (91 · 93 · 94 % × 1.64) | < 0.853 · < 0.835 · < 0.826 | ε < 9 · < 7 · < 6 % | > 80.2 · > 82.0 · > 82.9 % · ε < 19.8 · < 18.0 · < 17.1 % |
| 1.59 | 공칭 0.8 mm 두께에서 | 0.800 | 97.0 % · 3.0 % | 85.5 % · 14.5 % |
| 1.60 | p.5 범위 상단 | 0.796 | 97.6 % · **2.4 %** | 86.0 % · **14.0 %** |

⇒ **ε = 2.4–9.1 % (TD 1.64) ↔ 14.0–19.9 % (TD 1.86)** — 같은 측정값에서 ≈11 %p 차.  비교: 같은 공급사 (NEI) LPSCl · 370 MPa · 다이 밖 (정본 `doux2020_stack_pressure_assb` Table S2): 실측 1.522 g/cm³ · 상대밀도 80.3–84.9 % (TD 1.860) — 이 논문의 TD 1.86 환산 80.1–86.0 % 와 **같은 띠** [우리 산술].

### 3-3. ★★ "결정학 밀도 1.64" 의 정체 — 우리 질문 ①
- [인쇄] 두 문장 (위 표) — 라벨은 둘 다 **"crystallographic"**, 인용은 p.5 = [37] · p.9 = [10,37].  이 논문은 격자상수를 정련하지 않았고 (XRD 를 카드와 대조만, p.3) 진밀도를 재지 않았다 → **1.64 는 이 논문 안에서 계산 · 측정된 값이 아니다**.
- [인쇄 p.17] [37] = *L. Zhou, K.-H. Park, X. Sun, F. Lalère, T. Adermann, P. Hartmann, L. Nazar, ACS Energy Lett 2019, 4, 265.* · [10] = *A. Tron, R. Hamid, N. Zhang, A. Beutl, Nanomaterials 2023, 13, 327.* (교신 저자 그룹 자기 인용).  두 원문 다 litdb 정본 카드 없음 — **1.64 가 거기서 어떻게 나왔는지 [미확인]**.
- [우리 산술] 결정학 밀도 = Z·M/(N_A·a³), Z = 4 (F-43m argyrodite), M(Li₆PS₅Cl) = 268.36 g/mol:

| a (Å) · 출처 (정본 카드) | ρ_cryst (g/cm³) |
|---|---|
| 9.85910 · `ohno2020…` Table S1 (그 표의 이론밀도 인쇄값 **1.86**) | 1.860 |
| 9.8598 · `adeli2019_halide_substitution_boosting_argyrodite` (XRD) | 1.860 |
| 9.8614 · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` (중성자) | 1.859 |
| **1.64 가 되려면** | a = **10.28 Å** (+4.3 %) 또는 Z = 3.53 — 어느 쪽도 Li₆PS₅Cl 이 아니다 |

- 실측 진밀도 (정본 카드): Ohno 2020 dataset D 비중병 **1.874** (Table S6) · **같은 이름 NEI "fine" LPSCl 진밀도 1.87** (`frankenberg2025…` p.4 · p.12 — 측정법은 카드에 없음) → 결정학 · 실측 둘 다 ≈1.86–1.87 ⇒ **1.64 는 결정학 밀도도, 이 분말 이름의 진밀도도 아니다** [우리 산술 · 정본 카드 값].
- 반례 한 점 [우리 산술]: Ohno 2020 랩 D 의 Li₆PS₅Cl 펠릿 (720 MPa 단축) **기하 밀도 1.655 g/cm³** (정본 카드 Table S6) — 1.64 를 진밀도로 쓰면 이 펠릿의 공극은 **−0.9 %** (불가능) · 1.86 이면 11 % (그 카드의 상대밀도 89 % 와 같음).  배치는 다르다 (Giessen 합성).
- 이 논문 안의 두 번째 흔적 [우리 산술]: 양극 조성 *"57:40:3 wt% or 65:31:4 vol% of NMC:Li6PS5Cl:C65"* (p.6) — ρ_NMC 4.8 · ρ_C65 2.0 (둘 다 이 논문에 없음 · 가정) 로 환산하면 **NMC 31.4 : SE 64.6 : C 4.0 vol% (ρ_SE 1.64)** · 34.0 : 61.7 : 4.3 (ρ_SE 1.86) → 인쇄 vol% 는 **ρ_SE ≈1.64 로 계산**됐고 **이름 순서가 뒤바뀌었다** (65 = SE · 31 = NMC; ρ_NMC 4.7–4.85 · ρ_C 1.8–2.2 범위에서도 SE 64.2–64.8 %).
- 이 카드의 위치: 정본 카드에서 1.64 를 인쇄한 곳 — `bazzoun2025_dem_parameter_sensitivity_assb_cathode` (Table 2 · stated) · `bazzoun2026_dem_fem_rnm_ionic` (재료 파라미터) · `lee2025_heckel…` (SI p.3 *"calculated"*) · `lee2026_lpscl_coating_thickness_ncm811` (SI 식) · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` (SI 식 2) — 카드들에 근거가 적힌 것은 없다 (작업 브랜치 `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §3 집계 + 이 카드 grep).  ~~**"crystallographic" 라벨과 인용 번호를 함께 준 것은 이 논문이 처음**이다 (정본 grep 기준).~~ ⛔ 정정 (2026-10-14 · 같은 묶음 색인 때): 같은 그룹의 `tron2023_lpscl_ccd_ambient_pressure` (2023-10 출판 · 이 논문보다 이르다) 가 먼저 *"crystallographic density of 1.64"* 를 쓰고 인용 ref 22 = Doux 2020 (*Adv. Energy Mater.* 10, 1903253) 을 붙였다 — 그런데 Doux 2020 은 이론밀도 1.860 을 쓴다 (정본 doux2020 카드 · 원문 직접 확인 전).  같은 그룹이 같은 1.64 에 서로 다른 인용 (Doux 2020 ↔ 이 논문의 [37] Zhou 2019 · [10] Tron 2023 *Nanomaterials*) 을 붙인다.  ⇒ 다음 한 걸음 = [37] · [10] 원문 (본문 + SI) 에서 1.64 를 찾는 것.  거기에도 없으면 공급사 자료 · 데이터베이스 값 같은 공통 상류를 의심할 수 있다 [추정 — 확인 안 됨].

### 3-4. ★ σ_ion — Table 2 · Fig 5 · Li 전극 값 (p.8–10)
**Table 2 [인쇄 p.9]** (단위 ×10⁻³ S/cm · 25 °C · 측정 중 압력 = 코인셀 · 두께 ≈0.8 mm):

| 기관 | 상대밀도 (1.64 기준) | SS\|SE\|SS | Al/C\|SE\|Al/C | Al/C\|SE\|Al/C* (co-press) |
|---|---|---|---|---|
| RC1 | > 91 % | 0.3 | n.d. | n.d. |
| RC2 | > 94 % | 0.4 | 0.4 | n.d. |
| RC3 | > 93 % | 0.3 | 0.4 | **1.8** |
| RC4 | > 93 % | 0.3 | 0.3 | n.d. |

\* *"Al/C electrodes were co-pressed together on both side of the LPSCl under 360 MPa for 3 min."*

- 본문 (p.9): *"ca. 4 × 10−4 S cm−1 in an SS|SE|SS and Al/C|SE|Al/C symmetric configuration"* · *"an ionic conductivity of 1 × 10−3 S cm−1 is obtained for the symmetric Al/C|SE|Al/C cell configuration where Al/C foils were co-pressed … suggesting that the co-pressing … improves the mechanical contact at the electrode/SE interface leading to obtain a lower resistances.[44]"* → **co-press 값: 표 1.8 ↔ 본문 1 — 불일치**.
- 식 (1) [인쇄 p.8]: σ = l / ((R_b + R_gb) × A) — R_int (전극/SE 계면) 와 W 는 뺀다.
- **Fig 5 [판독 · 우리 산술]** (RC3): (a) SS\|SE\|SS — 삽입 그림의 첫 고주파 점 Z′ ≈0.29 kΩ·cm² 에서 이미 −Z″ ≈0.5 → **실축 절편이 1 MHz 창 밖** · 호가 ≈1.0–1.1 kΩ·cm² 까지 간 뒤 차단 스파이크 (주 그림 −Z″ ≈900 kΩ·cm² 까지).  Table 2 의 0.3 mS/cm 는 l = 0.8 mm 에서 R_b + R_gb ≈ **0.27 kΩ·cm²** — 보이는 호 (≈0.3 → 1.0) 의 대부분은 R_int 로 배정됐을 것 [추정 — 맞춤 값 미공개].  범례 오기 "SS \| LPSCl \| SE".  (b) co-press Al/C — 고주파 절편 ≈**0.085–0.087 kΩ·cm²** → l = 0.8 mm 면 σ ≈ **0.92–0.94 mS/cm** = 본문 "1 × 10⁻³" 와 맞고 **표의 1.8 은 l ≈1.5 mm 여야 나온다** (100 mg 이면 ρ ≈0.83 — 불가) [우리 산술].
- **Li 전극 (Li\|LPSCl\|Li)**: Table 4 R_b+gb 0 h = **125 Ω cm² (RC2 · RC3 같은 값)** → l = 0.8 mm 면 **0.64 mS/cm** · 전 범위 114–157 → 0.51–0.70 mS/cm [우리 산술].  저자: 옴 법칙 (박리-도금 과전압) 으로 **7.6 × 10⁻⁴ S/cm**, *"in good agreement with the EIS data and suggesting that the ionic conductivity also depends on the nature of the electrodes"* · *"tighter contact between the electrolyte and the ductile Li electrodes compared to the stiffer SS and Al/C electrodes"* (p.10).  검산 [우리 산술]: 20–25 mV @ 0.15 mA/cm² → 총 ASR 133–167 Ω cm² ≈ R_b+gb + R_int (0 h 144–154 Ω cm², Table 4) ✓ — 그러나 7.6 × 10⁻⁴ 는 ≈105 Ω cm² (≈16 mV) 를 요구 → **인쇄 숫자로 재현 안 됨** (그들이 쓴 η · l [미확인]).
- ⇒ **같은 분말 · 같은 성형 · 같은 두께**에서 접촉 규약만 바뀐 값: SS · Al/C **0.3–0.4** → Li **0.5–0.7** [우리 산술] → co-press Al/C **0.9–1.8** mS/cm — 기관 차 (0.3 ↔ 0.4) 보다 크다.

### 3-5. Li\|LPSCl\|Li 박리-도금 · 계면 안정성 (Table 3 · 4 · Fig 6 · 7 · p.10)
- 조건 [인쇄 Table 1 · p.8]: 1 h OCV → **150 µA/cm²** · 반주기 2 h (= 0.3 mAh/cm²) · 한계 ±1 V · 50 사이클 · 25 °C.
- **Table 3 [인쇄]**: RC1 **> 200 h** · RC2 **175 h** · RC3 **> 200 h** · RC4 **> 200 h** — *"average overpotential of about 20–25 mV"* · RC2 = 다른 다이 → *"Apparently, the latter one yields a lower quality of prepared pellets"* (p.10) · 한 셀은 2400 h 뒤 단락 (Fig S6, SI 미확보).
- **Fig 6 [판독]** (기관당 "Cell 1" 한 셀): RC1 ±23 → ±21 mV (≈200 h) · RC2 ±25 → ±31 mV (≈100 h) → **≈177 h 에 ±1 mV 로 붕괴 (단락)** · RC3 ±21–22 mV 로 > 215 h 안정 · RC4 그림 없음.
- 저자 해석: *"The quality of the prepared electrolyte pellets, especially parameters like porosity and remaining defects, can highly influence dendrite formation and propagation"* · 전해질 두께 ≈0.8 mm 는 응용 요구 (0.02–0.03 mm) 의 10 배 넘게 두껍다 (p.10).
- **Table 4 [인쇄]** (Ω cm²):

| 시간 (h) | R_b+gb RC2 | R_b+gb RC3 | R_int RC2 | R_int RC3 |
|---|---|---|---|---|
| 0 | 125 | 125 | 19 | 29 |
| 24 | 126 | 116 | 22 | 41 |
| 48 | 137 | 114 | 19 | 27 |
| 120 | 157 | 114 | 21 | 41 |

- 본문: R_int 는 *"at least for the first 120 h"* 크게 안 바뀌고, 그 뒤 계면층 형성으로 커져 *"up to 131 Ohm cm2 after 480 h"* (p.10) · 결론: *"stable for at least 200 h with a small increment of 10 Ohm cm2 in Rint, obtaining an area specific resistance of 20 Ohm cm2"* (p.16) — **120 h ↔ 200 h · RC3 R_int 27–41 ↔ "20" 불일치**.
- **Fig 7 [판독]**: 저주파 끝 RC2 ≈0.20 (0 h) → 0.23 (48 h) → 0.26 (120 h) → 0.33 (150 h) → 0.36 kΩ·cm² (200 h) · RC3 ≈0.18–0.21 (0–120 h) → 0.27 (200 h) → **0.45 kΩ·cm² (480 h)**.  RC2 는 R_b+gb 자체도 +26 % (0 → 120 h) — RC3 는 −9 %.

### 3-6. CCD — 임계 전류밀도 (Table 5 · Fig 8 · p.8 · p.10–12)
- 절차 [인쇄 p.8]: 부하 1 mAh/cm² 기준 · 10 (C/100) → 20 (C/50) → 50 (C/20) → 100 (C/10) → 200 (C/5) → 500 (C/2) → 1000 (1C) → 2000 (2C) µA/cm² · 각 1 h 도금 / 1 h 박리.
- **Table 5 [인쇄]** 과전압 (mV): RC2 **3 · 5 · 11 · 22 · 44** · RC3 **3 · 9 · 14 · 25 · 52** (10 · 20 · 50 · 100 · 200) · 500 이상 "–" · ⚠ 표 머리 단위가 "mA cm⁻²" 로 인쇄 (10–500 은 µA — §2.8 정의와 다름).
- **CCD = 200 µA/cm² (= C/5 for 1 mAh/cm²)** — 그 위에서 비선형 · 불안정 뒤 0 V 근처로 떨어짐 (덴드라이트) [인쇄 p.10–12].
- [판독] Fig 8: C/2 에서 RC2 ≈+0.13 V 까지 상승 · RC3 1C 에서 ≈0.32 V 스파이크 · 2C 에서 RC3 ≈0 V.
- [우리 산술] 기울기 ASR: RC2 ≈**220** Ω cm² (50–200 µA) · RC3 ≈**250–280** — 박리-도금 셀 (133–167) 보다 1.3–2.1 배 크다 = **셀 간 흩어짐** (다른 셀).
- 저자 결론: 낮은 내부 압력 (0.2 MPa) 의 **Li/SE 접촉 (계면 저항) 이 주 병목** · 보통은 사이클 중 고압 (*"up to 10 MPa"*) 으로 푼다 · 대안 = 부드러운 계면층 (p.12).

### 3-7. NMC90505\|LPSCl\|Li 전지 (Table 6 · 7 · Fig 9 · 10 · p.8 · p.13)
- 양극 [인쇄 p.6 · Fig 4c]: NMC:LPSCl:C65 = **57:40:3 wt%** · 막자 사발 손 혼합 (*"no sequential mixing … to ensure high reproducibility"*) · 1 g 준비 · **10 mg (= 5.7 + 4 + 0.3 mg)** 을 50 MPa · 30 s 예압한 SE 100 mg 위에 펴고 **360 MPa · 2–3 min** 동시 가압 → bilayer (Fig 3) · Li ⌀8 mm 한쪽.
- 로딩 [우리 산술]: 5.7 mg × 210 mAh/g / 0.7854 cm² = **1.52 mAh/cm²** → Fig 10 의 "1.5" 와 맞고 **Fig 9 캡션 "2.0 mA h cm⁻²" 는 13.1 mg 이어야** · 본문 C/20 = 75 µA/cm² (p.8, 1.5 기준) ↔ 100 µA/cm² (p.13, 2.0 기준).
- **Table 6 [인쇄]** (2 번째 사이클 충전/방전, mAh/g): C/20 — RC1 125/122 · RC2 145/142 · RC3 146/144 · RC4 114/102 · C/10 — 124/99 · 120/100 · 120/118 · 56/50 · C/5 이상 — RC1–3 *"Dendrites during charging"* · RC4 21/20.
- **Table 7 [인쇄]** (C/20 수명, 충전/방전 mAh/g): 1 사이클 RC1 182/125 · RC2 225/175 · RC3 229/175 · RC4 211/115 · 3 사이클 116/117 · 160/158 · 165/163 · 105/104 · 5 사이클 – · 148/146 · 153/148 · – · 마지막 116/117 (3rd) · 140/137 (13th) · 116/86 (7th) · 105/104 (3rd).
- 본문 (p.13): 첫 사이클 CE ≈70 % · 이후 ≈99 % · *"146/144 mA h g−1 for C/20 and 120/118 mA h g−1 for C/10"* (= RC3) · 문헌 [36] 보다 낮은 성능 = 코인셀의 낮은 압력 탓 · 결론 (p.16): *"cells reach down to 80% BoL in the first 10–15 cycles"* · *"After the first cycle, the CE increases up to 95 %"* (p.13 의 99 % 와 불일치).
- [판독] Fig 9 (율, 방전 mAh/g): RC1 125 · 122 · 118 → C/10 100 · 83 · 78 → C/5 42 · 32 · 31 → C/3 37 (*"Stopped at C/3 due to the dendrites"*) · RC2 153 · 140 · 51 → 97 · 47 · 39 → … · RC3 151 · 145 · 139 → 119 · 118 · 64 → … · RC4 115 · 103 · 104 → 50 · 50 · 49 → 15 · 15 · 20 → 5 (*"poor performance"*) · 충전 곡선의 전압 잡음 · 4.3 V 미도달 = 덴드라이트성 연단락 신호.
- [판독 · 숫자화] **Fig 10a (RC1 "수명 C/20") = Fig 9a (RC1 율) 와 같은 자료로 보인다**: 사이클 1–4 방전 124.9 · 121.7 · 117.5 · 99.4 ↔ 125.0 · 121.9 · 117.5 · 99.2 mAh/g (±0.2) · 사이클 4 · 7 의 계단 하락 = 율 시험 (C/20×3 → C/10×3 → C/5×3) 전환 위치 · CE 점 무늬도 같다 → **RC1 의 "C/20 수명" 은 독립 셀이 아닐 수 있다** (원문 설명 없음) · Table 7 RC1 이 3 사이클에서 끝나는 것과 맞물린다.
- [판독] Fig 10b (RC2): 176 → 165 → 159 → 151 → 146 … 132 (10) → 95 (13) → 9 (22) · Table 7 의 *"140/137 (13th cycle)"* 은 그림의 13 번째 (≈95) 가 아니라 8–9 번째 근처 값.  Fig 10c (RC3): 175 → 168 → 163 → 154 → 148 → 116 → 86 (*"Stopped at cycle 8"*).

### 3-8. ★ 기관 간 흩어짐 — [우리 산술] (기관당 인쇄값 한 개 · n · SD 원문 없음)
| 양 | 기관 수 | 값 | 평균 ± SD (CV) | 최대/최소 |
|---|---|---|---|---|
| σ_ion SS\|SE\|SS (mS/cm) | 4 | 0.3 · 0.4 · 0.3 · 0.3 | 0.325 ± 0.050 (15 %) | 1.33 |
| σ_ion Al/C\|SE\|Al/C | 3 | 0.4 · 0.4 · 0.3 | 0.367 ± 0.058 (16 %) | 1.33 |
| 상대밀도 하한 (1.64 기준) | 4 | > 91 · > 94 · > 93 · > 93 % | — | — |
| Li\|Li 수명 (h) | 4 | > 200 · 175 · > 200 · > 200 | — | — |
| R_b+gb (Li\|Li, 0 h, Ω cm²) | 2 | 125 · 125 | — | 1.00 |
| R_int (0 h) | 2 | 19 · 29 | — | 1.53 |
| CCD ASR (200 µA, Ω cm²) | 2 | 220 · 260 | — | 1.18 |
| C/20 2 사이클 방전 (mAh/g) | 4 | 122 · 142 · 144 · 102 | 127.5 ± 19.7 (15 %) | 1.41 |
| C/10 방전 | 4 | 99 · 100 · 118 · 50 | 91.8 ± 29.2 (32 %) | 2.36 |
| 1 사이클 충전 (Table 7) | 4 | 182 · 225 · 229 · 211 | 211.8 ± 21.3 (10 %) | 1.26 |
| 1 사이클 방전 (Table 7) | 4 | 125 · 175 · 175 · 115 | 147.5 ± 32.0 (22 %) | 1.52 |
| 첫 사이클 CE | 4 | 68.7 · 77.8 · 76.4 · 54.5 % | — | — |
| 활물질 이용률 (1 사이클 방전 / 210) | 4 | 60 · 83 · 83 · 55 % | — | — |

- ⚠ σ 의 CV 15 % 는 **0.3 · 0.4 를 한 자리로 적은 반올림 폭 (±0.05 = ±12–17 %)** 과 같은 크기 — 실제 흩어짐은 0 에서 ≈±30 % 사이 어디든 가능하다.  이 표로 "σ 재현성 ±15 %" 라고 쓰지 않는다.
- 저자의 단계 주장 (*"with increasing amount of components and parameters, the measurements become less reproducible"*) 과 방향은 맞는다 (σ → Li\|Li → C/20 → C/10 → C/5) — 통계 검정은 없다.

---

## 4. ★ 방법 — 조립 지시서 · 측정 사슬 · 입자 처리

### 4-1. 펠릿 · bilayer 지시서 (p.4 · p.6 · Fig 4)
1. SE 100 mg → ⌀10 mm 다이 → 0.4 t (50 MPa) 몇 초 → 2.9 t (≈360 MPa) 2 min (그림) / 3 min (본문) → 꺼내 ≈0.8 mm 자유 펠릿 → 질량 · 기하 부피로 겉보기 밀도 → 1.64 로 나눠 상대밀도.
2. bilayer: SE 100 mg 50 MPa · 30 s → 위 펀치만 빼고 양극 혼합 10 mg 을 고르게 → 360 MPa 2–3 min → 꺼냄.  (복합 양극 치밀화에는 보통 300–800 MPa 를 쓰고 그 응력이 활물질을 깬다 · 단결정이 더 견딘다 · 가압 순서가 계면 품질에 중요 — p.5–6 서술.)
3. 이온전도도 셀: SE 펠릿 양쪽에 SS 또는 Al/C (선택) — co-press 판 = Al/C 를 양쪽에 대고 360 MPa · 3 min 함께 가압 (Table 2 각주).

### 4-2. CR2032 조립 순서 (p.6 · Fig 4)
① 아래 캡 + PP 개스킷 → ② SS 판 0.5 mm × ⌀15.5 (스페이서 + 집전체) → ③ bilayer (양극 면이 SS 쪽 · SE 면이 위) → ④ Li ⌀8 mm × 0.2 mm → SS 스페이서 0.5 mm → ⑤ 물결 스프링 ⌀15.4 × 1.1 mm → 위 캡 → ⑥ **4.9 MPa** 로 봉합 → ⑦ 대칭셀은 Li 두 장 또는 Al/C 두 장.  (그림 4c 의 *"Li metal foil attachment both side"* 는 전지에서는 한쪽 — 그림 문구 오기로 보임.)

### 4-3. 전기화학 시험 정의 (Table 1 · p.8–9)
| 시험 | 조건 [인쇄] |
|---|---|
| 이온전도도 | EIS **1 MHz–1 Hz · 50 mV** (각주: 액체 LIB 10 mV [41] · SSB 50 mV [42]) · 표의 온도 인쇄 **"−25 °C"** ↔ 본문 *"conducted at 25 °C"* · ZView 등가회로 R_b–(R_gb CPE_gb)–(R_int CPE_int)–W_s · 식 (1) |
| 박리-도금 | 1 h OCV · 2 h / 2 h · ±1 V · 50 사이클 · 150 µA/cm² · 25 °C |
| 율 | 1 h OCV · 2.6–4.3 V · 3×C/20 + 3×C/10 + 3×C/5 + 3×C/3 + 3×C/2 + 3×C + 10×C/10 · 로딩 1.5–2 mAh/cm² · 25 °C · C 기준 210 mAh/g |
| 수명 | 1 h OCV · C/20 · 2.6–4.3 V · 5–15 사이클 또는 80 % BoL 까지 · 1.5–2 mAh/cm² · 25 °C |
| 추가 (권고) | CCD · Li/SE 계면 EIS (24 h 마다) · 사이클 전후 임피던스 · 분해 · 사진 |

- 정상 상태 판정 · 이완 시간 · 셀 휴지 기준 [미확인] (1 h OCV 만 인쇄).  면적 A 를 펠릿 (⌀10) 으로 했는지 전극 (Li ⌀8) 으로 했는지 [미확인] — Li\|Li 의 ⌀8 전극 ↔ ⌀10 펠릿은 전류가 전극 밖으로 퍼질 여지 (면적비 상한 1.56) 가 있다 [추정].

### 4-4. ★ 입자 처리
- 실험 — 실제 분말.  SE = NEI "fine" (≈1 µm 1 차 입자 · SEM 에서 응집체) · CAM = 단결정 NMC90505 (≈1–4 µm 판독) · C65 · 손 혼합.  성형 = 일축 냉간 압축 (재배열 · 응집체 해체 · 소성 변형이 섞인 실제 과정 — 이 논문은 기전을 나누지 않는다).
- 시뮬레이션 없음 · 입자 형상 · 접촉 모델 없음 → frame[5] 의 어느 쪽 계산도 아니다 (§7-3).

### 4-5. 기법 미니 용어집
- **Round-robin test (RRT)**: 같은 시료 · 같은 지시서를 여러 기관이 각자 재 기관 간 재현성을 보는 비교 시험 (Ohno 2020 은 지시서 없이 "각자 방식" — 이 논문은 지시서까지 맞췄다).
- **CR2032**: ⌀20 mm × 3.2 mm 코인셀 규격 · 내부 압력은 스프링 · 시료 두께가 정한다 — 측정 · 조절 불가.
- **봉합 (crimping) 압력 ↔ 적층 (stack) 압력**: 4.9 MPa 는 크림퍼가 캡을 접는 압력, 0.2 MPa 는 봉합 뒤 스프링이 셀 안에 거는 압력 (ref [15]).
- **차단 전극 (blocking electrode)**: 이온을 통과시키지 않는 전극 (SS · Al/C) — 저주파에서 축전기처럼 보여 R_b (+R_gb) 를 고주파 쪽에서 읽는다.
- **Al/C**: 탄소 코팅 알루미늄 박.  **co-press**: 전극 박을 SE 와 함께 고압으로 눌러 접촉을 만드는 것.
- **R_b · R_gb · R_int · W_s · CPE**: 입내 · 입계 · 전극/SE 계면 저항 · Warburg (확산) · 정위상 요소 (비이상 축전기).
- **CCD (critical current density)**: 대칭 Li 셀이 단락 없이 견디는 최대 전류밀도 — 계단 전류로 잰다.
- **CE · ICE · BoL**: 쿨롱 효율 · 첫 사이클 쿨롱 효율 · 초기 수명 (beginning of life) 용량 기준.
- **겉보기 (apparent) · 상대 (relative) · 결정학 (X-ray, crystallographic) · 비중병 (skeletal, pycnometric) 밀도**: 질량/기하 부피 · 겉보기/기준 · Z·M/(N_A·V_cell) · 기체 치환 고체 부피 — 이 논문은 첫째만 쟀고 셋째라 부른 값 (1.64) 을 기준으로 썼다.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) XRD NMC90505 · Li₆PS₅Cl (정련 없음) (b) SEM NMC (2 µm 막대) · LPSCl (5 µm 막대) (c) EDS + 조성 표 | ★ NEI "1 µm" = **1 차 입자** · 실제 분말은 응집체 [판독] — DEM SE 크기 (세대 2 r 0.5 µm) 와 다짐 단위가 다르다 |
| 2 | (a) 유압 프레스 (MP150 표기) · ⌀10 경화강 다이 부품 (b) LPSCl 펠릿 ⌀10 · 0.8 mm (RC2) | 랩 펠릿과 **같은 기하** (0.1 g · ⌀10) — §7-2 ⑤ |
| 3 | 원료 → 혼합 (NMC/SE/C65) → 다이 안 반쪽 셀 → bilayer (흰 SE · 검은 양극) | bilayer 공정 사진 |
| 4 | (a) 이온전도도 (b) Li 도금 · CCD (c) 율 · 수명 셀의 공정 상자 (톤 · 시간 · 질량 인쇄) + 적층 모식도 (d) 대칭셀 조립 사진 6 단계 | ★ 지시서 원본 — 2.9 t ≈ 362 MPa · 0.4 t ≈ 50 MPa [우리 산술] · 양극 10 mg = 5.7 + 4 + 0.3 mg |
| 5 | Nyquist (RC3) (a) SS\|SE\|SS (b) co-press Al/C\|SE\|Al/C + 등가회로 | ★★ 접촉 규약이 "bulk" 절편을 바꾼다 · (a) 는 1 MHz 창에서 bulk 절편 미도달 · (b) 절편 ≈0.086 kΩ·cm² → ≈0.93 mS/cm [판독 · 우리 산술] |
| 6 | Li\|LPSCl\|Li 0.15 mA/cm² 박리-도금 (RC1 · RC2 · RC3, 각 Cell 1) | RC2 ≈177 h 단락 [판독] — 펠릿 품질 (결함) 이 밀도 하한 (RC2 > 94 % 로 가장 높음) 과 따로 논다 |
| 7 | Li\|LPSCl\|Li EIS 시간 변화 (RC2 0–200 h · RC3 0–480 h) | 계면 저항 성장 · 저주파 끝 0.20 → 0.36 / 0.18 → 0.45 kΩ·cm² [판독] |
| 8 | CCD 계단 (C/100 → 2C, RC2 파랑 · RC3 회색) | CCD 200 µA/cm² · 그 위 불안정 |
| 9 | 율 (RC1–4): 방전용량 · CE vs 사이클 + 전압 곡선 | 셀 수준 흩어짐 (C/10 CV 32 % [우리 산술]) |
| 10 | C/20 수명 (RC1–3): 방전용량 · CE + 전압 곡선 | ⚠ (a) RC1 = Fig 9a 와 같은 자료로 보임 [판독 · 숫자화] |
| Table 1 | 시험 정의 | EIS 조건 (1 MHz–1 Hz · 50 mV) · "−25 °C" 오기 |
| Table 2 | ★ 상대밀도 하한 · σ_ion (SS · Al/C · co-press) | ★★ 기관 차 vs 규약 차 |
| Table 3 | Li\|Li 수명 (h) | 3/4 > 200 h |
| Table 4 | R_b+gb · R_int vs 시간 (RC2 · RC3) | Li 전극 R_b+gb 125 Ω cm² (두 기관 같음) → 0.64 mS/cm [우리 산술] |
| Table 5 | CCD 과전압 | ASR 220–280 Ω cm² [우리 산술] · 단위 오기 |
| Table 6 | 율 (2 사이클 충/방전) | 기관 간 C/20 102–144 |
| Table 7 | 수명 (1 · 3 · 5 · 마지막) | 첫 사이클 CE 55–78 % [우리 산술] |

크롭: `litdb/figures/beutl2024_round_robin_coin_cell_sulfide_assb/` — fig_1–fig_10 · tab_1–tab_7 (17 장 · 300 dpi = 원 래스터 해상도) · `figures.json` 의 `note` 에 판독 메모.

## 6. Post-processing ★
- **무엇을 (저자)**: ZView 등가회로 맞춤 → R_b + R_gb → 식 (1) σ · Li\|Li 과전압으로 옴 법칙 σ · CCD = 과전압 선형성 · 전압 붕괴 · 용량 · CE (율 · 수명) · 겉보기 밀도 = 질량 / 기하 부피 → ÷ 1.64.  **통계 처리 없음** (평균 · SD · n · 오차막대 · 검정 없음) · 맞춤 오차 · 맞춤 R 값 표 없음 (Table 4 만).
- **도구**: ZView · 측정 장비 · 코인셀 공급사 = Table S1 [SI 미확보].
- **우리 후처리 (이 카드)**: 크롭 17 장 · 결정밀도 재계산 · TD 두 기준 공극 표 · wt% → vol% 역산 · 톤 → MPa · Fig 5 절편 판독 → σ · Table 4 → σ · Li\|Li 과전압 → ASR · CCD 기울기 ASR · 로딩 · 기관 간 평균 · SD · CV · Fig 9a ↔ 10a RC1 방전 점 숫자화 (눈금 보정: Fig 9a 86.1 px / 50 mAh g⁻¹ · Fig 10a 124.3 px / 50).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 시료 | 순수 LPSCl 펠릿 (NEI "fine") + SE-rich 복합 bilayer (SE 61.7–64.6 vol%) | 순수 SE 보정 침대 (세대 2 계획: r 0.5 µm 단일 크기) · ps45 복합 (NCM 81.6 : SE 18.4 wt) | 순수 SE 펠릿만 대조 가능 · 복합은 조성 영역이 다르다 |
| 성형압 · 상태 | 360 MPa · 3 (또는 2) min · **다이에서 꺼낸 뒤** 두께 | DEM 300 MPa 판 정지 + 이완 (세대 2 단계 2-5 = 다이 안) · 2-7 = 자유 표면 (out-of-die 꼴) | 압력 +20 % · 상태 다름 → 직접 같은 점 아님 |
| 공극 연산자 | 질량 / 기하 부피 ÷ TD (= ε_sphere 꼴 · 판정문 MV-03 · 세대 2 D9) | 표적 ε_union 10–13 % (1.64 기준) · ε_sphere 동반 기록 | 연산자 차 (DEM 순수 SE 에서 ≈11–12 %p, MV-03) 와 TD 차 (≈11 %p) 가 **같은 크기** |
| 진밀도 | 1.64 ("crystallographic") | 세대 2 D10 = SE 1.64 (1저자 보고 표 · 랩 측정법 미기록) · 세대 1 덱 2.0 | 같은 1.64 — 결정학 1.86 과 12 % 차 (§3-3) |
| σ_ion | SS · Al/C 0.3–0.4 · Li 0.5–0.7 [우리 산술] · co-press 0.9–1.8 mS/cm | σ₀ 보고 기준 **1.5 mS/cm** (1저자 10-12) · 솔버 상수 3.0 (봉인 32 · Cronau 2021 SI S2c 펠릿 평탄 하단 — CL-91) | **co-press 값만 σ₀ 1.5 근처** · 코인셀 SS 값은 접촉 지배 → σ₀ 근거로 쓰면 안 된다 |
| 측정 중 압력 | ≈0.2 MPa (코인셀 · ref [15]) | 접촉망 σ = 300 MPa 하중 상태의 침대 · 언로딩 등록 P_meas 1 MPa | 코인셀 자료와 맞대려면 **언로딩 끝 상태**가 대응 상태 |
| 접촉 저항 | R_int 를 등가회로로 분리 — 그러나 접촉 몫이 R_b+gb 로 샐 수 있다 (Fig 5 · Li 전극) | FULL (Holm R_c = 1/(2σa) 직렬) ↔ CF · 복셀 FV (계면 항 0) | 같은 물리의 두 얼굴 [추정] — §7-2 ③ |
| 통계 | 기관당 한 값 · SD 없음 | DEM seed 산포 · 등록 판정 | 그들 흩어짐은 반올림 해상도 |

### 7-2. ★★ 우리에게 — 10-14b 다섯 질문 (근거 쪽수)

**① SE 진밀도 1.64 의 출처** — §3-3.
- 이 논문의 1.64 = *"crystallographic density"* 라벨 · 인용 [37] (p.5) · [10,37] (p.9) · 측정 · 계산 기록 없음 (p.4 측정법 = 질량 / 기하 부피만) · 격자상수 없음 (p.3).
- 결정학 산술 1.859–1.860 g/cm³ (정본 세 카드의 a) · 비중병 1.874 (Ohno D) · NEI "fine" 진밀도 1.87 (Frankenberg) · Ohno D 펠릿 기하 밀도 1.655 > 1.64 → **1.64 는 "결정학" 이 아니고, 진밀도로 쓰면 실측 펠릿이 음의 공극이 되는 경우까지 있다** [우리 산술].  이 논문이 "cell history" 근거로 인용한 Ohno 2020 [63] 은 같은 Li₆PS₅Cl 에 이론밀도 **1.86** 을 쓴다 (정본 카드 Table S1).
- 사슬의 다음 고리 = [37] Zhou 2019 (*ACS Energy Lett* 4, 265) · [10] Tron 2023 (*Nanomaterials* 13, 327) 원문 확인 — **이 PDF 로는 닫히지 않는다 [미확인]**.
- ⇒ 세대 2 D10 (SE 1.64) 의 한정어 *"진밀도 미확인 — 결정학 1.86 과 12 % 차"* 는 이 논문으로 **강화**된다 (라벨이 붙어 퍼진 값이 산술과 어긋남).

**② 펠릿 제작 · 측정 조건** — §3-2 · §4-1 표가 답.  요지: NEI "fine" ≈1 µm (D50 없음 · 응집체) · 100 mg · ⌀10 mm 경화강 · 360 MPa · 3 min (그림 2 min) · 실온 냉간 · Ar · 두께 ≈0.8 mm (**꺼낸 뒤**) · ρ 1.49–1.60 · **ε 2.4–9.1 % (1.64) / 14.0–19.9 % (1.86)** [우리 산술].

**③ σ_ion ↔ 압력 · 온도** — 압력 · 온도 계열 **없음** · hot pressing **없음** · pressure-invariant 주장 **없음**.  있는 것:
- 성형압 360 MPa 한 값 · 측정 25 °C 한 값 · 측정 중 압력 ≈0.2 MPa (인용) — 저자는 이 낮은 압력을 *"avoid the fabrication of too optimistic data"* 로 정당화 (p.8) 하고, 성능 열세를 *"low pressure applied during operation"* 탓으로 돌린다 (p.13).
- **전극 접촉 규약 효과 (같은 펠릿 계열)**: SS · Al/C 0.3–0.4 → Li 0.5–0.7 [우리 산술] → co-press Al/C 0.9–1.8 mS/cm.  ★ 해석 [추정]: 차단 전극과 SE 가 점 접촉이면 접촉점 주위 SE 안의 **협착 (spreading) 저항**이 생기고, 그 영역은 SE 자신이라 **완화 시간 (ε/σ) 이 bulk 와 같아 주파수로 갈라지지 않는다** → "bulk" 절편 · 호에 섞여 σ 를 낮게 읽게 한다.  co-press 는 접촉 면적을 키워 그 몫을 줄인다.  = 우리 Holm R_c = 1/(2σa) 가 **전극/펠릿 경계에서** 나타난 것 — 우리 FULL ↔ CF 차 (접촉망 내부) 의 실험 쪽 그림자다.  ⚠ 정량 비교 아님 (CF/FULL 배수는 모델 내부 민감도 — L2 판정 `SELF-24` · `L2-07`).
- 문헌 맥락 (정본 카드): Ohno 2020 — 같은 배치 Li₆PS₅Cl 이 8 데이터셋 0.44–2.98 mS/cm · 주 원인 = 측정 중 압력 · Cronau 2021 µC-LPSCl 적층압 ≥146 MPa 평탄 2.88–3.46 (판독) · Doux 2020 NEI LPSCl 370 MPa 펠릿 2–2.5 mS/cm.  이 논문의 코인셀 SS 값 0.3–0.4 는 **그 분포의 아래 바깥** — "측정 압력 ↓ → σ ↓" 방향과 맞는다 (재료 · 배치는 다르다).

**④ 측정 재현성 — 그리고 SBE · DBE σ_e 비 2.77 을 다시 재야 하나**
- 이 논문: 기관당 한 값 · n · SD 없음 · 그림 = 기관당 한 셀 · EIS 1 MHz–1 Hz · 50 mV · 25 °C · 정상 상태 기준 [미확인] · 두께 한 값 (≈0.8 mm) — **두께 계열로 접촉 저항을 떼는 관행은 없다** · 접촉은 등가회로 R_int 로만 다룬다.
- 크기: **같은 규약에서 기관 차 ×1.33 (σ, 반올림 해상도)** ↔ **규약 (전극 접촉) 차 ×2.5 (본문 1.0 ÷ 0.4) – ×5.5 (표 1.8 ÷ SS 평균 0.325)** [우리 산술].
- 우리 질문에의 답 [우리 판단]: 이 논문에는 σ_e (DC 분극) 자료가 없다.  다만 **"접촉 · 가압 규약이 다르면 2.77 같은 비는 규약만으로도 생긴다"** 는 크기 감각을 준다.  ⇒ 다시 재기 전에 먼저 **kgy 측정에서 SBE · DBE 가 같은 전극 · 같은 성형/측정 압력 · 비슷한 두께로 쟀는지** 확인 (CLAUDE.md: *"측정 조건 미확인"*).  같았다면 무작위 흩어짐 (CV ≈15 % 급) 으로 2.77 이 생기기는 어렵다 → 1저자 결정 *"비는 맞추지 않음 · 대소만"* 과 정합.  비 자체를 쓰려면: 시료 ≥ 3 개씩 · 두 두께 (R_total = R_contact + l/(σA) 의 기울기로 접촉 몫 제거) · 같은 지그 · 측정 압력 기록.
- 경고: RC2 는 상대밀도 하한이 가장 높았는데 (> 94 %) Li\|Li 는 가장 먼저 단락 (175 h) — **밀도 하나로 펠릿 품질을 판정할 수 없다** (p.10 저자 해석: 결함 · 다이).

**⑤ 우리 DEM/MPM — 세대 2 순수 SE 보정 표적 · Heckel**
- 세대 2 계획 (작업 브랜치 `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` D6 · D9 · D10 · §4-3): 표적 = 순수 SE 침대 300 MPa + 이완 끝 **ε_union 10–13 %** (랩 표준 · 측정법 미확인) · 랩 펠릿 (질량 + 두께 · TD 1.64) 은 **ε_sphere** 로 대조 · 랩 EIS 펠릿 = LPSCl 0.1 g · ⌀10 · 300 MPa · 두께 0.75–0.85 mm 어림 · TD 1.64 반증 경계 t = 0.776 mm.
- 이 논문 = **같은 질량 · 지름**, 압력 360 MPa, 다이 밖.  ★ 비교는 **밀도로** 해야 TD 와 무관하다 (TD 는 같은 밀도를 공극으로 바꿀 때만 들어온다):

| 양 | 펠릿 밀도 ρ (g/cm³) | ε (TD 1.64) | ε (TD 1.86) | 표지 |
|---|---|---|---|---|
| 이 논문 · 360 MPa · 다이 밖 | **1.49–1.60** | 2.4–9.1 % | 14.0–19.9 % | [인쇄 ρ] p.5 · p.9 · [우리 산술] |
| 같은 계열 300 MPa 어림 (TD 1.86 기준 Heckel: ε × e^(K·60), K ≈32 × 10⁻⁴ MPa⁻¹ → ×1.21) | ≈1.41–1.54 | ≈6–14 % | ≈17–24 % | [우리 산술 · 어림 — K 는 `lee2025_heckel…` 상용 LPSCl in-die stage II 값 · 다른 분말 · 다른 상태] |
| 세대 2 표적 창 10–13 % 를 TD 1.64 로 정의했다면 (0.1 g · ⌀10 펠릿) | **1.427–1.476** (t 0.892–0.863 mm) | 10–13 % | **20.7–23.3 %** | [우리 산술] |
| 다이 안 (세대 2 단계 2-5) 으로 옮기면 | 회복 1.6–7 % 만큼 더 치밀 (−1.4 – −4 %p, 세대 2 계획 표 B) | — | — | [우리 산술 · 어림] |

  ⇒ **밀도 공간에서는 표적 창 (ρ 1.43–1.48) 이 이 논문 계열의 300 MPa 어림 (≈1.41–1.54) 안에 든다** — 표적의 *값* 은 같은 기하 외부 실험과 모순되지 않는다 (확인은 아님: 300 MPa · 다이 밖 실측이 없다).  갈리는 것은 그 밀도를 **공극으로 읽는 TD** 다: 같은 펠릿이 TD 1.64 로 10–13 %, 결정학 TD 로 **21–23 %**.  [우리 판단 — 결정은 1저자] DEM 공극은 기하 양이라 대조할 실험 공극도 실제 고체 부피 (결정학 · 실측 ≈1.86–1.87) 기준이어야 같은 양이다 — TD 1.64 로 읽으면 같은 펠릿이 ≈11 %p 덜 기공적으로 읽힌다 (세대 2 계획 §4-3 *"진밀도 결정이 먼저"* 와 같은 결론 · MV-03 정의 차 11–12 %p 와 같은 크기).
- 반증 시험과의 관계: 이 논문 펠릿은 함축 두께 0.80–0.85 mm 로 **TD 1.64 경계 (0.776 mm) 보다 두껍다** → 1.64 를 반증하지도 확인하지도 않는다.  1저자 랩 펠릿 (300 MPa) 이 이보다 얇게 (치밀하게) 나오면 그 자체로 이상 신호 (압력이 낮은데 더 치밀) — 두께를 잰 **상태** (다이 안 · 꺼낸 뒤 · 지그 안 100–150 MPa) 를 함께 적어야 비교된다.
- **다압력 Heckel 점 없음** (한 압력 · 예압 50 MPa 밀도 미보고).  한 점 기록만: 360 MPa 에서 ln(1/(1−D)) = 1.61–1.97 (TD 1.86) / 2.39–3.71 (TD 1.64) [우리 산술] — frame[3] 빈칸 (다압력 실험 Heckel) 을 채우지 않는다.
- frame[4] 원칙: 이 점으로 DEM E 를 맞추지 않는다 · 쓰려면 같은 상태 (다이 밖 = 세대 2 단계 2-7) · 같은 연산자 (ε_sphere) · 같은 TD 로.
- 입경 맥락 [판독 · 정본 카드]: NEI "fine" 의 "1 µm" 는 **1 차 입자** — SEM 응집체 (Fig 1b) · Frankenberg 2025 레이저 x50 17 ± 2 µm.  세대 2 의 "SE 1 µm (r 0.5 µm 단일 크기)" 는 1 차 입자 크기를 쓴 것이고, 실제 다짐은 **응집체 해체 + 재배열**을 지난다 — E 연화가 대신하는 기전 목록 (frame[2]) 의 한 항목이 실험 사진에 보인다 [추정].

### 7-3. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 측정 규약 (코인셀 · 차단 전극 · EIS 조건) · 순수 SE 펠릿의 한 압력 밀도 · 기관 간 흩어짐 · 셀 수준 재현성.
- **없는 것**: 압력 계열 (Heckel) · 하중 중 두께 · 언로딩 · 단면 공극 영상 · 접촉 · 미세구조 정량 · 모델.  ⇒ DEM (수송) 쪽에는 "실험 σ 를 어떤 상태 · 규약에서 쟀나" 의 체크리스트를, MPM (기계) 쪽에는 한 점 밀도만 준다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **1.64 의 사슬 추적** — 이 논문이 준 [37] · [10] 을 읽는 것이 진밀도 질문 (세대 2 D10 · 랩 펠릿 공극) 의 가장 싼 다음 걸음.  그 전까지 모든 공극을 **TD 1.64 · 1.86 두 줄로** 적는다 (§3-2 표 꼴).
2. **같은 기하 이웃점** — 0.1 g · ⌀10 mm · 360 MPa → 0.80–0.85 mm (함축).  1저자 랩 펠릿 (300 MPa) 두께를 잴 때 이 범위와 상태 (꺼낸 뒤) 를 나란히 적으면 TD 논쟁과 별개로 "분말 · 공정이 비슷한가" 를 먼저 본다.
3. **σ₀ 근거 고르기** — 코인셀 · 차단 전극 값 (0.3–0.4) 은 접촉 지배라 σ₀ 근거에서 뺀다 · co-press (0.9–1.8) 처럼 접촉을 만든 값만 σ₀ 1.5 mS/cm 와 같은 층으로 본다.
4. **σ_e 비 2.77** — 재측정보다 먼저 kgy 측정 조건 대조 (전극 · 압력 · 두께) · 비를 쓰려면 두 두께 + 반복 3.
5. **코인셀 자료와 맞대는 상태 = 언로딩 끝** — 0.2 MPa 작동 압력은 우리 언로딩 시험 (P_meas 1 MPa) 쪽이지 300 MPa 하중 상태가 아니다.
6. **밀도 ≠ 품질** — RC2 (밀도 하한 최고 · 단락 최초).  DEM 에서도 공극이 맞는 것이 결함 · 접촉 · 파괴 구조가 맞는 것을 뜻하지 않는다.
7. **"1 µm" SE 는 응집체** — DEM SE 크기 선택 · 연화 해석에서 1 차 입자와 다짐 단위를 구분해 적는다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a four-laboratory round robin with the same NEI Li₆PS₅Cl powder and protocol (100 mg, Ø10 mm, 360 MPa, coin cells at ≈0.2 MPa stack pressure as cited from their ref. 15), stainless-steel blocking electrodes gave 0.3–0.4 mS cm⁻¹ in every laboratory, whereas Al/C electrodes co-pressed at 360 MPa gave 1.8 mS cm⁻¹ (Table 2; the text states 1 × 10⁻³ S cm⁻¹) — the electrode-contact protocol moved the result more than the laboratory did (Beutl et al., *Electrochem. Sci. Adv.* 2024, 4, e2400004)."
- "Their '>90 % relative density' (≥1.49 g cm⁻³) is computed against 1.64 g cm⁻³, labelled crystallographic; with Z = 4 and a ≈ 9.86 Å the crystallographic density of Li₆PS₅Cl is ≈1.86 g cm⁻³, so the same pellets are 80–86 % dense, i.e. 14–20 % porous [our arithmetic]."
- 국문: *"같은 NEI Li₆PS₅Cl 펠릿 (100 mg · ⌀10 mm · 360 MPa) 을 네 기관이 코인셀로 재면 σ_ion 은 0.3–0.4 mS/cm 로 모이지만, 전극을 360 MPa 로 함께 누르면 1–1.8 mS/cm 가 된다 (Beutl 2024).  같은 논문의 '상대밀도 > 90 %' 는 결정학 밀도라 부른 1.64 g/cm³ 기준이며, 결정학 산술 (≈1.86) 로는 80–86 % 다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
**본문 안 불일치 · 오기 (인용 전 반드시 확인)**
1. **"crystallographic density 1.64"** — 결정학 산술 1.86 과 12 % 차 (§3-3) · 이 논문은 계산 · 측정하지 않았다.
2. 밀도 범위 *"1.6–1.50"* (p.5) ↔ *"at least 1.49"* (p.9).
3. co-press σ: **Table 2 1.8** ↔ 본문 **1 × 10⁻³** (p.9) — Fig 5b 절편은 1 쪽 (l = 0.8 mm 가정, [우리 산술]).
4. 성형 유지: 본문 **3 min** (p.4) ↔ Fig 4 **2 mins** · bilayer *"2–3 min"* (p.6).
5. Table 1 이온전도도 온도 **"−25 °C"** ↔ 본문 25 °C (p.8).
6. Table 5 머리 단위 **"mA cm⁻²"** — §2.8 (p.8) 정의로는 10–500 µA cm⁻².
7. 양극 vol% **"65:31:4 … NMC:Li6PS5Cl:C65"** — 산술상 SE 65 · NMC 31 (순서 뒤바뀜 · ρ_SE 1.64 로 환산) [우리 산술].
8. 프레스 *"Maassen MP15"* (p.4) ↔ 사진 "MP150" [판독].
9. NMC 입경 *"10–15 µm"* (p.3) ↔ SEM 2 µm 막대 대비 ≈1–4 µm 결정 [판독].
10. Fig 5a 범례 "SS \| LPSCl \| SE" · Fig 4c 전지에 *"Li metal foil attachment both side"*.
11. **Fig 10a (RC1 수명) = Fig 9a (RC1 율) 자료로 보임** [판독 · 숫자화 §3-7] · Table 7 RC2 *"140/137 (13th cycle)"* ↔ Fig 10b 13 번째 ≈95 [판독].
12. Fig 9 캡션 2.0 mAh/cm² ↔ 10 mg 양극 → 1.52 [우리 산술] · C/20 = 75 (p.8) ↔ 100 µA/cm² (p.13).
13. R_int 안정 기간 *"first 120 h"* (p.10) ↔ *"at least 200 h … 20 Ohm cm2"* (p.16) · CE *"99 %"* (p.13) ↔ *"up to 95 %"* (p.16).
14. 옴 법칙 σ 7.6 × 10⁻⁴ 은 인쇄 과전압 (20–25 mV) · 두께 (0.8 mm) 로 재현 안 됨 (≈0.48–0.60 mS/cm 가 나온다) [우리 산술].
15. 초록 *"can provide reproducible data compared to the other cell types"* — 이 논문은 다른 셀 형식과 비교하지 않았다 (주장의 근거가 이 논문 안에 없다).

**전이 한계**
- 한 압력 · 한 두께 · 한 온도 · 기관당 한 값 (n · SD 없음) · σ 한 자리 유효숫자 → **재현성 정량 근거로 약하다**.
- 0.2 MPa 는 인용값 (ref [15] · 두께 1.9 mm 기준) — 이 논문 셀의 실제 압력은 재지 않았다.
- 재료 = NEI "fine" (응집체 · D50 없음) · 단결정 비코팅 NMC90505 — 다른 분말 · CAM 에 수치 이식 금지.
- 다이 밖 두께 (회복 · 취출 포함) — 다이 안 (하중 중 · 이완 뒤) 값과 섞지 않는다.
- SI 미확보 — 기관별 장비 (Table S1) · 원 스펙트럼 (Fig S5) 없이 "같은 지시서" 의 실제 이행 정도를 확인할 수 없다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로, p.16–18) | 왜 |
|---|---|---|
| 10 | A. Tron, R. Hamid, N. Zhang, A. Beutl, *Nanomaterials* 2023, 13, 327. | ★★ 1.64 인용 사슬 (p.9) — 같은 그룹 |
| 15 | A. Tron, A. Orue, P. López-Aranguren, A. Beutl, *J Electrochem Soc* 2023, 170, 100525. | ★ 코인셀 0.2 MPa 의 출처 · CCD "hidden parameters" — 같은 묶음 10-14b `tron2023_lpscl_ccd_ambient_pressure` 로 카드화 중 (정본 미등록) |
| 25 | J.-M. Doux, Y. Yang, D. H. S. Tan, H. Nguyen, E. A. Wu, X. Wang, A. Banerjeea, Y. S. Meng, *J Mater Chem A* 2020, 8, 5049. | 압력 셀 설계 — ⚠ 정본 `doux2020_stack_pressure_assb` (Adv. Energy Mater.) 와 **다른 논문** · 미 digest |
| 36 | S. Randau, D. A. Weber, O. Kötz, R. Koerver, P. Braun, A. Weber, E. Ivers-Tiffée, T. Adermann, J. Kulisch, W. G. Zeier, F. H. Richter, J. Janek, *Nat Energy* 2020, 5, 259. | 성능 기준선 (*"inferior performance to reported values"*) · 낮은 종횡비 펠릿 |
| 37 | L. Zhou, K.-H. Park, X. Sun, F. Lalère, T. Adermann, P. Hartmann, L. Nazar, *ACS Energy Lett* 2019, 4, 265. | ★★ 1.64 인용 사슬 (p.5 · p.9) — INDEX.md 실험값 시트 No.3 에 행만 있음 (카드 없음) |
| 38 | Supplier Data-Polyetheretherketone (PEEK) (Goodfellow), azom.com ArticleID=1882 | PEEK 압축강도 118–130 MPa (다이 재료) |
| 42 | P. Vadhva, J. Hu, M. J. Johnson, R. Stocker, M. Braglia, D. J. L. Brett, A. J. E. Rettie, *ChemElectroChem* 2021, 8, 1930. | SSB EIS 50 mV 진폭의 근거 |
| 44 | A. Orue Mendizabal, M. Cheddadi, A. Tron, A. Beutl, P. López-Aranguren, *ACS Appl Energy Mater* 2023, 6, 11030. | ★ co-press 접촉 효과 · 등가회로의 근거 (p.8–9) |
| 45 | S. Narayanan, U. Ulissi, J. S. Gibson, Y. A. Chart, R. S. Weatherup, M. Pasta, *Nat Commun* 2022, 13, 7237. | Li/LPSCl 계면 EIS 해석 |
| 60 | E. Trevisanello, R. Ruess, F. Conforto, F. H. Richter, J. Janek, *Adv Energy Mater* 2021, 11, 2003400. | 정본 카드 있음 (`trevisanello2021_sc_pc_ncm_cracking_diffusion`) |
| 62 | A. Bielefeld, D. A. Weber, J. Janek, *J Phys Chem C* 2019, 123, 1626. | 정본 카드 있음 (`bielefeld2019_microstructural_modeling_composite_cathode`) — AM:SE 40:60–60:40 진술의 근거 |
| 63 | S. Ohno, T. Bernges, J. Buchheim, … W. G. Zeier, *ACS Energy Lett* 2020, 5, 910. | 정본 카드 있음 (`ohno2020…`, SI 만) — 같은 장르 round robin · 이론밀도 1.86 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-14)
- 본문 18 쪽 전부: 텍스트 층 (PyMuPDF · `pdftotext -layout`) + 그림 · 표 렌더 (300 dpi = 원 래스터 해상도).  DOI · 권 · 논문 번호 · 접수/승인일 = p.1 인쇄 · 호 6 = 쪽 여백 Wiley 다운로드 띠.  **SI 는 이 PDF 에 없다** (본문이 Figure S1–S7 · Table S1 을 인용).
- 인용문 (1.64 두 문장 · 0.8 mm · 360 MPa · 3 min · 0.2 MPa · co-press · 7.6 × 10⁻⁴ · 결론 재현성 문장) 은 텍스트 층에서 그대로 옮겼다.
- 표 1–7 은 텍스트 층 + 크롭 영상으로 칸마다 대조 (Table 1 "−25 °C" · Table 5 "mA" 단위는 영상에서도 그렇게 인쇄됨).
- 판독: Fig 1b 눈금 막대 (2 · 5 µm) · Fig 5 삽입 절편 · Fig 6–10 · Fig 9a ↔ 10a RC1 방전 점은 원 래스터에서 축 눈금 픽셀 위치 (Fig 9a 250 ↔ 0 = y 96.0 ↔ 526.5 · Fig 10a = 83.0 ↔ 704.5) 로 보정해 숫자화 — 사이클 1–4 차 ≤ 0.2 mAh/g · 사이클 5–10 은 CE 사각형에 가려 Fig 9a 쪽 점이 부분적 (눈으로 같은 값).
- 크롭 17 장: 그림 = 쪽의 임베디드 래스터 사각형 + ≈2.5 pt 여백 · 표 = 텍스트 블록 범위 — 전부 눈으로 확인 (잘림 없음).
- 정본 litdb 중복 확인: `git ls-tree` papers/ 438 파일 + `git grep -i` (`elsa.202400004` · `round-robin` · `round robin` · `Beutl` · `coin-type cell`) — 이 논문 카드 없음 (Ohno 2020 · Cronau 2021 · Boger 2023 의 "round robin" 언급만).

## 🔗 관련 카드
- 측정 신뢰도 · 압력: `ohno2020_interlab_ionic_conductivity_argyrodite` · `cronau2021_stack_pressure_ionic_conductivity` · `doux2020_stack_pressure_assb` · ⏳ `tron2023_lpscl_ccd_ambient_pressure` (같은 묶음 · 정본 미등록).
- 순수 SE 펠릿 공극 · 진밀도: `miss2026_insitu_conductivity_porosity_pressure_compaction` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` · `faka2026_particle_size_consolidation_strain_lpscl` · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure`.
- 결정학 격자상수: `adeli2019_halide_substitution_boosting_argyrodite` · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X`.
- 복합 양극 · CAM: `bielefeld2019_microstructural_modeling_composite_cathode` · `trevisanello2021_sc_pc_ncm_cracking_diffusion`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
