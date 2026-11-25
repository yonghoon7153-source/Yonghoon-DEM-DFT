<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md / galvezaranda2024_time_dependent_dl_calendering_microstructure.md -->
# **건조(slurry drying) DEM 궤적을 predictor–corrector 로 쪼개다** — VGG16→Conv1D 가 프레임 한 칸(1,500,000 DEM step)을 건너뛰고 nDEM(5–10 k) 실제 DEM step 이 그것을 물리 위로 되돌린다, NMC111 96 % AM / 4 % CBD 학습 → 94/6 외삽 — Galvez-Aranda / Fernandez / Franco (ACS Appl. Mater. Interfaces 2025)

> slug `galvezaranda2025_paml_vgg16_dem_slurry_drying` · DOI `10.1021/acsami.4c23103` · type `PAML 하이브리드(predictor–corrector): per-particle VGG16→Conv1D 시간-surrogate × DEM 투영자(nDEM) + GeoDict 2024 DiffuDict 후처리` · PDF `da1aad1a-67PHYS1.PDF` (+ SI `db3b4ca3-am4c23103_si_001.pdf` + 보충영상 2편) · digested `2026-09-11` · status ✅

> elements: Li
> methods: elastic

---

## 0. 이 논문이 우리에게 *왜* 중요한가 — 그리고 **정확히 어디까지만** 중요한가 (positioning)

**한 문장**: 이것은 `galvezaranda2024_time_dependent_dl_calendering_microstructure` 의 **자매편**이고,
그 카드 §12-1 이 *"다음 digest 후보 1순위"* 로 지목하며 **세 가지를 확인하라**고 적어 둔 바로 그 논문이다.
**세 가지가 전부 답해졌다 — 그리고 두 개는 앞 카드의 미해결을 *반대 방향으로* 정리한다.**

| 앞 카드 §12-1 의 질문 | **이 논문의 답** | 어디서 |
|---|---|---|
| ① VGG16 이 **DEM 루프 안**인가, 전/후처리인가 | ★ **루프 안이다 — 그러나 힘 계산 대체가 아니라 *프레임 건너뛰기* 다.** DL 이 **프레임 한 칸(1,500,000 step = 75 µs)**을 통째로 점프시키고, 그 다음 **nDEM(5,000–10,000) 실제 DEM step** 이 그 pseudo-구조를 물리 위로 **투영**한다 = 전형적 **predictor–corrector / multiple-time-stepping** | §2.7 · Fig 3 |
| ② **teacher forcing 인가 rollout 인가** | ★★ **완전한 free-running ROLLOUT.** *"now the DL is fed using the following 4 microstructures (TF = 2, 3, 4, and **5**)"* — TF 5 는 **모델 자신의 출력**이다.  Fig 3 이 **색으로 못 박는다**: 검은 원 = DEM 참값은 **1,2,3,4 네 개뿐**이고 5 번부터 끝(21)까지 전부 회색(모델 산출).  **teacher forcing 이 아니다.** | §2.7 · **Fig 3 색 부호** |
| ③ 건조 단계에 **압력/응력 축**이 있는가 | ⛔ **없다. 하나도 없다.**  본문·SI 전체에서 `MPa` **0회**, `stress` **0회**, `pressure`(응력 의미) **0회**.  공정 축은 오직 **시간 프레임(TF, 75 µs/칸)** 이다 | 전수 grep |

- **위치**: Franco 그룹(LRCS Amiens / ARTISTIC)의 제조 디지털트윈 사슬에서 **건조(DEM) 단계 위에 얹은 DL 한 층**.
  계보: 슬러리 `vijay2025_hybrid_cgmd_dl_slurry_microstructure`(= 본문 ref [42]) → **건조 = 이 논문** →
  압연 `galvezaranda2024_time_dependent_dl_calendering_microstructure`(= 본문 ref [23]).
  물리 엔진은 전부 **ref [33] Xu 2023 (JPS 554, 232294)** 소유다 — ★ 앞 카드가 ref [36] 으로 부르며
  *"DEM 물성이 필요하면 진입점은 그쪽"* 이라 적은 **바로 그 논문**이고, 여기서 **정확한 서지를 확보했다**(§12-2).
- ★★ **우리에게 값진 것은 결과가 아니라 *분해* 다.** 이 논문의 실측이 말하는 것은 한 문장으로 줄어든다:
  **"프레임 dynamics 의 99.67 % 를 ML 이 건너뛰고, 남은 0.33 % 의 진짜 DEM 이 porosity 오차의 81–96 % 를 제거한다."**
  (`derived(ours)`, §3-D)  ⇒ **ML 은 거친 drift 를 주고, 물리 투영자가 구조를 만든다.**
  이 분해 자체는 우리 STEP1/STEP2 에 **그대로 옮길 수 있는 설계 패턴**이다.
- ⛔ **그러나 이 논문의 *숫자* 는 우리 축으로 못 온다** (§7-3 · §10):
  **액체계 LIB**(NMC111 96/2/2, PVdF+C65, 용매) · **압력 축 0** · **DEM 물성 0 줄** ·
  **실험 신규 0건**(검증 전체가 DEM 대비, 그 DEM 의 실험오차는 ref [33] 에 있고 **재인용조차 안 된다**) ·
  σ 삼중항 0 · 소성 형상변화 0 · **절대 porosity/밀도/τ 값이 논문 전체에 단 하나도 없다**(오직 % 오차).
- ⚠⚠ **그리고 이 카드가 잡은 가장 큰 결함**: **"exceptional generalization" 헤드라인의 근거 그림(Fig 8)이
  학습 조성 그림(Fig 6)의 *행 치환 복사본* 이다 — 32 칸 중 23 칸(72 %)이 소수 첫째 자리까지 동일**하고
  **치환 규칙(I←III, II←I, III←II)이 두 패널에 똑같이** 걸려 있다 (§3-C).
  ⇒ **외삽 성능은 이 논문의 출판된 수치로 검증 불가능하다.**

---

## 1. 한 줄 요약

건조 DEM 시뮬레이션 **11 TS(학습) + 8 TS(시험) × 21 TF** 의 입자별 **국소환경(LE) 6-특징 × 4 lag** 을 먹고
**다음 프레임의 (x,y,z) 3 개**를 뱉는 **VGG16 → Conv1D 변형**(23.80 M 파라미터)을 세운 뒤,
그 예측(TF = n\*)에 **nDEM 개의 진짜 DEM step** 을 걸어 겹침을 풀고 TF = n 으로 확정한다.
이것을 TF 5 → 21 까지 **자기출력을 다시 먹이며(rollout)** 반복한다.
검증 = (i) RDF 의 R² (ii) GeoDict 로 낸 density·porosity·τ 의 % 오차.
**pure DEM 34.2 min/TF vs PAML 2.4 min/TF (nDEM = 7000) = 14.3×/step**,
초록은 **615 → 36 min (17.1×)**, 본문은 **684 → 48 min (14.25×)** 로 **서로 안 맞는다**(§10-⑨).

---

## 2. 메타

| 저자 / 소속 | 지면 | DOI | 소재계 | 방법 |
|---|---|---|---|---|
| **Diego E. Galvez-Aranda**, **Francisco Fernandez**, **Alejandro A. Franco**\* — LRCS (UMR CNRS 7314, UPJV Amiens) / RS2E / ALISTORE-ERI / IUF | ***ACS Applied Materials & Interfaces* 17 (2025) 32150−32162**, 13 pp.  접수 2025-01-03, 수정 04-15, 수락 04-24, 출판 **2025-05-06**.  특집 *"Machine Learning for Materials Chemistry"* | `10.1021/acsami.4c23103` | 학습 = **NMC111 96 wt% + C65 2 wt% + PVdF 2 wt%** (시뮬 상 **AM 96 % + CBD 4 %**) · 외삽시험 = **94 % NMC − 3 % C65 − 3 % PVdF** (**AM 94 % + CBD 6 %**).  **액체계 LIB 양극** | **VGG16 → Conv1D 개조 CNN**(Table 1, 23.80 M 파라미터) + **DEM**(ref [33]; 저자들이 *"formerly called CGMD"* 라 적음).  전달물성 = **GeoDict 2024 DiffuDict**(Math2Market).  가시화 = **OVITO** |
| 구성 | Fig 1–8 · Table 1 · refs 42 · SI = **Fig S1–S4 뿐**(수치표 0) + **보충영상 2편(ZIP)** | | | 하드웨어: **MatriCS 플랫폼(UPJV) 1 노드 · 128 GB RAM · Intel Xeon E5-2680 v4 @ 2.40 GHz × 2 (14 core)** — ⚠ **CPU 만 명시, GPU·학습시간 미보고** |
| 자금 | ANR-22-PEBA-0002 (France 2030 PEPR **BATMAN**) · Horizon Europe **DigiCell** 101135486 · **PULSELiON** 101069686 · IUF | | | 감사문: *"We acknowledge **Jiahui Xu** … regarding the **DEM code used in her PhD thesis work**[33] to generate all the training data"* ⇒ **DEM 은 전적으로 ref [33] 자산** |

