# Using resistor network models to predict the transport properties of solid-state battery composites — Ketter (Nat. Commun. 2025) · voxel 저항망(RN)으로 NCM83–LPSCl 복합양극의 effective σ_ion·σ_e·κ 를 예측하고 EIS·DC·LFA 실측으로 검증

> slug `ketter2025_resistor_network_models_predict_transport_properties` · DOI `10.1038/s41467-025-56514-5` · type `exp (EIS-TLM impedance · DC polarization · LFA thermal diffusivity) + voxel resistor network (FD/SOR) — microstructure · percolation · porosity; no DEM/MPM` · PDF `fb389ab9-s41467-025-56514-5.pdf` · digested `2026-09-25` · status ✅
> SI `3f005fac-41467_2025_56514_MOESM1_ESM.pdf` (34 pp) · Source Data `235bb755-41467_2025_56514_MOESM3_ESM.zip` (본문 9 + SI 32 = **41 CSV 전수 대조**) · evidence `fulltext + Source Data` · 그림 `31/31 육안 확인` (본문 Fig 1–5 · SI Fig S1–S22 · SI Table S1–S4; **14장 재크롭** — `pdf_map.tsv` 참조) · 약칭 `[Ketter25RN]`
> ⚠ **이력** — 2026-09-03 research-agent 가 **초록만으로** 뼈대를 만들었고(그때 "LPSCl 0.32 ± 0.02 / NCM83 0.71 ± 0.04" 메모가 생겼다) → 2026-09-22 **1저자 결정으로 삭제**(`0eaef03bf`; `_INDEX_proposals.md` "⛔ 제외" 절) → **2026-09-25 재개**: 사용자가 본문·SI·Source Data 를 직접 올렸고, 원장 `SELF-51`(지어지거나 오귀속된 인용 뿌리 뽑기)이 우리 코드의 `κ_SE = 0.7 W m⁻¹ K⁻¹ "(Ketter 2025)"` 귀속을 원문으로 확인하라고 요구했다. 이 카드가 그 확인이다.
> 수치 등급 표기: **stated** = 본문·SI 문장/표에 인쇄 · **SD** = 저자 공개 Source Data CSV (그림 뒤의 정확한 값 — 디지타이즈 없음) · **derived(ours)** = 우리 산수 (인용 시 "우리 계산" 명시) · figure-read 는 이 카드에 **없다**.

---

## 0. ★ SELF-51 판정 — 우리 `κ_SE = 0.7 W m⁻¹ K⁻¹` 는 LPSCl 값인가 NCM 값인가 (이 카드를 연 이유)

| 질문 | 원문의 답 | 조건 | 출처 위치 | 등급 |
|---|---|---|---|---|
| Ketter 가 잰 **LPSCl** κ | **0.32 ± 0.02 W m⁻¹ K⁻¹** (SD: 0.32297 ± 0.02117 @ 298.16 K) | 25 °C · LFA 열확산 D × **계산** C_V × 기하밀도 ρ_geo, **3회 평균 ± 표준편차** · 펠릿 = 370 MPa 3 min 선압 → **등방 500 MPa 60 min** · **ρ_rel 87.87 ± 0.64 %** (ρ_geo 1.634 / ρ_theo 1.86 g cm⁻³) = 공극 ≈ 12 % | 본문 p. 4 ("LPSCl shows the lowest thermal conductivity in the series with 0.32 ± 0.02") · `Table S3` (dispersed phase 입력) · SD `Fig4b`·`Fig4c` · `Fig. S4b`·`Fig. S16b` 의 기준선 라벨 **"κ_LPSCl"** | stated + SD |
| Ketter 가 잰 **NCM83** κ | **0.71 ± 0.04 W m⁻¹ K⁻¹** (SD: 0.70577 ± 0.04209) | 같은 절차 · **ρ_rel 70.76 ± 1.70 %** (3.382 / 4.78) = 공극 ≈ 29 % | 본문 p. 4 ("With a value of 0.71 ± 0.04 W m⁻¹ K⁻¹, NCM83 shows the highest…") · `Table S3` (continuous phase 입력) · 기준선 라벨 **"κ_NCM"** | stated + SD |
| 우리 `0.7` 과 같은 것은 | **NCM83 행 (0.71)** | — | — | — |
| 이 논문 안에 **LPSCl ≈ 0.7** 이 있기는 한가 | **있다 — 0.66 W m⁻¹ K⁻¹. 단 측정이 아니라 입력이다.** Böger *et al.* 2023 (*ACS Appl. Energy Mater.* 6, 10704 — **같은 Zeier 그룹**, Bernges 공저) 의 LPSCl 값을 **치밀 SE 상**으로, Ar 기공 0.017 과 섞어 다공 LPSCl 의 κ 를 모사했다 (`Fig. 5b`) | RN 곡선의 φ_LPSCl = 100 % 끝점. Böger 실측점 6개(φ 75.4–90.9 %)의 최고값 0.498 보다 위 | 본문 p. 5 ("Assuming κLPSCl = 0.66 W m⁻¹ K⁻¹ for the electrolyte³⁰") · `Table S3` · SD `Fig5b` | stated(입력) · **Böger 원문 미확인** |
| 우리 서지 문자열 `Ketter, F. et al. (2025). Thermal conductivity of LPSCl argyrodite.` | **이 저자·제목의 논문은 없다.** 실물 = **Ketter, L.**, Greb, N., Bernges, T. & Zeier, W. G. "Using resistor network models to predict the transport properties of solid-state battery composites." *Nat. Commun.* **16**, 1411 (2025). 이니셜(F. ≠ L.)·제목 **둘 다 틀렸다** | — | 본문 p. 1 · 참고문헌 56·57 (저자 datastore 자기인용) | — |

**판정 = 유형 B (쟀는데 다른 양 — 다른 상) + 서지 변형.**
원문에 `0.71` 이 인쇄돼 있으므로 *"Ketter 에 0.7 이 있다"* 는 검색만으로는 통과한다 — 그것이 **NCM83 행**이라는 것을 읽어야 걸린다. `comparison_vs_ours.md` §I 의 규율 *"유형 B 가 더 위험하다"* 의 실례다. 코드 주석 `step3_sigma.py:1035` 의 *"Ketter 2025 = LPSCl/SE 논문 … Ketter는 SE"* 도 틀렸다 — 이 논문은 **두 상과 복합체를 모두 잰 복합양극 저항망 논문**이다.

**값 자체의 지위 (라벨과 분리)**
- 우리 두 솔버에서 `K_SE_THERMAL` 이 서는 자리는 **치밀·무공극 고체상**이다 — DEM 접촉망(`network_conductivity.py`)은 접촉을 따로 두고, STEP3 복셀(`step3_sigma.py`)은 기공을 셀로 명시(또는 0)한다. 그 규약에서 Ketter 의 **펠릿값 0.32(공극 ≈ 12 % + 입자간 접촉·입계 포함)는 맞는 양이 아니다** — 넣으면 기공·접촉을 **이중 계상**한다.
- ⚠⚠ **그런데 우리 SE 입력은 규약이 이미 섞여 있다.** 같은 날 정본 `cronau2021_stack_pressure_ionic_conductivity` 카드(SI 보강)는 `σ_grain = 3.0` 을 **"µC-Li₆PS₅Cl 펠릿, 적층압 ≥ 150 MPa 평탄의 하단"** 으로 판정했다 = **펠릿 lumping 값** (단결정 아님). 그러면 SE 의 **σ 는 펠릿 규약**, κ 를 0.66(치밀)으로 읽으면 **κ 는 치밀 규약** — 한 상의 두 입력이 서로 다른 규약에 서 있다. ⇒ κ_SE 의 "맞는 값" 은 **규약 결정의 함수**이고, 그 결정은 σ_grain 과 **함께** 내려야 한다 (원장 `SELF-51`; 아래 선택지 D). 펠릿 쪽으로 통일해도 두 펠릿은 상태가 다르다 — Cronau σ 는 **적층압 하**, Ketter κ 는 **등방 500 MPa 성형 후 무하중** LFA.
- 같은 논문이 **치밀 LPSCl 상**으로 쓴 값이 **0.66** 이다 → 우리 0.7 은 *값으로는* 그 자리에 있다 (+6 %). 그러나 근거는 Ketter 가 아니라 **Böger 2023** 이어야 하고, 그 0.66 이 Böger 원문에서 무엇인지(치밀 외삽? 별도 시료? 계산?)는 Ketter 에 적혀 있지 않다 → **n/a, Böger PDF 필요**.
- ⚠ **폭이 있다** — Ketter 자신의 LPSCl 펠릿(ρ_rel 87.87 %, 0.323)을 Fig 5b 와 같은 RN 기공 모델(치밀 0.66 + Ar 0.017)에 맞춰 치밀 쪽으로 되돌리면 **≈ 0.44 W m⁻¹ K⁻¹** 가 된다 [derived(ours): 같은 밀도에서 RN 곡선 0.482 대비 실측 0.323 = 0.670 배 → 0.66 × 0.670; **모델 의존 — 인용 금지, 폭만**]. 원인은 **같은 밀도 ~88 % 에서 Böger 실측 0.440(φ 88.34 %)과 Ketter 실측 0.323(87.87 %)이 27 % 어긋나기** 때문이다 (시료·합성·밀링 차; 논문 무언급). ⇒ "치밀 LPSCl κ" 는 **이 논문 한 편 안에서도 0.44–0.66** 이다.
- **NCM 쪽**: 우리 `K_AM_THERMAL = 4.0 W m⁻¹ K⁻¹` (출처 없음, 주석이 스스로 *"generic NCM 문헌-order; 전용 인용 없음"*) 에 대해 Ketter 는 **치밀 NCM κ 를 주지 않는다** (0.71 은 공극 29 % 펠릿). 지지도 반박도 아니다. 다만 **펠릿끼리의 비 κ_NCM83/κ_LPSCl = 2.22** 로 우리 코드의 비 **5.71** 보다 작고, **부호(NCM > LPSCl)는 측정으로 확인**된다 (`huang2025_dem_lbm_heat_conduction_composite_cathode` 카드 §7 이 열어 둔 질문의 답).

**권고 (⛔ 미실행 — 사용자 규칙 "보고 → 설명 → 비준 → 실행")**

