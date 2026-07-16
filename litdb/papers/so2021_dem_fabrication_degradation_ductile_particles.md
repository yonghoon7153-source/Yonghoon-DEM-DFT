# ⭐frame[5] *사이클 열화 DEM* — Simulation of Fabrication and Degradation of All-Solid-State Batteries with Ductile Particles — So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge (J. Electrochem. Soc. 2021)

> slug `so2021_dem_fabrication_degradation_ductile_particles` · DOI `10.1149/1945-7111/abe796` · type `DEM (소성 ductile-particle contact model + 2-step fabrication→intercalation/cycling 열화)` · PDF `So_2021_JES_FabricationDegradation_ASSB_DuctileParticles.pdf` · digested `2026-06-26` · status ✅ · 위시리스트 #37 (★ DEM fabrication + DEGRADATION, ductile particles)
>
> ## ★★★ 이 논문의 위치 — frame[5] *사이클(작동-시점) 열화* 의 **DEM 경로** (Bucci FEM-CZM 의 *DEM 형제*) ★★★
> Magnus So 그룹(Kyushu Univ., Gen Inoue 교신)의 **So-삼부작 중 *유일하게 사이클 열화*까지 가는 논문.** 우리가 이미 digest한
> 자매 둘은 *압밀(제조)까지만* — **So 2021 JPS 508 (LPS+Si cold-press, TauFactor σ)** 와 **So 2022 MethodsX (접촉모델 정의서)**.
> 이 JES 168 논문은 **(1) cold-press *제조*(자매 모델의 ductile 접촉법칙) + (2) Si AM 의 *Li-삽입 부피팽창*(최대 ~300 %)이 사이클마다
> 만드는 *기계 열화*(접촉손실·균열·영구 σ 감소)** 를 **하나의 2-step DEM** 으로 잇는다. ⇒ **우리 frame[5]의 *시간축 공백*(우리는
> *압밀*만, *사이클 열화* 미보유)을 *DEM 으로* 채우는 후보** — Bucci 2017 의 **FEM-CZM** 과 **같은 칸, 다른 방법**.
>
> ★ **Bucci(FEM-CZM) ↔ So(DEM) 한 줄 대비(외우기):**
> - **Bucci 2017**: 연속체 FEM + cohesive-zone, **SE 상 *취성* 균열**, AM·SE 둘 다 *linear-elastic*, driver = Vegard 팽창.
> - **So 2021 (이 논문)**: 입자 DEM + **cohesive *hybrid-particle*** 융착결합, **SE *연성(ductile) 소성* + 접촉 손실**, driver = Si AM 팽창.
> - ⇒ **둘 다 "사이클 팽창 → 균열·σ 감소"** 이지만 So 는 *입자-접촉망*(우리 DEM 과 같은 표현)에서, Bucci 는 *연속체 균열역학*에서.
>   **So 가 우리 DEM 파이프라인에 *더 가깝다*** (입자·접촉·TauFactor τ — 우리 LIGGGHTS+Kirchhoff 와 같은 종류의 객체).
>
> ★ **세 핵심 결과(외우기):**
> 1. **사이클 열화의 *주범* = SE *tortuosity* 급증(균열 때문), φ_SE 는 거의 안 변함(±10 %)** → **κ_SE^rel 의 변화는 τ_SE 가 지배**(Fig 9).
> 2. **작은 팽창(SOC 8 %, ΔV 22 %) → 접촉·σ *회복 가능*(near-original); 큰 팽창(SOC 24 %, ΔV 67 %) → 소성+균열 → *영구* σ·접촉 감소**(Abstract).
> 3. **★ 높은 *제조* 압력 = 사이클 *내구성*** — Pfab↑(100→500 MPa) → 초기 더 조밀 → 사이클 후 **균열 *현저히* 적고**(Fig 7), **κ_SE^rel 영구 감소 *현저히* 작음**(Fig 9d), 접촉면적 손실↓(Fig 10b). = "fabrication condition 이 durability 를 결정한다"는 이 논문의 메시지.
>
> ⚠ **소재가 우리와 다름(절대 전이 금지):** SE = **LPS = 75Li₂S·25P₂S₅ glass(argyrodite *아님*)**, AM = **Si *음극*(NMC 양극 아님; β_Si=2.8 → ~280 % 부피팽창)**. 우리 = **LPSCl + NMC811**. **방법·메커니즘·추세만** 전이; porosity·σ·응력 *절대값* 전이 금지.
> ⚠ **2D**(저자 명시 Shortcomings: "we simulated only in two dimensions") + **단일 실현** + **κ_SE^rel = TauFactor τ-기반 *상대값***(접촉저항 Holm *없음*).

---

## 1. 한 줄 요약
**황화물 ASSB 전극의 *제조*(cold-press)와 *작동-사이클 열화*(Si AM 의 Li-삽입 팽창에 의한 균열·접촉손실·이온전도 감소)를 *하나의 2-step DEM* 으로 모사** — **새 "cohesive hybrid-particle" 소성 DEM**(So 2022 접촉모델 = 비선형 Hertz + 평형 overlap h_eq 소성 + 경도 H 항복 + 융착결합)으로 제조 시 입자 소성변형·융착(consolidation)을, **그 위에 Si AM 의 주기적 팽창(SOCmax 8/16/24 %, 전극 ΔV 22/67 %)** 을 얹어 *사이클마다* 접촉면적이 늘었다 줄고(lithiation↑/delithiation↓), 응력이 SE 경도(1.9 GPa)를 넘으면 *소성+균열*로 융착이 끊겨 **κ_SE^rel 이 영구 감소**하는 과정을 본다. **핵심: (a) 열화는 φ_SE 보다 *tortuosity*(균열) 가 지배, (b) 작은 팽창은 *회복*·큰 팽창은 *영구* 손실, (c) *높은 제조압이 사이클 내구성을 키운다*.** 이 논문은 우리가 인용해온 **So 2020 2D[27]·So 2021 JPS·So 2022 MethodsX 계보**의 *유일한 사이클-열화 확장*이며, 우리 frame[5] *시간축 공백*을 **DEM 으로** 채우는 (Bucci FEM-CZM 의) 형제 후보다.

---

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Magnus So, Gen Inoue (교신, ginoue@chem-eng.kyushu-u.ac.jp), Ryusei Hirate, Keita Nunoshita, Shota Ishikawa, Yoshifumi Tsuge** (Department of Chemical Engineering, Faculty of Engineering, **Kyushu University**, Nishi-ku, Fukuoka 819-0395, Japan) | **J. Electrochem. Soc. 168 (2021) 030538** (10 pp; 제출 2020-12-17, 수정 2021-02-10, 게재 2021-03-26; paper 998 @ PRiME 2020) | **10.1149/1945-7111/abe796** (표지 라벨 "abed23" = IOP 내부 DOI, 정식 DOI는 abe796 계열 — 인용은 vol/page **168, 030538** 사용 권장) | **SE = LPS = sulfide type, 구체적으로 75Li₂S·25P₂S₅ glass (75 % dilithium sulfide; "lithium thiophosphate glass")** + **AM = Si (silicon *음극*, β_Si=2.8 expansion factor → ~280 % 팽창)** | **3D 접촉법칙의 2D DEM** — (1) cold-press *제조* + (2) Si 삽입 *사이클 열화*. Sakuda et al. (2013) 실험으로 보정. ★ **소성 + 사이클 열화 통합** |

> ⚠ **소재 주의:** 우리(LPSCl argyrodite + NMC811 *양극*)와 **다르다.** 여기 SE = **LPS(75Li₂S·25P₂S₅ glass, argyrodite 아님)**, AM = **Si *음극*** (β_Si=2.8; Si는 ~4200 mAh/g 고용량이나 ~300 % 팽창 → 균열). 절대값(porosity·σ·응력) 전이 금지, *방법·추세·메커니즘*만. E_SE=24 GPa가 우리 real-bulk 24와 같은 건 우연(LPS도 sulfide).
> ★ **JES funding:** JSPS KAKENHI Grant-in-Aid (Sci. on Interfacial Ion Dynamics for Solid State Ionics Devices, Comp. & Data Sci. Gp-A03, 19H05815) + MEXT "Researches on Supercomputer Fugaku" (JPMXP1020200301). ORCID: Magnus So 0000-0002-5358-3110, Gen Inoue 0000-0003-2427-0972.
> ★ **계보:** "You may also like" 패널에 Javed-Koyama(active-material coating) + **So-Permatasari-Yano "Understanding the Effect of Mechanical Degradation on the Performance of SSBs through Particle Simulations"**(= 이 논문의 *후속 심화*, 같은 1저자) + Yanev-Auer-Pertsch(resistive+diffusive kinetic limits, thiophosphate). ref [27] So-Park-Tsuge-Inoue *J. Electrochem. Soc.* 167, 013544 (2020) = 우리가 줄곧 인용한 **2D 정초 논문**. ref [24] **Bucci** et al. *J. Mater. Chem. A* 5, 19422 (2017) = 우리가 digest한 **CZM 사이클-균열** 논문(이 논문이 직접 인용·대비!). ref [25] Bucci 2018 *Phys. Rev. Materials* 2, 105407 (= 우리 digest한 delamination 논문).

---

## 3. 핵심 물성 (수치)
> 데이터 CSV: `docs/data/so2021_fabrication_degradation.csv` (fabrication / params / degradation 3 블록).

