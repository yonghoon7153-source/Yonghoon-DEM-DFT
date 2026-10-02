# 전극 tortuosity factor τ_e — 관통형(flow-through) tortuosity factor τ 는 다공 전극 수송을 잘못 재고, 대칭셀 임피던스(eSCM)로 정한 τ_e 를 P2D 에 넣으라 — Nguyen (npj Comput. Mater. 2020)

> slug `nguyen2020_electrode_tortuosity_factor` · DOI `10.1038/s41524-020-00386-4` · type `computational (TauFactor voxel FD/SOR · eRDM vs eSCM impedance · TLM fit) — tortuosity definition/method · liquid-electrolyte LIB` · PDF `6. The electrode tortuosity factor why the conventional tortuosity factor is not well suited for quantifying transport in porous Li-ion battery electrodes and what to use instead.pdf` · digested `2026-10-03` · status ✅
>
> inbox `tortuosity_20261003` #6 · 12 쪽 전부 읽음 (본문 + Methods + 참고문헌 43 편) · 그림 `figures/nguyen2020_electrode_tortuosity_factor/` (Fig 1–4 · 6–8 · Table 1 크롭; **Fig 5 는 크롭 없음** — p6 를 직접 렌더해 수치를 읽었다)
> 표기 규약: **stated** = 본문 문장 · **stated(그림)** = 그림 안에 인쇄된 숫자 (축 판독이 아님) · **derived** = 이 카드에서 계산 · **[미확인]** = 원문에서 못 찾음 · 식·쪽 = 원문 번호.
>
> ★ **이 카드의 결론 한 줄** — 이 논문의 "conventional tortuosity factor" τ (Eq 1, 두 평행 Dirichlet 면 사이 정상상태 flux) 는 **우리 웹앱 T = τ_Lap,eff² = φ_SE·σ_grain/σ_full 와 정의·경계조건·정규화·ε 장부가 같은 양**이다 (§정의 대조표).  Nguyen 은 바로 그 양을 **P2D 매개변수로 쓰지 말고** 대칭셀 차단 임피던스로 정한 **electrode tortuosity factor τ_e** 를 쓰라고 권한다 (p5 · p8).  둘의 차이는 구조에 따라 **부호도 크기도 정해져 있지 않다** — 잘 퍼콜된 구 충전에서는 +0.8 / +3.9 % (Fig 5), dead-end·구배 구조에서는 −46 % ~ +61 % (Fig 6), 한 줄 dead-end 기공은 τ = ∞ 인데 τ_e = 0.81 (Fig 3).
> 형제 카드: `taufactor_tortuosity_factor_tomography_tool` (이 논문의 eSCM·τ_e 코드가 들어간 툴 — ⟦10-03 코드 대조⟧ 절) · 같은 묶음 `landesfeind2016_tortuosity_eis_electrodes_separators` (= 이 논문 ref 17, eSCM 원조) · `tjaden2018_tortuosity_review_calculation_approaches` (landesfeind2016 카드는 이 묶음에서 같은 worktree 에 작성 중 · tjaden2018 은 `figures/_sources.json` 에만 있음 — 링크 확정은 메인).

---

## 1. 한 줄 요약
다공 전극의 tortuosity factor 를 재는 두 실험법 — **eRDM** (Thorat 2009, 시간영역 restricted-diffusion; 전극을 관통하는 정상상태 flux) 과 **eSCM** (Landesfeind 2016 · Malifarge 2017, 차단 조건 대칭셀 EIS + TLM 적합) — 을 **TauFactor 안에 둘 다 수치로 구현**해 같은 2D·3D 합성 미세구조에 적용했다.  결론: 전극에서는 이온이 반대편 집전체까지 **관통할 필요가 없고** 고/액 계면까지만 가면 되므로, 관통 flux 로 정의한 conventional τ 는 (i) dead-end 기공을 **부피로는 세고 수송으로는 0 으로** 취급하고 (ii) 비관통 구조에 τ = ∞ 를 주며 (iii) 방향(분리막 쪽 vs 집전체 쪽)을 못 본다.  그래서 새 개념 **electrode tortuosity factor τ_e** (Eq 2) 를 도입하고, **P2D(Newman) 매개변수화에는 τ_e 를 쓰라**고 권고한다.  eSCM 솔버는 TauFactor 에 공개 통합됐다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재계 | 연구유형 |
|---|---|---|---|---|
| **Tuan-Tu Nguyen**(1,2), Arnaud Demortière(1,3,4), Benoit Fleutot(1,3), Bruno Delobel(2), **Charles Delacourt**(1,3, 교신), **Samuel J. Cooper**(5, 교신) | **npj Computational Materials 6:123 (2020)** — 논문번호 123, 12 쪽 (p1 머리말 `npj Computational Materials (2020)6:123`) | **10.1038/s41524-020-00386-4** | **액체 전해질 LIB 다공 전극** (합성 미세구조; 구체 소재 없음). 계산 상수만 실험값: κ₀ = 0.046 S m⁻¹ (10 mM TBAClO₄, ref 16) · c_dl = 0.01 F m⁻² (refs 9,16) — Table 1 | **계산** — voxel 유한차분 (TauFactor, 과완화 반복) 로 eRDM(정상상태 Fick) · eSCM(주파수영역 대칭셀 임피던스) 모사 + TLM 적합. **실험 없음** (두 실험법을 수치로 비교) |

- 소속: (1) LRCS, CNRS UMR 7314, Université de Picardie Jules Verne, Amiens · (2) Renault Technocentre, Guyancourt · (3) RS2E, CNRS FR 3459 · (4) ALISTORE-ERI, CNRS FR 3104 · (5) Dyson School of Design Engineering, Imperial College London.
- 접수 2020-04-06 · 수리 2020-07-17 (p11). 게재일은 PDF 에 표기 없음 [미확인]. **CC BY 4.0** 오픈액세스 (p12).
- 지원: ANRT · Renault (1저자 박사과정) · EPSRC Faraday Institution Multi-Scale Modeling (EP/S003053/1, FIRG003) (p11).
- 코드: "All codes used in this study have been integrated into the open-source TauFactor platform" — MathWorks File Exchange 57956-taufactor · SourceForge (p11 Code availability). 데이터: 교신저자 요청 시 (p10).
- ⚠ **원문 오기 (인용 시 주의)**: ① p3 "TauFactor, developed by Cooper et al.³⁰" — ref 30 은 Miller 2013 (TEM 논문)이고 TauFactor 는 **ref 31** (p9 는 31 로 바르게 씀). ② p10 "GrainGeo module by GeoDict⁴¹" — ref 41 은 de Levie 1964; GeoDict 문헌은 목록에 없다. ③ "MacMullin" 을 Fig 2 캡션은 "McMullin", p9 는 "Mullin number" 로 오기. ④ ref 37 (Meyers, JES 147, 2930) 의 연도가 "(1988)" 로 인쇄 — 권·연도 정합 [미확인, 원문 그대로 둠].

