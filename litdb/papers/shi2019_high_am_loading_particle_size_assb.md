<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목 -->
# 입자 크기비 λ=D_CAM/D_SE 로 고-CAM 로딩(>50 vol%) 달성 — 우리와 *같은 LIGGGHTS DEM + Hertz* 로 "작은 SE + 큰 CAM"을 모델+실험 동시 증명 — Shi (Ceder 그룹, Adv. Energy Mater. 2019/2020)

> slug `shi2019_high_am_loading_particle_size_assb` · DOI `10.1002/aenm.201902881` · type `mixed (DEM-LIGGGHTS modeling + experiment)` · PDF `Shi_2019_AdvEnergyMater_HighActiveMaterialLoading_ASSB_ParticleEngineering.pdf` · digested `2026-06-26` · status ✅

> ★ **우리 "size = PACKING" 스토리의 핵심 frame[4] 앵커 + DEM 방법론 *형제*.** 이 논문은 (i) **우리와 똑같은
> LIGGGHTS DEM + Hertz 접촉**으로 cold-press 양극을 압밀하고, (ii) **NMC(NCM) + LPS**(우리 NMC811+LPSCl 에 가장
> 가까운 소재계)에서, (iii) **단 하나의 지배변수 = 크기비 λ = D̄_CAM/D̄_SE** 가 cathode utilization(=활성 CAM 분율)을
> 결정함을 *모델로 예측하고 실험으로 검증*한다. 결론: **"SE 를 CAM 보다 작게(λ↑)"** 하면 고-CAM 로딩(>80 wt% / >50 vol%)에서도
> 거의 full 용량 → 우리 Furnas-dip·12:4:1·bimodal·production-core(AM 70–85 wt%) 의 *직접 실험-모델 증거*. ⚠ 단 그들 DEM 은
> 우리처럼 **rigid-sphere + Hertz(소성 SHAPE 없음)** 이고 transport 는 **이온 percolation *연결성*(최단경로)** 까지만 — σ 실값·
> Stage-E 소성면적·삼중항·MPM morphology 는 *안 함*. 그들이 비운 칸 = 우리 novelty. ⭐ Bielefeld 2019(ref [16])·LPS 소성변형
> (ref [29])을 *명시 인용* → 우리 litdb 가 이미 가진 두 논문과 직결.

> 데이터 CSV: `docs/data/shi2019_am_loading.csv` (이 digest 전용 — λ·로딩·porosity·용량·utilization 정밀 수치, stated vs digitized 구분).

---

## 1. 한 줄 요약 (bilingual)

**KO** — Ceder 그룹(UC Berkeley + LBNL + Samsung)이 **LIGGGHTS DEM(우리와 동일 코드) + Hertz 접촉**으로 NMC(CAM)+LPS(SE)
복합 양극을 200 MPa 로 cold-press 압밀하고, 각 CAM 입자가 SE percolation 경로로 bulk-SE(separator)에 연결되는지를 **최단경로
percolation** 으로 판정해 **cathode utilization θ_CAM**(=활성 CAM 부피분율)을 계산. 핵심 발견: **θ_CAM 은 CAM 절대-부피분율보다
*크기비 λ = D̄_CAM/D̄_SE* 에 훨씬 민감** — *고정 로딩에서 SE 입경만 줄여도(λ↑) utilization 이 20%→100% 로 극적 상승*. 따라서 **SE 를
CAM 보다 작게(λ>1)** 하면 고-CAM 로딩(>80 wt% / >50 vol%, 액체셀 수준)에서도 거의 full 용량을 *간단 혼합·가압* 으로 달성. ⚠ 그들 DEM 은
**rigid-sphere(소성 SHAPE 없음)** + transport 는 **이온 *연결성*(percolation 존재/최단경로)** 까지 — *유효 σ 실값·접촉저항·열·전자 percolation·
소성 morphology 는 안 풂*. 실험(4 SE 크기 × 3 로딩 × 2 CAM 크기) 이 모델 예측 용량과 *good agreement*.

**EN** — The Ceder group (UC Berkeley + LBNL + Samsung) uses **LIGGGHTS DEM (same code as ours) + Hertzian contact** to
cold-press (200 MPa) NMC(CAM)+LPS(SE) composite cathodes, then judges — by **shortest-path Li-ion percolation** — whether each
CAM particle is connected through the SE network to the bulk-SE (separator), giving the **cathode utilization θ_CAM** (active CAM
volume fraction). Headline finding: **θ_CAM depends far more on the *particle size ratio* λ = D̄_CAM/D̄_SE than on the absolute CAM
volume fraction** — at *fixed loading*, merely reducing the SE particle size (raising λ) lifts utilization from ~20 % to ~100 %.
Hence **keeping SE smaller than CAM (λ>1)** enables high-CAM loading (>80 wt% / >50 vol%, liquid-cell level) with near-full capacity
by *simple mixing + pressing*. ⚠ Their DEM is **rigid-sphere (no plastic SHAPE)** and transport is **ionic *connectivity* (percolation
existence / shortest path) only** — no effective-σ values, no constriction resistance, no thermal/electronic percolation, no plastic
morphology. Experiments (4 SE sizes × 3 loadings × 2 CAM sizes) show *good agreement* with model-predicted capacities.

**이 논문의 위치 (우리 기준):** **frame[4] 외부 실험 앵커이자 동시에 DEM 방법론 *형제*.** Bazzoun(같은 코드·소재·transport)이
*transport σ 솔버 형제*라면, Shi 는 *그 한 단계 앞 — 압밀 + percolation-연결성을 같은 코드로 + 실험검증* 한 형제. 우리 "size=PACKING
not overlap"(σ_ionic·σ_e 의 size-effect 가 기하 packing 이지 overlap 이 아니라는 결론)의 **가장 직접적인 모델+실험 증거**. 그들이
비운 칸(σ 실값·삼중항·Stage-E·소성·dip 깊이의 정량)이 정확히 우리 novelty.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Tan Shi**¹, **Qingsong Tu**¹ (¹동등기여), Yaosen Tian, Yihan Xiao, Lincoln J. Miara², Olga Kononova, **Gerbrand Ceder*** (Dept. Materials Science & Engineering, **UC Berkeley** + **Materials Sciences Division, Lawrence Berkeley National Lab**; ²Lincoln Miara = **Advanced Materials Lab, Samsung Research America**, Burlington MA) | *Adv. Energy Mater.* **2020**, 10, 1902881 (Received 2019-09-03, Published online **2019-12-03**; 표지년 2020) | **10.1002/aenm.201902881** (open access, CC-BY) | **SE = LPS (amorphous 75Li₂S·25P₂S₅, glass)** + **CAM = NMC (Li[Ni₀.₅Mn₀.₃Co₀.₂]O₂ = NMC532, LZO-coated)** | **mixed** — DEM(LIGGGHTS) 미세구조 모델링 + percolation 분석 **+ 실험**(셀 제작·사이클 검증) |

- **소재 정밀:** SE = **amorphous 75Li₂S–25P₂S₅(LPS) glass**, ball-milled, **σ_ion = 0.39 mS cm⁻¹**(SPEX-mixed bulk). CAM = **Li₀.₅Mn₀.₃Co₀.₂O₂ → 즉 LiNi₀.₅Mn₀.₃Co₀.₂O₂ = NMC532**, **6–8 nm LZO(Li₂O–ZrO₂) 코팅**(계면반응 억제 → 입경효과만 보려고). 도전제 = **CNF(carbon nanofiber) 5 wt%**(실험엔 넣되 모델엔 명시적 미포함, prefactor 0.95 로만 보정).
- ⚠ **소재 주의 (우리 대비):** SE = **LPS glass(σ 0.39 mS/cm)** ≠ 우리 **LPSCl Li₆PS₅Cl(σ ~1–3 mS/cm, ~3–8× 높음)**. CAM = **NMC532-LZO** ≠ 우리 **NMC811**. ⇒ **σ 절대값·용량 절대값 전이 금지**; *크기비-packing-utilization 추세*만 frame[4] 앵커. (단 둘 다 황화물 SE + 층상 NMC + cold-press → *거동·추세* 전이 가능.)
- 등록/게재: 2019-09-03 / 2019-11-01(rev) / **2019-12-03**(online). DOE BES DE-AC02-05CH11231 + Samsung Advanced Institute of Technology(SAIT) 지원. LZO-coated CAM = Samsung R&D Japan(Ito et al. ref [6] 절차) 제공.
- ⭐ **우리 litdb 와의 직결 인용:** ref **[16] = Bielefeld 2019**(우리 `bielefeld2019_microstructural_modeling_composite_cathode.md`); ref **[29] = Choi et al. ACS AMI 2018** = "LPS 입자의 *소성변형* 을 실험관측" → 본문 §3.2·§4 Discussion 에서 "**입자간 접촉면적의 정확한 기술은 LPS 의 소성변형 모델링을 요구**"라고 *우리 MPM/Stage-E 의 필요성을 명시* (아래 §7·§A 참조).

