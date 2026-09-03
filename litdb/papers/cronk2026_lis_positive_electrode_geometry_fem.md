<!-- digest 표준 양식 (paper-level STANDALONE).  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md.
     ★ = 사용자가 특히 요청한 항목 (MATLAB 확률적 기하 + active surface + TauFactor τ + FEM 3대 가정). -->
# 확률적 voxel 기하 생성(MATLAB) + TauFactor τ + FEM 팽창응력으로 설계한 Li–S 전환형 양극 (LPSCl 촉매전해질) — 11 mAh cm⁻² · 10 MPa anode-free 파우치 — Cronk (Nat. Commun. 2026)

> slug `cronk2026_lis_positive_electrode_geometry_fem` · DOI `10.1038/s41467-026-69750-0` · type `FEM (COMSOL 6.1, 선형탄성+등방 eigenstrain) + 확률적 voxel 기하생성(MATLAB, Duquesnoy) + TauFactor τ + 실험(전기화학·cryo-FIB·XAS·operando 압력)` · PDF `Cronk_2026_NatCommun_LiS_PositiveElectrode_ASSB.pdf` · digested `2026-09-03` · status ✅
>
> ★ **우리 축에서의 자리**: 이 논문은 **DEM 도 MPM 도 없다.**  기하를 *확률적으로 생성*하고 **porosity 를 10 vol% 로 입력 고정**한 뒤 그 위에서 τ(TauFactor)·표면적(voxel)·응력(FEM)을 읽는다.  우리는 **압밀에서 porosity 를 산출**한다 → frame[3]/[5] 의 정면 대비.  동시에 **소재계가 정확히 우리 것**(Li₆PS₅Cl 촉매전해질)이고 **FEM 이 E_SE=22 GPa 를 쓴다** — 우리 DFT(E_VRH 22.06) 와 0.3 % 일치.  ⇒ 경쟁자가 아니라 **"압밀 물리를 빼면 무엇을 물을 수 없게 되는가"의 대조군**이자 **LPSCl 탄성·부피변화·스택압 앵커 공급원**.

---

## 0. 서지 · 실물 확인

| 항목 | 값 |
|---|---|
| 저자 | **Ashley Cronk**¹, Xiaowei Wang², Jin An Sam Oh², So-Yeon Ham¹, Shuang Bai¹, Phillip Ridley², **Mehdi Chouchane**³, Chen-Jui Huang³, Diyi Cheng², Grayson Deysher¹, Hedi Yang³, Baharak Sayahpour¹, Marta Vicencio², Choonghyeon Lee⁴, Dongchan Lee⁴, Min-Sang Song⁴, Jihyun Jang², **Jeong Beom Lee**⁴\*, **Ying Shirley Meng**²,³\* |
| 소속 | ¹UCSD MSE · ²UCSD NanoEngineering · ³**UChicago Pritzker (PME)** · ⁴**LG Energy Solution (LG Science Park, Seoul)** |
| 저널 | **Nature Communications (2026) 17:3298** |
| DOI | **10.1038/s41467-026-69750-0** |
| 접수/게재 | 접수 2025-03-25 · 수리 2026-02-09 |
| 분량 | **본문 15 pp** · **SI 45 pp** (Fig S1–S35, Table S1–S8) + Source Data XLSX(30 시트) |
| 자금 | LG Energy Solution – UCSD Frontier Research Laboratory (FRL) |
| 데이터 | Source Data 동봉 + **figshare 10.6084/m9.figshare.31094524** (Fig 5g/5h 전자별·반복별 응력 데이터) |

> ⚠ **업로드 뷰어의 쪽수(본문 43 · SI 139)는 틀렸다** — PyMuPDF 실측 **본문 15 pp / SI 45 pp**.  이 카드는 실측 쪽수로 적는다.

