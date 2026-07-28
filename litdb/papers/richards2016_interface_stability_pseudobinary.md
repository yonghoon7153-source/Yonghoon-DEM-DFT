# Interface Stability in Solid-State Batteries — Richards/Miara/Wang/Kim/Ceder (Chem. Mater. 2016)

> slug `richards2016_interface_stability_pseudobinary` · DOI `10.1021/acs.chemmater.5b04082` · type `DFT (grand-potential + pseudo-binary 계면 열역학; 실험 0)` · PDF 본문 `b9313d89-39._Interface_Stability_in_SolidState_Batteries.pdf` + SI 19 pp `66aff194-39._Sup_Interface_Stability_in_SolidState_Batteries.pdf` (인박스 파일번호 39) · digested `2026-07-28` · status ✅
> elements: Li, P, S, Cl, O, N, F, Br, I, H, B, Ge, Sn, Ti, Zr, La, Nb, Al, Mg, Zn, Y, In, Cd, Mn, Co, Ni, Fe, V
> methods: DFT, ESW
> **저자**: William D. Richards,† Lincoln J. Miara,‡ Yan Wang,† Jae Chul Kim,† **Gerbrand Ceder***,†,¶,§ (†MIT · ‡Samsung Advanced Institute of Technology–USA · ¶UC Berkeley · §LBNL) · *Chem. Mater.* 2016, 28, 266−273 · Received 2015-10-20 / Published 2015-12-07
> 첫 페이지 실물 대조 완료 — 과제 메모의 예상 정체(Richards, Chem. Mater. 28, 266, DOI 10.1021/acs.chemmater.5b04082)와 **일치**.

---

## 0. 이 digest를 읽는 법 (우리 캠페인에서의 위치)
**전극|전해질 계면 반응성의 pseudo-binary(혼합 분율 x 최소화) 방법 원전(原典)이다.** 계보:
- **[Zhu15]** (`zhu2015_esw_grand_potential_origin.md`, ACS AMI 2015-10) = **SE 단독** + Li 저장고 창 → 우리 `esw_grand_potential.py`/`oxidation_stability.json`의 원전.
- **이 논문** (Chem. Mater. 2015-12 투고/출판) = 거기에 **전극과의 화학 혼합**을 얹은 형식화(eq 2–5) → 우리 `GrandPotentialInterfacialReactivity`(interface_reactivity, `nd2o3_interface_reactivity` 등)의 원전. 두 논문은 두 달 간격의 상보 쌍 — Zhu가 "SE 혼자 몇 V까지 버티나", Richards가 "전극과 *섞이면* 무엇이 되나".
- **Xiao 2019** (Nat. Rev. Mater. 리뷰) = 이 방법 가족의 후속 정리 — 동시 큐레이터 digest 진행 중, 완성되면 교차참조(여기서는 방법 관계만 언급, 내용 선점 안 함).
- **우리 MLIP 차기 캠페인 ①**(`kb/projects/mlip_next_campaigns_2026_07.md` — UMA로 Li|도핑SE 계면 MD)의 **열역학 짝**: 이 논문·[Zhu15]의 분해 산물 목록이 곧 우리 MD가 관찰해야 할 **기대-산물 리스트**가 된다 (§13).

## 1. 한 줄 요약
계면 반응 에너지를 **두 상의 혼합 분율 x에 대해 최소화**하는 pseudo-binary 열역학(닫힌 eq 2 / Li-개방 eq 4)을 정의하고, 전해질 ~30종 × 양극 7종 전 조합의 분해 산물·구동력을 표로 제공 — **thiophosphate는 창(~1.7–2.1 V, figure-read)이 좁을 뿐 아니라 고전압 산화물 양극과 혼합 반응(PO₄·전이금속 황화물 형성)의 구동력이 특히 커서** 산화물 코팅이 필수이고, 반대로 여러 전해질(Li₃PS₄·LiPON 등)은 Li 금속에 불안정해도 **전자절연·Li-전도성 산물(Li₂S/Li₂O+Li₃P)로 자가-passivation**되므로 실효 계면이 성립함을 보였다 (+ 미시도 셀 조합 제안).

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 유형 | 순수 계산 (DFT + 실험 열화학 하이브리드 hull; 자체 실험 0) |
| 대상 전해질 | **황화물 5**: Li₂S, Li₃PS₄, Li₁₀GeP₂S₁₂(LGPS), Li₄SnS₄, **Li₆PS₅Cl(=우리 comp1 조성)** / **산화물 12**: Li₂O, LiAlO₂, Li₄Ti₅O₁₂, Li₂ZrO₃, Li₇La₃Zr₂O₁₂(LLZO), Li₄GeO₄, LiNbO₃, LiPON(Li₃.₂PO₃.₈N₀.₂≈Li₁₆P₅O₁₉N), Li₃PO₄, LiGe₂(PO₄)₃, LiTi₂(PO₄)₃, Li₃OCl / **질화물 3**: Li₃N, Li₃BN₂, Li₄NCl / **수소화물 2**: LiH, LiBH₄ / **염화물 5**: LiCl, Li₂MgCl₄, Li₂ZnCl₄, LiAlCl₄, Li₂CdCl₄ / **브로마이드 6**: LiBr, Li₂MgBr₄, LiAlBr₄, Li₂ZnBr₄, Li₂MnBr₄, Li₃InBr₆ / **불화물 4**: LiF, LiYF₄, Li₃AlF₆, Li₂ZrF₆ (+ Fig 1c Li binary: Li₃N·Li₃P·LiH·Li₂S·LiI·Li₂O·LiBr·LiCl·LiF) |
| 대상 전극 | LiCoO₂, LiFePO₄, LiMnO₂, LiNiO₂, LiTiS₂, LiVS₂, Li₂S (각 조합을 "해당 양극 평균전압의 μ_Li"에서 평가) |
| 핵심 질문 | 계면 저항이 율속인데 실험으로 계면 접근이 어렵다 → 벌크 열역학(전기화학+화학 구동력 포함)이 계면 안정성의 좋은 proxy인가? 어떤 조합이 passivation으로 살아남나? |
| 배경 수치(인용) | LGPS 12 mS/cm·Li₇P₃S₁₁ 27 mS/cm(글라스세라믹)·NASICON/garnet ~1 mS/cm — thiophosphate 고전도+기계적 접촉 우수가 동기 |

## 3. 핵심 수치 (이 논문이 명시적으로 준 것)
| 항목 | 값 | 출처 |
|---|---|---|
| 계면(표면)에너지 무시 정당화 | Δγ 0.5 J/m², 원자층 두께 산물 가정 시 **~100 meV/atom 상한** ≪ 벌크 구동력 | Methods |
| 전위 스캔 범위 | 0–7 V vs Li/Li⁺ (μ_Li 0 ~ −7 eV vs Li metal) | Methods |
| ZnCl₂+Li₂S 예제 구동력 | **0.27 eV/atom** (완전 반응 ZnCl₂+Li₂S→2LiCl+ZnS, x=0.5 최심점) | Fig 3 |
| LiPON(amorphous 대표) 산화 | **>1.2 V**에서 → Li₃PO₄ + Li₂PO₂N | 본문 |
| 결정질 Li₂PO₂N 산화 | **>2.75 V**에서 → Li₄P₂O₇ (ref 24 메커니즘과 정합) | 본문 |
| thiophosphate 예측 안정창 | **"2–2.5 V 사이만"** (본문 서술; Fig 2 막대 figure-read ~1.7–2.1 V) | 본문/Fig 2 |
| μ_Li 앵커 | anode ≈ 0 eV/atom(vs Li), layered oxide cathode ≈ **−4 eV/atom** | 본문 |
| 핵생성 장벽 | ΔG* = 16πγ³/(3ΔG²)·S(θ), S(θ)<1 — 이온성 고체 간 incoherent γ 유사 → **kinetic 안정화엔 작은 ΔG 필요** | Discussion |
| 조합별 ΔΦ 수치 | **표 없음 — Fig 4·S1–S7 막대그래프만** (figure-read: thiophosphate|layered oxide ~−0.5(추출만)~−1.1(mixing), Li₂S|LiCoO₂ ~−2.9, 산화물 전해질 0~−0.3, LiYF₄ ≈ 0 eV/atom, ±0.05 판독오차) | Fig 4, S1–S7 |

