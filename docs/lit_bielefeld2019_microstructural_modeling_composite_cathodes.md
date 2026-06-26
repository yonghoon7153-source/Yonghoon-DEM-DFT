# Bielefeld 2019 (J. Phys. Chem. C 123, 1626–1634) — 복합 양극 미세구조 모델링 (Janek 그룹, GeoDict)

**인용:** Anja Bielefeld, Dominik A. Weber, Jürgen Janek, "Microstructural Modeling of Composite
Cathodes for All-Solid-State Batteries", *J. Phys. Chem. C* **2019**, *123*, 1626−1634.
DOI **10.1021/acs.jpcc.8b11043**.  Received 2018-11-14, Revised 2018-12-25, Published 2018-12-31.
소속: Physikalisch-Chemisches Institut + Center of Materials Research (LaMA), **Justus-Liebig-Universität
Gießen** (Janek 그룹) + **Volkswagen AG, Group Research, Wolfsburg** (Bielefeld, Weber).
연락저자 anja.bielefeld@volkswagen.de / juergen.janek@phys.chemie.uni-giessen.de.

**소재(모델):** AM = **NCM-811**(LiNi₀.₈Co₀.₁Mn₀.₁O₂) 또는 **NCM-622**, SE = **LPS**(thiophosphate,
Li₃PS₄ 계 / β-Li₃PS₄)로 *예시*만 함.  ★ 실제 계산은 거의 **재료-무관**(particle shape·size·overlap만 입력;
"no material characteristics except the particle's shape, size, and overlap behavior have been used" — 본문 결론).
조성을 wt%로 환산할 때만 NCM-622 + LPS 밀도를 사용(예: 72/28 vol% = 86/14 wt%).

**도구:** **GeoDict** (Math2Market GmbH, Version 2018 SP 5) — 상용 디지털 재료 연구소(voxel 기반).
→ ★ **우리 positioning(NOVELTY.md §1)에서 "필드 주류 = GeoDict류 연속체/voxel 특성화"의 바로 그 도구.**

**중요 — SI 파일 불일치 경고:** 이 디제스트와 함께 업로드된 `SI_06.txt`는 **전혀 다른 논문**(Choi et al.,
elastomeric Li-metal anode, Korea Univ.)의 SI다.  Bielefeld 2019 본 논문과 무관하므로 **완전히 무시**했다.
이 디제스트의 모든 수치·그림·식은 **9쪽 본문 PDF에서만** 추출했다(Bielefeld 2019에는 별도 SI가 본문에
deposit되지 않음 — 모든 데이터가 본문 Fig 1–10 + Table 1 + Eq 1–9에 있음).

DB 동반 파일: `docs/data/bielefeld2019_percolation.csv` (입경별 percolation threshold + utilization
+ 비표면적, digitized 추세).

---

## ★ 결론 한 문단 — 이건 우리 DEM+MPM의 *가장 가까운 구조-모델링 peer*다 (단 top-down placement)

Bielefeld 2019은 **3D 복합 양극 미세구조를 만들어 percolation·utilization·active interface(접촉)·입경·조성·
porosity·전극두께를 분석**한, 비-GeoDict-특성화 중에서 **우리 DEM-패킹 + Kirchhoff/Holm 네트워크 + Stage-E
coverage 파이프라인과 가장 직접 비교되는 구조-모델링 논문**이다.  그러나 **미세구조 생성 방식이 결정적으로 다르다**:
그들은 **확률적 배치(stochastic placement)** — SE는 "겹침 허용 convex polyhedra", AM은 "겹침 없는 구"를 박스에
**랜덤하게 던져 넣고**, 겹침을 *사후에* 한 입자씩 옮겨 ~10⁻⁵ vol%까지 제거(AM)하거나 SE에 흡수(overlap을 AM에
할당)시킨다.  여기엔 **압력·힘·소성 같은 공정 물리가 전혀 없다** — porosity·composition·size는 *입력 파라미터*이지
*공정의 결과*가 아니다.  즉 **top-down / stochastic-placement (Choi·Kim 2024 taxonomy)**: 우리는 **bottom-up /
process-physics formation** (DEM 압축으로 porosity가 *나온다*).  그들이 우리와 *겹치는* 것 = percolation 임계·
이온/전자 cluster·접촉(active interface)·입경 효과·조성 최적·tortuosity 비명시 transport.  우리가 *더하는* 것 =
(i) 공정→구조(압밀) 예측, (ii) granular 접촉망 **constriction σ 삼중항**(ionic+electronic+thermal, Kirchhoff/Holm
— 그들은 σ를 *아예 계산 안 함*, percolation 존재 여부와 cluster 부피만), (iii) **MPM 소성 morphology/void-fill/
strain field**, (iv) **Furnas dip 정량**(그들은 단봉 입경만, 분포 없음).  그들이 *앞서는* 것 = **GeoDict 성숙도·
Hoshen-Kopelman cluster 분석·percolation 임계의 깨끗한 power-law(β=0.41) + 입경-percolation 로그식
`p_c=7.83·ln(d)+36.67 vol%`**.  소재는 NCM+LPS *예시*뿐 사실상 재료-무관 → **frame[4]-style 구조 descriptor
교차검증**(percolation 임계·접촉·조성 최적의 *추세* 비교)에 적합하나, σ 절대값·porosity 절대값 비교는 불가
(그들은 σ를 안 내고 porosity는 입력값).

---

## §1. 논문이 답하는 질문과 답

### 핵심 질문
ASSB 복합 양극에서 **잘-percolating 네트워크(이온 *그리고* 전자 둘 다)를 위한 경계조건은 무엇인가?**
구체적으로: porosity·조성(AM:SE)·AM 입경·입경분포·전극두께가 percolation에 어떤 영향을 주며, **고성능을 위한
이상 조성·설계 가이드라인을 미세구조 모델링만으로 도출**할 수 있는가?