---

## 3. 핵심 물성 (수치)

> ★ = stated(본문/그림 라벨에 적힌 값). digitized = Fig 곡선에서 읽음(TREND only, ±). 이 논문은 **유효 σ 실값을 안 냄** → "물성"은
> **utilization θ_CAM · 크기비 λ · 로딩 f_CAM · 용량 · porosity**. 절대 σ·용량은 LPS-glass/NMC532-LZO → *우리 소재 절대전이 금지*.

| 물성 | 값 | 조건 (λ, 로딩, 입경) | stated/digitized | 비고 |
|---|---|---|---|---|
| **압밀 압력** ★ | **200 MPa**(미세구조 모델 + 양극 압밀); separator는 ~100 MPa | DEM·실험 공통 | stated | = 우리 300 MPa cold-press 계열(약간 낮음) |
| **porosity (모델 입력 범위)** ★ | **Φ ≈ 0.1–0.2** (그림 음영대 = 실험 보고 porosity) | SSB 양극 복합, ref [29] | stated (Fig 7a) | ⚠ *실험 보고 porosity 의 범위*로 인용 — 단일 측정값 아님; 우리 15.6 % 가 이 범위 안 |
| **cathode utilization θ_CAM** ★ | **θ_CAM = V_CAM^active / V_CAM** (활성 CAM 부피분율) | percolation 정의 | stated (Eq) | ⭐ 핵심 출력. = 우리 **f_AM^cc / dead-AM** 의 직접 대응 |
| **크기비 λ (핵심 변수)** ★ | **λ = D̄_CAM / D̄_SE** | — | stated | ⭐ 이 논문 전체의 지배 무차원수 |
| θ_CAM @ λ=1.67, f_CAM 변화 | f_CAM <70 wt% → **θ≈1**; >75 wt% → **급락** | D̄_CAM=5µm 고정 | stated (Fig 3a) | "75 wt% 위에서 percolation 약화 → utilization 감소" |
| θ_CAM @ f_CAM=70 wt%, λ 변화 | **λ<1 → θ 급락**; **λ≈1.67 → θ≈1**(full util.) | D̄_CAM=5µm | stated (Fig 3b) | ⭐ "고정 로딩서 SE 입경만 줄여(λ↑) θ 20→100%" |
| **full-util. 임계 λ_min** ★ | f_CAM=70 → **λ_min=1.67**; 75 wt% → **λ_min=2.1**(98% util.) | θ_CAM 98% 기준 | stated (Fig 3d) | ⭐ **로딩↑ → 필요 λ↑** (= dip 의 조성의존을 λ 로 정량) |
| λ_min 예시 (75 wt%, 98% util) | D̄_CAM 5µm → **D̄_SE 2.4µm**; 20µm → **9.5µm** | λ_min=2.1 | stated | 설계 지침 핵심 숫자 |
| **고-CAM 로딩 달성** ★ | **f_CAM=80 wt% ≈ 50 vol%**(=액체셀 수준) @ near-full util. | D̄_CAM=12µm + D̄_SE=1.5µm (λ=8) | stated (Fig 5d,§4) | ⭐ **"단순 혼합·가압으로 >50 vol% CAM"** = 논문 타이틀 결과 |
| utilization @ f_CAM=80, λ=8(1→8) | θ_CAM **16%→20%** (λ 1→8) | D̄_SE 3µm, D̄_CAM=5→… | stated 본문(p.5) | 80 wt%서 λ 키워도 5µm CAM 으론 미흡 → 큰 CAM 필요 |
| utilization @ f_CAM=85 wt% | λ 1→8 → θ_CAM "only slightly" 상승 | — | stated | 고로딩 한계 |
| visualization util. (Fig 4) | model b θ_CAM=**52%**, model c **25%** | f_CAM=80, D̄_SE 3 vs 5µm | stated (Fig 4) | 큰 SE(5µm) → 활성 CAM 절반↓ |
| **SE 입경별 σ_ion(LPS)** ★ | bulk(SPEX) **0.39 mS/cm**; ball-mill 작을수록 **σ_ion 감소**(GB↑) | Table S3 | stated 본문(p.3) | ⚠ 작은 SE = σ_ion *낮아짐*(재료) 인데도 utilization↑(packing) → **"size=packing not σ"** |
| **실험 용량 (5µm NMC, λ 스윕)** | D̄_SE 8/5/3/1.5µm → ~**75 / 125 / >150 / >150 mAh/g**(λ↑→용량↑) | f_CAM=60 wt%, 5µm NMC | digitized Fig 5a/stated | 작은 SE(큰 λ) = 큰 용량 = θ_CAM↑ 실험검증 |
| 실험 용량 (λ=2.5→0.6, 5µm CAM) | SE 2µm→8µm → ~**155→~80 mAh/g** (모델·실험 일치) | Fig 5b | digitized Fig 5b | λ 2.5(SE 2µm) full → λ 0.6(SE 8µm) 반토막 |
| **CAM 입경 효과** ★ | 12µm CAM > 5µm CAM **용량 더 큼**(f_CAM=80, SE 3·1.5µm) | Fig 5c–e | stated | ⭐ **큰 CAM = 표면적당 SE-접촉 확률↑ → percolation↑** (반직관) |
| 실험 용량 (CAM 4→12µm) | 3µm SE: ~80→~140; 1.5µm SE: ~95→~130 mAh/g | f_CAM=80 wt% | digitized Fig 5e | 모델·실험 good agreement |
| 최대 실험용량(정규화 기준) | **155 mAh/g**(관측 최대) × θ_CAM(모델) = 모델 용량 | — | stated | 모델→용량 환산법 |
| Fig 6 (60/70/80 wt% 용량) | 60·70 wt% > **150 mAh/g**(λ≥1.67 고-util 영역); 80 wt% 급락 | 3µm & 1.5µm LPS, 5µm NMC | stated/digitized Fig 6 | f_CAM=60→70 wt% **용량 손실 없이** 증가 가능(1.5µm SE) |
| **σ_thermal / σ_electronic** | **n/a** | — | — | 이 논문 = 이온 percolation 만. 전자전도는 *CNF 가 담당*(모델 미포함) |
| coverage / 접촉면적% | **n/a**(정량 없음) | — | — | "접촉면적 정확기술 = LPS 소성변형 모델 필요"라고 *향후 과제* 명시(§4) |
| coordination Z | **n/a** | — | — | percolation 경로(최단경로)만, 배위수 직접 측정 없음 |
| **E_SE / σ_y / ν** | **n/a (수치 미보고)** | LPS | — | Hertz 접촉에 탄성 파라미터 쓰지만 *본문에 값 없음*(SI S1). 소성캡 없음(rigid Hertz) |
| Heckel P_y / knee | **n/a** | — | — | Heckel 분석 없음(단일압력 200 MPa, 압밀곡선 미보고) |
| **PSD (D̄ / σ)** ★ | **SE: 1.5 / 3 / 5 / 8 µm**; **CAM: 5 / 12 µm** | log-normal, SEM-matched | stated (Fig 1b, Fig 2) | ⭐ 우리 12:4:1 과 직접 비교축. λ 범위 **0.6–8** |
| **box-size 수렴 규칙** ★ | **L_box = 1.5·L_min ≈ 15·D̄_max** | RVE 수렴 | stated (§2.1, SI S2) | = 우리 RVE 박스팩터(우리 ~35)와 동류 — 절대값 다름 |

### 핵심 5개 데이터 포인트 (외워둘 값)
- **λ = D̄_CAM / D̄_SE** — 이 논문의 지배 무차원수. **"SE 를 CAM 보다 작게(λ>1)"** 가 황금률.
- **λ_min(full util.): 70 wt% → 1.67 / 75 wt% → 2.1** — **로딩↑ → 필요 λ↑** (조성-의존 dip 을 λ 로 정량).
- **f_CAM=80 wt% ≈ 50 vol% CAM**(액체셀 수준) = **D̄_CAM 12µm + D̄_SE 1.5µm (λ=8)** 로 달성.
- **작은 SE = σ_ion(재료) *낮아짐* 인데도 utilization↑** → **size=PACKING(연결성) not σ-material**(우리 결론과 동일).
- **큰 CAM = utilization↑**(반직관) — 큰 입자가 *표면적당 percolating-SE 접촉 확률↑* (Discussion §4 명시).

---

## 4. 시뮬레이션 방법 ★