## 3. 핵심 수치 ★ (전부 그림 안 인쇄값 또는 본문 — 축 판독 수치 없음)
### 3-1. τ (eRDM) vs τ_e (eSCM) — 같은 구조, 두 정의
| 구조 (그림·쪽) | 기하 | ε | A*_re | τ (eRDM) | N_M | τ_e (eSCM) | N_M,e | τ_e/τ (derived) | 출처 |
|---|---|---|---|---|---|---|---|---|---|
| 곧은 관통 기공 (Fig 3, p4) | 2D 100×100 px, 1 µm | — | — | **1** | — | **1** | — | 1 | stated(그림) |
| 곧은 dead-end 기공 (Fig 3) | 〃 | — | — | **inf** | — | **≈ 0.81** | — | — (∞ vs 0.81) | stated(그림) · p4 "infinite … less than 1" |
| A: 관통 기공 하나 (Fig 4a, p4) | 2D 300×300 px, 1 µm | 0.29 | 1 | **2.04** | 7.04 | **2.06** | 7.10 | 1.010 (+1.0 %; 본문 "<1%") | stated(그림) |
| B: 짧은 dead-end 가지 다수 (Fig 4a) | 〃 (ε_dead = 6 % 추가) | 0.35 | 4.46 | **2.46** | 7.04 | **2.59** | 7.40 | 1.053 (+5.3 %) | stated(그림) |
| C: 뭉툭한 dead-end 2 개 (Fig 4a) | 〃 | 0.35 | 1.38 | **2.46** | 7.04 | **2.97** | 8.49 | 1.207 (+20.7 %) | stated(그림) |
| D: 긴 dead-end 가지 (Fig 4a) | 〃 | 0.35 | 4.37 | **2.46** | 7.04 | **3.61** | 10.31 | 1.467 (+46.7 %) | stated(그림) |
| 3D 구 충전 A (Fig 5, p6) | 입경 2 µm, 100³ voxel, 250 nm | 0.35 | — | **2.58** | 7.37 | **2.60** | 7.43 | 1.008 (+0.8 %) | stated(그림, p6 렌더) |
| 3D 구 충전 B (Fig 5) | 입경 5 µm, 50³ voxel, 250 nm | 0.20 (캡션) | — | **3.35** | 14.56 | **3.48** | 15.13 | 1.039 (+3.9 %) | stated(그림) · ⚠ 아래 |
| 2층 다공도, **조밀층 집전체 쪽** (Fig 6, p7) | 50³ voxel, 1 µm; 두께 90 % ε 0.35 + 10 % ε 0.20 | (≈0.34) | — | **7.4** | 21.8 | **4.0** | 11.8 | 0.541 (−46 %) | stated · p7 |
| 〃 **조밀층 분리막 쪽** (Fig 6) | 같은 구조 뒤집음 | 〃 | — | **7.4** | 21.8 | **11.9** | 35.1 | 1.608 (+61 %) | stated · p7 |

- **방향 효과** (Fig 6): 같은 구조인데 τ_e 가 4.0 ↔ 11.9 = **×2.98** (derived). τ 는 7.4 하나 (방향 무관).
- **dead-end 부피분율** (TauFactor 판정, flux < 최대의 2 %): 3D A **4 %** · 3D B **8 %** (Fig 5, p6) · 2층 구조 **33 %** (Fig 6, p7). 3D 구 충전은 퍼콜레이션 **> 99 %** (p6).
- **특성 주파수** (Nyquist 위 표기, stated(그림)): Fig 4b A·C **283 Hz**, B·D **56 Hz** (면적 A* 가 클수록 낮다 — p5 "C_DL in Eq. 6") · Fig 5 A 28 / 225 Hz, B 225 / 892 Hz · Fig 6 ~10 / ~89 Hz (조밀층 집전체 쪽) · ~56 Hz (분리막 쪽).
- ⚠ **내부 불일치 (derived)**: Fig 5 B 는 τ/N_M = 3.35/14.56 = **0.230**, τ_e/N_M,e = 3.48/15.13 = **0.230** 인데 캡션은 ε = 20 %. 나머지 경우는 τ/N_M 이 표기 ε 과 맞는다 (A 0.350 · Fig 4 0.290/0.349 · Fig 6 0.339 ≈ 0.9·0.35 + 0.1·0.20 = 0.335). 원인 [미확인] — B 의 ε 는 0.23 으로 계산된 것으로 보인다.

### 3-2. ε 장부 효과 — 같은 N_M, 다른 τ (Fig 2, p3–4)
| 경우 | ε | τ | N_M | 비고 |
|---|---|---|---|---|
| Case A (관통 + dead-end 4 유형) | **34.7 %** | **2.25** | **6.49** | stated(그림) |
| Case B (flux 문턱 2 % 로 dead-end 를 지우고 관통만) | **22.6 %** | **1.47** | **6.49** | stated(그림) |
- 수송량 (N_M = κ₀/κ_eff) 은 **그대로**인데 τ 는 **−35 %** (derived 1.47/2.25 = 0.653). 이유: Eq 1 τ = ε·N_M 이라 dead-end 기공은 **flux 에는 0, ε 에는 +** 로 들어간다 (p5 "even though the dead-end pores do not contribute to species transport at steady-state, their presence does have an effect on the determination of tortuosity, via their additional volume fraction").

### 3-3. eSCM 계산 상수 (Table 1, p10)
| 변수 | 값 | 출처 표기 |
|---|---|---|
| κ₀ | **0.046 S m⁻¹** | 각주 1: ref 16 (Thorat), 10 mM 차단 전해질 TBAClO₄ |
| c_dl (미시 활성 표면적당) | **0.01 F m⁻²** | 각주 2: refs 9, 16 |
| f | **10⁷ – 10⁻¹ Hz** | a: 가정값 |
| voxel 크기 | **1 × 1 × 1 µm³** | a: 가정값 — ⚠ Fig 5 캡션은 "voxel size is 250 nm" (불일치, 원문 그대로) |

- σ_ionic · E_SE · porosity@P · coverage · Z · Heckel: **n/a** (압밀·소재 물성 논문 아님).

## 4. 방법 ★
### 4-A. 두 실험법 (p2 · Methods p8–9)
| | **eRDM** (Thorat 2009, ref 16) | **eSCM** (Landesfeind 2016 ref 17 · Malifarge 2017 ref 18) |
|---|---|---|
| 셀 | 집전체에서 벗긴 free-standing 전극을 **분리막 두 장 사이**에 두고 Li foil 두 장으로 샌드위치 (Fig 1a) | 같은 전극 두 장 (집전체 붙은 채) + 분리막 = **대칭셀** (Fig 1b) |
| 자극 | 편극으로 정전류 → 염 농도 구배 → 전류 차단 후 **이완**(relaxation) 의 셀 전위 감쇠 | **EIS** (주파수 영역) |
| 무엇을 재나 | 전극을 **관통**하는 유효 염 확산계수 D_eff (농축용액 Mac-Innes 수송모델로 적합, 분리막 τ 는 미리 알아야 함) | 기공 전해질의 유효 이온 저항 R_ion (TLM 적합) — 이온은 분리막에서 들어와 **고/액 계면**까지만 간다 |
| 조건 | 전극이 Li⁺ 에 가역 (Li foil) | **차단 조건** — 비삽입 염 (예: TBAClO₄) 또는 비삽입 상태 전극 → 전하전달·확산 없음, 이중층 충전만 |
| 장단점 (p2–3) | 집전체 없는 전극 + 벌크 확산계수 정확값 필요, 번거로움 | 빠르고 편함 (Pouraghajan 2018 비교에서 둘 다 가능한 경우 대체로 일치) |
- 원래 형태(RDM·SCM)는 **전자 절연** 다공체(분리막)용 — 전극은 전자 단락(RDM)·전위장 간섭(SCM) 때문에 그대로 못 쓴다 (p2). 그래서 "e-" 변형.