**계보** (전부 정본 카드 있음):
`vijay2025_hybrid_cgmd_dl_slurry_microstructure` (ref [42], 슬러리 단계) ·
**`galvezaranda2024_time_dependent_dl_calendering_microstructure`** (ref [23], 압연 단계 — 자매편) ·
`wet_processing_resolved_am_ssb_cathode_manufacturing` (**ref [36] Weitze 2024 ESM 73, 103747 — ★ ASSB 습식 양극**) ·
`ngandjong2021_dem_calendering_digital_twin` (ref [35]) ·
`duquesnoy2020_calendering_ml_mesostructure_generator` (ref [19]) ·
`alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (계보 인접) ·
`lyu2025_3d_dem_drying_calendering_lib` (독립 건조+압연 DEM).

---

## 3. 핵심 수치

### 3-A. 모델 · 데이터 · 비용 (stated / `derived(ours)` 명시)

| 항목 | 값 | 출처 |
|---|---|---|
| 학습 시계열 | **11 TS** (각각 서로 다른 슬러리 초기구조에서 출발한 건조 런) | stated §2.3 |
| 시험 시계열 | **8 TS** = 96/4 **4개**(Test I–IV) + 94/6 **4개**(Test I–IV) | stated §2.3 |
| TS 당 프레임 | **21 TF** (건조율 고정 ⇒ 모든 런이 21) | stated §2.1 |
| TF 당 DEM step | **1,500,000** (= **75 µs**) | stated |
| 전체 건조 = | **30,000,000 step** · Δt = **0.00005 µs** ⇒ **총 1.5 ms 모사시간** | stated + 🧮 |
| 슬라이딩 윈도 | **5 프레임 = 4 입력 → 1 타깃** ⇒ TS 당 **17 관측/입자** | stated §2.2 |
| 입자 수 | *"nearly **10,000** particle dynamics per TS of the same type (AM or CBD)"* ⇒ 대략 **2만/프레임** | stated §2.2 |
| 🧮 학습 행 수 | ≈ 2만 × 17 × 11 ≈ **3.7 M 샘플** — ⚠ 그러나 **독립 물리 궤적은 11 개뿐** | `derived(ours)` |
| LE 특징 | **`[x, y, z, r, C_AM, C_CBD]` 6개** (cutoff ≈ **3 µm**, ref [33]) | stated §2.2 |
| DL 출력 | **(x, y, z) 3개** (`Dense_3 → (none,3)`) — ★ **r 은 입력이지 출력이 아니다** | Table 1 |
| 파라미터 | 표 합계 **23,800,439 ≈ 23.80 M** (⚠ 한 칸 오타 보정 시 **23.80 M**, §10-⑦) | 🧮 Table 1 합산 |
| 학습 | **500 epoch**, loss = MSE.  수렴값 **MSE ≈ 0.022(train)/0.025(val)** · **MAE ≈ 0.105/0.11** | Fig 4 (축에서 읽음, 근사) |
| ⚠ 단위 | **MSE/MAE 의 단위·정규화 여부가 논문 어디에도 없다** — §10-② 가 이것을 다룬다 | — |
| 복셀 격자 | **76 × 76 × 124 = 716,224 복셀**, 0.4 µm/변 ⇒ 상자 **30.4 × 30.4 × 49.6 µm** | stated §2.6 + 🧮 |
| 복셀 라벨 | **0 = pore · 1 = CBD · 2 = AM** — ★ **세 개뿐**(자매편은 `4 = void` 를 더 썼다, §10-③) | stated §2.6 |
| CBD 미세공극 | **ξ = 0.5 가정**, Bruggeman `D_CBD = ξ^1.5` | stated §2.6 |
| τ 규약 | **`τ = ε / D_eff`** (MacMullin), D_pore ≡ 1, z 방향 Dirichlet 0↔1 mM Li⁺, x·y 주기 | stated §2.6 |
| RDF | `r_max = 4 µm`, `Δr = 0.01 µm` ⇒ **400 bin** | stated §2.5 + 🧮 |
| 하드웨어 | 1 노드 · 128 GB · **Xeon E5-2680 v4 × 2 (28 core)** — **GPU 언급 없음** | stated §3 |

### 3-B. ★ 기능 지표 오차 — **전수 (Fig 6 · Fig 8 은 그림 안에 숫자가 인쇄돼 있다 = stated, 디지타이즈 아님)**

**Fig 6 — 96 % AM / 4 % CBD (= 학습 조성)**

| | | porosity 오차 (%) | | | | | 인성(τ) 오차 (%) | | |
|---|---|---|---|---|---|---|---|---|---|
| µ구조 | nDEM=0 | 5000 | 7000 | 10000 | | nDEM=0 | 5000 | 7000 | 10000 |
| **I** | **59.7** | 3.9 | 3.6 | 4.3 | | **26.6** | 13.9 | 11.4 | **9.3** |
| **II** | **56.6** | 3.4 | 3.8 | 4.4 | | **27.7** | 7.7 | 7.5 | **3.4** |
| **III** | **41.7** | 7.8 | 6.7 | 7.7 | | **22.7** | **1.0** | 4.1 | 1.9 |
| **IV** | **60.5** | **2.4** | 3.3 | 2.6 | | **23.2** | 14.3 | 13.0 | 11.3 |
| 🧮 평균(nDEM≥5000) | — | **4.49 %** | | | | — | **8.23 %** | | |

**Fig 8 — 94 % AM / 6 % CBD (= 외삽 시험)**  ⚠⚠ **아래 값의 72 % 는 위 표의 복사본이다 (§3-C)**

| µ구조 | nDEM=0 | 5000 | 7000 | 10000 | | nDEM=0 | 5000 | 7000 | 10000 |
|---|---|---|---|---|---|---|---|---|---|
| **I** | 41.7 | 7.8 | 6.7 | 7.7 | | 22.7 | 1.0 | 4.1 | 1.9 |
| **II** | 59.7 | 3.9 | 3.6 | 4.3 | | 26.6 | 13.9 | 11.4 | 9.3 |
| **III** | **57.7** | 3.4 | 3.8 | 4.4 | | **33.9** | 7.7 | 7.5 | 3.4 |
| **IV** | **41.7** | **6.1** | **6.4** | **6.1** | | **22.5** | **8.8** | **3.6** | **2.0** |
| 🧮 평균(nDEM≥5000) | — | **5.35 %** | | | | — | **6.22 %** | | |

- **density 오차**: 96/4 = *"strictly less than 3 %"*, 94/6 = *"approximately 5 %"*, **둘 다 nDEM 에 무관**. (stated, 표 없음)
- **RDF R²** (Fig 5b/7b, 그림에서 읽음 — TREND):
  · 96/4: nDEM 7000·10000 → **> 0.9 안정**; nDEM 5000 → TF 19 에서 **≈ 0.69 까지 내려갔다 0.93 회복**;
    **nDEM 0 → 0.83(TF5) → 단조 붕괴 → TF 16–19 에서 ≈ 0.0**.
  · 94/6: nDEM 7000·10000 → **≈ 0.8 안정**(저자 표현 *"around 0.8"*); nDEM 5000 → **≈ 0.52 최저**; nDEM 0 → **≈ 0.0**.
  · ★ **TF 1–4 의 R² 는 정확히 1.000** — 그 네 칸은 **DEM 참값 시드**라 정보가 0이다 (§10-①).

### 3-C. ★★★ **Fig 8 = Fig 6 의 행 치환 복사본** (이 카드가 잡은 최대 결함)

`derived(ours)` 전수 대조 (셀 단위 완전일치 개수):

| | Fig 8 행 | 내용 | **Fig 6 의 어느 행과 같은가** | 일치 |
|---|---|---|---|---|
| **porosity (a)** | I | 41.7 · 7.8 · 6.7 · 7.7 | = Fig 6a **행 III** | **4/4** |
| | II | 59.7 · 3.9 · 3.6 · 4.3 | = Fig 6a **행 I** | **4/4** |
| | III | 57.7 · 3.4 · 3.8 · 4.4 | = Fig 6a **행 II** (첫 칸만 56.6→57.7) | **3/4** |
| | IV | 41.7 · 6.1 · 6.4 · 6.1 | 첫 칸 41.7 만 Fig 6a 행 III 과 같음 | 1/4 |
| **τ (b)** | I | 22.7 · 1.0 · 4.1 · 1.9 | = Fig 6b **행 III** | **4/4** |
| | II | 26.6 · 13.9 · 11.4 · 9.3 | = Fig 6b **행 I** | **4/4** |
| | III | 33.9 · 7.7 · 7.5 · 3.4 | = Fig 6b **행 II** (첫 칸만 27.7→33.9) | **3/4** |
| | IV | 22.5 · 8.8 · 3.6 · 2.0 | 없음 (신규) | 0/4 |
| | | | **합계** | **23 / 32 = 72 %** |

★ **결정적인 것은 개수가 아니라 *치환 규칙이 같다* 는 것이다**: 두 패널 모두
**Fig8-I ← Fig6-III · Fig8-II ← Fig6-I · Fig8-III ← Fig6-II**.
서로 다른 두 물리량(porosity, τ)이 **독립적으로 같은 순열로 우연히 일치할 확률은 무시할 수 있다.**
⇒ **유일하게 합리적인 설명 = 그림 제작 단계의 복사-붙여넣기 오류.**
⚠ **어느 그림이 오염됐는지는 특정할 수 있다**: **본문 §3 의 96/4 서술은 Fig 6 과 네 줄 모두 정확히 일치**하고
(*"60 % → ≈4 %"* = 59.7→3.9 · *"57 → ≈4"* = 56.6→3.4 · *"42 % and 23 % → 8 % and 2 %"* = 41.7→7.8, 22.7→1.9 ·
*"23 % → 11 %"* = 23.2→11.3), **94/6 서술은 단 하나의 수치도 인용하지 않는다**(density 5 % 만).
⇒ **Fig 8 쪽이 오염됐을 가능성이 높고, 본문은 그것을 한 번도 읽지 않았다.**

⇒ ★★ **판정**: 초록의 *"demonstrated **exceptional generalization capability**"* 는
**porosity·τ 축에서는 출판된 수치로 검증 불가능하다.**  외삽 축에서 **살아남는 유일한 증거는 R² 축**이고,
그것은 **"exceptional" 이 아니라 열화**를 보인다 — **0.9+ → ≈0.8** (저자 자신도
*"it is difficult for the PAML model to predict accurately the first peak of the RDF"* 라고 적는다).

### 3-D. ★★ 비용 · 가속 · 손익분기 (`derived(ours)` — 논문은 배수도 손익분기도 계산하지 않는다)

**논문이 준 것 (stated)**: pure DEM **34.2 min/TF**, 총 **684 min**.
PAML **0.6 / 2.1 / 2.4 / 2.85 min/TF** (nDEM = 0 / 5000 / 7000 / 10000), 총 **12 / 42 / 48 / 57 min**.

| 회계 방식 | nDEM=0 | 5000 | **7000** | 10000 |
|---|---|---|---|---|
| **논문식 배수** (684 ÷ 총시간) | 57.0× | 16.3× | **14.25×** | 12.0× |
| 🧮 **step 단위** (34.2 ÷ min/TF) | 57.0× | 16.3× | **14.3×** | 12.0× |
| 🧮 ★★ **정직한 end-to-end** (시드 4 프레임의 DEM 비용 **102.6 min** 포함) | 6.06× | 4.95× | **4.77×** | 4.53× |
| 🧮 **원리적 천장** (surrogate 비용 → 0) | | | **6.67×** | |

★★ **가장 중요한 한 줄**: 이 아키텍처는 **입력 lag 4 개**가 필요하므로 **TF1→TF4 를 pure DEM 으로 먼저 돌려야** 한다
= **3 × 34.2 = 102.6 min = 전체 684 min 의 15.0 %**.  ⇒ **Amdahl 천장 = 6.67×.**
surrogate 를 아무리 공짜로 만들어도 **end-to-end 가속은 6.67 배를 못 넘는다.**
논문의 14.25× 는 **이 시드 비용을 분모에 넣지 않아서** 나온 값이다.

🧮 **DEM step 보존율**: nDEM = 7000 × 17 예측프레임 = **119,000 step** / 참 궤적 **25,500,000 step** = **0.467 %**.
(5000 → 0.333 % · 10000 → **0.667 %**)  ⇒ **궤적의 99.3–99.7 % 를 ML 이 건너뛴다.**

🧮 **그런데 그 0.33–0.67 % 가 porosity 오차의 81–96 % 를 제거한다** (Fig 6a, nDEM 0→5000):
Test I **59.7→3.9 (−93.5 %)** · II **56.6→3.4 (−94.0 %)** · III **41.7→7.8 (−81.3 %)** · IV **60.5→2.4 (−96.0 %)**.
⇒ ★ **구조를 만드는 것은 ML 이 아니라 물리 투영자다.**  ML 은 거친 drift 만 공급한다.

🧮 **hybrid 안의 DEM step 은 pure DEM 보다 6.6배 비싸다** — (5000, 2.1) · (7000, 2.4) · (10000, 2.85) 선형적합 =
**9.00 ms/step + 절편 1.350 min/TF**.  pure DEM 은 **1.368 ms/step**.
절편 1.350 − DL-only 0.6 = **0.75 min/TF 가 DEM 호출 고정비**(재시작 I/O·이웃목록 재구축 추정).
⇒ **가속은 물리가 아니라 *구현* 이 막고 있다** — 호출 오버헤드를 없애면 같은 nDEM 에서 훨씬 빨라진다.
(⚠ 우리도 LIGGGHTS restart I/O 에서 정확히 같은 벽을 만난다.)

🧮 **학습 데이터 생성비**: 11 TS × 684 min = **7,524 min = 125.4 h = 5.2 일**(직렬).
시험셋 참값까지 = 19 TS × 684 = **12,996 min = 216.6 h = 9.0 일**.
🧮 **손익분기** (nDEM = 7000, 정직회계 절감 = 684 − 143.4 = **540.6 min/런**):
- 학습셋만 상각 → **13.9 런** (= 학습셋 **11 런의 1.27배**)
- 학습 + 시험 참값 상각 → **24.0 런**
- (논문식 회계로는 각각 **11.8 / 20.4 런**)
⇒ ★ **자매편(압연)의 손익분기 583 step = 3.4 전극-스윕 = 학습셋 자신의 크기와 *같은 구조* 의 결론**이다:
**"자기가 먹은 만큼 조금 더 만들어야 본전, 그 다음부터 이익."**
🧮 **분모에 아직 없는 것 4가지**: (i) **CNN 학습 시간 — 미보고**(500 epoch × 3.7 M 샘플 × 23.8 M 파라미터)
(ii) **nDEM 하이퍼 스윕 = 4 × 4 × 2 = 32 hybrid 런 ≈ 21 h** (iii) **GeoDict DiffuDict 솔브** — DL 경로에도
똑같이 필요하고 **비용 미보고** (iv) **상류 슬러리 시뮬레이션** — 대체되지 않는다.

---

## 4. 시뮬레이션 방법 ★

### 4-1. DEM (건조) — ⛔ **이 논문에는 파라미터가 한 줄도 없다**

전수 grep 결과 (본문 + SI):

| 우리가 항상 적는 것 | 이 논문 | 비고 |
|---|---|---|
| 코드 (LIGGGHTS / LAMMPS / Rocky) | **미기재** — *"a DEM method (formerly called CGMD in some of our previous works)"* | ref [33] 로 미룸 |
| 접촉법칙 (Hertz / Thornton-Ning / EEPA / hooke-hysteresis) | **미기재** | ref [33] |
| E · ν · µ · COR (상별) | **미기재** (`Young` `modulus` `Poisson` `friction` `restitution` = **0회**) | ref [33] |
| 응집/바인더 모델 | **미기재** (`cohesi` 는 결론의 *"future work"* 한 번뿐) | ref [33] |
| PSD · 입자 형상 | *"particle sizes and shapes of AM obtained by **computer tomography**"* — **값 없음** | ref [33] |
| **건조를 무엇으로 표현하나** (용매 명시? bead 수축? 응집력 램프?) | ⛔ **한 줄도 없다** | ★ §10-⑤ |
| servo / PID / 벽 BC | **미기재**.  주기경계는 LE 계산에 쓴다고만 적음 | — |
| **압력 / 응력** | ⛔ **0회** | ★ §0 질문 ③ |
| seed / 앙상블 / 오차막대 | **0** | — |

⇒ ★ **이 논문은 DEM 을 *블랙박스 적분기* 로만 쓴다.**  우리가 DEM 물성을 원하면 진입점은 **ref [33] Xu 2023** 뿐이다.
★ **2026-09-11 — 그 진입점이 정본에 들어왔다**: `papers/xu2023_realistic_am_shape_cgmd_calendering.md`
(위 "미기재" 5 행 중 **접촉법칙 · E/ν/µ · 응집모델 · PSD/형상 4 행이 채워지고**, **COR 는 거기에도 없으며**
**timestep · 플래튼 속도 · 압력축은 거기에도 없다**).

### 4-2. ★ 입자 처리 (= DEM 판 "무질서 처리")

| 축 | 이 논문 | 우리 |
|---|---|---|
| 형상 | **realistic-shape AM 2차입자 = 여러 구형 1차입자의 다중구(multisphere) 집합** (Fig 2, CT 유래) | **단일 구** (LIGGGHTS) |
| 상 | **AM 1차입자 · CBD 두 종류만** (용매는 명시 안 됨) | **AM_P · AM_S · SE + 첨가제** |
| PSD | 다분산(값 미보고) | 실 PSD 12:4:1 |
| **소성** | ⛔ **없다 — 접촉 소성도, 형상 소성도 없다.**  논문은 접촉법칙 자체를 안 적지만 *"particle overlaps … not physically possible"* 라고 겹침을 **오류로 취급**한다 ⇒ 강체구 규약 | DEM = hooke/hysteresis **접촉** 소성(δ 프록시) · MPM = **형상** 소성 |
| **DL 이 볼 수 있는 자유도** | **(x, y, z) 뿐.**  `r` 은 **입력이지 출력이 아니다**(`Dense_3 → 3`) | — |
| ⇒ **bead 수축 표현 가능?** | ⛔ **원리적으로 불가.**  `vijay2025` 의 건조 규약(**CBSA Ø7 → CBD 1.3 µm 수축**)이 ref [33] 에도 있다면 **surrogate 는 그 축을 얼려 버린다** — 그리고 **DEM 투영자도 그것을 못 고친다**(위치만 완화) | MPM 은 형상 자체가 변함 |

★★ **결정적 구조 사실**: 이 CNN 은 **입자 하나당 독립으로 호출**된다.
입력 = **그 입자 자신의** 4 프레임 [x,y,z,r,C_AM,C_CBD], 출력 = **그 입자 자신의** 다음 (x,y,z).
**이웃 입자의 좌표는 네트워크 안에 들어가지 않는다** — 이웃 정보는 **스칼라 2개(C_AM, C_CBD)** 뿐이고,
message passing 도 neighbor pooling 도 없다.  저자도 인정한다:
*"our DL model … has been trained to predict particle positions **without accounting for particle interactions**"*.
⇒ **겹침이 나오는 것은 버그가 아니라 아키텍처의 필연**이고, 그래서 DEM 투영자가 **필수 부품**이다.
⇒ ★ 그리고 이것이 §10-⑧ 의 **trivial baseline 요구**로 직결된다: 이웃을 못 보는 per-particle 외삽기라면,
**등속 외삽 `x₅ = 2x₄ − x₃`** 나 **한 파라미터 affine 붕괴**가 같은 정보로 같은 일을 할 수 있다.

### 4-3. ★ DL 모델 — Table 1 산술로 복원

입력 = **(4 timestep × 6 feature)**.  `conv1d` 1층 파라미터 **1216 = 64 × (3×6 + 1)** ⇒ **kernel 3, in_ch 6, 'same' 패딩** 확정.

| # | 층 | 출력 | 파라미터 | 🧮 검산 |
|---|---|---|---|---|
| 1 | Conv1D | 4 × 64 | 1,216 | 64·(3·6+1) ✅ |
| 2 | Conv1D | 4 × 64 | 12,352 | 64·(3·64+1) ✅ |
| 3 | **MaxPool** | 2 × 64 | — | 실제 축소 |
| 4 | Conv1D | 2 × 128 | 24,704 | 128·(3·64+1) ✅ |
| 5 | Conv1D | 2 × 128 | 49,280 | 128·(3·128+1) ✅ |
| 6 | **MaxPool** | **1 × 128** | — | **시간축 여기서 소멸** |
| 7 | Conv1D | 1 × 256 | **95,860** | ⚠ **98,560 이어야 한다** (256·385) — **숫자 전치 오타**(§10-⑦) |
| 8–9 | Conv1D ×2 | 1 × 256 | 196,864 ×2 | 256·(3·256+1) ✅ |
| 10 | MaxPool | 1 × 256 | — | ⚠ **항등 연산** |
| 11 | Conv1D | 1 × 512 | 393,728 | 512·769 ✅ |
| 12–13 | Conv1D ×2 | 1 × 512 | 786,944 ×2 | ✅ |
| 14 | MaxPool | 1 × 512 | — | ⚠ **항등** |
| 15–17 | Conv1D ×3 | 1 × 512 | 786,944 ×3 | ✅ |
| 18 | MaxPool | — | — | ⚠ **항등** |
| 19 | Flatten | 512 | — | |
| 20 | Dense_1 | 4096 | 2,101,248 | 512·4096+4096 ✅ |
| 21 | Dense_2 | 4096 | 16,781,312 | 4096·4096+4096 ✅ |
| 22 | **Dense_3** | **3** | 12,291 | 4096·3+3 ✅ |
| | **합계** | | **23,800,439 (23.80 M)** | 🧮 |

★★ **세 가지가 이 표에서 바로 나온다** (`derived(ours)`):
1. **6번 풀링 뒤 시간축 길이가 1 이 된다** ⇒ **7–17 번의 conv1d 9 개는 길이-1 수열 위의 conv = 사실상 dense 층**이다.
   kernel 3 의 세 tap 중 **가운데 하나만 살아 있고 양옆 두 tap 은 영-패딩을 곱한다** ⇒
   그 9 개 층의 **4.82 M 파라미터(전체의 20.3 %) 중 약 2/3 가 출력에 도달할 수 없다.**
2. **5 개 max-pool 중 3 개(10·14·18)가 항등**이다 — ★ **자매편 카드가 잡은 것과 똑같은 병리**
   (그쪽도 *"max-pool 3 개가 전부 항등(pool=stride=1)"*).  **같은 그룹의 같은 습관이 두 논문에 반복된다.**
3. ⇒ 저자의 정당화 *"we take advantage of **VGG16 spatial hierarchy**"* 는 **작동하지 않는다**:
   길이-4 수열은 **두 번 반감하면 끝**이라 hierarchy 가 존재할 수 없다.
   실제 모델 = **길이-4 위의 conv 4 층 + 약 22 M 짜리 MLP**.  "VGG16" 은 **상표이지 구조가 아니다.**

### 4-4. ★★ 하이브리드 루프 (= 이 논문의 진짜 기여) — §2.7 · Fig 3

```
[TF1 TF2 TF3 TF4]  ← 전부 pure DEM 참값 (Fig 3 의 ■ 검은 원)
        │ DL (per-particle, 프레임 한 칸 = 1,500,000 step = 75 µs 를 건너뜀)
        ▼
     TF5*  (pseudo — 겹침 있음, 비물리)
        │ DEM ×nDEM  (5,000–10,000 step = 0.25–0.5 µs = 그 칸의 0.33–0.67 %)
        ▼
     TF5   (확정, □ 회색 = 모델 산출)
