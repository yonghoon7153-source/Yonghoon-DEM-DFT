---
title: "Lee, Fujiki, Jung, Suzuki, Yashiro, Omoda, Ko, Shiratsuchi, Sugimoto, Ryu, Ku, Watanabe, Park, Aihara, Im, Han 2020 — High-energy long-cycling all-solid-state lithium metal batteries enabled by silver-carbon composite anodes (Nature Energy 5, 299-308)"
source_url: local-upload/06._High-energy_long-cycling_all-solid-state_lithium_metal_batteries_enabled_by_silver_carbon_composite_anodes.pdf
source_url_si: local-upload/06._Sup_High-energy_long-cycling_all-solid-state_lithium_metal_batteries_enabled_by_silver_carbon_composite_anodes.pdf
source_url_note: "파일명과 내용이 일치한다 (4호에서 있었던 본문/SI 뒤바뀜 없음). 본문 10쪽 · SI 18쪽, 쪽수와 첫 쪽 텍스트로 각각 확인했다 — SI 1쪽에 'SUPPLEMENTARY INFORMATION / In the format provided by the authors and unedited.'"
source_doi: 10.1038/s41560-020-0575-z
pdf_sha256_main: 3452770465c31f45acbb8988f2eb58386cfd25cb378ac8c6a09db564684fd2a9
pdf_sha256_si: 120d136d99668016ebb6fd17d3e0778ae872b6600441c4b16161f390f8e10391
ingested: 2026-09-16
sha256: 27a833607ca9b1267d3ec264e5c6d0d2f956fd4c91d41b93f685e87db4148059
---

# 수집 목적

Yong-Gun Lee¹, Satoshi Fujiki², Changhoon Jung¹, Naoki Suzuki², Nobuyoshi Yashiro²,
Ryo Omoda², Dong-Su Ko¹, Tomoyuki Shiratsuchi², Toshinori Sugimoto¹, Saebom Ryu¹,
Jun Hwan Ku¹, Taku Watanabe², Youngsin Park¹, Yuichi Aihara²(교신), Dongmin Im¹(교신),
In Taek Han¹ — **"High-energy long-cycling all-solid-state lithium metal batteries
enabled by silver–carbon composite anodes"**, *Nature Energy* **5** (2020) 299–308,
doi `10.1038/s41560-020-0575-z` (Received 2019-07-25 / Accepted 2020-02-07 /
Published online 2020-03-09) 의 **절별 해체분석** — 본문 PDF 10 쪽 + Supplementary
Information 18 쪽.

¹ Samsung Advanced Institute of Technology (SAIT), Samsung Electronics Co., Ltd,
130 Samsung-ro, Yeongtong-gu, Suwon-si, Gyeonggi-do 16678, Korea.
² Samsung R&D Institute Japan, Minoh-shi, Osaka 562-0036, Japan.
`[인쇄]` Competing interests: "All the authors are employed at Samsung Electronics Co. Ltd."
`[인쇄]` Acknowledgements: "This work was supported by funds from Samsung Electronics Co. Ltd."
→ **저자 16 명 전원이 산업체 소속이고 자금도 같은 회사다.** 이 계보에서 **첫 산업체 논문**이다.

**이 위키 `assb` 섹션의 6호 논문이다.** 액체셀 계열과 **섞지 않는다** — 음극 축이
다르다. 닻은 `questions/assb-contact-loss-vs-lampe.md`.

> ✅ **업로드 파일명 확인 (4호의 뒤바뀜 사고 재발 없음).** 파일명이 내용과 **맞다**:
> `06._High-energy…pdf` = **본문 10 쪽** (1 쪽에 `Articles` + 초록 + `Nature Energy |
> VOL 5 | APril 2020 | 299–308`), `06._Sup_High-energy…pdf` = **SI 18 쪽**
> (1 쪽이 표지이고 `SUPPLEMENTARY INFORMATION / In the format provided by the authors
> and unedited.` 가 찍혀 있다; 2 쪽부터 Supplementary Fig. 1 이 시작). 쪽수와 첫 쪽
> 텍스트로 각각 확인했다. `pdf_sha256_main` / `pdf_sha256_si` 는 업로드 파일을
> **직접 `sha256sum`** 한 값이다.

**★ 이 논문이 이 계보에서 하는 일** — 1~5 호가 전부 **양극 또는 Li 금속 음극**이었다.
6호는 **무음극(anode-free)** 이다. 음극 자리에 Li 금속 박이 없고, **Ag 나노입자 +
카본블랙 복합층(5–10 µm)** 만 SUS 집전체 위에 있으며, 충전 때 양극에서 나온 Li 가
그 층을 지나 **집전체와 Ag–C 층 사이에** 금속으로 쌓인다. 그래서 이 논문은
닻 카드의 미결 항목 3(**dead Li 와 SEI Li 를 가르는 관측이 있나**)과 ASSB 인수인계
노트 §2-A3 이 열어 둔 자리 — **무음극에서 `LLI` 는 무엇인가** — 를 정면으로 때린다.

그리고 **압력 축을 새로 쪼갠다**: 이 논문에는 압력이 **두 개**다.
**제작 압력 490 MPa (온간 등방압, WIP)** 와 **운전 압력 2 MPa (지그)**.
5호(Doux)가 Li 금속에 준 상한 **75 MPa** 는 **운전 압력**이었는데, 6호는 제작에서
그 **6.5 배**를 쓰고도 셀이 살아 있고, **운전에서는 `[인쇄]` 4 MPa 를 넘으면 단락
확률이 올라간다**고 적는다. → **두 압력은 같은 축이 아니다.**

---

# 0. 이 digest 를 쓰기 전에 실제로 본 것

크로핑 **26 장**(본문 그림 5 + SI 그림 18 + SI 표 3) 중 **그림 12 장을 Read** 했다.
표 3 장은 도구 권고대로 PDF 텍스트로 읽었다 (이미지보다 정확하다).

| 본 것 | 왜 |
|---|---|
| **Fig. 6 (p8 전면)** | ★★ 이 논문의 전기화학 본체 — 율·온도·**1000 사이클 용량유지율 + CE**. ⚠ 크로퍼가 이 그림을 "영역 없음" 으로 **제외**해서 `pymupdf` 로 **8 쪽을 직접 200 dpi 렌더**해 봤다 |
| Fig. 4 | ★★ 컷오프 전압 ↔ 면적용량 5 점 사상 + 도금 Li 두께 3 점. **음극 쪽 전압축** |
| Fig. 5 | ★★ TEM/EELS/SADP/XRD — **Li₉Ag₄ 상**과 **EELS Li 맵** |
| Fig. 2 | 대조군(맨 SUS)의 사이클 붕괴 모양 |
| Fig. 3 | SEM–EDS 도금/탈리, Ag 분포 (1 / 100 사이클) |
| Fig. S4 | ★ **Ag–C \| Li 반쪽전지** 전압곡선 + Cu/SUS CV |
| Fig. S5 | ★ 100 사이클 후 **충전/방전 상태** 단면 SEM — dead Li 의 (음성) 증거 |
| Fig. S6 | C 단독 / Ag 단독 층 대조 |
| Fig. S7 | ★ Ag–C **유/무** 초기 충방전 곡선 — 첫 사이클 비가역분 |
| Fig. S11 (+Table S2) | ★★ **운전 압력 2/3/4 MPa** 율특성·사이클 |
| Fig. S12 | ★★ **무압 운전** 0.1C/0.1C 곡선 |
| Fig. S13 | ★ Ag:C 조성 스윕 — **CE 축이 99.4–100.0** 으로 확대돼 있다 |
| Fig. S16 | ★★ 0.5C/0.5C **사이클 1/200/400/600/800/1000 의 V–Q** |

**안 본 것 (솔직히 밝힌다)**: Fig. 1 (모식도 + Arrhenius + Raman/XRD + LZO TEM —
셀 구성 확인용이고 우리 축이 아니다), Fig. S1·S2·S3 (SSE 필름 사진·용매·Raman),
Fig. S8·S9 (C 와 Ag 의 SADP 보조), Fig. S14 (조성별 곡선), Fig. S15 (온도별 Nyquist —
캡션의 숫자 `25 °C 50 Ω cm² ↔ 60 °C 5 Ω cm²` 만 텍스트로 인용), Fig. S17·S18
(적층수·5 Ah 셀), Fig. S19 (가열 시험).
⚠ **Fig. S10 (WIP 전/후 SEM)** 은 크로퍼가 `그래픽 없음(img0/draw0)` 으로 제외했다.
SI 11 쪽을 직접 렌더해 두었으나 **판독 가치가 낮다고 판단해 열지 않았다** — 그래서
`Q1`(접촉 손실 정량)에 대해 이 논문이 가진 **유일한 형태학 증거를 나는 보지 않았다.**
아래 §10 Q1 의 판정은 **Table S2 의 두께 수치와 본문 서술에만** 근거한다.

**그림에서만 읽은 값은 전부 `[도표]`** 로, 내가 계산한 값은 **`[재현]`** 으로,
원문에 인쇄된 값은 **`[인쇄]`** 로 표시한다. 표시 없는 문장도 전부 원문 근거이며,
내 추론에는 **`[해석]`** 을 붙였다.

★ **Fig. 6g 는 눈으로만 읽지 않았다.** PDF 텍스트층에서 축 눈금 라벨의 좌표를 뽑아
(`101` → y=1839 px, `95` → y=2435 px @400 dpi; 왼쪽 `100` → y=1850, `0` → y=2435)
**축을 먼저 교정한 뒤** 빨강(CE)·파랑(용량유지율) 화소의 중앙값을 사이클 구간별로
계산했다. 교정의 타당성은 **논문이 인쇄한 값으로 검증**했다 — 내 판독이 600 사이클
94.9 %, 1000 사이클 89.4 % 를 주고 본문이 `[인쇄]` 95 %, 89 % 라고 적는다. 일치한다.
같은 방법을 Fig. S16 의 곡선 끝점에도 썼다.

---

# 1. 원문에 없어서 확인이 필요한 것 (공백 먼저)

| # | 공백 | 왜 걸리나 |
|---|---|---|
| **G1** | ★★ **셀 개수가 어디에도 없다.** `n =` · `N =` · `three cells` · `average of` · `error bar` · `standard deviation` · `replicate` **전부 0 회** (본문+SI). 0.6 Ah 프로토타입 · 20 mAh 소형 파우치 · 5 Ah 적층셀 각각 몇 개를 만들어 몇 개를 돌렸는지 **한 줄도 없다.** Fig. 6g 의 1000 사이클이 **한 셀인지 대표 한 셀인지**조차 안 적혀 있다 | **파우치 스케일업 논문인데 이 계보 최초의 통계가 되지 못했다.** 사용자가 기대했던 "셀 수가 클 수 있다" 는 **충족되지 않았다** |
| **G2** | **Table S2 의 `±` 가 무엇인지 정의가 없다** — 표준편차인가 범위인가, 시료 몇 개인가, **한 셀 안 여러 지점**인가 **셀 간**인가 | 계보에서 **두 번째** 산포 수치(첫째는 5호 Table S2)인데 정의가 없어 전파에 못 쓴다 |
| **G3** | ★★★ **CE 의 계산 방법과 분해능이 없다.** 적분 방식·전류원 정확도·CV 구간 포함 여부 | **§12 D2 의 본체.** 99.8 % 와 99.99 % 를 가르지 못하면 이 셀의 `LLI` 추정 자체가 성립하지 않는다 |
| **G4** | **사이클 중 CV 유무.** Methods 는 **형성 사이클에만** CV(4.25 V, 0.05 C 컷)를 붙인다. Fig. 6g 캡션은 `CC mode` 라고만 적는다 | CV 를 넣으면 `Q_ch` 가 달라지고 **CE 의 정의가 달라진다** |
| **G5** | ★★ **"4 MPa 를 넘으면 단락 확률이 오른다" 의 근거 데이터가 없다.** Fig. S11 의 압력 점은 **2 · 3 · 4 MPa 세 개뿐**이다 | **운전 압력 창의 위 벽이 주장만 있고 측정이 없다** (§12 D3) |
| **G6** | ★★ **양극 쪽 사후 분석이 하나도 없다.** 1000 사이클 후 NMC 의 rock-salt·입자 균열·접촉 손실에 대한 관측 **0**. `degradation` 이라는 단어도 본문에 **0 회** | **용량 손실 11 %p 의 전극 귀속이 불가능하다.** 닻 카드의 질문(양극 `LAM_PE` vs 접촉 손실)에는 **입력을 주지 않는다** |
| **G7** | **Ag–C 층이 Table S3 의 두께 예산에 없다** (양극·SSE·도금 Li·집전체·필름만 있다) | 에너지밀도 계산의 분모가 빠져 있다 (§12 D7) |
| **G8** | **Ag 이동의 기구.** `[인쇄]` "the specific mechanism of Ag transport needs to be further investigated" | 논문이 스스로 인정한 공백. Ag 가 **매 사이클 집전체 쪽으로만** 간다면 유한 수명 변수다 |
| **G9** | **Fig. S4c 반쪽전지의 면적·활물질 질량이 없다** (축이 절대 mAh) | Ag–C 층의 **면적 용량**을 셀과 비교할 수 없다 |
| **G10** | ★★ **"isolated lithium" 의 양.** `[인쇄]` 맨-SUS 셀에서 "the discharge capacity decays due to the **generation of isolated lithium**" 이라고 **기구로 지목**하고 **한 번도 재지 않는다** | Q7 의 핵심. 지목은 있고 측정이 없다 |
| **G11** | **EELS Li 신호의 정량.** 방전 후·100 사이클 후에도 남는 Li 망의 **양**이 없다 | 이 논문이 가진 **유일한 Li 특이 채널**인데 정성이다 |
| **G12** | **압력 지그가 정압인가 정변위인가.** 충전 때 도금 Li 25–30 µm 가 생기면 셀이 두꺼워진다. 강성 지그면 압력이 오르고, 스프링이면 유지된다 | 5호가 압력을 **로드셀로 실계측**했던 것과 대비된다. `2 MPa` 가 **충전 말단에도 2 MPa** 인지 알 수 없다 |
| **G13** | **왜 60 °C 인가.** 모든 사이클·율·형성 시험이 **60 °C** 다. 25 °C 자료는 방전 1 점(90.7 %)뿐 | 창고·EV 운전 온도와 다르다. **수명 1000 사이클은 60 °C 의 값**이다 |