**계보 (우리 litdb 내 위치)**: Chouchane 은 **Franco/ARTISTIC(Amiens) → Meng 그룹** 계보이고, 우리 카드
`ngandjong2021_dem_calendering_digital_twin` · `duquesnoy2023_ml_multiobjective_manufacturing_optimization` ·
`alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `zhang2026_dryprocess_electrode_architecture_cell_level` 와
같은 줄기다.  `comparison_vs_ours_DEM.md` §🎤 에 "확보 1순위"로 적혀 있던
**Chouchane/…/Cronk/…/Meng, ACS Energy Lett. 2024, 9, 4 (Dry Thick Electrodes, FEM+ML)** 의
**ASSB Li–S 판**이 바로 이 논문의 §Modeling 절이다 (같은 저자·같은 생성기·같은 FEM 골격).

---

## 1. 한 줄 요약
**1-step 고에너지 밀링**으로 S 입자 표면에 **황-풍부 이온전도 계면상 Li₃PS₄₊ₙ** 을 만들어 활물질 이용률을 이론치 근처(1500–1694 mAh g_S⁻¹)로 올리고, **S 입경을 마이크론(0.5–5 µm)으로 맞추면** sub-micron 보다 이온 굴곡도(τ)·계면응력이 낮아 **500 사이클 81 % 유지**(sub-micron 61 %)를 얻으며, S 양극의 **큰 부피팽창(전극 두께 26→32 µm, +23 %)이 음극(Li/Si) 수축을 상쇄**해 75 MPa 기준 스택압 변동을 **1 MPa 미만**으로 눌러 **11 mAh cm⁻² · 25 °C 안정 사이클**과 **10 MPa 저압 Li₂S anode-free 파우치**를 시연한다.  ★ 그 입경 결정을 뒷받침한 것이 **확률적 voxel 기하 생성 + TauFactor τ + COMSOL FEM(선형탄성 + hygroscopic-swelling eigenstrain)** 이다.

---

## 2. 메타 — 소재계 · 조성 · 측정 규약 (★ 값에는 반드시 조건을 붙인다)

| 항목 | 값 | 조건 |
|---|---|---|
| SE | **Li₆PS₅Cl (LPSCl, NEI Corp.)** — 분리막 + 촉매전해질 | 촉매전해질용은 **Ar, 400 rpm, 2 h, 5 mm YSZ 볼, Retsch 유성밀** 로 사전 밀링(micron 화, Fig S2) |
| 대체 SE | β-Li₃PS₄ (LPS, NEI) | 동일 절차 |
| AM | **원소 황 S (99.98 %, Sigma)** 또는 **Li₂S (99.98 %)** | as-received / **400 rpm 10 h(micron)** / **400 rpm 24 h(sub-micron)**, 시료:볼 = **1:10 wt** |
| 도전재 | **아세틸렌 블랙(AB)** 기본 · VGCF · Ketjen black(EC-600JD) 비교 | |
| **양극 조성** | **S(또는 Li₂S) 30 : LPSCl 50 : 탄소 20 wt%** | 명시 없으면 전 전기화학 시험에 이 조성 |
| SE-only 양극 | **LPSCl(또는 LPS) 80 : 탄소 20 wt%** | LPSCl 자체 redox 용량 분리용 |
| 복합체 합성 | **1-step, 500 rpm, 1 h, 시료:볼 = 1:30** (유성밀) | 비교군 = hand-mix / multi-step(S+C 밀링 후 SE hand-mix) |
| 건식 공정 양극 | 복합체 + **PTFE 1 wt%**, 50–60 °C 몰타르 → **60 °C 열롤** → **300–200 µm 필름 ≈ 4.5–6 mAh cm⁻²** | |
| **셀 (펠릿)** | 10 mm Ti 플런저 + PEEK 다이, **분리막 3 ton (375 MPa) 3 min → 450–500 µm**, 양극·µSi 3 ton 5 min, LiIn·Li₂Si **1 ton (125 MPa) 30 s**, 조립 후 **손조임 75 MPa** | 면적 **0.785 cm²** |
| **셀 (파우치)** | Al 박 + 건식 Li₂S 양극 + SE 필름(LPSCl 98 : 아크릴레이트 바인더 2 wt%) + anode-free 층(카본블랙:Ag:PVDF = **69.75:23.25:7.0**, 10 µm SUS 박) → 진공실링 → **WIP 500 MPa @ 80 °C** | 면적 **3.24 cm²**, 2 cm × 2 cm, 분리막 **50 µm** |
| **운전 스택압** | **펠릿 75 MPa** (별도 언급 없으면 전부) · **파우치 등방압 10 MPa** | |
| 온도 | **25 °C ± 1 °C** (펠릿 전부) · **파우치는 60 °C 대류 챔버** | ⚠ 헤드라인 "10 MPa"는 **60 °C 조건**이다 |
| EIS 규약 | Biologic SP-300, **진폭 30 mV**, **7 MHz–100 mHz**, 10 pts/decade, 조립 직후 | σ = L/(R·A), **Ti\|SSE\|Ti** 또는 **Ti\|composite\|Ti** (전 차단) |
| 전압창 | Li₁In‖S **1–3 V vs Li/Li⁺** · Li₂Si‖S **0.7–3 V** · Si‖Li₂S **3.4–1 V** · anode-free‖Li₂S **3.4–1 V** | |
| C-rate 규약 | 설계 용량 = 활물질 × **S 1600 mAh g⁻¹ / Li₂S 1100 mAh g⁻¹** ÷ 셀면적 | |

---

## 3. ★★ 핵심 절 — 기하 모델링 (사용자 질문 ①: "MATLAB 으로 만든 geometry 에서 참고할 게 있나")

### 3.1 원문이 **명시한** 생성 규약 (Methods §"Modeling of sulfur electrode geometries", 본문 p13)

원문 전문(우리 인용):
> *"The electrodes structures were **stochastically generated using the MATLAB codes from Duquesnoy et al.⁶⁷**, with the **S as spherical particles**, and the **carbon additives as aggregates**. A **volume fraction of 10 % was dedicated to pores**, the **S amount ranged from 30 to 60 %**, and the **volume ratio between the LPSCl and carbon additives was kept constant at 5:2**. Three different cases were investigated, Bulk, Micro and Nano, with **S radii ranging respectively from 25 to 50 µm, 0.5 to 5 µm, and 0.25 to 0.5 µm**. To have a representative volume for each condition, the **length of the cubic electrodes was 200 µm for the Bulk, 50 µm for the Micro, and 15 µm for the Nano**. For each set of S size and amount, **3 electrodes were generated** to obtain statistically relevant observables. The evolution of the active surface area was monitored as the specific surface area, i.e., **the ratio between the number of pixels of S in contact with LPSCl and the total number of S pixels**. The tortuosity of the LPSCl phase was investigated using **TauFactor⁶⁸ in MATLAB**, and the reported value is the **average value of the tortuosity of the electrolyte phase in all directions**."*

| 규약 항목 | 원문 값 | 판정 |
|---|---|---|
| 생성기 | ref 67 = **Duquesnoy, Lombardo, Chouchane, Primo, Franco, *J. Power Sources* 480 (2020) 229103** MATLAB 코드 | stated (우리 litdb **미보유** → §12) |
| S 형상 | **구(sphere)** | stated |
| 탄소 형상 | **aggregate(응집체)** | stated — 세부 규칙(응집 크기·수·성장법칙) **미기록** |
| pore | **10 vol% 고정 입력** | stated |
| S 양 | **30 → 60 %** (4점: 30/40/50/60) | ⚠ **단위 미표기**.  Fig 5b/5c 축과 Source Data 헤더는 **"Active Material Mass Fraction (%)"** = 질량, 그런데 pore(10 %)와 LPSCl:C(5:2)는 **부피**.  ⇒ **wt/vol 혼합 지정**이고 변환에 필요한 **ρ_carbon 이 어디에도 없다** |
| LPSCl : 탄소 | **5:2 부피비 고정** | stated |
| 입경(반경) | Bulk **R 25–50 µm** · Micro **R 0.5–5 µm** · Nano **R 0.25–0.5 µm** | stated ("radii" 명시).  ⚠ **분포 형태(균등/로그정규/PSD) 미기록** |
| RVE | 정육면체 변 **200 / 50 / 15 µm** | stated.  ⚠ **RVE 수렴(RVA) 검증 없음** — "To have a representative volume"은 **주장**이지 시연이 아니다 |
| 반복 | 조건당 **3 침대** | stated.  ⚠ **오차막대·표준편차 어디에도 없음** (Fig 5b/5c 는 단일 마커, Source Data 도 평균 1개만) |

### 3.2 ★ 원문이 **적지 않은** 것 (전수 grep: 본문+SI 에 `voxel`·`resolution`·`periodic`·`overlap`·`seed`·`mesh size` **0건**)

| 미기록 항목 | 왜 치명적인가 |
|---|---|
| **voxel(pixel) 크기** | active surface 정의가 **voxel 카운트 비**다 → 이 한 숫자가 Fig 5b 전체를 정한다 (§3.3) |
| **주기경계 여부** | τ 와 표면적 둘 다 벽 효과에 민감.  특히 Bulk 는 변당 입자 **2–3개**뿐(§3.4) |
| **입자 겹침 허용 여부 / 최소간극** | S–S 접촉이 허용되면 LPSCl 대면 비율이 바뀐다 = active surface 의 분모/분자 둘 다 이동 |
| **시드 규약 / 3 침대의 산포** | "3 반복"인데 산포 미보고 → 미크론 vs sub-micron τ 차이가 통계적으로 유의한지 **판정 불가** |
| **FEM 메시 요소 크기 / 요소 수** | Iso2Mesh 로 메시했다고만 함 |
| **탄소상의 역학 물성** | Table S6 에 **S 와 LPSCl 만** 있다 — FEM 에서 탄소를 어느 상으로 처리했는지 **미기록** |
| **Fig 5g 도메인** | 라벨이 **25 µm(Micron) / 10 µm(Sub-micron)** 인데 생성 RVE 는 50 / 15 µm ⇒ **부분체적을 메시한 것으로 보이나 본문 언급 없음** |
| **porosity 측정값** | 실측 porosity **한 번도 없음** (모델은 10 vol% 입력, 실험은 "사이클 후 porosity 증가" 정성 서술뿐).  유일한 숫자 = **Table S8 "SSE 상대밀도 85 %"** = *비에너지 계산 가정치*, 양극 값 아님 |

### 3.3 ★★ active surface area = **격자 의존 · 비수렴 지표** — 우리 CL-25 함정이 여기 그대로 있다

정의: `f = (LPSCl 과 접한 S 픽셀 수) / (전체 S 픽셀 수)`.

`derived(ours)` — 반지름 R 의 구를 voxel h 로 그리면 총 셀 ≈ (4/3)πR³/h³, 껍질 셀 ≈ 4πR²·h/h³ 이므로
**껍질분율 f_shell ≈ 3h/R**.  그들 지표는 그 껍질 중 LPSCl 대면분만 세므로 `f ≤ 3h/R`.

1. **f 는 h 에 비례한다 ⇒ 격자를 조이면 0 으로 간다.**  물리량이 아니라 *격자 단위로 잰 비표면적*이다.
   같은 h 안에서만 비교 가능하고, **RVE 변이 200/50/15 µm 로 13× 다른 세 케이스**를 한 그림에 겹치려면
   h 를 어떻게 잡았는지가 결정적인데 — **미기록**.
2. **sub-micron 은 이미 해상도 바닥**: 보고값 **87.6 %** (30 wt%) 를 `f ≤ 3h/R` 에 넣으면
   **R/h ≤ 3.4** — 즉 sub-micron S 구는 **반지름 3 셀 이하**로 그려져 있다.  (모든 껍질 셀이 LPSCl 을
   본다는 최선 가정에서의 **상한**이므로 실제는 더 나쁘다.)
3. **★ 지표가 진짜 대비를 ~7배 압축한다.**  `derived(ours)`, PSD 를 반경 균등분포로 가정하고
   Sauter형 R₃₂ = 3(b⁴−a⁴)/(4(b³−a³)) 를 쓰면
   | 케이스 | R 범위 | **R₃₂** | 물리 비표면적 3/R₃₂ [µm⁻¹] | 상대 |
   |---|---|---|---|---|
   | Bulk | 25–50 | **40.18 µm** | 0.0747 | **1** |
   | Micron | 0.5–5 | **3.753 µm** | 0.799 | **10.7** |
   | Sub-micron | 0.25–0.5 | **0.4018 µm** | 7.466 | **100** |
   그런데 **보고된 지표(30 wt%)는 6.215 : 20.868 : 87.629 = 1 : 3.36 : 14.1**.
   ⇒ **참 대비 100:1 이 14:1 로 눌렸다 (압축계수 ≈ 7.1×)**.  원인은 (a) h 가 RVE 변에 따라 커지고
   (b) sub-micron 이 포화(87.6 % → 100 % 천장)했기 때문.
   ⇒ **Fig 5b 의 순서(nano > micron > bulk)는 진짜지만, 그 세기(gap)는 격자의 산물이다.**
4. **격자 무관 대안이 이미 그들 손 안에 있었다** — TauFactor 는 τ 뿐 아니라 **SA [µm⁻¹]** 를 출력한다
   (우리 카드 `taufactor_tortuosity_factor_tomography_tool` §3·§4(C)).  τ 에는 TauFactor 를 쓰고
   표면적은 자체 voxel 비로 잰 것이 이 절의 핵심 결함이다.  ⚠ 단 TauFactor 자신도 voxel 면을
   그대로 세므로 SA 를 **과대추정**한다(단일-voxel 구 ×2, 다-voxel 구 최소 ×1.5) — 그래도
   **차원이 µm⁻¹ 라 격자 간 비교가 가능**하다는 점이 결정적으로 다르다.

> ⇒ **우리 CL-25 와 같은 종류의 함정**: SDCP 표현부피가 vox 0.4→0.15 에서 참값의 4.311 → 0.238 배로
> **18.1배** 흔들렸고, 그 때문에 이득 수치 계열이 통째로 철회됐다.  차이는 **우리는 그것을 측정해서
> 알았고, 이 논문은 격자 크기를 적지 않아 아무도 확인할 수 없다**는 것.

### 3.4 ★ RVE 대표성 — Bulk 케이스는 **입자 8개 셀**이다

`derived(ours)` (φ_S ≈ 0.24–0.30, ⟨V⟩ = (4/3)π⟨R³⟩, 반경 균등분포):

| 케이스 | RVE 변 | 변당 입자 **지름** 개수 | **박스 안 S 입자 수(추정)** |
|---|---|---|---|
| Bulk | 200 µm | **≈ 2.0–2.5** | **≈ 8–10** |
| Micron | 50 µm | ≈ 6.7 | ≈ 200 |
| Sub-micron | 15 µm | ≈ 18.7 | ≈ 3,300 |

Fig 5a 의 Bulk 렌더에 보이는 큰 노란 구가 **4–6개**인 것과 정합한다.
⇒ **세 "RVE" 의 입자 수가 400배 다르다.**  Bulk 의 τ = 2.907 은 입자 ~8개짜리 셀에서 나온 값이고,
3 반복의 산포는 보고되지 않았다.  TauFactor 의 **RVA(representative volume analysis)** 기능이
바로 이 검사를 위해 존재하는데(우리 TauFactor 카드 §4(C)) 실행 흔적이 없다.

### 3.5 ★★ 비단조 τ 결과 — 원문 문장과 실제 데이터

원문: *"**Surprisingly, the micron sulfur electrode exhibits the lowest ionic transport tortuosity**, with all cases obtaining similar results until higher AM mass fractions (Fig. 5c)."*

**Source Data XLSX 에서 뽑은 정확값** (디지타이즈 아님 — 저자 제공 수치):

| AM (%) | **Sub-micron τ** | **Micron τ** | **Bulk τ** | sub/micron | bulk/micron |
|---|---|---|---|---|---|
| 30 | **3.3644** | **1.9800** | **2.9068** | 1.70 | 1.47 |
| 40 | **4.3554** | **2.2159** | **3.1836** | 1.97 | 1.44 |
| 50 | **5.9602** | **2.5742** | **3.9584** | 2.32 | 1.54 |
| 60 | **15.3269** | **3.0857** | **5.0823** | **4.97** | 1.65 |
| Δ(50→60) | **+9.367 (×2.57)** | +0.512 (×1.20) | +1.124 (×1.28) | | |

**판정 (사용자 질문 ④에 대한 답)**
- **곡선은 어디서도 교차하지 않는다.**  30–60 wt% 전 구간에서 **micron < bulk < sub-micron** 순서가
  유지된다.  "비단조"는 *곡선 교차*가 아니라 **입경에 대한 τ 의 비단조(중간 크기가 최소)** 다.
- 원문의 *"all cases obtaining similar results until higher AM mass fractions"* 는 **느슨하다** —
  30 wt% 에서 이미 **1.70배(sub/micron)·1.47배(bulk/micron)** 벌어져 있다.
- **50 wt% 이후 급변하는 것은 sub-micron 하나뿐**이다: 5.96 → 15.33 = **한 스텝에 ×2.57**
  (micron ×1.20, bulk ×1.28).  전형적인 **LPSCl 상 percolation 문턱 접근** 시그니처다.
  `derived(ours)` ρ_S=2.0·ρ_SE=1.6 (Table S6) + ρ_C≈2.0 g cm⁻³ **가정**으로 wt→vol 변환하면
  LPSCl 부피분율이 **30 wt%: 47.0 vol% → 60 wt%: 28.1 vol%** 로 떨어진다 (S 24.2 → 50.6 vol%).
  ⚠ ρ_C 는 논문 미기재 → 이 변환은 **우리 가정치**다.
- ★★ **"micron 이 최저"라는 결과가 왜 의심스러운가 (우리 관점의 핵심 비판)**:
  **고정 부피분율에서 구형 장애물의 τ 는 스케일 불변**이다 — 기하에 고유 길이가 없으므로
  입경만 바꾸고 부피분율을 고정하면 τ 는 원리적으로 변하지 않아야 한다.  세 케이스에서
  스케일 불변을 깨는 요인은 **딱 셋**이다:
  ① **RVE/입경 비**(2.0 vs 6.7 vs 18.7 — 400배 입자수 차),
  ② **voxel/입경 비**(미기록, §3.3 에서 sub-micron 은 R/h ≲ 3.4 로 바닥),
  ③ **PSD 폭**(Bulk 2× · **Micron 10×** · Nano 2× — micron 만 광대역이라 패킹이 다르다).
  ③ 은 **진짜 물리**(광대역 PSD → 충전 개선 → 매트릭스 연결성 향상)이고 우리 Furnas-dip 축과
  같은 계열이다.  그러나 논문은 ①②를 통제하지 않았으므로 **"micron 최저"가 물리인지
  해상도·유한크기 인공물인지 분리되지 않는다.**
  ⇒ 우리는 이 축에 **정량 규칙**을 갖고 있다(`d_h/dx ≳ 3.5`, CLAUDE.md 2026-08-07): 좁은 채널이
  2.65셀이면 격자 정밀화에 **+23.8 %**, 7.71셀이면 **+4.0 %** 로 6배 차이가 났다.  같은 규율을
  적용하면 이 논문 세 케이스는 **서로 다른 신뢰도 등급**에 놓인다.

### 3.6 ★ Fig 5b 원본 수치 (Source Data, 디지타이즈 아님)

| AM (%) | **Sub-micron 표면(%)** | **Micron 표면(%)** | **Bulk 표면(%)** |
|---|---|---|---|
| 30 | **87.629** | **20.868** | **6.215** |
| 40 | **74.927** | **18.618** | **6.090** |
| 50 | **59.837** | **16.834** | **5.313** |
| 60 | **42.518** | **14.838** | **4.915** |
| 30→60 상대변화 | **−51.5 %** | −28.9 % | −20.9 % |

⚠ **Source Data 헤더 오기**: Fig 5b·5c 세 계열이 **전부 "Sub-Micron S"** 로 라벨돼 있다(복사 실수).
Fig 5d 는 Bulk/Micron/Sub-Micron 으로 올바르다.  실제 그림(범례 색)과 대조해 **열 순서 =
(Sub-micron, Micron, Bulk)** 임을 확인했다 — 위 표는 그 확인 후의 배정이다.

---

## 4. ★★ FEM — 3대 가정과 그 사정거리 (사용자 질문 ⑤)

### 4.1 원문 (Methods §"Finite elements method (FEM) simulations", p13)

> *"The electrodes were meshed using the open-access toolbox **Iso2Mesh**⁶⁹ and later imported into **COMSOL Multiphysics 6.1**. There, using the **Solids Mechanics module**, the set of parameters and equations in **Tables S3 and S4** were set. In the model, the electrode was assumed to be **fully compact (no porosity)** and the S particles were **uniformly lithiated** throughout the simulation, leading to a volume expansion made possible with the **"Hygroscopic Swelling" node** which normally accounts for the volume expansion of solids due to the amount of water. During the simulation, the **external boundaries of the electrode were fixed**. To determine the analog hygroscopic coefficient of each type of S particles, a **2-D simulation** consisting of the exact same model for a **single S particle** was performed. The hygroscopic coefficient was deemed adequate when the S particle would reach the desired volumetric expansion (controlled here by its radius) at full lithiation. The cases of **sub-micro and micron S** were investigated for an **AM content of 30 wt%** where **three electrodes** were used for each case."*

⚠ **표 번호 오기**: Methods 는 "Tables **S3/S4**" 라 하지만 실제 FEM 파라미터·방정식은 **Table S6/S7**
(S3 = 용량·이용률 표, S4 = TGA 표).  본문 결과 절(p9)은 **S6/S7** 로 올바르게 적는다.

### 4.2 Table S6 — 파라미터 **전수** (SI p43 실물 확인)

| Name | Symbol | Value |
|---|---|---|
| Young Modulus of S | E_S | **17.8 GPa** |
| **Young Modulus of LPSCl** | **E_SE** | **22 GPa** |
| Poisson ratio of S | ν_S | **0.32** |
| **Poisson ratio of LPSCl** | **ν_SE** | **0.3** |
| Density of S | ρ_S | **2 g cm⁻³** |
| Density of LPSCl | ρ_SE | **1.6 g cm⁻³** |
| Hygroscopic coefficient of S_micro | β_H | **22.5 × 10⁻³ m³ kg⁻¹** |
| Hygroscopic coefficient of S_sub-micro | β_H | **24 × 10⁻³ m³ kg⁻¹** |
| Molar mass of Li | M_m | **7 × 10⁻³ kg mol⁻¹** |

★ **표에 없는 것 = 물리적으로 결정적**: **항복응력 σ_y 없음 · 경화 없음 · 소성 없음 · 파괴/CZM 없음 ·
탄소상 물성 없음 · C_Li(리튬 농도) 값 없음 · 마찰/접촉 없음**.

### 4.3 Table S7 — 방정식 **전수** (SI p44 실물 확인)

| Name | Symbol |
|---|---|
| On external boundaries | **u = 0** |
| In the electrode | **ρ ∂²u/∂²t = ∇·S + F_v** · **S = C : ε_el** · **C = C(E, ν)** · **ε_el = ε − ε_inel** · **ε_inel = ε_HS** · **ε = ½[(∇u)ᵀ + ∇u]** |
| Hygroscopic swelling in S particles | **ε_HS = β_H · M_m · C_Li** |
| Initial values | u = 0 · ∂u/∂t = 0 |

⇒ **완전한 선형탄성 + 등방 eigenstrain(비탄성 변형률) + 소변형 운동학**.  탄성 계수 C 는 (E, ν) 만의
함수이고, 소성 유동법칙·항복면·연화·파괴가 **하나도 없다**.

### 4.4 ⓐ *"fully compact (no porosity)"* — **역학이 수송과 다른 기하 위에서 돌았다** (사용자 읽기 확인)

**사용자의 읽기가 맞다.**  기하 생성기는 **pore 10 vol% 를 입력**으로 넣고 τ·표면적은 그 기하에서
쟀는데, FEM 은 *"the electrode was assumed to be **fully compact (no porosity)**"* 라고 명시한다.
어느 상이 그 10 % 를 흡수했는지(LPSCl 로 채웠는지, 메시에서 제거했는지)는 **미기록**.

**의미 (세 겹의 상한)**
1. **공극이 없으면 팽창한 S 가 흘러들 자리가 없다.**  실제 계에는 10 vol% 공극이 있고,
   저자들 자신의 cryo-FIB 는 사이클 후 *"an increase in porosity"* 로 두께가 유지된다고 적는다.
2. **외부 경계 u = 0** 이면 전극이 **거시적으로 부풀 수도 없다**.  그런데 같은 논문의 Fig 6a 는
   **26 → 32 µm (+23 %)** 팽창을 측정했다.  모델은 그 완화 경로를 원천 봉쇄한다.
3. **소성이 없다.**  같은 논문 본문(p9–10)은 *"the resulting stress on the SSE matrix causes it to
   **plastically deform** to accommodate particle expansion"* 이라고 결론짓는다 — **관측은 소성인데
   모델은 탄성**이다.
⇒ 보고된 응력은 **세 겹으로 부풀려진 상한**이다.  ★ 이것은 흠결이지만 **정직하게 상한으로 읽으면
쓸모가 있다**: "소성·공극·거시팽창을 전부 막았을 때 필요한 응력" = **완화 기구의 필요성 증명**.

`derived(ours)` 규모 감각: 30 wt% S 전극의 완전 리튬화 부피변화는 **25.84 %** (Fig S33 정확값).
그것을 강체 상자 안에 강제로 밀어넣으면 K_SE = 18.33 GPa(§4.6) 기준 정수압 ≈ **4.7 GPa**.
보고된 응력(평균 2.4 · 꼬리 8 GPa)과 같은 자릿수다 ⇒ **그 숫자는 미세구조가 아니라
경계조건이 정한다**.

### 4.5 ⓑ *"uniformly lithiated"* — 반응분포 없음
S 입자 전체가 동시·균일하게 리튬화한다.  즉 **전기화학 ↔ 역학이 단방향(용량 → 부피변화)** 으로만
연결되고, 반응 분포·SOC 구배·확산 시간척도가 전혀 없다.  ⇒ Fig 5g/5h 는 **1차 리튬화 종점의
스냅샷 한 장**이고, 저자들도 *"These simulations only capture stress after the 1st lithiation"* 이라 적는다.
⚠ 우리 STEP4(비선형 BV + 구형확산 시간전개)가 하는 일이 통째로 빠져 있다.

### 4.6 ⓒ "Hygroscopic Swelling" 트릭 — **우리가 이식할 값이 있는가?** (판정)

**무엇인가**: COMSOL 의 흡습팽창 노드는 수분 농도에 비례하는 **등방 eigenstrain**
`ε_HS = β_H · M_m · C_Li · I` 를 넣는다.  물 대신 Li 를 넣어 리튬화 팽창의 아날로그로 쓴 것이다
(= 열팽창 노드로 하는 것과 수학적으로 동일).  β_H 는 **2D 단일입자 런에서 목표 부피팽창이 나오도록
역보정**했다.

**판정 — 세 줄**
1. **트릭 자체는 새롭지 않다.**  등방 eigenstrain 은 열팽창/화학팽창의 표준 구현이고, 우리 MPM 에
   넣으려면 변형구배를 `F = F_el · (1+ε*)I` 로 곱분해하면 끝이다 (한 줄).
   ⇒ **구현을 배울 것은 없다.**
2. **★ β_H 값은 이식 불가능하다.**  ε_HS = β_H·M_m·C_Li 인데 **C_Li 가 논문 어디에도 없다**.
   β_H = 22.5·10⁻³ m³ kg⁻¹ 만으로는 변형률이 결정되지 않는다.  ⇒ 이식할 수 있는 것은
   **목표 부피변형률**(micron **71 %**, sub-micron **75 %**, Fig S32) 뿐이다.
3. **★★ 등방 eigenstrain 은 우리 MPM 이 하는 일을 못 한다.**  eigenstrain 은 **체적** 변형을 부과할 뿐
   **편차(소성) 유동**이 없다 — 즉 SE 가 공극으로 *흘러들어가* 모양을 바꾸는 물리가 없다.
   우리 J2 MPM 은 정확히 그것을 한다(frame[1]).  ⇒ **우리가 가져올 것은 "S 팽창을 eigenstrain
   으로 건다"는 소스 항 하나**이고, 그 위의 완화는 **우리 소성이 담당**한다.
   ⇒ **실행 가능한 백로그 항목**: `mpm3d_compaction.py` 에 `--am-eigenstrain <ΔV>` 를 추가해
   AM(우리 경우 NMC 또는 S) 상에 등방 체적 eigenstrain 을 걸고 SE 는 J2 로 흐르게 하면,
   **"탄성 상한(그들) vs 소성 완화(우리)"** 를 같은 기하에서 정량 비교할 수 있다.
   그것이 이 논문에서 우리가 가져올 **유일하고 확실한 이식물**이다.

### 4.7 ⓓ 외부 경계 고정 + LPSCl 탄성상수 대조 ★

**BC**: `u = 0` on all external boundaries — 완전 구속.  (스택압 BC 도, 자유팽창도, 주기경계도 아니다.)

**LPSCl 탄성상수 — 우리 DFT 와 대조** `derived(ours)`

| 출처 | E [GPa] | ν | **G [GPa]** | **K / B₀ [GPa]** |
|---|---|---|---|---|
| **Cronk FEM (Table S6)** | **22** | **0.3** | **8.462** (=E/2(1+ν)) | **18.333** (=E/3(1−2ν)) |
| **Deng 2016 (그들이 인용한 ref 57)** — 우리 카드 `deng2016_elastic_superionic_electrolytes_dft` | **22.1** | **0.37** | **8.1** | **28.7** |
| **우리 DFT (relaxed-ion)** | **22.06** | **0.360** | **8.11** | **B₀ 26.23** |
| Bazzoun 2026 DEM (우리 카드) | 22.1 | 0.37 | — | — |

- **E 는 3자 일치**: 22 / 22.1 / 22.06 — **0.3 % 이내**.  ⇒ 이 값은 이제 **문헌 합의**로 봐도 된다.
- **G 도 근사 일치**: 8.462 vs 8.1 vs 8.11 (**+4.3~4.5 %**).
- **★★ K 만 크게 어긋난다**: **18.33 vs 28.7 vs 26.23 = −30~−36 %**.
  원인은 **ν = 0.3 선택**이다 — 그들이 전단계수 근거로 인용한 **바로 그 Deng 2016 이 ν = 0.37** 을 준다.
  ⇒ **자기 참조와 불일치**.
- ⚠ **이것은 우리 자신이 CLAUDE.md 에 적어 둔 함정과 같은 것**이다: SDCP Methods SI 의
  *"ν ≈ 0.3 (K ≈ 20, μ ≈ 9.2)"* 에서 K 20 이 우리 DFT B₀ 26.23 과 **24 % 어긋난다**고 기록해 뒀다.
  ⇒ **같은 미끄러짐이 Nature Communications 에도 있다** = 우리 규율(물성 행은 DFT 쌍 (B₀, ν, μ) 으로,
  ν=0.3 은 DEM 설정에만)의 외부 근거.
- ★ **다만 이 논문 결과에 미치는 영향은 제한적이다** `derived(ours)`: 등방 팽창 개재물 문제에서
  기지의 von Mises 장은 **전단계수가 지배**한다(§4.8 Eshelby).  ν 를 0.30 → 0.37 로 고치면
  계면 σ_vM 이 **+12 %** 정도 오를 뿐이다.  ⇒ **K 오차는 정수압 항에 남고 von Mises 헤드라인은
  크게 안 흔들린다** — 공정하게 적어 둔다.

---

## 5. ★ Fig 5g/5h — von Mises 응력 결과와 그 해석 (사용자 질문 ⑥)

### 5.1 보고된 것
- **Fig 5g**: 컬러바 **0 → 5 × 10⁹ N m⁻² (0–5 GPa)**.  Micron S 박스 라벨 **25 µm**, Sub-micron **10 µm**
  (⚠ 생성 RVE 50/15 µm 와 불일치, §3.2).  응력은 **S 입자 표면에 껍질처럼 집중**(노란 링)하고
  벌크 SE 는 어둡다(≈0).  Micron 렌더는 큰 구 5–6개, Sub-micron 은 작은 구 수십 개.
- **Fig 5h**: 확률밀도 히스토그램, x = 0–8 × 10⁹ Pa.  **이봉(bimodal)**:
  0 근처 큰 봉(0.03 축에서 잘림) + **≈ 4.1–4.3 GPa 의 두 번째 봉**.
  두 번째 봉의 높이: **Sub-micron ≈ 0.0135 vs Micron ≈ 0.0065 (≈2배)**.
  꼬리는 양쪽 다 **8 GPa** 까지.
- **그림 안 주석 (stated)**: **σ̄_Sub-micro = 2.42 GPa · σ̄_Micro = 2.40 GPa**.
- 본문: *"stresses **beyond 5 GPa** were predicted"* (양 케이스) · *"most of the SSE matrix does not
  experience stress since only 30 wt% of sulfur is used"* · sub-micron 이 *"a higher frequency of stress"*.
- 본문 p10: *"The plastic deformation of the SSE matrix is not surprising, as the simulated stresses
  estimated above is **near the shear modulus of LPSCl**⁵⁷"* (ref 57 = Deng 2016).

### 5.2 ★★ 우리 판정 — 세 가지

**(i) 평균은 사실상 null 결과다.**  2.42 vs 2.40 GPa = **차이 0.8 %**, 오차막대 없음(3 침대인데 SD 미보고).
prescribed 팽창 자체가 **75 % vs 71 % = 5 % 차**인데 평균 차는 0.8 % 다.
⇒ **"sub-micron 이 더 큰 응력을 받는다"는 주장은 *평균*으로는 성립하지 않고, *분포 모양*
(≈4 GPa 모드의 무게)으로만 성립한다.**  논문은 이 구분을 하지 않는다.

**(ii) "near the shear modulus" 는 꼬리에만 해당한다.** `derived(ours)`
Deng 2016 의 G(LPSCl) = **8.1 GPa**.  평균 2.4 GPa 는 **G 의 30 %** 다.  히스토그램 꼬리(5–8 GPa)만
G 에 근접한다.  ⇒ *"소성이 놀랍지 않다"* 의 근거는 **전체가 아니라 계면 껍질**이다.
(그래도 결론은 살아남는다 — 소성은 계면에서 시작하면 되기 때문.)

**(iii) ★★★ 응력 크기는 미세구조가 아니라 (E, ν, ΔV) 가 정한다 — 그리고 이 모델에는 길이척도가 없다.**
`derived(ours)` 등방 eigenstrain ε\* 를 가진 구형 개재물이 같은 물성의 무한 기지에 있을 때
(Eshelby, 정확해) **계면에서의 von Mises = E · ε\* / (1 − ν)**, 그리고 이 값은 **입자 반경 a 에 무관**이다.

| 케이스 | 부과 ΔV (Fig S32) | ε\* = (1+ΔV)^{1/3}−1 | **σ_vM(계면) = Eε\*/(1−ν)** |
|---|---|---|---|
| Micron | **71 %** | 0.1957 | **6.15 GPa** |
| Sub-micron | **75 %** | 0.2051 | **6.44 GPa** |
| (소변형 규약 ε\*=ΔV/3 이면) | | 0.2367 / 0.2500 | 7.44 / 7.86 GPa |

⇒ 보고된 *"beyond 5 GPa"* 와 히스토그램 꼬리 8 GPa 를 **해석적으로 재현**한다.
⇒ **선형탄성 + 부과 eigenstrain 조합에는 고유 길이척도가 없다**(σ_y 도, 표면에너지도, K_IC 도,
gradient 항도 없다).  따라서 **입경 자체가 응력을 바꿀 수 없고**, micron ↔ sub-micron 차이는
전적으로 **"S 표면 근방에 SE 부피가 얼마나 있는가"** = **비표면적**에서 온다.
⇒ ★ **Fig 5h 는 Fig 5b 를 응력 단위로 다시 그린 것에 가깝다.**  FEM 이 새 물리를 더한 것이 아니라
기하 지표를 재표현한 것 — 논문은 이를 명시하지 않는다.
⇒ ★★ **진짜 크기효과를 얻으려면 길이척도를 넣어야 한다**: 항복응력(소성역 크기/R), 파괴길이
(K_IC/σ)², cohesive law.  **그것이 정확히 우리 MPM(J2) + A10 CZM(Bucci G_c) 이 소유한 반쪽**이다.

**우리 A10 축과의 접점**: `docs/a10_cycle_chemomech_design.md` 의 Bucci **G_c = 2.8 ± 1.8 J m⁻²**,
Fan 2026 **K_IC 0.2–0.4 MPa·m^½** (평면변형 환산 G_c = K_IC²(1−ν²)/E, 중앙값·E 24 → 3.24 J m⁻²).
계면 σ ≈ 6 GPa 이면 **임계 결함 크기 a_c ≈ K_IC²/(π σ²)** `derived(ours)`:
K_IC = 0.3 MPa·m^½, σ = 6 GPa → a_c ≈ **0.8 nm**.  σ = 2.4 GPa → **5 nm**.
⇒ **이 응력 수준에서는 원자 수준의 결함만 있어도 균열이 간다** = 탄성 해가 물리적으로 유지될 수 없다는
독립 증거.  ⇒ 실제 계는 **소성 또는 파괴로 즉시 완화**되고, 그것이 저자들 자신의 cryo-FIB 관측
(SE 소성변형 · Li₂S 컬럼형 균열)과 일치한다.

---

## 6. 실험 결과 — 절별 전수 (수치는 전부 조건과 함께)

### 6.1 계면상 형성 (Fig 2, p3–4)
- **1st 사이클 (Li-In 반쪽셀, 80 mA g⁻¹ = C/20, 75 MPa, 25 °C)**
  | 합성법 | 결과 |
  |---|---|
  | hand-mix | 낮은 이용률 |
  | multi-step (S+C 밀링 → SE hand-mix) | 낮은 이용률, **CE 17 %** |
  | **1-step (500 rpm 1 h)** | 방전 **≈1500 mAh g_S⁻¹** (이론 1675 의 90 %), **CE 129 %** (>100 = SE 가 용량 기여) |
- **XRD (Fig 2b, S4a)**: 1-step 만 비정질화; 탄소 없이 밀링 시 S·LPSCl 특성피크 **FWHM 증가**.
- **TGA (Fig S5)**: 350 °C 승화 기준으로 **30 wt% 중 6.5 wt% 의 S 가 미회수** → 결합환경 변화.
  ⇒ **23.5 wt% 는 미반응 원소 S** 로 잔존.
- **Raman (Fig 2c, S4b)**: S–S 굽힘 **152 cm⁻¹ 적색이동**(E₂ 대칭굽힘) + PS₄³⁻ 대칭신축 **425 cm⁻¹
  강도·파수 감소** ⇒ **가교 S–S 결합 = Li₃PS₄₊ₙ (황-풍부 티오포스페이트)**.
- **XANES S K-edge (Fig 2d)**: 원소 S **2473.6 eV** · LPSCl **2472.4 eV** · **pre-edge 2470.1 eV**
  (S 산화수 감소 = 장쇄 폴리설파이드형 사슬 → Li₃PS₄₊ₙ 의 S 사슬).
- **cryo-TEM / HAADF-STEM + EDS (Fig S6, S7, Table S1)**: 입자 가장자리에만 Cl 신호,
  **가장자리 50 nm 안쪽부터 Cl 소멸·S 만** → 벌크는 S, 표면이 황-풍부상.
  중심부 S 원자분율이 LPSCl 화학량론의 **2배**로 안정화.
  (Table S1 입자1: S 68.68 at% / P 7.82 / Cl 6.85 / O 16.65; 입자2: S 65.79 / P 7.62 / Cl 6.71 / O 19.88)
- ★ **σ 앵커 (조건 포함)**
  | 시료 | σ | 조건 |
  |---|---|---|
  | **LPSCl 촉매전해질** | **2 mS cm⁻¹** | Fig S8a, Ti\|composite\|Ti, **75 MPa, 25 °C** |
  | **LPS (β-Li₃PS₄)** | **0.04 mS cm⁻¹** | 동일 |
  | LPSCl 단독, 500 rpm **1 h → 10 h** | **1.3 × 10⁻³ → 4 × 10⁻⁵ S cm⁻¹** (**32배 붕괴**) | Fig S4f; Li₂S·LPS 절연상 생성 |
  | **S + LPSCl 복합(탄소 無)**, 500 rpm | **6 × 10⁻⁶ → 2 × 10⁻⁵ S cm⁻¹ (1 h 후)** | Fig S4c; ⚠ **S:LPSCl 비 미기록** |
  ⇒ ★ **복합체 σ 는 촉매전해질의 1/100** (0.02 vs 2 mS cm⁻¹).  밀링은 **1 h 가 최적** —
  계면반응은 완료하되 SE 를 안 죽이는 창.

### 6.2 Li₂S 양극 (Fig S9–S11)
- 1-step: **723 mAh g⁻¹, CE 99.3 %** (Li₀.₅In 대극).  hand-mix 는 **사이클 불가**.
- ⚠ **Li₂S 는 LPSCl 을 LPS 로 환원**시킨다: XRD 피크 소멸, PS₄³⁻ 신축 **425 → 418 cm⁻¹**.
  그럼에도 안정 사이클 → 분해산물이 redox-활성.

### 6.3 LPSCl redox 정량 (Fig 3, Table S2/S3)
- **LPSCl+탄소(80:20) 반쪽셀, S 전압창**: 환원 **115 mAh g⁻¹** / 산화 **355 mAh g⁻¹** (Fig 3a).
- **1.6 mAh cm⁻² 셀 (총 복합체 2.5 mg)**: 미반응 S 23.5 wt% → **1 mAh** 기여 = 방전의 **83 %**.
- **dQ/dV 4구역** (10/20/30 wt% S, 각 60/70/80 mA g_S⁻¹): I = S 환원 / II = 1.3 V 부터
  Li₃PS₄₊ₙ 환원(**방전 용량의 7.5 %**) / 1.15 V 부터 LPSCl 환원(**9.2 %**) / III = Li₂S 산화 /
  IV = 2.7 V 부터 SE 산화(가역).
- 충전 후 기여: 반응 S **10 %** · LPSCl **27.5 %**.  반응 S 의 비용량 **553 mAh g⁻¹** (≈Li₃PS₄₊₃).
- **Table S2 전수** (2.5 mg 복합체, 30:50:20 wt%) — 세 가지 추정 경로를 나란히 놓은 표
  | 경로 | | 미반응 S | Li₃PS₄₊ₙ 의 반응 S | LPSCl | 합계 (mAh) |
  |---|---|---|---|---|---|
  | 질량 기반 기대 | 방전 | 1 | 0.25 | 0.13 | **1.38** |
  | | 충전 | 1 | 0.25 | 0.44 | **1.70** |
  | 전기화학 기반 | 방전 | 1 | **0.20 (합산)** | | **1.20** |
  | | 충전 | 1 | 0.16 | 0.44 | **1.60** |
  | dQ/dV 전위 기반 | 방전 | 1 | 0.09 | 0.11 | **1.20** |
  | | 충전 | 1 | 0.16 | 0.44 | **1.60** |
  | **기여율 (%)** | 방전 | **83.3** | **7.5** | **9.2** | (1.20) |
  | | 충전 | **62.1** | **10** | **27.5** | (1.60) |
  ⇒ ★ **충전 용량의 37.5 %가 SE 계열**(반응 S 10 + LPSCl 27.5)이다 — CE 129 % 의 출처.
- **이용률 (Table S3, Fig 3c 셀)**: S 10 wt% → **92 %** · 22 wt% → **84.3 %** · 30 wt% → **84 %**.
- 제안 반응식 (본문): `Li₆PS₅Cl + Li⁺/e⁻ → Li₂S + Li₄PS₄ + LiCl` (Q_red ≈ 100 mAh g⁻¹) ·
  `Li₂S + Li₄PS₄ ⇌ Li₂.₅PS₄ + S + 3.5 Li⁺/e⁻` (Q_ox ≈ Q_rev ≈ 350 mAh g⁻¹).
- **Li₂S 산화 활성화 전위 = 2.4 V** — 촉매 없이 달성 (LPSCl 자체 산화가 2.3 V 부터).

### 6.4 가역성 (Fig 4)
- **in-situ EIS**: 방전 후 임피던스 **+85.2 Ω** (Li₂S 전하이동), 충전 후 **pristine 근처 복귀** (Fig S15).
- **XRD (7.6 mg cm⁻² 고로딩)**: 방전 시 나노결정 **Li₂S** 검출, 충전 시 Li₂S 소멸 + **10.5° 2θ 의 S**
  (Mo Kα λ=0.7107 Å, 5–50° 2θ) + 1st 사이클 후 **15° 2θ 신규 피크 = LPS**.
- **TGA (Table S4, 10 mAh cm⁻² 시료)**
  | 상태 | 전극질량 | S 질량 | TGA 손실 | 검출 S | 반응분 |
  |---|---|---|---|---|---|
  | Pristine | 18.7 mg | 5.61 | 23.7 % | 4.43 | **1.2 mg / 20 % 반응** |
  | Discharged | 19.8 | 5.94 | 2.1 % | 0.41 | **5.53 mg / 93.1 %** |
  | Charged | 14.1 | 4.23 | 19.7 % | 2.77 | **1.5 mg / 34 %** |
- **XANES LCF (Fig 4d–f, Table S5)**: LPSCl 계 — 초기 방전에 **LPSCl 절반이 LPS 로 분해**,
  충전 후 복합체의 **9.7 wt% 가 S**, **22 wt% LPS 잔존**.  S 계 — 방전 후 **Li₂S 20.2 wt%**,
  충전 후 Li₂S 미검출 + **S 32 wt%**.  ⚠ 저자 자신이 SI 에 **TFY 자기흡수·탐침깊이 500 nm–수 µm·
  빔 0.25×0.16 mm = 전극면적의 0.06 %** 한계를 명시.

### 6.5 입경 효과 — 전기화학 (Fig 5d–f, S28–S31)
- **1st 형성 (C/20 = 80 mA g⁻¹, 1 mg_S cm⁻², 75 MPa, 25 °C)**:
  **Sub-micron 1694 > Micron 1615 > Bulk 1500 mAh g_S⁻¹** (sub-micron 은 이론치 초과 = SE redox).
- 2nd 형성에서 분극 **577 → 452 mV** 감소.
- **율 특성 (Fig S28b, 0.1C→1C; 1C = 1.6 A g_S⁻¹ = 1.6 mA cm⁻²)**: micron·sub-micron 모두
  **≈700 mAh g_active⁻¹** (S+LPSCl 기준).  ⚠ 1C 는 **Li-In 임계전류 ~1 mA cm⁻² 초과**.
- **장기 (C/2 = 800 mA g⁻¹, 500 사이클, 25 °C)**: **Micron 81 %** > **Sub-micron 61 %** ≫ Bulk 급락
  (200 사이클 이내, ~320 mAh g⁻¹ 로 주저앉음).  ★ **+20 %p** 가 헤드라인.
- **탄소 대조 (Fig S29, micron 고정, VGCF/AB/KB)**: 비표면적↑ → 이용률↑(주로 SE 기여)
  **그러나 사이클 안정성에는 영향 없음** ⇒ 열화는 **탄소-SE 분해가 아니라 (화학)역학**.
- **EIS 100/300/500 사이클 (Fig 5f, S30, 탈리튬 상태)**: sub-micron 이 전 구간에서 높은 CEI 저항.
  막대 판독(**digitized, TREND only**) — CEI: micron **≈260 / 285 / 357 Ω**, sub-micron **≈418 / 443 / 512 Ω**;
  SSE: micron ≈20 / 17 / 12 Ω, sub-micron ≈35 / 28 / 28 Ω.  등가회로 = `SSE — [CEI ∥ CPE1] — CPE2`.
  ⚠ 저자 자신이 *"these results differ marginally"* 라 적는다.
- **cross-section SEM (Fig S31)**: micron ↔ sub-micron **구별 불가한 형상** ⇒ 그래서 FEM 을 불렀다.

### 6.6 부피변화·형상 (Fig 6, S32–S34)
- **S 양극 (cryo-FIB, Fig 6a)**: **26 µm (pristine) → 32 µm (리튬화) → 32 µm (1 사이클 후)**.
  예상치 **25.8 vol% 변화 → 32.7 µm** (Fig S33 정확값 25.841 %) — 관측과 근접.
  리튬화 용량 **1.22 mAh** ⇒ **4.9 µm mAh⁻¹**.
  1 사이클 후 두께 유지되나 **porosity 증가**로 설명(정량 없음).
- ★★ `derived(ours)` **Li 금속 스트리핑은 4.85 µm mAh⁻¹ cm²** (ρ_Li 0.534 g cm⁻³, 3861 mAh g⁻¹)
  ⇒ **4.9 vs 4.85 = 1 % 이내 일치** = 부피 상쇄가 **우연이 아니라 화학량론적으로 거의 정확**하다.
- **Li₂S 양극 (Fig 6b)**: **45 µm (pristine) → 26 µm (탈리튬, −42 %) → 32 µm (1 사이클 후)**.
  탈리튬 시 **컬럼형 균열**(단면 + 표면 Fig S34) — Si 음극에서 보고된 것과 같은,
  **2D 계면에 구속된 전환형 전극의 변형-유기 균열**.
  ⇒ ★ **Li₂S 가 S 보다 역학적으로 불리**(수축이 균열을 만든다).
- **Fig S32 (부과 부피팽창의 근거)** — Source Data 정확값 + 그림 판독
  | | 이용률 (%) | 부피변화 (%) |
  |---|---|---|
  | Sub-micron S | **95** | **75** |
  | Micron S | **90** | **71** |
  | Bulk S | **80** | **63** (그림) / **93** (Source Data XLSX) |
  ⚠ **Bulk 값 불일치**: XLSX 는 93, 그림의 막대는 명확히 **63**.  이용률 단조(95/90/80)와
  정합하는 것은 **63** 이므로 XLSX 오타로 판단.  **둘 다 기록**한다.
- **operando 압력 (Fig 6c/6d, C/10, 25 °C, N/P = 2, 기준 75 MPa)** — 로딩: LCO 26 mg cm⁻²
  (0.1 A g⁻¹) · S 2.5 mg_S cm⁻² (0.16 A g⁻¹) · Li₂S 3.8 mg cm⁻² (0.10 A g⁻¹)
  | 셀 | 압력 거동 (digitized, **TREND only**) |
  |---|---|
  | **LiSi ‖ Sulfur** (4 mAh cm⁻²) | 75.5 → **73.9 MPa** 완만한 하강 (**|Δ| ≈ 1.6 MPa**) |
  | LiSi ‖ LiCoO₂ | 76 → **80.7** → 77.7 MPa (**Δ_max ≈ +4.7**) — 본문 *"five times"* |
  | **µSi ‖ Li₂S** (3.5 mAh cm⁻²) | 76.2 → 75.75 → 76.05 (**밴드 ≈ 0.4 MPa ≈ 0**) |
  | Si ‖ LiCoO₂ | 76 → **77.8** → 76.2 (Δ ≈ +1.8) |
  ⇒ ★ **75 MPa 기준에서 ΔP/P < 1.5 %** — 전환형 양극 + 고용량 음극의 **역학적 균형** 시연.
  (µSi‖Li₂S 는 Fig S35 에서 **140 사이클 83 % 유지**, C/20 5 사이클 후 C/5, N/P 2.)

### 6.7 고로딩·셀 아키텍처 (Fig 7, Table S8)
| 시스템 | 값 | 조건 |
|---|---|---|
| Li-In ‖ S 1st 사이클 | **1314 mAh g⁻¹ @ 10 mAh cm⁻²** | 7 mg_S cm⁻², C/20 (0.08 A g⁻¹), 75 MPa, 25 °C |
| **11 mAh cm⁻² 사이클** | **86.8 % / 140 사이클** | C/20 (0.1 A g⁻¹), **0.52 mA cm⁻²**, AM 7 mg_S cm⁻², 25 °C |
| 건식 Li₂Si ‖ S 율특성 | 0.05C→**1C (5.5 mA cm⁻²)**, C/20 완전 회복 | 5.5 mAh cm⁻² 급 |
| 건식 Li₂Si ‖ S 사이클 | **77.4 % / 147 사이클** | **7.4 mAh cm⁻²**, C/5 (0.32 A g⁻¹), 1.5 mA cm⁻², AM 4.6 mg_S cm⁻², N/P 2, 25 °C |
| **Li₂S ‖ anode-free 파우치** | 1st **1077 mAh g⁻¹**, **ICE 83 %**, 가역 **≈900 mAh g⁻¹** | C/10 (0.1 A g⁻¹), **60 °C**, 4.7 mAh cm⁻², 15 mAh, 3.24 cm², 분리막 **50 µm** |
| 〃 사이클 | **86.6 % / 47 사이클**, **평균 CE 99.80 %** | **C/3 (0.34 A g⁻¹ = 1.5 mA cm⁻²)**, **등방압 10 MPa**, **60 °C**, AM 4.3 mg cm⁻² |
| 이론 비에너지 (Fig 7g) | 30 wt% S · 10 mAh cm⁻² → **≈520 Wh kg⁻¹** ("This work" 마커) | Li 금속 음극 + **30 µm SSE 층** + 1600 mAh g⁻¹ 가정 |
| 비에너지 비교 (Fig 7h) | S‖Li금속 **552** · S‖리튬화Si **480** · Li₂S‖Si **403** · Li₂S‖Li금속 **457** · **Li₂S‖anode-free 503** Wh kg⁻¹ | Table S8 가정치로 계산 ↓ |

**Table S8 전수 (비에너지 계산 가정)** — 5 아키텍처 공통: 면적용량 **10 mAh cm⁻²**, 양극 활물질 **30 %**,
SSE 두께 **30 µm**, SSE 밀도 **1.6 g cm⁻³**, **SSE 상대밀도 85 %**, Cu 박 10 µm / 8.9 g cm⁻³,
Al 박 10 µm / 2.7 g cm⁻³, 바인더 **1 %**.
| | Li‖S | Li₂Si‖S | 100 % Si‖Li₂S | Li금속‖Li₂S | anode-free‖Li₂S |
|---|---|---|---|---|---|
| 공칭전압 (V) | 1.7 | 1.7 | **1.4** | 1.7 | 1.7 |
| N/P | 1.2 | 1.2 | 1.2 | 1.2 | **—** |
| 음극 용량 (mAh g⁻¹) | 3500 | **860 (실측)** | 3500 | 3500 | — |
| 음극 밀도 (g cm⁻³) | 0.5 | — | 2.3 | 0.5 | — |
| 양극 용량 (mAh g⁻¹) | 1600 | 1600 | 1000 | 1000 | 1000 |
| 양극 밀도 (g cm⁻³) | 2 | 2 | 1.66 | 1.66 | 1.66 |

★ **정정 (정직)**: §10-11 에서 *"porosity 실측값 0건"* 이라 적었는데, 정확히는
**미세구조 모델·양극 실험 어디에도 porosity 값이 없고**, 유일하게 등장하는 것이 이 **Table S8 의
"SSE Relative Density 85 %"**(= **분리막 층 porosity 15 %** 가정)이다.  그것은 **비에너지 스프레드시트의
가정치**이지 측정도, 양극 미세구조 값도 아니다.  ⇒ 우리 압밀 축과 대조 불가라는 결론은 유지된다.
(참고로 15 % 는 우리 real_14 ε_sphere 15.6 % 와 우연히 가깝지만 **다른 층·다른 규약**이다 — 섞지 말 것.)

⚠ **헤드라인 조건 주의**: 초록의 *"11 mAh cm⁻² … at 25 °C"* 는 **펠릿·75 MPa** 이고,
*"low stack pressure of 10 MPa"* 파우치는 **60 °C** 다.  두 헤드라인의 조건이 다르다.
파우치는 제조 시 **WIP 500 MPa @ 80 °C** 를 거친다 — **제조압 ≠ 작동압** (우리 Doux/Cronau/Minnmann 3종 압력 구분 그대로).

---

## 7. ★ 우리 DEM+MPM 대비 (frame [1]–[5])

### 7.1 같은 것
| 축 | 그들 | 우리 |
|---|---|---|
| SE | **Li₆PS₅Cl** | Li₆PS₅Cl ✅ 동일 |
| E_SE | **22 GPa** (FEM 입력) | DFT **E_VRH 22.06** ✅ 0.3 % 일치 (⚠ 우리 DEM 1.35 / MPM 1.53 은 **연화 프록시**이지 물성이 아니다, frame[2]) |
| ρ_SE | **1.6 g cm⁻³** | 1.64 (Bazzoun) ≈ 일치 |
| τ 정의 | **TauFactor** `D_eff = D·ε/τ` | 우리 **τ_Laplace,bulk** 와 같은 form (우리 TauFactor 카드 §1) |
| 미세구조 → 수송 | voxel 상에서 상별 지표 | 우리 STEP3 도 **MPM 상 격자 위 유한체적** ∇·(σ∇φ)=0 ✅ 같은 이산화 |
| 압력 구분 | 제조 375–500 MPa ↔ 작동 10–75 MPa | 우리 3종 압력 규율 그대로 ✅ |

### 7.2 다른 것 — **가장 중요한 축**
| 축 | 그들 | 우리 | 판정 |
|---|---|---|---|
| **porosity** | **10 vol% 를 *입력*으로 고정** (FEM 은 그마저 0 으로 지움) | **압밀에서 *산출*** (LIGGGHTS 300 MPa → ε_sphere; MPM wallP/hold) | ★★ **frame[3] 정면 대비**.  그들은 "porosity 가 얼마인가"를 **물을 수 없다** |
| **압력** | 모델에 **압력 변수 자체가 없다** | Heckel(P_y 138 MPa)·다압력 스윕·servo/hold | 그들 모델은 **P-의존 아무것도 못 낸다** |
| **입자 처리** | S = **강체 구, 형상 불변**.  탄소 = aggregate(voxel).  SE = **연속체 선형탄성** | DEM = 강체 구 + CONTACT 소성(hooke/hysteresis) / **MPM = 진짜 SHAPE 소성 (J2)** | ★ 그들은 **3층 어디에도 소성이 없다** — CONTACT 소성조차 없다 |
| **접촉망** | 없음 (voxel 연속체) | DEM **Kirchhoff + Holm 1/(2σr_c)** 접촉당 협착 | σ 를 접촉 단위로 분해하는 것은 우리 고유 |
| **σ 삼중항** | **하나도 안 낸다** (τ 만; σ_ion·σ_e·k 계산 0건) | σ_ion / σ_e / k_thermal | ★ 그들의 τ 는 σ 로 이어지지 않는다 |
| **역학 완화** | 없음 (탄성 + u=0 + no porosity) | MPM 소성 유동 · void-fill · 축적소성변형장 | ★ frame[5] 우리 반쪽이 통째로 비어 있음 |
| **파괴** | 없음 | Auerbach 파괴 · A10 CZM (Bucci G_c 2.8±1.8) | |
| **반응분포** | *"uniformly lithiated"* | STEP4-v2 비선형 BV + 구형확산 시간전개 | |
| **격자 규율** | voxel 크기 **미기록**, 수렴시험 0 | `d_h/dx ≳ 3.5` 실용선 + CL-25/CL-41 격자 원장 | ★★ **우리가 앞선다** |
| **오차막대** | 3 침대인데 **SD 0건** | 시드 앙상블 · 쌍대응 SE · prereg 판정선 | ★★ 우리가 앞선다 |
| **RVE 검증** | 주장만 (RVA 없음) | Bazzoun box-factor 35 수렴 참조 · 우리 RVE 논의 | |

### 7.3 그들이 앞서는 것 (정직하게)
1. **실험이 압도적으로 두껍다** — cryo-FIB 두께 시계열, operando 압력, in-situ EIS, XANES LCF,
   TGA 정량, 500 사이클, 파우치.  우리 frame[4] 외부 앵커로 **그대로 쓸 수 있다**.
2. **Li–S 전환형 화학** — 우리 코퍼스는 전부 삽입형(NMC811/NCA).  **부피변화 25.8 %(전극)·
   71–75 %(입자)** 는 우리가 다뤄 본 적 없는 스케일이다.
3. **부피 상쇄(volume-change offsetting) 라는 설계축** — 우리 플래튼/스택압 축에 **없던 개념**.
4. **eigenstrain 으로 리튬화 팽창을 거는 실행 예제** — §4.6 의 이식 대상.

### 7.4 ⚠ 전이 금지 / 조건부
- **AM 이 다르다**: **원소 S / Li₂S** ≠ NMC811.  E_S = 17.8 GPa, ν 0.32 (우리 E_CAM 161.5 / 175 와 무관).
  **입자 부피변화 71–75 %** ≠ NMC811 의 수 %.  ⇒ **응력·팽창 절대값 전이 금지**.
- **τ 절대값 전이 금지**: 그들 τ 는 (a) voxel 크기 미기록, (b) RVE 대표성 미검증, (c) 오차 미보고,
  (d) 조성 축이 wt/vol 혼합.  ⇒ **순서(micron 최저)만 정성으로**, 숫자는 인용 시 조건 4개 병기.
- **active surface 절대값 전이 금지**: §3.3, 격자 단위 지표.  **참 대비의 1/7 로 압축**돼 있다.
- **5 GPa 전이 조건부**: 소성·공극·거시팽창을 전부 막은 **상한**.  "SE 가 소성해야 한다"는
  *정성 결론*은 견고하고, *숫자*는 상한으로만.
- **우리 쪽 인용 규율**: SDCP 이득의 vox 0.4 세대 수치(철회 계열)를 이 카드에 소환하지 않는다.
  격자 의존을 말할 때는 **세 값을 나란히 적고 "격자 수렴 미확인"** 이라고만 쓴다
  (0.15 / 0.125 / 0.115 → 1.123191 / 1.143817 / 1.155448, 증분비 1.773 이라 멱법칙 불성립).

---

## 8. Figure set ★

| Fig | 내용 | 우리가 쓸 것 |
|---|---|---|
| **1** | 개념도 — 고비에너지 ASSB 를 위한 Li–S 양극 설계 4요소 | 서사 프레임 |
| **2a** | 3 합성법의 1st 사이클 (C/20, Li-In) | **CE 17 → 129 %**; 합성이 계면을 만든다 |
| **2b–d** | XRD / Raman / XANES + 1차 미분 | Li₃PS₄₊ₙ 동정 3중 증거; **2470.1 eV pre-edge** |
| **2e** | S ↔ LPSCl 표면반응 모식 | |
| **3a–d** | LPSCl 단독 용량 · CV · dQ/dV 1st/3rd | **SE redox 정량 분해**(7.5 % / 9.2 % / 27.5 %) |
| **4a** | in-situ EIS 1st 형성 | **+85.2 Ω** 후 복귀 |
| **4b,c** | 고로딩 XRD · TGA (pristine/방전/충전) | Table S4 정량 |
| **4d–f** | XANES LCF wt% (LPSCl / S / Li₂S 계) | 상 정량 + **한계 명시(TFY, 0.06 % 면적)** |
| **★5a** | **생성된 3 기하 렌더** (Bulk 200 / Micron 50 / Sub-micron 15 µm; carbon·LPSCl·pore·sulfur 4상) | ★ **LPSCl/탄소가 voxel 텍스처로 보인다** — 상 배치가 입자가 아니라 격자 수준임을 육안 확인 |
| **★5b** | **active surface (%) vs AM (%)**, 3 입경 | §3.3·§3.6 정확값.  **순서만 사용, 세기는 격자 산물** |
| **★5c** | **ionic transport tortuosity vs AM (%)** | §3.5 정확값.  **교차 없음 · sub-micron 만 50→60 에서 ×2.57** |
| **5d** | 1st 형성 3 입경 | 1694 / 1615 / 1500 mAh g_S⁻¹ |
| **5e** | 500 사이클 C/2 | **81 % vs 61 %** (+20 %p) |
| **5f** | 100/300/500 사이클 Nyquist + 등가회로 막대 | CEI 저항 증가, ⚠ *"differ marginally"* |
| **★5g** | **von Mises 분포 3D** (0–5 GPa 컬러바; 25 µm / 10 µm 박스) | ★ 응력이 **S 표면 껍질**에만.  ⚠ 박스 크기가 RVE 와 불일치 |
| **★5h** | **최대 von Mises 히스토그램** (0–8 GPa) | ★ **이봉**; 2번째 봉 ≈4.1 GPa 에서 sub-micron 이 2배; **평균 2.42 vs 2.40 GPa = 사실상 동일** |
| **6a,b** | cryo-FIB 단면 (S / Li₂S, 3 상태) | **26→32→32 µm** · **45→26→32 µm + 컬럼균열** |
| **6c,d** | operando 압력 + 전압 | **ΔP < 1.6 MPa (S) / ≈0 (Li₂S)** vs LCO 4.7 / 1.8 |
| **7a–c** | 펠릿 Li-In‖S 고로딩 | **11 mAh cm⁻² · 86.8 % / 140 cyc** |
| **7d–f** | 건식 Li₂Si‖S | **7.4 mAh cm⁻² · 77.4 % / 147 cyc**, 1C = 5.5 mA cm⁻² |
| **7g,h** | 비에너지 지도 · 아키텍처 비교 | 30 wt% · 10 mAh cm⁻² → 520 Wh kg⁻¹; **anode-free Li₂S 503** |
| **7i–k** | anode-free 파우치 | **10 MPa · 60 °C · C/3 · 86.6 %/47 cyc · CE 99.80 %** |
| SI S1–S35 | 합성 모식 · SEM · XRD/Raman/EIS · LCF 전수 · **S32 부피팽창** · **S33 wt%→ΔV** | S32/S33 = FEM 입력의 출처 |
| Table S6/S7 | **FEM 파라미터·방정식 전수** | §4.2·§4.3 |

---

## 9. Post-processing ★

| 무엇 | 도구 | 어떻게 수치화 |
|---|---|---|
| 기하 생성 | **MATLAB (Duquesnoy 2020, ref 67)** | 확률적 배치; S=구, C=aggregate; pore 10 vol% 고정 |
| **active surface** | 자체 voxel 카운트 | `#(S∩LPSCl 픽셀)/#(S 픽셀)`, 3 침대 평균 ⚠ 격자 의존 |
| **tortuosity** | **TauFactor (MATLAB), ref 68 = Cooper 2016 SoftwareX** | LPSCl 상, **전 방향 평균**, 3 침대 평균.  우리 카드 `taufactor_tortuosity_factor_tomography_tool` **상호참조** |
| 메시 | **Iso2Mesh (ref 69 = Tran 2020 Neurophotonics)** | voxel → 사면체.  요소 크기 미기록 |
| FEM | **COMSOL Multiphysics 6.1, Solid Mechanics** | 선형탄성 + Hygroscopic Swelling eigenstrain, u=0 BC |
| β_H 보정 | **2D 단일입자 런** | 목표 부피팽창이 나올 때까지 역보정 (반지름으로 통제) |
| 부피팽창 입력 | 1st 방전 용량 − LPSCl 기여 → 이용률 → ΔV | Fig S32 (95/90/80 % 이용률 → 75/71/63 % ΔV) |
| EIS 피팅 | **ZView** (σ) · 등가회로 Fig S15/S30 | SSE + CB(CPE1) + CPE2 직렬 |
| XANES | **Athena (IFEFFIT)** — 배경/정규화/LCF | 비선형 최소자승 |
| 열분석 | NETZSCH STA 449 F3, **RT→450 °C, 5 °C/min, N₂** | S 정량 |

