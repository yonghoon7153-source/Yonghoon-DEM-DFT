---
title: "Bielefeld, Weber, Rueß, Glavas, Janek 2022 — Influence of Lithium Ion Kinetics, Particle Morphology and Voids on the Electrochemical Performance of Composite Cathodes for All-Solid-State Batteries (J. Electrochem. Soc. 169, 020539)"
source_url: local-upload/18._Influence_of_lithium_ion_kinetics_particle_morphology_and_voids_on_the_electrochemical_performance_of_composite_cathodes_for_all-solid-state_batteries.pdf + 18._Sup_Influence_of_lithium_ion_kinetics_particle_morphology_and_voids_on_the_electrochemical_performance_of_composite_cathodes_for_all-solid-state_batteries.pdf (SI)
source_url_note: "본문 14 쪽(IOP 내려받기 표지 1 + 본문 13 · 그림 11 · 표 1 · 참고문헌 67) + SI 15 쪽(LaTeX · Fig. S1-S8 · 표 S1-S3). FEM 모델 편 — 새 측정 0. 크로퍼 자동 17 장 + SI 벡터 그림 2 장(Fig. S2 · S7) 300 dpi 수동 크롭. Read 11 장 + SI S5 쪽 렌더, 안 본 것은 digest §14. 원자료는 커밋하지 않는다."
source_doi: 10.1149/1945-7111/ac50df
source_license: "© 2022 The Electrochemical Society (ECS), published by IOP Publishing — 오픈액세스 표기 없음"
pdf_sha256: 51cd41d5d463e40ea2f2c0692fefd3374027f4df3b6b34b9f302c75608690fc4
si_sha256: a9f31c93e310d4f5442c7e0f248bac7fc5248eda4b144d9c592e3f6729faacee
ingested: 2026-09-23
sha256: c3a826612123d278aa8772782346cda73060257158dc5a0d950d3eae2e79ee6f
---

# 수집 목적

`assb` 섹션 **56호**. 큐 **57번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열여덟째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행 ★★: "pore(void) 문턱 → 1호 `p_c` 와 이어짐" — 원장 정정 이미 있음: "**실험판이 아니라 FEM 시뮬레이션**(1호 Bielefeld 2019 모델의 후속 — void 를 넣은 미세구조 모델)". 지목 **4 회**: 02호 Clausnitzer 2023 ref 36(NMC811 `U₀` 의 출처) · 14호 Oh 2025 *Maxwell* ref [69]("abrupt resistance increase when the pore volume … surpasses a threshold" 의 근거) · 50호 Miß 2022 ref 35(`j₀` "in the range of 10⁻⁵ A cm⁻²") · 53호 Ren 2023 ref [203](입도 분포 · 농도 의존 동역학 한 문장).

이 digest 의 1순위 물음: **(1) void 를 어느 자리로 넣었나 — CAM–SE 접촉 면적(`φ`, 37호 `A_eff`)인가, 이온 경로(`ε/τ`)인가, 둘 다인가 · 둘을 갈랐나 (2) void 분율 스윕에 따른 활성 면적 · 과전압 · 용량 — 01호 `p_c` 의 void 판인가 · `θ(N)` 이 있는가 (3) 교환전류밀도 `j₀` 입력의 출처와 면적 규약(50호 대조) (4) 모델을 무엇과 대조했나 · 55호 Hlushkou 실측(void 13.2 % · `τ` 1.27/1.74 · `k_SE` 1.54 · LCO/SE 0.616)과의 관계 (5) void 스윕을 ASSB 합성 truth 에서 `θ`-전용 조작으로 쓸 수 있나(37호 다섯 조건).**

A. Bielefeld*, D. A. Weber, R. Rueß, V. Glavas, J. Janek* (5 인, * 교신 2) —
**"Influence of Lithium Ion Kinetics, Particle Morphology and Voids on the Electrochemical Performance of Composite Cathodes for All-Solid-State Batteries"**,
*J. Electrochem. Soc.* **2022**, **169**, 020539, doi `10.1149/1945-7111/ac50df`.
`[인쇄]` Manuscript submitted 2021-12-02 · revised 2022-01-05 · Published 2022-02-16 · "© 2022 The Electrochemical Society ("ECS"). Published on behalf of ECS by IOP Publishing Limited" — 오픈액세스 표기 없음.
소속: **JLU Giessen 물리화학연구소 + LaMa**(Bielefeld · Rueß · Janek) · **Volkswagen AG, Wolfsburg**(Weber · Glavas). 자금: `[인쇄]` "The authors thank the **Volkswagen AG** for the financial support" · BMBF FESTBATT(03XP0177A) · ProFeLi(03XP0184C) 논의.
**계보 겹침**: 01호(Bielefeld · Weber · Janek 2019 *J. Phys. Chem. C*)와 **제1 · 2 · 교신 저자 셋이 같다** — 이 편 ref 24 · SI ref 3. 큐 58(Bielefeld · Weber · Janek 2020 *ACS AMI* 12, 12821)은 이 편 ref 25 · SI ref 6. 3저자 **Rueß** 는 모든 입력의 출처인 Ruess 2020 *JES* 167, 100532(ref 10)의 제1저자이고, 38호 Conforto 2021(ref 47 — PSD 의 출처)의 2저자다. 23호 Koerver 2017 = ref 8(Fig. 2 SEM 차용). 55호 Hlushkou 2018 = ref 56. 큐 59(Asheri 2023)는 이 편보다 늦다(인용 0).

본문 PDF **14 쪽**(IOP 표지 1 + 본문 13 · 그림 11 · 표 1 · 참고문헌 67) · SI PDF **15 쪽**(LaTeX · Fig. S1–S8 · 표 S1–S3 · 참고문헌 7). PDF sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). ⚠ 본문 PDF 는 IOP 내려받기 표지가 붙은 판(표지에 내려받기 날짜 2026-09-23 인쇄) — 같은 논문의 다른 내려받기와 해시가 다를 수 있다. 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ **이 편은 모델(FEM) 편이다.** 아래 "void 가 과전압을 X mV 올린다" 류의 문장은 전부 **모델 명제**다 — 실측이 아니다. 실험은 남의(Rueß 2020) 충전 곡선 3 율뿐이고 이 편은 새 측정을 하지 않았다.
> ⚠ **기호**: 이 편의 `A` 는 **CAM/SE 계면 중 void 가 덮지 않은 면적의 백분율**(Fig. 8 가로축 "A/%" — 신품 입자 표면적 기준)이다. 카드의 `φ`(표면 피복 분율, 29 · 39호)와 **같은 양**이고, 37호 `A_eff` 의 자리다. 굴곡도 `τ` 는 이 편에 **값으로 한 번도 나오지 않는다**.

---

# 판정 (먼저)