---

# 2. 서지·소속·자금

- *Nature Energy* **5**, 299–308 (April 2020). doi `10.1038/s41560-020-0575-z`.
- Received 2019-07-25 / Accepted 2020-02-07 / Published online 2020-03-09.
- 저자 16 명. SAIT(수원) + Samsung R&D Institute Japan(오사카).
- `[인쇄]` Data availability: "All the data generated or analysed during this study are
  included in this published article and its Supplementary Information files. The data
  that support the plots within this paper are **available from the corresponding
  authors upon reasonable request.**" → **원자료 공개 없음.** 코드 없음(실험 논문).
- 특허가 인용에 들어 있다: ref 49 `US20190157723A1` (Suzuki, Yashiro, Aihara —
  *All-solid-state secondary battery and method of charging the same*), ref 50 ECS 초록.
  `[해석]` **이 개념의 원전은 특허와 학회 초록이고 이 논문은 그 공개판이다.**

---

# 3. 이 논문이 묻는 것과 답하는 것

**묻는 것**: Li 금속 박을 **쓰지 않고**(무음극) 황화물 ASSB 를 **고에너지 + 장수명**으로
돌릴 수 있는가.

**답**: `[인쇄]` 초록 — Ag–C 복합 음극이 `[인쇄]` "can effectively regulate Li
deposition, which leads to a genuinely long electrochemical cyclability."
0.6 Ah 파우치셀에서 `[인쇄]` **>900 Wh l⁻¹ · CE >99.8 % · 1000 사이클**.

**논증 구조 (5 단)**:
1. **맨 SUS 집전체**에 바로 도금하면 Li 가 **불균일·다공**으로 자라고 셀이 **수십
   사이클에 죽는다** (Fig. 2).
2. **Ag–C 층**을 끼우면 Li 가 **집전체와 Ag–C 층 사이에 치밀한 층(25 µm)** 으로 쌓이고
   방전 때 **완전히 사라진다** (Fig. 3).
3. 기구: Ag 가 먼저 **Li 와 합금(Li₉Ag₄)** 을 만들고, 그중 상당량이 **집전체 쪽으로
   이동해** Li 도금의 **핵생성 자리**가 된다 (Fig. 4·5).
4. 제작에 **온간 등방압(WIP) 490 MPa** 를 써서 계면 접촉을 만든다 (Fig. 6c, Fig. S10).
5. 0.6 Ah 파우치에서 성능을 보인다 (Fig. 6).

`[해석]` **논증의 약한 고리는 3 번이다.** Ag 가 핵생성을 돕는다는 것은 **형태 관찰과
"speculated / assume / presumed / believed" 로 서술**되고, 대조 실험은 SI 의
**C 단독 · Ag 단독** 두 개뿐이다 (Fig. S6). 정량적 인과는 없다.
`[인쇄]` 본문 그대로: "It is **speculated** that the application of Ag improves the
conductivity and lowers the nucleation energy of Li metal" / "We **assume** that Ag
forms an Ag–Li alloy first" / "it is **presumed** that the C acts as an ion conductor" /
"It is **believed** that Ag dissolved in Li metal is more energetically favoured".

---

# 4. 셀과 재료 — Methods 전부

## 4.1 양극
- 활물질: **LiNi₀.₉₀Co₀.₀₅Mn₀.₀₅O₂** (본문 표기 `NMC`; Ni 90 %).
- 코팅: **Li₂O–ZrO₂ (LZO) 5 nm**, 졸–겔. 용액 = 무수 2-프로판올 : 리튬 메톡사이드
  (메탄올 중 10 %) : 지르코늄(IV) 테트라프로폭사이드 = **200:20:1 몰비**. 1 h 교반 →
  50 °C 진공 증발(초음파) → 여과 → **공기 중 300 °C 1 h**. 선행 연구 ref 40 (Ito 2014).
- 복합양극: LZO-NMC : SSE(<1 µm, Mitsui) : 탄소나노섬유 : PTFE 바인더 =
  **85 : 15 : 3 : 1.5 (무게)**, 무수 자일렌. **건식 필름 공정**(ref 40,48,49).
- 두께 ≈**100 µm**, 로딩 **6.8 mAh cm⁻²**, `[인쇄]` 비용량 **215 mAh g⁻¹ @0.2C**.
- Table S3: `AM capacity 215 mAh g⁻¹`, `AM ratio 86 %`, `Thickness 95–105 µm (×2)`,
  `Areal capacity 6.4–6.8 mAh cm⁻²`.
- `[인쇄]` SSE 입자를 서브마이크론으로 쓴 이유: "to increase the contact area and the
  cathode density" — **접촉 면적을 공정으로 올린다**는 말이 여기 한 번 나온다. 그리고
  `[인쇄]` "Although there could be more side reactions with smaller SSE particles,
  the negative influence was **not significant under our experimental conditions**"
  ⚠ **근거 자료 없음.**

## 4.2 고체전해질
- **Li₆PS₅Cl (argyrodite)** 99 wt%, 3 µm, Mitsui Mining & Smelting + **비수계 아크릴레이트
  바인더 1 wt%**. 용매 = 자일렌 : 무수 isobutyl isobutyrate **50:50 w/w**,
  4 Å 분자체 + ZrO₂ 비드(3 mm), Thinky AR-100, **2000 rpm 6 min**.
- 이형 PET(75 µm) 위 닥터블레이드 → 50 °C 핫플레이트 → 40 °C 진공 하룻밤.
- 두께 **≈40 µm → 셀 압착 후 30 µm**.
- 전도도 `[인쇄]`: 결정질 argyrodite **1.8 mS cm⁻¹** (상온), 바인더 혼합 후 **1.31**,
  활성화에너지 **0.35 eV**. 비정질 Li₂S:P₂S₅ = 80:20 **0.76**, 75:25 **0.19** mS cm⁻¹.
- XRD: cubic *F*-43*m*, 15/17/25/30/31° = (111)(200)(220)(311)(222).
  Raman: **≈420 cm⁻¹** = PS₄³⁻ 정사티오인산. 시트 ↔ 분말 스펙트럼 거의 동일(Fig. S3).
- ⚠ **모든 공정이 드라이룸(이슬점 < −50 °C)**, 단 `[인쇄]` "Only the isostatic press was
  performed under **ambient atmosphere due to facility limitations**."
  `[해석]` **황화물 셀을 대기 중에서 490 MPa 로 눌렀다.** 논문은 그 영향을 검토하지 않는다.

## 4.3 음극 (이 논문의 본체)
- **Ag 나노입자 D50 = 60 nm** : **카본블랙 D50 = 35 nm** = **1 : 3 (무게)**.
- 바인더 **PVDF 7 wt%** (Kureha), 용매 NMP, Thinky AR-100.
- **스크린 프린터**로 **10 µm SUS 박**에 코팅 → 공기 중 80 °C 20 min → 진공 100 °C 12 h.
- 두께 **5–10 µm**. `[인쇄]` **Ag 가 복합체의 ≈8 vol%**, **Ag 사용량 8–16 mg Ah⁻¹**.
- 집전체가 **Cu 가 아니라 SUS** 인 이유: Fig. S4a `[도표]` Cu 의 CV 는 **1e-1 A** 스케일로
  터지고(사진에 Cu 가 갈변) SUS 는 **1e-4 A** 스케일에서 평평하다.
  `[인쇄]` "Cu reacts with the sulfide … cannot be used in sulfide based ASSBs."
- `[인쇄]` **"Unlike the ASSBs with a graphite anode, the solid electrolyte is not
  included inside the anode in our system."** → **음극 안에 이온 경로가 없다.**
  `[인쇄]` 그래서 "the C acts as an ion conductor in the nanocomposite layer" (추정).
- Table S1 면저항 (`[인쇄]`, CMI-SR1000N):

  | | SUS 집전체 | Ag:C = 1:3 | Ag 층 | C 층 |
  |---|---:|---:|---:|---:|
  | 두께 (µm) | 10 | 17 | 3 | 20 |
  | 면저항 (µΩ cm) | 52 | **222** | 15 | **5730** |

  `[인쇄]` 각주: "The resistivity of carbon (100 %) for electronic conduction is several
  orders lower than the resistivity of typical solid ion conductors for ionic
  conduction (>1000 Ω cm)."
  `[해석]` **즉 이 층은 전자는 잘 통하고 이온은 못 통한다.** 그런데도 Li 가 층의
  **반대편**(집전체 쪽)에 쌓인다 — SI Note 1 이 이것을 `[인쇄]` "we suspect that the
  **charge transfer kinetics** might be the dominant factor" 로 설명하고 만다.
  ⚠ **수송으로 설명하면 반대 위치에 쌓여야 한다고 논문 스스로 적는다.** 정량 없음.

## 4.4 파우치셀
- **67 mm × 112 mm bi-cell, 0.6 Ah.** 양면 도포 NMC 양극 하나를 음극 둘이 감싼다.
- 치수: 음극 **55 × 90 mm**, 양극 **53 × 88 mm**, SSE **57 × 92 mm**.
  `[재현]` 양극 면적 46.6 cm² × 2 면 = **93.3 cm²** × 6.8 mAh cm⁻² = **634 mAh** ✓
- 적층 후 라미네이트 백 진공 밀봉 → **WIP 490 MPa (Kobelco Sr. CIP)** → 백에서 꺼내
  Al(양극)·Ni(음극) 탭 초음파 용접(Branson 2000X) → 재포장·진공 밀봉.
- 운전: `[인쇄]` 본문 "we also applied a **uniform pressure of 2–4 MPa** to the pouch cell
  using a lab-made pressure jig during the cell operation" / Fig. 6c 캡션 "an external
  pressure of **2 MPa**" / SI Note 2 "a relatively low pressure of **2 MPa** was adopted".
  (§12 D4)

## 4.5 프로토콜
- 1.0 C ≡ **6.8 mA cm⁻²**. 0.05 C = 0.34 / 0.1 C = 0.68 / 0.2 C = 1.36 / 0.33 C = 2.24 /
  0.5 C = 3.4 / 2.0 C = 13.6 mA cm⁻².
- **형성**: 0.1 C 충전 → 0.2 C 방전, 2.5–4.25 V, 4.25 V 에서 **0.05 C 까지 CV**,
  2.5 V 와 4.25 V 에서 **각 10 min 유지**.
- **사이클**: **CC 0.5 C / 0.5 C**, 2.5–4.25 V vs Li⁺/Li, **60 °C**.
- **율특성**: 충전 0.1 C CC–CV 고정, 방전 0.2 → 2.0 C, 60 °C.
- **온도**: 충전 온도 60 °C 고정, 방전 온도만 60 → −10 °C.
- 장비: TOSCAT-3100 (TOYO). EIS: AutoLab, **1 MHz–0.01 Hz, 진폭 10 mV**.
- SSE 전도도용 펠릿: 13 mm 다이, **일축 300 MPa**, 양면 박(50 µm) + **30 MPa** 접촉,
  PTFE 바디 + SUS 핀 + 작은 스프링, Al 라미네이트 봉지, 80 °C 12 h 예열,
  **80 → −20 °C** 임피던스.
