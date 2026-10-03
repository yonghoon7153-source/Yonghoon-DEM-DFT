<!-- digest 초판 2026-10-03 (논문 에이전트 · 심층판 — 사용자 지정 "우리 연구와 맞닿아 있어 더 자세하게" · 대피 세션 claude/evac-2026-10-02 에서 작성, 커밋은 부모 세션).
     ① 그림 15장 전부 실독. 판독이 본문과 갈리는 4곳은 PDF 를 다시 렌더해 확대 확인했다 (Fig. 4f 400 dpi · Fig. 9b 500 dpi · Fig. 13a 600 dpi · Fig. 13e 500 dpi).
     ② Table 1 은 pp.33–35 세 쪽 표인데 도구가 p.34·35 를 '중복(작은 쪽)' 으로 버렸다 → tab_1b.png·tab_1c.png 를 t1 과 같은 규격(전면 bbox · 274 dpi · 90° 세움)으로
        손 렌더해 figures.json 에 manual_crop 사유와 함께 넣었다. 표 값은 세 쪽 모두 PDF 텍스트로 전사했다 (§4).
     ③ 참고문헌 237편을 파싱해 우리가 이미 digest 한 원전 15편과 DOI·서지로 대조했다 — 인용 역할 불일치 다수 (§12a).
     ④ 우리 쪽 값은 canonical_registry → citation_hazards → decisions 순으로 확인한 것만 썼다. MD σ·D·Ea 는 절대값을 한 번도 쓰지 않았다 (1저자 인용정책 2026-09-18).
     ⑤ 리뷰의 모든 수치는 2차 인용이다 — 본문에서 (2차 · ref N) 로 표시했고, 원전을 우리가 digest 했으면 slug 를 달았다.
     ⑥ talk 인입 대기열 점검: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → lee2026_skku_mlip_materials_design.md 한 파일뿐이고 이 논문은 없다 (talks 전체 검색 0건). 역링크 없음. -->

# Anion Engineering of Sulfide Solid Electrolytes: From Fundamentals to High-Performance All-Solid-State Batteries — Nosrati et al. (*Small* 2026, e76005)

> slug `nosrati2026_anion_engineering_sulfide_se_review` · DOI `10.1002/smll.76005` (PDF 꼬리말 인쇄 · Small 0.0:e76005) · type `리뷰 (자체 계산 0 · 자체 실험 0 — 전량 2차 인용)` · PDF `litdb/inbox/Nosrati 2026 - Anion engineering of sulfide solid electrolytes (Small e76005).pdf` (46 pp = 본문 pp.1–39 + 참고문헌 237편 pp.39–46 · 그림 15 · 표 1(pp.33–35 세 쪽) · **SI 없음**) · digested `2026-10-03` · status ✅ · 태그 **[외부]**

> elements: Li, P, S, Cl, Br, I, O, F, Ge, Si, Sn, Sb, Bi, Al, As, Ag, B, Mn, Ni, Co
> methods: DFT, AIMD, MD, MLIP, PDOS, ESW, XPS, Raman, elastic

> **저자**: **Ali Nosrati** · Osman Goni Shovon · S. M. Shaikhul Islam · **Junjie Niu\*** (Department of Materials Science and Engineering, CEAS, **University of Wisconsin–Milwaukee**) · 접수 2026-08-02 · 개정 2026-08-30 · 수락 2026-09-22 · © Wiley-VCH (OA 아님 · Hanyang 기관 접근) · 자금 UWM Ignite Grant FY26-106-068000-4 + UWM DIG · 기여: A.N. 집필 · J.N. 수정 · 이해상충 없음 · 자기인용 3편(refs 11·12·14 — 서론 일반 문장용).
>
> **계보·위치**: 같은 그룹의 리뷰 연작(Li 금속 표면개질 · micro-Si 음극 · NMC 원소 튜닝, 모두 2026)의 황화물 SE 편. **원자단위 계산 그룹이 아니다** — 계산 결과는 전부 남의 그림을 재수록한 것이다.
>
> **관련 digest (리뷰가 인용한 원전 · 우리가 이미 읽음)**: `kraft2017_lattice_polarizability_argyrodite_Li6PS5X`(ref 137) · `adeli2019_halide_substitution_boosting_argyrodite`(ref 135) · `morgan2021_anion_disorder_superionic_mechanism_li6ps5x`(ref 92) · `gilgonzalez2022_synergistic_cl_constricted_esw`(ref 206) · `lu2025_tailoring_cl_rich_anode_licl`(ref 164) · `liu2024_pband_center_sbo_dual_interface`(ref 172) · `ma2024_sb_doping_lpsc_conductivity`(ref 208) · `banik2022_substitutions_oxidative_stability_argyrodite`(ref 197) · `ong2013_lgps_family_substitution`(ref 147) · `deng2016_elastic_superionic_electrolytes_dft`(ref 191) · `sakuda2013_sulfide_mechanical_property`(ref 173) · `rao2011_argyrodite_se_studies_bvse`(ref 160) · `famprikis2019_fundamentals_inorganic_sse`(ref 25) · `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`(ref 153) · `richards2016_interface_stability_pseudobinary`(ref 58) · `okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces`(ref 64).
> **관련 digest (리뷰가 인용 안 함 · 우리 대조에 필요)**: `zuo2022_chlorination_cathode_interface` · `zhu2015_esw_grand_potential_origin` · `schwietert2020_redox_activity_vs_electrochemical_stability` · `schwietert2021_intrinsic_vs_decomposition_window_sse` · `ohno2020_interlab_ionic_conductivity_argyrodite` · `zhao2021_hecs_descriptors_argyrodite_activation_energy` · `zhu2020_air_stable_se_design_principles` · `kim2026_moisture_surface_degradation_lpscl_dryroom` · `hyun_han_argyrodite_moisture_degradation_design_principles` · `jang2023_zno_cosubstitution_argyrodite` · `xu2026_ndo_codoping_argyrodite` · `wang2025_electronic_localization_yo_argyrodite` · `yang2025_lao_dualdoping_argyrodite_lacl3` · `wang2025_pretrained_deep_potential_sulfide_sse` · `he2023_halogen_chemistry_solid_electrolytes` · `wu2026_ta_argyrodite_selfpassivating` · `zhou2026_high_entropy_lgps_multicationic` · `ziemke2026_li3ocl_substitutional_defects`.

> **본 digest 에서 실제로 본 그림 (2026-10-03)**: `Fig. 1`–`Fig. 15` — **15장 전부**. 판독이 본문과 어긋나 보여 PDF 를 다시 렌더해 확대 확인한 곳 4군데: `Fig. 4f`(400 dpi) · `Fig. 9b`(500 dpi) · `Fig. 13a`(600 dpi) · `Fig. 13e`(500 dpi).
> `Table 1` 은 세 쪽 모두 **PDF 텍스트로 전사**했다(이미지 판독 아님). 이미지는 `tab_1c.png`(p.35)만 방향·크롭 확인용으로 봤고 `tab_1.png`·`tab_1b.png` 는 이미지로 안 봤다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문에 없는 계산은 **(우리 산수)** 로 표시했다.

---

## 0. 이 digest 를 읽는 법 — 왜 우리 연구의 정면인가

우리 계산 캠페인은 처음부터 **음이온 부격자를 바꾸는 연구**였다. 이 리뷰의 분류(`Fig. 1` 의 "Anion engineering strategies" 네 칸)로 다시 적으면 이렇다.

| 리뷰의 전략 칸 | 우리 계 | 우리가 실제로 바꾼 것 |
|---|---|---|
| **Halide substitution** (할라이드 함량·종류) | comp1 = `Li₆PS₅Cl` → **modelc = `Li₅.₄PS₄.₄Cl₁.₆`** (Cl-rich) · comp2 = `Li₆PS₅Cl₀.₅Br₀.₅` | Cl 함량(=Li 공공 + 4a/4d 혼합) · Br 반 치환 |
| **Oxygen substitution** | **LPSOCl** = O 치환 modelc (`Li₂₇P₅S₂₁OCl₈`, 62원자 · O 는 PS₄ 안 S 자리 → `PS₃O`, P–O 1.559 Å) | 음이온 1개를 O 로 |
| **Dual anion–cation doping** | **+B₂O₃** (B + O, 128원자) · **Nd 도핑** (Nd@Li / Nd@P — **양이온** 축) | O 와 양이온을 같이 |
| Multi-anion frameworks | 없음 (comp2 가 가장 가깝다) | — |

리뷰의 결론은 한 줄이다 — *"음이온 부격자는 수송·밴드엣지·안정성·기계를 **동시에** 쥐는 레버이고, 단일 치환은 한 성질만 올리고 다른 데서 값을 치르며, 공도핑·다음이온은 그 대가를 **기능별로 분리**해서 이긴다."* (p.32, §6.1)

이 digest 의 목적은 그 명제들을 **우리 축(A 이온전도 · B 산화 4축 · C 기계 · D 전자구조 · E 환원 · F 도핑)에 하나씩 걸어서** "맞는 곳 / 어긋나는 곳 / 방법 의존이라 판정 불가인 곳" 을 가르는 것이다. 미리 결론을 당겨 쓰면:

| 리뷰 명제 | 우리 판정 (상세 §9 · §11) |
|---|---|
| Cl-rich(Li 결손) → Li 공공·무질서 → 수송↑ | ✅ **방향 일치** — 단 우리 쪽은 단일 시드라 *방향*까지만 (수치 순위 금지) |
| 할라이드·O 치환 → **VBM 하강 → 산화안정↑ (4.8 V 이상)** | 🔴 **B①(열역학 onset)에서는 성립 안 함** — comp1 = modelc 2.256 V, VBM 은 셋 다 S 3p. 리뷰는 축 이름을 한 번도 안 붙인다 |
| Cl 산물이 기계 구속으로 창을 넓힌다 (GG) | ✅ **B② 에서 방향 일치** (우리 `constrained_esw.py` 경향 재현 — 기존 판정) |
| P–O 결합 → 격자 강성↑ | ✅ **방향 일치** — LPSOCl B₀·E_VRH 가 modelc 보다 크다 (§9c) |
| 크고 분극 큰 음이온 → E↓ | ✅ **방향 일치** — comp2(Br) 가 comp1 보다 무르다. 그러나 **Cl-rich 는 이 규칙 밖** (E_VRH↑ · B₀↓) |
| O 치환 → σ 손해 | ⛔ **우리 데이터로 판정 불가** (원장이 LPSOCl↔modelc 차를 O 효과로 읽는 것을 금지) — 문헌은 리뷰와 같은 방향 |
| 할라이드 도입 → P–S 공유성↓ | 🔴 **우리 ICOHP 에서 안 보인다** — Cl-rich 에서 P–S 가 오히려 1 % 강하다 |

⚠ **세 가지를 먼저 박아 둔다.**
1. **이 리뷰의 숫자는 전부 남의 숫자다.** 측정 온도·합성·압력이 다른 값을 한 표(`Table 1`)에 섞었다. 우리 값 옆에 놓지 않는다.
2. **"산화안정성" 문장에 축이 없다.** p.18 의 *"above 4.8 V"* 와 p.24 의 *"thermodynamically stable only up to ≈1.6–2.3 V"* 가 같은 리뷰 안에 있다. 우리 규율(§B 4축)로 갈라 읽어야 한다.
3. **`Table 1` 2행이 정확히 우리 modelc 조성이다** — `Li₅.₄PS₄.₄Cl₁.₆` 20.2 mS cm⁻¹ · 0.407 eV (2차 · ref 228). 그런데 같은 명목 조성을 Adeli 2019 는 **3.3 mS cm⁻¹ (LiCl 석출)** 로 보고했고(`adeli2019` digest), 이 행의 σ–Ea 쌍은 홉 수 검산과 **차수에서 모순**이다 (§4c). 우리 모형의 실험 앵커로 쓰기 전에 원전부터 본다.

---

## 1. 한 줄 요약

황화물 고체전해질(유리·유리세라믹 / 아지로다이트 / thio-LISICON / LGPS)에서 **음이온 부격자 공학**(할라이드·O 치환, 무질서·공공 제어, 다음이온 골격, 음이온–양이온 공도핑)이 이온전도·전기화학 안정성·계면·기계·결함화학을 어떻게 바꾸는지 정리한 46쪽 리뷰. 핵심 주장은 **"단일 음이온 치환은 한 성질의 최적점과 다른 성질의 손해를 함께 만들고, 기능을 서로 다른 음이온/도펀트에 나눠 맡기는 공도핑·다음이온 설계가 그 손해를 피한다"**. 계산·실험을 스스로 하지 않았고, 수치·그림은 전부 재수록이다. Kraft 2017 의 전지수(σ₀) 경고를 정확히 소개하면서도 결론부에서는 "분극률 → Ea↓" 를 일반화하고, 산화안정성을 **밴드엣지(VBM) 정렬**로만 설명해 열역학 분해창 연구(Zhu 2015 · Schwietert 2020)와 엇갈린다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 형식 | Small 리뷰 · 본문 6절 (1 서론 · 2 구조 계열 · 3 수송 기전 · 4 음이온 부격자의 역할(4.1 무질서 · 4.2 수송·Ea · 4.3 계면 · 4.4 기계 · 4.5 결함화학) · 5 치환과 전기화학 성능 · 6 결론(6.1 통찰·트레이드오프 · 6.2 과제·로드맵)) |
| 리뷰의 정의 (p.2) | 음이온 공학 = ① 직접 음이온 치환(S²⁻ → 할라이드·O) ② 음이온 공공·무질서 조절 ③ 다음이온 골격(옥시설파이드·혼합할라이드) ④ 음이온 + 양이온 공도핑. **"전통적 도핑의 재명명이 아니다"** — 음이온 부격자의 **집단적 성질**(분극률·무질서·전기음성도)을 기능 단위로 본다는 주장 |
| 던지는 질문 | 음이온 부격자가 Li 수송·밴드엣지·계면·기계를 어떻게 동시에 정하나 · 어떤 전략이 트레이드오프를 푸나 · 상용화 로드맵 |
| 자기 범위 선언 (p.7) | *"aliovalent cation substitution … leaves the anionic (S²⁻) framework unchanged and is therefore not discussed further"* — ⚠ 그런데 `Table 1` 13행 중 6행이 음이온을 안 바꾼다 (§4b) |
| 계산 | **0** (재수록만). 범함수·코드·k점·셀·AIMD 길이 **전문 0회** (§6) |
| 참고문헌 | 237편 · 연도 분포 2022–2024 가 정점 (25 · 22 · 32편) · 2026 8편 |

---

## 3. 핵심 수치 총정리 (전부 2차 인용 · 우리 값과 섞지 않는다)

> 표기: `(2차 · ref N)`. 원전을 우리가 digest 했으면 slug. 리뷰가 측정 온도를 안 적은 곳은 "T 미기재".

### 3a. 계열별 이온전도 (실온, 리뷰 본문)

| 물질 | σ (mS cm⁻¹) | Ea (eV) | 출처 |
|---|---|---|---|
| 70Li₂S–30P₂S₅ 유리세라믹 (열처리) | ≈3.2 | — | 2차 · ref 67 |
| 75Li₂S–25P₂S₅ | 0.28 | — | 2차 · ref 75 |
| Li₂S–P₂S₅ 유리세라믹 (최적 열처리) | **17** | 0.18 (`Table 1`) | 2차 · ref 76 (Seino 2014) |
| Li₇P₃S₁₁ | >3 | — | 2차 |
| β-Li₃PS₄ | 0.1–1 | — | 2차 · refs 75, 78 |
| Li₂P₂S₆ (C2/m) | **7.8×10⁻⁸** | ≈0.48 | 2차 · ref 59 (Dietrich 2017) |
| Li₆PS₅Cl | ≈1.5 | — | 2차 (출처 번호 없음) |
| Li₅.₃PS₄.₃Cl₁.₇ | 6.6 | — | 2차 · ref 95 |
| Li₆PS₅I | **4.6×10⁻⁴** | — | 2차 · refs 92, 96 |
| Li₄GeS₄ / Li₄SnS₄ | 2×10⁻⁴ / 9.4×10⁻⁴ (p.7) — ⚠ 같은 Li₄SnS₄ 를 p.8 에선 ≈7×10⁻² | — | 2차 · refs 106, 107 |
| Li₄.₀₂₅Sn₀.₉₇₅Bi₀.₀₂₅S₄ | 0.135 | — | 2차 · ref 123 |
| As³⁺/Sb³⁺-Li₄SnS₄ | 0.139 | ≈0.21 | 2차 · ref 101 |
| 0.5Li₄SnS₄–2.5Li₃PS₄ | ≈2 | — | 2차 · ref 124 |
| 0.37LiI–0.25Li₃PS₄–0.38Li₄SnS₄ | 0.55 | — | 2차 · ref 125 |
| LGPS (Kamaya 2011) | ~10 대 (`Fig. 15`: ≈12) | — | 2차 · ref 73 |
| Li₁₀SnP₂S₁₂ | ≈4 | — | 2차 · refs 119, 120 |
| Li₁₀SiP₂S₁₂ (고압 합성) | 2.3 | — | 2차 · ref 121 |
| Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ (LGPS형) | **25** | — | 2차 · ref 36 (Kato 2016) |
| Li₁₀SnP₂S₁₂ Cl+O 공도핑 | 1.58 → 2.94 | — | 2차 · ref 53 |
| `Li₅.₃PS₄.₃ClBr₀.₇` (S/Cl/Br, Li 결손) | **24** | **0.155** | 2차 · ref 212 (Patel 2021) |
| Ge/Cl 공도핑 LGPS `Li₁₀₊ₓGe₁₊₂ₓP₂₋₂ₓS₁₂₋ₓClₓ` x=0.3 | **12.4** (25 °C) | 0.19 (캡션) | 2차 · ref 207 |
| `Li₆.₆P₀.₄Ge₀.₆S₅I` | 5.4 (냉간) / **18.4** (소결) | 0.17 (`Table 1`) | 2차 · ref 210 (Kraft 2018) |
| `Li₆.₄P₀.₆Si₀.₄S₅Br` (ACN 용매) vs 볼밀 | 3.1 vs 2.4 | 0.23 (x=0.4, `Fig. 14f`) | 2차 · ref 211 |
| LSSSI 도핑 LPSC (`Li₆.₀₂Sn₀.₀₂Sb₀.₀₃P₀.₉₅S₅Cl₀.₉₅I₀.₀₅`) | 5.2 (**30 °C** — 캡션) | ≈0.254 (`Fig. 12f` figure-read ≈) | 2차 · ref 208 = `ma2024_sb_doping_lpsc_conductivity` |
| `Li₃.₁₂P₀.₉₄Bi₀.₀₆S₃.₉₁O₀.₀₉` | 2.8 | — | 2차 · ref 40 (Ni 2022) |
| `Li₅.₄Al₀.₁P₀.₉₄Sb₀.₀₆S₄.₅₅O₀.₁₅Cl₁.₃` | 2.22 | — | 2차 · ref 209 |
| `Li₅.₆PS₄.₆Cl₀.₈I₀.₆` (LMA) | 2.44 | — | 2차 · ref 184 |

