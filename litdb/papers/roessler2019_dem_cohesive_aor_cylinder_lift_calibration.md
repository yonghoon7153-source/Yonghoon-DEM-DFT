<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = alizadeh2018_dem_adhesion_calibration_segregation_heap.md · coetzee2017_dem_calibration_review.md.
     쪽 표기 = "p.N" (PDF N 쪽 = 인쇄 104+N · Particuology 45, 105–115).
     값 표지: [인쇄] = 본문 · 표 · 그림 안에 숫자로 인쇄된 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv) · [우리 산술] = 인쇄값 (또는 우리 생성기 함수) 으로 다시 한 계산 · [미확인] = 원문 (본문 전수) 에 없음 · [추정] = 우리 해석.
     원문 = 본문 11 쪽 (SI 없음) — 텍스트 층 전수 + 식 (1)–(3) 400 dpi 렌더 대조 · 그림 17 · 표 3 = 크롭 20 장 전부 열람. -->

# **LIGGGHTS SJKR 의 cohesionEnergyDensity (CED) 를 원통 인양 시험으로 보정** — 점착 분말 (젖은 모래 9.5 wt% 수분) 은 안식각이 40–84° 로 재현되지 않으니, 대신 **기둥이 서 있다 → 볼록하게 휜다 → 무너진다** 의 상 전이와 슬라이스별 지름 (상대 굽힘) 을 기준으로 · 상 전이는 인양 속도 (8 · 100 mm/s) 와 원통 크기 (C1 · C2.5) 에 무관 (상대 간극 21 · 32 · 43 · 75 %) · 8 × 8 × 9 격자에서 **μ_p 0.5 · μ_r 0.9 · CED 520,000 J m⁻³** (윤곽 오차 4.4 %) — Roessler · Katterfeld (Particuology 2019)