- X-ray CT: Zeiss Xradia 520 Versa, **공간분해능 820 nm**, 80 kV / 7 W, ×4 대물 +
  2×2 비닝, **3200 투영 × 25 s**.
- SEM: Hitachi SU-8030 + Oxford X-max 80 EDS. TEM: FIB(Helios 450F1, 최종 박막화 5 kV) +
  **이중 Cs 보정 Titan cubed 300 kV** + Gatan Quantum 966 에너지 필터,
  **진공 이송 홀더(Gatan 648)** 로 대기 노출 차단.

---

# 5. 본문 절별 해체

## 5.1 서론 (1 쪽)
- 황화물 SSE 를 고른 이유: `[인쇄]` 상온 이온전도도 **1–25 mS cm⁻¹**, `t_Li⁺ ≈ 1`
  (액체 ≈0.5), **연질**이라 소결 없이 압착으로 만든다.
- 단점도 적는다: H₂S, 그리고 `[인쇄]` "most sulfide electrolytes tend to decompose
  rapidly in contact with lithium metal" — **argyrodite 만 상대적으로 느리다.**
- 무음극 개념(refs 22–25, Dahn 그룹 포함)을 인용하며 `[인쇄]` "solutions for the low Li
  Coulombic efficiency and extensive dendrite growth are **yet to be reported**."
- Ag 를 고른 근거: `[인쇄]` "As Ag is **soluble in Li** and **reduces the nucleation
  energy** for the formation of Li (refs 26–32), it assists the uniform deposition."
- C 의 역할: `[인쇄]` "in this work it plays the role of **a separator to keep the SSE
  layer away from Li metal**." → **C 는 물리적 차단막이다.**

## 5.2 Construction of the ASSB (2–3 쪽) — Fig. 1
셀 구성·전해질 물성. 우리 축에 걸리는 문장 둘:
- `[인쇄]` "the interfacial side reactions between the cathode active material and the
  SSE **at high voltages above 4.0 V** and the **high solid–solid interfacial
  resistance**, which deteriorate ASSBs' capacity and cycle life, are known critical
  issues" → **양극 열화 두 기구를 알고 있다고 적고, 그 뒤로 한 번도 측정하지 않는다** (G6).
- `[인쇄]` "the thickness of the Ag–C nanocomposite layer is **only 5–10 μm**" — 얇음이
  체적 에너지밀도의 근거다.

## 5.3 Fig. 2 — 대조군: 맨 SUS 집전체
- `[인쇄]` 0.05 C (0.34 mA cm⁻²), **SOC 50 %** 에서 이미 Li 도금이
  "**not dense**, it was **thick and random in shape**", 두께 **t = 30 µm**.
- `[도표]` Fig. 2b 상면도: "Deposition site" 와 "**No deposition site**" 가 한 시야 안에
  공존한다 — **면내 불균일**이 육안 수준이다. 인셋 사진에 금색 도금 Li.
- `[도표]` Fig. 2c 단면: Li 층이 **주상(columnar)·균열투성이**이고 SSE 도 갈라져 있다.
- `[인쇄]` "the discharge capacity decays due to the generation of **isolated lithium**."
  ★ **이 논문에서 dead Li 가 이름으로 등장하는 유일한 문장이다. 측정은 없다** (G10).
- `[도표]` **Fig. 2d — 붕괴의 모양이 계단(시그모이드)이다.** 20 mAh 파우치, 0.1 C/0.33 C,
  60 °C: 사이클 10 까지 ≈100 % → 15 에 ≈80 % → **20 에 ≈50 %** → 27 에 ≈20 % →
  50 에 **≈6 %**. 중간 20 사이클에 거의 전부가 일어난다.
  ★ `[해석]` **4호(Shi 2020)의 Fig. 1(a)·S1(a) 와 같은 모양이다** — 부드러운 감쇠가
  아니라 **급락**. 닻 카드의 "`θ(N)` 을 부드러운 함수로 매개화하면 안 된다" 에
  **두 번째 독립 표본**이 붙는다. ⚠ 단 여기서는 양극이 아니라 **음극**이 원인으로
  지목된다 — 즉 **급락의 모양 자체는 전극을 특정하지 않는다.**

## 5.4 Fig. 3 — Ag–C 가 있을 때의 도금/탈리
- 충전 0.1 C (0.68 mA cm⁻²) 후: `[인쇄]` "**dense and uniform** Li deposits
  (**t = 25 μm**)" 가 **집전체와 Ag–C 층 사이에** 생긴다.
- `[도표]` Fig. 3c 의 Ag EDS 맵: Ag 신호가 **도금 Li 층 전체에 퍼져 있다**
  (Ag–C 층이 아니라). C 맵은 Ag–C 층에만 남는다. → 본문의 "Ag 가 Li 로 이동" 을 지지.
- 방전 후 (Fig. 3d): `[인쇄]` "the Li metal layer **completely disappears**" 이고
  `[도표]` Ag 신호는 **Ag–C 층의 맨 아래(집전체 쪽) 가장자리에 밝은 띠**로 모인다 +
  층 전체에 성긴 점. `[인쇄]` "the Ag dissolved in the Li layer **does not return** to
  the Ag–C nanocomposite layer and remains **between the current collector and the
  Ag–C** layer."
- 1 사이클 vs 100 사이클 (Fig. 3e,f): `[도표]` 1 사이클은 Top/Middle/Bottom 이 비슷하고,
  100 사이클은 **Bottom 에 밝은 Ag 가 몰려 있고 입자가 작아졌다**.
  `[인쇄]` "Ag … **continuously moves in the direction of the current collector in each
  cycle, and does not return to its original position**."
  ★ `[해석]` **Ag 는 소모성 상태변수다.** 층 안 분포가 매 사이클 비가역으로 바뀐다 →
  **"동일한 음극" 이라는 가정이 사이클 축에서 깨진다.**
- ⚠ `[인쇄]` **캡션 마지막 줄**: "Cracks or empty spaces **below the Ag–C nanocomposite
  layer** were formed **during the sample preparation**."
  ★★ `[해석]` **dead Li 가 있다면 바로 그 자리(Ag–C 층 아래 = 집전체 계면)에 있다.**
  논문은 그 자리의 빈 공간을 **선험적으로 시료 준비 탓으로 돌린다.**
  그 귀속을 뒷받침하는 대조(예: 같은 공정으로 자른 pristine 시료 비교)는 없다.
- `[인쇄]` "**no residual Li deposits or Li dendrite features were found** in the Ag–C
  nanocomposite layer after these cycles (Supplementary Fig. 5)." (§12 D6)

## 5.5 Fig. 4 — ★★ 컷오프 전압을 축으로 쓴 음극 해부
이 그림이 **이 논문이 우리에게 주는 가장 직접적인 전압축 자료**다.
0.1 C 충전을 다섯 개의 컷오프에서 멈추고 각각 단면 SEM 을 찍는다.

| 컷오프 전압 | `[인쇄]` 면적용량 | `[재현]` 6.75 대비 | `[도표]` 비용량 | Ag–C 층 상태 (`[인쇄]`) | `[인쇄]` 도금 Li 두께 |
|---:|---:|---:|---:|---|---:|
| (pristine) | 0 | 0 % | 0 | Ag 입자 ~60 nm 균일 분산 | 0 |
| **3.5 V** | **0.5 mAh cm⁻²** | 7.4 % | ≈15 mAh g⁻¹ | 형상 변화 없음, **공극률만 뚜렷이 감소** | — |
| **3.55 V** | **0.64** | 9.5 % | ≈20 | **Ag NP 크기 증가** (Ag 리튬화 계속) | — |
| **3.6 V** | **1.12** | 16.6 % | ≈35 | **Ag/Ag–Li NP 가 급격히 수축** — Li 도금 시작 | **6 µm** |
| **4.0 V** | **5.0** | 74 % | ≈160 | 정상상태, 추가 변화 없음 | **20 µm** |
| **4.25 V** | **6.75** | 100 % | ≈215 | 정상상태 | **25 µm** |

- `[인쇄]` "The voltage **rapidly rose to ~3.55 V** and the slope was subsequently
  observed to **decline drastically**."
- `[인쇄]` 3.5 V 까지의 기울기 구간은 "primarily associated with the **C lithiation**"
  (Fig. S6·S7 근거), "the lithiation of **Ag also appears to initiate** in this region."
- ★★★ `[해석]` **이것이 "무음극은 OCP 가 평탄하다" 를 깨는 자리다.**
  충전 초기 **0.64–1.12 mAh cm⁻² (= 전체의 9.5–16.6 %)** 동안 셀 전압이
  **2.5 → 3.6 V 로 1.1 V 를 훑고**, 그 구간의 전압 변화는 **양극이 아니라 음극**에서
  온다 (Ag–C 의 리튬화는 Li⁺/Li 대비 0–1 V 에서 일어난다 — Fig. S4c).
  → **완전지 OCV 를 "양극 곡선 하나가 밀린 것" 으로 읽는 우리 계획은
  이 셀의 앞 10–17 % 구간에서 성립하지 않는다.** 닻 카드의 전제에 조건이 붙는다.
- `[재현]` **Li 두께–전하량 수지가 닫히지 않는다.** 치밀 Li 1 µm = 0.534×10⁻⁴ g cm⁻² ×
  3860 mAh g⁻¹ = **0.206 mAh cm⁻²**. 세 점에 적용하면

  | 전압 | 통과 전하 | 두께로 환산한 Li | 비 |
  |---:|---:|---:|---:|
  | 3.6 V | 1.12 | 6 µm → **1.24** | **110 %** |
  | 4.0 V | 5.0 | 20 µm → **4.12** | **82 %** |
  | 4.25 V | 6.75 | 25 µm → **5.15** | **76 %** |

  비가 **단조가 아니다**(110 → 82 → 76 %). 만약 Ag–C 층이 1.12 mAh cm⁻² 를 저장한다면
  3.6 V 에서 도금 Li 는 **0 이어야** 하는데 6 µm 가 보인다.
  ★ `[해석]` **두께는 Li 인벤토리 계기로 쓸 수 있는 정밀도가 아니다 (±25 % 수준).**
  이것은 우리가 §10 Q7 에서 쓰는 검출 한계 논증의 근거다. **논문은 이 수지를
  한 번도 맞춰 보지 않는다** (§12 D10).

## 5.6 Fig. 5 — TEM / EELS / SADP / XRD
- **pristine**: Ag ~60 nm, 서로 떨어져 있고 `[인쇄]` "**no network formation**".
  SADP: Ag **결정질**, C **비정질**.
- **충전 후(0.1 C)**: Ag NP 가 `[인쇄]` "**fragmented into smaller ones**".
  SADP 가 **비정질 링**으로 바뀐다 → Ag–Li 합금. 단 `[인쇄]` 일부 파편은 결정성을
  유지 (Fig. S9).
- ★★ **EELS Li 맵 (Fig. 5c/f/i/l)** — 이 계보에서 **처음 등장하는 Li 특이 채널**이다.
  `[인쇄]` "the presence of Li **in the Ag NPs is not clearly identified**, but it was
  found **on the C particles** and was observed to **not fill the pores** between the
  particles."
  `[도표]` 내가 본 것: **pristine (5c) 에는 빨강(Li) 이 없고**, 충전 후(5f)·**방전
  후(5i)·100 사이클 후(5l) 에는 모두 빨강 망(network)이 남아 있다.**
  ★★★ `[해석]` **방전 후에도 Ag–C 층 안에 Li 가 남아 있다는 것이 이 그림에 보인다.**
  이것이 dead Li 인지, LiC_x 인지, SEI 인지, 합금 잔여인지는 **EELS 로 갈리지 않는다**
  (Li K-edge 의 화학 이동을 논문이 쓰지 않는다). 그리고 **정량이 없다** (G11).
  ⚠ 본문은 이 관측을 `[인쇄]` "the compositional variation was **not significant**"
  한 마디로 넘기고, 다른 곳에서는 `[인쇄]` "**no residual Li deposits** … were found"
  라고 적는다 (§12 D6).
- **100 사이클 후**: `[인쇄]` Ag NP 가 "**smaller and sparse**". 단 `[인쇄]` "Ag NPs that
  were expected to retain their particle size **through recrystallization** were also
  observed simultaneously." → **한 시야 안에 두 개체군이 있다.** 분율 없음.
