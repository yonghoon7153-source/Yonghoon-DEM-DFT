# ⏸ 병합 대기 — `he2023_halogen_chemistry_solid_electrolytes`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09 · litdb-curator 다중 동시 실행으로 **`INDEX.md`·`comparison_vs_ours.md` 직접 수정 금지**를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 블록을 옮기고 이 파일을 지운다.**
>
> ⛔ **이 편은 리뷰다 — 자체 계산 0 · 자체 실험 0.** 모든 수치가 2차 인용이고,
> `Table S1` 47행에는 **압력·전극·온도이력이 한 칸도 없다.**
> ⇒ **`comparison_vs_ours.md` 의 물성 4축(A/B/C/D) 표에 넣지 않는다.**
> ⇒ **§J-7 형식의 `🔧 방법·개관 원전` 블록**으로만 둔다 (아래 ②).

---

## ① `INDEX.md` 에 추가할 행

> 넣을 위치 제안: **📌⭐ MUST-READ (분야 전체 field-map)** 절 — `bai2020_argyrodite_review_progress`(argyrodite 전용 field-map)와
> `famprikis2019_fundamentals_inorganic_sse`(SE 일반 튜토리얼) 사이. 이 편은 **"할로겐"이라는 축의 field-map** 이라 셋이 겹치지 않는다.