> slug `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` · DOI `10.1016/j.partic.2018.08.005` · type `DEM (LIGGGHTS 3.01, Hertz–Mindlin + simplified JKR cohesion = cohesionEnergyDensity × contact area, EPSD rolling friction) + exp (lifted-cylinder angle-of-repose test on wet sand) — cohesive calibration` · PDF `4ac47ba6-42._DEM_parameter_calibration_of_cohesive_bulk_materials_using_a_simple_angle_of_repose_test.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *DEM parameter calibration of cohesive bulk materials using a simple angle of repose test* (p.1)
> **저자**: Thomas Roessler (교신, throessl@ovgu.de) · André Katterfeld — Chair of Material Handling, Institute of Logistics and Material Handling Systems, University of Magdeburg, Germany (p.1)
> *Particuology* **45** (2019) 105–115 · 접수 2018-01-11 · 수정 2018-06-28 · 승인 2018-08-16 · 온라인 2019-01-25 (p.1).
> **판독 원자료**: `litdb/figures/roessler2019_dem_cohesive_aor_cylinder_lift_calibration/digitized.csv` · 크롭 20 장 `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 이종기술 논지 (`docs/hetero_thesis.md`) **D3** (SE 분말 점착 실험 앵커 + 같은 짝의 DEM 보정 런) 에 대해 — **우리 믹서 덱과 같은 코드 · 같은 점착 매개변수 (LIGGGHTS `cohesionEnergyDensity`, SJKR)** 를 실험으로 보정한 절차.  1저자 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` B5-1 (★★★) · 그 목록 §2 "읽는 순서 9" (Roessler 2019 + Geldart 2006 = D3).

> ★★ **한 줄로 왜 중요한가**: 우리 `scripts/make_mixer_deck.py` 의 `fix … property/global cohesionEnergyDensity peratomtypepair` 는 **이 논문이 보정한 바로 그 매개변수** 다 (힘 = CED × 겹침 접촉 원 면적).  이 논문은 (i) **점착 분말에는 안식각이 앵커로 쓸모없다** (같은 시료 세 번에 40.4–84.3°) 는 것과 (ii) 대신 **원통을 들어 올릴 때 기둥의 상 전이 · 굽힘 윤곽** 이 재현성 있고 크기 · 속도에 무관한 보정 기준이라는 것을 보이고, (iii) 그 기준으로 CED 를 **±10 % 안** 에서 가른다 (450,000 = 너무 일찍 무너짐 · 550,000 = 안 무너짐).
> ⚠ 단 시료가 **젖은 모래 (액체 다리)** · DEM 입자 5.5–12.7 mm (실제 d50 ≈ 0.5 mm 의 10–25 배) · G 를 실제의 1/900 로 낮춤 · 최적 μ_r 이 **격자 끝 (0.9)** · 시간 간격이 표기 ("Rayleigh 의 ≈10 %") 와 달리 Rayleigh 시간의 45–103 % [우리 산술] — **절차는 옮기고 값은 옮기지 않는다.**

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 젖은 모래 (수분 9.5 wt% · 최대 3.15 mm · 벌크 밀도 1250 kg m⁻³) 를 원통 (C2.5: 지름 250 · 높이 375 mm) 에 채워 들어 올리면 안식각은 40.4–84.3° 로 흩어지지만, **간극 h ≈ 80 mm 까지 서 있는 기둥 → 140 mm 까지 균열과 함께 볼록하게 휨 (z 20 mm 에서 상대 굽힘 ≈ 24–26 %) → 160 mm 에서 무너지기 시작 → 280 mm 에서 정지** 의 상 전이는 세 번 모두 같고, 인양 속도 (8 · 100 mm/s) · 원통 크기 (C1 100 × 150 mm) 에도 상대 간극 (21 · 32 · 43 · 75 %) 으로 같다.  LIGGGHTS (Hertz–Mindlin + SJKR + 탄소성 구름마찰) 에서 μ_p · μ_r · CED 를 8 × 8 × 9 격자로 훑어 슬라이스 지름 윤곽을 자동 비교하니 **μ_p 0.5 · μ_r 0.9 · CED 520,000 J m⁻³** 가 윤곽 오차 2.7–6.3 % (평균 4.4 %) 로 가장 잘 맞고 붕괴 시점도 맞았다 [인쇄 p.9–10].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① **D3** — 점착 분말의 실험 앵커로 안식각을 써도 되나? | **안 된다 (점착이 강하면)** — 같은 젖은 모래 세 번에 사면각 40.4 · 52.3 / 54.9 · 84.3 / 52.1 · 48.6°.  더미 윤곽도 재현 안 됨 | [인쇄] p.5 · Fig 7 |
| ② 그러면 무엇을 재나? | **원통 인양 중 기둥의 상 전이 간극 + 슬라이스 지름 (상대 굽힘 y_rel = (y − D)/D)**.  상 전이는 속도 · 원통 크기 무관 (상대 간극 기준) — 작은 시험 장치 · 빠른 DEM 인양이 허용된다 | [인쇄] 식 (6) · p.6–7 · Fig 8–12 |
| ③ 우리 덱의 **CED 와 같은 매개변수**? | **같다** — LIGGGHTS 단순 JKR: F_coh = CED · A (A = 두 구 교차 원 면적, 식 3).  점착 매개변수가 **하나 (CED, J m⁻³)** 라 보정이 단순 · 계산비는 Luding 모델의 1/1.2 · EEPA 의 1/2 (Klama 2017) | [인쇄] 식 (3)–(5) · p.2–3 |
| ④ 그들 CED 를 **우리 Bond 수** 로 바꾸면? | 우리 생성기 정의 (SJKR 평형 겹침 점착 힘 ÷ 자기 무게, `bond_for_ced`) 로 CED 520,000 · G 10⁸ Pa · ν 0.3 · ρ 2083 · d 5.5 / 8 / 12.7 mm ⇒ **Bo ≈ 1.02 / 0.70 / 0.44** · 보정 창 460,000–540,000 ⇒ d 8 mm 에서 Bo 0.49–0.79 [우리 산술].  우리 LC 의 SE–SE **Bo 0.212** (CED ≈ 1.05 × 10⁴ J m⁻³ — SE 반경 75.7 µm · E 10⁷ Pa) 와 **같은 자릿수** | [우리 산술] |
| ⑤ 보정의 **식별성**? | CED 는 기둥 붕괴 · 굽힘으로 **±10 % 안** 에서 갈린다 (450k 이미 붕괴 · 550k 굽힘 없이 버팀).  마찰 둘은 약하게 — 최적 **μ_r 0.9 = 격자 상한** (최적이 격자 밖일 수 있다) · 예비 탐색은 두 마찰 모두 0.9 고정 | [인쇄] p.9 · Table 3 · [우리 산술] |
| ⑥ **강성 연화 · 입자 확대** 의 영향? | G 를 실제 모래 (≈ 90 GPa) 의 **1/900 (10⁸ Pa)** 로 낮춤 — 저자 스스로 "더 높은 G 로 옮기면 접촉 매개변수를 다시 보정해야" · 확대 (5.5–12.7 mm) 는 "시험이 장치 크기에 무관하니 영향 작다" (논증 약함 §10) | [인쇄] p.8 · [추정] |
| ⑦ 점착 메커니즘 분류 (우리 SE 는 어디?) | Rumpf 1958 표 — 물질 다리 없음 (정전기 · 반데르발스 · 원자가) / 액체 다리 (자유 액면 = 모세관 · 계면력, 움직이지 않는 결합제) / 고체 다리 (소결 · 결정 성장 · 결정화).  이 논문 = **액체 다리** · 우리 건식 SE = **물질 다리 없음 (반데르발스 · 정전기)** [추정] | [인쇄] Table 1 |

⛔ **한정어 (떼지 말 것)**: ① 시료 = **젖은 모래** (모세관 · 점성) — 건식 µm 분말의 반데르발스 점착과 기전이 다르다 ② DEM = **거친 확대 입자 (5.5–12.7 mm)** + **G 1/900** — CED 값은 이 입경 · 강성 · 밀도 조합에서만 뜻이 있다 ③ **단일 시험 · 단일 수분** (저자: 다른 수분 · 재료로 판별력 검증 필요) ④ 시간 간격 표기 불일치 (§3-6).

---

## 1. 한 줄 요약

**비점착 분말의 표준 보정 시험 (원통 인양 안식각) 을 점착 분말에도 쓰되, 정적 안식각 대신 인양 중 "기둥이 서 있다가 → 볼록하게 휘다가 → 무너지는" 상 전이와 기둥 윤곽을 보정 기준으로 바꾼 논문.**  실험: 젖은 모래 · 두 원통 (C1 100 × 150 mm 강관 · C2.5 250 × 375 mm 플라스틱관) · 인양 속도 8 · 100 mm/s → 상 전이 4 개가 재현되고 상대 간극 (21 · 32 · 43 · 75 %) 으로 크기 · 속도에 무관.  DEM: LIGGGHTS 3.01 · Hertz–Mindlin (no slip) + **단순 JKR (CED × 접촉 면적)** + Wensrich–Katterfeld 탄소성 구름마찰 · 입자 1 만 개 (5.5–12.7 mm) · 예비 13 런 (CED 0–600,000 / 50,000) 으로 창을 좁힌 뒤 **576 조합** (μ_p · μ_r 0.2–0.9 / 0.1 · CED 460,000–540,000 / 10,000) 을 슬라이스 지름 자동 비교로 골라 μ_p 0.5 · μ_r 0.9 · CED 520,000 J m⁻³.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| T. Roessler (교신) · A. Katterfeld (Univ. Magdeburg) | *Particuology* 45 (2019) 105–115 | 10.1016/j.partic.2018.08.005 | **젖은 모래** (수분 9.5 wt% · 최대 3.15 mm · 벌크 1250 kg m⁻³ · 모래–강 벽마찰 0.35 · 모래–플라스틱 0.37) | **DEM 보정 방법** (LIGGGHTS 3.01) + **실험** (원통 인양 안식각 · 상 전이 · 윤곽) |

> ★ **계보**: Katterfeld 그룹 (Magdeburg) 의 보정 계열 — Gröger & Katterfeld 2006 · 2007 · **Wensrich & Katterfeld 2012** (구름마찰로 모양 대리 — 이 논문의 구름마찰 모델) · **Roessler & Katterfeld 2016** (ICBMH, 안식각 시험의 크기 확장성 — 마른 모래에서 원통 크기는 안식각에 영향 없고 인양 속도는 안식각을 낮춘다).  정본 [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md) 의 "Roessler & Katterfeld [133]" (크기 스케일 불변 · 인양 속도 의존) 서술이 이 2016 선행 연구와 같은 내용이다 [추정 — 그 리뷰의 [133] 원문은 미대조].
> ★ 점착 모델 계보: Kloss 2012 (LIGGGHTS SJKR) · Behjani 2017 (액체 다리 = SJKR + 낮은 반발계수 · 같은 날 카드 [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) 의 응집수 원전) · Luding 2008 (정본 [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md)).

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 점착 모델 (식 1–5 · Fig 1 · p.2–3)
| 항목 | 값 · 식 | 표지 |
|---|---|---|
| JKR (원문 인용) | **F_all = F_ext + 3WπR + √(3πWR·F_ext + (3πWR)²)** (식 1, 인쇄 그대로) | [인쇄] 식 (1) |
| ⚠ 식 (1) 대조 | JKR 원전의 겉보기 하중은 P₁ = P + 3γπR + √(**6**γπRP + (3γπR)²) (정본 [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) 식 19) — 근호 안 첫 항의 계수 **3 ↔ 6** | [우리 산술] |
| 접착일 | **W = γ₁ + γ₁ − γ₁,₂** (식 2, 인쇄 그대로) — Dupré 식은 γ₁ + **γ₂** − γ₁₂ (조판 오기) | [인쇄] 식 (2) |
| LIGGGHTS 단순 JKR | **F_cohesion = CED · A** · A = πa² = (π/4d²)·(4d²R₁² − (d² − R₂² + R₁²)²) (두 구 교차 원) | [인쇄] 식 (3)–(5) |
| 장점 · 한계 (저자) | 매개변수 하나 · 계산 싸다 · **강한 다짐 · 응력 이력 표현 못 함** (하중을 빼면 거의 원 상태로 돌아감) → 호퍼 · 사일로 다짐엔 Luding · EEPA 권장 · 계산비: Luding +20 % · EEPA +100 % (Klama 2017) | [인쇄] p.2 |
| 액체 다리 표현 | 표면장력 = SJKR · 점성 소산 = **낮은 반발계수** (Behjani 2017) · Tabor 기준 (거칠고 단단한 접촉) 은 이 접촉에 해당 없음 | [인쇄] p.2 |

### 3-2. 실험 (§Experimental · Fig 4–12 · p.3–7)
| 항목 | 값 | 표지 |
|---|---|---|
| 원통 C1 | **지름 100 · 높이 150 mm** · 강관 · 인양 **8 mm/s 고정** | [인쇄] p.4 |
| 원통 C2.5 | C1 의 **2.5 배** (250 × 375 mm) · 플라스틱관 · 인양 **2–200 mm/s** 가변 · 시험 = 8 · 100 mm/s | [인쇄] p.4 |
| 높이/지름 | 1.5 (둘 다) | [인쇄] p.4 |
| 시료 | 마른 모래 + 물 → **수분 9.5 wt%** · 최대 입경 3.15 mm · PSD Fig 6 (d50 ≈ 0.45–0.5 mm [판독]) · **벌크 밀도 1250 kg m⁻³** (3 회 이상 평균) · 벽마찰 강 **0.35** · 플라스틱 **0.37** (Jenike 벽마찰 시험기) | [인쇄] p.5 · [판독] Fig 6 |
| 측정 | 슬라이스 높이 z = **{20, 40, 80, 120} mm** (C2.5) · **{8, 16, 32, 48} mm** (C1) 의 기둥 지름 y · C2.5 는 20 mm · C1 은 8 mm 들 때마다 · **y_rel(z) = (y(z) − D_cyl)/D_cyl** (식 6) | [인쇄] p.3–4 · 식 (6) |
| 안식각 (세 번) | **40.4 ; 52.3° · 54.9 ; 84.3° · 52.1 ; 48.6°** (좌 ; 우 사면) — "정량 보정에 부적합" | [인쇄] Fig 7 · p.5 |
| 상 I — 선 기둥 | h ≈ **80 mm** 까지 굽힘 없음 | [인쇄] p.5 |
| 상 II — 볼록 굽힘 | 균열과 함께 휨 · h ≈ **140 mm** 에서 최대 · z 20 mm 상대 굽힘 **≈ 26 %** (본문) / **≈ 24 %** (Fig 10 판독) | [인쇄] p.5 · [판독] |
| 상 III — 붕괴 시작 | h ≈ **160 mm** · 불규칙하게 퍼짐 · 160–280 mm 반복 | [인쇄] p.5 |
| 상 IV — 정지 | h ≈ **280 mm** | [인쇄] p.5 |
| 상대 굽힘 (Fig 10) | h 80: 2 · 1 · 0 % · h 100: 5 · 4 · 1 % · h 120: 12.5 · 11 · 5 % · h 140: 24 · 20.5 · 11 · 2 % (z 20 · 40 · 80 · 120) | [판독] |
| 속도 무관 | 8 ↔ 100 mm/s 에서 같은 h 에 같은 상 (상 III 의 떨어진 재료 정착만 다름) | [인쇄] p.6 · Fig 11 |
| 크기 무관 | 상대 간극 (h ÷ 원통 높이) **20 % (상 I) · 32 % (II) · 43 % (III) · 75 % (IV)** 로 두 원통 같다 | [인쇄] p.7 · Fig 12 · [우리 산술] 21 · 32 · 43 · 75 % |
| ⚠ 경과 시간 서술 | "8 mm/s: 10 s (상 III) · 16.25 s (상 IV) · 100 mm/s: 1.6 s (III) · 2 s (IV)" — 일정 속도면 160 · 280 mm 에 **20 · 35 s · 1.6 · 2.8 s** 여야 한다 (10 s · 16.25 s ⇔ 80 · 130 mm) | [인쇄] p.6 · [우리 산술] |

### 3-3. DEM 설정 (Table 2 · §DEM calibration · p.7–9)
| 항목 | 값 | 표지 |
|---|---|---|
| 코드 | **LIGGGHTS 3.01** (오픈소스) | [인쇄] p.7 |
| 접촉 | **Hertz–Mindlin (no slip)** + **단순 JKR 점착 (CED)** | [인쇄] Table 2 |
| 구름마찰 | **수정 탄소성 스프링–대시포트** (Wensrich & Katterfeld 2012) | [인쇄] Table 2 |
| 입경 (확대) | **5.5–12.7 mm** (본문은 'Fig. 4' 를 가리키나 PSD 는 Fig 6) · 실제 d50 ≈ 0.5 mm 의 **≈ 10–25 배** [판독 · 우리 산술] | [인쇄] p.8 |
| 입자 수 | **10,000** | [인쇄] p.8 |
| 입자 밀도 | **2083 kg m⁻³** (벌크 1250 을 맞추려고) | [인쇄] Table 2 |
| 전단탄성률 | **10 × 10⁷ Pa (= 10⁸)** — 실제 모래 알갱이 ≈ **90 GPa** (Daphalapurkar 2011) 의 **1/900** | [인쇄] Table 2 · p.8 · [우리 산술] |
| 포아송비 · 반발계수 | 0.3 · **0.2** (근사 — 낮은 반발 = 점성 소산 대리) | [인쇄] Table 2 |
| 입자–벽 마찰 | 0.35 (실험) | [인쇄] Table 2 |
| 시간 간격 | **4.4 × 10⁻⁵ s** "≈ Rayleigh 시간의 10 %" | [인쇄] Table 2 |
| ⚠ 시간 간격 점검 | 표의 G · ρ · ν 로 Rayleigh 시간 = πR√(ρ/G)/(0.1631ν + 0.8766) = **4.3 × 10⁻⁵ (5.5 mm) · 6.2 × 10⁻⁵ (8 mm) · 9.8 × 10⁻⁵ s (12.7 mm)** ⇒ 이 dt 는 **103 · 71 · 45 %** — "10 %" 와 맞지 않는다 (가장 작은 구에서 안정 한계 근처) | [우리 산술] |
| 절차 | 생성 → 중력 정착 (평균 속도 < 0.5 mm/s) → 원통 일정 속도 인양 → 간극 280 mm 에서 종료 · 정착 | [인쇄] p.8 · Fig 13 |
| 예비 탐색 | μ_p = μ_r = **0.9 고정** · CED **0 → 600,000 J m⁻³ (50,000 간격)** — 본문 "12 런" (0 포함하면 13 [우리 산술]) · 450,000: h 120 에서 **이미 붕괴** · 550,000: 160 에서 **아직 안 무너지고 굽힘도 없음** ⇒ 그 사이 | [인쇄] p.9 · Fig 14 |
| 본 탐색 (Table 3) | μ_p **0.2–0.9 (0.1)** · μ_r **0.2–0.9 (0.1)** · CED **460,000–540,000 (10,000)** = **576 조합** [우리 산술] | [인쇄] Table 3 |
| 자동 비교 | 슬라이스 z {20, 40, 80, 120} mm 지름 (서로 수직인 두 지름 평균) 을 h 80 · 100 · 120 · 140 mm 에서 실험과 비교 → 오차 최소 조합 → 붕괴 간극 확인 | [인쇄] p.9 · Fig 15 |
| **최적** | **μ_p 0.5 · μ_r 0.9 · CED 520,000 J m⁻³** · 윤곽 오차 **2.7 (h 80) · 2.9 (100) · 6.3 (120) · 5.4 % (140) · 평균 4.4 %** · 상 III (붕괴 시작) 도 맞음 · 원뿔대 모양은 안 맞음 | [인쇄] p.9–10 · Fig 16 · 17 |

### 3-4. 우리 생성기 Bond 수로 환산 [우리 산술 — `scripts/make_mixer_deck.py` 의 `bond_for_ced` · `overlap_for_ced` · `ced_for_bond` 를 그대로 호출]
| 경우 | CED (J m⁻³) | 반경 | E (Pa) | ρ (g cm⁻³) | Bo (점착 힘 ÷ 무게) | 평형 겹침 δ/r |
|---|---|---|---|---|---|---|
| Roessler 최적 · d 5.5 mm | 520,000 | 2.75 mm | 2.6 × 10⁸ (= 2G(1+ν)) | 2.083 | **1.02** | 0.015 % |
| Roessler 최적 · d 8 mm | 520,000 | 4 mm | 2.6 × 10⁸ | 2.083 | **0.70** | 0.015 % |
| Roessler 최적 · d 12.7 mm | 520,000 | 6.35 mm | 2.6 × 10⁸ | 2.083 | **0.44** | 0.015 % |
| Roessler 창 하 · 상한 · d 8 mm | 460,000 · 540,000 | 4 mm | 2.6 × 10⁸ | 2.083 | **0.49 · 0.79** | — |
| 우리 LC SE–SE | **1.05 × 10⁴** | 75.7 µm (1 µm × CGF 151.4 / 2) | 1.0 × 10⁷ | 2.00 | **0.212** | — |
| 우리 SE 가 Bo 3.0 · 38.4 이려면 | 2.53 × 10⁴ · 5.91 × 10⁴ | 75.7 µm | 1.0 × 10⁷ | 2.00 | 3.0 · 38.4 | — |

- 같은 반경 · 강성에서 **Bo ∝ CED³** (생성기 docstring) — 그래서 CED ±8 % 창이 Bo **×0.7–1.1** 이고, "450k 붕괴 · 550k 버팀" 의 판별은 Bo 로 **×1.4** 범위다.
- ⚠ 이 환산은 우리 Bo 정의 (점착 지배 · 단일 접촉 평형 겹침 힘) 를 그들 입자에 적용한 것 — 그들 논문에는 Bo 가 없다.  **절대값 비교가 아니라 "같은 자릿수 (Bo ~ 0.4–1)" 라는 감각만** 옮긴다.

### 3-5. 점착 메커니즘 표 (Table 1 · Rumpf 1958)
- **물질 다리 없음**: 정전기 인력 · 반데르발스 힘 · 원자가 결합.
- **물질 다리 — 액체 다리**: 자유 액면 (모세관력 · 계면력) · 움직이지 않는 결합제 다리 (결합제 · 접착제 · 흡착층).
- **물질 다리 — 고체 다리**: 소결 · 결정 성장 · 결정화.

### 3-6. ★ 우리 산술 · 정합 점검 묶음
① **식 (1)** 근호 안 3πWRF_ext ↔ JKR 원전 6γπRP (정본 `johnson1971_…` 식 19).  ② **식 (2)** γ₁ + γ₁ − γ₁,₂ ↔ γ₁ + γ₂ − γ₁₂.  ③ **dt 4.4 × 10⁻⁵ s** = Rayleigh 시간의 45–103 % (≠ "≈ 10 %").  ④ **경과 시간** 서술 ↔ 일정 속도 · 상 간극 불일치 (§3-2).  ⑤ **z 20 mm 상대 굽힘** 본문 26 % ↔ Fig 10 ≈ 24 %.  ⑥ **예비 런 수** "12" ↔ 0–600,000 / 50,000 = 13 값.  ⑦ **교차 참조** 'Fig. 4' (입경) ↔ 실제 Fig 6.  ⑧ **최적 μ_r = 0.9 = 격자 상한** — 최적이 격자 밖에 있을 수 있다 (같은 값으로 예비 탐색을 고정한 것과 겹친다).
⇒ 결과 (μ_p 0.5 · μ_r 0.9 · CED 520,000) 는 **이 격자 · 이 dt · 이 입경에서의 최적** 으로만 읽는다.

---

## 4. ★ 방법 — 시험 · DEM · 보정 · 입자 처리

### 4-1. 시험 논리 (p.3)
원통 인양 시험을 **무구속 일축 압축 시험 (σ_c 측정) 의 가장 약한 판** 으로 본다 — 다짐 하중 없이 자기 무게만으로 기둥이 서고 휘고 무너진다.  일축 시험은 다짐 응력 σ₁ 을 준 뒤 측면 벽을 빼고 하중을 올려 붕괴 응력 σ_c 를 얻는데 (Fig 2, Chen 2017), 이 시험은 σ_c 대신 **붕괴 간극 · 굽힘 윤곽** 을 잰다.  수분이 늘면 진자 → 깔때기 → 모세관 상태로 결합 강도가 오른다 (Chen & Roberts 2018).

### 4-2. DEM 보정 알고리즘 (Fig 15)
매개변수장 (μ_p · μ_r · CED) → 각 조합의 런 → h 80 · 100 · 120 · 140 mm 에서 슬라이스 지름 → 실험과 차이 → 최소 오차 조합 → 붕괴 간극 대조.

### 4-3. ★ 입자 처리 (우리 축 언어로)
- **강체 구 DEM** (확대 5.5–12.7 mm · 1 만 개) · 모양 = 구름마찰 대리 · 소성 없음 · 형상 불변.
- 점착 = **SJKR (CED × 교차 원 면적)** — 우리 믹서 덱과 **같은 모델** · 액체 다리의 점성 = 낮은 반발계수.
- 강성 = **G 1/900** (시간 간격 때문).

### 4-4. 기법 미니 용어집
- **원통 인양 안식각 시험 (lifting cylinder / pull-up test)** — 원통에 분말을 채우고 들어 올려 생긴 더미의 사면각을 재는 표준 시험.
- **상대 굽힘 y_rel** — 기둥 슬라이스 지름이 원통 지름보다 몇 % 넓은가.
- **상대 간극** — 인양 높이 ÷ 원통 높이 (크기 무관 비교용).
- **SJKR (simplified JKR)** — LIGGGHTS 점착: 힘 = CED × 접촉 면적.
- **EPSD 구름마찰** — 구름 저항을 탄소성 스프링–대시포트로 모델 (Wensrich & Katterfeld).
- **Rayleigh 시간** — 레일리 파가 입자를 가로지르는 시간 · DEM 시간 간격의 기준.

---

## 5. Figure set ★ (크롭 20 장 = `litdb/figures/roessler2019_dem_cohesive_aor_cylinder_lift_calibration/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| Table 1 | Rumpf 1958 점착 메커니즘 분류 | ★ 우리 SE 점착을 어느 칸에 둘지 (물질 다리 없음 [추정]) |
| 1 | 점착 Hertz 접촉의 접촉 반경 기하 (R₁ · R₂ · d · a) | ★ 식 (3) 교차 원 면적 = 우리 SJKR 면적 |
| 2 | 일축 압축 시험 (σ₁ → 벽 제거 → σ_c) | D3 대안 시험 |
| 3 | 기둥 형성 · 슬라이스 높이 z · 간극 h 정의 | ★ 측정 규약 |
| 4 | 시험대 (C1 · C2.5, 모터 · 도르래) | 장치 |
| 5 | 수분 9.5 wt% 모래 사진 | — |
| 6 | 실험 PSD vs DEM 확대 PSD | 확대 비율 (≈ 10–25 배) |
| 7 | 세 번 반복의 더미 + 사면각 인쇄 (40.4–84.3°) | ★★ "점착 분말은 안식각이 재현 안 된다" 의 증거 한 컷 |
| 8 | 상 I–IV (세 반복) | 상 전이 재현성 |
| 9 | 볼록 굽힘 진행 + 슬라이스 선 | 윤곽 측정 |
| 10 | 상대 굽힘 vs 높이 (h 80–140 mm) | ★ 보정 표적 곡선 |
| 11 | 인양 속도 8 ↔ 100 mm/s 의 상 | 속도 무관 |
| 12 | 원통 C2.5 ↔ C1 의 상 (상대 간극) | ★ 크기 무관 |
| 13 | DEM 절차 (a–f) · 속도 색 | DEM 시험 재현 |
| 14 | 예비 탐색 CED 450,000 ↔ 550,000 | ★ CED 판별력 |
| Table 2 | DEM 일반 매개변수 (dt 표기 점검 §3-6) | 입력 세트 형식 |
| 15 | 매개변수장 · 자동 비교 알고리즘 | ★ 우리 D3 보정 런 설계에 그대로 |
| Table 3 | 탐색 범위 (576 조합) | — |
| 16 | 윤곽 — 실험 vs 최적 DEM | 보정 결과 |
| 17 | 상 I–IV — 실험 vs 최적 DEM | 붕괴 시점 일치 |