- ★★ **Fig. 5n — XRD (Cu Kα), Ag–C\|SSE\|NMC 파우치셀**:

  | 상태 | `[인쇄]` 피크 | 귀속 |
  |---|---|---|
  | pristine | **38.2°, 44.3°** | Ag (111), (200) |
  | 충전 후 (0.1 C) | **23, 27, 28.3°** 신규; 기존 Ag 피크 이동/소멸 | **Li₉Ag₄ (γ₃)** (refs 29,30) — `[도표]` 라벨 (211)(220)(310) |
  | 방전 후 | **38.4°, 44.6°** 재출현, 합금 피크 소멸 | Ag 재결정 |
  | 전 구간 | 25.6 / 30.2 / 31.6 / 40 / 45.2 / 48.2 / 52.7° | argyrodite (220)(311)(222)(331)(422)(511)(440) |

  `[도표]` pristine 패턴에 **`(Unknown)` 이라고 라벨된 피크가 두 개** 있다 (≈35.5°, ≈37.3°).
  논문은 이것을 논하지 않는다.
  ★★★ `[해석]` **이것이 "Li 저장소를 상(相)으로 동정한" 첫 사례다.** 5호(Doux)는
  SEI 상(Li₂S·LiCl·P₄·Li₃P₇)을 잡았지만 **Li 금속은 XRD 로 원리적으로 안 보인다**고
  적었다. 6호는 **Li 를 품은 금속간 화합물(Li₉Ag₄)** 을 잡는다 — Li 자체가 아니라
  **Li 를 담은 그릇**을 본다. 그리고 그 그릇이 **가역적**임을 보인다(방전 후 소멸).
  ⚠ 상 분율은 **정량되지 않는다** (Rietveld 없음, 내부 표준 없음).
- ⚠ Fig. 5n 안의 모식도가 충전 상태를 **"Ag–C alloy"** 라고 적는다. 본문·캡션은
  Ag–Li 합금이다. 오식 (§12 D9).
- `[인쇄]` 결론 문단: "Although there is **not clear evidence that confirms the
  involvement of C in the electrochemical reactions**, it is obvious that the C
  particles conduct Li ions and also mechanically support the Ag–C layer owing to
  their strong modulus of **~200 GPa** (ref 45)."
  ⚠ `[해석]` **자기모순에 가깝다** — 같은 논문 Fig. 4 가 `[인쇄]` 3.5 V 까지의
  기울기를 "primarily associated with the **C lithiation**" 이라고 적었다.
  C 가 리튬화한다면 그것은 전기화학 반응이다. (§12 D5-b)

## 5.7 Pouch cell performance (5–6 쪽) — Fig. 6
- **bi-cell 구조**: 양면 NMC 양극 하나를 음극 둘이 감싼다. Fig. 6b 의 X-선 CT 로
  `[인쇄]` 양극 120 µm, "SSE and Ag–C nanocomposite layers (**30 μm combined**)".
  ⚠ Methods 는 SSE 만 30 µm 이고 Ag–C 가 5–10 µm 다 (§12 D8).
  `[인쇄]` "**the Ag–C and SSE layers are not distinguishable in the X-ray CT image**."
  → **820 nm 분해능으로도 음극층을 분해하지 못한다.** CT 는 접촉 확인용이다.
- **압력** (Fig. 6c): `[인쇄]` "external pressurization is **essential** for a uniform
  interface formation and stable lithium deposition" / "pressurization is
  **unavoidable for high-current operations**". → **WIP 490 MPa (제작) + 지그 2 MPa (운전)**.
- **율특성** (Fig. 6d,e): 충전 0.1 C CC–CV 고정, 방전 0.2 → 2.0 C, 60 °C.
  `[인쇄]` **Q₁.₀C/Q₀.₂C = 93 %**, `[인쇄]` 0.2 C 비용량 **215 mAh g⁻¹**,
  `[인쇄]` 2.0 C 에서 **이용률 >80 %**.
  `[도표]` Fig. 6e 인셋(이용률 vs 면적전류): 1.36 → ≈100 %, 2.24 → ≈97, 3.4 → ≈95,
  6.8 → ≈93, 13.6 mA cm⁻² → **≈85 %**.
  `[도표]` Fig. 6d: 충전(0.1 C CC–CV) 곡선이 **≈690 mAh**, 0.2 C 방전이 **≈630 mAh**
  → `[재현]` **초기 비가역 ≈8.7 %**.
- **온도** (Fig. 6f): 충전은 항상 60 °C, 방전 온도만 바꾼다.
  `[인쇄]` 45 °C **99.5 %**, 25 °C **90.7 %**, −10 °C **>40 %**.
  `[도표]` 인셋: −10 ≈48, 0 ≈72, 10 ≈82, 25 ≈90, 45 ≈99.5, 60 = 100 %.
  SI Fig. 15 캡션 `[인쇄]`: **계면 저항 25 °C 50 Ω cm² ↔ 60 °C 5 Ω cm² (10 배)**.
  ★ `[해석]` **이 셀의 "용량" 은 온도에 대해 `η(T)` 로 지워졌다 돌아온다** — 재료
  손실이 아니다. 3 항 분해의 `η` 가 **온도 축에서도 열린다**는 실측 한 점.
- ★★★ **사이클 (Fig. 6g)** — CC 0.5 C/0.5 C, 2.5–4.25 V, 60 °C, 0.6 Ah 파우치.
  `[인쇄]` 평균 셀 전압 **3.76 V**, 방전 용량 **146 mAh g⁻¹** (= 0.2 C 의 210 대비 **70 %**),
  `[인쇄]` **600 사이클 95 % · 1000 사이클 89 %**, `[인쇄]` **CE >99.8 %**.

  내 축 교정 판독 (`[도표]`, 방법은 §0):

  | 사이클 구간 | CE 중앙값 | CE 최저 |
  |---|---:|---:|
  | 0–200 | **99.89 %** | 99.80 |
  | 200–400 | 99.90 | 99.78 |
  | 400–600 | 99.88 | 99.13 |
  | 600–800 | 99.90 | 99.62 |
  | **800–900** | **99.80** | **97.86** |
  | **900–1000** | **99.21** | **97.42** |

  용량유지율(같은 교정): 200 → 98.3 %, 400 → 96.8, 600 → **94.9**, 800 → 92.3,
  1000 → **89.4** (인쇄값 95·89 와 일치 ✓ — 교정 검증).
  ★★ **마지막 ≈150 사이클에서 CE 가 초록의 ">99.8 %" 아래로 내려간다.**
  본문·초록·캡션 어디에도 언급이 없다 (§12 D1).
- **적층**: `[인쇄]` bi-cell(스택 1) 기준 **700 Wh l⁻¹** (라미네이트 120 µm 포함),
  `[인쇄]` ">1,000 Wh l⁻¹ 도 설계 가능". **5 Ah 급**: bi-cell **10 병렬 적층**,
  **0.05 C/0.05 C**, `[인쇄]` "**without external pressure**",
  `[인쇄]` **5,870 mAh · 942 Wh l⁻¹**.
  ★ `[해석]` **초록의 ">900 Wh l⁻¹" 는 0.6 Ah 셀이 아니라 5 Ah 적층셀의 값이고,
  그 셀은 0.05 C 에서 무압으로 돌렸다.** 1000 사이클을 돈 셀(0.6 Ah, 2 MPa)의
  에너지밀도는 **703 Wh l⁻¹** 다. **두 주장이 같은 셀의 것이 아니다.**
- **안전**: 상용 LIB 1.4 Ah vs ASSB 프로토 1.2 Ah, 4.25 V 충전 후 상온→210 °C @5 °C/min.
  `[인쇄]` LIB 는 100 °C 부근 팽윤, 210 °C 도달 **3 min 후 열폭주**. ASSB 는 열폭주
  없음, 210 °C **1 h 유지에도 전압 불변**. 150 °C 오일 배스 5 min 무팽윤.
  절단 시험: LED 가 절단 중 **일시 단락**으로 약해졌다가 절단 완료 후 복귀.

## 5.8 Conclusions (8 쪽)
`[인쇄]` "The formation of a **dense Li metal layer**, which could be **moved repeatedly**
between the Ag–C nanocomposite layer and the SUS current collector was demonstrated.
Ag NPs were alloyed with Li in the early stage of the charging process, but a
**significant fraction of Ag was found to move to the current collector side** and
assist the uniform and dendrite-free plating of Li metal."
⚠ `[해석]` 결론에 **CE·수명의 기구적 설명이 없다.** "dendrite-free" 는 **형태 관찰의
언어**이고, 1000 사이클에 11 %p 가 어디로 갔는지는 결론에 없다.

---

# 6. SI 해체

## 6.1 Fig. S1 / S2 / S3 — SSE 필름 (안 봄, 텍스트만)
`[인쇄]` WIP 후 밀도 증가로 필름 기계적 강도 향상(S1). 자일렌+IBIB 혼합 용매로
**핀홀 없는** 분산(S2). 시트 ↔ 분말 Raman 거의 동일(S3).

## 6.2 Fig. S4 — ★ Cu/SUS CV + **Ag–C 반쪽전지**
- `[도표]` (a) Cu: 전류가 **1e-1 A** 스케일로 터진다 (2 V 부근에서 수직 상승), 인셋
  사진의 Cu 는 **갈색으로 변색**. (b) SUS: 같은 창에서 **1e-4 A** 스케일, ±1.5e-5 A
  수준으로 평평하고 5 사이클이 겹친다.
  `[재현]` **전류 규모가 ≈10³–10⁴ 배 다르다.**
- ★★ `[도표]` **(c) Ag–C \| Li 반쪽전지**: 전류를 걸자마자 전압이 **1.0 V 아래로 급락**,
  0.8 → 0.05 V 로 완만히 내려가며 **≈2.2 mAh** 리튬화. 탈리튬화는 0.05 → 0.3 V 부근
  완만 → 2.0 V 까지 상승, **≈2.0 mAh** 회수.
  `[재현]` **초기 비가역 ≈0.2 mAh / 2.2 mAh ≈ 9 %.** (⚠ 면적·질량 미상 → 셀 대비
  환산 불가, G9.)
  ★★★ `[해석]` **Ag–C 층의 작동 전위창이 0–1 V vs Li⁺/Li 이고 그 안에서 기울기를
  갖는다.** 즉 **이 음극은 평탄하지 않다.** Li 도금(0 V 평탄)은 그 **뒤에** 온다.
  → §5.5 의 결론(앞 10–17 % 에서 완전지 OCV 가 양극 곡선이 아니다)의 **독립 근거**.
- SI 본문의 부수 발견 `[인쇄]`: **Ag₂S 형성이 의심되나** Ag₂S 의 리튬화가 일어나는
  **≈2.0 V 부근에 신호가 없고** 전압이 바로 1.0 V 아래로 떨어지므로 "the formation of
  Ag₂S is **not significant**". (근거: Solid State Ionics **340**, 115015 (2019).)

## 6.3 Fig. S5 — ★ 100 사이클 후 충전/방전 단면
- `[도표]` (a) **0.5 C 충전 상태**: 위에서부터 Ag–C(얇은 띠) / **두껍고 균질한
  "Li deposits"** / SUS. 20 µm 스케일바 기준 Li 층이 **≈30 µm**. 계면에 얇은 밝은 선.
- `[도표]` (b) **0.5 C 방전 상태**: SSE / **Ag–C (≈7–8 µm, 10 µm 스케일바)** / SUS.
  **Li 층이 없다.** Ag–C 층 안의 밝은 점(Ag)이 **아래쪽(SUS 쪽)에 더 밀집**해 있다.
  SSE 에는 균열이 보인다.
- ★★ `[해석]` **이것이 이 논문의 dead Li 측정이다 — 그리고 음성 증거다.**
  `[재현]` **검출 한계**: 치밀 Li 1 µm = 0.206 mAh cm⁻² = **6.8 mAh cm⁻² 의 3.0 %**.
  관측된 열화는 1000 사이클에 **11 %p**, 즉 **사이클당 0.011 %**.
  → **SEM 은 사이클당 손실보다 ≈270 배 거친 계기이고**, 누적으로도 **3 % 미만의
  잔류 Li 는 원리적으로 못 본다.** "보이지 않았다" 는 "없다" 가 아니다.

