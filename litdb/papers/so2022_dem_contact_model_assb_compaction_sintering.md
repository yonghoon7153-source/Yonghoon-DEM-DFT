# ASSB 전극 압밀·소결 DEM을 위한 접촉모델 (탄성+소성+점탄성 + 소결 + 면적/스프링 인자) — So (MethodsX 2022)

> slug `so2022_dem_contact_model_assb_compaction_sintering` · DOI `10.1016/j.mex.2022.101857` (원논문 `10.1016/j.jpowsour.2022.231279`) · type `DEM` (methods/접촉모델 정의서) · PDF `So_2022_MethodsX_DEM_ContactModel_ASSB_Compaction_Sintering.pdf` · digested `2026-06-26` · status ✅ · OPEN ACCESS (CC BY)

## 1. 한 줄 요약
**우리가 이미 digest한 So 2021 (JPS, LPS+Si cold-press DEM)의 *접촉모델 그 자체*를 따로 떼어 완전히 유도한 동반(companion) MethodsX 논문.**
핵심은 **Maxwell 점탄성 모델에서 유도한 "평형 overlap(h_eq)의 *변화율(rate)*" 소성·점탄성 접촉법칙**(So 2021의 h_eq를 *왜·어떻게* 그렇게 정의하는지의 1차 도출)과, **porosity→0일 때 강체-구 접촉의 수치 파탄(접촉면적·스프링 상수 과소평가)을 막는 두 인자 — 면적 인자 c_area 와 스프링 인자 c_spring**, 그리고 **소성·점탄성 + 소결(sintering, 융착 결합 fusion bond)을 한 rate 식 안에 통합**한 점이다.
즉 So 2021이 "결과(상대밀도·σ_SE)"라면 So 2022는 "엔진(접촉모델 방정식)"이며, **우리 hooke/hysteresis(Luding) no-cap LAW + Stage-E(Tabor 소성면적) + 18× 연화** 삼층을 *한 논문이 어떻게 통합 처방하는지*의 가장 직접적인 문헌 대응물이다. ⚠ 단 **소재는 LPS(Li₂S–P₂S₅) + NCM/LiCoO₂**(우리 LPSCl 아님), **전달 솔버는 전혀 없음**(순수 역학/압밀 접촉모델) — 우리 σ 삼중항·Kirchhoff·MPM morphology는 *이 논문 범위 밖*이다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Magnus So, Gen Inoue (교신), Kayoung Park, Keita Nunoshita, Shota Ishikawa, Yoshifumi Tsuge** (Kyushu University, Dept. Chemical Engineering) | **MethodsX 9 (2022) 101857** | 10.1016/j.mex.2022.101857 (원논문 DOI 10.1016/j.jpowsour.2022.231279) | **LPS = Li₂S–P₂S₅** SE + **NCM/LiCoO₂** AM (Table1 E_AM=199·H_AM=11.2 = Cheng LiCoO₂) | **DEM 접촉모델 유도/정의서** (MethodsX = Method Article); 압밀(mold compaction) 적용 |

> **MethodsX란?** 원 연구논문의 *방법*만 재현가능하게 상세 기술하는 Elsevier 동반 저널.
> 이 논문의 "original method" 참조 = **So 2022 JPS 530, 231279** ("Simulation of the Compaction of an ASSB Cathode with Coated Particles using DEM").
> 즉 이 MethodsX는 **그 JPS 양극-코팅 압밀 논문의 접촉모델 부록**이며, 동시에 **So 2021 JPS 508, 230344**(=우리가 digest한 LPS+Si 논문, ref [1])과 **So 2021 JES 168, 030538**(ref [2], "ductile particles")의 모델을 통합·심화한 것이다.
> ⚠ **소재 주의:** 우리(LPSCl + NMC811)와 다르다. SE = **LPS(Li₂S–P₂S₅, argyrodite 아님)**; AM = **NCM/LiCoO₂ 양극**(Table1 E_AM=199 GPa·H_AM=11.2 GPa = Cheng et al. LiCoO₂ — So 2021의 Si 음극 E=70·H=10.6 과 *다름*). 절대값 전이 금지, *방법·추세*만.

## 3. 핵심 물성·파라미터 (수치)
> 데이터 CSV: `docs/data/so2022_contact_model_params.csv`