| `papers/he2023_halogen_chemistry_solid_electrolytes.md` | **[외부·리뷰·★★할로겐 축 field-map + Cl-rich 계보의 인용 뼈대]** **Bijiao He**¹, Fang Zhang¹, **Yan Xin\***¹, Chao Xu¹, Xu Hu², Xin Wu³, **Yang Yang\***⁴⁻⁸, **Huajun Tian\***¹ (¹華北電力大 NCEPU Beijing ²국가절能中心 ³中建三局 ⁴⁻⁸ Univ. of Central Florida), "**Halogen chemistry of solid electrolytes in all-solid-state batteries**" (***Nature Reviews Chemistry* 7, 826–842 (2023)**, DOI `10.1038/s41570-023-00541-7`, online 2023-10-13; 본문 12 pp · **Fig 7** · **본문 표 0개** · refs **203** · SI 6 pp = **`Table S1` 47행** + SI refs 48). ⚠ **자체 계산 0 · 자체 실험 0** — 본문에서 "DFT/first-principles/density functional" 은 **참고문헌 주석에만** 등장. **다루는 범위** = Li–M–X 할라이드(LiAlCl₄·Li₂MX₄·Li₃MX₆·Li₂Sc₂/₃Cl₄) + LPSX 황화물(Li₆PS₅X·Li₇P₂S₈X); **분량 배분이 할라이드 ~5 pp vs argyrodite ~2 pp 로 기운다**. **★1 자리 점유 정본**: free-anion 두 자리를 **4a / 4d** 로 부르고(`Fig. 4b` 범례 `S/X (4a) · X/S (4d) · S (16e) · P (4b) · Li (24g,48h)`), **케이지 중심 = 4d** — **de Klerk 2016 의 `4c` ≡ 이 리뷰의 `4d`** 임이 `Fig. 4c`(LPSCl = "pathway cage **around Cl** position" / LPSI = "around **S** position")로 독립 확인됨. **Cl⁻ 167 pm ≈ S²⁻ 170 pm(3 pm 차) → 무질서 / Br 182(+12) → 무질서 / I 206(+36) → 질서(4a 전용, inter-cage 0)** (`Fig. 2a` 결정반경 + 본문-ref 115·131). 점프 3종(`Fig. 4d`) **doublet(48h–24g–48h) · intra-cage · inter-cage** 정의는 de Klerk 와 동일. **"all-Cl@4a → inter-cage 0 / all-Cl@4d → doublet 급락 / 최적 = 4a:4d = 1:3"** 를 확정 사실처럼 옮김(원 출처 **본문-ref 135 = de Klerk 2016 *Chem. Mater.* 28, 7955** — ✅ 우리 1차 digest 로 대조해 **정확히 옮겼음 확인**; ⚠ 단 **그 최적치가 방법 의존이라는 반론**(2024 MTP-MLIP 는 25 % 보고)은 **안 적었다**). **★2 Cl-과잉 기전(`Fig. 5a`)**: `과잉 할로겐 → 4d 무질서↑(1S3X 배열이 최고 점프율) → 4d 평균 음전하↓ → Li 재분포 → **24g 점유↑(전이상태 수명↑)** → inter-cage 거리 단축 → 고속전도`, 그리고 **"에너지 지형을 바꾸는 것이지 Li 결핍 때문이 아니다"** 를 명시(본문-ref **162 = Feng 2020 ESM 30, 67** · **138 = Wang P. 2020 Chem. Mater. 32, 3833**) ⇒ **우리 modelc 서사를 "vacancy↑" 로만 쓰면 문헌과 어긋난다**. 할로겐 고용한도는 "넘으면 잉여 LiX 로 σ↓" 라고만 하고 **수치 미제공**. **★5 `Table S1`(SI)** = 47행 σ/Ea/합성법 — **Li₆₋ₓPS₅₋ₓCl₁₊ₓ 계열이 x=0(6편)·0.25(1편)·0.5(5편)·0.7(1편)** 으로 실려 **우리 modelc(x=0.6)가 그 빈칸에 앉는다**; 대표값 Li₅.₅PS₄.₅Cl₁.₅ **6.41×10⁻³/Ea 0.261**(SI-21=본문-170 Yu 2020) · **9.4×10⁻³/0.29** cold-pressed(SI-26=본문-**155 Adeli 2019**, ✅우리 digest) · **9.03×10⁻³/0.27**(SI-27=본문-156 Peng 2022) · **1.02×10⁻²** cold-pressed(SI-28=본문-157 Jung 2020), Li₅.₃PS₄.₃Cl₁.₇ **~5×10⁻³(느린 승온) vs ~1.6×10⁻³(빠른 승온)**(SI-29=본문-158 Kitajima 2021), argyrodite 최고 **Li₅.₃PS₄.₃ClBr₀.₇ 2.4×10⁻²/Ea 0.155**(SI-32=본문-**164 Patel 2021**). 🔴 **이 표의 최대 소득은 값이 아니라 산포다**: **같은 조성(x=0.7)에서 승온속도만 바꿔 3.1×**, **Li₆PS₅Cl 문헌 Ea 산포 0.11–0.33 eV(3.0×)가 Cl-rich 로 얻는 ΔEa(≈0.035 eV)의 6배** ⇒ *"Cl-rich 가 σ 를 몇 배 올린다"* 는 **반드시 "같은 논문 안에서" 단서를 달아야** 한다. **★4 aliovalent 판정 — 이 리뷰는 "σ 를 올린다" 쪽**(p834 첫 문장 *"Aliovalent substitution of cations on the Li site or P site is often used to generate Li vacancies and increase the number of charge carriers"*): **Ca²⁺→Li 자리 Li₅.₃₅Ca₀.₁PS₄.₅Cl₁.₅₅ 1.02×10⁻²/0.30**(본문-**149 = Adeli/Nazar 2021 Chem. Mater. 33, 146**) · Al³⁺→Li 자리 Li₅.₄Al₀.₂PS₅Br 2.4×10⁻³(본문-**133 = Zhang Z. 2020 JPS 450, 227601**) · P 자리 Si/Ge 는 Li₆PS₅I 2.2×10⁻⁴ 대비 **5–25×↑**. ⚠ **우리 단서 3건**: ① Ca 계는 **Cl 1.55 와 교락**돼 순수 Cl-rich 와 구분 안 됨 ② 교락 없는 증거는 **I-쪽 P 자리**뿐 ③ 🔴 **리뷰 문장 자체에 기전 오류** — **P 자리 Si⁴⁺/Ge⁴⁺ 치환은 Li 를 *늘린다*(Li₆₊ₓ), 공공을 만들지 않는다** (우리 `li2024_inf3…` §14-⑱ 에서 잡은 것과 같은 종류의 오류). **σ 를 낮추는 사례로 리뷰가 든 것은 ① Li₃InBr₆ 의 aliovalent("ineffective", 본문-104–107, **할라이드지 argyrodite 아님**) ② F⁻→Cl⁻ 등가치환(Li₃InCl₄.₈F₁.₂ 1.37×10⁻³→5.1×10⁻⁴, 본문-112)** ⇒ **Liang 2026 의 "aliovalent 가 LPSC σ 를 낮춘다" 스니펫과 정면으로 갈린다 — 둘 다 2차 인용이므로 원전(Adeli 2021·Zhang 2020) 직접 확인 필요**. **★3 산화·수분**: 🔴 **ESW·산화 onset 수치 0건** — 근거가 `Fig. 2a` 표준환원전위(F 2.870 / Cl 1.358 / O 1.230 / Br 1.080 / I 0.536 / **S 0.142** V vs SHE; ⚠ 축 라벨이 **"eV" 로 오기**)와 정성 문장뿐; *"LiX 도핑이 ESW 를 넓힌다"* 는 **비교쌍이 LPS(무할로겐) vs LPSX** 로 **argyrodite 내부 Cl 1.0↔1.6 이 아니며**, 리뷰 스스로 *"확장된 ESW 가 고전압 양극에 못 미친다"* (본문-**167 = Yun 2023 ESM 59, 102787**, ✅우리 digest)로 되돌린다. **수분은 argyrodite 데이터 0건**(H₂S·RH 전무) — 다만 **F@Li₃InCl₆ 에서 "σ↓ + 수분보호↑"** 트레이드오프를 명시(본문-112)해 **Wang 2025 `Fig. S11`(O 도핑 σ −41 %)과 같은 모양의 패턴을 다른 화학에서 제공**(상충 아님, 침묵+간접지지). ★★ **본문-ref 154 = Li G. et al. *Adv. Funct. Mater.* 33, 2211805 (2022) `Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆`** = **Cl 1.6(우리 modelc 와 동일) + O 치환(우리 LPSOCl) 의 문헌 선례** — 최우선 획득 대상. **★6 계면(`Fig. 7c` vs `7d`)**: Li₃MX₆ = `Li₃MX₆+3Li→6LiX+M⁰` → **혼합 Li⁺/e⁻ 전도 계면 → 폭주** vs Li₆PS₅Cl = `→Li₁₁PS₅Cl→{Li₂S,LiCl,S}→{Li₃P,LiCl,Li₂S}` → **전자 차단(그림에 ✗) = 자기제한 SEI**; **Cl-rich 는 Li 금속 상용성도 좋다**(본문-**185 = Zeng 2022 Nat. Commun. 13, 1909**) 🔴 **단 같은 문단이 "과잉 Cl 의 다수는 격자가 아니라 입계 LiCl 나노쉘로 간다"** 고 적어 **우리 modelc(Cl 1.6 전량 격자 치환)를 "실험 시료의 모델" 로 부르면 안 됨을 못박는다** ⇒ *"the bulk-lattice limit of Cl incorporation"* 으로 서술. **★7 리뷰가 "모른다"고 적은 것 9건**(digest §12) 중 우리 것 둘: **G1** *"세 할로겐의 Li 공공 정도로는 수 자릿수 σ 차이를 설명 못 한다 — **원자 점유에서 더 파고들어야 한다**"* (= comp2 disorder ensemble 의 존재 이유) · **G4** *"**희토류 HSE 의 이온전도·구조안정성 연구는 아직 초기 단계**이고 서로 다른 희토류의 역할을 더 밝혀야 한다"* (= **ndo_lpscl16 (Nd) 의 gap 문장, 거의 원문 그대로 인용 가능**). **★8 SI 전용**: `Table S1` 이 이 리뷰의 정량 자료 **전부**이고, 🔴 **SI 는 자체 ref 번호(1–48)를 써 본문(1–203)과 충돌한다** (예: **18** = 본문 Peng 2023 리뷰 ↔ SI Rao&Adams 2011 / **26** = 본문 Li–I₂ flow ↔ SI Adeli 2019 / **32** = 본문 Na–I₂ ↔ SI Patel 2021) ⇒ **본문 번호로 Table S1 값을 인용하면 전혀 다른 논문을 인용하게 된다**; SI 에만 있고 본문에 없는 논문 **SI-36 = Kato 2016 Nat. Energy 1, 16030**. **🔴🔴 최대 결함 — 본문이 자기 SI 와 220× 어긋난다**: **본문 p832 *"Li₆PS₅I is only about 10⁻⁶ S cm⁻¹"*** ↔ **`Table S1` SI-18 = 2.2×10⁻⁴ S cm⁻¹**(본문의 "Cl·Br 10⁻²–10⁻³" 도 자기 표의 Li₆PS₅Cl 7.4×10⁻⁴ 를 벗어남). **argyrodite 절 전체의 출발 논증("several-orders-of-magnitude difference")이 그 10⁻⁶ 위에 서 있어** 결함이 핵심 주장에 걸린다 ⇒ **Li₆PS₅X σ 대비를 인용할 땐 `Table S1` 값만 쓰고 본문 서술은 버린다**(안전선 = "Cl/Br 대비 I 는 한 자릿수 이상 낮다"). **🔴 우리 비판 13건**(digest §17): 자체 데이터 0 · `Table S1` 압력 44행 미기재(`cronau2021` 대비 무효화) · ref 번호 이중체계 · **`Fig. 6` 은 성능 비교로 사용 불가**(양극 5종·음극 3종·셀당 점 1개 — 최고점 235 mAh/g 는 **TiS₂ 이론용량**이지 전해질 성능이 아니다) · `Fig. 2a` 축 단위 **V→eV 오기** · "1:3 최적" 의 방법 의존성 은폐 · aliovalent 기전 오류 · **산화안정성 절이 비어 S²⁻-pinning 논점과 대화 못 함** · 공기/수분 정량 0 · 기계적 물성 0("deformability" 만) · argyrodite 분량 부족(스스로 본문-**ref 18 = Peng et al. *Batteries & Supercaps* 6, e202200553 (2023) "Halogen-rich lithium argyrodite SEs: a review"** 를 가리킴 → 획득 권장) · `Fig. 4b` 범례 `S/X`·`X/S` 순서 규약 미설명. **그림 8장 전부 열람**(자동 크로퍼가 **Fig 1·3·7 을 통째로 누락**(캡션이 다음 쪽/측면) + **Fig 2·4·5 를 단 경계에서 절단**(Fig 4 는 a·b·c 패널 전멸) → **6장 손 재크롭 후 재열람**, `figures.json` 에 `curator_note` 기록; `Table S1` 은 PDF 텍스트를 좌표 복원해 전사). | **리뷰 · 할로겐 축 field-map · 자리표기(4a/4d) 정본 · Cl-rich 기전 도식 · 실험 σ/Ea 소환표 — ⛔ 값의 근거로 인용 금지** |