## 6.4 Supplementary Note 1 + Fig. S6 — C 단독 / Ag 단독
- `[인쇄]` **C 단독**: Li 가 집전체와 C 층 사이에 쌓이되 "**inhomogeneous and porous
  interface**". **Ag 단독**: Li 성장은 더 균일하지만 "**the silver layer disappears
  during the charging process**" → Li 금속이 SE 와 직접 접촉 → SE 분해 위험.
- `[도표]` (a) C 단독 방전 용량: 0.1 C ≈203, 0.33 C ≈197, **1.0 C ≈181 mAh g⁻¹**.
  `[재현]` 1.0C/0.33C = **≈92 %**.
  (c) Ag 단독: 0.1 C ≈190, **0.33 C ≈72**, **1.0 C ≈3 mAh g⁻¹** → `[재현]` **≈4 %**.
  ★ **Ag 단독은 율에서 완전히 무너진다.** Table S1 의 면저항(Ag 층 15 µΩ cm 로 가장 낮다)과
  **반대 방향**이다 → 전자 전도가 원인이 아니다. `[해석]` **이온 경로(C)가 없어서다.**
- `[도표]` (d) Ag 단독 단면 SEM 에 **"Ag–Li or Ag"** 라고 라벨된 큰 밝은 덩어리가
  **도금 Li 층 안에** 떠 있다 — Ag 가 Li 로 들어간다는 Fig. 3c 의 독립 확인.
- `[인쇄]` 위치 역설: 전자 전도가 이온 전도보다 훨씬 빠르므로 "**If the transport
  phenomena govern the position of Li deposition, the deposition is bound to occur at
  the carbon/electrolyte interface** … However, because we observe that Li metal is
  deposited on the opposite side, we suspect that the **charge transfer kinetics**
  might be the dominant factor."
  ★ `[해석]` **논문이 자기 수송 논증으로 자기 관측을 예측하지 못한다고 적는다.**
  정직하지만, 대안(전하이동 속도론)에 대한 측정은 **없다**.

## 6.5 Fig. S7 — ★ Ag–C 유/무 초기 곡선
0.1 C 충전 / 0.2 C 방전, 같은 양극.
- `[도표]` **충전**: 두 곡선 모두 **≈233 mAh g⁻¹** 에서 4.25 V 도달. 차이는
  **첫 20–30 mAh g⁻¹ 에만** 있다 — Ag–C 有(파랑)는 3.55 V 에 도달하기까지 ≈22 mAh g⁻¹ 를
  쓰고, Ag–C 無(검정)는 ≈3 mAh g⁻¹ 만에 3.48 V 에 도달해 평탄해진다.
  그 뒤 두 곡선은 **완전히 겹친다**.
- `[도표]` **방전**: 4.2 → 3.5 V 구간은 겹치고, 종점이 Ag–C 有 **≈214**, 無 **≈217 mAh g⁻¹**.
- `[재현]` **ICE**: 有 214/233 = **91.8 %** (비가역 **19 mAh g⁻¹ = 8.2 %**),
  無 217/233 = **93.1 %** (비가역 **16 mAh g⁻¹ = 6.9 %**).
  → **Ag–C 층이 첫 사이클에 ≈3 mAh g⁻¹ (≈1.3 %p) 의 Li 를 더 먹는다.**
- ★★★ `[해석]` **이것이 이 논문이 실제로 주는 `LLI` 관측이다.**
  (a) **첫 사이클 비가역분 19 mAh g⁻¹**, (b) **사이클당 CE 결손**. 둘 다 **전하 수지**이고,
  그 안에서 SEI-Li / dead-Li / Li₉Ag₄-Li / LiC_x 를 **가르지 않는다.**
  단 **有/無 차분(3 mAh g⁻¹)** 은 **Ag–C 층에 귀속되는 몫의 상한**을 준다 — 이 계보에서
  처음 나온 **전극 귀속 가능한 LLI 조각**이다. ⚠ 셀 1 개씩, 오차 없음.

## 6.6 Supplementary Note 2 + Fig. S10–S12, Table S2 — ★★ 압력
- **WIP 효과** (Fig. S10, **안 봄**): `[인쇄]` SEM 으로 "the improvement in the **contact**
  between the electrode and the electrolyte as well as the **increase in the densities**
  of both the electrode and electrolyte were realised by the WIP pressurisation."
  ⚠ **정량 없음** — 접촉 면적도, 공극률도, `θ` 도 없다.
- ★★ **Table S2 — 두께 (`[인쇄]`, ± 의 정의 없음, n 미상)**

  | | Before WIP | After WIP | +3 d 무압 | +7 d 무압 |
  |---|---:|---:|---:|---:|
  | 셀 두께 (µm) | **644.5 ± 2.9** | **609.0 ± 2.4** | 608.8 ± 2.2 | **609.8 ± 2.6** |

  `[재현]` **치밀화 = −35.5 µm = −5.51 %**. 7 일 무압 방치 후 되돌아온 양 = **+0.8 µm**
  (측정 산포 ±2.4 안). `[인쇄]` "the microstructural relaxation **did not occur**".
  ★★★ `[해석]` **5호(Doux)의 `θ(P)` 이력(경로 의존)에 대한 독립 확인이다.**
  Doux 는 25 MPa 를 찍고 5 MPa 로 내려와도 임피던스가 110 → ≈50 Ω 에 머문다는
  **전기적** 증거를 줬다. 6호는 **490 MPa 를 찍고 압력을 완전히 빼도 두께가
  안 돌아온다**는 **기하학적** 증거를 준다 — 같은 결론, 다른 채널.
  → **압축은 비가역이고, 그래서 제작 압력은 "한 번 치르는 비용" 이다.**
- ★★ **운전 압력 (Fig. S11)** — **2 · 3 · 4 MPa 세 점뿐**.
  `[도표]` (a) 율특성(1.0C/0.33C): **94.0 / 95.1 / 95.5 %** — 단조 증가하지만 폭이
  **1.5 %p** 다.
  `[도표]` (b) 0.5C/0.5C 300 사이클 유지율: 세 곡선이 **거의 완전히 겹친다** (≈94 % @300).
  `[인쇄]` "Over the 2–4 MPa range, the rate capability and cycle performance were
  **not significantly different**. Since it is ultimately advantageous to lower the
  external pressure, a relatively low pressure of **2 MPa** was adopted."
  ★★★ `[인쇄]` **"On the other hand, the probability of short-circuiting increased upon
  application of high pressures exceeding 4 MPa."**
  ⚠⚠ **이 문장을 뒷받침하는 데이터가 논문 어디에도 없다** (§12 D3). 4 MPa 초과 점이
  Fig. S11 두 패널 어디에도 없고, 단락 횟수·셀 수·조건도 없다.
- ★★ **무압 운전 (Fig. S12)**: `[인쇄]` "with the Ag-C nanocomposite layer, operation at
  low c-rate (0.1 C) was **possible even in the absence of external pressure**."
  `[도표]` 0.1C/0.1C 무압: 충전 **≈235**, 방전 **≈217 mAh g⁻¹**, 곡선 모양이
  Fig. S7(2 MPa, 0.1C/0.2C)의 **≈233 / ≈214 와 사실상 같다.**
  ★★★ `[해석]` **저율에서는 운전 압력의 기여가 측정 한계 안이다.**
  5호(Doux)에서 1 → 25 MPa 가 임피던스를 **>15 배** 움직였던 것과 정반대다.
  차이는 **제작 압력**이다 — 490 MPa WIP 가 이미 계면을 만들어 놓았기 때문에
  운전 압력이 **할 일이 남아 있지 않다.** → **제작 압력과 운전 압력은 다른 연산자다.**
  (그리고 5 Ah 적층셀도 `[인쇄]` 무압으로 0.05 C 에서 942 Wh l⁻¹ 를 냈다.)

## 6.7 Supplementary Note 3 + Fig. S13, S14 — 조성 최적화
- 소형 파우치 **2 × 2 cm², 20 mAh**, 60 °C.
- `[인쇄]` **C 단독(Ag = 0)** 또는 Ag <10 wt%: 1.0C/0.33C 비가 **75 %** (Ag 함유 조성은
  **95–96 %**), 0.5C/0.5C 운전 불가, **단락이 쉽게 발생**.
- `[인쇄]` **Ag:C = 1:1**: 단락 가능성 높고 **CE <95 %**. 이유로 ① Ag NP 응집 증가
  ② Ag–Li 합금량 증가에 따른 **큰 체적 변화** ③ `[인쇄]` "an increase in the amount of
  **lithium remaining in Ag NPs (irreversible Li)** after discharge".
  ★★★ **이 논문에서 "비가역 Li" 가 명시적으로 이름 붙는 유일한 자리다.**
  `[인쇄]` 그리고 그것이 **단락의 원인**으로 지목된다. **정량 없음.**
- `[인쇄]` **Ag:C = 1:2**: 개선되지만 여전히 부족. **1:3**: 300 사이클까지 율특성·유지율·
  CE 모두 높게 유지 → 프로토타입에 채택.
- ★★★ `[도표]` **Fig. S13c 의 CE 축이 99.4–100.0 으로 확대돼 있다** (Fig. 6g 는 95–101).
  1:3(분홍)과 1:2(검정)의 CE 기준선이 **≈99.97 %** 이고 간헐적으로 99.8–99.85 로 떨어진다.
  1:1(파랑)은 100.0 → 99.8 → 99.6 → 99.5 → **8 사이클 안에 축 아래로 사라진다.**
  `[도표]` Fig. S13b 유지율: 1:3 은 300 사이클에 **≈92.5 %**, 1:2 는 240 사이클에 ≈89 %,
  1:1 은 37 사이클에서 끝난다(≈96.5 %).
  ★★★ `[재현]` **20 mAh 셀은 CE 와 유지율이 서로 맞는다**: 92.5 % @300 → 사이클당
  **99.974 %**, 도표 판독 CE **99.97 %**. **일치한다.**
  **0.6 Ah 셀은 맞지 않는다** (§12 D2). — 이것이 이 논문이 우리에게 준 가장 값진 대조다.
- ⚠ `[인쇄]` "CE was very low (**<95 %**)" 인데 Fig. S13c 의 축 바닥은 **99.4 %** 다
  (§12 D11).
- `[인쇄]` Fig. S14 캡션: 조성을 바꿔도 **3.6 V 아래 초기 리튬화 용량은 크게 안 변하고,
  Ag 를 늘리면 3.5 V 부근에 작은 평탄역이 생긴다.**
  ★ `[해석]` **Ag 리튬화의 전압 서명이 3.5 V 부근 평탄역**이다 — Fig. 4 의 3.5–3.55 V
  구간(Ag NP 크기 증가)과 일치.

## 6.8 Fig. S15 / S16 / S17 / S18, Table S3
- **S15 (안 봄, 캡션만)**: `[인쇄]` 충전 후 계면 저항 **25 °C 50 Ω cm² ↔ 60 °C 5 Ω cm²**
  (약 10 배).
- ★★★ **S16 — 0.5C/0.5C, 사이클 1/200/400/600/800/1000 의 V–Q.**
  `[도표]` 방전 종점: **146 / 143 / 141 / 138 / 135 / 131 mAh g⁻¹** (인쇄값 146·138.7·130 과
  일치 ✓).
  ★★ **곡선의 모양**: 충전·방전 곡선이 **0 ~ ≈110 mAh g⁻¹ 구간에서 거의 완전히 포개진다.**
  움직이는 것은 **방전 말단의 무릎 하나뿐**이다. 충전 곡선의 종점도 같이 왼쪽으로
  움직인다 (화소 측정: 사이클 1 에서 충전·방전 종점의 x 차 **−3 px**, 사이클 1000 에서
  **+23 px**; `[재현]` 눈금 10.5 px = 1 mAh g⁻¹ → **+2.2 mAh g⁻¹**, 즉 그 사이클의
  CE ≈ 98.3 ± 0.4 % — Fig. 6g 의 900–1000 구간 중앙값 99.21 %·최저 97.42 % 와 **같은
  구간에 있다** ✓).
  ★★★ `[해석]` **이것은 "곡선이 늘어나거나 밀리는" 열화가 아니라 "끝이 잘리는" 열화다.**
  3.2 V 위쪽에서 두 곡선이 겹치므로 **전극 balancing 의 이동(LLI 의 전형적 서명인
  수평 이동)이 곡선 모양에 나타나지 않는다.** 나타나는 것은 **방전 컷오프 도달 시점**뿐.
  → **이 자료에 OCV 적합을 걸면 `LLI` 와 `LAM` 을 가를 정보가 거의 없다** —
  자유도 하나(용량 축 절단)만 움직인다. ⚠ 단 이것은 **0.5 C CC 곡선**이지 OCV 가 아니다.
  저항 증가로도 같은 모양이 나온다 (**그리고 논문은 사이클 중 EIS 를 하지 않는다**).
