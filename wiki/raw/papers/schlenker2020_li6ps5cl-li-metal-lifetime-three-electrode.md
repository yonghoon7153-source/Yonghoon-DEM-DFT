---
title: "Schlenker, Stępień, Koch, Hupfer, Indris, Roling, Miß, Fuchs, Wilhelmi, Ehrenberg 2020 — Understanding the Lifetime of Battery Cells Based on Solid-State Li6PS5Cl Electrolyte Paired with Lithium Metal Electrode (ACS Appl. Mater. Interfaces 12, 20012)"
source_url: local-upload/8._Understanding_the_Lifetime_of_Battery_Cells_Based_on_Solid-State_Li6PS5Cl_Electrolyte_Paired_with_Lithium_Metal_Electrode.pdf
source_url_note: "본문 PDF 14 쪽(논문 11 쪽 + 저자 정보 · 참고문헌 59), SI 없음. 크로퍼 11 장(본문 그림 11) 중 7 장을 봤다(Fig. 1 · 2 · 3 · 4 · 6 · 7 · 8), 안 본 것 Fig. 5 · 9 · 10 · 11. 렌더 확인 p3 주파수 · p5 전기용량 지수."
source_doi: 10.1021/acsami.9b22629
source_license: "(c) 2020 American Chemical Society — 오픈액세스 표기 없음"
pdf_sha256: 2c6367325b20826d21012114532da971e26a3b169a2dacc3fd1a96ab9fa7b409
ingested: 2026-09-23
sha256: 8f9245f4a26fc035d8f4ea407cf308c46cba3de974b06942f7d8af37277a2d7d
---

# 수집 목적

`assb` 섹션 **46호**. 큐 **47번**(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g, 2차 묶음 여덟째 편).
닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q5**(기준극 계보)와 **Q7**(Li 금속 음극).

지목 경위: 21호(Sedlmeier 2023) 가 ref 17 로 이 편을 "EIS 에 기준극을 쓴 선례" 셋(Dugas 2021 · **Schlenker 2020** · Ikezawa 2020) 중 하나로
꼽으며 `[인쇄]` "representing a pseudo-RE for EIS measurements" 로 분류했고, 21호 digest 가 `[추론]` **"Schlenker 2020 → Hertle 2023 →
16호(Ramanayagam 2026) 로 이어지는 Marburg 계열 금 도금 W 선"** 을 세웠다. 원장(`ASSB_WANTED_PAPERS.md`) 은 이 편을 Hertle 행에 병합해
"'0 V 로 놓은 리튬화 금선' 관례의 출처" 후보로 두었다. **45호(Hertle) 가 그 계보의 가운데 고리를 끊었다** — Hertle 은 Giessen 이고 참고문헌에
Schlenker 가 없다. 이 편은 계보 판정의 마지막 조각이다: **이 편이 기준극을 실제로 썼는가, 썼다면 영점을 무엇으로 정했는가.**

소속: **KIT IAM**(Schlenker · Stępień · Indris · Ehrenberg) + **Robert Bosch GmbH**(Stępień · Koch · Hupfer · Fuchs · Wilhelmi) +
**Univ. Marburg**(**Roling · Miß**). 자금 Bosch. ★ **Roling 과 Miß 는 16호(Ramanayagam, Miß, … Roling 2026)의 공저자이기도 하다.**

> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

---

# 판정 (먼저)

## (1) Q5 — 기준극을 썼나, 영점은 무엇인가

| 물음 | 이 편 | 판정 |
|---|---|---|
| **3전극 · 기준극을 실제로 썼나** | **썼다.** `[인쇄]` "For the reference cell, a tungsten wire plated with gold was placed in the middle of the electrolyte powder prior to densification" · "A gold-plated tungsten reference wire is placed in the middle of the electrolyte pellet" | ✅ Au 도금 W 선, **분말에 묻어 540 MPa 로 함께 압착**(매립형) — 16호 · 45호와 **같은 하드웨어 계열** |
| **리튬화** | `[인쇄]` "Initially, the reference wire is plated with lithium from both electrolytes [sic — electrodes] to reach a constant potential of the reference" | 전류 · 시간 · 전하 · 선 지름 · Au 두께 **전부 미인쇄**. 평탄 · 사다리 그림 **0** |
| **영점(0 V vs Li?)** | **인쇄된 기준 전위 값이 없다.** `0 V` 1 회는 대칭셀 OCV("the open circuit voltage is 0 V") · 기준극 대비 전위 축 그림 **0** · 기준극은 **EIS 분할에만** 쓰였다(Fig. 4) | ★★★★ **"0 V 로 놓은 리튬화 금선" 관례는 이 편에서 나오지 않았다** — 이 편은 영점을 쓰지 않는다 |
| **검증 · 표류 · 누설** | `leak` · `drift` · `calibrat` **0** · `stabl*` 1(무관 — "most stable cell") · "constant potential" 1 회(목표 서술, 값 · 그림 0) | 누설 직접 측정 **0/46** · 표류 수 0 · 반복 0 |
| **왜 영점이 필요 없나** `[해석]` | Li\|Li₆PS₅Cl\|Li **대칭셀**이고 기준극도 두 Li 전극에서 도금한 Li 다 — **같은 금속 셋**. 측정은 AC 임피던스(WE–RE)라 기준극의 DC 값이 결과에 들어가지 않는다. 필요한 것은 측정 동안의 **안정성 · 낮은 기준극 임피던스**뿐이고, 그것도 지면이 보이지 않는다 | Q5 **스물두 번째 형태 "영점이 들어가지 않는 자리 — 같은 금속 대칭셀의 AC 분할 전용"** |
| **대신 남은 기준극 흔적** | `[인쇄]` 도금 쪽 반쪽(Fig. 4c) "some inductive contributions are observed that interfere with the bulk, grain boundary, and interface resistance which makes a separation of these resistances impossible" | `[해석]` 반쪽 **하나에만** 있는 유도성 → 45호 줄 "반쪽에만 있는 호는 기준극 채널 artifact 부터" 의 후보(원문은 원인 무언급) |

## (2) ★★★★ 21호 추정 계보 "Schlenker → Hertle → 16호" — 최종 판정

| 고리 | 근거 | 판정 |
|---|---|---|
| **인용 사슬** Schlenker → Hertle | 45호: Hertle 참고문헌 40 편에 Schlenker 0 · Hertle 의 금선 선례는 Solchenbach 2016(액체, 큐 48) 하나 | ❌ (45호) |
| **영점 관례** "0 V 리튬화 금선" | 이 편: 기준 전위 값 **0** · 0 V vs Li 문장 0 | ❌ — **0 V 의 원전은 Hertle(Giessen) 하나**이고 16호는 그것을 인용 [24] 으로 가져갔다(16호 digest) |
| **하드웨어** Au 도금 W 선 · 매립 · 제자리 Li 도금 | 이 편(2019-12 투고) · Hertle(2023, ∅10 µm) · 16호(2026, ∅25 µm) 셋 다 같은 선 종류 | ✅ 같은 계열 — 이 편이 **우리 계보에서 가장 이르다** |
| **저자 사슬** Marburg | 이 편 공저자 **Roling · Miß**(Marburg) = 16호 공저자 **Miß · Roling**. `[인쇄]` 감사의 글 "developing the three-electrode reference cell" 의 두 사람(Okumus · Koc)은 소속 미인쇄 | ✅ 저자 겹침은 지면 사실. 16호가 이 편을 **인용했는지는 우리 16호 digest 에 기록이 없다**(미확인) |

⇒ **판정: 21호의 한 줄 계보는 두 줄이 합쳐진 것이다.**
**하드웨어 · 저자 줄**(이 편 2020, Roling · Miß → 16호 2026, Roling · Miß — 같은 Au 도금 W 선) 과
**영점 줄**(Hertle 2023 Giessen → 16호, 인용 [24]) 이 **16호에서 처음 만난다**. 이 편은 영점을 준 적이 없고, Hertle 은 이 편을 거치지 않았다.
`[해석]` 그래서 16호의 기준극은 **Marburg 의 선을 Giessen 의 영점으로 읽은 것**이고, 이 편에서 그 선이 쓰인 자리(같은 금속 대칭셀 · AC 전용)는
**영점을 요구하지 않는 유일한 자리**였다 — NMC 상대 · DC 전위 축으로 옮긴 16호에서 처음 영점이 필요해졌고, 그때 가져온 것이 Hertle 의 0 V 다.
21호의 분류("pseudo-RE for EIS") 는 **실질이 맞다**.

