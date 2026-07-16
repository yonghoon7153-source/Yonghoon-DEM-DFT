<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. depth 기준 = bazzoun2026 + luding2008 + thorntonning1998 -->
# EEPA 점착 탄소성 접촉모델 (면적의존 점착) — 응집 분말의 미시역학 — Thakur (Granular Matter 2014)

> slug `thakur2014_eepa_adhesive_elastoplastic_dem` · DOI `10.1007/s10035-014-0506-4` · type `DEM (contact-LAW theory + uniaxial calibration)` · PDF `Thakur_2014_GranularMatter_EEPA_AdhesiveElastoPlasticContact.pdf` · digested `2026-06-26` · status ✅
> ★★ **WISHLIST Tier-2 #19 = EEPA(Edinburgh Elasto-Plastic Adhesion) 접촉모델의 *원전 정의서*.** LIGGGHTS/EDEM 표준 점착 탄소성 접촉법칙. 우리 모델(Luding 2008 `hooke/hysteresis`, `papers/luding2008_*`)과 경로 A(Thornton–Ning 1998, `papers/thorntonning1998_*`) 사이에 위치하는 **제3의 접촉 LAW** — 두 모델의 합집합(이력+소성겹침 from Luding) + **면적의존 점착(area-dependent adhesion)이라는 고유 기능**.
> ★ **핵심 위치**: EEPA = (Luding 이력 선형 + δ_p 소성겹침) + **k_adh·δⁿ 점착 항이 소성 접촉면적과 함께 성장**. 우리 SE-SE cold-weld/cohesion(LIGGGHTS `adhesionStiffness` / MPM `--coh`, backlog A3) + Stage-E 소성 *접촉면적*의 직접 개념 다리.

---

## 0. 왜 이 논문이 우리에게 중요한가 (먼저 읽을 것)

우리 DEM 압밀은 LIGGGHTS `hooke/hysteresis`(= Luding 2008 eq6) 위에서 돌고, `coefficientAdhesionStiffness`(m7,
SE-SE=1e6)로 SE-SE 점착을 준다. **그 `adhesionStiffness` 항이 어느 LAW에서 왔는가**가 그동안 코드 주석 수준으로만
있었다. **Thakur 2014가 바로 그 점착 탄소성 접촉모델(EEPA)의 원전 정의서**다 — LIGGGHTS의 `pair_style gran model
... cohesion ...` / EDEM의 EEPA가 이 논문의 5-파라미터(k₁·k₂·k_adh·f₀·n) 법선 이력 + 면적의존 점착의 직접 구현이다.

이 digest가 *직접 해소/근거화*하는 세 가지:
1. **EEPA = 우리 접촉 LAW의 "점착 확장판"의 정의**: Luding(`papers/luding2008_*`)이 *법선 이력+소성겹침*의 원형이면,
   Thakur EEPA는 거기에 **면적의존 점착(load-dependent adhesion, k_adh)** + **상수 점착(f₀)**을 명시적으로 분리해
   추가한 LAW. 우리 `adhesionStiffness`가 그 k_adh에 대응.
2. **면적의존 점착 ↔ 우리 Stage-E 소성 *접촉면적***: EEPA의 점착력 f_min이 **소성 접촉면적(= δ_p, plastic overlap)과
   함께 성장**한다. 이것이 우리 Stage-E(Tabor+volume)가 계산하는 바로 그 *소성 접촉면적*에 점착을 묶는 발상 —
   "압밀이 깊어질수록 접촉이 더 끈끈해진다"의 물리 정의. (frame[5] 역학 절반의 핵심.)
3. **calibration 방법론(접촉 파라미터 → 벌크 항복강도/flow function)**: 이 논문 후반(§6–7)이 *접촉 소성 λ_p가
   어떻게 벌크 응집강도(unconfined yield strength)·flow function·porosity로 매핑되는지*를 미시역학으로 분해한다.
   **우리가 경로 A 항복캡을 LPSCl 벌크 거동에 보정할 때의 방법론 템플릿** (cross-ref So 2021 / 18× 연화 보정).

⚠ **단, 이 논문 소재는 석회석(limestone, ESKAL 500, PARDEM 참조 분말)이지 LPSCl/NMC811이 아니다.** 응력범위도
**16–96 kPa**(우리 300 MPa의 ~1/3000 — 분말 *handling/silo* 스케일이지 *배터리 압밀* 스케일이 아님). 가치는 **(a)
EEPA LAW 정의, (b) 면적의존 점착 발상, (c) 접촉→벌크 calibration 방법론**이며 **절대값(porosity·σ_u) 전이는 불가**.

---

## 1. 한 줄 요약

응집 분말(0.1–10 µm, 점착성)의 **응력이력 의존 응집강도**를 정량 예측하기 위해 **EEPA(Edinburgh Elasto-Plastic
Adhesion) 접촉모델**을 제안: 법선은 **비선형/선형 이력 스프링**(초기재하 k₁·δⁿ, 제하/재하 k₂(δⁿ−δ_pⁿ)) + **소성겹침
δ_p**(이력) + **점착**(상수 f₀ + **면적의존** −k_adh·δⁿ). 이 LAW로 일축 압밀→무구속 압축 파괴를 시뮬레이션해
석회석 분말의 **flow function(무구속 압축강도 vs 사전압밀응력)을 실험과 ~12 % 이내로 재현**. **접촉 소성(λ_p=1−k₁/k₂)이
응력이력 의존성의 근원**임을 미시역학으로 증명: λ_p↑ → 제하 시 탄성복원↓ → 압밀 porosity↓ → 배위수 Z↑ → 응집강도↑.
정규화 무구속강도가 **(1−η_c)·Z에 선형(Rumpf 모델, R²=0.94)**으로 collapse. **= 우리 `adhesionStiffness`의 원전 LAW +
면적의존 점착의 정의 + 접촉소성→벌크강도 calibration 방법론.**

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Subhash C. Thakur, John P. Morrissey, Jin Sun, J.F. Chen, Jin Y. Ooi** (School of Engineering, **The University of Edinburgh**, King's Buildings, EH9 3JL; J.F. Chen는 Queen's Univ. Belfast) | **Granular Matter 16(3) 383–400 (2014)**; Received 2013-06-29, Published online 2014-05-21; © Springer-Verlag Berlin Heidelberg 2014 | **10.1007/s10035-014-0506-4** | **소재 무관 — 일반 응집 분말.** 참조 고체 = **석회석 ESKAL 500**(KSL Staubtechnik, 평균 4.7 µm), PARDEM(유럽 분말 연구망) reference solid. **LPSCl/NMC811 직접 데이터 없음** | **DEM 접촉 LAW 이론**(EEPA 제안) + **일축시험 calibration**(EDEM v2.4, N=2200/10000) + 미시역학 분해 |

