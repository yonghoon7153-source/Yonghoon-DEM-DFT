# 점착 탄소성 구의 stick/bounce — 항복압 캡(p_y) 접촉 LAW의 정의서 — Thornton & Ning (Powder Technology 1998)

> slug `thorntonning1998_adhesive_elastoplastic_contact` · DOI `10.1016/S0032-5910(98)00099-0` · type `DEM (contact-LAW theory)` · PDF `ThorntonNing_1998_PowderTech_StickBounce_AdhesiveElastoPlasticSpheres.pdf` · digested `2026-06-26` · status ✅
> ★★ **WISHLIST Tier-1 #14 (③) = "경로 A"의 핵심 LAW.** 우리 현재 모델(Luding 2008 `hooke/hysteresis`, `papers/luding2008_*`)이 **갖지 못한 항복압 캡 p_y**를 이 논문이 가진다. **Varkey 2026(`papers/varkey2026_*`)이 base 접촉모델로 쓰는 바로 그 LAW**이며, So 2021(`papers/so2021_*`) H-cap·Tabor H≈3σ_y와 같은 발상. → 우리 18× E-연화를 *real E + 항복 캡*으로 대체하는 직접 경로(`elasto_plastic_feasibility.md` 경로 A).

---

## 0. 왜 이 논문이 우리에게 *경로-A 정초*인가 (먼저 읽을 것)

우리 DEM 압밀은 LIGGGHTS `hooke/hysteresis`(= Luding 2008 eq6) 위에서 돈다. 그 LAW는 **소성 분기(k₁→k₂)와
영구겹침(δ₀)은 가지지만, 접촉 평균압이 항복압 p_y(또는 경도 H)에 도달하면 압을 *cap*하는 메커니즘이
없다.** 그래서 같은 300 MPa에서 진짜 소성보다 덜 변형하고, 우리는 그걸 **E_SE를 24→1.35 GPa로 18× 낮춰**
보상한다. (`luding2008_*` §7.4 / CLAUDE.md frame[2].)

**Thornton–Ning 1998이 바로 그 빠진 캡을 가진 접촉 LAW다.** 4단계 — (1) 탄성 Hertz → (2) 항복 개시(평균압이
p_y 도달) → (3) **선형** 소성 분기(접촉압이 p_y에 *고정*) → (4) 영구겹침을 남기는 더 큰 반경 R_p*로의 탄성
제하 — 이 구조가 곧 "**Luding의 소성 분기 + 빠진 H/p_y 캡**"이다. 즉:

> **Thornton–Ning ≈ Luding eq6 의 소성 분기에 "접촉 평균압 ≤ p_y" 제약을 얹은 것** = 경로 A가 LIGGGHTS에
> 넣고자 하는 바로 그 LAW. (So 2021은 같은 걸 Tabor 경도 H로, `F_th=2/3·H·A_con`로 함 — eq14. Tabor H≈3σ_y가
> Thornton–Ning의 p_y≈1.6σ_y와 같은 물리.)

이 digest가 *직접 해소/근거화*하는 것:
1. **경로 A의 LAW 사양**: 항복 캡 p_y의 정의(eq9·14), 소성 분기 식(eq19), 영구겹침 반경 R_p*(eq20·28),
   adhesive 확장(eq58–77)까지 — LIGGGHTS pair_style에 얹을 *완성된 분석식*.
2. **Varkey 2026의 base LAW 출처**: Varkey가 쓴 `F_el-pl=f_y+πp_y·R*(δ−δ_y)`(varkey digest §4)는 이 논문
   eq19 `P=P_y+πp_y·R*(α−α_y)`의 재서술이다. Varkey는 이 위에 multi-contact 구속항만 더했다.
3. **JKR 점착 ↔ 우리 SE-SE cohesion**: 우리 LIGGGHTS `adhesionStiffness`(k_c) / MPM `--coh`(backlog A3)의
   엄밀판 = Thornton–Ning의 adhesive-EP(JKR 표면에너지 Γ + 항복 캡).
4. **Stage-E의 타당 조건**: 우리 Stage-E(Tabor+volume)는 접촉압 ≈ H(완전소성)를 가정 — Thornton–Ning은
   *언제* 그 가정이 성립하는지(α>α_y, 압이 p_y로 cap된 소성 분기)를 정확히 알려준다.

⚠ **단, 이 논문 자체의 목적은 "충돌 반발계수(COR) 분석식"이지 압밀이 아니다.** 우리에게 핵심 가치는 **법선
접촉 LAW(4단계 + JKR)**이며, 반발계수·stick/bounce 결과는 *그 LAW의 검증/예시*다. 우리는 준정적 압밀이라
COR 자체는 직접 안 쓰지만, **LAW(특히 항복 캡과 영구겹침)는 그대로 쓴다.**

---

## 1. 한 줄 요약

점착 있는/없는 **탄성-완전소성(elastic-perfectly plastic) 구**의 법선 충돌을 4단계 접촉 LAW로 모델하고,
충돌속도·임계 점착속도(sticking velocity)·항복속도(yield velocity)의 함수로 **반발계수의 분석해**를 유도.
핵심 LAW = **Hertz 탄성 → p_y(한계 접촉압)에서 항복 → 압을 p_y로 고정한 *선형* 소성 분기 → 영구겹침을 남기는
더 큰 반경 R_p*의 탄성 제하**. 점착은 JKR(표면에너지 Γ, pull-off P_c=3/2·πΓR*)로 다룬다. **= 우리 hooke/
hysteresis가 갖지 못한 "항복압 캡"을 가진 접촉 LAW, 그리고 Varkey 2026이 쓰는 base 모델.**

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Colin Thornton, Zemin Ning** (Civil & Mechanical Eng., Aston University, Birmingham; Ning 일부 Cavendish/Cambridge) | **Powder Technology 99(2) 154–162 (1998)**; Received 1997-06-23, revised 1998-05-07, accepted 1998-06-09 | **10.1016/S0032-5910(98)00099-0** | **소재 무관 — 일반 탄성-완전소성 점착 구**. 워크드 예시(Fig 9/10)는 p_y=0.5–3.04 GPa·Γ=0.2–0.4 J/m² 범위. **LPSCl/NMC811 직접 데이터 없음** | **접촉 LAW 이론** (+ COR 분석해 + 검증용 수치 시뮬, Ning 1995 박사논문) |

