<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 기준 = papers/agarwal2026_umlip_applicability_domain_ssb_interfaces.md
     2026-11-10 신규 작성 (논문 에이전트 · 사용자 읽기 목록 123 번 · cascade 트랙 [1저자 = 사용자]).
     읽은 이유: reports/황화물 분해 부피 도펀트 문헌 갭.md 가 '갭을 단정하기 전에 본문을 봐야 하는 다섯 편 (가 묶음)' 으로 꼽은 편이다.
       그때는 초록 · 스니펫만 봤다. 갭 질문 7 개의 답은 §4 에 쪽 · 절 · 그림/표 번호와 함께 모았다.
     그림: 크롭 9 장 (그림 6 + 표 3). 그림 6 장 전부 Read 로 실제로 봤다.
           표 3 장은 도구가 하나도 못 잘랐다 (JES 의 로마 숫자 캡션 'Table I.' 을 캡션으로 읽지 못했고 번호 공백 보고에도 안 떴다) → 손 크롭 (figures.json 에 manual_crop 사유).
           손 크롭이 온전한지는 이미지로 확인했고 값은 PDF 텍스트로 옮겼다.
     SI (Fig. S1 메시 수렴 · COMSOL 입력) 는 올라오지 않았다 — 본문이 SI 를 가리키는 곳은 전부 '(SI · 미입수)' 로 적었다.
     ⚠ 'figure-read ≈' 는 PDF 에 박힌 래스터 그림의 픽셀을 축 눈금으로 환산한 값이다 (논문이 표로 준 값이 아니다).
       검산 1 건: Fig. 6 의 초록 표식 중심 3.49 GPa = Table II 의 3.64 · 3.34 의 평균.
     ⚠ '[우리 산술]' · '[추정]' 은 논문 값이 아니다. 특히 §13-2 (표 1 음극 쪽 부피 변화의 재현 검산) 는 격자상수 기억값으로 한 어림이다 —
       Materials Project 부피로 다시 계산하기 전에는 판정이 아니라 '확인 필요' 깃발이다.
     우리 쪽 숫자는 옮기지 않았다 — 원장 경로로만 가리킨다. -->

# Evaluation of the Electrochemo-Mechanically Induced Stress in All-Solid-State Li-Ion Batteries — Tian, Chakraborty, Talin, Eisenlohr & Qi (*J. Electrochem. Soc.* 2020)

> slug `tian2020_electrochemo_mechanical_stress_assb` · DOI `10.1149/1945-7111/ab8f5b` (*J. Electrochem. Soc.* **167**, 090541 (2020) · 접수 2019-12-26 · 수정 2020-04-16 · 게재 2020-05-18 · JES Focus Issue on Battery Safety, Reliability and Mitigation · **OA CC BY 4.0**) · type `mixed — DFT 입력 (Materials Project 의 grand-potential 분해 반응 · 결정 부피 · first-principles 문헌값) → 연속체 화학-역학 FEM (COMSOL 5.4 · 축대칭 · 선형 탄성) · 자체 DFT 계산 0 · 자체 실험 0` · PDF `61cbac9e-123._Evaluation_of_the_electrochemo-mechanically_induced_stress_…pdf` (사용자 목록 123 번 · 11 pp = IOP 표지 1 + 논문 10 [본문 · 부록 · refs 72 편]) · **SI 미입수** (`Fig. S1` 메시 수렴 · COMSOL 입력 파일) · digested `2026-11-10` · status ✅ · 태그 **[외부·방법 원전·⛔ LiPON 박막 셀 — 황화물 0]**
> elements: Li, P, O, N, Si, Co
> methods: DFT, ESW, elastic

> **저자 (표지 그대로)**: **Hong-Kang Tian**¹, Aritra Chakraborty¹, **A. Alec Talin**², Philip Eisenlohr¹, **Yue Qi**¹\* — ¹ Michigan State University, Chemical Engineering and Materials Science · ² Sandia National Laboratories (Livermore). 교신 `yueqi@egr.msu.edu`.
> 자금: DOE BES EFRC **NEES** (Nanostructures for Electrical Energy Storage · DESC0001160) · NSF DMR-1832808 (H.K.T. · Y.Q.) · Sandia (DE-NA-0003525).
> 🎤 **관련 발표**: 해당 없음 — `litdb/talks/lee2026_skku_mlip_materials_design.md` 의 인입 대기열을 확인했고 이 논문은 그 표에 없다.
> 계보: 분해 반응의 방법 원전은 ref [37] = 우리 `zhu2015_esw_grand_potential_origin` 과 ref [38] = `zhu2016_first_principles_interface_stability_assb` (같은 날 digest · 목록 124 번). 셀과 전기화학 매개변수는 ref [28] (Talin 2016 · 같은 2.5D 셀의 제작 · 시험 · 모사) 에서 왔다. 전극 팽창 · 탄성은 ref [3] (Qi 2014). 같은 그룹의 앞 편은 ref [24] (Tian & Qi 2017 · 접촉 면적 손실 모사).
> 같은 갭 묶음의 다른 digest (같은 날): `wang2022_two_parameter_space_dendrite_constriction` · `fitzhugh2021_sei_design_constrained_ensemble` · `fitzhugh2019_ht_functionally_stable_interfaces_sulfide` · `zhu2016_first_principles_interface_stability_assb`.

---

## 0. 이 digest 를 읽는 법

이 논문은 **'SE 분해의 부피 변화를 응력으로 바꾼' 연속체 모델의 실례**다. 우리 갭 보고서가 "사실상 이것 하나" 라고 적은 그 편이다. 셋을 갈라서 읽는다.

1. **논문이 실제로 한 것** (§5–§6) — Si / LiPON / LiCoO₂ **박막 2.5D 셀 하나**. 전해질은 **LiPON 하나** (결정 Li₂PO₂N 으로 대표).
   ⛔ **황화물은 모델에 없다. Li₆PS₅Cl · Li₃PS₄ · LGPS · LLZO 도 없다.** 황화물은 서론의 동기 문장 (β-Li₃PS₄/NMC 박리 · refs 23–25) 과 참고문헌에만 나온다.
2. **논문 숫자가 서 있는 가정** (§13) — 부피 변화는 **전극 상까지 넣은 반응식 전체**로 정규화했고 (SE 만의 변형률이 아니다), 계면층 두께 · 반응 선택 · 경계조건이 전부 '최악' 쪽 가정이다.
3. **우리에게 넘어오는 것** (§4 Q7 · §10–§11) — 값이 아니라 **환산 절차와 회계 규약의 선례**다. 우리 숫자는 이 문서에 옮기지 않았다 (원장 경로만).

**표 번호 주의** — 원문은 표를 로마 숫자로 센다. webapp 링크가 아라비아 숫자만 잡으므로 이 digest 는 이렇게 부른다: **`Table 1` = 원문 Table I** (분해 반응 · 부피) · **`Table 2` = 원문 Table II** (최대 주응력) · **`Table 3` = 원문 Table A·I** (부록 매개변수).

**쪽 표기** — `p.N` 은 올라온 PDF 의 쪽이다 (IOP 표지가 1 쪽). 논문 자체의 쪽은 N − 1 이다.

**본 그림 / 안 본 그림** — 크롭 9 장 중 그림 6 장 (`Fig. 1`–`6`) 을 전부 실제로 봤다. 표 3 장은 손 크롭이 온전한지 이미지로 확인하고 값은 PDF 텍스트로 옮겼다. **SI 는 파일이 없어 안 봤다** (`Fig. S1` · COMSOL 입력).

**표지** — **[봄]** = 본문 · 그림 · 표에서 직접 확인 · **[우리 산술]** = 논문 숫자만으로 한 검산 · **[추정]** = 논문 밖 값이나 해석이 들어간 것.

---

## 1. 한 줄 요약

원뿔 기둥 위에 LiCoO₂ → LiPON → Si 를 차례로 입힌 2.5D 박막 전고체 셀을 축대칭 FEM (COMSOL · 선형 탄성) 으로 풀어 **응력의 두 원천**을 견줬다. ① 1.2 C 충전 중 전극의 Li 농도 변화 (Si 팽창 · LiCoO₂ 수축) 와 ② 전극/LiPON 계면에서 LiPON 이 분해해 생기는 계면층의 부피 변화다. ② 의 부피 변화는 Materials Project 의 grand-potential 평형상으로 반응식을 쓰고 MP 결정 부피로 계산했다 — Si 쪽 **−27 %**, LiCoO₂ 쪽 **−8 %** (둘 다 수축). 계면층을 10 nm · 50 nm 로 가정했을 때 최대 제1주응력은 LiPON 에서 **9.9–26.8 GPa** 로, 충전이 만드는 응력 (480 s 끝에서 figure-read ≈ 1.4–1.9 GPa) 보다 훨씬 크다. 저자 결론: *이 기하 · 이 물질 조합에서는 전해질 분해가 사이클링보다 더 큰 기계 손상을 줄 수 있다.*

---

## 2. 메타

| 저자 | 저널/년 | DOI | 계 | 연구유형 |
|---|---|---|---|---|
| H.-K. Tian, A. Chakraborty, A. A. Talin, P. Eisenlohr, Y. Qi\* (MSU + Sandia) | *J. Electrochem. Soc.* **167**, 090541 (2020) | 10.1149/1945-7111/ab8f5b | Si / LiPON (Li₂PO₂N) / LiCoO₂ 2.5D 박막 셀 (ref [28] 의 실물) | 연속체 전기화학 + 화학-역학 FEM · 입력은 MP DFT 자료와 문헌값 |

- 랩 표준 표기: *J. Electrochem. Soc.*, 167, 090541 (2020).
- 출처 표지: **[외부]** (MSU Yue Qi 그룹 + Sandia Talin · 우리 그룹 아님 · 팔로우 랩 아님).
- PDF 구성: p.1 IOP 표지 · p.2–9 본문 · p.9–10 부록 (식 A·1 · A·2 · `Table 3`) · p.10–11 참고문헌 72 편.

---

## 3. 이 논문이 던지는 질문 (Introduction 의 구조 · p.2–3)

1. 전극 재료는 (탈)리튬화 때 부피가 변한다. Li 조성이 고르지 않으면 'diffusion-induced stress' 가 생기고 전극이 깨진다. 액체 전해질 전지에서는 단일 입자부터 복합 전극까지 모델이 쌓였다 (refs 1–13).
2. 전고체에서는 SE 가 액체와 달리 전극 변형을 **구속**하므로 기계 열화가 더 심할 것이다. 관찰 예 셋: Li/LAGP/Li 대칭 셀에서 계면상 성장으로 LAGP 가 깨진다 (ref 20) · LAGP/Li 계면이 비정질화 + **부피 팽창** → SE 파괴 · 임피던스 급증 (refs 21, 22) · NMC/β-Li₃PS₄ 복합 양극에서 충전 중 계면 박리 (황화물 SE 계면 분해 + NMC 수축 · refs 23–25).
3. 구속은 셀 구조에 달렸다 — 2D 평면 박막 · 2.5D (한쪽 평면 + 한쪽 바늘형) · 3D (완전 교차).
4. 화학 변형의 원천은 둘이다. (i) 전극의 Li 농도 변화 — 균열 전파 · 박리 수치 연구가 있다 (refs 32, 33 = 우리 `bucci2017_chemomech_failure_assb_cycling_czm` · `bucci2018_mechanical_instability_interface_delamination`). (ii) **계면상 형성** — 유망하다던 SE 들이 환원/산화 분해한다는 것이 밝혀졌고 (refs 37, 38) 그 계면상 형성에 부피 변화가 따른다. *"As we shall show in this paper, this source of chemical strain can lead to relatively high stress generation."*
5. 그래서 (i) + (ii) 를 함께 평가하는 **일반 연속체 틀**을 만든다. 예제는 ref [28] 의 2.5D 'egg carton' 셀이다.
6. 입력은 실험과 제일원리에서 온다. *"The volume change due to the decomposition of the SE will be obtained by assuming the products of the most energetically favorable reaction at the Li chemical potential of the electrode."* 구속은 두 극한 경계조건으로 근사한다. *"This DFT-informed continuum model can be easily adapted for evaluating various electrode/SE materials 3D ASSLB geometries."* (p.3) — ⚠ 일반성은 주장일 뿐이고 실제로 푼 계는 하나다.