| 물성/파라미터 | 값 | 조건 (출처) | stated/digitized | 비고 |
|---|---|---|---|---|
| **E_SE (LPS)** | **24 GPa** | Sakuda [4] | stated (Table 1) | 우리 real-bulk 24 와 *수치 동일*(우연; LPS도 sulfide) |
| **E_AM (NCM/LiCoO₂)** | **199 GPa** | Cheng [10] LiCoO₂ | stated (Table 1) | ⚠ Table1 라벨이 "SE Young modulus (LPS)"로 오기됐으나 값 199 = LiCoO₂ → AM은 양극. So 2021의 Si(70) 과 다름 |
| **H_SE (LPS hardness)** | **1.9 GPa** | McGrogan [8] | stated (Table 1) | **항복 임계 F_th 를 H로 근사**(σ_yield ≈ H). LPS가 무름 → SE만 소성 |
| **H_AM (NCM hardness)** | **11.2 GPa** | Cheng [10] | stated (Table 1) | AM은 단단 → 소성 거의 안 함 |
| ν (Poisson) | 0.3 (both) | This study | stated (Table 1) | |
| μ (마찰) | 0.5 | This study | stated (Table 1) | Coulomb |
| e (COR) | 0.5 | This study (arbitrary global) | stated (Table 1) | damping η = f(e), eq 12 |
| **c_area (면적 인자)** ★ | **2** | Fig 8a, Sakuda 피팅 | stated | A = A_Hertz·(1 + c_area·h_eq/R_eff); 0/2/5 중 2 최적 |
| **c_spring (스프링 인자)** ★ | **5** (생산) / 7 (E수렴) | Fig 7–8 | stated | k = k_Hertz·(1 + c_spring·h_eq/R_eff)^{3/2}; c_spring=7이면 solid frac→1서 E_electrode→E_LPS |
| **h_ov^max (소결/압밀 한계)** ★ | **0.6·R_eff** | Fig 4b/8b | stated | over-compaction 방지 상한; 0.4/0.6/0.8 중 0.6 최적(Sakuda) |
| F_th 포물선 인자 | 2/3 | eq 5–6 | stated | 접촉 초기 최대응력 = 평균의 3/2 → 유효면적 ×2/3 |
| Hertz kn 지수 | 1/2 | eq 15 | stated | kn = 4/3·E_eff·h_ov^{1/2}·R_eff^{1/2} |
| 스프링-인자 지수 | 3/2 | eq 9 | stated | 면적↑ + 길이수축 둘 다 → 3/2 |
| t_press/t_rel (점탄성) | 0.1/1/10/100 | Fig 9 | stated | 가압시간 vs 점탄성 완화시간; 비 ↑ → 상대밀도↑ |
| 상대밀도 vs P (mono, c_area=2) | ~0.72@100 → ~0.9@400 → ~1.0@600+ MPa | Fig 8 | digitized | Sakuda 실험과 ~200 MPa 위 잘 일치; 저압 과치밀(응집체 미모델) |
| 입자수 (mono / coated) | 1,846 SE (mono) / 10,746 AM + 27,263 SE (coated) | Table 2 | stated | mono = 순수-LPS 보정용; coated = SE-코팅-AM |
| 입경 (primary AM / SE) | 1 / 0.5 µm | Table 2 (coated) | stated | aggregate: AM 5 µm, SE 1.45 µm |
| 도메인 | 10×10 µm (mono) / 20×20 µm (coated) | Table 2 / Fig 6 | stated | mono box 14.8(@50)→11.2 µm(@400); coated 23.9 µm(@360) |
| **전달 (σ_ionic/e/thermal)** | **n/a — 없음** | — | — | ★ 순수 역학/압밀 접촉모델. 전달 솔버·percolation·tortuosity 전혀 없음 |
| **Heckel P_y / knee** | n/a (Heckel 안 함) | — | n/a | 상대밀도-vs-P 곡선만; knee ~150–200 MPa 부근 (digitized) |
| **PSD (D10/D50/D90)** | n/a (명시 표 없음) | — | n/a | primary 0.5/1 µm + aggregate 1.45/5 µm 만 |

## 4. 시뮬레이션 방법 ★ — 접촉모델 완전 유도

이 논문의 본체는 **접촉법칙 방정식의 단계적 유도**다. 아래는 *모든 식*을 순서대로(elastic → 평형overlap 도입 → Maxwell 점탄성 유도 → 소결 rate → 면적/스프링 인자 → 압밀 한계 → 점탄성 적용).

### 4.0 code / version
- **code**: **in-house DEM** (So 그룹 자체, MATLAB 추정 — So 2021과 같은 계보). LIGGGHTS/LAMMPS 아님. "original method"는 Cundall–Strack 1979 [12].
- 적분/이웃탐색 등 수치 세부는 이 MethodsX에 상세 없음(So 2021 본문 참조 — Verlet 2차, kd-tree).

### 4.1 탄성 접촉역학 (Elastic contact mechanics) — eq 10–18
입자쌍 총력 (eq 10):
```
F_{i,j}^{particle-pair} = F_{i,j}^{normal} + F_{i,j}^{tan}
```
법선력 = 스프링(밀어냄) + dashpot(에너지 소산) (eq 11):
```
F_{i,j}^{normal} = ( −F_{i,j}^{spring} + η (u_i − u_j)·n_{i,j} ) n_{i,j}
```
damping η는 COR e로부터 (eq 12, = 우리 hooke/hysteresis와 동일한 표준식):
```
η = −2 ln(e) · √( m_eff·k_n / (ln²(e) + π²) )
```
스프링력(탄성) (eq 14):
```
F_spring = k_n · h_ov          (h_ov = overlap distance)
```
비선형 Hertz 스프링 상수 (eq 15):
```
k_n = 4/3 · E_eff · h_ov^{1/2} · R_eff^{1/2}
```
유효반경·유효모듈러스 (eq 16–17):
```
R_eff^{-1} = R_i^{-1} + R_j^{-1}
E_eff^{-1} = (1−ν_i²)E_i^{-1} + (1−ν_j²)E_j^{-1}
```
접선력 = Coulomb 마찰 (eq 18):
```
|F_{i,j}^{tan}| ≤ μ |F_{i,j}^{normal}|
```
**→ 여기까지는 정확히 우리 hooke/hysteresis(Luding 2008)·Bazzoun·Varkey의 탄성 Hertz 부분과 동일.** 차이는 다음 절부터.

### 4.2 평형 overlap(h_eq) 도입 — 소성의 핵심 (eq 1, Fig 1–2)
**문제의식:** 압축 후 *압력을 풀어도* 두 입자가 서로 멀어지지 않고 **영구적으로 붙어 있다**(cold-press 소성). 이를 **평형 overlap h_eq**(소성변형으로 접촉점이 비구형이 된 *새 평형 위치*)로 표현. 스프링력은 *실제 overlap에서 평형 overlap을 뺀 만큼*만 발생 (eq 1):
```
F_spring = k_n (h_ov − h_eq) = 4/3 · E_eff · R_eff^{1/2} · h_ov^{1/2} · (h_ov − h_eq)
```
- **Fig 2(a)**: 상대 스프링력(=스프링력/F_th) vs 상대 overlap. 처음엔 Hertz(점선) 따라가다(파랑 "initial spring force"), 상대력이 1을 넘으면 **소성변형 시작**(검정 "plastic deformation" = h_eq 증가선), release 시 **오른쪽으로 평행이동한 곡선**(주황 "final spring force", h_eq>0에서 시작).
- **Fig 2(b)**: h_eq^rel = 0 / 0.05 / 0.1 / 0.15 별 release 곡선 — h_eq가 클수록 곡선이 더 오른쪽에서 시작(영구 overlap 큼). "Line of plastic deformation"이 모든 곡선의 상단 포락.
- **물리 의미:** h_eq = **우리 hooke/hysteresis의 잔류 overlap(δ_residual)·우리 Stage-E의 소성-함몰**과 같은 양. **이 논문이 그것을 *동역학(rate)*으로 정의**하는 게 새로움(다음 절).