- **S17 / Table S3 — 에너지밀도 계산 근거** (`[인쇄]`):

  | 항목 | 값 |
  |---|---|
  | 양극 AM 용량 / AM 비율 / 두께 / 면적용량 | 215 mAh g⁻¹ / 86 % / 95–105 µm (×2) / 6.4–6.8 mAh cm⁻² |
  | SSE 두께 | 30 µm |
  | **음극: 도금 Li 두께** | **30 µm** |
  | 집전체 | Al 12 µm (양극) / SUS 10 µm (음극) |
  | 면적 | 57 cm² (6.0 × 9.5 cm) |
  | 포장 필름 / 절연 필름 | 120 µm (×2) / – · 40×9 · 40×34 |
  | **총 두께** | **594 / 4140 / 13990 µm** |
  | 평균 방전 전압 | 3.76 / 3.79 / 3.79 V |
  | 셀 용량 | 0.64 / 5.87 / 21 Ah |
  | **에너지밀도** | **703 / 942 / 998 Wh L⁻¹** |

  ⚠⚠ **Ag–C 층(5–10 µm × 2)이 이 표에 없다** (G7, §12 D7). 그리고 **도금 Li 를 30 µm** 로
  잡는데 본문 SEM 은 **25 µm** 다.
  `[재현]` 같은 논문의 **실측 두께**(Table S2, WIP 후 **609.0 µm**)를 쓰면
  703 × 594/609 = **686 Wh L⁻¹**; 10 적층은 **4140 + 20×7.5 = 4290 µm** → 942 × 4140/4290 =
  **≈909 Wh L⁻¹**. **초록의 ">900" 은 살아남지만 여유가 거의 없다.**
- **S18**: 5 Ah 급 셀 사진 + 충방전 곡선. `[인쇄]` 5,870 mAh.

## 6.9 Supplementary Note 4 + Fig. S19 — 안전 (안 봄, 텍스트만)
§5.7 에 요약. `[인쇄]` 210 °C 1 h 유지에도 ASSB 전압 불변.

---

# 7. ★ 사용자가 물은 네 가지에 대한 직답

## 7.1 ① dead Li 를 재는 수단이 있나 — **부분적으로 있다. 그러나 dead Li 를 "다른 Li" 와 가르지는 못한다.**

이 논문이 Li 를 보는 **네 개의 채널**:

| # | 채널 | 무엇을 보나 | 정량? | 한계 |
|---|---|---|---|---|
| ① | **방전 상태 단면 SEM** (Fig. 3d, S5b) | 도금 Li 층의 **소멸** | ✗ | `[재현]` 검출 한계 ≈1 µm = **용량의 3.0 %**. 사이클당 손실(0.011 %)보다 **≈270 배 거칠다**. **음성 증거만** |
| ② | ★ **EELS Li 맵** (Fig. 5c/f/i/l) | Ag–C 층 **내부**의 Li 분포, nm 척도 | ✗ | `[도표]` **방전 후·100 사이클 후에도 Li 망이 남아 있다.** dead Li / LiC_x / SEI / 합금 잔여를 **가르지 못한다** (화학 이동 미사용). 본문은 "not significant" 로 넘긴다 |
| ③ | ★★ **XRD 의 Li₉Ag₄ 상** (Fig. 5n) | **합금에 담긴 Li** — 상으로 동정 | ✗ (Rietveld 없음) | 가역적(방전 후 소멸). **dead Li 는 아니다** — 오히려 "돌아오는 Li" 의 그릇 |
| ④ | **쿨롱효율 + 용량유지율** | 전하 수지로 본 **총 결손** | ○ (수치는 있다) | **전극·화학종 귀속 0**. 그리고 두 값이 **서로 맞지 않는다** (§12 D2) |

★★ **5호(Doux)와의 비교**: Doux 는 **SEI 는 상으로 잡히고(XRD) dead Li 는 원리적으로
안 보인다**(Li 금속은 XRD 로 안 보이고 토모는 밀도 대비뿐)고 남겼다.
6호는 **Li 특이 채널(EELS)** 을 처음 들여왔고 **Li 저장 상(Li₉Ag₄)** 을 처음 동정했다.
그러나 **dead Li 를 SEI-Li·합금-Li·LiC_x 와 가르는 관측은 여전히 없다.**
그리고 이 논문은 `[인쇄]` "isolated lithium" 을 **열화 기구로 지목**하면서
**한 번도 재지 않는다** (G10). `dead li` 문자열 **0 회**, `isolated` **2 회**(그중 하나는
"Ag NPs are isolated in the matrix of C" 로 다른 뜻).

**판정: Q7 은 5호에서 "절반" 이었고 6호에서도 "절반" 이다 — 채널은 늘었고 정량은 0 이다.**

## 7.2 ② 무음극에서 `LLI` 는 무엇이 되나 — **전하 수지 두 개뿐이고, 둘이 서로 안 맞는다.**

이 논문이 Li 인벤토리를 세는 방법은 **정확히 둘**이다:

```
(a) 첫 사이클 비가역분   ICE 결손 = Q_ch − Q_dis
    `[재현]` Ag–C 有 19 mAh g⁻¹ (8.2 %) · 無 16 mAh g⁻¹ (6.9 %)
    → 차분 3 mAh g⁻¹ = Ag–C 층에 귀속되는 몫의 상한  ★ 전극 귀속 가능한 유일한 조각

(b) 사이클당 CE 결손      1 − CE
    0.6 Ah 셀 `[도표]` 99.89 % (0–800) → 99.21 % (900–1000)
    20 mAh 셀 `[도표]` 99.97 %
```

**두께(SEM)는 인벤토리 계기가 못 된다** — §5.5 에서 보였듯 수지가 76 / 82 / 110 % 로
**비단조**다.

★★★ **그리고 (b) 가 용량유지율과 맞지 않는다** (0.6 Ah 셀):
`[재현]` CE 99.89 % 를 **영구 Li 손실**로 읽으면 사이클당 0.16 mAh g⁻¹,
1000 사이클 누적 **161 mAh g⁻¹**. 실제 손실은 **16 mAh g⁻¹** 이고, 양극이 가진
전체 Li 재고는 **215 mAh g⁻¹** 다. **약 10 배 어긋난다.**
거꾸로, 89 % @1000 을 순수 LLI 로 설명하려면 평균 CE 가 **99.988 %** 여야 한다.
→ **초록의 ">99.8 %" 와 본문의 "89 %" 는 같은 물리를 가리키지 않는다.**
★ **대조군이 같은 논문 안에 있다**: 20 mAh 셀은 CE 99.97 % ↔ 유지율 92.5 %@300
(= 99.974 %/cycle) 로 **맞는다.**
`[해석]` **가장 그럴듯한 설명은 0.6 Ah 셀의 CE 가 계측 바닥(floor)에 걸려 있다는 것**이다
(Fig. 6g 의 축은 95–101, Fig. S13c 는 99.4–100.0 — **분해능 자체가 다르다**).
논문은 이 대조를 **한 번도 하지 않는다** (G3).

★★★ **우리에게 남는 명제**: 무음극 셀에서 **`LLI` 의 추정자는 CE 와 용량유지율 둘이고,
둘 다 같은 양을 재지만 분해능이 다르다. 어느 쪽도 불확실성 없이 보고되면 안 된다.**
→ 새 개념 페이지 `concepts/anode-free-li-inventory-accounting.md` 로 컴파일했다.

## 7.3 ③ Ag 는 3 항 분해의 어느 칸인가 — **세 칸에 동시에 앉는다. 그래서 칸이 하나 더 필요하다.**

`Q_apparent = θ_AM · η(i,P) · Q_material` (음극이 무해하다는 전제로 세운 식) 위에서:

| Ag 의 역할 | 근거 | 들어갈 칸 |
|---|---|---|
| **Li 를 담는 활물질** (Li₉Ag₄) | `[인쇄]` Fig. 5n XRD, Fig. 4 3.5–3.55 V | **`Q_material`** (음극 쪽). `[재현]` 용량 **559 mAh g⁻¹(Ag)**, 셀 기준 **0.45–0.89 %** (8–16 mg Ah⁻¹) |
| **핵생성 자리 = 접촉/균일성** | `[인쇄]` "lowers the nucleation energy", Fig. 2 vs 3 | **`θ`** (음극 계면의 유효 접촉 면적) |
| **전하이동 속도론** | `[인쇄]` SI Note 1 의 "charge transfer kinetics might be the dominant factor"; Fig. S6 Ag 단독의 율 붕괴 | **`η(i)`** |
| ★ **비가역 Li 저장소** | `[인쇄]` SI Note 3 "irreversible Li remaining in Ag NPs" | **어느 칸도 아니다** — 이것은 **`LLI` 쪽 항**이다 |
| ★★ **위치가 사이클마다 바뀌는 상태변수** | `[인쇄]` "continuously moves … does not return" | **어느 칸도 아니다** — `θ`·`η` 의 **시간 의존 파라미터** |

★★★ `[해석]` **Ag 는 3 항 분해의 칸 하나에 안 들어간다.** 그리고 마지막 두 줄이
중요하다 — **음극이 자기 `Q_material`(Li₉Ag₄) 과 자기 `LLI`(비가역 Li) 를 동시에 갖고,
그 둘의 크기가 같은 자릿수(0.45–0.89 % vs 첫 사이클 8.2 %)** 다.
→ **3 항 분해에 "음극 인벤토리" 항을 붙이지 않으면 이 셀은 표현되지 않는다.**
(5호가 이미 "3 항 분해에 음극 항이 빠져 있다" 를 지적했다. 6호가 그것을 **수치로** 채운다.)

★ **그리고 좋은 소식이 하나 있다**: Ag 의 몫에는 **상한이 계산된다.**
`[재현]` Li₉Ag₄ 완전 형성을 가정해도 **셀 용량의 0.89 % 이하**다. 즉
**첫 사이클 비가역 8.2 % 중 Ag 합금이 설명할 수 있는 것은 최대 1/9 이다.**
나머지는 SEI + dead Li + LiC_x 다 — **그리고 이 논문은 그 셋을 가르지 않는다.**

## 7.4 ④ 셀 수·통계 — **없다. 사용자가 기대한 "계보 최초의 통계" 는 오지 않았다.**

- `n =` · `N =` · `three cells` · `average of` · `error bar` · `standard deviation` ·
  `replicate` · `uncertain*` **전부 0 회** (본문 10 쪽 + SI 18 쪽 전수).
- 모든 전기화학 그림이 **곡선 한 개 / 조건**이다. 0.6 Ah 프로토타입의 1000 사이클도
  **한 줄**이다.
- ★ **유일한 산포**: **Table S2 의 `±2.2–2.9 µm`** (셀 두께 4 시점).
  `[재현]` 상대 산포 **≈0.4 %**. ⚠ **`±` 의 정의도 n 도 없다** (G2).
  → **이 계보에서 두 번째 산포 수치**이고(첫째는 5호 Table S2 의 펠릿 4 개),
  **둘 다 전기화학이 아니라 기하다.**
- `[인쇄]` 정성적 산포 언급은 두 번: "the probability of short-circuiting **increased**"
  (>4 MPa) 와 "a short-circuit **occurred easily**" (C 단독) — **둘 다 확률을 말하면서
  분모를 밝히지 않는다.**

**판정: `assb` 6/6 편이 전기화학 라벨에 오차 막대를 붙이지 않았다.**
파우치 스케일업·산업체·*Nature Energy* 라는 세 조건이 모두 갖춰져도 바뀌지 않았다.

---

# 8. 방법론 평가 (비판적)

**강한 것**
1. **관측 채널이 많고 서로 독립이다** — SEM/EDS · TEM/HAADF · **EELS** · SADP · XRD ·
   X-선 CT · CV · EIS. 그리고 **진공 이송 홀더**로 대기 노출을 막는다 (황화물·Li 시료에
   필수인데 자주 생략되는 절차다).
2. **컷오프 전압을 축으로 쓴 해부(Fig. 4)** 가 깔끔하다 — 전압 → 면적용량 → 형태를
   **같은 축 위에** 놓는다. `assb` 1–5 호에 이런 설계가 없었다.
3. **대조군이 실제로 있다** — 맨 SUS(Fig. 2), C 단독·Ag 단독(Fig. S6),
   Ag–C 유/무(Fig. S7), 조성 4 수준(Fig. S13). **1–5 호 중 대조 설계가 가장 두껍다.**