⚠ **우리 STEP3 와 비교**: 우리도 voxel 격자에서 상을 읽지만 (a) 그 격자는 **MPM 압밀 결과**이고,
(b) 우리는 **격자 원장(CL-25)** 으로 상별 표현부피/참부피 비를 실측하며,
(c) `d_h/dx ≳ 3.5` 게이트를 **런 전에** 찍는다.  이 논문에는 (a)(b)(c) 가 전부 없다.

---

## 10. ★ 비판 · 한계 (bounded transferability)

1. **★★ 이 모델에는 길이척도가 없다.**  선형탄성 + 부과 등방 eigenstrain 은 스케일 불변이다
   (§5.2(iii), Eshelby σ_vM = Eε\*/(1−ν), 반경 무관).  따라서 **"입경이 응력을 바꾼다"는 결론이
   구성모델에서 나올 수 없고**, 실제로 평균은 2.42 vs 2.40 GPa 로 **차이 0.8 %** 다.
   Fig 5h 가 보여주는 것은 **비표면적의 재표현** = Fig 5b 의 응력 단위 번역이다.
2. **★★ 역학 기하 ≠ 수송 기하.**  τ·표면적은 pore 10 % 기하에서, 응력은 *"fully compact"* 기하에서
   나왔다.  같은 그림(Fig 5) 안에서 **두 개의 다른 전극**을 비교하고 있다.