### 4-B. 정의식 — 식 번호·쪽 (원문 렌더로 확인)
| 식 (쪽) | 원문 식 | 뜻 |
|---|---|---|
| **Eq 1 (p1)** | **τ/ε = ρ_eff/ρ₀ = κ₀/κ_eff = D₀/D_eff = N_M** | **conventional tortuosity factor** τ · MacMullin 수 N_M. ρ₀·κ₀·D₀ = 전해질 고유값, ρ_eff·κ_eff·D_eff = 다공 구조가 만든 "유효" 관측값 (refs 11, 12) |
| **Eq 2 (p8)** | **τ_e/ε = R_ion·A_CC·κ₀/L = N_M,e** ;  R_ion = Σ r_ion | **electrode tortuosity factor** τ_e. L = 전극 두께 (m), A_CC = 거시 집전체 면적 (m²), R_ion = TLM 적합 이온 저항 |
| Eq 3 (p9) | A* = A_micro/A_CC = a·A_CC·L/A_CC = a·L | 집전체 면적당 미시 활성 표면적 (무차원); a = 부피당 활성 표면적 (m⁻¹) |
| Eq 4 (p9) | Z̃_El = √(R_ion·Z̃_t)·coth(√(R_ion/Z̃_t)) = √(R_ion/(jωA_CC C_DL))·coth(√(jωA_CC C_DL R_ion)) ;  Z̃_t = 1/(jωA_CC C_DL) ;  C_DL = Σ c_dl ΔA* | 차단 조건 TLM (r_ion ≫ r_el = 0 가정, Landesfeind) — 순수 축전 이중층 |
| Eq 5 (p9) | lim_{ω→0} Re(Z̃_El) = R_ion/3 | 45° 영역이 실수축으로 ≈ R_ion/3 — 적합 없이 R_ion 추정 (ref 19) |
| Eq 6 (p9) | lim_{ω→0} Im(Z̃_El) = −1/(ωA_CC C_DL) | 저주파 수직선 = 총 이중층 용량 → A* 가 특성 주파수에 들어간다 |
| Eq 7 (p9) | Z̃*_El = Z̃_El·A_CC·κ_eff/L | 무차원 임피던스 (그림의 축) |
| Eq 8 (p10) | F = Σ_n (\|Z̃*_El−sim − Z̃*_El\|)² / \|Z̃*_El−sim\|^p | MATLAB `fminsearch` 목적함수; p = 가중 지수 (ref 20). "τ_e can be extracted from just the values of Z̃*_El at ω → 0 and ω → ∞" (p10) |

- 두 식의 **형식은 같다** (τ/ε = κ₀/κ_eff). 다른 것은 κ_eff 를 **어떤 경계조건의 어떤 측정**에서 얻느냐다 — Eq 1 은 관통 정상상태 flux, Eq 2 는 차단 대칭셀 TLM 의 R_ion.
- Eq 4 의 TLM 은 Finite-Space Warburg 와 수학적으로 같은 꼴이지만, 시간상수가 **표면 스케일** (이중층) 이지 부피 스케일이 아니다 (p9). 전하전달을 막은 P2D 는 TLM 으로 줄어든다 → P2D 로도 차단 대칭셀 임피던스를 적합할 수 있다 (순수 축전일 때) (p9).
- 확장: Malifarge (ref 18) — 고상 전자저항 임의값 포함 해석식 · Pouraghajan (ref 20) — 집전체 접촉저항·R_ct·고상 전자저항 포함 일반 TLM · CPE (Q_S) 로 대체 가능 (p9).

### 4-C. 수치 구현 (TauFactor, Methods p9–10)
| | eRDM 모사 | eSCM 모사 |
|---|---|---|
| 지배식 (Fig 8, p10) | 기공 Ω 에서 **∇²Ĉ = 0** (정상상태) | 기공 Ω (전극 + 분리막) 에서 **∇²Φ̃₂ = 0** (주파수 영역 Fourier 변환) |
| 경계 — 양 끝 | **Ĉ = 1 / Ĉ = 0** (두 평행판) | 고상 전위 **Φ̃₁ = 1 / Φ̃₁ = 0** (두 집전체; 전극마다 등전위 = 고상 저항 0 가정) |
| 경계 — 기공벽 | **∇Ĉ·n = 0** (no-flux) | 전극 기공벽: **−κ_eff∇Φ̃₂·n + jωc_dl(Φ̃₁ − Φ̃₂) = 0** (그림 원문 표기 κ_eff) · 분리막 벽: **−∇Φ̃₂·n = 0** (불활성) |
| 물리 | 무한희석 Fick 확산만 — 전기 이동·대류 없음, 이중층 없음 (p3, p9) | 이동 전류 + **용량성 전류** (이중층 충전) — 반응 없음 |
| 산출 | 정상상태 flux → τ (Eq 1) | Z̃_El−sim = ΔΦ̃₁ (임의 1 V; 선형이라 무관) ÷ 총 이온 전류밀도 (셀 단면 기준) → Eq 4 적합 (Eq 8, `fminsearch`) → R_ion → τ_e (Eq 2) |
| 풀이 | 과완화 반복 (TauFactor 기존 솔버) | C++ 사전컴파일 + 주파수마다 과완화 반복 (p10) |
- 전기전도·열전도도 같은 수학 (농도 구배 → 전위·온도 구배) 으로 정상상태 유효값을 낼 수 있다 (p9) — ★ 우리 σ_ion·σ_e·κ 삼중항이 같은 Laplace 꼴인 근거와 같은 문장.
- 3D eSCM 은 분리막 기공망 대신 **전해질만 있는 자유 층**을 두 전극 사이에 둠 (데이터 준비 단순화); 2D 는 전극 기공과 정확히 정렬된 곧은 기공 분리막 (p10). 향후 "반쪽 셀" 로 줄이는 안 (p10).
- 코드 실물 대조 (TauFactor 1.424.0): mode 5 "Symmetric Cell Impedance Spectrum w/ Mirror" 와 mode 6 "Electrode Tortuosity w/Mirror" 가 들어 있다 — **mode 5 는 τ_e 를 내지 않고 스펙트럼만** 낸다 (`Results.Tau=nan`), Eq 4 적합 코드는 툴에 없다. 상세·줄 번호는 `taufactor_tortuosity_factor_tomography_tool` ⟦10-03 코드 대조⟧ 절.

