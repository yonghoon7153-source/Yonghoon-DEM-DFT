<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 참고 = shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md
     2026-11-26 신규 — 논문 에이전트 (API 배치 2026-11-26 #4). 본문 14 pp (369–382) + SI PDF 3 pp 글자층 전문 정독.
     그림: 크롭 11 장 (본문 Fig. 1–5 · SI Fig. S1–S5 · Table 1) 중 그림 10 장 전부를 원해상도로 봤다 · Table 1 은 PDF 글자층으로 읽었다.
     SI 1 (zip · UBIRA eData 원자료) 은 EIS 원자료 txt 4 개만 /tmp 에 풀어 주파수 범위 · 스윕 수 · 측정 시간만 셌다 (스크립트 실행 없음 · 다른 파일은 안 열었다 · 풀었던 폴더는 지웠다).
     ⚠ 작업 중 이 그림 폴더가 바깥 프로세스에 의해 한 번 지워져 (fig_1.png 만 남음) 같은 명령으로 다시 추출했다 — 크롭은 같은 결과다 (본 그림 목록 그대로).
     extract_figures.py 가 쓴 litdb/figures/_sources.json 은 두 번 다 git checkout 으로 되돌렸다.
     talk 인입 대기열 확인은 이 배치 지시 (공유 표 · talk 안 건드림) 에 따라 하지 않았다.
     Jeff Sakamoto 는 저자가 아니다 — 참고문헌 9 · 26 에만 나온다 (배지 대상 아님).
     ⚠ 이 논문은 계산이 0 이다 (DFT · MD 없음) — argyrodite 물성 4축 (A–D) 에 행을 만들 값이 없다 (σ · ESW · 탄성 · 띠틈 어느 것도 보고 안 함). -->

# Solid–liquid electrolyte interphases in quasi-solid-state lithium–sulfur batteries with argyrodite-type solid electrolyte separators — Mistry, …, Spencer-Jolly (*Faraday Discuss.* 2026, 269, 369–382)

> slug `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` · DOI `10.1039/d6fd00058d` · type `exp (FIB-SEM/EDX · time-resolved EIS (blocking/LE/SE/LE/blocking) · XPS (Al Kα) · HAXPES (Ga Kα 9252 eV) + QUASES 배경 모형 · Li–In 대칭셀 정전류 · PXRD; 계산 0)` · PDF `litdb/inbox/4. Solid-liquid electrolyte interphases in quasi-solid-state lithium-sulfur batteries with argyrodite-type solid electrolyte separators.pdf` (+ SI `4. Sup2) … .pdf` 3 pp · 원자료 `4. Sup1) … .zip`) · digested `2026-11-26` · status ✅
> elements: Li, P, S, Cl, C, O, F, N
> methods: XPS

> **저자**: **Jaimini Jessica Mistry** ᵃᵇ · Sramana Kundu ᵈ · Lechen Yang ᵇᶜ · Longlong Wang ᵉ · Mark Stockham ᵃᵇ · Ben F. Spencer ᵈ · **Dominic Spencer-Jolly\*** ᵃᵇ (교신)
> ᵃ School of Metallurgy and Materials, University of Birmingham · ᵇ The Faraday Institution (Harwell) · ᶜ Department of Materials, University of Oxford · ᵈ Henry Royce Institute / Photon Science Institute, University of Manchester · ᵉ Harbin Institute of Technology (Shenzhen)
> 접수 2026-04-07 · 수락 2026-05-11 · 게재 2026-05-27 · CC-BY 4.0 · *Faraday Discussions* 269 (토론회 논문 — 짧은 형식 · 5 그림)
> 기여 진술: J.J.M. 전 영역 · S.K. · B.F.S. XPS/HAXPES 측정 · 분석 · L.W. 보조 XPS · L.Y. FIB-SEM/EDX · M.P.S. EIS 해석 · D.S.J. 구상 · 지도
> 데이터: UBIRA eData `10.25500/edata.bham.00001736` (= 이 digest 의 SI 1 zip — EIS txt 4 · SEM tif 2 · 대칭셀 txt 1 · XPS `.vms`/`.sff` · docx 2). 영상 없음.
> **계보**: Busche 2016 *Nat. Chem.* (SLEI 개념 · ref 8) → Busche 2020 *Adv. Mater. Interfaces* (LiCGC/LiTFSI–DOL:DME ≈70 Ω cm² · 층상 SLEI · ref 16) → Woolley & Vargas-Barbosa 2024 *ACS Energy Lett.* (이온성 액체가 황화물 SE 와 덜 반응 · ref 31) → **본 논문** (Li₅.₅PS₄.₅Cl₁.₅ × 에테르 vs 이온성 액체 · 같은 그룹 Spencer-Jolly 의 Inorganics 2022 ref 15 연장)
> 🔗 **이어 읽기**: §14 — `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` · `cronk2026_lis_cathode_interphase_chemistry` · `kim2026_moisture_surface_degradation_lpscl_dryroom` · `deng2026_polysulfate_layer_moisture_oxidation_lpsc` · `banerjee2020_interfaces_interphases_assb_review` 외

---

## 0. 이 digest 를 읽는 법

**읽기축 (우리 트랙에서의 자리)**: 준고체 (quasi-solid-state) Li–S 전지 = **황화물 SE 분리막 + 양극 쪽 소량 액체 촉매전해질 (catholyte)**. 이 논문은 그 사이에 생기는 **고체–액체 전해질 계면상 (SLEI)** 하나만 본다. 양극 · 황 · 전위는 없다 — **전류를 안 흘린 화학 접촉 250 h** 가 주 실험이고, 전류는 대칭셀 100 h 하나뿐이다. 우리에게 닿는 곳은 ① 우리 SE 조성 (modelc Li₅.₄PS₄.₄Cl₁.₆) 과 거의 같은 **Li₅.₅PS₄.₅Cl₁.₅** 의 표면 화학 (PS₄³⁻ → SO₃²⁻/SO₄²⁻ · P₂Sₓ · Li₂Sₓ · LiCl) · ② **XPS 동정 · HAXPES 깊이** 방법 · ③ **EIS 등가회로로 계면 저항을 떼어 내는 법** (용량으로 과정 배정) 셋이다. 우리 DFT 수치와 맞댈 물성값은 없다 (§7).

**판정 요약 (§6 · §10 상세)**:

| 주장 | 판정 | 핵심 근거 |
|---|---|---|
| LiTFSI–DOL:DME 는 LPSCl 과 계속 반응해 수 µm 두께 · 구멍 난 SLEI 를 만든다 | ✅ 형태는 받친다 | `Fig. 1a,b` · `Fig. S1` — F/C/N/O 띠 ≈2–5 µm (figure-read) · S 결핍 띠 |
| DOL:DME 의 R_SLEI 가 ≈25 → ≈2000 Ω cm² (250 h) 로 커진다 | ✅ 방향 · ⚠ 마지막 점 | `Fig. 2c` — 250 h ≈1.9 kΩ cm² · **≈265 h 점은 ≈3.0 kΩ cm²** (figure-read · 본문 언급 없음) |
| EMIMTFSI 의 R_SLEI 는 150–220 Ω cm² 로 일정하다 | ✅ 일정함은 받친다 · ⚠ '더 낮다' 는 시간 조건부 | `Fig. 2c` — **처음 ≈20 h 동안은 DOL:DME 쪽이 같거나 더 낮다** (figure-read) |
| 두 SLEI 에 황산염 · 아황산염이 생긴다 | ⚠ **TFSI⁻ 잔류와 구분 안 됨** | S 2p 169 eV · S 1s 'SOₓ' 는 TFSI⁻ 의 –SO₂– 황과 겹친다 · 세척 여부 미기재 · C–F 293 eV 가 둘 다에 있다 (§10-1) |
| EMIMTFSI 계면은 ≈21 nm 의 Cl 없는 '유기 분해물' 덮개 + 그 밑 무기 분해층의 층상 구조 | ⚠ **잔류 이온성 액체 막으로도 같은 결과** | EMIMTFSI 는 진공에서 안 날아간다 · C 1s 의 'C–O' 는 EMIM⁺ 의 C–N 과 겹친다 (산소 없는 양이온) · 덮개 물질을 C 로 가정 (§10-2) |
| 대칭셀 100 h 에서 SLEI 가 안정하다 | ⚠ '안정' 은 맞지만 '저저항' 은 아니다 | `Fig. 5` — ≈0.19 V @ 0.1 mA cm⁻² ⇒ 겉보기 전체 ASR ≈1.9 kΩ cm² (우리 산수) — DOL:DME 의 250 h R_SLEI 와 같은 크기 |

**본 digest 에서 실제로 본 그림** — 크롭 11 장 중:

- 원해상도로 본 것 **10 장 (그림 전부)**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. S1` · `Fig. S2` · `Fig. S3` · `Fig. S4` · `Fig. S5`.
- **안 본 것**: `Table 1` (`tab_1.png` — 표라서 PDF 글자층으로 읽었다).
- 그림에서만 읽은 값은 **`figure-read ≈`** 로 적었다. 판독 정밀도는 눈금 간격의 ≈ ±5 % · 로그축은 ±0.1 decade.
- "(우리 산수)" = 논문 숫자끼리 계산한 값 · "(원자료)" = SI 1 zip 의 EIS txt 에서 센 값 · "(일반 문헌값)" = 이 논문에 없는 외부 상수.

---

## 1. 한 줄 요약

argyrodite **Li₅.₅PS₄.₅Cl₁.₅** 펠릿을 **1 M LiTFSI in DOL:DME (1:1)** 과 **0.5 M LiTFSI in EMIMTFSI** 에 250 h 담가 두면, 에테르 쪽은 수 µm 두께의 F/C/N/O 풍부 · 구멍 난 계면상이 자라고 계면 저항이 ≈25 → ≈2000 Ω cm² 로 계속 오르는 반면 (저자 해석: 생긴 폴리설파이드 · P₂Sₓ 가 에테르에 녹아 나가 새 SE 면을 계속 드러낸다), 이온성 액체 쪽은 SEM 으로 분해 안 되는 얇은 층에 150–220 Ω cm² 로 머물고 HAXPES 가 ≈21 nm 의 Cl 없는 덮개 아래 무기 분해층을 보여 '층상 SLEI' 를 이룬다 — 그래서 이온성 액체가 준고체 Li–S 의 촉매전해질 후보라고 결론짓는다 (Li–In 대칭셀 100 h 안정).

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | SE = Li₅.₅PS₄.₅Cl₁.₅ (MSE Supplies 상용 분말 · D50 2–3 µm) · LE1 = 1 M LiTFSI in DOL–DME 1:1 v/v (ELYTE 상용) · LE2 = 0.5 M LiTFSI in EMIMTFSI (LiTFSI TCI > 98.0 % · EMIMTFSI Proionic 전자급 ≥ 99.9 %) |
| 질문 | 준고체 Li–S 의 SE 분리막 / 액체 촉매전해질 계면에서 피할 수 없는 화학 반응이 만드는 SLEI 의 **두께 · 조성 · 저항 · 시간 안정성**이 액체 종류에 따라 어떻게 다른가? 기존 SLEI 연구는 대부분 **산화물 SE** (LLZO · LATP · LiCGC) 였다 |
| 왜 준고체 Li–S | 전고체 Li–S 는 황 양극의 ≈80 % 부피 팽창이 접촉 손실 · 균열을 만든다 (ref 5) · 액체 Li–S 는 셔틀 · 덴드라이트 · LiNO₃ 소모 — 그 절충 (ref 6, 7) |
| 왜 황화물 | 높은 σ · 덴드라이트 저항 · 낮은 밀도 (항공 등 질량 민감 용도 · ref 30–32) |
| 선행 | 에테르 + 황화물 = 두껍고 저항 큰 SLEI (ref 33–35) · 이온성 액체가 호환성을 높이고 SLEI 저항을 낮춘다 (Vargas-Barbosa · ref 31) |
| 답 (저자) | 이온성 액체 (EMIMTFSI 기반) 가 얇고 층상이며 저항이 시간에 안 변하는 SLEI 를 만든다 → 준고체 Li–S 촉매전해질로 유망 |
| 연구 유형 | 실험만 · **계산 0** |
| 우리와의 거리 | 물성 4축 수치 없음. SE 표면 분해 화학 (O 화된 S · LiCl) · XPS/HAXPES 동정 · EIS 계면 분리 방법만 닿는다 |

## 3. 핵심 수치 총정리 ★

> 규율: 전부 **문헌 소환값**이다 — 우리 db 절대값과 한 표에 섞지 않는다. 본문 명시값과 `figure-read ≈` 를 칸마다 구분했다. 온도는 25 °C.

### 3a. 계면 저항 (EIS · `Fig. 2c`)

| 양 | LiTFSI–DOL:DME | LiTFSI–EMIMTFSI | 출처 |
|---|---|---|---|
| R_SLEI 처음 | **∼25 Ω cm²** (본문) · figure-read ≈0.02 kΩ cm² | **150 Ω cm²** 하한 (본문) · figure-read ≈0.15 kΩ cm² | 본문 · `Fig. 2c` |
| R_SLEI 12 h | figure-read ≈0.15 kΩ cm² | figure-read ≈0.16 | `Fig. 2c` |
| R_SLEI 24 h | figure-read ≈0.22 | figure-read ≈0.20 | `Fig. 2c` (두 계 교차 ≈ 12–24 h) |
| R_SLEI 100 h | figure-read ≈0.37 | figure-read ≈0.15 | `Fig. 2c` |
| R_SLEI 150 h | figure-read ≈0.78 | figure-read ≈0.17 | `Fig. 2c` |
| R_SLEI 200 h | figure-read ≈1.6 | figure-read ≈0.20 | `Fig. 2c` |
| R_SLEI 250 h | **∼2000 Ω cm²** (본문) · figure-read ≈1.9 | **≤ 220 Ω cm²** (본문 '220 이후 안정') · figure-read ≈0.22 | 본문 · `Fig. 2c` |
| 마지막 점 (≈265 h) | figure-read **≈3.0 kΩ cm²** — 본문 언급 없음 | figure-read ≈0.22 | `Fig. 2c` |
| 비교 문헌값 | LiCGC / LiTFSI–DOL:DME **∼70 Ω cm² (170 h 후)** (ref 16 · 저자가 'best-in-class' 로 인용) | | 본문 |

- 측정 면적 = PTFE O-ring 내경 4 mm ⇒ 0.126 cm² (우리 산수). R_SLEI 가 SE 양쪽 두 계면의 합인지 한쪽인지는 **본문에 없다** (§10-4).

### 3b. 용량 (EIS 배정 · `Fig. S3`)

| 양 | DOL:DME | EMIMTFSI |
|---|---|---|
| C_bulk+gb (F cm⁻¹ · 기하 정규화) | figure-read ≈1.1×10⁻¹⁰ (0 h) → ≈5×10⁻¹¹ (250 h) → ≈2.7×10⁻¹¹ (≈265 h) — **꾸준히 줄어든다** | figure-read ≈1.4×10⁻¹⁰ 일정 |
| C_SLEI (F cm⁻²) | figure-read ≈1.5×10⁻⁷ (0 h) · ≈1.9×10⁻⁷ (12 h) → ≈2.6×10⁻⁸ (≥ 150 h) · ≈4×10⁻⁸ (≈265 h) | figure-read ≈6.5×10⁻⁸ (0 h) → ≈3.5×10⁻⁸ 일정 |
| 배정 띠 (그림의 음영) | 'SLEI' = 10⁻⁹–10⁻⁷ · 'bulk + GB' = 10⁻¹¹–10⁻⁹ (Irvine–Sinclair–West 기준 · ref 36) | 같음 |

- 캡션은 "capacitances remain largely stable" 이라 하지만 DOL:DME 의 처음 두 C_SLEI 점은 **배정 띠 (≤ 10⁻⁷) 밖**이고 C_bulk+gb 는 250 h 동안 반 decade 가까이 줄었다 (figure-read).

### 3c. 두께

| 양 | DOL:DME | EMIMTFSI | 방법 |
|---|---|---|---|
| SEM/EDX 계면층 | '**several microns**' (본문) · F 띠 figure-read ≈2–5 µm (10 µm 눈금 기준) | 'SEM 으로 분해 안 됨' (본문) | `Fig. 1` · `Fig. S1` |
| HAXPES Cl 없는 덮개 | **∼3 nm** (본문 '다른 시료' · 처녀 시료도 ∼3 nm) | **∼21 nm** (결론에선 '∼20 nm') | QUASES · `Fig. 4a` |
| HAXPES 계산 입력 | Cl 1s 운동에너지에서 IMFP **≈13 nm** (TPP2M) · 덮개 물질 = **C 로 가정** | | 실험 절 |

### 3d. XPS 결합에너지 (`Table 1` · C 1s 284.8 eV 기준)

| 영역 | BE (eV) | 배정 | 색 | ref |
|---|---|---|---|---|
| P 2p | 132.6 | P₂Sₓ | 노랑 | 48 |
| | 131.6 | PS₄³⁻ | 분홍 | |
| S 2p | 169.0 | SO₄²⁻ | 빨강 | 45, 49 |
| | 167.0 | SO₃²⁻ | 주황 | |
| | 164.0 | P₂Sₓ | 노랑 | |
| | 162.0 | Li₂Sₓ | 갈색 | |
| | 161.0 | PS₄³⁻ | 분홍 | |
| | 159.0 | Li₂S | 보라 | |
| Cl 2p | 198.4 | Li₅.₅PS₄.₅Cl₁.₅ / LiCl | 연두 | 50 |
| C 1s | 293.1 | C–F (–CF₃) | 남색 | 50, 51 |
| | 288.7 | C=O | 하늘 | |
| | 286.3 | C–O | 진녹 | |
| | 286.0 | O=C–O | 회색 | |
| | 284.8 | C–C | 청록 | |

- `Table 1` 은 2p 성분을 하나의 BE 로만 준다 (2p₃/₂ 인지 미기재). `Fig. 3b` 처녀 시료의 PS₄³⁻ 이중선 큰 봉우리는 figure-read ≈160.8 eV · 작은 봉우리 ≈162.0 eV 라 161.0 은 2p₃/₂ 로 읽힌다. **그런데 HAXPES 는 "S 2p₃/₂ = 162.0 eV 로 보정 — XPS 와 일관" 이라 적었다** — 표의 PS₄³⁻ 161.0 과 1 eV 어긋난다 (§10-6).
- O=C–O 286.0 < C–O 286.3 은 통상 순서 (O=C–O ≈289) 와 반대다 — 오기로 보인다 (그림 `Fig. 3d` 는 C–O 와 O=C–O 를 같은 회녹 칸 ≈286–288 에 묶었다).

### 3e. 대칭셀 (`Fig. 5`)

| 양 | 값 |
|---|---|
| 구성 | Li–In / LiTFSI–EMIMTFSI (유리섬유) / Li₅.₅PS₄.₅Cl₁.₅ / LiTFSI–EMIMTFSI (유리섬유) / Li–In · 5 mm · ≈10 MPa |
| 조건 | 0.1 mA cm⁻² · 반주기당 0.1 mAh cm⁻² (= 1 h · 우리 산수) · 100 h · 25 °C ⇒ ≈50 주기 |
| 전압 | 본문: 처음 20 h 에 ≈200 mV 로 오른 뒤 안정 · figure-read: + 쪽 ≈0.11 (시작) → ≈0.22 (≈18 h) → ≈0.18–0.19 (≥ 45 h) · − 쪽 ≈ −0.12 → ≈ −0.17 → ≈ −0.15 V |
| 겉보기 ASR | ≈0.19 V / 0.1 mA cm⁻² ≈ **1.9 kΩ cm²** (우리 산수 · 반주기 끝 값 · 정상상태 아님) |

### 3f. 원자료로 센 것 (SI 1 zip · EIS txt 4 개)

| 항목 | 값 (원자료) | 본문 |
|---|---|---|
| 주파수 범위 | **1 MHz – 0.1 Hz** · 스윕당 71 점 (10 점/decade) | "**5 kHz to 50 Hz**" — 어긋남 (`Fig. S2` 색 막대 상한 ≈log f 3.7 ≈ 5 kHz 이므로 **그림 · 맞춤은 ≤ 5 kHz 로 자른 것**으로 보임 · 하한은 `Fig. 2` 의 '10 Hz' 화살표가 있으니 50 Hz 가 아님) |
| 스윕 | 각 계 파일 _01 = 101 스윕 / 30.2 h · _03 = 19 스윕 / 221.8 h ⇒ ≈252 h | 250 h |
| 측정 날짜 (파일 이름) | DOL:DME `17102025` (2025-10-17) · EMIMTFSI `04122025` (2025-12-04) | 미기재 — 두 계가 **다른 날 · 다른 펠릿** (짝 실험 아님 · 반복 n 미기재) |
| DOL:DME 첫 스윕 1 MHz 실수부 | 117.2 Ω ⇒ ×0.126 cm² ≈ 15 Ω cm² (우리 산수 · 액체 + SE 직렬저항 포함) | — |

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 재료
- Li₅.₅PS₄.₅Cl₁.₅ 상용 분말 (MSE Supplies · D50 2–3 µm). **PXRD** Bruker D6 · **Co 선원** · 슬릿 0.5 mm · 0.0206° 간격 · 10–90° (그림 `Fig. S5` 는 10–70° 만) · 1 h · 기밀 홀더. 불순물 Li₂CO₃ · Li₂S · LiCl (캡션: 수분 부반응일 수 있음).
- LE1 1 M LiTFSI DOL:DME 1:1 (ELYTE) · LE2 0.5 M LiTFSI in EMIMTFSI.
- Li–In: Li 리본 100 µm + In 박 250 µm 을 접어 압연 → 100 µm 합금박. 모든 준비 Ar 글러브박스 (H₂O, O₂ < 0.1 ppm).

### 4b. 침지 시료 (FIB-SEM · XPS · HAXPES)
- 'Li₅.₅PS₄.₅Cl₁.₅ disk' 를 액체에 **250 h** 침지. **디스크 제조 조건 · 액체 부피 · 침지 후 세척 (세척 용매 · 건조) 은 미기재** — 표면 분석 해석에 결정적인 빈칸 (§10-1, 2).
- 공기 차단 이송 홀더 (FIB).

### 4c. EIS (time-resolved)
- 셀: **차단전극 (SUS) / LE / SE / LE / 차단전극** · 맞춤 Swagelok 형 · PTFE O-ring 내경 4 mm 가 계면 면적을 정의.
- SE 펠릿: 205 mg · 지름 10 mm · ≈400 MPa 일축 냉간 압착.
- Biologic VMP3 · PEIS · 10 mV 교란 · 10 점/decade · 본문 '5 kHz–50 Hz' (원자료 1 MHz–0.1 Hz · §3f) · 25 °C · 250 h · 무전류.
- 등가회로 (`Fig. S2a`): **(R_bulk+gb C_bulk+gb)(R_SLEI C_SLEI) CPE** — 그림 기호는 C 자리에 CPE 모양 (화살표 두 개) 이다 · **직렬 저항 (액체층 · 접촉) 항이 없다** · ZView 맞춤.
- 과정 배정은 특성 용량 (Irvine–Sinclair–West) 으로 (`Fig. S3`).

### 4d. 대칭셀
- 5 mm PEEK 셀 · SE 40 mg ≈400 MPa · 양쪽에 유리섬유 (Whatman) + **"2 mL"** 액체 (5 mm 원판에 2 mL 는 비현실적 — 2 µL 의 오기로 보임 · §10-7) · Li–In 5 mm 100 µm · Cu 집전체 · ≈10 MPa · 0.1 mA cm⁻² · 0.1 mAh cm⁻² · 25 °C · 100 h.

### 4e. FIB-SEM / EDX
- Thermo Fisher Helios G4 Plasma-FIB · 30 kV · 15 nA 단면 가공 · EDX X-max 150 SDD (Oxford) · Aztec.

### 4f. XPS / HAXPES
- HAXPES-Lab (Scienta Omicron) · 단색 **Ga Kα 9252 eV** (Excillum MetalJet · 3.57 mA · 250 W · 50 µm) · EW-4000 분석기 · 기저 진공 5×10⁻¹⁰ mbar · 입구 슬릿 1.5 mm · 통과에너지 survey 500 / core 100 eV (분해능 2.0 / 0.6 eV).
- 같은 자리의 단색 Al Kα 1486 eV (20 mA · 300 W · 빔 ≈1 mm) · 통과에너지 150 / 50 eV (≈0.6 / 0.3 eV).
- BE 보정: XPS = C 1s 284.8 eV · HAXPES = **S 2p₃/₂ 162.0 eV**.
- CasaXPS Voigt 근사 맞춤 · HAXPES 상대감도 = ref 44, 45 · XPS = Scofield.
- **덮개 두께**: QUASES-Analyze 로 Cl 1s 아래 비탄성 배경을 모형화 — IMFP ≈13 nm (TPP2M · Cl 1s 운동에너지) · 덮개 = 탄소 근사. 저자 단서: "상대적 매몰 깊이 차는 유효하지만 절대 두께는 뽑기 어렵다".

### 4g. 계산
- **없음.** DFT · MD · 열역학 상 계산 · 반응 에너지 어느 것도 없다. 분해 경로는 전부 XPS 동정 + 문헌 유추다.

## 5. 결과 — 절별 상세 (그림 실독 포함 · 모든 수치)

### 5.1 DOL:DME 계면 — 형태 (`Fig. 1a,b`, `Fig. S1`)

- **본문**: 250 h 침지 단면에서 SE 표면이 거칠고 구멍 투성이 (pitted) · EDX 상 수 µm 의 화학적으로 다른 층 — F 풍부 (노랑) + C (주황) · N (파랑) · O (빨강) · 국소적으로 S (초록) · P (분홍) · Cl (보라). SE 벌크는 S · P · Cl 이 강하다.
- **그림 실독 (`Fig. 1a`)**: 단면 (파란 점선 상자 · 10 µm 눈금) 위쪽 가장자리가 해면 모양으로 부서져 있고 가공면 위로 흙덩이 같은 덩어리 층이 얹혀 있다. 단면 내부에도 작은 구멍 (어두운 점) 이 흩어져 있다.
- **`Fig. 1b`** (Cl 보라 + F 노랑 겹침): 맨 위 띠가 노랑 — 두께 figure-read ≈2–5 µm (곳에 따라 다름 · 경계가 들쭉날쭉) · 그 아래는 고른 Cl 보라.
- **`Fig. S1` (원소별 · 왼쪽 = DOL:DME)**: C · N · F 가 위쪽 ≈3–5 µm 띠에 몰려 있고 (figure-read) · **S 는 같은 띠에서 어둡다 (결핍)** · O 는 띠 + 단면 곳곳의 밝은 점 · P 는 위쪽이 약간 옅음 · Cl 은 거의 고름. F 맵에는 **단면 아래 가장자리에도** 노란 띠가 있다 — 가공 재증착 또는 다른 면의 액체 흔적으로 보인다 (논문 언급 없음).

### 5.2 DOL:DME 계면 — 저항 (`Fig. 2a,c`, `Fig. S2b`, `Fig. S3`)

- **본문**: 시간이 갈수록 임피던스가 계속 커진다. 등가회로 3 기여 = ① 벌크 + 입계 (시상수 겹쳐 하나로) · ② SLEI 통과 · ③ 차단전극 / LE 계면의 용량성. 증가는 R_SLEI 가 **∼25 → ∼2000 Ω cm²** 로 커진 탓이다.
- **`Fig. 2a` 실독**: Nyquist (kΩ cm² 축 · 0–6) · 색 = 시간 0 (연함) → 250 h (진함). 마지막 스펙트럼은 Re 축 ≈1.3 kΩ cm² 에서 시작 (figure-read) 해서 1.5 kHz → 100 Hz → 10 Hz 화살표를 지나 ≈6 kΩ cm² 까지 간다. 초기 스펙트럼은 원점 근처에서 거의 직선으로 솟는다 (삽입 0–0.6).
- **`Fig. S2b` 실독**: 'Initial Cycle' 은 원점에서 바로 ≈45° 이상으로 솟아 반원이 거의 안 보이고, 'Final Cycle – 250 Hours' 는 **고주파 절편이 ≈1.3 kΩ cm²** 로 옮겨 간 뒤 납작한 호 (≈1.3 → ≈4.5) 와 저주파 꼬리. ⇒ 250 h 에 커진 것은 R_SLEI 호만이 아니라 **고주파 절편 (회로상 R_bulk+gb 에 흡수되는 직렬 성분)** 도 ≈1.3 kΩ cm² 만큼이다 (figure-read) — 본문은 이 부분을 말하지 않는다 (§10-3).
- **`Fig. 2c` 실독**: §3a 표. DOL:DME 는 ≈100 h 까지 완만 (≈0.37) · 그 뒤 가속 (150 h ≈0.78 · 200 h ≈1.6) · 210–250 h ≈1.8–2.0 정체 · **≈265 h 점 ≈3.0** (본문 언급 없음).
- **`Fig. S3` 실독**: §3b 표. C_bulk+gb 가 계속 줄어든다 — 기하 정규화 용량이 줄면 '같은 두께 펠릿의 유전 응답' 이 아니라 **유효 두께가 늘거나 접촉 면적이 줄었다**는 뜻일 수 있다 (해석은 우리 것 · 논문 언급 없음).

### 5.3 DOL:DME 계면 — 화학 (`Fig. 3`, `Table 1`)

- **본문**: 가장 큰 변화는 S 2p. 처녀 시료 = PS₄³⁻ 강한 이중선 (분홍) + 소량 Li₂S (보라) · 아황산 (주황). 침지 후 **아황산 · 황산 (빨강) 상대량 급증** → "황화물 SE 와 산소 함유 DOL:DME 의 화학 반응". C 1s 에서 C–F (남색) 증가 → "LiTFSI 염의 석출 또는 분해". P 2p · Cl 2p 는 큰 변화 없음 (P 2p 는 PS₄³⁻ 만 · Cl 2p 는 한 이중선). Cl 은 LPSCl 과 LiCl 의 BE 가 거의 같아 구분 불가 — 문맥상 LiCl 이 생겼을 것 (ref 37).
- **폴리설파이드 부재**: P₂Sₓ · Li₂Sₓ 증거 없음 — 예상 분해물 (ref 33) 인데 안 보이는 것은 **에테르에 녹아 나갔기 때문** (문헌 지식). 그 용해가 두껍고 구멍 난 형태의 원인일 수 있다.
- **`Fig. 3` 실독 (가운데 줄 = DOL:DME)**:
  - (a) P 2p: PS₄³⁻ 이중선이 남되 처녀 대비 세기가 약 1/3 (figure-read · 같은 세로 눈금 가정) · 133–134 eV 쪽에 넓은 꼬리.
  - (b) S 2p: **169–170 eV 이중선 (SO₄) 이 주봉** · 167 eV SO₃ 소량 · 161 eV PS₄³⁻ 는 작은 혹으로 남음.
  - (c) Cl 2p: 이중선 (≈198.4 / ≈200.0) 이 처녀 대비 약 절반 (figure-read).
  - (d) C 1s: C–C 284.8 주봉 · C–F ≈293 · C=O ≈289 소량.

### 5.4 EMIMTFSI 계면 — 형태 · 저항 (`Fig. 1c,d`, `Fig. 2b,c`, `Fig. S2c`)

- **본문**: 2 차 전자상은 비교적 매끈 · EDX 는 F 풍부 + C 풍부 층 — DOL:DME 보다 훨씬 얇아 SEM 으로 두께 분해 불가. 임피던스는 시간에 거의 불변 · R_SLEI 150–220 Ω cm² (250 h) — DOL:DME 보다 낮고 garnet + 통상 액체 조합보다도 낮으며 LiCGC / LiTFSI–DOL:DME (∼70 Ω cm² · 170 h) 같은 'best-in-class' 와 같은 크기.
- **`Fig. 1c` 실독**: 단면 윗가장자리가 깔끔하고 표면은 잔물결 같은 결 (덩어리 층 없음). **`Fig. 1d`**: 단면 전체가 Cl 보라 · 맨 위에 F 노랑 띠가 눈에 안 띈다.
- **`Fig. S1` 실독 (오른쪽 = EMIMTFSI)**: C · N · O 맵은 어둡고 고름 · **F 맵은 위 띠가 아니라 단면 전체에 퍼진 점 무늬** (figure-read) — 표면층이 아니라 **펠릿 안쪽 기공으로 액체가 스며든 흔적**일 수 있다 (우리 해석 · 논문은 'F 풍부 층' 이라고만). S · P · Cl 고름.
- **`Fig. 2b` 실독**: 축이 0–0.6 kΩ cm² 로 DOL:DME (0–6) 의 1/10. 모든 시간의 스펙트럼이 거의 한 곡선 위 — 원점 근처 (≈0.02) 에서 시작해 1.5 kHz → 100 Hz (≈0.13, 0.11) → 10 Hz (≈0.33, 0.30) 로 거의 45°+ 직선에 가깝게 오른다 (figure-read). **뚜렷한 반원이 없다** — R_SLEI 150–220 Ω cm² 는 반원이 아니라 휘어짐 정도에서 뽑힌 값이다 (§10-3).
- **`Fig. S2c` 실독**: 초기 · 250 h 두 곡선이 Re ≈0.1 kΩ cm² 아래에서 겹치고 그 위에서 갈린다 (250 h 쪽이 같은 Im 에서 Re 가 조금 큼). 맞춤선은 점을 잘 따른다.

### 5.5 EMIMTFSI 계면 — 화학 (`Fig. 3` 윗줄)

- **본문**: FIB-SEM-EDX · EIS 로는 반응이 적어 보이나 XPS 는 반응을 보여 준다. S 2p 에 황산 · 아황산 (DOL:DME 와 같음) + **P₂Sₓ · Li₂Sₓ 가 계면상에 남는다** (이온성 액체에 안 녹으므로). P 2p 에서 P₂Sₓ 고농도 확인. **Cl 종의 상대 세기 · 원자 % 가 처녀 · DOL:DME 시료보다 낮다** → Janek 그룹 (ref 16) 처럼 유기 · 염 분해물이 위를 덮는 층상 구조 · LPSCl 과 LiCl 이 그 아래 묻혔을 것.
- **`Fig. 3` 실독 (윗줄 = EMIMTFSI)**:
  - (a) P 2p: 주성분이 **P₂Sₓ (≈132.5–134 eV · 노랑 두 성분)** · PS₄³⁻ (≈131.5) 는 작은 혹.
  - (b) S 2p: **SO₄ 이중선 (≈169.3 / ≈170.5) 이 압도적** — DOL:DME 보다 큼 · SO₃ 작음 · 162–165 eV (Li₂Sₓ · P₂Sₓ) 낮은 언덕 · PS₄³⁻ ≈161 작은 혹.
  - (c) Cl 2p: 거의 평평 — 처녀 대비 1/10 수준 (figure-read).
  - (d) C 1s: C–C 284.8 · **'C–O' 성분 ≈287 이 큼** · C–F ≈293 이 DOL:DME 보다 큼 · C=O 없음.
- 원자 % 표는 본문 · SI 어디에도 없다 ('atomic percentage' 를 말하지만 숫자를 안 준다).

### 5.6 HAXPES — 덮개 두께 (`Fig. 4`, `Fig. S4`)

- **본문**: 경 X 선이라 수십 nm 를 본다. Cl 은 SE 와 그 분해물에만 있으므로 Cl 1s 가 위 유기층 두께의 탐침. Cl 1s 봉우리 대비 비탄성 배경이 크면 Cl 종이 더 깊이 묻힌 것. EMIMTFSI (주황) 가 처녀 (보라) · DOL:DME (파랑) 보다 배경/봉우리 비가 훨씬 크다 → 배경 모형 결과 Cl 없는 덮개 **∼21 nm** (다른 시료 **∼3 nm**) → `Fig. 4b` 의 층상 SLEI (위 = 이온성 액체 · 염 분해물 · 아래 = 무기 분해물).
- **`Fig. 4a` 실독** (가로축 = **운동에너지** 6500 → 5200 eV): 처녀 · DOL:DME 는 ≈6420 eV 에 날카로운 Cl 1s 봉우리 + 그 아래쪽 (낮은 KE) 으로 점점 **줄어드는** 배경. EMIMTFSI 는 봉우리가 잡음 수준으로 작고 배경이 낮은 KE 쪽으로 **오히려 올라간다** (figure-read) — 전형적인 '깊이 묻힌 방출원' 모양. 검은 선 = QUASES 배경 맞춤.
- **`Fig. 4b`**: 개념도 — XPS 빔은 위 유기층 (빨강/주황/노랑) 까지만 · HAXPES 빔은 무기층 (파랑/연두) · SE 벌크 (진녹) 까지. **캡션은 "HAXPES penetrates 10s of microns"** 라 적었는데 본문 · 실험 절은 '수십 nm' (IMFP 13 nm) — 캡션 단위 오기 (§10-6).
- **`Fig. S4` 실독**:
  - (a) S 1s: 처녀 = PS₄³⁻ 단봉 ≈2469.3 eV · DOL:DME = **PS₄³⁻ ≈2468.3 큼 + SOₓ ≈2477.5 + 작은 어깨 ≈2475.5** · EMIMTFSI = **SOₓ ≈2477.7 이 주봉** · Li₂Sₓ ≈2471 · PS₄³⁻ ≈2469 둘 다 작음 (figure-read). ⇒ HAXPES 깊이 (수십 nm) 에서도 EMIMTFSI 시료는 PS₄³⁻ 가 거의 안 보인다 — '21 nm 덮개' 보다 **산화 S 가 더 깊이** 있거나 덮개가 S 를 품는다 (TFSI⁻ 는 S 를 품는다 · §10-2).
  - (b) Cl 1s: 처녀 ≈2821.2 (작음) · **DOL:DME ≈2820.1 이 처녀보다 크다** · EMIMTFSI ≈2820.6 아주 작음 (figure-read). DOL:DME 에서 Cl 이 표면 쪽에 **농화**된 것 (LiCl 석출?) 으로 읽히지만 논문은 다루지 않는다.

### 5.7 대칭셀 (`Fig. 5`)

- **본문**: 무전류 안정을 확인했으니 전류 하에서도 본다. Li–In 은 Li 금속보다 (전기)화학 안정 · 덴드라이트 저항이 커서 Li–In / LE 계면의 부수 전압 효과를 줄이는 모델 계. 0.1 mA cm⁻² · 100 h — 처음 20 h 에 ≈200 mV 로 오른 뒤 안정 → 동적 조건에서도 SLEI 가 안정 (EIS `Fig. 2b` 와 일관).
- **실독**: 전압 축 ±0.6 V · 시간 0–100 h · 주기 ≈48–50 개 (반주기 1 h 와 맞음). 각 반주기 안에서 전압이 **평탄하지 않고 계속 오른다** (톱니 모양) — 정상상태 옴 분극이 아니라 농도 분극 · 용량성 응답이 섞인 꼴. + 쪽 최고 ≈0.22 V (≈18 h) · − 쪽 최저 ≈ −0.17 V (≈18 h) → 45 h 이후 ≈ +0.18–0.19 / −0.15 V 로 평탄 (figure-read). **+/− 가 비대칭** (≈0.04 V 차) — 두 Li–In 전극 또는 두 SLEI 가 같지 않다는 뜻인데 논문은 설명하지 않는다.
- (우리 산수) 0.19 V / 0.1 mA cm⁻² ≈ 1.9 kΩ cm² — EIS 의 R_SLEI (0.15–0.22 kΩ cm²) 의 ≈9 배. 차이는 Li–In / LE 계면 · 유리섬유 속 액체 · SE 펠릿 벌크 · 확산 분극의 몫이다 — **이 셀은 SLEI 만 분리해 재지 못한다** (§10-5).

### 5.8 PXRD (`Fig. S5`)

- **실독**: 10–70° (Co) · 가장 큰 봉우리 ≈30° (LPSCl 별표 + Li₂S 초승달 겹침 표시) 가 매우 넓다 · 그 왼쪽 ≈26–28° 에 넓은 어깨 (Li₂CO₃ 타원 자리 근처) · 날카로운 작은 봉우리 ≈18.3 · 21.2 · 35.4 · 36.9 · 53.2 · 56.7 · 62.2° (figure-read). LiCl 다이아몬드 자리 ≈41 · 59.5° 에 아주 작은 혹.
- 본문 '10–90°' ↔ 그림 '10–70°' (그림이 잘렸거나 측정 범위 오기). 최강 봉우리 폭이 넓은 것은 결정성 · 기밀 홀더 돔 배경 · 상 겹침 중 무엇인지 논문이 말하지 않는다.

## 6. 메커니즘 · 논증 흐름 — 판정

```
(전제) 황화물 SE 는 액체 전해질과 반응해 SLEI 를 반드시 만든다 (ref 8)
   │
   ├─ 에테르 (LiTFSI–DOL:DME)
   │    ① LPSCl + 산소 함유 용매 → SO₃²⁻ / SO₄²⁻ (XPS S 2p)                   ⚠ TFSI⁻ 의 S 와 겹침 (§10-1)
   │    ② 예상 분해물 P₂Sₓ · Li₂Sₓ 는 에테르에 녹아 빠진다 (XPS 에 부재)        ⚠ '부재' 로부터의 추론 · 액체 쪽 분석 없음
   │    ③ 녹아 나간 자리 → 새 SE 면 노출 → 반응 반복 (자기 유지 부식)         ✅ 형태 (구멍 · 수 µm) 와 정합 · 직접 증거는 없음
   │    ④ 두껍고 · 불균일 · 저항 큰 SLEI · R_SLEI 계속 증가 (25 → 2000 Ω cm²)   ✅ EIS · ⚠ 직렬 성분 증가 미해석 (§10-3)
   │
   └─ 이온성 액체 (LiTFSI–EMIMTFSI)
        ① 역시 SO₃²⁻/SO₄²⁻ 생성 (XPS)                                          ⚠ 같은 겹침 · 더 심함 (잔류 IL)
        ② P₂Sₓ · Li₂Sₓ 는 IL 에 안 녹아 계면상에 남는다 (P 2p · S 2p)           ✅ 이 두 시료의 가장 뚜렷한 차이
        ③ 녹아 나가지 않으니 자기 제한적 (얇음 · 저항 일정)                     ✅ EIS 일정 · SEM 얇음과 정합
        ④ 위 ≈21 nm Cl 없는 유기/염 분해층 + 아래 무기층 (LiCl 등) = 층상     ⚠ 잔류 IL 막 대안 미배제 (§10-2)
        ⑤ 전류 하에서도 안정 (대칭셀)                                           ⚠ 안정은 맞음 · 저항 분리 안 됨
```

- **논증의 뼈대는 '용해도 대비'** 다: 같은 염 (LiTFSI) · 같은 SE 에서 용매만 바꿨더니 (i) 분해물이 녹느냐 · 남느냐가 갈리고 (ii) 그것이 계면이 자기 제한적이냐 · 진행형이냐를 정한다. 이 뼈대는 형태 (`Fig. 1`) · 저항 시간 거동 (`Fig. 2c`) · P₂Sₓ/Li₂Sₓ 잔존 여부 (`Fig. 3a,b`) 세 독립 관찰이 같은 방향을 가리켜 **정성적으로는 설득력이 있다**.
- 약한 고리는 **분석 화학** 쪽이다 — 황산/아황산 동정과 '유기 분해 덮개' 둘 다 **씻지 않은 (또는 세척 미기재) 액체 잔류**로도 설명되고, 그 대안을 배제하는 실험 (세척 전후 · N 1s · F 1s · 순수 액체 대조) 이 없다.
- 용매 효과와 **염 농도 (1 M vs 0.5 M)** · **점도** · **용존 미량 수분/산소** 가 함께 바뀌었다 — '용매 종류' 하나의 효과로 단정할 수 없다 (§10-8).

## 7. 우리 계산 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

> 규율: 문헌 수치는 소환값이다 — 우리 절대값과 한 표에 놓지 않는다. 이 논문은 **계산 0 · SE 벌크 물성 0** 이라 A–D 4축 비교 행이 없다. 아래는 **조성 · 개념 · 방법**만 맞댄다.

### 7a. 조성 대조
| 항목 | 이 논문 | 우리 | 비고 |
|---|---|---|---|
| SE 조성 | Li₅.₅PS₄.₅Cl₁.₅ (상용 · 실측 조성 분석 없음 · PXRD 불순물 Li₂CO₃/Li₂S/LiCl) | modelc = Li₅.₄PS₄.₄Cl₁.₆ (DFT 모델 셀) | Cl 0.1 차 · '같은 계열의 Cl-rich argyrodite' 로만 연결 — 이 논문은 σ · ESW · 탄성 · 띠틈을 하나도 안 냈으므로 수치 대조 없음 |
| 전위 | 무전류 화학 접촉 (EIS 는 10 mV 교란 · 대칭셀은 Li–In 대비 ≈ ±0.2 V) | 우리 산화 onset 은 grand-potential 층① (S²⁻ 한계 · 값은 `our_dft_baseline.md` ESW 절) | **축이 다르다** — 이 논문의 SO₄²⁻ 는 전기화학 산화가 아니라 액체 (용매 · 염 · 불순물 O) 와의 **화학 반응** 산물이다. 우리 ESW 축 ① 과 엮지 않는다 |

### 7b. 개념 대조 — 우리 계와 닿는 곳
- **O 화된 S (SO₃²⁻/SO₄²⁻) 는 우리 CEI · 수분 · O 대조 계산과 같은 산물군**이다. 우리 쪽: CEI O 단독 대조 frontier (`kb/concepts/se_redox_frontier.md` 4 장 ④ — Li₃PO₄ → Li₄P₂O₇ → LiPO₃ → P₂O₅ 사다리) · CEI 생성물 띠틈 카드 (`db/properties/cei_product_gap_card_2026_10_27.json` — Li₂SO₄ 가 결정 목록에 있다 · **값은 여기 옮기지 않는다**). 이 논문은 PO₄³⁻ 를 동정하지 않았다 (P 2p 에 133–134 eV 성분을 전부 P₂Sₓ 로 배정) — P–O 성분이 숨어 있을 가능성은 우리 동정에서도 같은 겹침 문제다 (P₂Sₓ ≈132.6 vs 인산 ≈133–134 · 일반 문헌값).
- **LiCl 동정 불가** (Cl 2p 198.4 eV 에서 LPSCl ≈ LiCl): 우리 grand-potential 분해 반응 (예: modelc onset 반응식에 1.6 LiCl) 의 LiCl 을 XPS 로 확인하려 해도 같은 벽에 막힌다 — HAXPES `Fig. S4b` 에서 DOL:DME 의 Cl 1s 가 처녀보다 **크고 ≈1 eV 낮은 BE** 인 것은 LiCl 농화의 단서로 읽을 여지가 있으나 논문이 다루지 않았다 (§10-6).
- **우리 XPS 동정표** (`db/properties/xps_reference_sei.csv` — ⚠ 이것은 우리 DFT 값이 아니라 **문헌 · 핸드북 BE 모음**이다 · C 1s 284.8 기준 · 2p₃/₂): PS₄³⁻ P 2p 131.7 · S 2p 161.6 · LiCl Cl 2p 198.6 · Li₂SO₄ 표지 S 2p 168.0. 이 논문: 131.6 · **161.0** · 198.4 · **169.0**. S 2p 두 줄이 0.6 · 1.0 eV 어긋난다 — 이 논문 HAXPES 보정 (S 2p₃/₂ = 162.0) 과의 불일치 (§3d) 까지 합치면 **S 2p 절대 BE 를 이 논문에서 우리 표로 옮기지 않는다**. 성분 사이 **상대 간격**만 참고.
- **액체가 SE 펠릿 안으로 스며든다** (`Fig. S1` EMIMTFSI 의 F 가 단면 전체에 퍼짐 · figure-read · 우리 해석): 우리 DEM/기공 트랙의 '분리막 기공' 이 액체 촉매전해질과 만나면 계면은 평면이 아니라 **기공 벽 전체**다 — R_SLEI 를 O-ring 면적 (0.126 cm²) 으로 정규화하는 것이 과소 · 과대 어느 쪽인지 모른다는 뜻. 기공 수치 비교는 `cho2026_pore_network_homogeneity_powder_compacted_se_separator` 쪽 몫 (이 digest 는 수치 없음).
- **우리 계산 규율과의 관계**: 장벽 (Ea) · 짧은 MD · 흡착 에너지가 없으므로 홉 수 검산 (`D-2026-09-27-barrier-hop-count`) · 관측창 (`D-2026-10-05-md-observation-window`) · 배위수 (`D-2026-10-05-adsorption-site-coordination`) 는 **해당 없음**. '250 h 동안 저항 일정 = 안정' 은 실험 관측창 (250 h · 25 °C) 의 서술이다 — 그보다 느린 반응은 배제 못 한다 (저자도 '적어도 250 h' 로 적었다).

### 7c. 🔑 층위를 갈라 쓴 결론

> **"같은 LiTFSI 를 쓴 두 액체에서 Li₅.₅PS₄.₅Cl₁.₅ 표면 반응의 '진행형 대 자기 제한' 차이 (DOL:DME 는 R_SLEI 가 250 h 동안 두 자릿수 증가 · EMIMTFSI 는 ≈150–220 Ω cm² 유지) 는 이 논문의 실측이 받친다. 그 계면상의 조성 (황산염 · 유기 덮개 ≈21 nm) 은 액체 잔류와 구분되지 않아 정량 근거로 쓰지 않는다."**
>
> - 원고 · 발표: 첫 문장만 · *Faraday Discuss.*, 269, 369 (2026).
> - 내부: 우리 SE 의 '액체와의 화학 안정성' 을 DFT 로 다룰 계획은 없다 — 이 논문은 반응물 쪽 (용매 · 염) 계산이 없어 비교 기준이 되지 못한다.

## 8. DFT/계산 방법 ★ (템플릿 항목별)

- **code / functional / pseudo / k / ecut / supercell / DFT+U / AIMD / MLIP / 무질서 처리**: 전부 **해당 없음 — 계산 0**.
- 계산을 대신하는 정량 모형은 둘뿐: ① EIS 등가회로 맞춤 (ZView · 회로 `(RC)(RC)CPE`) ② HAXPES 비탄성 배경 모형 (QUASES · IMFP 13 nm TPP2M · 덮개 = C 근사).
- 후처리 도구: CasaXPS (Voigt) · QUASES-Analyze · ZView · Aztec (EDX) · 그림은 matplotlib 꼴 (축 스타일로 보아 · 미기재).

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a,b | DOL:DME 250 h 침지 단면 SEM + Cl/F EDX 겹침 — 구멍 난 표면 · F 풍부 띠 figure-read ≈2–5 µm | 황화물 SE 가 에테르 액체와 '진행형' 으로 반응하는 형태 표본 (정성 그림) |
| 1c,d | EMIMTFSI 250 h 단면 — 매끈 · 층 분해 안 됨 | 대비용 · 두께 정량 불가 |
| 2a | DOL:DME 시간분해 Nyquist (0–250 h · kΩ cm²) — 250 h 고주파 절편 ≈1.3 kΩ cm² (figure-read) | 계면 저항 시간 추적 형식 · **직렬 성분 증가가 숨어 있는 예** |
| 2b | EMIMTFSI 시간분해 Nyquist (0–0.6 kΩ cm²) — 모든 시간 거의 겹침 · 반원 없음 | '반원 없는 스펙트럼에서 뽑은 R' 의 예 (맞춤 의존) |
| 2c | R_SLEI vs 시간 두 계 — DOL:DME ≈0.02 → ≈1.9 (250 h) → ≈3.0 (≈265 h) · EMIMTFSI ≈0.15–0.22 kΩ cm² · **≈12–24 h 교차** | 핵심 그림 · 인용은 '방향 + 시간 조건' 으로 |
| 3a–d | XPS P 2p · S 2p · Cl 2p · C 1s (처녀 / DOL:DME / EMIMTFSI) — EMIMTFSI 는 P₂Sₓ 우세 · SO₄ 압도 · Cl 거의 0 · C–F 큼 | LPSCl 표면 분해 동정 예 · ⚠ TFSI⁻ 잔류 겹침 반례 |
| 4a | HAXPES Cl 1s survey (운동에너지 축) — EMIMTFSI 배경이 낮은 KE 쪽으로 올라감 | 비탄성 배경으로 매몰 깊이 재는 법 (Tougaard/QUASES) |
| 4b | 층상 SLEI 개념도 (유기층 / 무기층 / SE) · 캡션 '10s of microns' 오기 | 개념도만 |
| 5 | Li–In 대칭셀 0.1 mA cm⁻² · 100 h — ≈ +0.19 / −0.15 V 안정 · 반주기 안 톱니 | '안정' 표본 · 겉보기 ASR ≈1.9 kΩ cm² (우리 산수) |
| S1 | 원소별 EDX 맵 (C · O · S · P · Cl · N · F) 두 계 — DOL:DME 위 띠 C/N/F 풍부 · S 결핍 · EMIMTFSI F 가 단면 전체에 퍼짐 | 액체 침투 단서 (우리 해석) |
| S2a–c | 등가회로 + 처음/마지막 스펙트럼 맞춤 — 회로에 직렬 R 없음 · 그림 주파수 상한 ≈5 kHz | 우리 EIS 해석 시 반면교사 (직렬 R · CPE 표기) |
| S3 | C_bulk+gb · C_SLEI vs 시간 — 배정 띠 10⁻¹¹–10⁻⁹ / 10⁻⁹–10⁻⁷ · DOL:DME C_bulk+gb 감소 · 초기 C_SLEI 띠 밖 | 용량으로 과정 배정하는 법 · 용량 → 두께 검산 (§10-3) |
| S4a,b | HAXPES S 1s · Cl 1s 맞춤 — EMIMTFSI 는 깊이에서도 SOₓ 우세 · DOL:DME Cl 1s 가 처녀보다 큼 | 깊이별 동정 예 |
| S5 | 처녀 Li₅.₅PS₄.₅Cl₁.₅ PXRD (Co · 10–70°) — 넓은 주봉 · Li₂CO₃ · Li₂S · LiCl 표지 | 상용 분말의 불순물 수준 참고 |
| Table 1 | XPS BE · 배정 · 색 (§3d) — O=C–O < C–O 순서 오기 의심 · C–N 칸 없음 | BE 상대 간격만 참고 |

## 10. 비판 — 이 논문의 약한 곳 ★

1. **황산 · 아황산 동정이 TFSI⁻ 잔류와 겹친다 (가장 큼).** TFSI⁻ (CF₃SO₂)₂N⁻ 의 S 는 S 2p ≈169 eV 근처 · S 1s 고 BE 에 나온다 (일반 문헌값) — 이 논문이 SO₄²⁻ 로 배정한 자리와 같다. 두 침지 시료 모두 C–F (293 eV) 가 뚜렷해 TFSI⁻ (또는 그 분해물) 가 표면에 있음이 확실한데, **세척 여부 · 세척 용매가 미기재**이고 N 1s · F 1s · O 1s 스펙트럼이 없다. EMIMTFSI 시료에서 SO₄ 가 더 큰 것은 '더 많이 산화됐다' 가 아니라 '안 날아가는 액체가 더 많이 남았다' 로도 같은 크기로 설명된다. 처녀 SE 를 같은 액체에 **잠깐 (수 초)** 담갔다 꺼낸 대조가 있었으면 갈렸다.
2. **'≈21 nm 유기 분해 덮개' 는 잔류 이온성 액체 막과 구분되지 않는다.** EMIMTFSI 는 증기압이 사실상 0 이라 UHV 에서도 막으로 남는다 · DOL:DME 는 휘발한다 — 두 시료의 '덮개 두께 차 (21 vs 3 nm)' 가 **분해층 차가 아니라 휘발성 차**일 수 있다. 덧붙여 C 1s 의 'C–O' (≈287 eV) 성분이 EMIMTFSI 시료에서 크게 나오는데, **EMIM⁺ 에는 산소가 없다** — 그 자리는 이미다졸륨 C–N 과 겹치고 `Table 1` 에 C–N 칸이 없다. 이것은 오히려 **미분해 EMIM⁺ 의 존재**를 가리킨다. 덮개 물질을 C 로 근사한 절대 두께는 저자도 '어렵다' 고 인정했다 — 21 nm 는 상대 비교값이다.
3. **EIS 회로에 직렬 저항이 없고, 커진 것이 R_SLEI 만이 아니다.** 차단전극 / LE / SE / LE / 차단전극 셀에서 두 액체층의 이온 저항은 순수 직렬 R 인데 회로에 그 항이 없어 R_bulk+gb 에 흡수된다. `Fig. S2b` 의 250 h 고주파 절편이 ≈1.3 kΩ cm² 만큼 오른쪽으로 옮겨 갔다 (figure-read) — 액체 쪽 변화 (DOL 의 루이스산 개환 중합 · 휘발 · 폴리설파이드 용해에 따른 점도 변화) 일 수 있고 SE 쪽 변화일 수도 있다. 본문은 이 성분을 말하지 않는다. 또 그림 주파수 상한이 ≈5 kHz 라 (원자료는 1 MHz 까지 있다 · §3f) 벌크 반원은 보이지 않고 'bulk + GB' 용량 ≈10⁻¹⁰ F cm⁻¹ 의 맞춤은 범위 밖 외삽에 기댄다. **용량 → 두께 검산 (우리 산수 · εr 는 가정)**: C_SLEI ≈2.6×10⁻⁸ (DOL:DME) · ≈3.5×10⁻⁸ F cm⁻² (EMIMTFSI) 를 평판 축전기 d = ε₀εr/C 로 풀면 εr 5–10 에서 각각 ≈0.17–0.34 µm · ≈0.13–0.25 µm — **둘이 거의 같고**, SEM 의 '수 µm vs 분해 불가' 와도 HAXPES 의 '21 nm' 와도 안 맞는다. 즉 R_SLEI 호가 실제로 SEM 에 보이는 그 층의 응답인지 회로만으로는 확인되지 않는다.
4. **R_SLEI 의 정의가 반쪽이다.** 셀에 SE/LE 계면이 **둘** 있는데 R_SLEI 가 둘의 합인지 하나인지 · 면적 정규화가 O-ring 면적인지 기재 없음. 반복 셀 수 (n) · 오차막대도 없다. 두 계 EIS 는 원자료 파일 이름상 **7 주 간격의 다른 날** 측정이다 (2025-10-17 vs 2025-12-04).
5. **'저저항' 결론과 대칭셀 전압이 안 맞는다.** 0.1 mA cm⁻² 에서 ≈0.19 V ⇒ 겉보기 ≈1.9 kΩ cm² (우리 산수) — DOL:DME 의 250 h R_SLEI 와 같은 크기다. 실용 준고체 Li–S (≈1 mA cm⁻² 급) 로 옮기면 ≈1.9 V 분극이 된다 (단순 선형 외삽 · 우리 산수). 대칭셀이 SLEI 를 따로 재지 않으므로 '안정' 은 말할 수 있지만 '낮은 저항' 의 증거는 아니다. 같은 셀을 DOL:DME 로 돌린 대조도 없다 (EMIMTFSI 만 돌렸다).
6. **보정 · 표기 오기 여럿**: ① HAXPES 를 S 2p₃/₂ = 162.0 eV 로 보정했다면서 'XPS 와 일관' 이라 했는데 `Table 1` · `Fig. 3b` 의 PS₄³⁻ 는 161.0 (figure-read ≈160.8) — 1 eV 어긋남 · 그 결과 HAXPES Cl 1s 위치가 시료마다 ≈2820.1–2821.2 로 흩어진다 (`Fig. S4b` · 대전 · 보정 차를 구분 못 함) ② `Fig. 4` 캡션 '10s of microns' (본문 · 실험 절은 nm) ③ EIS 주파수 '5 kHz–50 Hz' ↔ 그림의 10 Hz 표지 · 원자료 1 MHz–0.1 Hz ④ PXRD '10–90°' ↔ 그림 10–70° ⑤ `Table 1` O=C–O 286.0 < C–O 286.3 ⑥ 결론 '∼20 nm' ↔ 본문 '∼21 nm' (반올림이지만 같은 양에 두 숫자).
7. **대칭셀 '2 mL'** — 5 mm 유리섬유 원판이 담을 수 있는 부피 (수 µL) 의 수백 배다. µL 의 오기로 보이며, 만약 실제로 mL 급이었다면 '준고체' (소량 촉매전해질) 조건이 아니다.
8. **교락 변수**: 염 농도 (1 M vs 0.5 M) · 점도 · 용매 순도 · 미량 수분 (EMIMTFSI 전자급 ≥ 99.9 % · ELYTE 상용 DOL:DME 는 수분 사양 미기재) 이 용매와 함께 바뀌었다. 황산/아황산 생성의 산소원이 '용매의 O' 인지 '용존 H₂O/O₂' 인지 가르는 실험이 없다 — 처녀 시료에도 아황산이 이미 있다 (`Fig. 3b` · 저자도 불순물로 인정).
9. **폴리설파이드 용해 가설을 액체 쪽에서 확인하지 않았다.** 침지 후 액체의 UV-vis · Raman · ICP (S/P 농도) 한 번이면 '녹아 나갔다' 를 직접 볼 수 있었다 — 현재는 'XPS 에 안 보인다' 는 부재 증거뿐이다.
10. **Li–S 전지가 없다.** 제목이 'quasi-solid-state Li–S batteries' 이지만 황 양극 · 폴리설파이드가 실제로 존재하는 촉매전해질 · 전위 창 (≈1.7–2.8 V vs Li) 은 실험에 없다. 실제 셀에서는 양극에서 온 폴리설파이드가 SLEI 에 닿는다 — 그 조건의 SLEI 는 이 논문의 '무 폴리설파이드 액체' 결과와 다를 수 있다.
11. 토론회 (Faraday Discussions) 논문이라 짧은 형식 — 정량 (원자 % · 맞춤 잔차 · 반복 셀) 이 대부분 빠져 있다. 원자료가 공개된 것 (UBIRA eData) 은 장점이다 — 위 3 · 4 의 의문은 원자료로 재맞춤해 확인할 수 있다.

## 11. 적용 인사이트 ★ (우리 연구에 어떻게)

1. **SE 표면 분석을 읽을 때 '액체 잔류' 를 먼저 묻는다.** LiTFSI 계 액체와 닿은 황화물 SE 의 S 2p 169 eV · C 1s 'C–O' 는 분해 산물이 아니라 잔류 염 · 양이온일 수 있다. 우리 SEI/CEI XPS 동정 (`db/properties/xps_reference_sei.csv`) 을 쓸 때도 액체 접촉 시료면 같은 의심을 단다.
2. **EIS 계면 분리의 체크리스트** (이 논문의 빈칸에서 거꾸로): 직렬 R 항 · 계면 개수 · 면적 정규화 · 맞춤 주파수 범위 · 용량 → 두께 검산 · 반복 n. 우리 쪽 공동연구 EIS 해석 요청이 오면 이 다섯을 먼저 본다.
3. **'자기 제한 vs 진행형' 은 산물의 용해도로 갈린다** — 우리 계산 축으로 옮기면 '분해 산물이 계면에 남는가' 는 열역학 (grand-potential) 만으로는 못 정하고 **용매화 · 용해** 가 필요하다. 우리 ESW · CEI 계산 결과를 액체 공존 셀 (준고체) 에 적용할 때 '분해 산물이 부동태층으로 남는다' 는 가정을 그대로 가져가지 않는다.

## 12. 인용 가능 문장 (영문 초안 · 랩 표기 *Faraday Discuss.*, 269, 369 (2026))

- "When Li₅.₅PS₄.₅Cl₁.₅ was held in contact with 1 M LiTFSI in DOL–DME for 250 h, the interphase resistance increased continuously from ∼25 to ∼2000 Ω cm², whereas with 0.5 M LiTFSI in EMIMTFSI it remained at 150–220 Ω cm²." (*Faraday Discuss.*, 269, 369 (2026))
- "The ether electrolyte produced a several-micron-thick, pitted interphase, consistent with dissolution of polysulfide-type decomposition products, while the ionic-liquid interphase could not be resolved by FIB-SEM." (같은 출처)
- ⛔ 쓰지 않는 문장: "LPSCl forms sulfate in contact with ionic liquids" (TFSI⁻ 잔류와 구분 안 됨) · "a 21 nm organic decomposition layer" (잔류 IL 막 대안 · 탄소 근사 절대값) · "low-resistance interphase under cycling" (대칭셀 겉보기 ASR ≈1.9 kΩ cm²).

## 13. 주의 / 한계 (인용 규율)

- 문헌 소환값이다 — 우리 db 절대값과 섞지 않는다. 이 논문에는 우리와 맞댈 SE 벌크 물성값이 없다.
- R_SLEI 수치는 **시간 조건** (≥ ≈24 h 에서만 EMIMTFSI < DOL:DME) 과 **회로 조건** (직렬 R 없는 (RC)(RC)CPE · ≤ 5 kHz 맞춤) 을 같이 적어야 한다.
- `figure-read ≈` 값 (특히 ≈265 h 의 3.0 kΩ cm² · 고주파 절편 1.3 kΩ cm² · 용량들) 은 그림 판독이다 — 원자료 재맞춤 전에는 정량 인용하지 않는다.
- S 2p 절대 BE (161.0 · 169.0) 를 우리 동정표로 옮기지 않는다 (보정 불일치 §10-6).
- 이 논문의 '안정 · 저저항' 은 무전류 · 무 폴리설파이드 · 25 °C · 250 h (EIS) / 100 h (대칭셀) 관측창 안의 서술이다.

## 14. 이어 읽기 — litdb 의 관련 digest

| slug | 연결 이유 |
|---|---|
| `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` | 같은 '준고체 Li–S' 이름이지만 **뜻이 다르다** — Shen 은 약용매화 에테르 액체 안의 '준고체 황 반응' (SE 없음) · 이 논문은 SE 분리막 + 액체 촉매전해질 구조. LiTFSI 에테르 액체 쪽 용매화 · 폴리설파이드 용해도 감각을 거기서 얻는다 (Li₂S₆ 용해도 ≈50–80 mM[S] 수준의 약용매화 에테르라면 이 논문의 '녹아 나감' 가설이 약해진다) |
| `cronk2026_lis_cathode_interphase_chemistry` | LPSCl 이 Li–S 양극 안에서 'LPS-like' 로 분해 · 'catholyte' 라는 말을 **양극 복합체 속 SE** 로 쓴다 — 이 논문의 'catholyte = 액체' 와 용어가 충돌하니 주의. 실제 S 양극 조건의 SE 분해 화학 (이 논문에 없는 것) |
| `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` | 전고체 Li–S 의 반응 · 계면 공학 종합 — 이 논문이 동기로 든 '황 양극 ≈80 % 팽창' 과 전고체 대안의 위치 |
| `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` | 전고체 Li–S 의 삼상 계면 문제 — 준고체가 액체로 메우려는 그 접촉 문제의 전고체 쪽 해법 |
| `kim2026_moisture_surface_degradation_lpscl_dryroom` | LPSCl 표면이 SO₄/SO₃ · LiOH · Li₂CO₃ 로 무너지는 XPS 동정 — 이 논문 처녀 시료의 아황산 · PXRD Li₂CO₃ 불순물과 같은 출처 (수분) 를 의심할 근거 · 동정 BE 대조 |
| `deng2026_polysulfate_layer_moisture_oxidation_lpsc` | LPSC 표면 sulfite/sulfate 를 XPS 로 정량 (에칭 전후 %) — 이 논문에 없는 '깊이별 정량 + 에칭' 의 본보기 · SO₄²⁻ 동정의 기준선 |
| `hyun_han_argyrodite_moisture_degradation_design_principles` | argyrodite 수분 열화 설계 원리 — 액체 속 미량 수분이 산소원일 가능성 (§10-8) 의 배경 |
| `he2026_cryo4dstem_chloride_migration_moisture_argyrodite` | 수분 노출 시 Cl 이 이동 · 농화 — HAXPES 에서 DOL:DME 시료의 Cl 1s 가 처녀보다 큰 것 (`Fig. S4b`) 을 읽을 때의 참고 |
| `banerjee2020_interfaces_interphases_assb_review` | 계면 · 계면상 리뷰 — ref 208 (Oh 2015 · 용매화 이온성 액체와 황화물 SE 의 호환성) 을 다룬다 · 이 논문의 '이온성 액체가 낫다' 의 선행 맥락 |
| `kim2026_iccf_molten_salt_sei_lpscl_sheet` | 황화물 SE 시트의 공동을 이온전도성 충전재로 메워 계면을 만든다 — 'SE + 액체/연질 상' 혼성 계면의 다른 설계 |
| `luo2026_lis_separator_crystal_engineering_review` | Li–S 분리막 설계 리뷰 — SE 분리막을 쓰는 준고체 구조의 위치 |
| `shang2026_uio66_anion_competition_peo_lis` | 고체 Li–S 에 LiTFSI · DOL/DME 를 적셔 조립한 셀 — '소량 액체 적심' 의 다른 예 |
| `sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance` | 산화물 SE (LLZO) 표면 화학 (Li₂CO₃) 이 계면 저항을 정한다 — 이 논문이 '대부분 산화물만 연구됐다' 고 한 선행 축의 대표 |
| `fan2026_sulfide_assb_stability_review_ECERD2600097` | 황화물 SE 안정성 리뷰 (catholyte 절 포함) — 화학 · 전기화학 안정성 틀 |

## 15. 기법 용어 미니사전

- **SLEI (solid–liquid electrolyte interphase)**: SE 와 액체 전해질이 닿는 자리에 화학 반응으로 생기는 얇은 상. 전극의 SEI 와 달리 전위 없이도 생긴다.
- **준고체 (quasi-solid-state) Li–S (이 논문의 뜻)**: SE 분리막 + 양극 쪽 소량 액체 촉매전해질. 분리막이 셔틀 · 덴드라이트를 막고 액체가 양극 접촉을 돕는다.
- **차단전극 셀 (blocking electrode)**: Li⁺ 를 주고받지 못하는 금속 (SUS) 전극 — 저주파에서 축전기처럼 보여 (CPE) 이온 과정만 분리해 볼 수 있다.
- **시간분해 EIS**: 같은 셀의 임피던스를 일정 간격으로 반복 측정해 저항 성분의 시간 변화를 본다.
- **특성 용량 배정 (Irvine–Sinclair–West)**: 맞춤된 각 RC 의 용량 크기 (벌크 ≈10⁻¹² · 입계 ≈10⁻¹¹–10⁻⁸ · 표면층 ≈10⁻⁹–10⁻⁷ · 전극 계면 ≈10⁻⁷–10⁻⁵ F) 로 그것이 어느 물리 과정인지 정한다.
- **CPE (constant phase element)**: 이상적이지 않은 축전기 — 표면 거칠기 · 분포 때문에 반원이 눌리는 것을 표현.
- **HAXPES (hard X-ray photoelectron spectroscopy)**: 수 keV X 선 (여기선 9.25 keV) 으로 광전자의 운동에너지를 키워 탈출 깊이를 수십 nm 로 늘린 XPS.
- **IMFP (inelastic mean free path)**: 광전자가 에너지를 잃지 않고 가는 평균 거리 — 여기선 ≈13 nm (TPP2M 공식). 정보 깊이는 대략 그 3 배 (일반 문헌값).
- **비탄성 배경 분석 (Tougaard · QUASES)**: 봉우리 아래쪽 (낮은 KE) 배경의 모양이 방출원의 깊이를 담는다 — 깊이 묻힐수록 봉우리는 작고 배경은 크다.
- **FIB-SEM**: 집속 이온빔으로 단면을 깎아 SEM 으로 보는 것 (여기선 Xe 플라스마 FIB · 30 kV · 15 nA).
- **Li–In 합금 전극**: Li 금속보다 전위가 높고 (≈0.6 V vs Li · 일반 문헌값) 반응성이 낮아 대칭셀의 모델 전극으로 쓴다.
- **P₂Sₓ / Li₂Sₓ**: 브리지 S 를 가진 인 황화물 · 리튬 폴리설파이드 — PS₄³⁻ 가 산화 · 분해될 때의 중간 산물. 에테르에는 녹고 이온성 액체에는 덜 녹는다.