> ★★★★ **void 를 넣은 자리 — 접촉 면적(`φ`)만이다. 경로 효과는 구성상 0 이고, 검증 모델에서는 void 자체가 0 이다.**
>
> | 기하 모델 | void 의 자리 | 경로(`ε/τ`) | 접촉(`φ`) | 연결(`θ`) |
> |---|---|---|---|---|
> | **입자형 재구성**(검증 · PSD · `D̃`/`j₀` 연구) | **없다** — `[인쇄]` "the SE is assumed to be in ideal contact, filling all remaining volume". 실험 전극의 void **14 %** 는 SE 로 채워졌다(CAM 42 vol% 고정 → SE 58 vol%, 실물 `[재현]` 44 %) | void 없음 — SE 연속 기질 · `τ` 미계산 | 1(이상 접촉) | **강제로 1** — SI: `[인쇄]` "electronic percolation will not be achieved for randomly distributed spherical particles at this volume fraction [**01호**]" ⇒ placeholder 트릭 + "isolated particles … **moved manually**" |
> | **1-입자-void**(void 연구) | **CAM 표면의 반구** — 무작위 위치 · 크기 · 피복률 지정 | 구성상 0 — `[인쇄]` "this model approach is **not capable to quantify** the influence of voids … on ionic percolation, as we are focusing on the role of the active surface area and one CAM particle only". SE 는 균일 상자(미세구조 비해상) | **스윕한 양** — 100 → ≈52 %(7 µm) | 입자 하나, 집전체에 붙임 — 1 |
> | **원뿔형 구조화 전극** | 없다 — `[인쇄]` "the model also does not feature voids" | 굴곡도를 "disable" 하는 기하 | 1 | 1 |
>
> ⇒ **void 의 두 효과(경로 ↔ 접촉)를 갈랐나: 아니다.** 한 모델은 둘 다 지우고(검증), 다른 모델은 접촉만 남긴다(void 연구). 두 효과를 **한 구조에서 같이** 계산한 표본은 이 편에도 없다 — 55호(경로만)와 이 편(접촉만)이 **서로의 빈 칸**이다(55호와 01호의 관계가 되풀이된다).
>
> ★★★★ **원장 · 14호의 "pore 문턱 → 저항 급증" 은 이 편에 없다.** `threshold` **0** · `surpass` **0** · `abrupt` 1(= "the lithium concentration gradient in the particle is comparably abrupt" — 큰 void 아래 입자 내부 농도 구배) · `resistance` 4(전부 일반론 · 공간전하층 · `R_CT` 정의 · 충/방 비대칭). **void 부피분율 스윕 자체가 없다** — 스윕한 것은 한 입자의 **피복률**(`A`)과 **void 크기**다. ⇒ 14호 ref [69] 의 귀속은 이 편에서 확인되지 않는다(`[해석]` 58호 Bielefeld 2020 또는 01호일 가능성 — 큐 58 에서 확인). 원장의 "`p_c` 와 이어짐" 도 뒤집어 읽어야 한다: 이 편이 01호 `p_c` 와 닿는 유일한 자리는 **"01호 모델대로면 42 vol% 에서 전자 퍼콜레이션이 안 되는데 실험 셀은 된다 → 그래서 퍼콜레이션을 손으로 강제했다"** 는 SI 한 단락이다(`[재현]` 01호 식 (8) `p_c(5 µm)` = 49.3 vol% · `p_c(d)` = 42 vol% 는 d ≈2.0 µm).
>
> ★★★★ **`j₀` 는 FEM 의 출력이 아니라 입력이다 — 출처는 Rueß 2020 의 EIS `R_CT`, 면적 `A` 미정의.** Table S2 `[인쇄]` `j₀` "see figure 7a) … **calculated from `R_CT`** Rueß et al. (equation 12)" · 식 (12) `R_CT = RT/(zFAj₀)` — **`A` 가 무엇인지(기하 전극 면적 · BET · 모델 CAM 면적) 지면에 없다.** 모델은 그 `j₀` 를 **모델 CAM/SE 계면**(0.17 m² g⁻¹, 전극 단면의 `[재현]` ≈13.6 배)에 건다(SI Fig. S3 경계 조건). 그리고 `[인쇄]` "**none of the simulation input has been fitted** to meet the experimental data". ⇒ 50호가 인쇄한 "Bielefeld 2022 … 10⁻⁵ A cm⁻²"(= 0.1 A m⁻² ↔ Miß NMC 0.11)는 **Rueß EIS 값의 재인용**이고 FEM 이 독립으로 낸 값이 아니다. 실접촉 면적을 썼는지는 **판정 불가** — `[재현]` 규약에 따라 `j₀,1` 1.55 × 10⁻⁵ A cm⁻² 이 가리키는 기하 ASR 은 ≈112 Ω cm²(모델 CAM 면적 기준) ↔ ≈1520 Ω cm²(`A` = 기하 면적이었다면) — **자릿수 하나 차이**, Rueß 2020 의 `R_CT` 로 가를 수 있다(큐 밖 후속 1순위).
>
> ★★★ **실험 대조 — 남의 충전 곡선 3 율(0.02 · 0.1 · 0.5 C, 첫 충전)과, 오차 척도 없이.** "good agreement" · RMSE · 잔차 0(`error` 0). `[도표]` Fig. 4: 0.5 C 컷오프 용량 모의 ≈103–106 ↔ 실험 ≈115 mAh g⁻¹ · 0.02 C 모의 ≈188 ↔ 실험 ≈197. **"적합 없음" 선언과 선택형 조정이 공존한다**: (i) PSD 는 Conforto(38호) EIS-PSD 를 "modified"(Table S3) — 11 · 14 · 20 µm 로 자른 셋 중 **실험에 맞는 S(≤ 11 µm)** 를 이후 모든 계산에 썼다 (ii) 고립 CAM 입자를 첫 충전 모의로 찾아 **손으로 옮겼다** (iii) `D̃`/`j₀` 는 SOC 의존 세트를 썼는데, **본문이 "best" 라고 쓴 것은 상수 세트**(Fig. 7d `{D̃_Li,2, j₀,1}`)다 — 선택 근거는 `[인쇄]` "the best and physically correct choice".
>
> ★★★ **55호 대조 표적과의 관계 — 같은 양이 하나도 없다.** void 13.2 %(55호, 수지 + void) ↔ 이 편 실험 전극 14 %(Rueß, 인용값) · 검증 모델 **0 %** · void 모델은 **부피가 아니라 피복률**. `τ` 1.27/1.74 ↔ 이 편 `τ` **미계산**(`tortuos*` 7 회 전부 서론 · 구조화 논의). `k_SE` 1.54(SE 현 길이 분포) ↔ 이 편 SE 는 **비해상 연속 채움**(`[해석]` 55호 "SE 는 입자가 아니라 연속 기질" 과 정성적으로는 같은 그림이지만, 모양 인자는 없다). LCO/SE 0.616 ↔ 이 편 NCM/SE 부피비 **모델 0.724 · 실물 `[재현]` 0.955**. ⇒ 55호 수치는 이 편의 **검증 모델이 "void → SE 가상 치환" 상태**라는 것을 말해 준다: 55호에서 그 치환은 `ε/τ` 를 ×1.71 좋게 만들었다(다른 계라 크기는 옮기지 않는다) — 이 편의 검증은 **경로가 실물보다 좋은 모델로** 한 것이다. 이 편은 55호(ref 56)를 **공극률 13 % 의 출처**로만 인용한다(55호 D7 "void = 수지 + void" 가 그대로 넘어온다).
>
> ★★★ **`θ(N)` 0 — 정적 구조, 첫 충전 한 번.** "void 가 클수록 부피 변화에 의한 접촉 손실" 은 **해석 문장**(`[인쇄]` "The larger voids can be interpreted as partial contact loss … resulting from NCM particle shrinkage upon delithiation")이고 시간 · 사이클 축은 없다. Fig. 2 오른쪽 SEM(미사이클 · 1 회 충전 · 50 사이클)은 23호 Koerver 2017 에서 **차용한 사진**이고 정량 0.
>
> ★★★ **void 스윕은 `θ`-전용 조작이 아니다 — `φ` 조작이고, 그것도 `φ` 하나로 요약되지 않는다(모델 명제).** (a) 저율에서 안 보인다 — `[도표]` Fig. 8 0.02 C 피복 손실 48 % 에 void 과전압 ≤ ≈7 mV · 4.2 V 도달 용량 ≈193 → ≈188 mAh g⁻¹(−3 %) (b) 고율에서 **용량 손실처럼** 보인다 — 0.5 C ≈107 → ≈80 mAh g⁻¹(−25 %) (c) ★ **같은 `φ`(70 %)에서 void 크기만 바꿔도 과전압이 ×2.6–4.5** — `[도표]` Fig. 9 0.2 C @50 ≈19 → ≈50 mV · @100 ≈14.5 → ≈65 mV(`d_CAM/d_Void` 10 → 1.2). `[재현]` 피복을 BV 분모의 면적 축소로만 넣으면(37호 `A_eff ↔ k` 항등의 형) 0.2 C @50 · `A` 53 % 에서 **≈21 mV** — `[도표]` 47 mV 의 **절반 이하**이고, 나머지는 입자 내부 확산의 공간 불균일(`[인쇄]` "many uniformly distributed voids can partly compensate the local inactive surface area by lithium diffusion inside the CAM particle"). ⇒ 3D 해상 모델에서는 표면 피복이 **`j₀` 의 정확한 쌍둥이가 아니다** — 분포가 두 번째 손잡이다. 37호 다섯 조건은 (i) · (ii) · (iv) · (v) ❌, (iii) 부분(§9).
>
> **채움표: ≈20.0 → ≈20.0 (새 칸 0).** Q1 **층 하나** — "피복률 `φ` 의 모델 스윕 · `φ` 고정에서 분포가 과전압을 ×2.6–4.5" (모델 명제라 칸을 움직이지 않는다 · `θ(N)` 0/56 · `θ` 는 손으로 1) · Q2 없음 · **Q3 층 하나** — "비적합 선언 + 선택형 조정(PSD 절단 · 수작업 연결 · 세트 선택) + `j₀` 면적 미정의" · **Q4 0/56 — 마흔여덟 번째 성질 "비유일성을 그림으로 보이고(상수 세트가 SOC 의존 세트보다 잘 맞는다) '물리적으로 옳다' 로 골랐다 — `j₀` 적합을 'Achilles heel' 로 경고했지만 식별성은 재지 않았다"** · Q5 해당 없음(Li 금속 대극 모델, `j₀ᵃ` 3 A cm⁻²) · Q6 없음(`MPa` 0 · `pressure` 1 추측문) · Q7 해당 없음 · Q8 층 하나(NCM811 OCV Fig. S2 — **02호 `U₀` 의 경유지, 원전은 Rueß 2020**). 곱 축퇴 처방 **서른아홉 번째 적용**(§10) — 새 줄 "**`φ` 고정 분포 스윕 — 3D 모델에서 `A_eff ↔ k` 항등의 파괴 검사**".

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 없는 것 | 왜 필요한가 |
|---|---|---|
| G1 | **식 (12) 의 `A`** — `R_CT` 에서 `j₀` 를 계산할 때 쓴 면적(기하 · BET · 모델 CAM 면적 · 접촉 보정) | 50호 대조("실접촉 면적을 썼나")의 답이 여기에 있다. `[재현]` 규약 차 ≈×13.6(모델 CAM 면적 ↔ 전극 단면) |
| G2 | **Rueß 2020 의 원자료 값**(`R_CT(V)` · `D̃(V)` 의 수치 · 온도 · 셀 압력) | `j₀(V)` · `D̃(V)` 곡선이 그림(Fig. 7a)으로만 있다 — 입력의 층위(GITT 인가 EIS 인가, 두 전극 스펙트럼의 음극 몫)를 원전에서 확인해야 한다 |
| G3 | **온도** — Table S2 `[인쇄]` `T` = **273.15 K**(0 °C). 실험 온도는 이 편에 없다 | 0 °C 가 오기면 `RT/F` 9 % · 식 (12) 의 `j₀` 도 같은 비로 움직인다(D1) |
| G4 | **SE 밀도** — 70/30 wt% + void 14 % → CAM 42 vol% 의 환산 | `[재현]` 42 % 는 `ρ_SE` ≈1.95 g cm⁻³ 를 요구한다(`ρ_NCM811` 4.77 은 인쇄). 지면에 없다 |
| G5 | **void 경계 조건** — 1-입자 모델의 void 표면(CAM–void · SE–void)에 무엇을 걸었나 | SI Fig. S3 경계표에 void 가 없다. `[해석]` COMSOL 기본(무플럭스 · 절연)으로 보인다 — 그러면 void = 반응 면적 0 + SE 부피 소량 제거 |
| G6 | **1-입자 모델의 C-율 정의** — 입자 하나의 용량(200 mAh g⁻¹)인가 | 과전압 대 전류밀도 환산의 전제. 아래 `[재현]` 은 입자 용량 × 200 mAh g⁻¹ 로 가정 |
| G7 | **void 부피분율 ↔ 피복률 대응** | 이 편 void 는 피복률로만 정의된다. 55호 13.2 % · 실험 14 % 와 같은 축에 놓으려면 이 대응이 필요하다 |
| G8 | **정량 오차 척도**(RMSE · 잔차 · 세 무작위 배열의 분산) | "good agreement" · "very similar" 뿐이다 |
| G9 | **0.2 C 실험 곡선** | 모의는 0.02 · 0.1 · 0.2 · 0.5 C, 실험은 0.02 · 0.1 · 0.5 C 만(Fig. 4 · 5 · 7 범례). 0.2 C 는 대조 없이 모의만 있다 |
| G10 | **PSD 원본과 "modified" 의 내용** | Table S3 `[인쇄]` "Conforto et al. (modified, see results section)" — 결과 절은 11 · 14 · 20 µm 상한만 준다. 원 분포 · 절단 방식 미인쇄 |

