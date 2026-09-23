# Impact of the Solid Electrolyte Particle Size Distribution in Sulfide-Based Solid-State Battery Composites — Schlautmann et al. (*Adv. Energy Mater.* **2023**, 13, 2302309) · 무탄소 NCM811/LPSCl 복합양극 microstructure · 유효 σ_ion/σ_e vs SE 입도 (EIS-TLM + DC + GeoDict)

> slug `schlautmann2023_se_particle_size_composite_transport` · DOI `10.1002/aenm.202302309` · type `exp + GeoDict voxel flux sim (EIS-TLM impedance · DC polarization · SEM-EDS microstructure · no DEM/MPM)` · PDF `55f48983-68._Impact_of_the_Solid_Electrolyte_Particle_Size_Distribution_in_Sulfide-Based_Solid-State_Battery_Composites.pdf` (본문 9 pp) + `ba169fe5-68._Sup_Impact_of_the_Solid_Electrolyte_Particle_Size_Distribution_in_Sulfide-Based_Solid-State_Battery_Composites.pdf` (SI 19 pp — Fig S1–S22 · Table ST1–ST4) · digested `2026-09-23` · status ✅ · OA CC-BY

> elements: Li, P, S, Cl, Ni, Co, Mn, O
> methods: Raman, arrhenius

<!-- 실독 기록 (2026-09-23)
     크로핑 32항목(본문 그림 6 + SI 그림 22 + SI 표 4)을 전부 Read 로 열어 봤다. 안 본 것은 없다.
     도구 크롭 중 4장(fig_S2 · fig_S5 · fig_S7 · fig_S9)이 같은 쪽 앞 캡션의 꼬리 글자를 물고 있어
     원본 래스터 bbox 기준(위 −6 pt)으로 다시 잘랐다. SI 표 4개는 SI 가 "Table ST1–ST4" 로 적어
     도구 캡션 정규식이 못 잡았으므로 같은 렌더 경로(300 dpi · blank_ratio · _shrink)로 손 크롭했다.
     본문은 이 표를 "Table S1" 로 부른다 → 파일명 tab_S1…tab_S4, 이 카드도 Table S1–S4 로 적는다.
     표기 규약: 논문에 적힌 값 = stated · 그림에서만 읽은 값 = figure-read ≈ · 논문에 없는 계산 = 우리 산수.
     쪽 표기: 본문 p. 1–9 = 저널 쪽 "2302309 (n of 9)" · SI p. S1–S18 = SI 인쇄 쪽 번호(PDF 쪽 = 인쇄 +1). -->

## 0. 이 digest 를 읽는 법 — 지금 걸린 질문과 원문 판정

**계기 (2026-09-23)**: 랩 동료의 표가 이 논문을 *"NCM + Li₆PS₅Cl composite, effective electronic
conductivity 0.38–0.40 mS/cm"* 로 적고, 그것으로 *"황화물 복합양극의 σ_e 는 ~0.1–1 mS/cm"* 를 주장한다.
우리 쪽 답은 *"그 밴드는 **탄소 없는** 복합체의 것이고 우리 전극은 VGCF 3 wt% 를 담는다"* 였다.
원문으로 확인한 판정:

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 조성** | NCM811(**LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂**, MSE Supplies, D50 **3.4 µm**) : Li₆PS₅Cl(AMG Lithium, **S/M/L/XL = D50vol 4/11/20/40 µm**) = **70:30 wt%** (Table S1 표기 **52:48 vol%**). **도전 탄소 0 · 바인더 0** — *"The two components were transferred into a 15 mL ZrO₂ cup"* | p. 3 · p. 8 · `Table S1` · `Table S2` |
| **Q2 σ_e** | **0.301 / 0.257 / 0.311 / 0.406 mS cm⁻¹** (S/M/L/XL, AC-TLM, `Table S4`). 본문 p. 6 의 *"0.40 (±0.06) for XL · 0.38 (±0.15) for S"* 가 동료 표의 **0.38–0.40** 이다. ⚠ **S 의 0.38 은 `Fig. 6a`·`Table S4`(0.301) 와 어긋나고 `Fig. S14` 의 DC 값(figure-read ≈ 0.38)과 맞는다.** 측정 = **이온차단(강철‖복합체‖강철) 대칭셀 EIS + "T-type" TLM**, DC 분극으로 교차확인, **25 °C · 스택압 50 MPa · 성형 3 t(3 min)**, 펠릿 두께 **미보고** | p. 6 · p. 8 · `Fig. 5a` · `Fig. 6a` · `Fig. S14` · `Table S4` |
| **Q3 NCM–NCM 전자 계면항** | 모델에 **있다**: `z_el = r_el,bulk + z_el,int`(NCM–NCM 전자 전하이동 = 병렬 R-CPE), **`R_el = L(r_el,bulk + r_el,int)`** (Eq. 2). **분리된 값(벌크 vs 계면 몫)은 본문·SI 어디에도 없다** — 합만 보고한다. 간접 단서만 있다: 접촉저항이 없는 GeoDict voxel 계산 σ_e 가 실측의 **2.54 / 2.98 / 2.04 / 1.06 배**(우리 산수, `Table S4`) — 저자는 그 차를 *"surface effects on the NCM leading to different resistances between NCM particles"* 로 **가정**할 뿐 측정하지 않았다 | p. 4–5 · p. 6 · Eq. 1–2 · `Table S4` |
| **Q4 σ_ion vs SE 입도** | σ_ion,eff **0.254 / 0.199 / 0.153 / 0.165 mS cm⁻¹**, κ_ion,sim **4.70 / 6.65 / 8.56 / 7.50**, C/20 첫 방전 **198 ± 18 / 165 ± 3 / 165 ± 3 / 152 ± 3 mAh g⁻¹**. 순수 LPSCl σ 는 입도와 무관(**2.2 mS cm⁻¹**, L 만 2.8) → 우리 Cronau(r_SE) 인자가 **1.00 인 구간**(r ≥ 0.5 µm)과 정합. ⚠ **우리 생산 r_SE = 0.5 µm(⌀1.0) 는 이 논문 범위 밖**(가장 고운 S 도 D50vol 4 µm) | p. 2 · p. 5 · `Fig. 4` · `Fig. 6a` · `Fig. S15` · `Table S4` |

⇒ **동료 논거에 대한 판정**: *"0.38–0.40 mS cm⁻¹"* 는 원문에 있다. 단 그것은 **탄소도 바인더도 없는
NCM811:LPSCl 70:30 wt% 복합체**(고체 중 CAM 52 vol% — `Table S1` 표기; 같은 표의 밀도로 환산하면 47.7 vol%)를 25 °C 에서 잰 값이다. **VGCF 를 담은 전극의 비교 대상이 아니다.**
정본 litdb 의 탄소 포함 황화물 복합양극 σ_e 는 두 자릿수 위에 있다 — Lee 2025 **33–34 mS cm⁻¹**(VGCF 3 · PTFE 0.5 wt%),
Kim 2024 **38.6 / 54.8 / 65.2 mS cm⁻¹**(carbon 3 wt%, AM 80/85/90 wt%) (§7c). 그리고 **무탄소 밴드조차 보편값이 아니다** —
Minnmann 2021 은 같은 종류 셀에서 CAM 25 → 61 vol% 에 σ_el,eff 가 **~0.021 → ~1 mS cm⁻¹** 로 두 자릿수 움직인다고 보고했다(§7c).

---

## 1. 한 줄 요약

Li₆PS₅Cl 의 입도 분포(D50vol 4/11/20/40 µm)를 바꿔도 **순수 SE 의 σ·결정구조·국소구조는 그대로**인데,
**무탄소 NCM811 복합양극**에서는 작은 SE 가 공극을 줄이고(24.3 → 14.1 %) SE 를 고르게 퍼뜨려 **σ_ion,eff 를 0.165 → 0.254 mS cm⁻¹ 로 올리고
용량·율특성을 개선**한다. 전자 쪽 **σ_el,eff 는 0.26–0.41 mS cm⁻¹ 로 입도에 거의 둔감**한데, **접촉저항 없는 voxel 모델(GeoDict)은
작은 SE 에서 σ_el 이 커진다고 예측**해 실측과 추세부터 어긋난다 — 저자는 NCM–NCM 계면(표면) 저항을 원인으로 **가정**한다.
결론 서사는 *"빠르기만 한 것이 아니라 **균형 잡힌**(σ_ion/σ_el → 1) 전달이 용량을 올린다"* 이다.

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Eva Schlautmann**, Alexander Weiß, Oliver Maus, Lukas Ketter, Moumita Rana, Sebastian Puls, Vera Nickel, Christine Gabbey, Christoph Hartnig, **Anja Bielefeld**, **Wolfgang G. Zeier\*** (Univ. Münster · JLU Giessen · FZ Jülich IEK-12 · **AMG Lithium GmbH**) | *Adv. Energy Mater.* **13**, 2302309 (2023) · 접수 2023-07-19 · 개정 08-23 · 온라인 09-24 | 10.1002/aenm.202302309 | **Li₆PS₅Cl**(AMG, 4 PSD) + **NCM811** = LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂(MSE Supplies), **무탄소·무바인더** 70:30 wt% · 분리막 Li₅.₅PS₄.₅Cl₁.₅ · 대극 In/LiIn | 실험(EIS-TLM · DC 분극 · 반쪽셀) + **GeoDict voxel flux 시뮬** |

- **동기 (p. 1–2)**: 고-로딩 양극은 CAM 이 많아 Li⁺ 경로가 꼬인다(Minnmann 2021, ref 8). 고체 SE 는 작은 공극에 스며들지 못해 **공극이 σ_ion 을 깎는다**(Bielefeld, ref 9–10). 입도 궁합(Rana, ref 11)·CAM 이용률(Shi, ref 12) 연구는 있었지만, *"SE 입도에 따라 공극·균질성·전하 수송이 어떻게 상관되고 그것이 전기화학 성능에 어떻게 이어지는가"* 는 열려 있었다.
- **질문**: SE PSD 만 바꾼 복합양극 4종에서 (i) 순수 SE 자체가 변하는가, (ii) 미세구조(공극·분포)는 어떻게 변하는가, (iii) 유효 σ_ion·σ_el 과 굴곡인자 κ 는, (iv) 용량·율특성은, (v) 시뮬레이션(GeoDict)은 그 추세를 재현하는가.
- **이해관계 (p. 8, stated)**: *"Three authors are employed by the company that provided the samples and performed the particle size distribution analyses."* — PSD 측정과 시료가 공급사(AMG)에서 왔다. **네 PSD 를 어떻게 만들었는지(분쇄·분급 여부)는 적혀 있지 않다.**

## 3. 핵심 수치 총정리 ★

### 3a. 재료