4. **부정적 결과를 적는다** — Cu 집전체 실패, Ag 단독의 율 붕괴, 1:1 조성의 단락,
   수송 논증이 관측을 예측 못 한다는 고백.
5. 편집 품질이 높다 — 4호·5호에서 무거웠던 "본문이 잘못된 그림을 가리킨다" 류의
   사고가 **없다.**

**약한 것**
1. ★★★ **정량이 거의 없다.** 이 논문의 결론을 떠받치는 것은 **형태 관찰**이고,
   그 관찰에 **분율·면적·부피·상 분율이 하나도 붙지 않는다.** Ag 가 "상당 부분"
   이동했다(significant fraction), 입자가 "더 작고 성기다", Li 가 "완전히 사라진다" —
   전부 **형용사**다.
2. ★★★ **양극 사후 분석 0** (G6). 1000 사이클 11 %p 의 전극 귀속이 불가능하다.
   그리고 **사이클 중 EIS 가 없다** — EIS 는 온도 의존(S15)에만 쓰인다.
   → **4호(Shi)가 준 `R_LF`/`R_MF` 같은 전극 분해 정보가 여기엔 없다.**
3. ★★ **CE 와 유지율의 불일치를 검토하지 않는다** (§12 D2). 산업체 논문에서
   **CE 가 광고 문구**로 쓰이는데 그 계측 정밀도가 명시되지 않는다.
4. ★★ **운전 압력 창의 위 벽이 주장뿐이다** (§12 D3).
5. **60 °C 전용** (G13). 1000 사이클은 60 °C 의 수명이다.
6. **기구 설명이 추정의 연쇄다** — speculated / assume / presumed / believed 가
   핵심 문단마다 있다. 논문은 정직하게 그렇게 적지만, **초록과 결론은 그 정직함을
   달고 가지 않는다** ("dendrite-free", "effectively regulate").
7. **원자료 비공개** ("upon reasonable request").

---

# 9. 이 논문이 우리 3 항 분해에 붙는 자리

```
현재:  Q_apparent = θ_AM · η(i, P) · Q_material        (양극 중심)

6호가 요구하는 확장:

Q_apparent = θ_AM(N) · η(i, P, T) · Q_material
             ────────────────────────────────  양극
           −  L_anode(N)                        ← Ag–C 층이 삼키는 Li (비가역)
           +  Q_anode,rev(Li₉Ag₄, LiC_x)         ← 음극이 되돌려 주는 Li
```

**6호가 실제로 채운 칸**

| 칸 | 6호가 주는 것 | 값 |
|---|---|---|
| `η(i)` | 율 스윕 5 점 (0.2–2.0 C) | `[인쇄]` Q₁.₀C/Q₀.₂C **93 %**, 2.0 C 이용률 >80 %. `[재현]` 0.5 C 에서 **146/215 = 68 %** |
| **`η(T)`** ★ 새 축 | 온도 스윕 6 점 (60 → −10 °C) | `[인쇄]` 45 °C 99.5 · 25 °C 90.7 · −10 °C >40 %. 계면 저항 `[인쇄]` 5 → 50 Ω cm² |
| `η(P)` | **운전 압력 3 점 + 무압** | `[도표]` 2/3/4 MPa 에서 율특성 94.0/95.1/95.5 %; **무압 0.1 C 는 2 MPa 와 구별 안 됨** |
| `θ_AM` | **없다** — 공정(WIP)으로 처리하고 재지 않는다 | Table S2 의 **−5.51 % 치밀화**가 유일한 대리량 |
| `Q_material` | **없다** — 양극 사후 분석 0 | — |
| **`L_anode`** ★ 새 항 | 첫 사이클 비가역 + CE 결손 | `[재현]` **19 mAh g⁻¹ (8.2 %)**, 그중 Ag–C 귀속 **≤3 mAh g⁻¹** |
| **`Q_anode,rev`** ★ 새 항 | Li₉Ag₄ (XRD 로 동정, 가역) + LiC_x | `[재현]` Ag 몫 **≤0.89 %** of 셀 |

★★ **가장 중요한 한 줄**: `[재현]` **0.5 C 에서 `η ≈ 0.68` 이다** (146/215).
즉 **이 셀은 운전 중에 양극 재고의 32 %를 쓰지 않는다.**
`[해석]` → **그 32 % 가 `LLI` 에 대한 완충기로 작동한다.** Li 를 잃어도 양극이
사용하는 SOC 창이 이동할 뿐 용량은 덜 준다. **겉보기 용량유지율은 LLI 를 과소보고한다** —
이것이 §7.2 의 CE↔유지율 간극을 **부분적으로만** 설명한다 (완충 여력 69 mAh g⁻¹ <
CE 가 함의하는 누적 결손 161 mAh g⁻¹).

---

# 10. Q1~Q8 (닻 카드 기준)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1 접촉 손실 정량** | ★ **없다.** `contact loss` **1 회**뿐이고 그것도 **남의 논문 인용**(refs 5,37–39). `percolat*`·`tortuos*`·`void`(공극 뜻)·`inactive` **0 회** | 유일한 대리량 = Table S2 의 **셀 두께 −5.51 % (WIP)**. `θ` 도 접촉 면적도 없다. **공정으로 처리하고 재지 않는다** |
| **Q2 독립 관측** | ★ **많다 — 그러나 전부 음극이다.** SEM/EDS · TEM/HAADF · **EELS(Li)** · SADP · XRD(Li₉Ag₄) · X-선 CT(820 nm) · CV · EIS(온도만) | **양극 쪽 독립 관측 0** (G6). `LAM_PE` ↔ 접촉 손실을 가르는 관측은 **하나도 없다** |
| **Q3 라벨 층위** | **measured-electrochemical**(용량·CE·율·온도) + **measured-morphological 정성**(전부 수치 0) + **measured-phase 비정량**(Li₉Ag₄, Rietveld 없음). **적합 라벨 0** (`fit*`·`equivalent circuit` 0 회) | **오차 막대 0 · 셀 수 0**. ★ 유일한 산포 = **Table S2 ±2.2–2.9 µm**(정의·n 없음) |
| **Q4 유일성** | **없다 (6/6 편).** `identifiab*` 0 회 | **역문제를 아예 풀지 않는다** — 등가회로 적합도, 곡선 적합도 없다. 5호와 같은 형태(순수 forward 측정) |
| **Q5 Li-In** | **해당 없음** — `indium` 0 회. 음극은 무음극/Ag–C | ★ 그러나 **같은 문제가 다른 옷을 입고 나온다**: 기준 전위가 **전압창의 앞 10–17 % 에서 평탄하지 않다** (Fig. 4 + Fig. S4c) |
| **Q6 압력** | ★★★ **있다 — 그리고 축을 둘로 쪼갠다.** **제작 490 MPa WIP** (계보 최고, 비가역: Table S2) + **운전 2/3/4 MPa 스윕** + **무압 대조**(Fig. S12) | ⚠ 운전 스윕이 **3 점 · 폭 1.5 %p** 이고, `[인쇄]` **">4 MPa 단락" 은 데이터 0** |
| **Q7 dead Li** | ★★ **부분 — 채널은 늘었고 정량은 0.** ① 방전 단면 SEM(음성, `[재현]` 한계 3 % 용량) ② **EELS Li 맵**(방전 후에도 Li 망 잔존) ③ **XRD Li₉Ag₄**(Li 저장 상 동정) ④ CE | **dead Li 를 SEI-Li·합금-Li·LiC_x 와 가르는 수단은 없다.** `[인쇄]` "isolated lithium" 을 기구로 지목하고 **재지 않는다** |
| **Q8 화학·OCP** | ★★ **있다 — 계보 최초로 음극 쪽 전압축.** LZO(5 nm)-코팅 **LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂** : Li₆PS₅Cl : CNF : PTFE = 85:15:3:1.5, **6.8 mAh cm⁻²**, **215 mAh g⁻¹@0.2C**, 2.5–4.25 V, 전 구간 기울기 | **OCV·GITT 0 회** — 전부 CC 또는 CC–CV. ★ **Fig. 4a 가 컷오프 전압 ↔ 면적용량 5 점 사상**, ★★ **Fig. S16 이 1000 사이클 V–Q 6 곡선** |

---

# 11. 우리 프로젝트에 붙는 제약 (해석)