---

# 1. 서지 · 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전, IOP 표지 쪽 제외 · 바닥글 "All rights … reserved" 줄 제외); SI 는 괄호(참고문헌 전).

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** (SI 0) | **1** (SI 0) | **0** | 0 | 0 | **0** | 0 | **0** | 0 | **5** (SI 0) | **0** (SI 0) |

- NFKC 변경 본문 **161 자**(`ﬁ` 102 · `ﬂ` 23 · `˜` 36 — 물결 결합 부호 `D̃`) · SI **129 자**(`µ` 52 · `ﬁ` 34 · `˜` 22 · `ﬀ` 12 · `ﬃ` 3 · `¨` 3 · `ﬂ` 2 · `ϕ` 1) — **열 변화 0**. 소프트 하이픈 0 · 줄끝 하이픈 본문 41 곳 · SI 4 곳(이으면 `void*` 88 → 87 · `interface area` 16 → 17 — 열 변화 0).
- ⚠ IOP 조판 추출은 양쪽 정렬 줄을 **낱말 하나씩 줄바꿈**하고 식 (1)–(12)를 글자 조각으로 흩는다 — 공백 정규화 뒤 셌고 식은 SI Fig. S3(식 요약표)으로 확인했다. SI(LaTeX)는 `ﬀ` · `ﬁ` 합자가 NFKC 대상 문자로 남는다(글리프 탈락 없음).
- `uncertaint` 1 = **Conforto EIS-PSD 의 측정 불확실성**("the measurement uncertainty in the EIS-based technique increases for higher CAM particle sizes") — 이 편 결과의 불확실성이 아니다.
- `contact loss` 5 = 초록 1 · void 해석 2 · "upper boundary … whole SE particles that are disconnected" 1 · 결론 권고 1 — **전부 해석 · 권고 문장**, 정량 0.
- 보조(본문 / SI): `void*` **88 / 17** · `surface area` 22 / 0 · `interface area` 16 / 0 · `active surface` 10 · `active interface` 9 · `contact` 12 / 1 · `percolat*` **2 / 6**(본문 = 전자 퍼콜레이션 "does not show major issues" 1 · 이온 퍼콜레이션 "not capable to quantify" 1; SI = 강제 퍼콜레이션 단락) · `isolat*` 0 / 1 · `manual*` **0 / 2**(고립 입자 이동 · 주기 경계 메싱) · `tortuos*` 7 / 0 · `porosit*` 4 · `threshold` **0 / 0** · `surpass` **0** · `abrupt` 1(농도 구배) · `fit*` 2(`fitted` 1 = "none … has been fitted" · 1 = "the often performed fitting of j0 … should be rethought and used with caution") · `sensitiv*` 1 · `Achilles` 1 · `caution` 1 · `inaccurate` 1 · `scatter*` 1 · `reproduc*` 7 · `agreement` 2 · `error` **0** · `assum*` 12 / 1 · `exchange current` 21 / 4 · `RCT` 1 / 1 · `BET` 1 · `temperature` 1 / 2 · `273` 0 / 1 · `cycl*` 4 · `degrad*` 5 · `crack*` 3 · `shrink*` 1 · `pressure` 1("assuming that the SE becomes more compact upon cycling due to external pressure") · `Bruggeman` 0 · `utiliz*` 1(서론) · `LAM` 구절("loss of active material") 0 · `uniqu*` 0 · `Hlushkou` 0(번호 인용 [56] 만).
- `[해석]` 식별성 낱말 자리를 **"Achilles heel" · "used with caution" · "not straightforward to estimate whether these two effects might compensate each other"** 가 차지한다 — 비식별을 **경고문으로** 인쇄한 계보(49 · 53 · 54호의 "unfeasible" 류에 이어), 재지는 않는다.

---

# 2. 모델 (§Model, SI Fig. S3 · Table S1–S2)

- **지배식** `[인쇄]`: 몰 플럭스 식 (1) 확산 + 이동; SE = **단일 이온 옴 도체** 식 (4) `j = σ_ion^SE ∇φ`(농도 구배 0 — 대이온 없음; 공간전하층 무시, "order of nanometers … not significant", ref 39). CAM(NCM811) = 이온은 확산만 식 (5)–(6) `∂c/∂t + ∇·(D̃ ∇c) = R_I`, 전자는 옴 식 (7). 전자 전도를 크게 잡아(`σ_eon^CAM` 100 S m⁻¹, Table S2) 전자 · 이온 식을 떼었다 — `[인쇄]` "We accordingly loose the ability to quantify electronic limitations as reported by Neumann et al."(ref 38 — Neumann 2020 *ACS AMI*, NCM622/β-Li₃PS₄ CT 재구성).
- **계면**: CAM/SE · Li/SE 모두 Butler–Volmer 식 (8)(`α` = 0.5 둘 다). 과전압 식 (9) `η = (φ_CAM − φ_SE) − E_eq`. `j₀` 의 농도 의존 식 (11)(ref 42 · 43 — Schönleber 2017 · Weiss 2021): `j₀ ∝ k_ex^α k_in^(1−α) c_Li+^α c_e^α c_V^α c_LiI^(1−α)` 형(`c_Li+` · `c_e` 는 상수로 둠) ⇒ `[인쇄]` "expected to exhibit a **negative parabolic shape** with a maximum at an intermediate lithiation degree". 그러나 **모델은 식 (11) 을 쓰지 않고 측정 `j₀(V)` 를 그대로 넣는다**(Table S2 "see figure 7a) … calculated from `R_CT`").
- 식 (12) `[인쇄]` `R_CT = RT/(zFAj₀)` — `A` 정의 없음(G1).
- 음극: Li 금속, `j₀ᵃ` = **3 A cm⁻²**(Rueß) · SOC 무관 — "high".
- **파라미터 표**(Table S2 `[인쇄]`): `σ_Li^SE` **0.7 mS cm⁻¹**(Rueß) · 분리막 `l_SE` 10 µm · 양극 두께 `l_c` **40 µm** · `c_spec` 200 mAh g⁻¹ · `ρ_NCM811` 4.77 g cm⁻³ · `c_Li,ref` 49 mol l⁻¹(`[재현]` = 275 mAh g⁻¹, 완전 리튬화 기준) · `σ^CC` 300 S m⁻¹ · **`T` 273.15 K** · 컷오프 3.5–4.2 V · 시간 간격 0.01/C(≤ 4.0 V) · 0.001/C(> 4.0 V). 인가 전류는 0.1 s 매끈한 계단(Fig. S1).
- OCV = Fig. S2(`[도표]` `x` 0.22–1.0, 4.22 → 3.59 V, `x` ≈0.97 아래 급강하) — Rueß 출처. ⇒ **02호 Clausnitzer 2023 이 "ref 36 Bielefeld 2022" 로 가져온 NMC811 `U₀` 의 경유지가 이 그림이고, 원전은 Rueß 2020 이다**(Q8 층).
- 용량성 요소(이중층 · `C_dl`) **0** — 정전류 충전만 계산한다. EIS 모의 0.