| 항목 | 값 | 표기 | 출처 |
|---|---|---|---|
| CAM | LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ ("NCM811"), MSE Supplies, **250 °C 동적진공 1박 건조**(Büchi B-585). 코팅 언급 없음 | stated | p. 2 · p. 8 |
| CAM 입도 | **D50 3.4 µm** (`Fig. S1` 캡션) · `Table S3`: **µa 4.57 · σa 0.99 · D90num 6.89 · D50num 3.38 · D10num 1.54 µm** (SEM 영상분석 count CDF 의 log-normal 적합) | stated | SI p. S2 · S14 |
| ⚠ CAM 입도 교차 | `Fig. S18a` count CDF 는 **D10 ≈ 3.0 · D50 ≈ 4.7 · D90 ≈ 5.5 µm** 로 읽힌다 — `Table S3` 의 D-값(1.54/3.38/6.89)과 **어긋나고** 같은 표의 µa 4.57 · σa 0.99 와는 맞는다 (§10-5) | figure-read ≈ | SI p. S14 |
| SE | Li₆PS₅Cl (**AMG Lithium 제공**), 4 PSD. 입도 분석 = Sympatec Helos 정적 레이저회절 | stated | p. 2 · p. 7 |
| SE PSD 이름 | **S = D50vol 4 µm · M = 11 · L = 20 · XL = 40 µm** | stated | p. 2 |
| SE PSD 통계 (`Table S2`) | D10vol / D50vol / D90vol = **0.97 / 4 / 9.22** (S) · **2.16 / 11 / 52.71** (M) · **3.76 / 20 / 118.66** (L) · **8.12 / 40 / 133.16** (XL) µm | stated | SI p. S12 |
|  | µa **4.81 / 21.10 / 30.64 / 65.29** µm · σa **4.48 / 37.79 / 44.64 / 100.73** µm · "s" **1.95 / 4.45 / 3.28 / 2.98** ("s / µm" 로 표기, §10-6) | stated | SI p. S12 |
| 조성 | **NCM811 : LPSCl = 70 : 30 wt%** · `Table S1` 부피분율 **52 : 48 vol%** · 밀도 **4.78 / 1.87 g cm⁻³** | stated | p. 3 · p. 8 · SI p. S10 |
| ⚠ vol% 검산 | 같은 표의 밀도로 환산하면 **LPSCl 52.3 · NCM 47.7 vol%** — 표의 48/52 와 **뒤바뀐 방향** (§10-4) | 우리 산수 | — |
| 공극 (`Table S1`) | **S 14.1 · M 18.1 · L 21.4 · XL 24.3 %** (*"calculated as Minnmann et al. reported via density measurements"*) | stated | SI p. S10 |
| **도전재 · 바인더** | **없음.** 복합체 = NCM + LPSCl 두 성분만 (볼밀 혼합) | stated | p. 8 |
| 분리막 SE | Li₅.₅PS₄.₅Cl₁.₅ (자체 고상합성), **8 mS cm⁻¹** | stated | p. 3 · p. 7 |

### 3b. 순수 SE (입도 효과 없음)

| 물성 | 값 | 조건 | 표기 | 출처 |
|---|---|---|---|---|
| σ_total (RT) | **2.2 mS cm⁻¹** (S·M·XL) · **2.8 mS cm⁻¹** (L) | EIS, R-CPE 적합(차단 거동만 보임) | stated | p. 2 · `Fig. 2b` |
| 저자 해석 | 2.8 도 *"within the measurement and sample uncertainty"* · 전부 argyrodite 범위 10⁻³–10⁻² S cm⁻¹ | — | stated | p. 2–3 |
| 활성화 장벽 | *"similar activation barriers"* — **수치 미보고** | 온도가변 EIS | stated | `Fig. S3` |
| Ea (우리 판독) | 기울기 figure-read ≈ −4.6 kK → **Ea ≈ 0.40 eV** (네 시료 겹침). ⚠ 절대 수준은 본문 2.2 와 안 맞는다 (§10-8) | 1000/T 3.2–4.3 K⁻¹ | figure-read ≈ + 우리 산수 | `Fig. S3` |
| XRD | 상순수, 평균구조·격자상수 차이 없음. Rietveld **Rwp 5.9 / 6.7 / 8.1 / 8.3 %**, gof 1.2 / 1.2 / 1.2 / 1.1 (S/M/L/XL) | Cu Kα₁, 캡일러리 | stated (그림 안 인쇄) | `Fig. 2c` · `Fig. S4` |
| PDF (국소구조) | 차이 없음. small-box **Rw 21.6 / 19.7 / 19.9 / 19.1 %** | Ag Kα₁, Qmax 18 Å⁻¹, r 1.5–40 Å 정련 | stated (그림 안 인쇄) | `Fig. 2d` · `Fig. S5` |
| Raman | PS₄³⁻ **427 cm⁻¹** 단일 예리 신호, 네 시료 동일 | — | stated | `Fig. S6` |

### 3c. 반쪽셀 성능 (In/LiIn ‖ Li₅.₅PS₄.₅Cl₁.₅ ‖ 복합양극, 25 °C, 50 MPa, 2.0–3.7 V vs In/LiIn)

| 항목 | S | M | L | XL | 표기 · 출처 |
|---|---|---|---|---|---|
| C/20 첫 충전 (mAh g⁻¹) | **247 ± 24** | **212 ± 4** | **212 ± 4** | **205 ± 4** | stated · p. 4 (M·L 을 하나로 적음) |
| C/20 첫 방전 (mAh g⁻¹) | **198 ± 18** | **165 ± 3** | **165 ± 3** | **152 ± 3** | stated · p. 4 |
| 1C 방전 끝(2.0 V) 용량, 대표 곡선 | ≈105 | ≈90 | ≈63 | ≈45 | figure-read ≈ · `Fig. 4b` |
| 율 시험 1C 단계 (5 사이클 평균대) | ≈100 | ≈89 | ≈70 | ≈53 | figure-read ≈ · `Fig. 4d` |
| 0.1 C 50 사이클: 1 → ~10 → 50 사이클 | ≈179 → 171 → 177 | ≈160 → 150 → 156 | ≈157 → 141 → 143 | ≈151 → 131 → 134 | figure-read ≈ · `Fig. 4c` |
| 첫 사이클 쿨롱효율 (0.1 C) | ≈78 % | ≈77 % | ≈75 % | ≈72–73 % | figure-read ≈ · `Fig. S8e–h` |

- 전류밀도(stated, p. 8): C/20 **0.107** · C/10 **0.214** · C/5 **0.428** · C/2 **1.070** · 1C **2.140 mA cm⁻²**. CAM 로딩 **10.7 mg cm⁻²** (복합체 12 mg / 0.785 cm²).
  ⇒ 1C 기준 = 2.14 / 10.7 = **200 mA g⁻¹** (우리 산수).
- *"No difference can be seen in the capacity retention"* (p. 4) — **절대 용량 차는 그대로, 감쇠 모양만 같다.** 10 사이클 뒤 S·M 의 소폭 상승은 산화분해 산물(phosphate/sulfate 계)의 redox 활성으로 해석 (refs 21–22).
- 1C 곡선의 과전압은 SE 입도가 클수록 증가 (p. 4, `Fig. 4b`).

### 3d. 유효 전달 — `Table S4` 전문 (SI p. S17) ★

| PSD | D50vol (µm) | **σ_ion,eff exp** (mS cm⁻¹) | σ_ion,eff sim | κ_ion,sim | **σ_el,eff exp** (mS cm⁻¹) | σ_el,eff sim | κ_el,sim |
|---|---|---|---|---|---|---|---|
| S | 4 | **0.254** | 0.193 | 4.70 | **0.301** | 0.765 | 3.04 |
| M | 11 | **0.199** | 0.130 | 6.65 | **0.257** | 0.767 | 2.89 |
| L | 20 | **0.153** | 0.097 | 8.56 | **0.311** | 0.635 | 3.35 |
| XL | 40 | **0.165** | 0.107 | 7.50 | **0.406** | 0.431 | 4.75 |

- 본문 요약 (p. 5–6, stated): σ_ion,eff **L·XL 0.16 (±0.03) · S 0.25 (±0.01)**; σ_el,eff **XL 0.40 (±0.06) · S 0.38 (±0.15)**.
- ⚠ **S 의 σ_el 두 값**: `Table S4` **0.301** = `Fig. 6a` 원(figure-read ≈ 0.30, 오차막대 ≈ 0.15–0.45) = `Fig. 6b` x 좌표(0.254/0.301 = **0.84**, 우리 산수). 본문 **0.38** 로 계산하면 비가 **0.67** 이 되어 `Fig. 6b` 의 S 점 위치와 안 맞는다. 본문 0.38 은 `Fig. S14` 의 **DC 사각형**(figure-read ≈ 0.38)과 같다 (§10-1).
- **DC 분극 값** (`Fig. S14`, figure-read ≈): σ_el **0.38 / 0.23 / 0.36 / 0.36** · σ_ion **0.28 / 0.15 / 0.13 / 0.15** (S/M/L/XL). 저자 판정: AC 와 *"No significant difference"*.
- κ 정의 (p. 5, stated): **κ = 부피분율 × 벌크 전도도 / 유효 전도도.** (= Minnmann 2021 의 τ² 와 같은 양)

### 3e. 계면 면적 (CAM–LPSCl 비표면, GeoDict MatDict)

| | S | M | L | XL | 출처 |
|---|---|---|---|---|---|
| 본문 (stated) | **142.7 × 10⁵ m⁻¹** | S 의 1/3.5 | — | **16.5 × 10⁵ m⁻¹** | p. 6 |
| `Fig. S22` 축 "10⁵ m⁻¹" (figure-read ≈) | ≈1.43 | ≈0.38 | ≈0.26 | ≈0.165 | SI p. S17 |

⚠ **두 표기가 100배 다르다.** 비(S/XL ≈ 8.7)는 같다. 물리 상한으로 가르면 **그림 쪽이 맞다** — CAM 전체 표면/부피 = 6φ/d ≈ **5.9 × 10⁵ m⁻¹**(S, φ_CAM 0.447, d 4.57 µm; 우리 산수)인데 본문 값 1.43 × 10⁷ m⁻¹ 은 그 **24배**라 불가능 (§10-7).

### 3f. 우리 산수 (논문 미보고 — 입력은 전부 stated 값)

