# Can substitutions affect the oxidative stability of lithium argyrodite solid electrolytes? — Banik et al. (Zeier & Mo groups; manuscript / ACS-class, ~2022)

> slug `banik2022_substitutions_oxidative_stability_argyrodite` · DOI `n/a` (PDF에 DOI 미인쇄; FESTBATT 03XP0430F·DESY P22; 본문에 인쇄된 식별자 없음 → "n/a"로 둠) · type `mixed (DFT phase-stability + HAXPES + stepwise CV)` · PDF `15bcf906 / a25a0287-18._Can_substitutions…` · digested `2026-06-26` · status ✅
> **저자**: Ananya Banik,ᵃ Yunsheng Liu,ᵇ Saneyuki Ohno,ᶜ Yannik Rudel,ᵃ Alberto Jiménez-Solano,ᵈ Andrei Gloskovskii,ᵉ Nella M. Vargas-Barbosa,ᶠ **Yifei Mo,ᵇ\* and Wolfgang G. Zeier**ᵃ,ᶠ\* — ᵃUniv. Münster · ᵇUniv. Maryland (Mo group) · ᶜKyushu Univ. · ᵈMPI-FKF Stuttgart · ᵉDESY · ᶠHelmholtz-Institut Münster (IEK-12). 교신 yfmo@umd.edu, wzeier@uni-muenster.de
> **[외부]** — Münster(Zeier)·Maryland(Mo)·Kyushu(Ohno). **우리 그룹(한양대/J-W Lee/Y.M.Lee/Cho/Kang/Cha) 아님.** ⚠ **핵심**: Yifei Mo = 우리 grand-potential 방법(Mo–Ong–Ceder 2012)의 *원저자*이고, Zeier = argyrodite 분야 표준 실험실. 즉 **우리 방법론 계보의 본가가, 우리 axis_1 결론(치환은 S-limited 산화 onset을 못 옮긴다)을 독립적으로 동일 도구로 발표**한 논문.

---

## 0. 이 digest를 읽는 법 (왜 이 논문이 우리에게 결정적인가)
이 논문은 우리 oxidation 작업의 **`axis_1` (intrinsic 0-pressure window)의 외부·동방법 정답지**다. 한 문장: **"황화물 argyrodite에서 (양이온 P→Si/Ge, 음이온 Cl→I) 치환을 해도 산화 분해(oxidative degradation)는 *바뀌지 않는다* — 왜냐하면 가전자대 끝(VBM)이 PS₄³⁻의 비결합(non-bonding) 궤도와 free S²⁻로 채워져 있어서, *S가 조성에 있는 한* 산화 한계는 S가 고정(pin)하기 때문."** 이는 우리의 "comp1·modelc 산화 onset이 VBM이 +0.32 eV 다른데도 둘 다 2.14 V로 동일(S²⁻-limited)" 결론과 **메커니즘·방법·결론이 모두 일치**한다. 게다가 이 논문은 우리가 쓰는 grand-potential(phase-stability) 방법을 직접 쓰고, HAXPES(=UPS급 밴드엣지)로 "VBM이 안 변한다"를 실측하며, stepwise CV로 "실효 산화 onset이 안 변한다"를 보인다 — 우리 `VBM_vs_grandpotential_report`의 세 축(VBM·grand-potential·CV)을 한 논문에서 모두 짚는다.

> ⚠ **전압 기준 혼용 주의**: 본문·Fig 2–3은 **In/InLi**와 **Li⁺/Li** 두 축을 병기. 변환 ≈ **+0.62 V**(In/InLi → Li⁺/Li). 논문이 인용하는 "oxidation starts at 2.5 V vs In/InLi"(ref18 Dewald) = 약 **3.1 V vs Li⁺/Li**. Fig 1c의 LPSCl 산화 onset도 In/InLi 축 2.5 V. **우리 grand-potential 2.14 V는 Li⁺/Li 기준** — 직접 비교 시 축을 반드시 맞출 것(아래 §7에서 정렬).

## 1. 한 줄 요약
양·음이온 치환(P→Si/Ge, Cl→I)은 argyrodite의 **산화 안정성을 거의 바꾸지 못한다**: HAXPES VBM·광학 gap·DFT pDOS/COHP·grand-potential 분해창·stepwise CV가 **일관되게** VBM=S(자유 S²⁻ + PS₄³⁻ 비결합 S 3p)임을 보이고, S가 조성에 있는 한 산화 onset은 S가 고정한다 → **"단순 치환으로는 황화물 SE의 산화 안정성을 개선할 수 없다; cathode 코팅 또는 다른 물질군이 필요하다."**

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교 물질(실험) | **Li₆PS₅Cl**(baseline) · **Ge-Li₆PS₅I**(=Li₆.₆P₀.₄Ge₀.₆S₅I) · **Si-Li₆PS₅I**(=Li₆.₆P₀.₄Si₀.₆S₅I). Si/Ge는 σ가 LPSCl과 비슷하게 골라 *mass-transport 효과를 배제*(전기화학 측정 가능). |
| 비교 물질(이론만) | **Li₆PS₅I**(미치환, σ 너무 낮아 실험 제외) + DFT용 근접조성 **Li₆.₂₅P₀.₇₅Si₀.₂₅S₅I**, **Li₆.₇₅P₀.₂₅Ge₀.₇₅S₅I** |
| 일반식 | **Li₆₊ₓMS₅X** (M = P⁵⁺, Si⁴⁺, Ge⁴⁺; X = Cl⁻, I⁻) |
| 중심 질문 | "조성 tailoring(σ 올리려 흔히 함)이 *산화 안정성도* 바꾸나?" → **답: 거의 안 바꾼다.** |
| 동기 | σ는 치환으로 잘 올리는데(ref5), 산화 안정성도 따라 바뀌는지 *불명* → 직접 검증. 최근 "전자절연 첨가제로 안정성 개선" 보고(ref27)도 *이유 불명*. |
| 방법 3종 명시(intro) | (1) band-edge(HOMO-LUMO) approach (2) stoichiometry-stability approach (3) **phase-stability approach** — Binninger 2020(ref28)이 비교. band-edge=*상한*(어느 원소가 분해를 주도하나), phase-stability=*실제 분해 전압*. **이론 창이 실험보다 좁다**(ref17,18,32,33)는 점도 명시. |