# 3. 기하 모델 세 개 (§Geometrical model, SI)

## 3.1 입자형 재구성 (Fig. 1 · Table S3)

- 목표: Rueß 2020 전극 — `[인쇄]` "70 wt% polycrystalline NCM811 and 30 wt% Li₆PS₅Cl and a residual void space of **14%**" · 탄소 없음 · "does not show major issues with electronic percolation … the CAM particles therefore have to be well-connected".
- GeoDict GrainGeo → Matlab → COMSOL 5.4. CAM = 서로 겹치는 **구형 2차 입자**, PSD 따름. **SE 는 "ideal contact, filling all remaining volume"** — void 없음. 부피 40 × 40 × 40 µm³ + 분리막 10 µm + 집전체 1 µm. 주기 경계(x · y).
- ★ **SI "Reconstruction" 단락 전문 요지** `[인쇄]`: "The weight composition of 70/30 NCM811/Li₆PS₅Cl and 14% of residual void space is equivalent to an overall volume fraction of **42% CAM**. According to a percolation study on similar composites [**SI ref 3 = 01호**], electronic percolation will **not** be achieved for randomly distributed spherical particles at this volume fraction, so … electronic percolation is assured by a placeholder "trick"" — 볼록 다면체(20 × 15 × 10 µm) placeholder 가 부피 40 % 를 막고 CAM 을 나머지 60 % 에 겹침 3 % 목표로 뿌린다. 그 뒤 "A first charge simulation is used to identify **isolated particles** which are then **moved manually** to assure connection of all CAM particles in a percolating network."
- ⇒ `[해석]` **01호 퍼콜레이션 모델의 예측(42 vol% 는 문턱 아래)과 실험 셀(퍼콜레이션 문제 없음)이 어긋났고, 저자들은 01호를 고치지 않고 구조를 손으로 맞췄다.** `θ` 는 이 편에서 **출력이 아니라 1 로 고정한 입력**이다. 01호 `p_c` 의 "void 판" 은 이 편에 없다.
- `[재현]` 조성: CAM 42 · SE 58 · void 0 vol%(모델) ↔ 실물 CAM 42 · SE **44** · void 14(`[재현]` 1 − 0.42 − 0.14) ⇒ 모델 SE 부피가 실물의 **×1.32**. 그리고 42 % 자체가 `ρ_SE` ≈1.95 를 전제한다(G4).
- 세 무작위 배열 a · b · c — Table I `[인쇄]` 입자 266 · 249 · 248 개, 면적 0.173 · 0.172 · 0.167 m² g⁻¹.
- 면적: 모델 0.17 m² g⁻¹ ↔ BET 0.2(ref 11 Trevisanello) — `[인쇄]` 차이는 "surface roughness … not part of the microstructure model". `[인쇄]` "the active surface area relative to the electrode cross section is in the order of 10" — `[재현]` 40 µm × 0.42 × 4.77 g cm⁻³ × 0.17 m² g⁻¹ = **13.6**(BET 로 16.0).

## 3.2 1-입자-void 모델 (Fig. 2 · SI)

- `[인쇄]` 구형 CAM 한 개(지름 `d_CAM`)를 SE 상자가 감싼다(상자는 x · y 로 `d_CAM/4` 여유), 아래쪽은 `d_CAM/10` 잘라 집전체에 붙인다(`[재현]` 잘린 캡 = 표면적의 10 %). SE 미세구조는 "for technical reasons" 해상하지 않는다(01호식 다면체 SE 는 메시 부담).
- void = CAM 표면 위 **반구**, 지정 지름으로 무작위 위치에 **목표 피복률에 닿을 때까지** 생성(COMSOL Application Builder). `[인쇄]` "the achieved surface coverage for the whole particle may differ slightly".
- `[도표]` Fig. 2: 7 µm 입자 "Ideal · 90 · 80 · 70 · 60 · 50 % CAM/SE contact" 6 기하 + 23호 SEM(미사이클 · 1회 충전 · 50 사이클).
- 해석 틀 `[인쇄]`: 큰 void = "partial contact loss between CAM and SE particles resulting from NCM particle shrinkage upon delithiation" · 작은 void = 제조 잔류 공극 또는 "inactive material, such as carbon or binder that reduces the CAM/SE-interface area". 크기 추정: 접촉 손실형 void ≈ SE 입자 크기 1–10 µm(ref 27 Minnmann) · 제조형 < 2 µm "we estimate".

## 3.3 원뿔형 구조화 전극 (Fig. 3 · SI 식 (1)–(11))

- 절두 원뿔 CAM(집전체 쪽 지름 `a` > 분리막 쪽 `b`) + 나머지 SE, 단위 셀 주기 경계. `[인쇄]` SI 식 (8) `ν_CAM = (π/12)(1 + x + x²)`, `x = b/a` ⇒ `ν_CAM` 0.55 → `b/a` = 0.6623 → `(a, b)` ∈ {(2, 1.3), (5, 3.3), (10, 6.6), (20, 13.3)} µm. 겹침 `dn` 으로 `b/a` 와 부피분율을 떼는 변형(Fig. S4 · S8).
- 메시(Fig. S5 `[인쇄]`, 쪽 렌더로 열 배정 확인): **1-입자-void** 최대 요소 0.378 µm · 사면체 1.74 × 10⁶(0.7 µm void) · 5.2 × 10⁵(2.0 µm) · 4.1 × 10⁵("7.0 µm voids") · **입자형** 최대 요소 **1.79 µm** · 8.63 × 10⁶ · **원뿔** 1.02 µm · 5.2 × 10⁵. `[해석]` 입자형의 최대 요소 1.79 µm 는 S-PSD 최소 입자(≈1–2 µm, Fig. 5a)와 같은 크기다 — 메시 수렴 검사는 인쇄되지 않았다. HP Z8 G4 한 대.

# 4. 검증 (§Validation, Fig. 4)

- 대조 셀: Rueß 2020 · Trevisanello 2021 · Conforto 2021(38호) — 미세구조 파라미터 Table S3. **첫 충전**만(`[인쇄]` "we use experimental input that was measured during the 1st charge as well"; Rueß 는 `R_CT` 가 충/방에서 크게 다르다고 보고 — CEI).
- `[도표]` Fig. 4 왼쪽: 세 배열 곡선이 거의 겹친다. 0.5 C 컷오프 ≈103–106(모의) ↔ ≈115 mAh g⁻¹(실험) · 0.1 C ≈165 ↔ ≈172 · 0.02 C ≈188 ↔ ≈197. 0.5 C 실험 곡선은 시작부터 3.75 V 로 뛰고(모의 ≈3.71) 50–100 mAh g⁻¹ 에서 모의가 낮고 4.0 V 위에서 모의가 가파르다 — `[인쇄]` 서술과 맞다.
- `[도표]` Fig. 4 오른쪽 dQ/dV: 0.02 C 모의 두 봉 ≈3.675 · ≈3.77 V(봉 높이 ≈1000 · ≈510) · 0.1 C 모의 봉 ≈3.69 V ≈680 ↔ 0.1 C 실험 봉 ≈3.72 V ≈880. **0.02 C 실험 dQ/dV 는 그려져 있지 않다** — `[인쇄]` 두 봉 비교는 Märker 2019 액체 반쪽전지(ref 48) 3.7 · 3.8 V 와 한다.
- `[인쇄]` 결론: "we consider the simulation and the experiment in good agreement given the complexity of real cells … **none of the simulation input has been fitted**".
- `[해석]` 이 대조에서 검사되지 않은 것: (i) void 14 % 의 효과 — 모델에 void 가 없다 (ii) 0.2 C (iii) 방전 (iv) 사이클. 그리고 이 편 스스로 void 가 0.1–0.5 C 에서 수십 mV 를 만든다고 계산했다(§6) — **검증 모델에 그 항이 없는데 맞았다는 것**은, 무엇이 그 몫을 흡수했는지(과소 면적 0.17 ↔ 0.2 · SE 부피 ×1.32 · 입력 `D̃`/`j₀` 규약)를 묻게 한다. 원문은 구조화 절에서 반대 부호 두 효과(거칠기 ↑면적 · void ↓면적)에 대해 `[인쇄]` "It is not straightforward to estimate whether these two effects might compensate each other" 라고 적는다.