### 4.3 모델 유도 — Maxwell 점탄성에서 소성 rate 도출 ★★ (eq 2–6)
**출발점 = Maxwell 점탄성 모델**(스프링+dashpot 직렬). 일정 응력에 대해 (eq 2):
```
σ = η ∂ε/∂t = E·t_rel · ∂ε/∂t          (t_rel = η/E = 완화시간 relaxation time)
```
여기서 **E = k_n/A, ε = Δh_eq/h, σ = F/A** 를 대입 → **소성력 rate 식** (eq 3):
```
F_plasticity = k_n · t_rel · ∂h_eq/∂t
```
**cold-press 가정:** 소성흐름은 *임계력 F_th 를 넘는 초과분*에서만 진행 → `F_plasticity = F_spring − F_th` → **평형 overlap의 변화율(압축 중)** (eq 4):
```
∂h_eq/∂t = (F_spring − F_th) / (t_rel · k_n)
```
- **t_rel 역할:** 점탄성 시뮬레이션에선 *재료 점도*에 연결(creep). **소성 전용 시뮬레이션에선 단순 완화항**이며, **t_rel ≪ 시뮬레이션 시간**으로 두어 *정상상태(steady-state)*가 되게 함. (점탄성 모드에선 t_rel이 중요 — §4.7/Fig 9.)

**임계력 F_th(항복) — 경도 H로 결정** (eq 5):
```
F_th = min(σ_i^{yield}, σ_j^{yield}) · A_con^{eff}
```
문헌에 항복강도 정보가 부족하므로 **σ^yield ≈ H(경도)로 근사**(= 우리 Stage-E가 H≈3σ_y 쓰는 것과 같은 발상; 여기선 직접 H로). 유효 접촉면적 (eq 6):
```
A_con^{eff} = 2/3 · A_con^{spherical} = 2/3π · h_ov · R_eff
```
**2/3 인자**: 소성 시작 직전 접촉 응력분포가 *포물선*이라 최대응력이 평균의 3/2배 → 유효(항복판정)면적은 ×2/3. (A_con^spherical = π·h_ov·R_eff = 구-구 겹침 접촉원 면적.)

### 4.4 소결(sintering) — 융착결합 fusion bond을 같은 rate 식에 통합 ★ (eq 7, Fig 3)
**LPS 같은 고변형성 재료는 상온에서도 고압 소결(room-temperature pressure sintering)이 가능** [4]. 이를 **융착결합(fusion bond, 점착 cohesive 상호작용)**으로 모델: overlap이 평형 overlap보다 *작아지면*(인장 쪽) 스프링력이 **음(인력)**이 되어 끌어당김. 두 소성과정 = **consolidation(압축 융착)** + **detachment(인장 분리)**. 분리는 `F_spring < −F_th`에서 일어나며 그때 h_eq가 0까지 감소(융착 끊김).

**통합 rate 식 (eq 7)** — 부호에 따라 3분기:
```
∂h_eq/∂t =  (F_spring − F_th)/(t_rel·k_n)   if  F_spring > F_th        (consolidation, 압축 융착)
            0                                if  −F_th < F_spring < F_th (불변, dead band)
            (F_spring + F_th)/(t_rel·k_n)    if  F_spring < −F_th       (detachment, 융착 끊김)
```
- **Fig 3(a)**: 상대 consolidation rate(∂h_eq/∂t) vs 상대 스프링력. **압축(>F_th)에서 양의 rate(융착↑), 인장(<−F_th)에서 음의 rate(분리), 중간 dead band는 0.** 점선 화살표 = 진행방향.
- **Fig 3(b)**: 융착결합 포함 입자쌍 힘-변위 곡선 — "consolidation / compression / tension / detachment" 영역 표시. 더 깊이 압축될수록(검정 화살표) 더 큰 인장력이 있어야 분리됨("더 많이 융착된 입자는 떼는 데 더 큰 인장 필요").
- ⚠ **AM에는 융착 허용 안 함**(NCM/Si는 고온에서만 소결 — cold-press 전 aggregate 내부엔 이미 융착 있을 수 있음). 융착은 **변형성 SE(LPS)에만**.

### 4.5 ★ 면적 인자 c_area & 스프링 인자 c_spring — porosity→0 수치 파탄 처방 (eq 8–9, Fig 4)
**문제 (porosity → 0):** 고압축에서 강체-구 *겹침 근사(spherical overlap)*가 **접촉면적과 스프링 상수를 과소평가**한다. 세 원인(§Additional info, p9):
1. 소성흐름으로 접촉점에서 *재료가 밀려나* 실제 접촉면적이 구-겹침 예측보다 **크다**(pile-up).
2. 입자 형상이 변하며 *2차 접촉(secondary contacts)*이 생기는데 구-겹침으론 안 잡힘.
3. 고변형서 "주어진 변위 → 힘" 의존이 더 이상 유효하지 않음(force underestimated).