## 4. 방법 형식화 ★★ (최우선 — 수식 그대로)

### 4a. DFT/데이터 셋업
- **code**: VASP, **PAW**, **GGA**(functional 명시상 PBE 계열; vdW 없음). **cutoff 520 eV**, **k-grid ≥ 500/n_atoms**.
- **GGA/GGA+U 혼합**: Jain et al. 스킴(ref 36)으로 절연체/금속 혼재 반응 처리 (+U 관례는 Anisimov/Dudarev refs 37–38).
- **실험 열화학 하이브리드 (이 논문의 특색)**: 전해질 형성에너지를 **NIST-JANAF·Kubaschewski 실험표의 "nearest phases"(조성을 담는 Gibbs triangle = low-energy facet의 꼭짓점 상)로부터의 DFT 반응에너지**로 계산 — 산화상태 불변 반응의 DFT 오차 상쇄(ref 39 Hautier) 활용. 예: LiYF₄ = E_exp(LiF)+E_exp(YF₃)+ΔE_DFT(LiF+YF₃→LiYF₄); Li₃PS₄는 P₂S₅ 실험값이 없어 **3Li₂S+2P+5S→2Li₃PS₄**의 DFT 반응에너지+Li₂S 실험값; LiAlO₂는 실험 형성에너지 직접 사용. "실험 데이터를 최대한 쓰고 DFT로 보강" = [Zhu15]의 순-MP 방식과 구별되는 지점.
- **DB**: ICSD(ref 26) + data-mined 화학치환 구조(ref 27) — "Materials Project로 온라인 공개"(ref 28). grand-potential phase diagram 구축은 **pymatgen**(ref 30).
- **metastable SE 규약**: 0 K에서 hull 위인 기지 전해질(예: LGPS)은 **E_above_hull→0으로 놓고**(인접 상 대비 형성에너지 0) 평가 — 0 K→상온 자유에너지 변화 근사. [Zhu15]와 동일 규약.
- **무질서/AIMD/NEB/COHP 등**: 없음 (순수 hull 열역학; 배열 샘플링 언급도 없음 — [Zhu15]의 50–60배열 언급보다도 간략).

### 4b. 전해질 단독 창 (eq 1) — [Zhu15]와 동일 구성
```
Φ[c, μ_Li] = E[c] − n_Li[c]·μ_Li                    (eq 1)
```
- 전위 0–7 V ⇔ μ_Li 0~−7 eV. 각 μ_Li에서 **Φ의 조성-공간 convex hull**을 취해 상평형 결정. 전해질이 hull에 남는 μ_Li 구간 = 안정창.

### 4c. 닫힌(chemical) pseudo-binary — **eq 2, 이 논문의 핵심 신규**
```
ΔE[cₐ, c_b] = min_{x∈[0,1]} { E_pd[x·cₐ + (1−x)·c_b] − x·E[cₐ] − (1−x)·E[c_b] }   (eq 2)
```
- 두 상 a·b를 분율 x로 섞은 **모든 유효 조성** x·cₐ+(1−x)·c_b에 대해, 그 조성의 phase-diagram 바닥상 조합 에너지 E_pd와 원료 에너지 차 = 반응에너지. **x를 [0,1]에서 최소화** → "가장 구동력 큰 혼합 비율"의 반응을 찾는다. (x=0/1 끝점에서 ΔE=0이므로 최소점은 내부; Fig 3b가 V-자 곡선.)
- 용도: **전기화학 구동력 없는 순수 화학 반응성** — 전해질|코팅, 전해질|전해질(이중 전해질 쌍 검증), 합성/공정 접촉.

### 4d. 열린(전위 하) 버전 — eq 3·4
```
Φ_pd[c, μ_Li] = min_{n_Li} { E_pd[c + n_Li] − n_Li·μ_Li }                        (eq 3)
ΔΦ[c_cathode, c_elec, μ_Li] = min_{x∈[0,1]} { Φ_pd[x·c_cathode + (1−x)·c_elec, μ_Li]
                              − x·Φ[c_cathode, μ_Li] − (1−x)·Φ[c_elec, μ_Li] }   (eq 4)
```
- eq 2의 E·E_pd를 grand-potential Φ·Φ_pd로 치환 — 계면 영역이 **외부 Li 저장고(전지 회로)와 평형**하며 반응. μ_Li는 **"계산된 양극 평균전압"으로 고정**(충방전 중 DOD에 따라 변하지만 반응에너지 영향 작다고 명시). 에너지는 **비-Li 원자수로 정규화**.
- 용도: **작동 중(cycling) 양극|전해질 계면** — 배터리 조건의 정본.

### 4e. 분리 진단 — eq 5 (no-mixing)
```
ΔΦ_no-mixing[c_elec, μ_Li] = Φ_pd[c_elec, μ_Li] − Φ[c_elec, μ_Li]               (eq 5)
```
- x=0 강제 = **전해질이 그 전위에서 Li 추출/삽입만으로 겪는 분해**(전극과 안 섞임). Fig 2 창과의 거리와 상관. 정의상 **|ΔΦ| ≥ |ΔΦ_no-mixing|** 보장.
- **진단 논리**: ΔΦ ≈ ΔΦ_no-mixing이면 구동력의 주원인 = 전위(Li 추출/삽입), ΔΦ ≫ ΔΦ_no-mixing이면 = **전극 성분과의 화학 혼합**. Fig 4·S1–S7이 두 값을 나란히 막대로 표시("at cathode μ_Li" vs "with mixing").

### 4f. 어떤 조합에 어떤 식을 쓰나 (정리)
| 상황 | 식 | SI 표의 열 |
|---|---|---|
| 전해질 단독 창·한계 반응 | eq 1 | Table S1 (anodic/cathodic) |
| 전해질 분해 @ 양극 전위 (혼합 없이) | eq 5 | Tables S2–S9 "reaction at cathode voltage" 열 |
| 양극\|전해질 작동 계면 (정본) | eq 4 | Tables S2–S9 "reaction with mixing" 열 |
| 코팅·이중 전해질 등 **비-전기화학 접촉** | eq 2 | (본문 Fig 3 예제; 표는 없음) |

### 4g. 계면에너지 무시 정당화
원자층 두께 계면 산물 + Δγ 0.5 J/m² 상계 → **~100 meV/atom** — 관련 계(벌크 구동력 수백 meV~수 eV/atom)에 비해 작다고 명시. (미세 |ΔΦ|<0.1 eV/atom 조합의 판정엔 이 상한이 곧 오차막대 — §16.)