3. **★★ voxel 크기 미기록 + 격자 수렴 0.**  active surface 는 정의상 `∝ h` 라 **h→0 에서 0 으로 간다**.
   sub-micron 은 **R/h ≲ 3.4** 로 이미 바닥이다.  ⇒ 우리 CL-25(18.1배 변동)와 같은 함정에
   **측정 없이** 서 있다.
4. **★ Bulk RVE 는 입자 ~8개짜리 셀**(변당 지름 2–2.5개).  *"To have a representative volume"* 은
   시연 없는 주장이고, TauFactor 의 RVA 를 쓰지 않았다.
5. **★ 3 침대인데 산포 0건.**  Fig 5b/5c/5h 어디에도 오차막대가 없고 Source Data 도 평균만 준다.
   micron ↔ sub-micron 의 τ·응력 차이가 **통계적으로 유의한지 판정 불가**.
6. **소성이 없는데 결론이 소성이다.**  본문은 SE 의 **소성변형**으로 형상을 설명하는데
   (cryo-FIB 관측), 모델은 순수 탄성이다.  ⇒ 5 GPa 는 *"소성이 필요하다"* 의 증거이지
   *"실제 응력"* 이 아니다.  `derived(ours)` K_IC 0.3 MPa·m^½ 기준 임계 결함크기
   **a_c ≈ 0.8 nm @ 6 GPa** — 탄성 해는 물리적으로 유지 불가.
