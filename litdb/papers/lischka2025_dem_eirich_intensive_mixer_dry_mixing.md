<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목.  COMPREHENSIVE / paper-level standalone. -->
# Eirich **집약형 실험실 믹서(EL1.0 / EL0.1)** 안의 Li-ion 양극 **건식 혼합**을 DEM 으로 — coarse-graining(CGF 200) + **JKR 점착 + cohesion-number 로 γ 를 입경에 맞춰 재계산** + 믹싱툴 소비전력 실험 검증, 그리고 "전단이 아니라 **툴과의 충돌**이 카본블랙 분쇄의 지배 기전" 이라는 판정 — Lischka & Nirschl (Particuology 2025)

> slug `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · DOI `10.1016/j.partic.2025.06.002` · type `DEM (EDEM 2022.3, coarse-grained CGF 200 + JKR cohesion, cohesion-number γ scaling; exp 소비전력·벌크밀도 검증)` · PDF `03. Simulation of an intensive lab mixer for dry mixing of Li-ion cathode materials via the discrete element method.pdf` · digested `2026-09-19` · status ✅ · OPEN ACCESS (CC BY 4.0)

> elements: C Co Li Mn Ni O

> ⚠⚠ **이 논문은 ASSB 가 아니다 — 고체전해질이 한 알도 없다.** 계는 **NMC622 (BASF) + 카본블랙 Super C65 2 wt%** 둘뿐이고, 그나마도 DEM 안에서는 **그 둘을 섞어 만든 단일 coarse-grain 입자 한 종**으로 표현된다. LPSCl 도, PTFE 도, 바인더도, SE 도 없다. ⇒ **소재 절대값(γ·μ·ρ·d)의 우리 계로의 전이는 금지**. 옮겨올 수 있는 것은 **방법(코스그레이닝 하에서 점착을 어떻게 재계산하는가)·지표 정의·판정 논리**뿐이다.

> ★★ **`frankenberg2024_dem_high_intensity_mixer_assb` 와 같은 논문이 아니다** (아래 §A-0 에 근거 전문). 짧게: 저자·기관·저널·연도·믹서·코드·소재가 전부 다르고, **이 논문이 Frankenberg (2024) 를 참고문헌으로 인용한다** (본문 §1 · §2: *"For a different type of mixer, the Nobilta annular gap intensive mixer, two papers by Asylbekov et al. (2023) and Frankenberg et al. (2024) can be found…"*). 즉 두 편은 **서로 다른 믹서를 다루는 별개 논문이고, 이 논문이 그쪽을 '다른 종류의 믹서' 로 명시적으로 구분**한다.

> ★ **같은 축의 이웃 카드 (교차참조)** — 이 카드는 혼자 읽어도 되지만, 건식혼합 축에서 다음과 짝을 이룬다:
> · **`hare2026_dem_pept_dry_mixing_nmc622_eirich`** (Powder Technol. 2026, DOI 10.1016/j.powtec.2025.121804) — ★★ **같은 믹서(Eirich EL1) · 같은 소재(NMC622) · 같은 코드계열(EDEM)** 인데 **PEPT 로 입자 궤적을 실측해 DEM 을 검증**한다. 본 카드가 §4.2 에서 *"Lischka 본문에 Hertz·Mindlin 이라는 낱말이 0회"* 라고 적은 공백을, 그 카드는 **`Hertz–Mindlin + JKR` 이라고 명시**해 **같은 믹서·코드 조합의 관행이 무엇인지** 알려 준다 (⚠ 그래도 *이 논문 본문* 은 그렇게 적지 않았으므로 본 카드의 한정어는 유지한다). 본 논문이 MSD 타당성 논거로 인용한 **Hare 2023 (CERD 197, 509)** 의 후속·확장이기도 하다.
> · **`nadeem2023_gnn_mixing_index`** (Adv. Powder Technol. 2023) — 혼합지표의 **사양서**. 본 카드 §4.6·§B-3 이 지적한 **RSD 의 표본크기 의존·bin 규약 미보고** 문제를 정면으로 다루는 쪽이라, "어떤 혼합지표를 우리가 구현할 것인가" 는 **그 카드가 정본**이고 본 카드는 **그 문제의 실물 사례**를 제공한다.
> · **`lippke2023_dem_drying_structure_formation_lib`** — 같은 제조사슬의 *건조* 단계 DEM (Lippke 는 `frankenberg2024` 공저자).

---

## 1. 한 줄 요약

**Eirich EL1.0 집약형 믹서 안에서 NMC622+카본블랙(2 wt%) 건식 혼합을 DEM 으로 풀어, ① 혼합 균질도(RSD)는 30 초 안에 포화하고 그것을 결정하는 것은 *툴 속도가 아니라 용기(vessel) 회전*이며, ② 카본블랙 분쇄(comminution)의 지배 기전은 *전단이 아니라 고속 회전 툴과의 충돌*(전단율 최대 10 s⁻¹ = 압출기 대비 1–2 자릿수 낮음)이고, ③ 툴 속도를 올리면 오히려 입자가 원심으로 밀려나 *충돌률은 떨어진다*(그래서 툴 확대·블레이드 추가가 혼합시간을 56 %·75 % 줄인다)는 세 판정을 낸 논문.** 방법론적 핵심 둘: **(A) coarse-graining CGF = 200** (DEM 입자 2.0 mm ↔ 실제 ~10 µm; 우리 계산 = CGF 정의를 stated 값에 적용) — CGF 100·150 은 기저와 일치하고 **CGF 400 부터 어긋나 "d > 2 mm 는 못 쓴다"** 는 상한을 실측으로 그었다; **(B) ★ 점착은 JKR 이고, 코스그레이닝으로 입경을 바꿀 때 표면에너지 γ 를 "cohesion number 불변" 으로 재계산**한다 (Eq 1–2, Behjani 2017) ⇒ **γ ∝ R\*^{8/5}** (우리 유도). **⛔ 그러나 γ ↔ linear adhesion stiffness k_c 환산식은 이 논문에 없다 — JKR-γ 계열 하나뿐이다.** 그리고 **점착을 상(phase)별로 다르게 주지 않는다** — 입자종이 하나뿐이라 `γ_pp` 하나 + `γ_pw`(벽) 하나, 총 2개다 (실측 비 `γ_pw/γ_pp = 1/6`, Table 1 다섯 행 전부). 전달 솔버·porosity·전기화학은 **전부 없다**.

## 2. 메타

| 항목 | 값 |
|---|---|
| **저자** | **Clemens Lischka\*** (교신, clemens.lischka2@kit.edu), **Hermann Nirschl** |
| **소속** | **Institute for Mechanical Process Engineering and Mechanics (MVM), Karlsruhe Institute of Technology (KIT)**, Straße am Forum 8, 76131 Karlsruhe, Germany |
| **저널 / 권 / 쪽 / 연도** | ★ **Particuology 104 (2025) 52–67** — **PDF 에서 직접 확인함** (① PDF 메타데이터 `subject` = *"Particuology, 104 (2025) 52-67. doi:10.1016/j.partic.2025.06.002"*, ② 1쪽 저널 배너 *"Contents lists available at ScienceDirect — Particuology — journal homepage: www.elsevier.com/locate/partic"*, ③ 16쪽 전부의 러닝헤드 *"Particuology 104 (2025) 52–67"*, ④ 1쪽 각주 ISSN `1674-2001`). ⇒ **"Particuology" 는 추정이 아니라 확인된 값**이다. |
| **DOI** | `10.1016/j.partic.2025.06.002` (1쪽 각주 + 메타데이터, 두 곳 일치) |
| **투고 이력** | Received 24 July 2024 · Revised 15 May 2025 · **Accepted 3 June 2025** · Available online 20 June 2025 |
| **라이선스** | © 2025 Chinese Society of Particuology and Institute of Process Engineering, CAS. Published by Elsevier B.V. — **CC BY open access** |
| **자금** | BMBF (독일 연방교육연구부), 과제 **Sim4Pro, grant 03XP0242B**, **ProZell Cluster** |
| **소재계** | **AM = NMC-622 (BASF)** + **도전제 = 카본블랙 IMERYS Super C65, 2 % mass fraction**. ⛔ **SE·바인더·PTFE 없음.** 액계 LIB 양극의 *건식 혼합 단계* (건식공정 추세 하에서 "유일하게 남는 혼합 단계") |
| **장비** | **Eirich EL1.0** (최대 충전 1 L) · **Eirich EL0.1** (최대 0.1 L) — 실험실급 집약형(intensive) 믹서 |
| **연구유형** | **DEM 공정 시뮬 (EDEM 2022.3, GPU) + 실험 검증**(믹싱툴 소비전력·벌크밀도·Lumisizer 침강 입도). 실험 파트(§3)는 선행 `Lischka et al. 2024 (Powder Technol. 431, 119072)` 의 데이터·프로토콜 위에 세워짐 |
| **abstract** | ⚠ **이 PDF 사본에는 초록 텍스트 블록이 없다** (1쪽 우단 `y ≈ 269–288` 구간이 비어 있고, 그 페이지의 이미지 3개는 전부 로고 크기다). 요약은 §5 Conclusion 으로 대체해 읽었다. |

> ★ **계보**: KIT-MVM (Nirschl) 라인. 본 논문은 **자기 그룹 선행 3편 위에** 서 있다 — ① **Lischka & Nirschl 2023** (*Energy Technol.* 11(5) 2200849, "Calibration of Li-ion cathode materials for DEM simulations") = **coarse-grain 보정 방법론의 정본**(본 논문은 *"A detailed description of the DEM methodology and also the calibration simulations used for the coarse grain approach is described in ref."* 라고 통째로 위임한다); ② **Lischka et al. 2024** (*Powder Technol.* 431, 119072) = 같은 Eirich 믹서의 **실험** 편(혼합품질·링전단셀·짧고 강한 혼합이 최적 전기전도도); ③ **Mayer / Bockholt / Kwade** 계열 = 카본블랙 분산도가 전극 성능을 정한다는 배경. 믹서 DEM 계보는 **Tokoro 2009**(Eirich R02 최초) → **Gong 2019 / Zuo 2021·2023**(Eirich EL10, 습식·밀도비·블레이드 배치) → 본 논문. **cohesion number** = **Behjani et al. 2017** (*Adv. Powder Technol.* 28(10) 2456). **벌크밀도-에너지 모델** = **Schilde et al. 2010** (*Chem. Eng. Sci.* 65(11) 3518) 의 습식 분산 동역학을 건식으로 이식. **충돌 응력 상한 논거** = **Rumpf 1959** · **Burmeister 2018**. **MSD 비교대상** = **Hare et al. 2023** (PEPT, 같은 EL1.0, 습식 음극 슬러리).

## 3. 핵심 수치 (stated / derived / digitized 를 행마다 표시)

### 3.1 DEM 재료·접촉 파라미터 (Table 1 전재 — **stated**)

> **Table 1 원문**: *"DEM simulation parameters used for different stages of comminution in accordance with mixing time and mixing tool speed."*
> ⇒ ★ **읽는 법**: 이 표는 "재료 물성표" 가 **아니다**. **혼합이 진행된 정도(= 카본블랙이 얼마나 분쇄됐나)를 입력 파라미터 5개(입경·밀도·정마찰·동마찰·점착에너지)로 *번역해 넣은* 표**다. 분쇄는 시뮬 안에서 **일어나지 않는다**(§4.5).

| 혼합시간 t_mix (툴속도) | 입경 d | 밀도 ρ_bulk | 정마찰 p-p μ_s,pp | 동마찰 p-p μ_d,pp | 정마찰 p-w μ_s,pw | 동마찰 p-w μ_d,pw | **점착에너지 p-p γ_pp** | **점착에너지 p-w γ_pw** |
|---|---|---|---|---|---|---|---|---|
| **0 min (30–20 m/s)** | **2.0 mm** | 1200 kg/m³ | **1.0** | **0.1** | **1.2** | 0.1 | **0.3 J/m²** | **0.05 J/m²** |
| 30 min (30 m/s) | 1.757 mm | 1817 kg/m³ | 0.504 | 0.0249 | 0.558 | 0.024 | 0.238 J/m² | 0.039 J/m² |
| 30 min (25 m/s) | 1.768 mm | 1781 kg/m³ | 0.504 | 0.025 | 0.559 | 0.025 | 0.239 J/m² | 0.0395 J/m² |
| 30 min (20 m/s) | 1.772 mm | 1768 kg/m³ | 0.505 | 0.0252 | 0.56 | 0.026 | 0.24 J/m² | 0.04 J/m² |
| 90 min (30–20 m/s) | 1.723 mm | 1938 kg/m³ | 0.5 | 0.025 | 0.55 | 0.025 | 0.236 J/m² | 0.0393 J/m² |

**모든 케이스 공통 (stated)**: 입자 전단탄성률 **G = 1e8 Pa**(*"constant shear modulus of 1e8 Pa … to minimize the computational cost associated with higher shear moduli"* — 즉 **계산비용 때문에 낮춘 값이지 물성이 아니다**) · 입자 **ν = 0.25** · **COR = 0.5**(*"basically impossible to measure for a mixture of two different species in a bulk"* 라 **가정값**) · 기하(스테인리스) **G = 1e11 Pa, ρ = 7650 kg/m³, ν = 0.25** · **timestep = Rayleigh 의 20 %** · 구름마찰(rolling friction) **표에 없음**(본문 §2.1 은 *"Static and rolling friction parameters as well as cohesion forces"* 를 보정 대상으로 열거하나 **값은 이 논문에 안 실림** — 선행 Lischka & Nirschl 2023 소관).

### 3.2 우리가 표에서 **뽑아낸 것** (derived — 전부 위 stated 값의 산술이다)

| 유도량 | 값 | 어떻게 | 왜 중요 |
|---|---|---|---|
| **★ 벽 점착 / 입자 점착 비** | **γ_pw / γ_pp = 1/6 = 0.1667**, **다섯 행 전부** | 0.05/0.3 = 0.16667 · 0.039/0.238 = 0.16387 · 0.0395/0.239 = 0.16527 · 0.04/0.24 = 0.16667 · 0.0393/0.236 = 0.16653 | 본문이 말한 *"벽 표면에너지에는 **입자-입자 접촉과 같은 스케일 인자**를 적용"* 이 **수치로 확인**된다 = 벽 점착은 독립 자유도가 아니라 **입자 점착에 1/6 로 묶인 종속 파라미터** |
| **★ CGF 200 이 대표하는 실제 입경** | **≈ 10 µm** | 2.0 mm / 200 = 10 µm. **교차확인 5/5**: 1.5/150 · 1.0/100 · 4/400 · 8/800 전부 10 µm | 논문이 **명시하지 않은** 값인데 CGF 정의로 일의적으로 정해진다. NMC622 2차입자 스케일로 타당. ⇒ 이 DEM 의 "입자" = **NMC 2차입자 + 그 표면의 CB 를 합친 10 µm 덩어리** |
| **★ cohesion-number 가 함의하는 γ 스케일링** | **γ ∝ R\*^{8/5} = R\*^{1.6}** (ρ·E\* 고정 시) | Eq (2) `Coh = (1/ρg)·(γ⁵/(E*²R*⁸))^{1/3}` 을 Coh = const 로 풀면 γ⁵ ∝ R\*⁸ | **★★ 우리 prereg `m7` §8-③ 의 직접 대상** — "점착을 입경에 어떻게 옮기나" 의 문헌 처방. §4.3 참조 |
| **Table 1 이 실제로 따르는 유효 지수** | **1.61 / 1.79 / 1.84 / 1.84** (행 5·2·3·4) | `n = ln(γ/0.3)/ln(d/2.0)` | ⚠ **단일 지수 1.6 으로 정확히 재현되지 않는다** — 1.723 mm 행만 1.61 로 딱 맞고 나머지 셋은 1.8 쪽이다. 논문은 Eq (2) 안에서 **ρ 를 어떻게 처리했는지 적지 않았다** (ρ 가 행마다 1200→1938 로 변한다). ⇒ 지수는 **1.6–1.85 밴드**로만 인용 |
| **★ 논문이 "Table 1 에 있다" 고 했는데 없는 값** | **CGF 150·100(및 400·800) 의 γ** | 본문 §2.2: *"we can nevertheless use Eq. (2) to find the necessary surface energy for particle diameters of 1.5 mm and 1 mm … **Table 1 gives these values**"* — 그러나 실제 Table 1 은 **혼합시간 5행뿐**이고 1.5 mm·1.0 mm 행이 **없다** (렌더로 표 원본 확인) | ⛔ **보고 누락**. CGF 스윕(Fig 9)에 실제로 들어간 γ 를 **독자가 알 수 없다** ⇒ 그 스윕은 **재현 불가** |
| (참고) 위 누락값을 R\*^{1.6} 로 **우리가 채워 본 값** | 1.5 mm → **≈0.19** · 1.0 mm → **≈0.099** · 4 mm → **≈0.91** · 8 mm → **≈2.76 J/m²** | 0.3·(d/2.0)^1.6 | ⚠ **전적으로 우리 추정**이다. 논문 값이 아니다. 인용 금지, 감 잡는 용도 |
| **★★ 그 스케일링을 실제 입자(10 µm)까지 밀면** | **γ_real ≈ 0.3 / 200^1.6 = 0.3/4799 ≈ 6.3 × 10⁻⁵ J/m²** | 200^1.6 = exp(1.6·ln200) = exp(8.4773) = 4799 | ⚠⚠ **비물리적으로 작다**(산화물 vdW 표면에너지는 보통 10⁻²–10⁰ J/m² 대). ⇒ **"보정된 CG γ 를 cohesion-number 로 되짚어 실제 γ 를 얻는다" 는 경로는 이 논문의 수에서 성립하지 않는다.** 논문 자신도 *"the surface energy between NMC and NMC particles is **unknown and difficult to measure**"* 라 적고 그 방향을 **포기**한다. ⇒ **문헌 γ 에 접지하려는 우리 시도에 대한 경고** (§B-2) |
| **입자 수** | **하한 ≥ 40,000 개** (확정) · 부피기준 **O(10⁵)** (느슨) | 하한 = RSD 프로토콜의 *"≥100 samples × ≥400 particles"* · 부피 = 800 mL × 패킹분율 φ ÷ (π/6)(2 mm)³ = 190,900·φ → φ 0.5–0.64 에서 95k–122k | ⚠ 논문에 **입자수가 한 번도 안 나온다**. 부피추정은 Table 1 의 `ρ_bulk` 가 EDEM 의 *입자밀도* 입력인지 *결과 벌크밀도*인지 논문이 구분 안 해서 느슨하다 |
| **★ 무작위혼합 한계의 올바른 RSD** | **RSD_r = 0.05** | 논문의 `RSD_s = x_t(1−x_t)/s = 0.25/400 = 6.25e-4` 는 **분산 σ_r²** 이다. RSD 로 바꾸면 `σ_r/x_t = √(6.25e-4)/0.5 = 0.025/0.5 = 0.05` | ⚠⚠ **논문의 "RSD < 0.05 는 무작위혼합값(0.000625)보다 훨씬 위" 라는 문장이 단위 혼동**이다. 같은 척도로 맞추면 **그들의 수렴값 0.05 = 무작위혼합 한계 그 자체** ⇒ 회전용기 케이스는 **사실상 완전혼합에 도달**한 것이다(논문 주장보다 *좋은* 결과). §10-① |
| **JKR pull-off 힘의 CG 스케일** | **F_po ∝ f^{2.6}** (본 논문) vs **f²** (Frankenberg 2024) | F_po = (3/2)πΓR\* 이고 Γ ∝ f^1.6·R ∝ f | ★★ **두 카드가 코스그레이닝 하에서 점착을 다르게 스케일한다** — §A-2 의 헤드라인 |

### 3.3 실험 결과 (§3 — stated / digitized)

| 양 | 값 | stated/digitized | 비고 |
|---|---|---|---|
| **벌크밀도 ↔ 비에너지 모델 (Eq 5, Schilde 이식)** | `ρ_bulk(t) = ρ_bulk,0 + (ρ_bulk,∞ − ρ_bulk,0)·e_tot(t)/(e_tot(t)+K_t)` | stated | `K_t` = 최종 벌크밀도의 50 % 에 도달하는 데 필요한 에너지(공정·재료 상수). ⚠ **K_t 의 수치는 논문에 없다** |
| **최대 도달 벌크밀도 ρ_bulk,∞** | **1.83 g/mL** (= 1830 kg/m³) | stated | *"3 % higher than the highest measured value"* ⇒ 분쇄는 **사실상 완료**로 간주 |
| **벌크밀도 측정범위** | 1000 → 1800 kg/m³ | stated | 소형 실린더 부피·질량법 |
| **CB 등가입경 d₅₀ vs 벌크밀도** | **2.5 µm → 1 µm** (ρ_bulk 1000 → 1800 kg/m³) | stated | Lumisizer(LUM GmbH) 원심침강 + Stokes. ⚠ 저자 스스로 *"absolute values … of limited reliability"* (현탁 불완전 + NMC 표면에 붙은 CB 가 같이 침강) |
| **★ 그 관계의 피팅식** | **y = 2.72·x^(−1.86), R² = 0.81** (x = ρ_bulk [g/mL], y = d₅₀ [µm]) | **stated (그림 위에 인쇄)** | Fig 3(b). 벌크밀도가 분쇄도의 대리지표임을 정량화 |
| **비에너지 입력 e_tot 범위** | ≈ 1 → 10³ kJ/kg (ρ_bulk 1.05 → 1.8 g/mL) | digitized (Fig 3a, 로그축) | **TREND only** |
| **CB 추가 소요에너지 E_CB (Eq 6)** | `E_CB = E_total − E_idle − E_NMC` | stated | ⚠ 본문은 *"subtracting … the energy required without any material `E_empty`"* 라 쓰고 식에는 `E_idle` 로 적는다 — **같은 양의 두 이름**(표기 불일치) |
| **E_CB 초기값 (t≈1 min)** | **≈ 4.4 / 2.7 / 1.63 kJ/kg** (30 / 25 / 20 m/s) | digitized (Fig 4) | 90 min 에서 **≈ 0 으로 수렴** = 더 이상 분쇄 안 됨 |
| **★ 교반·분쇄 에너지 효율 η_cb (Table 2)** | **30 m/s: 0.58 → 0.02** · **25 m/s: 0.48 → 0.05** · **20 m/s: 0.42 → 0.00** (t_mix < 1 min → 90 min) | **stated** | `η_cb = E_CB / E_net`. ⇒ **권고: 최고 툴속도(30 m/s)로 돌려라** (에너지 이용률 최대) |
| **순수 NMC 기준런 질량** | **700 g** | stated | E_NMC 뺄셈용 |

### 3.4 시뮬 결과 (§4 — stated / digitized)

| 양 | 값 | stated/digitized | 비고 |
|---|---|---|---|
| **믹싱툴 파워 (시뮬 산출식)** | `P_tool = 2π n M` (n = 회전수/s, M = 툴 총토크 Nm) | stated | 실험은 Eirich 내장 토크계 직접측정, **무부하 파워를 뺀 순(net) 값** |
| **★ 검증 1 — P_tool vs 툴속도** | EL1.0·EL0.1, 5–30 m/s, **멱법칙 증가**; *"the trend is well captured"* | stated(정성) + digitized(Fig 5) | ⚠ **정량 일치는 주장하지 않는다.** 로그축에서 EL0.1 5 m/s 는 시뮬이 실험의 **약 2배** 로 읽힌다(digitized, 불확실) ⇒ **"추세 일치" 까지만** |
| **★ 검증 2 — P_tool vs 혼합시간** | 0.167 / 30 / 90 min × (30, 25, 20 m/s) 9점에서 **기호(시뮬)가 선(실험) 위에 거의 얹힌다** | digitized (Fig 6, 선형축) | 30 m/s: ≈72 → 39 → 33 W · 25 m/s: ≈57 → 32 → 27 W · 20 m/s: ≈46 → 22 → 19 W (**digitized, TREND**). ⚠ **반쯤 순환적 검증**임 — §10-③ |
| **★ 혼합품질 RSD 최종값 (용기 회전 시)** | **< 0.05** | stated | 85 rpm·170 rpm 모두. **툴속도 영향 미미** |
| **RSD 최종값 (용기 정지 0 rpm)** | **≈ 0.60 (40 m/s) / ≈ 0.67 (5 m/s)** | digitized (Fig 7b) | **10배 이상 나쁘다** ⇒ *"용기 회전이 균질화에 필수"* |
| **혼합 완료 시간** | **≈ 20 s** (용기 회전 시), 본문 결론은 *"within half a minute"* | stated | 최대 시뮬시간 30 s |
| **RSD₉₀ (자기 정상값의 90 % 도달시간, Table 3)** | 0 rpm **7.6 s**(40 m/s) / **2.7 s**(5 m/s) · 85 rpm **16.8 / 17.5 s** · 170 rpm **15.9 / 18.9 s** | **stated** | ⚠ **혼합품질 순위가 아니다** — 0 rpm 이 "가장 빨리" 도달하지만 그 도달점이 RSD 0.6 이다. 논문도 그렇게 해석(*"the majority of the albeit poor mixing result is already achieved within a very short mixing time"*) |
| **MSD / MSD₉₅ (Table 3)** | 40 m/s **0.040 / 0.070** · 5 m/s **0.030 / 0.050** (단위 인쇄 그대로 **m²/s**) | **stated** | ⚠ **Eq (8) 의 MSD 는 차원이 m² 인데 표는 m²/s** — 논문 내 단위 불일치. 인쇄된 대로 옮긴다 |
| **MSD 문헌 대조** | Hare 2023 (PEPT, 같은 EL1.0, **습식 음극 슬러리**, 6 m/s) **≈ 0.001 m²/s** | stated | ⚠ **한쪽 방향 타당성 논증뿐** — *"건식은 점성이 무시할 만하니 MSD 가 더 커야 하고, 실제로 크므로 타당"*. 정량 검증이 아니다 |
| **★ 전단율 최대** | **≈ 10 s⁻¹** | stated | *"one to two orders of magnitude lower compared to other types of mixers with comminution tasks, e.g. extruders"* — 이유 = Eirich 에는 **1 mm 이하 좁은 전단대가 없다** |
| **★ 전단율의 지배 인자** | **용기 속도가 평균 전단율을 ~100배 바꾼다**; **툴 속도의 영향은 작다** | stated | ⇒ **전단은 분쇄의 지배 기전이 아니다** 는 판정의 근거 |
| **★ 충돌속도 분포** | 툴 5 → 30 m/s 에서 상대충돌속도 분포가 **크게 우측이동** (30 m/s 에서 최대 ~33 m/s) | digitized (Fig 8b, 누적 Q₀) | *"a massive increase … a circumstance that remained hidden in the analysis of the shear rate"* ⇒ **충돌이 지배 기전** |
| **★ CGF 타당범위** | **CGF 100·150·200 일치** / **CGF 400 은 40 m/s 에서 어긋남** / **CGF 800 은 전 속도에서 어긋남** ⇒ *"not capable … for particle diameters bigger than 2 mm or a Coarse-Grain-Factor of 200"* | stated | **정규화 충돌률**(총입자수로 나눔) 기준. Fig 9(b) 에서 base(CGF200) ≈3.0 → 1.1 → 0.7 s⁻¹ (5/20/40 m/s), CGF800 ≈4.8 → 3.5 → 4.0 (digitized, TREND) |
| **★ 충돌률의 툴속도 의존 (모든 변형 공통)** | **툴이 빠를수록 충돌률이 *떨어진다*** | stated | 기전 = **원심(centrifuging)** — 툴이 재료를 자기 주변에서 밀어낸다 |
| **운전모드 (역류 counter-current)** | ≤20 m/s 에서 충돌률이 **유의하게 높음**, >20 m/s 에서 **동류(co-current)와 나란해짐** | stated | 저속에선 층높이가 낮아져 툴 근처 입자가 많아짐; 고속에선 유동화로 상쇄 ⇒ **에너지 관점 이득 없음** |
| **용기 경사 0·10·20·30°** | 충돌률 **거의 무영향**(약간 증가) | stated | 원심효과를 못 상쇄 |
| **★ 용기 속도 170 rpm vs 85 rpm** | 모든 툴속도에서 **충돌률 상승** | stated | 겉보기 역설 해소: 툴 주변 **체류량은 16–35 % 적지만**, 응력영역으로 **들어오는 질량유량이 56–98 % 증가** |
| **용기 0 rpm** | 충돌률이 85/170 rpm 대비 **크게 하락** | stated | *"should be avoided"* |
| **충전량 500 / 800(기준) / 1000 mL** | 정규화 충돌률 **1000 > 800 > 500** | stated | 채울수록 원심 탈출을 **입자층이 막아준다**. ⚠ **단 충돌 *에너지* 는 더 높은 충전에서 안 오른다** ⇒ *"최대 충전으로 분쇄하는 것이 유리하지 않을 수 있다"* (마찰손실 증가) |
| **툴 크기 75 / 100 / 125 %** | 클수록 충돌률 ↑; **125 % 는 20 m/s 이상에서 충돌률이 거의 평탄**(원심 저하가 사라짐) | stated | 위치 고정이라 125 % 는 벽간극이 좁아진다 |
| **핀 수 0 / 4 / 6 / 12** | **6개 초과는 유의한 증가 없음**; **0개가 가장 나쁨**(특히 저속) | stated | 툴 영역으로 **동시에 들어오는 재료량**이 한계라서 |
| **★ 블레이드 설계(6 핀 + 6 블레이드)** | **모든 툴속도에서 기준 대비 충돌률 상승** (digitized 로 **약 2–3배**) | stated(방향) + digitized(크기, Fig 17b) | 블레이드가 재료를 핀 영역으로 **밀어 넣어** 원심을 줄인다. ⚠ 직경이 커지므로 **같은 원주속도가 되게 회전수를 낮춰** 비교했다(공정한 비교) |
| **★★ 목표 벌크밀도 1400 kg/m³ 도달 혼합시간 단축** | **용기 170 rpm −20 %** · **툴 확대 −56 %** · **블레이드 설계 최대 −75 %** | **stated** | 선행연구에서 **1400 kg/m³ 가 최적 분쇄도**였음. Eq (5)+E_coll 로 환산 |
| **파워비 충돌률 n_coll = N_coll/P_tool** | 툴속도 증가에 따라 **단조 감소**; **거의 모든 변형이 같은 곡선 위에 겹침**(역류 5–15 m/s 만 약간 위) | stated | base ≈2e4 (5 m/s) → ≈6e2 s⁻¹W⁻¹ (40 m/s), digitized |
| **질량비 충돌에너지 e_coll** | 툴속도에 **단조 증가** (base ≈0.7 → ~9 → ~25 W/kg @ 5/20/40 m/s) | digitized (Fig 19a) | 40 m/s 에서 변형 간 산포 **~5 ~ ~60 W/kg** (최저 = 용기 0 rpm, 최고 = 블레이드) |
| **★ 파워비 충돌에너지 ε_coll = E_coll/P_tool** | **≈ 10 %** (전 툴속도) | stated | ⇒ **투입 파워의 ~90 % 는 분쇄에 못 쓰이고 마찰열·운동에너지로 간다.** base digitized ≈0.04(5 m/s) → ~0.15(20) → ~0.2(40) |
| **★ 최종 트레이드오프** | *"optimized design and operation parameters **may reduce mixing time but are not more efficient** … better comminution performance comes at the cost of higher absolute power usage"* | stated | **시간 ↔ 절대 전력의 교환**이지 효율 개선이 아니다 |

### 3.5 ⛔ 이 논문이 **내지 않는** 것 (질문 6 의 직답)

| 양 | 유무 | 근거 |
|---|---|---|
| **porosity / 공극률** | ⛔ **없음** | 전문에 `poros` 가 **참고문헌 제목(Mayer 2022)에서 단 한 번**만 등장. 압밀 단계 자체가 없다 (믹서는 분말을 *섞고 부술 뿐* 누르지 않는다). 나오는 밀도량은 **벌크밀도**뿐이고 그것도 **실험 입력**이지 시뮬 출력이 아니다 |
| **σ_ionic / σ_e / σ_thermal** | ⛔ **없음 — 전달 솔버 0채널** | `conduct` 는 전부 *conductive additive*(도전제) 또는 선행연구 언급. 본 논문 §1 이 *"short but intensive mixing led to optimal electrical conductivity of the cathode powder materials"* 라고 **선행(Lischka 2024)** 을 인용할 뿐 **이 논문에는 σ 값이 한 개도 없다** |
| **tortuosity / percolation / coordination** | ⛔ **없음** | `tortuos` 0회. 접촉망 기술자(descriptor) 자체가 없다 |
| **전기화학 (용량·율특성·셀)** | ⛔ **없음** | 셀을 만들지 않는다. 성능 대리지표는 **벌크밀도(=분쇄도)** 하나 |
| **입자 파쇄(breakage) 시뮬** | ⛔ **없음** | DEM 이 입자를 깨지 않는다. 분쇄는 **파라미터로 번역해 넣는다**(§4.5). 충돌에너지는 *"the upper limit for the energy that can be converted to break"* = **상한 프록시**일 뿐 |
| **입자 형상 소성 / 형상 변화** | ⛔ **없음** | 강체 구 |
| **응집(agglomeration) 지표** | ⛔ **없음** (⚠ 질문 3·4 의 핵심) | 응집체가 **깨지는 쪽**만 다루고, **상별로 어디에 뭉치는가**는 전혀 재지 않는다. 지표는 RSD(라벨 분산) 하나 |

---

## 4. 시뮬레이션 방법 ★

### 4.0 전체 구조 (한 문단)
**Eirich EL1.0 / EL0.1 의 실제 기하(회전 믹싱툴 + 회전 용기 + 고정 벽 스크레이퍼)를 그대로 DEM 도메인으로 넣고**, 그 안에 **NMC622+CB 혼합물을 대표하는 단일 종 coarse-grain 입자(CGF 200, d = 2.0 mm)** 를 채운 뒤, 툴속도·용기속도·경사·충전량·툴 형상을 바꿔 가며 **준정상 유동(≥30 s)** 을 만든다. 그 위에서 **① 믹싱툴 토크 → 소비전력**(실험 검증 축), **② 라벨 기반 혼합지수 RSD·MSD**, **③ 툴과의 충돌 빈도·충돌 속도 → 충돌에너지**(후처리 식으로 환산), **④ 속도장 → 전단율장**을 뽑는다. **분쇄 자체는 시뮬하지 않고**, 실험에서 측정한 분쇄 단계(벌크밀도)를 **입력 파라미터 집합으로 번역해 다시 넣는 방식**(Table 1)으로 시간의존성을 재현한다.

### 4.1 code · 버전 · 하드웨어 · 수치 (stated)
- **DEM 코드 = `EDEM 2022.3`** (Altair, 상용 GPU DEM). ⇒ 우리 **LIGGGHTS** 와 다른 코드이고, Frankenberg 의 **Rocky 2023 R1** 과도 다르다 (믹서 DEM 3편 = 3개의 서로 다른 상용/오픈 코드).
- **하드웨어 = Nvidia RTX-2080Ti GPU** 1장. ⚠ **충돌 이벤트 평가만은 CPU 에서** 돌린다 — *"the evaluation of every collision event is computationally expensive and must be performed on CPUs instead of faster GPUs"* ⇒ 그래서 충돌 통계는 **유동이 완전히 발달한 뒤 1 초 구간**만 평가한다.
- **timestep = Rayleigh time step 의 20 %** (정확도-속도 절충).
- **런 길이**: *"until a quasi-static flow behaviour was established … usually achieved after a simulation time of at least 30 s"*. RSD 평가의 최대 시뮬시간도 **30 s**.
- **연속체 보간**: 전단율을 얻기 위해 입자 데이터를 **소프트웨어 내장 가우시안 가중함수**로 속도장으로 보간한다(§4.8 의 Eq 9 입력). ⚠ **가우시안 폭(커널 반경)·격자 간격이 논문에 없다** ⇒ 전단율 절대값의 격자의존성이 **미보고**.

### 4.2 ★ 접촉·점착 모델 — **JKR**, 그리고 그 외에는 (질문 2 의 직답)
- **점착 모델 = JKR (Johnson–Kendall–Roberts)** — 본문 §2.2: *"When using the Johnson-Kendell-Roberts (JKR) contact model the work of cohesion is given by …"*. **표면에너지 γ 의 단위 = J/m²** 로 명시.
- ⚠ **탄성 base 접촉법칙의 이름이 본문에 없다.** 전문에 `Hertz` · `Mindlin` 이라는 낱말이 **0회**다. EDEM 의 표준 구현이 *Hertz–Mindlin with JKR cohesion* 이므로 그것일 가능성이 높으나 **논문이 그렇게 적지 않았으므로 우리 카드는 "JKR(점착) + 이름 없는 탄성 접촉" 까지만 적는다.** (E\*·ν 가 Eq 2 유도에 등장하므로 Hertz 계열 탄성인 것은 확실하다.)
- **소성·항복 캡 없음** — Thornton–Ning 류 항복분기도, hooke/hysteresis 류 이력도 **없다**. 이 논문은 압밀이 아니라 유동·충돌을 풀기 때문에 소성이 필요 없다.
- **마찰**: 정마찰·동마찰을 **입자-입자(p-p)와 입자-벽(p-w) 두 쌍**으로 따로 준다 (Table 1 네 열). **구름마찰(rolling friction)** 은 본문이 보정 대상으로 *언급*하나 **값이 이 논문에 없다**(선행 2023 논문 소관).
- **COR = 0.5, 모든 케이스 고정** — 근거는 *"very difficult to obtain experimentally for pure substances and basically impossible to measure for a mixture of two different species in a bulk at the same time"* ⇒ **측정 불가라서 가정한 값**. ★ 이 COR 이 충돌에너지 식 Eq (4) 에 `(1−k²)` 로 직접 들어가므로 **충돌에너지 절대값은 이 가정값에 걸려 있다**(k=0.5 → 1−k² = 0.75; 만약 k=0.3 이면 0.91 로 +21 %).
- **전단탄성률 G = 1e8 Pa 로 인위적으로 낮춤** — 이유가 명시적으로 **계산비용**이다 (*"to minimize the computational cost associated with higher shear moduli"*). ★★ **이것은 우리 18× E-연화와 *동기가 다른* 같은 종류의 조작**이다: 우리는 *강체구가 못 하는 입상 재배열을 럼핑*하려고 낮췄고, 이들은 *timestep 을 키우려고* 낮췄다. 둘 다 "DEM 강성은 물성이 아니라 운용 노브" 라는 사실의 사례이고, 그래서 **이 논문의 G 를 물성으로 인용하면 안 된다**.

> ★★ **상별(phase-pair) 점착 행렬이 있는가? — 없다.** 입자종이 **하나뿐**(NMC+CB 를 합친 CG 입자)이라 점착 파라미터는 **γ_pp 1개 + γ_pw 1개**로 끝이다. **우리의 3×3 `coefficientAdhesionStiffness`(AM–AM / AM–SE / SE–SE)에 대응하는 구조가 이 논문에는 존재하지 않는다.** 유일하게 "쌍마다 다른" 것은 **입자↔벽** 이고, 그조차 독립 자유도가 아니라 **γ_pw = γ_pp/6 으로 묶여 있다**(§3.2 실측). ⇒ 질문 2 의 *"상별로 다르게 주는가"* 답 = **아니오**.

### 4.3 ★★ cohesion number — 입경이 바뀔 때 γ 를 어떻게 바꾸나 (질문 2·7 의 심장)

**동기 (본문 §2.2 원문 취지)**: γ 는 **2 mm DEM 입자에 대해 실험으로 보정**한 값이다. 그런데 CGF 를 바꾸려고 입경을 바꾸면 **표면적/부피 비가 달라져** 같은 γ 가 같은 거동을 주지 않는다. 그래서 **Behjani et al. (2017) 의 cohesion number 를 불변량으로 삼아** γ 를 재계산한다.

**정의 (Eq 1)**
```
Cohesion number = (work of cohesion) / (gravitational potential energy)
```

**JKR 점착일(work of cohesion)** — 본문 인쇄 그대로
```
W_coh = 7.09 · ( γ⁵ · R*⁴ / E*² )^(1/3)
```
- `γ` = 접촉하는 두 재료 사이 **표면에너지 [J/m²]**
- `R* = (1/R₁ + 1/R₂)⁻¹` = 등가반경
- `E* = ( (1−ν₁²)/E₁ + (1−ν₂²)/E₂ )⁻¹` = 등가 영률
- `g` = 중력가속도

**중력 퍼텐셜에너지** = `m g R*` = `ρ R*³ g R*` = `ρ g R*⁴`

**최종형 (Eq 2)**
```
Coh = (1/(ρ g)) · ( γ⁵ / ( E*² · R*⁸ ) )^(1/3)
```
*(7.09 상수는 상수라 Eq 2 에서 빠졌다. 위 두 식을 나눠 보면 정확히 Eq 2 가 나온다 — 우리 검산 통과.)*

**★ 그래서 스케일링 규칙 (우리 유도, ρ·E\* 고정 가정)**
```
Coh = const   ⇒   γ⁵ ∝ R*⁸   ⇒   γ ∝ R*^(8/5) = R*^1.6
```
⇒ **입자를 크게 만들면 γ 를 R^1.6 으로 키워야 "같은 만큼 점착성인" 분말이 된다.** 물리적 의미는 자명하다 — 작은 입자가 본래 더 점착적(표면/부피)이므로, 그 *무차원 점착성* 을 보존하려면 큰 입자에 더 큰 γ 를 줘야 한다.

**벽 처리 (stated)**: 벽은 반경을 정의할 수 없다 — *"the diameter of the wall can not be set to a meaningful value since the contact area would be very large … This would result in unrealistically high surface energies."* ⇒ **벽에는 Eq 2 를 적용하지 않고, 입자-입자에서 나온 *스케일 인자를 그대로 가져다* 2 mm 기준 벽 값에 곱한다.** 우리 실측으로 이 규칙은 **γ_pw = γ_pp/6 을 전 행에서 유지**하는 것으로 나타난다(§3.2).

**저자 자신의 한계 선언 (★ 우리에게 가장 중요한 문장)**
> *"Although the cohesion number would theoretically allow to calculate the cohesion work of the **real world** particle system, we use it here to calculate the necessary surface energy γ when scaling our calibrated DEM simulation model for a study of the Coarse Grain Factor. One difficulty of using it for the real particle system lies primarily in the fact that **the surface energy between NMC and NMC particles is unknown and difficult to measure**."*

⇒ **즉 저자들은 "실제 입자의 γ 로부터 CG γ 를 얻는" 방향을 *명시적으로 포기*하고, "보정된 CG γ 끼리 서로 옮기는" 좁은 용도로만 쓴다.** (§B-2 에서 우리 prereg 에 대한 함의를 정리한다.)

**⚠ 우리 검산 3건 (전부 §3.2 표에 수치)**
1. Table 1 의 다섯 행은 단일 지수 1.6 으로 **정확히 재현되지 않는다**(유효지수 1.61–1.84). 논문이 Eq 2 안의 ρ 처리를 안 적었고 ρ 가 행마다 변한다.
2. 논문이 *"Table 1 gives these values"* 라 한 **CGF 150·100 의 γ 가 Table 1 에 없다** ⇒ Fig 9 CGF 스윕은 **재현 불가**.
3. 이 규칙을 실제 10 µm 입자까지 밀면 γ_real ≈ **6.3e-5 J/m²** 로 **비물리적으로 작다** ⇒ cohesion-number 는 **CG 크기들 사이의 내삽 규칙**이지 **실물 γ 로 가는 다리가 아니다**(저자 선언과 일치).

**⛔ 질문 7 의 직답 — `γ ↔ linear adhesion stiffness k_c` 환산식은 이 논문에 없다.**
이 논문의 점착 노브는 **JKR 의 표면에너지 γ [J/m²] 하나**다. 선형 점착강성(스프링형 `k_c`, N/m 또는 우리의 `coefficientAdhesionStiffness`)은 **한 번도 등장하지 않으며**, 둘을 잇는 식·표·부록도 **없다**. ⇒ **우리 `m7` 을 이 논문의 γ 에 접지할 직접 경로는 없다.** (간접적으로 무엇이 가능한지는 §B-2.)

### 4.4 ★ coarse-graining (CGF) — 질문 1 의 규모 축
- **왜**: 실제 계는 *"particle sizes … of active material NMC and carbon black in the order of μm to nm"* 이라 그대로는 풀 수 없다. 그래서 *"simulation particles are made larger by a constant Coarse Grain Factor (CGF) than reality"*.
- **기준(base) = CGF 200, d = 2.0 mm** ⇒ **대표 실제입경 ≈ 10 µm** (우리 유도, 5개 CGF 에서 교차확인).
- **스윕**: 아래로 **CGF 150 (1.5 mm) · CGF 100 (1.0 mm)**, 위로 **CGF 400 (4 mm) · CGF 800 (8 mm)**. 툴속도 **5 / 20 / 40 m/s** 세 점에서 비교.
- **비교량 = 총입자수로 정규화한 충돌률** `N_coll,norm` (입자수가 CGF 마다 다르므로 필수).
- **판정 (stated)**: CGF **100·150 은 기저와 높은 일치** ⇒ *"a reduced calculation effort due to the increase in particle size leads to comparable results"*; CGF **400 은 40 m/s 에서 어긋남**; CGF **800 은 전 속도에서 어긋남** ⇒ **"d > 2 mm (CGF > 200) 은 쓸 수 없다"**.
- ★ **유동장 자체는 CGF 에 둔감**: Fig 9(a) 에서 툴·스크레이퍼 주변 유동 형상이 CGF 200/150/100 에서 *"very similar"*, 다만 **해상도만** 미세하게 좋아진다.
- ⚠ **이 CGF 판정의 신뢰도를 깎는 두 가지**: ① 위에서 적은 대로 **각 CGF 에 실제로 들어간 γ 가 보고되지 않았다** ⇒ "CGF 100–200 일치" 가 *기하 덕인지 γ 재계산 덕인지* 분리 불가. ② **CGF 400·800 은 애초에 물리 격자가 아니라 "어긋남을 유도하려고 일부러 넣은 프로브"** 라고 저자가 적는다(*"to induce deviations from the base case"*) — 즉 상한은 **아래로부터 확인**된 것이 아니라 **위로 밀어서 깨뜨려 본** 것이다.

### 4.5 ★ 입자 처리 (DEM판 "무질서 처리") — 질문 4 의 직답
| 축 | 이 논문 |
|---|---|
| **형상** | **구(sphere)만**. 비구형 대리(다구형/superquadric) 언급 **없음** |
| **PSD** | **단분산**. Table 1 은 상태마다 **단일 직경** 하나만 준다 (2.0 / 1.757 / 1.768 / 1.772 / 1.723 mm). 분포 폭·표준편차 **없음** |
| **★ 성분 구성** | ⛔ **단일 종.** *"The individual simulated particles **contain a mixture of NMC622 and carbon black material**"* — **NMC 와 CB 가 각각의 DEM 입자가 아니라, 한 입자 안에 섞여 들어가 있다.** ⇒ **다성분 DEM 이 아니다.** 상별 거동(어느 상이 어디에 모이나)은 **원리적으로 나올 수 없다** |
| **★ 소성** | **없음**(강체 구, 형상 불변). 겹침 δ 는 기하 프록시 |
| **파쇄** | **없음**. 분쇄는 **파라미터 번역**으로만 표현 — *"The influence of the comminution of the carbon black agglomerate structures is reflected by a change in **particle size**, an increase in the **bulk density** and a reduction in the **coefficient of friction**"* (Fig 2a 모식: 혼합시간↑ → 벌크밀도↑ → DEM 입경↓ → 마찰↓) |
| **초기 구조** | 혼합 시뮬은 **완전 분리 상태(RSD = 1)** 에서 출발. Fig 7(a) 로 보면 **두 색 층이 상하로 쌓인 초기조건** |
| **경계** | 실제 믹서 기하 전체(도메인 축소·주기경계 언급 **없음**) |

> ★★ **이것이 "혼합 DEM" 으로서 이 논문의 가장 큰 구조적 한계다.** 입자가 한 종이므로 **이 모델은 "혼합" 을 *서로 다른 재료가 섞이는 것* 으로 풀지 않는다.** 뒤의 RSD 는 그래서 **물성이 같은 입자 절반에 라벨을 붙여 그 라벨이 퍼지는 속도**를 잰다(§4.6). ⇒ **표면에너지 차이가 상별 응집을 만드는가** 라는 우리 `m7` 의 질문은 **이 논문의 사정권 밖**이다. (⚠ 두 라벨 집단의 물성이 서로 다르다는 서술은 논문 어디에도 없고 Table 1 은 단일 파라미터 세트만 준다 — 그래서 우리는 "동일 물성 + 라벨" 로 읽는다.)

### 4.6 ★ 혼합 지표 — RSD 와 MSD (질문 3 의 직답)

**(a) 상대표준편차 RSD (Eq 7)**
```
RSD(t) = sqrt( (1/n_s) · Σ_{n=1..n_s} ( x_i(t) − x_t )² )  /  x_t
```
| 입력 | 값·규약 | 비고 |
|---|---|---|
| `n_s` = 표본(샘플 bin) 수 | **≥ 100** | stated |
| `x_i(t)` = 표본 내 현재 농도 | — | Fig 7(a) 캡션: *"blue grid shows the used sample bins"* ⇒ **공간 격자로 나눈 bin** |
| `x_t` = 목표 농도 | **0.5, 모든 시뮬 동일** | ⇒ **50 : 50 두 집단** |
| 표본당 입자수 `s` | **≥ 400** | stated |
| 무작위혼합 하한 | `RSD_s = x_t(1−x_t)·(1/s) = 0.25/400 = ` **0.000625** | stated |

⚠⚠ **격자·표본 의존성에 대한 우리 판정 3건**
1. **`RSD_s` 는 RSD 가 아니라 분산이다.** `x_t(1−x_t)/s` 의 차원은 `x` 의 제곱이다. 같은 척도(RSD)로 바꾸면 `√(6.25e-4)/0.5 = ` **0.05**. ⇒ 논문의 *"RSD < 0.05 는 RSD_s 보다 훨씬 위(=나쁨)"* 는 **단위 혼동**이고, 올바르게 맞추면 **회전용기 케이스는 무작위혼합 한계에 도달했다**(논문 주장보다 좋은 결과). 반드시 이 정정을 달아 인용할 것.
2. **`s` 가 RSD 하한을 직접 정한다** (`RSD_r = √((1−x_t)/(x_t·s))`). `s = 400` → 0.05; `s = 40` → 0.158; `s = 4000` → 0.0158. ⇒ **bin 을 얼마나 잘게 쪼개느냐로 "혼합 완료" 판정선이 통째로 움직인다.** 논문은 `s ≥ 400`·`n_s ≥ 100` 이라는 **하한만** 주고 **실제 bin 크기·개수·배치를 적지 않았다** ⇒ RSD 절대값은 **재현 불가**, **같은 논문 안의 arm 간 상대비교만 안전**.
3. **bin 이 회전 용기와 함께 도는지(라그랑주) 고정인지(오일러) 불명.** 회전 용기에서는 이 선택이 RSD 에 직접 들어간다.

**(b) 평균제곱변위 MSD (Eq 8)**
```
MSD(t) = ⟨(x(t)−x(0))²⟩ + ⟨(y(t)−y(0))²⟩ + ⟨(z(t)−z(0))²⟩
```
- **평균 `MSD̄` 와 95퍼센타일 `MSD₉₅` 를 함께** 보고한다 — 이유 명시: *"since the ensemble average hides the underlying distribution character"*. ★ **좋은 습관 — 우리도 enrichment 를 평균만 적지 말 것**(§B-3).
- ⚠ Eq (8) 의 차원은 **m²** 인데 Table 3 단위는 **m²/s** — **논문 내 불일치**. 인쇄된 대로 옮긴다.

**(c) RSD₉₀ 지표의 함정 (우리 판정)** — `RSD₉₀` = *"자기 정상값의 90 % 에 도달하는 시간"*. 정상값이 arm 마다 다르면 **품질 순위가 아니다**. 실제로 0 rpm 이 가장 "빠른데"(2.7–7.6 s) 도달점이 RSD ≈ 0.6 이다. **우리가 어떤 수렴시간 지표를 만들 때 반드시 피해야 할 정의 형태.**

### 4.7 ★ 믹서 기하·운전조건 (질문 1 의 기하 축)

| 항목 | 값 (stated) |
|---|---|
| **장비** | Eirich **EL1.0** (최대 1 L) · **EL0.1** (최대 0.1 L). 검증은 둘 다, **상세 해석은 EL1.0 만** |
| **구성 요소 (Fig 1)** | ① **고속 회전 믹싱툴**(편심 설치) ② **회전 믹싱 용기** ③ **고정 벽 스크레이퍼**(재료를 툴 영역으로 밀어 넣는 역할) |
| **툴 형상 (기준)** | **"Z-Wirbler"**, **아래로 향한 핀**. 구성 = **반경방향 이빨 12개 + 수직 핀 6개(표준)**. **핀과 용기 바닥 간격 ≈ 2 mm** |
| **툴 원주속도 w_tool** | 실기 **5 – 30 m/s**. ★ **시뮬은 40 m/s 까지** — *"we use a higher maximum tool speed for the simulations in order to evaluate even higher energy inputs"* ⇒ **40 m/s 결과는 장비 범위 밖의 외삽** |
| **용기 회전수** | **85 rpm · 170 rpm** (실기 2단) + **0 rpm**(시뮬 전용 대조) |
| **운전 모드** | **동류(co-current)** = 실험·기준 / **역류(counter-current)** = 시뮬 전용 |
| **용기 경사** | 0° → **30°, 10° 간격** (0/10/20/30) |
| **충전 부피** | **800 mL 기준**(실험과 동일) · 500 mL · 1000 mL |
| **툴 크기 스케일** | **75 % · 100 %(기준) · 125 %** — **위치는 고정**하므로 125 % 는 벽간극이 좁아지고 75 % 는 넓어진다 |
| **툴 핀 수** | **0 · 4 · 6(기준) · 12** |
| **신설 설계** | **6 핀 + 6 블레이드** — 핀 주위에 블레이드를 둘러 재료를 핀 영역으로 **밀어 넣는다**. ★ 직경이 커지므로 **회전수를 낮춰 같은 원주속도로 맞춰 비교** |
| **재질** | 용기·내장품 모두 **스테인리스강** |
| **전단율 평가면** | **툴 최대 원주속도에 해당하는 높이의 수평 단면** |
| **충돌 평가창** | 유동 완전발달 후 **1 초**, CPU 에서 |

### 4.8 충돌에너지·전단율 후처리 식 (stated)

**충돌에너지 (Eq 3 → Eq 4)**
```
E_coll = [ m_part · m_mt / (2 (m_part + m_mt)) ] · v_rel² · (1 − k²)        (3)
m_part + m_mt ≈ m_mt   (툴 질량 ≫ 입자 질량)
E_coll = (m_part / 2) · v_rel² · (1 − k²)                                   (4)
```
- `v_rel` = **법선방향 상대충돌속도**, `k` = COR = **0.5 고정**.
- **DEM 소프트웨어의 직접 출력이 아니다** — 충돌 이벤트마다 후처리로 계산해 **1 초 구간 합산**.
- ★ **해석 규약**: 법선방향 소산에너지를 *"the **upper limit** for the energy that can be converted to break the carbon black aggregate and agglomerate structures"* 로 본다(Rumpf 1959 · Burmeister 2018). ⇒ **분쇄량이 아니라 분쇄에 쓸 수 있는 에너지 상한**.

**전단율 크기 (Eq 9)**
```
|γ̇| = sqrt( 2(du/dx)² + 2(dv/dy)² + 2(dw/dz)²
            + (du/dz + dw/dx)² + (du/dy + dv/dx)² + (dw/dy + dv/dz)² )
