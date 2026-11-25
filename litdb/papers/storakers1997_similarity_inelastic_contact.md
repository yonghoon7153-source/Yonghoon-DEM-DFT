# 비탄성 접촉의 자기상사(similarity) 해석 — Storåkers, Biwa & Larsson (Int. J. Solids Struct. 1997)

> slug `storakers1997_similarity_inelastic_contact` · DOI `10.1016/S0020-7683(96)00176-X` · type `continuum (self-similar inelastic single/pair contact theory)` · PDF `Storakers_1997_IJSS_SimilarityAnalysis_InelasticContact.pdf` · digested `2026-06-26` · status ✅
>
> ★ WISHLIST Tier-0 #6 — **자기상사 비탄성 접촉의 엄밀 이론**. 우리에게 결정적인 이유: (1) **Martin–Bouvard 2003**(이미 digest)가 그들 DEM 복합 압밀의 소성 접촉면적으로 **이 논문의 법칙 `A = 2π·c²(m)·r·h`를 그대로 사용**한다 → 이 digest가 그 DEM 접촉모델의 **원천 이론**이다. (2) 우리 **Stage-E(Tabor+volume) 소성 접촉면적**은 경험적 재유도이고, Storåkers의 `c²(m)·r·h`가 그 **엄밀 자기상사 물리판** → **A/B 비교(우리 Stage-E 경험식 vs Storåkers 물리식)의 기준**이다. (3) **c²(m)** = 진짜 접촉면적 / 기하 overlap 면적 비, **0.5(선형/강경화) → 1.43–1.45(이상소성, pile-up)** — 우리 ε_sphere "displaced material re-emerges as a bulge"(소성 시 변위된 물질이 bulge로 재돌출) 가정의 정확한 물리 인자.

---

## 1. 한 줄 요약
멱법칙(변형률경화) 소성·점소성·비선형탄성을 **균질함수(homogeneous function)** 로 모델링하면 접촉/압입 문제가
**자기상사(self-similar)** 가 되어, 움직이는 접촉경계를 갖는 시간·이력 의존 문제가 **고정된 flat-die(평면 펀치)
문제 + 누적 중첩(cumulative superposition)** 으로 환원된다는 것을 일반적으로 증명하고, 그 환원으로
**구형 압입의 보편 경도식**과 **진짜 접촉면적↔기하 overlap을 잇는 자기상사 상수 c²(m,n)**(이상소성 pile-up
1.43–1.45 → 강경화 sink-in 0.5)를 닫힌형/수치로 도출한 **비탄성 단접촉·이체접촉 역학의 정전(canonical
reference)**. 분말 압밀의 소성 접촉법칙(Martin–Bouvard DEM, 우리 Stage-E)이 바로 이 이론에서 나온다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **B. Storåkers, S. Biwa†, P.-L. Larsson** (Dept. of Solid Mechanics, Royal Institute of Technology **KTH**, S-100 44 Stockholm, Sweden; †현 Kyoto Univ.) | **Int. J. Solids Struct. 34(24) 3061–3083 (1997)**, 접수 1996-04-23 / 개정 1996-08-07 | 10.1016/S0020-7683(96)00176-X | **소재 무관** — 일반 비탄성 고체(멱법칙 점소성/변형률경화 소성). 동기 = 표면거칠기 평탄화·**분말 압밀**·압입(Brinell/Berkovich/Vickers) 경도시험 | 연속체 자기상사 이론 + FEM(13,882 DOF) — 단접촉(반공간 압입) + 이체(두 변형체 상호압입) |

> 응용 동기로 **(c) compaction = 분말 입자 압밀**(Fig 1c)을 명시. 후속 동저자 **Storåkers (1996)** "Local contact behaviour of viscoplastic particles" (IUTAM, Mech. Granular & Porous Materials)가 이 이론을 **복합분말 압밀**에 명시 적용했고, 그것이 **Martin–Bouvard 2003 DEM**의 접촉법칙 출처. 즉 이 1997 논문 → Storåkers 1996 IUTAM → Martin–Bouvard 2003 DEM 의 **이론 계보의 뿌리**.

> ⚠ **순수 연속체 단/이체 접촉 구성식 이론**이다 — 패킹·다체·전달(σ) **전무**. frame[5] 기준 **per-contact 면적/하중 법칙**으로만 사용(패킹·dip·transport 도구 아님). 모든 결과는 **무차원**(σ₀ 정규화) → LPSCl 절대값 없음, 가져올 것은 **면적-overlap 인자 c²(m)·경도식·자기상사 구조**.

## 3. 핵심 물성 (수치)
> 무차원 이론이라 "물성" = 자기상사 상수·경도 인자·면적↔overlap 비. digitized = Fig 5에서 읽음(추세만).

