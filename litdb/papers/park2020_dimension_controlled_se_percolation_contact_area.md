# 치수 제어 산화물 고체전해질 (0D 구 · 1D 원기둥 · 2D 판) 을 넣은 전고체 전극 — 퍼콜레이션 경로 · specific contact area · 유효 이온전도도 (GeoDict 복셀 가상 전극 → COMSOL P2D) — Park (Chem. Eng. J. 2020)
> slug `park2020_dimension_controlled_se_percolation_contact_area` · DOI `10.1016/j.cej.2019.123528` · type `voxel-sim (GeoDict 확률 배치 · PoroDict 접촉면적 · ConductoDict Ohm σ_eff → COMSOL 5.4 P2D; 산화물 LLZO-Ta · 흑연 음극 · 실험 없음)` · PDF `5. Dimension-controlled solid oxide electrolytes for all-solid-state electrodes Percolation pathways, specific contact area, and effective ionic conductivity.pdf` · digested `2026-10-03` · status ✅
>
> SI = `5. Sup) Dimension-controlled solid oxide electrolytes for all-solid-state electrodes Percolation pathways, specific contact area, and effective ionic conductivity.pdf` (10쪽) — **본문 9쪽 · SI 10쪽 전부 읽음**.
> **쪽 표기**: 본문 p.n = 학술지 쪽 = PDF 쪽 (*Chem. Eng. J.* 391 (2020) 123528, 1–9쪽 · **환산 없음** · p.1 = 표제 · 초록).  SI p.n = SI PDF 쪽 (SI 에는 인쇄 쪽 번호가 없다): p.1 표지 · p.2 Fig. S1 + Table S1 · p.3 Fig. S2 + Table S2 · p.4 Fig. S3 + Table S3 앞 · p.5 Table S3 뒤 + 각주 · p.6 Fig. S4 · p.7 Fig. S5 + Fig. S6 · p.8 Fig. S7 + Nomenclature · p.9–10 Nomenclature.
> **식 번호**: 원문에 번호 붙은 식이 **하나도 없다** — 식은 SI 그림 (Fig. S2 · Fig. S3) 안에만 있다.  그림 · 표 번호 = 원문.
> 수식 · 표 · 그림이 든 쪽은 전부 그림으로 렌더해 읽었다 (텍스트 추출은 지수 · 그리스 문자를 깨뜨린다).  값 표지: **stated** = 본문 · 캡션 · 표 · 그림 안 글자 / **판독** = 그림에서 읽은 값 (≈ · TREND 전용 · 정밀 인용 금지) / **파생** = 이 카드 작성자의 계산 (식 명시 · 원문 값 아님) / **[미확인]** = 원문에 없음.
>
> ★ **이 카드의 역할** — 형제 카드 `park2020_digitaltwin_assb_foundational` (*Adv. Energy Mater.* 2020 — **다른 논문**, DOI `10.1002/aenm.202001563`) 의 SI Fig S9 (σ_eff 식 · 경계조건) 캡션이 인용하는 **[12b]** 원문이다.  그 카드가 남긴 열린 질문 (τ 산출법 · 경계조건 · σ₀ · 접촉면적 분모) 에 이 원문이 답하는지를 **§ τ 정의 대조 (3)** 에서 닫는다.
>
> ★ **판정 요약**
> - (1) 전극 SE = **산화물** garnet **LLZO-Ta** (Li₇La₃Zr₂O₁₂-Ta) · AM = **흑연 음극** · P2D 셀의 분리막만 **황화물 Li₂S–P₂S₅ 펠릿**.  **LPSCl 은 어디에도 없다.**  **실험 0 건** — 전부 가상 전극이다.
> - (2) τ 는 본문 산문 (p.3) 과 SI Fig. S2 의 그림 안 식 **j = (εσ/τ)∇φ** (SI p.3) 에만 나온다.  **정의 · 값 · 명명표 항목이 없다** (SI p.8–10 Nomenclature 에 τ 없음).  식의 대수로 **τ = ε·σ₀/σ_eff = 우리 tau2 자리** (원문 이름 "tortuosity" — "factor" 없음).
> - (3) σ₀ = **LLZO-Ta 5.4×10⁻⁴ S cm⁻¹ 상수** (Table S2, 문헌 [17]).  형제 카드 (AEM) 의 조성 의존식과 **다르다**.  단일 전도상 선형 해라 이 모형 안에서 **σ₀ 는 τ 에서 약분된다** (파생).
> - (4) **specific contact area = AM–SE 접촉면적 ÷ 전 AM 부피** [m⁻¹] (p.3 정의).  SI 명명 · P2D 자리 (전극 부피당) 와 분모가 어긋날 수 있다.
> - (5) 퍼콜레이션 = **SE 만 든 50 µm 상자**의 바닥 → 위 (z) **최단 퍼콜레이션 경로 길이** (0 = 비관통).  **단일 실현** (p.3 · Fig. 1).
> - (6) 계면: **공간전하층 미고려 명시 · 접촉은 겹친 복셀 융합** → 계면 저항 항 0 = 우리 분류로 **CONTACT_FREE 부류** (STEP3 복셀 쪽).
> - (7) ⚠ **SI Table S3 와 그림 · 본문 사이 불일치 4 건** — 1D 2500 σ_eff 지수 · 2D 2500 a_s · 혼합 3:1↔1:3 라벨 · 본문에 없는 '1:3' 행 (§3-H).

---

## 1. 한 줄 요약
흑연 음극에 넣는 산화물 SE (LLZO-Ta) 의 **형상 차원** — 0D 구 (지름 250 · 500 · 1000 nm), 1D 원기둥 (지름 250 nm, 길이 2.5 · 5 · 7.5 µm), 2D 정사각 판 (두께 250 nm, 변 2.5 · 5 · 7.5 µm) — 을 GeoDict 복셀 가상 전극 (복셀 100 nm) 에서 바꿔, (i) SE 만 든 상자의 최단 퍼콜레이션 경로, (ii) 흑연–SE 접촉면적 ÷ 흑연 부피 (specific contact area), (iii) ConductoDict 유효 이온전도도 σ_eff 를 내고, (iv) 그 값을 COMSOL P2D 에 넣어 율특성을 예측한 **순수 시뮬레이션** 논문이다.  결론은 넷이다.  0D 는 ≤ ~500 nm 여야 이온 경로가 생긴다.  1D 는 접촉면적이 0D 250 nm 의 약 1/3 로 줄어도 σ_eff 가 약 15–23 배 커서 성능이 가장 좋다.  2D 는 판이 커지면 전극을 못 채워 두께가 1.5–2.2 배 늘어난다.  0D:1D = 2:2 혼합은 1D 단독 성능에 근접한다 (SE 13.5 vol% 고정).  우리에게 주는 것도 셋이다.  (a) 이 그룹의 "σ_eff = εσ/τ" 관례의 [12b] 원전을 확인한다 — **τ 정의 · 값은 여기에도 없다**.  (b) 접촉면적 정의 (AM 부피당) 와 퍼콜레이션 정의 (최단 경로 길이, 단일 실현) 가 우리 LHS 열과 어디서 다른지 보여 준다.  (c) 복셀 융합 · 계면 저항 0 인 **CONTACT_FREE 부류 T** 의 문헌 예다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/AM) | 연구유형 |
|---|---|---|---|---|
| **Joonam Park** (DGIST, 공동 1저자) · **Ju Young Kim** (ETRI, 공동 1저자) · Dong Ok Shin · Jimin Oh · Jumi Kim · Myeong Ju Lee (ETRI) · **Young-Gi Lee** (ETRI, 교신) · **Myung-Hyun Ryou** (한밭대, 교신) · **Yong Min Lee** (DGIST, 교신) | *Chem. Eng. J.* **391** (2020) 123528 (9쪽) | 10.1016/j.cej.2019.123528 | 전극 SE = **LLZO-Ta** (garnet 산화물) · AM = **흑연** (음극) · 바인더 SBR/CMC 5 wt% · (P2D 셀: 분리막 Li₂S–P₂S₅ 펠릿 · 상대극 Li 금속) | **순수 시뮬레이션**: GeoDict 가상 전극 (복셀) → PoroDict · ConductoDict → COMSOL Multiphysics 5.4 Batteries & Fuel Cells (Newman P2D) |

- 접수 2019-10-09 · 수정 2019-11-15 · 승인 2019-11-17 · 온라인 2019-11-22 (p.1).  © 2019 Elsevier.
- 소속 (p.1): a DGIST 에너지공학과 · b ETRI Nano Convergence Devices Research Department (Power Control Device Research Section) · c 한밭대 화학생명공학과.
- 연구비 (p.6): NRF 기후변화대응 기술개발 (NRF-2017M1A2A2044493) · DGIST R&D (19-01-HRHR-02) · DGIST Supercomputing and Bigdata Center.
- 키워드 (p.1): Dimension-controlled solid oxide electrolyte; Percolation; Specific contact area; Effective ionic conductivity; All-solid-state electrode; All-solid-state batteries.
- 하이라이트 (p.1, 원문): "Ionic pathway can be enhanced introducing dimension-controlled solid electrolytes." · "Effective conductivity is a key parameter for performances of all-solid-state electrode." · "Blending 0D and 1D solid electrolytes is to realize high-performance of all-solid-state batteries."
- **계보 (인용 사슬로만)**: 이 논문의 σ_eff 계산 문장은 [15] = Park 2019 *Energy Storage Mater.* 19, 124 를 인용한다 (p.3).  [15] 는 같은 묶음 형제 카드 `park2019_electrode_design_methodology_assb_3d` 다 (이 카드는 그 카드의 내용을 대조하지 않았다).  형제 카드 AEM 2020 은 SI Fig S9 캡션에서 [12] = (a) Park 2019 ESM + (b) 이 논문을 인용한다.  "digital twin" 낱말은 이 논문에 없다 — "virtual electrodes" · "virtual 3D image analysis" 라 부른다 (p.1 · p.2).  GeoDict 판 (version) 미기재 [미확인].
- 원본 위치: `litdb/inbox/` (원래 파일명 그대로).

## 3. 핵심 수치

### 3-A. 설계 행렬 (stated)
| 항목 | 값 | 위치 |
|---|---|---|
| SE 9 종 | **0D** 250 · 500 · 1000 nm (구 지름) · **1D** 2500 · 5000 · 7500 nm (원기둥 길이 · 밑면 지름 250 nm 고정) · **2D** 2500 · 5000 · 7500 nm (정사각 판 가로 = 세로 · 두께 250 nm 고정) | p.2 · p.4 · SI Fig. S1 |
| 최소 치수 | 250 nm (세 계열 공통) — "Considering the practical size control of LLZO-Ta by the synthesis" | p.2 |
| 조성 (wt%) | 흑연 57.0 : LLZO-Ta 38.0 : SBR/CMC 5 (= 흑연:SE **60:40**) · 흑연 66.5 : LLZO-Ta 28.5 : SBR/CMC 5 (= **70:30**) | p.2 |
| 적재량 · 기공 | 7 mg cm⁻² · 30 % — 2D 는 30 % 를 못 맞춰 두께 증가 허용 | p.2 |
| 혼합 SE | 0D 250 nm : 1D 5000 nm = **3:1 · 2:2** (본문) — Table S3 에는 1:3 행도 있다 (본문 · 그림에 없음) | p.5 · SI p.4–5 |
| 복셀 | **100 nm** ("approximately one-third of the smallest LLZO-Ta particle") — 실제 비 100/250 = 0.4 (파생) → **최소 치수 = 2.5 복셀** | p.2 |
| 도메인 | 밑면 50 × 50 µm (500 × 500 복셀) · 높이 = 충전 결과 (전극 ≈ 39 µm, Table S3 L_n) | p.2 · SI p.4 |
| 퍼콜 분석 상자 | **SE 만** · 한 변 50 µm 정육면체 · SE 0–30 vol% · 0D 250 / 1D 2500 / 2D 2500 | p.2 · p.3 |
| 흑연 | ellipsoid convex polyhedral · Gaussian 크기 · 등방 방위 · 겹침 허용.  Table S1: Random Points 30 · 지름 x 15 (SD 5, Bound 5) · y 10 (5, 7.5) · z 10 (5, 5) µm | p.2 · SI p.2 |
| SE 배치 | 균일 크기 · "by overlap with an isolation distance −0.1 μm" (흑연 주위에 놓이고 잘 접촉) · 흑연–SE 겹침 부피 (< 0.5 % of domain) 는 LLZO-Ta 로 재배정 ("considering their relative strengths [18,19]") | p.2 |
| 바인더 | "Added Binder Function" 으로 흑연 · LLZO 외벽 코팅 · 접촉한 입자 사이에는 바인더 없음 가정 [20] | p.2 |
| 고유 전도도 (Table S2, S cm⁻¹) | 흑연 전자 **2.5** [15] · 이온 0 · SBR/CMC 0 · 0 · LLZO-Ta 전자 0 · **이온 5.4×10⁻⁴** [17] | SI p.3 |
| P2D 셀 | 복합 음극 (L_n 39 µm · 2D 2500 은 42 µm) · LPS 펠릿 (L_e **1000 µm**) · Li 금속 · 1 C = **1.2 mA cm⁻²** · 25 °C (298.15 K) · 0.1 / 0.3 / 0.5 C · 설계 용량 1.2 mAh cm⁻² | p.3 · p.5 · SI p.4–5 |

