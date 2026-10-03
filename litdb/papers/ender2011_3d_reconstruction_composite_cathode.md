<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018_… · taufactor_… · landesfeind2016_… (같은 묶음 선배 카드).
     원문 = 3 쪽 단신 (Electrochem. Commun.) · SI 없음 → 카드는 비례해서 짧게, 수치는 전수.
     쪽 표기 = 인쇄 (학술지) 쪽.  PDF n 쪽 = 인쇄 (165 + n) 쪽 → PDF 1 · 2 · 3 = p.166 · p.167 · p.168.  식 · 표 · 그림 번호 = 원문.
     식 1–5 · Table 1 · 그림 축은 원문을 렌더해 대조했다 (텍스트 추출은 "σ<10⁻¹¹" 을 "σb10−11" 로, 식 1 · 5 를 조각으로 깨뜨린다).
     값 표지: stated = 본문 · 표 · 캡션 원문 / 판독 = 그림에서 읽은 값 (추세 전용) / 파생 = 카드 작성자 산술 (식 명시 · 원문 값 아님). -->
# Three-dimensional reconstruction of a composite cathode for lithium-ion cells — LiFePO₄ 복합양극 FIB/SEM 3상 재구성 (카본블랙 · LiFePO₄ · 기공) 과 상별 τ 세 가지 (FEM Laplace τ_FEM · 최단경로 τ_geom · Bruggeman) — Ender (Electrochem. Commun. 2011)
> slug `ender2011_3d_reconstruction_composite_cathode` · DOI `10.1016/j.elecom.2010.12.004` · type `image-based (FIB/SEM 3D 재구성 + FEM Laplace τ · 기하 τ · Bruggeman — liquid-LIB LiFePO₄ 복합양극)` · PDF `9. Three-dimensional reconstruction of a composite cathode for lithium-ion cells.pdf` · digested `2026-10-03` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 원문의 "tortuosity τ" 는 식 (2) `σ_eff = (x/τ)·σ_i` 의 τ = x·σ_i/σ_eff 다 → **우리 tau2 (tortuosity factor) 와 같은 정의식**.
> 원문이 바로 뒤에 *"Equation (2) is sometimes defined using τ² instead of τ, which has to be considered when comparing tortuosity values. The values τ_FEM in Table 1 are calculated with the definition given in (2)."* 라고 못박는다 (p.168).
> τ_Bruggemann = x^−0.5 (식 3) 은 tau2 의 Bruggeman 형, τ_geom = ⟨min(L)/D⟩ (식 5) 는 **τ_geo** (최단 경로 ÷ 두께 — 수송 τ 아님).
> ⚠ 원문은 τ_geom 과 τ_FEM 을 같은 표에서 **환산 없이 맞댄다** (기공 1.313 ↔ 1.312 "agree well") — 우리 규약으로 τ_geo 의 짝은 tau = √tau2 (기공 1.145) 다 (§ τ 정의 대조 ④).
>
> ★ **결정 11 요약** — τ_FEM 은 식 (4) `∇(σ_bulk∇ϕ) = 0` 을 **상 안 단일 σ_bulk** 로 푼 연속체 Laplace 해 → **접촉 · 계면 저항 항이 없다**.  저자 스스로 *"FEM simulation of the effective conductivity, which considers phase-related conductivities and contact resistances, becomes feasible"* 를 이 재구성이 열어 주는 **다음 일**로 적는다 (p.168).
> ⇒ CL-81 구조 결론 ("영상 연속체 Laplace 에는 Holm 항이 0") 의 **문헌 선례 — 구조 쪽만**.  복셀 ÷ 접촉망 대조 자체와 결손의 크기는 주지 않는다.  이산화는 복셀 직접 FD/FV 가 아니라 **FEM (ParCell3D, 원문 ref [10])** 이고 요소화 방법은 이 논문에 없다.

---

## 0. 결론 먼저

| 질문 | 답 | 근거 (쪽) |
|---|---|---|
| 원문 τ 는 제곱 든 양인가 | 기호에 제곱은 없지만 양은 **tortuosity factor 계열 = 우리 tau2** (Tjaden κ = τ²) | 식 2 · "sometimes defined using τ²" (p.168) |
| 어떻게 풀었나 | 식 (4) 상 안 균일 σ_bulk → Laplace · **FEM-tool ParCell3D** · "integrated flux through the upper boundary" → σ_eff → τ_FEM | p.167 · p.168 |
| 경계조건 · 방향 · 정규화 단면 · 요소화 | **원문에 없다** [미확인] | p.168 |
| 접촉 · 계면 저항 | **없다** — 저자가 "contact resistances" 를 넣은 FEM 을 앞으로 가능해지는 일로 적음 | p.168 |
| 상별 τ (Table 1) | 기공 (x 0.647): τ_geom 1.313 · τ_FEM 1.312 · Bruggeman 1.243 / CB (0.201): 3.331 · 5.652 · 2.231 / LFP+CB (0.353): 2.306 · 3.122 · 1.683 / LFP (0.152): 비관통 ("–") | Table 1 (p.168) |
| 우리 다섯 양 | τ_FEM → **tau2** · τ_Bruggemann → tau2 의 Bruggeman · τ_geom → **τ_geo** · f · tau 는 파생 · τ_e 없음 | § τ 정의 대조 |
| 결정 11 | CL-81 구조 결론의 선례 (구조만) + 접촉 0 연속체의 τ ≥ 1 예 — 권고 변경 없음 | §8 |

## 1. 한 줄 요약
SOFC 에서 쓰던 FIB/SEM 연속 단면 + 영상처리를 Li-ion LiFePO₄ 복합양극에 적용해, **실리콘 수지 함침**으로 카본블랙 (CB) · LiFePO₄ · 기공 세 상을 모두 분리 (저자: "for the first time") 하고 5×5×15 µm³ (24 M 복셀) 재구성에서 상별 **부피분율 · 비표면적 · tortuosity** 를 낸 3 쪽 단신이다.
tortuosity 는 같은 재구성에서 **세 방법** — FEM 으로 Laplace 를 푼 τ_FEM, 최단경로 τ_geom, Bruggeman x^−0.5 — 으로 냈다.  기공은 셋이 1.24–1.31 로 모이지만 CB 는 2.2–5.7 로 갈려 (저자 해석: 수지상 CB 구조), 저자는 **τ_FEM 이 가장 믿을 만하다**고 판정했다.
우리에게 주는 것은 셋이다: (i) τ 정의 (식 2 = tau2) 와 τ/τ² 경고의 이른 원문, (ii) 영상 연속체 Laplace 에 접촉 저항 항이 없다는 것을 **저자 스스로 적은 선례** (CL-81), (iii) 같은 시료에서 flux τ 와 기하 τ 를 나란히 준 자료 — 단 규약을 섞어 비교한 실례이기도 하다.
수치는 액체 전해질 LIB 의 **미압연 (기공 64.7 %) LFP 전극**이라 우리 LPSCl 값으로 옮기지 않는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Moses Ender** (교신) · Jochen Joos · Ellen Ivers-Tiffée — IWE, Karlsruher Institut für Technologie (KIT) · **Thomas Carraro** — IAM, Ruprecht-Karls-Universität Heidelberg | **Electrochem. Commun. 13 (2011) 166–168** | **10.1016/j.elecom.2010.12.004** | 액체 전해질 LIB 양극: LiFePO₄ (Süd Chemie) + 카본블랙 SuperP (TIMCAL) + PVDF = **70:24:6** (질량), Al 집전체 | **영상 기반 미세구조 정량** (FIB/SEM 재구성 + 3상 분할 + FEM Laplace) — DEM · MPM 아님 |