## 5. 결과 I — 전해질 단독 창 (Fig 1c·2, Table S1)
- **음이온이 anodic(산화) 한계를 지배**: 할라이드 음이온이 고전위에 가장 안정, 황화물·질화물·인화물은 낮음. Fig 2는 **음이온 전기음성도 증가 → anodic 안정성 증가** 트렌드(N<S<…<F). Fig 1c binary 서열(figure-read): Li₃N(최협, ~0.6 V까지) < Li₃P < LiH < Li₂S < LiI < Li₂O < LiBr < LiCl < **LiF(최광, ~6 V+)**. binary는 음이온 완전환원 상태라 **0 V까지 전부 안정**(추가 환원 불가) — passivation 논리의 뿌리 ([Zhu15] Fig 2a와 동일 물리).
- **2-step 논리 (mixed-anion 전해질의 anodic 한계)**: 분해가 ① LiₙX binary 조합으로의 분해 → ② 그 binary의 해리(Li 추출) 순서라, anodic 한계 = **"가장 덜 안정한 관련 binary"의 한계 + 혼합(mixing) 에너지만큼의 확장**. 원문 예: **"the anodic stability of Li₆PS₅Cl is determined primarily by the stability of Li₂S"** — **argyrodite 산화 한계 = S²⁻(Li₂S) 지배, Cl 무관**을 2016에 명문화 = 우리 axis ① S-limited·[Banik] S-pin의 원조 문장.
- **polyanion 예외**: 인산염·LiBH₄처럼 강결합 폴리음이온은 Li 추출에 폴리음이온 해리가 동반돼 **창이 크게 넓어짐**.
- **양이온 산화 예외**: 다른 성분이 산화되며 Li을 잃는 경우 — 예: **Li₂MnBr₄의 Mn²⁺ 산화** (창 축소). → 우리 cascade "late-TM 회피"의 산화측 원형.
- **Table S1 — 전해질별 한계 반응 (정독 발췌; 균형 검산 완료)**:
  - **Li₆PS₅Cl anodic**: `Li₆PS₅Cl → S + Li₃PS₄ + LiCl` (2 Li 추출) — **우리 GG-set onset 2.256 V 반응과 산물·Δn 동일**.
  - **Li₆PS₅Cl cathodic**: `2 Li₆PS₅Cl + 2 Li → Li₄P₂S₆ + 4 Li₂S + 2 LiCl` — 첫 환원이 **P⁵⁺→P⁴⁺(P–P 결합 Li₄P₂S₆)** 단계. ([Zhu15]의 1.71 V 첫 환원 P⁰+Li₂S+LiCl과 다름 — hull entry 차이, §12b.)
  - Li₃PS₄: anodic `2 Li₃PS₄ → Li₄P₂S₆ + 2 S` / cathodic `2 Li₃PS₄ + 2 Li → Li₄P₂S₆ + 2 Li₂S` — **산화·환원 양쪽 첫 단계가 Li₄P₂S₆** (이 hull의 특징).
  - LGPS: anodic `Li₁₀GeP₂S₁₂ → Li₂GeS₃ + 2 Li₃PS₄ + S` / cathodic `→ Li₄GeS₄ + Li₄P₂S₆ + 2 Li₂S`.
  - Li₄SnS₄: anodic `→ S + Li₂SnS₃` / cathodic `→ 3 Li₂S + SnS`.
  - LiBH₄: anodic `6 LiBH₄ → Li₂B₆H₁₂(인쇄 표기; Tables S2/S4에는 Li(BH)₆=closo-형 LiB₆H₆로 등가 표기) + 9 H₂` / cathodic `6 LiBH₄ → (동일 closo상) + 18 LiH` — H 균형은 closo LiB₆H₆ 해석이 맞음(표기 불일치 캐비앗).
  - LiPON(Li₁₆P₅O₁₉N): anodic `4 Li₁₆P₅O₁₉N → N₂ + 2 Li₂PO₂N + 18 Li₃PO₄` / cathodic `Li₁₆P₅O₁₉N → Li₂PO₂N + 17 Li₂O(?) + 4 Li₃P` (렌더 상 계수 일부 저신뢰 — 산물 종만 인용: Li₂PO₂N·Li₂O·Li₃P).
  - Li₃PO₄: anodic `4 Li₃PO₄ → 2 Li₄P₂O₇ + O₂` / cathodic `Li₃PO₄ → 4 Li₂O + Li₃P`.
  - LLZO: anodic `4 Li₇La₃Zr₂O₁₂ → 4 Li₆Zr₂O₇ + O₂ + 6 La₂O₃` / cathodic `4 Li₇La₃Zr₂O₁₂ + 12 Li → 3 Zr + 6 La₂O₃ + 5 Li₈ZrO₆` (Zr⁰ 환원).
  - 할라이드류 anodic = 원소 할로겐/할로겐-rich 상 방출(예: `Li₂MgCl₄ → MgCl₂ + Cl₂`, `Li₂MgBr₄ → MgBr₂ + 2 Br`), cathodic = **비-Li 양이온 금속 환원**(예: `Li₂MgCl₄ → Mg + 4 LiCl`, `LiAlCl₄ → Al + 4 LiCl`, `Li₂CdCl₄ → Cd + 4 LiCl`, `Li₃InBr₆ → In + 6 LiBr`, `LiYF₄ → 4 LiF + Y`) — "제2 양이온 추가 = 저전압 음극에 대한 환원 불안정"의 표 근거.
- **황화물 창은 좁다**: Fig 2에서 Li₃PS₄·LGPS·Li₄SnS₄·Li₆PS₅Cl 모두 ~1.7–2.1 V 좁은 막대(figure-read; 본문 서술 "2–2.5 V"). 동시대 [Zhu15] 표값 Li₆PS₅Cl 1.71–2.01 V와 정합(단 Richards는 수치표 미제공 — 정량 인용은 [Zhu15]로).

## 6. 결과 II — Li 금속 자가-passivation (본문 + Table S1)
- **Li₃PS₄·Li₃PO₄·LiPON은 계산상 Li 금속에 불안정**하지만 실험적으로 안정 계면 형성 — Table S1이 보이듯 이 계면엔 **Li₂S/Li₂O + Li₃P 층**이 형성되는데, **Li₃P는 알려진 Li-이온 전도체**(ref 41 Nazri)라 분해를 passivate하면서 Li 전도는 유지. LiPON|Li의 이런 산물 형성은 in-situ XPS 실험(ref 42 Schwöbel 2015)으로 관찰됨.
- LiPON 전압 단계: amorphous(Li₃.₂PO₃.₈N₀.₂) **>1.2 V → Li₃PO₄ + Li₂PO₂N**; 결정질 Li₂PO₂N은 더 넓은 창, **>2.75 V → Li₄P₂O₇** (ref 24 제안 메커니즘과 일치).
- **"전기화학적으로 안정 ≠ 계면 성립"의 역도 성립**: 창이 전극 전위까지 안 닿아도 **산물이 전자절연+Li-전도**면 계면은 작동 — 이 논문의 실용 결론이자 [Zhu15] §6 passivation 논리의 적용판. (전자절연성 판정 자체는 정성적 — §16.)