### 3b. 무질서·분극률·결함

| 양 | 값 | 출처 |
|---|---|---|
| Li₆PS₅Cl 자리 무질서 | **"62 % Cl on inner 4c sites"** (p.12) — ⚠ 같은 숫자가 `kraft2017` digest 에선 "할라이드가 S²⁻ 자리(4d)에 앉은 비율 62 %" · 리뷰는 출처를 [61, 129] 로 단다 | 2차 · refs 61, 129 (원값은 Kraft 2017 = ref 137) |
| Kraft 2017 Cl→I | Ea 하강 + σ₀ 하강 동반, σ 최적 `Li₆PS₅Cl₀.₅Br₀.₅` (`Fig. 5d`: Ea figure-read ≈ Cl 0.45 → Br 0.30–0.31 → I **0.38 반등** · σ₀ ≈ 2–3×10⁷ → ≈10³ K S cm⁻¹) | 2차 · ref 137 = `kraft2017_…` |
| Ge 유도 I/S 무질서 (Kraft 2018) | 개시 x_R ≈ 0.2 (20–25 % Ge) · **최대 무질서 figure-read ≈ 6 %** (`Fig. 14a` 우축 0–8 %) · Ea figure-read ≈ 0.37 → 0.23 eV | 2차 · ref 210 |
| LGPS 결함 앙상블 (Gorai 2020) | 형성에너지 figure-read ≈ V_Li 0.06–0.15 · Li_i 0.06–0.20 · P_Ge 0.14–0.20 · Ge_P 0.35–0.49 eV · 배열 간 퍼짐 **최대 ~140 meV** (본문) | 2차 · ref 198 |
| Li₂S 결함화학 (Lorger 2019) | LiCl 도핑 → V_Li (Ea **0.73 eV**, 0.33 % LiCl) · LiF 도핑 → Li_i (Ea **1.00 eV**, 0.11 % LiF) · 이동도 교차 ~300–600 °C · 이온반경 Cl⁻ 1.81 / S²⁻ 1.84 / F⁻ 1.33 / OH⁻ 1.37 Å | 2차 · ref 144 |
| LGPS O 치환 | "Ea ≈0.17 → 0.36 eV" (p.10) — ⚠ 원전 Ong 2013 의 **0.36 은 Li₁₀GeP₂O₁₂(전산화물)** 이고 **0.17 은 LGPS 격자 +4 % 스케일 값** (모체 LGPS 는 0.21) — 짝이 틀렸고 인용도 [93, 127] 로 돌렸다 | 2차 · `ong2013_lgps_family_substitution` §3 |

### 3c. 전기화학 안정성·계면 (축 표기는 우리가 붙임)

| 진술 | 값 | 우리 축 | 출처 |
|---|---|---|---|
| 황화물 산화 개시 | "above ~2–3 V" · 환원 "below ~0–0.5 V" | 혼합 | 2차 · refs 199, 200 |
| Li₇P₃S₁₁·LGPS·Li₆PS₅Cl 열역학 안정 상한 | **≈1.6–2.3 V** · 황화물 내재 창 "~0–2.5 V" vs 산화물 "0–5 V 이상" | B① | 2차 (번호 없음) |
| S 부격자 산화 분해 | "∼2.5–2.8 V vs Li⁺/Li" | 혼합 | 2차 · ref 155 |
| β-Li₃PS₄ ‖ NCM811 | >3.8 V 에서 산화 분해 | 겉보기 | 2차 · ref 165 (Koerver 2017) |
| **할라이드 치환의 산화 한계** | **"above 4.8 V vs Li⁺/Li"** | ⛔ 축 없음 | 2차 · ref 29 (리뷰 논문) |
| LiBH₄ 치환 x=0.1 | 창 1–4 V | 겉보기 | 2차 · ref 205 |
| Li 금속 E_F | "≈ −2.9 eV vs vacuum" (일함수 값) | — | 본문 |
| 전기음성도 | S 2.58 · O 3.44 · Cl 3.16 · F 3.98 | — | 본문 |
| Cl15 (`Li₅.₅PS₄.₅Cl₁.₅`) 4d Cl 점유 | **90.01 %** (원전 4a 56.32 %) · 대칭셀 **"1500 h @0.5 mA cm⁻²"** — ⚠ 원전(`lu2025` digest, Fig 2a)은 **800 h @0.5 · 2000 h @0.2** | E | 2차 · ref 164 |
| LiFSI 첨가 LPSCl (LiF-rich SEI) | >3000 h @0.1 mA cm⁻² | E | 2차 · ref 163 |
| LPSC-SbO | Li 대칭 4000 h · Li–S 932.6 mAh g⁻¹ @0.1C · 150 cyc 83.7 % · ε_p −2.06 → −2.57 eV (`Fig. 8e`) | E·B③·D | 2차 · ref 172 = `liu2024_…` |
| GG LPSCl1.5 | 대칭셀 >1400 h (`Fig. 11a`, 0.1 mA cm⁻²) · 위계 Cl1.5 > Cl1.0 > Cl0.5 | E·B② | 2차 · ref 206 = `gilgonzalez2022_…` |
| 산화 분해 반응 (Cl15) | `Li₅.₅PS₄.₅Cl₁.₅ → Li₃PS₄ + 1.5 LiCl + 0.5 Li₂S` (전자 0 — **화학적 준안정 분해**) | (hull) | 2차 · ref 164 |

### 3d. 기계

| 진술 | 값 | 출처 |
|---|---|---|
| 황화물 Young's modulus | **"10–25 GPa"** (p.20, p.36) — ⚠ 인용한 Sakuda 2013 원전은 유리 **18–25 GPa** | 2차 · ref 173 = `sakuda2013_…` |
| Li₂S–P₂S₅–P₂O₅ 옥시설파이드 유리 | P₂O₅ 0 → 10 mol% 에서 E **22 → 27 GPa** (P–O 결합해리에너지) | 2차 · ref 176 (Kato 2014) |
| LMA-Cl₁.₄₋ₓIₓ | E 15 → 11 GPa (x 0 → 1.4) · σ 최대 x=0.6 · 최적 E "12.37 GPa" (⚠ `Fig. 9b` figure-read ≈ 13.0) · CCD **1.6** vs 양끝 0.7 mA cm⁻² | 2차 · ref 184 |
| Li₂S–P₂S₅ 유리 | Li₂S↑ → E↑ (`Fig. 9d` figure-read ≈ 25 mol% 13 → 80 mol% 25 GPa) | 2차 · ref 185 |
| LiI 첨가 유리 | E↓ (`Fig. 9f` figure-read ≈ 0 → 30 mol% LiI: 23.5 → 18.6 GPa) · Si 음극 셀 E 17 vs 23 GPa → 20 사이클 용량 우위 | 2차 · ref 186 |
| 박막 한계 | 냉간가압 황화물 막 ~50–100 µm 아래는 균열 | 본문 p.37 |

### 3e. 셀·CCD (대표값)

| 계 | 값 | 출처 |
|---|---|---|
| Li₇P₃S₁₁ + 0.05 MO₂ | CCD 0.64 → **1.14** (SiO₂; `Fig. 12b` 라벨 **1.12**) · NCM811 200 cyc 86 % | 2차 · ref 52 |
| LSSSI 도핑 LPSC | 대칭 6000 h · CCD 1.4 · NCM811 181.0 mAh g⁻¹ | 2차 · ref 208 |
| Bi/O Li₃PS₄ | CCD 1.2 · 400 h @1 mA cm⁻² (본문만) · 2000 h @0.1 (`Fig. 13d`) | 2차 · ref 40 |
| Al/Sb/O LPSCl | H₂S −78 % · CCD 0.6 · 2000 h vs 기준 <44 h | 2차 · ref 209 |
| Li₆.₈Si₀.₈As₀.₂S₅I | 62,500 cyc @2.44 mA cm⁻² · 9.26 mAh cm⁻² — ⚠ 원전 제목상 **Li-In‖TiS₂** 셀(리뷰는 셀 구성 생략) | 2차 · ref 202 |
| GG 다층 Cl1.5/Cl1.0/Cl1.5 ‖ NMC811 | 20C 700 cyc — ⚠ `Fig. 11f` 에 **55 °C** 인쇄, 본문은 온도 생략 | 2차 · ref 206 |
| LPSOBC ‖ NCM811 | 50 cyc 후 177 mAh g⁻¹ | 2차 · ref 139 (Hwang 2024) |
| uncoated NMC811/LPSCl | ~100–300 cyc 에서 크게 감퇴 | 본문 (번호 없음) |

### 3f. 공정·수분

| 진술 | 값 | 출처 |
|---|---|---|
| LGPS 볼밀 무질서 | σ 한 자릿수 하락 | 2차 · ref 221 (Schweiger 2022) |
| Li₂S–P₂S₅–LiBH₄ 열간가압 | 상대밀도 86 → 91.5 % · σ 3.8 → 6.0 | 2차 · ref 223 |
| LiI 20 mol% 슬러리 vs 분말 (−40 °C 이슬점 드라이룸 30 min) | H₂S 0 cc g⁻¹ · σ 95 % 유지 vs 분말 68 % 손실 | 2차 · ref 226 |
| Si 치환 한계 (Li₆PS₅Br) | 볼밀 x=0.3 → ACN 용매 x=0.4 (입자 반경 ~350 nm · 공간전하층 모형) | 2차 · ref 211 |

### 3g. 로드맵 수치 (⛔ 인용 대상 아님)
- 소비자 기기 late-2020s · 자동차 ~2030 · 팩 **~400–450 Wh kg⁻¹ by mid-2030** (p.38) ↔ `Fig. 15` 는 **~450–500 Wh kg⁻¹** — 자기 그림과 다르다.

---

## 4. `Table 1` 전사 — 13행 전부 (pp.33–35) ★

> 원제: *"A comparative overview of several studies on anion-engineered lithium-based sulfide solid electrolytes…"*. 열 = 조성 · 합성 · 계열 · 음이온 전략(의도) · 결정 · 두께(mm) · σ · Ea · 창 · CCD · 전극 · 셀 성능 · 장점 · 단점 · ref.
> 웹 화면용 이미지: `tab_1.png`(p.33) · `tab_1b.png`(p.34) · `tab_1c.png`(p.35). **값의 정본은 아래 텍스트 전사다.**

### 4a. 물질·수송 열 + 우리 산수 두 열

| # | 조성 · ref | 합성 | 계열 · 전략(의도) | σ (mS cm⁻¹) | Ea (eV) | 홉 검산 1/Γ (298 K) *(우리 산수)* | σ₀ = σT·e^{Ea/kT} *(우리 산수, S K cm⁻¹)* | **음이온을 바꾸나?** |
|---|---|---|---|---|---|---|---|---|
| 1 | `Li₆PS₅Cl` · [227] Yu 2016 | BM 550 rpm 16 h + 550 °C 5 h | argyrodite · S 자리 Cl → 무질서·평탄화 | 1.8 | 0.29 | 8 ns | 4.3×10⁴ | (모체 그 자체) |
| 2 | **`Li₅.₄PS₄.₄Cl₁.₆`** · [228] Chen 2023 | **고속 혼합 2.5 min + 480 °C 16 h 소결** | argyrodite · **과잉 Cl (LiCl-rich) → Li 공공 최대** | **20.2** | **0.407** | **0.76 µs** | **4.6×10⁷** | ✅ |
| 3 | `Li₅.₄₅Ag₀.₀₅PS₄.₅Cl₁.₅` · [229] | BM 500 rpm 15 h + 500 °C 5 h | argyrodite(Cl-rich) · **Ag → Li** | 9.1 | 0.25 | 1.7 ns | 4.6×10⁴ | ✗ (양이온) |
| 4 | `Li₆.₅₅P₀.₄₅Si₀.₅₅S₅I` · [230] | BM 500 rpm 24 h + 550 °C 2 h | argyrodite(I-rich) · **Si → P** | 1.1 | 0.19 | 0.16 ns | 5.4×10² | ✗ (양이온) |
| 5 | `Li₆.₆P₀.₄Ge₀.₆S₅I` · [210] Kraft 2018 | 손분쇄·펠릿 + **550 °C 2주** | argyrodite · **Ge → P 로 S/I 무질서 유도** | 18.4 | 0.17 | 0.075 ns | 4.1×10³ | △ (양이온이 음이온 무질서를 유도) |
| 6 | `Li₁₀SnP₂S₁₂` + Li₃InCl₆ 계면안정층 · [231] | LSnPS BM 500 rpm 10 h + 550 °C 4 h · LIC BM 24 h + 260 °C 2 h | LGPS형 · **Sn → Ge 완전 치환** (비용·양극계면) | 4.79 (LIC 1.48) | 0.15 | 0.034 ns | 4.9×10² | ✗ (양이온 + 버퍼) |
| 7 | `Li₉.₅₄Si₁.₇₄(P₀.₉₀₃Sb₀.₀₉₇)₁.₄₄S₁₁.₇Cl₀.₃` · [232] | BM 370 rpm 40 h + 460 °C 8 h | LGPS형 · Cl + Sb (공기안정 Sb–S) | 8.8 | — | — | — | ✅ |
| 8 | `Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃` · [36] Kato 2016 | BM 370 rpm 40 h + 475 °C 8 h | LGPS형 · Si + Cl (3D 경로) | **25** | — | — | — | ✅ |
| 9 | `Li₃.₈₅Sn₀.₈₅Sb₀.₁₅S₄` · [233] | 볼밀 없이 550 °C 12 h | thio-LISICON · **Sb → Sn** | 0.85 | 0.43 | 1.9 µs | 4.7×10⁶ | ✗ (양이온) |
| 10 | `Li₇P₂S₈I` + SnCl₂ · [234] | 고에너지 BM + 200 °C 5 h | "thio-LISICON (LPSI)" · 금속할라이드 공도핑 (Li–Sn SEI) | 7.77 | 0.25 | 1.7 ns | 3.9×10⁴ | ✅ (Cl) |
| 11 | 70Li₂S–30P₂S₅ · [235] | 2단계 밀링·재결정 ("Li₇P₅S₁₁" 오기) | 유리세라믹 · 결정화 제어 | 3.1 | 0.35 | 83 ns | 7.7×10⁵ | ✗ (공정) |
| 12 | 70Li₂S–30P₂S₅ · [76] Seino 2014 | 냉간가압 후 **가압 하 280 °C 2 h** | 유리세라믹 · 일체화 + 결정화 | 17 | 0.18 | 0.11 ns | 5.6×10³ | ✗ (공정) |
| 13 | `Li₇P₂.₉Mn₀.₁S₁₀.₇I₀.₃` · [236] | BM 510 rpm 30 h + 250 °C 2 h | 유리세라믹 · Mn/I 공도핑 ("Li₇P₅S₁₁" 오기) | 5.6 | 0.22 | 0.53 ns | 8.8×10³ | ✅ (I) |

> 🔢 **홉 수 검산 규칙** (`D-2026-09-27-barrier-hop-count` · 트랙 = 우리 DFT 기준선 · 1저자 = 사용자): Γ = ν₀·exp(−Ea/kT), **ν₀ = 10¹³ s⁻¹ 가정**, T = 298 K (kT = 0.02568 eV), 1/Γ = 평균 대기. 차수 검산이지 확산계수·전도도가 아니다.

### 4b. 셀·장단점 열

| # | 두께 (mm) | 창 (V vs Li⁺/Li) | CCD (mA cm⁻²) | 전극 | 셀 성능 | 장점 (표) | 단점 (표) |
|---|---|---|---|---|---|---|---|
| 1 | — | — | — | Li₂S–C ‖ Li-In | 634 mAh g⁻¹ 초기 · 40 cyc 후 >300 | 계면이 수송 병목임을 정량 | 계면저항이 벌크보다 빨리 증가 |
| 2 | — | — | — | NCM622 (20 mg cm⁻²) ‖ **흑연** | 165.1 mAh g⁻¹ @0.1C · 200 cyc 80 % @0.3C | 초고 σ · 간단·빠름·확장 가능 · 고로딩 | 고온 소결 필요 · **취성 세라믹 (>6 MPa 에서 깨짐)** |
| 3 | — | — | **1.8** | NCM622 + Li₃InCl₆ 버퍼 ‖ Li-In | 154.9 @1.0C · 100 cyc 94.5 % | σ·Li 금속 호환·CCD↑ | 귀금속 Ag |
| 4 | 0.5–1 | **"Up to 6 V"** | — | NCM811 + LPSCl + Super P ‖ Li 금속 | 105 @0.05C · 300 cyc 연속 감퇴 · 평균 CE 96.3 % · 1C 31 | 낮은 Ea · 넓은 창 | 장기 용량 손실 · 양쪽 계면 열화 |
| 5 | — | — | — | 후막 NCM622 (160 µm) ‖ LTO | 99 mAh g⁻¹ · 0.25/0.5/1C 150 cyc · 6.8 mAh cm⁻² | 고 σ · 낮은 Ea · 후막 셀 | Ge 고가 · 매우 긴 합성 |
| 6 | — | — | — | NCM622 + LIC + LIC 버퍼 ‖ Li-In | 176.1 @0.1C · 100 cyc 후 106.2 @0.5C | 낮은 Ea · −20–60 °C 작동 · 양극쪽 안정 | 복잡한 이중층 · Li-In 사용 |
| 7 | — | — | — | NMC811 + SE (70:30) ‖ Li 금속 + 흑연막 | 182.4 @0.5C **55 °C** (공기노출 SE) · 30 cyc 92 % | 황화물치고 탁월한 공기안정 | σ 가 기록값보다 낮음 · Li 금속 불안정 → 보호층 |
| 8 | 0.24 | **"∼0–5 V vs Li-metal"** | — | LiNbO₃-LCO ‖ "Li₄Ti₃O₁₂"(오기) | 150C (25 °C) · 1500C (100 °C) · 500 cyc @18C 100 °C 75 % | 초고 σ·출력 · 고온 수명 | Li 금속 불안정 |
| 9 | — | — | — | TiS₂ ‖ Li-In | 230 @0.05C 30 °C · 80 cyc 99.2 % | 공기안정 · 저독성·풍부 원소 | 낮은 σ · 산화물 양극 미시험 · Sb 고용한계 |
| 10 | 0.16–0.18 (EIS) · 1 (풀셀) | "electrochemically stable; CV 에 Li 석출/용해 피크" | 1 | LiNbO₃-NCM811 + SE ‖ Li 금속 | 183.3 @0.1C · 250 cyc 99.2 % @0.5C | 고 σ · Li 안정 · Li–Sn SEI | 고로딩(>5.5 mg cm⁻²) 불량 |
| 11 | — | — | — | — | — | GC 계열 σ 향상 | 복잡 · 셀 미평가 · 준안정 |
| 12 | — | **"0 to >5 V"** | — | — | — | 고 σ · 낮은 Ea · 낮은 GB 저항 | 고온 일체화 · 풀셀 미시연 |
| 13 | — | **"∼0 to 5 V"** | — | S : SE : CB = 45:15:40 ‖ Li 금속 | 796 @0.05C · 60 cyc ~800 | 쉬운 합성 · LPS 대비 σ↑ | 풀셀 계면저항 높음 |