### 핵심 답 (논문 abstract + 결론)
1. **작은 AM 입자**가 유효 전자전도에 유리 — 높은 비표면적 → AM-AM 접촉 가능성↑ → percolating 전자 cluster↑.
   percolation 임계가 **입경에 로그 의존**: `p_c = 7.83·ln(d/µm) + 36.67 vol%` (Eq 8).
2. **Porosity가 이온·전자 전도를 결정적으로 좌우** — 고-porosity는 SE/AM 입자를 분리시켜 두 cluster 모두 끊음.
   저자들은 "**실험 연구가 porosity를 *반드시* 측정/보고**해야 한다"고 강하게 권고(우리 측에 시사하는 바 큼).
3. **이상 조성**(전자 percolation ∧ 이온 percolation 둘 다 + active interface 최대)은 **porosity 의존**:
   - porosity 5% → **62/38 vol%** AM:SE (= NCM-622+LPS 환산 **80/20 wt%**)
   - porosity 10% → **66/34 vol%** (= **82/18 wt%**)
   - porosity 20% → **72/28 vol%** (= **86/14 wt%**)
   → porosity↑일수록 이상 AM 분율은 *높은 쪽*으로 이동(porosity가 SE를 희석하므로 이온 percolation 위해 AM↑).
4. **전극두께의 영향은 *얇은* 전극에서만** — 두꺼운 전극(20–140 µm)에서는 active interface가 거의 동일.
   얇은 전극은 finite-size 효과로 percolation 임계가 약간 낮아지고(더 잘 percolate) **percolation 효과가 억제**되어
   "유리한 전극 특성"의 착시를 줌 → 두꺼운 전극의 percolation을 얇은 전극으로 추정하면 안 됨.
5. **이 전부를 *재료 특성 없이*** 입자의 shape·size·overlap만으로 도출 → 설계 가이드라인 제공.

---

## §2. 미세구조 생성 방법 ★ (가장 중요 — 우리와 결정적 차이)

### 2.1 두-성분 모델 (Fig 1)
복합 양극을 **2-submodel**로 구성(carbon·binder는 *의도적으로 배제* — §2.3):
- **AM submodel**: **겹침 없는(no overlap) 구(球)**, **균일(uniform) 입경**(단봉 — bi/tri-modal은 *향후 과제*로
  명시 보류).  입자를 박스 전체에 **랜덤 분포**.  목표 solid volume까지 채운 뒤, 남은 겹침을 **한 입자씩 허용거리
  내로 이동**시켜 제거; 안 되면 입자당 최대 10회 반복 → 대부분 겹침을 **~10⁻⁵ vol%까지 최소화**.  밀집 패킹(고-AM
  vol%)에서는 겹침 제거가 어려워짐: 최고-AM(~65 vol%)에서 겹침이 **~1 vol%까지** 도달(등크기 구의 기하 한계
  **74%**[Tóth, ref 31]에 근접 때문) — 비균일 분포를 넣으면 더 높은 패킹으로 이동하나 입력 파라미터가 늘어 *보류*.
- **SE submodel**: **겹침 허용(with overlap) convex polyhedra**(볼록 다면체).  겹침 허용은 LPS의 **상대적으로
  낮은 Young's modulus ~25 GPa**(ref 32–34)와 **좋은 연성(ductility)**의 *합리적 근사*(SE가 변형해 공극을 메우는 것을
  *기하적 겹침*으로 흉내).  SE 입경 = enclosing sphere 지름.

### 2.2 두 submodel의 "결혼(marriage)"
AM과 SE를 따로 만든 뒤 합침.  ★ **겹침은 AM에 *할당*** — AM이 구를 유지하도록(겹친 부피를 AM 쪽으로 귀속).
이러면 복합체에서 **SE 부피 손실**이 생기므로, **SE substructure를 *사전에* 더 치밀하게(denser)** 만들어 보상:
- porosity 정의: `φ = V_pore / V_total` (Eq 2) = `1 − (V_AM + V_SE)/V_total` (Eq 3).
- 부피분율(전체 부피 기준 = superscript V, porous 포함): 주어진 조성·porosity에서
  `g^V_AM = (1 − g^S_SE)(1 − φ)` (Eq 4),  `g^V_SE = (1 − φ)/[(1 − φ) + φ/g^S_SE]` (Eq 5).
  (superscript S = solid 기준 분율 = 조성 표기에 직접 쓰는 값.)
- Eq 5는 SE-substructure 생성 시 *electrolyte가 채워야 할 solid 부피분율*을 계산 — SE 생성 단계엔 AM이 아직
  없고, 나중에 결혼에서 AM이 SE-substructure의 일부를 *잡아먹어* 최종 목표 조성/porosity가 달성됨.

### 2.3 carbon/binder 배제 (우리 측 직접 관련)
실제 복합 양극은 **5성분**(AM, SE, conductive agent, binder, pore).  본 연구는 **binder·carbon을 배제**:
(i) 실용적 이유로 Strauss et al.(ref 13)의 **carbon-free** 실험과 맞추려고; (ii) **carbon black이 thiophosphate
SE와 접촉 시 분해 반응**(ref 7,23,24)을 일으키므로 carbon-free가 바람직; (iii) AM coating(예: Li₆Nb₂Ta₃...-oxide,
Li₄Ti₅O₁₂, LiNbO₃, Li₂O–ZrO₂)은 *나노스케일·충분한 전하수송*이라 percolation에 **무시 가능 영향**(ref 26) → 모델에서
제외해도 무방.  → ★ **carbon black이 SE 분해를 일으킨다**는 근거는 우리 carbon-free DEM 가정에도 동일하게 유효.

### 2.4 ★ 핵심 — 전자전도는 *AM*만, 이온전도는 *SE*만
- **SE는 단일이온전도체**(electronic σ 무시) → **이온 cluster에만** 기여.
- **AM은 이온전도 무시**(SE 대비 ~5–6 orders of magnitude lower, ref 35) → **전자 cluster에만** 할당.
- 즉 **이온 path = SE 연결망**, **전자 path = AM 연결망** (carbon-free라 AM이 유일 전자전도체).
  → ★ 이 **상-역할 분리가 우리와 정확히 같다**: 우리도 σ_ionic = SE backbone, σ_electronic = AM backbone(carbon-free)
  로 모델링(σ_ionic 폼 = √φ_eff·CN²·..., σ_e 폼 = φ_AM⁴·√A_AM-AM·...).

