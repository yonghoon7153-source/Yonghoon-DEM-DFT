# 복합 양극의 3D 미세구조 모델링 — percolation 이론으로 이온·전자 전도 클러스터 분석 — Bielefeld (J. Phys. Chem. C 2019)

> slug `bielefeld2019_microstructural_modeling_composite_cathode` · DOI `10.1021/acs.jpcc.8b11043` · type `continuum (geometric microstructure + percolation)` · PDF `Bielefeld_2019_JPCC_MicrostructuralModeling_CompositeCathode_Percolation.pdf` · digested `2026-06-26` · status ✅
>
> ★ **우리 backlog-B3 의 1차 출처** — 우리 percolation 지수(√(φ−φc)·CN²·f_p³)의 *universality-class* 문헌 앵커.
> 두 핵심값 **β=0.41**(Eq 1/Fig 4)·**p_c=[7.83·ln(d/µm)+36.67] vol%**(Eq 8/Fig 6) 둘 다 **본문 verbatim 확인**.
>
> 데이터 CSV: `docs/data/bielefeld2019_percolation.csv` (이 digest 전용, 정밀 수치). 기존 `bielefeld2019_percolation.csv`도 같은 내용(병존).

---

## 1. 한 줄 요약 (bilingual)

**KO** — Janek 그룹(+Volkswagen)이 GeoDict 안에 **구형 AM(겹침 없음) + 볼록 다면체 SE(겹침 있음)** 로 복합 양극 3D 미세구조를 *랜덤 배치*로 만들고, **percolation 이론**(Hoshen–Kopelman 클러스터 라벨링)으로 이온·전자 전도 클러스터의 *존재·이용률(utilization)·active interface 면적*을 조성/porosity/입경/두께 함수로 분석. 핵심 결론: **작은 AM 입자 → 전자전도 향상**(접촉↑·표면적↑), **porosity 가 이온·전자 둘 다 결정적**, **두께 효과는 얇은 전극에서만**(percolation 억제). 거기서 *이상 조성*과 설계 지침을 도출. ⚠ **유효 전도도 σ 자체는 안 푼다**(constriction 저항은 명시적 "향후 과제", Greenwood 1966 인용) — percolation 존재·클러스터 부피·기하 active interface 까지만.

**EN** — The Janek group (+ Volkswagen) builds 3D composite-cathode microstructures in GeoDict by *stochastic placement* of **spherical AM (no overlap) + convex-polyhedral SE (with overlap)**, then uses **percolation theory** (Hoshen–Kopelman cluster labelling) to analyze the *existence / utilization level / active-interface area* of the ionic and electronic conduction clusters vs composition, porosity, AM particle size, and electrode thickness. Headline results: **small AM particles enhance effective electronic conduction** (more contacts, higher surface area), **porosity crucially affects both** ionic and electronic conduction, **thickness affects electronic conduction only in thin electrodes** (percolation suppressed → falsely-favorable appearance). From this they derive *ideal compositions* and electrode-design guidelines. ⚠ The paper does **NOT** compute an effective conductivity σ — point-contact constriction resistance is explicitly deferred to future work (cites Greenwood 1966). It is a **percolation/geometry** study.

**이 논문의 위치 (우리 기준):** 우리와 *가장 가까운 구조-모델링 peer*. 같은 Janek 그룹이 (2019 σ 없음) → **Bielefeld 2020**(연속체 flux-PDE σ_eff+바인더, 같은 1저자) → **Bazzoun 2026**(RNM/Holm constriction σ + 실험 EIS) 으로 *스스로* σ-솔버를 정교화해 왔고, 우리(Kirchhoff/Holm 삼중항 + MPM)는 그 궤적의 자연스러운 끝. ⇒ **이 논문이 *비운 칸*(σ 솔브·소성 SHAPE·dip·공정-예측)이 정확히 우리 novelty 의 위치.**

---

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Anja Bielefeld**, Dominik A. Weber, **Jürgen Janek** (Physikalisch-Chemisches Institut + Center for Materials Research LaMa, Justus-Liebig-Universität Giessen; + **Volkswagen AG Group Research, Wolfsburg**) | J. Phys. Chem. C **2019**, 123, 1626–1634 | 10.1021/acs.jpcc.8b11043 | **LPS (Li₃PS₄/Li₁₀GeP₂S₁₂ 계열, 일반 thiophosphate) + NCM-622** (예시; 모델은 사실상 *재료-무관*, 기하만) | 3D 미세구조 모델링 (GeoDict) + percolation 이론. **순수 모델링**(실험 없음; Strauss et al. ref 13 실험을 정성 비교만) |

- 수신/수정/게재: 2018-11-14 / 2018-12-25 / 2018-12-31. FELIZIA 프로젝트(03XO0026G, BMBF) 감사.
- **carbon-free** 복합 양극 가정(도전제·바인더 *의도적 배제* — "future addable"). 5성분(AM·SE·도전제·바인더·기공) 중 **AM+SE 2성분**만 모델링.

---

## 3. 핵심 수치 (numbers)

> ★ = digitized 아님, **본문/식 stated**. 이 논문은 σ 절대값이 없으므로 "물성"은 percolation 임계·이용률·면적·기하.