### 4c. `Table 1` 에서 우리가 읽은 것 (우리 산수)

1. **표 제목과 내용이 안 맞는다** — 13행 중 **6행은 음이온을 바꾸지 않는다** (Ag→Li · Si→P · Sn→Ge · Sb→Sn · 결정화 · 열간가압), 1행(Ge→P)은 양이온이 음이온 무질서를 *유도*한 경우다. p.7 의 범위 선언("양이온 단독 전략은 다루지 않는다")과도 어긋난다.
2. **역산 전지수 σ₀ 가 다섯 자릿수(4.9×10² – 4.6×10⁷ S K cm⁻¹)로 흩어진다** (T = 298 K 가정). 같은 Cl-rich 아지로다이트끼리도 2행(4.6×10⁷)과 3행(4.6×10⁴)이 1000배 다르다. Kraft 2017 이 경고한 "Ea 만으로 σ 순위를 읽을 수 없다" 가 **이 표 안에서 재현**된다 — 그러니 이 표의 σ 순위와 Ea 순위를 같이 읽지 않는다.
3. **2행(우리 modelc 조성)의 σ–Ea 쌍은 홉 수 검산과 차수에서 모순이다.** σ 20.2 mS cm⁻¹ 를 Nernst–Einstein(Haven = 1)으로 홉 빈도로 바꾸면 (n_Li = 4×5.4/a³, a ≈ 9.80 Å **가정**, 홉 길이 2–3 Å **가정**) **Γ ≈ 0.9–2.1×10⁹ s⁻¹ 가 필요**한데, Ea 0.407 eV · ν₀ 10¹³ s⁻¹ 의 홉 수 검산은 **Γ ≈ 1.3×10⁶ s⁻¹ (1/Γ ≈ 0.76 µs)** 다 — **700–1600배 모자란다**. 같은 계산을 1행(1.8 · 0.29)·3행(9.1 · 0.25)에 하면 1–2배 안에서 맞는다. ⇒ 2행은 (i) 실효 전지수가 ~10¹⁶ s⁻¹ 이거나 (ii) Ea 가 실온 σ 와 다른 온도구간·다른 성분(입계 포함 등)에서 나왔거나 (iii) 둘 중 하나가 오기다. 리뷰는 이 행을 "ultra-high ionic conductivity" 로만 소개한다. ⚠ 이것은 차수 검산이지 원전 판정이 아니다 — **원전(ref 228) 확인 전 우리 modelc 의 실험 앵커로 쓰지 않는다.**
4. **'창' 열 다섯 칸은 전부 겉보기 CV 창이다** ("Up to 6 V" · "∼0–5 V" · "0 to >5 V" · "∼0 to 5 V" · "electrochemically stable"). 같은 리뷰 p.24 의 열역학 상한 ≈1.6–2.3 V 와 **다른 양**이다. 우리 B①(2.256 V)과 같은 줄에 놓지 않는다.
5. **같은 명목 조성 = 우리 modelc** 가 문헌에서 **3.3 mS cm⁻¹**(Adeli 2019, 550 °C 5–7 h 합성 · LiCl 석출 — `adeli2019` digest §5.3)와 **20.2 mS cm⁻¹**(Chen 2023, 고속 혼합 + 480 °C 16 h)로 **6배** 갈린다. 리뷰는 앞의 값을 싣지 않았다. ⇒ `adeli2019` digest 가 이미 적은 *"Cl 1.6 단일상은 공정 의존적 가정"* 의 두 번째 데이터점이다.

---

## 5. 본문 절별 정리 (그림 실독 포함)

### 5.1 서론 (§1, pp.1–3)
- 황화물 SE 장점 = 고 σ(최고 24 [35] · 25 mS cm⁻¹ [36]) · 연성(계면 접촉) · 저온 공정 · Li 금속 호환. 과제 = 수분(H₂S) · 좁은 창 · 계면 · 비용 (2차 · refs 31–46).
- 음이온 공학 정의(§2 표 참조). **"전통적 도핑의 재명명이 아니다"** — 음이온 부격자를 *기능 단위*로 보고, 배열 엔트로피·다음이온 혼합으로 단일음이온계에 없는 조성공간을 연다는 주장 (p.2).
- 예: Cl+O 공도핑 Li₁₀SnP₂S₁₂ σ 1.58 → 2.94 (2차 · ref 53). O 치환은 "비가교 산소 자리"가 S 보다 안정해 전체 안정성을 올린다 (p.2–3, 2차 · ref 52).
- ⚠ p.3: *"SSSEs … superior ionic conductivity **and electrochemical stability** compared to their oxide counterparts [63, 64]"* — 같은 리뷰 p.24 가 *"intrinsic ESW of sulfides (∼0–2.5 V) is much narrower than oxides (0–5 V or higher)"* 라고 쓴다. **자기모순** (ref 64 = `okuno2020_…` 은 양극 계면 비교 논문).
- `Fig. 1` — 개념 바퀴 (§7 참조).

### 5.2 구조 계열 (§2, pp.3–9)
- **§2.1 유리·유리세라믹**: PS₄³⁻ · P₂S₇⁴⁻ · P₂S₆⁴⁻ 단위, 가교/비가교 S. 70:30 ≈3.2, 75:25 0.28, 최적 열처리 17 mS cm⁻¹ (ref 76). ★ **유리 vs 결정의 음이온 부격자 역할 구분**(p.4): 결정은 무질서를 *도입*해야 하고, 유리는 무질서가 *내재*한다 → 같은 치환이 유리/결정에서 반대 경향을 낼 수 있다. **혼합 음이온 효과**(LiI → 자유부피↑, Li 자리에너지 분포 확대, ref 82)는 결정 아지로다이트의 할라이드 자리 무질서와 **기전이 다르다**고 명시 — 이 리뷰에서 가장 좋은 구분이다.
  - `Fig. 2a–c` Li₂P₂S₆ (C2/m): 모서리 공유 PS₄ 쌍(P₂S₆²⁻) · Li 밀도맵 = 1D 사슬 → 7.8×10⁻⁸ mS cm⁻¹ · 0.48 eV (ref 59). ⚠ 본문 p.5 *"Unlike the P₂S₆²⁻ configuration, which contains a direct P–P bond…"* 는 **P₂S₆⁴⁻ 오기** (P–P 결합은 Li₄P₂S₆ 의 차아인산 음이온).
  - P₂O₅ 소량 → Li₇P₃S₁₁ 상 유도, σ 3.6배 · Al 도핑 Li₃₋₃ₓAlₓPS₄ 3배 이상 (refs 84, 85).
- **§2.2 아지로다이트**: F4̄3m · PS₄³⁻(4b P) · **할라이드 4a · 자유 S²⁻ 4d** · Li 48h(T5)/24g(T5a). Cl·Br 은 S²⁻ 와 섞이고 I 는 질서 유지 → σ Cl ≈1.5 · `Li₅.₃PS₄.₃Cl₁.₇` 6.6 · Li₆PS₅I 4.6×10⁻⁴ mS cm⁻¹.
  - `Fig. 2d–f` (ref 86): Li₆PS₅Cl 셀 · **500 K DFT-MD Li 밀도** · 48h 점프 통계(선 굵기 = 빈도). 계산 조건 기재 0.
- **§2.3 thio-LISICON**: Li₄GeS₄ (Pnma) · Li₄SnS₄ · Li₄SiS₄ (Pmn2₁). 양이온 단독 치환은 "다루지 않는다" 선언.
  - `Fig. 2g`: **그림은 LiS₄(청록)·GeS₄(남색) 사면체**인데 본문 p.7 은 "GeS₄ tetrahedra and **LiS₆ octahedra**" · 캡션은 "interconnected GeS₄ tetrahedra" — 그림(고립 GeS₄ + LiS₄)과 서술이 어긋난다.
- **§2.4 LGPS**: P4₂/nmc · 4d (Ge₀.₅P₀.₅) + 2b P · Li1–Li4 · c축 1D + 층간 교차 (`Fig. 2h,i`, refs 87, 73). Sn·Si 유사체 ≈4 · 2.3 mS cm⁻¹.
- **§2.5 기타**: Li₄SnS₄ 계(Bi·As·Sb, HSAB 연산), Li₃PS₄–Li₄SnS₄ 유리세라믹, LiI–티오인산염 하이브리드 (§3a 값).
- **★ 계열별 전략이 다르다** (p.8): *"argyrodites have received disproportionate research attention, and the resulting halide-substitution design rules are sometimes implicitly generalized to other families"* — 옳은 경고. `Fig. 3` 표가 그걸 정리한다.

### 5.3 수송 기전 (§3, pp.8–10)
- 공공/격자간 홉. 다중 비등가 Li 자리 + 병목 → **가장 높은 홉이 장거리 수송을 정한다**.
- 아지로다이트: 케이지 내(48h–48h) + 케이지 간(16e 경유) (`Fig. 4a–c`, ref 130). ⚠ 본문은 "inter-cage jumps (through 16e interstitials)" 를 `Fig. 4a–c` 에 붙이는데, `Fig. 4a` 의 **16e 라벨은 PS₄ 의 S** 다 (Li 격자간 16e 는 `Fig. 4e` 에 따로 있다 — 둘 다 16e Wyckoff 지만 다른 좌표 세트).
- **Cl⁻ 치환의 기전 서술 (p.9)**: *"When Cl⁻ substitutes for S²⁻, it introduces a **larger, more polarizable** anion"* → 🔴 **사실 오류**. Cl⁻(1.81 Å)는 S²⁻(1.84 Å)보다 작고(리뷰 자신이 p.23 에 이 반경을 적는다), 분극률도 S²⁻ 가 크다. 이 문장 위에 "혼합 다면체 → 골격 강성↓ → 회전장벽↓ → paddle-wheel" 사슬을 세웠다.
- **"Cl, Br > I" 와 결정 홉** (p.9, `Fig. 4d–f`, ref 131 Chien 2024): *"In Cl/Br-argyrodites the doublet (48h–24g–48h) jump must be fast, while the inter-cage (48h–16e–48h) barrier is critical."*
  - `Fig. 4f` 실독 (400 dpi 확대, **figure-read ≈**): 봉우리 높이(절대) — 48h′–48h′ 케이지 간 **Cl 0.42 · Br 0.51 · I 0.77** / 케이지 내 Cl 0.17 · Br 0.20 · I 0.31 / doublet **Cl 0.32 · Br 0.23 · I 0.20** / 48h–16e 케이지 간 **Cl 0.20 · Br 0.27 · I 0.48** eV. 직전 최소 기준 장벽: Cl doublet ≈0.25 vs Cl 48h–16e ≈0.13.
  - 🔴 **Cl 곡선에서는 doublet 장벽이 48h–16e 장벽보다 크다** — 본문 문장과 반대. I 에서는 48h–16e 가 율속(≈0.31)이라 맞는다. 그리고 세 할로겐 모두 **가장 높은 봉우리는 48h′–48h′ 케이지 간 홉**이다. 장벽을 무엇으로 계산했는지(NEB? 범함수?) **리뷰에 없다**.
  - 홉 수 검산 (298 K · ν₀ 10¹³ s⁻¹ 가정): Cl doublet 0.25 eV → 1/Γ ≈ 1.7 ns · Cl 48h–16e 0.13 eV → ≈16 ps · I 48h′–48h′ ≈0.56 eV → ≈0.3 ms.
- LGPS·가넷 경로: *"in garnet-type and some LGPS-type electrolytes, a migration path such as 24d→96h→48g→96h→24d"* → 이 경로는 **가넷(LLZO)** 표기다. LGPS 에 붙인 것은 혼동.
- O 치환 LGPS: "Ea ≈0.17 → 0.36" (§3b ⚠ 짝 오류). 할라이드 도핑은 16h/8f/4c 자리 개방 (Li₉.₅₄…Cl₀.₃).
- 끝 문장(p.10): *"Softer lattices … decrease energy barriers and also reduce the ionic attempt frequency [137]"* — 전지수 단서를 여기선 정확히 단다.

### 5.4 음이온 부격자의 역할 (§4, pp.10–24)

**§4 머리 (p.11)**: S 가 O 를 대신하면 전기음성도↓ → Li 결합 약화 · 반경↑ → 통로 확장 · 분극률↑ → 유연한 격자. 그리고 세 개의 일반화가 한 단락에 몰려 있다 —
 (i) *"oxygen substitution or the formation of halide-enriched surfaces … lower the VBM, which widens the electrochemical stability window"* (ref 139),
 (ii) 음극 쪽에선 할라이드 → LiCl·LiF 계면,
 (iii) *"larger and more polarizable anions … lowers the Young's modulus"*.

**§4.1 무질서 4범주 (pp.11–12)** — 리뷰가 "정의가 흐릿하다"고 스스로 지적하고 분류를 내놓는다.
| 범주 | 리뷰 정의 | 아지로다이트 예 |
|---|---|---|
| 조성(혼합음이온) 무질서 | 등가 자리에 두 종 이상이 통계적으로 분포 | "halide and sulfide can mix over the 4a and 4d sites" |
| 자리 무질서(부격자 혼합) | 원래 자리가 아닌 곳을 점유 | "some halide ions occupy S²⁻ sites and vice versa" |
| 점유 무질서(부분 점유) | 음이온 공공 | "Li₇PS₆ → Li₆PS₅Cl creates a **sulfur vacancy**" 🔴 |
| 동적 무질서 | PS₄³⁻·P₂S₇⁴⁻ 열운동이 홉과 같은 시간척도 | — |
- 🔴 **조성 vs 자리 구분이 아지로다이트에선 같은 현상을 두 번 센다** — 둘 다 4a/4d S²⁻↔X⁻ 교환이다. 리뷰의 구분 기준("조성 무질서는 화학량 변동, 자리 무질서는 위치 교환")은 Cl-rich 조성(우리 modelc)에서 두 개가 **동시에** 일어날 때 무엇을 재야 하는지 말해 주지 않는다.
- 🔴 **"Li₇PS₆ → Li₆PS₅Cl 은 S 공공을 만든다"** 는 틀렸다 — 음이온 자리 수는 6 그대로(PS₄ 의 S 4 + 자유 S 2 → S 4 + S 1 + Cl 1)이고 **Li 하나가 빠진다 (Li 공공)**. 리뷰 자신이 p.22 에서 "할라이드 치환은 Li 공공을 만든다" 고 바로 쓴다.
- 평탄화 기전: 자리에너지 분포 · 병목 확장 · 새 경로 · 다면체 회전장벽↓ (p.12).

**§4.2 수송·Ea (pp.12–14)**
- Ea = 이동 + 결함형성. 고무질서 초이온전도체는 이동항 지배 (refs 143–145).
- bcc 음이온 골격이 fcc/hcp 보다 장벽 낮음 (refs 83, 142) — ⚠ 원전인 Wang et al. 2015 *Nat. Mater.* 대신 2차 문헌을 인용.
- 분극률 서술: *"Replacing a less polarizable anion such as O²⁻ with a more polarizable one like S²⁻, Se²⁻, or I⁻ leads to a softening of the lattice …"* · *"This soft lattice lowers the Debye frequency which in turn lowers the migration barriers … Importantly, lattice softness also reduces the Arrhenius pre-factor"* (p.12).
- *"Experiments varying the halide fraction in Li₆PS₅X show that increasing lattice polarizability … lowers Ea but also affects carrier concentration [61]"* — ⚠ ref 61 = Banerjee & Tkatchenko 2025 (**계산** 논문)을 "experiments" 로 인용.
- `Fig. 5a,b` (ref 61): **질서(X⁻@4a · S²⁻@4c) vs 무질서**. 실독: (b) 는 4a 의 꼭짓점 자리(셀당 1)에 S²⁻, 4c 내부 4자리 중 1에 X⁻ = **셀당 한 쌍 교환(25 %)** 을 그린 예시다. 본문은 이 그림 옆에서 *"62 % Cl on inner 4c sites"* 를 말한다.
- ⚠ **4c/4d 혼용**: 같은 자유 S 자리를 p.6·p.11·`Fig. 3`·`Fig. 4e` 에선 **4d** (본문 11회), p.12·`Fig. 5` 에선 **4c** (3회)로 부르고, 원점 선택에 따른 동치라는 말이 **한 번도 없다**.
- `Fig. 5c,d` (ref 137 Kraft 2017): 격자 연화 → Ea↓ **그리고** σ₀↓. 본문 p.13: *"The result is an optimal point … Li₆PS₅Cl₀.₅Br₀.₅. This finding necessitates a paradigm shift … not simply to minimize lattice stiffness, but to optimize it."* — ✅ 정확. 그러나 `Fig. 5d` 실독(figure-read ≈): Ea 는 Br–Br₀.₅I₀.₅ 근처 ≈0.30–0.31 eV 최저 뒤 **I 에서 ≈0.38 로 반등**한다. 본문은 *"Systematically increasing the polarizability (from Cl to I) leads to a predictable softening … successfully lowers the activation energy"* 라고만 써서 **I 반등(= 무질서 소멸)** 을 빠뜨렸다 (`kraft2017` digest §5).
- 홉 수 검산 (298 K, ν₀ 10¹³ s⁻¹ 가정): Kraft Cl ≈0.45 eV → 1/Γ ≈ 4 µs · Br ≈0.30 → ≈12 ns. ⇒ 4 µs 와 12 ns 의 300배 차이에도 실측 σ 는 Cl 1.3 ↔ Br ~1 mS cm⁻¹ 로 비슷하다 — 이것이 바로 σ₀ 보상(Meyer–Neldel)이고, **ν₀ 를 상수로 놓는 홉 검산이 아지로다이트에서 차수를 틀릴 수 있다**는 경고이기도 하다.
- `Fig. 5e` (ref 146 Ohno 2020): 계열별 Ea 범위 막대. figure-read ≈ 아지로다이트 막대 0.14(Li₆.₁₇₅P₀.₈₂₅Si₀.₁₇₅S₅Br)–0.66(**Li₆PO₅Cl**), Li₆PS₅Cl ≈0.45; LGPS 막대 ≈0.22(Li₁₀GeP₂S₁₁.₄O₀.₄)–0.27(Li₁₀SiP₂S₁₂). ⇒ **산화물 아지로다이트 끝점이 막대 꼭대기** — "O 는 장벽을 올린다" 의 정성 근거. 홉 검산: 0.66 eV → 1/Γ ≈ 15 ms.
- 정적 위상 vs 회전 (p.12): *"Recent studies, however, suggest that while PS₄ reorientation can influence local site energies, the dominant effect … is its static topology and polarizability, rather than large-angle rotations [137]"* — 🔴 p.9 의 "Cl 치환 → 회전장벽↓ → paddle-wheel 로 Ea↓" 와 **같은 리뷰 안에서 충돌**한다.