**처방 1 — 면적 인자(area factor)** (eq 8): 소성흐름이 접촉면적을 키우는 걸 h_eq에 비례해 보정.
```
A = A_Hertzian · ( 1 + c_area · h_eq / R_eff )
```
- 접촉면적↑ → 같은 압력에서 입자간 압밀응력↓ → 추가 압밀에 *더 높은 몰드압 필요*. c_area는 **패킹밀도를 실험(Sakuda)에 맞추는 피팅 파라미터** [1,6]. **c_area=2 채택**(0/2/5 테스트, Fig 8a).

**처방 2 — 스프링 인자(spring factor)** (eq 9): 스프링 상수도 h_eq에 비례해 강화.
```
k = k_Hertzian · ( 1 + c_spring · h_eq / R_eff )^{3/2}
```
- **지수 3/2 이유:** 스프링 상수는 (면적↑) AND (길이 수축) 둘 다로 증가, 그리고 스프링력의 h_ov 증가도 3/2 지수 → 3/2 채택.
- **c_spring의 물리적 의미(Fig 7b):** solid fraction→1일 때 **전극 유효 영률 E_electrode 가 *벌크 LPS의 E*로 수렴해야** 물리적. c_spring=3/5/7 중 **c_spring=7이라야 E_electrode/E_LPS → 1**(완전치밀=벌크). → c_spring은 *치밀체가 벌크처럼 단단해지는* 거동을 강제하는 인자.

- **Fig 4(a)**: c_spring·c_area 효과. c_area=0(점선)=면적보정 없음 vs c_area=2(실선); c_spring=2 강조. 면적↑이 곡선을 *오른쪽*(더 큰 overlap에서 같은 힘 = 더 무름·압밀 저항)으로.
- **Fig 4(b)**: **압밀 한계 h_ov^max** 효과 (다음 절).
- **Fig 5**: 항복강도 σ^yield (a) 와 영률 E (b) 의 force-displacement 영향. **σ^yield는 곡선의 *수직*(임계력) 방향, E는 *수평*(측방) 방향**을 지배 — **E가 F_th(항복)에 주는 영향은 미미**(±20% E 스윕에서 임계력 거의 불변). ★ 이 분리가 핵심 통찰: *항복은 σ_y/H가, 강성은 E가* 각각 다른 축을 지배.

### 4.6 ★ 압밀(소결) 한계 h_ov^max — over-compaction 방지 (Fig 4b, 8b)
**문제:** 고압축서 평형 overlap이 무한정 증가 → solid fraction이 1을 초과(비물리적 over-compaction). 문헌의 Voronoi 방법(다면체 부피로 국소면적 추정)은 *계산비용 큼*. **간단 대안:** 평형 overlap에 *상한* 부과.
```
h_eq (또는 h_ov) ≤ h_ov^max = 0.6 · R_eff     (default)
```
- **0.6·R_eff 선택 근거:** solid volume fraction→1 (≈600 MPa 고압) 케이스에 대응. Fig 8b에서 0.4(과소밀도)/0.6(최적)/0.8(과밀)·R_eff 비교 → **0.6이 Sakuda 실험과 가장 잘 맞고 over-compaction 회피**.
- **Fig 4(b)**: h_eq^rel=0/0.2/0.4/0.6 곡선; "consolidation limit"에서 곡선이 *수직 급상승*(더 못 들어감) = 강체-벽 같은 잼밍.

### 4.7 점탄성 적용 — Li 같은 strain-rate 민감 재료 (eq 2, Fig 9)
모델은 **점탄성으로도 확장** 가능. 일부 응용에선 *완화시간 t_rel 자체가 중요*(creep)하며, 공정시간 대비 점탄성 응답시간의 *비*가 중요.
- **Fig 9(a)**: t_press/t_rel = 0.1/1/10/100 별 힘-변위 곡선.
- **Fig 9(b)**: 상대밀도 vs 몰드압 (t_press/t_rel = 1/10/10000). **비가 클수록(가압이 완화보다 느릴수록) 더 치밀** — 점탄성 재료가 충분히 흐를 시간을 가짐. **배터리에선 Li(점탄성·strain-rate 민감 [19])에 적용 가능**.
- 즉 **소성(t_rel≪sim, 정상상태) ↔ 점탄성(t_rel 유한, 율속 의존)** 이 *하나의 rate 모델*의 두 극한.

### 4.8 입자 처리 ★★ (DEM판 "무질서 처리")
- **구(sphere)만** — AM·SE 모두 완벽 구. **형상은 절대 변하지 않는다.** 소성은 **CONTACT 소성**(평형 overlap h_eq = 접촉점 국소 함몰/융착의 proxy)이며 **진짜 입자 SHAPE 흐름(void-fill flow)이 아니다.**
- 단 So 2021/Varkey/Bazzoun보다 *접촉 소성의 정교함*은 최상급: **rate 기반 h_eq + 융착(소결) + 면적/스프링 인자 + 압밀 한계**. = *접촉 수준에서 가능한 거의 모든 보정*을 넣었으나, **입자 외형 자체는 구로 남는다**.
- SE는 코팅 시 **aggregate(1.45 µm SE 응집체, 5 µm AM 응집체)** — primary 0.5/1 µm 구의 집합이지만 응집구조 자체가 multi-scale.
- ★ **명시 한계(저자 스스로, p9):** "고변형서 spherical overlap 근사가 깨진다(접촉면적·2차접촉·force 모두 과소)" → 이를 *인자로 패치*했을 뿐, **연속체 소성 형상장은 못 줌**.

