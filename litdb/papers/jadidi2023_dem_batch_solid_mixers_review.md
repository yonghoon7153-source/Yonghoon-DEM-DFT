<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# 배치(batch) 고체 믹서의 DEM 적용 **종합 리뷰** — 믹서 분류 · 혼합/분리 기전 · **혼합지수(mixing index) 8종 전수** · 접촉·점착모델 표준 · 보정 · coarse-graining · 미해결 목록 — Jadidi, Ebrahimi, Ein-Mozaffari, Lohi (*Reviews in Chemical Engineering* 39(5) 729–764, 2023; online 2022-03-28)

> slug `jadidi2023_dem_batch_solid_mixers_review` · DOI `10.1515/revce-2021-0049` · type `DEM (REVIEW — 배치 고체 믹싱; 7개 믹서족 문헌표 + 혼합지수 카탈로그)` · PDF `5629f9d5-07._A_comprehensive_review_of_the_application_of_DEM_in_the_investigation_of_batch_solid_mixers.pdf` · digested `2026-09-19` · status ✅

> ⚠ **연도 표기**: 정식 인용은 **Rev. Chem. Eng. 2023, 39(5), 729–764** (지면 2023-07-26), 온라인 선공개 **2022-03-28**, 접수 2021-06-06 / 채택 2022-02-22.  slug 은 지면 연도(2023)를 따랐다.  문헌관리자에 따라 `2022` 로 잡히는 판이 있으니 중복 검색 시 **두 연도 모두** 확인할 것.

> ★ **이 카드는 "물성 카드" 가 아니라 "분야 지도" 다.**  이 논문에는 우리가 옮겨 쓸 재료 수치(σ, E, porosity)가 **하나도 없다**.  대신 *"믹싱 DEM 이라는 분야에서 무엇이 표준이고 무엇이 미해결인가"* 의 목록을 준다.  우리는 이 분야에 **새로 들어가는 쪽**이고 현재 ① 전단 믹싱 공정 단계가 없고 ② 응집/분산 지표가 없다 (사전등록 `docs/reviews/prereg_m7_aggregation_20260919.md` §2).  그래서 이 카드의 무게중심은 **§4.7 (혼합지수 전수)** · **§4.3 (점착 모델·보정)** · **§4.5 (coarse-graining 판정)** · **§7 (우리 대비)** 다.

> ★ **자매 카드 (같이 읽을 것)**
> - `frankenberg2024_dem_high_intensity_mixer_assb` — **ASSB 고강도 건식 믹싱을 실제로 돌린 편**.  이 리뷰가 *"분야가 이렇게 한다"* 고 적은 것(coarse-graining f, JKR Γ, AOR 보정)을 **우리 소재계 근처에서 수치로** 보여준다.  ⇒ 리뷰 = 규범, Frankenberg = 실행 예.
> - `coetzee2017_dem_calibration_review` — 보정 방법론 리뷰.  이 리뷰 §5.1.2/§5.2.4 가 두 문단으로 압축한 것을 한 편으로 다룬다 (두 학파 · 해의 비유일성).
> - `bazzoun2026_dem_fem_rnm_ionic` / `bazzoun2025_dem_parameter_sensitivity_assb_cathode` — 우리 소재계(LPSCl+NMC811)의 **압밀·수송** 쪽.  믹싱 리뷰와 겹치지 않는다(믹서 없음) ⇒ **두 문헌군은 공정 단계가 다르다**.

---

## 1. 한 줄 요약

**[리뷰]** 배치 고체 믹서(텀블링·대류식) 연구에 DEM 이 어떻게 쓰였는지를 **7개 믹서족 × 문헌표(Table 7–13)** 로 전수 정리하고, 혼합/분리 기전 · 혼합지수 8종 · 접촉모델 표준 · 보정 절차 · 계산비용 대응책(GPU·coarse-graining·ML)을 한 편에 모은 뒤, **분야가 산업 수요와 어긋나 있다**는 정량 진단(비구형 20 % · 점착 18 % · 단분산 46 %)으로 끝난다.
**[우리]** 옮겨 올 값은 없고 **옮겨 올 것은 "지표의 이름과 식", "점착 보정의 표준 절차", "무엇이 아직 미해결인지"** 다 — 그리고 이 리뷰의 가장 유용한 사실 하나는 **혼합지수의 장단점을 이 리뷰가 스스로 평가하지 않고 다른 3편에 떠넘긴다**는 것(§4.7.3)이다.

---

## 2. 메타

| 저자 | 소속 | 저널/년 | DOI | 대상 | 연구유형 |
|---|---|---|---|---|---|
| **Behrooz Jadidi, Mohammadreza Ebrahimi, Farhad Ein-Mozaffari*(교신), Ali Lohi** | Department of Chemical Engineering, **Ryerson University**, 350 Victoria St., Toronto M5B 2K3, Canada | **Rev. Chem. Eng. 39(5) (2023) 729–764** (online 2022-03-28) | 10.1515/revce-2021-0049 | **배치(batch) 고체–고체 믹서** (연속식은 **명시적 제외**) | **리뷰** (문헌 종합 + 저자 자신의 권고) |

- 연구비: NSERC (캐나다).  이해충돌 없음 선언.
- 키워드(원문): batch mixing; discrete element method (DEM); mixing indices; mixing kinetics and mechanism; solid blending.
- ⚠ **저자군 자신이 이 분야의 원저자이기도 하다** — Ebrahimi 2018/2020, Yaraghi 2018, Jadidi 2022 (paddle blender) 가 Table 12 에 자기 논문으로 들어간다.  ⇒ paddle blender · RSD · granular temperature · particle diffusivity 쪽 서술은 **자기 계보의 강조**로 읽을 것.
- **⛔ 소재계 없음**: 이 리뷰는 제약·식품·화학 일반 분말이 대상이다.  **ASSB·전극·전해질은 한 번도 나오지 않는다.**  황화물·NMC·LPSCl 언급 0.  ⇒ 재료 전이는 **원리적으로 불가**, 전이 가능한 것은 **방법론·지표·진단**뿐.

---

## 3. 핵심 "수치" — 이 리뷰가 실제로 주는 정량

⚠ **물성 수치가 아니다.**  이 리뷰가 주는 숫자는 (a) 분야 통계 (b) 계산비용 규모 (c) 원저에서 옮겨 온 조건값 몇 개뿐이다.  **전부 stated (본문/그림 라벨), digitize 한 값 없음.**

| 양 | 값 | 출처 위치 | stated/digitized | 비고 |
|---|---|---|---|---|
| **비구형 입자를 넣은 연구 비율** | **20 %** (구형 80 %) | Fig 4(a) + 본문 §4 | stated | Tables 7–13 전수 기준 |
| **점착(cohesive) 분말을 다룬 비율** | **18 %** (비점착 82 %) | Fig 4(b) + 본문 §4 | stated | |
| **단분산 / 이분산 / 다분산 비율** | **46 % / 38 % / 16 %** | Fig 4(c) + 본문 §4 | stated | ★ 우리는 3종 = **16 % 쪽** |
| 시간스텝 규약 | Rayleigh time 의 **20–30 %** | §5.1.1 | stated | "usually no more than a **few microseconds**" |
| 시뮬 가능한 공정 시간 | **최대 수 분(a few minutes)** | §5.1.1 | stated | "in a reasonable time frame" |
| 문헌의 전형적 규모 | **최대 수십만 입자**, 입경 **밀리미터 급** | §5.1.1 | stated | ★ 우리 입경(≈1 µm)보다 **3 자릿수 크다** |
| 산업 규모 요구 | 수억~수십억 입자 = **현 하드웨어로 불가** | §5.1.1 | stated | |
| 비구형 접촉검출 비용 | 3D 다면체에서 전체 계산시간의 **80 %** | §5.1.1 · §6(1) (Zhong 2016 인용) | stated | |
| GPU 가속 | **40–75×** (단일 GPU vs 단일 CPU) | §5.2.1 (Gan 2016) | stated | "GPU 종류·알고리즘 의존" |
| 멀티 GPU | **18×** (32 GPU + MPI vs 단일 GPU) | §5.2.1 (Gan 2016) | stated | |
| coarse-grain 치환비 | CG 입자 1개 = 원래 입자 **l³ 개** (직경 l 배) | §5.2.2 (Sakai 2016) | stated | ★ 판정은 §4.5 |
| 텀블링 믹서 운전 | 회전 **최대 ~100 rpm**, 작업 충진율 **총부피의 50–60 %** | §1.1 (Niranjan 1994) | stated | |
| **[원저] 점착이 오히려 혼합을 돕는 구간** | `F_cohesion/W_p = 0.1` (매우 약한 점착) | Table 9 (Chaudhuri 2006) | stated | 회전드럼, avalanche·bed dilation 증가 |
| **[원저] 점착이 혼합을 망치는 구간** | **CED > 80 kJ m⁻³** | Table 9 (Yazdani & Hashemabadi 2019) | stated | SJKR, 회전드럼 |
| **[원저] 크기·밀도 차이** | "입자 간 **밀도 또는 크기 차이를 줄이면** 혼합 성능이 좋아진다" | Table 10 (Zhou 2003) | stated | ★ 우리 침대는 둘 다 크다 (§7) |
| **[원저] 다분산 ↔ 분리** | 다분산이 단분산보다 혼합도 **낮다**(분리 때문) / 그런데 **최종 혼합지수는 다분산 > 삼분산 > 이분산** | Table 9 (Alchikh-Sulaiman 2016) | stated | ⚠ 같은 논문 안에서 방향이 **반대로 읽히는 두 문장** — §4.7.5 |
| **[원저] 다분산이 분리를 줄인다** | "sieving(체거름) 분리는 **다분산도를 높이면 최소화**" · 다분산↑ → **응력 낮아짐** · 확산·대류 **둘 다 증가** | Table 10 (Remy 2011) | stated | 위 줄과 **정면 충돌** (다른 믹서·다른 지표) |
| **★★ [원저] 밀도차 > 형상차·크기차** | "일반적으로 **밀도가 다른 입자를 섞을 때** 형상이나 크기가 다른 경우보다 **혼합 성능이 더 나빴다**" | Table 9 (Hlosta 2020) | stated | ⚠ 리뷰 §2.2 의 *"크기 차이가 가장 영향력 있다"*(Alizadeh 2013)와 **충돌**.  우리 침대는 밀도차 ≈2.9× |
| **★★ [원저] 크기비 × 밀도비의 최적점** | "주어진 부피분율에서 **입자 밀도비와 크기비의 최적 조합**이 있었다" · "r_s, r_d, x_l 을 올리면 혼합지수가 **최대점까지 올라갔다가 그 뒤로는 내려간다**" | Table 10 (Halidan 2014, PMSI) | stated | ★ **비단조 최적** — 우리 12:4:1 × 2.9 가 그 최적의 어느 쪽인지 **모른다** |
| **[원저] 직경비가 크면 혼합 악화** | "선택한 **입자 직경비가 클수록 혼합 품질이 나빠졌다** (크기 분리 때문)" | Table 13 (Cai 2019, double-screw conical) | stated | 위 Halidan 의 "최대점 이후 하강" 과 같은 방향 |
| **★★★ [원저] 벌크 보정이 공정 예측으로 전이되지 않았다** | "보정 단계에서 DEM 과 **FT4 측정이 잘 맞았음에도 불구하고**, 믹싱 시스템 DEM 모델은 실험 혼합속도를 **정성적으로만** 예측할 수 있었다" | Table 12 (Pantaleev 2017, 점착·습윤 분말, Thakur 2014 모델) | stated | ★★ **AOR/FT4 보정의 한계를 문헌이 직접 보고한 유일한 줄** — §8-③ |
| **[원저] Froude 수 고정 스케일업** | "**Froude 수를 고정**하면 스케일업이 혼합 **품질**에는 영향을 주지 않았다.  단 혼합 **속도**에는 영향을 주었다" | Table 10 (Herman 2021) | stated | 스케일업 규칙 |

> ★ **읽는 법**: 마지막 두 줄이 이 리뷰의 성격을 그대로 보여준다 — **리뷰는 원저들의 결론을 나란히 놓기만 하고 충돌을 조정하지 않는다.**  "다분산이 분리를 늘린다(회전드럼, Lacey)" 와 "다분산이 분리를 줄인다(블레이드, 분리패턴)" 가 같은 리뷰 안에 무표시로 공존한다.  ⇒ **이 리뷰를 근거로 "다분산은 X 다" 라고 쓰면 안 된다.**