# 5. 입력 — PSD 와 `D̃` · `j₀` (§Input parameters, Fig. 5–7 · Table I · Fig. S6)

## 5.1 PSD (Fig. 5 · 6 · Table I)

- `[인쇄]` 입력 출처: Rueß 2020 GITT · EIS + **Conforto 2021 "impedance modeling for the PSD"** — "All input parameters were measured on the same materials". Conforto EIS-PSD 는 큰 입자에서 불확실(반무한 확산으로 이동).
- 세 상한: S ≤ 11 · M < 14 · L ≤ 20 µm. `[도표]` Fig. 5a 막대(발생 빈도)는 11 µm 아래 거의 같고 M · L 은 11.5–20 µm 에 드문 막대 몇 개.
- Table I `[인쇄]`: 입자 수 S 248–266 · M 177 · L 128 · 면적 0.167–0.173 · 0.139 · 0.113 m² g⁻¹ — `[인쇄]` "loss of **35%** surface area for the S-PSD to the L-PSD and around **50%** less particles"(`[재현]` 34 % · 50 %).
- `[도표]` Fig. 5b–d 0.5 C 컷오프: S ≈103–106 · M ≈84 · L ≈63 ↔ 실험 ≈115; 0.02 C: S ≈188 · M ≈185 · L ≈178 ↔ ≈197. `[인쇄]` "The L-PSD even shows significant deviations from the experimental data for 0.02 C".
- Fig. 6 `[도표]`: 0.2 C 충전 끝 CAM 내 ln(c) 색지도 — L 의 큰 입자 중심이 붉다(고농도 · 미추출). `[인쇄]` "A significant portion of the larger particles is **not activated at all** and the inner parts remain highly lithiated."
- `[해석]` **이 "비활성" 은 `θ`(비연결)가 아니라 확산 한계 `u`(연결됐으나 율 안에 못 비움)다** — 모든 입자가 손으로 연결돼 있다. 카드 3 항 분해([[assb-apparent-capacity-decomposition]])에서 `u` 쪽 표본이고, 저율에서 대부분 회복된다(0.02 C L ≈178 ↔ S ≈188).
- `[해석]` **PSD 선택은 실험 일치로 했다** — S 를 "modified" 로 만들어 이후 모든 계산(Fig. 7 · 10)에 썼고, 선택 근거는 Fig. 5 의 일치다. "none fitted" 는 연속 파라미터를 최적화하지 않았다는 뜻으로 읽어야 한다(D2).

## 5.2 `D̃_Li` · `j₀` 의 SOC 의존 (Fig. 7 · S6)

- `[도표]` Fig. 7a: `D̃_Li`(10⁻¹² cm² s⁻¹) — 3.6 V ≈0.07 → 3.73 V ≈3.8 → 3.73–3.84 V 고원 ≈3.3–3.6 → **3.94 V 최대 ≈6.85** → 4.08 V ≈3.5 → 4.22 V ≈0.17(`[인쇄]` "typically by two orders of magnitude"). `j₀`(10⁻⁵ A cm⁻²) — 3.6 V ≈0.2 → **3.8 V 최대 ≈1.55** → 4.0 V ≈1.2 → 4.19 V ≈0.28.
- `[인쇄]` 상수 세트: `D̃_Li,1` **6.8 × 10⁻¹²** · `j₀,1` **1.55 × 10⁻⁵ A cm⁻²**(최대) · `D̃_Li,2` **3.5 × 10⁻¹²**(고원 [3.7, 3.9] · [4.05, 4.15] V) · `j₀,2` **0.90 × 10⁻⁵**(평균). `[재현]` `j₀,1` = 0.155 A m⁻² · `j₀,2` = 0.090 A m⁻² — 50호가 "10⁻⁵ A cm⁻² = 0.1 A m⁻²" 로 읽은 범위.
- `[인쇄]` 해석: `D̃` 상승은 divacancy 도약(Van der Ven ref 54) · 4.15 V 하락은 층간 거리 감소. `j₀` 초기 상승은 공공 증가, 3.8–4.0 V 완만한 하락은 입자 내 농도 구배, 4.0 V 위 급락은 표면 Li 고갈.
- `[도표]` Fig. 7b–f(0.5 C 컷오프, 실험 ≈114): SOC 의존 ≈103 · (c) `{D₁, j₁}` ≈143 · **(d) `{D₂, j₁}` ≈113 — 25 mAh g⁻¹ 위 거의 전 구간 실험과 겹친다** · (e) `{D₁, j₂}` ≈137 · (f) `{D₂, j₂}` ≈108.
- `[인쇄]` "**The simulation that reproduces the experimentally obtained data best stems from the mean diffusion coefficient and the maximum exchange current density (Fig. 7d)**, although it does not reproduce the initial voltage increase." ↔ 결론 `[인쇄]` "**Constant input parameters are not capable of accurately simulating the voltage curve**" (D3).
- `[인쇄]` 4.0 V 위 모의 급상승이 실험에 없는 이유 — 세 후보(모델 밖 효과 · 입력 부정확 · 실험 오류) 중 "combination", 실험 오류는 "least probable". `D̃` 는 두 전극 EIS 에서 음극 몫이 섞이고, 3.75–3.9 V 불균일 리튬화로 과소평가, 고전압 혼화 간극에서 GITT/EIS 가정 붕괴 — "may be underestimated significantly". "The measurement of `j₀` is generally more accurate" — CEI 성장만이 어긋남(Fig. 7a 비대칭).
- ★ `[인쇄]` "we want to emphasize this is a potential **Achilles heel** in electrochemical simulation and that the often performed **fitting of `j₀` or the reaction rate constant to the simulation should be rethought and used with caution**." 그러고 나서 "we rely on the SOC-dependent input parameters … as we consider this as the best and physically correct choice".
- `[해석]` **Q4 표본**: 서로 다른 두 입력 가족(SOC 의존 곡선 ↔ 상수 `{D₂, j₁}`)이 같은 전압 곡선 가족을 비슷하게(0.5 C 에서는 상수 쪽이 더) 재현한다 — **이 편 그림 자체가 곡선 → `(D̃, j₀)` 역문제의 비유일성 시연**이다. 저자는 그 결론을 "적합하지 말라" 로 인쇄했고, 선택은 물리적 정당성으로 했다. 식별성 척도는 0.

# 6. void (§Void influence, Fig. 8 · 9 · S7)

- `[인쇄]` 문헌 void: 6–40 %(Ates ref 57 슬러리 20–40 % · 함침 LCO 6–8 % ref 58 · 압착 셀 NCM/Li₆PS₅Cl ≈14 %(refs 10, 27) · **LCO/LPS-LiI 13 %(ref 56 = 55호)**).
- `[인쇄]` 동기: "to date, the effect of **interfacial** voids and their properties on the lithium diffusion in NCM are not clear".

## 6.1 활성 계면 면적 스윕 (Fig. 8 · S7)

- 7 µm 입자 + **1.4 µm** 반구 void, 남은 계면 100 → `[인쇄]` "no more than **52%**". 0.02 · 0.1 · 0.2 · 0.5 C. void 과전압 = 이상 계면 전압 − void 기하 전압(50 · 100 mAh g⁻¹ 두 점).
- `[도표]` Fig. 8 오른쪽(짙은 = 7 µm, 옅은 = 5 µm; 실제 점 위치 `A` ≈93 · 84 · 73 · 63 · 53 %): **0.2 C @50** ≈5 · 12.5 · 23 · 34 · **47 mV** · 0.2 C @100 ≈4.5 · 9.5 · 18.5 · 28 · **40** · 0.1 C @50 ≈3 · 7 · 13.5 · 20.5 · 29.5 · 0.1 C @100 … ≈23 · **0.02 C ≤ ≈7.3**. 5 µm(`A` ≈50 %): 0.2 C @50 ≈39.5 · @100 ≈29.5 · 0.1 C ≈21.5. **0.5 C 는 오른쪽 그림에 없다.**
- `[도표]` Fig. 8 왼쪽 컷오프 용량: 0.5 C ≈107(100 %) → ≈80(50 %) — **−25 %** · 0.2 C ≈150 → ≈125 · 0.02 C 확대창 4.2 V 도달 ≈193(100 %) → ≈188(50 %) — **−3 %**.
- `[인쇄]` "At the small charge rate of 0.02 C, the active surface area reduction due to voids does not noticeably affect the voltage profile" · "at 0.2 and 0.5 C rate, where the overpotential rises up to 50 mV for 52% remaining interface area at 100 mAh g⁻¹" (D5 — 그림 0.2 C @100 ≈40, @50 ≈47) · "Overall, the void overpotential is higher at 50 mAh g⁻¹ compared to 100 mAh g⁻¹".
- Fig. S7(5 µm · 1.4 µm void, `[도표]` 범례 40–100 %A 일곱 곡선) — `[인쇄]` "the trends are the same for both particle sizes, while the magnitude is smaller".
- ★ `[재현]` **BV 면적 축소만의 몫** — 7 µm 입자(질량 8.57 × 10⁻¹⁰ g × 200 mAh g⁻¹), 표면 1.54 × 10⁻⁶ cm², `j₀` = 1.55 × 10⁻⁵ A cm⁻², 대칭 BV `η = 2(RT/F)·asinh(j/2Aj₀)`, 273.15 K: 0.2 C 에서 `A` 1 → 0.53 의 `Δη` ≈**20.9 mV**(298 K 로 22.8) · 0.1 C ≈13.2 · 0.5 C ≈27.6. `[도표]` 0.2 C @50 **47** · 0.1 C @50 **29.5** ⇒ 순수 동역학 몫 **≈44–45 %**, 나머지는 입자 내부 확산의 공간 불균일. (`j₀` 를 0.90 으로 두어도 0.2 C 몫은 ≈25 mV — 절반 근처는 유지.) ⚠ C-율 정의(G6) · 모델 `j₀(SOC)` 의 국소 값은 가정.