---

## 4. ★ 갭 질문에 대한 답 (요청 7 항목 · 쪽 = PDF 쪽)

> 묻는 쪽: `reports/황화물 분해 부피 도펀트 문헌 갭.md` (27 행 · 61 행 · 71 행 · 표 '가' 줄). 후보 주제 B = '분해 부피 변화의 화학-기계 효과 (한 아지로다이트 호스트의 도펀트별 숫자)'.

### Q1. 어떤 전해질을 모델했나 — 황화물이 있나

**LiPON 하나다. 황화물은 없다.**

- 셀 = Si 음극 / LiPON / LiCoO₂ 양극 (p.2 서론 끝 · p.3 "Battery architecture" · `Fig. 1`).
- LiPON 은 **결정 Li₂PO₂N** 으로 대표했다 — *"we selected Li2PO2N to represent LiPON, since it has been reported that the thin-film LiPON synthesized through Atomic Layer Deposition (ALD) is characterized as Li2PO2N"* (p.4 · refs 51, 52).
- LLZO · LGPS · Li₃PS₄ · 아지로다이트 · 할라이드: **모델에 없다.** β-Li₃PS₄ 는 서론의 관찰 예 (p.2) 로, LGPS · β-Li₃PS₄ 는 'CV 로 넓은 창이 주장됐던 SE' 의 인용 (refs 34, 35) 으로만 나온다. LAGP 도 동기 문장뿐이다.
- 도펀트 · 조성 변형: 0.

⇒ 보고서 표 '가' 줄의 조건 ("황화물 사례가 있으면 '분해 부피 → 응력 환산 없음' 을 '아지로다이트 · 도펀트별 환산 없음' 으로 좁힌다") 은 **발동하지 않는다.** 황화물 · 아지로다이트에 대한 환산은 이 논문에 없다.

### Q2. 전해질마다 쓴 분해 반응 · 부피 변화 · 회계

반응과 값은 `Table 1` (원문 Table I · p.5) 에 있다. 전사는 §6.4. 요점만 적는다.

| 항목 | 논문이 한 것 | 위치 |
|---|---|---|
| 산물 집합의 출처 | MP DFT 자료로 만든 **grand-potential 상도** 의 평형상 (refs 37, 38 의 방법) — 전극의 Li 전위 창마다 산물이 다르다 | p.4 "Volume change induced by the decomposition…" · `Table 1` 제목 |
| 반응식의 출처 | *"obtained from the DFT-computed database in Material Project queried through its … API"* (refs 53, 54) | p.4 |
| 부피의 출처 | *"The unit volume of each solid compound was obtained from the Material Project database."* — **자체 DFT 계산 없음** · 범함수 · +U · MP 판 미기재 | p.4 |
| 부피 변화의 정의 | ΔV_d = (V₂ − V₁)/V₁ · V₁ · V₂ = 반응식의 **모든 반응물 · 모든 생성물**의 총부피 | p.4 식 9 |
| Li 저장소 | **Li 금속이 아니다.** 반응식 안에 전극 상이 직접 들어간다 — 음극 쪽은 Li–Si 합금상 (Li₂₁Si₅ · Li₁₃Si₄ · Li₇Si₃ · Li₁₂Si₇ · LiSi · 'LiSi₃') → Si, 양극 쪽은 Li₀.₇₅CoO₂ · Li₀.₅CoO₂ → LiCoO₂. μ_Li 는 **산물 집합을 고르는 데만** 쓰이고 부피는 닫힌 반응식으로 센다 | `Table 1` · p.7 *"these are full reactions from the oxidation/reduction of the electrodes and electrolyte"* |
| 정규화 | **반응물 전체 (SE + 전극 상)** 의 부피로 나눈다. SE 부피만으로 나눈 값이 아니다 | 식 9 |
| 기체 | N₂ 의 부피는 **뺐다** — *"the volume of N2 was excluded in the molar volume change, as gas may diffuse out"* | p.7 |
| 등방성 | 부피 변화를 등방 선변형률로 바꾼다 | p.5 식 10 |
| 고른 값 | 음극 쪽 **−27 %** (Li₁₂Si₇ 행 — 모사한 조성 범위 Li₁.₆₈Si–Li₂Si 안의 '최악') · 양극 쪽 **−8 %** (> 3.63 V 행) | p.7 |

🔑 **이 표에서 가장 중요한 한 줄 [봄]**: `Table 1` 의 0.01–0.53 V 네 행은 **SE 쪽 반응이 똑같다** (Li₂PO₂N 4 개당 8 Li₂O + Li₇PN₄ + 3 Li₃P · SE 화학식당 Li 6 개 흡수). 다른 것은 Li 를 내주는 합금상뿐인데 값은 **−23 · −24 · −27 · −29 %** 로 갈린다. 즉 이 '분해 부피 변화' 에는 **전극 합금의 탈리튬화 수축이 섞여 있고**, SE 고유의 양이 아니다. 우리 보고서가 말한 '회계에 따라 부호가 갈린다' 의 네 번째 실례다 (§13-3).

### Q3. 부피 변화 → 응력 환산 방법과 숫자

| 항목 | 내용 | 위치 |
|---|---|---|
| 솔버 | COMSOL Multiphysics 5.4 + Electrochemistry · MEMS 모듈 | p.3 "Computation Methods" |
| 기하 | 육각 배열 2.5D 셀을 **축대칭** 단위 하나로 근사 (figure-read ≈ 반지름 1.8 μm · 높이 5.5 μm) | p.3 · `Fig. 1` · `Fig. 4` 축 |
| 화학 변형률 | ε_c,ij = ((1 + ΔV)^(1/3) − 1) δ_ij | p.5 식 10 |
| 역학 | 정적 평형 ∇·σ = 0 · **선형 등방 탄성** σ = C : (ε − ε_c) · 미소변형 | p.5 식 11–13 |
| 탄성 상수 | Si 96 GPa · 0.29 / LiCoO₂ 191 GPa · 0.24 / LiPON 77 GPa · 0.25 (E · ν) — **계면층의 탄성 상수는 따로 적혀 있지 않다** | `Table 3` (p.10) |
| 구속 | 집전체 · 연속 막과 닿는 바깥 경계 = 법선 변위만 막는 롤러. 이웃 기둥 사이 **공극 쪽 측면**만 두 극한: **fixed side** (공극 없음) / **free side** (공극 있음) | p.3 · `Fig. 1` |
| 계면층 | 두 계면 (Si/LiPON · LiCoO₂/LiPON) 에 두께 **10 nm · 50 nm** 가정 · LiPON 안쪽 층 · 절점 일치 (완전 접합) · **t = 0 에 이미 다 생긴 것**으로 | p.3 · p.5 |
| 메시 | 요소 11,000–290,000 시험 · 200,000 이상에서 최대 주응력 0.5 % 이내 수렴 (`Fig. S1` · SI · 미입수) | p.3 |
| 지표 | 제1주응력의 분포와 도메인별 최댓값 — *"a metric to determine the location of possible crack propagation"* | p.3 |

숫자 (`Table 2` = 원문 Table II · p.8 · 전사는 §6.5):

| 우리가 초록 수준으로 적은 값 | 본문 대조 | 판정 |
|---|---|---|
| LiPON 약 −27 % | `Table 1` 굵은 행 · p.7 · p.8 · p.9 | ✅ 맞다. 단 **Si 쪽 계면의 '반응식 전체' 부피 변화**다 (LiCoO₂ 쪽은 −8 %) |
| 최대 주응력 26.8 GPa (계면층 50 nm) | `Table 2` — **fixed side · LiPON 도메인 · 50 nm** | ✅ 맞다. 단 **조건이 빠졌다**: free side 면 **12.1 GPa** |
| 9.90 GPa (10 nm) | `Table 2` — fixed side · LiPON · 10 nm (free side 9.89) | ✅ 맞다 |
| "10 → 50 nm 에서 9.90 → 26.8 GPa" (보고서 61 행) | fixed side LiPON 에서만. free side LiPON 은 9.89 → 12.1 · Si 는 12.6 → 14.7 · LiCoO₂ 는 1.80 → 3.64 | ⚠ 두께 의존은 **도메인 · 경계조건에 따라 1.2–2.7 배**로 갈린다 |

⚠ 환산 절차 안의 불일치 하나 [우리 산술]: 식 10 에 −27 % · −8 % 를 넣으면 선변형률은 **−9.96 % · −2.74 %** 다. 논문은 *"−8.3% and −2%"* 라고 적었다 (p.7). −8.3 % 는 1 − (1.27)^(1/3) 과 일치한다 (부호를 떼고 넣은 뒤 음수로 돌린 꼴). 어느 값이 FEM 에 들어갔는지는 SI 입력 파일에 있을 것이다 (미입수). §13-1.

### Q4. '분해 응력이 전극 부피 변화 응력보다 훨씬 클 수 있다' 의 근거와 조건

근거는 `Fig. 6` 과 `Table 2` 다 (p.8–9).

| 도메인 | 분해 유발 (50 nm · fixed / free) | 분해 유발 (10 nm · fixed / free) | 충전 유발 (1.2 C · 480 s 끝 · figure-read ≈) |
|---|---|---|---|
| LiPON | 26.8 / 12.1 GPa | 9.90 / 9.89 GPa | 1.4 (fixed) / 1.9 (free) GPa |
| Si | 14.7 / 14.5 GPa | 12.6 / 12.5 GPa | 0.8 GPa (두 조건 겹침) |
| LiCoO₂ | 3.64 / 3.34 GPa | 1.80 / 1.68 GPa | 0.9 GPa (두 조건 겹침) |

- 비 [우리 산술]: 50 nm 기준 LiPON ≈ 19 배 (fixed) · ≈ 6 배 (free) / Si ≈ 18 배 / LiCoO₂ ≈ 4 배. 10 nm 기준으로도 LiPON ≈ 5–7 배 · Si ≈ 16 배 · LiCoO₂ ≈ 2 배.
- 저자 문장 (p.9): *"the decomposition-induced stress would be more significant than the charging-induced stress if there are no voids in this battery, especially in the LiPON electrolyte."* · *"the decomposition of electrolyte could cause more damage than the cycling of the batteries in terms of the mechanical failure **in this specific battery geometry and material combinations**."*

**조건** (전부 본문에서 확인):
1. 이 기하 (2.5D 박막 · 롤러 구속) 와 이 물질 조합 한정 (p.9).
2. 계면층이 **t = 0 에 10 nm 또는 50 nm 로 이미 다 생겼다**는 가정 (p.5). `Fig. 6` 은 50 nm 값만 그린다 (캡션).
3. 반응은 **'최악' 선택** — *"we focused on the 'worst' cases"* (p.7).
4. 충전 쪽은 가장 빠른 1.2 C 하나만, 그리고 **480 s 에 끝난다** — LiCoO₂ 꼭대기가 y = 0.5 한계에 먼저 닿아서다. Si 는 표면층만 x = 1.68 → 2 로 간다 (p.6). 저자도 *"results in low battery capacity"* 라고 적는다. 즉 견준 충전 응력은 **용량의 일부만 쓴 충전**의 것이다.
5. 선형 탄성. 저자 스스로 *"This stress level is beyond the elastic limit"* (p.7) 라고 적는다 — 10–27 GPa 는 실제 응력이 아니라 **선형 탄성 눈금**이다.
6. 본문은 '공극이 없으면' 이라고 조건을 달았지만 `Fig. 6` 에서는 free side 에서도 분해 쪽이 전 도메인에서 크다 [봄].

### Q5. 양극 쪽 (산화 분해) 도 다루나

**다룬다 — LiPON 한정.**