| 선택지 | 내용 | 조건 |
|---|---|---|
| **A** | 값 0.7 유지 + 라벨을 *"치밀 LPSCl, Böger 2023 의 0.66 (Ketter 2025 `Table S3` 가 치밀상 입력으로 쓴 값) 근방 — Böger 원문 확인 전 `Assumed`"* 로 교체 | 가장 작은 변경. Böger 확인 뒤 B 로 승격 가능 |
| **B** | 값을 0.66 으로 + Böger 2023 직접 인용 | **Böger PDF 확인 필수** (0.66 의 정의) |
| **C** | Ketter 0.32 는 **펠릿-유효값 비교 전용** (예: 우리 복합체 κ 를 Ketter `Fig. 4c` 에 대보는 검증) — 치밀 규약을 쓰는 한 고체상 입력으로는 쓰지 않는다 | A·B 와 병행 |
| **D** (먼저) | **SE 입력 규약을 하나로 정한다** — σ_grain 3.0 은 펠릿 lumping 값(cronau2021 카드 09-25)이다. ① **치밀 규약**: κ_SE ≈ 0.44–0.66 (이 카드 §0 폭), σ_grain 에도 치밀·입내 값이 필요 (현재 출처 없음) ② **펠릿 규약**: κ_SE 0.32 (Ketter, ρ_rel 88 %, 무하중) — 단 STEP3 는 기공을 따로 명시하므로 **기공 이중계상**을 감수하거나 보정해야 한다 | 1저자 판단 — σ 와 κ 를 **같은 규약**에 세우는 것이 목적. 이 카드는 판단하지 않는다 |

그리고 어느 선택지든 **서지 문자열 2곳 + 코드 주석 4곳 교체** (§7-7 목록).

---

## 1. 한 줄 요약

Zeier 그룹(뮌스터)의 Ketter·Greb·Bernges·Zeier 는 **300³ voxel(2 µm/voxel → 600 µm 정육면체) 합성 미세구조** 위에 **면-인접 저항망(반-voxel 직렬 = 조화평균 링크 + 이종상 계면저항 R_int/dx)** 을 SOR 로 풀어 NCM83(LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂)–Li₆PS₅Cl 복합양극의 유효 **σ_ion · σ_e · κ** 를 계산하고, 같은 조성 6점(φ_NCM 0/20/40/60/80/100 vol%)의 **EIS(T-type TLM) · DC 분극 · LFA** 실측과 비교했다. 망의 입력은 **순수상 펠릿의 실측값 넷뿐**(σ_ion,LPSCl 2.33 · σ_e,NCM83 5.22 mS cm⁻¹ · κ 0.32 / 0.71 W m⁻¹ K⁻¹)이고 **접촉저항·기공은 망에 없다 — 대신 펠릿값이 그것을 품고 들어온다**. σ 는 5 자릿수에 걸쳐 로그 척도로 맞지만 **φ_NCM ≥ 60 % 의 σ_ion 을 10.7–58× 과대**하고, κ 는 **LPSCl|NCM83 계면열저항 2 × 10⁻⁶ m² K W⁻¹** 를 넣어야 40 % 까지 따라온다. 복합양극 κ 는 조성·VGCF(≤ 5 wt%)와 무관하게 **< 1 W m⁻¹ K⁻¹** 이다. 문헌 3건(LiMn₂O₄–Li₃InCl₆ · 다공 LPSCl · PEO 계 고분자)에 같은 모델을 적용했고, Si–LPSCl–C 1건은 **실패**를 SI 에 스스로 실었다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Lukas Ketter**¹˒², Niklas Greb¹, Tim Bernges¹, **Wolfgang G. Zeier**¹˒²˒³ (교신) |
| 소속 | ¹ Institute of Inorganic and Analytical Chemistry, Univ. Münster · ² International Graduate School BACCARA, Univ. Münster · ³ Forschungszentrum Jülich, IMD-4 (Helmholtz-Institute Münster) — SI 는 같은 곳을 옛 이름 **IEK-12** 로 적는다 |
| 서지 | *Nature Communications* **16**, 1411 (2025) · DOI `10.1038/s41467-025-56514-5` · Open Access CC BY 4.0 |
| 일자 | 접수 2024-06-16 · 승인 2025-01-20 · 온라인 게재일 표기는 PDF 본문에 없음 (PDF 메타데이터 생성일 2025-02-06) |
| 데이터 / 코드 | 데이터 DOI `10.17879/54928371863` · **RN 코드 DOI `10.17879/16948580876` (MIT 라이선스)** — 둘 다 Univ. Münster datastore (참고문헌 56·57) |
| 기여 | L.K.·T.B.·W.G.Z. 착상 · L.K. 실험(N.G. 기여)·해석·**RN 코드 작성**·계산·집필 |
| 자금 · 계산 | BMBF FESTBATT (03XP0597A) · BACCARA(NRW) · HPC **PALMA II** (Univ. Münster) · 이해상충 없음 |
| 재료계 | **NCM83 (LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂, MSE Supplies)** + **Li₆PS₅Cl (자체 고상합성)** + VGCF (Sigma-Aldrich, 1–5 wt% 시리즈만) · **바인더 없음** |
| 연구유형 | 실험(EIS-TLM · DC 분극 · LFA · XRD-Pawley · SEM/EDX) + **voxel 저항망 시뮬레이션**(자작 코드) · **DEM/MPM/FEM/DFT 없음** |
| 같은 그룹 짝 카드 | `schlautmann2023_se_particle_size_composite_transport` (Ketter 가 공저자 · **같은 LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂** — 그 논문은 "NCM811" 로 표기) · `minnmann2021_jes_charge_transport_bottlenecks` (TLM 원전, ref 12) · `bielefeld2019_…`·`bielefeld2020_…` (refs 8·9) · `aminchiang2016_…` (ref 44) |

## 3. 핵심 수치 ★

### 3-1. 순수상 — RN 의 입력이 된 실측값

| 양 | LPSCl | NCM83 | 조건 | 지위 | 출처 |
|---|---|---|---|---|---|
| **σ_ion** | **2.33 mS cm⁻¹** (SD 2.33404) | ≈ 0 — 입력 **10⁻¹⁰⁰ mS cm⁻¹** (수치적 0) | 25 °C · EIS 강철‖LPSCl‖강철 · 고주파 절편을 R–CPE 로 맞춤 (`Fig. S8a`) · 셀: 100 mg, 370 MPa 3 min 성형 → 측정 중 50 MPa | LPSCl = **측정 → 입력** · NCM = **가정** (ref 44 Amin & Chiang 2016 이 "자릿수 아래" 근거) | SI p. S12 ("2.33 mS cm⁻¹ was determined for LPSCl") · `Table S3` · SD `Fig3d` |
| **σ_e** | ≈ 0 — 입력 10⁻¹⁰⁰ | **5.22 mS cm⁻¹** (SD 5.22147) | 25 °C · DC 분극, 이온차단 강철 스탬프 · −40…+50 mV 계단, 계단당 3.5 h · 정상전류 V–I 기울기 (`Fig. S14a`) | NCM = **측정 → 입력** · LPSCl = **가정** (ref 45 Gorai 2021) | 본문 p. 3 ("the experimentally assessed values for σion,LPSCl and σe,NCM were taken as input") · SI §S4.3 · `Table S3` · SD `Fig3d` |
| **κ (25 °C)** | **0.32 ± 0.02 W m⁻¹ K⁻¹** | **0.71 ± 0.04 W m⁻¹ K⁻¹** | LFA 펠릿(등방 500 MPa 60 min) · 3 시료 평균 ± SD | 측정 → 입력 | 본문 p. 4 · `Table S3` · SD `Fig4c` |
| κ(T) 173 → 298 → 373 K | 0.336 → 0.323 → 0.330 | 0.675 → 0.706 → 0.687 | "remarkably low and approximately constant" | 측정 | SD `Fig4b` |
| 열확산 D (298 K, 3 시료) | 0.182 · 0.204 · 0.194 → 평균 **0.193 mm² s⁻¹** | 0.283 · 0.288 · 0.269 → **0.280 mm² s⁻¹** | NETZSCH LFA 467, 개량 Cape–Lehmann | 측정 | SD `FigS15` |
| C_V (= C_p 로 근사) | 0.798 (173 K) · **1.022 (298 K)** · 1.081 (373 K) J g⁻¹ K⁻¹ | 0.470 · **0.746** · 0.829 | LPSCl = Böger 의 포논 계산 · NCM83 = LiNiO₂/LiCoO₂/LiMnO₂ 포논 DOS(Yang 2020)의 0.83/0.11/0.06 가중 | **계산** (측정 아님) | SI §S6 · SD `Fig4a` |
| ρ_geo / ρ_theo / **ρ_rel** | 1.634 ± 0.012 / 1.86 / **87.87 ± 0.64 %** | 3.382 ± 0.081 / 4.78 / **70.76 ± 1.70 %** | LFA 펠릿 (등방 500 MPa 60 min) · 3회 | 측정 | SI §S7 · SD `FigS18a` |
| 입자 / 도메인 크기 | 도메인 **d ≈ 20 µm** | 입자 **d ≈ 2 µm** | 위색 SEM(φ_NCM 80 %) 판독 | stated (저자) | 본문 p. 3 |
| 격자상수 (LFA 전 → 후) | F-43m a = 9.85557(7) → 9.8545(14) Å | R-3m a = 2.8721(2) → 2.87287(3) · c = 14.1841(14) → 14.1879(4) Å | Pawley, TOPAS-Academic V6 | 측정 (LFA 전후 부반응 없음 확인) | `Table S2` |

- **재현 검산** [derived(ours)]: κ = ρ·D·C_V → LPSCl 1634 kg m⁻³ × 1.933 × 10⁻⁷ m² s⁻¹ × 1022 J kg⁻¹ K⁻¹ = **0.323** ✓ · NCM83 3382 × 2.800 × 10⁻⁷ × 746 = **0.707** ✓ (SD 0.323 / 0.706). ⇒ κ 는 **계산 C_V 에 선형으로 걸린다** — C_V 가 5 % 틀리면 κ 도 5 % 틀린다.
- 본문의 C_V 범위 문장("LPSCl 0.72–1.10 · NCM83 0.39–0.85 J g⁻¹ K⁻¹")은 SD 로 보면 **≈ 150–400 K 창**의 양끝이다 (캡션의 173–373 K 창에서는 0.80–1.08 / 0.47–0.83). 사소한 표기 차.
- 순수상 σ 의 오차막대는 **값의 ±50 %** — `Fig. S22` 캡션이 밝히는 **그림 규약**이지 측정 불확도가 아니다 ("Each data point corresponds to a single measurement", `Fig. 3d` 캡션).

### 3-2. 복합체 유효 σ — 실측(DC · EIS) vs RN (SD `Fig3d`, mS cm⁻¹, 25 °C)

