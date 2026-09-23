---
title: "Sakka, Yamashige, Watanabe, Takeuchi, Uesugi, Uesugi, Orikasa 2022 — Pressure dependence on the three-dimensional structure of a composite electrode in an all-solid-state battery (J. Mater. Chem. A 10, 16602-16609)"
source_url: local-upload/1._Pressure_dependence_on_the_three-dimensional_structure_of_a_composite_electrode_in_an_all-solid-state_battery.pdf + 1._Sup_Pressure_dependence_on_the_three-dimensional_structure_of_a_composite_electrode_in_an_all-solid-state_battery.pdf (SI)
source_url_note: "본문 8 쪽(참고문헌 44 편) + SI 16 쪽(그림 S1-S16). 크로퍼가 본문 7 + SI 16 = 23 장을 잡았고 15 장 봤다(Fig. 1-6 · S1-S4 · S7 · S13-S16). 단위는 페이지 렌더링으로 확인(추출 텍스트에서 µ · fi 글리프 소실). 원자료는 커밋하지 않는다. 25호(Zhou 2025) ref 12 · 33호(Zhang 2025) ref [120]."
source_doi: 10.1039/d2ta02378d
source_license: "CC-BY 4.0 (지면 표기 'Licensed under CC-BY 4.0')"
pdf_sha256: 58852a218b768472288e22f2f93fbe271b63005177747d837c73f543a0e848ad
si_sha256: 356bee3bd41d20ad23f5839e5e8bb9b7ccebe2e23c4bc168e503c3db20399b08
ingested: 2026-09-23
sha256: f8774df6cde824a265611b66cb7cde74869693850d30cbc405bafea6fc37470e
---

# 수집 목적

`assb` 섹션 **39호**. 큐 **40번** — **2차 묶음(큐 40~59, 원장 §1 상단 순서)의 첫 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1) 최상위 ★★★★ — 25호(Zhou 2025, ref 12)와 33호(Zhang 2025 저압 종설, ref [120])가
**같은 원전을 다른 명제로** 인용해서, "X선 CT 로 압력별 CAM–SE 접촉 면적 분율을 쟀다 — `θ(P)` 측정 후보" 로 올라온 편.

Yuya Sakka, Hisao Yamashige, Ayaka Watanabe, Akihisa Takeuchi, Masayuki Uesugi, Kentaro Uesugi, **Yuki Orikasa**(교신) —
**"Pressure dependence on the three-dimensional structure of a composite electrode in an all-solid-state battery"**,
*J. Mater. Chem. A* **2022**, **10**, 16602–16609, doi `10.1039/d2ta02378d`.
`[인쇄]` 접수 2022-03-24 · 수리 2022-07-08 · 게재 2022-07-22. **CC-BY 4.0**.
소속: 리쓰메이칸대 응용화학(Sakka · Watanabe · Orikasa) · **Toyota Motor Corporation**(Yamashige — `[인쇄]` "designed the operando measurement cell") · JASRI/SPring-8(Takeuchi · M. Uesugi · K. Uesugi — 빔라인 BL20XU 지원 · 재구성).
`[인쇄]` 자금: JSPS KAKENHI 19H02694 · NEDO JPNP20004. 빔타임 제안 5 건(2019B1726 · 2020A0502 · 2021A1005 · 2021A1539 · 2021B1724).

본문 PDF **8 쪽**(본문 6 + 참고문헌 2, 44 편) · SI PDF **16 쪽**(그림 S1–S16, 표 0, 방법 서술 0). sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 눈으로 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ pymupdf 추출에서 `µ` 와 `fi` 글리프가 떨어진다(예: "pixel size of ca. 0.5 mm", "rst"). **단위는 페이지를 렌더링해 눈으로 확인했다** — 화소 **0.5 µm**, 분석 영역 **512 × 512 × 50 µm³**.

---

# 판정 (먼저)