> ★ **고전 정초 논문**(Thornton 그룹). Storåkers·Johnson(Contact Mechanics 1985)·JKR(1971)·Davies(1949)와
> 더불어 입자기술 접촉역학의 표준 인용. **Varkey 2026이 base 접촉모델로 명시 인용**(varkey §2.2), So 2021
> H-cap·우리 Stage-E의 이론적 친척. PDF OCR은 숫자치환으로 깨졌으나(예: "5"→"5", "0"→"0") **수식·그림·표는
> 가독** — 아래 수식은 모두 원문 eq 번호로 검증.

## 3. 핵심 물성 (수치)

> ⚠ **이 논문은 소재 측정값 논문이 아니라 LAW 논문**이다. 아래 "수치"는 (a) LAW를 정의하는 무차원/분석식,
> (b) Fig 9/10 워크드 예시값(금속급 p_y·Γ). **LPSCl·NMC811 절대값 전이 불가** — 가치는 *수식·항복 캡 구조·
> 정성거동*에 있다.

| 물성/파라미터 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **한계 접촉압 p_y** (= 항복 캡) | **0.5 / 1.0 / 3.04 GPa** (예시 3종) | Fig 10 워크드 | stated | p_y = 2E*a_y/(πR*) (eq9); 소성 분기의 압 천장 |
| 항복속도 V_y | 0.62 m/s (p_y=3.04) / 0.045 (p_y=1.0) / 0 (p_y=0.5, 0하중서 소성) | Fig 10 | stated | V_y∝p_y^(5/2) (eq10); 이 아래는 탄성 |
| 임계 점착속도 V_s | 0.016 m/s (p_y≥1) / 0.032 (p_y=0.5) | Fig 10 | stated | V_s∝(Γ^5R*^4/E*^2)^(1/6) (eq54) |
| 표면에너지 Γ | 0.2 / 0.4 J/m² | Fig 9/10 | stated | JKR interface energy; pull-off P_c=3/2πΓR* |
| 반발계수 e (고속극한) | **e ∝ V^(−1/4)** | V_i>10·V_y | stated | e=1.185(V_y/V_i)^(1/4) (eq46) |
| e_max (점착 영향) | 1.0(p_y=3.04) / 0.9(1.0) / 0.5(0.5) | Fig 10 | stated | 무른 입자일수록(p_y↓) e_max↓ |
| 소성 접촉강성 k_N | k_N = πR*·p_y = 2E*a_y (상수) | 소성 분기 | stated | eq22; Hertz의 감소기울기와 대비 |
| FE 검증(타 논문) 인용 | 항복 후 압분포가 균일 p_y로; 소성영역이 표면 도달 = 항복력의 ~6배 | §5 인용 | stated | Hardy et al.[8] FEA; "elastic enclave" 중심 잔존 |
| **E_SE / σ_y / ν** | **소재값 없음** (p_y가 일반 파라미터) | — | — | p_y≈1.6σ_y (또는 H≈3σ_y, Tabor) 로 σ_y 연결 |
| porosity / σ / coverage / Z | **n/a** (충돌 LAW — 압밀·전달 안 다룸) | — | — | frame[5]: 단일 접촉 LAW만; 집합거동·전달 0 |
| PSD | n/a (2구 또는 구-평면 일반) | — | — | mono/poly 무관 — LAW는 R*로 일반화 |

## 4. 시뮬레이션 방법 ★ — **이것이 경로-A 접촉 LAW의 정의**

> 이 논문은 "시뮬레이션 코드" 논문이 아니라 **분석 LAW + 검증용 수치적분**이다. Ning(1995 박사논문 [13])이
> 이 LAW + 뉴턴 운동방정식을 수치적분해 Fig 3/8/9/10을 얻었다. 아래는 **LAW 자체의 4단계 정의**.

- **code / version**: 비특정(Ning 1995 in-house 충돌 적분기). **방법론 자체가 우리가 LIGGGHTS에 얹고자 하는
  접촉 LAW의 정의**. 기호: E* 환산모듈러스(eq5), R* 환산반경(eq6), m* 환산질량(eq8), α=상대접근(겹침), a=접촉반경.