[TF2 TF3 TF4 **TF5**] → DL → TF6* → DEM ×nDEM → TF6 → …  ★ 자기출력을 다시 먹는다 = ROLLOUT
                                                       … → TF21 (건조 완료)
```

- **predictor** = DL.  **corrector/projector** = nDEM DEM step.  `nDEM` 이 **새 하이퍼파라미터**다.
- ★★ **rollout 확정 근거 3 겹**: ① 본문 *"the DL is fed using the following 4 microstructures (TF = 2, 3, 4, and **5**)"*
  ② **Fig 3 의 색 부호** — 검은 원(참값)은 **1,2,3,4 뿐**, 5\*/5/6\*/6/…/19/20\*/20/21\*/21 이 전부 회색
  ③ **Fig 5b/7b 의 nDEM=0 R² 가 단조 붕괴**한다 = **자기회귀 오차 누적의 교과서적 서명**
  (teacher forcing 이면 프레임마다 참값으로 리셋되어 이 모양이 안 나온다).
- ⇒ ★ **자매편 §10-⑤ 의 미해결에 대한 함의**: **이 논문은 rollout 이고 그 R² 는 단조 붕괴한다.**
  자매편(압연)의 Fig 5c 는 92.2 → **프레임 9 에 정확히 100 복귀** 한다 — **이 논문의 rollout 서명과 정반대 모양**이다.
  ⚠ **그렇다고 자매편이 teacher-forced 라고 *단정할 수는 없다*** (다른 논문·다른 조건화).
  그러나 **같은 1저자·같은 그룹의 rollout 구현이 이렇게 생겼다는 것**은 자매편 §10-⑤ 읽기 (a)를 **강화**한다.
  ⇒ 자매편 카드 §10-⑤ 를 *"미해결"* 에서 *"미해결 — 단 자매 rollout 의 서명이 확보됐고 그것과 어긋난다"* 로 갱신한다.

### 4-5. 후처리 / 평가 지표

- **데이터 지표**: MSE(학습 loss) · MAE · **RDF 의 R²**.
  `R² = 1 − Σ_r (g_t − g_p)² / Σ_r (g_t − ḡ)²`, `ḡ = (Δr/r_max)·Σ_r g_t` (eq 7–8) ⇒ **400 bin 산술평균**.
- **기능 지표** (GeoDict 2024):
  · **ε** = (N_pore + ξ·N_CBD) / **N_total**, ξ = 0.5 (⚠ 분모 정의 문제 = §10-③)
  · **D_eff** = DiffuDict 정상상태 Fick 솔브 (z 방향 0↔1 mM Li⁺ Dirichlet, x·y 주기)
  · **τ = ε / D_eff** (MacMullin)
  · **density** — 계산식 미기재.
- ⚠ **GeoDict 솔브는 DL 이 하는 일이 아니다** — 자매편 카드가 잡은 것과 같은 구조:
  **DL 출력은 좌표 목록 하나**뿐이고, τ·D_eff 를 얻으려면 **예측 격자 위에서 FV 솔브를 새로 돌려야** 한다.
  그 비용은 **DEM 경로와 동일**하고 **논문 어디에도 없다.**

---

## 5. 결과 — 절별 전수

### 5-1. §3 첫 문단 — 학습 (Fig 4)
500 epoch, MSE·MAE 수렴, train ≈ val.  저자: *"the close alignment … emphasizes that the DL model
generalized well to unseen data, avoiding overfitting."*
⚠ **검증 분할 방법이 한 줄도 없다.**  샘플이 **같은 상자 안의 2만 입자 × 겹치는 시간창**이라,
행 단위 무작위 분할이면 **검증 행은 학습 행의 물리적 이웃**이다 ⇒ **train≈val 은 과적합 부재의 증거가 못 된다.**
독립 단위는 **11 개 궤적**이지 3.7 M 행이 아니다.

### 5-2. §3 RDF / R² (Fig 5, 7, S1–S4)
- nDEM 0 (= 순수 DL) 의 RDF 는 **r → 0 까지 g ≈ 1.5–3 으로 채워진다** = **배제영역이 아예 없다**
  (Fig 5a 초록).  ⇒ 순수 DL 산출물은 **구조 없는 기체**에 가깝다.
- nDEM ↑ ⇒ RDF 가 DEM 쪽으로 수렴.  저자: *"the position, height, and width of the first peaks are well reproduced."*
- ★ DEM 참값 RDF: **r ≲ 0.88 µm 에서 정확히 0**, 첫 어깨 ≈ 1.25 µm, **주 peak ≈ 1.45 µm (g ≈ 6.5)**,
  이후 1.75 / 2.5 / 2.85 에 작은 peak, 장거리에서 1 로 수렴. (그림에서 읽음 — 근사)
- 96/4: nDEM 7000·10000 **R² > 0.9**; 94/6: **≈ 0.8**.

### 5-3. §3 기능 지표 (Fig 6, 8)
§3-B 표 그대로.  저자 요약: *"higher errors for 0 DEM steps compared to … different nDEM steps"*.
⚠ **94/6 문단의 *"In all cases, we have a good decrease in the percentage error when the nDEM
hyperparameter increases"* 는 자기 그림(Fig 8a)과 어긋난다** — porosity 4 행 중 **단조감소 0 행**,
행 III 은 3.4 → 3.8 → **4.4 로 증가**한다 (§10-⑥).

### 5-4. §4 결론 / 전망
- **digital twin** 을 명시적 목표로 건다: *"dynamic systems that underpin the concept of digital twins"*.
- 저자 자인 한계: *"the current DL framework … **does not inherently capture broader system properties such
  as thermal characteristics**"*, *"a DL model trained **exclusively on particle locations** can provide
  satisfactory results, thereby establishing a **solid proof of concept**"* ⇒ **저자 스스로 PoC 라고 부른다.**
- 전이 한계 자인: *"predictive accuracy may be compromised when faced with materials whose **force field
  parameter values significantly diverge** from the original training set."*
- CFD / CFD-DEM 대비 우위 주장 (미세구조·CBD 분포 해상).
- ★ 미래 응용 제안: **inline mass-loading profilometry + surrogate → 오븐에서 나오는 전극의 τ·전도도 실시간 추정**.

---

## 6. Figure set ★ (전수 + 우리가 쓸 것)

| Fig | 무엇을 보여주나 | **우리가 쓸 수 있는 것** |
|---|---|---|
| **1a** | 제조 3단계 다이어그램(슬러리→코팅/건조→압연) + ARTISTIC granular 파라미터 | 사슬 위치 그림 (발표용 맥락) |
| **1b** | ★ DL 개념도: 건조 시계열 미세구조 예측.  **CBD 빨강, realistic-shape AM 은 2차입자마다 다른 색** | ⚠ 우리 그림 규약과 다름(우리는 상별 색) |
| **2** | ★★ **국소환경(LE) 세 종류**: (a) 2차입자 **안**의 1차 AM (b) CBD 로만 둘러싸인 CBD (c) **가장자리**의 CBD(1차 AM + CBD 혼재) | ★ **우리 coordination/coverage 정의와 개념적으로 같은 자리**.  ⚠ 우리는 Z 를 **상 쌍별**로 쪼개지만 여기는 **C_AM · C_CBD 두 스칼라**로만 |
| **3** | ★★★ **하이브리드 워크플로 전체**.  검은 원 = DEM 참값(1–4), 회색 원 = 모델 산출(5–21).  `DL → n*` → `DEM ×nDEM → n` | ★★★ **rollout 확정의 결정적 증거** (§4-4).  **우리 STEP1 시간-surrogate 설계도의 원형** |
| **4a,b** | 학습 MSE / MAE vs epoch (500).  수렴 ≈ 0.022 / 0.105 | ⚠ **단위 미기재** — §10-② 의 대상.  축 스팬(0–0.20 / 0–0.40)이 넓어 "완벽 수렴"처럼 보인다 |
| **5a** | ★ 96/4 Test I 최종 RDF: DEM(검정) vs nDEM 0/5000/7000/10000 | ★★ **배제영역(0–0.88 µm)이 눈으로 보인다** = §10-① 의 원천.  순수 DL(초록)이 그 영역을 g≈2 로 채운다 |
| **5b** | ★★ **R² vs TF (96/4 Test I)**.  TF 1–4 = **정확히 1.000** | ★★ **두 가지**: ① 시드 4 칸이 자유점수라는 증거 ② **nDEM=0 의 단조 붕괴 = rollout 서명** |
| **6a,b** | ★★ **heat map: porosity / τ % 오차 × (µ구조 I–IV) × nDEM** — **숫자가 인쇄돼 있다** | ★★ **stated 수치 확보**(§3-B).  ★ 그리고 **nDEM 단조성 검사의 원천**(§10-⑥) |
| **7a** | 94/6 Test I 최종 RDF | ★ 외삽에서 **첫 peak 를 못 맞춘다**는 저자 자인의 근거 |
| **7b** | ★ R² vs TF (94/6) — 7000/10000 이 **≈0.8**, 5000 은 **≈0.52 까지** | ★★ **외삽 축에서 살아남는 유일한 증거**(§3-C) |
| **8a,b** | ⚠⚠ **heat map (94/6)** — **32 칸 중 23 칸이 Fig 6 의 행 치환 복사본** | ⚠⚠ **인용 금지 대상**.  §3-C 참조 |
| **Table 1** | ★ VGG16 개조 구조 (22 층, 파라미터 수) | ★★ **§4-3 의 구조 병리 복원**(길이-1 conv · 항등 풀링 · 오타 1건) |
| **S1 / S3** | 96/4 · 94/6 의 Test II·III·IV RDF | — (본문 Fig 5a/7a 와 같은 종류) |
| **S2 / S4** | 96/4 · 94/6 의 Test II·III·IV R² vs TF | ★ R² 재현성 확인용.  ⚠ **SI 에 수치표는 하나도 없다** |

### 6-B. 보충 영상 2편 (읽을 수 없음 — 존재와 파일명만 기록)
- `Formulation AM 94 CBD 6 - Test I.mp4` (2,582,258 B)
- `Formulation AM 96 CBD 4 - Test I.mp4` (2,571,608 B)
ASSOCIATED CONTENT: *"Videos illustrating in comparative manner the DEM and the DEM + DL simulations
for the formulations AM 94 % CBD 6 — Test I, and AM 96 % CBD 4 — Test I (ZIP)"*
⇒ **DEM vs DEM+DL 나란히 비교 영상**.  ⚠ 이 컨테이너에서 디코딩 불가 ⇒ **내용 인용 금지.**

---

## 7. 우리 DEM+MPM 대비 ★ → `our_dem_baseline.md` · `comparison_vs_ours_DEM.md`

### 7-1. frame[5] 상 어디에 서는가

- **이 논문이 소유한 절반** = **DEM 쪽 = 수송/패킹 축의 *구조 생성기***.
  그런데 그 DEM 은 **강체구 다중구 + 접촉 소성 없음**이라, frame[2] 의 우리 DEM 과 **같은 칸**이다.
- **이 논문이 갖지 못한 절반** = **소성(MPM) 전부**.  형상 변화 0 · 공극 충전 흐름 0 · 소성변형장 0 ·
  응력장 0.  게다가 **DL 출력이 (x,y,z) 3개뿐**이라 **형상/반경 자유도를 원리적으로 표현할 수 없다**(§4-2).
  ⇒ **frame[5] 의 우리 분업을 또 한 번 독립 확인한다** ([Varkey26] 이 그랬듯이):
  *"2025 년 최첨단 하이브리드 DEM+DL 이, 접촉법칙을 건드리기는커녕 **입자 위치만** 다룬다."*
- **수송 축**: τ·D_eff 를 **복셀 FV(GeoDict DiffuDict)** 로 낸다 = **우리 STEP3 와 같은 종류**.
  ⚠ 그러나 **공극상 Fick 확산(액체 전해질 Li⁺)** 이고 우리는 **SE 고체상 이온전도**다 — 위상만 같다.
  ⚠⚠ 그리고 **우리 STEP3 도 `CONTACT_FREE` 가지 위에 있다**(CLAUDE.md CL-81) — 두 복셀 FV 의
  일치를 **교차검증으로 인용하지 말 것.**

### 7-2. ★★ 우리 STEP1 에 시간-surrogate 를 붙일 수 있는가 — **판단 재료 정리**

**문헌이 주는 긍정 재료 (4가지)**

1. ★★ **predictor–corrector 분해가 실제로 작동한다.**  0.33 % 의 물리로 porosity 오차의 **81–96 %** 가 사라진다.
   ⇒ 우리 STEP1 에 붙일 때도 **"DL 이 프레임을 건너뛰고 LIGGGHTS 가 몇 천 step 으로 되돌린다"** 가
   합리적 1안이다 (힘 계산을 대체하는 ML potential 보다 **훨씬 낮은 위험**).
2. ★ **rollout 이 실제로 성립한다** — 17 프레임 자기회귀에서 R² 0.9 이상 유지(학습 조성).
   즉 **누적 발산을 물리 투영자가 잡아준다.**  이것이 이 논문의 가장 실용적인 발견이다.
3. ★ **등-예산 대조에서 DEM 단독은 아예 못 간다** (`derived(ours)`): nDEM=7000 총비용 48 min 은
   pure DEM 으로 **1.4 프레임**밖에 못 산다.  ⇒ **"그냥 DEM 을 짧게 돌려라" 는 대안이 아니다.**
   (이것은 이 논문에 **유리한** 계산이다 — 균형 있게 적는다.)
4. ★ **nDEM 이 물리예산 노브**라 **감사 가능**하다: nDEM=0 팔이 **음성 대조**로 상주한다.
   우리 규약(prereg · 음성 대조 · `--compare-dir --expect-differ`)과 궁합이 좋다.

**문헌이 주는 부정 재료 (4가지)**

5. ⛔ **압력 축이 없다.**  우리 300 MPa · Heckel `P_y = 138 MPa` 와 **원리적으로 안 겹친다**.
   이 사슬 3편(슬러리·건조·압연) 중 **어느 것도 MPa 를 들고 있지 않다**
   (압연은 CD %, 건조는 TF).  ⇒ 압력축이 필요하면 진입점은 여전히
   `ngandjong2021_dem_calendering_digital_twin` (0–160 MPa) 또는 ref [33] Xu 2023.
6. ⛔ **Amdahl 천장 6.67×** — 4-lag 시드 요구가 **전체 비용의 15 %** 를 불변으로 남긴다.
   우리가 같은 설계를 쓰면 **시드 프레임 수 = 가속 천장**이 된다.  lag 를 줄이거나
   (조건화 변수로 대체) 시드를 **싼 초기화**로 바꿔야 한다.
7. ⛔ **계면 축이 없다.**  이 논문의 검증량은 **porosity · τ · density = 전부 벌크 1점 통계**다.
   **coordination · coverage · 접촉면적 · 협착 저항 = 0건.**
   ⚠ 자매편 카드가 보인 **"벌크 3–5 % vs 계면 10–17 %" 의 이원성**을 여기서는 **측정조차 안 한다**.
   ⇒ **우리가 재는 양은 전부 계면 쪽**이므로, 이 논문의 정확도는 **우리 축의 정확도 증거가 아니다.**
8. ⛔ **실험 앵커 0건** — §7-3 참조.

**⚠⚠ 우리 쪽 선결조건 (이것이 지금 착수하면 안 되는 이유 — 앞 카드 F-DL4 와 동일, 재확인)**

> 우리 MPM scaffold 의 **정착 porosity 가 플래튼 *정지 프레임* 의 함수**다.
> `--sub` 40 / 80 / 160 → **14.38 / 12.76 / 11.08 %** 로 계속 내려가고 **수렴하지 않는다**;
> sub=80 궤적의 **frame 15 가 정확히 앵커값 15.93 %**, frame 17 이 14.38 % 다.
> 정본: `docs/mpm_platen_kinematic_stop_defect.md` rev6 §31 ·
> `docs/reviews/fam_platen_prereg_20260812.md` §11-1 (**CL-04**: 준정적 ε_sphere **1.13 %** = 실험 15.6 % 대비 **14.5 %p 과압축**).

★★ **이 논문이 그 위험의 교보재다.**  여기서 학습·검증되는 단위는 **프레임**이고, 지표는 **프레임별 R²**다.
만약 우리가 같은 방식으로 STEP2 에 붙이면, surrogate 는 **"플래튼이 몇 번째 프레임에서 멈추나"** 를
물리로 착각하고 배우게 되고 — **그 인공물을 아름다운 R² 로 완벽히 재현한다.**
(그리고 이 논문의 R² 는 **첫 4 프레임이 정확히 1.000** 인 것에서 보듯 **자유점수를 포함**한다 ⇒
지표 자체가 그 착각을 **가려 준다**.)
⇒ **순서는 바뀌지 않는다: SR 트랙 2(플래튼 정지) 종결 → 그 다음 시간-surrogate.**

### 7-3. 항목별 same / different / why

| 축 | 이 논문 | 우리 | 판정 · 왜 |
|---|---|---|---|
| **공정 단계** | 건조(drying) | 압밀(compaction, 300 MPa) | ⛔ **다름** — 상류 단계.  우리 사슬엔 건조가 아예 없다 |
| **압축/압밀 축 단위** | **시간 프레임 (75 µs/TF)** | **압력 (MPa)** + 두께 | ⛔ **원리적 비호환**.  변환 불가 |
| **소재계** | 액체계 LIB (NMC111 + C65 + PVdF + 용매) | **ASSB** (LPSCl + NMC811) | ⛔ 다름.  CBD ↔ SE 는 **역할이 반대**(CBD 는 전자, SE 는 이온) |
| **DEM 입자** | 강체 multisphere(CT 형상) AM + 구형 CBD | 강체 **단일 구** AM_P/AM_S/SE | ⚠ **형상은 그쪽이 낫다**, 소성은 **둘 다 없다** ⇒ frame[2] 같은 칸 |
| **소성** | ⛔ 0 (접촉 소성도 미기재) | DEM = 접촉 소성(δ) · **MPM = 형상 소성** | ✅ **우리가 앞선다** (frame[5] 의 MPM 절반을 그쪽은 통째로 결여) |
| **porosity 규약** | **복셀 라벨 카운트** (`N_pore + 0.5·N_CBD`) / N_total | **ε_sphere (구 부피합)** | ⛔ **다른 규약** — 값 비교 금지.  자매편 카드 §10-② 가 같은 함정을 이미 실측했다 |
| **porosity 절대값** | ⛔ **논문에 하나도 없다** (오직 % 오차) | 15.6 % (real_14) 등 | ⛔ **대조 불가** |
| **수송** | τ · D_eff (공극상 Fick, GeoDict FV) | **σ_ion · σ_e · k** 삼중항 (접촉망 Kirchhoff/Holm + 복셀 FV) | ✅ **우리가 앞선다** (3채널 vs 1채널, 접촉망 vs 복셀만) |
| **계면량** | ⛔ 0 (coverage·Z·접촉면적 없음) | Tabor/Stage-E coverage, Z, A(δ), Holm 협착 | ✅ **우리 고유** |
| **실험 앵커** | ⛔ **신규 0건** — *"validated through experiments"* 는 전부 **ref [33] 상속**이고 **그 숫자는 재인용조차 안 된다** | Minnmann 10 %@300 MPa · Cronau overlap 11–12 % · Bazzoun EIS σ | ✅ **우리가 앞선다** |
| **가속 배수** | 14.25× (논문식) / **4.77× (정직 end-to-end)** | STEP4 AMG 래치 15–34 % 절감 등 | — 규약(F-DL2)은 **분모 3종 병기** |
| **불확실도** | ⛔ seed 0 · 앙상블 0 · 오차막대 0 | LOOCV · Bayesian PI · 중첩 CV · prereg | ✅ **우리가 크게 앞선다** |
| **rollout 명시** | ✅ **명시 + 그림으로 확정** | (해당 없음) | ★ **우리가 배울 규율** |
| **재현성** | 데이터·코드 공개 언급 없음 | — | ⚠ |

### 7-4. ★ 방법 규율로 흡수할 것 (숫자가 아니라 이것)

1. ★★ **시간-surrogate 를 만들면 `rollout` / `teacher-forcing` 을 매니페스트 키로 강제**하고
   **둘 다 보고**한다.  그리고 **rollout R² 가 프레임에 따라 단조 감소하는지**를 1번 그림으로 낸다.
   (이 논문은 rollout 이고 실제로 단조 붕괴한다 — **그 모양이 정상이다.**)
2. ★★ **"시드 프레임" 비용을 분모에 넣는다.**  이 논문의 14.25× → **4.77×** 가 그 차이다.
   가속 배수 보고 3종 세트: **① step 단위 ② end-to-end(시드 포함) ③ 손익분기 런 수.**
3. ★★ **물리 투영 예산(nDEM)을 노브로 노출하고 `nDEM = 0` 을 음성 대조로 상주**시킨다.
   ⚠ 그러나 **nDEM 단조성을 가정하지 말 것** — 이 논문 실측에서 porosity 는 5000→10000 구간에서
   **8/8 침대 중 단조개선 0건**이다(§10-⑥).
4. ★ **trivial baseline 을 *반드시* 같이 싣는다** (§10-⑧): **persistence** · **등속 외삽** ·
   **1-파라미터 affine 붕괴** 셋.  전부 무료이고, 셋 다 **같은 DEM 투영자**를 통과시켜 대조한다.
5. ★ **정규화 여부와 단위를 loss 옆에 반드시 적는다** (§10-②).
   우리 규약으로: `loss_units: {raw_um | minmax_box | zscore}` 를 매니페스트 키로.
6. ★ **porosity 분모(N_total)의 정의를 매니페스트에 박는다** (§10-③) —
   앞 카드 §12-5 가 이미 제안한 `porosity_convention` 키의 **두 번째 교보재**다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

1. ★★★ **STEP1 시간-surrogate 의 설계 원형을 얻었다 — 단, 우리 버전은 "프레임" 이 아니라 "압력" 으로 색인해야 한다.**
   이 논문은 시간축(TF)으로 색인한다.  우리 압밀은 **플래튼 정지 프레임이 물리가 아니다**(CL-04).
   ⇒ **우리 surrogate 의 축은 TF 가 아니라 `wallP`(플래튼 반력) 여야 한다.**
   그러면 (a) 정지-프레임 인공물을 배우지 않고 (b) 실험 BC(300 MPa 정압)와 직접 닿고
   (c) Heckel 축과 바로 겹친다.  ⇒ **"predictor–corrector at constant wallP"** 가 우리 1안.
2. ★★ **물리 투영 예산은 놀랄 만큼 작아도 된다 (0.33 %)** — 그러나 그 이유는 투영자가 고치는 것이
   **겹침(로컬 접촉 위반)** 이라는 국소 제약이기 때문이다.  ⇒ 우리 쪽 대응 제약은
   **① 겹침 ② 플래튼 반력 ③ 질량/부피 보존** 셋이고, **②는 국소가 아니라 전역**이라
   **더 많은 step 이 필요할 가능성이 높다.**  ⇒ nDEM 스윕을 **wallP 수렴 기준**으로 설계.
3. ★★ **계면량은 이 패턴으로 안 될 위험이 크다.**  이 논문은 계면량을 아예 안 재고,
   자매편은 재서 **계면 10–17 % vs 벌크 3–5 %** 를 얻었다.  우리 산출물(coverage·Z·A(δ)·협착)은
   **전부 계면**이다 ⇒ **surrogate 는 구조를 내고, 계면량은 그 구조 위에서 *언제나 물리로 다시 계산*한다.**
   (= GeoDict 를 다시 돌리는 것과 같은 규율.  그 비용을 분모에 적는다.)
4. ★ **per-particle 아키텍처는 우리에게 부적절할 수 있다.**  이 모델은 이웃 좌표를 못 본다
   (C_AM, C_CBD 두 스칼라뿐).  우리 침대는 **AM 골격이 하중을 차폐**하는 구조라
   (AM 차폐 = 1.75 % vs 11–12 % overlap 격차) **이웃 의존성이 훨씬 강하다.**
   ⇒ 최소한 **상별 Z 쌍(Z_AM-AM, Z_AM-SE, Z_SE-SE)** 과 **국소 φ** 를 특징에 넣는다.
5. ★ **`r` 을 출력에 넣을지 지금 결정해야 한다.**  이 모델은 `r` 을 입력만 하고 출력 안 한다
   ⇒ 반경 변화를 **원리적으로 표현 못 한다**.  우리 A10 사이클 축(**±6 % 반경 진동**,
   `dem_mechanical_stresses_ssb_electrode_cycling`)이나 MPM 형상변화를 surrogate 로 다루려면
   **출력 차원에 반경/형상을 반드시 포함**해야 한다.
6. ★ **DEM 호출 오버헤드가 가속의 실제 병목**이다 (`derived(ours)` 6.6× per-step 페널티,
   0.75 min/TF 고정비).  ⇒ 우리가 구현할 때는 **LIGGGHTS 를 프로세스로 재시작하지 말고
   in-memory 로 유지**(라이브러리 모드 / `run ... pre no post no`)해야 한다.
   이것 하나로 이 논문의 14× 가 훨씬 커진다.
7. ⚠ **건조 축 자체는 우리에게 아직 없다** — 그리고 이 논문은 그 구멍을 안 메운다
   (건조 물리가 **한 줄도 없다**).  ⇒ 상류가 필요해지면 진입점은 **ref [33] Xu 2023** ·
   `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `lyu2025_3d_dem_drying_calendering_lib`,
   **ASSB 라면 ref [36] Weitze 2024**(= 정본 `wet_processing_resolved_am_ssb_cathode_manufacturing`).