**§4.3 계면 (pp.14–20)**
- **§4.3.1 밴드 정렬 모형** (p.14): E_F(전극) > CBM(SE) → 환원 · E_F < VBM → 산화 · *"the intrinsic electrochemical stability window of an SSE is fundamentally defined by its band gap"*. S 3p 가 VBM → 높은 VBM 이 좁은 산화창의 원인. **치환 기전**: 전기음성도 큰 O·Cl·F 가 *"severely moves the VBM and slightly moves the CBM to lower energies [152]"* · I 는 VBM 을 올린다 · S 3p–O 2p 혼성이 "중간 준위"를 만든다 [153, 154].
  - 🔴 **ref 152 = Ravi 2016 *ACS Energy Lett.* "CsPbX₃ 페로브스카이트 나노결정 밴드엣지"**, ref 154 = 혼합 할라이드 페로브스카이트 밴드갭. 황화물 SE 의 VBM 이동을 **할라이드 페로브스카이트(VBM = X p–Pb s 반결합)** 로 뒷받침했다 — 페로브스카이트는 할라이드가 VBM 그 자체라 할라이드를 바꾸면 VBM 이 움직인다. **아지로다이트는 S 가 남아 있는 한 VBM 이 S 3p 다** (`banik2022` · 우리 PDOS, §9d).
  - 🔴 Goodenough 식 "창 = 밴드갭" 은 **열역학 분해창이 갭보다 훨씬 좁다**는 Zhu 2015 · Richards 2016 · Schwietert 2020 와 정면으로 다른데, 리뷰는 앞 셋 중 Zhu 2015·Schwietert 2020 을 인용하지 않는다.
- **§4.3.2 음극** (pp.14–17): Li₃PS₄·Li₆PS₅Cl 은 Li 금속에 대해 열역학적으로 불안정 → Li₂S + Li₃P + LiCl (LGPS 는 Li–Ge 합금 → MIEC 계면 → 무한 성장, ref 156) vs Cl/Br 아지로다이트는 **LiCl/LiBr 자기제한** (ref 158). Han 2019: 전자전도가 덴드라이트 원인 (ref 157).
  - 🔴 p.15: *"halide substitution **lowers the VBM** and suppresses electron transfer from lithium metal into the electrolyte"* — **환원(Li 금속 → SE 전자 주입)은 CBM 의 문제**다. VBM 을 내려서 전자 주입을 막는다는 문장은 물리적으로 성립하지 않는다.
  - 🔴 p.15: *"Li₆PS₅Cl and Li₆PS₅Br exhibit improved compatibility with lithium metal by forming thin, self-limiting SEIs rich in LiCl or LiBr [160]"* — ref 160 = **Rao & Adams 2011** (`rao2011_…` digest: 볼밀 합성 + BV 이동망 연구, **Li 금속·SEI 서술 0**) → 인용 역할 불일치.
  - Lu 2025 (Cl15, `Fig. 6`): Cl 이 계면 쪽으로 이동 → LiCl-rich SEI. 리뷰의 구동력 설명: 4d Cl 소모 → 농도구배 + 화학적 분해 `Li₅.₅PS₄.₅Cl₁.₅ → Li₃PS₄ + 1.5LiCl + 0.5Li₂S` + "자유 Cl⁻ 는 약하게 배위, S²⁻ 는 PS₄ 에 묶임". ³¹P NMR: cycled 후 PCl₄ 41→36 %↓ · PS₂Cl₂ 17→24 %↑ (원전 표기, `lu2025` digest).
    - `Fig. 6` 실독: (a) Cl15 단면 SEM/EDS — Cl 맵이 상단(Li 쪽)까지 뻗음. (b) Li 1s(LiCl ≈56 eV / Li ≈54.8) · S 2p(P–Sₙ–P · PS₄³⁻ · Li₂S/S²⁻) · P 2p(P–Sₙ–P · PS₄³⁻ · P/LiₓP) 깊이 ~4.95–~39.98 nm. (c) figure-read ≈: **PS₄³⁻ 가 S 2p 의 74–85 %, P 2p 의 68–77 %** · **P–Sₙ–P 가 P 2p 의 22–32 %** · Li₂S 7–9 % · **Li₃P/P 0–2 %** (0–60 nm).
    - ⚠ **LPSCl 대조 패널이 없다** — 본문의 "stoichiometric Li₆PS₅Cl 대비 S·P 신호 억제" 는 이 그림으로 확인 불가. **LiCl 은 (c) 에서 정량되지 않는다** ("LiCl-rich" 는 Li 1s 정성뿐). P 2p 의 1/4 이 P–Sₙ–P(가교 다황) 인 점은 리뷰가 언급하지 않는다.
    - ⚠ 대칭셀 수치: 리뷰 "1500 h @0.5" ↔ 원전 800 h @0.5 · 2000 h @0.2.
  - Narayanan 2022 (`Fig. 7a,b`, ref 161): 실독(figure-read ≈) — 30 µA(≈0.15 mA cm⁻²)에서 Li⁰ 분율이 38 µAh cm⁻² 에 ≈34 % 까지, 2.5 µA(≈0.01)에선 ≈6 %. Li₂S/S-2p 는 세 전류 모두 ≈77–89 % 로 수렴. Li₃P/P-2p 는 30 µA 가 ≈75 % 봉우리 후 ≈60 %, 2.5 µA 가 ≈73 % 까지 증가, 10 µA 는 ≈17–41 % 에 머문다. EIS 는 J = 0.01 mA cm⁻² 에서 8 µAh cm⁻² 때 반원이 가장 큼(Z′ ≈290 Ω 까지). ⚠ (a)의 전류 세트(30/10/2.5 µA)와 (b)의 세트(2.5/0.5/0.05/0.01 mA cm⁻²)가 다르다.
  - Zeng 2022 (`Fig. 7c,d`, ref 50): Cl₀.₆ (200 cyc) "거칠고 불균일한 LiCl 층" vs Cl₁.₃ (400 cyc) "매끈·균일". ⚠ **조성과 사이클 수가 동시에 다르다** · (d) 에서 "LiCl interlayer" 로 표시한 띠가 **50 µm 축척 막대와 비슷한 두께(수십 µm, figure-read ≈)** — nm 급 SEI 로 읽기 어렵다 (원전 확인 필요).
- **§4.3.3 양극** (pp.17–20): S 3p VBM → 저전위 산화(∼2.5–2.8 V). Koerver 2017 (β-Li₃PS₄ ‖ NCM811, >3.8 V). **"Halide substitution … increasing the oxidative stability limit to above 4.8 V vs Li⁺/Li" [29]** (ref 29 = Zhang 2019 *Adv. Mater.* 리뷰). Cl-rich → LiCl 지배 CEI. 시뮬레이션이 "할라이드·S/Cl 무질서가 PS₄³⁻ 를 안정화하고 VBM 을 내린다" 고 한다는 서술 [50, 161, 166]. O 도핑 LGPS 산화한계↑ (ref 169). 4.5 V 이상에선 인공 계면층(LiNbO₃·Li₂ZrO₃·Li₃PO₄·LiF·AlF₃) 필요.
  - 🔴 **Zuo 2022** (`zuo2022_…` — Cl-rich 가 양극 계면에서 **더 많이** 분해하지만 저항성 산물을 덜 만든다) **미인용**. 우리 B① 은 comp1 = modelc (§9b).
  - Hu 2024 (`Fig. 8a,b`, ref 171): 탈리튬 NMC532 + LPSC 를 섞기만 해도 자발 반응. 실독(figure-read ≈): Raman ≈425 cm⁻¹ PS₄³⁻ 주봉 + 혼합 12 h 후 점선 위치 ≈475 cm⁻¹ 부근 신호 성장(S–S) · S 2p Li₂Sₙ · P 2p P₂Sₓ 성분이 25/50/75 % 시료로 갈수록 커진다 · 연 XAS 도식 = **Ni⁴⁺/³⁺ 가 주동**, Mn⁴⁺·Co³⁺ 순.
  - Li–S 전지 (`Fig. 8c–f`, ref 172 = `liu2024_…`): Sb/O 공도핑으로 SbS₄³⁻ → ε_p −2.06 → −2.57 eV · 음극 LiₓSbᵧS_z 계면 · 양극 S₈ 와의 전하이동 억제. ⚠ 리뷰는 이를 *"anion substitution (Sb for P, O for S)"* 로 묶는데, **ε_p 이동은 P–S → Sb–S 결합 대비(양이온 효과)** 다. 그리고 ε_p 는 절연체에서 비유일한 E_F 기준이라 VBM 기준으로 다시 재면 하강폭이 ≈0.2 eV 로 줄어든다는 판정이 `liu2024` digest §6.2 에 이미 있다 — 다시 논증하지 않는다. 본문 p.19 *"compared to the SbS₄³⁻ tetrahedron"* 은 PS₄³⁻ 오기.

**§4.4 기계·계면 접촉 (pp.20–22)**
- 황화물 E "10–25 GPa" → 크리프·입계 유동·균열 · 덴드라이트를 기계적으로 못 막는다 (ref 173).
- O → P–O 결합 → 강성↑: Kato 2014 옥시설파이드 유리 22 → 27 GPa (P₂O₅ 0 → 10 mol%, 몰부피↓).
- LiF 계면층(고표면에너지·고강성·전자절연), Li₃PO₄·Li₃BO₃ 양극 코팅.
- Dixit 2022 (ref 183): LPS vs LPSCl 펠릿·고분자 복합체 — LPSCl 이 더 치밀, UV 경화 고분자와는 Cl-rich 분해 산물(꽃잎 형태) → σ 저하.
- Kim 2026 (`Fig. 9a–c`, ref 184): Cl→I 치환 LMA. 실독 (500 dpi, figure-read ≈): **σ** 0.35 / 0.71 / 2.14 / **2.40 (x=0.6)** / 1.71 / 1.38 / 1.27 / 1.17 mS cm⁻¹ · **E** 15.3 / 14.7 / 13.5 / **13.0 (x=0.6)** / 12.8 / 12.5 / 11.8 / 10.8 GPa (x = 0–1.4, 0.2 간격). CCD 0.7 (Cl₁.₄) · **1.6** (Cl₀.₈I₀.₆) · 0.7 (I₁.₄) mA cm⁻² (`Fig. 9c` 라벨). 🔴 본문 "최적 조성 E = 12.37 GPa" 는 그림의 x=0.6 점(≈13.0)과 안 맞고(12.4–12.5 는 x = 1.0 근처), **캡션은 "optimizing σ at x = 0.8"** 이라 본문(x = 0.6, Cl₀.₈I₀.₆)과도 어긋난다 — Cl 아래첨자 0.8 을 x 로 혼동한 것으로 보인다.
- Kato 2018 (`Fig. 9d–g`, refs 185, 186): Li₂S 함량↑ → E↑ (고립 PS₄³⁻ ↑) · 황화물 유리는 산화물과 칼코게나이드 사이 (`Fig. 9e` figure-read ≈ 황화물 영역 E ≈12–30 GPa · 원자부피 ≈11–16 cm³ mol⁻¹) · LiI → E↓ (`Fig. 9f`) · Si 음극 셀에서 E 17 vs 23 GPa → 20 사이클 후 figure-read ≈ 1500 vs 850 mAh g⁻¹ (`Fig. 9g`).
- ⚠ 이 절에 **DFT 탄성상수가 한 줄도 없다** — 정작 Deng 2016 (ref 191, PBEsol 탄성텐서 23종)은 §4.5 에서 "무른 격자가 낮은 장벽 홉을 허용" 이라는 **수송 문장**에만 인용된다.

**§4.5 결함화학·캐리어 (pp.22–24)**
- 전하 보상: S²⁻ → X⁻ 는 Li 공공 · O²⁻ 는 등가(결함 불필요) · Bi³⁺→P⁵⁺ + O 는 Li 격자간 (ref 40). *"This is why Cl-rich argyrodites such as Li₅.₅PS₄.₅Cl₁.₅ have higher lithium vacancy concentrations than stoichiometric Li₆PS₅Cl."* ✅
- 크기: 큰 음이온(Br⁻)이 자유부피↑ → 결함형성↓ / I⁻ 은 국소 변형으로 공공 형성 불리 (출처 없음) / Cl⁻–S²⁻ 크기 일치가 변형 최소.
- 전기음성도: *"Anions with higher electronegativity form stronger, **more covalent** bonds with lithium"* → O·F 치환은 공공형성에너지↑ → σ↓ ("O 치환의 안정성–전도 트레이드오프"). 🔴 **전기음성도 차가 커질수록 Li–X 는 더 이온결합적**이다 (Li–F 가 가장 이온적). "더 세다" 는 몰라도 "더 공유적" 은 거꾸로다.
- "soft-cradle" 효과 (ref 192 Mo 2012). Deng 2016 (ref 191) 을 수송 근거로 인용.
- Gorai 2020 (`Fig. 10a,b`, ref 198): LGPS 결함은 **스칼라가 아니라 분포** · P_Ge < Ge_P · P-rich/Ge-poor 합성 권고. ⚠ `Fig. 10a` 안에 원전의 "(b)" 라벨이 그대로 남아 **(b) 가 두 번** 찍혀 있다.
- Lorger 2019 (`Fig. 10c–e`, ref 144): Li₂S 에 LiCl → V_Li(σ↑), LiF·LiOH → Li_i(σ↓) · 이동도 교차 · Brouwer 3영역 (내재/외인/회합). 홉 검산 (298 K): 0.73 eV → 1/Γ ≈ 0.22 s · 1.00 eV → ≈2.3 h — Li₂S 가 실온 부도체라는 사실과 정합.
- §4 결론 (p.23): *"anion identity … simultaneously governs the charge-compensation pathway, the local strain landscape, and the band-edge position that dictates oxidative stability"* — 세 번째 고리(밴드엣지 → 산화안정)는 §9b·§9d 에서 우리 데이터와 어긋난다.

### 5.5 치환과 성능 (§5, pp.24–32)
- 머리 (p.24): 황화물 산화 >~2–3 V · 환원 <~0–0.5 V · **LPSCl 등 열역학 상한 ≈1.6–2.3 V** · 내재 창 ~0–2.5 V (vs 산화물 0–5 V). 이 문장은 **p.18 의 ">4.8 V" 와 같은 리뷰 안에 있다.**
- 단일 치환: BH₄⁻ (Wang 2021, x = 0.1, 1–4 V) · **Gil-González 2022 Cl-rich** (`Fig. 11a–f`): σ 최대 LPSCl1.5 · **"higher mechanical strain associated with chlorine-based decomposition products … widening its operational voltage window"** (= 우리 B②) · 대칭셀 위계 Cl1.5 > Cl1.0 > Cl0.5 · LNMO·LCO 풀셀 · Cl1.5/Cl1.0/Cl1.5 다층 20C.
  - `Fig. 11` 실독: (a) Cl1.5 ±≈15 mV 1400 h · (b) Cl0.5 ≈35 h 부터 과전압 급증(±1 V 까지) · (c) Cl1.0 ≈140 h 이후 단락형 (전부 0.1 mA cm⁻²). (d) LNMO 50 cyc 에 figure-read ≈ 87 → 72 mAh g⁻¹ (≈17 % 손실, 활용률 낮음) — 본문 "stable cycling" 은 후하다. (e) LCO 1C ≈127 · 3C ≈105 · 10C ≈90 · 20C ≈47. (f) **"20C at 55 °C"** 700 cyc ≈125 mAh g⁻¹ — 본문은 55 °C 를 뺐다.
  - `gilgonzalez2022` digest 의 **반전 결론**(덴드라이트 억제엔 Cl1.0 의 "moderate instability" 가 숨은 지표)을 리뷰는 "moderately stable middle layer" 로만 옮겼다.
- **Hwang 2024 O 치환** (`Fig. 11g,h`, ref 139): `Li₆PS₅Br₀.₅Cl₀.₅` (LPSBC — **우리 comp2 와 같은 조성**) → `Li₆PS₄.₅O₀.₅Br₀.₅Cl₀.₅` (LPSOBC). 다중척도 시뮬레이션 + 실험: O 가 계면을 안정화, S 산화·원소 교환 억제, 접촉 손실 지연.
  - `Fig. 11g` 실독: NCM811/LPSBC 계면 S 의 PDOS 는 E_F 근처에 상태가 있고(빨강), LPSOBC 쪽은 계면·벌크 곡선 모양이 비슷하다. ⚠ 두 PDOS 패널은 **y 눈금이 없고 축척이 다르다** — "bulk-like" 는 정성 판단. (h) 는 **LPSOBC 셀 한 계열만**(용량 ≈200 → 178 mAh g⁻¹ · CE · 나이키스트 3장 모두 단일 시료) — 캡션의 "LPSBC 대비 우월" 은 이 그림으로 확인 불가. 전압축 2.0–3.6 V 의 기준 전극 미기재.