### 3-B. 퍼콜레이션 — SE 만 든 50 µm 상자, 바닥 → 위 (z) 최단 퍼콜레이션 경로 길이 (Fig. 1, p.4)
| SE vol% | 0D 250 nm | 1D 2500 nm | 2D 2500 nm |
|---|---|---|---|
| 0 · 5 | 0 | 0 | 0 |
| 10 | 0 | **77** (Fig. 1b 표지) | 0 |
| 15 | 0 | ≈ 66 | ≈ 82 |
| 20 | 0 | 50 | **50** (Fig. 1b 표지) |
| 25 | **83** (Fig. 1b 표지 · 1a 판독 ≈ 83.5) | 50 | 50 |
| 30 | ≈ 67 | 50 | 50 |

단위 µm.  0 = 퍼콜레이션 경로 없음 (p.3 원문 "the length of the shortest percolation pathway has a zero value meaning that no percolation is formed").  표지 아닌 값은 판독.

- **관통 시작 구간** (판독): 1D 5–10 vol% · 2D 10–15 vol% · 0D 20–25 vol%.  원문 (p.3): *"In the case of solid electrolytes with a restricted content of under 20 vol%, … the solid electrolytes with a high dimensional geometry (Fig. 1b-1 and b-2) start securing the percolation pathway, while those with a low dimensional geometry (0D) can have a percolation structure of more than 25 vol% (Fig. 1b-3), which is consistent with percolation theory trends."*
- **파생 τ_geo** (= 경로 길이 ÷ 상자 변 50 µm · 우리 산술):
  - 1D: 10 % 1.54 · 15 % ≈ 1.32 · ≥ 20 % 1.00
  - 2D: 15 % ≈ 1.64 · ≥ 20 % 1.00
  - 0D: 25 % 1.66 · 30 % ≈ 1.34
  - 원문은 이 비를 계산하지 않는다 — *"how close the shortest percolation pathway is to the side of the structure"* (p.3) 로만 읽는다.
- ⚠ **≥ 20 vol% 1D · 2D 의 경로 = 정확히 50 µm (= 완전 직선)** 가 세 점 연속이다 (Fig. 1b-2 는 곧은 수직선).  겹침 허용 무작위 배치 20 vol% 에서 50 µm 직선 전체가 SE 안에 있을 확률은 작다 (우리 판단).  경로 길이 산정 방식은 원문 미기술 [미확인] → **τ_geo = 1.00 을 물리값으로 읽지 말 것.**
- Fig. 1c (20 vol% 단면) 원문 서술 (p.3): 0D 250 은 *"many isolated particles … and a tortuous pathway"* · 1D 2500 은 *"minimizing the isolated particles and the tortuosity"* — 정성 (수치 없음).

### 3-C. 전극 두께 (Fig. 2a, p.4 · Table S3)
| SE | 두께 (판독) | 원문 · 표 |
|---|---|---|
| 0D (기준선) | ≈ 38.3–38.6 µm | Table S3 L_n "39×10⁻⁶ m (Others)" |
| 1D 2500 · 5000 | ≈ 38.6 | 증가 없음 |
| 1D 7500 | ≈ 39.2 | *"a small thickness increase (~1 μm)"* (p.4) |
| 2D 2500 | ≈ 41.7 | *"a small thickness increase of ~2 μm"* (p.5) · Table S3 L_n 42×10⁻⁶ m |
| 2D 5000 | ≈ 60.1 | *"~1.5 … times greater"* (p.4) — 60.1/38.5 ≈ 1.56 (파생) |
| 2D 7500 | ≈ 85.3 | *"over 2 times greater"* (p.4) — ≈ 2.2 (파생) |

- 원인 (원문 p.4): *"owing to the large size and high anisotropy of the solid electrolytes with a high dimensional geometry and intrinsic stiffness of the LLZO-Ta, it was impossible to fill the electrode pores with 1D 7500 nm and all 2D solid electrolytes while satisfying the fixed pore density of the electrode"* → 흑연과 2D 판이 서로 피한다 (Fig. 2b).
- ⚠ 역학 계산은 없다 — '강성' 은 **배치 알고리즘이 못 채운 결과**에 붙인 해석이다.

### 3-D. specific contact area (SCA) · σ_eff — 치수 축 전부
| 전극 | ε_e (Table S3) | SCA Table S3 | SCA 그림 판독 | σ_eff Table S3 | σ_eff 그림 판독 | 그림 | 비고 |
|---|---|---|---|---|---|---|---|
| 60:40 0D 250 | 0.135 | 70099 | ≈ 7.0×10⁴ | 5.69×10⁻⁷ | ≈ 5.7×10⁻⁷ | S5 · 6a · 7a | 일치 |
| 60:40 0D 500 | (0.135 가정) | — | ≈ 2.5×10⁴ | — | ≈ 4.3×10⁻⁸ | S5 | 표에 없음 |
| 60:40 0D 1000 | — | — | ≈ 8.7×10³ | — | ≈ 0 | S5 | ion density 없음 (S4c) |
| 60:40 1D 2500 | 0.135 | 23133 | ≈ 2.30×10⁴ | **8.58×10⁻⁷** | **≈ 8.4×10⁻⁶** | 4a | ⚠ σ 한 자릿수 불일치 |
| 60:40 1D 5000 | 0.135 | 24347 | ≈ 2.42×10⁴ | 1.19×10⁻⁵ | ≈ 1.18×10⁻⁵ | 4a · 6a | 일치 |
| 60:40 1D 7500 | — | — | ≈ 2.35×10⁴ | — | ≈ 1.33×10⁻⁵ | 4a | 표에 없음 |
| 60:40 2D 2500 | 0.125 | **23621** | **≈ 1.20×10⁴** | 2.95×10⁻⁶ | ≈ 2.9×10⁻⁶ | 4a | ⚠ SCA 2 배 불일치 |
| 60:40 2D 5000 | — | — | ≈ 2.1×10³ | — | ≲ 2×10⁻⁷ (판독 한계) | 4a | |
| 60:40 2D 7500 | — | — | ≈ 4×10² | — | 막대 안 보임 | 4a | |
| 60:40 0D:1D 3:1 | 0.135 | **37022** | **≈ 5.95×10⁴** | 2.77×10⁻⁶ | ≈ 2.75×10⁻⁶ | 6a | ⚠ 그림 SCA = 표의 '1:3' 값 |
| 60:40 0D:1D 2:2 | 0.135 | 48639 | ≈ 4.85×10⁴ | 5.69×10⁻⁶ | ≈ 5.65×10⁻⁶ | 6a · 7a | 일치 |
| 60:40 0D:1D 1:3 | 0.135 | 59580 | — | 5.95×10⁻⁶ | — | 없음 | 본문 · 그림에 없는 행 |
| 70:30 0D 250 | — | — | ≈ 5.74×10⁴ | — | **0** | 7a | *"did not show any ionic conduction"* (p.6) |
| 70:30 0D:1D 2:2 | 0.095 | 38422 | ≈ 3.81×10⁴ | 2.43×10⁻⁶ (표 라벨 "1:3") | ≈ 2.40×10⁻⁶ | 7a | 본문 *"~2.0 × 10⁻⁶"* (p.6) |

SCA 단위 m⁻¹ · σ_eff 단위 S cm⁻¹ · ε_e = 전극 전체 대비 LLZO-Ta 부피분율 (SI 명명표 "volume fraction of electrolyte").

- **본문 서술 (stated)**:
  - 0D: 지름 ↑ 에 SCA · σ_eff 모두 감소, 250 → 500 nm 에서 *"an exceptionally sharp reduction"* → *"the particle size of the solid electrolyte should be less than ~500 nm"* (p.3–4).
  - 0D 의 σ_eff 는 *"ranged from 10⁻⁸ to 10⁻⁷ S cm⁻¹"* — 흑연 전자 σ_eff *"10⁻¹ S cm⁻¹"* 보다 훨씬 낮다 (p.4).
  - 1D: SCA 는 0D 250 보다 *"up to one-third lower"* 인데 σ_eff 는 *"more than twenty times"* (p.5).  *"if the specific contact area of ~2.2 × 10⁴ m⁻¹ is sufficient to receive lithium ions …, the 1D solid electrolyte improves the electrode performance"* (p.5).
  - 2D: SCA · σ_eff 모두 1D 보다 낮다.  그래도 2D 2500 의 σ_eff 는 0D 보다 높다 (p.5).
  - 혼합: *"tended to reach an average value depending on their weight contents"* (p.5).
  - 70:30: 0D 는 이온전도 없음 · 0D:1D 혼합은 *"~2.0 × 10⁻⁶ S cm⁻¹"* (p.6).
- **원문 낱말의 실제 크기** (파생):
  - "up to one-third lower" = 23133/70099 = **0.33 배** (약 1/3 수준으로 낮다 = 67 % 감소) 를 가리킨다.
  - "more than twenty times" 는 1D 5000 (×20.9) · 1D 7500 (×≈23, 판독) 에 맞는다.  1D 2500 은 그림으로 ×≈15 이고, Table S3 값 8.58×10⁻⁷ 이면 ×1.5 다.
- **같은 SCA, 다른 σ** (파생 · 판독 포함): 0D 500 (SCA ≈ 2.5×10⁴, σ ≈ 4×10⁻⁸) 과 1D 5000 (2.43×10⁴, 1.19×10⁻⁵) 은 SCA 가 거의 같은데 **σ_eff 는 ≈ 280 배** 다르다 → **접촉면적과 SE 망 전도는 다른 축**이다.

### 3-E. P2D 성능 (판독 — Fig. 4b · Fig. S6 · Fig. 6b · Fig. 7b)
**Fig. 4b** (60:40, 끝점 면적 용량 mAh cm⁻² — 곡선은 ≈ 0.05 V 근처에서 끝난다, 차단전압 원문 미기재):
| SE | 0.1 C | 0.3 C | 0.5 C |
|---|---|---|---|
| 0D 250 | ≈ 0.22 | ≈ 0.04 | ≈ 0.02 |
| 1D 2500 | ≈ 0.94 | ≈ 0.30 | ≈ 0.17 |
| 2D 2500 | ≈ 0.47 | ≈ 0.10 | ≈ 0.04 |

