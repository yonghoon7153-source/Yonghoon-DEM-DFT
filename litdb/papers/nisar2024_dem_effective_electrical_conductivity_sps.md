<!-- digest: COMPREHENSIVE / paper-level STANDALONE. 읽으면 ≈ 논문 읽은 것. depth ref = bazzoun2026_dem_fem_rnm_ionic.md -->
# 부분소결 다공성 재료의 유효 전기전도도를 위한 DEM 저항망 모델 (sinter-neck conductance) — Nisar (Comp. Part. Mech. 2024)

> slug `nisar2024_dem_effective_electrical_conductivity_sps` · DOI `10.1007/s40571-024-00773-4` · type `DEM+RNM` · PDF `Nisar_2024_CompPartMech_DEM_EffectiveElectricalConductivity_SPS_Porous.pdf` · digested `2026-06-26` · status ✅ · OPEN ACCESS (CC-BY 4.0)

---

## 1. 한 줄 요약
**우리 σ_electronic Kirchhoff/Holm 솔버의 *방법론적 쌍둥이* (σ_ionic 쌍둥이가 Bazzoun이라면 이쪽은 σ_ELECTRONIC).**
입자중심을 노드로 하는 **DEM 저항망**으로 부분소결 다공성 재료의 유효 *전기*전도도 κ_eff(porosity)를 풀되, 우리의 **Holm 구속저항
R=1/(2σa) 대신** ⟶ **소결 NECK(목)의 기하 컨덕턴스**를 쓴다: neck 반경 a를 **부피보존 기준**(겹침 부피를 원통형 neck으로 재분배)으로
결정 + 고밀도 비물리 겹침을 보정하는 **GB(입계) 보정인자 α** + neck 내부 공극을 위한 **GB 저항(δ_gb, ε)**. SPS-소결 **다공성 NiAl**의
실측 σ로 검증(4점 탐침, 4 샘플 porosity 0.05–0.216) → GB 저항 추가 후 실험과 **근사 일치**. ⇒ 우리에게 (a) frame[4] σ_e 저항망 교차검증,
(b) 우리 ε_sphere 과압축/Stage-E *부피* 접촉면적의 **대안·교차검증 후보**(neck-volume-preservation), (c) 향후 *소결* 확장 시 직접 참조 스펙.
**단 — NiAl 금속 단상(no AM/SE/pore-3상), 전기-ONLY, 소결(고온 1100–1300 ℃) 체제 → 절대값·소재는 우리 LPSCl 냉간가압과 무관, 방법/추세만.**

---

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| F. Nisar, J. Rojek, S. Nosewicz, J. Szczepański (IPPT PAN, Warsaw) · K. Kaszyca, M. Chmielewski (Łukasiewicz IMiF, Warsaw) | Comput. Part. Mech. **11** (2024) 2191–2201 | 10.1007/s40571-024-00773-4 | **다공성 NiAl 금속간화합물** (단상; battery 아님) | **DEM 저항망(RNM) + SPS 실험 검증** |

- Received 16 Feb 2024 · Accepted 5 May 2024 · OPEN ACCESS (CC-BY 4.0).
- 펀딩: National Science Centre, Poland, 2019/35/B/ST8/03158.
- **계보 (중요):** 이 논문은 같은 그룹(Rojek/Nosewicz, IPPT PAN)의 **열전도 모델 [37] Nisar 2024 Powder Tech 437:119546**의 *전기* 버전이다.
  열-전기 유사성(thermal–electrical analogy)을 이용해 **열 neck 컨덕턴스 모델 [36] Rojek 2022 Powder Tech 405:117521**을 전기로 옮겼다.
  → 즉 **Rojek 2022(neck 컨덕턴스 정의) → Nisar 2024 Powder Tech(열 검증) → 이 논문(전기 검증)** 이라는 그룹-내부 진화. (우리 Bielefeld→Bazzoun 궤적과 같은 구조.)

---

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity (4 샘플) | **0.216 / 0.164 / 0.106 / 0.050** | SPS NiAl (Table 1) | stated | = 1 − ρ/ρ₀ (Archimedes) |
| κ_eff (exp, 4점탐침) | **4.33 / 6.14 / 7.44 / 8.77 × 10⁵ S/m** | 위 porosity 대응 | stated | porosity↑ → κ↓ (역관계) |
| κ_e (fully dense NiAl) | **9.8 × 10⁵ S/m** (=0.98 MS/m) | 이론밀도 재료 고유 | stated | 전달 정규화 기준 |
| ρ₀ (이론 벌크밀도) | **5910 kg/m³** (=5.90 g/cm³) | NiAl | stated | porosity 환산용 |
| neck 컨덕턴스 기울기 | **K_i/K_cyl = 1.08·(a/r_i)** | hemisphere/cylinder 정규화 | stated (eq19) | a=neck 반경, r_i=입자 반경 |
| GB 층 두께 δ_gb | **0.23 µm** (채택); SEM 측정 0.15–0.4 (단일 GB 0.36) | 보정 fitting param | stated (Fig5/Fig9) | neck 내 공극층 |
| GB 전도도 감쇠인자 ε | **0.16** (채택); 스캔범위 0.1–0.5 | 보정 fitting param | stated (Fig9) | κ_gb = ε·κ |
| 입경 PSD | **diameter 1.5–20 µm, max:min = 15** | real PSD | stated | heterogeneous |
| 초기/탭 밀도 | **65 %** | 중력낙하+벽수축 | stated | DEM 패킹 |
| 시료 형상 | **D=123.6 µm × H=202 µm 원통**, >17,000 입자 | DEM 도메인 | stated | |
| σ_ionic / σ_thermal / coverage / Z | **n/a** | — | — | 전기-ONLY (Z 분포는 neck-size 히스토그램으로 간접, Fig6) |
| E_SE / σ_y / ν | **n/a** (역학 파라미터 본 논문 미보고) | — | — | 소결은 별도 thermo-viscoelastic 모델 [43]로 (재료 파라미터 [43] 참조) |
| Heckel P_y / knee | **n/a** (소결, 냉간가압 압밀 아님) | — | — | |
| SPS 가압 | **5 또는 30 MPa** + 1100–1300 ℃ + 10 min | Table 1 | stated | ★ *소결* 압력 (우리 300 MPa 냉간가압과 차원 다름) |

