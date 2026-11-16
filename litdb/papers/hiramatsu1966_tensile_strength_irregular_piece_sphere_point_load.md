<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-11 · 정독 53) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).  두 필수 절 = §0-1 고른 의도 대조 · §8 자세한 분석.
     강도 규약을 가리킨 두 카드 = wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem (L194 · L27 · L224 · L150) · stallard2022_cathode_mechanical_properties_review (L240 · L27 · L82 · L273 · L418 · L439 · L508).
     원문 = 스캔 PDF 15 쪽 (Acrobat Capture · 글자 쪽 = 1-bit CCITT 300 dpi 2190 × 2850 px · 판 = 200 dpi 회색 사진) = 인쇄 pp. 89–99 (11 쪽) + "facing page 90" 판 4 쪽.  SI 없음 · 표 0 · 번호 식 (1a)–(13) · 참고문헌 7.
     쪽 표기 = 인쇄 쪽 "p.97".  PDF 쪽 = p.89 → PDF 1 · p.90 → PDF 2 · 판 (Fig. 2 · 6 · 8 사진) → PDF 3–6 · p.91–99 → PDF 7–15.  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · 식 · 캡션에 찍힌 글자 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 62 행 — 300 dpi 렌더 = 1-bit 원본 해상도 · 눈금 글자 중심 최소제곱 · 표지 중심은 4–8 배 확대 단위 격자에서 눈으로) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · 원문 식 (11) · (12a) · (12b) 를 그대로 다시 더한 급수 포함 — §3-4 · §3-5) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 ·
     [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 15 쪽 전수에 없음.
     글자 층 (OCR) 은 수식에서 깨지고 'FIG. 1' 을 'FIG. l', 'Fig. 4' 를 'Fro. 4' 로 읽는다 → 식 · 캡션은 전부 렌더 (식 크롭 23 장) 에서 옮겼다.  DEM · FEM · 입자 계산 없음 — 1966 년 탄성 해석 (Legendre 급수) + 3D 동결 광탄성 + 암석 시험. -->
# 불규칙 시편 · 구를 두 점으로 눌러 암석 인장강도를 구하는 식의 원전 — 탄성 구 하중 축 중심의 인장 응력 (tensile stress) 1.21–1.36 F/(2πa²) (θ₀ < 5° · Poisson 수 m 3–7) + 10 % → S_t ≑ 1.4 F₀/(2πa²) 또는 ≑ 0.9 F₀/d² (= 2.8 F₀/(πd²) ≈ 0.891 F₀/d² 의 반올림 · 계수 1 아님) · Legendre 급수 해 · 3D 동결 광탄성 (구 · 정육면체 · 각기둥) · 8 암석 불규칙 시편 ↔ 원판 지름 압축 (Brazilian) 대조 — Hiramatsu · Oka (Int. J. Rock Mech. Min. Sci. 3, 89–99, 1966)

> slug `hiramatsu1966_tensile_strength_irregular_piece_sphere_point_load` · DOI `10.1016/0148-9062(66)90002-7` · type `continuum elasticity theory + 3D frozen-stress photoelasticity + rock tests (analytic elastic sphere under two uniform normal cap pressures of half-angle theta0 — Legendre series, Poisson's number m; epoxy sphere / cube / prism slices; point-load splitting of irregular lumps of 8 rocks vs disk diametral compression; 2D irregular plates under line loads — no DEM, no FEM, no particle simulation)` · PDF `cda474af-11._Determination_of_the_tensile_strength_of_rock_by_a_compression_test_of_an_irregular_test_piece.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: Y. Hiramatsu · Y. Oka — Department of Mineral Science and Technology, Kyoto University, Kyoto, Japan — *Int. J. Rock Mech. Min. Sci.* **Vol. 3**, **pp. 89–99** (Pergamon Press Ltd. **1966** · Printed in Great Britain — 첫 쪽 쪽 머리 그대로) · 접수 **1966-01-21** · 호 · 출판일 [미확인 — 스캔에 없음] · **DOI 는 스캔에 인쇄되지 않았다** (PDF 메타데이터 제목 = "PII: 0148-9062(66)90002-7" = DOI 꼬리와 같다) · 연구비 · 교신 · 저작권 표시 [미확인].
> **이웃 카드 (링크만)**: [`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`](wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md) (이 논문을 [26] 으로 인용 — 식 (1) σθθ ≈ P/D² · 계수 1 · L194 "[26] 원문은 미확인") · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) (같은 그룹 리뷰 · [108] · 식 4 σ_F = 2.8 P_C/(π d_P²)) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) (DEM 입자별 명목 응력 σm = f_max/d² · 계수 1 꼴) · [`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`](sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md) (NMC811 입계 직접 인장 — 다른 시험) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) · [`dang2019_nmc111_secondary_particle_flat_punch_fracture_strength`](dang2019_nmc111_secondary_particle_flat_punch_fracture_strength.md) (NMC111 평판 · 식 [1] S_t ≈ 2.8F_c/(πd²) · 이 논문을 [17] 로 인용 — 이 카드를 쓰는 동안 정본에 들어왔다).
> **판독 원자료**: `litdb/figures/hiramatsu1966_tensile_strength_irregular_piece_sphere_point_load/digitized.csv` (62 행 — Fig. 7 표지 53 (평균 표지 4 + 단일 시험 49 · 암석 기호별) + Fig. 5 중심 값 · 0 교차 9) · 그림 크롭 **46 장** (도구 3 중 다시 자름 3 + 손 크롭 43 = 그림 7 · 식 23 · 근거 문단 13) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 원문 식 (13) 은 **S_t ≑ 1·4 F₀/(2πa²) 또는 S_t ≑ 0·9 F₀/d²** (F₀ = 시편이 깨지는 하중 · "2a or d is the distance between the points of loading") 이다 (p.97 [인쇄]) — 첫 꼴을 d 로 쓰면 정확히 **2.8 F₀/(πd²) = 0.8913 F₀/d²** [카드 산술] 라서 같은 그룹 리뷰 (stallard2022 식 4) 의 꼴과 **같고**, 둘째 꼴 0.9 는 그 반올림 (+0.98 %) 이다.  **Wheatcroft 2023 의 σ_F = P_f/D² (계수 1) 은 원문에 없는 꼴**이다 (원문 0.9 의 1.111 배 · 2.8/π 의 1.122 배 [카드 산술]).  식의 뿌리는 **탄성 구** (반지름 a) 의 두 극에 반각 θ₀ 의 모자 모양으로 고른 수직 압력을 준 Legendre 급수 해 (식 (1)–(12)) 에서 읽은 **하중 축 중심의 인장 응력 1.21–1.36 × F/(2πa²)** (θ₀ < 5° · Poisson 수 m = 3∼7 = ν 0.14–0.33) 에 "maximum value being 10 per cent greater than the value at the centre" 를 얹은 값이고 (p.97), 불규칙 시편으로는 3D 동결 광탄성 (구 · 정육면체 · 각기둥 단면이 하중 축 근처에서 "much the same", p.90) 으로 넓혔으며, 8 암석의 불규칙 시편 ↔ 원판 지름 압축 결과 (Fig. 7) 로 "coincides fairly well" 을 보였다 (p.97).

★ **카드 재계산** [카드 산술 · §3-4 · §3-5]: 원문 식 (11) + (12b) 의 중심 값은 닫힌 꼴 **σθ(0) = 21/(14 + 10ν) · F/(2πa²) = 42/[π(14 + 10ν)] · F/d²** (θ₀ → 0) 이고, ν 1/3 → **1.2115** · ν 1/7 → **1.3611** 로 원문 "1·21 to 1·36" 을 **정확히** 재현한다 (ν 0.3 이면 **0.786 F/d²** — wheatcroft2023 의 독립 FE 중심 ≈0.79 [다른 카드 · 판독] 와 같다).  그러나 **축 위 분포** (Fig. 5 · '최대 10 %') 는 급수를 수렴할 때까지 (n ≤ 1500–4000) 더하면 재현되지 않고 — θ₀ 5° · m 3 에서 최대 = 중심의 **1.70 배** (r/a ≈ 0.74 · m 5 이면 2.99 배 · m 7 이면 3.78 배) · 압축으로 바뀌는 곳 r/a **0.84** — **n ≤ 3 (차수 0–6 의 네 항) 에서 자르면** 재현된다 (최대 1.06–1.08 배 @ r/a ≈ 0.35 · 0 교차 r/a **0.62**).  원문은 계산 항 수를 적지 않았다 [미확인] — 1.4 는 수렴 해로 보면 **중심 쪽 값** 의 규약이다 [카드 해석].

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 강도 식 원문 그대로 | *"S_t ≑ 1·4 F₀/2πa² or S_t ≑ 0·9 F₀/d², (13) where F₀ is the critical load, and 2a or d is the distance between the points of loading."* · "≑" = 근사 · 단위 = 하중 / 길이² (Fig. 7 = kg/cm²) · 초록 · 결론도 **0·9** | [인쇄] p.97 · p.89 · p.98 · `eq_13_tensile_strength_formula.png` |
| ② ★ 인용된 꼴과의 대조 | 계수 **1** (Wheatcroft) = 원문에 없음 · **2.8/π ≈ 0.891** (Stallard 리뷰 식 4) = 원문 첫 꼴 1.4/(2π) per a² 와 **정확히 같다** (d = 2a) · **0.9** = 원문 둘째 꼴 (2.8/π 의 반올림) | [카드 산술] §3-2 |
| ③ ★ 유도 가정 | 완전 탄성 · 등방 · 구 · φ 무관 (축대칭) · 하중 = 두 극 모자 (반각 θ₀) 위의 **고른 수직 압력 p** (마찰 · 접선력 없음) · 점하중 극한 p = F/{2πa²(1 − cos θ₀)}, θ₀ → 0 · 중심에서 응력 유한 · 표면 전단 0 · E 는 소거되고 m 만 남는다 · 수치: θ₀ < 5°, m 3∼7 → 중심 σθ 1.21–1.36 F/2πa² · 최대 10 % 더 큼 → 1.4 | [인쇄] p.90–97 · 식 (10a) · (11) · (12) |
| ④ ★ 적용 조건 | 하중 축은 *"through about the middle of the irregular test piece in the direction of its smallest dimension"* (p.90) · 인장 파괴가 실제로 일어날 것 (시편이 둘 · 때로 셋으로 쪼개짐 · 하중점 근처의 작은 압축 파괴는 있음 · p.97 · Fig. 6b) · 저자: *"not perfect because the stress state in the test piece is not simple and uniform, and affected a little by the nature of rock"* (p.98) | [인쇄] |
| ⑤ ★ 시험 (암석 · 시편 · 하중) | 8 암석 — 대리석 · 사암 · 석회암 · 백운암 · 안산암 · 응회암 (두 산지) · 이암 · 불규칙 시편 짧은 치수 **2.5–9 cm** · 원판 지름 **2.5–5.5 cm** · 두께 **2–3.5 cm** · 돌기가 달린 강 조각 한 쌍 (*"a projection, 7·5 cm in radius"*) · **50 t** 만능시험기 · 큰 표지 6 개 = 각 **약 40 시험** 평균 · 하중 속도 · 온도 · 암석 물성 [미확인] | [인쇄] p.97–98 |
| ⑥ ★ 다른 시험과의 비교 (Fig. 7) | (S_t)_i (식 13) ↔ (S_t)_d (원판 지름 압축 [6, 7]) — 판독 53 점: 식별되는 평균 표지 **4** 의 비 **0.92 · 1.01 · 1.00 · 1.01** · 단일 시험 49 점 비 중앙 **1.07** (10–90 % **0.71–1.60** · 전체 **0.56–1.94**) · 원점 지나는 기울기 **1.04** (단일 · 전체 1.035) · 범위 8.7–148 kg/cm² (≈0.85–14.5 MPa) · 원문은 산포 숫자를 내지 않았다 | [판독] Fig. 7 · [카드 산술] |
| ⑦ 2D 짝 | 같은 두께의 불규칙 판 · 선하중: *"S_t was given by twice the critical load under which the test piece broke divided by πdt"* = 2F₀/(πdt) · 광탄성 무늬 원판 ≈ 불규칙 판 (Fig. 8) | [인쇄] p.98 |
| ⑧ 저자 한계 | 완전 탄성 · 고른 수직 하중의 전제 · 불규칙 시편 = 구 인지 *"still some doubt"* (p.97) · θ₀ 와 m 의 영향 *"still room for discussion"* (p.97) · 세 파괴 양식 중 무엇이 일어날지는 *"can only be found by experiment"* (p.96) | [인쇄] §3-9 |
| ⑨ 우리 R7 (AM 파괴) 에 쓸 때 | 강도 값은 **계수와 함께** 기록하고 **하중 공간** (P_f = σ_F · D²/c) 에서 비교 · 탄성 구 중심 진응력 ν 0.25–0.30 = **0.81–0.79 F/d²** · 접촉 크기 θ₀ 에 따라 축 위 최대 인장이 **0.84–3.2 F/d²** 로 바뀐다 (ν 0.3 · θ₀ 10° → 3°) · 우리 AM–AM 접촉의 Hertz 반각 ≈7.5–9.3° 는 원문 범위 (θ₀ < 5°) 밖 [카드 산술 · 가정 명시] | §7-2 · §7-3 · §8 |

⛔ **한정어 (떼지 말 것)**: ① 식 (13) 은 **근사** (≑) — 이론 (탄성 구 · 점하중 θ₀ < 5° · m 3∼7) + 암석 8 종 실험으로 정한 **명목 강도 규약**이지 진응력이 아니다 ② 1.4 는 중심 값 (1.21–1.36) 위에 '최대 10 %' 를 얹어 반올림한 값 — 그 '10 %' 와 Fig. 5 의 축 위 분포는 원문 식을 수렴할 때까지 더한 결과와 맞지 않는다 (네 항에서 자른 급수와 맞는다 · §3-5) ③ d = **두 하중점 사이 거리** (구 = 지름 · 불규칙 시편 = 그 축의 길이) ④ 재료 = 암석 **cm** 시편 · 정적 · 하중 속도 · 온도 [미확인] — NCM · LPSCl 값 0 건 ⑤ 서지 = 쪽 **89–99** (인용한 카드들의 89–90 아님) · 머리글 학술지 = *Int. J. Rock Mech. Min. Sci.* ("Geomech. Abstr." 는 인쇄 안 됨).
⇒ **절대값 전이: 0 건** (강도 값은 암석).  전이되는 것 = **계수 규약** (1.4/(2π) ≡ 2.8/π ≈ 0.891 → 0.9 · 계수 1 아님) · **탄성 구 중심 응력의 닫힌 꼴** (재료 · E 무관 · ν 만) · **2D ↔ 3D 기하 계수 차** (§3-8) · 검증 꼴 (다른 시험과 1:1 대조).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-11 의 '왜' 칸)

의도 원문: *"c · m — 명목 강도 σ ≈ P/D² 규약의 원 출처 · Wheatcroft 는 계수 1 · 같은 그룹 리뷰는 σ_F = 2.8 P_C/(π d_P²) (계수 ≈0.891) 로 인용해 12 % 차 · wheatcroft '[26] 원문은 미확인' (L194) → 강도 값을 R7 에 쓰기 전에 규약 확정"* (가리킨 카드 = wheatcroft2023 L194 · stallard2022 L240)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "명목 강도 σ ≈ P/D² 규약의 원 출처" | **일부** | 원문은 F/d² 로 정규화한 명목 인장강도 규약의 출처다 (식 (13) p.97 · 초록 p.89 · 결론 p.98) — 그러나 계수가 **0·9** (첫 꼴 1·4 F₀/2πa² = 2.8/π ≈ 0.891) 이고 **"σ ≈ P/D²" (계수 1) 꼴은 원문에 없다**.  조건: 탄성 구 · 두 점하중 (모자 반각 θ₀ < 5°) · m 3∼7 · 하중 축 중심의 인장 파괴 (쪼개짐) · 암석 cm 시편 · 정적 (속도 [미확인]) · 상온 [미확인] |
| "Wheatcroft 는 계수 1" | **채움** (원문과 다르다는 것을 확인) | Wheatcroft 식 (1) σθθ ≈ P/D² → σ_F = P_f/D² [다른 카드 · wheatcroft2023 L27 · L224] ↔ 원문 0·9 → 계수 1 = 원문의 **1.111 배** · 탄성 구 중심 진응력 (ν 0.3 · 0.786 F/d²) 의 **1.27 배** [카드 산술] |
| "같은 그룹 리뷰는 σ_F = 2.8 P_C/(π d_P²) (계수 ≈0.891)" | **채움** | 원문 첫 꼴 1·4 F₀/(2πa²) 에 a = d/2 를 넣으면 정확히 **2.8 F₀/(πd²)** [카드 산술] — 리뷰는 원문 첫 꼴을 d 로 옮겼다 · 원문 둘째 꼴 0·9 는 2.8/π = 0.8913 의 반올림 (+0.98 %) |
| "12 % 차" | **채움** (한정 하나) | 1 / 0.8913 = **1.122** → 계수 1 ↔ 2.8/π 의 차 12.2 % · 원문 0·9 와는 **11.1 %** [카드 산술] · 진응력 쪽으로는 셋 다 중심 값 (ν 0.3 · 0.786) 보다 크다: 0.891 +13 % · 0.9 +14 % · 1 +27 % |
| "wheatcroft '[26] 원문은 미확인' (L194)" | **채움 — 이 카드로 해소** | 원문 = 이 논문 (식 (13) · 1966) · 단 그 줄의 서지 쪽 **"89–90"** 은 원문 쪽 머리 **"pp. 89–99"** 와 다르다 (아래 표 · 카드 문제) |
| "→ 강도 값을 R7 에 쓰기 전에 규약 확정" | **채움 (규약) · 없음 (NCM 값)** | 원문이 주는 것 = 계수의 뿌리 (탄성 구 중심 응력 + 10 %) · 적용 조건 (하중 축 · 인장 쪼개짐 · θ₀ · m) · 암석에서 원판 시험과의 1:1 대조 · 원문이 못 주는 것 = NCM 2 차 입자 (다결정 · 기공 · 입계 파괴 · µm) · 다접촉 · 무른 SE 에 싸인 조건의 계수와 값 → §7-2 · §8 R7 |

**가리킨 카드 · 같은 식을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `wheatcroft2023_…` L194 | *"[26] Y. Hiramatsu, Y. Oka, Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 1966, 3, 89–90. — ⚠ [26] 원문은 미확인. 같은 그룹 리뷰 [20] 은 같은 논문 ([108]) 을 σ_F = 2.8 P_C/(π d_P²) (계수 ≈0.891) 로 인용한다 … 이 논문은 "≈" 로 계수를 1 로 둔다"* | 저자 · 권 3 · 1966 ✓ · **쪽 89–99** · 머리글 학술지 = "Int. J. Rock Mech. Min. Sci." (Geomech. Abstr. 인쇄 없음) · 계수 서술 (리뷰 = 0.891 · Wheatcroft = 1) ✓ | **일부** — 쪽 · 학술지 꼬리가 원문과 다름 (Wheatcroft 참고문헌 목록을 그대로 옮긴 것) · [미확인] 해소 |
| `wheatcroft2023_…` L27 · L224 | *"식 (1) σθθ ≈ P/D² [26] → σ_F = P_f/D² (계수 1)"* · *"Hiramatsu–Oka [26] 를 따라 지름방향 압축 구의 인장 원주응력이 σθθ ≈ P/D² 로 스케일한다고 보고"* | 스케일 (∝ F/d²) ✓ · 계수는 원문 0·9 (중심 진응력 0.77–0.87 F/d²) | **채움** — 카드는 Wheatcroft 의 말을 바르게 옮겼다 (계수 1 은 Wheatcroft 의 선택) |
| `wheatcroft2023_…` L150 · L234 | FE (E 200 · ν 0.3 · D 10 µm) 중심 σθθ ≈ 0.79 P/D² · 평판 최대 ≈1.38 @ z/D ≈ 0.37 · 원뿔 최대 ≈4.77 @ z/D ≈ 0.44 [판독] | 원문 식의 닫힌 꼴 (ν 0.3) **0.786** · 수렴 급수 (ν 0.3 · θ₀ 5°) 최대 1.52 @ z/D 0.38 · (θ₀ 3°) 3.18 @ 0.43 [카드 산술] | **채움** (독립 대조 — 같은 물리) |
| `stallard2022_…` L27 · L82 · L273 · L508 | *"σ_F = 2.8 P_C/(π d_P²) (식 4, Hiramatsu–Oka [108] · Yoshida [111])"* | = 원문 첫 꼴 1·4 F₀/(2πa²) (d = 2a) | **채움** |
| `stallard2022_…` L240 | *"[108] Hiramatsu, Y., and Oka, Y. (1966). Determination of the tensile strength of rock by a compression test of an irregular test piece. Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 3, 89–90. https://doi.org/10.1016/0148-9062(66)90002-7."* | 제목 · 저자 · 권 · 연도 ✓ · DOI ✓ (스캔 메타 PII 와 같다) · **쪽 89–99** | **일부** — 쪽 (리뷰 참고문헌 목록을 그대로 옮긴 것) |
| `stallard2022_…` L418 · L439 | *"⚠ Brazil-nut 식 (2.8 인자) 은 불규칙 암석 조각에서 나온 근사다 [108] — 구형 이차입자에서 응력 상태 · 접촉 조건이 다르면 인자가 바뀐다"* · *"Hiramatsu–Oka 2.8 인자 (불규칙 조각용 근사)"* | 인자는 **탄성 구** 해석 (식 (12b) 의 중심 1.21–1.36 + 10 %) 에서 나왔고, 불규칙 조각은 광탄성 · 암석 시험으로 넓힌 **적용 범위**다 (p.97 *"perhaps valid also for an irregular test piece"*) · 뒷말 (접촉 조건 · m 에 따라 바뀜) 은 원문 p.97 *"since the values of θ₀ and m are varied, there is still room for discussion"* 과 맞는다 | **일부** — 앞말 (출처 = 불규칙 조각) 이 원문과 반대 |
| `dang2019_…` L31 · L199 (식 [1]) · L160 | *"S_t ≈ 2.8F_c/(πd²) — Hiramatsu & Oka [17]"* · 계수 0.891 | = 원문 첫 꼴 1·4 F₀/(2πa²) (d = 2a) | **채움** |
| `dang2019_…` L176 · L384 (참고문헌 [17]) | *"Y. Hiramatsu and Y. Oka, International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts, 3(2), 89 (1966)."* · L384 *"카드 없음 (후보 표 N-11)"* | 권 3 · 첫 쪽 89 · 1966 ✓ · 호 "(2)" = 스캔에 인쇄 없음 [미확인] · 머리글 학술지 = "Int. J. Rock Mech. Min. Sci." ("& Geomechanics Abstracts" 없음) | **일부** — 학술지 꼬리 (Dang 참고문헌 목록을 그대로 옮긴 것) · "카드 없음" 은 이 카드로 풀림 |
| `dang2019_…` L217 · L54 · L369 | *"Hiramatsu–Oka 식 — 불규칙 취성 조각을 두 점으로 눌러 인장 강도를 어림하는 경험식 (1966 · 암석) — 계수 2.8/π"* · *"S_t 는 식 [1] 의 근사 (불규칙 취성 조각 · 계수 2.8/π)"* | "근사" ✓ (원문 "≑" · "approximately") · 그러나 계수는 **탄성 구 해석** (식 (12b) 중심 1.21–1.36 + 10 %) 에서 정했고 암석 시험은 그 검증이다 (p.97 *"we need examine by experiment the validity of (13) which was derived purely theoretically"*) — 실험에 맞춘 경험식이 아니다 | **일부** — "경험식" 이 원문과 다르다 |
| 후보 표 `S8_candidates.md` N-11 행 | 서지 *"3, 89–90"* · 의도 문장 | 쪽 89–99 | **일부** (서지 쪽) |
| `comparison_vs_ours_DEM.md` L4497 (비교 문서 · 카드 아님) | *"Hiramatsu–Oka 2.8 인자 (불규칙 조각용)"* | 위 L418 과 같음 | **일부** (참고 — 고치지 않음 · 이 카드의 C 절 줄이 바른 출처를 적는다) |

⇒ **의도 대조 결과: 일부** — 명목 강도 규약의 원 출처 · 2.8/π 꼴 = 원문 첫 꼴 · 12 % 차 (원문 0.9 와는 11 %) · Wheatcroft L194 의 [미확인] 해소는 **채움**; 그러나 "σ ≈ P/D² (계수 1)" 은 **원문 꼴이 아니고** (원문 0·9 ≈ 2.8/π), NCM 조건의 계수 · 값은 **없음**, 2 차 인용의 서지 (쪽 89–90 → 89–99 · 학술지 꼬리 "Geomech. Abstr.") 와 "불규칙 조각에서 나온 인자" · "경험식" 서술이 원문과 다르다 (원문 = 탄성 구 해석으로 계수를 정하고 실험으로 확인).

---

## 1. 한 줄 요약
불규칙한 암석 덩어리를 마주 보는 두 점으로 눌러 쪼개는 간편 시험에서 **인장강도 = 0.9 × 깨지는 하중 / (하중점 거리)²** 라는 규약을 세운 1966 년 논문 — 근거는 (i) 3D 동결 광탄성으로 본 "불규칙 시편 ≈ 구 (하중 축 근처)" (ii) 두 극 모자 고른 압력을 받는 **탄성 구의 Legendre 급수 해** 에서 읽은 하중 축 중심 인장 응력 1.21–1.36 F/(2πa²) (+10 %) (iii) 8 암석에서 원판 지름 압축 (Brazilian) 강도와의 1:1 대조 (Fig. 7).  같은 논리를 2D 로 내린 **불규칙 판 (선하중) S_t = 2F/(πdt)** 도 함께 준다.
저자의 결론: *"we can determine the tensile strength of rock by the compression test of an irregular test piece, and that the tensile strength is given by 0·9 times the critical load under which the test piece breaks divided by the square of the distance between the points of loading. This method of testing is not perfect … But being rapid and convenient, it may be widely used in practice."* (p.98)

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| Y. Hiramatsu · Y. Oka (Kyoto Univ., Dept. of Mineral Science and Technology) | Int. J. Rock Mech. Min. Sci. 3, 89–99 (1966) · Pergamon | 10.1016/0148-9062(66)90002-7 (스캔에 인쇄 없음 · 메타 PII 와 같음) | 암석 8 종 (대리석 · 사암 · 석회암 · 백운암 · 안산암 · 응회암 2 · 이암) · 광탄성 모형 = 에폭시 수지 | 이론 (탄성 구 해석해) + 3D 동결 광탄성 + 2D 광탄성 + 암석 압축 시험 |

- **1저자 (메인 세션) 메모와의 대조**: 메모 *"Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 3 (1966) 89–90 (첫 쪽 인쇄가 'pp. 89–99' 일 수 있다)"* → 원문 첫 쪽 머리 = *"Int. J. Rock Mech. Min. Sci. Vol. 3, pp. 89–99. Pergamon Press Ltd. 1966. Printed in Great Britain"* (`txt_p1_header_title_abstract.png`) — **쪽 = 89–99** (인쇄 11 쪽 + 판 4 쪽) · 학술지 꼬리 "Geomech. Abstr." **인쇄 없음** · 호 [미확인] · 저자 "Y. HIRAMATSU and Y. OKA" ✓ · 제목 ✓ (대문자 인쇄) · DOI = 스캔에 없음 (메타 PII 와 같음).
- **글의 꼴**: 1 Introduction → 2 Stress state in an irregular elastic body subjected to a pair of concentrated loads (3D 광탄성 · Fig. 1–2) → 3 Analysis of the stress in an elastic spherical body compressed diametrically (식 (1a)–(12f) · Fig. 3–4) → 4 Discussion (Fig. 5 · 파괴 양식 셋 · 식 (13)) → 5 Experiments (Fig. 6–8 · 판 공식) → 6 Conclusion → References 7.  그림 8 (사진은 판 4 쪽 — Fig. 2 · 6 · 8) · 표 0 · SI 없음.
- **맥락**: 불규칙 시편으로 **압축**강도를 재는 방법들 [1–5] (Protodyakonov · Ilivitskii · Evans · Hobbs) 이 *"their principles are not entirely clarified"* (p.89) 인 상황에서 → 같은 시험을 **인장**강도로.  기준 시험 = 원판 지름 압축 [6] Akazawa 1943 · [7] Carniero & Barcellos 1949 (Brazilian test 의 원 문헌들).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 시편 · 재료 · 장치 (p.89–90 · p.97–98 · `txt_p1_photoelastic_models_freezing.png` · `txt_p2_photoelastic_result_loading_axis.png` · `txt_p13_experiments_setup_fig7.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 광탄성 모형 | 에폭시 수지 **구 지름 9·4 cm** · **정육면체 모서리 9·2 cm** · 직육면체 *"15 cm × 15 cm in sectional area, 8·8 cm high"* (원문 그대로) | [인쇄] p.89 |
| 동결 조건 | 집중하중 한 쌍 **52·5 kg** (≈515 N [카드 산술]) · **130 ± 1 °C 약 17 hr** 전기로 · **2·6 °C/hr** 서냉 (자기 기록 온도계로 확인) | [인쇄] p.89–90 |
| 단면 | 하중 축을 포함해 자른 판 두께 **8·2 · 7·75 · 6·3 mm** (구 · 정육면체 · 직육면체) · 재료 줄무늬 값 **약 2·6 kg/mm** · 편광기 관찰 | [인쇄] p.90 |
| 암석 (Fig. 7 범례) | A 대리석 (Mine City 근처) · B 사암 ("Izumi-Sagan") · C 석회암 (Ookanō mine) · D 백운암 (Ookanō mine) · E 안산암 (Manza mine) · F 응회암 (Manza mine) · G 응회암 (Shakanai mine) · H 이암 (Shakanai mine) · 탄성률 · ν · 밀도 · 기공 · 입도 [미확인] | [인쇄] p.98 |
| 불규칙 시편 | 짧은 치수 **2·5–9 cm** | [인쇄] p.97 |
| 원판 시편 | 지름 **2·5–5·5 cm** · 두께 **2–3·5 cm** · 시험 = 지름 압축 [6, 7] | [인쇄] p.97 |
| 가압 | *"a pair of steel pieces, each having a projection, 7·5 cm in radius, inserted between the platens of a 50 t universal testing machine"* — Fig. 6a 의 돌기는 시편보다 훨씬 작아 보인다 → "radius" 가 돌기 끝 곡률 반지름인지 [미확인] · 하중 속도 · 온도 · 습도 [미확인] | [인쇄] p.97 · [판독 · 사진] |
| 시험 수 | 큰 원 표지 6 개 = (S_t)_d · (S_t)_i 각각 *"about forty tests"* 의 평균 · 작은 표지 = 단일 시험 | [인쇄] p.97 |

### 3-2. ★ 식 (13) 원문 그대로 · 계수 대조 (p.97 · p.89 · p.98 · `eq_13_tensile_strength_formula.png` · `txt_p13_breakage_numerics_1p21_1p36.png` · `txt_p1_header_title_abstract.png` · `txt_p14_conclusion.png`)
- 도입 (p.97, 원문): *"Numerical calculation shows that when θ₀ < 5° and m = 3∼7, (σθ)θ=0 takes the value from 1·21 to 1·36 times F/2πa² at the centre of the test piece where F is the load, and it increases slightly with the distance from the centre, the maximum value being 10 per cent greater than the value at the centre. Therefore, it is supposed that the tensile strength may be approximately given by the following formula:"*
- **식 (13)**: *"S_t ≑ 1·4 F₀/2πa²  or  S_t ≑ 0·9 F₀/d², (13) where F₀ is the critical load, and 2a or d is the distance between the points of loading."*
- 초록 (p.89): *"the tensile strength of rock could be approximately determined by 0·9 times the critical load under which the test piece broke, divided by the square of the distance between the points of loading."* · 결론 (p.98) 같은 꼴 (0·9).
- 넓힘 (p.97): *"The discussion above-mentioned is perhaps valid also for an irregular test piece subjected to a pair of concentrated loads, since, as described in Section 2, the stress state in this test piece may be the same as that in a spherical test piece compressed diametrically with the same force."*

**계수 대조** [카드 산술 · σ = c · F/d² 로 맞춤]:
| 꼴 | c | 원문과의 관계 | 쓰는 곳 |
|---|---|---|---|
| 1·4 F/(2πa²) (원문 첫 꼴) | 2.8/π = **0.8913** | 원문 | — |
| 0·9 F/d² (원문 둘째 꼴) | **0.9000** | 원문 (첫 꼴의 +0.98 %) | 초록 · 결론 |
| 2.8 P/(π d²) | 0.8913 | **= 원문 첫 꼴** (d = 2a) | stallard2022 식 4 [다른 카드] |
| P/D² | **1.0000** | 원문에 없음 · 0.9 의 1.111 배 · 0.8913 의 1.122 배 | wheatcroft2023 식 (1) · song2025 σm · 우리 강도 분류기 (wheatcroft 카드 L419 `fracture_classify_strength` σ_nom = F/(2R)²) [다른 카드] |
| 탄성 구 중심 진응력 (θ₀ → 0) | 42/[π(14 + 10ν)] = **0.771** (ν 1/3) · **0.786** (ν 0.3) · **0.810** (ν 0.25) · **0.867** (ν 1/7) | 원문 "1·21–1·36 F/2πa²" 의 닫힌 꼴 (§3-4) | — |

- 같은 강도의 규약 바꿔 쓰기 [카드 산술]: Wheatcroft 평판 **207 MPa** (c 1) → c 0.9 **186.3** · c 0.8913 **184.5 MPa** · Stallard NMC333 이차입자 **185.6 MPa** (c 0.8913) → c 1 **208.2 MPa** = P_c/D² 0.208 mN µm⁻² (stallard 카드 D14 의 0.208 과 같다 [다른 카드]).
- **정규화 항등식** [카드 산술]: F/(2πa²) = 2F/(πd²) = 0.6366 F/d² = **두께가 지름과 같은 원판의 Brazilian 응력 2F/(πDt) (t = D)** → 원문 "1·21–1·36 × F/2πa²" 는 "같은 F · 같은 d 의 두꺼운 원판 응력의 1.21–1.36 배" 로도 읽힌다 (§3-8).
- 1·4 의 자리 [카드 산술]: 중심 1·21–1·36 × (1 + 10 %) = 1.33–1.50 → 가운데 ≈1.41 → 1·4 (원문은 고른 방법을 말하지 않는다 [미확인]).

### 3-3. ★ 탄성 해석 — 무엇을 어떻게 풀었나 (p.90–96 · 식 크롭 `eq_01abc` – `eq_lame_poisson_number_m` · Fig. 3 · Fig. 4)
- **문제** (p.90): *"Let us assume that an elastic spherical body, a in radius, is loaded diametrically."* · 극좌표 (r, θ, φ) · *"any stress component is independent on φ"* (축대칭).
- **평형** (1a)–(1c) (p.90): ∂σr/∂r + (1/r)∂τrθ/∂θ + (1/r)(2σr − σθ − σφ + τrθ cot θ) = 0 · ∂τrθ/∂r + (1/r)∂σθ/∂θ + (1/r){(σθ − σφ) cot θ + 3τrθ} = 0 · ∂τφr/∂r + (1/r)∂τθφ/∂θ + (1/r)(3τrφ + 2τθφ cot θ) = 0.
- **Hooke** (2a)–(2f) (p.91): σr = λΔ + 2μ ∂u/∂r · σθ = λΔ + 2μ((1/r)∂v/∂θ + u/r) · σφ = λΔ + 2μ(u/r + (v/r) cot θ) · τrθ = μ(∂v/∂r − v/r + (1/r)∂u/∂θ) · τθφ = μ((1/r)∂w/∂θ − (w/r) cot θ) · τφr = μ(∂w/∂r − w/r) — *"where λ and μ are the Lamé's constants of rock"* (Δ = 식 (4a) 의 부피 변형).
- **Δ · Ω 로** (3a)–(3b) · 정의 (4a)–(4b): Δ = (1/(r² sin θ)){∂(r²u sin θ)/∂r + ∂(rv sin θ)/∂θ} · 2Ω = ∂v/∂r + v/r − (1/r)∂u/∂θ → Ω 소거 → **∇²Δ = 0** (5).
- **급수**: Δ = Σ_{n≥1} (A_n rⁿ − A′_n r^−(n+1)) P_n(cos θ) (6) · 2Ω (7) · u · v (8a)–(8b) · w (8c) · 응력 급수 (9a)–(9f).
- **경계** (p.93): 중심 유한 → **A′_n = C′_n = D′_n = 0** · 표면 r = a 에서 τrθ = τθφ = τφr = 0 → **D_n = 0**, C_n = [n(n+2)λ + (n²+2n−1)μ] / [(n−1)(n+1)(4n+6)μ] · a²A_n.
- **하중** (10a) (p.94): *"Let us assume that the load acts normally and uniformly on the surface of the sphere, symmetrically with respect to the z-axis, the angle subtended at the centre of the sphere by the margin of the loaded area being 2θ₀"* → (σr)_{r=a} = p (0 ≤ θ ≤ θ₀, π − θ₀ ≤ θ ≤ π) · 0 (θ₀ < θ < π − θ₀) — **마찰 · 접선 하중 없음**.
- 대칭 → **짝수 n 만** (n → 2n) · Fourier–Legendre 전개 (10b): (σr)_{r=a} = p(1 − cos θ₀)P₀ − Σ_{n≥1} (4n+1)/(2n(2n+1)) · p sin θ₀ · ∂P_{2n}(cos θ₀)/∂θ · P_{2n}(cos θ).
- **계수** (11): A_{2n} = −(4n+3)(4n+1){cos θ₀ P_{2n}(cos θ₀) − P_{2n−1}(cos θ₀)} p / {[(8n²+8n+3)λ + (8n²+4n+2)μ] a^{2n}} · C_{2n} = [2n(2n+2)λ + (4n²+4n−1)μ] / [(2n−1)(2n+1)(8n+6)] · a²A_{2n} (인쇄본 분모에 μ 없음 — p.93 C_n 에는 있음) · 나머지 0.
- **응력** (12a)–(12f): σr · σθ · σφ · τrθ 의 급수 · τθφ = τφr = 0.  ★ 강도 식에 쓴 양 = **(σθ)θ=0 = 하중 축 위의 '원주 (수평)' 응력**.
- **점하중 극한** (p.95): *"When a spherical body is compressed diametrically by a pair of sharply pointed forces F, each stress component can be evaluated mathematically by first putting p = F/{2πa²(1 − cos θ₀)}, and then letting θ₀ tend to zero."*
- **탄성 상수** (p.96): *"If the Young's modulus and the Poisson's number be denoted by E and m respectively, λ and μ are represented by mE/(m + 1)(m − 2) and mE/2(m + 1) respectively. If we substitute these values for λ and μ in the system (12), E vanishes and we obtain equations containing only Poisson's number m."* — m = 1/ν → m 3∼7 = ν **0.143–0.333** [카드 산술].
- 계산 수단 · 더한 항 수 · 계산 비용 [미확인] (*"Numerical calculation shows …"* 한 문장).

### 3-4. ★ 중심 값의 닫힌 꼴 — 카드 재유도 [카드 산술]
r = 0 에서는 r^{2n} (n ≥ 1) · a²r^{2n−2} (n ≥ 2) 항이 사라져 **n = 0, 1 (Legendre 차수 0 · 2) 만** 남는다.  P_{−1} ≡ P₀ = 1 (표준 약속 · 원문 미기재) 로 (11) · (12a) · (12b) 를 그대로 쓰면:
- n = 0: σr = σθ = σφ = (1 − cos θ₀)p → **F/(2πa²)** (정수압 몫 · 중심의 평균 응력 = 정확히 F/(2πa²))
- n = 1: σθ 에 −(5/2)·(8λ+7μ)/(19λ+14μ)·cos θ₀ sin²θ₀ · p · σr 에 +5·(8λ+7μ)/(19λ+14μ)·cos θ₀ sin²θ₀ · p
- θ₀ → 0 (sin²θ₀/(1 − cos θ₀) → 2) · λ/μ = 2ν/(1 − 2ν) 를 넣으면:
  - **(σθ)₀ = 21/(14 + 10ν) · F/(2πa²)** (하중이 누르는 쪽이면 인장) = 42/[π(14 + 10ν)] · F/d²
  - **(σr)₀ = [1 + 10(2ν + 7)/(10ν + 14)] · F/(2πa²)** (압축)

| ν (m) | (σθ)₀ 인장 [F/2πa²] | [F/d²] | (σr)₀ 압축 [F/2πa²] | 쓰임 |
|---|---|---|---|---|
| 1/3 (3) | **1.2115** | 0.771 | 5.423 | 원문 "1·21" |
| 0.30 (3.33) | 1.2353 | **0.786** | 5.471 | NCM 근처 · wheatcroft FE ν 0.3 |
| 0.25 (4) | 1.2727 | 0.810 | 5.545 | 우리 AM E* 의 ν [다른 카드] |
| 0.20 (5) | 1.3125 | 0.836 | 5.625 | Fig. 5 점선 |
| 1/7 (7) | **1.3611** | 0.867 | 5.722 | 원문 "1·36" |
| 0.36 | 1.1932 | 0.760 | — | LPSCl DFT ν 0.360 [우리] (참고 · 탄성일 때) |
| 0.49 | 1.1111 | 0.707 | — | MPM SE ν 0.49 [우리] (참고 · 탄성일 때) |

- θ₀ = 5° 면 n = 1 몫이 cos θ₀(1 + cos θ₀)/2 = 0.9943 배 → m 3 **1.199** · m 7 **1.348** (원문 범위 1·21–1·36 은 θ₀ → 0 의 값 그대로 · θ₀ 5° 의 아래 끝은 1.20).
- 수치 급수 (§3-5) 와 소수 넷째 자리까지 같다 · **독립 대조**: wheatcroft2023 의 축대칭 탄성 FE (E 200 GPa · ν 0.3 · D 10 µm) 중심 σθθ ≈ **0.79 P/D²** [다른 카드 · 판독] ↔ 닫힌 꼴 ν 0.3 = **0.786**.

### 3-5. ★ 축 위 분포 — Fig. 5 판독 ↔ 원문 식 재계산 (p.96 · `fig_5.png` · `txt_p12_fig5_reading_fracture_modes.png`)
- **그림** (Fig. 5): 패널 셋 2θ₀ = **0° · 6° · 10°** (= θ₀ 0 · 3 · 5°) · 실선 m = 3 · 점선 m = 5 · 세로축 r/a (하중 축 위 중심으로부터의 거리) · 가로축 −σ/(F/2πa²) (−2 … 10 · 인장이 0 의 왼쪽).
- **판독** [판독 · ±0.15 · digitized.csv fig5]: r/a ≈ 0 에서 σθ 인장 **≈1.4 · ≈1.3 · ≈1.2** · σr 압축 **≈5.2 · 5.1 · 5.2** · σθ 는 r/a ≈ 0.55 까지 거의 수직 → **r/a ≈ 0.62–0.66 에서 0** → r/a ≈ 0.8 에서 압축 ≈8–10 · σr 은 r/a ≈ 0.5 에서 ≈12.
- **원문 말** (p.96): *"(σθ)θ=0 is a tensile stress and distributes fairly uniformly over the central part, about half the diameter wide, and that the magnitude does not depend much on θ₀ and m. While another principal stress (σr)θ=0, which also does not depend much on θ₀ and m, is compressive and from five to ten times (σθ)θ=0 within the range where the latter distributes fairly uniformly. It should be noted, however, that both (σr)θ=0 and (σθ)θ=0 are very great compressive stresses in the neighbourhoods of the loading points."*
- **카드 재계산** [카드 산술 · 원문 식 (11) + (12a) · (12b) 그대로 · 축 θ = 0 (P_{2n}(1) = 1 · ∂²P_l/∂θ²|₀ = −l(l+1)/2) · P_{−1} = 1 · a = 1 · 결과를 F/(2πa²) 로]:

| θ₀ · m | 더한 항 (n ≤ N) | 중심 σθ | 축 위 최대 σθ (중심 대비) · 자리 | σθ 가 0 이 되는 r/a |
|---|---|---|---|---|
| 0.5° · 3 | 3 | 1.211 | 1.308 (**1.08 ×**) · 0.35 | **0.62** |
| 3° · 3 | 3 | 1.207 | 1.296 (1.07 ×) · 0.35 | 0.62 |
| 5° · 3 | 3 | 1.199 | 1.277 (1.06 ×) · 0.34 | 0.62 |
| 5° · 3 | 4 | 1.199 | 1.368 (1.14 ×) | 0.67 |
| 5° · 3 | 10 | 1.199 | 1.897 (1.58 ×) | 0.805 |
| 5° · 3 | **20 · 3000 (수렴)** | 1.199 | **2.04 (1.70 ×) · r/a ≈ 0.74** | **0.84** |
| 5° · 5 | 3000 | 1.299 | 3.88 (2.99 ×) · 0.81 | 0.88 |
| 5° · 7 | 3000 | 1.348 | 5.10 (3.78 ×) · 0.83 | 0.89 |
| 3° · 3 | 3000 | 1.207 | 3.88 (3.21 ×) · 0.84 | 0.90 |
| 1° · 3 | 3000 | 1.211 | r/a 0.8 에서 4.68 · 하중점 쪽으로 계속 커짐 (r/a 0.95 에서 28.6) | ≤ 0.95 에 없음 |

  - σr (수렴 · m 3 · θ₀ 1–5°): 중심 5.40–5.42 · r/a 0.4 **9.2–9.4** · 0.5 **12.6–12.9** — Fig. 5 판독 (≈5.2 · 0.5 에서 ≈12) 과 맞다 (n ≤ 3 이면 0.5 에서 11.3–11.5).
  - 계산 점검 [카드 산술]: 수렴 급수는 하중 모자 바로 밑에서 **σr → p** 를 지킨다 (θ₀ 5° · m 3: r/a 0.99 에서 263.2 ↔ p = 262.8 F/2πa² · m 5 263.8 · θ₀ 10° · m 3: 65.9 ↔ 65.8) · σθ 는 반무한체 원형 고른 하중의 표면 중심 값 (1 + 2ν)p/2 근처로 간다 (m 3 · θ₀ 5°: r/a 0.995 에서 219.6 ↔ 219.0 · m 5: 191.0 ↔ 184.0 · θ₀ 10°: 61.5 ↔ 54.9 — 모자 바로 밑은 급수 수렴이 느려 4–12 % 차) · N 20 과 N 3000 의 축 최대가 같다 (θ₀ 5° · 2.042).
  - 독립 대조 (ν 0.3 · 수렴) [카드 산술 · F/d²]: θ₀ **3°** 중심 0.783 · 최대 **3.18 @ z/D 0.43** · θ₀ **5°** 0.778 · **1.52 @ 0.38** · θ₀ 7.5° 0.768 · 1.02 @ 0.32 · θ₀ **9°** 0.760 · **0.89 @ 0.28** · θ₀ 10° 0.754 · 0.84 @ 0.25 (z/D = r/(2a)) ↔ wheatcroft2023 FE 평판 최대 **≈1.38 @ z/D ≈ 0.37** · 원뿔 팁 **≈4.77 @ ≈0.44** [다른 카드 · 판독] — 접촉이 작을수록 최대가 크고 접촉 쪽에 붙는 같은 꼴.
- ⇒ [카드 해석] **원문 Fig. 5 와 '최대 10 %' 는 급수를 n ≤ 3 근처에서 자른 계산과 맞고**, 수렴한 탄성 해는 **하중점 쪽으로 인장이 커지는** 분포다 (점하중일수록 크고 · 압축으로 바뀌는 띠는 모자 깊이 ≈0.1–0.2 a 안).  그래서 원문의 1·4 (≈ 중심 × 1.1) 는 수렴 해에서는 **중심 쪽 값** 이다.  원문 계산의 항 수 · 방법 [미확인] — 카드는 원문 식을 그대로 썼고 독립 해 (FE · 다른 해석해) 로 축 위 분포 전체를 대조하지는 않았다 (wheatcroft FE 판독 값과의 대조만).
- 원문이 관찰한 파괴 (p.97): *"every test piece broke into two pieces, sometimes into three pieces, perhaps due to the tensile stress (σθ)θ=0, although compression fracture was found over a small area near each point of loading [see Fig. 6(b)]."* — 쪼개짐 면이 하중 축을 지난다는 관찰은 규약과 맞지만, 균열이 **어디서 시작했는지** (중심 ↔ 하중점 근처의 최대 인장 · 국부 파쇄) 는 원문이 가르지 않는다.

### 3-6. ★ Fig. 7 — 불규칙 시편 (S_t)_i ↔ 원판 (S_t)_d [판독] (p.98 · `fig_7.png` · digitized.csv fig7 53 행)
- 판독 방법: PDF 14 쪽 300 dpi (= 1-bit 원본) · 눈금 글자 중심으로 축 맞춤 (x: px = 92.3 + 4.686·X · 잔차 ≤ 0.8 kg/cm² · y: py = 757.7 − 4.667·Y · 잔차 ≤ 0.3) · 표지 중심은 4–8 배 확대 단위 격자에서 눈으로 (±1 kg/cm²) · 저자의 1:1 선은 이 맞춤의 대각선보다 ≈0.7 위 · 기호 → 암석은 6 배 확대 범례로 (A 속 찬 이중 원 · B 빈 이중 원 · C 검은 원 + 오른쪽 흰 띠 · D 오른쪽 반 검정 · E 원 속 십자 · F 점선 원 · G 점 박힌 원 · H 찬 원).
- **범위**: (S_t)_d **8.7–146** · (S_t)_i **10.5–148 kg/cm²** (≈0.85–14.5 MPa [카드 산술 · 1 kg/cm² = 0.0981 MPa]).
- **큰 표지 (평균 · 약 40 시험)** — 원문 "six" 중 식별 **4**: A 42.4 → 39.0 (비 **0.92**) · A 66.4 → 67.3 (**1.01**) · B 85.6 → 86.0 (**1.00**) · B 146.3 → 147.9 (**1.01**) · 나머지 둘 [판독 불가 — H 덩어리 안의 큰 표지일 수 있음].
- **단일 시험 49** (H 덩어리 11 포함 · 겹친 검은 원이라 개수 · 중심 불확실): 비 (S_t)_i/(S_t)_d 중앙 **1.07** · 기하 평균 1.08 · 10–90 % **0.71–1.60** · 범위 **0.56–1.94** · ±20 % 안 **51 %** · ±30 % 안 **65 %** · log 표준편차 0.29 · H 빼면 (38) 중앙 1.05 · 10–90 % 0.67–1.37.
- 암석별 (단일 · 중앙): C **1.17** (8) · D 1.07 (8) · E **0.66** (3) · F 0.95 (10) · G 1.07 (8) · H **1.32** (11 · 겹침).
- 원점을 지나는 최소제곱 기울기 **1.035** (전체 53) · **1.041** (단일 49) [카드 산술].
- **계수 1 이었다면** [카드 산술]: 모든 (S_t)_i × 1.111 → 평균 표지 비 1.02–1.13 · 단일 중앙 1.19.
- 원문 판정: *"Figure 7 shows that (St)i, coincides fairly well with (St)d, from which it follows that (13) can be used to evaluate, from the compression test of an irregular test piece, the tensile strength with nearly the same accuracy as in the diametrical compression test of a disk test piece."* (p.97) — 산포 · 오차의 숫자는 없다 [미확인].
- ⚠ 원판의 (S_t)_d 를 어느 식으로 셈했는지는 원판에 대해 인쇄되지 않았다 ([6, 7] 인용뿐) — 판 시험의 2F/(πdt) (p.98) 와 같은 식으로 보인다 [카드 해석].

### 3-7. 광탄성 (Fig. 2 · 8 · p.89–90 · p.98)
- Fig. 2 (구 · 정육면체 · 직육면체 단면 · 하중 축 포함): *"observation of Fig. 2 [a–c] may make it clear that, within the accuracy of photoelasticity, the stress states in a sphere, a cube and a rectangular prism, in the vicinity of the axis of loading, are much the same."* (p.90) — 세 무늬 모두 가운데 X 꼴 (등방점) · 하중점 근처 촘촘한 줄무늬 · 정육면체 · 직육면체는 모서리 · 옆면 쪽 무늬가 다르다 [판독 · 정성].
- 동결 응력법의 한계 (p.90): *"because every stress component is statically indeterminate, the stresses found by the frozen-stress method depend on the elastic constants of the material of the model at the moment the stress is fixed, which are far different from those of rock."* → 정량은 해석 (§3-3).
- Fig. 8 (원판 ↔ 불규칙 판 · 선하중 · 2D): *"which agree pretty well with each other"* (p.98).
- 줄무늬 차수 · 응력 값 [미확인 — 그림만].

### 3-8. 2D 짝 — 불규칙 판의 선하중 (p.98 · `txt_p14_irregular_plate_line_load.png`)
- *"the tensile strength of rock, S_t, could be determined by compression test of an irregular-shaped plate, and that S_t was given by twice the critical load under which the test piece broke divided by πdt, where d is the distance between the points of loading, t the thickness of the test piece."* → **S_t = 2F₀/(πdt)** [인쇄 · 말로].  시험 수 · 판 두께 · 결과 그림 [미확인].
- [카드 산술] 같은 F · 같은 d 에서 3D 구 (0.9 F/d²) ↔ 2D 판 (t = d · 0.637 F/d²) → **3D/2D = 1.41** · 중심 진응력 기준 1.21–1.36 (§3-2 항등식).
- ⇒ [카드 해석] 같은 '지름 압축 쪼개짐' 이라도 2D (판 · 선하중) 와 3D (덩어리 · 점하중) 의 기하 계수가 **21–41 %** 다르다 — 원문은 2D → 3D 전이에 대해 말하지 않는다.

### 3-9. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**:
1. *"The analysis of stress described in Section 3 holds true on the premises that the spherical test piece is perfectly elastic and that the load acts normally and uniformly on the test piece. Therefore we need examine by experiment the validity of (13) which was derived purely theoretically. Furthermore there is still some doubt as to whether or not the stress state in an irregular test piece is exactly the same as that in a spherical test piece when both are subjected to a pair of concentrated loads of the same magnitude."* (p.97)
2. *"since the values of θ₀ and m are varied, there is still room for discussion on the influence of the values of θ₀ and m on the determination of the tensile strength of rock."* (p.97)
3. 파괴 양식 셋 — *"(i) tension fracture due to (σθ)θ=0 over the middle part of the test piece, (ii) crushing due to the great compressive stresses (σr)θ=0 and (σθ)θ=0 near the points of loading, (iii) compression fracture due to (σr)θ=0 over the whole range between the two points of loading. Which phenomenon does occur actually can only be found by experiment."* (p.96)
4. *"This method of testing is not perfect because the stress state in the test piece is not simple and uniform, and affected a little by the nature of rock."* (p.98)
5. 동결 응력의 탄성 상수가 암석과 다르다 (p.90).

**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. 결론 *"From the results of compression tests of both a **sphere** and an irregular test piece"* (p.98) ↔ 5 절은 불규칙 시편을 **원판** 과 견줬다 (p.97) — 구 시편 시험은 보고되지 않았다.
2. Fig. 7 캡션 *"(Si)t"* ↔ 세로축 · 본문 *"(St)i"* · 본문 한 곳 *"(St)t"* (p.97).
3. *"six bigger circular marks"* ↔ 암석 8 종 · 그림에서 큰 표지로 식별되는 것은 A · B 둘씩뿐.
4. 식 인쇄: (12a) 첫 괄호 *P_n(cos θ)* ↔ 다른 곳 P_{2n} · (11) C_{2n} 분모에 μ 없음 ↔ p.93 C_n 에는 있음 · (8b) 첫 항 분모에 μ 없음 ↔ (8a) 에는 있음 ((9b) 와 맞으려면 μ 가 있어야 한다 [카드 해석]) · (9b) 끝 항 C′_n/r^{n+1} ↔ (9c) C′_n/r^{n+3} (C′_n = 0 이라 결과 무영향).
5. p.93 *"the terms containing 1/rⁿ, 1/r^{n+1} and 1/r^{n+2} in (2a) – (2f) should be zero"* — 급수 (9a)–(9f) 를 가리키는 것으로 보인다 [카드 해석].
6. 본문 *"three values of θ₀, 0°, 3°, 5°"* ↔ 그림 라벨 2θ₀ = 0° · 6° · 10° (같은 뜻) · 본문 m = 3∼7 ↔ 그림은 m 3 · 5 둘.
7. *"the maximum value being 10 per cent greater"* · Fig. 5 의 0 교차 r/a ≈ 0.62–0.66 ↔ 원문 식을 수렴까지 더한 결과 (최대 1.7 배 · 0 교차 0.84 · θ₀ 5°) — 네 항에서 자른 결과와 맞음 (§3-5) [카드 산술].
8. *"a projection, 7·5 cm in radius"* ↔ 시편 2.5–9 cm · Fig. 6a 사진의 작은 돌기 — 뜻 [미확인].
9. 직육면체 *"15 cm × 15 cm in sectional area, 8·8 cm high"* — 원문 그대로 (단면 크기 · 높이의 뜻 [미확인]).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **광탄성 (3D)**: 에폭시 모형 (구 · 정육면체 · 직육면체) → 52.5 kg 한 쌍 → 130 °C 17 hr → 2.6 °C/hr 서냉 (응력 동결) → 하중 축 포함 단면 (6.3–8.2 mm) → 편광기 줄무늬 (Fig. 2) — 정성 비교만.
- **광탄성 (2D)**: 원판 · 불규칙 판 선하중 (Fig. 8) — 정성 비교.
- **암석 시험**: 불규칙 시편 (2.5–9 cm) 을 돌기 달린 강 조각 사이에서 50 t 시험기로 압축 → 깨지는 하중 F₀ · 하중점 거리 d → 식 (13) → (S_t)_i · 같은 암석의 원판 지름 압축 → (S_t)_d → Fig. 7.  하중 속도 · 시편 수 (암석별) · 습도 · 온도 [미확인].

### 4-2. 계산 사슬
평형 + Hooke (구면 좌표 · 축대칭) → Δ 의 Laplace 식 → Legendre 급수 일반해 → 중심 유한 · 표면 전단 0 → 모자 고른 압력의 Fourier–Legendre 계수 맞춤 → 응력 급수 (12) → 점하중 극한 · E 소거 (m 만) → θ₀ < 5°, m 3–7 에서 축 위 (σθ)θ=0 수치 → 중심 1.21–1.36 F/2πa² + 10 % → 식 (13).  계산 도구 · 항 수 [미확인].

### 4-3. 입자 처리 ★
- **입자 = 하나의 균질 · 등방 · 선형 탄성 연속체 (구)** — 내부 결정립 · 기공 · 결함 · 소성 · 손상 없음.  불규칙 시편은 "하중 축 근처에서 구와 같다" 로 대신한다 (광탄성 근거).
- **접촉 = 두 극 모자의 고른 수직 압력** (반각 θ₀ · 마찰 없음 · Hertz 꼴 아님) → 점하중 극한.  접촉 크기와 재료 강성의 관계는 다루지 않는다 (θ₀ 는 주어진 값).
- 다입자 · 접촉망 · 재배열 없음 (시편 하나 · 하중점 둘).

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete · particle 낱말 0 회 — 1966).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 해석은 *"perfectly elastic"* 전제 (p.97) · 하중점 근처의 *"crushing due to the great compressive stresses"* 를 가능성으로만 (p.96) · 관찰 *"compression fracture was found over a small area near each point of loading"* (p.97) — 넣는 법 · 비용 없음.  우회 = **명목 강도 + 다른 시험 (원판) 과의 실험 대조** 로 오차를 흡수.
3. **2D / 3D** — 3D 해석 (구) + 3D 동결 광탄성 (단면) + 3D 암석 덩어리 / 2D 짝 = 원판 · 불규칙 판 (선하중) · 공식 2F/(πdt) — **2D → 3D 전이에 대한 말 없음** · 카드 산술 = 기하 계수 21–41 % 차 (§3-8).
4. **압력을 뺄 때의 거동** — **다루지 않았다** (하중 증가 → 깨지는 하중 F₀ 만).

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| irregular test piece | 가공하지 않은 암석 덩어리 시편 — 마주 보는 두 점으로 눌러 쪼갬 |
| critical load F₀ | 시편이 깨지는 하중 |
| d (= 2a) | 두 하중점 사이 거리 (구면 지름) |
| θ₀ | 하중을 받는 모자의 반각 (모자 가장자리가 중심에서 2θ₀ 를 이룸) |
| Poisson's number m | 1/ν (m 3∼7 = ν 0.143–0.333) |
| (σθ)θ=0 | 하중 축 위의 원주 (수평) 방향 응력 — 인장 · 쪼개짐을 일으키는 응력 |
| frozen-stress photoelasticity | 하중을 건 채 가열 · 서냉해 응력 무늬를 굳히고 단면을 잘라 보는 3D 광탄성 |
| material fringe value | 줄무늬 차수 하나에 해당하는 응력 × 두께 (kg/mm) |
| diametrical compression test of a disk | 원판을 지름 방향으로 눌러 쪼개는 간접 인장 시험 (Brazilian test · [6, 7]) |
| Brazil-nut test | 리뷰 (stallard2022) 가 이 시험을 입자 압축에 붙인 이름 — 이 논문에는 없는 낱말 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 손 크롭) | (a) 지름 압축 구 (b) 한 쌍 집중하중의 불규칙 시편 | 시험 꼴 — 단일 입자 압축 시험 (U1) 의 그림 |
| **Fig. 2** (`fig_2.png` 판 1 · `fig_2b.png` · `fig_2c.png` 판 2) | 3D 동결 광탄성 단면 줄무늬 — (a) 구 (b) 정육면체 (c) 직육면체 | 하중 축 근처 무늬가 형상에 둔감하다는 근거 (정성) — 불규칙 입자에 구 해석을 쓰는 근거의 꼴 |
| **Fig. 3** (`fig_3.png`) | 구면 좌표 응력 성분 (σr · σθ · σφ · τ) | 식 (1)–(12) 기호표 |
| **Fig. 4** (`fig_4.png`) | 하중 p 와 모자 반각 2θ₀ | 경계 조건 (10a) — 마찰 없는 고른 압력 모자 |
| **Fig. 5** (`fig_5.png`) | 축 위 (σr)θ=0 · (σθ)θ=0 · 2θ₀ = 0 · 6 · 10° · m 3 · 5 | ★ 중심 σθ ≈1.2–1.4 · σr ≈5.2 [판독] · ⚠ 축 위 모양은 카드 재계산 (수렴) 과 다름 (§3-5) |
| **Fig. 6** (`fig_6.png` 다시 자름) | (a) 불규칙 백운암 시편을 돌기 사이에서 누름 (b) 둘로 쪼개진 시편 | 파괴 꼴 (하중 축을 지나는 쪼개짐 · 하중점 국부 파쇄) |
| **Fig. 7** (`fig_7.png`) | (S_t)_i ↔ (S_t)_d · 8 암석 · 평균 큰 표지 + 단일 시험 | ★ 1:1 대조 · 평균 비 0.92–1.01 · 단일 0.56–1.94 [판독] — 규약 오차 (11–12 %) 와 재료 산포의 크기 비교 |
| **Fig. 8** (`fig_8.png` 다시 자름) | 2D 광탄성 — (a) 원판 (b) 불규칙 판 · 선하중 | 2D 짝 (S_t = 2F/(πdt)) 의 근거 |
| 식 크롭 23 (`eq_01abc` … `eq_13`) · 근거 문단 13 (`txt_p*`) | 식 (1a)–(13) · 경계 조건 · 점하중 극한 · λ–μ–m · 인용 문장 | 보고서 붙임 · 식 옮김의 근거 |

