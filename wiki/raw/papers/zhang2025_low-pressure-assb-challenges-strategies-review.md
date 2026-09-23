---
title: "Zhang, Fu, Lu, Hu, Xia, Zhang, Wang, Zhou, Yan, Xia, Wang, Sun 2025 — Challenges and Strategies of Low-Pressure All-Solid-State Batteries (Adv. Mater. 37, 2413499)"
source_url: local-upload/32._Challenges_and_strategies_of_low-pressure_all-solid-state_batteries.pdf
source_url_note: "22쪽 (본문 pp. 1-16 + 참고문헌 124편 pp. 17-19 + 저자 약력 pp. 19-22). **SI 없음**. 그림 Fig. 1-8 + Table 1 크로핑 9장, 크로퍼 누락 0. **Review — 1차 측정 0**; 그림은 모식도 + 타 논문 재수록. 본 그림은 Fig. 1·2·3·4·5·7 여섯 장 (Fig. 6·8 미열람, Table 1 은 텍스트 전사)."
source_doi: 10.1002/adma.202413499
source_license: "CC BY-NC-ND (Wiley-VCH, (c) 2024 The Authors)"
pdf_sha256: 6b3ed38fa4666c0986929173792e175b266ae754451d5ab50c0728488b9c7f14
ingested: 2026-09-23
sha256: 96d1cf54127c945c80d68c1c9430eac40d4772907e07a6b81055316c4a8eaec3
---

# 수집 목적

`assb` 섹션 **33호**, 큐 **32번**. 닻은 `questions/assb-contact-loss-vs-lampe.md` 이고, 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d)에는 축이 **Q6·Q1 — 24 번(저압 장수명 = 25호 Zhou)과 짝** 으로
등록돼 있었다. 들어온 경로는 8호(Li et al. 2026) §6.1 이 이 편을 "recent low-pressure reviews identify pressure reduction
as a central commercialization problem (Zhang et al., 2025)" 로 인용한 것이고, 큐 지문은 `MPa` 50 회 · `contact loss` 4 회로
"32호(Biçer) 종설이 못 준 압력 수치를 이 편이 공급한다" 는 기대를 달았다.

이 digest 의 일은 넷이다 (지시):

1. **Q6(주축)** — 운전 스택 압력 ↔ 접촉 손실(`θ`) ↔ 용량 감쇠의 **정량 관계**를 **1차 원전으로** 제시하는가. 제조 압력과 운전 압력을
   가르는가. 압력별 `θ(P)` 측정 원전(원장 최상위 후보 **Sakka 2022 *JMCA* 10, 16602**)을 인용하는가. **Xu·Yang·Li 2024 *AEM* 14,
   2303539** 와 8호의 "<≈1 MPa", 25호의 "≤5 MPa" 의 출처 관계.
2. **Q1** — "저압에서 접촉 손실이 커진다" 는 서술이 `θ(N)`·`θ(P)` **측정**에 근거하는가.
3. **귀속 검사** — 8호·25호가 이 편에 걸어 둔 기대가 원문에 있는가 (32호 digest 의 '8호 귀속 검사' 선례를 따른다).
4. 수치 표본을 우리 위키에 이미 digest 된 원전과 대조 · 곱 축퇴 처방 열여섯 번째 적용 · DEM 보정 목표로 쓸 압력–접촉 정량 표가 있는가.

> ⚠ **형식 — Review 22 쪽(본문 pp. 1–16 + 참고문헌 124 편 pp. 17–19 + 저자 약력 pp. 19–22), 1차 측정 0.**
> 그림 8 장은 전부 모식도이거나 타 논문 재수록이다(캡션마다 "reproduced/adapted with permission"). 따라서 이 digest 의
> `[인쇄]` 는 10·12·13·32호와 같은 뜻 — **"이 지면에 이렇게 적혀 있다"** 이지 "실측됐다" 가 아니다.
> **이 편의 요약 문장은 채움표 칸을 올리지 않는다** — 칸을 움직일 수 있는 것은 1차 원전으로 거슬러 확인된 명제뿐이다.
>
> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`) · `[재현]` 우리가 지면의 숫자로 계산·대조한 값 ·
> `[해석]` 우리 해석. `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **Q6 칸** | **이동 없음** | 압력 ↔ `θ` ↔ 용량 감쇠의 정량 관계 **0**. 압력–용량 쌍은 재수록 그림 하나(Fig. 3I, 70/7/2 MPa **첫 사이클 곡선**, 출처 번호가 캡션·본문에서 갈림)와 한 압력의 사이클 곡선(Fig. 7B, 2 MPa 고정 · 컷오프만 바꿈)뿐. 압력 스윕 × 사이클의 원전 서술 0 |
| 제조 ↔ 운전 압력 | ✅ **가른다 — 계보 종설 첫 분리** | `[인쇄]` §2.1 두 범주 정의 + Fig. 1 두 패널 + **Table 1 이 두 열을 따로 인쇄**(10 행). 32호가 못 한 것. 단 분리는 **분류**이고 측정이 아니다 |
| **Q1 칸** | **이동 없음 — `θ(N)` 0/33, `θ(P)` 0** | 양극 쪽 접촉 손실 서술은 [57](= 우리 23호 Koerver 2017) 한 곳이고, **원전의 배정을 뒤집어 옮긴다**(D1). 접촉 **분율**·**면적**·단면 정량을 인쇄한 문장 0 |
| **Sakka 2022** | **인용한다 — ref [120]. 그러나 다른 명제에** | "압력 **방향**" 전략(3D 접촉 · 등방 가압)의 근거로 [118] 과 묶어 한 번. **CT 접촉 분율·압력 값은 한 글자도 안 옮긴다.** 25호는 같은 원전을 "50 ↔ ≤12 MPa 접촉 면적 분율" 로 옮겼다 — 두 인용 편이 **같은 원전을 다른 명제에 쓴다** |
| **Xu·Yang·Li 2024** | **인용한다 — ref [11]. 그러나 "<≈1 MPa" 는 없다** | [11–13] 이 붙는 문장은 `[인쇄]` "ASSBs currently require high fabrication and operation pressures, often reaching **hundreds of megapascals**". 이 편의 산업 요구치는 **"< 2 MPa"(Fig. 1, 인용 없음) · "no more than 2 MPa"(p.4, `[인쇄]` "To our knowledge", 인용 없음)** |
| 8호 귀속 | ✅ **선다** | 8호가 이 편에 매단 것은 "pressure reduction = central commercialization problem" 하나 — `[인쇄]` p.4 "reducing the pressure of ASSBs, especially operation pressure, is essential for their commercialization". 8호는 "<≈1 MPa" 를 이 편이 아니라 Xu 2024 에 매달았다(오귀속 아님) |
| 25호 짝 | ✅ **"짝 지목, 인용 아님" 확인 — 그리고 인용은 양방향 모두 시점상 불가** | 이 편 수정본 2024-10-30 · 온라인 2024-12-26 ↔ 25호 접수 2024-11-24. 25호의 "≤5 MPa" 는 **이 편에서 오지 않았다**(이 편은 2 MPa) |
| 원장 기대 "32호 종설에 없는 압력 수치 공급" | ✅ 절반 | `MPa` 50 회 `[재현]` 일치 — 그러나 공급된 것은 **전략별 한 점짜리 압력(Table 1)** 과 **요구치 하나(2 MPa)** 이지 압력의 **함수**가 아니다 |
| 곱 축퇴 처방 16 번째 | **적용 불가 — 대상 없음** | 1차 데이터 0, 곱이 설 모델 0 (식 1 개는 Cu 집전체 응력식) |
| DEM 보정 목표 | **압력–접촉 정량 표 0** | Table 1 은 화학·율·셀 형식이 다른 10 행의 (제조 P, 운전 P, 용량 한 점) — 보정 표가 아니다. 쓸 만한 것은 원전 지목뿐(§"DEM") |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | Challenges and Strategies of Low-Pressure All-Solid-State Batteries |
| 저자 (12) | Jiaxu Zhang, Jiamin Fu (공동 1저자), Pushun Lu, Guantai Hu, Shengjie Xia, Shutao Zhang, Ziqing Wang, Zhimin Zhou, Wenlin Yan, Wei Xia, **Changhong Wang\***, **Xueliang Sun\*** |
| 소속 | Eastern Institute for Advanced Study / Eastern Institute of Technology (Ningbo) · USTC · Ningbo Key Lab of ASSB · Univ. Western Ontario |
| 서지 | *Adv. Mater.* **2025**, 37, 2413499 · doi `10.1002/adma.202413499` · Wiley-VCH · CC BY-NC-ND (© 2024 The Authors) |
| 일정 | 접수 2024-09-09 · 수정 2024-10-30 · 온라인 2024-12-26 |
| 자금 | NSFC (W2441017; 22409103) · "Innovation Yongjiang 2035" (2024Z040) · 중국 박사후 과제 3 건 |
| COI | `[인쇄]` "no conflict of interest" (산업체 소속 0) |
| 형식 | Review 22 쪽: 본문 pp. 1–16(그림 8 · 표 1 · 식 1) + 참고문헌 **124 편** pp. 17–19 + 저자 약력 pp. 19–22. **SI 없음** |
| PDF sha256 | `6b3ed38fa4666c0986929173792e175b266ae754451d5ab50c0728488b9c7f14` (큐 표 앞 32 자 일치). PDF 는 기관 다운로드본(2026-09-21 스탬프) |
| `[해석]` 연구망 | 공저자 Wenlin Yan 은 약력에 `[인쇄]` "PhD student at UCSD, under the supervisor of Prof. Ping Liu" — **25호(Zhou 2025)의 교신 Ping Liu 와 같은 연구실**. 그런데 둘은 서로 인용하지 않는다(시점상 불가, 위 표) |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **산업 요구치 "< 2 MPa" · "no more than 2 MPa" 의 출처 0** — Fig. 1 캡션은 인용 없음, p.4 는 `[인쇄]` "To our knowledge ... (this value varies slightly for different OEMs)" | 요구치 계보의 **다섯 번째 인쇄값**이 또 출처 없이 나온다(§"요구치 계보") |
| G2 | **"The operation pressure of ASSBs in most labs is 50–600 MPa"(Fig. 1 캡션)의 출처 0** | 우리 위키 표본과 맞지 않는다(D4) |
| G3 | **`θ`·접촉 분율·접촉 면적의 수치 0** — `fraction` 0 회, `percolat*` 0, `tortuos*` 0 | Q1 에 줄 것이 없다 |
| G4 | **양극 "재활성화" 문장의 근거 0** — `[인쇄]` "Continuous application of external pressure has been identified as an effective method to maintain contact ... ensuring the reactivation of these materials" 에 인용 번호 없음(앞 문장의 [57] 은 이 명제를 싣지 않는다, D1) | 우리 [[assb-pressure-reapplication-separation-test]] 의 전제(`P↑` → 접촉 되돌림)와 같은 명제인데 원전이 없다 |
| G5 | 재수록 압력 추적 그림(Fig. 3D · 4D · 4G · 7A)의 **기저 스택 압력을 본문이 말하지 않는다** — 그림에만 있다(Fig. 4D ≈45 MPa · 4G ≈20 MPa, `[도표]`) | "저압" 전략의 근거로 쓰인 응력 진동이 **고압 기저 위**에서 잰 것이다(§"압력 진동") |
| G6 | 80 °C 에서 필요 운전 압력이 2 MPa 로 준다는 명제의 출처가 두 곳에서 다르다(p.1 [14] ↔ p.14 [20] 문맥) | D6 |
| G7 | 기준극·3전극 셀은 Ning 2023 [86] 의 Li/Li₆PS₅Cl 셀 한 줄뿐, Li-In 기준 0 | Q5 해당 없음 |
| G8 | `LLI`·`LAM`·`degradation mode`·`fit*`·`OCV`·`EIS`·`SOH` **전부 0 회** | 이 편의 체계에서 용량은 **성능 지표**이고 분해 대상이 아니다(Q4) |