> ★ **EEPA의 원전**: 이 논문이 "Edinburgh Elasto-Plastic Adhesion" 모델의 *제안 논문*. Edinburgh Powder Tester(EPT)
> 와 결합된 calibration 방법론이 함께 제시됨. 이후 LIGGGHTS·EDEM·Rocky에 표준 점착 탄소성 접촉으로 포팅됨.
> Thakur의 동반 논문(Particuology 12, 2–12 (2014), ref[45]) = packing/compression/caking 실험·시뮬 짝.
> 비선형(n>1) 버전은 별도 논문(ref[54], Morrissey PhD 2013)에 — 이 논문은 **선형(n=1)만** 본격 다룸.

## 3. 핵심 물성 (수치)

> ⚠ **이 논문은 소재 측정값 논문이 아니라 LAW+방법론 논문**이다. 아래 "수치"는 (a) EEPA 모델 파라미터(Table 1),
> (b) 석회석 calibration 결과, (c) 미시역학 무차원 관계. **LPSCl·NMC811 절대값 전이 불가**(소재 다름 + 응력 16–96
> kPa = 우리 300 MPa의 1/3000). 가치는 **수식·파라미터 정의·면적의존 점착·calibration 방법론**이다.

| 물성/파라미터 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **k₁ (loading stiffness)** | **1 kN/m** | Table 1 고정 | stated | 초기(처녀)재하 강성 — 가장 무른 가지 |
| **k₂ (un/reloading stiffness)** | **1, 1.25, 2, 5, 10, 100 kN/m** | Table 1 sweep | stated | k₂/k₁=1..100; 제하·재하 가파른 가지 |
| **k_adh (adhesive stiffness)** | **0.1–100 kN/m** | Table 1 sweep | stated | ★ **면적의존 점착** −k_adh·δⁿ |
| **f₀ (상수 점착, 첫 접촉)** | **−0.002 ~ −0.05 N** | Table 1 sweep | stated | van der Waals형 pull-off (load-무관) |
| **n (비선형 지수)** | **1** (이 연구) / >1 (동반논문) | Table 1 | stated | n=1 → piece-wise 선형 (Fig 1b); n>1 비선형 (Fig 1a) |
| porosity / 상대밀도 (fill, no-adh) | **41 %** | f₀=0, k_adh=0, aspect 1.5 | stated | vs 36 % mono 구(frictionless) — *형상* 효과 5%p |
| porosity (fill, high-adh) | **~72–75 %** | f₀ 0.1 N 또는 k_adh 1e5 N/m | digitized(Fig16) | 점착→사슬구조→ porosity↑ |
| consolidated porosity η_c | **~35–47 %** | σ₁ 20–100 kPa | digitized(Fig18) | 응력↑→η_c↓; 점착↑→η_c↑ |
| **σ_u (무구속 항복강도)** | **~2.3 → ~5.6 kPa** | σ₁=16→96 kPa | digitized(Fig8) | flow function; 실험 ~12 % 이내 일치 |
| σ_u COV (수치산포) | **3.4 %** | 3 random seeds @100 kPa | stated | 무작위 패킹의 벌크 영향 작음 |
| coverage / 접촉면적% | **n/a** (명시 출력 없음) | — | — | 접촉면적은 λ_p·δ_p로 *간접* — 직접 % 안 줌 |
| **coordination Z (peak)** | Fig15: **Z≈7–9.5** (peak 부근) | 모든 λ_p·σ₁ | stated | σ_u·d²/f₀ vs Z 단일 critical curve로 collapse |
| **E_SE / σ_y / ν** | **소재값 없음** (k는 모듈러스 직접환산 불가) | ν_pp=0.3 | — | EEPA k₁/k₂는 접촉강성(kN/m), 벌크 E 아님 |
| Heckel P_y / knee | **n/a** (Heckel 분석 안 함) | — | — | 압밀은 η_c vs σ₁(Fig13/18)로 보고 |
| PSD | **단일** ESKAL 500 (4.7 µm 평균) | Fig 2 SEM | stated | mono에 가까움; bi/poly-PSD 아님 |
| 입자형상 | **paired sphere(2구), aspect 1.5** | Fig 3 | stated | ★ 단일 구 아님 — 형상interlocking으로 벌크마찰 |
| 벌크마찰 포화 | **~0.8** (mono 구) / **~1.9** (aspect 1.5) | 직접전단 | stated | 형상이 벌크마찰 결정 — sliding μ는 ~0.8서 포화 |

## 4. 시뮬레이션 방법 ★ — **이것이 EEPA 접촉 LAW의 정의**

> 이 논문 §2가 **EEPA 법선·접선 접촉 LAW의 정의**, §3–4가 calibration·셋업, §5–7이 결과·미시역학.

- **code / version**: **EDEM® v2.4 (DEM Solutions Ltd, Edinburgh) — API로 EEPA 구현**. (이후 후속 버전·LIGGGHTS·Rocky
  포팅.) 시간적분 Newton (eq 1: `m_i d²x_i/dt² = f_i + m_i g`; eq 2: `I_i dω_i/dt = T_i`; eq 3: `T_i = Σ l_i^c × f_i^c`).
  timestep = Rayleigh time step의 <10 % (8×10⁻⁷–2×10⁻⁶ s).