- **DEM 접촉법칙 (법선, 비점착)** — ★★★ **4단계 LAW 본체** (Fig 1·2):

  - **Phase 1 — 탄성 Hertz 재하 (α < α_y):**
    - Hertz 압분포 `p(r)=(3P)/(2πa²)·[1−(r/a)²]^(1/2)` (eq1) — 반타원체.
    - 법선력 `P = (4/3)·E*·R*^(1/2)·α^(3/2)` (eq2) → **F ∝ δ^1.5** (우리 Hertz와 동일).
    - 접촉반경 `a=(3PR*/(4E*))^(1/3)`, `a²=R*·α` (eq3·4).

  - **Phase 2 — 항복 개시 (α=α_y, a=a_y):** ★ **여기가 Luding에 없는 부분**
    - **한계 접촉압 정의** `p_y ≡ p₀ = 2E*·a_y/(πR*)` (eq9). = 항복 시점의 *peak(중심) 접촉압*. 이 압을
      넘으면 압을 더 올리지 않고 cap한다. (Fig 1 우측의 평탄 천장 p_y.)
    - 항복력·반경 관계 `p_y = 3P_y/(2πa_y²)`(eq14), `a_y³ = 3R*P_y/(4E*)`(eq16).
    - **항복속도** (이 아래 충돌은 순수 탄성): 에너지 균형 `½m*V_y² = ∫₀^{α_y}P dα = 8E*a_y⁵/(15R*²)`(eq7)
      → `V_y = (π/2E*)²·(8πR*³/15m*)^(1/2)·p_y^(5/2) = 3.194·(p_y⁵R*³/(E*⁴m*))^(1/2)` (eq10).
      구-평면(R*=R, m*=m): `V_y=1.56·(p_y⁵/(E*⁴ρ))^(1/2)`(eq11, Davies 1949).
    - **물리 의미**: V_y ∝ p_y^(5/2) → p_y(즉 σ_y)가 클수록 항복이 어렵다(더 큰 V 필요). 우리 LPSCl는 무른
      편(σ_y 0.05–0.30 GPa) → 낮은 압에서 항복.

  - **Phase 3 — 소성 재하 분기 (α > α_y): ★ 압을 p_y로 고정한 *선형* 분기**
    - 소성영역 가정: Hertz 압분포를 p_y에서 cut-off, 안쪽 반경 a_p에 균일압 p_y 가정(Fig 1). 항복 후 법선력
      `P = P_e − 2π∫₀^{a_p}[p(r)−p_y]r dr`(eq12), P_e=같은 면적을 줄 등가 탄성력(eq3 형).
    - 적분 → `P = πa_p²·p_y + P_e·[1−(a_p/a)²]^(3/2)`(eq13), `a²=a_p²+a_y²`(eq17).
    - **★ 최종 힘-변위(선형)**: `P = P_y + π·p_y·R*·(α − α_y)` (**eq19**). **= 선형!** (Fig 2의 직선 P가지.)
      소성 분기는 Hertz 곡선에 항복점에서 *접하고*, 연장하면 P-축을 P₀=−P_y/2(<0)에서 만난다(eq24·25).
    - **소성 접촉강성** `k_N = πR*·p_y = 2E*·a_y` (eq22) — **상수**(Hertz의 감소기울기 ∝√α 와 대비).
    - ⇒ **이것이 "Luding 소성 분기 + p_y 캡"이다**: Luding은 k₁→k₂로 *선형 근사* 분기를 갖되 캡 압이 없다.
      Thornton–Ning은 그 선형 분기의 *기울기를 p_y가 물리적으로 결정*하고(k_N=πR*p_y), *압 자체를 p_y로 cap*한다.

  - **Phase 4 — 탄성 제하 (더 큰 반경 R_p*, 영구겹침):** ★ **영구 소성변형 = 우리 ε_sphere displaced-material**
    - 소성변형 후 제하 시 접촉면 곡률이 1/R_p* < 1/R*(평탄해짐). 제하는 Hertz지만 **R_p* 곡률**로.
    - 최대압축점에서 R_p*·P* = R*·P_e* (eq20), P_e* = 4/3·E*R*^(1/2)·α*^(3/2)(eq21).
    - → `R_p* = (4E*/(3P*))·((2P*+P_y)/(2πp_y))^(3/2)` (eq28). **1/R_p* < 1/R* → 큰 반경(평탄한 압흔).**
    - **제하 힘법칙** `P = (4/3)·E*·R_p*^(1/2)·(α − α_p)^(3/2)` (eq29). α_p = **영구 잔류겹침**(P=0이 되는 α).
    - ⇒ **이 α_p가 곧 영구히 남는 겹침** = Luding δ₀ = So h_eq = **우리 ε_sphere "displaced material"**.
      Thornton–Ning은 그 잔류겹침이 *p_y 캡과 R_p*로부터 물리적으로 유도*됨을 보인다(경험 파라미터 아님).

  - **★ Fig 3 (검증)**: 충돌속도 4종의 P-δ 곡선 — V↑이면 (i) 더 깊은 소성, (ii) **제하 강성↑**(R_p*↑ ⇒ 더
    가파른 반발). 그래서 탄성복원/압축 일 비율이 V에 의존 → **COR가 속도의존**(§3).

- **반발계수 COR (비점착 EP)** — ★ LAW 검증/예시 (우리는 압밀이라 직접 안 쓰나 LAW 정당성):
  - 일반식 `e=(6√3/5)^(1/2)·[1−(1/6)(V_y/V_i)²]^(1/2)·[(V_y/V_i)/((V_y/V_i)+2√(6/5−(1/5)(V_y/V_i)²))]^(1/4)`
    (**eq44**) — Vi=Vy에서 e=1 만족.
  - 고속극한(V_i>10V_y): `e=1.185·(V_y/V_i)^(1/4)` (**eq46**) → **e ∝ V^(−1/4)**(논문 핵심 결과, Fig 4).
    구-평면 `e=1.324·(p_y⁵/(E*⁴ρ))^(1/8)·V_i^(−1/4)`(eq47; Johnson 교재는 prefactor 1.72 — 소성강성 2배 가정).

- **점착(JKR) 탄성 구 (§4)** — ★ **우리 SE-SE cohesion의 엄밀판**:
  - JKR 힘-접근 관계(eq48, Johnson Contact Mechanics 1985), pull-off `P_c = 3/2·πΓR*`(**eq50**),
    0하중 평형겹침 `α_f = 3/4·(π²Γ²R*/E*²)^(1/3)`(eq49).
  - **물리(Fig 5)**: 두 표면이 닿는 순간 vdW로 힘이 **P=−8P_c/9**로 즉시 점프(점 A). 제하 시 P=0(점 A)을
    지나도 표면이 붙어 있어 추가 일이 필요 → 분리는 점 F에서. **접촉 파괴 일** `W_s=0.9355P_c·α_f=
    7.09(Γ⁵R*⁴/E*²)^(1/3)`(eq52).
  - **임계 점착속도** `V_s=(14.18/m*)^(1/2)·(Γ⁵R*⁴/E*²)^(1/6)`(eq54). V_i<V_s면 stick(e=0). 점착 COR
    `e=[1−(V_s/V_i)²]^(1/2)`(eq57).

