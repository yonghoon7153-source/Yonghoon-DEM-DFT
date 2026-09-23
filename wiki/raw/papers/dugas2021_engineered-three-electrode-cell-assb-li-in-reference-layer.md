---
title: "Dugas, Dupraz, Quemin, Koç, Tarascon 2021 — Engineered Three-Electrode Cells for Improving Solid State Batteries (J. Electrochem. Soc. 168, 090508)"
source_url: local-upload/10._Engineered_three-electrode_cells_for_improving_solid_state_batteries.pdf
source_url_note: "PDF 10 쪽(1 쪽 = IOP 다운로드 표지, 논문 9 쪽 + ORCID · 참고문헌 29). SI 없음. 크로퍼 10 장(Fig. 1-10) 전부 봤다, 화소 판독 Fig. 3a · 5c · 7 · 9a · 10a(원본 래스터). 원자료 · PDF 는 커밋하지 않는다. 21호(Sedlmeier 2023) ref 16 이 지목한 'EIS 에 기준극을 쓴 선례' — 기준극은 링이 아니라 전면 Li0.5In:SE 복합층(링은 집전체)."
source_doi: 10.1149/1945-7111/ac208d
source_license: "(c) 2021 The Electrochemical Society, published by IOP Publishing — 오픈액세스 표기 없음, all rights reserved"
pdf_sha256: 4840210294f3a27d0803d63c70563c338ed7042d9fee0fffb5fbb417b12612c2
ingested: 2026-09-23
sha256: ae317a8149f26d022ac35ecb4b7139464642da03954bead95e5a22c322a2fa5d
---

# 수집 목적

`assb` 섹션 **48호**. 큐 **49번**(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g, 2차 묶음 열째 편).
닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q5**. 원장 ★★ · 지목 1 회: 21호(Sedlmeier 2023) 가 ref 16 으로 —
"EIS 에 기준극을 쓴 선례 셋" 중 하나(**"circular indium-lithium RE … around the outer perimeter of a solid electrolyte (SE) separator pellet"**),
In₁Li₀.₅/SE 복합 전극의 선례, 그리고 **"changes in the low-frequency region … upon lithiation and delithiation are expected.16"** 의 근거.
21호는 이 편을 저주파 호 = "charge-transfer" 배정의 인용(refs 4,16,40–43 · 16,44)에도 썼다.

> ⚠ **이 편에는 열화 분해가 없다.** 최대 10 사이클(2전극) · 5 사이클(3전극), `degrad*` · `aging` · `LAM` · `LLI` 0 회.
> 이 편이 카드에 주는 것은 **기준극 설계 · 기준극 검증의 범주 · 2전극 비식별성의 같은 셀 시연**이다.

> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`, 판독 오차 붙음) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

---

# 원문에 없어서 확인이 필요한 것 (공백 먼저)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **기준극 층 · 상대극 · 작업극 복합체의 질량(또는 두께) 미인쇄.** 인쇄는 SE 45 mg(펠릿) · 40 mg(둘째 층) · 조성비(RE/CE 합금 : SE 60 : 40, WE 70 : 30)뿐 | (5) 상대극 재고비 · (5′) 기준극 재고 예산 · 전류밀도(Li 셀 27 µA cm⁻² 외) · 면적당 `C` 의 거칠기 환산이 전부 막힌다 |
| **G2** | **기준 전위를 Li 대비로 잰 문장 · 수 0.** 영점은 `[인쇄]` "expected to remain at a constant voltage of 622 mV vs Li⁺/Li,17"(Santhosha 2019 = 42호) 한 번 — 그것도 **2전극 셀의 귀속 전제**로 | 3전극 결과는 전부 "V vs LiIn/In" 축에 남는다(환산 0). 같은 지면 Fig. 10a 에 Li 금속 상대극 ↔ 기준극 곡선이 있으나 **본문은 그 값을 읽지 않는다**(아래 판정 (1)) |
| **G3** | **기준극 안정성 = "hundreds of hours" · "very good stability" — mV 수 0.** 근거는 TiS₂ 5 사이클(>680 h) 전압 곡선의 겹침(`[인쇄]` "neatly superimposed") | 겹침은 작업극 가역성과 기준극 표류의 **합**이다. 그리고 Fig. 8d 는 사이클을 **다른 패널**에 그려 겹침이 그림에서 직접 보이지 않는다 |
| **G4** | **누설 · 쌍극(bipolar) 교환 측정 0**(`leak` · `drift` · `bipolar` 0 회) | 이 기준극은 **전류 경로를 가로지르는 전면 복합층**이다(판정 (2)). 전자 전도 합금망이 층을 가로지르면 층 안 이온 iR 이 합금에 Li 출입을 시킬 수 있다 — 누설과 다른, 이 기하 고유의 항 |
| **G5** | **"artefact-free" 의 검사 = 양의 Im 호 부재 한 기준**(`[인쇄]` "free of artefact loops which might extend until positive values of Im(Z),15 as expected based on the axial symmetry") | 위치 · 분배 artefact 는 유도성 호 없이도 생긴다(45 · 47호). **기준극 없는 2전극 셀(지면에 있다, Fig. 4)의 EIS ↔ 3전극 합** 비교는 하지 않았다 |
| **G6** | **"repeated at least twice"** — 셀 간 산포 · 오차 막대 0 | 모든 판정의 분해능이 정해지지 않는다 |
| **G7** | **운전 압력은 "initial" 교정값** — 2.3 Nm = 1 t cm⁻²(빈 셀에서 힘 센서로 교정), 사이클 중 압력 기록 0 | Li 셀(45 kg cm⁻², 힘 센서 프레임)과의 비교에서 압력이 유일 원인이라는 문장(D8)의 근거가 약하다 |
| **G8** | **고주파 "둘째 호"(NMC 셀) 의 정체 미정** — `[인쇄]` "we speculate that it might correspond to some process occurring at the planar interface" | 같은 기준극 층을 쓴 LTFS 셀에는 없다 — 기준극 층 몫 후보를 약하게 만드는 대조가 지면에 있다(판정 (3)) |

---

# 판정 (먼저)

## (1) Q5 — 영점 · 조성 · 표류 · 누설

| 물음 | 이 편 | 판정 |
|---|---|---|
| **영점을 무엇으로** | `[인쇄]` "Since the counter electrode is expected to remain at a constant voltage of 622 mV vs Li⁺/Li,17 these features can be attributed to the LTFS cathode material." — **2전극 셀(Fig. 4)에서 전압 특징을 양극에 귀속시키는 전제**로 한 번. 3전극 절 · 그림은 전부 **"V vs LiIn/In"(또는 "LiIn:In")** 축, Li 척도 환산 0, 컷오프도 LiIn/In 기준(LTFS 1.2–2.4 · NMC 2–3.6 · TiS₂ 0.8–2.4 V) | **인용(42호 Santhosha, 세 자리 "622")** — 그리고 **3전극 결과에는 영점이 들어가지 않는다**(측정 축 그대로 인쇄 = P11 의 앞 절반을 지킨 형) |
| **셀 안 Li 대비 증인** | Fig. 10a: **Li 금속 상대극**(LTFS \| β-LPS \| Li₀.₅In:β-LPS 기준층 \| β-LPS \| Li 박, 45 kg cm⁻²)의 전위가 기준극 대비로 그려져 있다. 본문은 이 곡선의 값을 말하지 않는다(`[인쇄]` 극성 · 분극 "at least two times greater" 만) | `[도표]` 원본 래스터(9.8 mV/px) 휴지 끝(수직 눈금 끝) 판독: **사이클 1 도금 가지 −0.593 … −0.603 · 박리 가지 −0.623 … −0.632 V · 사이클 2 도금 −0.613 · 박리 −0.623 … −0.632 V** ⇒ 양방향 이완 끝이 **−0.62 ± ≈0.01 V vs LiIn/In** 에서 만난다 ⇒ `[해석]` **이 셀의 기준극 ≈0.62 V vs Li(셀 안, β-LPS, 1 h 이상 휴지)** — 42호 액체 0.622 · 41호 SI 판독 ≈0.621 · 45호 인쇄 0.618 과 1 px 안. **값은 우리 판독이고 원문 명제가 아니다** |
| **조성 창** | `[인쇄]` Li · In 박 무게비 **33.2** → "to target Li0.5In composition" · "ensures that the anode voltage directly corresponds to the In/LiIn couple as the cell is assembled" · 기준극 = CE 와 **같은 Li₀.₅In : SE(60 : 40 w/w)** · TiS₂ 셀만 CE 가 **Li₀.₉In**(기준극은 Li₀.₅In 유지) | `[재현]` (114.82/6.94)/33.2 = **x 0.498 → 33.3 at% Li** — 42호 평탄 창 ≈1–47 at% 한가운데 ✓. **Li₀.₉In = 47.4 at%** — 42호 창 끝(46–47 at% 이완 0.610 V, "onset of the InLi-phase is already at 47 %")에 걸친다(상대극 쪽; TiS₂ 셀은 첫 단계가 CE 탈리튬이라 창 안으로 들어간다). 상 확인(XRD) 0 — "matt and brittle" 이 판정 기준 |
| **같은 재료 CE ↔ 기준극 창** | `[인쇄]` "its redox potential remains in a potential window of ±160 mV around the RE with a polarization that slightly changes owing to some inhomogeneity of composite CE" · argyrodite 에서 "narrows down from ±160 mV to ±20 mV so that a 2 electrodes configuration can safely be employed with this electrolyte (**20 mV correspond to ⩽2 mA h g⁻¹ at end of charge for NMC**)" | ★★★ **계보 첫 인쇄 "상대극 창 → 용량 오차 → 2전극 허용" 규칙.** 창은 **전류 중 분극**이다 — `[도표]` Fig. 5c(11.9 mV/px) CE 가지 −0.15 … +0.11 V, **휴지 끝은 양방향 모두 ≈0 ± 0.02 V 로 돌아온다**(리튬화 가지 눈금 끝 −0.01 … +0.01 · 탈리튬 가지 −0.02 … −0.01) ⇒ `[해석]` 같은 재료 두 전극이 휴지에서 1–2 px 안 — **상대 표류 상한**일 뿐(공통 모드 불가시, 42호 대칭셀과 같은 한계) |
| **표류(시간)** | `[인쇄]` 결론 "displays stable RE voltage for hundreds of hours" · 근거 "These 5 cycles lasted more than 680 h, which demonstrates a very good stability of the Li0.5In: β-LPS RE"(TiS₂, Fig. 8d) | **수 0 · 그림은 사이클별 다른 패널.** `[해석]` 곡선 겹침으로 안정성을 말하는 것은 **작업극 불변 + 기준극 불변 ↔ 둘이 같이 움직임**을 못 가른다(43호 공통 모드 판독의 반대 — 여기서는 작업극 하나만 증인) |
| **누설** | `leak` 0 · 기준극 층 질량 미인쇄(G1) | **누설 직접 측정 0/48.** (5′) 는 분모도 분자도 없다 |
| **기준극 기하 · 배치 검증** | 아래 (2) | 위치: 축대칭 전면층(인쇄) · 분리막 질량비 대조 ✓ 근사(우리 판독) · 위치 섭동 0 · 기준극 없는 셀 EIS 대조 0 |

⇒ **스물네 번째 형태(Q5)**: `[해석]` **"같은 재료 기준극으로 상대극 창을 재고, 그 창을 용량 오차로 번역해 2전극의 허용 조건을 인쇄했다 — 영점은 2전극 귀속 전제로 한 번 인용(622 mV)했고, 3전극 축은 끝까지 'vs LiIn/In' 로 남겼으며, 셀 안 Li 금속 증인(Fig. 10a)은 그려 두고 읽지 않았다."**
칸: **Q5 +0.5** — 근거가 논문의 측정(Fig. 5 CE vs RE 창, 두 전해질) + 명제(±160 → ±20 mV · "20 mV ↔ ⩽2 mA h g⁻¹" · "2 electrodes … can safely be employed"). **반 칸인 이유**: 창은 분극(휴지 복귀는 우리 판독) · 용량 번역은 NMC 충전 끝 한 점 · Li 대비 영점은 인용 · Fig. 10a 의 ≈0.62 V 는 우리 판독 · 표류 수 0 · 누설 0 · 셀 간 산포 0.

## (2) 기준극 기하 — "원형 InLi 기준극, 펠릿 둘레" 는 **집전체**의 모양이다

`[인쇄]` "a piece of metal foil (15 µ Al in this work), in which an 8 mm hole is punched, is clamped in the middle to be used as RE current collector" ·
"the contact between the RE and its current collector is taken at the periphery of the RE" ·
**"This composite RE takes the form of a layer located between WE and CE and covering the whole cell, leading to an ideal geometry for impedance spectroscopy similar to the one described in Ref. 15 for liquid electrolytes."** ·
"Since the RE layer is located in the middle of the cell, the addition of electrolyte in this layer is necessary to ensure sufficient Li⁺ conduction between working (WE) and counter (CE) electrodes."
Fig. 2 조립도 `[도표]`: ⑤ RE powder 가 ∅8 mm 원통 단면 **전체**를 채우고 ③ 집전체(단차 있는 링)가 층 둘레에 닿는다 · (d) 최종 적층 = WE 분말 \| SE \| **RE 층(전면)** \| SE \| CE 분말.

- **21호의 묘사("circular indium-lithium RE that is located around the outer perimeter of a solid electrolyte (SE) separator pellet")는 원문과 다르다** — 원형인 것은 15 µm Al 링 집전체이고, 기준극은 **단면 전체를 덮는 합금 : SE 복합층**이다. 원장 행("원형 InLi 기준극")과 21호 digest("원형 InLi RE, 펠릿 둘레")가 이 묘사를 물려받았다.
- `[해석]` **이 설계의 고유 조건 — 기준극이 전류 경로 안에 있다.** 전류는 층의 SE 몫을 통해 지나가고, 합금 몫은 둘레 링까지 전자 경로가 이어져야 기준극으로 작동한다. `[재현]` 합금 60 wt%(밀도 ≈6–7 g cm⁻³ 가정) : β-LPS 40 wt%(1.87) → **합금 부피분율 ≈28–32 %** — 무작위 충전의 전자 퍼콜레이션 문턱 부근이고, 압착으로 In 이 번지면 넘는다. 층을 가로지르는 합금망이 있으면 층 안 이온 iR 이 한쪽 면에서 Li 를 넣고 다른 면에서 빼는 **쌍극 교환**을 구동한다 — 기준극이 읽는 것은 망 전체의 혼합 전위. 크기: 구동력은 층 두께의 iR(층 두께 · 저항 미인쇄), Li 셀 27 µA cm⁻² 에서 100 Ω cm² 층이라도 ≈2.7 mV — **이 편의 C/20–C/25 조건에서는 mV 급 이하로 추정**(우리 계산, 측정 0). 고율에서는 따로 봐야 한다.
- **분배 대조(40호 줄)**: `[도표]` Fig. 7(1.744 px/Ω cm²) 고주파 절편 **WE 쪽 ≈283**(인쇄 283) · **CE 쪽 ≈296 Ω cm²** ↔ SE 질량 WE 쪽 40 mg · CE 쪽 45 mg(`[인쇄]` "The WE is placed in the side where the electrolyte layer is thinnest"). `[재현]` 283 : 296 = 0.96 ↔ 40 : 45 = 0.89 — 기준 평면이 SE 전체 옴의 **48.9 %** 지점(질량으로는 47.1 %). ≈1.8 %p(≈10 Ω cm²) 차는 기준극 층 자신의 이온 저항 배분 · 두 층의 밀도 차로 설명 가능 — 판정 불가, **위치 artefact 가 크다는 신호는 아니다**.

## (3) 기준극 검증 — 무엇을 어떤 범주로 검사했나

| 범주 | 이 편의 검사 | 판정 |
|---|---|---|
| **위치(기하)** | 축대칭 전면층 설계 + `[인쇄]` 양의 Im 호 부재 | ⚠ 필요조건만 — 위치 artefact(재분배)는 유도성 호 없이도 생긴다. 섭동(기준극 위치 · 두께 바꾸기) 0 |
| **분배(외부 기준)** | **없다** — 기준극 없는 2전극 셀을 같은 공정으로 만들었으나(`[인쇄]` "Two electrode cells were assembled in similar cells except for the absence of a RE current collector") EIS 비교 0 | ❌ **기준극 층 삽입 임피던스**(층 자신의 이온 · 쌍극 임피던스)를 볼 수 있던 대조가 지면에 있었다 |
| **표류** | TiS₂ 680 h 곡선 겹침(정성) | ⚠ 작업극 증인 하나, 수 0 |
| **영점** | 인용 622 mV · 셀 안 Li 증인은 그림에만 | ⚠ (1) |
| **합 일치** | **검증으로 쓰지 않았다** — 3E 합으로 2E 를 **재구성**해 비식별성을 보였다(아래 (4)) | ✅ 범주 오류 없음(45 · 43 · 40호와 대조: 그쪽은 같은 셀 합 일치를 "validating" 으로 썼다) |

`[해석]` 고주파 "둘째 호"(NMC 셀 32 kHz, α 0.85 · 손 분쇄 NMC 에서 고주파 저항이 SE 층 몫보다 `[인쇄]` "∼50 %" 큼 · argyrodite 에서 SE 층 15 Ω cm² 와 안 맞음)의 후보는 셋 — ① 저자 추정 "planar interface between electrolyte layer and cathode composite" ② 양극 복합체 이온 경로(TLM 고주파 몫) ③ 기준극 층 몫. **같은 기준극 층을 쓴 LTFS 셀에서는 SE 호가 펠릿 전도도와 맞고(`[인쇄]` "in good accordance", 둘째 호 불필요)** ⇒ ③ 은 NMC 에만 나타날 이유가 없어 약하다 — 이 편이 지면 안에 남긴 대조다(원문은 이 논리를 쓰지 않았다).

## (4) ★★★ 2전극 재구성 — "적합이 만족스럽다" 가 귀속 오류를 알리지 않는다는 같은 셀 시연

`[인쇄]` "The impedance of a LTFS:Li0.5In cell in 2 electrodes configuration was reconstructed simply by summing the impedances of WE and CE. The contribution of the electrolyte between RE and CE (i.e., the dashed line in Fig. 7b) was subtracted … The equivalent circuit in Fig. 7a was used to fit this spectrum as well, which lead a satisfactory result … **This implies that the WE and CE impedances cannot be decorrelated in a 2 electrodes measurement.** At lowest frequencies the WE contributes most … the Warburg parameter is in the same order as in 3 electrodes configuration (20% discrepancy). However, the intermediate frequency loop is more significantly affected since its resistance is more than doubled (307 Ω cm² instead of 139). Obviously the difference corresponds to the contribution of the CE and should not be attributed to the WE. Furthermore, **if such a spectrum evolves during cycling there is no way to identify which electrode is at the origin of the variations.**"

- `[도표]` Fig. 7: 중주파 호 꼭짓점 **35 mHz(WE) → 18 mHz(재구성)** · Warburg 표지 **14 → 16 Ω s⁻¹ᐟ²**(`[재현]` +14 %, 인쇄 "20%" — D6) · CE(Fig. 7b) 저주파 부분은 Re ≈300–390 · −Im ≲ 25 Ω cm² 의 납작한 두 호.
- `[해석]` **우리 축에 직결된다**: 같은 모형 족(R-CPE 직렬)에서 **두 전극 호의 합이 한 전극 호 하나로 "만족" 적합**되고, 그 값이 ×2.2 틀린다 — 적합 품질이 귀속을 검사하지 못한다는 것을 **같은 셀 · 같은 상태**에서 보인 표본(`degradation-degeneracy` 의 "좋은 적합 ≠ 식별" 과 같은 구조, 전극 축 판). 폭(근최적 집합)은 재지 않았다 — Q4 는 0.
- 같은 부류의 둘째 문장: TiS₂ `R_CT` 음영 영역 — `[인쇄]` "**Values in this area are only indicative of a negligible Rct since the quality of the fit is not altered upon removal of the corresponding loop.**" — **호 제거 검정**을 비식별 판정으로 쓴 문장(계보 첫 인쇄로 보인다).
- 손 분쇄 NMC 중간 대역: `[인쇄]` "no experimental data allows to discriminate between the different options, and two simple R-CPE elements were employed only for the sake of simplicity" — 모형 선택 비유일성의 인쇄(45호 "physically meaningful" 선택과 대조: 여기는 선택 근거가 "단순성" 이라고 고지).

## (5) 21호가 이 편에 단 인용 셋 — 대조

| 21호 문장 | 이 편 | 판정 |
|---|---|---|
| "a **circular** indium-lithium RE that is located **around the outer perimeter** of a solid electrolyte (SE) separator pellet,16" | 전면 복합층 + 둘레 링 **집전체**(판정 (2)) | ❌ **기하 오독** — 원형은 집전체다 |
| "composite electrodes … In₁Li₀.₅ … (In₁Li₀.₅/SE) have been reported,13,16 whereby lithium was enfolded inside an indium foil to form a brittle In1Li0.5 mixture, which in a second step was ground … and mixed with a sulfidic solid electrolyte" | `[인쇄]` "The Li was enfolded inside the In foil, then the foil was laminated and folded several times … until the alloy became matt and brittle" · 60 : 40 막자 혼합 | ✅ 선다. ⚠ 21호의 같은 문장 "nominal In:Li molar ratio of 1:2 (… In1Li0.5)" 는 **자기 모순**(1 : 2 면 In₁Li₂) — 이 편의 33.2 무게비는 In : Li = 2 : 1(몰) |
| "changes in the low-frequency region of the impedance response of the electrodes upon lithiation and delithiation are **expected**.16" | Li₀.₅In CE(Fig. 9): `[인쇄]` "During first lithiation … the growth of a loop is observed at low frequencies (apex at 540 mHz end of LTFS charge). This process **keeps growing monotonously with time during the subsequent delithiation and lithiation**" · `[도표]` 꼭짓점 표지 **670 mHz(1차 리튬화) → 44 mHz(1차 탈리튬) → 54 mHz(2차 리튬화) → 5.6 mHz(2차 탈리튬)**, 호가 매 구간 커진다(눈금 10 · 10 · 10 · **20** Ω cm²). **방향에 따라 뒤집히는** 저주파 변화는 **Li 금속** CE(Fig. 10) — 도금에 저주파 호(꼭짓점 표지 5.6 · 3.7 mHz) 성장, 박리에 kHz 호(조립 직후 12 kHz · 박리 중 4.7 kHz) 성장 | ⚠ **약한 판으로만 선다** — Li-In 에서는 "변한다" 는 맞고 **방향 의존은 아니다(시간 단조 성장)**. 21호가 본 부류 뒤집힘(꼬리 ↔ 반원, 전류 방향)의 선례는 이 편의 **Li 금속** 쪽이다. 원장 문구 "리튬화에 따른 저주파 변화" 는 "**리튬화 · 탈리튬 모두에서 시간에 따라 단조 성장(Li-In) · 방향 의존은 Li 금속**" 이 정확하다 |
| 저주파 반원 = "charge-transfer resistance.4,16,40–43"(Li 금속) · "thought to represent the charge-transfer resistance.16,44"(InLi-(Li)) | 이 편의 `charge transfer` 5 회는 **전부 양극(WE)**. Li 금속 저주파 호: `[인쇄]` "we believe the growth of the low frequency loop to be associated to formation of a **resistive layer** upon plating" · kHz 호: "an increasing amount of **porosity**"(가설). Li-In 저주파 호: 배정 0 | ❌ **이 편은 음극 저주파 호를 전하이동에 배정하지 않는다** — 21호 배정의 근거로 서지 않는다. `[재현]` Li-In CE 2차 탈리튬 호(5.6 mHz, −Im 꼭짓점 `[도표]` ≈60 Ω cm² → 이상 RC 면 R ≳ 120) ⇒ `C_eff` ≲ ≈0.24 F cm⁻² — "전하이동" 이름표였다면 3-b 에서 실패하는 자릿수(21호 자신의 3-b 도 이 대역에서 실패했다) |

---

# 서지

Romain Dugas, Yves Dupraz, Elisa Quemin, Tuncay Koç, Jean-Marie Tarascon, "Engineered Three-Electrode Cells for Improving Solid State Batteries", *J. Electrochem. Soc.* **168** (2021) 090508, DOI 10.1149/1945-7111/ac208d.
Collège de France (Chimie du Solide et Energie, UMR CNRS 8260) + RS2E (FR CNRS 3459) + CIRB Collège de France(Dupraz — 셀 하드웨어). 투고 2021-06-14 · 수정 2021-08-11 · 게재 2021-09-02. © 2021 ECS(IOP) — 오픈액세스 표기 없음. ERC ARPEMA(670116). Data availability "N.A". SI 없음.
참고문헌 29. 계보 편 인용: ref 7 = **Nam 2018**(41호) · ref 9 = **Schlenker 2020**(46호) · ref 10 = **Solchenbach 2016**(47호 — `[인쇄]` 금도금 W 선이 "may not provide a stable voltage upon cycling.10" 의 근거로) · ref 11 = **Ikezawa 2020**(40호) · ref 17 = **Santhosha 2019**(42호 — 622 mV) · ref 15 = Costard … Ivers-Tiffée 2017 *JES* 164, A80(40호 1.55 V 의 출처와 같은 논문 — 여기서는 "ideal geometry" 근거).

# 셀 · 방법 (전부 `[인쇄]`)

- **하드웨어**: PEI 원통 몸체를 둘로 나누고 스테인리스 링(기준극 접점) + **15 µm Al 박에 ∅8 mm 구멍**을 가운데 물림 · 나사 6 + O-링 2 로 기밀 · SS 피스톤 ∅8 mm 두 개(판 2 장에 달림, 두 번째 나사 6 조로 닫음) · 나일론 페럴 · 절연 인서트. 조임 토크 **2.3 Nm = 1 t cm⁻²**(빈 셀에서 힘 센서로 교정, "initial pressure").
- **조립**: SE 펠릿 45 mg 을 다이에서 4 t cm⁻² × 3 min → ① RE 복합 분말 + 펠릿 + 피스톤, 1 t cm⁻² 수 초("the tension it applies on the wall of the cell maintains it at the level of its current collector") → ② 뒤집어 SE 분말 40 mg, 1 t cm⁻² 수 초 → ③ WE · CE 분말 양쪽, **4 t cm⁻² × 15 min** → 닫고 글러브박스 밖. WE 는 얇은 SE 층 쪽.
- **재료**: WE = LiNi₀.₆Mn₀.₂Co₀.₂O₂(NMC) · TiS₂(Aldrich) · 자체 합성 Li₁.₁₃Ti₀.₅₇Fe₀.₃S₂(LTFS), 활물질 : SE = 70 : 30 wt, 막자 손 분쇄 또는 Spex 8000M 20 min(BPR 20 : 1), **탄소 0**. SE = β-Li₃PS₄(용액 합성, 두 배치) 또는 Li₆PS₅Cl(고상). CE = Li₀.₅In : SE 60 : 40(TiS₂ 셀은 Li₀.₉In : β-LPS) · **RE = 같은 Li₀.₅In : SE 60 : 40**. "No attempt to optimize this mass ratio was made."
- **Li 금속 셀**: Li 박 긁고 유리관으로 압연, ∅8 mm 펀칭 · 힘 센서 프레임 **45 kg cm⁻²** · 글러브박스 안 사이클.
- **전기화학**: 실온(≈24 °C) · 황화물 C/25 · NMC C/20(C = 활물질 1 mol 당 Li 1 mol 을 1 h) · VMP3 · LTFS 1.2–2.4 · NMC 2–3.6 · TiS₂ 0.8–2.4 V vs LiIn/In · 2 h 마다 멈추고 1 h 휴지 뒤 EIS(15 mV, 200 kHz–10 mHz 10 점/decade + 10–1 mHz 5 점, 한 스펙트럼 < 75 min) · EC-Lab 적합 · SE 전도도 MTZ 5 MHz–1 Hz(2전극) · "repeated at least twice".

# 결과 — 절별 해체

## §1 SE 펠릿 (Fig. 3)
`[인쇄]` β-LPS 두 배치 비저항 **4,670 · 4,250 Ω cm**(≈0.2 mS cm⁻¹), 고주파 호 꼭짓점 **615 kHz ↔ 4.83 MHz**(배치 간 유전율 차 — "low repeatability") · argyrodite **3.7 mS cm⁻¹**, 꼭짓점 ≈190 MHz(측정 불가 대역).
`[도표]` Fig. 3a 적합 원호의 Re 절편 배치 1 **≈4,490** · 배치 2 **≈4,250 Ω cm**(137 px/1000 Ω cm) — 배치 1 인쇄값 4,670 과 ≈4 % 차(D3).

## §2 2전극 최적화 (Fig. 4)
LTFS vs Li₀.₅In:β-LPS. 손 분쇄 첫 충전 0.7 Li = 160 mA h g⁻¹, 이후 <180 · 볼밀 첫 충전 ≈95 % Li 추출, 가역 243(손 분쇄 최대의 ×1.35). 손 분쇄는 4 사이클째 최대 → 10 사이클 −3.7 % · 볼밀 7 사이클 −4.6 %. 쿨롱 효율 첫 사이클부터 >97.5 %(`[도표]` 97.6–100.4 %) ↔ 순수 Li + In 금속 음극 <70 %(ref 18) — "a purely metallic anode limits the cell's discharge".
★ `[인쇄]` 손 분쇄 용량 증가: "suggests that a higher amount of active material becomes accessible to both e⁻ and Li⁺ … **The mechanism for such activation with a solid electrolyte is unclear; it possibly involves local deformation of the electrolyte in the cathode composite as a consequence of the pressure variation upon cycling, which could slightly improve the double percolation.**" — `[해석]` **접근 가능 분율이 사이클에 따라 *증가*한다는 가설**(카드의 `θ(N)` 과 같은 양의 반대 방향) — 측정 0.
★ 2전극 귀속: 첫 충전이 이후보다 100 mV 높고 평균 방전 전압 −30 mV / 5 사이클 — "Since the counter electrode is expected to remain at a constant voltage of 622 mV vs Li⁺/Li,17 these features can be attributed to the LTFS cathode material" + 액체셀 곡선과 비교.

## §3 3전극 전압 (Fig. 5)
LTFS 볼밀 가역 233 · NMC 볼밀 가역 ≤60, 첫 효율 40 %, 2.3–3.1 V 초기 경사(27 mA h g⁻¹; 탄소 없이도 → 볼밀이 반응성 키움) · NMC 손 분쇄 경사 2.3 mA h g⁻¹, 효율 64 %, 가역 60, 분극 ±150 mV(C/20) · **NMC argyrodite**: 분극 ×1/3, 첫 충전 140 → 방전 108(77 %) — `[인쇄]` "The missing 33% irreversible capacity (31 mA h g⁻¹) … intrinsic to the active material itself" · 2 사이클 겹침.
CE 창: 판정 (1). `[도표]` Fig. 5d(argyrodite) CE ≈0 ± 0.02 V.

## §4 3전극 EIS (Fig. 6)
모두 2차 방전 중간. R-CPE 직렬 + 마지막 CPE(반사 경계). `Z_CPE = 1/[Q(j2πf)^α]`, `f₀ = 1/[2π(RQ)^{1/α}]`.
- (a) LTFS:β-LPS 볼밀: SE 호 α 0.98 · **283 Ω cm²** · f₀ 340 kHz — `[인쇄]` "corresponds to a conductivity of **1.9 mS cm⁻¹**"(D1) · 펠릿 측정과 "14% lower conductivity and a 10% higher value of log(f0)" · 둘째 R-CPE = 전하이동(+ 복합체 Li⁺ 전도 일부) · CPE α 0.53(≈45°) = 입자 확산. `[도표]` 중간 호 꼭짓점 35 mHz, Warburg 14 Ω s⁻¹ᐟ².
- (b) NMC 볼밀: Re > 2.2 kΩ cm² at 1 mHz · SE 는 펠릿 값을 대입 + **둘째 고주파 호 32 kHz(α 0.85)** "required to match" — "a single R-CPE loop … would extend until negative values of Re(Z) … lacks physical sense" · 전하이동 12 Hz, **1750 Ω cm²**(LTFS 의 12.5 배).
- (c) NMC 손 분쇄: <900 Ω cm² · 고주파가 SE 층 몫보다 ≈50 % 큼 · 저주파 호 f₀ ≈30 µHz(대역 밖) · 15 kHz–20 Hz 복합 응답 "Z?" = R-CPE 둘(단순성).
- (d) NMC argyrodite: 한 자릿수 작음 · SE 호 ≈250 MHz · 고주파가 SE 층 15 Ω cm² 와 안 맞음 → 둘째 호 · 저주파 전하이동 뒤 45°(NMC 확산이 보인다). `[도표]` 전하이동 호 꼭짓점 54 mHz, R ≈10–15 Ω cm², Warburg 3.3 Ω s⁻¹ᐟ².
- 저자 결론: 산화물 양극 + 황화물 SE 계면 문제 → 코팅 필요(ref 25).

## §5 2전극 재구성 (Fig. 7) — 판정 (4)

## §6 `R_CT` 상태 추적 (Fig. 8)
LTFS: 3 요소 회로가 사이클 전체 적합 · 중간 호 변화를 `R_CT` 로 — 근거 `[인쇄]` "Since the ion conductivity of β-LPS in the cathode composite is not expected to be dependent on the state of charge, variations in resistance of this loop can be attributed to the charge transfer to the active material, RCT." 2차 사이클 충전 20–45(중간 최소) · 방전 75 → 230 Ω cm². 첫 충전 10–15. **최대값 사이클마다 증가, 5 사이클 끝 1500 Ω cm²**. 충방전 비대칭 → 음이온 산화환원 경로 차(refs 26, 27).
TiS₂: 충방 스펙트럼 비슷 · 리튬화에 10–12 → <2.5 Ω cm² · `[인쇄]` "reversibility above 99% (94% at 1st cycle)"(뒤 문단 "> 94%" — D5) · 5 사이클 >680 h → 기준극 안정성 · 음영(<2.5) = 제거 검정 문장.
⚠ 본문 "The second cycle with this material … is plotted in **Fig. 6c**" = Fig. 8c(D4).

## §7 음극 두 종 (Fig. 9 · 10)
- Li₀.₅In:β-LPS CE(1 t cm⁻²): `R_el` 변동 ±17 %(1 사이클) · ±3 %(2 사이클) → **스펙트럼을 `R_el` 에 맞춰 정렬**(가로축 절대값 없음) · 저주파 호 단조 성장(판정 (5)).
- Li 박 CE(45 kg cm⁻²): LTFS 분극 200 → 500 mV — `[인쇄]` "**It simply originates from the lower applied pressure** (45 kg cm⁻²) used for running the Li-based cell as compared to the In0.5Li one (1 t cm⁻²)"(D8) · 가역 180 mA h g⁻¹ · 첫 효율 93 % · Li 분극 "at least two times greater … despite the low current density of 27 µA cm⁻²". SE 호 구분 안 됨 · 조립 직후 12 kHz 호 → 도금 2 h 안에 사라지고 저주파 호 성장 → 박리에 저주파 호 곧 소멸 · 중주파 호 성장 → 2차 도금 마지막 세 스펙트럼 3.7 mHz 겹침("steady state") → 2차 박리 중주파 호 더 크게.
- 결론 문장: 3전극이 도금/박리 영역을 가르고, 대칭 Li\|Li 셀은 "both plating and stripping occur simultaneously" 라 못 가른다. 해석은 가설(다공 · 저항층).
- `[재현]` **4단계(DC ↔ EIS) — Li 금속 CE**: Fig. 10a 가지 ↔ 휴지 끝 `[도표]` 과전압 ≈0.06–0.15 V at 27 µA cm⁻² ⇒ **DC ≈2–6 kΩ cm²** ↔ Fig. 10b–e 스펙트럼 폭 `[도표]` ≈0.5–1.2 kΩ cm²(눈금 막대 판독, 거침) ⇒ **×≈2–10** — 1 mHz 아래 과정 또는 전류 중 ↔ 휴지 상태 차(저자: 저주파 호가 "fast disappearance as the current is reversed"). 46호(DC ≥ ×3 EIS 합)와 같은 방향.

# 곱 축퇴 처방 — 서른한 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | `R_CT`(N, SOC) 연속 추적(Fig. 8b · d) — `Q` · α **미인쇄**, 꼭짓점 주파수는 Fig. 6 · 7 네 상태뿐 | ❌ 상태축 `C` 없음 |
| **2단계** 면적 대조군 | 손 분쇄 ↔ 볼밀(같은 NMC · SE) — 볼밀이 계면 반응성도 바꾼다(`[인쇄]` 경사 27 ↔ 2.3 mA h g⁻¹) | ⚠ 면적 · 화학 교락 |
| **3단계-a** `Ea` | 실온 한 점 | ❌ |
| **3단계-b** `C` 상한 | `[재현]` 이상 RC: LTFS 139 Ω cm² · 35 mHz → **≈33 mF cm⁻²** · NMC 볼밀 1750 · 12 Hz → **≈7.6 µF cm⁻²** · NMC argyrodite ≈10–15 · 54 mHz → **≈0.2–0.3 F cm⁻²**(기하 면적당) | ✅ **"전하이동" 이름표 — 느린 두 호가 이중층 자릿수를 넘는다**(LTFS 는 복합체 거칠기 ≳10³ 필요, argyrodite NMC 는 ≳10⁴); 볼밀 NMC 는 통과. 전극 질량 미인쇄라 거칠기 환산은 범위만. **여섯 번째 실패 계열**(19 · 20 · 21 · 43 · 47호 다음) — 여기서는 확산(화학 용량) 대역과 겹친 호 |
| **4단계** 시간 영역 | Li 금속 CE: DC ≈2–6 ↔ EIS ≈0.5–1.2 kΩ cm²(§7) | ✅ 부분 — 음극 판, ×≈2–10 이 대역 밖 또는 전류 중 상태 |

`[해석]` 카드의 곱: LTFS `R_CT` 최대값의 사이클 증가(→1500 Ω cm²)는 `R_CT ∝ 1/(A_eff·k)` 의 **어느 인자인지 가르지 않았다** — 저자는 SE 전도도 SOC 무관 논증(소거법)으로 호를 `R_CT` 로 지정하고, 원인을 충방 비대칭 → 음이온 경로(`k` 쪽)로 읽었다. 같은 셀의 용량 변화(Fig. 4 −4.6 %/7 사이클, 2전극 · 다른 셀)와의 대조는 없다.
**처방에 더하는 것**: 새 줄 후보 **"호 제거 검정 + 2전극 합 재구성 — 적합 품질이 귀속을 알리지 않는다는 것의 같은 셀 시연"** — (i) 한 호를 빼도 적합 품질이 같으면 그 호의 `R` 은 "지표" 로만 쓴다(`[인쇄]` TiS₂ 음영) (ii) 곱을 가르기 전에 **2전극 스펙트럼을 한 전극 모형으로 적합하면 '만족' 이 나오는지** 3전극 반쪽 합으로 먼저 본다 — 만족이면 2전극의 그 호는 귀속 불가(이 편 ×2.2).

# 칸별 요약 (채움표 행)

| 칸 | 판정 |
|---|---|
| Q1 정량 | **없다 — `θ(N)` 0/48.** `contact` 3 회 전부 기준극 전기 접점. `percolat*` 1 = 손 분쇄 활성화 가설("double percolation" 개선) — **접근 분율 증가 가설**, 측정 0 |
| Q2 독립관측 | **없다** — `R_CT`(N) 는 소거법 배정 · 면적/`k` 미분리 · 용량 분해 0 |
| Q3 라벨층위 | 층 하나 — **fit-by-elimination + removal-test flag**: `R_CT` 는 "SE 는 SOC 무관" 소거로 지정, 제거 검정에서 적합 불변인 값은 "indicative" 로 표시 · "repeated at least twice" 산포 0 |
| Q4 유일성 | **0/48 — 마흔 번째 성질 "비식별성을 두 번 인쇄했다(2전극 합이 한 전극 모형으로 '만족' 적합되며 ×2.2 틀린다 · 제거해도 적합이 안 변하는 호는 지표일 뿐) — 폭은 재지 않았다"**. `identifiab` · `uncertaint` 0 · `decorrelat*` 1 |
| Q5 Li-In | **+0.5 — 스물네 번째 형태**(판정 (1)). 누설 0/48 |
| Q6 압력 | 이동 없음 — 제조 4 t cm⁻²(≈392 MPa) 15 min · 운전 1 t cm⁻²(≈98 MPa, 초기 토크 교정) · Li 셀 45 kg cm⁻²(≈4.4 MPa, 힘 센서). 층 하나: **"분극 차는 압력 탓" 단정이 음극 교체와 교락**(D8) |
| Q7 dead Li | 해당 없음(무음극 아님) — Li 금속 도금/박리의 주파수 영역 분리(3전극)는 칸 밖 기여 |
| Q8 화학 · OCP | LTFS(음이온 산화환원, 첫 충전 +100 mV) · NMC622 · TiS₂(경사 평탄) — OCP 곡선 수치 0 |

---

# 어긋남 (D)

| # | 인쇄 | 그림 · 계산 | 성질 |
|---|---|---|---|
| **D1** | SE 호 283 Ω cm² "corresponds to a conductivity of 1.9 mS cm⁻¹" | 자기 Fig. 3a β-LPS ≈0.2 mS cm⁻¹ · `[재현]` 40 mg · 0.503 cm² · 283 Ω cm² → 0.15(치밀 1.87 g cm⁻³) … 0.19 mS cm⁻¹(1.48) | **×10 — 0.19 의 오기로 보인다.** 이어지는 "14% lower conductivity" 의 방향도 흔들린다(펠릿 0.21 > 0.19) |
| **D2** | "The missing **33%** irreversible capacity (31 mA h g⁻¹)" | `[재현]` 140 − 108 = 32 → **23 %**(같은 문장 앞 "77% efficiency" 와 합이 100) | 오기 |
| D3 | β-LPS 배치 1 "4,670 Ω cm" | `[도표]` 적합 원호 절편 ≈4,490 | ≈4 %, 판독 근사 |
| **D4** | TiS₂ 2차 사이클 "plotted in Fig. 6c" | Fig. 8c | 그림 번호 |
| D5 | TiS₂ "above 99% (94% at 1st cycle)" | 뒤 문단 "excellent reversibility (> 94%)" | 같은 양 두 표현 |
| **D6** | Warburg "20% discrepancy" | `[도표]` 표지 14 ↔ 16 Ω s⁻¹ᐟ² = 14 % | 표지 반올림일 수 있음 |
| **D7** | Fig. 9b "apex at 540 mHz end of LTFS charge" | `[도표]` 그림 표지 **670 mHz** | 본문 ↔ 그림 |
| **D8** | Li 셀 분극 증가 "**simply originates** from the lower applied pressure" | 압력(1 t → 45 kg cm⁻²) · 음극(Li₀.₅In 복합 → Li 박) · 셀이 동시에 바뀜, 압력만 바꾼 대조 0 | 교락된 단정 |
| **D9** | TiS₂ "charge-discharge traces neatly superimposed during the first 5 cycles" | Fig. 8d 는 사이클별 **다른 패널** — 겹침이 그림에 없다 | 증거 제시 형식 |
| D10 | "In0.5Li"(2 회) | 나머지 23 회 "Li0.5In" | 표기 |
| D11 | 기준극 조성 "Li0.5In"(초록 · 방법) | 결론 "stable RE voltage" 의 대상 셀은 TiS₂(CE Li₀.₉In, RE Li₀.₅In) | 기록 |
| **D12** | (21호) "circular … RE … around the outer perimeter" | 전면층 + 링 집전체 | **교차 편 — 기하 오독** |
| **D13** | (21호) Li · InLi 저주파 호 "charge-transfer … 16" | 이 편 음극 저주파 호 배정 = "resistive layer"(Li) · 없음(Li-In) | **교차 편 — 인용 불지지** |
| D14 | (21호) "In:Li molar ratio of 1:2 (… In1Li0.5)" | 이 편 무게비 33.2 → 몰비 2 : 1 | 교차 편 — 21호 자기 모순 |
| D15 | (원장 · 21호) "리튬화에 따른 저주파 변화" | Li-In: 방향 무관 시간 단조 성장 · 방향 의존은 Li 금속 | 교차 편 — 문구 정밀화 |

# 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전; IOP 표지 쪽 제외). SI 없음.
NFKC 변경 본문 **97 자**(`ﬁ` 92 · `ﬂ` 5) — 열 변화 0. 소프트 하이픈 0 · 줄끝 하이픈 **20 곳**(이어도 지문 열 변화 0; "ball-milled" · "charge-discharge" · "R-CPE" 는 진짜 하이픈).

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | **1**(토크 ↔ 압력 교정 — 기준 전위 아님) | 0 | 0 | 0 | 0 | **0**(압력은 "t cm⁻²" 6 · "kg cm⁻²" 3) |

Q5 보조: `leak` **0** · `drift` **0** · `assum*` **0** · `expect*` **4**(622 mV 전제 1 · 전도도 1 · 축대칭 artefact 1 · SE SOC 무관 1) · `622` **1** · `0.62` 0 · `stab*` 5(초록 · 결론 · TiS₂ 680 h · 선행 두 편) · `hundreds` 1 · `680` 1 · `Li0.5In` 23 · `In0.5Li` 2 · `Li0.9In` 2 · `plateau` 2(둘 다 LTFS — Li-In 평탄 0) · `reference` 11 · `RE` 22 · `bipolar` 0 · `inhomogen*` 1(CE).
EIS 보조: `artefact` **5**(`artifact` 0) · `symmetr*` 4 · `axisymm*` 1 · `fit*` 10 · `decorrelat*` **1** · `charge transfer` 5(전부 WE) · `capacitan*` 1(SE 기하 용량) · `Warburg` 1 · `error` · `reproducib*` · `ambigu*` 0 · `repeat*` 2 · `prove` 1("To prove its versatility").
곱 축퇴 보조: `contact` 3(전부 기준극 전기 접점) · `percolat*` 1 · `porosit*` 1(Li 계면) · `pressure` 9 · `Coulomb*` 4 · `efficien*` 8 · `side reaction` 1 · `decompos*` 1 · `degrad*` · `aging` · `isolat*` · `dead` 0.
`[해석]` **영점의 낱말이 `expect*` 에 들어 있다** — 21호 "calculated based on" · 43호 "Suppose" · 45호 "therefore exhibited" 와 같은 부류이고, 기준 전위 어휘(`calibrat` · `drift` · `leak`)는 0. 대신 **"V vs LiIn/In" 축이 끝까지 환산되지 않아** 가정이 결과에 들어갈 자리가 2전극 귀속 한 문장뿐이다.

---

# 그림 — 본 것 / 안 본 것

크로퍼 10 장(`wiki/raw/figures/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer/`) — **10 장 다 봤다**(Fig. 1–10).
화소 판독(PDF 원본 래스터에서): **Fig. 3a**(137 px/1000 Ω cm — 적합 원호 절편) · **Fig. 5c**(11.9 mV/px — CE 휴지 눈금 끝) · **Fig. 7**(1.744 px/Ω cm² — WE · CE 쪽 고주파 절편) · **Fig. 9a**(9.8 mV/px — CE 창, 눈금이 상자 벽과 겹쳐 휴지 끝 판독 불가) · **Fig. 10a**(9.8 mV/px — Li 금속 CE 휴지 눈금 끝). 나머지(Fig. 1 · 2 모식도 · 4 · 6 · 8 · 9b–e · 10b–e)는 눈 판독.
본문과 어긋난 그림: Fig. 3a(D3) · Fig. 7(D6) · Fig. 8(D4 · D9) · Fig. 9b(D7).
본문이 말하지 않은 그림 내용: **Fig. 10a 의 Li 금속 ↔ 기준극 휴지 전위 ≈−0.62 V**(판정 (1)) · Fig. 5c 의 CE 휴지 복귀(≈0 ± 0.02 V).

# 계보에서의 자리

`[해석]` … → 셀 안 도금 Li · 소모품 기준극(45호) → 영점이 들어가지 않는 자리(46호) → 원전 측정 + 사용 조건, 액체(47호) → **같은 재료 기준극으로 상대극 창을 재고 용량 오차로 번역, 측정 축 그대로(48호, 2021)**.
- 시간 순서: Nam 2018(41호 SI — Li 금속 **기준극**으로 Li₀.₅In CE, `[도표]` ≈0.621) → Santhosha 2019(42호 액체 0.622) → **이 편 2021(Li 금속 **상대극**을 Li₀.₅In 기준극으로, `[도표]` ≈0.62 — 둘째 ASSB 안 그림 판독, 둘 다 수 미인쇄)** → Hertle 2023(45호 −618 mV 인쇄).
- In 가지 영점의 경로: 이 편은 Santhosha(42호) 경로를 쓴다 — 41호 Jung 2008 경로 인용 0, 41호(Nam)는 **기준극 설계 선례**로만 인용("adding a Li or Li-In electrode to provide a stable reference potential.7,8", 그리고 "No EIS in 3 electrodes configuration was reported with such cells").
- 금선 가지 읽기: 이 편은 47호를 "may not provide a stable voltage upon cycling" 의 근거로 읽는다 — 47호의 인쇄(>500 h, 조건부 안정)와 **조건(초기 창 · 온도 이력 · 고전압 수명)** 중 불안정 쪽만 가져갔다.

# 후속 (서지 기준, 미열람)

| 서지 | ref | 왜 |
|---|---|---|
| **Costard, Ender, Weiss, Ivers-Tiffée 2017 *JES* 164, A80** | 15 | ★★★ "ideal geometry"(전면 기준층)의 근거 **이자** 40호 R-LTO 1.55 V 의 유일 근거 — 두 번째 지목, 큐 없음 |
| Ender, Illig, Ivers-Tiffée 2017 *JES* 164, A71 | 6 | 3전극 artefact 원전(40호 ref 10 과 같은 편) — 전면층 기하의 artefact 조건 |
| Klink … La Mantia 2012 *Electrochem. Commun.* 22, 120 | 5 | 3전극 artefact(45호 ref 19 와 같은 편) |
| Dees, Jansen, Abraham 2007 *JPS* 174, 1001 | 4 | 미세 기준극 조건(47호 ref 15 와 같은 편) |
| Kasemchainan … Bruce 2019 *Nat. Mater.* 18, 1105 | 8 | 사후 추가 Li/Li-In 기준극 · 임계 박리 전류(46호 ref 13 과 같은 편) |
| Marchini, Saha, Alves Dalla Corte, Tarascon 2020 *ACS AMI* 12, 15145 | 18 | 순수 Li + In 금속 음극 → LTFS 첫 효율 <70 % — "상대극이 방전을 끊는다" 표본 |
| Zhang … Janek 2017 *ACS AMI* 9, 35888 | 19 | NMC 초기 경사 = SE 분해(탄소 촉진) |
| Kaiser … Roling 2018 *JPS* 396, 175 | 23 | 복합 양극 전송선 모형 — 손 분쇄 NMC "Z?" 대안 |

큐 50–59 인용: **0**(Barai 2018 · Miß 2022 · Illig 2012 · Oh 2025 · Ren 2023 · Neumann 2021 · Hlushkou 2018 · Bielefeld 2022 · 2020 · Asheri 2023 — ref 6 은 Ender · Illig · Ivers-Tiffée **2017**, 큐 52 Illig **2012** 와 다른 편). 큐 41 · 42 · 43 · 47 · 48 대상(40 · 41 · 42 · 46 · 47호)은 인용.

# 이 digest 가 주장하지 않는 것

- **"이 셀의 기준극이 0.62 V vs Li 로 측정됐다" 를 원문 명제로 쓰지 않는다** — Fig. 10a 휴지 눈금 끝의 **우리 화소 판독**(9.8 mV/px, JPEG, 1 h 이상 휴지 · 완전 이완 미확인, Li 표면 상태 미확인)이다. 원문의 영점은 인용 622 mV 다.
- **쌍극 교환이 이 셀에서 일어났다고 하지 않는다** — 합금 부피분율 ≈30 % 와 전자 경로 필요성에서 나온 **가능성**이고, 크기 추정(C/20 급에서 mV 이하)은 층 두께 · 저항을 가정한 것이다.
- **고주파 "둘째 호" 가 기준극 artefact 라고 하지 않는다** — 같은 기준층을 쓴 LTFS 셀 대조가 오히려 그 후보를 약하게 만든다.
- **21호가 틀렸다고 단정하지 않는다** — 기하 묘사(D12) · 전하이동 인용(D13)은 이 지면과 안 맞지만, 21호의 "저주파 변화가 예상된다" 는 약한 판으로 선다. 21호의 자기 결과(방향 의존 부류 뒤집힘)는 이 편과 무관하게 21호 데이터로 선다.
- **D1 을 확정 오기로 쓰지 않는다** — 두께 · 밀도 미인쇄라 0.15–0.19 mS cm⁻¹ 범위 계산이고, "×10" 은 자기 Fig. 3a 와의 대조까지다.
- **`R_CT` 증가가 접촉 손실이라고도, 아니라고도 하지 않는다** — 곱의 어느 인자인지 이 지면은 가르지 않았다.
