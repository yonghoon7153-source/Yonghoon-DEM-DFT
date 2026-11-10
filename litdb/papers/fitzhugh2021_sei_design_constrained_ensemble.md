<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 기준 = papers/agarwal2026_umlip_applicability_domain_ssb_interfaces.md
     2026-11-10 신규 작성 (논문 에이전트 · 사용자 읽기 목록 121 번 · cascade 트랙 문헌 갭 점검 다섯 편 중 표 '가' 줄).
     왜 읽었나: reports/황화물 분해 부피 도펀트 문헌 갭.md 가 '갭을 단정하기 전에 본문을 봐야 하는 다섯 편' 으로 꼽았고 한 번도 못 읽은 채였다
       → 갭 질문 7 개의 답은 §7 (항목마다 쪽 · 절 · 그림/표 번호).
     그림: 크롭 13 장 (그림 11 = 본문 5 + ESI 6 · 표 2). 그림 11 장을 전부 Read 로 실제로 봤다. 표 2 장은 관례대로 PDF 텍스트로 옮겼다 (쪽 렌더로 칸 배치만 확인).
     이 논문의 그림은 전부 내장 JPEG 래스터다 (벡터 좌표 없음). 'figure-read ≈' 값은 내장 이미지의 픽셀에서 읽었다 —
       tools/litdb/fitzhugh2021_digitize.py (마커 중심 · 막대 꼭대기 · 칸 색 → 색 막대) → litdb/figures/fitzhugh2021_sei_design_constrained_ensemble/digitized.csv (502 행).
       판독 검산 4 건 통과: (가) Fig. 5b 의 K_crit 0 % · 5 % 판독 13.33 · 7.60 = ESI 표의 13.31 · 7.60
                          (나) Fig. S1d LPS 막대 18.42 / 14.77 / 12.99 = 본문 18.5 / 14.8 / 13.0
                          (다) K_eff 곡선 8 묶음이 전부 G0·(1 − K_eff/K_crit) (최대 차 0.0009 eV/atom)
                          (라) Fig. 5c 봉우리 픽셀 높이 ÷ Fig. 5d H_R = 2.94–3.09 px/µA (여섯 곡선이 같은 전류 눈금)
     '우리 산술' 표지가 붙은 값 (ε_RXN·V⁰ 역산 · 기여 분해 · 순위 상관 · 전하합 · 잘린 분포 통계 · 보간 개시 전압) 은 논문 값이 아니다.
     우리 쪽 숫자는 옮기지 않았다 — 원장 경로로만 가리킨다 (구속 ESW 원장 · B₀ · cascade 축 카드 전부). -->

# Solid–electrolyte-interphase design in constrained ensemble for solid-state batteries — Fitzhugh, Chen, Wang, Ye & Li (Energy Environ. Sci. 2021)