# 그림 — 크로핑 9 장 (Fig. 1–8 + Table 1), 실제로 본 것: **Fig. 1 · 2 · 3 · 4 · 5 · 7** (6 장)

Table 1 은 PDF 텍스트가 정확해 텍스트로 전사했다. **안 본 그림**: Fig. 6(in situ XCT 셀 모식도 [107] · Raman 응력 지도 [39] ·
Cu 응력 모델 [108]) · Fig. 8(전략 요약 모식도). 둘 다 캡션상 압력–접촉 정량이 없어 우리 축 밖이라 판단했다 — ⚠ Fig. 6A 의 XCT 는
**SE 균열**을 보는 셀이고 양극 접촉 분율이 아니다(캡션·본문 기준, 그림 미확인).
**본 6 장 중 본문과 어긋난 것 4 장** (Fig. 1 · 2 · 3 · 5 — 아래 각 절, D 표).

## `[도표]` Fig. 1 — 제조 압력 ↔ 운전 압력 모식도 (봤다)

(A) "Fabrication Pressure" — 양극 복합체 compressing · SE densifying · Li/합금 음극 calendaring + pelletizing · isostatic pressing.
(B) "Operation Pressure" — 4 볼트 지그 · 사이클 중 팽창 · 입계/입내 균열 모식 + **막대그래프**: 세로축 "Operating Pressure (MPa)"
(0–700, 50 근처에서 축 끊김), 가로 "lab" ↔ "industry". 라벨 **"50~600 MPa"**(lab) · **"< 2 MPa"**(industry).
⚠ `[도표]` lab 막대는 **0 에서 ≈550 MPa** 까지 그려져 있다(라벨 50–600 과 다름 — 모식이라 사소, D12).
**그림 전체에 출처 번호가 없다**(가운데 모식 부분만 [21][22] adapted).

## `[도표]` Fig. 2 — 제조 압력 (봤다) — ⚠ 패널 D 가 본문 서술과 반대

- (A) SE 영률: polymer ≈0 · sulfide ≈20–30 · oxide ≈40–200 GPa (`[도표]`, 본문 수치 [22–37] 과 정합).
- (B)(C) LLZTO 표면 응력 지도(±220 MPa 색축) — 연마 전/후([39]).
- **(D) [50] Cronau 2021 재수록** — 박스 `[도표]` **"Stack pressure = 100 MPa"**, 가로 "Fabrication pressure / MPa" 100–500, 세로 이온전도도
  (축 끊김). GC(■) ≈1.4E-3 → 1.8E-3 → 2.1E-3 → 2.2E-3 → 2.3E-3 · **μC(▲) ≈1.5E-3 → 1.8E-3 → 2.1E-3 → 2.05E-3 → 2.05E-3** · AM(●)
  ≈1.1E-4 → 1.5E-4 → 1.9E-4 → 2.1E-4 → 2.2E-4 S cm⁻¹ (`figure-read ≈`).
  ⚠⚠ **본문은** `[인쇄]` "the ionic conductivity of microcrystalline SSEs is **notably independent** of fabrication pressure. Beyond 300 MPa ... remains
  constant" 이라 μC 를 GC·AM 과 **대조**하는데, 그림에서 **μC 는 GC 와 거의 같은 궤적**이다 — 100 → 300 MPa 에 `[재현]` ≈×1.4 오르고
  300 MPa 뒤 평탄. "300 MPa 뒤 평탄" 은 GC 도 같다(≈×1.05). **대조가 그림에 없다**(D3). 원전의 주장일 수도 있으나 이 지면의 그림은
  그것을 보여주지 않는다.
- (E) 다결정 ↔ 단결정 NCM811 모식 + SEM — 모식 라벨 "**Contact loss**" · "Large gaps & cracks" ↔ "Small gaps"(정성).
- (F) Si 전극: "Break under 3 MPa"(코팅 없음) ↔ "Stable under 100 MPa"(코팅), SEM 0/15/60 ↔ 0/60/100 MPa — 본문과 정합.

## `[도표]` Fig. 3 — 운전 압력 × 양극 (봤다) — ⚠ 패널 I 의 출처가 캡션과 본문에서 다르다

- (A)(B) **[58] Koerver 2018 *EES* 재수록** — (A) `ΔV/V₀` vs `x(Li)`: LCO 는 `x` ≈0.6 에서 **≈+2.2 %** 로 부풀었다 줄고, NCM-111/523/622/NCA/811
  은 단조 수축, NCM-811 `x` ≈0.15 에서 **≈−6.6 %** (`figure-read ≈`). (B) 부분 몰부피 `V̄m(Li)`(cm³ mol⁻¹) vs `x`: NCM 계열은 `x` 1.0–0.4 에서
  **≈1–3**, `x` <0.35 에서 급상승해 NCM-811 ≈22(`x` ≈0.25); LCO 는 `x` ≈0.75 에서 **≈−4**; 수평 기준선 Lithium ≈12.8 · LFP ≈11.5 ·
  a-Si ≈8.8 · Indium ≈7.9 · LTO 0 · Graphite 곡선 ≈3–8 (`figure-read ≈`).
  ★ `[해석]` **이 패널이 14호(Oh 2025, Maxwell volumetry) 가 비교하지 않은 기준 부피다** — 14호의 `F·dE/dP` = `[재현]` **42.5 cm³ mol⁻¹**
  은 Li 금속 13.0 + NCM 결정학적 몫(이 그림에서 mid-SOC ≈1–3) 합의 **≈3 배**다. 14호 digest 의 판단(초과분은 복합체 void/역학 항)과
  같은 방향이지만, 결정학적 몫의 **원전 곡선**이 들어온 것은 처음이다(⚠ 14호 셀의 화학·SOC 창과 정확히 맞춰 보지 않았다).
- (C)(D) [59] Jun 2020 — LGPS 환원 분해 모식 + **DEP**(differential electrochemical pressiometry): `ΔP_Gr` 0 → **≈0.7–0.8 MPa**
  (`[도표]`, 세로축 라벨 "ΔP_Gr (Mpa)"), `dP/dQ` 곡선 ±6–8 kPa (mA h)⁻¹.
- (E) [60] 점토형 SSE — 사진에 **"SAIT"** 글자(Samsung SAIT 소속 원전과 정합). (F) VIGLAS [17] · (G) MIEC garnet [61] · (H) PCEE [62] — 사진·모식.
- **(I) 캡션 [63] Oh 2019 *AEM*** — `[도표]` 방전 곡선 3 패널 **"70 MPa" · "7 MPa" · "2 MPa"**, 범례 Pristine · S1 · S2 · S3, 가로 "Capacity (mA h g⁻¹)" 0–200,
  세로 3.0–4.4 V vs Li/Li⁺. `figure-read ≈`: 70 MPa 네 곡선 모두 방전 끝 **≈165–170**; 7 MPa **≈160–165**; 2 MPa Pristine **≈150** ↔ S1–S3 **≈160**.
  ⚠⚠ 본문은 이 패널을 `[인쇄]` "a scalable in situ processing approach ... sulfur ... crosslinking sulfuration of polybutadiene rubber ... **[78]**. Assembled
  batteries exhibited similar discharge capacity even as the operating pressure decreased from 70 to 2 MPa, **as shown in Figure 3I**" 로 **[78] Kwon 2022
  *ESM*** 에 붙이고, 바로 다음 문장의 [63] 은 Li₆PS₅Cl–NBR 공중합 **다른 연구**다(D2). `[해석]` 범례 "S1–S3" 은 가황 수준처럼 읽혀 본문 쪽([78])이
  맞을 가능성이 있으나, 우리는 두 원전 어느 것도 보지 않았다 — **확정 불가**.
  ★ 이 패널이 이 편에서 **유일한 "같은 전극 · 운전 압력 3 점 · 용량" 원자료**다 — 그리고 그것은 **첫(또는 초기) 사이클 곡선**이지 사이클 감쇠가
  아니다. 2 MPa 에서 Pristine 이 ≈10 % 낮다는 것(figure-read)은 본문의 "similar discharge capacity" 에 **묻힌다**.

