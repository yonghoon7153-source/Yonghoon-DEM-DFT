---
title: "Oh, Kim, Kim, An, Kwon, Choi 2025 — Maxwell Protocol for Non-Destructive Health Diagnosis of All-Solid-State Batteries (Angew. Chem. Int. Ed. 64, e202514910)"
source_url: local-upload/13._Maxwell_Protocol_for_Non-Destructive_Health_Diagnosis_of_All-Solid-State_Batteries.pdf + 13._Maxwell_Protocol_for_Non-Destructive_Health_Diagnosis_of_All-Solid-State_Batteries.docx (SI)
source_url_note: "본문 9쪽 (텍스트 pp. 1-8 + 참고문헌 74편 pp. 8-9) + **SI .docx (진짜 Supporting Information, Wiley-VCH 템플릿)** — Experimental Procedures + Note S1 + Figure S1-S16, 표 0장. 지면은 Angewandte Chemie 독일어판 조판(Forschungsartikel / Zitierweise)이지만 **본문은 영어**. 크로핑 본문 6장 전부 봄, SI 16장 중 11장 봄(S5·S6·S10·S11·S15 형태학 패널은 안 봄). 실험 논문 — 1차 측정 있음(엔트로피메트리 3셀·volumetry 3+1셀·XRM 4개·SEM). `[인쇄]`/`[도표]`/`[재현]`/`[해석]` 4구분."
source_doi: 10.1002/anie.202514910
source_license: "CC BY-NC-ND 4.0 (Wiley-VCH, open access) — 인용 가능, 비상업·무변경"
pdf_sha256: fa35a5cdd5d3fcecff6b488cd823113fc79f90120eaf81e4900d290a96f88dd4
si_sha256: ce0b9a35c96ef99c0fcfab136e8c0ea0e20129016db51e7f54056c2f8a1624b8
ingested: 2026-09-22
sha256: 7ccce63d3eae3a9395b37564681d8b1aec24b89e52ac70a5c9d04fe164fa1487
---

# 수집 목적

`assb` 섹션 **14호**. 큐 **13번** (13호 = 큐 12 Zheng 2026 그리드 appraisal, 12호 = 큐 11
Kouhestani 2022). 닻은 `questions/assb-contact-loss-vs-lampe.md`. 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-1)의 등록 축은 **Q3·Q4 + "OCV 경쟁 접근"** —
즉 우리 닻 물음(half-cell OCP fitting 으로 접촉 손실 ↔ `LAM_PE` 를 가를 수 있는가)과 **같은
대상을 다른 관측으로** 진단한다고 주장하는 편인지 읽는 것이 과제였다.

> **판정 한 줄 (먼저)**: 이 편은 **OCV 곡선 `E(x)` 를 적합하지 않는다.** 같은 상태함수의
> **두 편미분** `(∂E/∂T)_P` 와 `(∂E/∂P)_T` 를 정지 상태(OCV)에서 재고, Maxwell 관계로 각각
> `ΔS(x)`(양극 구조·비균질) 와 `ΔV`(복합전극 void) 로 읽는다. **경쟁이 아니라 관측 추가**다
> ([[constrained-crb-identifiability]] 의 "관측 추가" 칸에 정확히 들어간다). 분리 주장은
> **"mechanical(void) ↔ chemical(계면 저항)"** 이지 **`LAM_PE` ↔ 접촉 손실이 아니며**, 그 분리를
> 교차 실험으로 시험하지 않았다. **Q4(유일성)는 역문제 자체가 없어 0/14.** 자세한 판정표는 끝에.

> 표기: `[인쇄]` 본문·SI 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`) · `[재현]` 우리가
> 지면의 숫자로 계산한 값 · `[해석]` 우리 해석. `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.
> ⚠ 지면이 *Angewandte Chemie* 독일어판 조판("Forschungsartikel", "Zitierweise", 하단
> `Angew. Chem. 2025, 137, e202514910`)이지만 **본문은 전부 영어**다 (독일어는 머리말 두 단어뿐).
> 인용 서지는 큐 문서대로 *Angew. Chem. Int. Ed.* 2025, 64, e202514910 을 쓴다.

# 서지

**Jihoon Oh**⁺, **Inwoo Kim**⁺, Hyunjae Kim, Seongha An, Dohun Kwon, **Jang Wook Choi**\* —
"Maxwell Protocol for Non-Destructive Health Diagnosis of All-Solid-State Batteries",
***Angew. Chem. Int. Ed.* 2025, 64, e202514910**, doi `10.1002/anie.202514910`,
**Batteries Hot Paper**. ⁺ 공동 제1저자. 교신 Choi (jangwookchoi@snu.ac.kr).
- 소속: 서울대 화학생물공학부 + **HMG-SNU 공동배터리연구센터(JBRC, 현대차)** + SNUEI.
- 접수 2025-07-08 → 개정 08-10 → 승인 **08-12** → 온라인 08-23 (접수→승인 **35 일**).
- 라이선스 `[인쇄]` **CC BY-NC-ND** (Wiley-VCH, open access).
- 분량: **9 쪽** = 본문 pp. 1–8 (절 5 개 + 그림 6) + 참고문헌 **74 편** pp. 8–9.
  **SI 있음** (.docx, Wiley 템플릿 — `[인쇄]` 머리 "©Wiley-VCH 2021 … DOI: 10.1002/anie.2021XXXXX"
  placeholder 그대로): Experimental Procedures(3 절) + Note S1 + **Figure S1–S16** + Author
  Contributions. **표는 0 장** (본문·SI 모두). 파라미터 표·셀 사양 표 없음 — 사양은 SI 산문에만.
- 자기 인용: `[재현]` 74 편 중 **J. W. Choi 공저 21 편**(refs 2·9·10·13·18·21·24·25·28·29·30·
  32·33·38·47·48·49·56·57·71·72). 엔트로피메트리 원전 [56]·[57] (Kim … Choi *PNAS* 2022 ·
  Kim … **Yazami**, Choi *EES* 2020)도 자기 논문.
- ★ **큐 13호 후속 후보 4 순위 "Oh Jihoon, *AEM* 2025, 15, 2404817"** 이 이 논문의 **ref [10]**
  (J. Oh, D. Kwon, S. H. Choi, …, J. W. Choi) — **같은 저자·같은 연구실**이다. 13호(Zheng)의
  [34] 와 동일 서지.