## 6. Post-processing ★
- **강도 계산**: 깨지는 하중 F₀ · 하중점 거리 d → S_t = 0.9 F₀/d² (불규칙 덩어리) · 2F₀/(πdt) (판).  d 를 재는 법 (캘리퍼 · 어느 두 점) [미확인].
- **해석 → 계수**: 축 위 σθ 수치 → 중심 1.21–1.36 + 최대 10 % → 1.4 (반올림 규칙 [미확인]).
- **검증**: 같은 암석의 원판 강도와 1:1 그림 (Fig. 7) — 평균 (약 40 시험) 과 단일 시험을 같은 그림에 · 산포 통계 없음.
- **이 카드의 판독 · 재계산**: digitized.csv (Fig. 7 53 점 · Fig. 5 9 행 · 방법은 note 열) · 급수 재계산 = 원문 식 (11) · (12a) · (12b) 를 축 위에서 n ≤ N 까지 더함 (Legendre 점화식 · N 3 · 4 · 10 · 20 · 1500–4000 · 경계 점검 §3-5).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 다른 카드 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 크기 · 하중 조건이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 강도 규약 | S_t ≑ 0.9 F₀/d² (≡ 2.8/π · 1.4/(2π) per a²) · 암석 | 강도 분류기 σ_nom = F/(2R)² (c 1) ↔ Wheatcroft σ_F (c 1) [다른 카드 · wheatcroft L419] · DEM 파괴 판정 = Auerbach 원뿔 균열 **개시** P_c = A·K²·R/E* (사후 분류) [다른 카드 · stallard §7] | **다른 사건**: 이 식 = 쪼개짐 하중 · Auerbach = 균열 개시 · 우리 c 1 끼리는 자기 일관 (§7-2) |
| 입자 응력 상태 | 두 점 (모자) 하중 · 마찰 없음 · 균질 탄성 구 | AM 은 접촉 Z 개 (AM–AM · AM–SE · 벽) · 다결정 · 기공 · 무른 SE 에 싸임 [우리] | **다름** — 두 점 하중 해석의 계수는 다접촉 입자에 그대로 맞지 않는다 [카드 해석] |
| 접촉 크기 | θ₀ < 5° (분석 범위) | AM–AM Hertz 반각 ≈7.5° (F/D² 109 MPa · 우리 코퍼스 중앙) · ≈9.3° (207 MPa) [카드 산술 · E* 74.67 GPa · F/D² 값 = 다른 카드 wheatcroft D13 · D16] | 원문 범위 밖 → 축 위 최대는 수렴 해 기준 0.89–1.0 F/d² (ν 0.3 · θ₀ 9–7.5°) (§7-3) |
| 탄성 상수의 역할 | 응력 / (F/a²) 은 **E 무관** · ν (m) 만 | DEM AM E 140 GPa · ν 0.25 (E* 74.67) · SE E_eff 1.35 GPa (18 배 연화) · MPM SE E 1.53 · ν 0.49 [우리 · 다른 카드] | 연화 E 는 θ₀ (접촉 크기) 를 통해서만 들어온다 [카드 해석] — 중심 응력 계수는 ν 로만 바뀐다 (ν 0.49 → 0.707 F/d²) |
| 크기 | 시편 2.5–9 cm | NCM 2 차 입자 D ≈10–12 µm [다른 카드] | 2,500–9,000 배 [카드 산술] — 결함 크기 · 입계 파괴 · 크기 효과 (wheatcroft σ ∝ D^−0.81) 는 이 논문 밖 |
| 검증 | 원판 시험과 1:1 · 평균 ±8 % · 단일 ×0.56–1.94 [판독] | DEM 파괴 표지 ↔ 실측 파쇄 수 대조 없음 [다른 카드 · song2025 · comparison C 절] | 이 논문의 1:1 대조 꼴은 R7 결과 전 대조의 본 |