> ⚠ **단위/체제 주의:** κ_eff 는 **10⁵–10⁶ S/m 급의 금속 전도도**(우리 LPSCl σ_ionic ~10⁻¹ mS/cm = 10⁻² S/m, σ_e ~수 mS/cm 와 *8~9자리* 차이).
> porosity 도 **5–22 %** 의 *소결된 dense 금속*(우리 냉간가압 복합 양극 10–18 %와 우연히 겹치나 *물리 기원이 다름* — 소결 neck 성장 vs 가압 재배열/소성).
> ⇒ **절대값은 절대 전이 금지. 방법·추세·neck-volume 아이디어만.**

---

## 4. 시뮬레이션 방법 ★
- **code / version**: **in-house DEM 프레임워크**(IPPT PAN; Rojek 그룹의 소결 DEM 코드 [36][43] 위에 전기 모듈 추가). 상용 아님.
  (cf. 우리 LIGGGHTS + `network_conductivity.py`; Bazzoun 의 LIGGGHTS+COMSOL+MATLAB.)
- **DEM 접촉법칙 / 압밀**: 이 논문은 *전기 모듈*이 본체. **미세구조(geometry)는 별도 *소결 시뮬레이션*에서 생성** — **thermo-viscoelastic
  소결 모델 [43] Nosewicz 2013/2017**(점탄성 입자 소결, dihedral angle·표면에너지·확산 enthalpy·열팽창 파라미터, 재료 파라미터는 [43]과 동일)으로
  hot-press(열간가압)를 시뮬 → 중간중간 멈춰 **여러 porosity의 대표 geometry**를 추출. ⟶ 즉 **압밀/소성 law 자체는 본 논문 범위 밖**(neck은
  소결로 *성장*하지 가압 overlap이 아니다). **입자는 구**, rigid (소결 neck만 별도 기하로 표현).
- **재료 파라미터**: 전달용 — 이론밀도 ρ₀=5910 kg/m³, 고유 κ_e=9.8×10⁵ S/m, 수치적 비용량 c=2×10⁶ F/kg(물리 무의미, 명시적
  Euler 적분 수렴용 가짜 capacitance). **역학 E·σ_y·ν 는 본문 미보고**(소결 파라미터 [43] 위임).
- **bond/binder 모델**: 없음 — **금속 단상**. neck = 소결 *융합*(bond) 그 자체가 컨덕턴스를 만든다(바인더 무관).
- **MPM/continuum**: **없음** (이 그룹은 DEM-only; 연속체 비교는 [20] FEM 열전도 인용으로 대체).
- **전달 솔버** ★ (= 우리 솔버와 *직접* 대응):
  - **노드 = 입자 중심, 가지(branch) = 저항.** **제1 Kirchhoff 법칙**: 노드 i 로 들어/나가는 전류 합 = 0
    `I_i = Σ_j I_ij − I_i^ext = 0` (eq1–2). Ohm `I_ij = (V_j − V_i)/R_ij = K_ij(V_j − V_i)` (eq3).
  - **전역 행렬식 `K·V = I`** (eq4); 외부전류 없으면 `K·V = 0`(eq5). **K(컨덕턴스 행렬) = FEM 강성행렬과 동형**(K singular →
    최소 1 노드에 전압 처방 필요). 처방/미지 분해 `[K_uu K_up; K_up^T K_pp]·{V_u;V_p}={I_u;I_p}` (eq7) → `K_uu·V_u = I_res` (eq8),
    `I_res = I_u − K_up·V_p` (eq9).
  - **풀이법 = 명시적 forward-Euler 반복**(transient pseudo-time): 대각 capacitance C_uu(eq11, C_i=m_i c_i) 도입 →
    `C_uu·V̇_u + K_uu·V_u = I_res` (eq10) → `C_uu·(V^{i+1}−V^i)/Δt = I_res − K_uu·V^i` (eq12) →
    `V^{i+1} = (𝓘 − Δt·C_uu⁻¹·K_uu)·V^i + Δt·C_uu⁻¹·I_res` (eq13). C_uu 대각이라 역행렬 trivial → 반복 1회가 싸다.
    **수렴지표** g_max^{i+1} = max_n |（V_n^{i+1}−V_n^i)/V_n^{i+1}| (eq14) ≤ tol **β = 2×10⁻⁴** (eq15). ~**40 iteration**, dt=5 µs.
    **부록 증명**: 이 forward-Euler 반복식(eq13)이 선형계 *반복해*와 동일하고, 안정성 조건 `Δt < 2C_ij/K_ij`(eq42–43)이 곧 수렴조건.
    (전기 전류흐름은 본질적으로 *정상상태* — transient는 솔버 가속 트릭일 뿐, "전기에서 transient response는 매우 짧아 무시 가능"이라 명시.)
  - ★ **컨덕턴스 = 직렬 3저항** (eq17): `R_ij = R_i + R_j + R_c` ⟶ `K_ij = K_i K_j K_c / (K_i K_j + K_j K_c + K_i K_c)` (eq18).
    - **R_i, R_j = 각 입자의 *hemisphere* 저항** (Rojek [36] 열 문제 기하 재사용): neck 위 반구 컨덕턴스 K_i 를
      그 반구를 감싸는 *원통*(반경·높이 r_i)의 컨덕턴스 `K_cyl = λ·πr_i²/r_i = λπr_i`(eq20)로 정규화 → **선형관계 K_i/K_cyl = 1.08·(a/r_i)** (eq19).
      (λ=열전도도를 전기 κ로 치환.) ⟶ **a(neck 반경)가 크면 입자저항 작다 = 컨덕턴스는 neck 크기가 지배.**
    - **R_c = 접촉(=neck 내부 GB) 저항** (eq26, §3.5): SEM(Fig2/Fig5)에서 **neck 안에도 공극이 남아** 추가저항을 준다 →
      neck을 두께 δ_gb 의 GB 층으로 보고 그 층의 전도도를 `κ_gb = ε·κ`로 감쇠 → `K_c = ε·κ·πa²/δ_gb`. **δ_gb, ε = 보정 fitting param.**
  - **neck 반경 a 결정 = 핵심 novelty** (§3.3–3.4):
    - 통상 **Coble 소결모델** `a = √(2 r* h)`, r*=2r_i r_j/(r_i+r_j)(effective radius), h=overlap (eq21) — **하지만 [36]에서
      Coble은 고밀도(큰 overlap)서 neck 과대평가** 라 명시. → **기각**.
    - 대신 **Rojek [36] 2-입자 소결 기하 + 부피보존 기준** 채택(Fig4): **overlap 부피가 원통형 neck 으로 재분배된다고 보고 부피보존으로
      a 계산.** (overlap 렌즈 부피 = neck 원통 부피 ⟶ a). ⟶ 우리 ε_sphere "변위된 접촉 재료가 bulge로 re-emerge"의 *neck 버전*.
  - **GB 보정인자 α (고밀도 비물리 겹침 보정)** ★ (§3.4): 소결 시뮬은 *2-입자* 상호작용만 보고 *다중접촉*을 무시 → 고밀도서 한 입자의
    neck들이 **합쳐 입자 표면을 초과**하는 비물리 발생. **grain-boundary fraction** `f_i^gbf = Σ_j S_ij^neck / S_i ≤ 1` (eq22–23)로 추적;
    위반 시 그 입자의 **모든 neck을 α_i 로 축소** `a_ij^corr = α_i·a_ij` (eq24), `α_i ≤ 2r_i/√(Σ a_ij²)` (eq25).
    ⟶ **우리 ε_sphere 음수(과압축)·Stage-E min(caps) 상한과 *정확히 같은 문제·다른 처방***(아래 §A·§B 상술).