| φ_NCM (vol%) | σ_e DC | σ_e EIS | **σ_e RN** | σ_ion DC | σ_ion EIS | **σ_ion RN** | RN/실측 (e) | RN/실측 (ion) | 실측 σ_ion/σ_e |
|---|---|---|---|---|---|---|---|---|---|
| 0 | — | — | 10⁻¹⁰⁰ | — | **2.334** | 2.33 (입력) | — | — | — |
| 20 | 0.01466 | 0.01373 | 0.00918 | 1.024 | 1.791 | 1.247 | **0.63–0.67** | 0.70–1.22 | 70 (DC) · 130 (EIS) |
| 40 | 0.2086 | 0.2257 | 0.5126 | 0.3300 | 0.3579 | 0.4482 | **2.27–2.46** | 1.25–1.36 | **1.58 · 1.59** |
| 60 | 1.035 | 1.121 | 1.620 | 0.01083 | 0.00926 | 0.1162 | 1.44–1.57 | **10.7–12.6** | 0.0105 · 0.0083 |
| 80 | 1.985 | 1.718 | 3.230 | 7.18 × 10⁻⁵ | 5.83 × 10⁻⁵ | 3.37 × 10⁻³ | 1.63–1.88 | **47–58** | 3.6 × 10⁻⁵ · 3.4 × 10⁻⁵ |
| 100 | **5.221** | — | 5.22 (입력) | — | — | 10⁻¹⁰⁰ | — | — | — |

RN 전 곡선 (10 % 간격, SD): σ_e = 5.22 · 4.193 · 3.230 · 2.372 · 1.620 · 0.9958 · 0.5126 · 0.1732 · 0.00918 · 7.40 × 10⁻⁷ · 0 (φ_NCM 100 → 0) · σ_ion = 0 · 5.65 × 10⁻⁵ · 0.00337 · 0.0391 · 0.1162 · 0.2413 · 0.4482 · 0.7900 · 1.247 · 1.768 · 2.33 (φ_NCM 100 → 0).
- 본문: σ_e 10¹ … 10⁻² · σ_ion 10¹ … 10⁻⁵ mS cm⁻¹ 범위, **"closest to each other for φ_NCM = 40 %"** — 실측 σ_ion/σ_e ≈ 1.6. RN 의 교차점은 φ_NCM ≈ 39 % [derived(ours), 30·40 % 사이 로그 보간].
- ⚠ **SI p. S16 의 문장은 σ_e 와 σ_ion 이 뒤바뀌어 있다**: *"both circuits yield σe = 0.36 mS cm⁻¹ and σion = 0.23 mS cm⁻¹"*. SD 의 TLM 값은 σ_e **0.2257** · σ_ion **0.3579**, DC 는 0.2086 · 0.3300 이고, 원 임피던스로도 확인된다 [derived(ours)]: 이온차단(전자 경로) 저주파 끝 Z′ ≈ **327.6 Ω** vs 전자차단(이온 경로) ≈ 300.6 Ω − Z_block(LiIn|LPSCl 대칭셀 `Fig. S8b`, ≈ 91 Ω) ≈ **210 Ω** ⇒ R_ion < R_e ⇒ **σ_ion > σ_e**. SD 열 이름은 조성에 대해 단조(σ_e↑·σ_ion↓)로도 일관하다.
- 20 % 에서 σ_ion 의 DC(1.024)와 EIS(1.791)가 **1.75× 어긋난다** — 두 방법 일치를 내세우는 논문의 표에서 가장 큰 불일치 (논문 무언급).

### 3-3. 복합체 κ_RT — 실측 vs RN (계면열저항 ITR 유무) (SD `Fig4c`, W m⁻¹ K⁻¹, 25 °C)

| φ_NCM | 실측 ± SD | 펠릿 공극 (100 − ρ_rel) | RN (ITR 없음) | RN (+ITR) | RN/실측 | (RN+ITR)/실측 | ITR 효과 | (실측 − RN_ITR)/SD |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.32 ± 0.02 | 12.13 % | 0.32 (입력) | 0.32 | — | — | — | — |
| 20 | 0.36 ± 0.02 | 15.62 % | 0.373 | 0.338 | +4 % | −6 % | −9.4 % | +1.1 |
| 40 | 0.40 ± 0.04 | 21.16 % | 0.441 | 0.396 | +10 % | −1 % | −10.2 % | +0.1 |
| 60 | 0.44 ± 0.03 | 22.42 % | 0.520 | 0.483 | +18 % | **+10 %** | −7.1 % | −1.4 |
| 80 | 0.50 ± 0.07 | 25.33 % | 0.611 | 0.590 | +22 % | **+18 %** | −3.5 % | −1.3 |
| 100 | 0.71 ± 0.04 | 29.24 % | 0.71 (입력) | 0.71 | — | — | — | — |

(RN 10 % 간격 전 곡선: 무 ITR 0.32 · 0.3446 · 0.373 · 0.405 · 0.441 · 0.479 · 0.520 · 0.5644 · 0.6108 · 0.6594 · 0.71 / +ITR 0.32 · 0.3233 · 0.338 · 0.363 · 0.396 · 0.437 · 0.483 · 0.5341 · 0.5897 · 0.6485 · 0.71, SD.)
- **ITR = 2 × 10⁻⁶ m² K W⁻¹** (LPSCl|NCM83, 이종상 링크에만): *"it is found empirically that better agreement … can be achieved"* (p. 5). 문헌 범위 — 완전 계면(포논 부정합) 10⁻⁹–10⁻⁷, 거친·다공 거시 계면 10⁻⁶–10⁻³ (ref 48 Zheng 2021) — 의 **가장 낮은 자릿수**에서 고른 한 값이다. 불확도·민감도 스캔은 없다.
- 이 값의 크기 감각 [derived(ours)]: 2 µm 링크 하나의 컨덕턴스 (0.5/0.71 + 0.5/0.32)⁻¹ = 0.441 → ITR 포함 (… + R_int/dx = 1)⁻¹ = **0.306 (−30.6 %)**. 같은 저항을 두께로 바꾸면 LPSCl 펠릿 **0.64 µm** · NCM83 펠릿 **1.42 µm** 에 해당.
- ITR 을 넣어도 **60·80 % 는 +10·+18 % 과대가 남는다** (1.3–1.4 SD) — ITR 로 설명된 것은 **일부**다.
- ⚠ 80 % 복합체의 κ(T) 는 298 → 323 K 에서 **0.499 → 0.424 로 계단 하락**한다 (≤ 273 K 에서는 0.531–0.550, 173 K 의 SD 가 ±0.139). "온도에 대략 일정" 서술과 어긋나는 **시료 거동** — 논문 무언급 (SD `Fig4b` 관찰).
- 복합체 D(298 K) 는 20–80 % 가 0.192–0.207 mm² s⁻¹ 로 거의 같다 (LPSCl 0.193, NCM83 0.280) ⇒ 복합체 사이 κ 차이의 대부분은 **ρ·C_V** 에서 온다 [derived(ours), SD `FigS15`·`FigS18a`·`Fig4a`].

### 3-4. VGCF 첨가 (φ_NCM = 40 %, 1–5 wt%) — SD `FigS4a`·`FigS4b`·`FigS18b` · DC 분극 · 단일 측정

| VGCF wt% | σ_e (mS cm⁻¹) | 배수 | σ_ion (mS cm⁻¹) | 변화 | κ_RT (W m⁻¹ K⁻¹) | 변화 | ρ_geo (g cm⁻³) |
|---|---|---|---|---|---|---|---|
| 0 | 0.2086 | 1 | 0.3300 | — | 0.404 ± 0.044 (3회) | — | 2.387 |
| 1 | 5.406 | ×25.9 | 0.1565 | **−52.6 %** | 0.447 | +10.8 % | 2.567 |
| 2 | **56.92** | **×273** | 0.1359 | **−58.8 %** | 0.459 | +13.6 % | 2.529 |
| 3 | **73.81** (최대) | ×354 | 0.1507 | −54.3 % | **0.528** (최대) | +30.7 % | 2.514 |
| 4 | 52.85 | ×253 | 0.0994 | −69.9 % | 0.387 | −4.2 % | 2.409 |
| 5 | 45.88 | ×220 | 0.0396 | **−88.0 %** | 0.287 | −28.9 % | **1.991** (급락) |

- 저자 서술: 본문 *"electronic conductivity increases over two orders of magnitude upon introduction of **<2 wt.%** VGCF, only **minor** influences on the ionic conductivity"* · SI *"for VGCF contents **above** 2 wt.%"*. ⇒ **문구가 서로 다르고**, 데이터는 1 wt% ×26 · 2 wt% ×273 이다 (두 자릿수는 **2 wt% 에서** 넘는다). "minor" 는 전자 이득에 견준 말일 뿐 σ_ion 은 **1–3 wt% 에서 절반 이하**로 떨어진다.
- VGCF 고유 σ_e 는 **n/a** (재지도, 모델링도 안 함). VGCF κ "above **1700** W m⁻¹ K⁻¹" (refs Ting & Lake 1995; Heremans 1985 — **문헌 인용**), VGCF 비열 **0.7 J g⁻¹ K⁻¹** (Ting & Lake — 문헌). κ 가 거의 안 오르는 이유로 저자는 **흑연 섬유의 강한 이방성 + 섬유–기지 부착 불량 → 큰 계면열저항**을 든다 (가설, 정량 없음). 3 wt% 초과의 κ 하락은 **밀도·열확산 하락**(`Fig. S18b`, `Fig. S16a`) 때문이라고 적는다.
- VGCF 는 **RN 으로 모사하지 않았다** — "additives that cannot be simply modelled by a voxel approach" (p. 6).

### 3-5. 문헌 사례 (RN 입력 = 그 논문의 보고값) — `Table S3` · SD `Fig5a–c`·`FigS21`