### 2.5 도메인/해상도
- microstructure dimensions: **(80 × 80 × 140) µm³**, resolution **0.2 µm/voxel** (= 200 nm).
- 전극두께 140 µm = **미래 thick 전극** 대표; 200 nm 해상도는 입경 3 µm까지 모델 가능.
- Table 1 입력 파라미터(전체):
  | parameter | value |
  |---|---|
  | microstructure dimensions | (80 × 80 × 140) µm³ |
  | resolution | 0.2 µm/voxel |
  | shape of AM | spherical |
  | particle size of AM | {3,4,5,6,7,8,9,10,15} µm |
  | particle size distribution of AM | **uniform**(단봉) |
  | shape of SE | convex polyhedra |
  | particle size of SE | **3 µm** |

### 2.6 ★ Choi/Kim taxonomy 분류 — top-down / stochastic placement
- **공정 물리 없음**: 압력·힘·소성·접촉법칙·시간적분이 *전혀 없다*.  porosity·조성·입경은 모두 *입력값*이고
  미세구조는 **랜덤 배치 + 사후 겹침조정**으로 만들어진다.  → **bottom-up *formation*(우리)이 아니라 *placement*.**
- 단, GeoDict의 "convex-polyhedra-with-overlap"은 단순 hard-sphere RSA보다는 *조금* 더 물리적(SE 연성을 겹침으로
  근사) — 그러나 이는 **소성 *흐름*이 아니라 기하적 겹침**(우리 DEM δ-overlap 프록시와 같은 층위, 진짜 SHAPE flow 아님).
- 결론: **top-down(stochastic placement) 구조-모델링 peer.**  우리 NOVELTY.md §1 표의 "top-down/reconstruction
  (필드 주류)" 열에 정확히 들어감(GeoDict ConductoDict/DiffuDict 류와 같은 계보, 단 이 논문은 σ를 안 풀고
  *percolation 존재/cluster 부피*까지만 감).

---

## §3. Percolation 이론 & 분석 방법 ★

### 3.1 percolation 이론 배경 (§Percolation Theory)
- percolation = 임계현상·상전이.  occupied/unoccupied site 네트워크의 connectivity를 검사.
- **order parameter Θ**가 임계점 `p_c`(percolation이 처음 관측되는 critical occupation probability)에서 급변.
  임계 위에서 power-law: **Θ ∝ (p − p_c)^β** (Eq 1), β = critical exponent(Grimmett, ref 21).
- finite-system에서는 상전이가 통계적 변동으로 *번짐*(smeared); 무한계만 날카로운 임계 가짐.
- **subcritical(p < p_c)** = 비-percolating, **supercritical(p > p_c)** = percolating.
- ★ ASSB에서 percolation 임계의 의미: 고성능엔 **이온 *그리고* 전자 둘 다** cathode 전역 percolation 필요(ref 11).

### 3.2 cluster 식별 — Hoshen-Kopelman
- occupied/unoccupied site 네트워크 생성 → connectivity 검사.  한 경계에서 시작해 **이웃 occupied site를
  cluster에 추가**(재귀)해 전체 구조를 훑음 — **Hoshen-Kopelman 알고리즘**(ref 22).
- **전역(throughout the whole structure)을 관통해 양 경계를 잇는 cluster = percolating cluster.**
- 이온 cluster: current collector(상부)에서 시작, SE separator 쪽까지 연결 검사.
- 전자 cluster: current collector 쪽에서 시작, AM 연결 검사.
- Fig 1에서 전자 cluster = **노란색(yellow)**, 이온 cluster = **연한 파랑(light blue)**, 분리(미연결) 입자 = 빨강.

### 3.3 utilization level (이용률) θ_ν — Eq 6
**θ_ν = V_c / V_ν** (Eq 6): c = cluster(ionic 또는 electronic), ν = solid component(AM 또는 SE).
= percolating cluster에 속한 AM(또는 SE) 부피 / 전체 AM(또는 SE) 부피.
→ ★ **우리 "dead-AM"/"utilization"과 동일 개념**(연결망에 못 든 입자는 전기화학적으로 죽음).  우리 σ_e 폼의
`f_AM^cc`(connected AM 분율), Minnmann 2021의 utilization과 같은 물리.

### 3.4 비표면적 / active interface — Eq 7
**A_spec**(specific surface area, m²/m³) = 구조 부피당 cluster 표면적; 또는 이온-전자 cluster *사이*의 면적 =
**active interface area A_spec,a**(= 리튬 intercalation 가능 면적, 고에너지·고출력에 중요).
- 기하 한계(전부 고립 없이 노출 시): `A_spec,geo = g^V_AM·(A_sphere/V_sphere) = g^V_AM·(6/d)` (Eq 7).
  → ★ **우리 coverage/active interface(A_AM-SE)와 직접 대응**.  단 우리는 **Hertz/Tabor 접촉면적**(소성 보정)으로
  *실제 전도 접촉면적*을 계산하는 반면, 그들 A_spec,a는 **cluster 경계의 기하 표면적**(접촉의 *소성 변형* 무시).