## `[도표]` Fig. 4 — 운전 압력 × 음극 (봤다) — 본문과 정합, 단 기저 압력을 본문이 숨긴다

- (A) **[85] = 우리 5호 Doux 2020 재수록** — 5 MPa "> 1000 h: No short-circuit" · 25 MPa "~48h: Plating short-circuit" · 75 MPa "0h: Mechanically induced
  short-circuit". 5호 digest 와 **일치**(§"수치 표본").
- (B) [86] Ning 2023 *Nature* — 모델 "Net dendrite growth (µm)" vs 반사이클 용량: 7 MPa ≈5.7 µm(0.5 mAh cm⁻²) · 1 MPa ≈0.6 · 0 MPa ≈0 (`figure-read ≈`).
- (C) [87] Mg₁₆Bi₈₄ 중간층 깊이 프로파일. (D)(E) **[88] Ji 2022 *ESM*** — μ-LiₓSi|SSE|LTO: `[도표]` **"Stress (MPa)" 축 43.6–45.6**, 사이클당 진동
  `ΔMPa` **≈1.0 → 0.8 → 0.7 → 0.65 → 0.5**(5 사이클), 장치 그림의 힘 표시기 **"45 MPa"**. 본문 `[인쇄]` "stress fluctuations of ≈0.7 MPa" 는 이 진동의
  중간값과 맞는다 — ⚠ **기저 ≈45 MPa 는 본문에 없다**(G5).
- (F) **[89] Zhang 2017 *JMCA* 재수록** — LCO/SSE/In-Li X-CT, pristine ↔ charged 단면에 곡률 `R₁` → `R₂`(휨) 표시 + 평면 CT 원판 2 장. **접촉 분율·수치
  0**(그림에도). 본문 `[인쇄]` "the pressure also induced noticeable cracks at the edges of the electrolyte, causing **contact loss**" — **음극/SE 쪽** 명제다.
- (G) [90] Han 2021 *Joule* — Sb:LPSC(7:3) `[도표]` "Stress (MPa)" **≈20 → ≈22.3**(첫 충전), 이후 ≈20.5–21.8 진동. 본문 `[인쇄]` "a substantial pressure of
  **2.25 MPa** was generated" ↔ `[재현]` 기저 ≈20 에서 ≈+2.3 — 정합, **기저 ≈20 MPa 는 본문에 없다**.

## `[도표]` Fig. 5 — 무음극 (봤다) — ⚠ 캡션의 패널 문자·출처가 그림·본문과 뒤바뀐다

- 그림의 **(A)** = `R_tot` (Ω cm²) vs 시간, Cu · Ag · Au 3 행, 5 사이클 — Cu 는 탈리 끝마다 ≈40 → ≈62 로 치솟고 Ag·Au 는 ≈30 근처(`figure-read ≈`).
- 그림의 **(B)** = 집전체 / Mg 박막 / Mg + MXene 완충층 모식("Low pressure operation", "Stress buffering").
- **캡션**: `[인쇄]` "A) Li plating on the bare current collector, Mg film, and Mg/MXene double-layer ... [98]. **B) Total resistance measured over five cycles for
  Cu, Ag, and Au electrodes** ... [103]" — **A·B 가 그림과 뒤바뀌어 있다.**
- **본문**: `[인쇄]` "As depicted in **Figure 5A**, compared to the bare Cu electrode, Ag- and Au-modified electrodes exhibit lower total resistance ... owing to reduced
  contact loss ... **[106]**" · "Jang Wook Choi et al. developed MXene ... **[103]**. As shown in **Figure 5B**" — 본문의 패널 문자는 그림과 맞고, **출처 번호는
  캡션과 다르다**(Cu/Ag/Au: 캡션 [103] ↔ 본문 [106] Sandoval 2023 *Joule*; MXene: 캡션 [98] Pan 2024 ↔ 본문 [103] Oh 2023 *AEM*). D5.
- (C) 탄소 펠트 탄성층 모식([18]) · (D) Ag–C 탄성 바인더 모식([104]).

## `[도표]` Fig. 7 — 저압 전략 (봤다) — 본문 수치와 정합

- (A) [58] Koerver 2018 — `σ₁₁/10⁵ Pa` 축 ±0.8: LCO `Δσ₁₁ > 0`(≈+0.6), NCM `Δσ₁₁ < 0`(≈−0.45), LCO+NCM `Δσ₁₁ ≈ 0` (`figure-read ≈`) ⇒ `[재현]` 진동 폭
  **≈0.05–0.07 MPa** — 이 편에 재수록된 압력 진동 가운데 **가장 작다**(§"압력 진동").
- (B) **[20] Gao 2022 *Joule*(Bruce)** — **"2 MPa, 2.6–4.4 V"**: 방전 ≈135 → ≈88 mAh g⁻¹(50 사이클) ⇒ `[재현]` **≈65 %** (본문 `[인쇄]` 65 % ✓);
  **"2 MPa, 2.6–4.2 V"**: ≈117 → ≈112 ⇒ `[재현]` **≈96 %** (본문 `[인쇄]` 94 % — 판독 오차 안); 초기 용량 비 117/135 ⇒ `[재현]` **−13 %**
  (본문 `[인쇄]` "only a 14% reduction" ✓). 쿨롱 효율 둘 다 ≈99 %.
  ★ `[해석]` **이 패널이 이 편에서 "저압 운전 + 사이클 감쇠" 의 가장 깨끗한 원자료다 — 그리고 압력은 2 MPa 한 점이다.** 감쇠를 바꾼 변수는
  압력이 아니라 **컷오프(양극 부피 변화 6 → 2.5 %)** 다. `θ` 는 재지 않았다(본문 기준). ⇒ 압력 ↔ 감쇠가 아니라 **부피 변화 ↔ 감쇠** 의 표본이다.
- (C) 캡션 **[119]** ↔ 본문 **[19]** — 스프링 몰드 CCD: 압력 `[도표]` ≈5.0 → ≈5.2 MPa 진동(본문 `[인쇄]` "5–5.21 MPa" ✓), 전류 0.2 → 1.0 mA cm⁻²,
  **"Cell short 1.0 mA cm⁻²"** 라벨. 본문 `[인쇄]` "allowing the battery to cycle at higher current densities **up to 1.0 mA cm⁻²**" 는 **그 전류에서 단락했다는
  그림 라벨과 긴장**한다(⚠ "up to" 를 "까지 가서 단락" 으로 읽으면 양립). Table 1 [119] 행 "0.87 mAh cm⁻² at 1 mA cm⁻²" 와의 관계도 불명(D7).

# 절별 해체

## §1 Introduction (p.1)

- `[인쇄]` "ASSBs currently require high fabrication and operation pressures, often reaching **hundreds of megapascals**.[11–13]" — [11] = **Xu·Yang·Li 2024
  *AEM* 14, 2303539**(참고문헌 `[인쇄]` "Adv. Energy Mate." 오타), [12] Oh…Choi 2024 *ESM* 71, [13] Puls … 2024 *Nat. Energy* 9, 1310(SSB 벤치마크).
- `[인쇄]` "High fabrication pressure is essential to achieve intimate solid–solid ionic contact due to the rigidity of inorganic SSEs, while high **operation**
  pressure is applied to counteract the volume expansion of electrode materials" — **두 압력의 역할을 한 문장에서 가른다.**
- 저압 사례 4 개 `[인쇄]`: 점탄성 SSE(영률 1.5 GPa) **<0.1 MPa** [17] · 자기조절 탄소 중간층(치밀화 변형 89 %) 무음극 **7.5 MPa** [18] · 정압 스프링
  (5.5 lb mm⁻¹) **5 MPa** 에서 높은 CCD [19,20] · **80 °C 운전 → 필요 압력 2 MPa [14]**.

## §2 범주·기원·도전 (pp. 2–4) — ★ 축 Q6

- `[인쇄]` §2.1 "these pressures can be categorized into two types: **fabrication pressure** and **operation pressure**" — 제조 = 전극·전해질 제작 중 외부 힘
  (compressing · densifying · calendaring · pelletizing), 운전 = 충방전 중 인가 압력.
- `[인쇄]` 영률 서열 polymer < sulfide(18.5–37.2 GPa) < oxide(41–200 GPa) · "The higher Young's modulus of SSEs, the greater the fabrication pressure required".
- `[인쇄]` 운전 압력의 역할: 전극 부피 변화 · 계면 진화 · Li 덴드라이트("which can even reach **GPa levels** in localized areas") 에 대항 ·
  "the operation pressure significantly influences the cycling stability, rate performance, and discharge capacity of ASSBs.[47–49]" — **정성**, 수치 0.
- §2.2 `[인쇄]` 셀 면적이 커지면 필요한 힘이 선형으로 커지고 파우치에서 불균일 압력 분포 → "nonuniform lithium-ion flux, poor contact between layers, and
  localized stress concentrations, which may result in accelerated degradation". `[인쇄]` "**To our knowledge, the acceptable operation pressure for original
  equipment manufacturers (OEMs) is no more than 2 MPa** (this value varies slightly for different OEMs), with lower pressure being preferred." — 인용 없음(G1).

## §3.1 제조 압력 (pp. 4–5)