| 사례 | 계 | 연속상 / 분산상 입력 | s_clust | 결과 (SD) |
|---|---|---|---|---|
| Hendriks 2023 (ref 13) | LiMn₂O₄–Li₃InCl₆ (할라이드) | σ_e,LMO **0.12** / σ_ion,LIC **0.23 mS cm⁻¹** | 500 | 대체로 일치 · 단 φ_LMO 60 % 의 σ_ion 은 RN 0.0115 vs 실측 **0.00172 (6.7× 과대)** — 우리 계와 같은 **고-CAM 이온 과대** 패턴 |
| Böger 2023 (ref 30) | 다공 LPSCl (Ar 기공) | Ar **0.017** / LPSCl **0.66 W m⁻¹ K⁻¹** | 500 | φ 75–91 % 실측 0.269–0.498 · RN "slightly overestimating" (φ 88.3 % 에서 RN ≈ 0.49 vs 실측 0.440 [derived(ours) 보간]) · ⚠ Böger 는 **같은 Zeier 그룹** (Bernges 공저) |
| Froboese 2019 (ref 15) | PEO:LiTFSI:SiO₂ 기지 + 이온차단 입자 (0–20 · 0–50 · 40–70 · 70–110 µm) | 기지 **0.619 mS cm⁻¹** / 차단상 10⁻¹⁰⁰ | **10⁰ · 10¹ · 10² · 10³ · 10⁴ · 5 × 10⁴** | 작은 입자일수록 σ_ion 이 더 떨어지는 크기효과 재현 · **~30 vol% 넘어서는 감소를 약하게 예측** (저자 명시) |
| Rudel 2023 (ref 11) — SI 전용 | Si–LPSCl–C 음극 | 차단상 10⁻¹⁰⁰ / LPSCl **2.16 mS cm⁻¹** | **1** | **실패**: RN 은 ~30 vol% 에서 급한 문턱을, 실측은 완만한 감소를 보인다 (φ_LPSCl 40 %: RN 0.058 vs 0.0082 = **7×** · 50 %: 0.229 vs 0.031 = **7.3×** · 30 %: 7.0 × 10⁻⁵ vs 0.0040 = **57× 과소**) — 저자: *"no well-defined microstructure"* |

### 3-6. 망 크기 — 60³ (dx 10 µm, s_clust 4) vs 300³ (dx 2 µm, s_clust 500) · SD `FigS22`

| φ_NCM | σ_e 300³ | σ_e 60³ | σ_ion 300³ | σ_ion 60³ | κ+ITR 300³ | κ+ITR 60³ |
|---|---|---|---|---|---|---|
| 20 | 0.00918 | **3.3 × 10⁻¹¹** | 1.247 | 1.299 | 0.338 | 0.361 |
| 40 | 0.5126 | 0.2600 | 0.4482 | 0.5720 | 0.396 | 0.421 |
| 60 | 1.620 | 1.337 | 0.1162 | 0.1435 | 0.483 | 0.499 |
| 80 | 3.230 | 3.026 | 0.00337 | **1.35 × 10⁻⁹** | 0.590 | 0.595 |

- 비용: **60³ "< 1 hour, Laptop" · 300³ "up to 5 days, HPC"** (조성 시리즈 하나 기준, `Fig. S22` 그림 안 문구).
- 두 망의 클러스터 **부피는 같다** [derived(ours)]: 500 × (2 µm)³ = 4 × (10 µm)³ = **4000 µm³ = 등가구 지름 19.7 µm** — SEM 의 LPSCl 도메인 d ≈ 20 µm 에 맞춘 선택으로 읽힌다 (논문은 "comparable homogeneity" 로만 적는다).
- 문턱 근처(20 % σ_e, 80 % σ_ion)에서 60³ 은 **자릿수로 무너진다** (실측 σ_e 20 % = 0.0147). ITR 효과는 60³ 에서 약하다 — **계면 수가 적어서** (저자) ⇒ **ITR 적합값은 해상도에 묶인 값**이다.

## 4. 방법 ★

### 4-1. 저항망 (RN) — 무엇을 푸는가
- **지배식**: 정상상태 Fourier `q = −κ∇T` (Eq. 1) · Ohm `J = −σ∇ϕ` (Eq. 2). 전하와 열을 **같은 망, 같은 코드**로 푼다 (채널마다 상 전도도만 바꾼다).
- **노드** = 각 voxel 중심 (T_i,j,k 또는 ϕ_i,j,k). **링크** = 면-인접 6 이웃 (`Fig. S2b`, `Fig. 2c`).
- **링크 전도도** (Eq. S2, 같은 상 / 다른 상 공통): 두 반-voxel 의 직렬 = **조화평균** `κ_{i,j+½,k} = (0.5/κ_{i,j,k} + 0.5/κ_{i,j+1,k})⁻¹`.
- **이종상 링크** (Eq. S3): `κ_{i,j+½,k} = (0.5/κ_{i,j,k} + 0.5/κ_{i,j+1,k} + R_int/dx)⁻¹` — **면마다 직렬 시트저항 R_int 를 더하는 형**이다. ⇒ 물리적으로 "링크 하나 = dx·(0.5/κ_a + 0.5/κ_b) + R_int 의 면적당 저항" 이라 **dx 에 대해 일관**된 계면항 구현이다 (Aalilija 2021, SI ref 3). 논문에서 R_int ≠ 0 은 **열 채널에만** 썼다.
- **경계조건** (`Fig. S2a`): 마주 보는 두 면에 **무한전도 voxel 층 + 고정 T/ϕ**, 나머지 네 면은 **단열/절연(zero-flux)**. 주기경계는 **망에는 없다** (미세구조 생성 때만 cyclic).
- **유효값**: 정상상태 분포에서 **평균 플럭스 밀도**를 구해 1D 로 Eq. 1/2 를 뒤집는다 (`Fig. 2d` 의 선형 T/ϕ 프로파일 + 양끝 평탄 구간 = 무한전도 경계층).
- **접촉저항 · Holm 협착: 없다.** 같은 상 voxel 두 개는 2 µm × 2 µm 면으로 **완전 접촉**한다. 입자간 접촉·입계·기공의 효과는 **순수상 펠릿 실측값이 lumping 해서 들고 들어온다** — 저자: *"As the input parameters … were taken from porous samples and a linear relationship between composition and density exists, porosity is accounted for in the simulation to a certain extent, although the actual pore structure is not explicitly simulated"* (SI §S7).

### 4-2. 수치해석
- **SOR** (successive over-relaxation, Gauss–Seidel 식 제자리 갱신): Eq. S5 `T_spot = Σ κ_n T_n / κ_sum` → Eq. S6 `T^{n,SOR} = T^{n−1} + ω(T^n − T^{n−1})`, **ω = 1.979** (300³ 권장값, Qiao 2013 = SI ref 1). 초기값 = 선형 T 분포.
- **잔차** (Eq. S7): `r = (1/n_tot) Σ |κ_sum T_spot − Σ κ_n T_n| / κ_sum`, 50 반복마다 계산 · 수렴 = **r < 10⁻⁹ K** (문턱 근처·고대비 몇 경우만 r < 5 × 10⁻⁹ K 로 완화, "treated with caution"). `Fig. S3a` 대표 곡선: ~2500 반복에 10⁻⁹ 도달.
- 전하 채널은 같은 코드에 σ 를 넣는다 (잔차 단위만 K → V).
- **검증** (`Fig. S3`): ① 직렬·병렬 층상 구조가 해석해(Eq. S8·S9)를 재현 (κ 0.71/0.32, R_int = 0) ② **Yuge 1977** 의 수정 EMT (Eq. S10) — 30³, s_clust = 1(무상관 site 혼합), σ_end 0.1–0.9 vs 1 — 재현.
- **망 크기**: 본 계산 300³ (PALMA II HPC), 경량판 60³ (§3-6). 조성 간격 Δφ_disp = 10 % (`Table S3` 캡션). **실현(시드) 수는 적혀 있지 않다 → n/a** (조성당 한 구조로 읽힌다).

### 4-3. 미세구조 생성 — **합성**(FIB-SEM 도 DEM 도 아니다)
- 입력 3 개: 한 변 voxel 수 L_vox, 분산상 부피분율 φ_disp, 클러스터 크기 s_clust (`Fig. S1`, SI §S1.1).
- 연속상으로 채운 정육면체에 **분산상 클러스터를 반복 삽입**: 클러스터 수 `n_clust = int(φ_disp·n_tot / (100·s_clust))` (Eq. S1) → 무작위 씨앗에서 **표면에만 voxel 을 붙여 키우는** 성장, 생성 중 cyclic 경계 → **클러스터 간 겹침 허용** → 겹침과 int 절삭으로 모자란 부피는 **클러스터 없이 낱 voxel 로 채움**.
- NCM83–LPSCl: **NCM83 = 연속상(단일 voxel ≈ 2 µm 입자)**, **LPSCl = 분산상(500-voxel 클러스터 ≈ 20 µm 도메인)**. 전자 채널: 연속 5.22 / 분산 10⁻¹⁰⁰ · 이온 채널: 연속 10⁻¹⁰⁰ / 분산 2.33 · 열: 연속 0.71 / 분산 0.32 (`Table S3`).
- **기공 상 없음** (NCM83–LPSCl 계산). 다공 LPSCl 사례(Böger)에서만 Ar 기공을 **연속상**으로 두었다.
- SEM/EDX 대조는 **정성**(`Fig. 2b`, `Fig. S5–S7`): 실측 EDX 에서 저-φ_NCM 의 LPSCl 은 수십 µm 로 **이어진 영역**, NCM 은 **수십 µm 응집체**를 이룬다 — RN 은 NCM 을 **단일 voxel 로 분산**시킨다.

### 4-4. ★ 입자 처리 (DEM 의 "무질서 처리"에 해당하는 칸)
- **구도 형상도 없다** — 입자는 **voxel(정육면체) 덩어리**다. NCM83 입자 = voxel 1 개, LPSCl 도메인 = 500-voxel 무작위 성장 덩어리.
- **PSD 없음** — 상마다 한 크기 (모노). 크기효과는 **s_clust 스윕**으로만 다룬다 (Froboese 사례 10⁰–5 × 10⁴).
- **역학 없음** — 압밀·재배열·**CONTACT 소성도 SHAPE 소성도 없다**. 압력은 실험에만 있고 모델에는 기하로도 들어오지 않는다.
- ⇒ 우리 frame 으로: **frame[5] 의 전달(transport) 절반만** 가지며 그 안에서도 **접촉 단위 물리가 없다**. DEM(패킹·접촉망)·MPM(형상 소성) 어느 쪽 짝도 아니다.

