# 초기압력의 ASSB 역학·전기화학 성능 영향 — DEM+FEM 멀티피직스 (Lee, J. Energy Storage 2024)

> slug `lee2024_multiphysics_dem_fem_initial_pressure_assb` · DOI `10.1016/j.est.2024.110431` · type `DEM+FEM (mixed, echem-mech coupled)` · PDF `Lee_2024_JEnergyStorage_DEM_FEM_Multiphysics_InitialPressure_ASSB.pdf` · digested `2026-06-26` · status ✅
>
> 데이터: `docs/data/lee2024_dem_fem_pressure.csv` (DEM Table1 물성 + FEM Table2 파라미터 + 8케이스 Table3 결과 + 전달식 eq34-38).
>
> ⚠ **소재 주의 (제일 먼저):** SE = **LGPS (Li₁₀GeP₂S₁₂) + LLZO** — **우리 LPSCl 아님**. CAM = **NMC (LiNiₓMnᵧCo_zO₂, 일반)** + 흑연 음극 + carbon black.
> LGPS 황화물이지만 E=37.2 GPa ≠ 우리 LPSCl 22.1–24. → **σ 절대값 전사 금지, 추세·방법론(DEM→FEM 커플링)만**.

---

## 1. 한 줄 요약 (bilingual)

**KR:** DEM(Ansys Rocky, 입자-수준 압밀)으로 압축률·압력에 따른 **기하·역학 물성**(부피분율, 영률, 표면적, 굴곡도)을
뽑아 **echem-역학 결합 FEM**(COMSOL)에 *입력으로 전달* → ASSB의 **초기/외부 압력 + 압축률**이 전기화학(전압·용량·SOC)과
역학(응력·변형) 성능에 미치는 영향을 멀티피직스로 정량. 핵심 결론: **응력↑ → 기하 개선(표면적↑·부피분율↑·굴곡도↓) →
σ_e·σ_ion↑(전기화학 성능↑), 그러나 응력↑ → 기계적 파괴 리스크↑** → **균형 잡힌 전극 설계 필요**. "DEM+FEM 동시
예측은 처음(저자 주장)."