---

## 9. 인용 가능 문장 (deck / paper 용)

> Galvez-Aranda, Fernandez & Franco (*ACS Appl. Mater. Interfaces* **17**, 32150–32162, 2025) couple a
> per-particle VGG16-derived 1D-CNN to a DEM integrator in a **predictor–corrector** loop: the network
> advances the microstructure by one full frame (1,500,000 DEM steps = 75 µs) and a small number of real
> DEM steps (`nDEM` = 5,000–10,000) then relaxes the unphysical overlaps.  The loop is run **free-running
> (autoregressive rollout)** from four DEM seed frames to the dried electrode (TF 21).  Reported cost is
> 34.2 min per frame for pure DEM versus 2.4 min for the hybrid at `nDEM` = 7,000.

> The paper's own data show that the physics projector, not the network, supplies the structure: retaining
> only **0.33–0.67 %** of the DEM steps removes **81–96 %** of the porosity error of the pure-DL arm
> (59.7 → 3.9 %, 56.6 → 3.4 %, 41.7 → 7.8 %, 60.5 → 2.4 % at `nDEM` = 5,000).

> ⚠ Quote the speed-up with its denominator.  The reported 14.25× (684 → 48 min) excludes the four DEM
> seed frames the 4-lag window requires; those cost 102.6 min = 15 % of the pure-DEM run, so the
> **end-to-end speed-up is 4.77× and is capped at 6.67× no matter how fast the surrogate becomes**
> (Amdahl on the seed frames).  Break-even against the 11-trajectory training set is **≈14 new drying
> simulations** (≈24 if the 8 test-set ground truths are amortised too).