7. **ν = 0.3 이 자기 참조(Deng 2016, ν = 0.37)와 불일치** → K 를 **−30~−36 %** 로 과소평가.
   (⚠ 공정하게: von Mises 헤드라인에 대한 영향은 **+12 % 수준**이다, §4.7.)
8. **조성 축이 wt/vol 혼합**이고 ρ_carbon 이 없어 **독립 재현이 불가능**하다.
9. **Methods 의 표 번호 오기** (S3/S4 → 실제 S6/S7) · **Source Data 계열 라벨 오기**
   (Fig 5b/5c 세 계열 전부 "Sub-Micron S") · **Fig S32 Bulk ΔV 63(그림) vs 93(XLSX)** 불일치.
10. **Fig 5g 박스(25/10 µm) ≠ 생성 RVE(50/15 µm)** — 부분체적 사용으로 보이나 미기록.
    사실이면 micron FEM 셀의 S 입자는 **≈26개**로 줄어든다 `derived(ours)`.
11. **porosity 실측값이 0건.**  모델은 **10 vol% 입력**, 실험은 *"an increase in porosity"* 정성 서술뿐.
    유일한 숫자는 **Table S8 의 "SSE Relative Density 85 %"**(분리막 층 porosity 15 %) 인데
    그것은 **비에너지 계산의 가정치**이지 측정도 양극 값도 아니다 (§6.7 정정 참조).
    ⇒ 우리 압밀 축과 **수치로 대조할 지점이 없다** (이 카드가 §A 에 porosity 행을 못 채우는 이유).
