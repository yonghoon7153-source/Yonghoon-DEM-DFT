# ⭐frame[5] *사이클 응력* DEM — Understanding mechanical stresses upon solid-state battery electrode cycling using the discrete element method — Alabdali, Zanotto, Chouchane, Ngandjong, Viallet, Seznec, Meng, Franco (Energy Storage Materials 2024)

> slug `dem_mechanical_stresses_ssb_electrode_cycling` · DOI `10.1016/j.ensm.2024.103527` · type `DEM (LIGGGHTS, Hertz; uniaxial+isostatic compaction → cyclic AM expansion/contraction → per-particle stress; σ_el·τ via GeoDict ConductoDict/DiffuDict)` · PDF `DEM_MechanicalStresses_SSB_ElectrodeCycling.pdf` · digested `2026-06-26` · status ✅ · WISHLIST #47 (★ DEM mechanical stresses during CYCLING — frame[5] 사이클축)
>
> ## ★★★ 이 논문의 위치 — frame[5] *사이클(작동-시점) 응력* 의 **DEM 경로** (우리가 *압밀*만 보던 시간축의 *직접* DEM 확장) ★★★
> **Alejandro A. Franco 그룹 (LRCS Amiens + ARTISTIC initiative; +UCSD Shirley Meng + U. Chicago)** 의 **자체 DEM**.  ★ 우리(Yonghoon DEM)는 *제조-시점* 압밀 구조→수송 σ 만 계산하고 **사이클 중 응력 진화는 frame[5] 공백**인데, 이 논문이 **바로 그 칸을 *우리와 같은 종류의 DEM*(LIGGGHTS, Hertz 접촉, 구 입자)으로** 채운다:
> **(1) uniaxial 375 MPa 압밀 → (2) relaxation → (3) isostatic 1/3/5 MPa 압밀 → (4) AM 입자를 5 사이클 ±6 % 부피로 *팽창·수축* → 각 입자에 걸리는 *응력*을 SOC·입경·z-위치별로 읽는다.**  ⇒ **Bucci 2017 FEM-CZM / So 2021 ductile-DEM 과 *같은 frame[5] 칸, 또 다른 방법***.
>
> ★ **세 자매 사이클 논문의 분담(외우기) — 같은 frame[5] 칸, 세 방법:**
> - **Bucci 2017 (FEM-CZM)**: 연속체 FEM + cohesive-zone, **SE 상 *취성* 균열**, driver = Vegard 팽창, **균열 *예측*(7.5 % 임계)**.
> - **So 2021 (ductile-DEM)**: 입자 DEM + CONTACT 소성 + 융착, **SE *연성* + 접촉손실·균열·κ 영구감소**, driver = Si 팽창, **σ(=κ_SE^rel) *열화 시계열***.
> - **이 논문 (Franco DEM, 2024)**: 입자 DEM(LIGGGHTS, Hertz, **rigid 구**), **사이클 ±6 % 팽창/수축 → *응력 분포*(SOC·입경·z)**, **균열 *없음*(응력만; "균열 위험"은 *해석*)**.  ⇒ **우리 LIGGGHTS+DEM 파이프라인에 *가장 가까운* 코드/방법** (Bazzoun 과 같은 ARTISTIC 계보).
>
> ★ **세 핵심 결과(외우기):**
> 1. **Uniaxial 375 MPa 는 입자에 *과도한* 응력**(z축 AM **>500 MPa, 일부 700 MPa**; AM 응력 ≈ **2× SE 응력**) → **AM 균열·SE 변형 위험↑.  Isostatic(1–5 MPa)는 같은 압밀도를 *수십 배 낮은 응력*(σ ~6–16 MPa)로** 달성 → 같은 σ_el·τ 를 *훨씬 덜 파괴적*으로 얻음.  = **"고압 단축 ≈ 저압 등방 in 전도도, but 등방이 응력 면에서 우월"** 이 논문의 핵심 메시지.
> 2. **★ 입경-응력 상관(중요):** **작은 입자가 큰 입자보다 *높은* 응력**(Fig 4/5 중앙열, 단조감소) → **작은 AM 일수록 사이클·압밀 응력 집중** (Bucci/Kang 의 "큰 입자가 깨진다"와 *driver·방향이 다른* 결과 — §우리-대비에서 정밀 구분).
> 3. **★ 사이클 응력의 *비대칭 진화*:** **방전(discharge, AM 팽창)** → AM-SE 응력차 *벌어짐*(AM 더 받음); **충전(charge, AM 수축)** → 응력이 SE 로 *이전*(AM 부피↓ → SE 가 받음) → 더 *균일*한 응력장 → **충전 후 더 균일한 이온 percolation**.  → 사이클마다 응력장이 *재분배*.
>
> ⚠ **소재/방법 정렬 — 우리와 *거의* 같음(드물게 좋은 정합):** SE = **Li₆PS₅Cl (LPSCl, 우리와 동일!)** 73.30 wt%, CAM = **NMC532 (LiNi₀.₅Mn₀.₃Co₀.₂O₂)** 26.7 wt% (⚠ 우리 production 은 NMC**811** — 같은 NMC 계열이나 *조성 다름*).  code = **LIGGGHTS (우리와 동일)**, 접촉 = **Hertz(Granular Force Field, GFF)**, **rigid 구** (소성·형상변화 *없음*).  ⇒ porosity·σ 절대값은 *NMC532·조성차* 로 직접 동일시 주의하나, **방법·메커니즘·추세는 우리에 *가장* 직접 전이 가능**.
> ⚠ **이 논문은 *응력*과 *기하 descriptor*(σ_el normalized·τ)만 — 진짜 σ_ionic/σ_e *절대값* 솔버 없음(GeoDict ConductoDict/DiffuDict = *상대* σ_el·τ); 균열·소성·morphology *없음*; AM 팽창은 *균일 rate*(확산분포 무시, 저자 명시).**

---

## 1. 한 줄 요약
**황화물 ASSB 복합 *양극*(LPSCl + NMC532)의 *제조*(uniaxial 375 MPa → relaxation → isostatic 1/3/5 MPa)와 *전기화학 사이클*(NMC 입자를 5 사이클 ±6 % 부피로 팽창/수축)을 *하나의 DEM 워크플로*(LIGGGHTS, Hertz, rigid 구)로 이어, 각 단계·각 입자에 걸리는 *기계 응력*을 SOC·입경·z-위치별로 정량화** — 핵심: **(a)** uniaxial 375 MPa 압밀은 입자에 *과도한* 응력(z축 AM >500–700 MPa, AM ≈ 2× SE)을 주어 AM 균열·SE 변형 위험을 키우는 반면, **isostatic(1–5 MPa)** 은 *비슷한 전도도*(σ_el·τ)를 **한두 자릿수 낮은 응력**으로 달성 → *덜 파괴적*; **(b)** **작은 입자가 더 높은 응력**(입경-응력 단조감소); **(c)** 사이클 중 응력장이 *비대칭으로 재분배* — 방전(AM 팽창) 시 AM 이 더 받고, 충전(AM 수축) 시 응력이 SE 로 이전돼 *더 균일*해진다.  ⇒ 우리 frame[5] *사이클 응력* 시간축 공백을 **우리와 거의 같은 LIGGGHTS-DEM 으로** 채우는 *직접 청사진* (Bucci FEM-CZM·So ductile-DEM 의 세 번째 형제; 단 *균열·소성·절대 σ* 는 미보유 → 우리 Stage-E/MPM/fracture/삼중항이 *위*에 얹힐 자리).