| 양 | 값 | 조건 | stated/digitized | 식·그림 |
|---|---|---|---|---|
| **β (임계지수)** ★ | **0.41** | d=10µm, 8 packings | stated (Fig 4 본문) | Eq 1, Fig 4 |
| A_spec power-law 계수 ★ | **1.73×10⁵ m²/m³** | p−p_c 위 | stated (Fig 4) | A_spec=1.73e5·((p−p_c)/vol%)^0.41 |
| **p_c(d) 식** ★ | **p_c = [7.83·ln(d/µm) + 36.67] vol%** | 전자 클러스터 | stated | Eq 8, Fig 6 |
| p_c @ d=3 / 5 / 10 / 15 µm | 45.3 / 49.3 / 54.7 / 57.9 vol% AM | Eq 8 계산 | stated_eq8 | Fig 6 |
| 전이영역(transition) @3µm / @15µm | 41–46 / 52–57 vol% AM | Fig 5 | stated 본문 | Fig 5 |
| **이상 조성** @porosity 5/10/20 % | **62/38 · 66/34 · 72/28 vol% AM/SE** | A_spec 최대 + 양 클러스터 percolate | stated 본문 | Fig 7, 8 |
| (위를 wt%로, NCM-622+LPS) | 80/20 · 82/18 · **86/14 wt%** | 〃 | stated 본문 | Fig 8 |
| **well-performing 창** | **AM 69–79 vol%** (69/31 ~ 79/21) | porosity 20 %, d=5µm | stated 본문 | Fig 7 |
| ─ 전자 한계(아래) | AM < 69 vol% → 전자 클러스터 부실 | 〃 | stated | Fig 7 |
| ─ 이온 한계(위) | AM > 79 vol% → 이온 클러스터 부실 | 〃 | stated | Fig 7 |
| porosity 기준(70/30 고정) | >34 % 둘 다 고립 / 전자한계 ~21 %까지 / <21 % 양호 | d=5µm | stated 본문 | Fig 9 |
| utilization 정의 | θ_ν = V_cluster/V_phase | (정규화) | stated | Eq 6 |
| A_spec 기하한계 | A_spec,geo = g_AM^V·6/d | 포화값 | stated | Eq 7 |
| 전이밴드 이용률 산포 | 같은 분율서 ~30 % vs ~70 % | 48–52 vol% AM | stated 본문 | Fig 3 |
| 최대 AM 겹침 | ~1 vol% @ ~65 vol% AM | 제거 후 잔존 | stated 본문 | p.1628 |
| 기하 dense-pack 한계 | ~74 vol% (등구) | — | stated | p.1628 (ref 31 Tóth) |
| E_SE (가정) | ~25 GPa | LPS, refs 32–34 | stated (겹침 허용 근거; 수치 안 씀) | p.1628 |
| 미세구조 dims / 해상도 | 80×80×140 µm³ / **0.2 µm/voxel (200 nm)** | — | stated | Table 1 |
| 두께 스윕 | 20–140 µm | 20% porosity, 70/30 | stated | Fig 10 |

**소재 주의:** wt% 환산은 **NCM-622+LPS** 밀도 기준 — 우리 NMC811+LPSCl 가 *아님*. percolation 임계·이용률·면적은 **기하**(입자 모양·크기·겹침)에서 나오므로 *재료-무관 추세*로만 사용. σ 절대 비교 불가(애초에 σ가 없음).

---

## 4. 시뮬레이션 방법 ★

- **code / version**: **GeoDict** (Math2Market, Version 2018 SP 5, ref 30). GeoDict 의 GAD/ProcessGeo 계열 stochastic-placement + Hoshen–Kopelman cluster 분석. (σ-PDE 솔버 ConductoDict/DiffuDict 는 *이 논문에선 안 씀* — percolation cluster 까지만.)
- **DEM 접촉법칙**: **없음.** 이건 DEM 이 아니라 *기하 stochastic-placement* 모델. 입자 간 힘·압밀 역학 *전혀 없음* — porosity·조성은 **입력**(랜덤 배치 후 사후 겹침조정).
- **재료 파라미터**: percolation 분석에 *재료 물성 안 씀*. 단 SE 다면체 겹침 허용의 *근거*로만 E_SE ~25 GPa(refs 32–34, 낮은 영률+연성) 인용. SE 전자전도 무시(이온 대비 5–6 자리수 낮음, ref 35) → SE=이온 클러스터, AM=전자 클러스터로 *완전 분리 배정*.
- **bond/binder 모델**: **carbon-free 가정 — 도전제·바인더 의도적 배제.** "원리상 추가 가능"(Strauss et al. 방식). carbon 은 thiophosphate 와 산화분해(ref 7,23,24) + AM 코팅이 계면 보호 → 코팅은 percolation 에 무시할 영향(나노 두께, 충분한 전하전달, ref 26).
- **MPM/continuum**: **소성·형상변화 없음.** 입자는 *영원한 강체 구/다면체*. 압밀 거동(압력→porosity) 자체가 없음 — porosity 는 *지정 입력*.
- **전달 솔버 (σ)** ★: **없음 (핵심 한계).** 유효 σ 를 *안 푼다.* percolation 존재 + cluster 부피(utilization) + 기하 active interface 까지만. **점접촉 constriction/contact 저항은 명시적으로 "향후 과제"** (본문 p.1629: "do not take into account possible resistances occurring at particle–particle interfaces and constriction resistances ... regarded as a large number of interacting microcontacts" — ref 36 = **Greenwood 1966**, 우리 Holm 1967 과 같은 계보). ⇒ 우리·Bazzoun 이 *바로 이 칸*(constriction σ + Kirchhoff)을 채운다.
- **입자 처리** ★ (DEM판 "무질서 처리" 대응):
  - **AM = 구 (겹침 없음), uniform 단봉 PSD 만.** 분포(Gaussian width, bi/tri-modal)는 *향후 과제*로 명시 보류 — "입자 *크기 자체*의 영향을 분포 설정 편향에서 분리하기 위해" 단일 크기 채택. ⇒ **Furnas dip(분포 효과)은 이 논문 범위 밖.**
  - **SE = 볼록 다면체 (겹침 있음).** SE 입경 = enclosing-sphere 지름. *겹침을 AM 에 배정*해 AM 을 구로 유지(→ 미리 SE 를 더 조밀하게 생성해 보정, Eq 5).
  - **rigid 입자만 — CONTACT 소성도, SHAPE 소성도 없음.** AM 겹침은 반복적으로 제거(~10⁻⁵ vol% 잔존; 고밀도서 어려움, 최고 ~65 vol% AM 서 ~1 vol% 잔존, 등구 74% 한계 근접). 겹침은 *기하 침투*지 *변형 흐름* 아님.
  - **클러스터 식별**: 한 경계면(현재 집전체 or SE separator)에서 시작 → 이웃 점유 site 연결 검사(Hoshen–Kopelman) → 구조 전체를 가로질러 양 경계를 잇는 클러스터 = **percolating cluster**. 이온 클러스터(SE, light blue) / 전자 클러스터(AM, yellow) 따로.
- **도메인/RVE / seeds / 두께**: 80×80×140 µm³, 200 nm voxel. 전이영역(48–52 vol% AM 부근)은 통계 위해 **AM 분율당 10개 랜덤 실현** 평균; Fig 4 power-law 는 **8 packings/밀도**. 두께 효과는 140µm 기본 구조를 20–120µm 로 *잘라서* 분석(reduced-model-size 효과).
- **특이사항**: percolation "order parameter" Θ ∝ (p−p_c)^β (Eq 1, Grimmett ref 21). 유한계는 전이가 통계요동으로 *번짐* → 무한계만 날카로운 임계 — 그래서 전이영역서 다중 실현 평균. p_c 정의 = **10개 중 *과반*이 percolate 하는 AM vol% = 평균 utilization 40%** (Fig 6).

---

## 5. 섹션별 결과 — ALL numbers