### 7-2. ★ R7 강도 규약 — 우리 코드 · 보고에 쓸 때
- **규칙** [카드 해석]: 강도 값은 늘 **계수 c 와 함께** 적는다 (σ_F = c · P_f/D²).  우리 DEM 에서 비교할 양은 **하중** 이다: 문턱 하중 P_f = σ_F · D²/c 를 접촉력 (또는 입자 최대 접촉력) 과 견준다.  그러면 c 는 측정과 비교에서 상쇄되고 남는 것은 "실측 쪼개짐 하중" 뿐이다.
- **자기 일관 점검**: 우리 분류기 σ_nom = F/(2R)² (c 1) ↔ Wheatcroft σ_F (c 1) → **일관** [다른 카드 · wheatcroft L419].  Stallard 리뷰 값 (NMC333 185.6 MPa · c 2.8/π) 을 같은 분류기에 넣으면 문턱 하중이 11 % 낮아진다 (185.6 D² vs 208.2 D²) [카드 산술] → **c 1 로 바꿔 넣는다 (208.2 MPa)**.  같은 규약 (c 2.8/π) 인 Dang 2019 NMC111 평판 Weibull 평균 188 MPa 도 c 1 로는 **210.9 MPa** [다른 카드 · dang2019 D6 · ×π/2.8 = ×1.1220] — Wheatcroft 207 (c 1) 과 2 % 안 (dang2019 카드의 판정).
- **진응력으로 말하려면**: 탄성 구 중심 σθ = **0.786 F/d²** (ν 0.3) · 0.810 (ν 0.25) — Wheatcroft 207 MPa (c 1) 는 중심 진응력 **163 MPa** (ν 0.3) · 168 (ν 0.25) 에 해당 [카드 산술 · 탄성 · 두 점 하중 가정].  ⚠ 축 위 최대 인장은 접촉 크기에 따라 중심의 1.1–4 배 (θ₀ 10–3° · ν 0.3 · θ₀ → 0 이면 하중점 쪽으로 커진다 · §3-5) — "입자 인장강도" 를 하나의 진응력 값으로 옮기지 않는다.
- **12 % 의 크기 감각**: 규약 차 (11–12 %) 는 이 논문 자신의 단일 시험 산포 (×0.71–1.60 · 10–90 %) 보다 작지만 **체계 오차** (모든 값이 같은 쪽) 라 평균에는 그대로 남는다 [카드 해석].

