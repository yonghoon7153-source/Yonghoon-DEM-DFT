# Origin of Outstanding Stability in the Lithium Solid Electrolyte Materials: Insights from Thermodynamic Analyses Based on First-Principles Calculations — Zhu/He/Mo (ACS Appl. Mater. Interfaces 2015)

> slug `zhu2015_esw_grand_potential_origin` · DOI `10.1021/acsami.5b07517` · type `DFT (MP-hull thermodynamics, 실험 0)` · PDF `127e2023-38._Originations.pdf` + SI `db1e808d-38._Sup_Orations.pdf` (inbox #38) · digested `2026-07-28` · status ✅
> elements: Li, P, S, Cl, O, Ge, I, N, F, Zr, La, Ti, Al, Si, Nb, Ta, Zn
> methods: DFT, ESW
> **저자**: Yizhou Zhu, Xingfeng He, **Yifei Mo*** (Univ. of Maryland, College Park) · ACS AMI 2015, 7, 23685−23693 · Received 2015-08-13 / Published 2015-10-06
> ⚠ 서지 교정: 과제 메모의 DOI `10.1021/acsami.5b01004`는 오기 — PDF 실물 각 페이지 풋터가 **`10.1021/acsami.5b07517`** (본문·SI 모두 확인).

---

## 0. 이 digest를 읽는 법 (우리 캠페인에서의 위치)
**우리 `oxidation_stability.json` / `oxidation_stability_cascade.csv`가 쓰는 grand-potential ESW 방법의 원전(原典)이다.** Mo 2012(LGPS 단일물질)·Ong 2008(Li–Fe–P–O₂)의 grand-potential phase diagram을 **SE 물질군 전체(14종)+Li binary(7종)+코팅(5종)에 처음 체계 적용**해, (i) "SE의 진짜(thermodynamic) 창은 좁다", (ii) "CV의 0–5 V는 kinetic 과전압+분해산물 interphase passivation의 겉보기 창"이라는 — 이후 [Banik]·[GG]·[Kang]·[Son]·Schwietert가 전부 딛고 서는 — 서사의 출발점. **Li₆PS₅Cl(=comp1)이 계산 대상에 포함**되어 있어 우리 canonical과 숫자 단위 대조가 가능하다. [Zhu20](공기안정 설계)의 ref [2], [Kang] Fig 1a의 ref 49, [Bai] §4 계면의 "환원 ~1.7 V·분해 Li₃PS₄+S+LiCl"의 1차 출처가 모두 이 논문.

## 1. 한 줄 요약
14종 Li SE의 grand-potential 창을 MP-hull로 전수 계산해 **"대부분의 SE는 Li 금속에도 고전압에도 열역학적으로 불안정하고(황화물 intrinsic 창 ~1.6–2.3 V), 실험서 보이는 '0–5 V 안정'은 intrinsic이 아니라 ① 분해 kinetics의 과전압과 ② 전자절연 분해산물 interphase(=SEI)의 passivation에서 온 것"**임을 처음 정량화 — 산물이 전자전도성(Li–Ge 합금·Ti³⁺)이면 passivation 실패(연속 분해), 코팅은 같은 원리의 인공 SEI로 황화물 anodic limit을 ~2–2.3→~4 V로 확장.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자/기관 | Zhu, He, Mo* (UMD MSE + UMD Energy Research Center) |
| 저널 | ACS Appl. Mater. Interfaces 2015, 7, 23685−23693 |
| DOI | 10.1021/acsami.5b07517 (⚠ 5b01004 아님) |
| 유형 | 순수 계산 (DFT + MP 데이터베이스 열역학; 자체 실험 0) |
| 대상 | **황화물 8**: Li₂S, LGPS(Li₁₀GeP₂S₁₂), Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄, Li₃PS₄, Li₄GeS₄, Li₇P₃S₁₁, **Li₆PS₅Cl**, Li₇P₂S₈I / **산화물 6**: LiPON(Li₂PO₂N), LLZO, LLTO, LATP, LAGP, LISICON / **Li binary 7**: LiF, LiCl, LiI, Li₂O, Li₂S, Li₃N, Li₃P / **코팅 5**: Li₄Ti₅O₁₂, LiNbO₃, Li₂SiO₃, LiTaO₃, Li₃PO₄ |
| 핵심 질문 | CV의 0–5 V 창 vs 계산·in-situ XPS의 분해 관찰 — 이 "outstanding discrepancy"의 근원은? SE는 정말 0–5 V "true" 창을 가질 수 있나? |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| **Li₆PS₅Cl 창** | **1.71–2.01 V** (0.30 V) | grand-potential, MP-2015 hull, E_hull→0 규약 | red: P+Li₂S+LiCl / ox: Li₃PS₄+S+LiCl |
| LGPS 창 | 1.71–2.14 V | 〃 | 최종산화 2.31 V (P₂S₅+GeS₂+S) |
| 황화물 전반 | 환원 ~1.6–1.7 V / 산화 ~2–2.5 V | 〃 | Li₇P₃S₁₁ 2.28–2.31 = 전체 최협(0.03 V) |
| 산화물 전반 | 산화 2.9–4.3 V | 〃 | LATP 4.21 / LAGP 4.27 V (최고) |
| LPSCl 0 V 환원 | E_D **−0.96 eV/atom** → **Li₃P+Li₂S+LiCl** | Li 금속 접촉 | 우리 0 V 산물과 정확 동일 |
| LPSCl 5 V 산화 | E_D **−1.33 eV/atom** → P₂S₅+S+**PCl₃** | 5 V | Cl까지 산화(2.88 V부터) |
| 이온전도도/Ea/기계/gap | n/a | — | 이 논문 범위 밖 (열역학 전용) |

## 4. DFT/계산 방법 ★ (방법론 형식화 — 최우선)
- **code**: VASP, PAW, **PBE(GGA)**. cutoff·k-point 밀도는 **"Materials Project와 일관"**(수치 명시 없음 — MP 표준 520 eV·k-density 상속으로 읽음).
- **에너지 보정**: 산화물·전이금속·기체 분자에 **MP 보정 스킴**(refs 18–19 = Wang 2006 GGA+U 산화에너지 + Jain 2011 GGA/GGA+U 혼합) 적용. ⚠ **2015년 세대 보정** — MP2020 음이온(S) 보정 이전 (→ §7 우리와의 onset 차이의 근원).
- **데이터 소스**: 대부분 **MP 데이터베이스**(ref 20)에서 소환; MP에 없는 물질만 자체 DFT (실험 구조 기반).
- **무질서 처리**: 무질서 점유 구조는 **50–60개 배열 샘플 → 최저에너지 배열을 GS로**(Mo 2012 LGPS 방법). LLTO는 실험구조(Fourquet)에서 ordering.
- **grand-potential phase diagram** (pymatgen, ref 22):
  - **eq 1**: `μ_Li(φ) = μ⁰_Li − eφ` — 전위 φ(vs Li/Li⁺)가 Li 저장고의 화학퍼텐셜을 내림. Li 금속 기준.
  - **eq 2**: `E_D(φ) = E(phase equilibria, φ) − E(SE) − Δn_Li·μ_Li(φ)` — 전위 φ에서의 분해 구동력. Δn_Li = 분해 시 SE 조성→평형조성 Li 개수 변화.
  - **PV·엔트로피 항 무시** (0 K; refs 11, 21과 동일 근사) — 명시적 자인.
- **창 읽는 규약**: 각 φ에서 조성의 hull 평형(phase equilibria)을 구하고, **환원전위 = 최고전압 lithiation plateau(Δn_Li>0)**, **산화전위 = 최저전압 delithiation plateau(Δn_Li<0)**. 그 사이가 intrinsic ESW. SI Table S2가 물질별 전 계단(plateau 전압·Δn_Li·평형상) 명세.
- **metastable SE 처리 (중요 규약)**: E_hull>0인 SE는 **"energy above hull을 0으로 낮춰서"** 평가 — Li/이온 무질서의 엔트로피 안정화(LGPS 선례)로 정당화. **Li₆PS₅Cl의 E_hull = 83 meV/atom**(Deiseroth 구조의 ordered 배열; 조성 평형 = Li₃PS₄+Li₂S+LiCl) → 0으로 규약. LGPS 21 / Li₇P₃S₁₁ 22 / LLZO 7 / LLTO 68 / LATP 29 / LISICON 34 meV/atom (Table S1).
- **ICSD 구조 없는 조성**(Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄, LAGP, Li₇P₂S₈I): 해당 조성의 phase equilibria 조합을 E_hull=0 entry로 구성.
- **LiPON**: 실물은 amorphous·조성 범위 — 결정질 **Li₂PO₂N**(Senevirathne 2013)을 대표로.
- **AIMD / MLIP / NEB / COHP / Bader / DOS**: 없음 (순수 hull 열역학).

### 4b. "true vs 겉보기(kinetic) window" 구분 논리 (서사의 원형)
1. **Intrinsic(true) window** = 위 열역학 창. 황화물 ~1.7–2.3 V로 좁다.
2. **겉보기 창이 넓은 이유 ①: kinetic 과전압** — 산화 분해산물 대부분이 전자절연이고, non-Li 원소의 고체 내 확산이 느리고, O₂/N₂ 기체 핵생성·방출이 느림 → 분해 반응 자체가 sluggish. metal–air OER에서 >1 V 과전압이 흔함(ref 37)을 유추 근거로 → **nominal 산화전위 >5 V로 보일 수 있음**. ⚠ 단 "과전압 하에서도 열역학적으로는 여전히 자발 → 장기적으로는 진행되어 열화"를 명시 (kinetic stabilization ≠ passivation).
3. **겉보기 창이 넓은 이유 ②: 분해산물 interphase의 passivation** — §6. 이것이 논문 제목의 "origin of outstanding stability".
4. Figure 4가 통합: **관찰되는 nominal 창 = SE intrinsic 창 + (anode interphase 창) + (cathode interphase/코팅 창) + 과전압**.

## 5. 결과 I — Li 금속·저전압 환원 (§3.1, Table 1·2, Fig 1)
- **대부분의 SE는 Li 금속에 열역학 불안정.** 0 V에서 highly favorable한 분해 (Fig 1: E_D가 창 밖에서 전위에 선형으로 하강, 0 V에서 황화물 −0.9~−2.0 eV/atom).
- **Li binary(LiF, Li₂O, Li₂S, Li₃P, Li₃N)는 0 V 안정** (Fig 2a) — 이것이 뒤의 passivation 논리의 뿌리.
- **LGPS**: 1.71 V부터 환원 시작, 최종 0 V에서 Li₁₅Ge₄+Li₃P+Li₂S, **E_D −1.25 eV/atom (= −3014 kJ/mol LGPS)**. CV·XPS 실험(ref 12: 1.71 V 환원 개시·Li–Ge 합금 형성)과 정합.
- **황화물 공통**: 환원전위는 **P·Ge의 환원이 지배**, ~1.6–1.7 V에서 시작. 0 V 산물 = Li₃P + Li₂S (+ Ge계는 Li–Ge 합금, **Cl→LiCl, I→LiI**). Li₇P₃S₁₁만 2.28 V (Li₃PS₄ 함유 조성이라 Li₃PS₄로의 lithiation이 먼저).
- **산화물**: LLTO 1.75 V·LATP 2.17 V부터 **Ti⁴⁺→Ti³⁺ 이하** 환원 (LLTO 실험 1.7–1.8 V와 정합, refs 24–25; in-situ XPS의 Ti 환원 refs 14–15 정합). LAGP 2.70 V·LISICON 1.44 V부터 **Ge 환원→Li–Ge 합금** (refs 26–28 정합).
- **"Li에 안정하다고 알려진" SE도 계산상 환원됨**: LiPON 0.68 V (0 V 산물 Li₃P+Li₃N+Li₂O, E_D −0.66 eV/atom — in-situ XPS ref 13과 산물 일치), Li₃PS₄·Li₇P₂S₈I도 환원 → **"이들의 Li 안정성은 thermodynamically intrinsic이 아니다"**.
- **LLZO 예외**: 환원전위 **0.05 V**·0 V E_D **−0.021 eV/atom(49 kJ/mol)** = 전 SE 중 최소 구동력 → kinetic 억제 용이 + 산물(Li₂O·Zr₃O·La₂O₃) passivation → 문헌의 0–5 V 창 설명. **단 0.004 V·0.021 eV/atom은 "DFT 정확도·스킴 근사 이하 → Zr₃O/Zr로 환원되는지 inconclusive"라고 자인** (⚠ 미세 창 판정의 hull-오차 경고 — 우리 collapse 판정에 시사, §7). 300 °C에서 garnet–Li 불안정 실험(ref 36)을 온도로 kinetics가 풀린 사례로 해석.

### Table 2 전량 — Li 금속(0 V) 환원: 평형상 + E_D (eV/atom)
| SE | 0 V 평형상 | E_D |
|---|---|---|
| Li₂S | Li₂S (안정) | 0 |
| LGPS | Li₁₅Ge₄, Li₃P, Li₂S | −1.25 |
| Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄ | Li₁₅Ge₄, Li₃P, Li₂S | −1.28 |
| Li₃PS₄ | Li₃P, Li₂S | −1.42 |
| Li₄GeS₄ | Li₁₅Ge₄, Li₂S | −0.89 |
| Li₇P₃S₁₁ | Li₃P, Li₂S | −1.67 |
| **Li₆PS₅Cl** | **Li₃P, Li₂S, LiCl** | **−0.96** |
| Li₇P₂S₈I | Li₃P, Li₂S, LiI | −1.26 |
| LiPON | Li₃P, Li₃N, Li₂O | −0.66 |
| LLZO | Zr(또는 Zr₃O), La₂O₃, Li₂O | −0.021 |
| LLTO | Ti₆O, La₂O₃, Li₂O | −0.34 |
| LATP | Ti₃P, TiAl, Li₃P, Li₂O | −1.56 |
| LAGP | Li₉Al₄, Li₁₅Ge₄, Li₃P, Li₂O | −1.99 |
| LISICON | Li₁₅Ge₄, LiZn, Li₂O | −0.77 |

## 6. 결과 II — passivation 메커니즘 (§3.1 후반, Fig 2) ★ "kinetic stabilization/passivation 서사의 원형"
- **화학퍼텐셜 분해**: `μ_Li = μ̃_Li⁺ + μ̃_e⁻`. 계면 평형에서 **고이동도 Li⁺의 전기화학퍼텐셜 μ̃_Li⁺는 계면을 가로질러 (거의) 일정**, 반면 **interphase가 전자절연이면 μ̃_e⁻가 interphase에서 급락** → SE가 실제로 보는 **μ_Li가 anode의 극한값에서 SE 창 안쪽으로 강하** → 분해 구동력 소멸, **분해 정지**. Fig 2b(anode)·Fig 3b(cathode) 도식. **분해산물 interphase = 사실상 ASSB의 SEI.**
- **passivation 성립 조건 = 산물의 전자절연성**: Li 환원산물이 **Li binary(Li₂O, Li₂S, Li₃P, Li₃N, LiCl, LiI, LiF)** — 0 V 안정 + 전자절연 → **LiPON·Li₃PS₄·Li₇P₂S₈I의 실험적 Li-호환성의 근원**. (Li₃N·Li₃P는 고 Li⁺ 전도(refs 50–51) → 계면 저항도 낮음 = LiPON–Li 계면이 좋은 이유.)
- **passivation 실패 = MCI(mixed conducting interphase)**: **LGPS·LAGP·LISICON → 전자전도성 Li–Ge 합금**, **LLTO·LATP → Ti³⁺ 이하 티타네이트(전자전도)** → interphase가 전자·이온 혼합전도 → μ_Li 강하 불가·분해 물질수송 촉진 → **벌크로 계속 분해** (Janek in-situ XPS의 MCI, ref 15와 정합). CV서 관찰되는 LGPS/LLTO/LATP/LAGP/LISICON의 lithiation이 이것.
- **Fig 2a — Li binary·SE의 창 막대**(dashed = 완전 delithiation 전위): binary 산화전위 — Li₂S 2.01 V(Table 1)·Li₂O 2.9 V(본문; Li₂O₂ 경유 O₂ 방출)·LiI→I ~2.47 V(SI-g)·LiCl→PCl₃ 2.88 V(SI-f, P₂S₅/S 공존계) — LiF가 최고(막대 ~6.4 V, figure-read)·Li₃N 최저(~0.5 V, figure-read). **Cl⁻/I⁻ 산화가 S²⁻보다 늦다** = 할라이드 도핑의 산화측 무해성 뿌리.
- ⚠ 저자 캐비앗: 이 스킴은 **중성 Li의 평형 = 필요조건**; 하전 캐리어(e⁻/Li⁺)의 평형·space-charge·결함화학은 별도(refs 32–33) — interphase에 전자/홀 축적 시 전자전도 활성화되어 passivation 꺼질 수 있음을 명시.

## 7. 결과 III — 고전압 산화 (§3.2, Table 3, Fig 3)
- **황화물**: 2–2.5 V부터 산화. **S²⁻→S⁰이 공통**, P→P₂S₅·Ge→GeS₂. LGPS 2.14 V 개시(→Li₃PS₄+GeS₂+S), 2.31 V 완전산화(P₂S₅+GeS₂+S) — CV 실험(ref 12) 정합. **Li₆PS₅Cl: 2.01 V → Li₃PS₄+S+LiCl** (SI: 2.31 V P₂S₅+S+LiCl → **2.88 V P₂S₅+S+PCl₃** = Cl까지 산화되어 완전 delithiation). 5 V 분해에너지 황화물 −0.9~−2.0 eV/atom = "highly favorable".
- **산화물**: LLZO 2.91(→Li₂O₂+La₂O₃+Li₆Zr₂O₇; 3.30 V부터 O₂)·LISICON 3.39·LLTO 3.71 V. **NASICON계 LATP 4.21·LAGP 4.27 V = 최고 + 5 V 구동력 최소(~−0.06 eV/atom)**. 고전압 산화는 전부 **O₂ 방출 동반**(Li₂O 2.9 V 산화·Li₂O₂ 재산화의 연장). LiPON 2.63 V(N₂ 방출) — Yu et al. I–V onset ~2.6 V·6 V 기포 관찰(ref 10) 정합.
- **과전압 논리**(→§4b): 절연 산물·non-Li 확산·기체(O₂/N₂) 핵생성 sluggish → nominal 산화전위 >5 V 가능.

### Table 3 전량 — 5 V 산화: 평형상 + E_D (eV/atom)
| SE | 5 V 평형상 | E_D |
|---|---|---|
| Li₂S | S | −1.99 |
| LGPS | GeS₂, P₂S₅, S | −1.12 |
| Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄ | P₂S₅, S, GeS₂ | −1.08 |
| Li₃PS₄ | S, P₂S₅ | −1.01 |
| Li₄GeS₄ | GeS₂, S | −1.27 |
| Li₇P₃S₁₁ | S, P₂S₅ | −0.92 |
| **Li₆PS₅Cl** | **P₂S₅, S, PCl₃** | **−1.33** |
| Li₇P₂S₈I | P₂S₅, S, I₂ | −1.04 |
| LiPON | PON, P₂O₅, N₂ | −0.69 |
| LLZO | O₂, La₂O₃, La₂Zr₂O₇ | −0.53 |
| LLTO | O₂, TiO₂, La₂Ti₂O₇ | −0.15 |
| LATP | O₂, TiP₂O₇, Ti₅P₄O₂₀, AlPO₄ | −0.065 |
| LAGP | Ge₅O(PO₄)₆, GeP₂O₇, AlPO₄, O₂ | −0.056 |
| LISICON | Zn₂GeO₄, GeO₂, O₂ | −0.57 |

### Table 1 전량 — 전해질별 창 + 양끝 분해산물
| SE | 환원 (V) | 환원 평형상 | 산화 (V) | 산화 평형상 | 창 (V) |
|---|---|---|---|---|---|
| Li₂S | – | Li₂S (0 V 안정) | 2.01 | S | – |
| LGPS | 1.71 | P, Li₄GeS₄, Li₂S | 2.14 | Li₃PS₄, GeS₂, S | 0.43 |
| Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄ | 1.71 | P, Li₄GeS₄, Li₂S | 2.14 | Li₃PS₄, GeS₂, S | 0.43 |
| Li₃PS₄ | 1.71 | P, Li₂S | 2.31 | S, P₂S₅ | 0.60 |
| Li₄GeS₄ | 1.62 | Li₂S, Ge | 2.14 | GeS₂, S | 0.52 |
| Li₇P₃S₁₁ | 2.28 | Li₃PS₄, P₄S₉ | 2.31 | S, P₂S₅ | **0.03 (최협)** |
| **Li₆PS₅Cl** | **1.71** | **P, Li₂S, LiCl** | **2.01** | **Li₃PS₄, LiCl, S** | **0.30** |
| Li₇P₂S₈I | 1.71 | P, Li₂S, LiI | 2.31 | LiI, S, P₂S₅ | 0.60 |
| LiPON | 0.68 | Li₃P, LiPN₂, Li₂O | 2.63 | P₃N₅, Li₄P₂O₇, N₂ | 1.95 |
| LLZO | 0.05 | Zr₃O, La₂O₃, Li₂O | 2.91 | Li₂O₂, La₂O₃, Li₆Zr₂O₇ | 2.86 |
| LLTO | 1.75 | Li₄Ti₅O₁₂, Li₇/₆Ti₁₁/₆O₄, La₂Ti₂O₇ | 3.71 | O₂, TiO₂, La₂Ti₂O₇ | 1.96 |
| LATP | 2.17 | P, LiTiPO₅, AlPO₄, Li₃PO₄ | 4.21 | O₂, LiTi₂(PO₄)₃, Li₄P₂O₇, AlPO₄ | 2.04 |
| LAGP | 2.70 | Ge, GeO₂, Li₄P₂O₇, AlPO₄ | 4.27 | O₂, Ge₅O(PO₄)₆, Li₄P₂O₇, AlPO₄ | 1.57 |
| LISICON | 1.44 | Zn, Li₄GeO₄ | 3.39 | Li₂ZnGeO₄, Li₂GeO₃, O₂ | 1.95 |

### SI Table S2(f) — Li₆PS₅Cl 전 계단 (plateau 전압 / Δn_Li per f.u. / 평형상)
| φ (V vs Li/Li⁺) | Δn_Li | 평형상 |
|---|---|---|
| 0.87 | +8 | Li₃P, Li₂S, LiCl |
| 0.93 | +6 | LiP, Li₂S, LiCl |
| 1.17 | +5.43 | Li₃P₇, Li₂S, LiCl |
| 1.30 | +5.14 | LiP₇, Li₂S, LiCl |
| **1.71** | **+5** | **P, Li₂S, LiCl** |
| — | 0 | Li₆PS₅Cl (E_hull→0 규약) |
| **2.01** | **−2** | **Li₃PS₄, S, LiCl** |
| 2.31 | −5 | P₂S₅, S, LiCl |
| 2.88 | −6 | P₂S₅, S, PCl₃ (완전 delithiation) |

(참고 — Li₃PS₄ 계단(S2c): 0.87(+8 Li₃P+Li₂S)/0.93/1.17/1.30/1.71(+5 P+Li₂S)/[0]/2.31(−3 P₂S₅+S). LGPS(S2a): 0.28→1.71 계단 뒤 2.14(−4 GeS₂+Li₃PS₄+S)/2.31(−10 P₂S₅+GeS₂+S). Zhu의 plateau 표기는 각 assemblage의 **고전압 끝**(=그 조성이 안정한 창의 위 경계) 기준 — 우리 pymatgen 출력(각 field의 저전압 끝)과 관례가 한 경계씩 어긋남, §10 맵핑 참조.)

## 8. 결과 IV — 코팅 = 인공 SEI (§3.3, Fig 3, SI Table S3)
- 코팅 재료(Li₄Ti₅O₁₂, LiTaO₃, LiNbO₃, Li₂SiO₃, Li₃PO₄)의 창 = **환원 0.7–1.7 V ~ 산화 3.7–4.2 V** → 2–4 V(통상 사이클 범위) 안정 + **전자절연 → 인공 SEI로 SE를 passivation** (자발 interphase와 동일 메커니즘, §6).
- 개별 창(SI Table S3): Li₄Ti₅O₁₂ 1.75–3.71 / LiNbO₃ 1.74–3.88(3.92 Nb₂O₅) / Li₂SiO₃ 0.76–3.74 / LiTaO₃ 1.18–3.95(4.12 Ta₂O₅) / **Li₃PO₄ 0.69–4.21**(4.33 LiPO₃·4.99 P₂O₅). Fig 3a의 3.9 V 수평선 = **LiCoO₂ 평형전압**.
- **효과**: 황화물 SE의 anodic limit **~2–2.3 V → ~4 V** 확장; 코팅 자체의 산화 과전압으로 nominal은 그 이상. anode 쪽도 동일 전략(Polyplus의 LATP 보호, ref 46).
- **코팅 > 자발 interphase인 이유**(§4 Discussion): 박막증착 코팅은 **수 nm**(자발 분해층은 ~100 nm; <10 nm이면 계면저항 유의미하게 낮음, refs 16·42) + **비-Li 원소 상호확산 차단**(LCO–황화물 계면의 Co/S 교환 억제, ref 16) + **space-charge 완화**(ref 40).

## 9. Discussion 통합 + 설계 원리 (§4, Fig 4)
- **Fig 4 (통합 도식)**: 관찰되는 nominal 창 = **intrinsic 창(녹색) + anode interphase 확장(주황) + cathode interphase/코팅 확장(노랑) + kinetic 과전압(점선)**. "SE의 유효 창 = 자기 intrinsic 창 + interphase들의 창".
- **kinetic stabilization과 passivation은 별개**로 명시: 전자는 여전히 자발(장기 열화 경로), 후자는 구동력 자체를 제거.
- **Goodenough HOMO–LUMO 창**(ref 47)과의 관계: 전자 평형 기반의 LUMO–HOMO도 창 추정법이나, 본 스킴은 **중성 Li 평형** 기반 — 필요조건이며 실험 정합으로 타당성 주장. 하전종 평형(분극·space-charge·결함) 필요성은 인정.
- **설계 원리** (원문 §4):
  1. **환원은 cation이 지배** → **Ge·Ti 함유 회피**(전도성 합금/저가 티타네이트로 passivation도 실패); **Si·Sn·Al·Zn도 유사 우려** 명시.
  2. **anion은 무해** — Li 환원산물이 O·S·F·Cl·I 전부 **Li binary(안정+절연)** → LiPON·Li₃PS₄·Li₇P₂S₈I의 Li-호환 근원.
  3. **Li-halide 도핑 = "이온전도도와 Li 안정성을 동시에 얻는 highly effective한 설계"** (refs 30·48–49 — Li₇P₂S₈I·LiBH₄/LiI·**Li₆PS₅X**) ← **argyrodite Cl의 2015년 처방 원형**.
  4. interphase 성질(전자절연·고 Li⁺ 전도·박형)이 셀 성능 좌우; 나쁘면 **코팅으로 대체**. LGPS 분해상의 가역 사이클(ref 12 Han "single-material battery") = 분해상이 활물질화되는 경로(열화·저 CE의 근원)도 명시.

## 10. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md` ★★
### 10a. 방법 일치 판정 — `esw_cascade_batch.py`(PLAIN variant) vs Zhu 2015
| 요소 | Zhu 2015 | 우리 (esw_grand_potential.py / esw_cascade_batch.py) | 판정 |
|---|---|---|---|
| 형식 | grand potential: μ_Li(φ)=μ⁰−eφ, E_D=E(equil)−E(SE)−Δn·μ_Li, hull 평형 | pymatgen `PhaseDiagram.get_element_profile(Li, comp)` = 동일 construction (V = μ_Li(metal)−μ_Li, e=1) | **✓✓✓ 동일 형식** (같은 pymatgen 계보; Zhu가 pymatgen ref 22 사용) |
| hull 데이터 | **MP 2015** (구세대 보정: Wang06+Jain11, S 음이온 보정 없음) | **MP 2026, thermo_type GGA_GGA+U 고정**(MP2020 보정 포함) | △ **같은 DB, 다른 세대** → onset 수치 이동 (아래) |
| SE entry 처리 | SE를 **E_hull→0** entry로 삽입 (엔트로피 정당화) | **composition-only** (SE 에너지 미사용; hull 상끼리의 plateau만) | **✓ onset 위치는 등가** — 양쪽 다 창 경계가 hull상↔hull상 경계라 SE 자체 에너지와 무관. 차이는 E_D 절대값 산출 여부(그들 O, 우리 X) |
| 창 정의 | red = 최고전압 lithiation plateau / ox = 최저전압 delithiation plateau | red/ox = evolution ± 부호 경계 (동일) | **✓ 동일 정의** — 단 **plateau 라벨 관례가 한 경계 어긋남** (10b) |
| 무질서/metastable | 50–60배열 최저 + E_hull→0 | modelc는 조성만 (hull 미등재), comp1은 MP entry 존재 | ✓ 철학 동일 (조성 기준 창) |
| 결론 | — | — | **우리 cascade ESW는 Zhu 2015 방법의 직계 구현이 맞다** (형식·정의 동일; hull 세대만 현대화) |

### 10b. 수치 대조 — Li₆PS₅Cl 계단 (경계 맵핑 포함; 2026-07-28 이 digest에서 판정)
| hull 경계 (화학) | Zhu 2015 (MP2015) | 우리 (MP2026 GGA_GGA+U; `oxidation_stability.json`) | 해석 |
|---|---|---|---|
| 0 V 완전환원 산물 | Li₃P+Li₂S+LiCl (+8 Li, E_D −0.96 eV/atom) | **Li₃P+5Li₂S+LiCl (+8 Li)** — 정확 동일 | **✓✓✓ 산물·Δn 완전 일치** |
| P→LiP₇ 심화환원 경계 | 1.30 V | **1.24 V** (= 우리 CSV의 `red_V` 라벨) | ✓ 같은 경계, Δ0.06 V |
| **환원 onset** (Li₃PS₄+5Li→P+4Li₂S 경계) | **1.71 V** ("reduction potential") | **1.717 V** (= 우리 `ocv_V` 라벨의 neutral 경계) | **✓✓✓ Δ0.007 V — 11년 DB 세대 차에도 불변** |
| **산화 onset** (→Li₃PS₄+S(or LiS₄)+LiCl) | **2.01 V** (−2 Li, 원소 S) | **2.14 V**(PLAIN, LiS₄ 경유 −1.75 Li) / **2.256 V**(GG set, **−2 Li·원소 S = Zhu와 동일 반응**) | ✓ 반응 동일, 전압 +0.13~+0.25 V (hull 세대·S보정·LiS₄ entry) |
| P₂S₅/P₂S₇ 단계 | 2.31 V (P₂S₅+S+LiCl) | 2.36/2.385 V (P₂S₇+S 계열) | ✓ 같은 P–S 산화 단계 (상 동정만 DB 의존) |
| Cl 산화 종단 | **2.88 V (PCl₃)** | 3.33 V (SCl) / modelc 3.39 V (PCl₅) | ✓ "Cl은 맨 마지막" 공통; 종단상·전압은 DB 의존 |
| **창 폭** | **1.71–2.01 = 0.30 V** | 같은 구성으로 1.72–2.14 = **0.42 V** (GG set 0.54 V) | 창 자체는 좁다는 결론 동일 |
- **🔑 판정 ① (construct 맵핑)**: "Zhu red 1.71 V vs 우리 red 1.24 V"는 **모순이 아니라 라벨 관례 차이**. Zhu의 reduction potential(=lithiation이 시작되는 최고 전압)에 대응하는 우리 수치는 **`ocv_V` 1.717 V**(neutral 분해 Li₃PS₄+Li₂S+LiCl 창의 하단 경계)이고, 우리 `red_V` 1.242 V는 **그 다음 심화환원(P→LiP₇계) plateau의 하단**(=Zhu 표의 1.30 V 경계)이다. pymatgen row가 각 field의 저전압 끝을, Zhu 표가 고전압 끝을 라벨하기 때문. → **문헌 대조 시 우리 1.24를 "환원 onset"으로 쓰면 0.5 V 과소처럼 보인다 — Zhu-관례 환원전위는 1.717로 병기할 것.** (이 맵핑은 [Bai] note의 "리뷰 1.7 V ≠ 우리 1.24" 긴장을 기계적으로 해소; Schwietert 계열의 "실효 ~1.25 V"와 우리 1.24의 근접은 별개 정합.)
- **🔑 판정 ② (환원측 robust vs 산화측 민감 — 우리 해석)**: 환원 onset 경계(1.71↔1.717)가 DB 세대에 불변인 이유 — 경계 반응 Li₃PS₄+5Li→P+4Li₂S는 **양변 S가 전부 sulfide(S²⁻)** 라 MP2020 S-음이온 보정이 상쇄. 산화 onset은 S²⁻→polysulfide/S⁰로 **음이온 보정이 비상쇄** + LiS₄ 같은 신규 entry가 끼어들어 **DB 세대·entry set에 민감**(2.01→2.14→2.256). → **산화 onset 수치는 hull 버전·보정·제외 set 명시 없이 절대 이식 금지** (기존 규율의 근거 완성).
- **판정 ③ (OCV)**: Zhu의 Table S1 "LPSCl 조성 평형 = Li₃PS₄+Li₂S+LiCl (E_hull 83 meV/atom)" = 우리 `ocv_self_decomposition_rxn`과 동일 조합. Zhu는 이를 0으로 규약해 SE가 1.71–2.01 V 사이 "안정"으로 나타나고, 우리는 metastable 그대로 두어 같은 구간이 "Li-중성 분해"로 나타남 — **물리는 동일**(중성 조합의 안정 창 = intrinsic 창).

### 10c. cascade collapse 판정(window<0.05 V, 후기 TM 회피)의 Zhu-프레임 근거
- Zhu 설계원리 1(§9) = **"환원되기 쉬운 cation은 창을 좁히고, 전도성 산물(합금·저가 산화물)로 passivation까지 막는다"** → 우리 cascade에서 Fe₂O₃/CoO/MnO 도핑 시 window 0.004–0.039 V로 붕괴하고 산물이 금속성 계열인 것은 이 원리의 극단 사례 — **회피 판정이 원전 논리로 정당**.
- **단, 같은 원전이 미세 창 판정의 한계도 경고**: LLZO의 0.021 eV/atom·0.004 V 사례에서 "DFT 정확도·스킴 근사 이하 → inconclusive" 자인 → **우리 collapse 플래그는 '회피 필터'로만 쓰고, <0.05 V끼리의 미세 순위 비교에는 쓰지 말 것** (hull 오차 안).

## 11. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | E_D(φ) 곡선 (a 황화물 / b 산화물): 창 안 0, 밖 선형 하강; 0 V 황화물 −1~−2 eV/atom | 우리 cascade에 E_D(φ) 곡선 산출 추가하면 구동력 크기(kinetics 가늠자)까지 확보 — 현재 onset만 기록 |
| 2a | Li binary + SE 창 막대 (dashed=완전 delithiation) | "산물별 창" 시각화 원형 — 우리 sei_products gap 서열의 열역학 짝 |
| 2b | anode 계면 μ_Li/μ̃_Li⁺/μ̃_e⁻ 프로파일 (절연 interphase → μ_Li 강하) | **passivation 논리의 교과서 도식** — deck 인용 1순위 |
| 3a | 코팅 창 막대 + LiCoO₂ 3.9 V 라인 | 우리 코팅 서사([Cha]/[Sundar])의 원조 그림 문법 |
| 3b | cathode 쪽 μ_Li 프로파일 (코팅=인공 SEI) | 〃 |
| 4 | 통합: intrinsic 창 + interphase 확장 + 과전압 = nominal 창 | **"true vs 겉보기 창" 한 장 요약** — 우리 B① 프레임의 원전 도식 |
| S2 표 | 물질별 전 계단 (φ/Δn/상) | 우리 key_breakpoints와 1:1 대조 포맷 (10b) |

## 12. Post-processing ★
- **무엇**: grand-potential phase diagram → (i) 전위별 phase equilibria, (ii) plateau 표(SI S2·S3), (iii) E_D(φ) 곡선(Fig 1), (iv) 창 막대(Fig 2a·3a).
- **도구**: pymatgen (phase diagram·grand potential; ref 22) + VASP(MP 미등재 물질만) + MP DB.
- **수치화·기록**: 물질당 [환원전위, 환원산물 / 산화전위, 산화산물](Table 1) + 0 V/5 V E_D(Table 2·3) + 전 계단(SI). 우리 JSON 스키마(onset·rxn·key_breakpoints)와 사실상 동일 구조 — 우리가 E_D 열만 빠짐.

## 13. 적용 인사이트
1. **계보 문장 확보**: "우리 cascade의 grand-potential ESW는 Zhu/He/Mo 2015 (ACS AMI 7, 23685)의 μ_Li(φ) construction을 pymatgen `get_element_profile`로 구현한 직계 — 창 정의·분해산물 화학(Li₃P+Li₂S+LiCl / Li₃PS₄+S+LiCl)은 원전과 일치, onset 수치만 MP hull 세대(MP2020 S-보정·LiS₄ entry)로 +0.13~0.25 V 이동."
2. **라벨 규율 (신규)**: 문헌 대조 시 **Zhu-관례 환원전위 = 우리 `ocv_V`(1.717)**, 우리 `red_V`(1.242)는 심화환원 경계 — comparison·deck에서 혼용 금지 (10b 판정 ①).
3. **B① 서사 원전**: "thermo 창 좁음 + kinetic 과전압 + 전자절연 interphase passivation" 3단 논리를 인용할 땐 이 논문이 1차 출처 ([Kang] Fig 1a ref 49·[Banik]·Schwietert보다 앞).
4. **Cl-rich 4축의 2015 처방 원형**: "Li-halide 도핑 = σ+Li안정 동시 확보" 명시(§9 원리 3) + LiCl 산물의 전자절연 passivation — 우리 E축([Lu]/[Liu]/[Li25]) LiCl-SEI 서사의 시조.
5. **Nd/O passivation 원리 원전**: "산물이 전자절연이면 분해 정지" = 우리 sei_products.json gap 분류·Nolan Type 3([Kang])의 2015 원형 — 우리는 gap 수치로 정량화한 것.
6. **후속 아이디어**: (a) cascade에 **E_D(φ) 곡선/0 V·고전압 E_D 열 추가**(구동력 크기 = kinetics 가늠자; LLZO −0.021 vs LAGP −1.99 같은 대비가 도판트 간에도 가능), (b) 산화 onset의 **hull-세대 감도(2.01→2.14→2.256)를 오차막대처럼 병기**.

## 14. 인용 가능 문장 (deck/paper용)
- "Our grand-potential ESW pipeline is a direct implementation of the Zhu–He–Mo (2015) construction; it reproduces their Li₆PS₅Cl decomposition chemistry exactly (Li₃P+Li₂S+LiCl at 0 V; Li₃PS₄+S+LiCl at the anodic onset), with onsets shifted only by the Materials Project hull generation (2.01 → 2.14/2.256 V)."
- "The reduction-side boundary is database-robust (1.71 V in 2015 vs 1.717 V in our 2026 hull) because sulfide anion corrections cancel across the reaction, whereas the oxidation onset is correction-sensitive because S²⁻ leaves the sulfide oxidation state."
- "The narrow thermodynamic window of sulfide electrolytes (~0.3–0.6 V) is not a death sentence: as first formalized by Zhu et al., the experimentally relevant window is extended by sluggish decomposition kinetics and by electronically insulating decomposition interphases — which is precisely the axis our dopant screening targets."

## 15. 주의/한계 (over-claim 방지) — 비판적으로
- **0 K hull**: PV·엔트로피 무시(자인). 유한온도 안정화(무질서 엔트로피)는 E_hull→0 규약으로 우회했을 뿐 정량 아님 — **창을 넓히는 방향의 선택**이며, LPSCl 83 meV/atom(ordered-config 값; 현대 문헌은 ~20–30 meV/atom대, 예: [Rao] Cl₁.₅ 28)이 그대로면 창은 더 좁거나 소멸.
- **MP 2015 세대 의존**: onset 수치는 보정 스킴·entry 유무에 민감 — 우리 재계산이 실증(산화 +0.13~0.25 V). **이 논문의 창 수치를 현대 hull 수치와 섞어 인용 금지** (산물 화학·서열·논리 구조만 세대-불변).
- **passivation 판정이 정성적**: "전자절연"을 산물 상식으로 판정 — σ_e·gap·두께·성장 kinetics 계산 없음. interphase의 Li⁺ 전도도 refs 소환 수준. (우리 sei_products gap 분류·[Sundar]식 산물-전도도 스크린이 정량 후속.)
- **kinetic 과전압 >1 V는 metal–air OER 유추**(ref 37) — 황화물 고유 계산 아님.
- **계면 화학 혼합(전극과의 상호반응) 미포함** — 전극-SE pseudo-binary는 2016 후속(Zhu/He/Mo JMCA)에서; 여기선 SE 단독 + Li 저장고만.
- **LiPON = 결정 Li₂PO₂N 대표** (실물 amorphous·조성 범위), LLTO ordered 배열 — 대표성 한계.
- **space-charge/결함 미포함** (자인) — interphase 전자축적 시 passivation 꺼질 수 있음.
- **LLZO 0 V 판정 inconclusive** (0.021 eV/atom = 정확도 이하) — 미세 창·미세 구동력 판정 전반의 경고 (우리 collapse 규율에 반영, §10c).

## 16. 기법 용어 미니사전
- **grand potential (Φ = E − μ_Li·n_Li)**: Li를 주고받는 열린 계의 퍼텐셜. 전위 φ가 μ_Li를 정하고(eq 1), 최소 Φ 조합이 그 전위의 평형상.
- **Li grand potential phase diagram**: 위 Φ로 다시 그린 상도 — 전위축을 따라 조성의 평형상이 계단(plateau)으로 바뀜.
- **plateau / Δn_Li**: 한 평형상 조합이 안정한 전위 구간 / 그 조합으로 갈 때 조성이 흡수(+)·방출(−)하는 Li 수.
- **E_D(φ)**: 전위 φ에서의 분해 반응에너지(eq 2) — 창 안 0, 밖 음수(구동력).
- **intrinsic(true) vs nominal(kinetic) window**: hull이 주는 열역학 창 vs 과전압·passivation으로 넓어 보이는 실험 창.
- **passivation vs kinetic stabilization**: 전자절연 interphase가 μ_Li를 창 안으로 끌어와 **구동력 제거** vs 반응이 느려서 **못 갈 뿐 자발**(장기 열화).
- **MCI (mixed conducting interphase)**: 전자+이온 혼성 전도 interphase(Li–Ge 합금·Ti³⁺ 티타네이트) — μ_Li 강하 불가 → 연속 분해 (Janek 명명).
- **μ_Li = μ̃_Li⁺ + μ̃_e⁻**: 중성 Li 화학퍼텐셜의 전기화학 분해 — passivation 도식(Fig 2b·3b)의 기초.
- **HOMO–LUMO 창 (Goodenough)**: 전자 준위 기반 창 추정 — 본 논문의 중성-Li 평형 스킴과 상보(우리 "VBM≠onset" 규율의 먼 조상).