---

## 4. 방법론 — **리뷰가 적는 "분야 표준"** ★

### 4.0 리뷰의 구조 (무엇이 어디 있나)

| 절 | 내용 | 우리에게 |
|---|---|---|
| §1 · §1.1 · §1.2 | 믹서 분류: 텀블링 vs 대류식 (+Table 1, 2 장단점) | 배경.  **우리는 어느 쪽도 아니다** (§7) |
| §2.1 | 혼합 기전 3종 (대류·확산·전단) + Fig 1 | 용어 정의.  전단이 **응집 파괴**를 담당 |
| §2.2 | 분리(segregation) 기전 4종 + Fig 2 | ★ **2종이 우리 공정에도 산다** (§4.9.3) |
| §3.1 | 실험 특성화: invasive(시료채취) / noninvasive + Table 3 | 표본크기 경고가 **여기 한 줄만** 있다 |
| §3.2.1 | DEM 기본식 (1)(2) + 접촉모델 Table 4 + rolling resistance | ★ §4.2 |
| §3.2.2 | 기전 진단량: 식 (3)–(8) | ★ **우리가 하나도 안 재는 것들** (§4.8) |
| §3.2.3 | 혼합품질 평가 = **혼합지수** + Table 5 | ★★ §4.7 |
| §4 + Table 6, 7–13 + Fig 4 | 설계·운전 파라미터 영향 전수표 + 분야 통계 | §9 census |
| §5.1 | 난점: 계산시간 · 보정 · 최적화 비용 | ★ §4.3 · §4.4 |
| §5.2 | 해법: GPU/HPC · **scaling·coarse-graining** · data-driven/ML · 최적화 기반 보정 | ★ §4.5 · §4.6 |
| §6 | 결론 + **권고 4개** | ★ §10.3 미해결 목록 |

### 4.1 지배방정식 (원문 그대로)

```
m_i  d(v→_i)/dt = Σ_j^{Nc} ( F→_ij^{c,n} + F→_ij^{c,t} ) + Σ_k^{Nnc} F→_ik^{nc} + F→_i^{f−p} + F→_i^{ext}     (1)

I_i  d(ω→_i)/dt = Σ_j^{Nc} ( M→_ij + M→_ij_r )                                                              (2)
```

- `F→_ik^{nc}` = **비접촉력** — van der Waals, 정전기, 액체 브리지.  **[리뷰]** *"미세 입자를 다루거나 수분이 유동거동에 영향을 줄 때 중요해진다"* ⇒ 입자 종류·크기·운전조건에 따라 포함/배제.
- `F→_i^{f−p}` = 유체–입자 상호작용.  **[리뷰]** *"고체–고체 믹싱에서는 유체 효과가 입자 궤적에 무시할 만하므로 흔히 무시된다"*; 포함 여부는 **중력·항력·접촉력의 비**로 판단하라고 적는다.  CFD-DEM 은 계산시간을 크게 올린다.
- `M→_ij` : **구형 입자에서는 접선 성분에서만** 발생.  **비구형이면 법선 성분도 토크를 만든다** (Favier 1999).
- `M→_ij_r` (rolling resistance) : 접촉면의 불균일 압력에서 온다.  세 모델 — **Model A 일정토크 / Model B 점성 / Model C 탄소성 spring-dashpot**.  **[원저 Ai 2011]** *"Model C 가 가장 적합"*.

> ⚠ **[우리 분석]** 우리 덱은 rolling resistance 를 이 축에서 논의한 적이 없다.  구형 강체 가정 + `hooke/hysteresis` 라 **비구형 대리(rolling friction)** 라는 이 분야의 표준 우회로를 쓰지 않는다.  Frankenberg 는 `μ_r = 0.2` 로 **비구형을 rolling friction 으로 대리**했다 — 같은 문제를 그쪽은 우회했고 우리는 열어 둔 상태다.

### 4.2 접촉모델 — **Table 4 원문 그대로** (리뷰가 적는 "분야 표준 팔레트")

> 원문 제목: *Table 4: Summary of the common normal forces used in DEM.*

|  | **Elastic** | **Inelastic** |
|---|---|---|
| **Free flowing** | – Hertzian model (Norouzi et al. 2016)<br>– Linear spring model (Norouzi et al. 2016) | – **Hysteretic spring model** (Walton and Braun 1986a, 1986b) |
| **Cohesive** | – **JKR** (Barthel 2008)<br>– **DMT** (Prokopovich and Perni 2011) | – **Elasto-plastic adhesive models** (Hare et al. 2015; **Luding 2008**; Pasha et al. 2014; Thakur et al. 2014) |

- 법선력 모델의 상위 분류 4가지 **[리뷰, Alizadeh 2013 인용]**: ① continuous potential ② linear viscoelastic ③ nonlinear viscoelastic ④ **hysteretic**.
- 접선력: **[리뷰]** *"가장 흔하고 널리 적용되는 접선 접촉력 모델은 **Mindlin & Deresiewicz (1953)**"*.
- ⚠ **[리뷰가 하지 않는 것]** *"이 연구에서는 간결성을 위해 접촉모델과 그 식을 보고하지 않는다"* — **식이 한 줄도 없다.**  Norouzi 2016 / Kruggel-Emden 2007 / Zhu 2007 / Stevens & Hrenya 2005 로 넘긴다.  ⇒ **접촉모델 식이 필요하면 이 리뷰가 아니라 그 4편**이다.

> ★★ **우리 좌표 찍기**: 우리 생산 규약 `hooke/hysteresis` + `coefficientAdhesionStiffness` 는 Table 4 의 **[Free flowing × Inelastic] = Hysteretic spring (Walton–Braun)** 칸 + 점착항이다.  즉 **[Cohesive × Inelastic] = elasto-plastic adhesive (Luding 2008 계열)** 로 가는 문턱에 걸쳐 있다.  이 분야 표준으로 보면 우리 모델은 *"비점착 히스테리시스 + 점착 강성 한 항"* 이고, **JKR 계열(표면에너지 Γ)이 아니다** — 사전등록 `prereg_m7` §2-3 이 적은 그대로다.  ⇒ **리뷰가 우리 위치를 확인해 준다** (반박도, 승인도 아니다).

### 4.3 ★ 점착 분말 — 무엇을 쓰고 어떻게 보정하는가

**[리뷰 §5.1.2 원문의 파라미터 목록]**
> *"the DEM interaction parameters such as **coefficient of static and rolling frictions, coefficient of restitution, surface energy, plasticity ratio, and adhesion stiffness** as well as particle properties such as **shear modulus** are systematically varied and their influence on the **bulk response** (i.e. macroscopic response obtained from standard characterization tests such as **angle of repose or shear cell tests**) is monitored."*

여기서 우리에게 직접 걸리는 것 세 가지:

1. **`surface energy` 와 `adhesion stiffness` 가 같은 목록에 나란히 있다.**  이 분야는 두 파라미터화를 **같은 벌크 타깃(AOR/shear cell)에 맞추는 경쟁 노브**로 취급한다.
   ⚠ **그러나 이 리뷰는 둘 사이의 변환(예: `k_c ↔ Γ`)을 주지 않는다.**  어디에도 없다.  ⇒ 사전등록 `prereg_m7` §2-3 의 *"⬜ `k_c ↔ Γ` 관계는 미고정"* 은 **이 리뷰로 닫히지 않는다.**  닫으려면 접촉모델 원저(Luding 2008 · Pasha 2014 · Thakur 2014)로 내려가야 한다.
2. **보정 = 벌크 역보정이 표준이다.**  *"특정 입자·분말의 DEM 입력을 **직접 현미경 측정으로 얻는 것은 매우 어렵고 비싸며, 불가능하지는 않더라도**"* (Benvenuti 2016) ⇒ *"통상 보정은 **시행착오(trial and error)** 로 수행된다"*.
   ★ **안식각(AOR) 보정은 이 리뷰에서 "표준 절차" 로 명시된다** — 사용자 질문에 대한 답: **그렇다, 표준이다.**  단 리뷰는 그것을 *"느리고 자원 소모적"* 이라 부르며 §5.2.4 최적화 기반 보정으로 넘어간다.
   ⚠ **정밀화**: 리뷰는 AOR 을 **점착 전용 프로토콜**로 말하지 않는다 — 마찰·COR·표면에너지·강성을 **한꺼번에** 맞추는 벌크 타깃이다.  ⇒ **AOR 하나로 점착만 분리해 앵커할 수 없다** (해의 비유일성; `coetzee2017_dem_calibration_review` 가 이 지점을 다룬다).
3. **점착이면 보정이 더 어렵다.**  *"점착 입자를 시뮬레이션할 때 보정은 훨씬 더 어려워진다 — 접촉모델과 입자물성에 **사용자가 정해야 할 입력이 더 많기** 때문"* (Pantaleev 2017; Safranyik 2017).  **[리뷰의 인과 주장]** 이것 + 긴 계산시간이 *"점착 재료를 포함한 믹서 시뮬 연구가 문헌에 적은 이유"* 다 (= Fig 4(b) 의 18 %).

**[실제 쓰인 점착 접촉모델 — Table 9~11 에서 내가 확인한 것]**

| 모델 | 어디 | 비고 |
|---|---|---|
| **Hertz–Mindlin + JKR** | 회전드럼 (Sebastian Escotet-Espinoza 2018) | `표면에너지`를 노브로 스윕 |
| **Hertz–Mindlin + SJKR** (simplified JKR) | 회전드럼 (Yazdani & Hashemabadi 2019; 외 1) | `CED (cohesion energy density, J m⁻³)` 를 노브로 |
| **Hertz–Mindlin + van der Waals** | 블레이드 믹서 (Chandratilleke 2014), 리본 믹서 (Chandratilleke 2018) | 입자–입자 / 입자–벽 점착 분리 |
| **Walton & Braun (hysteretic) + square-well potential** | 회전드럼 (Chaudhuri 2006) | `F_cohesion/W_p` 무차원 점착수 |
| ★ **Visco-elasto-plastic adhesive (Thakur et al. 2014)** | **paddle blade blender** (Pantaleev 2017), Table 12 | ★★ Table 4 의 **[Cohesive × Inelastic] 칸을 실제로 쓴 유일한 연구**.  **dry and wet powder**(수분함량을 노브로 쓴 유일한 연구)이고, 보정·검증이 AOR 이 아니라 **FT4 분체 레오미터**다.  ⚠ 그리고 **이 리뷰에서 가장 중요한 경고**를 남긴다 — §9 표 참조 |
| **Luding 2008 자체** | Table 4 에 **범주 인용으로만** 등재 | Tables 7–13 의 어느 연구도 Luding 판을 쓰지 않았다 (같은 범주의 Thakur 판을 Pantaleev 가 씀) |

> ★★ **가장 값진 관찰 하나**: 점착의 세기를 재는 **노브가 논문마다 다르다** — `Γ (J m⁻²)` · `CED (J m⁻³)` · `F_cohesion/W_p (무차원)` · `van der Waals` 파라미터.  **리뷰는 이들을 비교 가능한 축으로 환산하지 않는다.**  ⇒ 우리 `k_c (N m⁻¹)` 가 이 목록에 **다섯 번째로 들어가도** 분야 안에서 이상한 일이 아니다; 이상한 것은 **아무도 환산표를 안 만들었다**는 것이다.  (우리가 만들면 그 자체가 기여다 — 단 *"만들어야 한다"* 는 우리 판단이지 리뷰의 주장이 아니다.)

### 4.4 계산비용 (§5.1.1) — 우리 규모와의 어긋남

- 시간스텝 = Rayleigh time 의 20–30 % → **수 µs 이하**.  *"미세(submillimeter) 분말을 시뮬할 때 더 심해진다 (더 작은 스텝이 필요하므로)"*.
- 전형 규모 = **수십만 입자 · mm 급 입경 · 실험실/파일럿 믹서**.
- ⇒ **[우리 분석 · 중요]** 이 분야가 표준을 세운 물성 영역은 **mm 급 자유유동 분말**이다.  우리 침대는 **µm 급 + 강점착(Bond 수 ≫ 1)** 이다.  **세 자릿수의 스케일 차**를 건너 이 분야의 *"보통 이렇게 한다"* 를 그대로 가져오면 안 된다.  이 리뷰 자신이 §5.1.1 · Fig 4(b) 로 *"점착 미세분말은 우리가 거의 안 해 봤다"* 고 인정한다.

