<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 기준 = papers/agarwal2026_umlip_applicability_domain_ssb_interfaces.md
     2026-11-10 신규 작성 (논문 에이전트 · 사용자 읽기 목록 124 번 · cascade 트랙 [1저자 = 사용자] 의 문헌 갭 보고서가 꼽은 '갭을 단정하기 전에 본문을 봐야 하는 다섯 편' 중 하나).
     사용자 지정 갭 질문 7 개 → §4 (항목마다 쪽 · 절 · 그림/표 번호).
     그림: 크롭 16 장 (본문 그림 5 + SI 그림 1 + 표 10). 그림 6 장 전부 Read 로 실제로 봤다 (`Fig. S1` 은 도구가 놓쳐 손 크롭).
           표 10 장은 관례대로 PDF 텍스트 + 쪽 렌더로 옮겼다 (tab_*.png 을 이미지로 읽지 않았다).
     ⚠ 'figure-read ≈' 값은 PDF 에 박힌 원본 래스터 (이 논문의 그림은 전부 래스터다) 에서 축 눈금 픽셀로 보정해 읽은 것이다 (논문이 표로 준 값이 아니다).
       검산: `Fig. 1a` 막대 8 개 ↔ `Table 2` (차 ≤ 0.01 V) · `Fig. 1b` 곡선 양 끝 15 점 ↔ `Table 2` (차 ≤ 0.02 eV/atom) · `Fig. 2` 막대 끝 7 개 ↔ `Table 3` (차 ≤ 0.02 eV)
             · `Fig. 5a` 코팅 5 종 ↔ 2015 편 SI 계단표 (차 ≤ 0.01 V · LiTaO₃ 점선 끝만 0.07 V 다름) · `Fig. 4` 황화물 곡선 ↔ `Table 5` · `Table S3` 구간 범위 안.
     우리 쪽 숫자는 CLAUDE.md · kb 카드에 이미 적힌 것만 따로 줄에 적었다 — 문헌 값과 같은 표에 놓지 않았다 (cascade · 계면 반응성 절대값은 경로만). -->

# First principles study on electrochemical and chemical stability of solid electrolyte–electrode interfaces in all-solid-state Li-ion batteries — Zhu, He & Mo (*J. Mater. Chem. A* 2016)