12. **σ_ionic·σ_e 를 미세구조에서 계산하지 않는다** — τ 에서 멈춘다.  실험 σ 는 벌크 EIS 뿐.
13. **1st 리튬화 1회 스냅샷** — 사이클 누적·springback·재습윤 없음(저자 자신이 명시).
14. ⚠ **파우치 헤드라인의 온도**: "10 MPa 저스택압"은 **60 °C**.  25 °C 저압 데이터는 없다.

---

## 11. 우리 모델에 바로 쓸 것 (실행 항목)

| # | 항목 | 어디에 |
|---|---|---|
| **U1** | **`--am-eigenstrain <ΔV>`** — MPM AM 상에 등방 체적 eigenstrain 부과 → **탄성 상한(그들) vs J2 소성 완화(우리)** 를 같은 기하에서 비교.  검증 표적 = 계면 σ_vM 이 **Eε\*/(1−ν) = 6.15 GPa** 에서 소성으로 얼마나 떨어지는가 | `scripts/mpm3d_compaction.py` + 백로그 |
| **U2** | **LPSCl 탄성 앵커 3자 합의 확정**: E = **22 / 22.1 / 22.06 GPa** (Cronk FEM / Deng DFT / 우리 DFT).  원고 §Methods 물성 행에 3자 병기 | `docs/sulfide_se_mechanical_anchors.md` |
| **U3** | **ν=0.3 함정의 외부 사례**로 Cronk Table S6 를 인용 (우리 SDCP SI 정정의 논거 강화) | 동상 · CLAUDE.md ν 절 |
| **U4** | **부피 상쇄 앵커**: **4.9 µm mAh⁻¹** (S 양극) ≈ **4.85 µm mAh⁻¹** (Li 금속) ⇒ 우리 플래튼/스택압 축에 "**양극 팽창으로 음극 수축을 상쇄**"라는 **새 설계 자유도** 추가 | `comparison_vs_ours_DEM.md` §C |
| **U5** | **operando 압력 밴드**: 75 MPa 기준 ΔP **1.6 MPa (S) / 0.4 (Li₂S) / 4.7 (LCO)** → 우리 작동압 원장(Doux 5 · Lee 2 · Minnmann 40 · Wang 110 · Luan 30)에 **75 MPa 행** 추가 | 동상 §A |
| **U6** | **τ 문턱 증거**: sub-micron τ 가 50→60 wt% 에서 **×2.57** — 우리 σ_ionic φc(0.195/0.200 FROZEN)·σ_e φ_AM<0.3 금지선의 **τ-쪽 대응 관측**.  ★ 솔브된 τ 는 발산할 수 있고 **우리 멱법칙은 못 한다** | 동상 §B |
| **U7** | **격자 규율 홍보 재료**: 이 논문은 voxel 크기를 안 적었고 우리는 CL-25 로 **18.1배 변동을 실측**했다.  원고 §Methods 의 "격자 원장" 절 정당화 | 원고 |
| **U8** | **TauFactor SA 출력 사용** — 우리가 표면적을 낼 때 voxel 비가 아니라 **µm⁻¹ 차원량**을 쓰도록 규약화 (그들이 놓친 자리) | STEP3 후처리 |