## 6.2 void 크기 · 분포 스윕 (Fig. 9)

- 남은 계면 **70 %** 고정, `d_CAM/d_Void` 1.2 → 10. `[도표]` Fig. 9 확대창 범례: no voids · 10 · 7 · 5 · 3.5 · 2.3 · 1.4 · 1.2 ⇒ `[재현]` void 지름 **5.83** · 5.0 · 3.04 · 2.0 · 1.4 · 1.0 · 0.7 µm. ↔ 본문 `[인쇄]` "void sizes of maximum **4 µm** and minimum 0.7 µm"(D4).
- `[인쇄]` "To cover 30% … 160 small voids of 0.7 µm diameter … but only **two 4 µm-sized voids** are needed" ↔ `[재현]` 반구 void 가 구 표면에서 차지하는 면적 = `π(d_v/2)²`(정확) ⇒ 0.7 µm × 160 = 공칭 40 % · 무작위 겹침 `1 − e^{−0.40}` = **33 %** ✓ · **4 µm × 2 = 16 %** ✗ · 5.83 µm × 2 = 35 %(겹침 29 %) ✓ — "two voids" 는 비 1.2(5.8 µm)와 맞는다(D4).
- `[도표]` Fig. 9 오른쪽(로그 세로축): **0.2 C @50** 비 1.2 ≈50 → 1.4 ≈36 → 2.3 ≈35 → 3.5 ≈31 → 5 ≈23 → 7 ≈21 → 10 ≈**19 mV** · **0.2 C @100** ≈**65** → … → ≈**14.5** · 0.1 C @50 ≈35 → ≈11 · 0.02 C ≈9.6 → ≈2.8. ⇒ **같은 `φ` 에서 ×2.6(@50) – ×4.5(@100)**. 자기 정합: 비 5(= 1.4 µm void)의 0.2 C @50 ≈23 ↔ Fig. 8 `A` ≈73 % 점 ≈23 ✓.
- ⚠ 비 1.2 에서는 @100 > @50(65 ↔ 50) — "void overpotential is higher at 50" 는 Fig. 8 조건에서만(D11).
- `[재현]` 같은 70 % 에서 BV 면적만의 몫 0.2 C ≈10.9 mV — **가장 균일한 분포(≈19 mV)도 그 위**다.
- `[인쇄]` 결론 문단: "The surface effect, we observe, alone is dependent on the void size, the void distribution and its surface coverage … a homogeneous void distribution is preferable" · "assuming that the SE becomes more compact upon cycling due to external pressure, the influence of the smaller voids is expected to decrease" · 그리고 한계 "not capable to quantify the influence of voids … on ionic percolation".

# 7. 구조화 양극 (§(Micro-)structured cathodes, Fig. 10 · 11 · S8)

- 42 vol% 원뿔(면적 0.17 — `[인쇄]` 단위 "0.17 g m⁻²" 오기, D6) ↔ 입자형 ↔ 실험: `[도표]` Fig. 10 왼쪽 0.5 C 컷오프 **원뿔 ≈114 · 입자형 ≈102–106 · 실험 ≈115**. `[인쇄]` "the overpotential is generally reduced in the structured electrode … the profile shape is the same" — 곡선 모양은 `D̃`/`j₀` 가 정한다. `[해석]` **void 도 굴곡도도 없는 원뿔이 0.5 C 에서 입자형보다 실험에 더 가깝다** — 이 편의 "검증" 이 미세구조를 얼마나 가리는지(곡선 → 구조 역문제의 약함)를 보여 주는 한 점.
- `[도표]` Fig. 10 오른쪽 면적(55 vol% 원뿔): `a` 2 µm ≈**0.51** · 5 ≈0.21 · 10 ≈0.11 · 20 ≈0.07 m² g⁻¹ ↔ BET 0.2(42 vol%) · S 0.17 · M 0.14 · L 0.113. `[인쇄]` 2 µm 원뿔은 "five times the interface area".
- `[인쇄]` Fig. 11: 2 µm 원뿔 1 C 까지 평탄 · 5 µm 은 1 C 에서 ≈100 mAh g⁻¹ · 10 · 20 µm 은 저용량 컷오프. 겹침 원뿔(Fig. S8)은 더 나쁘다 — "a high surface area is the key". 권고: "structuring of SSB cathodes has to be in the low µm-range, **below 5 µm**" (레이저 12 µm 채널 선례 ref 60–61).
- `[인쇄]` 무-SE 확산 의존 전극(LiTiS₂, `D̃` 10⁻⁸–10⁻⁹)은 NCM811(`D̃` 세 자릿수 낮음)에 "unlikely".

# 8. 결론 (인쇄 요지)

(1) `D̃` · `j₀` 의 SOC 의존이 "matters … significantly", 상수 입력은 "not capable" — "not blindly rely on literature findings" · 더 믿을 만한 `D̃` 실험 자료 요구 (2) 적은 수의 큰 입자가 면적을 크게 깎는다 — 단결정 · 소입자 권고 (3) void 부피 최소화 + **CAM/SE 계면 void 는 작게 · 균일하게**(등방 열간 가압 ref 29) · "We encourage a deeper look into **partial contact loss, its size and shape characteristics and evolution**, both experimentally and theoretically" (4) 구조화는 저 µm 채널 필요 — "unlike liquid electrolytes, the SE does not infiltrate (micro-)porosities" (5) 결합 (화학-)역학 + 전기화학 미세구조 모의가 "formation and evolution of voids and inter-particle cracks during cycling" 을 평가하는 데 필요.

---

# 9. 이 편을 ASSB 합성 truth 에 쓸 때 — 37호 다섯 조건 (`[추론]`)

37호 §9 의 조건 (i) `θ` 가 용량에 곱해지되 `ε_p` 와 별개 (ii) 비연결 입자가 자기 SOC 의 리튬을 붙든다 (iii) 죽은 부피가 전해질이 되지 않는다 (iv) `θ` 에만 반응하는 조작 · 관측 (v) 이중층이 접촉 면적에 비례.

| 조건 | 이 편 | 판정 |
|---|---|---|
| (i) `θ` 별개 칸 | `θ` 는 **손으로 1** — 고립 입자를 옮겨 없앴다 | ❌ 칸 없음 |
| (ii) `_li` 형 비연결 | 비연결 입자 0. L-PSD 큰 입자 중심의 "not activated" 는 **연결된 채 확산 한계**(`u`) | ❌ (`u` 표본은 있다) |
| (iii) 죽은 부피 ≠ 전해질 | 1-입자: void 는 void(무반응 면) ✅ · **입자형 검증 모델: void 14 % 를 SE 로 채웠다** — 37호가 경고한 "죽은 부피 → 전해질" 의 **공극 판** | ⚠ 부분 |
| (iv) `θ`-전용 조작 | void 스윕은 **`φ` 조작**이고, `φ` 고정에서도 분포가 과전압을 ×2.6–4.5 움직인다 ⇒ `φ` 한 칸으로도 요약 안 된다 | ❌ (`φ` 조작으로는 부분) |
| (v) `C_dl ∝` 면적 | 용량성 요소 0 — EIS · 이완 없음 | ❌ 해당 없음 |

