# Bielefeld 2020 (ACS Appl. Mater. Interfaces 12, 12821−12833) — 유효 이온전도도 + 바인더 영향 모델링 (Janek 그룹, GeoDict — ★ Bielefeld 2019의 σ-추가 후속편)

> slug `bielefeld2020_effective_ionic_conductivity_binder` · DOI `10.1021/acsami.9b22788` · type `FEM·digital-twin` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Anja Bielefeld, Dominik A. Weber, Jürgen Janek, "Modeling Effective Ionic Conductivity and
Binder Influence in Composite Cathodes for All-Solid-State Batteries", *ACS Appl. Mater. Interfaces*
**2020**, *12*, 12821−12833.  DOI **10.1021/acsami.9b22788**.
Received 2019-12-17, Accepted 2020-02-25, Published 2020-02-25.
소속: Physikalisch-Chemisches Institut + Center of Materials Research (LaMA), **Justus-Liebig-Universität
Gießen** (Janek 그룹) + **Volkswagen AG, Group Innovation, Wolfsburg** (Bielefeld, Weber).
연락저자 anja.bielefeld@volkswagen.de / juergen.janek@phys.chemie.uni-giessen.de.

> ⚠ **연도 정정:** 위시리스트는 이 논문을 "Bielefeld 2022"라 불렀으나 **실제는 2020**(받은 날 2019-12-17,
> 게재 2020-02-25).  같은 GeoDict 구조-모델링 계보 = Bielefeld **2019**(JPCC 123, 1626 — 이미
> `docs/lit_bielefeld2019_microstructural_modeling_composite_cathodes.md`로 digest됨)의 **직접 후속편**.

**소재(모델):**
- **AM = NCM-811**(LiNi₀.₈Co₀.₁Mn₀.₁O₂) — σ_eff 본 계산에서는 σ_AM(이온) = 10⁻⁴ mS/cm (Amin & Chiang
  NMC523값, AM 이온전도는 SE 대비 4 orders 작아 *무시*).  C-rate 추정(§3.3)에서는 NCM811 비용량 196 mAh/g·
  밀도 4.76 g/cm³ 사용.
- **SE = LPSCl (Li₆PS₅Cl)**, σ_bulk,SE = **2.7 mS/cm** (Kato 2016).  σ-vs-입경 시뮬 비교 검증(§3.1.1)에서는
  Kato 2018의 **LCO + LGPS(Li₁₀GeP₂S₁₂) + acetylene black** 미세구조를 SEM 기반 재구성(SI Table S2).
- 적용사례(§3.3)에서 SE를 **LGPS(3.2 mS/cm)** 와 **LSiPSCl(Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃, 25 mS/cm)** 으로도 비교.
- ★ 2019와 달리 **재료-무관이 아님**: σ_eff 절대값을 계산하므로 σ_bulk,SE = 2.7 mS/cm·AM/SE 접촉저항
  ρ_AM/SE = 40 Ω·cm²(Braun 2018, Kato EIS 추정) 같은 **재료 파라미터가 실제로 입력된다**.

**바인더:** PVDF(ρ=1.78 g/cm³) 와 NBR(ρ=1.0 g/cm³)을 **gravimetric density만** 비교(폼/배치는 둘 다 동일,
"binder bridge" = SI 절차로 생성한 *오목 meniscus*).  실험 비교점은 Nam et al. 2018(NCM622:LPSCl:C65:NBR).

**도구:** **GeoDict** (Math2Market GmbH, Version 2019 SP2) — voxel 기반.  ★ σ_eff는 GeoDict의
**flux-based 정상상태 풀이**(EJ-HEAT 솔버, Wiegmann & Zemitis 2006; 정상 열전도 PDE와 同형) — 즉 **2019의
"σ는 future work" 미룸을 *이 논문에서 풀었다*.**  단 이것은 **연속체/voxel PDE**(EJ-heat harmonic averaging)
이지, granular 점접촉 **constriction 저항(Holm/Greenwood)을 입자별로 푸는 RNM이 아니다**(§σ-method 분류 참조).

DB 동반 파일: `docs/data/bielefeld2020_sigma_binder.csv` (σ_eff·τ²·입경·porosity·바인더 분율 추세 + Bruggeman 비교).

---

## ★ 결론 한 문단 — 2019가 비웠던 "σ" 칸을 *연속체 flux PDE*로 채운 후속편; 단 constriction은 *여전히* 안 풂

Bielefeld 2019는 percolation 존재 + cluster 부피(utilization) + 기하 active interface까지만 가고 **유효
전도도 σ_eff 자체는 "future work"(constriction = Greenwood 1966)로 미뤘다.**  **이 2020 논문(같은 1저자)은
바로 그 σ_eff를 *추가*했다**: GeoDict의 **flux-based 정상상태 풀이**(∇·j=0, j=−σ∇φ, Poisson형, EJ-HEAT
솔버)로 SE 상의 **유효 이온전도도 σ_eff,ion + 이온 tortuosity factor τ²**를 계산하고, **바인더(CBD)가 SE
이온망을 막아 σ_eff를 떨어뜨리는 효과**까지 정량화한다.  ★ 이건 **우리 Stage-E σ_ionic + τ_Laplace/R_brug 작업
*그리고* 우리 CBD/바인더-블로킹 작업(#271 Hong PTFE void-fill, #19 Kim SuperP-vs-VGCF, 우리 additives.py +
voxel σ_ionic 블로킹)에 동시에 매핑되는** 가장 직접적인 한 편이다.

★★ **그룹-내부 진화의 가운데 토막:** **Bielefeld 2019**(percolation, σ *없음*) → **Bielefeld 2020**(*이 논문*:
연속체 flux-PDE로 σ_eff + 바인더 추가, 같은 1저자) → **Bazzoun 2026**(RNM/Holm constriction σ + 실험 EIS,
같은 Janek 그룹).  σ 솔버가 **점진적으로 정교해진다**: 2019 σ-없음 → 2020 **연속체 PDE σ(point-contact
constriction 없음 = σ의 *상한*)** → 2026 **RNM/Holm constriction σ(= 우리 접근)**.  ★ **즉 2020은 우리 contact-
network 방향으로 가는 *중간 단계*** — 연속체 σ는 granular 구속저항을 빼서 *과대(상한)* 평가하고, Bazzoun과
우리는 그 constriction을 *되돌려* 넣는다.  ⇒ 우리 novelty(공정→구조 + **granular constriction σ 삼중항** + MPM
소성)는 이 그룹이 *스스로 걸어온 궤적의 끝*에 정확히 놓인다.

★ **단 결정적 한계 3개**(아래 §10 정밀): (i) **연속체 flux-PDE = point-contact constriction *없음*** → σ_eff는
강체-접촉 granular망의 **상한(upper bound)** (우리 Holm 솔버는 그 아래로 깎는다); (ii) **porosity·조성·입경 =
*입력***(stochastic placement, 2019와 동일 미세구조 생성) → 공정-물리 압밀이 아님; (iii) **단봉 + (제한적)
trimodal PSD**, **bi/tri-modal은 입경비 1:1:2 trimodal 한 케이스만** → Furnas dip 정량은 여전히 없음.

---

## §1. 논문이 답하는 질문과 답

### 핵심 질문
ASSB 복합 양극에서 **유효 이온전도도 σ_eff,ion(과 그에 딸린 이온 tortuosity factor τ²)이 설계·공정 파라미터에
어떻게 의존하는가** — 구체적으로 (a) 조성(AM:SE), (b) AM 입경·입경분포, (c) **잔류 porosity(void space)**,
(d) **바인더(CBD) 분율·배치**.  그리고 이 σ_eff로부터 **실현 가능한 전류밀도·C-rate**를 추정해, "application-driven
cell design은 미세구조 레벨에서 시작한다"를 보인다.