> slug `zhu2016_first_principles_interface_stability_assb` · DOI `10.1039/C5TA08574H` · type `계산 열역학 (MP hull · grand potential · pseudo-binary · 자체 실험 0 · AIMD/MLIP 0)` · PDF `13b8013f-124._First_principles_study_…pdf` (inbox #124 · 15 pp = 표지 1 + 본문 14 [pp. 3253–3266 · refs 69]) + SI `6c3b8a9a-124._Sup_First_principles_study_…pdf` (7 pp · `Table S1`–`S4` · `Fig. S1`) · digested `2026-11-10` · status ✅ · 태그 **[외부·계산·cascade 갭 판정 (다섯 편 중 하나)·`[Zhu16]`]**
> elements: Li, P, S, Ge, O, N, Co, La, Zr, Ti, Al, Nb, Ta, Si
> methods: DFT, ESW

> **저자 (표지 그대로)**: **Yizhou Zhu**ᵃ, **Xingfeng He**ᵃ, **Yifei Mo**\*ᵃᵇ — ᵃ Univ. of Maryland, Materials Science and Engineering · ᵇ Univ. of Maryland Energy Research Center (College Park, MD). 교신 `yfmo@umd.edu`.
> 접수 2015-10-25 · 채택 2015-12-11 · 온라인 2015-12-11 · *J. Mater. Chem. A* 4권 9호 (2016-03-07) **표지 논문** (PDF 1 쪽이 표지 그림).
> 자금: US DOE EERE **DE-EE0006860** · 계산 자원 UMD 슈퍼컴퓨팅 + XSEDE (NSF **TG-DMR130142**). 사사: Chunsheng Wang · Fudong Han (UMD) — 본문이 '실험과 일치' 의 근거로 드는 ref 12 (Han … **Zhu** … Wang, *Adv. Mater.* 2015) 의 저자들이다 (같은 그룹 · §18-10).
> 🎤 **관련 발표**: 해당 없음 — `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열 (대기열이 있는 talk 은 이것 하나) 을 확인했고 이 논문은 그 표에 없다.
> **계보**: 같은 세 저자의 2015 편 = [`zhu2015_esw_grand_potential_origin`](zhu2015_esw_grand_potential_origin.md) (*ACS AMI* 7, 23685 · 이 논문 ref 14 · SE **단독** 창) 의 **직계 후속** — 같은 기계에 전극 (LiCoO₂) 을 붙이고, 닫힌계 pseudo-binary · 전위 아래 pseudo-binary · 계면 3 유형 분류를 더했다. 2015 편 digest §15 가 *"전극–SE pseudo-binary 는 2016 후속 (Zhu/He/Mo JMCA) 에서"* 라고 가리키던 편이 이것이다. pseudo-binary 형식의 출처로 이 논문이 드는 것은 ref 31 = [`miara2015_llzo_cation_dopants_cathode_interphases`](miara2015_llzo_cation_dopants_cathode_interphases.md), 같은 해 독립 형식화는 [`richards2016_interface_stability_pseudobinary`](richards2016_interface_stability_pseudobinary.md) (이 논문은 인용하지 않는다).
> litdb 의 다른 digest 12 편이 이미 이 논문을 인용하고 있었다 (일부는 `[Zhu16]` 약칭 · §20 — 그 인용값을 원문과 대조했다).

---

## 0. 이 digest 를 읽는 법

이 논문은 2015 편이 SE 하나만 놓고 물었던 질문 (*"이 전위에서 SE 가 버티나"*) 을 **SE 와 양극이 맞닿은 자리**로 옮긴 것이다. 셋을 갈라서 읽는다.

1. **논문이 실제로 계산한 것** (§5–§10) — 0 K Materials Project hull 위의 반응 열역학. SE 7 종 (LGPS · Li₃PS₄ · LLZO · LLTO · LATP · LiPON 두 조성) + 기준 Li₂S × 양극 LiCoO₂ (방전 LCO · 충전 대리 Li₀.₅CoO₂) + 코팅 후보 18 종.
   ⛔ **Li₆PS₅Cl 은 없다. Li₇P₃S₁₁ 도 없다. NCM · LiNiO₂ 도 없다. 도펀트 계열도 없다.** (아지로다이트는 *"Li₃PS₄ 의 할라이드 도핑"* 한 문장의 인용 [65] 로만 나온다.)
2. **논문이 계산하지 않고 문헌으로 채운 것** (§11 · §18) — 계면 산물이 전자를 통하느냐 · Li 를 통하느냐. 계면 3 유형 분류는 전부 여기에 선다.
3. **우리에게 넘어오는 것** (§4 · §15 · §16) — 값이 아니라 **식 · 정규화 · 분류 틀**이다. 우리 조성의 값은 이 논문에 없으므로 숫자 대조는 하지 않는다.

**본 그림 / 안 본 그림** — 크롭 16 장 중 그림 6 장 (`Fig. 1`–`Fig. 5` · `Fig. S1`) 을 전부 실제로 봤다. 표 10 장 (`Table 1`–`Table 6` · `Table S1`–`Table S4`) 은 PDF 텍스트와 쪽 렌더로 옮겼다 (크롭 PNG 를 이미지로 읽지 않았다). 그림과 본문 · 표가 어긋난 곳은 §18-11 에 모았다 (단위 표기 2 · 표–그림 불일치 3).

**이 논문에는 장벽 · MD 가 없다** — 홉 수 검산 · 관측창 한 줄 · 흡착 배위수 규율은 해당 없음.

---

## 1. 한 줄 요약

MP hull 위에서 ① SE 단독의 전기화학 창 ② O · S · Co 화학퍼텐셜 창의 겹침 ③ SE–LiCoO₂ 닫힌계 상호 반응 ④ 2–5 V 전위 아래의 SE–LiCoO₂ 반응 ⑤ 코팅층 18 종의 창과 양쪽 반응을 차례로 계산해 — **대부분의 SE–전극 계면은 열역학적으로 불안정하고 계면상 (interphase) 형성이 보편적**임을 보인다. 황화물–LCO 가 가장 나쁘고 (닫힌계 상호 반응 에너지 −340 ~ −564 meV/atom · 산물 Co₉S₈ + Li₂SO₄ + Li₃PO₄ + Li₂S · 원인은 Co 가 아니라 **O 와 S 음이온 화학퍼텐셜의 불일치**), 산화물 SE–LCO 는 0 ~ −53 meV/atom, LiPON 은 그 사이다. 계면의 운명은 **생긴 산물이 전자를 통하느냐**로 갈린다고 보고 Wenzel 2015 의 3 유형 (안정 / 혼합 전도 계면상 / 전자 절연 SEI) 으로 **정성 분류**하며, 코팅층은 '혼합 전도 계면 (Type 2) 을 인공 SEI (Type 3) 로 바꾸는 것' 으로 설명한다. **산물의 물성은 계산하지 않았고 (문헌 인용), 점수 · 순위로 쓴 수는 반응 에너지와 창뿐이다.**

---

## 2. 메타

| 저자 | 저널/년 | DOI | 계 | 연구유형 |
|---|---|---|---|---|
| Y. Zhu, X. He, Y. Mo\* (Univ. of Maryland) | *J. Mater. Chem. A* **4**, 3253–3266 (2016) · 표지 논문 | 10.1039/C5TA08574H | SE 7 (LGPS · Li₃PS₄ · LLZO · LLTO · LATP · LiPON₀.₁₄ · LiPON₀.₄₆) + Li₂S × {LiCoO₂ · Li₀.₅CoO₂ · Li 금속 (0 V)} + 코팅 18 종 | 계산 열역학 (MP + 일부 자체 DFT) · 실험 0 |

- 랩 표준 표기: *J. Mater. Chem. A*, 4, 3253 (2016).
- 출처 표지: **[외부]** (Maryland Mo 그룹 · 우리 그룹 아님). 우리 grand-potential ESW 방법의 원저자 그룹이다.

---

## 3. 이 논문이 던지는 질문 (Introduction · pp. 3253–3254)

1. 전고체전지의 벌크 전도도는 액체 수준 (1–10 mS/cm) 에 왔는데 출력은 못 따라간다 — 병목은 **계면 저항**이다. 통상 원인으로 접촉 불량 [5] · 접촉의 기계적 파손 [6] · 상호 확산 [7] · Li 결핍 공간전하층 [2] 을 든다. *"The possibility of decomposition at the interfaces is often overlooked since the SEs are claimed to have excellent stability."*
2. 그런데 실험은 계면 분해를 이미 봤다 — LiCoO₂ 와 Li₂S–P₂S₅ [8] · LLZO [7] 사이에 수십–100 nm 계면상 (TEM · EDX) · Li 금속과 LiPON [9] · LLTO [10] · NASICON [11] 의 반응 (in situ XPS) · LGPS 의 환원 · 산화 (CV [12] · 계산 [13, 14]).
3. 계면상이 생기는 길은 셋이다 (p. 3254): *(1) the reduction or oxidation of SEs under an applied potential … (2) the chemical reactions between the SE and the electrode materials caused by the chemical incompatibility … (3) the electrochemical reactions of the SE–electrode interfaces during the voltage cycling.*
4. 이 세 길의 **열역학**은 잘 정의되는데 SE–전극 조합에 대해 정리된 적이 없다 → 계산 틀을 세워 흔한 SE 와 전극의 계면 열역학을 내고, 계면을 유형으로 나눠 대책 (코팅) 을 논한다.

---

## 4. ★ 갭 질문에 대한 답 (cascade 문헌 갭 보고서 · 표 '가' 줄)

> 물음의 출처: `reports/황화물 분해 부피 도펀트 문헌 갭.md` — *"계면 산물 물성을 점수로 썼나 · 썼다면 A 의 '산물 물성 순위 0 건' 을 'SE 도펀트에 대해 0 건' 으로 좁힌다"*.
> 쪽 번호는 저널 쪽 (3253–3266) 이다. PDF 쪽 = 저널 쪽 − 3251.

| # | 질문 | 답 | 근거 위치 |
|---|---|---|---|
| 1 | 산물 물성을 **점수 · 순위**로 쓰나 | **아니오 — 정성 3 유형 분류다.** 산물의 전자 · 이온 전도성은 계산하지 않고 문헌 인용으로 붙인다. 수로 줄 세운 것은 반응 에너지와 전기화학 창뿐 | §4 Discussion pp. 3263–3264 · `Table 4` · `Table 6` |
| 2 | 다룬 계 | SE 7 종 (+ 기준 Li₂S) · 닫힌계 SE–{LCO · L₀.₅CO} 14 쌍 · 전위 아래 SE–LCO 7 쌍 · Li 금속은 0 V 한계로 · 코팅 18 종 × 4 상대 = 72 값. **황화물은 Li₃PS₄ · LGPS 둘뿐 — Li₆PS₅Cl · Li₇P₃S₁₁ 없음** | `Table 1` (p. 3255) · `Table 4` (p. 3260) · `Table 5` (p. 3261) · `Table 6` (p. 3262) · `Table S2`–`S4` |
| 3 | 방법 | MP hull (pymatgen) · grand potential (식 2–4) · 닫힌 pseudo-binary 와 mutual 반응 에너지 (식 5–10) · Li 열린 pseudo-binary 를 φ = 2–5 V 로 훑음 (식 11–14) · MP 보정 그대로 | §2 Methods pp. 3254–3256 |
| 4 | 도펀트 / 조성 변화 분석 | **황화물 호스트에 원소를 바꿔 넣은 비교는 없다.** 있는 것: LiPON 의 N 함량 2 점 · 코팅의 Li 함량 계열 · LGPS ↔ Li₃PS₄ (Ge 유무) · 설계 문장 (계산 없음: Ti · Ge 회피 / 음이온 혼합 · 할라이드 도핑 · 옥시황화물 기대) | §3.3 p. 3260 · §3.5 pp. 3262–3263 · §4 p. 3264 |
| 5 | 분해 **부피 변화** | **계산 없음.** 언급은 한 문장 (*"a repetitive volume change and the failure of the mechanical contact"*) — 인용 [12] 에 기댄 정성 서술 | §4 p. 3264 |
| 6 | 코팅 선택 지침 | 넓은 창 (환원 < 2 V · 산화 ~4 V) · 양쪽과의 상호 반응 에너지가 0 에 가까울 것 · 얇을 것 (수 nm) · 전자 절연 + 이온 전도 (인공 SEI). 후보 18 종 — 황화물 쪽은 Li 가 적은 조성, LLZO 쪽은 Li 가 많은 조성 | §3.5 pp. 3261–3263 · `Fig. 5` · `Table 6` · `Table S4` · `Fig. S1` |
| 7 | 2.5–4.25 V 로 읽으면 | 창 전체가 황화물의 산화 개시 (2.15–2.31 V) 위다. Li₃PS₄–LCO 평형 산물 가운데 Li₃PO₄ 는 2.91 V 까지만 있고 3.26 V 위로는 Li 를 담은 산물이 없다. 전자 전도성 Co 황화물은 창 전체에 있다 | `Table 2` · `Table 5` · `Table S3` · `Fig. 4` · `Fig. 5a` |

**갭 보고서 문장에 대한 판정 (이 논문 한 편 기준)**
- *"분해 산물의 물성으로 순위를 매긴 연구는 코팅 · 물질 전체 수준뿐 — SE 도펀트에 대해서는 0 건"* → **고칠 필요 없다.** 이 논문은 산물 물성을 계산하지도 점수화하지도 않는다. 오히려 "원칙은 2015–2017 년에 섰다" 쪽의 근거가 하나 는다 — 산물의 **전자 전도** (유형을 가름) 와 **이온 전도** (Type 3 의 저항을 가름) 두 축을 양극 쪽까지 문장으로 세운 편이다.
- 덧붙일 것 하나: 보고서 112 행의 *"Zhu 2017 … 계산으로 '계면을 위한 도핑' 을 명시한 **유일한** 제안"* 은 좁혀 써야 한다. 이 논문 (2016 · p. 3264) 이 이미 *"anion mixing should be a viable strategy for the SE material design … doping of Li₃PS₄ with halides, such as LiCl and LiI … we expect some oxysulfide compounds as promising SEs"* 와 *"the use of these cations [Ti, Ge] should be avoided"* 를 적는다 (2015 편에도 같은 취지 — 그 digest §9). 계산으로 받친 도펀트 비교가 아니라 설계 문장이라는 점은 Zhu 2017 과 같다.
- 판정은 사용자 몫이다 (보고서는 이 digest 가 고치지 않았다).

### 4.1 질문 1 — 점수 · 순위인가, 정성 분류인가

**분류의 출처와 이름 (p. 3263 · 원문 그대로)**
> *"Following the definitions by Wenzel et al.,¹⁰ we distinguish three different types of interfaces based on the interface stability and interphase properties."*
> - *"**Type 1 interface** – stable interfaces with no decomposition interphase layer. Type 1 interfaces are either thermodynamically intrinsically stable or kinetically stabilized over the cycling voltage range."*
> - *"**Type 2 interface** – interfaces formed with interphase layers that are mixed ionic and electronic conductors (MIECs)."*
> - *"**Type 3 interface** – interfaces formed with a stable solid-electrolyte interphase (SEI). … the interphase layers in Type 3 interfaces are electronically insulating and are stable during the electrochemical cycling"*

ref 10 = Wenzel, Leichtweiss, Krüger, Sann, Janek, *Solid State Ionics* 278, 98 (2015) — 분류 자체는 Janek 그룹 것이고 이 논문은 그것을 계산한 계면들에 붙였다.

**분류 기준 (p. 3263)**
> *"The electronic conductivity of the interphase, regardless of specific electronic conductive mechanisms, determines whether the interface is Type 2 or Type 3. If the formed interphase is a MIEC, the simultaneous transport of Li ions and electrons would enable continued decomposition reactions that are thermodynamically favorable."*
> *"The interfacial resistance of Type 3 interfaces is highly dependent on the ionic conductivity of the SEIs."*

즉 축은 둘이다 — **전자 전도 여부가 유형을 가르고 (2 ↔ 3), 이온 전도도가 Type 3 안에서 좋고 나쁨을 가른다.** 문턱 값 · 수식 · 점수는 없다.

**어느 계면이 어느 유형인가 (pp. 3263–3264 · 저자 배정)**

| 계면 | 유형 | 저자가 든 이유 | 그 물성의 출처 |
|---|---|---|---|
| Li–LLZO | Type 1 일 수 있음 | 동역학적 안정화 + 구동력이 작음 (0 V 에서 −0.02 eV/atom) | 계산 (`Table 2`) + CV 문헌 [34] |
| Li–LiPON · Li–Li₃PS₄ | *"typical Type 3"* | 산물 Li₂O · Li₃N · Li₃P (· Li₂S) 가 전자 절연 · Li₃N · Li₃P 는 빠른 Li 전도체 | 문헌 [9, 14, 63, 64] |
| Li–LGPS · Li–LLTO · Li–LATP | *"typical Type 2"* | 전자 전도성 Li–Ge 합금 · 리튬 티타네이트 → 환원이 계속됨 | 문헌 [12, 32] |
| 황화물 SE–LCO | **Type 2 와 Type 3 의 혼합** (*"not purely Type 2 … but rather a mixture of Type 2 and Type 3"*) | Co₉S₈ · Co₃S₄ 가 전자 전도성 → 10–100 nm 두꺼운 계면상. 다만 Co 확산이 한정돼 SE 쪽 끝은 Co 황화물이 적어 아직 부동태 | 문헌 [39, 62] (Co 황화물 전도성) · [8] (두께) |
| LLTO–L₀.₅CO · LATP–L₀.₅CO | Type 1 (열역학적 안정) | 상호 반응 에너지 0 | 계산 (`Table 4`) |
| 그 밖의 산화물 SE–LCO | Type 1 (동역학) 또는 분해 뒤 Type 3 | 고전압 산물이 대체로 전자 절연. 단 Li 가 적거나 없어 (예 La₂Zr₂O₇) **Li 전도가 나쁠 수 있다** → 이 경우 문제는 안정성이 아니라 계면상의 이온 전도도 | 추론 (*"most of the equilibrium phases have low or zero Li content as a result of the delithiation"*) · LaCoO₃ 는 전자 전도성일 수 있음 [53] |
| 코팅층을 넣은 계면 | Type 2 → Type 3 로 바꾼 것 (*"artificial SEIs"*) | 코팅이 전자 절연 · 얇음 | 문헌 [54–60] |

**수로 줄 세운 것은 무엇인가** — `Table 4` 의 ΔE_D,min,mutual (계면 쌍별 · meV/atom) · `Table 6` 의 코팅 18 종 × 4 상대 (meV/atom) · `Fig. 1a` · `Fig. 5a` 의 창 (V). 전부 **반응의 구동력 또는 모재의 창**이지 산물의 물성이 아니다. 산물 목록 (`Table 4` · `Table 5` · `Table S2`–`S4`) 은 표로 주지만 그 위에 점수를 얹지 않는다 — `Table S4` 의 코팅–황화물 반응 산물 (TiS₂ · Li₅/₇NbS₂ · Li₄/₃Ta₂S₄) 에는 3 유형 분류조차 적용하지 않았다 (§18-2).

### 4.2 질문 2 — 다룬 계와 황화물의 숫자

**세어 보면**

| 묶음 | 내용 | 수 | 위치 |
|---|---|---|---|
| SE | LGPS · Li₃PS₄ (황화물 2) · LLZO · LLTO · LATP (산화물 3) · LiPON₀.₁₄ · LiPON₀.₄₆ (산질화물 2) — 저자 표현 *"five classes"* | 7 조성 | `Table 1` |
| 기준 이원 | Li₂S (창 · μ 창만) | 1 | `Table 2` · `Fig. 1` · `Fig. 2` |
| 양극 | LiCoO₂ (방전) · Li₀.₅CoO₂ (충전 대리 · 층상) — *"similar results are expected for other transition metal oxide cathodes"* (p. 3263 · 계산 없음) | 1 물질 2 상태 | `Table 1` |
| Li 금속 | 별도 계면 계산 없음 — grand potential 의 φ = 0 V 극한 | — | `Table 2` |
| 닫힌계 SE–양극 | 7 SE × 2 상태 | 14 쌍 | `Table 4` · `Table S2` · `Fig. 3` |
| 전위 아래 SE–LCO (2–5 V) | Li₃PS₄ · LLZO · LiPON₀.₁₄ (본문) + LGPS · LLTO · LATP · LiPON₀.₄₆ (SI) — 그림은 6 쌍 | 7 쌍 | `Table 5` · `Table S3` · `Fig. 4` |
| 코팅 후보 | Li–Ti–O 3 · Li–Nb–O 4 · Li–Si–O 4 · Li–Ta–O 4 · Li–P–O 3 (실증된 것 5: Li₄Ti₅O₁₂ · LiNbO₃ · Li₂SiO₃ · LiTaO₃ · Li₃PO₄) | 18 종 | `Fig. 5a` · `Table 6` |
| 코팅 × 상대 | 18 × {Li₃PS₄ · LLZO · LCO · L₀.₅CO} | 72 값 (산물은 5 코팅 × 2 SE 만) | `Table 6` · `Table S4` · `Fig. S1` |

**황화물 숫자 전부 (논문 값 · MP 2015 세대 hull · 0 K — 소환값이다)**

| 양 | Li₃PS₄ | LGPS (Li₁₀GeP₂S₁₂) | Li₂S (기준) | 위치 |
|---|---|---|---|---|
| hull 위 높이 | 0 (γ 상 Pmn2₁ 을 Li–P–S 상도에 추가) | 21 meV/atom (→ Li₃PS₄ + Li₄GeS₄) | — | `Table 1` |
| 환원 개시 · 산물 | 1.71 V · P, Li₂S | 1.71 V · P, Li₄GeS₄, Li₂S | 0 V 에서 안정 | `Table 2` |
| 산화 개시 · 산물 | 2.31 V · S, P₂S₅ | 2.15 V · Li₃PS₄, GeS₂, S (완전 탈리튬 2.31 V → GeS₂, P₂S₅, S) | 2.01 V · S | `Table 2` · `Fig. 1a` |
| 0 V (Li 금속) 산물 · ΔE | Li₃P, Li₂S · −1.42 eV/atom | Li₁₅Ge₄, Li₃P, Li₂S · −1.25 eV/atom (본문 문장은 −1.23) | 0 | `Table 2` |
| 5 V 산물 · ΔE | S, P₂S₅ · −1.01 eV/atom | GeS₂, P₂S₅, S · −1.12 eV/atom | S · −1.99 eV/atom | `Table 2` |
| μ_O 창의 위 끝 (O 흡수 개시) | −3.66 eV → Li₃PO₄, S | −3.66 eV → Li₄GeS₄, S, Li₃PO₄ | figure-read ≈ −3.08 eV | `Table 3` · `Fig. 2a` |
| LCO 의 O-poor 한계 (μ_O = −2.64 eV) 에서 | Li₃PO₄, S · −0.51 eV/atom | Li₃PO₄, S, GeS₂, Li₂SO₄ · −0.46 eV/atom | — | `Table 3` |
| L₀.₅CO 의 O-poor 한계 (μ_O = −0.73 eV) 에서 | LiPO₃, SO₃, Li₂SO₄ · −3.73 eV/atom | GeP₂O₇, SO₃, Li₂SO₄ · −3.68 eV/atom | — | `Table 3` |
| μ_S 창 | 0 … figure-read ≈ −0.57 eV (LGPS 와 같은 막대 높이) | 0 … −0.59 eV (*"S-poor limit of LGPS"*) | 0 … figure-read ≈ −4.00 eV | `Table 3` · `Fig. 2b` |
| μ_Co 창의 위 끝 | figure-read ≈ −0.60 eV | figure-read ≈ −0.60 eV | (그림에 없음) | `Fig. 2c` |
| 닫힌계 × LCO — x_m · 산물 · mutual / total | 0.41 · Co₉S₈, Li₂S, Li₂SO₄, Li₃PO₄ · **−405 / −405** meV/atom | 0.42 · Co₉S₈, Li₂S, Li₂SO₄, Li₃PO₄, Li₄GeO₄ · **−340 / −349** meV/atom | — | `Table 4` |
| 닫힌계 × L₀.₅CO | 0.39 · 같은 산물 · **−564 / −584** | 0.40 · 같은 산물 · **−499 / −527** | — | `Table 4` |
| 전위 아래 × LCO (2–5 V) mutual 범위 | [−737, −594] meV per non-Li atom | [−696, −519] meV per non-Li atom | — | `Table 5` · `Table S3` |
| 전위 아래 × LCO total @ 5 V | −1273 (본문 *"−1.27 eV per atom"*) | −1269 | — | `Table 5` · `Table S3` · `Fig. 4` |
| 코팅과의 mutual | `Table 6` 의 Li₃PS₄ 열 (0 ~ −177 meV/atom · §10) | 계산 없음 | — | `Table 6` |

- **Li₆PS₅Cl · Li₇P₃S₁₁** — 이 논문에 **없다**. SE 단독 창 · 0 V/5 V 산물은 2015 편 (`zhu2015_esw_grand_potential_origin` §3 · §7) 에 있고, 양극과의 pseudo-binary 는 `richards2016_interface_stability_pseudobinary` §8a · §19d 와 `xiao2019_cathode_coating_screening` 에 있다.
- ⚠ 닫힌계 값은 **원자당**, 전위 아래 값은 **비-Li 원자당** 이다 (§5.3). 같은 줄에 놓고 배수를 내면 안 된다.

### 4.3 질문 3 — 방법 (요약 · 식 전문은 §5)

- **상도**: pymatgen 으로 조성 상도 (convex hull) 와 grand potential 상도를 짓는다 (ref 30 = Ong 2008). 식 (1) ΔE_D = E_eq(C) − E(phase) = hull 위 높이의 음수.
- **grand potential · 전압**: 식 (2) 가 원소 M 을 열어 둔 분해 에너지, 식 (3) `μ_Li(φ) = μ⁰_Li − eφ` 가 전압을 Li 화학퍼텐셜로 옮긴다. 창 = 산화도 환원도 안 되는 φ 구간. 같은 식으로 O · S · Co 도 연다 (`Fig. 2` · `Table 3`).
- **pseudo-binary (닫힌계)**: 식 (5)–(7) — 원자당으로 정규화한 SE 와 전극 조성을 x : (1 − x) 로 섞은 조성의 hull 에너지에서 두 끝점 에너지의 선형 결합을 뺀다.
- **상호 반응 에너지의 정의 = 식 (8)**: `ΔE_D,mutual = ΔE_D(SE, electrode, x) − x·ΔE_D(SE) − (1 − x)·ΔE_D(electrode)` — 끝점이 hull 위에 떠 있는 몫 (SE · 전극 자신의 분해 에너지) 을 뺀 것. 식 (9) 가 x 에 대한 최솟값 (x = x_m), 식 (10) 이 그 x_m 에서의 total.
- **전압 적용 방식**: 식 (11)–(14) — pseudo-binary 조성을 Li 저장소 (전위 φ) 에 열어 두고 φ 를 **2 V 에서 5 V 까지 훑는다** (*"for Li-ion batteries"* · p. 3256). 전극 자신도 그 전위에서 탈리튬된다 (표에 L₀.₅CO · CoO₂ 가 상으로 나온다). ⚠ `richards2016…` 은 μ_Li 를 '양극 평균 전압' 한 점에 고정했다 — 여기는 구간 전체다.
- **정규화**: 닫힌계 = 원자당 / 전위 아래 = **비-Li 원자당** (*"because the number of Li changes with the phase equilibria at different applied voltages"* · p. 3256).
- **데이터 출처**: 대부분 **Materials Project** (ref 26) · MP 에 없는 물질만 자체 DFT (VASP · PAW · PBE · MP 와 같은 파라미터). 추가한 상: γ-Li₃PS₄ (Li–P–S) · Li₂PO₂N (Li–P–O–N).
- **보정**: *"The energy correction schemes for oxides, transition metal oxides, and gas molecules such as O₂, N₂, and F₂ were included in the MP"* (refs 16, 17). 황화물 음이온 보정은 문장에 없다.
- **0 K** — 엔트로피 무시 (p. 3265 자인).

### 4.4 질문 4 — 도펀트 · 조성 변화 분석이 있나

**한 호스트에 원소를 바꿔 넣은 계산은 없다.** 조성을 움직인 것은 넷이고, 넷 다 도펀트 스크린이 아니다.

| 무엇을 바꿨나 | 결과 | 성격 | 위치 |
|---|---|---|---|
| **LiPON 의 N 함량** (Li₂.₈₈PO₃.₇₃N₀.₁₄ ↔ Li₂.₉₈PO₃.₃N₀.₄₆) | LCO 와의 mutual −35 → −99 · L₀.₅CO 와 −65 → −154 meV/atom · 분해 에너지가 커지기 시작하는 전압 3.8 V → 2.8 V. *"The phase equilibria and decomposition energy are highly dependent on the LiPON composition."* | 같은 족 안의 음이온 비 2 점 (hull 혼합물로 넣은 조성 · 구조 없음) | §3.1 p. 3257 · §3.3 p. 3260 · `Table 4` · `Table S1` |
| **Ge 유무** (LGPS ↔ Li₃PS₄) | Li 쪽: LGPS 는 Li–Ge 합금 → Type 2 / Li₃PS₄ 는 Type 3. 양극 쪽: LGPS 가 조금 덜 반응 (−340 ↔ −405) · 산물에 Li₄GeO₄ 추가 | 두 물질의 대비 | `Table 2` · `Table 4` · p. 3264 |
| **코팅의 Li 함량** (족마다 3–4 조성 · 예 Li₈Nb₂O₉ · Li₃NbO₄ · LiNbO₃ · LiNb₃O₈) | Li 가 많을수록 환원 전위가 낮고, Li 가 적거나 O 가 많을수록 산화 전위가 높다. Li 가 많은 조성은 LLZO 와, 적은 조성은 황화물과 덜 반응 | 코팅 조성 계열 (SE 도펀트 아님) | §3.5 pp. 3262–3263 · `Fig. 5a` · `Table 6` |
| **설계 문장** (계산 없음) | *"Cations, such as Ti and Ge, in SEs would facilitate the formation of the Type 2 interfaces … the use of these cations should be avoided in the design of SE materials for Li metal compatibility. In contrast, anion mixing should be a viable strategy … LiPON is a successful case of using oxynitride … Similar successes have been demonstrated in the doping of Li₃PS₄ with halides, such as LiCl and LiI.⁶⁵,⁶⁶ Similarly, we expect some oxysulfide compounds as promising SEs."* | 원소 부류 수준의 규칙 — 양이온 (전자 전도 산물 → Type 2) ↔ 음이온 (절연 Li 이원상 → Type 3) | §4 p. 3264 |

- 설계 문장은 **Li 금속 쪽** 이야기다. 양극 쪽에 대해서는 SE 조성을 바꾸는 제안이 없고 코팅만 처방한다.
- 할라이드 도핑 · 옥시황화물은 계산하지 않았다 (ref 65 = Deiseroth 2008 아지로다이트 · ref 66 = Rangasamy 2015 Li₇P₂S₈I).

### 4.5 질문 5 — 분해 부피 변화

- **계산 0** — 몰부피 · ΔV · 변형률 · 응력 어느 것도 없다 (본문 · SI 전수 검색: `volume` 1 회 [권호 표기 제외] · `strain` 0 · `stress` 0).
- 유일한 문장 (p. 3264): *"Active electrochemical cycling of these interphase layers may facilitate the growth of the decomposition interphase layers and may lead to a repetitive volume change and the failure of the mechanical contact as a result of cyclic lithiation and delithiation.¹²"* — 혼합 전도 계면상이 전기화학적으로 사이클되면 부피가 되풀이해 변한다는 **정성 추론**이고 근거는 ref 12 (Han 2015 · LGPS) 다.
- 인접 서술 둘: 서론의 *"the mechanical failure of the contacts⁶"* (통상 원인 나열) · LiPON–LCO 의 기체 (N₂ · O₂) 방출과 in situ TEM 의 공극 [47] (p. 3261).
- ⇒ 갭 B (도펀트별 분해 부피) 에 대해 이 논문은 선행이 아니다.

### 4.6 질문 6 — 코팅층 선택 지침

**저자가 든 요건 (§3.5 · §4)**
1. **넓은 전기화학 창** — 환원 2 V 아래 ~ 산화 약 4 V (`Fig. 5a`). 산화 한계는 O₂ 방출이라 과전압이 크다 → 겉보기 한계는 평형값보다 높다고 본다 (Li–O₂ 전지의 Li₂O/Li₂O₂ 산화 유추 · ref 61).
2. **μ_Li 다리** — 코팅은 황화물 SE 와 LCO 사이의 큰 μ_Li 차이를 이어 양쪽과 Li 평형을 맞춘다 (평형 기준 1).
3. **양쪽과의 화학 반응이 작을 것** — LCO · L₀.₅CO 와 0 에 가깝고, 황화물과는 원래 계면 (≈ −500 meV/atom) 보다 훨씬 작다 (`Table 6`).
4. **얇을 것** — 수 nm (자발 계면상은 10–100 nm) → 저항이 준다.
5. **전자 절연 + Li 전도** — 인공 SEI. Type 3 인데 계면상의 Li 전도가 나쁜 경우 (LLZO–LCO 의 La₂Zr₂O₇) 에도 코팅이 답이다.
6. **상대에 맞춘 조성** — *"the coating layers that are the most stable with sulfide SEs may not necessarily be the most stable ones with LLZO"*. LLZO 에는 Li 가 많은 조성 (Li₄TiO₄ · Li₂TiO₃ · Li₈SiO₆ · Li₄SiO₄ · Li₅TaO₅ · Li₃TaO₄ · Li₈Nb₂O₉ · Li₃NbO₄), 황화물에는 기존 실증 조성 (Li₄Ti₅O₁₂ · LiTaO₃ · Li₂SiO₃).

**후보와 숫자** — §10 의 `Table 6` 전사 · `Fig. 5a` 창 (figure-read) 참조. 눈에 띄는 것 셋:
- **Li₃PO₄ 만 네 상대 모두와 0** (Li₃PS₄ · LLZO · LCO · L₀.₅CO).
- 표준 코팅 **LiNbO₃ 는 Li₃PS₄ 와 −155 meV/atom** — 18 종 중 셋째로 나쁘다 (Li₈SiO₆ −177 · LiNb₃O₈ −173 다음). 산물은 S · Li₂S · Li₃PO₄ · Li₅/₇NbS₂ (`Table S4`).
- 지침에 쓰인 물성은 **코팅 자신의 창과 반응 에너지**다. 코팅–SE 반응 산물의 물성은 평가하지 않는다.

### 4.7 질문 7 — 우리 작동창 (양극 쪽 2.5–4.25 V vs Li/Li⁺) 으로 읽으면

> 관례의 출처: CLAUDE.md §데이터 규율 (사용자 2026-11-09) · `kb/concepts/se_redox_frontier.md` 4 장 ④. 아래는 **이 논문의 숫자만** 으로 읽은 것이고, 우리 값은 맨 끝에 따로 적었다.

**(가) SE 단독 — 창 전체가 산화 구간이다.**
산화 개시가 Li₃PS₄ 2.31 V · LGPS 2.15 V · Li₂S 2.01 V 로 전부 2.5 V 아래다 (`Table 2`). 2.31 V 위로는 계단이 더 없어서 (산물 S + P₂S₅ [+ GeS₂] 고정) 구동력이 전위에 비례해 커진다.

| 물질 | 2.5 V | 4.25 V | 5 V (`Table 2`) |
|---|---|---|---|
| Li₃PS₄ | −0.07 | −0.73 | −1.01 |
| LGPS | −0.12 | −0.82 | −1.12 |
| Li₂S | −0.33 | −1.49 | −1.99 |

(eV/atom · 원 조성의 원자당. **2.5 V · 4.25 V 열은 우리 산술이다** — `Table 2` 의 계단 전압과 반응식의 Li 수로 낸 값이고 논문이 직접 준 수가 아니다: Li₃PS₄ → ½ P₂S₅ + 3/2 S + 3 Li 이므로 ΔE = −3(φ − 2.31)/8 · LGPS 는 2.15 V 에서 4 Li, 2.31 V 에서 6 Li 더 + hull 위 높이 0.021 · Li₂S 는 −2(φ − 2.01)/3. 같은 식이 5 V 표값 셋을 ±0.01 로 재현한다.)

**(나) LCO 와 맞닿은 계면 — 평형 산물 집합이 창 안에서 다섯 가지를 거친다 (Li₃PS₄).**

| 전위 구간 (V) | Li₃PS₄–LCO 평형 산물 (`Table 5`) | LGPS–LCO 평형 산물 (`Table S3`) |
|---|---|---|
| 2.50–2.91 (LGPS 는 2.50–2.62 / 2.62–2.90) | Co₃S₄ · Li₂SO₄ · **Li₃PO₄** | Co₃S₄ · Li₂SO₄ · **Li₃PO₄** · Li₂Ge₇O₁₅ → Co₉S₈ · Li₂SO₄ · **Li₃PO₄** · GeO₂ |
| 2.91–2.99 (LGPS 2.90–3.00) | Co₃S₄ · Li₂SO₄ · Li₄P₂O₇ | Co₉S₈ · Li₂SO₄ · LiCoPO₄ · GeO₂ |
| 2.99–3.20 (LGPS 3.00–3.14) | Co₃S₄ · Li₂SO₄ · LiCoPO₄ | Co₃S₄ · Li₂SO₄ · LiCoPO₄ · GeO₂ |
| 3.20–3.26 (LGPS 3.14–3.20 / 3.20–3.32) | Co₃S₄ · Li₂SO₄ · Co₃(PO₄)₂ | Co₃S₄ · Li₂SO₄ · Co₃(PO₄)₂ · GeO₂ → Co₃S₄ · CoSO₄ · Co₃(PO₄)₂ · GeO₂ |
| 3.26–4.25 (LGPS 3.32–4.25) | Co₃S₄ · CoSO₄ · Co₃(PO₄)₂ — **Li 를 담은 산물 없음** | Co₉S₈ · CoSO₄ · Co₃(PO₄)₂ · GeO₂ — **Li 를 담은 산물 없음** |

- **Li₃PO₄ 는 2.9 V 까지만 평형 산물이다.** 그 위로는 인산염이 Li 를 잃고 Co 인산염 (LiCoPO₄ → Co₃(PO₄)₂) 으로, 황산염도 3.26 V 위에서 CoSO₄ 로 간다. 충전 끝 (4.25 V) 의 평형 계면상에는 Li 가 한 원자도 없다 — 저자가 산화물 SE 에 대해 한 말 (*"most of the equilibrium phases have low or zero Li content as a result of the delithiation"* → 이온 전도가 나쁜 계면상) 이 황화물–LCO 에 더 강하게 해당한다 (저자는 황화물에 대해서는 이 점을 말하지 않는다 — 우리 읽기).
- **전자 전도성 Co 황화물 (Co₃S₄ / Co₉S₈) 은 2–5 V 전 구간에 있다** → 저자 분류로 Type 2 성분이 창 내내 남는다.
- **구동력** (meV per non-Li atom · `Fig. 4` figure-read ≈ · 표의 구간 범위와 일치): Li₃PS₄–LCO mutual −627 (2.5 V) → 최소 크기 −594 (≈ 3.0 V) → −735 (4.18 V 부터 평탄 · 4.25 V) / total −670 (2.5 V) → −1058 (4.25 V). LGPS–LCO mutual −546 → −696 / total −620 → −1058.
  mutual 은 창 안에서 1.2–1.3 배만 움직이고, total 의 증가분은 대부분 **SE 자신의 탈리튬** 이다 (저자 설명 그대로 · p. 3260).
- **Li₃PO₄ 가 평형상으로 남는 위 끝은 곁의 화학이 정한다** (전부 이 논문의 표 · 4.21 V 만 figure-read):

| 계 | Li₃PO₄ 가 평형상인 위 끝 (V) | 그 위에서 P 가 가는 곳 | 위치 |
|---|---|---|---|
| Li₃PO₄ 단독 | figure-read ≈ 4.21 | Li₄P₂O₇ (4.33 까지) → LiPO₃ | `Fig. 5a` |
| LiPON₀.₁₄ 단독 | 3.58 | Li₄P₂O₇ + LiNO₃ (N 이 산화되며 Li 를 가져감) | `Table S1` |
| LiPON₀.₁₄ + LCO | 4.16 | Li₄P₂O₇ → CoPO₄ | `Table 5` |
| LiPON₀.₄₆ 단독 | 2.60 | Li₄P₂O₇ | `Table S1` |
| LiPON₀.₄₆ + LCO | 3.57 | LiCoPO₄ → Co₃(PO₄)₂ | `Table S3` |
| LATP + LCO | 4.00 (4.22–4.53 V 에서 다시 나옴) | LATP 자신 (AlPO₄ · LiTi₂(PO₄)₃) | `Table S3` |
| **Li₃PS₄ + LCO** | **2.91** | Li₄P₂O₇ → LiCoPO₄ → Co₃(PO₄)₂ | `Table 5` |
| **LGPS + LCO** | **2.90** | LiCoPO₄ → Co₃(PO₄)₂ | `Table S3` |

  황화물이 곁에 있으면 Li₃PO₄ 가 사라지는 전압이 Li₃PO₄ 단독보다 1.3 V 낮다. 우리 읽기 (논문 서술 아님): Li₃PO₄ 가 Li₄P₂O₇ 로 응축하려면 Li 와 함께 O 를 내놓아야 한다 (2 Li₃PO₄ → Li₄P₂O₇ + 2 Li + ½ O₂). 단독일 때는 그 O 가 O₂ 로 나가야 해서 4.2 V 까지 버티고, 곁에 O 를 받아 줄 산화 가능한 종 (S → 황산염 · N → 질산염) 이 있으면 O₂ 방출 없이 낮은 전위에서 일어난다. N 이 많을수록 낮아지는 것 (LiPON₀.₁₄ → LiPON₀.₄₆) 도 같은 방향이다.

**(다) 코팅 — 2.5–4.25 V 를 자기 창으로 다 덮는 것은 18 종 중 둘뿐이다** (`Fig. 5a` figure-read ≈ · ±0.02 V).
- 덮는다: Li₄P₂O₇ (2.31–4.33 V) · LiPO₃ (2.48–5.00 V — 아래 끝은 판독 오차 ±0.02 V 안에서 2.5 V 와 같다).
- 위 끝이 0.04 V 모자란다: **Li₃PO₄ (0.69–4.21 V)**.
- 산화 한계가 4.25 V 아래: LiTa₃O₈ 4.04 · LiTaO₃ 3.95 · LiNb₃O₈ 3.92 · LiNbO₃ 3.87 · Li₂Si₂O₅ 3.79 · Li₂SiO₃ 3.74 · Li₄Ti₅O₁₂ · Li₂TiO₃ 3.71 · 나머지는 더 낮다 (§10 표).
- 저자는 이 산화가 O₂ 방출이라 과전압으로 버틴다고 본다 (열역학 안정이 아니라 동역학). 4.25 V 까지 '열역학적으로' 안정한 코팅은 이 논문 숫자로는 응축 인산염뿐이다.

**(라) 우리 값 (원장 · 따로 적는다 — 조성 · hull 세대가 달라 위 표와 한 줄에 놓지 않는다)**
- 우리 SE (comp1 · modelc) 의 grand-potential 산화 개시는 `litdb/our_dft_baseline.md` 에 있다 (Li-rich facet 규약 값 2.14 V · 다음 breakpoint 2.36 V · LiS₄ 등을 뺀 상 집합으로는 2.256 V · `HZ-esw-reduction-limit-facet-convention`). 2.5 V 아래라는 결론 — *"창 전체가 열역학적 산화 구간"* — 은 이 논문의 Li₃PS₄ · LGPS 와 같은 방향이다.
- 우리 O 단독 대조 조성에서 Li₃PO₄ 가 평형인 것은 창 맨 아래 2.50–2.70 V 뿐이고 그 위는 Li₄P₂O₇ → LiPO₃ → P₂O₅ 다 (kb 카드 4 장 ④ · `db/properties/cei_esw_Li_controls_2026_09_16.json`). 이 논문의 Li₃PS₄–LCO (Li₃PO₄ ≤ 2.91 V → Li₄P₂O₇ → Co 인산염) 와 **모양이 같다** — 계가 달라 (우리는 SE 자신의 O 만 · 양극 없음) 경계 전압을 맞대지는 않는다.
- 우리에게 **없는 것**: 전위를 건 pseudo-binary (식 11–14). 우리 계면 반응 계산은 닫힌계다 (cascade 축 ① 카드 5b: *"'전압 V 에서' — 리튬화 상태 대리이지 전압이 아니다"*).

---

## 5. 방법 — 식 전문 · 평형 기준 · 정규화 (§2 · pp. 3254–3256)

### 5.1 식 (1)–(14) 전사

```
(1)  ΔE_D(phase) = E_eq(C) − E(phase)                         # hull 위 높이의 음수
(2)  ΔE_D^open(phase, μ_M) = E_eq(C_eq(C, μ_M)) − E(phase) − Δn_M·μ_M
(3)  μ_Li(φ) = μ⁰_Li − eφ                                      # φ 는 Li 금속 기준
(4)  ΔE_D^open(phase, φ) = ΔE_D^open(phase, μ_Li(φ))
(5)  C_interface(C_SE, C_electrode, x) = x·C_SE + (1 − x)·C_electrode     # 조성은 원자 1 개로 정규화 · x = SE 의 분율 (0–1)
(6)  E_interface(SE, electrode, x) = x·E(SE) + (1 − x)·E(electrode)
(7)  ΔE_D(SE, electrode, x) = E_eq(C_interface(C_SE, C_electrode, x)) − E_interface(SE, electrode, x)
(8)  ΔE_D,mutual(SE, electrode, x) = ΔE_D(SE, electrode, x) − x·ΔE_D(SE) − (1 − x)·ΔE_D(electrode)
(9)  ΔE_D,min,mutual(SE, electrode) = min_{x∈(0,1)} [ΔE_D,mutual(SE, electrode, x)]        # 최소가 되는 x = x_m
(10) ΔE_D,min,total(SE, electrode) = ΔE_D(SE, electrode, x_m)
(11) ΔE_D^open(SE, electrode, x, φ) = E_eq(C_eq(C_interface(C_SE, C_electrode, x), μ_M)) − E_interface(SE, electrode, x) − Δn_Li·μ_Li(φ)
(12) ΔE_D,mutual^open(SE, electrode, x, φ) = ΔE_D^open(SE, electrode, x, φ) − x·ΔE_D^open(SE, φ) − (1 − x)·ΔE_D^open(electrode, φ)
(13) ΔE_D,min,mutual^open(SE, electrode, φ) = min_{x∈(0,1)} [ΔE_D,mutual^open(SE, electrode, x, φ)]
(14) ΔE_D,min,total^open(SE, electrode, φ) = ΔE_D^open(SE, electrode, x_m(φ), φ)            # mutual 이 0 이면 식 (9) 의 x_m 을 쓴다
```

- **mutual 과 total 의 차이** — total (식 7 · 11) 은 섞은 조성이 평형으로 내려가는 전체 에너지다. 끝점 (SE · 전극) 이 hull 위에 떠 있거나 (닫힌계) 그 전위에서 스스로 분해하면 (열린계) 그 몫이 들어 있다. mutual (식 8 · 12) 은 그 몫을 뺀 것 — *"the mutual reaction between SE and electrode materials excluding the decomposition energy ΔE_D of the SE and electrode"*.
- **x_m 은 mutual 의 최소에서 고른다** — 표에 적힌 산물은 그 x_m 에서의 평형상이다. 저자 단서 (p. 3255): *"the identified x_m corresponds to the most exothermic decomposition reactions, while the actual interphase layer may differ … and may have a distribution of elemental profile and material compositions across the interfaces"* → 전 구간 산물은 `Table S2`.
- 검산 (우리 산술): 식 (8) 로 `Table 4` 의 total 을 다시 내면 (total = mutual − x·E_hull(SE) − (1 − x)·E_hull(전극)) 12 행 중 10 행이 ±1 로 맞는다. 어긋나는 2 행은 LiPON–L₀.₅CO 이고 SI 값이 맞다 (§18-11).

### 5.2 평형 기준 넷 (§2.6 · p. 3256)

| 기준 | 내용 | 무엇을 재나 | 결과 절 |
|---|---|---|---|
| 1 | 중성 Li 와 인가 전위의 평형 — 접촉점에서 μ_Li 가 같아야 한다 (Li 이동이 빠르므로 쉽게 성립) | SE 의 전기화학 안정 (창) | §3.1 → 여기 §6 |
| 2 | Li 아닌 중성 원소 M 의 평형 — 접촉점에서 μ_M 이 같아야 한다 (Co · S 는 Li 만큼 못 움직인다) | 한 원소만 열었을 때의 화학 안정 | §3.2 → §7 |
| 3 | 맞닿은 두 물질의 **완전한** 열역학 평형 (모든 원소) | 계면의 화학 안정 (전위 없이 · 열처리 · 소결 때 중요) | §3.3 · §3.5 → §8 · §10 |
| 4 | 인가 전위 아래에서 두 물질의 평형 | 계면의 전기화학 안정 | §3.4 → §9 |

*"These equilibrium criteria must be satisfied for the interfaces to be thermodynamically stable."* 기준 1–2 는 원소 하나만 평형에 이른 물리 상황, 3–4 는 전부 평형에 이른 상황이다.

### 5.3 정규화 — 이 논문에서 가장 헷갈리는 곳

| 양 | 정규화 | 근거 |
|---|---|---|
| SE 단독 ΔE_D^open (`Table 2` · `Table 3` · `Fig. 1b` · `Fig. 5b`) | **원 조성의 원자 수** (eV/atom) | `Table 2` 캡션 *"normalized to the number of atoms in the original composition"* |
| 닫힌계 pseudo-binary (`Table 4` · `Table 6` · `Table S2` · `Table S4` · `Fig. 3` · `Fig. S1`) | **원자당** (조성을 원자 1 개로 정규화한 뒤 섞음 · meV/atom) | 식 (5) 설명 |
| 전위 아래 pseudo-binary (`Table 5` · `Table S3` · `Fig. 4`) | **비-Li 원자당** | §2.5 *"normalized to the number of non-Li atoms because the number of Li changes with the phase equilibria at different applied voltages"* |

- 표 머리와 본문은 셋 다 *"per atom"* 이라고만 쓴다. 차이는 §2.5 의 한 문장에만 있다.
- 크기 확인 (우리 산술): Li₃PS₄–LCO 닫힌계 −405 meV/atom 은 x_m = 0.41 에서 비-Li 원자 분율이 0.699 이므로 **≈ −580 meV per non-Li atom** 이다. `Table 5` 의 2.0 V 값 (두 끝점이 모두 안정한 전위) 이 −596 이라 서로 맞는다. LGPS 도 −340 → ≈ −495 ↔ 2.0 V 의 −519.
- 검산 하나 더 (우리 산술 · 표가 정말 비-Li 원자당인지): `Table 5` 의 2.91 V 경계에서 total − mutual = −737 − (−596) = **−141 meV**. 이 전위에서 LCO 는 아직 안정하므로 차이는 SE 자신의 탈리튬 몫뿐이다 — Li₃PS₄ 한 식당 −3 × (2.91 − 2.31) = −1.80 eV. 그 구간의 산물 (Co₃S₄ + Li₂SO₄ + Li₃PO₄) 이 정하는 섞음 비는 Li₃PS₄ : LiCoO₂ = 1 : 2.73 (x ≈ 0.42) 이고 그 혼합물의 비-Li 원자는 Li₃PS₄ 한 식당 13.2 개다 → −1.80 / 13.2 = **−137 meV** (비-Li 원자당 ✓). 전체 원자 (18.9 개) 로 나누면 −95 meV 라 안 맞는다.
- ⇒ *"닫힌계 −0.41 → 5 V −1.27 eV/atom"* 을 배수로 읽으면 (3.1 배) 정규화 차이 (×1.43) 와 SE 자신의 탈리튬 몫이 섞인다. 같은 잣대로는 **mutual −580 → −737 (1.3 배) · total −580 → −1273 (2.2 배)** 다 (§20-2).

---

## 6. 결과 I — SE 단독의 전기화학 창 (§3.1 · `Table 2` · 막대 · 곡선 그림)

2015 편의 복습에 해당한다 (*"the results are reviewed in Section 3.1"*). LiPON 만 조성이 바뀌었다.

### `Table 1` 전사 — 재료

| 약칭 | 조성 | 실험 σ_RT (mS/cm) | 구조 출처 | hull 위 (meV/atom) | 조성의 평형상 |
|---|---|---|---|---|---|
| LGPS | Li₁₀GeP₂S₁₂ | 12 | MP-696138 | 21 | Li₃PS₄, Li₄GeS₄ |
| LPS | Li₃PS₄ | 0.16 (나노다공 β-Li₃PS₄ · Liu 2013) | ref 18 (γ 상 Pmn2₁) | 0 | Li₃PS₄ |
| LLZO | Li₇La₃Zr₂O₁₂ (입방) | 0.5 | ref 20 | 7 | Li₂O, La₂O₃, Li₆Zr₂O₇ |
| LLTO | Li₀.₃₃La₀.₅₆TiO₃ | 1 | ref 22 | 68 | TiO₂, Li₄Ti₅O₁₂, La₂Ti₂O₇ |
| LATP | Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃ | 1 | ref 24 | 29 | LiTi₂(PO₄)₃, Li₃PO₄, AlPO₄ |
| LiPON₀.₁₄ | Li₂.₈₈PO₃.₇₃N₀.₁₄ | 2 × 10⁻³ | — (구조 없음) | 0 | Li₂PO₂N, Li₃PO₄, Li₂O |
| LiPON₀.₄₆ | Li₂.₉₈PO₃.₃N₀.₄₆ | 3.3 × 10⁻³ | — (구조 없음) | 0 | Li₂PO₂N, Li₃PO₄, Li₂O |
| LCO | LiCoO₂ | — | MP-24850 | 0 | LiCoO₂ |
| L₀.₅CO | Li₀.₅CoO₂ (층상) | — | MP-762036 | 33 | LiCo₂O₄ (스피넬) |

- LiPON 은 구조가 없는 **hull 혼합물** (hull 위 0) 로 넣었다 → 창과 반응 에너지가 조성의 평형상 세 개 (Li₂PO₂N · Li₃PO₄ · Li₂O) 의 것이다 (§18-5).
- 충전 양극은 가장 에너지가 낮은 **층상** L₀.₅CO 를 쓴다 (열역학적 안정상은 스피넬 LiCo₂O₄).

### `Table 2` 전사 — 창과 평형상 (ΔE: eV/atom · 원 조성 원자당)

| SE | 0 V (Li 금속) | 환원 개시 | 산화 개시 | 5 V |
|---|---|---|---|---|
| Li₂S | Li₂S (안정) · 0 | — | 2.01 V → S · 0 | S · −1.99 |
| LGPS | Li₁₅Ge₄, Li₃P, Li₂S · −1.25 | 1.71 V → P, Li₄GeS₄, Li₂S · −0.02 | 2.15 V → Li₃PS₄, GeS₂, S · −0.02 | GeS₂, P₂S₅, S · −1.12 |
| Li₃PS₄ | Li₃P, Li₂S · −1.42 | 1.71 V → P, Li₂S · 0 | 2.31 V → S, P₂S₅ · 0 | S, P₂S₅ · −1.01 |
| LiPON₀.₁₄ | Li₃P, Li₃N, Li₂O · −0.68 | 0.69 V → Li₃P, Li₂PO₂N, Li₂O · 0 | 1.07 V → Li₂PO₂N, Li₃PO₄, LiN₃ · 0 | N₂O₅, P₂O₅, O₂ · −0.31 |
| LiPON₀.₄₆ | Li₃P, Li₃N, Li₂O · −0.62 | 0.69 V → 같음 · 0 | 1.07 V → 같음 · 0 | NO₂, P₂O₅, N₂ · −0.66 |
| LLZO | Zr, La₂O₃, Li₂O · −0.02 | 0.05 V → Zr₃O, La₂O₃, Li₂O · −0.01 | 2.91 V → Li₂O₂, La₂O₃, Li₆Zr₂O₇ · −0.01 | O₂, La₂O₃, La₂Zr₂O₇ · −0.53 |
| LLTO | Ti₆O, La₂O₃, Li₂O · −0.34 | 1.75 V → Li₇Ti₁₁O₂₄, TiO₂, La₂Ti₂O₇ · −0.07 | 3.71 V → O₂, TiO₂, La₂Ti₂O₇ · −0.07 | O₂, TiO₂, La₂Ti₂O₇ · −0.15 |
| LATP | Ti₃P, TiAl, Li₃P, Li₂O · −1.56 | 2.16 V → P, LiTiPO₅, AlPO₄, Li₃PO₄ · −0.03 | 4.31 V → O₂, LiTi₂(PO₄)₃, Li₄P₂O₇, AlPO₄ · −0.03 | O₂, TiP₂O₇, Ti₅(PO₄)₄, AlPO₄ · −0.06 |

- 개시 전압에서의 −0.02 · −0.07 · −0.03 은 그 SE 의 **hull 위 높이** (21 · 68 · 29 meV/atom) 다 — 2015 편은 이것을 0 으로 놓는 규약을 썼고 이 편은 그대로 두고 mutual 에서 뺀다.
- 본문 서술 (p. 3257): 환원 전위는 CV 와 맞는다 (LGPS 1.71 V [12] · LLTO 1.75 ↔ 1.7 V · LATP 2.16 ↔ 2.4 V). LLZO 는 0.05 V · −0.02 eV/atom 으로 구동력이 가장 작아 *"may be kinetically stabilized against Li metal"*. 황화물은 *"oxidized at a similar potential of ∼2 to 2.5 V"* — Li₃PS₄ 실험 2.6 V [36]. 산화물의 산화는 전부 O₂ 방출 (과전압 큼). LiPON 은 1.07 V 부터 산화되지만 분해 에너지가 수십 meV/atom 에 머물다가 LiPON₀.₁₄ 3.8 V · LiPON₀.₄₆ 2.8 V 위에서 커진다 (`Fig. 1b`) · 고전압에서 N₂ · O₂ 방출 (실험의 기포 [25]).
- 결론 문장: *"the thermodynamic intrinsic electrochemical window of most SE materials is significantly narrower than that previously expected"*.

### `Table S1` 전사 — LiPON 두 조성의 전 계단 (SI)

φ 는 환원 쪽 행에서는 그 평형상 집합이 버티는 위 끝, 산화 쪽 행에서는 그 집합이 시작되는 전위다. Δn_Li 는 식당 Li 변화 (+ 흡수 · − 방출).

| φ (V) | LiPON₀.₁₄: Δn_Li · 평형상 | LiPON₀.₄₆: Δn_Li · 평형상 |
|---|---|---|
| 0.01 | +8 · Li₃N, Li₂O, Li₃P | +8 · 같음 |
| 0.61 | +7.72 · Li₇PN₄, Li₂O, Li₃P | +7.08 · 같음 |
| 0.68 | +7.44 · LiPN₂, Li₂O, Li₃P | +6.16 · 같음 |
| 0.69 | +6.88 · Li₂PO₂N, Li₂O, Li₃P | +4.32 · 같음 |
| (창) | 0 · Li₂.₈₈PO₃.₇₃N₀.₁₄ | 0 · Li₂.₉₈PO₃.₃N₀.₄₆ |
| 1.07 | −0.01 · Li₂PO₂N, LiN₃, Li₃PO₄ | −0.29 · 같음 |
| 1.67 | −0.01 · Li₂PO₂N, N₂, Li₃PO₄ | −0.33 · 같음 |
| 2.60 | −0.42 · N₂, Li₄P₂O₇, Li₃PO₄ | −0.98 · Li₂PO₂N, N₂, Li₄P₂O₇ |
| 2.63 | — | −1.09 · P₃N₅, N₂, Li₄P₂O₇ |
| 2.75 | — | −1.10 · P₄ON₆, N₂, Li₄P₂O₇ |
| 2.77 | — | −1.38 · LiPO₃, N₂, Li₄P₂O₇ |
| 3.58 | −0.80 · N₂, Li₄P₂O₇, LiNO₃ | — |
| 3.66 | −0.88 · N₂, Li₄P₂O₇, NO₂ | — |
| 3.71 | −0.98 · Li₄P₂O₇, LiPO₃, NO₂ | −1.98 · LiPO₃, NO₂, N₂ |
| 3.77 | −1.12 · Li₄P₂O₇, LiPO₃, LiNO₃ | — |
| 4.33 | −1.74 · LiPO₃, O₂, LiNO₃ | — |
| 4.38 | — | −2.98 · P₂O₅, NO₂, N₂ |
| 4.82 | −1.88 · LiPO₃, O₂, N₂O₅ | — |
| 4.99 | −2.88 · P₂O₅, O₂, N₂O₅ | — |

- LiPON₀.₁₄ 의 1.07 V '산화 개시' 는 식당 Li 0.01 개짜리다 — 2.60 V (−0.42) 부터가 실질적인 탈리튬이다 (§18-5).
- 인산염의 순서는 Li 가 빠지는 순서 그대로다: Li₃PO₄ → Li₄P₂O₇ → LiPO₃ → P₂O₅.

### `Fig. 1` (봄)

- **a** — SE 8 종의 창 막대 (가로축 φ 0–5 V · 윗축 μ_Li 0 ~ −5 eV). 초록 = 안정 창, 점선 = 완전 탈리튬까지의 최고 평형 전위. figure-read ≈ (V · ±0.01): Li₂S 0–2.00 / LGPS 1.71–2.14 (점선 2.31) / Li₃PS₄ 1.71–2.30 / LiPON₀.₁₄ 0.69–1.06 (점선 5.00) / LiPON₀.₄₆ 0.69–1.06 (점선 4.38) / LLZO 0.05–2.91 (점선 3.30) / LLTO 1.75–3.71 / LATP 2.16–4.30 (점선 4.66). 표와 전부 맞는다.
- **b** — 분해 에너지 vs φ 곡선 8 개. 창 안에서 0, 밖에서 꺾인 직선으로 내려간다. 양 끝 figure-read 는 `Table 2` 와 ±0.02 로 맞는다. ⚠ 세로축 표기가 *"(meV/atom)"* 인데 눈금은 0 ~ −2.0 이고 값은 표의 **eV/atom** 과 같다 — 단위 오기 (§18-11).

---

## 7. 결과 II — Li 아닌 원소의 화학퍼텐셜 창 (§3.2 · `Fig. 2` · `Table 3`)

기준 2 — O · S · Co 를 하나씩 열어 SE 와 LCO 의 안정 창이 겹치는지 본다.

### `Fig. 2` (봄) — 막대 끝 figure-read ≈ (eV · 원소 기준 상태 대비 · ±0.02)

| 물질 | μ_O 창 (a) | μ_S 창 (b) | μ_Co 창 (c) |
|---|---|---|---|
| LCO | −0.38 … −2.64 | −2.06 아래 | 0 … −3.04 |
| L₀.₅CO | 0 … −0.73 | −6.69 아래 | −2.33 … −3.71 |
| LLZO | −0.40 … −6.11 | — | 전 구간 (0 … 축 끝 −4) |
| LLTO · LATP | 0 … −3.90 | — | 전 구간 |
| Li₂S | −3.08 아래 (축 끝 −7 까지) | 0 … −4.00 | — |
| LGPS · Li₃PS₄ | −3.67 아래 | 0 … −0.57 | −0.60 아래 |
| LiPON₀.₁₄ · LiPON₀.₄₆ | −4.09 … −4.83 | — | 전 구간 |

(`Table 3` 이 준 값 7 개 — −2.64 · −0.73 · −3.66 · −4.08 · −0.59 · −2.06 · −6.69 — 와 ±0.02 로 맞는다.)

- **O**: 산화물 SE 의 창은 LCO · L₀.₅CO 와 겹친다. 황화물은 **겹치지 않는다** — LCO 의 아래 끝 (−2.64) 과 황화물의 위 끝 (−3.66) 사이가 1.0 eV, L₀.₅CO (−0.73) 와는 2.9 eV 떨어져 있다. LiPON 도 틈이 있지만 (−2.64 ↔ −4.08) 분해 에너지가 훨씬 작다.
- **S**: 황화물의 창 (0 … −0.59) 과 LCO (−2.06 아래) · L₀.₅CO (−6.69 아래) 도 안 겹친다.
- **Co**: 모든 SE 와 겹친다 → *"the incompatibility between sulfide SEs and LCO mostly originates from the discrepancy of O and S anion chemistries rather than that of Co."* EDX 가 본 Co 의 '상호 확산' [8] 은 Co 황화물 계면상의 형성으로 다시 읽는다.

### `Table 3` 전사 — 상대의 화학퍼텐셜에서의 평형상 (ΔE: eV/atom)

| 물질 | 열린 원소 · 값 | 그 값의 뜻 | 평형상 | ΔE |
|---|---|---|---|---|
| LGPS | μ_O = −0.73 | L₀.₅CO 의 O-poor 한계 | GeP₂O₇, SO₃, Li₂SO₄ | −3.68 |
| | μ_O = −2.64 | LCO 의 O-poor 한계 | Li₃PO₄, S, GeS₂, Li₂SO₄ | −0.46 |
| | μ_O = −3.66 | 산화 개시 | Li₄GeS₄, S, Li₃PO₄ | −0.02 |
| Li₃PS₄ | μ_O = −0.73 | L₀.₅CO 의 O-poor 한계 | LiPO₃, SO₃, Li₂SO₄ | −3.73 |
| | μ_O = −2.64 | LCO 의 O-poor 한계 | Li₃PO₄, S | −0.51 |
| | μ_O = −3.66 | 산화 개시 | Li₃PO₄, S | 0 |
| LiPON₀.₁₄ | μ_O = −0.73 / −2.64 / −4.08 | 같은 순서 (−4.08 = 산화 개시) | LiNO₃, Li₃PO₄, Li₄P₂O₇ / N₂, Li₃PO₄, Li₄P₂O₇ / Li₂PO₂N, Li₃PO₄, LiN₃ | −0.09 / −0.02 / 0 |
| LiPON₀.₄₆ | μ_O = −0.73 / −2.64 / −4.08 | 같은 순서 | 같은 상 | −0.36 / −0.11 / 0 |
| LCO | μ_S = −0.59 | LGPS 의 S-poor 한계 | Co₉S₈, Li₂SO₄ | −0.28 |
| | μ_S = −2.06 | LCO 분해 개시 | CoO, Li₆CoO₄, Li₂SO₄ | 0 |
| L₀.₅CO | μ_S = −0.59 | LGPS 의 S-poor 한계 | Co₉S₈, CoSO₄, Li₂SO₄ | −0.39 |
| | μ_S = −6.69 | L₀.₅CO 분해 개시 | Li₂SO₄, Co₃O₄, LiCoO₂ | −0.03 |

읽기: **양극의 높은 μ_O 가 황화물을 산화해 Li₃PO₄ · Li₂SO₄ 를 만들고** (Li₃PS₄ 는 O 를 받으면 먼저 Li₃PO₄ + S⁰), **황화물의 높은 μ_S 가 LCO 를 환원해 Co 황화물을 만든다.** 충전 상태 (L₀.₅CO) 의 μ_O 에서는 구동력이 −3.7 eV/atom 까지 간다 (SO₃ 까지).

---

## 8. 결과 III — SE–LCO 닫힌계 화학 반응 (§3.3 · `Fig. 3` · `Table 4` · `Table S2`)

기준 3 — 전위 없이 두 물질을 섞었을 때. 열처리 · 소결에 해당한다.

### `Table 4` 전사 (meV/atom)

| SE | 전극 | x_m | x_m 에서의 평형상 | mutual | total |
|---|---|---|---|---|---|
| LGPS | LCO | 0.42 | Co₉S₈, Li₂S, Li₂SO₄, Li₃PO₄, Li₄GeO₄ | −340 | −349 |
| | L₀.₅CO | 0.40 | 같음 | −499 | −527 |
| Li₃PS₄ | LCO | 0.41 | Co₉S₈, Li₂S, Li₂SO₄, Li₃PO₄ | −405 | −405 |
| | L₀.₅CO | 0.39 | 같음 | −564 | −584 |
| LiPON₀.₁₄ | LCO | 0.93 | CoN, Li₃PO₄, Li₆CoO₄, N₂ | −35 | −35 |
| | L₀.₅CO | 0.59 | Co₃O₄, LCO, LiNO₃, Li₃PO₄ | −65 | −65 (SI: −79) |
| LiPON₀.₄₆ | LCO | 0.81 | CoN, Li₂O, Li₃PO₄ | −99 | −99 |
| | L₀.₅CO | 0.62 | CoO, LCO, Li₃PO₄, N₂ | −154 | −154 (SI: −167) |
| LLZO | LCO | 0.96 | La₂O₃, Li₆Zr₂O₇, Li₅CoO₄ | −1 | −8 |
| | L₀.₅CO | 0.47 | La₂O₃, La₂Zr₂O₇, Li₇Co₅O₁₂, O₂ | −39 | −60 |
| LLTO | LCO | 0.64 | Co₃O₄, La₂Ti₂O₇, Li₂TiO₃, L₀.₅CO | −0.5 | −44 |
| | L₀.₅CO | — | LLTO, L₀.₅CO (안정) | 0 | — |
| LATP | LCO | 0.32 | L₀.₅CO, Co₃O₄, Li₃PO₄, LiAl₅O₈, TiO₂ | −53 | −63 |
| | L₀.₅CO | — | LATP, L₀.₅CO (안정) | 0 | — |

본문 서술 (pp. 3259–3260)
- 황화물–LCO: 산물에 **Co₉S₈ · Li₂SO₄ · Li₃PO₄** — Co 가 3+ → 2+ 로 환원된다. *"The cobalt sulfide phases with lower valences are known to be electronically conductive,³⁹ which are detrimental to the stability of the interfaces."* 충전 상태 (L₀.₅CO) 에서 구동력이 더 크다 (−405 → −564 · −340 → −499).
- 산화물 SE–LCO: 0 ~ 수십 meV/atom. LLTO · LATP 는 L₀.₅CO 와 열역학적으로 안정. LATP–LCO 의 Co₃O₄ 는 실험 [42] 과 일치. 산화물 쪽에서는 Co 가 3+ → 4+ 로 **반대 방향** 이다 (Li₇Co₅O₁₂ · L₀.₅CO) — 황화물과 산화물의 계면 분해는 성격이 다르다. Li₃PO₄ · LiAl₅O₈ 는 계면을 부동태화하고 Li 를 통할 수 있다 [43].
- LiPON: N 함량에 크게 의존 (§4.4). 실험에서 LCO 와 잘 맞는 것 [45–48] 은 주 산물 **Li₃PO₄** (잘 알려진 코팅재 [49–51]) 덕으로 본다.

### `Fig. 3` (봄)

가로축 x (SE 의 분율 0–1 · 축 제목 *"Molar fraction of SE in pesudo-binary x"*) · 세로축 mutual 반응 에너지 (0 ~ −600 meV/atom). 실선 = LCO, 점선 = L₀.₅CO, 7 색. 황화물 네 곡선만 깊고 (최저 −340 · −405 · −499 · −564), LiPON₀.₄₆ 이 −99 / −154, 나머지는 −65 위쪽에 몰려 있다. 최솟값 위치 · 크기는 `Table 4` 와 맞는다. Li₃PS₄–LCO 실선은 x = 0.41–0.48 에서 바닥이 평평하다.

### `Table S2` 전사 — x 에 따른 평형상 (황화물 전량 · mutual / total meV/atom)

**LGPS–LCO**

| x | 평형상 | mutual / total |
|---|---|---|
| 0.06 | CoO, Li₃PO₄, Li₂SO₄, Li₄GeO₄, Li₆CoO₄ | −82 / −83 |
| 0.159 | Co, Li₃PO₄, Li₂SO₄, Li₄GeO₄, Li₆CoO₄ | −210 / −213 |
| 0.163 | Co, Li₂O, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | −213 / −216 |
| 0.35 | Co₉S₈, Li₂O, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | −314 / −321 |
| **0.42** | Co₉S₈, Li₂S, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | **−340 / −349** |
| 0.44 | Co₉S₈, Li₂S, Li₂GeO₃, Li₃PO₄, Li₂SO₄ | −339 / −348 |
| 0.52 | Co₉S₈, Li₂S, Li₃PO₄, Li₂SO₄, Li₄GeS₄ | −329 / −339 |
| 0.59 | Co₃S₄, Li₂S, Li₃PO₄, Li₂SO₄, Li₄GeS₄ | −319 / −331 |
| 0.61 | CoS₂, Co₃S₄, Li₂S, Li₃PO₄, Li₄GeS₄ | −313 / −325 |

**LGPS–L₀.₅CO**

| x | 평형상 | mutual / total |
|---|---|---|
| 0.0510 | Co₃O₄, LCO, Li₂GeO₃, Li₃PO₄, Li₂SO₄ | −230 / −262 |
| 0.0513 | Co₃O₄, LCO, Li₂CoGeO₄, Li₃PO₄, Li₂SO₄ | −231 / −263 |
| 0.088 | CoO, LCO, Li₂CoGeO₄, Li₃PO₄, Li₂SO₄ | −314 / −346 |
| 0.090 | CoO, LCO, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | −317 / −349 |
| 0.10 | CoO, Li₃PO₄, Li₂SO₄, Li₄GeO₄, Li₆CoO₄ | −328 / −360 |
| 0.13 | Co, CoO, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | −360 / −391 |
| 0.14 | Co, CoO, Li₂CoGeO₄, Li₃PO₄, Li₂SO₄ | −370 / −401 |
| 0.31 | Co, Co₉S₈, Li₂CoGeO₄, Li₃PO₄, Li₂SO₄ | −467 / −496 |
| 0.37 | Co, Co₉S₈, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | −492 / −520 |
| 0.397 | Co₉S₈, Li₂O, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | −498 / −526 |
| **0.404** | Co₉S₈, Li₂S, Li₃PO₄, Li₂SO₄, Li₄GeO₄ | **−499 / −527** |
| 0.43 | Co₉S₈, Li₂S, Li₂GeO₃, Li₃PO₄, Li₂SO₄ | −492 / −519 |
| 0.50 | Co₉S₈, Li₂S, Li₃PO₄, Li₂SO₄, Li₄GeS₄ | −462 / −489 |
| 0.59 | Co₃S₄, Li₂S, Li₃PO₄, Li₂SO₄, Li₄GeS₄ | −428 / −453 |
| 0.64 | CoS₂, Co₃S₄, Li₂S, Li₃PO₄, Li₄GeS₄ | −398 / −423 |

**Li₃PS₄–LCO**

| x | 평형상 | mutual / total |
|---|---|---|
| 0.06 | CoO, Li₃PO₄, Li₂SO₄, Li₆CoO₄ | −90 / −90 |
| 0.15 | Co, Li₃PO₄, Li₂SO₄, Li₆CoO₄ | −233 / −233 |
| 0.16 | Co, Li₂O, Li₃PO₄, Li₂SO₄ | −237 / −237 |
| 0.34 | Co₉S₈, Li₂O, Li₃PO₄, Li₂SO₄ | −368 / −368 |
| **0.41** | Co₉S₈, Li₂S, Li₃PO₄, Li₂SO₄ | **−405 / −405** |
| 0.48 | Co₃S₄, Li₂S, Li₃PO₄, Li₂SO₄ | −405 / −405 |
| 0.50 | CoS₂, Co₃S₄, Li₂S, Li₃PO₄ | −401 / −401 |

**Li₃PS₄–L₀.₅CO**

| x | 평형상 | mutual / total |
|---|---|---|
| 0.05 | Co₃O₄, LCO, Li₃PO₄, Li₂SO₄ | −238 / −269 |
| 0.09 | CoO, LCO, Li₃PO₄, Li₂SO₄ | −331 / −361 |
| 0.10 | CoO, Li₃PO₄, Li₂SO₄, Li₆CoO₄ | −344 / −374 |
| 0.12 | Co, CoO, Li₃PO₄, Li₂SO₄ | −380 / −409 |
| 0.36 | Co, Co₉S₈, Li₃PO₄, Li₂SO₄ | −552 / −573 |
| 0.387 | Co₉S₈, Li₂O, Li₃PO₄, Li₂SO₄ | −562 / −582 |
| **0.394** | Co₉S₈, Li₂S, Li₃PO₄, Li₂SO₄ | **−564 / −584** |
| 0.47 | Co₃S₄, Li₂S, Li₃PO₄, Li₂SO₄ | −543 / −560 |
| 0.53 | CoS₂, Co₃S₄, Li₂S, Li₃PO₄ | −518 / −534 |

이 표에서 읽히는 것 (digest 정리)
1. **Li₃PO₄ 는 모든 x 에서 산물이다** — 양극이 많은 쪽 끝부터 SE 가 많은 쪽 끝까지. Li₂SO₄ 는 SE 가 가장 많은 꼭짓점 (CoS₂ 가 나오는 x ≥ 0.5) 에서만 빠진다.
2. **Co 의 행방이 x 에 따라 넷으로 바뀐다** — 양극 쪽부터 CoO / Co₃O₄ → **금속 Co** → Co₉S₈ → Co₃S₄ → CoS₂. 금속 Co 가 평형상인 구간이 있다 (LCO 와는 x ≈ 0.15–0.16 · L₀.₅CO 와는 x ≈ 0.12–0.37). 저자는 Co 황화물의 전자 전도성만 말하고 금속 Co 는 언급하지 않는다 (§18-2).
3. **최솟값이 뾰족하지 않다** — Li₃PS₄–LCO 는 x = 0.41 (Co₉S₈) 과 0.48 (Co₃S₄) 이 똑같이 −405 다. '가장 발열적인 산물 집합' 이 하나로 정해지지 않는 사례 (§16-4).
4. 저자가 Discussion 에서 말하는 *"variation of the interphase composition across the interface"* (ESI) 가 이 표다.

**`Table S2` c–g 요약 (LiPON · 산화물)**

| 쌍 | x 에 따른 평형상의 흐름 | mutual 범위 |
|---|---|---|
| LiPON₀.₁₄–LCO | x 0.93–0.98: CoN / Co₂N / Co + Li₃PO₄ (+ Li₅CoO₄ · Li₆CoO₄ · Li₂O · LiN₃ · Li₂PO₂N) | −35 ~ −11 |
| LiPON₀.₁₄–L₀.₅CO | x 0.59: Co₃O₄, LCO, LiNO₃, Li₃PO₄ → 0.80–0.90: N₂ + Co 산화물 → 0.94–0.99: CoN · Co₂N · Co + Li₃PO₄ (+ LiCoPO₄ · Li₄P₂O₇ · Li₂PO₂N) | −65 ~ −7 |
| LiPON₀.₄₆–LCO | x 0.77–0.83: CoN / Co₂N / Co + Li₃PO₄ + Li₂O (· Li₅CoO₄ · Li₆CoO₄ · LiN₃) | −99 ~ −91 |
| LiPON₀.₄₆–L₀.₅CO | x 0.30: Co₃O₄, LCO, LiNO₃, Li₃PO₄ → 0.52–0.77: N₂ + Co 산화물/질화물 + LCO → 0.84–0.86: CoN · Co₂N · Co + Li₂O | −154 ~ −117 |
| LLZO–LCO | x 0.96: La₂O₃, Li₆Zr₂O₇, Li₅CoO₄ | −1 |
| LLZO–L₀.₅CO | x 0.47: O₂, La₂Zr₂O₇, La₂O₃, Li₇Co₅O₁₂ → 0.49: Li₂O₂ → 0.87–0.98: Li₆Zr₂O₇ · Li₈CoO₆ · Li₅CoO₄ | −39 ~ −3 |
| LLTO–LCO | x 0.64: Co₃O₄, La₂Ti₂O₇, Li₂TiO₃, L₀.₅CO / 0.98: … Li₄Ti₅O₁₂ | −0.5 · −0.04 |
| LATP–LCO | x 0.25–0.52: Co₃O₄ + Li₃PO₄ + L₀.₅CO + {LiAl₅O₈ · AlPO₄} + {Li₂TiO₃ · Li₄Ti₅O₁₂ · TiO₂ · LiTiPO₅} | −53 ~ −41 |
| LLTO–L₀.₅CO · LATP–L₀.₅CO | 반응 없음 | 0 |

---

## 9. 결과 IV — 전위 아래의 SE–LCO 계면 (§3.4 · `Fig. 4` · `Table 5` · `Table S3`)

기준 4 — pseudo-binary 를 φ = 2–5 V 의 Li 저장소에 열어 둔다. 값은 **비-Li 원자당** · 표의 [a, b] 는 그 전위 구간 안의 범위다 (어느 끝이 어느 전압인지는 표가 말하지 않는다 → `Fig. 4`).

### `Table 5` 전사 (본문 · meV per non-Li atom)

| 계면 | φ (V) | x_m(φ) 에서의 평형상 | mutual | total |
|---|---|---|---|---|
| **Li₃PS₄–LCO** | 2.00–2.91 | Co₃S₄, Li₂SO₄, Li₃PO₄ | [−641, −596] | [−737, −596] |
| | 2.91–2.99 | Co₃S₄, Li₂SO₄, Li₄P₂O₇ | [−596, −594] | [−750, −737] |
| | 2.99–3.20 | Co₃S₄, Li₂SO₄, LiCoPO₄ | [−607, −594] | [−779, −730] |
| | 3.20–3.26 | Co₃S₄, Li₂SO₄, Co₃(PO₄)₂ | [−613, −608] | [−785, −773] |
| | 3.26–5.00 | Co₃S₄, CoSO₄, Co₃(PO₄)₂ | [−737, −616] | [−1273, −763] |
| LLZO–LCO | 2.00–2.57 | La₂O₃, Li₆Zr₂O₇, Li₅CoO₄ | [−2, −2] | [−9, −9] |
| | 2.57–2.81 | La₂O₃, Li₆Zr₂O₇, Li₇Co₅O₁₂ | [−7, −2] | [−13, −8] |
| | 2.81–3.50 | La₂O₃, La₂Zr₂O₇, Li₇Co₅O₁₂ | [−33, −2] | [−72, −11] |
| | 3.50–3.99 | La₂O₃, La₂Zr₂O₇, O₂, L₀.₅CO | 0 | [−137, −53] |
| | 3.99–5.00 | LaCoO₃, La₂Zr₂O₇, O₂ | [−5, 0] | [−656, −284] |
| LiPON₀.₁₄–LCO | 2.00–2.12 | CoN, N₂, Li₃PO₄ | [−53, −53] | [−55, −55] |
| | 2.12–2.70 | CoO, N₂, Li₃PO₄ | [−64, −53] | [−70, −55] |
| | 2.70–3.01 | Co₃O₄, N₂, Li₃PO₄ | [−59, −53] | [−84, −70] |
| | 3.01–3.89 | Co₃O₄, LiNO₃, Li₃PO₄ | [−67, −35] | [−139, −77] |
| | 3.89–4.16 | LiCoPO₄, LiNO₃, Li₃PO₄ | [−33, −11] | [−190, −165] |
| | 4.16–4.18 | LiCoPO₄, LiNO₃, Li₄P₂O₇ | [−9, −9] | [−221, −221] |
| | 4.19–4.23 | CoPO₄, LiNO₃, Li₄P₂O₇ | [−9, −8] | [−221, −215] |
| | 4.23–4.54 | CoPO₄, LiNO₃, O₂ | [−53, −9] | [−288, −169] |
| | 4.54–5.00 | CoPO₄, Co(NO₃)₄, O₂ | [−116, −56] | [−482, −294] |

### `Table S3` 전사 (SI)

| 계면 | φ (V) | 평형상 | mutual | total |
|---|---|---|---|---|
| **LGPS–LCO** | 2.00–2.14 | Co₉S₈, Li₂SO₄, Li₃PO₄, Li₂GeO₃ | [−540, −519] | [−546, −525] |
| | 2.14–2.45 | Co₃S₄, Li₂SO₄, Li₃PO₄, Li₂GeO₃ | [−556, −543] | [−604, −551] |
| | 2.45–2.62 | Co₃S₄, Li₂SO₄, Li₃PO₄, Li₂Ge₇O₁₅ | [−547, −542] | [−645, −611] |
| | 2.62–2.90 | Co₉S₈, Li₂SO₄, Li₃PO₄, GeO₂ | [−542, −536] | [−683, −632] |
| | 2.90–3.00 | Co₉S₈, Li₂SO₄, LiCoPO₄, GeO₂ | [−541, −536] | [−696, −675] |
| | 3.00–3.14 | Co₃S₄, Li₂SO₄, LiCoPO₄, GeO₂ | [−551, −542] | [−764, −728] |
| | 3.14–3.20 | Co₃S₄, Li₂SO₄, Co₃(PO₄)₂, GeO₂ | [−557, −552] | [−773, −759] |
| | 3.20–3.32 | Co₃S₄, CoSO₄, Co₃(PO₄)₂, GeO₂ | [−583, −559] | [−787, −744] |
| | 3.32–5.00 | Co₉S₈, CoSO₄, Co₃(PO₄)₂, GeO₂ | [−696, −588] | [−1269, −767] |
| LLTO–LCO | 2.00–2.58 | Li₂TiO₃, La₂TiO₅, CoO | [−73, −21] | [−130, −71] |
| | 2.58–2.63 | Li₂TiO₃, La₂TiO₅, Co₃O₄ | [−19, −18] | [−63, −62] |
| | 2.63–3.34 | Li₂TiO₃, La₂Ti₂O₇, Co₃O₄ | [−17, −1] | [−71, −54] |
| | 3.34–3.71 | LLTO, L₀.₅CO | 0 | [−152, −68] |
| | 3.71–4.10 | La₂Ti₂O₇, TiO₂, O₂, L₀.₅CO | 0 | [−68, −9] |
| | 4.10–5.00 | La₂Ti₂O₇, TiO₂, O₂, CoO₂ | 0 | [−113, −9] |
| LATP–LCO | 2.00–2.27 | Li₃PO₄, LiAlO₂, Li₂TiO₃, Co | [−282, −223] | [−326, −242] |
| | 2.27–2.37 | Li₃PO₄, Al₂CoO₄, Li₂Ti₃CoO₈, Co | [−213, −193] | [−233, −213] |
| | 2.37–2.53 | Li₃PO₄, Al₂CoO₄, Li₂Ti₃CoO₈, CoO | [−189, −168] | [−205, −184] |
| | 2.53–2.88 | Li₃PO₄, Al₂CoO₄, TiCoO₃, CoO | [−165, −121] | [−182, −138] |
| | 2.88–3.14 | Li₃PO₄, Al₂CoO₄, Ti₂CoO₄, Co₃O₄ | [−118, −101] | [−133, −116] |
| | 3.14–3.40 | Li₃PO₄, Al₂CoO₄, TiO₂, Co₃O₄ | [−99, −81] | [−116, −101] |
| | 3.40–3.59 | Li₃PO₄, LiAl₅O₈, TiO₂, Co₃O₄ | [−78, −54] | [−109, −85] |
| | 3.59–3.94 | Li₃PO₄, AlPO₄, TiO₂, Co₃O₄ | [−51, −8] | [−82, −38] |
| | 3.94–4.00 | Li₃PO₄, AlPO₄, LiTiPO₅, Co₃O₄ | [−5, −2] | [−35, −32] |
| | 4.00–4.10 | LATP, L₀.₅CO | 0 | [−32, −32] |
| | 4.10–4.22 | LATP, CoO₂ | 0 | [−47, −32] |
| | 4.22–4.53 | Li₃PO₄, AlPO₄, LiTi₂(PO₄)₃, O₂ | [−2, 0] | [−38, −30] |
| | 4.53–5.00 | LATP, L₀.₅CO | 0 | [−113, 52] (표 그대로 · §18-11) |
| LiPON₀.₄₆–LCO | 2.00–2.33 | N₂, CoN, Li₃PO₄ | [−124, −124] | [−191, −173] |
| | 2.33–2.87 | N₂, CoO, Li₃PO₄ | [−137, −118] | [−233, −182] |
| | 2.87–3.20 | N₂, Co₃O₄, Li₃PO₄ | [−116, −103] | [−260, −220] |
| | 3.20–3.43 | LiNO₃, Co₃O₄, Li₃PO₄ | [−114, −103] | [−245, −193] |
| | 3.43–3.57 | LiNO₃, LiCoPO₄, Li₃PO₄ | [−123, −112] | [−359, −327] |
| | 3.57–3.72 | LiNO₃, LiCoPO₄, Co₃O₄ | [−137, −126] | [−392, −359] |
| | 3.72–4.18 | LiNO₃, LiCoPO₄, Co₃(PO₄)₂ | [−145, −137] | [−523, −404] |
| | 4.18–4.23 | LiNO₃, CoPO₄, Co₃(PO₄)₂ | [−148, −146] | [−540, −529] |
| | 4.23–4.48 | LiNO₃, CoPO₄, Co(NO₃)₂ | [−160, −149] | [−639, −548] |
| | 4.48–4.54 | LiNO₃, CoPO₄, Co(NO₃)₄ | [−154, −153] | [−663, −647] |
| | 4.54–4.60 | LiCo(PO₃)₄, CoPO₄, Co(NO₃)₄ | [−152, −152] | [−715, −697] |
| | 4.60–5.00 | Co(PO₃)₃, CoPO₄, Co(NO₃)₄ | [−152, −152] | [−918, −739] |

본문 서술 (pp. 3260–3261)
- Li₃PS₄–LCO 는 **2–5 V 전 구간에서 불안정** — mutual [−737, −594]. total 은 5 V 에서 LGPS · Li₃PS₄ 모두 −1.27 eV. *"The growing differences between ΔE^open_D,min,mutual and ΔE^open_D,min,total at higher voltages are mainly due to the increasing contribution from the delithiation of the SEs to the total decomposition energy"*.
- 산화물 SE–LCO 는 전 구간에서 훨씬 낫다. LLZO–LCO 는 mutual 최대 −33. 4 V 위 산물 La₂Zr₂O₇ · LaCoO₃ 는 Li 전도가 나쁠 것이고 LaCoO₃ 는 전자 전도성일 수 있다 [53] (LaCoO₃ 는 1000 °C 넘는 열처리 뒤 실험에서 관찰 [52]). 다만 최종 평형은 O₂ 방출이라 동역학이 느리다.
- LLTO · LATP 는 각각 3.34 V · 4.53 V 위에서 mutual 0.
- LiPON₀.₁₄–LCO 는 산화물급으로 작지만 2–5 V 내내 반응한다. Li₃PO₄ 계면상과 작은 분해 에너지가 실험의 안정성을 설명. N₂ · O₂ 방출 → in situ TEM 의 공극 [47].
- 결론: *"a SE with a wide electrochemical window and good chemical stability with electrodes is desired … For those SEs (such as sulfides) and interfaces that cannot satisfy the above criteria, an interfacial coating layer material can be applied."*

### `Fig. 4` (봄)

가로축 φ 2.0–5.0 V (윗축 μ_Li −2 ~ −5 eV) · 세로축 *"Mutual reaction energy ΔE^open_D,min,mutual (meV/atom)"* +100 ~ −1400. **실선 = mutual · 점선 = total** · 6 색 (LGPS 빨강 · LPS 보라 · LiPON₀.₁₄ 하늘 · LLZO 초록 · LLTO 검정 · LATP 주황). LiPON₀.₄₆ 은 그림에 없다.

figure-read ≈ (meV per non-Li atom)

| φ (V) | Li₃PS₄ mutual | LGPS mutual | 두 황화물 total (점선 · 거의 겹침) |
|---|---|---|---|
| 2.0 | −597 | −525 | −597 / −525 (실선과 겹침) |
| 2.5 | −627 | −546 | ≈ −670 / ≈ −620 |
| 3.0 | −594 | −542 | ≈ −700 (LGPS) |
| 3.54 | −657 | −616 | — |
| 3.97 | −710 | −669 | — |
| 4.18 이상 | −735 (평탄) | −696 (평탄) | 4.25 V 에서 ≈ −1058 · 5 V 근처 ≈ −1268 |

- 황화물의 mutual 은 2.3 V 부근에서 한 번 깊어졌다가 3.0 V 에서 가장 얕고, 거기서 4.18 V 까지 직선으로 깊어진 뒤 **평탄**해진다 (LCO 가 CoO₂ 까지 탈리튬된 뒤).
- 산화물: LATP 주황 실선은 2 V 의 −280 에서 올라와 4 V 에서 0 · LLTO 검정 실선은 3.34 V 에서 0 · LLZO 초록 실선은 3.3–3.5 V 에서 −33 까지 내려갔다가 0 · 초록 점선은 4.0 V 에서 −137 → −284 로 뛴 뒤 5 V 에 −656.
- 그림과 SI 표가 어긋나는 곳: LLTO 점선 (figure-read ≈ 4.1 V −60 → 5 V −150) ↔ `Table S3` 의 4.10–5.00 V [−113, −9] (§18-11).

---

## 10. 결과 V — 코팅층 (§3.5 · `Table 6` · `Table S4` · `Fig. S1` · 창 막대 그림)

### `Fig. 5a` (봄) — 코팅 18 종의 창 · figure-read ≈ (V · ±0.02)

논문은 이 창을 표로 주지 않는다 (2015 편 SI 가 5 종만). 눈금 보정 뒤 막대 끝을 읽었고, 2015 편 SI 계단표가 있는 5 종 (Li₄Ti₅O₁₂ · LiNbO₃ · Li₂SiO₃ · LiTaO₃ · Li₃PO₄) 의 실선 양 끝이 ±0.01 V 로 맞는다.

| 족 | 화합물 | 환원 한계 | 산화 한계 (실선 끝) | 완전 탈리튬 (점선 끝) |
|---|---|---|---|---|
| Li–Ti–O | Li₄TiO₄ | 0.12 | 3.20 | 3.71 |
| | Li₂TiO₃ | 0.50 | 3.71 | — |
| | Li₄Ti₅O₁₂ | 1.75 | 3.71 | — |
| Li–Nb–O | Li₈Nb₂O₉ | 0.62 | 3.17 | 3.92 |
| | Li₃NbO₄ | 0.94 | 3.64 | 3.92 |
| | LiNbO₃ | 1.75 | 3.87 | 3.92 |
| | LiNb₃O₈ | 2.23 | 3.92 | — |
| Li–Si–O | Li₈SiO₆ | 0.23 | 2.95 | 3.79 |
| | Li₄SiO₄ | 0.26 | 3.41 | 3.79 |
| | Li₂SiO₃ | 0.76 | 3.74 | 3.79 |
| | Li₂Si₂O₅ | 1.27 | 3.79 | — |
| Li–Ta–O | Li₅TaO₅ | 0.34 | 3.11 | 4.05 |
| | Li₃TaO₄ | 0.54 | 3.60 | 4.05 |
| | LiTaO₃ | 1.18 | 3.95 | 4.05 |
| | LiTa₃O₈ | 1.59 | 4.04 | — |
| Li–P–O | Li₃PO₄ | 0.69 | 4.21 | 5.00 (축 끝) |
| | Li₄P₂O₇ | 2.31 | 4.33 | 5.00 (축 끝) |
| | LiPO₃ | 2.48 | 5.00 (축 끝) | — |

- 족 안에서 **Li 가 많을수록 환원 한계가 낮고, Li 가 적을수록 산화 한계가 높다** (저자 서술 그대로). 같은 족의 점선 끝이 한 값으로 모인다 (Ti 3.71 · Nb 3.92 · Si 3.79 · Ta 4.05) — 그 족에서 Li 가 가장 적은 상의 산화 한계다.
- LiTaO₃ 의 점선 끝 (≈ 4.05 V) 은 2015 편 digest 가 적은 4.12 V 와 0.07 V 다르다 (이 그림은 LiTa₃O₈ 을 거친다 — 상 집합 차이로 보임 · 미확정).
- 본문: 실증된 다섯은 *"a wide electrochemical window from a reduction potential of less than 2 V to an oxidation potential of ∼4 V"*.

**`Fig. 5b` (봄)** — 실증된 코팅 5 종의 분해 에너지 vs φ. figure-read ≈ (eV/atom): 0 V 에서 LiNbO₃ −0.81 · Li₃PO₄ −0.69 · LiTaO₃ −0.58 · Li₂SiO₃ −0.40 · Li₄Ti₅O₁₂ −0.33 / 5 V 에서 Li₂SiO₃ −0.41 · Li₄Ti₅O₁₂ −0.25 · LiNbO₃ −0.22 · LiTaO₃ −0.20 · Li₃PO₄ −0.18. ⚠ 세로축 표기는 *"(meV/atom)"* 이지만 값은 eV/atom 이다 (Li₃PO₄ 의 0 V 값이 8 Li × 0.69 V ÷ 8 원자 = 0.69 eV/atom 으로 계단과 맞는다 · §18-11).

### `Table 6` 전사 — 코팅과 네 상대의 ΔE_D,min,mutual (meV/atom)

| 코팅 | Li₃PS₄ | LLZO | LCO | L₀.₅CO |
|---|---|---|---|---|
| Li₄TiO₄ | −125 | 0 | 0 | −30 |
| Li₂TiO₃ | −75 | −5 | 0 | 0 |
| Li₄Ti₅O₁₂ | −80 | −75 | −1 | 0 |
| Li₈Nb₂O₉ | −147 | 0 | 0 | −20 |
| Li₃NbO₄ | −132 | −4 | 0 | 0 |
| LiNbO₃ | −155 | −76 | 0 | 0 |
| LiNb₃O₈ | −173 | −115 | −16 | 0 |
| Li₈SiO₆ | −177 | 0 | −3 | −50 |
| Li₄SiO₄ | −81 | −1 | 0 | −12 |
| Li₂SiO₃ | −19 | −29 | 0 | 0 |
| Li₂Si₂O₅ | −10 | −69 | −4 | 0 |
| Li₅TaO₅ | −117 | 0 | 0 | −32 |
| Li₃TaO₄ | −64 | −3 | 0 | 0 |
| LiTaO₃ | −49 | −68 | 0 | 0 |
| LiTa₃O₈ | −64 | −105 | −22 | 0 |
| Li₃PO₄ | 0 | 0 | 0 | 0 |
| Li₄P₂O₇ | −9 | −101 | −44 | −3 |
| LiPO₃ | −32 | −201 | −76 | −19 |

이 표에서 읽히는 것 (digest 정리)
1. **Li₃PO₄ 만 네 열이 전부 0** 이다.
2. **Li₃PS₄ 열**: 덜 반응하는 순 Li₃PO₄ 0 · Li₄P₂O₇ −9 · Li₂Si₂O₅ −10 · Li₂SiO₃ −19 · LiPO₃ −32 · LiTaO₃ −49 · Li₃TaO₄ = LiTa₃O₈ −64 · Li₂TiO₃ −75 · Li₄Ti₅O₁₂ −80 · Li₄SiO₄ −81 · Li₅TaO₅ −117 · Li₄TiO₄ −125 · Li₃NbO₄ −132 · Li₈Nb₂O₉ −147 · **LiNbO₃ −155** · LiNb₃O₈ −173 · Li₈SiO₆ −177. Nb 족 넷이 전부 −130 아래다.
3. **Li 함량의 두 방향**: Li 가 많은 조성은 충전 양극 (L₀.₅CO) 과 반응하고 (Li 를 내준다 — Li₈SiO₆ −50 · Li₅TaO₅ −32 · Li₄TiO₄ −30), Li 가 적은 조성은 방전 양극 (LCO) · LLZO 와 반응한다 (Li 를 빼앗는다 — LiPO₃ −76 / −201 · Li₄P₂O₇ −44 / −101 · LiTa₃O₈ −22 / −105).
4. 응축 인산염 (Li₄P₂O₇ · LiPO₃) 은 창은 가장 넓지만 (`Fig. 5a`) **방전 상태 LCO 에서 Li 를 끌어온다** — Li₃PO₄ 로 돌아가려는 방향 (우리 읽기 · 저자 언급 없음).

본문 (pp. 3262–3263): 코팅은 원래의 황화물–LCO (≈ −500 meV/atom) 보다 양쪽 계면을 훨씬 안정하게 만든다 → 두꺼운 계면상 억제 · 실험의 상호 확산 감소 [54, 56, 59] 와 일치. LLZO–LCO 에 Nb 를 넣은 실험 [58] 은 Li₈Nb₂O₉ · Li₃NbO₄ 류 비정질 니오베이트 형성으로 해석.

### `Table S4` 전사 — 코팅–SE 반응의 산물 (meV/atom)

| SE | 코팅 | x_m | 최소 반응 에너지에서의 평형상 | mutual / total |
|---|---|---|---|---|
| Li₃PS₄ | Li₄Ti₅O₁₂ | 0.53 | TiS₂, Li₃PO₄, Li₄TiS₄ | −80 / −80 |
| | LiNbO₃ | 0.54 | S, Li₂S, Li₃PO₄, Li₅/₇NbS₂ | −155 / −155 |
| | LiTaO₃ | 0.54 | S, Li₂S, Li₃PO₄, Li₄/₃Ta₂S₄ | −49 / −49 |
| | Li₂SiO₃ | 0.25 | Li₂S, Li₃PO₄, SiO₂ | −19 / −19 |
| | Li₃PO₄ | — | Li₃PS₄, Li₃PO₄ (반응 없음) | 0 / 0 |
| LLZO | Li₄Ti₅O₁₂ | 0.46 | La₂Zr₂O₇, La₂TiO₅, Li₂TiO₃ | −75 / −78 |
| | LiNbO₃ | 0.62 | LaNbO₄, La₂Zr₂O₇, Li₃NbO₄ | −76 / −79 |
| | LiTaO₃ | 0.54 | La₃NbO₇ (표 그대로 — Ta 계에 Nb 상 · 오기로 보임), La₂Zr₂O₇, Li₃TaO₄ | −68 / −72 |
| | Li₂SiO₃ | 0.53 | La₂Zr₂O₇, La₂O₃, Li₄SiO₄ | −29 / −32 |
| | Li₃PO₄ | — | LLZO, Li₃PO₄ (반응 없음) | 0 / — |

- 황화물–코팅 반응은 전부 **O ↔ S 교환** 이다 — P 는 Li₃PO₄ 로 가고 코팅의 금속은 황화물 (TiS₂ · Li₄TiS₄ · Li₅/₇NbS₂ · Li₄/₃Ta₂S₄) 이 된다. Si 만 SiO₂ 로 남는다.

### `Fig. S1` (봄 · 손 크롭)

- **a** — Li₃PS₄–코팅 5 쌍의 mutual vs x (0 ~ −200 meV/atom). 최저점: LiNbO₃ −155 (x ≈ 0.54) · Li₄Ti₅O₁₂ −80 (0.53) · LiTaO₃ −49 (0.54) · Li₂SiO₃ −19 (0.25) · Li₃PO₄ 0 (수평선). 표와 맞는다.
- **b** — LLZO–코팅 5 쌍 (0 ~ −120 meV/atom). Li₄Ti₅O₁₂ −75 (0.46) · LiTaO₃ −68 (0.54) · Li₂SiO₃ −29 (0.47–0.53 평탄) · Li₃PO₄ 0. LiNbO₃ 곡선의 최저점은 figure-read ≈ −76 at **x ≈ 0.49** 이고 x = 0.62 에서는 ≈ −64 다 — `Table S4` 의 x_m 0.62 와 어긋난다 (§18-11).

---

## 11. Discussion — 저자의 종합 · 설계 지침 · 한계 (§4 · pp. 3263–3265)

1. **총평**: *"Most SE–electrode interfaces are not thermodynamically stable before, after, and during electrochemical cycling."* 황화물은 LCO 에 대해 화학적으로도 전기화학적으로도 불안정 (음이온 화학퍼텐셜 불일치). 산화물은 훨씬 낫지만 열역학적으로는 반응이 유리 → 열처리 · 사이클 뒤 열화 가능. ⇒ **계면상 형성은 어디에나 있고, 그 물성이 셀 성능을 좌우한다.**
2. **3 유형** — §4.1.
3. **Type 1 은 드물다**: 창이 넓고 전극과 화학적으로 맞아야 하는데, Li 금속과 고전압 양극 양쪽에 Type 1 인 SE 는 비현실적.
4. **Li 금속 쪽 설계**: 양이온 (Ti · Ge) 은 전자 전도 산물을 만들어 Type 2 → 피한다. 음이온 혼합은 안정성과 전도도를 함께 올리는 길 (LiPON = 옥시질화물 · Li₃PS₄ 의 할라이드 도핑 · 옥시황화물 기대).
5. **양극 쪽**: 황화물–LCO 는 Type 2 + 3 혼합. 혼합 전도 계면상은 사이클 전압에서 스스로 전기화학 사이클을 돌 수 있고 → 계면상 성장 · 부피 변화 반복 · 접촉 파손 → 사이클 열화. *"the key problem of sulfide SE–LCO interfaces is the poor stability, which leads to thick interphase layers, high interfacial resistance, and degradation over cycling."* 처방 = 코팅으로 Type 3 로 바꾸기.
6. **산화물 SE–LCO**: Type 1 또는 Type 3. Type 3 가 되면 산물이 Li 를 잃어 Li 전도가 나쁘다 → 여기서도 코팅 (예: 니오베이트 [58]). Nb 금속의 연성이 접촉을 돕는다는 말도 덧붙인다.
7. **저자가 적은 한계**: 동역학 없음 (준안정 평형 가능 · 실제 계면상은 다를 수 있다) · 중성 원소 평형만 (Li⁺ · e⁻ 의 평형 → 공간전하 · 분극은 범위 밖 [67]) · 벌크 에너지만 (구조 무질서 · 계면 결정면 · 미세구조 미고려 — *"These atomistic and microstructural features may also change the electronic conductivity of the interphase and the corresponding interface types"*) · DB 에 없는 상 (그래서 Li₃PS₄ · Li₂PO₂N 을 추가) · DFT 에너지 정확도 [68] · 0 K (엔트로피 무시).

---

## 12. DFT/계산 방법 ★

- **code / version**: VASP (판 미기재) · PAW.
- **functional**: PBE (GGA). vdW 언급 없음.
- **k-points / ecut**: *"consistent with the parameters used in the Materials Project"* — 수치 미기재.
- **DFT+U · 보정**: MP 의 보정 스킴 (산화물 · 전이금속 산화물 · 기체 O₂ · N₂ · F₂ · refs 16, 17 = Jain 2011 GGA/GGA+U 혼합 · Wang 2006). 값 미기재.
- **에너지 출처**: 대부분 Materials Project DB (2015 년 판 · 판 번호 미기재). MP 에 없는 물질만 자체 DFT.
- **구조**: LGPS = MP-696138 (실험 구조에서 정렬 · hull 위 21 meV/atom) · Li₃PS₄ = γ 상 Pmn2₁ 기반 바닥상태를 Li–P–S 상도에 추가 · LLZO = 입방 (정방상과 에너지 비슷하다고 봄) · LLTO Li₀.₃₃La₀.₅₆TiO₃ · LATP Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃ · Li₂PO₂N 결정 (ref 29) 을 Li–P–O–N 에 추가 · LCO = MP-24850 · L₀.₅CO = MP-762036 (층상 최저).
- **무질서 처리**: 이 논문에는 절차 서술이 없다 (2015 편에 있음). LiPON 은 구조 없이 hull 혼합물.
- **AIMD · MLIP · NEB · 전자구조 (DOS · 띠틈)**: 없음.
- **특이사항**: 엔트로피 · PV 무시 (0 K) · 계면 구조 · 계면 에너지 없음 (벌크 상의 섞음).

---

## 13. Post-processing ★

- **무엇**: 조성 상도 → hull 위 높이 (식 1) · grand potential 상도 (Li · O · S · Co 를 각각 열어) → 창과 전위별 평형상 (식 2–4) · pseudo-binary 를 x 로 훑어 kink 마다 평형상과 반응 에너지 (식 5–10) · 같은 것을 φ 별로 (식 11–14).
- **도구**: pymatgen (상도 · grand potential · ref 30) · MP DB.
- **수치화 · 기록**: 창 = 막대 (`Fig. 1a` · `Fig. 5a`) · 분해 에너지 vs φ 곡선 (`Fig. 1b` · `Fig. 5b`) · mutual vs x 곡선 (`Fig. 3` · `Fig. S1`) · φ 구간마다 평형상과 [최소, 최대] 범위 (`Table 5` · `Table S3`) · x kink 마다 평형상 (`Table S2`). 산물은 화학식 목록으로만 남기고 상 분율 · 반응식 계수는 주지 않는다.

---

## 14. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | SE 8 종의 전기화학 창 막대 (φ 0–5 V · 윗축 μ_Li) · 점선 = 완전 탈리튬 전위. **봄 + 픽셀 판독 (표와 ±0.01 V)** | 황화물 창이 2.5 V 아래에서 끝난다는 한 장 — 우리 작동창 (2.5–4.25 V) 을 겹쳐 그리면 '창 전체가 산화 구간' 설명 그림이 된다 |
| 1b | 분해 에너지 vs φ 곡선 8 개 (0 ~ −2.0). **봄 + 양 끝 판독** — ⚠ 축 단위 표기 meV 는 eV 의 오기 | 구동력이 계단 뒤 전위에 비례한다는 것 — 2.5 V · 4.25 V 값을 계단표에서 산술로 낼 수 있다 (§4.7) |
| 2a–c | SE · LCO · L₀.₅CO 의 μ_O · μ_S · μ_Co 안정 창 막대. 황화물은 O · S 에서 LCO 와 안 겹치고 Co 에서는 겹친다. **봄 + 픽셀 판독 (표와 ±0.02 eV)** | '불일치의 원인은 Co 가 아니라 음이온' 의 근거 그림 · 우리 μ_O 열린 계산 (`cei_esw_O_2026_09_16.json`) 과 같은 구성 — S · 전이금속을 여는 확장의 본보기 |
| 3 | mutual 반응 에너지 vs x (실선 LCO · 점선 L₀.₅CO · 7 SE). **봄** | pseudo-binary 곡선의 표준 꼴 · 바닥이 평평한 사례 (Li₃PS₄–LCO x 0.41–0.48) |
| 4 | 전위 (2–5 V) 에 따른 mutual (실선) · total (점선) · 6 계면. **봄 + 곡선 판독** | ⭐ 우리에게 없는 축 — 2.5–4.25 V 구간을 떼어 읽었다 (§4.7). mutual 과 total 을 나눠 그리는 법 · 4.18 V 위 평탄 |
| 5a | 코팅 18 종의 창 막대 (5 족 색 구분 · 점선 = 완전 탈리튬). **봄 + 픽셀 판독 (18 종 전부)** | 논문이 표로 안 준 값 — Li–P–O 족 (Li₃PO₄ 4.21 · Li₄P₂O₇ 4.33 · LiPO₃ 5.0 V) 이 우리 kb 카드의 응축 인산염 순서와 같은 방향 |
| 5b | 실증 코팅 5 종의 분해 에너지 vs φ. **봄 + 양 끝 판독** — ⚠ 축 단위 표기 오기 | 코팅의 0 V 구동력 (Li 금속 쪽에 못 쓰는 이유) |
| S1 | 코팅–Li₃PS₄ (a) · 코팅–LLZO (b) 의 mutual vs x. **봄 (손 크롭) + LiNbO₃ 곡선 판독** | LiNbO₃–Li₃PS₄ −155 가 한눈에 · `Table S4` 의 x_m 오기 확인 |
| Table 1 | 재료 9 종 — 조성 · 실험 전도도 · 구조 출처 · hull 위 높이 · 조성 평형상. **텍스트 전사** | LiPON 이 hull 혼합물이라는 사실 · L₀.₅CO 가 층상 대리 |
| Table 2 | SE 8 종의 0 V · 환원 개시 · 산화 개시 · 5 V 평형상과 분해 에너지. **텍스트 전사** | 황화물 창 · Li 금속 쪽 산물 |
| Table 3 | 상대의 μ_O · μ_S 에서의 평형상. **텍스트 전사** | 양극의 O 가 황화물을 Li₃PO₄ + S 로 만든다는 열린계 그림 |
| Table 4 | 닫힌계 14 쌍의 x_m · 평형상 · mutual · total. **텍스트 전사 + 식 (8) 검산** | `[Nolan18Rev]` · `jiang2022_se_doped_lpscl_high_throughput_dft` 가 인용한 −405 · −564 · −340 · −499 의 원전 |
| Table 5 | 전위 아래 3 계면 (Li₃PS₄ · LLZO · LiPON₀.₁₄) 의 구간별 평형상 · 범위. **텍스트 전사** | Li₃PO₄ 가 2.91 V 까지만 · 3.26 V 위 Li 없는 산물 |
| Table 6 | 코팅 18 × 상대 4 의 mutual. **텍스트 전사** | Li₃PO₄ 만 전부 0 · LiNbO₃–Li₃PS₄ −155 |
| Table S1 | LiPON 두 조성의 전 계단 (φ · Δn_Li · 평형상). **텍스트 전사 (§18-5 에서 사용)** | 1.07 V '산화 개시' 의 Δn_Li 가 −0.01 뿐임 |
| Table S2 | 닫힌계 7 SE × 2 전극의 x 별 평형상. **텍스트 전사 (황화물 전량 · 나머지 요약)** | 계면상 조성의 공간 변화 · 금속 Co 구간 |
| Table S3 | 전위 아래 4 계면 (LGPS · LLTO · LATP · LiPON₀.₄₆). **텍스트 전사** | LGPS–LCO 의 2.5–4.25 V 산물 |
| Table S4 | 코팅 5 × SE 2 의 x_m · 산물. **텍스트 전사** | 코팅–황화물 산물 = 전이금속 황화물 |

---

## 15. 우리 DFT 대비 → `our_dft_baseline.md` · `db/properties/` 원장

> 규율: 문헌 수치는 소환값이다. 아래 표의 '우리' 칸에는 **값을 싣지 않고 정의와 원장 경로만** 적는다. 이 논문에는 우리 조성 (Li₆PS₅Cl · Li₅.₄PS₄.₄Cl₁.₆ · 도핑 조성) 이 없으므로 수치 대조 자체가 성립하지 않는다.

### 15.1 방법 · 정의 대조표

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| SE 단독 창 | 식 (2)–(4) · pymatgen grand potential · MP 2015 세대 · Li₃PS₄ · LGPS | 같은 구성 (`get_element_profile`) · MP 2026 `GGA_GGA+U` 고정 · comp1 · modelc (`litdb/our_dft_baseline.md`) | 같은 방법 · 다른 조성 · 다른 hull 세대. 우리 조성과의 수치 대조는 2015 편 digest §10b 에 이미 있다 — 이 편이 더하는 것은 없다 |
| 닫힌계 계면 반응 | 식 (5)–(10) · **mutual** (끝점의 hull 위 높이를 뺌) · meV/atom | pymatgen `InterfacialReactivity(use_hull_energy=True)` — `db/properties/interface_reactivity_results.json` · cascade 축 ① 카드의 R1 | **같은 양**이다. 계보 카드 (`kb/syntheses/cathode_coating_computational_lineage.md`) 가 '[Zhu16] 판' 이라고 불러 온 정의가 원문 식 (8) 로 확인된다 |
| 충전 상태 대리 | Li₀.₅CoO₂ (층상 · hull 위 33 meV/atom) | Li₀.₅NiO₂ (반충 대리) + LCO (cascade 축 ① 카드 R4) | 같은 발상 — 리튬화 상태의 대리이지 전압이 아니다 |
| 전위 아래 계면 | 식 (11)–(14) · φ 2–5 V 를 훑음 · 비-Li 원자당 | **없음** (닫힌계만) | 🔴 우리에게 없는 축. 양극 쪽 판단을 2.5–4.25 V 에서 한다는 관례를 계면 계산에 적용하려면 이 구성이 필요하다 (§16-2) |
| Li 아닌 원소의 창 | μ_O · μ_S · μ_Co 를 각각 연다 | μ_O 만 (`db/properties/cei_esw_O_2026_09_16.json` — 인용 가능한 것은 Δμ_O 축 위의 순서와 산물 정체) | 같은 구성. S · 전이금속은 열지 않았다 |
| 산물 평가 | 문헌 인용으로 전자 전도 여부 → 3 유형 (정성 · 문턱 없음) | 산물별 MP 띠틈 등급 (넓은 갭 · 좁은 갭 · 금속성 · 미판정 — 문턱 명시) + 추적 원소가 어느 산물로 가는지의 분율 (cascade 축 ① · ③ 카드 R2) | 우리 쪽이 규칙을 적어 둔 정량 층이다. 둘 다 '부동태화된다' 까지는 못 간다 (갭 · 전도성은 필요조건 — 카드 5b) |
| 준안정 상 처리 | hull 위 높이를 그대로 두고 mutual 에서 뺀다 | 도핑 조성을 평형 상 혼합으로 넣는다 (카드 '관점') | 같은 처리 — 구동력의 하한 쪽 |
| 온도 · 동역학 | 0 K · 엔트로피 무시 · 동역학 없음 | 같음 | 공통 한계 |

### 15.2 트랙별 판정 — 지지 · 반박 · 무관

| 우리 판정 · 트랙 | 이 논문과의 관계 | 근거 |
|---|---|---|
| **cascade 갭 A** — *"산물 물성 순위: SE 도펀트에 대해 0 건"* (`reports/황화물 분해 부피 도펀트 문헌 갭.md` · cascade 트랙 · 1저자 = 사용자) | 🟢 **유지** | 정성 3 유형 · 산물 물성 계산 0 · 도펀트 계열 0 (§4.1 · §4.4). 같은 보고서의 *"Zhu 2017 이 유일한 제안"* 문구만 좁힐 것 (§4 머리) |
| **cascade 갭 B** — 도펀트별 분해 부피 | ⚪ **무관** | 부피 계산 0 · 언급 1 문장 (§4.5) |
| **양극 쪽은 2.5–4.25 V 에서 판단 · 창 전체가 산화 구간** (CLAUDE.md §데이터 규율 · 사용자 2026-11-09) | 🟢 **같은 방향** | Li₃PS₄ 2.31 V · LGPS 2.15 V · Li₂S 2.01 V — 전부 2.5 V 아래 (`Table 2`). 계면에서도 2–5 V 전 구간 반응 (`Table 5`) |
| **ESW 산화 개시는 S 가 정한다 (축 ①)** | 🟢 **같은 방향** | *"The sulfide SEs are oxidized at a similar potential of ∼2 to 2.5 V"* · Li₂S 2.01 V 가 바닥 |
| **Li₃PO₄ 는 작동창 맨 아래에서만 평형** (`kb/concepts/se_redox_frontier.md` 4 장 ④) | 🟢 **같은 모양 (다른 계)** | Li₃PS₄–LCO 에서 Li₃PO₄ ≤ 2.91 V → Li₄P₂O₇ → Co 인산염 (`Table 5`). 우리는 SE 자신의 O · 양극 없음이라 경계 전압을 맞대지 않는다 |
| **`interface_reactivity` 의 문헌 귀속** — 형식화 [Rich16] → mutual 판 [Zhu16] → 양극 SOC 두 상태 [Nolan19] (계보 카드) | 🟢 **확인 + 보정 하나** | mutual 정의 = 식 (8) ✓. 다만 **양극의 두 상태 (LCO · L₀.₅CO) 는 이 논문이 이미 한다** — [Nolan19] 의 몫은 여러 양극 · 여러 코팅으로의 전수 적용이다 |
| *"닫힌 −0.41 → 5 V 개방 −1.27 eV/atom = 3.1 배"* (`nolan2018_computation_accelerated_design_review` digest · `comparison_vs_ours.md` §J-7 `[Nolan18Rev]` 블록의 '개방계 확장의 정량 동기' 행) | 🔴 **정정 필요 (원전 기준)** | −0.41 은 mutual · 원자당, −1.27 은 total · 비-Li 원자당이다. 같은 잣대로는 mutual 1.3 배 · total 2.2 배 (§5.3 · §20-2). 그 행들은 이 digest 가 고치지 않았다 |
| 띠틈 · 탄성 · 수송 축 | ⚪ **무관** | 해당 계산 없음 |

### 15.3 litdb 의 관련 digest 와 엮기

| digest | 이 논문과의 관계 |
|---|---|
| `zhu2015_esw_grand_potential_origin` | 직계 전편. 2016 편에서 바뀐 것: LiPON 을 Li₂PO₂N 하나에서 실제 조성 두 개 (hull 혼합물) 로 · hull 위 높이를 0 으로 놓지 않고 그대로 실음 · LATP 산화 개시 **4.31 V** (본문 · `Table 2` · `Fig. 1a` 일치 — 2015 편 표의 4.21 과 다르다 · 2015 digest §15 의 미판정 건에 대한 정황) · LGPS 산화 2.15 (2015: 2.14) · LATP 환원 2.16 (2015: 2.17). Li₆PS₅Cl · Li₇P₃S₁₁ 등은 2016 편에서 빠졌다 |
| `richards2016_interface_stability_pseudobinary` | 같은 해 · 같은 종류의 식 · 다른 그룹 (Ceder). 차이 셋: ① Richards 는 μ_Li 를 양극 평균 전압 한 점에, Zhu 는 2–5 V 구간 ② Richards 의 ΔΦ (식 4) 는 분해 전 끝점 기준이라 Zhu 의 **total** 에 해당하고 no-mixing (식 5) 을 따로 낸다 — Zhu 는 mutual 을 먼저 낸다 ③ 양극 7 종 × 전해질 37 종 ↔ LCO 하나 × SE 7 종. **같은 Li₃PS₄–LiCoO₂ 인데 적힌 산물이 다르다** — Richards: Co(PO₃)₂ + CoS₂ + S / Zhu (3.26–5 V): Co₃S₄ + CoSO₄ + Co₃(PO₄)₂ (§16-4) |
| `miara2015_llzo_cation_dopants_cathode_interphases` (ref 31) | 이 논문이 pseudo-binary 의 출처로 드는 편. 식 (11)–(13) 의 *"similar to the previous study³¹"* |
| `nolan2018_computation_accelerated_design_review` | 같은 그룹의 리뷰. `Fig. 2C` · p. 2035 의 −0.41 · −0.56 · −1.27 이 이 논문 `Table 4` · `Table 5` 에서 온다 (§20) |
| `nolan2019_chemistries_stable_high_energy_cathodes` · `nolan2021_garnet_cathode_coating` | 같은 기계를 NMC · 가넷 코팅으로 넓힌 후속. 식은 이 논문을 인용으로 승계 |
| `xiao2019_cathode_coating_screening` · `xiao2020_interface_stability_ssb_review` | Ceder 쪽 계보. Xiao 2019 가 '소수 산화물 제안' 으로 든 Li-rich 목록 (Li₄TiO₄ · Li₂TiO₃ · Li₈SiO₆ · Li₄SiO₄ · Li₅TaO₅ · Li₃TaO₄) 은 이 논문 p. 3263 의 **LLZO 용** 목록이다 |
| `jiang2022_se_doped_lpscl_high_throughput_dft` | 기준선으로 이 논문의 340 · 405 · 499 · 564 를 인용 — 원문과 일치 |
| `lomeli2024_predicting_reactivity_passivation_ssb_interfaces` · `guo2025_kinetic_cathode_se_interface` · `qi2025_high_voltage_limits_halide_sulfide_assb` · `park2026_llzo_li13si4_dopant_interface_thermal_battery` · `jang2026_halide_se_interfacial_stability_highv_na` · `zhu2020_air_stable_se_design_principles` | 방법의 출처로 이 논문을 인용하는 편들 |
| `sundar2025_oxide_coating_screening_lpscl` (갭 보고서의 '방법이 가장 가까운 선행') | 이 논문이 문장으로만 세운 두 축 (산물의 전자 전도 · 이온 전도) 을 계산값 (띠틈 · 이동 장벽) 으로 바꿔 코팅 순위에 쓴 편 — 9 년 뒤 |

---

## 16. 적용 인사이트

1. **갭 판정 (cascade 트랙)** — 이 논문은 산물 물성을 점수로 쓰지 않는다. '산물이 전자를 막고 Li 를 통하면 좋다' 는 원칙을 양극 쪽까지 문장으로 세웠고, 원소 부류 수준의 설계 규칙 (양이온 = 전자 전도 산물 / 음이온 = 절연 Li 이원상) 까지 갔다. **도펀트별 숫자** 는 여전히 비어 있다. 보고서 표 '가' 줄의 이 편은 '갭을 깨지 않음' 으로 닫을 수 있다 (판정은 사용자).
2. **우리 작동창에서 계면을 읽으려면 열린 pseudo-binary 가 필요하다.** 이 논문 숫자로는 황화물–LCO 의 평형 계면상이 2.5 V 와 4.25 V 에서 완전히 다르다 — Li₃PO₄ 는 2.91 V 까지만, 3.26 V 위는 Li 가 없는 산물뿐이고 전자 전도성 Co 황화물은 내내 있다. '이로운 산물을 내는 도펀트' 를 물으려면 산물 집합을 **창의 두 끝 (2.5 · 4.25 V)** 에서 내야 하고, 닫힌계 한 점 (반충 대리) 으로는 이 변화를 못 본다. 도구는 이미 있다 (pymatgen 의 grand-potential 모드) — 새 물리량이므로 보고량 카드부터 (φ 선택 규칙 · 정규화 · mutual/total 선언).
3. **정규화와 mutual/total 을 선언하지 않으면 배수가 틀린다.** 이 논문의 닫힌계 값 (원자당 · mutual) 과 전위 아래 값 (비-Li 원자당 · total) 을 나란히 놓은 *"3.1 배"* 가 litdb 에 다섯 군데 있다 (§20-2). 같은 잣대로는 mutual 1.3 배다 — 전위가 '상호 반응' 을 키우는 폭은 크지 않고, total 의 증가는 SE 자신의 산화다 (저자 설명과 같다). 우리가 열린계 카드를 쓸 때 맨 먼저 적을 줄이다.
4. **'어느 산물 집합에 점수를 매기나' 는 규약이다.** ① x_m 을 mutual 의 최소에서 고르느냐 total 의 최소에서 고르느냐에 따라 표에 적히는 산물이 달라질 수 있다 (Zhu ↔ Richards 가 같은 Li₃PS₄–LiCoO₂ 에 다른 산물을 적는다 — DB · 상 집합 차이도 섞여 있어 원인은 미확정) ② 최솟값이 평평하면 (x 0.41 · 0.48 둘 다 −405) 산물 집합이 하나로 안 정해진다 ③ x 를 훑으면 금속 Co 가 평형상인 구간이 있다. 우리 카드의 '반충 최소 kink 산물' 규칙은 ① 을 정해 두었지만 ② · ③ (동률 · 인접 kink) 은 적어 둘 만하다.
5. **코팅 지침에서 가져올 것** — Li₃PO₄ 는 네 상대 모두와 반응 0 이고 창이 4.21 V 까지다 (우리 창 위 끝에서 0.04 V 모자람 · hull 오차 안). 표준 코팅 LiNbO₃ 는 Li₃PS₄ 와 −155 meV/atom 으로 반응해 Nb 황화물을 만든다 — '코팅 자체의 안정성이 아니라 코팅–SE 반응 산물이 성능을 정한다' (Sundar 2025) 의 씨앗이 이 표에 이미 있다.

---

## 17. 인용 가능 문장 (deck/paper 용 · 영문 초안)

- "Zhu, He, and Mo evaluate SE–LiCoO₂ interfaces with closed and Li-open pseudo-binary constructions and classify the resulting interphases qualitatively (stable, mixed-conducting, or SEI-forming); the electronic conductivity of each interphase is taken from the literature and is not calculated."
- "For Li₃PS₄–LiCoO₂, Li₃PO₄ is an equilibrium product only below 2.91 V vs Li/Li⁺, and above 3.26 V every equilibrium product is Li-free (Co₃S₄, CoSO₄, and Co₃(PO₄)₂)."
- "The incompatibility between sulfide electrolytes and LiCoO₂ originates from the mismatch of the O and S chemical potentials, not from Co."
- "The closed-system mutual reaction energies (−405 and −564 meV/atom for Li₃PS₄ with LiCoO₂ and Li₀.₅CoO₂) are normalized per atom, whereas the potential-dependent values are normalized per non-Li atom."
- 출처 표기 (랩 표준): *J. Mater. Chem. A*, 4, 3253 (2016).

---

## 18. 비판 — 주의 / 한계 (over-claim 방지)

1. **분류를 떠받치는 물성이 계산값이 아니다.** 전자 전도 여부는 문헌 인용이다 — Co 황화물은 ref 39 (*RSC Adv.* 4, 21151 (2014)) 와 ref 62 (*Inorg. Chem.* 4, 685 (1965)), LaCoO₃ 는 *"may be electronically conductive"* (ref 53 · 1967), Li₃N · Li₃P 의 Li 전도는 refs 63 · 64. 띠틈 · 전도도 · 문턱 어느 것도 없다. 유형 배정은 저자의 판단이다.
2. **분류를 자기 표 전체에 적용하지 않았다.** ① `Table S4` 의 코팅–황화물 산물은 TiS₂ · Li₅/₇NbS₂ · Li₄/₃Ta₂S₄ 같은 전이금속 황화물인데 전자 전도성 여부를 따지지 않고 *"better stability … compared to the original sulfide SE–LCO interfaces"* 로 넘어간다 (LiNbO₃–Li₃PS₄ −155 meV/atom 은 작지 않다) ② `Table S2` 의 금속 Co 구간도 언급이 없다 ③ 양극 쪽 계면상의 Li 전도는 산화물 SE 에 대해서만 논하고, Li 가 전혀 없는 황화물–LCO 고전압 산물 (`Table 5`) 에 대해서는 말하지 않는다.
3. **정규화가 표마다 다르고 표기는 같다** (§5.3). 본문도 −1.27 을 *"eV per atom"* 이라고 쓴다. 후속 문헌 (같은 그룹의 2018 리뷰 포함) 이 두 값을 한 줄에 놓게 된 뿌리다.
4. **x_m 규약** — mutual 의 최소에서 고른다. 그 x 에서의 산물만 본문 표에 실려 '계면 산물' 로 읽히지만, x 를 훑으면 산물이 크게 바뀐다 (`Table S2`). 최솟값이 평평한 경우 (Li₃PS₄–LCO) 의 처리 규칙은 없다.
5. **LiPON 은 구조가 아니라 hull 혼합물이다.** '창 0.69–1.07 V' 는 조성의 평형상 (Li₂PO₂N + Li₃PO₄ + Li₂O) 가운데 가장 먼저 반응하는 것의 창이고, 1.07 V '산화 개시' 의 Li 변화는 LiPON₀.₁₄ 에서 식당 −0.01 뿐이다 (`Table S1`). 의미 있는 눈금은 저자도 따로 든 3.8 V · 2.8 V 다. 비정질 LiPON 의 에너지 (hull 위 높이) 는 들어 있지 않다.
6. **양극은 LiCoO₂ 하나** — *"similar results are expected for other transition metal oxide cathodes"* 는 계산 없는 문장이다. Ni 계 (우리 셀) 로 옮기려면 Richards 2016 · Xiao 2019 · Nolan 2019 를 본다.
7. **0 K · 벌크 · 평형** — 엔트로피 · 동역학 · 계면 구조 · 공간전하 없음 (저자 자인). '산물' 은 평형 후보 집합이지 관찰된 계면상이 아니다. 기체 (O₂ · N₂) 가 산물인 반응은 0 K 에너지라 기체 엔트로피가 빠져 있다.
8. **MP 2015 세대 hull** — 숫자를 현재 hull 값과 섞지 않는다 (2015 편 digest §15 와 같은 단서). 추가한 상 (γ-Li₃PS₄ · Li₂PO₂N) 에 결과가 기대고, 5 원소 상도 (Li–Co–O–P–S) 의 완전성은 확인할 길이 없다 (저자 자인: *"The phase diagrams might be incomprehensive"*).
9. **충전 양극의 대리** — 층상 Li₀.₅CoO₂ (hull 위 33 meV/atom) 한 점. 열린계에서는 전극이 전위에 따라 스스로 탈리튬되므로 (표에 L₀.₅CO · CoO₂) 닫힌계의 'L₀.₅CO 열' 과 열린계의 '4 V 부근' 은 같은 상태가 아니다.
10. **'실험과 일치' 의 독립성** — LGPS CV (ref 12) 는 1저자 Zhu 가 공저자인 같은 그룹 실험이다 (2015 편 digest §15 와 같은 지적). LLTO · LATP · LiPON · LCO–황화물 TEM 은 외부 문헌.
11. **논문 안의 불일치 (원문 것 — 인용할 때 주의)**
    - 단위 표기: `Fig. 1b` · `Fig. 5b` 의 세로축 *"(meV/atom)"* → 값은 **eV/atom** (표 · 계단 산술과 일치).
    - 본문 ↔ 표: LGPS 의 0 V 반응 에너지 본문 −1.23 ↔ `Table 2` −1.25 · LiPON₀.₄₆ 의 mutual 본문 −106 / −153 ↔ `Table 4` −99 / −154.
    - 본문 표 ↔ SI: `Table 4` 의 LiPON–L₀.₅CO total (−65 · −154) ↔ `Table S2` (−79 · −167). 식 (8) 로 다시 내면 SI 값이 맞다. LATP–LCO 의 total −63 은 SI 의 x = 0.35 행 값이다 (x_m 0.32 행은 −62).
    - SI 표 ↔ 그림: `Table S3` 의 LLTO–LCO total 범위가 `Fig. 4` 검은 점선과 구간별로 안 맞는다 (figure-read ≈ 4.1 V −60 → 5 V −150 ↔ 표의 4.10–5.00 V [−113, −9] · [−152, −68] 은 3.34–3.71 V 행에 적혀 있다) · LATP 마지막 행 [−113, 52] 는 그림상 [−113, −52] 로 읽힌다 (부호 누락으로 보임).
    - `Table S4`: LLZO–LiTaO₃ 산물의 *"La₃NbO₇"* (Ta 계에 Nb) · LLZO–LiNbO₃ 의 x_m 0.62 ↔ `Fig. S1b` 최저점 x ≈ 0.49.
    - 축 제목 *"pesudo-binary"* · 식 (5) 의 *"C_inteface"* (오탈자).
    - 판정: 결론을 바꾸는 것은 없다. 인용은 `Table 2` · `Table 4` (mutual 열) · `Table 5` · `Table S2` 기준으로.

---

## 19. 기법 용어 미니사전

- **interphase (계면상)**: 두 물질이 맞닿아 반응해 생긴 제 3 의 층. interface (경계면) 와 구분한다.
- **pseudo-binary (유사 이원)**: 두 화합물을 x : (1 − x) 로 섞은 조성들을 한 축으로 놓고, 각 조성의 hull 에너지를 훑어 가장 유리한 반응을 찾는 구성. 꺾이는 점 (kink) 마다 평형상 집합이 바뀐다.
- **mutual reaction energy (상호 반응 에너지)**: pseudo-binary 의 분해 에너지에서 두 끝점 자신의 분해 에너지 (hull 위 높이 · 또는 그 전위에서의 자기 분해) 를 뺀 것 (식 8 · 12). 두 물질이 '서로 때문에' 얻는 구동력.
- **total decomposition energy**: 끝점의 자기 분해까지 포함한 전체 (식 7 · 10 · 11 · 14).
- **x_m**: mutual 이 최소가 되는 섞음 비.
- **grand potential 상도**: 한 원소 (Li · O · S · Co) 를 저장소에 열어 둔 상도. 그 원소의 화학퍼텐셜 μ 를 훑으면 평형상이 계단으로 바뀐다. Li 를 열면 μ_Li = μ⁰ − eφ 로 전압 축이 된다.
- **화학 안정 ↔ 전기화학 안정**: 전위 없이 섞기만 했을 때 (기준 3) ↔ 전위를 걸었을 때 (기준 1 · 4).
- **O-poor / S-poor 한계**: 그 물질이 버티는 μ_O · μ_S 의 가장 낮은 값.
- **MIEC (mixed ionic and electronic conductor)**: 이온과 전자가 함께 통하는 물질. 계면상이 MIEC 이면 분해가 멈추지 않는다 (Type 2).
- **Type 1 / 2 / 3**: 계면상 없음 / MIEC 계면상 / 전자 절연 계면상 (SEI). Wenzel 2015 (Janek 그룹) 의 분류.
- **인공 SEI**: 자발 계면상 대신 미리 입힌 전자 절연 · 이온 전도 코팅.

---

## 20. litdb 역참조 — 이 논문을 가리키던 카드와 소환값 대조

이 digest 전에는 litdb 에 원문이 없어서 아래 카드들이 2차 경로 (주로 같은 그룹의 2018 리뷰) 로 이 논문의 값을 적었다. 원문과 대조했다 (**다른 카드는 고치지 않았다** — 정정은 제안이다).

**20-1. 맞는 것**
- `jiang2022_se_doped_lpscl_high_throughput_dft` 의 기준선 340 · 405 · 499 · 564 meV/atom = `Table 4` mutual ✓.
- `nolan2018_computation_accelerated_design_review` (`[Nolan18Rev]`) 의 Li₃PS₄–LiCoO₂ −0.41 · Li₃PS₄–Li₀.₅CoO₂ −0.56 eV/atom · 산물 Li₃PO₄ + Li₂SO₄ + Li₂S + Co₉S₈ = `Table 4` (−405 · −564) ✓ · 5 V 의 −1.27 = 본문 p. 3260 · `Table 5` (−1273) ✓.
- `xiao2019_cathode_coating_screening` 이 옮긴 Li-rich 산화물 여섯 = p. 3263 ✓ (단 그 목록은 LLZO 용이다).
- 계보 카드의 'mutual (끝점 준안정성 제거) 판 = [Zhu16]' = 식 (8) ✓.

**20-2. 고쳐 읽어야 하는 것**
- **'닫힌 −0.41 → 5 V 개방 −1.27 = 3.1 배'** (`nolan2018_computation_accelerated_design_review` digest 네 곳 [155 · 272 · 405 · 574 행] · `comparison_vs_ours.md` §J-7 `[Nolan18Rev]` 블록 한 행) — 두 수는 잣대가 다르다 (mutual · 원자당 ↔ total · 비-Li 원자당). 원문 기준 같은 잣대: mutual ≈ −580 (닫힌계를 비-Li 원자당으로 환산 · 우리 산술) → −596 (2 V) → −737 (5 V) = **1.3 배** · total → −1273 = **2.2 배**. '개방계로 가면 구동력이 3 배' 는 쓰지 않는다. '전위가 올라가면 SE 자신의 산화 몫이 더해져 total 이 두 배쯤 된다' 가 원문에 맞는 문장이다.
- **'양극 SOC 두 상태 전수 적용 = [Nolan19]'** (계보 카드 · `nolan2019…` digest) — 방전 · 충전 두 상태를 나란히 계산한 것은 이 논문 (2016) 이 먼저다. [Nolan19] 의 새로움은 양극 · 코팅 화학의 범위다.

**20-3. 새로 생긴 연결**
- `qi2025_high_voltage_limits_halide_sulfide_assb` 가 *"(litdb 없음)"* 이라고 적은 SI 참고문헌 [8] 이 이 digest 다.
- `park2026_llzo_li13si4_dopant_interface_thermal_battery` 가 *"이 논문이 스스로 인용한 ref 8 이 바로 그 방법"* 이라고 한 편도 이것이다.

---

## 🗨️ Q&A 로그

(아직 없음)