### 3.1 재료/모델 파라미터 (Table I, 전부 stated)
| 물성/파라미터 | 값 | 출처 (논문 ref) | 비고 |
|---|---|---|---|
| **E_SE (LPS, 75Li₂S·25P₂S₅)** | **24 GPa** | Sakuda et al. [9] | = 우리 real-bulk 24 와 수치 동일(우연; LPS도 sulfide). **연화 안 함** — real E 그대로 |
| **E_AM (Si 음극)** | **70 GPa** | Sethuraman et al. [34] | Si 음극(우리 NMC 140·So 2022 LiCoO₂ 199 와 *다름*) |
| **σ_H^SE (LPS hardness)** | **1.9 GPa** | McGrogan et al. [31] | **항복 임계 F_th = 2/3·σ_H·A_con (eq 8)** — σ_yield ≈ H 근사. LPS 무름 → SE만 소성 |
| ν (Poisson) | 0.3 (both) | This study | |
| μ (마찰) | 0.5 | This study | Coulomb |
| e (COR) | 0.5 | This study | damping η=f(e) |
| **β_Si (Si expansion factor)** ★ | **2.8** | Obrovac et al. [35] | 완전충전 AM 의 상대 부피팽창율 ≈ 280 %; Si 삽입의 *driver*. **이게 열화 엔진** |
| **L_cat (cathode 두께)** | **60 µm** | This study | 삽입 시 *areal spring constant* = E_SE/(L_SE+L_cat) 계산용(상단벽 스프링) |
| **L_SE (SE층 두께)** | **60 µm** | This study | |
| **P_fab (제조압 sweep)** | **50–500 MPa** | This study | 50/100/200/500(상대밀도), 100/200/500(열화) |
| **SOC_max (삽입 sweep)** | **8–24 %** | This study | Si 부분삽입(완전삽입은 팽창 과대 → 부분만); SOC=순간충전량/용량 |
| **φ_AM^rel (AM 부피분율)** | **0.4** | This study | anode 내 AM/전체고체 = 0.4 |
| **cluster 직경 (SE 응집체)** | **5–10 µm** | Methods | Sakuda SEM 관찰과 일치; pre-existing algorithm(연료전지용 [32,33])으로 응집 |
| **α (sub-particle 접촉면적비)** ★ | **0.65** (best) | Fig 4 보정 | A_con=π·h_ov·R_eff·α (eq 9); 0.50/0.65/0.80/1.00 중 0.65가 Sakuda 최적. **표면 거칠기·2차접촉의 1-파라미터 프록시** |
| **γ (Li₂S cohesive energy)** | **2.8 J/m²** | [2,24,31] | σ_coh=2γ/δ |
| **δ (cohesive zone 길이)** | **~1 nm** | [2,24,31] | |
| **σ_c (Li₂S fracture strength)** | **5.6 GPa** | eq 10 | σ_c=2γ/δ=5.6 GPa |
| **σ_H/σ_c (경도/파괴강도 비)** ★ | **0.34** | eq 10 | = 1.9/5.6 → **경도 ≪ 파괴강도 → 초기 파손은 *소성*이 지배(취성 아님)** = 왜 "ductile particle" 모델인지의 *근거* |

### 3.2 ★ 제조(cold-press) — 상대밀도 vs P (Fig 4, Sakuda 검증)
| 양 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| 상대밀도 (SE-only) | ~0.30(초기)→0.62(50)→**0.70(74)**→0.74(100)→0.83(200)→**0.90(360)**→0.95(500 MPa) | α=0.65 | digitized (Fig 4a) | **Sakuda et al.(2013) 실험 open-circle 와 잘 일치** (200–500 MPa) |
| α 효과 | α=1.0(보정 없음) *under-densify* / α=0.65 best / α=0.5 most dense | Fig 4a | stated | α↓ → 접촉면적↑ → 같은 P 서 더 압밀 저항 → 더 무름. **저압(<200 MPa)서 모델>Sakuda(과치밀) = 3D 응집체 미모델 탓**(자매 So 2022 와 동일) |
| 전극 높이(SE-only) | loading 시 지수감소 → unload 시 **springback(부분회복)** | Fig 3b | digitized | y축 ×10⁴ µm(cluster-scale 모델); Pfab↑ → 최종높이↓; **압축해제 후 초기로 안 돌아감(영구 h_eq)** |

### 3.3 ★★ 사이클 열화 (intercalation, Si AM 팽창) — 이 논문의 *심장*
| 양 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **전극 ΔV/V** | **22 %**(SOC 8 %) / **67 %**(SOC 24 %) | Fig 6/7 | stated | Si 팽창의 *전극 레벨* 부피변화. ΔV=67 %가 균열 임계 |
| **SE normal stress** | SOC8: ~0–2 GPa(peak 0.5–1) / SOC24: **6–8 GPa tail**(일부 인장 ~−2) | Fig 6c | digitized | SOC24 응력이 **H_SE=1.9 GPa 초과 → 소성+균열**; "major portion of shear stress > 1.9 GPa"(stated) |
| **porosity vs cycle** (Pfab=100) | SOC8: 0.12↔0.145 / SOC16: 0.155↔0.185 / SOC24: **0.18↔0.21** | Fig 8c | digitized | **삽입(lithiation)서 porosity↑**(팽창이 SE 밀어내며 void 생성); SOCmax↑ → porosity↑ |
| **porosity vs Pfab** (SOC24) | Pfab100: 0.22 / 200: 0.155 / **500: 0.06** | Fig 8d | digitized | **높은 제조압 → 낮은 porosity**(조밀 시작 → 사이클 후에도 조밀) |
| **wall pressure peak** (Pfab=100) | SOC8: ~200 / SOC16: ~450–500 / **SOC24: ~850–900 MPa** | Fig 8a | digitized | 삽입마다 주기적 응력 스파이크 — **제조압(100)보다 큰 작동압**(팽창이 SE층 밀어냄) |
| **height swing** (Pfab=100) | SOC8: 59↔61 / **SOC24: 59↔66 µm** | Fig 8b | digitized | SOCmax↑ → 높이 진동폭↑ |
| **tortuosity τ_SE** (Pfab=100) | SOC8: ~1.5–3 / SOC16: peak ~12–15 / **SOC24: peak ~25** | Fig 9a | digitized | ★ **균열(Fig 7)이 τ 급증의 원인**; SOC24 큰 스파이크 |
| τ_SE vs Pfab (SOC24) | Pfab500: peak ~10–15(< Pfab100) | Fig 9b | digitized | **높은 제조압 → 균열↓ → τ 스파이크↓**(덜 열화) |
| **κ_SE^rel = φ_SE/τ_SE** (Pfab=100) | SOC8: 0.22–0.28 / SOC16: 0.03–0.15 / **SOC24: 0.02–0.12** | Fig 9c | digitized | **delithiation서 κ↑**(SE 더 조밀); 사이클마다 **영구 감소**; SOC24 최대 손실 |
| **κ_SE^rel 영구감소 vs Pfab** | **Pfab↑ → 영구감소 *현저히* 작음** | Fig 9d | stated | ★ **핵심 내구성 결과**: 제조압이 사이클 σ-유지를 결정 |
| **κ_SE^rel 회복/영구손실** | 작은 팽창 → **near-original 회복**; 큰 팽창 → **영구 감소** | Abstract | stated | 회복(reversible) vs 영구(irreversible) 경계 = 팽창 크기 |
| **AM-SE contact area** (Pfab=100) | SOC8: 0.5↔2.8 / SOC24: peak ~3.3 (×10⁴ m²/m³) | Fig 10a | digitized | **lithiation서 접촉↑**(AM이 SE로 팽창); **delithiation서 급감**(수축→접촉손실) |
| AM-SE contact area vs Pfab (SOC24) | Pfab500: peak ~4.2×10⁴(> Pfab100) | Fig 10b | digitized | **높은 제조압 → 전체 접촉↑ AND 시간경과 접촉손실↓** |
| **균열 손상** | Pfab100·SOC24: *significant cracks*; Pfab200: *much less*; SOC8: *relatively unaffected* | Fig 7 | stated | **고압제조 + 저SOC = 균열 적음**; Fig 7에 white crack 라인 |

### 3.4 미측정 / n/a (우리 앵커와 직접대조 주의)
| 항목 | 상태 |
|---|---|
| **σ_ionic 절대값** | **n/a** — κ_SE^rel(=φ/τ, TauFactor *상대값*)만; σ_SE^bulk 곱으로만 절대 추정 가능. 접촉저항(Holm) *없음* |
| σ_electronic / σ_thermal | **n/a** — SE 이온전도만(AM/SE 전자·열전달 미산출) |
| coverage / coordination Z | **n/a**(명시 보고 없음; AM-SE contact *area*는 Fig 10 — coverage %는 아님) |
| Heckel P_y / knee | **n/a**(Heckel 안 함); 상대밀도-vs-P 곡선의 knee ~100 MPa 부근(digitized) |
| PSD (D10/D50/D90) | **n/a**(명시 표 없음; SE 응집체 5–10 µm, AM 단일 입경 미명시) |
| 소재 σ_grain | **n/a**(상대 κ만; 절대 σ_SE^bulk 미명시) |

---

## 4. 시뮬레이션 방법 ★ — ductile-particle 소성 DEM + 2-step 제조→사이클

> ★ 이 논문의 *엔진*은 **자매 So 2022 MethodsX 접촉모델**(평형 overlap h_eq 소성 rate + 경도 H 항복 + 융착결합 cohesive)이고, *새로움*은 그 위에 **(2) Si AM 의 *Li-삽입 팽창*을 얹어 *사이클 열화*까지** 가는 것이다. 아래는 (i) 접촉법칙(자매와 공유) → (ii) 제조 step → (iii) **삽입/열화 step(★ 이 논문 고유)** 순.