### 7-3. 접촉 크기 θ₀ — 우리 AM–AM 접촉은 원문 범위 밖 [카드 산술 · 가정 명시]
- 같은 두 구 (반지름 R) 의 Hertz 접촉: a_c = (3FR*/(4E*))^{1/3} · R* = R/2 · F = σ_nom · (2R)² → **sin θ₀ = a_c/R = (1.5 σ_nom/E*)^{1/3}** (크기 무관).
- E* 74.67 GPa (우리 fracture_model 의 AM–AM 값 · E 140 · ν 0.25 [다른 카드 · wheatcroft D13]) 에서 σ_nom = 109 MPa (우리 코퍼스 AM_P–AM_P 중앙 접촉 F/D² [다른 카드 · wheatcroft D16]) → **θ₀ ≈ 7.5°** · 207 MPa (Wheatcroft 평판 강도) → **≈9.3°**.
- 원문 분석은 θ₀ < 5° · 수렴 해 (ν 0.3) 로는 θ₀ 7.5° → 축 최대 **1.02 F/d²** · 9° → **0.89** · 중심 0.76–0.77 [카드 산술 · §3-5] — 우연히 원문 0.9 근처.
- ⚠ 가정: Hertz 꼴 (타원 압력) ≠ 원문의 고른 압력 모자 · 두 점 하중 · 탄성 · 우리 입자는 SE 에 싸여 여러 접촉으로 하중을 받는다 → 이 숫자는 **범위 감각** 이지 보정값이 아니다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **단일 입자 탄성 역학 (해석해) + 강도 규약 + 실험 대조**.  우리 분업으로는 DEM 쪽 (접촉력 → 파괴 판정 · R7) 에 넣을 **판정 문턱의 규약** 과, MPM / 입자별 FE 쪽 (입자 안 응력장) 의 **단일 입자 해석 기준** 을 준다.
- 없는 반쪽: 다입자 · 재배열 · 소성 · 파괴 진행 (균열 성장) · 탈압.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = 암석 8 종 (cm) · 광탄성 에폭시 — **LPSCl · NCM 과 재료 · 크기 · 하중 조건이 다르다**.  기공 · 진밀도 값 없음 → 랩 표준과 나란히 놓을 숫자 없음.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **강도 규약 등록 칸** — 파괴 판정 문턱을 결과 전에 적을 때 "σ_F 값 · 계수 c (1 · 2.8/π · 0.9) · 시험 (평판 · 원뿔 · 원판) · d 의 정의 (지름 · 하중점 거리)" 를 함께 적는다 · 비교는 하중 공간 (P_f = σ_F D²/c) | 기공 · 진밀도 · 압력별 곡선 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ 2D 짝의 공식 S_t = 2F/(πdt) (불규칙 판 · 선하중 · p.98) — 2D 판 지름 압축 단위 시험의 기준 하중 꼴 (응력 분포는 이 논문에 없음) | 2D 응력 분포식 · 오차 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 (접촉 = 고른 압력 모자 · 마찰 없음) | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 기공에 맞춤) | 없음 | 순수 SE · 항복 · 기공 없음 |
| **단계 5** (3D 복합 압밀) | 조건 R7 의 판정 문턱 규약 (아래) · AM 입자가 깨지는지 보고할 때 "max 접촉력 / D²" 의 계수 표기 | 복합 · 다접촉 조건의 계수 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 (하중 증가 → F₀ 만) | — |
| **단계 7** (형상 · 피복 · 수송) | 없음 | — |
| **후보 D0** (지금 DEM) | 우리 c 1 분류기 ↔ Wheatcroft c 1 = 자기 일관 확인 · Stallard 값 (c 2.8/π) 은 ×1.122 로 바꿔 써야 함 (§7-2) · DEM 에는 입자 쪼개짐이 없고 사후 표지뿐 — 이 식은 표지 문턱의 꼴 | 다접촉 입자의 쪼개짐 하중 · 크기 효과 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계 조건 꼴 — 마찰 없는 고른 수직 압력 모자 (10a) · 점하중 극한 p = F/{2πa²(1 − cos θ₀)} | 마찰 · 분리 없음 |
| **후보 A** (MPM · AM 강체 · SE 한 장) | 없음 — AM 이 강체라 안쪽 응력이 없다 → 파괴 판정은 접촉 하중으로만 (이 식의 규약) | — |
| **후보 A′** (MPM 입자별 속도장) | ★ AM 을 변형체로 두면 입자 안 σθ 를 직접 읽을 수 있다 → 기준 = 탄성 구 해석 (중심 σθ = 21/(14+10ν) F/2πa²) · 판정은 진응력 강도와 (c 와 분리) | NCM 진응력 강도 값 없음 |
| **후보 B** (입자별 FE + 접촉) | ★ 단일 입자 검증해 — 중심 닫힌 꼴 + 축 위 급수 (수렴 · θ₀ 의존) · wheatcroft FE 판독과 같은 꼴 | 다결정 · 입계 · 균열 진행 없음 |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 — 하중점 근처 "crushing" 을 가능성으로만 (p.96) | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 | — |
| **U0–U6** | ★ **U1** (입자 하나 압축 · 해상도): 탄성 구 지름 압축의 해석 기준 — 중심 (σθ)₀ = 21/(14+10ν) · (σr)₀ = 1 + 10(2ν+7)/(10ν+14) · 중심 평균 응력 = 1 (모두 F/2πa² 단위 · E 무관) → 지름당 셀 수를 바꾸며 중심 값의 수렴을 본다 · ⚠ 하중점 근처 값은 θ₀ · 급수 항 수에 민감 (원문 그림 자체가 네 항 자름과 맞음) — 비교는 중심에서 | U0 · U2 · U3 · U4 · U5 · U6 없음 |
| **R1–R7** | ★ **R7** (AM 파괴): 규약 원전 — S_t ≑ 0.9 F₀/d² (≡ 2.8/π) · 계수 1 아님 · 근거 = 탄성 구 중심 응력 + 10 % · 적용 = 두 점 하중 · 인장 쪼개짐 · θ₀ < 5° · m 3–7 · 암석 검증 (평균 ±8 % · 단일 ×0.56–1.94) | R1–R6 없음 · NCM 2 차 입자 (다결정 · 입계 파괴 · µm · 다접촉 · SE 속) 의 계수 · 값 없음 |
| **결과 전 대조 항목** | ① (U1 · 후보 A′ · B) 단일 탄성 구 지름 압축: 중심 σθ = **21/(14+10ν) F/(2πa²)** (ν 0.3 → 0.786 F/d²) · 중심 σr = 1 + 10(2ν+7)/(10ν+14) · 평균 응력 F/(2πa²) — 해석해 · 맞추는 데 쓰지 않음 ② (R7 보고) "max 접촉력 / D²" 를 c 1 로 세고 문턱도 c 1 값으로 (Wheatcroft 207 · 67 MPa · Stallard 185.6 → 208.2) ③ (2D ↔ 3D) 2D 판 문턱 2F/(πDt) 와 3D 구 0.9 F/d² 를 섞지 않는다 (같은 F · d 에서 1.41 배) | 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 (다른 양) |