- **DEM 접촉법칙 (법선)** — ★★★ **§2.2 = EEPA 본체** (Fig 1a 비선형 / 1b 선형):
  - **5개 파라미터로 4개 가지 정의** (Fig 1): **k₁**(virgin loading), **k₂**(un/reloading), **f₀**(상수 점착),
    **k_adh**(점착 강성), **n**(비선형 지수).
  - **★ 법선 힘 = 이력 스프링 + 점성댐핑** (eq 4): `f_n = (f_hys + f_nd)·u`, u=접촉점→입자중심 단위법선.
  - **★★★ 이력 스프링 f_hys (eq 5) — 우리 점착 모델의 본체** (3개 가지):
    ```
              ┌ f₀ + k₁·δⁿ              if  k₂(δⁿ − δ_pⁿ) ≥ k₁·δⁿ        (처녀 재하 loading, 기울기 k₁)
    f_hys =   ┤ f₀ + k₂(δⁿ − δ_pⁿ)      if  k₁·δⁿ > k₂(δⁿ−δ_pⁿ) > −k_adh·δⁿ (제하/재하 un/reloading, 기울기 k₂)
              └ f₀ − k_adh·δⁿ           if  −k_adh·δⁿ ≥ k₂(δⁿ − δ_pⁿ)      (점착 분기 adhesive/tensile, 기울기 −k_adh)
    ```
    - **k₁ (virgin loading stiffness)**: 첫 압축(처녀 재하)을 따르는 가장 무른 가지. 힘이 최대재하력에 도달할 때까지
      이 선을 따라 상승.
    - **k₂ (un/reloading stiffness)**: 제하·재하 가파른 가지. **이 가지가 0을 만나는 overlap = δ_p(소성겹침)**.
      재하 시 k₂를 따라 올라가다 처녀 k₁ 선에 닿으면 다시 k₁로 전환.
    - **δ_p (plastic overlap)**: ★ **영구 소성겹침**. k₂ 제하 가지가 힘=0을 만나는 overlap. **제하해도 δ가 0으로
      안 돌아가고 δ_p만큼 영구히 겹친 채 남음** = "압흔이 남는다" = **우리 ε_sphere "displaced material"**. (Luding δ₀와
      같은 물리; EEPA는 δ_p로 표기.)
    - **f₀ (constant adhesion at first contact)**: ★ **상수(load-무관) 점착** = van der Waals형 pull-off. 첫 접촉
      순간(δ=0)부터 −|f₀|의 인력이 항상 작용(Fig 1의 원점 아래 f₀ 절편). **소성 이력과 무관한 점착 성분.**
    - **k_adh (adhesive stiffness)**: ★★ **면적의존(load-dependent) 점착 가지 −k_adh·δⁿ의 기울기.** 제하가 δ_p
      아래로 가면 **인장력(음수)** 발생. **이 점착은 δ(= 소성 접촉면적 대용)와 함께 성장** → "더 깊이 압밀된 접촉이
      더 끈끈하다." (=논문 핵심 신규성; §4.1·§7.)
    - **n (nonlinear index parameter)**: 모든 가지의 δⁿ 지수. **n=1 → 전 가지 선형**(Fig 1b, 이 연구 본체) →
      Luding/Walton류 piece-wise 선형과 등가. **n>1 → 비선형**(Fig 1a, AFM의 fumed silica·titania 매끈 비선형 거동
      재현; 동반논문 ref[54]). 이 논문은 **k₂·k_adh·f₀ 효과 연구를 위해 n=1 고정**.
  - **★ 최대 인력(점착 바닥) f_min**: 점착 가지의 최저점 = `f₀ − k_adh·δ_min^n` (Fig 1의 δ_min 위치). **δ_p가
    클수록(깊은 소성) f_min이 더 음수** → 면적의존 점착이 곧 "소성겹침↑ → pull-off↑". 이 점 아래로 더 가면 힘·점착
    모두 감소하다 분리(δ=0).
  - **점착 분기 reload의 무한 k₂ 경로**: 점착 가지에서 재하하면 (첫 제하점에 따라) *무수한 k₂ 경로* 중 하나를 따라
    올라가 처녀 k₁ 선에 닿을 때까지 → 닿으면 추가 재하는 k₁ 따름. δ_min 아래의 이력은 미모델(Tomas 모델과 차이).
  - **★ k₁=k₂ → 탄성 극한**: k₁을 k₂와 같게 두면 EEPA가 **순수 탄성 접촉**으로 환원(소성겹침 0). 즉 이력모델이
    탄성을 특수경우로 포함. (우리 SE/AM은 k₂>k₁ → 완전 이력.)
  - **법선 댐핑** (eq 6·7): `f_nd = β_n·v_n`, `β_n = √(4m*k₁/(1+(π/ln e)²))`. v_n=법선 상대속도, m*=환산질량,
    e=반발계수(입력). **★ 댐핑이 k₁ 기반**(loading stiffness) — 주의.

- **★★ 항복압/경도 캡은 *없다* (Luding과 같은 한계, Thornton–Ning과 다름):** EEPA는 **소성 분기(k₁→k₂)와 영구겹침
  (δ_p)은 가지지만, 접촉 평균압이 항복압 p_y(또는 경도 H)에 도달하면 압을 cap하는 메커니즘이 *없다*.** 소성은 *강성
  비(k₁/k₂)로 정의된 이력*일 뿐, *접촉압 천장*이 아니다. ⇒ **EEPA ⊂ Luding 계열(캡 없음)**, Thornton–Ning(p_y 캡)·
  So(H 캡)와 **다른 층위**. (이것이 §7 비교의 핵심 — 아래.)

- **접선 접촉법칙 (§2.2 후반)**:
  - **접선력** (eq 8): `f_t = f_ts + f_td` (스프링 + 댐핑).
  - **접선 스프링** (eq 9·10, 증분): `f_ts = f_ts(n−1) + Δf_ts`, `Δf_ts = −k_t·δ_t`. **k_t = 2/7·k₁** (Walton–Braun
    [23] 고정값).
  - **접선 댐핑** (eq 11·12): `f_td = −β_t·v_t`, `β_t = √(4m*k_t/(1+(π/ln e)²))`.
  - **★ Coulomb 한계(점착 보정)** (eq 13): `f_ct ≤ μ·|f_hys + k_adh·δⁿ − f₀|`. **점착력이 마찰 한계에 더해짐** —
    인장 점착(−k_adhδⁿ+f₀)을 법선력에 보태 한계마찰을 키움. **이 점착-마찰 결합이 벌크 무구속강도에 큰 영향**(§7,
    Fig 22: 마찰한계에서 점착항을 빼면 무구속강도 급감·파괴모드 변함).
  - **구름저항** (eq 14): `τ_i = −μ_r·|f_hys|·R_i·ω_i` (EDEM 기본 rolling). μ_r=0.001(거의 무시).

- **재료 파라미터 (Table 1)**: N=2200(또는 10000), ρ=10000 kg/m³(density-scaled), **e=0.4**, k₁=1 kN/m,
  k₂∈{1,1.25,2,5,10,100}, k_adh 0.1–100, f₀ −0.002~−0.05 N, **μ_sf=0.5**(정마찰), **μ_rf=0.001**(구름), μ_pf=0.1(platen),
  wall μ=0(무마찰 측벽), wall G=10¹⁰ N/m², **ν_pp=0.3 / ν_pw=0.25**, Δt 8e-7~2e-6 s.
- **bond/binder 모델**: **없음**(바인더 미모델 — 점착은 f₀·k_adh로 통합). 입자-기하(벽/platen) 상호작용은 Hertz–Mindlin
  no-slip(점착 없음).
- **MPM / continuum**: **없음**(순수 이산 DEM). → frame[5] 역학 절반.
- **전달 솔버**: **없음**(σ_ionic/e/thermal 전혀 안 다룸). → frame[5]에서 **역학 절반만** 소유.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **★ 비구형 = paired sphere(2구 겹침, aspect 1.5)** (Fig 3) — **단일 구가 아님!** (Luding·Thornton–Ning은 단일 구.)
    근거: (i) 정확한 형상 불요 — *충분한 형상interlocking으로 벌크마찰 생성*되면 됨 [67]; (ii) mono 구는 벌크마찰이
    sliding μ=2.0서도 ~0.8 포화, aspect 1.5 paired는 ~1.9까지 도달 [68]. multi-sphere 기법[42].
  - **단일 ESKAL 500 PSD** (4.7 µm 평균) — mono에 가까움; **bi/poly-PSD 아님**.
  - **★ rigid paired-sphere + CONTACT 탄소성** (eq 5의 k₁→k₂ 소성분기 + δ_p 영구겹침) — **진짜 SHAPE 소성 아님.**
    paired-sphere의 *형상 자체*는 절대 안 변하고(두 구는 강체 결합 유지), "소성"은 **접촉점 힘-변위 LAW의 분기 +
    잔류 overlap**일 뿐. ⇒ `elasto_plastic_feasibility.md §0` 층위(1) CONTACT-LAW (층위(3) SHAPE는 우리 MPM).