### 5.0 Introduction / 동기 (p.1626–1627)
- ASSB 의 한계 = 복합 양극 내 **불충분한 이온·전자 percolation**(crucial). 성능은 재료물성(탄성·전기화학·morphology)·셀설계에 민감.
- 선행 실험 인용(이 논문의 *비교 기준*): **Strauss et al. (ref 13)** = carbon-free NCM-622 + LPS 에서 **AM 입경↑(최대 20µm) → 전자전도 급락** → "작은 AM 이 성능↑". **Siroma (ref 14)** NCM-523+Li₂S–P₂S₅ = "고 AM/SE 부피비 → 전자 σ_eff↑, 단 이온 σ_eff↓"(우리 trade-off). **Hlushkou (ref 16)** = porosity 가 σ_eff,ion·tortuosity 에 큰 영향(LCO·Li₂S–P₂S₅–LiI). **Nam (ref 11)** 85 wt% AM 고로딩 → 용량·rate 저하(바인더+소량 SE 가 이온전도 부실 주범).
- **목표**: 압밀역학·실험 없이, *최대한 대표성 있는* 미세구조를 *편의적으로 많이* 생성해 porosity·AM 입경·분포·조성·두께를 *설계 변수*로 동시 분석 → 고성능 복합양극의 *boundary condition* 정의·지침.

### 5.1 Percolation 이론 (Methods, p.1627)
- 임계확률 p_c = percolation 이 처음 관측되는 occupation 확률. p<p_c subcritical, p>p_c supercritical.
- **Eq 1: Θ ∝ (p − p_c)^β** — order parameter 의 power law, β = 임계지수(Grimmett ref 21). 유한계는 전이 번짐, 무한계만 날카로운 p_c.
- ASSB 적용: 비슷한 미세구조의 *유효 이온·전자 σ 를 percolation 문턱 근방에서 추정 가능* — 단 *이 논문은 그 σ 추정을 실행하지 않고* threshold·cluster 식별까지만.

### 5.2 미세구조 생성 (Microstructural Modeling, p.1628)
- **2-submodel**: SE submodel + AM submodel 따로 생성 후 *결혼(marriage)*. AM = 구·uniform·겹침 없음. SE = 볼록 다면체·겹침 있음.
- 겹침 제거: 입자별 겹침을 허용범위 내로 이동, 10회 반복 → ~10⁻⁵ vol% 까지(대개). 조밀할수록 어려움. **최고 ~65 vol% AM 서 겹침 ~1 vol%** (등구 dense-pack 74% 근접, ref 31). 비균일 PSD 면 더 높은 packing 가능(보류).
- **porosity 정의**: φ = V_pore/V_total (Eq 2) = 1 − (V_AM+V_SE)/V_total (Eq 3). 부피분율 2종 구분: 위첨자 V(=총부피, 기공 포함) vs S(=고상만). g_AM^V = (1−g_SE^S)(1−φ) (Eq 4); g_SE^V 는 Eq 5 로 조정(SE 생성 시 AM 미존재 → 나중에 marriage 로 SE 일부를 AM 이 차지).
- **클러스터**: SE=순수 이온전도(전자 무시) → 이온 클러스터; AM=유일 전자전도 → 전자 클러스터. 각 경계(집전체/separator)에서 연결검사. Fig 1 에 yellow(전자)·light-blue(이온).
- 두께: future tech 위해 **140 µm** 상대적 대형 전극, 200 nm 해상도(3µm 입자까지 합리적).

### 5.3 전자전도 (Electronic Conduction, p.1629–1631)
- **입경 효과 (Fig 2, 5):** 55 vol% AM 고정, d=5/10/15µm 예시(Fig 2). 작은 입자=전자 클러스터 잘 percolate, 중간크기=이용률↓, 큰 입자=아예 percolate 안 함.
- **Fig 3 (d=5µm):** AM 분율↑ → 이용률·표면적 둘 다 ↑(같은 곡선 진행). 48 vol% 아래=둘 다 매우 낮음(부실 연결). 45 vol% 의 작은 동요 = 분율당 1 packing 이라(통계). **전이영역 48–52 vol% 는 10개 평균**(요동 회피). 같은 분율서 *random packing 에 따라 ~70 % vs ~30 % 이용률 산포*. 52 vol% 위=포화(geometric max 근접, Eq 7 A_spec,geo=g_AM^V·6/d).
- **Fig 4 — β=0.41 (핵심):** d=10µm, p_c 바로 위에서 전자 클러스터 표면적을 8 packings/밀도로 계산. **log–log 가 power law 로 잘 맞음, 임계지수 β=0.41** (전이 부근 오차막대 큼). 입경은 임의 선택, 모든 입경에 적용 기대. **β=0.41 = Sur et al. (ref 37) 의 simple-cubic 격자 3D site-percolation 연구와 good agreement** → percolation law 적용 가능 확인.
- **Fig 5 (d=3–15µm):** 작은 입자=저 AM 분율서 percolation. p_c 정의 = *과반이 percolate = 평균 이용률 40%*. 전이영역: **3µm = 41–46 vol%**, **15µm = 52–57 vol%**. steepness 는 입경 무관 유사. 이용률 vs 표면적 차이: 작은 입자일수록 비표면적↑.
- **Fig 6 — p_c=7.83·ln(d/µm)+36.67 (핵심 Eq 8):** 입경 vs p_c 를 로그식으로 fit(데이터 충분 정확). 입경↑ → p_c↑(로그). 데이터 ±1–2 vol% 산포.
- **Strauss 비교:** 큰 AM=작은 표면적=percolation 기회↓=낮은 전자 σ_eff (ref 13 ex situ XRD 의 inactive NCM-622 고분율 관측과 정합). 단 Strauss packing 밀도·porosity 미지.
- **종합:** carbon-free 전자전도는 **AM packing 밀도 + 입경**에 강의존. 조밀=친밀접촉·연결성↑·활성분율↑. 작은 입자=저 packing 서도 고 이용률(고 porosity 보상 가능) — 단 고표면적은 화학분해·계면층(ref 7) 취약.

### 5.4 이온전도 (Ionic Conduction, p.1631–1632)
- AM=5µm 채택(전자서 작은 입자 유리 + Strauss 현실값). **2 경우**: 일정 porosity·조성변화 / 일정 조성·porosity 변화.
- **일정 porosity (Eq 9):** g_AM^S = g_AM^V/(1−φ). 두 submodel 병합 후 양 클러스터 계산.
- **Fig 7 (porosity 20%, d=5µm) — well-performing 창:**
  - **전자 한계 = AM < 69 vol% (69/31)**; **이온 한계 = AM > 79 vol% (79/21)**. ⇒ **양호 창 = AM 69–79 vol% (fairly small)**.
  - SE 는 모델서 겹치게 설계해도 *고-AM 미세구조서 잘 연결된 이온 클러스터 못 만듦.* active interface 는 고-AM 서 줄어듦 → **최적 = 72/28 vol% = 86/14 wt%(NCM-622+LPS).**