- **입자 처리** ★ (DEM판 "무질서 처리"): **구만**, rigid. **mono-shape**(neck만 별도 기하). **진짜 SHAPE 소성 아님** — neck은 *소결 성장* 기하지
  입자 형상 자체가 변형장으로 흐르는 게 아니다. real **poly-PSD**(1.5–20 µm, 비율 15)로 *heterogeneity*는 충실. ⟶ Bazzoun/Varkey와 같은
  "구=타협" 계보(단 여기선 *소결 neck*을 명시 기하로 더해 점접촉보다 한 단계 물리적).
- **도메인/RVE / seeds / 압력범위**: 원통 D=123.6 µm × H=202 µm, >17,000 입자, 초기 65 %. 측면 절연(insulated wall), top V=3.5×10⁻⁵ V /
  bottom 0 V. **seed/실현 다수 여부 미명시**(샘플당 1 geometry로 보임). SPS: 5/30 MPa, 1100–1300 ℃.
- **특이사항/튜닝**: GB 파라미터 **2개(δ_gb, ε)를 Sample 3(porosity 0.106) 한 샘플에 보정 → 나머지 3개에 검증**(과적합 방지 정직).
  보정 map(Fig9) = δ_gb 0.1–0.3 µm × ε 0.1–0.5 격자에서 실험 오차밴드 안 조합 다수 → 그중 (0.23, 0.16) 채택.

---

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | Sample 1 SPS 온도·압력 profile(1200 ℃, 5 MPa, 60 min 사이클) | *소결* 공정 — 우리 냉간가압과 다른 체제임을 못 박는 그림 |
| **2** | **neck 내부 공극 SEM**(porosity 0.164): 입자 사이 neck + neck 안 *파단면 공극* | ★ **R_c(GB-within-neck) 도입 근거** = 우리 Stage-E "접촉도 완벽 dense 아님" 직관의 SEM 증거 |
| **3** | **저항망 모식**: 입자중심=노드, 가지=저항 직렬 `R_i—R_c—R_j`(eq17) | ★ = **우리 Holm/Kirchhoff 그림** 그 자체 (R_bulk+R_constriction 직렬) |
| **4** | **2-입자 neck 기하**(서로 다른 크기): a(neck 반경), h(overlap), 반구 반경·높이 r_i | ★ **neck-volume-preservation + K_i/K_cyl=1.08 a/r_i** 정의 그림 (§B 흡수 대상) |
| 5 | **소결 GB SEM**: (a) 다중 GB (b) 확대 측정 *단일 GB 두께 0.36 µm* | δ_gb 보정값(0.23)의 SEM 출처 — 우리 Cronau sub-µm GB 인자의 *측정* 짝 |
| **6** | **neck-size 분포 히스토그램**(porosity 0.05/0.106/0.164/0.216, a/r_min 정규화) | ★ porosity↓ → 분포 **우측 이동**(neck 성장) = 우리 coordination/coverage 분포의 σ_e 짝; **a/r_min 정규화 = 우리 a/r 비** |
| 7 | porosity 0.164 **수렴 해**: (a) 수렴지표 vs iter (b) 높이별 전위 수렴 (c) 최종 전위장(선형 구배) | 솔버 수렴 검증 방식 — 우리 CG/spsolve 수렴 체크의 forward-Euler 버전 |
| **8** | **κ_eff(porosity) — GB 저항 *없이*** vs 실험: 추세 맞으나 **일관 과대평가** | ★ "구속/GB 저항 빼면 σ 과대" = 우리 contact-free upper-bound σ_cf 와 *같은 논리* |
| 9 | **보정 map**: δ_gb × ε → κ_eff 등고선, 실험밴드 안 조합 | 2-파라미터 보정 + 과적합 방지(1샘플 보정·3샘플 검증) 방법론 |
| **10** | **κ_eff(porosity) — GB 저항 *포함*(ε=0.16, δ_gb=0.23)** vs 실험: **근사 일치** | ★ frame[4] **검증 완료** 그림 — neck-RNM + GB 저항이 실측 재현 |