## (3) Q7 — Li 금속 음극의 수명을 무엇이 정하나, 단락을 어떻게 판정했나

| 물음 | 이 편 | 판정 |
|---|---|---|
| **저자 결론(기구)** | `[인쇄]` 초록 "A main factor for the lifetime … is the buildup of a lithium vacancy gradient, leading to voids which decrease the interface area and therefore increase the local current density" + 씨앗형 도금(적음 · 많음 → 국소 전류밀도 ↑ → 덴드라이트 단락) | 기구 **셋 중 "계면 면적 손실"** 을 주로, SEI 를 부로, **Li 소모는 다루지 않는다** |
| **SEI 는** | XPS 깊이 분석: 전해질 쪽 이전 계면 = 기준 스폿과 차이 없음 · 집전체 쪽 잔류 Li 에 Li₂S 상대량 ↑, 그러나 `[인쇄]` "the absolute S 2p intensity is also very low (<6 at. %)" · Li₃P "barely seen" | "questionable if such a minor amount leads to such a high overvoltage increase" — **SEI 기각이 아니라 보류**(`[인쇄]` "A SEI should not be neglected") |
| **단락 판정** | `[인쇄]` "**A sudden voltage drop indicates a short circuit.**" — 그것이 **유일한 기준**. 임피던스 확인 · 사후 단면 · 전자 전도 측정 **0**. 덴드라이트 영상 **0**(ToF-SIMS 는 강판 위 씨앗) | ⚠ 단락은 **전압 모양 판정** |
| **`[도표]` 붕괴의 모양** | Fig. 1a–d 에서 "단락" 뒤에도 전압이 곧바로 0 이 아니다 — a ≈+3 mV · b ≈+2 mV 계단이 남고, c 는 −5 → −10 mV 계단 뒤 0, d 는 마지막 음 반주기가 −9 → −5 mV 로 줄다 0 | `[해석]` **한 계단이 아니라 여러 계단** — 완전 단락 전에 부분 전자 경로가 있었다는 모양과 양립 |
| **정상 열화 ↔ 단락 구분** | 정상 = 정전류 중 과전압 **상승**(Fig. 1f 정의) · 단락 = 급락. **완만한 하강은 둘 다 아니다**: `[인쇄]` Fig. 1d "the overpotential of the negative voltage curves decreases over stripping and plating" · Fig. 7 파랑의 하강을 "plated onto the steel current collector … enlarges the lithium active area and results in a potential drop" 으로 **면적 증가**에 배정 | ⚠ **연성 단락(병렬 전자 경로)을 가르는 신호가 지면에 없다** — `soft` 0 · `leak` 0 |
| **`[도표]` 수명 전 구간의 계단 크기** | 단락 수십 시간 전부터 반주기 전압이 **줄어든다**: d +13/−15 → +9.5/−9.3 mV(×≈0.7) · c +20/−22 → +17/−20 · b +33/−31 → +25/−27 · a 봉우리 +35/−30 → +32/−24 | `[해석]` 접촉 개선과 **연성 단락 병렬 경로**가 같은 서명(겉보기 저항 ↓)을 낸다. **대칭셀은 OCV 가 구조적으로 0 V** 라 연성 단락의 고전 서명(개방회로 자기방전 · OCV 감쇠)이 **원리적으로 안 보인다** — 41호(CE 저하 = 연성 단락 누설)보다 한 층 더 나쁜 자리 |
| **쿨롱 효율 · `LLI` 대리** | `Coulomb*` · `efficien*` · `LLI` **0** — 대칭셀이라 CE 개념이 없다(`[인쇄]` "no real charging and discharging process takes place") | CE → `LLI` 통로 **없음**. `[재현]` 한 전극의 순 이동 ≤ 반주기량(최대 12.4 µg ≈ 박 재고의 2.4–3 %) — **Li 소모는 수명 제한 기구가 아니다**(이 셀 설계에서) |
| **dead Li ↔ SEI Li** | `dead` 0 · `isolat*` 1(강판 위 "small isolated seeds") · Li 재고 수지 0 | Q7 칸 이동 없음 |

## (4) 칸 이동 — **≈19.5 → ≈19.5 (새 칸 0)**

- **Q5 반 칸 검토 후 접음**: 기준극은 있으나 **기준 전위에 관한 측정 · 명제가 0**(`[인쇄]` "constant potential" 은 목표 서술). 계보 판정(두 줄의 합류)은
  **저자 목록 · 인용 목록 대조 = 우리 판독**이고 논문 명제가 아니다 → 칸이 아니라 형태 하나(스물두 번째).
- **Q7 이동 없음**: Li 대칭셀(무음극 아님). SEI 는 XPS 로 **찾으려 했고 뚜렷하지 않았다**(정량 = 원소 at% 뿐) · dead Li 수단 0.
- **Q2 반 칸 검토 후 접음**: 음극 계면에서 "면적 ↔ SEI" 를 **XPS(화학) + 3E EIS(전극 분해) + 면적 비대칭 셀(Fig. 7) + 압력(Fig. 6, 다른 SE)** 네 채널로 **논증**했지만,
  저자 스스로 `[인쇄]` "Still it is an open question if this effect of interface area is stronger than the influence of the SEI" — 가르지 않았다. 양극 `LAM` 대상 0.
- Q1 `θ(N)` **0/46**(양극 없음) · **Q4 0/46 — 서른여덟 번째 성질** · Q6 이동 없음(층 하나) · Q8 해당 없음.

## (5) 가장 날카로운 것 넷

1. ★★★★ **계보 판정 — 두 줄의 합류.** 하드웨어 · 저자(Marburg: 이 편 → 16호) 와 영점(Giessen: Hertle → 16호) 이 16호에서 처음 만난다. 이 편은 영점을 쓴 적이 없다.
2. ★★★★ **저자가 "A 또는 B" 를 인쇄하고, 두 갈래를 같은 이름으로 적었다.** `[인쇄]` "An increase of interface resistance can be highly correlated **either** with a decreasing interface area … as R ∼1/A **or** an ionically insulating SEI formation at the interface, **leading to a decreasing active contact area** for lithium stripping." — 두 가설이 둘 다 **"활성 접촉 면적 감소"** 로 끝난다. `[해석]` 계면 저항은 **기하 접촉 × 화학 통과 분율**의 곱만 본다 — 카드 곱 축퇴(`A_eff` ↔ `k`)의 **Li 음극 판**이고, 저자가 문장 안에서 그 곱을 한 이름으로 합쳤다.
3. ★★★ **Li 대칭셀에서는 연성 단락이 원리적으로 안 보인다.** OCV ≡ 0 V 라 개방회로 신호가 없고, 정전류 중 겉보기 저항 하강은 접촉 개선과 병렬 전자 경로가 같은 부호로 만든다. 이 편의 판정 기준은 "급락" 하나이고, 단락 전 수십 시간의 계단 크기 감소(`[도표]` ×≈0.7)는 설명되지 않은 채 남는다.
4. ★★★ **`[재현]` 지면의 세 숫자가 인쇄된 Li 면적(∅4 mm, 0.126 cm²) 이 아니라 ≈0.16 cm²(∅≈4.5 mm) 에서 맞는다** — Fig. 8 반주기 Li 양(1.0 µg = 0.30 mA cm⁻² × 5 min ⇒ 0.154 cm² · 6.2 µg = 0.15 × 60 min ⇒ 0.160 cm²) · Fig. 4b 가로축(아래 D2) · "about 6 MPa"(0.1 kN / 0.16 cm² = 6.3 MPa; 0.126 cm² 면 8.0 MPa). `[해석]` 압착 뒤 Li 박이 퍼진 면적 — 원문 무언급.

---

# 0. 원문에 없어서 확인이 필요한 것

- **기준극**: W 선 지름 · Au 두께 · 리튬화 전류/시간/전하 · 도달 전위 · 기준극 임피던스 · 측정 전후 안정성 · 반복 셀 수. 감사의 글의 두 사람(Okumus · Koc) 소속.
- **EIS 조건(대칭셀)**: 진폭(주 셀 미인쇄 — 유리 SE 셀만 10 mV) · **DC 전류를 흘리면서 쟀는지**(Fig. 4 캡션 "during the application of a constant current" — 그렇다면 DC 중첩 EIS 의 안정성 조건 미기재) · 스펙트럼 간격(`[재현]` 6 분 — D2).
- **온도**: 주 셀(Li₆PS₅Cl) 시험 온도 **미인쇄**. 유리 SE 펠릿 제조만 "room temperature".
- **전류밀도의 기준 면적**: Li ∅4 mm(0.126 cm²) 인가 압착 뒤 면적인가 — 지면의 수가 ≈0.16 cm² 를 가리킨다(판정 (5)-4).
- **Fig. 8**: 셀 수 · 오차 막대 정의(표준편차? 범위?) · "Total lithium amount" 가 한 방향 누적인가 양방향 합인가.
- **Fig. 1e**: 어느 셀들인가(a–d 와 가로축 범위가 안 맞는다 — D6) · "overpotential" 이 f 의 어느 양(초기 · 상승분)인가.
- **Fig. 7**: 두 Li 판의 크기 · 전류(전류밀도를 어느 면적에 맞췄나) · 시작 0.5 h 이전 구간.
- **단락 확인**: 임피던스(저주파 실수축 수렴) · 해체 · 단면 — 전부 0.
- **운전 압력 장치**: "constant force of 0.1 kN" 을 무엇으로 걸었나(스프링? 추?).