- 잔류 응력: LLZTO 미처리 표면 중간 응력 **26 MPa**(지도의 1/4 압축) → 2000# 연마 뒤 평균 **143 MPa**(대부분 인장) [39].
- SSE: 비정질·유리세라믹은 제조 압력↑ → 전도도↑("at an operation pressure of **100 MPa**"), 펠릿 밀도 1.45(100 MPa) → 1.8 g cm⁻³(500 MPa);
  미결정은 "notably independent", 하중 제거 뒤 공극 재출현 → **운전 압력에 크게 의존** [50] (그림과 D3).
  유리세라믹 티오인산염 최적 **0.5 GPa** [41] · FIB 3D: 50 MPa 제조 → 공극 → 입계 임피던스↑, **370 MPa** 에서 유지율·율 개선 [54](Doux 2020 *JMCA*).
- 양극: **510 MPa** 가압에서 다결정 NCM(LP·SP) 다수 균열, 단결정은 **1020 MPa** 에서도 형태 유지 [51]; LCO 는 고압 처리 영향 거의 없음 [55].
- 음극: 중공 Si 는 캘린더링에 파괴, CVD 치밀층 코팅 뒤 >100 MPa 견딤, 코팅 없는 Si 는 **3 MPa** 에서도 균열 [52].

## §3.2 운전 압력 × 양극 (pp. 5–8) — ★ 축 Q1·Q6

- `[인쇄]` "Appropriate operation pressure can usually prevent chemo-mechanical failure of cathode composites caused by volume changes of active materials" [57].
- `[인쇄]` 부피 변화(Fig. 3A/B, [58]): "the volume of most cathode materials **contracts** during lithium removal, with LCO being a rare exception".
- ★ §3.2.1 황화물 복합양극 `[인쇄]` 전문: "Nickel-rich cathode materials like NCM-811, paired with β-Li₃PS₄ solid electrolytes, have been studied to investigate
  interface changes during the charge–discharge cycles of ASSBs.**[57]** It was observed that the active material particles lose close contact with the SSEs due to
  the volume changes of NCM-811 during electrochemical processes. **This loss of contact leads to a decrease in electrochemical activity in subsequent cycles.**
  **Continuous application of external pressure has been identified as an effective method to maintain contact between the active material and SSEs, thereby
  ensuring the reactivation of these materials for future electrochemical reactions.**" → 원전 대조는 §"수치 표본" · D1.
- 단결정 NCM 이 저압에서 구조 유지가 낫다 [51,64–66] — 정성.
- LGPS 환원 분해 → 계면 공극, DEP 로 압력 변화 추적 [59] → "high operation pressure is necessary".
- 황 양극: 부피 팽창 최대 80 %; S₉.₃I 분자결정(체적탄성률 0.29 GPa, 융점 ≈65 °C) → **30 MPa** 안정 운전 [70]; 3D 호스트·탄성 바인더로 "tens of MPa" [71–73];
  `[인쇄]` "ideally **less than 2 MPa**".
- 산화물: PCL 동적 순응 중간층 [74] — 대칭셀 **0.2 MPa** 700 h, LFP 파우치 **0.1 MPa** 400 사이클 85 % 유지. [74] = **Xu, Zhu, Zhao, Du, Li, Yang *Adv. Mater.*
  2023** — `[해석]` **Xu 2024 종설(ref [11])의 세 저자 H. F. Xu · B. Li · S. B. Yang 이 모두 들어 있는 1차 연구**다. 8호가 Xu 2024 로 인쇄한 "<≈1 MPa"
  의 배경이 이 그룹 자신의 0.1–0.2 MPa 데이터일 가능성이 있다 — **가설, Xu 2024 를 받아야 확인된다.**
  MIEC garnet 다공 구조 → 외압 없이 운전, 100 mA cm⁻² [61].
- 점토형 SSE(GaF₃–2LiCl, 영률 <1 MPa, Tg −60 °C, 3.6 mS cm⁻¹) → 외압 불필요 [60] · VIGLAS → **<0.1 MPa**, NCM622 [17].
- 고분자: PCEE(1.1 mS cm⁻¹, t⁺ 0.75) Li|PCEE|LFP 1C 1000 사이클 93 mAh g⁻¹, 0.005 %/사이클 [62] · 437 Wh kg⁻¹ [77] · 가황 BR 바인더 → 70 → 2 MPa 에서 비슷한
  방전 용량(Fig. 3I, D2) · 겔형 바인더 [79].
- 소결 `[인쇄]` "mechanical failure primarily arises from the volume changes in electrode materials and interface evolution" — 정성.

## §3.3 운전 압력 × 음극 (pp. 8–12)

- 양극 부피 변화 <10 % [80,81] ↔ 음극(Li·Li-Mg·Si) >100 % [82]; 음극 쪽 압축 응력 **~10⁻¹ GPa** [83].
- Li 금속 [85] = 5호: 5 MPa >1000 h · 25 MPa 48 h · 75 MPa 기계적 관통, `[인쇄]` "75 MPa exceeds the yield strength of lithium metal by a **hundredfold**, and the
  electrolyte, with **18% porosity**". [86] Ning 2023: 0 → 7 MPa 모델 덴드라이트 증가, 3전극 Li/Li₆PS₅Cl 4.0 mA cm⁻² 에서 **0.1 MPa → 170 사이클, 7 MPa → 35
  사이클** 단락 ⇒ `[인쇄]` "higher pressure leads to faster short-circuiting". in situ TEM [45]: 급속 도금 국부 응력 ≥GPa.
- PDMS 기판 [92] 5000 사이클 55 mV · Mg₁₆Bi₈₄ 중간층 [87] **2.5 MPa**, 11.1 mAh cm⁻², 310 Wh kg⁻¹.
- Si [88]: `[인쇄]` 3 mAh cm⁻², 응력 진동 **≈0.7 MPa**(기저 ≈45 MPa 는 그림에만). In [89] = Zhang 2017 *JMCA*: X-CT 휨 + SE 가장자리 균열 → **contact loss**,
  `[인쇄]` "if the battery is not subjected to external pressure during cycling, electrode expansion could prevent tight contact ... ultimately leading to battery
  failure". Sb [90]: 사이클 뒤 **2.25 MPa** 발생, 5 사이클 뒤 두께 비가역.
- 고용체: Li-Mg [99] · Li-Ag [100,101] — [100] = **우리 6호 Lee 2020**, `[인쇄]` "Li-Ag solid solution alloys also exhibit robust structural stability, making
  low-pressure operation more feasible" · rGO/Li-Ag **4.9 MPa** [102].
- 무음극: Ag/Au 수식이 탈리 끝 총저항을 낮춘다 "owing to reduced **contact loss**" [106] · Mg/MXene **2 MPa** [103] · Ag–C 탄성 바인더 [104] · 탄소 펠트
  [18] 초기 CE **58.4 → 83.7 %**.

## §4 분석·모사 (pp. 12–13)

- in situ XCT(밀리미터 셀) [107] · 다층 SE 횡균열 · Raman → 2D/3D 응력 지도 [39].
- **식 (1)** — Li/Cu 계면 응력 `P_i = ε_Cu E_Cu/(1−ν_Cu) × {3(r_i+t)³ / 2[(r_i+t)³ − r_i³] − ν_Cu/(1−ν_Cu)}` [108]: Cu 변형 0.024 → 0.052 에 응력 **0.151 → 0.503
  GPa**, `[인쇄]` "two orders of magnitude higher than the externally applied pressure". ⚠ 변수 목록에 `κ`(곡률)가 정의되는데 식에 `κ` 가 없다(D10).
- 고분자 코팅 두께 × 압력 → 계면 임피던스 모델 + ML 고속 계산 [76] · DFT: SSE 분해 부피 변화가 전극보다 클 수 있다 [44].
- **DEM 0 · FEM 0 · 연속체 압력–접촉 모델 0** (`DEM`·`discrete element`·`finite element` 0 회).

## §5 저압 전략 + Table 1 (pp. 12–16)

- 재료: Al/Zr 계층 Ni-rich (`Δvolume` ≈4.15 %) **2 MPa** [43] · SE-free LiₓTiS₂ 일체형 양극 — `[인쇄]` "By **minimizing contact losses** between the electrode and the solid
  electrolyte" [115] · LCO+NCM 혼합(반대 팽창) [58] · Li 복합 음극 [116][117] · 가황 BR "150 mAh g⁻¹ even **without external pressure**" [78] · 블록 공중합 바인더
  **1 MPa** [24].
- 셀: 컷오프 4.4 → 4.2 V — NCM83/Li₆PS₅Cl/In-Li, 양극 부피 팽창 **6 → 2.5 %**, 유지율 **65 → 94 %**(50 사이클), 용량 −14 % [20]; `[인쇄]` "Batteries tested under **2 MPa**
  at an ambient temperature of **80 °C** displayed higher discharge specific capacity compared to those tested at 30 °C" (인용 번호 없음 — 문맥상 [20], 서론은 [14], D6) ·
  압력 **방향**: `[인쇄]` "Adjusting the testing environment to achieve **3D contact** between the active material and solid electrolyte has been suggested as a strategy to
  improve battery performance, particularly under low operating pressures.**[120,118]**" → 공기 가압 등방 파우치 홀더 [118] · 스프링 몰드 5 → 5.21 MPa(+4 %) [19]/[119].
- **Table 1** (`[인쇄]`, 10 행 — 제조 P [MPa] / 운전 P [MPa] / 전략 / 성능 / ref):

