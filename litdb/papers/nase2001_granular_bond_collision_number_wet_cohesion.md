<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = jarray2019_cohesion_driven_mixing_segregation_drum.md · alizadeh2018_dem_adhesion_calibration_segregation_heap.md (같은 날 같은 묶음).
     원문 = 10 쪽 (인쇄 p.214–223) · SI 없음.  쪽 표기 = 인쇄 쪽 "p.N" (PDF n 쪽 = p.(213 + n)).
     ⚠ 텍스트 층의 글꼴 대응이 깨져 있다: ( ) → "Ž .", / → "r", → → "™", ∞ → "`", ° → "8", [ ] → "w x" — 식 (1)–(34) 와 수치는 렌더 (150 dpi) 로 대조했다.
     값 표지: [인쇄] = 본문 · 그림 안 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv · 정밀도는 그 머리) /
     [우리 산술] = 인쇄값 · 인쇄 식으로 한 계산 · 이 논문 밖 값과 엮은 계산 (가정 명시) / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->

# 점착 분체의 두 무차원 수 — **입자 Bond 수 Bo_g = F_c/W** (정지 더미 · 호퍼는 **Bo_g ≈ 1 에서 급변**) 와 **충돌 수 Co = F_c/F_Bagnold** (회전 드럼의 동적 안식각은 Bo_g 로는 전이가 안 보이고 **Co 로 보면** 전이) — 모세관 (액체 다리) 점착 · 유리구 0.5–10 mm · 실험 + 입자 동역학 (DEM) — Nase · Vargas · Abatan · McCarthy (Powder Technology 2001)