| 양 | S | M | L | XL | 식 / 입력 |
|---|---|---|---|---|---|
| φ_SE (전체 부피 중) | 0.412 | 0.393 | 0.377 | 0.363 | 0.48 × (1 − 공극) · `Table S1` |
| φ_CAM (전체 부피 중) | 0.447 | 0.426 | 0.409 | 0.394 | 0.52 × (1 − 공극) |
| κ_ion,sim 재계산 | 4.70 | 6.65 | 8.56 | 7.47 | φ_SE × 2.2 / σ_ion,sim → `Table S4` 와 일치(XL 7.50 은 반올림차) ⇒ **모델은 48/52 vol% 를 썼다** |
| κ_el,sim 재계산 | 3.04 | 2.89 | 3.35 | 4.75 | φ_CAM × 5.2 / σ_el,sim → `Table S4` 와 **정확히 일치** |
| κ_ion,obs | 3.57 | 4.35 | 5.42 | 4.84 | φ_SE × 2.2 / σ_ion,exp (= `Fig. S15a` 원) |
| κ_el,obs | 7.72 | 8.62 | 6.83 | 5.04 | φ_CAM × 5.2 / σ_el,exp (= `Fig. S15b` 원) |
| σ_el sim/exp | **2.54** | **2.98** | **2.04** | **1.06** | `Table S4` |
| σ_ion sim/exp | 0.76 | 0.65 | 0.63 | 0.65 | `Table S4` |
| σ_ion/σ_el (exp) | 0.844 | 0.774 | 0.492 | 0.406 | `Table S4` (= `Fig. 6b` x 축) |
| 복합체 σ_ion 감소 (벌크 2.2 대비) | 8.7× | 11.1× | 14.4× | 13.3× | 2.2 / σ_ion,exp |
| 성형압 | 3 t / 0.785 cm² ≈ **375 MPa** (셀 전부 공통) | | | | 3000 × 9.81 N / 0.785 cm² |
| 대칭셀 펠릿 두께 추정 | ≈455 µm | ≈477 | ≈497 | ≈516 | 100 mg · 밀도·공극 `Table S1` 가정 — **논문은 두께 미보고** |
| → 함의 R_el (σ_el,exp 로) | ≈193 Ω | ≈237 | ≈204 | ≈162 | L/(σA) — `Fig. S10` 스펙트럼 끝(≈105–245 Ω)과 같은 자릿수 = **검산용**일 뿐 |

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 합성 (p. 7)
- **Li₆PS₅Cl**: AMG Lithium 제공 (합성·입도 제어 방법 미기재).
- **Li₅.₅PS₄.₅Cl₁.₅** (분리막): LiCl(Alfa, 99 %) 손분쇄 15 min → Li₂S(Alfa, 99.99 %)·P₂S₅(Sigma) 추가 15 min → 펠릿 → **탄소코팅 석영앰플 진공봉입** → **450 °C 72 h**(100 °C h⁻¹ 승온, 자연냉각) → 재분쇄·재펠릿 → 같은 열처리 한 번 더. 전 과정 O₂ < 0.1 ppm · H₂O < 0.5 ppm.

### 4b. 복합양극 (p. 8)
- NCM811(건조) + LPSCl = **70 : 30 wt%**, 15 mL ZrO₂ 컵 + 3 mm ZrO₂ 볼, **Fritsch pulverisette 23 Mini Mill 15 Hz · 15 min**.
- **도전재·바인더 없음** (*"The two components were transferred…"*).

### 4c. 셀 (p. 8)
- PEEK 라이닝 기밀 프레스셀, **스테인리스 스탬프 = 집전체, 면적 0.785 cm²**(⌀10 mm).
- 반쪽셀: 분리막 60 mg 손프레스 → 복합체 **12 mg**(CAM **10.7 mg cm⁻²**) → **일축 3 t · 3 min** → In 포일(100 µm, ⌀9 mm) + Li 1.5 mg → 금속 프레임 **50 MPa** → 25 °C **6 h** 평형.

### 4d. 전기화학 (p. 8)
- 장기: MACCOR, 25 °C, **2.0–3.7 V vs In/LiIn**, 0.1 C × 50 사이클. 율: Biologic VMP300, C/20 → 1C (3c 의 전류밀도). **삼중 반복**(`Fig. S8`, `Fig. S9`).

### 4e. 유효 전달 측정 — 이온·전자 **분리 측정** ★ (p. 4–5, p. 8)

| | **이온차단 대칭셀** → σ_el,eff | **전자차단 대칭셀** → σ_ion,eff |
|---|---|---|
| 구성 | **강철 ‖ 복합체 100 mg ‖ 강철** | In/Li ‖ Li₅.₅PS₄.₅Cl₁.₅ 80 mg ‖ 복합체 100 mg ‖ Li₅.₅PS₄.₅Cl₁.₅ 80 mg ‖ In/Li |
| 성형 · 압력 | 3 t · 3 min → 50 MPa, 25 °C 6 h | 같음 |
| EIS | 25 °C, VMP300, **10 mV, 10 mHz–7 MHz** | 같음 |
| DC 분극 | 본문: *"45 to 50 mV … in 5 mV steps"*, **2 h/step** (⚠ `Fig. S12` 는 ±5 → ±45 mV 교대로 보인다, §10-10) | **0.5 → 5 mV, 0.5 mV step, 5 h/step** |
| 적합 | **"T-type" TLM**, RelaxIS 3 | 같은 TLM + 분리막 R + (R∥CPE: SE‖In/LiIn 계면) 직렬 |

**TLM 식 (Eq. 1, p. 4 — 원문 그대로 옮김)**:

`Z_CC(ω) = [z_ion·z_el / (z_ion + z_el)]·L + [2·z_el²·√z_int / (z_ion + z_el)^(3/2)] × [cosh(L·√((z_ion+z_el)/z_int)) − 1] / sinh(L·√((z_ion+z_el)/z_int))`

- **z_el** = 전자 레일 = **r_el(벌크 저항) + z_el,int(NCM 입자 간 전자 계면 임피던스 — *"electronic charge transfer across the NCM–NCM interface"*, 병렬 R-CPE)** (p. 4–5, Minnmann 2021 을 따름)
- **z_ion** = 이온 레일 = **저항 r_ion 만** (황화물이 빨라 CPE 불필요 — p. 5, ref 7)
- **z_int** = 두 상 사이 **CPE_int** (대칭셀이라 전하이동 없음 = non-faradaic)
- **Eq. 2**: **`R_el = L·(r_el,bulk + r_el,int)`** · **Eq. 3**: `R_ion = L·r_ion` → σ = L/(R·A).
- ★ **우리 검산 (논문에 없음)**: ω → 0 에서 z_int → ∞ 이면 Eq. 1 → **`Z(0) = L·z_el(0) = L(r_el,bulk + r_el,int) = R_el`** (이온 레일은 강철에서 막힘).
  ω → ∞ 에서 → `L·(z_ion ∥ z_el,HF)`. ⇒ **DC 값에는 NCM–NCM 계면항이 반드시 들어 있다** — 그래서 `Fig. S14` 의 AC ≈ DC 는
  "TLM 전자 레일(계면 포함) = 관통 전자 전도" 의 실측 확인이다. **계면항을 뺀 r_el,bulk 만 쓰면 σ_el 을 과대평가**한다 (§7b).

### 4f. 구조 분석 (p. 7–8)
- XRD: STOE StadiP, Debye–Scherrer, Cu Kα₁(본문 인쇄값 *"1.545051 Å"* — §10-11), 0.5 mm 캡일러리, 2θ 10–70°, step 0.1, 15 s/step.
- PDF: STOE StadiP, **Ag Kα₁ 0.55941 Å**, Ge(111), MYTHEN2 1K × 4, Q 0.8–20.5 Å⁻¹, **24 h**, PDFgetX3(Qmax 18 Å⁻¹), **TOPAS Academic V7 small-box**(스케일·상관운동·격자상수·원자위치·등방 ADP 순차 정련, r 1.5–40 Å).
- SEM/EDS: Zeiss AURIGA CrossBeam 3 kV(in-lens), EDS X-Max 80 mm² 15 kV, 금 코팅, 탄소테이프 고정. ⚠ **관찰면 서술이 두 가지다** — 본문 p. 3 은 *"cross-sections … of the pressed composites"*, 실험절 p. 7 은 *"the surface of the pressed composites"*. 단면 제작법(FIB·연마 등)은 **미기재**.

### 4g. 미세구조 모델링 · 전달 시뮬레이션 ★ (p. 8 · SI p. S10–S16)

- **코드**: **GeoDict** (Math2market) — GrainGeo(입자 배치) · ProcessGeo(정리 "Cleanse") · **ConductoDict(전도 flux 풀이)** · MatDict(표면적). 하드웨어 Dell Precision 3650 (96 GB, i7-11700).
- **DEM/MPM/FEM 없음.** 압밀 역학이 **없다** — 입자를 **무작위 배치한 뒤 겹침만 줄인다**. 공극률은 **실측 밀도에서 가져와 입력**한다(예측 아님).
- **도메인**: M/L/XL = **(300 µm)³ @ 600 nm/voxel** (= 500³ ≈ 1.25 × 10⁸ voxel, 우리 산수) · S = **(90 µm)³ @ 300 nm/voxel** (= 300³ ≈ 2.7 × 10⁷). 조성당 **독립 구조 3개** 평균.
- **flux 계산**: 전위차 **1 V**(S 만 **0.3 V** — 모델 크기 차에 맞춘 전류밀도 스케일, `Fig. S21` 캡션). 벌크 전도도 **LPSCl 2.2 · CAM 5.2 mS cm⁻¹**(⚠ 5.2 의 출처 미기재, §10-9). **이온 전류는 SE 로만, 전자 전류는 CAM 으로만.**
- **입자 처리 ★ (우리 "무질서 처리" 칸)**:
  - **형상**: SE = **볼록 다면체**(`Fig. S19` 에서 보임). CAM = **구**(M/L/XL — 다면체는 생성이 너무 오래 걸려서) · **볼록 다면체**(S — SE 와 크기가 비슷해 실형상이 필요해서) (SI p. S14).
  - **PSD**: SE = 실측 부피 CDF 의 log-normal 적합(scipy `curve_fit`, 첫 점 제외) → **폭을 산술 σa 대신 "span" s 로 대체**하고 D10vol–D90vol 에서 **절단**(안 그러면 ~160 µm 입자 생성). CAM = count CDF 적합, 산술 σa 사용, 절단 없음.
  - **겹침**: 무작위 배치 → **겹침을 3 % 까지 최소화**하면 멈춤. CAM–SE 겹침은 **CAM 에 배정**(CAM E = **194 GPa**, ref 31) → SE 속에 CAM 잔조각이 생기면 "Cleanse" 로 제거(**1000 voxel 미만** 고립 CAM 은 SE 로 재배정).
  - ⇒ **강체·기하 규칙뿐.** 접촉 법칙(Hertz/소성) 없음, **형상 소성 없음** — SE 가 CAM 을 감싸는 모양은 **겹침 영역을 CAM 쪽으로 빼는 기하 연산**이지 유동이 아니다.
  - **접촉 저항 없음**: 같은 상의 voxel 끼리는 벌크로 이어진다 = 우리 STEP3 가 앉은 **`CONTACT_FREE` 가지와 같은 층위** (§7b · CL-81).