- **code / version**: ⭐ **LIGGGHTS (open-source DEM) = 우리와 동일 코드** (refs [18–20] = Kloss/Goniva LIGGGHTS, Di Renzo, Schöpfer). + **percolation 분석**(자체, Dijkstra 류 최단경로). + **QuickSurf**(시각화, Fig 4 SE surface).
- **DEM 접촉법칙**: ⭐ **Hertz** granular contact (normal + tangential, refs [22 Zhang–Makse, 23 Sakuda]) + **damping** + **frictional yield**(마찰만, 소성 SHAPE 아님). = 우리 hooke/hysteresis 와 *같은 계열의 탄성-접촉*(우리는 hysteresis, 그들은 Hertz). **항복캡/소성흐름 없음** — rigid sphere.
- **재료 파라미터**: E_SE·E_CAM·ν·μ 를 SI S1 에 두되 **본문에 수치 미보고**. (Hertz 탄성 + 마찰 yield. 소성 항복응력 σ_y 캡 *없음*.)
- **bond/binder 모델**: **없음.** CNF(도전제) 는 **모델에 명시적 미포함** — prefactor **0.95**(=5 wt% CNF 질량 보정)로만 f_CAM·f_SE 정의: `f_CAM = 0.95·M_CAM/(M_CAM+M_SE)`, `f_SE = 0.95·M_SE/(M_CAM+M_SE)`. SE 다공/바인더 morphology 없음.
- **MPM/continuum**: ⭐ **없음.** 입자는 *영원한 강체 구*. **소성 SHAPE 변화·void-fill 흐름 전혀 없음.** ⚠ ★ 단 §3.2·§4 에서 **"입자간 접촉면적의 정확한 기술은 LPS 의 *소성변형* 모델링을 요구하며, 그 변형 정도가 접촉면적·따라서 접촉저항을 좌우한다"** 고 *명시적으로 자기 한계를 인정*(ref [29] Choi 2018 LPS 소성관측 인용) → **정확히 우리 MPM(SHAPE 소성) + Stage-E(소성 접촉면적)가 메우는 칸**.
- **전달 솔버 (σ)** ★: ⭐ **유효 σ 를 *안 푼다*** — **이온 percolation *연결성*** 만:
  - **CAM "active" 판정**: 한 CAM 입자가 *최소 1개 Li-percolation 경로* 로 bulk-SE(separator)에 연결되면 active(Fig 1c).
  - **네트워크**: CAM 입자를 노드로(이웃 CAM 연결), SE 입자를 **bulk-SE 경계의 target 노드**로, CAM 을 source 로 → **각 CAM 의 *최단 percolating 경로*** 추출(ref [26] Zeng–Church = 그래프 최단경로) → CAM 이 separator 에 닿는가 판정.
  - **이온은 SE 로만**(refs [24,25]): "Li 확산이 CAM 보다 SE 에서 훨씬 빠름 → percolation 경로는 SE 입자로만" → SE=이온 backbone. **constriction/contact 저항 *없음*** — 연결성(존재)까지만.
  - ⚠ 즉 그들 "transport" = **Bielefeld 2019 와 같은 *percolation 연결성* 수준** (σ 실값 아님). 단 Bielefeld 가 *cluster 부피/면적* 이면 Shi 는 *각 CAM 의 separator 도달여부(최단경로)* → **utilization** 으로 환산.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - ⭐ **구(sphere) 만, 소성 SHAPE 없음(rigid).** AM·SE 둘 다 강체 구. *형상변화·δ-overlap-as-flow 없음* — Hertz 탄성 접촉 + 마찰. = 우리 DEM rigid-sphere 가정과 **물리적으로 동일**.
  - ⭐ **bi-disperse(이성분 크기) + log-normal PSD.** SE 4크기(1.5/3/5/8µm) × CAM 2크기(5/12µm), 각 성분 **log-normal 분포**(SEM σ 매칭, Fig 1b). λ 범위 **0.6–8**. → **우리 12:4:1 이산 다분산과 동형의 *연속-크기비* 스윕**.
  - **압밀 = 재배열 + Hertz 탄성중첩** (소성흐름 아님). 평판을 위에서 prescribed-velocity 로 내려 200 MPa 도달 → 정지 → 운동E→0 까지 hold(=우리 hold protocol).
- **도메인/RVE / seeds / 압력범위**: 입방 V_box, **L_box = 1.5·L_min ≈ 15·D̄_max**(수렴, SI S2). 전이영역 통계 위해 **각 조건 ≥3 random initial config 평균**. 단일압력 **200 MPa**(separator ~100 MPa). 4벽 + 상하 평판 granular wall.
- **특이사항/튜닝**: CNF prefactor 0.95; θ_CAM 환산 = (모델 θ_CAM) × (실험 관측 최대용량 155 mAh/g) = 모델 예측 용량 → Fig 5b/d 에서 실험과 직접 비교. **모델 검증을 12µm CAM 으로 반복**(Fig S2)해 "λ 효과지 SE-크기 단독 아님" 확인.

---

## 5. 섹션별 결과 — ALL numbers

### 5.0 Abstract / Introduction (p.1–2)
- **문제:** SSB 복합양극은 보통 **SE 30–50 wt%** 필요 → **CAM 부피분율 낮음 → 에너지밀도 낮음.** 액체셀은 CAM **>90 wt% (>50 vol%)** → SSB 가 경쟁하려면 고-CAM 로딩 필수.
- **반직관 핵심 메시지:** "**고-CAM 로딩에서 utilization 은 CAM/SE 입자 크기비(λ)에 강하게 의존**" — **SE 입경↓ + CAM 입경↑(λ↑)** → **>50 vol% CAM 고-utilization 을 *단순 혼합·가압* 으로** 달성. "**가장 결정적 인자 = SE 를 CAM 보다 작게**"(by factor 2–3 → utilization 20%→100%).
- **이온 percolation 이 율속:** 결과는 "**cold-press SSB 양극에서 이온 percolation 이 limiting factor**"라는 개념과 정합.

### 5.1 Computational & Experimental Methods (p.2–3)
- **§2.1 모델링:** 무작위 삽입 구 CAM/SE → 입방 도메인. CNF 미포함(0.95 prefactor). log-normal PSD(Fig 1b, SEM 매칭). **LIGGGHTS DEM** + Hertz + 평판 200 MPa 압밀 → 정지. CAM active 판정 = 최단 percolating 경로로 separator 도달(Fig 1c). θ_CAM = V_CAM^active/V_CAM. **box 수렴 L_box=1.5L_min≈15D̄_max**, 각 조건 ≥3 config 평균.
- **§2.2 실험:** **NMC(D̄=5µm, Samsung Japan) + 대입경 NMC(D̄=12µm, MSE Supplies)**, 둘 다 **6–8 nm LZO 코팅**(Ito ref [6], 계면반응 억제 → 입경효과만). **Bulk LPS** = Li₂S(99.98%)+P₂S₅(99%) **SPEX 8000M 50mL ZrO₂, 200 min** → σ_ion **0.39 mS/cm**(ref [27] 일치). **작은 LPS** = wet ball-mill(heptane+dibutyl ether, Retsch PM200, ZrO₂ 1–10mm) → **1.5/3/5/8 µm**, ⚠ **작을수록 σ_ion *감소*** (GB/입계저항↑ + 잔류용매, Table S3). **셀:** PEEK 실린더(내경 8mm)+SS 로드 집전체; bulk LPS 35mg @~100 MPa → 양극(5mg)@~200 MPa → In 음극 @~200 MPa. **5 MPa 작동압**(스프링). Bio-Logic VMP300, 2–3.7 V vs In, 0.05 mA/cm², CCCV(5h hold @top).

### 5.2 Influence of Particle Size Ratio & Cathode Loading on θ_CAM (p.4 — Fig 3, 핵심)
- **Fig 3a (λ=1.67 고정, f_CAM 60→90 wt%):** f_CAM **<70 wt% → θ_CAM=1**(full util.); **>75 wt% → θ_CAM 급락.** ⇒ "Li percolation 이 SE 양 감소(=CAM↑)로 약화." 고정 λ 에 대응하는 **최대 f_CAM(=full util. 유지)** 존재(이 경우 70 wt%).
- **Fig 3b (f_CAM=70 wt% 고정, λ=D̄_CAM/D̄_SE 변화, D̄_CAM=5µm, SE 1.5/3/5/8/12/15µm):** ⭐ **θ_CAM 이 *오직 SE 입경 변경만으로* 20%↔100% 변동.** **λ<1 → percolation 명백히 감소**(SE 가 CAM 보다 크면 나쁨). **λ≈1.67 → θ≈1.** "최소 λ 가 주어진 로딩의 full util. 에 필요." **12µm CAM 으로도 같은 결과**(Fig S2) → "효과는 λ 때문이지 SE-크기 단독 아님."
- **Fig 3c (θ_CAM heatmap, λ × f_CAM):** percolation 은 **f_CAM↓(=위→아래 SE wt%↑)** 또는 **λ↑(좌→우)** 로 *항상* 개선. ⇒ **고-로딩 고용량 = 큰 λ 필요.** **λ<1 은 어떤 경우든 악화**(SE 는 *항상* CAM 보다 작아야 — separator 의 "큰 SE 선호"와 정반대).
- **Fig 3d (full-util. 임계 λ vs f_CAM, θ_CAM=80/90/98% 곡선):** ⭐ **λ_min 이 f_CAM 에 강의존.** 예: **75 wt% 로딩서 98% util. → λ_min=2.1** → 5µm CAM 이면 **SE 2.4µm**, 20µm CAM 이면 **SE 9.5µm**. f_CAM=80 wt%서 **λ 1→3 → θ 30%→60% 두 배**; 그러나 **f_CAM=85 wt%서 λ 1→8 → θ 16%→20% (미미)** → 고로딩 한계.