---

## 12. ★ ref 67 (Duquesnoy 2020) 을 받아야 하는가 — 판정

**Duquesnoy, Lombardo, Chouchane, Primo, Franco, "Data-driven assessment of electrode calendering
process by combining experimental results, in silico mesostructures generation and machine learning",
*J. Power Sources* 480 (2020) 229103.**  카드 작성 시점(2026-09-03)에 `papers/` **미보유**
(우리는 Duquesnoy **2023** ESM 만 보유).

> ★★ **상태 갱신 (2026-09-03, 이 카드 작성 중 발견)**: 정본 워크트리에
> `litdb/figures/duquesnoy2020_calendering_ml_mesostructure_generator/` (그림 7장, 출처 PDF
> `Duquesnoy_2020_JPowerSources_DataDriven_Calendering_ML.pdf`) 가 **같은 날 생성돼 있다**
> = **다른 세션이 이미 그 논문을 확보해 digest 진행 중**이다 (카드 `.md` 는 아직 없음).
> ⇒ 아래 판정은 *"받아야 하나"* 가 아니라 **"받은 것을 무엇에 쓸 것인가"** 로 읽는다.
> 그 카드가 올라오면 **§3.2 의 미기록 8항목을 1:1 로 대조**할 것 (특히 voxel 크기·주기경계·겹침·시드).