### 3.5 ★ 명시적 한계 — 접촉저항·구속저항을 *안 푼다*
본문 그대로: "Apart from ionic intercalation, electronic conduction has to be assured... these do **not take
into account possible resistances occurring at particle-particle interfaces and constriction resistances** which
reflect the fact that electric contacts have to be regarded as a large number of interacting microcontacts (ref 36)."
→ ★ **결정적 차이**: 그들은 **percolation 존재 여부 + cluster 부피(utilization) + 기하 표면적**까지만.
**constriction σ(Holm) / Kirchhoff 전류해 / 유효 전도도 절대값은 *계산하지 않는다*.**  우리(그리고 Bazzoun)는
바로 그 constriction 저항 R=1/(2σr_c)과 Kirchhoff Σ(φi−φj)/R=0를 푼다 = 우리가 *더하는* 핵심.
ref 36 = **Greenwood 1966 "Constriction resistance and the real area of contact"** — 우리 Holm 1967과 같은 계보
(저자들도 이 물리를 *알고* 있으나 "future work"로 두고 본 논문은 percolation까지만).

---

## §4. Figure-by-figure (모든 수치)

### Fig 1 — 미세구조 모델링 모식 (GeoDict)
- 좌→우: SE(convex polyhedra with overlap, 짙은 파랑) + AM(spherical without overlap, 빨강) → 복합 양극(overlap을
  AM에 할당) → percolation cluster(전자 = 노랑, 이온 = 연파랑).
- **우리 참고:** 우리 DEM 압밀(LIGGGHTS) → 네트워크 추출 파이프라인과 1:1 대응되는 *그림 구성*.  단 그들 1단계는
  랜덤 배치(우리는 압력 압축), 3단계는 percolation cluster 존재까지(우리는 그 위에 σ 솔버).

### Fig 2 — 입경별 전자 cluster 예시 (AM 55 vol%)
- AM 지름 {5, 10, 15} µm 세 미세구조, 전자 cluster = 노랑, 미연결 = 빨강.  **동일 AM 분율 55 vol%**에서:
  - **d=5 µm**: 전자 cluster가 잘 percolate(노랑 多).
  - **d=10 µm**: utilization 더 낮음.
  - **d=15 µm**: 큰 입자는 percolating cluster *거의 없음*(빨강 多).
- → ★ **작은 입자 = 더 잘 percolate**(같은 vol%라도) — 우리 "size = packing/contact 효과"와 정합(작은 SE→σ↑를
  AM 쪽에서 본 버전: 작은 AM→전자망↑).

### Fig 3 — utilization level + 비표면적 vs AM vol% (d = 5 µm)
- **좌(utilization %)**: 5 µm AM 분율 vs AM utilization → **percolation 전이**.  48 vol% 미만 = 둘 다 매우 낮음
  (입자 빈약 연결, cluster가 구조를 관통 못 함).  **48–52 vol% 전이영역**에서 각 분율당 **10개 미세구조** 계산
  (통계 변동 큼: 같은 AM 분율이라도 랜덤 패킹에 따라 utilization ~70% 또는 ~30%로 갈림).  >52 vol%에서 saturation
  (포화)으로 접근.  (45 vol%의 작은 perturbation = 그 두 점이 단일 패킹 기반이라 생긴 noise.)
- **우(A_spec, 10⁵ m²/m³)**: 같은 percolation 전이 따라감(정의상).  단 utilization은 *정규화된* 양, A_spec 절대값은
  입경 의존.  포화 시 **기하 최대(Eq 7 점선)에 근접** — 거의 모든 입자가 cluster에 들고 고립 입자 少.
- → ★ utilization(정규화) vs A_spec(절대) 구분 = 우리 coverage(정규화 %) vs A_AM-SE(절대 m²) 구분과 같은 논리.

### Fig 4 — power-law 검증 (log–log, d = 10 µm)
- percolation 임계 *바로 위*에서 전자 cluster 비표면적을 8개 패킹밀도로 계산 → log–log에서 **power-law fit**:
  `A_spec(p−p_c) = 1.73×10⁵·((p−p_c)/vol%)^0.41 m²/m³`.
- ★ **critical exponent β = 0.41** — Sur et al.(ref 37)의 **3D site-percolation on simple cubic lattice**와 잘 일치
  → "percolation power-law가 이런 입자 배열에 *적용된다*"는 검증.  임계 근방에서 error bar(표준편차) 큼.
- → ★ **우리 f_p(percolation fraction)·percolation 임계 분석의 이론적 정당화**: 우리 σ 폼의 √(φ−φc), φ_AM⁴ 등
  percolation-backbone 지수들과 같은 Stauffer-Bruggeman/site-percolation 계보.

### Fig 5 — utilization + A_spec vs AM vol%, 입경 3–15 µm 전부
- 좌(utilization), 우(A_spec).  **작은 입자일수록 낮은 AM 분율에서 percolating cluster 형성**.  전이영역:
  **3 µm = 41–46 vol%**, **15 µm = 52–57 vol%**로 이동.  전이 *기울기*는 입경 무관 비슷.
- **utilization vs A_spec 거동 차이**: 작은 입자 = 더 높은 A_spec(비표면적↑).
- → ★ 우리 AM:SE 스윕 + 입경 효과의 직접 대응; 작은 입자가 저-분율 percolation 가능 = 우리 작은 SE/AM packing 우위.

### Fig 6 — ★ percolation 임계 vs 입경 (로그식, Eq 8)
- percolation 임계 정의 = **10개 배열 중 *과반*이 percolating cluster를 갖는 AM 분율**(= 평균 utilization이 40%인 지점).
- 입경 3–15 µm에 대해: **p_c = 7.83·ln(d/µm) + 36.67 vol%** (Eq 8) — **로그 관계**.
  - 대략: d=3 → ~45.3 vol%, d=5 → ~49.3, d=7 → ~52.0, d=10 → ~54.7, d=15 → ~57.9 vol%(곡선 읽기).
- → ★ **우리가 흡수할 정량식**: 전자 percolation 임계 = `f(ln d_AM)`.  우리 σ_e 폼의 입경 의존(r_SE^β 등)·dead-AM
  warning 임계를 이 로그식과 대조 가능.  단 **단봉·랜덤배치·carbon-free·LPS-overlap 가정**의 임계임을 명시(우리
  bimodal·압축·VGCF와 *직접 절대 동일시 금지*, 추세·스케일만).