| 양 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **c²(이상소성)** | **≈ 1.43** (본문/Fig5 원점) ; **1.45**(Martin–Bouvard 인용) | 1/m+1/n→0 (m,n→∞) | stated | **pile-up 최대**; 진짜 접촉면적이 기하 overlap의 ~1.43배 |
| **c² 천이(=1)** | **c²=1 at 1/m+1/n ≈ 1/3** | sink-in↔pile-up 경계 | stated | ~m=3 어닐드 금속(Norbury–Samuel 1928 잔류압흔 표면 아래) |
| **c²(선형/강경화)** | **≈ 0.5** | 1/m+1/n→1 (m=n=1) | stated 끝점 | **sink-in**; 접촉면적이 overlap의 절반 |
| 접촉면적 법칙 | **A = 2π·c²(m)·r·h** | 구-구 소성접촉 | stated(=M-B eq8) | r=결합반경, h=overlap(겹침). **Martin–Bouvard가 그대로 사용** |
| 구형 압입 프로파일 | **u₃ = h·[1 − c²·(r/a)²]** (eq74) | sphere p=2 | stated | c²>1 pile-up(접촉테 위로 솟음), c²<1 sink-in |
| **Tabor 경도상수** | **α = 2.8, β_m = 0.4** | 변형률경화 경도식(eq78) | stated(Tabor 1951 채택) | H≈2.8σ₀ ; 대표변형 ~0.4(a/D) "Tabor strain" |
| 보편 경도식 | **L/πa² = [3(n+2)/n]·σ₀·(a/3D)^(1/m)·(ȧ/3D)^(1/n)** (eq78) | sphere | stated | α=2.8,β_m=0.4 대입 |
| 점성(뉴턴유체) 극한 | h(a)=2a²/D (eq69), a∝t^(1/3)(eq72) | m→∞,n=1,σ₀=3μ | stated | 자기상사 점성 압입(해석 검증) |
| 구성식 | **σ_e = σ₀·ε̇_e^(1/n)·ε_e^(1/m)** (eq6) | 일반 점소성 | stated | m=∞ 변형률경화 소성, n=∞ 비선형 점성/크리프 |
| FEM | **13,882 DOF**, rim 특이점(HRR crack-tip) 해상 | reduced flat-die | stated | Biwa–Storåkers 1995 메시 |
| porosity / Heckel / PSD | **n/a** | — | — | 패킹·압밀곡선·PSD 전혀 없음(순수 단접촉 구성식) |

## 4. 시뮬레이션 방법 ★
- **code / version**: 자체 **FEM** (Biwa–Storåkers 1995 설계 메시, **13,882 DOF**). reduced flat-die(평면 펀치)
  문제를 풀고 **누적 중첩**으로 원래 곡면 압입 복원. 상용코드 아님(ABAQUS는 비교용 인용만).
- **구성식 (이 논문의 핵심)** ★ — **균질함수 점소성**:
  - 두 점소성 포텐셜 Φ(σ_ij), Ψ(ε̇_ij): `ε̇_ij=∂Φ/∂σ_ij`, `σ_ij=∂Ψ/∂ε̇_ij` (eq1), Legendre 쌍대 `𝒟=σ_ij·ε̇_ij=Φ+Ψ`(eq2).
  - Φ가 차수 (n+1) 동차 → Ψ는 차수 (n+1)/n 동차(쌍대성). 누적변형 `ε_e=∫ε̇_e dt`(eq3, 경로의존)를 passive 파라미터로 두면
    `Φ=σ₀/(n+1)·(σ_e/σ₀)^(n+1)·ε_e^(−n/m)` (eq4), `Ψ=σ₀·n/(n+1)·(ε̇_e)^(n+1)/n·ε_e^(1/m)` (eq5),
    연결관계 **`σ_e = σ₀·ε̇_e^(1/n)·ε_e^(1/m)`** (eq6) — m=변형률경화, n=율민감/크리프 지수.
  - 비등방 `σ_e=(β_ijkl σ_ij σ_kl)^(1/2)`(eq9), 비압축·등방 시 **von Mises** `σ_e=(3/2 s_ij s_ij)^(1/2)`(eq14)로 환원.
- **자기상사 환원(reduced flat-die)** ★ — 이 논문이 파는 핵심 기교:
  - 접촉윤곽 `r=a·C̃(θ), C̃(0)=1`(eq24)이 **시간에 무관·공간적 자기상사 팽창**. a priori 스케일 `xᵢ=a·x̃ᵢ`,
    `u̇ᵢ=ḣ·ũᵢ`, `ε̇_ij=(ḣ/a)·ε̃_ij`(eq25–27) → 비등차 BC `ũ₃=1, x̃₃=0`(eq28) = **flat-die 압입과 형식 동일**.
  - 변위 BC 적분(eq29–30) → **분리(separable) 결과** `h(a)=F(θ)/c^p(θ)·a^p/D^(p−1)`(eq31), 고유함수 c^p(θ)(eq32).
    → "움직이는 접촉경계+시간/이력 의존" 문제가 **고정 flat-die + 반경 a에 대한 누적 중첩**(eq40–42, radial ray 적분)으로 환원.
  - **이게 자기상사의 효용**: 재료 이력(시간)을 **공간 비국소성(nonlocality)** 으로 치환 → 한 번의 flat-die 해 + 중첩으로 임의 압입깊이/율의 해 생성.
- **재료 파라미터**: 무차원 (σ₀, m, n, p). p=압입자 프로파일 동차차수: **p=1 콘/Vickers/Berkovich, p=2 구(곡률 2/D)**.
  m,n 스윕(이상소성 m,n→∞ ~ 선형 m=n=1). 수렴이 m에 민감 → m=1부터 parameter-tracking.