### 4.0 code / version
- **code**: **in-house DEM, MATLAB**(So 그룹 자체; "We developed our own DEM model in MATLAB and ran the calculations on a conventional PC"). LIGGGHTS/LAMMPS 아님. "original DEM model" = Cundall–Strack 1979 [17]. 적분/이웃탐색 세부는 자매 So 2021 JPS 본문 참조(Verlet 2차, kd-tree).
- 선행 DEM-ASSB 리뷰(§Intro): Gimenez [18](AM+CB 전자전도, *작은 변형*만+void=SE), Shi [19](AM/SE 크기최적화, **작은 SE가 mass transfer에 유리** — 우리와 동일 trend), Bielefeld [15,16](particle-based connectivity+contact-area+PSD — 우리와 가장 가까운 구조-모델링 peer), Fathiannasab [14](synchrotron tomography 구조 + galvanostatic; void가 mass transfer 저해, 고압제조 → 저porosity·적은 void). **DEM 소성 모델 선례**: Di Leo [26](Si nanotube SiO₂ shell 소성), Gao [27], Liu [28]. **Storåkers [20]**(spring-back) + **Luding [23]**(cohesive beam, no permanent deform) → 이 논문 모델의 출발.

### 4.1 탄성 접촉역학 (Fig 1, eq 1–4)
- 법선력 Hertzian (eq 1): `F_normal = k_spring·h_ov`, 스프링상수 (eq 2): `k_spring = 4/3·E_eff·h_ov^{1/2}·R_eff^{1/2}`.
- 유효반경 (eq 3): `R_eff^{-1}=R_1^{-1}+R_2^{-1}`; 유효모듈러스 (eq 4): `E_eff^{-1}=(1−ν_1²)/E_1+(1−ν_2²)/E_2`.
- 접촉반경 `a=√(h_ov·R_eff)`; 접촉 응력분포 = **포물선**(최대응력=평균의 3/2). + damping + Coulomb 마찰(자매와 동일, 본문 "detailed description in original DEM model [17]").

### 4.2 ★ 새 소성변형 모델 (New model of plastic deformation, Fig 2, eq 5–9)
**출발(Tomas [22]+Luding [23]):** "elastic Hertzian under low stress, permanent plastic when shear exceeds hardness." Luding 선형모델은 *낮은 경도/탄성*(σ_H/E<0.01)에만 유효 → **고체전해질엔 부적합** → **비선형 Hertz 유지하되 평형 overlap 으로 영구변형** 도입.

- **평형 overlap h_eq** (Fig 2b): 압축 후 두 입자가 *영구히 붙어있는* 새 평형위치. 법선력 (eq 5):
  ```
  F_normal = k_spring (h_ov − h_eq)         (h_eq=0 이면 순수 Hertz = elastic)
  ```
- **소성 rate(Maxwell 점탄성 유도)** (eq 6) — 완화시간 t_rel:
  ```
  ∂h_eq/∂t = (F_normal − F_threshold)/(t_rel·k_spring) · (1 − φ_solid^4)
  ```
  ★ **`(1 − φ_solid^4)` = over-compaction 방지 항** — 국소 solid volume fraction φ_solid→1 일 때 소성 rate→0(이 논문이 *2D 도메인에 z방향 두께=평균 SE직경* 부여해 φ_solid 추정; Voronoi tessellation 으로 국소 부피). t_rel ≪ 시뮬레이션시간(정상상태). "real time scale → unacceptably long → t_rel arbitrary & small for steady state."
- **항복 임계 F_threshold(경도 H)** (eq 7–8): 소성은 *임계력 초과* 시만 진행. 최대응력 σ_max=3/2·F_normal/A_con(eq 7); 항복:
  ```
  F_th = 2/3·σ_H·A_con          (eq 8)     (σ_yield ≈ σ_H 근사; 문헌 항복강도 부족)
  ```
- **접촉면적 + 표면거칠기 α** (eq 9): 매끈한 구의 A_con=π·h_ov·R_eff 는 *완전 매끈* 가정 — 실제 ASSB 입자표면은 거칠다 → **무차원 1-파라미터 α**(real 접촉면적/매끈구 비):
  ```
  A_con = π·h_ov·R_eff·α          (eq 9)    α=0.65 (Fig 4 Sakuda 보정)
  ```
- **strain hardening 무시**(실험 데이터 부족 명시). 일정하중 소성흐름: 접촉면적↑ → σ↓ → 응력이 더는 경도 초과 안 할 때까지 *시간경과 감소*(creep-like). **Fig 2c**: F_max=50/100/200 µN 별 force-overlap 이력 — 임계 초과 후 release 가 *오른쪽 평행이동*(h_eq>0 영구). **Fig 2d**: σ_H=1.0/1.5/2.0 GPa 별 — H가 *소성전이점*과 *최종 h_eq* 결정.

### 4.3 ★ 융착결합(cohesive contact) — over-compaction 항 + 음의 인력
- 소성 식 (eq 6)의 `(1−φ_solid^4)` 항: "In order to avoid over-compaction, we inserted a term that goes to zero when the estimated equilibrium solid volume fraction tends to unity." = 자매 So 2022 의 `h_ov^max=0.6R_eff` 와 *같은 목적*, *다른 형식*(여기선 φ_solid^4 게이트).
- **융착(cohesive):** "Sakuda et al.[9] indicates that atoms/ions diffuse at the material/pore interface, forming strong bonds during densification. Therefore we assumed sulfide SE particles that have undergone plastic deformation upon contact will exert *tensile* stresses during separation." → **소성변형한 SE 접촉은 *분리 시 인장력*(융착)** → 사이클 수축 때 *바로 안 떨어지고* 끌어당김 = 접촉면적 손실 *지연*. (자매 So 2022 의 consolidation/detachment dead-band rate 의 적용판.)

### 4.4 ★★ STEP 1 — 제조(cold press, SE-only 보정) (Fig 3–4)
- **SE-only(LPS 75 % dilithium sulfide)**: bottom=wall, top=**pressure wall(목표 Pfab 까지 가압)**, sides=주기경계. 입자를 **5–10 µm cluster**(Sakuda SEM 관찰)로 그룹화 — 초기위치는 pre-existing algorithm(연료전지 [32,33]), aggregation 계산 후 **중력패킹 DEM**.
- **Fig 3a**: Pfab 시간이력(빠르게 증가 후 완화); **Fig 3b**: 높이 지수감소 → release 시 springback(부분). **Fig 3c–f**: 입자 cluster 분포(초기 / 100·200·500 MPa, α=0.65 colored).
- **Fig 4a**: 상대밀도 vs Pfab, **α=0.50/0.65/0.80/1.00 + Sakuda(2013) open-circle 검증** — α=0.65 최적. **Fig 4b–d=Sakuda SEM(무압/74/360 MPa) vs 시뮬(e–g)** 정성대조 — voids 가 저압(b,c)서 존재하다 고압(d)서 붕괴.

### 4.5 ★★ STEP 2 — 삽입/사이클 열화 (intercalation damage) — ★ 이 논문 고유
- **anode(AM Si + SE) 2-step**: cold press(step1과 동일 BC) **+ intercalation**. 삽입 BC: **상단벽에 *스프링력* 추가**(부피팽창이 SE층+cathode층 압축을 만든다고 가정). **areal spring constant = E_SE/(L_SE+L_cat)**(SE 영률 ÷ (SE 두께+cathode 두께)). **SOC = 순간충전/용량**; Si 팽창 과대 → **부분삽입(SOCmax 8–24 %)**. β_Si=2.8(Obrovac) → 완전충전 부피 2.8×.
- ★ **AM 입자가 SOC 따라 *팽창*** → 주변 SE 입자 밀어냄 → (i) AM-SE 접촉면적↑(lithiation)·↓(delithiation), (ii) SE 입자간 응력↑(Fig 6), (iii) 응력 > H_SE(1.9 GPa) 또는 융착 인장 초과 → **소성+균열 → 융착 끊김 → 영구 σ 손실**.
- **균열/cohesive 파괴 판정(eq 10)**: 인장응력이 SE 균열 유발. **cohesive theory of fracture** [25 Bucci 2018]: 인장응력이 *경도(σ_H)* 초과 시 입자 *연결 상실*. fracture strength σ_c=2γ/δ=**5.6 GPa**(γ=2.8 J/m², δ~1 nm); 경도/파괴강도 **σ_H/σ_c=1.9/5.6=0.34** → **초기 파손은 *소성*이 지배**(취성 아님 → "ductile particle"). ⇒ **분리(detachment) 조건은 *경도* 기준(σ_H 초과 인장 시 융착 끊김), *fracture strength*(5.6)는 더 위** = 소성이 먼저.
- **5 사이클** 반복(Fig 7–10): 각 사이클 = lithiation(팽창)→delithiation(수축).

### 4.6 입자 처리 ★★ (DEM판 "무질서 처리")
- **구(sphere)만** — AM·SE 모두 구. **형상은 절대 변하지 않는다.** 소성 = **CONTACT 소성**(평형 overlap h_eq = 접촉점 국소 함몰/융착 proxy)이며 **진짜 입자 SHAPE 흐름(void-fill flow)이 아니다.** 저자 명시(Future research): "natural step is to extend to **non-spherical particles** which can be simulated in DEM by the **multisphere method**."
- 단 **소성 + 융착(cohesive) + α 거칠기 + φ_solid^4 over-compaction 게이트 + *사이클 균열(detachment)*** 까지 = *접촉 수준*에서 가능한 최대 정교함. **rigid sphere 이지만 CONTACT 소성·융착·접촉손실·균열까지 있는** 중간지대.
- SE = **5–10 µm 응집체(cluster)**; 단일 1차입경 mono-disperse 의 집합이나 *응집구조 자체가 multi-scale*. AM(Si)는 큰 단일입자.
- ★ **명시 한계(Shortcomings):** "2D cluster DEM may **overestimate solid fraction** at low Pfab"; "particle number limited to **1600** in AM-SE sims → 더 많은 입자로 number-independence 확인 필요"; "AM expand at *same rate* throughout (확산분포 무시) — 고율방전서 SE층 근처 AM이 더 팽창."