- 원문 (p.5): 설계 용량 1.2 mAh cm⁻² · 1D 2500 이 최선 · *"A capacity retention of ~75% at 0.1 C"* · *"the capacity of the 1D 2500 nm electrolyte at 0.3 C was superior to that of the 0D 250 nm electrolyte at 0.1 C"*.  해석: *"the effective ionic conductivity within the electrode in this cell system is more important than the specific contact area"*.
- **Fig. S6** (부피 용량 mAh cm⁻³, 0.1 C 판독): 1D 2500 ≈ 243 · 2D 2500 ≈ 114 · 0D 250 ≈ 58 — 면적 용량 ÷ 두께와 자기일관 (0.94 / 39 µm ≈ 241, 파생).

**Fig. 6b** (capacity retention %):
| SE | 0.1 C | 0.3 C | 0.5 C |
|---|---|---|---|
| 0D 250 | ≈ 19 | ≈ 3 | ≈ 1 |
| 0D:1D 3:1 | ≈ 50 | ≈ 13 | ≈ 6 |
| 0D:1D 2:2 | ≈ 73 | ≈ 21 | ≈ 10 |
| 1D 5000 | ≈ 76 | ≈ 25 | ≈ 14 |

- 원문 (p.5–6): *"the capacity retention at the condition of 0D:1D = 2:2 almost reached that of the electrode with 1D 5000 nm"*.

**Fig. 7b** (끝점 면적 용량 mAh cm⁻²):
| 전극 | 0.12 mA cm⁻² | 0.36 | 0.60 |
|---|---|---|---|
| 60:40 0D 250 | ≈ 0.23 | ≈ 0.04 | ≈ 0.02 |
| 60:40 0D:1D 2:2 | ≈ 0.88 | ≈ 0.26 | ≈ 0.12 |
| 70:30 0D:1D 2:2 | ≈ 0.73 | ≈ 0.53 | ≈ 0.33 |
| 70:30 0D 250 | 용량 없음 (*"was not achieved at all"*, p.6) | | |

- 원문 (p.6): 70:30 혼합 *"~0.7 mAh cm⁻²"* (0.12 mA cm⁻²) · 높은 전류 (0.36 · 0.60) 에서는 60:40 혼합보다 용량이 많다 — *"The electrode with an increased amount of active materials experienced a decreased C-rate"*.
- **Fig. S7** (SI p.8, 1D 5000 전극의 빈 공간에 SE 추가): 0D 500 nm 는 목표 15 vol% 까지 목표와 같고 최대 ≈ 17 vol% (기공 30 → ≈ 13 %) · 1D 5000 은 ≈ 1 vol% 에서 멈춘다.  원문 *"~ 17 vol%"* · *"~ 1 vol%"* (p.6).

### 3-F. SI 표 전사 (stated)
**Table S1** (SI p.2) — "Gaussian conditions for the particle of graphite", Unit µm, Random Points 30: Diameter of x axis 15 / 5 / 5 · y axis 10 / 5 / 7.5 · z axis 10 / 5 / 5 (Mean Value / Standard Deviation / Distribution Bound).

**Table S2** (SI p.3) — "Intrinsic electric and ionic conductivities of electrode materials", Unit S cm⁻¹: Graphite 2.5 [15] / 0 · SBR/CMC 0 / 0 · LLZO-Ta 0 / 5.4×10⁻⁴ [17] (Electric / Ionic).

**Table S3** (SI p.4–5) — "Model parameters and formulas":
| 매개변수 | 값 | 각주 |
|---|---|---|
| L_n | 42×10⁻⁶ m (2D 2500) · 39×10⁻⁶ m (Others) | a |
| L_e | 1000×10⁻⁶ m | a |
| R_s | 7.5×10⁻⁶ m | a |
| D_s | 1.45×10⁻¹³ m² s⁻¹ | b |
| D_e,LLZO-Ta | 3.74×10⁻¹³ m² s⁻¹ | c |
| D_e,LPS | 4.58×10⁻¹² m² s⁻¹ | c |
| k | 2.0×10⁻¹¹ m s⁻¹ | b |
| i₀ | 10 A m⁻² | c |
| σ_s,eff | 2.65×10⁻¹ S cm⁻¹ (2D 2500) · 4.64×10⁻¹ (70:30 wt% 2:2) · 3.58×10⁻¹ (Others) | a,c |
| σ_e,eff,LLZO-Ta | 5.69×10⁻⁷ (0D 250) · **8.58×10⁻⁷ (1D 2500)** · 1.19×10⁻⁵ (1D 5000) · 2.95×10⁻⁶ (2D 2500) · 2.77×10⁻⁶ (3:1) · 5.69×10⁻⁶ (2:2) · 5.95×10⁻⁶ (1:3) · 2.43×10⁻⁶ (70:30 wt% **1:3**) S cm⁻¹ | a,c |
| σ_e,LPS | 1.81×10⁻³ S cm⁻¹ | c |
| ε_s | 0.457 (2D 2500) · 0.537 (70:30 wt% 2:2) · 0.492 (Others) | a |
| ε_e | 0.125 (2D 2500) · 0.095 (70:30 wt% 2:2) · 0.135 (Others) | a |
| a_s | 70099 (0D 250) · 23133 (1D 2500) · 24347 (1D 5000) · **23621 (2D 2500)** · **37022 (3:1)** · 48639 (2:2) · **59580 (1:3)** · 38422 (70:30 wt% 2:2) m⁻¹ | a |
| c_s,max | 31507 mol m⁻³ | b |
| c⁰_e,LLZO-Ta | 38400 mol m⁻³ | c |
| c⁰_e,LPS | 16322 mol m⁻³ | c |
| t₊ | 0.99 | c |
| A | 1.131×10⁻⁴ m² | a |
| I_1C | 1.2 mA cm⁻² | a |
| T | 298.15 K | a |
| E_eq | 0.2033+0.6613exp(−68.63soc)−0.006943tanh((soc−0.4895)/0.0854) −0.0925tanh((soc−0.0317)/0.053)−0.075tanh((soc−0.5692)/0.875) +0.02675tanh(−(soc−0.1814)/0.03031) | c |

각주 (원문): **a** "Parameter set in electrode and cell design" · **b** "Obtained from COMSOL library" · **c** "Parameters based on literature (Ref. 15, 17 and 25)".
- σ_e,eff · a_s · ε 에 각주 a (설계) 가 붙는다 → 이 값들이 이 논문 3D 구조 해석의 출력이라는 뜻으로 읽힌다 (추론).  σ_e,eff 에는 c (문헌) 도 같이 붙어 있다.
- SI 에 수정 표시 흔적 (형광 칠: Fig. S4 캡션 · Fig. S6 캡션 · Fig. S7 번호 · Table S3 각주 a 일부 · 각주 c 의 "25") 이 남아 있다 — 내용과 무관.

### 3-G. 파생 — f · tau2 · tau · Bruggeman 배수 (우리 산술 · 원문 값 아님 · TREND 전용)
식: f = σ_eff/σ₀ · **tau2 = ε_e/f = ε_e·σ₀/σ_eff** · tau = √tau2 · Bruggeman tau2_B = ε_e^(−1/2) (COMSOL 관례 τ_F = ε^(−1/2)).  σ₀ = 5.4×10⁻⁴ S cm⁻¹ (Table S2).  ε_e · σ_eff = Table S3 (판독이면 표시).

| 전극 | ε_e | σ_eff (S cm⁻¹) | f | tau2 | tau | tau2 / tau2_B |
|---|---|---|---|---|---|---|
| 0D 250 | 0.135 | 5.69×10⁻⁷ | 1.05×10⁻³ | 128 | 11.3 | 47 |
| 0D 500 | 0.135 (가정) | ≈ 4.3×10⁻⁸ (판독) | ≈ 8×10⁻⁵ | ≈ 1.7×10³ | ≈ 41 | ≈ 620 |
| 1D 2500 (Table S3 값) | 0.135 | 8.58×10⁻⁷ | 1.59×10⁻³ | 85 | 9.2 | 31 |
| 1D 2500 (Fig. 4a 판독) | 0.135 | ≈ 8.4×10⁻⁶ | ≈ 0.016 | ≈ 8.7 | ≈ 2.9 | ≈ 3.2 |
| 1D 5000 | 0.135 | 1.19×10⁻⁵ | 0.022 | 6.1 | 2.5 | 2.3 |
| 1D 7500 | ≈ 0.13 (두께 +1 µm 환산, 가정) | ≈ 1.33×10⁻⁵ (판독) | ≈ 0.025 | ≈ 5.3 | ≈ 2.3 | ≈ 1.9 |
| 2D 2500 | 0.125 | 2.95×10⁻⁶ | 5.46×10⁻³ | 22.9 | 4.8 | 8.1 |
| 0D:1D 3:1 | 0.135 | 2.77×10⁻⁶ | 5.13×10⁻³ | 26.3 | 5.1 | 9.7 |
| 0D:1D 2:2 | 0.135 | 5.69×10⁻⁶ | 0.0105 | 12.8 | 3.6 | 4.7 |
| 0D:1D 1:3 (표에만) | 0.135 | 5.95×10⁻⁶ | 0.0110 | 12.2 | 3.5 | 4.5 |
| 70:30 0D:1D 2:2 | 0.095 | 2.43×10⁻⁶ | 4.50×10⁻³ | 21.1 | 4.6 | 6.5 |
| 70:30 0D 250 · 60:40 0D 1000 | — | 0 | 0 | ∞ → **N/A (비관통)** | — | — |

- 전자 쪽 (흑연, σ₀,s = 2.5 S cm⁻¹): tau2_s = ε_s·σ₀,s/σ_s,eff = **3.4** (Others) · 4.3 (2D 2500) · 2.9 (70:30) — Bruggeman ε_s^(−1/2) 의 2.1–2.9 배 (파생).
- 읽는 법:
  - ① 모든 tau2 > 1 — Wiener 상한 f ≤ ε 와 정합 (복셀 연속체 해의 성질).
  - ② 같은 ε_e = 0.135 에서 0D 250 → 1D 5000 으로 tau2 가 128 → 6.1 (**×21 감소**).
  - ③ Bruggeman 은 이 전극들을 2–47 배 (0D 500 은 수백 배) 과소평가한다.
  - ④ ⚠ **이 tau2 는 모형 T 다** — 단일 전도상 선형 Ohm 해라 σ_eff ∝ σ₀ 이고, **σ₀ (5.4×10⁻⁴) 는 tau2 에서 약분된다**.  tau2 는 이 복셀 구조 (해상도 · 겹침 규칙 포함) 만의 함수다.
  - ⑤ 1D 2500 은 표값과 그림값이 tau2 로 **10 배** 갈린다 → 인용 금지 (3-H ✗1).