> slug `nase2001_granular_bond_collision_number_wet_cohesion` · DOI `[미확인]` (원문에 DOI 인쇄 없음 · 인쇄 PII S0032-5910(00)00398-3) · type `exp + DEM (particle dynamics with capillary liquid-bridge cohesion; granular Bond number and collision number as discrete characterization criteria; static heap, hopper discharge, rotating tumbler; glass, acetate, acrylic beads)` · PDF `1eba5498-34._Discrete_characterization_tools_for_cohesive_granular_material.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Discrete characterization tools for cohesive granular material* (p.214)
> **저자**: Steven T. Nase · Watson L. Vargas · Adetola A. Abatan · J.J. McCarthy\* — Department of Chemical and Petroleum Engineering, University of Pittsburgh, PA, USA (p.214)
> *Powder Technology* **116** (2001) 214–223 · 접수 2000-03-31 · 수정 2000-06-20 · 게재확정 2000-07-21 (p.214) · 지원 = ACS Petroleum Research Fund · Univ. Pittsburgh Central Research Development Fund · NSF (p.222).
> **판독 원자료**: `litdb/figures/nase2001_granular_bond_collision_number_wet_cohesion/digitized.csv` (그림 5 · 6 · 9 · 10 · 11) · 크롭 11 장 `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 우리 믹서 DEM 은 점착 세기를 **Bo_code (SJKR 평형 겹침 힘 ÷ 자기 무게)** 하나로 정의한다 (`scripts/make_mixer_deck.py` `bond_for_ced` · `ced_for_bond`).  이 논문은 "Bond 수 하나로 정지 · 호퍼는 되는데 **회전 드럼은 안 된다** — 드럼에서는 점착 대 **충돌** 힘의 비가 필요하다" 를 실험 + DEM 으로 보인 원전이다.  1저자 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` 의 점착 · Bond 수 축.

> ★★ **한 줄로 왜 중요한가**: (i) **Bo_g ≈ 1** 이 정지 더미 각 · 호퍼 유량의 급변점 (여러 재료 · 실험 + 계산) — 우리 SE–SE Bo_code 0.212 (기준 덱) 는 그 **아래**, LH (38.4) · LU (212 · 637) 는 **위**.  (ii) 그런데 **회전 드럼 (우리 믹서와 같은 장치)** 의 동적 각은 Bo_g 로 수십 배 바꿔도 **뚜렷한 전이가 없다** → 드럼에서는 **Co = 점착력 / Bagnold 충돌력** 이 지배 · Co ∝ 1/ω² — 같은 Bo 라도 **회전 속도 (우리 Fr 밴드)** 가 영역을 바꾼다.  (iii) 점착이 크면 동적 각이 회전이 빨라질수록 **오히려 작아진다** (건조 계와 반대).  (iv) 결론의 마지막 문장: Bo_g · Co 를 같이 조절하면 다분산 혼합물에서 **한 종만 점착** 하게 하거나 한 종이 다른 종에 **선택적으로 붙는 정렬 혼합 (Hersey)** 을 만들 수 있다 — 우리 논지의 질문 그 자체.
> ⚠ 단 점착 = **모세관 (물 다리)** · 입자 = **mm 유리구** · Co 에는 **값이 주어지지 않은 상수 λ²** 가 들어 있어 "Co ≈ 1" 의 위치는 그 선택에 달려 있다 (원문 명시).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 액체 다리 점착을 입자 수준 힘으로 보고 두 무차원 수 — 최대 모세관력 ÷ 입자 무게 (Bo_g = 3γ/(2R²ρ_s g)) 와 최대 모세관력 ÷ Bagnold 충돌력 (Co) — 를 세우면, 정지 더미의 각과 호퍼 유량은 Bo_g ≈ 1 에서 급변하지만 회전 드럼의 동적 각은 Bo_g 에 둔감하고, 대신 (젖음 − 마름) 동적 각 차를 Co 로 그리면 Co ≈ 1 근처 (λ² 선택에 따름) 에서 급변한다 [인쇄 p.218–222].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① Bond 수 정의 | **Bo_g = F_c/W = 2πRγ / ((4/3)πR³ρg) = 3γ/(2R²ρg)** (식 26 — F_c = 최대 모세관력 2πRγ · 접촉각 0) · Buckingham π 의 넷째 묶음과 엮으면 충돌 수 | [인쇄] p.217 |
| ② 정지 · 호퍼의 전이 | 정지 더미 각: Bo_g < 1 ≈ 29–30° (유리 실험) → Bo_g ≈ 2–8 에서 35 → 55° → 60 에서 85° · 호퍼 유량: Bo_g 0.01–0.5 ≈ 285 g/s → 4.5–8 에서 257 → 180 g/s · 두 경우 모두 **Bo_g ≈ 1** 근처에서 급변 ("입자 자기 무게 < 점착력 이면 정지 계가 점착성") | [판독] Fig 5 · 6 · [인쇄] p.218–219 |
| ③ ★ 회전 드럼은? | 동적 각 (구르기 영역 · 임계 회전의 10 %) 은 Bo_g 10⁻³ → 10² 에 23 → 48° 로 **완만** · **뚜렷한 전이점 없음** → 전단 (충돌) 이 중요 → **Co 가 지배 변수** 라고 제안 | [판독] Fig 9 · [인쇄] p.220 |
| ④ ★ 충돌 수 | Co = F_c/F_Bg = 2πRγ / (πρ_sλ²R⁴(du/dy)²) = γδ²/(2λ²ρ_sR³⟨u⟩²) (식 29 · du/dy ≈ 2⟨u⟩/δ) · 드럼: Co = 4γ/(ρ_sλ²R³ω²)·(δ/R_t)⁴ (식 34 · δ/R_t ≈ 0.03, Gilchrist 2D) · **λ² = 값이 주어지지 않은 상수** | [인쇄] p.217 · p.220 |
| ⑤ Co 전이 | (젖음 − 마름) 동적 각 차 vs Co → "Co ≈ 1 근처 급변 (λ² 선택에 따름)" · 우리 판독: 0 에서 떠나는 곳은 Co ≈ 10⁻² · Co ≈ 1 에서 ≈ 4° · 작은 비드 (0.5 · 0.8 mm) 는 9–15.5° 로 위 띠 | [인쇄] p.221 · [판독] Fig 11 |
| ⑥ 회전 속도의 반전 | 마른 계 (10 mm · 2 mm 마름): 회전 ↑ → 각 ↑ · 점착 계 (2 mm 젖음): 회전 ↑ → **각 ↓** ("통념과 반대") · 빠른 회전에서 마른 각에 접근 | [인쇄] p.221 · [판독] Fig 10 |
| ⑦ 우리 믹서에 옮기면 | 우리 SE–SE Bo_code 0.212 (기준) — 정지 기준으론 '자유 흐름' 쪽 · 드럼 기준 (Co) 은 **λ² 를 모르면 절대값이 없다** · 같은 식으로 계산한 Co·λ²: SE–SE 기준 **9.6 × 10⁻⁴** · LU212 **0.96** · LU637 **2.9** · AM_P LH **0.019** · LHx30 **0.58** (δ/R_t = 0.03 가정) | [우리 산술] §3-6 |

⛔ **한정어 (떼지 말 것)**: ① 점착 = **모세관 (펜듈러 액체 다리 · 물 · 액체 0.68 vol%)** — SJKR · 반데르발스 점착이 아니다 ② 입자 = **mm 크기 유리 · 아세테이트 · 아크릴 구** (μm 분말 아님) ③ Co 의 상수 **λ² 값 미기재** — 전이 위치는 그 선택에 달림 (원문 명시) · 식 (29) 와 식 (31) · (34) 사이에 **2 배 차** (§10 항목 2) ④ 드럼 Co 의 δ/R_t ≈ 0.03 = **2D 드럼 실험값** 차용 ⑤ 점성력은 코드에 넣었지만 특성화 (Bo_g · Co) 에서는 **빠졌다**.

---

## 1. 한 줄 요약

**습윤 (모세관) 점착 입자의 거동을 입자 수준 힘 비 두 개 — 입자 Bond 수 (점착 ÷ 무게) 와 충돌 수 (점착 ÷ Bagnold 충돌력) — 로 특성화하고, 정지 더미 · 호퍼 · 회전 드럼 세 장치에서 실험과 DEM 으로 각 수의 전이 (≈ 1) 를 확인한 10 쪽 논문.**  결론: 정지 · 준정지 계는 Bo_g, 충돌이 중요한 흐르는 계 (드럼) 는 Co 가 점착의 중요도를 가른다 — 대규모 실험 없이 a priori 로 "유동성" 을 가늠할 수 있다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| S.T. Nase · W.L. Vargas · A.A. Abatan · J.J. McCarthy\* (Univ. Pittsburgh) | *Powder Technol.* 116 (2001) 214–223 | [미확인] (PII S0032-5910(00)00398-3 인쇄) | 실험: 유리구 지름 0.5–10 mm (아세테이트도) + 물 (계면활성제로 표면장력 38–72.9 mN m⁻¹) · 액체 0.68 vol% / 계산: 소다석회 유리 ρ 2500 kg m⁻³ · E 7.0 × 10¹⁰ Pa · ν 0.25 · 물 점도 · 표면장력은 실험보다 넓게 · "acrylic" · "soft" (acrylic 성질 · E 두 자릿수 작음) | **실험 + DEM (입자 동역학)** |

> ★ **계보**: McCarthy (Pittsburgh) — 드럼 혼합 (Metcalfe · Shinbrot · McCarthy · Ottino 1995 [8] · Gilchrist 등 1999 [42]) · 액체 다리 = Fisher 1926 [26] · Lian · Thornton · Adams [27–29] · 접촉 = Thornton 탄–완전소성 [23] · Walton–Braun 접선 [24, 25] · 점성 = Adams & Perchard [32] · Goldman 등 [33] · 점성 다리 = Ennis · Tardos · **Pfeffer** [36–38] (같은 날 카드 `pfeffer2001_…` 의 제1저자) · 결론의 정렬 혼합 = **Hersey [44]** (같은 날 카드 `hersey1975_ordered_mixing_concept`).

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. 입자 동역학 (DEM) 접촉 모델 (§2.1 · p.215–216 · 식 1–11)
| 식 | 내용 | 표지 |
|---|---|---|
| (1)–(4) | 탄성 적재 **F_n = k_n α^{3/2}** · k_n = (4/3)E\*√R\* · 1/E\* = (1−ν₁²)/E₁ + (1−ν₂²)/E₂ · 1/R\* = 1/R₁ + 1/R₂ · α = (R₁ + R₂) − D₁₂ (겹침) | [인쇄] p.215 |
| (5) | 항복 (F_y = "본질적으로 맞춤 매개변수") 뒤 선형 **F_n = F_y + k_y(α − α_y)** · k_y = (2/3)(F_y/α_y) (Thornton [23]) | [인쇄] p.215 |
| (6)–(7) | 항복 전 제하 = 탄성 · 항복 뒤 제하 **F_n = F_max − k_n√R̄ (α_max − α)^{3/2}** · R̄ = R′/R\* = (F_y/F_max)((2F_max + F_y)/(3F_y))^{3/2} | [인쇄] p.215 |
| (8)–(11) | 접선 (Walton–Braun [24, 25]): F_t = F_t0 − k_t Δs · k_t = k_t0(1 − (F_t − F_t\*)/(μF_n − F_t\*))^γ (증가) · k_t0(1 − (F_t\* − F_t)/(μF_n + F_t\*))^γ (감소) · γ = 1/3 · k_t0 = k_n(1 − ν)/(1 − ν/2) | [인쇄] p.215–216 |

### 3-2. 모세관 · 점성 힘 (§2.2–2.3 · p.216–217 · 식 12–24)
- 표면장력 항 **F_s = 2πRγ sin²β** · 압력 결손 항 F_h = πR²ΔP sin²β (β = 반 채움각 · 접촉각 0 가정) → **F_c = 2πRγ sin²β (1 + H\*)** · H\* = RΔP/(2γ) (무차원 평균곡률) · Laplace–Young 식으로 H\* (식 18–22) [인쇄].
- 다리 파단 거리 **S_c ≈ V^{1/3}** (V = 다리 부피, Lian 등 [27]) · 쌍별 (펜듈러) 가정 · 접촉 때 다리 생성 → S > S_c 까지 유지 · **미리 계산한 표** 로 조회 [인쇄 p.216–217].
- 점성: 법선 F_vn = 6πμR\* v_n (R\*/S) (Adams & Perchard [32]) · 접선 F_vt = ((8/15) ln(R\*/S) + 0.9588)·6πμR\* v_t (Goldman [33]) · 거칠기로 최소 간격 **S_o ≈ 10⁻⁶ m** [인쇄 p.217].
- ⚠ 점성력은 끌림만이 아니라 다리 형성 · 파단을 모두 방해해 **"엄밀히 인력이 아니므로"** 특성화 (Bo_g · Co) 에서 제외 [인쇄 p.217].

### 3-3. ★ 무차원 수 (§3 · p.217 · 식 25–29)
- 변수 (R, ρ_s, γ, ⟨u⟩, ρ_f, g, δ) → Buckingham π 네 묶음: **(δ/R) · (ρ_s/ρ_f) · (γ/(ρ_s g R²)) · (⟨u⟩²/(gR))** (식 25) [인쇄].
- 셋째 묶음 = 최대 모세관력 ÷ 무게 = **입자 Bond 수 Bo_g = 3γ/(2R²ρg)** (식 26) [인쇄].
- 넷째 묶음 + Bo_g + 기하 · 밀도 비 → γδ²/(ρ_sR³⟨u⟩²) (식 27) · 흐름층 전단율 du/dy ≈ 2⟨u⟩/δ (식 28) → **Co = F_c/F_Bg = 2πRγ/(πρ_sλ²R⁴(du/dy)²) = γδ²/(2λ²ρ_sR³⟨u⟩²)** (식 29 — F_Bg = Bagnold 충돌력 · λ² = 상수) [인쇄].

### 3-4. 실험 · 계산 조건 (§4 · p.217–218)
| 항목 | 값 | 표지 |
|---|---|---|
| 실험 입자 | 유리구 지름 **0.5–10 mm** (아세테이트도) | [인쇄] p.217 · 그림 10 · 11 범례 |
| 점착 조절 | 물 + 계면활성제 → 표면장력 **38–72.9 mN m⁻¹** (모세관 상승법) · 그 밖에 입자 크기 · 밀도로 Bo_g 범위 확장 | [인쇄] p.218 |
| 액체량 | **0.68 vol%** (실험 · 계산 같음 · 포화도 효과는 논쟁 중이라 고정) · 매 실험 전 휘저어 미리 섞음 | [인쇄] p.218 |
| 계산 입자 | 소다석회 유리 ρ_s **2500 kg m⁻³** · E **7.0 × 10¹⁰ Pa** · ν **0.25** · 점도 = 상온 물 · 표면장력 = 실험보다 넓게 | [인쇄] p.218 |
| 정지 더미 | 두 플렉시글라스 판 (간격 1 in.) 의 직사각 통 · 바닥 열림 폭으로 느린 배출 | [인쇄] p.218 · Fig 2a |
| 호퍼 | 같은 통 · 바닥 벽 **45°** · 깔때기 흐름 · **6 kg** · 저울 → 선형 질량–시간 | [인쇄] p.219 · Fig 2c |
| 드럼 | 구르기 영역 · 회전 = **임계값 (각가속 = 중력) 의 10 %** · 각 = 비드가 벽에 닿는 두 점 · 여러 번 평균 | [인쇄] p.219–220 · Fig 2b |

### 3-5. 결과 (§4.1–4.3 · p.218–221 · 그림 5 · 6 · 9 · 10 · 11 판독)
| 장치 | 결과 | 표지 |
|---|---|---|
| 정지 더미 (Co → ∞) | Bo_g < 1 ≈ 29–30° (유리) → Bo_g ≈ 2.3 → 35° · ≈ 4 → 39° · 6.5–8 → 52–55° · 60 → 85° · 아세테이트 1.3–9 → 32.7–47.3° · acrylic (계산) 0.36 → 16° · 37 → 67° · **soft (계산) 10 → 62° · 100 → 90°** · 마른 안식각 (점선) ≈ 24° · 전이 ≈ **Bo_g ≈ 1** ("자기 무게 < 점착력 이면 점착성") · Albert 등 [11] 과 정성 일치 | [판독] Fig 5 · [인쇄] p.218–219 |
| 호퍼 (Co 100–25,000 ≫ 1) | 유량 ≈ 285 g/s (Bo_g 0.01 · 0.5) → 257 (4.5) → 242 · 239 (5.8 · 6.3) → **180 g/s (8)** · 전이 ≈ **Bo_g ≈ 1** | [판독] Fig 6 · [인쇄] p.219 |
| 드럼 vs Bo_g | acrylic (계산) 0.0045 → 23° · 0.44 → 35.5° · 유리 (실험) 0.4 → 37° · 72 → 48° · 아세테이트 1.3 → 34.6° · 9.2 → 44.3° — **완만 · 전이점 없음** | [판독] Fig 9 · [인쇄] p.220 |
| 드럼 vs 회전 | 10 mm 젖음 = 마름: 28.0 → 31.5° (1.1 → 6 rpm) · 2 mm 마름: 23.0 → 25.0° · **2 mm 젖음: 28.3 → 26.6°** (1.1 → 3.8 rpm, 감소) | [판독] Fig 10 · [인쇄] p.221 |
| 드럼 vs Co | (젖음 − 마름) 각 차: 10 mm (Co 6 × 10⁻⁴ – 0.017) ≈ 0 · 4 mm 0.02 → 0.8° · 0.26 → 4° · 2 · 1.5 mm (Co 0.2–5) 1.5–6° · 0.8 mm (2.5–35) 9–13° · 0.5 mm (8.5–150) 11.5–15.5° · 원문: "Co ≈ 1 근처 급변 (λ² 선택에 따름)" | [판독] Fig 11 · [인쇄] p.221–222 |

### 3-6. ★ 우리 산술
| 항목 | 값 | 가정 · 출처 |
|---|---|---|
| 유리구 + 물 (γ 72.9) 의 Bo_g = 3γ/(2R²ρg) | 지름 0.5 · 0.8 · 1.5 · 2 · 4 · 10 mm → **71 · 28 · 7.9 · 4.5 · 1.1 · 0.18** (γ 38 이면 × 0.52) | 식 26 · ρ 2500 — 그림 5 의 유리 Bo_g 범위 (0.09–60) 와 맞는다 |
| 식 29 ↔ 식 31 · 34 | 식 29 에 식 30 (호퍼 ⟨u⟩ = Q/(2δW)) · 식 33 (드럼 ⟨u⟩ = ωR_t²/(2δ)) 을 넣으면 각각 **2γδ⁴W²/(λ²ρ_sR³Q²)** · **2γ/(ρ_sλ²R³ω²)(δ/R_t)⁴** — 인쇄 식 31 · 34 는 그 **2 배** (식 27 을 λ² 로 나눈 꼴) | λ² 에 흡수되는 상수 차지만 식을 섞어 쓰면 Co 가 2 배 어긋난다 |
| 우리 드럼 | rpm **75.04** (LC_ref_r2 덱 메타) → ω 7.858 rad s⁻¹ · Fr 0.0827 → 드럼 반지름 **13.14 mm** · ω/ω_c = √Fr = **0.29** (이 논문 = 0.1 — '임계의 10 %' 를 각속도로 읽을 때) | `docs/data/mixer_highbo_dev_decks_20260930_v26/decks/LC_ref_r2_s32452843/deck_meta.json` · `make_mixer_deck.py` `FR_ANCHOR` |
| ★ 우리 Co·λ² (식 34 꼴 · F_c = Bo·W 로 일반화) | Co·λ² = (8/3)·Bo·g·(δ/R_t)⁴/(Rω²) — SE (R 7.57 × 10⁻⁵ m): **4.5 × 10⁻³ × Bo** · AM_S: 1.1 × 10⁻³ × Bo · AM_P (6.81 × 10⁻⁴ m): **5.0 × 10⁻⁴ × Bo** | δ/R_t = 0.03 (2D 드럼 실험값 차용) · 덱의 거친 입자 (CGF 151.4) 반지름 · 식 29 꼴이면 절반 |
| 팔별 | 기준 SE–SE (Bo 0.212) **9.6 × 10⁻⁴** · LU212 **0.96** · LU637 **2.9** · LC AM_P–AM_P (0.00109) 5.5 × 10⁻⁷ · LH (38.4) **0.019** · LHx10 (384) **0.19** · LHx30 (1152) **0.58** | Bo_code 값 = CLAUDE.md · 논지 §2-6 (LU 이름 = SE–SE Bo_code) |
| 해석 | λ² 를 모르니 절대 비교는 안 된다 — 그러나 **같은 λ² 아래 상대 서열** 은 선다: 기준 덱의 SE–SE 는 드럼 기준으로 LU · LHx 계열보다 **3 자릿수** 아래 | [추정] |

---

## 4. ★ 방법 — 입자 처리 · 특성화 논리

### 4-1. ★ 입자 처리 (DEM)
- **강체 구 + Thornton 탄–완전소성 법선 접촉** (항복 힘 F_y = 맞춤 매개변수 · 제하 = 새 접촉 반경 R′) — 접촉 **힘 법칙** 의 소성이지 입자 **형상** 소성이 아니다.
- 점착 = **쌍별 펜듈러 액체 다리** (미리 계산한 표 조회) · 파단 S_c ≈ V^{1/3} · 점성 (법선 · 접선 윤활) · 최소 간격 10⁻⁶ m.
- 그림에 나온 계산 입자: "acrylic" 과 "soft" (acrylic 성질 · E 두 자릿수 작음) — 둘 다 Fig 5 · 9 의 계산 기호 (구체 크기 · 개수 [미확인]).

### 4-2. 특성화 논리
- **정지 계** → 충돌 없음 → Co → ∞ → **Bo_g 하나** (p.218).
- **호퍼** → Co 100–25,000 ≫ 1 (식 31) → 여전히 **Bo_g 가 지배** (p.219).
- **드럼** → δ/R_t ≈ 0.03 로 Co 가 호퍼보다 훨씬 작다 → **Co 가 지배** → 젖음–마름 각 차 vs Co (p.220–221).

### 4-3. 기법 미니 용어집
- **입자 Bond 수 Bo_g** — 최대 점착력 ÷ 입자 무게 (유체역학 Bond 수의 유비).
- **충돌 수 Co** — 최대 점착력 ÷ Bagnold 충돌력 (전단 흐름에서 입자 충돌이 주는 힘).
- **Bagnold 충돌력** — 전단율² 에 비례하는 입자 충돌 응력 × 면적 (F_Bg ∝ ρ_s λ² R⁴ (du/dy)²).
- **펜듈러 상태** — 액체가 입자 접촉점마다 다리로만 있고 서로 이어지지 않은 낮은 포화 상태.
- **반 채움각 β** — 입자 중심에서 본 액체 다리 경계까지의 각.
- **구르기 영역 (rolling regime)** — 드럼 자유 표면이 거의 평평한 연속 흐름 영역.
- **동적 안식각** — 구르기 영역에서 자유 표면의 정상 각.

---

## 5. Figure set ★ (크롭 11 장 = `litdb/figures/nase2001_granular_bond_collision_number_wet_cohesion/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 대칭 액체 다리 — R · β · 목 Y₀ · 경계 Y(x) · 간격 S_tot | 점착 힘 정의의 기하 |
| 2 | 세 장치 — (a) 정지 안식각 α_s (b) 동적 각 α_d (드럼) (c) 호퍼 (흐름 폭 δ · 저울) | ★ 같은 재료를 세 장치로 — 우리 E0 · 회전 런 구분과 같은 축 |
| 3 | 실험 더미 — 마름 · 젖음 (각 α) | — |
| 4 | 계산 더미 — 마름 · 젖음 | — |
| 5 | ★ 정지 더미 각 vs Bo_g (유리 · 아세테이트 실험 · acrylic · soft 계산) · 마른 각 점선 | ★★ Bo_g ≈ 1 전이 · soft 가 같은 Bo_g 에서 더 가파름 (§8 항목 4) |
| 6 | 호퍼 유량 vs Bo_g | Bo_g ≈ 1 전이 (점 6 개) |
| 7 | 실험 드럼 — 마름 · 젖음 (각 β) | 우리 드럼과 같은 장치 |
| 8 | 계산 드럼 — 마름 · 젖음 | — |
| 9 | ★ 동적 각 vs Bo_g — 전이 없음 | ★★ 드럼에서 Bo 만으로는 부족 |
| 10 | 동적 각 vs 회전 (10 mm 젖음 · 마름 / 2 mm 젖음 · 마름) | ★ 점착 계는 회전 ↑ → 각 ↓ |
| 11 | ★ (젖음 − 마름) 각 차 vs Co (0.5–10 mm · low γ) | ★★ Co 전이 — 단 크기별 띠 (§10 항목 3) |