```
입력 = 입자 데이터를 **가우시안 가중으로 보간한 연속 속도장**. ★ 장점으로 저자가 든 것: *"the shear forces relevant for the comminution … are summarized in a single scalar quantity."*

**벌크밀도-에너지 모델 (Eq 5, Schilde 이식)** · **CB 추가에너지 (Eq 6)** · **효율 η_cb = E_CB/E_net** → §3.3.

### 4.9 전달 솔버 — **없음**
전기전도도·이온전도도·열전도도·유효물성 어느 것도 풀지 않는다. **성능의 유일한 대리지표는 벌크밀도(= CB 분쇄도)** 이고, 그것이 전극 성능과 연결된다는 근거는 **선행 문헌 인용**(Bockholt 2013 · Mayer 2020·2022 · Wenzel 2014 · Lischka 2024)으로만 제공된다.
---

## 5. Figure set ★ (전 19개 — 무엇을 보여주나 / 우리가 쓸 수 있나)

| Fig | 내용 | 우리가 참고할 점 | 우리 쓸모 |
|---|---|---|---|
| **1** | Eirich EL1.0 **기하 스케치** — 회전 믹싱툴(편심) + 회전 용기 + 고정 벽 스크레이퍼 | 집약형 믹서의 3요소. 우리에겐 **이런 기하가 아예 없다**(`insert/pack` → 정착 → 플래튼) | 🔸 개념 |
| **2(a)** | ★ **coarse-grain 모식** — 한 CG 입자 안에 회색 NMC + 검은 CB 알갱이. 화살표: **혼합시간↑ / 벌크밀도↑ / DEM 입경↓ / 마찰↓** | ★ **"분쇄를 시뮬하지 않고 파라미터로 번역한다" 는 설계 철학이 한 컷에 있다.** 우리가 *m7* 결과를 "공정 단계" 로 번역할 때의 참고형 | 🔸🔸 개념 |
| **2(b)** | ★★ **보정 실험 4종 콜라주** — ① **정적 안식각**(분말 더미 사진 + 시뮬, **2.0 / 1.5 / 1.0 mm 세 CG 크기 비교 이미지 포함**) ② **링전단시험기 Schulze RST-01** (τ–σ 선도, Experiment vs Simulation) ③ **경사판(inclined plate), 스테인리스** = 벽마찰 ④ **동적 안식각**(회전드럼 + τ vs 무차원시간, Exp vs Sim) | ★★ **γ 의 CG 스케일링이 *실제로 검증된 유일한 자리*** — 세 입경에서 같은 안식각이 나온다는 것. ⚠ **단 이 논문에는 그 숫자가 없다**(전부 선행 2023 논문 위임) | 🔸🔸🔸 방법 |
| **3(a)** | 실험: **비에너지 입력 e_tot vs 벌크밀도** (로그 y, 1→10⁴ kJ/kg), 측정점 + **Schilde 모델(Eq 5) 적합** | ★ **공정 에너지 ↔ 분말 상태의 정량 다리**. 우리 압밀에는 없는 축(우리는 압력↔porosity) | 🔸🔸 데이터 |
| **3(b)** | 실험: **CB 등가입경 d₅₀ vs 벌크밀도**, 적합식 **y = 2.72 x^(−1.86), R² = 0.81** (그림 위 인쇄) | ★ **stated 피팅식** — 벌크밀도가 분쇄도의 대리임을 정량화. 단 Lumisizer 절대값 신뢰도는 저자가 스스로 깎음 | 🔸🔸 데이터 |
| **4** | 실험: **CB 추가에너지 E_CB vs 혼합시간**(로그 x, 1→100 min), 30/25/20 m/s 세 곡선. 4.4 / 2.7 / 1.63 → ~0 kJ/kg | 분쇄가 **초기에 싸고 나중에 비싸다**(거친 입자가 먼저 깨짐) + 초기 마찰손실이 큼 | 🔸 데이터 |
| **5(a)(b)** | ★ **검증 1**: 툴 파워 `P_tool`(W) 및 질량비 파워 `p_tool`(W/kg) **vs 툴속도**, EL1.0(△ exp / 파선 sim) + EL0.1(○ exp / 실선 sim), 로그 y | ★ **"추세는 잡히나 절대값은 어긋날 수 있다" 의 정직한 제시**. 로그축에서 EL0.1 5 m/s 는 sim 이 exp 의 ~2배로 읽힌다(digitized) | 🔸🔸 검증 |
| **6** | ★★ **검증 2**: `P_tool` **vs 혼합시간**(0.167/30/90 min) × 3 툴속도, **선 = 실험(누적 에너지에서 유도)**, **기호 = 시뮬**, 오차막대 포함, 선형 y | ★ 9점이 거의 겹친다 = 가장 강해 보이는 검증. ⚠ **그러나 반쯤 순환적**(§10-③) — 밀도·충전높이가 실측으로 고정되고 마찰이 "파워가 맞게" 조정됨 | 🔸🔸 검증 |
| **7(a)** | ★ **혼합 스냅샷 3×2** — 툴 5 vs 40 m/s × 용기 0/85/170 rpm, 30 s 시점. **두 색 입자**(초기 상하 2층) + **파란 격자 = 표본 bin** | ★★ **"혼합" 의 정체가 여기서 드러난다 — 두 색은 *서로 다른 재료가 아니라 라벨*이다.** 5 m/s·0 rpm 에서 검은 층이 바닥에 그대로 남아 있는 것이 보인다 | 🔸🔸🔸 방법 |
| **7(b)** | ★★ **RSD vs 무차원 혼합시간**, 6 곡선(40·5 m/s × 0·85·170 rpm) | ★★ **핵심 결과 1**: 회전용기 3쌍은 전부 <0.05 로 수렴, 0 rpm 2쌍은 **0.6–0.67 평탄** ⇒ **용기 회전이 지배**, 툴속도는 2차 | 🔸🔸🔸 결과 |
| **8(a)** | ★ **전단율 크기 누적분포 Q₀**(로그 x, 1e-7 → 10 s⁻¹), 4곡선(5·40 m/s × 0·170 rpm) | ★★ **핵심 결과 2**: 최대 **10 s⁻¹**, 압출기 대비 1–2자릿수 낮음. **용기속도가 평균을 ~100배 옮기고 툴속도는 거의 안 옮긴다** ⇒ 전단은 지배 기전이 아니다 | 🔸🔸🔸 결과 |
| **8(b)** | ★ **툴과의 상대충돌속도 누적분포**, 6곡선(5→30 m/s) | ★★ **핵심 결과 3**: 툴속도가 충돌속도 분포를 **크게** 옮긴다 — *"a circumstance that remained hidden in the analysis of the shear rate"* ⇒ **충돌이 지배 기전** | 🔸🔸🔸 결과 |
| **9(a)** | CGF 200/150/100 × 툴 5/20/40 m/s **유동장 9컷** | 유동 형상은 CGF 에 둔감, **해상도만** 좋아진다 | 🔸 방법 |
| **9(b)** | ★★ **정규화 충돌률 vs 툴속도**, CGF 100/150/200/400/800 | ★★ **CGF 상한을 수치로 그은 자리**. 100·150 은 200 과 겹침, 400 은 40 m/s 에서 이탈, 800 은 전역 이탈 ⇒ **CGF ≤ 200** | 🔸🔸🔸 방법 |
| **10(a)(b)** | **운전모드**(동류/역류): 유동장 + 충돌률 | ≤20 m/s 에서 역류가 유리(재료 높이가 낮아져 툴 근처 밀도↑), >20 m/s 에서 유동화로 상쇄 | 🔸 결과 |
| **11(a)(b)** | **용기 경사 0/10/20/30°**: 유동장 + 충돌률 | **거의 무영향** — 원심효과를 못 이긴다 | 🔸 결과 |
| **12(a)(b)** | ★ **용기 속도 0/85/170 rpm**: 유동장 + 충돌률 | ★ **겉보기 역설의 해소**: 170 rpm 은 툴 주변 *체류량*이 16–35 % 적은데 *유입 질량유량*이 56–98 % 많아 충돌률이 높다 ⇒ **"얼마나 있나" 가 아니라 "얼마나 지나가나"** | 🔸🔸 결과 |
| **13(a)(b)** | **충전량 500/800/1000 mL**: 유동장 + 정규화 충돌률 | 충전이 높을수록 **입자층이 원심탈출을 막아** 충돌률↑. ⚠ 단 충돌 *에너지* 는 안 따라 오름(마찰손실) | 🔸 결과 |
| **14** | **툴 크기 75/125 % 도면** | 위치 고정 → 벽간극이 함께 바뀜(교락 인자) | 🔸 방법 |
| **15(a)(b)** | ★ **툴 크기 영향**: 유동장 + 충돌률 | **125 % 는 20 m/s 이상에서 충돌률이 평탄** = 원심 붕괴가 사라짐 ⇒ **툴/용기 비가 설계 노브** | 🔸🔸 결과 |
| **16** | **핀 수 0/4/6/12 툴 도면** + 블레이드 설계 | 형상 변형 목록 | 🔸 방법 |
| **17(a)(b)** | ★ **툴 설계 영향**: 유동장(0핀 / 6핀 / 6핀+6블레이드) + **절대 충돌률 N_coll**(로그 y) | ★ **6핀 초과는 이득 없음**(동시에 유입되는 재료가 한계), **0핀이 최악**, **블레이드가 전 속도에서 최고**(digitized ~2–3배) | 🔸🔸 결과 |
| **18** | ★ **파워비 충돌빈도 n_coll = N_coll/P_tool vs 툴속도**, 13개 변형 전부 한 그림 | ★★ **거의 모든 변형이 한 곡선 위에 겹친다** ⇒ *"설계·운전을 바꿔 절대 충돌률을 올려도 **파워당 효율은 안 오른다**"*. 역류 5–15 m/s 만 예외적으로 위 | 🔸🔸🔸 결과 |
| **19(a)** | ★ **질량비 충돌에너지 e_coll (W/kg) vs 툴속도**, 13 변형 | 툴속도에 **단조 증가**(원심으로 *빈도* 는 떨어져도 *에너지* 는 오른다 — 빈도×속도² 의 경쟁에서 속도²가 이긴다). 40 m/s 산포 ~5 ~ ~60 W/kg | 🔸🔸 결과 |
| **19(b)** | ★★ **파워비 충돌에너지 ε_coll = E_coll/P_tool vs 툴속도** | ★★ **≈ 10 %** — **투입 파워의 ~90 % 가 분쇄에 못 쓰인다**. 저속일수록 변형 간 산포가 큼(= 저속에서 설계가 더 민감) | 🔸🔸🔸 결과 |

## 6. Post-processing ★

- **무엇을 계산하나**
  - **믹싱툴 토크 → 파워**: `P_tool = 2πnM`, 시간평균. **실험은 Eirich 내장 토크계의 net 값**(무부하 차감) — 비교 규약이 맞춰져 있다.
  - **혼합지수 RSD (Eq 7)**: 공간 bin(≥100개, 각 ≥400 입자) 안의 라벨 농도 `x_i` 를 목표 `x_t=0.5` 와 비교. 무차원 혼합시간으로 플롯.
  - **MSD / MSD₉₅ (Eq 8)**: 평균과 95퍼센타일 **둘 다**.
  - **충돌 빈도**: 툴과의 **완료된 접촉 수/초**, 유동 발달 후 **1 초** 창. 필요하면 **총입자수로 정규화**(CGF·충전량 비교 시 필수).
  - **충돌 에너지 (Eq 3→4)**: 이벤트별 법선 상대속도로 계산 후 **초당 합**.
  - **전단율장 (Eq 9)**: 가우시안 가중 보간 속도장의 **스칼라 크기**, 툴 최대원주속도 높이의 **수평 단면**에서 누적분포 Q₀ 로.
  - **파생 효율 2종**: `n_coll = N_coll/P_tool` (파워비 빈도) · `ε_coll = E_coll/P_tool` (파워비 에너지) · 실험측 `η_cb = E_CB/E_net`.
  - **혼합시간 환산**: `E_coll` 과 Eq (5) 를 결합해 **목표 벌크밀도(1400 kg/m³) 도달 혼합시간**을 계산 → 변형별 **단축률(%)**.
- **도구**: DEM = **EDEM 2022.3**(GPU) + **CPU 에서 충돌 이벤트 후처리**. 연속체 보간은 **EDEM 내장 가우시안 가중**. 실험 = Eirich 내장 토크계 · 소형 실린더 벌크밀도 · **Lumisizer (LUM GmbH)** 원심침강 입도 · (선행 논문) 링전단셀 Schulze RST-01 · 회전드럼 · 경사판.
- **수치화·플롯 방식**: 분포는 **누적 Q₀** 로(전단율·충돌속도), 스윕은 **툴속도를 공통 x축**으로 전 변형을 한 그림에 겹쳐(Fig 18·19) **"절대값은 다른데 효율은 같다"** 를 시각적으로 증명. 검증은 **실험 = 선, 시뮬 = 기호** 규약.
- ⚠ **재현성 공백 3곳**: ① RSD bin 의 실제 크기·개수·회전계 여부 ② CGF 별 γ 값 ③ 가우시안 보간 커널 폭·격자.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⚠ `litdb/our_dem_baseline.md` 는 현재 **값 0개의 자리표시**다(2026-09-09). 아래 "우리" 열의 수치는 **CLAUDE.md 정본 서술**에서 가져온 것이고, 기준값 문서로는 아직 확인 불가다.

| 항목 | 이 논문 (Eirich 믹서 DEM) | 우리 (ASSB cold-press DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| **공정 단계** | **건식 혼합(분산 + 분쇄)** — 누르지 않는다 | **`insert/pack` → 정착 → 플래튼 압밀 300 MPa** | ★ **직렬로 다른 단계.** 우리에겐 **전단 믹싱 단계가 아예 없다**(prereg `m7` §2-1 이 실측 확인). 정면충돌 아님 |
| **소재계** | **NMC622 + 카본블랙 2 wt%** (SE 없음, LIB) | **LPSCl + NMC811** (+ VGCF·PTFE 는 MPM/복셀) | ⛔ **SE 가 없다** ⇒ 소재 절대값 전이 전면 금지 |
| **입자 종 수** | **1종** (NMC+CB 를 합친 CG 입자) | **3종** (AM_P · AM_S · SE) | ★ **우리가 더 많다.** 그들은 다성분 DEM 이 아니다 |
| **★ 점착 모델** | **JKR**, 표면에너지 **γ [J/m²]**. `γ_pp` 1개 + `γ_pw`(= γ_pp/6) 1개 | **`hooke/hysteresis` + `coefficientAdhesionStiffness` k_c [N/m 계열]**, **3×3 상쌍 행렬** (AM–AM 1.0e5 / AM–SE 2.0e5 / SE–SE 1.0e6) | ★★ **파라미터 종류 자체가 다르다**(에너지형 vs 강성형) **+ 우리는 상쌍 비대칭을 갖고 그들은 없다.** ⇒ **값 대응 불가**, 규칙만 참고 |
| **★ γ / k_c 의 입경 스케일링** | **cohesion number 불변 ⇒ γ ∝ R\*^1.6** (CG 크기 간 내삽 전용) | **미고정** (`prereg m7` §2-3: *"`k_c ↔ Γ` 관계는 미고정"*) | ★★ **우리 공백에 직접 닿는 유일한 문헌 처방.** 단 **k_c 로 가는 다리는 이 논문에 없다**(§4.3 말미) |
| **★ 점착값의 지위** | **실험 보정값**(2 mm CG 입자에 대해) — 물성 아님. 저자 자신이 *"NMC–NMC 표면에너지는 미지·측정난"* 이라 못박음 | **입력 규약값** (출처 앵커 미고정) | ★ **둘 다 "재료 물성" 이 아니다.** 이 논문은 그 사실을 **명시적으로 적는다** ⇒ 우리 `m7` 의 방어 논리에 인용 가능 (§9) |
| **★ 혼합/분산 지표** | **RSD** (라벨 50:50, 공간 bin, `s≥400`·`n_s≥100`) + **MSD·MSD₉₅** | **미보유** (prereg `m7` §4 가 **상별 접촉 enrichment `E_XY`** 를 주지표로 신설 중; 부지표 CLMI/Lacey) | ★★ **그들 RSD 는 우리 질문에 못 쓴다** — 라벨 확산(대류 혼합)을 재지, **상별 응집**을 재지 않는다. 그러나 **표본크기 의존의 실증 사례**로서 우리 prereg 가 Lacey 를 부지표로 강등한 판단을 **뒷받침**한다 |
| **★ 강성 조작** | **G = 1e8 Pa 로 낮춤 — 이유는 *계산비용/timestep*** | **E_SE 24 → 1.35 GPa (18× 연화) — 이유는 *입상 재배열 럼핑*** | ★★ **같은 조작, 다른 동기.** 그들 = 수치 편의 / 우리 = 결손 물리 보상. **그들 G 를 물성으로 읽으면 안 된다** |
| **coarse-graining** | **CGF 200** (2.0 mm ↔ 실제 ~10 µm), 상한 실측 **CGF ≤ 200** | **안 함** (실크기 12:4:1 — Furnas dip 을 위해 필수) | 우리가 셀 스케일로 갈 때 필요해질 축. **점착까지 같이 스케일해야 한다**는 것이 이 논문의 교훈 |
| **소성** | **없음** (강체 구, 항복캡 없음) | DEM `hooke/hysteresis`(접촉 소성, 형상 불변) + **MPM 진짜 J2 형상 소성** | frame[5] — **형상 소성은 여전히 우리 MPM 고유** |
| **파쇄** | **시뮬 안 함** — 분쇄를 **파라미터로 번역해 넣음** | Auerbach 취성 파괴 + fracture-aware σ | ★ **우리가 파쇄를 *푼다*.** 단 우리 것은 압밀 하중 하의 파괴이고 그들 것은 충돌 분쇄라 **대상이 다르다** |
| **전달 삼중항** | ⛔ **0채널** | σ_ionic·σ_e·σ_thermal (접촉망 Kirchhoff/Holm + 복셀 FV) | ★ **우리 압도적 우위** |
| **porosity** | ⛔ **미산출** (벌크밀도만, 그것도 실험 입력) | pure-SE ~10 % / real_14 15.6 % @300 MPa | `densification_porosity_db` 에 **porosity 칸 비움** |
| **전기화학** | ⛔ **없음** | STEP4 BV·확산·풀셀 | — |
| **검증 축** | **믹싱툴 소비전력**(2 믹서 × 6 속도 + 3 시간 × 3 속도) + 벌크밀도/Lumisizer + MSD 문헌 타당성 | Minnmann porosity · Cronau overlap · Bazzoun σ_eff 등 | ★ **그들은 *공정 관측량*(토크)으로, 우리는 *구조·전달 관측량*으로 검증** — 검증축 자체가 다르다 |
| **코드** | **EDEM 2022.3** (상용, GPU) | **LIGGGHTS** (오픈) | — |

---

## A. `frankenberg2024_dem_high_intensity_mixer_assb` 와의 분리 ★★ (요청 항목)

### A-0. 먼저 — **같은 논문이 아니다** (근거 전문)

| 판별축 | **Lischka 2025 (이 카드)** | **Frankenberg 2024 (기존 카드)** |
|---|---|---|
| 저자 | **Clemens Lischka, Hermann Nirschl** (2인) | **Frankenberg, Kissel, Burmeister, Lippke, Janek, Kwade** (6인) |
| 기관 | **KIT — MVM, Karlsruhe** | **TU Braunschweig — IPAT** + **Univ. Gießen** |
| 저널·연도 | **Particuology 104 (2025) 52–67** | **Powder Technology 435 (2024) 119403** |
| DOI | `10.1016/j.partic.2025.06.002` | `10.1016/j.powtec.2024.119403` |
| 믹서 | **Eirich EL1.0 / EL0.1** (편심 회전툴 + **회전 용기** + 벽 스크레이퍼) | **Hosokawa Alpine Picoline / Nobilta** (**환상 간극 annular-gap** 로터-드럼) |
| DEM 코드 | **EDEM 2022.3** | **Rocky 2023 R1** |
| 소재 | **NMC622 + CB 2 wt% — SE 없음 (LIB)** | **LFP + CB + Li₃InCl₆ 할라이드 SE — ASSB** |
| 목적 | **분산(혼합 균질도) + 분쇄(CB 해쇄)** | **응집(heteroaggregate 형성)** |
| 성능 연결 | **벌크밀도**(분쇄도 대리). 셀 없음 | **풀셀 방전용량** 실측 |
| CG 배율 | **CGF 200** (2.0 mm) | **f = 26.65** (0.5 mm) |
| ★ 점착 스케일 규칙 | **cohesion number 불변 ⇒ γ ∝ f^1.6** | **force-scaling ⇒ Γ ∝ f¹ (JKR 힘 ∝ f²)** |

★★ **결정적 증거**: **이 논문이 Frankenberg (2024) 를 인용한다.** 본문 §1 마지막 문단 —
> *"For **a different type of mixer, the Nobilta annular gap intensive mixer**, two papers by Asylbekov et al. (2023) and **Frankenberg et al. (2024)** can be found in the literature regarding the use of the DEM methodology in the production of batteries."*

즉 **이 논문 스스로가 Frankenberg 를 "다른 종류의 믹서" 로 분류**한다. ⇒ **중복 아님, 보강 아님, 별개 카드가 맞다.**

### A-1. ★ 둘이 **겹치는** 것 (같은 문제를 푼다)
1. **둘 다 "고강도/집약 건식 믹서 안의 입자 응력·충돌" 을 DEM 으로 푼다** — 우리 파이프라인에 **없는 공정 단계**를 메우는 같은 자리.
2. **둘 다 coarse-graining 이 필수**이고, 둘 다 **점착(JKR)이 없으면 거동이 안 나온다**고 판단했다.
3. **둘 다 검증을 *공정 관측량*으로** 한다 (Lischka = 툴 소비전력 / Frankenberg = 비파워 멱지수 + 분체 3종 시험).
4. **둘 다 전달 σ 0채널 · porosity 미산출 · 강체 구 · 형상 소성 없음** ⇒ frame[5] 의 같은 절반(MPM 쪽)이 비어 있다.
5. **둘 다 "더 세게 = 더 좋다" 를 부정**한다 — Frankenberg 는 *분산 포화 후 재응집*, Lischka 는 *원심에 의한 충돌률 붕괴*.

### A-2. ★★ 둘이 **갈라지는** 것 — **코스그레이닝 하에서 점착을 다르게 스케일한다** (가장 값진 대조)

| | **Lischka 2025** | **Frankenberg 2024** |
|---|---|---|
| **보존하는 불변량** | **cohesion number** = 점착일 / **중력** 퍼텐셜에너지 | **응력 σ 와 충돌당 비에너지 E_m** (관성 기반) |
| **표면에너지 스케일** | **γ_CG = γ₀ · f^1.6** | **Γ_CG = Γ₀ · f¹** |
| **JKR 흡인력 스케일** | **F_po ∝ f^2.6** (우리 유도: F_po ∝ ΓR) | **F ∝ f²** (명시) |
| **결과적 Coh 의 거동** | **f 에 불변**(설계상) | **Coh ∝ f⁻¹** (우리 유도) — CG 입자가 **상대적으로 덜 점착적**이 된다 |
| **물리적 정당화** | 중력 대비 점착성을 보존 → **안식각 등 중력지배 벌크시험**을 재현해야 하므로 자연스러움 | 믹서는 관성지배(중력 무관) → **충돌 응력·에너지**를 보존해야 하므로 자연스러움 |
| **검증 방식** | 2.0/1.5/1.0 mm 에서 **같은 안식각**(Fig 2b, 숫자 없음) + CGF 100–200 에서 **같은 정규화 충돌률**(Fig 9b) | 두 입자 정면충돌의 **force–time 곡선**이 f² 스케일을 따르는지 직접 확인 |

⇒ ★★ **두 처방은 양립하지 않는다.** 같은 CG 배율에서 한쪽은 점착을 f^1.6 으로, 다른 쪽은 f¹ 로 키운다. **f = 26.65 라면 그 차이가 26.65^0.6 ≈ 7.0배**다 (우리 산술). **어느 쪽이 맞느냐는 "그 공정에서 무엇이 지배하느냐" 에 달려 있다** — 중력지배 벌크거동(안식각·유동성)을 재현해야 하면 Lischka 쪽, 관성지배 충돌응력을 재현해야 하면 Frankenberg 쪽이다. ⇒ **coarse-graining 에서 점착 스케일은 "정답이 하나인 물리" 가 아니라 *어떤 불변량을 선택했는가* 다.** 이것이 두 카드를 나란히 둘 때 나오는 가장 큰 배움이다.

### A-3. 그 밖의 분업
- **공정 방향이 반대다.** Frankenberg = **응집(aggregation)** 을 만들려고 돌린다(heteroaggregate = 큰 AM 코어 + CB·SE 쉘). Lischka = **해쇄(de-agglomeration/분쇄)** 하려고 돌린다(CB 응집체를 깬다). ⇒ **같은 장비류에서 *목표가 정반대*.** 우리에게는 **둘 다 필요**하다 — `m7` 이 묻는 것은 *응집이 생기는가* 이고, 그 응집을 *깨는* 쪽의 에너지 눈금은 Lischka 가 준다.
- **성능 연결이 다르다.** Frankenberg 는 **풀셀 용량**까지 간다(우리가 못 가는 곳). Lischka 는 **벌크밀도**에서 멈추고 성능 연결은 문헌 인용.
- **기하 노브가 다르다.** Frankenberg 는 회전속도 n 하나를 스윕. Lischka 는 **툴속도·용기속도·경사·충전량·툴크기·핀수·블레이드·운전모드 8축**을 스윕 ⇒ **설계 스윕의 폭은 Lischka 가 압도적**.
- **응력 표현이 다르다.** Frankenberg 는 **SI·SF·SN·E_m (Kwade stressing model)** 의 완전한 4종 세트 + 공간영역별 분해. Lischka 는 **충돌률·충돌에너지·전단율** 3종이고 공간분해는 하지 않는다(단면 하나). ⇒ **응력 기술자(descriptor) 정교함은 Frankenberg 쪽.**

---

## B. 적용가능성 — 우리 `m7` 사전등록에 실제로 무엇을 주는가

### B-1. ⛔ 먼저, **못 주는 것**부터
1. **`k_c` 의 값**. 이 논문에 `k_c` 도, `γ↔k_c` 식도 없다. **prereg `m7` §8-③ 은 이 논문으로 풀리지 않는다.**
2. **상별 표면에너지 대비**. 입자종이 하나라 **상쌍 비대칭의 선례가 없다** ⇒ prereg §8-④(*"표면에너지를 상별로 다르게 주는 예"*) 도 **이 논문으로 안 풀린다.**
3. **응집 지표**. RSD 는 라벨 분산이라 `E_SE-SE` 같은 **상별 응집**을 대신할 수 없다.
4. **숫자의 전이**. γ 0.3 J/m² 는 **2 mm CG NMC/CB 입자**의 보정값이다. 우리 1 µm SE 입자에 어떤 의미로도 옮길 수 없다.

### B-2. ★★ 대신 주는 것 ① — **"문헌 표면에너지에 접지하기" 라는 계획 자체에 대한 경고**
prereg `m7` §2-3 은 *"우리 노브는 `k_c`, 문헌 주류는 JKR Γ"* 라고 적고 **접지 가능성을 열어 뒀다**. 이 논문은 그 문을 **좁힌다**:
- 이 분야 문헌의 γ 는 **재료 물성이 아니라 *그 CG 크기에서의 보정 상수*** 다. 저자가 직접 *"NMC–NMC 표면에너지는 미지이고 측정하기 어렵다"* 고 적고 **실물 γ 를 쓰는 길을 포기**한다.
- 같은 입자 크기대(mm 급 CG)에서 **두 문헌 값이 67배 차이**난다 — Lischka **0.3 J/m² @2 mm** vs Frankenberg **0.0045 J/m² @0.5 mm**. (cohesion-number 로 0.5 mm 까지 내리면 Lischka 값은 0.3·(0.25)^1.6 ≈ **0.0369 J/m²**로, 그래도 Frankenberg 의 **8.2배**다 — 우리 산술.) ⇒ **"문헌 γ" 라는 단일 값이 존재하지 않는다.**
- 그리고 cohesion-number 로 실물 입경까지 밀면 **비물리적인 6e-5 J/m²** 가 나온다(§3.2).
⇒ ★ **권고: `m7` 을 "문헌 표면에너지에 접지" 하려는 시도는 *하지 말거나*, 한다면 반드시 "우리 입자 크기·우리 벌크 관측량에 우리가 보정한 값" 이라는 지위로만 할 것.** 이 논문은 그 지위 선언의 **인용 가능한 선례**다(§9).

### B-3. ★ 주는 것 ② — **지표 설계에서 피할 함정 3개** (전부 이 논문의 실물 사례)
1. **분산과 RSD 를 섞지 말 것.** 이 논문은 `x_t(1−x_t)/s` 를 `RSD_s` 라 부르고 0.000625 와 0.05 를 같은 문장에서 비교한다 → **결론의 방향이 뒤집힌다**(§3.2·§10-①). ⇒ **`m7` 보고에서 `E_XY` 와 그 분산·표준오차의 차원을 명시할 것.**
2. **표본크기가 하한을 정한다.** `RSD_r = √((1−x_t)/(x_t·s))` 이므로 bin 을 잘게 쪼개면 "완전혼합" 판정선이 올라간다. ⇒ **prereg §4 가 `E_XY` 를 고른 이유("격자·구간 나누기가 필요 없다")가 이 사례로 정당화된다.** 부지표 CLMI/Lacey 를 **주판정에 넣지 않기로 한 것도 옳다.**
3. **"자기 정상값의 90 % 도달시간" 은 품질 순위가 아니다** (RSD₉₀ 함정, §4.6c). ⇒ 우리가 수렴시간 지표를 만들면 **정상값을 arm 간에 고정하거나 같이 보고**할 것.
4. (보너스) **평균만 적지 말 것** — 이 논문은 MSD 를 **평균과 95퍼센타일로 함께** 낸다(*"the ensemble average hides the underlying distribution character"*). ⇒ `E_SE-SE` 도 **시드별 분포**를 같이 보고.

### B-4. ★ 주는 것 ③ — **"우리에게 전단 믹싱 단계가 없다" 는 한계의 크기를 문헌으로 재는 눈금**
prereg `m7` §2-1 은 우리 결과를 *"믹싱 헤테로지니티"* 라 부르지 말라고 못박았다. 이 논문은 **그 금지가 얼마나 큰 것인지**를 숫자로 준다:
- 실제 Eirich 믹서의 전단율은 **최대 10 s⁻¹**, 충돌속도는 **최대 ~33 m/s**, 파워비 충돌에너지 **~10 %**.
- **혼합 균질화는 20–30 초에 포화**하고 그것을 정하는 것은 **용기 회전**이다.
- ⇒ **우리 `insert/pack` + 정착은 이 중 어느 것도 갖지 않는다.** ★ 그러나 동시에 **위안**도 있다 — **혼합 균질도는 30 초면 포화**하므로, "잘 섞인 초기조건" 이라는 우리 가정 자체는 **실제 공정에서 쉽게 달성되는 상태**다. 우리가 못 보는 것은 *균질화* 가 아니라 **분쇄(CB 해쇄)와 그로 인한 마찰·밀도 변화**다.
- ⇒ ★ **우리가 정직하게 말할 수 있는 문장**: *"우리 모델은 혼합이 이미 완료된(RSD 포화) 분말에서 출발한다 — 그것은 이 공정계에서 30 초면 도달하는 상태이므로 합리적 초기조건이다. 우리가 표현하지 않는 것은 균질화가 아니라 **도전제 해쇄와 그에 따른 분말 상태 변화**다."* ⇒ prereg §2-1 의 한정어를 **더 정확하게** 만든다.

### B-5. ★ 주는 것 ④ — **"충돌이지 전단이 아니다" 라는 기전 판정의 방법론**
저자는 두 후보(전단 / 충돌)를 각각 **분포**로 뽑아 비교해 판정했다: 전단율 분포는 **툴속도에 거의 안 움직이고**, 충돌속도 분포는 **크게 움직인다** ⇒ 관측된 툴속도 의존이 충돌에서 온다. ★ **이것은 "노브를 바꿨을 때 어느 채널이 실제로 움직이는가" 로 기전을 갈라내는, 우리 `CL-44`/`CL-45`(σ-치환 채널 vs 부피 채널) 와 *같은 형태의 논증*이다.** ⇒ `m7` 에서 *"비대칭이 응집을 만든다"* 를 주장할 때도 **경쟁 채널(입자 크기 차이로 인한 접촉통계 편향)을 같은 방식으로 따로 재서 갈라야 한다** — prereg §5 의 *"`E_SE-SE(A) > 1` 자체는 판정이 아니다"* 경고가 바로 그것이고, 이 논문이 그 방법의 **모범 사례**다.

### B-6. 주는 것 ⑤ — **CGF 상한이라는 실용 규칙** (미래 대비)
우리가 셀 스케일 DEM 으로 갈 때 필요해질 것: **정규화 관측량(여기서는 입자당 충돌률)으로 CG 크기를 올려 가며 어긋나는 지점을 찾는다** — 이 논문은 **CGF 400 에서 고속만, CGF 800 에서 전역**이 깨진다고 실측했다. ★ **우리 격자수렴 판정(`CL-74`)과 같은 논리**이고, 우리 쪽이 더 엄격하다(우리는 *"뒤쪽 전부 tol 안"* 을 요구). ⚠ 단 이 논문의 판정은 **γ 가 함께 재계산된 상태**에서 나온 것이므로 **기하 효과와 점착 효과가 교락**돼 있다(§4.4 말미).

---

## C. 우리 novelty — 이 논문 대비 우리가 갖는 것
1. **전달 삼중항** (σ_ionic·σ_e·σ_thermal, 접촉망 Kirchhoff/Holm + 복셀 FV) — 그들 **0채널**.
2. **porosity·percolation·배위수·tortuosity·coverage** — 그들 **전부 없음**.
3. **진짜 형상 소성 (MPM J2)** 과 void-fill 유동 — 그들 강체 구.
4. **다성분 DEM (3종) + 상쌍 비대칭 점착 행렬 (3×3)** — 그들 1종·2값(그나마 1/6 로 묶임).
5. **파쇄를 *푼다*** (Auerbach + fracture-aware σ) — 그들은 분쇄를 **파라미터로 번역**.
6. **압밀 압력 축** (Heckel, P_y, 다압력) — 그들 축 자체가 없음(비에너지 축).
7. **전기화학까지의 사슬** (STEP4) — 그들 셀 없음.
⚠ **반대로 그들이 우리보다 나은 것**: **공정 기하와 운전조건 스윕**(8축) · **공정 관측량(토크·소비전력)에 의한 검증** · **코스그레이닝 상한의 실측** · **에너지 회계(η_cb·n_coll·ε_coll)의 체계성**. 우리에겐 **공정 축 자체가 없다.**


---

## 8. 적용 인사이트 (내 연구에 어떻게)

- **① ★★ `m7` 사전등록 §8 의 네 질문에 대한 부분 답** — 이 논문으로 **①②는 답이 나오고 ③④는 안 나온다**:
  - §8-① *"점착 모델이 무엇인가"* → **이 문헌계의 주류는 JKR + 표면에너지 γ [J/m²]** 임이 두 편(Lischka·Frankenberg)에서 확인된다. 우리 `hooke/hysteresis + coefficientAdhesionStiffness` 는 **다른 계열**이다.
  - §8-② *"파라미터 이름·단위·출처"* → 이름 `γ_pp`/`γ_pw`, 단위 J/m², **출처 = 실험 보정(안식각·링전단·경사판)**. **문헌 물성표가 아니다.**
  - §8-③ *"`k_c ↔ Γ` 식이 있는가"* → ⛔ **없다.** ⇒ **prereg §2-3 의 한정어(*"`k_c ↔ Γ` 관계는 미고정"*)는 이 논문으로 풀리지 않고 그대로 유지**된다.
  - §8-④ *"표면에너지를 상별로 다르게 주는 예"* → ⛔ **없다.** 입자종이 1개다. ⇒ **[19] 의 "4종 표면에너지 차이" 선례는 이 논문에 없다.**
- **② ★ 대신 얻는 것 — 우리 `m7` 값의 *지위 선언* 에 쓸 문헌 근거.** 이 논문은 *"NMC–NMC 표면에너지는 미지이고 측정하기 어렵다"* 고 **1저자가 본문에 직접 쓴다.** ⇒ 우리가 `k_c` 3값의 출처를 못 대는 것은 **이 분야의 일반적 상태**이지 우리 모델만의 결함이 아니다. **단, 그 문장은 "그러니 아무 값이나 써도 된다" 가 아니라 "그러니 *벌크 관측량에 보정하고 그 사실을 적어라*" 로 읽어야 한다** — 이 논문도 그렇게 한다(안식각·링전단·경사판 3종).
- **③ ★★ 지표 설계 — `E_XY` 선택이 이 논문으로 정당화된다.** prereg §4 가 Lacey 를 부지표로 강등하고 **격자 불요한 enrichment** 를 주지표로 삼은 판단이, 이 논문의 RSD 가 겪는 **표본크기 의존(`RSD_r = √((1−x_t)/(x_t s))`)과 bin 규약 미보고**로 **실증**된다. ⇒ **prereg 를 고칠 필요 없음. 오히려 §4 의 "왜 이것인가" 근거 문단에 이 사례를 각주로 달 수 있다** (런 전 문서 수정은 §4 의 *근거 서술*에 한정 — 지표·판정선·보고창은 건드리지 않는다).
- **④ ★ 분포를 같이 보고하는 습관.** 이 논문은 MSD 를 **평균 + 95퍼센타일**로 낸다(*"the ensemble average hides the underlying distribution character"*). ⇒ `E_SE-SE` 도 **시드별 값을 전부 적고** 평균·SE 를 같이 낸다 (prereg §5 가 이미 시드 ≥3 을 요구하므로 **추가 비용 0**).
- **⑤ ★ 경쟁 채널 분리의 모범 사례.** "전단이냐 충돌이냐" 를 **두 분포를 각각 노브(툴속도)에 대해 움직여 보고** 갈랐다 — 우리 `CL-44`/`CL-45`(σ-치환 vs 부피 채널)와 **같은 형태**. ⇒ `m7` 에서 `E_SE-SE(A) > 1` 을 응집 증거로 쓰지 말라는 prereg §5 경고를 지키되, **경쟁 채널(입자 크기 차에 의한 접촉통계 편향)을 *따로 재는* 팔**을 나중에 붙일 여지를 남긴다 (예: 모든 상의 반경을 같게 둔 대조 — ⚠ 이것은 **런 후 추가 제안**이고 현 prereg 3팔 설계에 넣는 것이 아니다).
- **⑥ ★ 우리 한계 문장을 정밀하게** — §B-4 대로, *"우리는 균질화를 못 보는 게 아니라 (그것은 30 초면 포화한다) **도전제 해쇄와 그에 따른 분말 상태 변화**를 못 본다"* 로 바꿔 적으면 더 정확하고 더 방어 가능하다.
- **⑦ coarse-graining 을 언젠가 도입한다면** — **점착도 같이 스케일해야 하고, 그 규칙이 유일하지 않다**(§A-2). 우리 `k_c` 는 강성형이라 Lischka/Frankenberg 어느 처방도 그대로 못 쓴다 ⇒ **우리가 보존할 불변량을 먼저 고르고 그것으로 `k_c` 스케일을 *유도*해야 한다** (예: 접촉당 분리일 보존 vs 무차원 Bond 수 보존). **DO NOT** 문헌 지수(1.6 또는 1.0)를 `k_c` 에 그대로 붙이지 말 것.
- **⑧ 데이터 적재 제안**: `docs/data/lischka2025_eirich_mixer.csv` — Table 1(5행 × 9열, stated) · Table 2(η_cb, stated) · Table 3(RSD₉₀·MSD, stated) · Fig 3b 피팅식(stated) · 혼합시간 단축률 3건(stated) · CGF 판정(stated) + 우리 유도량(§3.2) 을 **derived 플래그와 함께**. ⛔ **`densification_porosity_db.csv` 에는 넣지 말 것** — porosity 칸이 전부 비고 압력 축이 아예 없다(비에너지 축).

## 9. 인용 가능 문장 (deck/paper 용)

- "Lischka & Nirschl (*Particuology* **104** (2025) 52–67) simulated dry mixing of an NMC-622 / carbon-black (2 wt %) cathode powder in an **Eirich EL1.0 intensive laboratory mixer** by DEM (EDEM 2022.3), using a **coarse-grained particle (CGF = 200, d = 2.0 mm)** that represents the NMC + carbon-black mixture as a *single* species, with **JKR cohesion** and friction parameters calibrated against angle-of-repose, ring-shear and inclined-plate experiments."
- "★ They found that **impact against the fast-rotating mixing tool — not shear — is the dominant comminution mechanism**: the simulated shear-rate distribution peaks at only ~10 s⁻¹ (one to two orders of magnitude below extruders, because the Eirich geometry has no sub-millimetre shear gap) and is almost insensitive to tool speed, whereas the particle–tool collision-velocity distribution shifts strongly with tool speed."
- "★ **Homogeneity and comminution are governed by different knobs.** Mixture homogeneity (RSD) saturates within about 20–30 s and is controlled by the **vessel rotation**, not the tool speed; the comminution-relevant collision rate instead *falls* with increasing tool speed because the tool centrifuges material out of its own stress zone — which is why enlarging the tool or adding feeder blades cut the mixing time needed to reach a target bulk density by **56 %** and **up to 75 %** respectively, while raising vessel speed from 85 to 170 rpm gave **20 %**."
- "★ **Only ~10 % of the mixing-tool power appears as particle–tool collision energy** (ε_coll = E_coll/P_tool), the rest being dissipated as friction heat or kinetic energy; and although design changes raise the *absolute* collision rate, the **power-specific** collision rate collapses onto a single curve for nearly all configurations — i.e. better comminution comes at the cost of higher absolute power, not higher efficiency."
- "★ On coarse-graining they scale the **JKR surface energy by holding Behjani's cohesion number constant**, `Coh = (1/ρg)·(γ⁵/(E*²R*⁸))^{1/3}`, which implies **γ ∝ R\*^{8/5}**; coarse-grain factors of 100–200 then reproduce the same particle-normalised collision rate, while CGF 400 and 800 deviate, giving a practical ceiling of **CGF ≤ 200 (d ≤ 2 mm)** for this system."
- "⚠ ★ Critically, the authors state that **the NMC–NMC surface energy is 'unknown and difficult to measure'** and therefore use the cohesion number *only* to transfer their **experimentally calibrated** coarse-grain surface energy between coarse-grain sizes — not to recover a real-particle surface energy. The reported γ values (0.3 J m⁻² particle–particle and 0.05 J m⁻² particle–wall at d = 2 mm) are therefore **coarse-grain calibration constants, not material properties**, and cannot be transferred to a different particle size or material system."
- "⚠ This is a **process-mechanics DEM for a conventional (liquid-electrolyte) Li-ion cathode powder**: there is **no solid electrolyte**, the two solids are lumped into one DEM species, and the model outputs **no porosity, no ionic/electronic/thermal conductivity and no electrochemistry** — the only performance proxy is the powder bulk density used as a measure of carbon-black comminution."

## 10. 주의 / 한계 (over-claim 방지)

- **① ★★ RSD 하한의 단위 혼동 (우리 판정).** 논문의 `RSD_s = x_t(1−x_t)/s = 0.000625` 는 **분산**이고, 같은 척도의 RSD 는 **0.05** 다. 따라서 *"achievable final value … RSD < 0.05, which is well above the value for statistical random mixing"* 는 **성립하지 않는다** — 같은 척도로 맞추면 **그들의 결과는 무작위혼합 한계 위가 아니라 *그 자리*** 다. ⚠ **인용할 때 이 정정을 붙일 것.** (산술: √(6.25e-4)/0.5 = 0.025/0.5 = 0.05.) 이것은 논문의 결론(용기 회전이 지배)에는 영향이 없고, 오히려 **회전용기 케이스를 더 좋게** 만든다.
- **② ⛔ 소재 전이 금지.** **SE 가 없는 LIB 계**다. γ 0.3 J/m², μ_s 1.0, ρ 1200–1938 kg/m³, d 2 mm — 전부 **2 mm CG NMC/CB 입자**의 값이다. 우리 LPSCl·NMC811·µm 급 계로 **어떤 숫자도 옮기지 말 것**.
- **③ ★ Fig 6 검증은 반쯤 순환적이다.** 혼합시간별 파워 일치는, ⓐ **벌크밀도와 그에 따른 충전높이를 실측으로 고정**하고 ⓑ **마찰·점착을 "줄어든 파워가 재현되도록" 조정**한 뒤 얻은 것이다 (본문: *"the material parameters **were adjusted** … **so that** the reduced power requirement of the mixing tool could be shown"*). 실제로 Table 1 의 30 min·90 min 네 행은 마찰값이 거의 동일하므로, 시간 의존성의 대부분은 **밀도·충전높이·입경**(= 측정값)에서 온다. ⇒ **"모델이 파워 감소를 예측했다" 가 아니라 "측정된 분말 상태를 넣으면 파워가 맞는다"** 로 읽을 것.
- **④ ⚠ Fig 5 는 "추세 일치" 까지다.** 저자도 *"the trend is well captured"* 라고만 쓴다. 로그축에서 EL0.1 저속은 시뮬이 실험의 **~2배** 로 읽힌다(digitized). **절대 파워값을 우리 문서에 인용하지 말 것.**
- **⑤ ⚠ 분쇄는 시뮬되지 않는다.** 입자는 깨지지 않는다. 충돌에너지는 *"the upper limit for the energy that can be converted to break"* = **상한 프록시**다. ⇒ **"DEM 이 카본블랙 분쇄를 예측했다" 는 서술 금지.** 예측된 것은 **분쇄에 쓸 수 있는 에너지**이고, 그것을 분쇄량으로 바꾸는 다리는 **실험 곡선(Eq 5)** 이다.
- **⑥ ⚠ 40 m/s 는 장비 범위 밖**(실기 최대 30 m/s). 40 m/s 결과는 **외삽**이고, 특히 Table 3 의 RSD/MSD 비교가 그 속도에서 이뤄졌다.
- **⑦ ⚠ 재현 불가 3곳**: RSD bin 의 실제 크기·개수·회전계 여부 / **CGF 별 γ 값(논문이 "Table 1 에 있다" 고 했으나 실제로 없음)** / 전단율 보간 커널 폭·격자. ⇒ **CGF 스윕과 RSD 절대값은 제3자가 재현할 수 없다.**
- **⑧ ⚠ 논문 내부 불일치 3건 (전부 우리가 확인)**: ⓐ MSD 차원 `m²`(Eq 8) vs 표 단위 `m²/s`(Table 3) · ⓑ Eq 6 의 `E_idle` 과 본문의 `E_empty` 가 같은 양의 두 이름 · ⓒ **Table 1 의 90 min 밀도 1938 kg/m³ 가 본문이 말한 최대 도달 벌크밀도 1.83 g/mL(=1830) 를 넘는다** — 즉 DEM 입력이 실험이 도달 불가라 한 값보다 6 % 조밀하다. (⚠ 이 마지막 건은 Table 1 의 `ρ_bulk` 가 EDEM 의 *입자밀도* 입력일 가능성이 남아 있어 **모순이라고 단정하지는 않는다** — 논문이 그 구분을 적지 않았다는 것이 요점이다.)
- **⑨ ⚠ 강성 G = 1e8 Pa 는 계산비용 때문에 낮춘 값**이라고 저자가 직접 쓴다. **물성으로 인용 금지.** (스테인리스 기하는 1e11 로 3자릿수 높다.)
- **⑩ ⚠ COR = 0.5 는 측정 불가라서 가정한 값**이고, 충돌에너지에 `(1−k²)` 로 직접 들어간다 ⇒ **모든 E_coll 절대값은 이 가정에 걸려 있다.** 민감도 스윕 없음.
- **⑪ ⚠ MSD 의 "검증" 은 한쪽 방향 타당성 논증**이다 (Hare 2023 습식 슬러리 0.001 m²/s 보다 건식이 커야 하고 실제로 크다). **다른 계·다른 상태와의 부등호 하나**이므로 검증으로 인용하지 말 것.
- **⑫ ⚠ 툴 크기 스윕은 교락돼 있다** — 위치를 고정했으므로 **툴 직경과 벽간극이 동시에 변한다**. "툴이 크면 좋다" 는 결론에서 어느 쪽이 원인인지 분리되지 않았다(저자도 *"finding the best tool size to vessel ratio"* 를 후속으로 남긴다).
- **⑬ ⚠ 각 변형은 1 런으로 보인다.** 시드 반복·오차 보고가 **Fig 6 을 제외하면 없다**. ⇒ Fig 9·17·18·19 의 변형 간 차이에 **불확실성 막대가 없다.**
- **⑭ ⚠ 격자·CG 판정이 γ 와 교락.** CGF 100–200 일치는 **γ 를 함께 재계산한 상태**에서 나온 것이라, 기하 수렴과 점착 스케일링 중 무엇의 공인지 분리 불가(§4.4).

## 11. 기술 미니 용어집 (이 카드를 혼자 읽을 사람용)

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **Eirich intensive mixer** | 편심 고속 회전툴 + **회전 용기** + 고정 벽 스크레이퍼로 구성된 집약형 혼합기. 산업·연구에서 조립·과립·코팅·해쇄에 널리 쓰임 | EL1.0(1 L)·EL0.1(0.1 L) |
| **coarse graining (CGF)** | 계산 가능하게 DEM 입자를 실제보다 **일정 배율로 키우는** 기법. 입자수와 timestep 부담을 동시에 줄인다 | CGF = 200 (2 mm ↔ 실제 ~10 µm) |
| **JKR** | Johnson–Kendall–Roberts 점착 접촉 이론. 접촉면 **안**에서 작용하는 표면에너지 γ 로 흡인력을 준다(무른·큰 입자 극한). 대비되는 것이 **DMT**(작고 단단한 입자, 접촉 바깥 vdW) | 점착 모델 본체 |
| **surface energy γ** | 두 표면을 떼는 데 드는 단위면적당 일 [J/m²]. JKR 의 유일한 점착 노브 | γ_pp = 0.3, γ_pw = 0.05 (d = 2 mm) |
| **cohesion number Coh** | **점착일 / 중력 퍼텐셜에너지** 의 무차원 비. 크면 "중력보다 점착이 이기는" 분말 | CG 크기 간 γ 이전 규칙의 불변량 |
| **comminution** | 분쇄·해쇄. 여기서는 **카본블랙 응집체를 잘게 푸는 것** | 벌크밀도 상승으로 측정 |
| **RSD (relative standard deviation)** | 표본별 농도가 목표 농도에서 벗어난 정도를 목표로 나눈 값. 혼합 균질도의 고전 지표 | Eq 7, 목표 0.5, bin ≥100 × ≥400 입자 |
| **MSD** | 평균제곱변위. 입자가 얼마나 멀리 퍼졌나 | 평균 + 95퍼센타일 |
| **Q₀ 분포** | **개수 기준** 누적분포 (Q₀ = number-based cumulative). Q₃ 는 부피 기준 | 전단율·충돌속도 분포 |
| **co- / counter-current** | 툴 회전과 용기 회전이 **같은 방향 / 반대 방향** | 기준은 동류 |
| **specific energy e_tot** | 질량당 투입 에너지 [kJ/kg]. 공정 강도의 스케일-불변 축 | 벌크밀도와 1:1 대응 |
| **Rayleigh time step** | 표면 탄성파가 입자를 가로지르는 시간 ∝ R√(ρ/G). DEM 안정 timestep 의 기준 | 그 20 % 사용 |
| **PEPT** | Positron Emission Particle Tracking. 불투명 장비 안에서 표지입자를 실시간 추적 | Hare 2023 의 MSD 출처 |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
