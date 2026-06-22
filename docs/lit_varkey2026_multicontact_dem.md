# Varkey 2026 (Adv. Powder Tech. 37, 105338) — 다중접촉 탄소성 DEM

**인용:** C.A. Varkey, K. Giannis, S. Melzig, C. Schilde, S. Zellmer, "DEM simulation of
solid-electrolyte separator and cathode densification using a stress-based multi-contact
elasto-plastic model", Advanced Powder Technology 37 (2026) 105338 (오픈액세스 CC-BY,
DEM10 특별호).  Fraunhofer IST + TU Braunschweig, HELENA 프로젝트 (할라이드 SSB).

**소재:** Li₃YBrCl₆ **할라이드** SE (우리의 LPSCl Li₆PS₅Cl 황화물이 **아님**) + NMC-811 + SBR 바인더 + CB.

DB 동반 파일: `docs/data/densification_porosity_db.csv` (우리 porosity 관계식 fit용으로 정리한
이들의 P-vs-porosity 데이터점).

---

## ★ 결론 — 정말로 소성변형을 기술하는가?  아니다 (입자 형상이 아니라 접촉(contact) 소성만)

이것은 **여전히 강체 구(rigid-sphere) DEM**이다.  "탄소성(elasto-plastic)"은 전적으로
**접촉**(힘-변위 법칙)에서의 일이지 **입자**의 일이 아니다.  입자는 완벽한 구로 남아
**형상이 절대 변하지 않는다**.  논문이 직접 그렇게 명시한다 (p.12):

> "Even though the halide solid electrolyte particles are irregular in shape, … a compromise
> on the choice of particle shape is made.  A new set of study employing more realistic
> particle shapes can be done in future."

⇒ "입자 **구조(STRUCTURE)**의 소성변형"(분체층이 치밀화됨) ✓  ≠
  "입자 **형상(SHAPE)**의 소성변형"(morphology) ✗.  겹침(overlap) δ는 소성에 대한
  기하학적 **프록시**일 뿐, 실제 재료 흐름(flow)이 아니다.

---

## ★ 탄소성 모델을 어떻게 적용했는가 — 지배방정식

### 1. Thornton–Ning 법선 접촉 (§2.2) — 접촉당 탄소성 법칙
유효 탄성계수 / 반경 (eq 3):
```
1/E* = (1−ν_i²)/E_i + (1−ν_j²)/E_j      1/R* = 1/r_i + 1/r_j
```
**탄성(Hertz) 영역**, 겹침 δ < δ_y 인 동안 (eq 2):
```
F_el = (4/3)·E*·√(R*·δ³)
```
접촉 반경 (eq 4):  `a = ( 3·F·R* / (4·E*) )^(1/3)`.
임계 항복압력 p_y 에서의 **항복 개시** → 임계 힘/겹침 (eq 5):
```
f_y = (1/6)·(R*/E*)²·(π·p_y)³        δ_y = (1/4)·(R*/E*²)·(π·p_y)²
```
**소성 영역**, δ ≥ δ_y (eq 6) — 항복 후 겹침에 대해 **선형(LINEAR)**으로 가는 점에 주목:
```
F_el-pl = f_y + π·p_y·R*·(δ − δ_y)
```
**제하(unloading)** 시 더 평평한 유효 소성반경 R_p* 와 잔류 겹침 δ_R 사용 (eq 7):
```
F_unloading = (4/3)·E*·√( R_p*·(δ − δ_R) )      → 영구변형 + 에너지 소산
```
접선방향, Coulomb 결합 (eq 8):  `F_tangential = −μ·F_n·(s_t/|s_t|)`.
보정된 **항복비(yield ratio) = 0.0103** (겹침 약 1.03 %에서 소성 시작).