### Fig 7 — ★ utilization(좌) + active interface(우) vs 총 AM vol% (porosity 20%, d = 5 µm)
- 하축 = 전체(porous 포함) AM 분율, 상축 = solid 내 AM:SE vol%(50/50→80/20).
- **좌**: AM(파랑)·SE(빨강) utilization.  **전자 한계(electronic limitation)** = AM **69 vol% 미만**(= 69/31 vol%),
  **이온 한계(ionic limitation)** = AM **79 vol% 초과**(= 79/21 vol%).  → **well-performing 구간이 *좁다*** (69–79 vol%).
  - 흥미로운 점: 모델에서 SE를 *겹치게* 설계해도, **고-AM-지배** 미세구조에선 SE가 잘-연결 이온 cluster를 못 만듦.
- **우**: active interface area A_spec,a → AM↑면 *감소*(고-AM서 SE 표면 줄어듦).  **최적 = 72/28 vol%**
  (= NCM-622+LPS **86/14 wt%**).
- → ★ **우리 production core(AM 70–85 wt% ≈ SE 30–50 % of solid)와 정합**: 그들 vol% 최적 72/28 = wt% 86/14는 우리
  고-AM core 상단.  이온/전자 *양쪽* percolation을 만족하는 좁은 창 = 우리 dead-AM/dead-SE 양끝 경고와 같은 물리.

### Fig 8 — ★ active interface vs 조성, **porosity 5/10/20%** 비교 (d = 5 µm)
- A_spec,a vs AM:SE vol%, 세 porosity.  **작은 porosity = 고밀도·고질량로딩 → active interface *훨씬* 큼**
  (5% ≫ 10% > 20%).  또 **전자 percolation 전이가 더 작은 AM 분율에서** 일어남(고밀도).
- **이상 조성 (porosity별):**
  - **5% porosity → 62/38 vol% = 80/20 wt%** (NCM-622+LPS)
  - **10% porosity → 66/34 vol% = 82/18 wt%**
  - **20% porosity → 72/28 vol% = 86/14 wt%** (Fig 7과 일치)
- → porosity↑ → 이상 AM 분율 *상승* + 고-porosity서 이온 한계가 더 두드러짐(최적 위쪽 drop이 20%서 더 가파름).
- → ★ ★ **우리 "porosity 관계식에 조성 항 + (이 논문은) porosity별 최적 조성 이동" 직접 데이터**.  우리 Furnas dip
  최적(AM 70–85 wt%)이 porosity에 따라 *이동*하는지 점검할 cross-check.  ★ 그들 최적 **62/38 vol% @ 5% porosity =
  우리 σ_ionic 골치 corner "62:38"과 동일 조성** — 우연이지만, 이 조성이 *이온/전자 균형점*이라 민감한 이유의 한 단서.

### Fig 9 — ★ porosity 의존 (조성 70/30 vol% 고정, d = 5 µm)
- utilization(좌)·active interface(우) vs 총 AM 분율, porosity **43% → 3%** 스윕.
- **고-porosity(>34%)** = 이온·전자 *둘 다* 고립영역 발생.  **21%까지** 전자 한계 잔존; **<21%** → cathode가
  "잘 작동해야 함(ought to perform well)".  → ★ **그들의 percolation-기반 porosity 임계 ~21–34%**.
- active interface: porosity↓ → 더 많은 입자(AM·SE 둘 다) 연결 → 표면적↑(단조).
- → ★ **그들 percolation 관점의 "porosity floor for good performance" ≈ 21%**(전자 한계 해소).  우리 강체-구 floor
  ~20%·Doux 18%·Varkey 21/37%와 **놀랍게 같은 수치대** — 단 *의미가 다름*: 그들 21%는 "percolation이 회복되는
  porosity"(전도-기능 임계)이고 우리/Doux 20%는 "압력으로 못 닫는 *기하* porosity floor"(압밀 한계).  **둘이 21%
  근처에서 만나는 건 흥미로운 우연**(둘 다 강체-구 패킹의 산물) — 인용 시 *의미 구분* 필수.

### Fig 10 — ★ 전극두께 효과 (porosity 20%, 조성 70/30, d = 5 µm)
- 140 µm 두께를 **20·40·60·80·100·120·140 µm로 잘라** active interface 비교.
- **대부분 두께서 active interface 거의 동일**(곡선 겹침).  최적 조성은 두께 무관.  단 최적 *아래*에서 곡선 모양이
  다름(특히 전자 cluster 쪽 — current collector 쪽에서 시작하므로).
- **얇은 전극**: 초기-연결 입자가 전체의 더 큰 분율 차지 → active interface가 *증강*(저-AM서도).  **percolation 임계가
  더 작은 AM 분율로 약간 이동**(finite-size 효과) → percolation 효과 *억제* → "유리한 특성" 착시.  = **reduced
  model-size effect(유한크기 효과)**.  이온전도는 두께 영향 거의 없음(Fig 7 drop이 모든 두께서 구분 안 됨).
- → ★ **두꺼운 전극의 percolation을 얇은 전극으로 추정 금지** — 우리 RVE 크기 수렴(Bazzoun box factor 35) 점검과
  같은 교훈.  단 모델은 **긴 확산경로를 모사 안 함** → C-rate·charge/discharge 직접 반영 못 함(저자 명시).

---

## §5. Post-processing ★

- **무엇:**
  - **Hoshen-Kopelman cluster labeling**(ref 22) → percolating cluster 식별(이온/전자 각각).
  - **utilization level θ_ν = V_c/V_ν** (Eq 6) — connected 부피분율.
  - **specific surface area A_spec** + **active interface A_spec,a** (cluster 경계 기하 표면적; Eq 7 기하 한계).
  - **percolation power-law fit** Θ∝(p−p_c)^β → β=0.41 (Fig 4, log–log).
  - **percolation 임계 로그 fit** p_c=7.83·ln(d)+36.67 (Fig 6).
  - **porosity convention**: `φ=V_pore/V_total` (Eq 2) — **단순 부피분율**(우리 ε_sphere/ε_union 구분 같은 소성-보정
    개념 *없음*; 강체 기하 부피).  porosity는 *입력*(생성 시 목표값)이지 측정 결과 아님.