---

## 6. Post-processing ★
- **무엇**: (a) **κ_eff = −I·L/(ΔV·A)** (eq28) — 원통 단면 A·높이 L 에 Ohm 법칙(전류 I = top/bottom 합산 I_top=ΣI_i (eq29), I_bottom (eq30),
  I=I_top=I_bottom (eq31)); (b) **neck-size 분포**(Fig6, a/r_min 히스토그램 = 소결 진행 척도); (c) **GB fraction f_i^gbf**(eq22) 추적·α 보정;
  (d) **SEM 형태분석**(neck 내 공극·GB 두께 측정, Hitachi S4100); (e) **2-파라미터 보정 map**(Fig9, 실험 오차밴드 confinement).
- **도구**: in-house DEM 코드(전기 모듈 + 소결 [43]), SEM(Hitachi S4100), 4점탐침(실험 σ).
- **수치화·플롯·기록 방식**: κ_eff–porosity를 4점으로(Fig8 GB-없음 / Fig10 GB-있음), 보정은 등고선 map(Fig9).
  **전기 transient는 솔버 가속용** — 실제 전류해는 정상상태(eq13 수렴값). **속도/효율 정량 비교(우리 RNM↔FEM 32–98× 같은 표)는 없음**(이 논문은 RNM 단독).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 네트워크 솔버 | 입자중심 노드 + Kirchhoff 1법칙 `Σ I_ij=0` (eq1) | 동일 Kirchhoff (`scripts/network_conductivity.py`, Laplacian L·V=b) | **같은 골격** ✓ |
| 가지 저항 구조 | **직렬 `R_ij=R_i+R_j+R_c`** (eq17) | **직렬 `R_total=R_bulk+R_constriction`** (network_conductivity:365) | **구조 동형** ✓ (이름만 hemisphere↔bulk, neck-GB↔constriction) |
| 입자 내부 저항 | hemisphere `K_i/K_cyl=1.08 a/r_i` (eq19, neck-크기 의존) | `R_bulk=(d/2)/(σπr²)` (실린더, hop 거리 의존) | **둘 다 입자체 저항**; 그들=neck 함수, 우리=거리 함수 |
| **접촉 저항 핵심** | **NECK 기하 컨덕턴스** `K_c=ε·κ·πa²/δ_gb` (소결 neck 단면) | **Holm 구속저항** `R=1/(2σa)` (Maxwell a-spot, eq Holm 1967) | ★ **근본 차이** — 소결 *목 단면 전도* vs 점접촉 *수렴(constriction)* (§A 상술) |
| neck/접촉 반경 a | **부피보존**(overlap 부피 → 원통 neck) | Hertz `a=√(R*δ)` / Stage-E 5-regime `min(caps)` (Tabor F/H·volume V/h·geom 2πR²) | ★ **둘 다 부피 보존 철학**; 그들=소결 neck, 우리=소성 contact-area (§B 상술) |
| 고밀도 비물리 겹침 보정 | **GB fraction α** `f_i^gbf=ΣS^neck/S_i≤1`, 위반 시 neck 축소 (eq22–25) | **ε_sphere 과압축 캡** + Stage-E `min(A_tabor,A_volume,A_geom)` 상한 + AM-shielding | ★ **같은 문제·다른 처방** (§A·§B 핵심) |
| GB(입계) 저항 | **δ_gb·ε 명시 보정**(neck 내 공극) | **Cronau(r_SE) σ_grain 인자**(sub-µm 비정질화, *재료* 물성) | 그들=*기하* neck 공극(fitting), 우리=*재료* GB(literature 고정) — 종류 다름 |
| 전달 채널 | **전기 σ_e ONLY** | **σ_ionic + σ_e + σ_thermal 삼중항** | ★ 우리 삼중항 우위 (§C) |
| 상(phase) 수 | **단상 금속(NiAl) + pore** | **AM(NCM) + SE(LPSCl) + pore 3상** | ★ 우리 battery-specific 우위 (§C) |
| 압밀/morphology | **소결 [43] 외부 위임**(neck 성장), 형상 안 변함 | DEM 압밀 + **MPM 진짜 소성 SHAPE flow** | ★ 우리 MPM morphology 우위 (§C) |
| 검증 | **실험 σ(4점탐침 SPS NiAl)** ✓ | solver=ground truth(외부 실측은 Bazzoun/Minnmann 차용) | 그들 NiAl 실측 = *방법* 검증 템플릿(소재는 무관) |
| 체제 | **소결**(1100–1300 ℃, 5/30 MPa), 금속 10⁵–10⁶ S/m | **냉간가압**(300 MPa, 상온), SE 10⁻² S/m | ★ **절대 비교 불가** — 방법·추세만 |

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) — neck-conductance RNM vs Kirchhoff + Holm CONSTRICTION
> **두 모델 다 "DEM 저항망으로 유효 전도도"** → *가장 직접적인 방법론 비교*. 핵심은 **가지 저항을 무엇으로 채우느냐**.

### A.1 전류해(solver) — 사실상 동일 (frame[4] 교차검증)
- **그들**: 노드=입자중심, `K·V=I`(eq4), Kirchhoff 1법칙(eq1) → 한 노드 전압 처방 → **forward-Euler pseudo-time 반복**(eq12–13)으로
  `K_uu V_u=I_res`(eq8)를 풂. 수렴 tol β=2×10⁻⁴, ~40 iter. **부록에서 이 반복=직접 선형해와 동치임 증명**(eq32–43).
- **우리** (`network_conductivity.py`): 동일하게 입자=노드, 접촉=edge, **그래프 Laplacian L·V=b** 를 **CG → ILU-CG → spsolve** 3단 robust 직접해.
  Dirichlet 전위 BC(전위 처방), 절연 경계.