---

# 1. 서지 · 낱말 지문

**Ruth Schlenker\*, Dominik Stępień, Pascal Koch, Thomas Hupfer, Sylvio Indris, Bernhard Roling, Vanessa Miß, Anne Fuchs, Martin Wilhelmi,
Helmut Ehrenberg** — "Understanding the Lifetime of Battery Cells Based on Solid-State Li₆PS₅Cl Electrolyte Paired with Lithium Metal Electrode",
*ACS Appl. Mater. Interfaces* **2020**, 12, 20012–20025. DOI `10.1021/acsami.9b22629`. Research Article, 투고 2019-12-14 · 수락 · 게재 2020-04-06.
오픈액세스 표기 없음(© 2020 ACS). 14 쪽(본문 11 쪽 + 저자 정보 · 참고문헌 59). **SI 없음**(지면에 Supporting Information 항목 0).
교신 Ruth Schlenker(KIT IAM, `partner.kit.edu` — Bosch 파트너 계정). "The authors declare no competing financial interest." 자금 Robert Bosch GmbH.

**낱말 지문** (NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문 = 참고문헌 전, 쪽머리 · 쪽번호 줄 제거):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | **14** |

- NFKC 변경 본문 **136 자**(`ﬁ` 70 · `ﬀ` 44 · `ﬂ` 16 · `ﬃ` 6) — 열 변화 0. 소프트 하이픈 0. 줄끝 하이픈 **24 곳**(이어도 열 변화 0; 하이픈을 살리면 `three-electrode` 4 → 5 · `constant-current` · `Warburg-short` · `lithium-stripping` 은 진짜 하이픈).
- ⚠ 추출에서 **음수 지수 부호가 빠지는 곳**이 있다 — "10^10 F/cm²" 는 **렌더링으로 확인한 결과 인쇄 자체가 양의 지수**다(D4). "10^6 and 10^−1 Hz" 는 렌더 확인(10⁶ Hz – 0.1 Hz).
- `contact loss` 1 = `[인쇄]` "Our reference electrode results suggest a **partial lithium contact loss** at the lithium stripping side" — **Li 음극** 접촉(양극 아님).
- `MPa` 14 = 제조 540(LPSCl 펠릿) · 265(유리 SE 펠릿) · **운전 "only about 6 MPa"** 1 · 압력 스윕 4.4–44.2(본문 3 · 캡션 2 · "8−44" 1) · 문헌 경도 2 · 6 · 49 · 200 · 600(5).
- **Q5 보조**: `reference` 17(기준극 11 — 감사의 글 1 포함 · XPS 기준 스폿 6) · `gold` 2 · `tungsten` 2 · `three-electrode` 4(+1 줄끝) · `leak` **0** · `drift` **0** · `calibrat` **0** · `stabl*` 1(무관) · `constant potential` 1 · `0 V` 1(대칭셀 OCV) · `assum*` 5(기준 전위 0 — XPS · 문헌 가정 · Fig. 7 · 강판 모형).
- **Q7 보조**: `short circuit` 7 · `short-circuit*` 1 · `sudden` 1 · `dendrit*` **27** · `void*` 9 · `SEI` **30** · `soft` **0** · `Coulomb*` **0** · `efficien*` **0** · `dead` **0** · `isolat*` 1 · `lifetime` 20 · `cell failure` 11 · `critical` 0 · `Sand` 1(Sand's time, 서론).
- **곱 축퇴 보조**: `contact area` **19** · `interface area` **14** · `area` 63 · `capacit*` 16(용량 "capacity" · "capacities" = 전기용량 포함) · `pressure` 27 · `Vickers` 11 · `hardness` 13 · `Warburg` 26 · `fit*` 5 · `error` 0 · `reproducib*` 0 · `identical` 4 · `inductive` 1.
- `[해석]` **낱말 쪽에서 본 이 편**: 식별성 어휘 0 · 기준 전위 어휘 0 · 대신 **"면적" 어휘가 계보에서 가장 짙다**(`contact area` 19 + `interface area` 14) — 그런데 **면적을 잰 적은 없다**(R ∼ 1/A 추론 · 면적을 바꾼 셀의 크기 미인쇄).

---

# 2. 셀 · 실험 (`[인쇄]`, 괄호 안 `[재현]`)

| 항목 | 값 |
|---|---|
| SE | Li₆PS₅Cl(NEI Corp. 구매) 100 mg → ∅10 mm × 750 µm 펠릿, **4.3 t = 540 MPa**, PEEK 다이 (`[재현]` 4.3 t × 9.81 / 78.5 mm² = 537 MPa ✓ · 겉보기 밀도 100 mg / 0.0589 cm³ = **1.70 g cm⁻³** — D13) |
| 전극 | Li 박(Honjo) **∅4 mm × 60 µm**, 펠릿 양면 압착 (`[재현]` 재고 0.126 cm² × 60 µm × 0.534 g cm⁻³ = **403 µg** · 면적 0.16 cm² 면 513 µg) |
| 셀 | 글러브박스(O₂/H₂O < 0.1 ppm) · **파우치** · 일정 힘 **0.1 kN** · `[인쇄]` "the applied pressure during these experiments was very small (only about 6 MPa)" (`[재현]` 0.1 kN / 0.126 cm² = 8.0 MPa · / 0.785 cm²(펠릿) = 1.3 MPa · / 0.16 cm² = 6.3 MPa) |
| 기준극 셀 | Au 도금 W 선을 **SE 분말 가운데에 두고 압착 전** 매립 · 두 Li 전극에서 Li 도금 |
| EIS | Gamry Interface 5000 · **10⁶–10⁻¹ Hz** · 진폭 미인쇄 |
| 정전류 | BaSyTec · 정전류 반주기 ↔ **10 분 OCV** ↔ 반대 정전류 |
| 과전압 정의 | Fig. 1f: 정전류 인가 순간의 **초기 과전압** + 정전류 중 **상승분** |
| 비교 셀(Marburg) | 0.33 LiI + 0.67 Li₃PS₄ 유리(유성 밀 500 rpm ≈8 h) · ∅12 mm · **265 MPa × 5 min** · Li 박 양면 · CompreDrive 안에서 **4.4–44.2 MPa** 스윕 · Novocontrol Alpha-AK **1 MHz–1 mHz, 10 mV** · RelaxIS 적합 · σ **0.8 mS cm⁻¹** |
| 사후 분석 | ToF-SIMS(ION-TOF 5, Bi₃⁺ 30 keV, ≤500 × 500 µm²) · XPS(PHI Quantera SXM, Al Kα, 45°, Ar 1.5 keV 깊이, 55 eV, 중화 없음, ∅≈200 µm) · 불활성 이송 셔틀(스퍼터 Li 박으로 검증) · 광학 현미경 |
| 온도 | **미인쇄**(주 셀) |

---

# 3. 절별 해체

## 3.1 서론 (p1–2)

- Li 금속 음극의 주 문제 = 덴드라이트 성장 · 셀 고장. 액체 쪽 억제 사례(Rehnlund · Qian · Lu · Han) 나열, `[인쇄]` "the actual lithium dendrite growth mechanism is not sufficiently understood yet".
- 핵생성 문헌(Bai · Sano · Sagane · Yan · Ely) · Sand's time · Rosso · Chazalviel · Seong · Swamy(LLZTO 균열은 최고 전기장 자리).
- ★ 새로움 주장: `[인쇄]` "to the authors' knowledge, it has never been investigated whether the amount of lithium that is stripped and plated within one cycle at a constant current density affects the lithium dendrite growth, neither for liquid nor for solid electrolytes." — 반주기당 Li 양 × 수명.
- 아지로다이트: 10⁻²–10⁻³ S cm⁻¹, Boulineau(LCO/LTO), Kasemchainan(Cl-argyrodite 덴드라이트, ref 13 — 이 편의 기준 대화 상대).
- `[해석]` 서론 첫 단락의 "Higher specific capacities up to 3860 mAh/g for the negative electrode are achieved for example by the addition of silicon" — 3860 mAh g⁻¹ 은 흔히 Li 금속의 값으로 쓰는 수다(외부 지식, D14).

## 3.2 Fig. 1 — 대칭셀 전압 곡선과 수명 (p2–3)

- `[인쇄]` 캡션: (a)(b) **J = 0.30 mA cm⁻² × 5 min**, (c)(d) **J = 0.15 × 60 min**, OCV 10 분. 본문: (a)(b) **0.15 × 5 min**, (c)(d) **0.30 × 60 min** — **뒤바뀜(D1)**.
  `[재현]` 캡션이 맞다 — Fig. 8 반주기 Li 양 비 6.2/1.0 = 6.2 ↔ 캡션 J·t 비 (0.15 × 60)/(0.30 × 5) = 6 · 본문 비 24. Fig. 2a(0.15 인쇄)의 ±20 mV 가 Fig. 1c 와 같은 크기. a,b(±30–35 mV) > c,d(±13–22 mV) 도 캡션 쪽.
- `[도표]` 수명: a ≈20 h · b ≈33 h · c ≈70 h · d ≈167 h. 반주기 주기 a,b 0.5 h(5 + 10 + 5 + 10 분) · c,d ≈2.33 h.
- `[인쇄]` "A sudden voltage drop indicates a short circuit." · Fig. 1a 는 양 전류에서 >10 mV 과전압 → 다음 음 전류 초기 과전압이 높다 · 1b,c 는 대칭 · 1d 는 음 곡선 과전압이 줄어든다.
- `[인쇄]` 첫 반주기 전압은 "either remains constant or decreases"(Wood · Lin 도 보고) · 이어지는 음 곡선은 네 셀 모두 **과전압 상승 시작** — `[인쇄]` "We believe that this increase is the key factor in understanding the lifetime".
- `[인쇄]` Lin et al. 의 설명(오목면 두꺼운 SEI 의 에너지 장벽, 새로 도금된 Li 가 소진되면 SEI 밑 원래 박에서 박리) 인용 — 이후 이 편이 **SEI 대신 면적 · 공공 확산**을 내세운다.
- **Fig. 1e** `[도표]`: 과전압(로그, mV) vs 단락까지 "Total Li-amount [µg]". 0.30: (≈31, ≈40) · (≈39, ≈23) · (≈66, ≈2.9) — 직선 적합. 0.15: (≈10, ≈125) · (≈30, ≈5) · (≈71, ≈1.3) — 적합선이 가운데 점(≈5)을 ≈15 mV 로 지나 **3 배 빗나간다**. `[인쇄]` "includes the values of three identical cells for each current density" · "a shorter cell lifetime is related to a higher overpotential before a short circuit occurs".
  ⚠ 점 셋 · 두 전류밀도 · 적합 통계 0. 0.15 의 ≈125 mV 는 c,d 어느 반주기(≤≈22 mV)보다 ×6 크다 · 0.15 가로축 10–71 µg 는 Fig. 8 의 0.15 막대(≈70–510 µg) 와 겹치지 않는다(D6).
- **Fig. 1f** `[도표]`: 0.30 셀 5 분 계단(2.17–2.25 h) — 인가 즉시 ≈0.020–0.023 V, 계단 끝 ≈0.035 V; 두 가로선 ≈0.023 · ≈0.035 V 사이가 "increase of overpotential".
- `[도표]` **수명 전 구간 계단 크기가 줄어든다**(판정 (3) 표) — 본문은 1d 음 곡선만 언급.

## 3.3 Fig. 2 · 3 — XPS 로 SEI 찾기 (p3–5)

- 절차: 0.15 mA cm⁻² × 30 분 × 5 사이클 → 한쪽으로 **연속 박리**해 집전체를 떼고(Fig. 2b "5x → 1x → XPS") → 전해질 표면("electr." — 이전 계면) · 기준 스폿("ref." — Li 와 안 닿은 곳) · 집전체 위 잔류 Li 를 깊이 분석.
- `[도표]` Fig. 2a: 사이클 ±20 mV 급 · 연속 박리 ≈7.4 h 부터 0.018 → 0.021 V 로 완만 상승, 가로축은 ≈11.5 h(연속 ≈4 h)에서 끝난다 (`[재현]` 0.15 mA cm⁻² × 0.126–0.16 cm² × 4 h = 76–96 µAh = 20–25 µg ≈ 박 재고의 **4–6 %** ↔ 캡션 "until most of the lithium is moved" — 그림이 잘렸을 수 있다, D16).
- 전해질 쪽(Fig. 3a,c): 이전 계면 = 기준 스폿, 봉우리 모양 · 결합에너지 차 없음. S 2p ≈161.5 eV 주성분(황화물), Li₂S ≈160.2 eV 매우 약함. P 2p 한 성분(Li₆PS₅Cl). Li₃P "barely seen above the detection limit".
- Wenzel(스퍼터 Li — 에너지 큰 증착) · Kasemchainan(250 h 노출, 표층 긁었는지 불명) 과의 차이를 **증착 방식**으로 설명(`[인쇄]` "might").
- 잔류 Li 쪽(Fig. 3b,d): 처음엔 붙어 있는 전해질 신호 → 스퍼터 ≈8 분(≈151 nm) 까지 Li₂CO₃ · LiOH · Li₂O(새 박에도 있는 표층) → 이후 Li⁰(`[인쇄]` ">80% after ∼8 min"; `[도표]` Fig. 3d Li 1s ≈80 % at ≈8–9 min · ≈91 % at 23 min). S 2p 최대 6 at% 에서 감소.
- `[인쇄]` "If there would be a clear SEI, the Li2S signal should be dominating in the beginning of the depth profile." · "It remains unclear what the contributions for such an increased overvoltage related to cell lifetime are."
- ⚠ **XPS 는 계면을 떼어 낸 뒤의 두 면**을 본다 — 떼는 과정에서 SEI 가 어느 면에 남는지 · 연속 박리가 계면을 바꿨는지는 통제 없음. 새 박 기준 스펙트럼은 "our previous measurements" (지면 0).

## 3.4 Fig. 4 — 3전극 EIS (p5–6) — **Q5 · 곱 축퇴 본체**

- `[인쇄]` 기준극 셀: Au 도금 W 선을 펠릿 가운데 · 두 전극에서 Li 도금 → **0.30 mA cm⁻²** 정전류 중 **박리 쪽 계면**을 시간에 따라 EIS.
- 등가회로(Fig. 4a 삽도): `R1 – (R2‖CPE2) – (R3‖CPE3) – (R4‖CPE4) – Ws`. 전기용량은 Brug 식.
  - R2‖CPE2 = 벌크 + 입계, `[인쇄]` "a mixed capacity of about **10^10 F/cm²**" (렌더 확인 — 양의 지수, D4)
  - R3‖CPE3 = SE\|Li 계면, **10⁻⁷ F cm⁻²**
  - R4‖CPE4 = "chemical capacities", **10⁻⁴ F cm⁻²**(refs 42–45 Jamnik · Maier · Bron–Roling)
  - Ws = Warburg short
- `[도표]` Fig. 4a(박리 쪽, 옴 단위 — 면적 규격화 아님): 범례 **0.1 · 1.3 · 2.6 · 3.8 · 5.1 µg**. 고주파 첫 점 ≈35 → ≈43 Ω, 저주파 끝(0.1 Hz) ≈60 → ≈105 Ω 이고 끝에서도 꼬리가 닫히지 않는다. 화살표 "R₃ →".
- `[도표]` **Fig. 4b**: 벌크+입계 ≈41 · 42 · 43 · 42 · 42 Ω(평탄) · **계면 ≈1.5 · 4.1 · 5.9 · 7.8 · 8.8 Ω(×≈6)**, 가로축 "**Amount Li [µm]**" 0.3 · 6 · 12 · 18 · 24.
  - ⚠ **D2**: 범례는 µg 0.1–5.1, 축은 "µm" 0.3–24 — 비 ≈4.7. `[재현]` 5.1 µg 을 Li 두께로 바꾸면 0.126–0.16 cm² 에서 **0.60–0.76 µm**(×31–39 작다). 대신 **분** 으로 읽으면 맞는다: 0.30 mA cm⁻² × 0.16 cm² = 48 µA → 0.207 µg min⁻¹ → 6 · 12 · 18 · 24 분 = 1.24 · 2.49 · 3.73 · 4.97 µg ↔ 범례 1.3 · 2.6 · 3.8 · 5.1. `[해석]` 가로축은 **박리 시간(분)** 이고 EIS 간격 6 분 — 그리고 면적이 ≈0.16 cm² 다(판정 (5)-4).
- `[인쇄]` 해석: 벌크 · 입계 불변("no major chemical changes … are expected") · 계면 R3 증가. 계면 저항 = Li 표층(Li₂O · Li₂CO₃ · LiOH) 이 SE 에 닿은 **평균 접촉 저항**. 그리고 판정 (5)-2 의 **"either … R ∼1/A or an ionically insulating SEI … leading to a decreasing active contact area"**. Wenzel(스퍼터 Li) 의 더 강한 증가 · Kasemchainan 의 공극(void) — `[인쇄]` "The formation of voids corresponds to a reduced interface area".
- `[인쇄]` 저주파 "chemical capacities and Warburg short contributions increase significantly" → 또 하나의 원인.
- **Fig. 4c**(도금 쪽) `[도표]`: 고주파에 **유도성 꼬리**(Z_imag 양수 쪽 — 그림은 아래로), 전체 저항 **감소**(실수축 교차 ≈40.5 → ≈33.5 Ω · 저주파 끝 ≈56–57 → ≈47 Ω, "R₁₋₃ ←"), 저주파가 반원 모양. `[인쇄]` "some inductive contributions … makes a separation of these resistances impossible" · "the overall resistance … is decreasing" · "a better contact between lithium metal and solid electrolyte exists on the lithium plating side as bulk and grain boundary resistances are expected to remain constant according to the lithium stripping side" — **벌크 불변을 박리 쪽에서 빌려와** 도금 쪽 감소를 계면에 준다.
  `[해석]` 기하가 대칭(선이 가운데)인데 유도성이 **한 반쪽에만** 있다 — 45호 줄("반쪽에만 있는 고주파 호/특징은 기준극 채널 artifact 부터 거른다")의 후보. 원문 원인 무언급.
- `[인쇄]` "It is important to keep in mind that the interface resistance in the EIS spectra represents an averaged contact resistance." · "Still it is an open question if this effect of interface area is stronger than the influence of the SEI."

## 3.5 Fig. 5 · 6 — 공공 확산 가설과 압력 대조 (p6–8)

- **가설**(Fig. 5 모식도 — 안 봤다, 캡션만): 박리는 국소 접촉점에서 일어나고, Li⁺ 는 SE 로, **Li 공공은 Li 금속 안으로 확산**해야 한다. `[인쇄]` D_Li(자기확산) 10⁻¹¹–10⁻¹⁰ cm² s⁻¹(refs 46, 47) · c_Li ≈0.1 mol cm⁻³ → Nernst–Einstein `s_Li = c F² D / RT` = **3 × 10⁻⁶ – 3 × 10⁻⁵ S cm⁻¹** < σ_SE ≈10⁻³ ⇒ **공공 확산이 병목** → 저주파 Warburg short. 접촉점 크기 분포 → 넓은 Warburg 분포 → 위상 45° 보다 낮은 비이상 스펙트럼. 전류 큰 점에 공공 과포화 → void.
  `[재현]` c_Li = 0.534 / 6.94 = 0.077 mol cm⁻³ 로 계산하면 s_Li = **2.9 × 10⁻⁶ – 2.9 × 10⁻⁵** — 인쇄 범위와 맞다(0.1 은 반올림).
- 도금: Kasemchainan(ref 13)처럼 **Li–void–SE 삼중 경계**에서 → 도금 전류 점이 박리 때보다 잘 정의 → 더 이상적인 Warburg(Fig. 4c).
- **Fig. 6**(유리 SE 셀, 무 DC): `[인쇄]` 가압 8.8 → 44.2 MPa 에서 Warburg 가 "much more ideal", 감압 → 4.4 MPa 에서도 "quite ideal".
  `[도표]` 6a 고주파 절편 ≈128(8.8 MPa) → ≈97 Ω(44.2) · 6b 감압: 44.2 ≈97 → 4.4 MPa ≈88–90 Ω(절편은 **감압에서 더 낮아진다**) · 저주파 호는 감압에서 커진다.
  `[도표]` **6c** R_Ws(감압 가지만): 44.2 ≈13 · 35.4 ≈24 · 26.5 ≈29.7 · 17.7 ≈33 · 8.8 ≈32 · 4.4 ≈32.5 Ω · **6d** α_Ws: 44.2 ≈**0.41** · 나머지 ≈0.46–0.47. 축 이름 "Pressure [**mPa**]"(D9).
  ⚠ **D9**: 적합은 감압 가지뿐 — 가압 가지의 "더 이상적" 은 적합값이 없고, 적합된 44.2 MPa 점(α ≈0.41)이 **감압 가지에서 가장 비이상**이다.
- **경도 논증**: Li 항복 2 MPa(Wang–Sakamoto) × 3 → 비커스 ≈6 MPa · 문헌 ≈49 MPa(Cardarelli) → 44 MPa 면 "almost perfect contact" 이어야 하는데 계면 임피던스가 계속 준다 ⇒ `[인쇄]` "we suggest that the hardness of the SEI on Li metal determines the contact area" — Li₂O · LiOH · Li₃N 표층 Li 의 항복 ≈200 MPa(Xu 2017) → 비커스 ≈600 MPa.
- `[인쇄]` 요약: 3전극 EIS 가 두 전극 과정을 가른다 · 박리 쪽 R 증가 = 계면 저항 + 저주파 · 공공 구배 → void → 면적 감소 · `[인쇄]` "Such a behavior is more likely than a strong influence of a possible SEI growth on the voltage response as the overvoltage increases repeatedly in each cycling step. If the voltage increase … would be mainly caused by an SEI growth, the SEI would build up and down according to the overvoltage behavior" — **가역성 논증**(반주기마다 되풀이되는 상승은 단조 성장인 SEI 로 설명이 어렵다).

## 3.6 Fig. 7 — 면적 비대칭 셀 (p8)

- 두 Li 판 크기를 다르게 한 대칭셀. `[도표]` (0.5–1.2 h 구간만) **파랑(큰 → 작은 쪽으로 박리)**: ≈8.8 → ≈7.2 mV 로 감소 · **주황(작은 → 큰)**: ≈6.0 mV 평탄. 크기 · 전류 **미인쇄**.
- `[인쇄]` 파랑의 초기 상승과 하강: "It is very likely that the stripped lithium is plated partially onto the smaller lithium electrode … and also plated onto the steel current collector on the edge of the lithium metal which enlarges the lithium active area and results in a potential drop." · Fig. 1a 의 음 곡선 초기 과전압과 "similar" · `[인쇄]` "The higher the overpotential, the smaller the active lithium contact area."
- `[해석]` 이 그림이 **면적 대조군**이다(처방 2단계) — 그러나 크기 미인쇄 · EIS 0 · 한 쌍 · 0.7 h 뿐이라 **R·C 짝**을 못 준다. 그리고 파랑의 하강을 "집전체 가장자리 도금 → 활성 면적 증가" 로 읽는 문장은 **전자 경로가 커진다는 말**이기도 하다 — 강 집전체 가장자리에 도금된 Li 가 상대극 쪽으로 자라면 그것이 곧 연성 단락의 시작이다. 원문은 둘을 가르지 않는다.

## 3.7 Fig. 8 — 반주기 Li 양 × 수명 (p8–9)

- `[도표]` 막대(총 Li 양 µg, 오차 막대 정의 미인쇄):

  | J (mA cm⁻²) | 반주기 Li (µg, 인쇄) | 총량 `[도표]` | 오차 막대 `[도표]` |
  |---|---:|---:|---|
  | 0.15 | 3.1 | ≈85 | ≈68–102 |
  | 0.15 | **6.2** | **≈510** | ≈350–670 |
  | 0.15 | 12.4 | ≈70 | ≈60–79 |
  | 0.30 | 0.6 | ≈28 | ≈20–38 |
  | 0.30 | **1.0** | **≈93** | ≈73–116 |
  | 0.30 | 2.0 | ≈53 | ≈40–69 |

- `[인쇄]` "Either a small or a large amount of stripped and plated lithium during one cycle leads to faster cell failure in comparison with a medium amount" — 비단조. 캡션: "A similar lifetime behavior, **independent of the capacity**, is observed for both current densities" ↔ 같은 캡션 "Cell failure depends on current density and amount of lithium stripped and plated per cycle"(D11).
- `[재현]` 반주기 양 → 면적: 1.0 µg = 3.86 µAh 를 0.30 mA cm⁻² × 5 min 에 → **0.154 cm²** · 6.2 µg = 23.9 µAh 를 0.15 × 60 min 에 → **0.160 cm²** — **Fig. 1 의 두 프로토콜이 각 전류의 "중간" 막대다**(캡션 배정 기준). 0.30 중간 막대 ≈93 µg ↔ Fig. 1a `[재현]` 6.7 h 통전 × 46 µA ≈80 µg(범위 안) · 1b ≈132 µg(위) · 0.15 중간 ≈510 ↔ 1c ≈360 · 1d ≈860 µg — **a–d 는 중간 조건 셀들과 양립**(셀 동정 미인쇄).
- `[재현]` **Li 재고**: 0.15 중간 조건 총 ≈510 µg ≈ 한 박의 재고(403–513 µg)를 **통째로 한 번 옮긴 양** — 그래도 한 전극의 순 이동은 반주기량(6.2 µg ≈1.2–1.5 %)을 넘지 않는다.
- `[인쇄]` 해석(적은 양): 적게 도금되면 **작은 면적만 잘 붙어** 그 자리 저항 ↓ → 국소 전기장 · 전류밀도 ↑ → 빠른 단락(refs 56, 57). 중간 = 더 넓은 도금 면적 → 중간 전류밀도. `[인쇄]` "However, if this explanation holds true in general, then a high amount of stripped and plated lithium should lead to higher lifetime, which would be in contrast to … the findings in our experiment." — 많은 양은 다음 절로.
- ⚠ 두 전류의 "중간" 이 6.2 ↔ 1.0 µg(×6.2) 로 다르다 — **보편 최적 양이 아니다**(저자도 결론에서 "individual for each current density"). 0.15 의 "적음"(3.1 µg) 이 0.30 의 "많음"(2.0) 보다 크다.
- `[해석]` 0.30 셋 막대의 오차 막대 겹침: 중간(≈73–116) ↔ 많음(≈40–69) 은 안 겹치지만 간격이 좁고 n 미인쇄.

## 3.8 Fig. 9–11 — 강판 위 씨앗 도금 (p9–10) — ⚠ 그림 9 · 10 · 11 은 **안 봤다**(캡션 · 본문만)

- 모형계: Li 한쪽 + **이온 차단 강판**(반대쪽)에 0.30 mA cm⁻² 로 **0.6 · 1.0 · 2.0 µg**(= Fig. 8 의 0.30 세 양) **한 반주기만** 도금. `[인쇄]` "Even though lithium is softer than a steel plate, it is assumed that the lithium plating on a steel plate is similar to a lithium electrode with less contact to a rough electrolyte surface."
- 광학 현미경(Fig. 9): 적은 양 = 작은 핵 분포 · 많은 양 = 더 많은 씨앗. `[인쇄]` "The seeds represent contact areas to the electrolyte." · "The light microscope only gives a rough estimation".
- ToF-SIMS(Fig. 10, 1.0 µg): 씨앗 = 안쪽 원(SE 와의 연결 — Cl 잔류) · 가운데(옆으로 퍼진 Li) · 가장자리 얇은 띠(Fe 신호 — 매트릭스 효과). `[인쇄]` "the intensity in ToF-SIMS analysis cannot be correlated to the concentration".
- Fig. 11(Li · Cl 지도, 세 양): 적은 양 = 고립된 작은 씨앗 · 중간 = 더 많은 씨앗, 가장자리 겹침 · **많은 양 = 넓게 겹친 도금 + 이미 도금된 Li 위에 새 씨앗**(3 차원). `[인쇄]` 새 씨앗 = 새 연결 · 높은 국소 압력 → 낮은 국소 저항 → 높은 국소 전류밀도 → 이른 고장 · 처음 핵 자리는 압력이 빠져 접촉 ↓.
- ⚠ **D8**: 본문 패널 지칭(a = 적음 · b = 중간 · c = 많음)과 캡션((a+b) 0.6 · (c+d) 1.0 · (e+f) 2.0 µg; 위 Li · 아래 Cl) 이 다르다. 그림을 안 봐서 어느 쪽이 맞는지 확인하지 않았다.
- ⚠ "많은 양을 **반복** 도금하면 씨앗이 쌓인다" 는 **한 반주기 2.0 µg** 강판 시편에서 나왔다 — 반복 · 박리 · Li 기판 · 0.15 계열(3.1–12.4 µg) 의 시편 0.

## 3.9 결론 (p10)

- 과전압 상승이 덴드라이트 이해의 열쇠 · XPS Li₂S 소량(S 2p 6 at%) — SEI 가 원인인지 "questionable" · 3전극 EIS: 박리 쪽 저항 증가 = **Li 공공 구배(Warburg short)** + **void → 계면 면적 감소** · `[인쇄]` "the lithium electrode represents the bottleneck and therefore **limits the power density** in all-solid-state batteries"(출력 측정 0 — D15) · 도금 쪽 저항 감소 = 더 나은 접촉.
- 반주기 양: 0.30 · 0.15 둘 다 적음 · 많음이 빠른 고장 — 씨앗형 도금으로 설명.
- `[인쇄]` "A SEI should not be neglected, but the main focus should be put on the actual contact area at the interface between the lithium electrode and solid electrolyte in further investigations of cell lifetimes."

---

# 4. ★★★★ Q5 — 영점 계보에서의 자리

- **형태**: 스물두 번째 — **"영점이 들어가지 않는 자리: 같은 금속 대칭셀의 AC 분할 전용"**. 19호(4전극 — 두 기준극 차로 영점을 **소거**)와 결과는 닮았지만 기구가 다르다: 19호는 설계로 상쇄했고, 이 편은 **측정량(AC 임피던스)** 이 애초에 기준극 DC 값을 보지 않는다. 대가는 같다 — **기준극 자신에 대한 정보가 지면에 0** 이다.
- **이 편이 영점을 요구하지 않은 이유가 이식 조건이다** `[해석]`: (a) WE · CE · RE 가 모두 Li 금속(도금 Li) · (b) DC 전위를 읽지 않는다 · (c) 상대극 재고가 무한에 가깝다(60 µm 박). 16호는 셋 다 깼다 — NMC 상대 리튬화(원천이 Li 금속 아님) · 전위 축(DC) 사용 · 0.27 mAh cm⁻² 소량 리튬화(45호). **같은 선을 영점이 필요한 자리로 옮기면서 영점을 다른 연구실(Giessen)에서 빌렸다.**
- **P8 (재료 · 위치 섭동)** · **P10 (누설)** · **P11 (측정 셀 안 Li 대비 교정)** — 전부 0. 단, 이 편에서는 P11 이 **공짜로 성립할 자리**였다: Li\|Li 셀에서 RE–WE · RE–CE 개방회로 전압은 기준극이 도금 Li 면 **≈0 V** 여야 하고, 그 두 숫자 인쇄 하나로 "constant potential" 이 측정이 됐을 것이다(`[해석]`).
- **계보 표 위치**: 시간순으로 이 편(2019-12 투고)은 41호 Nam(2018-07) · 42호 Santhosha(2019-03) 다음, 20호 Chang(2019 접수) 과 같은 해 — **Au 도금 W 선 기준극의 계보상 가장 이른 ASSB 사용**. 금선 기준극 전체로는 Solchenbach 2016(액체, 큐 48) 이 앞선다(45호 인용).

---

# 5. ★★★ Q7 — 수명 기구 · 단락 판정의 층위

| 층 | 이 편 | 층위 |
|---|---|---|
| 계면 저항 성장(박리 쪽) | 3E EIS R3 ×≈6 (`[도표]` 1.5 → 8.8 Ω, 5.1 µg 박리) | **측정** — 단 원인 배정(면적 ↔ SEI)은 **논증** |
| 공공 확산 한계 | Nernst–Einstein 크기 비교 + Warburg 모양 + 압력 대조(다른 SE) | **계산 + 해석** |
| void | 문헌(Kasemchainan · Krauskopf) + 추론 | **해석**(영상 0) |
| SEI | XPS — 소량 Li₂S | **측정(음성 쪽)** |
| 덴드라이트 단락 | 전압 급락 | **판정 = 모양** · 영상 · 임피던스 0 |
| 씨앗 도금 → 국소 전류 | 강판 한 반주기 ToF-SIMS | **대리 모형계** |
| Li 소모 | 없음 | `[재현]` 제한 기구 아님 |

- `[해석]` **정상 열화 ↔ 단락의 구분 신호**: 이 편에서 쓸 수 있었던 것은 셋 — ① 단락 뒤 EIS 가 저주파에서 실수축에 **전자 저항으로 수렴**하는가(이온 경로면 Warburg/용량성 꼬리) ② 정전류 계단의 **전압–전류 선형성**(전자 경로는 옴성, 계면 과정은 비선형) ③ 전류를 끊은 뒤 **이완 시상수**. 대칭셀은 OCV 가 0 이라 ③ 이 약하고, ①② 는 지면에 없다. 41호(연성 단락 누설 → CE 저하) 와 달리 **CE 통로 자체가 없어서** 연성 단락이 "과전압 감소" 로만 나타난다 — 그리고 이 편은 과전압 감소를 **면적 증가** 로 두 번 읽었다(Fig. 1d · Fig. 7).
- 우리 쪽에 남는 것: Li 금속 음극 완전지에서 **"음극 계면 저항 ↓"** 를 좋은 신호로 읽기 전에 연성 단락을 먼저 배제해야 한다 — 완전지는 개방회로 자기방전(전압 감쇠)이 보이므로 대칭셀보다 **가를 수 있는 자리**다.

---

# 6. ★★★ 곱 축퇴 — 저자 문장 안의 합류

- `[인쇄]` "either with a decreasing interface area … as R ∼1/A **or** an ionically insulating SEI formation at the interface, **leading to a decreasing active contact area**" — 두 갈래의 끝이 같은 말이다. `[해석]` R3 는 `A_geom × f_pass`(기하 접촉 × 화학적 통과 분율)의 역수만 본다 — 카드의 `A_eff ↔ k` 항등(37호)의 **Li 음극 판**. 저자는 이 곱을 **XPS 음성(화학 쪽 작다) + 가역성 논증 + 도금 쪽 반대 부호** 로 기하 쪽에 배정했고, 스스로 "open question" 이라 적었다.
- **역방향 짝** `[해석]`: 같은 셀 두 반쪽에서 박리 쪽 R ↑ · 도금 쪽 R ↓ — 면적(형태) 가설은 **부호 반대**, 단조 계면층 성장은 **둘 다 ↑** 를 예측한다. 이 편의 가장 좋은 판별 설계다. 그러나 도금 쪽은 유도성 때문에 성분 분리가 막혔다(`[인쇄]` "separation … impossible") — 짝이 **반쪽만** 남았다.
- 처방 단계는 §10.

---

# 7. `[재현]` 검산 장부

| # | 계산 | 결과 |
|---|---|---|
| R1 | 4.3 t × 9.81 N / (π × 5² mm²) | 537 MPa ↔ 인쇄 540 ✓ |
| R2 | 펠릿 100 mg / (π × 0.5² × 0.075 cm³) | 1.70 g cm⁻³ (D13) |
| R3 | 0.1 kN / 0.126 · 0.785 · 0.16 cm² | 8.0 · 1.3 · 6.3 MPa ↔ 인쇄 "about 6" |
| R4 | 1 µg Li = 1e-6 / 6.941 × 96485 C | 13.9 mC = **3.86 µAh** |
| R5 | Fig. 8 중간 양 ↔ Fig. 1 캡션 프로토콜 | 0.154 · 0.160 cm² (d ≈4.4–4.5 mm) |
| R6 | Fig. 4b 가로축을 분으로 · 48 µA | 1.24 · 2.49 · 3.73 · 4.97 µg ↔ 범례 1.3 · 2.6 · 3.8 · 5.1 |
| R7 | 5.1 µg 를 Li 두께로 (0.126–0.16 cm²) | 0.60–0.76 µm ↔ 축 "24 µm" (D2) |
| R8 | Li 박 재고 60 µm | 403 µg (0.126) · 513 µg (0.16) |
| R9 | Nernst–Einstein, c = 0.077 mol cm⁻³ | 2.9e-6 – 2.9e-5 S cm⁻¹ ↔ 인쇄 3e-6 – 3e-5 ✓ |
| R10 | DC 면적저항 Fig. 1a/b(0.30, 캡션) 0.023 · 0.035 V | **77 · 117 Ω cm²** |
| R11 | 3E EIS 두 반쪽 합(0.1 Hz 끝, 다른 셀, 5.1 µg 시점) ≈105 + ≈47 Ω × 0.16 cm² | **≈24 Ω cm²** ⇒ DC 의 1/3–1/5 |
| R12 | Fig. 2a 연속 박리 ≈4 h × 0.15 mA cm⁻² × 0.126–0.16 cm² | 20–25 µg ≈ 재고 4–6 % (D16) |
| R13 | 반주기 순 이동 최대 12.4 µg / 재고 | 2.4–3.1 % |

- R10–R11 `[해석]`: DC 과전압의 **≥2/3 가 0.1 Hz 아래**에 있다 — 저자의 공공 확산(Warburg short, 저주파) 서사와 **방향이 맞는다**. 그러나 셀이 다르고(기준극 셀 ↔ Fig. 1 셀) 저자는 이 대조를 하지 않았다.

---

# 8. 우리 축 (Q1–Q8)

| Q | 이 편 | 칸 |
|---|---|---|
| Q1 | 양극 없음. Li\|SE 계면 면적 = R ∼ 1/A **추론**, 면적 측정 0 | 없다 — `θ(N)` **0/46** |
| Q2 | 음극 계면 "면적 ↔ SEI" 를 네 채널로 논증, 저자 "open question" | 반 칸 검토 후 접음 |
| Q3 | 단락 = 전압 모양 판정 · Fig. 8 오차 막대 정의 · n 미인쇄 · Fig. 1e "three identical cells" 점 3 개 · 적합 통계 0 | 층 하나 — **voltage-shape failure label + undefined error bars** |
| Q4 | 0 — `identifiab` · `uncertaint` 0 | **0/46 — 서른여덟 번째 성질** "'A 또는 B' 를 인쇄하고, 두 갈래를 같은 이름('활성 접촉 면적 감소')으로 끝냈다 — 그리고 스스로 'open question' 이라 적은 쪽을 결론의 'main focus' 로 올렸다" |
| Q5 | 기준극 사용 · 영점 0 · 검증 0 | 이동 없음(반 칸 검토 후 접음) — **스물두 번째 형태** |
| Q6 | 제조 540 MPa · 운전 0.1 kN("about 6 MPa", `[재현]` 6.3–8.0) · **압력 스윕 4.4–44.2 MPa 는 다른 SE 셀**(가압 · 감압 이력) | 이동 없음 — 층 하나 **"감압 이력: 저주파(R_Ws) 는 되돌아오고 고주파 절편은 안 돌아온다"** |
| Q7 | Li 대칭셀 · SEI XPS 음성 쪽 · dead Li 0 · 단락 = 모양 | 이동 없음(무음극 아님) |
| Q8 | 양극 없음 | 해당 없음 |

---

# 9. 곱 축퇴 처방 — 스물아홉 번째 적용 (Li 음극 계면)

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | R3 는 5 상태(`[도표]` 4b) · C3 는 **대표값 한 개**(10⁻⁷ F cm⁻²) — 상태별 `C` 미인쇄 | ❌ |
| **2단계** 면적 대조군 | ★ **면적 비대칭 셀**(Fig. 7) — 크기 · 전류 미인쇄 · EIS 0 · 전압 0.7 h · ★ **압력 스윕**(Fig. 6) — 다른 SE, R_Ws · α 만 적합(R3 계열 미인쇄) | ⚠ 면적 손잡이는 둘, 판독이 R·C 가 아니다 |
| **3단계-a** `Ea` | 온도 미인쇄 · 한 점 | ❌ |
| **3단계-b** `C` 상한 | C3 10⁻⁷ F cm⁻²(규격화 면적 미인쇄) · C2 "10^10"(부호 오기) · 도금 쪽 유도성 | ⚠ 판정 불가 — 규격화 기준이 없다 |
| **4단계** 시간 영역 | `[재현]` DC 77–117 Ω cm² ↔ 3E EIS 합(0.1 Hz 끝) ≈24 Ω cm² — ≥2/3 가 0.1 Hz 아래 | ✅(부분) — 대역 밖 몫의 크기만 · 다른 셀 |
| **새 줄 후보** | **역방향 반쪽 짝**: 한 셀에서 박리 쪽 · 도금 쪽을 동시에 — 면적(형태)은 부호 반대, 단조 계면층은 같은 부호 | `[해석]` 이 편이 반쪽만 실행(도금 쪽 성분 분리 실패) |

⚠ **이것이 곱을 푼 것은 아니다.** 양극이 없고, R3 의 기하 ↔ 화학 분배는 논증이다. 기여는 **곱이 저자 문장 안에서 한 이름으로 합쳐지는 표본**과 **역방향 짝**이라는 설계다.

---

# 10. 어긋남 (실제로 어긋난 것만)

| # | 어디 | 무엇 |
|---|---|---|
| **D1** | Fig. 1 본문 ↔ 캡션 | 본문 (a,b) 0.15 × 5 min · (c,d) 0.30 × 60 min ↔ 캡션 (a,b) 0.30 × 5 · (c,d) 0.15 × 60. `[재현]` Fig. 8 비 · Fig. 2a 크기 · 전압 크기가 **캡션** 편 |
| **D2** | Fig. 4b 가로축 | "Amount Li [µm]" 0.3–24 ↔ 범례 µg 0.1–5.1 — Li 두께면 ≤0.76 µm; `[재현]` **분**(6 분 간격, 0.16 cm²)으로 맞는다 |
| **D3** | Li 면적 | 인쇄 ∅4 mm(0.126 cm²) ↔ 지면 세 수(Fig. 8 · Fig. 4b · "about 6 MPa")가 ≈0.16 cm² 를 가리킨다 |
| **D4** | 본문 p5 | 벌크 · 입계 "mixed capacity of about **10^10** F/cm²"(렌더 확인, 양의 지수) — 문맥상 10⁻¹⁰ |
| D5 | 본문 p5 | "plated with lithium from both **electrolytes**" — 전극 |
| **D6** | Fig. 1e ↔ Fig. 8 · Fig. 1c,d | 0.15 수명 10–71 µg ↔ Fig. 8 0.15 막대 ≈70–510 µg · 0.15 "overpotential" ≈125 mV ↔ c,d 최대 ≈22 mV · 적합선이 가운데 점을 ×3 빗나감 |
| D7 | p9 | "a medium **current density** leads to the most stable cell … (see Figure 8)" — Fig. 8 은 전류밀도 고정, 반주기 양을 바꾼다 |
| D8 | Fig. 11 본문 ↔ 캡션 | 패널 지칭 a/b/c ↔ (a+b)/(c+d)/(e+f) — 그림 미열람, 어느 쪽이 맞는지 미확인 |
| **D9** | Fig. 6 | 축 "Pressure [mPa]" · "가압에서 더 이상적" 은 적합값 없음 · 적합된 44.2 MPa α ≈0.41 이 감압 가지에서 가장 비이상 |
| D10 | p4 | 잔류 Li 의 Li 1s 이동을 "(Figure 3c)" 로 지칭 — 잔류 Li 는 3b · 3d |
| D11 | Fig. 8 캡션 | "independent of the capacity" ↔ 같은 캡션 "depends on … amount … per cycle" ↔ 결론 "lifetimes depend on the cycled capacity" |
| D12 | 참고문헌 | ref 16 = ref 30(Swamy 2018 중복) · ref 9 제목 없음 · ref 24 권호 불완전("1 (March.") · ref 3 "Boucamp" |
| D13 | 실험 | 겉보기 밀도 1.70 g cm⁻³ — `[해석]` Li₆PS₅Cl 결정 밀도로 흔히 쓰는 ≈1.64 g cm⁻³(외부 값)보다 크다 → 질량 · 두께 중 하나가 어림값 |
| D14 | 서론 | "3860 mAh/g … by the addition of silicon" — `[해석]` Li 금속의 값(외부 지식) |
| D15 | 결론 | "limits the power density" — 출력 · 율 측정 0 |
| D16 | Fig. 2 | 캡션 "until most of the lithium is moved" ↔ 그림 연속 박리 ≈4 h(`[재현]` 재고 4–6 %) — 그림이 잘렸을 수 있다 |

---

# 11. 그림 — 무엇을 봤나

크로퍼 **11 장**(본문 그림 11, SI 없음). **7 장 봤다**: Fig. 1(6 패널) · 2 · 3 · 4 · 6 · 7 · 8.
**안 본 것**: Fig. 5(공공 구배 모식도) · 9(광학 현미경) · 10 · 11(ToF-SIMS) — 모식도 · 형태 영상이라 우리 축(기준극 · 단락 판정 · 곱)에 수치를 주지 않는다고 보고 캡션 · 본문만 읽었다. D8 은 그래서 미확인이다.
**본문과 어긋난 그림**: Fig. 1(본문 J·t 배정 — D1) · Fig. 4b(축 단위 — D2) · Fig. 6(단위 · "더 이상적" — D9) · Fig. 3(패널 지칭 — D10) · Fig. 1e ↔ Fig. 8(D6).
렌더 확인: 본문 p5 "10^10 F/cm²"(D4) · p3 "10⁶ and 10⁻¹ Hz".

---

# 12. 참고문헌 중 후속 후보 (59 편 중 — 미열람, 서지는 지면 그대로)

| 서지 | ref | 왜 |
|---|---|---|
| Kasemchainan, Zekoll, Spencer Jolly, Ning, Hartley, Marrow, Bruce 2019 *Nat. Mater.* 18, 1105 | 13 | 이 편의 대화 상대 — **임계 박리 전류 → void → 도금 때 덴드라이트**, 삼중 경계 도금, 아지로다이트 XPS(Li₃P) |
| Krauskopf, Hartmann, Zeier, Janek 2019 *ACS AMI* 11, 14463 | 14 | 공공 과포화 · void · **압력 ↔ 비커스 경도 가정**의 원전(이 편이 반박) — Giessen |
| Wenzel, Sedlmaier, Dietrich, Zeier, Janek 2018 *SSI* 318, 102 | 38 | 아지로다이트 \| Li **계면층 성장**(스퍼터 Li) — SEI 쪽 대조 |
| Bron, Roling, Dehnen 2017 *JPS* 352, 127 | 45 | **Roling** — 황화물 \| Li 혼합 전도 계면층의 임피던스(chemical capacitance) — R4 배정의 근거 |
| Wang, Sakamoto 2018 *JPS* 377, 7 | 51 | Li 항복 2 MPa · 계면 저항 ↔ 접착 |
| Xu, Ahmad, Aryanfar, Viswanathan, Greer 2017 *PNAS* 114, 57 | 54 | 소규모 Li 항복 ≈200 MPa — "SEI 경도가 접촉을 정한다" 논증의 기둥 |

큐 48–59(Solchenbach 2016 · Dugas 2021 · Barai 2018 · Miß 2022 · Illig 2012 · Oh 2025 · Ren 2023 · Neumann 2021 · Hlushkou 2018 · Bielefeld 2022 · Bielefeld 2020 · Asheri 2023) 인용 **0**.
⚠ 이 편이 인용한 기준극 선례도 **0** — 3전극 셀은 감사의 글("developing the three-electrode reference cell") 로만 출처가 적힌다.

---

# 13. 우리 프로젝트와의 접점

- **degradation-degeneracy**: 액체셀 · 합성 truth 파이프라인과 직접 접점 없음. 대칭셀이라 OCV 적합 · 모드 분해 대상 자체가 없다.
- **ASSB 카드**: (a) 기준극 계보의 마지막 조각 — 16호 기준극의 영점 문제는 **"다른 자리에서 빌린 영점"** 이라는 형태로 정리된다 · (b) 곱 축퇴의 음극 판 표본 · (c) Q7 쪽: Li 금속 대칭셀의 단락 판정이 **모양 판정**이고, 연성 단락 배제 절차가 없다는 계보 사실.
- **α · β 검증 하네스(bms-balancing)**: 이 편 수치는 들어가지 않는다(액체 · 완전지 아님).

---

# 14. 이 digest 가 주장하지 않는 것

- **"Fig. 1 의 완만한 전압 감소가 연성 단락이다" 라고 주장하지 않는다** — 접촉 개선과 같은 서명이라 **가를 수 없다**는 것까지다.
- **"16호가 이 편을 인용하지 않았다" 고 주장하지 않는다** — 우리 16호 digest 에 기록이 없을 뿐이다. 저자 겹침(Roling · Miß)은 지면 사실이다.
- **Li 면적 ≈0.16 cm² 는 측정이 아니다** — 세 수를 맞추는 면적이고, 원문은 ∅4 mm 만 인쇄한다.
- **DC ↔ EIS 의 3–5 배는 다른 셀 사이의 비교**다 — 대역 밖 몫의 크기 어림이지 분해가 아니다.
- **"XPS 가 SEI 를 배제했다" 고 읽지 않는다** — 원문도 보류("should not be neglected")다.