- **κ 산출**: κ = φ·σ₀/σ_eff (φ 는 모델 상분율). **비표면적**: MatDict "Surface Area" / 전체 모델 부피 = CAM–LPSCl 활성계면.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 순수 Li₆PS₅Cl — 입도가 달라도 재료는 같다 (`Fig. 2`, `Fig. S2`–`S6`)
- `Fig. 2a` (부피 누적분포, 로그 x): S 는 ~15 µm 에서 100 % 에 닿고 M·L·XL 은 오른쪽으로 벌어진다. **첫 측정점(1–1.5 µm)이 이미 S ≈ 12 % · M ≈ 24 % · L ≈ 12 % · XL ≈ 4 %** (figure-read ≈) — **큰 PSD 에도 미세분이 부피로 상당히 섞여 있다**(M 은 5 µm 이하가 ~29 %). SI 도 *"among the larger (characteristic) D50vol-sized particles a substantial number of small particles are present"* 라 적는다 (SI p. S11).
- `Fig. S16b` (count CDF): **S 의 개수 중앙값 ≈ 0.16 µm**, M·L·XL 은 셋이 거의 겹쳐 **≈ 2.7 µm** (figure-read ≈). ⇒ 개수로 보면 S 는 **서브-µm 미세분이 지배**한다. 저자는 count CDF 가 큰 입자를 과소대표한다며 **부피 CDF 를 모델 입력으로 택했다**.
- `Fig. 2b`: 차단 스파이크만 보이는 Nyquist(Z′ 절편 ≈ 95–100 Ω, figure-read) → R-CPE 적합 → **2.2 mS cm⁻¹**(L 2.8).
- `Fig. 2c`/`Fig. S4`(XRD Rietveld), `Fig. 2d`/`Fig. S5`(PDF 1.5–20 Å 표시), `Fig. S6`(Raman): **네 PSD 가 구별되지 않는다.**
- `Fig. S2` (SEM): S 는 수 µm 조각의 응집체, XL 은 20–40 µm 급 판상·각진 입자 표면에 미세 조각이 붙어 있다 — 부피 PSD 의 넓은 꼬리와 일치.

### 5.2 복합체 미세구조 — 작은 SE 가 고르게 퍼지고 공극이 준다 (`Fig. 1`, `Fig. 3`, `Fig. S7`, `Fig. S19`, `Fig. S20`, `Table S1`)
- `Fig. 3a`·`Fig. S7` (SEM-EDS 가색: NCM 보라, LPSCl 노랑): S 는 노란 SE 가 잘게 흩어져 있고, L·XL 은 **수십 µm 급 노란 섬**이 보인다. 2 µm 배율(`Fig. S7a1–d1`)에서 NCM 입자는 1–3 µm 1차 입자의 응집으로 보인다.
- `Fig. 3b`·`Fig. S20` (모델 단면: LPSCl 청록, NCM 황토): 모델도 같은 방향. ⚠ **L·XL 모델의 SE 섬은 SEM-EDS 섬보다 눈에 띄게 크다**(모델 ~30–70 µm vs SEM 노란 영역 ~10–30 µm, figure-read ≈) — §10-6 의 PSD 입력 문제와 같은 방향.
- `Table S1`: 공극 **14.1 → 18.1 → 21.4 → 24.3 %** (S → XL). *"Despite the same composition in terms of weight fraction, the overall volume occupied by Li6PS5Cl is larger"* (p. 5) — 즉 **σ_ion 이득의 일부는 SE 부피분율(φ_SE 0.412 vs 0.363, 우리 산수) 자체**다.
- `Fig. S19`: L 모델 생성 4단계 — 무작위 LPSCl(다면체) → 무작위 NCM811 → 잔여 NCM 이 SE 속에 박힌 복합체 → "Cleansed" 복합체.

### 5.3 셀 성능 — 작은 SE 가 용량·율특성에서 이긴다 (`Fig. 4`, `Fig. S8`, `Fig. S9`)
- `Fig. 4a` (C/20): 충방전 곡선 모양은 같고 S 가 가장 길다(충전 ≈ 245, 방전 ≈ 195 mAh g⁻¹ 대표곡선).
- `Fig. 4b` (1C): **방전 곡선 모양 자체가 입도에 따라 변한다** — S 는 3.0 V 부근 평탄부가 남고 XL 은 곧바로 기운다. 과전압 = 입도↑.
- `Fig. 4c` (0.1 C 50 사이클, 평균 ± 표준편차 음영): 네 곡선이 **평행**. S 의 음영이 가장 넓다(≈160–190).
- `Fig. 4d` (율): C/20 → 1C 에서 **S ≈ 186→100, XL ≈ 155→53** (figure-read ≈), C/20 복귀 시 대부분 회복.
- `Fig. S8`: **S 는 셀 1 과 셀 2·3 이 ≈ 15 mAh g⁻¹ 벌어진다** — S 의 큰 ± 는 셀 간 차다. 첫 사이클 CE 는 입도↑ 에 따라 **≈ 78 → 72 %** 로 준다(figure-read ≈).
- `Fig. S9`: 율 삼중반복. XL 패널만 y축이 0–200 으로 다르다.

### 5.4 TLM 분석 — 두 대칭셀, 두 레일 (`Fig. 5`, `Fig. S10`, `Fig. S11`)
- `Fig. 5a` (이온차단, 강철‖복합체‖강철): Nyquist 에 **호 두 개**, 실축 끝 ≈ 160–215 Ω (figure-read ≈). 회로도: 위 레일 = 파란 [R + (R∥CPE)] 반복(전자), 아래 = 노란 R(이온), 가로대 = CPE.
- `Fig. 5b` (전자차단): 레일 역할이 바뀌고 양끝에 Z_SE(분리막 R) + Z_In/LiIn|SE(R∥CPE)가 붙는다. 실축 끝 ≈ 220–440 Ω (figure-read ≈), **S 가 가장 짧다**.
- `Fig. S10` 삼중반복(이온차단) 실축 끝: **S ≈ 106 / 170 / 210 Ω** · M ≈ 214 / 236 / 246 · L ≈ 115 / 150 / 181 · XL ≈ 121 / 163 / 168 (figure-read ≈). **S 의 셀 간 2배 차**가 σ_el(S) ± 0.15 의 정체다 — 캡션: *"slightly changing processing mechanics … stickier haptics of the smaller particles"*.
- ⚠ 두 호 중 어느 것이 NCM–NCM 계면(z_el,int)인지 **논문은 배정하지 않는다** (§6 Q3).
- 본문 p. 4 의 *"The resulting Nyquist plots … are shown in Figure 4"* 는 **Figure 5 의 오기**다.

### 5.5 이온 전달 — 작은 SE 가 σ_ion,eff 를 올린다 (`Fig. 6a` 위, `Fig. 6c`, `Fig. S15a`)
- 실측 **0.254 (S) → 0.199 (M) → 0.153 (L) ≈ 0.165 (XL)**; L 과 XL 은 오차 안에서 같다.
- 시뮬 **0.193 / 0.130 / 0.097 / 0.107** — **추세는 같고 절대값은 실측의 0.63–0.76배** (우리 산수).
- `Fig. 6c`: 국소 이온 전류밀도 0–100 mA cm⁻² — S 는 전 부피에 고르게 퍼지고 XL 은 **몇 개의 점접촉에 몰린다**(*"bottlenecks"*, p. 6).
- κ_ion: 시뮬 4.70 → 8.56 (L) · 관측 3.57 → 5.42 (L) — 작은 SE 에서 **감소**(`Fig. S15a`).

### 5.6 전자 전달 — 실측은 둔감, 시뮬은 반대 추세 (`Fig. 6a` 아래, `Fig. S15b`, `Fig. S21`)
- 실측 **0.301 / 0.257 / 0.311 / 0.406** — 오차막대(S ±0.15, L ≈ ±0.11)를 감안하면 **거의 평평**, 굳이 보면 XL 이 가장 높다.
- 시뮬 **0.765 / 0.767 / 0.635 / 0.431** — **작은 SE 일수록 높다**(`Fig. S21`: 0–220 mA cm⁻² 지도에서 S·M 이 고르게 초록).
- Minnmann 2021 은 **작은 SE 에서 σ_el 이 줄었다**고 봤다(p. 6). 이 논문 실측은 그렇지도 않다.
- 저자 설명 (p. 6, 원문): *"It is unclear why this effect is not evident in the experiment. At this stage, we assume this to stem from **surface effects on the NCM leading to different resistances between NCM particles** as any changes due to cycling-based decomposition or contact losses can be ruled out for these symmetric cells."* ⇒ **가설이고 측정 아님.**
- κ_el,sim 3.04 / 2.89 / 3.35 / 4.75 (`Table S4`) · κ_el,obs 7.72 / 8.62 / 6.83 / 5.04 (우리 산수). ⚠ `Fig. S15b` 의 "simulated" 삼각형은 κ_ion,sim 과 **같은 값**을 그렸다 (§10-3).

### 5.7 "균형 전달" — 용량 vs σ_ion/σ_el (`Fig. 6b`)
- x = σ_ion/σ_el(실측) **0.41 (XL) · 0.49 (L) · 0.77 (M) · 0.84 (S)**, y = 용량. C/20 ≈ **151 / 158 / 164 / 181** · 1C ≈ **54 / 70 / 83 / 100** mAh g⁻¹ (figure-read ≈).
- 저자 결론: *"not only fast charge transport but also balanced charge transport is essential"* (ref 26, Hendriks LiMn₂O₄/Li₃InCl₆ 선례).
- ⚠ 4점이고 **입도·공극·계면면적·비가 전부 같이 움직인다** — 비의 인과를 분리한 실험이 아니다 (§10-12). 캡션은 *"initial charge capacity"* 라 적는데 C/20 값(≈151–181)은 첫 충전값(205–247)이 아니라 방전 쪽 크기다.

### 5.8 계면 면적 (`Fig. S22`)
- S 가 압도적(≈1.43), M ≈0.38, L ≈0.26, XL ≈0.165 × 10⁵ m⁻¹ (figure-read ≈; 본문 지수 오기 §10-7). 작은 SE = 더 많은 CAM–SE 접촉 = 더 많은 활성계면 → 용량의 두 번째 기전으로 제시.

### 5.9 결론 (p. 6–7, stated)
1. 연구 범위에서 PSD 는 **순수 LPSCl 의 σ 와 구조에 영향이 없다**.
2. 복합양극에서는 작은 LPSCl → **높은 용량·나은 율특성**.
3. 작은 LPSCl → 큰 접촉계면 · 고른 분포 → **균일한 이온 전류, 작은 공극, 큰 SE 부피분율 → 높은 σ_ion,eff · 낮은 κ_ion**.
4. **빠르고 균형 잡힌** 전자·이온 수송이 핵심 — CAM·첨가제·catholyte 를 바꿀 때마다 입도·수송 파라미터를 다시 맞춰야 한다.

---

## 6. 우선 질문 Q1–Q4 — 원문 대조 (stated 와 우리 산수를 갈라서)