- **통계:** 전이영역서 분율당 **10개 랜덤 미세구조** 평균±표준편차(랜덤 패킹 변동 흡수).  power-law는 **8개 패킹밀도**.
- **도구:** **GeoDict 2018 SP5**(Math2Market) — voxel 생성 + cluster 분석.  power-law/로그 fit은 GeoDict 출력의
  후처리(그림에 식·error bar).
- **수치화·플롯:** utilization(%)·A_spec(10⁵ m²/m³)를 vol% 축으로; log–log(Fig 4); porosity/두께 상-하축 병기(Fig 7–10).
- ★ **명시적 미산출:** σ_eff(ionic/electronic) **절대값 없음**, constriction/contact 저항 없음, tortuosity *수치* 없음
  (본문에 "tortuosity가 thick 전극서 역할"이라 언급하나 *계산은 안 함* — "not explicitly treated in this study").

---

## §6. 비교 vs 우리 DEM+MPM ★ (핵심 섹션 — `our_dem_baseline.md` 대조)

### 6.1 구조-모델링 head-to-head (가장 직접 비교)
| 항목 | Bielefeld 2019 | 우리 DEM+MPM | 차이 / 이유 |
|---|---|---|---|
| **미세구조 생성** | **랜덤 배치**(AM 구 no-overlap + SE polyhedra overlap) + 사후 겹침조정 (GeoDict) | **DEM 압력 압축**(LIGGGHTS hooke/hysteresis) → porosity가 *나옴* | ★ **placement vs process-physics** — 그들 porosity·조성·입경 = *입력*, 우리 porosity = *공정 결과* |
| **소성/형상변화** | SE overlap = 기하 근사(연성 흉내), 진짜 SHAPE flow ✗ | DEM δ-overlap(프록시) + **MPM 진짜 소성 형상변화**(SEM 일치) | 둘 다 DEM은 구 프록시; **우리는 MPM이 진짜 흐름 추가** |
| **percolation** | ✅ Hoshen-Kopelman, 이온/전자 cluster, β=0.41, p_c=f(ln d) | ✅ f_perc_x/y/z, percolation 임계, √φ_eff·CN²·f_p³ | **같은 물리**(site-percolation) — 우리 σ 폼이 percolation backbone 내장 |
| **utilization/dead** | ✅ θ_ν=V_c/V_ν (연결 부피분율) | ✅ f_AM^cc(connected AM), dead-AM warning | **동일 개념** ✓ |
| **active interface/coverage** | A_spec,a = cluster 경계 *기하* 표면적 (Eq 7) | **Stage-E 소성 접촉면적**(Hertz/Tabor), coverage %, A_AM-SE | 우리는 *접촉의 소성 변형* 포함(Tabor); 그들은 기하 표면적만 |
| **유효 σ (ionic/e/thermal)** | ✗ **계산 안 함**(percolation 존재 + cluster 부피까지만; constriction은 "future work") | ✅ **Kirchhoff/Holm σ 삼중항**(ionic+electronic+thermal) | ★ **우리가 더하는 핵심** — 그들은 σ 절대값 자체가 없음 |
| **tortuosity** | 언급만, *미산출* | ✅ τ(Laplace/Dijkstra), σ_thermal Ridge 입력 | 우리 정량 τ |
| **PSD/Furnas** | **단봉 uniform**만(bi/tri-modal = 향후 과제) | ✅ bimodal 12:4:1 + **Furnas dip 정량**(AM 70–85 wt%) | ★ 우리 분포·dip; 그들은 입경 *하나*만 |
| **소재** | NCM-811/622 + LPS *예시*, 사실상 재료-무관(shape/size/overlap만) | LPSCl + NCM811, E_eff/σ_y/Cronau σ_grain 등 재료 파라미터 | 그들 재료-무관 → 절대값 비교 불가, *구조 추세*만 |
| **검증** | 구조만(Strauss ref 13 carbon-free 정성 일치) | DEM↔MPM 독립 cross-validation + 실험 앵커(Minnmann/Bazzoun) | 둘 다 실험 직접 측정 아님(모델) |

### 6.2 percolation/contact 교차검증 — 추세 일치하는가?
- ★ **일치 (frame[4]-style 구조 descriptor 교차검증):**
  - **작은 입자 → 저-분율 percolation**(Fig 5–6) = 우리 "작은 SE/AM = packing/contact 우위".
  - **utilization/dead-AM 개념** 동일(θ_ν = 우리 f_AM^cc).
  - **고-AM = 이온 한계, 저-AM = 전자 한계, 중간 좁은 창**(Fig 7) = 우리 dead-SE/dead-AM 양끝 + Minnmann 2021
    "CAM↑→σ_ion↓, σ_e↑, 42 vol% 교차" 와 같은 trade-off.
  - **이상 조성 72/28 vol% (86/14 wt%) @ 20% porosity** ⊂ 우리 production core(AM 70–85 wt%).
  - **percolation power-law β=0.41**(3D site-percolation) = 우리 percolation-backbone 지수의 이론 정당화.
  - **good-performance porosity ~21%**(전자 한계 해소) ≈ 우리 강체-구 floor ~20%/Doux 18%/Varkey 21% — **단 의미
    다름**(그들=전도 회복 임계, 우리=압밀 기하 floor; 21% 근처 만남은 둘 다 강체-구 패킹 산물인 우연, 의미 구분 필수).