### 4-D. 미세구조 세트 (p10)
- **2D "모델" 구조** — MS Paint 로 그림 (Fig 2–4). 2D 는 분리막에 전극 기공과 정렬된 곧은 기공.
- **3D** — GeoDict **GrainGeo** 모듈의 구 무작위 충전 (Fig 5, 6). Fig 6 은 두께 90 % ε 0.35 + 마지막 10 % ε 0.20 의 2층 (조밀층이 기공 대부분을 닫아 **길고 잘 연결된 dead-end** 를 만들도록 설계, p7).
- **입자 처리** ★: 구 (강체, 기하 생성) — 접촉법칙·압밀·소성·형상변화 **없음**. voxel 연속상 위에서 Laplace/임피던스만 푼다 ⇒ 점접촉 협착 개념도 없다 (TauFactor 카드 §A 와 같은 위치).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 실험 배치 모식: (a) eRDM — 분리막 두 장 사이 free-standing 전극, 이온 flux 가 전극을 **관통** (b) eSCM — Al foil 위 동일 전극 두 장 + 분리막, 이온은 분리막에서 들어와 계면에서 멈추고 전자는 집전체에서 온다 | 우리 σ 솔버의 경계조건은 전부 (a) 형 (두 띠 관통) — §정의 대조표 |
| 2 | 기공 유형 분류 (관통 = 회색 · dead-end 파랑/보라/초록 · 저 flux 모서리 빨강) + 정상상태 스칼라장 + 정규화 flux 지도. Case A ε 34.7 % τ 2.25 ↔ Case B (관통만) ε 22.6 % τ 1.47, **N_M 6.49 동일** | ★ ε 장부 효과 — 우리 φ_SE 도 비관통 SE 를 포함해 같은 방식으로 T 를 키운다 |
| 3 | 가장 단순한 두 구조: 곧은 관통 τ = τ_e = 1 (eSCM 구현 교차검증) · 곧은 dead-end τ = inf, τ_e ≈ 0.81 + 모사 Nyquist (45° 가이드) | 비관통 = τ ∞ 인데 τ_e 는 유한 (< 1 도 가능) — 우리 비관통 24/130 침대 |
| 4 | (a) A–D 2D 구조와 ε · A*_re · τ · N_M · τ_e · N_M,e 표 (b) 모사 EIS + Eq 4 적합, 중주파 확대 (56 / 283 Hz) | 같은 τ (2.46) · 같은 N_M (7.04) 인데 τ_e 2.59–3.61 — τ 는 dead-end **형태**를 못 본다. B·D 의 45° 이탈은 실험에서 접촉저항으로 오독될 수 있다 (p5) |
| 5 | (크롭 없음 — `figures.json` missing_labels f5; p6 렌더로 판독) 3D 구 충전 A (2 µm, ε 35 %) · B (5 µm, ε 20 %): τ 2.58/3.35 vs τ_e 2.60/3.48, 관통/dead-end 96/4 % · 92/8 % 기공망 그림 | 잘 퍼콜된 구 충전에서 두 정의 차 ≤ 4 % — 우리 퍼콜 침대에서 기대되는 크기의 문헌 근거 (ASSB 전이는 §10) |
| 6 | 2층 다공도 구조: (a) 모사 EIS — τ_e 4.0 (조밀층 집전체 쪽, TLM 과 잘 맞음) vs 11.9 (분리막 쪽, 중주파 이탈) (b) eRDM τ 7.4 · flux 밀도 투영 (위쪽 조밀층에서 낮음) · 관통 67 % / dead-end 33 % | ★ 방향 의존 ×2.98 — 우리 graded-z (A7) · 플래튼 근처 밀도 구배는 T 로 순위를 못 매긴다 |
| 7 | TLM 이론: (a) 차단 조건 이상 응답 — 분포 용량 45° 영역 (실수축 길이 R_ion/3) + 이온 차단 수직선 (b) TLM 회로 (r_el · r_ion · z̃_t) | 우리 실험 앵커 (Bazzoun · Minnmann · Kim 2025) 가 R_ion 을 뽑는 방식 — 그 τ 가 어느 정의인지 §7 |
| 8 | TauFactor 구현 그림: (a) eRDM ∇²Ĉ = 0, Ĉ = 1/0, 벽 ∇Ĉ·n = 0 (b) eSCM ∇²Φ̃₂ = 0, 전극 벽 −κ_eff∇Φ̃₂·n + jωc_dl(Φ̃₁ − Φ̃₂) = 0, 분리막 벽 −∇Φ̃₂·n = 0, Φ̃₁ = 1/0; 이동 전류 · 용량성 전류 화살표 | ★ §정의 대조표 "경계조건" 칸의 원천 |
| Table 1 | eSCM 계산 상수: κ₀ 0.046 S m⁻¹ · c_dl 0.01 F m⁻² · f 10⁷–10⁻¹ Hz (가정) · voxel 1 × 1 × 1 µm³ (가정) | ⚠ voxel 1 µm (가정) ↔ Fig 5 캡션 250 nm 불일치. TauFactor GUI 기본값 (1 S/m · 1 F/m²) 과도 다르다 — 툴 카드 참조 |

## 6. Post-processing ★
- **dead-end 판정**: 정상상태 flux 밀도 지도에 **최대 flux 의 2 %** (자의적 문턱, p4 · Fig 5 캡션) 를 걸어 "관통" / "dead-end" 를 나누고 부피분율을 셈 (TauFactor). dead-end 는 다시 4 하위 유형 (Fig 2: 파랑 = eRDM 에선 dead-end · eSCM 에선 CV 방향에 따라 다름 / 보라 = 관통 기공에서 갈라진 가지 / 초록 = CV 가 크면 관통이 될 수 있는 것 / 빨강 = 저 flux 모서리). ⚠ TauFactor 1.424.0 코드의 같은 분류 블록은 문턱이 **0.5 %** 다 (툴 카드 ⟦10-03⟧).
- **τ_e 추출**: 모사 스펙트럼을 Eq 4 TLM 에 최소제곱 적합 (Eq 8, `fminsearch`, 가중 p) → R_ion → Eq 2. (ω→0, ω→∞ 극한값만으로도 가능, p10.)
- **N_M · N_M,e 병기**: 그림마다 τ 와 MacMullin 수를 같이 적는다 — ε 장부를 뺀 순수 수송량이 N_M (Fig 2 에서 결정적).
- **균질화 진단**: 모사 EIS 가 TLM 의 45° 에서 벗어나면 → (i) 모사 부피가 대표성이 없거나 (ii) 구조가 균질화 불가 (구배 전극 등) 둘 중 하나 (p6, p8). "simulated EIS … could be used as a quantitative tool to assess deviation from the porous electrode theory" (p6). TLM 과의 일치도를 수치화하는 지표는 제안만 (p8).
- **도구**: TauFactor (MATLAB, 과완화 반복 FD), GeoDict GrainGeo (3D 생성), MS Paint (2D), MATLAB `fminsearch`.

### 6-bis. 절별 결과 흐름 (논증 순서)
1. **기공 유형 (Fig 2, p3–4)** — flux 가 거의 0 인 기공을 지워도 N_M 은 그대로 → eRDM 의 τ 는 그 기공을 **부피로만** 센다.
2. **최단 사례 (Fig 3, p4)** — 곧은 관통이면 두 방법 모두 1 (구현 교차검증). 곧은 dead-end 면 eRDM ∞, eSCM 0.81 (<1).
3. **2D A–D (Fig 4, p4–5)** — dead-end 6 % 를 형태만 바꿔 붙인 세 구조가 τ·N_M 은 같고 τ_e 는 2.59 / 2.97 / 3.61. 해석 (p5): eSCM 은 "한쪽 경계에서 고/액 계면까지 가기가 얼마나 어려운가" 의 상대 척도 — A 는 계면이 적지만 가기 쉽고, B 는 면적 ×4.46 인데 약간 더 어렵고, C 는 추가 면적 절반이 분리막에서 멀어 τ_e 가 높고, D 는 긴 가지라 가장 높다. A 와 B 는 N_M,e·R_ion 이 비슷한데 B 가 접근 가능한 계면이 많다 → "전기화학 활성 비표면적 (specific electrochemically active surface area) 을 늘리면서 N_M,e 를 낮게 유지" 하면 출력 성능이 좋아질 수 있다 (p5, "may improve power performance").
4. **권고 (p5)** — 전극 기공은 하전 종이 전기화학 면적에 닿는 통로이므로 eSCM 의 τ_e 가 더 적절. 입자/특징 크기 ≪ 두께라 부분부피에서 τ 를 뽑을 수 있으면 eRDM 도 의미가 있지만 dead-end 처리 오류는 남는다. **"for battery macroscopic models such as Newman's P2D model, the electrode tortuosity factor τ_e should be preferred over the conventional tortuosity factor τ during the parametrization step"**.
5. **3D 구 충전 (Fig 5, p6)** — 퍼콜레이션 > 99 %, dead-end 4 / 8 % 라 두 정의 차가 작다. dead-end 상당수가 CV 경계에 있어 CV 를 키우면 더 준다. B (5 µm) 의 TLM 이탈 = 대표성 부족 신호. Pouraghajan (ref 20) 의 상용 전극 일치 결과를 이것으로 설명할 수 있다 (p6–7).
6. **2층 구조 (Fig 6, p7)** — 저다공도 → 퍼콜 감소 → dead-end ↑ 를 의도적으로 만든 예. τ 7.4 인데 τ_e 는 4.0 (조밀층 집전체 쪽) / 11.9 (분리막 쪽). 바인더 과잉 (집전체 쪽) · 급속 건조 (분리막 쪽 조밀) 같은 제조 결함의 모델. 분리막 쪽 고다공도 구배 설계 지지 (Morasch ref 33); Lu (ref 34) 는 기하 tortuosity 로 분석해 협착 무시 등 단순화가 있다고 비판 (p7).
7. **P2D 에 τ_e 를 써야 하는 이유 (p7–8)** — P2D 는 ε · a · τ 한 값씩으로 전극을 기술하고, **τ 가 미세구조 복잡도를 담는 유일한 항**인데 conventional τ 는 "flow through" 시나리오만 담아 계면 접근성을 표현하지 못한다.
8. **논의 (p8)** — dead-end 기공이 두 방법 불일치의 주원인; τ_e 는 1 보다 작을 수 있다; 분석 **방향**이 τ_e 를 바꾼다 (구배 전극에서 중요); 3D 모사 EIS 의 TLM 이탈은 CV 비대표성 또는 비균질성의 표지. 실제 전극 데이터 적용은 후속 연구로 미룸.