**판정: 필수다 — 단 목적은 물리가 아니라 *메타데이터*다.**

| 근거 | 내용 |
|---|---|
| ① **미기록 항목이 거기 있을 가능성이 높다** | voxel 크기 · 주기경계 · 겹침 규칙 · 시드 · aggregate 모델 = Cronk 2026 이 하나도 안 적은 항목이고, **생성기 원논문**이 그것을 정의한다.  §3.2 의 8개 구멍 중 최소 5개가 닫힌다 |
| ② **§3.3·§3.5 의 판정을 확정형으로 바꾼다** | 지금 우리는 "격자 의존이다(원리)" 까지만 말할 수 있다.  h 를 알면 **"micron 최저 τ 가 물리인가 해상도인가"** 를 계산으로 가른다 |
| ③ **계보의 뿌리** | Franco/ARTISTIC → Duquesnoy 2020 (생성기) → Chouchane (Meng 그룹 이식) → **Cronk 2026 + ACS EL 2024**.  우리 litdb 에 2023(ML) 은 있는데 **생성기 자체가 없다** = 계보에 구멍 |
| ④ **우리 positioning 문서의 정밀도** | `positioning_vs_geodict.md` 가 "구조 *생성*은 규칙 배치, 우리는 압축 물리" 라고 좁혀 놨는데, 그 "규칙"의 **정본 정의**를 아직 안 갖고 있다 |
| ⑤ **저비용** | J. Power Sources, 단편.  읽기 부담 작음 |

⚠ **받되 지켜야 할 선**: 그 논문은 **LIB 액체계 캘린더링**(흑연/NMC + 액체 전해질)이다.
⇒ **물성·τ·porosity 절대값 전이 전면 금지**, 가져올 것은 **생성 알고리즘 규약**뿐.
(우리 `zhang2026` 카드의 chemistry 게이트와 같은 등급: FORM/METHOD-ONLY.)

**함께 받으면 좋은 것 (2순위)**: **Chouchane, Yao, Cronk, Zhang, Meng, ACS Energy Lett. 9 (2024) 4**
— `comparison_vs_ours_DEM.md` §🎤 가 이미 "확보 1순위"로 적어 둔 그 논문.  Cronk 2026 의
모델링 절이 그것의 ASSB 판이므로 **둘을 같이 보면 이 파이프라인 전체가 닫힌다.**

---

## 13. 기술 미니-용어집

- **eigenstrain (고유변형률)** — 응력을 만들지 않는 "무응력 변형" (열팽창·상변태·리튬화 팽창).
  구성식은 `σ = C : (ε − ε*)`.  이 논문은 ε\* 를 COMSOL 의 **Hygroscopic Swelling** 노드로 넣었다
  (물 농도 대신 Li 농도).  **등방(체적)** 이라 편차 유동(소성)이 없다.
- **Eshelby 개재물 해** — 무한 기지에 든 타원체 개재물의 eigenstrain 문제의 해석해.
  등방 팽창 구의 경우 **기지 von Mises = E ε\*/(1−ν) · (a/r)³** 이며 **반경 a 에 무관** = 스케일 불변.
- **tortuosity factor τ (TauFactor 규약)** — `D_eff = D · ε/τ`.  **기하학적 경로길이 비(τ_geo)와 다르다**
  (고전 관계에서 τ_factor ≈ τ_geo²).  ⚠ 논문 간 인용 시 이 규약 차이가 **+33 % vs +15 %** 같은
  미끄러짐을 만든다 (우리 `zhang2026` 카드 §⑤ 사례).
- **specific active surface area (이 논문의 정의)** — `#(S∩LPSCl voxel)/#(S voxel)`.
  ⚠ **차원이 없다** — 진짜 비표면적 [µm⁻¹] 이 아니라 **격자 단위로 잰 껍질 분율**.
- **Li₃PS₄₊ₙ** — PS₄³⁻ 말단 S 에 원소 S 가 사슬로 붙은 황-풍부 티오포스페이트.
  Raman S–S 굽힘 적색이동 + PS₄³⁻ 신축 약화 + XANES pre-edge 로 동정.
- **CE 129 %** — 충전용량/방전용량 > 1.  S 외에 **SE 자체가 산화 용량을 낸다**는 뜻
  (열역학적 "초과 용량"이 아니라 **다른 활물질의 기여**).
- **anode-free** — 음극 활물질 없이 집전체 + 핵생성층(여기선 카본블랙:Ag:PVDF)만 두고
  충전 중 Li 를 그 자리에 도금.  Li 금속 대비 제조·비에너지 이득, ICE 손실이 대가(여기 83 %).
- **WIP (warm isostatic pressing)** — 등방 가압 + 가온.  여기선 **500 MPa @ 80 °C** = 제조압.
- **hold vs servo (우리 용어, 대조용)** — 이 논문 FEM 은 **u=0 고정**이라 우리 `hold` 보다도
  강한 구속이다 (우리 hold 는 목표응력 도달 후 플래튼 고정, 이쪽은 **처음부터** 전 경계 고정).

---

## 14. 한 줄 결론

**압밀 물리를 빼고 porosity 를 입력으로 고정하면, 미세구조 모델은 "표면적과 굴곡도"까지만 말할 수
있고 "응력"은 사실상 그 표면적의 재표현이 된다.**  이 논문은 그 한계 안에서 훌륭한 실험과 짝을
이뤄 실용적 설계결론(micron S 가 최적)을 냈지만, **격자 크기·RVE 대표성·산포를 적지 않아 그
결론의 방법론적 근거는 재현 불가능**하다.  우리에게 이 논문의 값은 (a) **LPSCl E=22 GPa 3자 합의**,
(b) **4.9 µm mAh⁻¹ 부피 상쇄 앵커와 75 MPa 스택압 밴드**, (c) **eigenstrain 소스항 이식**,
(d) **"길이척도 없는 탄성 모델은 크기효과를 못 낸다"는 frame[5] 의 교과서적 반례** 넷이다.