### 4.9 도메인/RVE / servo / seeds / 압력범위
- **mono(보정)**: 1,846 SE 입자, 10×10 µm 측방 박스. **coated(적용)**: 10,746 AM + 27,263 SE, 20×20 µm.
- **압력**: mono 50/100/400 MPa(Fig 6) + 상대밀도-vs-P 곡선은 **~700 MPa까지**(Fig 8); coated 360 MPa(Fig 6d). press 프로파일 = **PI/servo로 200 MPa까지 램프 후 release**(Fig 7a inset).
- **seed**: 다중실현·통계 명시 없음(보정용 단일 실현으로 보임).
- **coated 입경·분율**: Nakamura et al. [9]에서 가져옴(AM/SE 크기·상대부피분율).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | **접촉모델 모식**: (a) spring+slider+dashpot + **파란 dashpot(소성/점탄성)**, (b) cold-press 중 overlap h_ov, (c) 압축후 **평형 overlap h_eq** | h_eq = 우리 hooke/hysteresis 잔류 overlap·Stage-E 함몰의 *동역학적* 버전. (a)의 파란 dashpot = Maxwell 소성 가지 |
| 2 | **힘-변위 release 곡선**: (a) Hertz→소성→final spring (h_eq 오른쪽이동), (b) h_eq^rel=0/0.05/0.1/0.15 별 | 소성 이력(hysteresis)의 정식 그림 — 우리 hooke/hysteresis 적재/제하 루프와 직접 대응 |
| 3 | **소결(융착) rate**: (a) consolidation rate vs 스프링력 (압축↑/인장↓/dead band), (b) 융착 포함 힘-변위(consolidation·detachment) | ★ **소결 = 우리가 안 가진 물리**. 융착 dead-band + detachment 임계 = `--coh` cold-weld 모델의 rate 버전 |
| 4 | **면적/스프링 인자 + 압밀 한계**: (a) c_area·c_spring 효과, (b) h_ov^max=0.6R_eff 한계(수직 잼밍) | ★ c_area = 우리 Stage-E 소성면적 대안; h_ov^max = 우리 ε_sphere over-compression 캡 대응 |
| 5 | **σ^yield(a)·E(b)의 힘-변위 영향** | σ_y는 *수직(임계력)*, E는 *수평(강성)* 지배; E의 항복영향 미미 = ±20% E 스윕 임계력 불변 → **항복캡과 E 연화가 *다른 축*임을 명시** |
| 6 | **입자분포 SEM-style**: (a–c) mono 50/100/400 MPa(박스 14.8→13.8→11.2 µm), (d) **SE-coated-AM 360 MPa(23.9 µm)** | morphology 정성 — 우리 vis_zoom·MPM morphology 대비(단 구라 형상변화 없음) |
| 7 | **c_spring 효과**: (a) 높이-시간(탄성회복=springback이 c_spring↑로 감소), (b) **E_electrode/E_LPS vs solid fraction(c_spring=7서 →1)** | ★ (b) = "치밀체가 벌크처럼 단단해진다"의 정량화; 우리 E_eff 연화와 *반대 방향*의 보정(강성 회복) |
| 8 | **★ 검증**: (a) 상대밀도 vs P, c_area=0/2/5 + **Sakuda 실험 다이아**, (b) h_ov^max=0.4/0.6/0.8 + Sakuda | **(a) 실험검증** = 우리 porosity@P 앵커 대응; **저압서 모델>Sakuda(과치밀) = 응집체 미모델 탓**(명시) |
| 9 | **점탄성**: (a) t_press/t_rel=0.1/1/10/100 힘-변위, (b) 상대밀도 vs P (비 1/10/10000) | 점탄성=소성의 율속 일반화; Li(strain-rate 민감)에 적용 — 우리 무관(우리 SE는 정상상태 소성) |

