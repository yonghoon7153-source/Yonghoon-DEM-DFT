# NMC532 **이차입자**의 E · H · 계면 K_c 를 **SOC · 사이클의 함수로** — 글러브박스 나노압입 (Berkovich Oliver–Pharr + cube-corner pop-in), 소결 펠릿 · 제일원리 E 대비 — Xu, Sun, de Vasconcelos, Zhao (J. Electrochem. Soc. 2017, Purdue)

> slug `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` · DOI `10.1149/2.1751713jes` · type `exp (instrumented nanoindentation in Ar glovebox — Berkovich Oliver–Pharr E·H + cube-corner pop-in K_c; sintering-pellet contrast) + ab-initio E(SOC)` · PDF `12b057a2-Xu_2017_J._Electrochem._Soc._164_A3333.pdf` · digested `2026-09-25` · status ✅

> 본문 9 pp = *J. Electrochem. Soc.* **164** (13) **A3333–A3341** (2017).  업로드 PDF 는 IOP 표지 1쪽 + 본문 9쪽 = 10쪽.
> **이 카드의 "p." 는 저널 쪽 (A3333–A3341)** 이다.  PDF 쪽 = 저널 쪽 − 3331 (예: p. A3337 = PDF 6쪽).
> ⛔ **SI (Fig S1–S7) 미보유** — pop-in 하중곡선(S1) · AFM 균열 이미지와 입자-vs-펠릿 하중곡선(S2) · 입도·펠릿 SEM·XRD(S3) ·
> DFT 결합길이·Bader·격자상수(S4–S7) 는 **본문 문장으로만** 안다.  그 내용에 기대는 판정은 이 카드에서 하지 않는다.
> 그림 9장(본문 Fig 1–8 + Table 1) 전부 `litdb/figures/xu2017_nmc532_nanoindentation_modulus_hardness_toughness/` —
> **Fig 1 · Table 1 은 수동 크롭** (§5 끝), 전 9장 육안 확인.
> ⚠ PDF 표지의 "You may also like" 에 **같은 제목의 ECS 학회 초록**(Kejie Zhao 단독) 이 있다 — **그것은 이 논문이 아니다.**
> ★ 이 카드는 **원장 SELF-51** (우리 코드의 E_AM = 140 GPa 출처 · 틀린 서지 *"Phys. Rev. X 7, 041038"*) 의 원문 대조로 만들었다 — §0 · §7 · §8.

---

## 0. ★ 원고 각주 · SELF-51 확인값 — 이것부터 (2026-09-25 PDF 원문 대조)

| 질문 | 확인값 | 근거 (쪽 · 그림 · 표) | 등급 |
|---|---|---|---|
| **서지** | R. Xu, H. Sun, L. S. de Vasconcelos, K. Zhao, *J. Electrochem. Soc.* **164** (13) A3333–A3341 (2017), DOI 10.1149/2.1751713jes.  투고 2017-09-12 · 수정 2017-10-16 · 출판 2017-11-02 | p. A3333 머리 | ✅ PDF 확인 |
| **옛 서지 *"Phys. Rev. X 7, 041038 (NCM811 nanoindentation)"*** | **이 논문이 아니다** — 저널·권·쪽·조성 전부 불일치 (이 논문은 JES · **NMC532**).  PRX 7, 041038 의 실체는 이 컨테이너에서 확인 불가 (Crossref 접속 거부) | — | ⛔ 틀린 서지 |
| **조성** | **LiNi₀.₅Mn₀.₃Co₀.₂O₂ (NMC532)** — MTI 상용 전극.  ⛔ **NCM811 이 아니다** | p. A3333 *"an example LiNi0.5Mn0.3Co0.2O2 (NMC532, referred as NMC in the following text) electrode"* | stated |
| **pristine E** | **142.5 ± 11.3 GPa** | p. A3336 끝 문단 · Table 1 (p. A3337) · Fig 4b 검정 막대 (*"142.5 ± 11.33"*) | stated |
| **pristine H** | **8.6 ± 1.3 GPa** | 같은 곳 (Fig 4b 문장: *"8.58 ± 1.3"*) | stated |
| **n · ±** | 배치당 **서로 다른 이차입자 15개** (*"on 15 different secondary particles in each batch"*).  ± 가 SD 인지 SE 인지 **E·H 에 대해서는 명시 없음** (K_c 는 *"standard deviations"* 명시) | p. A3334 | stated / ± 정의 미기재 |
| **측정 조건** | Keysight **G200** · **Ar 글러브박스 안** · **Berkovich** · **Oliver–Pharr** · P_max **1 mN** (균열 문턱 2 mN 아래) · 하중/유지/제하 **10 / 5 / 10 s** · **연마한 전극 단면**에서 **지름 > 10 µm 이차입자의 중심** (targeted indentation) · 압흔 < 1 µm · E 환산: 다이아몬드 E_i **1141 GPa**, ν_i **0.07**, **NMC ν = 0.3 가정** | p. A3334 · p. A3336 | stated |
| **압입 위치** | **이차입자 단면의 중심** (1차입자 ≈1 µm 가 모인 "meatball" 응집체) — **1차입자 1개도, 단결정도 아니다.**  압흔 크기 ≈ 1차입자 크기라 **입계(GB) 가 섞인 응집체 국소값** | p. A3334 · p. A3337 *"The mechanical response of NMC is largely influenced by the "grain boundaries""* | stated |
| **"pristine" 의 상태** | **as-received 상용 전극** (80 °C 진공 건조, 셀 조립 안 함) = **전해질·전기화학 이력 없음, 완전 리튬화 (SOC 0 %)** | p. A3333–A3334 · p. A3337 *"0% represents the pristine NMC"* | stated |
| **완전 충전 (SOC 100 % ≡ 저자 표기 Li₀.₅)** | E **111.6 ± 6.4** · H **7.1 ± 0.8 GPa** (저자: pristine 의 *"about 77% and 80%"*) | p. A3337 · Fig 5a | stated |
| **100 사이클 후 (방전 = "fully lithiated")** | E **107.3 ± 13.3** · H **6.5 ± 0.9 GPa** (*"74% and 73%"*) | p. A3338 · Fig 5b | stated |
| **소결 펠릿 (bulk 대조)** | E **177.5 ± 19.5** · H **12.6 ± 1.4 GPa** · K_c **0.309 ± 0.04 MPa·m^½** (결정립 ≈ 10 µm; 볼밀 1차입자 → 180 MPa 성형 → 1000 °C 10 h) | p. A3334 · p. A3335 · p. A3337 · Table 1 · p. A3339 | stated |
| **제일원리 E (pristine)** | **190.0 GPa** (VASP PBE+U, 120 원자, x·y·z 단축인장 평균) | Table 1 · p. A3335 | stated |
| **계면 파괴인성 K_c (pristine 이차입자)** | **0.102 ± 0.03 MPa·m^½** — cube-corner 압입 · **pop-in 법**으로 균열길이 · 시료당 15압입 중 **8–10개**만 사용 | p. A3339 · Table 1 · Fig 8 | stated |
| K_c (SOC 100 %) | ≈ **0.058** (판독) — 본문 *"reduces by nearly a factor of two"* | Fig 8a · p. A3340 | digitized |
| K_c (100 사이클) | **0.036 ± 0.018** (*"over 60% of the fracture strength is lost"*) | p. A3340 · Fig 8b | stated |
| **"계면 파괴강도"** (초록 표현) | **강도(MPa) 는 한 번도 재지 않았다.**  초록의 *"interfacial fracture strength"* = 본문의 **파괴인성 K_c (MPa·m^½)** 다 | p. A3333 초록 vs p. A3334 | 용어 주의 |
| **이 논문이 인용한 다른 값** | E·H: *"elastic modulus and hardness of NMC thin films and pellets"* [26 Kim 2016 *Extreme Mech. Lett.* 9, 439 · 27 Cheng 2017 *J. Eur. Ceram. Soc.* 37, 3213] — **숫자는 옮기지 않았다**.  펠릿·DFT 가 *"agree well with other reports"* [6 Sun & Zhao 2017 *JPCC* 121, 6002 · 10 Li 2017 *J. Solid State Electrochem.* 21, 673] — **역시 숫자 없음**.  K_c: **LiMn₂O₄ 0.49 ± 0.13** [29 Amanieu 2014 *Mater. Sci. Eng. A* 593, 92] · **LiCoO₂ 0.9 ± 0.1** [31 Swallow 2014 *JES* 161, F3084] — **둘 다 NMC 아님** | p. A3333 · p. A3337 · p. A3340 | stated |
| **우리 E_AM 140 GPa** | pristine NMC532 이차입자 142.5 ± 11.3 과 **−0.22 SD = 정합**.  단 **조성이 다르고 (532 ≠ 811)**, 140 이라는 숫자는 **이 논문에 없다**.  NCM811 조성 일치 값 = 짝 카드 `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` 의 다결정 NMC811 나노압입 **138 ± 24 GPa (n = 29)** (그 카드의 기록) — 두 조성의 응집체 E 차 (4.5 GPa) 는 **양쪽 SD 안** | §7-1 | 판정 ✅(한정어 필수) |
| **우리 H_AM 6.0 GPa** | pristine 8.6 ± 1.3 대비 **−2.0 SD — 이 논문으로 뒷받침되지 않는다.**  6.0 에 가까운 것은 **열화 상태** (100 cyc 6.5 · SOC100 7.1) | §7-2 | 판정 ⛔ |
| **우리 K_IC_P 0.3 / K_IC_S 1.0** | 0.3 은 이 논문의 **소결 펠릿 (0.309)** 과 같고 **이차입자 (0.102) 의 3배**.  1.0 (단결정) 에 대응하는 측정은 **없다** | §7-3 · §8 | 판정 ⚠ |
| **우리 ν_AM 0.25 *"(Xu 2017)"*** | 이 논문은 ν 를 **재지 않았고 0.3 을 가정**했다 ⇒ 0.25 의 출처로 쓸 수 없다 | p. A3334 | 판정 ⛔ |