- **도메인/RVE / servo / seeds / 압력범위**: 일축 압밀 mould **15 mm 지름**(EPT 원본의 ~1/3 스케일, 비용절감). 3단계
  (Fig 4): (a) random rainfall 충전(fill) → (b) 상부 platen으로 일축 압밀(strain rate ≈0.2 s⁻¹)·제하·mould 제거 →
  (c) 무구속 압축 파괴(2 mm/s ≈0.1 s⁻¹). **3 random seeds**(sample 1/2/3, N=2200) + 1 large(N=10000)로 산포 평가.
  inertial number I<10⁻⁴ (준정적). **압밀응력 16/36/56/76/96 kPa** (5 level).
- **특이사항/튜닝**: density scaling으로 준정적 가속. k₁은 "과한 overlap 막되 너무 stiff 안 하게"(timestep·실험
  loading 응답 절충) 선택. **k₂/k₁·k_adh·f₀를 *독립 변수*로 sweep**해 미시역학 분해(§6–7).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1 (★★★ 핵심)** | **EEPA 법선 힘-변위 LAW.** (a) 비선형(n>1): k₁δⁿ(재하)·k₂(δⁿ−δ_pⁿ)(제하/재하)·−k_adhδⁿ(점착)·δ_p(소성겹침)·δ_max·δ_min. (b) 선형(n=1): 같은 가지 직선화, f₀ 절편 명시 | **우리 `adhesionStiffness`(k_adh) + 소성겹침(δ_p)의 정의 그림.** Luding Fig1과 직접 대조: Luding엔 f₀(상수 점착)·k_adh 분리가 *불명시*, EEPA가 **상수 점착 f₀ vs 면적의존 점착 k_adh를 명시 분리**. 슬라이드/논문 method에 인용 |
| **2** | ESKAL 500 석회석 SEM (4.7 µm, 불규칙 형상) | 참조 분말의 *실제* 형상(비구형) — paired-sphere 근사의 동기. 우리 SE/NMC 형상도 비구형이나 우리는 구+overlap |
| **3** | paired particle (aspect 1.5, 두 1 mm 구 겹침) | **형상interlocking 근사** — 단일 구의 한계(벌크마찰 못 줌)를 2구로 보완. 우리는 구+rolling friction으로 비구형 흉내(다른 처방) |
| **4** | 일축시험 3단계: (a)재하 (b)제하 (c)무구속 압축 | EPT 일축 calibration 프로토콜. 우리 servo/hold 압밀과 대비(우리는 mould 안 제거, 압력 직접) |
| **5/6** | 압밀(σ_a-ε_a, Fig5)·무구속(Fig6) 응력-변형, 3 seeds + N=10000 | **수치산포 작음**(σ_u COV 3.4 %). random 패킹이 벌크에 minor. 우리 multi-seed 산포 논의와 정성 일치 |
| **7** | 무구속 σ_a-ε_a, σ₁=16/36/56/76/96 kPa | **사전압밀응력↑ → 무구속강도↑ + 초기강성↑** = 응력이력 의존성. flow function의 raw 곡선 |
| **8 (★)** | **flow function: σ_u vs σ₁** — 제안 EEPA(파랑 ●) vs 실험(빈 ○) vs modified-JKR(빨강 ■) | ★★ **EEPA는 실험과 ~12 % 이내**; **JKR(탄성 점착)은 너무 평탄 → 응력이력 못 잡음.** = "탄성 점착모델로는 응집분말 안 됨, 접촉 소성이 필수"의 증거. 우리 SE 압밀 응력의존성도 소성이 필요함의 방증 |
| **9** | (a) 선형 EP 접촉(상수 점착) 모식 f_u-δ (b) 압밀 σ_a-ε_a 모식 | λ_p·λ_b 정의용 도식 (δ_p, ε_p 표시) |
| **10 (★)** | **flow function vs 접촉소성 λ_p** (k₁/k₂로 유도, k_adh=0) | ★ **λ_p↑ → flow function 기울기↑(응집강도↑).** λ_p=0(탄성)이면 거의 평탄(응력이력 없음). **접촉 소성이 응집강도의 source** = 우리 18× 연화/항복캡이 노리는 바로 그 물리 |
| **11** | 벌크소성 λ_b vs 접촉소성 λ_p (σ₁별) | λ_p↑→λ_b↑. **λ_p=0(탄성)도 λ_b는 큼**(재배열). → 벌크소성만으론 응력이력 설명 못 함, *접촉* 소성이 결정 |
| **12** | 압밀 σ_a-ε_a, λ_p=0/0.5/0.99 | λ_p↑→ 초기 porosity↑(클러스터링) → 더 무른 재하. **소성↑인데 더 무름**(역설) = 큰 초기 porosity 탓 |
| **13** | 압밀 porosity η vs ε_a, λ_p=0.99 | 압밀곡선; 저응력서 porosity 큰 차→ 고응력서 수렴(~5 kPa) |
| **14 (★)** | **무구속강도 σ_u vs 압밀 porosity η_c**, λ_p별 | ★ η_c↓ → σ_u↑ (토양역학 압밀과 유사). **단 porosity만으론 부족**(λ_p<0.8서 선은 unique하나 그 이상 수렴) → Z가 추가 변수 |
| **15 (★★)** | **정규화 σ_u·d²/f₀ + Z vs 순간 배위수 Z_i** — 모든 λ_p·σ₁ collapse | ★★ **단일 'critical curve'** (토양역학 critical state 유사). **상수 점착(k_adh=0)서 응집강도 증가 메커니즘 = 압밀응력·접촉소성에 의한 *접촉 수(Z) 증가*.** = 우리 percolation/coordination Z 논의의 정량 근거 |
| **16 (★)** | **fill porosity η_f vs k_adh(상축)·f₀(하축)** | ★ **점착↑ → fill porosity↑**(사슬구조). no-adhesion 41 % → 강점착 ~72–75 %. **f₀와 k_adh가 *다른* 곡선**(f₀=점착력 N, k_adh=점착강성 N/m 직접비교 어려움) |
| **17** | 입자간 힘비 f_at/f_g vs fill porosity | f₀·k_adh 무관하게 *동원 점착력/중력비* vs porosity 단일선 collapse — porosity는 동원 점착력에 의존 |
| **18** | 압밀 porosity η_c vs σ₁, k_adh·f₀별 | 점착↑→η_c↑. **k_adh는 f₀보다 *느리게* 감소**(점착력 ∝ k_adh, 고응력서 더 커 압축 저항) |
| **19** | flow function σ_u vs σ₁, k_adh·f₀별 | **σ_u(f₀,k_adh) ≈ σ_u(f₀)+σ_u(k_adh)** (가산적). f₀ 케이스는 Z 증가만, k_adh는 Z+면적의존점착 둘 다 |
| **20** | Mohr 원(일축 인장·압축) | σ_u=(1+sinφ)/(1−sinφ)·σ_t (eq19) 유도 도식 |
| **21 (★★)** | **정규화 σ_u·d²/f_atp vs Z·(1−η_c)** — 모든 점착 파라미터, **R²=0.94 선형** | ★★ **Rumpf 모델 collapse**: 벌크 무구속강도 = 접촉 점착력 f_atp × 배위수 Z × 고체분율(1−η_c)의 선형함수. **미시(접촉 점착·Z·porosity) → 거시(응집강도) 통일 관계** = 우리가 접촉 파라미터→벌크 강도 매핑할 때의 *방법론 핵심* |
| **22** | 무구속 σ_a-ε_a, 마찰한계에 점착항 포함/제외 | **마찰 한계에서 점착항을 빼면 무구속강도 급감 + 파괴모드 변함**(전단파괴). eq13 점착-마찰 결합의 중요성 |