### 5.3 Visualization of Ionic Percolating Networks (p.5 — Fig 4)
- 3 모델: (a) f_CAM=70, D̄_SE=3µm; (b) f_CAM=80, D̄_SE=3µm; (c) f_CAM=80, D̄_SE=5µm (모두 D̄_CAM=5µm). gray=CAM, yellow=SE percolating network(QuickSurf), 우열=active/inactive CAM.
- **(a)→(b):** f_CAM 70→80 wt%(λ 고정 1.67) → SE 부피↓ → **percolating network 작아지고 덜 균일 → θ_CAM 98%→…감소.**
- **(b) vs (c):** f_CAM=80 고정, **SE 3µm→5µm(λ 1.67→1)** → **percolating network 더 작아짐** → 활성 CAM 이 separator 근처에만 → **θ_CAM = 52%(b) vs 25%(c)** (큰 SE 가 활성 CAM 절반↓). ⭐ "큰 SE → 작은 percolation network → 적은 활성 CAM."

### 5.4 Experimental Validation (p.5–6 — Fig 5, 6, 핵심 검증)
- **Fig 5a (4 cells, LPS 8/5/3/1.5µm, f_CAM=60 wt%, 5µm NMC, 1st-cycle V-curve):** **8µm·5µm LPS → 작은 용량(~75·~125 mAh/g)** vs **3µm·1.5µm LPS → full(>150 mAh/g)** → "**작은 SE(큰 λ) 이 θ_CAM↑**" 실험증명.
- **Fig 5b (실험 vs 모델 용량, λ=2.5/1.3/0.8/0.6):** 모델 용량 = (155 mAh/g)×θ_CAM(Fig 3c). **good agreement.** λ 2.5(SE 2µm)→full ~155; λ 0.6(SE 8µm)→~80 mAh/g.
- **Fig 5c,d (5µm vs 12µm NMC, 3µm·1.5µm LPS, f_CAM=80 wt%):** **12µm CAM(검정) > 5µm CAM 용량** (양 LPS 크기 공통) → **큰 λ 가 θ_CAM 이득** 재확인.
- **Fig 5e (용량 vs CAM 크기 4→12µm):** 3µm SE·1.5µm SE 둘 다 **CAM 클수록 용량↑**, 모델·실험 일치. ⭐ "**큰 CAM = 표면적당 percolating-SE 접촉 확률↑** → θ_CAM↑"(반직관, §4 에서 해설).
- **Fig 6 (f_CAM=60/70/80 wt% 검증, 3µm·1.5µm LPS, 5µm NMC):** **60·70 wt%(λ≥1.67) 둘 다 고-util 영역(green)** → **용량 거의 동일 >150 mAh/g** → **f_CAM 60→70 wt% 를 용량손실 없이 증가 가능**(특히 1.5µm SE, λ=3.33). **80 wt%(low-θ red/purple 영역) → 급락**. 모델·실험 good agreement(Fig 6b,d).

### 5.5 Discussion (p.6–8)
- ⭐ **반직관 결과의 물리:** "큰 CAM = 긴 확산경로(불리)지만 **표면적이 커서 percolating SE 망에 접촉할 확률↑** → utilization↑. **액체셀 직관(큰 CAM 나쁨)은 SSB 에 그대로 안 통함.**" "Li percolation 이 율속" 일관.
- **f_CAM=80 wt% ≈ 50 vol%** (이전 보고 밀도·porosity 로 환산, ref [29]). near-full util. = **D̄_CAM 12µm + D̄_SE 1.5µm**. = 액체셀 수준.
- **>80 wt% 가능?** λ 더 키우면(SE sub-µm) 가능 — nano-SE 합성 동향(refs [14,15]) → 더 높은 로딩 동기. ⚠ 단 trade-off: **매우 큰 λ(아주 큰 CAM) = power density↓**(큰 CAM lithiate 느림, ref [24]); **아주 작은 SE = percolation 채널폭↓ + 입계↑ → SE 망 임피던스↑**(ref [30]) + **GB 저항(SE 선택의존)**. ⇒ **power vs energy trade-off 로 λ 최적화.**
- ⭐ ★ **접촉면적·소성변형(우리 MPM/Stage-E 직격):** "**λ 가 이온확산에 미치는 영향의 추가 정밀화는 입자간 *접촉면적* 같은 세부를 요구하며, 접촉면적의 정확한 기술은 *LPS 입자의 소성변형 모델링* 을 필요로 한다 — 이는 실험적으로 관측됐다(ref [29]). 변형 정도가 입자간 접촉면적·따라서 경계저항을 크게 좌우한다.**" → **자기 rigid-Hertz 모델의 한계를 명시 + 우리 MPM(SHAPE 소성)·Stage-E(Tabor 소성면적)·Holm constriction 이 메우는 칸을 *지목*.**
- **carbon(전자) percolation:** CNF 미포함 모델은 **이온 percolation 만** — 5 wt% CNF 가 전자 percolation 담당. "한 최근 연구(ref [13] Strauss): 도전제 없으면 *CAM 자체* 가 전자 percolation 가능" → "**전자 percolation 도 같은 입경효과 적용**"(우리 σ_e size-effect 와 동방향). carbon 추가 모델링은 입자수 10¹⁰ 초과로 계산불가(SuperP nm) → 향후.

### 5.6 Conclusion (p.8)
- **크기비 λ = D̄_CAM/D̄_SE 가 cold-press SSB 의 utilization·로딩 허용도를 지배** — 모델+실험 공통. **cathode utilization = percolation-controlled.** **큰 λ = 고-CAM 로딩 가능.** 고-로딩 regime 에서 utilization 이 *λ 에 가장 결정적.*
- ⭐ **"큰 CAM(12µm) + 작은 SE(1.5µm) 로 액체셀 수준(50 vol%) CAM 복합양극 제작 가능"** 시연. **SSB 양극 입경 최적화의 정량 가이드** 제공. (oxide SE Li₇La₃Zr₂O₁₂ 등에도 적용 가능 — 단 GB 기여는 SE 선택의존.)

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (a) 초기 입방→압밀 모식(L_box→두께 T, 200 MPa); (b) **PSD log-normal**(SE 1.5/3/5/8µm + CAM 5/12µm); (c) **CAM 2개의 이온 percolating 경로**(검은 점선, separator 까지) | ⭐ (b) = 우리 12:4:1 직접 비교축; (c) = 우리 percolation 최단경로/f_perc 와 *같은 그림*. 압밀모식 = 우리 DEM 평판압밀과 동일 |
| **2** | (a–d) LPS SEM 8/5/3/1.5µm + (e,f) LZO-NMC 5/12µm SEM | 실측 PSD 근거; 우리 입력 PSD 의 실험 대응 |
| **3** ★★ | (a) θ_CAM vs f_CAM @λ=1.67; (b) **θ_CAM vs λ @f_CAM=70**; (c) **θ_CAM heatmap(λ×f_CAM)**; (d) **임계 λ vs f_CAM(80/90/98% util.)** | ⭐⭐ **이 논문의 심장.** (b)=고정로딩서 λ↑→util.↑(size=packing); (c)=우리 porosity-조성-크기비 3D 스윕의 *utilization 판*; (d)=**dip 의 조성의존을 λ_min(f_CAM) 로 정량** |
| **4** | 3 모델 percolating SE network 시각화(QuickSurf): (a)70/3µm (b)80/3µm θ=52% (c)80/5µm θ=25% | 큰 SE→작은 network→적은 활성 CAM. = 우리 dead-AM 시각화의 대응(단 그들=이온망, 우리=σ 망) |
| **5** ★ | (a) V-curve 4 LPS크기(60 wt%); (b) **실험 vs 모델 용량(λ)**; (c,d) 5 vs 12µm NMC V-curve; (e) **용량 vs CAM크기(4→12µm) 모델·실험** | ⭐ **frame[4] 실험검증.** (b)(e) = 모델 utilization → 실험 용량 *직접 비교* = 우리 σ→용량 예측의 검증 템플릿 |
| **6** | (a,c) V-curve 60/70/80 wt%(3µm·1.5µm LPS); (b,d) 실험 vs 모델 용량 | f_CAM 60→70 wt% 용량손실 없이 증가(1.5µm SE) — 우리 production-core(70–85 wt%) 상한의 실험 |
| **7** | (a) **CAM vol% loading vs f_CAM(wt%)**, 음영=실험 porosity Φ=0.1–0.2; (b) θ_CAM heatmap(λ×CAM vol%) | ⭐ **wt%↔vol% 환산표(porosity 0.1–0.2 대역)** = 우리 wt%/vol% 매핑 직접 사용. 80 wt%≈50 vol% |