### 4.5 ★ coarse-graining / scaling — **리뷰의 판정: 허용조건을 제시하지 않는다**

**[리뷰 §5.2.2 전문 요지 — 이것이 그 절의 *전부*다]**
- **scaling relationship**: *"관련 무차원수들을 원래 계와 스케일업 계에서 **일정하게 유지**한다(무차원 해석).  스케일업 시뮬에서는 **입자와 믹싱 시스템을 함께** 스케일한다.  … 스케일된 계와 원래 계의 **동역학적 거동의 유사성은 무차원 해석을 통해 보장된다** (Ding et al. 2001)."*
- **coarse-graining**: *"CG 입자는 원래 입자 직경의 **l 배**다.  즉 **l³ 개의 원래 입자가 CG 입자 1개로 대표**된다.  **운동방정식과 접촉모델은 CG 입자의 동역학적 거동과 원래 입자 집합의 평균 거동이 동일해지도록 조정된다** (Sakai 2016)."*
- *"유동층과 공기수송에서의 성공 사례가 보고되었고 **믹싱 시스템에도 적용될 수 있다**"* (Sakai 2012; Sakai & Koshizuka 2009).
- §6 권고 (2): 점착 미세분말은 **Thakur 2016 / Pantaleev 2017 의 particle scaling** + 최적화 기반 보정 + GPU 로 *"이제 합리적 시간 안에 가능해야 한다"*.

> ★★★ **판정 (정직하게)**: **이 리뷰는 coarse-graining 의 "언제 허용되는가 / 무엇이 깨지는가" 를 한 줄도 적지 않는다.**
> - 실패 모드 **미제시** (응집·점착·분리·표면적·접촉수 중 무엇이 안 보존되는지 없음).
> - 검증 기준 **미제시** (어떤 양이 l 에 불변이어야 하는지 없음).
> - 보존되는 것이 **"평균 거동"** 이라고만 적는다 — 어떤 평균인지 정의 없음.
> - 상한 l **미제시**.
> ⇒ 사용자 질문 *"리뷰의 판정은?"* 에 대한 답 = **판정이 없다. 전면 허용 서술이다.**
> ⚠ **이것을 "CG 가 안전하다" 로 읽으면 안 된다.**  실제 판정은 이 리뷰 밖에 있다 — 우리 리포 기준으로는 `frankenberg2024_dem_high_intensity_mixer_assb` 가 **force-scaling (접촉력 f², 겹침 f, 충돌시간 f)** 으로 *"무엇을 보존하려는지"* 를 식으로 적고 **AOR/SAOR/compaction 3단계로 검증**한 편이고, 그 카드가 이 축의 정본에 가깝다.
> ★ **우리에게 직접 걸리는 점**: 우리 18× E-연화(`E_SE 24 → 1.35 GPa`)는 *"계산 가능성을 위해 접촉 강성을 인위적으로 바꾸고 벌크 응답으로 정당화한다"* 는 점에서 **이 분야의 force-scaling 과 같은 인식론(frame [2])** 이다.  다만 **목적이 다르다** — 그들은 *입자 수*를 줄이려 하고, 우리는 *없는 기전(재배열·GB 슬라이딩·미세파괴)*을 흡수한다.  ⇒ *"문헌도 강성을 손댄다"* 를 우리 연화의 **면죄부로 쓰면 안 된다**; 같은 부류라는 것만 말할 수 있다.

### 4.6 데이터 기반 · ML · 최적화 기반 보정 (§5.2.3, §5.2.4)

- **시간 외삽** (Bednarek 2019; Doucet 2008): 수 초만 DEM 으로 돌리고 계의 특성·동역학을 뽑아 **긴 시간으로 외삽**.
- **ML + DEM** 두 용도: (i) 최적 설계·운전 탐색에 필요한 **시뮬 개수 감소** (ii) 수 분~수 시간 규모 **거동 예측**.
  ⚠ **[리뷰의 제한]** *"ML 은 **훈련에 쓴 설계공간 안에서만** 잘 작동하고, 비선형·복잡계에서는 **수 초~수 분의 DEM 이 훈련에 충분한 데이터를 주지 못할 수 있다**"*.
- **최적화 기반 보정** (§5.2.4) — DoE 는 여전히 시뮬을 많이 요구한다는 단점; 대안으로 **유전알고리즘(Do 2018) · 반응표면(Yoon 2007) · Kriging(Rackl & Hanley 2017) · 인공신경망(Benvenuti 2016) · generalized surrogate modeling(Richter 2020)**.  **[리뷰의 권고]** *"최적화 기반 보정이 보정 부담을 줄일 큰 잠재력을 보였다고 **우리는 믿는다**"*.

> ★ **[우리 분석]** 우리는 이 목록의 **인프라를 이미 갖고 있다** (Laplace 사후 PI · 중첩 CV · D-최적 배치제안 · GPR/RF).  다만 우리 ML 은 **구조→물성 예측**에 쓰고 **접촉 파라미터 보정**에는 한 번도 안 썼다.  리뷰가 권고하는 용법은 후자다.  ⇒ 우리가 빠뜨린 칸 (§10.4).

### 4.7 ★★ 혼합지수 (mixing index) — 전수 + 우리 판정

#### 4.7.1 Table 5 — **원문 그대로** (식·범위·사용처)

> 원문 제목: *Table 5: The summary of mixing/segregation indices and their applications.*
> **범위 열 = "완전 분리 – 완전 무작위"** (즉 `0–1` 은 *분리 0 → 무작위 1*, `1–0` 은 *분리 1 → 무작위 0*).

| # | 지수 (출처) | 식 (원문 그대로) | 범위 (분리→무작위) | 리뷰가 적는 사용처 |
|---|---|---|---|---|
| 1 | **Lacey index** (Lacey 1954) | `LI = (σ₀² − σ²) / (σ₀² − σ_r²)` | **0–1** | 블레이드 믹서 (Chandratilleke 2009, 2010, 2012, 2014), 리본 블렌더 (Basinskas & Sakai 2016a; Chandratilleke 2018; Gao 2019), slant cone (Alian 2015b), ploughshare (Alian 2015a; Hassanpour 2011), 회전드럼 (Alchikh-Sulaiman 2016; He 2019; Ji 2020; Liu 2013), double-screw conical (Cai 2019) |
| 2 | **Intensity of segregation** | `I_s = (σ² − σ_r²) / (σ₀² − σ_r²)` | **1–0** | 회전드럼 (Chaudhuri 2006; Qi 2017; Yazdani & Hashemabadi 2019), cone blender (Moakher 2000), bin blender (Portillo 2008) |
| 3 | **Relative standard deviation (RSD)** | `RSD = σ / C_avg` | **1–0** | paddle (Ebrahimi 2020, 2018; Jadidi 2022; Yaraghi 2018), bin-blender (Alexander 2004b; Arratia 2006a, 2006b), V-blender (Lemieux 2007), 블레이드 (Remy 2009, 2010a, 2010b, 2011), 회전드럼 (Sebastian Escotet-Espinoza 2018) |
| 4 | **Particle scale mixing index (PSMI)** (Chandratilleke 2012) | `PSMI = (S₀² − S²) / (S₀² − S_r²)` | **0–1** | 리본 (Halidan 2014), screw (Qi 2017), 블레이드 (Qi 2017) |
| 5 | **Siria mixing index** (Siiriä & Yliruusi 2009) | `S = Σ_{i=1}^{N} Σ_{j=1}^{N} M_ij / N²` | **0–1** | 회전드럼 (Wen 2015), multiple-spouted bed (Chen 2018; Wen 2015) |
| 6 | **Segregation index (SI)** (Stambaugh 2004) | `SI = C_AA/(C_AA + C_AB) + C_BB/(C_BB + C_AB)` | **2–0** | rotating (Hlosta 2020; Marigo 2012), hoop mixer (Marigo 2012), turbula (Marigo 2012) |
| 7 | **Graphic segregation index (GPSI)** (Dai 2020) | `GPSI = A_mg / A_fg` | **1–0** | vibrated bed (Dai 2020) |
| 8 | **Subdomain-based mixing index (SMI)** (Cho 2017) | `SMI = (1/N) Σ_{i=1}^{M} [ SMI(S_i) Σ_{k=1}^{Q} n_ki ]` | **0–1** | screw (Cho 2017), 리본 (Harish 2019) |

**⚠⚠ 이 표를 쓰기 전에 반드시 알아야 할 것 (정직):**
**리뷰는 이 식들의 기호를 한 번도 정의하지 않는다.**  본문에도, Nomenclature 에도 **`σ`, `σ₀`, `σ_r`, `C_avg`, `S`, `S₀`, `S_r`, `M_ij`, `C_AA`, `C_AB`, `C_BB`, `A_mg`, `A_fg`, `N`, `M`, `Q`, `n_ki`, `SMI(S_i)` 중 어느 것도 없다.**  Nomenclature 는 `LI = Lacey index` 처럼 **약어 풀이만** 한다 (실측 확인: p.758–759).
⇒ **이 카드의 식을 코드로 옮길 때는 원저를 열어야 한다.**  특히 `σ₀`(완전분리 분산)·`σ_r`(완전무작위 분산)의 정의는 표본 정의에 따라 달라지고, 그 선택이 바로 아래 §4.7.4 의 함정이다.

#### 4.7.2 세 계열 분류 (리뷰가 **인용**하는 분류 — 저자 자신의 것이 아니다)

**[리뷰 §3.2.3]** *"Bhalode & Ierapetritou (2020) 가 흔히 쓰는 혼합지수들을 비판적으로 리뷰했다.  저자들은 계산 방법에 따라 세 그룹으로 분류했다: **(1) variance-based, (2) distance-based, (3) contact-based**."*

| 계열 | Table 5 에서 해당 | 필요한 것 | 우리 관점 |
|---|---|---|---|
| **variance-based** (분산 기반) | LI, I_s, RSD, PSMI | **표본(셀/그리드/시료)** 정의 | ⚠ 표본 크기·개수·위치에 **직접** 의존 |
| **distance-based** (거리 기반) | (Table 5 에 명시 대응 없음; 최근접 이웃 계열) | 이웃 탐색 반경 | 반경 선택이 노브 |
| **contact-based** (접촉 기반) | **SI (Stambaugh)**, (Siiriä `M_ij` 도 이 계열로 읽힘 — ⚠ 리뷰가 확인해 주지 않음) | **접촉/이웃 쌍 카운트** | ★★ **우리 `E_XY` enrichment 가 여기다** (§7·§8) |

> ★★★ **이것이 이 카드의 가장 실용적인 한 줄이다**: 사전등록 `prereg_m7` §4 의 주지표
> `E_XY = n_XY / n_XY^random`,  `n_XY^random = N_contact · (2 − δ_XY) · f_X · f_Y`
> 는 **분야 분류상 `contact-based` 지수**이고, **Stambaugh 의 SI 와 같은 재료(상쌍별 접촉수 `C_AA`, `C_AB`, `C_BB`)로 만들어진다.**  즉 우리가 새 지표를 발명한 것이 아니라 **이름 있는 계열에 착지한 것**이다 — 그리고 우리 정규화(무작위 기대 대비)는 SI 의 정규화(`C_AA/(C_AA+C_AB)`)와 **다르다**(우리 쪽이 조성 보정을 명시적으로 한다).  ⇒ 논문에 쓸 때 *"contact-based mixing index (cf. Stambaugh et al. 2004), normalised to the random-mixing expectation"* 로 **계보를 붙일 수 있다**.

#### 4.7.3 ★ 리뷰가 어느 것을 **권고**하고 어느 것을 **피하라** 하는가 — **판정: 둘 다 하지 않는다**

사용자 질문에 대한 직답:

1. **권고 없음.**  리뷰가 §3.2.3 에서 내리는 유일한 결론은 **사용 빈도 서술**이다: *"Table 5 를 근거로, **RSD 와 Lacey 혼합지수가 문헌에서 가장 흔히 쓰이는 혼합지수**라고 결론지을 수 있다."*  ⇒ **"가장 흔하다" 는 "가장 좋다" 가 아니다.**  리뷰는 그 둘을 권고하지 **않는다**.
2. **기피 권고 없음.**  어떤 지수도 *"쓰지 말라"* 고 하지 않는다.
3. **장단점 평가를 남에게 넘긴다.**  *"Wen et al. (2015) 가 여러 혼합지수를 상세히 정리하고 **각각의 장단점을 평가**했다.  … Deen et al. (2010) 이 네 가지 혼합지수를 비교했다. … Bhalode & Ierapetritou (2020) 가 **비판적으로 리뷰**했다.  **독자는 이 문헌들을 참고하라.**"*
   ⇒ **[우리 행동]** 지표 선택의 근거가 필요하면 이 리뷰가 아니라 **Bhalode & Ierapetritou 2020 (Powder Technol. 373: 195–209)** · **Wen 2015 (Procedia Eng. 102: 1630–1642)** · **Deen 2010 (Ind. Eng. Chem. Res. 49: 5246–5253)** · Fan 1970 (Ind. Eng. Chem. 62: 53–69) 을 **따로 digest 해야 한다** (§10.4 목록에 올림).

#### 4.7.4 ⚠⚠ **격자 / 표본크기 의존** — 리뷰에 무엇이 있고 무엇이 **없나**

**있는 것 — 딱 한 문장, 그것도 실험 쪽이다 (§3.1):**
> *"It is also worth mentioning that the **sample size, number of samples** taken from a mixing system, and the **location of sampling points** can affect the **accuracy of the mixing assessment** (Poux et al. 1991)."*

**없는 것 (전수 검색으로 확인):**
- **"scale of scrutiny"** — 전문에 **0 회**.  (분산 기반 지수의 고전적 핵심 개념인데 등장하지 않는다.)
- **DEM 측 격자/셀/빈(bin) 분할에 대한 서술** — `grid` · `cell`(shear cell 제외) · `bin`(bin blender 기기명 제외) · `sub-domain` 의 방법론적 논의 **0 회**.
- **표본 수렴 시험 / 셀 크기 민감도** — **0 회**.
- **그래서 SMI(Cho 2017)를 "Subdomain-based" 라 부르면서도** subdomain 을 어떻게 나누는지, 그 선택이 값에 어떻게 걸리는지 **적지 않는다**.
  ⚠ 추가 관찰: **원저 제목은 *"A non-sampling mixing index for multicomponent mixtures"*** 인데 리뷰의 라벨은 *"Subdomain-based mixing index"* 다.  **"non-sampling" 과 "subdomain-based" 는 같은 말이 아니다.**  ⇒ 이 지수를 쓰려면 **원저에서 직접 확인**해야 한다 (리뷰의 라벨을 신뢰하지 말 것).

> ★★ **판정**: 사용자가 물은 *"격자/표본크기 의존 서술"* 은 **이 리뷰에 사실상 없다.**  실험 시료채취에 대한 한 문장이 전부이고, **DEM 으로 지수를 계산할 때의 셀 분할 의존은 다뤄지지 않는다.**
> ⚠ **이것이 우리에게 왜 중요한가 (우리 분석)**: 우리 리포는 *"부분집합 필터로 훑으면 조용히 초록이 된다"*(규율 ⑤)와 **격자 미수렴**(복셀 vox 스윕)으로 두 번 데였다.  분산 기반 혼합지수는 **정확히 같은 구조의 함정**이다 — 셀을 크게 잡으면 `σ → σ_r` 이 되어 **어떤 침대든 "잘 섞였다"** 가 나온다.  그래서 `prereg_m7` §4 가 *"격자·구간 나누기가 필요 없다"* 는 이유로 접촉 enrichment 를 주지표로, Lacey 를 **부지표로만** 둔 것은 **이 리뷰와 무관하게 내린 판단인데, 이 리뷰의 공백이 그 판단을 반박하지 않는다** (지지하지도 않는다 — 리뷰가 말이 없으므로).

#### 4.7.5 ⚠⚠ **입자 크기 차이 편향** — 리뷰에 **없다**

- Table 5 의 어떤 지수도 **입자 크기/질량/부피 가중**을 언급하지 않는다.  `σ` 가 **개수 분율**의 분산인지 **질량 분율**의 분산인지 리뷰는 **말하지 않는다**.
- 크기 차이는 리뷰에서 **분리(segregation)의 원인**으로만 다뤄진다 (§2.2: *"입자 크기 차이가 분리에 가장 영향력 있는 파라미터"* — Alizadeh 2013).  **지수의 편향 요인으로는 한 번도 다뤄지지 않는다.**
- 가장 가까운 것은 **[원저] Ebrahimi 2020 (Table 12)**: *"**particle number ratio 가 혼합 성능에 가장 큰 영향**을 미쳤다; particle number ratio 를 줄이면 혼합 성능이 악화되었다."*  ⇒ 개수비가 결과를 지배한다는 관측은 있는데, **그것이 지수의 인공물인지 물리인지 리뷰는 구분하지 않는다.**
- 그리고 §3 표의 **모순 쌍**(Alchikh-Sulaiman 2016: 다분산 혼합도 ↓ / 최종 혼합지수 ↑)은 **정확히 이 미해결 지점의 증상**으로 읽힌다 — 다만 **그렇게 읽는 것은 우리 해석이고 리뷰의 주장이 아니다.**

> ★★ **[우리 분석 — 카드 밖으로 인용할 때 반드시 라벨할 것]**: 우리 생산 침대의 크기비는 **12 : 4 : 1 (AM_P : AM_S : SE)** 이고 `r_SE = 0.5 µm` 이 생산 기본값이다 (출처 = 리포 규범 문서; 정본 기준값 문서는 아직 자리표시).  ⇒ **부피비 1728 : 64 : 1** 이다.  이 상태에서 **개수 기반 분산 지수**(RSD/Lacey)를 셀에 적용하면, 같은 부피에 들어가는 SE 개수가 AM_P 보다 **세 자릿수** 많아 **σ 가 SE 통계에 지배**된다.  ⇒ **우리 침대에 RSD/Lacey 를 바로 쓰면 "SE 가 얼마나 고르게 흩어졌나" 만 재고 AM 은 거의 안 보이게 된다.**  이것은 **리뷰가 경고하지 않는 함정**이고, 그래서 `prereg_m7` 의 주지표(접촉 enrichment, 조성으로 정규화됨)가 우리 경우에 더 안전하다.  ⚠ 단 **접촉 기반도 크기 편향이 없지는 않다** — 큰 입자는 이웃이 많아 접촉 카운트를 더 많이 만든다.  `prereg_m7` §5 가 *"`E_SE-SE(A) > 1` 자체는 판정이 아니다 — 입자 크기 차이만으로도 접촉 통계가 기운다; 판정은 **팔 사이 차이**로만"* 이라고 못 박은 것이 바로 그 대응이다.  **이 리뷰는 그 대응을 제공하지 않는다 — 우리가 이미 갖고 있다.**

#### 4.7.6 Table 5 **밖에서** 실제로 쓰인 지표·진단량 (Tables 7–13 에서 수집; 전수 아님)

리뷰의 "Parameters calculated to analyze mixing quality" 열에 실제로 등장하는 것들 — **Table 5 에 없는 것이 절반이다**:

- **Weak and strong sense mixing index** (Alizadeh 2014b, 회전드럼) — ★ Table 5 에 **없는 지수**
- **Granular temperature** (Remy 2009/2010b, Ebrahimi 2018, Jadidi 2022, 블레이드/paddle)
- **Particle diffusivities** / **Diffusion coefficient** (Remy 2009/2010b, Ebrahimi 2018/2020, Jadidi 2022, Chandratilleke 2018)
- **Axial dispersion coefficient** (Tahvildarian, Sebastian Escotet-Espinoza 2018, Alizadeh 2014b)
- **Mixing time** · **Mixing kinetics** (Arratia 2006a; Remy 2011; Sebastian Escotet-Espinoza 2018)
- **Interparticle forces / force network / contact forces (particle–particle, particle–wall)** (Chandratilleke 2009/2010; Halidan 2018; Chandratilleke 2018; Ebrahimi 2018)
- **Normal and shear stress profile** · **particle bed pressure** · **shear stress** (Remy 2009/2011)
- **Dimensionless shear rate** · **particle collision energy** (Nakamura 2013, high-shear)
- **Velocity fields / mean velocity / velocity profile / relative velocity after collision** (다수)
- **Circulation intensity** (Tahvildarian, V-blender) · **Variances of the transportation velocity (VTV)** (Basinskas & Sakai 2016b)
- **Segregation patterns** (Remy 2011) · **Segregation mechanisms** (Arratia 2006a) · **Mixing mechanisms** (다수)
- **Energy consumption** (Ren 2013, tote blender)
- **Centroid angle** (Pachón-Morales 2020, 비구형+점착 드럼) — ★ Table 5 에 **없는 지수**
- **PMSI** (Halidan 2014, Table 10) — ⚠ **Table 5 의 `PSMI` 와 철자가 다르다**(같은 particle-scale 지수를 가리키는 것으로 보이나 리뷰가 확인해 주지 않는다)
- **Bulk density · void fraction · solid fraction** (Boonkanokwong 2016), **bulk density · total energy** (Pantaleev 2017)
- **Impeller torque · power consumption** (Boonkanokwong 2018), **device power consumption · collision energy distribution** (Cai 2019), **force and torque on blades** (Herman 2021)
- **Visual observation** (Qi 2017) — 정성 판정도 "지표" 열에 그대로 올라간다
- ⛔ **배위수(coordination number)** — **한 번도 나오지 않는다.**  **τ(굴곡도) · percolation · 전도도(이온/전자/열)** 도 **0 회**.
  ⚠ **정밀화**: *"porosity 도 0 회"* 는 **틀리다** — `void fraction`·`solid fraction`·`bulk density` 는 등장한다 (Boonkanokwong 2016; Pantaleev 2017).  다만 그것은 **충진 상태의 스칼라**이고, 우리가 쓰는 **연결성 기반 구조량**(배위수·τ·percolation)은 **하나도 없다**.
  ⇒ ★ **분야 경계가 여기서 드러난다**: 믹싱 DEM 은 **운동학·응력·균질도(+충진 스칼라)** 를 재고, **수송 구조(연결성)** 는 재지 않는다.  그것은 우리(+ `bazzoun2026`, `sangros2020`) 쪽 문헌군의 소관이다.

### 4.8 기전 진단량 — 식 (3)–(8) 원문 그대로 ★

**[리뷰 §3.2.2]** "혼합 *기전*(mechanism)을 DEM 으로 평가하는 법" — 지수(§4.7)가 *결과*를 재는 것과 달리 이쪽은 *과정*을 잰다.

**① 확산계수 (i 방향 확산 / j 방향 조성구배)** — Yaraghi 2018
```
D_ij = ( Δx_i − Δx̄_i )( Δx_j − Δx̄_j ) / (2 Δt)        (3)
```
`Δx_i` = i 방향 입자 변위, `Δx̄_i` = 전체 입자의 i 방향 **평균 변위**.
⚠ **원문에 앙상블 평균 기호가 인쇄되어 있지 않다** (식 (6)은 본문이 ⟨⟩ 를 언급하는데 인쇄된 식에는 그것도 없다).  ⇒ **식을 코드로 옮길 때 평균 연산자를 원저에서 확인할 것.**

**② 전단이 있는 경우의 확산계수 (선형 관계)** — Hwang & Hogg (1980), 경사면 건조분말 혼합
```
D_ij = D₀ ( 1 + α ∂v→_i/∂j )                           (4)
```
`D₀`, `α` = 상수.

**③ Peclet 수 (확산 vs 대류)** — Yaraghi 2018
```
Pe_ij = U_i L_c / D_ij                                  (5)
```
`U_i` = i 방향 평균속도, `L_c` = 믹서의 특성길이.
**[리뷰의 판정 규칙]** `Pe < 1` → **확산 지배**; `Pe > 1` → **대류 지배**.