### 4-5. 실험
- **LPSCl 합성**: LiCl (Sigma-Aldrich 99 %) · Li₂S (Thermo 99.9 %) · P₄S₁₀ (Sigma-Aldrich 99 %) 화학량론 → 손 분쇄 15 min → 손 프레스 → 탄소 코팅 석영 앰플 진공 봉입 → **550 °C (100 °C/h 승온) 2 주** → 자연 냉각 → 손 분쇄.
- **소프트 밀링**: NCM83 (MSE Supplies, 250 °C 진공 하룻밤 건조) · VGCF (Sigma-Aldrich, 250 °C 건조) · 부피비 계산 밀도 **LPSCl 1.86 · NCM83 4.78 g cm⁻³** (refs Deiseroth 2008 · Woo 2009) · ZrO₂ 볼 3 mm 3.6 g + 분말 400 mg · ZrO₂ 15 mL 컵 · **15 Hz 15 min** (Fritsch Pulverisette 23 Mini Mill). 순수상도 같은 밀링을 거친다.
- **조성 (`Table S4`)**: φ_NCM/φ_LPSCl 100/0 · 80/20 · 60/40 · 40/60 · 20/80 · 0/100 ↔ w_NCM/w_LPSCl 100/0 · **91/9 · 79/21 · 63/37 · 39/61** · 0/100 (위 밀도로 정확히 재현됨 [derived(ours)]).
- **전기 셀**: 기밀 셀 케이싱(ref 55), 재료 100 mg, **370 MPa 3 min 성형 → 측정 중 50 MPa**. 이온차단 = 강철 스탬프. 전자차단 = 양쪽에 **LPSCl 80 mg 층 + In 박(100 µm, Ø 9 mm) + Li 박(1.5 mg) → LiIn** (`Fig. 3a`, `Fig. S9`). ⚠ 셀 지름·두께·성형 후 밀도는 **n/a** (본문에 없음).
- **EIS**: BioLogic VMP-300, 25 °C 항온기, OCV 2 h 평형, **7 MHz – 100 mHz, 15 점/decade, 10 mV**, RelaxIS3 로 적합.
- **DC 분극**: Metrohm Autolab PGSTAT302N, 25 °C, **−40…+50 mV 계단 × 3.5 h**, 정상전류로 V–I 적합 (`Fig. 3c`, `Fig. S13`, `Fig. S14`).
- **LFA**: 펠릿 370 MPa 3 min 선압 → **등방 500 MPa 60 min** · NETZSCH LFA 467 · **−100 … +100 °C, 25 °C 간격**, N₂ 100 mL/min · 흡수·방사용 **탄소 코팅**(N₂ 글러브박스) · MCT 검출기 + ZnS 창 · 온도당 3 샷(−100 °C 만 5) 평균 ± SD · **개량 Cape–Lehmann 모델** (NETZSCH LFA Analysis 8.0.3). 공기 노출 < 30 s — LFA 전후 XRD 에 부상 없음 (`Fig. S19`, `Fig. S20`, `Table S2`).
- **C_V 계산** (SI §S6, Eq. S12): 정규화 포논 DOS g(ω) 로 `C_V = (3zR/M) ∫ g(ω) (ħω/k_BT)² e^{ħω/k_BT}/(e^{ħω/k_BT} − 1)² dω` · LPSCl 은 Böger 의 포논 계산값 · NCM83 = 0.83 C_V(LiNiO₂) + 0.11 C_V(LiCoO₂) + 0.06 C_V(LiMnO₂) (`Fig. S17`) · 복합체 = 질량가중 (Eq. S13) · **C_p ≈ C_V** 근사.
- **XRD**: STOE STADI P, Mythen 2X 1K, Ge(111), Cu Kα1, 2θ 10–70° (원문 "step size of 3°"), 밀봉 모세관, Pawley (TOPAS-Academic V6, 수정 TCH pseudo-Voigt, Chebyshev 9 항).
- **SEM/EDX**: Zeiss AURIGA CrossBeam, Au 스퍼터 · SEM 3 kV In-lens · EDX 20 kV, X-Max 80 mm².

## 5. Figure set ★ (31장 전부 실독 — 이 카드의 크롭은 `litdb/figures/ketter2025_…/`)

| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| **1** | 복합전극 모식도 vs voxel 표현 (상면도) | "voxel 로 줄여도 굴곡·도메인 크기는 남는다"는 논문의 전제 그림 |
| **2** | (a) 300³, φ_NCM 80 % voxel 구조 + ΔT/Δϕ 경계 (b) 위색 SEM φ_NCM 80 % (LPSCl 노랑 d ≈ 20 µm, NCM83 보라 d ≈ 2 µm) (c) voxel 과 6 이웃 = 망 노드 (d) 정상상태 평균 T/ϕ 프로파일 (0–600 µm 선형 + 양끝 평탄) | (c) = 우리 STEP3 7-점 스텐실과 같은 구조 · (d) = 유효값 추출 방식 (평균 플럭스 → 1D Ohm/Fourier 환산) — 우리 STEP3 의 유효값 정의(전류·두께·면적·전위차)와 같은 층위 · ⚠ 자동 크롭은 (c)(d) 를 잘랐다 → 재크롭 |
| **3** | (a) 이온/전자 차단 셀 + T-type TLM (b) φ_NCM 40 % EIS (이온차단 ~328 Ω 까지 두 호 · 전자차단 ~300 Ω) + TLM 적합 (c) φ_NCM 40 % DC V–I (d) **σ_e·σ_ion vs φ_NCM — DC(원) · EIS(사각) · RN(점선)** | ★ **이 카드의 근거 그림** (§3-2). (d) 의 오차막대 = ±50 % 규약. 40 % 에서 σ_ion > σ_e 가 눈으로도 보인다 · ⚠ 자동 크롭이 오른쪽 절반(패널 d 전부)을 잘랐다 → 재크롭 |
| **4** | (a) 계산 C_V(T), 조성별 (b) κ(T) 173–373 K (c) **κ_RT vs φ_NCM: 실측 · RN · RN+ITR** | ★ **κ 판정의 근거** (§0 · §3-3). 80 % 곡선의 계단 하락이 (b) 에서 보인다 · ⚠ 색 범례 라벨(LPSCl → NCM83) 잘림 → 재크롭 |
| **5** | (a) Hendriks LMO–LIC σ_e/σ_ion vs φ_LMO (b) **Böger 다공 LPSCl κ vs φ_LPSCl** + RN (c) Froboese 차단 입자 크기 4 종 vs RN 클러스터 10⁰–5 × 10⁴ (d) φ_block 20 % 에서 클러스터 크기별 voxel 구조 | (b) = LPSCl 치밀 입력 **0.66** 이 쓰인 자리 (§0) · (c)(d) = **도메인 크기 → σ 효과를 s_clust 하나로 푸는 법** — 우리 d_h 접힘·SE 입경 축과 같은 질문 · ⚠ 윗 띠 잘림 → 재크롭 |
| S1 | 미세구조 생성 알고리즘 (클러스터 수 결정 → 성장·삽입 → 모자란 voxel 보충) | 우리 합성 RVE 생성기(`pellet_rve_sigma.py` 류)와 대조할 **가장 단순한 기준선** |
| S2 | (a) 경계조건 (T_hot/T_cold 면, 나머지 κ = 0) (b) 6 이웃 노드 (c) 링크 κ 세 경우: 같은 상 · 절연 경계(0) · 이종상 + R_int/dx | ★ Eq. S3 의 그림판 — **면 직렬 계면항**의 시각적 정의 (§7-6) |
| S3 | (a) SOR 잔차 vs 반복 (~2500 회에 10⁻⁹ K) (b) 직렬/병렬 해석해 재현 (c) Yuge 수정 EMT 재현 (30³, s_clust 1) | 코드 검증 절차의 최소 세트 — 우리 selftest 와 같은 층위 · ⚠ 위에 식 S8/S9 문단이 섞여 있었다 → 재크롭 |
| S4 | (a) **VGCF 0–5 wt% 에서 σ_e·σ_ion** (b) κ_RT + 기준선 **κ_NCM 0.71 · κ_LPSCl 0.32** | ★ (b) 의 두 기준선 라벨이 **"0.7 = NCM" 의 가장 빠른 시각 증거** · (a) = 우리 Phase A (VGCF 조성) 의 **무-PTFE 실험 짝** (§8-③) |
| S5 | SEM · EDX(S 노랑/Ni 자홍) · RN 입방체 — LPSCl · φ_NCM 20 · 40 % | 실측 LPSCl 은 큰 결정립 사이 균열·기공, 저-φ_NCM 에서 LPSCl 이 연속 영역 |
| S6 | 같은 세트 — φ_NCM 60 · 80 % · NCM83 | 고-φ_NCM 에서 LPSCl 이 **고립 섬** — 이온 문턱의 실물 |
| S7 | φ_NCM 80 %: EDX 겹친 SEM vs 위색 SEM | `Fig. 2b` 위색의 근거 |
| S8 | LPSCl 임피던스: (a) 강철 접점 — 스파이크, 절편 ≈ 45 Ω → R–CPE (b) LiIn 접점 — 원점에서 떨어진 반원 (≈ 62–91 Ω) → R + ZARC | (a) = σ_ion 2.33 의 원천 (**벌크+입계 합**, RT 에서 분리 안 됨) · (b) = 전자차단 셀의 Z_block 보정 · ⚠ 본문 한 줄 섞임 → 재크롭 |
| S9 | T-type TLM 사다리 (z_ion · z_e · z_int), (a) 이온차단 (b) 전자차단 + Z_block | Minnmann 2021 TLM 과 같은 회로 (`minnmann2021_…`) · ⚠ 재크롭 |
| S10 | 이온차단 EIS 적합 — 20 · 40 · 60 · 80 % (20 % 는 kΩ 급 미폐합) | 전자 경로 저항의 조성 의존 원자료 |
| S11 | 전자차단 EIS 적합 — 20 · 40 · 60 · 80 % (80 % 는 kΩ 급 스파이크) | 이온 경로 저항 원자료 · 80 % 이온 붕괴 |
| S12 | φ_NCM 40 % 저주파 영역을 MIEC 등가회로(R_ion ∥ R_e + CPE, 전자차단은 + Z_block)로 적합 | TLM 과 **같은 값**이라는 교차검증 — 단 SI 문장은 σ_e/σ_ion 을 **뒤바꿔** 적었다 (§3-2) · ⚠ 재크롭 |
| S13 | φ_NCM 40 % DC 원자료: 계단별 I(t) 와 V–I (R_e · R_ion + R_block) | 3.5 h 계단의 정상 도달 확인 · ⚠ 재크롭 |
| S14 | 모든 DC 적합: (a) 이온차단 — NCM83·80·60·40·20 % (b) 전자차단 (c)(d) VGCF 1–5 wt% | (a) 순수 NCM83 기울기 ≈ 24.0 Ω → σ_e 5.22 의 원천 · (c) VGCF 고함량 기울기 ~1–1.7 Ω [derived(ours)] → §10-9 · ⚠ 재크롭 |
| S15 | 열확산 D(T) — 6 조성 × 3 시료 | κ 의 D 성분 · 80 % 시료 간 산포 큼 |
| S16 | VGCF 시료 D(T) · κ(T) + 기준선 κ_NCM / κ_LPSCl | `Fig. S4b` 와 같은 두 기준선 |
| S17 | LiNiO₂/LiCoO₂/LiMnO₂ 포논 DOS → C_V, 0.83/0.11/0.06 가중 → NCM83 C_V | κ 의 C_V 성분이 **계산**임을 보이는 그림 |
| S18 | (a) ρ_rel · ρ_geo · ρ_theo vs φ_NCM (b) VGCF 시료 ρ_geo | ★ **κ 입력이 다공 펠릿값**이라는 근거 (공극 12 → 29 %) |
| S19 | XRD + Pawley, LFA 전/후 — LPSCl · 20 · 40 % | 부상 없음 |
| S20 | 같은 것 — 60 · 80 % · NCM83 | 부상 없음 |
| S21 | Rudel Si–LPSCl–C σ_ion vs φ_LPSCl + RN (s_clust 1) | ★ **실패 사례** — "잘 정의된 미세구조" 가정의 경계 (§3-5) |
| S22 | 60³ / s_clust 4 ("< 1 h, laptop") vs 300³ / s_clust 500 ("up to 5 days, HPC") — σ 와 κ | 해상도·비용 교환 · 문턱 근처에서 60³ 붕괴 · ITR 효과의 해상도 의존 (§3-6) · ⚠ 재크롭 |
| Table S1 | 임피던스 적합 χ² (모듈러스 가중, 자유도당): 3.0 × 10⁻⁷ … 2.5 × 10⁻⁴ (최악 = `Fig. S11c` 60 % 전자차단) | 적합 품질 · ⚠ 본문 한 줄 섞임 → 재크롭 |
| Table S2 | Pawley 격자상수, LFA 전/후 | §3-1 |
| **Table S3** | **RN 입력 전부** — 그림 · L_vox · s_clust · 연속/분산상 전도도 · R_int | ★ **이 카드의 두 번째 근거 표** — 0.71 이 연속상(NCM83), 0.32 가 분산상(LPSCl), 0.66 이 Böger 분산상(LPSCl) 입력임을 한 표에서 확인 |
| Table S4 | 부피비 ↔ 질량비 | §4-5 |