- 공도핑: Li 2024 MO₂ (`Fig. 12a,b`) · **Choi 2024 Ge/Cl LGPS** (`Fig. 12c–e`) · Ma 2024 LSSSI (`Fig. 12f,g`) · Ni 2022 Bi/O (`Fig. 13a–d`) · Choi 2024 Al/Sb/O (`Fig. 13e–g`).
  - `Fig. 12e` 실독: NEB 장벽 라벨 **Ge-doped γ 0.32 · γ-β 0.26 · γ-γ 0.34 · γ-α 0.21** / **Cl-doped γ 0.42 · γ-β 0.49 · γ-γ 0.36 · γ-α 0.21 eV**. 🔴 캡션 *"Cl doping generally results in lower overall barriers"* 와 본문 *"GeS₃Cl tetrahedra … significantly reduces energy barriers"* 는 **그림 숫자(Cl ≥ Ge)와 반대**다 — 그림에 없는 무도핑 LGPS 를 기준으로 해야만 성립할 수 있는데 리뷰는 그 기준을 싣지 않았다. 홉 검산: 0.21 eV → 0.36 ns · 0.49 eV → 19 µs.
  - `Fig. 12b`: CCD 라벨 Li₇P₃S₁₁ **0.64** · Si **1.12** · Ge **1.02** · Sn **0.78** mA cm⁻² — 본문 "1.14".
  - `Fig. 12f` (figure-read ≈): σ(×10⁻³ S cm⁻¹, **30 °C**) x = 0 3.45 · 0.03 4.5 · **0.05 5.17** · 0.07 4.2 · 0.10 2.5 / Ea 0.294 · 0.270 · **0.254** · 0.281 · 0.289 eV · XRD 는 x ≥ 0.07 에서 Sb₂S₃·SbSI 불순물 표식. `Fig. 12g` 는 **LPSC-0.05 셀만** (181 → ≈140 mAh g⁻¹ @50 cyc, figure-read ≈) — "기준 대비 개선" 은 그림으로 확인 불가.
  - `Fig. 13a` (600 dpi 확대): **"8-Li₆PS₅I" 점이 ≈1.8×10⁻³ 에 찍혀 있고 y축 "Conductivity" 에 단위가 없다** — 단위가 S cm⁻¹ 이면 리뷰 p.6 의 Li₆PS₅I 4.6×10⁻⁷ S cm⁻¹ 와 **≈4000배** 다르다 (원전 라벨 확인 필요).
  - `Fig. 13b,c`: H₂S (cm³ g⁻¹, 350 min) X = 0 ≈0.82 · 0.02 ≈0.63 · 0.04 ≈0.38 · 0.08 ≈0.14 · **0.06 최저** · 수돗물 침지 60 s 비교. `Fig. 13d`: CCD 1.2 vs 0.7 · 2000 h @0.1 vs Li₃PS₄ ≈95 h 실패 — 본문의 "400 h @1 mA cm⁻²" 는 그림에 없다.
  - `Fig. 13e` (500 dpi 확대): XRD 에 **LiSbS₂(●) 가 x = 0.04 · 0.06 · 0.08, LiCl(◆) 가 x = 0.08** 에 표시. 🔴 본문 *"proving that the complex doping strategy yields a well-defined and **phase-pure** argyrodite structure"* — **최적 조성 x = 0.06 에도 불순물 표식이 있다.** Raman: PS₄³⁻ ≈420 · SbS₄³⁻ ≈330 cm⁻¹.
  - `Fig. 13f` (figure-read ≈): H₂S @60 min (RH 40 %) LPSCl 0.62 · x=0 0.54 · 0.02 0.28 · 0.04 0.20 · **0.06 0.13** · 0.08 0.10 cm³ g⁻¹ (−78 % 재현 ✓) · 노출 전 σ 는 x=0(Al/Cl 사전최적 기준) ≈2.7 → x=0.06 ≈2.2 (≈−19 %, 로그축 판독). `Fig. 13g`: 계단 전류 시험에서 단락 신호가 Li₆PS₅Cl ≈25 h · x=0.06 ≈31 h 에 나타난다(figure-read ≈ · 본문 CCD 0.6 mA cm⁻²) · 0.1 mA cm⁻² 장기 2000 h vs 44 h.
- 표적 단일 치환: **Kraft 2018** (`Fig. 14a–d`): Ge⁴⁺(0.39 Å) → P⁵⁺(0.19 Å, 리뷰 수치) 가 I/S 무질서를 연다. 실독(figure-read ≈): x_R ≈ 0.15 까지 무질서 0 · ≈0.25–0.3 에서 1.5–3 % · 최대 ≈6 % · Ea ≈0.375 → ≈0.23 eV (x_R ≥ 0.35 평탄) · σ ≈10⁻⁶ → ≈10⁻² S cm⁻¹ (저해상도). 🔴 리뷰 *"This consequent disorder is not a side effect but the **primary reason**"* — 무질서는 **최대 ≈6 %** 인데 Ge 치환은 **Li 도 같이 늘린다**(Li₆₊ₓ). 그림은 상관을 보일 뿐 원인을 가르지 않는다. `Fig. 14c`: 후막 셀 0.25C ≈98 · 0.5C ≈73 · 1C ≈43 mAh g⁻¹ — "negligible fade, even at increased C-rates" 는 블록 안의 안정이지 율 손실(1C 에서 ≈56 % 감소)이 아니다. 홉 검산: 0.375 eV → 0.22 µs · 0.23 eV → 0.78 ns.
- **Choi 2025** (`Fig. 14e–h`, ref 211): 볼밀 Si 치환 한계 30 % → ACN 용매 40 % · 공간전하층 모형(작은 입자 → 표면부피분율 Φs↑ → 치환 수용↑). 실독(figure-read ≈): 원(용매) σ₂₉₈ 1.72 → **3.1 (x=0.4)** → 2.25 (0.5) · 삼각형(S-, 볼밀) **≈2.65 (x=0.3)** · 사각형("[ref.]" = **문헌값**) 최대 ≈2.35 (x≈0.35). Ea 0.27 (x=0) · 0.25 (0.3) · 0.23 (0.4). ⚠ 캡션은 사각형을 "ball-milled series (squares) at x = 0.3" 이라 부르지만 범례상 사각형은 문헌값이고 x = 0.3 에서 ≈1.65 다. 본문 "볼밀 2.4" 는 자체 볼밀(≈2.65)과도 안 맞는다.
- **Patel 2021** (ref 212, 그림 없음): `Li₆₋ₓPS₅₋ₓClBrₓ` — Br⁻ 하나가 S²⁻ 를 대신할 때마다 Li 공공 하나. 최적 `Li₅.₃PS₄.₃ClBr₀.₇` 에서 S/Cl/Br 이 4a/4d 에 무작위, Li 부격자 "liquid-like" → **24 mS cm⁻¹ · 0.155 eV**. 홉 검산: 0.155 eV → 1/Γ ≈ 42 ps (NE 로 필요한 Γ 보다 10–20배 크다 = 차수 정합).
- 공정 (pp.32): 건식 막 · 냉간소결 · R2R · 적층제조 · 레이저 치밀화 · 과도 밀링은 결함·σ↓ (ref 220 Maus 2025, Li₅.₅PS₄.₅Cl₁.₅) · LGPS 밀링 무질서 σ 10배↓ (ref 221) · 슬러리 수분 보호 (ref 226).
- **§5 결론 원리 (p.32)**: *"performance improves with the degree to which anion strategies are functionally decoupled rather than merely the number of dopants used"*.

### 5.6 결론·로드맵 (§6, pp.32–39)
- **§6.1**: "진짜 변혁적" = ① 아지로다이트 할라이드 치환(무질서 → 자릿수 향상) ② **다음이온·고엔트로피** ③ 표적 공도핑(LGPS Ge/Cl). 무질서는 보편적으로 좋지 않다 — 크기 일치·다중 음이온 자리일 때만; I 는 크기 불일치로 해롭고, 과도한 무질서는 상분리·불순물. 트레이드오프: O → 산화안정↑ σ↓ · 큰 분극 음이온 → 순응성↑ 하지만 문턱 넘으면 σ↓ · 최고 성능 조성은 복잡한 합성. "무질서 → 평탄화" 는 *"now broadly accepted"*.
  - ⚠ "고엔트로피 다음이온이 변혁적" 은 본문 근거가 Patel 2021 한 편과 ref 132 한 줄뿐이다.
- **§6.2**: 시대 구분 (~2015 σ 시대 → 2015–2020 계면 시대 → 2020– 통합·공학 시대). 과제 셋 = 화학·전기화학 불안정 · 계면 · 비용/확장. 수분: O 치환이 *"enhances moisture resistance with only a **marginal** sacrifice in ion conductivity"* (p.37) — ⚠ p.22·p.36 의 "O 는 σ 를 깎는다(트레이드오프)" 와 온도차가 있고, `[Wang25DPA]` 는 같은 계열에서 −37~−41 % 를 보고한다 (comparison §A).
  - p.37 *"The outdated approach of assuming wide windows from **simplistic computational calculations** has been replaced by …"* — 🔴 역사가 거꾸로다. **넓은 창은 CV(겉보기)에서 나왔고 좁은 창을 보인 것이 계산**(Zhu 2015 · Richards 2016)이다.
  - p.36 *"later rivaled by optimized **argyrodite** compositions like Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃"* — 🔴 **LGPS형**이다 (리뷰 자신의 `Table 1` 8행도 LGPS형).
- 로드맵 `Fig. 15` · 2025–2035 ML 스크리닝 · 고엔트로피·옥시할라이드설파이드 · 2050–2100 "도로·건물이 배터리" — 전망이므로 인용 대상 아님.

---

## 6. DFT/계산 방법 ★ — 이 리뷰의 계산 층위

이 리뷰는 **자기 계산이 0** 이다. 재수록한 계산 그림의 방법도 **하나도 적지 않는다.** 하이픈 줄바꿈을 복원한 본문(pp.1–39)에서 문자열을 셌다:

| 우리가 찾던 것 | 등장 | 판정 |
|---|---|---|
| `PBE` · `PBEsol` · `HSE` · `SCAN` · `VASP` · `Quantum ESPRESSO` | **0** | ⛔ 재수록 계산값의 범함수·코드 확인 불가 |
| `k-point` · `cutoff` · `supercell` · `DFT+U` · `vdW` | **0** | ⛔ |
| `AIMD` · `ab initio` · `NEB` · `nudged` | **0** (DFT-MD 1 · "molecular dynamics" 3 · "machine-learning-assisted MD" 1) | ⛔ `Fig. 4f`·`Fig. 12e` 장벽의 계산법 불명 |
| `grand potential` · `convex hull` · `Bader` · `COHP` · `ELF` · `BVSE` · `bond valence` | **0** | 우리 ESW·결합·BVSE 축은 이 리뷰 지도 밖 |
| `Nernst` · `Haven` · `Meyer`(–Neldel) | **0** (개념만 "pre-factor" 4회 — 전부 §4.2 Kraft 단락) | 전지수 경고가 결론부로 안 이어진다 |
| `elastic constant` · `bulk modulus` · `shear modulus` · `phonon` | **0** (`Young` 16 · `Debye` 2) | 기계 절이 실측 E 만 다룬다 |
| `SQS` · `special quasirandom` | **0** ("site disorder" 17회) | 무질서를 *계산에서 어떻게 표현했나* 는 한 번도 안 묻는다 |
| `polarizab` | **34** | 분극률이 이 리뷰의 중심 어휘 |

**재수록된 계산 그림 목록 (방법 기재 상태)**

| 그림 | 원전 | 무엇을 계산했나 | 리뷰가 적은 방법 |
|---|---|---|---|
| `Fig. 2e,f` | ref 86 | 500 K Li 밀도 · 점프 통계 | "DFT-based MD" 한 마디 |
| `Fig. 4f` | ref 131 Chien 2024 | 경로별 이동 에너지 곡선 | 없음 |
| `Fig. 5a,b` | ref 61 Banerjee & Tkatchenko 2025 | 질서/무질서 구조 (원전은 비국소 분산 상호작용이 국소구조를 정한다는 계산) | 없음 |
| `Fig. 8c–e` | ref 172 Liu | 전하밀도차 · PDOS · ε_p | 없음 (→ `liu2024` digest §6) |
| `Fig. 10a,b` | ref 198 Gorai 2020 | LGPS 결함형성에너지 앙상블 | "ensemble-based defect calculations" |
| `Fig. 11g` | ref 139 Hwang 2024 | NCM811/LPS(O)BC 계면 구조 · S PDOS | "multiscale simulations" |
| `Fig. 12e` | ref 207 Choi 2024 | 단일·협동 홉 장벽 | "machine-learning-assisted MD" |
| (그림 없음) | ref 171 Hu 2024 | 탈리튬 NMC/LPSC 계면 DFT-MD | "DFT-MD simulations" |

- **무질서 처리**: 리뷰 n/a. 재수록 그림 중 `Fig. 5b` 는 셀당 한 쌍 교환 예시, `Fig. 10b` 는 배열 4개(s1–s4) 앙상블 — 무질서를 **분포로 보고**한 유일한 계산 그림이다.
- ⇒ 이 리뷰의 계산 수치는 **어느 것도 우리 값과 방법을 맞춰 비교할 수 없다.** 가져올 것은 *질문*과 *원전 번호*뿐이다.

---

## 7. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 개념 바퀴: 계열 4 · 전략 4 (할라이드 · O · 다음이온 · 음이온+양이온) · 구조/전자 결과 5 (격자 팽창 · 음이온 무질서 · 지형 평탄화 · 밴드엣지(VBM/CBM) 이동 · 골격 연화/경화) · 성질 5 · 셀 4 · 과제 4. ⚠ "Property enhancements" 삽화는 **EDLC 나이키스트 도식**(ref 62 Mei 2018) — SE 데이터 아님 | 원고 서론 '음이온 공학' 틀의 체크리스트 (§11-ii). 그림 재사용 X |
| 2a–c | Li₂P₂S₆ (C2/m): 모서리공유 PS₄ 쌍 · Li 밀도맵 = 1D (7.8×10⁻⁸ mS cm⁻¹ · 0.48 eV, ref 59) | 우리 계 밖 |
| 2d–f | Li₆PS₅Cl 셀 · **500 K DFT-MD Li 밀도** · 48h 점프 통계(선 굵기 = 빈도) (ref 86) | 우리 MLIP-MD Li 밀도·점프망 그림 양식 참고 (방법 미기재라 값 비교 X) |
| 2g | Li₄GeS₄ (Pnma) — 그림은 LiS₄·GeS₄ 사면체, 본문은 "LiS₆ 팔면체" · 캡션은 "interconnected GeS₄" | 불일치 기록만 |
| 2h,i | LGPS: Li1–Li4 · (Ge/P)S₄ · PS₄ · LiS₆ 사슬 · c축 16h/8f 지그재그 (refs 87, 73) | — |
| 3 | 5계열 × (구조·장점·단점·음이온 부격자 특징·핵심 전략·한계) + 6축 레이더(σ · 계면접촉 · 기계강도 · Li 안정 · 산화안정 · 비용). **레이더에 눈금·출처·수치 0** | ⛔ 레이더 수치화·인용 금지 (저자 정성 판단). argyrodite 칸 "Distinct 4a (halide) and 4d (S²⁻) sites" · thio-LISICON 칸 "Anion identity is fixed by family definition" ↔ `Table 1` 10행과 모순 |
| 4a–c | Hanghofer 2019: 4a/4d/4b · 16e(= PS₄ 의 S) · 48h 케이지 내 · 케이지 간 P1/P2 · PS₄ 회전 화살표 | 우리 BVSE 채널 해석 어휘(intra/inter-cage) |
| 4d | Chien 2024 Li 밀도 등면: Cl·Br 연결망 / I 고립 덩어리 | 무질서 ↔ 연결성 정성 근거 |
| 4e,f | 경로 4종 정의(48h–24g–48h doublet · 48h–16e–48h · 48h–48h′–48h · 48h′–48h′) + 에너지–경로 곡선. figure-read ≈ 봉우리 48h′–48h′ Cl 0.42/Br 0.51/I 0.77 · doublet 0.32/0.23/0.20 · 48h–16e 0.20/0.27/0.48 eV — **Cl 에선 doublet > 48h–16e 로 본문과 반대** | 우리 NEB 가 되살아나면 경로 라벨 체계 참고. 방법 미기재 → 값 인용 X |
| 5a,b | 질서(X⁻@4a · S²⁻@4c) vs S²⁻/X⁻ 자리 무질서 — (b) 는 셀당 1쌍(25 %) 교환 예시 (ref 61) | 우리 무질서 배열 설명 그림 양식. **4c 표기**(본문 다른 곳은 4d) 주의 |
| 5c,d | Kraft 2017: 격자 연화 → Ea↓ + σ₀↓ (Cl→I). figure-read ≈ Ea 0.45 → 0.30 → I 0.38 반등 · σ₀ ≈2–3×10⁷ → ≈10³ K S cm⁻¹ | Meyer–Neldel 근거는 `kraft2017` 원전으로 인용 |
| 5e | Ohno 2020 계열별 Ea 범위 막대 — 아지로다이트 막대 꼭대기 = Li₆PO₅Cl ≈0.66 eV (figure-read ≈) | "O 는 장벽을 올린다" 정성 근거 |
| 6a–c | Lu 2025 Cl15‖Li: SEM/EDS · XPS 깊이 · 반정량 (PS₄³⁻ 우세 · P–Sₙ–P 22–32 % · Li₃P ≈0) — **LPSCl 대조 없음 · LiCl 미정량** | `lu2025` digest 로. "LiCl-rich" 는 정성 |
| 7a,b | Narayanan 2022: 전류밀도별 Li⁰·Li₂S·Li₃P 분율 (operando XPS) + EIS | 우리 Li 흡수 분해 산물(Li₂S · Li₃P · LiCl) 정성 앵커 |
| 7c,d | Zeng 2022: Cl₀.₆ (200 cyc) vs Cl₁.₃ (400 cyc) 단면 — 조성·사이클 동시 변화 · 표시된 띠가 수십 µm | ⛔ 정량·인과 인용 X |
| 8a,b | Hu 2024: 탈리튬 NMC532 + LPSCl 자발 반응 (Raman ≈475 cm⁻¹ S–S · XPS Li₂Sₙ/P₂Sₓ) · Ni⁴⁺/³⁺ 주동 | §B③ 정성 (우리 comp1‖LCO 산물과 같은 계열) |
| 8c–f | Liu 2024 Sb/O: 전하밀도차 · ε_p −2.06 → −2.57 eV (P–S vs Sb–S) · 기전 도식 | `liu2024` digest 판정 유지 (ε_p 기준 문제 · 양이온 효과) |
| 9a–c | Kim 2026 Cl→I LMA: σ 최대 x=0.6 ≈2.40 · E 15.3 → 10.8 GPa · CCD 1.6 vs 0.7 (figure-read ≈) — 본문 E 12.37·캡션 x=0.8 과 불일치 | I 쪽 연화 방향 (우리 comp2(Br) 연화와 같은 방향) |
| 9d–g | Kato: Li₂S↑ → E↑ · 유리군 E–원자부피 지도 · LiI → E↓ · Si 음극 셀 | 기계 축 정성 (유리 실측 — 우리 단결정 DFT 와 다른 양) |
| 10a,b | Gorai 2020 LGPS 결함 앙상블: P_Ge 0.14–0.20 < Ge_P 0.35–0.49 eV · 배열 퍼짐 ~140 meV | "결함·장벽은 스칼라가 아니라 분포" — 우리 disorder_ensemble 보고 규율과 같은 정신 |
| 10c–e | Lorger 2019 Li₂S: LiCl → V_Li · LiF/LiOH → Li_i · 이동도 교차 · Brouwer 3영역 | li2s 트랙(**외부 1저자**) 참고 후보로만 — 판단은 그 트랙 몫 |
| 11a–c | GG 2022 대칭셀 0.1 mA cm⁻²: Cl1.5 1400 h · Cl0.5 ≈35 h · Cl1.0 ≈140 h | `gilgonzalez2022` digest (반전 결론 포함) |
| 11d–f | GG 풀셀: LNMO 50 cyc ≈87→72 · LCO 율 · 다층 NMC811 **20C · 55 °C** | ⚠ 온도 생략 · "stable" 과장 주의 |
| 11g,h | Hwang 2024: NCM811/LPSBC vs /LPSOBC 계면 S PDOS · LPSOBC 셀(단일 계열) | ⭐ 우리 LPSOCl·comp2 에 가장 가까운 O 치환 계산 — 원전 확보 (§12b) |
| 12a,b | Li 2024 MO₂ 공도핑 Li₇P₃S₁₁: 첫 CE 74.7/85.5/82.1/81.7 % · CCD 0.64/1.12/1.02/0.78 | — |
| 12c–e | Choi 2024 Ge/Cl LGPS: 나이키스트 · Arrhenius · NEB 장벽(Ge 0.32/0.26/0.34/0.21 · Cl 0.42/0.49/0.36/0.21 eV) — 캡션 "Cl 이 더 낮다" 와 반대 | 캡션 모순 기록. 장벽 인용 X |
| 12f,g | Ma 2024 LSSSI 도핑 LPSC: XRD(x ≥ 0.07 불순물) · σ/Ea (30 °C) · NCM811 셀(단일) | `ma2024` digest |
| 13a–d | Ni 2022 Bi/O Li₃PS₄: 열처리 T–σ 지도(**8번 Li₆PS₅I ≈1.8×10⁻³ · 단위 없음**) · H₂S · 수침지 · CCD/장기 | 수분 축 정성. 13a 의 Li₆PS₅I 점 인용 금지 |
| 13e–g | Choi 2024 Al/Sb/O LPSCl: XRD(**LiSbS₂ x = 0.04–0.08**) · Raman · H₂S/σ 유지 · CCD/장기 | 본문 "phase-pure" 반증 기록 |
| 14a–d | Kraft 2018 Ge-Li₆PS₅I: 무질서 ≤≈6 % ↔ Ea ≈0.37 → 0.23 · σ · 후막 셀 · EDX | 무질서 *크기* 감각 (62 % vs 6 % 가 같은 단어) |
| 14e–h | Choi 2025 용매 합성 Si 40 % · σ(x) · 공간전하층 모형 · Φs(r) | 공정 의존 고용한계 — 우리 modelc 단일상 가정과 연결 (§4c-5) |
| 15 | 로드맵 2000–2100 (2008 Li₆PS₅X · 2011 LGPS · 2014 17 mS · 2016 25 mS · 2025 습공기 공정 · 2030s ~450–500 Wh kg⁻¹ · 2100+) | ⛔ 인용 X (전망 · 본문 수치와 불일치) |
| Table 1 | 13행 비교표 (pp.33–35) — σ · Ea · 창 · CCD · 셀 · 장단점. **2행 = 우리 modelc 조성** | §4 전사 · 창 열 인용 금지 · σ₀ 다섯 자릿수 산포 |