**④ Granular temperature** — Boonkanokwong 2016
```
T = (1/3) u′ u′                                         (6)
```
`u′` = 각 입자의 **변동속도**(제어체적 내 입자군의 평균속도를 개별 속도에서 뺀 것), ⟨⟩ = 제어체적 내 **시간 평균** (본문 서술; 인쇄식엔 기호 없음).
**[리뷰의 해석]** `T` ↑ = 속도 변동 ↑ = 유동 균일도 ↓ = **확산 기전의 기여가 크다**.  그리고 *"확산과 전단은 보통 함께 일어나므로 **전단 기전의 강도도 granular temperature 로 가늠**할 수 있다"* (Sacher & Khinast 2016) ⇒ **T 가 높은 영역 = 전단율이 높은 영역**.

**⑤ 정규화 전단율 분포 (x–y 평면)** — Radl 2010, 블레이드 믹서를 연속체로 보고
```
γ* = √[ 2*(∂U*/∂x*)² + 2*(∂V*/∂y*)² + (∂U*/∂x* + ∂V*/∂y*)² ]     (7)
```
`U*, V*` = 임펠러 속도로 정규화한 x·y 평균속도, `x*, y*` = 믹서 반경으로 정규화한 좌표.

**⑥ 충돌 응력 (제어체적 `V_c`)** — Campbell (2002), Remy 2010b 사용
```
τ_ij = (d_p / V_c) F_i k_j                              (8)
```
`d_p` = 입자 직경, `F_i` = i 방향 접촉력, `k_j` = j 방향 단위벡터.

> ★ **[우리 분석 — 가장 값진 전이 가능성]** 식 (3) 의 `D_ij` 는 **입자 재배열(rearrangement)의 직접 관측량**이다.  우리는 그 재배열을 **관측하지 않고 `E_eff` 18× 연화 안에 뭉쳐 넣었다** (frame [2]).  ⇒ **압밀 중 `D_ij` 를 재면, 지금까지 "보이지 않는 기전" 이던 것이 관측량이 된다.**  이것은 새 물리가 아니라 **이미 있는 덤프로 계산 가능한 후처리**다 (변위 시계열만 있으면 된다).  ⚠ 단 *"연화가 재배열의 프록시" 라는 우리 주장이 `D_ij` 로 검증된다* 고 말하려면 **압밀 단계별 `D_ij` 와 연화 계수 사이의 예측을 런 전에 등록**해야 한다 — 지금 말할 수 있는 것은 *"재볼 수 있다"* 까지다.

### 4.9 분야 구조 — 믹서 · 기전 · 분리 · 실험

#### 4.9.1 믹서 분류 (§1.1, §1.2 + Table 1, 2)

| | **텀블링 믹서** (tumbling) | **대류식 믹서** (convective) |
|---|---|---|
| 구조 | 용기 자체가 축 둘레로 회전 (부분 충진) | 용기 고정 + **임펠러/패들/리본/plough** 회전 |
| 지배 기전 | **확산(diffusive)** | 보통 **대류(convection)** > 확산 (⚠ 반례 있음: Ebrahimi 2018, Yaraghi 2018 은 대류식에서 **확산이 지배**라고 보고) |
| 종류 | twin-shell(V) · tote · double-cone · horizontal rotary.  **V(twin-shell)가 가장 널리 쓰임** | 수평: 리본 · ploughshare · paddle · sigma blade / 수직: **high-shear** · screw · bladed.  단축/쌍축 |
| 운전 | ~100 rpm, 충진율 50–60 % | 광범위 |
| **장점** (Table 1/2) | 저비용 유지보수(세척·비움) · 시료채취 용이 · 최종 혼합물 완전 배출 | 배치·연속 **둘 다** 가능 · **자유유동·점착 둘 다** 적용 · 용량 범위 넓음 |
| **단점** (Table 1/2) | 배치만 · 배출 중 **de-mixing** · **분리 가능성 높음** · **점착 재료에 부적합** | 유틸리티·유지비 높음 · **시료채취 어려워 혼합품질 분석 복잡** · 세척 어려움 |
| 혼합 속도 | 느림 (충분한 시간이면 균질 달성) | 빠름 |

**[리뷰]** *"전단 기전은 **응집체(agglomerate)를 깨는 데 필수적 역할**을 한다.  따라서 **점착 분말을 혼합할 때는 전단 기전이 지배적인 믹서가 유리하다**"* (Hogg 2009).

#### 4.9.2 혼합 기전 3종 (§2.1, Fig 1)

- **대류(convective)**: 인접 입자들이 **덩어리로** 한 위치에서 다른 위치로 이동.  **가장 빠르고**, 용기 전체에 분포시킨다.
- **확산(diffusive)**: 미시적 **무작위** 운동으로 상대 위치가 바뀜.  **미시적 균질화에 필수**, 가장 좋은 무작위 혼합을 주지만 **느리다**.
- **전단(shear)**: **속도가 다른 입자 층 사이의 운동량 교환** → 일부 입자가 다른 층으로 이동.  임펠러 근처(속도 분포가 넓은 곳)와 **벽 근처(압축·팽창)** 에서 발달.  ★ **응집 파괴 담당.**
- **[리뷰]** 셋은 항상 **동시에** 일어나고, 믹서 종류·운전조건(초기 적재 패턴·회전속도)·유동성에 따라 **하나가 지배**한다.

#### 4.9.3 ★ 분리(segregation) 기전 4종 (§2.2, Fig 2) — **우리 공정에 2종이 산다**

| 기전 | 구동 | 유체 필요? | **우리 침전·압밀에서?** |
|---|---|---|---|
| **trajectory** (궤적) | 유체–입자 상호작용 | **예** | ⛔ 없음 (유체 없음) |
| **elutriation** (비산) | 유체–입자 상호작용 | **예** | ⛔ 없음 |
| **percolation / sifting** (체거름) | **입자 크기 차이** — 큰 입자 사이 틈으로 **작은 입자가 아래로 미끄러진다** | 아니오 | ✅ **살아 있다** — 우리 SE(작다)가 AM 틈으로 내려간다 |
| **push-away** (밀어냄) | **밀도 차이** — 고밀도 입자가 가벼운 둘을 밀어냄 → 무거운 쪽이 중앙, 가벼운 쪽이 벽으로 | 아니오 | ✅ **살아 있다** — 같은 소재계의 문헌값 ρ_CAM 4.77 vs ρ_SE 1.64 g cm⁻³ ≈ **2.9×** (출처 = `bazzoun2026_dem_fem_rnm_ionic` 카드; ⚠ **우리 덱의 실제 입력 밀도는 별도 확인 필요**) |

**[리뷰]** *"모든 물성 차이가 분리를 일으킬 수 있지만, **혼합물 내 입자 크기 차이가 가장 영향력 있는 파라미터**"* (Alizadeh 2013).  형상도 축방향·반경방향 분리에 유의한 영향 (He 2019, 2021).  **[리뷰]** 분리는 *"입자 물성과 운전조건을 바꿔 줄일 수 있다"* (Tang & Puri 2004; Rhodes 2008).

> ★★ **[우리 분석]** 이것이 **믹서가 없는 우리도 이 분야의 언어를 쓸 수 있는 이유**다.  percolation 과 push-away 는 **유체도 임펠러도 필요 없다** — 중력·진동·재배열만 있으면 된다.  우리 `insert/pack → 정착 → 압밀` 은 그 조건을 **전부** 만족한다.  ⇒ `prereg_m7` 이 재려는 *"점착 비대칭이 만드는 상별 분리"* 는 이 분야 용어로 **"percolation/push-away 에 점착이 얹힌 경쟁"** 이고, 그렇게 이름 붙이면 리뷰의 문헌 기반 위에 올라탈 수 있다.
> ⚠ **그러나 "믹싱" 이라 부르면 안 된다** — `prereg_m7` §2-1 이 이미 못 박았고, 이 리뷰의 정의(§2.1: 혼합은 대류·확산·전단 기전으로 **불균일을 줄이는 조작**)로도 우리 공정은 **혼합 조작이 아니다**.  **리뷰가 우리 사전등록의 금지 조항을 독립적으로 지지한다.**

#### 4.9.4 실험 특성화 (§3.1, Table 3) — 우리가 참고할 것

| | 장점 | 단점 |
|---|---|---|
| **Invasive** (시료채취, Thief sampler — side/end/core) | 구현 쉬움 · 비용 효율 | 시료기 삽입으로 **분체층 파괴** · 유동경로 교란 · 정확도 낮음 · **벽 근처 접근 불가** |
| **Non-invasive** (영상 해석 · 분광 · 단층촬영; PEPT · PIV · RPT · NIR · X-ray) | **인라인 측정** · 다양한 계에 적용 | 비쌈 · 구현 번거로움 |

**[리뷰의 결론]** *"실험만으로 고체 혼합 공정을 상세히 분석하는 것은 **불가능(not feasible)** 하다 — 이것이 입자 시뮬레이션의 필요성을 뒷받침한다"*.
Tables 7–13 에서 실제로 쓰인 검증 수단(내 집계, 근사): **PEPT** 가 가장 많고 → **영상해석** → **PIV** → **thief sampling** → NIR · RPT · core sampling · **동적 안식각(DAOR, Jadidi 2022)** · **FT4 분체 레오미터(Pantaleev 2017)** · optical visualization (Qi 2017) · 육안 관찰.
⚠ **벌크 시험은 AOR 하나가 아니다** — 리뷰 본문이 *"angle of repose **or shear cell tests**"* 라 적고, 실제 표에는 **FT4 레오미터**도 쓰였다.

---

## 5. Figure / Table set ★

| # | 내용 | 우리가 참고할 점 |
|---|---|---|
| **Fig 1** | 혼합 기전 3종 모식도 (a) 대류 (b) 확산 (c) 전단 | 발표 슬라이드용 용어 그림.  **우리 공정에는 (b) 만 있고 (a)(c) 가 없다**는 것을 이 그림 위에 표시하면 한 장으로 설명된다 |
| **Fig 2** | 분리 기전 4종 (a) trajectory (b) elutriation (c) percolation(sifting) (d) push-away | ★★ **우리 침전·압밀에 (c)(d) 만 산다**는 §4.9.3 판정을 그대로 얹을 그림 |
| **Fig 3** | Newton 2법칙 + 접촉모델의 DEM 적용 모식 | 교육용.  새 정보 없음 |
| **Fig 4** | ★ **분야 통계 원형그래프 3장**: (a) 구형 80 / 비구형 20 % (b) 비점착 82 / 점착 18 % (c) 단 46 / 이 38 / **다 16 %** | ★★ **우리 위치를 한 장으로 주장**할 수 있는 유일한 그림 — 우리는 3종(다분산) = **16 %** 쪽, 점착 켜면 **18 %** 쪽 |
| **Table 1 / 2** | 텀블링 / 대류식 장단점 | 배경 |
| **Table 3** | invasive vs noninvasive 장단점 | 실험 협업 시 |
| **Table 4** | ★ **법선 접촉력 표준 팔레트 2×2** | ★★ **우리 모델의 좌표를 찍는 표** (§4.2) |
| **Table 5** | ★★ **혼합/분리 지수 8종 + 식 + 범위 + 사용처** | ★★★ 이 카드 §4.7.1 에 전재 |
| **Table 6** | 혼합에 영향 주는 파라미터 3분류 (운전 / 설계 / 입자물성) | 설계변수 체크리스트 |
| **Table 7** | cone blender 문헌표 (Moakher 2000, Arratia 2006a, Ren 2013, Alian 2015b) | — |
| **Table 8** | V-blender (Lemieux 2007, Tahvildarian, Alizadeh 2014a) | — |
| **Table 9** | ★ **회전드럼** (Chaudhuri 2006, Marigo 2012, Alizadeh 2014b, Alchikh-Sulaiman 2016, Sebastian Escotet-Espinoza 2018, He 2019, Yazdani & Hashemabadi 2019, Hlosta 2020 …) | ★ **점착 스윕이 여기 몰려 있다** (JKR/SJKR/square-well) |
| **Table 10** | ★ **블레이드/고전단 믹서** (Zhou 2003, Remy 2009/2010b/2011, Chandratilleke 2009/2010/2014, Nakamura 2013 …) | ★ **다분산 · 표면거칠기 · 점착 findings** |
| **Table 11** | 리본 블렌더 (Basinskas & Sakai 2016a, Halidan 2018, Chandratilleke 2018, Gao 2019) | 점착 vs 비점착 최적 rpm 비교 |
| **Table 12** | ploughshare / paddle (Alian 2015a, Ebrahimi 2018/2020, Jadidi 2022 …) | 저자 자신 계보 · **DAOR 검증** |
| **Table 13** | screw blender (Qi 2017, Cho 2017 …) | — |
| **Nomenclature** (p.758–759) | 기호표 | ⚠ **혼합지수의 내부 기호(σ₀, σ_r …)는 여기 없다** (§4.7.1) |