- LiPON 이 LiᵧCoO₂ 에 산화되는 반응 두 줄 (`Table 1` · p.5): 2.64–3.04 V 에서 Li₄P₂O₇ + P₃N₅ + N₂ (**−2 %**) · > 3.63 V 에서 P₂O₅ + PNO + N₂ (**−8 %**).
- 기체 생성이 예측되고 실험에서도 고전압 뒤 LiPON 에 기포 (O₂ 또는 N₂) 가 보고됐다고 적는다 (p.7 · ref 36). N₂ 부피는 뺐다.
- 응력: *"The LCO interphase generates stress of magnitude around ~3 GPa similarly under the two boundary conditions"* (p.7) · `Table 2` 의 LiCoO₂ 도메인 3.64 / 3.34 (50 nm) · 1.80 / 1.68 GPa (10 nm).
- 부호는 **수축** — 우리 보고서가 '양극 쪽 산화 = 수축 → 접촉 손실' 이라고 본 것과 같은 방향이다. 단 ① 산화물 (LiPON) 이고 ② **기체를 뺀 것이 수축의 일부**이며 ③ 리튬화되며 팽창하는 LiCoO₂ 가 같은 식 안에 들어 있다. 황화물 양극 쪽의 근거로 옮길 수 없다.
- ⚠ > 3.63 V 반응은 충전된 양극 (Li₀.₅CoO₂) 이 산화제인데 모델은 이 층을 **t = 0** 에 둔다. 부록 식 A·2 에 초기 조성 (y ≈ 0.98) 을 넣으면 양극 전위는 ≈ 2.3 V 다 [우리 산술] — 표의 첫 산화 단 (2.64 V) 보다도 아래다. §13-4.

### Q6. 저자들이 든 한계 · 가정

**저자가 적은 것 [봄]**

- 값은 구조 · 경계조건에 민감하다 — *"These values will be sensitive to the details of the ASSLB structure and boundary conditions."* (p.8)
- 응력 수준이 탄성 한계를 넘는다 (p.7). 그래도 선형 탄성으로 풀었다.
- 열역학적으로 유리한 반응일 뿐이다 — *"may occur during the formation of the interface, during the cycling of the battery, or be limited by kinetics"* (p.7). 계면상은 전자 절연이면 결국 성장을 멈춘다고 본다.
- '최악' 반응 선택 (p.7) · 분해는 전기화학 반응 **전에** (성막 중에) 일어난다고 가정 → t = 0 (p.5).
- 계면층은 전기화학 모델에는 넣지 않았다 — 나노미터 두께라 임피던스 영향이 작다고 봤다 (p.3).
- 응력이 전극 평형 전위에 주는 영향 무시 (p.4) · 변형이 물질 전달에 주는 영향 무시 · 확산계수 상수 (p.3) ⇒ **일방향 결합** (농도 → 응력).
- LiPON 자체의 Li 농도 변화에 따른 부피 변화 무시 (가동 Li 는 전체의 약 20 % · 충전 중 변화는 전체의 5 % 미만 · p.4 · p.6).
- 부피 변화는 등방 (p.5) · Li 농도–부피 관계는 선형 근사 (식 8).
- 공극은 직접 넣지 않고 측면 경계조건 두 극한으로만 (p.3). 크기를 잰 자료가 없어서다.
- 종료 조건 때문에 상변화 · 확산계수 변화가 없다 (p.4).
- LiPON = Li₂PO₂N (p.4) · N₂ 부피 제외 (p.7).

**들어 있지 않은 것 (본문에 없음을 확인)**

- 소성 · 크리프 · 점탄성: 없음. **균열 · 박리의 진전: 없음** — 최대 주응력의 위치와 크기만 본다. 파괴 인성 · 에너지 해방률 같은 파괴 기준도 없다.
- 계면층의 성장 속도 · 두께의 시간 변화: 없음 (두 두께를 손으로 넣었다).
- 계면층 고유의 탄성 상수 · 산물 혼합물의 물성: 적혀 있지 않다.
- 성막 잔류응력 · 외부 스택 압력 · 온도: 없음.
- 방전 · 반복 사이클의 응력: 없음 (방전 곡선이 맞는다는 말만 있고 그림은 없다 — *"not shown"*).

### Q7. 같은 환산을 아지로다이트에 하려면 필요한 입력

**(가) 논문 방법 그대로 따르면 필요한 것**

| # | 입력 | 논문에서의 출처 · 위치 |
|---|---|---|
| 1 | 전극의 Li 전위에서의 평형 산물 집합 (전압 창별) | MP grand-potential 상도 · p.4 · `Table 1` |
| 2 | 전극 상을 넣어 계수를 맞춘 **full reaction** — Li 를 주고받는 전극 상을 무엇으로 쓸지 포함 | `Table 1` · p.7 |
| 3 | 반응식의 **모든 고체상**의 화학식당 부피 | MP 값 · p.4 |
| 4 | 기체 산물 처리 규칙 | N₂ 제외 · p.7 |
| 5 | ΔV 정의 (분모 = 반응물 전체) 와 등방 변환 | 식 9 · 식 10 |
| 6 | 도메인별 등방 탄성 상수 E · ν (SE · 두 전극) | `Table 3` |
| 7 | 계면층 두께와 놓는 자리 | 10 · 50 nm 가정 · p.5 |
| 8 | 셀 기하와 구속 (경계조건) | `Fig. 1` · p.3 |
| 9 | 선형 탄성 정적 FEM | COMSOL 5.4 · p.3 |
| 10 | (충전 응력과 견주려면) 전극 팽창 계수 · 확산계수 · 반응 속도 상수 · 평형 전위 곡선 · 초기 농도와 충전 곡선 실험 대조 | 식 1–8 · `Table 3` · 식 A·1 · A·2 · `Fig. 2` |

**(나) 의견 — 논문에 없는 것** (전부 '의견' 이다)

- 의견: 1–2 는 우리에게 이미 반응식으로 있다 — ESW 사다리 (`litdb/our_dft_baseline.md`) 와 cascade 축 ① · ③ 의 닫힌계 최소 kink 반응 (`db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json` · `cascade_axis_li_anode_estimand_2026_11_04.json`). 축 ① · ③ 의 반응식은 'SE + 전극 상 → 산물' 꼴이라 식 9 를 그대로 얹을 수 있는 **같은 부류**다.
- 의견: 3 이 논문 방법의 빈자리다. 논문은 모든 상이 MP 에 있는 경우만 다뤘다. 도핑 조성은 MP 상이 아니므로 **호스트 · 도핑 셀의 부피는 우리 DFT (EOS V₀) 에서** 와야 하고, 산물상 부피는 MP 에서 올 것이다 → **두 출처의 부피를 한 식에 섞는 문제**가 생긴다 (범함수 · 판이 다르다).
- 의견: 4 는 아지로다이트 산화 쪽에서 결과를 좌우한다 (분자성 산물 · 기체). 0 으로 두면 수축이 부풀려진다 — 논문의 N₂ 제외와 같은 구조다.
- 의견: 5 의 분모 선택을 결과 전에 박아야 한다. 논문식 (반응물 전체) 과 SE 부피만으로 나누는 식은 음극 쪽에서 **부호가 반대로 나올 수 있다** (§13-3).
- 의견: 6 의 값은 원장에 있다 (`db/properties/canonical_registry.json` 의 `b0-dft-bm3-v1` · `elastic-dft-relaxedion-*` 묶음 — 여기 옮기지 않는다 · 조성 간 비교는 `HZ-elastic-cross-composition` 조건부). 등방 E · ν 로 줄이는 방식 (VRH) 은 이 논문과 같다.
- 의견: 7–9 는 스크리닝 목적이면 FEM 대신 **구속에 무관한 눈금**으로 대신할 수 있다 — 예: 층의 이축 구속 응력 E·ε/(1 − ν). 이 논문의 10 nm 값이 대체로 그 크기다 (§13-6).
- 의견: 균열 · 접촉 손실을 말하려면 **파괴 기준**이 따로 필요하다. 이 논문에는 없다. 갭 보고서가 든 정량 문턱은 `bucci2017_chemomech_failure_assb_cycling_czm` 의 것이다 (전극 팽창 기준 — SE 분해 기준이 아니다).

---

## 5. 모델 (방법) 전체

### 5.1 기하와 경계조건 (`Fig. 1` · p.3)

- 실물: 원뿔 미세기둥 기판 위에 LiCoO₂ 스퍼터 → LiPON 스퍼터 → Si 박막 (ref [28]). `Fig. 1a` 는 FIB 단면 SEM 이다 — Cu · Si · LiPON · LiCoO₂ · Pt 라벨, 눈금 막대 2 μm. 이웃 봉우리 사이에 **공극 (검은 틈)** 이 보인다 [봄].
- 모델: 육각 배열을 축대칭 단위 하나로 근사 (`Fig. 1b`). 위에서부터 음극 (Si · 하늘색) / 전해질 (LiPON · 파랑) / 양극 (LiCoO₂ · 보라).
- 바깥 경계: 집전체 · 연속 막과 닿는 면은 법선 변위만 막는다 (그림의 '원 + 삼각형' 기호).
- 공극 쪽 측면 (짧은 수평면 + 긴 수직면): **fixed side** / **free side** 두 극한. 공극 크기를 잰 자료가 없어서 양쪽으로 묶는다. ⚠ 'fixed' 가 변위를 전부 막는지 법선만 막는지는 문장으로 가를 수 없다.
- 계면층 안쪽 경계는 절점을 맞춰 완전 접합으로 둔다 (*"well-bonded interface formed by a Chemical Vapor Deposition (CVD) process"* — 앞에서는 스퍼터라고 했다).
- 치수 [figure-read ≈]: `Fig. 5` 의 눈금선 (2 · 4 μm) 에서 위쪽 막의 반지름 ≈ 1.8 μm · 전체 높이 ≈ 5.5 μm · 기둥부 바깥 반지름 ≈ 1.2 μm · Si 막 ≈ 0.3 μm · 그 아래 LiPON 막 ≈ 0.5 μm. `Table 3` 의 Si 단면적 1.02 × 10⁻¹¹ m² 를 원으로 보면 반지름 1.80 μm 로 맞는다 [우리 산술]. ⇒ 50 nm 계면층은 막 두께의 10–20 % 다 — '얇은 층' 이 아니다.

### 5.2 전기화학 — Li 농도장 (p.3–4)

| 영역 | 식 | 내용 |
|---|---|---|
| 전극 (Si · LiCoO₂) | 식 1 | Fick 확산 ∂C/∂t + ∇·(−D∇C) = 0. Si 는 등방 · LiCoO₂ 는 이방 (면 방향 ≠ 법선 방향) · D 는 상수 |
| LiPON | 식 2–3 | Nernst–Planck (확산 + 전기 이동) + 전기중성 Σ ZᵢCᵢ = 0. 가동 이온은 Li⁺ 뿐 (수송수 1) · 음전하는 국소 고정 |
| 계면 | 식 4–6 | Butler–Volmer. 교환 전류 i⁰ = F k [(C_max − C)·C_Li⁺ / ((C_max − C_min)·C⁰_Li⁺)]^α · [C/C_max]^(1−α) · 과전압 η = φ_전극 − φ_전해질 − E_전극 |
| 정전류 | 식 7 | 두 계면을 지나는 총전류가 같다. 다른 면은 무유속. 전류밀도는 투영 면적 기준 |

- 평형 전위 E_전극 은 맞춘 다항식이다 (부록 식 A·1 · A·2 · ref 45). [우리 산술] 식 A·1 은 x = 0 에서 0.62 V · x = 3.75 에서 0.13 V 이고 모사 범위 x = 1.69–2.0 에서 **0.33–0.30 V** 다. 식 A·2 는 y = 0.5 에서 4.25 V · y = 0.9 에서 3.45 V · 초기 조성 y = 0.98 에서 **2.34 V** 다 → 초기 셀 전압 ≈ 2.0 V 로 `Fig. 2` 의 모사선 시작점과 맞는다.
- 종료 조건: 4.2 V 도달 또는 전극 어느 점에서든 x = 3.75 (LiₓSi) 나 y = 0.5 (LiᵧCoO₂) 도달.
- 응력 계산은 **농도 스냅숏을 정적 문제에 넣는** 방식이다. 고체 확산이 탄성 변형보다 훨씬 느리다는 것이 근거다 (refs 46, 47).