- **Fig 8 (porosity 5/10/20 %) — 이상 조성 vs porosity:** 작은 porosity = 고 packing·고 mass loading → A_spec 유의 ↑(5% ≫ 10/20%). 전자 percolation 전이가 *작은 AM 분율*서 일어남(저 porosity). **이상 조성: 5% → 62/38 (80/20 wt%), 10% → 66/34 (82/18 wt%), 20% → 72/28 (86/14 wt%).** porosity↑ → 최적이 *고 AM* 쪽 이동 + 이온한계 중요도↑(최적 위 drop 이 20%서 더 가파름).
- **일정 조성 70/30, porosity 변화 (Fig 9):** porosity 43%→3% 스윕. **>34 % = 이온·전자 둘 다 고립영역**; **21 %까지 전자한계 잔존, <21 % 양호.** active interface 는 porosity↓ 면 증가(단 porosity 아닌 전극부피 기준 정규화 주의).

### 5.5 전극 두께 (Electrode Thickness, p.1632)
- 고에너지 위해 두꺼운 전극 필요 — 얼마나 두꺼워도 (고 rate) 성능 유지? percolation = 충분 전도망·확산거리·tortuosity 가 두꺼운 전극서 추가역할.
- **Fig 10 (porosity 20%, 70/30, d=5µm, 두께 20–140µm):** 대부분 두께서 active interface 곡선 유사. 최적 조성 위치는 두께 무관 동일, 단 *최적 아래 곡선 모양*이 다름(전자 클러스터 때문, 집전체 측 시작점). **얇은 전극 = 초기 연결입자가 전체의 큰 분율 → A_spec↑(저 AM 서도) + percolation 문턱이 작은 AM 분율로 약간 이동 → percolation 억제 = *겉보기 favorable*** (= reduced model size = finite size effect). **이온전도는 두께 무관**(A_spec drop Fig7 과 두께별 구분불가). ⇒ 얇은 전극의 좋아보임은 *유한크기 인공물*; 두꺼운 전극도 미세구조상 비슷한 클러스터링 제공 가능(단 긴 확산경로·charge/discharge 성능은 *이 모델이 못 반영*).

### 5.6 Conclusions / 설계지침 (p.1633)
- carbon-free 복합양극 미세구조 모델 확립(AM+SE), Strauss 실험과 정합. percolation 으로 이용률·active interface 평가. **porosity·조성·두께·AM 입경**을 *설계 변수*로 — well-connected boundary condition 정의.
- **작은 AM = 전자전도에 유리**(고표면적·percolation 기회↑) ↔ 단 고표면적=화학분해 위험(ref 7).
- **porosity 가 결정적** → *실험연구도 porosity 측정·보고 필수* 강력 권고(비교성). 작은 porosity 유리(저공극 제조 필요성 ↔ ref 42 Kim 이 LCO 에 SE 침투, porosity ~6–8% 달성·친밀 이온접촉).
- **실셀은 time-variant**: 사이클 중 조성변화·입자균열·부피변화·역학/전기화학 이슈(ref 43). AM 코팅·바인더·도전제·불균일성(공정조건)이 추가 난이. 이건 본 연구 범위 밖 — 지침·성능추정·*수학모델 확장의 토대* 제공이 목적(전기화학반응·입자→저항망 변환 = Sunde ref 40, Ott ref 41 fuel cell).

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **TOC** | 미세구조(AM red / SE) + 이온(blue)·전자(yellow) 클러스터; "ASSB 설계: porosity·조성·AM 입경·두께" | 그들 4 설계축 = 우리 입력 설계축과 동일 매핑 |
| **1** | GeoDict 워크플로: 다면체 SE(겹침) + 구 AM(겹침 없음) → 복합(겹침 AM 배정) → percolation 이온/전자 클러스터 | 우리 *압밀→네트워크* 와 대비: 그들은 *배치→cluster*(압밀·σ 없음) |
| **2** | 55 vol% AM, d=5/10/15µm 전자 클러스터(yellow=연결, red=고립) | 입경 시각화 — 큰 입자 percolate 실패 |
| **3** | d=5µm 이용률(좌)·전자 클러스터 비표면적(우) vs AM vol%; 기하한계 점선(Eq 7) | utilization θ_ν = 우리 f_AM^cc/dead-AM; 전이밴드 산포(70 vs 30%) = 우리 SE-poor 코너 산포 |
| **4** ★ | **β=0.41 power-law** (A_spec vs p−p_c, d=10µm, log–log) | ★ **우리 √(φ−φc) percolation-backbone 지수의 universality-class 앵커** (Sur 3D site-perc) |
| **5** | 이용률·비표면적 vs AM vol%, d=3–15µm 전체 | 작은 입자 = 저분율 percolation (우리 size=packing) |
| **6** ★ | **p_c=7.83·ln(d)+36.67** (전자 p_c vs 입경, 로그fit) | ★ **우리 σ_e 입경의존·dead-AM 임계와 대조**; 입경↑→p_c↑ |
| **7** | porosity 20%, d=5µm: 이용률(좌, 전자한계<69·이온한계>79)·A_spec(우, 72/28 최적) | ★ **well-performing 창 69–79 vol% = 우리 dead-SE/dead-AM 양끝 + Minnmann 42 vol% 교차** |
| **8** | porosity 5/10/20% 별 A_spec vs 조성; 이상 조성 62/38·66/34·72/28 | ★ **porosity↑→이상 AM↑ 이동** = 우리 porosity-조성 결합; A_spec(5%)≫(20%) |
| **9** | 70/30 고정, porosity 43→3% 스윕: 이용률·A_spec | porosity 기준(>34 고립, <21 양호) — 우리 ~20% floor 와 *의미 다름*(percolation vs 기하) |
| **10** | 20% porosity, 70/30, 두께 20–140µm A_spec | 얇은 전극 percolation 억제(유한크기) = 우리 g_thin gate 와 정성 일치 |

> 모든 그림이 *기하/percolation* — **σ 곡선 없음**. Fig 3·4·5·7·8·9·10 의 세로축은 *utilization(%)* 또는 *A_spec(m²/m³)* 이지 σ(mS/cm) 가 아님. ⇒ 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 **직접 수치 비교 불가**.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