## 7. 결과 III — pseudo-binary 예제와 양극 조합 스크리닝 (Fig 3·4)
- **Fig 3 (ZnCl₂|Li₂S 교육 예제)**: Li–Zn–S–Cl 사원계 상도에서 ZnCl₂–Li₂S 반응 벡터가 hull 아래 LiCl–ZnS tieline과 교차 → 완전 반응 `ZnCl₂ + Li₂S → 2 LiCl + ZnS`가 x=0.5에서 **최대 구동력 0.27 eV/atom**. 역으로 **LiCl|ZnS 계면은 tieline 위 = 열역학 안정** — "상도의 tieline 존재 = 계면 안정"의 그림 문법.
- **Fig 4 (양극 7종 × 대표 전해질 12종, μ_Li = 양극 평균전압)**: 값은 막대만(±0.05 figure-read) —
  - **thiophosphate가 최악**: PS₄기가 산화물 양극의 낮은 μ_Li + 산소 화학퍼텐셜과 이중으로 반응 → **PO₄(인산염)·전이금속 황화물 형성**. 최대는 layered **LiCoO₂·LiNiO₂** 조합(고전압+산소 제공), **LiFePO₄에도 불안정**(황화물 한정).
  - **산화물 전해질은 훨씬 안정**(0~−0.3 eV/atom대). 산화물 양극 전위서 "mixing 없이 이미 낮은 반응에너지" = redox 없이 조성 혼합만.
  - **Li₂S|LiCoO₂ ~−2.9 eV/atom**(Fig S3, figure-read) = 완전 탈리튬화(Li₂S→S) 구동력 — Li₂S 양극은 고전압 짝 금지.
- **실험 정합**: (i) 사이클 수명 ↔ 계산 분해에너지 크기 상관(시도된 계들); (ii) LiTiS₂|Li₂S–P₂S₅ 셀(ref 46, 코팅 없이 50+ 사이클) = 계산상 소구동력(양극 전압이 낮아 Li₃PS₄에 Li 삽입 구동력 미소); (iii) LiPON 고전압 = Li₃PO₄ passivation; (iv) LiCoO₂/Li₂S–P₂S₅ 계면의 **P·Co 상호수송 TEM 관찰**(ref 49 Sakuda) = "혼합 반응" 예측 그대로; (v) LiBH₄|LiCoO₂ 계면저항 지속 증가(ref 59) = 대구동력 예측 그대로.
- **신규 셀 제안** (미시도): ① **Li₃PS₄(또는 고전도 Li₇P₃S₁₁)|LiVS₂** — Fig 4 최소 분해에너지, LiTiS₂ 셀보다 전압·안정성 우위 예측; ② **LiBH₄|LiTiS₂** — LiCoO₂에는 불안정하지만 저전압 LiTiS₂에는 안정 예측.

## 8. 결과 IV — 전 조합 산물 표 (SI Tables S1–S9 정독 다이제스트)

### 8a. 황화물 × 양극 (Table S5 — **우리 재료 포함, 전 행**)
| 전해질\|양극 | @양극전위 (eq 5 산물) | mixing (eq 4 산물) |
|---|---|---|
| Li₂S\|LiCoO₂·LiFePO₄·LiMnO₂·LiNiO₂ | Li₂S → S | 동일 (혼합 이득 없음 = 순수 전위 구동) |
| Li₂S\|LiTiS₂ / LiVS₂ | none | LiTiS₂+Li₂S→Li₂TiS₃ / LiVS₂+2Li₂S→Li₃VS₄ |
| Li₃PS₄\|LiCoO₂ | 2 Li₃PS₄ → P₂S₇ + S | **3 LiCoO₂ + 2 Li₃PS₄ → Co(PO₃)₂ + 2 CoS₂ + 4 S** |
| Li₃PS₄\|LiFePO₄ | 2 Li₃PS₄ → P₂S₇ + S | 동일(자체 분해가 최심 = mixing 이득 없음) |
| Li₃PS₄\|LiMnO₂ | 〃 | 14 LiMnO₂ + 8 Li₃PS₄ → 3 Mn₂S₃ + 4 Mn₂P₂O₇ + 23 S |
| Li₃PS₄\|LiNiO₂ | 〃 | 117 LiNiO₂ + 44 Li₃PS₄ → 22 Li₄P₂O₇ + 39 Ni₃S₄ + 20 Li₂SO₄ |
| Li₃PS₄\|LiTiS₂ | Li₃PS₄ + 5 Li → P + 4 Li₂S (저전압이라 **환원**) | Li₃PS₄ → 4 Li₂S + P |
| **Li₃PS₄\|LiVS₂ / Li₂S** | **none** | **none** ← 제안 셀의 근거 |
| LGPS\|LiCoO₂ | LGPS → GeS₂ + P₂S₇ + 3 S | **7 LiCoO₂ + 2 LGPS → 2 GeP₂O₇ + 10 S + 7 CoS₂** |
| LGPS\|LiFePO₄ | LGPS → 3 S + P₂S₇ + GeS₂ | 동일 |
| LGPS\|LiMnO₂ | 〃 | 14 LiMnO₂ + 4 LGPS → 4 Mn₂P₂O₇ + 31 S + 4 GeS₂ + 3 Mn₂S₃ |
| LGPS\|LiNiO₂ | 〃 | 171 LiNiO₂ + 22 LGPS → 22 Li₄P₂O₇ + 22 GeO₂ + 36 Li₂SO₄ + 57 Ni₃S₄ |
| LGPS\|LiTiS₂ | LGPS → 2 P + 8 Li₂S + Li₄GeS₄ (환원) | 8 LiTiS₂ + LGPS → 2 P + Li₄GeS₄ + 8 Li₂TiS₃ |
| LGPS\|LiVS₂ / Li₂S | none | none |
| Li₄SnS₄\|LiCoO₂·LiFePO₄·LiMnO₂ | Li₄SnS₄ → SnS₂ + 2 S | 동일 |
| Li₄SnS₄\|LiNiO₂ | 〃 | 27 LiNiO₂ + 11 Li₄SnS₄ → 11 SnO₂ + 9 Ni₃S₄ + 8 Li₂SO₄ |
| Li₄SnS₄\|LiTiS₂ | → 3 Li₂S + SnS (환원) | 3 LiTiS₂ + Li₄SnS₄ → 3 Li₂TiS₃ + SnS |
| Li₄SnS₄\|LiVS₂ | none | LiVS₂ + 2 Li₄SnS₄ → 2 Li₂SnS₃ + Li₃VS₄ |
| Li₄SnS₄\|Li₂S | none | none |
| **Li₆PS₅Cl\|LiCoO₂** | 2 Li₆PS₅Cl → **2 SCl + P₂S₇ + S** (완전 탈Li; S–Cl 상!) | **11 LiCoO₂ + 8 Li₆PS₅Cl → 8 CoSCl + 30 S + 2 CoP₄O₁₁ + CoS₂** |
| **Li₆PS₅Cl\|LiFePO₄** | 2 Li₆PS₅Cl → 3 S + P₂S₇ + 2 LiCl | 동일(자체 분해) |
| **Li₆PS₅Cl\|LiMnO₂** | 〃 | 2 LiMnO₂ + Li₆PS₅Cl → Mn₂PO₄Cl(인쇄 Mn₂PClO₄) + 5 S |
| **Li₆PS₅Cl\|LiNiO₂** | 〃 | 21 LiNiO₂ + 12 Li₆PS₅Cl → 40 S + 6 Li₄P₂O₇ + 5 Ni₃S₄ + 6 NiCl₂ |
| **Li₆PS₅Cl\|LiTiS₂** | Li₆PS₅Cl + 5 Li → 5 Li₂S + P + LiCl (환원) | 5 LiTiS₂ + Li₆PS₅Cl → LiCl + 5 Li₂TiS₃ + P |
| **Li₆PS₅Cl\|LiVS₂** | none | LiVS₂ + 2 Li₆PS₅Cl → 2 LiCl + 2 Li₃PS₄ + Li₃VS₄ |
| **Li₆PS₅Cl\|Li₂S** | **none** | **none** |
- 🔑 argyrodite 독법: (i) LiCoO₂ 전위(≈3.9 V)에선 **LiCl마저 소모돼 S–Cl 화학(SCl·CoSCl)으로 감** — 우리 staircase의 3.326 V SCl 단계와 같은 화학(§12b); (ii) LiFePO₄~LiNiO₂ 대부분에서 eq5 산물 = `3 S + P₂S₇ + 2 LiCl` = **[Zuo]/[Kang25] 산화분해(폴리설파이드/P₂Sₓ/LiCl) 화학**; (iii) 저전압 황화물 양극(LiTiS₂)과는 거꾸로 **환원**당해 Li₂S+P+LiCl; (iv) **Li₂S 양극과는 완전 호환**.