- **점착 탄소성 구 (§5)** — ★ **JKR + 항복 캡 결합 (우리 경로 A + cohesion의 완성형):**
  - JKR 압분포에 p_y 캡(Fig 7): `p(r)=2E*a/(πR*)·[1−(r/a)²]^(1/2) − (2ΓE*/(πa))^(1/2)·[1−(r/a)²]^(−1/2)`(eq58).
  - 등가 Hertz력 `P₁=P+2P_c±(4PP_c+4P_c²)^(1/2)`(eq60), 점착 한계압 `p_y=2E*a_y/(πR*)−(2ΓE*/(πa_y))^(1/2)`
    (eq65) — **점착이 항복압을 낮춘다**(표면인력이 응력 보태므로).
  - 소성 강성 `dP_p/dα`(eq69), 제하 강성(eq72·73, Ning 1995), **plastic pull-off 증가** `P_cr=3/2·πΓR_p*`
    (eq77) — **충돌속도↑ → R_p*↑ → pull-off↑**(Fig 8: 제하 강성·pull-off 모두 V와 함께 증가).
  - 해석해 불가 → **가산 소산 가정**: `(1−e²)=(1−e_p²)+(1−e_a²)`(eq78), e_p=소성(eq44), e_a=점착(eq57).
    → V_i≤V_s: e=0; V_s<V_i≤V_y: e=[1−(V_s/V_i)²]^(1/2); V_i>V_y: eq81. (Fig 10 수치와 잘 일치.)

- **재료 파라미터**: **소재 무관** — LAW는 (E*, R*, m*, p_y, Γ)로 일반화. Fig 9/10 워크드 예시만
  p_y=0.5–3.04 GPa, Γ=0.2–0.4 J/m²(금속급).
- **bond/binder 모델**: 없음(점착은 JKR Γ로 통합).
- **MPM / continuum**: 없음(순수 분석 접촉 LAW + 충돌 적분).
- **전달 솔버**: **없음**(σ_ionic/e/thermal 전혀 안 다룸) → frame[5]에서 **역학(접촉 LAW) 절반만**.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구(또는 구-평면)만** — 형상 일반화는 R*뿐. **입자 SHAPE는 절대 안 변함.**
  - **rigid 구 + CONTACT 탄소성** — α_p 영구겹침은 *접촉점 국소 압흔의 proxy*이지 **진짜 입자 SHAPE 흐름이
    아님.** ⇒ `elasto_plastic_feasibility.md §0` 층위(1) CONTACT-LAW(층위(3) SHAPE는 우리 MPM).
  - PSD 무관 — LAW는 단일 접촉(R*=R₁R₂/(R₁+R₂))이라 mono/bi/poly 다룰 필요 없음(집합거동을 안 봄).
- **도메인/RVE / seeds / 압력범위**: **없음** — 단일 충돌(2구 또는 구-평면). 압력이 아니라 **충돌속도**가
  제어변수(Fig 3 100–400nm 변위, Fig 9/10 0.01–100 m/s). 준정적 압밀이 아니라 동역학 충돌.
- **특이사항/튜닝**: §6 철학 = "**식을 σ_y·Γ 같은 *측정 어려운* 재료물성이 아니라, 단순 충돌실험으로 얻는
  파라미터(V_y, V_s)로 표현**" — 실용성 강조. 우리에겐 반대로 **재료물성(σ_y→p_y) 기반 LAW**가 필요(압밀이라).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1 (★)** | **비점착 EP 압분포**: Hertz 반타원 → 항복 후 중심 평탄압 **p_y** + 바깥 Hertz 잔여(a_p 안쪽 균일, a까지) | **항복 캡의 정의 그림**. 우리 Stage-E가 가정하는 "접촉압→포화" 상태의 출처. p_y 평탄압 = 완전소성 접촉면 |
| **2 (★★ 핵심)** | **비점착 EP 힘-변위**: Hertz 곡선 P_e, **선형 소성 P가지**(항복점서 접하고 P₀=−P_y/2서 P축 교차), 항복점(α_y,P_y), 최대(α*,P*), 제하점 α_p | **= 경로 A의 LAW 도식.** eq19 선형 분기 + eq29 제하. **Luding eq6 Fig 1과 직접 대조**: Luding은 k₁→k₂ 선형이되 캡 없음; 여기는 기울기를 p_y가 결정+압 cap |
| **3** | 비점착 EP, 충돌속도별 P-δ (실제 수치) | V↑→소성↑·제하강성↑(R_p*↑) → COR 속도의존의 근원. 우리 Stage-E의 "깊은 접촉=큰 소성면적"과 정성 일치 |
| **4** | 비점착 EP COR vs V/V_y (eq44 vs eq46 vs 수치) | **e∝V^(−1/4)** 고속극한; eq46은 V>10V_y서만 정확. (압밀 무관, LAW 검증) |
| **5** | **JKR 점착탄성 힘-변위**: 닿는 순간 −8P_c/9(점 A) → 최대 B → 제하 → 분리 F | **우리 SE-SE adhesion의 물리 도식.** pull-off P_c, 접촉파괴 일 W_s(점 A–F 면적) |
| **6** | JKR 점착탄성 COR vs V/V_s (eq57) | e=0.995 @V=10V_s; V<V_s면 stick(e=0). 우리 cohesion이 stick 만드는 조건 |
| **7 (★)** | **점착 EP 압분포**(JKR + p_y 캡): 중심 평탄 p_y + JKR 인장 가장자리 | **경로 A + cohesion 결합형.** 점착이 항복압을 낮춤(eq65). 우리 SE-SE(끈끈+무름) 접촉의 정확한 그림 |
| **8** | 점착 EP 힘-변위(수치, 충돌속도별) — 제하강성·pull-off 모두 V와 증가 | **plastic pull-off P_cr=3/2πΓR_p*(eq77)**: 깊이 압밀된 SE 접촉일수록 떼기 어려움 — 우리 압밀 후 SE망 결속 |
| **9** | 점착 EP COR vs 충돌속도, Γ=0.2 vs 0.4 J/m² | 점착은 **V<V_y에서만** COR에 민감, V>V_y면 둔감 — 압밀(저속)서 점착 중요 |
| **10 (★)** | 점착 EP COR vs 충돌속도, **p_y=0.5/1.0/3.04 GPa** | **항복압(=σ_y) 효과**: p_y↓ → e_max↓(0.5GPa면 0하중 항복, e_max=0.5). 우리 무른 LPSCl(낮은 p_y)의 거동 단서 |
| 11 | 점착 EP COR vs V/V_y, V_s/V_i 비별 곡선군 | 종합 거동맵(eq79–81). stick→상승→peak→V^(−1/4) 하강 |