> 모든 transport 그림이 **utilization(θ_CAM, %) 또는 용량(mAh/g)** — **유효 σ(mS/cm) 곡선 없음.** ⇒ 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 *σ 직접 비교 불가*. 비교 가능 = *utilization·percolation·λ-효과·용량 추세*.

---

## 7. Post-processing ★

- **무엇**:
  - **cathode utilization θ_CAM = V_CAM^active/V_CAM** — 각 CAM 입자가 최단 Li-percolation 경로로 separator(bulk-SE)에 닿으면 active. = **percolation 연결성 → 활성분율**. (우리 **f_AM^cc / dead-AM** 의 정확한 대응 — 단 우리는 σ-가중, 그들은 *존재만*.)
  - **최단경로 percolation**: CAM 노드 그래프 + SE-경계 target → Dijkstra 류 최단경로(ref [26] Zeng–Church) → separator 도달 판정. **저항/전류/전위 없음 — 연결성만.**
  - **모델→용량 환산**: 예측용량 = θ_CAM(모델) × 155 mAh/g(실험 관측 최대) → Fig 5b/d/6b/d 에서 실험과 직접 대조.
  - **box-size 수렴**: L_box=1.5·L_min≈15·D̄_max (SI S2). 전이영역 ≥3 config 평균.
  - **σ_ion(LPS) vs 입경 측정**(재료, Table S3): bulk 0.39 → 작을수록 감소(GB↑). ⇒ utilization↑이 σ_material↑ *아님* 을 증명(packing).
- **도구**: **LIGGGHTS**(압밀 DEM), 자체 percolation/최단경로 코드, **QuickSurf**(Gaussian SE-surface 시각화, Fig 4), 실험 = SEM(Zeiss Gemini Ultra-55, ~200입자 평균 PSD)·Bio-Logic VMP300.
- **수치화·플롯·기록**: θ_CAM heatmap(λ×f_CAM, Fig 3c·7b), 임계-λ 곡선(Fig 3d), 실험-vs-모델 용량 산점(Fig 5b/e·6b/d), wt%↔vol% 환산(Fig 7a, porosity 음영대 0.1–0.2). **모든 종축 = θ_CAM(%) 또는 용량 — σ 아님.**

---

## 8. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⭐ 이 표가 핵심 — Shi 는 우리와 **같은 코드(LIGGGHTS)·같은 접촉계열(Hertz/탄성)·가장 가까운 소재(황화물+NMC)** 라 *방법-수준 직접 대조*가 가능한 드문 논문.

| 항목 | 이 논문 (Shi 2019/2020) | 우리 | 차이 / 이유 (rigid·plastic / 소재 / 2D·3D / 연결성·σ실값) |
|---|---|---|---|
| **DEM 코드** | ⭐ **LIGGGHTS** (refs 18–20) | **LIGGGHTS** | **동일.** 우리 DEM 방법론의 *직접 동료* (Bazzoun 과 함께) |
| **접촉법칙** | **Hertz** + damping + 마찰 yield, **소성 SHAPE 없음** | **hooke/hysteresis** + adhesion, **소성 SHAPE 없음** | 둘 다 *탄성-접촉 rigid-sphere*(Hertz vs hysteresis 차이만). **둘 다 δ-overlap 프록시, 진짜 흐름 아님** → 우리 18× 연화·그들 무연화(단일압력)는 *같은 rigid 한계* 다른 처리 |
| **입자 모델** | **구, rigid, log-normal bi-disperse** (SE 1.5–8 × CAM 5/12µm, λ 0.6–8) | **구, rigid, bimodal 12:4:1** + 18× 연화 | **거의 같음** — 둘 다 형상 안 변함. 그들 λ-연속스윕 = 우리 이산 12:4:1 의 *연속판* |
| **압밀 압력** | **200 MPa 단일** (separator 100) | **300 MPa**(제조) | 같은 cold-press 계열(약간 낮음). 둘 다 *제조압*(작동압 아님; 그들 작동 5 MPa) |
| **porosity** | **입력/환산 Φ=0.1–0.2**(실험 보고 범위, Fig 7a) | **15.6 %(DEM)/16.7 %(MPM)** real_14 | ⭐ **우리 15.6 % 가 그들 0.1–0.2 대역 *정중앙*** → 같은 자릿수 cross-check. 단 그들 porosity 는 *측정 안 함*(환산용 음영대) → 절대 동일시 금지, *대역 일치*만 |
| **transport** | ⭐ **이온 percolation *연결성*(최단경로 → utilization)** — **σ 실값 없음, constriction 없음, 전자·열 없음** | **Kirchhoff + Holm constriction σ_ionic/e/thermal 삼중항**(실값, LOOCV 0.975/0.953/0.903) | ⭐⭐ **우리가 한 층 위.** 그들 = "CAM 이 연결됐나(active?)"; 우리 = "그래서 σ 가 얼마 + constriction 으로 얼마 깎이나". = 우리 transport novelty 의 *정확한 좌표* |
| **utilization vs dead-AM** | **θ_CAM = V_active/V_CAM**(존재 기준) | **f_AM^cc / dead-AM**(σ-가중 연결분율) | **같은 개념** — 그들 θ_CAM 이 우리 dead-AM 의 *순수 기하 percolation 판*. 우리는 σ·fracture 가중 |
| **접촉면적** | **n/a — "정확기술엔 LPS 소성변형 모델 필요"라 *명시 향후과제*(§4, ref 29)** | **Stage-E Tabor+volume 소성 접촉면적** | ⭐ **그들이 *지목한* 칸을 우리가 채움.** Shi 가 직접 "소성변형이 접촉면적·경계저항 좌우"라 인정 = frame[5] 분업의 *그들 측 인정* |
| **소성/morphology** | **없음**(rigid Hertz) | **MPM 진짜 SHAPE 소성**(SEM 일치)·void-fill·Σdg | morphology = 우리 MPM 고유. 그들 rigid-구 한계를 우리 MPM 이 메움(frame[1]/[2]) |
| **크기비 효과** | ⭐ **λ=D_CAM/D_SE 가 utilization 지배(λ↑→util↑)** — *작은 SE → σ_material↓에도 util↑* | **"size=PACKING not overlap"**(σ_ionic·σ_e size-effect=기하) | ⭐⭐ **결론 *동일*.** Shi 실험: 작은 SE = σ_ion(LPS)*낮아짐* 인데도 utilization↑ → **순수 packing/연결성** = 우리 결론의 *모델+실험 증거* |
| **큰 CAM 효과** | ⭐ **큰 CAM = utilization↑**(표면적당 SE-접촉 확률↑, 반직관) | DEM: 큰 AM = AM-AM 접촉↑·packing(σ_e φ_AM⁴·√A) | **같은 방향** — 큰 CAM 이 percolation 유리. Kang2025 "큰 입자 균열" caveat 과 결합(packing 이득 ↔ 균열 대가) |
| **Furnas dip** | ⭐ **dip 의 *조성의존*을 λ_min(f_CAM) 로 정량**(70→1.67, 75→2.1) | **dip @ AM 70–85 wt%**(de Larrard/McGeary 기하); **소성 MPM 재현 못 함** | ⭐ **상보.** 우리 dip(porosity 최저 조성) ↔ 그들 λ_min(util.=1 유지 한계). **"로딩↑→필요 λ↑"가 우리 dip 의 조성-크기비 결합의 *실험판*** |
| **검증** | ⭐ **실험 4 SE×3 로딩×2 CAM 셀, 모델 용량 good agreement** | solver=ground truth + Bazzoun/Minnmann/Cronau 외부앵커 | ⭐ **Shi = 우리 σ→용량 예측의 *검증 템플릿*** (그들이 직접 모델→용량→실험 닫음) |
| **소재** | **LPS glass(σ 0.39) + NMC532-LZO** | **LPSCl(σ ~1–3) + NMC811** | ⚠ **σ·용량 절대전이 금지.** 둘 다 황화물+층상NMC+cold-press → *추세*만 frame[4] 앵커 |