> ⚠ Do **not** cite this paper's extrapolation result.  The heat map that supports the
> "exceptional generalization" claim (Fig 8, 94 % AM / 6 % CBD) reproduces **23 of its 32 cells exactly**
> from the training-formulation heat map (Fig 6, 96/4), under the **same row permutation in both panels**
> — a figure-production error.  The only extrapolation evidence that survives is the RDF R², and it
> **degrades** (> 0.9 → ≈ 0.8), consistent with the authors' own remark that the first RDF peak is
> not reproduced off-formulation.

> ⚠ The drying process axis is **time only** (75 µs per frame; 1.5 ms total).  The paper contains no
> stress or pressure variable of any kind, so it cannot be mapped onto a Heckel / compaction-pressure
> axis.  No DEM material parameters (contact law, E, ν, µ, COR) are given; all are deferred to
> Xu et al., *J. Power Sources* **554** (2023) 232294.  No new experimental validation is performed.

---

## 10. 주의 / 한계 — over-claim 방지 + **내가 잡은 내부 불일치 전수**

### ① ★★ **R² 의 분모가 무엇인지 확인했다 — 그리고 그것이 구조 충실도를 증명하지 못한다** (사용자 지시 검사 #2)

`R² = 1 − Σ_r (g_t − g_p)² / Σ_r (g_t − ḡ)²` 를 **RDF 곡선** 위에서, `r ∈ [0, 4] µm`, `Δr = 0.01` ⇒ **400 bin**.