### 8b. LiPON·산화물 하이라이트 (Tables S2·S6)
- **Li₃PO₄: 7개 양극 전부 none/none** — 표 전체에서 유일하게 LiF와 함께 완전 불활성. "LiPON 계열의 고전압 실효성 = Li₃PO₄ passivation"의 표 근거.
- LiPON(Li₁₆P₅O₁₉N): 모든 양극 전위에서 자체 산화(N₂ 또는 NO₂ 방출 + Li₃PO₄/Li₄P₂O₇/Li₂PO₂N). mixing: LiCoO₂ → LiCoPO₄+LiNO₃+Li₄P₂O₇; LiNiO₂ → 5 Li₃PO₄+4 NiO+LiNO₃; **LiTiS₂ → 9 Li₃PO₄ + Li₂PO₂N + TiN + 2 Li₂S**(질화물 형성).
- **LiNbO₃**: 전 양극 @V none; mixing도 **LiCoO₂·Li₂S와는 none**(왜 LNO가 LCO 코팅의 표준인지) — 단 **LiNiO₂와는 반응**(LiNiO₂+LiNbO₃→Li₃NbO₄+NiO), LiFePO₄/LiMnO₂/LiTiS₂/LiVS₂와도 반응. → **고-Ni 양극에선 LNO도 화학적으론 무결하지 않다**는 표 증거 (우리 NCM 문맥 주의).
- LLZO: @LiCoO₂ 전위서 자체 산화(La₂Zr₂O₇+La₂O₃+O₂/Li₂O₂ 계열; Table S2·S6 인쇄가 등가 반응을 달리 표기). 황화물 양극(LiTiS₂·LiVS₂·Li₂S)과는 @V none이지만 **mixing으론 반응**(ZrO₂+La-옥시설파이드(La₂SO₂ 표기)+Li₃VO₄/Li₂SO₄류) — "산화물\|황화물 맞대면도 화학적으론 반응"의 근거.
- Li₂O: 고전압 양극 전위서 → Li₂O₂(peroxide)/O₂; LiAlO₂ @LiCoO₂ → LiAl₅O₈+O₂; Li₄Ti₅O₁₂·Li₂ZrO₃·Li₄GeO₄·LiGe₂(PO₄)₃·LiTi₂(PO₄)₃·Li₃OCl 각 행 존재(생략; 필요 시 SI p11–13).

### 8c. 할라이드/불화물 (Tables S7–S9)
- **패턴**: @양극전위 거의 전부 none(광창) ↔ **mixing은 광범위 반응** — 즉 이 물질군의 리스크는 전기화학이 아니라 **화학 혼합**.
- 염화물: Li₂MgCl₄ — **7개 양극 전부 @V none, 7개 전부 mixing 반응**(LiCoO₂→Mg(CoO₂)₂+LiCoCl₄+LiClO₃류; LiTiS₂→Ti₂S₃+4LiCl+MgS; **Li₂S→4LiCl+MgS**). LiAlCl₄·Li₂ZnCl₄·Li₂CdCl₄ 유사(Cd/Zn은 LiTiS₂ 전위서 **금속으로 환원**: Li₂CdCl₄→Cd+4LiCl).
- 브로마이드: Li₂MnBr₄ @LiCoO₂ 전위 → MnBr₄(Mn 산화) = **양이온 산화 예외의 표 실현**; Li₃InBr₆ @LiTiS₂ → In⁰+6LiBr.
- **불화물 = 최우수**: **LiF none/none 전부**; LiYF₄는 LiNiO₂ mixing(→Y₂O₃+NiO+8LiF) 하나만; Li₃AlF₆·Li₂ZrF₆도 소수 조합만 반응(산물이 대개 LiF+산화물 = 그 자체 passivating).

### 8d. "전기화학적으로 안정해도 화학적으로 반응" 클래스 (@V none & mixing≠none) — **코팅 논리의 근거**
Li₂MgCl₄·LiAlCl₄(전 양극), LiNbO₃(LiFePO₄/LiMnO₂/LiNiO₂/LiTiS₂/LiVS₂), LLZO(LiTiS₂/LiVS₂/Li₂S), LiAlO₂(LiFePO₄/LiMnO₂/LiTiS₂), Li₄Ti₅O₁₂(LiFePO₄/LiMnO₂/LiNiO₂), Li₂ZrO₃(LiFePO₄/LiMnO₂/LiTiS₂/LiVS₂/Li₂S), LiGe₂(PO₄)₃/LiTi₂(PO₄)₃(산화물 양극들), LiYF₄(LiNiO₂), Li₃AlF₆(LiCoO₂/LiMnO₂/LiNiO₂/Li₂S), Li₂ZrF₆(전 양극 mixing), Li₂O(LiTiS₂/LiVS₂/Li₂S) 등.
→ **전압 창(eq 1/5)만 보면 "안정"으로 오판** — 계면 판정은 반드시 eq 4(개방)·eq 2(폐쇄) 혼합까지. 우리 [Cha] dual-compatibility(LZC만 NCM·LPSCl 양쪽 무반응)의 열역학 문법이 정확히 이것.

### 8e. 완전 불활성(전 조합 none/none) 클래스
**Li₃PO₄, LiF** (7×2 전부 none) — "이상적 코팅"의 표 정의. (LiYF₄ 준하는 수준.)