---

## 8. Post-processing ★

- **무엇** (재수록 그림 기준): Li 밀도 등면(`Fig. 2e`, `Fig. 4d`) · 점프 통계 그래프(`Fig. 2f`) · 경로–에너지 곡선(`Fig. 4f`, `Fig. 12e`) · PDOS + p-밴드중심(`Fig. 8e`, `Fig. 11g`) · 전하밀도차(`Fig. 8c,d`) · 결함형성에너지–E_F 도표 + 앙상블 산포(`Fig. 10a,b`) · Brouwer 도표(`Fig. 10e`) · XPS 깊이 분해 + 반정량(`Fig. 6`, `Fig. 7a`, `Fig. 8a`) · Raman(`Fig. 8a`, `Fig. 13e`) · EIS + 등가회로(`Fig. 7b`, `Fig. 11h`) · Rietveld 무질서율(`Fig. 14a`) · 공간전하층 모형(`Fig. 14g,h`).
- **도구**: 어느 그림에도 소프트웨어 이름이 없다 (VESTA·pymatgen·LOBSTER 0회).
- **수치화·기록**: 리뷰 자체의 수치화는 `Table 1` 하나. 무질서·장벽·결함에너지를 **정의와 함께 표로 기록한 곳이 없다** — 우리가 읽은 값은 전부 figure-read 다.

---

## 9. 우리 DFT 대비 ★★ (`../our_dft_baseline.md` · `db/properties/canonical_registry.json`)

> 우리 값 규율: canonical/HOLD/금지는 registry → citation_hazards → decisions 순으로 확인했다. **MD σ·D·Ea 는 절대값을 쓰지 않는다**(1저자 2026-09-18). band gap 은 PBE fixed-occ nscf 고유값이고 문헌 절대 비교 금지('wide-gap' 수준만). 기계는 relaxed-ion PBE(QE) 를 밝힌다.

### 9a. A — 이온전도

| 리뷰 명제 | 리뷰 근거 (2차) | 우리 | 판정 |
|---|---|---|---|
| Cl-rich(Li 결손) → Li 공공↑·무질서 → σ↑ (p.22 · `Table 1` 2행 · Adeli · Feng 2020 · Patel 2021) | refs 135, 193, 212, 228 | 기준선 문서: comp1 → modelc 에서 **D↑·Ea↓ 방향**. ⚠ 둘 다 단일 시드 — comp1 단일시드 Ea 는 **HOLD**(`HZ-comp1-Ea-diffusive-gate`), modelc 단일시드는 `cross_composition_ranking` 금지 | ✅ **방향 일치 · 수치 순위로 쓰지 않는다** |
| 4a/4d 무질서 → 지형 평탄화 → Ea↓ (p.6, p.11–12, `Fig. 5`) | refs 92, 93, 137 | modelc 는 Cl-rich 무질서 배열 · 무질서율을 정의해 잰 지표는 없음 | ✅ 정성 일치 / ⚠ 리뷰에 무질서율 정의가 없어 정량 대조 불가 |
| 분극률↑ → Ea↓ 그러나 σ₀↓ (Kraft) | ref 137 | 우리 σ₀(전지수) 축 없음 · ε∞/음속 미보고 | 판정 불가 — `kraft2017` digest §7 의 기존 판정 유지 |
| **O 치환 → σ↓** (p.22, p.36) · "marginal" (p.37) | p.12 ref 148(⚠ OER 전기촉매 논문) · p.22·p.36·p.37 은 출처 번호 없음 | LPSOCl ↔ modelc 차를 **O 효과로 읽는 것 자체가 원장 금지**: `HZ-cross-system-Ea` **BLOCKED** · modelc 3×3×1 항목 `difference_with_lpsocl_as_O_effect` · `same_table_with_lpsocl_box331__seed_count_differs` | ⛔ **우리 데이터로 판정 불가.** 문헌끼리는 리뷰와 같은 방향(`[Wang25DPA]` −37~−41 % · `Fig. 5e` Li₆PO₅Cl) |
| 큰 음이온 → 격자 팽창 → 병목 확장 → Ea↓ (p.12, p.22) | refs 127, 147 | — | ⚠ **문헌끼리 엇갈림**: `[Zhao21HECS]`(`zhao2021_…`) BVSE 50종 회귀는 r_anion 을 VIP 1위로, "작은 음이온 치환"을 Ea↓ 전략으로 낸다. 크기 효과는 무질서 허용 여부와 엉켜 있어 단독 규칙이 안 된다 |
| `Table 1` 2행: Li₅.₄PS₄.₄Cl₁.₆ 20.2 mS cm⁻¹ · 0.407 eV | ref 228 | modelc = **같은 명목 조성** · 우리 DFT 는 단일상 가정 | ⚠ **같은 조성 3.3 ↔ 20.2 (6배, 공정 의존)** + 2행 σ–Ea 홉 검산 모순(§4c) — 우리 단일상 가정은 둘과 *양립*하지만 증명되지 않는다 |
| paddle-wheel(p.9, `Fig. 12e` GeS₃Cl) vs "정적 위상이 지배"(p.12) | refs 133–135, 137, 207 | PS₄ 회전 지표 없음 | 판정 불가 — 리뷰 내부 충돌 기록만 |

### 9b. B — 산화안정성 (4축으로 갈라 읽는다)

| 리뷰 명제 | 우리 축 | 우리 | 판정 |
|---|---|---|---|
| *"Halide substitution … increasing the oxidative stability limit to above 4.8 V vs Li⁺/Li"* (p.18, ref 29 = 리뷰) | **축 없음** — B②(기계 구속, GG K_eff 20 → LPSCl1.5 0.80–4.30 V)보다도 높으니 **겉보기 CV 창**으로 읽어야 한다 | **B① onset: comp1 = modelc = 2.256 V** (grand-potential · LiS₄·SCl₃·Li₅PS₄Cl₂ 제외 · S²⁻-limited) | 🔴 **B① 에서는 성립 안 함** (Cl 이 onset 을 안 옮긴다 — `banik2022` 와 같은 결론). 겉보기 창과는 비교 대상이 아니다 |
| *"S²⁻ → O²⁻/Cl⁻/F⁻ … severely moves the VBM … to lower energies [152]"* · 할라이드·S/Cl 무질서가 VBM 을 내린다 [50, 161, 166] (p.14, p.18, p.23, p.37) | B① 의 전자구조 설명 | VBM 성격: **comp1·modelc 둘 다 S 3p** · LPSOCl 도 **S 3p**, O 2p 는 VBM 아래 2.3–5.5 eV 에 매몰 (`lpsocl_dos_gap.json`) · LPSOCl vs modelc dVBM **−0.058 eV** (셀 간 정렬 미보정 *정황*, `b2o3_cbm_character` 기록) | 🔴 **부분 치환은 VBM 성격을 안 바꾼다** — 리뷰의 근거(ref 152)는 할라이드가 VBM 그 자체인 페로브스카이트다 |
| p.24 "LPSCl 열역학 상한 ≈1.6–2.3 V · 황화물 창 ~0–2.5 V" | B① | 2.256 V | ⭕ 같은 자리. ⚠ **절대값 일치 주장 금지** — 우리 2.256 vs `[Zhu15]`·`[Schw21]` 2.01 V 의 0.246 V 는 원인 미확정 (기준선 문서) |
| `Table 1` 창 열 ("Up to 6 V" · "∼0–5 V" · "0 to >5 V" …) | 겉보기 CV | — | ⛔ B① 과 같은 줄에 두지 않는다 |
| GG: Cl 산물 고몰부피 → 기계 구속 → 창 확대 (p.25) | **B②** | 우리 `constrained_esw.py` 가 경향 재현 (modelc 쪽이 넓어짐 — comparison §B② 기존 판정) | ✅ **방향 일치** — "Cl-rich 가 산화에 강하다" 가 참인 유일한 축 |
| Hu 2024: 탈리튬 NMC + LPSCl 자발 반응 · S–S · P₂Sₓ (`Fig. 8a,b`) | **B③** | comp1‖LiCoO₂ −0.3227 eV/atom (InterfacialReactivity, 산물 Co₉S₈·Li₂SO₄·Li₃PO₄·Li₂S·LiCl — comparison §B③) | ✅ 정성 일치 (황 산화 + 인 산화종) |
| Hwang 2024: O 치환 계면의 S 가 bulk-like (`Fig. 11g`) | B③ | LPSOCl 계면 계산 없음 | 판정 불가 — 원전 확보 대상 |
| Zuo 2022 (리뷰 **미인용**): Cl-rich 가 **더 많이** 분해, 산물의 질이 다름 | B① 양 · B③ 질 | 우리 modelc onset 반응식이 Zuo Eq2(전자 적게·LiCl 많이) 거동 | 리뷰의 "Cl → 산화안정↑" 를 반박하는 실측이 빠졌다 |
| O 치환 → 수분 저항 (Bi/O · Al/Sb/O · 옥시설파이드 유리) | **B④/수분** | 우리 수분 축 값 없음 (`o2_muO_screen` citable: None) | 판정 불가 — 문헌 대 문헌 (`[Zhu20]` · `[Kim26Moist]` · `[Hyun25Han]` · `[Yang25]`) |

### 9c. C — 기계

| 리뷰 명제 | 리뷰 근거 (2차) | 우리 (relaxed-ion PBE · QE · 0 K 단결정 C_ij → VRH / BM3 EOS) | 판정 |
|---|---|---|---|
| 황화물 E "10–25 GPa" | ref 173 (원전은 유리 18–25) | E_VRH comp1 **22.06** · modelc **27.66** · LPSOCl **35.04** · comp2 **20.03** GPa | ⚠ **다른 양** (펠릿·유리 실측 vs 단결정 DFT) — 범위 안팎을 따지지 않는다 |
| **P–O → 강성↑** (Kato 2014 옥시설파이드 유리 E 22 → 27 GPa) | ref 176 | LPSOCl vs modelc: **E_VRH 35.04 vs 27.66 (+27 %)** · **B₀ 24.71 vs 21.71 (+14 %)** | ✅ **방향 일치 (O → 강성↑)**. ⚠ E_VRH 는 계마다 비교군이 달라(`HZ-elastic-cross-composition` CONDITIONAL — 조성별 pseudo/ecut/k) **방향 서술까지**, B₀ 는 같은 비교군(`b0-dft-bm3-v1`). 크기 비교 금지 |
| 크고 분극 큰 음이온 → E↓ (Kim 2026 Cl→I · Kato LiI) | refs 184, 186 | comp2(Br 50 %) vs comp1: **E_VRH 20.03 vs 22.06 (−9 %, 같은 비교군)** · B₀ 25.8 vs 26.233 | ✅ **방향 일치** (`kraft2017` 의 음속 연화와도 같은 방향) |
| 리뷰 규칙(작고 덜 분극 → 단단)으로 Cl-rich 를 설명 | — | comp1 → modelc: **E_VRH↑ (22.06 → 27.66) 인데 B₀↓ (26.233 → 21.71)** | ⚠ **리뷰 틀 밖** — Cl-rich 의 효과는 분극률이 아니라 Li 공공·무질서·C₄₄ 경로 (기준선 문서 "방향 반대"). 음이온 크기 규칙 하나로 E 와 B 를 함께 예측할 수 없다 |
| "적당한 E 가 CCD 최대" (Kim 2026) vs "부드러운 SE 는 덴드라이트를 못 막는다" (p.20) | ref 184, 173 | CCD·파괴 계산 없음 | 판정 불가 (서로 다른 축을 한 문단에 섞음) |

### 9d. D — 전자구조

| 리뷰 명제 | 우리 (PBE fixed-occ nscf 고유값) | 판정 |
|---|---|---|
| 할라이드 치환 → VBM↓ → gap·창 확대 (p.14) | gap comp1 **2.066** vs modelc **2.099** eV (Δ +0.033, 같은 비교군) · VBM 둘 다 S 3p | ⚠ 방향은 같지만 크기가 PBE 무질서 흔들림(±0.2–0.3 eV) 안 — **"변화 없음"** 으로 읽는다 |
| O 치환 → VBM↓ (p.11, p.14, p.37) | LPSOCl **2.2309** eV (modelc 대비 +0.132) · O 상태가 밴드엣지에 없음 · VBM S 3p | 🔶 gap 은 조금 넓어짐(방향 일치) · VBM 성격 불변 → **산화 onset 상승으로 이어진다는 근거가 안 된다** (B① 은 S 가 pin — `[Famprikis19]` 음이온 IP 사다리) |
| O 를 넣으면 창이 넓어진다 | **+B₂O₃ 1.9671 eV — modelc(2.099)보다 좁다**. CBM 이 **B**(삼각평면 BS₃ 의 빈 p_z, 원자당 CBM 성분 1위) — `b2o3_cbm_character_2026_09_07.json` | 🔴 **반례** — O 를 같이 넣어도 동반 양이온이 CBM 을 끌어내리면 갭이 준다. 리뷰의 "음이온 → 밴드엣지" 틀은 양이온이 만드는 엣지 상태를 못 본다 |
| *"halide incorporation decreases the covalency of the P–S bond network"* (p.15, refs 135, 159) | ICOHP(P–S, 결합당, LOBSTER · 같은 비교군): comp1 **−5.938** → modelc **−6.000** eV (**Cl-rich 에서 1 % 강화**) · comp2 −5.913 (0.4 % 약화) · LPSOCl −6.04 | 🔴 **우리 계산에서 '공유성 감소' 는 안 보인다.** 그리고 우리 `adeli2019` digest 에는 P–S 공유성·환원 구동력 서술이 없다 (인용 역할 확인 필요) |
| S 3p–O 2p 혼성이 "중간 준위" 를 만든다 (p.14, refs 153/154 — 154 는 페로브스카이트) | LPSOCl fixed-occ nscf: **갭 안 결함 준위 없음 (clean insulator)** | 🔴 우리 계산에선 중간 준위 없음 |

### 9e. E — 환원 / Li 금속

| 리뷰 명제 | 우리 | 판정 |
|---|---|---|
| LPSCl 은 Li 금속에 열역학적으로 불안정 → Li₂S + Li₃P + LiCl (p.15) | grand-potential: **환원 가장자리 1.717 V** (comp1 = modelc · 2026-09-22 라벨 정정 후 — 1.242 V 는 첫 환원 평탄) · 0 V 산물 Li₂S/Li₃P/LiCl | ✅ 일치 (불안정 + 산물). ⚠ 창 절대값의 문헌 일치는 주장하지 않는다 (`HZ-esw-reduction-limit-label` CONDITIONAL) |
| Cl-rich → LiCl-rich 자기제한 SEI → 음극 우위 (Lu · Zeng · GG 대칭셀) | 열역학 가장자리는 comp1 = modelc → Cl 효과는 **구동력이 아니라 산물 분율·형태 축** | ⚠ **문헌 충돌** (comparison §E 머리: GG 의 "moderate instability(Cl1.0)" vs Lu 의 "Cl15 우위") — 리뷰는 한쪽만 서술 |
| "할라이드가 VBM 을 내려 Li → SE 전자이동을 막는다" (p.15) | — | 🔴 물리 오류 (환원은 CBM) — 인용 금지 |

### 9f. F — 도핑 (음이온–양이온 공도핑)

| 리뷰 명제 | 우리 | 판정 |
|---|---|---|
| 공도핑 = 기능 분리 (O 로 안정 · 양이온으로 캐리어) (p.25, p.32) | 우리 **Nd₂O₃**(Nd 양이온 + O) · **+B₂O₃**(B + O) 는 리뷰 분류상 공도핑이다 | 🔶 틀은 맞지만 **B₂O₃ 는 '분리' 가 아니라 '간섭'** (B 가 CBM 을 낮춤 · §9d). Nd·희토류는 리뷰에 **0회** |
| O 는 S 자리에 들어가 P–O (안정 결합) | LPSOCl: O 가 PS₄ 안 S 자리 → **PS₃O, P–O 1.559 Å** | ✅ 자리 일치 (`[Jang23ZnO]` · `[Liu24SbO]` 도 PS₄ 안 S) |
| HSAB 연산(Sb·Sn·Bi) → 수분 안정 | cascade `air_hsab` 축 (comparison §A 토크 노트) | 정성 일치 (수치 X) |
| 양이온 치환이 음이온 무질서를 유도 (Kraft 2018 Ge → I/S) | 우리 Nd@Li / Nd@P 트랙 — 음이온 무질서 지표 미측정 | 빈칸 (아이디어만 — §11-iii) |

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