| 항목 | 이 논문 (Bielefeld 2019) | 우리 | 차이 / 이유 |
|---|---|---|---|
| 구조 생성 | **stochastic placement** (porosity·조성=입력, 랜덤배치+사후 겹침조정) | **process-physics** (DEM 압밀로 porosity 를 *예측*; MPM 소성흐름) | top-down/placement vs bottom-up/formation — 우리 NOVELTY |
| 압밀 역학 | **없음** (porosity 지정) | DEM 접촉력·Heckel(P_y 138)·MPM J2 | 그들 porosity 는 *측정/예측* 아닌 *입력* → 우리 15.6% 와 절대비교 금지 |
| σ 산출 | **안 함** (percolation 존재·cluster부피·기하 A_spec 까지; constriction=future, Greenwood) | **Kirchhoff + Holm constriction R=1/(2σr_c) 삼중항** | ★ 우리 transport novelty 의 *정확한 위치* — 그들 빈 칸 |
| 전달 채널 | 이온+전자 (클러스터 존재만) | σ_ionic + σ_e + **σ_thermal** (실값) | 우리 삼중항 + 열 우위 |
| 접촉면적 | **기하** active interface (A_spec=g_AM·6/d, 변형 없음) | **Stage-E 소성 접촉면적**(Tabor+volume) | 그들 면적은 기하상한; 우리는 소성변형 면적 |
| 입자 형상 | rigid 구(AM)+다면체(SE), **소성 없음** | DEM rigid + **MPM 진짜 SHAPE 소성** | morphology = 우리 MPM 고유 |
| PSD | **uniform 단봉만** (분포=future) | **bimodal 12:4:1** + 정량 Furnas dip | dip = 그들 빈 칸 → 우리(또는 de Larrard) 소유 |
| 작은 AM 효과 | "작은 AM→전자↑"(접촉·표면적, *percolation 존재* 근거) | σ_e: φ_AM⁴·NCM(r)·√A_AM-AM·AM-AM backbone (*σ 실값* 근거) | 같은 *방향*, 우리는 σ 로 정량(그들은 cluster 존재로) |
| 두께 효과 | 전자만, *얇을 때만*(유한크기 억제) | σ_e g_thin gate σ(−5·(T/d−8)) (thin 3D→2D) | ★ 같은 물리(얇은 전극서만 두께 중요) — 우리는 σ_e 폼에 *수식 gate* |
| 검증 | Strauss 실험 *정성* 비교만(실험 없음) | solver=ground truth + Bazzoun/Minnmann 실험 앵커 | 둘 다 직접 실험 부족(우리는 외부 앵커 확보) |
| 소재 | NCM-622+LPS = **wt% 환산용 예시**(사실상 재료-무관) | NMC811+LPSCl 특이 | 재료-특이 절대값 끌어오기 금지 |

**핵심 차이 3줄:** (1) 그들은 percolation 클러스터를 *센다(count)*, 우리는 그 위에 transport 를 *푼다(solve)* — constriction(Holm) 포함; (2) 그들은 σ 가 아예 없고 이온+전자 *존재*만, 우리는 σ_i/σ_e/σ_thermal *실값* 삼중항; (3) 그들 입자는 기하(소성 없음·단봉), 우리는 MPM SHAPE 소성 + bimodal dip. **단 percolation *추세*(작은 입자→percolation↑, 고-AM 이온한계/저-AM 전자한계, β=0.41)는 frame[4] 구조-descriptor 교차검증** — 같은 universality class.

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) — 심층

### A.1 그들의 *기하 percolation-cluster* 모델 vs 우리 *접촉망 + Kirchhoff/Holm transport SOLVE*
Bielefeld 의 분석은 **연결성(connectivity)** 에서 멈춘다: Hoshen–Kopelman 으로 "이 점유 site 들이 양 경계를 잇는 spanning cluster 를 이루는가?"를 판정하고, 그 클러스터의 *부피*(utilization θ_ν)와 *표면적*(A_spec)을 잰다. **저항·전류·전위는 등장하지 않는다.** 본문이 직접 인정: "이 연구는 입자–입자 계면 저항과 constriction 저항(다수 microcontact 의 상호작용, Greenwood ref 36)을 *고려하지 않는다*."

우리 파이프라인은 *그 위 한 층*을 더 간다:
- DEM 접촉망의 **각 SE–SE 접촉을 저항 R=1/(2σ·r_c) (Holm 1967) 로** 환산(접촉반경 r_c = 소성변형 깊이 기반),
- **Kirchhoff Σ(φ_i−φ_j)/R=0** 를 풀어 *유효 σ_eff,ion/e/thermal* 의 **실값**을 얻는다.
- ⇒ Bielefeld 가 "percolate 한다/안 한다 + 얼마나 연결됐나"까지면, 우리는 "그래서 σ 가 얼마인가 + constriction 으로 얼마나 깎이나"까지. **이게 우리 transport novelty 의 정확한 위치이고, 같은 Janek 그룹이 후속(2020 연속체 σ → Bazzoun 2026 RNM/Holm)에서 *스스로 채워온* 칸이다.**

> 대응 매핑: 그들 **utilization θ_ν = V_c/V_ν** ↔ 우리 **f_AM^cc / dead-AM**(연결 분율); 그들 **active interface A_spec** ↔ 우리 **coverage / A_AM-SE**(단 그들=기하, 우리=Stage-E 소성); 그들 **percolation 존재** ↔ 우리 **f_perc_x/y/z + f_p³ isotropy**.

### A.2 "작은 AM → 전자 σ↑" — 그들 vs 우리 σ_e 폼
- **그들 (Fig 5, 6):** 작은 AM = 비표면적↑·접촉 기회↑ → *저 AM 분율서도 전자 클러스터 percolate*(p_c 가 작은 AM 서 낮음, Eq 8). 근거 = **percolation 존재 + A_spec**(σ 아님).
- **우리 σ_e (Stage 22.5, LOOCV 0.953):** σ_e ∝ (σ_S·NCM_S)^(1−p)·(σ_P·NCM_P)^p · **φ_AM⁴** · **√A_AM-AM** · … 여기서 **NCM(r)=1/(1+(r_AM/2)^1.5)** (Trevisanello GB 인자, 작은 입자=GB↑이지만 접촉수↑가 우세) + **√A_AM-AM**(Holm 접촉면적) → 작은 AM = AM-AM 접촉수·면적↑ → σ_e↑. 근거 = **σ 실값 + 명시 접촉저항.**
- ⇒ **같은 *방향*, 다른 *깊이*.** 그들은 "작은 AM 이면 percolate 한다"(존재), 우리는 "작은 AM 이면 σ_e 가 얼마만큼 올라간다"(정량, φ_AM⁴·√A·NCM(r) 분해). 우리 σ_e 의 *입경 의존*이 그들 p_c(d) 로그식과 *같은 부호*임을 frame[4] 교차검증으로 인용 가능.

