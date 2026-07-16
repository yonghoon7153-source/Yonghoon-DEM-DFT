<!-- digest 표준 양식. 복사해서 papers/<slug>.md 로. ★ = 사용자가 특히 원한 항목 -->
# 구형 입자의 기계적 패킹 — 크기비·다성분 최대 충전밀도의 고전 — McGeary (J. Am. Ceram. Soc. 1961)

> slug `mcgeary1961_bimodal_sphere_packing` · DOI `10.1111/j.1151-2916.1961.tb13716.x` · type `exp` · PDF `McGeary_1961_JAmCeramSoc_Mechanical_Packing_of_Spherical_Particles.pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
**진동 기계적 패킹**으로 단일크기 구 62.5% → 이성분 ~86% → 삼성분 90% → 사성분 95.1%(이론밀도)를 실험으로 보인,
**bimodal/multimodal 구 충전의 원전(原典)** — 핵심은 "조대-미세 구 직경비가 **≥ 약 7:1**이어야 미세입자가
조대입자 간극(삼각형 공극)을 통과해 효율적으로 채운다"는 **임계 크기비**다. 이것이 우리 **Furnas dip(AM+SE 12:4:1
크기비로 특정 조성에서 porosity가 더 낮아지는 기하 효과)의 직접적 기하 기반**이고, 소성 연속체 MPM이 재현 못 하는 바로 그
**rigid-sphere 기하**다(frame [4]).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| R. K. McGeary (Nuclear Materials and Equipment Corp., Apollo, PA — Plutonium Bearing Fuel Materials, AEC AT(30-1)-2389) | J. Am. Ceram. Soc. **44** [10] 513–522 (Oct 1961) | 10.1111/j.1151-2916.1961.tb13716.x | **해당 없음** — 금속 구 shot (강철/텅스텐/알루미늄)으로 한 **이상화 패킹 실험** (전해질·양극 무관) | 실험 (기계적 진동 패킹, 입체현미경 관찰) |

> 맥락: 우라늄 산화물 핵연료를 긴 금속관에 진동 충전하는 원자력 연구(1954~)에서 "최대 충전밀도 PSD"를 찾던 흐름의
> **첫 이상화·체계적 시도**. Furnas(1929–31), Westman & Hugill(1930)이 시작했다가 중단한 "크기비 패킹"을 잇는다고
> 본인이 §I에서 명시. → 우리 코드(de Larrard 기하, Furnas dip)의 **계보 뿌리** 논문.

## 3. 핵심 물성 (수치) — packing density / size-ratio (transport·DEM 없음)
> 이 논문은 전달물성(σ)·역학(E, σ_y)·DEM이 **전혀 없는** 순수 기하 패킹 실험이다. 아래 표는 §3 = **충전밀도 vs 크기비**로 적응함.
> "% of theoretical density" = 입자 물질의 결정밀도 대비 채워진 분율 = **(1 − porosity)** (저자 §II 각주: 소결과 달리 입자 내부 공극은 무시, 입자 사이 공극 제거가 끝점).

| 물성 | 값 | 조건 (성분·크기비) | stated/digitized | 비고 |
|---|---|---|---|---|
| **단일크기 패킹밀도** | **62.5 %** (= porosity 37.5 %) | 1-size, orthorhombic 배열, 큰 용기 | **stated** (Table II) | 재료·절대크기 무관(강철 7/20/60-mesh 모두 62.5; 텅스텐 59.5; Al 61.0) |
| **이성분 최대밀도** | **86.0 %** ("density limit for steel shot") | 조대=7-mesh, 미세는 400-mesh까지, d_c/d_f ≥ 7 | **stated** (Fig 5, §V) | porosity 14.0 %; 최적 조성 ~72.7 % coarse |
| **삼성분(ternary) 최대밀도** | **90.0 %** (이론한계 93.5의 96.5 %) | 7:60:400-mesh, 크기비 **77:7:1**, 조성 **67:23:10 vol%** | **stated** (§VI, Fig 6/7) | 0.124 / 0.011 / 0.0016 in. 직경 |
| **사성분(quaternary) 최대밀도** | **95.1 ± 0.3 %** (이론한계 97.5의 ~98 %) | 크기비 **1:7:38:316**, 조성 **6.1:10.2:23.0:60.7 vol%** | **stated** (abstract, Table IV) | "압축·고온소성 세라믹과 동등" — 단지 부어서(pour) 진동만 |
| **임계 크기비 (knee)** | **d_c/d_f ≈ 7** | 이성분 밀도-크기비 곡선의 무릎 | **stated** (§V, Fig 5) | 이하서 밀도 급감; **삼각형 공극 통과 조건** |
| 삼각형 공극 직경 | **0.154·d_c** | 동일크기 구 3개가 만드는 close-pack 공극 | **stated** (§V) | √(...): p_t = d(2/√3−1)=0.154 d_c; 정사각 공극 0.414 d_c > 삼각 |
| coordination Z | n/a | — | — | 배위수 직접 측정 없음 (배열 기하만; 4가지 1-size 배열 53.36/60.46/69.81/74.05 % 언급) |
| σ_ionic / σ_e / σ_thermal | **n/a** | — | — | 전달물성 전혀 없음 |
| E / σ_y / ν | **n/a** | — | — | "no plastic deformation of particles occurs" — **강체 구** 명시 (§I, §X) |
| Heckel P_y | **n/a** | — | — | 압축곡선·Heckel 없음 (진동 패킹, 압력 인가 아님) |
| 단일크기 4배열 이론밀도 | 53.36 / 60.46 / 69.81 / **74.05 %** | simple cubic / orthorhombic / double-nested / close-packed | **stated** (§III) | 실험은 orthorhombic(~62.5)가 지배; close-pack은 진동서 불안정 |

### 핵심 4개 데이터 포인트 (외워둘 값)
- **62.5 %** — 단일크기 (1-component) 진동 패킹 밀도
- **86.0 %** — 이성분 한계 (d_c/d_f ≥ 7)
- **90.0 %** — 삼성분 (77:7:1, 67:23:10)
- **95.1 %** — 사성분 (1:7:38:316, 6.1:10.2:23.0:60.7)
- **임계비 7:1** — 무릎; 미세입자가 조대 삼각공극을 통과하는 한계
- **"각 추가 성분의 밀도 이득은 직전 성분의 절반 미만"** (§X) — 수확체감

## 4. 시뮬레이션 방법 ★ (이 논문은 **실험** — 기계적 패킹 절차로 적응)
- **code / version**: **없음** (1961 — 컴퓨터 시뮬레이션 아님). 모든 "계산값"은 손기하(strict crystallography 기하 구성) + 경험식.
- **DEM 접촉법칙 / 재료 파라미터 / bond / MPM / 전달 솔버**: **전부 n/a** (실험 논문).
- **입자 처리** ★ (= 우리 관심 "무질서/입자 처리"의 실험판):
  - **완전 강체 구**(rigid sphere). 저자가 §I·§X에서 **"입자의 소성변형이 일어나지 않는다(no plastic deformation
    occurs)"**를 패킹의 정의로 명시 → 우리 DEM의 "eternal rigid sphere" 가정과 **물리적으로 동일한 이상화**.
    → 이 논문의 모든 밀도는 **순수 기하 패킹**(형상변화·δ-overlap 없음)이다.
  - **mono → bi → ternary → quaternary PSD**: 각 성분은 "단일 mesh"(좁은 분포)로 분리. 13개 단일-mesh 성분
    (Table I, d 0.124 in.~<0.0016 in., ~77배 범위)을 조합. → 우리 12:4:1 이산 다분산과 동형.
  - **소성 없음을 실험으로 검증**: §X — 진공/하중(1~16 lb/in²) 변화가 최종밀도에 영향 없음 = "딱딱한 구는
    재배열만으로 채워지고, 형상흐름(plastic flow)은 없다"를 직접 확인. → **우리 MPM의 void-fill 소성흐름과
    정반대 극(極)**: McGeary = 순수 기하 상한, MPM = 소성으로 그 아래로 뚫는 메커니즘.
- **패킹 절차(= "방법")**:
  - **축방향 진동**(axial vibration, ~사인파). 전자식 가진기(10-lb force) + 공압 피스톤 비교. 빈도/가속도/지속시간이
    레버. 최적 ~**250 cps** (텅스텐), 가속 5~10 g, 하중 ~1 lb/in²면 충분.
  - **투명 용기 + 저배율 입체현미경**으로 **배열을 눈으로** 관찰(이 논문의 신규성). 원통관(D/d 1:1~200:1).
  - **이성분 순차충전**(중요): 조대 성분을 먼저 진동→최소부피, 진동 정지, 미세 성분을 부어 넣고 다시 진동→최소부피.
    조대층을 "고정 다공 필터"로 보고 미세입자가 **여과(filter through)**되어 들어가게 함. (혼합-후-진동은 분리/저밀도 →
    실패; §V.) → 우리 scaffold(AM 고정 + SE 채움)의 **실험적 원형**.
- **도메인/seeds**: 100-ml graduate / 3/8·1/2·1·1½·2 in. 관. 사성분 2회 반복서 **95.1 ± 0.3 %** 재현(σ≈0.3 %p).
- **특이사항**: 진공(73–74 cm Hg)은 도움 안 됨(§VIII — 공기역학 교란만); 용기 재질(유리/플라스틱) 무영향(§X);
  **재료(강철/W/Al)·절대크기 무관, 크기비만 지배**(Fig 5 결론).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 관 속 구 배열 3종 모식(orthorhombic / double-nested / close-packed) + 정면·측면 | 진동 시 close-pack은 무너지고 **orthorhombic(~62.5 %)**가 안정 — 강체 구 단일크기 상한의 기하 |
| **2** | 용기직경/구직경(D/d) vs 단일크기 패킹효율 (1~200) | 벽효과: D/d ≳ 10에서 62.5 %로 수렴; **D/d=3,4서 역밀도(dip)** — 우리 RVE 박스팩터 수렴(35)과 동류 |
| **3** | **이성분 밀도 vs %조대구**, 7-mesh + 6가지 미세크기 (역삼각 다이어그램) | ★ **Furnas dip의 원형 그림**: 미세가 작을수록 곡선이 위로(밀도↑), 피크는 ~73 % 조대 부근. 20-mesh는 종(bell)형(미세가 안 통과) |
| **4** | 이성분, 조대 + 400-mesh 텅스텐 (77.5배 차이) | 극한 크기차 → **84.7 %** 한계(86.0보다 낮음, 최적 74.0 % 조대) — 절대크기 무관·크기비 지배의 보강 |
| **5** | ★★ **최대밀도 vs d_c/d_f (크기비)** — 모든 이성분 곡선 중첩 | ★★ **이 논문의 심장**: 무릎 **d_c/d_f≈7**, 이하 급감, 이상 86.0 % 평탄. **삼각공극 직경**이 무릎 위치 결정. = 우리 dip의 임계비 |
| **6** | (A) 조대코너 등밀도선 + (B) 삼성분 농도삼각형 (77:7:1) | 삼성분 최대 90.0 %@67:23:10; 다성분 최적조성 기하 — 우리 다성분 조성스윕 설계 참조 |
| **7** | 삼성분 패킹 실사진(×11): 7+60+400-mesh, 90.0 % | 조대 주위 rhombic + 미세가 쐐기공극 채운 "bull's-eye"; **구멍 거의 없음** = 고밀도 다분산 충전의 모습 |
| **8/9/10/11/13** | 미세성분 진입속도 vs 빈도·가속·재료(W vs Al) + 패킹 형성 사진 | **충전 동역학**(rate): ~250 cps 최적, 무거운 W가 Al보다 빠름. 우리 정적 결과엔 직접 안 쓰나 "진동=재배열 메커니즘" 근거 |
| **12** | 진공 vs 미세진입 | 진공은 **도움 안 됨**(공기 교란) — 패킹은 순수 역학 재배열임을 확인 |

## 6. Post-processing ★
- **무엇**:
  - **% 이론밀도 측정** = 비중계(pycnometric) 측정밀도 / 입자 물질 결정밀도. **porosity = 1 − (%th/100)**.
    (우리 ε_sphere/ε_union 컨벤션과 비교: McGeary는 **입자 사이 공극만** — 강체라 입자 내부 공극 0 → 우리 union/sphere 구분이 무의미한 순수 기하 상한.)
  - **다성분 한계밀도 경험식** (eq 3): `%th = 100·[1 − vₙ·Xₙ/(vₙ·Xₙ + V)]`,
    vₙ = 최미세 성분의 공극 부피분율, Xₙ = 최미세 성분 부피분율, V = 고체부피 상수. → 삼/사성분 "이론한계" 예측에 사용.
  - **단일층 구수 경험식** (eq 1): `S = 4(r+1) + (13/2)Σr` (S = 층당 구 수, r = 링 수); (eq 2) 총 구수 M.
  - **삼각공극 기하**: p_t = d(2/√3 − 1) = 0.154 d_c → 임계 크기비 7:1 유도.
- **도구**: 비중계, 체질(sieving) 부피측정, 입체현미경 육안 관찰, **16-mm 현미경 동영상**(진동 중 패킹 관찰), 손기하 구성.
- **수치화·플롯**: 역삼각 좌표(Fig 3/4: %조대 vs 밀도/부피), 농도삼각형(Fig 6B), 크기비 단일곡선으로 모든 이성분 데이터 collapse(Fig 5) — **"크기비가 지배변수"를 시각적으로 증명**.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (McGeary 1961) | 우리 | 차이 / 이유 (rigid·plastic / 재료 / 2D·3D / 기하·연속체) |
|---|---|---|---|
| **입자 모델** | **강체 구**, 순수 기하 재배열, **소성 0** (실험 확인) | DEM = 강체 구 + hooke/hysteresis CONTACT(δ 프록시), 18× 연화 | **거의 같음**: 둘 다 형상 안 변함. McGeary는 그 **순수 기하 상한**을 실험으로 못박음 → 우리 DEM의 강체 가정의 **실험 정당화** |
| **단일크기 floor** | **62.5 %**(porosity 37.5 %), orthorhombic | 강체 구 porosity floor ~**20 %**(우리 3D, 진동+연화 overlap) | 우리가 더 치밀 = (i) 3D 진동+초기패킹 ~75 %, (ii) **연화 overlap**이 McGeary 순수기하 위로 채움. McGeary 37.5 %는 **overlap 없는 순수 기하** 극한 |
| **이성분 최대** | **86.0 %**(porosity 14 %), d_c/d_f≥7 | composite real_14 porosity **15.6 %**(DEM)/16.7 %(MPM) @300 MPa | 같은 자릿수(14 vs 15.6 %p porosity). McGeary는 **무압·진동**, 우리는 **300 MPa+소성**. → 둘이 비슷 = 우리 composite가 거의 **기하 패킹 상한**에 가까움 |
| **임계 크기비** | **d_c/d_f ≈ 7** (삼각공극 통과) | AM:SE 크기비 **12:4:1** (≈3:1 인접, 12:1 양극단) | ★ 우리 12:1(조대AM_P:미세SE)은 **McGeary 7:1을 넘김** → SE가 AM 간극을 채울 수 있는 영역 = **Furnas dip이 발생하는 기하 조건 충족**. 우리 4(AM_S):1(SE)≈4:1도 ≥... 경계 부근 |
| **Furnas dip** | **Fig 3/5가 dip의 원전**: 크기비↑→ 특정 조성서 밀도 피크(porosity 최저) | DEM/de Larrard: AM 70–85 wt%서 dip; **소성 MPM은 재현 못 함** | ★★ **dip = McGeary 기하 그 자체**. 우리 결론 "dip은 rigid-sphere 기하 현상, 소성 연속체 MPM 불가(frame[4])"의 **1961년 실험 근거** |
| **다성분 한계** | 삼성분 90 %, 사성분 95.1 % (성분↑→밀도↑, 체감) | 우리 corpus는 본질상 이성분(AM+SE)+AM 이봉(P/S) ≈ 삼성분 | McGeary는 우리가 못 가본 **사성분 95 %**까지 → "성분 더 넣으면 더 치밀"의 상한 지도. 우리 12:4:1 이봉AM = 사실상 삼성분 패킹 |
| **전달 σ** | **없음** | σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903 (LOOCV) | McGeary는 **기하만**(우리 DEM 전달 영역 전무) — 순수 packing reference |
| **소성 흐름** | **명시적으로 없음**(§X 실험 확인) | MPM = 진짜 소성 void-fill (porosity를 기하 floor **아래로**) | ★ McGeary = 소성 **없는** 상한 / MPM = 소성으로 그 **아래** 뚫음. **frame[5] 분업의 양 끝**을 한 쌍으로 정의 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **Furnas dip의 1차 문헌 근거 확보**: 우리가 "dip은 기하(de Larrard)이고 소성 MPM은 재현 못 한다(frame[4])"고
  주장할 때, **McGeary 1961 Fig 3/5(크기비↑→밀도피크, 무릎 7:1)**가 그 **실험 원전**. dip은 1961년부터 알려진
  **강체-구 기하 보편현상**임을 인용 → 우리 DEM-vs-MPM 분업 주장의 신뢰도 강화.
- ② **임계 크기비 7:1로 우리 12:4:1을 정량 점검**: 우리 AM_P:SE = 12:1 (≫7, dip 가능), AM_S:SE = 4:1 (<7 — 무릎 아래,
  부분 충전). → **dip의 깊이가 조성에 따라 변하는 이유**(AM_P-rich서 깊고 AM_S-rich서 얕음)를 McGeary 무릎으로 설명 가능.
  우리 porosity 관계식에 **크기비 항**을 넣을 근거(Varkey의 E-stiffness 항과 별개의 **기하 항**).
- ③ **composite porosity 상한 = ~14 % (기하)**: McGeary 이성분 86 %(porosity 14 %)는 우리 real_14 15.6 %와 거의 일치
  → 우리 composite가 이미 **기하 패킹 상한 근처**에 있고, 그 이하(소성 void-fill)는 **MPM이 −8~10 %p 더** 줄이는 영역임을
  깔끔히 분리(MPM se-dump 27.6 % vs rigid 36 %p의 의미가 McGeary 상한 위에서 해석됨).
- ④ **사성분 95 % = 미래 다층 양극의 상한 지도**: 우리 Phase 5(layered composite)에서 **PSD를 더 다분산화하면**
  McGeary처럼 95 %까지 가능 — 단 "각 성분 이득 체감"·"성분간 크기차 충분해야"라는 McGeary 경고가 설계 제약.

## 9. 인용 가능 문장 (deck/paper용)
- "The geometric basis of the porosity-vs-composition dip is the classical McGeary (1961) result: rigid
  spheres pack to 62.5 % (one-size), ~86 % (binary, coarse/fine diameter ratio ≥ 7), 90 % (ternary,
  77:7:1) and 95.1 % (quaternary, 1:7:38:316) of theoretical density, with the critical ratio d_c/d_f ≈ 7
  set by the triangular interstitial-pore diameter (0.154·d_c)."
- "Because McGeary's densification is purely geometric — no particle plastic deformation occurs — the
  packing dip is a rigid-sphere phenomenon, which our discrete DEM (and de Larrard geometry) reproduce
  but the plastic continuum MPM cannot, irrespective of solid-electrolyte calibration."

## 10. 주의/한계 (over-claim 방지)
- **소재 전이 불가(절대값)**: 금속 shot(강철 ρ7.52 / W 19.30 / Al 2.70 g/cm³)이지 LPSCl·NMC811이 **아니다**.
  **밀도·porosity·크기비의 기하 추세만** 전이 가능, σ·E·압밀압력 절대값은 **무관**. 우리 자료엔 "% theoretical density =
  기하 packing" 의미로만 인용.
- **강체·무압 진동**: 우리 300 MPa 냉간압축과 **메커니즘이 다름**(McGeary = 진동 재배열, 소성 0). 따라서 우리 composite
  15.6 %가 McGeary 14 %와 비슷한 건 "둘 다 기하 상한 근처"라는 **정성 일치**이지, 동일 공정 절대비교가 아니다.
- **3D·이상화**: 단일-mesh(좁은 분포) 구만 — 실제 연속 PSD·비구형(우리도 비구형은 못 하지만)·바인더·계면 없음. de Larrard가
  연속 PSD로 확장한 버전이 우리 dip 모델에 더 가깝다.
- **digitized 없음**: 본 digest의 모든 수치는 **본문/Table 1–4의 stated 값** (Fig 5/3에서 따로 읽은 값 없음). 단,
  86.0/84.7/90.0/95.1 %, 7:1, 0.154 d_c, 조성 비율은 전부 텍스트·표 명시값.
- **dip 깊이·위치의 절대값**: McGeary는 "최대밀도 vs 크기비"는 정량적이나, **특정 조성에서의 dip 깊이**는 우리 LPSCl 12:4:1·
  300 MPa 조건에 그대로 옮길 수 없음 — 크기비·조성 **추세**(어디서 피크가 나는지)만 가이드.
- **Z·percolation·전달 없음**: 배위수·삼투·전도도는 이 논문에 전무 → 우리 DEM 전달망 검증엔 **기하 패킹 상한만** 기여.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