---

## ② `comparison_vs_ours.md` 에 추가할 블록 — **§J-7 형식의 `🔧 방법·개관 원전`**

> 약칭 제안: **[He23Hal]**
> ⛔⛔ **A(이온전도)·B(산화안정)·C(기계)·D(전자구조) 표에 행을 만들지 않는다.**
> 이 편에는 **우리 값과 대응하는 자체 측정·계산이 0건**이고, `Table S1` 은 조건 미기재 2차 인용표다.
> 행을 만들면 `n/a` 로 채워져 표가 무의미해진다. **아래는 "우리가 쓰는 말과 프레임의 원본"** 이다.
>
> 📑 Reference key 에 추가할 줄(요약형):
> **[He23Hal]** | He/Zhang/**Xin\***/Xu/Hu/Wu/**Yang\***/**Tian\*** 2023 ***Nat. Rev. Chem.* 7, 826–842**(NCEPU + UCF; DOI 10.1038/s41570-023-00541-7) — "**Halogen chemistry of solid electrolytes in ASSBs**". **자체 계산·실험 0 → 전 수치가 소환값**. 산출물 = **①할로겐 축 연표(1923–2021, `Fig. 1`)** · **②argyrodite 자리표기 4a/4d + 점프 3종 정본(`Fig. 4b–d`)** · **③Cl-과잉 기전 도식(`Fig. 5a`)** · **④`Table S1` 47행 σ/Ea 소환표(SI)**. ⚠ **본문 ref(1–203) ≠ SI ref(1–48)** · ESW·산화 onset·수분·기계 수치 **0건** | ✅ `papers/he2023_halogen_chemistry_solid_electrolytes.md` | **review · 프레임·용어 전용 — 물성 4축 *수치* 비교 제외**