### A.3 "두께는 얇을 때만 중요" — 그들 Fig 10 vs 우리 g_thin gate
- **그들 (Fig 10):** 전자전도는 **얇은 전극서만** 두께 영향(초기 연결입자가 전체의 큰 분율 → 유한크기로 percolation *억제* → A_spec 겉보기↑). **이온전도는 두께 무관.** = *reduced model size / finite-size effect*.
- **우리 σ_e:** **g_thin = σ(−5·(T/d_AM − 8))** gate 가 *얇은 영역(T/d→0)서 1, 두꺼운 영역서 0* → thin-film 항(β_φth·logφ + β_covth·logcov_AM,P)을 *얇을 때만* 켠다. 물리 동일: **얇은 전극서 3D→2D crossover 로 percolation 거동이 달라진다.** 우리는 그걸 *σ_e 폼의 수식 gate* 로 박았고, 그들은 *그림으로 관측*. ⇒ **frame[4] 정성 교차검증** — 우리 g_thin 의 물리적 정당화로 Bielefeld Fig 10 인용 가능. (단 그들은 "겉보기 favorable=인공물"이라 *경고*; 우리 gate 는 *실제 thin-film 효과*를 반영 — 둘 다 "thin 은 다르다"는 같은 메시지.)

### A.4 porosity 의 의미 차이 (절대 동일시 금지)
- 그들 porosity 는 **입력 placement porosity** + percolation *recovery* 기준("70/30 서 porosity<21%면 전자 percolate, >34%면 둘 다 고립", Fig 9). = "얼마나 비어야 클러스터가 끊기나."
- 우리 ~20% 는 **강체 구 압밀 floor**(소성 흐름 없으면 못 넘는 *기하 잔류공극*). = "얼마나 압축해도 안 채워지나."
- ⇒ **두 ~20% 는 우연히 가깝지만 *물리적으로 다른 양*.** 그들 "21%=전자 percolation 회복 한계" ≠ 우리 "20%=rigid-sphere 압밀 floor". CSV Block 4 에 명시. 비교 시 *추세*(porosity 가 둘 다에 결정적)만.

---

## B. 적용가능성 (applicability to our LIGGGHTS DEM model)

### B.1 ★ backlog-B3 의 universality-class 앵커 — 정확한 인용법
우리 backlog-B3 는 "우리 √(φ−φc)·CN²·f_p³ percolation 지수를 *universality class* 문헌으로 정당화"를 요구한다. **이 논문이 바로 그 출처이고, 두 값 모두 verbatim 확인했다:**

1. **β = 0.41** — Eq 1 `Θ ∝ (p − p_c)^β`, Fig 4 에서 d=10µm 전자 클러스터 표면적을 8 packings 로 fit 해 얻은 임계지수. **본문: "good agreement with a study of 3D site-percolation in a simple cubic lattice performed by Sur et al. (ref 37)."** ⇒ **backlog 의 β=0.41 은 정확(CONFIRMED).** 인용 시:
   > "The 3D site-percolation universality class (critical exponent β ≈ 0.41, Bielefeld 2019 Fig 4 / Sur et al.) underpins our percolation-backbone exponents: the √(φ−φc) order-parameter scaling and the φ_AM⁴ Bruggeman backbone both derive from the same 3D-percolation class."
   - ⚠ 정밀 주의: β=0.41 은 *Bielefeld 가 자기 미세구조에 fit 한 값*이며 *Sur et al. 의 3D site-percolation* 과 일치한다고 *주장*. 표준 3D percolation 의 *교과서* β 는 문맥(order parameter 정의)에 따라 다르므로(예: 3D 무작위 percolation 의 강도 지수 β≈0.41 은 site-percolation 계열과 부합), **"Bielefeld 가 자기 데이터에서 0.41 을 얻고 Sur 3D site-perc 와 부합시켰다"**로 인용(이중인용: Bielefeld 2019 + Sur et al. ref 37). 우리 √(φ−φc) 의 *지수 0.5* 는 mean-field 근사이지 β=0.41 자체가 아님 — "같은 universality class 의 percolation backbone" 으로 정당화하되 *지수 0.5 = 0.41 등치 주장 금지*(우리 0.5 는 데이터-locked mean-field; 0.41 은 강도지수).

2. **p_c = [7.83·ln(d/µm) + 36.67] vol%** — Eq 8, Fig 6. 전자 percolation 임계가 AM 입경의 *로그함수*. **backlog 의 "p_c = 7.83·ln(d) + 36.67" 정확(CONFIRMED, 단위 vol% AM).** 인용 시:
   > "The electronic percolation threshold scales logarithmically with AM particle size, p_c = 7.83·ln(d/µm) + 36.67 vol% (Bielefeld 2019 Eq 8) — larger AM raises the threshold (fewer contacts), the geometric basis for our σ_e size dependence (NCM(r), √A_AM-AM) and the dead-AM cutoff."
   - p_c 정의 = "10 실현 중 *과반* percolate = 평균 이용률 40%" — 우리 dead-AM 임계(연결 분율 기준)와 *정의 유사*. d=3µm→45.3 / 5µm→49.3 / 10µm→54.7 vol% AM. 우리 production core AM 70–85 wt% 는 *이 임계 위*(전자 충분)이고, SE-rich 코너로 갈수록 그들 "전자 한계(<69 vol% AM)"에 접근.

### B.2 그들 다면체-SE packing vs 우리 구-SE — φc 가 바뀌나?
- Bielefeld 은 **SE 를 볼록 다면체(겹침 허용)** 로, 우리(+Bazzoun)는 **구**로 둔다. 다면체는 *면접촉 가능 + 더 조밀 packing* → *낮은 φc 에서 이온 percolation* 을 줄 수 있다(공간 채움 효율↑). 그들이 SE 겹침을 허용한 이유도 "낮은 영률(~25 GPa)+연성 → 다면체화 합리적".
- ⇒ **방향: 다면체 SE → φc(이온) 가 구-SE 보다 *낮게* 나올 수 있음**(같은 부피서 더 잘 연결). 우리 σ_ionic 의 **φc_S=0.195 / φc_P=0.200**(구-SE, mono) 은 *구 가정*의 임계. 그들과 *절대 동일시 금지*(그들은 σ 가 없고 다면체) 하되, **"SE 형상(구 vs 다면체)이 φc 를 ~수 vol% 움직일 수 있다"**는 *민감도 방향*으로 기록. 우리 MPM 은 SE 를 *소성으로 다면체화*(SHAPE 흐름)하므로 — **그들 다면체-SE 의 기하 효과를 우리는 MPM 소성으로 *동적으로* 얻는다**(그들은 정적 입력 형상). 이건 우리 강점.
- ⚠ 단 그들 다면체는 *placement 입력 형상*(변형 없음)이고 우리 MPM 다면체화는 *압력 하 소성 흐름* — *기하 결과*는 비슷할 수 있어도 *기원*이 다름(정적 vs 역학). φc 절대값 전이 불가, *방향*만.