## 9. Discussion — 메커니즘·설계 논리 (본문 §Discussion 정독)
1. **kinetics와의 연결 (정성)**: 계면 반응은 확산 or 핵생성 율속. 얇은 계면층은 확산 거리 짧아 확산 시정수 작음 → **핵생성 장벽이 관건**: ΔG*=16πγ³/(3ΔG²)·S(θ). 이온성 고체 간 incoherent γ가 서로 비슷 → **kinetic 안정화가 가능하려면 ΔG(반응에너지)가 작아야** — "작은 계산 반응에너지 = 안정 계면 기대"의 이론 근거(열역학 스크리닝의 kinetics 정당화).
2. **thiophosphate|고전압 산화물 양극의 2-경로 열화**: ① 양극 전위의 μ_Li만으로 **Li-추출 → passivating하지만 고저항인 황(S) 층**; ② 산화물 양극과의 **혼합 → Li₃PO₄류 인산염**(phosphate 안정성이 구동) — LiCoO₂/Li₂S–P₂S₅ 계면의 P·Co 수송 관찰(ref 49)과 정합.
3. **space-charge 가설 반박(부분)**: Li 편석 space-charge는 오히려 캐리어 증가로 전도 ↑ 방향 — 계면 저항의 주범은 **S²⁻ 산화를 포함한 전해질 완전 분해(blocking layer)**가 산화물 양극 μ_Li에서 더 개연적.
4. **CV 광창(≤10 V 보고) 아티팩트**: 전극 위 **얇은 산화·Li-결핍 전해질층(예: 원소 S)**이 Li 이동을 차단해 전류가 안 보일 뿐 — **CV는 고전압 Li-수송 측정으로 보강해야** ([Adeli]/[Taklu] CV 함정 행의 원조 경고).
5. **양쪽 전극에 다 좋은 SE는 드묾**: Fig 2 기준 **LLZO·LiAlO₂**가 고전압 양극 요건 충족(β″-알루미나 유사). binary 할라이드는 창은 극광이나 σ가 낮고, **제2 양이온을 넣으면 저전압 음극에 환원 불안정**(8c의 금속 환원 행들).
6. **코팅 논리**: 코팅은 전해질을 낮은 μ_Li로부터 격리; **코팅 결함부에서 일어나는 양극|전해질 반응이 passivating·이온절연 산물을 만들어 결함에 자가-복원적** → 저전도 재료라도 **얇게** 쓰면 됨. 음극 코팅은 더 어려움 — **Li 환원 산물이 대개 전자전도성(=not passivating)**.
7. **이중 전해질 전략**: 고전압 전해질(양극측)+저전압 전해질(음극측) — 예: **Li₃PS₄(음극측)+Li₂MgCl₄(양극측)**. 요건: 두 전해질의 μ_Li 창이 겹칠 것(Li 이동 구동력 없음) + **eq 2로 상호 화학반응 없음을 검증할 것**. ⚠ 단 본문은 이 쌍의 eq 2 검증값을 제시하지 않음 — Table S2의 `Li₂S+Li₂MgCl₄→4LiCl+MgS` 행은 황화물|염화물 혼합이 발열일 수 있음을 시사(§16 비판).
8. **결론**: 양극 μ_Li에서의 **벌크 안정 또는 "이온전도성 산물 passivation"**이 장수명의 요건; **질량 이동(혼합)을 허용한 열역학 계산이 계면 분석의 필수 확장**.

## 10. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | 풀셀 도식: 충전 시 양극측 **Li-결핍 분해층** / 음극측 **Li-환원 분해층** | 계면 열화 2-모드의 교과서 도식 (deck 인용) |
| 1c | Li binary 창 막대 (Li₃N→LiF) | binary 서열 = passivation 산물 사전; [Zhu15] Fig 2a와 동일 문법 |
| 2 | 전해질 ~30종 창 막대, **음이온별 그룹+해당 binary 병기** | "anodic 한계=음이온 binary" 논리의 그림; 황화물 좁은 창 직관 |
| 3a,b | Li–Zn–S–Cl 사원계 상도 + ΔE(x) V-곡선 (최심 0.27 eV/atom) | **pseudo-binary 방법 자체의 교육 그림** — 우리 interface_reactivity 설명용 1순위 |
| 4 | 양극7×전해질12 반응에너지 막대 (**at μ_Li vs with mixing 쌍**) | eq5/eq4 분리 진단의 시각화 — 우리 CSV에 no-mixing 열 추가 아이디어 |
| S1–S7 | 음이온군별(질화/수소화/황화/산화/브롬/염소/불소) 같은 막대 | 물질군 스캔; 수치는 전부 figure-read임을 명심 |
| Tables S1–S9 | 한계 반응 + 조합별 산물 전표 | **§8 발췌의 원천 — 우리 캠페인 ① 기대산물 리스트의 사전** |

## 11. Post-processing ★
- **무엇**: (i) grand-potential phase diagram(전위별 상평형·창), (ii) **pseudo-binary 반응에너지 최소화**(x-스캔), (iii) no-mixing 분리(eq 5), (iv) 산물 표 작성(반응식), (v) 막대그래프(at-μ vs mixing 쌍).
- **도구**: VASP(형성에너지) + 실험 열화학표(NIST-JANAF/Kubaschewski) + **pymatgen**(상도/grand potential; 현재의 `InterfacialReactivity`/`GrandPotentialInterfacialReactivity` 클래스가 이 논문 방법의 라이브러리화).
- **수치화·기록**: 조합당 [반응식 @cathode-μ_Li, 반응식 with-mixing] + 막대(eV/atom, 비-Li 원자 정규화). 창은 Fig 2 막대(표 없음).

## 12. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md` ★★

### 12a. 방법 계보 판정
| 요소 | Richards 2016 | 우리 | 판정 |
|---|---|---|---|
| SE 단독 창 | eq 1 (=[Zhu15]와 동일 구성) | `esw_grand_potential.py` (pymatgen get_element_profile) | ✓ 동일 형식 ([Zhu15] digest §10a에서 판정 완료) |
| 계면 반응성 | **eq 2(닫힌)/eq 4(개방)/eq 5(no-mixing)** | **`GrandPotentialInterfacialReactivity` 기반 interface_reactivity** (`oxidation_stability.json`의 `*_interface_reactivity`) | **✓✓✓ 직계 — 우리 도구가 이 논문 형식의 pymatgen 구현** ([Sundar]도 동일 도구) |
| hull 데이터 | ICSD+data-mined, **실험 열화학 하이브리드**(nearest-phase 참조) | MP 2026 (GGA/GGA+U + MP2020 보정) | △ 세대·보정 계열 다름 → **산물 종은 대체로 보존, 전압·중간상은 이동** (12b) |
| μ_Li 선택 | 양극 **평균전압** 고정 | 우리 interface_reactivity는 케이스별(문서화된 μ 명시 필요) | ⚠ **μ_Li 명시 없이 산물 비교 금지** — 같은 조합도 μ에 따라 Li-함유 산물(저 delithiation) ↔ Co-rich 산물(고 delithiation)로 갈림 |
| 계면에너지 | 무시(~100 meV/atom 상한 정당화) | 동일(무시) | ✓ 같은 근사 — 미세 \|ΔΦ\| 판정 한계 공유 |