### Q1. 조성 — 탄소가 있나?
- **CAM (stated)**: LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂, MSE Supplies, **D50 = 3.4 µm** (p. 2, `Fig. S1`; `Table S3` D50num 3.38 · D10num 1.54 · D90num 6.89 · µa 4.57 · σa 0.99 µm). 단결정/다결정 여부 **미기재** — SEM(`Fig. S1`, `Fig. S18b`)은 서브-µm~µm 1차 입자의 응집체로 보인다(figure-read, 판정 아님).
- **SE (stated)**: Li₆PS₅Cl(AMG) 4종 — D10vol/D50vol/D90vol = 0.97/4/9.22 · 2.16/11/52.71 · 3.76/20/118.66 · 8.12/40/133.16 µm (`Table S2`).
- **비율 (stated)**: **70 : 30 wt%** (p. 3 · p. 8), `Table S1` 에 **52 : 48 vol%**(NCM : LPSCl). ⚠ 같은 표의 밀도(4.78/1.87)로는 **47.7 : 52.3** (우리 산수) — 표의 vol% 가 뒤바뀐 방향이지만 **모델은 48/52 를 썼다**(κ 재계산이 `Table S4` 와 정확히 일치).
- **탄소 (stated, p. 8)**: *"Cathode composites were prepared by mixing lithium nickel cobalt manganese oxide … and the respective Li6PS5Cl … in a weight ratio of 70:30. **The two components** were transferred into a 15 mL ZrO₂ cup…"* ⇒ **도전 탄소·바인더 없음.** 논문에 나오는 "carbon" 은 합성 앰플의 탄소코팅(p. 7)과 SEM 탄소테이프(p. 7)뿐이다. **전도도를 잰 모든 시료(대칭셀 100 mg)가 이 무탄소 복합체다.**

### Q2. 전자전도도 — 값·시료·방법
- **값 (stated, `Table S4`, SI p. S17)**: σ_el,eff,exp **S 0.301 · M 0.257 · L 0.311 · XL 0.406 mS cm⁻¹**. 시뮬 0.765 / 0.767 / 0.635 / 0.431.
- **본문 (stated, p. 6)**: *"with 0.40 mS cm⁻¹ (±0.06 mS cm⁻¹) for the composite XL and 0.38 mS cm⁻¹ (±0.15 mS cm⁻¹) for the composite S, in Figure 6a."* ⇐ **동료 표의 "0.38–0.40" 은 이 문장이다** — 네 PSD 중 양 끝 둘(S, XL).
- **불일치**: S = 0.38 은 `Fig. 6a`(≈0.30)·`Table S4`(0.301)·`Fig. 6b` 위치(비 0.84)와 **셋 다 어긋나고**, `Fig. S14` 의 **DC** 사각형(≈0.38, figure-read)과 맞는다. ⇒ 본문 문장은 **S 의 DC 값과 XL 의 AC 값을 한 문장에 섞은** 것으로 보인다(우리 판단). 어느 쪽을 쓰든 **0.26–0.41 mS cm⁻¹ 밴드**는 변하지 않는다.
- **방법 (stated, p. 4–5, p. 8)**: 이온차단 대칭셀(**강철 스탬프 양쪽**, 복합체 100 mg), 3 t · 3 min 성형(≈375 MPa, 우리 산수) → 금속 프레임 **50 MPa** → 25 °C 6 h. **EIS 25 °C · 10 mV · 10 mHz–7 MHz** 를 **"T-type" TLM**(Eq. 1–2, RelaxIS 3)으로 적합 → R_el → σ = L/(R·A). 이어서 **DC 분극**(2 h/step)으로 교차확인 → `Fig. S14` *"No significant difference"*. 삼중반복(`Fig. S10`).
- **두께**: **미보고.** 100 mg · `Table S1` 밀도·공극으로 추정하면 ≈ 455–516 µm (우리 산수, 같은 셀 형식의 Minnmann 2021 은 470 µm 를 보고했다).
- **온도**: 25 °C. **압력**: 측정 중 50 MPa (성형 3 t).

### Q3. NCM–NCM 전자 계면 임피던스 — 숫자가 있나?
- **모델 (stated)**: *"The electronic impedance z_el is represented by the electronic bulk resistance r_el and an in-series connected electronic interfacial impedance z_el,int of the NCM particles, as previously reported by Minnmann et al. This electronic interfacial impedance is based on the electronic charge transfer across the NCM–NCM interface and is represented by a parallel R-CPE unit."* (p. 4–5). 유효 저항은 **합** `R_el = L(r_el,bulk + r_el,int)` (Eq. 2).
- **분리 방법 (원리)**: TLM 적합에서 r_el,bulk(순저항)과 z_el,int(R∥CPE)는 **주파수 응답이 달라** 원리상 갈린다 — 고주파 절편은 `L·(r_ion ∥ r_el,bulk)`, 저주파 끝은 `L(r_el,bulk + r_el,int)` (우리 검산, §4e).
- **보고된 값**: **없다.** 본문·SI 어디에도 r_el,bulk, r_el,int, R-CPE 파라미터, 계면 몫(%)이 없다. `Fig. 5a`·`Fig. S10` 은 적합 곡선만 보여 준다. DC 분극(`Fig. S12`)은 원리상 합만 준다.
- **간접 단서 (우리 산수 — 조건부)**: 접촉저항이 **없는** GeoDict 가 σ_el 을 실측의 **2.54 (S) · 2.98 (M) · 2.04 (L) · 1.06 (XL)** 배로 준다. **그 차를 전부 NCM–NCM 계면에 돌리면** 계면 몫 = 1 − exp/sim = **61 · 66 · 51 · 6 %**.
  ⚠ 이 추정은 두 조건에 묶인다 — (i) 시뮬 σ_el 은 **CAM 벌크 5.2 mS cm⁻¹ 에 선형 비례**하는데 그 값의 **출처가 없다**(모든 PSD 를 맞추려면 1.7–4.9 mS cm⁻¹ 가 필요 — 한 값으로 네 점이 안 맞는다), (ii) 같은 모델이 **이온 채널에서는 실측보다 낮게** 나온다(0.63–0.76×) — 모델 미세구조 자체가 실측과 다르다는 뜻이다.
  ⇒ **확실한 것은 크기가 아니라 추세의 불일치**다: 시뮬은 SE 가 작을수록 σ_el↑, 실측은 평평. 저자는 이것을 NCM 표면효과로 **가정**만 했다.
- **우리에게 의미 (§7b)**: 이 항 = CL-81 이 이름 붙인 **복셀 모델에 없는 접촉 항**의 전자판이다.

### Q4. 이온 수송 vs SE 입도 — 우리 Cronau(r_SE)·생산 r_SE 와
- **실측 (stated, `Table S4`)**: σ_ion,eff **0.254 / 0.199 / 0.153 / 0.165 mS cm⁻¹** (S/M/L/XL). 본문: S 0.25 ± 0.01, L·XL 0.16 ± 0.03.
- **굴곡인자**: κ_ion,sim **4.70 / 6.65 / 8.56 / 7.50** (stated) · κ_ion,obs **3.57 / 4.35 / 5.42 / 4.84** (우리 산수 = `Fig. S15a` 원).
- **셀 성능**: 3c 표 (C/20 첫 방전 198/165/165/152 · 1C ≈100/89/70/53 figure-read ≈).
- **Cronau(r_SE) 대조** (우리 σ_ion 폼, CLAUDE.md): Cronau 인자 = **1.00 (r ≥ 0.5 µm)** · 0.90 (0.3–0.5) · 0.65 (0.1–0.3) · → 0.33 (≤ 30 nm). 이 논문의 순수 SE σ 는 **D50vol 4 → 40 µm 에서 평평**(2.2; L 2.8) + XRD·PDF·Raman 불변 ⇒ **"r ≥ 0.5 µm 에서 인자 1"** 과 정합.
  ⚠ 그러나 **Cronau 의 감소 구간(서브-µm)을 검정하지 않는다** — 가장 고운 S 도 D50vol 4 µm(r ≈ 2 µm), D10vol 0.97 µm(r ≈ 0.5 µm)이다. S 의 **개수** 중앙값은 ≈ 0.16 µm(figure-read)지만 그 미세분은 부피가 작아 펠릿 σ 를 좌우하지 못한다. 게다가 네 PSD 의 **제조법(볼밀 여부)이 미기재** — Cronau 의 감소는 볼밀 분말의 비정질화 효과다.
- **우리 생산 r_SE = 0.5 µm (⌀1.0)**: 이 논문의 S 보다 **지름 4배 미세** → **범위 밖**. 이 논문은 "더 고운 쪽으로 갈수록 좋다" 의 **방향**만 준다. ⌀1 µm 에서 복합체 σ_ion 이 계속 오르는지·Cronau 절삭이 이기는지는 **이 데이터로 판정 불가**.
- **우리 폼과 기전 대응**: 이 논문의 이득은 **σ_grain 이 아니라 미세구조**(공극↓ → φ_SE↑, 분포 균질 → 경로 짧아짐)에서 온다 = 우리 폼에서 **(φ_eff)^½ · CN² · cov^½ · f_p³ · C(τ)** 가 담는 쪽. CLAUDE.md 의 *"size effect is PACKING, not overlap"* 와 **같은 방향** (Bazzoun 2026 · Minnmann 2021 에 이어 세 번째 독립 실측).

---

## 7. 우리 DEM+MPM 대비 ★ (근거 = 작업 브랜치 CLAUDE.md 2026-09-23 · 원장 `docs/reviews/claims.json` — ⚠ 정본 `our_dem_baseline.md` 는 값 없는 자리표시다)

⛔ **이 절은 우리 모델의 σ_e 절대값과 SBE/DBE·SDCP 이득 비·퍼센트를 적지 않는다** (여러 개가 `quotation_ban` 등록 대상). 필요한 곳은 원장 ID 로만 가리킨다.