- 접수 2010-10-18 · 수정본 2010-12-03 · 승인 2010-12-03 · 온라인 2010-12-13.  © 2010 Elsevier B.V. All rights reserved (OA 아님).  키워드: Lithium-ion cell · FIB/SEM · LiFePO₄ · Carbon black · Tortuosity · Image processing.
- 사의: 전극 제조 Henning Lorrmann (ISC Würzburg) · 연구비 BMBF (인쇄 "PTJ- 03SF0343H") · CFN (Project F2.1) · Friedrich-und-Elisabeth-BOYSEN-Stiftung.  참고문헌 16 편.
- 권호: PDF 머리말은 "13 (2011) 166–168" 이고 **호수는 인쇄돼 있지 않다** — 메인 전달의 "13(2)" 는 이 카드에서 확인하지 않았다 [미확인].
- 인용 사슬: **Landesfeind 2016 의 ref 35 = 이 논문** (메모 v2 §8 머리말 — Landesfeind PDF 참고문헌 목록에서 재확인; 이 카드 작성자는 Landesfeind 원문 미열람).  ⚠ 정본 카드 `landesfeind2016_…` §5-8 · Fig. 21 의 "Ender et al. [34]" 는 **J. Electrochem. Soc., 159, A972 (2012) — 다른 논문**이다.
- 풀이 도구 분류: 정본 카드 `tjaden2018_…` §4.4 는 Ivers-Tiffée 그룹의 **ParCell3D 를 "flux-based, mesh" (2b)** 로 분류한다 (리뷰 p.55 · p.59) — TauFactor 같은 복셀 직접 FD 와 다른 갈래.

## 3. 핵심 수치

### 3-1. 시료 · 공정 (§2 Experimental, p.166)
| 항목 | 값 | 표지 |
|---|---|---|
| 조성 | LiFePO₄ (Süd Chemie) : 카본블랙 SuperP (TIMCAL) : PVDF = **70 : 24 : 6** (질량) | stated |
| 슬러리 · 코팅 · 건조 | NMP 슬러리 → *"An Al current collector (110 µm) was doctor coated"* → 60 °C 진공 건조 | stated (110 µm 가 무엇의 두께인지는 이 문장 그대로 옮김) |
| 양극 두께 · 적재량 | **30 µm · ~24 g·m⁻²** | stated |
| 압연 | §2 공정 기술에 **없다** (혼합 → 슬러리 → 닥터 코팅 → 건조).  압연은 p.168 에 "현재 연구 중" 주제로만 나온다 | 원문에 없음 |
| 전기화학 | 대칭 · 풀셀 EIS, SOC 10–100 %, 0 → +40 °C · 전하이동 분극저항 · 활성화에너지를 문헌과 대조 (ref [9]) | stated — **값은 이 논문에 없다** (n/a) |
| LiFePO₄ 전자전도도 | σ < 10⁻¹¹ S/m (상온, ref [8]) | stated (인용값) |
| 밀도 (질량 → 부피) | ρ_LiFePO₄ 3.6 · ρ_CB 1.8 · ρ_PVDF 1.77 g·cm⁻³ | stated (p.167) |
| LFP 입경 | "the particle size is quite small" (p.168) — 수치 없음.  Fig. 1b 의 밝은 LFP 단면은 대부분 1 µm 눈금보다 작다 (≈ 0.1–0.5 µm) | 수치 n/a · 판독 |

### 3-2. FIB/SEM · 영상처리 · 재구성 (p.166–167)
| 항목 | 값 | 표지 |
|---|---|---|
| 함침 · 시편 | 실리콘 수지 (Wacker) 진공 함침 → 경화 → 2×2×5 mm³ 절단 → 연삭 · 연마 | stated |
| 장비 · 취득 | ZEISS 1540XB CrossBeam · **300 장 · 간격 25 nm · 픽셀 17.5 nm** | stated |
| 재구성에 쓴 장수 | **200 장** ("200 consecutive SEM images" · "200 selected 2D images") — 300 → 200 선택 사유는 원문에 없다 | stated |
| 보정 | 연속 상 정렬 · 픽셀 크기를 스텝 폭으로 재조정 · 히스토그램 평활화 · median 잡음 필터 · 선명화 (절차 상세는 ref [3] · [4] 로 미룸) | stated |
| 분할 | 회색조 PDF 에 정규분포 셋 최우도 적합 → 식 (1) 확률 → 두 상 확률이 같은 점 = **x_l 61 · x_u 138** (0–255, 모든 영상에 같은 값) | stated |
| 문턱 교차검증 | Otsu (ref [11]) 가 x_u = 138 재현 · x_l 은 *"a supplementary method is not available"* | stated |
| 재구성 체적 | **5×5×15 µm³ = 375 µm³ · 24 M 복셀** | stated (초록 · p.167) |
| 복셀 크기 | 25 nm 등방 (재조정된 스텝 폭) 이면 200 × 200 × 600 = **24.0 M** — 원문 24 M 과 일치 | 파생 |
| 깊이 | 200 장 × 25 nm = **5.0 µm** = 체적의 한 변 (300 장이면 7.5 µm) | 파생 |
| 체적의 축 (Fig. 1a) | 앞면 가로 **15 µm** × 세로 **5 µm** (전극 윗면부터 아래로) · 밀링 깊이 **5 µm** — 30 µm 전극의 윗부분 | 판독 (축 이름은 원문에 없음) |
| 도구 | 부피분율 · 표면적 = Matlab · ScanIP (Simpleware 표면 삼각화, ref [12]) · τ = **FEM-tool ParCell3D (ref [10])** + 다른 두 방법 · 시각화 Paraview | stated (p.167) |

### 3-3. ★ Table 1 전수 (p.168, stated)
> 캡션: *"Volume fraction, surface area and tortuosity of the LiFePO₄ cathode, calculated from (a) reconstruction data and (b) mass ratio."*  비표면적과 τ 세 열은 전부 위첨자 a (= 재구성 기준).