- ⟶ **솔버 골격은 byte-수준으로 같은 물리**(Kirchhoff resistor network). 차이는 *수치 전략*뿐: 그들 명시적 반복(대각 C로 가속) vs 우리 직접 sparse solve.
  ★ **그들의 forward-Euler 반복은 우리 CG가 ill-conditioned 토폴로지서 mis-converge할 때의 *대안 솔버* 후보**(network_conductivity 의 spsolve-fallback 경고와
  같은 문제를 그들은 transient 반복으로 우회 — §B 흡수 후보 ④).

### A.2 가지 저항 — **근본 차이: 소결 NECK 단면 전도 vs 점접촉 CONSTRICTION**
- **그들 R_c = K_c = ε·κ·πa²/δ_gb** (eq26): neck을 **단면적 πa², 두께 δ_gb 의 작은 *원통 도체***로 본다 ⟶ **벌크 전도(bulk conduction through a slab)**.
  소결로 입자가 *융합*해 연속 금속 목이 생겼으므로 이게 맞다. a 가 크면 R_c 작다(πa²↑).
- **우리 R_constriction = 1/(2σa)** (Holm 1967, Maxwell a-spot): 두 반무한 도체가 *반경 a 의 작은 원판(a-spot)으로만 닿을 때* 전류선이 그
  a-spot으로 **수렴(constriction)**하며 생기는 저항 ⟶ **표면 수렴 저항(spreading/constriction resistance)**. a 가 크면 R↓ (1/a) 이나 *스케일링이 다르다*.
- ★ **어느 게 더 엄밀한가 (점접촉 한정)**:
  - **점접촉·a≪r (sintering 초기, 또는 우리 냉간가압 SE-SE 접촉)**: **Holm 구속저항 1/(2σa)이 더 엄밀하다.** 반무한체 가정의 Maxwell 해는
    a≪r 에서 *닫힌형 정답*. 그들 neck 모델은 a→0 에서 K_c=ε·κ·πa²/δ_gb → 0 (단면 사라짐)이지만 *δ_gb 가 분모에 고정*돼 있어 **얇은 slab 가정이 점접촉서 깨진다**.
  - **소결 후·a~r (큰 neck, 융합 목)**: 그들 neck-slab 이 더 맞다. constriction 저항은 a→r 에서 0 으로 가야 하는데(우리 Mikic `(1−a/r)^1.5` 보정이
    이걸 처리), Holm 본식은 그 saturation 이 없다. ⟶ **우리는 이걸 `contact_mode='physics'`의 Mikic 보정** `R=(1−a/r_min)^1.5/(2a)`
    (network_conductivity:347–349)로 처리 = 그들 neck-slab 과 *같은 saturation 방향*. 즉 **우리 physics 모드 = Holm(점접촉) + Mikic(목 saturation)** 이
    그들 neck 모델의 두 극한을 모두 커버. ★ **그들에게 없는 게 우리 Mikic 의 부드러운 보간**; 우리에게 없는 게 그들 *명시적 neck 단면 πa²/δ_gb*.
- **R_i 입자체 저항**: 그들 hemisphere `K_i/K_cyl=1.08 a/r_i`(neck-크기 의존, 반구 기하) vs 우리 실린더 `R_bulk=(d/2)/(σπr²)`(hop 거리 의존).
  둘 다 "입자 내부 전도"지만 그들은 *neck 함수로 입자체까지 묶고*(소결 기하), 우리는 *접촉 반경(a)과 입자체(r)를 분리*. **직렬 조립은 동일**(eq17↔R_total).

### A.3 고밀도 비물리 겹침 — **같은 문제, 평행한 처방** ★ (가장 흡수 가치 높은 칸)
- **그들 GB-α** (eq22–25): 소결이 진행돼 한 입자의 neck 합 면적이 입자 표면을 넘으면(`f_i^gbf>1`) 비물리 ⟶ 그 입자 *모든 neck 을 α_i 로 축소*.
  α_i ≤ 2r_i/√(Σa_ij²) — **표면 보존(surface budget)** 기준.
- **우리 ε_sphere 과압축 + Stage-E min(caps)**: 강체 구가 깊이 겹치면 ε_sphere(구 부피합)가 *음수*가 되거나 접촉면적이 비물리로 커짐 ⟶
  (i) **AM-shielding**(rigid AM 골격이 하중지지 → SE overlap 작게), (ii) **ε_union**(상한 sanity), (iii) **Stage-E A_physics =
  max(lower, min(A_tabor=F/H, A_volume=V/h_min, A_geom=2πR_min²))** (network_conductivity:240–264; CLAUDE.md) — **부피/경도/기하 상한으로 cap**.
- ★ **정확한 대응**: 그들 *α(표면예산 축소)* ↔ 우리 *A_geom=2πR_min²(기하 상한)* 가 **같은 역할**(접촉면적이 입자 표면을 못 넘게). 그들 *neck-volume*
  ↔ 우리 *A_volume=V/h_min*(부피보존 면적)이 **같은 철학**. ⟶ **두 모델이 독립적으로 "고밀도 over-compression을 부피/표면 보존으로 capping"** 하는 데 수렴 =
  frame[4] 방법론 교차검증. **우리 Stage-E 5-regime 이 그들 단일-α 보다 더 세분**(Tabor 소성 경도캡 H 추가)인 한편, **그들은 그걸 *neck 기하 한 식*으로 더 단순·일관**.

### A.4 검증 철학
- **그들**: GB 저항 *빼면* κ 과대(Fig8) → GB 저항 *넣으면* 실측 일치(Fig10). ⟶ **우리 contact-free upper-bound(σ_cf, R_constriction=0)** 가
  full(σ_full)보다 항상 큰 것과 *같은 논리*: "접촉/neck 저항을 빼면 이상화 상한, 넣으면 물리값". 그들 GB-저항 = 우리 constriction(+Stage-E) 의 역할.