## 6. Post-processing ★
- **임피던스**: T-type TLM (Siroma 2015 식, Minnmann 2021 이 NCM622–LPSCl 에 쓴 것) — Eq. S11 `Z_CC = z_e z_ion/(z_e+z_ion)·L + 2 z_e² √z_int/(z_e+z_ion)^{3/2} · (cosh(√((z_e+z_ion)/z_int)·L) − 1)/sinh(…)` · z_ion = R, z_int = CPE, z_e = R + ZARC (전자 벌크 + 전자 계면) · 이온차단은 전자 레일, 전자차단은 z_ion↔z_e 를 바꾸고 **Z_block (R + ZARC, `Fig. S8b`) 을 직렬 차감**. 저항 × 전극 길이 = 유효 총저항 → `σ = h/(A·R)`. 교차검증 = MIEC 회로(Zahnow 2021). 적합 도구 **RelaxIS3**, 품질 `Table S1`.
- **DC 분극**: 계단 전압마다 정상전류 → V–I 선형 적합 기울기 = 총저항 (이온차단 → R_e, 전자차단 → R_ion + R_block).
- **열**: LFA 신호 → 개량 Cape–Lehmann (NETZSCH LFA Analysis 8.0.3) → D · `κ = ρ·D·C_p` (C_p ≈ 계산 C_V) · 3 시료 평균 ± SD.
- **RN**: 평균 플럭스 → 1D Ohm/Fourier 로 유효값 · 조성 10 % 간격 스윕 · 실측과 같은 그림에 겹쳐 그림 (선형 점선은 "guide to the eye").
- **구조**: Pawley (TOPAS-Academic V6) · SEM 위색은 EDX 겹침으로 확인 (`Fig. S7`).
- **플롯 규약**: 전기 실측 = 단일 측정, 오차막대 ±50 % · 열 실측 = 3회 평균 ± SD · Source Data 전부 공개 (이 카드의 수치는 전부 SD 와 일치 확인).

## 7. 우리 DEM+MPM 대비 ★★

> ⚠ 정본 `our_dem_baseline.md` 는 **값 0 개 자리표시자**다 — 아래 "우리" 칸은 작업 브랜치 `claude/stoic-knuth-NObVQ` (@ `766c0405b`, 2026-09-25) 의 **코드 줄 번호**에서 직접 읽었다.

### 7-1. 열 — κ_SE (§0 요약)
| 항목 | Ketter 2025 | 우리 | 판정 |
|---|---|---|---|
| κ LPSCl | **0.32 ± 0.02** (펠릿, 공극 ≈ 12 %) · 치밀 입력 0.66 (Böger) | `K_SE_THERMAL = 0.7e-2 W/(cm·K)` "LPSCl (Ketter 2025)" — `network_conductivity.py:132` · `step3_sigma.py:1039` | **라벨 오귀속** (0.71 = NCM83). 값은 치밀 규약에서 0.66 근방이라 **방어 가능하나 근거는 Böger** (미확인) |
| κ NCM | **0.71 ± 0.04** (펠릿, 공극 ≈ 29 %) · 치밀값 없음 | `K_AM_THERMAL = 4.0e-2` (출처 없음) — `network_conductivity.py:131` · `step3_sigma.py:1038` | Ketter 는 판정 불가 (치밀 NCM 미측정) |
| 비 κ_AM/κ_SE | **2.22** (펠릿끼리) | **5.71** (코드 `k_ratio`, `network_conductivity.py:362`) | 부호 일치 · 크기 근거 없음. ⚠ 그 비를 쓰는 열 `k_weight` 는 프로덕션에 **한 번도 적용되지 않았다** (CLAUDE.md σ_thermal 절 정정 배너, CL-12) |
| 계면열저항 | **2 × 10⁻⁶ m² K W⁻¹** 적합 (해상도 의존) | 없음 — STEP3 prov: *"Kapitza 계면 열저항 무시 → 상한"* (`step3_sigma.py` `thermal_k_table`) | ★ **"상한" 라벨의 실험적 크기**: ITR 없는 voxel RN 은 이 계에서 실측을 **+4 ~ +22 %** 넘었다 (§3-3) |
| 복합체 κ 실험 앵커 | **있다** — 6 조성 LFA (25 °C, 173–373 K) | STEP3 prov: *"열전도 실험 앵커 없음"* | ★ **정본 litdb 최초의 NCM–LPSCl 복합체 κ 실측** — 단 공극 15–25 % 펠릿·무탄소·LPSCl 20 µm (§7-5) |

### 7-2. 전자 — σ_e(NCM) 와 우리 `σ_AM`
| 우리 값 | 자리 | Ketter NCM83 **5.22 mS cm⁻¹** 대비 |
|---|---|---|
| **50 mS cm⁻¹** `SIGMA_AM_ELECTRONIC = 0.05` "NCM811 grain interior, discharged" | DEM 접촉망 `network_conductivity.py:57` | **9.6×** 위 |
| **10 mS cm⁻¹** `sigma_am_s` 기본 (NMC811) | STEP3 `mpm_webapp_payload.py:1422-1423` | 1.9× |
| **5 mS cm⁻¹** `sigma_am_p` 기본 (NMC811) | STEP3 `mpm_webapp_payload.py:1424-1425` | 0.96× |
| σ_S 10 / σ_P 5 (Stage 22.5 LOCKED 엔드포인트, 코퍼스 적합값) | σ_e 스케일링 폼 (CLAUDE.md) | 1.9× / 0.96× |

- **원문 확인된 상온 NCM8xx σ_e 앵커가 이제 둘이다**: `wang2018_…` NMC811 **4.1 mS cm⁻¹** (20 °C, **SPS > 98 % 치밀**, DC) + 이 카드 NCM83 **5.22 mS cm⁻¹** (25 °C, **냉간가압 분말 펠릿**, DC, 성형 370 MPa · 측정 50 MPa, 셀 밀도 n/a).
- 추론 (약함, 인용 금지): **접촉이 거의 없는 소결체와 접촉투성이 냉간 펠릿이 1.3× 안에서 만난다** ⇒ NCM8xx 펠릿의 σ_e 는 접촉저항이 10 배로 깎아 먹은 값이 아니다 ⇒ **"고유 50 ≫ 펠릿 5" 로 50 을 방어할 근거가 이 두 편에는 없다.** (⚠ 재료·공급사·온도·Li 함량(둘 다 합성 직후 = 완전 리튬화 쪽)이 다르고, Ketter 셀 밀도는 모른다 — 방향만.)
- 우리 DEM 접촉망은 입자당 고유 σ 를 넣고 **접촉을 Holm 으로 따로 깎는다** → 넣어야 할 양은 **펠릿값보다 크거나 같은 고유값**이다. STEP3 는 CONTACT_FREE 라 펠릿값을 넣으면 **Ketter 와 같은 lumping 규약**이 된다 (§7-3).
- ★ **Schlautmann 2023 카드 §10-9 의 열린 질문에 대한 유력한 답**: 그 논문 GeoDict 시뮬의 *"CAM 5.2 mS cm⁻¹"*(출처 미기재)는 같은 그룹·같은 LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ 의 이 측정(5.22)일 가능성이 높다 — **추론** (두 논문 어디에도 연결 문장 없음).

### 7-3. 방법 대조 — 이 RN 은 **어느 우리 솔버의 짝인가**

| 축 | Ketter RN | 우리 `network_conductivity.py` (DEM 접촉망) | 우리 STEP3 (`step3_sigma.py` · `voxel_conductivity.py`) |
|---|---|---|---|
| 노드 | voxel 중심 (dx 2 µm) | **입자 중심** | voxel 중심 (dx 0.15–0.4 µm) |
| 링크 | 6 이웃 면 · 반-voxel 직렬(조화평균) | **접촉 쌍** · Holm `R = 1/(2σa)` 직렬 | 6 이웃 면 · 조화평균 |
| 접촉 / 협착 | **없음** (펠릿 입력이 lumping) | **명시** (접촉당 a, Stage-E 소성면적) | **없음** — `CONTACT_FREE` 가지 (CL-81) |
| 이종상 계면항 | **R_int/dx (열만, 2 × 10⁻⁶)** | 없음 | 없음 |
| 기공 | 없음 — 입력 펠릿이 기공을 품음 | 입자 사이 공간 (명시) | pore 셀 (명시) |
| 미세구조 | **합성** 클러스터 삽입 | DEM 압밀 (LIGGGHTS) | MPM 압밀 상 격자 |
| 입자 형상 | 없음 (voxel 덩어리) | 강체구 + overlap 프록시 | MPM 소성 형상 |
| 입력 σ 의 지위 | **순수상 펠릿 유효값** | 고체상 고유값 | 고체상 고유값 (+ VGCF 100 = 분말값 lumping, CL-47) |
| 솔버 | SOR ω 1.979, r < 10⁻⁹ K, 300³ ≤ 5 일 HPC | 희소 선형계 (Kirchhoff) | CG / AMG |
| 채널 | σ_ion · σ_e · κ (같은 코드) | σ_ion · σ_e · κ | σ_ion · σ_e · κ |
| 실험 검증 | **자기 실험** σ 6 점 · κ 6 점 + 문헌 3 건 (+ 실패 1) | Bazzoun 2026 RNM (같은 Holm) | Lee 2025 σ_e 절대 대조 등 |