| 상 | 부피분율^a (재구성) | 부피분율^b (질량비) | 비표면적^a [µm⁻¹] | τ_geom^a | τ_FEM^a | τ_Bruggemann^a |
|---|---|---|---|---|---|---|
| LiFePO₄ | 0.152 | 0.194 | 5.020 | – | – | – |
| LiFePO₄ + CB | 0.353 | 0.353 | 17.312 | 2.306 | 3.122 | 1.683 |
| Carbon black (CB) | 0.201 | 0.167 | 13.910 | 3.331 | 5.652 | 2.231 |
| Pores | 0.647 | 0.647 | 17.312 | 1.313 | 1.312 | 1.243 |

- 본문 요약 (p.167–168, stated): 기공 ~65 % · LFP ~15 % · CB ~20 % · 질량 기준 LFP ~19.4 % · CB (PVDF 포함) ~17 % · *"the 20% deviation between reconstructed and mass content values is subject of future investigations"* · LFP 는 **비관통 ("infinite tortuosity")** · 기공 τ_geom 과 τ_FEM *"agree well (both ~1.3)"*, τ_Bruggemann *"nearby (~1.25)"* · CB 는 *"quite differing"* (3.3 · 5.7 · 2.3) — 수지상 (dendritic) CB 탓 · LFP+CB (두 고체에 같은 전도도) 는 2.3 · 3.1 · 1.6 · *"τ_FEM is assessed as most reliable"*.
- ⚠ **본문 반올림 둘이 표와 어긋난다**: CB Bruggeman 본문 **2.3** ↔ 표 2.231 (→ 2.2) · LFP+CB Bruggeman 본문 **1.6** ↔ 표 1.683 (→ 1.7).  표 값은 식 (3) 으로 재현된다 (§3-5) → **표 값만 쓴다**.

### 3-4. 파생 환산 (카드 산술 — 원문은 이 열들을 계산하지 않았다)
f = x/τ_FEM · tau = √τ_FEM · N_M = 1/f = τ_FEM/x · N_M(B) = x^−1.5

| 상 | x | tau2 (= τ_FEM) | tau = √tau2 | f | N_M | N_M(B) | tau2 ÷ τ_Bruggemann | tau ÷ τ_geom | τ_FEM ÷ τ_geom (원문식 맞대기) |
|---|---|---|---|---|---|---|---|---|---|
| 기공 | 0.647 | 1.312 | 1.145 | 0.493 | 2.03 | 1.92 | 1.06 | **0.87** | 1.00 |
| CB | 0.201 | 5.652 | 2.377 | 0.0356 | 28.1 | 11.1 | 2.53 | **0.71** | 1.70 |
| LFP+CB | 0.353 | 3.122 | 1.767 | 0.113 | 8.84 | 4.77 | 1.86 | **0.77** | 1.35 |

- 마지막 두 열은 같은 자료를 두 규약으로 읽은 것이다.  원문처럼 τ_geom 을 τ_FEM 옆에 두면 기공 1.00 ("agree well"), Tjaden 규약 (τ_geo 의 짝 = √κ) 으로 두면 **세 상 모두 flux 쪽이 작다 (0.71–0.87)**.

### 3-5. 내부 정합 점검 (파생)
| 점검 | 결과 |
|---|---|
| 재구성 부피분율 합 | 0.152 + 0.201 + 0.647 = **1.000** ✓ · LFP + CB = 0.353 ✓ |
| τ_Bruggemann = x^−0.5 (식 3) | 0.353^−0.5 = 1.6831 · 0.201^−0.5 = 2.2305 · 0.647^−0.5 = 1.2432 → 표 1.683 · 2.231 · 1.243 **재현** (재구성 x 로 계산됐다) |
| 열 b 의 합 | LFP 0.194 + CB 0.167 = **0.361 ≠ 같은 열 LFP+CB 0.353** (기공 0.647 도 열 a 값 그대로) — **표 내부 불일치**.  0.194 : 0.167 의 비는 질량비 70 : (24 + 6) 와 밀도 3.6 / 1.8 / 1.77 로 재현된다 (LFP 몫 0.5374 ↔ 0.5376) → 열 b 는 고체 총량 **0.361** 을 나눈 값이고 그 0.361 의 출처는 원문에 없다 |
| 원문 30 µm · ~24 g·m⁻² 로 본 고체분율 | ~24 g·m⁻² 를 **전체 코팅 적재량**으로 가정하면 고체 두께 8.68 µm ÷ 30 µm = **0.289** (기공 0.71) — 재구성 0.353 도 열 b 0.361 도 재현 못 한다.  국소 (윗부분 5 µm) 재구성 대 전극 평균의 차이인지, 적재량 정의 차인지는 미확인 |
| "20 % deviation" | LFP (0.152 − 0.194)/0.194 = **−21.6 %** · CB (0.201 − 0.167)/0.167 = **+20.4 %** ✓ |
| 비표면적 정규화 · 가법성 | LFP+CB 와 기공이 같은 17.312 → 상별 표면적을 **같은 전체 부피**로 나눴다는 것과 정합 (정규화 부피는 원문 미기재 — 추론).  그 정규화와 면적 가법성을 가정하면 S_LFP–CB = (5.020 + 13.910 − 17.312)/2 = **0.809** · S_LFP–기공 = **4.211** · S_CB–기공 = **13.101 µm⁻¹** → LFP 표면의 **≈ 16 %** 가 CB 와 맞닿고 **≈ 84 %** 가 기공 (전해질) 쪽 |

## 4. 방법 ★

### 4-1. τ 세 가지 — 원문 식 그대로 (p.168)
| 식 | 원문 형태 | 무엇을 · 어떻게 | 원문이 적은 것 | 원문에 없는 것 |
|---|---|---|---|---|
| (2) | `σ_eff = (x/τ)·σ_i` | 정의: τ 는 *"correlates the intrinsic conductivity with the effective conductivity of the porous media with the volume fraction x"* (ref [13]) | *"Equation (2) is sometimes defined using τ² instead of τ … The values τ_FEM in Table 1 are calculated with the definition given in (2)."* | — |
| (3) | `τ_Bruggemann = x^−0.5` | Bruggeman (ref [14]) 를 효과 다공 매질 모형 (ref [1]) 에서 쓰는 꼴 · x = 재료 분율 (기공이면 ε) | 값은 재구성 x 로 (§3-5) | — |
| (4) | `∇(σ_bulk∇ϕ) = 0` (인쇄형 그대로 — 발산의 점 없이) | 해 = 미세구조 안 전위 분포 → 전류밀도 → **위 경계 ("upper boundary") 를 지나는 적분 flux** → σ_eff → 식 (2) 로 τ_FEM | 도구 = FEM-tool ParCell3D (ref [10], p.167) | ① 경계조건 (두 면의 전위 · 옆면 조건) ② 흐름 방향 · 어느 축이 "upper" 인가 ③ σ_eff 정규화 단면 · 길이 ④ 요소 종류 · 복셀 → 요소 변환 · 수렴 ⑤ σ_bulk 값 — 전부 [미확인] |
| (5) | `τ_geom = ⟨min(L)/D⟩` | 구조를 지나는 최단 경로 길이 L 의 평균 ÷ 두께 D (ref [13, 15]) | *"calculated using 20 paths for each starting point"* | 출발점 집합 · 경로 알고리즘 (연결성 · 거리 척도) · D 값 · 방향 [미확인] |