**10-1. 분극률 → Ea 저하의 일반화 (Kraft 2017 의 Meyer–Neldel 뉘앙스가 결론에서 사라진다).**
- "polarizab" 가 본문에 **34회** 나오는데, 전지수 σ₀ 동반 하강은 §4.2 의 Kraft 단락 **4회에만** 갇혀 있다. §4 머리(p.11) · §4.5 · §6.2(p.37 *"high polarizability of the S²⁻ anion and the facile mobility of Li⁺"*) 는 다시 "분극 → 쉬운 이동" 으로 돌아간다.
- `Fig. 5d` 의 **I 반등**(Ea ≈0.38)을 서술하지 않아 "Cl → I 로 예측대로 낮아진다" 고 썼다 — I 의 저전도는 연화가 아니라 **무질서 소멸 + σ₀ 붕괴**다 (`kraft2017` §5).
- p.9 의 기전 사슬은 **"Cl⁻ 가 S²⁻ 보다 크고 더 분극된다"** 는 사실 오류 위에 서 있다.
- 우리 쪽 교훈: 홉 수 검산에서 ν₀ 를 상수(10¹³ s⁻¹)로 두면 Kraft 계열에서 Cl(4 µs)과 Br(12 ns)의 300배 차이를 만들지만 실측 σ 는 비슷하다 — **검산 줄은 차수 경고용이지 순위 판정용이 아니다.**

**10-2. 무질서 정의 (4a/4d 자리 교환).**
- 4범주 분류에서 **조성 무질서와 자리 무질서가 아지로다이트에서는 같은 4a/4d 교환**이다 — 두 번 센다.
- **무질서율의 정의가 없다** — "X 가 S 자리에 앉은 분율" 인지(50 % = 무작위, 62 % = 역전), 무작위를 100 % 로 정규화한 값인지 말하지 않는다. "62 %" 는 Kraft 정의(할라이드가 S²⁻ 자리에 앉은 비율)인데 출처를 [61, 129] 로 돌렸다.
- **4d(11회)·4c(3회) 혼용**, 동치 언급 0. Morgan 2021(4c)·Kraft 2017(4d)·Lu 2025(4d)를 섞어 읽는 독자가 점유율 숫자를 자리별로 잘못 짝지을 수 있다.
- 같은 단어 "무질서" 가 Li₆PS₅Cl 의 **~62 %** 와 Ge-Li₆PS₅I 의 **≤≈6 %**(`Fig. 14a`)를 동시에 가리킨다. Kraft 2018 의 Ea 하강을 "무질서가 주원인" 으로 단정했지만 그 계는 Li 도 함께 늘었다.
- "Li₇PS₆ → Li₆PS₅Cl 은 S 공공" — 틀렸다(Li 공공).

**10-3. 서로 다른 합성·측정 조건의 σ 를 한 표에 섞었다.**
- `Table 1` 의 역산 σ₀ 가 **다섯 자릿수** 흩어진다 (§4c). 측정 온도도 제각각 — Ma 2024 는 30 °C, GG 다층 셀은 55 °C, Bi/O 는 단위 없는 축.
- 같은 명목 조성(우리 modelc)이 문헌에서 **3.3 ↔ 20.2 mS cm⁻¹**. 같은 시료를 8개 실험실이 재면 σ 가 **6.7배** 흩어진다는 인터랩 연구(`ohno2020_interlab_…`)를 **인용하지 않았다**.
- 그 위에서 "최고 σ" 순위와 "Ea 순위" 를 같이 읽게 만든다.

**10-4. DFT 수치의 방법 누락.**
- 범함수·코드·k점·셀·AIMD 길이·NEB 여부가 **전부 0회** (§6). `Fig. 4f`·`Fig. 12e` 장벽, `Fig. 10` 결함에너지, `Fig. 8e`·`Fig. 11g` PDOS 가 방법 없이 재수록됐다. ε_p 의 E_F 기준 문제(절연체에서 비유일)는 `liu2024` digest 가 이미 판정했다.
- 계산 그림의 **캡션이 숫자와 반대**인 경우까지 있다 (`Fig. 12e`).

**10-5. 산화안정성을 밴드갭/VBM 정렬로만 설명한다.**
- "창 = 밴드갭" (p.14) 과 "VBM 하강 → 산화한계 4.8 V 이상" (p.18) 은 **열역학 분해창**(Zhu 2015 · Richards 2016)과 **골격 유지 탈리튬화**(Schwietert 2020)를 비켜 간다 — 앞의 둘 중 Zhu 2015 와 Schwietert 2020/2021 은 **미인용**. 근거로 쓴 ref 152·154 는 **할라이드 페로브스카이트**다.
- 같은 리뷰 안에 **p.3("황화물이 산화물보다 전기화학 안정성 우수") · p.18(">4.8 V") · p.24("≈1.6–2.3 V", "~0–2.5 V")** 가 공존한다. 축 이름이 없어서 셋이 모순인지조차 독자가 가를 수 없다.
- p.37 "단순 계산이 넓은 창을 가정했다" 는 역사적으로 반대다.
- Cl-rich 가 양극에서 **더 많이** 분해한다는 Zuo 2022 미인용.

**10-6. 사실 오류 (원고 인용 금지)** — Cl⁻ 가 S²⁻ 보다 크고 더 분극 (p.9) · Li₇PS₆ → Li₆PS₅Cl 이 S 공공 (p.11) · "전기음성도↑ → Li 와 더 공유적" (p.22) · "할라이드가 VBM 을 내려 Li 금속 → SE 전자이동 억제" (p.15) · Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ 를 아지로다이트로 (p.36) · 가넷 경로 24d→96h→48g 를 LGPS 에 (p.10) · P₂S₆²⁻ 에 P–P 결합 (p.5, ⁴⁻ 오기) · "Li₁₀MP₂O₁₂ Ea 0.17 → 0.36" 짝 오류 (p.10) · Sb→P 를 "anion substitution" 으로 (p.19) · `Table 1` "Li₇P₅S₁₁"(×2) · "Li₄Ti₃O₁₂" 오기.

**10-7. 그림–본문 불일치 (실독으로 확인)**
| 위치 | 그림 | 본문/캡션 |
|---|---|---|
| `Fig. 4f` | Cl: doublet 장벽 ≈0.25 > 48h–16e ≈0.13 eV | "Cl/Br 에서 doublet 은 빨라야 하고 48h–16e 가 결정적" |
| `Fig. 9b` | σ 최대 x = 0.6 · 그 점 E ≈13.0 GPa | 본문 "E 12.37" · 캡션 "x = 0.8" |
| `Fig. 11f` | "20C at 55 °C" | 본문 온도 생략 |
| `Fig. 11h` · `Fig. 12g` | 단일 시료 | "기준 대비 우월" |
| `Fig. 12b` | CCD 1.12 | 본문 1.14 |
| `Fig. 12e` | Cl 장벽 ≥ Ge 장벽 | "Cl doping generally results in lower overall barriers" |
| `Fig. 13a` | Li₆PS₅I ≈1.8×10⁻³ (단위 없음) | 본문 p.6 Li₆PS₅I 4.6×10⁻⁷ S cm⁻¹ |
| `Fig. 13d` | 2000 h @0.1 mA cm⁻² | 본문 "400 h @1 mA cm⁻²" (그림에 없음) |
| `Fig. 13e` | LiSbS₂ x = 0.04–0.08 · LiCl x = 0.08 | "phase-pure" |
| `Fig. 6` | Cl15 단독 · LiCl 미정량 | "LPSCl 대비 S·P 억제" · "LiCl-rich" |
| `Fig. 7c,d` | 조성 + 사이클 동시 변화 · 띠 수십 µm | "Cl-rich 가 더 균일" (통제 비교처럼) |
| `Fig. 14c` | 1C 에서 ≈56 % 용량 감소 | "negligible fade, even at increased C-rates" |
| `Fig. 14f` | 사각형 = "[ref.]" 문헌값 | 캡션 "ball-milled series (squares)" |
| `Fig. 15` | ~450–500 Wh kg⁻¹ | 본문 ~400–450 Wh kg⁻¹ (pack) |
| `Fig. 2g` | LiS₄ + GeS₄ 사면체 | 본문 "LiS₆ octahedra" |

**10-8. 인용 역할 불일치** — §12a 표. 요약: ref 160(Rao 2011)에 SEI 내용 없음 · ref 135(Adeli 2019)를 P–S 공유성·환원 구동력 근거로 · ref 152/154(할라이드 페로브스카이트)를 황화물 VBM 근거로 · ref 148(OER 전기촉매 논문)을 "O 는 안정성↑·σ↓" 근거로 · ref 167(전극 물리 일반 리뷰)을 "S–S 형성 억제" 근거로 · ref 200(층상 LiMS₂ 음극 논문)을 "황화물 SE 는 0–0.5 V 아래에서 환원" 근거로 · ref 62(EDLC 나이키스트)를 개념도 삽화로 · ref 187(페로브스카이트 결함 자기조절)을 전하 보상 원리 근거로 · ref 61(계산)을 "experiments" 로 · ref 29(일반 리뷰)를 ">4.8 V" 근거로 · Ong 2013 의 값을 refs 93/127 로 · Lu 2025 수치 변형(1500 h).

**10-9. 범위 선언과 내용의 불일치** — `Table 1` 13행 중 6행 음이온 불변 · 결론의 "고엔트로피 다음이온 = 변혁적" 을 받치는 본문 근거가 한 편 · thio-LISICON 을 `Fig. 3` 에서 "음이온 정체 고정" 으로 정의해 놓고 `Table 1` 10행에 Cl/I 계를 thio-LISICON 으로 분류.

**10-10. 내부 충돌** — O 의 σ 대가 "marginal"(p.37) vs 트레이드오프(p.22·p.36) · paddle-wheel(p.9) vs 정적 위상(p.12) · Li₄SnS₄ 9.4×10⁻⁴(p.7) vs 7×10⁻²(p.8) · 황화물 안정성 p.3 vs p.24.

**10-11. σ–Ea 홉 수 검산 모순** — `Table 1` 2행 (§4c-3). 우리 modelc 조성이라 특히 중요하다.

**10-12. 과잉 외삽** — 2050–2100 로드맵("도로·건물이 거대한 배터리", "자기치유 나노구조") 은 리뷰의 데이터와 무관한 전망이다.

---

## 11. 우리 연구 연결 ★★★

### 11-i. 축별 판정표 — 맞는 곳 / 어긋나는 곳 / 방법 의존이라 판정 불가

| 축 | ✅ 맞는 곳 | 🔴 어긋나는 곳 | ⛔ 판정 불가 (방법·원장) |
|---|---|---|---|
| **A 이온전도** | Cl-rich → Li 공공·무질서 → 빠름 (우리 기준선 방향 · 수치 순위 X) · 무질서가 연결성을 만든다 (`Fig. 4d` · `Fig. 5`) | — (우리 쪽 반증 없음) | O 치환의 σ 효과 (원장 금지) · 분극률 → σ₀ 축 (우리 σ₀ 없음) · `Table 1` 2행 절대값 (σ 절대값 인용 금지 + 홉 검산 모순) |
| **B① 열역학 onset** | 황화물 열역학 상한 ≈1.6–2.3 V (p.24) 와 같은 자리 | **할라이드·O 치환이 산화 한계를 올린다 (p.18)** — 우리 comp1 = modelc 2.256 V · VBM S 3p 불변 | LPSOCl onset (미계산) |
| **B② 기계 구속** | GG: Cl 산물 → 구속 → 창 확대 (우리 `constrained_esw.py` 경향 재현) | — | 절대 창 (K_eff 의존) |
| **B③ 양극 계면** | 탈리튬 NMC 와 자발 반응 · S–S/P₂Sₓ 산물 | 리뷰의 "Cl-rich CEI 가 수동화" 는 Zuo 2022 (더 많이 분해) 를 빼고 쓴 것 | O 치환 계면 (Hwang 2024 원전 미독) |
| **B④ 수분** | — | — | 우리 값 없음 |
| **C 기계** | O → 강성↑ (LPSOCl) · Br → 연화 (comp2) | 리뷰의 크기·분극 규칙으로 Cl-rich 를 못 설명 (E_VRH↑ · B₀↓) | 실측 E 와 DFT E_VRH 의 크기 비교 |
| **D 전자구조** | O → 갭 소폭↑ (+0.13 eV, 정황) | VBM 하강 서사 (VBM 성격 불변) · P–S 공유성 감소 (우리 ICOHP 는 반대 방향 1 %) · O 2p 중간 준위 (우리: 없음) · +B₂O₃ 는 O 가 있어도 갭↓ | 진공 기준 절대 VBM (우리 벌크 계산으로 못 잰다 — 슬랩·정렬 필요) |
| **E 환원** | Li 금속에 불안정 · Li₂S/Li₃P/LiCl | "VBM 하강이 환원을 막는다" | Cl 함량에 따른 SEI 형태 (계면 MD 없음 — comparison §H) |
| **F 도핑** | O@PS₄ 자리 · 공도핑 분류 | "기능 분리" 가 +B₂O₃ 에선 간섭으로 나타남 | Nd (리뷰 0회) |

### 11-ii. 원고 서사에 쓸 수 있는 '음이온 공학' 틀 (우리 상대값 인용정책 안에서)

리뷰의 분류를 **틀로만** 빌리고, 수치는 전부 우리 정본에서 가져온다. 트랙 = 우리 DFT 기준선 · ESW · 탄성 → 1저자 = 사용자 (통지할 제3자 없음).

1. **두 레버를 축별로 분해해 보인다** — *"Within the anion-engineering taxonomy (halide enrichment vs. oxygen substitution), our PBE calculations show that the two levers act on different property axes: Cl enrichment (Li₆PS₅Cl → Li₅.₄PS₄.₄Cl₁.₆) leaves the thermodynamic (layer-①) oxidation onset unchanged at the S²⁻-limited value and keeps the valence-band maximum of S 3p character, whereas O substitution into the PS₄ unit stiffens the framework (higher bulk modulus in the same EOS protocol) without introducing O states at either band edge."* — 숫자를 넣을 때는 2.256 V · B₀ 21.71 → 24.71 GPa 를 방법 라벨과 함께, E_VRH 는 "direction only" 단서와 함께.
2. **리뷰의 '밴드엣지 이동' 서사에 대한 반론 문장** — *"Partial anion substitution does not remove S 3p states from the valence-band edge; the oxidation onset therefore remains pinned by the remaining sulfide anions, consistent with Banik et al. (2022)."* (근거: `banik2022` + 우리 PDOS. 리뷰는 인용하지 않는다 — 리뷰를 반론 대상으로 쓰려면 p.14·p.18 쪽수를 정확히 단다.)
3. **산화안정을 말할 때 축을 붙인다** — *"Cl enrichment widens the mechanically constrained window (layer ②), not the intrinsic onset (layer ①)."* (GG + 우리 `constrained_esw.py` 경향.)
4. **수송은 '방향' 으로만** — *"Both the literature trend and our simulations point in the same direction (Cl enrichment accelerates Li transport)"* 까지. 비율·Ea 차는 멀티시드 판정이 있는 값만, 그리고 계 간 상대차로만 (1저자 2026-09-18).
5. **O 치환의 σ 대가는 우리 말로 쓰지 않는다** — 문헌(리뷰 + `[Wang25DPA]`)의 트레이드오프로만 인용하고, 우리 LPSOCl MD 를 그 근거로 붙이지 않는다 (원장 금지).

### 11-iii. 빈칸 — 아이디어만 · 비용 감각 · "할 것" 이 아니다

| 빈칸 | 리뷰가 주는 단서 | 우리 쪽 상태 | 비용 감각 (실행 계획 아님) |
|---|---|---|---|
| **Br-rich (Cl→Br)** | Patel 2021 `Li₅.₃PS₄.₃ClBr₀.₇` 24 mS cm⁻¹ · LPSBC→LPSOBC (Hwang 2024) | comp2(`Li₆PS₅Cl₀.₅Br₀.₅`) 가 gap(legacy, provisional) · B₀ · E_VRH · ICOHP 를 이미 가짐. **Br-rich Li 결손 조성(modelc 의 Br 판)** 은 없음 | 같은 파이프라인 1조성 = EOS · fixed-occ nscf · LOBSTER(우리 실측 SCF ~10 h + nscf k점당 ~20 h, gabia CPU 8랭크) · 탄성(GPU 41 GB, 수 일) · MD 3×3×1 |
| **I / I-rich** | Kim 2026 Cl→I 연화 · Kraft 2018 Ge 유도 I/S 무질서 · `Fig. 4f` I 의 48h′ 장벽 | comp3(Cl₀.₅I₀.₅)·comp5(Li₆PS₅I) legacy gap 만 (provisional, 구조모형 rhombo-62) | I 는 무질서가 열리지 않으면 느리다 — 질서 배열 선택이 결과를 정한다 (보고량 카드 필요) |
| **Se (S→Se)** | 분극 사다리 언급 · ref 166 (Li₆PS₅₋ₓSeₓCl SEI 계산) | 없음 | Se 는 S 보다 이온화 퍼텐셜이 낮다 → **B① onset 이 Se 로 내려갈** 가능성 (음이온 IP 사다리) — 산화 쪽엔 불리한 방향의 가설 |
| **N** | Li₃N 계면층 언급뿐 | Li₃N 계는 **UMA 사용 금지** (2026-06 판정) | N³⁻ 는 IP 사다리 최하단 → 산화 onset 하강 쪽 — 우리 산화 서사엔 역방향 |
| **F** | LiF SEI · `[LiInF]`(F 가 σ 를 깎음) | 없음 (F 는 cascade 도펀트 후보 맥락뿐) | F⁻ 는 IP 최상단이지만 S 가 남는 한 B① 은 S 가 pin — "F 로 산화창" 은 B① 에선 기대하기 어렵다 |
| **다음이온 (S/O/Cl/Br)** | LPSOBC (Hwang 2024) · 옥시할라이드설파이드 로드맵 | LPSOCl(S/O/Cl) 하나 | 조성×배열 조합 폭발 — 앙상블 규칙 없이 스칼라 보고량이 정의되지 않는다 (CLAUDE.md 보고량 판정 기준) |
| **양이온이 여는 음이온 무질서** | Kraft 2018 (Ge → I/S) | Nd@P / Nd@Li 트랙의 4a/4d 점유 변화 미측정 | 기존 MD 궤적에서 음이온 자리 점유를 세는 사후분석이면 새 계산 없이 볼 수 있을지 모른다 (가능성 메모) |

### 11-iv. ⛔ 이 리뷰에서 인용하면 안 되는 것