### 7a. 항목별 대조

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 소재 | NCM811(Ni₀.₈₃) + Li₆PS₅Cl, **무탄소·무바인더** 70:30 wt% | NCM811 + Li₆PS₅Cl + **VGCF** + PTFE (+SDCP) | SE·CAM 화학은 같다. **탄소망 유무가 σ_e 를 가르는 1차 변수** → σ_e 밴드 전이 불가 |
| SE 입도 | D50vol 4 / 11 / 20 / 40 µm (넓은 PSD) | 생산 r_SE **0.5 µm (⌀1.0)** · 코퍼스 r_SE 최대 1.5 µm (⌀3.0) | 우리 생산값은 그들 S 보다 **지름 4배 미세** — 검정 범위 밖 |
| 순수 SE σ | **2.2 mS cm⁻¹** 펠릿(L 2.8), PSD 무관 | σ_grain **3.0** (Cronau 단결정) × Cronau(r_SE) | 펠릿(입계 포함) < 단결정: 2.2/3.0 = 0.73 (우리 산수) — CL-81 이 적은 "STEP3 는 grain-interior σ 를 먹인다" 와 같은 방향 |
| σ_ion,eff vs 입도 | 작은 SE → ↑ (0.165 → 0.254), 공극 24.3 → 14.1 % 동반 | 폼: 입도는 φ_eff·CN·cov·f_p·C(τ) 로 들어간다(패킹) | **방향 일치** (frame [4] 독립 실측) |
| κ 정의 | κ = φ·σ₀/σ_eff | τ_Laplace,eff 같은 정의 (Minnmann 식과 동일) | 직접 비교 가능한 정의 |
| σ_e 측정 | 이온차단 대칭셀 **TLM(R_el 에 NCM–NCM R-CPE 포함) + DC**, AC ≈ DC | CL-38(대칭셀 TLM 전자 레일) · CL-46(펠릿 DC 문헌) | **TLM 레일이 계면항을 담으면 DC 관통 전도와 같다**는 실측 선례 (7b) |
| σ_e 값 | **0.26–0.41 mS cm⁻¹** (무탄소, 25 °C) | VGCF 전극 → 비교 대상은 **탄소 포함 문헌**(CL-46) | 모집단이 다르다 (7c) |
| σ_e 시뮬 | GeoDict voxel flux, **접촉저항 없음** → 실측의 2.0–3.0× (S/M/L) · 1.06× (XL) | STEP3 복셀 FV = **`CONTACT_FREE` 가지** (CL-81) | 같은 구조적 결손 — 크기는 σ_CAM 입력(출처 없음)에 묶임 |
| σ_ion 시뮬 | 실측의 **0.63–0.76×** (낮다) | STEP3 σ_ion 은 협착 미포함 **상한** 쪽 (CL-81) | 그들 모델은 상한이 **아래**에 있다 ⇒ 미세구조 재현 오차가 계면항보다 크다 — sim/exp 비를 계면항의 척도로 쓰면 안 된다 |
| 미세구조 생성 | 무작위 배치 + 겹침 3 % 까지 제거, **공극은 실측 입력** | DEM 압밀(공극 창발) · MPM 소성 · STEP3 는 MPM 침대 위 | 그들은 **역학이 없다** — 공극·배치가 예측이 아니다 |
| 입자 형상 | SE 볼록 다면체, CAM 구(M/L/XL)·다면체(S), **강체** | DEM 강체구(+연화 접촉) · MPM SE 형상 소성 | 그들·우리 DEM 모두 형상 소성 없음, 우리 MPM 만 있음 |
| 해상도 | 600 nm (M/L/XL) · 300 nm (S) voxel — CAM 지름당 ≈ 7.6 / 15 voxel (우리 산수) | STEP3 생산 vox 0.15 µm, 격자 수렴 미확인 축 있음 (CL-41 · CL-72) | S 만 다른 격자·다른 상자 → S vs 나머지 시뮬 비교에 이산화 차가 섞인다 |
| 압력 | 성형 ≈375 MPa 1점 · 측정 50 MPa | 300 MPa 압밀 기준 | 다압력 데이터 없음 |

### 7b. 원장 CL-38 · CL-46 · CL-81 과의 연결 ★★

- **CL-38 (대칭셀 TLM 의 전자 레일 저항, status `hold`)** — 원장은 SDCP 원고 그림(Figures_v7 · SI v6)의 대칭셀 EIS 에서 뽑은 전자 레일 값을 **σ_e 앵커로 인정하되 우리 값과의 큰 차를 "접촉저항" 이라 부른다**(값은 원장에만).
  이 논문이 주는 것: ① **TLM 전자 레일의 정의 자체가 계면항을 포함한다** — `R_el = L(r_el,bulk + r_el,int)` (Eq. 2), 그리고 우리 검산대로 Eq. 1 의 DC 극한은 정확히 그 합이다.
  ② 무탄소 복합체에서 **그 합 = DC 분극 값**(`Fig. S14`). ⇒ *"대칭셀 TLM 전자 레일은 DC 관통 전도와 같은 양일 수 있다 — 단 레일이 NCM–NCM(또는 입자 간) 계면 요소를 **담고 있을 때만**."*
  ⚠ 전이 한계: CL-38 의 전극은 **VGCF 를 담는다** — 그 전극의 전자 레일은 NCM–NCM 이 아니라 **탄소망**이고, 탄소–탄소·탄소–NCM 접촉이 그 계면 요소다. 이 논문은 **정의와 방법의 선례**이지 **값**을 주지 않는다.
- **CL-46 (절대 σ_e 는 문헌 펠릿 DC 와 같은 자릿수, status `live`)** — 원장의 비교군은 **탄소 포함** 황화물 복합양극 DC 값(Lee 2025 · Kim 2024)이다.
  이 논문은 그 비교를 **흔들지 않는다** — 무탄소 복합체라 다른 모집단이다. 오히려 CL-46 의 선택(탄소 포함 문헌만 비교)이 **왜 맞는지를 보여 주는 대조군**이다: 탄소가 빠지면 σ_e 가 **두 자릿수 아래(0.26–0.41)** 로 떨어진다.
  ★ 방법 대응: CL-46 bridge 는 *"DC 분극 = STEP3 가 푸는 관통 전자 전도"* 라 적는다. 이 논문의 AC ≈ DC(`Fig. S14`)는 **무탄소 계에서 TLM 과 DC 가 같은 양을 잰다**는 추가 근거다.
- **CL-81 (복셀 σ 는 `CONTACT_FREE` 가지 위, status `live`)** — GeoDict ConductoDict 도 **같은 상 voxel 을 벌크로 잇고 접촉 항이 없다** = 같은 가지.
  ① **전자 채널**: 시뮬이 실측보다 **2.0–3.0×(S/M/L) 높고 추세가 반대** — `CONTACT_FREE` 가 상한이라는 CL-81 의 예측과 **부호가 맞는** 외부 실례. 저자 자신이 원인을 **입자 간 저항**으로 지목한다(가설).
  ② **이온 채널**: 시뮬이 **실측보다 낮다**(0.63–0.76×) — 상한이어야 할 것이 아래에 있다 ⇒ **모델 미세구조(PSD 절단·vol% 불일치·600 nm 해상도)가 접촉항보다 큰 오차**를 낸다. CL-81 이 경고한 *"그 배수를 하나의 보정 배수로 다른 솔버에 이식할 수 없다"* 의 실례다.
  ③ **처방 대응**: CL-81 의 결손 (2) *"본질적 계면 저항 — 격자와 무관하게 없다"* 에 대해 이 논문의 TLM 이 쓰는 형식(**입자 간 계면 = 직렬 R∥CPE**, 전하 전달 저항)은 STEP3 에 넣을 **면(face) 컨덕턴스 항의 함수형 후보**다. ⚠ **값은 주지 않는다**(Q3).
  ④ 우리 VGCF 전극에서 σ_e 경로는 NCM–NCM 이 아니라 **탄소망**이므로, 이 논문의 전자 계면항은 **우리 σ_e 에 직접 해당하지 않는다**. 직접 해당하는 것은 **이온 채널의 SE–SE 접촉항**(CL-81 본문의 대상)이다.

### 7c. 정본 σ_e 문헌 카드 셋과 나란히 (값은 전부 각 카드의 stated 값)

| 카드 | 복합체 | 탄소 | σ_e (mS cm⁻¹) | 방법 · 조건 |
|---|---|---|---|---|
| **이 논문** | NCM811 : LPSCl 70 : 30 wt% | **없음** | **0.301 / 0.257 / 0.311 / 0.406** (S/M/L/XL) | 이온차단 대칭셀 TLM + DC, 25 °C, 성형 3 t, 측정 50 MPa |
| `lee2026_lpscl_coating_thickness_ncm811` | NCM811 + LPSCl (MCL = **VGCF 제외** 복합체), 무코팅 | **없음** | **0.257** (무코팅) → 코팅 시 1.92 × 10⁻⁴ 까지 | SS‖MCL‖SS DC 분극 5–50 mV · 30 s/step, **60 °C**, 냉간 400 MPa |
| `minnmann2021_jes_charge_transport_bottlenecks` | NCM622(BASF, D̄≈3 µm) + LPSCl(NEI), CAM 25–61 vol% | **없음**(기본 계열; VGCF 는 별도 비교군) | **0.56** @ 42 vol% (스윕 ~0.021 → ~1) | 대칭셀 TLM, L = 470 µm, A = 0.785 cm² |
| `lee2025_corolling_dryprocess_lpscl_ptfe` | CAM : SSE : VGCF : PTFE = 80 : 17 : 3 : 0.5 wt% | **VGCF 3 wt%** | **34** (PTFE 0.5) · 4.5 (PTFE 2) · **0.011** (PTFE 5) · co/free 33/34 | 펠릿 DC 분극 계열, 75 MPa (카드 기준) |
| `kim2024_carbon_volumetric_occupation_se_domain` | AM 80/85/90 wt% + carbon 3 wt% | **carbon 3 wt%** | **38.6 / 54.8 / 65.2** · 건식 1 wt% SC/CF **5.08 / 5.18** | DC 정전압, 517 MPa |

- ⇒ **무탄소 세 편이 0.26–0.56 mS cm⁻¹ 에 모인다**(측정 온도 25/60 °C·CAM 분율이 달라도). 동료가 말한 "0.1–1" 은 **이 무탄소 군의 밴드**이고, 그 안에서도 CAM 분율에 강하게 걸린다(Minnmann 스윕).
- ⇒ **탄소 포함 군은 한~두 자릿수 위** — 바인더 ≤ 1 wt% 조건에서 **5.1–65 mS cm⁻¹** (Kim 2024 건식 1 wt% carbon 5.08 ~ Kim 2024 3 wt% 65.2; Lee 2025 PTFE 0.5 wt% 34). 우리 VGCF 3 wt% 전극의 절대 σ_e 는 **이쪽과 대조**해야 한다 — CL-46 의 선택이 맞다.
- ⚠ **"탄소가 있으면 항상 수십" 도 아니다** — Lee 2025 의 PTFE 5 wt% 는 VGCF 3 wt% 인데도 **0.011** 로 무탄소 밴드보다 **낮다**. 탄소망의 연결이 σ_e 를 정하고 바인더가 그것을 끊을 수 있다 (CL-46 이 이미 이 방향으로 PTFE 미스탬프를 설명한다).
- ⚠ Lee 2026 의 0.257 은 **60 °C** 값이라 25 °C 인 이 논문과 **같은 줄에서 비교하지 않는다**(NCM 전자전도는 열활성). 자릿수만 같이 본다.

### 7d. 우리 σ_ion 스케일링 폼 (CLAUDE.md T1) 과

`σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov_Hertz^½ · f_p³ · exp[a + b·ln τ + c·(ln τ)² + β_P2·P2 + β_F·log f_intact]`,
SAT-blend `φc_eff = (1 − g)·0.200 + g·0.195`, `δ = 0.040`, σ_grain = 3.0 mS cm⁻¹.

- 이 논문의 φ_SE(전체 부피) **0.36–0.41**(우리 산수)은 SAT-blend 문턱 ~0.2 보다 한참 위 → **퍼콜레이션 문턱 효과가 아닌 구간**이다. 입도 효과는 우리 폼에서 **CN² · cov^½ · C(τ)** 와 φ 자체로 들어가야 한다.
- **Cronau 인자**: 네 PSD 모두 인자 = 1 구간 → 폼의 σ_grain 쪽은 **변하지 않아야** 하고, 이 논문의 순수 SE 결과(2.2 평평)가 그것을 지지한다.
- **P2 항**(62:38 D1+ 코너, r_SE > 0.5 에서 켜짐)의 영역과 겹치지 않는다 — P:S 조성축이 없는 논문이다.
- ⚠ **점 대 점 대조는 못 한다**: 이 논문은 CN·coverage·f_p 를 내지 않는다(voxel κ 만). 대조는 **방향**(작은 SE → σ_ion↑, κ↓)에서 끝난다.