---

## 6. Post-processing ★ — 이 리뷰가 적는 후처리 목록

리뷰 자체가 후처리를 수행하는 논문이 아니므로, **"이 분야가 DEM 출력으로 무엇을 만드는가"** 의 목록이다:

1. **혼합지수** (§4.7) — 표본(셀/시료) 단위 조성 → 분산 → LI / I_s / RSD / PSMI, 또는 입자 단위 → PSMI / SMI, 또는 접촉/이웃 카운트 → SI / Siriä.  ⚠ **도구·구현 언급 없음** (어떤 코드로 어떻게 셀을 나누는지 리뷰에 없음).
2. **기전 진단** (§4.8) — 변위 시계열 → `D_ij` (식 3) → `Pe` (식 5); 속도장 → `T` (식 6), `γ*` (식 7); 접촉력 → `τ_ij` (식 8).
3. **힘/응력장** — interparticle force, force network, particle–wall contact force, normal·shear stress profile, bed pressure.
4. **운동학장** — 속도장·평균속도·순환강도·축방향 분산계수·VTV.
5. **에너지** — 충돌 에너지, 비파워/에너지 소비.
6. **실험 대조** — PEPT/PIV/RPT 궤적 vs DEM 궤적, thief sampling vs 셀 조성, **DAOR(동적 안식각) vs 시뮬 안식각**, **FT4 분체 레오미터 vs DEM**(Pantaleev 2017).
7. **DEM 코드** — 리뷰가 이름을 대는 것: **LIGGGHTS** (Berger 2015 의 MPI/OpenMP 하이브리드 병렬화 맥락), **MFIX DEM** (Amritkar 2014; Liu 2014).  ⚠ 상용(EDEM/Rocky) 이름은 §5 본문에 나오지 않는다.

> ⚠ **[정직]** 이 리뷰에는 **후처리 도구 체인(스크립트·라이브러리·워크플로)에 대한 서술이 사실상 없다.**  "무엇을 계산하는가" 는 있고 "어떻게 계산하는가" 는 없다.  ⇒ 구현은 원저로.

---

## 7. ★★ 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⚠ **먼저 적는 제약**: 이 브랜치의 `our_dem_baseline.md` 는 **값 0개의 자리표시**다.  아래 "우리" 열의 수치는 **리포 규범 문서(CLAUDE.md) 기준**이며, 정본 기준값 문서로 확인된 것이 아니다.  ⇒ 이 표를 **원고에 그대로 인용하지 말 것**; 대조의 *구조*만 쓸 것.

| 항목 | 이 리뷰(= 믹싱 DEM 분야) | 우리 (DEM+MPM) | 같다/다르다 · 왜 |
|---|---|---|---|
| **공정 단계** | 회전/임펠러 **믹서 안의 혼합** | `insert/pack` → **정착** → **플래튼 압밀** (믹서 없음) | ⛔ **다르다 — 근본적으로.**  우리는 이 리뷰의 대상이 아니다.  전이 가능한 것은 지표·진단·보정뿐 |
| **혼합 기전** | 대류 · 확산 · 전단 (셋 다) | **확산(재배열)만** — 대류·전단을 만드는 기구가 없다 | ⛔ 다르다.  ⇒ 우리 계에서 *"전단으로 응집을 깬다"* 는 경로가 **없다** (Hogg 2009 의 권고를 못 쓴다) |
| **분리 기전** | 4종 (trajectory · elutriation · percolation · push-away) | **percolation + push-away 만** 작동 (유체 없음) | ✅ **부분적으로 같다** — §4.9.3.  두 기전은 우리 침대에서도 물리적으로 살아 있다 |
| **입자 형상** | 구형 **80 %** / 비구형 20 % | **구형 100 %** (강체) | ✅ 같다(분야 다수파) · ⚠ 우리는 **MPM 에서 형상 소성**을 따로 가진다 = frame [5] 로 보완 |
| **점착 모델** | JKR(Γ) · SJKR(CED) · vdW · square-well · (범주로) elasto-plastic adhesive | `hooke/hysteresis` + **`coefficientAdhesionStiffness` (k_c)** | ⚠ **다르다 — 파라미터화가 다르다.**  리뷰는 `k_c` 형 파라미터를 **보정 목록에 이름으로 인정**하지만 **JKR Γ 와의 환산은 주지 않는다** |
| **점착 보정** | **AOR / shear cell 벌크 역보정이 표준**, 통상 시행착오 | ⛔ **없다** — 우리 `m7` 값들은 **벌크 앵커가 없다** | ❌ **우리가 빠진 칸.**  `prereg_m7` 이 A/B/C 를 **상대 비교**로만 판정하게 설계된 이유이자 한계 |
| **혼합지수** | LI · I_s · RSD · PSMI · Siriä · SI · GPSI · SMI (RSD·Lacey 최빈) | ⛔ **없다** (배위수 `se_se_cn`·`am_se_cn` 은 있으나 지수로 변환 안 함) | ❌ **우리가 빠진 칸** — 단 `prereg_m7` 이 `E_XY`(contact-based) + CLMI(Lacey, 부지표)로 **메우는 중** |
| **지표 계열** | variance / distance / **contact** 3계열 (Bhalode 2020 분류) | `E_XY` = **contact-based**, CLMI = variance-based | ✅ **우리 선택이 이름 있는 계열에 착지한다** (§4.7.2) — 논문에 계보를 붙일 수 있다 |
| **표본크기·격자 의존** | ⛔ **리뷰가 다루지 않는다** (실험 시료채취 한 문장뿐) | `prereg_m7` 이 **격자 불요 지표를 주지표로** 선택 + Lacey 를 부지표로 강등 | ✅ **우리가 더 보수적이다.**  ⚠ 리뷰가 우리를 지지하는 것이 아니라 **말이 없는 것**이다 |
| **크기 차이 편향** | ⛔ **다루지 않는다** (크기차는 "분리의 원인"으로만) | `prereg_m7` §5 가 *"`E > 1` 자체는 판정이 아니다 — 크기차만으로도 접촉 통계가 기운다"* 로 명시 대응 | ✅ **우리가 앞선다** (분야 공백을 우리가 이미 막아 둠) |
| **다성분** | 단 46 / 이 38 / **다 16 %**.  §6 권고 (4): *"대부분 단·이분산, **같은 밀도·같은 형상**만 봤다 — 다분산·밀도차·형상차를 연구하라"* | **AM_P · AM_S · SE 3종**, 크기 3종 + **밀도 2.9× 차** | ✅ **우리가 분야 권고의 목표 지점에 이미 있다** = 강한 포지셔닝 문장 |
| **입자 크기** | **mm 급**이 표준 | **µm 급** (r_SE ≈ 0.5 µm) | ⚠ **3 자릿수 차** — 이 분야의 경험칙·보정값·Bond 수 체제가 **그대로 전이되지 않는다** |
| **계산 대응책** | GPU(40–75×) · CG(l³) · 시간 외삽 · ML | GPU(Taichi/MPM) 사용 · **CG 미사용** · 우리 ML 은 **구조→물성** | ⚠ 우리는 CG 를 안 쓴다 (RVE 가 작아 필요가 없었다) — 이 축은 우리에게 **비활성** |
| **강성 인위 조정** | force-scaling / CG 접촉모델 조정 (§4.5) | **18× E-연화** (24 → 1.35 GPa) | ⚠ **같은 부류, 다른 목적.**  그들 = 입자 수 감축 / 우리 = 없는 기전 흡수.  ⛔ *"문헌도 하니까 괜찮다"* 로 쓰지 말 것 |
| **수송(σ) / 연결성** | ⛔ **0 회** (배위수·τ·porosity·전도도 전부 없음) | σ_ionic·σ_e·σ_thermal 삼중항 + percolation + coverage | ✅ **우리 고유 — 분야 경계 밖**.  frame [5] "DEM = 수송" 이 이 리뷰로 **다시 확인**된다 |
| **소성 형상변화** | ⛔ 없음 (전 문헌 강체 구) | **MPM 이 담당** | ✅ 우리 고유.  Varkey/Bazzoun 과 같은 결론 — **믹싱 DEM 도 frame [1]/[2] 의 같은 결손을 갖는다** |
| **실험 검증 수단** | PEPT · PIV · RPT · thief · NIR · **DAOR** | porosity · 두께 · EIS(문헌 앵커) | ⚠ **다른 관측량**.  PEPT/PIV 는 **궤적**을 보고 우리는 **최종 구조**를 본다 ⇒ 직접 대조 불가 |

### 7.1 통제해야 할 교란 (real difference vs method artifact)

1. **믹서 유무 = 방법 차이가 아니라 *공정* 차이다.**  이 리뷰의 어떤 정량 결론(최적 rpm, 최적 충진율, 블레이드 각도)도 우리에게 **의미가 없다**.  전이 가능한 것은 **지표의 정의**와 **분리 기전의 이름**뿐.
2. **mm ↔ µm.**  분야 경험칙은 mm 급 자유유동 분말에서 나왔다.  점착 지배 체제(Bond ≫ 1)는 리뷰 자신이 **18 % 만 다뤘다**고 인정한 영역이다.
3. **개수 통계 ↔ 부피 통계.**  분산 기반 지수의 `σ` 가 개수 분율 기준이면 우리 침대에서는 SE 가 통계를 지배한다 (§4.7.5).  **가중 규약을 정하지 않고 값을 비교하면 그 차이는 물리가 아니라 규약이다.**
4. **리뷰의 라벨을 원저의 주장으로 읽지 말 것.**  실측 사례: SMI 를 *"Subdomain-based"* 라 부르는데 원제는 *"non-sampling"* 이다 (§4.7.4).
5. **digitize 한 값 없음** — 이 카드의 모든 수치는 stated.  단 **내가 센 census(§9)는 근사**이며 리뷰의 Fig 4 통계와 **다르다**(줄바꿈·"continued" 중복 때문).  **인용은 Fig 4 쪽으로.**

---

## 8. 적용 인사이트 — `prereg_m7` 에 직접 걸리는 것

### ① ★★ `E_XY` 에 **계보**를 붙일 수 있다 (즉시 사용 가능)
`prereg_m7` 주지표는 분야 분류상 **contact-based mixing index** 이고 (Bhalode & Ierapetritou 2020 의 3계열 중 하나), 재료(상쌍별 접촉수)가 **Stambaugh 2004 의 SI** 와 같다.
⇒ 원고 문장: *"contact-based segregation metric (cf. Stambaugh et al., Phys. Rev. E 70 (2004); classification per Bhalode & Ierapetritou, Powder Technol. 373 (2020) 195), normalised to the random-mixing expectation."*
⚠ **SI 자체를 우리 값으로 계산하지는 말 것** — 범위 `2–0` 규약과 정규화가 달라 우리 `E_XY` 와 직접 비교되지 않는다.  **계보만** 인용.

### ② ★★ 부지표 CLMI(Lacey)에 **가중 규약**을 런 전에 못 박아야 한다
리뷰가 `σ₀`·`σ_r` 를 정의하지 않고(§4.7.1) 가중도 말하지 않으므로(§4.7.5), **우리가 정해야 한다**.
⇒ `prereg_m7` 개정 시 추가할 한 줄: *"CLMI 의 `x_i` 는 입자 `i` 의 이웃 중 다른 상의 **개수 분율**로 정의한다 (부피 가중 아님).  `σ_r²` 는 같은 개수 분율에 대한 이항 기대값."*  **런 뒤에 정하면 사전등록이 아니다.**