### 5.3 부피 변화의 두 원천 (p.4)

**(i) Li 농도** — 식 8: ΔV_Li = a_v · ΔC_Li (비선형 관계를 비례로 근사).
- Si: Si → Li₃.₇₅Si 에서 **263 %** 팽창 (ref 3) → a_v = 8.45 × 10⁻⁴ %/(mol m⁻³).
- LiCoO₂: y 0.5 → 1 에서 **+2 %** (ref 3 · meta-GGA [SCAN · ref 50] 의 추세와 맞는 쪽을 골랐다. DFT 방법에 따라 추세가 다르다고 적는다) → a_v = 8 × 10⁻⁵.
- LiPON: 무시.

**(ii) SE 분해** — 식 9: ΔV_d = (V₂ − V₁)/V₁. Q2 의 표 그대로다.
- 충전하면 Si 는 리튬화되고 Li 전위는 0.6 → 0.1 V 로 내려간다 (x = 0 → 4). LiCoO₂ 는 2.5–4.2 V 범위에서 올라간다 (y = 1 → 0.5).
- 그 전위마다 Li₂PO₂N 의 평형 산물이 다르다 → `Table 1`.

### 5.4 계면층과 역학 (p.5)

- 두께 10 nm · 50 nm 의 근거: SEI 의 전형 두께 10–100 nm (refs 55, 56 — 액체 전해질 SEI 리뷰) + 계면이 사이클 전에 약 50 nm 라는 실험 (ref 57 · 원문 표기는 *"LiPON/Si and Li/LiCoO2 interfaces are both around 50 nm before cycling"* — 뒤쪽은 LiPON/LiCoO₂ 의 오기로 읽힌다).
- 분해 응력은 확산 응력과 **따로** 계산한다. 분해가 전기화학 반응 전에 (성막 중에) 일어난다고 보고 t = 0 에 둔다 (ref 38).
- 식 10–13: Q3 의 표 그대로다.

### 5.5 매개변수 (`Table 3` = 원문 Table A·I · p.10 전사)

| 기호 | 뜻 | 값 | 출처 |
|---|---|---|---|
| C⁰_Li⁺ | Li₂PO₂N 의 초기 Li 이온 농도 | 2 × 10⁴ mol m⁻³ | [28] |
| C⁰_Li,neg | LiₓSi 초기 Li 농도 | 1.4 × 10⁵ mol m⁻³ (x ≈ 1.69 [우리 산술]) | [28] |
| C⁰_Li,pos | LiᵧCoO₂ 초기 Li 농도 | 4.9 × 10⁴ mol m⁻³ (y = 0.98 [우리 산술]) | [28] |
| a_v,Si | Si 부피 변화 계수 (Si ↔ Li₃.₇₅Si) | 8.45 × 10⁻⁴ %/(mol m⁻³) | [3] |
| a_v,LCO | LiCoO₂ 부피 변화 계수 (Li₀.₅CoO₂ ↔ LiCoO₂) | 8 × 10⁻⁵ %/(mol m⁻³) | [3] |
| D_Li,Si | LiₓSi 의 Li 확산계수 | 1 × 10⁻¹⁸ m²/s | [28] |
| D_Li,LCO (normal) | LiᵧCoO₂ 법선 방향 | 2.5 × 10⁻¹⁸ m²/s | [28] |
| D_Li,LCO (lateral) | LiᵧCoO₂ 면 방향 | 1 × 10⁻²¹ m²/s | [28] |
| D_Li⁺ · D_n | Li₂PO₂N 의 Li 이온 · 음전하 확산계수 | 각 5 × 10⁻¹⁷ m²/s | [28] |
| α_neg · α_pos | 전하 전달 계수 | 각 0.5 | [28] |
| C_Li,neg,max · min | LiₓSi 최대 · 최소 농도 | 3.11 × 10⁵ · 0 mol m⁻³ | [28] |
| C_Li,pos,max · min | LiᵧCoO₂ 최대 · 최소 농도 | 5 × 10⁴ · 2.5 × 10⁴ mol m⁻³ | [28] |
| k_neg · k_pos | 계면 반응 속도 상수 | 1 × 10⁻² · 1 × 10⁻⁴ mol (m² s)⁻¹ | [28] |
| Z_Li⁺ · Z_n | 전하수 | +1 · −1 | [28] |
| E · ν · ρ (Si) | 탄성률 · 푸아송비 · 밀도 | **96 GPa** · 0.29 · 2209 kg m⁻³ | [3] · [3] · [69] |
| E · ν · ρ (LiCoO₂) | 같음 | **191 GPa** · 0.24 · 4790 kg m⁻³ | [70] |
| E · ν · ρ (LiPON) | 같음 | **77 GPa** · 0.25 · 2300 kg m⁻³ | [71] · [71] · [72] |
| A | Si 전극 단면적 | 1.02 × 10⁻¹¹ m² | [28] |

- 표 제목: *"Most of the values were obtained either by fitting to experiments [28] or by DFT predictions [3]."*
- [우리 산술] 검산: 263 % ÷ 3.11 × 10⁵ = 8.46 × 10⁻⁴ ✓ · 2 % ÷ 2.5 × 10⁴ = 8 × 10⁻⁵ ✓ · 3.75 ÷ 3.11 × 10⁵ mol m⁻³ = 12.06 cm³/mol = 결정 Si 의 몰부피 → C_max 는 리튬화 전 Si 부피 기준이다.
- ⚠ 표와 본문이 어긋나는 곳 [봄]: 본문 (p.3) 은 *"Li diffuses laterally along the LCO surface about three orders of magnitude **faster** than normal to it"* 라고 하는데 표는 법선 2.5 × 10⁻¹⁸ > 면 방향 1 × 10⁻²¹ 이다. 둘 중 하나의 라벨이 뒤바뀌었다.
- ⚠ Si 의 탄성률은 값 하나다 (96 GPa). 출처 ref [3] 의 제목은 'Li 농도 의존 탄성' 인데 모델은 농도 의존성을 쓰지 않는다 [봄]. LiPON 77 GPa 는 박막 나노압입 측정값이다 (ref 71 의 제목) — 부피는 결정 Li₂PO₂N, 탄성은 실물 박막에서 왔다.

---

## 6. 결과

### 6.1 충전 곡선 대조 (`Fig. 2` · p.5)

- 축: 전압 2–4.5 V · 용량 0–25 μAh/cm². 모사선 3 개 (검정 28 · 빨강 14 · 파랑 3.7 μA/cm² = 1.2 C · 0.6 C · 0.16 C) 와 실험점 (별 · 원 · 마름모 · ref [28]).
- 본문: 4 V 에서 본 종지 용량 0.038 · 0.092 · 0.22 Ah m⁻² (= 3.8 · 9.2 · 22 μAh/cm²) 가 실험과 *"satisfactory agreement"* · 방전 곡선도 맞는다 (그림 없음).
- [우리 산술] 28 μA/cm² × 480 s = 3.73 μAh/cm² ✓ (종료 시각과 맞는다).
- ⚠ 그림을 보면 [figure-read ≈] **초반 전압은 모사가 실험보다 낮다.** 28 μA/cm²: 첫 실험점 (≈ 0.36 μAh/cm² · 3.74 V) 에서 모사선은 ≈ 3.35 V (선이 가파른 구간이라 ± 0.1 V) → 차 ≈ 0.4 V · 0.7 μAh/cm² 에서 ≈ 0.3 V · 1.4 에서 ≈ 0.15 V · 2.1 에서 ≈ 0.1 V · 끝에서 겹친다. 3.7 μA/cm²: 2.5–15 μAh/cm² 구간에서 ≈ 0.09–0.13 V 낮고 20 이후 겹친다. 14 μA/cm²: 1 μAh/cm² 에서 ≈ 0.15 V 낮다. 맞는 것은 **종지 용량과 끝부분**이다. 응력 평가에 쓴 것이 바로 가장 어긋나는 28 μA/cm² 곡선이다.
- 그림에 10 s · 240 s · 480 s 원 표시가 있다 (`Fig. 3` · `Fig. 4` 의 세 시각).

### 6.2 Li 농도장 (`Fig. 3` · p.6)

- 가운데 = 240 s 의 3D 단면. 위쪽 확대 3 장 = Si/LiPON 가장자리 · 아래쪽 확대 3 장 = LiCoO₂ 꼭대기 (10 · 240 · 480 s). LiPON 안의 화살표 = Li⁺ 이동 방향 (LiCoO₂ → Si).
- 색 막대 3 개: LiCoO₂ 의 Li 2.5–5 (Li₀.₅CoO₂ ~ LiCoO₂) · LiPON 의 Li 이온 1.4–2.6 · Si 의 Li 1.4–1.8 (Li₁.₆₈Si ~ Li₂.₁₇Si).
- 충전은 480 s 에 LiCoO₂ 가 y = 0.5 에 닿아 끝난다. 농도 변화는 **계면 근처 얇은 경계층에만** 생긴다 [봄 — 확대 그림에서 Si 아래쪽 남색 띠 · LiCoO₂ 표면 흰 테두리가 시간에 따라 두꺼워진다]. Si 는 x = 1.68 → 2.
- LiPON 의 Li 이온 농도 변화는 ± 5 × 10³ mol m⁻³ 로 전체 Li (1 × 10⁵) 의 약 5 % → LiPON 화학 변형 무시가 정당하다는 것이 본문 논리다. 그림에서도 Si 쪽 LiPON 은 옅어지고 (고갈) LiCoO₂ 꼭대기 쪽은 짙어진다 (축적) [봄].
- ⚠ 색 막대 단위 표기 [봄]: 그림에는 LiPON 막대 아래 `×10⁵` · Si 막대 아래 `×10⁴` 로 적혀 있다. `Table 3` (LiPON 초기 2 × 10⁴ · Si 초기 1.4 × 10⁵ mol m⁻³) 과 본문 (± 5 × 10³) 에 맞추려면 **둘이 뒤바뀌어야** 한다.

### 6.3 충전이 만드는 응력 (`Fig. 4` · p.6–7)

- 6 장 (fixed / free × 10 · 240 · 480 s) · 색 막대 −5 ~ +5 GPa (빨강 = 인장).
- [봄] 10 s: Si/LiPON 계면을 따라 가는 파란 선 하나뿐. 240 · 480 s: Si 의 리튬화된 얇은 층이 **짙은 파랑 (압축)** · LiCoO₂ 표면을 따라 **옅은 빨강 선 (탈리튬화층 인장)** · 위쪽 막 양 끝 (Si/LiPON 가장자리) 에 옅은 빨강 — free side 480 s 에서 가장 뚜렷하다. LiPON 대부분은 0 근처이거나 약한 압축이다.
- 본문: Si 의 변형이 LiCoO₂ 보다 크다 (x 1.68 → 2 에서 약 +23 % ↔ −2 %). fixed 와 free 는 두 가지만 다르다 — free 는 LiCoO₂ 꼭대기 위의 압축을 풀어 주고, Si 팽창을 받는 가장자리 LiPON 의 인장이 free 에서 더 크다. 충전 끝의 최대 인장은 Si 가 아니라 **LiPON** 에 생긴다.

### 6.4 분해 반응과 부피 변화 (`Table 1` = 원문 Table I · p.5 전사)