## 6. Post-processing ★

- **무엇**: 이 논문은 **분석 LAW 유도 + COR 닫힌형**이 본체. 후처리라 할 것은 (a) 에너지 균형(재하/제하 일의
  비 = e², eq30–44), (b) Ning(1995) 수치적분으로 P-δ·COR 곡선(Fig 3/8/9/10), (c) **가산 소산 분해**(eq78,
  소성 e_p + 점착 e_a). **Heckel/percolation/coverage/tortuosity/porosity 규약 — 전부 없음**(충돌 LAW 전용).
- **도구**: Ning 1995 박사논문 in-house 충돌 적분기. FE 검증은 *인용*(Hardy et al.[8], Sinclair et al.[9]).
- **수치화·플롯·기록**: COR를 정규화 속도(V/V_y, V/V_s)로 플롯. FEA 결과(항복 후 균일 p_y 압분포; 소성영역이
  표면 도달 = 항복력의 ~6배; 중심 "elastic enclave" 잔존)를 §5에서 인용해 *균일 p_y 가정*을 정당화.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★★ **이 절이 핵심.** Thornton–Ning 1998 = **경로 A의 접촉 LAW 정의서**이므로 "대비"는 곧 **(가) Luding이
> 못 가진 항복 캡을 이 LAW가 어떻게 채우는지 + (나) Varkey가 이걸 어떻게 쓰는지 + (다) So 2021/Stage-E/우리
> 18× 연화와의 관계**다.

### 7.1 ★★★ 경로 A의 핵심 — Luding(우리 현재 모델)이 **못 가진 항복 캡**을 이 LAW가 가진다

CLAUDE.md frame[2] / `luding2008_*` §7.4: 우리 `hooke/hysteresis`(=Luding eq6)는 **소성 분기(k₁→k₂, δ₀)는
있으나 경도/항복압 캡이 없다** → 같은 300 MPa서 진짜 소성보다 덜 변형 → **E_SE 24→1.35 GPa 18× 연화로 보상**.

**Thornton–Ning이 정확히 그 빠진 캡을 가진다.** 두 LAW의 1:1 대조:

| 단계 | Luding eq6 (우리 현재) | Thornton–Ning 1998 (경로 A) | 차이 |
|---|---|---|---|
| **초기 재하** | k₁·δ (선형) | (4/3)E*R*^(1/2)α^(3/2) = **Hertz** (eq2) | Luding 선형 vs TN δ^1.5 (둘 다 탄성) |
| **항복 개시** | **없음** (캡 없이 k₂로 보간) | α_y에서 **평균압 = p_y 도달** (eq9) | ★ **TN만 물리적 항복점** |
| **소성 분기** | k₂(δ−δ₀) 선형, 기울기 경험적 | P_y+**πp_y·R*(α−α_y)** 선형, 기울기 **k_N=πR*p_y**(물리) (eq19·22) | ★ **TN은 압을 p_y로 cap**; Luding은 캡 압 없음 |
| **영구겹침** | δ₀=(1−k₁/k₂)δ_max (경험) | α_p (R_p* 제하서 P=0; eq29) — **p_y·R_p*에서 유도** | 둘 다 영구겹침; TN은 *물리적으로* 결정 |
| **제하** | k₂ 선형 | (4/3)E*R_p*^(1/2)(α−α_p)^(3/2) = **Hertz, 큰 반경** (eq29) | TN은 평탄화된 압흔 반경 R_p* |

⇒ **핵심**: Thornton–Ning = **"Luding의 선형 소성 분기 + 빠진 p_y 캡"**. 우리가 LIGGGHTS에 이 LAW(또는 그
캡)를 얹으면, **접촉 평균압이 p_y(LPSCl ≈0.08–0.48 GPa = 1.6×σ_y 0.05–0.30)에서 고정**되어 *real E_SE=24
GPa로도* 300 MPa 압에서 충분히 변형(eq19 선형 분기) → **18× 연화 불필요**. (이것이 `elasto_plastic_feasibility.md`
경로 A의 LAW 근거. So 2021이 같은 발상의 H-cap으로 LPS 상대밀도 0.98 달성 = 선례.)

⚠ **단 — 우리 압밀 접촉압(~300 MPa = 0.30 GPa)과 LPSCl p_y(~0.08–0.48 GPa)가 *같은 자릿수***임에 주의:
- σ_y=0.30 GPa(상한)이면 p_y≈0.48 GPa > 0.30 MPa-press → 일부 접촉만 항복(부분 소성).
- σ_y=0.05 GPa(하한)이면 p_y≈0.08 GPa ≪ 0.30 → 대부분 접촉 항복(완전 소성, 압 p_y로 cap).
- ⇒ **경로 A의 결과는 σ_y(→p_y) 선택에 민감** — Fig 10이 정확히 이걸 보여줌(p_y 0.5→1.0→3.04에서 거동 급변).
  우리 MPM champion σ_y=0.15 GPa(2D)/0.30(3D)와 **정합 검증** 필요(frame[4]: DEM·MPM 각각 실험 보정).

### 7.2 ★★ Varkey 2026이 쓰는 base 접촉 LAW가 바로 이것

`papers/varkey2026_*` §4(또는 varkey §2.2)의 접촉모델 식이 **이 논문 eq19의 재서술**이다:

| Varkey 표기 (varkey §4) | Thornton–Ning 1998 원전 | 관계 |
|---|---|---|
| 탄성 `F_el=(4/3)E*√(R*δ³)` (δ<δ_y) | **eq2** `P=(4/3)E*R*^(1/2)α^(3/2)` | **동일**(Hertz) |
| 소성 `F_el-pl=f_y+πp_y·R*(δ−δ_y)` (δ≥δ_y) | **eq19** `P=P_y+πp_y·R*(α−α_y)` | **동일**(f_y↔P_y, δ↔α) |
| 제하 `F_unl=(4/3)E*√(R_p*(δ−δ_R))` | **eq29** `P=(4/3)E*R_p*^(1/2)(α−α_p)^(3/2)` | **동일**(δ_R↔α_p 잔류겹침) |
| `f_y=(1/6)(R*/E*)²(πp_y)³`, `δ_y=(1/4)(R*/E*²)(πp_y)²` | eq14·16·9 조합의 *닫힌형 재서술* | TN은 p_y·a_y·P_y 관계로 줌; Varkey는 p_y로 직접 푼 형태 |
| 항복비 0.0103 (δ_y/...) | (p_y·E*에서 유도) | Varkey halide(E=10.58 GPa) 수치값 |

⇒ **Varkey 2026(2026 최신 DEM)의 *접촉 LAW = Thornton–Ning 1998*. Varkey의 신규성은 그 위의 multi-contact
구속항(F_mc=β·ν·a_ij·P_ij, Giannis)뿐.** 따라서 우리가 경로 A로 이 LAW를 도입하면 **Varkey와 동일한 접촉
LAW 기반**에 서게 된다(거기에 우리 MPM 형상소성·σ 삼중항이 더해짐 = 우위). Varkey FEM 검증(varkey SI Fig S1)이
"Thornton–Ning 단독은 고밀도서 under-stiff, F_mc가 보정"을 보임 — **즉 경로 A에 TN만 얹으면 ρ>0.7서 과소강성
(우리 18× 연화가 메우던 그 증상)이 남을 수 있어** F_mc(경로 B) 보강이 후속 고려사항.

### 7.3 ★★ So 2021 H-cap·Tabor H≈3σ_y와 같은 발상 (캡의 두 버전)

| 모델 | 항복 기준 | 캡 메커니즘 | 우리 대응 |
|---|---|---|---|
| **Thornton–Ning 1998** | 평균 접촉압 = **p_y** (eq9) | 소성 분기서 압을 p_y로 고정(eq19, k_N=πR*p_y) | 경로 A (Hertz 기반 캡) |
| **So 2021** (`so2021_*`) | 접촉력 = **F_th=2/3·H·A_con** (eq14) | overlap 완화 ∂h_eq/∂t=(F_spring−F_th)/(t_rel·k_n) (eq13) | 경로 A (경도 H 기반 캡) |
| **Tabor 1951** | — | **H ≈ 3σ_y** (완전소성 경도) | p_y·H를 σ_y로 잇는 다리 |

- **p_y ↔ H ↔ σ_y 환산**: Tabor 완전소성 경도 H≈3σ_y; Thornton–Ning p_y는 *항복 개시 시 peak 압*이라
  ≈1.6σ_y(탄성-소성 전이 시작); 완전소성 도달 시 평균압→H≈3σ_y. So의 F_th=2/3·H·A_con은 포물선 압분포
  평균(2/3 인자) → 평균압≈2/3·H≈2σ_y. ⇒ 세 모델 모두 **"접촉압을 σ_y의 ~1.6–3배에서 cap"**하는 같은 물리,
  표현만 다름.
- **우리 Stage-E의 타당 조건**: Stage-E(Tabor+volume) 소성 접촉면적은 **접촉압 ≈ H(완전소성)** 가정.
  Thornton–Ning은 *언제 그게 성립하는지* 정확히 줌 = **α>α_y(항복 후), 압이 p_y로 cap된 소성 분기**.
  α<α_y(탄성 Hertz)면 Stage-E의 H-가정은 과대. → Stage-E 적용 전 **접촉이 항복했는지(local 압>p_y) 체크**가
  물리적으로 옳다(현재는 일괄 적용).

### 7.4 ★ JKR 점착 = 우리 SE-SE cohesion (LIGGGHTS k_c / MPM `--coh`)의 엄밀판

- Thornton–Ning의 **JKR 점착**(Γ, P_c=3/2πΓR*, eq50; 점착 EP 압분포 eq58; plastic pull-off P_cr=3/2πΓR_p*
  eq77)이 우리 SE-SE 결합의 *엄밀 이론판*:
  - 우리 LIGGGHTS `coefficientAdhesionStiffness`(k_c, SE-SE 1e6 = AM의 10×) = Luding의 −k_c·δ 선형 점착.
    **Thornton–Ning은 같은 점착을 JKR(표면에너지 Γ 기반, 물리적)로** 준다 → k_c↔Γ 매핑의 이론 기준.
  - **MPM `--coh`(backlog A3)** = 연속체 SE에 attractive σ. Thornton–Ning JKR이 그 점착의 *접촉-스케일
    정의*(pull-off·접촉파괴일 W_s·jump-in −8P_c/9) → `--coh` 도입 시 검증 기준.
- ★ **점착이 항복압을 낮춘다**(eq65: p_y_adh = 2E*a_y/(πR*) − (2ΓE*/(πa_y))^(1/2)) — 표면인력이 응력을
  보태므로 더 낮은 외력서 항복. ⇒ 우리 끈끈한 SE-SE는 *덜 눌러도 소성* → 압밀 촉진. (So Fig 6b: SE-SE
  overlap 0.10이 압력무관 高 = 점착 잔류겹침. 정성 일치.)
- ★ **plastic pull-off 증가**(eq77, Fig 8): 깊이 압밀된 SE 접촉일수록 R_p*↑ → 떼기 어려움 → 압밀 후 SE망
  결속(Luding Fig 2 인장강도와 같은 물리).