## 6. Post-processing ★
- **원문**: 정지 · 동적 각 = 판 · 벽 접점에서 각도기 측정 · 여러 번 평균 (통계 미기재) · 호퍼 = 저울 질량–시간 기울기 · 계산 = 같은 정의 · 무차원 수 = 손 계산 (λ² 미기재).
- **우리 후처리 (이 카드)**: 그림 5 · 6 · 9 · 10 · 11 판독 (digitized.csv) · 비드별 Bo_g 재계산 · 식 29 ↔ 31 · 34 일관성 확인 · 우리 드럼 Co·λ² (§3-6).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태)

| 항목 | 이 논문 (Nase 2001) | 우리 믹서 DEM | 차이 / 판정 |
|---|---|---|---|
| 점착 | 모세관 다리 (F_c = 2πRγ, **E 무관**) | SJKR (F = CED × 접촉 면적 · 겹침 → **E 의존**) · Bo_code = 평형 겹침 힘 ÷ 무게 | 같은 "점착 ÷ 무게" 지만 힘의 출처가 다르다 — 수치를 같은 축에 놓을 때 표지 필요 |
| Bond 수 | Bo_g ≈ 1 = 정지 · 호퍼 전이 | 기준 SE–SE 0.212 · AM_P LC 0.00109 · LH 38.4 · LU 212/637 | 우리 기준 덱 = 정지 기준으로도 '자유 흐름' 쪽 (논지 §2-6 "사실상 안 붙는 가루" 와 정합) |
| 드럼 지배 수 | **Co** (점착 ÷ 충돌) | 등록 · 판독에 **Co 없음** | ★ 드럼 혼합을 Bo_code 로만 정의 · 비교하면 회전 속도 (Fr) 의 몫이 빠진다 [추정] |
| 회전 | 임계의 10 % · rpm 1–6 (mm 비드 드럼) | Fr 0.0827 (임계의 29 % · 75 rpm · 반지름 13.14 mm) | Co ∝ 1/ω² — Fr 밴드 (0.055–0.086) 안에서도 Co 가 1.5 배 움직인다 [우리 산술] |
| 접촉 힘 법칙 | Thornton 탄–완전소성 + Walton–Braun 접선 | Hertz + 이력 접선 + SJKR + cdt 구름 (`pair_style gran model hertz tangential history cohesion sjkr rolling_friction cdt`) | 소성 접촉 없음 (믹서) |
| 입자 | mm 유리 (E 70 GPa) | 거친 입자 (CGF 151.4) · E 연화 (SE 1 × 10⁷ Pa) | soft 계산 (E 두 자릿수 작음) 이 같은 Bo_g 에서 더 가파른 더미 → 연화 E 가 점착 거동을 바꿀 수 있다 [판독 · 추정] |