---

## § tortuosity 정의 대조표 ★★ (이 묶음의 목적 — tortuosity 정의를 닫는다)
> 열: 원문 기호 · 정의식 · 이름 · 경계조건 · 우리 어느 τ 와 같은 양인가 · 환산식.  우리 쪽 코드 줄은 메인 리포 `claude/stoic-knuth-NObVQ` (HEAD `1afd37a9a`) 에서 읽었다.

| 원문 기호 (출처) | 정의식 | 이름 | 경계조건 | 우리 어느 τ 와 같은 양인가 | 환산식 |
|---|---|---|---|---|---|
| **τ** (Nguyen Eq 1, p1) | τ/ε = κ₀/κ_eff = D₀/D_eff = N_M | conventional ("flow through") tortuosity factor — eRDM 계열 | 두 평행 Dirichlet 면 (Ĉ = 1 / 0) · 기공벽 no-flux · 정상상태 · 반응·이중층 없음 (Fig 8a, p10) | ★ **T = τ_Lap,eff²** = φ_SE·σ_grain/σ_full (웹앱 `app.py:2610` 은 √ 를 취해 τ_Lap,eff 로 표시). 정의·BC·정규화·ε 장부 모두 같다 (아래 판정) | **τ_Nguyen = T = τ_Lap,eff²** ; τ_Lap,eff = √τ_Nguyen |
| **N_M** (Eq 1) | κ₀/κ_eff = τ/ε | MacMullin number | 〃 | **1/f**, f = σ_full/σ_grain (= `sigma_full`, `network_conductivity.py:857`) | N_M = 1/f = T/φ_SE |
| **τ_e** (Eq 2, p8) | τ_e/ε = R_ion·A_CC·κ₀/L = N_M,e ; R_ion 은 Eq 4 TLM 적합 (또는 Eq 5 극한) | **electrode tortuosity factor** — eSCM 계열 | 대칭셀 · 차단 조건 · 고상 등전위 Φ̃₁ = 1/0 (두 집전체) · 전극 기공벽 −κ_eff∇Φ̃₂·n + jωc_dl(Φ̃₁ − Φ̃₂) = 0 · 분리막 벽 no-flux (Fig 8b) | ★ **우리에게 없다.** 가장 가까운 것은 `ionic_active_pct` (분리막 쪽 = 위 띠에 닿는 SE 성분과 접촉한 AM 비율, `dem_analysis_core.py:741–768` · `lhs_design_dataset.py:1067`) — 편측·분리막 기준이라는 **개념**은 같지만 **이진 접근성**이지 저항 가중이 아니다 | **환산 불가** — 구조·방향 의존. 원문 예: τ_e/τ = 0.54 ~ 1.61 (Fig 4–6), 0.81 vs ∞ (Fig 3) |
| **N_M,e** (Eq 2) | τ_e/ε = R_ion·A_CC·κ₀/L | electrode MacMullin 수 (p9 "Mullin" 오기) | 〃 | 없음 | — |
| **A*** (Eq 3, p9) | A_micro/A_CC = a·L | 집전체 면적당 미시 활성 표면적 | — | 아날로그: AM–SE 계면 면적 ÷ 전극 면적 (우리 접촉면적 열) — ⚠ 액체 전극은 **기공벽 전체**가 이중층, ASSB 는 **AM(+탄소)–SE 접촉면만** | 정의 다름 — 직접 환산 금지 |
| "geometrical tortuosities" (p2 · p7 Lu ref 34) | 원문에 식 없음 | 기하 tortuosity | 경로 기반 — "ignoring constriction in flow paths" (p2) | **τ_Dijkstra · τ_Dij,all · 벽 τ** (기하 최단경로; `app.py:2617–2620`, CLAUDE.md "벽 τ = 기하 최단경로 — 수송 τ 아님") | **환산 없음** — 다른 양 (Nguyen: 3D 기공망 특성화에 부적합) |
| (우리) τ_Lap,geom | √(φ_SE·σ_grain/σ_bulk_net) (`app.py:2613`) | Laplace, 협착 제외 | τ 와 같은 관통 BC · 접촉망의 CONTACT_FREE 가지 (`R_constriction = 0`, `network_conductivity.py:1111–1113`) | τ_Nguyen **형식**에 contact-free σ 를 넣은 것 — Nguyen 의 voxel 연속체 τ 와 같은 "협착 없음" 쪽 | T_geom = τ_Lap,geom² |
| COMSOL τ_F (메인 제공: COMSOL 5.6 Eq 6-6 — 이 카드에서 원문 대조 안 함) | f_e = ε_p/τ_F (⇒ κ_eff = κ·ε_p/τ_F) | tortuosity factor (P2D 매질 입력) | 매질 매개변수 (BC 없음) | **= T** (같은 꼴). Nguyen 권고대로면 이 칸은 **τ_e** 여야 한다 | **τ_F = T = τ_Lap,eff²** (√ 아님) |
| Bruggeman (메인 제공) | τ_F = ε_p^(−1/2) | 상관식 | — | T_Brug = φ^(−1/2) ⇔ f_Brug = φ^1.5 | 예 φ 0.30 → T 1.826 · f 0.164 (derived) |
| TauFactor `Results.Tau` mode 1/2 | τ = D·VolFrac/D_eff (`TauFactor.m:3495`) | Tortuosity Factor (D:D) | Dirichlet 1/0 · 측면 Mirror(1) / Periodic(2) | = τ_Nguyen = T (형식) | 툴 카드 ⟦10-03⟧ |
| TauFactor mode 6 | τ_e = 3·VolCorrect/D_eff (`TauFactor.m:3684`) | Electrode Tortuosity | 저주파 한 점 (`freq = 1e-6/a`, 코드 주석 "needs justification") | = τ_e (의도) [유도 미확인] | 툴 카드 ⟦10-03⟧ |