- **상별 계산 규약** (p.168): **CB** = *"a theoretical value (zero conductivity for LiFePO₄)"* — LFP 를 절연으로 둔 CB 단독 망 · **LFP + CB** = *"same conductivity for carbon black and LiFePO₄"* — 두 고체를 한 전도체로 묶음 · **LFP** = 비관통이라 τ 없음 · **기공** = 전해질상.
- **저자 해석** (p.168): 실제 복합체의 유효 τ 는 *"between the values of the carbon black alone and of the mixed phase"* · τ_FEM 이 가장 믿을 만하다 — τ_geom · τ_Bruggemann 은 기하 매개변수 가정을 포함하고, 특히 Bruggeman 의 가정 (*"spherical insulating particles in a conductive matrix"*) 이 이 구조에서 성립하지 않는다.
- ⚠ 그 괄호의 두 끝은 **둘 다 접촉 저항이 없는 같은 연속체**다 — 실제 전자 τ (CB–CB · CB–LFP 접촉 저항 포함) 가 그 안에 든다는 보장은 없다 (방향: 더 높게).  원문 문장은 "상 전도도 배정" 에 대한 괄호다.

### 4-2. 분할 (식 1 · Fig. 2, p.167)
- CB (어두움) 와 기공 (중간) 의 회색조 봉우리가 겹쳐 그 사이 극소가 없다 → 극소를 찾는 통상 문턱법을 못 쓴다 → 정규분포 셋 최우도 적합 (Fig. 2a) → `P_i(x) = p_i(x) / Σ_i p_i(x)` (식 1, Fig. 2b) → 두 상의 확률이 같은 두 점을 **모든 영상에 같은 문턱**으로.
- 실리콘 수지의 역할 (Fig. 1b): 에폭시 함침은 LFP (밝음) 와 나머지 (회색) 두 상만 보이고, 실리콘 수지는 CB (어두움) · 기공 (회색) 까지 셋을 가른다 — 함침이 가공 (machining) 과 대비를 동시에 준다 (p.166).
- 부피분율은 문턱 선택에 **직접 묶인다** (원문 p.167).  x_u 는 Otsu 로 확인했지만 x_l 은 확인 수단이 없다 → CB · 기공 분율과 CB τ 가 x_l 에 민감할 수 있다 (감도 미보고).

### 4-3. 시뮬레이션 · 입자 처리 ★
- **DEM · MPM 없음.**  입자 = **실제 형상 그대로** (FIB/SEM 영상) — 구 근사 없음.  압밀 · 변형 모사 없음 (영상은 건조 전극의 한 장면).
- 3상 연속체 위 Laplace — 상 안 전도도 균일, 상 사이 계면 · 접촉 저항 **없음** (영상에서 이어진 CB 입자끼리 · CB–LFP 는 저항 0 으로 융합).  "접촉 소성 vs 형상 소성" 구분은 해당 없음.
- 관측: LFP (x 0.152) 비관통 · CB (0.201) 관통 · 수지상 · *"Both solid phases appear well connected with each other and the pores are almost homogeneously dispersed among them"* (p.167).

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문에서) |
|---|---|
| FIB/SEM slice-and-view | 집속 이온빔으로 한 층 (25 nm) 씩 깎고 SEM 으로 찍기를 반복 → 영상 더미 → 3D |
| 실리콘 수지 함침 | 기공을 채워 가공을 돕고 CB 와 기공의 SEM 대비를 만든다 (에폭시는 대비 실패) |
| 최우도 분할 (식 1) | 회색조 PDF = 정규분포 셋의 합으로 적합 → 회색값마다 상별 확률 → 확률 0.5 교차점이 문턱 |
| Otsu 법 (ref [11]) | 두 무리를 가르는 표준 문턱 알고리즘 — 여기서는 x_u 확인에만 |
| 비표면적 [µm⁻¹] | 상 경계 면적 ÷ 부피 (Simpleware 표면 삼각화, ref [12]) — 정규화 부피 미기재 (전체 부피로 추론, §3-5) |
| τ_FEM | 식 (4) FEM 해에서 식 (2) 로 낸 τ = 우리 tau2 |
| τ_geom | 최단 경로 ÷ 두께의 평균 (식 5) = 우리 τ_geo |
| τ_Bruggemann | x^−0.5 (식 3) = tau2 의 Bruggeman 형 (우리 `sigma_bruggeman` = φ^1.5 와 같은 관계) |
| ParCell3D | 이 그룹 (IWE, KIT) 의 FEM 도구 (ref [10]).  Tjaden 2018 분류로 flux-mesh (2b) |
| RVE | "representative volume element" — 이 논문은 이름만 쓰고 **RVE 크기 검정은 하지 않았다** |

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | (a) FIB 로 판 시료 영역의 SEM 상 + 재구성 상자 (초록, 15 µm × 5 µm × 5 µm) · (b) 위 = 에폭시 함침 (LFP 만 구분) · 아래 = 실리콘 수지 (LFP 밝음 · CB 어두움 · 기공 회색), 1 µm 눈금 | 재구성 상자가 30 µm 전극의 **윗부분 5 µm** 만 덮는 것으로 읽힌다 (판독) → τ 의 대표성 · 방향 판단의 유일한 단서.  함침제 선택이 3상 분할의 성패를 가른다 |
| 2 | (a) 평균 회색조 PDF (파란 원) + 정규분포 셋 적합 (빨강) — 판독 봉우리 CB ≈ x 45–50 (p ≈ 0.004) · 기공 ≈ x 90 (≈ 0.014–0.015) · LFP ≈ x 200 (≈ 0.002) + 양 끝 (x 0 · 255) 튀는 점 · (b) 상별 확률 P_CB · P_pore · P_LiFePO4 와 0.5 교차점 x_l · x_u | 겹친 봉우리 → 문턱이 정규분포 가정에 묶인다 = 부피분율 · CB τ 의 숨은 불확실성 (감도 미보고) |
| 3 | 재구성 3D 시각화 (5×5×15 µm³): LFP 초록 · CB 어두움 · 기공 투명 + 2 µm 확대 큐브 | 수지상 CB 망 · 떠 있는 LFP 섬 (비관통) 의 시각 근거 |
| Table 1 | 상별 부피분율 (재구성 · 질량비) · 비표면적 · τ_geom · τ_FEM · τ_Bruggemann | 이 카드 수치의 전부 (§3-3) |