## 6. Post-processing ★

- **무엇**:
  - **flow function**: σ_u(무구속 압축강도) vs σ₁(사전압밀응력) — Jenike[2] 분류. 실험(EPT) vs 시뮬 비교(Fig 8).
  - **접촉 소성 λ_p = δ_p/δ = 1 − k₁/k₂** (선형 n=1; eq 16) + **벌크 소성 λ_b = ε_p/ε** (eq 17) 분해.
  - **배위수 Z** (peak·순간 Z_i), **porosity** (fill η_f / consolidated η_c). Heckel·percolation·coverage·
    tortuosity·전달지표 — **전부 안 함**(역학·강도 전용).
  - **★ Rumpf 미시역학 분해**: 인장강도 `σ_t = F_at·(1−η)·Z/(π·d²)` (eq 18, Rumpf 1962; F_at=접촉 점착력, η=porosity,
    Z=배위수). 무구속 압축 = `σ_u=(1+sinφ)/(1−sinφ)·σ_t` (eq 19, Mohr). → **정규화 `σ_u·d²/f_atp ∝ (1−η_c)·Z`**
    (eq 20) — R²=0.94 collapse (Fig 21). 응력텐서로 거시응력 산출.
- **도구**: EDEM v2.4 (상용) + API. 실험은 **Edinburgh Powder Tester (EPT)** — 반자동 일축시험기(stress-strain·
  porosity·peak 무구속강도), 재현성 COV <7 % [45,54].
- **수치화·플롯·기록 방식**: 접촉 파라미터 sweep(k₂/k₁ 1–100, k_adh 0.1–100, f₀ 0.002–0.05) → 각각 flow function·
  η·Z 산출 → 정규화(σ_u·d²/f₀ 또는 /f_atp) collapse. 무차원 critical curve(Fig 15)·Rumpf 선형(Fig 21)로 통일.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★★ **이 절이 핵심.** EEPA = 우리 `adhesionStiffness`의 원전 LAW + 면적의존 점착의 정의 + 접촉소성→벌크 calibration
> 방법론. "대비"는 곧 **(가) EEPA vs 우리 모델(Luding) vs 경로 A(Thornton–Ning) 3-way + (나) 면적의존 점착 ↔ Stage-E/
> cohesion 다리 + (다) calibration 방법론 + (라) frame[5] 분업**이다.

### 7.1 ★★★ 3-way 접촉 LAW 비교 — EEPA vs Luding(우리 모델) vs Thornton–Ning(경로 A)

세 LAW는 **"점착 탄소성 법선 접촉"의 세 변종**이다. 핵심 축 = **(i) 항복압 캡 유무, (ii) 점착의 종류**.

| 축 | **Luding 2008 (우리 현재 모델)** | **Thakur 2014 EEPA (이 논문)** | **Thornton–Ning 1998 (경로 A)** |
|---|---|---|---|
| **초기 재하** | k₁·δ (선형) | **k₁·δⁿ** (n=1 선형 / n>1 비선형) | (4/3)E*R*^½·α^1.5 = **Hertz** |
| **제하/재하** | k₂(δ−δ₀), k₂∈[k₁,k̂₂] δ_max 의존 보간 | **k₂(δⁿ−δ_pⁿ)**, k₂ 고정값(또는 무한경로) | (4/3)E*R_p*^½(α−α_p)^1.5 = **Hertz, 큰 반경** |
| **소성 분기** | k₁→k₂ 선형 (캡 압 **없음**) | k₁→k₂ 선형 (캡 압 **없음**) | **P_y+πp_y·R*(α−α_y)** 선형, **압을 p_y로 cap** ★ |
| **항복압/경도 캡** | ✗ **없음** | ✗ **없음** | ✅ **p_y 캡** (eq9, k_N=πR*p_y) |
| **영구 소성겹침** | δ₀=(1−k₁/k₂)δ_max (경험) | **δ_p** (이력변수; λ_p=1−k₁/k₂) | α_p (p_y·R_p*에서 *유도*) |
| **점착 — 상수** | −k_c·δ (상수 점착, *분리 안 됨*) | **f₀** (상수 pull-off, **명시 분리**) ★ | (JKR로 통합) |
| **점착 — 면적의존** | (k_c·δ가 δ와 함께 크나 *소성면적* 개념 불명시) | **−k_adh·δⁿ** (= **소성겹침과 함께 성장**) ★★ | JKR plastic pull-off P_cr=3/2πΓR_p* (R_p*↑) |
| **점착 이론기반** | 선형 k_c (경험) | 선형 k_adh + f₀ (경험, 분리) | **JKR 표면에너지 Γ** (물리) |
| **n 비선형** | 선형 only (Walton 비선형은 단순화함) | **n 파라미터로 선형↔비선형 전환** ★ | Hertz(재하)·소성(선형) — n 없음 |
| **마찰-점착 결합** | μˢ(fⁿ+k_c·δ) | μ·|f_hys+k_adh·δⁿ−f₀| (eq13) | (별도) |
| **LIGGGHTS 가용** | ✅ `hooke/hysteresis` (우리 사용) | ✅ EEPA (cohesion 모델; LIGGGHTS/EDEM 표준) | (직접 pair_style 없음 — 커스텀/Varkey=Rocky) |
| **소재** | 일반 µm 분말 | **석회석**(16–96 kPa) | 일반 EP 구(충돌 COR) |

⇒ **3-way 위치 정리**:
- **Luding ⊂ EEPA(거의)**: EEPA의 **법선 이력(k₁·k₂·δ_p)은 Luding eq6과 사실상 동형**. EEPA가 추가한 것 = **(1)
  상수 점착 f₀를 면적의존 점착 k_adh와 *명시 분리*, (2) 비선형 지수 n, (3) 마찰한계에 점착 명시 포함(eq13).** 즉
  **EEPA ≈ Luding + (f₀/k_adh 분리 + n + eq13)**. 우리 LIGGGHTS `hooke/hysteresis`+`adhesionStiffness`가 *실질적으로
  EEPA의 선형(n=1) 부분집합*을 쓰고 있다.