### 2. 응력 기반 다중접촉 결합 (§2.3, Giannis [24]) — 이 논문의 신규성(NOVELTY)
한 입자의 Poisson 측방 팽창이 그 입자의 **다른** 접촉들을 밀어낸다(구속, confinement) —
고전적 **쌍별(pairwise)** DEM이 무시하는 다체(multi-body) 효과.  분지벡터 lⁿ 과 접촉력 fⁿ 의
dyad를 입자의 모든 NP개 접촉에 대해 합하고 입자 부피 Vᵖ 로 나눈 입자별 응력텐서 (eq 9):
```
σᵖ = (1/Vᵖ)·Σ_{n=1..NP} lⁿ ⊗ fⁿ
```
트레이스에서 나오는 다중접촉 압력 (eq 10)과 그것이 더해주는 추가 법선력 (eq 11):
```
P_ij = ( tr(σ_i) + tr(σ_j) ) / 3        F_mc = (β·ν·a_ij)·P_ij        (β = 0.5 보정값)
```
**결합된** 법선력 (eq 12–13):
```
loading:    F_{i-j} = F_el     + F_mc   (δ < δ_y)
            F_{i-j} = F_el-pl  + F_mc   (δ ≥ δ_y)
unloading:  F_{i-j} = F_unloading + F_mc (δ ≥ δ_y)
```
→ 이 항은 구속이 강해질수록(접촉이 많을수록 ⇒ tr σ 가 커짐) 커지므로
**상대밀도 > 0.7**(치밀 영역)에서만 의미가 있고, 그 아래에서는 거의 무시할 만하다.

### 3. 결합(bond) 모델 (§2.4, Sangrós [38]) — 바인더(SBR) + 카본블랙
i,j 사이 결합 조건 (eq 14) `d_ij < (r_i+r_j)(1+f)`; 결합 반경 (eq 15) `r_b = α_b·min(r_i,r_j)`.
스프링-대시팟 힘/모멘트 변화율 (eq 16–19): `dF_b,n/dt = −v_n·S_n·A`, … 법선/접선 결합강성
S_n=2.5e13, S_t=1.875e13 N/m³, 감쇠 0.9997; α_b 는 결합 부피 = 실험 바인더 부피분율이
되도록 조정 (α_b 하단/상단 구배: separator 0.45/0.2, cathode 0.35/0.25).

### 4. Porosity / 읽어내기(readout)
공극률 (eq 20): `ε = 1 − m/(ρ_eff·t·A)`.  겹침 % (eq 22): `δ% = δ/min(r_i,r_j)·100`.
EIS로부터의 이온전도도 (eq 21): `σ = l/(R·a)`; 그리고 입자내부 R_p(길이) + 접촉 R_c(면적) +
결합 R_b 로 이루어진 저항 네트워크 (Fig 3, Sangrós [39])를 풀어서 σ_ionic 산출.

### 접촉모델 비교 결과 (Fig 6, 8) — 왜 다중접촉이 중요한가
- **Hertz**: 힘을 과대평가(항복 없음) → 두께/압력을 엄청 높게 예측.
- **Thornton–Ning**: 항복 후 편차(더 낮은 힘, 잔류 겹침) → 개선됨, 실험 두께에 대해
  약 300 MPa로 추정.
- **다중접촉 탄소성**: 높은 겹침(>24 %)에서 구속력을 더함 → 올바른 350 MPa에서 실험
  두께와 일치.  "상대밀도 > 0.7 에서는 Hertz / Thornton–Ning 권장하지 않음; 다중접촉 필요."

---

## ★ 부족한 부분 — 우리 DEM+MPM 프레임 대비 어디가 모자란가