**[He23Hal] `he2023_halogen_chemistry_solid_electrolytes` — 우리가 쓰는 argyrodite 용어·프레임의 표준 서술**

| 항목 | [He23Hal] 의 정의/서술 | 우리 | 판정 |
|---|---|---|---|
| **free-anion 자리 표기** | **4a / 4d**, **케이지 중심 = 4d** (`Fig. 4b` 범례 + `Fig. 4c`) | 우리·`deklerk2016` digest = **4a / 4c(=4d)** | ✅ **매핑 확정.** 원고·발표는 **4a/4d 로 통일**(Nat. Rev./Kraft/Wang P. 관례). ⛔ 한 문장에 4c 와 4d 를 섞지 말 것 |
| **점프 3종 정의** | **doublet(48h–24g–48h) · intra-cage(48h–48h) · inter-cage(48h–48h)**, inter-cage 가 거시 수송 지배 (`Fig. 4d`, 본문-refs 132–134) | 동일 정의(de Klerk 계보) | ✅ 용어 일치 — 우리 MSD/점프 분석의 표준 어휘로 채택 |
| **무질서 → 수송 on/off** | all-Cl@4a → inter-cage **0** / all-Cl@4d → doublet 급락 / 최적 **4a:4d = 1:3** (본문-ref 135) | comp2 ordered(d=0) frozen 아티팩트가 같은 물리; disorder ensemble d-level 스캔 | ✅✅ **우리 comp2 설계의 문헌 프레임.** ⚠ **"최적 %" 숫자는 인용 금지** — 원전은 분포당 단일 배열·단위셀·100 ps 이고 2024 MTP-MLIP 재검은 25 % 를 보고한다. 안전 인용 = *"중간 무질서에 최적이 존재(양 끝은 나쁘다)"* |
| **Cl-rich 가 빠른 이유** | **에너지 지형(무질서·4d 음전하↓·24g 점유↑)** — *"not caused by Li deficiency"* (본문-refs 138·162) | 우리는 지금 **disorder + vacancy** 로 서술 | ⚠ **서사 교정 권고**: "무질서가 주, vacancy 는 동반" 으로. 문헌 표준은 vacancy 설명을 **명시적으로 배제**한다 |
| **Cl/S 무질서의 구조적 근거** | **Cl⁻ 167 pm vs S²⁻ 170 pm (3 pm)** / Br +12 / I +36 pm (`Fig. 2a`) | 우리 comp1·modelc 의 S/Cl 자리교환 decorate | ✅ **한 줄 근거 확보** (⚠ Shannon 반경 — 리뷰가 출처를 안 밝힘) |
| **24g 점유율** | `Fig. 5a` 가 **σ 의 중간 지표로 명시** | 미측정 | ⭕ **이식 후보 (T1)** — UMA 궤적에서 싸게 뽑히는 양. **문헌 기전을 우리 데이터로 직접 시험** |
| **산화 onset** | **수치 0건.** 정성 서술의 비교쌍은 **LPS vs LPSX**(argyrodite 내부 Cl 1.0↔1.6 아님) | comp1·modelc **동일 2.256 V (S²⁻-limited)** | 🔴 **표면상 상충 — 실제로는 다른 비교쌍.** 섞지 말 것. 우리 편은 **[Banik]**(S 가 VBM pin)이 지지하고, 리뷰 스스로 본문-ref 167(=**[Yun23]**)로 ESW 확장 주장을 되돌린다 |
| **수분/공기** | argyrodite 정량 **0건**. F@Li₃InCl₆ 의 **σ↓ + 수분보호↑** 사례만(본문-112) | LPSOCl / +B₂O₃ 축 | ⚠ **[Wang25DPA] `Fig. S11`(O 도핑 σ −41 %)과 상충하지 않지만 지지도 안 한다.** 같은 *모양*의 트레이드오프를 다른 화학에서 제공 ⇒ **간접 지지**. 근거로 쓸 것은 **본문-ref 154(Li G. 2022 AFM, `Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆`)** |
| **Li 금속 계면** | `Fig. 7d` `Li₆PS₅Cl→Li₁₁PS₅Cl→{Li₂S,LiCl,S}→{Li₃P,LiCl,Li₂S}` + **전자 차단(자기제한)** vs `Fig. 7c` Li₃MX₆ **혼합전도 폭주** | grand-potential 환원한계 1.242 V / OCV 1.717 V | ✅ **정성 정합**(산물 계열 동일). ⛔ 전압 대 전압 비교 불가(리뷰에 수치 없음) |
| **modelc 의 물리적 정체** | 본문-ref 185(Zeng 2022): **과잉 Cl 의 다수는 입계 LiCl 나노쉘**, 격자 치환은 소수 | modelc = Cl 1.6 **전량 격자 치환** 단결정 셀 | 🔴 **모델 한계 명시 의무.** *"실험 Cl-rich 시료의 모델"* ❌ → *"a fully lattice-substituted Cl-rich model / the bulk-lattice limit"* ⭕ |
| **희토류 도핑** | *"still at an early stage … roles of the different rare earths need to be further explored"* (p838) | `ndo_lpscl16`(Nd·O) | ✅ **우리 gap 문장의 외부 근거.** 원고 서론에 거의 원문 인용 가능 |
| 밴드갭 / 기계 | **0건 / 0건**("deformability" 정성) | comp1 2.066 · modelc 2.099 eV / E_VRH 22.06→27.66 GPa | **n/a — 비교 대상 없음** |