- **bond/binder / MPM / 전달 솔버**: **전부 없음**. 순수 역학 단/이체 접촉.
- **입자 처리** ★ (DEM "무질서 처리"의 연속체 원형):
  - **구를 진짜 형상소성으로 변형**(FEM이 자기상사 변형장을 직접 해석) — pile-up/sink-in을 c²로 정량.
    즉 **(3) SHAPE 소성** 층위(우리 MPM과 같은 부류), DEM의 δ-overlap 프록시가 **아니다**.
  - 단 — **단일 접촉**(반공간 1개 또는 두 변형체 1쌍). 패킹·다체 없음(이체 확장 §5는 두 곡면의 국소접촉까지만).
  - PSD 개념 없음(곡률 D, 결합곡률 eq84로 흡수). 두 물성 결합은 강도 σ₀(eq82)·곡률 D(eq84)·지수 m,n 공유로.
- **도메인 / mesh / 압력범위**: reduced flat-die FEM, ρ/a≤50(또는 1/m+1/n≤0.25면 10) remote boundary,
  rim 특이점(HRR crack-tip형, Hutchinson 1968)을 정밀 메시로 해상. 압밀 정의역 개념 없음(임의 압입깊이 자기상사).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 접촉 응용 3종: (a) **압입**(Berkovich) (b) **거칠기 평탄화**(flattening of asperities) (c) **압밀**(compaction, 구 패킹 + p,q 응력) | (c) = 우리 분말 압밀의 출발 그림. 이 이론이 압밀용으로 의도됨을 명시 |
| **2** | 곡면 강체 압입자 ↔ 변형 반공간 기하: 프로파일 x₃=f(x₁,x₂), 접촉반경 a, 깊이 h, 윤곽 r=C(θ) | 우리 접촉 overlap–접촉반경의 정의 그림(단접촉) |
| **3** | (Fig 3 = 식 전개; 본문엔 Fig 3로 구형 Brinell + flat-die Boussinesq 모식이 §4.2에 등장) | 구형 압입의 reduced 문제 = flat 원형 펀치 |
| **(p3075 좌)** | reduced flat-die **FEM 메시** ρ/a≤50, rim(ρ/a≤2) 상세 | rim 특이점 해상 = 우리 MPM grid 수렴 논의와 평행 |
| **5** ★ | **c²−1 vs (1/m+1/n)** — 일반 점소성(○ m=n, ▽ m>n, △ m<n) + 소성흐름(Biwa–Storåkers 1995) + 크리프(Storåkers–Larsson 1994) + 변형이론(Hill 1989, 점선) | ★★ **핵심 그림**: c²(이상소성 1.43 → 선형 0.5), **1/m+1/n≈1/3에서 sink-in↔pile-up 천이**. 우리 Stage-E 면적의 pile-up 인자 출처 |
| **6** | 변형 표면형상 u₃/h vs r/a (1/m+1/n=1, 1/3, 1/10) | pile-up이 큰 지수(이상소성)서 접촉테(r/a=1)에 **솟음**; sink-in은 가라앉음. c²의 형상 의미 |
| **7** | **reduced 평균압 ln L̃ vs (1/m+1/n)** + (n+2)/n 스케일 인자 적용 시 단일 직선 | 경도가 결합지수만의 함수. Tabor α=2.8 적합(eq77) |
| **8** | **정규화 접촉압분포 p(r)/p(0) vs r/a** (1/m+1/n=1,1/3,1/10) | 이상소성서 rim 발산(p∝rim), 강경화서 중앙集中. 우리 Holm 구속저항의 압력분포 배경 |

## 6. Post-processing ★
- **무엇**:
  - **c²(m,n) 추출**: reduced flat-die 해(점소성, FEM)에서 고유함수 c^p(θ)(eq32) 계산 → 누적 중첩(eq31)으로
    압입깊이 h ↔ 접촉반경 a 분리관계 도출 → 프로파일 eq74 `u₃=h(1−c²(r/a)²)`에서 c² 읽음. p=2, C̃=F=1로 axisym 환원.
  - **평균압(경도)** `L/A = σ₀·α(m,n)·[β_m(a/D)^(p−1)]^(1/m)·[β_n(ȧ/D)(a/D)^(p−2)]^(1/n)`(eq46) — α,β_m,β_n은
    **m,n,p만의 함수**(압입 크기 무관). reduced 평균압 L̃를 (n+2)/n로 스케일(eq76)해 단일곡선화(Fig7).
  - **접촉면적** A=a²·∫₀^2π C̃²(θ)/2 dθ (eq44), axisym이면 A=πa².
- **도구**: 자체 FEM(Biwa–Storåkers 메시) + 자기상사 해석. radial-ray 적분(eq40)으로 누적변형 산정.
- **수치화·플롯·기록**: 모든 응력 **σ₀ 정규화**, 결합지수 **1/m+1/n** 단일 가로축으로 c²·L̃·압력분포를 collapse.
  Tabor 1951 경험상수(α=2.8, β_m=0.4)를 **이론 정수로 채택**해 보편 경도식 eq78 제시.

## 7. 핵심 물리: 자기상사가 무엇을 사주나 (이 논문의 뼈대)