**판정**: 의뢰 가설 *"우리 `network_conductivity.py` 와 같은 계열"* 은 **절반만 맞다**. 둘 다 Kirchhoff 저항망이지만 **이산화가 voxel-면이고 접촉 물리가 없다** ⇒ 방법의 짝은 **우리 STEP3** 이고, DEM 접촉망의 짝은 여전히 `bazzoun2026_dem_fem_rnm_ionic` 이다.
- ⇒ **frame[4] 교차검증 상대로서의 쓸모 = 모델이 아니라 실험**이다: 무탄소 NCM83–LPSCl 의 σ_ion · σ_e **와 κ** 를 같은 시료 계열에서 잰 **실험 앵커**. 모델(RN)은 우리 STEP3 과 같은 규약이라 **독립 확인이 못 된다** (같은 가정을 공유하면 일치는 증거가 아니다 — CLAUDE.md CDX-16 과 같은 논리).
- **frame[5]**: 이 논문은 **전달 절반만** 소유한다 (σ 삼중항 + 실험). **없는 절반** = 압밀·패킹·접촉망·형상 소성·응력 — 그래서 압력이 모델에 들어갈 길이 없다 (압력은 펠릿 입력값에 숨어 있다).

### 7-4. 같은 인식론 — "잃어버린 물리를 유효 상수에 lumping 한다"
Ketter 의 RN 은 기공·입계·입자간 접촉을 **순수상 펠릿 σ/κ 에 lumping** 한다 — 우리 **DEM E_eff 18× 연화**(frame[2])·**VGCF σ = 100 분말값**(CL-47) 과 **같은 인식론**이다. 그래서 같은 함정도 공유한다: **복합체 속 그 상의 기공·접촉 상태가 순수상 펠릿과 다르면** lumping 이 틀린다. Ketter 자신의 밀도 표가 그 차이를 보인다 — 순수상 공극 12 %·29 % vs 복합체 15.6–25.3 % (§3-3) — 그리고 이온 문턱 근처(60–80 %)에서 RN 이 10–58× 틀린다.

### 7-5. 실험 앵커로 쓸 때의 매핑과 주의
- 조성 환산 [derived(ours), Ketter 밀도 1.86/4.78, 2원계]: AM **70 / 75 / 80 / 82 wt% ↔ φ_NCM 47.6 / 53.9 / 60.9 / 63.9 vol%**. 우리 생산급(82:18 wt%) ≈ **64 vol%** 는 Ketter 60 과 80 % 사이 = **이온 붕괴 구간**이다.
- ⚠ **크기 계층이 우리와 반대**: Ketter LPSCl **~20 µm ≫ NCM83 ~2 µm** · 우리 생산 침대는 SE 가 작고(r_SE ~0.5 µm) AM 이 크다. 고-CAM 에서 큰 SE 는 먼저 끊긴다 ⇒ Ketter 60 % 의 σ_ion **0.0093–0.0108** 을 우리 침대의 기준으로 쓰면 안 된다. 대조: Bazzoun 2026 (SE D50 1.5 µm, CNF 2 + PTFE 0.3 wt%, 400 MPa) 은 CAM 60 vol% 근방(80 wt%)에서 **0.065 mS cm⁻¹** — Ketter 의 약 **6–7×** [derived(ours), 조건 여럿이 다름 — 추세만].
- 압력: 전기 셀 370 MPa 성형 · 50 MPa 측정 · LFA 펠릿 500 MPa 등방 — **우리 300 MPa 와 다르고 셀 밀도가 없다** ⇒ porosity 매핑은 LFA 펠릿(§3-3)만 가능하다.
- 무탄소 · 무바인더 (VGCF 시리즈만 예외) ⇒ 우리 SBE/DBE 첨가제 팔과 직접 비교 불가.

### 7-6. ★ Eq. S3 — STEP3 에 계면저항을 넣는 **출판된 선례** (CL-81 에 주는 것)
`comparison_vs_ours_DEM.md` §B (Islam26 블록)는 *"STEP3 에 계면 저항을 넣으려면 SE–SE 면(face) 컨덕턴스 g = 2σa 형(접촉망과 같은 층위)이 격자-독립적이다"* 라고 적었다. Ketter 의 Eq. S3 `(0.5/κ_a + 0.5/κ_b + R_int/dx)⁻¹` 가 바로 그 **면 직렬 계면항**이고, 실측 복합체 κ 로 한 번 검증까지 됐다 (열, LPSCl|NCM83).
- 가져올 것: **구현 형식** (면마다 시트저항 R_int 를 직렬로 — 격자와 무관한 물리량) · 그 형식이 **작동한다는 증거** (40 % 에서 κ 오차 +10 % → −1 %).
- 가져오면 안 되는 것: **값 2 × 10⁻⁶** — ① 한 데이터셋에 "empirically" 고른 한 값 ② Ketter 격자에서 NCM 입자 = voxel 1 개라 **계면 면적밀도가 dx 로 정해진다** (저자 스스로 60³ 에서 효과가 약하다고 보고) ③ 우리 격자(0.15 µm)에서는 계면이 해상되지만 **계단 근사가 계면 면적을 부풀린다** — 같은 R_int 를 넣어도 효과가 격자에 따라 달라진다. ⇒ 값은 **해상도에 묶인 적합 상수**다.
- 이온 채널로 옮길 때 (GB/접촉 저항): Ketter 는 **전하 채널에 R_int 를 쓰지 않았다** — 그 확장은 이 논문 밖이다.

### 7-7. 우리 리포 안의 Ketter 서술 — 정정 목록 (⛔ **미실행** · `SELF-51` 소관 · 비준 후 작업 브랜치에서)
| 파일 : 줄 (작업 브랜치 @ `766c0405b`) | 지금 | 원문 기준 문제 |
|---|---|---|
| `scripts/network_conductivity.py:132` | `K_SE_THERMAL = 0.7e-2 … LPSCl (Ketter 2025)` | 라벨 오귀속 (0.71 = NCM83) |
| `scripts/step3_sigma.py:1035-1036` | "★SE=문헌앵커(Ketter 2025 = LPSCl/SE 논문) … Ketter 아님[Ketter는 SE]" | 논문 성격 오기 — 두 상·복합체를 모두 잰 복합양극 RN 논문 |
| `scripts/step3_sigma.py:1038-1039, 1052-1054` | "[lit: Ketter 2025 (LPSCl thermal)]" · "NOT Ketter(=LPSCl/SE)" | 같은 오귀속 (webapp prov 문자열로 노출) |
| `scripts/mpm_webapp_payload.py:2580-2581` | "SE=Ketter2025(LPSCl) 문헌앵커, AM=… NOT Ketter" | 같은 오귀속 (payload 설명 문자열) |
| `scripts/audit_transport_cap_equivalence.py:399` | "`K_SE 0.7` (LPSCl, Ketter 2025)" | 같은 오귀속 |
| `docs/thermal_conductivity_derivation.md:298` | "Ketter, F., et al. (2025). Thermal conductivity of LPSCl argyrodite." | **지어진 서지** (이니셜·제목) |
| `GB_correction_fitting_report.md:1070` | 같은 지어진 서지 | 같음 |
| `GB_correction_fitting_report.md:376, 542-551` (§13.1 · §13.8) | "Ketter/Zeier voxel 기반 … 입력 **FIB-SEM**/voxel … Constriction ❌ 불가능" | 입력은 FIB-SEM 이 아니라 **합성 클러스터 구조** · 접촉 협착은 없지만 **이종상 계면항(R_int)은 있다** (열) · (같은 문서 `:880` 의 서지는 올바름) |
| `docs/thermal_conductivity_derivation.md:102` | "k_AM = 4.0, k_SE = 0.7 → AM 이 SE 의 약 5.7 배" | 비 5.7 은 출처 없음 · Ketter 펠릿 비 2.2 |
| (정본 litdb) `wang2025_ai_ecosystems_electrolyte_interface_ssb.md:71, 783` | "✅ `ketter2025_…` 원전 보유" | 09-04 ~ 09-25 동안 가리키던 것은 **초록 뼈대**였다 — 이 카드(같은 slug)로 비로소 참이 됐다 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **SELF-51 κ_SE**: 라벨을 고치고(§0 선택지 A), Böger 2023 PDF 를 확보해 0.66 의 정의를 확인한 뒤 B 로 승격. **치밀 규약을 유지하는 한 값 0.7 을 0.32 로 "바로잡는" 것은 오답** — 규약(치밀 고체상 vs 다공 펠릿)이 다르다. ⚠ 단 σ_grain 3.0 이 펠릿 규약(cronau2021 카드 09-25)이라 **SE 두 입력의 규약 통일(선택지 D)이 먼저**다.
- ② **STEP3 열 채널의 "상한" 라벨에 실험 크기를 붙인다**: ITR 없는 voxel κ 는 이 계에서 **+4 ~ +22 %** 과대 (Ketter §3-3). 우리 κ 절대값을 쓸 때 *"계면열저항 미포함 — 같은 계 voxel RN 기준 +4–22 % 과대 선례(Ketter 2025)"* 를 병기할 수 있다 (⚠ 해상도·조성 다름 — 방향·자릿수만).
- ③ **Phase A (VGCF 조성) 의 무-PTFE 실험 짝**: Ketter `Fig. S4a` — φ_NCM 40 %, LPSCl 20 µm, 무바인더에서 **VGCF 1 → 2 wt% 사이 σ_e 가 ×26 → ×273 (퍼콜레이션 문턱)**, 3 wt% 최대(73.8 mS cm⁻¹) 후 하락, **σ_ion 은 1–3 wt% 에서 −53 ~ −59 %**. 우리 등록 estimand(순서)와는 다른 축이지만, "탄소가 이온을 반으로 깎는다"는 크기는 우리 SE 차단 규약의 외부 참고값이다 (조건 다름 — 크기 전이 금지).
- ④ **σ_AM 50 재검토의 두 번째 원문 앵커**: Wang 2018 (4.1) + Ketter (5.22). 둘 다 50 의 1/10 근방 — DEM 접촉망의 50 은 "출처 없음 + 문헌 두 편보다 10× 위" 로 기록하고, 사용자 판단으로 넘긴다.
- ⑤ **작은 망 비용 교훈**: 조성 시리즈에서 문턱 근처만 틀리는 저해상 망(60³)은 "추세 스크린" 용이고 문턱 판정용이 아니다 — 우리 LEAN/저해상 팔의 쓰임새 규칙과 같다.