**⛔ [He23Hal] 에서 우리 쪽으로 옮기면 안 되는 것**
1. **`Table S1` 의 σ·Ea 값 전부** — 압력 44행 미기재, 조건 미상. **ML 학습 라벨로도 금지.**
2. **"4a:4d = 1:3 최적"의 숫자** — 방법 의존(2024 MTP-MLIP 는 25 %). 정성 문장까지만.
3. **`Fig. 6` 의 어떤 점도** — 양극·음극·로딩이 전부 다른 14개 셀. 전해질 순위를 말할 수 없다.
4. **"할로겐이 ESW 를 넓힌다"** 를 **argyrodite 내부 Cl 조성 효과로 옮기는 것** — 비교쌍이 다르다.
5. **본문 ref 번호로 `Table S1` 값을 인용하는 것** — SI 는 별도 번호 체계다.
6. 🔴 **본문 p832 의 "Li₆PS₅I ≈ 10⁻⁶ S cm⁻¹"** — 자기 `Table S1`(2.2×10⁻⁴)과 **220× 모순**.
   Li₆PS₅X 의 σ 대비가 필요하면 **`Table S1` 값만** 쓰고, **기전은 `deklerk2016`(all-4a → inter-cage 0)로** 인용한다.

---

## ③ 후속 획득 목록 (원전 확인 — 우리가 아직 원문을 안 봤다)