| 상대 전극 | 전압 창 (V) | 반응 | 부피 변화 | SE 화학식당 Li 수수 [우리 산술] |
|---|---|---|---|---|
| LiₓSi | 0–0.01 | 21 Li₂PO₂N + 8 Li₂₁Si₅ → 42 Li₂O + 21 Li₃N + 21 Li₃P + 40 Si | −19 % | +8 |
| LiₓSi | 0.01–0.53 | 52 Li₂PO₂N + 24 Li₁₃Si₄ → 104 Li₂O + 13 Li₇PN₄ + 39 Li₃P + 96 Si | −24 % | +6 |
| LiₓSi | (빈칸 — 위와 같은 창) | 28 Li₂PO₂N + 24 Li₇Si₃ → 56 Li₂O + 7 Li₇PN₄ + 21 Li₃P + 72 Si | −23 % | +6 |
| LiₓSi | (빈칸 — 위와 같은 창) | **4 Li₂PO₂N + 2 Li₁₂Si₇ → 8 Li₂O + Li₇PN₄ + 3 Li₃P + 14 Si** | **−27 %** | +6 |
| LiₓSi | (빈칸 — 위와 같은 창) | 4 Li₂PO₂N + 24 LiSi → 8 Li₂O + Li₇PN₄ + 3 Li₃P + 24 Si | −29 % | +6 |
| LiₓSi | 0.53–0.65 | 6 Li₂PO₂N + 32 LiSi₃ → Li₁₄P₂(N₂O)₃ + 9 Li₂O + 4 Li₃P + 96 Si | −22 % | +5.33 |
| LiᵧCoO₂ | 2.64–3.04 | 7 Li₂PO₂N + 24 Li₀.₇₅CoO₂ → 2 Li₄P₂O₇ + P₃N₅ + N₂ + 24 LiCoO₂ | −2 % | −0.86 |
| LiᵧCoO₂ | > 3.63 | **3 Li₂PO₂N + 12 Li₀.₅CoO₂ → P₂O₅ + PNO + N₂ + 12 LiCoO₂** | **−8 %** | −2 |

- 굵은 두 행이 모델에 들어간 것이다 (원문도 굵게). `Fig. 1d` 에 같은 두 반응이 그려져 있다.
- 여덟 반응식의 원소 균형은 전부 맞는다 [우리 산술].
- 본문 (p.7): Si 쪽은 모든 행이 수축이다. Si 가 LiSi · Li₁₂Si₇ · Li₇Si₃ · Li₁₃Si₄ · Li₂₁Si₅ 로 갈수록 전위가 내려가고 반응이 바뀐다 (refs 58, 59). 모사한 Li 범위 (Li₁.₆₈Si–Li₂Si) 안의 '최악' = Li₁₂Si₇ 행 −27 %. LiCoO₂ 쪽 '최악' = −8 %.
- 🔗 우리 `zhu2015_esw_grand_potential_origin` digest 의 SI 표 S2(h) (같은 Li₂PO₂N · 같은 방법) 와 대조 [봄 — 두 digest 사이]:
  - 환원 3 단의 산물 · Li 수수가 일치한다 (+8: Li₃P · Li₃N · Li₂O / +6: Li₃P · Li₇PN₄ · Li₂O). 맨 위 단만 다르다 — [Zhu15] 는 0.68 V 에서 LiPN₂ (+4), 이 논문은 0.65 V 에서 Li₁₄P₂(N₂O)₃ (+5.33). MP 판 차이로 읽힌다 [추정].
  - 산화 첫 단 (2.63–2.64 V · P₃N₅ + Li₄P₂O₇ + N₂ · −0.86) 과 마지막 단 (3.63 V · PON + P₂O₅ + N₂ · −2) 이 일치한다.
  - ⚠ **이 논문의 표에는 3.04–3.63 V 구간이 없다.** [Zhu15] SI 에는 그 사이에 단이 더 있다 (2.75 · 2.77 · 3.05 V — P₄ON₆ · LiPO₃ · PON 조합). 표가 사다리 전체가 아니라 **고른 단**이라는 뜻이다.
  - `PNO` 표기는 [Zhu15] 본문 Table 3 과 같은 표기다 (그 digest 의 판정: 인산질화물 PON).
- 'LiSi₃' · 'Li₁₄P₂(N₂O)₃' 는 원문 표기 그대로다. LiSi₃ 가 어떤 MP 항목인지는 본문에 없다.

### 6.5 분해가 만드는 응력 (`Fig. 5` · `Table 2` = 원문 Table II · p.7–8)

`Table 2` 전사 — 도메인별 최대 제1주응력 (GPa):

| 측면 조건 | 도메인 | 계면층 50 nm | 계면층 10 nm |
|---|---|---|---|
| Fixed side | Si 전극 | 14.7 | 12.6 |
| Fixed side | LiCoO₂ 전극 | 3.64 | 1.80 |
| Fixed side | LiPON 전해질 | **26.8** | **9.90** |
| Free side | Si 전극 | 14.5 | 12.5 |
| Free side | LiCoO₂ 전극 | 3.34 | 1.68 |
| Free side | LiPON 전해질 | 12.1 | 9.89 |

- `Fig. 5` [봄]: 왼쪽 = 메시와 분홍색 계면층 두 줄 (위쪽 수평선 = Si/LiPON · 뒤집힌 U = LiCoO₂/LiPON). 오른쪽 4 장 = 10 nm · 50 nm × fixed · free. **색 막대가 ± 5 GPa 에서 잘린다** — 표의 9.9–26.8 GPa 는 그림에서 읽을 수 없고, 그림은 분포만 보여 준다.
  - 10 nm: 계면층 선만 빨갛고 나머지는 회색 (≈ 0) 에 가깝다.
  - 50 nm fixed: 위쪽 막 전체가 빨강 (2–4 GPa 대) · 다리 부분도 옅은 빨강.
  - 50 nm free: 위쪽 막은 빨강이지만 다리의 계면층 바깥은 회색으로 돌아간다.
  - **가장 짙은 점은 위쪽 계면층 선의 양 끝 (측면 경계와 만나는 자리) 과 T 자 팔 아래 오목 모서리**다.
- 본문: 수축이라 셀 대부분이 인장이다. 3 GPa 를 넘는 영역이 두께와 함께 커진다. LiCoO₂ 쪽 계면상은 두 조건 모두 약 3 GPa. Si · LiPON 은 fixed 에서 더 크다. *"The large stress level above 3 GPa corresponds to 3%, 1.5% and 3.8% of elastic strain in Si, Li2CO3 [원문 그대로 — LiCoO₂ 의 오기], and LiPON"* → [우리 산술] 3 GPa ÷ E = 3.1 · 1.6 · 3.9 % 로 맞는다.
- 최대 응력의 자리 (p.8): 위쪽 Si · LiPON 연속 막은 공극 위에서 **다리**가 된다. 그 다리의 한가운데가 모델에서는 위쪽 막의 **양 옆 끝**이고 Si · LiPON 의 최대 응력이 거기서 난다 — 그림과 맞는다 [봄].
- 전해질 최대 응력은 fixed 26.8 → free 12.1 GPa 로 떨어진다. 대부분의 응력이 위쪽에 몰리는 것은 Si 쪽 (−27 %) 이 LiCoO₂ 쪽 (−8 %) 보다 훨씬 커서다.

### 6.6 두 원천의 비교 (`Fig. 6` · p.9)

- 축: 최대 제1주응력 (GPa · 끊긴 축 0–4 / 12–15 / 26–28) · 충전 시간 0–500 s.
- 'Decomposition' 표식 6 개 (t ≈ 0) = `Table 2` 의 50 nm 값. 'Charging' 선 6 개 = 1.2 C 충전 중 도메인별 최댓값.
- 충전 선 [figure-read ≈ · 478 s]: LiPON free (파랑 점선) **1.9** · LiPON fixed (파랑 실선) **1.4** · LiCoO₂ (초록 · 두 조건 겹침) 0.9 · Si (빨강 · 두 조건 겹침) 0.8 GPa. 선은 480 s 에서 끝난다.
- 비교표와 조건은 Q4.
- ⚠ 본문 · 결론은 충전 응력이 측면 조건과 무관하게 *"very similar"* 하다고 하지만, 그림에서 **LiPON 은 free 가 fixed 보다 ≈ 0.5 GPa (약 1.4 배) 크다** [봄]. Si · LiCoO₂ 는 실제로 겹친다.

### 6.7 저자 논의 · 결론 (p.9)

- 어느 경우든 균열이 날 곳은 최대 주응력이 생기는 **LiPON** 이다. 균열이 조금 나도 전도 경로가 남으면 작동하지만 임피던스가 오른다.
- 완화책 셋: 계면 코팅으로 분해를 줄인다 (refs 60–62) · 고분자나 고분자 복합 전해질처럼 **더 무른 재료**로 구속을 푼다 (refs 63–65) · 정합 구조나 **의도적 내부 공극** 같은 구조 최적화 (refs 66–68).
- 결론 문장: 50 nm 계면층 형성이 Si · LiCoO₂ 계면에서 −27 % · −8 % 의 부피 감소를 주고 셀 대부분에 3 GPa 넘는 인장을 만든다. 측면에 공극이 있으면 전해질의 최대 주응력이 크게 준다. 충전이 만드는 응력은 더 작고 LiCoO₂ 표면층과 Si 근처 LiPON 에만 걸린다. *"Both will depend largely on the electrode/electrolyte materials used in ASSLB."*

---

## 7. DFT/계산 방법 ★

- **code / version**: 자체 DFT 없음. 연속체 = **COMSOL Multiphysics 5.4** (Electrochemistry + MEMS 모듈).
- **functional · vdW**: 미기재. 분해 반응의 에너지와 부피는 Materials Project 값을 API 로 받았다 (refs 53, 54) — MP 판 · 범함수 · 보정 언급 없음. LiCoO₂ 부피 추세만 meta-GGA (SCAN · ref 50) 쪽을 택했다고 적는다.
- **pseudo / PAW · k-points · ecut · supercell**: 해당 없음 (자체 계산 0).
- **DFT+U**: 미기재.
- **AIMD · MLIP**: 없음.
- **무질서 처리**: 없음. 비정질 LiPON 을 **결정 Li₂PO₂N 하나**로 대표했다.
- **상도 방법**: grand-potential 상도에서 전극 Li 전위별 평형상 (refs 37, 38) → 전극 상을 넣은 full reaction 으로 다시 씀.
- **FEM**: 축대칭 · 요소 11,000–290,000 시험 · > 200,000 에서 최대 주응력 0.5 % 이내 (`Fig. S1` · SI · 미입수) · 선형 등방 탄성 · 정적 평형 · 미소변형.
- **결합 방식**: 일방향. 시간 의존 전기화학 (Newman 형 · refs 39, 40) → 농도 스냅숏 → 정적 응력. 분해 응력은 별도 계산 (t = 0).
- **특이사항**: 초록은 *"predicted by density functional theory (DFT) calculations"* 라고 쓰지만 본문의 실제 절차는 **MP 자료 조회**다.

---

## 8. Post-processing ★

- **무엇**: Li 농도장 (세 시각) · 제1주응력 분포 · 도메인별 최대 제1주응력 · 두 원천의 시간축 비교.
- **도구**: COMSOL 후처리 · MP API (반응 · 부피).
- **식 (본문 전사)**
  - (1) ∂C_Li/∂t + ∇·(−D_Li ∇C_Li) = 0
  - (2) ∂Cᵢ/∂t + ∇·(−Dᵢ ∇Cᵢ − Zᵢ (Dᵢ/RT) F Cᵢ ∇φ_전해질) = 0
  - (3) Σ Zᵢ Cᵢ = 0
  - (4) i = i⁰ [exp(−αFη/RT) − exp((1 − α)Fη/RT)]
  - (5) i⁰ = F k [(C_max − C_Li) C_Li⁺ / ((C_max − C_min) C⁰_Li⁺)]^α [C_Li/C_max]^(1−α)
  - (6) η = φ_전극 − φ_전해질 − E_전극
  - (7) I_total = ∫ i_neg dA = ∫ i_pos dA
  - (8) ΔV_Li = a_v ΔC_Li
  - (9) ΔV_d = (V₂ − V₁)/V₁
  - (10) ε_c,ij = ((1 + ΔV)^(1/3) − 1) δ_ij
  - (11) ∇·σ = 0 · (12) σ = C : ε_el = C : (ε − ε_c) · (13) ε = ½[∇u + (∇u)ᵀ]
  - (A·1) E_neg(a) = −4.76a⁶ + 9.34a⁵ − 1.8a⁴ − 7.13a³ + 5.8a² − 1.94a + 0.62 · a = C/C_max (x = 0–3.75)
  - (A·2) E_pos(b) = (207.168b¹⁰ − 467.807b⁸ + 354.911b⁶ − 198.242b⁴ + 322.003b² − 219.027) / (80.310b¹⁰ − 182.567b⁸ + 113.081b⁶ − 3.43b⁴ + 35.463b² − 44.337) · b = C/C_max (0.5–1)