**문제**: 비탄성 접촉은 (i) 소성/점성 비선형, (ii) **움직이는 접촉경계**, (iii) 마찰, (iv) **이력의존**(시간을
따라 증분 추적 필요)으로 해석적으로 매우 난해(intractable). brute-force FEM은 움직이는 경계 + 자연시간을 동시
다뤄야 함.

**Storåkers의 답 = 자기상사 환원**: 재료 거동(σ_e=σ₀ε̇^(1/n)ε^(1/m))과 압입자 프로파일(f(αx)=α^p f(x), eq15)이
**동차함수**이면 접촉 문제가 **자기상사** — 접촉윤곽이 시간불변·자기상사 팽창(eq24). 그러면:
1. **움직이는 경계 → 고정 경계**: 속도장 스케일(eq25–28)로 reduced 문제가 **flat-die(평면 펀치) 압입**과 형식 동일.
2. **시간/이력의존 → 공간 비국소성**: 누적변형 적분(eq3, eq40)이 radial ray를 따른 공간 비국소 항으로 들어옴.
3. **임의 압입 → 한 번의 해 + 중첩**: flat-die 해를 **누적 중첩**(eq41–42)하면 임의 압입깊이·율의 해가 나옴.
4. **분리성**: 압입깊이 h와 기준반경 a가 **분리**(eq31) → 경도(평균압)가 a/D, ȧ/D의 멱법칙으로 깔끔하게 표현(eq46).

**왜 우리에게 중요한가**: 이 환원의 부산물이 두 가지 — (A) **접촉면적↔overlap의 자기상사 상수 c²(m,n)**(아래),
(B) **보편 경도식**(H≈2.8σ₀, eq78). 둘 다 분말 압밀 DEM의 접촉법칙으로 직접 흘러들어간다.

### 7.1 ★★ 자기상사 상수 c²(m,n) — pile-up/sink-in (우리 Stage-E의 심장)
구형(p=2) 압입 변형 프로파일은 **u₃ = h·[1 − c²·(r/a)²]** (eq74). 접촉테(r=a)에서:
- **c² > 1 → piling-up**: 변위된 물질이 접촉테 위로 **솟아오름**(bulge). 진짜 접촉면적 > 기하 overlap.
- **c² < 1 → sinking-in**: 표면이 가라앉음. 진짜 접촉면적 < 기하 overlap.
- **c² = 1 → 천이**: 접촉테가 원래 표면 높이 (잔류압흔 = 표면).

**c²(m,n) 값 (Fig5, 결합지수 1/m+1/n)**:
| 1/m+1/n | c² | 거동 |
|---|---|---|
| → 0 (이상소성 m,n→∞) | **≈ 1.43** (M-B 인용 1.45) | **최대 pile-up** |
| ~0.27 | ~1.10 | pile-up |
| **≈ 1/3** | **= 1.00** | **sink-in↔pile-up 천이** (~m=3 어닐드 금속) |
| ~0.6 | ~0.70 | sink-in |
| → 1 (선형 m=n=1) | **≈ 0.5** | **최대 sink-in** |

**Biwa–Storåkers 1995의 핵심 발견**: `c²(m)=c²(n)` (소성흐름 ↔ 크리프 결과가 매우 근접) → **모든 경우가
1/m+1/n 단일함수로 collapse**(Fig5). 즉 변형률경화 소성이든 멱법칙 크리프든 같은 c²(1/m+1/n).
물리적 관찰: **어닐드 금속(m≈3)은 잔류압흔이 표면 아래(sink-in)**, **냉간가공재는 pile-up**(Norbury–Samuel 1928)
— c²=1 천이가 m≈3(1/m+1/n≈1/3)에 오는 것과 정합.

**접촉면적 법칙**: `A = 2π·c²(m)·r·h`. 이게 **Martin–Bouvard 2003 eq8**과 정확히 같은 식(r=결합반경, h=overlap).
이상소성 c²≈1.43이면 A는 기하 overlap 면적(πa²≈2πrh의 절반 스케일)의 약 1.43배 — **pile-up이 면적을 키운다**.

### 7.2 ★★ 보편 경도식 — H ≈ 2.8 σ₀ (Tabor)
일반 경도식(eq46)을 구(p=2)로 환원(eq75) 후, Storåkers는 **Tabor 1951 경험상수 α=2.8, β_m=0.4**를 이론 정수로
**채택**하여 보편 경도식 **L/πa² = [3(n+2)/n]·σ₀·(a/3D)^(1/m)·(ȧ/3D)^(1/n)** (eq78)을 제시.
- α=2.8 = **경도계수 H≈2.8σ₀**(이상소성 plateau). β_m=0.4 = **대표변형(Tabor strain) ~0.4·a/D**.
- 이상소성(m,n→∞)에서 L̃ 값들이 일치, m=n=1(선형)에서 factor 3 차이(선형탄성 한계). reduced 평균압을
  (n+2)/n로 스케일(eq76)하면 1/m+1/n<0.5에서 단일 직선 적합(eq77: α=3, β_m=(n/(n+2))^n, β_n=1/3).

