# Regulation of the Lattice Dynamics of Li₂ZrCl₆ Solid Electrolytes via Low-Ion-Potential Element Doping for All-Solid-State Batteries — Yuan Ren (Authorea preprint 2026)

> slug `ren2026_li2zrcl6_low_ion_potential_doping` · DOI `10.22541/authorea.15005774/v1` · type `exp + DFT/AIMD/NEB/phonon` ·
> 본문 PDF `80a8e6ce` (Authorea 표지 2 pp + 원고 29 pp = 31 pp) + **SI `205249ff`.docx**(Fig S1–S20 캡션 · Table S1–S6 · eq 1–5 · ref 1–19) 전문 정독 · digested `2026-07-28` · **2차 패스(본문 그림 픽셀 독립 검증) `2026-08-04` → §20** · status ✅
> elements: Li, Zr, Cl, Er, Nd
> methods: DFT, AIMD, NEB, phonon, XPS, Raman
>
> **저자** Yuan Ren\*(교신, `yuanren@imust.edu.cn`), Dewang Fu, Wenke Feng, Yixiao Zhai, Anning Song, Pan Zhang, Chengyu Zhang, Yan Li, Chao Zhang
> — **Inner Mongolia University of Science & Technology**(内蒙古科技大学, Baotou 014010), School of Mechanical Engineering (Chao Zhang만 School of Life Science and Technology)
> 자금: NSFC **52162033** · 내몽고 청년과기인재 NJYT24004 · 내몽고자연과학기금 2024LHMS05050 · JG2025034C · 2024QNJS006
> Posted **2026-07-07**, Authorea. Wiley 원고 템플릿("Article category: Full Paper / Subcategory: Lithium Ion Batteries", Received/Revised/Published online **공란**).

---

## ⛔⛔ 최우선 규율 — 이 문서를 인용할 때마다 읽을 것

> ### 1. **동료심사 전 프리프린트다.**
> Authorea 각 페이지 하단 원문: *"This a preprint and has not been peer reviewed. Data may be preliminary."*
> **이 digest에서 나오는 모든 수치·주장은 "Ren et al., Authorea 프리프린트(동료심사 전), 2026" 을 병기해야 한다.**
> deck·원고·메일 어디에도 peer-review 통과 결과처럼 쓰지 않는다. §17 인용 문장은 전부 이 꼬리표를 달고 있다.
>
> ### 2. **할라이드다. 우리는 황화물이다.**
> Li₂ZrCl₆ = **염화물(halide) SE**. 우리 캠페인 = **황화물 argyrodite Li₆PS₅Cl**.
> 음이온 화학(Cl⁻ 1가 vs S²⁻ 2가)·전하·배위·골격 위상이 전부 다르다.
> **σ / Ea / D / 격자상수 / 장벽 / 응집에너지 — 이 논문의 어떤 절대값도 우리 물성 4축에 편입 금지.**
> (`litdb/INDEX.md` ⚠EXTERNAL 규율 + `kim2025_li3ycl6` digest 선례 준용.)
>
> ### 3. **σ 절대값 인용 금지 — 비율만.** 그리고 그 비율조차 §6.6·§6.7의 조건부다.
>
> ### 4. 이 digest에는 **우리가 직접 한 재계산(§4.2 · §6.3 · §6.7 · §7.4 · §20 전체)** 이 들어 있다.
> 논문에 인쇄된 값과 **우리 검산값**을 반드시 구분해서 인용할 것. 재계산 절차는 전부 본문에 적어 뒀다.
>
> ### 5. ⛔⛔ **2026-08-04 2차 패스(§20) 를 읽기 전에는 이 논문의 어떤 수치도 인용하지 마라.**
> 그림 픽셀 실측 결과 **헤드라인 Eₐ(0.163 eV)가 Methods 에 없는 500 K 잡음점이 만든 인공물**로 확정됐고,
> **NEB 장벽은 정방향 반쪽 값**이며, **EIS 셀 상수가 명시 기하와 2.56배 어긋난다.**
> **최종 인용 규율은 §20.11 하단 박스**에 정리돼 있다 — 그게 이 문서의 정본 규율이다.

---

## 0. 이 digest를 읽는 법 — 우선순위 지도

사용자가 지정한 6개 질문에 맞춰 분량을 배분했다.

| 질문 | 답이 있는 절 | 한 줄 답 |
|---|---|---|
| ① **"ion potential" 정의식**은? | **§4.1–4.2** | **Φ = Z/r 그 자체**(Z=양이온 형식전하, r=해당 배위의 Shannon 이온반경, **단위는 pm⁻¹**). Table S6 18계 전값을 우리가 **Shannon 반경으로 전수 역산 검증 완료** — 예외 없이 일치 |
| ② lee2024 **inductive effect와 같은 축인가** | **§4.4** ★★ | **같은 축 · 반대 부호 · 다른 인과경로.** 축(=중심양이온이 음이온을 얼마나 세게 붙드는가)은 동일하고, 이 논문의 ref[28][29]가 인용하는 "고-Φ → M–Cl 공유성↑ → Cl⁻ 유효전하↓" 논리는 **문자 그대로 inductive effect다**. 그런데 이 논문은 **정반대(저-Φ)** 를 처방하고, 인과경로도 *정전기(전하)* 가 아니라 *동역학(격자 유연성)* 이다. **Bader/COHP를 한 번도 계산하지 않아** 두 경로를 자기 데이터로 구별하지 못한다 |
| ③ **z/r 이 값싼 대리지표가 되는가** | **§4.5** ★★ | **안 된다.** 그들 자신의 Table S6(18계)에서 **Pearson r = −0.255 (R² = 0.065), Spearman = −0.089** — Φ가 σ 분산의 **6.5 %** 만 설명한다. 같은 Φ=0.0781에서 Ta 1.42 vs Nb 0.55(2.6배). **Li 함량이 훨씬 나은 예측자**(Spearman +0.628) |
| ④ **lattice dynamics** — 우리 공백 축에 뭐가 들어오나 | **§7** ★ | **개념 1개 + 서술자 1개는 진짜 수확**: 원소분해 **VDOS(phonon DOS)** 와 **⟨ω⟩ = ∫ω g(ω)dω / ∫g(ω)dω (VDOS 1차 모멘트)**. 단 **⟨ω⟩ 값은 논문 어디에도 없고**, 분산곡선·허수모드 점검·Debye 온도·열용량 전부 없음. DFPT와 유한변위(0.01 Å)를 **동시에** 적는 방법 서술 모순 |
| ⑤ σ 방법과 신뢰도 (**AIMD 27× 편향 이력**) | **§6** ★★ | AIMD(VASP/PBE/+U/Γ/2 fs/**50 ps**/600–900 K 4점/NVT-NH) → NE(Haven=1) → 300 K 외삽. **우리 검산: 600–900 K 실측 구간에서 11개 조성 D 분산은 2.3–3.6배뿐인데, 300 K로 외삽하면 29.6배로 벌어진다.** 즉 헤드라인 격차는 **외삽이 만든 것**. Meyer–Neldel 보상선 R²=0.93·E_MN=57 meV≈시뮬 창의 kT |
| ⑥ **Li₃YCl₆(kim2025)와의 관계 · 차원성** | **§9** ★★ | **같은 P3̄m1 Li₃YCl₆형 골격**이다. kim2025 hcp_1이 **1D(c축)** 이라 한 그 골격 — 이 논문 Fig 3a가 pristine LZC에서 **MSD_a≈MSD_b≈0, MSD_c만 상승** 으로 독립 재확인. **도핑이 차원성을 1D→2D(Er)/준-3D(Nd)로 올린다**(Fig 3b·3c). 논문은 이 프레임을 쓰지 않는다 = **우리가 얹는 해석** |
| ⑦ 이식 가능 / 금지 | **§15** | 가능 = ⟨ω⟩·VDOS 서술자·Oct–Tet–Oct 어휘·Φ의 *반례로서의* 가치·MSD 축분해 / 금지 = 전 절대값·"저-Φ가 좋다" 명제·volcano 서사·Nd 결과의 우리 Nd로의 이전 |
| ⑧ ★★★ **그림을 실물로 재보면** (2026-08-04 추가) | **§20** ★★★ | **1차가 남긴 3건 확정 + 신규 5건.** 핵심: **(a)** Fig 3d/3e y축이 `ln(D)` 라벨인데 실제는 **log₁₀(D)**(4자리 일치 3건). **(b)** Methods 에 없는 **500 K 점이 12/12 계열에 존재**하고 ±1.3 dex 로 흩어진다. **(c)** 헤드라인 Er0.5 는 **D(500 K) > D(600 K)** — 냉각하니 빨라진다(불가능). 그 점을 빼고 600–900 K 만 쓰면 **Eₐ = 0.372 eV**, 이는 **같은 논문 NEB 0.370 eV 와 0.5 % 일치** → **인쇄 Eₐ 0.163 은 인공물이고, §8.2-4 의 "정적 NEB 과대" 판정은 이 조성에 한해 철회**. **(d)** EIS 셀 상수가 명시 기하(16 mm)와 **2.56배** 안 맞는다. **(e)** 도핑 시료 XRD 날카로운 선 4/4 가 **fcc LiCl 위치** → "불순물 없음"·"저각 이동" 주장 흔들림 |

---

## 1. 한 줄 요약