## 6. Post-processing ★
- **무엇**: 영상 정렬 → 재조정 → 평활화 · 필터 · 선명화 → 최우도 3상 분할 → 부피분율 (복셀 계수) · 비표면적 (표면 삼각화) → τ 세 가지 (FEM Laplace · 최단경로 · Bruggeman) → 질량비 부피분율과 대조.
- **도구**: Matlab · ScanIP/Simpleware (분율 · 표면적) · ParCell3D (FEM) · Paraview (시각화).  τ_geom 의 구현 도구는 원문에 없다.
- **수치화 · 기록**: Table 1 한 장 (상 행 × 방법 열).  방법을 열로 나란히 둔 형식은 우리 τ 열 묶음 (f · tau2 · tau · τ_geo 병기) 의 본보기다.  그러나 열 머리에 규약 (τ 인가 τ² 인가) 을 적지 않아 기하 τ 와 tortuosity factor 가 같은 줄에 앉았다.
- **불확실성 · 수렴 · RVE · 문턱 감도**: 보고 없음.

## § τ 정의 대조 — 우리 규약 매핑

| # | 원문 기호 (식 · 쪽) | 원문 정의 · 이름 | 정규화 (부피 · 단면 · σ₀) | 우리 양 | 환산 · 비고 |
|---|---|---|---|---|---|
| ① | **τ = τ_FEM** (식 2 · 4, p.168) | σ_eff = (x/τ)σ_i ⇒ τ = x·σ_i/σ_eff · 이름 "tortuosity" ('factor' 없음) | x = 그 상의 부피분율 (재구성, Table 1 a; 기공은 ε) · σ_i = "intrinsic conductivity" = 식 4 의 σ_bulk (그 상의 **입력값**, 수치 미보고) · σ_eff = 위 경계 적분 flux — 단면 · 길이 · 방향 미기재 | **tau2** (tortuosity factor) | f = x/τ_FEM · tau = √τ_FEM · N_M = τ_FEM/x (§3-4).  원문이 τ/τ² 를 직접 경고 — 'tortuosity factor' 이름은 우리 쪽에서 붙인다 |
| ② | **τ_Bruggemann** (식 3) | x^−0.5 | x (재구성) | tau2 의 Bruggeman 형 (= 우리 tau2_B = φ^−½) | ⇔ f = x^1.5 (우리 `sigma_bruggeman` = φ^1.5) · √ 관례면 x^−0.25 · Landesfeind Eq 6 의 α = 0.5 와 같은 꼴 |
| ③ | **τ_geom** (식 5) | ⟨min(L)/D⟩ · *"geometrical definition"* | L = 최단 경로 · D = 두께 · 출발점마다 20 경로 | **τ_geo** (`tau_geo_SE_dij` 계열) — 수송 τ 아님 | 우리 τ_geo 는 SE 중심 꺾은선 · 분모 Δz (tjaden 카드 D1) — 같은 범주 · 이산화 다름 |
| ④ | (표 맞대기) τ_geom ↔ τ_FEM | 원문은 기공 1.313 ↔ 1.312 를 "agree well" 로 읽는다 | — | τ_geo ↔ **tau2** (다른 거듭제곱) | 우리 규약의 짝은 τ_geo ↔ tau: 1.313 ↔ 1.145 (기공) · 3.331 ↔ 2.377 (CB) · 2.306 ↔ 1.767 (LFP+CB) → tau/τ_geo = **0.87 · 0.71 · 0.77** (파생) |
| ⑤ | σ_i = σ_bulk | 상의 고유 (벌크) 전도도 | 단일 전도상 해에서는 τ 가 그 값에 무관 (선형성 — 파생) | σ₀ — 단 **모형 입력 벌크값** (펠릿 · 측정값 아님) | 우리 σ₀ = 3.0 mS/cm (펠릿, CL-91) 도 망 tau2 에서 약분된다 (메모 v2 §3-1) — 약분은 같고 **기준 상태가 다르다** |
| ⑥ | x | 부피분율 (복셀 계수) | 영상 합집합 분율 | φ (f 의 짝) | 우리 φ_SE 는 구 부피 합 (겹침 이중계상) — 같은 '전체 상' 규약이지만 정의가 다르다 (복셀 대조 시 같은 φ 로 다시 정규화) |
| — | τ_e | (없음) | — | — | electrode tortuosity factor 계열 없음 — EIS 는 전하이동용이고 τ 로 환산하지 않았다 |

- **σ₀ 기준 (한 줄)**: σ_i = σ_bulk = 그 상 (전해질 · CB · CB+LFP) 의 **모형 입력 벌크 전도도** — 측정 펠릿값도, 순수 상 τ² ≡ 1 정규화 (Minnmann 관례) 도 아니다.  액체 전해질상은 미세구조 없는 벌크값이라 "기하만의 τ" 에 가장 가까운 기준이고, CB · CB+LFP 는 융합 연속체 가정의 **접촉 없는 이론값** (원문 "theoretical value") 이다.
- **판정**: ① τ_FEM = tau2 — 정의식이 같고 접촉 항이 없어 우리 망의 **FULL 이 아니라 CF 쪽 · STEP3 쪽**과 같은 범주.  ② τ_Bruggemann = tau2 의 Bruggeman.  ③ τ_geom = τ_geo.  ④ 원문 표의 τ_geom ↔ τ_FEM 맞대기는 우리 규약에서 **다른 양의 비교**다 — τ/τ² 경고 바로 뒤에 섞였다는 점이, 우리 키에 거듭제곱 · 방법 꼬리표를 강제하는 이유를 그대로 보여 준다.
- **수치 감각 (파생)**: 기공 tau2 1.31 = Bruggeman 의 1.06 배 (f ≈ 0.49) · CB 5.65 = 2.53 배 · LFP+CB 3.12 = 1.86 배.  참고: 우리 접촉망 FULL tau2 의 Bruggeman 배수 중앙 hertz 3.40 · physics 5.42 (메모 v2 §3-5, 1세대 협착식 포함) · 액체 전극 EIS ≈ 1.5–3 배 (Landesfeind A1386).

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 이 브랜치에서는 자리표시 — 값 없음.  아래 우리 쪽 서술은 CLAUDE.md CL-81 절 · 메모 v2 기준)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 미세구조 원천 | FIB/SEM 영상 (실제 형상, 25 nm) | DEM 강체구 (LIGGGHTS) · MPM 상 격자 | 다름 — 우리는 생성 모형, 이 논문은 측정 영상 |
| 전도상 | 기공 = 액체 전해질 (이온) · CB · CB+LFP (전자, 이론값) | SE 입자 (이온) · AM + 탄소 (전자) | 다름 — 액체상에는 입자 접촉이 없고 우리 SE 에는 있다 |
| τ 정의 | τ_FEM = x·σ_i/σ_eff | tau2 = φ·σ₀/σ_eff | **정의식 같음** ✓ |
| 풀이 | 연속체 Laplace (식 4) · FEM (ParCell3D) | 접촉망 Kirchhoff (간선 = 원기둥 bulk + Holm) · STEP3 복셀 FV (조화평균 면) | **STEP3 와 같은 범주** (연속체 · 계면 항 0) · 접촉망 FULL 과 다름 |
| 접촉 · 계면 저항 | 없음 — 저자가 다음 일로 명시 (p.168) | 망 FULL = Holm · CF = 0 · STEP3 = 0 (CL-81) | 이 논문 τ ≈ 우리 **CF · STEP3 계열** |
| tau2 ≥ 1 (Wiener) | 세 상 모두 τ_FEM ≥ 1.312 ✓ | CF 가지 26/157 이 tau2 < 1 (메모 v2 §3-6 — 원기둥 bulk 성질) | 연속체는 지킨다 → CF 의 tau2 < 1 은 '접촉 0' 이 아니라 **이산화 (원기둥) 의 결과** (§8) |
| flux ÷ 기하 | tau/τ_geom 0.71–0.87 (파생) | √tau2_CF/τ_Dij 중앙 0.80 · √tau2_FULL/τ_Dij hertz 1.71 (메모 v2 §3-5) | 수가 비슷하다고 정합으로 읽지 않는다 — 방향 근거로만 (§10) |
| σ₀ | 상 입력 벌크값 (미보고 · 약분) | σ_grain 3.0 (펠릿 · CL-91 · 약분) | 약분은 같다 · 기준 상태 다름 |
| 부피분율 | 복셀 계수 (합집합) | φ_SE = 구 부피 합 | 다름 |
| 방향 · 경계 | "upper boundary" flux · 경계조건 미기재 | z 관통 · 띠 Dirichlet | 원문 미기재 |
| 체적 · 해상도 | 5×5×15 µm³ · 24 M 복셀 · RVE 검정 없음 | DEM 상자 · STEP3 vox 0.115–0.4 µm (격자 미수렴 SR-01) | 다른 축 |
| 압밀 | 없음 (미압연 · 기공 64.7 %) | 300–400 MPa 냉간 압축 | **다름** — 수치 전이 불가 |
| 재료 | LFP + SuperP + PVDF · 액체 LIB | NCM811 + LPSCl (+ VGCF · PTFE) | 다름 |