### 판정 — 우리 τ_Lap,eff 는 "conventional tortuosity factor" 쪽인가? → **예 (제곱하면 같은 양)**
| 비교 축 | Nguyen Eq 1 τ (eRDM 모사) | 우리 T = τ_Lap,eff² | 판정 |
|---|---|---|---|
| 식 형식 | τ = ε·κ₀/κ_eff | T = φ_SE·σ_grain/σ_full (`app.py:2610`) | 같음 |
| 경계조건 | 두 평행 Dirichlet 면, 반응·이중층 없음 | z 하단·상단 띠 (`network_conductivity.py:225–249`) 에 가상 source/sink (`:590–593`) · 측면 최소영상 = 주기 (`:288–294`) | 같음 (관통형). 측면은 TauFactor mode 2 짝 |
| 풀이 영역 | 관통 기공만 flux (dead-end 는 flux 0) | 바닥·꼭대기 둘 다 가진 성분만 (`:552–557`) | 같음 |
| 정규화 | 관측 κ_eff (CV 전체 단면) | σ_ratio = G_eff·T/A_box, A = box_x·box_y 전체 (`:852–857`) | 같음 |
| ε 장부 | 전체 기공 (dead-end 포함 — Fig 2·4 논리) | φ_SE = **모든 SE 구** 부피 합 / V_box (`:1120–1123`; 노드 = 그 타입 전부, `:209–211`) | 같음 — ⚠ 구 부피 합 (겹침 이중계상) 이지 합집합 아님 |
| 비관통 | τ = ∞ (p5) | `perc_nodes` 없음 → σ = None (`:559–576`) → τ_Lap N/A | 같음 |
| 협착 | 없음 (voxel 연속체) | 접촉당 Holm 협착 포함 (FULL) | **다름** — 물리 차이 (정의 차 아님). STEP3 복셀 σ (`step3_sigma.py:835–840`: "plate φ=1 at the bed bottom, φ=0 plate at the bed top, lateral Neumann") 는 협착 없음 = TauFactor mode 1 짝 |

⇒ **우리 두 σ 솔버 (DEM 접촉망 · MPM STEP3 복셀) 가 내는 τ 는 전부 Nguyen 의 conventional τ 다.  τ_e 를 내는 경로는 리포에 없다.**

### Nguyen 한계가 우리에게 걸리는 방식 (COMSOL / P2D 입력 시)
| # | Nguyen 의 지적 | 우리에게 | 크기·조건 |
|---|---|---|---|
| ① | P2D 매개변수에는 τ_e 를 써라 (p5 · p8) — τ 는 계면 접근성을 표현 못 한다 (p7–8) | T 를 COMSOL τ_F 에 넣는 것은 Nguyen 이 반대한 **conventional 선택**이다 | 잘 퍼콜된 구 충전: +0.8 / +3.9 % (Fig 5) — 작다. dead-end 많음·구배: −46 % ~ +61 % (Fig 6) — 크고 **부호 불정**. 일반 보정계수 없음 |
| ② | 비관통이면 τ = ∞ 인데 전극은 작동한다 (p5) | LHS 130 중 **비관통 24** (CLAUDE.md J20-n) 는 T·τ_Lap = N/A 가 **정의상 맞다**. 그러나 "이온적으로 죽은 전극" 으로 읽으면 틀린다 — 같은 침대의 `ionic_active_pct` 는 유한 (경로 기준 고립 61–97 % ⇒ 활성 3–39 %, J20-p) | 이진 판정 (N/A) 과 접근성 (활성 %) 을 섞지 말 것 |
| ③ | dead-end 는 ε 에만 들어가 τ 를 키운다 (Fig 2: 같은 N_M 에서 τ −35 %) | φ_SE 가 비관통·고립 SE 까지 세므로 T 도 같은 방식으로 부푼다. **f (= 1/N_M) 가 ε 장부와 무관한 수송량** | 인계 열 계획 (f · T = φ/f · τ = √T) 에서 f 를 1차 수송량으로, T 는 "φ 규약 (구 부피 합 · 전체 SE)" 표지와 함께 |
| ④ | τ_e 는 방향 의존, τ 는 아니다 (Fig 6: 4.0 vs 11.9) | 두 단자 관통 문제는 위·아래를 바꿔도 같은 컨덕턴스 (가역성) → **T 는 방향 맹**. 플래튼 근처 밀도 구배 · graded-z (`--poro-grad`, A7) 를 율속 관점에서 순위 매길 수 없다 | 구배가 분리막 쪽이면 τ_e ↑ (Fig 6 ×2.98) |
| ⑤ | 실험 τ (차단 대칭셀 EIS-TLM) 는 τ_e 계열 | 우리 실험 앵커가 **어느 정의인지 앵커마다 다르다**: Bazzoun (카드 표기 "full-blocking 대칭셀 Z-type TLM") → eSCM 계열로 판독 · Minnmann (전자차단 셀 In/(InLi)ₓ \| LPSCl \| 복합양극 \| LPSCl \| In/(InLi)ₓ, T-type TLM — 카드 §2.2) → 이온 레일이 **양쪽 가역 전극**에 닿아 관통형에 가깝다 | [우리 카드 기술 기반 판독 — 원문 셀 배치 재확인 권장]. Bazzoun 의 "RNM < exp @ 80 wt%" 비교는 **정의가 다른 두 양**의 비교일 수 있다 (크기 미상) |
| ⑥ | 차단 TLM 은 r_el ≪ r_ion 가정 (Landesfeind, p9) · 이중층 = 기공벽 전체 | ASSB: 이온상 = 고체 SE · 이중층은 **AM(+탄소)–SE 접촉면만** · SE–SE 접촉은 Holm 협착 · σ_e/σ_ion 비가 조성마다 다르다 | Nguyen 의 τ_e 를 **그대로 이식할 수 없다** — ASSB 판 BC (축전 결합 = AM–SE 접촉에서만) 를 새로 세워야 한다 (§8 ②) |

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (값 자리표시 상태 — 비교는 코드 줄로 한다)
| 항목 | 이 논문 | 우리 | 같음/다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | 수송 **정의·경계조건** 논문 (액체 LIB, voxel) | DEM = 접촉망 σ 삼중항 · MPM STEP3 = 복셀 σ | 수송 쪽 절반만 다룬다. 압밀·형상·기계 = 없음 |
| 실험 vs 계산 | 두 **실험법**을 수치로 모사·비교 — 실험 데이터 없음 | 각 모델을 실험에 따로 보정 (frame[4]) | 이 논문의 "일치/불일치" 는 수치↔수치 — 실험 검증 아님 |
| τ 정의 | conventional τ (Eq 1) · electrode τ_e (Eq 2) | T = τ_Lap,eff² (conventional) 하나 + 기하 τ (Dijkstra 계열) | conventional 은 같음 · **τ_e 공백** |
| 관통 vs 접근 | eRDM 관통 · eSCM 편측 접근 + 이중층 | σ_full 관통 · `ionic_active_pct` 편측 (분리막 쪽, 이진) | 우리에게는 τ_e 의 **두 반쪽이 따로** 있다 (관통 저항 · 이진 접근성) — 저항 가중 접근성은 없다 |
| 계면 | 액체/고체 계면 전체 = 이중층 | AM–SE · SE–SE 점접촉 (Holm) | 액체 → ASSB 전이 불가 (BC 재설계 필요) |
| 협착 | 없음 | Holm 1/(2σa) · Stage-E 소성 면적 | 우리가 더하는 물리 (TauFactor 카드와 같은 논리) |
| 입자 | GeoDict 강체 구 · 압밀 없음 | DEM 압밀 강체구 + 연화 E_eff (접촉 소성 대리) · MPM 소성 형상 | 이 논문은 입자 물리 0 — 비교 대상 아님 |
| RVE / 해상도 | 50³–100³ voxel; 5 µm 구 침대는 대표성 의심 (TLM 이탈) | d_h/dx ≥ 3.5 규칙 · RVE ≥ 7.5× 최대입자 | 진단 철학 같음 — "모사 EIS 의 TLM 이탈" 은 우리에게 없는 진단 도구 |
| 방향성 | τ_e 방향 의존 | T 방향 맹 | 구배 침대 평가 불가 |
| 실험 앵커 τ | Thorat / Landesfeind / Malifarge 법 | Bazzoun · Minnmann · Kim 2025 TLM, Duquesnoy τ_TLM | 앵커별 정의 확인 필요 (§대조표 ⑤) |