### 12b. argyrodite 수치·산물 대조 (문헌 소환값 — 우리 절대값과 별도 표기)
| 항목 | Richards 2016 | [Zhu15] (MP2015) | 우리 (MP2026, GG set) | 해석 |
|---|---|---|---|---|
| 산화 onset 반응 | `Li₆PS₅Cl → S + Li₃PS₄ + LiCl` (Table S1) | 2.01 V 동일 반응 | **2.256 V 동일 반응** | **✓✓✓ 3세대 hull에서 산물 화학 불변** (전압만 세대 의존 — [Zhu15] §10b 판정 재확인) |
| 첫 환원 단계 | `2 Li₆PS₅Cl + 2 Li → Li₄P₂S₆ + 4 Li₂S + 2 LiCl` (**P⁴⁺ 중간체**) | 1.71 V에서 `+5 Li → P + Li₂S + LiCl` (P⁰) | ocv 1.717 V 경계(Li₃PS₄+Li₂S+LiCl 중성 조합) → red 1.242 V(P→LiP₇계) | ⚠ **hull entry 의존**: Richards hull엔 Li₄P₂S₆가 있어 첫 단계가 P⁵⁺→P⁴⁺; Zhu/우리 계단엔 없음. **P–P 결합 중간체 = MD에서 찾아볼 가치 있는 후보**(§13) — 단 "어느 쪽이 맞다" 단정 금지(DB 차) |
| 0 V 종점 | (S1은 창 경계 반응만; S5 LiTiS₂ 행이 저전위 방향 `5 Li₂S + P + LiCl`) | **Li₃P + Li₂S + LiCl, E_D −0.96 eV/atom** | **동일 산물** (esw: Li₃P+5Li₂S+LiCl) | ✓ 0 V 화학은 전원 일치 — 캠페인 ① 종점 |
| 고전압(LiCoO₂ μ) 산물 | **SCl·CoSCl 등 S–Cl 화학** (LiCl 소모) | 2.88 V부터 PCl₃ (5 V E_D −1.33) | 우리 staircase **3.326 V SCl** (modelc 3.39 PCl₅) | ✓ **"Cl은 맨 마지막에 산화되며 S–Cl/P–Cl 상으로 감"** 3자 공통; 상 동정은 DB 의존 |
| vs LiCoO₂ mixing 산물 | CoSCl+S+CoP₄O₁₁+CoS₂ (완전 delithiation, 평균전압 μ) | (해당 계산 없음 — 2016 JMCA 후속) | `nd2o3_interface_reactivity` (vs LiCoO₂): Co₉S₈+Li₃PO₄+Li₂S+LiCl+Li₂SO₄, dE −0.32~−0.33 eV/atom | △ **같은 형식·다른 μ/hull**: 우리 산물은 Li-보존적(저산화 조건), Richards는 심탈리튬 조건 — 산화도가 μ_Li 함수임을 보여주는 좋은 대비. 혼용 금지 |
| 산화 한계의 원인 | **"Li₆PS₅Cl의 anodic 안정성은 Li₂S(=S²⁻)가 지배"** (본문 명문) | S²⁻→S⁰ 공통 | S²⁻-limited onset 2.256 V (comp1=modelc 동일) | **✓✓✓ 우리 axis ① 문장의 2016 원조** — [Banik] S-pin·[Son] "<2.5 V"와 한 계보 |

### 12c. 우리 oxidation CSV(collapse/late-TM 회피)와의 대비
- Richards의 **양이온 산화 예외**(Li₂MnBr₄ Mn²⁺ 산화로 창 축소)와 **다가 양이온 환원**(Zn/Cd/In/Al → 금속, LiTiS₂ 전위서도) = 우리 cascade **late-TM/환원성 양이온 회피 판정과 동일 물리의 양면**: (a) 산화측 — TM이 새 산화 채널을 열어 창 붕괴(우리 Fe₂O₃/CoO/MnO collapse 0.004–0.039 V), (b) 환원측 — TM/다가 양이온이 금속으로 환원돼 전자전도 산물(=passivation 실패, [Zhu15] MCI). Richards §Discussion "제2 양이온 추가 → 저전압 음극 불안정"이 (b)의 원문.
- 단 Richards엔 **"창<임계 collapse 플래그" 같은 자동 판정은 없음** — 우리 CSV의 기여 지점. 역으로 [Zhu15] LLZO 사례(0.021 eV/atom inconclusive)의 경고대로 **미세 창·미세 ΔΦ(<0.1 eV/atom)는 계면에너지 상한(~0.1 eV/atom)과 같은 급이라 순위 다툼 금지**.

### 12d. 역할 분담 (this paper ↔ [Zhu15] ↔ 우리)
- [Zhu15] = SE 혼자 (창 + passivation 서사) → 우리 `esw_*` 체인.
- **Richards 2016 = SE×전극 혼합 (계면 반응성 + 조합 스크리닝 + 설계 처방)** → 우리 `interface_reactivity` 체인.
- 우리 캠페인 ① = 이 열역학 **종점**들에 UMA-MD로 **경로/속도(동역학)**를 붙이는 작업 — 문헌이 "무엇이 되나"를, 우리가 "어떻게·얼마나 빨리 되나"를 맡는 구조.

## 13. 캠페인 ① (Li|도핑SE 계면 MD) 기대-산물 리스트 ★ — 이 논문+[Zhu15]에서 도출
> 용도: `mlip_next_campaigns_2026_07.md` §① 의 "신규 상 DFT 스팟체크" 대상 목록과 analyzer 관측량 정의. **열역학 종점 = 문헌 소환값**, MD는 같은 시간창 상대비교만(캠페인 규율).

| 단계 | 기대 상 (문헌 근거) | MD 관측량 (기존 analyzer 매핑) |
|---|---|---|
| 접촉 초기(창 상단, ~1.7 V 등가) | **Li₄P₂S₆형 P–P 결합 중간체**(Richards S1 cathodic; hull-entry 의존이라 "있으면 보너스") + Li₂S + LiCl | P–P 최근접거리 신규 피크(RDF), PS₄ 보존율 하락 개시 |
| 진행(중간) | **P⁰/LiP₇→LiP 계열**([Zhu15] S2f 계단 1.71→0.87 V) + Li₂S 성장 | P 배위서 S 소실, P–Li 배위 증가; S–Li 배위(Li₂S 모티프) 층 성장 |
| 종점(0 V 열역학) | **Li₃P + Li₂S + LiCl** ([Zhu15] E_D −0.96 eV/atom; Richards 동일 화학; 우리 esw 동일) | 원소별 z-침투 깊이 포화 여부(self-limit), Cl는 LiCl로 잔류(관전자) |
| 도핑 분기 (O-계: B₂O₃·CaO 등) | **Li₂O**(산화물 환원 산물의 공통 종점; Richards S1 Li₃PO₄→Li₂O+Li₃P·LiPON→Li₂O 계열) — B 특이상(Li₃BO₃류)은 이 논문 범위 밖 **n/a** | O 배위 변화(P–O→Li–O), B–S/B–O 배위 per-frame(기존 B₂O₃ 트래커) |
| 도핑 분기 (F-계: CaF₂·LiF·ScF₃) | **LiF**(binary 종점; Richards Fig 1c 최광창=0 V 안정) | F–Li 응집(LiF 클러스터), F의 Li층 침투 여부 |
- **DFT 스팟체크 세트(캠페인 ① 리스크 항 충족)**: Li₂S·Li₃P·LiCl·Li₂O·LiF (+관찰되면 Li₄P₂S₆) — UMA 검증범위 밖 신규 상 목록이 이 표로 확정됨.
- **판정 문법**: MD에서 위 산물이 **같은 시간창에 도핑 셀에서 덜/더** 나오는지가 1차 결과(절대 속도 금지); passivation 성립 여부는 "침투 깊이 포화(self-limit)"로 정의 — 100 ps에서 self-limit 안 되는 건 이미 기록된 한계.