---

## 1. 한 줄 요약

상용 **NMC532 전극**(MTI, 94.2 : 3.0 : 2.8 = NMC : CB : PVDF)을 액체 반쪽셀에서 **첫 충전 도중(SOC 33/66/100 %)** 과
**사이클 후(1/30/50/100)** 에 해체·연마하고, **Ar 글러브박스 안의 나노압입**으로 **이차입자 단면 중심**의
**E · H (Berkovich, Oliver–Pharr, 1 mN)** 와 **계면 파괴인성 K_c (cube-corner, pop-in 법)** 를 잰 논문.
pristine 이차입자는 **E 142.5 ± 11.3 · H 8.6 ± 1.3 GPa · K_c 0.102 ± 0.03 MPa·m^½** 로, 같은 분말을 치밀하게 소결한
**펠릿 (177.5 · 12.6 · 0.309)** 보다 E 는 **0.80×**, H 는 **0.68×**, K_c 는 **⅓** 이다 — 원인은 **1차입자 사이의 약한 계면**.
탈리튬화하면 E·H 가 **~20 %**, K_c 가 **~40 %** 떨어지고, 100 사이클 후엔 E·H **~25 %**, K_c **~65 %** 가 사라진다
(**첫 사이클이 가장 큰 계단**).  DFT (PBE+U) 는 E 를 **190 → ≈150 GPa** 로 선형 감소시켜 **방향**을 재현한다.
★ **리포에서 NMC 이차입자의 E·H·K_c 를 한 시료군에서 같이 준 유일한 원문**이자, 우리 **E_AM = 140 GPa** 가
**"이차입자 응집체" 급 값**임을 보이는 근거 — 단 **NMC532** 이고, 우리 **K_IC_P 0.3** 은 이 논문의 **이차입자가 아니라 펠릿** 값과 같다.

---

## 2. 메타

| 저자 | 소속 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|---|
| **Rong Xu**, Hong Sun, **Luize Scalco de Vasconcelos**, **Kejie Zhao\*** (kjzhao@purdue.edu) | School of Mechanical Engineering, **Purdue University** (West Lafayette, IN) | *J. Electrochem. Soc.* **164** (13) **A3333–A3341** (2017) | 10.1149/2.1751713jes | **NMC532 (LiNi₀.₅Mn₀.₃Co₀.₂O₂)** 상용 전극 (MTI) + 같은 분말의 소결 펠릿 | **실험** (나노압입 E·H·K_c, AFM, SEM, XRD, 액체 반쪽셀) + **보조 계산** (VASP PBE+U 단축인장 E) |

- 자금: NSF **CMMI-1726392 · CBET-1603866**.  감사: B. Deng (시료), J. He (AFM), Q. Sun (XRD).
- **같은 그룹 선행 [15]** (R. Xu, L. S. Vasconcelos, J. Shi, J. Li, K. Zhao, *Exp. Mech.* 2017) = "1차입자 탈접착 (decohesion) 이
  NMC 의 주된 기계적 열화" 를 국소 형태 추적으로 먼저 보였고, 이 논문은 그 **정량판** (E·H·K_c 의 SOC·사이클 궤적).