⇒ `[추론]` 이 편의 1-입자-void 모델은 37호 갈래 ①(`A_eff(N)`)의 **3D 해상판**이고, 37호가 식으로 보인 `A_eff ↔ k` 항등을 **부분적으로 깨는** 첫 모델 표본이다(§6.1 `[재현]` 동역학 몫 ≈절반 · §6.2 분포 의존). 합성 truth 로 쓰려면: (a) `φ` 와 함께 **피복 분포(void 크기)** 를 truth 파라미터로 기록 (b) `j₀` 균일 축소 대조 실행을 같이 돌려 "피복 = `j₀` 쌍둥이" 몫과 확산 몫을 뗀다 — **이 편은 그 대조를 하지 않았다**(상수 `j₀` 세트는 입자형 모델에서만) (c) 검증용 입자형 모델처럼 void 를 SE 로 채우지 않는다.

---

# 10. 곱 축퇴 처방 — 서른아홉 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 모의 EIS 0 · `C_dl` 0 · 입력 `R_CT`(Rueß)는 `j₀` 로 바뀌어 들어가고 그 `A` 가 미정의 | ❌ |
| **2단계** 면적 대조군 | **모델 안의 면적 대조군 둘**: (a) 피복률 스윕(Fig. 8) — "면적만 바꾼 쌍" 의 3D 판 (b) **`φ` 고정 · 분포 스윕(Fig. 9)** — 면적 **밖**의 손잡이 | ⚠ 모델판 — 실측 0 |
| **3-a** `Ea` | `T` 한 점(273.15 K 인쇄) | ❌ |
| **3-b** `C` 상한 | — | 해당 없음 |
| **4단계** 두 영역 | 없음 | ❌ |
| 율 스윕 줄 | 4 율(모의) — `i → 0`(0.02 C)에서 void 과전압 ≤ ≈7 mV · 용량 −3 % ⇒ **저율이 `φ` 를 지운다**(첫 줄 전제의 모델 확인) | ✅ 모델판 |
| `A_eff ↔ k` 항등 줄(37호) | `[재현]` 피복 효과 중 BV 면적 몫 ≈44–45 % · 나머지는 분포 · 확산 | ⚠ **3D 에서 부분 파괴** |
| 면적 정규화 규약 줄(50호) | `j₀` 가 EIS 입력인데 식 (12) `A` 미정의 — 규약 차 `[재현]` ≈×13.6 | ⚠ 50호 대조의 한쪽이 규약 없음 |

**곱이 선 자리** — 모델에서 `j₀` 와 계면 면적은 BV 식에서 곱으로 만난다(모델 CAM/SE 면적 × `j₀`). 이 편은 `j₀` 를 외부에서 고정하고 면적을 기하로 준 뒤 **적합하지 않았다** — 곱은 풀린 것이 아니라 **입력 단계에서 한 규약으로 고정**됐다(31호 "상수 입력" 부류). 그리고 PSD 선택이 면적(Table I 0.113–0.173)을 실험 일치로 골랐으므로 **면적 쪽 인자가 사실상 곡선에 맞춰졌다** — `j₀` 를 고정하고 면적을 고른 것이다.

**⇒ 이 적용이 처방에 더하는 것**:
1. **새 줄 "`φ` 고정 분포 스윕 — 3D 모델에서 `A_eff ↔ k` 항등의 파괴 검사"**: 표면 피복을 넣은 해상 모델에서 (i) 피복률 스윕과 (ii) **같은 피복률에서 피복 크기 · 분포 스윕**과 (iii) **`j₀` 균일 축소**(같은 `A·j₀`)를 나란히 돌린다. (ii) 가 과전압을 움직이고 (iii) 이 (i) 과 어긋나면 그 계에서 접촉 손실은 `j₀` 의 쌍둥이가 아니다 — 곡선에 **분포의 서명**(입자 내부 확산 불균일)이 남는다. 56호: (i) · (ii) 는 했고 ×2.6–4.5, (iii) 은 안 했다(`[재현]` BV 몫 ≈절반).
2. **"비적합" 선언의 층위 검사** — 연속 파라미터를 최적화하지 않았어도 **이산 선택**(PSD 절단 · 입력 세트 · 수작업 연결)을 실험 일치로 했으면 그 선택이 곱의 한 인자를 맞춘다. 비적합 선언 옆에 이산 선택 목록을 적는다.

**⚠ 이것이 곱을 푼 것은 아니다** — 전부 모델 명제이고, 실측 쪽 `R·C` · `Ea` · 면적 대조군은 0 이다. `[재현]` 동역학 몫은 C-율 정의와 국소 `j₀` 에 대한 가정 위에 있다. 신품 · 첫 충전 · `LAM_PE` 없음.

---

# 11. Q1–Q8 / 채움표 행

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **이동 없음 — 층 하나(모델 명제)** "피복률 `φ` 의 3D 모델 스윕: 저율 무감(0.02 C ≤ ≈7 mV · −3 %) · 고율 용량 손실처럼(0.5 C −25 %) · **`φ` 고정에서 분포가 ×2.6–4.5**". `θ` 는 손으로 1 · void 부피 스윕 0 · `θ(N)` **0/56** | 없음 — 대조는 남의 충전 곡선 3 율 | ★ 층 하나 **"비적합 선언 + 이산 선택(PSD 절단 · 수작업 연결 · 입력 세트) + `j₀` 면적 미정의"** — 입력은 같은 재료의 측정(Rueß · Conforto)이나 `j₀` 는 `R_CT` 에서 `A` 미상으로 환산; 오차 척도 0; 검증 모델은 void 를 SE 로 채움 | **0/56 — 마흔여덟 번째 성질** "비유일성을 그림으로 보이고(상수 `{D₂, j₁}` 가 SOC 의존보다 0.5 C 에서 잘 맞는다 — 본문 'best') '물리적으로 옳다' 로 골랐다 — `j₀` 적합을 'Achilles heel' 로 경고했으나 식별성은 재지 않았다" | 해당 없음(Li 금속 대극 모델 · `j₀ᵃ` 3 A cm⁻²) | 없음(`MPa` 0 · `pressure` 1 추측문) | 해당 없음 | **층 하나** — NCM811 OCV(Fig. S2, `x` 0.22–1.0) = **02호 `U₀` 의 경유지, 원전 Rueß 2020**; 기울기 있음 |

**채움표 56호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** 칸을 움직이지 않은 이유: Q1 의 새 내용은 **모델 명제**(실측 · 논문 측정 명제가 아님) · Q8 은 02호가 이미 채운 칸의 출처 추적.

---

# 12. 어긋남 (실제로 어긋난 것만)

| # | 자리 | 어긋남 |
|---|---|---|
| **D1** | Table S2 `T` | **273.15 K**(0 °C) — 실험 온도는 지면에 없다. 오기라면(298.15) `RT/F` ×1.09, 식 (12) `j₀` 도 같은 비 |
| **D2** | §Validation ↔ Table S3 · Fig. 5 | "none of the simulation input has been fitted" ↔ PSD "modified" · 세 절단 중 실험 일치로 S 선택 · 고립 입자 "moved manually" |
| **D3** | 본문 Fig. 7 절 ↔ 결론 | "best … Fig. 7d"(상수 `{D₂, j₁}`) ↔ "Constant input parameters are not capable of accurately simulating the voltage curve" |
| **D4** | §Void distribution | "ratio 1.2 … 10 corresponding to void sizes of maximum 4 µm" ↔ `[재현]` 7/1.2 = 5.8 µm(Fig. 9 범례에 1.2 · 1.4 둘 다 있다) · "two 4 µm-sized voids" 로 30 % ↔ `[재현]` 16 %(5.8 µm 면 35 %) · SI 메시 표 "7.0 µm voids"(비 1.0 — Fig. 9 범례에 없음) |
| **D5** | §Active interface area ↔ Fig. 8 | "at 0.2 and 0.5 C … up to 50 mV for 52% … at 100 mAh g⁻¹" ↔ `[도표]` 오른쪽 그림에 0.5 C 없음 · 0.2 C @100 ≈40, @50 ≈47 |
| **D6** | §Structured | "active surface area of 0.17 **g m⁻²**" — 단위 뒤집힘(m² g⁻¹) |
| **D7** | §Geometrical model | "attempt to reconstruct the electrode microstructure reported by Rueß … residual void space of 14%" ↔ 재구성은 void 0 %(SE 가 채움) — 복원한 것은 CAM 부피분율뿐 |
| D8 | SI Reconstruction | 70/30 wt% + 14 % → 42 vol% — `ρ_SE` 미인쇄(`[재현]` ≈1.95 필요) |
| D9 | Fig. 8 ↔ Fig. S7 | 5 µm 입자: Fig. 8 오른쪽 옅은 점은 `A` ≈50 % 까지 ↔ S7 범례 **40 %A** 곡선 존재 |
| D10 | 식 (12) ↔ Table S1–S2 | `A` 미정의 · Table S1 `j₀` 단위 A m⁻² ↔ Fig. 7a 10⁻⁵ A cm⁻²(단위는 환산 가능, 면적 규약은 없음) |
| D11 | §Active interface area ↔ Fig. 9 | "void overpotential is higher at 50 mAh g⁻¹" ↔ Fig. 9 비 1.2 에서 @100 ≈65 > @50 ≈50 |
| **D12** | **계보 — 14호 ref [69]** | 14호 `[인쇄]` "abrupt resistance increase when the pore volume … surpasses a threshold" 의 근거로 이 편 ↔ 이 편 `threshold` · `surpass` 0 · void 부피 스윕 0 · 저항 계산 0 |
| **D13** | **계보 — 50호 ref 35** | 50호 `[인쇄]` 서술(정전류 곡선 + 형태 반영 FEM 으로 10⁻⁵ A cm⁻²) ↔ 이 편: `j₀` 는 Rueß `R_CT` 에서 계산한 **입력**, "none … fitted" |
| D14 | ref 56(55호) | "13% in LiCoO₂/Li₂S-P₂S₅-LiI-composites" 를 공극률로 인용 ↔ 55호 `[인쇄]` 13.2 % = 수지 + 잔류 void |