| 제조 | 운전 | 전략 | 성능 | ref |
|---:|---:|---|---|---|
| 360 | 2 | Hierarchical Al/Zr decorated Ni-rich cathode | 166.7 mAh g⁻¹ at 0.2C | [43] |
| 390 | 0.1 | O3-LiₓTiS₂, SE-free cathode | 165 mAh g⁻¹ at 0.2C | [115] |
| 445 | 70 | Blending cathode with opposite expansion coefficients | Not Given | [58] |
| Not Given | 0.32 | 3D lithium-host design | 40 mAh at 0.2C/0.4C (pouch) | [116] |
| 380 | 1 | Composite anodes | 25 mAh cm⁻² at 0.1 mA cm⁻² | [117] |
| 500 | 2 | Reduce the cut-off voltage | 118 mAh g⁻¹ at 1 mA cm⁻² | [20] |
| 500 | 2 | Isostatic pouch cell holders utilizing air | 173.6 mAh g⁻¹ at 0.1C (pouch) | [118] |
| 375 | 5 | Incorporating compression springs | 0.87 mAh cm⁻² at 1 mA cm⁻² | [119] |
| 5 | <0.1 | Viscoelastic inorganic SSEs | 173 mAh g⁻¹ at 1 C | [17] |
| Not Given | 2.5 | Mg₁₆Bi₈₄ interlayer at anode, F-rich interlayer at cathode | 11.1 mAh cm⁻² at 0.25 mA cm⁻² | [87] |

  `[재현]` 제조 압력이 인쇄된 8 행 중 **7 행이 360–500 MPa**(나머지 [17] 5 MPa) ↔ 운전 압력 10 행 중 **9 행이 ≤5 MPa**(나머지 [58] 70 MPa).
  ⇒ **"저압 ASSB" 의 표본은 전부 "고압 제조 · 저압 운전"** 이다 — 25호의 모양(375 제조 · 2–30 운전)과 같다. **각 행은 압력 한 점, 용량 한 점**이고
  같은 전극의 압력 스윕은 표 안에 **0 행**이다. 성능 칸의 단위가 mAh g⁻¹ · mAh · mAh cm⁻² 로 섞여 행끼리 비교도 안 된다.