- ⚠ **소재 전이**: 액체 전해질 (κ₀ 0.046 S/m, 10 mM TBAClO₄) · c_dl 0.01 F/m² — LPSCl 고체전해질과 무관. **정의·논리만** 전이, 숫자는 전이 금지.
- ⚠ 2D 사례 (Fig 2–4) 는 **개념 증명용 그림 구조** — 절대 크기 (예 +46.7 %) 를 우리 3D 침대 기대치로 쓰지 말 것. 3D 의 근거는 Fig 5 (구 충전 두 개) · Fig 6 (설계된 2층 하나) 뿐이다.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **웹앱 라벨 점검 대상 (메인 확인 요청)** — `app.py:1947 · 2050–2051 · 2140–2141 · 2615` 이 τ_Lap,eff 를 "COMSOL/EIS input" 으로 표시한다. (a) 메인 제공 COMSOL 5.6 Eq 6-6 (f_e = ε_p/τ_F) 이 맞다면 COMSOL 칸에 들어갈 값은 **T = τ_Lap,eff²** 이고, √T 를 넣으면 κ_eff 가 **√T 배 과대** (T = 4.3 이면 ×2.07, derived). (b) "EIS" — 차단 대칭셀 EIS-TLM 의 τ 는 Nguyen 분류로 **τ_e 계열**이고 우리 T 는 conventional 이라 같은 양이 아니다. (c) Nguyen 권고상 P2D/COMSOL 에는 τ_e 가 맞는데 우리는 그 양을 안 낸다. ⇒ 라벨을 "conventional (관통형) τ — COMSOL τ_F 에는 제곱값 T" 로 바꾸는 것이 최소 수정. (웹앱은 이 카드 범위 밖 — 판단·수정은 메인.)
- ② ★ **접촉망 τ_e 는 싸다 (제안 — 미구현)** — 우리 DEM 접촉망에는 이미 AM–SE 접촉면적이 있다. SE 망 + AM–SE 접촉마다 축전 결합 (ω→0 극한이면 균일 충전 전류 = 균일 sink) + AM 등전위 (σ_e ≫ σ_ion 일 때) + 분리막 쪽 띠 Dirichlet + 집전체 쪽 띠 차단 = **Nguyen eSCM 의 접촉망 판**. 희소 솔브 한 번 더. Eq 5 (Re Z → R_ion/3) 로 R_ion → τ_e. ASSB 에서 이중층이 AM(+탄소)–SE 접촉에만 있다는 점이 액체판과 다른 BC 다 (§대조표 ⑥).
- ③ **Nguyen 판별자 (dead-end 분율) 의 하한은 지금 출력에서 바로 나온다** — 분리막 쪽 (위 띠) 도달 SE (`dem_analysis_core.py` 의 `top_reachable_se`) − 관통 SE (`network_conductivity.py:552–557` 의 `perc_nodes`). 위상 기준 dead-end ⊆ flux 문턱 기준 dead-end (관통 성분의 저 flux 가지까지 포함) 이므로 **하한**. 작으면 (Fig 5: 4–8 %) T ≈ τ_e 기대, 크면 T 를 P2D 입력으로 신뢰하지 말 것. ⚠ `network_conductivity.active_fraction` 은 **바닥** 도달 기준 (`:1013–1016`) 이고 `ionic_active_pct` 는 **위(분리막) 띠** 기준 (`dem_analysis_core.py:743` "SE that reaches top (SE pellet)") — 기준면이 반대다. Nguyen 의 방향 논리로는 이온 접근성은 분리막 쪽 기준이어야 하므로 `active_fraction` 을 이온 "활성" 으로 읽지 말 것 [두 지표의 용도 구분은 메인 확인].
- ④ **비관통 24 침대 인계** — T·τ_Lap 열은 N/A 그대로가 맞다 (conventional τ = ∞). 0·임의값으로 채우지 말고, "전극 불능" 해석도 붙이지 말 것 (Nguyen p5). τ_e 열이 생기면 이 24 개가 τ 와 τ_e 가 가장 크게 갈리는 집합이다.
- ⑤ **graded / 방향** — A7 graded-z (`--poro-grad`) 와 플래튼 근처 밀도 구배는 T 로 비교하면 위·아래 뒤집은 설계가 같은 값을 받는다. Fig 6 의 ×2.98 이 그 맹점의 크기 예 (액체 2층 구조 하나 — 전이 아님).
- ⑥ **Duquesnoy 2020 의 TauFactor τ vs EIS τ_TLM 2.4–2.7× 괴리** (`duquesnoy2020_calendering_ml_mesostructure_generator`, TauFactor 카드 역링크 절) — 기존 판정은 "voxel 미해상". Nguyen 은 두 번째 후보를 준다: TauFactor mode 1 τ (관통) 와 대칭셀 EIS τ_TLM (τ_e 계열) 은 **다른 정의**. 다만 잘 퍼콜된 구조에서 정의 차는 ≤ 4 % (Fig 5) 이므로 2.4× 를 정의 차만으로 설명할 수는 없다 — 미해상이 주원인이라는 기존 판정은 유지, 정의 차는 보조 항.
- ⑦ **모사 EIS = RVE·균질화 진단** — 우리 STEP4 EIS 기능 (`eis_drt_ica.py`, CLAUDE.md 07-23) 이나 ② 의 접촉망 임피던스가 생기면, TLM 45° 이탈을 RVE 충분성·구배 진단으로 쓸 수 있다 (p6 · p8).