→ **이게 Mesarović–Fleck 2000의 완전소성 plateau p_m≈H≈2.8–3σ_y와 같은 숫자**다(§7.3 교차참조). 한쪽은
자기상사 **해석**(Storåkers, c²·H), 다른 쪽은 dissimilar EP **FEM**(MFleck, 영역 천이) — 둘이 H≈2.8–3σ₀,
면적 인자 ~1.4에서 **독립 일치**.

### 7.3 이체(dissimilar) 확장 (§5) — 두 변형체 상호압입
두 물체가 **m,n,p를 공유**하면(단, 한쪽이 평면 p→∞인 경우 제외) 이체 접촉도 자기상사로 환원:
- 응력장 `σ_ij^(k)=σ_ij^(0)`(eq79, 반공간 기본해 공유), 변위 `u_i^(k)=(σ₀/σ_k)^q·u_i^(0)`(eq80), `1/q=1/m+1/n`.
- **결합강도** `1/σ₀^q = 1/σ₁^q + 1/σ₂^q`(eq82, series형), **결합곡률** `F(θ)/D^(p−1)=F⁽¹⁾/D₁^(p−1)+F⁽²⁾/D₂^(p−1)`(eq84).
- 국소·매끄러운 접촉이면 **볼록성 제약 없음**. → 임의 강성·크기의 두 구 상호압입이 반공간 기본해로 환원.
- **명시**: "spheres of different rigidities and sizes related to **composite compaction** problems have recently
  been investigated by **Storåkers (1996)**" — 즉 이 이체 확장이 **복합분말 압밀**(우리 AM+SE, Martin–Bouvard
  hard+soft)의 직접 이론 기반.

### 7.4 해석 검증: 뉴턴유체 타원체 압입 (§4.1)
m→∞, n=1, σ₀=3μ(전단점도)이면 점성 반공간. 타원체 압입 → **접촉윤곽이 정확히 타원**(이심률 e from eq60),
중앙압 eq63, 일정하중 하 **a∝t^(1/3)**(eq72). 비자명 3D 해석해로 자기상사 절차(eq32,33,46)를 검증.

## 8. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> ★ 본 논문은 **자기상사 비탄성 접촉의 정전 이론**이다. 우리의 *per-contact 소성 면적/하중 법칙의 엄밀 기준*으로
> 쓰되, 패킹·dip·transport 도구로는 절대 쓰지 않는다(frame[5]).

### 8.1 비교표
| 항목 | 이 논문 (Storåkers 1997) | 우리 | 차이 / 이유 |
|---|---|---|---|
| **소성 층위** | **(3) SHAPE 소성** — 자기상사 형상변형, pile-up까지 c²로 정량 | DEM=(1)거의 없음(hooke/hyst≈선형Hertz)+(2)Stage-E(Tabor) 사후 / MPM=(3)J2 SHAPE | Storåkers=우리 **MPM과 같은 SHAPE 부류**이나 *단접촉 자기상사 해석*. 우리 DEM 접촉엔 이 항복-소성·c² 없음 |
| **접촉면적 법칙** | **A = 2π·c²(m)·r·h**, c²(0.5→1.43) | DEM Stage-E: Tabor A=F/H + volume A=V/h + 기하 caps의 min/max(5-regime) | ★★ **A/B 비교 대상**: 우리 Stage-E = 경험적 재유도, Storåkers c²·r·h = 엄밀 자기상사. **이상소성 c²≈1.43 = 우리 pile-up/volume 가정의 물리 인자** |
| **pile-up 인자** | **c²≈1.43(이상소성)** = 진짜면적/overlap면적 | ε_sphere "displaced material re-emerges as a bulge"(부피보존) | **정확히 같은 물리**: 변위 물질이 bulge로 재돌출 → 면적 ↑. c²가 그 ↑의 자기상사 정량(아래 §8.2) |
| **경도 cap** | **H ≈ 2.8 σ₀**(Tabor α=2.8, eq78) | Stage-E·H-cap이 H=3σ_y 가정(So 2021 F_th=2/3·H·A_con) | **우리 H-cap 가정의 엄밀 근거** — Storåkers가 Tabor H≈2.8σ₀를 이론 정수로 도출 |
| **경화지수** | m(변형률경화)·n(크리프) 일반 멱법칙 | LPSCl 거의 이상소성(σ_y 0.05–0.30, 경화 약함) | LPSCl ≈ m→∞ 끝 → **c²≈1.4 적용**(아래 §8.3) |
| **모듈러스 처리** | **real(무차원 σ₀)**, 연화 안 함 | DEM E_eff=1.35(18× 연화) / MPM real-bulk | Storåkers는 형상소성 직접 해석 → 연화 불필요. 우리 DEM 연화 = "이 c²·H 법칙 부재"의 보상 |
| **이체 접촉** | dissimilar(σ₁≠σ₂, D₁≠D₂) 환원(eq82,84) | AM(강체)–SE(소성) 극단 이질 | **우리 AM–SE 상호압입의 이론 기반**; Storåkers 1996 IUTAM이 복합압밀로 적용 |
| **전달** | 없음 (역학 전용) | σ_ionic+σ_e+σ_thermal 삼중항 | **frame[5] 분업** — 이 논문은 역학 절반의 *접촉면적 구성식*만 |
| **패킹/다체** | 단접촉 + 이체(2구) 국소 | DEM 132케이스 실패킹 + Furnas dip | Storåkers는 패킹 도구 아님 — c²·H **면적/하중 법칙만** 우리에 줌 |
| **차원** | axisym 2D + 이체(단접촉) | DEM/MPM 2D·3D 패킹 | 단접촉이라 절대스케일 이슈 없음(결합곡률 D로 흡수) |
| **검증** | 자기상사 이론 + FEM + 뉴턴유체 해석해 | solver=ground truth + Minnmann/Bazzoun 앵커 | 상호보완 — 이건 *접촉 구성식* 검증, 우리는 *패킹·전달* 검증 |