## 6. Post-processing ★
- **무엇**: 이 논문의 후처리는 **압밀(상대밀도) vs 몰드압** 곡선 + **전극 높이-시간**(springback) + **전극 유효 영률 E_electrode/E_LPS vs solid fraction**(c_spring 보정 검증) 뿐. **Sakuda et al. [4] 실험 상대밀도에 직접 중첩**해 c_area·c_spring·h_ov^max 3개 인자를 보정.
- ⚠ **percolation·tortuosity·coverage·coordination·전달 σ 후처리는 전혀 없음** (그건 So 2021 JPS·So 2022 JPS 본문 쪽; 이 MethodsX는 *접촉모델 엔진*만).
- **도구**: 자체 DEM 후처리. 외부 TauFactor/COMSOL 등 없음(전달 안 함).
- **수치화 방식**: 상대밀도를 몰드압(50–700 MPa)의 함수로 c_area∈{0,2,5}·h_ov^max∈{0.4,0.6,0.8}·c_spring∈{3,5,7} 스윕 → Sakuda 다이아와 시각 비교 → 최적값(2/0.6/5–7) 선택.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (So 2022) | 우리 | 차이 / 이유 (rigid·plastic / 소재 / 2D·3D / 단일·다중압력) |
|---|---|---|---|
| **DEM 접촉 소성** | **rate 기반 CONTACT 소성**(h_eq Maxwell rate + H 항복캡) — 문헌 최정교 | hooke/hysteresis(plasticity 無 by construction) + Stage-E(Tabor) 사후보정 | **같은 부류**(CONTACT 소성, δ/h_eq 잔류) — **진짜 SHAPE 흐름 아님**. So의 h_eq-rate가 우리 hooke/hysteresis보다 *명시적 항복캡* 보유 |
| **항복캡** | **✅ F_th = H·A_con (eq 5)** — H에서 응력 cap | **✗ 없음** (Luding no-cap LAW) → 18× 연화로 보상 | ★ **핵심 차이**: So는 항복캡이 있어 *real E=24로도* 압밀 재현. 우리는 캡이 없어 24→1.35 연화. **So의 H-cap = 우리 18× 연화의 물리적 대안**(=경로 A) |
| **E 연화** | **연화 안 함** (real E=24) | E_eff=1.35 (18× 연화) | So는 항복캡(eq5) + 면적/스프링 인자로 real E 사용 가능. ★ "연화 irreducible"은 *우리 hooke/hysteresis에 캡이 없는 탓*임을 재확증 |
| **소성 접촉면적** | **✅ 면적 인자 c_area (eq 8)**: A=A_Hertz(1+c_area·h_eq/R) | **Stage-E**(Tabor F/H + volume V/h + geom min-caps) | **같은 목표 다른 처방**: c_area는 *단일 피팅 인자*로 면적 키움; 우리 Stage-E는 *물리식 5-regime*(Tabor·volume·geom). **c_area = Stage-E의 1-파라미터 축약판** |
| **over-compaction 캡** | **✅ h_ov^max=0.6R_eff (Fig4b)**: 평형overlap 상한 | **ε_sphere over-compression min-caps**(A_tabor=F/H, A_volume=V/h_min, A_geom 하한) | ★ **직접 대응**: 둘 다 "겹침 무한증가 → solid frac>1 비물리" 방지. So는 *overlap 자체*에 상한; 우리는 *접촉면적 메트릭*에 min-cap(porosity는 ε_sphere로). 발상 동일 |
| **소결(sintering)** | **✅ 융착결합 rate (eq 7)**: consolidation+detachment dead-band | **✗ 없음** (우리는 압밀만, 소결 미모델) | ★ **그들이 앞섬**: 우리는 cold-press 압밀까지만. So는 *상온 압력소결*(LPS 융착)을 rate로. 우리 `--coh`/adhesion은 *정적* 점착이지 *rate 융착·detachment*가 아님 |
| **입자 형상** | 구만, 형상 불변 | 동일(구·rigid) | **같음** — 둘 다 rigid sphere; So도 비구형은 future work. **형상 morphology는 우리 MPM만** |
| **소재 SE** | **LPS (Li₂S–P₂S₅)**, E=24, H_SE=1.9 GPa | **LPSCl (argyrodite)**, E_eff 1.35 / real 24 | **다른 SE**. E=24 수치 우연 일치; H_SE=1.9는 우리가 안 쓰는 LPS 경도 |
| **소재 AM** | **NCM/LiCoO₂ 양극** (E=199, H=11.2) | **NMC811 양극** (E=140) | **같은 *부류*(양극, rigid·단단)** — So 2021의 Si 음극과 달리 이번엔 *양극*. E 199 vs 우리 140 |
| **차원** | **3D** (mono 10µm box, coated 20µm) | DEM 3D / MPM 2D·3D | **둘 다 3D** |
| **압력** | **다중**(50–700 MPa 상대밀도 곡선) | DEM 단일 300 + Heckel 4압력 | So 다중압력 상대밀도-vs-P → 우리 Heckel(P_y=138) 검증 유용 |
| **전달 솔버** | **✗ 전혀 없음** (순수 역학/압밀) | **Kirchhoff + Holm + Stage-E + 삼중항** | ★ **우리 압도적 우위**: So 2022는 σ_ionic/e/thermal·percolation·coverage 전무. *접촉모델 엔진만* |
| **MPM/morphology** | **✗ 없음** (구·CONTACT 소성) | **MPM J2 ν=0.49 진짜 소성 형상장 + scaffold 커플링** | ★ **우리 우위**: 입자 SHAPE 흐름·void-fill·Σdg 변형장 = 우리 MPM 고유 |
| **검증 앵커** | **Sakuda 실험 상대밀도**(LPS) | Minnmann/Doux/Bazzoun(LPSCl) + MPM 독립 | 둘 다 실험 앵커 보유; 단 *다른 소재*(LPS vs LPSCl) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **"real E + 접촉 항복캡(eq5) + 면적/스프링 인자(eq8/9)" = 우리 18× 연화 제거(경로 A)의 *가장 완성된 문헌 레시피*.** So 2021이 "H-cap로 0.98 달성"을 *보였다면*, So 2022는 *그 H-cap의 완전한 방정식 + porosity→0 수치 처방*까지 준다. → 우리 `elasto_plastic_feasibility.md`/`contact_models_layer_map.md §2 경로 A` 구현 시 **이 논문이 LAW 사양서**: eq5(F_th=H·A_con)로 항복, eq8(c_area)로 소성면적, eq9(c_spring)로 강성회복, h_ov^max=0.6R_eff로 over-compaction 캡. real E_SE=24 그대로 → 18× 연화 없이 300 MPa porosity 시험 가능(So가 LPS로 입증).
- ② **면적 인자 c_area ↔ 우리 Stage-E 의 *직접 대안 비교*.** 둘 다 "강체-구 접촉면적이 소성서 과소" 문제의 처방. **c_area = 1-파라미터 피팅**(A=A_Hertz(1+c_area·h_eq/R), c_area=2); **우리 Stage-E = 물리식 5-regime**(Tabor F/H, volume V/h, geom min-cap). → *같은 구조의 σ_ionic·coverage*에서 c_area-방식 면적 vs Stage-E 면적을 비교하면 **Stage-E의 물리적 우위(또는 c_area의 단순성)를 정량화**하는 비교연구 가능. (우리는 면적을 *전달 coverage·Holm*에 쓰고, So는 *압밀응력*에만 씀 — 그래서 우리 Stage-E가 한 발 더 나감.)
- ③ **h_ov^max 압밀 한계 = 우리 ε_sphere over-compression min-cap 의 문헌 형제.** 우리 CLAUDE.md가 "over-compression은 porosity가 아니라 *접촉면적 메트릭*에서 캡(network_conductivity.py:240-264 5-regime min-caps)"이라 했는데, So는 *overlap 자체*에 0.6R_eff 상한을 건다. → **우리 메트릭-캡과 So의 overlap-캡 두 전략을 명문화**(둘 다 solid frac>1 비물리 방지). 우리는 porosity를 ε_sphere(material-conserving)로 처리하므로 *overlap 상한이 굳이 필요 없을 수* 있으나, So식 0.6R_eff 캡을 도입하면 *극단 dense 케이스의 negative-ε*를 원천 차단 가능(=대안 처방).
- ④ **소결(eq7)은 우리가 *안 가진* 물리 — 흡수 후보.** LPS·LPSCl 같은 황화물은 상온 압력소결로 입계가 융착(Sakuda 입자 유합 SEM과 일치). 우리 `--coh`/adhesionStiffness는 *정적 vdW 점착*이지 *rate 기반 융착+detachment dead-band*가 아니다. → **장기 가압·소결 거동**을 다루려면 So eq7의 consolidation/detachment rate를 우리 LIGGGHTS pipeline에 도입할 가치(단 우리 핵심은 *transport*라 우선순위는 MPM morphology < 소결).
- ⑤ **Fig 5의 "σ_y는 수직(항복)·E는 수평(강성), E의 항복영향 미미"** = 우리 MPM 결론("BULK E가 dominant lever, σ_y는 부차")과 *접촉수준에서 정합*. 단 방향이 미묘히 다름: So는 *힘-변위 곡선의 두 축*을 σ_y/E가 나눠 지배한다 하고, 우리 MPM은 *압밀밀도*에 E가 dominant. 둘 다 "E와 σ_y는 분리 가능한 레버"라는 점에서 일치 → **우리 frame[2] "BULK E가 주 레버" 진술의 DEM-접촉 근거**.