- **그들은 *실측*으로 닫음**(NiAl 4점탐침); **우리 σ_e 는 solver=ground truth** + 외부 실측은 Bazzoun/Minnmann(σ_ionic)·Lee/Trevisanello(σ_e 재료) 차용.
  ⟶ ★ **그들의 "GB 없음=과대 → GB 있음=일치" 2단 검증이 우리 σ_e 검증의 *방법 템플릿*** (우리도 constriction 없음 σ_cf → 있음 σ_full → 실측 이 3단 가능).

---

## B. 적용가능성 (applicability to our model) — 구체적으로 무엇을, 어디에
> map 대상: `scripts/network_conductivity.py`(저항망·Stage-E 면적), `_film_area`(5-regime), σ_e Stage 22.5 폼.

- **① neck-volume-preservation 을 Stage-E *부피 접촉면적*의 대안/교차검증으로** ★ (1순위):
  - 우리 `A_volume = V_overlap / h_min`(network_conductivity:242) = "겹침 부피를 두께 h_min 으로 나눈 면적" — **이미 부피보존 철학**.
  - 그들 부피보존 neck = "겹침 부피를 *원통*으로 재분배 → a=√(V/πh)" 사실상 **같은 식의 다른 정규화**. ⟶ **`_film_area` 에 `A_neck_volpres` 한 줄
    추가**(겹침렌즈 부피 → 원통 neck 반경, Rojek [36] eq)해 **A_volume 과 교차검증**: 두 부피보존 면적이 일치하면 우리 Stage-E *volume* arm 이
    독립 재유도로 확증됨; 어긋나면 정규화 차이(h_min vs 원통 높이) 정량. **비용 거의 0**(δ, R 만 필요).
- **② GB fraction α 를 ε_sphere 과압축 *진단 게이지*로** ★:
  - 그들 `f_i^gbf = ΣS_ij^neck/S_i ≤ 1`(eq22)는 **입자별 "접촉이 표면을 얼마나 덮었나"** = 우리 *coverage* 의 *입자-국소* 버전.
    우리는 coverage 를 AM 표면 전역으로 보지만, **`f_i^gbf > 1` 위반 입자 카운트**를 ε_sphere 음수(과압축) 케이스의 *조기 경보*로 쓸 수 있다
    (CLAUDE.md "ε_sphere 음수 = 과압축 extreme"의 *입자-국소 진단*). → `network_conductivity` 의 per-contact 루프에 입자별 ΣA_contact/S_particle 집계 추가.
- **③ neck-slab R_c = ε·κ·πa²/δ_gb 를 *소결/cold-weld* 확장 시 직접 채택** ★ (So 2022 와 결합):
  - 우리 현재 SE-SE 접촉은 점접촉(Holm) — 하지만 **So 2022(MethodsX) 가 sintering fusion-bond** 를, **Lee2025 PTFE cold-weld** 를 지적.
    SE 가 *융합*(가압-소결 또는 cold-weld)하면 점접촉이 아니라 **neck-slab** 이 맞다. ⟶ **`contact_mode='sinter'` 새 분기**: a≳a_crit(융합 임계) 접촉은
    `R = δ_gb/(ε·σ·πa²)`(그들 eq26)로, 미만은 Holm — **두 체제 자동 전환**. δ_gb 는 우리 Cronau sub-µm GB 두께로, ε 는 Cronau(r_SE) 감쇠로 *재료 물성에서* 채워
    그들 *fitting* 을 우리 *literature-grounded* 로 대체(우리 강점 보존).
- **④ forward-Euler 반복 솔버 = ill-conditioned 토폴로지 fallback** :
  - `network_conductivity` 의 spsolve 가 `G_eff > 1.1·Σg` 비물리(line 667)로 mis-converge 하는 sparse-graph 가 있다. 그들 **대각-C forward-Euler 반복**(eq13)은
    *항상 수렴 보장*(부록 안정성 증명) → **3단 robust solve 의 4단째**(CG→ILU-CG→spsolve→forward-Euler-iter)로 추가 가능. β=2×10⁻⁴, Δt<2C/K(eq43) 그대로.
- **⑤ 검증 템플릿 = "구속/GB 없음 → 있음 → 실측" 3단** :
  - 그들 Fig8(GB 없음, 과대) → Fig10(GB 있음, 일치) 2단을 우리 σ_e 에 적용: **σ_cf(constriction=0, 상한) → σ_full(Holm+Stage-E) → Bazzoun/Lee 실측** 3점을
    한 plot 에 → 우리 Stage-E 기여폭을 그들식으로 시각화(우리 이미 σ_full/σ_cf/σ_bulk 3모드 보유 — line 11–12).
- **⑥ neck-size 분포(Fig6) = σ_e 의 coordination/coverage 분포 짝** :
  - 그들 a/r_min 히스토그램이 porosity↓ 로 우측 이동(neck 성장) = 우리 *coverage_AM 분포·am_am_cn 분포* 가 압밀↑ 로 우측 이동하는 것과 같은 진단.
    → σ_e Ridge/폼의 구조 descriptor(am_am_cn, √A_AM-AM) 가 *분포 1-모멘트* 만 쓰는데, **분포 폭(std)도** 그들처럼 보면 sparse-AM(고-CAM) 과소예측 진단에 도움.

> ⚠ **흡수 시 절대 주의**: 그들 δ_gb·ε 는 *소결 NiAl* 의 fitting 값(0.23 µm, 0.16) — **우리 LPSCl 로 숫자 전이 금지**. 채택하는 건 *식의 구조*(neck-volume, α, neck-slab)지
> *값*이 아니다. 값은 우리 Cronau/literature 로 채운다. 또 그들 체제는 *소결*(neck 융합) — 우리 *냉간가압*(점접촉 + cold-weld)엔 ③의 자동 전환이 필수.

---

## C. ★ 우리 novelty — 왜 우리가 state-of-the-art 인가 (our novelty vs this DEM model)
> 사용자 요청: **firm DEM novelty** — 우리가 SOTA 임을 분명히. 아래는 *방어 가능한* 차별점만(과장 없이), 끝에 그들이 앞서는 칸도 정직히.