- **EEPA ≠ Thornton–Ning**: **둘 다 점착 탄소성이지만 EEPA엔 *항복압 캡이 없다*.** EEPA 소성 = 강성비(k₁/k₂)로 정의된
  *이력*; Thornton–Ning 소성 = 접촉압이 p_y에 *고정*되는 *물리적 항복*. ⇒ **EEPA는 Luding과 같은 "캡 없는" 층위**,
  Thornton–Ning(경로 A)·So(H-cap)와 다른 층위. **따라서 EEPA를 도입해도 우리 18× 연화 문제는 *해결 안 됨*** (EEPA도
  real E_SE 24 GPa로는 300 MPa서 under-deform). 경로 A의 *항복캡*이 그 역할.
  - ⚠ **중요 정정 — EEPA는 "경로 A"가 아니다**: 사용자 seed가 "EEPA = path A 후보"라 했으나, 정확히는 **EEPA = 우리
    현재 Luding 모델의 *점착 명시판*(같은 캡-없음 층위)**이지, *항복캡을 더하는* 경로 A가 아니다. 경로 A의 캡은
    Thornton–Ning(p_y)/So(H)가 제공. **EEPA의 가치는 "경로 A 후보"가 아니라 "면적의존 점착 LAW의 정의 + calibration
    방법론"**이다. (다만 EEPA에 *p_y/H 캡을 더하면* 경로 A의 *점착 포함* 완성형이 됨 — §7.5.)

### 7.2 ★★ 면적의존 점착(k_adh·δⁿ) ↔ 우리 Stage-E 소성 *접촉면적* + SE-SE cohesion

EEPA의 **고유 신규성 = 점착력 f_min이 소성 접촉면적과 함께 성장**(−k_adh·δⁿ, δ가 깊을수록·δ_p가 클수록 더 끈끈).
이것이 우리 두 곳과 직접 연결:

1. **★ Stage-E 소성 *접촉면적* (frame[5] 역학 절반):** 우리 Stage-E(Tabor+volume)가 계산하는 것이 바로 *소성
   접촉면적* A_physics(`network_conductivity.py`). **EEPA는 그 *같은 소성 접촉면적에 점착을 묶는다*** — "압밀이
   깊어질수록(δ_p↑) 접촉면적↑ → 점착력↑." 우리는 그 소성면적을 *전달*(σ_ionic, Holm R=1/(2σr_c))에 쓰고, EEPA는
   *점착/강도*에 쓴다. **같은 물리량(소성 접촉면적)의 두 용도** = 개념 다리. → 만약 우리가 SE-SE 점착을 *면적의존*으로
   만들고 싶으면(현재 `adhesionStiffness`는 k_adh·δ로 이미 δ-의존이나 *소성면적*과 명시 연결은 안 됨) EEPA가 그
   정의를 준다.
2. **★ SE-SE cold-weld/vdW cohesion (backlog A3):** 우리 LIGGGHTS `coefficientAdhesionStiffness`(SE-SE 1e6 = AM의
   10×) = **EEPA의 k_adh에 직접 대응**(면적의존 점착). + 우리엔 *상수* f₀ 슬롯이 명시적으로 없는데, **EEPA가 f₀(상수
   vdW pull-off)와 k_adh(면적의존 cold-weld)를 분리**해 — SE의 *vdW 점착(f₀)* vs *압밀로 생기는 cold-weld(k_adh)*를
   따로 줄 수 있음을 시사. **MPM `--coh`**(연속체 SE attractive σ, backlog A3) = 같은 점착의 연속체판; EEPA가 그
   점착의 *이산·면적의존 정의*(f₀+k_adh)와 정성거동(Fig 16: 점착↑→fill porosity↑·사슬구조; Fig 18: 점착↑→압밀
   porosity↑)을 제공 → `--coh`/`adhesionStiffness` 매핑·검증 기준.
3. **★ Coulomb 한계에 점착 포함 (eq 13)**: EEPA는 마찰 한계 μ·|f_hys+k_adh·δⁿ−f₀|에 점착을 더한다 — Fig 22가
   "점착항을 빼면 무구속강도 급감·전단파괴 모드"를 보임. 우리 SE-SE 점착도 마찰 한계에 기여(LIGGGHTS 동일 처리) →
   압밀 후 시료 결속·전단저항의 근거.

### 7.3 ★ Calibration 방법론 (접촉 파라미터 → 벌크 항복강도/flow function) — 우리 경로 A 보정의 템플릿

이 논문 후반(§6–7)이 **접촉 파라미터를 벌크 거동에 보정하는 방법론**의 정석:
- **접촉 소성 λ_p = 1−k₁/k₂가 응집강도의 source** (Fig 10): λ_p↑ → flow function 기울기↑. λ_p=0(탄성)이면 응력이력
  거의 없음. ⇒ **"접촉에 소성이 있어야 응집분말의 응력이력이 재현된다"** — 우리 SE 압밀 응력의존성도 (단순 탄성이
  아니라) 소성 접촉이 필요함의 방증. (단 EEPA λ_p는 *강성비* 소성이지 *항복압* 소성이 아님 — §7.1.)
- **★ Rumpf collapse (eq 18·20, Fig 21, R²=0.94)**: `σ_u·d²/f_atp ∝ (1−η_c)·Z`. **거시 응집강도 = f(접촉 점착력
  f_atp, 배위수 Z, 고체분율 1−η_c)**. → **우리가 경로 A 항복캡을 LPSCl 벌크 거동(porosity·강도)에 보정할 때 같은
  분해를 쓸 수 있다**: 접촉 파라미터(p_y, k_adh) sweep → η_c·Z 산출 → 벌크 강도/porosity collapse. So 2021(`so2021_*`)
  H-cap을 LPS 상대밀도 0.98에 맞춘 것 + 우리 18× 연화를 300 MPa porosity에 맞춘 것이 *같은 방법론*(접촉→벌크 보정)의
  사례 — EEPA가 그 *체계적 분해*(Rumpf·critical curve)를 제공.
- **EPT calibration 프로토콜** (Fig 4): fill→consolidate→unconfined의 3단계로 *각 응력에서* flow function 측정 →
  실험과 직접 비교. 우리 압밀(servo/hold)과 다르나(우리는 mould 유지·압력 직접), *접촉 파라미터를 벌크 측정에 맞추는*
  루프 구조는 동일. ⚠ **단 응력범위 16–96 kPa**(handling)이지 우리 300 MPa(배터리)가 아님 — 방법론만 차용, 절대값 X.
- **JKR(탄성 점착)으로는 안 됨** (Fig 8): modified-JKR(EDEM 2.4, 탄성)은 flow function이 너무 평탄 → 응력이력 못
  잡음. ⇒ **응집분말 calibration엔 접촉 소성이 필수.** (우리가 hooke/hysteresis = 소성 이력을 쓰는 정당화; 순수 탄성
  Hertz로는 압밀 응력의존성 부족.)

### 7.4 ★ 면적의존 점착이 porosity를 *올린다* — 우리 SE 압밀과 방향 주의

- EEPA: **점착↑ → fill porosity↑**(Fig 16: 41 %→~72–75 %, 사슬구조·클러스터링)이고 **압밀 porosity도 ↑**(Fig 18).
  점착이 입자를 붙여 *느슨한* 구조 형성·중력 저항·재배열 억제.