### 3-H. 내부 정합 검사 (우리 산술) — 통과 셋 · 불일치 넷
| # | 검사 | 결과 |
|---|---|---|
| ✓1 | 부피 장부 ε_s + ε_e + 바인더 + 기공 = 1 | 0.492 + 0.135 + **0.073** + 0.30 = 1 → 바인더 부피분율 0.073 (파생) |
| ✓2 | 2D 2500 의 ε 가 두께 39 → 42 µm 로 희석되는가 | 0.135 × 39/42 = 0.1254 (표 0.125) · 0.492 × 39/42 = 0.457 (표 0.457) → 적재량 고정 · 기공 ≈ 35 % (파생) |
| ✓3 | 두 조성의 ε_s/ε_e 가 같은 밀도비를 주는가 | 60:40 → ρ_LLZO/ρ_흑연 ≈ 2.43 · 70:30 예측 ε_s/ε_e 5.67 vs 표 0.537/0.095 = 5.65 ✓ |
| ✗1 | 1D 2500 σ_e,eff | 표 **8.58×10⁻⁷** ↔ Fig. 4a **≈ 8.4×10⁻⁶** (한 자릿수 차).  지수 오기로 보인다 (판정 불가).  P2D 에 어느 값이 들어갔는지 [미확인].  추론 근거: 표의 a_s 는 1D 2500 (23133) 과 2D 2500 (23621) 이 거의 같다.  그런데 Fig. 4b 에서 1D 2500 (≈ 0.94) 이 2D 2500 (σ 2.95×10⁻⁶, ≈ 0.47) 을 이긴다 → 1D 2500 σ > 2.95×10⁻⁶ = 그림값 쪽과 정합 |
| ✗2 | 2D 2500 a_s | 표 **23621** ↔ Fig. 4a **≈ 1.20×10⁴**.  본문 (p.5) *"all electrodes with 2D solid electrolytes showed a relatively low specific contact area … than the electrodes with 1D"* 은 그림 쪽이다.  표값은 Fig. 4a 의 1D 7500 막대 (≈ 2.35×10⁴) 와 가깝다 (추론) |
| ✗3 | 혼합 a_s 라벨 | Fig. 6a 3:1 ≈ 5.95×10⁴ = 표 "1:3" 59580 · 표 "3:1" 37022 는 그림에 없다.  무게 선형 혼합 예측 3:1 58661 / 1:3 35785 (파생) → **표의 3:1 ↔ 1:3 이 뒤바뀐 것으로 보인다** |
| ✗4 | '1:3' 행 | 본문은 *"two blended solid electrolyte systems with 0D 250 nm:1D 5000 nm = 3:1 and 2:2"* 만 설계한다 (p.5).  Fig. 7 은 70:30 을 "0D:1D = 2:2" 로 적는데, 표의 70:30 σ_e,eff 는 "1:3" 라벨이고 같은 표의 70:30 σ_s,eff · ε · a_s 는 "2:2" 라벨이다 — 라벨 혼선 |
| (덧) | 본문 수치 | *"~2.0 × 10⁻⁶"* (p.6) ↔ 표 · 그림 2.4×10⁻⁶ · *"more than twenty times"* 는 1D 2500 에 안 맞는다 (3-D) |

## 4. 시뮬레이션 방법 ★

### 4.1 흐름 (p.2–3)
① SE 단독 상자 (50 µm) → 최단 퍼콜레이션 경로 (치수별 퍼콜 경향 확인) → ② 흑연 배치 (GrainGeo) → SE 채우기 (isolation distance −0.1 µm) → 겹침 재배정 → 바인더 코팅 → ③ PoroDict → specific contact area · ConductoDict → σ_eff → ④ COMSOL P2D 에 σ_eff · a_s · ε · 두께를 넣어 율특성 예측.
- 원문 3장 머리 (p.3): GeoDict 시뮬레이션은 *"i) building a 3D structure and ii) assigning the proper material properties to each entity"* 두 단계다.  *"For facile modeling, particles with large sizes are first positioned, and the rest of the space is filled with small particles"* · 물성은 *"the measured values from other reports"*.
- 적용 범위 주장 (p.3): *"this method is quite versatile because diverse electrode systems, including sulfide, oxide, polymer, and liquid electrolytes, can be predicted and evaluated by simply controlling the various parameters"* — 이 논문에서 검증된 것은 아니다.
- 산화물 계면 가정 (p.3): *"The poor conductivity at the interface of the solid oxide electrolytes and active materials was assumed to be improved by co-sintering the electrode at high temperature or covering each particle with a lithium-ion conducting coating comprising ductile electrolytes (sulfide or polymer) [35–38]."*

### 4.2 구조 생성 — GeoDict GrainGeo (p.2)
- **흑연**: ellipsoid convex polyhedral · Gaussian 크기 (Table S1) · 등방 방위 · overlap 허용 — *"this function is appropriate to reflect the form of compressed graphite particles in the electrode [15]"*.
- **SE**: 균일 크기 (종류당 하나) · 흑연 둘레의 빈 공간에 채움 · *"by overlap with an isolation distance −0.1 μm, which caused the LLZO-Ta particles to be positioned around the graphite particles and make good contact with them"*.  (우리 해석: 음의 격리 거리 = 최대 0.1 µm 겹침 허용 — GeoDict 설정의 정확한 의미는 원문 미기술.)  SE–SE 쌍에도 같은 규칙이 걸리는지는 원문이 따로 말하지 않는다 [미확인].
- **겹침 재배정**: 흑연–SE 겹침 부피 (전체의 < 0.5 %) → LLZO-Ta.  근거 = *"considering their relative strengths [18,19]"* ([18] 흑연 영률 · [19] LLZO 영률 — 값은 이 논문에 없다).
- **바인더**: *"Added Binder Function"* · 외벽 코팅 · *"under the assumption that there were no polymeric binders between particles that were in contact [20]"*.
- **SE 단독 상자**: 같은 50 µm 변 · SE vol% 함수 — 배치 규칙 (겹침 여부) 은 원문 미기술 [미확인].
- **방위**: 흑연 = 등방.  SE 1D · 2D 방위 규칙은 원문 미기술 (Fig. 1c 단면은 무작위로 보인다 — 판독).
- **실현 수 = 1 회** (반복 · seed · 평균 언급 없음).  원문 스스로 *"the quality of the percolation by specific solid electrolytes should be ideally analyzed with statistical methods to find its threshold [13,21]"* 라 적고 최단 경로로 대신한다 (p.3).

### 4.3 해상도 · 도메인 (p.2)
- 복셀 100 nm.  원문: *"it is essential to select the appropriate voxel size to obtain efficient and consistent simulation results"* — **수렴 시험 보고 없음**.
- **최소 치수 250 nm = 2.5 복셀**: 0D 250 구 · 1D 원기둥 지름 · 2D 판 두께가 전부 2.5 복셀이다.  고정 겹침 0.1 µm = 1 복셀.
- 겹침 ÷ 지름 δ/d (우리 산술): 0D 250 **0.40** · 0D 500 0.20 · 0D 1000 0.10 — 크기마다 상대 겹침이 4 배 다르다.
- 밑면 500 × 500 복셀 · 높이 = 충전 결과 (≈ 39 µm ≈ 390 복셀 · 2D 7500 은 ≈ 85 µm).

### 4.4 specific contact area — PoroDict (p.3)
- **정의 (원문)**: *"The specific contact area is defined by the contact area between the active materials and solid electrolytes per unit volume of all active materials, which represents the real interface where the electrochemical reaction can take place."*
- ⇒ **SCA = A_AM–SE / V_AM** [m⁻¹].  산출 알고리즘 (복셀 면 계수 · Minkowski 추정 등) 은 미기술 [미확인].
- 복셀 공유면이라면 구성상 AM 표면을 넘지 못한다 (우리 판단).
- ⚠ 같은 양의 SI 이름은 a_s *"specific surface area of electrode, m⁻¹"* (SI p.8) 다.  P2D 식에서 a_s 는 **전극 부피당** 반응면적 자리다 (SI p.4 Fig. S3: ∇(σ_s,eff∇φ_s) = a_s j).  → 본문 정의 (AM 부피당) 와 P2D 자리 (전극 부피당) 사이에 **분모 차 ε_s (≈ 0.49) 가 있을 수 있다**.  원문은 환산을 말하지 않는다 [미확인].

### 4.5 σ_eff — ConductoDict, Ohm 정상상태 (p.3 · SI p.3)
- 원문 (p.3): *"The effective ionic conductivity is the parameter that results from the intrinsic ionic conductivity, volume fraction, and tortuosity of solid electrolytes. That is, the effective ionic conductivity is proportional to both the intrinsic ionic conductivity and volume fraction but is inversely proportional to the tortuosity of the 3D electrodes."*
- 원문 (p.3): *"Notably, the effective conductivities were calculated from an ordinary differential equation of Ohm's law and boundary conditions without considering the space charge layer between electrode materials' phase or dispersed ionic conductors (Fig. S2 and Table S2) [15,17,22–24]."*
- **Fig. S2 그림 안 식** (SI p.3, 부호 · 아래첨자 없음, 글자 그대로): `Domain: j = (εσ/τ) ∇φ` · 캡션 *"Domain with governing equations and its boundary conditions (Ohm's law)"*.
- **경계조건 (SI p.3, 그림 안)**: φ|₊z = 1 · φ|₋z = 0 · φ|₊x = 1 · φ|₋x = 0 · φ|₊y = 1 · φ|₋y = 0 — **6 면 Dirichlet**.  형제 AEM 카드의 Fig S9 와 같은 그림이다.  세 방향 해를 겹쳐 그린 것인지, 보고한 σ_eff 가 어느 방향인지는 원문 미기술 [미확인].
- **입력** (Table S2): 이온 전도는 LLZO-Ta 하나 (5.4×10⁻⁴), 흑연 · 바인더는 이온 0 → **단일 전도상 선형 문제** (파생: σ_eff/σ₀ = 구조 상수).
- 전자 σ_eff: *"did not need to be considered in this electrode system due to the high electric conductivity and volume fraction of graphite"* (p.3).  그러나 Table S3 는 σ_s,eff 값을 싣는다 (계산했는지 미기술).
- 솔버 종류 (explicit jump 등) · 수렴 기준 미기술 [미확인] ("explicit jump" 낱말 없음).
- **"ion density tomography"** (Fig. 3c · S4c) = 같은 해의 전류밀도 크기 단면 (단위 mA cm⁻²) — σ_eff 가 장 (field) 해의 출력이라는 정황 (추론).  ⚠ **컬러바 눈금이 "1×10 · 8×10 · 6×10 · 4×10 · 2×10 · 0"** 이다 — 지수가 빠져 있어 절대값을 읽을 수 없다 (본문 그림 · SI 그림 모두).

### 4.6 퍼콜레이션 경로 (p.3)
- 원문: *"practically speaking, the level of well-formed percolation pathways can be confirmed by checking how close the shortest percolation pathway is to the side of the structure. As a result, these percolation properties directly or indirectly influence the specific contact area and effective ionic conductivity"* · *"under a condition looking for formed percolation pathways from a bottom plane to top plane of Z-axis (Fig. 1)"*.
- 경로 = SE 상 안의 최단 경로 (Fig. 1b 에 3D 곡선으로 그렸다).  산정 알고리즘 (복셀 이웃 규칙 · 거리 척도) 미기술 [미확인].
- 대상 = SE 단독 상자 (흑연 · 바인더 없음).  **복합 전극 안의 퍼콜레이션은 따로 세지 않았다** — 복합 전극에서는 σ_eff = 0 (70:30 0D) 으로만 비관통이 드러난다.

### 4.7 전기화학 — COMSOL 5.4 Batteries & Fuel Cells, Newman P2D (p.3 · SI p.4–5)
Fig. S3 식 전사 (SI p.4, 그림 안 글자 그대로 · 기호는 원문):
- 셀: Composite Anode | Li₂S-P₂S₅ Pellet | Li Metal.
- 경계: 집전체 쪽 −σ_s,eff ∂φ_s/∂x = I/A, ∇c_e = 0, ∇φ_e = 0 · 음극/펠릿 경계 −σ_s,eff ∂φ_s/∂x = 0 · Li 금속 φ_s = 0, ∇c_e = 0, ∇φ_e = 0.
- 입자: ∂c_s/∂r|_(r=0) = 0 · D_s ∂c_s/∂r|_(r=Rs) = j/F · ∂c_s/∂t = ∇(D_s∇c_s).
- 반응: η = φ_s − φ_e − E_eq · j = i₀(exp(α_aFη/RT) − exp(−α_cFη/RT)) · "At surface of active materials" i₀ = Fk(c_s,max − c_s)^0.5 (c_s)^0.5 (c_e/c_e,ref)^0.5.
- 전해질 물질 수지: ε_e ∂c_e/∂t + ∇(−D_e,eff∇c_e + t₊(−σ_e,eff∇φ_e + (2σ_e,eff RT/F)(1−t₊)∇ln c_e)/F) = a_s j/F.
- 전해질 전하: ∇(−σ_e,eff∇φ_e + (2σ_e,eff RT/F)(1−t₊)∇ln c_e) = a_s j · 고체: ∇(σ_s,eff∇φ_s) = a_s j.
- 원문 (p.3): *"Key parameters obtained through the 3D structural analysis were applied to this battery model"* · SEI · 덴드라이트 등 부반응 없음 · 매개변수는 *"real measurements or previous works (Table S3) [15,17,25]"*.
- ⚠ 미기술 [미확인]:
  - COMSOL 유효 수송 보정 설정 (No correction · Bruggeman · Tortuosity)
  - D_e,eff 와 D_e 의 관계 (표는 D_e 만 준다)
  - i₀ 를 표값 10 A m⁻² 로 고정했는지, k 식으로 계산했는지
  - 차단전압