1. **전달 *삼중항*(ionic + electronic + thermal) — 그들은 전기-ONLY(SPS 금속).**
   Nisar 는 *전기* 단일 채널, *금속간화합물 NiAl*, *소결* 체제. 우리는 **σ_ionic(LOOCV 0.975) + σ_e(0.953) + σ_thermal(0.903)** 세 채널을 *같은 Kirchhoff
   골격* 위에서 동시에, **battery 복합 양극**에서 푼다. 특히 **σ_thermal 은 다중패스(AM-AM/AM-SE/SE-SE k_weight)** 라 단일 backbone 으로 안 되고 Ridge 가
   필요함을 우리가 정량화 — Nisar 의 열-전기 *유사성(analogy)* 가정이 *복합 다상*에선 깨짐을 우리가 보임(그들 NiAl 단상에선 analogy 가 성립하나 우리 3상에선 채널별 물리가 갈림).

2. **Holm 구속물리(a-spot) + Mikic saturation — 점접촉서 그들 neck-slab 보다 엄밀.**
   냉간가압 SE-SE 는 *점접촉*(a≪r)이 지배 — 여기서 **Maxwell/Holm 1/(2σa)이 닫힌형 정답**이고, 큰 neck 한계는 **Mikic `(1−a/r)^1.5`** 로 부드럽게 보간한다
   (network_conductivity:347). 그들 neck-slab `πa²/δ_gb` 는 *소결 융합목*엔 맞지만 *점접촉*서 δ_gb 고정-slab 가정이 깨진다. ⟶ **우리 솔버는 점접촉(Holm)~목(Mikic) 양극단을
   한 식으로 커버**; 그들은 소결-목 한쪽만. **각 체제의 옳은 물리를 우리가 모두 보유** = 방법 우위.

3. **DEM↔MPM 커플링 + 진짜 소성 morphology — 그들은 형상 안 변함.**
   Nisar 의 입자는 구·rigid(neck 만 소결로 성장). 우리는 **MPM(von Mises J2, ν=0.49)** 으로 *진짜 입자 SHAPE flow*(SEM 코어보존+경계평탄화 ✓), 부피보존 void-fill,
   공간 누적소성변형장 Σdg(열화 개시)를, **scaffold 커플링**(실제 DEM AM 위치 고정 + SE 만 MPM)으로 porosity 15.93 %·두께 29.95 µm 가 *EMERGE* 하게 푼다.
   ⟶ frame[5] 분업(DEM=transport / MPM=mechanics)을 *실제로 구현*. Nisar 는 transport 한쪽만(소결 morphology 는 외부 [43] 위임).

4. **Fracture-aware transport (Auerbach/Lawn) — 그들 미보유.**
   우리 σ_ionic/σ_e 폼은 **f_intact = 1 − fracture_excluded_pct/100** 의 partial-Holm(균열난 접촉은 micro-asperity 로 부분전도) 을 담는다(β_F·log f_intact).
   AM_P(다결정) 파괴(92:8 8mAh서 37–40 % cracked)를 transport 에 반영 — Nisar 의 *완전 소결 금속*엔 균열축이 없다.

5. **Literature-grounded σ_grain (Cronau/Trevisanello/Wang) — 그들 *fitting* 2-파라미터.**
   그들 GB(δ_gb=0.23, ε=0.16)는 *한 샘플 보정값*. 우리는 **σ_grain=3.0 mS/cm(Cronau 2022 단결정) × Cronau(r_SE) sub-µm 비정질화 인자**(no-fit literature),
   σ_e endpoints **Trevisanello 10/5 mS/cm(LOCKED)**, σ_thermal Wang step — **재료 물성을 문헌에서 고정**해 DoF 비용 0 + 과적합 차단. (그들 정직한 1샘플-보정·3샘플-검증은
   존중하나, 우리는 *애초에 fit 하지 않는다*.) ★ **다만 그들 neck-volume/α 의 *구조*는 우리 Stage-E 를 *literature 값으로* 채우면서도 흡수 가능**(§B).

6. **Battery-specific 3상(AM-SE-pore) — 그들 단상 금속.**
   우리는 NCM(전자상)+LPSCl(이온상)+pore 의 *상-특이 전달*(이온은 SE망·Holm, 전자는 AM망·Trevisanello, 열은 다중패스)을 푼다. Nisar 는 단상 NiAl — *상 간 trade-off,
   percolation 위상역전(LIB pore-Bruggeman vs 우리 SE-network), dead-AM/dead-SE* 같은 battery 고유 물리가 *원리적으로 없다*.

7. **Scaling-law predictor (LOOCV 0.90–0.975) — 그들 4점 곡선.**
   우리는 설계 knob → σ 삼중항을 *예측*하는 압축된 폼(σ_ionic 5-OLS, σ_e 8-LIVE, σ_thermal 14-Ridge)을 정보이론 ceiling 까지. Nisar 는 *시뮬-실측 검증 곡선*(4 porosity)이지 *예측기*가 아니다.

### ★ 그들이 *앞서는* 칸 (정직 — over-claim 방지)
- **명시적 sinter-neck 기하 + 부피보존 neck 기준 + neck-내-GB 저항** = **우리 overlap-proxy 보다 한 단계 물리적인 *목* 모델.**
  우리 SE-SE 는 점접촉(Holm)으로만 보고 *목의 단면·내부 공극*을 명시 기하로 안 푼다. **만약 우리가 *소결/cold-weld* 를 추가**한다면(So 2022 fusion-bond, Lee2025 PTFE cold-weld),
  그들 `K_c=ε·κ·πa²/δ_gb` + 부피보존 a 가 **직접 참조 스펙**이다(§B③). ⟶ **"sintering/fusion transport" 는 그들이 owns, 우리 미보유** — backlog 에 명시.