| # | 이들 모델에 없는 것 | 우리 모델은 있는 것 |
|---|---|---|
| 1 | **입자 형상(SHAPE) 변화** — 구만, δ는 프록시 | MPM: 진짜 소성 morphology (SEM의 코어 보존 + 경계 평탄화, ✓ 일치) |
| 2 | **부피보존 공극채움 흐름(FLOW)** — 재배열+겹침으로 치밀화 | MPM: SE가 공극으로 소성 흐름(ν=0.49, K 실제값) → 패킹 바닥 아래로 |
| 3 | **20 % 미만 porosity** — 명시적으로 "추구 안 함"(비용); 바닥 21/37 % | 우리는 일상적으로 10–16 % 도달 (실제 ASSB >95 % 밀도: Minnmann 10 %, real_14 15.6 %) |
| 4 | **소성변형률 장(FIELD)** — 공간적 Σdg / 손상 개시 없음 | MPM Σdg 장 (화학-역학 열화 개시, 균열 시딩) |
| 5 | **수송 삼중항(TRIAD)** — σ_ionic만 | σ_ionic + σ_electronic + σ_thermal, 검증된 스케일링 법칙 (LOOCV 0.97/0.95/0.90) |
| 6 | **Coverage** — "접촉 표면적 %"(8–13 %), 접촉면적 분율일 뿐 | SE에 의한 AM coverage, plastic(변형)·rigid(기하) Hertz/Tabor 밴드 |
| 7 | **AM 균열 / Auerbach** — 바인더 결합파단만, CAM 입자 균열 없음 | DEM 균열인지 Holm (f_intact), Auerbach, force-chain, 침투(percolation) |
| 8 | **다중접촉은 쌍별 보정(CORRECTION)** — 접촉당 평균장 P_mc, 준독립적 | MPM 연속체는 모든 재료점을 응력장으로 **고유하게(NATIVELY)** 결합(엄밀, 평균장 아님) |
| 9 | **소재 = 할라이드** (E=10.58 GPa) — 수치가 LPSCl로 전이 안 됨 | LPSCl 기준 (E_eff 1.35 / 실제 24, Minnmann/Cronau) |