### 7.5 ★ 영구겹침 α_p = 우리 ε_sphere "displaced material" 규약 (LAW 근거 강화)

- `luding2008_*` §7.2: ε_sphere 규약("변위된 접촉물질은 bulge로 재출현 → solid=Σ원래 구부피")의 LAW 근거 =
  Luding δ₀. **Thornton–Ning은 같은 영구겹침을 *p_y 캡 + R_p* 제하 곡률*에서 물리적으로 유도**(eq28·29의 α_p).
- ⇒ ε_sphere가 ε_union보다 물리적인 이유의 **두 번째 독립 LAW 근거**: 영구겹침이 *경험 파라미터(Luding δ₀)*가
  아니라 *항복압·평탄화 반경에서 유도되는 실재*임을 Thornton–Ning이 보장. (δ₀ ↔ α_p는 같은 물리의 두 표기.)

### 7.6 frame[5] — 여전히 단일 접촉 LAW, SHAPE·morphology·전달은 우리 영역

- Thornton–Ning은 **단일 접촉의 per-contact 구성식**(층위1 CONTACT-LAW). **여전히 rigid 구**(α_p는 *접촉점
  국소 압흔 proxy*) → **입자 SHAPE 흐름·morphology·변형장·void-fill 전무** = Varkey/So와 *동일한 한계*.
  그건 우리 **MPM**(층위3 SHAPE).
- **전달 σ 전혀 없음**(충돌 COR LAW) → frame[5]의 역학(접촉 LAW) 절반만. σ_ionic/e/thermal 비교점 0 → 우리
  Kirchhoff/Holm 네트워크 영역.
- ⇒ 경로 A로 이 LAW를 도입해도 **frame[5] 분업은 유지**: DEM = 항복캡 접촉 + 전달, MPM = 형상소성·morphology·
  변형장. **18× 연화 제거**(real E + p_y 캡)는 *압밀 정확도*의 도약이지, MPM이 주는 형상소성을 DEM이 흡수하는
  게 아니다.

### 7.7 비교 요약표

| 항목 | 이 논문 (Thornton–Ning 1998) | 우리 | 차이 / 관계 |
|---|---|---|---|
| 접촉 LAW | **Hertz→p_y 항복→선형 소성(압 cap)→R_p* 제하** | LIGGGHTS `hooke/hysteresis`(Luding, **캡 없음**) | ★ TN이 **빠진 p_y 캡**을 가짐 = 경로 A의 LAW |
| 항복 캡 | **p_y = 2E*a_y/(πR*)** (eq9) | **없음** → 18× E-연화로 보상 | ★ 우리 연화의 *물리적 대체물* |
| 소성 분기 | **선형, 기울기 k_N=πR*p_y**(물리) (eq19·22) | k₂(δ−δ₀) 선형, 기울기 경험적 | TN은 압을 p_y로 cap; Luding은 캡 없음 |
| 영구겹침 | **α_p** (R_p* 제하서 유도, eq28·29) | δ₀=(1−k₁/k₂)δ_max (경험) / ε_sphere | 같은 물리; TN은 *물리적 유도*(ε_sphere LAW 근거 2) |
| 점착 | **JKR**(Γ, P_c=3/2πΓR*, plastic pull-off) | k_c 선형(Luding) / MPM `--coh` | TN이 점착의 *엄밀 이론판* |
| Varkey 2026 관계 | **Varkey base 접촉 LAW = 이것** (+F_mc) | (우리가 경로 A로 도입 시 동일 base) | Varkey 신규성은 multi-contact만 |
| So 2021 관계 | p_y 캡(Hertz 기반) | (So H-cap = H 기반 같은 발상) | 둘 다 "압을 σ_y의 1.6–3배서 cap" |
| 소성 종류 | **CONTACT-LAW**(층위1), rigid 구 | DEM도 CONTACT; SHAPE는 MPM | **같은 한계**(SHAPE 없음) — frame[5] |
| 전달 σ | **없음**(충돌 LAW) | σ_ionic+σ_e+σ_thermal 삼중항 | 우리 전달 우위 |
| morphology/변형장 | 없음(rigid 구) | MPM 진짜 형상변화·Σdg | 우리 MPM 보강 |
| 소재 | **소재 무관**(p_y·Γ 일반) | LPSCl/NMC811 | 절대값 전이 불가; LPSCl σ_y→p_y로 적용 |
| 제어변수 | **충돌속도**(동역학) | 압력(준정적 압밀) | 우리는 LAW만 차용, COR식은 직접 안 씀 |

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **★ 경로 A의 LAW 사양으로 직접 사용**: real E_SE=24 GPa + Thornton–Ning 4단계(eq2→9→19→29)를 LIGGGHTS에
  (또는 LIGGGHTS hysteretic/EEPA에 p_y 캡 추가) → **18× 연화 없이** 300 MPa porosity 재현 시험. p_y는 LPSCl
  σ_y(0.05–0.30 GPa)에서 ≈1.6σ_y로 설정. **So 2021이 H-cap으로 LPS 상대밀도 0.98 달성 = 선례**. →
  `elasto_plastic_feasibility.md §1 경로 A` 의 LAW 근거. `docs/data/thorntonning1998_*.csv`에 4단계 식·파라미터.
- ② **Stage-E 적용 조건 정밀화**: Stage-E(Tabor+volume, 접촉압≈H 가정)는 **α>α_y(항복 후)에서만 물리적**.
  Thornton–Ning이 항복 시점(p_y 도달)을 줌 → 접촉별로 *항복 여부(local 압 vs p_y)* 게이팅하면 탄성 접촉의
  H-과대 보정. 우리 300 MPa-press와 LPSCl p_y(0.08–0.48 GPa)가 같은 자릿수라 **부분-항복 접촉이 실재** →
  게이팅 가치 있음.