### ③ ★ 점착 노브의 **벌크 앵커 부재**가 분야 기준으로도 결손이다
리뷰는 보정(AOR/shear cell)을 *"현실적 결과의 열쇠"* 라 부른다 (§5.1.2 첫 문장).  우리 `m7` A/B/C 는 그 앵커가 없다.
⇒ ⛔ **결론을 절대값으로 쓰지 말 것** — `prereg_m7` 이 이미 *"팔 사이 차이로만 판정"* 으로 설계했으므로 **판정은 유효**하다.  다만 *"우리 k_c 가 실제 분말의 점착을 재현한다"* 는 주장은 **못 한다**.  앵커를 원하면 **AOR 시뮬 + 실측 AOR** 한 쌍이 최소 비용 경로다 (Frankenberg 가 정확히 그 3단계를 밟았다).
⚠⚠ **그러나 앵커를 붙여도 정량 예측이 보장되지 않는다** — 이 리뷰 안의 **Pantaleev 2017 (Table 12)** 가 정확히 그 실험을 했다: 점착·습윤 분말 + **visco-elasto-plastic adhesive (Thakur 2014)** 모델 + **FT4 레오미터 보정** → *"보정 단계에서는 근접 일치했지만 믹싱 모델은 혼합속도를 **정성적으로만** 예측했다"*.
⇒ **[우리 판단]** AOR 앵커의 값어치는 *"절대 예측"* 이 아니라 *"우리 k_c 가 실물 분말의 어느 밴드에 있는지"* 를 말해 주는 것까지다.  그렇게 **한정해서** 계획할 것.  (이것은 `prereg_m7` 의 상대-비교 설계를 **약화시키지 않는다** — 오히려 그 설계가 옳았다는 문헌 근거다.)

### ④ ★ `D_ij`·`Pe`·`T` 는 **지금 있는 덤프로 잴 수 있다**
식 (3)(5)(6) 은 변위·속도 시계열만 요구한다.  우리 압밀 런의 atom 덤프에 이미 있다.
⇒ **재배열을 처음으로 *관측량*으로 만드는 경로.**  ⚠ 연화(frame [2])와의 연결 주장은 **런 전 등록 없이는 금지** — 지금 말할 수 있는 것은 *"측정 가능하다"* 까지.

### ⑤ ★ 분리 기전 이름표 (발표·원고에서 바로 쓸 수 있다)
*"믹서 없는 정착·압밀에서도 **percolation(크기)** 과 **push-away(밀도, 같은 소재계 문헌값 기준 ρ_CAM/ρ_SE ≈ 2.9 — Bazzoun 2026)** 는 유체 없이 작동한다 — trajectory·elutriation 만 유체를 요구한다 (Rhodes 2008, via Jadidi 2023 §2.2)."*
⇒ *"우리 계에 분리 물리가 있다"* 를 **문헌 정의로** 정당화하는 가장 짧은 경로.

### ⑥ ★ 포지셔닝 문장 (Fig 4)
*"DEM mixing studies are 80 % spherical, 82 % non-cohesive and 46 % mono-disperse (Jadidi et al. 2023, Fig. 4); tri-component, size-disparate, cohesive beds — ours — are the 16 % / 18 % corner the review itself calls the gap between academia and industry."*

---

## 9. Tables 7–13 census — **내가 센 것 (근사)** + 전이 가능한 원저 findings

⚠ **아래 빈도는 내가 PDF 표에서 센 것이고 근사다** (줄바꿈으로 한 항목이 쪼개지고, "(continued)" 헤더가 중복된다).  **정량 인용은 리뷰 자신의 Fig 4 로 할 것.**

**접촉모델 빈도(근사 순위)**: `Hertz–Mindlin` 계열이 압도적 1위 → `Zhou et al. (1999)`(rolling friction 포함 모델) → `Tsuji et al. (1992)` → `Walton & Braun`(hysteretic) → `linear spring-dashpot` → 점착 변형(`+JKR` 1, `+SJKR` 2, `+van der Waals` 2, `+square-well` 1).
**혼합지수 빈도(근사)**: **Lacey ≫ RSD** > Intensity of segregation > Segregation index ≈ granular temperature > PSMI ≈ Siriä ≈ SMI.  (리뷰 자신의 서술: *"RSD 와 Lacey 가 가장 흔하다"* — 순서는 내 집계와 반대이나 **둘이 최빈이라는 점은 일치**.)
**검증수단 빈도(근사)**: PEPT > 영상해석 > PIV > thief sampling > NIR ≈ RPT ≈ core sampling ≈ DAOR ≈ 육안.

**전이 가능한 원저 findings (전부 [원저] 표기 — 리뷰의 주장이 아니다):**

| 출처 (Table) | 문장 | 우리에게 |
|---|---|---|
| Zhou 2003 (T10) | *"입자 간 **밀도 또는 크기 차이를 줄이면** 혼합 성능이 향상"* · *"작은 입자는 바닥에, 큰 입자는 위에 모였다"* | ★ 우리 침대는 **둘 다 크다** ⇒ 분리 구동력이 강한 설계라는 것을 문헌으로 말할 수 있다 |
| Chaudhuri 2006 (T9) | *"점착 증가 → **avalanche 크기와 분체층 팽창(dilation) 증가**"* · *"**매우 약한 점착**(`F_cohesion/W_p = 0.1`)에서는 점착 입자가 자유유동보다 **더 잘** 섞였다"* | ★★ **점착이 단조롭게 나쁘지 않다** — 약한 점착은 bed dilation 을 통해 재배열을 **돕는다**.  `m7` 의 A(비대칭) 팔이 B/C 보다 **더 섞일** 가능성을 미리 배제하지 말 것 |
| Yazdani & Hashemabadi 2019 (T9) | *"**CED > 80 kJ m⁻³** 인 강점착에서 CED 를 더 올리면 혼합 성능 **악화**"* · *"서로 다른 점착 입자 사이에 **입자간 점착이 없으면 균일 혼합이 달성되지 않았다**"* | ★★ **비대칭 점착(우리 A 팔)이 균일화를 방해할 수 있다**는 직접 선례 — `m7` h1 방향과 **부합** (⚠ 회전드럼·SJKR·다른 소재계) |
| Chandratilleke 2014 (T10) | *"**강점착**에서는 분체층이 **들려서(lifted)** 블레이드와 상호작용이 제한 → 혼합 무력"* · *"**입자–벽 점착을 줄이면** 혼합 성능 향상"* | 우리는 블레이드가 없어 첫 줄은 비적용; **입자–벽 점착** 축은 우리 플래튼/벽에 존재 (미탐색) |
| Halidan 2018 (T11) | *"점착·비점착 **둘 다 최적 임펠러 속도는 100 rpm**"* · *"충진율과 **점착성(cohesiveness)이 올라가면 혼합 품질 악화**"* · *"2-blade 리본은 점착 재료에 부적합"* | 점착 ↑ → 혼합 ↓ 의 일반 경향 |
| Remy 2011 (T10) | *"**다분산도를 높이면 sieving 분리가 최소화**"* · *"다분산도 ↑ → **응력 낮아짐**"* · *"입자 확산도와 대류 **둘 다 증가**"* | ★ **다분산이 분리를 줄인다**는 반대 방향 증거 — §3 의 모순 쌍 |
| Alchikh-Sulaiman 2016 (T9) | *"다분산 혼합물의 혼합도는 단분산보다 **낮았다**(분리 때문)"* · *"**최종 혼합지수는 다분산 > 삼분산 > 이분산**"* | ⚠ 같은 논문의 두 문장.  **지표와 시점(최종 vs 과정)이 다르면 결론이 뒤집힌다**는 증거 |
| Remy 2010b (T10) | *"**표면 거칠기**와 블레이드 속도가 혼합에 유의한 영향"* · *"거칠기 ↑ → 속도변동·bed dilation·granular temperature·확산도 **모두 증가**"* | ★ 거칠기가 **재배열을 키운다** — 우리 B3 표면거칠기 보정(수송 전용)과 **다른 축**(역학 축) |
| Ebrahimi 2020 (T12) | *"**particle number ratio 가 혼합 성능에 가장 큰 영향**; 줄이면 악화"* | ★ 개수비 지배 — 우리 3종 개수비는 극단적(SE 가 압도적 다수) |
| Nakamura 2013 (T10) | *"**일정 임펠러 tip speed** 가 서로 다른 용기 크기에서 내부 전단유동 크기와 충돌에너지의 유사성을 보장"* | 스케일업 규칙 (우리 RVE 에는 비적용) |
| Alizadeh 2014b (T9) | *"**정지마찰 계수와 Young's modulus 가 입자 혼합 동역학에 유의한 영향**"* | ★★ **E 가 혼합 동역학을 바꾼다** — 우리 18× 연화가 **재배열 통계까지 바꿀 수 있다**는 경고(같은 방향의 독립 관측) |
| **★★★ Pantaleev 2017 (T12)** | *"DEM 모델과 실험 결과는 건조·습윤 분말 **둘 다에서 정성적으로 잘 맞았다**"* · *"**보정 단계에서 DEM 과 FT4 측정이 근접 일치했음에도 불구하고, 믹싱 시스템 DEM 모델은 실험으로 측정한 혼합속도를 정성적으로만 예측할 수 있었다**"* | ★★★ **이 카드에서 가장 중요한 한 줄.**  분야 표준인 **벌크 보정이 공정 예측으로 자동 전이되지 않는다**는 것을 원저가 직접 보고한다.  ⇒ 우리가 AOR 앵커를 붙여도 **정량 예측이 보장되지 않는다** (§8-③).  ⚠ 점착 노브를 쓴 유일한 elasto-plastic adhesive 연구에서 나온 결과라 **가장 우리와 가까운 선례** |
| **★★ Hlosta 2020 (T9)** | *"일반적으로 **밀도가 다른 입자를 섞을 때** 형상이나 크기가 다른 경우보다 **혼합 성능이 더 나빴다**"* · *"충진율이 혼합 균질도에 가장 큰 영향"* · 최적 충진율이 구형(40–50 %)과 **날카로운 형상(30–40 %)** 에서 다르다 | ★★ **밀도차가 크기차보다 나쁘다** — 리뷰 §2.2 의 "크기차가 제일 중요" 와 **충돌**.  우리 AM/SE 밀도비 ≈2.9 를 **크기비만큼 중요한 축**으로 볼 근거 |
| **★★ Halidan 2014 (T10)** | *"주어진 부피분율에서 **입자 밀도비와 크기비의 최적 조합**이 최선의 혼합 성능을 주었다"* · *"r_s·r_d·x_l 을 올리면 혼합지수가 **최대점까지 증가한 뒤 감소**"* | ★★ **비단조**.  우리처럼 크기비·밀도비가 **둘 다 큰** 계가 그 최적의 어느 쪽인지 모른다 ⇒ *"우리 조성이 패킹에 최적" 과 "혼합/분산에 최적" 은 다른 질문* |
| Cai 2019 (T13) | *"**입자 직경비가 클수록 혼합 품질이 나빠졌다** (크기 분리 때문)"* | 12:4:1 은 **큰** 직경비다 |
| Herman 2021 (T10) | *"**Froude 수 고정**이면 스케일업이 혼합 **품질**엔 영향 없고 **속도**엔 영향 있다"* · 스케일업 비·Froude 수로 혼합속도·속도·힘·토크 **상관식 유도** | 스케일업 규약 (우리 RVE 에는 비적용) |
| Pachón-Morales 2020 (T9) | 비구형+점착 드럼, **centroid angle** 지표; *"점착이 커지면 centroid angle 증가"* | 점착 → 정적 구조 기울기 증가 (AOR 류) |
| Ji 2020 / He 2020·2021 (T9) | *"비구형의 혼합속도가 구형보다 **빨랐다**"*(Ji) / *"구는 대류혼합이 **낮고** 확산혼합이 **높다**"*(He 2020) / *"형상이 다르면 **축방향 분리**; 구는 중앙, 타원체는 주변"*(He 2021) | ⚠ Govender 2018 은 반대(*"구형 쪽이 최종 지수에 더 빨리 도달"*) — **또 하나의 미조정 충돌** |

---

## 10. 주의 / 한계 / 미해결