## 3. 핵심 물성 (수치 총정리)
> 논문은 *절대 수치표*가 적고 그래프 위주(특히 CV·HAXPES·gap은 Fig/Table S에 분산). 본문에서 읽히는 정량값:

| 물성 | 값 | 조건/출처 | 비고 |
|---|---|---|---|
| 광학 band gap (모든 조성) | **> 3 eV**, direct | Fig 3a (Tauc, (F(R)·hν)²), Table S1 | 이론(DFT direct)과 일치. 치환 시 *약간* shift = CB 위치 변화(아래 §5.4) |
| HAXPES VBM(가전자대 onset) | 모든 조성 **거의 동일 위치** | Fig 3b (6 keV X-ray, bulk-sensitive) | "first peak at similar energy" → VBM 불변. I계는 밴드엣지 강도↑(I 5p 기여) |
| CV 산화 onset (실효) | **모든 조성 유사**, ~**2.5 V vs Li⁺/Li**(LPSCl, ref18) ; In/InLi 축 ~1.8 V 이상서 전류 급증 | Fig 2a–d (stepwise CV, C-SE 복합, OCV 0.5 V vs In/InLi, 0.1 V씩 reversal 증가→3 V) | onset이 조성 무관 = "anion도 cation도 실효 산화 안정성 못 바꿈" |
| grand-potential 분해창(계산) | Fig 3c (Li⁺/Li 축): LPSCl ~**1.7–2.3 V**, Li₆PS₅I·Si·Ge ~**1.7–2.4 V** (그림 읽기; Table S2에 분해산물) | Lithium-evolution vs V (Fig S5) → 창 | Li₆PS₅I가 *약간* 더 안정(중간 분해산물) → Ge-Li₆PS₅I 분해의 *중간체* |
| 실험 창 vs 계산 창 | 실험(Fig 3d)이 계산(3c)보다 *약간* 넓음 | 고전도·고표면적 카본으로 kinetics 개선 → 정합↑ | 이전(ref18)보다 이론-실험 일치 좋아짐 |
| VBM 성분 | **자유 S²⁻ + PS₄³⁻ 비결합 S 3p** 지배 (할라이드·M 무관) | Fig 4 (pDOS·COHP), Fig S6 | Cl 3p는 VBM *아래* 깊이; I 5p는 밴드엣지에도 일부 |
| CB 성분 | **PS₄³⁻(M-S) 반결합** 지배 (P 기여 큼) | Fig 4c COHP | 치환은 *gap 크기*(=CB 위치)만 바꿈, VBM 아님 |

## 4. 재료 & 방법 ★
- **합성/실험**: 고상; Li₆PS₅Cl + Si/Ge 치환 Li₆PS₅I 계. 측정 = **stepwise CV**(C–SE 복합, 계면적 ↑), **광학 흡수**(diffuse reflectance → Tauc gap), **HAXPES**(6 keV, DESY PETRA III P22 빔라인, bulk-sensitive VBM). ⚠ **Li₆PS₅I는 HAXPES 시 강한 sample charging으로 측정 실패**(데이터 없음).
- **DFT/계산 방법 ★ (이 논문의 디테일은 *제한적*)**:
  - **code/functional/pseudo/k/ecut/supercell**: 본문·SI 발췌 범위에 **명시 안 됨**(n/a). 전자구조·gap·pDOS·COHP·grand-potential을 모두 first-principles로 했다고만. (Mo 그룹 관행상 VASP/PBE/MP 호환일 가능성 높으나 *논문 텍스트 근거 없음* → n/a 처리.)
  - **DFT+U**: 명시 없음(n/a). (S/P/Si/Ge/Cl/I는 localized d/f 없어 U 불필요한 계.)
  - **AIMD/MLIP**: 사용 안 함(이 논문은 전도도 AIMD가 아니라 *산화 안정성·전자구조* 논문).
  - **무질서(S²⁻/X⁻ 4a/4c site disorder) 처리**: 명시 없음(n/a). 계산 조성은 **실험 근접 정수비 단일 모델**(Li₆.₂₅P₀.₇₅Si₀.₂₅S₅I, Li₆.₇₅P₀.₂₅Ge₀.₇₅S₅I)로 택함 — SQS/enumerate 언급 없음 → *단일 배열 추정*(우리 modelc·Liu2022와 같은 "lowest-config" 철학으로 보이나 명시 안 됨).
  - **밴드 위치**: VBM·CBM 모두 **Γ-점** → direct gap 확인(Fig S4).
  - **grand-potential**: **Lithium-evolution number vs potential**(= 우리 `get_element_profile`와 동일 산출물)로 열역학 분해창 + Table S2 분해산물. **phase equilibria at reduction/oxidation potentials**(Table S3)로 I⁻/I₂ redox가 창에 영향 없음을 확인.