## 9. 인용 가능 문장 (deck/paper용)
- "Following Nguyen et al. (npj Comput. Mater. 6, 123, 2020), the network tortuosity factor T = φ_SE·σ_grain/σ_eff reported here is a conventional, flow-through tortuosity factor obtained between two Dirichlet boundaries; it is not the electrode tortuosity factor τ_e that those authors recommend for P2D parameterisation, and the two need not agree for dead-end-rich or graded microstructures."
- "In Nguyen et al.'s simulations the two definitions differed by only 0.8–3.9 % for well-percolated sphere packings (dead-end pore fractions of 4–8 %), but by −46 % to +61 % for a two-layer electrode depending on which side faced the separator — the conventional value cannot be corrected to τ_e by a universal factor."
- "Because the conventional tortuosity factor carries the full phase volume fraction in its numerator, non-percolating (dead-end) volume raises τ without changing the measured transport (MacMullin number); we therefore report f = σ_eff/σ₀ alongside T."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **"τ_e 가 P2D 예측을 더 잘한다" 는 이 논문에서 입증되지 않았다.** 권고는 모델 정합성 논리 (P2D 의 전하전달 차단 극한 = TLM) + 수치 예시에 근거한다. 실제 전극·성능 데이터 대조는 "follow-up study" 로 미뤘다 (p8). 인용 시 "recommended" 이지 "validated" 가 아니다.
- ⚠ **액체 전해질 LIB · voxel 연속체** — 점접촉 협착 없음, 입자 물리·압밀 없음 (구는 GeoDict 기하 생성). ASSB 로는 **정의 논리만** 전이한다 (§대조표 ⑥).
- ⚠ **2D 예시가 대부분** (Fig 2–4, MS Paint) · 3D 는 구 충전 2 개 + 설계된 2층 1 개, CV 50³–100³ voxel. 통계 (반복 실현·시드) 없음.
- ⚠ **τ_e − τ 의 부호는 일반적이지 않다** (Fig 3: τ_e < τ; Fig 4: τ_e > τ; Fig 6: 둘 다). 보정계수로 쓰지 말 것.
- ⚠ τ_e 추출은 TLM 가정 (r_el ≪ r_ion, 순수 축전, 균일 농도) 위에 있다 (p9) — ASSB 에서 r_el ≪ r_ion 은 조성마다 다르다.
- ⚠ **내부 불일치** (원문 그대로 두고 표지만): Fig 5 B ε (캡션 20 % ↔ τ/N_M 0.230) · Table 1 voxel 1 µm (가정) ↔ Fig 5 캡션 250 nm · dead-end 문턱 2 % (논문) ↔ 0.5 % (TauFactor 1.424.0 코드) · 인용번호 오기 (ref 30, ref 41) · "McMullin"/"Mullin".
- ⚠ **COMSOL 은 원문에 없다** — 원문은 P2D (Newman) · TLM 만 말한다. COMSOL τ_F 와의 대응은 메인이 준 COMSOL 5.6 Eq 6-6 위에서의 **우리 확장**이다.
- ⚠ 그림 수치는 모두 **그림 안 인쇄값** (축 판독 아님) — 정밀도는 인쇄 자릿수까지. 비율·역산 ε 은 derived.

## 11. 참고문헌 중 우리가 추가로 볼 만한 것 (원문 목록 그대로 · 이유 한 줄)
| ref | 서지 (원문 표기 그대로) | 왜 |
|---|---|---|
| 17 | Landesfeind, J., Hattendorff, J., Ehrl, A., Wall, W. A. & Gasteiger, H. A. Tortuosity determination of battery electrodes and separators by impedance spectroscopy. J. Electrochem. Soc. 163, A1373–A1387 (2016). | eSCM 원조 — 차단 대칭셀 TLM 의 가정·절차. 같은 묶음 inbox #5 (형제 카드) |
| 18 | Malifarge, S., Delobel, B. & Delacourt, C. Determination of tortuosity using impedance spectra analysis of symmetric cell. J. Electrochem. Soc. 164, E3329–E3334 (2017). | 고상 전자저항 임의값을 포함한 대칭셀 해석식 — ASSB 처럼 r_el ≪ r_ion 이 안 설 때 필요 |
| 20 | Pouraghajan, F. et al. Quantifying tortuosity of porous Li-ion battery electrodes: comparing polarization-interrupt and blocking-electrolyte methods. J. Electrochem. Soc. 165, 2644–2653 (2018). | eRDM vs eSCM **실측** 비교 + 접촉저항·R_ct 를 넣은 일반 TLM — 우리 σ_full ↔ TLM 앵커 비교의 실험판 |
| 28 | Usseglio-Viretta, F. L. E. et al. Resolving the discrepancy in tortuosity factor estimation for Li-ion battery electrodes through micro-macro modeling and experiment. J. Electrochem. Soc. 165, A3403–A3426 (2018). | 영상 기반 τ 와 실험 τ 의 괴리 해소 — Duquesnoy 2.4× · Bazzoun RNM<exp 같은 우리 괴리의 선행 분석 |
| 29 | Landesfeind, J., Ebner, M., Eldiven, A., Wood, V. & Gasteiger, H. A. Tortuosity of battery electrodes: validation of impedance-derived values and critical comparison with 3D tomography. J. Electrochem. Soc. 165, A469–A476 (2018). | 같은 전극에서 임피던스 τ 와 단층촬영 τ 직접 대조 — 정의 차의 실측 크기 |
| 42 | Cooper, S. J., Bertei, A., Finegan, D. P. & Brandon, N. P. Simulated impedance of diffusion in porous media. Electrochim. Acta 251, 681–689 (2017). | TauFactor mode 4 (확산 임피던스) 의 근거 + 부록에 eSCM 과의 수학 대응 (p10) — 접촉망 임피던스 구현 시 참고 |
| 16 | Thorat, I. V. et al. Quantifying tortuosity in porous Li-ion battery materials. J. Power Sources 188, 592–600 (2009). | eRDM 원조 · κ₀ 값 출처 |
| 12 | Zahn, R., Lagadec, M. F. & Wood, V. Transport in lithium ion batteries: reconciling impedance and structural analysis. ACS Energy Lett. 2, 2452–2453 (2017). | Eq 1 정의의 출처 (refs 11, 12) — τ vs N_M 표기 규약의 기준 |
| 33 | Morasch, R., Landesfeind, J., Suthar, B. & Gasteiger, H. A. Detection of binder gradients using impedance spectroscopy and their influence on the tortuosity of Li-ion battery graphite electrodes. J. Electrochem. Soc. 165, A3459 (2018). | 구배 전극의 방향 의존 τ 실측 — 우리 graded-z · PTFE/바인더 구배 논의 (litdb 에 이름만 2 곳 등장, 카드 없음) |
| 34 | Lu, X. et al. 3D microstructure design of lithium-ion battery electrodes assisted by X-ray nano-computed tomography and modelling. Nat. Commun. 11, 1–13 (2020). | 기하 tortuosity 로 구배 설계를 한 사례 (Nguyen 이 협착 무시로 비판) — 우리 벽 τ 를 설계 지표로 쓰면 같은 함정 |

## 용어 미니 사전
| 용어 | 뜻 |
|---|---|
| RDM / eRDM | restricted-diffusion method — 편극 후 이완 중 염 확산을 보고 D_eff 를 얻는 시간영역 법 / 전극용 변형 (Thorat) |
| SCM / eSCM | symmetric cell method — 고주파 임피던스로 κ_eff (분리막) / 차단 조건 대칭셀 + TLM 으로 전극 R_ion (Landesfeind · Malifarge) |
| τ (conventional) | 두 평행 경계 사이 관통 정상상태 flux 로 정한 tortuosity factor (Eq 1) |
| τ_e | 대칭셀 차단 임피던스의 R_ion 으로 정한 electrode tortuosity factor (Eq 2) — "한쪽 경계에서 고/액 계면까지 가기 어려움" 의 상대 척도 |
| N_M / N_M,e | MacMullin 수 = κ₀/κ_eff = τ/ε (ε 장부와 무관한 수송량) / τ_e/ε |
| through pore / dead-end pore | 분리막 쪽에서 집전체 쪽까지 이어진 기공 / 끝나거나 정상상태 flux 가 무시할 만한 기공 (flux < 최대 2 %) |
| A* · a | 집전체 면적당 미시 활성 면적 (= a·L) · 부피당 활성 면적 |
| TLM | transmission line model — r_ion · r_el · 계면 임피던스 z̃_t 의 분포 회로 (de Levie) |
| C_DL · c_dl | 집전체 면적당 이중층 용량 · 미시 활성 면적당 이중층 용량 |
| blocking condition | 비삽입 염 / 비삽입 상태로 전하전달을 막아 이중층 충전만 남긴 조건 |
| CV | control volume (모사 부피) |
| homogenisable | 다공 전극 이론 (P2D) 의 균질 매질 가정이 서는가 — TLM 이탈로 진단 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