### 핵심 답 (abstract + §3 + §4)
1. **조성:** AM 분율↑ → σ_eff,ion **선형 감소**(모든 입경에서).  τ²는 50:50서 ~2로 시작해 65:35까지 거의-선형
   상승, **65:35 AM:SE 초과서 *급격히* 상승**(특히 작은 입자).  → 고-에너지(고-AM) 설계는 이온전도가 한계.
2. **입경:** **작은 AM → σ_eff,ion↓ + τ²↑**(작은 입자가 더 많아 우회 장애물↑, Froboese 2019와 일치).  큰 AM →
   더 넓은 이온경로 → σ_eff↑.  → 작은 AM은 전자전도(2019)엔 좋지만 이온전도엔 *나쁨* = **이온/전자 trade-off**.
3. **porosity(void):** porosity↑ → σ_eff,ion **결정적으로 감소** (**5% void가 20% void 대비 σ_eff *2배*** @고-AM).
   τ²는 porosity↑서 가파르게 상승.  → "process-rooted property, 절대 무시 말 것"(2019 권고 재확인).
4. **★ 바인더(CBD):** **소량이라도 강한 음(陰)의 영향.** 부피분율 V(B):V(AM)=0.05 / 0.10 두 함량에서:
   - σ_eff,ion **급감**(특히 고-AM 70:30서 *abrupt drop*), τ²는 70:30서 **6.4(0.05) / 10(0.10)** 까지 상승
     (바인더-free 4.2 대비).
   - **active interface(Li 삽입 가능 SE/AM 면적)** 감소: 저-AM서 **17%(0.05) / 29%(0.10)**, 고-AM서 **43% / 82%**.
   - **utilization:** AM 이용률은 거의 불변(바인더가 *기존* AM-cluster에 추가되는 생성방식 때문)이나 **SE 이용률은
     70:30 AM:SE 초과서 유의하게 감소**(바인더가 SE 이온경로를 차단).
   → ★ "binder impedes and blocks ionic pathways; hence, not all SE particles contribute to ionic conduction."
5. **전류밀도/C-rate:** σ_eff로 추정 — **σ_bulk,SE < 5 mS/cm SE는 thick 전극의 enabler가 아니다.** 5 mA/cm² 목표 시
   σ_bulk,SE = 5 mS/cm이면 전극두께 **<70 µm** 필요.  LGPS(3.2)는 high-energy/intermediate서 C-rate <0.2 C로 낮고,
   high-power(60:40, τ²=1.7, 100 µm)서만 1.5 C.  → "이온전도도 10 mS/cm를 enhanced C-rate·합리적 에너지밀도의
   설계 타깃"으로 제시.  **미세구조 튜닝이 재료 σ만큼 중요**.

---

## §2. σ_eff 계산 방법 ★ (가장 중요 — 2019의 σ-deferral을 *어떻게* 풀었나 + 분류)