### B.3 우리 percolation feature 로의 매핑 (요약)
| 우리 feature | Bielefeld 대응 | 인용 근거 |
|---|---|---|
| √(φ−φc) (order parameter) | Θ ∝ (p−p_c)^β, β=0.41 (Eq1, Fig4) | universality class (Sur 3D site-perc) |
| φ_AM⁴ Bruggeman backbone | 전자 클러스터 percolation·β | 같은 3D-percolation 계열 |
| f_p³ (3D isotropy) | spanning cluster x/y/z 연결 | percolation 존재 정의 |
| dead-AM 임계 | p_c=7.83·ln(d)+36.67 (Eq8, Fig6) | 전자 percolation 임계 입경의존 |
| dead-SE (고-AM 이온한계) | AM>79 vol% 이온한계 (Fig7) | well-performing 창 상한 |
| g_thin gate | 얇은 전극 percolation 억제 (Fig10) | thin-film finite-size 효과 |
| σ_e 입경의존(NCM(r),√A) | "작은 AM→전자↑" (Fig5,6) | 작은 입자 percolation 향상 |

---

## C. ★ 우리 novelty — 왜 우리가 state-of-the-art 인가 (our novelty vs this model)

> evidence-based, over-claim 금지. 각 항목 = 그들이 *명시적으로 안 한 것* + 우리가 *한 것*.

**우리가 *앞서는* 7개 (그들 빈 칸):**

1. ★ **우리는 transport 를 *푼다*, 그들은 percolation 클러스터를 *센다*.** Bielefeld 은 σ 를 *전혀 산출 안 함* — percolation 존재 + utilization + 기하 A_spec 까지만이고, **점접촉 constriction 저항을 명시적으로 "future work"(Greenwood 1966)로 미룬다**(본문 p.1629 직접 인용). 우리는 **Kirchhoff Σ(φ_i−φ_j)/R=0 + Holm constriction R=1/(2σ·r_c)** 를 풀어 σ_eff *실값*을 낸다. ⇒ Bielefeld 은 *connectivity*, 우리는 *conductivity with constriction physics*. **이게 우리 transport novelty 의 정확한 좌표.**

2. ★ **full 삼중항(열 포함).** 그들 = 이온+전자(존재만). 우리 = **σ_ionic(LOOCV 0.975) + σ_electronic(0.953) + σ_thermal(0.903, 14-feature Ridge)** *실값*. **열전도(σ_thermal)는 그들 전혀 없음** — 멀티패스(AM-AM/AM-SE/SE-SE 병렬) 저항망을 우리만 푼다.

3. ★ **Stage-E 소성 접촉 *면적*.** 그들 active interface = **기하**(A_spec=g_AM·6/d, *겹침=정적 침투*, 변형 없음). 우리는 **Tabor + volume 소성 접촉면적**(δ overlap → 소성변형 면적)으로 contact area 를 재유도 → σ 와 coverage 에 반영. 그들 면적은 *기하 상한*, 우리는 *소성변형* 면적.

4. ★ **DEM↔MPM 커플링 (소성 morphology).** 그들 입자는 *영원한 강체*(소성 없음). 우리 **MPM(J2, Taichi GPU)** 은 SE 의 *진짜 SHAPE 소성 흐름*(SEM 코어보존+경계평탄화 일치)·void-fill·누적소성변형장 Σdg 를 준다. scaffold 커플링(DEM AM 위치 고정 + SE MPM)으로 porosity/두께/coverage 가 *emerge*. **그들 다면체-SE 의 기하 효과를 우리는 압력 하 소성으로 *동적*으로 얻는다.**

5. ★ **fracture-aware (Auerbach/Lawn).** 그들 = 균열 *언급만*(실셀 time-variant, ref 43)·미모델. 우리 = **f_intact·frac_severe·Auerbach 임계** → 깨진 접촉의 부분전도(fracture-Holm)를 σ 폼에 반영(AM_P 92:8 8mAh 서 37–40% cracked).

6. ★ **문헌-grounded σ_grain.** 그들 = *재료-무관*(NCM-622+LPS = wt% 환산용 라벨, σ 안 씀). 우리 = **Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) sub-µm GB 인자 + Trevisanello NCM(r) + Wang** = 실제 LPSCl/NMC811 *재료 σ* 앵커. ⇒ 우리 σ 는 *재료-특이 실값*, 그들 percolation 은 *기하 추세*.

7. ★ **solver→scaling-law LOOCV 압축 → predictor.** 그들 = 그림·식(p_c, β)까지. 우리 = 네트워크 솔버 출력을 **5–14 param 스케일링 법칙으로 압축**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903 LOOCV) → ML predictor → 설계입력→전 metric 예측→2D 합성. 그들 "이상 조성(62/38~72/28)"은 *이산 스윕 결과*, 우리는 *연속 예측 함수*.

**그들이 *앞서는* 것 (정직):**

- **GeoDict 성숙도** — 상용 voxel 재료연구소(Math2Market). 우리 자체 파이프라인보다 *도구 성숙도*에서 앞섬. (단 우리도 Hoshen–Kopelman 류 cluster 분석·power-law fit 보유 → *흡수보다 정당화 근거*로 사용.)
- **깨끗한 percolation-theory 프레임 + 정량식** — β=0.41(Eq1/Fig4)·p_c=7.83·ln(d)+36.67(Eq8/Fig6) 의 *명료한 universality-class 정량화* + porosity 별 이상조성의 *체계적 스윕*(5/10/20%). **= 우리 backlog-B3 가 원하는 바로 그 앵커.**
- **볼록 다면체 SE 기하** — SE 를 다면체로 둔 *정적* 기하 처리(우리 DEM 은 구-SE). 우리는 MPM 소성으로 *동적* 다면체화하지만, *입력 형상*으로서 다면체 packing 의 φc 효과는 그들이 먼저 다룸.
- **2019 의 *선구적* 설계-지침 연구** — ASSB 복합양극 percolation 을 porosity·조성·입경·두께 4축으로 *최초로 체계화*한 foundational 논문. **인용 시 "Bielefeld 2019 = 이 분야 percolation 설계-지침의 토대"로 자리매김**(우리는 그 위에 σ-solve·소성·dip·공정예측을 *추가*).