### 7-1. frame[5]
DEM (입자 동역학) + 실험 — 우리 쪽 반쪽은 **믹서 DEM 의 점착 · 흐름 영역 정의** (혼합 단계).  압축 · 수송 (frame[5] 의 DEM 수송 · MPM 역학) 과는 직접 관계없다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **드럼에서는 Bond 수만으로 점착 영역을 정할 수 없다 — 충돌 수가 필요하다.**  동적 각은 Bo_g 10⁻³ → 10² 에 완만 · 전이 없음 (Fig 9) · Co 로 보면 전이 (Fig 11).  → 우리 확인 블록 · DEV 팔은 점착을 **Bo_code 하나** 로 등록 · 보고한다 — 드럼 혼합 결과 (M · s1 · s2) 를 해석할 때 **Co (점착 ÷ 충돌)** 를 같이 적어야 "같은 Bo 인데 다른 결과" 를 설명할 수 있다.  Co 는 덤프에서 흐름층 속도 ⟨u⟩ · 두께 δ 를 재면 식 29 로 바로 계산된다 (λ² 하나만 남음) [제안 · 결과 전 등록 대상].
2. **같은 λ² 아래 서열로 보면 기준 덱의 SE–SE 는 드럼에서 '충돌 지배' 다.**  Co·λ²: 기준 SE–SE 9.6 × 10⁻⁴ vs LU212 0.96 · LU637 2.9 · LHx30 (AM_P) 0.58 (§3-6, δ/R_t = 0.03 가정).  → dev-u (LU) 에서 SE–SE 군집이 LC 보다 높게 나온 것 (CLAUDE.md 10-06 판독 · 범위 안 겹침) 은 Co 로 보면 **3 자릿수 다른 영역** 의 비교였다 [추정] — 논지 P1 의 "비코팅에서 SE–SE 응집이 남는다" 를 시험하는 팔은 SE–SE 의 **Co 가 1 근처 이상** 인지부터 확인 (λ² 를 정하는 실험 · 문헌이 먼저).
3. **점착 계는 회전이 빨라지면 각이 작아진다 — Fr 노브의 방향이 점착에 따라 뒤집힌다.**  2 mm 젖음: 1.1 → 3.8 rpm 에 28.3 → 26.6° (마름은 23.0 → 25.0°) (Fig 10).  → 우리 Fr 밴드 (0.055–0.086) 안에서 rpm 을 바꾸는 민감도 시험은 **점착 팔과 비점착 팔에서 반대 방향** 이 나올 수 있다 — 하나의 "Fr 감도" 로 묶지 말 것 [추정].
4. **연화 E 는 같은 Bo 에서도 점착 거동을 바꿀 수 있다.**  soft (E 두 자릿수 작음) 계산 더미는 Bo_g 10 에서 62° — acrylic (Bo_g 18) 38° 보다 가파르다 (Fig 5) — 이 논문의 점착 (모세관) 은 E 와 무관한데도.  → 우리 SE E = 1 × 10⁷ Pa (`E_PHASE`) 는 연화값 — SJKR 은 점착력 자체가 E 에 걸리므로 (면적 ∝ 겹침) 효과가 더 클 수 있다 [추정].  E 감도 (×20 경화 ref 팔) 의 해석에 이 그림을 참고 문헌으로.
5. **Bo_g ≈ 1 은 '정지 계' 의 경계 — 우리 D3 (SE–SE 점착 앵커) 의 실험 설계에 그대로 쓸 수 있다.**  정지 안식각 (Fig 5) · 호퍼 유량 (Fig 6) 은 Bo_g ≈ 1 에서 급변.  → SE 분말의 정지 안식각 · 호퍼 (또는 Hausner) 측정 → Bo 범위 (≪ 1 · ≈ 1 · ≫ 1) 판정 → 덱 Bo_code 의 자릿수 앵커 (논지 D3) — 단 우리 실제 SE (1 µm) 는 반데르발스 점착이라 Bo 가 ≫ 1 일 것이 거의 확실하다 [추정] → **거친 입자 덱의 Bo_code 를 '실제 Bo' 와 같게 둘 수 없다** (CGF 스케일링 · 같은 날 `alizadeh2018_…` · `roessler2019_…` 의 보정 논리와 같은 문제).
6. **결론 문장 = 우리 논지의 질문.**  "Bo_g 와 Co 를 같이 조절하면 다분산 혼합물에서 한 종만 점착하게 하거나, 한 종이 다른 종에 선택적으로 붙어 정렬 혼합을 만들 수 있다 [44]" (p.222).  → 상별 (SE · AM_P · AM_S) Bo · Co 를 표로 같이 적는 것이 이 논문의 문법 — 우리 §3-6 표가 그 첫 판 (λ² · δ 측정 전).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
> 아래 영문은 원문 내용을 **우리가 다시 쓴 문장** 이다 (원문 문장 그대로 아님 — 괄호 쪽이 근거).
- "For capillary-cohesive glass beads, the static heap angle and hopper discharge rate change sharply near a granular Bond number Bo_g = F_c/W ≈ 1 (Nase et al., Powder Technol. 2001)." [인쇄 p.218–219 내용]
- "In a rotating tumbler the dynamic angle shows no clear transition with Bo_g; instead the wet–dry angle difference collapses against a collision number Co = F_c/F_Bagnold, with a transition near Co ≈ 1 subject to an unspecified constant (Nase et al. 2001)." [인쇄 p.220–222 내용]
- "When cohesion is important, the dynamic angle can decrease with increasing rotation rate, contrary to the dry case (Nase et al. 2001)." [인쇄 p.221 내용]
- 원문 구절 (그대로): *"subject to choice of the constant, λ²"* (p.222).
- ⚠ §3-6 의 우리 드럼 Co·λ² (9.6 × 10⁻⁴ … 2.9) 는 [우리 산술 · δ/R_t 가정 · λ² 미정] — 원문 값으로 인용하지 말 것.

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **λ² 미기재** — Co 전이 "≈ 1" 의 위치는 λ² 선택에 달려 있다 (원문 명시) → Co 의 절대값은 이 논문만으로 재현할 수 없다.
2. **식 29 ↔ 식 31 · 34 의 2 배 차** — 식 29 (γδ²/(2λ²ρ_sR³⟨u⟩²)) 에 식 30 · 33 을 넣으면 인쇄 식 31 · 34 의 절반이 나온다 (§3-6) — λ² 에 흡수되지만 식을 섞으면 Co 가 2 배 어긋난다 [우리 산술].
3. **Fig 11 은 한 곡선으로 완전히 모이지 않는다** — 같은 Co ≈ 2.5–5 에서 1.5 mm 비드 ≈ 5–6° vs 0.8 mm ≈ 9–10.5° (3–4° 띠 차) · 0 에서 떠나는 곳은 Co ≈ 10⁻² 근처 (우리 판독) — "Co ≈ 1 급변" 은 그림의 어느 특징을 말하는지 모호하다 [판독 · 추정].
4. **"Co 를 0 으로 둘 수 없다" (p.219) ↔ 정지 계 "Co → ∞" (p.218)** — 호퍼 절의 '0' 은 '∞' 의 오기로 보인다 [추정].
5. **참고문헌 44 의 쪽** — Hersey, Powder Technol. 11 (1975) **149–153** 으로 인쇄 ↔ Hersey 원문 PDF 는 41–44 (같은 날 카드 `hersey1975_ordered_mixing_concept`) [인쇄 · 우리 대조].
6. **입자 · 점착의 전이성** — mm 유리 + 물 다리 (Bo_g 0.09–71) → μm 황화물 분말 (반데르발스 · 정전기) 로 옮길 때 힘의 출처 · 크기 의존 (모세관 F ∝ R vs 무게 ∝ R³ 는 같음) 은 비슷해도 **E 의존 · 거칠기 · 습도** 가 다르다.
7. **드럼 Co 의 δ/R_t ≈ 0.03** = Gilchrist 2D 드럼의 기하 상사 값 — 3D · 배플 · 다른 채움에서는 다를 수 있다 (우리 산술에 그대로 차용 — 4 제곱이라 민감).
8. **점성 제외 · 액체량 고정 (0.68 vol%)** — 다리 부피에 따른 F_c 차이 무시 (결론에서 저자 스스로 인정).
9. **계산 조건 일부 미기재** — 계산 입자 크기 · 개수 · 시간 간격 · F_y 값 · λ² [미확인].

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 11 | R. Albert, I. Albert, D. Hornbaker, P. Schiffer, A.-L. Barabási, The angle of repose in wet and dry granular media, Phys. Rev. E 56 (1997) R6271–R6276. | 젖음 안식각 실험 — 카드 없음 |
| 20 | N. Harnby, The mixing of cohesive powders, in: N. Harnby, M.F. Edwards, A.W. Nienow (Eds.), Mixing in the Process Industries, Butterworths Heineman Publishers, London, 1992, pp. 78–94. | 점착 분체 혼합 — 카드 없음 |
| 23 | C. Thornton, Coefficient of restitution for collinear collisions of elastic–perfectly plastic spheres, J. Appl. Mech. 64 (1997) 383–386. | 탄–완전소성 접촉 — 카드 없음 |
| 24 | O.R. Walton, R.L. Braun, Viscosity, granular-temperature, and stress calculations for shearing assemblies of inelastic, frictional disks, J. Rheol. 30 (1986) 949–980. | 접선 모델 — 카드 없음 |
| 27 | G. Lian, C. Thornton, M.J. Adams, A theoretical study of liquid bridge forces between two rigid spherical bodies, J. Colloid Interface Sci. 161 (1993) 138–147. | 다리 힘 · 파단 거리 — 카드 없음 |
| 35 | R.A. Bagnold, Experiments on a gravity-free dispersion of large solid spheres in a Newtonian fluid under shear, Proc. R. Soc. 225 (1954) 4–63. | 충돌력 원전 — 카드 없음 |
| 41 | P.M. Lacey, Developments in the theory of particle mixing, J. Appl. Chem. 4 (1954) 257–268. | Lacey 원저 — 같은 날 카드 후보 (#30) |
| 42 | J.F. Gilchrist, D.V. Khakhar, J.J. McCarthy, J.M. Ottino, Chaotic mixing of granular materials in two-dimensional tumbling mixers, Chaos 9 (1999) 195–205. | δ/R_t ≈ 0.03 의 출처 — 카드 없음 |
| 44 | J.A. Hersey, Ordered mixing: a new concept in powder mixing practice, Powder Technol. 11 (1975) 149–153. | ✅ [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md) (⚠ 쪽 41–44 — §10 항목 5) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 10 쪽 텍스트 층 전수 (pdftotext layout) + 식 (1)–(34) 렌더 (150 dpi) 글자 대조 — 식 (6)–(7) · (26) · (29) · (31) · (34) 는 렌더값을 옮김.
- 그림 11 장 = 전부 임베디드 래스터 (600 · 200 dpi) — 래스터 경계 + 2 pt 손 크롭 · 600 dpi 원본은 600 dpi 그대로 · 200 dpi 원본은 300 dpi · 전부 열람.  표 없음.
- 판독 5 개 그림 → digitized.csv.  우리 쪽 대조: 덱 메타 (rpm 75.04 · 반지름 · CGF) · `make_mixer_deck.py` (`FR_ANCHOR` · `E_PHASE` · pair_style) · Bo_code 값 = CLAUDE.md (믹서 행) · 논지 §2-6.
- 정본 litdb 중복 확인: `litdb/papers/` 목록 + 'Nase' · 'Discrete characterization' · 'collision number' grep — 없음.

## 🔗 관련 카드
- 같은 날 · 점착 혼합 · 보정: [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) (드럼 · 실란화 점착 · Bo_g · 동적 안식각) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (Coh 수 · 더미) · [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (SJKR CED 보정) · [`geldart2006_powder_flowability_angle_of_repose_tester`](geldart2006_powder_flowability_angle_of_repose_tester.md) (안식각 · Hausner).
- 같은 날 · 정렬 혼합: [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md) · [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md).
- 접촉 이론: [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