- **실험 σ 직접 검증의 *2단 디자인*(GB 없음=과대 → 있음=일치)** 이 깔끔. 우리 σ_e 도 이 디자인을 차용하면 Stage-E 기여를 더 설득력 있게 보일 수 있다(§B⑤).
- **forward-Euler 반복의 *수렴 보장 증명*(부록)** — 우리 spsolve mis-converge fallback 보다 이론적으로 견고(§B④ 흡수 후보).
- **단상·소결이라 열-전기 *analogy* 가 깔끔히 성립** — 우리 3상에선 채널이 갈려 못 쓰지만, 그들 맥락에선 한 모델로 열·전기 둘 다 = 우아함(우리가 배울 *단순성*).

> **결론(positioning):** Nisar 2024 는 **소결 *금속*의 *전기* 단일채널 neck-RNM** = 우리 σ_e Kirchhoff/Holm 의 *방법론적 사촌*. 우리는 **battery 3상 × 전달 삼중항 × Holm+Mikic ×
> DEM↔MPM 소성 × fracture-aware × literature-grounded × 예측기** 로 **명백히 더 넓고 깊다(SOTA).** 그들의 *유일한* 우위 = **명시적 소결-neck 물리** — 이건 우리가 *아직 소결을
> 안 다뤄서*지 못해서가 아니며, 추가 시 그들 식이 직접 청사진이 된다(So2022 와 함께). frame[5] 로 말하면: **그들은 transport 절반의 *소결-neck 변종*; 우리는 transport 삼중항 + mechanics(MPM) 양쪽.**

---

## 8. 적용 인사이트 (내 연구에 어떻게) — 요약
- ① **frame[4] σ_e 저항망 교차검증**: 우리 Kirchhoff `R_total=R_bulk+R_constriction`(network_conductivity:365) ≡ 그들 `R_ij=R_i+R_j+R_c`(eq17) → *솔버 골격 독립 재현* 확인.
- ② **neck-volume-preservation → `_film_area` 에 A_neck_volpres 한 줄 추가** = Stage-E *volume* arm 교차검증(§B①). 비용 0.
- ③ **소결/cold-weld 확장 시 `contact_mode='sinter'`** = 그들 neck-slab `δ_gb/(ε·σ·πa²)` 채택, δ_gb·ε 는 *우리 Cronau* 로 채움(§B③, So2022 결합).
- ④ **검증 2단 디자인 차용**: σ_cf(상한) → σ_full → 실측 3점 plot 으로 Stage-E 기여 시각화(§B⑤).
- ⑤ **forward-Euler 반복 = spsolve mis-converge 4단째 fallback**(§B④).

## 9. 인용 가능 문장 (deck/paper용)
- "An independently-formulated DEM resistor-network for effective *electrical* conductivity (Nisar et al., Comput. Part. Mech. 2024) — using the
  identical particle-centre Kirchhoff network and series branch resistance R_ij = R_i + R_j + R_c as our σ_e solver — validates the resistor-network
  approach against experimentally-measured conductivity of SPS-sintered porous NiAl, while differing in the contact term: a *sinter-neck* conductance
  (K_c = ε·κ·πa²/δ_gb with a volume-preservation neck criterion) where our solver uses Holm-1967 constriction (R = 1/(2σa)) with a Mikic finite-contact
  correction — the latter being more rigorous for the point-contact (a≪r) regime of cold-pressed sulfide electrolytes."
- "Both models independently cap non-physical high-density overlaps by a volume/surface-budget criterion (their grain-boundary fraction α ≤ 2r/√Σa²; our
  Stage-E A_geom = 2πR_min² and A_volume = V/h_min), demonstrating that 'over-compression must be capped by volume/surface conservation' is a
  representation-independent requirement of granular resistor networks."

## 10. 주의/한계 (over-claim 방지)
- **소재·체제 절대 전이 금지**: **NiAl 금속간화합물 단상**, **SPS *소결*(1100–1300 ℃)**, κ ~10⁵–10⁶ S/m. 우리 LPSCl/NCM 냉간가압·σ ~10⁻²–10⁰ S/m 과 *8~9자리·체제 모두 다름*.
  porosity 5–22 % 가 우연히 우리 10–18 %와 겹쳐도 *물리 기원*(소결 neck 성장 ≠ 가압 재배열/소성)이 달라 **절대 동일시 금지** — 방법·추세·neck 아이디어만.
- **digitized 주의**: κ–porosity 점들은 **Fig8/Fig10/Table1**에서 — *Table1 4점은 stated(정확)*, *Fig8/Fig10 곡선값은 digitized(±, TREND)*. CSV 에 precision 컬럼으로 구분 표기.
- **구만(rigid sphere) + 형상 안 변함**: neck 은 *소결 성장 기하*지 입자 SHAPE flow 아님 → 우리 MPM morphology 는 안 다룸(frame[5] transport 절반). Bazzoun/Varkey "구=타협" 계보.
- **단일채널(전기)**: σ_ionic/σ_thermal 없음 → 우리 삼중항과 직접 비교 불가(전기 추세만). 그들 *열-전기 analogy* 는 *단상 NiAl* 한정 — 우리 3상엔 미적용.
- **GB δ_gb·ε 는 *fitting*(한 샘플 보정)**: 그 0.23 µm / 0.16 은 *소재-특이 보정값* → 우리로 숫자 전이 금지. 흡수하는 건 *식 구조*지 *값* 아님.
- **소결 압력(5/30 MPa) ≠ 우리 냉간가압 300 MPa ≠ 작동압**: 그들 5/30 MPa 는 *소결 보조 가압*(고온서 확산이 치밀화 주역, 압력은 보조) → 우리 *제조 300 MPa*(상온, 압력이 주역)·
  *작동 수~수십 MPa* 와 모두 다른 축. Heckel/P_y 와도 무관(소결은 Heckel 압밀이 아님).
- **속도/효율 비교 없음**: 그들은 RNM 단독(FEM 대조 없음) → 우리 RNM↔FEM 32–98×(Bazzoun) 같은 속도 우위 주장은 *이 논문엔* 없음(Bazzoun 소유).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