- **특이사항**: HAXPES를 *이온전도체*에 쓴 드문 사례(주로 반도체용). 6 keV로 표면 기여 회피 = bulk VBM. **band-edge(HAXPES)와 phase-stability(grand-potential)를 한 논문에서 교차** → 우리 report의 "VBM=상한 vs grand-potential=실제"를 *실험·계산 양쪽으로* 구현.

## 5. 결과 — 섹션별 상세 (모든 논점)

### 5.1 도입: ESW를 보는 세 방법 + 이론<실험 창 (p.2–4)
- ESW 정의 = SE가 전극과 charge-transfer(환원·산화) 안 하는 전압 범위.
- **세 방법**: (1) band-edge/HOMO-LUMO — 산화 막으려면 cathode의 ε_F가 SE의 VBM보다 *위*에 있어야(Fig 1a). gap이 곧 band-edge 창. (2) stoichiometry(삽입/추출용). (3) **phase-stability** — SE를 *반응물*로 보고 특정 전압서 완전 산화/환원해 특정 산물 생성; 분해 반응 Gibbs 자유에너지로 결정(ref28,31). band-edge=*어느 원소가 분해 주도+상한*, phase-stability=*분해 전압*(Fig 1b).
- **이론 창 < 실험 창**(Fig 1c): 계면 kinetics·준안정 중간상을 계산이 다 못 잡아서(ref17,34,35). LPSCl: 산화 **2.5 V vs In/InLi**서 시작, 환원 **0.6 V vs In/InLi** 아래. **계산 phase-stability 창(ref21=Zhu/He/Mo 2015)이 실측보다 좁음.** Li–S·oxide-CAM 사이클 창도 비교용 표시.
- **핵심 좌표**: LPSCl 산화 안정성은 **S cathode 작동 범위 안 / oxide-insertion CAM 범위 밖** → 고전압 oxide 양극엔 부족 → "개선 가능한가?"가 논문 동기.

### 5.2 Practical electrochemical stability — stepwise CV (Fig 2, p.5–6)
- **방법**: C–SE 복합(계면적↑), OCV 0.5 V vs In/InLi, reversal을 0.1 V씩 3 V까지 올리며 각 단계 2회 스캔.
- **관찰**: **1.8 V vs In/InLi 아래 = capacitive only**(분해 없음). 그 위로 전류 급증 + 분해산물의 redox feature(anodic/cathodic) 등장(ref18). 낮은 reversal서 "안정해 보이던" 전위에서도 높은 reversal 후엔 분해 peak 진화(Fig 2 caption).
- **🔑 결론(Fig 2d)**: 세 조성(LPSCl·Si-Li₆PS₅I·Ge-Li₆PS₅I)의 **mole-정규화 산화 전류 onset이 모두 비슷** → "**음이온도 양이온도 실효 산화 안정성을 안 바꾼다.**" LPSCl→치환 Li₆PS₅I로 창이 *급변하지 않음*.

### 5.3 밴드엣지 측정 — 광학 gap + HAXPES (Fig 3a,b, p.6–7)
- **광학(3a)**: 모든 조성 direct gap **>3 eV**, 이론과 유사(Table S1). 치환 시 *약간* shift.
- **HAXPES(3b)**: 6 keV(bulk). **모든 조성 first peak 같은 에너지 = VBM 거의 동일**(electronic insulator). **I계는 밴드엣지 강도↑**(I 5p가 엣지에 더 기여) — but 곧 §5.5에서 "그래도 산화창엔 무관"으로 정리. (Li₆PS₅I는 charging으로 실패.)
- **계산 조성**: Li₆.₂₅P₀.₇₅Si₀.₂₅S₅I, Li₆.₇₅P₀.₂₅Ge₀.₇₅S₅I(실험 근접). VBM·CBM 모두 Γ(direct, Fig S4). **VBM은 치환에 거의 안 변하고, gap의 약한 shift = CB 위치 변화(양이온 치환).**

### 5.4 열역학 분해창 — grand-potential (Fig 3c,d, p.7–8)
- **Li-evolution vs V(Fig S5)** → 열역학 창(Fig 3c) + 분해산물(Table S2).
- **실험 창(3d) ≈ 계산 창(3c)**, 단 실험이 *약간* 더 안정(고전도 카본으로 kinetics↑ → 이전 ref18보다 정합↑).
- **흥미로운 점**: **Li₆PS₅I가 치환체보다 *약간* 더 안정** → Ge-Li₆PS₅I 분해의 *중간 분해산물*이 됨. 분해는 모두 **S/폴리설파이드·(P–S)ₓ 생성**(전기화학 활성) → Fig 2 redox feature 설명.
- **LiX(LiCl/LiI)가 분해산물 중 하나** → 최근 "LiX가 thiophosphate(Li₃PS₄) 산화 안정성 높인다"(ref27 Hakari) 인용. (= 우리 sei_products의 LiCl wide-gap passivation 논리와 같은 결.)