### 4.7 도메인/RVE / servo / seeds / 압력범위
- **2D**(z방향=평균 SE직경 두께 부여, 부피분율 추정용 Voronoi tessellation). SE-only 보정 + anode(AM+SE) 적용. 입자 **≤1600**(AM-SE).
- **압력**: 제조 Pfab=50/100/200/500 MPa(상대밀도 Fig 4); 열화 Pfab=100/200/500. 삽입 SOCmax=8/16/24 %. **5 사이클**.
- **servo**: 상단 pressure-wall(제조) + 상단 spring(삽입, areal const E_SE/(L_SE+L_cat)). PI 제어 명시는 자매(So 2021 JPS)와 동일 추정.
- **seed**: 다중실현·통계 명시 없음(단일 실현으로 보임).
- **특이사항**: α(거칠기), t_rel(완화), φ_solid^4(over-compaction), 융착 인장 — 4개 보정/물리 인자. real time scale 대신 t_rel arbitrary(정상상태).

---

## 5. 결과 상세 — Section-by-section (모든 수치)

### 5.1 §All-Solid-State Batteries (Intro) — 문제 + frame[5] 위치
- ASSB 동기: 불연성 SE → 화재위험 제거, separator 겸용 → compact. Sun et al. [2] 리뷰 4대 도전: (i) AM-SE 화학양립성, (ii) 부족한 이온전도, (iii) 계면 이해 부족, (iv) 시스템 설계.
- **고용량 AM(Si, ~4200 mAh/g [3]) → ~300 % 팽창 → 심각한 기계열화** [4–6]. 팽창 → SE 균열(Li 전도 저해), 수축 → AM-SE 박리·AM 주변 shell void → AM-SE 접촉 감소. **SE 역학물성 중요**(dendrite 억제·계면저항·균열). **Glassy sulfide(Li₂S)** = 우수한 역학(Young's modulus가 lithiation 응력 완화)·상온 압력소결(2차접촉 없이 고온서 성능저하 회피)·Pugh's ratio ~2.4(조밀전극 형성능).
- **재구성 모델 survey**: top-down(Fabre 1D [11], Inoue-Kawase FIB-SEM 3D [12], Itoh [13], Fathiannasab synchrotron [14]) vs bottom-up(Bielefeld particle-based [15,16], Gimenez DEM [18], Shi DEM 크기최적화 [19]). **DEM 소성 선례**: Storåkers spring-back [20], cohesive beam(Tomas [22], Luding [23]). **Bucci [24] FEM-CZM 균열 + Bucci [25] 1D 박리** = 우리 digest 한 논문들 — **이 논문이 직접 인용·비교**(아래 §5.2).

### 5.2 ★ §Modelling failure of battery electrode (Intro 후반) — Bucci 와의 명시 대비
- **Bucci et al. [24]**: "used a **FEM model** to simulate fracture in ASSB electrode. AM = expanding cubes, SE = continuous phase. Particle inhomogeneity in parameters. **SE fracture modelled by cohesive theory(CZM)** — cohesive zone around cracks limits progression. **Initial fracture occurs if AM allowed to expand more than 7 %**." ← **우리 Bucci digest 의 7.5 % 임계와 일치**(이 논문은 "7 %"로 인용).
- **Bucci [25]**: 1D AM-SE 계면 cohesive 박리 모델(delamination criterion + stability). property mapping → fracture vs plastic regime; "**plasticity of electrode materials could significantly prevent onset of delamination.**"
- **DEM 소성 ASSB 선례 빈약**: Di Leo [26](Si nanotube SiO₂-shell 소성, 안쪽으로 변형), Gao [27](Si-C core-shell 소성), Liu [28](SE stress contact model, SEI 주름→ratcheting·cyclic failure 위험↑).
- ★ **이 논문의 갭 주장(Purpose):** "Ductility is essential to form compact ASSB electrode + intimate contact. Calculations show ductility *reduces internal stresses* during intercalation [25]. **Despite the importance of ductility, to our best knowledge currently no model can simulate its effect on cold press densification and intercalation damage.**" ⇒ **이 논문 = *소성(ductility)을 cold-press 압밀 *그리고* 삽입 열화 *동시*에 넣은 최초 DEM**(저자 주장). "two-step: cold press fabrication + cyclic operation → how fabrication conditions affect degradation."

### 5.3 §Methods — 접촉모델(§4.1–4.3) + 2-step 구현(§4.4–4.5)
- DEM overview(Fig 1) → 소성 모델(eq 5–9, Fig 2) → SE-only 보정 BC(wall/pressure-wall/주기) + cluster 5–10 µm → anode 2-step(cold press + intercalation, 상단 spring). Table I 파라미터.

### 5.4 §Simulation of SE cold pressing for calibration (Results, Fig 3–4)
- **Fig 3a**: Pfab 시간이력(증가→완화); **3b**: 높이 지수감소→springback(release 시 증가하나 초기 미복귀); "higher Pfab → lower final height." **3c–f**: cluster 분포(초기/100/200/500, α=0.65).
- **Fig 4a**: 상대밀도 vs Pfab(α=0.50/0.65/0.80/1.00) + **Sakuda(2013) 검증**. **indentation hardness 1.9 GPa(McGrogan, 유사 Li₂S sulfide content)** 사용. **α=0.65 가 200–500 MPa 에서 잘 일치**; **저압(<200)서 차이 큼 — 3D aggregate 구조(b)가 더 큰 voids → 시뮬(2D)이 과치밀**. **4b–d=Sakuda SEM** vs **4e–g=시뮬**: voids 저압 존재→고압 붕괴.

### 5.5 §Simulation of cold pressing of ASSB electrode (Fig 5)
- anode(AM Si + SE) 제조: **Fig 5a=전극높이 시간이력**(지수감소→unload→안정); **5b=초기 분포**(검은 큰 Si AM + 파란 SE); **5c–f=제조후**(Pfab 50/100/200/500, **SE volume fraction 컬러바 0.5–1.0**). 고압일수록 조밀·SE분율↑.

### 5.6 ★★ §Simulation of intercalation of ASSB electrode (Fig 6–7) — 응력 + 균열
- **Fig 6a–b: lithiation 중 SE normal stress 분포(SOC별)** — "stresses increase with SOC." **6c: 응력 히스토그램** — **양수=압축, 음수=인장**; SOC8 vs SOC24. "**major portion of shear stress > hardness 1.9 GPa**" → **소성**; 일부 인장 → 균열. SOC24: ΔV/V=67 %, 응력 tail 6–8 GPa.
- **Fig 7: 5 사이클 후 전극구조(Pfab 100/200 × SOCmax 8/24)** — **white crack 라인**. **top row Pfab=100**: SOC8 *relatively unaffected*, SOC24 *significant cracks*. **bottom Pfab=200**: 두 SOC 모두 *훨씬 덜 손상*, 특히 SOC24. ⇒ ★ **"denser electrode from high Pfab → much less cracking after intercalation"** + "**higher Pfab less susceptible to internal pore and crack formation**"(Discussion).

### 5.7 ★★ §Time series of intercalation pressure, electrode height and porosity (Fig 8)
- **Fig 8a: wall pressure vs cycle(Pfab=100, SOCmax 8/16/24)** — **주기적 고압 스파이크**(삽입마다 AM이 SE층 밀어냄); SOC24 peak ~850–900 MPa(>제조압 100). **8b: 높이 vs cycle** — 삽입서 증가(SOC24 59↔66 µm). **8c: porosity vs cycle** — "**porosity increases during intercalation expansion and increases with SOCmax**"(0.12/0.155/0.18 baseline, peak +0.025–0.03). **8d: porosity vs cycle(SOC24, Pfab 100/200/500)** — "**higher Pfab → lower porosity**"(0.22/0.155/0.06).
- ★ **읽는 법(porosity 가 *삽입서 증가*):** Si 팽창이 SE 를 밀어내고 *수축 시 다시 안 메워짐*(소성+균열로 융착 끊김 + shell void) → 사이클마다 net void↑. = 우리 압밀(porosity↓)과 *반대 방향* 시간진화(우리는 제조서 porosity 줄이고 끝; 이 논문은 *작동서 porosity 늘어남*).

### 5.8 ★★ §Tortuosity and SE conductivity (Fig 9) — 열화의 *주범 진단*
- **κ_SE^rel = κ_SE^eff/κ_SE^bulk = φ_SE/τ_SE (eq 11).** τ_SE = SE 입자를 100 이미지에 투영 → **TauFactor[36]**(open-source MATLAB) 로 계산.
- **Fig 9a: τ_SE vs cycle(Pfab=100, SOC 8/16/24)** — SOC24 peak ~25(균열 때문). **9b: τ_SE vs cycle(SOC24, Pfab 100/200/500)** — Pfab↑ → 균열↓ → τ 스파이크↓. **9c: κ_SE^rel vs cycle(Pfab=100)** — "κ_SE^rel **higher during delithiation when SE particles more closely packed**"; **영구감소**(permanent decrease over cycles). **9d: κ_SE^rel vs cycle(SOC24, Pfab)** — "**permanent decrease in κ_SE^rel significantly less when Pfab higher**."
- ★ **핵심 진단(본문):** "**φ_SE only varied slightly within 10 % during expansion** → change in κ_SE^rel is **dominated by change in τ_SE**. Large variation in τ_SE explained by **development of cracks(Fig 7) that greatly increases the conductivity path.**" ⇒ **열화 σ-손실의 메커니즘 = porosity(φ) 거의 불변, *균열이 만든 tortuosity 증가*가 지배.** = 우리 σ_ionic 폼의 *τ*(C(τ) logpoly2)·*f_intact*(fracture-aware Holm)와 **직접 대응**.

### 5.9 ★★ §Contact area (Fig 10) — AM-SE 접촉손실 (deconstruction)
- **Fig 10a: AM-SE 접촉면적 vs cycle(Pfab=100, SOC 8/16/24, eq 9)** — "**contact area higher during lithiation, increases with SOCmax**. Contact area during delithiation **decreases between cycles, especially at first cycle.**" **10b: vs Pfab(SOC24, 100/200/500)** — "**Pfab not only increases overall contact area but also *reduces the contact area losses with time*.**"
- ★ **읽는 법:** 삽입(팽창) → AM-SE 접촉↑; 탈리(수축) → 접촉↓; **첫 사이클서 가장 큰 손실**(초기 융착이 끊기며 재접촉 못함). 고압제조 → 더 강한 융착·조밀 → 접촉손실 지연. = 우리 coverage_AM·Stage-E 접촉면적의 *사이클 시간축* 버전.

### 5.10 §Discussion (Novelty / Shortcomings / Future / Conclusions)
- **Novelty:** "A new DEM model with ductile particles able to simulate cold press fab + mechanical degradation. **Implementation of plasticity in DEM is novel, not only for battery electrodes but in the general context of particle simulation.** Two-step (cold press + intercalation) → effect of fabrication condition (pressure) on durability. Different from earlier studies where degradation simulated with *predetermined structure*." + "**Intercalation expansion → buildup of large stresses → crack formation. Electrode fabricated under higher Pfab less susceptible to internal pore and crack formation.**" → "**valuable tool to optimize fabrication processes + select adequate materials.**"
- **Shortcomings(저자 명시):** (1) **2D only** — 2D cluster DEM may overestimate solid fraction at low Pfab; z방향 두께=SE직경 가정; **구형 가정**(계산 단순화). (2) sub-particle 접촉 = α(무차원). (3) AM-SE 입자수 **≤1600** → number-independence 확인 필요. (4) intercalation 시 areal spring(SE+cathode 탄성) — foil layer 수축·foam packing 무시; 일부 압력이 실 배터리 범위 초과. (5) **coupled reaction+mass transfer 안 함** — AM이 *균일 rate*로 팽창(확산분포 무시); 고율방전서 SE층 근처 AM이 더 팽창 → 응력·접촉·균열·τ 분포 영향.
- **Future:** **non-spherical(multisphere)** [32]; micromechanical compression/nanoindentation 검증(rate 변화로 elastic/plastic 분리, hysteresis); **DEM+reaction/mass transfer coupling** → AM 팽창 분포를 reaction distribution 으로(이동계면 → **phase-field reaction[37]**); **dendrite 성장 phase-field + 균열 상호작용**[38,39]; **취성(brittle) 재료 확장**(인장강도 ≪ 압축 → 접근/분리 시 다른 항복강도 필요). "powder packing fabrication + granular jamming control 에도 적용 가능."
- **Conclusions:** "novelty = new plasticity model that simulates *transition from granular media to solid electrode product during cold pressing* + *crack propagation during cyclic charge*. Low Pfab → partial consolidation + voids → weak. High Pfab → significant plastic deform → strengthen cohesive bonds + minimize voids. **Fabrication pressure has a large impact on degradation; main reason = local voids → local crack nucleation sites. Model helps select suitable electrode materials to improve durability of future ASSBs.**"

---

## 6. Figure / Table set ★ (모든 그림·표 + 우리가 쓸 점)
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1** | DEM 접촉모델 모식: (a) spring+slider+dashpot, (b) overlap h_ov + 포물선 응력분포 a=√(h_ov·R_eff) | — | 우리 hooke/hysteresis 접촉의 기본 모식 (자매 So 2022 Fig 1과 동일 계보) |
| **2** | **소성 force-displacement**: (a) elastic(Hertz, 가역) vs (b) plastic(h_eq 영구 overlap) 모식, (c) F_max=50/100/200µN 이력, (d) σ_H=1.0/1.5/2.0 GPa 이력 | 임계 초과 후 release 오른쪽이동(h_eq>0) | ★ 우리 hooke/hysteresis 적재/제하 루프와 직접대응; (d) σ_H가 소성전이·최종 overlap 지배 = 우리 Stage-E H-기준 |
| **3** | 제조: (a) Pfab 시간이력, (b) 높이(loading/unloading+springback), (c–f) cluster 분포(초기/100/200/500 MPa) | 높이 ×10⁴µm; springback 부분 | 우리 vis_zoom·압밀 morphology 대비; springback = 우리 unload 거동 |
| **4** | **★ 제조 검증**: (a) 상대밀도 vs Pfab(α=0.50/0.65/0.80/1.00 + **Sakuda 실험**), (b–d) **Sakuda SEM**(무압/74/360) vs (e–g) **시뮬** | 상대밀도 0.30→0.70(74)→0.90(360)→0.95(500); α=0.65 best | ★ **(a) 실험 porosity@P 앵커 대응**; 저압 과치밀=3D aggregate 미모델(우리 floor 논의와 방향 주의) |
| **5** | anode 제조: (a) 높이 시간이력, (b) 초기 분포(검은 Si AM + 파란 SE), (c–f) 제조후(SE vol frac 컬러 0.5–1.0, Pfab 50/100/200/500) | — | bimodal(큰 AM + 작은 SE cluster); SE분율 공간분포 = 우리 복합 microstructure 대비 |
| **6** | **★ 삽입 응력**: (a–b) lithiation SE normal stress 분포(SOC별), (c) 응력 히스토그램(SOC8 vs SOC24; 양=압축/음=인장) | SOC24 응력 tail 6–8 GPa(>H 1.9); ΔV 22/67 % | ★ **응력 > H_SE 1.9 → 소성+균열**; 우리 force-chain/Stage-E 응력의 *사이클* 버전 |
| **7** | **★★ 5사이클 후 균열**: Pfab(100/200) × SOCmax(8/24) 4-패널, white crack 라인 | Pfab100·SOC24=significant; Pfab200=much less; SOC8=unaffected | ★★ **고압제조+저SOC=균열↓**; 우리 Auerbach 균열의 *사이클-시점* 대응(driver 다름: 팽창 vs 접촉응력) |
| **8** | **★★ 사이클 시계열**: (a) wall pressure, (b) height, (c) porosity(Pfab=100, SOC 8/16/24), (d) porosity(SOC24, Pfab 100/200/500) | wallP peak ~900(SOC24); porosity 삽입서↑·SOCmax↑·Pfab↓ | ★★ **porosity가 *작동서 증가*(우리 압밀과 반대 축)**; wallP 작동압>제조압; 우리 porosity@P와 시간축 비교 |
| **9** | **★★ 열화 진단**: (a) τ_SE(Pfab=100), (b) τ_SE(SOC24,Pfab), (c) κ_SE^rel(Pfab=100), (d) κ_SE^rel(SOC24,Pfab) | τ peak ~25(SOC24); κ_rel 0.02–0.28; φ 변화<10 % | ★★ **열화 σ-손실 = τ(균열)가 지배, φ 거의 불변** = 우리 C(τ)·f_intact fracture-Holm 직접대응; **Pfab↑→영구손실↓** |
| **10** | **★★ AM-SE 접촉면적 시계열**: (a) SOC별(Pfab=100), (b) Pfab별(SOC24) | lithiation↑/delithiation↓; peak 2.8–4.2×10⁴ m²/m³; 첫사이클 손실 최대 | ★★ **접촉손실 시간축**(우리 coverage_AM·Stage-E 면적의 사이클판); 고압제조→접촉손실↓ |

> ⚠ **Table I 가 유일한 표**(파라미터 14행). SI 별도 없음. 방법 원전 = 자매 **So 2022 MethodsX 101857**(접촉모델 완전유도) + **So 2021 JPS 230344**(수치세부) + **So 2020 JES 013544**(2D 정초).

---

## 7. Post-processing ★
- **무엇:**
  - **상대밀도/porosity**: 입자→2D(z=SE직경 두께 부여)→**Voronoi tessellation**으로 국소 부피분율 → solid volume fraction. over-compaction은 (1−φ_solid^4) 게이트로 차단.
  - **응력장**: SE normal stress 분포(공간) + 히스토그램(압축/인장 분해), SOC별. (Fig 6)
  - **균열**: 인장응력이 σ_H(또는 융착 인장) 초과 시 융착 끊김 → 균열 가시화(Fig 7 white line). cohesive theory of fracture(σ_c=2γ/δ).
  - **tortuosity τ_SE**: SE 입자 100-이미지 투영 → **TauFactor[36]**(Cooper/Imperial open-source MATLAB, 라플라스 확산 풀이 — 우리 τ_Laplace와 같은 종류). **κ_SE^rel = φ_SE/τ_SE (eq 11).** (Fig 9)
  - **AM-SE 접촉면적**: A_con=π·h_ov·R_eff·α (eq 9) per 접촉 합 → 시계열(Fig 10).
  - **시계열 메트릭(★ 사이클판)**: wall pressure, 전극 height, porosity, τ_SE, κ_SE^rel, AM-SE 접촉면적 — *모두 cycle number 함수*(5 사이클).
- **도구**: 자체 MATLAB DEM + **TauFactor [36]**(외부). 응력·porosity·접촉·균열은 자체 후처리.
- **수치화·기록 방식**: 제조 = 상대밀도 vs Pfab(50–500, α-sweep) → **Sakuda et al.(2013) 실험 검증**. 열화 = 6개 메트릭 vs cycle number(5사이클) × (SOCmax 8/16/24 @ Pfab=100) × (Pfab 100/200/500 @ SOC24) 2-축 sweep. **회복(reversible) vs 영구(irreversible)** 를 사이클 간 baseline drift 로 판정.

---

## 우리 DEM+MPM 대비 (comparison vs ours)
> ★ **사용자 MANDATORY A.** 이 논문 = *제조 ductile-DEM* + ***사이클 열화 DEM*** vs 우리 *제조 hooke/hysteresis+Stage-E+MPM-J2*. **핵심: 그들의 *사이클 접촉손실 DEM* 이 우리 frame[5] *시간축 공백* 의 후보** — Bucci CZM 과 *같은 칸, 다른 방법(DEM)*. "진짜 차이" vs "method-artifact" 명시 구분.

### 7.1 핵심 대비표
| 항목 | 이 논문 (So 2021 JES) | 우리 DEM+MPM | 차이 / 이유 (진짜 차이 vs artifact) |
|---|---|---|---|
| **시간축(★ 핵심)** | **제조 + *사이클 작동 열화*** (2-step) | **제조(압밀)만** — frame[5] 사이클 미보유 | ★★ **진짜 다른 칸** — 그들이 *사이클 열화*(우리 공백)를 *DEM*으로 가짐. 우리 정적 σ → 그들 *사이클 시계열* σ |
| **DEM 소성** | **CONTACT 소성 명시**(h_eq Maxwell rate + H 항복캡 + 융착 + α 거칠기) | hooke/hysteresis(plasticity 無) + Stage-E(Tabor) 사후보정 | **같은 부류**(CONTACT 소성, δ/h_eq 잔류) — **진짜 SHAPE 흐름 아님**. 우리 MPM만 shape-flow. So의 h_eq+H항복 = 우리 Stage-E의 DEM-내장판 |
| **항복캡** | **✅ F_th=2/3·σ_H·A_con (eq 8)** — H에서 응력 cap | **✗ 없음**(Luding no-cap) → 18× 연화로 보상 | ★ **핵심 차이**: So는 항복캡 있어 *real E=24*로도 압밀 재현(Sakuda 일치). 우리는 캡 없어 24→1.35 연화. **So H-cap = 우리 연화의 물리적 대안(경로 A)** |
| **E 연화** | **연화 안 함**(real E=24) | E_eff=1.35(18× 연화) | So H-cap(eq8)+α+융착으로 real E 사용. "연화 irreducible"은 *우리 hooke/hysteresis에 캡 없는 탓* 재확증 |
| **사이클 열화 모델** | **✅ Si 팽창(β=2.8)→접촉손실·균열·κ 영구감소** (DEM) | **✗ 없음**(정적 압밀 σ만) | ★★ **그들이 앞섬(frame[5] 공백)**: 우리는 제조-시점 σ; 그들은 *작동 사이클마다* σ 변화 추적 |
| **균열 위치/모델** | **SE 융착결합 *연성* 끊김**(σ_H 1.9 기준; σ_c=5.6 더 위 → 소성지배 0.34) | **AM 입자 *통계* 균열**(Auerbach P_c + Lawn) | ★ **반대 상 + 다른 모드**: 그들=SE 접촉 끊김(연성·융착), 우리=AM 입자 깨짐(취성 임계). **둘 다 fracture-aware σ 로 연결됨** |
| **열화 σ-손실 메커니즘** | **τ_SE(균열)가 지배, φ 변화<10 %**(Fig 9) | C(τ) logpoly2 + f_intact fracture-Holm | ★ **정성 일치**: 둘 다 "porosity보다 *tortuosity/연결성*이 σ 지배". So 가 *사이클 시간축*으로 입증 |
| **입자 형상** | 구만, 형상 불변(multisphere=future) | 동일(구·rigid) | **같음** — 둘 다 rigid sphere; So도 비구형 future. **형상 morphology는 우리 MPM만** |
| **소재 SE** | **LPS=75Li₂S·25P₂S₅ glass**, E=24, H=1.9 | **LPSCl(argyrodite)**, E_eff 1.35/real 24 | **다른 SE**(glass vs argyrodite). E=24 우연일치; H=1.9는 우리가 안 쓰는 LPS 경도 |
| **소재 AM** | **Si *음극*** (E=70, β=2.8 팽창) | **NMC811 *양극*** (E=140, 팽창 미미) | ★ **다른 AM(음극 vs 양극)**: Si는 ~280 % 팽창(열화 driver) — **NMC 양극은 팽창 작음(~1–2 %) → So의 Si-팽창 열화는 우리 NMC엔 *과대*** (단 메커니즘=일반화 가능) |
| **전달 솔버** | **TauFactor(τ만)→φ/τ** (Kirchhoff 망 아님) | **Kirchhoff + Holm 접촉저항** | **다른 방법**: So는 연속체 라플라스 τ만(접촉구속저항 無), 우리 명시 저항망. **우리가 Holm·coverage·Stage-E 면적 더 정밀** |
| **전달 채널** | σ_ionic만(τ 경유, 상대값) | σ_ionic + σ_e + σ_thermal | **우리 삼중항 우위** |
| **차원** | **2D**(z=SE직경 두께) | DEM 3D / MPM 2D·3D | ★ **그들 2D**(자매 So 2021 JPS는 3D!) — 이 JES 열화 논문은 2D, 절대규모 주의 |
| **검증 앵커** | Sakuda 실험 상대밀도(제조만; *열화는 실험검증 없음*) | Minnmann/Doux/Bazzoun(LPSCl) + MPM 독립 | ★ **그들 *열화*는 정성/모델 예측만**(실험 사이클 데이터 미대조) → 추세만 |

### 7.2 ★★ 그들의 사이클-열화 DEM = 우리 frame[5] 시간축 공백의 *DEM 경로*인가? (Bucci CZM 대비)
**답: 그렇다 — *DEM 으로* frame[5] 사이클 칸을 채우는 가장 가까운 후보. Bucci(FEM-CZM)와 *같은 칸, 다른 방법*이고, *우리 파이프라인엔 So 가 더 가깝다*(입자·접촉·TauFactor).**

| 측면 | So 2021 JES (이 논문) | Bucci 2017 (FEM-CZM) | 우리 (현재) |
|---|---|---|---|
| 방법 | **입자 DEM** + cohesive hybrid-particle | 연속체 **FEM** + cohesive-zone | DEM(압밀)+MPM(morphology) |
| 균열 양식 | **SE 융착 *연성* 끊김**(σ_H 기준; 소성지배) | **SE *취성* cohesive 균열**(G_c, traction-separation) | AM *통계* 균열(Auerbach); MPM=연성 only |
| driver | **Si AM 팽창**(β=2.8, ~280 %) | AM Vegard 팽창(β_AM=0.1, ΔV 3–30 %) | 압밀 접촉응력(가압) |
| σ 영향 | **κ_SE^rel 영구감소 *정량***(τ-기반) | flux *비가역 0*(정성, σ_eff 미산출) | σ 삼중항 *명시*(정적) |
| 우리와의 거리 | ★ **가까움**(입자·접촉·τ — 우리 객체와 동종) | 멀음(연속체 FEM, 우리 미보유 도구) | — |
| 우리 채택 경로 | **LIGGGHTS 사이클-DEM**(Si→NMC 팽창 교체) | de Vaucorbeil continuous-damage MPM / CZM | A10/B6 backlog |

- ★ **핵심 판단:** **So 2021 JES 가 우리 frame[5] 사이클 공백을 채우는 *가장 실용적 경로*** — 왜냐 그들의 *모든 객체*(입자, 접촉, h_eq 소성, TauFactor τ, AM-SE 접촉면적)가 **우리 LIGGGHTS+Kirchhoff 파이프라인과 동종**이기 때문. Bucci 는 *연속체 FEM*(deal.II)이라 우리가 새 솔버를 만들어야 하지만, So 경로는 **우리 DEM 에 *AM 팽창 step(intercalation BC) + 융착 detachment + 사이클 루프*를 추가**하면 된다. **단 So 가 *연성(ductile)* 균열**(σ_H 기준)이라 *취성 SE 균열*(LPSCl argyrodite 가 더 취성? Bucci 가 다루는 영역)은 여전히 Bucci/de Vaucorbeil 쪽.
- ⚠ **회복 vs 영구**(So Abstract)는 **우리에게 *새로운* 정성 결과**: "작은 팽창 → 접촉·σ *회복*; 큰 팽창 → *영구* 손실." 우리 정적 σ 는 이 *reversibility 축*을 아예 안 가짐 → frame[5] 시간축 도입 시 *첫 목표 메트릭*(σ_cycle1 vs σ_cycleN drift).
- ⚠ **NMC ≠ Si 주의:** So 의 열화 *크기*(ΔV 67 %, wallP 900 MPa, κ 0.02–0.28)는 **Si 음극(~280 % 팽창)** 값 → **우리 NMC811 *양극*(팽창 ~1–2 %)엔 과대.** 메커니즘(팽창→접촉손실→τ↑→κ↓)은 일반화되나 *절대 열화량*은 NMC 로 재보정 필요(Si vs NMC = 100× 팽창 차). ⇒ **So 의 *방법*은 채택, *수치*는 NMC-재보정.**

### 7.3 ★★ "제조압↑ → 사이클 내구성↑" — 우리 압밀 결론과의 연결 (진짜 시사점)
- So 핵심: **Pfab↑(100→500) → 사이클 후 균열↓·κ 영구손실↓·접촉손실↓**(Fig 7/9d/10b). 메커니즘 = 고압 → 조밀(void↓) → **융착결합 강화 + local crack nucleation site(=void) 제거.**
- ★ 우리 연결: 우리 **porosity@300 MPa(real_14 15.6 %)·Minnmann(10 %)** = *제조-시점* 조밀도. So 는 **그 조밀도가 *사이클 내구성*을 결정**한다 함 → **우리 porosity 예측이 *작동 수명*으로 이어지는 다리**(우리 정적 porosity → So-식 사이클 열화 → 수명). 우리 σ_ionic 폼(τ·f_intact)은 *정적* 인데, So 가 *그 τ·f_intact 가 사이클마다 어떻게 악화*되는지의 시간진화를 준다.
- ⚠ **단 방향 주의:** 우리 압밀에서 porosity 는 *제조서 줄고 끝*; So 에서 porosity 는 *작동서 다시 늘어남*(팽창-수축 void). ⇒ "최종 porosity"가 아니라 "*제조 porosity(초기) → 사이클 porosity(증가)*" 두 단계 — 우리는 1단계만, So 는 2단계.

### 7.4 frame[4]/[5] 정직 정리
- **frame[4](cross-fit 금지):** 이 논문은 우리와 *교차검증* 대상 아니라 **frame[5] 시간축 *보완***. DEM/MPM 을 여기 맞출 일 없음(둘 다 experiment 독립 calibrate). 단 **β_Si=2.8·H_SE=1.9·γ=2.8 J/m²·σ_c=5.6 GPa·α=0.65·t_rel·areal-spring BC 는 *방법/literature 값* → 채택 가능**(우리 사이클-DEM 만들 때).
- **frame[5](분업):** **압밀 transport σ-삼중항 + packing/dip + 소성 morphology = 우리(DEM+MPM)**; **사이클 *연성* SE 접촉손실 열화 = So DEM(우리 미보유)**; **사이클 *취성* SE 균열 = Bucci CZM**; **우리 MPM J2 = 압밀-연성 only**(사이클·취성 둘 다 미보유). → So 는 **DEM 경쟁자가 *아니라* 우리 DEM 의 *시간축 확장 청사진*.**

---

## 적용가능성 (applicability to our model)
> ★ **사용자 MANDATORY B.** 구체적으로 *어디에·어떻게* 쓰나 — backlog **A10(사이클 chemo-mech) / B6(operating-pressure σ 시간축)** 의 *DEM* 레퍼런스 + ductile-particle ↔ 우리 18× 연화/경로-A. 스크립트 매핑.

### 8.1 backlog 매핑
| backlog | 항목 | 이 논문이 주는 것 | 적용 방법 (우리 스크립트) |
|---|---|---|---|
| **A10** | 사이클 chemo-mechanics (frame[5] 시간축) | ★ **DEM 경로 *원형*** — AM 팽창 step(intercalation BC, 상단 areal spring E_SE/(L_SE+L_cat)) + 융착 detachment + 5-사이클 루프 → 접촉손실·균열·κ 영구감소 시계열 | 우리 **LIGGGHTS pipeline 에 *intercalation step* 추가**: AM(NMC) 입경을 SOC-비례 팽창(β_NMC≈1.01–1.02, *Si 2.8 아님*), 매 사이클 σ 재계산(Kirchhoff). Bucci(FEM)보다 *우리 객체와 동종* → 구현 부담 적음 |
| **B6** | operating-pressure σ-degradation(시간축) | ★ **κ_SE^rel 영구감소 + 회복/영구 경계 + wallP 사이클 스파이크** | 우리 정적 σ_ionic(τ·f_intact)에 *사이클 drift* 추가: σ_cycle1 vs σ_cycleN; 작은 팽창=회복, 큰=영구. **τ_SE 가 지배(φ<10 %)** = 우리 C(τ) 항을 *시간함수*로 |
| **A2 (참고)** | wallP 조건부(skeleton-spring) | ★ **삽입 wallP 스파이크 = AM 팽창의 *역* (제조 vs 작동 압력)** | 우리 wallP(제조 300)와 So 작동 wallP(팽창 900) 구분 = Doux/Minnmann 제조-vs-작동압 분리와 합류 |
| **D6 (대비)** | SE 취성균열 | So=*연성* 융착 끊김(σ_H 0.34<1) → **취성은 *Bucci/de Vaucorbeil* 쪽** | So 의 *연성* detachment 와 Bucci 의 *취성* CZM 을 *둘 다* 비교 — LPSCl 이 어느 모드인지 결정(So σ_H/σ_c=0.34 → glass-LPS 는 소성지배; argyrodite-LPSCl 은 더 취성일 수 있음) |

### 8.2 ★ 직접 채택 가능한 *방법/literature 값* (우리가 입력/인용)
| 값/방법 | 출처(이 논문) | 우리 용도 |
|---|---|---|
| **β(expansion factor) 프레임** β=ΔV_full | Table I (β_Si=2.8, Obrovac) | ★ 우리 사이클-DEM 의 AM 팽창 입력 — **NMC811 로 *재보정*(β_NMC≈1.01–1.02, Si와 100× 다름)** |
| **areal spring BC** = E_SE/(L_SE+L_cat) 상단스프링 | Methods | ★ 삽입 시 SE+cathode 탄성 구속 모델 — 우리 작동압 BC 후보 |
| **융착 detachment(σ_H 기준)** | eq 10 + 본문 | ★ 우리 `--coh`/adhesion 의 *사이클 끊김* 확장(정적→rate); detachment 임계=σ_H |
| **σ_H/σ_c=0.34 (소성 vs 취성 판정)** | eq 10 | ★ *재료가 연성인지 취성인지* 판정식 — LPSCl 에 적용(우리 SE 가 어느 모드?) |
| **κ_SE^rel=φ/τ + TauFactor** | eq 11 | 우리 τ_Laplace 와 *같은 도구* — 사이클 τ 진화 비교 |
| **열화 진단: τ 지배, φ<10 %** | Fig 9 본문 | ★ 우리 σ_ionic 폼이 *왜* τ·f_intact 에 민감한지의 *사이클* 근거 |
| **회복 vs 영구 경계(팽창 크기)** | Abstract | ★ frame[5] 시간축 *첫 검증 메트릭*(reversible/irreversible σ drift) |
| **Pfab↑→내구성↑(crack nucleation=void)** | Fig 7/Discussion | ★ 우리 porosity 예측 → *수명* 다리(제조 조밀도 → 사이클 내구성) |

### 8.3 ★ 우리 Auerbach·Stage-E 와의 접목
- 우리 **Auerbach** = 압밀 접촉응력 → AM 입자 균열(통계 P_c). So = 사이클 팽창응력 → *SE 접촉 융착* 끊김(연성). **접목:** 우리 *압밀* fracture-Holm(f_intact)을 So-식 *사이클* detachment 로 시간확장 → "f_intact(cycle N)" → σ_ionic(cycle N).
- 우리 **Stage-E AM-SE 접촉면적**(Tabor F/H + volume + geom) = *정적*. So Fig 10 = *그 면적의 사이클 시계열*(lithiation↑/delithiation↓, 첫사이클 손실 최대). **접목:** Stage-E 면적을 *시간함수*로 → coverage_AM(cycle N) → σ(cycle N). **NMC 팽창 작아 So-Si보다 손실 훨씬 적을 것** → 우리 NMC 사이클 열화는 *완만*할 것이라는 예측(검증 거리).

### 8.4 한계 (적용 시 주의)
- **2D · ≤1600 입자 · 단일실현** → 절대규모·통계 우리 real 12:4:1 3D 와 다름(추세/메커니즘만).
- **AM=Si 음극(β=2.8)** → 우리 NMC 양극(팽창~1–2 %)에 *열화 크기* 과대; **메커니즘만** 전이, *수치*는 NMC 재보정.
- **SE=LPS glass(≠ LPSCl argyrodite)** → σ_grain·H·결정구조 다름; κ_rel *상대값*(절대 σ 전이 금지).
- **열화는 실험검증 없음**(제조만 Sakuda 대조) → 사이클 결과는 *모델 예측/추세*만 신뢰.
- **융착 *연성* 균열(σ_H 0.34)** → *취성 SE 균열*(Bucci/de Vaucorbeil)은 별도. coupled reaction/mass-transfer 무시(균일 팽창 가정).

---

## ★ 우리 novelty — 왜 우리가 state-of-the-art 인가 (our novelty vs this DEM model)
> ★ **사용자 MANDATORY C.** 근거 기반(그들 stated 범위·한계 인용), 과장 없이. **우리 DEM novelty 를 *firm* 하게 — 우리가 SOTA.** 단 *정직히*: **이 논문은 *사이클 열화* + *ductile particle* 을 *한다* → frame[5] 시간축 칸을 *그들이 가지고 우리가 없다*(credit).** 우리는 transport triad / Holm / MPM morphology / scaling-law 에서 앞선다. 7대 차별점 매핑.

1. **★ 전달 TRIAD(σ_ionic + σ_electronic + σ_thermal)를 *하나의 명시적 접촉망*에서 (Kirchhoff + Holm 1967 구속저항).**
   So 2021 JES 는 **σ_ionic *상대값*(κ_SE^rel=φ/τ, TauFactor)만** — σ_electronic·σ_thermal 없음, **접촉구속저항(Holm) 없음**(연속체 라플라스 τ). ⇒ **우리는 같은 rigid-sphere 압밀 위에 σ 삼중항을 Kirchhoff+Holm 명시 저항망으로** 얹는다. So 계보가 *구조적으로 비운 칸*이고 우리 transport novelty 의 위치.

2. **★ Stage-E 소성 접촉-AREA 재유도(Tabor F/H + volume + geom min-cap) — *전달에 연결된* 면적.**
   So 의 **α(eq 9)는 *압밀응력 보정 1-파라미터*(0.65)** — 표면거칠기를 *피팅*으로 접촉면적에 곱하고, **그 면적이 σ로 가지만 *상대 τ* 경유**(Holm 구속 없음). 우리 Stage-E 는 *같은 소성-면적 문제*를 **물리식 5-regime**(Tabor·volume·geom)으로 풀고 **Holm 구속저항·coverage 에 직접 투입**. ⇒ 우리 면적=*전달-연결·물리식*, 그들 α=*거칠기-피팅*. (단 정직히: α 의 *단순성*은 장점.)

3. **★ DEM↔MPM 커플링(scaffold) — 진짜 소성 SHAPE morphology 필드.**
   So 2021 JES 는 **rigid 구 + CONTACT 소성**(h_eq=함몰 proxy)이라 **입자 외형이 변하지 않는다** — 저자 명시 "multisphere(비구형)는 future." 우리는 **MPM(von Mises J2, ν=0.49) 진짜 소성 SHAPE 흐름·void-fill·Σdg** + **DEM AM scaffold + MPM SE 커플링**으로 porosity(15.93 %)·두께 EMERGE. ⇒ So 가 "구로 단순화"한 *형상-morphology 절반*을 우리 MPM 이 채운다.

4. **★ Fracture-aware 전달(Auerbach + Lawn → partial-Holm) — *전달에 연결된* 균열.**
   So 의 균열(Fig 7)은 **τ 를 통해 κ_rel 에 영향**(상대값) — 단 *AM 입자 균열 아님*(SE 융착 끊김), 그리고 **σ_e/σ_thermal 엔 무관**. 우리는 **Auerbach 임계 + Lawn → fracture-aware Holm(f_intact)**으로 *깨진 접촉이 σ_ionic *그리고* σ_e 에* 주는 영향까지 폼에 넣는다(AM_P 92:8 8mAh서 37–40 % cracked, σ_e fracture-reduced). ⇒ **단 So 가 우리보다 앞서는 *방향*: 그들 균열은 *사이클 시간축*, 우리는 *압밀 정적*** (→ §아래 정직 credit).

5. **★ 문헌-grounded σ_grain(Cronau/Trevisanello/Wang) — 재료물성 1차 앵커 + 절대 σ.**
   So 는 **κ *상대값*만**(σ_SE^bulk 미명시·절대 σ 없음). 우리 σ_ionic = **Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) GB**, σ_e=**Trevisanello 10/5 + NCM(r)**, σ_thermal=Wang — *각 채널 literature 고정·절대값*. ⇒ 전달 absolute 가 문헌-anchored(So 는 relative-only).

