<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = nakamura2020_dry_coating_ncm_li3ps4_core_shell.md (같은 그룹 · 같은 날 묶음).
     쪽 표기 = 본문 "p.N" (PDF N 쪽 = 학술지 인쇄 쪽 240 + N, 즉 PDF 1 = p.241 … PDF 9 = p.249 — 카드에는 PDF 쪽 N 을 쓴다).  SI 없음.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 300 dpi 렌더, 마커 중심이 인쇄 x 값에
     0.3 단위 안으로 떨어짐 → y ±0.02 축 단위) · [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · [추정] = 우리 해석 · [미확인] = 원문 (본문 9 쪽 전수) 에 없음.
     원문 9 쪽 텍스트 층 전수 + 그림 7 · 표 1 = 크롭 8 장 전부 렌더로 열람. -->

# 건식 충격 블렌딩 (Hybridizer NHS-0) 코팅의 공정 창 — 황화물 SE 의 모델 물질 Na₂SO₄ (연성 · 상온 가압 소결) 로 NCM111 을 코팅: 회전자 선속도 50 m/s = 부분 피복 · ≥ 80 m/s = 완전 피복 · 시간 ↑ (60 → 1800 s) = 불연속 → 연속 막 · 게스트 비율 ↓ = 게스트 단위 질량당 에너지 ↑ → 연속 막 · 너무 세면 NCM 파쇄 (1800 s · ≤ 10 wt%) — 최적 80 m/s · 300 s · NCM:Na₂SO₄ 90:10 (막 ≈0.15 µm · 파쇄 없음) — Takashi Kawaguchi · Hideya Nakamura · Satoru Watano (오사카부립대, Powder Technol. 2017)

> slug `kawaguchi2017_dry_coating_parametric_na2so4_model_se` · DOI `10.1016/j.powtec.2016.09.085` · type `exp (건식 코팅 공정 매개변수 연구 — 모델 SE · SEM/EDX · ICP-AES 순조성 · 세척 후 입도 · 압분체 DC 저항 R_inc; 전기화학 · DEM 없음)` · PDF `040ad7d4-25._Parametric_study_of_dry_coating_process_of_electrode_particle_with_model_material_of_sulfide_solid_electrolytes_for_all-solid-state_battery.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Parametric study of dry coating process of electrode particle with model material of sulfide solid electrolytes for all-solid-state battery* (p.1)
> **저자 · 소속 (p.1)**: Takashi Kawaguchi · **Hideya Nakamura\*** · Satoru Watano — Department of Chemical Engineering, Osaka Prefecture University, Sakai (\* 교신 hnakamura@chemeng.osakafu-u.ac.jp)
> *Powder Technology* **305** (2017) 241–249 · 접수 2016-05-13 · 수정 2016-08-22 · 승인 2016-09-30 · 온라인 2016-10-03 (p.1) · 연구비 JST ALCA-SPRING · FESEM/EDX = Tatsumisago · Hayashi 교수 (p.9).  이해상충 · 데이터 진술 없음.
> **같은 그룹 계보 · 같은 축 카드 (링크만)**: [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (같은 그룹 · 같은 장치 계열을 **실제 황화물 SE (Li₃PS₄)** 에 적용 — 이 논문을 ref 25 로 인용, 단 모델 물질을 "sodium sulfide" 로 잘못 적음) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (ref 16 — "상온 가압 소결" 의 근거) · [`lee2026_lpscl_coating_thickness_ncm811`](lee2026_lpscl_coating_thickness_ncm811.md) (메카노퓨전 LPSCl 껍질 두께 축) · [`lee2026_mechanical_halogen_argyrodite_drycoating`](lee2026_mechanical_halogen_argyrodite_drycoating.md) (1저자 공저 — RAM 건식 코팅의 기계 물성 축) · [`kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable`](kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable.md) (메카노퓨전 · DEM 응력 지수 — 뼈대 카드).
> **판독 원자료**: `litdb/figures/kawaguchi2017_dry_coating_parametric_na2so4_model_se/digitized.csv` (12 행 — R_inc 세 그림) · 크롭 8 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 실제 황화물 SE 가 모자라 대신 **Na₂SO₄** (상온 가압 소결 · 황화물과 비슷한 강성 · 탄소성 — ref 18 의 압입 시험) 를 게스트로, NCM111 (부피 D50 5.4 µm) 을 호스트로 **Hybridizer NHS-0** (회전자 118 mm · 날 6 개 · 순환관) 에서 11 조건을 돌리면, **선속도 50 m/s 는 덜 덮고 80 m/s 이상은 다 덮으며**, 시간이 길수록 · 게스트 비율이 낮을수록 (게스트 단위 질량당 기계 에너지 ↑) **불연속 → 연속 막**으로 가지만, 지나치면 **NCM 이 깨진다** (1800 s · ≤ 10 wt%) — 그래서 최적은 **80 m/s · 300 s · 90 : 10 wt%** (연속 막 ≈0.15 µm · NCM 파쇄 없음 · 순조성 유지) 이고, 연속 막일수록 압분체 (360 MPa) 의 전자 저항 증가 R_inc 가 커서 계면 접촉이 잘 이뤄졌다고 판정한다 (p.4–8).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도) | **Hybridizer NHS-0 (Nara Machinery)** — 챔버 안지름 **125 mm** · 깊이 **49 mm** · 유효 부피 **470×10³ mm³** · 날 6 개 회전자 지름 **118 mm** · 순환관 / 선속도 **50 · 80 · 100 m/s** · 시간 **60 · 180 · 300 · 600 · 1800 s** · 초기 게스트 **5 · 10 · 20 · 30 wt%** · 투입 **10.0 g** · 막자 예비 혼합 **30 min**.  [우리 산술] 선속도 → 회전수 = 60·v/(π·0.118 m): **8,090 · 12,950 · 16,190 rpm**.  온도 · 분위기 · 에너지 계측 [미확인] | [인쇄] p.2 · Table 1 · [우리 산술] |
| ② 피복을 어떻게 쟀나 · 값 | 직접 피복률 **없음** — SEM/EDX (Mn · S 지도) 정성 + **압분체 DC 저항 증가 R_inc = (R_DC − R_NCM)/x_Na₂SO₄** (식 1) 를 계면 접촉의 대리 지표로 (절연 게스트가 NCM–NCM 전자 경로를 끊을수록 큼) · 연속 막 두께 **≈0.15 µm** (Run 11 단면) | [인쇄] p.3 · p.7 · Fig 3–5 · 7 |
| ③ 코팅이 SE 를 얼마나 쓰나 · 잃나 | 초기 30 wt% → 순 **≈20 wt%** (장치 벽 부착 · 60 s 안에 평형) · 50 m/s 는 12.7 % (덜 붙음) · **≤ 10 wt% 에서는 손실 없음** (9.2 · 4.8 · Run 11 9.8 ± 0.5) — 낮은 비율에서는 게스트가 다 NCM 에 붙는다 | [인쇄] Table 1 · p.4–6 |
| ④ 공정 창의 양 끝 | 아래 끝 = 충격 부족 (50 m/s → 부분 피복, R_inc ≈0.06×10⁴ Ω·m [판독]) · 위 끝 = NCM 파쇄 (1800 s: 막이 얇아져 충격 전달 · 피로 / ≤ 10 wt% @ 100 m/s: 완충 부족) · 게스트 20–30 wt% 는 300 s 까지 파쇄 없음 (**완충 효과**) | [인쇄] p.4–6 · Fig 3c · 4c · 5c |
| ⑤ "같은 총 SE 에서 코팅 상태" 실험에 주는 것 | ★ **코팅 형태 (불연속 ↔ 연속) 가 SE 비율 자체에 걸린다** — 같은 시간 · 속도에서 게스트가 적을수록 연속 막 (게스트 단위 질량당 에너지 ↑).  ⇒ 우리 계획의 "코팅 SE 몫 2 수준" 은 몫과 함께 **막 형태도 바꾼다** — 형태를 맞추려면 시간 · 속도를 같이 조정하고 SEM 으로 형태를 확인해야 한다 [추정] | [인쇄] p.6–7 · [추정] §7-3 |
| ⑥ Nakamura 2020 (실제 황화물) 과의 연결 | 같은 그룹 · 같은 회사 (Nara) 장치 · 같은 10.0 g · 300 s · 같은 360 MPa (Nakamura 는 반쪽 셀 이중층 펠릿) · 같은 "불연속 → 연속" 기전.  Nakamura 는 조건 (13,000 rpm · 300 s) 을 *"our previous investigations [25,28]"* 에서 정했고 NCM 비파쇄를 *"the process optimization conducted in our previous study [25]"* (= 이 논문) 덕으로 돌린다 [인쇄 — Nakamura 2020 p.4 · p.6].  13,000 rpm 은 이 논문 회전자 (118 mm) 라면 **≈80 m/s** = 이 논문의 최적 선속도 [우리 산술 — Nakamura 는 장치 모델명 미기재 → 같은 회전자인지 추정].  Nakamura 는 LPS 15 wt% 투입 → 순 13.1 (이 논문 20 wt% → 15.5 와 같은 방향의 벽 손실) | [인쇄] p.2–3 · Table 1 · [우리 산술] |
| ⑦ DEM · 모델 | 없음.  기전 설명 = 충격력으로 연한 게스트가 단단한 호스트 위에서 **소성 변형 · 합체** (앞선 연구 ref 18 이 밝혔다고 인용) · 부착의 첫 단계는 *"partially covered … by the mortar-and-pestle premixing"* (Fig 6a) 로만 그린다 — **응집력 · 표면 에너지 서술 없음** (반데르발스 응집 서술은 Nakamura 2020 쪽에 있다 · §7-2) | [인쇄] p.4 · p.7 |

⛔ **한정어 (떼지 말 것)**: ① 게스트 = **Na₂SO₄ (이온 전도 없음 · 황화물 아님)** — 강성 · 탄소성 · 가압 소결만 닮게 고름 (값 [미확인] — ref 18) · 표면 화학 · 점착 (논지의 표면 에너지 축) 은 다를 수 있다 ② 호스트 = NCM111 (Toda NCM-03, 부피 D50 5.4 µm) ③ 조건마다 **1 회** (Run 11 만 n = 3) — *"We confirmed that there is reproducibility … no need to consider the batch deviation"* (자료 미제시) ④ 피복은 R_inc (전자 저항 대리) 와 SEM 정성뿐 — 피복률 % 없음 ⑤ 전기화학 시험 없음.

---

## 1. 한 줄 요약

전고체 전지용 복합 입자를 "활물질 1 차 입자 하나하나를 SE 로 감싸되 활물질은 깨지지 않게" 만드는 건식 코팅의 공정 조건을 체계적으로 쓸어 본 논문.  실험용 황화물 SE 를 충분히 구할 수 없어 같은 기계적 성질 (상온 가압 소결 · 강성 · 탄소성) 을 갖는 Na₂SO₄ 를 쓰고, NCM 을 호스트로 Hybridizer 에서 선속도 · 처리 시간 · 초기 조성을 바꿨다 (Table 1).  선속도는 80 m/s 이상이어야 다 덮이고 (Fig 3), 시간이 길수록 소성 변형 · 합체로 연속 막이 되지만 1800 s 에서는 NCM 이 깨지며 (Fig 4), 게스트를 줄일수록 같은 시간에도 연속 막이 되지만 10 wt% 이하 (100 m/s) 에서는 완충이 부족해 NCM 이 깨진다 (Fig 5).  이를 "부분 → 치밀화 · 불연속 → 소성 변형 · 합체 → 연속 → 파쇄" 의 지도로 정리하고 (Fig 6), 80 m/s · 300 s · 90 : 10 에서 0.15 µm 연속 막 · 파쇄 없음 · 압분체에서 NCM 이 응집 없이 게스트 기지 안에 흩어진 구조를 얻었다 (Fig 7).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (호스트 / 게스트) | 연구유형 |
|---|---|---|---|---|
| T. Kawaguchi · **H. Nakamura\*** · S. Watano (오사카부립대 화공) | *Powder Technol.* 305 (2017) 241–249 | 10.1016/j.powtec.2016.09.085 | **LiNi₁/₃Co₁/₃Mn₁/₃O₂ (NCM-03, Toda Kogyo)** 부피 D50 5.4 µm / **Na₂SO₄ (Wako JIS 특급)** 습식 다환 분쇄 (MICROS-0, Nara) 뒤 부피 D50 0.95 µm (쌍봉) | 실험 — 건식 코팅 공정 매개변수 · 형태 · 순조성 · 파쇄 · 압분체 전자 저항.  **전기화학 · DEM · 모델 없음** |

- 키워드 (p.1): Dry coating · All-solid-state battery · Composite particle.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 장치 · 시료 (p.2 · Fig 1 · Fig 2)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 장치 | **Hybridizer NHS-0 (Nara Machinery Co., Ltd.)** — 챔버 안지름 **125 mm** · 깊이 **49 mm** · 유효 부피 **470×10³ mm³** · 회전자 지름 **118 mm** · 날 **6 개** · 순환관 · 배출 밸브 (Fig 1) | [인쇄] p.2 |
| 원리 | 예비 혼합 분말을 넣고 회전 → 입자가 순환하며 **입자–벽 · 입자–입자 충돌**로 큰 충격력 → 응집 해체 + 호스트 표면을 게스트가 덮음 → 정해진 시간 뒤 배출 | [인쇄] p.2 |
| 호스트 | NCM111 (NCM-03, Toda Kogyo) · **부피 D50 5.4 µm** · 단봉 · 0 아닌 구간 ≈3.7–9 µm [판독 Fig 2a] · 표면 = *"rectangular-shaped grains"* (p.4 · Fig 2b — 1 차 입자 · 2 차 입자 구분은 원문에 없음) · 단단 · 취성 · 전자 전도성 | [인쇄] p.2 · p.4 |
| 게스트 | Na₂SO₄ (Wako, JIS 특급) — 다환식 습식 분쇄기 (MICROS-0, Nara) 로 미리 분쇄 · **부피 D50 0.95 µm** · 분포 **쌍봉** (≈0.2 µm 봉우리 + ≈1 µm 봉우리와 ≈3 µm 까지의 어깨 · 0 아닌 구간 ≈0.1–6 µm [판독 Fig 2a]) · 연하고 연성 · 비전도 | [인쇄] p.2 · p.7 |
| 모델 물질 선정 근거 | 황화물 SE 를 실험에 충분한 양으로 구할 수 없어서 · (i) 상온 가압 소결 (ref 16) (ii) 강성 · 탄소성 이 황화물과 비슷함을 **압입 시험 (ref 18)** 으로 확인 → Na₂SO₄ 선정 (수치는 이 논문에 없음 [미확인]) | [인쇄] p.2 |
| [우리 산술] 크기비 | 호스트/게스트 부피 D50 = 5.4/0.95 = **5.7** — 우리 SC 4 µm/SE 1 µm = 4 · PC 9/1 = 9 사이 | p.2 |

### 3-2. ★ 실험 조건 · 순조성 (Table 1 · p.2–3) [인쇄]

| Run | 선속도 (m/s) | 시간 (s) | 초기 NCM : Na₂SO₄ (wt%) | 코팅 뒤 순 조성 (wt%) | [우리 산술] 회전수 (rpm) |
|---|---|---|---|---|---|
| 1 | 50 | 300 | 70 : 30 | 87.3 : 12.7 | 8,090 |
| 2 | 80 | 300 | 70 : 30 | 78.5 : 21.5 | 12,950 |
| 3 | 100 | 300 | 70 : 30 | 79.8 : 20.2 | 16,190 |
| 4 | 100 | 60 | 70 : 30 | 78.9 : 21.1 | 16,190 |
| 5 | 100 | 180 | 70 : 30 | 76.3 : 23.7 | 16,190 |
| 6 | 100 | 600 | 70 : 30 | 79.1 : 20.9 | 16,190 |
| 7 | 100 | 1800 | 70 : 30 | 80.5 : 19.5 | 16,190 |
| 8 | 100 | 300 | 80 : 20 | 84.5 : 15.5 | 16,190 |
| 9 | 100 | 300 | 90 : 10 | 90.8 : 9.2 | 16,190 |
| 10 | 100 | 300 | 95 : 5 | 95.2 : 4.8 | 16,190 |
| 11 | 80 | 300 | 90 : 10 | **90.2 ± 0.5 : 9.8 ± 0.5** (n = 3) | 12,950 |

- 총량 **10.0 g** (모든 Run) · 조건마다 1 회 (Run 11 제외) · 재현성은 확인했다고만 적음 [인쇄 p.2].
- 순조성 측정: **ICP-AES (SPS7800, Seiko Instruments)** [인쇄 p.3].
- 벽 부착: 30 wt% 투입은 모든 선속도에서 순 게스트가 줄었다 (챔버 · 순환관 벽) · **50 m/s 는 12.7 % 로 더 낮음 = 충격이 약해 덜 붙음** · 시간과 무관하게 ≈20 wt% (Run 3–7) = 벽 부착 · NCM 부착이 **60 s 안에 평형** · ≤ 10 wt% 는 거의 손실 없음 (*"most of the Na2SO4 particles were firmly adhered onto the NCM particles … without loss"*) [인쇄 p.4–6].

### 3-3. ★ 선속도 효과 (Fig 3 · p.4–5)

- **50 m/s**: Mn · S 가 같은 자리이나 NCM 원래 표면 (직사각형 결정립) 이 보임 = **부분 피복** · **80 m/s**: 원래 표면이 안 보임 = 거의 완전 피복 · **100 m/s**: 더 치밀한 **불연속 코팅** (30 wt% · 300 s) [인쇄 p.4].
- 기전 (ref 18): 연한 게스트가 강한 충격으로 단단한 호스트 위에서 **소성 변형 · 합체** → 막 · 80 m/s 가 그 충격의 문턱 [인쇄 p.4].
- R_inc (Fig 3b) [판독]: 50 m/s **0.06** · 80 m/s **1.24** · 100 m/s **1.50** (×10⁴ Ω·m) — [우리 산술] 80 / 50 = **≈20 배**.
- 세척 후 NCM 입도 (Fig 3c): 선속도가 높을수록 약간 작아지나 유의하지 않음 → **100 m/s 이하 · 300 s 안에서는 NCM 손상 없음** [인쇄 p.5].

### 3-4. ★ 처리 시간 효과 (Fig 4 · p.5–6)

- 60 s · 600 s = 불연속 코팅 → **1800 s = 연속 코팅** (기계 입력 에너지 ↑ → 소성 변형 · 합체) [인쇄 p.5].
- R_inc (Fig 4b — ⚠ 세로축 ×10⁵) [판독]: 60 s **0.049** · 180 s **0.140** · 300 s **0.151** · 600 s **0.122** · 1800 s **0.752** (×10⁵ Ω·m) — [우리 산술] 1800 s 는 300 s 의 **≈5 배** · 180–600 s 는 0.12–0.15 로 평탄 · 60 s 는 0.049 로 더 낮다.
- 입도 (Fig 4c): 600 s 까지는 파쇄 없음 = **게스트의 완충 효과** · **1800 s 에서 뚜렷한 크기 감소 = NCM 파쇄** (곡선 전체가 왼쪽으로 · 0 아닌 구간 ≈3.3–7.5 µm [판독]) — 원인 후보 둘 (둘 다 *"may be"*): 막이 얇아져 NCM 에 걸리는 충격이 커짐 · 피로 파괴 [인쇄 p.5–6].
- 요약 (p.6): 시간 ↑ = 연속 막 ↑ 이지만 NCM 손상 ↑ · 연속 막이 압분체 구조에 유리.

### 3-5. ★ 초기 조성 효과 (Fig 5 · p.6)

- 300 s 에서도 게스트 **≤ 20 wt%** 면 연속 막 (30 wt% 는 불연속, Fig 3a 100 m/s) — **게스트 단위 질량당 기계 에너지가 커서** [인쇄 p.6].
- R_inc (Fig 5b) [판독]: 5 wt% **0.23** · 10 wt% **0.67** · 20 wt% **1.99** · 30 wt% **1.50** (×10⁴ Ω·m) — 20 % > 30 % (순 게스트가 적은데도) = **연속 막이 불연속보다 계면 접촉에 유리** · 20 % 아래로는 R_inc 감소 — 원인은 *"may be"* 로 막이 얇아져 NCM 끼리 전자 경로가 생기는 것 [인쇄 p.6].
- 입도 (Fig 5c): 본문 = *"At less than 10 wt% of Na2SO4 significant breakage"* (완충 부족) · 20 · 30 wt% 는 파쇄 없음 [인쇄 p.6].  [판독] 큰 쪽 꼬리를 가장 많이 잃고 봉우리가 가장 높은 곡선은 **10 wt%** (≈2.4, 원래 NCM ≈1.7) · 5 wt% 가 그 다음 (≈2.0) — 같은 쪽의 순조성 문장도 *"lower than 10 wt% of Na2SO4 (Run No. 9 and 10)"* 로 10 wt% 를 포함하므로 본문의 "less than 10 wt%" 는 **"10 wt% 이하"** 로 읽어야 그림과 맞는다 [추정].

### 3-6. 기전 지도 (Fig 6 · p.7)

(a) 초기 = 막자 예비 혼합으로 일부 덮임 → (b) 충격 부족 = 부분 코팅 (시간이 지나도 그대로) / (g) 충격 과다 = 즉시 호스트 파쇄 (**관찰이 아니라 예상** — *"it is expected that host particles can be immediately broken"*) / (c) 충격 충분 = 게스트 치밀화 · **불연속 코팅** → (d) 시간 ↑ = **소성 변형 · 합체** → (e) **연속 코팅** → (f) 더 하면 호스트 파쇄.  아래 화살표 (오른쪽) = 처리 시간 · 위 화살표 (왼쪽을 가리킴) = 게스트 초기 비율 — 비율이 낮을수록 같은 시간에 오른쪽 (연속 막) 으로 간다 [인쇄 p.7 · 그림].  저자들은 이 기전이 *"other type of powder handling equipment in which mechanical forces are imparted to the particles"* 에도 적용될 것으로 보지만, *"the powder handling equipment which is able to achieve the continuous coating … is considered to be limited"* 라고 적는다 [인쇄 p.7].

### 3-7. ★ 최적 조건 검증 (Run 11 · Fig 7 · p.7–8)

- 요구 셋: (1) 호스트 파쇄 없음 (2) 연속 막 (3) 게스트 최소 → **80 m/s · 300 s · 90 : 10 wt%** · 게스트 하한 **10 wt%** (예비 시험 — 그 아래는 NCM 파쇄 불가피, 자료 미제시) [인쇄 p.7].
- 결과: 연속 막 **≈0.15 µm** (Fig 7a · b) · 순조성 유지 (90.2 ± 0.5 : 9.8 ± 0.5) · 세척 후 입도 · 표면 = 원래 NCM 과 같음 (Fig 7c · d) · **압분체 (360 MPa) 단면에서 NCM 이 응집 없이 Na₂SO₄ 기지에 흩어지고 계면 접촉이 잘 형성** (Fig 7e · f) [인쇄 p.7].
- 게스트 쌍봉 분포의 영향: 큰 게스트가 떨어져 나가 조성이 어긋날 걱정 → Run 11 은 조성이 유지돼 큰 게스트도 붙었다 = 최적 조건에 영향 없음 [인쇄 p.7–8].
- 맥락: 대부분의 황화물 복합 양극은 SE ≥ 30 wt% 이고, 10 wt% 로 코팅한 것은 PLD (Sakuda, ref 16) 뿐 — 건식 코팅이 더 실용적 [인쇄 p.8].

### 3-8. R_inc 측정 (p.3)

- 코팅 입자 **0.50 g** → ⌀10 mm 다이 (안벽 = 비전도 폴리아세탈, 상하 펀치 = 스테인리스) → 손 프레스 **360 MPa** → 다이 안에서 세로 방향 DC 저항 (Keithley 6514) → **R_inc = (R_DC − R_NCM) / x_Na₂SO₄** (식 1 · R_NCM = NCM 만의 압분체) [인쇄 p.3].
- 해석: NCM 이 잘 덮이고 계면이 잘 생기면 절연 게스트가 NCM 전자망을 끊어 R_inc ↑ · 덜 덮이면 NCM 망이 이어져 R_inc ↓ [인쇄 p.3–4].
- 단면: Ar 이온 단면 연마 (IM4000, Hitachi) → FESEM [인쇄 p.4].
- [우리 산술 · 추정] R_inc 는 **"전자 차폐"** 의 크기다 — 실제 황화물 껍질에서는 같은 현상이 σ_e 하락 (`nakamura2020_…` DC σ_e −94 %) 으로 나타난다.

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
NCM + 분쇄 Na₂SO₄ → 막자 30 min 예비 혼합 → Hybridizer (선속도 · 시간 · 조성 11 조건, 10.0 g) → (i) FESEM/EDX 형태 (ii) ICP-AES 순조성 (iii) 물로 게스트 씻어 낸 NCM 입도 (파쇄) (iv) 0.50 g · 360 MPa 압분체 DC 저항 → R_inc (v) 압분체 단면 SEM.

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **실험**: 게스트가 충격으로 **진짜 형상 소성 · 합체** (낱알 → 막) · 호스트는 과도한 충격 · 얇은 막 · 낮은 게스트 비율에서 **파쇄** · 게스트는 호스트의 **완충재**.
- **우리 대응**: 믹서 DEM (3 상 저-Fr 회전 드럼 · CED 행렬 점착 (SJKR) · 강체 구 — 메인 리포 `docs/reviews/mixer_layered_prereg_20260921.md`) 에는 게스트 소성 · 합체 · 호스트 파쇄가 **없다** · 충격 블렌더의 흐름은 묽다 — 같은 그룹의 Nakamura 2020 이 같은 회사 장치에서 *"ca. 1 vol%"* (다른 혼합기는 보통 > 30 vol%) 라고 적는다 (이 논문에는 고체 농도가 없다) — 우리 드럼 (조밀 흐름) 과 **다른 흐름 영역** ⇒ 코팅 상태는 우리 모델에서 **입력**이다 (결과가 아님).

### 4-3. 기법 미니 용어집
- **Hybridizer (NHS)**: Nara Machinery 의 충격식 건식 입자 복합화 장치 — 고속 회전자 · 날 + 순환관.
- **선속도 (tip speed)**: 회전자 끝의 선속도 = π · 지름 · 회전수.
- **불연속 / 연속 코팅**: 게스트 낱알이 따로 붙음 / 소성 변형 · 합체로 이어진 막.
- **완충 효과 (cushioning)**: 게스트 층이 충격을 흡수해 호스트 파쇄를 막는 것.
- **R_inc**: 게스트 질량분율로 나눈 압분체 전자 저항 증가 — 계면 접촉 · 피복 연속성의 대리 지표.
- **상온 가압 소결 (room-temperature pressure sintering)**: 황화물 SE 가 상온에서 눌리기만 해도 변형 · 합체해 입계 · 공극이 거의 사라지는 성질 (ref 16).

---

## 5. Figure set ★ (크롭 8 장 = `litdb/figures/kawaguchi2017_dry_coating_parametric_na2so4_model_se/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | Hybridizer 모식 (순환관 · 챔버 · 회전자 · 날 · 배출 밸브) | 코팅 장치의 실체 — 우리 드럼 믹서와 다른 장치 |
| 2 | (a) NCM · Na₂SO₄ 부피 입도 (게스트 쌍봉) (b) NCM SEM (c) Na₂SO₄ SEM | 호스트 · 게스트 크기비 5.7 |
| 3 | 선속도 50 · 80 · 100 m/s: (a) SEM + Mn · S 지도 (b) R_inc (c) 세척 후 NCM 입도 | ★ 선속도 문턱 80 m/s |
| 4 | 시간 60 · 600 · 1800 s: (a) SEM + 지도 (b) R_inc (×10⁵) (c) 입도 (1800 s 파쇄) | ★ 시간 → 연속 막 · 과처리 파쇄 |
| 5 | 초기 조성 80:20 · 90:10 · 95:5: (a) SEM + 지도 (b) R_inc vs 게스트 wt% (c) 입도 (≤10 % 파쇄) | ★ 게스트 비율이 막 형태를 바꾼다 (§7-3) |
| 6 | 기전 지도 (a)–(g) — 처리 시간 × 게스트 비율 × 충격 세기 | ★ 코팅 상태 공간의 그림 — 실험 설계의 축 |
| 7 | 최적 조건 (Run 11): (a) 코팅 입자 (b) 단면 (막 ≈0.15 µm) (c) 입도 (d) 세척 후 NCM (e · f) 압분체 단면 (×2000 · ×5000) | 응집 없는 분산 · 계면 형성 (모델 물질) |
| Table 1 | 11 Run 조건 + 순조성 | ★ 공정 창 원자료 · 벽 손실 |

## 6. Post-processing ★
- **무엇을**: SEM/EDX 정성 · ICP-AES 순조성 · 세척 후 레이저 회절 입도 · DC 저항 → R_inc.
- **안 한 것**: 피복률 정량 · 막 두께 분포 · 반복 (Run 11 외) · 오차 막대 · 입력 에너지 측정 · 온도 · 이온 전도도 · 셀.
- **우리 후처리 (이 카드)**: R_inc 판독 (세 그림 · Run 3 세 번 일치 확인) · 선속도 → 회전수 산술 · Nakamura 2020 회전수 대응.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 장치 · 흐름 | 충격 블렌더 (회전자 118 mm · 50–100 m/s · 고체 ≈1 vol% 묽은 흐름 — 같은 회사 장치에 대한 Nakamura 2020 의 진술, 이 논문에는 값 없음) | 3 상 저-Fr 회전 드럼 DEM (R 13.1 mm · 75 rpm · CGF 151.4 거친 입자 · CED 행렬 점착 · 조밀 흐름 — 메인 리포 `docs/reviews/mixer_layered_prereg_20260921.md`) | 다른 장치 · 다른 영역 — 충격 에너지 축이 우리에게 없다 |
| 게스트 거동 | 소성 변형 · 합체 → 막 | 강체 구 (겹침 δ) · 점착 (SJKR CED) | ⛔ 막 형성은 우리 DEM 밖 |
| 호스트 거동 | 과처리 · 얇은 막 · 낮은 게스트 비율에서 파쇄 | AM 파괴 = 접촉 판정 (Auerbach) 만 · 조각 없음 | 파쇄 완충 몫을 못 그린다 |
| 크기비 | 호스트/게스트 5.7 | SC/SE 4 · PC/SE 9 | 같은 범위 |
| 피복 지표 | R_inc (전자 차폐 대리) · SEM 정성 | coverage_AM (접촉 면적) · σ_e (망) | R_inc ↔ 우리 σ_e 하락과 같은 축 [추정] |
| 압분 | 360 MPa (0.50 g · ⌀10 mm) | 300 MPa | 비슷 |

### 7-2. 이종기술 논지 (`docs/hetero_thesis.md` 비준 블록 2026-10-05) 와의 관계
- 논지의 "SE 선코팅" 이 **물리적으로 무엇인가** 에 대한 공정 쪽 답: 연성 SE 를 큰 활물질 위에서 **충격으로 펴서 잇는 것** (불연속 → 연속) — 표면 에너지 (논지 §2) 가 아니라 **기계 에너지 · 소성** 으로 만든다.  논지는 코팅의 *결과* (상 간 표면 성질이 같아짐) 를 쓰고 이 논문은 코팅의 *과정* 을 준다 — 서로 다른 층이다 [추정].
- 응집 관련: 이 논문은 부착의 첫 단계를 *"partially covered … by the mortar-and-pestle premixing"* (Fig 6a) 로만 적고 **응집력 · 표면 에너지는 다루지 않는다**.  같은 그룹의 Nakamura 2020 은 같은 단계를 *"interparticle cohesive force (such as Van der Waals force) between the large core particle and smaller guest particle"* + 외력으로 설명하고 Seville 2000 (Powder Technol. 113, 그 목록 [32]) 을 인용한다 [인쇄 — Nakamura 2020 p.6].  논지 §2-3 (누가 뭉치는가 — 면적당 에너지 × 크기) · §2-5 (SE 조각은 코팅된 AM 에 붙는 쪽이 유리) 를 **이 논문으로 받치지는 않는다** — 받침이 필요하면 Nakamura 2020 의 정성 서술까지다 [추정].
- P1–P3 는 시험하지 않는다 (모델 물질 · 이온 전도 없음 · 혼합 상태 비교 없음).

### 7-3. ★ "같은 총 SE 에서 코팅 상태" 실험 (`docs/mixer_paper_pipeline_draft_20261013.md` V1 · V2 · V3) 에 주는 것
1. **코팅 형태는 (속도 · 시간 · 게스트 비율) 의 함수** — 같은 장치 · 같은 시간이라도 SE 비율이 다르면 막 형태가 다르다 (게스트 단위 질량당 에너지).  ⇒ V1 (코팅 상태) 과 V3 (SE 함량) 을 같이 움직이면 **형태가 교락**한다 — SE 함량 수준마다 연속 막이 되는 시간을 SEM 으로 먼저 찾고 맞춘다 [추정].
2. **벽 손실**: 게스트 20–30 wt% 투입에서 순 게스트가 크게 준다 (30 → ≈20) · ≤ 10 wt% 는 거의 없다 — 우리 SE 18.4 wt% 수준은 그 사이 ⇒ **코팅 뒤 순 조성 측정 필수** (Nakamura 2020 은 UV-vis, 이 논문은 ICP-AES).
3. **파쇄 창**: 우리 바이모달에서 큰 NCM (PC 9 µm) · 다결정은 파쇄 위험이 더 클 수 있고, SC 는 표면적이 커서 게스트를 먼저 가져간다 [추정] — 형태 · 입도 (세척 후) 를 PC · SC 따로 확인.
4. **R_inc 같은 값싼 대리 지표**: 압분체 전자 저항 증가 (또는 σ_e 하락) 로 "코팅이 이어졌나" 를 빨리 가르는 법 — 실제 황화물에서는 이온 경로 (σ_ion) 와 함께 재야 뜻이 있다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 → 코팅 형태 (부분 · 불연속 · 연속 · 파쇄) 의 **공정 창 지도** (실험).
- **없는 것**: 실제 SE · 이온 전도 · 셀 · 피복 정량 · 반복 · 모델.  ⇒ 우리 모델 어디에도 이 공정 축은 없다 (믹서 DEM 은 점착 · 혼합, MPM 은 압축) — 이 논문은 실험 설계 · 해석의 **바깥 지도**로만 쓴다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 코팅 상태는 "있다 / 없다" 가 아니라 공정 창의 한 점이다.**
- 논문: 50 m/s 부분 → ≥ 80 m/s 완전 · 불연속 → 연속 (시간 · 비율) → 과처리 파쇄 (Fig 6).
- 뜻: 우리 실험의 "코팅" 팔은 어느 상태인지 (불연속 / 연속) 를 SEM 으로 고정해 보고해야 비교가 선다 — 논지의 P2 ("코팅하면 응집이 사라진다") 도 **연속 막** 기준일 때 가장 깨끗할 것 [추정].
- 할 일: 실험 담당과 장치 · 조건을 정할 때 (파이프라인 Q4) "불연속 · 연속" 판정 사진을 결과 전 기준으로.

**8-2. SE 함량이 막 형태를 바꾼다 — V1 · V3 교락 경고.**
- 논문: 300 s 에서 게스트 ≤ 20 wt% 는 연속, 30 wt% 는 불연속 (Fig 5 · 3).
- 할 일: SE 함량 수준을 바꿀 때 코팅 시간을 수준별로 다시 정하거나, 형태가 다르다는 사실을 공변량으로 기록 (§7-3-1).

**8-3. 순 조성은 투입 조성이 아니다.**
- 논문: 30 → ≈20 wt% (벽 부착 · 60 s 안 평형) · 50 m/s 는 12.7 %.
- 뜻: "같은 총 SE" 는 **코팅 뒤 순 조성**으로 맞춰야 한다 (Nakamura 2020 이 그렇게 했다).
- 할 일: 코팅 분말의 순 조성 측정 (ICP · UV-vis 등) 을 실험 계획의 필수 단계로.

**8-4. 게스트는 완충재 — 코팅이 압축 중 AM 파쇄를 줄이는 기전의 공정 쪽 근거.**
- 논문: 20–30 wt% 게스트는 300 s 까지 NCM 을 보호 · 10 wt% 이하 · 1800 s 는 파쇄.
- 뜻: Nakamura 2020 이 압축 뒤 NCM 비파쇄를 *"the stress relaxation attributed to the core-shell structure"* (연성 LPS 껍질이 압축 응력을 줄임) 로 설명하고 그 비파쇄를 셀 성능 향상의 *"possible reason"* 으로 든 것 [인쇄 — Nakamura 2020 p.8] (그 카드 §8-3 의 기전 (b)) 과 같은 축 — 이 논문은 **코팅 공정 중** 완충, Nakamura 는 **압축 중** 완충이다.  우리 DEM 은 이 몫을 못 낸다 (조각 없음) → 실험–모델 차이의 후보 항목.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Using Na₂SO₄ as a mechanical model of sulfide electrolytes, Kawaguchi et al. (*Powder Technol.* 2017) mapped the dry impact-blending window for coating NCM: tip speeds ≥ 80 m/s were needed for full coverage, longer processing or a lower guest fraction turned discrete coatings into continuous ones, and excessive input (1800 s, ≤ 10 wt% at 100 m/s) fractured the NCM; the optimum was 80 m/s, 300 s, 10 wt% (≈0.15 µm continuous layer)."
- 국문: *"건식 충격 코팅에서 SE 막의 형태 (불연속 ↔ 연속) 는 처리 시간뿐 아니라 SE 비율 자체에 걸린다 — 같은 총 SE 비교라도 코팅 형태를 따로 확인해야 한다 (Kawaguchi 2017, 모델 물질 Na₂SO₄)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **모델 물질**: Na₂SO₄ 는 이온 전도가 없고 표면 화학이 황화물과 다르다 — 강성 · 탄소성 · 가압 소결 유사성의 수치 (ref 18) 가 이 논문에 없다.  표면 에너지 · 점착이 중요한 혼합 응집 (논지) 쪽으로는 옮기지 않는다.
2. **반복 없음**: 조건마다 1 회 (Run 11 만 n = 3) · *"no need to consider the batch deviation"* 의 근거 자료 없음.
3. **피복 정량 없음**: R_inc 는 전자 저항 대리 — 피복률 · 막 두께 분포가 아니다 · 게스트 질량분율로 나누는 정규화는 선형성을 가정.
4. **그림 캡션 표지 오류**: Fig 7 캡션은 패널 표지 (b) 를 세 번 쓰고 (단면 · 입도 · ×5000 단면) 세척 후 SEM 을 (c) 로 적는다 — 그림 속 표지는 c = 입도 · d = 세척 후 SEM · f = ×5000 이고 본문도 그림 표지를 따른다 · Fig 3b · 4b · 5b 세로축 이름의 "fragtion" 오타 · Fig 4b 만 ×10⁵ (나머지 ×10⁴) 이라 나란히 읽을 때 주의.
5. **"less than 10 wt%"** 의 경계 모호 — Fig 5c 에서 가장 크게 깨진 곡선은 10 wt% (100 m/s) [판독] → "10 wt% 이하" 로 읽어야 맞다 (§3-5) · 그런데 Run 11 (80 m/s · 10 wt%) 은 파쇄 없음 ⇒ 하한은 선속도에 걸린다 [추정] · 그 하한을 정한 예비 시험 자료는 없다.
6. **하한 10 wt% 의 예비 시험 · 온도 · 분위기 · 입력 에너지** 미제시.
7. **Nakamura 2020 과의 연결 표기 오류**: Nakamura 2020 은 이 논문을 *"sodium sulfide"* 의 연구로 인용한다 — 이 논문은 **sodium sulfate (Na₂SO₄)**.
8. **전이 한계**: NCM111 단봉 · Na₂SO₄ · 탄소 · 바인더 없음 · 셀 없음.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 11 | A. Sakuda, T. Takeuchi, H. Kobayashi, Electrode morphology in all-solid-state lithium secondary batteries consisting of LiNi1/3Co1/3Mn1/3O2 and Li2S-P2S5 solid electrolytes, Solid State Ionics 285 (2016) 112–117 | 카드 없음 — 작은 SE 로 단순 혼합 |
| 12 | J. Kim, M. Eom, S. Noh, D. Shin, Effect of mixing method on the properties of composite cathodes for all-solid-state lithium batteries using Li2S–P2S5 solid electrolytes, J. Power Sources 244 (2013) 476–481 | 카드 없음 — 혼합 방법 (습식) 효과 |
| 15 | A. Sakuda, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, All-solid-state lithium secondary batteries using LiCoO2 particles with pulsed laser deposition coatings of Li2S-P2S5 solid electrolytes, J. Power Sources 196 (2011) 6735–6741 | 카드 없음 — PLD SE 코팅 (본문은 PLD 를 [15,16] 으로 함께 인용) |
| 16 | A. Sakuda, A. Hayashi, M. Tatsumisago, Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery, Sci. Rep. 3 (2013) 2261 | 정본 카드 `sakuda2013_sulfide_mechanical_property` — 상온 가압 소결.  ⚠ 본문은 *"Only Sakuda et al. [16] … much less fraction of SE (=10 wt%)"* 를 이 논문에 돌리는데, 정본 카드는 그 셀 양극을 "PLD 코팅 LiCoO₂ · 무탄소 (80:20)" 로 적는다 — 이 논문의 "10 wt%" 와 같은 양인지 [미확인] |
| 17 | H. Kitaura, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, Fabrication of electrode-electrolyte interfaces in all-solid-state rechargeable lithium batteries by using a supercooled liquid state of the glassy electrolytes, J. Mater. Chem. 21 (2011) 118–124 | 카드 없음 — 유리 SE 과냉 액체 상태로 계면 형성 (가열 공정 · 본문 = 성능 저하 가능) |
| 18 | T. Kawaguchi, H. Nakamura, S. Watano, Dry coating of electrode particle with model particle of sulfide solid electrolytes for all-solid-state secondary battery, Powder Technol (2016), http://dx.doi.org/10.1016/j.powtec.2016.03.055 | 카드 없음 — 모델 물질 선정 (압입 시험) · 기전 원전.  같은 그룹 Nakamura 2020 목록 [28] 은 같은 DOI 를 *Powder Technol. 323 (2018) 581–587* 로 적는다 [인쇄 — Nakamura 2020] |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 9 쪽 텍스트 층 전수 · 저자 · 소속 · 날짜 · DOI = p.1 · 장치 치수 = p.2 인쇄 · Table 1 = 텍스트 층 + 크롭 영상 칸마다 대조.
- 그림 · 표 8 장 = 캡션 8 개 (그림 1–7 · 표 1; SI 없음) 전부 렌더로 열람 · 자동 추출의 "Table 1" 은 p.6 본문 문장을 캡션으로 오인한 쪽 전체 크롭이라 p.3 의 실제 표로 다시 잘랐다 · Fig 6 은 왼쪽 표지가 잘려 다시 잘랐다 · 나머지는 비백색 경계로 좁힘 · `figures.json` 의 `auto_bbox` · `recrop` · `manual_crop`.
- R_inc 판독: 세 그림의 Run 3 (100 m/s · 300 s · 70:30) 이 1.497 · 1.51 · 1.500 ×10⁴ Ω·m 로 서로 맞음 (축 배율 차 ×10⁵ 확인).
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI · 제목 낱말 · "Kawaguchi" 로 `litdb/` grep — 이 논문 카드 없음.  이름이 나오는 곳은 같은 묶음의 `nakamura2020_…` 뿐 · `huang2022_li2sis3_anomalous_conductivity_bvse` 의 "Kawaguchi RSI 2017" 은 다른 논문 (방사광 빔라인).
- 교차 인용 확인 (Nakamura 2020 원문 텍스트 층): 공정 조건의 출처 [25,28] · 비파쇄 = 앞선 연구 [25] 의 최적화 · 고체 농도 ≈1 vol% · 반데르발스 응집 서술 · [28] 의 서지 — 위 본문에 그 쪽수와 함께 적었다.
- Fig 2 · 5 · 6 · 7 크롭을 다시 열어 §3-1 (입도 구간) · §3-5 (Fig 5c 곡선 순서) · §3-6 (화살표 방향) · §10-4 (Fig 7 패널 표지 · "fragtion" 위치) 를 고쳤다 (같은 날).

## 🔗 관련 카드
- 같은 그룹: `nakamura2020_dry_coating_ncm_li3ps4_core_shell`.
- SE 건식 코팅: `lee2026_lpscl_coating_thickness_ncm811` · `lee2026_mechanical_halogen_argyrodite_drycoating` (1저자 공저) · `kim2025_conductive_agent_se_coating_cathode` · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` · `choi2026_bzox_dry_zro2x_nmc_shell_coating`.
- 혼합 장치 DEM: `frankenberg2024_dem_high_intensity_mixer_assb` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `jadidi2023_dem_batch_solid_mixers_review`.
- SE 기계 물성: `sakuda2013_sulfide_mechanical_property`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