- (우리 산술) 이온 저항 감각 — L_n/σ_eff 직렬 근사:
  - 0D 250: 39 µm ÷ 5.69×10⁻⁷ S cm⁻¹ ≈ 6.9×10³ Ω cm²
  - 1D 5000: 39 µm ÷ 1.19×10⁻⁵ ≈ 3.3×10² Ω cm²
  - LPS 펠릿: 1 mm ÷ 1.81×10⁻³ ≈ 55 Ω cm²
  - 0D 전극은 0.12 mA cm⁻² 에서도 ≈ 0.8 V 가 떨어진다 → 용량이 거의 안 나오는 것과 정합.

### 4.8 입자 처리 ★ (DEM 양식 항목)
- **강체 · 복셀 형상** (구 · 원기둥 · 정사각 판 · 볼록 다면체 흑연).  변형 없음 — **접촉 소성도 형상 소성도 없다**.  접촉 = 배치 단계의 **기하 겹침 (≤ 0.1 µm) → 복셀 융합**.
- PSD: SE = 종류당 단일 크기 (mono) · 흑연 = Gaussian (평균 15 × 10 × 10 µm, SD 5 µm) · 혼합 = 0D 250 + 1D 5000 두 형상.
- **압밀 없음** — 기공 30 % 는 배치 목표 (두께로 맞춤) 이고 압력 축이 없다.  '강성' (LLZO) 은 역학 계산이 아니라 겹침 재배정 규칙과 2D 충전 실패의 해석에만 나온다.

### 4.9 기법 미니 용어집
- **GeoDict** (Math2Market, 독일) — 복셀 기반 미세구조 생성 · 해석 상용 패키지.  **GrainGeo** = 입자 배치 모듈 · **PoroDict** = 기공 · 면적 · 경로 해석 모듈 · **ConductoDict** = 유효 전도도 (Ohm/Laplace) 해석 모듈.
- **isolation distance** — GeoDict 배치 규칙의 입자 간 거리 매개변수.  음수 = 겹침 허용 (우리 해석).
- **Added Binder Function** — 입자 외벽에 바인더 층을 덧입히는 GeoDict 기능 [20].
- **specific contact area** — 이 논문에서는 AM–SE 접촉면적 ÷ 전 AM 부피 (m⁻¹).
- **shortest percolation pathway** — 이 논문에서는 상자 바닥 → 위 SE 경로 가운데 가장 짧은 것의 길이 (0 = 비관통).
- **ion density tomography** — 이 논문에서는 ConductoDict 해의 전류밀도 크기 단면도 (mA cm⁻²).
- **P2D (Newman)** — 전극 두께 x 와 입자 반경 r 두 좌표의 균질화 전지 모형.  미세구조는 σ_eff · ε · a_s · 두께로만 들어간다.
- **dimension-controlled SE** — 형상 차원을 0D (구) · 1D (섬유형 원기둥) · 2D (판형) 로 바꾼 SE.
- **co-sintering** — 산화물 SE 와 활물질을 고온에서 함께 소결해 계면을 잇는 공정 (이 논문은 그것을 가정만 한다).

## 5. Figure set ★
| Fig (쪽) | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 (p.4) | (a) SE vol% vs 최단 퍼콜 경로 길이 (0D 250 · 1D 2500 · 2D 2500) + 상자 변 50 µm 선 · (b) 3D 구조 (1D 10 % · 2D 20 % · 0D 25 %) 와 경로 77 · 50 · 83 µm · (c) 20 vol% 단면 0D vs 1D | 퍼콜 판정과 τ_geo 의 **다른 정의** (최솟값 · SE 단독 · 단일 실현) — 우리 `percolation_pct` · `tortuosity_SE_wall` 과 대조 (§8) |
| 2 (p.4) | (a) 1D/2D 길이 · 폭 vs 전극 두께 (0D 기준선) · (b) 2D 7500 전극 3D + 단면 (흑연 · LLZO-Ta · SBR/CMC) | 강체 이방 입자의 충전 한계 (배치 결과) — 우리 '강체는 소성 흐름 없이 조밀해지지 않는다' 와 같은 방향 (정성) |
| 3 (p.5) | 1D 2500 vs 2D 2500 전극 (60:40): (a) 3D (b) 단면 (c) ion density 단면 | 전류 경로 가시화 — 컬러바 지수 누락 |
| 4 (p.6) | (a) 1D/2D 여섯 전극 SCA · σ_eff 막대 · (b) 0D 250 · 1D 2500 · 2D 2500 의 0.1/0.3/0.5 C 전압 곡선 | ★ 치수 축 핵심 수치 (Table S3 와 불일치 2 건) |
| 5 (p.7) | 0D 250 · 0D:1D 2:2 · 1D 5000 전극 단면 + 확대 | 혼합 형상 시각화 |
| 6 (p.7) | (a) 혼합 SCA · σ_eff · (b) 용량 유지율 vs C-rate | 혼합 = 선형 평균 경향 · 2:2 ≈ 1D 단독 성능 |
| 7 (p.8) | (a) 60:40 vs 70:30 (0D · 0D:1D 2:2) SCA · σ_eff · (b) 0.12 · 0.36 · 0.60 mA cm⁻² 전압 곡선 | 70:30 0D = 비관통 (σ = 0) — SE 13.5 → 9.5 vol% 사이의 문턱 |
| S1 + Table S1 (SI p.2) | 치수 제어 SE 모식 (0D 지름 · 1D 길이 · 2D 폭) + 방향 화살표 ("Particle-like Direction", "Poor Ion Pathway Direction", "Low Electrode Density Direction") · 흑연 Gaussian 조건 | 설계 축 · 구조 재현 |
| S2 + Table S2 (SI p.3) | ★ **j = (εσ/τ)∇φ** + 6 면 Dirichlet + 고유 전도도 표 | **τ 관례의 원문 근거 · σ₀** |
| S3 + Table S3 (SI p.4–5) | ★ P2D 식 · 경계조건 + 전 매개변수 (σ_e,eff · ε · a_s 포함) | 수치 원천 (불일치 주의) |
| S4 (SI p.6) | 0D 250 · 500 · 1000 전극 3D · 단면 · ion density (1000 nm = 0) | 입경 ↑ → 이온 경로 소멸 |
| S5 (SI p.7) | ★ 0D 지름 vs SCA · σ_eff | 치수 축 (0D) — 250 → 500 nm 급락 |
| S6 (SI p.7) | 부피 용량 기준 전압 곡선 | 두께 효과 확인 |
| S7 (SI p.8) | 1D 5000 전극에 0D 500 · 1D 5000 추가 충전 (목표 vs 실제 vol%) | 혼합 충전 여유 (≈ 17 vs ≈ 1 vol%) |

## 6. Post-processing ★
- **무엇**: 최단 퍼콜레이션 경로 길이 (SE 단독 상자) · specific contact area (PoroDict) · σ_eff (ConductoDict, Ohm) · 전류밀도 단면 (ion density tomography) · P2D 전압 곡선 → 용량 유지율.
- **도구**: GeoDict (판 미기재) · COMSOL Multiphysics 5.4 (Batteries & Fuel Cells).
- **수치화 · 보고**: 막대 (SCA 왼축 · σ_eff 오른축) · 꺾은선 (퍼콜 경로 · 두께 · 유지율) · P2D 입력값은 SI Table S3.
- **보고하지 않는 것**: τ 값 · 퍼콜 분율 · 고립 입자 비율 · 배위수 · 반복 실현 통계 — 하나도 없다.

---

## § τ 정의 대조 — 우리 규약 매핑

### (1) 원문이 말하는 것 / 말하지 않는 것
| 항목 | 원문 | 위치 | 판정 |
|---|---|---|---|
| 관계식 | j = (εσ/τ)∇φ — 그림 안 식 하나 (아래첨자 · 부호 없음) | SI p.3 Fig. S2 | τ 는 **1 제곱**으로 분모에 있다 (τ² 아님) |
| σ_eff 서술 | *"results from the intrinsic ionic conductivity, volume fraction, and tortuosity … proportional to both the intrinsic ionic conductivity and volume fraction but … inversely proportional to the tortuosity"* | p.3 | ⇒ σ_eff = ε·σ₀/τ (대수) |
| ε | ε_e *"volume fraction of electrolyte"* · ε_s *"volume fraction of active material"* (값 0.135 · 0.492 등) | SI p.9 · SI p.4–5 | 전극 전체 (기공 · 바인더 포함) 대비 — 부피 장부로 확인 (3-H ✓1) |
| τ 이름 · 정의 · 값 | 산문 "tortuosity" 4 회 (p.3 세 번 · p.5 한 번, 전부 정성) · Nomenclature 에 **τ 없음** · 값 없음 · "tortuosity factor" 0 회 · "Bruggeman" 0 회 | 전문 검색 | **정의 없음** |
| τ 산출법 | — | — | **미기술** (형제 AEM 카드와 같다) |
| 정규화 단면 | 명시 없음 | — | 전체 단면으로 읽는다 (추론: 식에 ε 가 있다 = 겉보기 플럭스 관례 · P2D 의 σ_e,eff 자리) |
| 방향 | 6 면 Dirichlet 그림 | SI p.3 | 보고 σ_eff 의 방향 미기술 |
| σ₀ | LLZO-Ta 이온 5.4×10⁻⁴ S cm⁻¹ [17] (상수) · 흑연 전자 2.5 S cm⁻¹ [15] | SI p.3 Table S2 ("Intrinsic …") | 문헌 입력값 — 펠릿 · 소결체 · 결정립 중 무엇인지 원문 미기술 [미확인] |
| 계면 | *"without considering the space charge layer between electrode materials' phase or dispersed ionic conductors"* · 산화물–AM 계면은 공소결 · 코팅으로 양호하다고 가정 | p.3 (두 곳) | **계면 저항 항 0** — CONTACT_FREE 부류 |
| Nomenclature 단위 | κ *"ionic conductivity, mS cm⁻¹"* · σ *"electric conductivity of electrode, mS cm⁻¹"* | SI p.10 | 표 (S cm⁻¹) · 그림 기호 (σ) 와 어긋난다 — 명명표 자체가 정의 근거가 못 된다 |

### (2) 매핑표 — 이 논문 ↔ 우리 다섯 양
| 우리 양 | 우리 식 · 키 | 이 논문에서 | 같은 양인가 | 환산 · 조건 |
|---|---|---|---|---|
| **f** | σ_eff/σ₀ · `f_ion_<mode>` | εσ/τ 의 무차원부 (이름 없음) = σ_e,eff (Table S3) ÷ 5.4×10⁻⁴ | 정의식 같음 | f = σ_e,eff/σ₀ (3-G) · 절대 비교는 σ₀ 를 맞춘 뒤 |
| **tau2** | φσ₀/σ_eff · `tau2_ion_<mode>` | **τ** (Fig. S2 의 τ) | **정의식 같음** (대수) | τ = ε_e·σ₀/σ_e,eff.  ε_e = 복셀 합집합 부피분율 ↔ 우리 φ = 구 부피 합 (겹침 이중계상) — 겹침만큼 다르다.  이 논문 τ 는 **계면 저항 0 · 복셀 융합 접촉** 위의 값 → 우리 FULL (Holm 직렬) 이 아니라 **STEP3 복셀 · CF 쪽 부류** |
| **tau** | √tau2 · `tau_ion_<mode>` | 없음 | — | 3-G 의 tau 열은 우리 산술 |
| **τ_geo** | 최단 경로 / 두께 · `tau_geo_SE_dij` (배포 키 `tortuosity_SE_wall`) | "length of shortest percolation pathway" ÷ 상자 변 (원문은 길이만 · 비는 우리 산술) | **범주 같음 (기하) · 통계 다름** | 이 논문 = SE **단독** 상자 · 복셀 SE 합집합 안의 **최단 하나** (분포의 최솟값) · 단일 실현.  우리 = 복합 전극 · SE **중심 꺾은선** · 무작위 200 쌍 **평균** ÷ Δz.  같은 구조라도 두 차이 모두 우리 값을 크게 만든다 |
| **τ_e** | (우리에 없음) | 없음 — P2D 에 관통형 σ_eff 를 그대로 넣는다 | — | Nguyen 2020 이 P2D 에는 τ_e 를 권하는 자리 (형제 카드 `nguyen2020_electrode_tortuosity_factor`) — 이 논문에는 그 구분이 없다 |