6. **★ 실험-앵커 *독립* 이중모델 보정 (frame[4]/[5]).**
   So 는 **Sakuda 상대밀도 *한 종류*에 α·t_rel·φ_solid^4 피팅(역학 단일모델), *열화는 실험검증 없음*.** 우리는 **DEM(E=1.35 hooke/hysteresis+Stage-E)과 MPM(E=1.53 J2)을 *각각 실험(Minnmann)에* 독립 보정** → 수렴(real_14 porosity 15.6↔16.7↔exp, coverage Tabor 48–52 %)=교차검증. ⇒ *두 독립 엔진 합의*가 우리 신뢰 척도.

7. **★ 솔버→스케일링법칙 압축(노이즈-천장 LOOCV) → ML 설계 예측기.**
   So 는 *접촉모델 → 사이클 시계열*에서 멈춘다(설계 역문제·ML 없음). 우리는 **솔버 출력을 노이즈-천장 LOOCV 스케일링법칙으로** 압축(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.90) → **설계 knobs → 전 메트릭 → 2D 미세구조 → 층상 복합양극** 5단계. ⇒ *예측·역설계*가 우리 정체성.

**⚠ 정직히 — 그들이 우리보다 앞서는 것 (frame[5] credit):**
- ★★ **사이클 작동 열화(intercalation degradation) — *우리가 *전혀* 안 가진* frame[5] 시간축 칸.** So 는 **AM 팽창(β)→접촉면적 사이클 진화→균열→κ_SE^rel *영구* 감소→*제조압이 내구성 결정*** 까지 *DEM* 으로 간다. 우리는 **제조-시점 정적 σ 만** — *작동 사이클마다 σ 가 어떻게 악화/회복하는지* 모델 없음. **이건 So(+Bucci)가 명백히 앞선 칸이고, 우리 미래 확장(A10/B6)의 청사진.** 특히 **회복(reversible) vs 영구(irreversible) σ 경계**(팽창 크기)는 우리에게 *완전히 새로운* 정성 결과.
- ★ **ductile-particle 소성 접촉모델(h_eq rate + H 항복캡 + 융착 + α)** — 우리 hooke/hysteresis(no-cap)보다 *접촉 소성 정교*. **So H-cap = 우리 18× 연화의 물리적 대안(경로 A)**: real E=24로도 압밀 재현. (단 *둘 다 rigid sphere* — 진짜 SHAPE 흐름은 우리 MPM 만.)
- ★ **Pfab↑→durability↑(crack nucleation=void)** — 우리 porosity 예측을 *수명*으로 잇는 다리. 우리는 porosity 까지만, So 는 그 porosity 의 *사이클 귀결*까지.
→ 즉 **사이클 열화·ductile 접촉의 *시간축 깊이*는 So 가, 전달 σ-삼중항·Holm·MPM morphology·scaling-law 의 *폭*은 우리가** 앞선다. 우리 SOTA 주장 = "*ASSB 복합양극의 구조→전달 σ-삼중항 + 소성 morphology + 설계예측 통합 파이프라인*"에 한정해 *정확*; **사이클 열화는 So/Bucci 가 소유한 frame[5] 칸**(우리 미래).