- 🧮 **첫 4 프레임은 자유점수다.**  Fig 5b/7b 에서 TF 1–4 의 R² 가 **정확히 1.000** 인 것은
  그 네 프레임이 **DL 출력이 아니라 DEM 참값 시드**이기 때문이다.  ⇒ **21 점 중 4 점(19 %)에 정보가 없다.**
  (자매편 카드가 *"0·1·2 = 정확히 100"* 으로 잡은 것과 **같은 구조**다.)
- 🧮 ★★ **배제영역이 공짜 점수다.**  DEM 참값 RDF 는 `r ≲ 0.88 µm` 에서 **정확히 0** 이다 (Fig 5a) ⇒
  **88 / 400 = 22 % 의 bin 이 "겹치지만 않으면 정확히 맞는" 칸**이다.
  **DEM 투영자를 통과한 모든 팔은 그 22 % 를 정의상 전부 얻는다.**
  반면 `nDEM = 0` 팔은 그 영역을 `g ≈ 1.5–3` 으로 채운다 ⇒ 거기서만 분자에
  `≈ 88 × 1.8² ≈ 285` 가 쌓인다.  거친 디지타이즈로 분모 전체가 **≈ 230** 규모이므로
  **배제영역 하나로 R² 가 0 이하로 떨어진다.**
  ⚠ 이 분모 추정은 **peak 폭을 눈으로 읽은 것**이라 **TREND 전용 — 숫자로 인용 금지.**
  그러나 **결론은 강건**하다: **"pure DL vs DL+DEM 의 R² 격차는 주로 *겹쳤는가* 를 재고 있고,
  그것은 DEM 투영자가 정의상 보장하는 것**이지 **건조 궤적이 맞는가**가 아니다."
- ⇒ ★ **R² 0.9 의 의미는 "RDF 의 peak 위치·높이·폭이 대체로 맞다"** 로만 제한해 읽어야 한다.
  그리고 **첫 peak 위치(≈1.45 µm)는 1차입자 지름이 정하는 상수**라 **겹치지 않는 어떤 배치든 재현한다.**
  ⇒ **RDF 는 이 공정에 대해 약한 판별자다.**

### ② ★★ **논문에서 가장 중요한 정확도 숫자(MAE)의 단위가 없다 — 두 읽기가 1,000 배 다르다**

Fig 4: 수렴 **MAE ≈ 0.105**, **MSE ≈ 0.022**.  **정규화 여부·단위가 본문·SI 어디에도 없다.**
🧮 두 읽기:

| 읽기 | MAE 의 물리값 | RDF 첫 peak 1.45 µm 대비 | 자기일관성 |
|---|---|---|---|
| (a) **원시 µm** | **0.105 µm** (= 복셀 0.4 µm 의 1/4) | **0.072×** | ⛔ **모순**.  입자를 0.1 µm 안에 맞히는 모델이 **Fig 5a 처럼 구조 없는 기체**를 낼 수 없다 |
| (b) **min-max 정규화(상자 기준)** | x·y **≈ 3.19 µm** · z **≈ 5.21 µm** | **2.2× / 3.6×** | ✅ **정합**.  입자당 오차가 최근접거리의 2–4배 ⇒ **RDF 가 기체처럼 되는 것이 당연** |

⇒ **(b)가 자기일관적인 유일한 읽기**다.  ⚠ 단정하지 않는다 — **논문이 안 적었다**는 것이 결함이다.
⇒ ★ 만약 (b)라면, **순수 DL 의 입자 위치 오차는 최근접 이웃거리의 2–4 배**이고
**DL 은 입자 수준 구조 정보를 사실상 0 만큼 공급한다** — 구조는 전부 DEM 투영자가 만든다(§3-D 와 정합).
⚠ 이것은 `vijay2025` 카드 §10-D 가 잡은 함정(**정규화 오차 0.017 → 실제 1.7 µm = 접촉거리의 68 %**)의
**정확한 재발**이다.  **같은 그룹, 세 논문 연속.**

### ③ ★★ **porosity 의 분모(N_total)가 정의되지 않았고, 라벨이 하나 사라졌다**

- 규정: *"adding the number of pores voxels and a fraction of the number of CBD voxels … and
  **normalizing it to the total number of voxels**"*, 라벨 = **0/1/2 세 개**.
- 🧮 그런데 격자는 **76 × 76 × 124 = 30.4 × 30.4 × 49.6 µm** 다.
  **건조가 끝난 전극은 초기 습윤 슬러리보다 얇다** ⇒ 격자에 **전극 위 빈 공간**이 남을 수밖에 없다.
  라벨 0(pore)밖에 없으므로 그 헤드룸은 **전부 porosity 로 계상된다.**
- ★★ **자매편은 이 문제를 라벨 하나로 풀었다** — `0=pore / 1=CBD / 2=AM / **4=void**`
  (`galvezaranda2024_…` §4-2).  **이 논문은 그 4 번 라벨이 없다.**
- ⇒ 두 가지 중 하나다: **(a) 격자를 전극에 맞춰 crop 한다** — 그러면 **crop 규칙이 안 적혀 있고,
  crop 자체가 두께 정보를 인코딩**하므로 "porosity 오차"의 일부가 **두께 오차**다
  (= 자매편이 잡은 함정과 같은 부류); **(b) crop 하지 않는다** — 그러면 ε 은 전극 porosity 가 아니다.
- ⚠ **판별 불가**: 논문은 **절대 porosity 를 단 하나도 보고하지 않는다**(오직 % 오차) ⇒
  값의 크기로 역추정할 수도 없다.  ⇒ **이 논문의 porosity 축은 규약이 닫혀 있지 않다.**

### ④ ★★★ **Fig 8 = Fig 6 의 행 치환 복사본 (32 칸 중 23 칸)** — §3-C 참조
초록의 *"exceptional generalization capability"* 를 **출판된 수치로 검증할 수 없다.**
⚠ 본문 94/6 문단이 **Fig 8 의 수치를 단 하나도 인용하지 않는다**는 것이 이 판정을 뒷받침한다.

### ⑤ ★★ **건조 물리가 어디에도 없다 — 그리고 투영자의 "건조 상태" 부기가 불명확하다**

- `evaporat` `solvent`(공정 설명 외) `shrink` `viscos` = **본문 방법론에 0회**.
  ⇒ **이 DEM 이 건조를 무엇으로 표현하는지 알 수 없다** (용매 입자 제거? CBD bead 수축? 응집력 램프?).
  `vijay2025` 의 같은 사슬은 **CBSA Ø7 → CBD 1.3 µm 수축**으로 건조를 흉내낸다.
- ★★ **그래서 다음 질문이 열린 채로 남는다**: hybrid 가 TF 20\* 에서 DEM 을 **7,000 step 만** 돌릴 때,
  그 DEM 은 **자기가 얼마나 건조된 상태인지**를 어디서 읽는가?
  - 건조 구동이 **누적 step 수의 함수**라면 → 투영자는 그 칸이 나타내는 75 µs 가 아니라 **0.35 µs 어치**의
    건조력만 걸게 된다 ⇒ **건조가 17 프레임 내내 과소 적용**된다.
  - 건조 구동이 **구조 상태변수**(예: 현재 bead 반경·응집계수)라면 → surrogate 는 **(x,y,z) 만** 내므로
    그 변수를 **공급하지 못한다**(§4-2).
  ⇒ **둘 중 어느 쪽인지 논문으로 알 수 없다.**  이것은 **결함 주장이 아니라 미결 질문**이지만,
  **우리가 같은 설계를 복제할 때 반드시 먼저 답해야 하는 질문**이다.
  (우리 대응물: 우리 STEP2 의 "건조 상태"에 해당하는 것은 **플래튼 위치/반력**이고, 그것이야말로
   §7-2 의 선결조건이 걸린 바로 그 변수다.)
- 🧮 **시간 규모 경고**: 전체 건조가 **1.5 ms 모사시간**이다.  실제 대류건조는 **수십 초–수 분**이다.
  ⇒ **DEM 시간 ↔ 실제 건조시간의 매핑은 이 논문에 없다.**  *"drying rate"* 는 **모델 파라미터**이지
  물리적 건조율(s⁻¹)이 아니다.  ⇒ **TF 축을 실제 공정 시간으로 읽지 말 것.**

### ⑥ ★ **nDEM 이 정확도 다이얼이 아니다 — 논문 서술과 자기 그림이 어긋난다**

🧮 **nDEM 5000 → 7000 → 10000 단조개선 카운트** (4 침대 × 4 표):

| 표 | 단조 개선 | **10000 이 5000 보다 나쁨** |
|---|---|---|
| Fig 6a (porosity 96/4) | **0 / 4** | **3 / 4** |
| Fig 8a (porosity 94/6) | **0 / 4** | **2 / 4** |
| Fig 6b (τ 96/4) | 3 / 4 | 1 / 4 |
| Fig 8b (τ 94/6) | 3 / 4 | 1 / 4 |

⇒ **porosity 는 8/8 침대에서 단조개선이 0 건**이다.  `nDEM` 은 porosity 축에서 **이진 스위치**
(물리를 걸었나/안 걸었나)이지 **튜닝 다이얼이 아니다.**
⚠ 그런데 94/6 문단은 *"**In all cases**, we have a good decrease in the percentage error when the
nDEM hyperparameter increases"* 라고 쓴다 — **Fig 8a 네 줄 전부와 어긋난다.**
⇒ 🧮 **실무 함의**: nDEM 10000 은 5000 보다 **36 % 더 비싸고**(2.85 vs 2.1 min/TF)
**porosity 는 6/8 에서 더 나쁘다.**  ⇒ **하이퍼 스윕이 porosity 축에서 아무것도 사지 못했다.**

### ⑦ **Table 1 파라미터 수 1 칸 오류**
7번 층 `conv1d 1×256` = **95,860** 으로 인쇄.  🧮 정답 = `256 × (3×128 + 1)` = **98,560**.
**숫자 전치(8↔5) 오타**로 보인다.  총합에 미치는 영향 2,700 (0.011 %) — **무해하지만 표가 자기검산을 안 거쳤다는 신호.**

### ⑧ ★★ **trivial baseline 이 0 개다 — 그래서 세 개를 명세하고, 무엇이 계산 가능한지 갈랐다** (사용자 지시 검사 #1)

논문은 **어떤 기준선도 제시하지 않는다**.  `nDEM = 0` 은 **기준선이 아니라 자기 모델의 고장난 팔**이다
(구조 없는 기체, §5-2) — *"고장난 나를 고친 나"* 는 ablation 이지 baseline 이 아니다.

**내가 요구하는 기준선 3 개** (전부 무료, 전부 **같은 DEM 투영자**를 통과시켜 공정 대조):

| | 기준선 | 정의 | 비용 | **이 논문 데이터로 판정 가능?** |
|---|---|---|---|---|
| **B1** | **persistence** | `x_{n+1}* = x_n` (직전 프레임 복사) → nDEM DEM step | **0** (DL 호출 제거 ⇒ hybrid 보다 **싸다**) | ⛔ **불가** — 프레임별 좌표·porosity 궤적이 공개 안 됨 |
| **B2** | **등속 외삽** | `x_{n+1}* = 2x_n − x_{n−1}` → nDEM DEM step.  ★ **DL 보다 *적은* 정보**(2 lag, 특징 3개)를 쓴다 | **0** | ⛔ **불가** |
| **B3** | **1-파라미터 affine 붕괴** | `z → α z`, `α = h(t+Δ)/h(t)` (전역 두께 수축 1개) → nDEM DEM step | **0** | ⛔ **불가** |

★★ **그런데 "판정 불가" 자체가 판정이다.**  §3-D 가 보인 것 — **0.33 % 의 물리가 porosity 오차의 81–96 %
를 제거한다** — 는 **"투영자가 거의 전부를 한다"** 는 뜻이고, 그렇다면 **B1–B3 중 하나가
23.8 M 파라미터 CNN 과 비슷하게 동작할 가능성이 실질적으로 높다.**
그리고 §10-② (b) 읽기가 맞다면 **DL 의 입자 위치 오차가 최근접거리의 2–4 배**이므로
**B2(등속 외삽)가 그보다 나쁘기도 어렵다.**
⇒ ★ **한 줄 판정**: *"이 논문은 자기 DL 이 필요하다는 것을 증명하지 못했다 — 비교 대상이 자기 자신의
고장난 팔 하나뿐이다."*

**⚠ 균형 — 논문에 유리한 기준선 하나는 내가 계산했고, 논문이 이긴다**:
🧮 **B4 = 등-예산 pure DEM**.  nDEM = 7000 의 총비용 48 min 으로 pure DEM 을 사면
**48 / 34.2 = 1.40 프레임**이다 ⇒ TF 4 → TF 5.4.  **건조 완료(TF 21)에 근처도 못 간다.**
⇒ **"짧게 돌린 DEM" 은 대안이 아니다**, 이 점에서 하이브리드의 가치는 **진짜다.**
남는 질문은 **"하이브리드가 필요한가"(예)** 가 아니라 **"그 안에 23.8 M CNN 이 필요한가"(미증명)** 다.

### ⑨ ★ **가속 배수: 초록과 본문이 서로 다르고, 둘 다 분모가 빠져 있다** (사용자 지시 검사 #3)