- 우리 계보와의 인용 관계: **5호 Doux 2020 = ref [35]** ("higher stack pressures … decrease
  the formation of voids" 근거) · 1호 Bielefeld **2019 는 없고 Bielefeld 2022 *JES* 169,
  020539 = ref [69]** ("abrupt resistance increase when the pore volume … surpasses a
  threshold" — 퍼콜레이션 문턱 진술의 출처) · **4호 Shi 2020 은 인용되지 않는다** (`Shi` 0 회;
  ">300 MPa 재가압" 처방에 인용 없음) · 9호 Huo · 10호 Vadhva · 11호 Yu 전부 없음.
- 키워드 `[인쇄]`: All-solid-state batteries · **Entropymetry** · **Maxwell relations** ·
  Nondestructive health diagnosis · **Volumetry**.

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 걸리는 축 |
|---|---|---|
| G1 | **"health" 의 정량 정의가 없다.** reuse / recondition / recycle 세 등급의 **문턱값이 0** — ΔS drop 몇 J mol⁻¹ K⁻¹ 이하, volumetry drop 몇 % 이상이 어느 등급인지 적히지 않았다. 논문 스스로 `[인쇄]` "quantitative metrics for each degradation mode … requires analyzing many cells … securing adequate sample sizes is currently difficult" | **Q3** |
| G2 | **오차 막대 0 · 통계 0.** `error bar`·`standard deviation`·`uncertaint*`·`n =` 전수 0 회(본문 + SI). "Three individual cells" 는 있으나 Fig. S3 는 **점 2 개만 보이고**(3 개가 겹친 것인지 불명), Fig. S9 는 막대 3 개에 오차 없음 | Q3 |
| G3 | **volumetry 의 `dE` 판독 규칙이 없다** — 감압 전 평균 ↔ 감압 중 평균? 피크-투-피크? `[도표]` Fig. S16 위 패널은 **재가압 뒤 OCV 가 초기보다 +0.4 mV 높게 안착**하고, 감압 유지 300 s 동안 OCV 가 **+0.5 mV 표류**한다 — 노화 신호(2.3 → 2.2 mV = 0.1 mV; 2.2 → 1.8 = 0.4 mV)와 같은 크기 | **Q2·Q3** |
| G4 | **volumetry 전·후 측정의 SOC 가 다르다** — Fig. 4 캡션은 둘 다 "after discharge at 2.5 V and a rest period" 인데 `[도표]` OCV 가 **3.532 V(전) ↔ 3.703 V(후)**, S16 도 **3.476 ↔ 3.648 V**. `dV/dx` 는 `x` 의 함수라 두 값은 같은 좌표가 아니다. 논문 언급 0 | Q2 |
| G5 | **`ΔV = F(dE/dP)` 의 단위·크기 검토가 없다.** `[재현]` 42.7 µJ mol⁻¹ Pa⁻¹ = **42.7 cm³ mol⁻¹** (몰부피 차원)인데 논문은 "volumetric energy" 라 부르고 **어떤 기준 부피와도 비교하지 않는다**. Li 금속 몰부피 13.0 cm³ mol⁻¹ (식 (10)의 `dV_anode/dx` 상수항)이 **가장 큰 이론항**인데 본문은 음극을 "creep → pore 무시" 로만 처리한다 | Q1·Q5 |
| G6 | **`E(P)` 가 비선형이라는 것을 안 적는다** — 같은 신품 셀 종류에서 `[인쇄]` 10→5 MPa 에 2.2 mV(**0.44 mV/MPa**) ↔ 20→10 MPa 에 2.3 mV(**0.23 mV/MPa**): **2 배**. Fig. 5e/f 는 y 축 눈금을 달리해(34–44 ↔ 14–30) 나란히 놓지 않는다 | **Q6** |
| G7 | **엔트로피메트리 SOC 축이 없다.** 모든 ΔS 곡선이 **OCV 축**이고 `x`(SOC) 축은 어디에도 없다. "every 5 % of SOC" 의 기준 용량(공칭? 실측?)도 없다 — 100 사이클 후 용량 `[도표]` ≈68 % 인 셀에서 "0.1C × 30 min" 이 무엇의 5 % 인지 불명 | Q8 |
| G8 | **ΔS 총합(sum rule) 검사가 없다.** `∫(dS/dx)dx` 는 상태함수 차이라 **비균질만으로는 변하지 않는다**. `[도표]` 전 곡선 평균 ≈ −3.5 ↔ 후 ≈ +1.5 J mol⁻¹ K⁻¹ — 부호까지 바뀐다. 논문은 이것을 "smoother"(비균질)로만 읽는다 | **Q2** |
| G9 | **활물질 로딩(mg cm⁻² · mAh cm⁻²) 0.** 조성 76:20:1.5:2.5 wt 만 있다. 용량 mAh g⁻¹ 가 무엇 기준인지(NCM 질량?) 명시 없음 | 서술 |
| G10 | **XRM 복셀 크기 없음** — SI `[인쇄]` "image resolution was set to 0.7 pixels per unit"(단위 미정, 오기로 보임). 기공 분할은 `[인쇄]` "window leveling" 문턱 — 문턱값·민감도 0. 그리고 **10 MPa 신품 4.5 % ↔ 20 MPa 신품 4.4 %** 는 **다른 셀**이다 | Q1·Q3 |
| G11 | **Recondition(>300 MPa) 을 실제로 수행한 데이터가 없다.** Fig. 6 의 세 등급 중 실험으로 뒷받침된 것은 "signal 있음/없음" 뿐이고 **재가압 후 회복 실측 0** — 그리고 300 MPa 는 이 셀의 **Li 금속 음극** 상한(5호 75 MPa)의 4 배 | **Q6** |
| G12 | **"chemical degradation" 단독 대조군이 없다.** 분리 주장(`[인쇄]` "distinguish between mechanical and chemical degradation")을 시험하려면 void 없이 계면 저항만 오르는 셀(예: 20 MPa 셀의 엔트로피메트리, 또는 비코팅 NCM)이 필요한데 **20 MPa 셀은 volumetry 만** 쟀다 | **Q2·Q4** |
| G13 | **Li 금속 음극의 열역학 항을 "constant" 로 둔 근거 0** — `[인쇄]` "whose potential can reasonably be assumed to remain constant". 100 사이클 뒤 음극 계면(SEI·다공 Li)의 `dE/dT`·`dE/dP` 기여 변화를 검토하지 않는다 | Q5 |
| G14 | 엔트로피메트리 1 프로파일의 소요 시간이 안 적혀 있다 — `[재현]` 점당 300 min × ≈28 점 ≈ **140 h**. `[인쇄]` "in real time" 과의 거리 | 서술 |

# 그림 — 본문 크로핑 6 장, **전부 봄**; SI 16 장 중 **11 장 봄** (S1·S2·S3·S4·S7·S8·S9·S12·S13·S14·S16), 안 본 것 **S5·S6·S10·S11·S15** (SEM-EDS·XRM 원영상 — 형태학 패널)

`wiki/raw/figures/oh2025_maxwell-protocol-nondestructive-assb-health/` (fig_1–fig_6, 누락 0).
SI 그림은 `.docx` 의 `word/media/image3–18`(문서 순서 = S1–S16; image1 = 로고 24×21 px,
image2 = 수식 EMF)을 꺼내 봤다 — 위키에는 저장하지 않았다(SI 원본은 업로드 경로).

| 그림 | 무엇 | 실제로 본 것 `[도표]` | 본문과의 관계 |
|---|---|---|---|
| **Fig. 1** | 모식도 | `dG = VdP − SdT`; 왼쪽 "Isobaric (dP = 0)" 층상 격자 + 온도계 → "Detection of delithiation heterogeneity in cathode"; 오른쪽 "Isothermal (dT = 0)" 균열 조직 + 압력계 → "Detection of internal voids" | 정보량 0 (본문 재서술) |
| **Fig. 2** | 모식도 — 균질 vs 비균질 탈리튬화의 `S`·`ΔS` 프로파일 | 위: `S` vs OCV, 두 볼록 봉우리(V₁·V₂), 비균질에서 V₂ 봉우리가 낮고 겹침. 아래: `ΔS` vs OCV, 단조 감소 두 구간 "Strong separation" ↔ "Weak separation" + **빨간 화살표 ↑**(고전압 끝의 ΔS 가 덜 내려간다) | ⚠ **x 축이 OCV 이지 SOC 가 아니다** — 비균질(입자별 SOC 분산)이 OCV 축에서 봉우리를 뭉개는 것은 맞지만, 같은 그림을 **SOC 축**으로 그리면 총합이 보존돼야 한다 (G8). 논문은 SOC 축 판을 그리지 않는다 |
| **Fig. 3** | 엔트로피메트리 방법·결과 (a–e) | **(a)** 시간 0–300 min: 충전 3.71→3.744 V(0–30 min) → 휴지; 온도 35 °C(0–150) → 20 °C(≈165–240) → 35 °C. OCV 는 휴지 내내 **계속 이완**(150 min 에 ≈3.7235 V, 기울기 figure-read ≈ −0.02~−0.03 mV/min); 파란 점선 = 두 35 °C 구간을 잇는 기준선; 20 °C 에서 전압이 기준선 **위**로 벌어짐(figure-read 240 min 에 ≈+2~4 mV). **(b)** 신품 ΔS vs OCV(3.53–4.25 V, ≈28 점): **+1~+3.5**(3.53–3.73 V) → 3.73–3.78 V 에서 **급락 −3** → −3~−5 평탄(3.8–3.95) → 봉우리(−3.5 @3.97) → −5~−7(4.0–4.12) → 봉우리(−4 @4.17) → **−11 @4.25 V**. 음영 4 구간(3.55–3.60 · 3.72–3.77 · 3.97–4.03 · 4.15–4.25). dQ/dV(mAh V⁻¹, 0–10) 봉우리 **3.60(≈3.8) · 3.73(≈3.5, "H1→M") · 4.00(≈2) · 4.18(≈2.3)**. **(c)** 신품(검정) = (b); **100 사이클 후(빨강): +2(3.55) → +3.5(3.65) → +3(3.72) → 완만 하강 → ≈0(3.85–4.12) → +2.5(4.19) → +1(4.25)** — **한 번도 음수로 안 내려간다**. **(d)** 신품 단면 SEM: 이차입자(≈4 µm) 온전, SE 가 감싸고 계면 밀착. **(e)** 100 사이클 후: 이차입자 내부 **격자 모양 미세균열**, 입자–SE 계면 **검은 틈**; 라벨 "Interparticle contact loss + Intraparticle micro-cracks = Heterogeneous delithiation" | ★ **(a) 의 크기가 (b) 와 안 맞는다**: 3.72 V 에서 ΔS ≈ +3 J mol⁻¹ K⁻¹ 이면 `[재현]` `dE = −ΔS·dT/F = 3×15/96485 = 0.47 mV` 인데 (a) 에 보이는 기준선 이탈은 **≈2–4 mV**(≈4–8 배, 판독 ±0.5 mV 감안해도 3 배 이상) — (a) 가 (b) 의 같은 점이 아니거나 예시 그림이다 (D1). ★ **(c) 의 "after" 곡선은 S2 의 세 셀 어느 것과도 끝점이 다르다** (D2). (e) 는 균열과 접촉 손실을 **한 화살표 등식**으로 묶는다 — 라벨이 결론이다 |
| **Fig. 4** | volumetry 방법·결과 (a–c) | **(a)** 모식도 — "Before cycle (good contact): Direct effect on CAM" ↔ "After cycle (void formation): ΔP relieved by voids". **(b)** 신품: OCV **3.5318 V**(0–90 s, 10 MPa) → 압력 10→5 MPa(≈90–170 s) 로 **3.5303 V** → 재가압(430–500 s) → 3.5318–3.5320 V. 전압 계단 ≈0.2 mV(계측 분해능), 잡음 ±0.2 mV. "OCV drop = 2.2 mV". **(c)** 50 사이클 후: OCV **3.7033 V** → 5 MPa 에서 3.7021 V → 복귀 3.7034 V. "OCV drop = 1.8 mV" | ⚠ **(b)(c) 의 OCV 가 171 mV 다르다**(G4) — 캡션은 둘 다 "after discharge at 2.5 V". 감압→OCV 하강이므로 **`dE/dP > 0`** (가압하면 OCV ↑). 노화 차 0.4 mV 는 **계단 2 개** 크기 |
| **Fig. 5** | XRM 공극 + volumetry 상관 (a–f) | **(a)(b)** 3D 렌더 "Void intensity" 컬러(100 µm 바), 후가 붉은 점 많음. **(c)** 10 MPa 후 기공 맵(청록) "**Porosity: 9.8 %**". **(d)** 20 MPa 후(주황) "**Porosity: 5.3 %**". **(e)** 10 MPa: volumetry **≈42.5 → 34.7** µJ mol⁻¹ Pa⁻¹, porosity **4.5 → 9.8 %** (y 축 34–44 / 4–10). **(f)** 20 MPa: **≈22.2 → 21.2**, porosity **4.4 → 5.3 %** (y 축 14–30 / 0–10) | ★ **(e)(f) 의 신품 volumetry 가 2 배 다르다**(42.5 ↔ 22.2) — 같은 신품 셀 종류, 다른 `ΔP` 구간(5 ↔ 10 MPa). **`dE/dP` 가 압력 구간의 함수**라는 뜻인데 축 눈금을 달리해 가려진다 (G6·D4). 본문 42.7 ↔ 그림 ≈42.5 ↔ `[재현]` 42.45 (D5) |
| **Fig. 6** | 프로토콜 모식도 | Solid-state batteries → "Under stack pressure (> MPa scale)" 프레스 → (위) Cycling → "Impact of internal degradation **not apparent in cycle performances** — Similar data / Cannot distinguish health status"; (아래) "Maxwell protocol ① Entropymetry ② Volumetry" → Internal health diagnosis → Classification: **Reuse (no signal) / Recondition (ΔV signal) / Recycle (ΔS signal)** | ★ 분류 규칙이 여기서만 드러난다: **ΔV 신호만 → recondition, ΔS 신호 → recycle**. 본문 텍스트의 recycle 정의는 "heterogeneous **along with** significant void" (ΔS ∧ ΔV) — 그림은 ΔS 만으로 recycle (D6). **ΔS 있고 ΔV 없는 셀**(void 없이 비균질 = 순수 화학 열화)의 칸이 없다 |
| **S1** | 엔트로피메트리 셀 100 사이클 | 0.5C, 25 °C, 10 MPa: 방전 **≈143 → ≈97 mAh g⁻¹**(figure-read, 유지율 ≈68 %), CE 첫 사이클 ≈85 % → ≈98–99 %. 1st 충전 ≈163(CV 꼬리 포함)/방전 143; 100th 충전 ≈100/방전 ≈98. 100th 방전 곡선 시작 ≈3.62 V(1st ≈4.15 V) | 본문은 유지율을 안 적는다. `[해석]` 100 사이클에 32 % 손실은 **큰 열화**이고, 이 셀의 엔트로피메트리 "after" 는 그 상태의 것이다 |
| **S2** | 엔트로피메트리 재현성 3 셀 | 신품 #1/#2/#3: 셋 다 +2~+3(3.65–3.75) → −10~−13(4.2–4.25); 후 #1/#2/#3: +3~+4(3.6–3.75) → 0 근방(3.8–4.1) → **#1 −2.3 @4.30 · #2 −4.5 @4.25 · #3 −5 @4.25** | ★ **본문 Fig. 3c "after" (4.25 V 에 +1)와 S2 의 세 곡선(−2.3/−4.5/−5) 이 다르다** — 4 번째 셀이거나 끝점을 잘랐거나 (D2). S4(after, 4.25 V 에 +1)는 Fig. 3c 와 일치 |
| **S3** | "ΔS drop" 3 셀 | 신품 **≈15.1 · ≈13.0**(2 점 보임) ↔ 후 **≈8.0 · ≈5.8**(2 점) — 각각 점선 타원. 정의 `[인쇄]` "difference between the highest and lowest ΔS values over the measured SOC range" | `[재현]` 감소 **≈45–60 %**. 3 셀이라는데 점 2 개 (G2) |
| **S4** | 후 ΔS + dQ/dV | dQ/dV 단위가 **%Q V⁻¹**(0–400; S3b 는 mAh V⁻¹) — 봉우리 3.75 V(≈225) + 4.05 V 둔덕(≈130). 음영 1 구간(3.72–3.80) | 신품(4 음영) ↔ 후(1 음영): 봉우리 넷 중 셋이 사라졌다는 뜻 — dQ/dV 자체가 이미 그것을 말한다 |
| **S7** | volumetry 10 MPa 셀 50 사이클 | 방전 **≈138 → ≈117 mAh g⁻¹**(figure-read ≈85 %; `[인쇄]` 86.0 %), 1st 충전 ≈160 | |
| **S8** | 프레스 사진 | "B Series DIGITAL ELECTRIC PRESS **TPU-040N**", TEMP CONTROL 25.0 °C; 펠릿 셀 SUS 하우징 | ⚠ SI 본문은 **TPU-080** 이라 적는다 (D8) |
| **S9** | volumetry drop 3 셀 | 막대 **≈18.5 / ≈20.3 / ≈18.1 %** | 산포 ≈2 %p — 단일 `dE` 잡음(±0.2 mV/2.2 mV ≈ ±9 %)보다 좁다. `[해석]` 판독이 평균값이면 가능 (G3) |
| **S12** | XRM 10 MPa 전/후 | 3D 렌더 + 기공 맵 **4.5 % → 9.8 %** + 2D 단면(75 µm 바): "NCM layer" 두께 figure-read ≈**60–70 µm**, 후에는 층이 **물결치고 두꺼워진다** | |
| **S13** | volumetry 20 MPa 셀 50 사이클 | 방전 **≈144 → ≈122 mAh g⁻¹**(≈85 %; `[인쇄]` 84.0 %) | ★ **초기 용량이 10 MPa 셀보다 높다**(144 ↔ 138) 그리고 유지율은 낮다 |
| **S14** | XRM 20 MPa 전/후 | 기공 맵 **4.4 % → 5.3 %** | |
| **S16** | volumetry 20 MPa | 위(신품): OCV **3.4758 V** → 10 MPa 에서 3.4741 → **재가압 후 3.4762**(초기 +0.4 mV); 10 MPa 유지 중 **3.4743 → 3.4748 표류**. "OCV drop = 2.3 mV". 아래(후): **3.6476** → 3.6461 → 복귀 3.6479; "2.2 mV" | ★ 비가역 오프셋 +0.4 mV · 표류 +0.5 mV = **노화 신호와 같은 자릿수** (G3) |

**본문과 어긋난 그림**: Fig. 3a (D1 크기), Fig. 3c ↔ S2 (D2 곡선 불일치), Fig. 5e/f (D4 눈금 ·
G6 비선형), Fig. 6 ↔ 본문 등급 정의 (D6), Fig. 4b/c 캡션 ↔ OCV (G4).

# "Maxwell" 의 정의 — 식 전개 (§Introduction + §Entropymetry + §Volumetry + Note S1)

- `[인쇄]` 식 (1) `dG = VdP − SdT`. 식 (2) `ΔG = ΔxFE = W_e` — `Δx` 전극 Li 화학량론 변화,
  `E` 셀 OCV, `F` Faraday. Note S1: `W_e = qE`, `q = ΔxF`, 준평형(무한소 추출 = 가역)이면
  `ΔG = W_e` at OCV.
- **Entropymetry (dP = 0)**: 식 (3) `S = −(dG/dT)_P` → (4) `(dS/dx)_P = −(d/dT)(dG/dx)_P`
  → (5) `dG/dx = FE` → **(6) `ΔS ≡ (dS/dx)_P = (dS_cathode/dx)_P + (dS_anode/dx)_P = −F(dE/dT)_P`**.
  `[인쇄]` "we employed a Li metal anode, whose potential can reasonably be assumed to remain
  constant; thus, the measured entropy change is mainly attributed to the cathode … the
  contribution of SE is negligible." 식 (7) `S = k_B ln W`.
- **Volumetry (dT = 0)**: 식 (8) `V = (dG/dP)_T` → (9) → **(10) `ΔV ≡ (dV/dx)_T =
  (dV_cathode/dx)_T + (dV_anode/dx)_T = F(dE/dP)_T`**.
- `[해석]` 엄밀히는 Maxwell 관계(`(∂S/∂P)_T = −(∂V/∂T)_P`)가 아니라 **`G(x, T, P)` 의 혼합
  2계 편미분의 대칭성**(`∂²G/∂x∂T = ∂²G/∂T∂x`)을 `x` 축에 확장한 것 — 액체셀 엔트로피메트리
  (Yazami 계보, ref [57]) 의 표준 유도와 같다. "Maxwell" 은 이름이지 새 물리가 아니다.
  ★ 그리고 식 (6)·(10) 은 **`E(x, T, P)` 한 상태함수의 두 편미분**이다 — 우리 OCV 적합이 쓰는
  `E(x)` 와 **같은 함수의 다른 방향 도함수**. 그래서 이 편은 OCV 의 *경쟁*이 아니라 OCV 의
  *관측 추가*다 (아래 §접점).
- ⚠ `[해석]` 식 (6) 의 음극항: Li 금속의 부분몰엔트로피 `S°(Li) ≈ 29 J mol⁻¹ K⁻¹` 은 **0 이
  아니라 상수**다 — 모양에는 안 걸리지만 절대값에는 걸린다(논문의 ΔS 는 "cell" 값). 식 (10)
  의 음극항 **`V_m(Li) = 13.0 cm³ mol⁻¹` 도 상수이며 `dV_cathode/dx`(층상 NCM, 전 구간 ≈1–2
  cm³ mol⁻¹) 보다 크다** — 본문의 "10 MPa → Li creep → 음극 pore 무시" 는 **pore 항**에 대한
  논거이지 **이 상수항**에 대한 논거가 아니다 (G5·G13).

# 절별 해체

## §Abstract · §Introduction

- `[인쇄]` 황화물 ASSB 열화 기구 둘: ① 활물질 부피 변화 → **고체 성분 간 물리 접촉 손실** →
  이온·전자 경로 단절 [38–40]; ② 황화물 SE 의 좁은 안정창 → 양·음극 계면 부반응 → **계면
  저항 증가** [41,42].
- `[인쇄]` 현행 진단은 **파괴적 post-mortem**(전자현미경·분광)이고, "the inevitable pressure
  release during cell disassembly … can deform the internal components to potentially obscure
  the true states" [34,53] — 해체 자체가 상태를 바꾼다.
- `[인쇄]` OCV 기반 비파괴법은 액체셀에서 발달했으나 ASSB 에는 드물고, "existing OCV-based
  methods have been considered primarily from a **kinetics** perspective, without incorporating
  **thermodynamic** parameters as inputs" — ★ 이 문장이 이 편의 자기 위치다: **OCV 를 열역학
  파라미터(T, P)로 미분한다**.
- 초록 `[인쇄]` "precise detection of the delithiation heterogeneity … and quantifies internal
  void formation by measuring changes in the OCV in response to temperature and pressure
  variations, respectively, **without perturbing the cell operation**" · 등급 "reuse,
  recondition, or recycle".

## §Entropymetry Method (pp. 2–5)

- 조건: `[인쇄]` 고정 스택 압력이 휴지 중 유지되므로 **등압**(dP = 0). 셀 **NCM811‖Li₆PS₅Cl
  (LPSCl)‖Li**. 온도를 바꾸며 SOC 별 OCV 변화 기록 [56].
- 물리 논거: `[인쇄]` 탈리튬화가 격자 안 Li/공공 배열을 바꿔 **상변화 ↔ 셀 엔트로피 변화가
  상관**; OCV 가 상 의존 에너지를 반영하므로 엔트로피메트리로 CAM 구조 변화를 "as a function
  of the SOC **in real time**" 추적 가능. ★ 그리고 **비균질의 원인을 둘 다** 적는다: `[인쇄]`
  "composite cathodes in ASSBs may experience **local physical contact loss** due to volume
  changes **as well as an increase in the interfacial resistance** resulting from unwanted side
  reactions … This interfacial degradation increases the heterogeneity of the lithiation states
  among CAM particles, which would be reflected in the ΔS". ⇒ **ΔS 는 접촉 손실과 계면 저항을
  한 신호로 받는다** — 이 편 스스로 그렇게 정의한다 (닻 Q2 판정의 핵).
- Fig. 2 논리: `[인쇄]` 상전이 전위(V₁·V₂)에서 등가 에너지 사이트가 최다 → `S` 볼록 최대
  [59]; 균질이면 두 포물선이 분리되고 `ΔS`(= `dS/dx`… 본문은 "the derivative of the S
  profile")는 "two well-resolved, monotonically decreasing sub-profiles with identical
  slopes"; 비균질이면 입자별 SOC 분산으로 분리가 흐려지고, "When the contact loss becomes
  severe or the interfacial resistance increases, the resulting **overpotential** further
  distorts the ΔS profile … asymmetric … reduced ΔS profile near V₂, as fewer particles are
  sufficiently delithiated" + "degradation amplifies the activation barrier … at high
  voltages". ⇒ `[해석]` **OCV 축**에서의 서술이다. 준평형 OCV 에서 "overpotential" 이 남는다는
  것은 곧 **완전히 이완되지 않은 상태**를 측정한다는 뜻 — Fig. 3a 의 OCV 가 150 min 에도 계속
  내려가는 것과 일치한다.
- 프로토콜 (Fig. 3a + SI): 휴지 후 온도 변화(**35 °C 150 min → 20 °C 90 min → 35 °C 60 min**),
  두 35 °C 구간 기준선 적합 → 20 °C OCV 편차 → 식 (6). **5 % SOC 마다 반복**(SI: `[인쇄]`
  "charging at 0.1C for 30 min until reaching an OCV of 4.5 V" — ⚠ Fig. 3b/c 의 OCV 상한은
  **4.25 V** 이고 사이클 상한이 4.3 V 다; D3).
- 검증 1 — dQ/dV 대조 (Fig. 3b): `[인쇄]` "the monotonically declining periods in the ΔS
  profiles corresponded with those around the dQ dV⁻¹ peaks … validating the suitability".
  `[도표]` 봉우리 3.60/3.73/4.00/4.18 V ↔ ΔS 하강 구간. **H1 → M 전이 = 3.7 V** [61].
- 검증 2 — 사이클 전후 (Fig. 3c): 100 사이클 0.5C, 2.5–4.3 V, 10 MPa (Fig. S1). `[인쇄]`
  "In the H1 phase, the ΔS profile of the cycled cell … closely resembled that of the uncycled
  one, whereas the profile deviated pronouncedly upon transition to the M phase" · "after
  cycling, the less discrete phase separation in the high-voltage regime (>4.0 V) was
  reflected in the smoothened dQ dV⁻¹ profile" (Fig. S4). 3 셀 재현성 Fig. S2·S3.
  ⚠ `[도표]` "after" 곡선은 **전 구간 +3.5 ~ 0** 이고 신품의 **−11** 이 사라졌다 —
  "smoother" 가 아니라 **진폭 ≈1/4** 이다 (S3 의 ΔS drop 13–15 → 5.8–8). `[해석]` 비균질
  (OCV 축 뭉갬)은 봉우리를 넓히지 총합을 바꾸지 않는다 — **SOC 축 적분이 ≈ −3.5 → ≈ +1.5 로
  부호가 바뀌는 것**은 (i) 측정 창이 달라졌거나(cycled 셀이 4.25 V OCV 에서 덜 탈리튬 — 논문도
  "fewer particles sufficiently delithiated" 라 적는다) (ii) **재료 자체가 바뀌었거나**(rock-salt
  등 = 진짜 `LAM_PE`) (iii) 음극·이완 인공물이다. 셋 중 어느 것인지 이 편은 가르지 않는다 (G8).
- 형태학 (Fig. 3d,e + S5·S6): `[인쇄]` "severe damage after cycling, which **must contribute**
  to heterogeneous delithiation" — NCM811 이차입자 내부 균열(격자 이방성 부피 변화 [63,64]);
  액체셀은 전해질이 균열로 침투하지만 ASSB 는 못 함 [65,66]; EDS 로 **입자 내부에 S(황) 검출
  안 됨** → SE 가 균열 안에 없음 → 이온 경로 단절 → SOC 분산. 결론 `[인쇄]` "entropymetry
  analysis effectively captures the delithiation heterogeneity and thus degradation".
  ⚠ 여기서 **"접촉 손실"(입자–SE 계면) 과 "입자 내 균열"(SE 없는 내부 균열) 이 Fig. 3e 한
  라벨로 묶인다** — 둘 다 `θ_AM` 의 손실이지만 압력으로 되돌아오는 것은 앞쪽뿐이다
  ([[assb-pressure-reapplication-separation-test]]).

## §Volumetry Method (pp. 5–6)

- 등온(dT = 0)에서 압력을 바꿔 OCV 변화 → 식 (10). `[인쇄]` "volumetry method relates to the
  extent of the volumetric distortion experienced by the active materials in response to the
  change in the stack pressure" · 입자 부피 변화가 주변 환경에 크게 영향받으므로 [67,68]
  "volumetry can be utilized to assess the degree of void formation" · void 가 늘면 "the volume
  of the active material to vary in accordance with the applied pressure" (Fig. 4a: **ΔP 가 void
  로 완화된다**). 근거 인용: **[69] Bielefeld 2022** "abrupt resistance increase when the pore
  volume … surpasses a threshold". 사후 처치(**re-pressurization = reconditioning**) 판단에도
  쓸 수 있다.
- 셀·조건: 스택 **10 MPa**. `[인쇄]` "10 MPa is sufficient to induce creep deformation in Li
  metal [70], thereby allowing the assumption of negligible pore formation in the anode … focusing
  the analysis exclusively on voids within the cathode composite." 50 사이클 전후(Fig. S7),
  디지털 전동 프레스(Fig. S8)로 압력 제어·감지. **ΔP = −5 MPa (10→5)**.
- 결과: `[인쇄]` **dE = 2.2 mV(전) · 1.8 mV(후)** → "decreased by approximately **18 %**" →
  식 (10) 으로 **42.7 · 34.7 µJ mol⁻¹ Pa⁻¹**. `[인쇄]` "The smaller volumetric energy change
  after cycling is attributed to the alleviation of the applied pressure through internal voids".
  3 셀 재현(Fig. S9 `[도표]` 18.5/20.3/18.1 %). 단면 SEM(S10) CAM–SE 계면 void.
- `[재현]` `F·dE/dP`: 2.2 mV/5 MPa → **42.45**, 1.8 → **34.73** µJ mol⁻¹ Pa⁻¹ (본문 42.7 은
  0.6 % 어긋남 — dE 를 2.21 mV 로 썼을 때 값; D5). 차원 = **m³ mol⁻¹** → 42.5 cm³ mol⁻¹.
  ★ 논문이 안 한 비교: Li 금속 몰부피 13.0 cm³ mol⁻¹ 만으로 `[재현]` 5 MPa 에 **0.67 mV**
  가 나온다(같은 부호: 방전이 셀 부피를 줄이므로 가압 → OCV ↑). 실측 2.2 mV 는 그 **3.3 배**.
  `[해석]` 즉 측정된 `dE/dP` 는 격자·금속의 열역학 몰부피로 설명되는 크기가 아니고, **펠릿의
  탄성·접촉 역학이 OCV 에 얹힌 유효 컴플라이언스**다 — 그래서 "void 로 완화" 라는 직관과는
  맞지만 **식 (10) 의 `dV/dx` 라는 이름과는 맞지 않는다**. 그리고 그 크기는 압력 구간에
  따라 **2 배 다르다**(G6).
- XRM 검증 (Fig. 5 + S11·S12): `[인쇄]` 공극률 **4.5 %(전) → 9.8 %(후, 10 MPa)** "more than
  double". ★ `[인쇄]` "While existing electrochemical methods, such as overpotential tracking and
  EIS, can nondestructively monitor … they are limited in their ability to elucidate the
  underlying degradation mechanism. **In contrast, our approach can distinguish between mechanical
  and chemical degradation** by utilizing the relevant thermodynamic principles." ← 이 편의
  **분리 주장**. 근거는 위 두 방법의 정의뿐이고 **교차 실험 0** (G12).
- 정량성 시험 — 20 MPa: `[인쇄]` "higher stack pressures are widely recognized to notably
  decrease the formation of voids **[35]**"(= 5호 Doux). 50 사이클 20 MPa(S13) 후 공극률 **5.3 %**
  = 신품 **4.4 %** 대비 "a mere 20 % increase". OCV 변화 **dP (20→10 MPa) 후 2.2 mV ↔ 전 2.3
  mV**(S16). `[인쇄]` "confirm the strong correlation between the stack pressure and void
  formation while also demonstrating that volumetry can be used to **quantitatively** assess the
  internal porosity." `[재현]` 사상은 **2 점**(Δporosity +5.3 %p ↔ −18 % · +0.9 %p ↔ −4 %) —
  보정 곡선이 아니다.
- ★★ **용량**: `[인쇄]` "the capacity retentions after 50 cycles at 10 and 20 MPa were similar
  at **86.0 % and 84.0 %**, respectively … consistent with … the internal voids may not directly
  affect the early-cycle performance [73,74]. However, … volumetry can nondestructively capture the
  degradation of the electrode integrity **at an early stage, before it is reflected in the
  specific capacity**." ⇒ `[해석]` **void 가 2 배(+5.3 %p)인 셀과 +0.9 %p 인 셀의 용량이
  같다 — 심지어 void 가 적은 20 MPa 셀이 2 %p 더 낮다.** 즉 이 50 사이클 창에서 **void ≠
  겉보기 `LAM_PE`** 이고, 1호의 퍼콜레이션 그림(`θ_AM` 은 `p_c` 위에서는 ≈1)과 정합한다.
  이 편이 우리 3 항 분해에 주는 가장 직접적인 실측이다 ([[assb-apparent-capacity-decomposition]]).

## §Proposing the Maxwell Diagnostic Protocol (pp. 6–8)

- `[인쇄]` 세 등급: **1. Reuse** — "minor interfacial voids … limited heterogeneity"; **2.
  Recondition** — "substantial internal voids … but … fairly homogeneous delithiation … subjected
  to **re-pressurization (>300 MPa)** to heal internal voids and restore the interparticle
  contact"; **3. Recycle** — "delithiation … severely heterogeneous **along with** significant
  void formation … recover the precious metals".
- `[인쇄]` 한계 자인: "quantitative metrics for each degradation mode are important … this
  requires analyzing many cells for statistically robust trends. Since ASSB cells are not yet
  commercially available, securing adequate sample sizes is currently difficult. Once standardized
  cells become accessible, studies correlating Maxwell protocol analysis, postmortem
  characterization, and electrochemical performance can be conducted".
- `[해석]` 등급의 논리 구조는 `(ΔS 신호, ΔV 신호)` 2×2 인데 실험은 **(0,0)·(0,1)·(1,1) 대각선
  근처만** 있다(엔트로피메트리 셀 = 100 사이클, void 도 있을 것; volumetry 셀 = 50 사이클,
  ΔS 안 잼). **(1,0) — 순수 화학 열화 — 칸이 실험에도 그림에도 없다.** 그리고 recondition
  의 ">300 MPa" 는 **수행되지 않았고 인용도 없다**(4호 Shi 는 참고문헌에 없다). Li 금속 셀에
  300 MPa 는 5호의 상한(75 MPa 도금 전 단락)의 4 배 — 재가압 중 단락 여부 미검토 (G11).

## §Conclusion

- `[인쇄]` "entropymetry quantifies the heterogeneity of the microstructures among the layered
  CAM particles, whereas volumetry detects the evolution of voids in the composite electrode …
  enables early-stage monitoring … graded for appropriate and timely treatment."
- Data availability `[인쇄]` "available in the Supporting Information" — SI 에 **원자료 없음**
  (그림 16 장 + 산문).

## SI — Experimental Procedures (전수 전사; 표 없음)

| 항목 | `[인쇄]` 값 |
|---|---|
| 복합양극 | **LiNbO₃-coated NCM811 : LPSCl : VGCF : BR = 76 : 20 : 1.5 : 2.5 wt** (butyl butyrate, slurry, Al foil, 100 °C 건조) |
| SE 층 | LPSCl 펠릿 **∅10 mm**, 냉간 **100 MPa** |
| 스택 | 양극 + SE **350 MPa** 압착 → Li foil → SUS 집전체; 스프링(Shinheung) + 깊이 조절 하우징으로 정압 유지; Ar 글러브박스 |
| volumetry 셀 | 같은 절차, 단 **프레스 안에서** 평가 |
| 사이클 | CC/CV 충전(CV → 0.05C) / CC 방전, **2.5–4.3 V vs Li/Li⁺**, 25 °C, WBCS 3000 (WonATech) |
| 프레스 | **TPU-080 (Tera-leader)** "shown in Figure S7" (⚠ S7 은 사이클 그림, 프레스는 S8; 사진 라벨은 TPU-040N — D8) |
| 엔트로피메트리 | 인큐베이터 IL-11 (JEIO TECH), **35 °C 150 min → 20 °C 90 min → 35 °C 60 min**; SOC 스캔 "charging at 0.1C for 30 min until reaching an OCV of 4.5 V"; 20 °C OCV 를 두 35 °C 사이 기준선 적합으로 보정 |
| 후-사이클 엔트로피메트리 | **100 사이클, 10 MPa, 0.5C**, 2.5–4.3 V |
| volumetry | **50 사이클, 10 또는 20 MPa**, 같은 율; 그 뒤 **12 h 휴지**; **ΔP = −5 또는 −10 MPa, 압력 오차 ≤0.01 MPa**, 원압 복귀 |
| SEM/FIB | JSM-7800F Prime (JEOL) / Helios 650 (FEI) |
| XRM | Xradia 620 Versa (Zeiss, SNU NCIRF), **80 kV · 125 µA · 10 W · 5 h**, "resolution … 0.7 pixels per unit"(sic), Dragonfly Pro 2021.1 · 기공 = "window leveling" 문턱 |
| 기여 | `[인쇄]` "H.K. and S.A. designed the entropymetry protocol" |

★ **없는 것**: 로딩(mg cm⁻² / mAh cm⁻²) · 셀 수(3 이라는 문장만) · 음극 Li 두께 · 스프링 상수 ·
XRM 복셀 · 기공 문턱값 · volumetry `dE` 판독 규칙 · 엔트로피메트리 휴지 시간(Fig. 3a 로는
150 min 뒤 dT).

# 어휘 집계 (본문 + SI, NFKC 정규화 후 `ﬁ`/`ﬂ` 잔존 0; 약어는 대소문자 구분)

`identifiab*` **0** · `uniqu*` 1(무관: "unique solid–solid interfacial dynamics") ·
`uncertaint*` **0** · `error bar`·`standard deviation`·`replicate`·`n =` **0** ·
`reproducib*` 3+1 · `fit*`·`model`·`simulation` **0**(SI `fitting` 1 = 기준선 적합) ·
`LAM`·`LLI`·`SOH`·`state of health` **0** (⚠ 대소문자 무시 집계에서 `SOH` 5 회가 잡혔는데
전부 참고문헌의 저자 "**Soh**n" — 13호의 "fl**am**mable" 교훈 재현) · `contact loss` 1(+ Fig.
3e 라벨) · `percolat*`·`tortuos*` 0 · `void` 26 · `porosity` 10 · `heterogene*` 12 ·
`indium`·`half-cell`·`GITT`·`dead li`·`isolated`·`plating`·`dendrite`·`hysteresis` **0** ·
`OCV` 17+8 · `MPa` 16+15 · `EIS` 1 · `DRT`·`SEI`·`CEI` 0 · `Maxwell` 13 · `entropymetry` 17 ·
`volumetry` 22 · `real time`/`real-time` 1+1 · `quasi-equilibrium` 2+1 · `creep` 1.

# 어긋남 (D)

| # | 어긋남 | 주장 약화 |
|---|---|---|
| D1 | `[도표]` Fig. 3a 의 기준선 이탈 ≈2–4 mV ↔ Fig. 3b 의 3.72 V ΔS ≈ +3 J mol⁻¹ K⁻¹ 가 함의하는 `[재현]` **0.47 mV** — 4–8 배. 예시 그림이거나 다른 점 | ★ 방법 그림이 데이터와 안 맞는다 |
| D2 | Fig. 3c "after 100 cycles" 끝점(4.25 V 에 **+1**) ↔ Fig. S2 세 셀(**−2.3/−4.5/−5**) — 어느 셀도 아님. Fig. S4 는 3c 와 일치 → "three cells" 밖의 4 번째 곡선이거나 끝점 절단 | ★ 재현성 주장의 표본이 불명 |
| D3 | SI "until reaching an OCV of **4.5 V**" ↔ Fig. 3b/c 최대 OCV **4.25 V**, 사이클 상한 4.3 V | 편집급 |
| D4 | 신품 volumetry **42.5(ΔP 5 MPa) ↔ 22.2(ΔP 10 MPa)** µJ mol⁻¹ Pa⁻¹ — 같은 신품 셀 종류에서 2 배. Fig. 5e/f y 축을 달리해 나란히 비교되지 않는다. 본문 무언급 | ★★ **`dE/dP` 는 상수가 아니라 압력 구간의 함수** → "ΔV" 는 재료 상수가 아니다 |
| D5 | 본문 **42.7** ↔ `[재현]` F×2.2 mV/5 MPa = **42.45** ↔ Fig. 5e ≈42.5 (34.7 은 일치) | 편집급 (dE 2.21 mV 로 계산한 듯) |
| D6 | 본문 recycle = "heterogeneous **along with** significant void"(ΔS ∧ ΔV) ↔ `[도표]` Fig. 6 "Recycle (**ΔS signal**)", "Recondition (**ΔV signal**)" | ★ 분류 규칙이 본문·그림에서 다르다 |
| D7 | Fig. 4 캡션 "after discharge at 2.5 V and a rest period" 양쪽 동일 ↔ `[도표]` OCV 3.532(전) / 3.703 V(후), S16 3.476 / 3.648 V — **전·후가 다른 SOC** | ★★ `dV/dx` 의 `x` 가 다르다 (G4) |
| D8 | SI 본문 프레스 "TPU-080 … shown in Figure S7" ↔ S7 = 사이클 데이터, S8 = 프레스, 사진 라벨 **TPU-040N** | 편집급 |
| D9 | `[인쇄]` "in real time" ↔ `[재현]` 1 프로파일 ≈140 h (점당 5 h × ≈28 점) + 사이클 정지 | 서술 |
| D10 | `[인쇄]` "quantitatively assess the internal porosity" ↔ 사상 **2 점**, 보정 곡선 0, 오차 0 | ★ 정량 주장의 근거 |
| D11 | `[인쇄]` "distinguish between mechanical and chemical degradation" ↔ 화학 단독 대조군 0, 20 MPa 셀 엔트로피메트리 0 | ★★ 분리 주장 미검증 |
| D12 | `[인쇄]` "capacity retentions … similar at 86.0 % and 84.0 %" ↔ void 2 배 셀이 **더 높은** 유지율 — "similar" 로 덮인 **역상관** | ★ 우리 축에는 오히려 정보 (void ≠ 용량) |
| D13 | `[인쇄]` "Li metal anode, whose potential can reasonably be assumed to remain constant" ↔ 식 (6)·(10) 의 음극항은 **상수 ≠ 0**(S°(Li) 29 J mol⁻¹ K⁻¹ · V_m 13 cm³ mol⁻¹); 100 사이클 뒤 변화 미검토 | Q5 |
| D14 | 10 MPa 신품 공극률 **4.5 %** ↔ 20 MPa 신품 **4.4 %** — 다른 셀인데 본문은 하나의 "before cycling" 처럼 쓴다 | 편집급 |
| D15 | 초록 "without perturbing the cell operation" ↔ 엔트로피메트리는 사이클을 멈추고 ≈140 h, volumetry 는 12 h 휴지 + 압력 조작 | 서술 |

# [재현] 계산 표

| 양 | 지면 값 | 재계산 | 비고 |
|---|---|---|---|
| `F·dE/dP`, 10→5 MPa, 전 | 42.7 µJ mol⁻¹ Pa⁻¹ | 96485×2.2e−3/5e6 = **42.45** | = 42.5 cm³ mol⁻¹ |
| 같은, 후 | 34.7 | **34.73** | ✓ |
| 감소율 | "approximately 18 %" | 1−1.8/2.2 = 18.2 % · 1−34.7/42.7 = 18.7 % | S9 막대 18.1–20.3 % |
| 20→10 MPa 전/후 | (그림만) | 22.19 / 21.23 | Fig. 5f ≈22.2 / 21.2 ✓ · 감소 4.3 % |
| `dE/dP` 기울기 | — | **0.44 mV/MPa (5–10) ↔ 0.23 mV/MPa (10–20)** | 2 배 (D4) |
| Li 금속 항 | — | V_m = 6.94/0.534 = 13.0 cm³ mol⁻¹ → 5 MPa 에 **0.67 mV** | 실측 2.2 mV 의 30 % |
| ΔS → dE | — | ΔS = 3 → dE = 0.47 mV @ dT = 15 K; ΔS = 11 → 1.71 mV | D1 |
| 공극률 증가 | "more than double" / "mere 20 %" | 9.8/4.5 − 1 = **118 %** · 5.3/4.4 − 1 = **20.5 %** | ✓ |
| 유지율 (figure-read) | 86.0 / 84.0 % | S7 117/138 = 84.8 % · S13 122/144 = 84.7 % · S1 97/143 = **67.8 %** | S1 값은 본문에 없음 |
| 엔트로피메트리 시간 | — | 300 min × 28 점 = **140 h** | D9 |
| 20 MPa 사이클 시간 | — | 50 cy × ≈4.5 h ≈ **225 h** | 5호 Doux: Li 금속 20 MPa 단락 **190 h** — 다른 셀 설계·전류밀도, 이 편은 단락 보고 0 |

# Q1~Q8 판정표 — `assb` 14호

| Q | 판정 | 근거 |
|---|---|---|
| **Q1 접촉 손실 정량** | **★ 있다 — 두 층위.** ① 형태학: **XRM 공극률 vol%** `[인쇄]` 4.5 → 9.8 (10 MPa, 50 cy) · 4.4 → 5.3 (20 MPa) — 4호 Shi 의 void vol%(2.87 → 9.50 @50 cy, ~2 MPa)와 **같은 종류·같은 자릿수**. ② ★ **계보 최초의 비파괴 in situ 대리량**: `F(dE/dP)_T` = 42.5 → 34.7 (−18 %). ⚠ 무차원 `θ` 아님 · 공극률→`dE/dP` 사상 **2 점** · `dE/dP` 가 압력 구간에 2 배 의존(D4) · **접촉 손실 = LAM 안/밖/미언급 → "미언급"**(`LAM` 0 회; 13호 새 제약 4 의 새 칸) | Fig. 5, S9, S12, S14 |
| **Q2 독립 관측** | **★★ 있다, 셋 — 그러나 가르는 쌍이 다르다.** 엔트로피메트리(ΔS 프로파일) · volumetry(dE/dP) · XRM/SEM. 이 편이 가른다고 주장하는 것은 **mechanical(void) ↔ chemical(계면 저항)** 이고, **`LAM_PE` ↔ 접촉 손실은 물음 자체가 없다**. 게다가 `[인쇄]` ΔS 는 "contact loss **as well as** interfacial resistance" 를 한 신호로 받는다고 스스로 정의 → **ΔS 채널은 우리 쌍을 합친다**. 교차 실험 0 (G12·D11). ★ 실익: **void +5.3 %p 에 용량 불변(D12)** = 접촉 손실이 이 창에서는 겉보기 `LAM_PE` 로 나타나지 않는다는 실측 | §Volumetry |
| **Q3 라벨 층위** | **measured-morphological (XRM 문턱 분할, 정확도·복셀 0) + measured-thermodynamic (ΔS drop · volumetry drop, n = 3, 오차 0)**. **"health" 등급의 문턱값 0**(G1) — 라벨이 **정성 등급**이고 정답 축이 **같은 셀의 형태학**(전·후 각 1 개, 다른 셀). 적합 라벨 0 (`fit*` 0). 접촉 손실의 LAM 소속: **미언급** | G1·G2 |
| **Q4 유일성** | **0 (14/14 편) — 성질이 또 다르다: 역문제가 없다.** 관측이 직접 열역학 도함수이고 파라미터 적합이 없으므로 조건수·프로파일이 **정의될 자리가 없다**. 대신 **귀속이 가정**이다: ΔS 변화 → "비균질", dE/dP 감소 → "void" — 대안 원인(재료 변화·음극 항·이완·압력 비선형)을 배제하는 시험 0. ⇒ 계보: 안 쟀다(1–7) → 이름(8) → 지문(9) → 명제(10) → 재료만(11) → 0(12·13) → **14호: "역문제를 두지 않아서 유일성 물음이 사라진 자리 — 그러나 귀속의 유일성은 그대로 안 쟀다"** | 어휘 0 |
| **Q5 Li-In / 음극 기준** | **해당 없음(Li 금속) → 그러나 문제가 남는다.** `[인쇄]` 음극 전위 "constant" 가정 → ΔS·ΔV 전부 양극 귀속. `[해석]` 식 (6)·(10) 의 음극항은 **상수 ≠ 0** 이고 Li 몰부피 항(13 cm³ mol⁻¹)이 양극 격자항보다 크다. 10호의 경고("In 계면 저항이 리튬화도로 변한다")의 Li 금속 판 = **음극 계면이 100 사이클 뒤 어떻게 `dE/dT`·`dE/dP` 에 들어오는가** 미검토 (G13·D13) | 식 (6)(10) |
| **Q6 압력** | **★★★ 있다 — 이 계보에서 가장 새로운 형태: 압력이 관측 변수다.** 제작 100/350 MPa · 운전 **10 / 20 MPa** · 진단 **ΔP = −5 / −10 MPa (≤0.01 MPa)** · 처방 **>300 MPa**(미수행). ① **압력 → OCV 기울기** `[인쇄]` 0.44 mV/MPa(5–10) · 0.23(10–20) — **계보 최초의 `E(P)`** ② 압력 → 공극률 2 점(9.8 / 5.3 %) ③ 압력 → 용량 2 점(86.0 / 84.0 % — **역상관**, 12호까지 "0" 이던 칸에 13호 다음으로 2 점) ④ 20 MPa Li 금속 셀 ≈225 h 사이클에 단락 보고 0 (5호 190 h 와 대조 — 다른 설계). ⚠ 로드셀 계측 명시 없음(프레스 "sensing"), 이력 0, 스윕 0(2 구간) | §Volumetry |
| **Q7 dead Li** | **해당 없음**(Li 금속). `dead li`·`isolated`·`plating` 0. CE `[도표]` S1 첫 사이클 ≈85 %, 이후 ≈98–99 % (눈금 20 %p) | S1 |
| **Q8 화학·OCP** | **★★★ 있다 — 계보 최초로 ASSB 실셀의 OCV 축 위에 열역학 도함수를 준다.** LiNbO₃-NCM811 / LPSCl / Li, 2.5–4.3 V, 기울기 있음. `[도표]` ΔS(OCV) 3.53–4.25 V ≈28 점 + dQ/dV(OCV) 4 봉우리(3.60/3.73/4.00/4.18 V) 신품, 후 1 봉우리(3.75)+둔덕(4.05). ⚠ **SOC 축 없음**(G7) — `E(x)` 곡선 자체는 여전히 0 장(4호 CC V–Q, 11호 0 에 이어). 접촉 손실 = LAM 안/밖: **미언급** | Fig. 3b/c, S4 |

**채움표 누적**: 13편 ≈8.5/8 → **14편 ≈8.5/8 유지** — 새 칸 0. 대신 **Q1 에 "비파괴 대리량"
층, Q6 에 "압력 → OCV" 층, Q8 에 "OCV 축 열역학 도함수" 층**이 붙는다. **Q4 0/14.**

# 우리 축과의 접점

## 1. 보완인가 대체인가 — **보완(관측 추가)**, 대체 아님

- 이 편은 `E(x)` 를 적합하지 않고 `LAM`·`LLI`·`θ` 어느 것도 산출하지 않는다. 산출물은
  **두 지표**(ΔS drop, volumetry drop)와 **정성 등급**이다. 우리 닻의 물음(OCV 적합이
  `LAM_PE` ↔ 접촉 손실을 가르는가)에 이 편은 **답하지 않고, 물음을 두지도 않는다**.
- [[constrained-crb-identifiability]] 의 세 조작(제약 추가 · **관측 추가** · 창 이동) 중
  **관측 추가**다: 감도행렬에 `∂(∂E/∂T)/∂θ_j`·`∂(∂E/∂P)/∂θ_j` 두 행 묶음이 더해진다. 이득
  조건은 "새 행 ≠ 0 이고 기존 행과 독립". `[해석]` 우리 모드에 대해:
  - **균일 `LAM_PE`**(활물질이 균일하게 빠짐, `x` 축 아핀 재조정): ΔS(x) 는 **intensive**
    (몰당)이라 모양 불변 → **새 행 = 0**. volumetry: 격자항 ∝ 활물질량이지만 유효 컴플라이언스가
    지배하므로 **불명**.
  - **완전 고립 접촉 손실**(입자가 전기적으로 사라짐): 참여 분율만 줄고 참여 입자는 균질 →
    ΔS(x) 모양 **불변** → 새 행 = 0. volumetry: void ↑ → **새 행 ≠ 0** (이 편의 주장).
  - **부분 접촉 손실 / 계면 저항 상승**(느린 이완, SOC 분산): ΔS(OCV) 뭉개짐 → **새 행 ≠ 0**.
  ⇒ `[해석]` **엔트로피메트리는 `LAM_PE` 와 완전 고립 접촉 손실 둘 다에 눈멀고(둘 다
  아핀), "덜 연결된" 중간 상태에만 민감하다.** volumetry 는 void 에 민감하되 `LAM_PE` 에는
  (아마) 무감. 따라서 **volumetry 가 우리 쌍을 가르는 후보 행이고, 엔트로피메트리는 아니다** —
  이 편의 자기 서술과 반대 방향의 결론이다(이 편은 ΔS 를 주 진단으로, ΔV 를 보조로 둔다).
  ⚠ 이것은 우리 `[해석]` 이고 실측 0 — 폭 측정기로 검사할 명제다.

## 2. 우리 폭 측정이 붙는 자리

- ① **volumetry 를 [[assb-pressure-reapplication-separation-test]] 의 소신호(small-signal)
  판으로**: 4호 `P↑` 연산자는 300 MPa · 비가역 · 1 회(대신호). 이 편의 `ΔP = −5 MPa` 는
  **가역·반복 가능·0.4 mV** — 같은 물리(`θ_AM(P)`)의 **미분**이다. 근최적 집합 위에서
  `∂E/∂P` 를 추가 잔차로 넣었을 때 `(a_PE, b_PE) ↔ θ` 폭이 얼마나 주는지 재는 것이
  우리가 이 프로토콜에 공급할 수 있는 것. ⚠ 단 D4(구간 의존)·D7(SOC 의존)·G3(판독 규칙)
  때문에 **`E(P)` 곡선 자체가 먼저 모델링돼야 한다** — 선형 `ΔV` 상수로는 못 쓴다.
- ② **ΔS(x) 를 [[halfcell-ocp-shape-invariance]] 의 두 번째 상태함수 검사로**: 아핀 창
  모형이 맞으면 `E(x)` 와 `∂E/∂T(x)` 가 **같은 (α, β) 로** 재조정돼야 한다. 두 곡선의 (α, β)
  가 어긋나면 아핀 전제가 깨진 것 — `E(x)` 하나로는 못 보는 검사. ⚠ 이 편의 ΔS 는 OCV
  축이라 SOC 축 변환(G7)이 먼저다.
- ③ **sum rule 검사(G8)를 이 편 데이터에 적용**: S2 세 셀의 전·후 ΔS 를 SOC 축 적분해
  총 엔트로피 변화가 보존되는지 — 보존되지 않으면 "비균질" 만으로는 설명 불가 = 진짜
  재료 변화(`LAM_PE`) 또는 인공물. 이 편이 인쇄한 그림으로 우리가 할 수 있는 뺄셈이며,
  **이 편은 하지 않았다**(7호·11호와 같은 형태).

## 3. 이웃 대조 (큐 안)

| 이웃 | 이 편과의 관계 |
|---|---|
| **4호 Shi 2020** | void vol% 같은 종류·자릿수(9.50 @50 cy ↔ 9.8 %); **>300 MPa 재가압** 처방이 4호의 실측(300 MPa, +60.5 %p)과 같은 숫자인데 **인용 없음**. 4호는 In 음극, 이 편은 Li 금속 — 300 MPa 의 안전성이 다르다 |
| **5호 Doux 2020** | ref [35]. 5호 `Z(P)` ↔ 이 편 `E(P)` — **압력 축의 두 번째 관측량**. 5호 Li 금속 20 MPa 단락 190 h ↔ 이 편 20 MPa ≈225 h 사이클 단락 보고 0 (전류밀도·설계 다름). 5호의 이력(`θ(P)` 경로 의존) 은 이 편의 S16 +0.4 mV 오프셋에 그림자로 보인다 |
| **9호 Huo 2025** | 9호는 `A_eff·ε_p/R_s` 를 **적합**으로 정하고 유일성 0; 이 편은 **적합 없이** 직접 도함수 — 역문제를 없앤 대신 귀속을 가정. 둘 다 `θ` 의 시간축을 못 준다(이 편은 전·후 2 점) |
| **10·11호 EIS/DRT** | `[인쇄]` "overpotential tracking and EIS … limited in their ability to elucidate the underlying degradation mechanism" — 이 편이 EIS 계보를 밀어내는 문장. 10호가 EIS 의 비유일성을 인쇄했고 이 편은 그 대안으로 **모델 차수가 없는 관측**을 제시 — 그러나 귀속의 유일성은 EIS 와 같은 상태 |
| **13호 Zheng 2026** | 13호의 SOH 이분법(true AM loss ↔ usable capacity)에 이 편은 **세 번째 축(void)** 을 더한다 — 그리고 **void 가 용량에 안 보인다**(D12)는 실측으로 13호의 "impedance 로 나타나는 손실" 쪽에도 안 들어감을 보인다. 13호 후속 4 순위 **Oh *AEM* 2025 = ref [10], 같은 저자**. 13호가 요구한 "pressure sensing" 을 이 편은 **진단 조작**으로 쓴다 |
| **1호 Bielefeld 2019** | 이 편의 [69] = Bielefeld **2022**(퍼콜레이션 문턱의 실험판) — 1호 `p_c` 의 후속. D12(void ↑ 용량 =)는 `θ_AM ≈ 1 above p_c` 그림과 정합 |

# 후속 후보 (원전 우선)

1. ★★★ **Oh, Kwon, Choi, …, Choi, *Adv. Energy Mater.* 2025, 15, 2404817** (ref [10]; 13호
   [34]) — 같은 연구실의 **저 N/P·저압 실셀**. 13호 후속 4 순위와 합쳐 1 순위로 승격 (Q6).
2. ★★★ **Bielefeld, Weber, Rueß, Glavas, Janek, *J. Electrochem. Soc.* 2022, 169, 020539**
   (ref [69]) — "pore volume 문턱 → 저항 급증" 의 실험 원전; 1호 `p_c` 의 실측판 (Q1).
3. ★★ **Kim, Kim, Kim, Chang, Choi, *PNAS* 2022, 119, e2211436119** (ref [56]) — 이 연구실의
   엔트로피메트리 원전(액체셀 NCM?) — ΔS 의 SOC 축·sum rule·오차 처리 확인 (G7·G8).
4. ★★ **Kim, Park, Kwon, …, Yazami, Choi, *EES* 2020, 13, 286** (ref [57]) — 엔트로피메트리
   계보의 Yazami 접점; `dE/dT` 정밀도·이완 기준선 처방.
5. ★★ **LePage et al., *JES* 2019, 166, A89** (ref [70]) — "10 MPa 에서 Li creep" 의 근거;
   이 편의 음극 pore 무시 가정의 원전 (Q5·Q6).
6. ★ **Lewis et al., *Nat. Mater.* 2021, 20, 503** (ref [73]) · **Lu et al., *Sci. Adv.* 2022,
   8, eadd0510** (ref [74]) — "void 가 초기 성능에 안 보인다" 의 원전 (D12 의 문헌 맥락).
7. ★ **Lee, Han, Lewis, …, McDowell, *ACS Energy Lett.* 2021, 6, 3261** (ref [34]) — "해체
   시 압력 해제가 상태를 바꾼다" 의 원전 (post-mortem 라벨의 신뢰성, Q3).

큐 14~37 과의 겹침: `ASSB_TRANSFER_NOTE.md` 를 Oh·Bielefeld·LePage·Lewis·Kim PNAS 로 검색 —
**0 건** (Bielefeld 는 **2019** 편(1호, 흡수 완료)만 큐에 있고 2022 편은 없다; Oh *AEM* 2025 는
13호 후속 후보 목록에만 있다).