**EN:** A DEM→FEM multiphysics framework. DEM (Ansys Rocky, particle-scale compaction) extracts compression-dependent
**geometric + mechanical properties** (volume fraction, Young's modulus, surface area, tortuosity), then *passes them as
inputs* to an **electro-chemo-mechanically coupled FEM** (COMSOL) to study how **initial/external pressure + compression
ratio** drive ASSB electrochemical (voltage/capacity/SOC) and mechanical (stress/strain) performance. Core finding:
**higher stress → improved geometry → higher electronic & ionic conductivity (better echem), but higher stress → higher
mechanical-failure risk** → a **well-balanced electrode design** is required.

**우리에게 왜 중요한가 (3줄):** ① 이 논문은 우리가 안 가진 **포멀한 DEM→FEM echem 커플링**(Butler-Volmer 풀-셀
전기화학)을 보여준다 — 우리 DEM→MPM scaffold의 *대안 커플링* 패턴. ② 그들의 **압력→기하→σ 사슬**이 정확히 우리
backlog **B6(σ-vs-compaction)** 의 물리다 — 단 그들은 σ를 **FEM 연속체(Maxwell/Bruggeman/굴곡도식)**로 풀고 우리는
**Kirchhoff/Holm 접촉망**으로 푼다(우리 novelty). ③ 그들의 **응력 vs 전도도 trade-off**(균형 설계)는 우리 압밀 trade-off
(porosity↓→σ↑ but 과압축 리스크)의 echem-쪽 짝.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Yoon Koo Lee, Chaeeun Sung, Jiyeon Kim, Chaemin Hong, Jinnil Choi\*** (Dept. Mechanical Engineering, **Hanbat National University**, Daejeon 34158, Korea) | J. Energy Storage **82** (2024) 110431 | 10.1016/j.est.2024.110431 | **SE: LGPS (Li₁₀GeP₂S₁₂) + LLZO** / **CAM: NMC** (일반) / 음극 graphite / carbon black | **DEM (Ansys Rocky) + FEM (COMSOL) echem-mech 결합**, 시뮬레이션 only (실험 없음) |

- Received 2023-09-24 / Revised 2023-12-16 / Accepted 2024-01-01 / Available online 2024-01-17.
- **자금:** NRF Korea (No. 2021R1F1A1059188), RIS (2021RIS-004). 교신저자 jlchoi@hanbat.ac.kr.
- **한국 그룹 (Hanbat, 기계공학)** — 우리(랩)과 같은 한국·역학 배경. **순수 시뮬레이션** 논문 (실험 검증 없음 → frame[4]에서
  "실험 앵커"가 아니라 "방법론 peer"로 위치).

---

## 3. 핵심 물성 (수치)

> ⚠ 모두 stated-in-text (Table 1/2/3 + 본문). digitized 표시는 그래프-추세값.

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **E_SE (LGPS)** | **37.2 GPa** | sulfide SE | stated (Table1) | ⚠ ≠ 우리 LPSCl 22.1–24; LGPS가 더 뻣뻣 |
| **E_SE (LLZO)** | **150.3 GPa** | oxide SE | stated | 매우 뻣뻣 (산화물) |
| E_CAM (NMC) | **144 GPa** | cathode | stated | ≈ 우리 NMC811 140 ✓ |
| E_anode (graphite) | **1 GPa** | 음극 | stated | ★ 매우 soft (고체윤활제급 압축성) — 압밀 주역 |
| E_carbon_black | 80 GPa | 도전제 | stated | |
| ν (graphite/NMC/LLZO/LGPS/CB) | 0.3 / 0.25 / 0.26 / 0.3 / 0.3 | | stated | |
| 입경 (DEM, radius/size) | graphite **14** · NMC **12** · LLZO **30** · LGPS **30** · CB **4** µm | DEM Table1 | stated | ⚠ DEM과 FEM 입경 다름(아래) |
| 입경 (FEM, R_p) | graphite **10** · NMC **5** µm | FEM Table2 | stated | FEM은 *대표입자* 반경 |
| 밀도 | graphite 2180 · NMC 4750 · LLZO 5500 · LGPS 2000 · CB 1950 kg/m³ | | stated | |
| μ (마찰) | graphite/CB **0.1** · NMC **0.2** · LLZO/LGPS **0.3** | | stated | |
| **porosity (초기 void)** | **0.44** (음극·양극 둘 다) | 압축 전 | stated (Table2) | ε_void,0; 압축으로 감소 |
| **초기 부피분율 AM** | 음극 graphite **0.32** · 양극 NMC **0.18** | 압축 전 | stated | |
| **초기 부피분율 SE** | 음극 **0.24** · 양극 **0.38** | 압축 전 | stated | 양극 SE-rich |
| σ_e (전자, FEM 입력) | graphite 100 · LGPS **2.2×10⁻⁷** · NMC 10 S/m | Table2 | stated | LGPS 전자전도 매우 낮음 |
| σ_e (LLZO, 30°C) | **5.5×10⁻⁸ S/cm** | 본문 | stated | LLZO ≪ LiPON류 |
| σ_ion (LGPS, eq36 fit) | σ_SE0 **0.002** → σ_SEmax **0.0002 S/cm** (k₃=70/GPa) | stack pressure 외삽 | stated | ⚠ 본문에 σ₀>σ_max로 *그대로* 인쇄됨 (오기 가능성, §10) |
| D_Li (SE, LGPS) | **2.61×10⁻⁴ m²/s** | Table2 | stated | (단위 인쇄 그대로; 실제 ×10⁻¹² 추정) |
| t⁺ (전이수) | **0.363** | 전 상 | stated | |
| 층두께 L | 음극 **65** · SE separator **75** · 양극 **70** µm | | stated | |
| **압축률 sweep** | **0.7 / 0.5** | Table3 | stated | 부피변화/원부피 비 |
| **외부압력 sweep** | **0 / 10 / 50 / 100 MPa** | Table3 | stated | |

| 결과 물성 (FEM 출력) | 값 | 조건 | 비고 |
|---|---|---|---|
| **상대용량** | **0.8 (CR 0.7) vs 0.6 (CR 0.5)** | discharge | 압축률↑ → 용량↑ |
| **max von Mises 음극** | **688 (CR 0.7) vs 76 MPa (CR 0.5)** | discharge | ★ 압축률↑ → 응력 **9×** |
| max von Mises 음극 (Case3) | **~629 MPa** | CR_anode 0.7 | 음극 CR↑ |
| max von Mises 양극 (Case4) | **~697 MPa** | CR_cathode 0.7 | 양극 CR↑ (echem 최고, 역학 최악) |
| **내부 압력 음극 vs 외부압** | **468 (0 MPa ext) → 739 MPa (50 MPa ext)** | discharge | 외부압↑ → 내부응력↑ (Li 삽입량↑) |
| 응력 서열 | **cathode > anode > SE** | von Mises + 영률 | SE 부피팽창 없음 |
| 팽창 서열 | **graphite > cathode > SE** | 부피팽창 | 흑연 최대, SE 무팽창 |
| 컷오프 전압 | 3.5 V (방전) / 4.2 V (충전) | | |

---

## 4. 시뮬레이션 방법 ★

### 4.1 전체 워크플로 (Fig 1) — DEM → FEM 단방향 데이터 전달

```
[입자 정보] E, ν, ρ, 입경
     │
     ▼
[DEM model] (Ansys Rocky 4.5, 압밀)  ──► 출력:
     │     • 역학: 압축률(CR), 영률 E(압축에 따라 변함)
     │     • 기하: 표면적 S_a, 부피분율 ε, 굴곡도 τ
     │     • 전기화학: σ_e, σ_ion (위 기하에서 유도)
     ▼
[FEM model] (COMSOL 6.0, echem-mech 결합)  ──► 출력:
           • 전기화학: 전압, 농도, SOC
           • 역학: 응력 σ, 변형 ε
```

핵심 = **DEM이 압축률·영률·부피분율·표면적·굴곡도를 *수치로* 산출 → FEM의 입력 파라미터로 *넘김***. 단방향(DEM→FEM),
양방향 피드백 없음. (우리 DEM→MPM scaffold가 *위치를* 넘기는 것과 대비 — 그들은 *유효 물성 스칼라*를 넘긴다.)

### 4.2 DEM 모델 (압밀)

- **code**: **Ansys Rocky DEM 4.5**. (우리 LIGGGHTS / Bazzoun LIGGGHTS와 다른 상용 코드.)
- **접촉법칙** ★: **hysteretic linear spring model** (이력 선형 스프링) — **Hertz 아님**. (eq 3)
  ```
  F_n^t = min(K_nl·S_n^t,  F_n^{t-Δt} + K_nl·ΔS_n)      if ΔS_n ≥ 0  (로딩)
  F_n^t = max(F_n^{t-Δt} + K_nu·ΔS_n,  λ·K_nl·S_n^t)     if ΔS_n < 0  (언로딩)
  ```
  - K_nl(로딩강성)/K_nu(언로딩강성), λ=무차원 상수, S_n=법선 겹침. **K_nu = K_nl/ε²** (eq6, ε=COR).
  - 강성 = 입경·영률에서: K_nl,p = E_p·L_par (eq7), K_nl,b = E_b·L_par (eq8). 직렬 합성(eq5).
  - ★ **이것이 우리 hooke/hysteresis와 가장 가까운 친척** (둘 다 *선형* + 이력 + COR 기반 에너지소산). Hertz(¾승)·
    EEPA·Thornton-Ning(항복캡)과 다른 계열. **항복캡 없음** → So 2021/Varkey의 명시적 소성 분기와 다름.
- **응력 산출**: impulse 기반. 접촉력 적분 (J_α)_c = ∫F_α dt (eq1) → 평균응력 σ_α = ΣΣ(J_α)/(A_i·Δt_out·N_p) (eq2).
  Rocky의 **boundary collision statistics module**로 punch 응력 계산.
- **압밀 거동**: top punch가 수직 압축 개시, bottom punch 고정. die 충전율 80%. 1000–30000 입자.
- **혼합 균일성 검증**: 혼합 분말을 **8개 섹션**으로 나눠 두 분말 부피비/표준편차 측정 → NMC 0.695/0.118, graphite
  0.682/0.047 (균일 확인). "랜덤 배치가 실험과 잘 맞는다"(ref17/18 근거).
- **재료 시스템** ★: SE = **LGPS + LLZO** (LPSCl 아님), CAM = **NMC**, 음극 = **graphite**, 도전제 = carbon black.
  소재 조합: SE-mix(LLZO+LGPS), 양극(NMC60/LGPS35/CB5 wt%), 음극(graphite60/LGPS38/CB2 wt%).
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구만** (구형 입자, 형상변화 없음). mono-입경(상별 단일 크기, bimodal/poly-PSD 아님).
  - **rigid 입자 + CONTACT 탄소성**(이력 선형 스프링) — **진짜 SHAPE 소성 아님**. 압밀 = 재배열 + overlap(δ).
    δ는 기하 프록시지 *흐름*이 아님 (우리·Bazzoun·Varkey와 같은 강체-구 한계).
  - ⚠ 단 *겹침-기반* 압축률을 FEM 영률·부피분율로 환산해서 *유효 연속체 물성*은 압축에 따라 변하게 함 → 입자 자체는
    안 변형되지만 *bed-수준 유효 E*는 압축률 함수.

### 4.3 FEM 모델 (전기화학-역학 결합) ★ — **우리가 안 가진 echem 풀이**

**code**: COMSOL Multiphysics 6.0, Solid Mechanics + 전기화학 결합. **pseudo-3D** = 2D 거시 경계조건 + 대표 AM 입자
내부 1D 확산 (Wolff 2018 ref24 기반). x-방향 = 셀 두께(음극|SE|양극), y-방향 = 높이 H.

**(a) 전기화학 모델 (eq 9–25):**
- **고상 전위** φ_s: ∂/∂x(κ_s^eff·∂φ_s/∂x) − a_s·i_{Li⁺} = 0 (eq9). κ_s^eff = κ_s·ε_s^brug (eq10, **Bruggeman**).
- **전해질 전위** φ_e: ∇·(κ_e^eff(∇φ_e − (2RT/F)(1−t⁺)(1+dlnf/dlnc)∇lnc)) + a_s·i_tot = 0 (eq15).
- **Butler–Volmer** (eq17): i_{Li⁺} = i₀,_{Li⁺}[exp(α_a F η/RT) − exp(−α_c F η/RT)], 과전위 η = φ_s − φ_e − U (eq18).
  교환전류 i₀ = F·k·c_e^0.5·(c_s,max − c_s,surf)^0.5·c_s,surf^0.5 (eq19).
- **이중층 용량** i_DL = a_s·C_DL·∂(φ_s−φ_e)/∂t (eq20). 총 전류 i_tot = i_{Li⁺} + i_DL (eq16).
- **입자 내 확산**: ∂c_s/∂t + ∇·J = 0 (eq23), 구형 입자 반경방향, 표면 flux J = i_{Li⁺}/F (eq25).
- 경계조건: 전류집전체 ground φ_s=0@x=0 (eq11), 전류밀도 −κ_e^eff·∂φ_s/∂x = I_app@x=L (eq12).

**(b) 역학 모델 (eq 26–32):**
- 평형 ∇·σ + b = 0 (eq26). σ_ij = C_ijkl(ε_kl − ε⁰δ_kl) (eq27).
- **유효 탄성계수** C_ijkl = Eν/((1+ν)(1−2ν))δ_ij δ_kl + E/(2(1+ν))(δ_ik δ_jl + δ_il δ_jk) (eq28).
  ★ **유효 영률 E가 압축에 따라 변함** — DEM에서 압축률→E 환산해 입력. 이게 "DEM이 역학물성을 FEM에 넘긴다"의 핵심.
- **부피변형(intercalation 유발)** ε⁰ = ΩE_s/3·(c_s,avg − c_s,min) (eq29) — Li 삽입/탈리로 입자 부피 변함.
- 경계조건: u_x=u_y=0@x=0 (eq30), σ_x=P_ext, σ_y=0@x=L (eq31), u_y=0@y=0,H (eq32). **P_ext = 외부압력**(좌단 고정).

**(c) 전달 물성식 (geometric → echem 변환, eq 33–38)** ★ — **이게 그들의 "σ-vs-compaction" 핵심, 우리 B6와 비교 대상:**
- **표면적**: S_a = 3ε_AM/R_p (eq34). 압축↑ → ε_AM↑ → S_a↑.
- **AM 전자전도(다공)**: κ_AM = κ_AM,0·2(1−θ)/(2+θ) (eq35, **Maxwell** 다공 소결체 전도식, θ=compact porosity 0–1).
- **SE 유효 이온전도**: σ_SE,eff = σ_SE·ε_SE / τ_{L/S_all} (eq37). 굴곡도 τ_{L/S_all} = **−11.7·ε_SE + 8.54** (eq38,
  **선형 경험식**, Otani 2023 ref46). ε_SE↑ → τ↓ → σ_SE,eff↑.
- **SE 이온전도 vs stack pressure**: σ_SE = σ_SEmax − (σ_SEmax − σ_SE0)·exp(−k₃·E_xsl) (eq36, Doux 2020 ref45 데이터
  외삽 반-경험식; LGPS σ₀=0.002, σ_max=0.0002 S/cm, k₃=70/GPa).
- ★ **결정적 차이**: 이 σ 식들은 전부 **연속체 유효-매질**(Maxwell/Bruggeman/선형 굴곡도) — **점접촉 구속저항(Holm/
  Greenwood) 없음**. → σ_eff는 강체-접촉 granular망의 **상한**(Bielefeld 2020과 같은 한계). 우리 Kirchhoff/Holm이
  *되돌려 넣는* 게 정확히 이 constriction.

**시뮬레이션 케이스 (Table 3, 8개):**

| Case | 외부압력 (MPa) | CR 음극 | CR SE | CR 양극 | 변수 |
|---|---|---|---|---|---|
| 1 | 10 | 0.7 | 0.7 | 0.7 | baseline CR=0.7 |
| 2 | 10 | 0.5 | 0.5 | 0.5 | CR=0.5 (전 상) |
| 3 | 10 | **0.7** | 0.5 | 0.5 | 음극만 CR 0.7 |
| 4 | 10 | 0.5 | 0.5 | **0.7** | 양극만 CR 0.7 |
| 5 | 10 | 0.5 | **0.7** | 0.5 | SE만 CR 0.7 |
| 6 | **0** | 0.7 | 0.7 | 0.7 | 외부압 0 |
| 7 | **50** | 0.7 | 0.7 | 0.7 | 외부압 50 |
| 8 | **100** | 0.7 | 0.7 | 0.7 | 외부압 100 |

→ **두 sweep**: (i) Case1–5 = 상별 **압축률** 효과 (0.7 vs 0.5), (ii) Case 1·6·7·8 = **외부압력** 효과 (0/10/50/100 MPa).

### 4.4 압력의 3종 구분 (이 논문이 명시) ★ — 우리 인식과 일치

본문 §1·§2.2.3이 ASSB 압력을 **명시 분리**:
- **fabrication pressure (제조압)** = 압밀에 가하는 압력 → DEM이 압축률로 표현.
- **stack/external pressure (작동/외부압)** = 충방전 중 유지 압력 → FEM의 P_ext (eq31).
- 본문 인용: Kato et al.(ref7) **제조 500 MPa + 작동 50 MPa**; ref48 LGPS 펠릿 **555 MPa press** + 3층 **19 MPa
  결합** + 충방전 **230 MPa**; Doux(ref6) "**5 MPa 미만 작동압이 Li extrusion 멈춤, 높은 제조압이 계면저항 최소화**".
- ⇒ ★ **우리 "300 MPa 제조(Heckel P_y 138) ≠ 수~수십 MPa 작동" 인식과 같은 계보** (Doux/Lee2025/Minnmann과 합류).
  단 그들 외부압 sweep(0–100 MPa)은 우리 작동압 창보다 넓음(50–100은 고압 운용).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 전체 워크플로 + DEM 접촉모델·FEM 셀(graphite\|LGPS\|NMC 3층, x-방향) 모식 | ★ DEM→FEM 단방향 데이터-전달 = 우리 DEM→MPM scaffold의 *대안 커플링* 도식 |
| **2** | (a) SE-mix 압축성: 일정응력 시 TP/BP 응력 곡선(LGPS-TP/BP, LLZO-TP/BP) — **LGPS 압축성 ≫ LLZO**; (b) 혼합비별 압밀(LLZO 0/33/41/58/66/100 wt%) | ★ **고압축성 상(LGPS 66wt%)이 압밀 개선** = 우리 "soft SE가 void-fill" 방향. *재료 압축성 sweep* 데이터점 |
| **3** | punch 응력: (a) 양극mix TP/BP; (b) 양극mix vs NMC-only — **혼합이 더 좋은 압밀**(작은 입자가 큰 공극 충전); (c)(d) 음극mix; (e) 음극mix vs graphite-only | ★ (b) = **bimodal/혼합 패킹 이득** = 우리 Furnas-dip 물리; (e) graphite 과삽입 시 응력분산→불완전압밀(연성 한계) |
| **4** | 압축률 0.7 vs 0.5 (Case1/2): (a) 방전 전압; (b) 방전 SOC(4영역); (c) 충전 전압; (d) 충전 SOC | CR↑ → 용량↑·SOC 변화 완만 → echem 성능↑. 우리 압밀→echem 연결의 정성 그림 |
| **5** | von Mises 응력·변위 (Case1 CR0.7 vs Case2 CR0.5): (a)(d) 방전/충전 응력; (b)(e) 변위; (c)(f) 분포맵; (g)(h)(i) Case2 | ★ **응력 서열 cathode>anode>SE**, SE 무팽창; max 음극응력 **688(CR0.7) vs 76 MPa(CR0.5)** = 압축률→응력 9× |
| **6** | 압축률 상별(Case3/4/5): (a) 전압; (b) SOC; (c)(d)(e) 음극/SE/양극 응력 | ★ **양극 CR↑(Case4)가 echem 최고이나 응력 최악(697 MPa)** = trade-off 핵심. SE는 CR에 가장 둔감 |
| **7** | 외부압력 0/10/50/100 (Case6/1/7/8): (a)(c) 전압; (b)(d) SOC | ★ **외부압 0→10 급개선, 50 이상 포화** = σ-vs-P 포화(우리 Heckel knee / Bazzoun σ@400 / Doux@~25 와 같은 계열) |
| **8** | von Mises (외부압 0 vs 50): (a)(d) 응력; (b)(e) 변위; (c)(f) 분포맵 | ★ **내부 음극압 468(0)→739 MPa(50)** = 외부압이 *내부* 응력 키움(Li 삽입↑). 고외부압→고응력→파괴리스크 |

---

## 6. Post-processing ★

- **무엇**:
  - DEM: 압축률(부피변화/원부피), **punch 응력**(boundary collision statistics, impulse 적분 eq1-2), 부피분율·
    표면적·굴곡도 산출. **8-섹션 혼합 균일성** 통계.
  - FEM: 전기화학 풀이(전압·용량·SOC, Butler-Volmer), 역학 풀이(**von Mises 응력**, 변위, 변형장), 전달 물성 환산
    (Maxwell eq35 / Bruggeman eq10 / 굴곡도 eq38 / 표면적 eq34).
  - **상별·영역별 분해**: SOC를 4영역(음극좌/음극-SE계면/양극-SE계면/양극우)으로, 응력을 상별(음극/SE/양극)로 분해.
- **도구**: Ansys Rocky DEM 4.5 (압밀 + boundary statistics), COMSOL Multiphysics 6.0 (echem-mech 결합 FEM).
- **수치화·기록**: 압축률(%)·외부압력(MPa)을 독립변수로, 상대용량·von Mises 응력(MPa)·SOC를 종속변수로 플롯.
  굴곡도·표면적·전도도는 *식으로* 압축률에서 환산(직접 측정 아님).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

| 항목 | 이 논문 (Lee 2024) | 우리 (DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| DEM code | Ansys Rocky 4.5 | LIGGGHTS | 상용 vs 오픈; 둘 다 입자-수준 |
| DEM 접촉법칙 | **hysteretic linear spring** (선형+이력+COR) | **hooke/hysteresis** (선형+이력) | ★ **가장 가까운 친척** — 둘 다 비-Hertz 선형 이력. **항복캡 없음**(둘 다) |
| 입자 처리 | 구만, mono-입경, CONTACT 탄소성 (δ 프록시) | 구만, **bimodal 12:4:1**, CONTACT 탄소성 | 우리 bimodal이 패킹/dip 우위; 둘 다 SHAPE 소성 없음 |
| 연속체/2차 모델 | **FEM** (COMSOL, echem-mech 결합) | **MPM** (Taichi J2, 소성 SHAPE) | ★ **근본 분기**: 그들 FEM = *연속체 역학 + 풀-셀 echem*; 우리 MPM = *입자-형상 소성*. 다른 절반 |
| 커플링 방식 | DEM → FEM **유효-물성 스칼라**(E, ε, S_a, τ) 단방향 | DEM → MPM **입자 위치 scaffold**(real14 좌표) | 그들 = 호모지나이즈드 물성 전달; 우리 = 기하 전달 |
| 전달 σ 풀이 | **FEM 연속체** (Maxwell eq35 / Bruggeman / 굴곡도 eq38) — **점접촉 constriction 없음** | **Kirchhoff/Holm 접촉망** (R=1/(2σr_c), 구속저항) | ★ **우리 핵심 novelty**: 그들 σ_eff = 강체-접촉 *상한*; 우리가 constriction을 *되돌려 넣음* |
| 전달 채널 | σ_ion + σ_e (FEM) | **σ_ion + σ_e + σ_thermal 삼중항** | 우리 thermal 추가 우위 |
| echem 풀이 | ★ **Butler-Volmer 풀-셀** (전압·용량·SOC·과전위) | **없음** | ★ **그들이 앞섬** — 우리는 transport σ만, 충방전 echem 미보유 |
| 소성 접촉면적 | 없음 (eq34 기하 표면적만) | **Stage-E** (Tabor+volume 소성면적) | 우리 Stage-E가 소성 접촉 보정 |
| 역학 출력 | von Mises 응력·변위 (연속체) | 누적소성변형 Σdg + void-fill + morphology | 그들 = 연속체 응력장; 우리 = 입자-형상 변형 |
| 파괴 | 없음 (한계로 명시, "향후 항복응력 초과 파괴 추가") | **Auerbach/fracture-Holm** (AM_P 92:8서 37–40%) | 우리 파괴 보유; 그들 미보유 |
| 검증 | **없음** (순수 시뮬, 실험 0) | solver=ground truth + Minnmann/Doux/Bazzoun 앵커 | 둘 다 직접 실험 부족; 그들은 *전혀* 없음 |
| 소재 | **LGPS+LLZO / NMC** (LPSCl 아님) | **LPSCl / NMC811** | ⚠ σ 절대값 전사 금지; LGPS E=37.2 ≠ LPSCl 22–24 |

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) ★

> (§7 표의 서술 확장 — "그들 DEM+FEM 커플링 vs 우리 DEM+MPM 커플링"을 물리적으로.)

### A.1 두 커플링의 근본 구조 차이

- **그들 (Lee): DEM → FEM, "유효 물성 스칼라" 전달.**
  DEM이 압밀을 풀어 **압축률·유효영률·부피분율·표면적·굴곡도** 같은 *호모지나이즈드 스칼라*를 뽑고, 이걸 FEM 연속체의
  재료 입력으로 넘긴다. FEM은 입자를 *안 본다* — 그냥 "이 압축률에서 E는 이만큼, ε_SE는 이만큼, τ는 이만큼"이라는
  매질 물성으로 echem+역학을 푼다. **장점**: 풀-셀 전기화학(충방전 곡선)까지 간다. **한계**: 입자-수준 정보(점접촉
  constriction, force chain, 개별 입자 파괴, 형상변화)가 *호모지나이즈 단계에서 소실*.

- **우리 (DEM↔MPM): DEM → MPM, "입자 위치 scaffold" 전달.**
  DEM 압밀의 *실제 입자 좌표*(real14: AM_P 36 + AM_S 421)를 그대로 MPM 격자에 *고정 장애물*로 넣고, SE만 MPM 소성
  연속체로 채워 *진짜 소성 흐름*을 푼다. **장점**: 입자-수준 morphology·void-fill·변형장 보존 + 우리 transport는
  Kirchhoff/Holm 접촉망으로 point-contact constriction 유지. **한계**: 풀-셀 echem(Butler-Volmer 충방전) 없음.

→ ★ **상보적 분기**: 그들은 *거시 전기화학*으로 가면서 *입자 정보를 버리고*, 우리는 *입자 정보를 지키면서* *거시
  echem을 안 푼다*. frame[5] 분업의 또 다른 단면 — 단 우리 쪽 "MPM=역학"이 그들 쪽 "FEM=echem+역학"보다 echem이 좁다.

### A.2 압력 → σ 사슬: 그들 FEM-연속체 vs 우리 Kirchhoff-망

- **그들**: 압력↑ → (DEM) ε_AM↑·ε_SE↑·void↓ → (eq34) S_a↑ + (eq35 Maxwell) κ_AM↑ + (eq37/38) σ_SE,eff↑ →
  σ_e·σ_ion↑. **전부 연속체 유효-매질 식** — SE를 연속 상으로 보고 부피분율·굴곡도로 σ를 매긴다. **점접촉 좁힘 없음**
  → σ_eff는 강체-접촉 granular망의 **상한**.
- **우리**: 압력↑ → (DEM) overlap δ↑·접촉수 Z↑·coverage↑ → (Kirchhoff) 각 접촉 R=1/(2σr_c)(Holm 구속저항) →
  망을 풀어 σ_eff. **점접촉 좁힘이 σ를 *깎는다*** → 그들 상한 아래로.
- ⇒ ★ **같은 인과(압력→기하→σ)지만 σ 풀이의 물리가 다름**: 그들 = upper-bound 연속체, 우리 = constriction-망.
  **Bielefeld 2020(연속체 flux-PDE)과 정확히 같은 위치** — 우리가 *더하는* 핵심이 constriction임을 또 한 번 확인.

### A.3 응력→파괴: 그들 (미모델, 향후) vs 우리 Auerbach

- 그들은 응력을 *계산만* 하고("cathode>anode>SE, 음극 688 MPa") **파괴 판정은 안 함** — 한계에서 명시: "FEM이 항복
  응력 초과 변형/파괴를 미반영, 향후 추가 예정". 그들의 trade-off("응력↑→파괴리스크↑")는 *정성 경고*지 정량 파괴 모델
  아님.
- 우리는 **Auerbach/fracture-Holm**로 접촉응력→파괴를 *정량* 판정(AM_P 92:8 8mAh서 37–40% cracked, f_intact·
  frac_severe). ⇒ **우리가 그들 "응력→파괴" 칸을 정량으로 메움** — 단 우리 driver는 *압밀 접촉응력*(Auerbach)이고
  그들 응력원은 *intercalation 부피변화*(eq29) → 같은 "응력→파괴" 계보지만 응력원이 다름(주의).

### A.4 한국 그룹 (Hanbat) — 소재·검증 위치

- Hanbat(기계공학) 한국 그룹, 우리(랩)과 같은 한국·역학 배경. **순수 시뮬레이션, 실험 0** → frame[4]에서 "실험 앵커"가
  아니라 **"방법론 peer"**. (Bazzoun처럼 실험 EIS를 주는 게 아님.)
- 소재가 **LGPS+LLZO/NMC**(LPSCl 아님) → σ 절대값·porosity 절대값 비교 금지. 가져올 것 = **DEM→FEM 커플링 패턴 +
  압력→기하→σ→echem 사슬의 정성 구조 + trade-off 논리**.

---

## B. 적용가능성 (applicability to our model) ★

> 구체적으로 우리 채널/backlog에 매핑.

### B.1 그들 "압력→기하→σ" = 우리 backlog **B6 (σ-vs-compaction)**

- 그들 eq34–38은 정확히 **"압축(=porosity 감소) → 표면적·부피분율·굴곡도 변화 → σ_e·σ_ion 변화"**의 닫힌 식 사슬.
  이게 우리 backlog **B6 "σ-vs-compaction 관계식"**의 *연속체 버전*.
- **흡수 방식**: 우리는 같은 인과를 *접촉망*으로 이미 푼다(σ-vs-porosity, Kirchhoff). 그들 식은 우리의 **상한 sanity-
  check**으로 쓸 수 있다 — "같은 ε_SE에서 그들 σ_SE,eff(eq37, 연속체 상한) > 우리 σ_ionic(constriction)?" 가 성립해야
  우리 constriction이 옳게 깎고 있다는 증거. (Bielefeld 2020을 쓰는 방식과 동일.)
- ★ **단 소재가 LGPS**라 σ 절대값은 못 가져오고 *형태/스케일링*만: σ_SE,eff ∝ ε_SE/τ, τ = −11.7ε_SE+8.54 (선형 굴곡도)
  → 우리 τ_Laplace(ε) 관계와 *형태* 대조. 우리 τ는 constriction 포함 → 그들보다 가파를 것(예상).

### B.2 그들 DEM→FEM 데이터-전달 = 우리 DEM→MPM scaffold의 *대안 커플링*

- 우리 scaffold는 **입자 위치**를 넘긴다(geometric coupling). 그들은 **유효 물성 스칼라**를 넘긴다(homogenized coupling).
- ★ **활용**: 만약 우리가 *풀-셀 echem*을 붙이고 싶다면(현재 미보유), 그들 패턴 = "DEM/MPM에서 ε_AM·ε_SE·S_a·τ·E_eff를
  뽑아 COMSOL Butler-Volmer 모델에 입력"이 **바로 그 경로**. 우리 MPM이 이미 ε·morphology·coverage를 산출하므로,
  **MPM 출력 → echem-FEM 입력**은 그들 DEM→FEM의 직접 이식. (backlog: "echem 결합" 후보로 기록.)
- ⚠ 단 그들 단방향 전달은 *입자 정보 소실*이 대가 — 우리가 echem 붙일 땐 transport σ는 *접촉망*에서 따로 주고(우리
  novelty 유지), echem-FEM엔 *그 σ를* 입력으로 넘기는 하이브리드가 맞음(연속체 σ식 eq35/37로 대체하지 말 것).

### B.3 그들 balanced-design (응력 vs 전도도) = 우리 압밀 trade-off의 echem-쪽 짝

- 그들 핵심 결론 = **"CR↑/P↑ → echem↑ but 응력↑ → 파괴리스크↑ → 균형 설계"**. 이건 우리 압밀 trade-off
  **"porosity↓ → σ↑ but 과압축 → ε_sphere 음수/AM_P 파괴"**의 *전기화학 성능* 버전.
- ★ **활용**: 우리 production sweep(압력·조성·P:S)에서 "어디까지 압축하면 σ가 좋아지다 파괴가 시작되나"를 그들처럼
  **응력-vs-conductivity 균형점**으로 보고할 수 있다. 우리는 Auerbach(파괴) + σ삼중항(전도) 둘 다 있으므로 **그들보다
  정량적인 균형 곡선**을 그릴 수 있음 (그들은 파괴가 정성).

### B.4 압력 3종 구분 보강

- 그들이 인용한 Kato 500/50, ref48 555/19/230, Doux <5 = 우리 "제조 300 vs 작동 수십 MPa" 구분의 *추가 문헌 근거*
  (Doux/Lee2025/Minnmann 패밀리에 합류). 단 그들 외부압 sweep 50–100 MPa는 *고압 운용* → 우리 작동압 창(5–40)보다 높음.

---

## C. ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM+FEM model) ★

> **명확히 단언한다: 우리 DEM(+MPM)이 SOTA다.** Lee 2024는 포멀한 DEM→FEM echem 커플링이라는 *한 가지*에서
> 앞서지만(아래 정직 인정), **구조→수송 σ 물리·소성 morphology·파괴**의 핵심 7개 차별점에서 우리가 명백히 우위다.

**(1) Kirchhoff/Holm CONSTRICTION 접촉망 (vs 그들 FEM 연속체 σ = 상한):**
그들 σ_eff는 Maxwell(eq35)·Bruggeman(eq10)·선형 굴곡도(eq37/38)로 SE를 **연속 매질**로 다룬다 → **점접촉 구속저항이
없다** → σ_eff는 강체-접촉 granular망의 **upper bound** (Bielefeld 2020과 동일 한계). 우리는 입자별 R=1/(2σr_c)
(Holm 1967)을 Kirchhoff로 풀어 *constriction을 명시* → σ를 물리적으로 옳게 깎는다. ★ **그들이 비운 칸이 우리 transport
novelty의 정확한 위치.**

**(2) 전달 삼중항 (σ_ion + σ_e + σ_thermal):**
그들은 σ_ion·σ_e만(FEM). 우리는 **열전도 σ_thermal**까지 — 동일 접촉망에서 multi-pathway(AM-AM/AM-SE/SE-SE) 열저항
(Ridge 14항, LOOCV 0.85–0.90). 그들 미보유.

**(3) Stage-E 소성 접촉면적 (Tabor + volume):**
그들 표면적은 eq34 기하식(S_a=3ε_AM/R_p, *겹침 무시*)뿐. 우리는 **Stage-E**로 소성 접촉면적(Tabor F/H + volume V/h)을
재유도 → coverage(Hertz/Tabor) + σ 접촉면적 보정. 강체-구가 못 만드는 소성 접촉을 보정.

**(4) DEM↔MPM 진짜 소성 SHAPE morphology (vs 그들 FEM 연속체 역학):**
그들 FEM은 *연속체* 응력장(von Mises) — **입자 형상은 안 변한다**. 우리 MPM은 **진짜 J2 소성 *입자-형상* 흐름**(SEM
일치: 코어보존+경계평탄화), void-fill flow, 누적소성변형 Σdg. ★ "응력을 *계산*"(그들) ≠ "형상이 *흐름*"(우리). 강체-구
DEM의 SHAPE 한계를 우리 MPM이 메운다 (frame[5]).

**(5) Fracture-aware Auerbach (vs 그들 파괴 미모델):**
그들은 응력만 계산하고 파괴는 "향후 과제"로 미룸. 우리는 **Auerbach/fracture-Holm**로 접촉응력→파괴를 정량(AM_P 37–40%
cracked, f_intact·frac_severe → σ 폼에 fracture 항). 그들 trade-off의 "파괴리스크"를 우리가 *수치로* 준다.

**(6) 문헌 σ_grain 앵커 (Cronau 단결정 + GB 인자):**
그들 σ_SE는 eq36의 *stack-pressure 외삽 반-경험식*(σ₀=0.002→0.0002, 게다가 σ₀>σ_max로 인쇄됨, §10). 우리는 **Cronau
2022 단결정 3.0 mS/cm × Cronau(r_SE) GB 인자**(입경별 amorphization) — 문헌-앵커된 σ_grain. 그들 σ 기준이 더 약함.

**(7) 스케일링-법칙 예측기 (σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.90):**
그들은 8 케이스 *시뮬*만 — 설계 변수→σ 예측식 없음. 우리는 88+ 케이스 코퍼스에서 **물리-앵커 스케일링 법칙**(예측기) +
Bayesian PI. 설계 입력→전체 metric 예측 (그들 미보유).

**정직하게 — 그들이 앞서는 한 가지:**
★ **포멀한 DEM→FEM 풀-셀 전기화학 커플링.** 그들은 **Butler-Volmer 충방전 echem**(전압곡선·용량·SOC·과전위·이중층
용량·고상확산)을 *실제로 푼다* — 우리는 transport σ만 있고 *충방전 echem solve가 없다*. 이건 우리 미보유 칸이고, 만약
우리가 echem을 붙이려면 그들 DEM→FEM 패턴이 청사진(B.2). 단 그들 echem-FEM의 *σ 입력*은 연속체 상한식(eq35/37)이라,
**우리 접촉망 σ를 그 echem에 입력으로 넘기면** = "우리 constriction σ + 그들 echem solve" = 양쪽 장점 결합(이상적 미래
방향). ⇒ 그들이 앞서는 건 *echem 풀이 기계*이지 *σ 물리*가 아니다 — σ 물리는 우리가 SOTA.

---

## 8. 적용 인사이트 (요약)

- ① **B6 σ-vs-compaction의 연속체-상한 reference**: 그들 eq34–38(압력→ε→S_a/τ→σ)을 우리 접촉망 σ의 *upper-bound
  sanity check*으로 (Bielefeld 2020처럼). 같은 ε_SE에서 그들 σ > 우리 σ면 constriction이 옳게 깎는 것. ⚠ LGPS라 절대값
  말고 *형태*만.
- ② **echem 결합 청사진**: 미래에 풀-셀 echem 붙일 때 = DEM/MPM에서 ε·S_a·τ·E_eff 뽑아 COMSOL Butler-Volmer에 입력
  (그들 패턴). 단 transport σ는 *우리 접촉망*에서 주고 echem-FEM엔 *그 σ를* 넘기는 하이브리드(연속체 σ식 대체 금지).
- ③ **균형 곡선**: 우리 sweep을 "응력(Auerbach) vs 전도도(삼중항)" 균형점으로 보고 — 우리는 파괴가 *정량*이라 그들보다
  정량적 trade-off 곡선 가능.

---

## 9. 인용 가능 문장 (deck/paper용)

- "A DEM→FEM multiphysics study (Lee 2024) couples particle-scale compaction to an electro-chemo-mechanical
  finite-element solve, passing compression-derived **homogenized** properties (volume fraction, Young's modulus,
  surface area, tortuosity) to a Butler–Volmer cell model — establishing the *continuum* form of the
  pressure→geometry→conductivity chain our contact-network solver computes with explicit Holm constriction."
- "Their effective conductivity is built from Maxwell/Bruggeman/linear-tortuosity continuum relations **without
  point-contact constriction** — an upper bound on a rigid-contact granular network — which our Kirchhoff/Holm
  solver corrects downward, exactly the transport-physics gap that defines our novelty (cf. Bielefeld 2020)."
- "Lee 2024 leads in one axis we lack — a formal full-cell electrochemical (Butler–Volmer) solve coupled to the
  compaction model — whereas we lead on the σ-physics itself (constriction network, σ triad, Stage-E plastic area,
  MPM particle-shape plasticity, Auerbach fracture, literature σ_grain, scaling-law predictor)."

---

## 10. 주의/한계 (over-claim 방지)

- ⚠ **소재 = LGPS (Li₁₀GeP₂S₁₂) + LLZO, NMC** — **우리 LPSCl 아님.** LGPS E=37.2 GPa ≠ LPSCl 22.1–24, σ 절대값도 다름.
  → **σ·porosity 절대값 전사 절대 금지.** 가져올 것 = DEM→FEM 커플링 패턴 + 압력→기하→σ→echem 사슬의 *정성 구조*뿐.
- ⚠ **구만 + CONTACT 탄소성** (이력 선형 스프링, **항복캡 없음**) → 진짜 SHAPE 소성 아님 (우리·Bazzoun·Varkey와 같은
  강체-구 한계). morphology·소성 floor는 우리 MPM 몫.
- ⚠ **FEM σ = 연속체 상한** (Maxwell/Bruggeman/선형 굴곡도, point-contact constriction 없음) → σ_eff는 강체-접촉
  granular망의 *upper bound* (Bielefeld 2020 동일). 우리 접촉망 σ와 직접 절대 동일시 금지.
- ⚠ **실험 검증 0** (순수 시뮬). frame[4]에서 "실험 앵커" 아님 — Bazzoun(실험 EIS)·Minnmann(EIS-TLM)과 역할 다름.
  방법론 peer로만.
- ⚠ **eq36 σ 파라미터 인쇄 이상**: σ_SE0=0.002 > σ_SEmax=0.0002 S/cm로 본문에 *그대로* 인쇄됨 (보통 σ_max>σ₀ 기대).
  오기 가능성 — eq36 σ 절대값 인용 시 주의. (k₃=70/GPa는 정상.)
- ⚠ **D_Li 단위 인쇄**: SE 확산 2.61×10⁻⁴ m²/s (Table2 인쇄 그대로; 물리적으로 ×10⁻¹² 추정 — 인용 시 단위 확인).
- ⚠ **DEM·FEM 입경 불일치**: DEM(graphite 14·NMC 12 µm) vs FEM R_p(graphite 10·NMC 5 µm) — 두 모델이 다른 입경 가정.
  DEM은 압밀-패킹용, FEM은 대표-입자 확산용 (의도적이나 absolute 매칭 주의).
- ⚠ **외부압 sweep 0–100 MPa**: 50–100 MPa는 *고압 운용* → Doux 최적 5 MPa·우리 작동압 창(5–40)보다 높음. "외부압↑→
  echem↑"을 우리 저압 작동 결론으로 무한 외삽 금지(그들도 50 이상 포화 명시).
- ⚠ **단방향 DEM→FEM** (피드백 없음) → echem 중 입자 재배열·force chain 변화 미반영. 우리 scaffold도 단방향이나 *위치*
  전달이라 입자정보 보존; 그들은 *호모지나이즈 스칼라*라 입자정보 소실.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