> slug `fitzhugh2021_sei_design_constrained_ensemble` · DOI `10.1039/D1EE00754H` (본문 1 쪽 · PDF 메타데이터로 **확인** — 우리 기록의 '추정' 해소) · type `DFT 자료 기반 HT 열역학 스크린 (MP 상 자료 · grand potential · 구속 앙상블 K_crit) + ML (결정트리 앙상블 · SHAP) + 실험 (황화물 유리 합성 · CV)` · PDF `d1b54f05-121._Solid_electrolyte-interphase_design_…pdf` (inbox #121 · 10 pp = *EES* 14, 4574–4583 · refs 24 편) + ESI `7b208695-121._Sup_…pdf` (8 pp = `Fig. S1`–`S6` · 표 2 장 · refs 9 편) · digested `2026-11-10` · status ✅ · 태그 **[외부 · Xin Li 그룹 (Harvard) · K_crit 원전 · ⛔ argyrodite 계산 0]**
> elements: Li, P, S, I, O, F, Cl, Br, Si, Ge, B, Na
> methods: DFT, ESW

> **저자 (표지 그대로)**: **William Fitzhugh**‡, **Xi Chen**‡ (‡ 공동 1 저자), Yichao Wang, Luhan Ye, **Xin Li**\* — John A. Paulson School of Engineering and Applied Sciences, Harvard University. 교신 `lixin@seas.harvard.edu`.
> 접수 2021-03-12 · 수락 2021-06-23 · 게재 2021-07-20 · CC BY-NC 3.0.
> 자금: Harvard Climate Change Solutions Fund · Dean's Competitive Fund for Promising Scholarship · Harvard Data Science Initiative Competitive Research Fund · **Nissan USA** · **LG Energy Solution**. 계산 자원: Harvard Odyssey · XSEDE. 이해상충 없음 (신고).
> 코드 · 자료 공개: **적힌 곳이 없다** (8 만 점 HT 자료 · 학습된 모형 · 합성한 유리의 실제 조성 어느 것도).
> 🎤 **관련 발표**: 해당 없음 — `litdb/talks/` 전체와 인입 대기열 (`lee2026_skku_mlip_materials_design.md`) 을 'Fitzhugh · constrained ensemble · 4574' 로 찾았고 이 논문은 없다.
> 계보: Xin Li 그룹 구속 앙상블 연작의 **계면판**이다. 벌크 SE 판 = 이 논문 refs 11–13 (Fitzhugh *J. Mater. Chem. A* 7, 23604 (2019) · Wu *Nat. Commun.* 9, 4037 (2018) · Fitzhugh *Small* 15, 1901470 (2019) — litdb 미보유). 유사상 (pseudo-phase) HT 의 전편 = ref 9 → `fitzhugh2019_ht_functionally_stable_interfaces_sulfide` (목록 122). Li 금속 쪽 (E_hull, K\*) 판 = `wang2022_two_parameter_space_dendrite_constriction` (목록 120). Cl 함량 계열에 같은 틀을 쓴 후속 = `gilgonzalez2022_synergistic_cl_constricted_esw`. (120 · 122 의 slug 는 `litdb/pdf_map.tsv` 에 등록된 이름이고 digest 는 같은 날 따로 쓰였다.)
> 이 논문을 인용한 litdb 편: `park2026_ml_framework_stable_interfaces_assb` (그 논문 ref 25 · digest 의 '읽을 것' 4 번) · `wang2025_ai_ecosystems_electrolyte_interface_ssb` (그 리뷰 ref 136 · digest §10f 가 옮긴 리뷰 `Fig. 8` 의 세 국면 · 결정트리 도식이 이 논문 `Fig. 1d` · `Fig. 2` 내용이다).

---

## 0. 이 digest 를 읽는 법

이 논문은 **'기계적 구속을 스크린 축으로 쓴 고처리량 계면 연구' 의 원전**이다. 셋을 갈라서 읽는다.

1. **논문이 실제로 계산한 것** (§4–§5) — Materials Project 의 전자 절연체 2 만여 종을 황화물 SE 4 종 (Li₁₀GeP₂S₁₂ · Li₁₀SiP₂S₁₂ · Li₇P₃S₁₁ · Na₇P₃S₁₁) 과 짝지은 계면 8 만여 개의 **임계 유효 탄성률 K_crit** (4 V), 그 위의 결정트리 앙상블, 알려진 황화물 유리 10 종의 조성 최적화.
   ⛔ **Li₆PS₅Cl 계산은 없다** (시험 셀의 음극 쪽 보호층으로만 나온다). 도핑 아지로다이트 0. 분해 산물의 목록 · 물성 0. 반응 변형률 ε_RXN 의 수치표 0.
2. **논문이 재지 않고 말한 것** (§14) — '프리피크 = 유리/LGPS 계면 분해', 'K_eff ≈ 4.6–4.9 GPa', '첫 충전 뒤 K_eff 가 K_crit 을 넘어섰다' 는 전부 모형에 기대 추론한 것이고 따로 잰 것이 아니다.
3. **우리에게 넘어오는 것** (§7 · §11–§12) — 값이 아니라 **정의 (K_crit) 와 '무엇이 비어 있나' 의 판정**이다.

⛔ 인용 금지 (한 줄 요약): 이 논문의 K_crit · 원소 상관 · child 조성을 **아지로다이트 도펀트의 값**으로 옮기지 않는다 — 계가 유리 코팅 / LGPS · LSPS · Li₇P₃S₁₁ · Na₇P₃S₁₁ 이고, 설계 수치는 전부 대리모형 예측값이다 (자세한 목록 §13).

**본 그림 / 안 본 그림** — 크롭 13 장 중 그림 11 장 (`Fig. 1`–`5` · `Fig. S1`–`S6`) 을 전부 실제로 봤다. `Table S1` · `Table S2` 는 PDF 텍스트로 옮겼다 (ESI 는 캡션에 'Table 1 · 2' 로 적고 본문은 S1 · S2 로 부른다 — 여기서는 본문 이름을 쓴다). 안 본 그림은 없다.

---

## 1. 한 줄 요약

고체 전지에서는 분해 산물이 원래 물질보다 부피가 크면 주변이 되눌러서 분해가 손해가 된다 (구속 앙상블). 이 논문은 그 생각을 **계면**에 처음 적용해 *'계면상 (SEI) 이 양극 전압에서 더 분해하지 않으려면 국소 유효 탄성률 K_eff 가 얼마를 넘어야 하나'* 를 **임계 유효 탄성률 K_crit** 로 정의하고 (식 3), MP 전자 절연체 2 만여 종 × 황화물 SE 4 종의 유사상 계면 8 만여 개에서 4 V 값을 계산했다. K_crit 는 평균 14–19 GPa · 표준편차 10–13 GPa 로 넓게 퍼지고 조성에 대해 비선형 · 진동한다. 조성 → K_crit 결정트리 앙상블 (RMSE 2.59 GPa) 과 SHAP 로 알려진 황화물 유리 10 종의 조성을 조금씩 바꿔 (O · F · Cl 첨가) K_crit 를 평균 16 → 11 → 8 → 2 GPa 로 낮추는 'child' 조성을 내고, 첫 유리 (Li₂S–P₂S₅–LiI 계) 의 변형 5 종을 합성해 CV 로 본다 — 3 V 근처 프리피크 전류가 수정 수준과 함께 단조 감소한다. **스크린 대상은 SE 가 아니라 코팅 (유리) 조성**이고, 아지로다이트 · 도펀트 계열 · 산물 물성 점수 · ε_RXN 수치표는 없다. 우리 판독으로는 (i) K_crit 하락의 대부분이 부피가 아니라 **분해 에너지 감소**에서 왔고 (ii) 제안된 child 조성 다수는 논문이 적은 전구체로 **만들 수 없는 조성** (전하합 ≠ 0 · Cl 원료 없음) 이며 (iii) 설계값은 직접 계산으로 한 번도 되짚지 않은 대리모형 값이다.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 계 | 연구유형 |
|---|---|---|---|---|
| W. Fitzhugh‡, X. Chen‡, Y. Wang, L. Ye, X. Li\* (Harvard SEAS) | *Energy Environ. Sci.* **14**, 4574–4583 (2021) · 게재 2021-07-20 | 10.1039/D1EE00754H | 계산: MP 전자 절연체 > 20,000 × {Li₁₀GeP₂S₁₂ · Li₁₀SiP₂S₁₂ · Li₇P₃S₁₁ · Na₇P₃S₁₁} / 설계: 황화물 유리 10 종 / 실험: Li₀.₃₆₄P₀.₁₁₀S₀.₃₈₈I₀.₁₃₈ 유리 + 변형 5 종 | HT 열역학 (MP 자료) + ML + 합성 · CV |

- 랩 표준 표기: *Energy Environ. Sci.*, 14, 4574 (2021).
- 출처 표지: **[외부]** (Harvard Xin Li 그룹 · 우리 그룹 아님).
- ⚠ **약어가 겹친다**: 서론 (p. 4575) 의 'LPS' 는 Li₃PS₄ (LGPS 의 분해 산물) 이고, p. 4577 부터의 'LPS' 는 **Li₇P₃S₁₁** (스크린한 SE) 이다. `Fig. 3a` · `Fig. S1d` · `Fig. S2` 의 LPS 는 뒤쪽이다. NPS = Na₇P₃S₁₁.
- ⚠ **'SEI' 의 뜻이 넓다**: 음극 계면이 아니라 **SE 와 코팅 사이에 생기는 계면상 일반**을 가리키고, 평가는 양극 전압 (2–4 V) 에서 한다.

---

## 3. 이 논문이 던지는 질문 (Introduction 의 구조 · p. 4574–4575)

1. SSB 의 큰 장벽은 셀 안 여러 계면의 (전기)화학적 불안정이다.
2. 액체 셀은 압력 p · 온도 T · 전압 φ 가 상태 변수다 (조작자가 정하고 상이 평형에 간다). 저자들은 이것을 pTφ 앙상블 = **'비구속' (unconstrained)** 이라 부른다.
3. 고체에서는 **압력이 상태 변수가 아니다.** 분해가 일어난 자리에만 국소 압력이 생기고, 고체는 그 압력 구배를 유지한다 (액체는 흘러서 푼다). 사고 실험: 전해질의 작은 부피 r₀ 만 분해했다 (x_D = 1 at r₀ · 그 밖은 0) → 반응 변형률과 압력이 r₀ 근방에만 있다.
4. 두 관찰: (i) 많은 SE 가 **부피가 더 큰** 산물로 분해한다 (ii) 그 팽창이 열역학을 바꾼다. 예 — LGPS 가 화학적으로 분해하면 Li₄GeS₄ + Li₃PS₄ 가 되고 부피가 **2 %** 크다 (몰분율 1, 0, 0 → 0, 1/3, 2/3). Li 대비 전기화학 분해는 완전 산화 (고전압) · 완전 환원 (저전압) 극한에서 **30 % 넘게** 는다 (refs 11–13).
5. 이 부피 증가 = **반응 변형률 ε_RXN** (reaction strain · reaction dilation). 가해진 응력 때문에 생긴 변형이 아니라 분해 자체가 만드는 stress-free strain 이다. 구속 아래에서는 큰 상을 작은 자리에 끼워 넣어야 하므로 국소 압력이 생긴다: **p = K_eff · ε_RXN** (p = 고체 부피 단위의 평균 압축 응력 · K_eff = 국소 유효 탄성률).
6. p 의 함수꼴이 창을 정한다 — 등압이면 종래 grand-canonical 로 돌아가 LGPS 창이 1.7–2.1 V (refs 14, 15), 압력이 국소 변형에 비례하면 (준)안정 창이 약 1–4 V (refs 1, 12, 13), 동역학 안정은 0 V 에서 10 V 까지 (refs 1, 4).
7. 이 논문: 구속 앙상블을 **처음으로 계면 안정성 계산에** 쓴다 → K_eff 가 계면 물질이 정하는 임계값 K_crit 위면 계면이 사이클 내내 안정, 아래면 자란다 → HT + ML 로 K_crit 를 낮추는 SEI 를 설계한다.

> Broader context (p. 4574) 의 서사: *"Any local mechanical constriction level below this critical value will allow decompositions to happen. The decomposition, however, will fill local voids and cracks, and eventually increase the local mechanical constriction beyond the critical value to suppress further decompositions through metastability."* — **분해가 공극 · 균열을 메워 스스로 멈춘다**는 화학–기계 되먹임이다. 정량 모형 (공극 부피 · 접촉) 은 없다.

---

## 4. 틀 — 구속 앙상블과 K_crit (★ 식 · 매개변수 · Li 저장소 · 부피)

### 4.1 유사상 (pseudo-phase) — 식 (1) · p. 4576

두 상 α · β 가 만나 분해한다: **(1 − x_β) α + x_β β → Σᵢ dᵢ Dᵢ** (식 1 · dᵢ = 분율 · Dᵢ = 산물 상).
G_hull (분해 에너지 크기) 을 최대로 하는 x_β 를 **x_m** 이라 하고, **(1 − x_m) α + x_m β** 를 '유사상' 이라 부른다 (ref 16 = 우리 `nolan2018_computation_accelerated_design_review`). 저자 표현으로 *"the most kinetically driven decomposition by definition"*. 계면을 조성 (1 − x_m) α + x_m β · 에너지 (1 − x_m) G_α + x_m G_β 인 **한 상**으로 다룬다.

### 4.2 구속 아래의 분해 — 식 (2) · (3) · p. 4576–4577

- 식 (2): **(1 − x_β) α|_{p=0} + x_β β|_{p=0} → Σᵢ dᵢ Dᵢ|_{p = K_eff·ε_RXN}** — 반응물은 압력 0, 산물은 국소 변형이 만든 압력 아래에 있다.
- 그 차이가 반응 에너지를 **K_eff · ε_RXN · V⁰** 만큼 바꾼다 (*"where V⁰ is the reference volume"* — 정의는 이 한 마디뿐).
- 식 (3): **ΔG⁰_RXN + K_crit · ε_RXN · V⁰ = 0** ⇒ K_crit = −ΔG⁰_RXN / (ε_RXN · V⁰). *"the interface reaction is expected to be thermodynamically favorable if and only if K_eff < K_crit."*
- `Fig. 1b` (K_crit > K_eff · 약한 구속): 산물 각 상의 자유에너지가 Gᵢ → Gᵢ + p(D)·Vᵢ 로 조금 올라가지만 어느 상이 유리한지는 안 바뀐다. `Fig. 1c` (K_crit < K_eff · 강한 구속): 유사상 (노란 별) 이 산물 hull 아래로 내려간다 = 분해하지 않는다.

### 4.3 계면의 세 국면 — `Fig. 1d` 표 전사 (그림 실독)

| | 조립 · 화학 이완 = **초기 SEI 형성** (K_eff ≈ 0) | 사이클 = **SEI 성장** (K_eff < K_crit) | 사이클 = **SEI 유지** (K_eff > K_crit) |
|---|---|---|---|
| 반응 | 초기 계면 → 초기 SEI | 초기 SEI + Li → 2차 SEI | 초기 SEI → 초기 SEI |
| 조성 | (1 − x_m) SSE + x_m A → Σ dᵢ Dᵢ | Σ dᵢ Dᵢ + N_Li → Σ fᵢ Fᵢ | Σ dᵢ Dᵢ → Σ dᵢ Dᵢ |
| 부피 | (1 − x_m) V_SSE + x_m V_A → Σ dᵢ V_Dᵢ | Σ dᵢ V_Dᵢ → Σ fᵢ V_Fᵢ | 변화 없음 |
| 압력 | 0 → 0 | 0 → K_eff · ε_RXN ≫ 0 | 0 → 0 |

- 조립 때는 구속이 없어 (K_eff ≈ 0) 계면 반응이 **닫힌계 (canonical)** 로 간다 — *"the system is not yet open to lithium, hence it is not grand canonical"* (p. 4577). 그래서 초기 SEI 는 피할 수 없다.
- 조립 뒤에는 Li 에 열린다. 구속이 약하면 전압이 초기 SEI 의 안정창을 드나들 때마다 2차 SEI 로 계속 분해 (성장), 충분히 강하면 그대로 (유지).
- **목표 문장** (p. 4577): *"the goal of solid-state battery design should be to focus on designing the initial SEI's such that they don't grow during cycling."* — K_crit 가 낮을수록 약한 구속에서도 멈추고, *"the electrochemical evolution will more easily increase the local K_eff beyond K_crit"* (p. 4578).

### 4.4 Li 저장소 · 부피 정규화 — 논문이 적은 것과 적지 않은 것

| 항목 | 논문이 적은 것 | 위치 | 논문이 적지 않은 것 |
|---|---|---|---|
| Li 저장소 (조립) | 닫힌계 (canonical) · K_eff ≈ 0 | p. 4577 왼쪽 | — |
| Li 저장소 (사이클) | 열린계 — 초기 SEI 의 grand potential 상도에서 분해 에너지와 반응 변형률을 얻는다 | `Fig. 1d` · Methods p. 4582 | 양극 전압에서는 Li 가 빠져나가는데 그림은 '+ N_Li' 로만 적는다 |
| 부피 수지 | `Fig. 1d` 부피 행은 고체 상만 센다 (Σ dᵢV_Dᵢ → Σ fᵢV_Fᵢ) — N_Li 는 조성 행에만 있다 | `Fig. 1d` (실독) | **ε_RXN 의 식 자체** · Li 를 부피에 세는지 밝힌 문장 · 기체/휘발 산물 처리 — 전부 refs 11–13 에 맡겼다 |
| 정규화 | 에너지 eV/atom (`Fig. 5a` 축) · 추가 항 K_eff·ε_RXN·V⁰ | p. 4576 | V⁰ 가 무엇의 부피인지 · 'atom' 에 SE 쪽 원자가 드는지 |
| ε_RXN ≤ 0 인 쌍 | — | — | 수축 분해면 어떤 구속도 못 막아 K_crit 가 정의되지 않는다. 그런 쌍을 뺐는지 · 0 으로 뒀는지 없다. 분포 그림은 0–80 GPa 만 보인다 |
| 압력 아래 산물 재선택 | 식 (2) 는 산물이 가압 상태라고만 한다 | p. 4576 | K_eff 를 올릴 때 산물 조합을 다시 고르는지 — 판독으로는 **다시 고르지 않는다** (§6.1) |

> 정리: 이 논문은 '구속 아래 계면' 의 **판정식**은 주지만 **부피 회계** (Li 저장소 · 기체 · 정규화) 는 선언하지 않는다. 우리 문헌 갭 보고서가 B 의 둘째 빈칸으로 꼽은 바로 그 회계다 — 이 편으로는 채워지지 않고 원전 (refs 11–13) 을 봐야 한다.

---

## 5. 핵심 수치 총정리 ★

> 표기: **굵은 값** = 본문 · 표에 숫자로 적힌 값. `figure-read ≈` = 그림 픽셀 판독 (`tools/litdb/fitzhugh2021_digitize.py`). 전부 문헌 소환값이다 — 우리 `db/properties/` 값 옆에 놓지 않는다.

### 5.1 HT 스크린의 규모와 분포 (`Fig. 3a` · `Fig. S1` · p. 4577–4578)

- 규모 (p. 4577): *"Over 80 000 SEI's were simulated using pseudo-binary calculation of over 20 000 electronic insulators from the Materials Project with four well known ceramic-sulfide solid electrolytes."* 자료 한 점 = (초기 SEI 조성, 그 SEI 를 양극 전압 [*"e.g., from 2 V to 4 V"*] 에서 안정시키는 K_crit).
- '전자 절연체' 를 고른 기준 (띠틈 문턱) 은 이 논문에 없다.

| SE | N (0–80 GPa) `figure-read ≈` | 평균 / 중앙 / 표준편차 (GPa) | 최빈 칸 `figure-read ≈` |
|---|---|---|---|
| Li₇P₃S₁₁ ('LPS') | 21,300 | **18.5 / 14.8 / 13.0** (본문 p. 4578) · `Fig. S1d` 막대 판독 18.4 / 14.8 / 13.0 | 14–16 GPa · 2,780 |
| Li₁₀GeP₂S₁₂ | 20,000 | `figure-read ≈` 19.0 / 15.6 / 12.0 (`Fig. S1d`) | 14–16 GPa · **4,170 (양옆 칸의 두 배)** |
| Li₁₀SiP₂S₁₂ | 19,900 | `figure-read ≈` 19.4 / 16.2 / 12.2 (`Fig. S1d`) | 14–16 GPa · 2,750 |
| Na₇P₃S₁₁ ('NPS') | 21,700 | `figure-read ≈` 13.7 / 10.9 / 9.7 (`Fig. S1d`) | 8–10 GPa · 4,070 |

- 네 분포의 합 ≈ 83,000 = 본문의 "over 80 000".
- 저자 해석: 표준편차가 커서 조성으로 K_crit 를 크게 움직일 여지가 있다 (*"ample opportunity for engineering ideal interfaces with low K_crit values"*).
- 그림에서만 보이는 것 ①: 히스토그램 축이 0–80 GPa 에서 끝난다. 히스토그램에서 다시 낸 평균 · 표준편차 (LGPS 18.4 · 11.0 / LSPS 18.9 · 11.4 / NPS 13.1 · 8.2) 가 `Fig. S1d` 막대보다 낮다 → 80 GPa 위 꼬리가 잘려 있다 (우리 추정).
- 그림에서만 보이는 것 ②: 최빈 칸이 뾰족하다. `Fig. S2` 에서 순수 Li₇P₃S₁₁ (x → 0) 의 K_crit 가 `figure-read ≈` 14.7 GPa 인데 이것이 본문 중앙값 14.8 과 같다. LGPS 는 14–16 칸 하나에 전체의 21 % 가 몰려 있다 → **반응하지 않는 쌍이 'SE 자기 값' 으로 들어가 분포의 봉우리를 만들었을 가능성** (우리 추론 · 논문은 x_m 이 0 이나 1 로 가는 쌍의 처리를 적지 않았다).

### 5.2 원소 조성 ↔ K_crit 상관 (`Fig. 3b` · p. 4578)

- 캡션: *"The correlation of elemental composition and K_crit for all pseudo-phases considered (LPS, LGPS, LSPS, NPS). Red elements are those that lower K_crit [ideal], whereas those elements that are blue raise K_crit."* 색 막대 −1.00 (진빨강) … +1.00 (진파랑).
- 저자 해석 (p. 4578): O · F · Cl 이 가장 이롭다 — *"This is likely attributed to these anions having high voltage redox potential. In other words, SEIs with high levels of oxygen, fluorine, and chlorine are less prone to delithiation in the considered voltage ranges."* V · Mo · W 도 4 V 아래에서 반응하지 않아 이롭다고 한다.
  → **저자 스스로 낮은 K_crit 의 원인을 부피가 아니라 산화환원 안정성 (탈리튬화가 덜 됨) 에 둔다.** §6.3 의 우리 분해와 같은 방향이다.
- 논문은 **값을 숫자로 주지 않는다** (색뿐). 어떤 상관계수인지 · 원소가 없는 화합물을 0 으로 넣었는지도 없다. 아래는 칸 색을 같은 그림의 색 막대에 대 읽은 값이다 (`figure-read ≈` · 0 근처는 ±0.03 · 76 원소 · 회색 27 칸은 자료 없음).

| 묶음 | `figure-read ≈` 상관 값 (음 = K_crit 낮춤 · 양 = 높임) |
|---|---|
| 음이온 | **F −0.58** · O −0.13 · Cl −0.13 · Br −0.02 · S +0.01 · I +0.41 · Se +0.49 · Te +0.51 |
| 알칼리 · 알칼리토 · H | Li 0.00 · Cs +0.29 · Be +0.33 · Ca +0.35 · Na +0.41 · K +0.42 · Rb +0.42 · Ba +0.45 · Sr +0.46 · Mg +0.48 · H +0.48 |
| p-블록 양이온 | P −0.02 · Ge +0.05 · N +0.05 · Pb +0.05 · Si +0.11 · Al +0.17 · C +0.17 · Tl +0.20 · Ga +0.24 · Bi +0.31 · B +0.34 · Sn +0.37 · In +0.45 · As +0.52 · Sb +0.56 |
| 3d | V −0.11 · Co +0.01 · Ni +0.07 · Cr +0.09 · Fe +0.09 · Ti +0.11 · Mn +0.18 · Sc +0.19 · Zn +0.27 · Cu +0.40 |
| 4d · 5d | W −0.15 · Ta −0.07 · Mo −0.01 · Hf +0.04 · Hg +0.07 · Re +0.09 · Nb +0.13 · Ag +0.16 · Pd +0.17 · Y +0.20 · Au +0.22 · Zr +0.24 · Ru +0.24 · Pt +0.29 · Cd +0.31 · Rh +0.45 |
| 란타나이드 · 악티나이드 | U +0.01 · Er +0.17 · Tm +0.20 · Ho +0.23 · Lu +0.28 · Eu +0.30 · Tb +0.30 · Yb +0.31 · Th +0.31 · Ce +0.33 · Gd +0.35 · Dy +0.35 · **Nd +0.41** · Sm +0.44 · Pr +0.51 · La +0.60 |

- 뚜렷이 음인 원소는 **F 하나**다. O · Cl · W · V 는 −0.11 … −0.15 로 약하고, 본문이 이롭다고 한 Mo (−0.01) 와 Br (−0.02) 는 사실상 0 이다 — 본문 서술이 그림보다 세다.
- 우리 갭 보고서의 도펀트 목록으로 읽으면: O −0.13 · Cl −0.13 · Br −0.02 · Ge +0.05 · Si +0.11 · Al +0.17 · Zn +0.27 · Bi +0.31 · B +0.34 · Sn +0.37 · Cu +0.40 · I +0.41 · Nd +0.41 · Sb +0.56. ⛔ 이것은 **코팅 물질 2 만 종 전체에 걸친 상관의 부호**이지 한 호스트에 도펀트를 넣었을 때의 값이 아니다 (§7-3 · §13).

### 5.3 K_crit 는 조성에 대해 비선형 · 진동한다 (`Fig. S2` · p. 4578)

- (1 − x) Li₇P₃S₁₁ + x A 의 1 차원 단면 네 개 (A = LCO · LNO · LTO · LFPO — 약어 풀이는 논문에 없다). 4 V 로 읽힌다 (캡션에 전압 없음 · 본문 문맥).
- `figure-read ≈`: x → 0 에서 네 곡선이 14.7 GPa 로 겹친다 / LCO 최대 19.8 GPa (x 0.39) · x → 1 에서 약 4–5 / LNO 최대 12.7 (x 0.51) · 끝 약 4–5 / LTO 최대 14.8 (x 0.35) · **최소 0.2 (x 0.81)** · 끝 7.9 / LFPO 끝 약 2.
- 캡션: 조성 공간은 **117 자유도 (원소 수 − 1)** — 즉 특징은 118 원소의 분율이다.
- x → 1 (순수 양극재) 에도 유한한 K_crit 가 있다 = 열린계에서는 **양극 활물질의 정상적인 탈리튬화도 '분해' 로 센다**는 뜻이다 (그림에서 읽히는 귀결 · 논문 언급 없음).

### 5.4 ML 대리모형 (`Fig. 2` · `Fig. 4a` · `Fig. 4b` · `Fig. S3` · p. 4577–4578 · Methods p. 4582)

- 모형: 결정트리 앙상블. 본문 · `Fig. 2` · `Fig. S3` 캡션은 **50 개**, Methods 는 Extremely Randomized Trees (ref 24) 에 ***"N = 30 in our setting"*** — 본문 안에서 어긋난다.
- 입력 = 조성 (원소 분율) · 출력 = K_crit. 시험: *"a test set of 10 000 SEIs"* · **RMSE 2.59 GPa** · *"especially in the lower range of K_crit"*.
- `Fig. 4b` (실독): 축이 둘 다 0–25 GPa 이고 **25 GPa 를 넘는 점이 하나도 없다.** 대각선 위에 정확히 놓인 점들의 가는 선 + 그 둘레의 넓은 구름 (15 GPa 근처에서 ±5 GPa 넘게 퍼진다).
- `Fig. S3` (50 개 중 한 나무 · 노드에 인쇄된 값 전사):

| 깊이 | 분기 | mse | samples | value (GPa) |
|---|---|---|---|---|
| 0 | F ≤ 0.096 | 27.974 | 10000 | 14.416 |
| 1 (참) | O ≤ 0.606 | 23.084 | 8739 | 15.24 |
| 1 (거짓) | Li ≤ 0.001 | 24.619 | 1261 | 8.712 |
| 2 | O ≤ 0.351 | 20.715 | 7785 | 15.712 |
| 2 | Li ≤ 0.0 | 25.73 | 954 | 11.384 |
| 2 | Si ≤ 0.01 | 18.755 | 992 | 10.228 |
| 2 | F ≤ 0.44 | 6.478 | 269 | 3.118 |
| 3 | Cl ≤ 0.064 | 17.804 | 3884 | 16.617 |
| 3 | P ≤ 0.093 | 21.986 | 3901 | 14.811 |
| 3 | P ≤ 0.079 | 22.215 | 771 | 12.016 |
| 3 | O ≤ 0.617 | 31.772 | 183 | 8.722 |
| 3 | K ≤ 0.096 | 16.398 | 419 | 8.451 |
| 3 | F ≤ 0.535 | 16.479 | 573 | 11.528 |
| 3 | Na ≤ 0.012 | 5.018 | 124 | 4.146 |
| 3 | Al ≤ 0.05 | 6.052 | 145 | 2.24 |

  (표본 수 검산: 8739 + 1261 = 10000 · 7785 + 954 = 8739 · 992 + 269 = 1261 — 전부 맞는다.)
- 읽히는 것: F 가 0.096 을 넘으면 평균이 15.2 → 8.7 GPa 로 떨어지고, 그중 **Li 가 든 것 (269 표본) 은 3.1 GPa**, Li 가 없는 것 (992) 은 10.2 GPa 다. 가장 왼쪽 가지 (F · O · Cl 이 다 낮다) 가 16.6 GPa 로 가장 높다.

### 5.5 SHAP 로 조성을 고치는 경로 (`Fig. 4c` · p. 4579–4580 · LSPS 계면 · 4 V)

첫 parent 유리 Li₀.₃₆₄P₀.₁₁₀S₀.₃₈₈I₀.₁₃₈ 에서 출발한다. 막대 색: 빨강 = K_crit 를 올리는 쪽 · 파랑 = 내리는 쪽 (⚠ `Fig. 3b` 와 색 뜻이 반대다).

| 단계 | 예측 K_crit (GPa) | 그림에 적힌 조성 (실독) | 빨강 막대 (긴 순) |
|---|---|---|---|
| Parent | **16.07** | Li 0.3639 · I 0.1376 · P 0.1101 · Si 0 | O = 0 · F = 0 · Cl = 0 · Br = 0 |
| 중간 1 (+O) | 13.19 | O 0.04489 · Li 0.3476 · I 0.1314 · P 0.1051 | O 0.045 (여전히 가장 길다) · F = 0 · Cl = 0 · Br = 0 |
| 중간 2 (+F) | 12.66 | F 0.04352 · O 0.04294 · Li 0.3325 · I 0.1257 · P 0.1006 | O 0.043 · Cl = 0 · S 0.3548 |
| 중간 3 (+Cl) | 12.17 | Cl 0.02582 · F 0.0424 · O 0.04183 · Li 0.3239 · I 0.1225 | O 0.042 |
| (중간 4–20) | … | 미세 조정 | |
| Child A (5 %) | **12.07** | O 0.04027 · F 0.04247 · Cl 0.02586 · Li 0.3244 · I 0.1227 | O 0.040 |
| Child B (10 %) | **6.89** | F 0.09045 · O 0.014 · Sb 0.02415 · Li 0.3064 · I 0.1159 · P 0.0927 · S 0.3244 | S 0.3244 · O 0.014 |
| Child C (무제한) | **2.05** | F 0.2816 · O 0.3747 · Li 0.1406 | (거의 없음) |

- **한 호스트에서 원소를 하나씩 넣은 값에 가장 가까운 것이 이 세 줄이다**: O 4.5 at% 에서 −2.88 GPa · 이어서 F 4.4 at% 에서 −0.53 · Cl 2.6 at% 에서 −0.49. 다만 (i) 누적 경로다 (독립 치환이 아니다) (ii) 넣을 때마다 Li · P · S · I 가 같이 줄어든다 (iii) 대리모형 값이다 (iv) 호스트가 유리고 상대가 LSPS 다.
- 알고리즘 (Methods): SHAP 값이 가장 양인 원소를 골라 제약 안에서 최적화 → SHAP 재계산 → 다음 원소. 방금 고친 원소가 다시 1 위면 2 위로 넘어간다 ('pseudo-longest red bar'). 더 못 내릴 때까지.
- 본문: *"The general trend of adding more F, O, Cl, Br for reduced K_crit as predicted by the SHAP model is also in good agreement with the elemental correlation map."* — Sb · I 에서는 맞지 않는다 (§14-9).

### 5.6 `Table S1` · `Table S2` 전사 (ESI p. 6–7 · PDF 텍스트)

제약: Child A = 원소별 변화 ≤ 0.05 ('95 % constraint' · C 5) · Child B = ≤ 0.10 (C 10) · Child C = 제약 없음 (C 100). 조성은 원자 1 개 기준으로 정규화. 캡션이 인정하듯 제약은 근사다 (한 원소를 바꾸면 다른 원소가 따라 바뀐다). K_crit 단위 GPa · 전부 **예측값**.

**`Table S1` — LSPS 와의 4 V 계면**

| # | Parent 유리 | σ (mS/cm) [ESI ref] | K_crit | Child A | K_crit | Child B | K_crit | Child C | K_crit |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Li0.364P0.110S0.388I0.138 | 1.7 [1] | 16.07 | Li0.324O0.04F0.042P0.098S0.346Cl0.026I0.123 | 12.07 | Li0.306O0.014F0.090P0.093S0.324Cl0.002Br0.03Sb0.024I0.115 | 6.89 | Li0.141O0.375F0.282P0.01S0.14I0.053 | 2.05 |
| 2 | Li0.338B0.169S0.351I0.143 | 0.2 [2] | 15.7 | Li0.335B0.135O0.019F0.047S0.322Cl0.002I0.142 | 11.23 | Li0.322B0.069F0.102P0.015S0.275Br0.042Sb0.038I0.136 | 5.46 | Li0.113B0.010O0.323F0.282S0.138Cl0.010I0.048Bi0.076 | 1.90 |
| 3 | Li0.431Si0.092S0.323I0.154 | 0.04 [3] | 17.74 | Li0.369O0.033F0.041Si0.067P0.039S0.274Cl0.044I0.132 | 12.45 | Li0.406F0.103Si0.004P0.015S0.273Cl0.001Sb0.053I0.145 | 5.49 | Li0.149O0.336F0.321S0.140I0.053 | 2.19 |
| 4 | Li0.423O0.013Si0.118P0.003S0.443 | 0.12 [4] | 17.4 | Li0.362O0.033F0.043Si0.068P0.003S0.394Cl0.046Br0.045Pb0.006 | 11.78 | Li0.376O0.093F0.082Si0.019P0.003S0.355Cl0.059K0.001Sb0.012 | 7.51 | Li0.123O0.288F0.281P0.001S0.149Cl0.008Ti0.150 | 2.11 |
| 5 | Li0.333S0.500Ge0.167 | 0.15–0.5 [5,6] | 15.57 | Li0.300O0.033F0.043S0.449Cl0.025Ge0.150 | 10.75 | Li0.312O0.002F0.090S0.398Cl0.008Ge0.111Br0.040Sb0.013I0.022Pb0.004 | 5.93 | Li0.078O0.348F0.285P0.017S0.117Ge0.009Bi0.145 | 1.56 |
| 6 | Li0.333Si0.167S0.500 | 0.27 [4] | 15.2 | Li0.275O0.035F0.041Si0.140S0.413Cl0.042Br0.012Pb0.041 | 11.22 | Li0.266O0.065F0.068Si0.125S0.399Cl0.064Br0.005Sb0.009 | 8.66 | Li0.083O0.367F0.375P0.018S0.124Cl0.033 | 1.86 |
| 7 | Li0.400Si0.133S0.467 | 1.0 [7] | 16.51 | Li0.341O0.049F0.043Si0.133S0.398Cl0.025Br0.004Pb0.004 | 11.66 | Li0.338O0.065F0.072Si0.063S0.394Cl0.068 | 9.49 | Li0.147O0.365F0.301S0.177Cl0.010 | 2.21 |
| 8 | Li0.370Si0.130S0.389Cl0.111 | 0.05 [8] | 13.57 | Li0.334O0.048F0.021Si0.081S0.415Cl0.100 | 10.47 | Li0.287O0.096F0.083Si0.132P0.011S0.305Cl0.086 | 8.98 | Li0.070O0.188F0.317Si0.025S0.074Cl0.021Br0.306 | 2.27 |
| 9 | Li0.406O0.061Si0.130S0.403 | 0.1 [1] | 15.24 | Li0.297O0.092F0.039Si0.125S0.349Cl0.037Br0.025Pb0.036 | 10.68 | Li0.332O0.093F0.069Si0.030S0.330Cl0.061K0.001Zn0.044Br0.040 | 8.86 | Li0.223O0.040F0.445Si0.070S0.222 | 1.90 |
| 10 | Li0.425O0.013Si0.121S0.441 | 0.3 [9] | 16.62 | Li0.355O0.055F0.040Si0.127S0.399Cl0.025 | 11.82 | Li0.364O0.078F0.077Si0.023S0.378Cl0.080 | 9.00 | Li0.129N0.156O0.257F0.291Si0.006P0.010S0.131Cl0.020 | 1.81 |

**`Table S2` — LGPS 와의 4 V 계면 (같은 parent 10 종 · σ 열은 위와 같다)**

| # | Parent K_crit | Child A | K_crit | Child B | K_crit | Child C | K_crit |
|---|---|---|---|---|---|---|---|
| 1 | 13.31 | Li0.280O0.021F0.042P0.085S0.417Cl0.048I0.106 | 7.60 | Li0.319O0.021F0.105P0.010S0.387Cl0.099K0.018I0.040 | 3.88 | Li0.128C0.011N0.115F0.508P0.022S0.137K0.030I0.049 | 1.36 |
| 2 | 12.62 | Li0.345B0.119O0.008F0.037P0.037S0.308I0.146 | 9.23 | Li0.316B0.177N0.008F0.092S0.274I0.133 | 6.89 | Li0.100B0.050O0.199F0.466S0.104Ni0.038I0.042 | 2.83 |
| 3 | 12.77 | Li0.417O0.013F0.029Si0.120S0.272I0.149 | 7.75 | Li0.337N0.035O0.080F0.079P0.080S0.252I0.138 | 5.50 | Li0.137N0.010O0.220F0.461P0.020S0.103I0.049 | 2.13 |
| 4 | 13.35 | Li0.451O0.010F0.054Si0.078S0.408 | 8.58 | Li0.348N0.065F0.094S0.394Cl0.075K0.006 | 4.71 | Li0.117O0.247F0.453Si0.040P0.019S0.123 | 2.10 |
| 5 | 14.54 | Li0.272Ni0.034O0.030F0.042P0.021S0.444Cl0.042Ge0.115 | 9.25 | Li0.294O0.052F0.091P0.040S0.406Ge0.117 | 6.77 | Li0.051N0.267O0.520F0.054P0.098Ge0.010 | 2.05 |
| 6 | 13.56 | Li0.314O0.031F0.048Si0.148S0.459 | 8.90 | Li0.299O0.001F0.091Si0.206S0.403 | 6.02 | Li0.088O0.257F0.453Si0.050S0.132 | 2.09 |
| 7 | 13.68 | Li0.387O0.010F0.049Si0.083P0.035S0.435 | 8.68 | Li0.416O0.009F0.105Si0.103S0.367 | 5.74 | Li0.106O0.257F0.454Si0.040P0.020S0.124 | 2.10 |
| 8 | 9.61 | Li0.359O0.013F0.050Si0.089P0.033S0.349Cl0.108 | 6.26 | Li0.330O0.017F0.096Si0.115P0.016S0.327Cl0.099 | 4.18 | H0.011Li0.125N0.012O0.011F0.579P0.026S0.131Cl0.037Ni0.025Br0.043 | 1.80 |
| 9 | 13.45 | Li0.376O0.068F0.051Si0.081P0.035S0.355Cl0.034 | 7.63 | H0.003Li0.288O0.068F0.067Si0.180P0.078S0.219Cl0.096 | 4.62 | Li0.329F0.516Si0.070P0.021S0.065 | 1.04 |
| 10 | 13.35 | Li0.458O0.010F0.054Si0.071S0.407 | 8.59 | Li0.390F0.103Si0.023S0.376Cl0.105Ge0.003 | 4.15 | Li0.118O0.247F0.453Si0.040P0.019S0.122 | 2.10 |

- 요약 (우리 산술): 평균 K_crit — `Table S1` parent 15.96 → A 11.41 → B 7.63 → C 1.99 GPa (평균비 0.72 · 0.48 · 0.13) / `Table S2` 13.02 → 8.25 → 5.25 → 1.96 (0.63 · 0.40 · 0.15). 본문 (p. 4579) 의 범위 서술 *"15–17 … 10–13 … 6–9 … 1.5–2 GPa"* 는 표의 실제 범위 (13.57–17.74 · 10.47–12.45 · 5.46–9.49 · 1.56–2.27) 보다 좁다.
- 새로 들어온 원소 (행 수): `Table S1` child A — **F 10 · Cl 9 · O 7** · Br 4 · Pb 4 · P 1 / child B — F 10 · Cl 8 · **Sb 6** · O 5 · Br 5 · P 3 · K 2 · I · Pb · Zn / child C — F 10 · O 7 · Cl 5 · P 3 · Bi 2 · Ti · Br · N. `Table S2` 에는 H · C · N · K · Ni 도 나온다.
- Child C 는 O + F 가 0.49–0.74 · Li 가 0.05–0.33 인 **산불화물**이다 — 황화물 유리가 아니다.
- 저자 단서 (p. 4579): *"in practice it is preferable to make the minimum possible compositional changes to lower the K_crit, as the ionic conductivity will likely fall quickly as composition is deviated."* child 의 전도도는 예측 · 측정 어느 쪽도 없다.
- ⚠ σ 열의 출처 번호가 조성과 맞지 않는 행이 여럿이다 (§16-6) — 전도도는 이 표에서 가져오지 말고 원전을 찾는다.

### 5.7 수정 수준별 예측 — 유리/LGPS 계면과 유리 자기분해 (`Fig. 5a` · `Fig. 5b` · `Fig. S4` · `Fig. S6` · p. 4580–4581)

첫 parent 유리에 'x % 수정' (원소별 화학양론 변화 ≤ x/100) 을 건 계열 0 · 1.25 · 2.5 · 4 · 5 · 6 %. 5 % = `Table S2` 1 행 child A. **1.25 · 2.5 · 4 · 6 % 의 조성은 어디에도 없다.** 아래는 전부 `figure-read ≈` (대괄호 = 표에 인쇄된 값).

| 수정 수준 (%) | 0 | 1.25 | 2.5 | 4 | 5 | 6 | 그림 |
|---|---|---|---|---|---|---|---|
| K_crit 계면 4 V (GPa) | 13.33 [13.31] | 11.07 | 9.07 | 7.96 | 7.60 [7.60] | 7.32 | `Fig. 5b` |
| K_crit 계면 3 V | 7.49 | 7.35 | 6.89 | 5.92 | 5.31 | 4.89 | `Fig. S4b` |
| K_crit 계면 2 V | 4.60 | 4.11 | 4.01 | 3.78 | 3.79 | 3.53 | `Fig. S4a` |
| K_crit 유리 자기분해 3.5 V | 4.04 | 5.51 | 4.86 | 5.05 | 5.30 | 5.10 | `Fig. S6` 왼쪽 |
| 계면 분해 E · 4 V · K_eff = 0 (eV/atom) | 0.427 | 0.381 | 0.332 | 0.286 | 0.264 | 0.284 | `Fig. 5a` |
| 〃 K_eff = 5 GPa | 0.267 | 0.210 | 0.149 | 0.107 | 0.091 | 0.090 | `Fig. 5a` |
| 〃 K_eff = 10 GPa | 0.107 | 0.037 | 0 | 0 | 0 | 0 | `Fig. 5a` |
| 〃 K_eff = 15 GPa | 0 | 0 | 0 | 0 | 0 | 0 | `Fig. 5a` |
| 계면 분해 E · 3 V · K_eff = 0 | 0.182 | 0.153 | 0.119 | 0.122 | 0.112 | 0.101 | `Fig. S4d` |
| 〃 K_eff = 3 / 6 / 8 GPa | 0.109 / 0.036 / 0 | 0.090 / 0.028 / 0 | 0.067 / 0.015 / 0 | 0.060 / 0 / 0 | 0.049 / 0 / 0 | 0.039 / 0 / 0 | `Fig. S4d` |
| 계면 분해 E · 2 V · K_eff = 0 | 0.0554 | 0.0491 | 0.0461 | 0.0411 | 0.0399 | 0.0433 | `Fig. S4c` |
| 〃 K_eff = 2 / 4 / 6 GPa | 0.0313 / 0.0071 / 0 | 0.0252 / ≈ 0.001 / 0 | 0.0231 / 0 / 0 | 0.0194 / 0 / 0 | 0.0187 / 0 / 0 | 0.0188 / 0 / 0 | `Fig. S4c` |
| 유리 자기분해 E · 3.5 V · K_eff = 0 | 0.378 | 0.354 | 0.348 | 0.350 | 0.369 | 0.331 | `Fig. 5b` · `Fig. S6` 오른쪽 |
| 〃 K_eff = 3 / 5 / 6 GPa | 0.097 / 0 / 0 | 0.160 / 0.032 / 0 | 0.133 / 0 / 0 | 0.142 / ≈ 0.004 / 0 | 0.160 / 0.021 / 0 | 0.137 / ≈ 0.006 / 0 | `Fig. S6` 오른쪽 |

(0 으로 적은 칸은 마커가 K_eff 가 더 큰 계열의 빨강 마커 밑에 가려 선으로 읽었다. '≈' 가 붙은 작은 값은 눈 판독이다.)

- 본문 (p. 4581): K_eff 5 GPa 는 분해 에너지를 낮추되 경향은 유지 · 10 GPa 는 2.5 % 넘게 수정한 child 를 4 V 에서 안정화 · 15 GPa 면 parent 까지 전부 안정. *"Note that the K_crit at 2 V are all below 4.6 GPa and that at 3 V are all above 4.9 GPa at all modifications."* (판독: 2 V 최댓값 4.60 · 3 V 최솟값 4.89 — 맞는다.)
- K_crit 는 전압과 함께 커진다 (parent: 2 V 4.6 → 3 V 7.5 → 4 V 13.3 GPa).
- 논문이 말하지 않은 것: **유리 자기분해의 K_crit 는 수정 뒤에 오히려 높다** (4.04 → 4.86–5.51 GPa). 다만 그 차는 모형 RMSE (2.59 GPa · 그것도 LSPS 4 V 모형의 값) 안쪽이다.

### 5.8 실험 — CV (`Fig. 5c` · `Fig. 5d` · `Fig. S5` · p. 4581 · Methods p. 4581–4582)

- 합성: 비정질 SE 'P1–C6' 을 고에너지 볼밀 350 rpm · 20 h. 원료 **Li₂S · P₂S₅ · LiI · LiF · Li₂O** (*"Stoichiometric amounts"*). ⚠ Cl 원료가 없다.
- 양극: LGPS–비정질 SE–탄소 복합 **1 mg** (중량비 45 : 45 : 10) + PTFE 5 % · 건식 압연 필름 · 0.49 cm² (본문은 *"diameter … 0.49 cm²"* 로 적었다). **양극 활물질은 없다.**
- 셀: Li/graphite (용량비 2.5 : 1) – **Li₅.₅PS₄.₅Cl₁.₅** – LGPS (120 mg) – 양극. 아지로다이트 층은 음극 쪽 계면을 안정시키려는 것이다 (ref 21). 초기 가압 **467 MPa** · 작동 **250 MPa**.
- CV: 개방회로 전압 → **8.5 V** · **0.1 mV/s**. 대조 'LGPS + C' = LGPS + 탄소 (90 : 10) 0.5 mg · 유리 없음.
- 봉우리 둘: H_L = 3 V 근처의 뾰족한 프리피크 (`Fig. 5c` 의 정의 — 프리피크 꼭대기에서 그 밑에 그은 점선 기준선까지) · H_R = 3.5 V 근처의 넓은 봉우리 (꼭대기에서 시작 전류 수준까지).

| 시료 | H_L (µA) `figure-read ≈` | H_R (µA) `figure-read ≈` | 프리피크 위치 (V) | 넓은 봉우리 위치 (V) |
|---|---|---|---|---|
| Parent | 17.0 | 28.8 | 2.85 | 3.45 |
| C1.25 | 9.8 | 11.9 | 2.85 | 3.34 |
| C2.5 | 9.1 | 12.9 | 2.84 | 3.29 |
| C4 | 8.2 | 19.6 | 2.85 | 3.47 |
| C5 | 6.6 | 24.7 | 2.78 | 3.46 |
| C6 | 6.1 | 19.9 | **2.64** | 3.32 |
| LGPS + C (대조) | 프리피크 없음 | ≈ 8 (본문 *"below 9 µA"*) | — | ≈ 3.2 |

(H 값은 `Fig. 5d` · 위치는 `Fig. 5c` 곡선 판독. C1.25 · C2.5 의 넓은 봉우리는 평평해서 위치 ±0.05 V.)

- `Fig. S5` (parent 와 C6 의 첫 5 사이클 · 2.4–5.0 V · 전류 축 있음) `figure-read ≈`:

| | Parent | C6 |
|---|---|---|
| 1 사이클 프리피크 | 2.83 V · 15.5 µA (절대 전류) | 2.70 V · 8.1 µA |
| 1 사이클 넓은 봉우리 | 3.47 V · 22.9 µA | 3.42 V · 17.9 µA |
| 1 사이클 5.0 V 끝 | ≈ 7.9 µA | ≈ 8.5 µA |
| 2 · 3 · 4 사이클의 최대 전류 (4.8–5.0 V) | ≈ 3.6 · 2.4 · 1.8 µA | ≈ 4.3 · 3.0 · 2.3 µA |
| 2 사이클 4.0 V | ≈ 0.5 µA | ≈ 0.6 µA |

- 본문 서술: H_L 은 수정과 함께 단조 감소 · H_R 은 진동. 첫 충전 뒤에는 방전과 다음 사이클 (4 V 아래) 에서 분해 전류가 거의 사라진다.

### 5.9 논문의 해석 사슬 (p. 4581)

1. H_R 의 조성 의존성은 K_eff = 0 에서의 **유리 자기분해 에너지 (3.5 V)** 와 *"a very similar trend"* → 넓은 봉우리 = 냉간 압착 펠릿의 기공 근처 (K_eff = 0) 에서 일어나는 유리 자기분해.
2. LGPS + C 대조는 넓은 봉우리만 (9 µA 아래) → LGPS 자기분해는 유리 수정과 무관한 배경.
3. *"Thus, the pre-peak H_L has to be contributed by the interface decomposition between LGPS and glass at a weak local mechanical constriction"* — 소거법이다.
4. 프리피크가 전부 3 V 근처 → 초기 계면의 **K_eff ≈ 4.6–4.9 GPa** (2 V 의 K_crit 전부보다 높고 3 V 의 K_crit 전부보다 낮다).
5. 첫 충전 뒤 전류가 사라진다 → 국소 분해가 K_eff 를 계면 K_crit (< 14 GPa) 과 유리 자기 K_crit (< 6 GPa) 위로 올렸다 → 충전된 펠릿 전체에서 K_eff > 14 GPa.
6. 결정 LSPS (ref 12) · LGPS (refs 1, 4, 13) 의 K_eff 상한은 계산–실험 대조로 **15–20 GPa** 쯤 — 전해질의 탄성률이 정하고, 결정 (ref 19) 과 비정질 (ref 20) 황화물이 비슷하다.
7. 결론 단서: *"the examples given here are tested at an experimental condition with strong mechanical constriction … so that the decomposition current is largely inhibited after the initial charge regardless of the composition"* — 즉 **설계의 이득이 나야 할 '약한 구속' 조건은 시험하지 않았다.** 조성 수정 전략이 공극 제거 · 미세 균열 방지의 부담을 덜 것이라는 것은 전망이다.

---

## 6. 검산 · 유도량 ★ (전부 **우리 산술** — 논문 값이 아니다)

### 6.1 K_eff 곡선은 전부 한 식이다

`Fig. 5a` · `Fig. S4c` · `Fig. S4d` · `Fig. S6` 의 K_eff > 0 곡선 8 묶음이 **G(K_eff) = G₀ · (1 − K_eff / K_crit)** (0 에서 자름) 을 판독 오차 안에서 따른다 (최대 차 0.0009 eV/atom). 예 — parent · 4 V: 0.427 × (1 − 5/13.33) = 0.267 (판독 0.267) · 0.427 × (1 − 10/13.33) = 0.107 (판독 0.107).
⇒ 이 곡선들은 (G₀, K_crit) 두 수의 다른 표현이고 새 정보가 없다. 압력에 따라 산물을 다시 고르는 계산이 아니다. 본문의 *"Using the predicted K_crit of SEI at 4 V, we further predict the 4 V interface (to LGPS) decomposition energy"* 가 이 뜻이다.

### 6.2 ε_RXN · V⁰ 역산 = G₀ / K_crit

식 (3) 에서 ε_RXN·V⁰ = |ΔG⁰_RXN| / K_crit (1 eV/GPa = 160.2 Å³).

| 수정 수준 (%) | 0 | 1.25 | 2.5 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 유리/LGPS 계면 · 2 V (Å³/atom) | 1.93 | 1.92 | 1.84 | 1.74 | 1.69 | 1.97 |
| 유리/LGPS 계면 · 3 V | 3.90 | 3.33 | 2.76 | 3.30 | 3.38 | 3.31 |
| 유리/LGPS 계면 · 4 V | 5.14 | 5.52 | 5.87 | 5.76 | 5.57 | 6.21 |
| 유리 자기분해 · 3.5 V | 14.98 | 10.30 | 11.46 | 11.11 | 11.16 | 10.38 |

- 이것이 **이 논문에서 꺼낼 수 있는 유일한 '부피' 숫자**다 — 논문은 ε_RXN 도 V⁰ 도 어떤 계에도 적지 않았다 (서론의 LGPS +2 % · > 30 % 는 선행 연구 인용).
- 유리 자기분해의 15 Å³/atom 은 원자 부피 (20 Å³ 안팎으로 어림) 의 절반을 넘는다. Li 를 뺀 고체 산물만으로 이 크기가 나오는지, 'atom' 과 V⁰ 의 기준이 무엇인지 이 논문으로는 알 수 없다 (§4.4).
- ⚠ K_crit 가 대리모형 예측값이면 이 역산은 그 오차 (RMSE 2.59 GPa) 를 그대로 안는다.

### 6.3 K_crit 가 내려간 이유의 분해 (4 V · 유리/LGPS)

K_crit 비 = (G₀ 비) ÷ (ΔV 비).

| 수정 수준 | K_crit | G₀ | ε_RXN·V⁰ | 하락 중 G₀ 의 몫 (로그 기준) |
|---|---|---|---|---|
| 1.25 % | ×0.830 | ×0.892 | ×1.075 | 61 % |
| 2.5 % | ×0.680 | ×0.777 | ×1.143 | 65 % |
| 4 % | ×0.597 | ×0.669 | ×1.121 | 78 % |
| 5 % | ×0.570 | ×0.619 | ×1.084 | 86 % |
| 6 % | ×0.549 | ×0.664 | ×1.209 | 68 % |

- 3 V 에서는 6 % 의 K_crit ×0.653 이 G₀ ×0.555 에서 다 나오고 부피 항은 반대로 움직였다 (×0.85). 2 V 는 G₀ 몫 93 %.
- ⇒ **이 예제에서 '기계적 설계' 가 한 일의 대부분은 분해 구동력 (화학 항) 을 줄인 것**이다. 부피 항은 4 V 에서 8–21 % 를 보탰을 뿐이고 그것도 모형 오차 안쪽이다. 저자의 원소 해석 (§5.2 — 탈리튬화가 덜 된다) 과 같은 이야기다.

### 6.4 예측 ↔ 측정의 순위 상관 (n = 6 · 셀 하나씩)

| 쌍 | Spearman ρ |
|---|---|
| H_L ↔ K_crit(4 V) · K_crit(3 V) | +1.00 · +1.00 |
| H_L ↔ 계면 분해 E (3 V · K_eff = 0) | +0.94 |
| H_R ↔ 유리 자기분해 E (3.5 V · K_eff = 0) | **+0.49** (여섯 순위 중 넷이 일치 · 1.25 % 와 6 % 가 뒤바뀜) |
| H_R ↔ 자기분해 E · child 다섯만 | **+0.10** |

- H_L: 순위는 완전히 맞는다. 그러나 **가장 큰 변화는 가장 작은 수정에서 난다** — parent → C1.25 에서 H_L −42 % · H_R −59 % 인데, 같은 구간의 예측은 K_crit(3 V) −1.9 % · 계면 E(3 V) −16 % · 자기분해 E −6 % 다. C1.25 → C6 구간은 H_L −37 % ↔ K_crit(3 V) −33 % 로 비슷하다.
- H_R: 예측 에너지는 0.331–0.378 eV/atom (1.14 배) 안에서 움직이는데 측정 전류는 11.9–28.8 µA (2.4 배) 다. *"very similar trend"* 는 parent 가 가장 높다는 것과 5 % 에 봉우리가 있다는 모양 두 가지에 기댄다.

### 6.5 K_eff 가 같다면 분해 개시 전압은 어디인가

논문의 논리 (K_crit(φ) 가 K_eff 를 넘는 전압에서 계면 분해가 시작) 를 2 · 3 · 4 V 세 점의 선형 보간으로 따라가면 (보간은 우리 가정):

| K_eff (GPa) | Parent | C1.25 | C2.5 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|
| 4.6 | 2.00 V | 2.15 | 2.20 | 2.38 | 2.53 | 2.79 |
| 4.75 | 2.05 | 2.20 | 2.26 | 2.45 | 2.63 | 2.90 |
| 4.9 | 2.10 | 2.24 | 2.31 | 2.52 | 2.73 | 3.00 |

- 모형대로면 개시 전압은 parent 에서 C6 로 **약 0.8–0.9 V 올라가야** 한다. 측정된 프리피크는 2.85 → 2.64 V 로 **0.2 V 내려간다** (`Fig. 5c` · `Fig. S5` 도 2.83 → 2.70 V). 방향이 반대다.

### 6.6 대리모형은 25 GPa 아래 자료로만 학습된 것으로 보인다

`Fig. S1b` (LSPS) 히스토그램을 25 GPa 에서 자르면 N ≈ 16,000 (80 %) · **평균 14.41 · 분산 27.89** — `Fig. S3` 뿌리 노드에 인쇄된 **value 14.416 · mse 27.974** 와 0.5 % 안에서 같다 (24 GPa 에서 자르면 14.21 · 26.42 / 26 GPa 면 14.62 · 29.63 / LGPS 를 25 에서 자르면 14.32 · 24.77 로 안 맞는다). `Fig. 4b` 의 두 축도 25 GPa 에서 끝난다.
- ⇒ 본문에 없는 전처리 (K_crit ≤ 25 GPa 만 사용) 가 있었다고 읽는 것이 그림과 맞는다. 분포의 위쪽 20 % 는 모형 밖이다.
- 그 범위의 분산이 27.97 이면 RMSE 2.59 GPa 는 **R² ≈ 0.76** 에 해당한다 (시험 분산이 뿌리와 같다는 전제).
- 뿌리 samples = 10000 인데 시험도 10,000 이다. 25 GPa 아래 LSPS 자료가 약 16,000 이면 겹치지 않는 학습 10,000 + 시험 10,000 은 나오지 않는다 → 학습 · 시험 분할이 어떻게 됐는지 알 수 없다.

### 6.7 child 조성의 전하합 — 적힌 전구체로는 못 만든다

명목 산화수 (Li +1 · P +5 · Si +4 · Ge +4 · B +3 · S −2 · O −2 · F −1 · Cl −1 · Br −1 · I −1 …) 로 Σ xᵢzᵢ 를 내면:

- **parent 20 칸은 전부 0.000 ± 0.002** (전하 균형).
- `Table S1` child A: 10 칸 중 9 칸이 음 (−0.39 … −0.07) · `Table S2` child A: −0.37 … +0.15 (음 7 · 양 2 · 0 근처 1). child B · C 는 더 벗어난다 (child C 는 S 가 황산염처럼 양이온일 수 있어 이 셈이 의미를 잃는다 — A 에만 쓴다).
- 실험한 계열의 5 % 조성 (`Table S2` 1 행 child A · Li0.280O0.021F0.042P0.085S0.417Cl0.048I0.106) 은 **Σxz = −0.367** 이다. Li 는 0.364 → 0.280 으로 줄고 S 는 0.388 → 0.417 로 늘었다 — 5 % 제약도 넘는다 (Li −0.084).
- 논문이 적은 전구체 Li₂S · P₂S₅ · LiI · LiF · Li₂O 는 각각 Σxz = 0 이고, 그 혼합은 어떤 비율이든 Σxz = 0 이다 (선형 제약 · 결합 상태와 무관). ⇒ **Σxz ≠ 0 인 예측 조성은 이 전구체로 만들 수 없다.** Cl 도 원료에 없다.
- 읽는 법: 음의 전하합 = 전하 균형선보다 Li 가 모자란 (= 이미 산화된 쪽) 조성이다. 알고리즘은 O · F · Cl 을 넣으면서 Li 를 빼는 방향으로 간다 — **미리 탈리튬화된 조성이 4 V 에서 덜 분해하는 것은 당연하다.**
- ⇒ 합성된 C1.25–C6 의 실제 조성은 예측 조성과 다를 수밖에 없고, 논문은 그 조성을 적지 않았다.

---

## 7. ★ 갭 질문에 대한 답 (사용자 지정 7 항 · 쪽 · 절 · 그림/표 번호)

> 쪽 번호는 저널 쪽 (4574–4583) · ESI 는 'ESI p.' 로 적는다. 트랙: cascade (1저자 = 사용자) 문헌 갭 점검.

| # | 질문 | 답 | 근거 위치 |
|---|---|---|---|
| 1 | **무엇을 스크린했나** — 전해질 조성? 코팅/중간층? SEI 산물? 몇 개 · 어떤 DB? | **코팅 물질**이다. MP 의 '전자 절연체' > 20,000 종을 고정된 황화물 SE 4 종 (LGPS · LSPS · Li₇P₃S₁₁ · Na₇P₃S₁₁) 과 짝지은 유사상 계면 > 80,000 개 (SE 당 약 2 만 · figure-read). 자료 한 점 = (초기 SEI 조성, K_crit). 그 뒤 알려진 황화물 유리 10 종 × child 3 단계 × 상대 SE 2 종 (LSPS · LGPS) 을 대리모형으로 최적화. 실험은 유리 1 종 + 변형 5 종. **전해질 조성은 스크린하지 않았고 (SE 4 종 고정) · SEI 산물 자체는 스크린 대상이 아니다** (산물 이름조차 안 나온다). DB = Materials Project + pymatgen | p. 4577 오른쪽 ("Over 80 000 SEI's …") · Methods p. 4582 "High-throughput computation" · `Fig. 2` · `Fig. 3a` · `Fig. S1` · `Table S1` · `Table S2` (ESI p. 6–7) |
| 2 | **기계적 구속이 스크린 축인가** · 식 · 매개변수 · Li 저장소 · 부피 정규화 | **예 — 유일한 축이다.** 목표 변수가 K_crit. 식: p = K_eff·ε_RXN (번호 없음 · p. 4575) · 식 (1) 유사상 분해 · 식 (2) 산물이 p = K_eff·ε_RXN 아래 (p. 4576) · **식 (3) ΔG⁰_RXN + K_crit·ε_RXN·V⁰ = 0** (p. 4577). 매개변수: K_eff (GPa · 그림에 쓴 값 0–15) · ε_RXN (stress-free 반응 변형률) · V⁰ ('reference volume'). Li 저장소: 조립 = 닫힌계 · 사이클 = 열린계 (grand potential · 2 / 3 / 3.5 / 4 V). 부피: `Fig. 1d` 부피 행은 고체 상만. ⛔ **ε_RXN 의 식 · Li 부피 처리 · 기체 처리 · V⁰ 의 정의는 없다** (refs 11–13 위임) · ε_RXN 수치도 없다 | p. 4575 왼쪽 · p. 4576 식 (1)(2) · p. 4577 식 (3) · `Fig. 1b`–`Fig. 1d` · Methods p. 4582 · 이 digest §4.4 |
| 3 | **도핑/치환 아지로다이트 · 한 호스트의 도펀트 계열이 있나 · 도펀트별 값?** | **아지로다이트: 없다 (계산 0).** Li₅.₅PS₄.₅Cl₁.₅ 는 시험 셀의 음극 쪽 보호층일 뿐이고, ref 8 (Adeli 2019) 은 서론의 일반 인용이다. **한 호스트 계열: 유리 하나 (Li₂S–P₂S₅–LiI 계) 의 '수정 수준' 계열 0–6 % 가 있다** — 그러나 축이 도펀트 종류가 아니라 수정량이고 O · F · Cl 이 같이 들어간다. 도펀트별 값에 가장 가까운 것 = `Fig. 4c` 의 누적 세 단계 (O → F → Cl: 16.07 → 13.19 → 12.66 → 12.17 GPa · 대리모형 · LSPS 계면 · 4 V) 와 `Fig. 3b` 의 원소 상관 지도 (숫자 없이 색). **도펀트별 숫자 표는 없다** | Methods p. 4581–4582 (셀 구성) · p. 4579–4580 · `Fig. 4c` · `Fig. 3b` · `Fig. 5` · `Fig. S4` |
| 4 | **분해 산물 (SEI) 을 물성으로 순위/점수 매기나** (전자 전도/띠틈 · Li⁺ 전도 · 부피 · 금속성 산물) | **아니오.** 점수는 K_crit (와 분해 에너지) 하나다. 전자 쪽은 **입력 코팅**을 '전자 절연체' 로 미리 거른 것이 전부 (기준 미기재) — 산물의 띠틈 · 금속성은 보지 않는다. Li⁺ 전도는 parent 유리의 문헌값 (0.04–1.7 mS/cm) 을 표에 싣고 '조성을 조금만 바꾸자' 는 경험칙으로 대신한다 — child 의 전도도 예측 없음. 부피는 ε_RXN 으로 K_crit 안에 들어가지만 따로 보고하지 않는다 | p. 4577 ("electronic insulators") · p. 4579 ("ionic conductivity will likely fall quickly") · `Table S1` σ 열 |
| 5 | **음극 쪽 vs 양극 쪽 · 전압 창** | **양극 쪽 (산화) 만.** K_crit 는 *"at a cathode voltage (e.g., from 2 V to 4 V) vs. lithium metal"* — 주 결과 4 V · 보조 2 V · 3 V (`Fig. S4`) · 유리 자기분해 3.5 V. 실험 CV 는 개방회로 전압 → 8.5 V (`Fig. 5c`) 와 2.4–5.0 V 5 사이클 (`Fig. S5`). 음극 쪽은 계산하지 않았다 (셀에서는 Li/graphite + Li₅.₅PS₄.₅Cl₁.₅ 층으로 처리) | p. 4577 오른쪽 · `Fig. 3` 캡션 ("at 4 V") · `Fig. S4` · `Fig. S6` · Methods p. 4582 |
| 6 | **Li₆PS₅Cl · LGPS · LSPS 등의 구체 숫자와 실험 검증** | **Li₆PS₅Cl: 숫자 없음.** LGPS (전부 선행 연구 인용): 화학 분해 (→ Li₄GeS₄ + Li₃PS₄) 부피 +2 % · 완전 산화/환원 극한 > 30 % · 비구속 창 1.7–2.1 V · 구속 (준)안정 창 ≈ 1–4 V · 동역학 0–10 V (p. 4575). 이 논문의 새 숫자: K_crit 분포 (Li₇P₃S₁₁ 18.5 / 14.8 / 13.0 GPa · 나머지 셋은 figure-read · §5.1) · 유리/LSPS · 유리/LGPS 의 K_crit (`Table S1` · `Table S2`) · parent 유리/LGPS 의 K_crit 4.6 / 7.5 / 13.3 GPa (2 / 3 / 4 V · figure-read) 와 계면 분해 에너지 0.055 / 0.18 / 0.43 eV/atom · K_eff 추정 4.6–4.9 GPa (초기 계면) · > 14 GPa (첫 충전 뒤) · 결정 LSPS/LGPS 상한 15–20 GPa. **반응 변형률 수치는 이 논문 계에 대해 하나도 없다.** 실험 = 유리 6 종 + LGPS + 탄소 복합 양극의 CV (250 MPa): 프리피크 H_L 17.0 → 6.1 µA 단조 감소 (figure-read) · 넓은 봉우리 H_R 은 진동 · 첫 충전 뒤 4 V 아래 전류 소멸 | p. 4575 · p. 4578 · p. 4580–4581 · `Fig. 5` · `Fig. S4`–`Fig. S6` · `Table S2` · Methods p. 4581–4582 |
| 7 | **'SEI 설계' 의 설계 변수** | **코팅 (유리) 의 원소 조성**이다 = 초기 SEI 의 조성. 원소별 최대 변화 (5 % · 10 % · 무제한 / 실험 계열 1.25–6 %) 안에서 O · F · Cl (· Br) 을 넣고 Li · P · S · I 를 조금 줄인다. **구속 압력은 설계 변수가 아니다** (K_eff 는 주어진 환경이고 사후에 추정한다) · 중간층 구조 · SE 본체의 도펀트도 아니다. 맺음말에서 *"the composition modification strategy for the electrolyte and coating materials"* 로 SE 까지 넓혀 말하지만 계산 · 실험은 코팅뿐 | p. 4577 왼쪽 ("designing the initial SEI's such that they don't grow") · p. 4579–4580 · Methods p. 4582 "Feature attribution and composition optimization" · p. 4581 맺음말 |

**보고서 표 '가' 줄에 대한 판정 (제안 — 보고서 · 원장은 고치지 않았다)**

- 보고서의 질문 *"구속 아래에서 조성 · SEI 산물을 스크린했나"* → **조성 (코팅 조성) 은 K_crit 로 스크린했다 · SEI 산물은 스크린 · 점수화하지 않았다.**
- 보고서 226 행의 접는 조건 *"도핑 아지로다이트의 구속 분해나 SEI 산물을 스크린했다면"* → **해당하지 않는다.** 갭 ('한 아지로다이트 호스트에서 도펀트별로 매긴 숫자 표' · 'SE 도펀트를 산물 물성으로 순위') 은 이 편으로는 깨지지 않는다.
- 다만 고칠 문장이 둘 있다.
  ① *"최근 HT/ML 계면 스크린은 부피를 아예 다루지 않는다"* (보고서 29 행) — 이 논문은 ε_RXN 이 들어간 K_crit 를 8 만 점의 **스크린 목표값**으로 썼다. '부피 · 구속을 축으로 쓴 HT 는 Fitzhugh 2021 이 있다 — 다만 ΔV/V 수치 0 · 코팅 조성 · 양극 전압만 · 손상 지표가 아니라 안정화 문턱' 으로 고치는 것이 맞다.
  ② A 의 **'SEI 설계' 문구는 이 논문 제목이 선점**했다 (뜻은 다르다 — 산물 물성이 아니라 기계적 준안정). 쓰려면 뜻을 갈라 쓰거나 다른 말을 쓴다.
- 새로 드러난 것: **'분해가 공극 · 균열을 메워 스스로 멈춘다'** 는 화학–기계 되먹임 서사가 여기 있다 (Broader context · p. 4581). B 의 '양의 변형률은 이롭다' 쪽 선행이고 정량은 없다. 수축 (접촉 손실) 쪽은 이 논문에 한 마디도 없다 — 보고서가 '가장 단단한 자리' 로 꼽은 양극 쪽 수축은 그대로 비어 있다.

---

## 8. DFT/계산 방법 ★

- **code / version**: VASP (판 미기재). *"All ab initio calculations of phase data were obtained following the Material Project calculation guidelines in the Vienna ab initio Software Package (VASP)"* · *"DFT data obtained from Materials Project"* — 어느 상을 MP 에서 가져오고 어느 상을 직접 계산했는지 구분이 없다 (SE 4 종이 MP 엔트리인지도).
- **functional + vdW**: **미기재** (MP 지침이면 PBE 계열 GGA/GGA+U 로 읽히나 논문은 범함수 이름을 적지 않았다) · 분산 보정 언급 없음.
- **pseudo / PAW · k-points · ecut · supercell**: 미기재 (MP 지침에 위임).
- **DFT+U**: 미기재.
- **AIMD / MLIP**: 없음. 온도 · 엔트로피 항 없음 (0 K 상 자료).
- **무질서 처리**: 없음. **유리를 '그 조성의 바닥상태 상 조합' 으로 대신한다** (*"predict K_crit of the ground state phase at any input composition"*) — 비정질의 에너지 · 부피는 어디에도 안 들어간다.
- **상도**: pymatgen (ref 22) · 유사 이원계는 binary-search 알고리즘 (ref 9) · 전기화학 안정성은 grand potential 상도.
- **구속**: *"performed on the computational platform we developed following the perturbation or Lagrangian optimization methods"* (refs 11–13). 판독으로는 선형 섭동 꼴이다 (§6.1).
- **전압**: 2 · 3 · 4 V (계면) · 3.5 V (유리 자기분해) vs Li.
- **ML**: Extremely Randomized Trees (ref 24) · 나무 수 50 (본문 · 캡션) 또는 30 (Methods) · 특징 = 원소 분율 (118 원소) · 목표 = K_crit · 시험 10,000 점 · RMSE 2.59 GPa (LSPS · 4 V 모형 하나만 보고) · SHAP (ref 17) · 탐욕적 조성 최적화. 학습 자료 수 · 분할 · 하이퍼파라미터 · 교차검증 미기재.
- **실험**: 볼밀 350 rpm · 20 h (Li₂S · P₂S₅ · LiI · LiF · Li₂O) / 양극 = LGPS : 유리 : 탄소 45 : 45 : 10 · 1 mg · PTFE 5 % · 0.49 cm² / 전해질층 LGPS 120 mg / Li₅.₅PS₄.₅Cl₁.₅ 층 / 음극 Li/graphite (용량비 2.5 : 1) / 467 MPa 초기 · 250 MPa 작동 / CV 0.1 mV/s · 개방회로 전압 → 8.5 V. XRD · XPS · 조성 분석 · 전도도 측정 **없음**.

---

## 9. Post-processing ★

- **무엇**: (i) 닫힌계 유사 이원 hull → x_m · 초기 SEI 조성 (ii) 그 조성의 grand potential 분해 에너지 + 반응 변형률 → 식 (2)(3) 으로 K_crit (iii) 분포 통계 · 원소 분율–K_crit 상관 지도 (iv) 결정트리 앙상블 회귀 → SHAP 귀속 → 조성 최적화 (v) CV 봉우리 높이 H_L · H_R 을 예측 K_crit · 분해 에너지와 **경향으로** 대조.
- **도구**: pymatgen · 자체 플랫폼 (비공개) · Extremely Randomized Trees · SHAP. 나무 그림의 노드 표기 (mse · samples · value) 는 scikit-learn 의 나무 내보내기 형식으로 보인다 (논문에 라이브러리 이름 없음).
- **수치화 · 기록 방식**: K_crit (GPa) 스칼라 하나 / 분포는 2 GPa 칸 히스토그램 0–80 GPa / 분해 에너지 eV/atom / 조성은 원자 1 개 기준 분율 / CV 는 전류 (µA) 봉우리 높이 — 전하량 적분 · 면적 정규화 · 반복 측정 없음.
- **우리가 재사용할 만한 표현**: `Fig. 1d` 의 세 국면 표 (조성 · 부피 · 압력 세 행) · `Fig. 5a` 꼴 (분해 에너지 vs 조성 · K_eff 를 매개변수로 한 곡선족 — 다만 §6.1 처럼 한 식의 다른 표현임을 밝혀야 한다).

---

## 10. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a–c | 유사상의 convex hull 도식. (a) 비구속: 노란 별 (유사상) 이 hull 위 G_hull 에 있다 (b) K_crit > K_eff: 산물 에너지가 Gᵢ + p(D)·Vᵢ 로 조금 올라가지만 분해는 그대로 (c) K_crit < K_eff: 유사상이 산물 아래로 내려가 안정. **봄** | K_crit 정의를 한 장으로 설명할 때의 도식 원형. 식 (3) 과 짝 |
| 1d | 세 국면 표 (초기 SEI 형성 · SEI 성장 · SEI 유지) × 조성 · 부피 · 압력 행 + 입자 삽화 (연갈색 SE · 보라 활물질 · 갈색 초기 SEI · 검정 2차 SEI). **봄** — 부피 행에 Li 가 없다는 것을 여기서 읽었다 | 회계 (Li 저장소 · 부피) 를 선언하는 표의 본보기이자 반례 — 조성 행의 N_Li 가 부피 행에서 사라진다 |
| 2 | 워크플로: 상 자료 + 알려진 유리 조성 → HT (전기)화학 안정성 → 결정트리 학습 (50) → 결정트리 최적화 → 이상적 계면. **봄** | 'HT → 대리모형 → 조성 역설계' 틀의 2021 년 사례 (우리 cascade 와 층위 비교용) |
| 3a | Li₇P₃S₁₁ 계면의 K_crit 히스토그램 (4 V · 0–80 GPa · 2 GPa 칸 · 최빈 14–16 GPa). **봄 + 픽셀 판독** | 분포 폭의 크기 감각 (표준편차 13 GPa). 80 GPa 위가 잘려 있다 |
| 3b | 주기율표 색 지도 = 원소 분율과 K_crit 의 상관 (빨강 = 낮춤). F 만 진하고 O · Cl · W · V 는 옅다. **봄 + 칸 색 판독 (76 원소)** | 우리 도펀트 목록의 부호를 한 번에 볼 수 있는 유일한 자리 — ⛔ 코팅 전체의 상관이라 호스트 도펀트 순위로 쓰지 않는다 |
| 4a,b | (a) 나무 일부 (F ≤ 0.096 → O ≤ 0.606 / Li ≤ 0.001) (b) 예측 vs 계산 K_crit 산점도 (LSPS · 4 V · RMSE 2.59 GPa). **봄** — 축이 25 GPa 에서 끝나고 대각선에 가는 선이 있다 | 대리모형 검증 그림을 읽을 때의 점검 항목 (범위 절단 · 정확히 맞는 점들의 선 = 누설 의심) |
| 4c | SHAP force plot 7 단: parent 16.07 → +O 13.19 → +F 12.66 → +Cl 12.17 → child A 12.07 → B 6.89 → C 2.05 GPa. **봄** | 한 호스트에 원소를 차례로 넣은 값의 유일한 예 (누적 · 대리모형). 색 뜻이 3b 와 반대임에 주의 |
| 5a,b | (a) 유리/LGPS 계면 분해 에너지 (4 V) vs 수정 수준 · K_eff 0 / 5 / 10 / 15 GPa (b) 예측 K_crit (4 V) 와 유리 자기분해 에너지 (3.5 V). **봄 + 마커 판독** | K_crit(φ) 와 분해 에너지를 한 계열로 그리는 꼴. 판독값으로 ε·V⁰ 역산 (§6.2) |
| 5c,d | (c) CV 곡선 7 개 (parent · C1.25–C6 · LGPS + C) 를 쌓아 그림 — 전류 눈금 없음 · H_L · H_R 정의 표시 (d) H_L · H_R vs 수정 수준. **봄 + 판독** | SE + 탄소 복합 '양극' CV 로 SE 분해 전류를 재는 실험 꼴. 프리피크 위치가 C5 · C6 에서 내려간다는 것은 그림에서만 보인다 |
| S1 | (a–c) LGPS · LSPS · Na₇P₃S₁₁ 의 K_crit 히스토그램 (d) 네 SE 의 평균 · 중앙 · 표준편차 막대. **봄 + 판독** | 본문에 숫자가 없는 세 SE 의 통계. LSPS 를 25 GPa 에서 자른 통계 = S3 뿌리 노드 (§6.6) |
| S2 | (1 − x) Li₇P₃S₁₁ + x A (A = LCO · LNO · LTO · LFPO) 의 K_crit vs x — 진동 · 다봉. **봄 + 판독** | pseudo-binary 에서 x_m 한 점만 보는 것의 위험을 보이는 그림. x → 0 의 14.7 GPa = SE 자기 값 |
| S3 | 결정트리 한 그루의 위 4 층 (노드마다 mse · samples · value). **봄 · 전사** | 뿌리 samples 10000 · value 14.416 · mse 27.974 — 학습 자료의 실체를 알려 주는 유일한 단서 |
| S4 | (a,b) 예측 K_crit 2 V · 3 V (c,d) 계면 분해 에너지 2 V · 3 V vs 수정 수준. **봄 + 판독** | K_crit 의 전압 의존 (2 → 3 → 4 V). 우리 작동창 상한 4.25 V 는 범위 밖 |
| S5 | parent 와 C6 의 CV 5 사이클 (2.4–5.0 V · 전류 축 있음). **봄 + 판독** | 유일하게 전류 눈금이 있는 CV. 2 사이클부터 4 V 아래 전류 소멸 · 5 V 근처는 C6 가 더 크다 |
| S6 | 유리 자기분해의 예측 K_crit (왼쪽) 과 분해 에너지 vs K_eff (오른쪽) · 3.5 V. **봄 + 판독** | 수정이 자기분해 K_crit 를 올린다는 것 (논문 무언급) |
| Table S1 | parent 유리 10 종과 child A · B · C 의 조성 · 예측 K_crit (LSPS · 4 V) · parent 전도도 문헌값. **PDF 텍스트** (§5.6 전사) | 전하합 검산의 재료 (§6.7). σ 열은 출처 번호가 어긋나 쓰지 않는다 |
| Table S2 | 같은 parent 의 LGPS · 4 V 판. **PDF 텍스트** (§5.6 전사) | 실험 계열 (`Fig. 5`) 의 5 % 조성이 1 행 child A 다 |

---

## 11. 우리 DFT 대비 → `our_dft_baseline.md` · `db/properties/` 원장

> 우리 값은 옮기지 않는다 (원장 경로만). 문헌값과 우리 절대값을 한 표에 놓지 않는다.

### 11.1 방법 · 정의 대조표

| 항목 | 이 논문 | 우리 (경로) | 차이 / 이유 |
|---|---|---|---|
| 보고량 | **K_crit(φ)** = 전압 φ 에서 분해를 멈추는 데 필요한 K_eff (GPa) = \|ΔG⁰_RXN\| / (ε_RXN·V⁰) | **φ_ox(K_eff)** = K_eff 에서의 창 가장자리 (V) — `tools/oxidation/constrained_esw.py` (선도 차수 · 전체 재최소화 · 혼합 세 판) | 같은 선형 관계의 **역함수**다. 개시 근처에서 K_crit(φ) ≈ n_e·e·(φ − φ₀)/ΔV. 다른 양이 아니라 다른 읽기 |
| 계 | 유리 코팅 / {LGPS · LSPS · Li₇P₃S₁₁ · Na₇P₃S₁₁} **계면 유사상** | 아지로다이트 호스트의 **자기분해** (comp1 · modelc · Cl 계열) — `db/properties/constrained_esw_results.json` · `constrained_esw_cl_scan*.json` | 계가 다르다 — 수치를 나란히 놓지 않는다 |
| Li 저장소 · 부피 | 조립 닫힌계 → 사이클 열린계. 부피 행은 고체만 (`Fig. 1d`) — 문장으로는 선언 없음 | 도구 머리말에 선언: 방출 · 소모 Li 는 음극 저장소로 가고 구속된 고체 부피에 세지 않는다 | 우리 쪽이 더 명시적이다. 논문 원전 (refs 11–13) 의 회계와 같은지는 **미확인** |
| 부피 자료 | MP 상 부피 (범함수 미기재) · 유리는 바닥상태 상 조합으로 대신 | 산물 = MP GGA/GGA+U 몰부피 · SE = 우리 DFT 셀 | 둘 다 분자성 산물 (S · P₂S₅ 류) 의 PBE 부피 과대 가능성을 안는다 |
| 전압 | 고정 전압 2 · 3 · 4 V 에서의 구동력 (완전 산화 쪽 산물) | 개시 반응 (첫 단계) 의 가장자리 · 판단은 작동창 2.5–4.25 V | 논문은 '4 V 에서 얼마나', 우리는 '어디서 시작' — 산물 단계가 다르다 |
| ε_RXN 의 부호 | 양 (팽창) 을 전제. ε ≤ 0 처리 미기재 | 반응마다 부호를 원장에 적는다 — 개시 반응의 부호는 조성에 따라 갈린다 (값은 원장에서) | 논문 틀은 팽창에서만 작동한다. 수축은 틀 밖 (보고서 B-③) |
| 대리모형 | 조성 → K_crit 결정트리 (RMSE 2.59 GPa) | 없음 (구속 ESW 는 직접 계산) | — |
| 탄성률 | K_eff = 국소 유효 구속 탄성률 (추정 4.6–4.9 → > 14 GPa · 상한 15–20 GPa) | B₀ · E_VRH 정본 (`canonical_registry.json` 의 `b0-dft-bm3-v1` · `elastic-dft-relaxedion-*`) | ⛔ 같은 양이 아니다. K_eff 는 미세구조 · 접촉 · 공극이 정하는 유효값이고 B₀ 는 무결함 벌크다. 논문도 상한이 전해질 탄성률에서 온다고만 한다 |
| 실험 | SE + 탄소 복합 양극 CV | 없음 (계산 트랙) | — |

### 11.2 트랙별 판정 — 선점 · 지지 · 무관

| 우리 항목 · 트랙 | 관계 | 한 줄 근거 |
|---|---|---|
| 문헌 갭 '한 아지로다이트 호스트의 도펀트별 숫자 표' (cascade · 1저자 = 사용자) | 갭 유지 | 아지로다이트 0 · 도펀트 계열 0 · ΔV/V 수치 0 (§7-3 · §7-6) |
| 문헌 갭 'SE 도펀트를 산물 물성으로 순위' (cascade) | 갭 유지 | 산물 물성 점수 0 · 산물 이름도 없다 (§7-4) |
| 보고서 문장 '최근 HT 계면 스크린은 부피를 다루지 않는다' | 고쳐야 함 | K_crit (ε_RXN 포함) 가 8 만 점 스크린의 목표값 (§7 판정 ①) |
| A 의 'SEI 설계' 문구 | 선점 (문구) | 논문 제목. 뜻은 '기계적 준안정' 이라 다르다 (§7 판정 ②) |
| cascade 산화 안정성 축 후보 ④ '기계적으로 묶인 안정창' (`kb/open_items.md` 의 후보 목록) | 정의 제공 | K_crit(φ) 는 그 축의 다른 읽기다. 도펀트로 넓힐 때 보고량 후보 (§12-①) |
| 구속 ESW 원장 (ESW · 1저자 = 사용자) | 같은 틀 · 다른 계 | 식은 같은 계열 (Fitzhugh 섭동). 이 논문은 계면 유사상 · 고정 전압, 우리는 호스트 자기분해 · 가장자리 |
| Nd 계면 (CEI · 1저자 = 실험 쪽 · 사용자 = 계산 담당) | 무관 | `Fig. 3b` 의 Nd +0.41 (figure-read) 은 코팅 2 만 종 전체의 상관이다. Nd 서사의 근거로도 반박으로도 쓰지 않는다 |
| B₂O₃ (b2o3 · 원고 1저자 아님) | 무관 | B +0.34 · O −0.13 (figure-read) 도 같은 이유로 옮기지 않는다 |
| 작동창 2.5–4.25 V 규칙 | 범위 밖 주의 | 논문은 2 · 3 · 4 V 세 점. K_crit 는 전압과 함께 커지고 4.25 V 값은 없다 — 외삽하지 않는다 |

### 11.3 관측창 · 홉 수 검산

해당 없음 — 이 논문에는 MD 도 장벽 (Ea) 도 없다. 열역학 (0 K 상 자료) 과 CV 뿐이다.

### 11.4 litdb 의 관련 digest 와 엮기

| digest | 이 논문과의 관계 |
|---|---|
| `gilgonzalez2022_synergistic_cl_constricted_esw` | 같은 그룹 · 같은 틀의 후속. 거기는 SE 자기분해 창 (K_eff 0 / 10 / 20 GPa 에서의 가장자리) · Cl 함량 계열 — **치환체로 분해 부피를 해상한 유일한 계열**이라는 보고서 서술은 이 편을 읽은 뒤에도 그대로다 |
| `wang2022_two_parameter_space_dendrite_constriction` (목록 120) | 같은 그룹의 Li 금속 쪽 판 (E_hull, K\*). 이 편의 K_crit 가 그쪽 K\* 의 전신으로 보인다 — 정의 대조는 그 digest 에서 |
| `fitzhugh2019_ht_functionally_stable_interfaces_sulfide` (목록 122) | 이 논문 ref 9. 유사상 binary-search 를 거기서 가져왔다 |
| `tian2020_electrochemo_mechanical_stress_assb` (목록 123) | 분해 부피 → **응력** (손상 쪽). 이 편은 같은 부피를 **안정화 문턱**으로 쓴다 — 같은 양의 정반대 읽기 (보고서 B 의 셋째 빈칸) |
| `zhu2016_first_principles_interface_stability_assb` (목록 124) · `richards2016_interface_stability_pseudobinary` · `nolan2018_computation_accelerated_design_review` | 이 논문 refs 10 · 16 계열 — 유사 이원 계면 열역학의 원전. 이 편은 그 위에 압력 항 하나를 얹었다 |
| `wang2026_interface_stability_kinetics_sulfide_assb` | 계면 ΔV/V 를 지도화했지만 구속 항은 없다. 이 편은 구속 항이 있지만 ΔV/V 를 안 보인다 — 서로의 빈칸 |
| `park2026_ml_framework_stable_interfaces_assb` | ref 25 로 인용. 그 논문이 못 잡는다고 적은 *"strain and volume-change effects"* 를 다루는 편이 이것이다 |
| `wang2025_ai_ecosystems_electrolyte_interface_ssb` | 리뷰가 이 논문을 ref 136 으로 요약 — 그 digest §10f 의 '랜덤포레스트' 는 원전에서는 Extremely Randomized Trees 이고 나무 수는 50 과 30 이 섞여 있다 |
| `sundar2025_oxide_coating_screening_lpscl` | 코팅을 **산물의 이온 · 전자 전도**로 거른 편. 이 편은 같은 '코팅 스크린' 이지만 점수가 K_crit 하나다 |

---

## 12. 적용 인사이트 (제안 — 원장 · 보고서는 고치지 않았다)

- **① K_crit(φ) 를 도펀트 표의 한 열로 쓸 수 있다.** 보고서 B-④ 의 '역학 환산' 에서 가장 가까운 결합으로 인용하려던 K_eff · K\* 의 계면판 정의가 식 (3) 이다. 같은 반응식에서 |ΔΩ(φ)| 와 ΔV 가 나오면 K_crit = |ΔΩ|/ΔV 는 나눗셈 한 번이다. 다만 회계 (Li 저장소 · 기체 · 정규화) 를 결과 전에 선언해야 한다 — 이 논문은 그것을 안 했다.
- **② ΔG · ΔV · K_crit 를 따로 싣는다.** K_crit 하나만 내면 화학 항과 부피 항이 섞인다. 이 논문의 child 는 대부분 화학 항으로 내려갔는데 '기계적 설계' 로 불렸다 (§6.3).
- **③ ε_RXN ≤ 0 규칙을 결과 전에 정한다.** 수축 분해에서는 K_crit 가 정의되지 않는다. 그 칸은 '구속 무효 · 접촉 손실 쪽' 으로 따로 분류해야 하고, 그것이 보고서가 꼽은 B 의 가장 단단한 자리 (양극 쪽 수축) 다. 우리 원장의 개시 반응 부호가 조성에 따라 갈린다는 점과 맞물린다.
- **④ 조성 '설계' 는 만들 수 있는 조성 안에서.** 전구체 혼합으로 닿는 조성만 후보로 두면 §6.7 의 문제가 생기지 않는다. 우리 cascade 설계는 전구체 기반이라 이 조건을 이미 지킨다 — 유지한다.
- **⑤ 대리모형에 대고 최적화하지 않는다 — 한다면 직접 계산으로 되짚는다.** 조성만 넣는 나무 모형은 계단 함수라, 최적화가 분기 문턱 (F ≈ 0.096) 을 넘는 쪽으로 가고 미량의 Pb · Sb · K · H 같은 답을 낸다. 이 논문은 child 의 K_crit 를 구속 앙상블로 직접 계산해 확인한 적이 없다.
- **⑥ 실험 쪽에 제안할 대조 셀 꼴.** SE + 탄소 복합 '양극' 의 느린 CV (0.1 mV/s) 로 SE 분해 전류를 재는 방식은 그대로 쓸 만하다. 이 논문에서 빠진 것 = **'유리 + 탄소 (LGPS 없음)' 대조** · 반복 셀 · 실제 합성 조성 · 압력을 바꾼 계열. 넷이 있어야 프리피크의 귀속과 구속의 효과를 가를 수 있다.
- **⑦ 부피 회계의 원전은 refs 11–13 이다.** Li 를 부피에 세는지 · 휘발성 산물을 어떻게 두는지는 Fitzhugh *J. Mater. Chem. A* 7, 23604 (2019) · Wu *Nat. Commun.* 9, 4037 (2018) · Fitzhugh *Small* 15, 1901470 (2019) 본문에 있을 것이다 (litdb 미보유). 보고서 B-② '회계 행렬' 을 쓰려면 그 셋 중 하나는 본문으로 열어야 한다.

---

## 13. 인용 가능 문장 (deck/paper 용 · 영문 초안)

- "Fitzhugh *et al.* defined a critical effective modulus, *K*<sub>crit</sub>, above which the interphase between a sulfide electrolyte and a coating no longer decomposes at a given voltage, and screened it over more than 80 000 pseudo-binary interfaces." — *Energy Environ. Sci.*, 14, 4574 (2021).
- "That screen varied the coating composition against four fixed thiophosphate electrolytes and evaluated the cathode-side voltage only; it reported neither reaction strains nor decomposition products, and it did not include argyrodites." — 같은 출처 (우리 판독 · §7).
- "The same authors noted that oxygen-, fluorine-, and chlorine-rich interphases have a lower *K*<sub>crit</sub> because they are less prone to delithiation in the voltage range considered." — 같은 출처 p. 4578.

**쓰면 안 되는 것 (⛔ 인용 금지 목록)**

- 인용 금지 ① — `Fig. 3b` 의 원소 부호 (F · O · Cl 음 · Nd · B · Sb · Cu 양) 를 **아지로다이트 도펀트의 순위**로. 코팅 물질 2 만 종 전체의 상관이고 숫자도 논문에 없다.
- 인용 금지 ② — child 조성 (`Table S1` · `Table S2`) 을 '실험으로 검증된 조성' 으로. 합성된 조성은 적혀 있지 않고, 표의 조성 다수는 적힌 전구체로 만들 수 없다 (§6.7).
- 인용 금지 ③ — 'K_eff ≈ 4.6–4.9 GPa' 를 측정값으로. 대리모형 예측 두 묶음 사이의 틈 (0.3 GPa) 이고 모형 RMSE 가 2.59 GPa 다.
- 인용 금지 ④ — `Table S1` 의 유리 전도도와 그 출처 번호. 번호가 조성과 어긋난다 (§16-6).
- 인용 금지 ⑤ — '조성 수정으로 계면 분해가 줄었음이 실험으로 확인됐다' 를 단서 없이. 셀 하나씩 · 프리피크 귀속은 소거법 · 강한 구속 (250 MPa) 에서만 (§14-5).
- 인용 금지 ⑥ — 이 digest 의 ε_RXN·V⁰ 역산값 (§6.2) 을 논문 값으로. 우리 산술이다.

---

## 14. 비판 — 주의 / 한계 (over-claim 방지)

1. **우리 계가 아니다.** 아지로다이트 계산 0 · SE 는 네 종으로 고정 · 바꾼 것은 코팅 (유리) 조성 · 전압은 양극 쪽만. '황화물 SE 의 SEI 설계' 라는 제목에서 기대하는 것보다 범위가 좁다.
2. **설계값은 전부 대리모형 값이고 직접 계산으로 되짚지 않았다.** parent 의 K_crit (16.07 등) 조차 *"from our prediction"* 이다. 유리 조성은 hull 로 바로 계산할 수 있는데도 child 의 K_crit 를 구속 앙상블로 확인한 값이 하나도 없다. 모형 정확도도 LSPS · 4 V 한 경우만 보고했다 — LGPS · 2 V · 3 V · 자기분해 3.5 V 모형의 오차는 모른다.
3. **대리모형 자체가 불투명하다.** (가) 25 GPa 아래로 잘린 자료로 학습한 것으로 보이는데 본문에 없다 (§6.6) (나) 나무 수 50 ↔ 30 (다) 학습 · 시험 분할 불명 — 10,000 + 10,000 이 그 범위의 자료 수를 넘는다 (라) `Fig. 4b` 의 대각선 위 가는 선은, 조성만 특징으로 쓰는 모형에서 **같은 조성 (다형체) 이 학습과 시험에 나뉘어 들어갔을 때** 나오는 모양이다 (우리 추론) — 그렇다면 처음 보는 조성에 대한 오차는 2.59 GPa 보다 크다 (마) 입력이 무엇인지 문장과 그림이 어긋난다: 본문은 자료 한 점이 *"the initial SEI composition"* 이라 하는데, `Fig. S3` 에는 Li ≤ 0.001 로 992 / 269 가 갈리는 분기가 있다 — Li 가 40 at% 인 SE 가 섞인 유사상 조성이라면 나오기 어렵다. 입력은 **코팅 물질의 조성**으로 읽는 편이 그림과 맞는다.
4. **child 의 큰 하락은 나무의 계단에서 온 것으로 보인다.** Child B 는 F 를 0.07–0.105 로 올리는데 그것이 뿌리 분기 문턱 (F ≤ 0.096 · 왼쪽 평균 15.2 · 오른쪽 8.7 GPa) 에 걸친다. 10 % 제약의 상한이 문턱과 겹친 결과다. Child C 의 2 GPa 안팎은 'Li 가 든 불화물' 가지의 잎 값 (2.2–4.1 GPa) 그대로다 (공개된 나무 한 그루 기준 · 우리 추론). Pb · Sb · Bi · K · Zn · Ti · Ni · H · C · N 같은 미량 첨가도 같은 종류의 산물이다.
5. **실험이 예측을 시험하지 못한다.** (가) 합성 조성이 예측 조성과 같을 수 없다 (§6.7) 그리고 실제 조성이 없다 (나) 셀 하나씩 · 오차막대 없음 — parent 의 넓은 봉우리가 `Fig. 5d` 에서 28.8 µA, `Fig. S5` 에서 22.9 µA 다. 두 그림이 같은 조건이라면 (`Fig. S5` 의 주사 속도는 적혀 있지 않다) 셀 간 편차가 20 % 로, C4 · C5 · C6 사이의 차와 같은 크기다 (다) 비교 대상이 열역학 구동력 (eV/atom) 과 봉우리 전류 (µA) 다 — 둘을 잇는 모형이 없다 (라) **'유리 + 탄소 (LGPS 없음)' 대조가 없다.** 프리피크를 유리/LGPS 계면에 돌린 근거는 소거법뿐이다. LiI 가 든 유리이므로 요오드화물 산화 같은 유리 자체의 반응일 가능성을 배제하지 않았다 (우리 의견 · 논문 밖 일반 지식에 기댄 가설 · 미검증) (마) LGPS + C 대조는 탄소가 절반 (0.05 mg ↔ 0.10 mg) 이고 배경 (약 8 µA) 을 빼지 않았다 (바) 저자도 인정하듯 강한 구속 (250 MPa) 에서만 쟀다 — 설계가 이득을 내야 할 약한 구속 조건의 자료가 없다.
6. **'첫 충전 뒤 K_eff 가 K_crit 을 넘었다' 는 유일한 설명이 아니다.** 탄소 복합체에서 황화물 SE 의 분해 전류가 첫 사이클 뒤 사라지는 것은, 탄소와 닿은 SE 가 소진되거나 절연성 산물이 전자 경로를 막아도 일어난다. 둘을 가르는 실험 (압력을 바꾼 계열 등) 이 없다.
7. **K_eff ≈ 4.6–4.9 GPa 는 정밀도가 없다.** 틈 0.3 GPa 는 모형 RMSE 의 1/9 이다. 여섯 셀의 K_eff 가 같다는 가정이 들어가고, 그 가정대로면 개시 전압이 0.8–0.9 V 올라가야 하는데 측정은 0.2 V 내려간다 (§6.5).
8. **부피 쪽이 비어 있다.** ε_RXN · V⁰ · 산물 목록이 어느 계에도 없다. Li 부피 · 기체 · ε ≤ 0 의 처리도 없다 (§4.4). 4 V 의 산화 산물은 분자성 고체일 텐데 그 PBE 부피가 과대하면 ε_RXN 이 커지고 K_crit 는 작게 나온다 (방향만 · 우리 추정 · 논문은 범함수도 적지 않았다). 유리를 바닥상태 결정상 조합으로 대신한 것도 부피 쪽 오차원이다.
9. **원소 서술이 그림보다 세고, 두 그림이 서로 어긋난다.** 본문은 Mo · Br 을 이로운 쪽에 넣지만 `Fig. 3b` 값은 0 에 가깝다. *"in good agreement"* 라던 SHAP 와 상관 지도는 I (지도 +0.41 ↔ `Fig. 4c` 에서는 내리는 쪽 막대) 와 Sb (지도 +0.56 ↔ 최적화가 child B 6 행에 Sb 를 **넣는다**) 에서 반대다. 단일 호스트 경로에서는 O 가 F 보다 훨씬 세다 (−2.88 ↔ −0.53 GPa) — 전체 상관 (F −0.58 ≫ O −0.13) 과 순서가 다르다.
10. **설계가 4 V 위에서는 통하지 않는다.** `Fig. S5` 에서 2–4 사이클의 5 V 근처 전류는 C6 가 parent 보다 20–28 % 크다 (figure-read). 논문 주장은 '4 V 아래' 로 한정돼 있어 모순은 아니지만, 초록의 *"electrochemically passivate based on our predictions"* 를 넓게 읽으면 안 된다.
11. **열역학 극한이다.** 산물은 0 K hull 상이다. 실제 계면의 동역학 산물 · 비정질 중간체 · 전자 접촉 조건은 들어 있지 않다. '전자 절연체' 선별 기준도 없다. 유리 자기분해 K_crit 가 수정 뒤 높아지는 것 (§5.7) 처럼, 한 지표를 내리면 다른 지표가 오르는 것도 다루지 않았다.
12. **조성 수정의 대가를 재지 않았다.** 전도도 · 유리 형성능 · 상 순도 어느 것도 측정하지 않았다. 알고리즘이 가는 방향 (Li 를 빼고 O · F 를 넣는다) 은 Li⁺ 전도에 불리한 방향이다.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (이 논문에서) |
|---|---|
| pTφ 앙상블 ('비구속') | 압력 · 온도 · 전압이 상태 변수인 액체 셀의 열역학. 등압이라 분해가 부피 벌을 받지 않는다 |
| 구속 앙상블 (constrained ensemble) | 압력이 상태 변수가 아니라 국소 상 분율의 함수 p({x}) 인 고체 셀의 열역학. 분해 자리에만 압력이 생긴다 |
| 반응 변형률 ε_RXN | 분해 산물과 원래 물질의 부피 차를 원래 부피로 나눈 것. 응력 때문이 아니라 분해 자체가 만드는 변형 (stress-free) |
| K_eff | 국소 유효 탄성률. 분해 자리가 주변에서 받는 되누름의 세기 (p = K_eff·ε_RXN). 재료 탄성률 · 공극 · 접촉 · 외부 압력이 함께 정하는 유효값 |
| K_crit | 분해의 구동 에너지를 정확히 상쇄하는 K_eff (식 3). K_eff > K_crit 이면 분해가 멈춘다. 낮을수록 약한 구속에서도 안정 |
| 유사상 (pseudo-phase) | 두 물질을 비율 x_m (구동력 최대) 로 섞은 가상의 한 상. 계면을 한 조성 · 한 에너지로 다루기 위한 장치 |
| 유사 이원계 (pseudo-binary) | 두 물질의 조성을 잇는 선 위에서 보는 상평형. 닫힌계 (Li 고정) 와 열린계 (μ_Li 고정) 두 판이 있다 |
| grand potential 상도 | Li 화학 퍼텐셜을 전압으로 고정한 열린계의 상평형. 여기서 분해 에너지와 산물을 얻는다 |
| 초기 SEI · 2차 SEI | 조립 때 닫힌계 반응으로 생긴 계면상 · 사이클 중 Li 가 드나들며 그것이 다시 분해해 생긴 계면상 |
| SEI 성장 / 유지 | K_eff < K_crit 이라 사이클마다 더 분해 / K_eff > K_crit 이라 초기 SEI 가 그대로 |
| Extremely Randomized Trees | 분기 문턱을 무작위로 뽑아 그중 좋은 것을 쓰는 결정트리 앙상블. 예측은 구간별 상수 (계단) 다 |
| SHAP | 예측값을 특징별 기여로 나누는 게임이론 기반 귀속. 여기서는 '어느 원소가 K_crit 를 올리나' 를 골라 그 원소부터 고친다 |
| child A · B · C | parent 유리에서 원소별 변화를 0.05 · 0.10 · 무제한으로 허용해 얻은 최적화 조성 |
| H_L · H_R | CV 첫 충전의 프리피크 (3 V 근처) 높이 · 넓은 봉우리 (3.5 V 근처) 높이 |

---

## 16. 본문 · ESI 의 오기 · 불일치 목록

1. Child A 의 요오드: 본문 (p. 4580) *Li₀.₃₂₄P₀.₀₉₈S₀.₃₄₆I₀.₁₃₈Cl₀.₀₂₆F₀.₀₄₂O₀.₀₄₀* (합 1.014) ↔ `Table S1` I 0.123 (합 0.999) ↔ `Fig. 4c` I = 0.1227. 본문이 parent 값을 잘못 옮겼다.
2. 나무 수: 본문 · `Fig. 2` · `Fig. S3` 캡션 50 ↔ Methods 30.
3. 약어 LPS 가 Li₃PS₄ (p. 4575) 와 Li₇P₃S₁₁ (p. 4577–) 둘 다에 쓰인다.
4. *"The diameter of the cathode film is 0.49 cm²"* — 넓이 단위다.
5. `Table S2` 의 두 칸은 조성 합이 1 이 아니다: 4 행 child B (0.982) · 6 행 child C (0.980 — 이웃 행에 있는 P ≈ 0.02 가 빠진 것으로 보인다).
6. `Table S1` · `Table S2` 의 전도도 출처 번호가 조성과 어긋난다 (ESI 참고문헌 제목 기준): 2 행 Li–B–S–I 유리 ↔ [2] 'Li₃PO₄–Li₂S–SiS₂' · 5 행 Li–Ge–S ↔ [5,6] 실리콘 황화물 유리 · 8 행 Li–Si–S–Cl ↔ [8] 'Li₂S–P₂S₅' · 9 행 Li–Si–S–O ↔ [1] 'Li₂S–P₂S₅–LiI' · 10 행 ↔ [9] 기계 물성 논문. 1 행만 분명히 맞는다.
7. 범위 서술이 표보다 좁다: 본문 *"15–17 / 10–13 / 6–9 / 1.5–2 GPa"* ↔ 표 13.57–17.74 / 10.47–12.45 / 5.46–9.49 / 1.56–2.27.
8. *"composition modification larger than 2.5 %"* — 그림에서는 2.5 % 부터 0 이다 (K_crit 9.07 < 10 GPa).
9. 프리피크 *"at 3 V"* · *"around 3 V"* — 판독은 2.64–2.85 V 다.
10. '5 % 제약' 의 실제 최대 변화는 0.109 (Li · `Table S1` 9 행) 까지, '10 %' 는 0.184 (S · `Table S2` 9 행) 까지 간다 — 캡션의 *"slightly exceeding"* 보다 크다.
11. `Fig. 3b` 와 `Fig. 4c` 의 색 뜻이 반대다 (3b 빨강 = K_crit 낮춤 · 4c 빨강 = K_crit 높임).

---

## 🗨️ Q&A 로그

(아직 없음 — 질문이 오면 날짜 · 질문 · 답 · 본 그림을 여기에 쌓는다.)