1. **"할라이드 치환이 산화 한계를 4.8 V 이상으로 올린다"** (p.18) — 축 없음 · 자기 p.24 와 모순 · 근거가 일반 리뷰(ref 29).
2. **`Table 1` '창' 열 다섯 칸** — 겉보기 CV 창.
3. **`Table 1` 의 σ·Ea 를 서로 비교하는 것** — σ₀ 다섯 자릿수 산포 · 측정 조건 상이.
4. **`Table 1` 2행(Li₅.₄PS₄.₄Cl₁.₆ 20.2 mS cm⁻¹ · 0.407 eV)을 우리 modelc 의 실험 앵커로** — 원전(ref 228) 미독 · 홉 검산 모순 · 같은 조성 3.3 mS cm⁻¹ 보고(Adeli) 존재.
5. **VBM 하강 기전 문장** (p.11, p.14, p.18, p.23, p.37) 과 그 근거 ref 152·154 (페로브스카이트).
6. **"Cl⁻ 는 S²⁻ 보다 크고 더 분극된다"** (p.9) · **"Li₇PS₆ → Li₆PS₅Cl 은 S 공공"** (p.11) · **"전기음성도↑ → Li 와 더 공유적"** (p.22) · **"할라이드가 VBM 을 내려 Li 금속 환원을 막는다"** (p.15).
7. **"Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ = argyrodite"** (p.36).
8. **`Fig. 3` 레이더 값** · **`Fig. 15` 로드맵 수치(Wh kg⁻¹ · 연도)**.
9. **`Fig. 12e` 캡션 "Cl 이 장벽을 낮춘다"** · **`Fig. 13e` "phase-pure"** · **`Fig. 13a` Li₆PS₅I 점** · **Kim 2026 "E 12.37 GPa"** · **Lu 2025 "1500 h @0.5 mA cm⁻²"** (원전 800 h @0.5 · 2000 h @0.2) · **"LGPS O 치환 Ea 0.17 → 0.36"**.
10. **"62 % Cl on inner 4c sites"** 를 리뷰 출처로 — 원값은 Kraft 2017, 정의와 함께 그 원전에서 인용.
11. **이 리뷰의 인용 번호를 원전 확인 없이** — §12a 의 역할 불일치가 다수다.

---

## 12. 원전 대조표

### 12a. 리뷰가 인용한 원전 중 우리가 이미 digest 한 것 (DOI·서지 대조)

| ref | 우리 slug | 리뷰가 쓴 역할 | 판정 |
|---|---|---|---|
| 25 | `famprikis2019_fundamentals_inorganic_sse` | "황화물이 산화물보다 Ea 낮다" | ✅ 맞게 씀 |
| 58 | `richards2016_interface_stability_pseudobinary` | "음이온 치환 + 계면개질의 상승효과" (p.3) | ⚠ 느슨 — 원전은 pseudo-binary 계면 열역학 |
| 64 | `okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces` | "황화물이 산화물보다 σ·**전기화학 안정성** 우수" (p.3) | 🔴 자기 p.24 와 모순되는 문장의 근거 |
| 92 | `morgan2021_anion_disorder_superionic_mechanism_li6ps5x` | Cl/Br 무질서 고용체, I 질서 | ✅ (원전은 4a/4c 표기) |
| 135 | `adeli2019_halide_substitution_boosting_argyrodite` | 저에너지 경로 · **"할라이드가 P–S 공유성을 낮춰 S²⁻ 환원 구동력↓"** | 🔴 우리 digest 에 P–S 공유성·환원 구동력 서술 없음 · 대칭셀 증거 약함(digest §9) — 역할 과장. 그리고 **x = 0.6(우리 modelc) = 3.3 mS cm⁻¹ · LiCl 석출**을 리뷰는 안 실었다 |
| 137 | `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` | σ₀ 트레이드오프 · Cl₀.₅Br₀.₅ 최적 | ✅ 정확 · ⚠ I 반등 누락 · 62 % 를 다른 번호로 |
| 147 | `ong2013_lgps_family_substitution` | 큰 할라이드 → 팽창 (p.12) | ⭕ — 그러나 O 치환 Ea 값(p.10)은 이 원전 값인데 [93, 127] 로 인용하고 짝도 틀림 |
| 153 | `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` | 다음이온 혼성 → 공간전하층 | ⭕ 공간전하층 원전으로는 맞음 (혼성 준위 주장의 근거는 아님) |
| 160 | `rao2011_argyrodite_se_studies_bvse` | **Cl/Br 아지로다이트가 LiCl/LiBr 자기제한 SEI** | 🔴 우리 digest 전문에 Li 금속·SEI 서술 0 — 합성 + BV 이동망 논문 |
| 164 | `lu2025_tailoring_cl_rich_anode_licl` | Cl15 LiCl SEI · 4d 90.01 % · NMR | ⭕ 기전 맞음 · 🔴 대칭셀 1500 h @0.5 는 원전(800 @0.5 · 2000 @0.2)과 다름 |
| 172 | `liu2024_pband_center_sbo_dual_interface` | ε_p 하강 → 양쪽 계면 안정 | ⚠ "음이온 치환" 으로 분류(실제론 Sb@P 효과) · ε_p 기준 문제 미언급 |
| 173 | `sakuda2013_sulfide_mechanical_property` | "E 10–25 GPa" | ⚠ 원전 18–25 GPa (유리) |
| 191 | `deng2016_elastic_superionic_electrolytes_dft` | "무른 격자가 저장벽 홉을 허용" (수송 문장) | ⚠ 원전은 탄성텐서 논문 — 정작 기계 절에서 안 씀. 원전 PBEsol Li₆PS₅Cl E 22.1/G 8.1 ≈ 우리 relaxed-ion comp1 22.06/8.13 (`deng2016` digest) |
| 197 | `banik2022_substitutions_oxidative_stability_argyrodite` | **"O·F 치환이 VBM 을 내려 산화안정↑"** (p.23, refs 196·197) | 🔴 **반대 방향 인용** — 원전 결론은 "P→Si/Ge · Cl→I 치환은 산화안정을 거의 못 바꾼다(VBM = S)". O·F 를 직접 시험한 논문도 아니다 |
| 206 | `gilgonzalez2022_synergistic_cl_constricted_esw` | Cl-rich · 기계 구속 창 · 대칭셀 · 다층 | ⭕ 대체로 맞음 · ⚠ 반전 결론(Cl1.0 의 moderate instability) 축소 · 55 °C 누락 |
| 208 | `ma2024_sb_doping_lpsc_conductivity` | LSSSI 다원소 도핑 | ⭕ (측정 온도 30 °C 를 본문이 생략) |

### 12b. 꼭 읽어야 할 빠진 원전 (리뷰 참고문헌에서 — 우리 축 기준 우선순위)

| 우선 | ref | 원전 | 왜 |
|---|---|---|---|
| **P1** | 228 | Chen *et al.* 2023 *Chem. Commun.* 59, 7220 "20 mS cm⁻¹ Li-argyrodite SE produced via facile high-speed-mixing" (DOI 10.1039/D3CC01387A) | **우리 modelc 와 똑같은 조성**의 실험값. 단일상인가(XRD/Rietveld) · Ea 0.407 eV 의 온도구간·성분 · σ–Ea 홉 검산 모순의 원인 확인. modelc 단일상 가정의 근거/반례 |
| **P1** | 139 | Hwang *et al.* 2024 *ACS Nano* 18, 23320 "Oxygen Substitution to Enhance Chemo-Mechanical Stability at the Cathode–Sulfide Electrolyte Interface" | **O 치환 계산의 최근접 선행** — 모체가 우리 comp2 조성(LPSBC), O 치환판이 LPSOBC. 그들의 범함수·계면 모형·O 자리가 우리 LPSOCl 과 같은가 · "산화 억제" 가 B① 인지 B③ 인지 |
| **P1** | 193 | Feng *et al.* 2020 *Energy Storage Mater.* 30, 67 "Enforcing Structural Disorder in Li-deficient Argyrodites Li₆₋ₓPS₅₋ₓCl₁₊ₓ" | Cl-rich/Li 결손 = modelc 계열의 무질서 정량 · 우리 modelc 배열 선택의 실험 기준 |
| **P1** | 61 | Banerjee & Tkatchenko 2025 *Nat. Commun.* 16, 1672 "Non-local interactions determine local structure and lithium diffusion in solid electrolytes" | `Fig. 5a,b` 의 원전. **비국소(분산) 상호작용이 국소구조·확산을 정한다** 는 주장 — 우리 PBE(분산 보정 여부) 구조·탄성 결과에 대한 방법 견제가 될 수 있다 |
| P2 | 212 | Patel *et al.* 2021 *Chem. Mater.* 33, 1435 `Li₆₋ₓPS₅₋ₓClBrₓ` | Br 판 modelc — 빈칸 1순위 (§11-iii) |
| P2 | 131 | Chien *et al.* 2024 *Chem. Mater.* 36, 382 "Li sublattice engineering" | `Fig. 4f` 장벽의 계산법 · Cl doublet 불일치 판정 |
| P2 | 169 | Raj *et al.* 2025 *ACS AMI* 17, 48195 "Role of Oxygen Substitution … LGPS-Structured Oxy-Sulfide" | O 치환의 σ·공기·계면 효과를 한 계에서 — LPSOCl 서사의 문헌 근거 |
| P2 | 176 | Kato *et al.* 2014 *J. Ceram. Soc. Jpn.* 122, 552 (Li₂S–P₂S₅–P₂O₅ 유리 E) | "O → 강성↑" 의 실측 앵커 (우리 LPSOCl B₀·E_VRH 방향과 같은 축) |
| P2 | 198 | Gorai *et al.* 2020 *J. Mater. Chem. A* 8, 3851 (LGPS 결함 앙상블) | 무질서계 보고량을 **분포로 정의**하는 계산 선례 — 우리 disorder_ensemble 보고 규율의 외부 짝 |
| P2 | 220 | Maus *et al.* 2025 *Adv. Energy Mater.* 15, 2403291 (Li₅.₅PS₄.₅Cl₁.₅ 후처리) | Cl-rich 의 공정 의존성 (같은 조성 6배 산포의 해석) |
| P3 | 166 | Golov & Carrasco 2023 *ACS Energy Lett.* 8, 4129 (Li₆PS₅₋ₓSeₓCl SEI 계산) | Se 빈칸 |
| P3 | 184 | Kim *et al.* 2026 *J. Mater. Chem. A* 14, 9939 (I-rich LMA, E·CCD) | E 측정법 확인 (`Fig. 9b` 12.37 불일치) |
| P3 | 210 | Kraft *et al.* 2018 *JACS* 140, 16330 (Ge-Li₆PS₅I) | "무질서가 주원인" 판정 — 원전이 Li 증가 효과를 어떻게 갈랐나 |
| P3 | 140 | Minafra *et al.* 2020 *Inorg. Chem.* 59, 11009 (Li₆PS₅X 국소 전하 불균일) | 무질서 정의·정량법 |
| P3 | 199 | Swamy *et al.* 2019 *Chem. Mater.* 31, 707 (황화물 산화환원 거동) | p.24 "2–3 V" 의 실험 원전 · B① vs 겉보기 |

---

## 13. 적용 인사이트 (가장 날카로운 셋)

1. **우리 원고가 이 리뷰를 그대로 인용하면 B 축에서 자기모순을 산다.** 리뷰의 "할라이드·O → VBM↓ → 산화안정↑(>4.8 V)" 는 우리 B①(comp1 = modelc 2.256 V · VBM S 3p 불변)과 정면으로 어긋난다. 반대로 **우리 결과는 리뷰가 놓친 구분을 정확히 채운다** — "Cl 은 B② 를 넓히고 B① 은 못 움직인다, O 는 강성과 갭을 바꾸지만 VBM 성격은 못 바꾼다." 이 문장이 우리 '음이온 공학' 서사의 중심이 될 수 있다.
2. **`Table 1` 2행이 우리 modelc 조성의 문헌 실험값인데 신뢰할 수 없는 쌍이다.** 같은 조성이 3.3(Adeli) ↔ 20.2(Chen) mS cm⁻¹ 로 6배 갈리고, Chen 쌍(20.2 · 0.407 eV)은 홉 수 검산과 700–1600배 어긋난다. 우리 modelc 를 "산업 표준 고전도 조성의 계산 모형" 으로 소개할 때 **실험 앵커는 원전(ref 228)을 읽고 나서** 고른다 — 그 전엔 `adeli2019` 의 "단일상은 공정 의존 가정" 문장이 우리 쪽 정직한 서술이다.
3. **'음이온 공학' 의 다음 질문은 우리 데이터 안에 이미 있다**: Cl-rich 에서 E_VRH↑·B₀↓ 가 갈리는 것은 리뷰의 크기·분극률 규칙 밖이고(§9c), +B₂O₃ 의 갭 축소는 "O → 창 확대" 의 반례다(§9d). 둘 다 **"음이온만 보지 말고 공공·동반 양이온이 만드는 상태를 같이 보라"** 는 같은 교훈이다 — 리뷰의 기능 분리 원리에 대한 우리 쪽 단서다.

---

## 14. 인용 가능 문장 (영문 초안 — 리뷰를 '지도' 로만 쓰는 형태)

- "Anion engineering of sulfide electrolytes — halide enrichment, oxygen substitution, multi-anion frameworks, and anion–cation co-doping — has been reviewed recently as a route to decouple conductivity, stability, and mechanics (Nosrati et al., *Small* 2026, e76005)." *(서론 지도 문장 — 수치 없음)*
- "Increasing lattice softness lowers the activation barrier but also the Arrhenius prefactor (Kraft et al., *JACS* 2017), so that the conductivity optimum lies at intermediate stiffness." *(원전 Kraft 로 인용 — 리뷰는 '참고' 만)*
- "Reported conductivities of the same nominal Cl-rich argyrodite composition differ by about a factor of six depending on processing (e.g., Li₅.₄PS₄.₄Cl₁.₆: 3.3 mS cm⁻¹ with LiCl segregation vs. 20.2 mS cm⁻¹ after high-speed mixing and sintering)." *(⚠ 두 원전(Adeli 2019 · Chen 2023)을 직접 인용 — Chen 원전 확인 후에만)*
- ⛔ 리뷰를 근거로 "halide/oxygen substitution raises the oxidative stability limit" 를 쓰지 않는다.

---

## 15. 주의 / 한계 (인용 규율)

- 이 digest 의 **리뷰 수치는 전부 2차 인용**이다. 원고에는 원전을 직접 인용한다 (§12).
- **figure-read 값**(`Fig. 4f` · `Fig. 5d` · `Fig. 9b` · `Fig. 12f` · `Fig. 13f` · `Fig. 14a,f` 등)은 재수록 그림을 다시 읽은 것이라 원전 그림보다 해상도가 낮다. 불일치 판정(§10-7)은 확대 재렌더로 확인했지만 **원전 그림으로 다시 확인하기 전에는 '리뷰 재수록본 기준' 이다.**
- **우리 산수**(§4c 홉 검산 · σ₀ 역산 · NE 역환산)는 ν₀ = 10¹³ s⁻¹, T = 298 K, Haven = 1, a ≈ 9.80 Å, 홉 길이 2–3 Å **가정**이다. 차수 검산이지 물성값이 아니다.
- 우리 값: gap·B₀·E_VRH·ICOHP·ESW onset·환원 가장자리는 registry canonical (E_VRH 계 간 비교는 CONDITIONAL — 방향까지). **MD 값은 절대값을 하나도 쓰지 않았다.** LPSOCl ↔ modelc 의 MD 차를 O 효과로 읽는 것은 원장 금지다.
- 트랙 표기: ESW · 탄성 · 우리 DFT 기준선 → 1저자 = 사용자. li2s(`Fig. 10c–e` Li₂S 결함화학 언급) → **외부 1저자** — 여기서는 원전 후보로만 적었고 판단하지 않았다. CEI(Nd 계면) → 실험 쪽 1저자 — 이 리뷰에 Nd 가 없어 해당 없음.

---

## 16. 기법·용어 미니사전

- **음이온 공학 (anion engineering)** — 이 리뷰의 정의: 음이온 부격자 전체(종·배열·공공·동역학)를 설계 변수로 보는 것. 양이온 치환이 음이온 무질서를 *유도*하는 경우(Ge→P)까지 포함시킨다.
- **4a / 4d (또는 4c) 자리** — F4̄3m 아지로다이트의 두 음이온 자리. 할라이드 기본 자리 4a, 자유 S²⁻ 자리 4d — 원점 선택에 따라 같은 자리를 4c 로 부른다 (Morgan 2021·이 리뷰 p.12). **자리 무질서율** = 할라이드가 S²⁻ 자리에 앉은 분율(Kraft 정의, 50 % = 무작위).
- **doublet / intra-cage / inter-cage 홉** — 48h–24g–48h(같은 24g 를 사이에 둔 짝 자리) / 같은 케이지 안 48h–48h / 케이지 사이(48h–16e–48h 또는 48h′–48h′). 가장 높은 홉이 장거리 수송을 정한다.
- **전지수 σ₀ 와 Meyer–Neldel 보상** — σT = σ₀·exp(−Ea/kT). 무른 격자는 Ea 와 σ₀ 를 함께 낮춰 σ 의 이득을 상쇄한다 (Kraft 2017). log σ₀ ∝ Ea 의 선형 관계 = Meyer–Neldel.
- **홉 수 검산** — Γ = ν₀·exp(−Ea/kT) (ν₀ 10¹³ s⁻¹ 가정), 1/Γ = 평균 대기. 장벽으로 "빠르다/느리다" 를 말할 때 차수 모순을 거른다 (`D-2026-09-27-barrier-hop-count`).
- **밴드 정렬 모형 vs 열역학 분해창** — 전자가 전극↔SE 로 넘어가는 문턱(VBM/CBM)으로 창을 보는 그림 vs 그랜드 퍼텐셜에서 분해 반응이 열리는 전위로 보는 그림. 후자가 훨씬 좁고(우리 B①), 우리는 후자를 쓴다.
- **B① ~ B④ (우리 산화 4축)** — ① 0 압력 열역학 onset(층①) ② 기계 구속 창 ③ 양극 계면 반응 ④ 열·수분. "산화에 안정" 은 축 이름 없이 쓰지 않는다.
- **p-밴드중심 ε_p** — PDOS 의 1차 모멘트. 절연체에서 기준을 E_F 로 잡으면 E_F 위치가 비유일해 비교가 흔들린다 (`liu2024` digest).
- **HSAB (soft acid)** — 무른 양이온(Sn⁴⁺·Sb⁵⁺·Bi³⁺)이 무른 염기 S²⁻ 와 강하게 결합해 가수분해를 늦춘다는 경험칙.
- **Brouwer 도표** — 도펀트 농도·온도에 따른 결함 농도 영역도 (내재 / 외인 / 회합).
- **공간전하층(SCL) 모형** — 입자 표면의 전하층에 치환 결함이 모여, 작은 입자일수록 고용한계가 커진다는 설명 (Choi 2025).
- **CCD (critical current density)** — Li 대칭셀에서 단락 직전 전류밀도. 측정 프로토콜(단계 시간·용량·압력) 의존이 커서 논문 간 비교가 어렵다.