**핵심 차이 3줄:** (1) ⭐ **같은 LIGGGHTS+Hertz rigid-구로 압밀+percolation 까지는 우리와 *형제*** — 단 그들은 **이온 percolation *연결성*(utilization)** 까지, 우리는 그 위에 **σ 실값(Holm constriction)+삼중항** 을 *solve*; (2) ⭐ **결론이 같다: "작은 SE+큰 CAM(λ↑) → utilization↑"이 우리 "size=PACKING not overlap"의 모델+실험 증거**; (3) ⭐ **그들이 직접 "LPS 소성변형 모델 필요"라 지목한 칸(접촉면적·morphology)을 우리 MPM/Stage-E 가 채움** = frame[5] 분업의 *그들 측 명시 인정*.

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) — 심층

### A.1 ⭐ "size = PACKING not overlap" — Shi 의 실험이 우리 결론의 *직접 증거*
우리 CLAUDE.md 의 가장 반복되는 결론 중 하나: **σ_ionic·σ_e 의 입경 효과는 *기하 packing*(Furnas) 이지 *overlap*(δ) 이 아니다.**
(예: "Overlap (δ/R ≈ size-scale-invariant at fixed P) can't flip with composition → the size-ordering is geometric Furnas
packing; overlap only sets the absolute level." / Minnmann2021 "fine SE → σ_ion,eff↑ = packing/τ 효과".)

**Shi 가 이걸 *실험으로* 못박는다:**
- Table S3: **작은 LPS 입자 = σ_ion(재료) 가 *낮아짐*** (입계저항↑ + 잔류용매). 즉 *재료* 관점에선 작은 SE 가 불리.
- 그런데 Fig 3b·5a: **작은 SE(큰 λ) = cathode utilization↑ → 용량↑.** ⇒ **utilization 이득은 σ_material 이 아니라 *packing/연결성*(작은 SE 가 CAM 간극을 채워 percolation 망을 촘촘히)** 에서 온다.
- ⭐ **이것이 정확히 우리 결론.** 우리 σ_ionic 의 size-effect 가 Cronau(r_SE) (재료 GB) 와 packing(φ_eff·CN²·cov) *둘 다* 를 담고, **packing 항이 size-ordering 을 지배**한다는 것 — Shi 가 "재료 σ↓ vs utilization↑" 의 *상반 부호* 로 **packing 이 이긴다** 를 실험분리. → **우리 σ_ionic 폼의 size 처리(packing-dominant)의 frame[4] 실험 정당화.**
- ⚠ 단 *방향(부호)* 만 전이: 그들 LPS-glass σ 0.39, 우리 LPSCl ~1–3. 절대 σ·utilization 숫자 전이 금지.

### A.2 ⭐ 크기비 λ ↔ 우리 12:4:1·Furnas dip — *연속 λ 스윕* vs *이산 크기비*
- **우리:** AM:SE = **12:4:1**(D̄_CAM_P:D̄_CAM_S:D̄_SE ≈ 12µm:4µm:1µm) bimodal → **Furnas dip @ AM 70–85 wt%**(porosity 최저). 우리 표현: "AM_P:SE=12:1(≫7=McGeary 임계, dip 깊음), AM_S:SE=4:1(<7, 부분충전)".
- **Shi:** **λ = D̄_CAM/D̄_SE 연속 스윕(0.6–8)**, **λ_min(full util.) = f(f_CAM)** (70 wt%→1.67, 75→2.1, 80 wt%→매우 큼).
- ⭐ **대응:** 우리 12:4:1 을 λ 로 풀면 **AM_P/SE λ=12, AM_S/SE λ=4** → *둘 다 Shi 의 "λ>1, 좋은 영역"*. 즉 **우리 12:4:1 은 Shi 의 high-utilization 설계와 정합** — 우리 production-core(AM 70–85 wt%)에서 λ=4~12 이면 Shi Fig 3d 의 λ_min(70 wt%=1.67, 75=2.1, 80≈3–8) 을 *충족하거나 상회*. ⇒ **우리 12:4:1·production-core 가 Shi 가 실험증명한 "고-CAM 고-utilization" 영역 안에 있다**(우리 설계의 외부 검증).
- ⭐ **dip 의 조성의존 = Shi 의 λ_min(f_CAM):** 우리 dip 이 *조성에 따라 깊이/위치가 변하는* 이유(AM_P-rich 서 깊고 AM_S-rich 서 얕음)를, Shi 의 **"로딩↑ → 필요 λ↑"**(Fig 3d) 가 *transport 측에서* 보강. 우리 dip = *porosity 최저* 조성, Shi λ_min = *utilization=1 유지* 한계 — **둘은 다른 양**(packing porosity vs ionic 연결성)이지만 *같은 크기비-조성 결합의 두 면*. → **우리 porosity 관계식의 "크기비 항"(McGeary 7:1 기하)에 더해, *utilization 측 λ 항*도 별개로 존재**함을 Shi 가 보임.
- ⚠ **frame[4] 비교 주의:** 우리 dip 은 *기하 porosity*(McGeary/de Larrard, 소성 MPM 재현불가), Shi λ_min 은 *이온 percolation 연결성*. **dip(porosity)↔λ_min(utilization) 직접 등치 금지** — 둘 다 "크기비가 조성에 따라 packing/연결성을 지배"라는 *공통 물리*의 다른 측정.

### A.3 ⭐ "큰 CAM = utilization↑" (반직관) — 우리 σ_e 큰-AM 효과 + Kang2025 균열 caveat
- **Shi (§4):** 큰 CAM 은 *확산경로 길어 불리* 하지만 **표면적이 커서 percolating-SE 망에 접촉할 확률↑ → utilization↑.** "액체셀의 '큰 CAM 나쁨' 직관이 SSB 엔 안 통함."
- **우리 σ_e (Stage 22.5):** σ_e ∝ φ_AM⁴·**√A_AM-AM**·NCM(r) — 큰 AM 은 AM-AM 접촉수·면적↑ → σ_e↑(같은 방향, *전자* 측). Shi 는 *이온* utilization 측에서 같은 "큰 CAM 유리" 를 보임.
- ⭐ **단 Kang2025(랩 자체논문) caveat 결합:** Kang 은 **큰 입자(10µm)가 사이클 균열↑**(유지 47.7% vs 67.3%@100cyc, c_Li 구배 ~10×) → **packing/utilization 이득(Shi) ↔ 사이클 균열 대가(Kang)** 의 trade-off. ⇒ **우리 모델은 둘 다 표현해야:** Shi 의 "큰 CAM packing/utilization↑"(우리 σ·porosity packing) + Kang 의 "큰 CAM 균열↑"(우리 Auerbach/fracture-Holm 의 *입경-스케일링* — 큰 AM_P 일수록 fracture↑). Shi(압밀-시점 packing 이득) + Kang(사이클 균열 대가)이 **우리 fracture-aware σ 의 입경-의존을 양방향으로 정의**.

### A.4 ⭐ 그들 "percolation 연결성" vs 우리 "Kirchhoff/Holm σ 실값" — novelty 의 정확한 좌표
Shi 의 transport 는 **Bielefeld 2019 와 같은 *percolation 연결성* 층**: "각 CAM 이 최단경로로 separator 에 닿는가?"(Fig 1c) → utilization.
**저항·전류·전위 없음.** 본문이 직접 인정(§4): "**λ 효과의 추가 정밀화는 입자간 접촉면적 같은 세부를 요구**" — 즉 *연결성*에서 멈췄음을 자인.

우리는 *그 위 한 층* 을 더 간다:
- DEM 접촉망의 **각 SE–SE 접촉을 R=1/(2σ·r_c)(Holm 1967)** 로 환산(r_c = 소성변형 깊이),
- **Kirchhoff Σ(φ_i−φ_j)/R=0** 를 풀어 **σ_eff,ion/e/thermal 실값**,
- **Stage-E(Tabor+volume)** 로 r_c(=접촉면적)를 *소성변형* 으로 재유도 — **Shi 가 "LPS 소성변형 모델 필요"라 지목한 바로 그것.**
- ⇒ **Shi(+Bielefeld 2019) = connectivity / utilization; 우리 = conductivity with constriction physics + 삼중항.** **이게 우리 transport novelty 의 정확한 위치**, 그리고 *같은 Ceder/Janek 계열이 스스로 인정한 빈 칸*(Shi §4 "소성변형 모델 필요" + Bielefeld "constriction=future, Greenwood").
- ⭐ **Bazzoun 2026(같은 LIGGGHTS+LPSCl) = 그 RNM/Holm σ 솔버를 *실제로 추가*** → **Bielefeld 2019(percolation) → Shi 2019(percolation+압밀+실험, 같은 코드) → Bazzoun 2026(RNM/Holm σ) → 우리(σ 삼중항+Stage-E+MPM)** 라는 *field 진화*의 자연스러운 끝.

> 대응 매핑: Shi **θ_CAM(active)** ↔ 우리 **f_AM^cc/dead-AM**; Shi **최단 percolation 경로** ↔ 우리 **f_perc_x/y/z + Dijkstra τ**; Shi **λ=D_CAM/D_SE** ↔ 우리 **r_AM/r_SE 크기비(12:4:1)**; Shi **"접촉면적=소성변형 필요"(미실현)** ↔ 우리 **Stage-E 소성 접촉면적(실현)**.

### A.5 porosity 의 의미 차이 (절대 동일시 금지)
- Shi porosity **Φ=0.1–0.2** = *실험 보고 porosity 의 범위*(Fig 7a 음영대, wt%↔vol% 환산용) — 그들이 *측정/예측한 단일값 아님*.
- 우리 **15.6 %(DEM)/16.7 %(MPM)** = *압밀로 예측/측정한 단일값*.
- ⇒ **우리 15.6 % 가 그들 0.1–0.2 대역 정중앙** = 같은 자릿수 cross-check(LPS-glass·NMC532 ≠ LPSCl·NMC811 이라 *대역 일치* 까지만). **그들 0.1–0.2 ≠ 우리 단일 15.6 %** 동일시 금지. (CSV Block 에 명시.)

---

## B. 적용가능성 (applicability to our LIGGGHTS DEM model)

### B.1 ⭐ frame[4] 외부 실험 앵커 — *utilization·용량 vs 크기비/로딩* (소재-매치 caveat)
Shi 는 **우리가 못 갖던 *모델→실험 닫힌 검증*** 을 제공: **모델 utilization → ×155 mAh/g → 실험 용량과 good agreement**(Fig 5b/e·6b/d).
우리도 σ→용량을 예측하지만 *직접 실험검증이 부족* → **Shi 의 "λ↑→util↑→용량↑" 추세를 우리 σ_ionic·dead-AM·percolation 의 frame[4] 외부 앵커로 채택**:
- **anchor 1 (size=packing):** "작은 SE = σ_material↓ 인데도 utilization↑" → 우리 σ_ionic size-effect 가 *packing-dominant* 임을 실험정당화 (A.1).
- **anchor 2 (λ_min vs 로딩):** **f_CAM 70→1.67, 75→2.1, 80 wt%→≈3–8** (full util.) → 우리 production-core(AM 70–85 wt%)·12:4:1(λ=4–12) 가 *Shi 의 고-util 영역 안* 임을 확인 (A.2).
- **anchor 3 (porosity 대역):** Φ=0.1–0.2 ⊃ 우리 15.6 % → 같은 자릿수 (A.5).
- ⚠ **material-match caveat:** σ·용량 *절대값* 은 LPS-glass(σ 0.39)·NMC532-LZO → **추세/부호만** 전이. 절대 σ 앵커는 LPSCl 쪽 **Minnmann(0.17)·Bazzoun(0.137)·Cronau(3.0)** 소유.

### B.2 우리 composition/size predictor 로의 매핑
| 우리 predictor 입력/출력 | Shi 대응 | 인용/적용 |
|---|---|---|
| **크기비 r_AM/r_SE (12:4:1)** | **λ = D̄_CAM/D̄_SE (0.6–8)** | 우리 12:4:1 = λ 4·12 → Shi 고-util 영역. 우리 size-스윕의 *연속 λ* 외부맵 |
| **dead-AM / f_AM^cc** | **θ_CAM utilization** | Shi θ_CAM(λ,f_CAM) heatmap = 우리 dead-AM(조성,크기비)의 실험검증 trend |
| **σ_ionic size-effect (packing)** | **작은 SE→util↑ (σ_material↓에도)** | A.1 — packing-dominant 실험 정당화 |
| **production-core AM 70–85 wt%** | **f_CAM 60→70 wt% 용량손실 0**(1.5µm SE, Fig 6) | 우리 core 상한의 실험; 70 wt% 안전, 80 wt% 는 λ≥3 필요 |
| **wt% ↔ vol% 환산** | **Fig 7a (Φ=0.1–0.2 음영대)** | 우리 wt%/vol% 매핑에 직접 사용(80 wt%≈50 vol%) |
| **Furnas dip 조성의존** | **λ_min = f(f_CAM) (Fig 3d)** | dip 의 조성-크기비 결합의 *utilization 측* 대응(직접 등치 금지) |
| **Stage-E 소성 접촉면적** | **§4 "LPS 소성변형 모델 필요"(미실현)** | 그들이 지목, 우리가 실현 → novelty 인용 |

### B.3 ⭐ 우리 모델이 Shi 에 *더하는* 것 (그들 빈 칸 = 우리 novelty)
1. **σ 실값 + Holm constriction** (그들=percolation 연결성/utilization 만, σ 없음).
2. **삼중항(σ_ionic+σ_e+σ_thermal)** (그들=이온 percolation 만; 전자는 CNF 가 담당하나 *모델 미포함*, 열 전무).
3. **Stage-E 소성 접촉면적** — *그들이 직접 "필요하다"고 지목한* 칸(§4, ref 29).
4. **MPM 진짜 SHAPE 소성·void-fill·morphology** (그들=rigid Hertz).
5. **fracture-aware**(Auerbach/Holm) — Shi packing 이득 + Kang 균열 대가의 입경-스케일링.
6. **Furnas dip 의 *porosity* 정량**(de Larrard/McGeary) — Shi 는 utilization-λ 만, porosity-dip 미측정.
7. **solver→scaling-law LOOCV→predictor**(연속 예측 함수) — Shi 는 이산 스윕.

---

## C. ★ frame[4] 위치 (experimental anchor) — 실험은 *경쟁* 아니라 *앵커*

> frame[4]: DEM·MPM 은 각각 *실험에* 보정(서로가 아님). Shi 는 **실험(+같은-코드 DEM)** 이므로 우리 SIMULATION 의 *경쟁자가 아니라
> 외부 검증 앵커*. 우리 시뮬은 *그들이 실험한 packing/utilization 을 σ 로 예측하고, 그들이 못 한 σ-실값·소성·삼중항을 추가*.

- **Shi = 실험 앵커:** 모델(같은 LIGGGHTS) + **실험 셀**(4 SE×3 로딩×2 CAM)로 **"λ↑ → utilization↑ → 용량↑"** 을 *측정*. 이건 우리 σ_ionic·dead-AM·percolation·size=packing 결론이 *맞아야 할 실험 trend*.
- **우리 SIMULATION 이 더하는 것:** Shi 가 *utilization(연결성)* 까지면, 우리는 그 위에 **(i) σ_eff 실값(Kirchhoff/Holm constriction), (ii) σ_e+σ_thermal 삼중항, (iii) Stage-E 소성 접촉면적(=Shi 가 지목한 칸), (iv) MPM SHAPE 소성 morphology, (v) fracture, (vi) porosity-dip 정량, (vii) predictor 연속함수.** ⇒ **우리는 Shi 가 실험한 packing/utilization 을 *σ 로 정량 예측* 하고, 그들이 명시적으로 비운 칸을 채운다.**
- ⚠ **transferability caveat (반드시 병기):**
  - **소재:** SE = **LPS glass(σ_ion 0.39 mS/cm)** ≠ LPSCl(~1–3, ~3–8×↑); CAM = **NMC532-LZO** ≠ NMC811. → **σ·용량 절대값 전이 금지**, *크기비-utilization-packing 추세*만.
  - **transport 깊이:** 그들 = **연결성(percolation 존재/최단경로)** ; 우리 = **σ 실값**. → utilization↔σ *직접 수치 비교 불가*(우리 σ_ionic 0.04–0.18 ↔ 그들 θ_CAM% 는 *다른 양*).
  - **rigid-sphere:** 둘 다 소성 SHAPE 없음 — *packing/연결성 추세*는 공유하나, *소성 morphology·접촉면적 절대값*은 둘 다 없음(우리 MPM/Stage-E 가 우리 측에서 보강).
  - **porosity:** 그들 Φ=0.1–0.2 = *환산용 대역* ≠ 우리 측정 15.6 % → *대역 일치*만.
  - **압력:** 그들 200 MPa(제조)·5 MPa(작동) vs 우리 300 MPa(제조). 제조압 계열 동일, 절대 동일시 주의.
- **포지셔닝 한 줄:** "Shi 2019/2020 (Ceder, same LIGGGHTS + Hertz, NMC+LPS) experimentally + computationally proves that the particle
  size ratio λ=D_CAM/D_SE — not absolute loading — governs cathode utilization (small SE + large CAM → >50 vol% CAM at near-full
  capacity). This is the direct model+experiment anchor for our 'size = packing, not overlap' conclusion and our 12:4:1 / AM 70–85 wt%
  production core. We add what they explicitly defer (§4, 'accurate contact area requires modelling plastic deformation of LPS'): the
  Kirchhoff/Holm constriction-resistance *conductivity* solve (full ionic/electronic/thermal triad), Stage-E plastic contact area,
  and MPM plastic morphology."

---

## 9. 적용 인사이트 (내 연구에 어떻게)

- ① ⭐ **"size=packing not overlap"의 frame[4] 실험 앵커 확보:** Shi Table S3(작은 SE=σ_material↓) + Fig 3b/5a(작은 SE=utilization↑) = **재료 σ↓ 인데도 utilization↑** → packing 이 σ-material 을 이김. 우리 σ_ionic·σ_e 의 *packing-dominant size 처리* 를 paper/deck 에서 이 *상반-부호 실험분리* 로 정당화(이중 결론: 우리 결론 + Shi 실험).
- ② ⭐ **우리 12:4:1·production-core 가 Shi 고-util 영역 안:** λ_min(70→1.67, 75→2.1, 80 wt%→≈3–8) vs 우리 λ=4–12(12:4:1) → **우리 설계가 Shi 가 실험증명한 "고-CAM 고-utilization" regime 충족.** 우리 composition/size predictor 의 *외부 sanity-check*.
- ③ ⭐ **dip 의 조성의존 = Shi λ_min(f_CAM):** 우리 Furnas dip(porosity, McGeary 7:1 기하) 에 더해 **utilization 측 λ_min 항** 이 별개로 존재 — "로딩↑→필요 λ↑"(Fig 3d) 를 우리 porosity-조성-크기비 결합의 *transport 보강* 으로 인용(직접 등치 금지). 우리 porosity 관계식 = E-stiffness 항(Varkey) + 기하 크기비 항(McGeary) + *utilization-λ 항*(Shi).
- ④ ⭐ **"큰 CAM 유리 ↔ 균열 대가" trade-off:** Shi(큰 CAM=packing/utilization↑) + Kang2025(큰 CAM=사이클 균열↑) → **우리 fracture-aware σ 의 입경-스케일링**(큰 AM_P 일수록 Auerbach fracture↑)을 *양방향*으로 정의. 큰 CAM 의 power-density 한계(ref 24)도 우리 설계제약에 기록.
- ⑤ ⭐ **그들이 *지목한* 칸을 우리가 채움(§4):** Shi 가 "정확한 접촉면적엔 LPS 소성변형 모델 필요"라 *자인* → **우리 MPM(SHAPE 소성)+Stage-E(Tabor 소성면적)+Holm constriction** 이 *그 칸*. **frame[5] 분업의 *그들 측 명시 인정*** 으로 우리 novelty positioning 강화(Varkey "구=타협" + Bielefeld "constriction=future" + Shi "소성변형 필요" = 3편이 *같은 빈 칸*을 지목).
- ⑥ **wt%↔vol% 환산(Fig 7a, Φ=0.1–0.2):** **80 wt%≈50 vol%** 등 우리 wt%/vol% 매핑에 직접 사용. 우리 production-core(AM 70–85 wt%) = CAM ~45–55 vol%.

---

## 10. 인용 가능 문장 (deck/paper용)

- "Using the same LIGGGHTS DEM and Hertzian contact as ours, Shi et al. (Ceder group, Adv. Energy Mater. 2020) demonstrate — by
  both modeling and experiment, in an NMC+LPS composite — that the *particle size ratio* λ = D̄_CAM/D̄_SE, not the absolute cathode
  loading, governs cathode utilization: keeping the SE smaller than the CAM (λ>1) lifts utilization from ~20 % to ~100 % at fixed
  loading and enables >50 vol% CAM (liquid-cell level) by simple mixing and pressing."
- "Shi's result that *smaller SE particles raise utilization even though their intrinsic σ_ion decreases* (Table S3) is the direct
  experimental evidence for our conclusion that the size effect on σ_ionic/σ_e is geometric *packing/connectivity*, not contact
  *overlap* — packing wins over the material-σ penalty."
- "Their full-utilization threshold λ_min(f_CAM) (1.67 at 70 wt%, 2.1 at 75 wt%) places our 12:4:1 design (λ = 4–12) and AM 70–85 wt%
  production core squarely inside the experimentally-validated high-utilization regime."
- "Shi's model resolves transport only to ionic-percolation *connectivity* (utilization via shortest path), and the paper explicitly
  states that an accurate description of inter-particle contact area 'requires modelling the plastic deformation of LPS particles'
  (§4). Our Kirchhoff/Holm constriction-resistance conductivity solve, Stage-E plastic contact area, and MPM plastic morphology fill
  exactly that deferred gap — the same gap the Janek group's Bielefeld 2019 (constriction = future work, Greenwood 1966) also names."

---

## 11. 주의/한계 (over-claim 방지)

- **σ 절대 비교 *불가*.** 이 논문은 **유효 σ 를 *안 푼다*** — 이온 percolation *연결성*(최단경로 → utilization θ_CAM)·용량(mAh/g)까지. 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 *수치 직접 비교 금지*(utilization% 와 σ 는 *다른 양*). 비교 가능 = *λ-효과·utilization·percolation·용량·porosity-대역 추세*.
- **소재 절대전이 금지.** SE = **LPS glass(75Li₂S·25P₂S₅, σ_ion 0.39 mS/cm)** ≠ 우리 **LPSCl(σ ~1–3)**; CAM = **NMC532-LZO** ≠ **NMC811**. → σ·용량 절대값 끌어오기 금지. 우리 소재계 절대 σ 는 Minnmann/Bazzoun/Cronau/Lee 소유. *추세/부호만* frame[4].
- **rigid-sphere + Hertz, 소성 SHAPE 없음.** 우리 DEM 과 *같은 rigid-구 한계* — δ-overlap·Hertz 중첩은 소성 프록시지 *진짜 흐름 아님*. 단일압력 200 MPa(Heckel·압밀곡선·연화 없음). 우리 18× 연화·MPM 소성이 우리 측에서 보강(그들엔 없음). **그들이 직접 "LPS 소성변형 모델 필요"라 자인**(§4) — rigid-Hertz 의 접촉면적 한계를 *논문이 인정*.
- **transport = *연결성*(존재) 까지.** constriction/contact 저항 없음(Bielefeld 2019 와 같은 층). 전자 percolation 은 *CNF 가 담당하나 모델 미포함*; σ_thermal 전무. ⇒ 우리 삼중항·Holm·Stage-E 가 더하는 칸.
- **porosity = 환산용 대역(Φ=0.1–0.2), 측정/예측 단일값 아님.** Fig 7a 음영대 = *실험 보고 porosity 범위*(ref 29). 우리 15.6 % 와 *대역 일치*만(같은 자릿수); **단일값 동일시 금지.**
- **utilization vs porosity-dip 직접 등치 금지.** Shi λ_min(utilization=1 유지) ≠ 우리 Furnas dip(porosity 최저, 기하). 둘 다 "크기비-조성 결합"의 *다른 면*(이온 연결성 vs 기하 packing). 소성 MPM 이 우리 dip 못 재현하는 frame[4] 논점과 별개 — Shi 의 λ-utilization 은 *연결성* 이라 *우리 dip(porosity)* 와 다른 양.
- **digitized vs stated:** λ_min(1.67/2.1)·θ 정의·f_CAM 임계(70/75/80 wt%)·porosity 대역(0.1–0.2)·λ 범위·PSD·box 규칙·80 wt%≈50 vol% = 모두 *본문 stated*. Fig 5/6 의 *용량 정확값*(75/125/150/155 mAh/g 등)·Fig 5e CAM-크기 곡선 = *digitized 추세*(±). CSV 에 source_type 으로 구분.
- **2D/3D:** 그들 모델은 **3D**(우리 DEM·MPM-3D 와 동일 차원) — 2D-3D caveat 은 우리 MPM-2D 챔피언에만 해당, Shi 비교엔 무관(둘 다 3D).
- **CNF/바인더 morphology 없음.** 도전제 5 wt% CNF = prefactor 0.95 로만 — 우리 CBD(VGCF/PTFE) morphology·σ-블로킹(Lee2025·Bielefeld2020) 효과 없음. *전자 percolation 정량* 은 우리(+그 논문들) 소유.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