### 7e. frame [4]/[5] 판정
- **frame [5]**: 이 논문은 **전달 절반(실험 + voxel 전도)** 을 갖고 **역학 절반이 비어 있다** — 공극은 입력, 배치는 무작위, 형상은 강체 다면체. 우리가 DEM(공극 창발·접촉망)과 MPM(SE 형상 소성)으로 채우는 칸이 정확히 그 빈칸이다.
- **frame [4]**: 그들의 시뮬은 구조 입력만 실험에서 받고 전도는 독립으로 푼 뒤 실측과 비교했다 — 교차적합 없음. 결과는 *"이온 추세 일치·절대 과소 / 전자 추세 불일치"* = **모델 한계의 정량**이지 실패가 아니다(우리 인식론과 같은 읽기).

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | ASSB 반쪽셀 모식(In/LiIn · 분리막 · 복합양극, Li⁺/e⁻ 경로) + S(4)/M(11)/L(20)/XL(40 µm) 복합체 모식(20 µm 눈금) | 입도비 개념도 — SE ≫ CAM 이면 CAM 이 SE 섬 사이에 몰린다 |
| 2a | 부피 누적 PSD (1–300 µm, 로그) — 첫 점이 이미 S≈12 · M≈24 · L≈12 · XL≈4 % (figure-read ≈) | **넓은 PSD + 미세분 꼬리** — "D50 하나"로 입도를 말하면 안 되는 이유 |
| 2b | 순수 LPSCl Nyquist(0–140 Ω) + R-CPE 삽도 — 차단 스파이크만 | 2.2 mS cm⁻¹(L 2.8) 의 원자료 |
| 2c | XRD 2θ 10–70°, 네 패턴 동일 | 입도 ≠ 결정구조 변화 |
| 2d | PDF G(r) 0–20 Å, 네 곡선 동일 | 입도 ≠ 국소구조 변화 (Cronau 감소 구간 아님) |
| 3a | SEM-EDS(NCM 보라·LPSCl 노랑), 25 µm 눈금 — S 는 잘게, XL 은 큰 노란 섬 | 분포 균질도의 실측 판독 |
| 3b | GeoDict 모델 단면(LPSCl 청록·NCM 황토) | 모델 SE 섬이 실측보다 큼(§10-6) |
| 4a | C/20 첫 충방전(2.0–3.7 V vs In/LiIn, 0–250 mAh g⁻¹) | 용량 서열 S > M ≈ L > XL |
| 4b | 1C 충방전 — 방전 끝 ≈105/90/63/45 mAh g⁻¹ (figure-read ≈) | 과전압이 입도와 함께 커짐 = 수송 제한 |
| 4c | 0.1 C 50 사이클 평균±표준편차 | 감쇠 모양 동일, 절대값 차 유지 |
| 4d | 율 시험 C/20→1C→C/20 | 1C ≈100/89/70/53 (figure-read ≈) |
| 5a | **이온차단(강철‖복합체‖강철) Nyquist + T-type TLM 회로**(전자 레일 = R + R∥CPE 반복) | ★ **σ_e 측정의 원자료 · NCM–NCM 계면항이 회로에 있는 자리** (CL-38 선례) |
| 5b | 전자차단(In/LiIn‖SE‖복합체‖SE‖In/LiIn) Nyquist + TLM(양끝에 Z_SE · Z_In/LiIn‖SE 부가) — 실축 끝 ≈220–440 Ω (figure-read ≈) | σ_ion 측정 셀 설계 |
| 6a | 유효 σ_ion(위, 노랑)·σ_el(아래, 청회) 실측 원 vs 시뮬 삼각형 vs D50vol | ★★ **Table S4 의 그림판** — σ_el 실측 평평 vs 시뮬 감소 (CL-81 외부 실례) |
| 6b | 용량(C/20·1C) vs σ_ion/σ_el — x = 0.41/0.49/0.77/0.84 | "균형 전달" 서사 (4점·교란 §10-12) |
| 6c | GeoDict 국소 이온 전류밀도 3D(0–100 mA cm⁻²) — S 고름, XL 점접촉 집중 | 우리 STEP3 전류장 시각화의 문헌판 |
| S1 | NCM811 SEM (D50 3.4 µm) | CAM 형상 — 1차 입자 응집체 |
| S2 | LPSCl SEM a–d (4/11/20/40 µm) | 큰 PSD 도 미세 조각 동반 |
| S3 | Arrhenius ln(σT) vs 1000/T (3.2–4.3 K⁻¹), 네 시료 겹침 | 기울기 ≈ 0.40 eV (우리 산수) · 절대 수준 불일치(§10-8) |
| S4 | Rietveld a–d (Rwp 5.9/6.7/8.1/8.3 %, gof 1.2/1.2/1.2/1.1) | 상순수 |
| S5 | PDF small-box a–d (Rw 21.6/19.7/19.9/19.1 %) | 국소구조 동일 |
| S6 | Raman a–d, 427 cm⁻¹ PS₄³⁻ | 동일 |
| S7 | SEM-EDS 2 µm(a1–d1)·20 µm(a2–d2) | 분포 균질도 · NCM 1차 입자 |
| S8 | 0.1 C 50 사이클 삼중반복 + CE | S 셀 간 차 ≈ 15 mAh g⁻¹ · 첫 CE ≈78→72 % |
| S9 | 율 시험 삼중반복 + CE | 반복성 |
| S10 | 이온차단 EIS 삼중반복 — 실축 끝 S ≈106/170/210 Ω 등 (figure-read ≈) | **σ_el(S) ±0.15 의 정체** (셀 간 2배) |
| S11 | 전자차단 EIS 삼중반복 | σ_ion 반복성 |
| S12 | DC 분극(이온차단) 전류-시간·V-I — b1 축라벨 "E"/"CC29" | DC 교차확인 원자료 (§10-10) |
| S13 | DC 분극(전자차단) µA 급, 셀 2개 | σ_ion DC |
| S14 | AC vs DC 유효 σ (전자·이온) — S 의 σ_el DC ≈0.38 | ★ **본문 "0.38" 의 출처로 보이는 점** · AC ≈ DC = TLM 레일이 계면 포함 관통 전도 |
| S15 | κ_ion·κ_el 관측 vs 시뮬 — b 의 시뮬 계열은 κ_ion,sim 복제 | κ 정의 대응 · 그림 오류(§10-3) |
| S16 | 부피 CDF(a) · 개수 CDF(b) — S 개수 중앙값 ≈0.16 µm | 부피/개수 PSD 괴리 |
| S17 | 실측 CDF vs GeoDict 입력 CDF: σa 폭(a) · span 폭(b) — M/L/XL 입력이 거의 단분산 계단 | ★ 모델 PSD 가 실측과 다르다 (§10-6) |
| S18 | CAM count CDF 적합(2–7 µm) + SEM | CAM D 값 불일치(§10-5) |
| S19 | L 모델 생성 4단계(LPSCl 다면체 → NCM → 잔여 NCM → Cleanse) | 기하 생성기의 한계(역학 없음) |
| S20 | 모델(위) vs SEM-EDS(아래) a–d | 모델 SE 섬 과대 |
| S21 | GeoDict 국소 전자 전류밀도 3D(0–220 mA cm⁻²) | 시뮬 σ_el 이 작은 SE 에서 높은 이유(균질) |
| S22 | CAM–LPSCl 비표면 vs D50vol (축 10⁵ m⁻¹) | 본문 지수 오기 판정(§10-7) |
| Table S1 | 모델 파라미터: 30/70 wt% · 48/52 vol% · 1.87/4.78 g cm⁻³ · 공극 14.1/18.1/21.4/24.3 % (SI 표기 ST1) | 공극 앵커 · vol% 불일치(§10-4) |
| Table S2 | LPSCl PSD 입력: µa · σa · "s" · D90vol · D10vol (SI 표기 ST2) | 모델 PSD 가 폭을 잘못 받은 근거 |
| Table S3 | CAM PSD 입력: µa 4.57 · σa 0.99 · D90/D50/D10num 6.89/3.38/1.54 (SI 표기 ST3) | CAM 입도 |
| Table S4 | 유효 σ_ion·σ_el 실측/시뮬 + κ_sim (SI 표기 ST4) | ★★★ **이 카드 수치의 정본** |

## 9. Post-processing ★
- **EIS → TLM 적합**: RelaxIS 3, "T-type"(두 레일 + 가로대 CPE) 회로, Eq. 1–3 → R_el, R_ion → σ = L/(R·A) (두께 미보고).
- **DC 분극**: 단계 전압(전자) / 단계 전압(이온, 0.5 mV) → 정상 전류 → V–I 기울기로 R (`Fig. S12`·`Fig. S13` 의 a2–d2 패널) → σ. AC 와 겹쳐 그림(`Fig. S14`).
- **순수 SE**: R-CPE 적합 → σ; 온도가변 EIS → ln(σT) vs 1000/T (Ea 수치 미보고).
- **구조**: Rietveld(XRD, 도구 미기재) · PDFgetX3 + TOPAS V7 small-box(PDF) · Raman.
- **PSD**: log-normal CDF 적합(scipy `curve_fit`, 첫 점 제외) → 기하 μ, σ → 산술 µa = exp(μ + σ²/2), σa = µa·√(e^{σ²} − 1) → span s = (D90 − D10)/D50 로 폭 대체 + D10/D90 절단 (SI p. S10–S13).
- **미세구조·전도**: GeoDict GrainGeo(배치) → ProcessGeo(Cleanse) → ConductoDict(flux, 1 V / 0.3 V) → σ_eff, κ = φσ₀/σ_eff → MatDict 비표면적. 구조 3개 평균.
- **기록·그림**: 모든 σ 는 mS cm⁻¹, 삼중반복 평균 ± 표준편차(성능·EIS), 시뮬은 3 구조 평균.