## 9. ★ 우리 novelty — 왜 우리가 이 도메인 DEM에서 state-of-the-art인가 (our novelty vs So 2022)

> 근거 기반(그들 stated 범위·한계 인용), 과장 없이. So 2022는 **접촉모델/압밀 역학의 최정교 문헌 중 하나**지만, *역학 접촉모델 그 자체에 국한*된다. 우리 7대 차별점을 그들이 *하는 것/없는 것*에 매핑.

1. **★ 전달 TRIAD(σ_ionic + σ_electronic + σ_thermal)를 *하나의 명시적 접촉망*에서 (Kirchhoff + Holm 1967 구속저항).**
   So 2022는 **전달 솔버가 전혀 없다** — percolation·tortuosity·coverage·σ 어느 것도 계산하지 않는 *순수 압밀 역학 접촉모델*이다(논문 전체가 force-displacement·상대밀도). 심지어 그들 *동반* So 2021조차 σ를 *TauFactor τ-기반 상대값*으로만 뽑고 접촉구속저항(Holm)이 없다. ⇒ **우리는 같은 rigid-sphere 압밀 위에 σ 삼중항(이온·전자·열)을 Kirchhoff+Holm 명시 저항망으로 얹는다** — 이게 So 계보가 *구조적으로 비운 칸*이고 우리 transport novelty의 정확한 위치다.

2. **★ Stage-E 소성 접촉-AREA 재유도(Tabor F/H + volume + geom min-cap) — *전달에 연결된* 면적.**
   So의 **면적 인자 c_area(eq 8)는 *압밀응력 보정 1-파라미터*** — A를 키워 "더 높은 몰드압 필요"를 맞추는 *피팅값*이고, **그 면적이 전달로 가지 않는다**(σ 없음). 우리 Stage-E는 *같은 소성-면적 문제*를 **물리식 5-regime**(Tabor 소성 A=F/H, volume A=V/h_min, geom 하한)으로 풀고 **그 면적을 Holm 구속저항·coverage에 직접 투입**한다. ⇒ 우리 면적은 *전달-연결·물리식*, 그들 면적은 *압밀-국한·피팅*. (단 정직히: c_area의 *단순성*은 장점 — §8②의 비교연구 거리.)

3. **★ DEM↔MPM 커플링(scaffold) — 진짜 소성 SHAPE morphology 필드.**
   So 2022는 **rigid 구 + CONTACT 소성**(h_eq는 접촉점 함몰 proxy)이라 **입자 외형이 변하지 않는다** — 저자 스스로 "고변형서 입자 *형상이 변하며* 2차접촉 생기지만 구-겹침으론 안 잡힘"이라 인정하고 *인자로 패치*만 한다. 우리는 **MPM(von Mises J2, ν=0.49)로 *진짜* 소성 입자 SHAPE 흐름·void-fill·누적소성변형장 Σdg**를 풀고, **DEM AM scaffold + MPM SE 커플링**으로 압밀 porosity(15.93 %)·두께가 *EMERGE*하게 한다. ⇒ So가 "구-겹침이 깨진다"고 인정한 *바로 그 형상-morphology 절반*을 우리 MPM이 채운다(frame[5]).

4. **★ Fracture-aware 전달(Auerbach + Lawn → partial-Holm).**
   So 2022는 입자 *균열(fracture)을 모델하지 않는다*(구는 안 깨짐; So 2021도 "intraparticle cracking은 future work"). 우리는 **Auerbach 임계 + Lawn 미세균열 → fracture-aware Holm(f_intact, partial conduction)**으로 *깨진 접촉이 전달에 주는 영향*까지 σ 폼에 넣는다(AM_P 92:8 8mAh서 37–40% cracked, σ_e fracture-reduced). ⇒ 균열-전달 결합 = 그들에 없는 축.

5. **★ 문헌-grounded σ_grain(Cronau/Trevisanello/Wang) — 재료물성 1차 앵커.**
   So 2022는 *전달이 없으니* σ_grain도 없다(역학 H/E만). 우리 σ_ionic은 **Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) sub-µm GB 인자**, σ_e는 **Trevisanello endpoint(10/5) + NCM(r) GB**, σ_thermal은 Wang — *각 채널을 literature 물성에 고정*. ⇒ 전달 absolute가 문헌-anchored.