### 2.1 미세구조 생성 = **2019와 동일**(stochastic placement, GeoDict)
- §2 첫 문단 명시: "We use the AM microstructures generated in our **previous work**[ref 21 = Bielefeld 2019]"
  → **미세구조 생성 알고리즘은 2019 그대로**: AM = **겹침 없는 구**(uniform/multimodal), SE = **겹침 허용 convex
  polyhedra**(LPS의 낮은 Young's modulus ~25 GPa·연성을 *기하 겹침*으로 근사), 겹침은 AM에 할당, SE는 사전에
  더 치밀하게 생성해 보상.  **porosity·조성·입경 = 입력값**(공정 물리 없음).
- ⇒ ★ **분류는 2019와 동일: top-down / stochastic placement** (Choi·Kim taxonomy).  *추가된 것은 σ 솔버뿐*이지
  미세구조 생성은 placement 그대로.

### 2.2 ★ σ_eff = GeoDict **flux-based 정상상태 풀이** (§2.2, Eq 5–11) — 2019가 미룬 그것
- **지배방정식** (정상상태, 전하보존):
  ```
  j = σ E = −σ ∇φ        (7)   Ohm 법칙 (j=전류밀도, σ=국소 이온전도도, φ=전위)
  ∂ρ/∂t + ∇·j = 0  →  ∇·j = 0   (8,9)
  ∇·(−σ∇φ) = 0          (10)   = Poisson형 (정상 열전도와 同형)
  ```
- **솔버:** GeoDict의 **EJ-HEAT** (Wiegmann & Zemitis 2006, ref 50) — 정상 열전도 ∇·(β∇T)=f 솔버를 σ로 재사용
  (전기전도 ↔ 열전도 수학 동형).  **voxel face에서 harmonic averaging**(EJ-heat solver), 재료 경계서 명시적 jump.
  미세구조 양단에 전위차 ΔU 인가(Dirichlet) → 유효 σ 텐서 σ_eff (3×3) 계산.  ★ **conduction은 current collector에
  수직(x₃ 방향)** → 대각 σ₃₃ + off-diagonal σ₁₃·σ₂₃ (이온이 x₃에서 벗어나는 경향) 계산:
  ```
        ⎛ σ11 σ12 σ13 ⎞   ⎛ —  —  σ13 ⎞
  σeff =⎜ σ21 σ22 σ23 ⎟ = ⎜ —  —  σ23 ⎟    (5)
        ⎝ σ31 σ32 σ33 ⎠   ⎝ —  —  σ33 ⎠
  ```
- **두 상 모두에 σ 할당**(2019의 percolation과 다른 점): SE = σ_bulk,SE = 2.7 mS/cm, AM = 10⁻⁴ mS/cm(4 orders
  작아 사실상 절연), **AM/SE 계면 접촉저항 ρ_AM/SE = 40 Ω·cm²**(Braun 2018) — ★ 즉 **계면 접촉저항은 넣되**, 그것은
  *AM/SE 계면*의 면저항이지 *SE-SE 점접촉의 constriction*이 아니다(아래 2.3).
- **τ² 산출** (Eq 1,3,11): tortuosity factor를 σ로부터 *역산*:
  ```
  σ_eff,ion = (ε_SE / τ²) · σ_bulk,SE     (3)   →   τ² = (σ_bulk,SE / σ_eff,ion) · ε_SE   (11)
  ```
  ε_SE = SE의 전체-부피 부피분율(void 포함) = (1−φ)·ν_SE.  → ★ **Eq 11 = 우리 τ_Laplace,eff 정의와 同형**
  (τ² = σ_0·φ/σ_eff, Minnmann 2021 Eq 4와도 同), 단 그들 σ_eff는 연속체 PDE 출력.

### 2.3 ★★ σ-method 분류 — **연속체 flux-PDE(constriction *없음* = σ 상한)** vs 우리 Holm contact-network
- 2020은 σ를 **풀지만**(2019의 deferral 해소), 그것은 **voxel 연속체 PDE**(EJ-heat harmonic averaging)이다 —
  즉 SE 상을 *연속 매질*로 보고 그 안에서 전위장을 푼다.  ★ **granular 점접촉을 통과하는 전류의 수렴저항
  (constriction resistance, R∝1/(σ·r_c), Greenwood 1966 / Holm 1967)을 *입자별로 풀지 않는다*.**
  - 그들이 *넣는* 저항 = **AM/SE 계면 접촉저항 40 Ω·cm²**(면저항, charge-transfer류) — 이건 SE→AM Li 삽입
    계면의 저항이지, **SE-SE 입자간 점접촉의 좁힘 저항이 아니다.**
  - SE-SE 망 자체는 연속체로 다뤄지므로 **SE-SE 점접촉 constriction은 빠진다** → σ_eff,ion은 **강체-접촉 granular
    망의 상한(upper bound)** 쪽.  (Bielefeld 2019가 "constriction = future work"라 한 그 물리가 *2020에서도
    여전히 빠져 있다* — 2020이 추가한 건 *연속체* σ이지 *constriction* σ가 아님.)
- **대조표 (σ를 어떻게 푸나):**
  | | 푸는 것 | constriction(점접촉 좁힘) | 결과 위치 |
  |---|---|---|---|
  | **Bielefeld 2019** | percolation 존재 + cluster 부피만 | ✗ ("future work", Greenwood) | σ *없음* |
  | **Bielefeld 2020 (이 논문)** | **연속체 flux-PDE** σ_eff (EJ-heat) + AM/SE 면접촉저항 | ✗ (SE-SE 점접촉 좁힘 없음) | σ **상한**(연속체) |
  | **Bazzoun 2026** | **RNM** + FEM | ✅ Holm R=1/(2σr_c), Kirchhoff | constriction σ |
  | **우리** | **Kirchhoff/Holm contact-network** + Stage-E 소성면적 | ✅ Holm + Tabor 소성 r_c | constriction σ (삼중항) |
- ⇒ ★ **frame[5] 정확한 위치:** 2020은 **연속체 σ**(우리 MPM이 transport σ를 못 주는 것과는 다름 — 2020은 *이온*
  σ를 줌, 단 *연속체* 방식)이고, **point-contact constriction은 우리(+Bazzoun)가 더한다.**  즉 2020 σ_eff,ion ≈
  *constriction-free 상한* / 우리·Bazzoun σ < 그 상한(좁힘 저항만큼 깎임).

### 2.4 SI: σ-flux 시뮬 파라미터 (Table S1) + 도메인
- void φ = **15%**(Hlushkou 2018류), σ_bulk,SE(LPSCl) = **2.7 mS/cm**(Kato 2016), σ_AM(NMC532) = **10⁻⁴ mS/cm**
  (Amin & Chiang), ρ_AM/SE = **40 Ω·cm²**(Braun), ΔU = **1 V**, **resolution 0.2 µm/voxel**, 도메인 **(80×80×140) µm**.
- ★ resolution 0.2 µm = 200 nm → **입경 3 µm가 모델 하한**(2019와 동일 한계 — 우리 12:4:1 작은 SE 미해상 / 512 grid
  수렴 논의와 같은 해상도 한계를 그들도 가짐).

### 2.5 ★ 바인더(CBD) 생성 방법 (§2.3 + SI Figs S1, S2) — 우리 CBD 작업 직접 대응
- **폼:** 본 모델의 바인더는 **특정 morphology(예: PTFE fibril)를 갖지 않고**, AM 입자가 가까워지는 곳에 **오목
  meniscus("binder bridge")** 형태로 *번지게(smear)* 둔다.  → "binder covers active interface area and may affect
  ionic transport throughout the cathode" (Strauss류 관찰 인용).
- **GeoDict 생성 3-step(SI):** ① **Dilation** — AM 입자를 얇은 바인더 막으로 코팅(voxel 팽창, AM 근접부서 겹침);
  ② 코팅+AM을 한 덩어리로 봄; ③ **Removal** — 주어진 voxel 수만큼 축소(대부분 코팅 제거, AM 사이 *binder bridge*만
  잔류).  desired 바인더 함량까지 반복.  ★ dilation=removal 같은 rate → **최소 접촉각 = 고-젖음성(high wettability)
  바인더**.  outer voxel dilate-remove로 함량 정밀 조절(Math2Market smart script, ACK 사사).
- **부피↔질량 회계:** 바인더 부피분율 = **V(B):V(AM)**(0.05 / 0.10) — ★ **AM 부피에 묶음** → 바인더 wt%는 조성에
  따라 *변함*(AM↑면 바인더 wt%↑).  PVDF(1.78)·NBR(1.0) density로 wt% 환산(Fig 5a): V(NBR):V(AM)=0.10이면 NBR
  wt%가 AM-rich서 ~2.5(저-AM)→~3.4(고-AM); V(NBR):V(AM)=0.05이면 ~1.2→~1.8 wt%.  PVDF(더 무거움)는 같은 부피서
  더 큰 wt%.  → "작은 바인더 wt%(2 wt% 미만)도 *유의 부피*를 차지해 성능을 좌우할 수 있다."
- ⇒ ★ **이건 우리 voxel σ_ionic 바인더-블로킹과 *정확히 같은 층위*:** 바인더를 **σ=0(또는 저-σ) obstacle voxel**로
  넣어 SE 이온망을 막는다.  단 그들 배치 = *AM 표면 meniscus*(interfacial), 우리는 #271 Hong에서 PTFE를 σ=0 장애물
  + (Hong이 지적한) void-fill 역학효과까지 본다(아래 §8 cross-check).

### 2.6 적용-전류 추정 (§2.4 + Eq 12–17, SI Fig S3)
- σ_eff,ion으로 이온 ohmic 전류밀도 추정(전자전도는 carbon으로 비한계 가정, charge-transfer·AM 확산 무시 = "good
  case"):
  ```
  j_ion = σ_bulk,SE·(ε_SE/τ²)·(ΔU/l)   (14)   →   C-rate = j_ion/(ε_AM·ρ_AM·ν_AM·(1−φ)·l)  (16,17)
  ```
- ΔU = 0.1 V(IR drop) 제한.  → "common SE(<5 mS/cm)는 thick 전극 enabler 아님; 고-σ SE 필요."

---

## §3. 결과 — section별 ALL 수치 ★

### 3.1 유효 전도 (§3.1)

#### Fig 1 — σ_eff,ion(a) + τ²(b) vs 조성, 입경 3–15 µm (porosity 15% 고정, uniform AM)
- **(a) σ_eff,ion [mS/cm] vs ε_AM [vol%]** (하축 40→67 vol% AM, 상축 AM:SE 50:50→70:30):
  - **AM↑ → σ_eff *선형* 감소**(모든 입경).  대략(digitized 추세): **40 vol% AM서 ~0.55–0.62**(큰 입자 위, 작은
    입자 아래) → **67 vol% AM서 ~0.07–0.10**.
  - **입경 효과:** **큰 AM(15 µm)이 위, 작은 AM(3 µm)이 아래** = ★ **큰 AM → σ_eff↑, 작은 AM → σ_eff↓**.
    (작은 입자가 더 많아 우회 장애물↑.)
- **(b) τ² vs ε_AM** (하축 40→67, 상축 50:50→70:30):
  - **50:50서 τ²≈2** 시작 → **65:35까지 거의-선형 상승**(τ²∈[2,5], 통상 양극 수준) → **65:35 AM:SE 초과서 *급등***
    (특히 작은 입자: 67 vol%서 3 µm은 **~10**, 15 µm은 **~3.5** 수준 digitized).
  - "65:35 AM:SE 초과서 τ² abruptly rises, especially for small particles" (Froboese 2019 일치).
- → ★ 우리 σ_ionic 폼(√φ_eff·CN²·...)의 **CAM↑→σ_ion↓ + 고-AM서 비선형 악화** 거동과 정합; τ²-vs-조성은 우리
  τ_Laplace/R_brug-vs-조성과 직접 대응(단 절대값은 연속체 상한).

#### §3.1.1 문헌 검증 (Kato 2018 재구성, SI Fig S4 + Table S2)
- Kato 2018의 **LCO + LGPS + acetylene black** 양극을 SEM에서 재구성: LCO = 5-edge planar polyhedra(두께 µ=3 µm),
  LGPS = 7-edge convex polyhedra(enclosing Ø µ=4 µm).  solid vol%: **AM 38.1 / SE 57.1 / acetylene black 4.8%**,
  **void 15% 가정**(Kato가 void 미보고 → Hlushkou 13.2%류로 추정).
- **결과:** 재구성 미세구조 σ_eff,ion = **0.68 mS/cm, τ² = 2.29** vs **Kato 실측 0.73 mS/cm, τ² = 2.47**.
  → ★ **flux-based 시뮬이 실측 σ_eff·τ²를 잘 재현**(검증).  단 Kato는 void를 빼고 τ²를 계산해 *ambiguous*하다고 지적
  (ε_SE를 void 빼고 잡으면 τ² 약간 낮아짐).
- → ★ ★ **이게 2020의 σ가 실험-검증된 *유일* 절대점**: 0.68 (sim) vs 0.73 (exp) mS/cm — 단 이건 LCO+LGPS계이지
  NCM811+LPSCl이 아니다(소재 다름, 추세/방법 검증으로만).

#### Fig 2 — τ² vs ε_SE(SE 전체 부피분율) + **Bruggeman 비교** (입경 3·15 µm, porosity 15%)
- **τ²-vs-ε_SE** (하축 ε_SE ~18→44 vol%): 작은 SE분율(=고-AM)서 τ² 급등.  fit:
  - **3 µm: τ²_3µm = 0.325·ε_SE^(−2.018)** (data)
  - **15 µm: τ²_15µm = 0.668·ε_SE^(−1.213)** (data)
- **★ Bruggeman 비교(§3.1.3, Eq 18,19):**
  - **표준 Bruggeman: τ²(ε) = ε^(−1/2)** (구형 입자 이상 균질 분포 가정).  → **모델 미세구조의 τ²를 *심하게
    과소평가*** (특히 작은 AM·작은 SE분율서 **모델값이 Bruggeman의 4배**).
  - **수정 Bruggeman: τ²(ε) = γ·ε^(−α)** (2 DoF).  데이터를 *받아들일 만하게* 맞추나 **α∈[2.02, 1.21]·γ∈[0.32,
    0.67]** — 표준값(α=0.5, γ=1)에서 *크게 벗어남*(Froboese와 비슷).  "이 파라미터는 *추가 과학적 통찰을 주지 않는다*."
  - → ★ "Bruggeman은 ASSB 양극에 *그대로 쓰면 안 됨* — SE 입자의 morphology·입경·분포가 이온 tortuosity에
    영향을 주는데 Bruggeman은 그걸 무시한다."
- → ★ ★ **우리 R_brug(Bruggeman 대비 비)와 직접 대응:** 우리도 σ_thermal Ridge에 R_brug_over_full_physics를 쓰고,
  Bruggeman이 ASSB에 부적합함을 안다.  Bielefeld의 "모델 τ² = Bruggeman의 4배"·"수정 Bruggeman α/γ가 비물리"는
  우리 R_brug 사용·Bruggeman 불신의 **권위 있는 외부 근거**.

#### §3.1.2 + Fig 3 — AM 입경 + **multimodal(trimodal) PSD**
- **단봉(monomodal):** AM 입경 d∈[3,15] µm 스윕(70:30 AM:SE 고정).  τ²-vs-d **log-log 선형**: τ²(d)=a·d^(−b).
  d→0 극한 τ²_mono = **6.40·(d/µm)^(−0.246)** (SI Fig S5; R²=0.95) → **vanishing 입경 극한 τ²_mono = 6.40**.
- **★ trimodal(L:M:S = 1:1:2 개수비, ideal packing):** 큰 입자 d_L∈[5.5,13.5] µm 변화, 중 d_M=5.5 µm, 소 d_S=3 µm
  고정(de Larrard ideal: r_M=(√2−1)r_L, r_S=(√(3/2)−1)r_L).  → ★ **trimodal이 monomodal보다 *이온 tortuosity 낮춤***:
  vanishing 극한 τ²_tri = **5.55·(d_L/µm)^(−0.190)** (R²=0.99) → **5.55**(< mono 6.40).
  - "이온 tortuosity factor 3.5를 타깃하면 mono·multi 둘 다 **AM 입경 12 µm** 필요."
- **Fig 3(b,c):** trimodal σ_eff,ion·τ² vs ε_AM, d_L∈[5.5,13.5] 스윕 — **작은 입자 배열이 σ_eff↓·τ²↑** (multimodal에서도
  작은 입자가 우회 장애물).  단 multimodal은 mono 대비 전반적으로 τ²가 *약간* 낮음(packing 개선).
- → ★ **우리 bimodal 12:4:1 + Furnas dip과의 접점:** 그들이 *유일하게* 시도한 분포(trimodal 1:1:2)는 **de Larrard
  ideal packing geometry** — 우리 dip 근거(de Larrard/McGeary)와 *같은 기하 계보*.  단 ★ **그들은 dip(porosity-vs-AM%
  최소)을 *측정하지 않는다*** — porosity는 15% 고정이고, multimodal은 *이온 tortuosity 저감*만 본다.  ⇒ Furnas dip
  정량은 *여전히* 우리(또는 de Larrard) 소유.

#### Fig 4 — σ_eff,ion(a) + τ²(b) vs AM:SE비, **porosity 5/10/20% 비교** (d=5 µm 단봉)
- ★ **porosity 효과 = 강한 σ 레버:**
  - **(a) σ_eff,ion (log축):** **5% void가 20% void 대비 σ_eff *2배***(고-AM서).  porosity↑ → σ_eff 급락; 고-AM
    로딩으로 갈수록 더 급락(20%서 AM 80:20 근처 σ_eff가 절벽).
  - **(b) τ² (log축):** porosity↑ → τ² 가파른 상승.  고-AM·고-porosity 코너서 τ²가 폭증(20% void, AM 85:15서 ~60+).
  - "more voids → loss of ionic pathways" — 5% void가 dense·고질량로딩서 σ_eff 2× 우위.
- → ★ ★ **우리 "porosity 관계식에 조성 항 + porosity 항" + R_brug**의 직접 σ-데이터.  porosity가 σ_eff를 *2배* 좌우
  = 우리 σ_ionic-vs-porosity 의존(√φ_eff)·우리 porosity 중심 모델링의 외부 근거.  단 그들 porosity = *입력*(우리 측정
  porosity와 절대 동일시 금지).

### 3.2 ★ 바인더 (§3.2) — Fig 5 전체 (우리 CBD/바인더-블로킹 핵심 대응)

#### Fig 5 — 두 바인더 함량 V(B):V(AM) = 0.05 / 0.10 (d=5 µm, porosity 15%, AM:SE+B 비)
- **(a) 바인더 wt% vs ε_AM** (PVDF·NBR):
  - V(NBR):V(AM)=0.10 → NBR **~2.5(저-AM, 50:44.6)→~3.4 wt%(고-AM, 80:12.8)**.
  - V(NBR):V(AM)=0.05 → NBR **~1.2→~1.8 wt%**.
  - PVDF(1.78 g/cm³, NBR 1.0보다 무거움) → 같은 부피서 더 큰 wt%(곡선 위).
  - ★ "V(NBR):V(AM)=0.1이 *2 wt% 미만* wt%에서도 유의 부피를 차지 = 작은 바인더 wt%도 성능 좌우."
- **(b) utilization vs ε_AM** (AM·SE, 바인더 0 / 0.05 / 0.10):
  - **AM utilization: 바인더 무관 거의 불변**(바인더가 *기존* AM-cluster에 dilation으로 추가되는 생성방식 → AM
    이용률 영향 적음).
  - ★ **SE utilization: 70:30 AM:SE 초과서 *유의 감소***(바인더가 SE 이온경로 차단) — "binder impedes/blocks ionic
    pathways; not all SE particles contribute."
- **(c) active interface A_spec,a [10⁵ m²/m³] vs ε_AM** (0 / 0.05 / 0.10):
  - 바인더↑ → active interface 감소; **65 vol% AM 초과서 가장 큰 감소**.  바인더-free 곡선이 위, 0.05 중간, 0.10 아래.
- **(d) ★ 상대 active interface A_spec,a^binder / A_spec,a^free [%] vs ε_AM** (= 바인더에 의한 손실 정량):
  - **저-AM:** 0.05 → **17% 감소**, 0.10 → **29% 감소**.
  - **고-AM:** 0.05 → **43% 감소**, 0.10 → **82% 감소**(!).
  - ★ Nam et al. 2018(NCM622:LPSCl:C65:NBR, GITT 실험) AM/SE 접촉면적 데이터 overlay: 작은 AM(70 wt%≈48 vol%)·큰
    AM(85 wt%≈69 vol%)서 data·model 잘 일치; 중간 조성서 실험이 model보다 더 나은 접촉(Nam 미코멘트).
- **(e) σ_eff,ion vs ε_AM** (log축, 0 / 0.05 / 0.10):
  - ★ **바인더↑ → σ_eff *급감*, 70:30 AM:SE 초과 고-에너지서 *abrupt drop*** — 0.10 곡선이 고-AM서 절벽.
- **(f) τ² vs ε_AM** (log축, 0 / 0.05 / 0.10):
  - ★ 바인더↑ → τ² 가파른 상승.  **70 vol% AM서 τ² = 6.4(0.05) / 10(0.10)** vs **바인더-free 4.2** → NCM811:LPS:NBR
    에서 **1.8 wt%(0.10) / 0.9 wt%(0.05) NBR**에 해당(Fig 5a).
- → ★ ★ ★ **우리 CBD/바인더-블로킹 작업의 직접 대응 + 우리가 못 갖던 것 일부:**
  - 그들은 **바인더 부피분율 → σ_eff 감소·τ² 증가·active interface 손실**을 *정량 곡선*으로 줌.
  - **우리 voxel σ_ionic 블로킹**(SuperP 0.0168 < VGCF 0.0298 mS/cm, SuperP가 ~1.8× 더 막음)·#271 Hong PTFE(σ=0
    obstacle)·#19 Kim SuperP-vs-VGCF와 **같은 물리**(저-σ 상이 SE 이온망 차단).
  - ★ 단 ★ **그들은 바인더가 *interfacial meniscus*(AM 표면)에 앉는다** → SE-SE 이온경로보다 **AM/SE active
    interface**를 더 막는다(Li 삽입 면적 손실 강조).  우리 voxel 블로킹은 SE 이온망 일반 차단 → **배치(interfacial
    vs bulk) 비교가 cross-check 거리**(아래 §8).

### 3.3 적용 전류밀도 (§3.3) — Fig 6 + Table 1
- **Fig 6(a):** j_ion vs (전극두께 l, σ_bulk,SE) (70:30, τ²=4, ν_SE=30 vol%, ΔU=0.1 V).  → 5 mA/cm² 목표 시
  **σ_bulk,SE=5 mS/cm이면 l<70 µm 필요**.  **(b)** j_ion vs (AM:SE비, τ²) (l=100 µm, σ_bulk,SE=3.2).
  **(c,d)** C-rate 버전(NCM811 196 mAh/g, 4.76 g/cm³).  C-rate ∝ 1/l² → 100 µm서 LGPS는 2C 불가.
- **★ Table 1 (적용사례 3종):**
  | 파라미터 | high-energy | intermediate | high-power |
  |---|---|---|---|
  | 전극두께 l [µm] | 300 | 140 | 100 |
  | AM:SE vol% | 80:20 | 70:30 | 60:40 |
  | τ² | 10 | 4 | 1.7 |
  | j_ion,LGPS [mA/cm²] | 0.18 | 1.46 | 7.25 |
  | j_ion,LSiPSCl [mA/cm²] | 1.42 | 11.4 | 56.7 |
  | C-rate,LGPS [/h] | 0.010 | 0.19 | 1.5 |
  | C-rate,LSiPSCl [/h] | 0.074 | 1.46 | 11.9 |
- → LGPS(3.2 mS/cm)는 high-energy/intermediate서 C-rate 매우 낮음(<0.2 C); **LSiPSCl(25 mS/cm)** 만 thick·고-에너지서
  쓸만.  → ★ "**SE는 LiB 액체전해질(5–10 mS/cm)보다 *더 높은* σ가 필요**" — SE가 AM 표면을 쉽게 적시지 못하고 void·
  바인더가 경로를 막기 때문.

---

## §4. SI (Supporting Information) — 항목별 수치

- **SI §Binder generation(Fig S1, S2):** 위 §2.5 — Dilation→Removal 3-step, dilation=removal rate → 고-젖음성
  meniscus.  Fig S2 = AM→+Binder→+SE 합성 모식.
- **SI Table S1(σ-flux 파라미터):** void 15%, σ_LPSCl 2.7 mS/cm(Kato), σ_NCM532 10⁻⁴ mS/cm(Amin&Chiang),
  ρ_AM/SE 40 Ω·cm²(Braun), ΔU 1 V, resolution 0.2 µm/voxel, 도메인 (80×80×140) µm.
- **SI Fig S3(전류밀도 요소):** 이온전도(선형)·재료선택·application 레이아웃·전압강하(0.1 V) → C-rate 추정 요소
  모식 (LGPS/LSiPSCl/NCM811).
- **SI Fig S4 + Table S2(Kato 재구성):** §3.1.1 — LCO(5-edge polyhedra, 두께 µ=3 µm, ray µ=2.5 µm) + LGPS(7-edge
  convex polyhedra, enclosing Ø µ=4 µm), AM 38.1/SE 57.1/AB 4.8 vol%, void 15%, 도메인 (80×80×100) µm.
- **SI Fig S5(τ² vs 입경):** §3.1.2 — mono τ²=6.40·d^(−0.246)(R²=0.95), tri τ²=5.55·d_L^(−0.190)(R²=0.99),
  void 15% 고정.  mono d∈[3,15], tri d_L∈[5.5,13.5]·d_M=5.5·d_S=3 µm.

---

## §5. Post-processing ★

- **무엇:**
  - **flux-based σ_eff 풀이**(EJ-HEAT, harmonic averaging) → σ_eff 텐서 σ₃₃·σ₁₃·σ₂₃ (Eq 5) → σ_eff,ion.
  - **τ² 역산**: τ² = (σ_bulk,SE/σ_eff,ion)·ε_SE (Eq 11) — σ에서 tortuosity factor를 *계산*(2019는 미산출).
  - **Hoshen-Kopelman cluster**(2019 계승) → utilization θ_ν, active interface A_spec,a (바인더 영향 정량에 사용).
  - **Bruggeman 비교 fit**: 표준 ε^(−1/2) + 수정 γ·ε^(−α) → α/γ 적합 → ASSB 부적합 결론.
  - **입경 power-law fit**: τ²(d)=a·d^(−b) (mono/tri), 극한 τ² 외삽.
  - **porosity convention**: φ = V_pore/V_total (2019 Eq 2) — 단순 부피분율, 소성-보정 *없음*, **입력값**.
  - **전류밀도/C-rate**: Eq 12–17, ΔU=0.1 V, NCM811 196 mAh/g·4.76 g/cm³.
- **통계:** (2019에서 계승) percolation 전이영역서 분율당 10 미세구조; 본 논문 σ-곡선은 대표 미세구조.
- **도구:** **GeoDict 2019 SP2**(Math2Market) — voxel 생성(2019 알고리즘) + **EJ-HEAT σ-flux 솔버** + cluster 분석.
- **수치화·플롯:** σ_eff(mS/cm, 종종 log축)·τ²(log축) vs ε_AM(vol%)·ε_SE; 상-하축 병기(AM:SE vol%↔vol% AM);
  바인더 0/0.05/0.10 3곡선(Fig 5).
- ★ **이번엔 σ_eff·τ²를 *산출함*** (2019의 "미산출" 항목 해소) — 단 *연속체* σ(point-contact constriction 없음).

---

## §6. 비교 vs 우리 DEM+MPM ★ (핵심 섹션 — `our_dem_baseline.md` 대조)

### 6.1 σ-method head-to-head (가장 중요)
| 항목 | Bielefeld 2020 | 우리 DEM+MPM | 차이 / 이유 |
|---|---|---|---|
| **σ 푸는 방식** | **연속체 flux-PDE**(EJ-heat, ∇·(−σ∇φ)=0, voxel harmonic avg) | **Kirchhoff contact-network**(노드=입자, 간선=접촉저항) | ★ **연속체 vs granular 접촉망** |
| **constriction(점접촉 좁힘)** | ✗ **없음**(SE-SE 연속체; AM/SE 면접촉저항 40 Ω·cm²만) | ✅ **Holm R=1/(2σ·r_c)** + Stage-E Tabor 소성 r_c | ★ **우리가 더하는 것** — 2020 σ_eff = constriction-free **상한** |
| **AM/SE 계면저항** | ✅ 40 Ω·cm²(Braun, 면저항) | (우리는 SE-SE/AM-AM/AM-SE 접촉을 Holm으로) | 그들 = 면저항(charge-transfer류), 우리 = 점접촉 좁힘 |
| **σ_eff 절대값** | σ_eff,ion **0.07–0.62 mS/cm**(조성·porosity), Kato재구성 0.68(검증) | σ_ionic **0.04–0.18 mS/cm**(DEM) | 연속체 상한이라 *더 큼* 경향 — 비교는 추세 |
| **τ²** | ✅ **산출**(역산 Eq 11): 2(50:50)→4–10(고-AM), Bruggeman 4× | ✅ τ_Laplace/Dijkstra, R_brug | **같은 정의**(Eq 11=우리 τ²); R_brug 대응 |
| **삼중항** | **이온만**(σ_e 없음 — 2019서 percolation만, 2020서 σ_ion만) | ✅ **σ_ionic+σ_e+σ_thermal** | 우리 삼중항 우위 |
| **바인더(CBD)** | ✅ **부피→σ_eff↓·τ²↑·active interface↓ 정량**(meniscus 배치) | ✅ voxel σ=0 블로킹(SuperP 0.0168<VGCF 0.0298), #271 Hong PTFE | **같은 물리**; 배치(interfacial vs bulk) 비교 거리 |
| **미세구조 생성** | **stochastic placement**(2019 계승; porosity=입력) | **DEM 압력 압축**(porosity=출력) | ★ placement vs process-physics |
| **소성/형상변화** | SE overlap=기하 근사(연성 흉내), SHAPE flow ✗ | DEM δ-overlap + **MPM 진짜 소성** | 우리 MPM morphology 추가 |
| **PSD** | uniform + **trimodal 1:1:2 한 케이스**(de Larrard) | bimodal 12:4:1 + **Furnas dip 정량** | ★ 그들 dip 미측정(porosity 고정) |
| **소재** | NCM811 + LPSCl(σ=2.7), 검증은 LCO+LGPS | LPSCl + NCM811(σ_grain 3.0, E_eff 1.35/real 24) | 소재 다름(검증계 LCO/LGPS) → 추세 |
| **검증** | LCO+LGPS재구성 0.68 vs Kato 0.73(1점) | DEM↔MPM cross-val + Minnmann/Bazzoun 앵커 | 둘 다 모델; 그들 σ 검증 1점뿐 |

### 6.2 σ_eff 추세 — 우리와 일치하는가? (frame[4] 구조 descriptor 교차검증)
- ★ **일치(추세):**
  - **CAM↑ → σ_eff,ion↓**(Fig 1a) = 우리 σ_ionic 폼 + Minnmann 2021("CAM↑→σ_ion↓") + Bazzoun(70/75/80 wt%서
    0.137/0.101/0.065↓).
  - **porosity↑ → σ_eff↓**(Fig 4, 5% void가 20% void 대비 σ 2×) = 우리 σ_ionic √φ_eff 의존 + porosity 중심 모델링.
  - **τ²-vs-조성**(2→10) = 우리 τ_Laplace/R_brug-vs-조성.  **Bruggeman이 4× 과소** = 우리 R_brug·Bruggeman 불신.
  - **고-AM서 σ_eff abrupt drop**(65:35 초과) = 우리 dead-SE(고-AM서 SE 이온망 끊김) + Fig 7(2019) 이온 한계>79 vol%.
- ★ **입경 효과는 *부호가 우리 σ_ionic과 같되 채널이 반대*** (주의):
  - **그들: 작은 AM → 이온 σ_eff↓·τ²↑**(작은 AM 多 → 우회 장애물↑) — *이온* 채널, AM=장애물.
  - **우리·Bazzoun: 작은 SE → 이온 σ↑**(작은 SE 多 → SE-SE 접촉수↑·packing↑) — *SE* 채널, SE=전도체.
  - → ★ **둘은 모순이 아니다**: 그들은 *AM 입경*(이온의 장애물)을 키우는 효과, 우리·Bazzoun은 *SE 입경*(이온의
    전도체)을 줄이는 효과 — **"작은 SE 좋다 + 작은 AM(이온엔) 나쁘다"가 같은 그림**(SE 잘게·AM 굵게 = 이온 최적,
    Shi 2020 권고).  Bielefeld 2019의 "작은 AM → 전자 percolation↑"와 합치면 **작은 AM = 전자↑·이온↓ = trade-off**.
- ★ **직접 비교 *불가*(절대값):**
  - **σ 절대값:** 그들 σ_eff(연속체 상한, constriction 없음) > 우리 σ_ionic(Holm 좁힘 포함) — 절대 동일시 금지,
    *추세*만.  소재도 다름(그들 검증계 LCO+LGPS, σ_LPSCl=2.7 vs 우리 σ_grain 3.0).
  - **porosity 절대값:** 그들 5/10/15/20% = *입력*; 우리 15.6%·~10% = *측정 결과* → 질문이 다름.
  - **τ² 절대값:** 그들 연속체 τ²(constriction 없음) vs 우리 τ_Laplace(좁힘 포함) → 추세만.

### 6.3 frame[4]/[5] 의의
- **frame[4]:** 같은 Janek 그룹이 *독립적으로* (우리와 무관하게) **CAM↑→σ↓·porosity↑→σ↓·Bruggeman 부적합·고-AM
  abrupt drop**을 재현 → 우리 σ_ionic 거동의 외부 확증.  단 σ 절대값은 *연속체 상한*이라 frame[4] *추세* 교차검증
  (절대값 교차검증은 Bazzoun RNM·Minnmann 실험 소유).
- **frame[5]:** 2020은 **이온 transport σ**(연속체)에 머물고, **point-contact constriction·σ_e·σ_thermal·소성
  morphology·dip**은 없음 → 우리 DEM(constriction 삼중항)+MPM(소성)이 그보다 넓다.  동시에 그들이 *추가*한 σ는
  우리가 MPM에서 *못 주는* 것(MPM은 transport σ 부재)과는 다른 축 — **2020 = 연속체 이온 σ, 우리 DEM = granular
  이온 σ + 전자/열, 우리 MPM = 소성 morphology**.

---

## §7. ★ 그룹-진화 논증 (NOVELTY용 — 읽기만, NOVELTY.md 편집 안 함)

★ **Janek 그룹의 σ-솔버 정교화 궤적 = 우리 방향이 옳다는 그룹-내부 증거:**

| 단계 | 논문 | σ를 어떻게 푸나 | constriction | PSD | 우리 대비 |
|---|---|---|---|---|---|
| ① percolation | **Bielefeld 2019** (JPCC) | percolation 존재 + cluster 부피만 | ✗ "future work"(Greenwood) | 단봉 | σ 자체가 없음 |
| ② **연속체 σ** | **Bielefeld 2020** (*이 논문*, ACS AMI) | **flux-PDE σ_eff,ion + τ²**(EJ-heat) | ✗ (연속체, SE-SE 좁힘 없음) | 단봉+trimodal 1케이스 | **σ 상한**(constriction 없음) |
| ③ **constriction σ** | **Bazzoun 2026** (J. Power Sources) | **RNM** Holm R=1/(2σr_c) + FEM | ✅ | 구만 | = 우리 접근(이온만) |
| ④ **우리** | DEM+MPM | **Kirchhoff/Holm** + Stage-E 소성면적 | ✅ + 소성 Tabor r_c | bimodal+dip | **삼중항 + MPM 소성** |

- ★ **핵심 서사:** Janek 그룹은 σ 솔버를 **2019 없음 → 2020 연속체(상한) → 2026 RNM/constriction**으로 *스스로*
  정교화해왔다.  **2020은 우리(contact-network constriction) 방향으로 가는 *중간 단계*** — 연속체 flux-PDE는
  granular 점접촉 좁힘을 빼서 σ를 *과대(상한)* 평가하고, Bazzoun(2026)과 우리는 그 constriction을 *되돌려* 넣는다.
  ⇒ "공정→구조 예측 + **granular constriction σ 삼중항** + MPM 소성 morphology"라는 우리 3대 portion은 이 그룹이
  *걸어온 궤적의 자연스러운 끝*에 정확히 놓인다 (positioning 최강 근거).
- ★ **바인더까지 같은 궤적:** 2020이 *처음으로* 바인더(CBD)를 ASSB 미세구조 모델에 넣었고(2019는 carbon-free로
  *배제*), Bazzoun(CNF/PTFE 질량보정으로 제외)·Hong 2026(PTFE/NBR 디지털트윈, 같은 그룹 아님)·우리(voxel σ=0
  블로킹)로 이어진다.  ⇒ **바인더-영향 정량 = 2020이 그룹 안에서 *연 칸*, 우리 CBD 모델이 그 위에서 morphology·
  void-fill 역학까지 확장**.

---

## §8. ★ 바인더 ↔ 우리 CBD/바인더-블로킹 cross-check (위시리스트 #3 핵심)

### 8.1 물리 일치 — 저-σ 상이 SE 이온망을 막는다
- **Bielefeld 2020:** 바인더 부피분율 V(B):V(AM) 0.05→0.10 → **σ_eff,ion 급감 + τ² 4.2→6.4→10(70:30) + active
  interface 17–29%(저-AM)·43–82%(고-AM) 손실**.  바인더는 SE 이온경로를 *차단*("not all SE particles contribute").
- **우리 voxel σ_ionic 블로킹(#19 Kim regime):** **SuperP 0.0168 < VGCF 0.0298 mS/cm** → SuperP가 SE 이온망을
  **~1.8× 더 막는다**(저-σ 상이 SE 경로 차단).  = ★ **Bielefeld의 "바인더↑→σ_eff↓" 메커니즘과 同물리**(저-σ obstacle).
- **#271 Hong 2026(우리 소재계 LPSCl+NCM 실험):** σ_ionic = **Pwd 0.087 / S-Pwd 0.079 / PTFE 0.064 / NBR 더 낮음**
  → **PTFE 바인더가 σ_ionic을 0.087→0.064(−26%)** (바인더-블로킹 실측).  = ★ Bielefeld σ_eff↓의 **LPSCl 실험 확증**.
- **Lee 2025(우리 소재계):** PTFE 0.5/2/5 wt% → σ_ionic **0.069/0.024/0.007**(−90% @5 wt%) + σ_e 34/4.5/0.011
  (−99.97%) → ★ 바인더 wt%↑면 **양쪽 σ 급감** = Bielefeld의 "소량 바인더도 강한 음의 영향"의 *극단* 실험.

### 8.2 정량 cross-check (바인더 함량 → σ/τ²/면적 손실)
| 출처 | 바인더 | 함량 | σ_ionic 영향 | τ²/면적 영향 | 비고 |
|---|---|---|---|---|---|
| **Bielefeld 2020** | NBR/PVDF | V(B):V(AM)=0.05 | σ_eff↓(급감) | τ² 4.2→6.4 (70:30); active interface −17~43% | 모델(meniscus 배치) |
| **Bielefeld 2020** | NBR/PVDF | V(B):V(AM)=0.10 (≈1.8 wt% NBR @70:30) | σ_eff↓(절벽) | τ² 4.2→10; active interface −29~82% | 모델 |
| **#271 Hong 2026** | PTFE | 1 wt% (75:22.5:1.5:1) | 0.087→**0.064** (−26%) | (Hong: void 28.7→**22.3** vol%) | LPSCl 실측 |
| **Lee 2025** | PTFE | 0.5→5 wt% | 0.069→**0.007** (−90%) | σ_e −99.97% | LPSCl 실측 |
| **우리 voxel(#19)** | (SuperP 0D) | (도전재 regime) | SuperP **0.0168** < VGCF **0.0298** | (SuperP가 ~1.8× 더 막음) | 우리 모델 |

### 8.3 ★ 배치(placement) 차이 + 우리가 흡수할 것
- **Bielefeld 배치 = AM 표면 interfacial meniscus**("binder bridge", 오목·고-젖음성) → **AM/SE active interface(Li
  삽입 면적)를 우선 막는다**(Fig 5d, 고-AM서 −82%).  ★ 즉 그들 바인더는 *SE-SE 이온경로보다 AM/SE 계면*을 더 차단.
- **우리 배치 = voxel σ=0 obstacle**(SE 이온망 일반 차단) + **#271 Hong이 지적한 void-fill 역학효과**(PTFE가 pore를
  28.7→22.3 vol%로 *낮춤* = densification 도움) — ★ **우리 audit #5가 놓치는 양(+)의 역학효과**(우리는 PTFE를 σ=0
  obstacle로만 봄, 기계적 void-억제는 빠짐).
- ★ **cross-check 결론:** Bielefeld(σ↓·active interface↓, interfacial)·우리 voxel(σ↓, bulk)·Hong(σ↓ +void↓
  역학효과)이 **같은 σ-블로킹 물리의 세 단면**.  우리가 흡수할 것 = (i) **active interface 손실의 *고-AM 비선형성*
  (−43~82%)** — 우리 coverage/A_AM-SE 폼에 바인더 항 추가 시 *고-AM서 더 급감*하게; (ii) **interfacial vs bulk
  배치 비교** — 그들 meniscus(계면)가 우리 voxel(bulk)보다 active interface를 더 막는지 RVE 비교; (iii) **void-fill
  역학효과**(Hong) — Bielefeld·우리 voxel 둘 다 *없는* PTFE 양의 densification 효과 → MPM/DEM 역학에서 보강.

---

## §9. 우리 연구에 적용 인사이트 (가장 날카로운 3가지)

1. **★ 2020이 "σ를 *연속체*로 풀었다 = constriction-free 상한"이 우리 Holm-constriction의 정확한 positioning.**
   - Bielefeld 2019(σ 없음) → 2020(연속체 flux-PDE σ, 점접촉 좁힘 *없음*) → Bazzoun 2026(RNM/Holm constriction) →
     우리(Holm + Stage-E 소성 r_c) 라는 **그룹-내부 σ-솔버 진화**에서, **2020 σ_eff = 우리 σ의 *상한*** (granular
     좁힘만큼 우리가 깎는다).  ⇒ deck에서 "연속체 σ는 상한, 우리는 contact-network constriction으로 *현실*에 맞춤"
     서사의 직접 근거.  Kato재구성 0.68 (sim) vs 0.73 (exp)는 *연속체가 검증된* 유일점(LCO+LGPS, 소재 다름 주의).

2. **★ Bruggeman 4× 과소 + porosity 2× σ 레버 = 우리 R_brug·porosity-중심 모델링의 권위 있는 외부 근거.**
   - "표준 Bruggeman τ²=ε^(−1/2)가 모델 τ²를 *4배* 과소평가, 수정 α/γ는 비물리" → 우리 σ_thermal Ridge의
     R_brug_over_full_physics 사용·Bruggeman 불신을 *그대로* 뒷받침.  "5% void가 20% void 대비 σ_eff *2배*" →
     우리 σ_ionic √φ_eff·porosity 관계식에 porosity가 결정적임을 외부 σ-데이터로 확증.  → `docs/data/
     bielefeld2020_sigma_binder.csv`로 보관(τ²-vs-ε_SE fit·Bruggeman·porosity별 σ).

3. **★ 바인더-영향 정량(σ↓·τ²↑·active interface −17~82%) = 우리 CBD/바인더-블로킹의 직접 cross-check + 흡수
   타깃.**  (위 §8.)  특히 **고-AM서 active interface −82%**의 비선형성을 우리 coverage 폼에, **interfacial(그들
   meniscus) vs bulk(우리 voxel) 배치**를 RVE 비교에, **Hong void-fill 역학효과**(둘 다 없음)를 MPM/DEM 역학에 흡수.

---

## §10. 주의 / 한계 (over-claim 방지)

- ★ **σ_eff = 연속체 flux-PDE (point-contact constriction *없음*):** 2020이 σ를 *풀긴 했으나*, EJ-heat harmonic
  averaging은 SE 상을 **연속 매질**로 보고 전위장을 푼다 — **SE-SE 점접촉을 통과하는 수렴저항(Holm/Greenwood)을
  입자별로 풀지 않는다**(넣는 건 AM/SE *면*접촉저항 40 Ω·cm²뿐).  → σ_eff,ion은 **강체-접촉 granular망의 상한** 쪽 →
  우리 Holm 솔버·Bazzoun RNM σ와 **절대 동일시 금지**(우리가 좁힘만큼 *낮다*).  이게 우리가 *더하는* 핵심.
- **σ 검증 1점뿐 + 소재 다름:** flux-σ의 실험 검증은 **Kato 2018 LCO+LGPS+acetylene black 재구성 0.68 vs 0.73
  mS/cm 한 점**.  σ_eff-vs-조성/porosity/바인더 곡선 자체는 *실측이 아니라 모델 출력*(porosity=입력).  검증계가
  **LCO+LGPS**(NCM811+LPSCl 아님) → σ 절대값을 우리 LPSCl계로 *직접 전이 금지*, 추세/방법 검증으로만.
- **stochastic placement (≠ 공정 물리):** 미세구조 생성은 **2019 그대로**(porosity·조성·입경=입력, 랜덤 배치 +
  사후 겹침조정).  추가된 건 σ 솔버뿐 → **porosity 절대값을 우리 압밀 porosity(측정 결과)와 동일시 금지**.
- **재료 파라미터는 들어가나 검증은 1점:** 2019(재료-무관)와 달리 σ_bulk,SE=2.7·ρ_AM/SE=40 등 재료값이 들어가지만,
  그 σ_eff 절대값이 LPSCl계서 맞는지는 *검증 안 됨*(Kato계 1점뿐) → **소재-특이 절대값(σ_grain, porosity floor)을
  이 논문에서 끌어오면 안 됨**.  단 *구조-기하 추세*(CAM↑→σ↓, porosity↑→σ↓, Bruggeman 부적합)는 전이성 높음.
- **PSD: 단봉 + trimodal 1케이스(1:1:2) → Furnas dip *없음*:** multimodal은 **이온 tortuosity 저감**만 보고
  **porosity는 15% 고정** → ★ **porosity-vs-AM% dip을 측정하지 않는다**.  우리 bimodal 12:4:1 + dip 정량(de
  Larrard/McGeary)과 비교할 **dip 데이터 없음**(그들 trimodal은 de Larrard *geometry*를 쓰되 *이온 τ* 관점).
- **바인더 morphology 단순화:** 바인더 = **특정 형상 없는 meniscus**(고-젖음성 가정) → 실제 PTFE *fibril*(Lee
  2025 SEM)·SuperP *응집*(Kim 2025)의 morphology 효과는 *없음*.  배치도 *interfacial(AM 표면)만* → bulk SE-pore
  바인더는 안 봄.  → 우리 CBD morphology 모델(curl+nucleate+shear-draw, `docs/cbd_morphology_roadmap.md`)과 *배치·
  형상*이 다름(σ-블로킹 *물리*는 같되 *어디/어떻게* 막는지 다름).
- **바인더 = σ=0 obstacle만(양의 역학효과 없음):** Bielefeld·우리 voxel 둘 다 바인더를 *전도 차단*으로만 봄 →
  **#271 Hong이 지적한 PTFE의 void-억제(28.7→22.3 vol% densification 도움) 양(+)의 역학효과가 *둘 다* 빠짐**.
- **전류/C-rate = "good case":** charge-transfer·AM 내부 확산·non-ohmic 무시 → "최선 추정"(저자 명시).  ΔU=0.1 V
  제한 → 더 큰 전압강하 허용 시 더 큰 전류.  → C-rate 절대값은 *상한*(이온 ohmic만).
- **2D vs 3D:** 본 논문 *3D*(80×80×140 µm³, 우리 3D와 차원 일치 ✓).  단 resolution 200 nm → 입경 3 µm 하한
  (우리 12:4:1 작은 SE 미해상 / 512 grid 수렴과 같은 한계).

---

## §11. 미니 용어집 (technique glossary)

- **flux-based effective conductivity (EJ-HEAT)** — 미세구조 양단에 전위차를 걸고 정상상태 전류장(∇·(−σ∇φ)=0)을
  voxel에서 풀어 유효 σ 텐서를 얻는 *연속체* 방법.  GeoDict의 EJ-HEAT(Wiegmann & Zemitis 2006)는 정상 열전도
  솔버를 재사용(전기↔열 동형), voxel face서 harmonic averaging + 재료경계 명시 jump.  ★ **점접촉 constriction 없음**
  → granular망의 σ 상한.
- **tortuosity factor τ² (Eq 11)** — τ² = (σ_bulk/σ_eff)·ε = 유효확산이 벌크 대비 얼마나 우회하는지.  σ에서 *역산*.
  = 우리 τ_Laplace,eff (τ²=σ_0·φ/σ_eff) / Minnmann 2021 Eq 4와 同 정의.  Bruggeman τ²=ε^(−1/2)는 ASSB서 4× 과소.
- **constriction resistance** — 점접촉을 통과하는 전류의 수렴저항 R∝1/(σ·r_c)(Greenwood 1966 / Holm 1967).
  ★ Bielefeld 2019가 deferral한 그것; **2020도 *연속체*라 여전히 안 풂**; Bazzoun(RNM)·우리(Kirchhoff/Holm)가 푼다.
- **Bruggeman relation (Eq 18) / 수정 Bruggeman (Eq 19)** — τ²=ε^(−1/2) (구형 입자 이상 균질 가정) / τ²=γ·ε^(−α)
  (2 DoF).  ASSB 양극서 표준식은 4× 과소·수정식 α/γ는 비물리(SE morphology·입경·분포 무시).  = 우리 R_brug 불신 근거.
- **binder bridge / meniscus (SI)** — AM 입자가 가까워지는 곳에 오목 meniscus로 번지는 바인더 배치(Dilation→Removal
  3-step, 고-젖음성).  *interfacial*(AM 표면) 배치 → AM/SE active interface를 우선 차단.  = 우리 voxel σ=0 블로킹의
  *interfacial* 버전(우리는 bulk).
- **V(B):V(AM) (바인더 부피비)** — 바인더 부피를 AM 부피에 묶은 비(0.05/0.10).  → 바인더 wt%가 조성에 따라 변함
  (PVDF 1.78·NBR 1.0 density로 환산).  소량(< 2 wt%)도 유의 부피 → 성능 좌우.
- **active interface area A_spec,a** — 이온-전자 cluster *사이* 경계 면적(= Li 삽입 가능 면적).  바인더↑면 손실
  (고-AM서 −82%).  = 우리 coverage·A_AM-SE 대응(단 *기하* 면적, 소성 접촉 변형 미포함).
- **utilization level θ_ν = V_c/V_ν** — percolating cluster에 속한 component(AM/SE) 부피분율.  2019 계승.  바인더는
  SE utilization을 고-AM서 떨어뜨림(SE 이온경로 차단).  = 우리 f_AM^cc/dead-AM.
- **ε_SE vs ν_SE (Eq 3,11)** — ε_SE = SE의 *전체 부피*(void 포함) 부피분율 = (1−φ)·ν_SE; ν_SE = SE의 *solid 기준*
  부피분율.  τ²·σ_eff 식에 ε_SE(void 포함)를 쓴다.  = 우리 φ_SE(solid)·총 부피분율 구분(2019 g^S/g^V와 同회계).
- **EJ-heat harmonic averaging** — voxel 경계에서 두 상의 전도도를 조화평균(직렬저항)으로 합치고 경계에 명시 jump를
  두는 수치기법(Wiegmann & Zemitis).  연속체 PDE의 이산화 — 점접촉 좁힘과는 다른 층위.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