- ③ **JKR 점착 = SE-SE cohesion/`--coh` 매핑 기준**: Thornton–Ning JKR(Γ, P_c, plastic pull-off P_cr=3/2πΓR_p*,
  점착이 p_y 낮춤 eq65)을 우리 `adhesionStiffness`(k_c) ↔ Γ 변환·MPM `--coh`(backlog A3) 검증의 *물리 기준*으로.
- ④ **Varkey 비교연구의 base 정렬**: 경로 A로 이 LAW를 도입하면 Varkey와 *동일 접촉 LAW* → Varkey가 한
  multi-contact F_mc(ρ>0.7 과강성 보정)를 우리 18× 연화와 직접 비교 가능(같은 base 위에서). Varkey FEM 검증
  (TN 단독은 고밀도 under-stiff)이 "경로 A에 F_mc 보강 필요"를 시사.
- ⑤ **σ_y→p_y 민감도(Fig 10)를 MPM과 교차검증**: Thornton–Ning Fig 10이 p_y(=σ_y) 효과를 명시 → 경로 A의
  porosity가 σ_y에 민감할 것. **우리 MPM champion σ_y(2D 0.15 / 3D 0.30 GPa)와 정합**(frame[4]: 각각 실험
  보정 → 일치 시 교차검증). DEM 경로 A의 p_y와 MPM σ_y가 같은 LPSCl 실험을 가리켜야 함.

## 9. 인용 가능 문장 (deck/paper용)

- "The normal contact in our path-A elasto-plastic DEM follows Thornton & Ning (1998): Hertzian elastic
  loading up to a yield onset where the mean contact pressure reaches a limiting value p_y, a *linear*
  plastic branch P=P_y+π·p_y·R*(α−α_y) with the contact pressure capped at p_y, and elastic unloading
  along a Hertzian curve with an enlarged radius R_p* that leaves a residual (plastic) overlap."
- "This is precisely the yield-pressure cap that our current hooke/hysteresis law (Luding 2008) lacks —
  a piecewise-linear hysteretic branch without a hardness/p_y limit — which is why we soften E_SE 18×
  (24→1.35 GPa); adding the Thornton–Ning p_y cap lets the contact deform realistically at the *real*
  E_SE, removing the empirical softening (the same route So 2021 demonstrated with an H-based cap)."
- "Varkey et al. (2026) use the Thornton–Ning law as their base contact model and add only a stress-based
  multi-contact term; adopting it on our side aligns our DEM with that state-of-the-art base while
  retaining our MPM shape-plasticity and σ-triad (the half Varkey, So and Thornton–Ning all defer)."
- "The residual plastic overlap α_p that Thornton–Ning derive from the p_y cap and the flattened
  unloading radius R_p* is the physical basis for our material-conserving ε_sphere porosity convention —
  the displaced contact material persists as a permanent indentation, not lost volume."
- "Thornton & Ning also give the adhesive elastic-plastic case (JKR + p_y cap): adhesion lowers the
  limiting pressure (p_y,adh = 2E*a_y/πR* − (2ΓE*/πa_y)^(1/2)) and raises the pull-off force with impact
  severity (P_cr = 3/2·πΓR_p*) — the rigorous version of our SE-SE cohesion (LIGGGHTS adhesionStiffness /
  MPM --coh)."

## 10. 주의/한계 (over-claim 방지)

- **소재 데이터 없음 = 절대값 전이 불가.** LAW 논문 — LPSCl·NMC811 σ·porosity·강도 절대값 없음. p_y=0.5–3.04
  GPa·Γ=0.2–0.4 J/m²는 *워크드 예시(금속급)*. **우리 압밀 절대값과 직접 비교 금지** — 가치는 *수식·항복 캡
  구조·정성거동·LAW 근거*.
- **목적은 COR(충돌 반발계수)이지 압밀이 아니다.** 제어변수는 *충돌속도*(동역학), 우리는 *압력*(준정적).
  우리가 차용하는 건 **법선 접촉 LAW(4단계+JKR)**이지 COR 분석식(eq44/46/57/78–81)이 아니다. (COR식은 LAW의
  검증·예시.)
- **rigid 구 + CONTACT 소성만**(층위1). 입자 SHAPE 흐름·morphology·변형장 전무 — Varkey/So와 동일, 우리 MPM
  영역. α_p는 *접촉점 압흔 proxy*이지 입자 변형 아님.
- **전달 σ 전혀 없음**(역학 전용) → frame[5] 역학 절반만. σ_ionic/e/thermal 비교점 0.
- **탄성-완전소성(elastic-perfectly plastic) 가정** — 경화(work-hardening) 없음. 실 LPSCl 경화는 별도(Varkey
  HARD_SE / MPM HARD_SE로). 균일 p_y 압분포는 FEA 근사(Hardy et al.[8] 인용; 중심 elastic enclave 무시).
- **점착 EP는 가산 소산 근사**(eq78): 소성·점착 일이 분리 가능하다는 *가정*(해석해 불가하므로). 정확한 결합은
  Fichman–Pnueli[11]가 복잡해 미사용. → 우리 끈끈+무른 SE의 정밀 거동은 수치(MPM/DEM)로 확인 필요.
- **경로 A에 TN *단독*은 고밀도서 under-stiff 가능**: Varkey FEM 검증(varkey SI Fig S1)이 "Thornton–Ning
  단독은 ρ>0.7서 FEM을 UNDER-predict, multi-contact F_mc가 보정"을 보임 → 경로 A가 18× 연화를 완전히 없앨지는
  **LPSCl @300 MPa 재현으로 미검증**(강하게 동기부여되나, F_mc 보강이 필요할 수 있음).
- **p_y↔σ_y 환산은 근사**(p_y≈1.6σ_y 항복개시 / H≈3σ_y 완전소성). 우리 압밀 접촉이 부분-항복이면 어느 쪽도
  단일 상수가 아님 → 경로 A 보정 시 Fig 10식 p_y 민감도를 직접 sweep 권장.

## Supplementary Information

**없음** (SI 없는 본문 9쪽 단독 논문; 사용자 지시: PDF만 복사, SI 없음).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