## 6. Post-processing ★
- **무엇을**: 영상에서 슬라이스 지름 → 상대 굽힘 · 상 전이 간극 · 사면각 (좌우) · DEM 슬라이스 지름 (수직 두 방향 평균) → 조합별 윤곽 오차 → 최소 조합.
- **도구**: 영상 · 자체 알고리즘 (이름 미기재).
- **안 한 것**: 반복 수 통계 (DEM) · 매개변수 민감도 지도 (576 조합의 오차 분포는 실리지 않음) · 다른 수분 · 재료 · 다른 G · 다른 확대 비율 · 일축 · 전단 시험과의 교차 확인.
- **우리 후처리 (이 카드)**: §3-4 Bo 환산 (우리 생성기 함수) · §3-6 정합 점검 (식 1 · 2 · dt · 시간 · 굽힘 · 런 수 · 교차 참조 · 격자 끝) · Fig 6 · 7 · 10 판독 (digitized.csv).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 코드 · 문서 출처를 병기)

| 항목 | 이 논문 (Roessler 2019) | 우리 (LIGGGHTS 믹서 드럼) | 차이 / 판정 |
|---|---|---|---|
| 코드 · 점착 | LIGGGHTS 3.01 · **SJKR (CED)** | LIGGGHTS · **SJKR (CED, 쌍별 행렬)** (`scripts/make_mixer_deck.py`) | ★★ **같은 모델 · 같은 매개변수** — 이 절차를 그대로 쓸 수 있다 |
| CED 정하는 법 | **실험 (원통 인양 상 전이 · 윤곽) 에 맞춘 보정** | **절대 Bo 목표에서 역산** (`ced_for_bond`) — LC SE–SE 0.212 · LA AM_P 3.0 · LH 38.4 = 내부 기준점 (문헌 앵커 아님) | ★ 우리 CED 는 **실험 앵커가 없다** = D3 의 빈칸 |
| 실험 시료 | 젖은 모래 (액체 다리) | (계획) LPSCl · NCM 건식 분말 (반데르발스 · 정전기 [추정]) | 기전 다름 — 절차만 전이 |
| 입경 · 확대 | 5.5–12.7 mm (실제의 10–25 배) | 실측 지름 × **CGF 151.4** (SE 1 µm → 151 µm) | 둘 다 확대 — 그들은 "시험이 크기 무관이라 괜찮다", 우리는 Bo 를 지켜 환산 |
| 강성 | G 10⁸ Pa (실제의 1/900) | SE E 10⁷ · AM 1.037 × 10⁹ Pa (÷ 135) | SJKR 에서 점착 힘은 겹침 (→ E) 에 걸리므로 **CED 는 E 와 짝으로만 뜻이 있다** — 그들 경고 = 우리 생성기 주석과 같은 결론 |
| 마찰 | μ_p 0.5 · μ_r 0.9 (보정) · 구름마찰 = 탄소성 스프링–대시포트 (Wensrich–Katterfeld) | μ_s 0.9 · μ_r 0.075 (hare2026 세트) · 구름마찰 = **`rolling_friction cdt`** (일정 방향 토크, `scripts/make_mixer_deck.py` pair_style) | 구름마찰 **모델이 다르다** (EPSD ↔ CDT) — μ_r 값 비교 금지 |
| 반발 | 0.2 (점성 소산 대리) | COR 0.3 | — |
| 보정 판별력 | CED ±10 % (붕괴 / 버팀) · 마찰은 약함 (μ_r 격자 끝) | — | 우리 D3 런 설계 시 **판별력 높은 관측량 (붕괴 간극)** 을 고르는 근거 |