- ⚠ **우리 SE-SE 점착(adhesionStiffness 1e6)의 효과는 다른 맥락**: 우리는 *충전*이 아니라 *300 MPa 압밀 후*를 보고,
  점착이 *압밀 후 시료 결속*(전단저항·인장강도)에 기여하지 *느슨하게* 만들지 않는다(고압이 사슬구조를 무너뜨림).
  CLAUDE.md scaffold `--coh` sweep 결과: **점착이 wallP는 바꾸나 porosity는 안 바꿈**(porosity는 wall_z/jamming
  기하로 고정). ⇒ **EEPA Fig 16/18의 "점착→porosity↑"는 *저응력 충전/handling* 현상**이지 우리 *고압 압밀* 현상이
  아님. 방법론·LAW는 차용하되 이 *정성거동*은 응력범위 차이로 직접 전이 금지.
- **단 critical curve(Fig 15)·Rumpf(Fig 21)는 응력범위 무관 가능성**: "응집강도 ∝ Z·(1−η_c)"는 *기하·접촉* 관계라
  고압서도 형태 유지 기대(우리 percolation/coordination Z 논의와 정합 — 더 많은 접촉 → 더 강함). 이건 차용 가치.

### 7.5 ★ EEPA + 항복캡 = 경로 A의 *점착 포함* 완성형 (LIGGGHTS 단순 경로)

- `elasto_plastic_feasibility.md` 경로 A(항복캡 DEM)는 **Luding/EEPA의 선형 이력에 p_y(또는 H) 캡을 더하는 것**.
  EEPA는 *선형 기반*(n=1)이라 **LIGGGHTS에서 p_y/H 캡을 얹기 더 단순**(Luding과 같은 장점) + **이미 점착(f₀·k_adh)을
  내장** → "real E_SE + p_y 캡 + 면적의존 점착"의 *점착 포함 경로 A*를 EEPA 위에 바로 구성 가능.
- ⇒ **권장 구성**: EEPA(LIGGGHTS cohesion, f₀+k_adh) **+ Thornton–Ning/So의 p_y 캡** → real E_SE=24 GPa로 18× 연화
  없이 300 MPa 압밀 + SE-SE 면적의존 cold-weld. (Varkey 2026은 Thornton–Ning+multi-contact를 Rocky로; 우리는
  EEPA+p_y캡을 LIGGGHTS로 — 둘 다 *접촉소성+점착* 같은 목표.)
- ⚠ **단 — frame[5] 불변**: EEPA+캡을 넣어도 **입자 SHAPE 흐름·morphology·변형장은 여전히 못 줌**(δ_p·δ는 *접촉점
  기하 proxy*, paired-sphere 형상도 강체). 그건 MPM 영역. 18× 연화 제거는 *압밀 정확도* 도약이지 MPM 형상소성 흡수가
  아님.

### 7.6 frame[5] — rigid(paired) 구 + CONTACT 소성 + 점착, SHAPE·morphology·전달은 우리 영역

- EEPA는 **단일/paired 접촉의 per-contact 구성식**(층위1 CONTACT-LAW) + 점착. **여전히 rigid 구**(paired-sphere
  형상도 고정; δ_p는 접촉점 압흔 proxy) → **입자 SHAPE 흐름·morphology·변형장·void-fill 전무** = Luding/Thornton–Ning/
  Varkey/So와 *동일한 한계*. 그건 우리 **MPM**(층위3 SHAPE; champion J2 E=1.53/σ_y=0.15, SEM 코어보존+경계평탄화 ✓).
- **전달 σ 전혀 없음**(역학·강도 LAW) → frame[5]의 역학(접촉 LAW) 절반만. σ_ionic/e/thermal 비교점 0 → 우리
  Kirchhoff/Holm 네트워크 영역. EEPA의 면적의존 점착 *접촉면적*은 우리 Stage-E 면적과 *물리량은 같으나* EEPA는 그걸
  점착에, 우리는 전달에 씀(상보).

### 7.7 비교 요약표

| 항목 | 이 논문 (Thakur 2014 EEPA) | 우리 | 차이 / 관계 |
|---|---|---|---|
| 접촉 LAW | **EEPA 점착 탄소성 이력**(k₁·k₂·f₀·k_adh·n) | LIGGGHTS `hooke/hysteresis`+`adhesionStiffness` (= EEPA n=1 부분집합) | **거의 동형 LAW** — 우리가 EEPA 선형판 사용 |
| 점착 — 상수 f₀ | **명시 분리** (vdW pull-off) | 명시 슬롯 없음(k_c·δ에 통합) | ★ EEPA가 f₀ 분리 — SE vdW vs cold-weld 구분 시사 |
| 점착 — 면적의존 k_adh | **−k_adh·δⁿ, 소성겹침과 성장** | `adhesionStiffness`(SE 1e6) | **1:1 대응** ✓ — k_adh = 우리 m7 |
| 소성겹침 | **δ_p** (λ_p=1−k₁/k₂) | ε_sphere "displaced material" / m8 plasticityDepth | **같은 물리** ✓ |
| 항복압/경도 캡 | ✗ **없음** (Luding과 같은 층위) | ✗ 없음 → 18× 연화 보상 | ★ EEPA ≠ 경로 A — 캡은 Thornton–Ning/So가 줌 |
| 비선형 지수 n | **있음** (n=1 선형 / n>1 비선형) | 없음(선형 hooke) | EEPA가 AFM 비선형 옵션 추가 |
| calibration | **flow function·Rumpf collapse(R²=0.94)·critical curve** | 18× 연화(porosity) / Stage-E(전달) | ★ EEPA = 접촉→벌크 강도 보정 방법론 템플릿 |
| 소성 종류 | **CONTACT-LAW**(층위1) — rigid (paired) 구 | DEM도 CONTACT; SHAPE는 MPM | **같은 한계**(SHAPE 없음) — frame[5] |
| 입자형상 | **paired-sphere(aspect 1.5)** | 구+rolling friction | 둘 다 비구형 *근사*(다른 처방) |
| 전달 σ | **전혀 없음**(역학·강도) | σ_ionic+σ_e+σ_thermal 삼중항 | 우리 전달 우위(frame[5]) |
| morphology/변형장 | 없음(rigid 구) | MPM 진짜 형상변화·Σdg | 우리 MPM 보강 |
| 소재·응력 | **석회석, 16–96 kPa**(handling) | LPSCl/NMC811, 300 MPa(배터리) | **절대값 전이 불가**(소재+응력 1/3000) — LAW·방법론만 |
| 차원 | 3D (mould 15 mm, N=2200/10000) | 3D DEM | (둘 다 3D) |

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **★ `adhesionStiffness`의 원전 LAW citation**: "우리 SE-SE 점착은 Thakur et al.(2014)의 EEPA(Edinburgh
  Elasto-Plastic Adhesion) 접촉모델의 면적의존 점착 항(−k_adh·δⁿ)을 LIGGGHTS `coefficientAdhesionStiffness`로
  구현" — method/SI에 인용. EEPA가 f₀(상수)·k_adh(면적의존)를 분리함을 명시.