---

## 9. 인용 가능 문장 (deck/paper용)
- "So et al. (2021, *J. Electrochem. Soc.* 168, 030538) extended their ductile-particle DEM (nonlinear Hertz + equilibrium-overlap plasticity + hardness yield F_th=2/3·σ_H·A_con + cohesive fusion bonds) to a *two-step* simulation — cold-press *fabrication* followed by *cyclic intercalation degradation* — making it, to our knowledge, the **DEM counterpart of Bucci's FEM-CZM** for the frame[5] *cycling*-time gap our compaction models do not span."
- "In their model the cycling loss of ionic conductivity is **dominated by SE *tortuosity* (crack-driven), with φ_SE varying < 10 %** — directly corroborating why our σ_ionic scaling law is sensitive to the C(τ) and fracture-aware f_intact terms; So provides the *time-axis* evidence."
- "Crucially, **higher fabrication pressure yields greater cycling durability** (less cracking, smaller permanent κ_SE^rel decrease, reduced AM-SE contact-area loss) because dense electrodes remove the local voids that nucleate cracks — the bridge from our *static* porosity@P prediction to *operational* lifetime."
- "Small AM expansion (SOC 8 %, ΔV 22 %) lets contact area and conductivity *recover* near-original on contraction, whereas large expansion (SOC 24 %, ΔV 67 %) drives plastic deformation + cracking → *permanent* loss — a reversible/irreversible σ-drift axis our static models lack entirely."
- "⚠ Their degradation magnitudes (ΔV 67 %, wall-pressure ~900 MPa) are for a **Si *anode* (β_Si=2.8, ~280 % expansion)**; for our **NMC811 *cathode* (~1–2 % expansion)** only the *mechanism* transfers — the *numbers* must be re-calibrated, predicting far milder NMC cycling degradation."