이 논문이 우리에게 주는 정확한 자리: 우리 **DEM 압밀 응력장**(von Mises CV, force-chain, AM_P stress ratio)이 *제조-순간* 의 한 스냅샷이라면, 이 논문은 그 *위에* **AM Vegard ±6 % 팽창을 LIGGGHTS 에 부과**해 *사이클마다* 응력이 어떻게 재분배되는지를 보여준다 — **우리 input 스크립트에 AM 입경 swing(`fix adapt`/반경 재설정)만 추가하면 재현 가능한 *직접* 확장**(우리 backlog **A10 사이클 chemo-mech** 의 *DEM* 구현 레퍼런스).

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Mohammed Alabdali**ᵃ·ᵇ, **Franco M. Zanotto**ᵃ·ᵇ, **Mehdi Chouchane**ᶜ, **Alain C. Ngandjong**ᵃ·ᵇ, **Virginie Viallet**ᵃ·ᵇ, **Vincent Seznec**ᵃ·ᵇ·ᵈ, **Ying Shirley Meng**ᶜ·ᵉ, **Alejandro A. Franco**ᵃ·ᵇ·ᵈ·ᶠ·\* |
| 소속 | ᵃ **Laboratoire de Réactivité et Chimie des Solides (LRCS), Université de Picardie Jules Verne**, CNRS UMR 7314, 15 rue Baudelocque, 80039 Amiens, France · ᵇ **RS2E** (Réseau sur le Stockage Électrochimique de l'Énergie), CNRS FR 3459 · ᶜ **Pritzker School of Molecular Engineering, University of Chicago** · ᵈ **ALISTORE-European Research Institute**, CNRS FR 3104 · ᵉ **Dept. of NanoEngineering, University of California San Diego (UCSD)** · ᶠ **Institut Universitaire de France (IUF)**, Paris |
| 교신 | **Alejandro A. Franco** (alejandro.franco@u-picardie.fr) |
| 저널/년 | **Energy Storage Materials 70 (2024) 103527** (Received 5 April 2024, revised 27 May 2024, accepted 29 May 2024, available online 30 May 2024) |
| DOI | **10.1016/j.ensm.2024.103527** · open access (CC BY 4.0), 2405-8297/© 2024 The Authors, Elsevier |
| 자금 | **Umicore (DESTINY PhD Programme**, EU Horizon2020 MSCA COFUND grant #945357) + **ERC** ("ARTISTIC" grant 772873 + "PULSELiON" 101069686 + ERC PoC "SMARTISTIC" 101069244) + U. Chicago–France ("FACCTS" 2023) + IUF |
| 연구유형 | **DEM 시뮬레이션** (LIGGGHTS, Hertz Granular Force Field) — *제조*(uniaxial+isostatic 압밀) + *사이클*(AM ±6 % 부피 팽창/수축) 의 **기계 응력 분석** + σ_el·τ 기하 descriptor.  실험 *없음*(이전 실험 프로토콜 ref [28] 기반).  ★ ARTISTIC 3D-resolved physics-based 모델 계보 |
| 모델 시스템 | **복합 *양극*(positive electrode/cathode)** — AM(NMC532) + SE(LPSCl) **2-상**, **carbon/binder *없음***(simplified 2-phase) |
| AM (CAM) | **NMC532 = LiNi₀.₅Mn₀.₃Co₀.₂O₂**, **26.7 wt%**, **PSD 3–10 µm** (사이클 시 **±6 % 부피** 팽창/수축 — Vegard) |
| SE | **Li₆PS₅Cl (LPSCl, argyrodite — 우리와 동일 소재!)**, **73.30 wt%**, **PSD 6–13 µm** (⚠ 이 논문은 SE 가 AM *보다 큼* — 우리 12:4:1 과 반대 size-ordering) |
| 도전제/바인더 | **없음** ("simulated composite cathodes consist of two types of materials" — carbon/binder 제외, 2-phase RVE) |
| code | **LIGGGHTS** (Newtonian eqns of motion; ref [29]) — **= 우리 코드** |
| 접촉/물성 | **Hertz** (Granular Force Field, GFF) + **Young's modulus·Poisson ratio·friction·COR** from refs [30,31] (= **Cronau/Pierce sulfide·NMC** 물성; SI 에 GFF 상세) |
| 도메인/HW | **150 × 150 × 150 µm³** 초기 box, **11,002 입자** (AM+SE), **AM mass loading 14.96 mg/cm²**.  MatriCS 플랫폼 (UPJV), 375 GB RAM, Intel Xeon Gold 6148 @2.40 GHz, **40 코어 1 노드** |

> ★ **계보:** ARTISTIC initiative(ref [22–25] Ngandjong·Chouchane 등 LIB 전극 DEM) → wet-process SSB(ref [26,27]) → *이 논문*(SSB 압밀+사이클 응력).  **Shi et al.(2020, ref [14])** = 같은 그룹 선행 SSB-DEM (cathode utilization V_AM^active/V_AM 정의 + PSD 효과 — 본문 Intro 에서 명시 계승).  **Torayev et al.(ref [38])** = 같은 그룹 tomography 기반 pore arrangement.  ref [14] Shi = "큰 AM/SE size 비 → 높은 AM loading → 용량↑" (우리 Furnas·bimodal 과 같은 결).

---

## 3. 핵심 물성 (수치)
> 데이터 CSV: `docs/data/dem_cycling_stresses.csv` (compaction / cycling-stress / params 3 블록).  ⚠ 이 논문의 정량 앵커는 **(i) 압밀 box 치수 진화(thickness)·(ii) uniaxial vs isostatic *응력 규모*·(iii) 입경-응력·z-응력 곡선·(iv) σ_el/σ_AM·τ 진화** 다 — **porosity·σ_ionic 절대값·coverage·coordination·Heckel·σ_y 는 *미보고*(n/a)** → 우리 압밀/전달 앵커(Minnmann 14 %, Doux 18 %, 우리 15.6 %; σ_ionic 0.04–0.18)와 **직접 비교 금지**.

### 3.1 ★ 압밀 — box thickness 진화 (Fig 2–3, M1, digitized)
| 단계 | z-thickness | 횡(xy) | src | 비고 |
|---|---|---|---|---|
| 초기 생성 | (150 µm box 내, 11,002 입자) | 150 × 150 µm | stated | NVE, T=300 K, AM loading 14.96 mg/cm² |
| **uniaxial 압밀 (375 MPa)** | **84 µm** | 150 × 150(주기) | digitized (Fig 2) | z 고정, xy 주기; 375 MPa 도달까지 (~400 µs) |
| **relaxation** (→1 atm) | **84 → 95 µm** (springback) | 150 × 150 | digitized (Fig 2–3) | 압력 해제 → 부분 회복(영구변형 + 탄성 회복) |
| **isostatic 압밀 (5 MPa)** | **95 → 125 µm** | **130 × 130 µm** (전 방향 압축) | digitized (Fig 3) | ⚠ thickness *증가*(95→125)는 isostatic 이 *모든 면*을 누르며 xy 가 150→130 으로 줄고 z 가 *재배열*된 결과(box 비등방 → 등방화) |
> ★ **읽는 법:** uniaxial 은 z 만 눌러 *얇고*(84) 응력 큼; relaxation 후 *부풂*(95); isostatic 은 xy 도 눌러(150→130) 더 *균일*·*저응력*.  thickness 절대값은 *box 정의*(xy 가 150→130 변하므로 z 증가가 *밀도 감소* 아님 — 부피로 봐야 함) → **porosity 절대값을 thickness 단독으로 읽지 말 것.**

### 3.2 ★★ Uniaxial 375 MPa 응력 (Fig 4, M1, digitized — 이 논문의 *심장* ①)
| 양 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **x축 응력 (AM)** | **~340–400 MPa** (z 위치 따라 fluctuate, plateau ~340) | uniaxial 375 MPa, 횡방향 | digitized (Fig 4 좌상) | AM 이 SE 보다 ~2× |
| **x축 응력 (SE)** | **~150–200 MPa** | 동일 | digitized | "stress on SE reduced by factor of two vs AM, on average" (stated) |
| **y축 응력 (AM/SE)** | x축과 유사 (~340–400 / ~150 MPa) | uniaxial, 횡 | digitized (Fig 4 중) | 횡(x·y) 응력은 압력경계(375)에 *못 미침* — bulk 가 위·아래 plate 압력 받아 더 높음 |
| **★ z축 응력 (AM)** | **~500–700 MPa** (peak ~700, plateau ~600) | uniaxial, *가압 방향* | digitized (Fig 4 좌하) | ★ **압력경계(375)보다 *높음*** — bulk 가 양면 plate 압력 받음; **작은 AM >500 MPa in all dims** |
| **z축 응력 (SE)** | **~250–450 MPa** | 동일 | digitized | AM 의 ~2/3 |
| **★ 입경-응력 (AM, Fig 4 중앙열)** | **단조 감소**: 입경 2 µm ~390 → 6 µm ~250 MPa (x/y); z 는 ~650→400 | particle radius 2–6 µm | digitized | ★★ **작은 AM 이 더 높은 응력**(edge·직접접촉 입자가 더 받음) |
| 응력 공간분포 | bottom·top 영역 응력 *낮음*, bulk 가 *높음* | Fig 4 우측 컬러맵(0–500 MPa) | stated | "particles in bottom and top experience less stress; bulk higher (pressure of both top+bottom plates)" |
| **AM/SE 응력비** | **AM ≈ 2 × SE** (평균) | 모든 축 | stated | "stress on SE reduced by factor of two w.r.t. AM, due to deformability + lower mechanical stiffness of SE" |
> ★★ **핵심:** uniaxial 375 MPa → **z축 입자응력 500–700 MPa**(경계압의 1.3–1.9×, AM); **AM 이 SE 의 2×** → "high pressures, AM cracking risk, shortened lifespan" (본문).  M2·S5(다른 seed)도 같은 size-dependent 거동(Fig S2).

### 3.3 ★★ Isostatic 1/3/5 MPa 응력 (Fig 5, M1, digitized — 이 논문의 *심장* ②)
| 양 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **isostatic 평균 응력 (x축)** | **~400 MPa? → 아니, 6–16 MPa** | ⚠ **5 MPa isostatic** | stated | ★ 본문: "average stress values of almost **400 MPa along x, 380 along y, 700 along z** for isostatic" ← ⚠ 이는 **uniaxial** 문장(Fig 4 재서술)이고, **isostatic 은 stress varies 6–16 MPa along x·y, 6–16 along z** (바로 다음 문장) |
| **★ isostatic 응력 범위 (x·y·z)** | **6 – 16 MPa** | isostatic 5 MPa | **stated** | ★★ "for isostatic compression, stress varies between **6–16 MPa** along x and y axes, and **6–16 MPa** along the z axis" — uniaxial(수백 MPa) 대비 **~2 자릿수 낮음** |
| isostatic 응력 (Fig 5a 세로축) | x·y: ~6–16 MPa; z: ~6–16 MPa | isostatic 1/3/5, AM·SE | digitized (Fig 5a, 컬러바 0–10 MPa) | "nearly **two orders of magnitude lower** than uniaxial" (stated) |
| **isostatic AM vs SE** | AM 여전히 SE 보다 약간↑ (방전 전) | isostatic, charge/discharge | digitized (Fig 5a) | "AM experiences higher stress vs SE due to deformable/soft SE" (방전 전) |
| **입경-응력 (isostatic)** | 여전히 **작은 입자 ↑** (단조감소, 약함) | Fig 5a 중앙열 | digitized | "particles in direct contact with planes endure higher stress, particularly larger particles at edges, decreasing toward core" |
| **Fig 5b 응력 히트맵 (xy 평균, z방향)** | **6 – 35 MPa** (대부분 20–25, 국소 hot-spot) | isostatic 5 MPa, charge/discharge, M1·M2 | digitized (Fig 5b, 컬러바 6–35 MPa) | M2 가 M1 보다 *불균일*(특히 y 하반부) → packing heterogeneity |
> ★★ **핵심 메시지(본문):** "Isostatic pressing at low pressures (1–5 MPa) demonstrates the potential to achieve **conductivity levels comparable to uniaxial pressing at nearly twice the order of magnitude** [lower stress] ... a promising avenue ... when uniaxial typically demands **300–500 MPa**."  ⇒ **같은 σ_el·τ 를 ~100× 낮은 응력으로** → AM 균열·SE 변형 *덜*.

### 3.4 ★★ 사이클 중 응력 진화 (Fig 5a, charge/discharge, digitized — *심장* ③)
| 양 | 거동 | src | 비고 |
|---|---|---|---|
| **AM 부피변화 (Vegard)** | **±6 %** (lithiation 팽창 / delithiation 수축), **5 사이클** | stated (§2.1.3) | "size of all AM particles expanded and contracted by **6 %** for five consecutive cycles to model behavior upon lithiation/delithiation" |
| **방전(discharge, AM 팽창) 전** | **AM 응력 > SE 응력**(차 큼) | stated (Fig 5a) | "Before AM increases while discharging, AM experiences higher stress vs SE due to deformable/soft SE" |
| **방전 진행 (AM 팽창)** | **AM-SE 응력차 *벌어짐*** (AM expansion → contact points/forces↑) | stated | "gap in stress widens with AM particle expansion under load" |
| **방전 끝 (full discharge)** | 응력차 *좁아짐* → AM·SE 비슷 | stated | "stress gap decreases until both AM and SE reach similar stress levels" |
| **★ 충전(charge, AM 수축)** | **응력이 AM → SE 로 *이전***(AM 부피↓ → SE 가 받음) | stated | "significant shift: AM contract back to original size → **transfer of stress to SE particles** as AM occupy less volume → **more homogeneous stress distribution** after charge" |
| **충전 후 횡(x·y) 응력** | 가장자리↑·코어↓ (변동) | stated | "lateral stress towards edges in x·y, decreases towards core → impacts ionic·electronic pathways" |
| **균일성 효과** | 충전 후 *더 균일* → **더 두드러진 이온 percolation 경로** | stated | "concentrated stress distribution generates more prominent ionic percolation pathways" |
> ★★ **읽는 법(사이클 비대칭):** **방전(팽창)** = AM 이 SE 를 밀어 *AM 응력↑·불균일*; **충전(수축)** = AM 이 비워준 자리 응력이 SE 로 *재분배* → *더 균일*.  사이클마다 응력장이 **AM↔SE 사이를 왕복** — 이것이 "사이클 응력 진화"의 본체.  ⚠ 균열·접촉손실은 *모델 안 함*(응력만; 위험은 *해석*).

### 3.5 ★ σ_el·τ 진화 (Fig 6, normalized — 기하 descriptor)
| 양 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **σ_el/σ_AM (uniaxial)** | **~0.072** (최고) | uniaxial 압밀 직후 | digitized (Fig 6a) | ★ uniaxial 이 가장 높은 σ_el (입자간 접촉↑·thickness↓) |
| σ_el/σ_AM (relaxed) | **~0.032** (급감) | relaxation 후 | digitized | "significant decrease upon relaxation" (접촉 끊김) |
| σ_el/σ_AM (isostatic) | **~0.033–0.043** (부분 회복) | isostatic 1/3/5 + 사이클 D1–C5 | digitized | "partial recovery during isostatic; **monotonic increase with isostatic pressure**" (5>3>1 MPa) |
| **σ_el/σ_AM (사이클 D/C)** | **~0.030–0.045** (D=discharge / C=charge, 1–5회) | isostatic 5 MPa, 5 사이클 | digitized (Fig 6a) | 사이클마다 진동(방전↑/충전↓ 경향), 큰 추세변화 없음 |
| **τ (tortuosity, uniaxial)** | **~2.3** (최저) | uniaxial | digitized (Fig 6b) | ★ uniaxial 이 *최저* τ (가장 직선 SE 경로) |
| τ (relaxed) | ~2.3 → 2.9 (5 MPa marker) | relaxation | digitized | |
| **τ (isostatic)** | **~2.2 – 3.8** (압력·사이클별) | isostatic 1/3/5 + D1–C5 | digitized (Fig 6b) | ★ **τ 가 isostatic 압력에 *비단조*** — **1 MPa 가 *최저* τ·최고 D_eff** (3·5 보다), "**non-monotonic** dependence on isostatic pressure" (stated) |
| **σ_el (lithiated/delithiated 미보정)** | (보정 안 함) | 본문 caveat | stated | "we are **not accounting for the change of electronic conductivity of AM in lithiated/delithiated states** → resulting values attributed to changes in geometry only" |
> ★ **핵심:** σ_el 은 isostatic 압력↑ → 단조↑(5>3>1); **τ·D_eff 는 *비단조*(1 MPa 최저 τ)** → "optimal isostatic pressure must be refined; simply raising isostatic pressure is *not sufficient* (Fig S10b,c)."  ⚠ σ_el 은 **AM 전도도로 *정규화*한 상대값**(σ_el/σ_AM), τ 는 SE 망 *기하* tortuosity — **절대 σ_ionic/σ_e(mS/cm) 아님.**

### 3.6 미측정 / n/a (우리 앵커와 직접대조 금지)
| 항목 | 상태 |
|---|---|
| **porosity / 상대밀도 절대값** | **n/a** — box thickness 진화(84/95/125 µm)만; porosity % 미보고.  ⚠ thickness 는 box 정의(xy 150→130 변동) 탓 단독으로 porosity 환산 불가 |
| **σ_ionic / σ_e / σ_thermal *절대값* (mS/cm)** | **n/a** — σ_el/σ_AM(*상대*, normalized) + τ(기하) 만; GeoDict ConductoDict(σ_el)/DiffuDict(τ) = *상대* descriptor.  접촉저항(Holm)·Kirchhoff 절대 σ *없음* |
| **coverage % / 접촉면적** | **n/a** (접촉응력만; coverage 미산출) |
| **coordination Z** | **n/a** (명시 보고 없음) |
| **Heckel P_y / knee / 압밀곡선** | **n/a** (Heckel 안 함) |
| **σ_y(항복강도) / 소성경화 / 균열** | **n/a** — ★ **rigid 구 + Hertz 탄성** (소성·항복·균열 *모델 안 함*).  응력이 "균열 위험"을 *시사*만 함(Auerbach 류 임계 *없음*) |
| **PSD D10/D50/D90 (정밀)** | **n/a** — AM 3–10 µm, SE 6–13 µm *범위*만(분위수 미보고) |
| **σ_grain / σ_AM 절대값** | **n/a** (σ_el 을 σ_AM 으로 정규화 → σ_AM 자체 절대값 미명시) |

---

## 4. 시뮬레이션 방법 ★ — LIGGGHTS DEM 4-step (압밀×2 + relaxation + 사이클 팽창)

> ★ 이 논문의 *엔진*은 **우리와 같은 LIGGGHTS DEM (Hertz, rigid 구)** 이고, *새로움*은 그 위에 **(4) AM 입자의 *Li-삽입 ±6 % 부피 팽창/수축*을 *5 사이클* 부과**해 *사이클 응력*까지 가는 것이다.  아래는 (i) 워크플로 → (ii) 각 step BC → (iii) **사이클 step(★ 고유)** → (iv) σ_el·τ post.

### 4.0 code / version / HW
- **code**: **LIGGGHTS** (ref [29]) — Newtonian eqns of motion.  **= 우리 코드** (LAMMPS 계열 DEM).  ⚠ MPM·FEM·연속체 *없음* (순수 DEM + GeoDict 후처리).
- **물성 출처**: Young's modulus·Poisson ratio·friction·COR (AM·SE) from **refs [30,31]** — **Granular Force Field (GFF)** 파라미터, SI 에 상세.  (ref [30] Pierce/Cronau sulfide·NMC 류 추정.)
- **HW**: MatriCS (UPJV), 375 GB RAM, Intel Xeon Gold 6148 @2.40 GHz, **40 코어 1 노드**.

### 4.1 ★ 워크플로 (Fig 1 — 실험 프로토콜 ref [28] 모사)
**Initial generation → Uniaxial compression → Relaxation → Isostatic compression → Cycling (discharge/charge).**  각 step 의 출력 미세구조가 다음 step 의 입력 (Fig 1 화살표).  ★ **워크플로 자체가 실험 cold-press(uniaxial) → cell assembly(isostatic) → cycling 을 그대로 반영** (ref [28] = 같은 그룹 wet-process SSB 프로토콜).

### 4.2 ★ Step 1 — Initial microstructure generation (§2.1.1)
- **11,002 입자**(AM NMC532 + SE LPSCl) 를 **150 × 150 × 150 µm³** box 에 **무작위 위치**로 stochastic 생성.  **AM mass loading 14.96 mg/cm²**.
- **NVE ensemble, T = 300 K** (입자수·box부피·에너지 보존).  **2 미세구조(M1·M2)** = 다른 random seed 로 입자 위치 → 비교용.
- AM 26.7 wt%(PSD 3–10 µm) + SE 73.30 wt%(PSD 6–13 µm) (Fig S1).

### 4.3 ★★ Step 2 — Uniaxial compression 375 MPa (§2.1.2)
- BC: **x·y 주기, z 고정**.  **두 이동 plate** 가 z 를 따라 입자에 *점증하는 힘*을 가해 **375 MPa over 150×150 µm² area** 도달까지 압축.  대부분 값이 일정해질 때까지(=plate 위치·plate 힘·입자 위치 정상상태) 실행 — **~400 µs**(800 µs 와 차이 없어 400 채택).  그 뒤 **압력을 ambient(1 atm)로 점감**(relaxation).
- ★ **375 MPa = 실험 cold-press 범위**(본문 "electrode usually pressed uniaxially at 300–500 MPa before cycling").

### 4.4 ★ Step 3 — Relaxation (Fig 2)
- uniaxial 압력 → 1 atm 해제.  **z-thickness 84 → 95 µm** (springback: 영구변형 + 탄성 회복).  → isostatic 의 입력.

### 4.5 ★★ Step 4 — Isostatic compression 1/3/5 MPa (§2.1.3, Fig 3)
- BC: **모든 면(전 방향) 고정 box 치수**.  **각 면에 동일 표면압(1·3·5 MPa)** 적용 → 등방 압축.  (5 MPa = ref [28] device 작동 상한.)
- **z-thickness 95 → 125 µm**, xy **150 → 130 µm** (등방화).  ★ **3 압력(1/3/5)** 각각 별도 → σ_el·τ·응력 비교.

### 4.6 ★★★ Step 5 — Cycling: AM 팽창/수축 (§2.1.3 끝, *이 논문 고유*)
- ★ **AM 입자 *전부*의 *크기*(반경)를 *6 % 부피*만큼 *팽창*(lithiation/discharge) 또는 *수축*(delithiation/charge), *5 사이클* 반복.**  "the size of all AM particles was **expanded and contracted by 6 %** for **five consecutive cycles** to model their behavior upon lithiation and delithiation respectively, occurring during the battery cell electrochemical cycling."
- ⚠ **균일 rate 가정(저자 명시 한계):** "In real systems, the size change of AM does **not occur uniformly** because of the heterogeneity in interfaces and AM active surface → heterogeneous (de)lithiation kinetics. ... we assume the DEM model captures the effects ... **symmetrical charge/discharge profiles anticipated, without difference in potential values** since AM revert to original size after each step (homogeneous AM size change)."  → **확산분포·비대칭 전위 무시** (frame[5] *전기화학* coupling 미반영 — So 2021 과 같은 한계).
- ★ **NMC532 ±6 % = 문헌 부피변화** (Si ~280 % 와 *대조* — NMC 양극은 작게 팽창; Kang NCA 5.9 %·Bucci 7.5 % 임계와 같은 계열).
- **하중:** 사이클은 **isostatic(1/3/5 MPa) 압력 유지 *하*에서** AM 팽창/수축 → 팽창이 SE 를 밀고, plate 가 등방압 유지 → 응력 재분배(Fig 5a).

### 4.7 ★ σ_el·τ 계산 (§2.1.4, post)
- **σ_el (electronic, AM 망)**: 입자 → **voxel 이산화**(voxel 0.5 µm) → **GeoDict ConductoDict[34]** 로 *current flux* 풀이, **z 방향 1 V** 전위차 (Ohm's law), 측방 주기.  **AM bulk σ 로 정규화** → **σ_el/σ_AM (상대)**.  ⚠ AM-SE overlap voxel 은 *더 높은 Young's modulus* 쪽(AM)에 할당.
- **τ (ionic, SE 망)**: **GeoDict DiffuDict** — SE 도메인 Fick 1법칙(농도차 Δc, z 방향) → 확산 flux j → **D_eff = −j × length / Δc** → **τ = √(η/D_eff)** (η = SE+AM 부피분율 = SE 가 차지하는 부피).  τ 는 기하 property (Δc·D 무관).  측방 주기.  ★ **이온은 SE 만, 전자는 AM 만 carry** 가정 (= 우리 분리망 가정과 동일).
- ⚠ **σ_el 은 정규화 *상대값*, τ 는 *기하* tortuosity** — **절대 σ_ionic/σ_e(mS/cm) 아님.**  (Bazzoun 의 Holm/Kirchhoff *절대* σ 와 *다른* 수준 — 이 논문은 *기하 descriptor* 까지만.)

### 4.8 입자 처리 ★★ (DEM판 "무질서 처리")
- **구(sphere)만** — AM·SE 모두 구.  **형상은 절대 변하지 않는다.**  **rigid + Hertz 탄성 접촉** (CONTACT 소성·항복·균열 *전부 없음*).  사이클 "팽창"은 **입자 *반경*을 키우는 것** (재료가 *흐르는* 게 아니라 *구가 커짐*) — **진짜 SHAPE 소성 아님**(δ-overlap·반경변화 프록시).
  ⇒ ★ **우리 분류로 "rigid 구 + Hertz" 의 *가장 단순* 단(Bazzoun 과 동급)** — So 2021(CONTACT 소성+융착)·우리 Stage-E(Tabor 사후보정)·우리 MPM(SHAPE 흐름)보다 *덜* 정교.  사이클은 *반경 swing* 으로만.
- **mono-disperse 아님:** AM 3–10 µm + SE 6–13 µm **연속 PSD**(Fig S1).  ⚠ **SE 가 AM 보다 *큼*** — 우리 12:4:1(SE≪AM)과 *반대* size-ordering → packing·dip 직접 비교 주의.
- ⇒ **균열·소성·morphology *없음*** = 이 논문이 *비운* 칸 (= 우리 Stage-E/fracture/MPM 이 채울 자리).

### 4.9 도메인 / servo / seeds / 압력
- **2-phase(AM+SE), carbon/binder 없음**, 150³ µm box, **11,002 입자** (≫ So 1600).  **2 seeds (M1·M2)** + SI 의 S5 등 추가 실현.
- **servo:** uniaxial = 이동 plate(목표 375 MPa 까지 점증력); isostatic = 전 면 등방압(1/3/5 MPa); 사이클 = isostatic 유지 + AM 반경 ±6 %.
- **압력:** uniaxial 375 MPa(=실험 cold-press 300–500); isostatic 1/3/5 MPa(작동압 수준); 사이클 5회.
- **3D** (≠ So 2021 2D, ≠ Bucci 2D) — ★ **3D 가 이 논문의 강점**(우리 3D MPM·DEM 과 같은 차원).

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §1 Introduction — 문제 + frame[5] 위치
- LIB → SSB 동기(고에너지밀도·안전).  SSB 가 LIB 뒤처짐 = **구조·전기화학 변환의 복잡성**(고체/고체 계면 chemo-mech 반응·AM 균열).  **제조 공정이 chemo-mech 양립성·최종 성능 결정** (refs [11–13]).
- ★ **Shi et al.[14](같은 그룹) 계승:** DEM 으로 **cathode 입자 size 비(PSD)** 가 SSB 용량에 미치는 영향; **cathode utilization = V_AM^active/V_AM** (SE 망에 접촉한 AM 부피 / 전체 AM) 정의 + **λ = D_AM/D_SE**(AM/SE 입경비)와 비교; **큰 AM size 비 → 높은 AM loading → 높은 용량**.  → 본 논문이 그 *역학 응력* 축을 추가.
- **사이클 중 압밀이 최종 미세구조·내부저항·용량감쇠에 영향**(refs [4,6,15–17]).  **isostatic 압축이 aging 완화 유망**(균일 압력 → 미세구조 균일 → 용량유지↑, refs [10,18–20]).  **3D 모델이 계면 진화·void 형성 이해에 필요**(refs [11,21]).
- ★ **갭 주장:** "lack of comprehensive **3D models that address material interfaces and mechanics** remains a gap.  ... ARTISTIC 로 LIB 전극 미세구조 예측[22–25] + wet-process SSB cathode[26,27] 전이성 입증.  **In this research, we aim to address the gap in understanding the effects of stress distribution during (de)lithiation, overlooked in different compression approaches.**"  → **uniaxial+isostatic 압밀 → 사이클 응력 → ionic τ·σ_el 영향** 의 3D-resolved DEM 모델 (저자: "to the best of our knowledge, this is the **first time a model that couples the compression approach with particle mechanical changes during electrochemical cycling** is proposed").  ⚠ 단 **full electro-mechanical coupling 은 계산비용으로 보류**(stress·전도도까지만).

### 5.2 §2 Methods — 워크플로 (§4 전체)
- §2.1 워크플로(Fig 1); §2.1.1 생성(11,002 입자, 150³, NVE 300 K, M1·M2); §2.1.2 uniaxial(375 MPa, z 가압, ~400 µs); §2.1.3 isostatic(1/3/5 MPa, 전 면) + **사이클 AM ±6 % ×5**; §2.1.4 σ_el(ConductoDict, 정규화)·τ(DiffuDict, √(η/D_eff)).

### 5.3 §3.1 Uniaxial·isostatic stress distribution (Fig 4–5)
- **Uniaxial(Fig 4):** size-dependent 응력(작은 AM↑), 특히 횡방향.  **z축 작은 AM >500 MPa in all dims.**  **AM ≈ 2× SE 응력**(SE deformable·soft).  bottom·top 영역 응력↓, bulk↑(양면 plate 압력).  M2·S5 동일(Fig S2).  ⇒ "uniaxial → higher conductivity (compaction) **but** subjects particles to significant stress → AM cracking·SE deformation risk."
- **Isostatic(Fig 5a):** 평균 응력 **~2 자릿수 낮음**(stress 6–16 MPa).  잘 압밀된 미세구조 유지.  ★ **사이클 응력 진화(§3.4):** 방전(AM 팽창) → AM-SE 차 벌어짐 → full discharge 서 비슷; 충전(AM 수축) → SE 로 응력 이전 → 더 균일.  **Fig 5b**(xy 평균 응력 z 방향, M1·M2 charge/discharge): heterogeneity 큼(M2 가 M1 보다, 특히 y 하반부) → "same porosity 라도 다른 성능 → local geometrical heterogeneity (stress-induced SE 입자 배열) 가 echem 성능에 큰 영향."
- ★ **Torayev et al.[38](같은 그룹) 인용:** Li-O₂ cathode tomography → exact pore location 이 같은 porosity 라도 다른 성능 → 본 논문의 stress-induced 배열 차(M1≠M2)와 같은 결.

### 5.4 §3.2 Electronic conductivity·tortuosity (Fig 6)
- **σ_el(Fig 6a, σ_el/σ_AM):** uniaxial **0.072**(최고, thickness↓·접촉↑) → relaxation **0.032**(급감) → isostatic **0.033–0.043**(부분 회복, **압력 단조↑**: 5>3>1).  사이클 D/C 진동.  "isostatic at low pressures → conductivity comparable to uniaxial at **~twice order of magnitude lower** [pressure] → promising for SSB cathode processing."
- **τ(Fig 6b):** uniaxial **~2.3**(최저, 직선 경로) → isostatic **~2.2–3.8**, ★ **비단조**(1 MPa 최저 τ, 3·5 보다).  "τ·D_eff do **not exhibit monotonic dependence** on isostatic pressure ... lowest τ·highest D_eff at **1 MPa**, then 3·5.  May be attributed to lower pressure allowing easier particle rearrangement; further investigation needed."
- ★ **caveat(본문):** "we are **not accounting for the change of electronic conductivity of AM in lithiated/delithiated states** → values attributed to **geometry only**."  + "σ_el increase with isostatic pressures exceeding 5 MPa (Fig S10), yet decrease below 1 MPa.  optimal isostatic pressure must be refined (simply raising pressure **not sufficient**, Fig S10b,c)."  + **interlaboratory reproducibility[39]:** 동일 시료 σ_ion 측정이 **1.3–5.8 mS/cm (RSD 35–50 %)** 산포 → SE 배열·전도망 단절 민감 (M1≠M2 와 같은 결).
- **Bielefeld et al.[4] 인용:** cone-like(AM·SE → 점접촉 pillar) vs stochastic 배열 → cone 이 active interface area 크게↑.  본 논문: enhanced 구조배열 → σ_el·D_eff↑ 정합(Bielefeld 보다 더; 추가 발전 필요).

### 5.5 §4 Conclusions (저자 요약)
- **DEM 워크플로**가 제조·사이클 중 **응력 진화**를 종합 평가.  echem-mech coupling 의 더 깊은 이해 제공(실험 난해).  **압력·미세구조·전도도의 동적 관계** 강조.
- ★ **uniaxial = 효과적 압밀·고전도 BUT 높은 응력 → AM 균열·수명단축**; ★ **isostatic = 덜 파괴적 대안 → 비슷한 전도도·*현저히 낮은 응력*·균일 압력** → "controlled stress distribution is critical for improving cycling protocols."
- **사이클 동적 응력 shift:** 팽창 시 AM↑·수축 시 SE 로 이전 → "understanding stress dynamics throughout the battery cycle for optimizing performance·longevity."
- **isostatic = 고압 uniaxial 불필요** → 제조비↓·산업 전환 유리.

---

## 6. Figure / Table set ★ (모든 그림 + 우리가 쓸 점)
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1** | ★ 워크플로 모식 (초기생성→uniaxial→relaxation→isostatic→cycling[discharged/charged], 응력 컬러바 0–10 MPa) | 5 step | ★ **우리 LIGGGHTS 파이프라인에 *사이클 step* 추가 청사진**; SE(노랑)·AM(회색)·stress(rainbow) |
| **2** | uniaxial→relaxation transition (M1): box 84 µm → 95 µm | z 84→95, xy 150 | ★ springback(영구+탄성); thickness 진화 |
| **3** | relaxation→isostatic transition (M1): 95 µm → 125 µm | z 95→125, xy 150→130 | ★ isostatic 등방화(xy 줄고 z 재배열) |
| **4** | ★★ uniaxial 375 MPa 응력 vs (z위치·입경) × (x/y/z), M1, 컬러맵 0–500 MPa | z축 AM 500–700 MPa; AM≈2×SE; 입경↓→응력↑ | ★★ **우리 압밀 응력장 von Mises CV·AM_P stress ratio 의 *직접* 대응**(같은 LIGGGHTS, uniaxial); 작은 입자↑ |
| **5a** | ★★ isostatic 5 MPa 응력 vs (z·입경) × (x/y/z), isostatic+discharge+charge AM·SE, 컬러바 0–10 MPa | 응력 6–16 MPa; 사이클 AM↔SE 재분배 | ★★ **사이클 응력 진화**(방전 AM↑/충전 SE↑); isostatic ~2자릿수 저응력 |
| **5b** | ★ z방향 평균 응력 히트맵 (xy 단면, M1·M2 × charge/discharge), 컬러바 6–35 MPa | 대부분 20–25, M2 불균일 | ★ packing heterogeneity(M1≠M2) → 같은 porosity 다른 성능 |
| **6a** | ★ σ_el/σ_AM 진화 (uniaxial→relaxed→isostatic→D1–C5), M1·M2 × 1/3/5 MPa | uniaxial 0.072 / relaxed 0.032 / isostatic 0.033–0.043(5>3>1) | ★ uniaxial 최고 σ_el; isostatic 압력 단조↑; 사이클 진동 |
| **6b** | ★ τ 진화 (동일 축) | uniaxial 2.3(최저) / isostatic 2.2–3.8(**1 MPa 최저**, 비단조) | ★ **τ 비단조**(1 MPa 최저) — 우리 τ_Laplace·C(τ) 대비; "압력 올린다고 τ↓ 아님" |
| **S1** | AM·SE PSD | AM 3–10 µm, SE 6–13 µm | ⚠ SE>AM (우리 12:4:1 반대) |
| **S2** | M2·S5 uniaxial 응력 (size-dependent 재현) | (Fig 4 동일 경향) | seed robustness |
| **S4/S7** | uniaxial 응력 (다른 미세구조) | | |
| **S8a–c** | isostatic 1·3 MPa 응력(M2) | | |
| **S9** | τ·D_eff (보충) | | |
| **S10b,c** | σ_el·τ vs isostatic 압력 (비단조 증거) | 1 MPa 최저 τ | ★ "압력 단순 증가 불충분" 근거 |

> ⚠ **본문 Table *없음*** (모든 정량은 Fig 4–6 + SI).  GFF 파라미터(E·ν·μ·COR)는 **SI** 에만 (본문 미노출 → 우리 CSV 에 "SI, 미상" 표기).  방법 원전 = LIGGGHTS[29] + GeoDict[34] + ref [28] 프로토콜.

---

## 7. Post-processing ★
- **무엇:**
  - **응력장**: 각 입자에 걸리는 **stress per dimension(x/y/z)** 을 (i) **z-위치 함수**(좌열 Fig 4/5), (ii) **입경(radius) 함수**(중앙열), (iii) **공간 컬러맵**(우열) 으로.  uniaxial(0–500 MPa) vs isostatic(0–10 MPa) vs 사이클 히트맵(6–35 MPa).  AM·SE 분리.
  - **σ_el (electronic)**: 입자 → voxel(0.5 µm) → **GeoDict ConductoDict** current-flux(z 1 V, 측방 주기) → **AM bulk σ 정규화** → σ_el/σ_AM (상대).  overlap voxel → 높은 E(AM) 할당.
  - **τ (ionic tortuosity)**: SE 도메인 → **GeoDict DiffuDict** Fick 1법칙(Δc, z) → D_eff = −j·L/Δc → **τ = √(η/D_eff)** (η=SE 부피분율).  기하 property.
  - **시계열(★ 사이클판)**: σ_el·τ·D_eff 를 **워크플로 step 함수**(uniaxial→relaxed→isostatic→D1·C1·…·D5·C5)로; 응력은 각 step 스냅샷.
- **도구**: **LIGGGHTS**(DEM, 응력) + **GeoDict ConductoDict(σ_el)·DiffuDict(τ)**[34] (상용 voxel 솔버 — Bielefeld 와 같은 계보, 단 *상대* σ_el·기하 τ 까지).  Python 스크립트로 voxel 변환(0.5 µm).
- **수치화·기록 방식**: 압밀 = box thickness 진화 + 응력 vs (z·입경·축); 사이클 = σ_el·τ vs step(2 seed × 3 isostatic 압력 × 5 사이클 D/C).  **σ_el 정규화(σ_el/σ_AM), τ 기하** — *상대* descriptor (절대 σ *없음*).

---

## A. ## 우리 DEM+MPM 대비 (comparison vs ours)
> ★ **사용자 MANDATORY A.**  이 논문 = *사이클 응력* DEM (LIGGGHTS, Hertz, rigid 구) vs 우리 *압밀 응력* DEM(von Mises CV·force-chain·AM_P stress) + Stage-E + MPM.  **핵심: 그들이 *사이클 응력 진화*(우리 frame[5] 공백)를 *우리와 거의 같은 코드*로 가짐.  우리는 *압밀-state* 응력을, 그들은 *사이클-evolution* 응력을 계산.**  "진짜 차이" vs "method-artifact" 명시 구분.

### A.1 핵심 대비표
| 항목 | 이 논문 (Franco DEM 2024) | 우리 DEM+MPM | 차이 / 이유 (진짜 차이 vs artifact) |
|---|---|---|---|
| **시간축(★ 핵심)** | **제조(uniaxial+isostatic) + *사이클 응력 진화*** (AM ±6 % ×5) | **제조(압밀)만** — frame[5] 사이클 미보유 | ★★ **진짜 다른 칸** — 그들이 *사이클 응력*(우리 공백)을 *LIGGGHTS-DEM*으로.  우리 *정적* 압밀 응력장 → 그들 *사이클* 응력 재분배 |
| **응력 *대상*** | **사이클 응력 *분포*(SOC·입경·z)** — 균열·소성 *없음* | 압밀 응력 (**von Mises CV**, force-chain, AM_P stress ratio) — 정적 스냅샷 | ★ 둘 다 *입자 응력*(같은 종류 객체); 우리=제조-순간, 그들=사이클-진화.  같은 LIGGGHTS 응력 read-out |
| **DEM 소성/형상** | **rigid 구 + Hertz** (소성·항복·균열 *전부 없음*); 사이클=반경 ±6 % swing | hooke/hysteresis + **Stage-E(Tabor 소성 접촉면적)** + **MPM J2(SHAPE 흐름)** | ★★ **우리가 더 정교** — 그들은 Stage-E·MPM·fracture *전부 없음*.  그들 사이클 "팽창"=구 반경 키움(SHAPE 흐름 아님) |
| **균열** | **모델 *안 함*** — 응력이 "AM 균열 위험" *시사*만 | **Auerbach P_c + Lawn 1998 + fracture-aware Holm(f_intact)** | ★★ **우리 우위** — 그들 균열 미보유(우리 압밀 균열 소유); 단 *사이클* 균열은 둘 다 미보유(Bucci/So 소유) |
| **전달 σ** | **σ_el/σ_AM(*상대*, GeoDict ConductoDict) + τ(기하, DiffuDict)** — 절대 σ *없음* | **σ_ionic·σ_e·σ_thermal *절대* 삼중항** (Kirchhoff/Holm, mS/cm) + 스케일링 폼 | ★★ **우리 압도적 우위** — 그들 σ_el 은 정규화 상대·이온은 τ 기하까지; **Holm 접촉저항·Kirchhoff 절대 σ *없음*** (Bazzoun 보다도 *덜* — Bazzoun 은 RNM 절대 σ 있음) |
| **소재** | **LPSCl(우리와 *동일*!) + NMC532**(우리 NMC811과 조성차) | **LPSCl + NMC811** | ★ **SE 동일**(드문 정합) → 방법·추세 직접 전이; ⚠ NMC532≠811(부피변화·E 차) → 절대 σ·응력 직접 동일시 주의 |
| **size-ordering** | **SE(6–13 µm) > AM(3–10 µm)** | **AM ≫ SE (12:4:1)** | ★ **반대** — packing·Furnas-dip 직접 비교 금지 (그들 size 효과는 *우리와 반대* 배열) |
| **차원** | **3D** (150³ µm, 11,002 입자) | DEM/MPM 2D+3D | ★ **둘 다 3D** (Bucci/So 2D 보다 우리에 가까움) |
| **AM 응력비** | **AM ≈ 2× SE** (uniaxial) | 우리 real_14 AM-shielding(SE overlap 1.75 %, AM 하중지지) | ★ **방향 일치**(AM 이 더 받음) — 단 그들=*응력비 2×*, 우리=*overlap/shielding* (같은 물리, 다른 metric); So 2021 Si AM-AM 2.5–5.9 GPa 와도 같은 계열 |
| **검증** | 실험 *없음* (ref [28] 프로토콜 기반); σ_el·τ 상대 | solver=ground truth + 외부 실험앵커(Minnmann/Bazzoun/Doux) | ★ 그들=순수 시뮬(상대 descriptor) → 우리 *압밀/전달* 절대값과 직접 수치비교 불가, *방법·추세*만 |

### A.2 ★★ 사이클 응력 = 우리 frame[5] 공백을 *LIGGGHTS 로* 채움 (사용자 핵심)
- **우리 압밀 응력장**(CLAUDE.md): von Mises CV(stress_cv), force-chain(big-AM load-bearing), AM_P stress ratio — **모두 *제조-순간(300 MPa)* 의 *한* 스냅샷.**  사이클 응력 진화는 **frame[5] 공백**(우리는 cycle 안 함).
- **그들 사이클 응력**: AM ±6 % 팽창/수축 ×5 → **응력이 AM↔SE 사이를 왕복 재분배**(방전 AM↑·불균일 / 충전 SE↑·균일).  → ★ **우리 압밀 응력장의 *시간축 확장* = 같은 LIGGGHTS 응력 read-out 에 AM 반경 swing 만 추가.**
- ⇒ ★ **인과 사슬:** *우리* 압밀 응력장(제조) → *그들* 사이클 응력 재분배(작동) → (균열·접촉손실은 *둘 다* 미보유, So/Bucci 소유).  **우리가 압밀 응력을 안다면, 그들 방법이 그 위에 *사이클 진화*를 얹는 직접 청사진.**

### A.3 ★ "작은 입자 ↑ 응력"(이 논문) vs "큰 입자 깨짐"(Bucci/Kang) — *모순 아님, 다른 축* (사용자 정밀)
**답: 모순 아님 — *응력 크기*(이 논문)와 *균열 driver*(Bucci/Kang)는 다른 양.**
- **이 논문(Fig 4/5 중앙열):** **작은 AM 이 더 *높은 접촉응력*** (edge·직접 plate 접촉 입자·작은 입자가 더 받음; 압밀/사이클 *접촉응력* 의 *기하* 효과).
- **Bucci/Kang:** **큰 입자가 더 *균열*** — 단 driver 가 다름: Kang = *사이클 Li-농도 구배*(큰 입자 ~10× 구배 → 확산응력 GPa); Bucci = *Vegard 팽창의 SE 구속*.  → "큰 입자가 *Li-구배·확산응력* 으로 깨진다" ≠ "작은 입자가 *접촉응력* 을 더 받는다".
- ⇒ ★ **두 결과 공존:** *접촉응력* 은 작은 입자↑(이 논문), *확산-유발 균열* 은 큰 입자↑(Kang/Bucci).  우리 Auerbach(*접촉응력* driver)는 **이 논문 쪽**(작은 입자↑ 접촉응력) 과 정합; A9(크기-의존 *균열*)는 Kang 쪽(*Li-구배* driver)이라 **driver 분리 필수**(우리 백로그 A9 가 이미 명시: "driver 다름").  ⚠ **이 논문은 NMC532 ±6 % 균일팽창**(확산분포 무시) → *Li-구배* 효과를 *못 봄* → "작은 입자↑ 응력"은 *접촉응력* 결론이지 *균열* 결론 아님 (conflate 금지).

### A.4 ★ uniaxial vs isostatic 응력 대비 = 우리 "제조압 ≠ 작동압" 인식의 *응력* 판
- 그들: **uniaxial 375 MPa → 입자 z응력 500–700 MPa**(경계압 초과) vs **isostatic 5 MPa → 응력 6–16 MPa**(~100× 낮음), *비슷한 σ_el·τ*.
- = 우리 **"300 MPa 제조(Heckel P_y 138) ≠ 수~수십 MPa 작동"**(Doux 5 MPa·Lee 2 MPa·Minnmann 측정 40) 인식의 **응력 분포 판**.  ★ **그들 isostatic 1–5 MPa = *작동압* 범위**(Doux/Lee/Minnmann 측정압과 같은 계열) → "고압 uniaxial 제작 + 저압 isostatic 운용" 이 우리 압력-구분과 *직접* 합류.  ⚠ 단 그들 uniaxial 375 = *제조*압이고 isostatic 1–5 = *작동* device 압(ref [28] 5 MPa device) — **둘 다 압밀에 쓰이나(그들은 isostatic 도 압밀 step) 응력 규모가 ~100× 다름** = 우리 "제조 vs 작동" 의 *응력* 증거.

### A.5 ★ Bucci FEM-CZM(연속체) vs 이 논문(DEM, 우리처럼 discrete) 대비
- **Bucci 2017/2018 = *연속체* FEM/해석** (SE 상 균열·계면 박리; AM=square Voronoi / 1D shell; Vegard eigenstrain).  **이 논문 = *discrete* DEM** (입자·접촉망 — *우리와 같은 표현*).
- ⇒ ★ **frame[5] 사이클 칸의 *방법 스펙트럼*:** **연속체**(Bucci FEM-CZM: 균열 *예측*, 절대 응력 GPa) ↔ **discrete DEM**(이 논문: 응력 *분포*, 균열 *없음*; So 2021: 응력+균열+κ 열화).  **이 논문이 우리 DEM 에 *방법적으로 가장 가깝다*** — 우리가 사이클 응력을 *우리 LIGGGHTS* 에 넣으려면 Bucci 의 연속체 CZM 보다 *이 논문의 DEM 반경-swing* 이 *직접* 이식 가능.  Bucci 의 균열 임계(7.5 %, G_c 4 J/m²)는 *위에* 얹는 fracture 판정으로.
- ⚠ **단 이 논문은 균열 *안 함*** → "사이클 균열 예측"은 여전히 Bucci(FEM-CZM)·So(DEM 융착파괴) 소유; 이 논문은 *응력까지만*(균열은 우리가 Auerbach/Bucci 임계로 *추가*해야).

### A.6 frame[4]/[5] 정직 정리
- **frame[4](cross-fit 금지):** 이 논문은 우리와 *교차검증* 대상이 아니라 **frame[5] 사이클축 *보완* + 방법 청사진** — DEM/MPM 을 여기에 맞출 일 없음(둘 다 experiment 에 독립 calibrate; 이 논문도 실험 *없이* ref [28] 프로토콜).  단 **워크플로·BC·AM ±6 % swing 은 *방법* → 우리 LIGGGHTS 에 직접 채택 가능**.
- **frame[5](분업):** **압밀 응력·구조→σ 삼중항·packing·morphology·압밀 균열 = 우리**; **사이클 응력 *진화* = 이 논문(+So 열화 시계열, +Bucci 균열)**; **우리 MPM J2 = 압밀 소성 morphology**(사이클 균열 불가).  → 이 논문은 **DEM 경쟁자라기보다 *우리 DEM 의 사이클 확장 템플릿***.

---

## B. ## 적용가능성 (applicability to our LIGGGHTS DEM model)
> ★ **사용자 MANDATORY B.**  구체적으로 *우리 어느 스크립트/채널*에 *무엇*을 넣을지 — backlog **A10(사이클 chemo-mech)·B6(operating-pressure 시간축)·A9(크기-응력)** 의 *DEM* 구현 레퍼런스.

### B.1 ★★ 우리 LIGGGHTS 압밀 → 사이클 확장 (backlog A10, *직접* 구현)
- **무엇**: 이 논문의 **Step 5 = AM 입자 반경 ±6 % swing ×5 사이클** (isostatic 압력 유지 하).
- **어디에**: 우리 `input_*.liggghts` 압밀 스크립트 (real_14 등) — 300 MPa 압밀 *후* 단계 추가.
- **어떻게 (우리 파이프라인 매핑):**
  1. 압밀(300 MPa, hold) 완료 후 **isostatic 작동압(예 5 MPa)으로 전환**(전 면 등방 servo) — 이 논문 Step 3→4 와 동일.
  2. **AM 입자(NMC811) *반경*을 Vegard 부피변화만큼 키우고/줄이기** — LIGGGHTS `fix adapt` 또는 per-atom `set` 로 radius 재설정(NMC811 = **±~5–6 % 부피**, Kang NCA 5.9 % / 본 논문 6 % 채택; ΔR = (1±ΔV)^(1/3)−1 ≈ ±2 % 반경).  **5 사이클 lithiation(팽창)/delithiation(수축).**
  3. 각 사이클 스냅샷에서 **우리 기존 응력 read-out**(von Mises, force-chain, AM_P stress ratio)을 그대로 적용 → **사이클 응력 재분배** 측정.
- **산출물**: `stress(SOC, cycle)` — 우리가 지금 *못 주는* 사이클 응력 진화 (방전 AM↑/충전 SE↑ 재분배 재현 + *우리 NMC811·12:4:1 sizes* 로).  ★ **우리 3D DEM 이 이미 3D → 이 논문(3D)과 같은 차원에서 *직접* 재현 가능** (So 2D 보다 유리).

### B.2 ★ 사이클 응력 → 균열/접촉손실 (우리가 *위에* 얹을 것 — A9/D6)
- ★ **이 논문이 *비운* 칸(균열) = 우리가 채울 자리:** 이 논문은 사이클 응력*까지만*; 우리는 그 응력에 **Auerbach P_c**(접촉응력→AM 균열) + **Bucci 임계(ΔV>7.5 %·G_c<4 J/m²)**(SE 균열, *위에* 얹기) + **f_intact fracture-Holm**(균열→σ↓)를 적용 → **사이클 응력 → 균열 → σ 열화** 완성.
- **어떻게**: 사이클 각 스냅샷 응력 → (i) AM-AM 접촉응력 > Auerbach 임계 → AM 균열(우리 기존); (ii) AM-SE 계면 응력·박리 → Bucci Eq 10(B6).  ⚠ NMC811 ±6 % < 7.5 % → Bucci 기준상 *균열 억제* 영역(LPSCl G_c 충분 시) — *작은* 양극 팽창이라 균열 위험 *낮음*(Si 280 %와 대조) → 우리 사이클 균열은 *완만*할 것으로 예측.
- **연결**: A9(크기-의존 *균열*)는 Kang 의 *Li-구배* driver; 이 논문은 *균일 팽창*(구배 무시)이라 **A9 의 *접촉응력* 절반**(작은 입자↑ 접촉응력)만 줌 → A9 의 *구배* 절반은 여전히 Kang/Bucci 소유.

### B.3 ★ uniaxial vs isostatic 응력 대비 → 우리 압력-구분 + 응력 검증 (B6)
- **무엇**: "uniaxial 375 → z응력 500–700 MPa(AM 2×SE) vs isostatic 5 → 6–16 MPa, 비슷한 σ_el·τ".
- **어디에**: 우리 deck/paper 의 "제조압(300, Heckel P_y 138) ≠ 작동압(수~수십 MPa)" 논거 + 우리 압밀 응력장 검증.
- **어떻게**: 우리 300 MPa 압밀 응력장(von Mises CV)이 이 논문 uniaxial 375 응력 규모(z 500–700, AM 2×SE)와 *같은 계열*인지 cross-check (frame[4] *방법* 정합; 절대값은 NMC532≠811 주의).  ★ **isostatic 1–5 MPa = 작동압** → 우리 Doux 5/Lee 2/Minnmann 40 압력-구분에 *응력 데이터* 추가.

### B.4 ★ σ_el/τ vs 압력 (비단조 τ) → 우리 τ_Laplace·C(τ) cross-check
- **무엇**: τ 가 isostatic 압력에 *비단조*(1 MPa 최저 τ, 3·5 보다 높음); σ_el 은 단조↑(5>3>1).
- **어디에**: 우리 σ_ionic 폼의 **C(τ) logpoly2** + τ_Laplace,eff.
- **어떻게**: 우리는 *제조압(300)* 단일 → 이 논문의 *작동압 sweep(1/3/5)* τ 비단조는 **우리가 작동압 sweep 을 하면 볼 수 있는 효과** (저압서 입자 재배열 용이 → τ↓).  ⚠ 그들 τ 는 *기하*(DiffuDict), 우리 τ_Laplace 는 *constriction 포함* → 직접 동일시 금지; *추세*(저압 재배열→τ↓)만.  + **interlaboratory σ_ion 1.3–5.8 mS/cm RSD 35–50 %**(ref [39]) = 우리 bulk σ 앵커 산포(Cronau 3.0/Lee 2.19/Bazzoun 1.02) 와 같은 결.

### B.5 한계 (적용 시 주의)
- **NMC532 ≠ NMC811**(우리) — 부피변화·E·σ 차 → 절대값 전이 금지; ±6 % 팽창은 *방법*으로만(우리 NMC811 값 별도 입력).
- **SE > AM size-ordering**(우리 반대) → packing·dip 직접 비교 금지; *워크플로·응력 read-out* 만 전이.
- **rigid 구 + Hertz, 균열·소성 없음** → 그들 응력은 *탄성 접촉*(소성 캡 없음 → uniaxial 서 *과대* 응력 가능; 우리 Stage-E·MPM 이 소성으로 캡).  **사이클 "팽창"=구 반경 swing**(SHAPE 흐름 아님) → 우리 MPM void-fill 과 다름.
- **균일 AM 팽창**(확산분포·비대칭 전위 무시) → *Li-구배*·고율방전 효과 없음 (저자 명시); **full electro-mech coupling 미보유**.
- **σ_el 정규화·τ 기하** → 절대 σ_ionic/σ_e(mS/cm) *없음* → 우리 삼중항 절대값과 직접 비교 불가, *상대 추세*만.
- **실험 검증 없음**(ref [28] 프로토콜 기반) → 절대 응력·σ 값보다 *방법·추세·메커니즘*(uniaxial≫isostatic 응력, 사이클 재분배, 작은 입자↑) 만 신뢰.

---

## C. ## ★ 우리 novelty — 왜 우리가 state-of-the-art 인가 (our novelty vs this DEM model)
> ★ **사용자 MANDATORY C.**  **firm DEM novelty — 우리가 SOTA.**  이 논문은 2024 Franco-그룹 SSB-DEM(우리와 같은 LIGGGHTS 계보)이지만, **transport·소성·morphology·fracture·예측 5개 축 전부에서 우리가 *더 정교*** + 단 **사이클 응력 *진화*(우리 frame[5] 공백)는 그들이 가짐 → 정직히 credit + 흡수 청사진**.

### C.1 우리가 SOTA 인 7개 차별점 (firm)
| # | 차별점 | 이 논문 (Franco DEM 2024) | 우리 | 우위 근거 |
|---|---|---|---|---|
| **(1)** | **transport TRIAD (σ_ionic/σ_e/σ_thermal *절대*)** | **σ_el/σ_AM(*상대*, GeoDict ConductoDict) + τ(*기하*, DiffuDict)** — Holm 접촉저항·Kirchhoff 절대 σ *없음*; 사이클 중에도 *상대* descriptor | **σ_ionic·σ_e·σ_thermal *절대* 삼중항** (Kirchhoff/Holm, mS/cm; LOOCV 0.975/0.953/0.903) | ★★ **압도적** — 그들은 σ *절대값을 안 풂*(Bazzoun 보다도 *덜*: Bazzoun 은 RNM 절대 σ 있음).  우리만 3-채널 절대 σ |
| **(2)** | **Stage-E 소성 접촉면적** | **없음** — rigid Hertz 접촉(소성 캡 *없음*); coverage 미산출 | **Stage-E (Tabor+volume 소성 접촉면적)** + Hertz/Tabor coverage(real_14 16/52 %) | ★★ 그들 응력은 *탄성 접촉*(소성 캡 없어 uniaxial 과대 응력 가능); 우리 Stage-E 가 소성으로 area 재도출 |
| **(3)** | **DEM↔MPM morphology (진짜 SHAPE 소성)** | **없음** — 사이클 "팽창"=구 *반경 swing*(SHAPE 흐름 아님); 형상 불변 | **MPM J2 진짜 소성 형상변화**(SEM 코어보존+경계평탄화 ✓) + void-fill flow + scaffold 커플링 | ★★ 그들 입자는 *영원한 구*; 우리 MPM 만 morphology·void-fill·변형장 Σdg |
| **(4)** | **fracture-aware (Auerbach)** | **없음** — 응력이 "AM 균열 위험" *시사*만(임계·판정 *없음*) | **Auerbach P_c + Lawn 1998 + f_intact fracture-Holm** (압밀 균열→σ↓) | ★★ 우리 압밀 균열 소유; 그들 균열 미보유 (사이클 균열은 둘 다 미보유→Bucci/So) |
| **(5)** | **literature σ_grain (Cronau)** | σ_AM 정규화만(σ_AM 절대값 미명시); SE σ_grain *없음* | **σ_grain=3.0 mS/cm (Cronau 2022 단결정) ×Cronau(r_SE) sub-µm 인자** | ★ 우리 σ 절대 anchoring(그들은 상대라 anchoring 불필요·불가) |
| **(6)** | **scaling-law 예측기 (ML)** | **없음** — 케이스별 시뮬만 (예측 폼 없음) | **σ_ionic/σ_e/σ_thermal scaling-law (LOOCV 0.90–0.975)** + Phase 2–5 predictor→2D synth→layered | ★★ 우리만 design→metric 예측 (그들은 매 케이스 재시뮬) |
| **(7)** | **packing/Furnas-dip (정량)** | size 효과 있으나 **SE>AM**(우리 반대) + **dip 미측정**(연속 PSD) | **Furnas dip AM 70–85 wt%**(de Larrard/McGeary 정량) + bimodal 12:4:1 | ★ 우리 정량 dip 소유; 그들 size-ordering 반대 + dip 안 봄 |

### C.2 ★ 정직 — 그들이 *앞서는* 칸 (credit + 흡수 청사진)
| 그들 우위 | 내용 | 우리 상태 | 흡수 경로 |
|---|---|---|---|
| ★★ **사이클 응력 *진화* (frame[5] 시간축)** | **AM ±6 % ×5 사이클 → 응력 AM↔SE 재분배**(방전 AM↑/충전 SE↑) — *우리 압밀만의 정적 응력의 시간축 확장* | **우리 frame[5] 공백** (압밀-state 응력만) | ★ **직접 청사진**: 우리 LIGGGHTS 에 AM 반경 ±6 % swing 추가(B.1) → 우리 von Mises·force-chain 을 *사이클마다* read-out.  **우리 3D·NMC811·12:4:1 로 재현 + 우리 Stage-E/fracture/삼중항을 *위에* 얹어 그들을 능가** |
| **uniaxial vs isostatic 응력 대비** | **375 MPa→500–700 MPa vs 5 MPa→6–16 MPa**(비슷한 σ_el) → 압밀 *방식*의 응력 대가 정량 | 우리는 *uniaxial 압밀*만(isostatic 미실험) | isostatic step 추가(B.3) → "고압 uniaxial 제작 + 저압 isostatic 운용" 우리 압력-구분에 응력 데이터 |
| **σ_el·τ vs 작동압 sweep** | **τ 비단조(1 MPa 최저)** + σ_el 단조↑ | 우리 *제조압(300)* 단일 | 작동압 sweep(B.4) → 우리 C(τ) 에 작동압 축 추가 |
| **워크플로 (실험 프로토콜 모사)** | 초기생성→uniaxial→relax→isostatic→cycling = ref [28] 실험 5-step 충실 모사 | 우리는 압밀까지만 | 우리 파이프라인을 사이클까지 연장(B.1) |

### C.3 ★ 한 줄 positioning (deck/paper용)
- ★ **"이 논문(Franco 2024)은 우리와 *같은 LIGGGHTS-DEM* 으로 *사이클 응력 진화*(우리 frame[5] 공백)를 보여주는 *가장 가까운 방법 청사진*이다 — 그러나 *응력까지만*: σ 는 *상대* descriptor(절대 σ_ionic/σ_e/σ_thermal 삼중항 없음), 소성 접촉면적(Stage-E)·진짜 SHAPE 소성(MPM)·균열(Auerbach) *전부 없음*.  우리는 그 사이클 응력을 *우리 LIGGGHTS* 에 AM 반경 swing 으로 *직접* 재현하고, 그 위에 *우리만의* 절대 σ 삼중항 + Stage-E + MPM morphology + Auerbach fracture 를 얹어 *능가*한다 — frame[5] 사이클 응력은 그들이 *연 칸*, 그 위 transport·소성·morphology·fracture 는 *우리가 채운 칸*."**

---

## 8. 인용 가능 문장 (deck/paper용)
- "Alabdali, Franco et al. (Energy Storage Mater. 2024) present the **first DEM workflow coupling the compaction route (uniaxial 375 MPa → relaxation → isostatic 1–5 MPa) with per-particle mechanical stress upon electrochemical cycling** (AM ±6 % Vegard expansion/contraction, 5 cycles) — the LIGGGHTS-DEM complement, on the *same code and same LPSCl SE as ours*, to our *compaction-time* stress field (frame[5] cycling-axis)."
- "Uniaxial 375 MPa subjects AM particles to **z-axis stresses of 500–700 MPa (≈ 2× the SE stress)**, raising the AM-cracking risk, whereas **isostatic 1–5 MPa achieves comparable σ_el and tortuosity at stresses of only 6–16 MPa** (~two orders of magnitude lower) — the *stress-distribution* evidence for our 'high-pressure fabrication + low-pressure operation' picture."
- "During cycling the stress field **redistributes between phases**: discharge (AM expansion) widens the AM-SE stress gap (AM bears more), while charge (AM contraction) **transfers stress to the SE**, yielding a more homogeneous distribution and more prominent ionic-percolation pathways — a cycling stress evolution we can reproduce by adding an AM-radius swing to our LIGGGHTS compaction script."
- "Their model is **stress-only**: electronic conductivity is reported as a *normalized* σ_el/σ_AM and ionic transport as a *geometric* tortuosity (GeoDict ConductoDict/DiffuDict), with **no Holm-constriction / Kirchhoff absolute σ, no plastic contact area, no shape plasticity, and no fracture criterion** — exactly the transport-triad, Stage-E, MPM-morphology and Auerbach-fracture capabilities our pipeline adds on top (we are state-of-the-art; their cycling-stress evolution is the one frame[5] capability we adopt as a blueprint)."

## 9. 주의/한계 (over-claim 방지)
- ★★ **stress-only(가장 중요):** 이 논문은 *응력 분포*와 *상대* σ_el·*기하* τ 까지 — **균열·소성·morphology·절대 σ *전부 미보유*.**  "사이클 σ 열화" 를 *그들이 푼다* 고 over-claim 금지 (그들 σ_el 은 *기하 변화*만, 사이클 균열·접촉손실 *안 함*; AM lithiated/delithiated 전도도 변화도 *미보정*).
- **소재 정렬:** SE = **LPSCl (우리 동일!)** 이나 CAM = **NMC532 ≠ 우리 NMC811** → 부피변화·E·σ 절대값 직접 동일시 금지; ±6 % 팽창은 *방법*으로만(우리 NMC811 별도 입력).
- **size-ordering 반대:** **SE(6–13) > AM(3–10 µm)** ↔ 우리 AM≫SE(12:4:1) → packing·Furnas-dip 직접 비교 *금지*; size 효과(작은 입자↑ 응력)는 *접촉응력* 결론(우리 Auerbach 와 정합), *균열* 결론 아님(Kang Li-구배와 conflate 금지).
- **rigid 구 + Hertz:** 소성·항복·균열 *없음* → uniaxial 응력 *과대* 가능(소성 캡 없음); 사이클 "팽창"=구 반경 swing(*SHAPE 흐름 아님*).  우리 Stage-E·MPM 이 채우는 칸.
- **균일 AM 팽창:** 확산분포·비대칭 전위·고율방전 *무시*(저자 명시) → *Li-구배* 효과 없음 → 사이클 응력은 *기하 균일팽창* 판(실제 비균일 (de)lithiation 미반영); **full electro-mech coupling 미보유**(저자: 향후 과제).
- **σ_el 정규화·τ 기하·digitized:** σ_el/σ_AM·τ 는 *상대 descriptor*(절대 mS/cm 아님); 본문 수치 대부분 **Fig 4–6 digitized**(±, TREND only) — stated 는 "AM 2×SE", "isostatic 6–16 MPa", "uniaxial 300–500 MPa", "±6 % ×5 cycles", "1.3–5.8 mS/cm RSD 35–50 %", "τ non-monotonic", thickness 84/95/125 µm 정도.  porosity·σ 절대값 **n/a** → 우리 압밀(15.6 %)/전달(0.04–0.18) 앵커와 **직접 비교 금지.**
- **실험 검증 없음** (ref [28] 프로토콜 기반 시뮬) → 절대값보다 *방법·추세·메커니즘* 만 신뢰.  **2 seed(M1·M2)** robustness 는 있으나 통계 한정.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