---

# 13. 계보 대조

| 편 | 대조 |
|---|---|
| **01호 Bielefeld 2019**(SI ref 3) | 같은 저자 셋. 01호 `p_c` 는 **이 편에서 반례를 만났다** — 42 vol% 무작위 구 = 문턱 아래(`[재현]` 식 (8), d 5 µm → 49.3 %) ↔ Rueß 셀 퍼콜레이션 문제 없음 → placeholder + 수작업 이동으로 강제. 01호의 유한 크기 폭 · 구 가정 문제(55호 `k_LCO` 3.64)가 어느 쪽인지는 이 편이 묻지 않는다. `θ` · `A_Spec` · `p_c` 계산 0 |
| **55호 Hlushkou 2018**(ref 56) | void 효과를 **서로 반대쪽에서 반씩**: 55호 = 경로만(`τ` 1.74 → 1.27) · 이 편 = 접촉만(`φ` 스윕). 55호 표적(13.2 % · `τ` · `k_SE` · 0.616)과 같은 양 0. 이 편 검증 모델은 55호 "가상 무공극" 과 같은 상태 |
| **50호 Miß 2022**(ref 35 로 인용됨) | `j₀` 10⁻⁵ A cm⁻² 는 이 편의 **입력**(Rueß EIS) — 두 값의 일치는 EIS ↔ EIS(TLM)이고 면적 규약은 한쪽(이 편)이 미인쇄. 50호가 `a_v = 3ε/r` 완전구(접촉 ≡ 1)를 쓴 것처럼 이 편 모델도 **이상 접촉 구**에 `j₀` 를 건다 |
| **37호 Li 2024** | 접촉 손실의 두 자리(`ε_p` ↔ `A_eff·k`) 중 **`A_eff` 자리**다. 37호 원형 모델의 식 항등(`A_eff ↔ k`)이 3D 해상에서 **부분 파괴**(§6 · §9) |
| **53호 Ren 2023**(ref [203]) | 53호 한 문장("입도 분포 · 농도 의존 동역학")은 이 편 §Input parameters 와 맞다 ✓ |
| **14호 Oh 2025 *Maxwell***(ref [69]) | D12 — 귀속 불확인 |
| **02호 Clausnitzer 2023**(ref 36) | NMC811 `U₀` = Fig. S2 → 원전 Rueß 2020 |
| **38호 Conforto 2021**(ref 47) | PSD 원천(EIS-PSD) — 이 편은 그것을 11 µm 에서 잘랐다; 38호 G3("EIS-PSD 신뢰 한계 1.8 · 4.5 µm")와 이 편의 "큰 입자에서 불확실" 이 같은 방향 |
| **23호 Koerver 2017**(ref 8) | Fig. 2 SEM 차용 · 수축 → 접촉 손실 서사의 원천 |
| **큐 58 Bielefeld 2020**(ref 25) | 이 편 서론 "Highly tortuous ionic paths … crucial impact"(refs 25, 27) — 굴곡도 · void 경로 효과는 그쪽 편에 있을 가능성(`[해석]`) · 14호 "pore 문턱" 의 실제 출처 후보 |

---

# 14. 그림 — 무엇을 봤나

크로퍼 자동 **17 장**(본문 Fig. 1–11 · SI Fig. S1 · S3 · S4 · 표 S1–S3) — 제외 7 건(f6 · f10 중복/영역 없음 보고됐으나 fig_6 · fig_10 은 정상 생성, SI S2 · S5–S8 벡터라 제외) + **수동 2 장**(SI Fig. S2 · S7, 300 dpi, `figures.json` 에 note).
- **Read 11 장 + 쪽 렌더 1**: Fig. 2 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · S3 · S2(수동) · S7(수동) + S5(쪽 렌더 — 메시 표 열 배정 확인용, 텍스트 추출 순서가 열과 달랐다).
- **안 봄**: Fig. 1(생성 절차 도식) · 3(구조화 도식) · 11(원뿔 곡선 — 본문 서술만) · S1(계단 함수) · S4(겹침 원뿔 도식) · S6(Fig. 7 재배열) · S8(겹침 원뿔 곡선). 표 S1–S3 은 텍스트로.
- 본문 서술과 어긋난 그림: **Fig. 8**(0.5 C 과전압 점 없음 · 100 mAh g⁻¹ 최대 ≈40 — D5) · **Fig. 9 범례**(비 1.2 = 5.8 µm — D4) · **Fig. 7d**(상수 세트가 최선 — 결론과 D3) · **Fig. 4 오른쪽**(0.02 C 실험 dQ/dV 없음).

---

# 15. 참고문헌 중 후속 후보 (67 번호 · SI 7, 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Ruess, Schweidler, Hemmelmann, Conforto, Bielefeld, Weber, Sann, Elm, Janek, *JES* 167, 100532 (2020)** | 10 · SI 1 | **모든 입력의 원전** — `R_CT(V)` → `j₀`(식 (12) 의 `A` · 온도), `D̃(V)`, OCV, void 14 %, 첫 충전 곡선. 38호 ref 19 · 29호 ref 26 과 같은 편 | 규약(G1) · Q3 · Q8 |
| **Bielefeld, Weber, Janek, *ACS AMI* 12, 12821 (2020)** | 25 · SI 6 | **큐 58** — 굴곡도 · 경로; 14호 "pore 문턱" 귀속 후보 | Q1 · 경로 |
| Minnmann, Quillman, Burkhardt, Richter, Janek, *JES* 168, 040537 (2021) | 27 | 압착 셀 void ≈14 % · SE 입자 1–10 µm · 굴곡도 병목(02호 SI ref 4 로도 지목) | 경로 · void |
| Neumann, Randau, Becker-Steinberger, Danner, Hein, Ning, Marrow, Richter, Janek, Latz, *ACS AMI* 12, 9277 (2020) | 38 | CT 재구성 NCM622/β-Li₃PS₄ 방전 모의 · 전자 전도 한계 · 집전체 접촉(54호의 다른 편) | 구조 ↔ 모의 |
| Trevisanello, Ruess, Conforto, Richter, Janek, *AEM* 11, 2003400 (2021) | 11 | BET 0.2 m² g⁻¹ · 균열 → 겉보기 `D̃` | 면적 규약 |
| Ates, Keller, Kulisch, Adermann, Passerini, *Energy Storage Mater.* 17, 204 (2019) | 57 | 슬러리 복합양극 void 20–40 % | void 범위 |
| Park, Kim, Oh, Jin, Kim, Jung, Lee, *AEM* 10, 2001563 (2020) | 44 | GeoDict 미세구조 생성 선례 | 합성 기하 |

**큐 58–59**: 58 Bielefeld 2020 = **ref 25** ✅(서론 2 곳 — 굴곡도 · void) · 59 Asheri 2023 ❌(이 편보다 늦다).

---

# 16. 이 digest 가 주장하지 않는 것

- **void 가 실제 셀에서 과전압을 X mV 올린다고 주장하지 않는다** — §6 의 수는 전부 이 편 모델의 출력(`[도표]`)이고, 실측 대조는 0 이다.
- **이 편의 `j₀` 가 틀렸다고 주장하지 않는다.** 면적 규약이 지면에 없어 50호와의 일치가 규약 일치인지 **판정할 수 없다**고 적는다.
- **14호의 인용이 틀렸다고 단정하지 않는다** — 이 편에 그 문장의 근거가 없다는 것까지다(58호에서 확인).
- `[재현]` BV 몫(≈절반)은 C-율 정의(G6) · 국소 `j₀` · 대칭 BV 가정 위의 **어림**이다 — 모델을 다시 돌린 것이 아니다.
- 우리 파이프라인(`degradation-degeneracy/`)을 이 모델로 돌려 보지 않았다. 우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다.
- 인용한 원전(Rueß 2020 · Bielefeld 2020 · Minnmann 2021)은 열람하지 않았다.