- **재료 · 차원 · 조건 차이**: 암석 (대리석 … 이암) ↔ NCM811 다결정 2 차 입자 + LPSCl · 2.5–9 cm ↔ ≈10 µm · 두 점 하중 ↔ 다접촉 + 무른 SE 매트릭스 · 정적 실온 [미확인] ↔ 300 MPa 압밀 중 · 3D (구 · 덩어리) 와 2D (판) 를 둘 다 준다.

## 9. 적용 인사이트 (행동)
1. **R7 문턱의 규약 칸을 등록한다 (단계 0 · R7)**: 문헌 강도마다 c (1 · 2.8/π · 0.9) · 시험 꼴 · d 정의를 적고, DEM 비교는 하중 공간에서.  Stallard 185.6 MPa (c 2.8/π) 는 우리 c 1 분류기에 **208.2 MPa** 로.
2. **U1 해석 기준으로 쓴다**: MPM · 입자별 FE 의 단일 구 지름 압축 시험에서 중심 σθ = 21/(14+10ν) F/(2πa²) (E 무관) 을 결과 전 대조 값으로 — 하중점 근처는 접촉 크기 · 해상도 · 급수 항 수에 민감하니 중심에서 견준다.
3. **"입자 인장강도" 를 진응력 하나로 쓰지 않는다**: 명목 (F/D²) ↔ 중심 진응력 (×0.79 · ν 0.3) ↔ 축 위 최대 (×1.1–4 · θ₀ 10–3° · ν 0.3) 를 구분해 보고.
4. **2D 결과를 3D 로 옮기지 않는다**: 같은 쪼개짐이라도 판 (2F/πdt) ↔ 덩어리 (0.9F/d²) 의 계수가 1.41 배 다르다.
5. **2 차 인용 정정 표지**: 서지 쪽 = 89–99 · 인자의 출처 = 탄성 구 해석 (불규칙 조각은 적용 범위) · 계수 1 은 Wheatcroft 의 선택 (원문 0.9).
6. **흐름 밖 (문헌 검증 습관)**: 오래된 해석 그림은 급수 항 수 · 계산 방법이 결과를 바꾼다 — 원문 식으로 다시 계산해 경계 조건 (σr → p · σθ → (1+2ν)p/2) 을 지키는지 본 뒤 쓴다 (이 카드 §3-5).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Following Hiramatsu and Oka (Int. J. Rock Mech. Min. Sci. 3 (1966) 89–99), the nominal tensile strength of an irregular lump compressed between two points is S_t ≈ 0.9 F₀/d² (equivalently 1.4 F₀/2πa² = 2.8 F₀/πd²), derived from the centre value of the hoop stress on the loading axis of an elastic sphere (1.21–1.36 F/2πa² for contact half-angles below 5° and Poisson's numbers 3–7, plus about 10 %) and checked against disk (Brazilian) tests on eight rocks."
- "The coefficient 1 in σ_F = P_f/D² is a convention, not the Hiramatsu–Oka value (0.9); strengths quoted with different coefficients must be compared as critical loads."
- 국문 (한정어와 함께): *"Hiramatsu–Oka (1966) 의 강도 식은 S_t ≑ 0.9 F₀/d² (= 2.8F₀/πd²) 이다 — 탄성 구의 하중 축 중심 인장 응력 (1.21–1.36 F/2πa², θ₀ < 5° · ν 0.14–0.33) 에 10 % 를 얹은 명목 값이고, 암석 8 종에서 원판 강도와 평균 ±8 % 로 맞았다 (단일 시험은 ×0.56–1.94 · Fig. 7 판독).  계수 1 (σ_F = P_f/D²) 은 원문 꼴이 아니다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-9 의 1–5.
**카드가 본 한계**
1. **명목 규약** — 진응력이 아니다 · 축 위 최대는 접촉 크기에 따라 중심의 1.1–4 배 (수렴 해 · θ₀ 10–3° · ν 0.3 · m 3 · θ₀ 1° 면 r/a 0.95 에서 24 배 · §3-5).
2. **원문 Fig. 5 · '최대 10 %'** 는 카드 재계산 (수렴) 과 다르다 — 네 항에서 자른 급수와 맞는다 · 원문 계산 방법 [미확인] · 카드 재계산은 독립 FE 로 축 전체를 대조하지 않았다 (wheatcroft FE 판독 셋과만).
3. **두 점 하중 · 마찰 없음 · 균질 탄성** — 다접촉 · SE 에 싸인 다결정 NCM 2 차 입자의 응력 상태와 다르다.
4. **θ₀ < 5° 분석** — 우리 AM–AM 접촉 (Hertz 7.5–9.3° [카드 산술]) 은 범위 밖.
5. **암석 cm 시편** — 크기 효과 (Weibull · 결함) · 입계 파괴 · Li 함량 의존 강도 없음.
6. **Fig. 7 판독**: H (이암) 덩어리는 겹친 찬 원이라 개수 · 중심 불확실 · "six bigger marks" 중 넷만 식별 · 원판 강도식은 원판에 대해 인쇄 안 됨.
7. **장치 · 조건 [미확인]**: 돌기 "7·5 cm in radius" 의 뜻 · 하중 속도 · 온도 · 습도 · 암석 물성.
8. **2 차 인용 서지** (89–90) 는 원문 (89–99) 과 다르다 · 학술지 꼬리 "Geomech. Abstr." 는 1966 머리글에 없다.
9. **전이 한계**: 절대값 0 건 — 규약 · 해석 꼴 · 기하 계수만.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [6] | AKAZAWA T. A new testing method to find the tensile strength of concrete, J. Japan Soc. Civil Engrs 29, 777–787 (1943). | ★ 원판 지름 압축 (Brazilian) 시험의 원전 — Fig. 7 의 (S_t)_d 기준 시험 · 2D 공식 2F/(πDt) 의 근거 · 카드 없음 |
| [7] | CARNIERO F. L. L. B. and BARCELLOS A. Résistance à la Traction des Batons, Instituto National de Technologia, Rio de Janeiro (1949). | ★ 같은 시험의 다른 원전 (인쇄 철자 그대로 — "Carniero" · "Batons" · "National") · 카드 없음 |
| [5] | HOBBS D. W. A simple method for assessing the uniaxial compressive strength of rock, Int. J. Rock Mech. Min. Sci. 1, 5–15 (1963). | 불규칙 덩어리 압축 (압축강도) 방법 — 이 논문이 인장으로 바꾼 출발점 · 카드 없음 |
| [1] | PROTODYAKONOV M. M. and VOBLIKOV V. S. Determining rock strength with specimens of irregular shape, Ugol 32, (4) (1957). | 불규칙 시편 강도 시험의 계보 (러시아어 · 구하기 어려움) |
| [2] · [3] · [4] | Protodyakonov 1960 (Int. Conf. Strata Control, Paper C2) · Ilivitskii & Nickolin 1961 (Ugol 36, (1) 34–36) · Evans, Pomeroy & Berenbaum 1961 (Colliery Engng 38) | 같은 계보 — 우리 계획과 거리가 멀다 |

## 13. [미확인] 목록 (15 쪽 전수에 없음)
1. 호 · 출판일 · DOI 의 인쇄 (메타 PII 만) · 연구비.
2. 급수의 계산 방법 · 더한 항 수 (Fig. 5 · '1.21–1.36' · '10 %' 의 계산 조건).
3. 1·4 를 고른 규칙 (중심 1.21–1.36 × 1.1 의 어느 값인지).
4. 돌기 *"7·5 cm in radius"* 의 뜻 · 접촉 크기 (θ₀) 의 실측.
5. 하중 속도 · 온도 · 습도 · 암석별 시험 수 · 암석 물성 (E · ν · 밀도 · 기공 · 입도).
6. 원판 강도 (S_t)_d 를 셈한 식 (원판에 대해) · 판 시험의 시험 수 · 결과 그림.
7. Fig. 7 의 "six bigger marks" 중 나머지 둘의 암석 · 산포 통계.
8. 광탄성 줄무늬 차수 · 정량 응력.
9. 직육면체 *"15 cm × 15 cm in sectional area, 8·8 cm high"* 의 단면 · 높이 뜻.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 스캔 15 쪽 전부를 150–300 dpi 렌더로 읽음 (글자 층 OCR 은 수식 · 일부 캡션이 깨져 렌더 기준).  서지 = 첫 쪽 쪽 머리 (*"Int. J. Rock Mech. Min. Sci. Vol. 3, pp. 89–99. Pergamon Press Ltd. 1966. Printed in Great Britain"*) · 제목 · 저자 · 소속 · 접수일 (1966-01-21) · 쪽 머리 (p.90–99) · PDF 메타 제목 (PII).  원문 낱말 셈: DEM · discrete · particle 0 회 · plastic 0 회 · "perfectly elastic" 1 회 (p.97) · unload 0 회.
- 그림 크롭 **46 장** = 도구 3 (Fig. 2 판 1 · Fig. 6 · Fig. 8 — **셋 다 다시 자름**: 쪽 폭 전체 · 캡션 없음 → 사진 rect ∪ 라벨 ∪ 캡션; 첫 재시도 (잉크 경계) 에서 사진 가장자리가 잘려 사진 rect 기준으로 한 번 더) + 손 크롭 43 (그림 7 = Fig. 1 · 2b · 2c · 3 · 4 · 5 · 7 · 식 23 · 근거 문단 13).  크롭마다 테두리 잉크 검사 · 이웃 줄과 붙었거나 식 아래가 잘렸던 손 크롭 (eq_02af · eq_08ab · eq_08c · eq_10a · eq_10b · eq_13 · txt_p13_extension · fig_3 머리 · fig_4) 은 잉크 틈 좌표로 다시 자름 · 46 장 전부 Read 로 열어 확인.  `figures.json` 의 `recrop` · `manual_crop` · `note_manual`.
- 판독: digitized.csv 62 행 — Fig. 7 (축 맞춤 · 표지 53 · 암석 기호) · Fig. 5 (중심 값 · 0 교차).  재계산: 원문 식 (11) · (12a) · (12b) 를 축 위에서 N = 2 … 4000 항까지 (§3-4 닫힌 꼴 · §3-5 표 · 경계 점검 σr → p · σθ → (1+2ν)p/2).
- 2 차 인용 대조: 정본 카드 wheatcroft2023 (L27 · L150 · L194 · L224 · L234) · stallard2022 (L27 · L82 · L240 · L273 · L418 · L439 · L508) · 후보 표 N-11 · comparison_vs_ours_DEM.md L4497 — 고치지 않았다 (카드 문제 = 정독 출력 batch_53 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (536 → 작성 중 537) + DOI (0148-9062) · 제목 낱말 ("irregular test piece" · "tensile strength of rock") · 저자 (Hiramatsu · Oka) grep — 카드 없음 (인용만: stallard2022 · wheatcroft2023 · 작성 중 들어온 dang2019 · S8_candidates · comparison_vs_ours_DEM) (2026-11-12).  같은 저자 · 같은 해 다른 카드 없음.

## 🔗 관련 카드
- 이 식을 쓴 NMC 입자 강도: `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` (c 1 · FE 응력 분포) · `stallard2022_cathode_mechanical_properties_review` (c 2.8/π · K_IC 추정) · `dang2019_nmc111_secondary_particle_flat_punch_fracture_strength` (c 2.8/π · 평판 · Weibull 188 MPa) · `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` (DEM σm = f_max/d²).
- 다른 강도 시험 · 입자 기계 물성: `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` (직접 인장) · `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` · `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` · `song2025_porous_argyrodite_modulus_fracture_toughness` (SE 쪽 파괴).
- 입자 분할을 실제로 내는 계산: `tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