> **포지셔닝 한 줄:** "Bielefeld 2019 establishes the percolation/geometry foundation (cluster existence, utilization, p_c(d), β=0.41); our work adds what it explicitly defers — a Kirchhoff/Holm constriction-resistance *conductivity* solve (full ionic/electronic/thermal triad), Stage-E plastic contact area, DEM↔MPM plastic morphology, fracture-awareness, material-grounded σ_grain, and a LOOCV-validated scaling-law/predictor — i.e. we *solve transport on the network the Janek group itself later filled* (2020 continuum σ → Bazzoun 2026 RNM/Holm)."

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① ★ **B3 앵커 확정·인용:** β=0.41(Eq1/Fig4)·p_c=7.83·ln(d/µm)+36.67(Eq8/Fig6) 를 우리 √(φ−φc)·CN²·f_p³·φ_AM⁴ 의 *universality-class 정당화*로 paper/deck 에 인용(이중인용 Bielefeld 2019 + Sur ref 37). ⚠ "우리 지수 0.5 = β 0.41" 등치 금지 — "같은 3D-percolation 계열" 까지만. `docs/data/bielefeld2019_percolation.csv`.
- ② **well-performing 창 69–79 vol% AM** 을 우리 dead-SE/dead-AM 양끝 + Minnmann 42 vol% NCM 교차 + 우리 production core(AM 70–85 wt%)와 대조 → *조성 최적 창*의 frame[4] 교차검증. porosity↑→이상 AM↑ 이동(62/38→72/28)은 우리 porosity-조성 결합 항의 정성 근거.
- ③ **Fig 10 thin-only 두께효과** = 우리 σ_e g_thin gate 의 물리 정당화로 인용(둘 다 "thin 은 다르다"). 단 그들 "얇으면 겉보기 favorable=유한크기 인공물" 경고도 함께 — 우리 thin 예측의 신뢰구간 논의에 사용.
- ④ **다면체-SE φc 민감도**: SE 형상(구 vs 다면체)이 φc 를 ~수 vol% 움직일 수 있음 → 우리 MPM 소성 다면체화가 *동적*으로 같은 효과 → "우리는 SE 형상효과를 역학으로 얻는다"는 차별점 문장화.
- ⑤ **포지셔닝 무기**: "Bielefeld(2019, percolation·σ없음) → Bielefeld(2020, 연속체 σ) → Bazzoun(2026, RNM/Holm σ+실험) → 우리(σ 삼중항+MPM)" 그룹-진화 서사 = 우리 방향이 *옳다*는 최강 positioning(같은 그룹이 σ-solve 로 *스스로* 진화).

---

## 9. 인용 가능 문장 (deck/paper용)

- "The closest microstructure-modeling peer to our pipeline, Bielefeld et al. (J. Phys. Chem. C 2019), analyzes ionic/electronic percolation in carbon-free ASSB composite cathodes via stochastic placement (spherical AM + convex-polyhedral SE) and Hoshen–Kopelman cluster labelling — but **explicitly does not compute effective conductivity, deferring point-contact constriction resistance to future work (Greenwood 1966).** Our Kirchhoff/Holm resistor-network solve fills precisely that gap."
- "Bielefeld 2019 quantifies the 3D site-percolation universality class (critical exponent β ≈ 0.41, Fig 4, in agreement with Sur et al.) and the size-dependent electronic percolation threshold p_c = 7.83·ln(d/µm) + 36.67 vol% (Eq 8) — the literature anchors for our percolation-backbone exponents (√(φ−φc), φ_AM⁴, f_p³)."
- "The Janek group's own trajectory — Bielefeld 2019 (percolation, no σ) → Bielefeld 2020 (continuum flux-PDE σ) → Bazzoun 2026 (RNM/Holm constriction σ + EIS) — converges toward exactly the contact-network conductivity solve our DEM provides, now extended by us to a full ionic/electronic/thermal triad plus MPM plastic morphology."
- "Their well-performing window (AM 69–79 vol%) and the porosity-shift of the optimum (62/38 → 72/28 vol% as porosity rises 5→20%) cross-validate, at the structure-descriptor level, our dead-SE/dead-AM composition limits and porosity–composition coupling."

---

## 10. 주의/한계 (over-claim 방지)

- **σ 절대 비교 *불가*.** 이 논문은 유효 σ 를 *안 푼다* — percolation 존재·utilization·기하 A_spec 까지. 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 *수치 직접 비교 금지*. 비교 가능한 건 *percolation 임계·utilization·active interface·β=0.41·p_c(d) 추세*뿐.
- **재료-무관/예시 소재.** NCM-622+LPS 는 *wt% 환산용 라벨*; percolation 은 기하에서 나옴 → **NMC811/LPSCl 로 재료-특이 절대값 끌어오기 금지**. 우리 소재계 절대값은 Minnmann/Bazzoun/Cronau 소유.
- **placement(입력) porosity ≠ 우리 압밀(측정/예측) porosity.** 그들 porosity 는 *지정*; 우리 15.6%(DEM)·16.7%(MPM)는 *압밀로 예측*. **두 ~20% (그들 percolation-recovery 21% vs 우리 rigid-sphere 압밀 floor 20%)는 의미가 다른 양** — 동일시 금지.
- **단봉 PSD.** AM uniform 단봉만; bi/tri-modal 은 *향후 과제* 명시 보류 → **Furnas dip(분포 효과) 다루지 않음**. 그들 "입경 효과"(Fig5,6)는 *크기* 효과지 *분포* 효과 아님. dip 은 우리(또는 de Larrard) 소유.
- **β=0.41 의 정밀.** β=0.41 은 *Bielefeld 가 자기 미세구조에 fit 한 값*이고 Sur 3D site-perc 와 *부합*. 우리 √(φ−φc)의 지수 0.5(mean-field, 데이터-locked)와 *등치 주장 금지* — "같은 3D-percolation universality class" 까지만. 이중인용(Bielefeld 2019 + Sur ref 37).
- **압밀 역학·소성·형상 *전혀 없음*** → frame[1]/[2] 의 우리 MPM 영역(SHAPE 소성·void-fill·변형장)은 *완전히 그들 밖*. frame[5] 분업에서 그들은 *transport-구조 절반*(그것도 σ 미solve)만.
- **두께 "thin-only" 경고.** 그들 Fig 10 의 얇은-전극 favorable 은 *유한크기 인공물*이라 *경고* — long-diffusion/charge-discharge 성능을 *반영 못 함*. 우리 thin 예측 인용 시 함께 명시.
- **digitized vs stated:** β=0.41·p_c 식·이상조성·창(69–79)·porosity 기준은 모두 *본문/식 stated*. Fig 의 정확한 데이터점(p_c ±1–2 vol%, A_spec 곡선)은 *digitized 추세*. CSV 에 source_type 으로 구분.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