> ★★★★ **Q1 — 쟀다. 그러나 잰 것은 `θ` 도 `u` 도 아니라 표면 피복 `φ` 다. 칸 +0.5 (`φ(P)`), `θ(N)` 0/39.**
>
> **(a) 무엇의 분율인가.** `[인쇄]` "The contact area fraction represents the fraction of the area in contact between NCM and LGPS **with respect to the surface area of the NCM particles** (Fig. S13)."
> ⇒ **CAM 표면 중 SE 와 닿은 몫 = 표면 피복 `φ`**. SE 와 전혀 안 닿은 입자의 **수 분율(통째 비연결 `u`) 은 보고하지 않는다**(`percolat*` 0 회 · 입자별 통계 0).
> 37호 결론(표면 `φ` → `A_eff·k_p` 곱의 손잡이 · 통째 `u` → `ε_p` = `LAM_PE`)에 대면 **이 편이 잰 것은 `A_eff` 쪽 손잡이**다 — `LAM_PE` 와 헷갈리는 쪽이 아니라 **`k` 와 헷갈리는 쪽**.
>
> **(b) 값.** `[도표]` Fig. 3c, 신품(사이클 0), 압력 5 점: **0 MPa ≈78.3 % · 6 ≈74.9 · 12 ≈77.9 · 50 ≈84.3 · 100 ≈82.7 %**. 세로축 70–90 % 로 잘려 있다.
> `[인쇄]` "The fraction increases by approximately 10% when the pressure is greater than 50 MPa compared with the state under a pressure less than or equal to 12 MPa" ·
> "the improvement in the contact area fraction stopped when the pressure reached 50 MPa". ⚠ 단조가 아니다(6 < 0 · 100 < 50) — 본문은 0 → 6 MPa 의 하락을 언급하지 않는다(D4).
>
> **(c) 축.** **압력(P) 축뿐.** CT 는 전부 신품 셀이고 사이클 뒤 CT 는 0 장 ⇒ **`θ(N)` 0/39** (그리고 `φ(N)` 도 0). 사이클 데이터(Fig. 2a, 6 MPa 10 사이클)는 있으나 그 셀의 구조는 안 찍었다.
> **`θ(P)` 측정 여부 — 아니다; `φ(P)` 측정이다.** 원장의 "`θ(P)` 측정 후보" 는 **`φ(P)`** 로 고쳐 읽는다. 게다가 이 압력은 **제조 압력과 같은 것**이다(아래 (e)).
>
> **(d) 해상도 · 분할의 불확실성 — 효과보다 크다.** `[인쇄]` 화소 ≈0.5 µm · 20 keV 단색 · 투영 1800 장 · Dragonfly 4.1 에서 "transmission intensity" 로 3 상(NCM · LGPS · void) 분할 — **문턱값 · 문턱 민감도 · 부분부피 처리 · 반복 측정 인쇄 0**.
> `[재현]` **분할이 질량을 보존하지 않는다**: 같은 1 : 1 : 0.1 (wt) 혼합물인데 Fig. 3b 의 NCM/LGPS 부피비가 **0.47 (0 MPa) → 0.76 → 0.97 (12) → 0.71 → 0.75 (100)** — 고체 두 상의 비가 ×2 흔들린다(압축으로 고체 부피가 절반이 될 수는 없다; 원문은 "soft LGPS … contract … reducing the apparent volume fraction" 로 설명).
> 이 흔들림이 `φ` 효과(≈+6–9 %p)보다 크다. 그리고 `[도표]` Fig. S13 에서 **0 MPa(공극률 44 %)에서도 거의 모든 NCM 단면이 초록(접촉) 테두리를 가진다** ⇒ 0.5 µm 화소에서 "접촉" 은 **1 µm 아래 틈을 못 가르는 판정**이다(`[인쇄]` LFP 절에서 "nanoscale voids … challenging to quantify correctly due to the resolution of X-ray CT" — 해상도 한계를 저자가 LFP 에만 적용).
>
> **(e) 제조 ↔ 운전 압력.** `[인쇄]` 서론이 둘을 가른다("The former is the fabrication pressure and the latter is the stack pressure") — 그리고 곧바로 **자기 실험에서 붙인다**:
> "Since **no pressure was added during fabrication** in our experiments, the pressure shown in this study **corresponds to the previously reported fabrication pressure**."
> + `[인쇄]` Fig. S14 — 50 MPa → 0 MPa 로 풀어도 "No clear changes were detected with respect to the void". ⇒ 이 편의 `φ(P)` 는 **단조 가압의 최대 압력 함수 = 제조 압력 함수**다. 운전 압력(되돌림) 의 `φ` 는 0 점.
>
> ★★★★ **Q6 — +0.5.** 계보 **첫 "압력 → 측정된 양극 구조량 → 측정된 저항" 사슬**: 같은 장치에서 압력별 CT(공극률 · 부피분율 · `φ` · 굴곡도)와 EIS(`[인쇄]` "simultaneously performed with the X-ray CT measurements") — `R_ct` 4 점(6 · 12 · 50 · 100 MPa), 겉보기 전도도 4 점, 용량(다른 셀 3 점 · 같은 셀 5 단계).
> 33호가 "압력 수치 50 개 중 압력의 **함수** 0" 이라 적은 자리에 **1차 원전의 함수**가 들어온다. 반 칸인 이유: 압력 = 제조 압력(단조, 되돌림 0) · 점당 n = 1 · 오차 막대 0 · 같은 셀 5 단계 용량은 **사이클 번호와 교락**(S3) · 2전극 `R_ct`(상대극 In–Li 계면도 같은 압력을 받는다).
>
> ★★★★ **곱 축퇴 — 이 편이 곱의 두 인자를 한 셀에서 따로 쟀다(22번째 적용).** `[도표]` `R_ct` 6 → 100 MPa **≈8.7×10⁵ → ≈0.6×10⁵ Ω (×14, "order of magnitude" ✓)** ↔ `φ` **≈74.9 → ≈82.7 % (×1.10)**.
> `[재현]` `R_ct·φ` = 6.5 → 3.2 → 1.4 → 0.51 ×10⁵ Ω — **면적당 전도도(= `k` × 해상도 아래 접촉 몫)가 ×13**. 로그로 **`R_ct` 변화의 ≈4 % 만 CT 접촉 면적이 설명한다.**
> 원문은 `[인쇄]` "This corresponds to the increase of the contact area fraction" · "The enhanced contact area fraction … led to an order of magnitude reduction in charge transfer resistance" — **상관 4 점을 귀속으로 읽는다**. ⇒ `[해석]` 18호 "chemical composition **or** contact area" · 37호 `A_eff ↔ k_p` 항등의 **첫 실측 표본**: 한 인자(`φ_CT`)를 직접 재도 곱의 나머지(`k_p` · 1 µm 아래 실접촉 · 상대극)가 변화의 대부분을 가져간다.
>
> ★★★ **25호 ↔ 33호 인용 판정 — 둘 다 원문에 선다, 다른 절에.** 25호 = 본문 결과(Fig. 3c + Fig. 6b: "at high pressures (50 MPa), SSE particles filled internal cavities … improving the contact area fraction compared to … at or below 12 MPa … notable reduction in charge transfer resistance") ✓, 단 "significantly" 는 ≈+6–9 %p 에 대한 과장 쪽.
> 33호 = 결론의 제언("realising the contact between the AM and the SE in a three-dimensional manner … improved even at low pressures") ✓ — Sakka 가 `[인쇄]` "it is expected" 로 쓴 **추측**을 33호는 "has been suggested" 로 옮겼다(정확). 두 인용은 모순이 아니라 **결과 ↔ 제언**의 분업이다.
> ⚠ **우리 25호 digest 의 오귀속 하나**: "모델상 **25 MPa 면 안정 접촉**" 은 Sakka 에 **없다**(모델 0 · "25 MPa" 는 SI Fig. S3 범례의 가압 단계로만 등장). Zhou 원문에서 그 문장은 ref 12 **다음 문장이고 인용 번호가 없다** — 25호 digest(`raw/`, 불변)가 인접 문장을 Sakka 에 붙였다. 컴파일 페이지에서 정정한다.
>
> ★★★ **DEM `θ(P)` 보정 목표 — 조건부 가능, 우선순위는 `φ` 가 아니라 공극률.** 인쇄 · 판독 가능한 압력–구조 곡선이 **5 점 × 5 종**(복합층 공극률 · SE 층 공극률 · 3 상 부피분율 · `φ` · 굴곡도 최빈/최소)이고 조성(1 : 1 : 0.1 wt) · 입도(SEM) · 일축 · Ø 1 mm 가 적혀 있다.
> 그러나 (i) `φ` 의 동적 범위(≈75–84 %)가 분할 불확실성(부피비 ×2)보다 작고, (ii) 접촉 판정 = **0.5 µm 화소** 라 DEM 쪽 접촉 정의를 그 해상도로 맞춰야 비교가 서며, (iii) 점당 n = 1 · 오차 0 · ROI 512 × 512 × 50 µm³ 한 개(전극 두께 `[재현]` ≈0.6 mm 중 어느 깊이인지 미기재).
> ⇒ **1순위 목표 = 복합층 공극률(P)**(44 → 23 %, 인쇄 막대 라벨), **2순위 = 3 상 부피분율**(질량수지 결함을 알고 쓸 것), **`φ(P)` 는 "해상도 0.5 µm 판정에서 0.75–0.85" 라는 범위 제약**으로만. 비등방성(Fig. 4)은 **정성**(방향별 `φ` 수치 0).
>
> **Q4 — 0/39, 서른한 번째 성질: "곱의 한 인자를 직접 재고, 나머지 인자가 변화의 96 %(로그)를 가져가는 것을 같은 지면에 둔 채 '대응한다' 로 읽었다."**
> `uncertaint` · `error` · `identifiab` 전부 0 회.

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **분할 문턱값 · 방법**(전역 문턱? 기계학습? 부피 필터?) · 문턱 민감도 | `φ` 는 경계 화소 판정 하나로 정해진다. 부피비 ×2 흔들림(§5.1)이 이 자리에서 나온다 |
| G2 | **CT 5 점이 같은 셀의 순차 가압인가, 다른 셀인가** | `[인쇄]` "can be performed in the same cell while changing the pressure" 는 **가능하다**는 말이다. S4 단면은 시야마다 입자 배치가 달라 보인다(`[해석]`, 같은 셀이라도 높이가 다르면 그럴 수 있다) |
| G3 | **ROI 가 전극 두께의 어디인가** (분리막 쪽? 집전체 쪽? 중간?) | `[재현]` 전극 두께 ≈0.6 mm(아래 §5.4) 중 50 µm 슬랩 하나 — 깊이 구배가 있으면 대표성 없음 |
| G4 | **`φ` 계산의 분모에 NCM–NCM 접촉 면이 들어가나** | 4호(Shi 2020)는 들어갔다. 들어가면 고압에서 NCM 끼리 닿는 면이 늘어 `φ` 가 눌린다 — 100 MPa 의 하락(84.3 → 82.7)의 후보 |
| G5 | **AB(도전재)는 어느 상으로 분류됐나** | 3 상 분할이라 AB(10 wt% 중 0.1)는 LGPS 나 void 로 흡수됐다. 전자 경로는 이 편에 없다 |
| G6 | **EIS 조건** — 주파수 범위 · 진폭 · SOC(충전 전? 후?) · 적합 결과표 · 두 번째 RC 의 정체 | Fig. S16 회로는 `R_SE` + (`R_CT`∥C) + ((R + Z_w)∥C). 두 번째 요소는 **이름 없음**. 어느 호가 양극이고 어느 호가 In–Li 인지 근거 0 |
| G7 | **"apparent conductivity" 가 무엇의 전도도인가**(SE 층? 복합층? 두께는 CT 에서?) | `[인쇄]` Nyquist 에서 추정 — 식 · 두께 0 |
| G8 | **S3 "capacity improvement" 의 기준 셀** | `[인쇄]` "divided by that of the former at the same cycle" — "former" 가 어느 셀의 몇 번째 사이클인지 미특정. Fig. 2a 셀로 `[재현]` 하면 인쇄값과 안 맞는다(D7) |
| G9 | **압력 유지 방식** | `[인쇄]` "controlled using screws" + 하단 로드 트랜스듀서(모니터). 사이클 중 압력 시계열 0 |
| G10 | **반복 · 산포** | 모든 그림 점당 n = 1, 오차 막대 0. Fig. 2b(다른 셀) 6 MPa 첫 방전 ≈27 ↔ S3a(다른 셀) 6 MPa 첫 방전 ≈35 mAh g⁻¹ — 셀 간 ≈30 % |
| G11 | **밀도값** | 질량수지 검산(§5.1)에 NCM · LGPS 밀도가 필요한데 인쇄 0 — 아래 `[재현]` 의 기대 부피비는 **외부 일반값** 가정 |