- ★ **직접 비교 *불가* (절대값):**
  - **σ 절대값**: 그들은 σ를 *안 냄* → 우리 σ_ionic 0.04–0.18 mS/cm·Bazzoun 0.137 등과 비교할 σ가 없음.  비교
    가능한 건 *percolation 임계·utilization·active interface 추세*뿐.
  - **porosity 절대값**: 그들 porosity = *입력*(5/10/20%) → 우리 측정 porosity(15.6%·~10%)와 *동일시 금지*.  그들은
    "이 porosity면 percolation이 어떻게 되나"를 보고, 우리는 "이 압력이면 porosity가 얼마 나오나"를 봄 — **질문이 다름**.
  - **조성 vol%↔wt% 환산**: 그들 wt%는 *NCM-622+LPS* 밀도 기반(우리 NCM-811+LPSCl과 미세 차) → wt% 직접 동일시 주의.

### 6.3 ★ 방법 분류 → NOVELTY positioning (litdb/NOVELTY.md용 — 읽기만, 편집 안 함)
- **그들 = top-down / stochastic placement**: 미세구조가 *주어진/입력된* 파라미터(porosity·조성·입경)로 랜덤
  배치되고, 그 위에서 percolation/접촉/표면적을 *특성화*.  GeoDict ConductoDict/DiffuDict 류와 같은 "연속체/voxel
  특성화 엔진" 계보(단 이 논문은 σ PDE까지 안 가고 percolation cluster까지만).  → NOVELTY.md §1 표 "top-down/
  reconstruction (필드 주류)" 열, §4 portion map에 **역할 = A(anchor, percolation 추세) + M(methodology peer)**.
- **우리 = bottom-up / process-physics formation**: 공정(압력·조성·입경·첨가제)에서 미세구조를 *예측*(DEM 압축+MPM
  소성) + 연속체가 놓치는 **granular constriction σ 삼중항** + **MPM 소성 morphology**.
- ★ **이 논문이 우리 novelty를 *선명하게* 해주는 이유**: Bielefeld는 우리와 *가장 가까운* 구조-모델링 peer인데도
  (i) 구조를 *던져넣고*(우리는 *압축해 만들고*), (ii) σ를 *안 풀고*(우리는 Kirchhoff/Holm 삼중항), (iii) 입경
  *하나*에 분포 없음(우리는 bimodal+dip).  즉 **"공정→구조 예측 + 접촉망 σ + 소성 morphology"** 세 portion이
  *정확히 그들이 비운 칸*에 들어감.  Janek 그룹 자신의 후속(Bazzoun 2026)이 *바로 그 σ 솔버*(RNM/Holm)를 추가한
  것 = 우리 방향이 옳다는 그룹-내부 증거(Bielefeld 2019 percolation → Bazzoun 2026 RNM σ → 우리 σ 삼중항+MPM).

---

## §7. 우리 연구에 적용 인사이트 (가장 날카로운 3가지)

1. **★ percolation 임계 로그식 + porosity별 이상 조성 = 우리 σ_e/dip 관계식의 구조-검증 앵커.**
   - `p_c(전자) = 7.83·ln(d_AM/µm) + 36.67 vol%` (Fig 6) → 우리 σ_e 폼의 입경 의존·dead-AM 임계와 *추세* 대조.
   - 이상 조성 **62/38(5%)·66/34(10%)·72/28(20%) vol%** → 우리 Furnas dip 최적(AM 70–85 wt%)이 **porosity에 따라
     이동**하는지 점검(그들은 porosity↑→AM↑로 이동).  → `docs/data/bielefeld2019_percolation.csv`로 보관.

2. **★ "porosity를 *반드시* 측정/보고하라"는 그들의 강한 권고 = 우리 porosity-중심 모델링의 권위 있는 근거.**
   - 그들 핵심 메시지: porosity가 이온·전자 percolation을 *결정적으로* 좌우하는데 실험들이 자주 *안 보고*함 → 비교
     불가.  우리는 porosity를 *공정에서 예측*하므로(DEM 압축), 이 gap을 *입력측에서* 메움 = NOVELTY §2-1 직접 강화.
   - good-performance porosity **~21%**(전자 한계 해소, Fig 9) → 우리 강체-구 floor ~20% 서사와 **수치는 같되 의미
     구분**(그들=전도 회복, 우리=압밀 floor) — deck에서 둘을 *함께* 쓰되 의미 명시.

3. **★ 그들이 *비운 칸* = 우리 3대 novelty의 정확한 위치**(positioning 최강 근거).
   - σ 절대값(constriction/Kirchhoff) 없음 → **우리 σ 삼중항**(+ Bazzoun이 같은 그룹서 RNM으로 *후속* 추가 = 방향 검증).
   - 진짜 소성 SHAPE flow 없음(SE overlap = 기하 근사) → **우리 MPM morphology**.
   - 단봉 입경만 → **우리 bimodal + Furnas dip 정량**.
   - 공정 물리 없음(랜덤 배치) → **우리 DEM 압축 예측**.

---

## §8. 인용 가능 문장 (deck/paper용)

- "Bielefeld et al. (Janek group, *J. Phys. Chem. C* 2019) established the closest structural-modeling
  precedent to our DEM+MPM pipeline — 3D microstructure generation of a carbon-free composite cathode
  followed by ionic and electronic *percolation* analysis (Hoshen-Kopelman), utilization level, and active
  interface area.  Crucially, their microstructures are built by **stochastic placement** (random non-overlapping
  AM spheres + overlapping SE polyhedra) with porosity, composition, and particle size as *inputs*, and they
  stop at percolation existence and cluster volume — they **do not solve for the effective conductivity itself**
  (constriction/contact resistances are explicitly deferred to future work).  Our process-physics DEM compaction
  (porosity as an *output*), our Kirchhoff/Holm constriction-resistance conductivity *triad*
  (ionic+electronic+thermal), and our MPM plastic morphology together occupy exactly the boxes their model
  leaves open — a gap later partly filled, on the same materials, by the same group's RNM solver (Bazzoun 2026)."