### 8.2 ★★★ Martin–Bouvard 2003가 이 법칙을 그대로 쓴다 (이론 계보)
`papers/martinbouvard2003_dem_composite_cold_compaction.md` §4의 DEM 접촉법칙:
- 소성 법선력 `N_P = π·Σ_pq·2^(1−1/m)·3^(1−1/m)·c(m)^(2+1/m)·r_pq^(1+1/m)·h^(1/m)` (M-B eq7) = **Storåkers et al. 유사해**.
- **접촉면적 `A = 2π·c(m)²·r_pq·h` (M-B eq8) = 이 논문의 면적 법칙 그 자체**.
- M-B가 인용한 **c(m): 0.5(선형경화) → 1.45(이상소성)** = **이 논문 Fig5의 c²(1/m+1/n)** (0.5↔1.43).

⇒ **이 digest = Martin–Bouvard DEM 접촉모델의 원천 이론**이다. 우리가 Martin–Bouvard를 "hard+soft 압밀의 정전"
으로 쓰는데, 그 DEM이 의존하는 **per-contact 소성면적·하중 법칙이 바로 Storåkers 1997/Biwa–Storåkers 1995**.
즉 우리는 이미 (Martin–Bouvard 경유로) 이 이론의 자손을 참조하고 있었고, 이 digest가 그 **뿌리를 명시**한다.

### 8.3 ★★ 우리 Stage-E(Tabor+volume) vs Storåkers c²·r·h — A/B 비교 (우리 노트의 "Stage-E A/B")
우리 CLAUDE.md/노트가 명시한 "**Storåkers/Thornton–Ning 접촉면적 → Stage-E A/B**" 비교의 **A쪽(엄밀 물리)이 이것**:

**우리 Stage-E (경험적 재유도, `network_conductivity.py:240-264`)**:
`A_physics = max(lower[A_hertz=πR*δ, A_ligg], min(caps[A_tabor=F/H, A_volume=V/h_min, A_geom=2πR_min²]))`
— Tabor(F/H, H=경도)·volume(부피보존 V/h)·기하 caps의 5-regime min/max. **목표**: 탄성 overlap을 소성 접촉면적으로 보정.

**Storåkers (엄밀 자기상사)**: `A = 2π·c²(m)·r·h`, c²(이상소성)≈1.43.

**A/B 대응 (어떻게 c²가 우리 volume 가정에 대응하나)**:
- 우리 **A_volume = V/h_min**(부피보존: 변위된 물질이 어딘가로 가야 함)은 **pile-up의 부피보존판**이다.
  Storåkers c²>1(pile-up)은 그 변위 물질이 **접촉테 bulge로 재돌출**해 진짜 면적을 키우는 것을 자기상사로 정량.
  → 우리 ε_sphere "displaced material re-emerges as a bulge" = **c²>1 pile-up의 우리식 표현**.
- 우리 **A_tabor = F/H**는 평균압=H(완전소성) 가정 → Storåkers **H≈2.8σ₀**(eq78)가 그 H의 엄밀값.
- **B/A 비교의 정량 표적**: 같은 (r, h, σ_y)에서 우리 Stage-E A_physics 와 Storåkers `2π·1.43·r·h`(이상소성)를
  대조 → 우리 5-regime 경험식이 이상소성 c²≈1.43을 **얼마나 재현**하는지가 검증. **이상소성 LPSCl이면 A는 기하
  overlap의 ~1.43배**여야 함(pile-up). 우리 A_volume이 그 근처면 Stage-E가 물리적으로 정당, 벗어나면 보정폭이 정량적 한계.
- ⚠ **단, c²는 단접촉·자기상사(독립접촉) 가정**. 고밀도(접촉 impingement, D≳0.82 — Mesarović–Fleck §6)에선 c² 자체가
  무효 → 우리 Stage-E의 min(caps) 천장(over-compression 차단)이 그 영역을 따로 처리. 둘은 **저밀도(독립접촉)에서만 직접 비교**.

### 8.4 ★ 교차참조: Mesarović–Fleck 2000 / Thornton–Ning / So 2021 / Tabor 1951
- **Mesarović–Fleck 2000** (`papers/mesarovicfleck2000_*`, 방금 digest): MFleck의 **완전소성 similarity plateau
  a²/2hR₀ → 1.4** (접촉면적/기하 overlap) = **Storåkers c²≈1.43의 dissimilar-EP FEM 대응판**. 둘 다 **~1.4 pile-up
  인자**에서 일치(한쪽 자기상사 해석, 한쪽 J2-FEM). MFleck p_m→H≈2.8–3σ_y = Storåkers eq78 α=2.8과 일치.
  → **두 정전이 면적인자 1.4·경도 2.8–3σ₀에서 독립 교차검증** (frame[4] 정신: 서로 cross-fit 아닌 독립 일치).
  실제로 MFleck §4가 **Storåkers 1997 표 c(m)·k(m)** 를 similarity 기준선으로 인용 → 두 논문이 직접 연결.