- **수치화 · 기록**: 본문에 표 2 장 (`Table 1` · `Table 2`) + 부록 표 1 장 (`Table 3`). COMSOL 입력은 SI (미입수). 응력 분포 그림의 색 막대는 ± 5 GPa 에서 잘려 있어 최댓값은 표로만 준다.

---

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a–d | (a) 2.5D 셀 FIB 단면 SEM (Cu · Si · LiPON · LiCoO₂ · Pt · 눈금 2 μm · 봉우리 사이 공극) (b) 축대칭 모델 · 메시 · 롤러 경계 기호 (c) 충전 중 변형: Li₁₂Si₇ → Li₂Si +23 % · LiCoO₂ → Li₀.₅CoO₂ −2 % (d) 분해 반응 두 개와 −27 % · −8 %. **봄** | '변형의 두 원천' 을 한 장에 놓는 도식 꼴 — 분해 부피를 다룰 때 전극 변형과 나란히 그리는 선례 |
| 2 | 충전 곡선 모사 ↔ 실험 (3.7 · 14 · 28 μA/cm²) · 전압 2–4.5 V · 용량 0–25 μAh/cm². 초반 전압은 모사가 낮다 (28 μA/cm² 첫 점에서 ≈ 0.4 V). **봄 + 픽셀 판독** | 'satisfactory agreement' 가 끝점 용량의 일치라는 것 — 모델 검증 문장을 읽을 때의 예 |
| 3 | 1.2 C 충전의 Li 농도장 (10 · 240 · 480 s) · 3D 단면 + 확대 6 장 · 색 막대 3 개. 변화는 계면 경계층에만. LiPON · Si 막대의 단위 지수가 뒤바뀌어 적혔다. **봄 (확대 재렌더 1 회)** | 충전 응력이 작게 나온 이유 (표면층만 반응하고 480 s 에 끝난다) 의 직접 근거 |
| 4 | 충전이 만드는 제1주응력 (fixed · free × 3 시각) · 색 막대 ± 5 GPa. 리튬화 Si 층 압축 · LiCoO₂ 표면층 인장 · 위쪽 막 양 끝 인장. **봄** | 박막 구속에서 팽창층은 압축 · 이웃은 인장이 되는 분포의 예 |
| 5 | 분해가 만드는 제1주응력 (10 · 50 nm × fixed · free) + 계면층 두 줄을 표시한 메시. 색 막대가 ± 5 GPa 에서 잘린다. 가장 짙은 점 = 위쪽 계면층 선의 양 끝과 오목 모서리. **봄** | ⭐ 최대값 (26.8 GPa) 이 **가장자리 · 모서리 집중**이라는 것 — 숫자를 인용할 때 붙일 단서 |
| 6 | 분해 (t = 0 표식 · 50 nm) ↔ 충전 (선 · 0–480 s) 의 도메인별 최대 제1주응력 · 끊긴 축. 충전 선 끝 ≈ 0.8–1.9 GPa. **봄 + 픽셀 판독 (표식 중심으로 축 검산)** | 논문 주장 전체가 이 한 장이다 — 조건 (50 nm · 최악 반응 · 480 s) 을 같이 적어야 한다 |
| Table 1 (원문 Table I) | Li₂PO₂N 의 전위 창별 분해 반응 8 줄과 부피 변화 (−19 ~ −29 % · −2 · −8 %). **손 크롭 확인 + 텍스트 전사** | ⭐ '전극 상을 넣은 닫힌 반응식 · 반응물 전체 정규화 · 기체 제외' 회계의 실례 — 우리 보고량 카드의 회계 선택지 |
| Table 2 (원문 Table II) | 도메인 × 측면 조건 × 계면층 두께별 최대 제1주응력 (1.68–26.8 GPa). **손 크롭 확인 + 텍스트 전사** | 초록 수준 값 26.8 · 9.90 GPa 의 조건 (fixed side · LiPON 도메인) 확인 |
| Table 3 (원문 Table A·I) | 모사 매개변수 전부 (농도 · 확산 · 반응 속도 · E · ν · ρ · 단면적). **손 크롭 확인 + 텍스트 전사** | 환산에 필요한 입력 목록의 원형 (§4 Q7) |

---

## 10. 우리 DFT 대비 → `our_dft_baseline.md` · `db/properties/` 원장

> 규율: 문헌 수치는 소환값이다. 아래 '우리' 칸에는 **값을 싣지 않고 원장 경로와 정의만** 적는다. 원장과 어긋나면 원장이 이긴다.
> 이 논문에는 아지로다이트 물성값이 하나도 없다 → `comparison_vs_ours.md` 의 A–D 물성 4축에는 행을 만들지 않는다 (§J-73 방법 원전 블록에만).

### 10.1 방법 · 정의 대조표

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 계 | Si / LiPON (결정 Li₂PO₂N) / LiCoO₂ 2.5D 박막 셀 | Li₆PS₅Cl 계열 (comp1 · modelc · 도핑 설계) 벌크 · 계면 스크리닝 | ⛔ 겹치는 계 0. 수치 이식 불가 |
| 분해 산물의 출처 | MP grand-potential 평형상 (refs 37, 38) | ESW 사다리 = grand-potential (`our_dft_baseline.md` · 상 배제 규약 포함) / cascade 축 ① · ③ = MP **닫힌계 pseudo-binary 최소 kink** | 방법 계보는 같다 ([Zhu15] · [Rich16]). 논문은 열린계로 산물을 고르고 닫힌 반응식으로 다시 쓴 혼합형이다 |
| 반응식의 꼴 | SE + **전극 상** → 산물 + 탈리튬화/리튬화된 전극 상 | 축 ③: 도핑 조성 + Li 금속 / 축 ①: 도핑 조성 + Li₀.₅NiO₂ (hull 조성) | 같은 부류 (전극 상이 식 안에 있다). Li 저장소가 다르다 — 논문은 Li–Si 합금 · LiᵧCoO₂ |
| 부피 | MP 결정 부피 (판 · 범함수 미기재) | 호스트 · 도핑 셀 = 자체 DFT EOS V₀ (원장 `b0-dft-bm3-v1` 묶음) · **산물상 부피는 아직 보고량에 없다** | 우리 쪽에 없는 열이다. 만들 때 두 출처 (자체 DFT ↔ MP) 를 섞게 된다 |
| 부피 변화의 분모 | 반응물 전체 (SE + 전극 상) | 미정 — 보고량 카드 전 | 분모가 부호를 바꿀 수 있다 (§13-3) |
| 기체 | N₂ 제외 | 미정 | 아지로다이트 산화 쪽은 분자성 · 기체 산물이 더 많다 |
| 탄성 상수 | 문헌 등방 E · ν (LiPON 은 박막 나노압입) | DFT C_ij → VRH · EOS B₀ (원장 `elastic-dft-relaxedion-*` · `b0-dft-bm3-v1` · 조성 간 비교는 `HZ-elastic-cross-composition` 조건부) | 값은 옮기지 않는다. 논문의 LiPON 은 황화물보다 훨씬 단단한 부류다 → 같은 변형률이면 선형 탄성 응력은 탄성률에 비례해 달라진다 (의견) |
| 계면층 두께 | 10 · 50 nm 가정 | 계산한 적 없다 | 논문도 가정이다 (액체 SEI 리뷰 + 실험 1 편) |
| 구속 | 박막 · 집전체 롤러 · 공극 측면 fixed / free | 분말 압착 셀 · 스택 압력 | 기하가 다르다 — 박막의 '완전 접합 + 롤러' 는 구속의 상한 쪽이다 |
| 전위 | 음극 Si 0.3 V 대 · 양극 쪽 > 3.63 V 단 선택 | 양극 쪽 판단은 셀 작동창 2.5–4.25 V (CLAUDE.md §데이터 규율) | 논문의 두 산화 단은 모두 우리 창 안의 전위다. 계가 달라 대응은 없다 |
| 응력 지표 | 최대 제1주응력 (파괴 기준 없음) | 없음 | — |

### 10.2 트랙별 판정 — 지지 · 반박 · 무관

| 우리 판정 · 트랙 | 이 논문과의 관계 | 근거 |
|---|---|---|
| **cascade 갭 보고서 B — '아지로다이트 분해 ΔV/V 를 응력 · 균열 위험으로 바꾼 연구는 없다'** | 🟢 **살아 있다 (이 논문이 깨지 않는다)** | 푼 계가 LiPON 하나 · 황화물 0 · 도펀트 0 (§4 Q1) |
| 같은 보고서 — '분해 부피를 응력으로 바꾼 연속체 모델은 Tian 2020 이 사실상 유일' | ⚪ 이 논문으로는 확인 불가 | 유일한지는 다른 문헌의 문제다. 단 **절차 자체는 2020 년에 이미 있다** → B 의 새로움은 '환산을 처음 한다' 가 아니라 '아지로다이트 · 도펀트별로, 회계를 밝혀서 한다' 쪽이다 |
| 같은 보고서 — 'LiPON 약 −27 % · 26.8 GPa · 9.90 GPa' | 🟡 **값은 맞고 단서가 필요하다** | −27 % = 전극 상 포함 반응식 전체 · 최악 행 / 26.8 · 9.90 GPa = fixed side · LiPON 도메인 / 가장자리 집중 · 선형 탄성 (§4 Q3 · §13) |
| 같은 보고서 — '세 문헌이 서로 다른 회계로 서로 다른 부호' | 🟢 **지지 + 네 번째 실례** | 같은 SE 반응이 합금상 선택만으로 −23 ~ −29 % (`Table 1`) · N₂ 제외 · 분모 = 반응물 전체. [Wang26IF] 의 화학 반응 ΔV/V (두 반응물 전체로 나눔) 와 같은 부류이고 [GG] 의 ε_RXN (SE 부피로 나눔) 과 다르다 |
| 같은 보고서 — '양극 쪽 산화 수축 → 접촉 손실이 가장 단단한 자리' | ⚪ 무관에 가깝다 (같은 부호의 다른 계) | LiPON/LiCoO₂ 도 수축 (−2 · −8 %) 이지만 산화물이고 기체 제외가 수축에 들어 있다. 황화물의 근거가 아니다 |
| ESW 값 (`our_dft_baseline.md` 의 산화 onset · 환원 한계) | ⚪ 무관 | 아지로다이트 값 없음. 방법 계보만 같다 |
| 탄성 원장 (`canonical_registry.json`) | ⚪ 무관 | 탄성 상수를 계산하지 않았다 (문헌값 입력) |
| MLIP-MD 규약 · UMA | ⚪ 무관 | MD · MLIP 없음 |
| 장벽 홉 수 · MD 관측창 · 흡착 배위수 규율 | ⚪ 해당 없음 | 장벽 · MD · 흡착 계산이 없다 |

### 10.3 litdb 의 관련 digest 와 엮기