### 7-1. frame[5] — 어느 반쪽을 가졌나
**DEM 입력 보정 (벌크 유동)** 만.  혼합 지표 · 압축 · 전달 · 형상 소성은 없다 → 우리 파이프라인의 **입력 앵커** 단계.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **CED 를 실험에 앵커하는 "같은 코드" 의 선례.**  우리 믹서 CED 는 지금 **절대 Bo 목표에서 역산한 내부 값** 이다 (논지 §3 · 파이프라인 G7–G9).  이 논문은 같은 LIGGGHTS SJKR CED 를 **실험 관측량에 직접** 맞춘다.  → D3: SE 분말 (그리고 NCM) 로 **같은 기하의 작은 시험** (원통 인양 또는 #44 Geldart 형 소량 시험) 을 하고, **같은 CGF · 같은 E 의 DEM 시험 런** 으로 CED 를 맞춘다 — 우리 생성기의 Bo 정의는 그 결과를 **보고 · 비교하는 단위** 로 남긴다.
2. **점착 분말에 안식각은 약한 앵커.**  같은 시료 세 번에 40–84° (Fig 7).  → SE (고점착 예상) 앵커를 안식각 하나로 잡지 말 것.  **판별력 있는 관측량** = 기둥 붕괴 간극 (CED ±10 % 판별) · 굽힘 윤곽.  소량 시료 (공기 민감 · 비싼 SE) 라는 제약에는 C1 (100 × 150 mm) 도 크다 — **같은 상대 간극 원리** 를 더 작은 원통에 쓰는 것이 이 논문의 "크기 무관" 결과가 허락하는 방향 [추정 — 작은 쪽 한계는 시험 안 됨].
3. **CED 는 E · 반경 · 밀도와 짝으로만 뜻이 있다.**  저자 경고: "G 를 바꾸면 다시 보정".  우리 생성기도 같은 이유로 CED 대신 Bo 를 기준으로 쓴다.  → D3 결과를 기록할 때 **(CED, E, R, ρ, 입경 분포)** 를 한 묶음으로 봉인하고, Bo 와 응집수 (같은 날 카드 `alizadeh2018_…` §3-3) 를 함께 적는다 — 어느 불변량을 지키는지가 결과를 바꾼다.
4. **Bo 자릿수 감각.**  젖은 모래 최적 CED 는 우리 정의로 Bo ≈ 0.4–1.0 (§3-4) — 우리 LC SE–SE 0.212 와 같은 자릿수 · Jarray 2019 실험 범위 (0.4–1.7, 같은 날 카드 `jarray2019_…`) 와도 겹친다.  즉 **"점착이 거동을 바꾸기 시작하는" Bo ~ 1 영역** 이다.  → 1 µm 건식 SE 분말이 실제로 이보다 훨씬 큰 Bo 를 가지는지는 **D3 측정 전에는 모른다** — 지금 덱의 0.212 를 "약점착 SE" 의 대표로 쓰지 말 것 (논지 §2-6 · §3 과 같은 결론).
5. **보정 격자의 끝에 최적이 오면 식별 실패 신호.**  μ_r 0.9 = 격자 상한 · 예비 탐색도 0.9 고정.  → 우리 D3 보정 런 등록 때 **격자 끝 최적 = 재탐색 규칙** 을 결과 전에 적는다 (규율 — 결과 보고 창을 옮기지 않기 위해).
6. **시간 간격 · 확대 · 연화의 3 중 근사에 주의.**  dt 가 가장 작은 구의 Rayleigh 시간 수준 (§3-6 ③) · G 1/900 · 입경 10–25 배.  → 우리 덱의 `plan()['dt_by']` (상별 Rayleigh dt) 처럼 **dt 를 가장 작은 · 가장 무른 상에서 정하는** 규칙을 유지 (생성기 주석 — A안 이후 AM_S 가 dt 를 정함).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For wet sand (9.5 wt% moisture), the angle of repose from a lifted-cylinder test scattered between 40.4° and 84.3° in three repetitions, whereas the sequence of column build-up, convex bending and collapse occurred at the same relative gap heights (≈21, 32, 43 and 75 %) for two cylinder sizes and lifting velocities of 8 and 100 mm/s (Roessler & Katterfeld, Particuology 2019)." [인쇄 · 우리 산술 for %]
- "Calibrating the LIGGGHTS simplified-JKR cohesion energy density against the column profile gave μp = 0.5, μr = 0.9 and CED = 520,000 J m⁻³ with a mean profile deviation of 4.4 %." [인쇄 p.9–10]
- "A pre-calibration showed that CED = 450,000 J m⁻³ let the column collapse too early and 550,000 J m⁻³ prevented collapse." [인쇄 p.9]
- ⚠ Table 2 의 "dt ≈ 10 % of Rayleigh time" 와 식 (1) · (2) 는 §3-6 점검 없이 인용하지 말 것.

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **액체 다리 (젖은 모래)** — 건식 µm 분말의 반데르발스 · 정전기 점착으로 값 전이 금지.
2. **식 (1) 계수 (3 ↔ 6)** · **식 (2) (γ₁ 두 번)** — 원전 대조 시 다름 (§3-6).
3. **dt 표기 불일치** — Rayleigh 시간의 45–103 % (≠ 10 %).  안정 한계 근처에서 돈 런일 수 있다 [추정].
4. **최적 μ_r = 격자 상한** · 예비 탐색 마찰 0.9 고정 — 마찰 식별 약함 · 576 조합의 오차 지형 미공개.
5. **"시험이 장치 크기에 무관 ⇒ 입자 확대 영향 작다"** 는 논증의 비약 — 실험의 원통 크기 무관 (거시 규모) 이 DEM 입경 (미시 규모) 무관을 보장하지 않는다 [추정].
6. **G 1/900** — 저자도 다른 G 로 옮기려면 재보정 필요하다고 적음.
7. **경과 시간 서술 불일치** (§3-2) · **굽힘 26 ↔ 24 %** · **런 수 12 ↔ 13** · **교차 참조 Fig 4 ↔ 6**.
8. **단일 수분 · 단일 재료** — 판별력 (다른 점착 수준을 가르는가) 은 시험되지 않았다 (저자 후속 과제).
9. **원뿔대 모양은 DEM 이 재현 못 함** (Fig 17) — 상 III 이후 형상 비교는 정성.
10. **전이 한계** — mm 확대 · 젖은 모래 · 인양 시험 ≠ CGF 151 · 건식 SE · 회전 드럼.  **절차 (관측량 고르기 · 격자 · 자동 비교 · (CED, E, R) 봉인) 만 옮긴다.**

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|
| Behjani, M. A., Rahmanian, N., & Hassanpour, A. (2017). An investigation on process of seeded granulation in a continuous drum granulator using DEM. Advanced Powder Technology, 28(10), 2456–2464. | 응집수 · SJKR + 낮은 반발 (액체 다리) — 카드 없음 (같은 날 카드 `alizadeh2018_…` 가 응집수를 씀) |
| Chen, W., Roberts, A., Williams, K., Miller, J., & Plinke, J. (2017). On uniaxial compression and Jenike direct shear testings of cohesive iron ore materials. Powder Technology, 312, 184–193. | 일축 압축 · Jenike 전단 (D3 대안 시험) — 카드 없음 |
| Chen, W., & Roberts, A. W. (2018). A modified flowability classification model for moist and cohesive bulk solids. Powder Technology, 325, 639–650. | 점착 분말 유동성 분류 — 카드 없음 |
| Grima, A. P., & Wypych, P. W. (2011). Development and validation of calibration methods for discrete element modelling. Granular Matter, 13(2), 127–132. | 점착 석탄 slump 윤곽 보정 — 카드 없음 |
| Kloss, C., Goniva, C., Hager, A., Amberger, S., & Pirker, S. (2012). Models, algorithms and validation for opensource DEM and CFD–DEM. Progress in Computational Fluid Dynamics, 12(2–3), 140–152. | ★ LIGGGHTS SJKR 의 원 문서 — 우리 덱 모델의 출처 · 카드 없음 · ★ 다음 후보 |
| Lommen, S., Schott, D., & Lodewijks, G. (2014). DEM speedup: Stiffness effects on behavior of bulk material. Particuology, 12, 107–112. | 강성 연화가 벌크 거동에 주는 영향 — 카드 없음 |
| Luding, S. (2008). Cohesive, frictional powders: Contact models for tension. Granular Matter, 10(4), 235. | 정본 카드 `luding2008_cohesive_frictional_contact_models` |
| Moreno-Atanasio, R., Xu, B. H., & Ghadiri, M. (2007). Computer simulation of the effect of contact stiffness and adhesion on the fluidization behaviour of powders. Chemical Engineering Science, 62(1–2), 184–194. | 강성 · 점착 연동 — 카드 없음 |
| Morrissey, J. P. (2013). Discrete element modelling of iron ore pellets to include the effects of moisture and fines. Doctoral dissertation, University of Edinburgh. | EEPA — 카드 없음 |
| Rackl, M., & Hanley, K. J. (2017). A methodical calibration procedure for discrete element models. Powder Technology, 307, 73–83. | 보정 절차 (실험계획) — 카드 없음 |
| Roessler, T., & Katterfeld, A. (2016). Scalability of angle of repose tests for the calibration of DEM parameters. In 12th ICBMH 2016. | 선행 (마른 모래 크기 · 속도) — 정본 `coetzee2017_…` 가 같은 내용을 인용 [추정] |
| Rumpf, H. (1958). Grundlagen und methoden des granulierens. Chemie Ingenieur Technik, 30(3), 144–158. | 점착 메커니즘 분류 원전 (Table 1) — 카드 없음 |
| Tomas, J. (2007). Adhesion of ultrafine particles—A micromechanical approach. Chemical Engineering Science, 62(7), 1997–2010. | 미분 점착 미시역학 — 카드 없음 |
| Wensrich, C. M., & Katterfeld, A. (2012). Rolling friction as a technique for modelling particle shape in DEM. Powder Technology, 217, 409–417. | 구름마찰 모델 (이 논문 DEM) — 카드 없음 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 11 쪽 텍스트 층 전수 (pdftotext raw · layout) · 식 (1)–(3) = 400 dpi 렌더 (텍스트 층이 그리스 문자 · 근호를 깨뜨림 — 식 1 의 계수 3 · 식 2 의 γ₁ 두 번 확인).
- 그림 17 · 표 3 = 크롭 20 장 (래스터 = 원본 300 dpi 경계 · 표 = 벡터 텍스트) — 전부 열람.
- 수치 재현: Bo 환산 (우리 생성기 `bond_for_ced` · `overlap_for_ced` · `ced_for_bond` 를 읽기 전용으로 호출) · Rayleigh 시간 · 격자 수 · 상대 간극 · 경과 시간 — scratch (저장 안 함), 결과는 §3-2 · §3-4 · §3-6.
- 정본 litdb 중복 확인: DOI `partic.2018.08.005` · 'Roessler' · 'Katterfeld' · 제목 낱말로 `litdb/` 전수 grep — 원저 카드 없음 (`coetzee2017_…` · `frankenberg2024_…` 가 저자를 언급할 뿐).

## 🔗 관련 카드
- 보정 · 점착: [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (같은 날 · 응집수 · 안식각 보정) · [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (JKR 원전 · SJKR CED 대응식) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) · [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md) · [`molerus1975_theory_of_yield_cohesive_powders`](molerus1975_theory_of_yield_cohesive_powders.md).
- 믹서 DEM: [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) (우리 마찰 세트의 출처) · [`lischka2025_dem_eirich_intensive_mixer_dry_mixing`](lischka2025_dem_eirich_intensive_mixer_dry_mixing.md) · [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) (실험 Bo 범위).
- LIGGGHTS 입문: [`shenouda2020_dem_metal_powder_am_liggghts_tutorial`](shenouda2020_dem_metal_powder_am_liggghts_tutorial.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