| | 총 pure DEM | 총 PAML | 배수 |
|---|---|---|---|
| **초록** | **615 min** | **36 min** | **17.1×** |
| **본문 §3** | **684 min** | **48 min** (nDEM=7000) | **14.25×** |
| 🧮 검산 | 684 = 20 TF × 34.2 ✅ | 48 = 20 × 2.4 ✅ | |
| 🧮 초록의 615 | = **18 TF** × 34.2 (프레임 수가 다르다) | 36 은 **어느 팔과도 안 맞는다** (12/42/48/57) | ⚠ |

⇒ **초록 수치는 본문에서 재현되지 않는다.**  인용한다면 **본문 값(684 → 48, 14.25×)** 을 쓰고,
그마저도 **정직 회계 4.77×** 와 **천장 6.67×** 를 병기한다 (§3-D).
**분모에 빠진 4가지**: 학습시간(미보고) · nDEM 스윕 32 런(≈21 h) · GeoDict 솔브(미보고) · 상류 슬러리.

### ⑩ **검증 분할이 물리적으로 독립이 아니다**
§5-1 참조.  독립 단위는 **11 궤적**이지 3.7 M 행이 아니고, **분할 방법이 안 적혀 있다.**
*"avoiding overfitting"* 주장의 근거(train≈val 곡선)는 **이 설정에서 약하다.**
⚠ **진짜 일반화 시험은 8 개 hold-out TS** 이고, 그 중 **4 개(94/6)의 결과 그림이 §10-④ 로 오염**됐다.

### ⑪ 기타 한계 (저자 자인 포함)
- **전이 한계 자인**: force field 파라미터가 학습셋과 크게 다르면 정확도 하락 (§4 결론).
- **거시 불균일 불가 자인**: *"not designed to capture macroscopic in-plane heterogeneities"* (§1).
- **열 물성 불가 자인**: DL 은 입자 위치만 배워 **thermal 같은 전역 물성을 못 낸다** (§4 결론).
- **좌표계**: Cartesian, **병진·회전 불변성 없음**.  저자 정당화 = *"샘플이 많고 상자 크기가 같다"*
  ⇒ ⚠ **상자 크기가 바뀌면 전이 불가** (저자 자인: *"We do not attempt to extrapolate … to generate larger samples"*).
- **입자간 거리 미사용 자인**: *"we deliberately chose not to incorporate interparticle distance as a
  descriptor … as it is inherently accounted for during the DEM steps"* ⇒ **설계가 투영자에 의존한다는 자백.**
- **seed / 앙상블 / 오차막대 / 불확실도 = 전부 0.**
- **데이터·코드 공개 언급 없음** ⇒ 재현 불가.
- **CBD 를 단일 유효상**으로 (나노공극 ξ=0.5 **가정**, 점탄성 없음).

---

## 11. 기술 미니-용어집 (이 논문을 읽는 데 필요한 것만)

- **PAML (Physics-Assisted Machine Learning)** — 물리를 **손실함수·출력층 제약**으로 넣는
  *Physics-**Constrained*** ML 과 구분되는 계열.  여기서는 **물리 솔버를 예측 사이에 끼워 넣는 방식**
  = 사실상 **predictor–corrector**.  저자들이 *"first-time application of PAML to LIB electrode manufacturing"* 주장.
- **predictor–corrector / multiple-time-stepping** — 싼 근사로 크게 전진(predictor)하고
  비싼 정확한 연산자로 되돌리는(corrector) 고전 수치 기법.  분자동역학의 RESPA,
  AIMD↔CMD 하이브리드(본문 ref [25])와 같은 계열.  ★ **이 논문의 실질**이 이것이다.
- **rollout (free-running) vs teacher forcing** — 시계열 추론의 두 방식.
  rollout = **자기 예측을 다시 입력**(오차 누적, surrogate 를 주장하려면 반드시 이쪽);
  teacher forcing = 매 스텝 **실제 과거**를 입력(오차 누적 없음, 그러나 참값 생성기가 계속 필요).
  ★ **이 논문은 rollout 이고 Fig 3 의 색 부호로 확정된다.**
- **LE (Local Environment)** — cutoff(≈3 µm) 안의 이웃으로 정의한 입자별 기술자.
  여기서는 `[x,y,z,r,C_AM,C_CBD]` 6 개.  ⚠ **이웃의 좌표는 안 들어간다** — 개수 2 개뿐.
- **TF (Time Frame)** — 이 논문의 공정 축.  1 TF = **1,500,000 DEM step = 75 µs**.  **압력이 아니다.**
- **nDEM** — DL 예측 두 번 사이에 돌리는 **진짜 DEM step 수**.  이 논문이 신설한 하이퍼파라미터이자
  **물리 예산 노브**.  `nDEM = 0` = 순수 DL(음성 대조).
- **RDF g(r)** — 2점 상관.  ★ **peak 위치는 입자 지름이 정하는 상수**라, 겹치지 않는 어떤 배치든
  1차 peak 를 재현한다 ⇒ **공정 판별력이 약하다.**
- **CBD (Carbon-Binder Domain)** — 카본블랙 + 바인더를 **하나의 유효상**으로 뭉친 것.  Franco 그룹 표준.
- **MacMullin 수 / τ** — 여기 규약은 **`τ = ε / D_eff`** (D_pore ≡ 1).
  ⚠ 문헌에 `τ = N_M·ε` 와 `τ² = N_M·ε` 두 규약이 섞여 있다 — **절대값 비교 시 규약 확인 필수.**
- **GeoDict DiffuDict** — Math2Market 의 복셀 기반 확산 FV 솔버.
  우리 STEP3(`voxel_conductivity.py` / `step3_sigma.py`)와 **원리적으로 같은 종류**.
- **VGG16** — 3×3 필터 13 conv + 3 dense 의 이미지 분류망.  ★ 여기서는 **Conv1D 로 개조**되었고,
  **입력 길이가 4 뿐이라 hierarchy 가 성립하지 않는다** (§4-3) ⇒ **상표에 가깝다.**

---

## 12. 미해결 / 다음에 할 것

1. ✅ **자매편 §12-1 의 세 질문 전부 답했다** (§0 표).  앞 카드 §10-⑤ / §12-1 을 갱신했다.
2. ✅✅ **확보·digest 완료 2026-09-11 → 정본 카드 `papers/xu2023_realistic_am_shape_cgmd_calendering.md`**
   (ref [33] Xu, Ngandjong, Liu, Zanotto, Arcelus, Demortière, Franco, *J. Power Sources* **554** (2023) 232294 —
   *"Lithium ion battery electrode manufacturing model accounting for 3D realistic shapes of active material particles"*).
   ★ 앞 카드가 ref [36] 으로 부르던 바로 그 논문.  **위 §12-2 의 네 질문에 대한 답**:
   ① **접촉법칙 = Lennard-Jones(모든 쌍) + JKR(겹친 쌍), LAMMPS** (⚠ LIGGGHTS 아님).
      **E** CBD_liquid 0.0005 / CBD_solid 2 / **AM 135** / Al 69 / Steel 200 GPa · **ν = 0.3 다섯 상 전부**
      (★ `ngandjong2021` 의 **ν_CBD = 0.5 비압축이 사라졌고 설명이 없다**) · **μ_t = 0.5**(Ngandjong X_u 0.001 의 500배) ·
      **COR 없음** — `η_n = η_n0·a·m_eff` 점성 감쇠(CBD 10 / AM 500)로 대체 · γ(JKR): AM-intra 10⁶ / **AM-inter 0** /
      CBD 80→400 pg µs⁻² (= **1000 / 0 / 0.08→0.4 J/m²**, `derived(ours)`).
      ⛔ **timestep 미기재 · 플래튼 속도 미기재 · 시드 미기재** ⇒ 준정적성 검산 불가.
   ② **건조 = CBD bead Ø6.2 → 1.3 µm 순간 수축**(= `ngandjong2021` 과 **완전히 같은 값**) **+ force field 전면 교체**
      (LJ 우물 CBD **×10⁶**, AM–AM 인력 **0 → 켜짐**).  최종 두께는 **실험 밀도·porosity 로 미리 계산해 지정** =
      ★ **건조 두께는 예측이 아니라 입력**이다.
   ③ ⛔ **압력 축 없다** — 본문·SI 전수 `MPa` **0 회**; 공정 축은 **CD 0–42.2 %** 뿐.
   ④ **검증 실체**: 슬러리 밀도 **2 점**(exp 2.03/2.14 vs sim 2.04/2.18) · porosity-vs-CD **exp 8 점** ·
      **µ-XCT 볼륨 2 개**(96:2:2 uncal + "30 % 압축")에서 서브볼륨 20 개 평균 **τ 1.599 ± 0.086 / 2.664 ± 0.31**.
      ⛔ **그 중 τ 는 독립 검증이 아니다** — SI 가 **dilation–erosion 인자를 τ 의 XCT 값에 맞춰** 골라
      *"to process **all** the results"* 라고 적는다.  **porosity 상속만 유효.**
3. ⬜ ★ **ref [36] Weitze, Zanotto, Zapata Dominguez, Franco, *Energy Storage Mater.* **73** (2024) 103747**
   — *"Simulating solid-state battery cathode manufacturing via wet-processing with resolved active
   material geometries"*.  ★★ **이 사슬의 유일한 ASSB 편**이고 정본 카드가 이미 있다
   (`wet_processing_resolved_am_ssb_cathode_manufacturing`, digested 2026-06-26).
   ⇒ **그 카드를 이 계보(F-DL 계열)에 재연결**하고, **ASSB 습식 제조에 압력 축이 있는지** 재확인한다.
4. ⬜ ★★ **우리 STEP1/STEP2 시간-surrogate 의 설계 문서** — 단 **선결조건 뒤**:
   `docs/mpm_platen_kinematic_stop_defect.md` (SR 트랙 2) 종결.
   설계 결정 4개를 §8 에서 미리 고정했다: **축 = wallP(TF 아님)** · **출력에 반경/형상 포함 여부** ·
   **특징에 상별 Z 쌍 포함** · **LIGGGHTS in-memory 유지**(호출 오버헤드 6.6× 회피).
5. ⬜ **기준선 B1–B3 를 우리 파이프라인의 상주 대조로 배선** (§10-⑧).
   ⚠ 이 논문·자매편 **둘 다 기준선이 0 개**다 — 같은 그룹, 두 편 연속.
6. ⬜ **매니페스트 키 2 종 신설 제안** (두 카드 공통 교보재):
   `porosity_convention: {sphere_sum | union | voxel_label}` (§10-③) ·
   `loss_units: {raw_um | minmax_box | zscore}` (§10-②) ·
   `inference_protocol: {rollout | teacher_forced}` (§7-4-1).
7. ⬜ **보충영상 2편** — 이 컨테이너에서 디코딩 불가.  WSL 에서 열어 **DEM vs DEM+DL 의 붕괴 궤적**을
   육안 대조하면 §10-② 의 (a)/(b) 읽기를 **직접 판별**할 수 있다 (입자가 얼마나 튀는지 보면 된다).

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