---

# 1. 서지 · 낱말 지문

규칙: **NFKC 정규화 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전)**. SI 는 따로 센다.
NFKC 변경 문자: 본문 **38 자**(`ﬀ` 30 · `ﬃ` 7 · `ﬂ` 1) — **열 변화 0**. SI 0 자. 소프트 하이픈 0. 줄끝 하이픈 이어붙이면 `stack pressure` 10 → 11(아래 보조 열), 지문 11 열 변화 0.
⚠ 이 PDF 는 `fi` 합자가 **NFKC 대상 문자로 남지 않고 글리프째 빠진다**("rst" · "quantied") — `identifiab` 류가 있었다면 `identiab` 로 떨어졌을 것이라 따로 검사했다: `identi*` 1 회("identified", 3 상 분할 문장) — `identifiab` 계열 0.

| | `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 본문 | **0** | **0** | **0** | 0 | 0 | **0** | 0 | 0 | 0 | **0** | **30** |
| SI | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 22 |

보조(본문): `contact area` **13** · `fraction` 14 · `tortuosity` 21 · `anisotrop*` 4 · `fabrication` 8 · `stack pressure` 10(이음 11) · `cycl*` 9 · `resolution` **1**(LFP 절) · `segment*` **1** · `threshold` **0** · `error` **0** · `percolat*` **0**.
⇒ `[해석]` **"contact area" 13 회 · "contact loss" 0 회** — 이 편은 접촉을 **손실(시간)** 이 아니라 **형성(압력)** 으로만 다룬다. 불확실성 어휘 전무.

---

# 2. 셀 · 실험 (`[인쇄]`)

- 양극 활물질: **LiNbO₃ 코팅 LiNi₀.₃₃Co₀.₃₃Mn₀.₃₃O₂ (NCM111)** — 회전 유동층 코팅기(Powrex MP-01), ref 35 절차. SE: **Li₁₀GeP₂S₁₂ (LGPS)**, 550 °C Ar 고상반응. 도전재: 아세틸렌 블랙(Denka).
- 복합체 **NCM : LGPS : AB = 1 : 1 : 0.1 (wt)**, 막자 혼합(Ar 글러브박스).
- 셀: **Ø 1 mm** 실린더에 복합양극 1.0 mg + SE 1.0 mg + In–Li 박(In 박 + Li 박 압착). O-ring 밀봉. 상 · 하 스테인리스 봉 = 집전체, 하단 봉이 **로드 트랜스듀서**에 닿는다. 압력은 상단 **나사**로 조절.
- `[인쇄]` "the loading of NCM is **60 mg cm⁻²**, which is much higher than the reported condition. This is due to the electrode diameter of 1 mm and the readability of the precision electronic balance." — 두꺼운 전극이 "inhomogeneous charge/discharge reaction due to the high ionic resistance in through-plain direction" 을 낳는다고 저자가 적는다.
- 전기화학: 298 K, **0.01 C**, 2.0–4.0 V(`[도표]` Fig. 2). Hokuto Denko HJ1001SDE.
- CT: SPring-8 **BL20XU**, 20 keV 단색(Si(111) 이중결정), CMOS(Hamamatsu C13440-20CU), **화소 ≈0.5 µm**, 시야 ≈1.0 × 1.0 mm, 투영 1800 장 / 180°, 노출 0.05 s. 분할 · 분석 **Dragonfly 4.1**.
- 분석 영역: 부피 · 접촉 = **512 × 512 × 50 µm³**, 굴곡도 = **36 × 36 × 50 µm³**.
- 압력 점: CT · 부피 = **0 · 6 · 12 · 50 · 100 MPa**; EIS = 6 · 12 · 50 · 100; 첫 사이클 다른 셀 = 6 · 50 · 100; 같은 셀 단계 가압 = 6 · 12 · **25** · 50 · 100 (SI Fig. S3, 두 사이클씩).
- **제조 압력 0** — `[인쇄]` "no pressure was added during fabrication".

---

# 3. 절별 해체

## 3.1 서론 (p1–2)

- `[인쇄]` 액체셀에서는 활물질–전해질이 "essentially sufficient interfacial connection" 을 이루지만, ASSB 는 AM–SE 접촉이 나쁘면 이온 수송이 막힌다(refs 17–21).
- `[인쇄]` **제조 압력 ↔ 스택 압력을 정의로 가른다**. "Charge/discharge reaction causes a volume change in the AM, resulting in poor contact between AM and SE. On the other hand, stack pressure is necessary to maintain proper contact."
- `[인쇄]` **"the upper limit of the stack pressure is suggested to be 1 MPa practically,[22]"** — ref 22 = **Wang · Kazyak · Dasgupta · Sakamoto, *Joule* 2021, 5, 1371–1390**. ★ `[해석]` 우리 계보가 모은 산업 요구치(8호 <≈1 · 12호 0.4–1 · 13호 <5 · 25호 ≤5 · 33호 <2 MPa, **확인된 원전 0**)에 **여섯 번째 인쇄 + 원전 지목 하나**가 붙는다. 원전은 미열람.
- `[인쇄]` "On the cathode side, it has been shown that strain caused by the pressure reduces the contact between the AM and SE and determines the performance.[18,24]"
- `[인쇄]` 새로움 주장: "quantitative analysis of the cathode three-dimensional structure controlled by applied pressure, and direct observation of the anisotropy of the contact interface do not yet appear to have been fully explored."

## 3.2 전기화학 — Fig. 2 · SI Fig. S3

- `[인쇄]` 6 MPa 일정 10 사이클(Fig. 2a): "Because a pressure of 6 MPa is very small, both the capacity and cycling performance are low. … Even if the stack pressure is maintained, **the volume change of NCM results in a significant decrease in contact with LGPS at specific spots, which causes capacity fading.**"
  `[도표]` 방전 1 → 2 → 10 사이클 ≈27 → ≈18 → ≈3 mAh g⁻¹; 첫 충전 ≈44. ⚠ **이 감쇠 귀속("접촉 감소")은 측정 없는 서술**이다 — 이 셀의 CT 는 없다. `[해석]` 23호(Koerver)의 "접촉 손실 = 첫 충전" 배정과 달리 **사이클마다의 접촉 감소**로 쓴다(33호가 23호를 뒤집은 방향과 같다).
- `[도표]` Fig. 2b(압력별 **다른 셀** 첫 사이클): 방전 6 MPa ≈27 · 50 MPa ≈39 · 100 MPa ≈44 mAh g⁻¹; 충전 ≈44 · ≈89 · ≈162. `[인쇄]` 첫 충전의 비가역분은 LGPS 산화 분해(ref 36).
  `[재현]` 방전 6 → 100 MPa **×1.6**, 첫 쿨롱효율 ≈61 → 44 → 27 % — **압력이 오를수록 첫 CE 가 떨어진다**(충전이 방전보다 훨씬 더 는다). 원문 언급 0.
- SI Fig. S3(같은 셀, 두 사이클씩 6 → 12 → 25 → 50 → 100 MPa): `[도표]` (b) "capacity improvement" ≈100 · ≈127 · ≈156 · ≈188 · ≈197 %.
  ⚠ `[도표]` (a) 의 **절대 방전 용량은 12 MPa 부터 거의 오르지 않고 100 MPa 에서 떨어진다**: 6 MPa 1st ≈35 · 12 MPa 3rd ≈21 · 25 MPa 5th ≈20 · 50 MPa 7th ≈22 · 100 MPa 9th ≈14 · 10th ≈10.5 mAh g⁻¹.
  ⇒ `[인쇄]` "The observed capacity also increases with respect to the applied pressure" 는 **"6 MPa 일정 셀의 같은 사이클 대비"** 라는 정규화 안에서만 참이다(D7). 압력 축과 사이클 축이 **완전 교락**(압력을 올릴 때마다 사이클 번호도 오른다).
- `[인쇄]` 선행 대조: 제조 압력 50 MPa 가 150 MPa 보다 용량이 낮았다는 ref 15(**Doux 외, *J. Mater. Chem. A* 2020, 8, 5049** — 우리 5호 Doux *AEM* 2020 = ref 26 과 **다른 논문**) → "the pressure shown in this study corresponds to the previously reported fabrication pressure … consistent".

## 3.3 공극률 · 부피분율 — Fig. 3a · 3b

- `[도표]` Fig. 3a 공극률: 복합층 ≈44 · 42.5 · 39 · 30.5 · 23 % / SE 층 ≈53 · 41 · 39 · 15 · 4.3 % (0 · 6 · 12 · 50 · 100 MPa). `[인쇄]` 100 MPa 에서 "23% and 5%".
  `[인쇄]` ≤12 MPa 에서 두 층 차이 없음, 고압에서 복합층의 압력 의존이 줄어든다 — NCM 의 높은 Young 률(ref 37) · 큰 입경(Fig. S1) 때문에 "more voids around the NCM particles".
- Fig. 3b (막대 안 **인쇄 숫자**): Void 44 / 42 / 39 / 31 / 23 % · LGPS 38 / 33 / 31 / 41 / 44 % · NCM 18 / 25 / 30 / 29 / 33 %.
  `[인쇄]` 해석: "The proportion of LGPS decreases while the proportion of NCMs increases up to a pressure of 12 MPa … high pressure makes LGPS compress around the NCM particles … causes the soft LGPS to contract,[38] thus reducing the apparent volume fraction. When the pressure exceeds 12 MPa, the volume of NCM does not increase, and the porosity decreases due to the increasing LGPS." ⇒ **"densification … proceeds through two stages."**
  ⚠ `[해석]` §5.1 — 이 "두 단계" 의 1 단계는 **질량수지를 어긴다**. 고정 혼합물에서 NCM/LGPS 부피비는 불변이어야 한다.
- `[인쇄]` 입자 크기 대조(SI Fig. S12): 수백 nm LFP 복합전극은 50 MPa 에서 void ≈5 % — "the small particles can fill the large void spaces. However, … nanoscale voids, which is challenging to quantify correctly due to the resolution of X-ray CT." (LFP 조성 · 셀 조건 인쇄 0.)

## 3.4 ★ 접촉 면적 분율 — Fig. 3c · SI Fig. S13

- 정의 `[인쇄]`: 위 판정 (a). "The contact area between NCM and LGPS serves as a reactive area for charge-transfer."
- 값 `[도표]`: 위 판정 (b). 세로축 70–90 %.
- `[인쇄]` 기구: "At low pressures, the NCM particles are pressurised preferentially,[24] and so contact with the surrounding LGPS is not increased; however, at high pressures, LGPS fills the voids around the NCM particles, resulting in an increased contact area." · "After 50 MPa, there is a small change in the volume of the voids, but no change in the contact area fraction."
- `[도표]` S13(XZ 단면, 5 압력, 100 µm 눈금): **모든 압력에서 NCM 단면 테두리의 대부분이 초록(NCM/LGPS)** — 파랑(NCM/void)은 짧은 조각. 0 MPa 도 마찬가지. **SE 와 한 점도 안 닿은 입자는 단면에서 거의 안 보인다.**
  ⇒ `[해석]` 이 해상도에서 **통째 비연결 `u` ≈ 0 에 가깝다** — 카드 물음의 `u` 는 이 방법의 측정 범위 밖이다(있다면 1 µm 아래 틈으로).

## 3.5 비등방성 — Fig. 4 · 7

- `[인쇄]` "the NCM particles have good contact with LGPS in the **Z-axis direction, which is the pressure direction**. On the other hand, preferential contact with the voids is observed in the **horizontal direction**." · "predominantly observed at low pressures, but also even at high pressures, though less frequently."
- `[도표]` Fig. 4a: XY · YZ · XZ 단면 각 압력 1 장씩(10 µm 눈금), 파랑 조각이 YZ · XZ 단면에서 입자의 **좌우 옆면**에 많다 — 정성적으로 서술과 맞다. Fig. 4c 100 MPa 3D 에 노란 타원 3 개(수평 공극).
  ⚠ **방향별 `φ` 수치 0** — 표면 법선 방향별 분포 · 히스토그램 · 통계 0. 비등방성은 **대표 단면을 보여 주는 정성 주장**이다.
- `[인쇄]` Fig. 7(모식, **안 봤다**) 서술: 평판 집전체의 일축 가압은 단단한 AM 을 먼저 누르고, AM 이 빽빽하면 AM 사이 틈이 "low-pressure spots" 가 되어 SE 가 못 채운다; "Since no force is applied from the horizontal direction, the gap cannot be fully filled."

## 3.6 굴곡도 — Fig. 5

- 정의 `[인쇄]`: SE 로 이어진 3D 경로 길이 ÷ 관찰 영역 두께(50 µm), 36 × 36 × 50 µm³, 압력당 경로 **N = 100**.
- `[도표]` 최빈(빨강) ≈5.7 · 5.1 · 4.7 · **3.8** · 5.6 / 최소(파랑) ≈4.5 · 3.5 · 3.2 · **2.5** · 2.8 (0 · 6 · 12 · 50 · 100 MPa). 100 MPa 분포가 넓다(≈2.8–8.7).
- `[인쇄]` 100 MPa 에서 굴곡도 증가 — "at 100 MPa when the AMs are well filled, the effect of increasing the AM is superior to the effect of decreasing the porosity" → "trade-off between the connectivity of AM/SE and the tortuosity of SE". 단 "minor impact … since the pressure dependence of the charge/discharge measurement does not exhibit significant differences at pressures above 50 MPa."
- ⚠ `[해석]` 측면 36 µm 는 NCM 입자(≈5–18 µm) 2–4 개 폭 — 대표 체적(REV)로는 작다. 100 MPa 의 "증가" 는 **ROI 하나**의 결과이고, 100 MPa 에서 NCM 부피분율이 29 → 33 % 로 오른 것(§5.1 의 분할 문제와 같은 자리)에 기대어 있다.
- 우리 24호 · 2호 굴곡도 논의와의 관계: 이 편의 굴곡도는 **기하 경로 길이비**(`τ`, 제곱 아님)이고 전도도 역산(`τ²` 혹은 `τ` 인자)이 아니다(`concepts/assb-tortuosity-factor-effective-conductivity-split.md`).

## 3.7 EIS — Fig. 6 · SI Fig. S15 · S16

- `[인쇄]` "apparent conductivity increases almost linearly with increasing pressure. This corresponds well to the behaviour of the porosity reduction." `[도표]` ≈7.8 · 8.0 · 9.1 · 9.7 ×10⁻⁵ S cm⁻¹ (6 · 12 · 50 · 100 MPa) — **+24 %**.
- `[인쇄]` "the charge transfer resistance is **inversely proportional to the pressure**. This corresponds to the increase of the contact area fraction of NCM/LGPS as shown in **Fig. 3b**[→ 3c, D2]." `[도표]` `R_ct` ≈8.7 · 4.1 · 1.6 · 0.6 ×10⁵ **Ω**(면적 정규화 없음).
- `[인쇄]` "The increase in the capacity of the charge/discharge reaction (**Fig. 1**[→ Fig. 2, D1]) is mainly attributed to the improved interface between NCM and LGPS, resulting in a reduction of the charge-transfer resistance."
- S16 회로: `R_SE` – (`R_CT` ∥ C) – ((R – Z_w) ∥ C). **두 번째 요소 이름 없음.** 2전극(In–Li | LGPS | NCM).
- `[도표]` S15: 6 MPa 반원 지름 ≈0.9 MΩ · 12 MPa ≈0.45 MΩ (축 2000 kΩ) / 50 MPa 호 ≈15 → ≈88 kΩ(지름 ≈70 kΩ) · 100 MPa 작은 호 ≈15 → ≈35 kΩ(≈20 kΩ) (축 200 kΩ).
  ⚠ 저압 두 점은 Fig. 6b 와 맞고, **고압 두 점은 눈으로 본 호 지름이 Fig. 6b `R_ct`(≈160 · ≈60 kΩ)의 ≈1/2–1/3**(D8). 두 RC 적합이 저주파 쪽을 나눠 가졌을 수 있다 — 적합표가 없어 확인 불가(G6).

## 3.8 결론 (p6)

- `[인쇄]` "increasing the pressure decreased the porosity and improved the contact area fraction … The enhanced contact area fraction between the AM and SE led to an order of magnitude reduction in charge transfer resistance. **The logarithmic increase of the charge/discharge capacity** with the increase in pressure was attributed to both … but the effect of the charge transfer resistance reduction was particularly dominant."
  ⚠ "logarithmic" 의 적합 · 근거 그림 0(D9). "particularly dominant" 의 정량 분해 0.
- `[인쇄]` "The contact interface between the AM and the SE was **marginally perpendicular** to the applied pressure. By improving the contact interface in the **vertical direction**, that is, by realising the contact … in a three-dimensional manner, it is expected that the charge/discharge characteristics of ASSBs can be improved even at low pressures." ⚠ 본문은 **Z(수직, 가압 방향) = 좋은 접촉 · 수평 = 나쁜 접촉**이라 했다 — 결론의 "vertical direction 을 개선" 은 본문 어휘와 방향이 뒤집힌다(D3).

---

# 4. ★★★★ `φ` 는 어느 손잡이인가 — 37호 두 손잡이 대조

| 37호 손잡이 | 원형 모델에서의 자리 | 이 편이 잰 것 |
|---|---|---|
| 표면 피복 손실(`A_eff`) | BV 분모에서 `A_eff·k_p·ε_p/R_s` — **`k_p` 와 정확한 항등**, OCV · 용량에 안 보임 | ✅ **이것** — `φ` = NCM 표면 중 LGPS 와 닿은 몫 |
| 입자 통째 비연결(`u`) | `ε_p` 뿐 = `LAM_PE` 와 같은 칸 | ❌ 보고 0 (S13 정성상 ≈0 — 해상도 밖) |

⇒ `[해석]` 이 편은 **`LAM_PE` 와 헷갈리는 손잡이를 재지 않았고, `k` 와 헷갈리는 손잡이를 쟀다**. 그리고 같은 지면의 `R_ct` 가 그 항등을 **데이터로** 드러낸다(§9): `φ_CT` 가 ×1.10 움직일 때 `R_ct` 는 ×14.
용량 쪽(Fig. 2b ×1.6)은 `φ` 로 설명될 수 없다 — 37호 모델에서 `A_eff` 는 용량에 없다; 이 편의 용량 증가는 `[해석]` 저율(0.01 C)에서도 남는 **`η` 항**(두꺼운 전극 ≈0.6 mm · `R_ct·A` ≈7×10³ Ω cm²) 이거나 **1 µm 아래 통째 비연결**이다 — 이 편은 둘을 가르지 않는다.

---

# 5. `[재현]` 검산

## 5.1 ★★★ 분할의 질량수지 (Fig. 3b 인쇄 숫자)

| P / MPa | NCM % | LGPS % | NCM/LGPS | 고체 합 % |
|---:|---:|---:|---:|---:|
| 0 | 18 | 38 | **0.47** | 56 |
| 6 | 25 | 33 | **0.76** | 58 |
| 12 | 30 | 31 | **0.97** | 61 |
| 50 | 29 | 41 | **0.71** | 70 |
| 100 | 33 | 44 | **0.75** | 77 |

- 고정 혼합물(1 : 1 : 0.1 wt)이면 **NCM/(LGPS+AB) 부피비는 압력에 불변**이어야 한다(고체의 ≤100 MPa 체적 변형은 수 % 이하 — `[추론]`, 물성값 인쇄 0).
- 외부 일반 밀도(NCM111 ≈4.7–4.8 · LGPS ≈2.0 · AB ≈2 g cm⁻³ — **이 편에 인쇄 0**)를 가정하면 기대비 ≈0.39–0.43. 0 MPa(0.47)만 그 근처이고 나머지는 **×1.7–2.3**.
- ⇒ `[해석]` 저압에서 **LGPS 로 분류돼야 할 부피가 void 로**(또는 고압에서 NCM 이 과대로) 들어갔다. 가장 그럴듯한 기구는 **부분부피**: 미세 LGPS + 1 µm 아래 공극의 혼합 영역이 0.5 µm 화소에서 중간 밝기가 되어 문턱에 따라 void 로 떨어진다. 원문 설명("soft LGPS contract → apparent volume fraction ↓")은 **"apparent"** 라는 단어로 이것을 반쯤 인정한다.
- **이것이 `φ` 에 주는 것**: NCM 경계 화소를 LGPS ↔ void 로 가르는 판정이 같은 문턱에 걸린다. 부피비 흔들림(×2)이 `φ` 효과(×1.10)보다 크다 ⇒ **`φ(P)` 의 압력 추세는 분할 불확실성 안에 있을 수 있다.** 반대 증거: ≤12 ↔ ≥50 MPa 두 무리가 갈라져 보인다(Fig. 3c). 판정: **추세의 방향은 약하게 서고, 크기는 서지 않는다.**

## 5.2 ★★★★ `R_ct × φ` — 곱의 나머지 인자

| P / MPa | `R_ct` (Ω, `[도표]`) | `φ` (`[도표]`) | `R_ct·φ` (Ω) | `R_ct·P` (Ω MPa) | `R_ct·A` (Ω cm², A = π(0.05)² = 7.85×10⁻³ cm²) |
|---:|---:|---:|---:|---:|---:|
| 6 | 8.7×10⁵ | 0.749 | 6.5×10⁵ | 5.2×10⁶ | 6.8×10³ |
| 12 | 4.1×10⁵ | 0.779 | 3.2×10⁵ | 5.0×10⁶ | 3.2×10³ |
| 50 | 1.6×10⁵ | 0.843 | 1.4×10⁵ | 8.1×10⁶ | 1.3×10³ |
| 100 | 0.62×10⁵ | 0.827 | 0.51×10⁵ | 6.2×10⁶ | 4.9×10² |

- `R_ct ∝ 1/(φ·k_eff)` 로 쓰면 **`k_eff` 가 ×13** 이어야 한다. `ln 1.10 / ln 14` ≈ **0.036** — CT 접촉 면적이 `R_ct` 로그 변화의 **≈4 %** 만 설명.
- "inversely proportional to pressure" — `R_ct·P` 가 ×1.6 안에서 일정 ⇒ **대략 참**(4 점).
- 면적 정규화하면 6 MPa ≈7×10³ Ω cm² · 100 MPa ≈5×10² Ω cm² — 16호(97/389 MPa, 양극 10–20 Ω cm²)의 **25–700 배**. 두께(≈0.6 mm) · 2전극 · SOC 미기재가 겹친다.
- ⇒ `[해석]` `k_eff` ×13 의 후보 셋(이 편은 가르지 않는다): ① **해상도 아래 실접촉**(0.5 µm 화소가 "닿음" 이라 부른 면 안에서 원자 접촉 몫이 압력으로 는다 — Hertz 형) ② **계면 화학 `k_p`**(압력이 LiNbO₃ 코팅 · 분해층을 바꾸나) ③ **상대극 In–Li 계면**(2전극 — 5 · 16호가 음극 계면의 강한 압력 의존을 잰 바 있다).

## 5.3 용량 · CE

- Fig. 2b 방전 ×1.6(6 → 100 MPa) · 첫 CE ≈61 → 44 → 27 %. `R_ct` ×14 · `φ` ×1.10 · 공극률 42.5 → 23 %.
- S3 정규화 재현 시도: 기준을 Fig. 2a 셀로 두면(`[도표]` 3 · 5 · 7 · 9 사이클 방전 ≈13 · 7 · 4.5 · 3.5) 비는 ≈1.6 · 2.9 · 4.9 · 4.0 — 인쇄 ≈127 · 156 · 188 · 197 % 와 **안 맞는다**. 기준 셀 미특정(G8) — **재현 불가**.

## 5.4 적재량 · 두께

- `[재현]` NCM 0.476 mg(1.0 mg × 1/2.1) ÷ 7.85×10⁻³ cm² = **60.6 mg cm⁻²** ✓ 인쇄 60 과 일치.
- `[재현]` 복합층 면밀도 127 mg cm⁻², 외부 밀도로 고체 밀도 ≈2.7 g cm⁻³ 가정 → 100 MPa(공극률 23 %)에서 두께 **≈0.6 mm**. ROI 50 µm 는 그 ≈1/12 — 어느 깊이인지 미기재(G3).

---

# 6. ★★★ 25호 ↔ 33호 인용 판정 (사용자 질문)

| 인용 편 | 인용 문장(원문, `[인쇄]`) | Sakka 에서 해당하는 곳 | 판정 |
|---|---|---|---|
| **25호 Zhou 2025** ref 12 | "Sakka et al. employed X-ray computed tomography (CT) to investigate the effect of stack pressure on the CAM-SSE interface. They found that at high pressures (50 MPa), SSE particles filled internal cavities within the cathode composite, significantly improving the contact area fraction compared to conditions at or below 12 MPa, resulting in a notable reduction in charge transfer resistance.12" | §3.4 · §3.7 (Fig. 3c · 6b) | ✅ **선다.** "significantly" 는 ≈+6–9 %p(상대 ≈+8–13 %)에 대한 표현으로 과한 쪽 · "stack pressure" 는 이 편 자신이 "fabrication pressure 에 해당" 이라 한 양 |
| 25호 (다음 문장) | "A model developed to assess the stability of the CAM-SSE contact showed that a pressure of 25 MPa was sufficient to maintain a stable interfacial contact." — **인용 번호 없음** | **없다** — Sakka 에 모델 0, "25 MPa" 는 SI Fig. S3 범례의 가압 단계뿐 | ⚠ **Sakka 의 명제가 아니다.** 우리 25호 digest 가 이 문장을 Sakka 에 붙였다(오귀속) |
| **33호 Zhang 2025** ref [120] | "Adjusting the testing environment to achieve 3D contact between the active material and solid electrolyte has been suggested as a strategy to improve battery performance, particularly under low operating pressures.[120,118]" — §5 압력 **방향** | §3.8 결론 마지막 문장 · §3.5 비등방성 | ✅ **선다.** Sakka 가 "it is expected" 로 쓴 **제언**을 "has been suggested" 로 옮김. "testing environment" 는 Sakka 어휘가 아니다 |

⇒ **두 인용 모두 원문과 맞다 — 같은 편의 다른 절(결과 ↔ 제언)을 인용했을 뿐이다.** 25호 쪽이 측정에 가깝고, 33호 쪽은 측정 없는 제언을 옮겼다.
원장의 "두 인용이 갈리는 것은 원문으로만 풀린다" 는 **풀렸다: 갈린 것이 아니라 나눈 것.** 남은 어긋남은 **우리 쪽**(25호 digest 의 "모델상 25 MPa" 오귀속) 하나다.

---

# 7. ★★★ DEM 보정 목표 판정

| 양 | 압력 점 | 값 형태 | 쓸 수 있나 |
|---|---|---|---|
| 복합층 공극률 | 0 · 6 · 12 · 50 · 100 | Fig. 3b 막대 **인쇄 라벨** 44 / 42 / 39 / 31 / 23 % | ✅ **1순위** — 해상도 아래 공극은 빠진다(과소), 그 한계를 DEM 쪽에 명시 |
| SE 층 공극률 | 같은 5 점 | `[도표]` ≈53 / 41 / 39 / 15 / 4.3 % | ✅ SE 단독 압분 곡선(33호 DEM 후보 Cronau 2021 과 같은 층) |
| 3 상 부피분율 | 같은 5 점 | 인쇄 라벨 | ⚠ 질량수지 결함(§5.1) — **void 합만** 쓰거나 NCM/LGPS 비를 고정해 재배분 |
| 접촉 면적 분율 `φ` | 같은 5 점 | `[도표]` 78.3 / 74.9 / 77.9 / 84.3 / 82.7 % | ⚠ **범위 제약으로만** — "0.5 µm 화소 판정에서 0.75–0.85". DEM 은 접촉 판정을 **간극 ≲0.5–1 µm = 접촉**으로 맞춰야 비교가 선다. 추세 크기는 분할 불확실성 안 |
| 굴곡도 최빈 · 최소 | 같은 5 점, N = 100 경로 | `[도표]` | ⚠ ROI 36 µm 측면 · 기하 경로비 — 약한 목표 |
| 비등방성 | — | 단면 그림 | ❌ 수치 0 |
| 입도 | — | `[인쇄]` NCM "on the order of 10 µm"; `[도표]` SEM S1 구형 ≈5–18 µm · S2 LGPS 부정형 ≈1–8 µm | ⚠ PSD 0 — SEM 한 장씩 |
| 조성 · 공정 | — | `[인쇄]` 1 : 1 : 0.1 wt, 막자 혼합, 일축, Ø 1 mm, **제조 가압 0**, 적재 60 mg cm⁻² | ✅ 명확. ⚠ DEM 에 필요한 밀도 · 탄성률 인쇄 0(ref 37 · 38 로 넘김) |

⇒ **판정: 조건부 보정 목표.** 계보에서 **처음으로 "같은 조성 · 같은 장치 · 단조 가압 5 점" 의 측정 압분 곡선**이 있다 — 25호의 DEM `θ`(계산, 375 MPa 한 점)와 층이 다르다.
그러나 **`θ(P)` 보정 목표로는 아니다** — `θ`(연결 분율) · `u`(통째 비연결)를 보고하지 않았고, `φ` 는 해상도 판정에 묶여 있다. DEM 쪽이 `φ` 를 목표로 삼으려면 **(i) 같은 해상도로 보셀화한 DEM 결과에 같은 3 상 판정**을 거는 방식이어야 한다.
⚠ **이 편의 압력은 제조 압력(최대 압력)이다** — DEM 의 가압 시뮬레이션과는 맞고, **운전 압력(제조 뒤 되돌림)의 `φ` 로 쓰면 안 된다**(S14: 50 → 0 MPa 에서 void 변화 "no clear change" — 되돌림 뒤 구조 보존, 정성).
DEM/MPM 브랜치 파일은 건드리지 않았다 — 판정만 여기와 컴파일 페이지에 둔다.

---

# 8. 37호 "ASSB truth 5 조건" 대조

| 37호 요구 | 이 편 | 판정 |
|---|---|---|
| ① 용량에 곱해지되 `ε_p` 와 별개인 `θ` | CT 가 NCM 부피(= `ε_p` 의 기하판)와 `φ` 를 **따로** 준다 — 그러나 `φ` 는 표면 피복(`A_eff` 쪽)이지 용량에 곱해지는 `θ` 가 아니다 | ⚠ 관측 수준에서 부분 |
| ② 비연결 입자가 자기 SOC 의 리튬을 붙듦 | 사이클 뒤 구조 0 | ❌ |
| ③ 죽은 부피가 전해질이 되지 않음 | 모델 0 | — |
| ④ `θ` 에만 반응하는 조작 | 압력은 공극률 · 겉보기 전도도 · `R_ct` · 상대극을 **같이** 움직인다 | ❌ |
| ⑤ 면적에 비례하는 이중층 | C 값 인쇄 0(S16 회로에 C 둘) | ❌ (재료는 있었다) |
| (38호 ⑥) OCV 관측의 이완 시간 | OCV 0 | — |

⇒ **0.5/5.** 새로 주는 것 — **요구 ⑦ 후보**(`[해석]`): **접촉 판정의 길이 척도**. truth 에 `θ` · `φ` 를 넣을 때 "어느 간극까지를 접촉으로 보나" 가 파라미터여야 한다 — 같은 미세구조가 0.5 µm 판정에서 `φ` ≈0.8 이고, `R_ct` 는 그 판정이 못 보는 척도에서 ×13 움직인다.

---

# 9. ★★★★ 곱 축퇴 처방 — 스물두 번째 적용

셀: NCM111(LiNbO₃) | LGPS | In–Li, 신품, 제조 = 가압 0 → 100 MPa 단조, 2전극.

### 입력 점검

- **1단계 `R_CT·C_dl`** — ⚠ 회로에 C 둘(S16), **값 인쇄 0**. `[도표]` S15 로 꼭짓점 주파수를 읽을 수 없다(주파수 표지 0).
- **2단계 면적 대조군** — ★ **있다, 처음으로 "측정된 면적" 을 가진 채로.** 압력 4 점이 `φ_CT` 를 0.749 → 0.827 로 바꾸고 같은 셀(동시 측정, G2 미확정)의 `R_ct` 가 ×14 변한다. 면적 가설(`R_ct ∝ 1/φ`, `k` 불변)의 예측 ×1.10 ↔ 관측 ×14 ⇒ **면적 가설 기각, 적어도 CT 척도의 면적으로는.**
- **3단계 `Ea`** ❌ 298 K 한 점.
- **4단계 `C` 상한** ❌ `C` 0.
- **율 스윕 줄** ❌ 0.01 C 한 율.
- **외부 기준 줄** — 없음.

### ★★★★ 이 적용이 처방에 더하는 것

1. **2단계의 실측 실패 형태** — 면적을 **재고도** 곱이 안 풀린다. `φ_CT` 는 `A_eff` 의 **해상도 한정판**이고, `A_eff = φ_CT × (해상도 아래 실접촉 몫)` 으로 한 겹 더 쪼개진다. `R_ct` 가 보는 것은 뒤 인자 × `k_p` × (상대극)이다.
   ⇒ 처방 표에 새 줄 후보: **"면적을 영상으로 쟀다면 영상의 길이 척도를 적고, `R·φ` 가 일정한지 먼저 본다"** — 일정하면 면적 채널, 아니면 곱의 나머지.
2. `[해석]` 18호 "composition **or** contact area" 의 **데이터판 판정**: 이 편에서는 (CT 척도의) contact area 가 아니다 — 나머지(`k_p` · 미세 접촉 · 상대극)다. 단 셋 중 무엇인지는 이 편이 가르지 않는다.
3. **압력 연산자의 비직교성 재확인** — 11호(Yu)가 붙인 "연산자가 직교하지 않는다" 에, 압력이 **공극률 · 전도도 · 양극 계면 · 상대극 계면**을 한꺼번에 움직이는 실측 하나.

### ⚠ 이것이 곱을 푼 것은 아니다

점당 n = 1 · 분할 질량수지 결함 · 2전극 · `R_ct` 적합표 0 · 고압 두 점은 Nyquist 호와 ×2–3 어긋남(D8). 기여는 **"면적을 재도 안 풀린다" 는 형태**와 그 **크기(×13)** 다.

---

# 10. Q5 — 열다섯 번째 형태 "상대극 계면을 양극 접촉 면적에 흡수한다"

2전극 In–Li | LGPS | NCM 에서 `R_ct` 를 **전부 NCM/LGPS 접촉**에 배정한다(`[인쇄]` "a good NCM/LGPS interface is formed, which leads to a decrease in the charge-transfer resistance"). In–Li 는 조립 방법 한 줄 외에 전위 · 임피던스 · 압력 거동 언급 0(`indium` 1 회 = 재료 목록).
`[해석]` 같은 나사 압력이 In–Li | LGPS 계면에도 걸린다 — 5호(Li 금속, 1 → 25 MPa 에서 >500 → 32 Ω) · 16호(3전극, 음극 4 ↔ 9 Ω cm²) · 25호(`R_anode` ×1.7–1.8)가 음극 계면의 압력 의존을 이미 쟀다. 이 편의 ×14 가 얼마만큼 상대극인지 모른다.
Q5 칸 이동 없음.

---

# 11. 채움표 행 (Q1–Q8)

| Q | 판정 |
|---|---|
| **Q1 정량** | **+0.5 — 계보 첫 3D 측정 표면 피복 `φ(P)`**(CT, 화소 0.5 µm, 5 압력, 신품): `[도표]` 78.3 / 74.9 / 77.9 / 84.3 / 82.7 %. 분모 = NCM 표면(`[인쇄]`). **`θ` 아님 · `u` 아님 — 37호 기준 `A_eff` 쪽 손잡이.** 반 칸: 신품(**`θ(N)` 0/39**) · 압력 = 제조 압력 · n = 1 · 오차 0 · 분할 문턱 0 · **분할이 질량을 안 보존(NCM/LGPS 부피비 0.47 → 0.97, ×2 — `[재현]`)** · 해상도 판정이라 0 MPa(공극률 44 %)에서도 `φ` ≈0.78. 18호(면적 **비** 하나, Image-J)·22호(XRD 불활성 상한)와 다른 층: **절대 분율 · 3D · 압력 함수** |
| **Q2 독립관측** | 이동 없음(**반 칸 검토 후 접음**) — CT 는 전기화학과 독립인 접촉 관측이지만 신품이라 가를 `LAM_PE` 가 없다(19호 선례와 같은 이유) |
| **Q3 라벨층위** | 층 하나 — **measured-imaging with unreported segmentation threshold, phase ratio not conserved** (3 상 판정 · 문턱 · 민감도 0 · 질량수지 ×2) + **fitted ECM `R_ct`(적합표 0, 고압 두 점 Nyquist 호와 ×2–3)** · 오차 막대 0 |
| **Q4 유일성** | **0/39 — 서른한 번째 성질 "곱의 한 인자를 직접 재고, 나머지 인자가 변화의 96 %(로그)를 가져가는 것을 같은 지면에 둔 채 '대응한다' 로 읽었다"**(`[재현]` `R_ct·φ` ×13). `uncertaint` · `error` 0 |
| **Q5 Li-In** | 이동 없음 — **열다섯 번째 형태 "상대극 계면을 양극 접촉 면적에 흡수한다"**(§10) |
| **Q6 압력** | **+0.5 — 계보 첫 "압력 → 측정 양극 구조 → 측정 저항" 사슬**: 로드 트랜스듀서 감시 · CT 5 점 · EIS 4 점(CT 와 동시) · 용량(다른 셀 3 점 + 같은 셀 5 단계). 제조 ↔ 스택 압력을 **정의로 가르고 자기 실험에서 같다고 명시**(`[인쇄]` "no pressure was added during fabrication … corresponds to … fabrication pressure"). 반 칸: 단조 가압만(되돌림 전기화학 0 · S14 정성 1 장) · n = 1 · S3 압력 ↔ 사이클 교락 · 2전극 |
| **Q7 dead Li** | 해당 없음(In–Li) |
| **Q8 화학·OCP** | 이동 없음 — NCM111(LiNbO₃) | LGPS, OCP · `∂E/∂x` 0. `[재현]` 첫 CE 61 → 27 %(압력 ↑ ⇒ 충전 과대, LGPS 산화 분해 `[인쇄]`) — 압력이 **SE 분해 몫**도 키운다(언급 0) |

---

# 12. 어긋남 (실제로 어긋난 것만)

| # | 어디 | 무엇 |
|---|---|---|
| D1 | p5 | "increase in the capacity … (**Fig. 1**)" — Fig. 1 은 셀 모식도. 용량은 Fig. 2 |
| D2 | p5 | "contact area fraction … as shown in **Fig. 3b**" — `φ` 는 Fig. 3c. 3b 는 부피분율 |
| D3 | 결론 ↔ 본문 | 본문: Z(가압 = 수직) 접촉 양호 · **수평** 불량. 결론: "marginally perpendicular … improving the contact interface in the **vertical** direction" — 방향 어휘 반전(초록 "in a plane perpendicular to the pressure direction" 은 본문과 맞게 읽힌다) |
| D4 | p4 ↔ Fig. 3c | "increases by approximately 10%" — `[도표]` ≤12 MPa 74.9–78.3 → ≥50 MPa 82.7–84.3: 평균 +6.5 %p · 최대 +9.4 %p. 그리고 **비단조**(0 → 6 MPa −3.4 %p · 50 → 100 MPa −1.6 %p) 를 본문이 말하지 않는다 — "two-stage" 서사(1 단계 = 접촉 불변)와 6 MPa 하락이 긴장 |
| D5 | p5 | "inversely proportional to the pressure" — `[재현]` `R_ct·P` 5.0–8.1×10⁶ (×1.6). 대략 |
| D6 | Fig. 3b ↔ 조성 | 고정 1 : 1 : 0.1 wt 혼합물의 NCM/LGPS 부피비 0.47 → 0.97 → 0.75 (§5.1). 원문은 LGPS 수축으로 설명 |
| D7 | p3 · S3 | "The observed capacity also increases with respect to the applied pressure" ↔ S3a 절대 방전 12 → 100 MPa 에서 ≈21 → ≈14 (감소). S3b 의 증가는 **다른 셀 대비 정규화** 안에서만 · 기준 셀 미특정 · 재현 불가 |
| D8 | Fig. 6b ↔ S15 | 50 · 100 MPa 호 지름 `[도표]` ≈70 · ≈20 kΩ ↔ `R_ct` ≈160 · ≈60 kΩ (×2–3). 6 · 12 MPa 는 맞다 |
| D9 | 결론 | "logarithmic increase of the capacity" — 적합 · 근거 그림 0; Fig. 2b 는 3 점, S3b 는 정규화 5 점 |
| D10 | 초록 · 제목 ↔ p3 | "stack pressure" / "applied pressure" 로 부르는 변수가 `[인쇄]` "corresponds to the previously reported **fabrication** pressure" — 서론이 가른 두 양을 결과에서 하나로 쓴다(명시는 했다) |
| D11 | 참고문헌 | **ref 23 = ref 41** (Fathiannasab 외 *JES* 2020, 167, 100558 — 저자 표기만 "A. G. Kashkooli" ↔ "A. Ghorbani Kashkooli" 로 다른 중복) |
| D12 | Fig. 2b ↔ S3a | 6 MPa 첫 방전 ≈27 ↔ ≈35 mAh g⁻¹ — 같은 조건 다른 셀 ≈30 % 차(산포 대용, 효과 ×1.6 과 같은 자릿수) |

---

# 13. 그림 — 무엇을 봤나

크로퍼 **23 장**(본문 7 + SI 16). **15 장 봤다**: 본문 **Fig. 1 · 2 · 3 · 4 · 5 · 6**, SI **S1 · S2 · S3 · S4 · S7 · S13 · S14 · S15 · S16**.
**안 본 것 8 장**: Fig. 7(모식 — 서술만 옮김) · S5 · S6(SE 층 · 단면 재구성) · S8–S11(6 · 12 · 50 · 100 MPa 분할 — 0 MPa 판 S7 만 봤다) · S12(LFP).
본문과 어긋난 그림: **Fig. 3c**(비단조 · "≈10 %") · **Fig. 3b**(질량수지) · **S3a ↔ S3b**(절대 ↔ 정규화) · **S15 ↔ Fig. 6b**(고압 두 점).
단위 확인: p2 · p3 를 렌더링해 **0.5 µm · 512 × 512 × 50 µm³** 를 눈으로 확인(추출 텍스트는 "mm").

---

# 14. 참고문헌 중 후속 후보 (44 편 중, 서지 기준 — 미열람)

| 서지 (원문 인쇄) | ref | 왜 | 축 |
|---|---|---|---|
| **Wang, Kazyak, Dasgupta, Sakamoto, *Joule* 2021, 5, 1371–1390** | 22 | "upper limit of the stack pressure is suggested to be **1 MPa practically**" — 계보 요구치(0.4–5 MPa, 원전 0)에 **처음 지목된 원전** | Q6 |
| **Ohashi, Kodama, Sun, Hori, Suzuki, Kanno, Hirai, *J. Power Sources* 2020, 470, 228437** | 24 | "strain caused by the pressure reduces the contact between the AM and SE" · "NCM particles are pressurised preferentially" — 이 편 기구 서술의 근거 둘 다 | Q1 · Q6 · DEM |
| **Ohashi, Kodama, Horikawa, Hirai, *J. Power Sources* 2021, 483, 229212** | 25 | "larger pressures can be applied to materials that have larger Young's moduli" · CT 3D 구조 — Young 률 차 압분 | DEM |
| **Fathiannasab, Zhu, Chen, *J. Power Sources* 2021, 483, 229028** | 18 | CT 로 AM/SE 전극 구조 · 압력 변형이 접촉을 줄인다 | Q1 · Q6 |
| **Doux, Yang, Tan, Nguyen, Wu, Wang, Banerjee, Meng, *J. Mater. Chem. A* 2020, 8, 5049–5055** | 15 | 제조 압력 50 ↔ 150 MPa 용량 — 5호(Doux *AEM* 2020 = 이 편 ref 26)와 **다른 논문** | Q6 |
| Neumann, Randau, Becker-Steinberger, Danner, Hein, Ning, Marrow, Richter, Janek, Latz, *ACS AMI* 2020, 12, 9277–9291 | 34 | CT 3D 구조 + 시뮬레이션 — ⚠ 큐 55 Neumann **2021** *ACS AEM* 과 **다른 논문** | Q1 |
| Zhang, Weber, Weigand, Arlt, Manke, Schröder, Koerver, Leichtweiss, Hartmann, Zeier, Janek, *ACS AMI* 2017, 9, 17835 | 12 | 원장 ★★★★ 에 이미 있음(토모그래피 · 7:3 조성) — 지목 +1 | Q1 · Q2 |
| Nam, Oh, Jung, Jung, *J. Power Sources* 2018, 375, 93 | 13 | 원장 ★★ 에 이미 있음 — 지목 +1. ⚠ 큐 42 Nam 2018 *JMCA* 와 **다른 논문** | Q1 |
| Froboese 외 *JES* 2019, 166, A318 | 39 | 37호 후속에도 있음(brug 3.67) — 지목 +1 | Q2 |
| Minnmann 외 *JES* 2021, 168, 040537 | 40 | 2호가 기댄 편 — 굴곡도 문헌값 | Q2 |

큐 41–59 에 있는 편: **0**(Neumann · Nam 은 이름이 같은 다른 논문).

---

# 15. 이 digest 가 주장하지 않는 것

- **`φ(P)` 의 추세가 가짜라고 주장하지 않는다.** 주장은 **분할의 질량수지 흔들림(×2)이 `φ` 효과(×1.10)보다 크고, 문턱이 인쇄되지 않아 크기를 믿을 근거가 지면에 없다**는 것까지다.
- **`R_ct` 의 ×14 가 상대극이라고 주장하지 않는다.** 후보 셋(해상도 아래 접촉 · `k_p` · 상대극) 중 이 편이 아무것도 가르지 않았다는 것까지다.
- **질량수지 기대비 0.39–0.43 은 이 편의 값이 아니다** — 외부 일반 밀도 가정. 그러나 **"비가 압력에 불변이어야 한다" 는 밀도와 무관**하다.
- **이 편의 `φ` 를 운전 압력의 `φ` 로 옮기지 않는다** — 제조 압력(최대 압력)의 함수다.
- **25호 원문(Zhou)이 틀렸다고 주장하지 않는다** — Zhou 의 "25 MPa 모델" 문장은 인용 번호가 없을 뿐이고, 그것을 Sakka 에 붙인 것은 우리 25호 digest 다.
- 그림 판독값(`[도표]`)은 전부 ≈ 이고, Fig. 3c 는 ±0.3 %p, `R_ct` 는 ±0.2×10⁵ Ω 정도로 읽었다.