- **DFT 해석은 같은 그룹의 [6] Sun & Zhao, *J. Phys. Chem. C* 121, 6002 (2017)** 에 기댄다 (*"We discussed the detailed TM-O
  interactions in NMC in an earlier publication.6"*).
- ⚠ **SI 미보유** (위 머리말).  ⚠ **데이터 공개 없음.**

---

## 3. 핵심 수치 ★ (stated / digitized / DERIVED 구분)

### 3-1. Table 1 — **stated** (p. A3337, 크롭 `tab_1.png` 로 원문 재확인)

| | **NMC 이차입자** | **NMC 소결 펠릿** | **제일원리** |
|---|---|---|---|
| **E (GPa)** | **142.5 ± 11.3** | **177.5 ± 19.5** | **190.0** |
| **H (GPa)** | **8.6 ± 1.3** | **12.6 ± 1.4** | N/A |
| **K_c (MPa·m^½)** | **0.102 ± 0.03** | **0.309 ± 0.04** | N/A |

- DERIVED (우리 산술): 펠릿/입자 = **E 1.246× · H 1.465× · K_c 3.03×**.  입자/DFT = **0.750**, 펠릿/DFT = **0.934**.
- 펠릿 **상대밀도·기공률은 보고 없음** (SEM 에 *"no obvious pores and cracks"* 라는 정성 서술뿐, p. A3335) ⇒ 펠릿 E 177.5 에 기공 효과가
  얼마나 들어 있는지 모른다.

### 3-2. E · H vs **SOC** (첫 충전, Fig 5a, p. A3338) — 양 끝 **stated**, 중간 **digitized**

| SOC (저자 정의) | E (GPa) | H (GPa) | 등급 |
|---|---|---|---|
| **0 %** (pristine) | ≈ **145.1** (막대 ≈ 134–156) | ≈ **8.9** (≈ 8.1–9.7) | digitized — ⚠ Table 1 의 142.5 / 8.6 과 다르다 (§8-1) |
| 33 % | ≈ **131.1** (≈ 118–144) | ≈ **8.0** (≈ 7.1–8.9) | digitized |
| 66 % | ≈ **116.0** (≈ 98–134) | ≈ **7.65** (≈ 6.1–9.2) | digitized |
| **100 %** (≡ Li₀.₅, 저자 표기) | **111.6 ± 6.4** (판독 111.6) | **7.1 ± 0.8** (판독 7.10) | stated (판독이 재현) |

- 저자 비율 *"about 77% and 80%"* — Table 1 기준 우리 산술은 **78.3 % · 82.6 %**, Fig 5 의 0 % 점(≈145.1 / 8.91) 기준은
  **76.9 % · 79.7 %** ⇒ **저자 비율은 Table 1 이 아니라 Fig 5 의 0 % 점으로 계산된 것**으로 읽힌다 (§8-1).
- SOC 의 기준 용량은 **정의 없음** (*"until cells reach 33%, 66%, and 100% of SOC"*).  **"100 % = Li₀.₅" 도 저자 표기**이지
  측정된 Li 함량이 아니다 (§8-4).

### 3-3. E · H vs **사이클** (Fig 5b, p. A3338) — 끝점 **stated**, 나머지 **digitized**

| 사이클 | E (GPa) | H (GPa) | 등급 |
|---|---|---|---|
| **0** (pristine) | ≈ **144.9** (≈ 135–155) | ≈ **8.9** (≈ 8.1–9.7) | digitized |
| **1** | ≈ **125.4** (≈ 112–139) | ≈ **8.1** (≈ 6.8–9.4) | digitized — **가장 큰 계단** (E −13.5 %) |
| 30 | ≈ **114.5** (≈ 94–135) | ≈ **7.1** (≈ 5.3–8.9) | digitized |
| 50 | ≈ **115.1** (≈ 105–125) | ≈ **7.0** (≈ 6.3–7.8) | digitized |
| **100** | **107.3 ± 13.3** (판독 107.2) | **6.5 ± 0.9** (판독 6.46) | stated (판독이 재현) |

- **측정 상태 = 방전 (lithiated)** — *"the elastic modulus and hardness of fully lithiated NMC steadily decrease"* (p. A3338).
- "1" 점의 정체는 본문에 따로 정의가 없다 — Methods 의 *"initially charged and discharged at C/20, followed by 30, 50, and 100
  cycles at C/5"* 로 보아 **C/20 형성 1회 후**로 읽힌다 (추정).  30/50/100 이 형성 포함 총 횟수인지도 **미기재**.
- 저자 비율 *"74% and 73%"* — Table 1 기준 **75.3 % · 75.6 %**, Fig 5b 0 점 기준 **74.1 % · 73.1 %** ⇒ §3-2 와 같은 패턴.

### 3-4. 계면 파괴인성 K_c (Fig 8, p. A3340) — 끝점 **stated**, 나머지 **digitized**

| 축 | 점 | K_c (MPa·m^½) | 등급 |
|---|---|---|---|
| SOC | 0 % | **0.102** (판독 0.1022, 막대 ≈ 0.071–0.133) | stated |
| SOC | 33 % | ≈ **0.091** (≈ 0.067–0.116) | digitized |
| SOC | 66 % | ≈ **0.070** (≈ 0.037–0.104) | digitized |
| SOC | 100 % | ≈ **0.058** (≈ 0.037–0.079) → pristine 의 **0.57×** | digitized (본문 *"nearly a factor of two"*) |
| 사이클 | 0 | **0.102** | stated |
| 사이클 | 1 | ≈ **0.088** (≈ 0.064–0.113) | digitized |
| 사이클 | 30 | ≈ **0.070** (≈ 0.047–0.093) | digitized |
| 사이클 | 50 | ≈ **0.051** (≈ 0.028–0.075) | digitized |
| 사이클 | **100** | **0.036 ± 0.018** (판독 0.0357) → pristine 의 **0.35×** (−64.7 %) | stated |

- 균열 개시 하중 (문턱): **이차입자 ≈ 2 mN vs 펠릿 > 10 mN** (p. A3339–A3340, Fig S2 — 미보유).
- 시료당 **15 압입 중 8–10 개**만 평균에 사용 — 나머지는 *"erroneous load-displacement curves"* 로 제외 (기준 미기재, §8-6).

### 3-5. 대조 실험 (Fig 4, p. A3336–A3337)

| 대조 | 결과 | 등급 |
|---|---|---|
| **압입 위치** (Fig 4a, 1 mN, 두 입자 D ≈ 28 · 15 µm) | 0.25 < y/D < 0.75 에서 값이 수렴; 본문 *"∼145 GPa"*, 기지(matrix) *"< 15 GPa"* | stated |
| ↳ 판독 | 입자 안쪽(0.25–0.75): D≈28 µm **n 13, 평균 ≈ 142.7, 범위 ≈ 126–163** · D≈15 µm **n 9, 평균 ≈ 149.7, 범위 ≈ 141–165**.  청색 점선 ≈ **141.6 GPa** (본문은 *"about 145"*).  ⚠ 기지 점은 ≈ **6–44 GPa** 로 절반 가량이 *"< 15"* 를 넘는다 (§8-2) | digitized |
| **기지 재료** (Fig 4b) | CB+PVDF 기지: **E 1.78 ± 0.35 · H 0.043 ± 0.01 GPa** / 페놀수지(PR) 기지: **E 10.1 ± 0.8 · H 1.1 ± 0.2 GPa**.  그 안의 NMC: **CB+PVDF 에서 E 142.5 ± 11.33 · H 8.58 ± 1.3**, **PR 에서 E 146.6 ± 9.81 · H 8.65 ± 1.02** ⇒ **기판(기지) 효과 무시 가능** | stated |
| **하중 의존** (Fig 4c) | < 2 mN = 하중 무관 (영역 I); > 2 mN QS 는 단조 감소, CSM 은 **균열로 계단식 급락**; > 10 mN 은 계면균열 + sink-in 으로 **O–P 법 부적합** ⇒ **P_max 1 mN 채택** | stated |
| ↳ 판독 (QS) | 0.5 mN ≈ **145** (±15) · 1 mN ≈ **142** (±12) · 2 mN ≈ **141** (±12) · 3 mN ≈ **121** · 6 mN ≈ **102** · 10 mN ≈ **86** · 12 mN ≈ **81 GPa**.  CSM 급락 ≈ **2.4 · 5.2 · 7.2 mN** | digitized |

### 3-6. 전기화학 (Fig 2, p. A3335) — 기계측정의 **이력** 기록

| 항목 | 값 | 등급 |
|---|---|---|
| 셀 | CR2032 반쪽셀: NMC 전극 / **Li 금속** / Celgard 2502 / **1 M LiPF₆ in EC:DEC 1:1** (**액체**) | stated |
| 창 · 율 | **3.0–4.3 V**; SOC 배치 = **C/20** 첫 충전; 사이클 배치 = C/20 1회 + **C/5** | stated |
| 방전용량 1 / 50 / 100 번째 | **160.5 / 150.4 / 134.9 mAh g⁻¹** | stated |
| 유지율 | **93.7 %** (50, Sample I) · **84.1 %** (100, Sample II) | stated (160.5 기준 산술 일치) |
| 쿨롱효율 | *"initial cycle 84.3%"* · 이후 > 97.5 % | stated — ⚠ Fig 2b 첫 점 ≈ **94 %** · Fig 2a 1번째 사이클 충전 ≈ **164** / 방전 160.5 → ≈ **98 %** (§8-3) |
| 전극 | NMC **94.2** : CB **3.0** : PVDF **2.8 wt%** · 두께 **45 ± 6 µm** · 로딩 **121 g m⁻²** | stated |
| ↳ 전극 밀도 · 기공 | 121 g m⁻² / 45 µm = **≈ 2.7 g cm⁻³** → 진밀도 가정(NMC 4.75 · CB 2.0 · PVDF 1.78) 시 **기공 ≈ 35–38 %** | DERIVED (가정 포함) |

### 3-7. 제일원리 (Fig 6, p. A3339) — E(0 %) 만 **stated**, 나머지 **digitized**

| SOC | E_DFT (GPa) | 응집에너지 (eV/atom) | Bader O (e) | Bader TM (e) | E_exp(Fig 5a)/E_DFT (DERIVED) |
|---|---|---|---|---|---|
| 0 % | **190.0** (판독 189.8) | ≈ 0.82 | ≈ −1.18 | ≈ +1.467 | ≈ 0.76 |
| 33 % | ≈ 176.9 | ≈ 0.68 | ≈ −1.115 | ≈ +1.485 | ≈ 0.74 |
| 66 % | ≈ 165.8 | ≈ 0.51 | ≈ −1.05 | ≈ +1.499 | ≈ 0.70 |
| 100 % | ≈ 149.8 | ≈ 0.32 | ≈ −0.99 | ≈ +1.530 | ≈ 0.75 |

- DFT 의 0 → 100 % 감소율 **0.789×** ↔ 실험(Fig 5a) **0.769×** — **상대 감소는 거의 같다** (우리 관찰; 저자는 *"qualitatively agrees"*
  만 말하고 *"quantitative discrepancy"* 를 계면 구조 탓으로 돌린다).  ⇒ **E_exp/E_DFT ≈ 0.70–0.76 이 SOC 에 거의 무관** = 응집체
  할인율이 SOC 와 곱해지는 꼴이라는 해석이 가능 (4점 판독, TREND only).
- ⚠ **응집에너지 절대값이 정의와 맞지 않는다** — 본문 정의는 *"the energy to break the lattice into isolated free atoms"* 인데,
  층상 산화물의 원자화 에너지는 **수 eV/atom** 급이다.  **0.3–0.8 eV/atom 은 그 정의의 값일 수 없다** ⇒ 절대값 해석 금지, 추세만 (§8-8).

### 3-8. 재료 · 시료

| 항목 | 값 | 등급 |
|---|---|---|
| 이차입자 평균 | **≈ 10 µm** (Fig S3a) | stated |
| 1차입자 평균 | **≈ 1 µm** (Fig S3b) | stated |
| 압입 대상 | **지름 > 10 µm 이차입자**의 연마 단면 중심 (Fig 4a 의 두 입자 D ≈ 28 · 15 µm) | stated |
| 소결 펠릿 결정립 | **≈ 10 µm** (파단면, Fig S3d) | stated |
| 펠릿 공정 | as-received 이차입자 분말을 **볼밀로 1차입자화** → **2 g · Ø13 mm · 180 MPa 단축 성형** (Carver 4350) → **1000 °C 10 h** (10 °C/min) → SiC 사포 + 다이아몬드 연마 | stated |
| 상 확인 | XRD (Bruker D-8 Focus, Cu Kα, 2θ 12–90°): 전극·펠릿 패턴 유사 | stated (⚠ §8-7) |

### 3-9. 압흔 크기 — **DERIVED** (이상 기하 가정, 우리 산술)

| 압자 · 하중 | 접촉깊이 h_c | 압흔 한 변 | 비고 |
|---|---|---|---|
| Berkovich 1 mN (H 8.6) | **≈ 69 nm** | **≈ 0.52 µm** | A = P/H, A = 24.5 h_c² — **1차입자(≈1 µm) 1개 크기** |
| Berkovich 2 mN | ≈ 97 nm | ≈ 0.73 µm | Fig 4c 삽입 적색 곡선 끝(≈ 95 nm) 과 정합 |
| cube-corner 3 mN | ≈ 366 nm | ≈ 0.90 µm | A = 2.598 h_c² — Fig 7b 의 h_m ≈ 369 nm 와 정합 |

---

## 4. 실험 · 계산 방법 ★

### 4-1. 시료 (p. A3333–A3334)
- **전극**: MTI 상용 NMC532 (위 조성·두께·로딩).  80 °C 진공 하룻밤 건조 → **Ar 글러브박스 (H₂O · O₂ < 1.0 ppm)** 보관 수일.
- **셀**: CR2032, Li 포일, Celgard-2502, 1 M LiPF₆ EC/DEC (1:1 vol, Sigma).  하룻밤 휴지 (젖음).
- **SOC 배치**: C/20, 3–4.3 V 로 **SOC 33 / 66 / 100 %** 까지 충전 후 해체.
- **사이클 배치**: C/20 충방전 1회 → C/5 로 **30 / 50 / 100** 회.
- **해체 후**: 글러브박스에서 꺼내 **DMC 로 여러 번 세척**, 실온 진공 건조.
- **연마**: pristine·사이클 전극 모두 EcoMet 3000 (Buehler), Al 홀더, 다이아몬드 3 → 1 µm (LECO) → **0.05 µm 콜로이달 실리카** → 경면;
  IPA 세척 후 **글러브박스로 반입** (*"delivered into glove box for nanoindentation"*).  ⚠ **연마 분위기는 미기재** (§8-5).
- **펠릿**: §3-8.

### 4-2. E · H 측정 — Oliver–Pharr (p. A3334, 식 1–3)
- **H = P_max / A(h_c)** (식 1) — A 는 접촉깊이 h_c 의 함수로 보정 (면적함수).
- **E_r = S·√π / (2β·√A)** (식 2) — S = 제하 초기 기울기, β = 압자 기하상수.
- **1/E_r = (1−ν²)/E + (1−ν_i²)/E_i** (식 3) — E_i 1141 GPa, ν_i 0.07 (Keysight 매뉴얼), **ν_NMC = 0.3 가정**.
- **targeted indentation** [28–31]: 광학으로 위치를 골라 **지름 > 10 µm 이차입자의 중심**에 찍는다 (압흔 < 1 µm, 기지와 충분히 멀리).
- 1 mN, 10 / 5 / 10 s, **배치당 입자 15개**, *"no detectable cracks"*, *"A series of additional tests … ensure the convergence"*.

### 4-3. K_c 측정 — cube-corner + pop-in 법 (p. A3334–A3335, 식 4–5)
- **cube-corner** (반정각 35.3°) 로 1차입자 사이에 **방사형 균열**을 낸다 — 날카로운 압자는 0.5–1.5 mN 급 저하중에서도 균열을 만든다 [35].
- **식 4 (LEM 형)**: **K_c = α · (E/H)^½ · (P / c^{3/2})**, α = **0.036** (cube-corner, [34] Nastasi 2012).
- 균열이 짧아 광학·SEM 으로 못 재므로 **식 5 (Field–Swain–Dukino 2003 [37])**: **c = √2·h_m + (Q·E′/H − √2)·h_x**,
  h_x = h_m − h_t (pop-in 으로 생긴 추가 침투), **Q = 4.55** (재료 무관 상수), E′ = 평면변형 탄성률.
- h_t (가상 무균열 곡선): **1–2 mN 저하중 곡선**(pop-in 없음)을 **2차 다항식**으로 맞춰 외삽 (p. A3335) — p. A3339 는 같은 것을
  *"following the Hertzian fitting procedure"* 라 적는다 (표현 불일치, §8-9).  **3–5 mN** 에서 pop-in 이 있는 곡선으로 h_x, h_m, c.
- **AFM 검증** (Veeco Dimension 3100, 스캔 3.35 µm, 0.5 Hz): 압흔 중심 → 균열끝 거리를 재 pop-in 값과 비교 —
  *"The AFM images give slightly smaller values presumably because of the invisible radial cracks beneath the surface"* (수치는 SI).
- 시료당 **15 압입**, **8–10 개**로 평균·SD.

### 4-4. 보조 분석
- **SEM** (JEOL T330): 입도 (이차 10 · 1차 1 µm), 연마 전후 형태 (Fig 3), 펠릿 표면·파단면 (Fig S3c, d).
- **XRD**: §3-8.

### 4-5. 제일원리 (p. A3335)
- **VASP** · **PAW** · **GGA-PBE** · **DFT+U** (U−J: **Ni 6.7 · Mn 4.2 · Co 4.91 eV**, [40] Zhou 2004) · **ENCUT 520 eV** ·
  **k = 2×1×1 Monkhorst–Pack** · 힘 수렴 **< 0.04 eV/Å**.
- 셀: **"R3m"** (인쇄본 그대로 — overbar 없음; Wyckoff Li 3b · O 6c · TM 3a 는 **R3̄m** 의 것) · 완전 리튬화 **120 원자**
  (= LiNi₀.₅Mn₀.₃Co₀.₂O₂ × 30).  탈리튬화 = **Li 를 무작위로 제거** (배열 1개로 읽힌다 — 앙상블·SQS 언급 없음).
- **E = x · y · z 세 방향 단축인장 응력-변형 곡선의 영률 평균** — 변형 크기·횡방향 이완 여부·자기 배열·TM 배치 **미기재**.
- 후처리: 응집에너지, **Bader 전하** (Fig 6b · S5), **전하밀도 차 맵** (Fig 6c; *"subtracting the charge density of pristine NMC from that
  of lithiated NMC"*, 원자 위치 고정), Ni–O 결합길이 분포 (S4), Li–O 결합·c 축 (S6), 분자궤도 도식 (S7).

### 4-6. ★ 입자 처리 (우리 DEM 의 "무질서 처리" 대응 항목) — **이 측정이 보는 "입자" 는 무엇인가**
- 측정 대상은 **이차입자 응집체 (hierarchical "meatball")** 의 **국소 부피** 다 — 1 mN Berkovich 의 압흔 한 변 ≈ **0.52 µm** (§3-9)
  ≈ 1차입자 ≈ 1 µm 이므로 **1차입자 1개와 그 입계들**이 탄성·소성장 안에 들어간다.
  ⇒ **단결정 값도, 이차입자 전체의 구조적 응답(압괴·입계 미끄럼 전체)도 아닌, "입계를 포함한 국소 응집체" 값.**
- 저자도 그렇게 해석한다: *"The size of the nanoindentation impression is around hundreds of nanometers which is comparable with the
  size of NMC primary particles. The mechanical response of NMC is largely influenced by the "grain boundaries"."* (p. A3337)
- 스케일 사다리 (이 카드의 핵심 틀):
  **DFT 결정 (190)  >  치밀 소결 펠릿 (177.5)  >  이차입자 국소 (142.5)  >  (이차입자 전체의 압축 응답 — 이 논문 밖)**.
  ⇒ DEM 에서 **입자 하나 = 이차입자 하나**인 강체구의 E 로는 **이차입자 국소값이 "올바른 부류"** 이지만, 입자 전체가 받는 접촉
  (접촉반경 ≫ 1차입자) 은 더 많은 입계를 거치므로 **실효 강성은 그보다 낮을 수 있다** — 이 논문은 그 칸을 재지 않았다.

---

## 5. Figure set ★ (본문 Fig 1–8 + Table 1 = 9장, **전부 크롭·육안 확인 2026-09-25**)

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig 1** (p. A3334) | 개념도: 사이클 → 손상 누적 (공동 STEM, Kim 2016 재인용) → **E·H 저하** → **입계 탈접착 (견인-분리 곡선: pristine 삼각형 vs cycled 축소)** → 입자 붕괴 → 새 표면에 저항층 → 임피던스 ↑ (막대 예시) → 성능 저하 | ★ **견인-분리(CZM) 삼각형이 사이클로 줄어드는 그림** = 우리 A10 `cycle_contact_ledger` 의 **poly 입계 CZM** 발상과 같은 그림.  단 그 그림의 값은 없다 (개념도) |
| **Fig 2** (p. A3335) | (a) 1·50·100번째 충방전 곡선 (C/5, 3–4.3 V) (b) 방전용량·쿨롱효율 vs 사이클 (Sample I 50 cyc, II 100 cyc) + 삽입 SEM (pristine / cycled, 10 µm) | 기계측정 시료의 **전기화학 이력** 증명서.  ⚠ 첫 CE 가 본문(84.3 %)과 그림(≈ 94 %)에서 다르다 (§8-3) |
| **Fig 3** (p. A3336) | SEM: (a) 연마 전 구형 이차입자 (b) 연마 후 평탄 단면 (*"Polished surface"*) (c) 압흔이 입자 중심에 찍힌 모습 + 삽입 하중-변위 (2 mN, ≈ 290 nm) | **압입 위치 규약** (입자 중심) 을 보는 그림.  ⚠ (c) 삽입 곡선은 2 mN 에서 ≈ 290 nm — Berkovich 라면 ≈ 100 nm 여야 하므로 **cube-corner 곡선으로 보인다** (캡션은 압자를 안 밝힘; 우리 추론) |
| **Fig 4** (p. A3337) | (a) 두 입자 (D ≈ 28 · 15 µm) 를 가로지르는 **E 선주사** (기지 → 입자 → 기지), 청색 점선 = 15입자 평균 (b) **CB+PVDF vs 페놀수지 기지** 에서 E·H 막대 + SEM 삽입 (c) **E vs 하중** (QS 막대 + CSM 연속선), 균열 급락 화살표, 삽입 = 최대하중 ≈ 1–10 mN 하중곡선 5개와 pop-in | ★★ **이 논문의 품질보증 그림** — 위치 (0.25 < y/D < 0.75) · 기지 · 하중 (< 2 mN) 세 교란을 따로 배제했다.  우리가 E_AM 을 인용할 때 **"어떤 조건의 값인가"** 의 근거.  (c) 는 **균열이 E 를 가짜로 낮춘다**는 경고 (10 mN 에서 ≈ 86 GPa) |
| **Fig 5** (p. A3338) | (a) **E·H vs SOC** (0/33/66/100 %) (b) **E·H vs 사이클** (0/1/30/50/100) — 좌축 E (40–160 GPa), 우축 H (5–15 GPa) | ★★★ **SOC·사이클 궤적** = 사이클 역학 모델의 입력 후보 (§9).  0 % 점 ≈ 145 GPa (Table 1 과 다름, §8-1) |
| **Fig 6** (p. A3339) | (a) **DFT E (190 → ≈ 150 GPa)** + 응집에너지 vs SOC + 결정 구조 삽입 (b) **Bader: O 는 덜 음전하 (−1.18 → −0.99), TM 은 더 양전하** (c) 전하밀도 차 맵 (0/33/66/100 % SOC, 0.004–0.02 e bohr⁻³) | 방향 재현 (선형 감소) 의 증거.  ⚠ 응집에너지 절대값 해석 불가 (§8-8) · 배열 1개 · k 2×1×1 |
| **Fig 7** (p. A3340) | (a) 균열 모식: 1차입자 경계 (점선), **방사형 균열이 입계를 따라 꺾임**, 측면(lateral) 균열 + 칩 탈락; 삽입 AFM (1 µm 척도, c 표시) (b) **pop-in 하중곡선** — P = 3 mN 에서 h_t · h_m · h_x 정의 + 식 5 | ★ **K_c 가 "입계 인성" 인 이유** (균열이 입계로 간다).  (b) 로 우리가 K_c 를 **재계산**했다 (§6-3): c ≈ 3.1 µm → K_c ≈ 0.082 (보고 밴드 안) |
| **Fig 8** (p. A3340) | **K_c vs SOC** (a) · **vs 사이클** (b), 0–0.15 MPa·m^½ | ★★★ 우리 **K_IC_P = 0.3** 과 나란히 볼 그림 — 이차입자 계면값은 **0.10 에서 시작해 0.036 까지** 내려간다 |
| **Table 1** (p. A3337) | 이차입자 vs 소결 펠릿 vs 제일원리의 **E · H · K_c** | ★★★ **원고 각주의 근거 표** (§3-1).  원문 표기 "Table I" (로마 숫자) |

**크롭 방법** (재현용): `tools/litdb/extract_figures.py` 자동 크롭 = Fig 2–8 (캡션 앵커, 쪽 여백 포함·내용 완전).
**Fig 1** = 캡션이 **그림 오른쪽 옆**이라 자동 크로퍼가 *"그래픽 없음"* 으로 제외 → 임베디드 래스터 경계 (35, 67, 323, 329) pt @300 dpi 수동.
**Table 1** = 로마 숫자 라벨 (도구는 아라비아 숫자만) → PDF 6쪽 (35, 648, 285, 758) pt @300 dpi 벡터 렌더 수동.
⚠ `--slug xu2017_… --clean` 을 다시 돌리면 **Fig 1 · Table 1 이 사라진다** (`pdf_map.tsv` 주석 참조).

---

## 6. Post-processing ★ (그들이 한 것 + 우리가 한 것)

### 6-1. 그들의 수치화
- **E · H**: 식 1–3 (Oliver–Pharr), 배치당 15입자의 평균 ± (정의 미기재).  하중 의존은 QS (단일 하중) + **CSM** (연속강성, 진동 하중) 병행.
- **K_c**: 식 4–5.  E′·H 는 **앞 측정값을 대입** — 즉 **K_c 는 E/H 측정 오차를 물려받는다**.  15 중 8–10 개 사용.
- **AFM**: pop-in c 의 검증 (정량 비교는 SI Fig S2).
- **DFT**: 세 방향 단축인장 E 평균 · 응집에너지 · Bader · 전하밀도 차.
- 플롯: Origin 풍 (좌 E / 우 H 이중축), 점선 연결, 막대 = ±.

### 6-2. 우리의 디지타이즈 절차 (재현용)
1. PDF 임베디드 래스터를 원해상도로 추출 (Fig 5: 1954×664 px, Fig 8: 1800×687, Fig 4: 1975×1756, Fig 6: 1971×1188).
2. 축 테두리 = 긴 검정/청색 선, 눈금 = 축 안쪽 짧은 선을 **픽셀로 자동 검출** → 선형 보정.
3. 마커 중심 = 11×11 px 사각 템플릿의 최대 채움 위치; 오차막대 끝 = 마커 열의 연속 픽셀 주사 (회색 막대는 완화 임계값).
4. **검증**: stated 끝점을 재현 — SOC100 **111.61 / 7.10** (stated 111.6 / 7.1), 100 cyc **107.23 / 6.46** (107.3 / 6.5),
   K_c **0.1022 / 0.0357** (0.102 / 0.036), DFT 0 % **189.8** (190.0).  ⇒ 중심값 정확도 ≈ **±0.5 GPa · ±0.05 GPa · ±0.001 MPa·m^½**.
   ⚠ **오차막대는 덜 믿을 것** — Fig 5b · 8b 의 0 · 1 사이클 막대가 겹친다 (확대 판독으로 보정).

### 6-3. ★ K_c 재계산 (Fig 7b, 우리 산술 — 방법 민감도)
- Fig 7b 판독: **P = 3 mN · h_t ≈ 337.6 nm · h_m ≈ 368.8 nm → h_x ≈ 31.2 nm**.
- E′ = E/(1−ν²) = 142.5/0.91 = 156.6 GPa, H = 8.6 → **Q·E′/H ≈ 82.8** → 식 5 의 h_x 계수 **≈ 81.4**.
- **c ≈ 3.06 µm → K_c ≈ 0.082 MPa·m^½** (식 4, α 0.036) — 보고값 0.102 ± 0.03 의 **밴드 안**. ✅ 논문 내부 정합.
- ★ **민감도**: h_x 가 ±10 nm 틀리면 c 가 ±0.8 µm, **K_c 가 −30 % / +59 %**.  **K_c 는 사실상 pop-in 길이 h_x 하나로 정해진다**
  (c ≈ 3.06 µm 중 ≈ 83 % 가 h_x 항).
- 대조: Fig 7a 삽입 AFM 의 c 는 척도(1 µm) 로 **≈ 1.1 µm** 로 보인다 — 같은 3 mN 이라면 K_c ≈ **0.38** 이 된다.  **그러나 그 압흔의
  하중은 미기재이고 두 패널이 같은 압흔이라는 말도 없다** ⇒ 모순이라 단정하지 않는다.  남는 결론은 하나: **K_c ≈ 0.1 은 방법
  (pop-in 추정 c) 조건부 값이고, 수 배 불확도를 안고 있다.**

### 6-4. G_c 환산 (DERIVED, 평면변형 G = K²(1−ν²)/E, ν = 0.3 — 논문 가정과 같게)

| 상태 | K_c | E | **G_c (J m⁻²)** |
|---|---|---|---|
| 이차입자 pristine | 0.102 | 142.5 | **≈ 0.066** |
| 이차입자 SOC 100 % | ≈ 0.058 | 111.6 | ≈ 0.027 |
| 이차입자 100 cyc | 0.036 | 107.3 | ≈ 0.011 |
| 소결 펠릿 | 0.309 | 177.5 | **≈ 0.49** |
| (우리) K_IC_P 0.3 · E 140 · ν 0.25 | 0.3 | 140 | ≈ 0.60 |
| (우리) K_IC_S 1.0 · E 140 · ν 0.25 | 1.0 | 140 | ≈ 6.7 |

- 참고: 황화물 SE 의 G_c 앵커 **2.8 ± 1.8 J m⁻²** (`bucci2017_chemomech_failure_assb_cycling_czm`, McGrogan 유리 LPS) 는
  **NMC 이차입자 입계의 ≈ 42 배**.  ⇒ **이차입자 내부 입계가 계면망에서 가장 약한 고리 후보**라는 것이 숫자로 선다
  (단 방법이 다른 두 값의 비 — 자릿수 수준으로만).

---

## 7. 우리 DEM+MPM 대비 ★  (기준 = 작업 브랜치 `claude/stoic-knuth-NObVQ` 코드, 2026-09-25 확인 — `our_dem_baseline.md` 는 아직 자리표시)

| 항목 | 이 논문 | 우리 | 같은 점 / 다른 점 / 왜 |
|---|---|---|---|
| **AM 조성** | NMC532 | NCM811 (생산) | ⛔ **다르다.**  Ni ↑ 에 따른 E 변화는 이 논문 밖.  조성 일치 = 짝 카드 `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` (다결정 NMC811 나노압입 E 138 ± 24 GPa, n = 29, ν 0.32 가정 — 그 카드의 기록) |
| **E_AM** | 이차입자 **142.5 ± 11.3** (pristine) · 펠릿 177.5 · DFT 190 | **140 GPa** (`dem_input_values.py` E_AM_PA 1.40e11, `fracture_model.py` E_AM, LIGGGHTS AM 1.4e8 sim 단위) | ✅ **수치 정합 (−0.22 SD)** — 우리 값은 **이차입자 응집체 부류**다.  ⚠ 140 이라는 숫자는 이 논문에 없다 = **"정합" 이지 "출처" 가 아니다** |
| **ν_AM** | **0.3 가정** (측정 아님) | **0.25** (`dem_input_values.py`, `fracture_model.py` NU_AM, *"ceramic"*) | ⛔ 작업 브랜치 `docs/Reviewer_Defence_Notes.md:114` 의 *"ν ≈ 0.25 표준 (Xu 2017)"* 은 **오귀속**.  E 환산 감도: 같은 E_r 에서 ν 0.25 로 풀면 E = **146.8** (+3.0 %) |
| **H_AM** | 이차입자 **8.6 ± 1.3** (pristine) · SOC100 7.1 · 100cyc 6.5 · 펠릿 12.6 | **6.0 GPa** (`fracture_model.py` H_AM *"source unverified (SELF-51)"*; `analyze_tabor_regime.py` σ_y = H/3 = 2.0 GPa) | ⛔ **pristine 대비 −2.0 SD** — 이 논문으로 6.0 을 뒷받침할 수 없다.  6.0 은 **열화 상태 값에 가깝다** |
| **H 문헌대 (am_load_balance_jam)** | — | *"NCM811 압입 경도 문헌대 ≈ 3~6 GPa"* (`am_load_balance_jam.py:28`, 사전등록 PASS 기준 `run_cases(band=(3.0, 6.0))`) · 역산 **H_AM 3.83 GPa** (real_14) | ⚠ **그 밴드에 출처가 없고**, 리포 유일의 NMC 나노압입 원문(이 논문, 532)의 pristine 8.6 은 **밴드 상단보다 2 SD 위**다.  3.83 은 이 논문 pristine H 의 **0.45×**.  ⚠ 그러나 **스케일이 다르다** — 이 논문 H 는 **sub-µm 국소값**(h_c ≈ 69 nm), 그 식의 H_AM 은 **플래튼–AM 크라운 접촉압**(입자 스케일) — 나노 H 는 그 상한 쪽 (§9-3) |
| **K_IC (이차입자 = AM_P)** | **0.102 ± 0.03** (계면, pristine) → 0.058 (SOC100) → 0.036 (100cyc) | **K_IC_AM_P = 0.3** (`fracture_model.py`, *"polycryst secondary NCM, Quinn 2020"* — 출처 미확인) | ⚠ **0.3 은 이 논문의 치밀 펠릿 (0.309 ± 0.04) 과 같은 값**이고 **이차입자 (0.102) 의 2.9배** (6.6 SD).  이 논문 기준이면 우리 AM_P 는 **너무 질기게** 잡혀 있다 |
| **K_IC (단결정 = AM_S)** | 측정 없음.  *"intrinsic … should be higher than … pellets"* (> 0.309) + LiCoO₂ 0.9 ± 0.1 (타 산화물, [31]) | **K_IC_AM_S = 1.0** (*"Liu 2020"* — 출처 미확인) | ⚠ 이 논문은 **하한 (> 0.31) 과 방향만** 준다.  1.0 의 앵커가 **아니다** |
| **E 의 SOC·사이클 의존** | E −22 % (SOC100) · −25 % (100 cyc); K_c −43 % · −65 % | 고정 (생산 = 압밀 = pristine 상태) | ✅ **압밀 시뮬엔 pristine 값이 맞다** (분말은 방전 상태).  사이클 모델 (A10) 에서만 의미 |
| **입자 처리** | 응집체 **국소** 부피 (≈ 1 개 1차입자 + 입계) | **강체 구 = 이차입자 1개**, hooke/hysteresis **접촉** 소성 (형상 불변) | 이 논문은 DEM 입자 한 개가 **무엇으로 이루어졌는지**(1차입자 + 약한 계면) 를 보여 준다 — 우리 DEM 은 그 안을 **점 하나**로 본다 (축 G) |
| **전해질** | **액체** (LiPF₆ EC/DEC) 반쪽셀 · DMC 세척 | **황화물 LPSCl ASSB** | ⛔ **사이클 열화 값의 전이 금지** — 액체는 입계로 **침투**한다 (황화물은 못 한다). §8-10 |
| **"AM–SE 강성 대비"** | H_NMC 8.6 vs (우리) H_SE 0.85 | 이 비 ≈ **10** | 우리 *"AM = 강체, SE 가 변형"* 비대칭 처리의 크기 근거 (방향은 이미 `martinbouvard2003_…` 등) |

### 7-1. E_AM = 140 GPa — **정합한다, 단 "출처" 로는 한정어가 붙는다**
- 이 논문의 pristine **NMC532 이차입자 142.5 ± 11.3 GPa** 는 우리 140 과 **−0.22 SD** — 차이가 측정 산포 안이다.
- 더 중요한 것은 **부류**다: 같은 논문 안에서 **이차입자 142.5 ↔ 치밀 펠릿 177.5 ↔ DFT 190** 이 갈린다 (1 : 1.25 : 1.33).
  ⇒ 우리 140 은 **"입계를 포함한 응집체"** 부류이고, `kang2025_toughened_bimodal_nca_lzo` 의 **E_NCA 175 (가정)** 는 **"치밀 결정"** 부류다.
  `docs/nca_material_preset.md` 의 *"140 vs 175 = 출처-방법 artifact"* 판정은 **이 논문 한 편 안의 대조로 직접 뒷받침된다** (같은 분말,
  같은 장비, 같은 조건에서 부류만 바뀌어 1.25×).
- LIB 제조-DEM 계보의 **"142 GPa"** (Sangrós 2019 · Lyu 2025 · Lippke 2023) 중 **Sangrós 2020 은 이 논문을 [32] 로 인용해
  142.5 → 111.6 을 그대로 쓴다** (`sangros2020_lib_electrode_dem_mech_elec_ionic` 카드 3절) — 나머지 셋의 142 가 같은 뿌리인지는
  각 원문의 참고문헌 확인 전까지 **추정**이다.
- ⛔ **"Xu 2017, NCM811 nanoindentation"** 표기(작업 브랜치 `docs/paper_brittle_caveat.md:163 · :327`)는 조성이 틀렸다 — **NMC532** 로 고칠 것.

### 7-2. H_AM = 6.0 GPa — **이 논문은 6.0 을 주지 않는다**
- pristine **8.6 ± 1.3** (Berkovich, 1 mN) — 6.0 은 −2.0 SD.
- 6.0 에 가까운 것은 **100 사이클 후 6.5 ± 0.9** 와 **SOC100 7.1 ± 0.8** — 둘 다 **열화·탈리튬화 상태**라 압밀(pristine) 의 앵커가 아니다.
- Vickers ↔ 나노압입 환산: 이상 기하에서 H_V ≈ **0.927 × H_IT** (투영면적 ↔ 표면적) → 8.6 은 H_V ≈ **8.0** — 여전히 6.0 이 아니다.
- `build_literature_reference.py` 의 **H_NCM 5.0–8.0 GPa** 범위도, **E_NCM811 130–165 GPa (*"Xu 2017 … range unverified"*)** 범위도
  **이 논문에 적힌 범위가 아니다**.  이 논문이 주는 것은 **142.5 ± 11.3** (±1 SD → 131–154) 과 Fig 4a 개별 압입의 판독 산포
  (≈ 126–165) 뿐이다.
- **독립 교차확인**: 짝 카드 [Sedl26] §7.5 가 같은 결론에 먼저 닿았다 — 그 논문이 인용한 NMC 경도 **7.8 · 8.9 · 8.6 GPa** (NMC532 이차입자;
  8.6 이 **이 논문**, 7.8 · 8.9 는 같은 Zhao 그룹의 de Vasconcelos 2019 *Exp. Mech.* · 2016 *EML*) 와 **14.2** (NMC811 펠릿, Sharma 2023) 가
  우리 "3–6 GPa" 와 **하나도 안 겹친다**.  이 카드는 그중 8.6 의 **원문 조건**(Berkovich · 1 mN · 15입자 · ν 0.3 가정) 을 확정한다.

### 7-3. K_IC — **이 논문은 우리 값과 "다른 쪽" 을 가리킨다**
- **K_IC_AM_P (다결정 이차입자)** 의 직접 대응물은 이 논문의 **이차입자 계면 K_c = 0.102** 다 — 방사형 균열이 **입계를 따라** 가는 것을
  본문이 보였다 (Fig 7a).  우리 0.3 은 이 논문의 **치밀 펠릿 (결정립 10 µm)** 값과 같다.
- 우리 모델에서의 크기 (DERIVED, `fracture_model.py` 식 그대로): **P_c = A·K_IC²·R/E\*** 이므로
  **K_IC_P 0.3 → 0.102 이면 P_c × 0.116 (개시 하중 1/8.7)**, δ_c × 0.237.  100 사이클 값(0.036) 이면 P_c × 0.014 (1/69).
  E·ν 를 이 논문 값(142.5 · 0.3)으로 바꾸는 효과는 P_c × 0.954 · δ_c × 0.939 — **K_IC 에 비하면 무시할 만하다**.
- 같은 그룹 · 같은 pop-in 법의 **NMC811 값 0.271 MPa·m^½** (Sharma 2023 — [Sedl26] 의 [23]; 펠릿인지 단결정인지 [Sedl26] 도 판정 불가, **미보유**) 까지
  나란히 두면: **우리 0.3 = "치밀체 급" 0.27–0.31** (이 논문 펠릿 0.309 · Sharma 0.271) 이고 **이차입자 입계 급 0.10 이 아니다**.
  ⇒ 다음에 확보할 원문 = **Sharma 2023** (K_IC_S 1.0 · K_IC_P 0.3 둘 다의 판정 재료).
- ⚠ **이 변경은 소리 없이 하면 안 된다** — `run_network_fracture_aware.py` 가 `fracture_classify_force_sim` · `k_ic_for_pair` 로 만든
  **`fracture_aware_excluded_pct` (σ_ionic T1 의 β_F·log f_intact)** 와 **`frac_severe_force_pct` (σ_e 22.5 의 β_Fe)** 가 전부 이 P_c 에
  걸려 있다 ⇒ 바꾸면 **분류 재실행 + 두 폼 재적합**이 필요하다 = **1저자 결정 사항**.
- 게다가 이 논문의 K_c 도 **방법 조건부**다 (§6-3: h_x ±10 nm → −30 / +59 %, 15 중 8–10 사용, AFM 대조는 SI).  그리고 **파괴 모드가 다르다** —
  Auerbach 는 **헤르츠 원뿔균열** (구–구 접촉), 이 논문은 **예리한 압자의 방사형 균열**.  공통점은 **둘 다 다결정 응집체에서는 입계로
  간다**는 것뿐이다.

### 7-4. frame [5] 로 본 자리
- 이 논문은 **DEM 도 MPM 도 아니다** — 우리 두 모델의 **재료 입력** 원전이다.
  · DEM 쪽: AM 접촉법칙의 **E·ν** (강체에 가까운 쪽이라 압밀엔 영향이 작다) + 파괴 분류의 **K_IC** (영향이 크다, §7-3).
  · MPM 쪽: AM 은 얼린 scaffold 라 **E_AM 을 쓰지 않는다** — 영향 0.
  · 사이클 (A10): **E·H·K_c(N)** 궤적이 **poly 입계 열화의 형태 앵커 후보** (§9-4).
- 이 논문이 **가진 반쪽**: 입자 한 개의 **재료값과 그 열화**.  **없는 반쪽**: 그 입자들이 모인 **전극** (접촉망 · 압밀 · 수송) — 전부 우리 쪽.

---

## 8. ★★ 비판적 검토 — 원고에 옮기기 전 확인할 것 (내부 불일치 목록)

1. **pristine 값이 두 벌이다** — Table 1 · p. A3336 · Fig 4b = **142.5 / 8.6**, Fig 5 의 0 % · 0 사이클 점 = **≈ 145.1 / 8.9** (판독),
   Fig 4a 본문 *"about 145"* (그러나 점선 판독 ≈ 141.6).  저자 비율 (77/80 %, 74/73 %) 은 **145/8.9 기준**으로 계산된 것으로 읽힌다 (§3-2, 3-3).
   둘 다 1 SD 안이라 **결론은 안 바뀐다**.  ⇒ **인용은 stated 142.5 ± 11.3 / 8.6 ± 1.3**, 비율은 Table 1 기준으로 다시 적을 것
   (E 78 %, H 83 % at SOC100 · 75 %, 76 % at 100 cyc).
2. **기지 "< 15 GPa"** (p. A3336) ↔ Fig 4a 기지 점 **≈ 6–44 GPa** (판독) — 절반 가량이 15 를 넘는다.  CB+PVDF 기지 자체는 1.78 ± 0.35 (Fig 4b) 이므로
   선주사의 기지 점은 **이웃 입자의 영향**을 받은 것으로 보인다.  결론(입자 중심은 수렴) 엔 영향 없음.
3. **쿨롱효율 세 값** — 본문 *"initial cycle 84.3%"* ↔ Fig 2b 첫 점 **≈ 94 %** ↔ Fig 2a 1번째 사이클 (충전 ≈ 164 / 방전 160.5) **≈ 98 %**.
   84.3 % 는 **그림에 없는 C/20 형성 사이클**일 가능성이 가장 크다 (미기재).
4. **"SOC 100 % = Li₀.₅"** — 측정이 아니라 **저자 표기**.  Fig 2a (C/5) 4.3 V 충전용량 ≈ **164 mAh g⁻¹** ÷ 이론 **277.6 mAh g⁻¹**
   (LiNi₀.₅Mn₀.₃Co₀.₂O₂, M = 96.55 g mol⁻¹) → Δx ≈ 0.59 → **Li ≈ 0.41** (우리 산술).  SOC 배치는 **C/20** 이라 더 뽑혔을 수 있다 ⇒
   **실제 Li 함량 ≤ ~0.41** (0.5 아님).  Fig 5a·6a·8a 의 x 축은 "Li₀.₅" 가 아니라 **"4.3 V 충전 끝"** 으로 읽을 것.
5. **연마 분위기 미기재** — 0.05 µm **콜로이달 실리카**(보통 수계) + IPA 세척 후 *"delivered into glove box"*.  **측정만 불활성**이고
   **준비는 대기·수분 노출 가능성**이 있다 (명시 없음).  탈리튬화·사이클 시료에서 특히 교란 후보.
6. **K_c 선별** — 15 압입 중 **8–10 개** 사용, 제외 기준 = *"erroneous load-displacement curves"* (정의 없음) ⇒ **선택 편향 가능**.
7. **XRD 로 "원소 조성 동일" 을 확인했다** (*"The similar XRD patterns confirm that the sintered NMC pellet has same elemental composition"*) —
   **XRD 는 원소 조성을 확인하지 못한다** (상·구조만).  1000 °C 10 h 소결의 **Li 휘발 · 양이온 혼합** 가능성이 배제되지 않았다 ⇒ 펠릿
   177.5 / 12.6 / 0.309 를 **"같은 조성의 치밀체"** 로 쓰는 데 한정어가 필요.  펠릿 **밀도도 미보고** (§3-1).
8. **응집에너지 0.3–0.8 eV/atom** — 정의 (*"break the lattice into isolated free atoms"*) 와 **자릿수가 안 맞는다** (층상 산화물은 수 eV/atom).
   다른 기준을 뺀 값일 가능성 — **절대값 인용 금지**, 추세만.
9. **h_t 맞춤 방식 두 표현** — p. A3335 *"second-order polynomial"* ↔ p. A3339 *"following the Hertzian fitting procedure"*.  K_c 가 h_x 에
   극도로 민감하므로 (§6-3) **어느 쪽이었는지가 결과를 바꾼다**.
10. **액체 전해질 교란** — pristine (0 점) 은 전해질에 **안 닿았고**, 1 사이클 점부터는 **담그고 · 세척하고 · 말린** 시료다.  **"담그기만 한"
    대조군이 없다** ⇒ 첫 사이클 계단 (E −13.5 %) 에 **전해질 침투·세척 효과**가 섞였을 수 있다.  저자는 결정성 손실 [12] 로 설명.
    황화물 ASSB 에선 전해질이 입계로 못 들어가므로 (`trevisanello2021_sc_pc_ncm_cracking_diffusion` 계열 논의) **사이클 열화 크기를 옮기지 말 것**.
11. **입경 ↔ 인성 논거의 출처** — *"A larger grain size … decreases the material toughness"* 에 단 [45, 46] 은 **암석역학** 논문 (Rock Mech. Rock Eng.,
    Int. J. Rock Mech.) 이다 — 유비이지 NMC 측정이 아니다.  저자도 *"We expect …"* 로 적었다.
12. **DFT 한계** — 배열 1개 (무작위 Li 제거), k 2×1×1, 방향 영률 평균 (다결정 Hill 평균 아님), 자기·TM 배치 미기재.
    E_DFT 190 은 **자릿수·방향 확인용**이지 정밀 앵커가 아니다.
13. **Jahn–Teller 논거의 적용 범위** — Ni²⁺ (JT 비활성) → Ni³⁺ (활성) 은 더 탈리튬화하면 Ni⁴⁺ (비활성) 로 간다.  JT 를 연화의 원인으로
    드는 설명은 **이 창 (≤ 4.3 V)** 안에서만 성립 — 외삽 금지 (우리 판단).

---

## 9. 적용 인사이트 — 우리 연구에 어떻게

1. **E_AM 140 의 인용 문장을 바꾼다** — "Xu 2017 (NCM811)" 이 아니라 *"consistent with nanoindentation of pristine polycrystalline NMC532
   secondary particles, 142.5 ± 11.3 GPa [Xu 2017]"*.  NCM811 조성 일치 값은 짝 카드 [Sedl26] (**138 ± 24 GPa, n = 29**) 로 —
   두 원문을 나란히 적으면 (**532: 142.5 ± 11.3 · 811: 138 ± 24**) **응집체 수준에서 조성 차가 산포 안**이라는 것까지 한 문장에 들어간다.
2. **"응집체 vs 치밀체" 스케일 사다리를 원고의 한 문장으로** — 같은 논문 안에서 142.5 : 177.5 : 190 = **1 : 1.25 : 1.33**.
   ⇒ *"우리 E_AM 은 응집체 부류, NCA 175 (가정) 는 치밀 결정 부류"* 가 **재료 차이가 아니라 측정 부류 차이**임을 보이는 최단 근거.
3. **H_AM 과 "3–6 GPa 문헌대" 를 재정의해야 한다** — (a) 6.0 은 이 논문으로 못 댄다 (b) `am_load_balance_jam` 의 사전등록 밴드 3–6 GPa 는
   출처가 없고 이 논문 pristine 8.6 과 안 맞는다 (c) 그런데 그 식의 H_AM 은 **입자 스케일 접촉압**이라 나노 H 는 **상한 쪽 양**이다
   (입자 압축 "경도" 는 전혀 다른 양 — `jung2023_single_crystal_ncm_morphology` 의 PC 113 MPa / SC 973 MPa 는 **micro-compression 피크 응력**).
   ⇒ 권고: 밴드를 **"나노압입 H (8.6 ± 1.3, NMC532) 가 상한, 입자 압축 강도가 하한"** 인 **스케일 명시 구간**으로 다시 등록하거나,
   밴드 판정을 빼고 역산값을 **서술**로만 보고한다.  (⚠ 그 문서가 이미 밝혔듯 두께 검정은 H_AM 0.75–40 GPa 에서 전부 PASS 인 **공허한 검정**이라
   실질 영향은 **서지·해석 층**에 있다.)
4. **K_IC_P 는 0.3 과 0.1 사이의 "결정 사항" 이다** — 이 논문은 이차입자 계면값 0.10 (pristine) 을 준다.  바꾸면 AM_P–AM_P 개시 하중이
   1/8.7 로 내려가 **f_intact 와 σ 폼 두 개가 흔들린다** (§7-3).  권고: 생산값은 그대로 두고, **K_IC_P ∈ {0.10, 0.30} 두 팔 민감도**를
   먼저 등록·실행해 `fracture_aware_excluded_pct` 가 얼마나 움직이는지 본다 (수치 비교는 같은 코퍼스·같은 분류기에서만).
5. **A10 사이클 역학의 "형태" 앵커 후보** — `cycle_contact_ledger --poly-mode expand-void` 의 poly 입계 열화는 **ASSUMED-FORM · 앵커 대기**다.
   이 논문은 **첫 사이클 급락 + 이후 완만한 단조 감소** (E·H 25 %, K_c 65 % / 100 cyc) 라는 **형태**를 준다.  ⚠ **액체 반쪽셀 · NMC532 · C/5** 라
   **크기는 옮기지 않는다** — "형태 (첫 사이클 계단 + 로그형 감쇠)" 만.
6. **G_c 서열이 계면망의 약한 고리를 가리킨다** — NMC 입계 ≈ 0.07 J m⁻² ≪ 치밀 NMC ≈ 0.5 ≪ 황화물 SE ≈ 2.8 (다른 방법, 자릿수만).
   AM–SE 계면 CZM 을 SE 의 G_c 로 두고 있다면, **이차입자 내부 입계는 그보다 한 자릿수 이상 약하다**는 것을 해석에 병기.
7. **AM_S (단결정) 는 다른 E 부류일 수 있다** — 입계가 없으므로 치밀·결정 부류 (177–190, 532 기준) 쪽일 가능성.  압밀에선 AM 이 SE 대비
   강체라 영향이 작지만 (Martin–Bouvard: 경질상 E 10↔100 에서 < 3 %), **P_c ∝ 1/E\*** 인 파괴 분류엔 작게 들어간다 — 2차 정정 후보.

---

## 10. 한계

### 10-1. 저자가 밝힌 것
- 입계 나노기공은 합성 유래로 존재할 수 있고 그 영향은 결과에 **포함돼 있다** (*"embedded in the experimental results"*).
- 사이클 초기의 미세구조 변화는 *"to be explored in future studies"*.
- 결정립(1차입자) 크기 의존은 *"interesting to systematically study … in future work"*.
- 미세구조 손상만으로는 사이클 후 기계물성 저하를 다 설명 못 할 수 있다 — **양이온 혼합** 등 원자구조 요인 [26].

### 10-2. 우리가 추가하는 것 (논문이 말하지 않은 것)
- **조성 1개 (NMC532)** · **분말 1종 (MTI)** · **압력 이력 1종 (상용 전극, 캘린더링 정보 없음)**.
- **액체 전해질** 이력 · **담그기 대조군 없음** · **연마 분위기 미기재** (§8-5, 8-10).
- **± 정의 미기재 (E·H)** · **K_c 선별 (8–10/15)** · **펠릿 밀도 미보고**.
- **스케일**: sub-µm 국소값 — 이차입자 **전체**의 접촉 강성·압괴강도가 아니다 (§4-6).
- **단결정 데이터 없음** — 우리 AM_S 에 대응하는 값이 없다.
- **SI 미보유** — AFM ↔ pop-in 정량 비교, 입자 vs 펠릿 하중곡선을 못 봤다.

---

## 11. 기법 미니 용어집

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **Oliver–Pharr (O–P)** | 제하 곡선 초기 기울기 S 와 면적함수 A(h_c) 로 E_r · H 를 뽑는 표준 해석 | E·H 전부 (식 1–3) |
| **환산탄성률 E_r** | 압자·시료 두 탄성체를 직렬로 본 유효 탄성률, 1/E_r = (1−ν²)/E + (1−ν_i²)/E_i | ν = 0.3 가정 → E |
| **Berkovich / cube-corner** | 삼각뿔 압자.  Berkovich 반정각 65.3° (A ≈ 24.5 h²) · cube-corner 35.3° (A ≈ 2.6 h², 날카로워 저하중 균열) | E·H 는 Berkovich, K_c 는 cube-corner |
| **QS / CSM** | 준정적 단일하중 / 작은 진동을 얹어 깊이별 강성을 연속 측정 | 하중 의존 (Fig 4c) — CSM 급락 = 균열 |
| **pop-in** | 하중 곡선에서 침투가 갑자기 늘어나는 사건 — 여기선 **방사형 균열 형성** | h_x = h_m − h_t |
| **Field–Swain–Dukino (2003) 법** | pop-in 길이로 균열길이 c 를 추정: c = √2·h_m + (Q·E′/H − √2)·h_x, Q = 4.55 | 균열을 직접 못 볼 때 (식 5) |
| **LEM 형 K_c 식** | K_c = α (E/H)^½ P / c^{3/2} — 반원형(half-penny) 방사균열 가정 | α 0.036 (식 4) |
| **평면변형 탄성률 E′** | E/(1−ν²) | 식 5 |
| **targeted indentation** | 광학 위치선정으로 이종 복합체의 **한 상** 에만 찍기 | 이차입자 중심 |
| **ISE (압입 크기 효과)** | 얕을수록 H 가 커지는 경향 — 나노 H 가 마이크로 Vickers 보다 큰 이유 중 하나 | 1 mN (h_c ≈ 69 nm) |
| **H_V ↔ H_IT** | 이상 기하에서 Vickers(표면적 기준) ≈ 0.927 × 투영면적 기준 H | §7-2 환산 |
| **G_c = K²(1−ν²)/E** | 평면변형 LEFM 에서 인성 ↔ 파괴에너지 | §6-4 |
| **Auerbach 법칙** | 구–평면 헤르츠 원뿔균열 개시 하중 P_c ∝ K_IC² R / E\* | 우리 `fracture_model.py` (이 논문 아님) |
| **Bader 전하** | 전하밀도의 영점 흐름면으로 원자 부피를 나눠 원자 전하를 정의 | Fig 6b |
| **Jahn–Teller (JT)** | 축퇴 전자배치 (Ni³⁺ 저스핀 d⁷ 등) 가 팔면체를 늘여 에너지를 낮추는 왜곡 | 탈리튬화 연화 설명 |
| **"meatball" 이차입자** | 서브µm 1차입자가 반데르발스로 뭉친 수십 µm 응집체 (저자 표현) | 측정 대상 |

---

## 12. 인용 가능 문장 (deck / 원고용)

- **E_AM (원고 SI 표 · Methods)**:
  *"E_AM = 140 GPa (project convention for NCM811) is consistent with nanoindentation of pristine polycrystalline NMC532 secondary particles,
  142.5 ± 11.3 GPa (Berkovich, 1 mN, Oliver–Pharr, ν = 0.3 assumed; Xu et al., J. Electrochem. Soc. 164, A3333 (2017)); dense sintered NMC532
  pellets and first-principles give 177.5 ± 19.5 and 190.0 GPa, respectively, i.e. our value belongs to the aggregate (secondary-particle) class."*
- 한국어: *"E_AM = 140 GPa 는 pristine 다결정 NMC532 이차입자의 나노압입값 142.5 ± 11.3 GPa (Xu 2017, JES) 와 정합하며, 같은 논문의 치밀 소결체
  177.5 · 제일원리 190 GPa 와 비교하면 입계를 포함한 응집체 부류의 값이다 (조성은 NMC532)."*
- **K_c (파괴 모델 한계 서술)**:
  *"Indentation measurements on NMC532 secondary particles give an interfacial (intergranular) fracture toughness of 0.102 ± 0.03 MPa m^1/2,
  about one third of dense sintered pellets (0.309 ± 0.04), decreasing to ~0.06 at 4.3 V and 0.036 ± 0.018 after 100 cycles in liquid half-cells
  (Xu et al. 2017)."*
- **SOC 의존 (사이클 모델 서론)**:
  *"Delithiation to 4.3 V lowers the modulus and hardness of NMC532 secondary particles from 142.5 ± 11.3 / 8.6 ± 1.3 to 111.6 ± 6.4 / 7.1 ± 0.8 GPa
  (Xu et al. 2017)."*  (⚠ "Li₀.₅" 대신 "4.3 V" 로 적는다 — §8-4)
- ⛔ **쓰면 안 되는 문장**: "Xu 2017 measured NCM811" · "H_NCM = 6 GPa (Xu 2017)" · "ν = 0.25 (Xu 2017)" · "K_IC = 0.3 for secondary particles (Xu 2017)" ·
  "Phys. Rev. X 7, 041038" · 응집에너지 절대값 인용.

---

## 13. 관련 카드 (litdb 내부 교차참조)

- ★ `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` — **짝 카드 (SELF-51)**: 다결정 **NMC811** 입계 강도 745 MPa · 나노압입 E 138 ± 24 GPa (n = 29) ·
  인용 경도 7.8 / 8.9 / **8.6 (= 이 논문)** / 14.2 · K 0.271 (Sharma 2023 차용).  이 카드가 그 인용 [29] 의 **원문**이다.
- `sangros2020_lib_electrode_dem_mech_elec_ionic` — **이 논문을 [32] 로 인용해 E_NMC 142.5 → 111.6** 을 DEM 입력으로 쓴 선례.
- `sangros2019_dem_calendering_lib_electrode` · `lyu2025_3d_dem_drying_calendering_lib` · `lippke2023_dem_drying_structure_formation_lib` — "142 GPa" 계보 (뿌리 추정).
- `kang2025_toughened_bimodal_nca_lzo` — E_NCA **175 (가정)** = 치밀 결정 부류 (§7-1).
- `so2022_dem_compaction_coated_particles_assb` — NCM **E 199 · H 11.2 GPa** (Cheng [37]) — 이 논문의 [27] Cheng 2017 과 같은 원전일 가능성 (**미확인**); 부류상 **펠릿** 쪽.
- `jung2023_single_crystal_ncm_morphology` — **입자 압축 "경도"** SC 973 / PC 113 MPa = **다른 양** (§9-3).
- `intergranular_cracking_nmc811_jmca2023` — 1차입자 E_p 150 GPa (FEM 가정) · 입계 균열의 FEM 판.
- `trevisanello2021_sc_pc_ncm_cracking_diffusion` — SC/PC 균열 · 액체 vs 고체 전해질 침투 논의.
- `bucci2017_chemomech_failure_assb_cycling_czm` — 황화물 SE G_c 2.8 ± 1.8 J m⁻² (§6-4 비교).
- `song2025_porous_argyrodite_modulus_fracture_toughness` — SE 쪽 **벌크 E·K_Ic** (나노압입 대비 ⅙ · ¼) — "나노 ↔ 벌크" 스케일 차의 SE 판.
- `martinbouvard2003_dem_composite_cold_compaction` · `mesarovicfleck2000_dissimilar_elastoplastic_indentation` — 경질 AM ↔ 연질 SE 비대칭의 근거.
- `aminchiang2016_nmc_electronic_ionic_transport_vs_li` · `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` — **CAM 고유 물성 앵커** 의 수송 쪽 짝.
- `lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging` — 전극/입자 **유효** E_IT 5–6 GPa (다른 양, 비교 금지 사례).

---

## 🗨️ Q&A 로그

- (2026-09-25) **Q. 우리 코드의 "Xu 2017 = Phys. Rev. X 7, 041038, NCM811 나노압입" 은 맞나?**
  → 아니다.  Xu 2017 은 *J. Electrochem. Soc.* 164, A3333 이고 **NMC532** 다.  pristine 이차입자 **E 142.5 ± 11.3 · H 8.6 ± 1.3 GPa**
  (Berkovich 1 mN, 15입자, Ar 글러브박스, ν 0.3 가정).  E_AM 140 은 **정합** (한정어: NMC532, 이차입자) · H_AM 6.0 은 **근거 없음** ·
  K_IC_P 0.3 은 이 논문의 **펠릿** 값 (이차입자는 0.10) · ν 0.25 는 **오귀속** (§0, §7).