**"Li₂ZrCl₆의 Zr⁴⁺를 이온퍼텐셜(Φ=Z/r)이 더 낮고 반경이 더 큰 희토류 Er³⁺/Nd³⁺로 aliovalent 치환하면 ① 전하보상으로 Li⁺ 캐리어가 늘고 ② M–Cl 결합이 약해져 Cl⁻ 골격이 물러지며(저주파 포논↑) ③ Li 이동이 Oct–Oct 직접 도약에서 Oct–Tet–Oct 협동 경로로 바뀌어 장벽이 내려간다"**
— 실험 σ_RT는 pristine 0.227 → **Er 1.32 / Nd 1.13 mS cm⁻¹**(≈5–6배), NCM811 전고체셀 100 cyc 82.5 % 유지.
**단 이것은 동료심사 전 프리프린트이고, ②의 전자적 근거(음이온 전하)는 한 번도 계산되지 않았으며, 핵심 서술자 Φ는 그들 자신의 18계 표에서 σ를 거의 설명하지 못한다(§4.5).**

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 물질 | **Li₂₊ₓZr₁₋ₓMₓCl₆ (M = Er³⁺, Nd³⁺; x = 0, 0.125, 0.25, 0.375, 0.5, 0.625)** — 모체 Li₂ZrCl₆ (LZC) |
| 최적 조성 | **Li₂.₅Zr₀.₅Er₀.₅Cl₆ (x=0.5)** · **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆ (x=0.375)** |
| 골격 | **P3̄m1** (본문 §2.1 명시). XRD 주피크가 **Li₃YCl₆형 (PDF#44-0286)** 과 일치 |
| 연구유형 | **exp + 계산 혼합.** 계산 = DFT 정적완화 + AIMD + NEB + phonon(VDOS); 실험 = 기계화학 합성 + XRD/Rietveld + XPS + Raman + SEM-EDS + EIS + 전고체셀 |
| 계산 조성 수 | **11개**(pristine + Er 5 + Nd 5) — 전부 AIMD |
| 실험 시료 수 | **5개**(pristine, Er x=0.25, Er x=0.5, Nd x=0.25, Nd x=0.375) |
| 출판 상태 | **⛔ Authorea 프리프린트, 동료심사 전** (Wiley 원고 템플릿 상태, Received/Revised 공란) |
| 우리 db 내 위치 | `db/properties/nd_substitution_survey_index.json` **#053** (system_class `halide_Li`, n_not_discussed 9) |

**litdb 안 이웃**:
- `papers/kim2025_li3ycl6_new_crystal_structure.md` — **같은 P3̄m1 Li₃YCl₆형 골격**, 같은 AIMD-NE 파이프라인, 같은 1D 차원성 문제. **직계 대조군**(§9).
- `papers/schlem2020_li3mcl6_cation_site_disorder.md` — 같은 삼방 할라이드 Li₃MCl₆(M=Y,Er), **Er을 다루는 유일한 다른 digest**.
- `papers/lee2024_multicomponent_argyrodite_mixed_oxidation_mtp.md` — **inductive effect 정량화**(§4.4의 상대).
- `papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` — **격자 무름 ↔ σ 실험 원전**(§7.5에서 이 논문과 정면 충돌).
- `papers/cha2024_dualcompatible_halide_ncm_lpscl_interface.md`(우리 db 기록상 LZC 코팅) — 같은 물질 LZC.

---

## 3. 문제 설정 — 저자들이 무엇을 반박·확장하려는가 (§1 Introduction)

### 3.1 출발점
- 할라이드 SE = **고전압 양극 호환 + 산화안정성 우수**. 그중 **Li₂ZrCl₆(LZC)** 는 Zr 자원이 흔하고 원료가 싸서 저비용 후보.
- **그러나** LZC는 *"rigid anion framework and limited Li⁺ carrier concentration"* 때문에 σ_RT가 **0.40 mS cm⁻¹뿐**(본문 §1이 [12,13]에서 소환한 값).
- 기존 개량 전략 3계열: **음이온 도핑**(O²⁻/S²⁻)[14,15] · **금속 양이온 도핑**(Al³⁺/Fe³⁺/Ca²⁺)[16–18] · **양이온 치환**(In³⁺/Sc³⁺/Bi³⁺/Nb⁵⁺)[19–22].
- 저자들의 비판: *"most of these strategies focus mainly on a **single structural size effect or charge-compensation effect**, and insufficient attention is given to the **coupling relationships among central cation–anion interactions, the dynamic response of the anion framework, and the Li⁺ migration barrier**."*

### 3.2 서술자 도입의 계보 (그대로 옮김 — 이게 §4의 근거다)
- **[24] Wang/Janek/Wagemaker, Nat. Commun. 2024, 15, 1050** — 이온퍼텐셜 기반으로 스크린·합성한 **고엔트로피 층상 할라이드 Li₂.₈In₀.₂Sc₀.₂Yb₀.₂Lu₀.₂Zr₀.₂Cl₆**, σ 2.13 mS cm⁻¹, multication synergy로 3D 균질 확산.
- 그 위에서 정의: *"the **ionic potential (Φ = Z/r**, where Z is the cation valence state and r is the ionic radius in the corresponding coordination environment) can serve as an important descriptor…"*
- *"Ionic potential reflects the **surface charge density and polarization ability** of ions and couples valence-state and spatial-scale information. Therefore, it can **qualitatively** describe the **Coulombic binding strength of central cations to the Cl⁻ anion framework**."*
- *"Notably, **higher or lower ionic potential is not inherently better**; rather, ionic potential ultimately affects ionic transport properties by regulating central cation–anion interactions and the local Li⁺ potential field."*
  > 🔑 이 문장은 **저자 스스로 단조 관계를 부정한 것**이다. 그런데 §2.3에서는 *"negatively correlated"* 라 쓴다(§4.5의 모순).

### 3.3 **반대 진영(고-Φ 노선)을 명시적으로 인용한다** ★ — 여기가 lee2024와 만나는 지점
> *"**Zhou et al.** reported that **high-ionic-potential cations indirectly weaken Li–Cl coupling by regulating the anion electronic environment**, thereby reducing the Li⁺ migration energy barrier.[28]
> **Li et al.** further demonstrated that **high-valence and highly electronegative cations enhance M–Cl covalency and reduce the effective negative charge of Cl⁻**,[29] thereby improving the flexibility of the anion framework and promoting Li⁺ diffusion."*
> — [28] X. Zhou et al., *Energy Storage Mater.* **2026**, 88, 105131 · [29] R. Li et al., *JACS* **2026**, 148, 3114

> ⚠⚠ **[29]의 문장은 `lee2024` §3a의 inductive effect와 문자 그대로 같은 명제다**:
> "고원자가 양이온 → M–X 공유성↑ → X⁻ 유효 음전하↓ → X–Li 상호작용 약화 → Li 확산↑".
> lee2024는 이걸 **Bader 전하로 정량화**했다(Si⁴⁺ 중심 S −1.48 e⁻ vs W⁶⁺ 중심 S −0.84 e⁻).

### 3.4 저자들의 반전(그리고 그 논증 구조)
> *"such strategies usually rely on strong M–Cl interactions or high-valence cation substitution, which may be accompanied by **reduced Li⁺ content, decreased carrier concentration, or increased elemental cost**. Therefore, they make it difficult to simultaneously achieve high carrier concentration and fast Li⁺ migration.
> In contrast, **low-ionic-potential cations weaken central cation–anion interactions, enhance the dynamic polarization ability of the anion framework, and induce lattice softening**, thereby reducing the migration energy barrier **while increasing the Li⁺ carrier concentration**."*

**논증을 분해하면 3단이다:**
1. **캐리어 항** — 고-Φ(=고원자가) 치환은 전하중성 때문에 Li를 **뺀다**(Li₂ → Li₁.₇₅). 저-Φ(=저원자가) 치환은 Li를 **넣는다**(Li₂ → Li₂.₅). ← **이건 논리적으로 맞다.**
2. **이동도 항** — 저-Φ → M–Cl 약화 → Cl⁻ 골격이 물러짐 → 장벽↓. ← **이게 새 주장이고, §7에서 phonon으로 뒷받침하려 한다.**
3. **결론** — 그러므로 저-Φ가 두 마리를 다 잡는다.

> ⚠ **2번이 이 논문의 유일한 신규 물리 주장이고, 1번은 aliovalency의 자명한 산술이다.**
> 그리고 §4.5·§6에서 보듯 **데이터가 실제로 지지하는 것은 1번뿐**이다.

### 3.5 Fig 1 — 설계 도식(그림 하나로 논문 전체가 요약된다)
- **위 패널(Pristine LZC)**: [ZrCl₆]²⁻ 팔면체 사이를 Li가 **Direct Oct–Oct migration**(보라 점선) → *"Strong Zr–Cl interaction / Rigid Cl⁻ framework"* → 오른쪽에 **단일 높은 봉우리** 장벽 곡선(High barrier).
- **아래 패널(Er³⁺/Nd³⁺-doped)**: 초록 팔면체([ErCl₆]³⁻/[NdCl₆]³⁻)가 섞이고 **Relay Oct–Tet–Oct migration** → *"Weakened M–Cl interaction / Softened, polarizable Cl⁻ framework"*(파동 기호) → 오른쪽에 **여러 개의 낮은 봉우리**(Lower distributed barriers).
- 🔑 **"하나의 큰 봉우리 → 여러 개의 작은 봉우리"** 라는 이 그림 문법은 우리 `[Dyre]`(dc Ea = percolation 병목)·`li_percolation F*` 서사와 **같은 언어**다. §8·§15에서 다시 쓴다.

---

## 4. ★★ 최우선 질문 ① — "ion potential"의 실체 완전 해부

### 4.1 정의식 (원문 그대로, 이게 전부다)

> **Φ = Z / r**
> *"where Z is the cation valence state and r is the ionic radius in the corresponding coordination environment"* (본문 §1)

논문이 정의하는 것은 **이 한 줄뿐이다.** 배위수·반경표 출처(Shannon?)·단위 — 전부 미기재.

### 4.2 ★ 우리 역산 검증 — 단위와 반경표를 확정했다

Table S6에 18계의 Φ가 인쇄돼 있다. 우리가 **Shannon 6배위 이온반경(pm)** 으로 Z/r을 계산해 전수 대조한 결과:

| 치환 양이온 | 논문 Φ (Table S6) | Z / r(VI, pm) | 일치 |
|---|---:|---|:--:|
| Zr⁴⁺ (pristine) | 0.0556 | 4 / 72 = 0.05556 | ✓ |
| Al³⁺ | 0.0561 | 3 / 53.5 = 0.05607 | ✓ |
| Fe³⁺ | 0.0465 | 3 / 64.5 = 0.04651 | ✓ |
| Mg²⁺ | 0.0278 | 2 / 72 = 0.02778 | ✓ |
| Zn²⁺ | 0.0270 | 2 / 74 = 0.02703 | ✓ |
| Ca²⁺ | 0.0200 | 2 / 100 = 0.02000 | ✓ |
| In³⁺ | 0.0375 | 3 / 80 = 0.03750 | ✓ |
| La³⁺ | 0.0291 | 3 / 103.2 = 0.02907 | ✓ |
| Y³⁺ | 0.0333 | 3 / 90 = 0.03333 | ✓ |
| Ta⁵⁺ | 0.0781 | 5 / 64 = 0.07813 | ✓ |
| Cu²⁺ | 0.0274 | 2 / 73 = 0.02740 | ✓ |
| Bi³⁺ | 0.0291 | 3 / 103 = 0.02913 | ✓ |
| Nb⁵⁺ | 0.0781 | 5 / 64 = 0.07813 | ✓ |
| Mo⁶⁺ | 0.1017 | 6 / 59 = 0.10169 | ✓ |
| Sc³⁺ | 0.0403 | 3 / 74.5 = 0.04027 | ✓ |
| Ga³⁺ | 0.0484 | 3 / 62 = 0.04839 | ✓ |
| **Er³⁺** | 0.0337 | 3 / 89 = 0.03371 | ✓ |
| **Nd³⁺** | 0.0306 | 3 / 98 = 0.03061 | ✓ |

> 🔑 **18/18 일치. 예외 없음.** 확정 사항:
> 1. **단위는 pm⁻¹**(Fig 4b 축 라벨 "Ionic potential (Å⁻¹)"는 **단위 오기** — Å⁻¹이면 Zr⁴⁺가 5.56이 돼야 한다).
> 2. **6배위 Shannon 반경** 을 썼다(본문에 Zr⁴⁺ 72 pm / Er³⁺ 89 pm / Nd³⁺ 98 pm 로 명시된 값과도 정합).
> 3. **조성 가중평균이 아니라 "치환 양이온 하나"의 Z/r 이다.** Li₂.₂₅Zr₀.₇₅Al₀.₂₅Cl₆ 의 Φ = Al³⁺의 Φ지, Zr과의 평균이 아니다.
>    → 즉 **Φ는 도펀트 농도 x에 대해 완전히 무감각한 서술자**다. x=0.05든 x=0.5든 같은 Φ.
> 4. 그러므로 **Φ는 계산이 필요 없다.** 주기율표와 Shannon 표만 있으면 나온다 = *진짜로 값싸다*. (§4.5에서 그 값이 얼마짜리인지 판정한다.)

### 4.3 ⚠ 나머지 두 서술자는 **정의가 없다**

§2.3의 "descriptor framework"는 서술자를 **세 개** 쓴다:

| 기호 | 논문의 말 | 정의식 | 판정 |
|---|---|---|---|
| **Φ** | ionic potential | **Z/r (있음)** | ✅ 재현 가능 |
| **Φ̄_Li** | *"local Li⁺ potential field"*, Fig 4a y축, 단위 **nm⁻¹**, 범위 ~22–34 | **없음** | ⛔ **판독 불가 / 재현 불가** |
| **Φ̄_Me/Φ̄_X** | *"cation/anion potential-energy ratio"*, *"relative binding strength of the central cation to the anion framework"*, Fig 4a x축, 범위 **1.3–2.1** | **없음** | ⛔ **판독 불가 / 재현 불가** |

> ⚠ 검산 시도: Cl⁻의 Φ = 1/181 pm⁻¹ = 0.005525 로 두면 Φ_Zr/Φ_Cl = **10.06**, Fig 4a의 1.67과 맞지 않는다.
> Li까지 포함한 양이온 평균으로도 4.94. **어떤 자연스러운 조합으로도 1.3–2.1이 나오지 않는다** → 우리가 모르는 정규화·격자합이 들어 있다.
> **논문·SI 어디에도 식이 없다.** 저자 문의 없이는 복제 불가(§19 Q1).

### 4.4 ★★★ 판정 — `lee2024` inductive effect와 **같은 축인가**

**결론: 같은 축 · 반대 부호 · 다른 인과경로. 그리고 이 논문 쪽 증거가 훨씬 약하다.**

| 비교항 | **lee2024** (황화물 argyrodite, MTP-MD) | **ren2026** (할라이드 LZC, 프리프린트) |
|---|---|---|
| **서술자** | **Bader 전하 Q(S)** — 계산해서 얻는 값 | **Φ = Z/r** — 표에서 읽는 값 |
| **물리 축** | 중심 양이온이 음이온 전자를 얼마나 끌어당기나 | 중심 양이온이 음이온을 얼마나 세게 붙드나 | ← **같은 축** |
| **처방 방향** | **고원자가**([C]⁶⁺ = W/Mo) | **저-Φ**(Er³⁺/Nd³⁺ ← Zr⁴⁺) | ← **정반대** |
| **인과 경로** | 정전기: Q(S) −1.48 → −0.84 e⁻ ⇒ **S–Li 인력 약화** ⇒ 장벽↓ | 동역학: M–Cl 약화 ⇒ **Cl 골격 유연화(저주파 포논↑)** ⇒ Li 통과 시 골격이 협동 이완 ⇒ 장벽↓ | ← **다른 경로** |
| **Li 캐리어 부수효과** | **감소**(고원자가 = Li 빼앗김). 논문이 명시적 trade-off로 다룸 | **증가**(저원자가 aliovalent = Li 추가) | ← **정반대이며, 이게 ren2026의 진짜 강점** |
| **전자구조 증거** | **Bader 전하 수치 제시** | **없음 — Bader/COHP/전하밀도차 0건.** XPS "Zr 3d·Cl 2p가 약간 이동"(수치 미제시)이 전부 | ← **결정적 비대칭** |
| **격자동역학 증거** | 없음("dynamic lattice effect"는 격자 팽창으로만) | **VDOS 3계**(§7). 단 y축 스케일 불일치 | ← ren2026 우위(질은 §7.3 참조) |

**세 가지를 분리해서 기억할 것:**

1. **축은 같다.** Φ = Z/r 은 고전적 "polarizing power" 지표이고, lee2024가 Bader로 측정한 M–X 결합세기 축의 **기하학적 대리지표**다. 그래서 이 논문 자신이 §1에서 **[28][29] = inductive effect 문헌**을 자기 계보로 인용한다.
2. **부호가 반대다.** lee2024: 고원자가가 좋다. ren2026: 저-Φ가 좋다.
   두 명제가 **동시에 참이려면 축 위에 최적점(volcano)이 있어야 한다.** ren2026은 그걸 §2.3에서 *"negatively correlated"*(단조)라 서술하고, §1에서는 *"higher or lower is not inherently better"*(비단조)라 서술한다 — **자기모순**.
   그리고 **그들 자신의 Table S6을 정렬하면 실제로 완만한 volcano가 보인다**(§4.5).
3. **경로가 다르고, ren2026은 자기 경로를 증명하지 않았다.**
   "저-Φ → Cl 전하 변화 → Li 인력 약화"(=inductive 경로)와 "저-Φ → 격자 유연화"(=이 논문 주장 경로)를 구별하려면 **Cl의 Bader 전하**를 재야 한다. **재지 않았다.**
   게다가 "Li 캐리어 +25 %"라는 제3의 경로가 같은 방향으로 작동한다. **세 경로가 전부 뒤엉켜 있고 분리 실험/계산이 하나도 없다.**

> 🔑🔑 **우리 캠페인에 주는 한 줄**:
> **"z/r 은 inductive effect와 *같은 축을 가리키는 값싼 화살표*이긴 하지만, *방향(부호)도 크기도 알려주지 않는다*.
> 방향과 크기는 여전히 Bader/ICOHP 같은 전자구조 관측량에서만 나온다."**
> → 우리 cascade의 Bader·ICOHP 열은 **대체되지 않는다.** Φ는 기껏해야 **후보 정렬용 0-비용 사전 필터**다(§15.1-1).

### 4.5 ★★★ 판정 — **그들 자신의 Table S6을 재분석하면 Φ의 예측력이 무너진다**

Table S6 전값(σ는 15편의 서로 다른 문헌 소환값 + this work 2개):

| 계 | Φ (pm⁻¹) | σ_RT (mS cm⁻¹) | 출처 |
|---|---:|---:|---|
| Li₂ZrCl₆ | 0.0556 | 0.28 | [SI ref 5] Wang, Nat. Commun. 2021 |
| Li₂.₂₅Zr₀.₇₅**Al**₀.₂₅Cl₆ | 0.0561 | 1.13 | [6] Gao, ESM 2024 |
| Li₂.₂₅Zr₀.₇₅**Fe**₀.₂₅Cl₆ | 0.0465 | 0.98 | [7] Kwak, AEM 2021 |
| Li₂.₁Zr₀.₉₅**Mg**₀.₀₅Cl₆ | 0.0278 | 0.62 | [8] Zhang, J. Energy Chem. 2023 |
| Li₂.₄Zr₀.₈**Zn**₀.₂Cl₆ | 0.0270 | 1.13 | [9] Lei, AEM 2025 |
| Li₂.₁Zr₀.₉₅**Ca**₀.₀₅Cl₆ | 0.0200 | 0.58 | [10] Liu, ChemComm 2025 |
| Li₂.₂₅Zr₀.₇₅**In**₀.₂₅Cl₆ | 0.0375 | 1.08 | [11] Chen, CCL 2022 |
| Li₂.₁**La**₀.₁Zr₀.₉Cl₆ | 0.0291 | 0.82 | [12] Yao, JEM 2025 |
| Li₂.₅**Y**₀.₅Zr₀.₅Cl₆ | 0.0333 | 1.19 | [13] Chen, Energy Mater. Adv. 2023 |
| Li₁.₇Zr₀.₇**Ta**₀.₃Cl₆ | 0.0781 | **1.42** | [14] Liu, ESM 2024 |
| Li₂.₁Zr₀.₉₅**Cu**₀.₀₅Cl₆ (표기 오타 "Li₆") | 0.0274 | 0.75 | [15] Li, ESM 2024 |
| Li₂.₁₅Zr₀.₈₅**Bi**₀.₁₅Cl₆ | 0.0291 | 0.49 | [16] Du, Nanoscale 2025 |
| Li₁.₇₅Zr₀.₇₅**Nb**₀.₂₅Cl₆ | 0.0781 | 0.55 | [17] Wu, AEM 2024 |
| Li₁.₇₅Zr₀.₇₅**Mo**₀.₂₅Cl₆ ⚠전하불균형 | 0.1017 | **0.17** | [17] Wu, AEM 2024 |
| Li₂.₄Zr₀.₆**Sc**₀.₄Cl₆ | 0.0403 | **1.50** | [18] Kwak, CEJ 2022 |
| Li₂.₁Zr₀.₉**Ga**₀.₁Cl₆ | 0.0484 | 0.40 | [19] Ghorbanzade, ACS AEM 2025 |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** (표기 "Li₀.₅" 오타) | 0.0337 | **1.32** | this work |
| **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆** (표기 "Li₀.₃₇₅" 오타) | 0.0306 | 1.13 | this work |

**논문의 주장**: *"in most systems, the ionic potential of the central cation is **negatively correlated** with the room-temperature ionic conductivity."*

**우리 재분석 (위 18쌍 그대로, 계산 절차 = 단순 Pearson/Spearman)**:

| 통계 | 값 | 해석 |
|---|---:|---|
| Pearson r (Φ, σ) | **−0.255** | 약한 음의 경향 |
| **R²** | **0.065** | ⛔ **Φ가 σ 분산의 6.5 %만 설명** |
| Spearman ρ (Φ, σ) | **−0.089** | ⛔ **순위 상관 사실상 0** |
| Pearson r (Φ, ln σ) | −0.432 | 로그축에서도 R² = 0.19 |
| pristine 제외 17쌍 | r = −0.226, **ρ = +0.011** | ⛔ 부호마저 사라짐 |
| pristine + this-work 제외(문헌 16쌍) | r = −0.179, ρ = −0.045 | ⛔ **자기 데이터를 빼면 상관 소멸** |
| **비교: Li 함량 vs σ** | **r = +0.553, ρ = +0.628** | 🔑 **Li 캐리어가 훨씬 나은 예측자** |
| 참고: Φ vs Li 함량 | r = **−0.715** | 🔑 aliovalency 때문에 **기계적으로 반상관** |

**세 개의 결정적 반례(그들 표 안에서):**
1. **Φ = 0.0781 동률**인 **Ta⁵⁺ σ 1.42 vs Nb⁵⁺ σ 0.55 — 2.6배 차이.** 서술자가 같은 값을 주는데 σ가 2.6배 갈린다. 함수 관계 자체가 성립하지 않는다.
2. **Φ ≈ 0.0556 vs 0.0561**(사실상 동일)인 **Zr(pristine) 0.28 vs Al 1.13 — 4배 차이.**
3. **최저 Φ 구간이 최고 σ가 아니다.** Ca(0.0200) 0.58, Mg(0.0278) 0.62, Cu(0.0274) 0.75 — 전부 Er(0.0337) 1.32보다 **낮다**. 즉 "낮을수록 좋다"가 **저-Φ 끝에서 먼저 깨진다**.

**Φ로 정렬했을 때 실제로 보이는 것 = 완만한 volcano(우리 판독):**

```
Φ:  0.0200  0.0270  0.0274  0.0278  0.0291  0.0291  0.0306  0.0333  0.0337  0.0375  0.0403  0.0465  0.0484  0.0556  0.0561  0.0781  0.0781  0.1017
     Ca      Zn      Cu      Mg      La      Bi      Nd*     Y       Er*     In      Sc      Fe      Ga      Zr      Al      Ta      Nb      Mo
σ:  0.58    1.13    0.75    0.62    0.82    0.49    1.13    1.19    1.32    1.08    1.50    0.98    0.40    0.28    1.13    1.42    0.55    0.17
                                            └────────── 최고군(1.1–1.5)이 Φ ≈ 0.030–0.040 에 모여 있다 ──────────┘        ↑Ta 이상치        ↓Mo 최저
```

> 🔑🔑 **우리 판정**: 데이터가 지지하는 진술은
> **"M–Cl 결합세기에는 최적 구간이 있다(Φ ≈ 0.030–0.040 pm⁻¹ 부근에 고전도군이 모인다). 그러나 산포가 너무 커서 Φ 하나로 σ를 예측할 수 없다."**
> 이것은 `[Kraft]`가 argyrodite에서 실험으로 확립한 **"soft lattice ≠ always better, 격자강성은 튜닝 대상"** 명제와 **같은 형태**다(§7.5).
> **⛔ "낮은 이온퍼텐셜이 좋다"는 논문의 헤드라인 명제는 그들 자신의 표에서 지지되지 않는다.**

**추가로 이 표 자체의 방법론적 약점 (인용 전 반드시 병기):**
- **15편의 서로 다른 논문의 σ를 한 축에 놓았다.** 합성법(볼밀 조건)·펠릿 압력/밀도·측정온도·total vs bulk·블로킹 전극이 전부 다르다. 정규화 0건.
- **도펀트 농도 x가 0.05~0.5로 10배 흩어져 있는데 Φ는 x에 무감각**(§4.2-3). 즉 x 효과가 통째로 잡음으로 들어간다.
- pristine LZC σ가 **한 논문 안에서 3개 값**: 본문 §1 **0.40**(문헌) / Table S6 **0.28**(SI ref 5) / 자체 측정 **0.227**.
- **Li₁.₇₅Zr₀.₇₅Mo₀.₂₅Cl₆ 는 전하 불균형**(양전하 합 6.25 vs 음전하 6.0). 표기 오류로 보이나 그대로 인쇄됨.
- "Li₀.₅Zr₀.₅Er₀.₅Cl₆"·"Li₀.₃₇₅…" — **자기 논문 최적 조성의 화학식이 틀렸다**(Li₂.₅/Li₂.₃₇₅여야 함).
- Fig 4b는 이 표의 막대그림인데 y축 라벨/단위가 본문·SI와 어긋난다(§11 Fig 4b).

### 4.6 Fig 4a — 서술자 지도의 치명적 한계

Fig 4a는 x = Φ̄_Me/Φ̄_X (1.3–2.1), y = Φ̄_Li (22–34 nm⁻¹) 평면에 18계를 찍은 산점도다.
LZC는 우하(≈1.67, ≈23), Er/Nd 최적조성(빨간 별)은 좌상(≈1.35–1.39, ≈31–32), Mo(≈2.02)·Ta/Nb(≈1.84)는 우측.

> ⛔ **이 그림에는 σ가 없다.** 컬러바도, 마커 크기 인코딩도, 등고선도 없다. 마커 모양은 "this work vs 문헌"만 구별한다.
> **즉 Fig 4a는 두 개의 *정의되지 않은* 서술자의 산점도이며, 구조–물성 관계를 주장할 수 있는 정보를 담고 있지 않다.**
> 논문이 이 그림에서 읽어내는 것(*"pristine LZC lies in a region with relatively high Φ̄_Me/Φ̄_X… after doping the whole system shifts towards a lower- Φ̄_Me/Φ̄_X region"*)은
> **"치환하면 서술자 값이 변한다"** 는 동어반복이지 인과가 아니다.

---

## 5. 구조·합성·국소환경 (§2.1, Fig 2, Table S1–S4)

### 5.1 계산 스크린 → 조성 선택
- Li₂₊ₓZr₁₋ₓMₓCl₆ (M=Er,Nd; 0 ≤ x ≤ 0.625) 슈퍼셀 모델 구축 → DFT 완화.
- 결과: *"all the doped systems maintain the **P3̄m1** framework characteristics of LZC without obvious structural collapse or abnormal local distortion"*.
- **응집에너지 E_coh**(Table S1·S2)로 열역학 안정성 판정. 최저값 = **Er x=0.5**, **Nd x=0.375** → 이 둘을 합성 대상으로.

**Table S1 (Er 계) — 원값**

| x | 0 | 0.125 | 0.25 | 0.375 | **0.5** | 0.625 |
|---|---:|---:|---:|---:|---:|---:|
| Total Energy /eV | −315.59 | −316.88 | −318.08 | −320.34 | −321.34 | −321.09 |
| "Binding Energy" /eV | −19.24 | −19.70 | −20.15 | −20.56 | **−22.02** | −21.51 |

**Table S2 (Nd 계) — 원값**

| x | 0 | 0.125 | 0.25 | **0.375** | 0.5 | 0.625 |
|---|---:|---:|---:|---:|---:|---:|
| Total Energy /eV | −315.59 | −316.80 | −316.95 | −319.68 | −318.92 | −319.92 |
| "Binding Energy" /eV | −19.24 | −19.67 | −20.71 | **−21.45** | −20.75 | −21.14 |

**SI eq (1)** (docx OMML에서 우리가 추출한 원식):
```
E_coh = [ E_total − a·E_Li − b·E_Zr − c·E_M − d·E_Cl ] / (a + b + c + d)
```
*"E_coh represents the **average cohesive energy per atom**… a, b, c, d represent the numbers of Li, Zr, M, Cl atoms in the corresponding supercell."*

> ⚠⚠ **세 가지 문제**:
> 1. **값이 식과 맞지 않는다.** 인쇄된 식은 **per-atom**인데, 염화물의 원자당 응집에너지는 통상 수 eV다. −19~−22 eV/atom은 자릿수가 맞지 않는다(정황상 **per formula unit** 로 읽어야 자릿수가 맞지만 확정 불가). SI 표 헤더도 "Binding Energy"라 써서 본문의 "cohesive energy"와 용어가 다르다.
> 2. **참조 상태 E_Li/E_Zr/E_M/E_Cl 이 하나도 명시되지 않았다**(벌크 금속? 고립 원자? Cl₂?). → **재현 불가.**
> 3. **조성이 다른 계들의 E_coh를 직접 비교해 "안정성"을 논한다.** 정석은 **E_hull(경쟁상 대비 분해에너지)** 인데, **E_hull·형성에너지·LiCl/ZrCl₄/ErCl₃ 분해 검사 전부 없다.**
>    Er 계는 x=0.5까지 거의 단조로 내려가므로 "최저 = 최적"은 사실상 "Er을 많이 넣을수록 결합이 세다"의 재진술이다.
> ⛔ 우리가 이 표에서 확인할 수 있는 유일한 것: **E_total 값이 72원자 규모 셀과 정합**(−315.59/72 = −4.38 eV/atom). §6.3에서 이 셀 크기를 독립적으로 확정한다.

### 5.2 합성 (§4 Experimental)
- **고에너지 기계화학(볼밀) 단일 공정, 열처리 없음.**
- 전구체: **LiCl(99 %, Aladdin) · ZrCl₄(99.9 %) · ErCl₃(99.9 %) · NdCl₃(99.9 %)**.
- 글러브박스 Ar, **H₂O < 0.1 ppm, O₂ < 0.1 ppm**.
- **500 mL ZrO₂ 자, ZrO₂ 볼 φ10 mm, ball:powder = 25:1, 700 rpm, 누적 45 h** — *30 min 밀링 / 10 min 강제냉각* 간헐 모드(국소 과열 분해 억제).
  > 🔑 이 간헐 밀링 레시피는 **`[Schlem]`의 "무질서 = 공정변수"** 프레임과 직결된다. 45 h·700 rpm은 매우 강한 조건이고, 열처리가 없으므로 **시료는 상당한 무질서/미결정 상태**일 것이다. 논문은 무질서 정량을 하지 않는다(§16-8).

### 5.3 XRD / Rietveld (Fig 2b, 2c, S3, S4; Table S3, S4)

> ⚠⚠ **아래 두 줄은 논문의 주장을 그대로 옮긴 것이다. 2026-08-04 2차 패스에서 Fig 2b 를 픽셀로 재보니 둘 다 그림의 지지를 받지 못한다 — 반드시 §20.7 을 같이 읽을 것.**
> 요지: 도핑 시료의 날카로운 선 **29.9 / 34.7 / 50.0 / 59.6°** 가 **fcc LiCl (111)/(200)/(220)/(311) = 30.10/34.89/50.15/59.62°** 와 4/4 일치(편차 −0.2° 일정)하고, **pristine LZC 의 최강선 16.0°·32.1° 는 도핑 시료에 없다.**

- 모든 도핑 시료의 주피크가 **Li₃YCl₆형(PDF#44-0286)** 과 일치, **불순물 피크 없음** → LZC 호스트 골격 유지. *(→ §20.7 에서 반증 표시)*
- **도핑 시 피크가 전체적으로 저각 이동** = 격자 팽창. 원인: **Zr⁴⁺(72 pm) → Er³⁺(89 pm)/Nd³⁺(98 pm)** 로 [MCl₆] 팔면체 팽창. *(→ §20.7: 대응 피크 쌍이 없어 "이동" 을 정의할 수 없다)*
- Rietveld(Fig 2c): **Li₂.₅Zr₀.₅Er₀.₅Cl₆ R_wp = 4.596 %, R_p = 3.72 %, GOF = 1.76** / **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆ R_wp = 4.86 %, R_p = 4.07 %, GOF = 1.89** (그림 판독).
  ⚠ **정련된 격자상수·자리점유율·원자좌표 표는 본문·SI 어디에도 없다.** Table S3/S4는 DFT 값과 "experimental value" 한 줄씩만 준다.

**Table S3 / S4 — 격자상수 (원값)**

| | 계산 (Å) | "실험" (Å) | error (%) | ecut | k-point |
|---|---|---|---|---|---|
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** | a = **12.51** / b = **12.51** / c = **11.42** | a = 12.48 / b = 12.49 / c = 11.44 | 0.5 | 520 eV | 3×3×3 |
| **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆** | a = **12.51** / b = **12.51** / c = **11.42** | a = 12.53 / b = 12.50 / c = 11.43 | 0.5 | 520 eV | 3×3×3 |

> ⚠⚠ **두 조성의 *계산* 격자상수가 소수 넷째 자리까지 완전히 동일하다.** 서로 다른 희토류(89 vs 98 pm), 서로 다른 농도(0.5 vs 0.375)인데 완화 결과가 같다는 것은 물리적으로 이상하다.
> "error 0.5 %" 열도 전 행 동일값(c의 11.42 vs 11.44는 0.17 %)이라 **행별로 계산된 값이 아니다.**
> **§6.3에서 우리가 독립적으로 확인한다 — AIMD/NE 파이프라인이 11개 조성 전부에 *단일 부피*를 썼다.** 두 사실이 서로를 지지한다:
> **계산 파이프라인이 조성별 격자 팽창을 반영하지 않았다.** 그런데 격자 팽창은 이 논문 기구 주장의 한 축이다(§16-5).

### 5.4 XPS (Fig 2d–2f)
- **Er 4d / Nd 3d** 피크가 각각 Er³⁺ / Nd³⁺ 특성 결합에너지에 대응 → *"the doped rare-earth elements exist mainly in stable +3 valence states"*.
- **Zr 3d 와 Cl 2p 가 도핑 후 약간 이동(slightly shift)** → *"suggesting that Er³⁺/Nd³⁺ substitution induces changes in the local electronic environment and **may modify** the interaction between the central cations and Cl⁻"*.
- 측정: 아르곤 글러브박스 → 전용 고진공 이송챔버 직결(대기 노출 회피), **C 1s 284.8 eV 보정**, Gaussian–Lorentzian 피팅, **Avantage** 소프트웨어.

> ⛔ **이동량(eV)이 본문·SI 어디에도 숫자로 없다.** "slightly shift" + "may modify"뿐.
> **이것이 "M–Cl 상호작용 약화"에 대한 유일한 실험적 전자구조 증거다.** 정량 0.
> 우리 기준(`[Banik]` HAXPES VBM, `[Whitten]` UPS 규율)으로 보면 **주장에 비해 증거가 두 단계 약하다.**

### 5.5 Raman (Fig 2g)
- **[ZrCl₆]²⁻ 관련 진동 피크가 도핑 후 넓어지고(broadening) 약간 적색이동(slight redshift)**
  → *"the introduction of Er³⁺/Nd³⁺ generates local structural disorder and changes in the coordination environment"*.
- 조건: **532 nm 여기, 레이저 파워 엄격 제한**(국소 과열로 인한 열화 방지). x축 100–500 cm⁻¹.

> 🔑 **적색이동 = 진동수↓ = 격자 연화** — 이게 "lattice softening"의 **유일한 실험 증거**이고, 방향은 phonon 계산(§7)과 정합한다.
> ⛔ 그러나 **피크 위치·이동량(cm⁻¹)·반치폭 수치가 하나도 없다.** 정성 관찰만.

### 5.6 SEM / EDS (Fig 2h, S5, S6)
- 수십 nm 급 나노결정 응집체 → **µm급 2차 응집체**. *"facilitates intimate interparticle contact during pellet pressing"*.
- EDS 맵: **Zr, Er/Nd, Cl 이 µm 스케일에서 균일**, 편석·농축 영역 없음 → 기계화학 합성 중 희토류가 LZC 기지에 균일 편입.

---

## 6. ★★ Li⁺ 확산·이온전도 (§2.2, Fig 3, Table S5) — 이 digest의 핵심 감사 대상

### 6.1 AIMD 셋업 전수 (§4 Computational)

| 항목 | 값 | 비고 |
|---|---|---|
| code | **VASP** (버전 미기재) | [35] Kresse–Furthmüller |
| pseudo | **PAW** | [36] Blöchl |
| functional | **GGA-PBE** | [37] · **vdW 보정 언급 없음** |
| **DFT+U** | **Er·Nd의 4f 궤도에 적용** | ⛔ **U 값 미기재.** 스핀분극 여부·4f를 core에 얼렸는지 여부도 **미기재** |
| ecut (정적) | **520 eV** | |
| k-mesh (정적) | **3×3×3** | Table S3/S4에도 반복 |
| 수렴 | 전자 **1.0×10⁻⁴ eV** / 이온 **1.0×10⁻³ eV** / 힘 **0.02 eV Å⁻¹** | |
| **AIMD 셀** | *"In the pristine Li₂ZrCl₆ structure uses a **2 × 2 × 2 supercell**"* | **§6.3에서 우리가 72원자(Li₁₆Zr₈Cl₄₈)로 확정** |
| 도핑 배열 | *"Aliovalent cation doping with Er³⁺ or Nd³⁺ is introduced into this structure, and **stable doped configurations are obtained through structural optimization**"* | ⛔ **조성당 배열 1개.** 열거·SQS·앙상블 없음. 배열 선택 규칙 미기재 |
| 앙상블 | **NVT, Nosé–Hoover** | |
| 온도 | **600, 700, 800, 900 K (4점)** → **300 K 외삽** | |
| Δt | **2 fs** | |
| **총 길이** | **50 ps** | ⛔ 평형화 구간 분리 언급 없음 |
| AIMD k-mesh | **Γ-centered 1×1×1** | |
| 후처리 | **pymatgen** [38] | |
| **시드 / 오차막대** | **1 / 없음** | ⛔ 표·그림 어디에도 ± 없음 |
| MSD 창 | **미기재** (Fig 3a–c는 0–40 ps 전 구간 표시) | |

**SI eq (2)–(5)** (docx OMML 원식, 우리가 추출):
```
(2)  MSD = (1/N) Σᵢ₌₁ᴺ | rᵢ(t+Δt) − rᵢ(t) |²
(3)  D   = MSD(Δt) / (2·d·Δt)          ← d = 차원인자
(4)  D   = c · exp( −Eₐ / (K_b T) )
(5)  σ   = ( n q² / (K_b T) ) · D       ← Nernst–Einstein, Haven 보정 없음 (q = +1)
```
SI 원문: *"d is the dimension factor of the ion migration path. The lithium-ion migration path in solid electrolytes is mostly **anisotropic**, so d is **3**."*
> ⚠ 문장이 비논리적이다("이방적이니까 d=3"). **식 자체는 총 MSD를 쓰면 이방성과 무관하게 옳다**(d=3 = 3차원 tracer 평균). 근거 문장만 틀렸다.
> 다만 **실제 확산이 사실상 1D인 pristine LZC(§9)** 에서, 단결정 등방평균 D를 NE로 σ로 바꾸면 **다결정 펠릿의 퍼콜레이션 손실을 무시**하게 된다 — `[kim2025]` p_c=1 논지 그대로.

### 6.2 ★ Table S5 전값 (SI) — 이 논문 계산 결과의 정본

| 조성 | D (300 K) /10⁻⁸ cm² s⁻¹ | Eₐ /eV | σ (300 K) /mS cm⁻¹ |
|---|---:|---:|---:|
| **Li₂ZrCl₆** (x=0) | 1.576 | **0.230** | **1.0088** |
| Li₂.₁₂₅Zr₀.₈₇₅**Er**₀.₁₂₅Cl₆ | 0.169 | 0.341 | **0.115** ⬇ |
| Li₂.₂₅Zr₀.₇₅**Er**₀.₂₅Cl₆ | 0.363 | 0.314 | **0.261** ⬇ |
| Li₂.₃₇₅Zr₀.₆₂₅**Er**₀.₃₇₅Cl₆ | 0.959 | 0.262 | **0.729** ⬇ |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** | **5.004** | **0.163** | **4.004** ⬆최대 |
| Li₂.₆₂₅Zr₀.₃₇₅**Er**₀.₆₂₅Cl₆ | 2.899 | 0.196 | 2.435 |
| Li₂.₁₂₅Zr₀.₈₇₅**Nd**₀.₁₂₅Cl₆ | 3.542 | 0.207 | 2.409 |
| Li₂.₂₅Zr₀.₇₅**Nd**₀.₂₅Cl₆ | 3.095 | 0.210 | 2.230 |
| **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆** | **4.687** | **0.189** | **3.560** ⬆최대 |
| Li₂.₅Zr₀.₅**Nd**₀.₅Cl₆ | 0.310 | 0.282 | 0.248 ⬇ |
| Li₂.₆₂₅Zr₀.₃₇₅**Nd**₀.₆₂₅Cl₆ | 0.289 | 0.300 | 0.243 ⬇ |

(Fig 3f = 이 표의 3중 막대그림. 단위 "Ea 10⁻¹ eV" 로 인코딩 — 값 일치 확인.)

### 6.3 ★★★ 우리 독립 검산 — 셀·N_Li·부피·파이프라인을 전부 역산했다

**절차**: SI eq (5) `σ = n q² D /(k_B T)` 에 **n = N_Li / V**, **V = a·b·sin120°·c** (Table S3의 a=b=12.51, c=11.42 Å → **V = 1547.8 Å³**), **N_Li = 8·(2+x)** 를 넣고 11개 조성의 σ를 재계산.

| 조성 | N_Li | 우리 σ (mS/cm) | 논문 σ | 비 |
|---|---:|---:|---:|---:|
| LZC (x=0) | 16 | 1.0097 | 1.0088 | 1.0009 |
| Er 0.125 | 17 | 0.1150 | 0.1150 | 1.0003 |
| Er 0.25 | 18 | 0.2616 | 0.2610 | 1.0024 |
| Er 0.375 | 19 | 0.7296 | 0.7290 | 1.0008 |
| Er 0.5 | 20 | 4.0073 | 4.0040 | 1.0008 |
| Er 0.625 | 21 | 2.4377 | 2.4350 | 1.0011 |
| Nd 0.125 | 17 | 2.4110 | 2.4090 | 1.0008 |
| Nd 0.25 | 18 | 2.2307 | 2.2300 | 1.0003 |
| Nd 0.375 | 19 | 3.5658 | 3.5600 | 1.0016 |
| Nd 0.5 | 20 | 0.2483 | 0.2480 | 1.0010 |
| Nd 0.625 | 21 | 0.2430 | 0.2430 | 1.0000 |

> 🔑🔑 **11/11 이 0.03–0.24 % 이내로 재현된다.** 확정된 사실:
> 1. **AIMD 셀 = 2×2×2 = 72원자 (Li₁₆Zr₈Cl₄₈)**, 도핑 시 Li 16→21개, Zr 8→3개.
>    → **MSD를 내는 Li가 16–21개뿐이다.** (`[kim2025]` Li₃YCl₆는 Li 9개였다 — 같은 등급의 얇은 통계.)
> 2. **Table S3/S4의 격자상수는 *슈퍼셀* 값이다**(단위셀 값이 아님).
> 3. **Table S5의 D 는 300 K 외삽값**이다(600 K 값이 아님).
> 4. **11개 조성 전부에 동일한 부피 1547.8 Å³ 를 썼다** — §5.3의 "계산 격자상수 동일" 관찰과 정확히 부합.
>    → **NE 변환에서 조성별 격자 팽창이 무시됐다**(σ에 미치는 영향은 1–2 % 수준으로 작지만, "격자 팽창이 기구다"라는 서사와는 어긋난다).
> 5. **Haven 비 보정 없음**(q=+1, 상관 무시) — 우리 UMA-MD 파이프라인과 같은 규약. `[Adeli]`가 argyrodite에서 **Haven 0.23–0.3** 을 실측했음을 기억할 것(NE는 협동운동이 있으면 σ를 **과소**평가).

### 6.4 ⚠ 본문 ↔ SI Table S5 **직접 충돌** — "volcano"가 아니다

본문 §2.2: *"the ionic conductivities of both Er-doped and Nd-doped systems exhibit a **volcano-type trend** as a function of dopant concentration x: the ionic conductivity **first increases** with increasing dopant content but then gradually decreases after exceeding a critical threshold."*

**Er 계 실제 궤적** (Table S5·Fig 3f):
```
x:    0      0.125   0.25    0.375   0.5     0.625
σ:  1.009 → 0.115 → 0.261 → 0.729 → 4.004 → 2.435
      ↓ 8.8배 급락        ↑ 35배 급등          ↓
```
**첫 도핑에서 σ가 8.8배 떨어진다.** "먼저 증가"가 아니다. **Er 계는 volcano가 아니라 "깊은 골 → 급등 → 하강"** 이다.

**Nd 계**: 1.009 → 2.409 → 2.230 → 3.560 → **0.248** → 0.243 (x≥0.5에서 **14배 붕괴**). 이쪽은 대략 volcano에 가깝다.

> ⛔ **본문의 "volcano" 서술은 Er 계에서 자기 SI 표와 모순된다.** 우리 규율(그림/표 우선)에 따라 **Table S5·Fig 3f를 정본**으로 삼는다.

**그리고 더 큰 이상**: **같은 x=0.125에서 Er은 0.115, Nd는 2.409 — 21배 차이.**
Er³⁺(Φ 0.0337, 89 pm)와 Nd³⁺(Φ 0.0306, 98 pm)는 화학적으로 거의 같은 3가 희토류다. **논문의 서술자(Φ)는 이 둘이 거의 같게 행동할 것이라고 예측한다.** 실제로는 21배 갈린다.
> 🔑 **이 21배는 물리가 아니라 "조성당 배열 1개 + 단일 시드 + 16–21 Li + 50 ps"의 통계 잡음일 가능성이 크다**(§6.7이 이를 정량적으로 뒷받침한다).

### 6.5 실험 σ (Fig 3g, 3h) — 측정 조건

| 항목 | 내용 |
|---|---|
| 방법 | **EIS**, 전기화학 워크스테이션 |
| 펠릿 | **직경 16 mm, 두께 약 1–2 mm** — ⛔ **§20.5: 이 기하로는 Fig 3g 의 실측 저항에서 인쇄된 σ 가 안 나온다.** 5/5 시료가 두께 3.7–4.8 mm 를 요구한다(=범위 밖). **직경 10 mm 로 놓으면 5/5 가 1.44–1.87 mm** 로 정확히 들어간다 → 셀 상수가 명시값과 **2.56배** 어긋난다 |
| 주파수 | **1 MHz – 0.1 Hz** |
| 식 | **σ = L/(R × S)** — R은 임피던스 스펙트럼에서 |
| ⛔ **미기재** | **블로킹 전극 종류 · 성형 압력 · 측정 압력 · 펠릿 상대밀도 · 측정 온도 · bulk/GB 분리 여부 · 등가회로 · 시료 수(n)/오차** |

**Fig 3h 실측값** (그림 판독, 본문값과 정합):

| 시료 | σ_RT (mS cm⁻¹) | pristine 대비 |
|---|---:|---:|
| Li₂ZrCl₆ | **0.227** (Fig 3h 막대 0.23) | 1.00× |
| Li₂.₂₅Zr₀.₇₅Nd₀.₂₅Cl₆ | 0.81 | 3.6× |
| **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆** | **1.13** | **4.98×** |
| Li₂.₂₅Zr₀.₇₅Er₀.₂₅Cl₆ | 0.76 | 3.3× |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** | **1.32** | **5.81×** |

> ⚠ **실험 Eₐ가 없다.** 온도의존 EIS(아레니우스)를 하지 않았다 → **계산 Eₐ(0.163/0.189/0.23 eV)를 검증할 실험 카운터파트가 0.**
> 이건 `[Adeli]`(EIS 0.34→0.29 ≡ PFG 0.35→0.29 이중 일치로 GB 오염을 반박)나 `[Kraft]`(E_A·prefactor 동시 보고)와 비교하면 **한참 얕은 전기화학**이다.

### 6.6 ★ 계산 ↔ 실험 대조 — 논문 주장과 실제

논문: *"The **high consistency** between theory and experiment in terms of the overall trend **strongly confirms** the mechanistic reliability…"*

**둘 다 있는 5개 점을 실제로 맞춰보면:**

| 시료 | AIMD σ | 실험 σ | AIMD/실험 | AIMD의 pristine 대비 | 실험의 pristine 대비 | 판정 |
|---|---:|---:|---:|---:|---:|---|
| Li₂ZrCl₆ | 1.0088 | 0.227 | **4.44×** 과대 | 1.00 | 1.00 | — |
| Er x=0.25 | 0.261 | 0.76 | **0.34×** (과소) | **0.26 (악화)** | **3.35 (개선)** | ⛔ **방향 반대** |
| **Er x=0.5** | 4.004 | 1.32 | **3.03×** 과대 | 3.97 | 5.81 | ○ 방향 일치 |
| Nd x=0.25 | 2.230 | 0.81 | **2.75×** 과대 | 2.21 | 3.57 | ○ |
| **Nd x=0.375** | 3.560 | 1.13 | **3.15×** 과대 | 3.53 | 4.98 | ○ |

> ⛔⛔ **Er x=0.25 에서 이론과 실험의 *부호*가 반대다.** AIMD는 "pristine 대비 4배 악화"라 하고, 실험은 "3.35배 개선"이라 한다.
> 이건 배율 문제가 아니라 **정성적 모순**이고, 하필 **Er 계에서 최적점 외의 유일한 실험점**에서 발생했다.
> 논문은 이 점을 언급하지 않는다. *"high consistency"* 라는 문장은 **실제 데이터로 뒷받침되지 않는다.**

**AIMD 과대 배율의 위치 (우리 db 이력과 비교)**:

| 계 | AIMD/실험 | 출처 |
|---|---:|---|
| Li₃YCl₆ (**할라이드**) | **27×** | `lee2024` ESI Table S1 (kb 기록) |
| Li₃YCl₆ hcp_1 (**할라이드**) | **25–420×** | `kim2025` Table 2(논문 자인) |
| Li₆PS₅I (황화물) | 840× | `lee2024` |
| Li₆PS₅Cl (황화물) | 1.9× | `lee2024` |
| **Li₂ZrCl₆ (이 논문, 할라이드)** | **4.4×** (pristine), **2.8–3.2×** (도핑) | 본 digest §6.6 |

> 🔑 **이 논문의 AIMD는 할라이드 AIMD 중에서는 "잘 맞는 편"(3–4×)이다.** Li₃YCl₆의 27–420배와는 등급이 다르다.
> **그러나** 그건 σ 절대값 얘기고, **조성 간 순위/방향은 여전히 틀린다**(Er 0.25). 그리고 §6.7이 보여주듯 **격차 자체가 외삽 산물**이다.
> ⛔ **"할라이드 AIMD는 크게 빗나간 이력이 있다"는 경고는 이 논문에도 그대로 유효하다** — 다만 이 논문의 실패 형태는 *절대값 폭주*가 아니라 *순위 뒤집힘*이다.

### 6.7 ★★★ 우리 독립 재분석 — **헤드라인 격차는 외삽이 만들었다** (Meyer–Neldel 진단)

**절차**: Table S5의 (D₃₀₀, Eₐ) 쌍에서 각 조성의 전지수 인자 `D₀ = D₃₀₀ · exp(Eₐ/k·300)` 를 복원하고, 실제 시뮬레이션 온도에서의 D(T)를 되돌려 계산했다.

**(a) 복원한 전지수 인자와 Meyer–Neldel 보상**

| 조성 | Eₐ (eV) | 복원 D₀ (cm² s⁻¹) |
|---|---:|---:|
| LZC | 0.230 | 1.15×10⁻⁴ |
| Er 0.125 | 0.341 | **9.05×10⁻⁴** (최대) |
| Er 0.25 | 0.314 | 6.84×10⁻⁴ |
| Er 0.375 | 0.262 | 2.42×10⁻⁴ |
| **Er 0.5** | **0.163** | **2.74×10⁻⁵** (최소) |
| Er 0.625 | 0.196 | 5.69×10⁻⁵ |
| Nd 0.125 | 0.207 | 1.06×10⁻⁴ |
| Nd 0.25 | 0.210 | 1.04×10⁻⁴ |
| Nd 0.375 | 0.189 | 7.01×10⁻⁵ |
| Nd 0.5 | 0.282 | 1.69×10⁻⁴ |
| Nd 0.625 | 0.300 | 3.17×10⁻⁴ |

**ln D₀ vs Eₐ 회귀: r = 0.965, R² = 0.932, 기울기 17.45 eV⁻¹ → E_MN = 1/기울기 = 57.3 meV.**
비교: **kT(300 K) = 25.9 meV · kT(600 K) = 51.7 meV · kT(900 K) = 77.6 meV.**

> 🔑 **E_MN(57 meV)가 시뮬레이션 온도창(600–900 K)의 kT 한복판에 있다.** 이것은 Meyer–Neldel 보상의 **교과서적 통계 인공물 신호**다:
> 좁은 고온창에서 잡음 섞인 D(T) 4점을 아레니우스 적합하면, 적합된 (Eₐ, ln D₀)가 **등속점(isokinetic point) T_iso ≈ 1/(k·기울기)** 를 축으로 회전하며 강하게 반상관된다.
> 즉 **11개 계는 "T_iso ≈ 665 K에서 사실상 같은 D"** 를 갖고, 300 K에서의 차이는 그 회전을 저온으로 연장한 결과다.

**(b) 결정적 확인 — 온도별 분산**

| T | 11개 조성 D의 max/min 분산 |
|---:|---:|
| **900 K** (시뮬) | **3.6×** |
| **800 K** (시뮬) | 2.8× |
| **700 K** (시뮬) | 2.4× |
| **665 K** (=T_iso) | **2.3× (최소)** |
| **600 K** (시뮬) | 2.7× |
| **300 K** (외삽) | **29.6×** |

> 🔑🔑🔑 **데이터가 실제로 존재하는 600–900 K 구간에서 11개 조성은 서로 2.3–3.6배 안에 다 들어간다.**
> **300 K로 외삽하는 순간 29.6배로 벌어진다.**
> 16–21개 Li, 50 ps, 단일 시드, 단일 배열 AIMD의 D 통계 불확실도는 통상 **2–3배 수준**이다(He/Zhu/Epstein/Mo, *npj Comput. Mater.* **2018**, 4, 18 — 이 논문 자신이 ref [31]로 인용한다).
> ⛔ **따라서: 이 논문의 σ(300 K) 서열·"volcano"·"6배 향상"은 실측 구간에서 통계 잡음과 구별되지 않는 차이를 300 K로 증폭한 것이다.**
> 논문은 [31] He/Mo를 **"MSD > 5 Å²면 장거리 확산"** 판정에만 쓰고, 그 논문의 본론인 **불확실도 정량은 전혀 쓰지 않았다.** (`kim2025` §8.3과 **정확히 같은 실패 패턴**.)

**(c) 추가 내부 불일치 (그림 판독 기반, 확정 불가)**
Fig 3a(pristine, 600 K)의 총 MSD는 40 ps에서 ≈10 Å², Fig 3b(Er x=0.5, 600 K)는 ≈50 Å² — **600 K에서 Er0.5가 pristine의 약 5배**.
그런데 Table S5의 (D₃₀₀, Eₐ)를 600 K로 되돌리면 **pristine 1.35×10⁻⁶ vs Er0.5 1.17×10⁻⁶ cm²/s = Er0.5가 오히려 조금 느리다.**
> ⚠ 두 진술이 양립하지 않는다. 가장 그럴듯한 해석은 **아레니우스 적합선이 600 K 데이터점을 제대로 지나지 않는다**(4점 적합이 나쁘다)는 것이고, 이는 §6.7(b)의 진단을 **강화**한다.
> (그림 y축 판독에 기댄 지적이므로 "확정"이 아니라 "표시"로 기록한다.)
>
> ### ✅ **2026-08-04 해소 (→ §20.2·§20.3)**
> 그 "가장 그럴듯한 해석"이 **맞았고, 원인까지 특정됐다.** 그림 마커를 픽셀로 전수 추출한 결과
> **적합에 쓰인 온도점이 4개가 아니라 5개**이고, 다섯 번째가 **Methods 에도 Table S5 에도 없는 500 K** 다.
> Er0.5 의 500 K 점은 600 K 점보다 **위**에 있어서(D 가 냉각 시 1.7배 증가 — 불가능) 적합선을 통째로 눕힌다.
> **500 K 를 빼고 600–900 K 만 쓰면 Er0.5 Eₐ = 0.372 eV, pristine = 0.332 eV** 로 올라간다.
>
> **"600 K 에서 Er0.5 는 pristine 의 몇 배인가" 세 답의 정리** (전부 같은 논문 안):
>
> | 출처 | Er0.5 / pristine @ 600 K |
> |---|---:|
> | Fig 3a·3b **MSD 곡선** (40 ps 총 MSD 50 / 10.3 Å²) | **4.9×** |
> | Fig 3d·3e **600 K 마커 실측** (log₁₀D −5.771 vs −6.096) | **2.1×** |
> | Table S5 (D₃₀₀, Eₐ)를 600 K 로 역산 | **0.87×** (Er0.5 가 *더 느리다*) |
>
> → **부호 모순은 해소된다**(마커를 직접 보면 Er0.5 가 빠르다 = MSD 그림과 같은 방향). Table S5 가 어긋난 이유는 그 Eₐ 가 **500 K 오염된 5점 적합**이라 600 K 로 되돌릴 때 틀어지기 때문이다.
> ⚠ **다만 배율은 여전히 2.1× vs 4.9× 로 2.3배 남는다** — 완전 해소는 아니다. MSD 창(적합 구간)이 공개되지 않아 여기까지가 한계다(→ **Q13**).

---

## 7. ★ Lattice dynamics / phonon (§2.3, Fig 4c–4e, §4 Methods) — **우리에게 없는 축**

### 7.1 방법 (원문)

> *"To calculate the **phonon density of states (VDOS)**, a first-principles method combined with lattice dynamics is adopted. A **2 × 2 × 2 supercell** is used to construct the long-range interaction model, and the **displacement step is set to 0.01 Å**… The **VASPKIT** tool is used to generate high-symmetry points… The **second-order force-constant matrix is obtained by density functional perturbation theory (DFPT)**. **Phonopy** is used to postprocess the VASP output results, extract the **phonon dispersion relations and total vibrational density of states (total VDOS)**, and calculate the **element-resolved projected vibrational density of states (projected VDOS)**. To analyse the dynamic behavior of lithium ions in the lattice, the **VDOS distribution of Li is extracted**…
> **The average phonon frequency is obtained from the ratio of the integral of the product of the phonon frequency and phonon VDOS to the integral of the phonon VDOS.**"*

즉:

$$\langle\omega\rangle=\frac{\int \omega\, g(\omega)\, d\omega}{\int g(\omega)\, d\omega} \quad\text{(VDOS 1차 모멘트)}$$

**참조**: [40] VASPKIT(Wang, CPC 2021) · [41] DFPT(Baroni, RMP 2001) · [42] Phonopy(Togo, JPCM 2023).

> ⚠⚠ **방법 서술이 내부 모순이다**: **0.01 Å 변위 스텝**(= 유한변위/frozen-phonon 방식)과 **DFPT**(= 섭동론, 변위를 쓰지 않음)를 **동시에** 적었다. 둘 중 하나만 사실이거나, 두 계산을 섞어 쓴 것이다. **어느 쪽인지 확정 불가.**
> ⚠ DFT+U(4f)가 걸린 상태의 phonon인지, U가 얼마인지, 스핀 처리는 어떻게 했는지 **전부 미기재**.

### 7.2 결과 (Fig 4c/4d/4e = LZC / Er0.5 / Nd0.375)

> *"Compared with LZC, the Er/Nd-doped systems exhibit **enhanced phonon density of states in the low-frequency region, especially at approximately 1–2 THz**, indicating that the introduction of low-ionic-potential rare-earth cations **activates richer low-frequency vibrational modes**. The increase in low-frequency phonon modes usually indicates that the lattice framework possesses **greater dynamic flexibility**, which makes it favourable for the anion framework to undergo **transient structural responses** during Li⁺ migration.[33]
> When Li⁺ passes through the **migration bottleneck region**, the flexible Cl⁻ framework **adapts to Li⁺ migration through local displacement and rearrangement of the charge environment**, thereby **reducing local repulsion and decreasing potential-energy fluctuations** along the migration pathway."*

([33] = **Y. Ren** et al., *Mater. Today Chem.* **2025**, 47, 102869 — **저자 자신의 선행 논문**이 이 해석의 유일한 근거.)

### 7.3 ⚠ 이 절의 증거력 감사 — 냉정하게

| 있어야 할 것 | 있나 | 비고 |
|---|---|---|
| 원소분해 VDOS 3계 (Cl/Li/Zr/Er/Nd) | ✅ Fig 4c–4e | 이 논문의 **진짜 새 자산** |
| **⟨ω⟩ 수치** | ⛔ **없음** | Methods에 정의만 하고 **값은 본문·표·SI 어디에도 없다** |
| **phonon 분산곡선** | ⛔ **없음** | Methods는 "extract the phonon dispersion relations"라 하는데 **그림이 없다** |
| **허수(음의) 진동수 점검 = 동적 안정성** | ⛔ **없음** | 도핑 준안정 구조를 다루면서 동적 안정성 진술 0 |
| Debye 온도 / 열용량 / Grüneisen | ⛔ **없음** | |
| 세 패널의 **공통 정규화** | ⛔ **불명** | Fig 4c y축 최대 ≈8, 4d ≈50, 4e ≈40 (판독). **패널마다 y 스케일이 다르다** → "저주파 DOS가 늘었다"를 **패널 간 높이 비교로 주장할 수 없다** |
| 세 패널의 **공통 x 범위** | ⛔ **아님** | 4c는 0–10 THz, 4d/4e는 0–14 THz. **도핑계가 오히려 더 높은 진동수까지 뻗는다**(판독) — "연화" 서사와 어색하게 공존하며 논문은 언급하지 않는다 |
| 정량 지표(저주파 적분·모드 수) | ⛔ **없음** | "especially at approximately 1–2 THz"라는 정성 서술뿐 |

> ⛔ **판정: "lattice softening"은 이 논문에서 *정량화되지 않았다*.**
> 지지 증거는 (i) 정규화가 불명한 세 VDOS 패널의 육안 비교, (ii) 수치 없는 Raman 적색이동, (iii) 자기 인용 [33] — 셋뿐이다.
> **정의는 해 놓고 값을 안 낸 ⟨ω⟩ 하나만 보고했어도 이 절의 신뢰도는 크게 달라졌을 것이다.**

### 7.4 🔑 그래도 우리가 가져갈 것 — **⟨ω⟩ (VDOS 1차 모멘트)**

우리 캠페인에는 **격자 동역학 축이 없다.** 있는 것은 **정적 탄성(C_ij, E/B/G)** 과 **EOS(B₀)** 뿐이고, 둘 다 **0 K 정적 곡률**이다.
`[Kraft]` digest가 이미 지적했듯 **우리 ε∞(전자 분극성)와 elastic(기계 강성)은 서로 다른 양**이고, Kraft가 실제로 잰 것은 **음속·Debye 진동수** — 즉 **포논 축**이다. 그 칸이 비어 있다.

**⟨ω⟩ = ∫ω g(ω)dω / ∫g(ω)dω 는 그 칸을 채우는 가장 값싼 스칼라다:**
- **DFPT/phonopy 없이도 얻을 수 있다** — MD 속도 자기상관함수(VACF)의 푸리에 변환이 곧 VDOS다. **우리 UMA-MD 궤적(이미 200 ps씩 있다)에서 후처리만으로 나온다.**
- **원소분해가 자연스럽다** — Li만의 VDOS, S/Cl만의 VDOS를 따로 낼 수 있다 → "Cl-rich가 음이온 골격을 무르게 하는가"를 **직접** 볼 수 있다.
- **Kraft의 실험 관측량(Debye ν_D, 음속)의 계산 대응물**이다 → 우리 elastic 체인과 σ 체인을 잇는 다리.
- **`[Deng16]`/`[Torii]`의 정적 C_ij 와 상보**: C_ij는 장파장 극한(음향 모드 기울기), ⟨ω⟩는 전 브릴루앙 영역 평균.

> 🔑 **채택 권고(우선순위 중)**: `tools/ionic/` UMA-MD 궤적에 VACF→VDOS→⟨ω⟩ 후처리 1개 추가.
> comp1 / modelc / +Nd / +B₂O₃ / LPSOCl 에 대해 **원소분해 ⟨ω⟩** 를 내면,
> (a) 우리 elastic 축(E_VRH 22.06 → 27.66)과 (b) 우리 σ 축(Ea 0.253 → 0.224)을 **하나의 물리량으로 연결**할 수 있다.
> ⚠ 단 **UMA는 포논 영역에서 별도 검증이 필요하다**(우리 규율: UMA는 LPSCl MD에 대해서만 검증됨; Li₃N 금지 사례). 도입 시 QE-DFPT 스팟체크 1건 필수.

### 7.5 ⚠⚠ **`[Kraft]`와 정면 충돌** — 이게 이 절에서 가장 중요한 판정

| | **ren2026** (할라이드, 프리프린트, 계산) | **`[Kraft]` 2017 JACS** (우리 물질 Li₆PS₅X, 순수 실험) |
|---|---|---|
| 명제 | **격자가 무를수록 좋다** (저주파 모드↑ → 장벽↓ → σ↑) | **soft lattice ≠ always better** |
| 근거 | VDOS 육안 비교 + Raman 적색이동(수치 없음) | **음속(v_long 1480→1130 ms⁻¹) + Debye ν_D(2.45→1.90×10¹² Hz) + RUS 탄성텐서 + 임피던스** |
| 메커니즘 | 연화 → Eₐ↓ → σ↑ (단조) | 연화 → **Eₐ↓ (0.46→0.30 eV)** *그러나* **prefactor σ₀도 ↓(2.7×10⁷→10³)** = **Meyer–Neldel 보상** → **상쇄** |
| 결론 | 더 무르게 만들어라 | **σ 최적은 중간 강성**(Cl₀.₅Br₀.₅), 양 끝(Cl 단독, I 단독)은 손해 |
| prefactor 논의 | **없음** | **핵심** |

> 🔑🔑 **ren2026은 prefactor를 한 번도 논하지 않는다. 그런데 §6.7에서 우리가 복원해 보니, 그들 자신의 데이터가 R²=0.93의 Meyer–Neldel 보상선 위에 놓여 있다** — Eₐ가 내려간 조성일수록 D₀도 같이 내려간다(Er0.5: Eₐ 0.163 최저, D₀ 2.7×10⁻⁵ 최저).
> **즉 Kraft가 argyrodite에서 실험으로 본 그 보상이 이 논문의 할라이드 계산 안에도 그대로 들어 있고, 저자들은 그것을 보지 못했다.**
> (⚠ 단 우리 §6.7의 해석은 "이 보상은 물리가 아니라 적합 잡음일 가능성이 크다"는 쪽이다 — Kraft의 보상은 **넓은 실측 온도창의 실험**이라 성격이 다르다. **두 보상을 같은 것으로 등치하지 말 것.**)

---

## 8. NEB — Oct–Oct → Oct–Tet–Oct 경로 재구성 (§2.3 후반, Fig 4f–4h)

### 8.1 결과

| 계 | 경로 | 장벽 (eV) |
|---|---|---:|
| **Li₂ZrCl₆** | **direct Oct–Oct** | **0.658** |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** | Oct–Oct | 0.514 |
| " | **Oct–Tet** (협동 경로) | **0.370** |
| **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆** | Oct–Oct | 0.561 |
| " | **Oct–Tet** | **0.417** |

**메커니즘 서술(원문 요지)**: 저-Φ 희토류가 M–Cl을 약화시켜 격자를 연화하고, aliovalent 치환이 추가한 Li⁺가 **Li 자리 점유율과 경로 연결성**을 올린다. 이 시너지로 **원래 고에너지였던 사면체(Tet) 자리가 중간 준안정 상태로 안정화**되고, Li 이동이 **단일 Oct–Oct 직접 도약 → Oct–Tet–Oct 협동 이동**으로 바뀐다. 그 결과 *"converts the originally concentrated high-barrier jump into a **more continuous multistep low-barrier migration process**, thereby smoothing the potential-energy fluctuations."*

### 8.2 ⚠ 감사

1. **NEB 셋업이 통째로 미기재**: 이미지 수, climbing-image 여부, 스프링 상수, 시작/끝 자리, 결함(공공) 도입 여부, 셀 크기, 배경전하 — **전부 없음**. [39] Henkelman–Jónsson 인용만.
2. **Fig 4f–4h의 최종 상태 에너지가 −0.2 eV 부근으로 내려간다**(판독) → **시작/끝 자리가 등가가 아니다.** 그러면 인쇄된 값은 **정방향 1-스텝 장벽**이고, **역방향 장벽은 더 높다.** 장거리 확산의 율속 장벽은 폐경로 전체의 최대값이어야 하는데, 그 논의가 없다.
3. **Oct–Tet–Oct 라면 봉우리가 두 개여야 한다.** Tet가 중간 준안정 상태라면 곡선은 [봉우리1 → 국소최소(Tet) → 봉우리2] 여야 하는데, Fig 4g/4h의 "Oct–Tet" 곡선은 **단봉으로 보인다**(판독). 즉 **인쇄된 0.370 / 0.417은 Oct→Tet 반쪽 장벽일 가능성**이 있고, 그렇다면 **전체 경로 장벽은 더 크다.**
4. **정적 NEB 장벽 ≫ AIMD Eₐ**: 0.658/0.230 = **2.86배**, 0.370/0.163 = **2.27배**, 0.417/0.189 = **2.21배**.
   > 🔑 이건 우리 db의 반복 패턴이다 — `ma2024` digest §"정적 단일경로 장벽(0.5–1.0 eV) ≫ 우리 AIMD Ea(0.22–0.25) = 정적 과대".
   > **단일 경로 정적 NEB는 유효 활성화에너지를 계통적으로 과대평가한다**(협동운동·다중경로·엔트로피 미포함). 이 논문에서도 **비율이 2.2–2.9배로 일정** → 정성 방향(도핑이 장벽을 낮춘다)만 신뢰.
   >
   > ### ⛔ **2026-08-04 이 판정을 부분 철회한다 (→ §20.3)**
   > 이 "2.2–2.9배 일정"은 **NEB 가 과대**해서가 아니라 **AIMD Eₐ 쪽이 500 K 잡음점으로 눌려서** 생긴 격차였다.
   > 500 K 를 뺀 깨끗한 600–900 K 재적합값과 다시 대면 격차가 사라지거나 절반으로 준다:
   >
   > | 계 | NEB | 인쇄 AIMD Eₐ | 비 | **깨끗한 600–900 K Eₐ** | **재비교** |
   > |---|---:|---:|---:|---:|---:|
   > | **Er0.5 (Oct–Tet)** | 0.370 | 0.163 | 2.27배 | **0.372** | **1.005배 — 일치** |
   > | pristine (Oct–Oct) | 0.658 | 0.230 | 2.86배 | **0.332** | 1.98배 |
   >
   > → **Er0.5 에서는 "정적 NEB 과대"가 아예 없다.** pristine 에 남은 2.0배는 협동운동·다중경로로 설명되는 **정상 격차**다.
   > ⚠ **`ma2024` 의 일반 명제(정적 NEB ≫ AIMD)를 부정하는 건 아니다.** 다만 **이 논문을 그 명제의 사례로 인용하면 안 된다** — 여기서는 원인이 반대편에 있었다.

### 8.3 🔑 우리가 가져갈 어휘 — "집중된 큰 봉우리 → 분산된 작은 봉우리"

Fig 1의 도식과 §2.3의 문장(*"smoothing the potential-energy fluctuations along the migration pathway"*)은
우리 `[Dyre]`(**dc Ea = percolation 병목**) · `li_percolation F*`(0.191 → 0.078 eV) · `[Klerk]`(intra-cage 0.10–0.14 vs **inter-cage 0.20–0.25 eV가 율속**) 서사와 **같은 문법**이다.
> **"중간 자리(Tet)를 안정화해서 하나의 큰 병목을 여러 개의 작은 병목으로 쪼갠다"** — 이 표현은 우리 F*(에너지 지형 평탄화) 결과를 설명할 때 그대로 쓸 수 있는 좋은 언어다. **수치 이식은 0, 어휘만.**

---

## 9. ★★ 차원성 — `kim2025_li3ycl6`와의 교차 (우리가 얹는 해석)

### 9.1 같은 골격이다

| | `kim2025` hcp_1 | **ren2026 LZC** |
|---|---|---|
| 물질 | Li₃YCl₆ | **Li₂ZrCl₆** |
| 공간군 | **P3̄m1** | **P3̄m1** (본문 §2.1) |
| XRD 참조 | (Asano 2018) | **Li₃YCl₆형 PDF#44-0286** |
| 확산 차원 | **1D (c축)** — a·b는 같은 층 [YCl₆]³⁻ 2개가 막음 | **?** ← Fig 3a가 답한다 |

### 9.2 Fig 3a–3c 축분해 MSD (600 K, 0–40 ps; 그림 판독, 40 ps 시점 값)

| 계 | 총 MSD | MSD_a | MSD_b | MSD_c | 읽기 |
|---|---:|---:|---:|---:|---|
| **Li₂ZrCl₆** | ≈10 Å² | **≈0** | **≈0** | **≈10** | **사실상 순수 1D (c축)** |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** | ≈50 Å² | **≈21** | ≈8 | **≈21** | **2D (a–c 면)** |
| **Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆** | ≈31 Å² | ≈5 | ≈10 | **≈15** | **준-3D, c 우세** |

(SI Fig S7–S17에 11개 조성 × 600–900 K 축분해 MSD가 전부 있다 — 이 논문의 가장 조밀한 데이터셋인데 본문은 거의 쓰지 않는다.)

> 🔑🔑 **pristine LZC가 1D라는 것은 `kim2025`가 같은 골격(P3̄m1 Li₃YCl₆형)에서 얻은 결론의 독립 재확인이다.**
> 두 논문은 서로를 인용하지 않고, 물질도 다르며(Y³⁺ vs Zr⁴⁺), 저자도 다르다. **골격이 차원성을 정한다**는 명제의 두 번째 데이터점.

### 9.3 ★ 그러면 진짜 기구는 "연화"가 아니라 **차원성 승급(퍼콜레이션)** 일 수 있다

`kim2025` §11.3이 정리한 물리:
- **1D 사슬의 site-percolation 임계는 p_c = 1** → **자리 하나만 막혀도 장거리 경로가 끊긴다.**
- **2D/3D는 p_c < 1** → blocker가 있어도 우회로가 남는다.
- 실증: hcp_1에 **Li–Y antisite 1개**를 넣으면 σ 12.6 → 3.6 → (c 완전차단) 0.6.

**이 프레임으로 Table S5의 Er 계를 다시 읽으면 전부 설명된다:**

| x | σ (mS/cm) | 퍼콜레이션 읽기 |
|---:|---:|---|
| 0 | 1.009 | **1D c-채널만** |
| 0.125 | **0.115** ⬇8.8배 | **Er³⁺ 1개(72원자 셀에 1개)가 1D 채널에 앉아 끊는다** — p_c=1 |
| 0.25 | 0.261 | 여전히 끊긴 상태, 새 경로 미형성 |
| 0.375 | 0.729 | 새 경로가 생기기 시작 |
| **0.5** | **4.004** ⬆ | **2D 망 퍼콜레이션 성립**(Fig 3b: MSD_a가 MSD_c와 동급으로 올라옴) |
| 0.625 | 2.435 | Er 과다 → 다시 blocking |

> 🔑🔑🔑 **이 읽기는 논문의 "volcano" 서술보다 데이터를 훨씬 잘 설명한다** — 특히 논문이 설명하지 못하는 **x=0.125의 8.8배 급락**을.
> 그리고 그 급락은 **"저-Φ 양이온이 격자를 무르게 한다"로는 절대 설명되지 않는다**(Er을 조금 넣어도 무르게 만들 텐데 σ는 8.8배 떨어진다).
> ⚠⚠ **다만 이건 우리 해석이지 논문의 주장이 아니다.** 그리고 §6.7에 따라 그 8.8배 자체가 잡음일 수 있다.
> **확정하려면**: 조성당 배열 앙상블(우리 disorder cfg 규율) + 시드 다중화 + Li 확률밀도 연결성 분석이 필요하다. **미판정으로 기록.**

### 9.4 우리 argyrodite와의 관계

| | 할라이드 (kim2025 · ren2026) | **우리 argyrodite** |
|---|---|---|
| Li 망 차원 | **1D**(P3̄m1) → 도핑/골격으로 2D·3D | **3D** (cage + inter-cage) |
| blocker 1개의 효과 | **자릿수 절단** | **점진적 감쇠** |
| 우리 `dopant_blocking_fraction`의 작동 범위 | — | **3D라서 점진적** |

> 🔑 **이 논문은 `kim2025`가 준 교훈("우리 blocking이 점진적인 이유는 Li 망이 3D이기 때문")의 *두 번째 독립 사례*다.**
> 그리고 **우리 Nd 결과(σ 0.52×, Ea 불변, D₀ 0.65×)** 가 "자릿수 절단"이 아니라 "0.5배 감쇠"로 나타나는 이유를 그대로 설명한다.
> ⛔ 반대로 **이 논문의 Nd가 σ를 5배 올렸다는 사실을 우리 Nd로 옮기면 안 된다** — §14.2-6 참조.

---

## 10. 전고체셀 성능 (§2.4, Fig 5)

### 10.1 셀 구성
- **양극**: 상용 **bare single-crystal NCM811** (코팅 없음)
- **음극**: **Li–In 합금**
- **전해질**: 볼밀한 Li₂.₅Zr₀.₅Er₀.₅Cl₆ / Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆ / pristine LZC
- **⭐ 버퍼층**: *"To suppress possible side reduction reactions of halide electrolytes at low potentials, a **sulphide solid-state electrolyte buffer layer, Li₆PS₅Cl (LPSC)**, is introduced between the Li–In alloy anode and the halide electrolyte"* [34]
- 셀 구조: **Li–In | LPSC | (Er/Nd-doped LZC) | NCM811**
- 조건: **30 °C**, 0.5 C, 전압창 그림상 **2.6–3.6 V vs Li–In/Li⁺** (판독)
- ⛔ **미기재**: 양극 로딩(mg cm⁻²·mAh cm⁻²), 복합양극 조성비, 스택 압력, 층 두께, 셀 면적

### 10.2 결과

| 항목 | 값 |
|---|---|
| **Rate**(Er 계, Fig 5a–5d) | 0.1 C **163.2** / 0.2 C **156.1** / 0.5 C **146.2** / 1 C **129.6** / 2 C **101.5** mAh g⁻¹ |
| 복귀 | 0.1 C 복귀 시 **158.5** mAh g⁻¹ (가역성 양호) |
| pristine LZC 셀 | 고율에서 용량 감쇠 뚜렷 + **충방전 곡선 전압 분극 큼** |
| **장기 사이클**(Fig 5g) | Li–In\|LPSC–Li₂.₅Zr₀.₅Er₀.₅Cl₆\|NCM811 **100 cyc @0.5 C 유지율 82.5 %**, **CE ≈ 99.4 %** — ⚠ **그림 실측은 141.2 → 110.4 mAh/g = 78.2 %, CE 중앙값 98.9 %(99.4 는 최댓값)** (→ §20.9) |
| Nd 계(Fig 5h) | *"relatively stable cycling performance"* (수치 미제시) |
| **ex-situ XPS**(Fig 5e/5f, S20) | 사이클 후에도 **Zr 3d·Cl 2p 피크 형태 안정, 새로운 분해산물 신호 없음** |

### 10.3 ⚠ 감사
- **이 논문에는 산화 안정성(ESW) 계산이 없다.** grand-potential도, CV/LSV도, 분해상 예측도 **0건**. 유일한 안정성 증거는 **사이클 후 XPS "새 피크 없음"** 이라는 정성 관찰.
- **음극 쪽은 자기 재료로 못 버텨서 황화물(LPSC)을 끼웠다.** 즉 이 논문 스스로 **할라이드의 환원 취약성**을 인정하고 우회했다.
  > 🔑 **우리 캠페인 관점에서 이건 오히려 좋은 그림**: *양극측 = 할라이드(산화 내성), 음극측 = 황화물 LPSCl(환원측 파트너)* 라는 역할 분담. `[Cha]` dual-compatibility·`[Son]`(LPSCl "<2.5 V") 서사와 정합.
- **Coulombic efficiency 99.4 %에 100 사이클이면 누적 손실이 ~45 %** 여야 하는데 유지율은 82.5 %다 — CE가 초기 몇 사이클을 제외한 평균이거나 정의가 다를 수 있다. **본문에 정의가 없다**(⚠ 확정 불가).
- **pristine LZC 셀의 100 사이클 유지율이 보고되지 않았다** → "도핑이 사이클을 개선했다"는 비교가 rate 데이터에만 있고 장기 사이클에는 없다.

---

## 11. Figure set 전수 ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 / 경고 |
|---|---|---|
| **1** | 설계 도식. 상: pristine LZC = 강한 Zr–Cl·rigid Cl 골격·**Direct Oct–Oct**·단일 높은 장벽. 하: Er/Nd 도핑 = 약한 M–Cl·연화/분극성 Cl 골격·**Relay Oct–Tet–Oct**·**"Lower distributed barriers"** | ★ **"큰 봉우리 하나 → 작은 봉우리 여러 개"** 도식 문법. 우리 `li_percolation F*` 결과 설명용 그림 언어로 즉시 차용 가능 |
| **2a** | pristine LZC + Er0.5 + Nd0.375 결정구조 + [ZrCl₆]/[ErCl₆]/[LiCl₆]/[NdCl₆] 다면체 갤러리 | 다면체 단위 카탈로그 제시 양식 |
| **2b** | XRD 5시료 + Li₃YCl₆ PDF#44-0286 참조선. 도핑 시 **저각 이동** | 격자 팽창의 1차 증거 |
| **2c** | Rietveld 2건 (Obs/Cal/Diff/Bragg). **R_wp 4.596·R_p 3.72·GOF 1.76**(Er) / **4.86·4.07·1.89**(Nd) | ⛔ **정련 파라미터 표(격자상수·좌표·점유율) 없음** |
| **2d** | **Zr 3d** XPS 3시료 (3d₅/₂·3d₃/₂) — 도핑 후 "약간 이동" | ⛔ **이동량 수치 없음** |
| **2e** | **Cl 2p** XPS 3시료 (2p₃/₂·2p₁/₂) | ⛔ 동일 |
| **2f** | **Er 4d** / **Nd 3d** XPS — Er³⁺·Nd³⁺ 확인 | 산화수 확인용 |
| **2g** | **Raman** 3시료, 100–500 cm⁻¹. [ZrCl₆]²⁻ 피크 **broadening + slight redshift** | ★ **연화의 유일한 실험 증거**. ⛔ 수치 없음 |
| **2h** | SEM + EDS 맵 (Zr Lα / Er Lα / Nd Lα / Cl Kα), 10 µm·20 µm 스케일 | 균일 편입 확인 |
| **3a–3c** | ★★ **축분해 MSD (600 K, 0–40 ps)** — LZC / Er0.5 / Nd0.375, 각각 총 MSD + a·b·c 성분 | ★★ **이 논문 최고의 데이터.** §9.2 차원성 판정의 근거. **우리 MSD는 등방 총합만 — 축분해는 우리 공백(채택 후보)** |
| **3d** | **Er 계 아레니우스** ln D vs 1000/T (6계) + Eₐ 라벨 | ⛔⛔ **§20.1–20.3 에서 전부 확정됨.** y축 라벨 "ln(D)" 는 **오류 — 실제는 log₁₀(D)**(적합선 기울기가 인쇄 Eₐ 를 4자리까지 재현, 3건). **500 K 점은 존재한다**(12/12 계열, 1000/T = 2.000). 그리고 그 점이 **헤드라인 Eₐ 를 만들었다** — Er0.5 는 D(500 K) > D(600 K) 로 비물리적이고, 빼면 Eₐ 0.163 → **0.372 eV** |
| **3e** | **Nd 계 아레니우스** (6계) | 동일 |
| **3f** | **D·Eₐ·σ 3중 막대** 11계 = Table S5의 그림판 (Eₐ는 10⁻¹ eV 단위로 인코딩) | ⛔ **오차막대 0** |
| **3g** | **EIS Nyquist** 5시료 (RT) + pristine 확대 inset | ⛔ 등가회로·피팅·bulk/GB 분리 없음 |
| **3h** | **실측 σ 막대** 0.23 / 0.81 / 1.13 / 0.76 / **1.32** mS cm⁻¹ | ⛔ 오차막대 0, n 미기재 |
| **4a** | ★ **서술자 지도** — x = Φ̄_Me/Φ̄_X (1.3–2.1), y = Φ̄_Li (22–34 nm⁻¹), 18계 산점 | ⛔⛔ **두 축 모두 정의식 없음 + σ 인코딩 없음** → 구조–물성 주장 불가(§4.6) |
| **4b** | **Φ vs σ 이중 막대** 18계 (Table S6) | ⛔ **우리 재분석 R² = 0.065**(§4.5). 축 라벨 단위 오기("Å⁻¹" → 실제 pm⁻¹; 범례 "10⁻¹/Å⁻¹") |
| **4c–4e** | ★ **원소분해 VDOS** — LZC(0–10 THz) / Er0.5(0–14) / Nd0.375(0–14), 범례 VDOS·Cl·Li·Zr(+Er/Nd) | ★ **우리 공백 축의 실물 예시**. ⛔ **y 스케일이 패널마다 다르고(≈8/50/40) x 범위도 다르다** → 패널 간 높이 비교 무효(§7.3) |
| **4f** | **NEB 3계 중첩** — LZC / Er0.5 / Nd0.375, x = Migration pathway (Å) 1–7 | 본문 값 0.658 / 0.370 / 0.417 eV. **곡선 끝이 −0.2 eV로 내려간다**(비등가 종점, §8.2) |
| **4g** | **Er 계 Oct–Tet(0.370) vs Oct–Oct(0.514)** | ★ 경로 비교 제시 양식 |
| **4h** | **Nd 계 Oct–Tet(0.417) vs Oct–Oct(0.561)** | 동일 |
| **5a–5c** | Rate 충방전 곡선 3시료 (0.1/0.2/0.5/1/2 C), y축 **V vs Li–In/Li⁺ 2.6–3.6 V** | ⚠ In/InLi 기준 전압축 — Li 기준 환산 시 오프셋 주의(우리 db 규율) |
| **5d** | Rate 성능 비교 3시료 (30 cyc) | pristine의 고율 열세 |
| **5e/5f** | 사이클 전/후 **Zr 3d / Cl 2p XPS** (Er 계) | 계면 화학안정성 정성 증거 |
| **5g** | Er 계 **100 cyc @0.5 C, 30 °C — 82.5 % / CE 99.4 %** | ⛔ pristine 대조 없음 |
| **5h** | Nd 계 100 cyc | ⛔ 수치 미제시 |
| **S1 / S2** | Er / Nd **6개 도핑 농도 결정구조** 전수 | 배열 시각화 (좌표표는 없음) |
| **S3 / S4** | Nd0.25 / Er0.25 **Rietveld** | 본문 Fig 2c의 보조 |
| **S5 / S6** | Er0.5 / Nd0.375 **SEM 1 µm** | |
| **S7–S17** | ★★ **11개 조성 × 600–900 K 축분해 MSD 전수** | ★★ **이 논문의 가장 조밀한 원데이터인데 본문이 거의 안 쓴다.** 차원성×농도×온도 3중 지도가 여기 있다 |
| **S18 / S19** | ★ Er / Nd **6개 농도의 "channel structures"** | 확산 채널 기하 — `kim2025` Fig S11(Li–Li 거리)과 같은 가족일 가능성. ⛔ **캡션에 정의·수치 없음** |
| **S20** | Nd0.375 사이클 전/후 XPS | |
| **Table S1/S2** | Er/Nd 계 **Total Energy + "Binding Energy"** 6농도 | ⛔ 참조상태 미기재 = 재현 불가(§5.1) |
| **Table S3/S4** | 최적 2조성 **격자상수(계산 vs 실험)** | ⛔ **두 표의 계산값이 완전 동일**(§5.3) |
| **Table S5** | ★★ **D·Eₐ·σ 11계 전수** | ★★ 이 논문 계산 결과의 정본. §6.2–6.7 전부 여기서 나옴 |
| **Table S6** | ★★ **18계 Φ + σ + ref** | ★★ §4.2 역산 검증·§4.5 상관 붕괴의 근거 |

---

## 12. Post-processing ★

| 무엇 | 도구 | 어떻게 수치화/기록 |
|---|---|---|
| **확산 통계** | **pymatgen** [38] | MSD(eq 2) → D = MSD/(2·d·Δt), d=3 (eq 3) → 아레니우스 D = c·exp(−Eₐ/k_bT) (eq 4) → **NE σ = nq²D/(k_bT)** (eq 5), Haven 보정 없음 → Table S5 |
| **Li 확률밀도** | (도구 미명시; pymatgen 계열 추정) | 공간확률밀도 분포 (Fig 3a–3c 삽입 그림, Fig S18/S19) |
| **축분해 MSD** | (미명시) | a/b/c 성분 분리 (Fig 3a–3c, S7–S17) ← **이 논문의 핵심 관측량** |
| **NEB** | VASP + [39] Henkelman–Jónsson | 경로별 에너지 프로파일 (Fig 4f–4h). ⛔ 이미지 수·CI 여부 미기재 |
| **Phonon(VDOS)** | **VASPKIT**[40](고대칭점) + **DFPT**[41] + **Phonopy**[42], 2×2×2 슈퍼셀, 변위 0.01 Å | total VDOS + **원소분해 projected VDOS** (Fig 4c–4e) + Li VDOS 추출 + **⟨ω⟩ 정의**(값 미보고) |
| **구조 시각화** | **VESTA** | Fig 2a, S1, S2 |
| **응집에너지** | VASP | SI eq (1), Table S1/S2. ⛔ 참조상태 미기재 |
| **XPS 피팅** | **Avantage**, Gaussian–Lorentzian, C 1s 284.8 eV 보정 | Fig 2d–2f, 5e/5f, S20 |
| **XRD 정련** | Rietveld (프로그램 미명시) | R_wp·R_p·GOF만 보고 |
| **Bader / COHP / ELF / 전하밀도차 / DOS(전자) / band gap** | — | ⛔ **전부 없음** ← §4.4 판정의 핵심 |
| **E_hull / 상안정성 / 분해상** | — | ⛔ **없음** |
| **ESW / grand-potential / CV / LSV** | — | ⛔ **없음** |
| **탄성 C_ij / EOS** | — | ⛔ **없음** |
| **BVSE** | — | ⛔ 없음 |

---

## 13. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

> ⛔⛔ **이 표는 "방법 대조표"다. 수치 대조표가 아니다.**
> 물질군(**할라이드 Li₂ZrCl₆** vs **황화물 argyrodite Li₆PS₅Cl**)이 다르고 이 논문은 **동료심사 전 프리프린트**다.
> **어떤 값도 우리 물성 4축에 편입하지 않는다.**

| 항목 | **ren2026 (Li₂ZrCl₆, 프리프린트)** | **우리 (comp1 / modelc)** | 판정 |
|---|---|---|---|
| **물질군** | 할라이드, [MCl₆] 팔면체 + hcp Cl 부격자, **P3̄m1** | 황화물 argyrodite, PS₄³⁻ 사면체 + Li cage, **F4̄3m** | **수치 비교 불가** |
| **σ 파이프라인** | MSD → D → 아레니우스 → **NE(Haven=1)** → 300 K | **동일** | ✓ **형식 완전 일치** |
| **힘 엔진** | **AIMD** (VASP/PBE/PAW/Γ/2 fs/NVT-NH) | **MLIP-MD** (UMA-s-1p1 omat, Langevin NVT, dt 2 fs, friction 0.02) | **다름 — "둘 다 AIMD"라 부르지 말 것**(baseline 경고) |
| **온도창** | **600·700·800·900 K (4점)** → 300 K | **600/800/1000 K (3점)** → 300 K (400/500 K 제외 판정) | ○ 유사. 둘 다 **T 2배 밖 외삽** |
| **실행길이** | **50 ps** (평형화 분리 언급 없음) | equilib 5 ps / prod **200 ps**, **MSD 창 2–50 ps 고정** | **우리 4배 길고 창 규약이 명시** |
| **셀 / 캐리어 수** | **72원자, Li 16–21개** (우리가 역산 확정, §6.3) | 우리 표준 셀 (Li 수 훨씬 많음) | **그들이 훨씬 얇다** |
| **시드 / 오차막대** | **1 / 없음** | modelc **3-seed** (Ea 0.197±0.032), 600 K 3-시드 오차막대 규약 | **우리 우위 (명확)** |
| **무질서·배열 처리** | **조성당 배열 1개**("structural optimization으로 stable configuration") | enumerate → lowest-Ewald → **UMA anneal 700 K 20 ps + relax** → **cfg 앙상블(d=0.5/1.0 × cfg0/1/2)**, 배열 간 분산으로만 판정 | **우리 우위 (2단계)** |
| **σ 절대값 취급** | 초록·결론에 단언 | **인용 금지 규율**, 비율도 멀티시드 판정만 | **우리 우위** |
| **Meyer–Neldel / prefactor** | **논의 없음** (우리가 복원: R²=0.93, E_MN 57 meV) | **Nd σ-drop을 D₀ 0.65×·Ea 불변으로 분해** = prefactor 축을 명시적으로 씀 | **우리 우위** |
| **정적 완화** | 520 eV, 3×3×3 k, F<0.02 eV/Å | QE 계열, 완화격자 | ○ 동급 |
| **DFT+U** | Er/Nd **4f에 적용, U 값 미기재** | (해당 없음) | ⛔ 재현 불가 |
| **vdW** | **없음** | — | ○ |
| **band gap / 전자구조** | **계산 0** | comp1 **2.066** / modelc **2.099** eV (fixed-occ nscf) | **비교 불가**(값 자체가 없음) |
| **Bader / ICOHP** | **0건** | Bader 보유, **ICOHP(Li–Cl) −1.86 / −2.10** (LOBSTER) | **우리 우위 — §4.4 판정의 근거** |
| **산화 onset / ESW** | **0건** | **2.256 V** (S²⁻-limited, 축①), 환원 1.242 / OCV 1.717 V | **그들 축 아님** |
| **기계 물성** | **0건** | E_VRH 22.06 / 27.66 GPa, B₀ 26.23 / 21.71 GPa, 전 C_ij | **우리 우위** |
| **phonon / VDOS** | **있음** (원소분해 VDOS 3계, ⟨ω⟩ 정의) | **없음** | ⚠⚠ **우리 공백 — 채택 후보 §7.4** |
| **NEB** | **있음** (Oct–Oct 0.658 → Oct–Tet 0.370/0.417) | 없음(우리는 MD 기반 Ea) | ○ 상보. 단 정적 NEB는 2.2–2.9배 과대(§8.2-4) |
| **축분해 MSD (a/b/c)** | **있음 — 핵심 관측량** | **없음** (등방 총합만) | ⚠ **우리 공백 — 채택 후보** |
| **실험 대조** | **있음** (EIS σ_RT 5점) — 단 **실험 Eₐ 없음** | (문헌 대조) | ○ 그들 강점, 단 얕음 |
| **E_hull / 상안정** | **없음**(응집에너지만, 참조상태 미기재) | host 상대 Δe | 둘 다 약함 |

---

## 14. 적용 인사이트 — 우리 연구에 어떻게

### 14.1 ✅ 가져갈 것 (개념·방법)

1. **⟨ω⟩ = VDOS 1차 모멘트** — 우리 격자동역학 공백을 채우는 **가장 값싼 스칼라**. UMA-MD 궤적의 VACF→FFT 후처리로 즉시 가능(§7.4). `[Kraft]`가 실험으로 잰 Debye ν_D·음속의 계산 대응물이 되고, 우리 elastic(C_ij)·EOS(B₀) 축과 σ 축을 잇는다.
   ⚠ 도입 시 **UMA 포논 영역 검증(QE-DFPT 스팟체크)** 필수.
2. **원소분해 VDOS** — "Cl-rich가 *음이온 골격*을 무르게 하는가"를 직접 볼 수 있는 유일한 관측량. comp1 vs modelc vs +Nd vs +B₂O₃ 비교에 그대로 적용 가능.
3. **축분해 MSD (a/b/c)** — `kim2025`에 이은 **두 번째 채택 근거**. 우리 modelc(rhombo-62)·슬랩·GB처럼 이방성이 있는 셀에서 즉시 정보가 된다. 코드 몇 줄.
4. **"집중된 큰 봉우리 → 분산된 작은 봉우리" 어휘** — 우리 `li_percolation F*`(0.191→0.078 eV)·`[Dyre]`·`[Klerk]` inter-cage 서사를 설명하는 그림 언어(§8.3). **수치 이식 0, 어휘만.**
5. **Φ = Z/r 을 *0-비용 사전 필터*로만** — 우리 47-dopant cascade의 후보 정렬에 **비용 0**으로 붙일 수 있다. 단 §4.5의 R²=0.065를 **반드시 병기**하고, **랭킹 지표가 아니라 "극단값 배제"용**으로만(예: Mo⁶⁺급 초고-Φ는 캐리어를 빼앗으니 후순위).
6. **"고-Φ vs 저-Φ 딜레마"의 명료한 서술** — 고원자가 도핑은 inductive 이득을 주지만 Li를 빼앗고, 저원자가 도핑은 Li를 주지만 inductive 이득이 없다. **우리 co-doping 서사(σ·안정 동시개선)의 정확한 문제 정의**이며, 우리 cascade가 이 trade-off를 ML로 다루고 있다는 포지셔닝 문장이 된다.
7. **역할 분담 그림** — *양극측 = 할라이드(산화 내성) / 음극측 = 황화물 LPSCl(환원 파트너)*. 이 논문이 자기 셀에 **LPSC 버퍼를 끼운 것**이 그 실증이다(§10.3). `[Cha]`·`[Son]`과 한 줄에 놓인다.
8. **재분석 프로토콜 자체** — §6.3(NE 역산으로 셀·N·V 확정), §6.7(D₀ 복원 → Meyer–Neldel → 온도별 분산)은 **앞으로 모든 AIMD-σ 논문에 적용할 표준 감사 절차**다. 재사용 권장.

### 14.2 ⛔ 이식 금지

1. **모든 σ·D·Eₐ 절대값** (1.32 / 1.13 / 0.227 mS cm⁻¹, 4.004 / 3.56 / 1.0088, 0.163 / 0.189 / 0.23 eV). 할라이드 + 프리프린트 + 외삽 인공물(§6.7) + 오차막대 0.
2. **NEB 장벽 0.658 / 0.370 / 0.417 eV** — 다른 물질, 셋업 미기재, 종점 비등가, 정적 과대(2.2–2.9배).
3. **격자상수·응집에너지** — 참조상태 미기재, 두 표 값 동일 이상.
4. **"저 이온퍼텐셜이 좋다" 명제** — 그들 자신의 Table S6에서 **R² = 0.065**로 지지되지 않음(§4.5).
5. **"volcano 농도 의존" 서사** — Er 계에서 자기 SI와 모순(§6.4), 그리고 §6.7에 따라 잡음일 가능성.
6. **⛔⛔ 이 논문의 Nd 결과를 우리 Nd 결과와 병치 금지.**
   - 그들: **Nd³⁺가 Zr⁴⁺ 자리를 aliovalent 치환 → Li 캐리어 +19 % → σ 5배↑** (할라이드).
   - 우리: **Nd 도핑 → σ 0.52×, Ea 0.224→0.227(불변), D₀ 0.65×** (황화물 argyrodite).
   - **같은 원소지만 다른 물질·다른 자리·다른 전하보상.** "Nd가 좋다/나쁘다"를 원소 수준에서 일반화하면 틀린다.
   - ⚠ 부수적으로: 우리가 복원한 그들 Nd0.375의 D₀/D₀(pristine) = **0.61×** 가 우리 Nd D₀ **0.65×** 와 비슷하다. **이건 우연이다.** 두 숫자를 같은 표·같은 문장에 넣지 말 것.
7. **Φ̄_Li · Φ̄_Me/Φ̄_X** — 정의식이 없다. 사용 불가.
8. **"lattice softening이 σ를 올린다"의 단조 형태** — `[Kraft]`가 우리 물질에서 **실험으로 반증**한 형태다(§7.5). 우리 문서에 쓰면 Kraft와 충돌한다.

---

## 15. 우리 캠페인 액션 아이템 (우선순위)

| # | 액션 | 근거 절 | 난이도 |
|---|---|---|---|
| **A1** | **VACF → VDOS → ⟨ω⟩ 후처리 파이프라인**을 `tools/ionic/` 에 추가. comp1/modelc/+Nd/+B₂O₃/LPSOCl 원소분해 ⟨ω⟩. QE-DFPT 스팟체크 1건으로 UMA 검증 | §7.4 | 중 (궤적은 이미 있음) |
| **A2** | **축분해 MSD(a/b/c)** 를 기존 MSD 파이프라인에 추가 (등방 총합 → +3성분) | §9.2, `kim2025` | 하 |
| **A3** | **AIMD/MD-σ 논문 감사 체크리스트 3종** 을 `kb/` 에 문서화: ①NE 역산으로 셀·N·V 확정 ②D₀ 복원 → Meyer–Neldel → E_MN vs kT(시뮬) ③시뮬 온도 vs 외삽 온도의 분산 비교 | §6.3, §6.7 | 하 |
| **A4** | cascade에 **Φ = Z/r 열 추가**(0-비용) — 단 **랭킹 아닌 극단값 배제용**, R²=0.065 캐비앳 동반 | §4.5, §14.1-5 | 하 |
| **A5** | 우리 Bader/ICOHP 열을 **"lee2024 축 vs ren2026 축"** 으로 재해석한 1장 노트 — "z/r은 축을 가리키지만 부호·크기는 전자구조만 준다" | §4.4 | 하 |

---

## 16. ⚠ 주의 / 한계 (over-claim 방지) — 비판적으로

> **0. 대전제: 동료심사를 통과하지 않은 프리프린트다.** 아래 문제 중 상당수는 심사 과정에서 교정될 수 있는 종류다. **현 상태를 최종본으로 인용하지 말 것.**

1. **헤드라인 서술자 Φ가 자기 데이터에서 작동하지 않는다.** Table S6 18계에서 **R² = 0.065, Spearman = −0.089**. 같은 Φ=0.0781에서 Ta 1.42 vs Nb 0.55. **Li 함량이 3배 나은 예측자**(§4.5). 그럼에도 초록·결론은 *"descriptor-driven design strategy"* 를 단언한다.
2. **"lattice softening"이 정량화되지 않았다.** ⟨ω⟩를 **정의만 하고 값을 안 냈고**, VDOS 세 패널은 **y축 스케일이 서로 다르며**, phonon **분산곡선·허수모드 점검이 없다**(§7.3).
3. **기구의 전자구조 절반이 계산되지 않았다.** "M–Cl 상호작용 약화"를 주장하면서 **Bader·COHP·전하밀도차 0건**. 유일한 증거는 수치 없는 XPS "약간 이동"과 수치 없는 Raman "약간 적색이동"(§5.4, §5.5).
4. **AIMD 격차가 외삽 산물이다.** 600–900 K 실측 구간 분산 **2.3–3.6배** → 300 K 외삽 **29.6배**. Meyer–Neldel 보상선 R²=0.93, **E_MN = 57 meV ≈ 시뮬 온도창의 kT**(§6.7). 50 ps·16–21 Li·단일 시드·단일 배열.
5. **계산 파이프라인이 조성별 격자 팽창을 반영하지 않았다.** Table S3/S4의 계산 격자상수가 두 조성에서 동일하고, NE 역산 결과 11개 조성 전부 단일 부피(§5.3, §6.3-4). **그런데 격자 팽창은 이 논문 기구 주장의 한 축이다.**
6. **본문 "volcano" ↔ SI Table S5 모순.** Er 계는 첫 도핑에서 σ가 **8.8배 하락**한다 — "먼저 증가"가 아니다(§6.4).
7. **이론–실험 방향 모순 1건.** Er x=0.25에서 AIMD는 "4배 악화", 실험은 "3.35배 개선"(§6.6). 논문은 *"high consistency"* 라 쓴다.
8. **무질서 정량 0.** 45 h·700 rpm 볼밀 무열처리 시료인데 자리 무질서(Li/Zr/Er 분배, 공공)를 재지도 모형화하지도 않았다. `[Schlem]`이 같은 삼방 할라이드에서 **볼밀 88–100 % vs 앰풀 2.5 %** 로 σ 18배를 만든 바로 그 변수다.
9. **실험 Eₐ가 없다.** 온도의존 EIS 미수행 → 계산 Eₐ의 실험 검증 0. bulk/GB 분리·펠릿 밀도·측정 압력·블로킹 전극 **전부 미기재**(§6.5).
10. **NEB 셋업 전면 미기재 + 종점 비등가**(끝 에너지 −0.2 eV) → 인용된 장벽이 율속 장벽이라는 보장이 없다(§8.2).
11. **DFT+U의 U 값 미기재**, 스핀 처리 미기재, 4f core-freezing 여부 미기재 → **희토류 계산의 핵심 파라미터가 없다 = 재현 불가.**
12. **phonon 방법 서술 모순** — 유한변위(0.01 Å)와 DFPT를 동시에 적었다(§7.1).
13. **응집에너지 참조상태 미기재 + 값이 인쇄된 식과 자릿수 불일치** → 재현 불가. **E_hull·분해상 검사 0**(§5.1).
14. **Table S6 표기 오류 다수**: 자기 논문 최적 조성 화학식 오기("Li₀.₅Zr₀.₅Er₀.₅Cl₆"), Cu 계 "Li₆"(→Cl₆), Mo 계 **전하 불균형**.
15. **pristine LZC σ가 한 논문 안에 3개 값** (0.40 / 0.28 / 0.227) — 어느 것을 기준으로 "6배"인지에 따라 3.3배~5.8배로 달라진다.
16. **원고 자체가 미교정 상태** — "he Li⁺ diffusion", "In summary, t a low-ionic-potential", "in in LZC", "cation chemical, characteristics", "To further quantitatively analyses" 등 오탈자 다수 + Authorea 키워드 필드가 중복 덤프("solar cells, carbon materials, photovoltaics…" 반복). **프리프린트 지위의 방증.**
17. **셀 데이터가 벤치마크 불가** — 로딩·압력·두께·면적 미기재, pristine 100 cyc 대조 없음, CE 99.4 %와 유지율 82.5 %의 산술 관계 불명(§10.3).
18. **차원성(1D→2D) 프레임을 쓰지 않았다** — 자기 Fig 3a–3c와 Fig S7–S17이 그 답을 갖고 있는데도. §9.3의 퍼콜레이션 읽기는 **우리 해석이지 논문의 주장이 아니다**(그리고 미판정이다).

---

## 17. 인용 가능 문장 (deck/paper용) — **전부 프리프린트 꼬리표 필수**

- **"Ren et al.(Authorea **프리프린트**, 동료심사 전, 2026)는 할라이드 Li₂ZrCl₆에서 **이온퍼텐셜 Φ = Z/r**(Z=양이온 가수, r=배위 이온반경)을 조성 설계 서술자로 제안하고, Zr⁴⁺를 저-Φ 희토류 Er³⁺/Nd³⁺로 aliovalent 치환해 실온 이온전도도를 약 5–6배 올렸다고 보고한다."**
  *(⛔ σ 절대값 없이. 우리 황화물 문맥으로 옮기지 않는다.)*
- **"중심 양이온이 음이온을 얼마나 세게 붙드는가 하는 축은 두 방향에서 접근된다 — 고원자가 쪽에서는 M–X 공유성 증가로 음이온 유효전하를 낮추는 inductive effect[Lee 2024]로, 저원자가 쪽에서는 M–X 약화로 음이온 골격을 유연화하는 lattice-softening[Ren 2026 **프리프린트**]으로. 두 처방은 같은 축에서 반대 부호를 가리키므로, 이 축에는 최적점이 존재한다."**
  *(★ §4.4·§4.5 판정의 압축. 우리 co-doping 서사의 문제 정의로 그대로 사용 가능.)*
- **"이온퍼텐셜 z/r 은 계산이 필요 없는 0-비용 서술자이지만, Ren et al.(**프리프린트**)의 18계 Li₂ZrCl₆ 치환 표를 재분석하면 실온 전도도 분산의 **6.5 %만 설명**하며(Pearson r = −0.26, Spearman = −0.09), 같은 Φ 값에서 σ가 2.6배 갈리는 쌍(Ta⁵⁺/Nb⁵⁺)이 존재한다. 따라서 z/r 은 음이온 전하(Bader)·결합세기(ICOHP) 같은 전자구조 관측량을 **대체하지 못한다**."**
  *(★★ 이 digest의 최대 수확. 우리 cascade descriptor 방어 논거.)*
- **"고온 AIMD로 얻은 활성화에너지·전지수 인자 쌍이 Meyer–Neldel 보상선 위에 놓이고 그 특성에너지가 시뮬레이션 온도의 kT와 같은 크기라면, 실온으로 외삽한 전도도 서열은 물리가 아니라 적합 잡음의 증폭일 수 있다 — Ren et al.(**프리프린트**)의 11개 조성은 600–900 K에서 확산계수가 2.3–3.6배 안에 모여 있으나, 300 K로 외삽하면 29.6배로 벌어진다."**
  *(★★ 우리 AIMD-σ 감사 표준 문장. 재사용 권장.)*
- **"P3̄m1 Li₃YCl₆형 골격의 Li 확산은 본질적으로 c축 1차원이며[Kim 2025], 같은 골격의 Li₂ZrCl₆에서도 축분해 MSD가 a·b 성분의 소멸을 보인다[Ren 2026 **프리프린트**]. 1차원 망은 site-percolation 임계가 p_c = 1이라 결함 하나로 장거리 수송이 끊기는 반면, argyrodite의 3차원 Li 망은 같은 blocking에도 점진적으로만 감쇠한다."**
  *(★ 우리 `dopant_blocking_fraction` 작동범위 설명용. 두 번째 문헌 사례.)*
- **"할라이드 전해질은 고전압 양극 쪽에서 유리하지만 저전위에서 환원에 취약해, Ren et al.(**프리프린트**)조차 Li–In 음극과 도핑 Li₂ZrCl₆ 사이에 **황화물 Li₆PS₅Cl 버퍼층**을 삽입해야 했다."**
  *(★ 우리 LPSCl의 역할 포지셔닝.)*
- ⛔ **사용 금지**:
  - "낮은 이온퍼텐셜 원소를 넣으면 이온전도도가 올라간다" — **그들 자신의 18계 표가 지지하지 않는다**(§4.5).
  - "격자를 무르게 하면 전도도가 올라간다" — `[Kraft]`가 우리 물질에서 **실험으로 반증한 형태**(§7.5).
  - "Nd 도핑은 σ를 올린다" — **할라이드에서의 aliovalent 캐리어 효과**이며, 우리 황화물 Nd 결과(σ 0.52×)와 정반대다(§14.2-6).
  - 이 논문의 **어떤 σ/Eₐ/장벽 절대값**도 우리 표·그림에 넣지 않는다.

---

## 18. 용어 미니사전

- **Ionic potential (이온퍼텐셜) Φ = Z/r**: 양이온의 형식전하를 이온반경으로 나눈 값. "polarizing power"(분극력)·"surface charge density"의 고전적 지표. 값이 클수록 음이온 전자구름을 세게 끌어당긴다(→ 공유성↑, 음이온 유효전하↓). **이 논문에서는 pm⁻¹ 단위, Shannon 6배위 반경, 치환 양이온 하나만**(§4.2).
- **Solid-electrolyte inductive effect**: 고산화수 중심 양이온이 음이온의 전자를 끌어당겨 **음이온–Li 정전 인력을 약화**시켜 Li 이동을 촉진하는 효과. `lee2024`가 Bader 전하로 정량화(Si⁴⁺ 중심 S −1.48 e⁻ vs W⁶⁺ 중심 −0.84 e⁻). **유기화학의 유발효과(inductive effect)에서 온 이름.**
- **Aliovalent substitution (이가 치환)**: 원래 자리와 **다른 가수**의 이온으로 치환하는 것. 전하중성을 맞추려면 캐리어(Li⁺)나 공공이 따라 들어온다. Zr⁴⁺ → Er³⁺ 하나당 **Li⁺ 하나 추가**. ↔ isovalent(등가) 치환.
- **Lattice softening (격자 연화)**: 결합이 약해져 진동수(포논)가 낮아지는 것. 관측량 = Raman **적색이동**, VDOS **저주파 증가**, 음속·Debye 온도 하락, 탄성계수 감소.
- **VDOS / phonon DOS g(ω)**: 진동 모드가 진동수 ω 근처에 얼마나 많은지의 분포. **원소분해 VDOS** = 각 원소가 어느 진동수 대역에 기여하는지. MD 궤적의 **속도 자기상관함수(VACF)를 푸리에 변환**해도 얻는다.
- **⟨ω⟩ (평균 포논 진동수, VDOS 1차 모멘트)**: ∫ω g(ω)dω / ∫g(ω)dω. 격자 강성/무름의 **단일 스칼라 요약**. Debye 온도와 같은 가족.
- **DFPT (density functional perturbation theory)**: 외부 섭동(원자 변위)에 대한 응답을 해석적으로 풀어 힘상수 행렬을 얻는 방법. **유한변위(frozen phonon)와 다른 경로**이며, 보통 둘 중 하나만 쓴다.
- **Oct–Tet–Oct 협동 이동**: Li가 팔면체(Oct) 자리에서 다른 Oct로 갈 때, 중간의 사면체(Tet) 자리를 **준안정 중간체**로 거치는 경로. 하나의 큰 장벽이 두 개의 작은 장벽으로 쪼개진다.
- **Nernst–Einstein (Haven = 1)**: σ = n q² D/(k_BT). 이온 간 상관을 무시하는 근사 — **협동 운동이 있으면 σ를 과소평가**한다(`[Adeli]` argyrodite 실측 Haven 0.23–0.3). 이 논문·우리 둘 다 보정 없음.
- **Meyer–Neldel rule / 보상효과**: 여러 시료에서 ln(전지수 인자) 가 활성화에너지에 **선형 비례**하는 현상, ln D₀ = ln D₀₀ + Eₐ/E_MN. 그 결과 **T_iso = E_MN/k_B 에서 모든 시료의 값이 교차**한다. 진짜 물리(엔트로피–엔탈피 보상)일 수도 있고, **좁은 온도창 적합의 통계 인공물**일 수도 있다 — **E_MN이 측정/시뮬 온도의 kT와 비슷하면 후자를 강하게 의심**해야 한다(§6.7).
- **Isokinetic temperature (T_iso)**: 보상선이 교차하는 온도. 그 온도에서는 모든 시료가 사실상 같은 값을 갖는다.
- **Site percolation threshold p_c**: 무작위로 자리를 막을 때 장거리 경로가 끊기는 임계 점유율. **1D 사슬은 p_c = 1**(하나만 막혀도 끊김), 2D/3D는 < 1.
- **E_hull (energy above hull)**: convex hull 위 초과 에너지. 열역학적 안정성의 표준 지표. **이 논문에는 없다** — 대신 참조상태 불명의 "binding energy"만 있다.
- **P3̄m1 / Li₃YCl₆형**: 삼방정 할라이드 SE 골격. Cl⁻ hcp 부격자에 [MCl₆] 팔면체가 배열되고 Li가 그 사이를 지난다. `kim2025`의 **hcp_1**과 같은 골격.

---

## 19. 미해결 질문 (후속 확보 시 채울 것)

| # | 질문 | 어디서 |
|---|---|---|
| **Q1** | **Φ̄_Li 와 Φ̄_Me/Φ̄_X 의 정의식** — Fig 4a 전체가 여기 걸려 있다 | 저자 문의 / 정식 출판본 |
| **Q2** | **DFT+U 의 U 값**(Er 4f, Nd 4f), 스핀 처리, 4f core-freezing 여부 | 저자 / 출판본 Methods |
| **Q3** | **⟨ω⟩ 실측값 11계** — 정의만 하고 값이 없다. 이게 있으면 "연화"가 정량이 된다 | 저자 / 출판본 SI |
| **Q4** | **phonon 분산곡선 + 허수모드 유무** (도핑계의 동적 안정성) | 저자 / 출판본 SI |
| **Q5** | **응집에너지 참조상태** E_Li/E_Zr/E_M/E_Cl + Table S1/S2가 per-atom인지 per-f.u.인지 | 저자 |
| **Q6** | **Er x=0.25의 이론(악화) vs 실험(개선) 모순**은 배열 선택 때문인가, 통계인가 | 앙상블 재계산 필요 |
| **Q7** | **NEB 셋업**(이미지 수·CI·종점 자리·공공 유무)과 Oct–Tet–Oct **전체 경로** 프로파일 | 저자 / 출판본 |
| **Q8** | Fig S18/S19 **"channel structures"** 의 정의와 수치 (kim2025 Fig S11의 Li–Li 거리 서술자와 같은 가족인가?) | 출판본 SI |
| **Q9** | **Rietveld 정련 파라미터 전표**(격자상수·좌표·점유율·U_iso) — 무질서 정량의 유일한 통로 | 저자 CIF |
| **Q10** | 실험 **Eₐ(온도의존 EIS)** 와 **bulk/GB 분리** — 계산 Eₐ 검증의 유일한 길 | 저자 / 후속 |
| **Q11** | 이 논문이 **peer review를 통과했는가 / 어디에 실렸는가** (Wiley 템플릿이므로 AEM·AFM·Small 계열 추정) | 2026 하반기 재확인 |

> **Q12–Q16 은 2026-08-04 2차 패스에서 추가됐다 — §20.11 하단 표 참조.**
> (Q12 XRD 의 LiCl 귀속 · Q13 500 K AIMD 의 실체 · Q14 Eₐ 정본 · Q15 EIS 펠릿 직경 · Q16 유지율 정의)
>
> ✅ **2차 패스에서 해소된 것**: 1차 §11 표의 "Fig 3d y축 규약 불명"·"500 K 점 존재 여부 불명"·§6.7(c) "확정 불가" 3건.

---

## 20. ★★★ 2차 패스 — 본문 그림 **픽셀 독립 검증** (2026-08-04)

**1차 패스(2026-07-28)** 는 본문 + SI(.docx)의 **텍스트·표**를 정독했다. 이번 패스는 다른 통로다:
PDF 그림을 **600–900 dpi로 렌더**해서 축 프레임·눈금·마커·막대·곡선을 **픽셀로 실측**하고, 인쇄된 숫자와 대조했다.
재현 코드 **`tools/litdb/ren2026_fig_verify.py`** (PyMuPDF + PIL만, numpy 없음 — `zhou2026_si_verify.py` 선례 준용).

> **결과 요약**: 1차가 "판독 추정"·"확정 불가"로 남긴 **3건이 전부 확정**됐고, **신규 5건**이 나왔다.
> 그중 **§20.3 은 이 논문의 헤드라인 Eₐ 를 직접 무효화하고, 동시에 §8.2-4의 "정적 NEB 과대평가" 판정을 뒤집는다.**

### 20.1 ✅ **확정** — Fig 3d/3e 의 y축은 `ln(D)` 가 아니라 **log₁₀(D)** 다

1차 §11 표(Fig 3d 행)는 *"y축 라벨 'ln(D)'인데 값 범위(−4.6~−7.0)로 보아 log₁₀ 로 보인다(판독)"* 로 남겨 뒀다. **확정한다.**

**절차**: 패널 프레임과 눈금을 실측(패널 d: x 1.0 = 815.0 px·1단위 = 924.5 px / y −4.6 = 2008.5 px·0.2 = 70.18 px)한 뒤,
**그려진 적합선 자체의 기울기**를 뽑아 두 규약으로 Eₐ 를 계산해 인쇄값과 대조했다.

| 계열 | 인쇄 Eₐ | 적합선 기울기 → **Eₐ(y = log₁₀D 가정)** | Eₐ(y = lnD 가정) |
|---|---:|---:|---:|
| Er x=0.125 | 0.3842 | **0.3842** ← 4자리 완전일치 | 0.1669 |
| Nd x=0.25 | 0.2046 | **0.2046** ← 4자리 완전일치 | 0.0888 |
| Nd x=0.5 | 0.2818 | **0.2818** ← 4자리 완전일치 | 0.1224 |
| Nd x=0.375 | 0.1893 | 0.1889 | 0.0821 |
| Er x=0.25 | 0.3140 | 0.3176 | 0.1379 |
| Er x=0.375 | 0.2624 | 0.2591 | 0.1125 |

> 🔑 **4자리 완전일치가 3건.** `ln` 규약에서는 **11개 전부가 정확히 ×1/2.303 만큼 어긋난다.**
> → **축 라벨이 틀렸다.** 라벨 그대로 읽으면 600–900 K 에서 D ≈ 10⁻³ cm²/s (액체·기체급)로 **물리적으로 불가능한 값**이 된다.
> 실제 축은 log₁₀ D 이고 D ≈ 10⁻⁵–10⁻⁷ cm²/s — 정상 범위.
> ⚠ **인용 시**: Fig 3d/3e 를 "ln D 그림"으로 옮겨 적으면 안 된다.

### 20.2 ✅ **확정** — Methods 에 없는 **다섯 번째 온도점(500 K)** 이 모든 계열에 있다

1차는 *"x축이 1000/T = 1.0–2.0까지 그려져 있어 **500 K 점의 존재 여부 불명**(Methods는 4점)"* 으로 남겼다.

**마커를 색별 연결성분으로 전수 추출**한 결과, **12개 계열(Er 6 + Nd 6) 전부**에 `1000/T = 2.000 ± 0.001` 위치의 마커가 있다. → **T = 500 K.**
Methods 원문은 *"simulation temperatures set to 600, 700, 800, and 900 K"* 이고, **SI Table S5 에도 500 K 는 없다**(1차 §6.2).

**그런데 그 500 K 점들은 정보가 없다.** 각 계열의 600–900 K 4점 적합선을 500 K로 외삽한 값 대비 실측 편차:

| 계열 | 500 K 점의 편차 (dex) |
|---|---:|
| Er x=0.125 | **−1.330** |
| Nd x=0.625 | −1.295 |
| Nd x=0.5 | −0.957 |
| Er x=0.25 | −0.249 |
| Nd x=0.25 | −0.159 |
| **Li₂ZrCl₆** | **+0.519** |
| **Er x=0.5** (헤드라인) | **+0.871** |

> ⛔ **±1.3 dex(±20배) 로 양쪽으로 흩어진다.** 계통 편차가 아니라 **순수 잡음**이다.
> 50 ps AIMD 로 500 K 에서 Li 확산을 재면 MSD 가 진동(rattling) 성분에 잠겨 D 가 아무 값이나 나온다 — 교과서적 실패 모드다.
> 🔑 **우리 CLAUDE.md 규율("아레니우스는 600/800/1000 K 3점, 400/500 K 제외 판정")이 남의 데이터에서 그대로 재확인됐다.**

### 20.3 ★★★ **신규·최중요** — 그 500 K 점 하나가 **헤드라인 Eₐ 를 만들었다**

**헤드라인 조성 Li₂.₅Zr₀.₅Er₀.₅Cl₆ (Fig 3d 연두)** 의 마커 5점 실측 (log₁₀ D):

| T | 900 K | 800 K | 700 K | 600 K | **500 K** |
|---|---:|---:|---:|---:|---:|
| log₁₀ D | −4.671 | −5.116 | −5.315 | −5.771 | **−5.539** |

> ⛔⛔ **D(500 K) = 2.89×10⁻⁶ > D(600 K) = 1.69×10⁻⁶.**
> **온도를 100 K 낮췄더니 확산이 1.7배 빨라진다** — 활성화 과정에서 **불가능**하다.

**이 점을 넣고 빼고의 차이:**

| 적합 | Eₐ (eV) |
|---|---:|
| **600–900 K 4점만 (물리적으로 방어 가능한 창)** | **0.372** |
| 500 K 포함 5점 (우리 재적합) | 0.195 |
| 그려진 적합선 (기울기 실측) | 0.182 |
| **논문 인쇄값 (Fig 3d 주석)** | **0.1625** |
| SI Table S5 | 0.163 |

같은 진단을 pristine Li₂ZrCl₆ 에 적용 (Fig 3e 에서 5점 전부 추출됨: 900 −5.191 / 800 −5.381 / 700 −5.774 / 600 −6.096 / **500 −6.154**):

| 적합 | Eₐ (eV) |
|---|---:|
| **600–900 K 4점** | **0.332** |
| 500 K 포함 5점 | 0.227 |
| 인쇄값 | 0.2392 (Fig 3d/e 주석) / 0.230 (Table S5) |

> 🔑🔑🔑 **그리고 여기서 논문 안의 두 숫자가 화해한다.**
> 1차 §8.2-4 는 *"정적 NEB 장벽 ≫ AIMD Eₐ, 비율 2.2–2.9배 → 단일경로 정적 NEB는 유효 활성화에너지를 계통적으로 과대평가"* 로 판정했다.
> **그런데 Er x=0.5 에서: 우리 깨끗한 600–900 K 재적합 Eₐ = 0.372 eV vs 같은 논문의 NEB Oct–Tet 장벽 = 0.370 eV — 0.5 % 차이로 일치한다.**
> ⛔ **즉 이 조성에서 "NEB가 2.27배 과대"였던 게 아니라, AIMD Eₐ 가 500 K 잡음점 때문에 2.29배 과소평가된 것이다.**
> **→ §8.2-4 의 판정을 이 조성에 한해 철회한다.** (pristine 은 여전히 0.658 / 0.332 = 2.0배 차이가 남는다 — 이쪽은 협동운동·다중경로로 설명되는 정상 격차다.)
>
> ⛔ **연쇄 파급**: 논문의 헤드라인 *"migration barrier decreases to 0.370 eV / Eₐ = 0.163 eV"* 는 **같은 물리량의 두 값이 우연히 나란히 실린 게 아니라, 하나(0.163)가 인공물**이다.
> 그리고 §6.7 의 Meyer–Neldel 진단(**E_MN = 57 meV**, ln D₀ vs Eₐ 의 r = 0.965)이 **왜** 그렇게 깨끗한 보상선을 그렸는지도 이제 설명된다 — **11개 계열 전부가 같은 잡음 지렛대(가장 긴 x-팔인 500 K 점)로 회전당했기 때문이다.**

### 20.4 ⚠ **신규** — 같은 Eₐ 가 논문 안에서 **세 군데에 서로 다르게** 인쇄돼 있다

Fig 3d/3e **패널 주석** vs Fig 3f **막대(단위 10⁻¹ eV)** vs SI **Table S5** 를 전수 대조:

| 조성 | Fig 3d/3e 주석 | Fig 3f 막대 | Table S5 | 판정 |
|---|---:|---:|---:|---|
| **Li₂ZrCl₆** | **0.2392** | 2.3 | 0.230 | ⛔ 주석만 다름 |
| **Er x=0.125** | **0.3842** | 3.41 | 0.341 | ⛔ **12.7 % 차이** |
| **Er x=0.625** | **0.1859** | 1.96 | 0.196 | ⛔ 주석만 다름 |
| **Nd x=0.25** | **0.2046** | 2.1 | 0.210 | ⛔ 주석만 다름 |
| 나머지 7계 | — | — | — | ○ 3자 일치 |

> **Fig 3f 막대 = Table S5** 는 11/11 일치한다(1차 §6.2 확인). **어긋나는 건 Fig 3d/3e 주석 4개뿐이다.**
> 그리고 §20.1 에서 봤듯 **그려진 적합선의 기울기는 주석과 일치**한다(Er0.125 4자리 완전일치).
> 🔑 **→ 같은 D(T) 데이터에 대한 서로 다른 두 개의 아레니우스 적합이 한 논문 안에 공존한다.** 어느 쪽이 정본인지 표시가 없다.
> 우리 규율(그림·표 우선)에 따라 **Table S5 = Fig 3f 를 정본**으로 유지하되, **어느 쪽도 §20.3 의 500 K 오염을 벗어나지 못한다.**

### 20.5 ⚠ **신규** — EIS **펠릿 기하가 자기 σ 값과 맞지 않는다**

본문 Experimental: *"pressed into uniform pellets with a **diameter of 16 mm** and a **thickness of approximately 1–2 mm**"*, `σ = L/(R × S)`.
**Fig 3g Nyquist 의 실축 저항**(Z″ 최저점 = 실축 절편)을 실측하고, 인쇄된 σ 를 재현하는 두께를 역산했다:

| 시료 | 실측 R (Ω) | 인쇄 σ (mS/cm) | d = 16 mm 가정 → 두께 | d = 10 mm 가정 → 두께 |
|---|---:|---:|---:|---:|
| Li₂ZrCl₆ (인셋) | ≈820 | 0.227 | **3.74 mm** ✗ | **1.46 mm** ✓ |
| Li₂.₂₅Zr₀.₇₅Er₀.₂₅Cl₆ | 231 | 0.81 | **3.77 mm** ✗ | **1.47 mm** ✓ |
| Li₂.₂₅Zr₀.₇₅Nd₀.₂₅Cl₆ | 270 | 0.76 | **4.12 mm** ✗ | **1.61 mm** ✓ |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** | 139 | 1.32 | **3.69 mm** ✗ | **1.44 mm** ✓ |
| Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆ | 210 | 1.13 | **4.78 mm** ✗ | **1.87 mm** ✓ |

> ⛔ **명시된 16 mm 로는 5/5 전부 "1–2 mm" 범위 밖(3.7–4.8 mm)** 이고, **10 mm 로는 5/5 전부 범위 안(1.44–1.87 mm)** 에 정확히 들어간다.
> → **인쇄된 σ 는 명시 기하의 셀 상수와 2.56배 어긋난다.** 직경이 10 mm(할라이드 SE 셀 표준 다이 크기)였을 가능성이 가장 높다.
> 🔑 **σ *비율*(1.32/0.227 = 5.81×)은 이 오류에 영향받지 않는다** — 저항비 820/139 = 5.90 과 일치. **비율만 인용한다는 우리 규율(최우선 규율 3)이 여기서 정확히 옳다.**
> ⚠ 다만 **§6.6 의 "AIMD/실험 = 3–4배 과대"** 는 σ 절대값에 걸려 있으므로, 셀 상수가 확정되기 전까지 **그 배율 자체가 미확정**이다.

### 20.6 ✅ **독립 재확인** — Fig 4b 픽셀 실측으로도 서술자 Φ 는 σ 를 설명하지 못한다

1차 §4.5 는 **SI Table S6 의 숫자**로 상관 붕괴를 보였다. 이번엔 **Fig 4b 막대 높이를 픽셀로 재서** 같은 검사를 독립 수행했다(막대 상단 가로선 검출 + 왼축 0.0–1.6 눈금 보정).

| 표본 | Pearson r | Spearman ρ | 출처 |
|---|---:|---:|---|
| 문헌 16계 | **−0.204** | **−0.141** | **2차: Fig 4b 픽셀** |
| 문헌 16쌍 | −0.179 | −0.045 | 1차: Table S6 숫자 |
| 전 18계 | −0.254 | −0.096 | 2차: Fig 4b 픽셀 |
| 전 18계 | −0.255 | −0.089 | 1차: Table S6 숫자 |

> 🔑 **두 개의 완전히 다른 통로(SI 표 vs 그림 픽셀)가 같은 결론에 도달한다. §4.5 판정 확정.**

**그림 자체가 주는 추가 반례** (Fig 4b σ 내림차순, 픽셀 실측):

| 순위 | 계 | Φ (오른축) | σ (mS/cm) |
|---:|---|---:|---:|
| 1 | Li₂.₄Zr₀.₆**Sc**₀.₄Cl₆ | 0.625 | **1.50** |
| 2 | Li₁.₇Zr₀.₇**Ta**₀.₃Cl₆ | **1.206** (전체 3위 高) | **1.42** |
| 3 | **Li₂.₅Zr₀.₅Er₀.₅Cl₆ (이 논문)** | 0.520 | 1.32 |
| … | | | |
| 17 | Li₂ZrCl₆ | 0.860 | 0.282 |
| 18 | Li₁.₇₅Zr₀.₇₅**Mo**₀.₂₅Cl₆ | **1.574** (최고) | **0.172** |

> ⛔ **① 저자들의 "최적" 조성이 자기 스크리닝 그림에서 3위다** (Sc0.4·Ta0.3 이 더 높다).
> ⛔ **② Ta(Φ 전체 3위)가 σ 2위다** — "저-Φ 가 좋다"의 정면 반례. 겉보기 음의 추세는 사실상 **Mo₀.₂₅ 한 점**이 만든다.
> ⚠ **③ 방법론 문제**: Fig 4b 의 σ 는 **서로 다른 16개 논문의 실측값**을 스택압력·밀도·펠릿 이력 보정 없이 한 축에 올린 것이다. 이런 메타 산점도로는 서술자를 세울 수 없다.

### 20.7 ⚠⚠ **신규** — Fig 2b: 도핑 시료의 날카로운 선 4개가 **fcc LiCl 위치**에 있다

1차 §5.3 은 논문 주장(*"주피크가 Li₃YCl₆형과 일치, **불순물 피크 없음**"*, *"도핑 시 피크가 **전체적으로 저각 이동**"*)을 그대로 전사했다.
**Fig 2b 의 각 트레이스를 색분리해 피크 위치를 실측**하니 그림이 그 서술을 지지하지 않는다. (x축 눈금 20/40/60/80° 실측 보정, 2θ = 20 + (x − 2149.5)/17.167.)

| 트레이스 | 날카로운 피크 2θ (°) |
|---|---|
| **Li₂ZrCl₆ (pristine)** | **16.0 · 32.1 · 41.9 · 50.1** |
| **Li₂.₅Zr₀.₅Er₀.₅Cl₆** (가장 깨끗) | **29.9 · 34.7 · 49.9 · 57.8 · 59.6** |
| Li₂.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆ | 15.5(흔적) · 29.9 · 34.7 · 50.0 · 57.8 · 59.6 (+잡음) |
| **fcc LiCl** (a = 5.1396 Å, Cu Kα) **예상** | **30.10(111) · 34.89(200) · 50.15(220) · 59.62(311)** |

> **Li₂.₅Zr₀.₅Er₀.₅Cl₆ 의 날카로운 선 4개가 LiCl 4개 반사와 4/4 일치**하고, 편차가 **−0.15 ~ −0.25° 로 일정**하다(= 단일 축 보정 오프셋).
> 반대로 **pristine LZC 의 최강선 16.0°·32.1° 는 도핑 시료 어디에도 없다**(Nd0.375 에 15.5° 흔적만).
> 전구체가 **LiCl + ZrCl₄ + ErCl₃/NdCl₃ 기계화학(700 rpm 45 h)** 이므로 **미반응 LiCl 잔류**는 이 합성의 표준 실패 모드다.
>
> 🔑 **가장 자연스러운 해석**: 도핑 시료는 **대체로 X-선 비정질**(20–21° 넓은 혹 — pristine 에는 없다) **+ 잔류 LiCl 결정**이다.
> ⛔ 그렇다면 **① "불순물 피크 없음" 은 틀렸고, ② "전체적 저각 이동" 은 정의 자체가 성립하지 않는다** — pristine 과 도핑 시료 사이에 **대응하는 피크 쌍이 없어서** 이동량을 잴 대상이 없다.
> ⛔ 그리고 **Fig 2c 의 Rietveld(R_wp 4.40/4.86 %, GOF 1.76/1.89)** 는 이 넓은 혹을 정련한 것이 된다 — 1차 §5.3 이 이미 지적한 *"정련된 격자상수·점유율 표가 어디에도 없다"* 와 합치면, **격자 팽창의 실험적 증거는 사실상 0** 이다. (그리고 §5.3 의 *"두 조성의 계산 격자상수가 소수 넷째 자리까지 동일"* 과 §6.3 의 *"11계 전부 단일 부피"* 로, **계산 쪽 증거도 0**.)
> ⚠ **등급: "강한 표시", 확정 아님.** LiCl 귀속은 그림 픽셀 판독 기반이다. 확정하려면 **원 XRD 데이터(또는 SI Fig S3/S4 의 고배율 원본)** 가 필요하다 → **Q12**.

### 20.8 ✅ **확정 승격** — NEB 종점 비대칭 · Tet 극소 부재

1차 §8.2-2, -3 이 "(판독)" 으로 남긴 두 지적을 렌더로 확정했다.

| 패널 | 곡선 | 시작 | 최고점 (인쇄) | **종점** |
|---|---|---:|---:|---:|
| Fig 4f | Li₂ZrCl₆ Oct–Oct (7 image) | 0.00 | 0.658 | **−0.15** |
| Fig 4f | Er0.5 (6 image) | 0.00 | 0.370 | **−0.22** |
| Fig 4f | Nd0.375 (6 image) | 0.00 | 0.417 | **−0.12** |
| Fig 4g | Er0.5 **Oct–Tet** | 0.00 | 0.370 | **−0.22** |
| Fig 4g | Er0.5 Oct–Oct | 0.00 | 0.514 | −0.07 |
| Fig 4h | Nd0.375 **Oct–Tet** | 0.00 | 0.417 | **−0.13** |
| Fig 4h | Nd0.375 Oct–Oct | 0.00 | 0.561 | +0.04 |

> 1. **종점이 전부 시작점보다 낮다** → 시작/끝 자리가 등가가 아니다. **인쇄값은 정방향 반쪽 장벽**이고
>    **역방향 장벽은 Er0.5 Oct–Tet 에서 0.370 + 0.22 = 0.59 eV**, Nd0.375 에서 0.417 + 0.13 = **0.55 eV** 다.
>    장거리 확산의 율속은 폐경로 최대값이므로 **실효 장벽은 0.55–0.59 eV 쪽**이다. (참고: pristine 도 0.658 + 0.15 = **0.81 eV**.)
> 2. **Fig 4g/4h 의 "Oct–Tet" 곡선은 단봉이다** — 중간 극소가 **없다**. 논문의 핵심 기구인
>    *"tetrahedral sites become **stabilized as intermediate metastable states**"* 를 뒷받침할 **국소최소가 그림에 없다.**
>    범례도 "Oct–Tet–Oct" 가 아니라 **"Oct-Tet"** 이다 → 인쇄된 0.370/0.417 은 **Oct→Tet 반쪽 구간**일 가능성이 크다.
> 3. **Fig 4f 는 서로 다른 경로를 나란히 놓았다** — pristine 은 **Oct–Oct(0.658)**, 도핑계는 **Oct–Tet(0.370/0.417)**.
>    **같은 경로끼리 비교하면** 0.658 → **0.514(Er)/0.561(Nd)** 이고, 도핑 이득이 **0.288 → 0.144 eV 로 반감**한다.
>    그리고 **pristine 의 Oct–Tet 경로는 한 번도 계산되지 않았다** → *"원래 고에너지였던 Tet 자리가 도핑으로 안정화됐다"* 는 **비교군이 없는 주장**이다.
> 4. x축 *"Migration pathway (Å)"* 눈금 1–7 은 **NEB 이미지 번호**다. 이 골격에서 Oct–Oct 이웃 거리는 ~3 Å 인데 6–7 로 표시돼 있다 → **축 라벨 오류**.

### 20.9 ⚠ **신규** — Fig 5g 유지율 실측 **78.2 %** (인쇄 82.5 %)

방전용량 곡선(teal)을 왼축(0–240 mAh/g, 60 당 207 px) 보정으로 전수 추적:

| | 값 |
|---|---:|
| 첫 사이클 | **141.2 mAh/g** |
| 100 사이클 | **110.4 mAh/g** |
| **실측 유지율** | **78.2 %** |
| 본문/초록 인쇄값 | **82.5 %** |
| CE (오른축 실측) | 중앙값 **98.9 %**, 최댓값 **99.4 %**, 초기 5점 93.5–97.1 % |

> ⚠ **4.3 %p 차이.** 정의 차이(형성 사이클 제외 등)일 수 있으나 **본문에 유지율 정의가 없다.**
> 인쇄된 *"CE remains stable at nearly 99.4 %"* 는 **중앙값이 아니라 최댓값**이다.
> 🔑 **인용 시 "82.5 % (그림 실측 78 %)" 로 병기**한다. 1차 §10.3 의 CE–유지율 정합성 의문은 **유지율 쪽 값이 낮았던 것으로 일부 해소**된다.

### 20.10 조판·라벨 오류 목록 (그림을 그대로 옮길 때 사고 방지)

| 위치 | 오류 |
|---|---|
| **Fig 3h** x축 | `Li₀.₂₅Zr₀.₇₅Nd₀.₂₅Cl₆`, `Li₀.₃₇₅Zr₀.₆₂₅Nd₀.₃₇₅Cl₆`, `Li₀.₅Zr₀.₅Er₀.₅Cl₆` — **Li 아래첨자가 2.25/2.375/2.5 여야** |
| **Fig 4a** 라벨 | 위와 같은 Li 아래첨자 오류 + `LI₂.₁Zr₀.₉₅Cu₀.₀₅Li₆` (끝이 **Cl₆** 여야) |
| **Fig 3e** 범례 | `Li₂.₅Zr₀.₇₅Nd₀.₂₅Cl₆` (**Li₂.₂₅** 여야) · `Li₂.₅Zr₀.₅Nd₀.₅Cl` (아래첨자 6 누락) |
| **Fig 3d/3e** y축 | `ln(D)` → 실제는 **log₁₀(D)** (§20.1) |
| **Fig 4f–4h** x축 | `Migration pathway (Å)` → 실제는 **NEB 이미지 번호** (§20.8-4) |
| **Fig 4c–4e** x축 | `Frequency` — **단위 없음**. 본문만 "THz" 라고 말한다 |
| **Fig 4b** 단위 | 범례 `Ionic potential(10⁻¹/Å⁻¹)` vs 오른축 `Ionic potential(Å⁻¹)` — **서로 모순**, 둘 다 Z/r(Zr⁴⁺ = 5.56 Å⁻¹)과 안 맞는다 |
| 본문 참고문헌 | **[8] 과 [30] 이 동일 문헌** (Xiao/Wu/Wang/Zhao/He, *Energy Environ. Mater.* **2024**, 7, e12729) — 중복 등재 |
| 본문 §2.2 서술 | *"doping significantly enhances Li diffusion **along the c-axis**, … clearly higher than a-axis and b-axis"* → **Fig 3b 는 MSD_a ≈ MSD_c ≈ 21 Å² 로 a와 c가 동급**(1차 §9.2 표). **자기 그림과 어긋난다.** 실제로 일어난 일은 "c 강화"가 아니라 **1D → 2D 차원성 승급**(§9.3) |
| Authorea 표지 | keywords 에 `solar cells · photovoltaics · supercapacitors · carbon materials` 등 무관 키워드가 반복 삽입돼 있다(프리프린트 메타데이터 품질 신호) |

### 20.11 2차 패스 종합 판정

| # | 항목 | 1차 상태 | **2차 결과** |
|---|---|---|---|
| 1 | Fig 3d/e y축 규약 | 판독 추정 | ✅ **log₁₀ 확정** (4자리 일치 3건) |
| 2 | 500 K 점 존재 | 불명 | ✅ **12/12 계열에 존재 확정** |
| 3 | 헤드라인 Eₐ | 외삽 인공물로 진단(§6.7) | ✅ **원인 특정: 500 K 잡음점. 깨끗한 창 재적합 Er0.5 = 0.372 eV** |
| 4 | NEB vs AIMD 2.27배 격차 | "정적 NEB 과대"로 판정(§8.2-4) | ⛔ **Er0.5 한해 철회 — 0.372 ≡ NEB 0.370 (0.5 %)** |
| 5 | Fig 3a/b MSD ↔ Table S5 불일치 | 확정 불가(§6.7c) | ✅ **원인 특정: 적합선이 600 K 점을 지나지 않는다(500 K 가 끌어내림)** |
| 6 | Eₐ 3중 인쇄 불일치 | — | ⚠ **신규 4/11** |
| 7 | EIS 펠릿 기하 | — | ⚠ **신규 — 셀 상수 2.56배 불일치** |
| 8 | Φ–σ 상관 붕괴 | Table S6 기반 | ✅ **그림 픽셀로 독립 재확인 (r −0.204)** + **자기 최적 조성이 자기 그림에서 3위** |
| 9 | XRD "불순물 없음"·"저각 이동" | 논문 주장 전사 | ⚠⚠ **신규 — 도핑 시료 날카로운 선 4/4 가 fcc LiCl 위치. 강한 표시(Q12)** |
| 10 | NEB 종점 비대칭·단봉 | 판독 | ✅ **확정 승격 — 실효 장벽 0.55–0.59 eV** |
| 11 | 100 cyc 유지율 | 인쇄값 전사 | ⚠ **신규 — 실측 78.2 %** |

> ### ⛔⛔ 이 논문 인용 규율 (2차 패스 후 최종)
> 1. **Eₐ 절대값 인용 금지.** 0.163 / 0.189 / 0.230 eV 는 **500 K 잡음점이 만든 값**이다(§20.3). 꼭 써야 하면 *"깨끗한 600–900 K 창 재적합 시 0.33–0.37 eV (본 digest §20.3 재분석)"* 로 병기.
> 2. **NEB 장벽은 "정방향 반쪽"임을 병기.** 0.370 eV → *"정방향 0.370, 역방향 0.59 eV, Tet 중간 극소 미확인"*.
> 3. **σ 절대값 인용 금지** (기존 규율 유지 + §20.5 셀 상수 문제로 근거 추가). **비율은 안전**(저항비와 자기정합).
> 4. **"불순물 없음"·"저각 이동" 인용 금지** (§20.7).
> 5. **유지율은 "82.5 % (그림 실측 78 %)"** 로 병기.
> 6. **저-Φ 처방을 명제로 옮기지 않는다.** 이 논문의 가치는 **처방이 아니라 반례 카탈로그**다(§4.5 + §20.6).

**신규 미해결 질문 (§19 에 추가):**

| # | 질문 | 어디서 |
|---|---|---|
| **Q12** | **Fig 2b 도핑 시료의 29.9/34.7/50.0/59.6° 4선이 잔류 LiCl 인가** — 그렇다면 Rietveld·"저각 이동"·격자 팽창 서사 전체가 무너진다 | 원 XRD 데이터 / 저자 / 출판본 SI Fig S3–S4 원본 |
| **Q13** | **AIMD 를 정말 500 K 에서도 돌렸는가**, 돌렸다면 왜 Methods·Table S5 에 없는가. 아레니우스 적합에 그 점을 넣었는가 | 저자 / 출판본 |
| **Q14** | **Fig 3d/3e 주석 Eₐ 와 Table S5 Eₐ 중 어느 쪽이 정본인가** (4계 불일치, 최대 12.7 %) | 저자 |
| **Q15** | **EIS 펠릿 실제 직경** — 16 mm 인가 10 mm 인가. σ 절대값 전체가 여기 걸려 있다 | 저자 / 출판본 |
| **Q16** | Fig 5g **유지율 정의**(기준 사이클) — 78.2 %(그림) vs 82.5 %(본문) | 저자 |

**재현 코드**: `tools/litdb/ren2026_fig_verify.py` — 실행하면 §20.1~20.3(Fig 3d/3e 마커·적합선), §20.5(EIS), §20.6(Fig 4b 막대), §20.7(Fig 2b 피크), §20.9(Fig 5g)가 전부 재출력된다.
`PYTHONIOENCODING=utf-8 python tools/litdb/ren2026_fig_verify.py`