6. **★ 실험-앵커 *독립* 이중모델 보정 (frame[4]/[5]).**
   So 2022는 **Sakuda 실험 상대밀도 *한 종류*에 c_area·c_spring·h_ov^max 3개 인자를 피팅**(역학 단일모델). 우리는 **DEM(E=1.35 hooke/hysteresis+Stage-E)과 MPM(E=1.53 J2)을 *서로가 아니라 각각 실험(Minnmann)에* 독립 보정**하고 — 수렴(real_14 porosity 15.6↔16.7↔exp, coverage Tabor 48–52%)은 *교차검증*, 발산은 *정량화된 모델한계*로 읽는다(frame[4]). ⇒ *두 독립 물리엔진의 합의*가 우리 신뢰 척도(단일 피팅모델보다 강건).

7. **★ 솔버→스케일링법칙 압축(노이즈-천장 LOOCV) → ML 설계 예측기.**
   So 2022는 *접촉모델 → 상대밀도 곡선*에서 멈춘다(설계 역문제·ML 없음). 우리는 **네트워크 솔버 출력을 노이즈-천장 LOOCV 스케일링법칙으로 압축**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.90)하고 → **설계 knobs → 전 메트릭 예측 → 2D 미세구조 합성 → 층상 복합양극**의 5단계 파이프라인으로 간다. ⇒ *예측·역설계*가 우리 work 정체성, So는 *forward 역학*에서 종료.

**⚠ 정직히 — 그들이 우리보다 앞서는 것:**
- **소결(sintering) rate 모델(eq 7)** — **우리가 *전혀* 안 가진 물리.** consolidation+detachment dead-band의 융착결합 rate는 상온 압력소결(LPS/LPSCl 황화물 입계 융착)을 *역학적으로* 모델한다. 우리 `--coh`/adhesion은 *정적* 점착이지 *rate 융착·분리*가 아니다. → 소결은 So 계보가 명백히 앞선 칸(우리 흡수 후보).
- **점탄성(Maxwell) 명시 rate(eq 2–4, Fig 9)** — 우리는 *정상상태 소성*만(t_rel≪sim). Li 같은 strain-rate 민감 상이나 *시간의존 creep*을 다루려면 그들 점탄성 모드가 앞선다.
- **접촉모델 자체의 정교함**: rate-기반 h_eq + 항복캡 + 면적/스프링 인자 + over-compaction 캡을 *하나의 LAW*로 통합한 완성도는 우리 hooke/hysteresis(no-cap)보다 높다 — 그래서 *경로 A의 사양서*로 쓸 가치가 있는 것.
→ 즉 **역학 접촉모델의 *깊이*는 So가, 전달·morphology·예측의 *폭*은 우리가** 앞선다. 우리 state-of-the-art 주장은 "*ASSB 복합양극의 구조→전달 σ + 소성 morphology + 설계예측 통합 파이프라인*"에 한정해 *정확*하다.

## 10. 주의/한계 (over-claim 방지)
- **소재가 다르다**: SE = **LPS(Li₂S–P₂S₅, argyrodite 아님)**; AM = **NCM/LiCoO₂ 양극**(Table1 E=199·H=11.2 = Cheng LiCoO₂, So 2021의 Si 음극과 다름). σ_grain·E_CAM·H 모두 우리와 다름 → **절대 porosity·σ·면적 직접 전이 금지, 방법·추세만**. E_SE=24가 우리 real-bulk와 같은 건 우연(LPS도 sulfide).
- ⚠ **Table 1 라벨 오기**: E_AM 행이 "SE Young modulus (LPS)"로 적혔으나 값 199 GPa = LiCoO₂(Cheng [10]) → *AM은 양극*. 값은 신뢰, 라벨만 오타.
- **rigid sphere + CONTACT 소성**: 입자 형상 불변(h_eq는 접촉 함몰/융착 proxy). **진짜 void-fill SHAPE 흐름 없음** → 우리 MPM morphology 영역 못 다룸(frame[5] 역학 절반). 저자 스스로 "고변형서 spherical overlap 깨짐(2차접촉·형상변화)"을 인정하고 *인자로 패치*만.
- **전달 전무**: σ_ionic/e/thermal·percolation·tortuosity·coverage·coordination *어느 것도 없음*. 이건 *접촉모델 엔진* 논문 — 전달은 So의 *다른* 논문(2021 JPS τ-기반, 우리가 별도 digest)·우리 Kirchhoff/Holm 소유.
- **c_area·c_spring·h_ov^max 는 피팅값**: Sakuda 실험에 맞춘 *조정 파라미터*(2 / 5–7 / 0.6R_eff). 우리 mono-disperse LPSCl·Stage-E 물리식에 직접 대입 금지(소재·정의차).
- **저압 과치밀(과소porosity)**: 단순 DEM이 ~150 MPa 이하서 Sakuda보다 *치밀* — **응집체(aggregate)를 안 모델한 탓**(저자 명시). 우리 압밀 floor 논의와 *방향 반대*(우리는 강체-구가 *과다* porosity) → 비교 시 주의.
- **그림 읽은 값(digitized)은 추세만(±)**: 상대밀도·높이·E_electrode 곡선 수치는 Fig 6–9에서 읽은 근삿값. stated(Table 1/2 파라미터, c_area/c_spring/h_ov^max, E/H, 박스크기)와 구분.
- **단일 실현으로 보임**: seed 다중실현·통계 명시 없음(보정용).
- **MethodsX = 방법 부록**: 이 논문은 *접촉모델 유도*에 집중하고 *물리 결과·검증*은 동반 JPS(So 2022 JPS 530, 231279)·So 2021에 분산. 결과(porosity·σ) 수치 인용 시 *그 본문* 논문을 우선.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