## 14. 적용 인사이트
1. **도구 정통성 문장 확보**: 우리 interface_reactivity는 Richards 2016 eq 2/4의 pymatgen 직계 구현 — [Zhu15](창)와 이 논문(혼합)으로 우리 열역학 체인의 원전 2편이 모두 digest됨.
2. **eq 5(no-mixing) 열 추가 아이디어**: 우리 CSV에 "at-μ(전해질만)" vs "with-mixing" 쌍을 병기하면 구동력의 원인(전위 vs 화학 혼합)을 조합별로 분리 진단 가능 — Fig 4의 문법 그대로.
3. **코팅/도핑 판정에 '@V none ≠ 안전' 규율**: §8d 클래스가 증명 — 전압 창만 보고 "호환"이라 말하면 틀림. [Cha] LZC dual-compat·[Sundar] 코팅 스크린 논리의 원전.
4. **캠페인 ① 설계 완성**: §13 표가 그대로 analyzer 스펙+스팟체크 목록. "그들 열역학 종점 ↔ 우리 동역학 경로" 역할 분담이 논문 프레임으로 깔끔.
5. **고-Ni 주의보**: LiNbO₃\|LiNiO₂ mixing 반응(Li₃NbO₄+NiO)·Li₆PS₅Cl\|LiNiO₂의 NiCl₂/Ni₃S₄/Li₂SO₄ — 고-Ni 양극은 코팅·전해질 모두에게 LiCoO₂보다 가혹 (우리 NCM 문맥·[Zuo] sulfate 관찰과 결 일치).
6. **이중 전해질(§9-7) 아이디어**: 황화물(음극측)+광창 할라이드(양극측) — 단 상호 eq 2 검증 필수라는 조건까지 세트로 인용.

## 15. 인용 가능 문장 (deck/paper용)
- "Our interfacial-reactivity screen implements the pseudo-binary construction of Richards et al. (2016): the reaction energy is minimized over the mixing fraction x of the two phases, in both the closed (chemical) and Li-open (grand-potential) ensembles."
- "Richards et al. already noted in 2016 that 'the anodic stability of Li₆PS₅Cl is determined primarily by the stability of Li₂S' — the S²⁻-limited oxidation onset we compute (2.256 V, identical for Li₆PS₅Cl and the Cl-rich composition) is the modern-hull restatement of that original observation."
- "Thermodynamic endpoint tables (Richards 2016; Zhu 2015) define the expected product set of our Li|SE interface MD — Li₂S, Li₃P and LiCl at 0 V — so the MD adds the kinetic pathway (rates, penetration depth, self-limiting behavior) to a fixed chemical destination."
- "Combinations that are electrochemically stable at the cathode potential can still react chemically upon mixing (e.g., Li₂MgCl₄ with every cathode tested) — voltage-window screening alone is insufficient for interface compatibility."

## 16. 주의/한계 (over-claim 방지 — 비판적으로)
- **0 K hull·PV/엔트로피 무시** + metastable SE의 E_hull→0 규약 = 창을 넓히는 방향의 선택 ([Zhu15]와 동일 한계).
- **계면에너지 무시(~100 meV/atom 상한)**: |ΔΦ|가 이 급인 조합(산화물 전해질 다수, Fig 4의 0~−0.3 구간)은 **부호/순위 판정이 근사 안에 있음** — "none"과 "미세 반응"의 경계 조합을 확정 인용 금지.
- **x-최소화 = 가장 발열인 혼합점**: 실제 계면은 확산 제한으로 그 조성을 못 찾아갈 수 있음 — 산물 목록은 "열역학이 허용하는 최심 조합"이지 실측 층서열이 아님. kinetics는 핵생성 논리(정성)뿐.
- **수치 표 부재**: 조합별 ΔΦ는 막대그래프뿐 — 본 digest의 eV/atom 값은 전부 figure-read(±0.05) 표기. 정량 인용은 반응식(표)과 본문 명시값(0.27 eV/atom, 1.2/2.75 V)만.
- **hull 세대 의존**: 실험 열화학 하이브리드(NIST-JANAF/Kubaschewski) + 2015 ICSD/MP — 중간상(Li₄P₂S₆ 유무, SCl vs PCl₃ 등)과 전압은 DB 세대에 민감. [Zhu15] §10b의 "산화측 민감" 판정이 여기도 그대로 적용 — **산물 '종'의 큰 화학(폴리설파이드/인산염/LiCl/합금)만 세대-불변으로 인용**.
- **LiPON 대표성**: Li₃.₂PO₃.₈N₀.₂≈Li₁₆P₅O₁₉N 결정 근사(실물 amorphous) — LiPON 행 정량 이식 금지.
- **이중 전해질 제안(Li₃PS₄+Li₂MgCl₄)은 본문 내 eq 2 미검증** — Table S2의 Li₂S|Li₂MgCl₄→4LiCl+MgS 발열 행이 황화물|염화물 혼합 반응 가능성을 시사. 제안 셀(Li₃PS₄|LiVS₂ 등)도 열역학 예측일 뿐 실증 없음.
- **"passivating/이온절연/전자절연" 판정이 전부 정성** — σ_e·gap·두께 계산 없음(우리 sei_products gap 분류·[Sundar] 산물-전도도 스크린이 정량 후속).
- **SI 인쇄 표기 흔들림**: LiBH₄ closo상(Li₂B₆H₁₂ vs Li(BH)₆), Table S2 vs S5/S6의 등가 반응 이표기(LLZO@LiCoO₂), LiPON 일부 계수 — 본 digest는 균형 검산으로 교정·플래그했고, 저신뢰 계수는 산물 종만 인용.
- **양극 전위 = 평균전압 고정**: 충전 말단(고 SOC)의 더 낮은 μ_Li에선 구동력·산물이 더 가혹해짐 — [Zuo]의 ≥4.2 V O-방출 결합 열화 같은 SOC-의존 화학은 이 프레임 밖.

## 17. 기법 용어 미니사전
- **pseudo-binary**: 두 고정 조성(전해질·전극)을 잇는 조성선(x·cₐ+(1−x)·c_b) 위에서만 반응을 허용하는 열역학 구성 — 계면에서 두 상만 만난다는 물리를 조성 공간에 투영.
- **E_pd[c] / Φ_pd[c, μ_Li]**: 조성 c의 phase-diagram 바닥(상평형) 에너지 / 그 grand-potential 버전(Li 개수 n_Li까지 최적화).
- **ΔΦ vs ΔΦ_no-mixing**: 개방계 계면 반응 구동력 vs 혼합 금지(x=0) 구동력 — 차이가 "화학 혼합의 몫".
- **reaction at cathode voltage (SI 표 열)**: 그 양극의 평균전압 μ_Li에서 전해질 단독 분해(eq 5의 산물).
- **reaction with mixing (SI 표 열)**: 같은 μ_Li에서 양극과 섞이며 가는 최심 반응(eq 4의 산물).
- **tieline 판정**: 상도에서 두 상을 잇는 tieline이 hull 위에 있으면 그 계면은 열역학 안정(Fig 3의 LiCl–ZnS).
- **Gibbs triangle / nearest phases**: 조성을 포함하는 상도의 저에너지 facet 꼭짓점 상들 — 실험 형성에너지 참조점으로 사용(산화상태 보존 반응의 DFT 오차 상쇄).
- **passivation vs kinetic stabilization**: 산물이 전자절연이라 구동력 자체가 꺼짐 vs 핵생성/확산이 느려 못 갈 뿐(ΔG* ∝ γ³/ΔG²) — 후자는 장기 열화 경로.