- **이름 규칙 적용**: 우리 문서에서는 "Park CEJ 2020 의 τ (= tau2 자리 · 원문 이름 'tortuosity' · 값 미보고)" 로 부른다.  'tortuosity factor' 는 원문에 없는 이름이라 원문 인용에 붙이지 않는다.
- **σ₀ 기준 한 줄**: σ₀ = **문헌 고유값 입력** (LLZO-Ta 5.4×10⁻⁴ S cm⁻¹ = 0.54 mS cm⁻¹).  순수 SE 펠릿을 τ² ≡ 1 로 두는 Minnmann 관례도, 우리 펠릿값 3.0 (CL-91) 도 아니다.  ⚠ 이 논문은 실험이 없어 σ₀ 가 τ (모형) 에서 약분된다 → σ₀ 차이는 **절대 σ_eff** 비교에서만 문제가 된다 (우리 3.0 vs 0.54 = 5.6 배).

### (3) 형제 카드 (AEM 2020) 의 열린 질문 — 이 원문이 답하는가
| 질문 (형제 카드 §4-T · §5 · §13) | AEM 카드 상태 | 이 논문 (CEJ) | 판정 |
|---|---|---|---|
| τ 산출법 (해에서 역산 vs 따로 계산한 τ 대입) | 미기술 [미확인] | 미기술 — τ 정의 · 값 · 명명표 항목 없음.  σ_eff 를 *"calculated from an ordinary differential equation of Ohm's law and boundary conditions"* (p.3) 로 적고 전류밀도 단면 (Fig. 3c · S4c) 을 보인다 = σ_eff 는 장 해의 출력이라는 정황 (추론).  계산 문장의 인용 = [15,17,22–24] | **닫히지 않음** — 남은 후보 [15] = [12a] (Park 2019 ESM, 같은 묶음 형제 카드) |
| 경계조건 · 방향 | 6 면 Dirichlet 그림 · 방향 미기술 | 같은 6 면 그림 (SI p.3) · 방향 미기술 (퍼콜 경로만 "Z-axis", p.3) | **닫히지 않음** (같은 그림의 원전 확인뿐) |
| σ₀ 규약 | LPSCl 조성 의존식 (AEM Table S1) | LLZO-Ta **상수** 5.4×10⁻⁴ [17] | AEM 의 조성식은 [12b] 에서 **오지 않았다**.  그룹 관례는 "재료별 문헌 고유값 입력" 이고 AEM 이 그것을 조성식으로 바꿨다 |
| 계면 · 접촉 저항 항 | "언급되지 않는다 → CF 쪽 (추론)" | **명시**: 공간전하층 미고려 · 계면은 공소결 · 코팅으로 양호하다고 가정 (p.3) | 이 논문에 한해 **닫힘** (계면 항 0).  AEM 이 같은 설정인지는 여전히 추론 |
| 접촉면적 분모 | 미기술 [미확인] | ***"per unit volume of all active materials"*** (p.3) | 이 논문에 한해 **닫힘**.  같은 그룹 · 같은 모듈이라 AEM 도 같을 개연성 (추론).  단 SI 명명 · P2D 자리와 분모가 어긋날 수 있다 (4.4) |
| τ 수치 ("역산 대신 원값") | 없음 (우리 역산만) | **없음** (σ_eff 만 — 3-G 는 우리 역산) | **불가** |

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> ⚠ `our_dem_baseline.md` 는 정본 브랜치에서 **자리표시** (값 0 개) 다.  아래 '우리' 칸의 수는 메인 리포 CLAUDE.md 와 판단 메모 v2 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`, 유도값 표지 그대로) 에서 가져왔다.
> **frame[5]**: 이 논문은 **수송 반쪽** (σ_eff · 퍼콜레이션 · 접촉면적) 만, 그것도 **연속체 복셀** 이산화로 가진다.  DEM 의 접촉망 (접촉당 Holm) 도, MPM 의 역학 (압밀 · 소성 흐름 · 응력) 도 없다.  구조는 압밀이 아니라 **확률 배치 (겹침 허용)** 다.
> **frame[4]**: 실험이 없으므로 이 논문은 어느 쪽 모델의 보정 앵커도 아니다 — 우리 모델을 여기에 맞추지 않는다.

| 항목 | 이 논문 | 우리 | 같은 점 / 다른 점 · 이유 |
|---|---|---|---|
| SE | LLZO-Ta (garnet 산화물, 강체 취급) · σ₀ 0.54 mS cm⁻¹ (문헌) | LPSCl (황화물, 연성) · σ₀ 3.0 mS cm⁻¹ (펠릿, CL-91) | 재료 이전 불가 — 기하 · 퍼콜 경향만 |
| AM | 흑연 음극 (볼록 다면체, 15 × 10 × 10 µm Gaussian, σ_e 2.5 S cm⁻¹) | NCM811 양극 (구, AM_P · AM_S) | 전자 경로 비제한이 그들에겐 자동 · 우리는 아니다 |
| SE 부피분율 | ε_e 0.135 (60:40 wt%) · 0.095 (70:30 wt%) — **38 wt% 인데 13.5 vol%** (LLZO 밀도 ≈ 흑연의 2.4 배, 3-H ✓3) | φ_SE ≈ 0.25–0.69 (메모 v2 §3-3 띠) | **wt% 로 비교 금지** — vol% 로만 |
| 입경비 | d_SE/d_흑연 ≈ 0.022 · 0.044 · 0.087 (0D 250 · 500 · 1000) — 흑연 등가구 지름 (15·10·10)^(1/3) ≈ 11.4 µm (파생) | r_SE/r_AM ≈ 0.13 (메모 v2 §0-1 ④) — SE 적은 두 띠 중앙 0.133 · 0.125, 범위 0.10–0.47 (§3-8 ① · case_master) · LHS 설계 열 `size_ratio_AM_over_SE` | 그들이 실패한 입경 (1000 nm, 비 0.087) 도 우리 중앙보다 작은 비다.  그러나 SE 부피가 훨씬 적어 같은 문턱이 아니다 |
| 구조 생성 | GeoDict 확률 배치 · 겹침 −0.1 µm 고정 · 압력 축 없음 | LIGGGHTS 압밀 (예: 300 MPa) · 연화 접촉 (E_eff 1.35 GPa) 이 겹침 δ 를 정한다 | 그들 겹침 = 생성 매개변수 (δ/d 0.1–0.4 가 크기마다 다름) · 우리 겹침 = 역학 결과 |
| 접촉 저항 | 0 (융합 복셀 · 공간전하 미고려 명시) | FULL = SE–SE Holm R_c = 1/(2σa) 직렬 (c_cpl[22] 교차 원판) · CF = R_c 0 | 그들 = 우리 **CF · STEP3 복셀 부류** (CL-81).  단 복셀 해는 **목 기하를 복셀 해상도만큼 담는다** → 원기둥 πr² 로 과전도하는 우리 망 CF (메모 v2 §3-6) 와 같은 '협착 0' 이 아니다 |
| σ 솔버 | ConductoDict 복셀 FV (Ohm), 6 면 Dirichlet 그림 | Kirchhoff 접촉망 (z 관통 · 띠 Dirichlet) · STEP3 복셀 FV (MPM 킷) | 이산화가 다르다 · 우리 STEP3 와는 같은 종류 |
| τ 보고 | 없음 (σ_eff 만) — 역산 tau2 6–128 (1D 5000 ~ 0D 250, 3-G) | tau2 — 코퍼스 T_H 중앙 6.21 (메모 v2 §1, 유도) | 범위가 겹치는 것은 우연이다 — φ · 재료 · 이산화 · 계면 항이 전부 다르다 → **나란히 두지 말 것** |
| 퍼콜레이션 | SE 단독 상자 최단 경로 길이 (0 = 없음) · 단일 실현 | `percolation_pct` (밴드 규칙 그래프 관통 SE 분율) · `NOT_PERCOLATING` (결정 2) · `ionic_active_pct` | 그들은 '있다/없다 + 최단 길이' 만 준다 · 분율이 없다 · 복합 전극에서는 세지 않았다 |
| τ_geo | 최단 경로 / 상자 변 (우리 산술) 1.00–1.66 | `tortuosity_SE_wall` LHS 1.29–4.15 (130 중 관통 106) · lhsx 1.26–1.60 (CLAUDE.md J20-n) | 통계 (최솟값 vs 쌍 평균) · 경로 (복셀 측지선 vs 중심 꺾은선) · 구조 (SE 단독 vs 복합) 가 다르다 — 범위 겹침은 비교 근거가 못 된다 |
| AM–SE 접촉면적 | SCA = A/V_AM [m⁻¹] — 0D 250 70099 → 1D ≈ 2.3–2.4×10⁴ → 2D 2500 ≈ 1.2×10⁴ (그림) | `coverage_AM_*_hertz_pct` = c_cpl[22] 교차 원판 합 / AM 표면 (입자 평균, J20-m 기하면적) · `area_*_n` 개수 | **분모가 다르다** (AM 부피 vs AM 표면) — 환산식은 §8 (c).  그들 면적은 복셀 공유면 (구성상 ≤ AM 표면, 우리 판단) · 우리 접촉별 합은 LHS-25 표면 한도 문제를 가진다 |
| σ₀ 와 T | 모형 안에서 약분 (단일 상 선형) | 약분 (메모 v2 §3-1) | 같은 성질 — 둘 다 '모형 T' |
| 실현 · 통계 | 1 회 | LHS 130 + 64 침대 | — |
| 실험 | 없음 | 절대 T 대조는 결정 4 (순수 SE 게이트) 전 HOLD | 둘 다 실험 앵커가 없다 — 대조는 정의 · 추세까지 |
| 전기화학 | COMSOL P2D (σ_eff · a_s · ε 입력) | STEP4 (BV 반응분포 · 시간전개) | 영역 밖 — 참고만 |

- ★ **같은 방향 (정성)**: 작은 SE → 접촉면적 ↑ · 퍼콜 ↑ · σ ↑ (Bazzoun Fig. 7 · 우리 size = packing 결론과 같은 방향).  SE 부피 ↓ → 문턱 근처에서 σ 붕괴 (70:30 0D = 0) — 우리 `NOT_PERCOLATING` 침대 (LHS 130 중 24) 와 같은 현상 부류.
- ★ **우리가 못 하는 것**: SE **형상 이방성** (1D · 2D SE) — DEM 은 구만 쓴다.  우리 계에서 SE 를 길게 잇는 기구는 합성 형상이 아니라 **MPM 의 소성 흐름** (SE 다리) 쪽 질문이다 (frame[5]).
- ★ **그들이 못 하는 것**: 압밀 (압력 → 구조) · 접촉당 협착 저항 · 소성 형상 변화 · 반복 실현 통계.

## 8. 적용 인사이트 (내 연구에 어떻게)

### SE 입자 치수 ↔ percolation pathway · specific contact area · σ_eff
- **(a) 가상 전극 (디지털 트윈) 생성** — GeoDict GrainGeo 확률 배치.
  - 큰 입자 (흑연) 먼저, 작은 입자 (SE) 나중이다.
  - SE 는 isolation distance −0.1 µm (겹침 허용) 로 흑연 둘레에 붙인다.
  - 흑연–SE 겹침은 LLZO 로 재배정하고, 바인더는 외벽 코팅이다.
  - 복셀 100 nm · 단일 실현이다.
  - 우리와의 차이: 압력이 구조를 정하지 않는다 (배치 목표 기공 30 %) · 겹침은 생성 매개변수다 (우리는 DEM 역학 결과) · 최소 치수가 2.5 복셀이다.
- **(b) τ** — 정의 · 값이 없다.  Fig. S2 식의 대수로 τ = εσ₀/σ_eff = **tau2 자리**이고 원문 이름은 "tortuosity" 다.  단일 상 선형 해라 σ₀ 가 약분된다 → **복셀 융합 · 계면 0 구조의 모형 T**.  우리 쪽 비교 상대는 FULL 망 T 가 아니라 **STEP3 복셀 T** (CONTACT_FREE 부류) 다.  역산값은 3-G.
- **(c) 접촉면적 — 계산 · 정규화**.
  - 이 논문: SCA = A_AM–SE / V_AM [m⁻¹] (p.3).  알고리즘은 미기술이다.
  - 우리 `coverage_AM_*` = 상별 AM 입자 평균 (접촉 원판 합 / 입자 표면) [%].
  - **환산식** (우리 유도 · 구 · 상 안 반지름 단일): SCA_ours = 3·Σ_phase (c̄_phase · N_phase · r_phase²) / Σ_phase (N_phase · r_phase³).  단상 mono 이면 SCA = 3c̄/r.
  - 반대로 Park SCA 를 피복률로 바꾸면 (흑연을 등가구 r ≈ 5.7 µm 로 근사, 우리 산술 · 상한 쪽 — 실제 다면체는 S/V 가 더 크고 복셀 계단은 면적을 부풀린다):
    - 0D 250: **≈ 13 %** (본문 정의 = AM 부피당으로 읽을 때) · ≈ 27 % (P2D 자리 = 전극 부피당으로 읽을 때)
    - 1D: ≈ 4–5 % (또는 ≈ 9 %)
  - ⇒ 절대 비교는 모양 인자 · 분모 · 방법 (복셀 공유면 vs c_cpl[22] 교차 원판) 이 맞을 때만 가능하다.  지금은 **정의 대응까지**.
- **(d) 퍼콜레이션**.
  - 이 논문 판정 = SE 단독 상자의 최단 경로 길이 0/≠0 (단일 실현).
  - 우리 대응 = `percolation_pct = 0` ↔ `NOT_PERCOLATING` (결정 2) — '있다/없다' 만 대응한다.  관통 분율 · 활성 AM 은 대응이 없다.
  - 관통 시작 (판독): 1D 5–10 · 2D 10–15 · 0D 20–25 vol%.
  - 복합 전극 안 SE 를 흑연이 아닌 부피로 나누면 (우리 산술): 60:40 **26.6 %** (관통 · σ 5.7×10⁻⁷) · 70:30 **20.5 %** (비관통 · σ 0).  바인더 부피까지 빼면 31 · 24 % 다.
  - 이것은 SE 단독 상자의 0D 문턱 (20–25 %) 과 **정성적으로 정합**한다.  단 단독 상자 문턱을 흑연 · 바인더가 있는 공간에 옮긴 것은 우리 근사다.
- **(e) 우리 LHS 인계 열과 직접 비교 가능한가**:
  | 우리 열 | 이 논문 대응 | 판정 |
  |---|---|---|
  | `size_ratio_AM_over_SE` (설계) | 0D 지름 ÷ 흑연 크기 (흑연은 비구형 Gaussian) | ◐ 역수 · 등가구 환산이 필요하다.  1D · 2D 는 '크기' 하나로 안 접힌다 |
  | `coverage_AM_*_hertz_pct` (AM–SE 면적) | SCA (AM 부피당) | ◐ 분모 · 방법 · 모양 인자 환산 뒤에만 |
  | `percolation_pct` · 관통 플래그 | 최단 경로 0/≠0 (SE 단독 상자) | ◐ 이진 판정만 · 구조 (단독 vs 복합) 가 다르다 |
  | `tortuosity_SE_wall` (τ_geo) | 최단 경로 ÷ 50 µm (우리 산술) | ✗ 통계 (최솟값 vs 쌍 평균) · 경로 정의 · 구조가 다르다 |
  | `tau2_ion_<mode>` (예정) | τ = εσ₀/σ_eff (대수, 미보고) | ◐ 정의식은 같다.  계면 항 0 · 복셀 이산화라 비교 상대는 STEP3 복셀 T |
- **(f) 보고 수치 전수** → §3 (3-B 퍼콜 · 3-C 두께 · 3-D SCA · σ_eff · 3-E 성능 · 3-F 표 전사 · 3-G 파생 · 3-H 정합 검사).
- **(g) σ₀ 규약** → LLZO-Ta 5.4×10⁻⁴ S cm⁻¹ 문헌 상수 · 모형 T 에서 약분 (§ τ 정의 대조 (2)).

### ★ 판단 메모 v2 §3-4 — Park σ₀ 규약 · "추세 전용" 한정어
- §3-4 는 AEM 2020 (NCM/LPSCl, 실험 σ_eff 역산) 의 표다.  이 CEJ 는 AEM SI Fig S9 식의 인용원 [12b] 이지만 **σ₀ 조성식의 출처가 아니다** (LLZO-Ta 상수 5.4×10⁻⁴ [17]).  ⇒ §3-4 의 "Park 의 σ₀ 는 측정 펠릿이 아니라 조성 의존 모형 입력" 은 AEM 에 한해 그대로 선다.  그룹 관례 자체는 "재료 문헌 고유값 입력" 이다.
- **"추세 전용" 은 유지하고 근거를 보탠다**:
  - (i) [12b] 에도 τ 값 · 산출법이 없다.
  - (ii) 그룹의 σ_eff 계산은 계면 항 0 · 복셀 융합 (CF 부류) 이라 우리 FULL T 와 부류가 다르다.
  - (iii) 해상도 2.5 복셀 · 단일 실현 · 표 불일치가 있다.
  - (iv) [12b] 자체는 실험이 0 건이다.
- 덧: 이 CEJ 의 역산 tau2 (3-G) 는 실험값이 아니라 **모형값**이라 σ₀ 에 무관하다.  AEM 역산 (실험 σ_eff ÷ 가정 σ₀) 과 성격이 다르다 — 메모 v2 §3-1 의 "비대칭" 이 여기엔 없다.  ⛔ 3-G 의 수를 Minnmann · AEM 역산값과 한 표에 섞지 않는다.

### ★ 결정 16 (메모 v2 §0-2) 에 주는 인사이트
| 결정 | 인사이트 | 권고를 바꾸나 |
|---|---|---|
| **11** (CF 지위 · 복셀 ÷ 망 대조) | 문헌의 복셀 σ (GeoDict 류) 는 '계면 항 0' 이지만 **목 기하는 복셀로 담는다**.  2.5 복셀 · 고정 겹침 1 복셀이면 목 크기가 해상도와 생성 규칙에 묶인다.  우리 망 CF (원기둥 πr², 목 없음 · 과전도) 와 같은 '협착 0' 으로 읽으면 안 된다.  ⇒ 복셀 ÷ 망 대조 사전등록에 **a/dx (목 반경 ÷ 복셀) · δ/d (겹침 ÷ 지름)** 를 공변량으로 넣을 근거 | **no** (사전등록 항목 보강) |
| **5** (COMSOL 표기) · **13** (τ_e) | 이 그룹은 τ 가 아니라 **σ_eff 자체** 를 P2D 에 넣었다 (Table S3).  √T/T 거듭제곱 함정은 피하지만, COMSOL 보정 설정과 D_e,eff 관계를 적지 않아 이중 보정 여부를 판정할 수 없다.  또 문턱 근처 전극 (0D 250: 고립 입자 다수, Fig. 1c · S4c) 에 관통형 σ_eff 를 그대로 넣었다 = Nguyen 이 τ_e 를 권한 자리 | **no** — 결정 5 에 "σ_eff (또는 f) 를 넘길 때 보정 설정 = No correction 명기" 한 줄 보강 · 결정 13 의 "P2D 입력 열 보류" 를 지지 |
| **9** (LHS-25) · **15** (메타) | 복셀 공유면 접촉면적은 구성상 AM 표면을 넘지 못한다 → 결정 9 ③ "구성상 ≤ 100 %" 검사와 같은 방향이다.  단 분모가 한 논문 안에서도 흔들린다 (본문 AM 부피당 ↔ SI 명명 '전극 비표면적' ↔ P2D 전극 부피당).  ⇒ AM–SE 면적 열에 **분모 메타 (AM 표면 · AM 부피 · 전극 부피)** 를 단다 | **no** (메타 키 보강) |
| **4** (순수 SE 게이트) | 이 논문 tau2 에도 순수 SE 기준 상태가 없다 (SE 단독 상자는 퍼콜 길이만, σ 미계산) → 정규화 대조 불가 | **no** |

### 그 밖의 인사이트
- ① 접촉면적과 σ_eff 는 **반대로** 움직일 수 있다 — 0D 250 → 1D 에서 SCA ×0.33 · σ ×15–23, 0D 500 ≈ 1D 5000 SCA 인데 σ 는 ×≈280.  ⇒ 인계 열에서 coverage 와 tau2 를 하나로 접지 않는다 (ML 기술자는 둘 다 쓴다).
- ② **wt% → vol% 함정**: 산화물 38 wt% = 13.5 vol%.  우리 문서에 문헌 조성을 옮길 때는 늘 vol% (전극 전체 대비) 로 옮긴다.
- ③ 강체 이방 입자의 충전 한계 (2D 7500 → 두께 2.2 배) 는 우리 '강체는 소성 흐름 없이 조밀해지지 않는다' (frame[1]/[2]) 와 같은 방향의 정성 근거다 — 단 배치 알고리즘의 결과이지 역학이 아니다.  원문도 해법으로 *"a mechanically deformable 2D sulfide solid electrolyte"* 를 든다 (p.5).
- ④ 퍼콜 판정을 '최단 경로 = 0' 하나로 하면 문턱 근처에서 단일 실현의 운에 좌우된다 (원문도 인정, p.3).  우리 결정 2 한정어 "문턱 근처의 관통 여부는 상자 크기의 실현값 — 재료 성질 아님" 과 같은 경고다.

## 9. 인용 가능 문장 (deck/paper용)
- "In voxel-based virtual electrodes (GeoDict) of graphite with garnet LLZO-Ta at a fixed 13.5 vol% solid electrolyte, Park et al. (Chem. Eng. J. 2020) report that elongating the electrolyte from 250-nm spheres to 250-nm-diameter, 2.5–7.5-µm cylinders lowers the graphite–electrolyte specific contact area to about one third while raising the simulated effective ionic conductivity by roughly 15–23×."
- "Their effective conductivity follows j = (εσ/τ)∇φ (SI Fig. S2), so τ in that convention sits in the tortuosity-factor position (τ = εσ₀/σ_eff); no τ values are reported."
- "Because interfacial (space-charge) resistance is excluded and touching particles are fused voxels, such voxel conductivities belong to the contact-free class and should be compared with voxel-based (STEP3-type) rather than contact-network transport factors."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **재료 이전**: 전극 SE 는 **산화물 LLZO-Ta** (강체 · σ₀ 0.54 mS cm⁻¹ 문헌값) 이고 AM 은 **흑연 음극**이다.  우리 LPSCl (연성 · 3.0 펠릿) + NCM811 양극으로 옮길 수 있는 것은 **기하 · 퍼콜레이션 경향**뿐이다.  절대 σ_eff · tau2 는 옮기지 않는다.  P2D 셀의 황화물은 분리막 (Li₂S–P₂S₅) 뿐이다.
- ⚠ **계면은 완벽하다고 가정했다** (공소결 · 코팅, p.3) · 공간전하 미고려 (p.3).  냉간 압착 산화물 복합체의 실제 계면 저항은 이 모형에 없다 → σ_eff 는 계면 저항에 대해 상한 쪽이다.
- ⚠ **실험 0 건**.  "reliability of our modeling" (p.4) 의 근거는 퍼콜레이션 이론 경향과 "큰 0D 가 성능을 해친다" 는 문헌 [39,40] 과의 정성 일치뿐이다.
- ⚠ **해상도**: 최소 치수 250 nm = 2.5 복셀 · 수렴 시험 없음 → SCA 와 연결성은 해상도 의존일 것이다 (계단 면적 · 목 폭).  절대 SCA 를 인용하지 말 것.
- ⚠ **고정 겹침 −0.1 µm** → δ/d 가 0.40 · 0.20 · 0.10 (250 · 500 · 1000 nm, 우리 산술).  SE–SE 쌍에도 걸린다면 0D 크기 효과가 상대 겹침과 **교란**된다 (우리 판단 · 원문은 SE–SE 적용 여부를 명시하지 않는다).
- ⚠ **단일 실현** · seed 없음 · 퍼콜은 최단 경로 하나 · ≥ 20 vol% 의 '정확히 50 µm' 는 의심스럽다 · SE 단독 상자 ≠ 복합 전극.
- ⚠ **Table S3 불일치 4 건** (3-H) → P2D 에 실제로 들어간 값이 불확실하다.  본문 수치 표현에도 문제가 있다: "~2.0×10⁻⁶" (표 · 그림 2.4×10⁻⁶) · "more than twenty times" (1D 2500 에는 안 맞음) · "up to one-third lower" (실제 = 약 1/3 수준).
- ⚠ **컬러바 지수 누락** (Fig. 3c · S4c) — ion density 절대값 판독 불가.
- ⚠ **P2D 입력**: 관통형 σ_eff 를 P2D 에 그대로 넣었다 (τ_e 문제 — Nguyen) · COMSOL 보정 설정과 D_e,eff 관계는 미기술 · 분리막이 1 mm 펠릿이다.  "σ_eff 가 접촉면적보다 중요하다" 는 이 매개변수 영역 (σ_eff 10⁻⁷–10⁻⁵ S cm⁻¹ · i₀ 10 A m⁻²) 의 **모형 내부 민감도**이지 일반 결론이 아니다.
- ⚠ **wt% 표기**: 60:40 · 70:30 (wt%) 은 SE 13.5 · 9.5 vol% 다 — 황화물 계의 같은 wt% 와 전혀 다른 구조다.
- ⚠ **참고문헌 목록 이상** (원문 그대로 둠 · [미확인]): [13] 의 저자 목록이 [12] 와 글자 그대로 같다 · [40] 의 제목이 [1] 과 글자 그대로 같다.
- ⚠ 이 카드의 **파생값** (τ_geo · f · tau2 · 피복률 환산 · 흑연 등가구 · 국소 SE 분율 · 이온 저항) 은 우리 산술이다 — TREND 전용, 원문 값으로 인용하지 않는다.
- ⚠ 우리 쪽 수치는 `our_dem_baseline.md` 가 비어 있어 메인 리포 문서 (CLAUDE.md · 메모 v2) 에서 가져왔다 — 그 문서의 한정어 (유도 · 1세대 협착식 · 결정 4 전 HOLD) 가 그대로 붙는다.

### 메모 v2 정정 후보
- **§8-1 순위 5** ("왜 필요한가: Park Fig S9 식 · 경계조건의 인용원 — ASSB 디지털트윈 τ 의 산출법 · σ₀ 규약 (역산 대신 원값)") — [12b] (= 이 논문) 로는 **"원값" 기대가 충족되지 않는다**.
  - τ 값이 0 개이고 τ 정의도 없다 (본문 p.1–9 전수 · SI Nomenclature p.8–10 에 τ 없음).
  - σ₀ 는 LLZO-Ta 상수 5.4×10⁻⁴ 뿐이다 (SI p.3 Table S2) — AEM 의 조성 의존식은 [12b] 에서 오지 않았다.
  - σ_eff 계산 문장은 [15] = [12a] 로 넘어간다 (본문 p.3 "[15,17,22–24]").
  - ⇒ 순위 5 의 "닫는 열린 항목" 은 [12a] 로 옮기는 것이 맞다.
- 그 밖에 메모 v2 의 Park 서술 (§1 표 Park 열 · §3-4 한정어) 과 **어긋나는 문장은 없다** — 이 원문은 그것을 보강한다 ("factor" 없는 "tortuosity" · 값 미보고 · 산출법 미기술).

### 다른 카드 갱신 거리 (메인 판단 — 이 카드는 다른 파일을 고치지 않았다)
- `park2020_digitaltwin_assb_foundational` §13 의 [12] 행 ("τ 의 정의 · 산출법 · 수치가 있을 가장 유력한 곳 — 이 논문이 비운 칸을 채울 1순위") — [12b] 는 그 칸을 채우지 못한다 (위와 같은 근거).  남은 후보는 [12a].
- 같은 카드 §4-T (3) 의 "Park 의 복셀 해에는 입자간 접촉 · 계면 저항 항이 언급되지 않는다 → … (추론)" — 같은 그룹의 [12b] 는 계면 (공간전하) 항을 **명시적으로 뺐다** (p.3).  AEM 자신에 대해서는 여전히 추론이지만 그룹 관례의 직접 근거가 하나 생긴다.

---

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
1. 본문 9쪽 · SI 10쪽 전부를 그림으로 렌더해 읽었다.  표 · 그림 수치는 렌더를 확대해 읽었다.
2. Table S3 의 **1D 2500 σ_e,eff = 8.58×10⁻⁷** 는 확대 렌더에서 지수 −7 을 확인했다 (텍스트 추출 오류 아님).  Fig. 4a 의 같은 막대 ≈ 8.4×10⁻⁶ (오른축 4.0×10⁻⁵ 눈금 기준) 와 한 자릿수 차이다.
3. Fig. S2 의 식 "Domain: j = (εσ/τ)∇φ" 와 6 면 경계조건을 확대 렌더로 확인했다.
4. Fig. 3c · S4c 컬러바는 확대해도 "1×10 · 8×10 · 6×10 · 4×10 · 2×10 · 0" — 지수가 없다.
5. 전문 낱말 검색 (본문 + SI): "tortuosity" 4 회 (본문 p.3 세 번 · p.5 한 번) · "factor" 는 "the factors that affect" (p.2) 뿐 · "Bruggeman" 0 · "digital twin" 0 · "explicit jump" 0 · "Minkowski" 0 · GeoDict 판 표기 없음 · "Z-axis" 는 퍼콜 경로 문장 (p.3) 뿐.
6. Fig. 6a 의 혼합 SCA (3:1 ≈ 5.95×10⁴ · 2:2 ≈ 4.85×10⁴) 는 축 픽셀 비례로 읽었고, Table S3 의 "1:3" 59580 · "2:2" 48639 와 각각 맞는다.
7. 부피 장부 · 두께 희석 · 밀도비 정합 (3-H ✓1–3) 은 Table S3 값만으로 계산했다.
8. SI 의 형광 칠 (수정 흔적) 위치를 기록했다 (3-F).
9. 참고문헌 [13] · [40] 의 이상은 PDF 목록 문자열 그대로 비교했다.

## 참고문헌 — 우리가 더 볼 것 (원 목록 문자열 그대로)
| 순위 | 서지 | 왜 | 정본 카드 |
|---|---|---|---|
| 1 | [15] J. Park, D. Kim, W.A. Appiah, J. Song, K.T. Bae, K.T. Lee, J. Oh, J.Y. Kim, Y.-G. Lee, M.-H. Ryou, Y.M. Lee, Electrode design methodology for all-solid-state batteries: 3D structural analysis and performance prediction, Energy Storage Mater. 19 (2019) 124–129. | σ_eff 계산 문장 · 경계조건 · (아마) τ 산출법의 다음 인용원 — 이 논문이 넘긴 자리 | 같은 묶음 형제 카드 `park2019_electrode_design_methodology_assb_3d` (내용 미대조) |
| 2 | [17] M. Finsterbusch, T. Danner, C.-L. Tsai, S. Uhlenbruck, A. Latz, O. Guillon, High capacity garnet-based all-solid-state lithium batteries: fabrication and 3D-microstructure resolved modeling, ACS Appl. Mater. Interfaces 10 (2018) 22329–22339. | σ₀ = 5.4×10⁻⁴ S cm⁻¹ 의 출처 — 측정 형태 (펠릿 · 소결체 · 결정립) 확인 | 없음 (`clausnitzer2024_degradation_mechanisms_cathode_llzo` 가 HT 공소결 LCO–LLZO:Ta 시료의 출처로 인용) |
| 3 | [22] M.R. Hasyim, M.T. Lanagan, A new percolation model for composite solid electrolytes and dispersed ionic conductors, Modell. Simul. Mater. Sci. Eng. 25 (2018) 025011–025036. | 이 논문이 **고려하지 않은** 분산 이온전도체 · 공간전하 효과의 퍼콜 모형 | 없음 |
| 4 | [23] R. Blender, W. Dieterich, A random AC network model for dispersed ionic conductors, J. Phys. C: Solid State Phys. 20 (1987) 6113–6126. | 같은 계열 — 무작위 AC 저항망 (우리 접촉망과 가까운 형식) | 없음 |
| 5 | [24] A.G. Rojo, H.E. Roman, Effective-medium approach for the conductivity of dispersed ionic conductors, Phys. Rev. B 37 (7) (1988) 3696–3698. | 같은 계열 — 유효 매질 근사 | 없음 |
| 6 | [12] E. Garboczi, K. Snyder, J. Douglas, M. Thorpe, Geometrical percolation threshold of overlapping ellipsoids, Phys. Rev. E 52 (1995) 819. · [13] E. Garboczi, K. Snyder, J. Douglas, M. Thorpe, Continuum percolation of congruent overlapping spherocylinders, Phys. Rev. E 94 (2016) 032122. ([13] 저자 표기 [미확인]) | 이방 입자 연속 퍼콜레이션 문턱 — 1D · 2D 이점의 이론 근거 | 없음 |
| 7 | [20] B.L. Trembacki, A.N. Mistry, D.R. Noble, M.E. Ferraro, P.P. Mukherjee, S.A. Roberts, Mesoscale analysis of conductive binder domain morphology in lithium-ion battery electrodes, J. Electrochem. Soc. 165 (2018) E725–E736. | "Added Binder" (접촉 사이 바인더 없음) 가정의 근거 | 없음 |
| 8 | [7] A. Bielefeld, D.A. Weber, J.R. Janek, Microstructural modeling of composite cathodes for all-solid-state batteries, J. Phys. Chem. C 123 (2019) 1626–1634. | 같은 GeoDict 계열의 퍼콜 분석 (다중 실현 · 클러스터 라벨링) — 이 논문의 단일 실현 최단 경로와 대비 | `bielefeld2019_microstructural_modeling_composite_cathode` |
| 9 | [21] Y. Shen, P. He, X. Zhuang, Fracture model for the prediction of the electrical percolation threshold in CNTs/Polymer composites, Front. Struct. Civ. Eng. 12 (2018) 125–136. | 원문이 '이상적 통계 문턱 분석' 의 예로 드는 자리 | 없음 |
| 10 | [39] M. Calpa, N.C. Rosero-Navarro, A. Miura, K. Tadanaga, Electrochemical performance of bulk-type all-solid-state batteries using small-sized Li7P3S11 solid electrolyte prepared by liquid phase as the ionic conductor in the composite cathode, Electrochim. Acta 296 (2019) 473–480. · [40] C. Park, S. Lee, K. Kim, M. Kim, S. Choi, D. Shin, Promises, challenges, and recent progress of inorganic solid-state electrolytes for all-solid-state lithium batteries, J. Electrochem. Soc. 166 (2019) A5318–A5322. ([40] 제목 [미확인]) | "큰 0D SE 가 성능을 해친다" 의 실험 쪽 근거 (황화물 계) | 없음 |

## Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