- **Thornton–Ning 1998** (`docs/data/thorntonning1998_*`): plastic 분기(p_y 한계압·잔류겹침 R_p*)는 Storåkers
  자기상사의 **단순화된 접촉법칙판**(WISHLIST #5/#14). Storåkers c²·H = 그 단순화의 엄밀 기준.
- **So 2021** (H-cap, `so2021_dem_mold_pressure_assb_coldpress.md`): F_th=2/3·H·A_con — Storåkers H≈2.8σ₀를 캡으로 사용.
- **Tabor 1951** (Hardness of Metals): H≈3σ₀·대표변형. Storåkers가 α=2.8,β_m=0.4를 **이론 정수로 채택**(eq78) — Tabor 경험식의 자기상사 근거.

### 8.5 ★ 경화지수 m/n ↔ LPSCl 소성, c²≈1.4 (우리 ε_sphere 가정 연결)
- **LPSCl SE는 거의 이상소성**(우리 MPM σ_y 0.05–0.30 GPa, 경화 약함; LPSCl 단결정 멱법칙 경화지수 작음).
  → 1/m+1/n → 0 끝 → **c² ≈ 1.4**.
- ⇒ **우리 거의 이상소성 SE의 진짜 접촉면적 ≈ 기하 overlap 면적 × ~1.4 (pile-up)**.
- 이게 우리 **ε_sphere 규약** "변위된 물질이 bulge로 재돌출, solid = Σ 원래 구 부피"(부피보존)의 정확한 물리:
  소성 시 접촉부 물질이 사라지지 않고 **테두리 bulge로 재돌출**(c²>1) → 진짜 접촉/지지 면적이 rigid-geometric
  overlap보다 큼. **rigid-geometric overlap만 세면 면적·solid를 과소**(c²=1 가정 = sink-in 없는 절단구) → 우리가
  A_volume(부피보존)·ε_sphere(부피보존)를 쓰는 이유의 자기상사 정당화.
- ⚠ 정확한 c²는 LPSCl의 실제 경화지수 m,n에 의존(현재 미측정). 거의 이상소성이면 1.4 근처, 약간이라도 경화하면
  1.4보다 낮음(Fig5; m=3급이면 c²≈1, sink-in 시작). **숫자는 "이상소성 한계 ~1.4"의 추정**, LPSCl m 정밀값 필요.

### 8.6 frame 정합성 점검
- **frame[5]**: 자기상사 단/이체 접촉 **구성식**(면적 c²·하중 H) — per-contact 면적/하중 법칙으로만 사용.
  패킹·dip·transport 도구 **아님** ✓. (Martin–Bouvard가 이 법칙을 **패킹 DEM에 꽂아** 다체로 올림 = 분업의 정석.)
- **frame[4]**: DEM도 MPM도 아닌 *제3의 엄밀 이론 기준*. DEM↔MPM cross-fit 아님. 우리 MPM J2가 단접촉서 Storåkers
  c²≈1.43·H≈2.8σ₀를 재현하는지 = **독립 sanity check 가능**(MFleck과 같은 표적). ✓
- **MPM cap dead-end과 모순?** **아님**. 우리가 죽인 건 *연속체 볼륨 cap*(입자 부피수축, 비물리). Storåkers는
  **등체적(비압축) 형상소성**(eq14 von Mises, 부피보존) — MPM champion J2와 같은 메커니즘. c² pile-up은 부피보존
  하에서 면적이 커지는 것이지 부피수축이 아님 → **MPM이 맞아야 할 단접촉 표적**, 버린 볼륨 cap 아님. ✓

## 9. 적용 인사이트 (내 연구에 어떻게)
- ① **Stage-E A/B 비교의 A쪽(엄밀 물리) 확보**: `A = 2π·c²(m)·r·h`(c²≈1.43 이상소성)를 우리 Stage-E A_physics의
  **검증 기준선**으로. 같은 (r,h,σ_y)에서 두 면적을 그려, 우리 5-regime 경험식이 이상소성 pile-up(×1.43)을 재현하는지
  정량 → 우리 노트 "Storåkers/Thornton–Ning 접촉면적 → Stage-E A/B"의 직접 실행. **저밀도(독립접촉 D<0.82)에서만 비교**.
- ② **이상소성 c²≈1.4 = 우리 ε_sphere/A_volume(부피보존)의 자기상사 정당화**: "변위 물질이 bulge 재돌출 → solid=Σ
  구부피"가 c²>1 pile-up의 우리식 표현임을 명문화. rigid-geometric overlap(c²=1)만 세면 면적·solid 과소 → 우리
  부피보존 규약이 옳다는 독립 근거(단, LPSCl m 정밀값으로 c² 확정 필요).
- ③ **Martin–Bouvard DEM의 이론 뿌리 명시**: 우리가 인용하는 Martin–Bouvard hard+soft DEM의 접촉면적/하중 법칙이
  Storåkers 1997/Biwa–Storåkers 1995(→ Storåkers 1996 IUTAM 복합압밀 적용)임을 계보로 기록 → paper에서 우리
  접촉모델의 lineage를 Hertz(1882)→Storåkers(1997)→Martin–Bouvard(2003)→우리 Stage-E로 그릴 수 있음.
- ④ **MFleck과 1.4·2.8σ₀ 교차검증 인용**: 자기상사 해석(Storåkers c²≈1.43, H≈2.8σ₀)과 dissimilar-EP FEM
  (MFleck a²/2hR₀→1.4, p_m→2.8–3σ_y)이 **독립적으로 같은 면적인자·경도**에 도달 → 우리 H-cap·pile-up 가정이
  두 정전 이론에서 동시 지지됨(강한 paper 문장).

## 10. 인용 가능 문장 (deck/paper용)
- "The plastic contact-area law A = 2π·c²(m)·r·h used in the foundational soft+hard DEM of Martin & Bouvard (2003)
  originates in the self-similarity analysis of inelastic contact by Storåkers, Biwa & Larsson (1997), where the
  similarity constant c²(m,n) ranges from ~0.5 (linear/strong hardening, sink-in) to ~1.43 (ideal plasticity,
  pile-up) and crosses unity at 1/m+1/n ≈ 1/3."
- "For our nearly ideally-plastic LPSCl solid electrolyte (weak hardening), Storåkers' c² ≈ 1.43 implies a true
  plastic contact area ~1.4× the rigid-geometric overlap area — the self-similar physics basis for our
  volume-conserving ε_sphere convention in which displaced contact material re-emerges as a rim bulge."
- "Storåkers' universal hardness H ≈ 2.8 σ₀ (adopting Tabor 1951's α = 2.8) and Mesarović–Fleck's (2000)
  fully-plastic similarity plateau (contact-area factor a²/2hR₀ → 1.4, p_m → 2.8–3 σ_y) independently agree on the
  ~1.4 pile-up factor and the H ≈ 3σ_y cap that underlie our Stage-E plastic contact-area model."
- "Self-similarity reduces the moving-boundary, history-dependent inelastic indentation problem to a stationary
  flat-die problem solved once and cumulatively superposed (Storåkers et al. 1997) — the per-contact constitutive
  foundation on which discrete-element packing models (frame [5]: DEM = packing/transport) build."

## 11. 주의/한계 (over-claim 방지)
- **단접촉·이체(2구) 연속체 구성식** — 패킹·다체·dip·transport **전무**. 우리 §8은 *접촉 면적/하중 법칙 기준*으로만
  사용(이체 확장도 두 곡면 국소접촉까지). frame[5] 역학-절반. **"Storåkers로 porosity/dip/σ를 본다"는 과대해석 금지.**
- **소재 무관(무차원 σ₀)** — LPSCl 절대값 없음. §8.5의 c²≈1.4는 "LPSCl≈이상소성" 가정의 결과이며, 실제 c²는 LPSCl의
  **경화지수 m,n에 의존**(미측정). 약한 경화라도 c²<1.4 (Fig5; m=3급이면 c²≈1) → "**이상소성 한계 ~1.4의 추정**"으로 사용.
- **자기상사 = 독립접촉 가정**: 접촉윤곽 자기상사 팽창은 **인접 접촉 비간섭**(impingement 무시)을 전제. 고밀도(D≳0.82,
  Mesarović–Fleck §6)에선 c²·자기상사 자체가 무효 → 우리 고밀도(90 %+) 압밀에 직접 c² 적용 주의. 우리 Stage-E
  min(caps) 천장이 그 영역(over-compression)을 별도 처리하므로 **저밀도에서만 c²와 직접 대조**.
- **digitized 값**(Fig5의 c² 곡선 중간점 1.10/0.70/0.90 등)은 **추세값(±)** — stated 끝점/천이(c²≈1.43 이상소성,
  c²=1 at 1/m+1/n≈1/3, c²≈0.5 선형; α=2.8, β_m=0.4; m,n→∞)와 구분.
- **마찰 미고려**(무마찰 압입 BC, eq18) — 실제 SE-AM 마찰(μ~0.4, Bazzoun) 무시. 단 자기상사는 마찰·접착도 수용
  가능하다고 명시(Spence 1968, Borodich 1993 인용) — 본문은 무마찰만 명시 해석.
- **E* 결합모듈러스 무관**: 이 논문은 모듈러스 연화를 다루지 않음(형상소성 직접 해석 → real σ₀). 우리 DEM 18× 연화는
  이 논문의 **부재 영역**(이 논문엔 항복-소성·c²가 *있어서* 연화 불필요) — 연화는 우리 DEM이 이 c²·H 법칙을 *안 가져서*
  생기는 보상이라는 점(So 2021·MFleck 논리)을 함께 명시해야 over-claim 아님.
- **c²(m)=c²(n) 근사**: 소성흐름↔크리프 c² 일치는 "very close agreement"(약 5 % 이내, 본문). 정밀 비교 시 ±5 % 인지.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