- "Their electronic-percolation threshold follows a logarithmic dependence on AM particle size,
  p_c = 7.83·ln(d/µm) + 36.67 vol%, and the percolation power-law exponent β = 0.41 matches 3D site-percolation
  on a simple-cubic lattice — independent theoretical support for the percolation-backbone exponents in our
  σ scaling laws.  Their ideal compositions (62/38, 66/34, 72/28 vol% AM:SE at 5/10/20% porosity) and their
  'good-performance' porosity of ~21% bracket our production core (AM 70–85 wt%) and our rigid-sphere porosity
  floor (~20%), respectively."

---

## §9. 주의 / 한계 (over-claim 방지)

- **stochastic placement (≠ 공정 물리):** porosity·조성·입경이 *입력값* → 우리 압밀 porosity(측정 결과)와 **절대
  동일시 금지**.  비교 가능한 건 *구조 descriptor 추세*(percolation 임계·utilization·active interface)뿐.
- **σ 절대값 *없음*:** 이 논문은 유효 전도도를 *안 푼다*(percolation 존재 + cluster 부피까지).  우리 σ_ionic/σ_e·
  Bazzoun σ_eff,ion과 **σ 직접 수치 비교 불가** — constriction/Kirchhoff는 그들의 명시적 "future work"(ref 36
  Greenwood 1966).  → ★ 이게 우리가 *더하는* 핵심이므로 인용 시 "그들은 percolation까지, 우리는 그 위에 σ"로 명확히.
- **재료-무관(거의):** NCM+LPS는 wt% 환산용 *예시*뿐, 계산은 shape/size/overlap만 → **소재-특이 절대값**(σ_grain,
  E_SE, porosity floor)을 이 논문에서 끌어오면 안 됨.  단 *구조-기하 추세*는 재료-무관이라 오히려 전이성 높음.
- **단봉(uniform) PSD:** bi/tri-modal은 *향후 과제*로 *보류* → **Furnas dip을 이 논문은 다루지 않음**.  우리 dip
  정량(de Larrard/McGeary)과 비교할 dip 데이터가 *없음*(그들 입경 효과는 단봉 입경 *크기* 효과지 *분포* 효과 아님).
- **porosity 의미 구분(중요):** 그들 "good-performance porosity ~21%"(Fig 9) = *전자 percolation이 회복되는*
  porosity(전도-기능 임계)이지, *압력으로 못 닫는 기하 floor*(우리/Doux 18–20%)가 아니다.  **둘이 21% 근처에서
  만나는 건 우연**(둘 다 강체-구 패킹 산물) — deck에서 함께 쓰되 *의미를 반드시 구분*.
- **2D vs 3D:** 이 논문은 *3D*(80×80×140 µm³) — 우리 3D MPM/DEM과 차원 일치(장점).  단 해상도 200 nm → 3 µm 입자가
  하한(우리 12:4:1 작은 SE는 이 해상도서 미해상 — 우리 512 grid 수렴 논의와 같은 한계를 그들도 가짐).
- **확산경로 미모사:** 모델은 percolation/cluster 기하만 — **긴 확산경로·tortuosity 수치·C-rate를 직접 반영 안 함**
  (저자 명시).  thick 전극 결론은 *접촉 clustering* 관점만 유효(전기화학 성능 ≠ percolation만).
- **carbon/binder 배제:** 5성분 중 2개 제외(carbon-free 정당화는 ref 7,23,24 SE 분해) → 우리 VGCF/PTFE 함유계와
  *조성-절대* 비교 금지.  단 carbon-free 가정 자체는 우리 carbon-free DEM과 *일치*.

---

## §10. 미니 용어집 (technique glossary)

- **percolation threshold p_c** — 무한 네트워크가 *처음* 관통-연결되는 임계 점유확률.  여기선 AM 분율(전자) / SE
  분율(이온).  유한계에선 전이가 번짐 → 그들은 "10개 중 과반 percolate"로 정의(평균 utilization 40%).
- **order parameter Θ & critical exponent β** — 임계 위 Θ∝(p−p_c)^β.  β=0.41(그들 fit) = 3D site-percolation
  보편값(Sur et al.).  우리 σ 폼 √(φ−φc)·φ^4 등의 percolation-backbone 지수와 같은 universality class.
- **Hoshen-Kopelman** — cluster labeling 알고리즘(1976).  격자/voxel 점유 site의 연결성분을 한 번 훑어 라벨링 →
  percolating cluster 식별.  우리 f_perc/연결성분 분석의 표준 알고리즘.
- **utilization level θ_ν = V_c/V_ν** — percolating cluster에 속한 component(AM/SE) 부피분율.  = 우리 f_AM^cc
  (connected AM 분율)·"dead-AM"의 반대.  Minnmann 2021 utilization과 동일.
- **specific surface area A_spec / active interface A_spec,a** — 구조 부피당 cluster 표면적 / 이온-전자 cluster
  *사이* 경계 면적(= intercalation 가능 면적).  우리 coverage·A_AM-SE에 대응하나 *기하 표면적*(소성 접촉 변형 미포함).
- **constriction resistance** — 점접촉을 통과하는 전류의 수렴저항 R∝1/(σ·r_c) (Greenwood 1966 / Holm).  ★ 그들이
  *명시적으로 배제*하고 우리(+Bazzoun)가 푸는 바로 그 물리.
- **convex polyhedra with overlap** — SE를 볼록 다면체로 모델링하고 겹침 허용(LPS 연성을 기하적으로 근사).  진짜
  소성 *흐름*이 아니라 *기하 겹침*(우리 DEM δ-overlap과 같은 층위; MPM 진짜 SHAPE flow와 다름).
- **finite-size effect (reduced model-size effect)** — 얇은 전극(작은 모델)에서 percolation 임계가 낮아지고
  초기-연결 입자 분율이 커져 "유리한 특성" 착시가 생기는 유한크기 현상(Fig 10).  우리 RVE 수렴(box factor) 점검과 동일.
- **g^V vs g^S** — 부피분율의 두 기준: superscript V = 전체 부피(porous 포함), superscript S = solid 기준(조성 표기값).
  Eq 4–5가 둘을 잇는다.  우리 φ_SE(solid 기준)·총 부피분율 구분과 같은 회계.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