- **frame [5]**: 이 논문은 **수송 기술자 절반 (영상 연속체 τ)** 만 가진다 — 기계 · 압밀 · 접촉망이 없다.  우리 쪽 같은 자리는 STEP3 (MPM 상 격자 위 복셀 FV) 이고, DEM 접촉망이 이 논문에 없는 접촉 항을 가진다.
- **frame [4]**: 이 논문 값으로 우리를 맞추지 않는다 (액체 LIB · LFP · 미압연).  쓰는 것은 정의 · 방법 · 한계 서술뿐이다.

## 8. 적용 인사이트

### 복셀 Laplace 로 τ 를 계산한 선례
(Landesfeind 2016 이 ref 35 로 *"numerical simulation of the Laplace equation as discussed, e.g., in Ender et al."* 이라 인용한 자리 — A1374 · 결정 11.  인용문 · 쪽은 메모 v2 §8-1 순위 9 행 기준이고, 이 카드 작성자는 Landesfeind 원문을 열람하지 않았다)
- **인용 사슬**: ref 35 = 이 논문 (메모 v2 §8 머리말의 재확인).  정본 카드 `landesfeind2016_…` §3-1 Eq. 5 행이 A1374 의 "3D 재구성 위 Laplace 수치해" 인용을 'Ender [35]' 로 적는다.  ⚠ 같은 카드 §5-8 의 'Ender et al. [34]' (LFP 70/6/24 · N_M ~2.5 · ~5) 는 JES 2012 의 다른 논문이다 — 이 논문의 기공 N_M 은 2.03 (파생) 이다.
- **재구성**: FIB/SEM 300 장 (간격 25 nm · 픽셀 17.5 nm) 중 200 장 → **5×5×15 µm³ · 24 M 복셀** (25 nm 등방과 산술 일치) · 실리콘 수지 함침으로 3상 분할 (최우도, x_l 61 · x_u 138).
- **부피분율 (재구성)**: 기공 0.647 · LFP 0.152 · CB 0.201 (질량비 환산 0.194 · 0.167 — 열 b 합 불일치 §3-5).
- **비표면적**: LFP 5.020 · CB 13.910 · LFP+CB = 기공 17.312 µm⁻¹.
- **τ 의 정의 · 기호**: τ (식 2) = x·σ_i/σ_eff — tortuosity factor 계열.  "τ²" 관례와 다를 수 있음을 원문이 경고한다.
- **어떤 식을 어떻게 풀었나**: 식 (4) `∇(σ_bulk∇ϕ) = 0` (상 안 균일 σ → Laplace) 를 **FEM (ParCell3D)** 으로 풀고, 위 경계의 적분 flux 로 σ_eff → τ_FEM.  **경계조건 · 방향 · 정규화 단면 · 요소화는 원문에 없다** [미확인].  ⚠ "복셀 Laplace" 는 근사 표현이다 — 방정식은 24 M 복셀 재구성 위의 Laplace 가 맞지만, 이산화는 복셀 직접 FD/FV 가 아니라 FEM 이다 (Tjaden 분류 2b).
- **상별 τ**: 기공 τ_FEM **1.312** (τ_geom 1.313 · Bruggeman 1.243) · CB **5.652** (3.331 · 2.231) · LFP+CB **3.122** (2.306 · 1.683) · LFP 비관통.
- **우리 다섯 양 중 무엇인가**: τ_FEM = **tau2** · τ_Bruggemann = tau2 의 Bruggeman · τ_geom = **τ_geo**.  f · tau 는 파생 가능 (§3-4) · τ_e 는 없다.
- **결정 11 — CL-81 구조 결론의 문헌 선례인가**: **예 — 구조 쪽만.**
  - 근거 ① 식 (4) 는 상 안 단일 σ_bulk 다 — 계면 · 접촉 저항 항이 식에 없다.
  - 근거 ② 저자 자신이 *"FEM simulation of the effective conductivity, which considers phase-related conductivities and contact resistances, becomes feasible"* 를 이 재구성이 열어 주는 다음 일로 적는다 (p.168) — 보고한 τ_FEM 에 그것이 없다는 저자의 인정으로 읽힌다.
  - 한정 ① **복셀 ÷ 접촉망 대조를 하지 않는다** (망 모형 없음) — 결손의 크기는 주지 않는다.
  - 한정 ② 기공 (액체) 상에는 입자 접촉이 **애초에 없어** 접촉 항 0 이 물리적으로 옳다.  CL-81 과 같은 처지는 CB · CB+LFP 고체상 (원문 "theoretical value") 이다.
  - 한정 ③ 원문 괄호 (CB 단독 ↔ CB+LFP) 는 두 끝 모두 접촉 0 이라 실제 전자 τ 의 범위가 아니다 (§4-1).
  - ★ 덤: 접촉 0 연속체의 τ_FEM 은 세 상 모두 **≥ 1** (Wiener 평행 상한 σ_eff ≤ x·σ_i 와 정합) → 우리 CF 가지의 tau2 < 1 (26/157) 은 '접촉 0' 이 아니라 **원기둥 bulk 이산화**의 성질이라는 메모 v2 §3-6 판정을 문헌 연속체 예로 받친다.  권고 (CF 이름표 "모델 내부 기준선" · CF 과전도 사전등록) **변경 없음**.