### 5.5 ★ 밴드엣지의 화학적 본질 — pDOS + COHP (Fig 4, p.9–10) — **논문의 심장**
- **pDOS(Fig 4a,b)**: 모든 argyrodite에서 **VB는 음이온 상태가 지배, 그중 S가 VBM을 지배.**
  - **LPSCl**: **Cl 3p는 VB *깊이*에 위치**(전기음성도 큰 Cl이 3p를 VBM 아래로 밀어냄) → Cl은 VBM에 없음.
  - **I계**: I 5p가 *밴드엣지에도* 일부 기여(HAXPES 강도↑와 정합). **그러나 phase-equilibria(Table S3)에서 I⁻/I₂ redox는 ESW에 영향 없음 → 무시 가능.**
  - **결론**: **할라이드 조성과 무관하게 S 상태가 VBM 지배.**
- **CB**: 양이온(특히 P) 기여 큼 → **PS₄³⁻ 영향이 CB 엣지에 더 강함.**
- **COHP(Fig 4c)**: **CB 엣지 = P–S *반결합* 상태**, **P–S *결합* 상태는 VBM보다 *훨씬 아래*.** → PS₄³⁻ 결합 상태가 너무 낮아서, **채워진 *비결합* S 궤도가 무거운 상태로 발현해 VBM을 형성.**
- **🔑🔑 핵심 문장(거의 직역)**: *"치환을 MS₄ 유닛이나 할라이드에 해도, **VBM의 에너지 상태는 대부분 S가 결정**한다. 치환은 **band gap의 크기만**(MS₄ 결합이 세지면 CBM이 위로) 바꾼다."* + *"S 상태가 band edge를 지배해 **산화 안정성 창을 effectively pin** 한다 → 모든 황화물 SE는 전조성 무관 비슷한 산화 안정성을 가질 것."*

### 5.6 결론 (p.10–11)
- **"Sulfur is the Achilles' heel of oxidative stability of sulfide SE."** 단순 치환은 *S가 조성에 있는 한* 내재 산화 안정성(과 분해 경로)을 거의 못 바꾼다.
- → 장수명 ASSB엔 **(a) cathode active material 코팅** 또는 **(b) 다른 물질군**이 필요. (S를 빼지 않는 한 산화 한계는 안 올라간다.)

## 6. 메커니즘 종합 (한 흐름)
σ 올리려는 치환(P→Si/Ge, Cl→I) → **VBM은 안 움직임**(HAXPES·pDOS: VBM=자유 S²⁻ + PS₄³⁻ 비결합 S 3p; Cl 3p는 깊이, I 5p는 엣지지만 I⁻/I₂ redox는 창 무관) → **실효 산화 onset 불변**(CV Fig 2d) + **열역학 분해창 불변**(grand-potential Fig 3c, 분해산물=폴리설파이드/S/(P–S)ₓ + LiX) → **치환은 gap 크기(=CB 위치)만 바꿈** → **결론: S가 산화 한계를 pin → 단순 치환으로 산화 안정성 개선 불가 → 코팅/타 물질군 필요.**

## 7. 우리 DFT 대비 (comp1 / modelc) ★ → `../our_dft_baseline.md`, `kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md`
> ⚠ **method-dependence 먼저**: (i) 전압 축(In/InLi vs Li⁺/Li, +0.62 V) — 절대 onset 직접 비교 시 정렬 필수. (ii) 이 논문의 DFT functional/k/U/disorder가 **미명시** → 절대 gap·절대 onset 수치 1:1 비교 금지(우리도 PBE-과소). (iii) 이 논문 치환축 = **P→Si/Ge, Cl→I**(우리 cascade의 격자 산화물 도판트나 Cl 1.0→1.6 *증량*과 *다른 레버*) → **수치 등치가 아니라 *메커니즘·방법·결론*의 정합**으로 비교.