## 11.1 ★★★ "무음극은 OCP 가 평탄하다" 에 조건이 붙는다
Ag–C 무음극에서 **앞 9.5–16.6 % 의 용량 동안 음극 전위가 ≈1 → 0 V 를 훑는다**
(Fig. 4a + Fig. S4c). 그 구간의 완전지 곡선은 **양극 곡선의 밀기·늘이기로 표현되지
않는다.** → `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 **3 파라미터 창 모형**
(`a_PE, b_PE` + 평탄 상대극)은 **전압창 전체에 걸면 안 되고 3.6 V 위에서만** 성립한다.
⚠ 그리고 그 구간은 **Ag:C 조성에 따라 모양이 바뀐다** (`[인쇄]` Fig. S14: Ag 를 늘리면
3.5 V 부근에 평탄역이 생긴다) — **음극 조성이 완전지 곡선 모양의 상태변수**다.

## 11.2 ★★★ `LLI` 추정자 두 개의 **분해능**이 이 문제의 본체다
같은 논문 안에서 20 mAh 셀은 CE↔유지율이 맞고(99.97 ↔ 99.974 %) 0.6 Ah 셀은
**10 배 어긋난다**(99.89 ↔ 99.988 %). **셀이 커질수록 CE 의 상대 정밀도가 나빠지고,
그 순간 CE 는 `LLI` 의 추정자가 아니라 계측 바닥이 된다.**
→ [[near-optimal-set-width-measurement]] 를 이 자리에 그대로 걸 수 있다:
**"CE 99.8 % 와 99.99 % 를 구분할 정보가 자료에 있는가" 는 판정 가능한 질문이다.**
→ 새 페이지 [[anode-free-li-inventory-accounting]].

## 11.3 ★★★ 제작 압력과 운전 압력은 **다른 연산자**다
[[assb-stack-pressure-operating-window]] 는 5호의 **운전 압력** 스윕 위에 세워졌다.
6호가 축을 하나 더 준다:

| | 5호 (Doux, Li 금속 펠릿) | 6호 (Lee, 무음극 파우치) |
|---|---|---|
| 제작 압력 | 370 MPa (펠릿) / 25·120 MPa (전극) | **490 MPa 등방(WIP), 대기 중** |
| 운전 압력 | **1–75 MPa 스윕** | **2 / 3 / 4 MPa + 무압** |
| 운전 상한 | `[인쇄]` **75 MPa 도금 전 단락** | `[인쇄]` **>4 MPa 에서 단락 확률 증가** (⚠ 데이터 없음) |
| 저압에서 | 1 MPa → 임피던스 >500 Ω | **무압 0.1 C 가 2 MPa 와 구별 안 됨** |
| 압축의 가역성 | 임피던스 이력(77 % 영구) | **두께 이력 — 7 일 무압에 +0.8 µm 만 복원** |

★★ `[해석]` **두 논문이 정반대로 보이지만 모순이 아니다.**
Doux 의 셀은 **제작 압력이 낮아서** 운전 압력이 계면을 만들어야 했고,
Lee 의 셀은 **490 MPa 가 이미 만들어 놓아서** 운전 압력이 할 일이 없다.
→ **창의 아래 벽 위치는 `f(제작 압력 이력)` 이다.** 그리고 **위 벽은 운전 압력 축에서
훨씬 낮다** (4 MPa vs 75 MPa) — 모집단이 다르지만(파우치 적층 vs 펠릿), 방향은
**무음극·대면적으로 갈수록 창이 좁아진다**는 것이다.
→ [[assb-pressure-reapplication-separation-test]] 의 `P↑` 분리 연산자는
**이 셀에 적용 불가**다: 4호가 쓴 300 MPa 는 이 셀 상한의 **75 배**다.

## 11.4 ★★ 열화의 **모양**이 또 계단이다 (두 번째 표본)
`[도표]` Fig. 2d(맨 SUS): 사이클 10 까지 평평 → 15–27 에 붕괴 → 50 에 6 %.
4호(Shi)의 양극 급락과 **모양이 같은데 전극이 다르다.**
★ `[해석]` **"급락 = 양극 접촉 손실" 이라는 귀속이 위험하다.** 같은 모양이
음극 실패에서도 나온다. → `θ(N)` 을 계단으로 모형화할 때 **어느 전극인지는
곡선 모양으로 정해지지 않는다.**

## 11.5 ★★ 이용률 `η` 가 `LLI` 의 완충기다
`[재현]` 0.5 C 에서 `η ≈ 0.68`. **양극 재고의 32 % 가 놀고 있고**, 그만큼 Li 손실이
용량 손실로 즉시 나타나지 않는다.
→ **겉보기 유지율은 LLI 의 하한이다.** 액체셀 갈래의 `LLI` 추정에도 같은 논리가
걸린다 (N/P 비가 크면 LLI 가 숨는다 — [[np-lip-ocv-reparametrization]] 의 좌표에서
`Li/P` 가 움직여도 창 안에서 안 보이는 구간).

## 11.6 ★ 음극이 시간에 따라 바뀌는 재료다
`[인쇄]` Ag 가 **매 사이클 집전체 쪽으로 이동하고 돌아오지 않는다.**
`[도표]` 100 사이클 후 Ag NP 가 작아지고 아래로 몰린다.
→ **"동일한 음극 OCP" 라는 가정이 사이클 축에서 깨진다.** 액체셀에서 우리가 쓰는
`halfcell-ocp-shape-invariance` 의 파괴가 **ASSB 무음극에서는 음극 쪽에서 먼저** 온다.

## 11.7 ★ 우리가 싸게 공급할 수 있는 것
1. **CE 분해능 판정**: 주어진 계측 잡음에서 CE 와 유지율이 **같은 LLI 를 지지하는지**
   재는 것. 6호의 두 셀(20 mAh vs 0.6 Ah)이 **정답이 있는 시험 문제**다.
2. **완충기 정량**: `η` 가 0.68 일 때 LLI → 용량 손실 전달함수. 전방 모형으로 싸다.
3. **음극 인벤토리 항을 붙인 3 항 분해**의 식별 가능성 — 항이 늘면 폭이 얼마나
   넓어지는가. [[near-optimal-set-width-measurement]] 를 그대로 건다.

## 11.8 `composite-cathode-percolation-utilization` 은 **건드리지 않았다**
지시대로다. 그리고 내용상으로도 옳다 — 이 논문은 **양극 `θ` 에 대해 아무것도
주지 않는다** (Q1 = 없다). 그 페이지는 이미 **320 줄**로 SCHEMA 200 줄 권고를 넘겼다.

---

# 12. 어긋남 원장 (본문 ↔ 그림 ↔ 초록 ↔ SI)

⚠ **미리 밝힌다: 이 논문은 2–5 호보다 어긋남이 적고 가볍다.** *Nature Energy* 의
편집 품질이 보이고, 4·5 호에서 가장 무거웠던 두 형태 — (a) 결론을 떠받치는 문장이
자기 그림과 충돌, (b) 인용조차 안 된 SI 가 본문을 반증 — 중 (b) 는 **여기 없다**
(모든 SI 그림이 본문에서 인용된다). (a) 는 **세 건**이고 그 셋이 무겁다.
억지로 개수를 맞추지 않았다.

| # | 어긋남 | 무게 |
|---|---|---|
| **D1** | ★★ **초록·Fig. 6g 라벨 ">99.8 %" ↔ 자기 그림.** `[도표]` 800–900 구간 CE 중앙값 **99.80 %**, **900–1000 구간 중앙값 99.21 % · 최저 97.42 %**. 즉 **광고된 1000 사이클의 마지막 ≈15 % 는 대부분 99.8 % 아래**다. 본문·초록·캡션에 **언급 0**. `[해석]` 이 하강은 음극 실패(dead Li·연성 단락)의 전형적 전조인데 논문은 그것을 논하지 않는다 | **무겁다** |
| **D2** | ★★★ **CE 와 용량유지율이 10 배 안 맞는다 (0.6 Ah 셀).** `[재현]` CE 99.89 % ⇒ 1000 사이클 누적 결손 **161 mAh g⁻¹**; 실측 손실 **16**; 양극 전체 재고 **215**. 89 % @1000 을 설명하려면 CE 가 **99.988 %** 여야 한다. ★ **같은 논문의 20 mAh 셀(Fig. S13)은 맞는다**(99.97 ↔ 99.974 %) — **CE 축의 눈금도 다르다**(95–101 vs 99.4–100.0). **논문은 두 셀을 한 번도 비교하지 않는다** | **가장 무겁다 — 그리고 우리 축이다** |
| **D3** | ★★ **"4 MPa 초과에서 단락 확률 증가" 에 데이터가 없다.** Fig. S11 의 압력 점은 **2·3·4 MPa** 세 개뿐이고 4 MPa 초과 실험이 본문·SI 어디에도 없다. 셀 수·단락 횟수·조건도 없다. **운전 압력 창의 위 벽 전체가 이 한 문장에 걸려 있다** | **무겁다** |
| **D4** | 운전 압력이 세 곳에서 다르게 적힌다: 본문 `[인쇄]` "**2–4 MPa**" ↔ Fig. 6c 캡션 `[인쇄]` "**2 MPa**" ↔ SI Note 2 `[인쇄]` "**2 MPa** was adopted" | 가볍다 |
| **D5** | **C 단독 음극의 율특성이 SI 안에서 안 맞는다.** Fig. S13a `[도표]` 1.0C/0.33C = **75 %** ↔ Fig. S6a `[도표]` 181/197 = **≈92 %**. (⚠ 두 그림이 같은 셀이라고 적혀 있지 않으므로 다른 셀일 수 있다 — 그런데 **그렇다면 셀 간 산포가 17 %p 라는 뜻**이고, 그것 역시 보고되지 않는다) | 중간 |
| **D5-b** | **C 의 전기화학 활성에 대한 두 문장이 충돌한다.** 본문 `[인쇄]` Fig. 4 설명: 3.5 V 까지의 기울기는 "primarily associated with the **C lithiation**" ↔ 본문 `[인쇄]` 결론 문단: "there is **not clear evidence that confirms the involvement of C in the electrochemical reactions**" | 중간 |
| **D6** | ★★ **"잔류 Li 없음" ↔ EELS 맵.** `[인쇄]` "**no residual Li deposits or Li dendrite features were found** in the Ag–C nanocomposite layer after these cycles" ↔ `[도표]` Fig. 5i(방전 후)·5l(100 사이클 후)의 **Li(빨강) 망이 pristine(5c, 빨강 없음) 대비 뚜렷하다**. 두 진술의 대상이 다르다(Li **금속 덩어리** vs Li **신호**)는 변호가 가능하지만, **논문은 그 구분을 명시하지 않고 정량도 하지 않는다**. 본문은 Fig. 5i 를 `[인쇄]` "the compositional variation was **not significant**" 로만 처리한다 | **무겁다 — 우리 축이다** |
| **D7** | **에너지밀도의 두께 예산이 자기 측정과 안 맞는다.** Table S3 `[인쇄]` 총 두께 **594 µm** ↔ Table S2 `[인쇄]` WIP 후 실측 **609.0 ± 2.4 µm**. 차이 **15 µm ≈ Ag–C 층 두 장(2 × 7.5 µm)** 이고 실제로 **Ag–C 가 Table S3 에 없다**. `[재현]` 실측 두께로 다시 계산하면 703 → **686 Wh L⁻¹**, 942 → **≈909** | 중간 |
| **D8** | Fig. 6b 본문 `[인쇄]` "SSE and Ag–C nanocomposite layers (**30 μm combined**)" ↔ Methods `[인쇄]` SSE 만 압착 후 **30 µm**, Ag–C **5–10 µm** (합 35–40) | 가볍다 |
| **D9** | Fig. 5n 안의 모식도가 충전 상태를 **"Ag–C alloy"** 라고 적는다 (본문·캡션은 Ag–**Li** 합금) | 가볍다(오식) |
| **D10** | ★ **도금 Li 두께와 통과 전하의 수지가 닫히지 않고 비단조다.** `[재현]` 110 / 82 / 76 % (3.6 / 4.0 / 4.25 V). 3.6 V 에서 Ag–C 가 1.12 mAh cm⁻² 를 저장했다면 도금 Li 는 0 이어야 하는데 **6 µm** 가 보인다. **논문은 이 수지를 한 번도 맞추지 않는다** | 중간 |
| **D11** | SI Note 3 `[인쇄]` Ag:C=1:1 의 "CE was very low (**<95 %**)" ↔ Fig. S13c 의 **y 축 바닥이 99.4 %** 라 그 값이 자기 그림에 **보이지 않는다** | 가볍다 |
| **D12** | ★ **"isolated lithium" 을 열화 기구로 지목하고 한 번도 재지 않는다** (`[인쇄]` Fig. 2 문단). 같은 논문이 EELS·XRD·CT 를 다 쓰면서 **그 양만 비운다** | 중간 |
| **D13** | **초록의 ">900 Wh l⁻¹" 와 "1,000 cycles" 가 같은 셀이 아니다.** 900 Wh l⁻¹ 는 **5 Ah 10-적층셀**(0.05 C, **무압**, `[인쇄]` 942), 1000 사이클은 **0.6 Ah bi-cell**(0.5 C, 2 MPa, `[인쇄]` **703** Wh l⁻¹). 초록은 둘을 한 문장에 놓는다 | 중간 |

**합계 14 건** (1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · **6호 14**).
무거운 것은 **D2 · D1 · D3 · D6** 넷이고, 그중 **D2 와 D6 은 정확히 우리가 물은 축**
(무음극 `LLI` 의 계정, dead Li 의 관측)이다.

---

# 13. 이 digest 가 주장하지 않는 것

- **Ag–C 층이 작동하지 않는다고 주장하지 않는다.** Fig. 2 ↔ Fig. 6g 의 대조
  (50 사이클에 6 % ↔ 1000 사이클에 89 %)는 크고, 대조군 설계도 이 계보에서 가장 두껍다.
- **CE 가 틀렸다고 주장하지 않는다.** D2 는 **CE 와 유지율이 같은 물리를 지지하지
  않는다**는 산술적 관찰이고, 가장 그럴듯한 해석은 **0.6 Ah 셀의 CE 가 계측 바닥**
  이라는 것이다. 논문에 계측 정밀도가 없으므로(G3) **어느 쪽인지 정할 수 없다.**
- **EELS 의 빨강이 dead Li 라고 주장하지 않는다.** LiC_x·SEI·합금 잔여일 수 있고,
  이 논문의 EELS 는 그것을 가르지 않는다. 주장하는 것은 **"방전 후에도 Li 신호가
  남아 있고 논문이 그것을 정량하지 않았다"** 뿐이다.
- **">4 MPa 에서 단락한다" 를 사실로 옮기지 않는다.** 데이터가 없다 (D3).
  [[assb-stack-pressure-operating-window]] 에도 **"데이터 없는 주장"** 으로만 적었다.
- **이 논문이 닻 카드의 질문(양극 `LAM_PE` vs 접촉 손실)에 답한다고 주장하지 않는다.**
  양극 사후 분석이 **0** 이다 (G6). 이 논문의 기여는 **음극 축**이다.
- **수치를 정본으로 쓰지 않는다.** 정본은 원문 PDF (`pdf_sha256_*` 로 봉인).
  `[재현]` 표시가 붙은 것은 전부 **내 계산**이고 가정을 본문에 적었다.
- **모집단**: LZO-NMC(Ni 90) / Li₆PS₅Cl / Ag:C=1:3 / **60 °C** / 2.5–4.25 V /
  0.5 C / 2 MPa 운전 / 490 MPa WIP 제작 / **조건당 셀 수 미상**.
  다른 온도·다른 음극·다른 제작 압력으로 옮기면 숫자가 그대로 가지 않는다.

---

# 14. 관련

- `questions/assb-contact-loss-vs-lampe.md` — 닻. Q1~Q8 채움표에 6호 행 추가.
- `concepts/anode-free-li-inventory-accounting.md` — ★ **이 ingest 가 만든 새 개념 페이지.**
- `concepts/assb-stack-pressure-operating-window.md` — 제작 압력 ↔ 운전 압력 분리 추가.
- `concepts/assb-apparent-capacity-decomposition.md` — 음극 인벤토리 항 + `η(T)` 추가.
- `concepts/assb-pressure-reapplication-separation-test.md` — `P↑` 연산자의 적용 불가 조건.
- `raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md` — 5호.
  Q7 의 나머지 절반을 여기에 넘겼고, 6호가 **채널만** 채웠다.
- `raw/papers/shi2020_mechanical-degradation-assb-cathode.md` — 4호.
  급락 모양의 첫 표본. 6호 Fig. 2d 가 **음극 쪽 두 번째 표본**이다.
- `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 · §2-A3 — 3 파라미터 창 모형의 적용
  구간이 좁아지고(§11.1), §2-A3 의 열린 자리에 **관측 채널 셋**이 들어왔다(§7.1).