## 10. 주의/한계 (over-claim 방지)
- ★ **소재가 다르다**: SE=**LPS=75Li₂S·25P₂S₅ glass(argyrodite 아님)**, AM=**Si *음극*(NMC 양극 아님; β=2.8 → ~280 % 팽창)**. σ_grain·E_CAM·H·결정구조 모두 우리(LPSCl+NMC811)와 다름 → **절대 porosity·σ·응력·열화량 전이 금지, 방법·메커니즘·추세만.** E_SE=24가 우리 real-bulk와 같은 건 우연(LPS도 sulfide).
- ★ **AM=Si 팽창이 *열화 driver*** → **우리 NMC 양극(팽창 ~1–2 %)엔 So 열화량 과대.** 메커니즘(팽창→접촉손실→τ↑→κ↓)은 일반화되나 *절대값*은 NMC 로 재보정 필요(Si vs NMC ≈ 100× 팽창 차).
- ★ **2D**(저자 명시 "we simulated only in two dimensions"; z=SE직경 두께 부여) — 자매 So 2021 JPS 는 3D 인데 *이 JES 열화 논문은 2D*. 절대규모·solid fraction(저압 과치밀) 주의.
- **rigid sphere + CONTACT 소성**: 입자 형상 불변(h_eq=함몰 proxy; 융착=접촉점 융합). **진짜 void-fill SHAPE 흐름 없음** → 우리 MPM morphology 영역 못 다룸. 저자 명시 "non-spherical multisphere=future."
- **κ_SE^rel=상대값(φ/τ, TauFactor)**: 명시적 접촉저항(Holm)·coverage·field-spreading 없음. σ_SE^bulk 미명시 → 절대 σ 없음. 우리 Kirchhoff+Holm 이 접촉구속 더 정밀.
- **열화는 실험검증 *없음***: 제조(상대밀도)만 Sakuda 대조; *사이클 결과(Fig 6–10)는 모델 예측/추세*만(실험 사이클 데이터 미대조). → 사이클 수치는 추세/메커니즘만 신뢰.
- **융착 *연성* 균열(σ_H/σ_c=0.34, 소성지배)**: *취성 SE 균열*은 별도(Bucci CZM / de Vaucorbeil). LPSCl argyrodite 가 *연성*인지 *취성*인지는 미결(So 의 glass-LPS 는 소성지배).
- **coupled reaction/mass-transfer 무시**: AM 균일 rate 팽창(확산분포 무시) — 고율방전서 SE층 근처 AM 더 팽창(저자 명시 future).
- **≤1600 입자·단일실현·α/t_rel/φ_solid^4 피팅인자**: 통계·number-independence 미확인(저자 명시); 보정값 직접 대입 금지.
- **그림 읽은 값(digitized)은 추세만(±)**: 상대밀도·porosity·wallP·τ·κ·접촉면적 곡선 수치는 Fig 3–10 에서 읽은 근삿값. stated(Table I 파라미터, β_Si/H_SE/γ/σ_c, ΔV 22/67 %, "φ<10 %", "Pfab↑→내구성↑")와 구분.
- **DOI 표기**: 표지 "abed23"는 IOP 내부 코드; 정식 인용은 **J. Electrochem. Soc. 168, 030538** (DOI 10.1149/1945-7111/abe796 계열).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