| 항목 | Banik (이 논문) | 우리 (comp1/modelc; cascade) | 일치/차이 + 이유 |
|---|---|---|---|
| **중심 결론(축 1)** | 치환(P→Si/Ge, Cl→I)으로 **산화 분해 안 바뀜** | comp1·modelc 산화 onset **동일 2.14 V**(LiS4 제외 2.256); cascade 47 dopant 대부분 ox=**2.14 V에 pin** | **✓✓✓ 정확 일치** — 우리 `axis_1_intrinsic_0pressure_window = DRAW`의 *외부·동방법 정답지*. 둘 다 "치환은 산화 onset을 안 옮긴다". |
| **메커니즘(왜 안 변하나)** | **VBM = 자유 S²⁻ + PS₄³⁻ 비결합 S 3p**가 산화 onset을 pin (pDOS+COHP) | VBM = S 3p (comp1 ~96%, modelc ~97%); 산화 = **S²⁻→폴리설파이드 S²⁻-limited** | **✓✓✓ 동일 메커니즘** — "S가 VBM·산화 한계를 pin". 우리 ICOHP(P–S) −5.94/−6.0, ELF(P–S) 0.946/0.944 = Banik COHP "P–S 결합 상태 깊이, 비결합 S가 VBM" 정량판. |
| **방법(계산)** | **grand-potential / phase-stability**(Li-evolution vs V, 분해산물 Table S2) | **grand-potential**(`get_element_profile`, Mo–Ong–Ceder 2012) | **✓✓ 동일 방법** — *게다가 Yifei Mo = 우리가 인용하는 Mo 2012의 저자*. 분야 표준을 본가가 같은 계에 적용. |
| **밴드엣지 vs 분해창 구분** | band-edge(HAXPES)=*상한/주도원소*, phase-stability=*분해 전압*을 **명시 분리**(intro·Fig 1b) + 이론창<실험창 | 우리 report 핵심: **VBM(밴드엣지)=과대상한, grand-potential=실제 onset** (comp1/modelc VBM +0.32 eV 다른데 onset 동일) | **✓✓✓ 동일 프레임** — Banik이 *실험(HAXPES)+계산*으로 우리 `VBM_vs_grandpotential_report`를 그대로 구현. "VBM 안 변함(HAXPES) → onset 안 변함(CV)"이 우리 "VBM 달라도 onset 동일"의 상보 증거. |
| **VBM 절대 위치 비교 가능성** | HAXPES VBM은 *측정*(같은 척도) → "거의 동일" 직접 비교 가능 | 우리 DFT 절대 VBM은 **셀 간 정렬 미보정 → 비엄밀**(report §4b) | △ **방법 차이**: Banik은 HAXPES로 절대 VBM을 *공통 척도*에서 봄(우리 DFT가 못 하는 것). 그래서 "VBM 불변"을 우리보다 *직접* 보임. 우리는 대신 onset 동일로 우회 증명. |
| **band gap** | direct **>3 eV**(광학 Tauc) | comp1 2.066 / modelc 2.099 eV (**PBE**) | △ **functional 차이 = method-artifact**: 우리 PBE는 ~1 eV 과소(He19 caveat). Banik 광학 gap >3 eV가 *실측*. **"wide-gap insulator" 수준만 일치**, 절대값 비교 금지. (Banik도 DFT gap이 광학과 "유사"라 했으니 그쪽 DFT도 >3? → functional 미명시라 단정 불가.) |
| **gap shift의 원인** | 치환 시 gap shift = **CB(PS₄ 반결합) 위치 변화**, VBM 아님 | comp1→modelc gap +0.033 eV ≈ 불변; VBM character 불변 | **✓ 일치** — 둘 다 "VBM 고정, 변하는 건 CB/gap 크기". 우리 modelc는 Cl *증량*이라 gap 거의 안 변(치환종이 아님); Banik은 양이온 치환이라 CB가 더 움직임. |
| **분해산물** | 폴리설파이드·S·(P–S)ₓ + **LiX**(LiCl/LiI); LiX가 thiophosphate 산화 안정성↑(ref27) | comp1 staircase: Li₃PS₄ + 0.25 LiS4 + LiCl(+P₂S₇·S·SCl 상위); modelc 1.6 LiCl | **✓✓ 일치** — 동일 폴리설파이드+LiX 화학. Banik의 "LiX가 안정화"(ref27) = 우리 sei_products LiCl gap 6.65 wide-gap passivation 논리(단 우리는 *분해억제/전자차단*(B), Banik 인용 ref27도 같은 결). |
| **이론창 < 실험창** | 명시(Fig 1c; kinetics·중간상 미반영) | 우리 grand-potential = **비관적 하한**; 실전은 kinetic passivation으로 더 넓음 | **✓ 일치** — 우리 "셋 다 OCV metastable, 실전은 kinetic" 인식과 동일. |
| **할라이드 증량(Cl-rich) 축** | **다루지 않음**(Cl→I *교환*만; Cl 1.0→1.5/1.6 *증량* 아님) | 우리 핵심 modelc = Cl 1.0→1.6 *증량* | ✗ **범위 밖** — Banik은 Cl-rich(증량)를 안 봄. 우리 modelc·Zuo·Gil-González·Wu의 4축(증량 시 σ↑·계면·calendar)은 Banik 너머의 우리 기여. **단 "음이온 종류 바꿔도 산화창 불변"은 "음이온 증량해도 onset 불변"(우리)과 같은 결**. |
| **격자 산화물 도판트(cascade)** | **다루지 않음**(P→Si/Ge cation, Cl→I anion만) | cascade 47 dopant(Nd₂O₃·B₂O₃·Sc₂O₃…), 대부분 ox=2.14 V pin, B₂O₃=2.317 V shift | ✗ **다른 레버지만 결론 호응** — Banik "MS₄·할라이드 치환은 onset 못 옮김"은 우리 cascade "대부분 S-limited 2.14 V pin"과 *정신 동일*. **단 우리는 B₂O₃(+0.18 V)·Cr₂O₃/Sc₂O₃/In₂O₃(2.356 V) 등 onset을 *옮기는* 소수 도판트도 발견** → Banik 명제의 *예외*를 우리가 정량(아래 §8 #2). |
| **Nd 산화 onset 하강** | n/a(Nd 안 봄) | nd onset 1.92 V(< 2.14), 단 trace Nd-S; bulk 폴리설파이드는 2.30 V(modelc보다 늦음) | ✗ **범위 밖** — Banik 프레임(S-pin)과 충돌 아님: Nd의 1.92 V는 *Nd-S* 산화(S backbone 아님), bulk S는 여전히 ~2.3 V로 S-limited → Banik "S가 pin"과 정합. |

**§7 한 줄 결론**: 이 논문은 **우리 axis_1(intrinsic 0-pressure window) 결론·메커니즘·방법의 외부·동방법 검증**이다. "치환은 S-limited 산화 onset을 못 옮긴다 + VBM=S 3p가 pin + grand-potential로 평가 + 밴드엣지는 상한"의 **네 기둥이 모두 일치**. 우리가 *넘어선* 부분은 (a) Cl *증량*의 4축(σ/계면/constriction/calendar), (b) onset을 옮기는 *예외* 도판트(B₂O₃ 등)의 정량, (c) Nd O-doping passivation 산물 분석.

## 8. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| **1a** | 산화 분해 = cathode로 VBM→정공 전자이동 도식(밴드이론) | band-edge approach 그림; 우리 report "VBM=상한" 도식 짝 |
| **1b** | band-edge 창 vs phase-stability 창 비교 | 우리 "VBM(상한) vs grand-potential(실제)" 정확히 그 그림 → deck에 차용 |
| **1c** | LPSCl 실측 창(green) vs 계산 phase-stability(화살표) + Li–S·oxide-CAM 창. 산화 2.5 V·환원 0.6 V(In/InLi) | LPSCl 좌표계(S 양극 OK·oxide 양극 부족); 우리 2.14 V(Li⁺/Li)=2.5−0.62≈1.9 정렬 체크 |
| **2a–c** | LPSCl·Ge-Li₆PS₅I·Si-Li₆PS₅I stepwise CV(분해 peak 진화) | "낮은 reversal서 안정해 보여도 분해" = Zuo CV apparent-onset과 같은 주의 |
| **2d** | **mole-정규화 산화전류 vs V — 세 조성 onset 유사** | **핵심 그림**: "치환 무관 onset 동일" = 우리 comp1=modelc onset 동일의 실험판 |
| **3a** | 광학 흡수(Tauc), 모든 조성 gap >3 eV | 우리 "wide-gap insulator"(PBE 과소 caveat) 실측 앵커 |
| **3b** | **HAXPES VB 스펙트럼 — 모든 조성 VBM 같은 위치**(I계 엣지 강도↑) | **핵심**: "VBM 불변"의 *실험 직접 증거*(우리 DFT 절대 VBM은 비엄밀) |
| **3c** | 계산 열역학 산화창(green=stable, orange/red=분해) 4조성 | grand-potential 창 = 우리 방법 동일 산출; LPSCl·치환 모두 ~1.7–2.4 V |
| **3d** | 실험 산화 한계 4조성(계산과 유사, 약간 넓음) | 이론창<실험창(kinetics) = 우리 "비관적 하한" 인식 |
| **4a** | pDOS 개념도(Li⁺/PS₄ 반결합 위 / S²⁻·PS₄ 비결합 = VBM / Cl 깊이 / PS₄ 결합 맨아래) | **VBM 화학 본질 도식** — 우리 VBM=S 3p의 *왜*를 그림으로 |
| **4b** | 원소투영 pDOS(Li/P/S/Cl) — S가 VBM 지배 | 우리 electronic.json VBM=S 3p 91–93%의 외부 정성 일치 |
| **4c** | **COHP — CB=P–S 반결합, P–S 결합은 VBM보다 훨씬 아래** | 우리 ICOHP(P–S)·ELF(P–S 0.946)의 외부 COHP 짝; "비결합 S=VBM" 정량 근거 |
| S1 | XRD + Pawley | 상순도(맥락) |
| S2 | RT 임피던스 | Si/Ge가 LPSCl과 σ 유사(mass-transport 배제 근거) |
| S3 | CV reversal 최대전류 비교 | 산화전류 정량 |
| S4 | 전자구조(VBM·CBM Γ) | direct gap 확인 |
| S5 | **Lithium-evolution number vs V** | **우리 `get_element_profile`와 동일 산출물** — 분해창 원자료 |
| S6 | pDOS·COHP(전조성) | VBM=S(할라이드 무관) 전조성 확인; I 5p 엣지 기여 |
| S2(표) | 열역학 분해산물 목록 | 우리 staircase 분해산물과 대조(폴리설파이드/S/P–S/LiX) |
| S3(표) | **환원·산화 전위서 phase equilibria + I⁻/I₂가 ESW 무관** | I 5p가 엣지에 있어도 산화창 안 바꿈 = "S가 pin" 보강 |

## 9. Post-processing ★
- **grand-potential / phase-stability ESW**: Lithium-evolution number vs potential(Fig S5) → 안정창 + 분해산물(Table S2) + 전위별 phase equilibria(Table S3). **도구 = first-principles 열역학 hull**(코드 미명시; pymatgen-류 추정이나 근거 없음 → n/a). **= 우리 `tools/oxidation/esw_grand_potential.py`(get_element_profile)와 동일 산출물.**
- **전자구조**: pDOS(원소투영) + **COHP**(결합/반결합) → 밴드엣지 화학 본질. **= 우리 LOBSTER ICOHP/COHP + pDOS와 동일 도구류**(우리는 LOBSTER 명시; Banik은 COHP만 언급).
- **밴드 위치**: VBM/CBM @ Γ로 direct gap 판정.
- **실험 post-proc**: 광학 = Tauc plot ((F(R)·hν)² vs hν, direct); HAXPES = VB onset(선형외삽) → VBM; CV = reversal별 전류 onset/peak → 실효 창.
- **수치화·기록**: 창은 전압범위(V), VBM은 스펙트럼 onset, gap은 Tauc 외삽 eV, 분해는 산물 리스트.
> **우리 적용**: Banik의 **"HAXPES VBM(불변) + grand-potential 창(불변) + CV onset(불변)" 3중 교차** = 우리 `VBM_vs_grandpotential_report`를 한 논문에 담은 템플릿. 우리 deck에서 "밴드엣지 측정(UPS/HAXPES)은 *band alignment*용, 산화 onset은 grand-potential/CV"라 말할 때 **Banik을 외부 실증으로 인용** 가능.

## 10. 주의/한계 (over-claim 방지) — 비판적으로
- **DFT 디테일 미공개**: functional·k·ecut·U·supercell·**무질서 처리**가 본문·SI 발췌 범위에 **없음**. → 우리가 "같은 grand-potential"이라 해도 *수치 재현성*은 검증 불가; **절대 gap·절대 onset 1:1 비교 금지**(우리 PBE 2.07 vs 그들 광학 >3은 functional/측정 차이). 우리 §7은 *메커니즘·결론·방법류*의 정합으로만.
- **전압 축 혼용**: In/InLi vs Li⁺/Li(+0.62 V). Fig 2·3 onset을 우리 2.14 V(Li⁺/Li)와 비교할 땐 축 정렬 필수. (Banik Fig 1c "2.5 V vs In/InLi"≈3.1 V vs Li⁺/Li는 *실험 apparent* onset; 우리 2.14는 *열역학*. 직접 등치 금지.)
- **치환 축이 다름**: Banik = **P→Si/Ge(cation), Cl→I(anion 교환)**. 우리 핵심 = **Cl 1.0→1.6(anion 증량)** + **격자 산화물 도판트(cascade)**. "치환 무관"의 *결론*은 같지만 *대상*이 달라 — "Banik이 우리 Cl-rich/cascade를 검증"이라 하면 부정확. 정확히는 "**'S가 있는 한 음·양이온 치환은 산화 onset을 못 옮긴다'는 *일반 명제*를 Banik이 (다른 치환계로) 실증, 우리 결론과 호응**".
- **Banik 명제의 *예외*를 우리가 가짐**: 우리 cascade에서 **B₂O₃(ox 2.317 V, +0.18)·Cr₂O₃/Sc₂O₃/In₂O₃/Ga₂O₃(2.356 V)·Y₂O₃(2.282)** 등 **산화 onset을 *옮기는* 도판트**가 소수 존재(대부분은 2.14 pin이지만). 즉 Banik "단순 치환은 못 바꾼다"는 *MS₄·할라이드 동족치환*엔 맞지만, **이질 산화물 도판트(B³⁺ 등)는 새 산화-한정 반응을 만들어 onset을 약간 올릴 수 있음** → Banik을 "*절대* 못 바꾼다"로 일반화 금지. (단 이동폭 ≤0.2 V로 작고, 산화물 도판트도 *S backbone* 산화는 못 늦춤.)
- **Li₆PS₅I HAXPES 실패**: I 미치환계 VBM은 *실측 없음*(charging). I 효과는 *치환계(Si/Ge-Li₆PS₅I)*로만 봄.
- **kinetic·constriction·calendar 미포함**: Banik은 *intrinsic*(축 1)만. 우리 Gil-González(축 2 constriction)·Zuo(축 3 계면)·Wu(축 4 calendar)의 다축이 Banik 너머. "산화 안정성 = 한 숫자"로 읽으면 안 됨(우리 multi-axis 원칙과 동일).

## 11. 적용 인사이트 (깊게) — 우리 연구에 어떻게
1. **`axis_1` 외부 정답지 확보 → deck/논문 1순위 인용**: "치환은 S-limited 산화 onset을 못 옮긴다"를 *Zeier 실험 + Mo 계산*이 독립 발표. 우리 "comp1=modelc onset 2.14 V(S²⁻-limited)"는 이제 **외부·동방법·동그룹(Mo) 검증을 가진** 결론. → 인용: "Consistent with Banik et al. (Zeier & Mo), where cationic/anionic substitution does not shift the S-pinned oxidative onset of Li₆PS₅X, our grand-potential ESW gives an identical 2.14 V onset for LPSCl and Cl-rich LPSCl1.6."
2. **"S가 VBM·산화 한계를 pin" = 우리 VBM=S 3p의 *왜*를 COHP로 설명**: Banik Fig 4c(P–S 결합 깊이, 비결합 S가 VBM)가 우리 ICOHP(P–S)/ELF의 해석을 외부에서 확증. → 우리 electronic 분석에 "non-bonding S 3p forms the VBM (cf. Banik COHP)" 한 줄 추가 가능.
3. **HAXPES = UPS급 밴드엣지의 *bulk* 버전 → 우리 report의 실험 짝 강화**: Whitten(UPS 튜토리얼)이 *기법*이라면, Banik은 *그 기법으로 argyrodite VBM 불변을 실측*한 사례. 우리 "VBM(밴드엣지)은 band alignment용, 산화 onset은 grand-potential/CV"에 **HAXPES 실증**을 더함.
4. **우리 *차별화* 명확화(정직)**: Banik은 (a) Cl *증량*, (b) 산화물 도판트, (c) Nd passivation, (d) 다축(constriction/calendar)을 *안 함*. 우리 기여 = "S-pin이라는 *공통 한계 위에서*, Cl-rich가 *산화 onset은 안 바꾸되* σ·계면·constriction·calendar 4축에서 어떻게 다른가" + "**산화물 도판트가 onset을 옮길 수 있는 소수 예외(B₂O₃)**" + "**Nd O-doping은 onset을 살짝 내리되 wide-gap passivation 산물로 보상**". → deck "우리 연구의 위치": *Banik이 닫은 '치환=산화 onset 불변'을 출발점으로, 우리는 그 위의 다축·예외·passivation을 정량*.
5. **"코팅/타 물질군 필요" = 우리 그룹 cathode-interface 3부작(Cha/Kang25/Kang)·Sundar 코팅 스크린의 *동기*와 정확히 일치**: Banik 결론("S 빼는 게 아니면 코팅이 답")이 우리 그룹 코팅 라인과 Sundar ALD 코팅 작업의 *문제설정*을 외부에서 정당화. → "intrinsic SE 산화창은 치환으로 못 늘리므로(Banik), 실전 고전압은 *계면 관리*(코팅·passivation)로 간다"는 서사 완성.

## 12. 인용 가능 문장 (deck/paper용)
- "Banik et al. (Zeier & Mo groups) show — by HAXPES, optical gap, DFT pDOS/COHP, grand-potential phase stability, and stepwise CV in concert — that the oxidative stability of Li₆₊ₓMS₅X is *pinned by sulfur* (non-bonding S 3p of PS₄³⁻ and free S²⁻ form the VBM), so cationic (P→Si/Ge) and anionic (Cl→I) substitutions do not move the oxidation onset."
- "This independently validates our axis-1 result that LPSCl and Cl-rich LPSCl1.6 share an identical S²⁻-limited grand-potential oxidation onset (2.14 V vs Li/Li⁺) despite differing band-edge positions."
- "Because the onset is S-limited (Banik; ours), raising the practical oxidative stability of a sulfide SE requires cathode coatings or a different materials class — not substitution — framing our group's cathode-interface coating line and the O-doping passivation strategy as the correct levers."
- "Our cascade refines Banik's general statement: while *iso-structural* MS₄/halide substitutions leave the 2.14 V S-onset untouched, a few heterovalent oxide dopants (e.g. B₂O₃, +0.18 V) introduce new oxidation-limiting reactions that shift the onset modestly — though none delays the sulfur backbone oxidation itself."

## 13. 주의/한계 재요약 (한 줄)
Banik = **intrinsic(축 1) 산화 onset이 치환 무관임을 S-pin으로 실증한 외부·동방법 정답지**. **DFT 디테일 미공개·전압축 혼용·치환축 상이(증량/도판트 아님)·다축 미포함**이 한계 → 우리는 *메커니즘·방법·결론*을 정합으로 받고, *Cl-증량 4축·예외 도판트·Nd passivation*을 우리 기여로 분리. "산화 안정성=한 숫자"로 읽지 말 것.

## 14. 기법 용어 미니사전
- **Phase-stability(grand-potential) approach**: SE를 반응물로 보고 μ_Li를 스캔, 각 전압서 분해 자유에너지로 *실제* 산화/환원 분해 전압·산물을 결정. = 우리 grand-potential ESW(Mo–Ong–Ceder 2012; Yifei Mo가 이 논문 공저자).
- **Band-edge(HOMO-LUMO) approach**: cathode ε_F vs SE VBM(산화)·anode ε_F vs SE CBM(환원)으로 *전자적* 안정 상한. 실제 분해창보다 넓음(상한). gap이 곧 band-edge 창.
- **HAXPES(hard X-ray photoemission spectroscopy)**: 고에너지 X선(6 keV)으로 *bulk* 가전자대(VBM) 측정. UPS(자외선, 표면 민감)의 bulk·심부 버전. VBM=DFT VBM과 같은 물리량(수직 이온화=밴드엣지) → *band alignment*용(산화 onset은 아님).
- **stepwise CV**: reversal 전위를 단계적으로 올리며 반복 스캔 → 분해산물 redox feature 진화로 *실효* 산화 안정 한계 측정. C–SE 복합으로 계면적↑.
- **pDOS**: 원소/궤도 투영 상태밀도 — 어느 원자가 어느 band를 만드나(여기선 VBM=S).
- **COHP / −COHP**: Crystal Orbital Hamilton Population — 에너지별 결합(bonding)/반결합(antibonding) 기여(여기선 CB=P–S 반결합, P–S 결합은 VBM 아래 깊이). = 우리 LOBSTER ICOHP/COHP.
- **Lithium-evolution number**: μ_Li(전압) 변화에 따른 분해 시 Li 방출/흡수량 — grand-potential 분해창의 원자료(우리 get_element_profile evolution과 동일).
- **In/InLi 기준**: 0.62 V vs Li⁺/Li. 황화물 ASSB 실험서 흔한 음극(완충). 본문 전압 다수가 이 기준.