- ② **★ 면적의존 점착 ↔ Stage-E 소성면적 다리**: "EEPA는 점착을 *소성 접촉면적*에 묶는다(f_min=f₀−k_adhδ_minⁿ,
  δ_p와 성장) — 우리 Stage-E(Tabor+volume)가 *전달*에 쓰는 그 같은 소성 접촉면적이다. 같은 물리량의 두 용도(점착 vs
  σ_ionic)." → frame[5] 역학/전달 상보의 구체 예. (§7.2)
- ③ **★ calibration 방법론 (경로 A 보정 템플릿)**: EEPA의 Rumpf collapse(σ_u·d²/f_atp ∝ (1−η_c)·Z, R²=0.94) +
  critical curve(σ_u·d²/f₀ vs Z)를 우리 *경로 A 항복캡 LPSCl 보정*에 차용 — 접촉 파라미터(p_y, k_adh) sweep →
  η_c·Z 산출 → 벌크 강도/porosity collapse. So 2021·18× 연화와 같은 *접촉→벌크* 루프의 체계화. (§7.3)
- ④ **★ SE 점착 f₀ vs k_adh 분리 도입 검토**: EEPA가 *상수 vdW(f₀)* vs *압밀로 생기는 cold-weld(k_adh)*를 분리 —
  우리 SE에 두 점착 성분을 따로 줄지 검토(현재는 k_adh만). MPM `--coh`(backlog A3) 도입 시 EEPA Fig 16/18 정성거동
  (단, *저응력 handling*임 주의 — §7.4)을 매핑 기준으로.
- ⑤ **EEPA+p_y캡 = LIGGGHTS 경로 A 점착포함 완성형**: EEPA(선형, 점착 내장) + Thornton–Ning/So p_y 캡 → real E_SE
  + 면적의존 cold-weld로 18× 연화 없는 압밀. Varkey(Rocky, Thornton–Ning+multi-contact)의 LIGGGHTS·점착 대응판.
  (§7.5; frame[5]는 불변 — 형상소성은 MPM.)

## 9. 인용 가능 문장 (deck/paper용)

- "우리 DEM의 SE-SE 점착은 Thakur et al.(2014, Granular Matter)의 EEPA(Edinburgh Elasto-Plastic Adhesion) 접촉모델 —
  법선 이력(초기재하 k₁·δⁿ, 제하/재하 k₂(δⁿ−δ_pⁿ)) + 상수 점착 f₀ + 면적의존 점착 −k_adh·δⁿ — 의 면적의존 항을
  LIGGGHTS `coefficientAdhesionStiffness`로 구현하며, EEPA가 분리한 f₀(상수 vdW)와 k_adh(소성면적 의존 cold-weld)에
  대응한다."
- "EEPA의 면적의존 점착력 f_min=f₀−k_adh·δ_minⁿ 은 소성 접촉면적(δ_p)과 함께 성장 — 우리 Stage-E(Tabor+volume)가
  전달(σ_ionic)에 쓰는 바로 그 소성 접촉면적이며, EEPA는 같은 면적을 점착/강도에, 우리는 전달에 쓰는 상보 관계다."
- "EEPA는 우리 hooke/hysteresis(Luding 2008)와 같은 *캡 없는* 층위의 점착 탄소성 LAW다 — 소성 분기(k₁→k₂, δ_p)는
  있으나 항복압 p_y 캡이 없어, real E_SE로는 우리 18× 연화 문제를 그대로 가진다. 항복캡(Thornton–Ning p_y / So H)을
  EEPA의 선형 이력 위에 더하는 것이 *점착 포함* 경로 A다."
- "Thakur et al.은 접촉 소성 λ_p=1−k₁/k₂가 응집분말 응력이력 의존성의 근원임을 보이고(탄성 JKR은 flow function이
  너무 평탄), 정규화 무구속강도가 (1−η_c)·Z에 선형(Rumpf, R²=0.94)으로 collapse함을 입증 — 접촉 파라미터를 벌크
  항복강도에 보정하는 우리 경로 A 보정의 방법론 템플릿이다."

## 10. 주의/한계 (over-claim 방지)

- **소재·응력 전이 불가 (이중 차이).** 소재 = **석회석(ESKAL 500)**이지 LPSCl/NMC811 아님 + 응력 = **16–96 kPa
  (handling/silo)**이지 우리 300 MPa(배터리 압밀)의 ~1/3000. **porosity(fill 41 %·~72–75 %, 압밀 35–47 %)·σ_u(2–6
  kPa) 절대값을 우리 압밀과 직접 비교 금지.** 가치는 **LAW 정의·면적의존 점착·calibration 방법론**.
- **★ EEPA는 "경로 A"가 아니다 (사용자 seed 정정).** EEPA = 우리 Luding 모델의 *점착 명시판*(같은 *캡 없음* 층위)
  이지, *항복캡을 더하는* 경로 A가 아니다. 경로 A의 캡은 Thornton–Ning(p_y)/So(H)가 제공. **EEPA 단독 도입으로는 18×
  연화가 해결되지 않는다.** (EEPA+p_y캡이라야 점착 포함 경로 A.)
- **rigid (paired) 구 + CONTACT 소성만**(층위1). 입자 SHAPE 흐름·morphology·변형장 전무 — paired-sphere 형상도
  강체. δ_p·δ는 *접촉점 기하 proxy*이지 입자 변형 아님. 우리 MPM 영역(frame[5]).
- **전달 σ 전혀 없음**(역학·강도 LAW) → frame[5] 역학 절반만. σ_ionic/e/thermal 비교점 0.
- **점착→porosity↑ 정성거동은 *저응력* 현상**(Fig 16/18). 우리 고압 압밀에선 점착이 porosity 안 바꿈(jamming
  기하로 고정; scaffold `--coh` sweep 확인). 이 정성거동 직접 전이 금지 — critical curve/Rumpf 기하관계만 차용.
- **n=1 선형만 본격 분석.** 비선형(n>1) 버전은 동반논문(ref[54]). 우리 hooke도 선형이라 정합하나, AFM 비선형 거동은
  이 논문 범위 밖.
- **paired-sphere ≠ 우리 구+rolling.** 비구형 *근사 처방*이 다름(EEPA=2구 형상interlocking, 우리=구+rolling
  friction). 벌크마찰 절대값(EEPA ~1.9 @aspect1.5) 직접 전이 금지.
- **k_adh·f₀ 직접 비교 어려움**(저자 명시): k_adh=점착 *강성*(N/m), f₀=점착 *력*(N) — Fig 16에서 다른 곡선. 우리
  `adhesionStiffness`(강성)와 매핑 시 단위 주의.
- **EDEM v2.4 상용 코드 산출.** LIGGGHTS EEPA 포팅이 *정확히* 같은 식인지(eq5·13·n 처리) 구현 검증 필요(특히 eq13
  점착-마찰 결합·n 지수).

## Supplementary Information

**없음** (사용자 지시: SI 없음, PDF만 복사). 본문 18쪽 자체가 완결. 비선형(n>1) 결과는 별도 논문 ref[54](Morrissey
PhD 2013); packing/compression/caking 실험 짝은 ref[45](Particuology 12, 2–12, 2014).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