| digest | 이 논문과의 관계 |
|---|---|
| `zhu2015_esw_grand_potential_origin` | ref [37]. 같은 Li₂PO₂N 사다리 — 이 논문 `Table 1` 은 그 사다리에서 단을 골라 전극 상을 붙인 것이다 (§6.4) |
| `zhu2016_first_principles_interface_stability_assb` | ref [38]. '분해는 성막 중에도 일어난다' 의 근거로 인용 (p.5). 그 편은 반응 에너지만 내고 **부피는 계산하지 않았다** (그 digest §4.5) — 부피를 붙인 것은 이 논문이다 |
| `richards2016_interface_stability_pseudobinary` | 닫힌 · Li 열린 pseudo-binary 의 정의 원전. 이 논문의 full reaction 은 그 닫힌 쪽 꼴이다 (이 논문은 인용하지 않는다) |
| `wang2026_interface_stability_kinetics_sulfide_assb` | 황화물 7 종의 ΔV/V 지도 (색만). 분모 규약이 이 논문과 같은 부류 — 역학은 한 문장. 이 논문은 반대로 한 계의 역학을 끝까지 갔다 |
| `gilgonzalez2022_synergistic_cl_constricted_esw` | ε_RXN = SE 부피 기준 · 양의 변형이 '이롭다' 는 구속 열역학. 이 논문과 **분모도 해석도 다르다** |
| `bucci2017_chemomech_failure_assb_cycling_czm` · `bucci2018_mechanical_instability_interface_delamination` | refs [32, 33]. 전극 팽창 → 균열 · 박리 (파괴 기준 있음). 이 논문은 분해 부피를 넣었지만 파괴 기준이 없다 — 둘을 합친 연구는 아직 못 봤다 |
| `deng2016_elastic_superionic_electrolytes_dft` · `sakuda2013_sulfide_mechanical_property` | 황화물 탄성의 문헌 앵커 — Q7 의 입력 6 을 문헌값으로 채울 때의 자리 |
| `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` | 황화물 양극 쪽에서 화학 반응만으로 접촉 손실 · 균열 (실험) — 이 논문이 계산으로 못 간 계 |
| `wang2022_two_parameter_space_dendrite_constriction` · `fitzhugh2021_sei_design_constrained_ensemble` · `fitzhugh2019_ht_functionally_stable_interfaces_sulfide` | 같은 갭 묶음. 탄성률을 **상평형을 옮기는 항**으로 쓰는 계열 ↔ 이 논문은 탄성률을 **응력 환산**에 쓴다 |

---

## 11. 적용 인사이트 — 우리 일에 어떻게

1. **회계를 결과 전에 박는다.** 이 논문 하나 안에서도 '분해 부피 변화' 가 Li 를 내주는 상에 따라 −23 ~ −29 % 로 움직인다. 보고량 카드에 넣을 선택지가 이 논문으로 분명해졌다 — ① Li 저장소 (전극 상 / Li 금속 / 부피 0 인 외부 저장소) ② 분모 (반응물 전체 / SE 만) ③ 기체 · 분자성 산물 (0 / 제외 / 포함) ④ 어느 전위 · 어느 kink ⑤ 등방 가정.
2. **이 논문의 값을 크기 대조에 쓸 때는 정의를 붙인다.** '−27 %' 는 SE 의 변형률이 아니다. 우리 보고서 61 행의 크기 대조 ("LSPS 최대 56 % · LiPON 약 −27 %") 는 **분모가 다른 두 양**을 나란히 놓은 것이다.
3. **최대 응력 하나로 요약하지 않는다.** 26.8 GPa 는 fixed side 의 가장자리 값이고 free side 면 12.1 이다. 구속에 덜 민감한 눈금 (층의 이축 구속 응력 E·ε/(1 − ν) 같은 닫힌 식) 을 같이 내는 편이 도펀트 비교에 맞다 (의견).
4. **선형 탄성 응력은 상한 눈금이다.** 저자도 탄성 한계를 넘는다고 적는다. 황화물은 더 무르고 소성 · 크리프가 있으므로 '응력 값' 보다 '변형률 · 변형 에너지' 로 말하는 쪽이 안전하다 (의견).
5. **대조 잡 후보** — 우리 파이프라인이 식 9 를 계산하게 되면 먼저 이 논문의 `Table 1` 을 MP 부피로 재현해 본다. 양극 쪽 두 행은 재현될 것으로 보이고 음극 쪽은 안 될 수 있다 (§13-2). 재현 여부가 곧 도구 검증이다.
6. **파괴 기준은 따로 가져와야 한다.** 균열 · 접촉 손실을 주장하려면 이 논문의 틀로는 부족하다.
7. 저자가 든 완화책 가운데 '더 무른 전해질' 은 황화물 쪽에 유리한 방향의 정성 논거로만 쓸 수 있다 — 이 논문은 황화물을 풀지 않았다. ⚠ 우리 `bucci2017_chemomech_failure_assb_cycling_czm` digest 는 반대 방향의 결과 (무른 SE 가 오히려 더 취약할 수 있다) 를 적어 두었다. '무르면 안전' 을 그대로 가져오지 않는다.

---

## 12. 인용 가능 문장 (deck/paper 용 · 영문 초안)

- "Tian et al. combined decomposition reactions and crystal volumes from a DFT database with a finite-element model of a Si/LiPON/LiCoO2 thin-film cell and reported that interphase formation generated larger first principal stresses than the Li-concentration changes during a 1.2 C charge (*J. Electrochem. Soc.*, 167, 090541 (2020))."
- "In that model, the volume change was defined over all reactants of the full reaction, including the electrode phase, and the maximum stress in the electrolyte ranged from 9.9 to 26.8 GPa depending on the assumed interphase thickness and the side boundary condition."
- "The authors modeled LiPON only; sulfide electrolytes were not treated."
- ⚠ 쓸 때 반드시: LiPON 박막 셀 한정 · 계면층 두께는 가정 (10 · 50 nm) · 선형 탄성 · '최악' 반응 · 부피 변화는 전극 상 포함. ⛔ "SE decomposition strain of −27 %" 처럼 SE 고유값으로 쓰지 않는다.

---

## 13. 비판 — 주의 / 한계 (over-claim 방지)

> 표지: **[봄]** = 본문 · 그림 · 표에서 직접 확인 · **[우리 산술]** = 논문 숫자만으로 한 검산 · **[추정]** = 논문 밖 값이나 해석 (SI 가 없어 확인 못 한 것 포함).

1. **[우리 산술] 식 10 과 본문의 변형률이 맞지 않는다.** ((1 − 0.27)^(1/3) − 1) = **−9.96 %** · ((1 − 0.08)^(1/3) − 1) = **−2.74 %** 인데 본문은 −8.3 % · −2 % 다 (p.7). −8.3 % 는 −((1.27)^(1/3) − 1) 과 정확히 일치한다. −2 % 는 어느 쪽 (−2.74 · −2.60) 과도 맞지 않는다. 역산하면 −8.3 % ↔ ΔV −22.9 % · −2 % ↔ ΔV −5.9 % 다. 선형 탄성이라 응력은 변형률에 비례한다 — 8.3 % 와 9.96 % 는 1.2 배 차이이므로 어느 값이 들어갔는지에 따라 Si 쪽 응력이 그만큼 달라진다. SI 의 입력 파일로만 가를 수 있다.
2. **[추정] `Table 1` 의 음극 쪽 부피 변화가 결정 부피로는 재현되지 않는다.** 식 9 를 문헌 격자상수 (실험 결정 구조 · **기억값 — MP 값이 아니다**) 로 다시 계산하면:

   | 행 | 논문 | 재계산 [추정] | 논문 값이 나오려면 필요한 Si 원자당 부피 |
   |---|---|---|---|
   | Li₂₁Si₅ | −19 % | ≈ −10 % | 9.9 Å³ |
   | Li₁₃Si₄ | −24 % | ≈ −13 % | 9.6 Å³ |
   | Li₇Si₃ | −23 % | ≈ −10 % | 10.2 Å³ |
   | **Li₁₂Si₇** | **−27 %** | **≈ −9 %** (부피에 ± 3–4 % 산포를 줘도 −5 ~ −11 %) | 9.4 Å³ |
   | LiSi | −29 % | ≈ −2 % | 9.1 Å³ |

   - 다섯 행 모두 **Si 생성물의 부피를 원자당 9–10 Å³ 로 둘 때만** 논문 값이 나온다. 다이아몬드 Si 는 약 20 Å³ 이다 — 절반이다. 다섯 행이 같은 값으로 모인다는 점이 우연이 아님을 시사한다.
   - 같은 방식으로 양극 쪽 두 행은 재현된다: 2.64–3.04 V 행 ≈ −1 ~ −2 % (논문 −2 %) · > 3.63 V 행 ≈ −7 ~ −10 % (논문 −8 %). 식 9 를 읽은 방식 자체는 맞다는 뜻이다.
   - 기억값 대조 2 건: Li₂O 24.6 Å³ ↔ 저장소의 MP 구조 (`db/raw/cascade_dissolution_2026_10_14/mp/structures/Li2O__mp-1960.cif`) 25.2 Å³ (+2.3 %) · P₂O₅ 는 저장소의 MP 항목 셀 (`db/inputs/cei_product_gap_2026_10_27/work/P2O5_mp-aaaaadqi/01_vcrelax.in` 의 출발 셀) 에서 86.8 Å³/화학식을 그대로 썼다. 나머지 (Li–Si 합금 다섯 · Si · Li₃P · Li₃N · Li₇PN₄ · Li₂PO₂N · LiCoO₂ · Li₀.₅CoO₂ · PON · Li₄P₂O₇ · P₃N₅) 는 대조하지 못했다.
   - ⚠ **판정이 아니다.** 격자상수가 기억값이고 이 환경에 MP 키가 없어 확인하지 못했다. 원인 (Si 부피의 정규화 실수인지 · 다른 MP 항목인지 · 우리 읽기의 오류인지) 도 논문만으로는 알 수 없다. **MP 부피 10 여 개로 식 9 를 다시 계산하기 전에는 '논문이 틀렸다' 고 쓰지 않는다.**
   - 맞다면 영향: Si 쪽 선변형률이 약 −3 % 로 줄고 (논문 −8.3 %) 응력도 그만큼 준다. 그래도 충전 응력 (≤ 1.9 GPa) 보다는 클 것이라 정성 결론은 유지될 공산이 크다.
3. **[봄 + 추정] '분해 부피 변화' 는 SE 의 양이 아니고 분모에 따라 부호가 바뀐다.**
   - [봄] 식 9 의 분모는 반응물 전체다. `Table 1` 의 0.01–0.53 V 네 행은 SE 반응이 같은데 합금상에 따라 −23 ~ −29 % 다 (§4 Q2).
   - [추정] 같은 Li₁₂Si₇ 행을 세 가지로 세면 (격자상수 기억값):

     | 회계 | 음극 쪽 (Li₁₂Si₇ 행) | 양극 쪽 (> 3.63 V 행) |
     |---|---|---|
     | 논문 `Table 1` (반응물 전체 · 전극 상 포함 · N₂ 제외) | −27 % | −8 % |
     | 같은 정의 · 결정 부피로 재계산 | ≈ −9 % | ≈ −7 ~ −10 % |
     | SE 부피만으로 정규화 (산물 중 전극 상 제외 · Li 는 밖에서 오고 간다고 봄) | **≈ +110 % (팽창)** | ≈ −27 ~ −29 % |

   - SE 는 화학식당 Li 6 개를 받아들이며 산물 (Li₂O · Li₇PN₄ · Li₃P) 로 바뀌므로 **SE 자리는 부푼다.** 논문의 '수축' 은 Li 를 내준 합금의 수축이 그보다 커서 나온 순합이다. 서론이 인용한 LAGP/Li 의 '부피 팽창' (refs 21, 22) 과 부호가 다른 것도 이 때문이다 — Li 금속 저장소에서는 저장소의 부피를 세지 않으면 팽창으로 읽힌다.
   - 모델은 이 **순 수축**을 LiPON 안쪽의 얇은 층 하나에 몰아 준다. 실제로는 SE 쪽 반응층은 팽창 (구속되면 압축), 전극 쪽은 수축 (인장) 일 것이다 — 층에 귀속하는 방식이 응력의 부호를 정한다.