- `[인쇄]` Fig. 8 방향 8 개: 무변형 활물질 · 탄성 SSE · 내균열 재료 · 다공 · 일체형 전극 · 반응 제어(컷오프) · **N/P 최적화**("contraction of the cathode is balanced by
  the expansion of the anode") · 정압 시스템.

## §6 결론 (pp. 16–17) — 새 명제 없음. 제조/운전 두 범주, 특성 분석(in situ CT · Raman 3D · 모사), 재료/셀 설계 두 갈래 전략의 재진술.

# 어휘 집계 — NFKC 정규화 후, 대소문자 구분, 낱말 경계 (본문 pp. 1–17 캡션 포함, 참고문헌 열 병기)

**정규화 전후 차이**: NFKC 가 바꾼 문자 **204 자** — 합자 `ﬁ` 83 · `ﬀ` 82 · `ﬂ` 21 · `ﬃ` 7 + 수학 이탤릭 그리스 문자 10(`𝜈` 4 · `𝜖` 2 · `𝛽`·`𝛼`·`𝜀`·`𝜅`) + `¸` 1.
**큐 지문 11 열은 정규화 전후 전부 동일**하다 — 합자가 든 낱말이 지문 열에 없어서다. 그러나 **열 밖에서는 합자가 낱말을 통째로 가린다**:
정규화 전 → 후 `effect` 0 → 30 · `significant` 0 → 29 · `stiff` 0 → 4 · `fluctuation` 0 → 4 · `identif` 0 → **2**(ORCID "identification" · "identified" — 둘 다
식별성과 무관) · `confirm` 0 → 1. ⇒ **이 편에서 정규화 없이 `identif*` 를 세면 0 이 "없음" 처럼 보이지만, 정규화 뒤에도 식별성 의미의 용례는 0** 이다.

| 큐 지문 열 | 큐 값 | 재집계 (NFKC · 대소문자 구분 · 낱말) | 판정 |
|---|---:|---:|---|
| `identifiab` | 0 | **0** | ✓ |
| `uncertaint` | 0 | **0** | ✓ |
| `confidence interval` | 0 | **0** | ✓ |
| `Bayes` | 0 | **0** | ✓ |
| `posterior` | 0 | **0** | ✓ |
| `calibrat` | 0 | **0** | ✓ |
| `LLI` | 0 | **0** (대소문자 무시 부분문자열이면 **23** — micro/poly**crystalli**ne · inter**metalli**c · **milli**meter 류, 참고문헌 3 포함) | ✓ |
| `LAM` | 0 | **0** (대소문자 무시 부분문자열 **1** — 참고문헌 저자명 Has**lam**) | ✓ |
| `degradation mode` | 0 | **0** | ✓ |
| `contact loss` | 4 | **4** (본문 4 · 참고문헌 0; 줄바꿈 사이 공백 허용) | ✓ |
| `MPa` | 50 | **50** (본문 50 · 참고문헌 0; Table 1 머리 `[MPa]` 2 포함. 대소문자 무시 부분문자열 **81** — co**mpa**re · i**mpa**ct) | ✓ |

**큐 지문 11 열 전부 일치.**

`contact loss` 4 회의 **소재**: ① In-Li 음극/SE 가장자리 균열(p.10, [89]) ② 무음극 Li 탈리(p.10) ③ 무음극 Ag/Au 수식(p.10, [106]) ④ SE-free LiₓTiS₂ 양극(p.12,
[115], 설계 논거) — **양극 복합체의 접촉 손실을 가리키는 것은 ④ 하나이고, 그것도 "SE 를 없애 접촉 손실을 줄인다" 는 설계 논거다.** 양극 접촉 손실의
핵심 서술(§3.2.1)은 낱말 `contact loss` 가 아니라 "lose close contact" 로 적혀 지문에 안 잡힌다.

추가 열 (본문, NFKC · 대소문자 구분): `pressure(s)` 216 · `operation/operating/operational pressure` 51 · `fabrication pressure` 30 · `stack(ing) pressure` 3 ·
`contact(s)` 40 · `capacity/capacities` 18 · `capacity fad*` 1 · `retention` 4 · `fraction` **0** · `percolat*` **0** · `tortuos*` **0** · `void(s)` 7 · `crack*` 16 ·
`CT/XCT/X-CT` 6 · `tomograph*` 3 · `SEM` 0 · `EIS` **0** · `impedance` 3 · `DRT` 0 · `OCV` **0** · `dQ/dV` 2 · `GITT` 0 · `SOH` 0 · `degradation` 4 · `aging` 0 ·
`fit*` **0** · `reference electrode` 0 · `three-electrode` 1 · In-Li/indium 5 · `anode-free` 8 · `Arrhenius` 0 · `temperature(s)` 9 · `DEM` **0** · `finite element` 0 ·
`uniqu*` 0 · `distinguish*` 0 · `load cell` 0 · `pressure sensor(s)` 1 · `GPa` 19 · `kPa` 0 · `OEM(s)` 2 · `industr*` 5 · `BMS` 0.

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/33 · `θ(P)` 0** | 양극 접촉 손실은 `[인쇄]` "lose close contact ... decrease in electrochemical activity in subsequent cycles" 한 문단([57])이고 **수치 0**. 그 문단은 원전(23호)의 배정을 뒤집는다(D1). 재수록 CT(Fig. 4F, [89])는 **음극/SE** 휨·균열이고 분율 0. `fraction`·`percolat*`·`tortuos*` 0 회. Sakka [120] 의 CT 접촉 분율은 **옮기지 않았다** |
| **Q2** 독립 관측 | **없다** | 1차 측정 0. 압력 추적(DEP [59] · 힘 센서 [88][90] · σ₁₁ [58])이 **관측 채널로 재수록**되지만 모드를 **가르는** 용도 0 |
| **Q3** 라벨 층위 | 칸 없음 · **층 하나: "재수록 그림의 출처가 캡션과 본문에서 갈린다"** | Fig. 3I(캡션 [63] ↔ 본문 [78]) · Fig. 5(패널 A/B 뒤바뀜 + [98]/[103] ↔ [106]/[103]) · Fig. 7C(캡션 [119] ↔ 본문 [19]) — 그림 8 장 중 **3 장**. 수치를 이 지면에서 옮기면 **어느 원전의 값인지** 가 먼저 불확실하다 |
| **Q4** 유일성·식별성 | **0 — ASSB 누적 0.5(29호) 유지. 스물다섯 번째 성질 "용량은 전략의 성적표 — 분해의 대상이 아니다"** | `capacity` 18 회가 전부 전략별 성능 수치(Table 1 성능 칸 · 유지율)이고, `degradation mode`·`LLI`·`LAM`·`fit*`·`OCV` **0**. 용량 감소의 원인을 부피 변화 · 균열 · 접촉 · 계면 진화로 **나열**할 뿐 어느 몫인지 묻지 않는다 — 물음이 설 자리가 없다 |
| **Q5** Li-In 기준 | **해당 없음** | In-Li 5 회는 전부 **음극**(X-CT [89], 컷오프 셀 [20]). 기준극 0. 3전극 1 회는 Li/Li₆PS₅Cl 단락 실험([86]) |
| **Q6** 압력 | **칸 이동 없음 — 층 둘** | ① **제조 ↔ 운전 분리**: 종설 계보 첫 명시 분리(§2.1 + Table 1 두 열). ② **"저압" = 고압 제조 · 저압 운전** 이 Table 1 전 행에서 `[재현]`(제조 7/8 행 360–500 MPa, 운전 9/10 행 ≤5 MPa). 칸을 못 올리는 이유: 압력 ↔ `θ` ↔ 감쇠의 **함수 0**; 압력–용량 원자료는 Fig. 3I(첫 사이클, 출처 불확정) 하나; Fig. 7B 는 압력 한 점. 요구치 **< 2 MPa** 는 출처 없음(G1) |
| **Q7** dead Li | **해당 없음 — 칸 이동 없음** | 무음극 절(§3.3.3)은 중간층 설계 · 총저항(Fig. 5A, [106]) · 초기 CE 58.4 → 83.7 %([18])뿐. `dead`·`inactive Li` 0 |
| **Q8** 화학·OCP | **칸 이동 없음 — 입력 하나** | OCP 0. 대신 Fig. 3A/B([58])가 **양극 화학별 `ΔV/V₀(x)` · `V̄m(Li)(x)`** 를 준다 — OCP 가 아니라 **부피 쪽 상태함수**. 14호 volumetry 의 기준 부피로 쓸 수 있다(`[해석]`, §Fig. 3) |

# 귀속 검사 — 8호 · 25호 · 원장이 이 편에 건 기대

## 8호(Li 2026) §6.1

`[인쇄]`(8호) "Reviews emphasize that many laboratory solid-state cells still rely on high external pressure, whereas practical targets are moving toward much lower
operating pressure; Xu et al. (2024) note industrial requirements below approximately 1 MPa, and recent low-pressure reviews identify pressure reduction as a central
commercialization problem (**Zhang et al., 2025**)."

| 8호가 이 편에 매단 것 | 33호 지면 | 판정 |
|---|---|---|
| "pressure reduction = central commercialization problem" | `[인쇄]` p.4 "reducing the pressure of ASSBs, especially operation pressure, is **essential for their commercialization** and widespread application in electric vehicles" · p.1 "these high pressures are unsuitable for the industrial application" | ✅ **선다** |
| (문장 앞부분, 인용 없이) "laboratory cells still rely on high external pressure" | Fig. 1 "most labs 50–600 MPa" · p.1 "hundreds of megapascals" | ✅ 선다 (단 50–600 의 근거는 없다, D4) |
| "<≈1 MPa" | **8호는 이것을 Xu 2024 에 매달았다 — 이 편이 아니다.** 이 편은 Xu 2024 를 [11] 로 인용하면서 **"<≈1" 을 옮기지 않고** 자기 값 **2 MPa** 를 인쇄한다 | 8호 쪽 **오귀속 아님**. 다만 **Xu 2024 를 인용하는 두 번째 편이 그 수치를 확인해 주지 않는다** — "<≈1 MPa" 의 출처 확인은 여전히 Xu 2024 원문에 걸려 있다 |

⇒ `[해석]` **32호(Biçer)와 반대 결과다.** 32호에서는 8호가 매단 요구 (ㄷ) 가 원전에 없었다. 33호에서는 8호가 매단 명제가 **그대로 선다** — 8호의 인용 규율은
"요구 문장" 에서 무너지고 "배경 문장" 에서는 선다(표본 2).

## 25호(Zhou 2025)

| 기대 | 확인 | 판정 |
|---|---|---|
| "24 번(저압 장수명)과 짝" (큐) · "25 (짝으로 지목 — 인용은 아님)" (원장) | 33호 참고문헌 124 편에 25호 없음 · 25호 참고문헌에 33호 없음(25호 PDF 전문 검색: `2413499`·"Low-Pressure" 0) | ✅ **인용 아님 확인** |
| 왜 인용이 없나 | 33호 수정본 **2024-10-30**, 온라인 **2024-12-26** ↔ 25호 접수 **2024-11-24**, 게재 2025-01-25 | `[재현]` **양방향 모두 시점상 불가** — 부재는 판단이 아니라 달력이다(22·23호 "지목 0 은 부재가 아니라 시점" 과 같은 형태) |
| 25호 "industry generally aims to operate at or below 5 MPa" 의 출처가 이 편인가 | 이 편의 요구치는 **2 MPa**. 5 MPa 는 스프링 몰드 [19][119] 운전 압력으로만 나온다 | ❌ **이 편에서 오지 않았다** — 25호 ≤5 MPa 는 여전히 출처 없음 |
| `[해석]` 연구실 인접 | 33호 공저자 Wenlin Yan(UCSD, Ping Liu 지도) ↔ 25호 교신 Ping Liu | 같은 연구실에서 **두 요구치(2 ↔ 5 MPa)** 가 두 달 간격으로 따로 인쇄됐다 |

## 원장 기대 — "32호 종설에 없는 압력 수치를 공급, `MPa` 50"

✅ `MPa` 50 은 재집계 일치. 공급된 것: 요구치 1 개(2 MPa, 출처 없음) · lab 대역 1 개(50–600, 출처 없음) · Table 1 의 (제조, 운전) 10 쌍 · 재수록 원전의 개별
압력값 ≈30 개(0.1 · 0.2 · 0.32 · 1 · 2 · 2.5 · 4.9 · 5 · 7 · 7.5 · 25 · 30 · 70 · 75 · 100 · 370 · 510 · 1020 MPa …). ⚠ **압력의 함수(`x(P)`)는 0 개.**

# Sakka 2022 · Xu 2024 — 인용 추적

| 원전 | 33호 ref | 33호가 붙인 명제 (`[인쇄]`) | 25호가 붙인 명제 (25호 digest) | 판정 |
|---|---|---|---|---|
| **Sakka, Yamashige, Watanabe, Takeuchi, Uesugi, Uesugi, Orikasa 2022 *JMCA* 10, 16602** | **[120]** | "Adjusting the testing environment to achieve **3D contact** between the active material and solid electrolyte has been suggested as a strategy to improve battery performance, particularly under low operating pressures.[120,118]" — §5 "Effect of applied pressure **direction**" | CT 로 **50 MPa 에서 접촉 면적 분율이 ≤12 MPa 보다 크게 개선**, 모델상 **25 MPa 면 안정 접촉** | ⚠ **같은 원전, 다른 명제.** 33호는 수치를 한 글자도 안 옮긴다. `[해석]` Sakka 가 둘 다 담았을 수 있다(압력 크기 + 방향). **원전을 안 봐서 확정 불가** — Sakka 의 `θ(P)` 측정 가치는 그대로이고, **지목은 2 회(25 · 33)** 가 된다 |
| **Xu, Yang, Li 2024 *AEM* 14, 2303539** | **[11]** | "high fabrication and operation pressures, often reaching **hundreds of megapascals**.[11–13]" | 25호 ref 11 — 앞 문장 "high stack pressures" 에만(25호 digest) | 두 편 모두 Xu 2024 를 **"압력이 높다"** 의 근거로 쓴다. **"<≈1 MPa" 를 Xu 2024 에서 인쇄한 것은 8호뿐** — 확인 편 0 |
| (관련) **Xu, Zhu, Zhao, Du, Li, Yang *Adv. Mater.* 2023, 35, 2212111** | [74] | PCL 동적 순응 중간층 — 대칭셀 **0.2 MPa** 700 h · LFP 파우치 **0.1 MPa** 400 사이클 85 % | — | `[해석]` Xu 2024 종설 저자 그룹의 1차 연구. "<≈1 MPa" 의 배경 후보 — **가설** |

# 요구치 계보 — 다섯 번째 인쇄값

| 편 | 요구치 | 근거 층위 | 원전 |
|---|---|---|---|
| 8호 Li 2026 | < ≈1 MPa | 재인용 | Xu 2024 (확인 편 0) |
| 12호 Kouhestani 2022 | 0.4–1 MPa | 재인용 (모델 최적) | Tian & Qi 2017 / Shao 2022 (미확정) |
| 13호 Zheng 2026 | < 5 MPa | 1 차 주장 | [35] (13호 digest) |
| 25호 Zhou 2025 | ≤ 5 MPa | 인용 없음 | — |
| **33호 Zhang 2025** | **< 2 MPa** (Fig. 1) · **≤ 2 MPa, OEM 마다 약간 다름** (p.4) · 황 양극 "ideally < 2 MPa" | **인용 없음, `[인쇄]` "To our knowledge"** | — |

`[해석]` **다섯 편, 네 값(≈1 · 0.4–1 · 2 · 5), 확인된 원전 0.** 값의 산포(0.4 → 5, 12.5 배)가 원전의 부재와 같이 간다. 우리 [[assb-stack-pressure-operating-window]]
의 아래 벽을 "산업 요구치" 로 적을 때는 **단일 값이 아니라 0.4–5 MPa 의 띠 + 원전 0** 으로 적는 게 지면에 충실하다.

# 수치 표본 대조 (이미 wiki 에 digest 된 원전으로)

| 33호 주장 | 원전 (우리 위키) | 판정 |
|---|---|---|
| [85] Li 대칭셀 5 MPa ">1000 h" 무단락 | 5호 Doux 2020: `[인쇄]` >1000 h (5호 digest: **본문이 그 근거로 인용하는 SI Fig. S5 는 92 h** 토모그래피) | ✅ 수치 일치 — 5호가 짚은 **근거 그림 불일치를 33호가 그대로 물려받는다** |
| [85] 25 MPa 48 h · 75 MPa 기계적 단락 | 5호: ≈48 h · 0 h ("shorted before the plating and stripping test began") | ✅ |
| [85] "75 MPa exceeds the yield strength ... by a hundredfold", "18% porosity" | 5호: `[인쇄]` "around 100 times"(`[재현]` 94×) · 공극률 18 %(`[재현]` 펠릿 4 개 15.1–19.8 %) | ✅ (5호의 산포 4.7 %p 는 옮기지 않음) |
| **[57] NCM811/β-Li₃PS₄: "This loss of contact leads to a decrease in electrochemical activity in subsequent cycles"** | **23호 Koerver 2017**: `[인쇄]` "While the contact loss should **only occur during the initial charge**, corresponding well to the initial capacity drop, **the ongoing capacity fade can be attributed to the propagating interphase formation**" · 50 사이클 뒤 "a **similar** morphology" | ❌ **배정이 뒤집힌다** — 원전은 접촉 손실을 **첫 충전** 에, 이후 감쇠를 **계면상** 에 배정했다. 33호는 접촉 손실을 **이후 사이클의 활성 감소** 로 옮긴다 (D1) |
| **[57] 문단: "Continuous application of external pressure ... ensuring the reactivation"** | 23호: 운전 압력 **64/70 MPa 일정**(D3 표기차), 압력을 바꾼 실험 0, 재활성 서술 0. `[인쇄]` "no additional solid electrolytes can fill the emerging voids" | ❌ **원전에 없다 — 그리고 인용 번호가 없다**(G4). `[해석]` 우리 위키에서 "재가압 → `θ_AM` 되돌림" 을 실측한 것은 **4호 Shi 2020(300 MPa 재가압)** 인데, 33호 참고문헌 124 편에 4호는 **없다** |
| [100] Li-Ag 고용체 → 저압 운전 가능 | 6호 Lee 2020: 운전 2/3/4 MPa + 무압 대조, 무압은 0.1 C 에서만, `[인쇄]` "pressurization is unavoidable for high-current operations" | ✅ 방향 일치 — 단 6호의 **율 조건**은 옮기지 않았다 |
| [89] Zhang 2017 *JMCA*: X-CT, 충전 뒤 휨 + SE 가장자리 균열 → contact loss | 미보유 (원장 ★★★, 22·23호 지목 2 회: "충전 중 부피 수축 → 접촉 감소를 압력으로 감시") | **미확인** — 33호의 서술(**X-CT 휨**)과 원장 서술(**압력 감시**)이 다른 측면을 가리킨다. 지목 3 회째 |
| [58] Koerver 2018 *EES*: Table 1 제조 **445** · 운전 **70** MPa | 4호 Shi digest 가 후속 2 순위로 지목("화학역학 종설 + 스택 압력"); 23호 Koerver 2017 의 제조 445/446 · 운전 70/64 MPa | ⚠ **같은 연구실 1 년 차 두 편이 같은 (445, 70)** — 23호 D3 의 "70 ↔ 64" 표기차가 2018 에서도 70 으로 인쇄된 것과 정합. 원전 미보유 |
| [86] Ning 2023: 0.1 MPa 170 사이클 ↔ 7 MPa 35 사이클 단락 | 5호 위 벽(≥25 MPa 단락)과 **방향 일치**, 대역은 더 낮다(7 MPa) | ⚠ 위 벽이 **셀 설계·전류(4.0 mA cm⁻²)** 에 따라 25 → 7 MPa 로 내려온다 — 5호 절 경고 2("위 벽이 전류로 얼마나 내려오는지 모른다")의 **재인용 표본 하나**(원전 미보유) |
| Fig. 7B [20] 유지율 65 → 94 %, −14 % | 33호 자기 Fig. 7B | ✅ `[재현]` 65 % · 96 % · −13 % (판독 오차 안) |
| Fig. 4G [90] "2.25 MPa" · Fig. 4D [88] "≈0.7 MPa" | 33호 자기 Fig. 4 | ✅ 진동 크기 정합 — **기저(≈20 · ≈45 MPa)는 본문에 없음** |

`[해석]` 우리 위키가 원전을 가진 대조 7 건 중 **5 건이 선다(5호 3 · 6호 1 · 자기 그림 여럿)** 이고, **서지 않는 2 건이 전부 23호 Koerver 2017 한 문단**이다 — 그리고
그 문단이 **이 편에서 양극 접촉 손실을 다루는 유일한 문단**이다. 32호가 인용 12 건을 제목 기준으로 어긋냈던 것과 달리, 33호의 어긋남은 **적지만 우리 축에
정확히 떨어진다.**

# ★ 압력 진동 크기 ↔ 산업 요구치 (`[해석]`, 재수록 원자료 네 개에서)

| 원전 (재수록) | 셀 | 기저 스택 압력 | 사이클당 압력 진동 | 출처 |
|---|---|---|---|---|
| [58] Koerver 2018 | LCO · NCM · 혼합 양극 | 미기재 | ≈0.05–0.07 MPa (`σ₁₁` ±0.6×10⁵ Pa) | Fig. 7A `[도표]` |
| [59] Jun 2020 | 흑연 음극 ± LGPS | 미기재 | ≈0.7–0.8 MPa (`ΔP_Gr`) | Fig. 3D `[도표]` |
| [88] Ji 2022 | μ-Si ‖ LTO | **≈45 MPa** | ≈0.5–1.0 MPa (5 사이클 감소) | Fig. 4D `[도표]` · `[인쇄]` ≈0.7 |
| [90] Han 2021 | Sb:LPSC ‖ Li | **≈20 MPa** | ≈1.2–2.3 MPa | Fig. 4G `[도표]` · `[인쇄]` 2.25 |
| [19]/[119] 스프링 몰드 | Li 금속 CCD | ≈5 MPa | ≈0.2 MPa (+4 %) | Fig. 7C `[도표]` · `[인쇄]` 5 → 5.21 |

⇒ `[해석]` **합금·Si 음극 셀의 사이클당 압력 진동(≈0.7–2.3 MPa)이 이 편 자신의 산업 요구치(≤2 MPa)와 같은 자릿수다.** 산업 조건에서 스택 압력은 **제어
상수가 아니라 사이클 안에서 ≈100 % 움직이는 상태변수**가 된다 — 8호의 "coupled state/control variable" 을 숫자로 받친다(8호는 숫자 없이 인쇄). ⚠ 단서 셋:
진동은 **고압 기저(20–45 MPa) · 정변위 지그** 에서 잰 것이라 저압 기저에서는 강성이 달라 진동도 다르다 · 스프링(정압) 지그는 진동을 ≈4 % 로 누른다 ·
**양극만의 진동은 ≈0.05–0.07 MPa**(LCO/NCM, [58])로 두 자릿수 작다 — 즉 **양극 접촉 손실 문제에서 압력 진동의 주범은 양극이 아니라 상대극**이다.
이 마지막 점은 우리 [[assb-pressure-reapplication-separation-test]] 의 `P` 축 설계(양극 `θ` 를 되돌리려 압력을 바꾼다)에 **상대극 부피 변화가 같은 크기로 섞인다**는
경고가 된다 — 17호·25호가 전압 쪽에서 본 "상대극이 가장 큰 항" 의 **역학 판**이다.

# DEM 보정 목표 — 압력–접촉 정량 표가 있는가

**없다.** 이 편에 있는 압력 관련 "표" 는 Table 1 하나이고, 그것은 (제조 P, 운전 P, 전략, 성능 한 점)이다 — 화학 · 율 · 셀 형식 · 용량 단위가 행마다 다르고,
**접촉 분율·면적·공극률 열이 없다.** DEM 에 넣을 **보정 목표**가 아니다.

지목으로 남는 것 (전부 원전 미보유):

| 용도 | 원전 | 이 편에서 본 것 | 왜 |
|---|---|---|---|
| **`θ(P)` 보정 목표** | Sakka 2022 *JMCA* [120] | 인용만(수치 0) | 25호 digest 가 옮긴 "50 ↔ ≤12 MPa 접촉 면적 분율(CT)" — DEM `θ(P)` 의 **유일한 측정 후보**. 여전히 1 순위 |
| **SE 압분 보정 목표** | Cronau…Roling 2021 *ACS Energy Lett.* 6, 3072 [50] | Fig. 2D: 스택 100 MPa 고정, 제조 100–500 MPa × 결정성 3 종의 σ | SE 입자층 치밀화 → 유효 전도도 — **SE 단독** 이라 양극 접촉 목표는 아니다. 16호와 같은 연구실(Roling) |
| **입자 부피 변화 입력** | Koerver 2018 *EES* [58] | Fig. 3A/B: `ΔV/V₀(x)`, `V̄m(Li)(x)` | DEM 입자 호흡(breathing)의 **입력 곡선** — 보정 목표가 아니라 입력 |
| **스택 응력 응답 목표** | Ji 2022 *ESM* [88] · Han 2021 *Joule* [90] · Jun 2020 *AFM* [59] | Fig. 3D · 4D · 4G | 정변위 지그에서 사이클당 ΔP — DEM 이 **입자 호흡 → 스택 응력** 을 재현하는지 보는 목표(접촉이 아니라 응력) |

# 곱 축퇴 처방 — 열여섯 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

**적용 불가 — 대상 없음.** 1차 데이터 0, 곱이 설 모델 0 (유일한 식 (1)은 Li/Cu 계면 응력).

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| 1단계 (16호) | `R` 과 `C` 를 같이 | `EIS` 0 회 · `impedance` 3 회(모델 [76] · 일반론) · 무음극 `R_tot`(Fig. 5A)는 저항만 | ❌ |
| 2단계 (18·25호) | 면적을 아는 대조군 | Sakka [120] 를 인용하지만 면적값 0 | ❌ |
| 3단계-a/b (19호) | `Ea` · `C` 상한 | `Arrhenius` 0. 온도는 "80 °C 면 2 MPa" 한 문장(출처 둘로 갈림, D6) | ❌ |
| 4단계 (20호) | 시간 영역 동일 검사 | 0 | ❌ |

★ `[해석]` **이 편이 처방에 주는 것은 단계가 아니라 교란 하나다**: `P` 를 처방의 조작 변수로 쓸 때(압력 되돌림 축), **상대극 부피 변화가 만드는 ΔP 가 사이클당
0.7–2.3 MPa** 로 산업 운전 압력과 같은 크기다(§"압력 진동"). 곱 `A_eff·ε_p/R_s` 의 `A_eff` 를 압력으로 흔들어 가르려면 **양극의 `A_eff(P)` 와 상대극의
`ΔP(SOC)` 를 먼저 분리**해야 한다. 이 편은 곱도, 분리도 말하지 않는다 — 번역은 우리 것.

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것, 그리고 인용

| # | 등급 | 내용 |
|---|---|---|
| **D1** | ★★★ | §3.2.1 이 [57](= 23호 Koerver 2017)에 이어 "loss of contact leads to a decrease in electrochemical activity **in subsequent cycles**" · "continuous application of external pressure ... **reactivation**" 을 쓴다 — 원전은 접촉 손실을 **첫 충전에만**, 이후 감쇠를 **계면상**에 배정했고 압력을 바꾸지 않았다. 재활성 명제는 **인용 번호도 없다**(G4) |
| **D2** | ★★ | Fig. 3I: 캡션 **[63]** Oh 2019 ↔ 본문 "as shown in Figure 3I" 는 **[78]** Kwon 2022 가황 BR 문장. 그리고 본문 "similar discharge capacity ... 70 to 2 MPa" 는 그림의 2 MPa Pristine ≈150 ↔ 70 MPa ≈165–170(`figure-read ≈`, ≈−10 %)을 덮는다 |
| **D3** | ★★ | Fig. 2D: 본문 "microcrystalline SSEs is **notably independent** of fabrication pressure" ↔ 그림의 μC 는 GC 와 같은 궤적(100 → 300 MPa ≈×1.4 후 평탄, `figure-read ≈`) — **대조가 그림에 없다** |
| **D4** | ★★ | Fig. 1 "The operation pressure of ASSBs in most labs is **50–600 MPa**" — 출처 0. 우리 위키의 운전 압력 표본(4호 ≈2 · 5호 1–75 스윕 · 6·7호 2–4 · 11호 20 · 14호 10/20 · 16호 97/389 · 17호 50 · 19호 0.42–0.84 · 23호 64/70 · 25호 2–30 MPa)에서 50 MPa 이상은 **16 · 17 · 23호 + 5호 75 MPa 점** 뿐 — 표본이 무작위는 아니지만 "most labs" 를 지지하지 않는다. 600 MPa 는 **제조** 압력 대역이다(Table 1 제조 360–500 · §3.1 510 · 1020) |
| **D5** | ★★ | Fig. 5: 캡션의 **A/B 가 그림과 뒤바뀜** + 출처 번호가 캡션([98] Mg/MXene · [103] Cu/Ag/Au)과 본문([103] MXene · [106] Cu/Ag/Au)에서 다름 |
| **D6** | ★ | "80 °C 운전 → 필요 압력 2 MPa": 서론 **[14]**(Zhang F. *eTransportation* 2023) ↔ §5 는 [20] Gao 2022 문단 안에서 인용 번호 없이 |
| **D7** | ★ | Fig. 7C: 캡션 **[119]** ↔ 본문 **[19]**; 본문 "cycle at higher current densities **up to 1.0 mA cm⁻²**" ↔ 그림 라벨 "**Cell short 1.0 mA cm⁻²**"; Table 1 [119] "0.87 mAh cm⁻² at 1 mA cm⁻²" 와의 관계 불명 |
| **D8** | ★ | 참고문헌 중복: **[45] = [84]**(Gao…Wang *Nat. Commun.* 13, 5050, 2022) · **[83] = [108]**(Cheng…Meng *Nat. Nanotech.* 18, 1448, 2023 — 저자 목록 길이만 다름) |
| **D9** | ★ | 산업 요구치 두 표기: Fig. 1 "**< 2 MPa**" ↔ p.4 "**no more than 2 MPa**"(≤) — 둘 다 출처 없음(G1) |
| **D10** | ⚠ | 식 (1) 변수 설명에 곡률 `κ` 가 정의되는데 식에 `κ` 가 없다 · 무음극 셀 "11.1 mAh⁻²"(p.10) ↔ Table 1 "11.1 mAh cm⁻²" |
| **D11** | ⚠ | 참고문헌 [11] 학술지명 "Adv. Energy **Mate.**" · Fig. 3D 세로축 "(Mpa)" · 약력 "in **20222**" |
| **D12** | ⚠ | Fig. 1 lab 막대 0 → ≈550 MPa ↔ 라벨 "50~600 MPa" (`figure-read ≈`, 모식) |

`[해석]` D1 · D2 · D3 은 **본문 서술이 원자료(원전 또는 재수록 그림)보다 강하게 말하는** 같은 방향이다 — 그리고 셋 다 **"압력 → 접촉 → 용량"** 서사를 매끈하게
만드는 쪽이다(재활성 · "similar capacity" · "independent").

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **Q6 칸은 안 움직인다 — 종설이 가진 압력 수치 50 개 중 "압력의 함수" 는 0 개.** 압력 ↔ `θ` ↔ 감쇠의 정량 관계를 1차 원전으로 댄 문장이 없다.
   가장 가까운 재수록 원자료(Fig. 3I 70/7/2 MPa)는 **첫 사이클 곡선이고 출처 번호가 둘로 갈린다.**
2. ★★★ **Sakka 2022 는 인용되지만 `θ(P)` 로서가 아니다** — 두 인용 편(25 · 33)이 같은 원전을 다른 명제에 쓴다. 원장 최상위는 유지, 지목 2 회.
3. ★★★ **"<≈1 MPa" 는 여전히 8호 혼자다** — Xu 2024 를 인용하는 두 번째 편(33호)은 그 수치를 안 옮기고 자기 값 2 MPa 를 인쇄한다. 요구치 계보 **5 편 · 4 값 ·
   원전 0**. Xu 2024 의 필요성은 **올라간다**(원장 ★★ → 판단은 사용자).
4. ★★★ **양극 접촉 손실의 유일한 문단이 원전(23호)의 배정을 뒤집는다** (D1) — 종설 층에서 "접촉 손실 → 사이클 감쇠 → 압력으로 재활성" 이 **원전 없이** 만들어지는
   현장. 분류 체계 **다섯 번째 표본 "접촉 손실 = 압력으로 되돌릴 수 있는 활성 감소"** — 우리 카드의 틀(가역 비활성 ≠ `LAM_PE`)에 **가장 가까운 종합 층
   표현인데, 근거가 없다.**
5. ★★ **제조 ↔ 운전 압력 분리는 이 편이 종설 계보 첫 명시**이고, Table 1 이 "저압 ASSB = 고압 제조 · 저압 운전" 을 전 행에서 보여준다 (`[재현]`).
6. ★★ `[해석]` **상대극 압력 진동(0.7–2.3 MPa/사이클) ≈ 산업 운전 압력** — 압력 되돌림 분리 시험에 상대극 역학 항이 같은 크기로 섞인다.
7. ★ Fig. 3B 가 14호 volumetry 의 **결정학적 기준 부피 곡선**을 준다(원전 [58]).

# 후속 후보 — 참고문헌 124 편 (제목·본문 용례 기준 선별)

124 편 구성 `[재현]`(본문 절 기준, 대략): 서론·SSE 재료 1–37 · 제조 압력 38–56 · 양극 57–79 · 음극 80–106 · 분석·모사 107–108 · 전략 109–124.
**모드 분해 · 식별성 · 기준극을 제목·용례에 단 원전 0.** 압력–접촉 정량 1차 후보는 Sakka [120] 하나.

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Sakka, Yamashige, Watanabe, Takeuchi, Uesugi, Uesugi, Orikasa 2022 *J. Mater. Chem. A* 10, 16602** | [120] | 이미 원장 최상위 — 이 편은 "3D 접촉/압력 방향" 명제로 인용(지목 2 회째). `θ(P)` 측정 후보 유일 | Q1·Q6·DEM | ★★★★ |
| **Xu, Yang, Li 2024 *Adv. Energy Mater.* 14, 2303539** | [11] | "<≈1 MPa" 를 확인할 곳이 이 원문뿐(33호는 확인 안 해 줌) | Q6 | ★★★ (승격 제안) |
| Xu, Zhu, Zhao, Du, Li, Yang 2023 *Adv. Mater.* 35, 2212111 | [74] | Xu 2024 저자 그룹의 0.1–0.2 MPa 1차 데이터 — "<1 MPa" 배경 가설 | Q6 | ★ |
| **Koerver, Zhang, de Biasi, …, Zeier, Janek 2018 *Energy Environ. Sci.* 11, 2142** | [58] | 4호가 이미 지목(2 순위) · 이 편 Fig. 3A/B · 7A · Table 1(445/70) — 부피 변화 곡선 + 압력 추적 + 혼합 양극. **지목 2 회** | Q6·Q8·DEM 입력 | ★★★ |
| **Gao, Liu, Hu, Ning, Jolly, …, Grant, Bruce 2022 *Joule* 6, 636** | [20] | 2 MPa 고정 · 컷오프로 양극 부피 변화 6 → 2.5 % · 유지율 65 → 94 % — **부피 변화 ↔ 감쇠** 의 1차 표본. `θ` 를 쟀는지 확인 | Q1·Q6 | ★★ |
| Cronau, Szabo, König, Wassermann, Roling 2021 *ACS Energy Lett.* 6, 3072 | [50] | SE 압분(제조 × 스택) σ — DEM SE 층 보정 목표 후보, 16호와 같은 연구실 | DEM | ★★ |
| Zhang, Schröder, Arlt, Manke, Koerver, Pinedo, Weber, Sann, Zeier, Janek 2017 *J. Mater. Chem. A* 5, 9929 | [89] | 원장 ★★★ — X-CT 휨·가장자리 균열 → contact loss(음극/SE). **지목 3 회째**(22 · 23 · 33) | Q1·Q6 | ★★★ (기존) |
| Ji, Zhang, Liu, …, Qu 2022 *Energy Storage Mater.* 53, 613 · Han, Lee, Lewis, …, McDowell 2021 *Joule* 5, 2450 | [88] · [90] | 사이클당 스택 응력 진동 원자료 — DEM 응력 응답 목표 | DEM | ★ |
| Ning, Li, Melvin, …, Bruce 2023 *Nature* 618, 287 | [86] | 0.1 ↔ 7 MPa 단락 사이클 170 ↔ 35 — 위 벽의 전류 의존 | Q6 | ★ |
| Puls … 2024 *Nat. Energy* 9, 1310 | [13] | SSB 셀 벤치마크(다수 연구실) — "lab 압력 대역" 의 실제 분포가 여기 있을 수 있다(D4 검증) | Q6 | ★ |

`[해석]` **Q1(`θ(N)`) · Q4(ASSB 식별성) · 곱 분리 · 기준극 누설** 을 채울 원전은 이 편의 인용 그물에서도 **나오지 않는다**(32호와 같은 결론). Q6 의 정량은
Sakka 한 편에 여전히 걸려 있다.