| 순위 | 논문 | 왜 |
|---|---|---|
| **1** | **Adeli, Bazak, Huq, Goward, Nazar, *Chem. Mater.* 33, 146 (2021)** (본문-149) + **Zhang Z. et al., *J. Power Sources* 450, 227601 (2020)** (본문-133) | **aliovalent 도핑 σ 방향 판정** — He 2023 ↔ Liang 2026 충돌의 원전. 우리 cascade site-rule 에 직결 |
| **2** | **Feng X. et al., *Energy Storage Mater.* 30, 67 (2020)** (본문-162) + **Wang P. et al., *Chem. Mater.* 32, 3833 (2020)** (본문-138) | **"Cl-rich 는 vacancy 가 아니라 무질서" + 1S3X 기전** — 우리 modelc 서사의 심장 |
| **3** | **Li G. et al., *Adv. Funct. Mater.* 33, 2211805 (2022)** (본문-154) | `Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆` = **Cl 1.6 + O 치환** = 우리 modelc+LPSOCl 의 문헌 선례 |
| 4 | **Zeng D. et al., *Nat. Commun.* 13, 1909 (2022)** (본문-185, OA) | "과잉 Cl 의 다수는 입계 LiCl" — 우리 모델 한계 선언의 근거 |
| 5 | **Peng, Yu, Cheng & Xie, *Batteries & Supercaps* 6, e202200553 (2023)** (본문-18) | **halogen-rich argyrodite 전용 리뷰** — He 2023 의 argyrodite 절이 얇은 것을 채운다 |
| 6 | **Patel S. V. et al., *Chem. Mater.* 33, 1435 (2021)** (본문-164 / SI-32) | argyrodite σ 기록값 `Li₅.₃PS₄.₃ClBr₀.₇ 2.4×10⁻² S/cm, Ea 0.155 eV` 의 원전 |