4. **[봄 + 우리 산술] 계면층을 t = 0 에 두는 가정과 고른 반응이 양극 쪽에서 맞지 않는다.** > 3.63 V 반응의 산화제는 Li₀.₅CoO₂ 다. 그런데 초기 양극은 y ≈ 0.98 이고 부록 식 A·2 로는 ≈ 2.3 V 다. 표의 첫 산화 단 (2.64 V) 에도 못 미친다. 음극 쪽은 초기 조성 (x ≈ 1.69 ≈ Li₁₂Si₇ · ≈ 0.33 V) 과 고른 행이 맞는다. 저자는 '최악' 이라고 밝혔지만, 양극 쪽 −8 % 층은 **충전 끝의 화학을 충전 시작에 놓은 것**이다.
5. **[봄] 계면층의 탄성 상수와 소속 도메인이 적혀 있지 않다.** `Table 3` 에는 Si · LiCoO₂ · LiPON 세 가지뿐이다. 계면층은 *"in the LiPON electrolytes"* 에 있다고만 한다 (p.3). 산물 혼합물 (Li₂O · Li₃P · Li₇PN₄ + Si) 의 탄성은 고려되지 않았다. [추정] `Table 2` 의 10 nm 값에서 Si ÷ LiPON = 1.27 로 E_Si ÷ E_LiPON = 1.25 와 거의 같다 — 두 도메인의 최댓값이 '같은 변형률 × 각자의 탄성률' 꼴이라는 뜻인데, 층이 어디에 어떻게 걸쳐 있어야 그렇게 되는지는 본문으로 알 수 없다.
6. **[봄 + 우리 산술] 헤드라인 숫자는 가장자리 집중 값이다.**
   - [우리 산술] 변형률 8.3–10 % 를 받은 층의 이축 구속 응력 E·ε/(1 − ν) 는 LiPON 에서 8.5–10.2 GPa 다. 10 nm 의 9.9 GPa 가 이 크기다 — **10 nm 값은 사실상 '변형된 층 자신의 부정합 응력'** 이고 벌크 전해질의 응력이 아니다 (본문도 10 nm 에서는 층 밖 응력이 미미하다고 적는다).
   - [우리 산술] 변형이 전부 막힌 균일한 층의 값 E·ε/(1 − 2ν) 는 12.8–15.3 GPa 다. **26.8 GPa 는 그 1.7–2.1 배**이므로 균일한 층의 응력이 아니라 기하 집중이다.
   - [봄] `Fig. 5` 에서 가장 짙은 점은 계면층 선이 측면 경계와 만나는 끝과 오목 모서리다. 본문도 최대 응력이 '다리 한가운데 = 모델의 옆 끝' 에서 난다고 적는다.
   - [추정] 변형률이 다른 층이 경계와 만나는 점과 오목 모서리는 선형 탄성에서 응력 특이점이 되기 쉬운 자리다. 메시 수렴 (0.5 %) 주장은 SI `Fig. S1` 에 있어 확인하지 못했다.
7. **[봄] 선형 탄성으로 10–27 GPa.** 저자가 탄성 한계 초과를 인정한다. 3 GPa 가 이미 탄성 변형률 3–4 % 다. 이 수는 '이만큼의 응력이 걸린다' 가 아니라 '선형 탄성이 깨진다' 로 읽어야 한다. 소성 · 균열 · 박리 · 공극 생성은 모델에 없다.
8. **[봄] 구속이 상한 쪽이다.** 집전체와 닿는 모든 바깥 경계가 법선 변위 0 이고 계면은 완전 접합이다. 스택이 순응하거나 계면이 미끄러지면 응력은 준다.
9. **[봄] 충전 쪽 비교 대상이 작게 잡혔다.** 1.2 C 하나 · 480 s · Si 표면층만 x 1.68 → 2. 저자도 용량이 낮다고 적는다. 완전 충전이나 Si 의 전 범위 (263 %) 를 쓴 비교가 아니다. 방전 · 반복 사이클도 없다.
10. **[봄] `Fig. 2` 의 '만족스러운 일치' 는 종지 용량의 일치다.** 응력 평가에 쓴 28 μA/cm² 곡선은 초반에 ≈ 0.4 V 낮다 (figure-read). 분극이 작게 모사됐다는 뜻이고, 농도 구배 — 곧 충전 응력 — 에도 영향을 줄 수 있다.
11. **[봄] 초록의 'predicted by DFT calculations' 는 MP 자료 조회다.** 판 · 범함수 · +U · 다형 선택 규칙이 없다. MP 는 판마다 항목과 hull 이 바뀐다 ([Zhu15] 와 맨 위 환원 단이 다른 것이 그 흔적으로 보인다).
12. **[봄] LiPON = 결정 Li₂PO₂N.** 실물은 비정질이고 조성 범위가 있다. 부피는 결정에서, 탄성 · 밀도는 실물 박막에서 왔다.
13. **[봄] 기체 제외 규칙이 양극 쪽 수축을 만든다.** N₂ 를 0 으로 두면 고체 부피는 당연히 준다. 기체가 빠져나가지 못하면 (묻힌 계면) 반대로 압력이 된다 — 본문도 실험의 기포를 언급한다.
14. **[봄] `Table 1` 은 사다리 전체가 아니다.** 3.04–3.63 V 구간이 비어 있고 (§6.4) 0.01–0.53 V 창 안의 세 행은 전압 칸이 빈칸이다.
15. **[봄] 본문 ↔ 그림 · 표의 작은 불일치들.**
    - 충전 응력이 측면 조건에 무관하게 *"very similar"* (p.9) ↔ `Fig. 6` 에서 LiPON 은 1.4 ↔ 1.9 GPa.
    - 면 방향 확산이 10³ 배 빠르다 (p.3) ↔ `Table 3` 은 반대.
    - `Fig. 3` 의 LiPON · Si 색 막대 지수가 뒤바뀜.
    - `Fig. 2` 의 '10 s' 원은 첫 실험점 (≈ 0.35 μAh/cm² — 28 μA/cm² 에서 약 45 s 분량 [우리 산술]) 에 그려져 있다.
    - 오기: *"Li2CO3"* (LiCoO₂) · *"28 μ A m−2"* (μA cm⁻²) · *"interfconce"* · *"summed to occur"* · 식 7 의 두 적분 면 이름이 같다.
    - 성막을 스퍼터 (p.2) 라고도 CVD (p.3) 라고도 한다. 공극 SEM 의 인용이 ref [36] (1997 년 LiPON 논문) 이다.
16. **[추정] 인용 역할 하나.** *"the impedance becomes higher as more cracks/damages are generated, as shown in recent experiments by Lee et al. [2]"* (p.9) — ref [2] 는 Si 나노기둥의 리튬화 파괴 논문 (PNAS 2012) 이다. 전고체 셀의 임피던스 근거로 맞는지는 그 논문을 봐야 한다 (안 봄).
17. **[봄] 일반성 주장과 실제 범위.** 서론 · 결론은 '다양한 전극/SE 조합 · 구조에 쓸 수 있다' 고 하지만 푼 것은 한 계 · 한 기하 · 한 충전율이다.

**그래도 이 논문의 강점**

- 분해 부피를 **응력으로 끝까지 환산한** 드문 실례다. 절차가 식 9 → 식 10 → 선형 탄성으로 투명하다.
- 실제 셀 (ref [28]) 의 기하 · 충전 곡선에 묶여 있다.
- 공극의 효과를 경계조건 두 극한으로 **묶어서** 보였다 (26.8 ↔ 12.1 GPa) — 모르는 것을 범위로 내는 방식.
- '최악' 선택 · 구조 민감성 · 탄성 한계 초과를 저자가 스스로 적었다.
- 반응식 8 줄을 표로 줬다 — 그래서 §13-2 같은 검산이 가능하다.

---

## 14. 기법 용어 미니사전

| 용어 | 뜻 (이 논문에서) |
|---|---|
| 2.5D 전지 · egg carton | 한쪽 전극은 기둥 모양으로 솟고 그 위를 전해질 · 반대 전극이 막으로 덮는 구조. 2D 박막과 3D 교차형의 중간 |
| interphase (계면상 · 계면층) | SE 가 전극과 닿아 분해해 생긴 새 상의 층. 액체 전지의 SEI 에 해당 |
| chemical strain (화학 변형률 · 고유변형률) | 조성이나 상이 바뀌어 응력 없이 생기려는 변형. 구속되면 응력이 된다 |
| diffusion-induced stress | 전극 안 Li 농도가 고르지 않아 생기는 응력 |
| 제1주응력 (first principal stress) | 한 점의 세 주응력 중 가장 큰 (가장 인장 쪽) 값. 취성 재료의 균열 지표로 쓴다 |
| grand-potential 상도 | Li 화학 퍼텐셜 (= 전위) 을 고정한 열린계에서 가장 안정한 상 조합을 찾는 방법 |
| full reaction | Li 를 주고받는 전극 상까지 넣어 원소 균형을 맞춘 닫힌 반응식 |
| Newman 모델 | 전극 확산 + 전해질 수송 + 계면 반응을 엮은 다공성/박막 전지의 표준 연속체 모델 |
| Nernst–Planck 식 | 농도 구배 (확산) 와 전위 구배 (전기 이동) 를 함께 넣은 이온 수송식 |
| Butler–Volmer 식 | 과전압과 계면 전류밀도의 관계식 |
| 롤러 경계 | 면에 수직인 변위만 막고 면을 따라 미끄러지는 것은 허용하는 경계조건 |
| fixed side / free side | 이웃 단위 사이 측면을 막은 경우 (공극 없음) / 풀어 둔 경우 (공극 있음) — 구속의 두 극한 |
| 선형 등방 탄성 | 응력이 변형률에 비례하고 방향에 무관하다는 가정. 상수는 E (탄성률) 와 ν (푸아송비) 둘 |

---

## 15. SI 에만 있는 것 (전부 **미입수** — 본문이 가리킨 목록)

- `Fig. S1` — 메시 세분화에 따른 최대 제1주응력의 수렴 (p.3).
- COMSOL 입력 — *"The input for the simulations can be found in the supporting materials."* (p.3)

우리 판정에 걸리는 순서: COMSOL 입력 (계면층에 넣은 변형률이 −8.3 % 인지 −9.96 % 인지 · 계면층의 탄성 상수와 소속 도메인 · 'fixed' 의 정의) → `Fig. S1` (가장자리 최댓값이 정말 수렴하는지).

---

## 16. 참고문헌 가운데 우리에게 걸리는 것

| ref | 서지 | 이 논문에서의 역할 | litdb |
|---|---|---|---|
| 3 | Qi, Hector, James, Kim, *J. Electrochem. Soc.* 161, F3010 (2014) | Si 263 % · LiCoO₂ +2 % · Si 탄성 | 카드 없음 |
| 4 | Koerver et al., *Energy Environ. Sci.* 11, 2142 (2018) | 부피–농도의 비선형 관계 | 카드 없음 |
| 20–22 | Tippens 2019 · Lewis 2019 · Chung & Kang 2017 | LAGP/Li 계면상 → 팽창 · 파괴 (동기) | 카드 없음 |
| 23 | Koerver et al., *Chem. Mater.* 29, 5574 (2017) | NMC/β-Li₃PS₄ 계면 분해 + 수축 → 접촉 손실 (동기) | 카드 없음 |
| 24 | Tian & Qi, *J. Electrochem. Soc.* 164, E3512 (2017) | 접촉 면적 손실 모사 (같은 그룹) | 카드 없음 |
| 28 | Talin et al., *ACS Appl. Mater. Interfaces* 8, 32385 (2016) | 셀 실물 · 충전 곡선 · 전기화학 매개변수 | 카드 없음 |
| 32, 33 | Bucci et al. 2017 · 2018 | 전극 팽창 → 균열 · 박리 모사 | `bucci2017_…` · `bucci2018_…` |
| 37 | Zhu, He, Mo, *ACS Appl. Mater. Interfaces* 7, 23685 (2015) | grand-potential 상도 방법 | `zhu2015_esw_grand_potential_origin` |
| 38 | Zhu, He, Mo, *J. Mater. Chem. A* 4, 3253 (2016) | 같은 방법 · 성막 중 분해 | `zhu2016_first_principles_interface_stability_assb` |
| 50 | Chakraborty et al., *npj Comput. Mater.* 4, 1 (2018) | 층상 양극 부피 추세 (SCAN) | 카드 없음 |
| 57 | Santhanagopalan et al., *J. Phys. Chem. Lett.* 5, 298 (2014) | 계면층 약 50 nm 의 실험 근거 | 카드 없음 |
| 71 | Herbert et al., *Thin Solid Films* 520, 413 (2011) | LiPON 박막 나노압입 → E · ν | 카드 없음 |

---

## 🗨️ Q&A 로그

(아직 없음)