## 9. 인용 가능 문장 (deck / paper 용)
- (EN, 열 물성) *"Ketter et al. measured room-temperature thermal conductivities of 0.32 ± 0.02 W m⁻¹ K⁻¹ for a Li₆PS₅Cl pellet (≈88 % dense) and 0.71 ± 0.04 W m⁻¹ K⁻¹ for a LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ pellet (≈71 % dense) by laser-flash analysis, and composite-cathode values below 1 W m⁻¹ K⁻¹ for all compositions (Nat. Commun. 16, 1411, 2025)."*
- (EN, 모델 한계) *"A voxel resistor network fed only with pure-phase pellet conductivities reproduces the composition dependence of σ_ion and σ_e of carbon-free NCM83–LPSCl composites over five orders of magnitude on a logarithmic scale, but overestimates σ_ion by one to two orders of magnitude at ≥ 60 vol% NCM83, near the ionic percolation threshold."*
- (EN, ITR) *"Matching the measured composite thermal conductivity required an LPSCl|NCM83 interfacial thermal resistance of 2 × 10⁻⁶ m² K W⁻¹ in a 2-µm voxel network; we treat it as a resolution-bound fitting value, not a material constant."*
- (EN, 우리 κ_SE — ⚠ Böger 확인 전에는 "assumed" 로만) *"The solid-phase thermal conductivity of Li₆PS₅Cl in our models (0.7 W m⁻¹ K⁻¹) is an assumed dense-phase value close to the 0.66 W m⁻¹ K⁻¹ used for dense Li₆PS₅Cl by Ketter et al. (after Böger et al.); it is not the 0.32 W m⁻¹ K⁻¹ measured by Ketter et al. on a porous pellet."*
- (KR) *"Ketter 등(2025)은 LFA 로 Li₆PS₅Cl 펠릿(상대밀도 ≈ 88 %) 0.32 ± 0.02, NCM83 펠릿(≈ 71 %) 0.71 ± 0.04 W m⁻¹ K⁻¹ 를 쟀고, 복합양극은 조성과 무관하게 1 W m⁻¹ K⁻¹ 미만이었다."*
- (KR) *"순수상 펠릿값만 넣은 voxel 저항망은 무탄소 NCM83–LPSCl 의 σ 조성 의존을 로그 척도로 재현하지만, 이온 문턱 근처(φ_NCM ≥ 60 %)에서 σ_ion 을 10–58 배 과대 예측한다."*

## 10. 주의 / 한계 (over-claim 방지) ★
1. **"good agreement" 는 5 자릿수 로그 축 위의 판정**이다. 선형으로는 σ_ion **60 % 10.7–12.6× · 80 % 47–58×** 과대, σ_e **40 % 2.3–2.5×** 과대, **20 % 0.63–0.67×** 과소. 저자도 φ_NCM > 40 % 의 이온 편차를 문턱 민감도로 돌린다 (p. 4) — **우리 생산 조성(≈ 64 vol%)이 바로 그 구간**이다.
2. **오차막대 ±50 % 는 규약**(단일 측정) — 측정 불확도로 읽지 말 것.
3. **SI p. S16 의 σ_e/σ_ion 뒤바뀜** (§3-2) — 그 문장을 인용하지 말고 SD/`Fig. 3d` 값을 쓴다.
4. **κ 입력은 다공 펠릿값**(공극 12 %·29 %)이고 복합체 펠릿 공극은 15.6–25.3 % — 망에는 기공이 없다. 논문도 "to a certain extent" 로만 방어한다.
5. **C_p ≈ 계산 C_V** — DSC 측정 아님. κ 가 C_V 에 선형이다. 본문 C_V 범위 문장은 ≈ 150–400 K 창 (캡션 창과 다름).
6. **ITR 2 × 10⁻⁶ 은 한 값 · 불확도 없음 · 해상도 의존**이고, 넣어도 60/80 % 가 +10/+18 % 과대로 남는다 — ITR 이 설명한 것은 **일부**.
7. **80 % 복합체 κ(T) 계단 하락** (298 → 323 K 0.499 → 0.424) — 논문 무언급 시료 거동.
8. **VGCF "minor" 이온 영향 = 실제 −53 ~ −88 %** · "<2 wt%"(본문) vs ">2 wt%"(SI) 문구 불일치 · VGCF 는 RN 미모사 · VGCF 고유 σ_e 없음.
9. VGCF 고함량 DC 저항이 **~1–1.7 Ω** (`Fig. S14c` 기울기, derived(ours)) — 셀·스탬프 접촉저항과 같은 자릿수일 수 있어 2–5 wt% σ_e 는 **하한일 가능성** (우리 추론, 논문 미논의). Source Data `FigS14c/d` 는 5 wt% 열을 **"4wt%" 로 중복 표기**했다 (SD 표기 오류).
10. **크기 계층 반전** (LPSCl ~20 µm ≫ NCM83 ~2 µm) · **합성 미세구조** (FIB-SEM·DEM 아님) · 실측 EDX 의 NCM 응집을 RN 이 안 그린다 · **PSD·형상·기공 없음** · 실현 수 n/a.
11. **Rudel Si–LPSCl–C 실패** (7× 과대 · 57× 과소) — "잘 정의된 도메인" 이 없는 복합체에는 쓰지 말 것 (저자 명시).
12. **비용**: 300³ 은 조성 시리즈당 최대 5 일 HPC (SOR) — "high computing power 없이" 라는 초록 문구는 **60³ 판에만** 해당하고, 60³ 은 문턱에서 자릿수로 틀린다.
13. **한 논문 안의 두 LPSCl κ 데이터 불일치**: 같은 밀도 ~88 % 에서 Ketter 0.323 vs Böger 0.440 (0.73×) — 논문 무언급. 치밀 LPSCl κ 는 이 논문 안에서도 0.44–0.66 폭 (§0, derived).
14. **할라이드(Hendriks)·고분자(Froboese) 사례는 우리 계가 아니다** — 방법 일반성의 근거일 뿐 값 전이 금지. Hendriks 60 % 에서도 σ_ion 6.7× 과대.
15. 본문의 "σ_e 10¹ … 10⁻² mS cm⁻¹" 는 자릿수 표기 — 실측 최대는 5.22 (10^0.72).

## 11. 용어 미니-글로서리
- **RN (resistor network) 모델**: 연속 매질을 노드와 저항의 망으로 바꿔 Kirchhoff(정상상태 보존)로 푸는 방법. 여기서는 voxel 중심 = 노드, 면 = 저항 → 유한차분(FD)과 같은 이산식.
- **조화평균 링크 (Eq. S2)**: 두 반-voxel 의 직렬 `(0.5/κ_a + 0.5/κ_b)⁻¹` — 우리 STEP3 의 면 전도도와 같은 규약.
- **R_int / ITR / Kapitza 저항**: 계면에서 생기는 면적당 열저항 (m² K W⁻¹). 완전 계면은 포논 부정합(10⁻⁹–10⁻⁷), 거친 거시 계면은 기공·거칠기로 10⁻⁶–10⁻³.
- **연속상 / 분산상 · s_clust · L_vox**: 기지 상 / 클러스터로 넣는 상 · 클러스터 하나의 voxel 수 · 한 변 voxel 수 (n_tot = L_vox³).
- **SOR (successive over-relaxation)**: 제자리 갱신 반복법에 과완화 계수 ω(1 < ω < 2)를 곱해 수렴을 당긴다. 300³ 에 ω = 1.979.
- **잔차 r (Eq. S7)**: 노드 보존식 불균형의 평균 (K) — 수렴 기준 10⁻⁹ K.
- **이온차단 / 전자차단 셀**: 강철 접점은 이온을 막아 전자 경로만 · LiIn|LPSCl 층은 전자를 막아 이온 경로만 측정.
- **T-type TLM**: 이온 레일(z_ion) · 전자 레일(z_e) · 두 레일 사이 계면(z_int)의 무한 사다리 등가회로 (Siroma; Minnmann 2021).
- **Z_block**: 전자차단 셀에서 직렬로 끼는 LPSCl 층 + LiIn 계면 임피던스 (R + ZARC) — 대칭셀로 따로 재서 뺀다.
- **MIEC 회로**: 혼합 이온-전자 전도체용 단순 회로 (R_ion ∥ R_e + 용량 요소) — TLM 교차검증용.
- **DC 분극**: 일정 전압 계단에서 정상전류를 재 Ohm 법칙으로 총저항을 얻는다 (차단 조건에 따라 한 운반자만).
- **LFA (laser flash analysis) · Cape–Lehmann**: 시료 한 면을 펄스로 데우고 반대면 온도 상승 곡선으로 열확산 D 를 적합 (방사·열손실 보정 모델).
- **C_V vs C_p**: 정적/정압 비열 — 고체 상온에서 차이가 작아 C_p ≈ C_V 로 근사.
- **Yuge 수정 EMT (Eq. S10)**: 단순입방 site 혼합의 유효전도도 근사식 — 코드 검증용 해석 기준.
- **펠릿 유효값 vs 고유값**: 공극·입계·접촉을 품은 시료 전체의 값 vs 치밀 단일상의 값. 모델 규약(무엇을 명시하나)에 맞춰 골라야 한다 — 이 카드 §0 의 핵심.

## 12. 이 카드가 확인하지 못한 것 (n/a)
- 전기 셀의 지름·두께·성형 후 밀도 (본문에 없음) · RN 실현(시드) 수 · ITR 불확도/민감도 · VGCF 고유 σ_e · 치밀 NCM83 κ · **Böger 2023 의 0.66 이 무엇인지** (치밀 외삽? 별도 시료?) · 온라인 게재일 (PDF 메타 2025-02-06 만).
- 코드(DOI `10.17879/16948580876`)와 데이터 datastore(DOI `10.17879/54928371863`)는 **내려받지 않았다** — 이 카드의 수치는 논문 본문·SI·Source Data(MOESM3) 기준.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