핵심: 1–4 항목은 임의의 강체 구 DEM에 대해 우리 **프레임 [1]/[2]**가 지목하는 바로 그 한계다.
이들의 다중접촉 항(#8)은 치밀영역 힘에 대한 영리한 DEM 패치이지만, 그래도 연속체(우리 MPM)가
엄밀하게 하는 것을 근사한 것에 불과하며 — 입자를 변형시키거나 공극으로 흐르게 할 수는 없다.
이들의 정직한 "구 = 타협, <20 % = 향후 과제"가 바로 **우리의 분해입자 소성 MPM이 메우는 그 간극**이다.

### 이들이 앞서는 부분 (도입/연구 가치 있음)
- **다중접촉 구속항 F_mc** = 물리적으로 투명한 치밀영역 힘 보정.  우리의 대응물은 경험적
  18× E 연화(softening).  연구 거리: 우리 연화가 사실상 P_mc를 재현하는가?  (같은 증상 —
  ρ>0.7 에서 쌍별 Hertz가 너무 뻣뻣함 — 다른 메커니즘.)
- **명시적 바인더(SBR) + CB 결합모델** 과 그 자체의 이온저항 R_b — 우리는 바인더를 역학적으로도
  전기화학적으로도 모델링하지 않음.  SBR/CB를 추가할 때 유관.
- **다중압력 실험검증** (100–350 MPa, separator AND cathode 둘 다, 두께 < 1 % 일치) —
  우리의 단일점(Minnmann) / Heckel 기준을 완전한 검증된 압력 스윕으로 확장하는 템플릿.
- **Thornton–Ning 정식 항복법칙** 과 잔류 겹침 — 교과서적 탄소성 접촉; 우리 hooke/hysteresis는
  더 단순함 (Stage-E가 소성 면적(AREA)을 별도로 더함).

---

## ★ 프레임 [5] 확증 — 최신 DEM이 우리 MPM이 메우는 간극을 스스로 인정한다

접촉법칙에서 우리보다 더 정교한(Thornton–Ning + 다중접촉 vs hooke/hysteresis + 연화) 2026년
동료심사 DEM이, 여전히 **DEM / 수송** 쪽에 있다: 접촉 네트워크, 접촉면적 성장,
**이온전도도**(R_p+R_c+R_b 네트워크 — 우리 Kirchhoff/Holm 대응물), porosity-vs-pressure,
패킹을 소유하면서 — 그 한계(구 형상, 20 % 미만 porosity 불가, "현실적 형상 = 향후 과제")를
명시적으로 이름 붙인다.  분해입자 소성영역 + 20 % 미만 porosity + morphology 는 강체 구 DEM을
넘어서는 방법이 필요하다는 **독립적 확증**으로 인용.  우리 DEM↔MPM 분할은 변명이 아니다 —
선도 연구그룹도 같은 벽에 부딪히고 그것을 향후 과제로 라벨링한다.

---

## ★ POROSITY 관계식에서 배울 점 (목표: 우리 porosity 관계식 추출)

### 데이터 (두께 = Fig 9/12 범례에 정확히 명시; porosity ≈ Fig 10/13 디지타이징)
**Separator** (할라이드 SE 97 wt% + SBR 3 wt%, 단봉(unimodal), E_SE=10.58 GPa):

| P (MPa) | porosity ≈ | h_c sim/exp (µm) |
|---|---|---|
| 0 | 45 % | (h_a 초기) |
| 100 | 35 % | 188.2 / 186 |
| 200 | 31 % | 170.3 / 171 |
| 300 | 25 % | 152.7 / 154 |
| 350 | 21 % | 143.5 / 145 |

**Cathode** (NMC-811 77.6 + SE 17.43 + SBR 3 + CB 0.97 wt%, 이봉(bimodal)):

| P (MPa) | porosity ≈ | h_c sim/exp (µm) |
|---|---|---|
| 0 | 49 % | (h_a 초기) |
| 125 | 39 % | 146.6 / 145.2 |
| 200 | 38 % | 141.2 / 140.5 |
| 300 | 37.5 % | 137.7 / 137.1 |
| 350 | 37 % | 135.6 / 135.3 |

DoD = (h_a − h_c)/h_a.  두 곡선 모두 **약 100 MPa에서 기울기 변화 = 탄성→소성 전이**를 보임
(이들 표현) — 우리 DEM Heckel P_y = 138 MPa 와 대응.

### 핵심 통찰: porosity 바닥(FLOOR)은 (E_SE, 조성, 흐름 메커니즘)이 결정한다
| | 이들의 할라이드 | 우리 LPSCl |
|---|---|---|
| SE Young's E | 10.58 GPa | E_eff 1.35 (MPM 1.53), 실제 24 |
| separator / 순수-SE 바닥 | **21 %** @350 | **~10 %** @300 (Minnmann) |
| AM-rich cathode 바닥 | **37 %** @350 | **15.6 %** (real_14 @300) |

같은 압력 범위에서 우리가 **약 2× 더 치밀** — 이유는 (a) LPSCl E_eff가 할라이드보다 약 8× 더
물러서(더 뻣뻣한 SE ⇒ 더 높은 잔류 porosity; 정확히 우리 MPM E-스윕 E24→33-38 %, E1.35→8 %),
그리고 (b) 우리 DEM 연화 + MPM 소성 **흐름**이 이들을 약 20 %에 가두는 강체 구 패킹 바닥
아래로 도달하기 때문.

⇒ **우리 porosity 관계식은 반드시 E_SE(강성) 항과 조성 항을 가져야 하며**, 소성 흐름이
포함되지 않는 한 약 20 %는 강체 구의 단단한 바닥이다.  Heckel `ln(1/(1−D)) = K·P + A`가
후보 형태 (우리 DEM에 대해 보유: R²=0.965, P_y=138 MPa); 이들의 독립적(더 뻣뻣한 SE) 데이터로
K와 탄성→소성 무릎(knee)을 교차검증할 수 있다.

### 소재 기준값 (Table 1)
- 할라이드 SE: E=10.58 GPa, ν=0.3, ρ=2.6 g/cm³, d10/50/90 = 1.1/2.1/3.8 µm.
- NMC-811: E=140 GPa, ν=0.25, ρ=4.75 g/cm³, d=2.6/3.4/6.1 µm.  (우리 E_AM=140 ✓)
- NMC "반경의 0.10 %까지 탄성, 이후 소성" — 항복 개시 기준값.
- 할라이드 고유 이온 σ = 1.8 mS/cm → 구속 separator 유효 0.0025–0.005 mS/cm.

---

## 실행 항목 (Action items)
1. **Porosity 관계식:** separator + cathode 데이터(`docs/data/densification_porosity_db.csv`)에
   Heckel 피팅; K / P_y 를 우리 DEM(P_y 138 MPa)과 비교 → 탄성→소성 무릎이 소재 일반적임을
   확인; 우리 porosity 스케일링에 **E_SE 바닥 항** 추가.
2. **프레임[5] 인용:** Varkey 2026 = 우리 MPM이 다루는 구-형상 / 20 % 미만 한계를 스스로
   이름 붙인 독립 DEM.
3. **(선택) 다중접촉 vs 연화 연구** — 치밀(ρ>0.7) 영역에서 F_mc ≈ 우리 18× 연화 인가?