## 10. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **본문 σ_el(S) = 0.38 ± 0.15 는 자기 그림·표와 어긋난다.** `Table S4` 0.301 = `Fig. 6a` ≈0.30 = `Fig. 6b` 비 0.84 와 정합하고, 0.38 은 `Fig. S14` DC 값(≈0.38)과 맞는다. ⇒ **인용은 `Table S4` 로**, "0.38–0.40" 은 *본문 문장* 으로만.
2. **NCM–NCM 계면항은 모델에만 있고 숫자가 없다.** 분리 몫(bulk vs 계면)은 보고되지 않았다. "시뮬이 높은 이유 = NCM 간 저항" 은 저자 **가정**(p. 6).
3. **`Fig. S15b` 의 "simulated" κ_el 계열(≈4.7/6.7/8.6/7.5, figure-read)은 κ_ion,sim 을 복제했다.** `Table S4` 의 κ_el,sim 3.04/2.89/3.35/4.75 는 φ_CAM·5.2/σ_el,sim 재계산과 정확히 일치하므로 표가 맞다.
4. **`Table S1` vol% 와 밀도가 서로 모순**: 30/1.87 : 70/4.78 → LPSCl **52.3 vol%**, 표는 **48**. 모델은 48 을 썼다(κ 재계산). ⇒ 모델 SE 부피가 고체 기준 ~4 %p 작게 들어갔을 **가능성** — 방향은 시뮬 σ_ion 과소 · σ_el 과대와 **같다**(우리 추론, 크기 미검증).
5. **CAM 입도 표가 자기 그림과 안 맞는다**: `Table S3` D10/D50/D90num = 1.54/3.38/6.89 µm vs `Fig. S18a` ≈3.0/4.7/5.5 µm (figure-read). 같은 표의 µa 4.57·σa 0.99 는 그림과 맞는다. 본문 "D50 = 3.4 µm" 은 표의 D50num 에서 왔다.
6. **모델 SE PSD 가 실측보다 훨씬 좁고 크다**: `Table S2` 가 span 을 **"s / µm"** 로 적고(span 은 무차원) 그 수를 폭으로 넣어 M/L/XL 입력이 **CV 0.21 / 0.11 / 0.05**(µa 21.1/30.6/65.3 µm, 우리 산수) = 거의 단분산 계단(`Fig. S17b`). 저자 자신이 적은 *"substantial number of small particles"* 가 모델에서 **사라진다**. `Fig. S20` 의 모델 SE 섬이 SEM 보다 큰 것과 같은 방향. ⇒ 시뮬 절대값·sim/exp 비의 해석에 **1차 교란**.
7. **비표면적 본문 값이 100배 틀렸다**: 142.7 × 10⁵ m⁻¹ 은 CAM 전체 표면(≈5.9 × 10⁵ m⁻¹, 우리 산수)의 24배라 불가능. `Fig. S22` 축(≈1.43 × 10⁵)이 맞다.
8. **`Fig. S3` Arrhenius 절대 수준이 본문 σ 와 안 맞는다**: 298 K 에서 ln(σT) ≈ 1.35 → σ ≈ 13 mS cm⁻¹ (σ 를 S cm⁻¹ 로 읽을 때, 우리 산수) vs 본문 2.2. 단위·정규화 미상 ⇒ **기울기(≈0.40 eV)만** 쓸 것, 그것도 figure-read.
9. **σ_CAM = 5.2 mS cm⁻¹ 출처 없음.** 시뮬 σ_el 은 이 값에 선형 비례하므로 "시뮬이 2–3배 높다" 의 **크기는 이 입력의 함수**다. 정본 `aminchiang2016_nmc_electronic_ionic_transport_vs_li` 카드의 NMC333/532 실측 봉투는 5 × 10⁻⁵ … 13.8 mS cm⁻¹ (30 °C, 탈리튬 x ≤ 0.75, **SOC 에 수 자릿수 의존**)이고 811 로의 외삽은 불확실하다 — 5.2 가 합성 직후(방전) NCM811 의 값이라는 근거는 이 논문에 없다. **추세 불일치만 견고**하다.
10. **DC 프로토콜 서술 불일치·그림 결함**: 본문 *"45 to 50 mV … in 5 mV steps"* vs `Fig. S12` ±5→±45 mV(figure-read). `Fig. S12 b1` 축 라벨이 "E"·"CC29"(플로팅 기본값). 본문 p. 4 "Figure 4" → Figure 5 오기.
11. **XRD 파장 인쇄값 1.545051 Å** 는 Cu Kα₁(≈1.5406 Å)과 다르다 — 오기로 보인다(결론 무관).
12. **"균형 전달" 인과 미분리**: `Fig. 6b` 는 4점이고 입도·공극·계면면적·σ 비가 함께 움직인다. 캡션("initial charge capacity")과 그려진 크기(방전급)도 어긋난다.
13. **S 의 반복성 불량**: σ_el ±0.15(±50 %), 첫 충전 ±24, 셀 간 2배 저항 차(`Fig. S10a`) — 저자는 "끈적한 취급감" 으로 설명. S 결론에 **넓은 오차**를 붙일 것.
14. **단일 조건**: 조성 70:30 하나 · 성형 3 t 하나 · 측정 50 MPa · 25 °C · 무탄소 · In/LiIn 반쪽셀. **다압력·탄소 포함·다른 CAM 분율로 전이 불가.** 대칭셀 두께 미보고(σ 재계산 불가).
15. **시뮬 이산화 불균일**: S 만 300 nm·(90 µm)³, 나머지 600 nm·(300 µm)³ — S vs M 시뮬 비교에 해상도·상자 차가 섞인다(σ_el,sim S ≈ M 인 것도 이 조건에서 나왔다).
16. **이해관계**: 공저자 3명이 시료 공급·PSD 측정사(AMG) 소속(명시). PSD 제조법 미공개.

## 11. 적용 인사이트
- ① **동료 논쟁 정리용 한 줄**: *"0.38–0.40 mS cm⁻¹ 는 **무탄소·무바인더** NCM811/LPSCl 70:30 wt% 복합체의 25 °C 값이다(본문 p. 6; 표 값은 0.26–0.41). 탄소 포함 황화물 양극 문헌값은 바인더 ≤ 1 wt% 에서 5.1–65 mS cm⁻¹ 이고, 바인더(PTFE 5 wt%)가 그것을 0.011 까지 깎을 수도 있다 — σ_e 는 탄소망의 연결이 정한다."*
- ② **CL-38 의 방법론적 뒷받침**: 대칭셀 TLM 의 전자 레일을 σ_e 로 읽으려면 **레일이 입자 간 계면 요소를 포함**해야 하고, 그 합의 DC 극한이 관통 전도다(Eq. 1 검산 + `Fig. S14`). 우리 쪽 대조 셀(VGCF 전극)에서는 **탄소–탄소·탄소–NCM 접촉이 그 요소**다.
- ③ **CL-81 처방의 함수형 후보**: 입자 간 계면 = **직렬 R∥CPE**(전하 전달 저항 + 계면 용량). STEP3 에 넣는다면 SE–SE 면 컨덕턴스(`g = 2σa` 형, CL-81 권고)에 **직렬 계면 저항**을 더하는 형식. 값은 이 논문이 안 준다 — 앵커는 우리 랩 Kim 2025(R_i,gb 분리 측정) 쪽.
- ④ **생산 r_SE 0.5 µm 의 외부 근거는 방향뿐**: 4 → 40 µm 에서 "작을수록 σ_ion·용량↑" 은 확인됐지만 ⌀1 µm 는 범위 밖. 서브-µm 영역은 Cronau(볼밀 비정질화)와 이 논문(재료 불변) 사이가 **비어 있다**.
- ⑤ **공극을 입력으로 받는 voxel 모델의 한계**가 수치로 보인다 — 그들 σ_ion 이득의 일부는 **공극 감소(φ_SE↑) 그 자체**다. 우리 DEM/MPM 은 공극을 창발시키므로 *"입도 → 공극 → σ"* 사슬을 **입력 없이** 풀 수 있다 = frame [5] 에서 우리 쪽 부가가치.
- ⑥ **PSD 는 부피·개수를 같이 적어라**: 같은 시료가 부피 D50 4 µm / 개수 중앙 ≈0.16 µm 다. 우리 입력(r_SE 단일값)과 대조할 때 어느 쪽인지 명시.

## 12. 인용 가능 문장 (영문 초안)
- *"In carbon- and binder-free NCM811/Li₆PS₅Cl (70:30 wt%) composites, the effective electronic conductivity measured by ion-blocking symmetric-cell impedance with a transmission-line model is 0.26–0.41 mS cm⁻¹ and nearly independent of the Li₆PS₅Cl particle size (D50vol 4–40 µm) [Schlautmann 2023, Table S4]."*
- *"Reducing the Li₆PS₅Cl D50vol from 40 to 4 µm lowers the composite void fraction from 24.3 to 14.1 % and raises the effective ionic conductivity from 0.165 to 0.254 mS cm⁻¹, while the pellet conductivity of the pure electrolyte (2.2 mS cm⁻¹) and its average and local structure remain unchanged [Schlautmann 2023]."*
- *"A contact-free voxel conduction model (GeoDict) over-predicts the electronic conductivity of these composites by a factor of 2–3 for the three finer electrolyte PSDs and reverses the size trend, which the authors attribute — without measuring it — to resistances between NCM particles [Schlautmann 2023, p. 6]."* (⚠ "factor 2–3" 는 `Table S4` 에서의 우리 산수임을 각주로)

## 13. 기법 용어 미니사전
- **TLM (transmission-line model)**: 복합전극을 이온 레일·전자 레일 두 저항선과 그 사이 계면 요소(가로대)로 나눈 사다리 회로. "T-type" = 두 전극이 같은 캐리어를 받는 대칭셀용 형태(여기서는 전자-전자 / 이온-이온 연결).
- **이온차단 대칭셀**: 양쪽이 금속(강철) — Li⁺ 는 못 나가고 전자만 관통 → DC 에서 전자 저항만 남는다. **전자차단 대칭셀**: 양쪽을 SE 층으로 막고 In/Li 전극 — 전자는 못 나가고 Li⁺ 만 관통.
- **z_el,int (전자 계면 임피던스)**: NCM 입자 사이 전자 전달의 저항 + 용량(R∥CPE). DC 극한에서 R 만 남아 전자 레일 저항에 더해진다.
- **CPE (constant phase element)**: 이상 커패시터 대신 쓰는 분산 용량 요소, Z = 1/[Q(jω)^α].
- **DC 분극**: 작은 계단 전압 → 정상 전류 → Ohm 기울기. 차단된 캐리어는 정상상태에서 흐르지 않으므로 남은 캐리어의 저항만 준다.
- **굴곡인자 κ (tortuosity factor)**: κ = φ·σ₀/σ_eff. 부피분율로 설명 안 되는 전도 손실. (τ 와 혼동 주의 — 여기 κ 는 Minnmann 의 τ² 와 같은 양.)
- **D50vol vs D50num**: 부피 가중 중앙 vs 개수 가중 중앙. 넓은 PSD 에서는 크게 다르다(S: 4 µm vs ≈0.16 µm).
- **span**: (D90 − D10)/D50 — **무차원** 폭 지표.
- **PDF (pair distribution function) · small-box**: 전 산란으로 얻은 원자쌍 거리 분포 G(r); 단위격자 하나로 맞추는 정련. Rw = 적합 잔차 지표.
- **Rwp / gof**: Rietveld 가중 잔차 / 적합도.
- **GeoDict**: 상용 디지털 재료 실험실 — GrainGeo(입자 생성), ProcessGeo(후처리), ConductoDict(전도 PDE), MatDict(형태 지표).
- **Cleanse**: 겹침 정리 후 남은 작은 고립 조각을 제거·재배정하는 ProcessGeo 연산.
- **비표면적 (specific interface area)**: 계면 면적 / 전체 부피 (m⁻¹).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