### 결정별 인사이트 (메모 v2 §0-2 번호)
| 결정 | 이 논문이 주는 것 | 권고 변경 |
|---|---|---|
| 11 (CF 지위 · 협착 비) | 위 — 구조 선례 + 연속체 tau2 ≥ 1 예.  ⚠ 같은 시료의 flux/기하 순서는 **반대** (tau/τ_geom 0.71–0.87, 파생) → "flux < 기하" 만으로 CF 원기둥 bulk 를 진단하지 말고 **Wiener tau2 ≥ 1** 로 진단 (§10 정정 후보 ②) | **no** (근거 보강 · 진단 문장 정밀화) |
| 14 (전자 · 열 T) | 저자는 전도도가 다른 두 고체를 섞은 τ 를 **정의하지 않았다** — CB 단독 (σ_LFP = 0) · CB+LFP (같은 σ) 두 극한만 내고 실제는 "사이" 로 남겼다 → 단일 σ₀ 기준 τ 는 "이론값" 이라는 원문 선례.  권고 ("단일 σ₀ 기준 f · T + GB 흡수 명시 — 또는 f 만") 와 같은 쪽 | **no** (이름표 "단일 σ₀ 기준 이론값" 추가 제안) |
| 5 · 15 (COMSOL 표기 · 키 이름) | 원문이 τ/τ² 를 경고해 놓고 같은 표에서 τ_geom 과 τ_FEM 을 맞댔다 = 규약 꼬리표 없는 열이 실제로 섞이는 실례.  τ_FEM 의 꼴 (σ_eff = xσ/τ) 은 COMSOL τ_F 와 같다 | **no** (키에 거듭제곱 · 방법을 넣는 권고의 문헌 실례) |
| 9 (LHS-25 면적) | 영상 면적은 상 경계 기하라 S_A + S_B − S_A∪B = 2·S_AB 항등식과 표면 예산을 **자동으로** 지킨다 (§3-5: LFP 표면의 ≈ 16 % 가 CB 접촉) — 우리 접촉별 면적 합에는 그 예산이 없다 | **no** ("구성상 ≤ 100 %" 검사의 영상 쪽 기준 예) |

### 그 밖의 적용
- ① **영상 연속체 τ 는 실험보다 낮게 나오기 쉽다 — 접촉 항이 없는 액체상에서도** (크기 감각 · 교차 논문 파생): 이 논문 기공 N_M 2.03 (ε 0.647) 은 Bruggeman 의 1.06 배다.  같은 계열 고탄소 LFP 전극의 EIS 맞춤식 (Landesfeind LFP-highC `N_M = 3.0 ε^−1.2`, 카드 `landesfeind2016_…` §5-6) 을 ε 0.647 에 넣으면 **5.06 ≈ 2.5 배**다.  다른 전극 · 다른 조성 (AM/binder/C 70/15/15 vs 이 논문 70/6/24) · 다른 공정이라 크기 감각만이다.  ⇒ STEP3 (영상형 연속체) 와 실험의 격차를 **접촉 항 하나로 귀속하지 않는다** — 영상 쪽 결손 (해상도 · 상 배정; Landesfeind A1383 은 미해상 CBD 를 지목) 이 섞인다.  복셀 ÷ 망 ÷ 실험 삼각 대조의 사전등록에 이 교란을 같이 적는다.
- ② **상 배정 감도를 τ 와 같은 표에 둔다** — 이 논문은 x_l 을 확인할 수단이 없다고 적고 감도를 내지 않았다.  우리 복셀 σ 도 상 배정 규칙 (PTFE centerline · SDCP 스탬프 — CL-60 · CL-25) 에 같은 종류로 걸린다.
- ③ **Table 1 형식 (상 행 × 방법 열)** 은 우리 인계 τ 열 묶음 (f · tau2 · tau · τ_geo) 의 본보기다 — 단 열 머리에 거듭제곱 · 방법 · 축 (방향) 꼬리표를 붙인다 (이 논문은 방향도 적지 않았다).