### 10.1 이 리뷰를 인용할 때 (over-claim 방지)
- ⛔ **재료 수치 0.**  σ·E·porosity·점착 에너지의 **절대값을 이 리뷰에서 가져올 수 없다**.
- ⛔ **혼합지수 식의 기호가 정의되어 있지 않다** (§4.7.1).  구현은 반드시 원저로.
- ⛔ **지수의 장단점 평가가 이 리뷰에 없다** (§4.7.3).  *"Jadidi 리뷰가 X 지수를 권고한다"* 는 문장은 **쓸 수 없다**.
- ⛔ **격자/표본크기 의존, 크기차 편향 서술이 없다** (§4.7.4–5).  그 경고를 이 리뷰 인용으로 달면 **날조**다.
- ⛔ **coarse-graining 의 허용조건·실패모드가 없다** (§4.5).  *"리뷰가 CG 를 검증했다"* 로 읽지 말 것.
- ⚠ **접촉모델 식이 한 줄도 없다** (저자가 명시적으로 생략).
- ⚠ **저자군 자신의 논문이 Table 12 에 있다** (Ebrahimi·Yaraghi·Jadidi) — paddle/RSD/granular temperature 계보의 강조를 감안할 것.
- ⚠ **원저들의 결론 충돌을 조정하지 않는다** — 실측 3쌍: ① 다분산이 분리를 늘린다(Alchikh-Sulaiman) ↔ 줄인다(Remy 2011) ② 크기차가 가장 중요(§2.2, Alizadeh 2013) ↔ **밀도차가 더 나쁘다**(Hlosta 2020) ③ 비구형이 더 빨리 섞인다(Ji 2020) ↔ 구형이 더 빨리 최종값에 도달(Govender 2018).
- ⚠ **리뷰 내부 불일치 2건 (실측)**: ① Table 5 의 `PSMI` 가 Table 10 에서는 `PMSI` 로 적힌다. ② Table 5 는 Halidan 2014 를 **ribbon blender** 의 PSMI 사용례로 적는데, Table 10 은 같은 논문을 **bladed mixer** 로 싣는다.  ⇒ **표의 귀속을 그대로 인용하지 말고 원저로 확인할 것.**
- ⚠ **[우리 분석]** 로 표시한 모든 문단(§4.4 끝, §4.5 끝, §4.7.5, §7, §8)은 **리뷰의 주장이 아니다**.  분리해서 인용할 것.

### 10.2 전이 한계 (우리 계로)
- **믹서 없음** ⇒ 운전 파라미터 결론(rpm·충진율·blade 각도·loading pattern) 전량 **비적용**.
- **mm ↔ µm 3 자릿수** ⇒ 경험칙·파라미터 값 **비전이**.
- **소재계 없음** (일반 분말) ⇒ 황화물·NMC 특이성(연성 SE, 표면 반응) **전무**.
- **2D/3D 문제 아님** (전부 3D) — 이 축은 무해.
- **강체 구 100 %** ⇒ Varkey/Bazzoun 과 **같은 frame [1]/[2] 결손**.  이 리뷰도 형상 소성을 모른다.

### 10.3 ★ 리뷰가 **스스로 미해결로 남긴 것** (§5 난점 + §6 권고 4개, 원문 요지)
1. **계산시간**: DEM 은 공정의 **수 분**밖에 못 돈다; 산업 규모(수억~수십억 입자)는 **현 하드웨어로 불가**; 미세 분말일수록 악화.
2. **보정**: 직접 측정이 거의 불가 → **시행착오**가 통상; 점착이면 입력이 더 많아 더 어렵다; *"어떤 경우엔 보정이 공정 시뮬 자체보다 더 오래 걸린다."*
3. **최적화 도구로서의 한계**: 설계·운전 조합이 많아 **완전한 최적화 도구로 쓰기 어렵다**.
4. **권고 (1) 비구형**: 정의된 형상(정제·캡슐·바늘)의 믹싱 시뮬이 **희소**; 접촉검출이 계산시간의 ~80 % ⇒ **효율적 접촉검출 알고리즘** 필요.
5. **권고 (2) 점착 미세분말**: 문헌에 **거의 없다**; particle scaling(Thakur 2016 / Pantaleev 2017) + 최적화 보정 + GPU 로 *"이제 가능해야 한다"*.
6. **권고 (3) 스케일업**: 실험실 ↔ 대형 믹서의 품질 동등성은 **오랜 미해결**; GPU·멀티GPU 로 여러 크기를 돌려 **스케일업 방법론을 수립**하라.
7. **권고 (4) 다성분/다분산**: *"대부분 **단·이분산, 같은 밀도·같은 형상**만 다뤘다 — 이것은 DEM 연구가 산업 수요와 **잘 정렬되어 있지 않음**을 보여준다.  **다분산이 혼합 품질에 미치는 영향**, 그리고 **밀도·형상이 다른 입자**의 혼합을 DEM 으로 분석하라."*
8. **ML 의 한계**: 훈련 설계공간 밖에서는 못 쓰고, 수 초의 DEM 이 훈련 데이터로 부족할 수 있다.

### 10.4 ★ **우리가 이 분야에서 빠뜨리고 있는 것** (우리 판단, 실행 가능 순)
| # | 빠진 것 | 크기 | 비고 |
|---|---|---|---|
| 1 | **혼합/분리 지수 자체** — 배위수는 재는데 지수로 변환하지 않는다 | 中 | `prereg_m7` 이 메우는 중 (`E_XY` + CLMI) |
| 2 | **`D_ij` · `Pe` · granular temperature** — 재배열의 직접 관측량 | 大 | 기존 덤프로 **후처리만** 하면 됨 (§8-④) |
| 3 | **점착 파라미터의 벌크 앵커(AOR/shear cell)** | 大 | 분야 표준 절차인데 우리는 **0** (§8-③) |
| 4 | **`k_c ↔ Γ` 환산** | 中 | 리뷰에 없음 ⇒ Luding 2008 · Pasha 2014 · Thakur 2014 로 내려가야 함 |
| 5 | **지수 비평 3편 미 digest** — Bhalode & Ierapetritou 2020 · Wen 2015 · Deen 2010 (+Fan 1970) | 大 | **지표 선택의 근거가 거기 있다**.  이 리뷰는 넘기기만 한다 |
| 6 | **원저 지수 논문 미 digest** — Stambaugh 2004 (SI, contact-based) · Cho 2017 (다성분·non-sampling) · Chandratilleke 2012 (PSMI, 입자 스케일) | 大 | ★ **Cho 2017 은 "multicomponent" 를 제목에 단 유일한 지수** = 우리 3종에 가장 가깝다 |
| 7 | **전단 공정 단계 부재** | 大 | 리뷰 기준 *"응집 파괴는 전단이 담당"* ⇒ 우리 계에는 응집을 **깰 기구가 없다** (구조적 사실, 결함 아님) |
| 8 | **rolling resistance / 비구형 대리** | 小 | Model C (Ai 2011) · Frankenberg `μ_r=0.2` 선례 |
| 9 | **최적화 기반 보정에 우리 ML 을 쓰지 않음** | 中 | 인프라는 있고 용도만 다름 (§4.6) |
| 10 | **coarse-graining** | 小 | 우리 RVE 규모에선 불필요 — **비활성**으로 기록해 두면 충분 |

---

## 11. 인용 가능 문장 (deck / paper 용)

- *"A 2023 comprehensive review of DEM in batch solid mixers (Jadidi et al., Rev. Chem. Eng. 39(5) 729–764) catalogues eight mixing/segregation indices — Lacey, intensity of segregation, RSD, particle-scale (PSMI), Siiriä, Stambaugh's segregation index, graphic (GPSI) and subdomain-based (SMI) — and reports that **RSD and the Lacey index are the two most commonly used**; the review does not itself rank them, deferring the critical assessment to Bhalode & Ierapetritou (2020), Wen et al. (2015) and Deen et al. (2010)."*
- *"Following the three-family classification the review cites (variance-based / distance-based / contact-based), our phase-pair contact enrichment is a **contact-based** metric of the same family as Stambaugh et al.'s segregation index, normalised here to the random-mixing expectation — chosen because it requires **no spatial binning**, and therefore carries no scale-of-scrutiny dependence."*
- *"Of the four size/density segregation mechanisms catalogued in the review (trajectory, elutriation, percolation/sifting, push-away), **only trajectory and elutriation require fluid–particle interaction**; percolation (size-driven) and push-away (density-driven) therefore remain active in a fluid-free settling-and-compaction process such as ours."*
- *"The review quantifies the gap between DEM mixing practice and industrial need: **80 % of the surveyed studies use spherical particles, 82 % non-cohesive powders and 46 % mono-disperse systems**, with only 16 % poly-disperse — and it explicitly recommends DEM studies of poly-dispersity and of particles differing in density and shape."*
- *"The review lists **surface energy, plasticity ratio and adhesion stiffness** side by side as DEM calibration parameters to be matched against bulk tests (angle of repose, shear cell), but provides **no conversion between them** — so a linear adhesion-stiffness parameterisation and a JKR surface-energy parameterisation cannot be compared quantitatively on the basis of this review."*
- ⛔ **쓰면 안 되는 문장**: *"리뷰가 Lacey 대신 접촉 기반 지수를 권고한다"* · *"리뷰가 coarse-graining 의 타당성 조건을 제시한다"* · *"리뷰가 분산 기반 지수의 격자 의존을 경고한다"* — **전부 이 리뷰에 없다.**

---

## 12. 용어 미니 글로서리 (이 카드를 읽는 데 필요한 것만)

| 용어 | 뜻 (이 리뷰의 용법) |
|---|---|
| **batch vs continuous mixer** | 배치 = 원료를 넣고 섞고 **한 배치씩 배출**.  연속 = 계속 투입·배출.  **이 리뷰는 배치만** |
| **tumbling / convective** | 용기가 도는 쪽 / 용기 고정 + 임펠러가 도는 쪽 |
| **convective · diffusive · shear mixing** | 덩어리 이동 / 개별 입자 무작위 이동 / 층간 운동량 교환.  **전단이 응집 파괴 담당** |
| **percolation (sifting)** | 큰 입자 사이 틈으로 **작은 입자가 내려가는** 크기 구동 분리 |
| **push-away** | **밀도 차이** 구동 분리 — 무거운 입자가 가벼운 둘을 밀어낸다 |
| **Lacey index** | 분산 기반 혼합지수.  `(σ₀²−σ²)/(σ₀²−σ_r²)`, 0(분리)→1(무작위) |
| **RSD** | 상대표준편차 `σ/C_avg`, 1(분리)→0(무작위).  **작을수록 잘 섞임** |
| **intensity of segregation** | Lacey 의 여집합 형태, 1→0 |
| **PSMI** | 입자 스케일 지수 — 셀이 아니라 **입자 주변**에서 조성을 재는 계열 (Chandratilleke 2012) |
| **SI (Stambaugh)** | **접촉 기반** 분리지수 — 동종/이종 접촉수의 비, 2(분리)→0(무작위) |
| **SMI (Cho)** | 다성분용 지수.  리뷰 라벨 "subdomain-based", 원제는 **"non-sampling"** |
| **scale of scrutiny** | 분산 기반 지수에서 **표본(셀) 크기** — ⚠ **이 리뷰에는 이 용어가 없다** |
| **granular temperature** | `T = (1/3)⟨u′u′⟩`, 속도 변동의 세기.  ↑ = 확산·전단 기전 활발 |
| **Peclet number** | `Pe = U L_c/D`.  `<1` 확산 지배 / `>1` 대류 지배 |
| **Rayleigh time** | 탄성 표면파가 입자를 가로지르는 시간.  DEM 시간스텝 = 그 **20–30 %** |
| **coarse-graining** | 입자를 `l` 배로 키워 `l³` 개를 하나로 대표.  접촉모델을 조정해 평균 거동을 맞춘다 |
| **force-scaling** | CG 입자의 접촉력을 `f²` 등으로 스케일해 원래 입자의 응력·에너지를 보존 (⚠ 이 리뷰가 아니라 `frankenberg2024_*` 의 용어) |
| **JKR / DMT / SJKR** | 점착 접촉이론.  JKR = 접촉면 내 점착(Γ, J m⁻²), DMT = 접촉면 밖 점착, SJKR = LIGGGHTS/EDEM 계열의 단순화판(CED, J m⁻³) |
| **CED** | cohesion energy density — SJKR 의 점착 세기 노브 |
| **AOR (DAOR/SAOR)** | 안식각 (동적/정적).  DEM 보정·검증의 표준 벌크 시험 |
| **PEPT / PIV / RPT** | 양전자 방출 입자 추적 / 입자영상 유속계 / 방사성 입자 추적 — 비침습 검증 수단 |
| **thief sampler** | 분체 속에 찔러 넣어 시료를 뽑는 침습 채취기 (side/end/core) |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