## 9. 인용 가능 문장 (deck/paper용)
- "Ender et al. (Electrochem. Commun. 13, 166, 2011) defined the tortuosity through σ_eff = (x/τ)·σ_i (their Eq. 2) — i.e. τ is the tortuosity factor (our tau2) — and explicitly warned that the same relation is sometimes written with τ²."
- "In their FIB/SEM reconstruction of a LiFePO₄/carbon-black cathode (5 × 5 × 15 µm³, 24 million voxels), an FEM solution of ∇·(σ_bulk∇φ) = 0 with a single phase conductivity gave τ_FEM = 1.312 for the pore phase (ε = 0.647), 5.652 for carbon black and 3.122 for the combined solid phase; contact resistances were not included and were named by the authors as a future extension of the FEM."
- "Image-based continuum conductivity calculations of this kind contain no interfacial resistance term; this is the structural precedent for treating a voxel finite-volume σ as the contact-free branch of a contact-network model."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **액체 전해질 LIB · LFP · 미압연 (기공 64.7 %)** — LPSCl 전고체 수치로 전이 불가.  쓰는 것은 정의 · 방법 · 한계 서술뿐.
- ⚠ **경계조건 · 흐름 방향 · σ_eff 정규화 단면 · FEM 요소화 · 수렴 · σ_bulk 값 · τ_geom 알고리즘 (출발점 · 연결성 · D)** 이 원문에 없다 → 우리 값과 수치 비교 금지.  τ ≥ 1 과 기공 ≈ Bruggeman 은 전체 단면 정규화와 정합하지만 (추론) 확인은 아니다.
- ⚠ **RVE 라고 부르지만 RVE 검정이 없다** (한 체적 · 한 시료 · Fig. 1a 판독상 전극 윗부분 5 µm).  같은 그룹의 RVE 방법 논문은 SOFC 대상이다 (정본 카드 `tjaden2018_…` 참고문헌 [147], 서지는 그 카드 그대로) — 이 논문 범위 밖.
- ⚠ **Table 1 내부 불일치**: 열 b LFP 0.194 + CB 0.167 = 0.361 ≠ 0.353 (§3-5) · 본문 반올림 Bruggeman 2.3 · 1.6 ↔ 표 2.231 · 1.683 (§3-3).  **표 열 a 값만 인용**.
- ⚠ 원문의 τ_geom ↔ τ_FEM "agree well" 은 다른 거듭제곱의 맞대기다 (§ τ 정의 대조 ④) — "기하 τ 로 수송 τ 를 대신할 수 있다" 의 근거로 인용하지 않는다.
- ⚠ 파생 tau/τ_geom 0.71–0.87 은 **τ_geom 알고리즘 미기재** 상태의 산술이다 — "연속체라면 flux ≥ 기하" 를 보편 규칙으로 쓸 수 없다는 반례 자료로만 쓰고, 어느 쪽이 옳다는 판정 근거로 쓰지 않는다.  우리 √tau2_CF/τ_Dij 0.80 과 숫자가 비슷한 것은 **정합이 아니다** (다른 상 · 다른 알고리즘).
- ⚠ 부피분율 · CB τ 는 문턱 x_l (61) 에 묶여 있고 감도는 보고되지 않았다.  재구성 CB 상에 PVDF 가 포함되는지 원문에 없다 (질량 기준 열 b 만 "PVDF 포함" 명시).
- ⚠ 비표면적 정규화 부피 미기재 — 전체 부피 정규화는 LFP+CB = 기공 (17.312) 에서 추론했다.  §3-5 의 LFP–CB 접촉 몫 (≈ 16 %) 은 그 추론 + 면적 가법성 가정 위의 파생값이다.
- ⚠ §8 ① 의 "≈ 2.5 배" 는 **교차 논문 파생** (다른 전극 · 조성 · 공정) — 크기 감각 전용.
- ⚠ "for the first time, all phases involved" 는 저자의 우선권 주장 (검증 안 함).
- ⚠ 원문 서지 오식 의심: ref [4] 의 DOI 가 "doi:10.1016/j.powersour.2010.10.006" 로 인쇄돼 있다 (다른 항목은 "jpowsour") — 인쇄 그대로 옮김 [미확인].
- **메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`):
  - ① **§8-1 순위 9 행** *"복셀 Laplace N_M (STEP3 계열)"* — 원문 (p.167 · p.168) 의 산출은 **N_M 이 아니라 τ_FEM** (식 2 = tau2; N_M = τ_FEM/x = 2.03 은 파생) 이고, 풀이는 **FEM (ParCell3D, ref [10])** 이라 복셀 직접 FD/FV (STEP3 · TauFactor) 와 이산화가 다르다 (Tjaden 리뷰 p.55 · p.59 의 2b).  STEP3 와 같은 것은 "영상 위 연속체 Laplace · 계면 항 0" 이라는 **범주**다 → *"영상 기반 연속체 Laplace τ (FEM) — STEP3 와 같은 범주 (계면 항 0)"* 로.
  - ② **§3-5 행** *"√T_CF / τ_Dij 0.80 … Tjaden 'flux ≥ 기하' — 우리 CF 는 반대 방향 (원기둥 bulk, §3-6)"* — 이 논문 Table 1 (p.168) 은 원기둥 bulk 도 접촉 항도 없는 연속체 FEM 인데 tau/τ_geom = 0.87 · 0.71 · 0.77 (파생) 로 **같은 '반대 방향'** 이다.  ⇒ flux/기하 순서는 기하 알고리즘에 달린다 → 그 순서를 원기둥 bulk 의 서명으로 쓰지 말고, 진단은 §3-6 의 **Wiener T ≥ 1** (이 논문 연속체는 지킨다) 로 한다.  같은 취지로 `comparison_vs_ours_DEM.md` J 절의 *"같은 시료에서 τ_flux / τ_geo = 1.24–1.59 (Tjaden 표 4·5)"* 에 반대 방향의 같은 시료 예가 있음을 덧붙일 후보 (메인 판단).

## 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 원문 ref | 목록 서지 (그대로) | 왜 |
|---|---|---|
| [10] | J. Joos, T. Carraro, B. Rüger, A. Weber, E. Ivers-Tiffée, ECS Trans. 28 (11) (2010) 81. | τ_FEM 을 낸 ParCell3D — 경계조건 · 요소화 · 정규화 (이 카드의 [미확인] 다섯) 를 닫을 자리 |
| [13] | L. Shen, Z. Chen, Chem. Eng. Sci. 62 (14) (2007) 3748. | 식 (2) · (5) 의 출처 — τ 와 τ² 관례가 갈리는 원 논의 |
| [15] | P.R. Shearing, L.E. Howard, P.S. Jorgensen, N.P. Brandon, S.J. Harris, Electrochem. Commun. 12 (3) (2010) 374. | τ_geom (식 5) 의 출처 — "20 paths for each starting point" 의 알고리즘 |
| [4] | J. Joos, T. Carraro, A. Weber and E. Ivers-Tiffée, J. Power Sources (2010), in press, doi:10.1016/j.powersour.2010.10.006. | 재구성 위 공간 분해 FEM 의 방법 원전 (DOI 인쇄 오식 의심 — §10) |
| [3] | B. Rüger, J. Joos, T. Carraro, A. Weber, E. Ivers-Tiffée, ECS Trans. 25 (2) (2009) 1211. | 영상 수집 · 보정 · 정렬 · 3D 적층 절차 (이 논문이 [3] · [4] 로 미룸) |
| [9] | J.P. Schmidt, T. Chrobak, M. Ender, J. Illig, D. Klotz and E. Ivers-Tiffée, J. Power Sources (2010), doi:10.1016/j.jpowsour.2010.09.121. | 같은 전극의 EIS 값 (분극저항 · 활성화에너지) — 이 논문에는 없다 |
| [16] | J. Illig, T. Chrobak, M. Ender, J.P. Schmidt, D. Klotz, E. Ivers-Tiffée, ECS Trans. 28 (30) (2010) 3. | 재구성 평균 입경으로 Li 확산계수 산출 |
| [7] | J. R. Wilson, J. S. Cronin, S. A. Barnett, and S. J. Harris, J. Power Sources (2010), doi: 10.1016/j.jpowsour.2010.04.066. | LiCoO₂ 첫 3D 재구성 (활물질 · 기공 2상) — 선행 |
| [14] | D.A.G. Bruggeman, Annal. Phys. 5 (24) (1935) 636. | 식 (3) 원전 |

- 이 논문 목록 밖 (다른 정본 카드 경유): 같은 저자들의 후속 J. Electrochem. Soc., 159, A972 (2012) (Landesfeind ref [34] — 카드 `landesfeind2016_…` §14 서지 그대로) · Joos 외 RVE 논문 (카드 `tjaden2018_…` 참고문헌 [147]).

## 🔗 이 정의 · 방법을 쓰는 corpus 카드
- `landesfeind2016_tortuosity_eis_electrodes_separators` — ref 35 로 이 논문을 Laplace 수치해의 예로 인용 (A1374) · 같은 카드 §5-8 의 Ender [34] 는 다른 논문.
- `tjaden2018_tortuosity_review_calculation_approaches` — κ = τ² 명명 · ParCell3D = flux-mesh (2b) 분류 · "flux ≥ 기하" 문장 (p.60–61).
- `taufactor_tortuosity_factor_tomography_tool` — 같은 정의 (τ = ε·D/D_eff) 를 복셀 직접 FD 로 푸는 도구 (이 논문은 FEM).
- 메인 리포 정본: CLAUDE.md CL-81 절 (복셀 FV = 접촉망 CONTACT_FREE 가지 위) · 메모 v2 §3-1 · §3-5 · §3-6 · §8-1.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
