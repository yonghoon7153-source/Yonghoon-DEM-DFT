<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-10 · 정독 52) 에서 꼭 뽑으라고 한 항목.
     본 = wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md (같은 질문 · 같은 꼴 — 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 · 파생 원장) · 두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 날의 kawaguchi2018_dry_coating_model_se_particle_powtec.md 와 같은 꼴.
     쪽 표기 = 인쇄 쪽 p. A2749–A2751 (PDF N 쪽 = 인쇄 A2747 + N · PDF p.1 = 출판사 내려받기 표지) · 보충 자료 = "SI p.1–3" (쪽 번호 1–3 인쇄).  크롭 파일 이름의 p2749 … 는 인쇄 쪽 · figures.json 의 page 는 PDF 쪽.
     값 표지: [인쇄] = 본문 · 그림 안 글자로 적힌 값 · [SI] = 보충 자료에 인쇄된 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 143 행 — 원본 래스터 화소 · 방법 · 자체 검산은 그 파일 머리) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · §13 원장) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [그림 관찰] = 크롭을 보고 적은 정성 서술 · [미확인] = 본문 3 쪽 + SI 3 쪽 전수에 없음 · [2차] = 다른 카드에 적힌 값 (그 카드 위치 병기).
     원문 6 쪽 (본문 3 + SI 3) 은 글자 층 추출 + 쪽 렌더로 읽었다.  번호 붙은 식 1 개 (식 [1]) + SI 식 2 개 ((S1) · (S2)) · 그림 3 + SI 5 · 표 0 + SI 2 · 참고문헌 19 + SI 3.  시뮬레이션 (DEM · FEM · MPM) 없음 — 실험 Communication. -->

# NMC111 2차입자 **평판 압입 (flat punch indentation) 파괴강도 S_t ≈ 2.8F_c/(πd²)** (Hiramatsu–Oka) — pristine **Weibull 평균 188 MPa** (S₀ 205 · m 4.8 · 입자 33) → 전해질 침지 165 · 첫 탈리튬화 **22** · 첫 리튬화 **70** MPa, 파괴는 **입계** 위주 · 원자료 129 입자 (SI 표 S2) — Wheatcroft 2023 이 2차 인용한 "NMC111 평판 188 MPa" 의 1 차 자료 · DEM AM 파쇄 판정의 평판 쪽 끝 — Dang · Wang · Cheng (*J. Electrochem. Soc.* 166 (13) A2749–A2751 (2019))

> slug `dang2019_nmc111_secondary_particle_flat_punch_fracture_strength` · DOI `10.1149/2.0331913jes` · type `exp (single-particle flat punch indentation — Nanoindenter G200, diamond flat punch nominal Ø40 µm, Ar glove box, load control 1 mN/s; NMC111 (Umicore) secondary particles d ≈6–23 µm: pristine · electrolyte-soaked 48 h · 1st delithiation · 1st lithiation (liquid half-cell, C/10, 3–4.3 V); strength S_t ≈ 2.8F_c/(πd²) (Hiramatsu–Oka); two-parameter Weibull (Origin); SEM)` · PDF `ceb387e9-10._Communication_Fracture_Behavior_of_Single_LiNi0.33Mn0.33Co0.33O2_Particles_Studied_by_Flat_Punch_Indentation.pdf` (4 pp = 표지 1 + 본문 3) + SI `5d30a24f-10._Sup_Communication_Fracture_Behavior_of_Single_LiNi0.33Mn0.33Co0.33O2_Particles_Studied_by_Flat_Punch_Indentation.pdf` (3 pp) · digested `2026-11-12` · status ✅

> elements: Li, Ni, Mn, Co, O

> **원제**: *Communication—Fracture Behavior of Single LiNi0.33Mn0.33Co0.33O2 Particles Studied by Flat Punch Indentation* (p. A2749)
>
> **읽은 범위**: 본문 3 쪽 전부 (글자 층 + 쪽 렌더 · 참고문헌 19 편 전수) · **SI 3 쪽 전부** (Fig. S1–S5 · Table S1–S2 · 식 (S1)–(S2) · 참고문헌 3).  그림 · 표 10 장 + 식 3 + 근거 문단 14 = 크롭 27 장 전부 열어 확인 (§5-1).
> 본문 그림 셋은 **래스터** (Fig. 1 = 1200 × 930 px · Fig. 2 = 1200 × 1048 · Fig. 3 = 777 × 1751 px, ≈300 dpi) — Fig. 3b 의 입자 지름을 원본 화소에서 읽어 **SI 표 S2 의 인쇄 강도 129 개 중 126 개에 짝지었다** (§3-4).
> **절대값 전이**: pristine 강도는 **NMC111 · 건조 · 상온 · 아르곤 · 평판 두 점 하중** 의 값이다 — 우리 NCM811 다결정 AM_P 에 그대로 옮기는 값이 아니라 **판정 문턱의 자릿수 · 산포 (Weibull m) · 규약의 기준**으로 쓴다.  순환 값 (침지 · 탈리튬화 · 리튬화) 은 **액체 전해질 반쪽셀 · NMP 80 °C 추출** 이력이라 ASSB 로 옮기지 않는다.  LPSCl (SE) 값은 없다.

---

## 0. 결론 먼저 — 이 카드를 연 질문 (후보 N-10 · 조건 R7)

우리 DEM 은 AM–AM 접촉을 **Auerbach 임계하중 P_c = A·K_IC²·R/E\*** (A 200 · K_P 0.3 · E\* 74.67 GPa) 과 Lawn 배수 (1 · 3 · 11 · 32 × P_c) 로 **분류**한다 ([2차] `wheatcroft2023_…` §7.3).  그 카드는 강도 기준의 두 끝을 원뿔 67 / 평판 207 MPa (NMC811) 로 잡았고,
그 비교 문헌 *"NMC111 평판 평균 188 MPa [21]"* 를 **원문 미확인** 으로 남겼다 (wheatcroft L34 · L91 · L189 · L535).  `stallard2022_…` 리뷰 카드도 *"원고에는 1차 논문 (… Dang 2019 …) 을 인용"* 하라고 적었다 (L431).  원문을 대조한 결과:

| 확인 항목 | 원문 (쪽) | 판정 |
|---|---|---|
| 재료 | **LiNi0.33Mn0.33Co0.33O2 (NMC111), Umicore** — *"Spherical NMC secondary particles, which are micro-sized agglomerations of submicron primary particles"* (p. A2749) | 다결정 2차입자 (1차입자 크기 숫자 [미확인] — "submicron" 만) · 우리 AM_P (NCM811 다결정) 와 **부류는 같고 조성 · 공급사는 다르다** · AM_S (단결정 규약) 는 대상 밖 |
| 시험법 | **Nanoindenter G200 (Agilent) + 다이아몬드 평판 압자 (명목 지름 40 µm)**, 아르곤 글러브박스 안 · **건조** · 입자를 평판 가운데에 둠 · **하중 제어 1 mN s⁻¹** (부하 · 제하) · 기판 = 매끈한 **다결정 다이아몬드** (p. A2749) | [인쇄] · 입자 하나씩 두 점 (평판 – 기판) 지름 압축 |
| **강도 정의** | 식 [1] **S_t ≈ 2.8F_c/(πd²)** — Hiramatsu & Oka [17] (p. A2750) · F_c = 변위가 갑자기 뛰는 하중 (*"the load corresponding to the breakage of particles"*) · d = **현미경 투영 면적에서 계산한 지름 (ImageJ, 누르기 전)** (p. A2749) | ✅ **계수 2.8/π ≈ 0.891** [카드 산술] — Wheatcroft (계수 1, σ = P_f/D²) 와 **다른 규약** · `stallard2022_…` 식 4 와 **같은 규약** |
| **"188 MPa"** | **SI 표 S1** pristine **S_m = 188 MPa** (S₀ 205 · m 4.8) + 본문 Fig. 3c 의 글자 *"S_m=188 MPa, S_0=205 MPa, m=4.8"* — **본문 문장에는 숫자가 없다** | ✅ 값은 있다 — 정의 = **Weibull 평균 S₀Γ(1+1/m)** (식 S2) · 규약 2.8/π · 평판 · pristine · 건조.  [카드 산술] SI 표 S2 33 개의 **산술 평균도 188.3** · 중앙값 182.6 |
| 표본 수 · 산포 | 본문에 n · ± 없음 · **SI 표 S2 = 원 자료 전부** (pristine **33** · 침지 **34** · 첫 탈리튬화 **29** · 첫 리튬화 **33** 개 — 행 수 [카드 산술]) · Weibull m **4.8 · 4.8 · 4.1 · 4.1** [SI 표 S1] | [카드 산술] SD (N−1) 40.9 · 36.8 · 6.3 · 19.3 MPa (CV 0.22 · 0.22 · 0.28 · 0.28) · 표 S1 의 (S₀, m) 은 **최대가능도 (MLE) 로 재현** (회귀가 아님, §3-4) |
| 입경 의존 | 저자: *"the fracture strength of NMC secondary particles at all states is, statistically, independent of the particle size"* (p. A2750) · F_c ∝ d² (식 [1]) | [판독 + 카드 산술 §3-4] pristine 기울기 **−0.16 [−0.40, +0.09]** (유의 아님 = 저자와 같음) · 그러나 **첫 리튬화 −0.62 [−0.81, −0.42]** · 침지 −0.29 [−0.50, −0.09] 는 유의 — "모든 상태에서 무관" 은 **pristine 에만** 선다 |
| 파괴 꼴 | *"mainly inter-granular with some trans-granular fracture events"* (Fig. 2c–2d · S4, p. A2750) · 부서진 입자 = 1차입자 다발로 흩어짐 (Fig. 2c · S4) | ✅ 우리 A10 *"poly = 입계"* 와 같은 방향 · Auerbach 원뿔 균열은 관찰 대상이 아니었다 |
| 순환의 영향 | 서열 *"uncycled (i.e., pristine and electrolyte-soaked) > 1st-lithiation > 1st-delithiation"* · 침지 S_m 은 pristine 보다 **12 % 작다** (p. A2750) · 기전 = 첫 탈리튬화에서 1차입자가 **∼5 % 작아짐** → 계면 결함 (p. A2750–A2751, 측정 근거 미제시) | [카드 산술] S_m 비: 침지 0.878 · 첫 리튬화 **0.372** · 첫 탈리튬화 **0.117** (pristine 기준) |
| E · K_IC · 경도 | **없다** — modulus · hardness · yield · elastic 0 회 · toughness 1 회 (정성: *"Trans-granular fracture depends on the fracture toughness of NMC primary particles"*) | ⛔ E_AM · K_IC 의 출처가 될 수 없다 |

**한 줄 판정** — Wheatcroft 이 옮긴 *"NMC111 평판 188 MPa"* 는 **원문에 있다 (SI 표 S1 · Fig. 3c)** — 단 그것은 **2.8/π 규약의 Weibull 평균** 이고, Wheatcroft 자신의 207 MPa 는 **계수 1 규약** 이다.  같은 규약 (F/d²) 으로 맞추면 **Dang NMC111 211 ↔ Wheatcroft NMC811 207 MPa** — 서로 다른 연구실 · 조성 · 공급사의 평판 강도가 **2 % 안에서 만난다** [카드 산술].
⇒ R7 판정 창의 **평판 (두 점 · 무딘 접촉) 끝** 이 독립 자료 하나로 굳는다 (n 33 · Weibull m 4.8 · 원 자료 공개).  우리 코퍼스의 AM_P–AM_P **중앙 접촉 (F/D² 109 MPa, [2차] wheatcroft D16)** 은 이 분포에서 Weibull 파괴 확률 **≈2.8 %** 자리다 (pristine · 두 점 하중 가정 · §7-4).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-10 의 '왜' 칸)

의도 원문: *"c · 조건 R7 — 평판으로 누른 NCM 2 차입자 파괴 강도의 1 차 자료 · Wheatcroft p.4 의 'NMC111 평판 평균 188 MPa' 는 2 차 인용 · 원문 미확인 (wheatcroft L34 · L91) · stallard2022 도 '원고에는 1차 논문 (… Dang 2019 …) 을 인용' 하라고 적음 (L431)"* (가리킨 카드 = `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` L189 · L34 · L91 · `stallard2022_cathode_mechanical_properties_review` L239 · L431).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "평판으로 누른 NCM 2 차입자 파괴 강도의 1 차 자료" | **채움** | p. A2749 (방법) · 식 [1] (p. A2750) · Fig. 3 (p. A2751) · SI 표 S1 · S2.  **NMC111 다결정 2차입자 (Umicore)** · 다이아몬드 평판 명목 Ø40 µm · Nanoindenter G200 · 하중 제어 1 mN s⁻¹ · **건조 · 아르곤 글러브박스 · 상온 (온도 숫자 [미확인])** · **누른 채 (부하 중) 의 파괴 하중** — 압력을 뺀 뒤의 값 아님 · d = 투영 면적 지름 (누르기 전) · 네 상태 129 입자 |
| "Wheatcroft p.4 의 'NMC111 평판 평균 188 MPa'" | **채움 (값 · 재료 · 기하 일치 · 규약 주의)** | **SI 표 S1** pristine S_m **188** MPa (S₀ 205 · m 4.8) · Fig. 3c 글자 같음.  "평균" = Weibull 평균 S₀Γ(1+1/m) (식 S2) — [카드 산술] 표 S2 의 산술 평균 188.3 과도 같다.  ⚠ 규약 = **2.8F_c/(πd²)** (계수 0.891) — Wheatcroft 207 (계수 1) 과 나란히 놓으려면 188 × π/2.8 = **210.9** MPa [카드 산술] |
| "원문 미확인 (wheatcroft L34 · L91)" | **풀림** | 위 두 행 — 원문 확인됨.  Wheatcroft 카드 L535 (D24) 의 *"(Dang NMC333 비교 188 은 규약 미확인)"* 도 이제 답이 있다: **Hiramatsu–Oka 2.8/π 규약** |
| "stallard2022 도 1차 논문을 인용하라고 적음 (L431)" | **채움 (1 차 값 확보)** | 리뷰 Fig. 10C · 13A 의 NMC333 이차입자 상자그림 (그 카드의 vector-read) 의 원 자료 = 이 논문 SI 표 S2 — 수염 · 상자 · 중앙을 원 자료로 재계산해 대조 (아래 표) |
| (질문 c) "항복 · 경도 · 크리프 값과 정의 · 일축 항복 환산" | **일부** | **파괴 강도** (Hiramatsu–Oka 의 인장 강도 추정) 만 — 항복 · 경도 · 크리프 · 영률 **없음**.  S_t 는 "두 점 압축된 불규칙 취성 조각의 인장 강도" 근사 (식 [1] 의 원전 [17] 은 정본 카드 없음 · 후보 N-11) |
| (조건 R7) "AM 파괴" | **채움 (입자 한 개 · 두 점 · 고립)** | 파괴 문턱 F_c(d) · S_t 분포 · 파괴 꼴 (입계).  다접촉 · 전극 속 · SE 와 섞인 상태 · 압밀 중 파괴는 **없음** |

**가리킨 카드 · 같은 논문을 인용한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 내용 | 원문 | 판정 |
|---|---|---|---|
| `wheatcroft2023_…` L34 · L91 | *"NMC111 평판 평균 188 MPa [21] (p. 4) — 2차 인용 · 원문 미확인"* | SI 표 S1 S_m 188 · 평판 · NMC111 ✓ — 규약 2.8/π (Weibull 평균) | **같음** (값 · 재료 · 기하).  카드의 "미확인" 은 이 카드로 풀린다 — 그 카드가 틀린 것은 아님 · 갱신 대상 |
| `wheatcroft2023_…` L189 | [21] 서지 *"D. Dang, Y. Wang, Y.-T. Cheng, J. Electrochem. Soc. 2019, 166, A2749–A2751."* | 같음 (호 13 · 제목은 Wheatcroft 목록에 없음) | **같음** |
| `wheatcroft2023_…` L535 (D24) | *"(Dang NMC333 비교 188 은 규약 미확인)"* | 규약 = 2.8F_c/(πd²) (식 [1]) | 풀림 — 같은 규약 (F/d²) 으로는 **210.9 ↔ 207** [카드 산술] · 갱신 대상 |
| `stallard2022_…` L239 | [107] 서지 (Dang, Wang, Cheng 2019 · 제목 · J. Electrochem. Soc. 166, A2749–A2751 · DOI) | 같음 (호 13 빠짐 · 제목 대소문자만 다름) | **같음** |
| `stallard2022_…` L115 · L158 · L27 · L375 · L526 | NMC333 이차입자 pristine **중앙 185.6** (상자 156.3–216.0 · 수염 128.3–289.2) [그 카드: 리뷰 Fig. 10C vector-read] | SI 표 S2 pristine 33 개: 최솟값 **128.3** · 최댓값 **289.2** ✓ · 사분위 (중앙 뺀 반쪽 중앙) **156.3 · 215.95** ✓ · **중앙 = 182.6** (17 번째) | **일부 — 중앙만 3.0 MPa 다르다.**  [카드 산술] (182.6 + 188.5)/2 = **185.55** = 17 · 18 번째 값의 평균 — 리뷰 그림이 짝수 개처럼 중앙을 그었거나 판독 쪽 차이로 보인다 (리뷰 원 그림으로만 가를 수 있음 · 판정 보류).  그 카드 L181 의 *"건조 pristine 분모면 0.379"* 는 원 자료 중앙으로 **0.385** |
| `stallard2022_…` L176 | 13A 침지 107.6 · 134.0 · **158.9** · 192.2 · 241.8 / 첫 탈리튬화+재리튬화 30.0 · 53.8 · **70.3** · 82.5 · 118.0 / 첫 탈리튬화 9.4 · 17.1 · **21.5** · 28.2 · 33.8 | SI 표 S2 로 재계산: 침지 (n 34) 107.6 · 134.0 · 158.95 · 192.2 · 241.8 ✓ · 첫 리튬화 (n 33) 30.0 · 53.8 · 70.3 · 82.5 · 118.0 ✓ · 첫 탈리튬화 (n 29) 9.4 · 17.15 · 21.5 · 28.25 · 33.8 ✓ | **같음** (세 상자 15 값 전부 ±0.05 안) |
| `stallard2022_…` L176 · L91 | 상태 표지 *"x ≈ 0.92"* · *"x ≈ 0.33"* · 리뷰 문장 *"average fracture strength only 44% of … pristine"* | Dang 원문에 x 값 · "44 %" **없음** — Fig. 1c 용량 곡선 (판독 ≈184 · ≈185 → 163 mAh/g) 뿐 · S_m 비 70/188 = **0.372** · 70/165 = 0.424 · 중앙 비 70.3/158.95 = **0.442** [카드 산술] | 리뷰의 덧붙임 — 그 카드가 이미 *"44 % 의 분모는 침지 후"* 로 짚었다 ✓ (어긋남 아님) |
| `stallard2022_…` L115 | *"NMC333, 결정립 0.5–1 µm, pristine"* | Dang 원문 = *"submicron primary particles"* — **숫자 없음** (Fig. 2d 의 1 µm 스케일바로 ≈0.3–1 µm [그림 관찰]) | **일부** — 0.5–1 µm 는 리뷰의 귀속 (Dang 원문으로 확인 불가) |
| `stallard2022_…` L89 | 침지 조건 *"1 M LiPF₆/EC 48 h → DMC 세척 → NMP 80 °C 30 min → 건조"* | 전해액 = **1 M LiPF₆ in EC : EMC = 3 : 7 (v/v) + VC 2 wt%** (Gotion) · 침지 전극은 *"dispersed … in the same way as the cycled electrodes"* (DMC 세척 · NMP 80 °C 30 min · 초음파 10 s · 80 °C 30 min 건조) | **일부** — "EC" 만 적은 것은 줄임 (리뷰 문장인지 카드 요약인지는 리뷰 원문으로만) |
| `sedlatschek2026_…` L142 · L268 · L327 · L386 | *"188 MPa (평균 파괴 인장강도) · NMC111 다결정 입자 · flat punch"* · 서지 J. Electrochem. Soc. 166 (13) (2019) A2749–A2751 | ✓ (Hiramatsu–Oka 의 "인장 강도" 추정 · Weibull 평균) | **같음** — 규약 (2.8/π) 표기만 없다 |

- 후보 표 · 가리킨 카드 셋 (wheatcroft · stallard · sedlatschek) 이 이 논문을 **"카드 없음 (인용만)"** 으로 적고 있다 — 이 카드가 생겨 **낡은 표기**가 됐다 (고치지 않음 · 보고).

⇒ **의도 대조 결과: 채움** — 평판으로 누른 NCM (NMC111) 2차입자 파괴 강도의 1 차 자료이고, "188 MPa" 는 원문 SI 표 S1 에 있다 (2.8/π 규약의 Weibull 평균 · 산술 평균도 188.3) · 원 자료 129 개가 공개돼 있어 리뷰 그림의 값도 재계산된다.  **단 질문 c 의 항복 · 경도 · 영률은 없다 (일부)** · 다접촉 · 압밀 중 파괴는 없다.

---

## 1. 한 줄 요약

Kentucky 대학 (Y.-T. Cheng 그룹) 이 상용 **NMC111 다결정 2차입자 (Umicore)** 를 하나씩 **다이아몬드 평판 (명목 Ø40 µm)** 으로 아르곤 글러브박스 안에서 눌러, 변위가 갑자기 뛰는 하중 **F_c** 를 재고 **Hiramatsu–Oka 식 S_t ≈ 2.8F_c/(πd²)** 로 강도를 냈다.
**pristine · 전해질 48 h 침지 · 첫 탈리튬화 (4.3 V 충전) · 첫 리튬화 (3 V 방전)** 네 상태 129 입자의 강도를 **2 모수 Weibull** 로 정리 — S_m = **188 · 165 · 22 · 70 MPa** (m 4.8 · 4.8 · 4.1 · 4.1).  F_c 는 입경과 함께 커지고 (≈d²) 강도는 **입경과 무관** 하다고 저자는 결론짓는다 (원 자료 재분석으로는 pristine 에서만 무관 — §3-4).
파괴는 **입계 위주 (일부 입내)** 이고, 첫 탈리튬화에서 1차입자가 ∼5 % 줄어 생긴 계면 결함이 강도를 한 자릿수 떨어뜨린다는 해석.  ⇒ 우리에게는 **R7 (AM 파괴) 판정 창의 "평판 끝" 독립 앵커 + Weibull 산포 (m 4.8) + 강도 규약의 기준** 이다.  E · K_IC · 경도 · 압밀 · 다접촉 · SE 는 없다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Dingying Dang** (z · 교신) · **Yikai Wang** (\* · ECS 학생회원) · **Yang-Tse Cheng** (z · 교신) — dingying.dang@uky.edu · yang.t.cheng@uky.edu (p. A2749 꼬리) |
| 소속 | Department of Chemical and Materials Engineering, **University of Kentucky**, Lexington, Kentucky 40506, USA |
| 저널 | ***J. Electrochem. Soc.* 166 (13) A2749–A2751 (2019)** · *Communication* (3 쪽) · 머리글 *"0013-4651/2019/166(13)/A2749/3/$38.00 © The Electrochemical Society"* |
| DOI | `10.1149/2.0331913jes` (초록 끝) |
| 이력 | *"Manuscript submitted June 18, 2019; revised manuscript received July 29, 2019. Published August 13, 2019."* |
| ORCID | Dang 0000-0003-1243-9857 · Wang 0000-0002-1156-0324 · Cheng 0000-0003-0737-9212 |
| 자금 | NSF Award No. 1355438 · U.S. DOE Battery Materials Research (BMR) Program Contract DE-EE0007787 |
| 보충 자료 | *"Supplementary Material"* 3 쪽 (Word 판) — §1 장치 (Fig. S1) · §2 순환 입자 (Fig. S2) · §3 d ≈12.5 µm 하중–변위 (Fig. S3) · §4 Weibull (식 S1–S2 · 표 S1–S2) · §5 파괴 입자 (Fig. S4) · §6 셀 분해 손상 (Fig. S5) |
| 소재 | NMC111 (LiNi0.33Mn0.33Co0.33O2, **Umicore**) · 전극 92 : 4 : 4 wt% (NMC : PVDF (Alfa Aesar) : Super C65 (TIMCAL)) · NMP · 7.3 mg cm⁻² · **무압연** |
| 전해질 · 셀 | **액체** 1 M LiPF₆ in EC : EMC = 3 : 7 (v/v) + VC 2 wt% (Gotion) 500 µL · Li 박 · Celgard 2400 · **Swagelok 셀** (PFA-820-6) — ⚠ **ASSB 아님** |
| 연구 유형 | 실험 미세역학 (단일 입자 평판 압입) + 통계 (Weibull) + SEM |
| PDF 첫 쪽 | IOP 내려받기 표지 (*"To cite this article: Dingying Dang et al 2019 J. Electrochem. Soc. 166 A2749"*) — 본문은 PDF 2–4 쪽 |

## 3. 핵심 수치 ★

### 3-1. 헤드라인 — SI 표 S1 (Weibull) + 표 S2 원 자료의 기술 통계

| 상태 | S_m (MPa) [SI 표 S1] | S₀ (MPa) [SI] | m [SI] | n [카드 산술 — 표 S2 행 수] | 산술 평균 · SD (N−1) [카드 산술] | 중앙 · Q1 / Q3 (중앙 뺀 반쪽) [카드 산술] | 최소 – 최대 [SI 표 S2] |
|---|---|---|---|---|---|---|---|
| **pristine** | **188** | **205** | **4.8** | **33** | 188.3 · 40.9 | 182.6 · 156.3 / 216.0 | 128.3 – 289.2 |
| electrolyte-soaked (48 h) | 165 | 180 | 4.8 | 34 | 164.9 · 36.8 | 159.0 · 134.0 / 192.2 | 107.6 – 241.8 |
| 1st delithiation | **22** | 25 | 4.1 | 29 | 22.4 · 6.3 | 21.5 · 17.2 / 28.3 | 9.4 – 33.8 |
| 1st lithiation | **70** | 77 | 4.1 | 33 | 70.3 · 19.3 | 70.3 · 53.8 / 82.5 | 30.0 – 118.0 |

- 규약: 모두 **S_t ≈ 2.8F_c/(πd²)** (식 [1]) · 평판 · 건조 · 글러브박스.  P_f 열 (표 S2) = **i/N** (오름차순 i 번째 ÷ 상태별 개수) — 1/33 = 3.03 % ✓ · 1/34 = 2.94 % ✓ · 1/29 = 3.45 % ✓ [카드 산술].
- 본문 문장의 숫자: **73.8 mN** (Fig. 2a 입자의 F_c) · **16.2 µm** (그 입자 지름, Fig. 2 캡션) · **12 %** (침지 S_m 감소) · **∼5 %** (순환 부피 변화 — 서론 / 첫 탈리튬화 1차입자 크기 감소 — 논의) · **40 µm** (평판 명목 지름) · **1 mN s⁻¹** · 7.3 mg cm⁻² · C/10 · 3–4.3 V · 48 h · 80 °C 30 min · 10 s.  강도 숫자는 **본문 문장에 없고** SI 표 · Fig. 3c 글자에만 있다.
- [카드 산술] 표 S1 의 S_m 은 식 (S2) 로 재현된다: 205·Γ(1+1/4.8) = 187.8 · 180·Γ(1.208) = 164.9 · 77·Γ(1+1/4.1) = 69.9 · 25·Γ(1.244) = 22.7 (인쇄 22 — 반올림 안 한 모수 (MLE 24.72 · 4.054) 로는 22.4).
- [카드 산술] 비: 침지 / pristine S_m = **0.878** (*"12 % smaller"* ✓) · 첫 리튬화 / pristine **0.372** · 첫 탈리튬화 / pristine **0.117** · 첫 리튬화 / 침지 0.424 · 산술 평균 비도 0.876 · 0.373 · 0.119.

### 3-2. 그 밖의 인쇄 · 판독 수치

| 양 | 값 | 위치 · 표지 |
|---|---|---|
| Fig. 2a 입자 | d **16.2 µm** · F_c **73.8 mN** | [인쇄] Fig. 2 캡션 · p. A2749 |
| 그 입자의 강도 | 2.8 × 73.8 mN /(π × 16.2² µm²) = **250.6 MPa** (계수 1 로는 281.2) | [카드 산술] — 표 S2 pristine 의 **250.4 · 251.1** 둘 중 하나로 보인다 [카드 해석] |
| Fig. 2a 부하 가지 (선 중심 · 선 굵기 ≈250 nm) | 5 mN @ ≈160 nm · 20 @ ≈320 · 40 @ ≈470 · 60 @ ≈620 · 73 mN @ ≈750 nm | [판독] digitized.csv |
| Fig. 2a 파괴 직후 | 하중 ≈73.7 → 73.0 mN 거의 일정하게 변위 ≈0.8 → ≈11.4 µm (하중 제어 폭주 · **입자 지름의 ≈65 %**) → 조각을 다시 눌러 **≈79.6 mN @ ≈11.5–11.7 µm** → 0 까지 거의 수직 제하 | [판독] |
| 파괴 순간 겉보기 변형 | δ/d ≈ 0.75/16.2 = **0.046** | [카드 산술 · 판독] (프레임 순응 보정 여부 [미확인]) |
| 부하 기울기 (20 → 60 mN) | ≈**134 mN/µm** | [카드 산술 · 판독] |
| Fig. 1c 용량 (첫 탈리튬화 셀) | 충전 끝 ≈**184 mAh g⁻¹** @ 4.3 V | [판독] Fig. 1c |
| Fig. 1c 용량 (첫 리튬화 셀) | 충전 ≈185 → 방전 ≈**163 mAh g⁻¹** @ 3.0 V · 첫 쿨롱 효율 ≈0.88 | [판독] · [카드 산술] |
| Fig. S3 (d "about 12.5 µm") 평탄 하중 = F_c | pristine ≈49.6 · 32.9 · 24.2 · 침지 ≈37.8 · 28.7 · 28.3 · 첫 리튬화 ≈14.1 · 12.1 · 7.9 · 첫 탈리튬화 ≈5.0 · 3.8 mN | [판독 ≈ ±0.5 mN · 크롭 눈금] |
| 그 강도 (d = 12.5 µm 가정) | pristine ≈283 · 188 · 138 · 침지 ≈216 · 164 · 161 · 리튬화 ≈80 · 69 · 45 · 탈리튬화 ≈28.5 · 21.7 MPa | [카드 산술 — F × 5.70 MPa/mN] — 표 S2 범위 안 |
| Fig. S3 파괴 뒤 재부하 최대 | pristine ≈78.5 · 침지 ≈69 · 탈리튬화 ≈49 · 리튬화 ≈39.4 mN (변위 6–9.8 µm) | [판독] — 조각 덩어리를 누른 값 · 저자 분석 없음 |

### 3-3. ★ 원 자료 (SI 표 S2) 가 드러낸 것 — 입경 · 추정법 · 그림과의 결합 (§13 원장)

**(a) 그림 3b 의 지름을 원 자료에 붙였다.**  Fig. 3b 의 표지 중심을 원본 래스터에서 읽고 (눈금 최소제곱 — x 0.0343 µm/px · y 0.662 MPa/px, 눈금 잔차 ≤ 0.02 µm · 0.24 MPa), 상태마다 정렬한 판독 강도를 표 S2 의 인쇄 강도와 순서 보존 최소 차이로 짝지었다 —
**126 / 129 개** (pristine 32/33 · 침지 34/34 · 첫 탈리튬화 28/29 · 첫 리튬화 32/33) · |판독 − 인쇄| 중앙 0.13–0.96 · 최대 1.72 MPa.  못 찾은 셋 (pristine 217.0 · 탈리튬화 28.2 · 리튬화 85.5 MPa) 은 다른 표지 밑에 가렸다.
**검산**: F_c = S·πd²/2.8 로 되돌린 값이 Fig. 3a 의 판독 F_c 와 같은 d 에서 중앙 |차이| **0.08 (pristine) · 0.11 · 0.20 · 0.20 mN** — 그림 3 의 자료가 **식 [1] (2.8/π)** 로 그려졌음을 확인 [판독 + 카드 산술].

| 상태 | d 범위 (µm) [판독] | d 평균 · 중앙 | ln S_t ~ ln d 기울기 [95 %] · p | ln F_c ~ ln d 기울기 [95 %] |
|---|---|---|---|---|
| pristine (32) | **6.6 – 18.8** | 12.2 · 12.4 | **−0.16 [−0.40, +0.09] · 0.20** | **1.84 [1.60, 2.09]** |
| 침지 (34) | 6.2 – 21.8 | 13.4 · 13.4 | −0.29 [−0.50, −0.09] · **0.007** | 1.71 [1.50, 1.92] |
| 첫 탈리튬화 (28) | 6.2 – 20.5 | 12.2 · 11.7 | −0.30 [−0.63, +0.04] · 0.078 (Spearman 0.023) | 1.70 [1.37, 2.04] |
| 첫 리튬화 (32) | 5.7 – 23.1 | 12.5 · 12.0 | **−0.62 [−0.81, −0.42] · < 0.001** | 1.38 [1.19, 1.58] |
| 공통 기울기 (ANCOVA, 126) | — | — | −0.36 ± 0.06 | — |

- ⇒ 저자의 *"at all states … independent of the particle size"* 는 **pristine 에서만 원 자료로 선다** (기울기 0 이 구간 안).  침지 · 첫 리튬화는 큰 입자가 유의하게 약하다 (첫 리튬화 S ∝ d^−0.62).  [카드 해석] 순환이 만든 계면 결함이 큰 입자에 더 많다는 Wheatcroft (NMC811 XCT) 의 그림과 같은 방향 — 저자의 "응집 강도는 크기와 무관" 논증과는 어긋난다.
- 시험한 입자 크기 분포 (126, [판독]): 5–7.5 µm 14 · 7.5–10 28 · 10–12.5 21 · 12.5–15 27 · 15–17.5 18 · 17.5–20 12 · 20–22.5 4 · 22.5–25 2 개.  분말 전체의 PSD 는 [미확인] (입자 선정 기준도 미기재).

**(b) 표 S1 의 Weibull 모수는 최대가능도 (MLE) 값이다** [카드 산술]: MLE = pristine m **4.80** · S₀ **204.9** / 침지 4.82 · 179.7 / 탈리튬화 4.05 · 24.7 / 리튬화 4.05 · 77.4 — 인쇄값 (4.8 · 205 · 4.8 · 180 · 4.1 · 25 · 4.1 · 77) 과 반올림까지 같다.
SI 문장이 말하는 *"P_f(S_i) = i/N"* 의 직선 회귀 (P_f = 1 인 마지막 점 제외) 로는 pristine m **5.56** · S₀ 200.1 (Bernard 추정 (i−0.3)/(N+0.4) 로는 5.44 · 204.1) — **i/N 은 그림 3c 에 점을 찍는 데 쓴 값**이고 모수는 Origin 의 MLE 로 보인다 [카드 해석].

**(c) Weibull 분위 (표 S1 모수, 2.8/π 규약)** [카드 산술 S_p = S₀(−ln(1−p))^{1/m}]: pristine 1 % **78.6** · 5 % **110.4** · 50 % 189.9 · 95 % 257.6 MPa (경험 5 % 분위 138.0) · 침지 5 % 96.9 · 50 % 166.8 · 첫 리튬화 5 % 37.3 · 50 % 70.4 · 첫 탈리튬화 5 % 12.1 · 50 % 22.9.
d = 10 µm 입자의 F_c: pristine 5 % 분위 **12.4 mN** · 중앙 **21.3 mN** · 첫 리튬화 중앙 7.9 · 첫 탈리튬화 중앙 2.6 mN.

### 3-4. ★ 강도 규약 — **같은 입자에 네 가지 숫자** (정본 litdb 의 R7 카드들)

| 규약 | 식 | F/d² 에 곱하는 수 | 쓰는 카드 | Dang pristine S_m 188 을 옮기면 [카드 산술] |
|---|---|---|---|---|
| Hiramatsu–Oka (이 논문 · 리뷰 식 4) | S_t = 2.8F/(πd²) | **0.891** | 이 카드 · `stallard2022_…` (식 4) | **188** |
| 명목 (계수 1) | σ = F/d² | 1 | `wheatcroft2023_…` (σ_F = P_f/D²) · `song2025_insitu_ct_dem_…` (σm = f/d²) | **210.9** |
| 투영 면적 | σ = F/(πd²/4) | 1.273 | `meyer2018_calendering_process_model_…` (그 카드 §3-8) | **268.6** |
| 우리 DEM 판독 | F/(2R)² (= F/D²) | 1 | `wheatcroft2023_…` §7.3 · §7.4 의 우리 사다리 · 코퍼스 | 210.9 |

- ⇒ 같은 입자 · 같은 하중이 규약에 따라 **188 · 211 · 269 MPa** 로 적힌다 (최대 **43 %**).  R7 문턱을 문헌에서 옮길 때 **규약을 먼저 맞춘다** — 판정 기준을 결과 전에 등록할 때 규약 열을 같이 적는다.
- [카드 산술] 같은 규약으로 놓은 평판 pristine: **Dang NMC111 210.9 (Weibull 평균) · 211.3 (산술 평균) · 204.9 (중앙) ↔ Wheatcroft NMC811 207 (평균, n 15)** · 투영 면적 규약으로 Dang 중앙 260.9 ↔ `meyer2018_…` NCM111 ≈274 [그 카드 판독 · 다른 공급사 · 원통 압자 Ø100 µm].

### 3-5. 이 논문이 인용한 값 · 방법 (2차 인용 — 원문 미확인) + 서지 (참고문헌 목록 그대로)

| 이 논문이 전하는 것 | 쓰인 곳 | 참고문헌 (p. A2751, 인쇄 그대로) |
|---|---|---|
| 슬러리 혼합 · 캘린더링이 2차입자를 깰 수 있다 | 서론 (p. A2749) | [2] C. Sangrós Giménez, B. Finke, C. Schilde, L. Froböse, and A. Kwade, Powder Technology, 349, 1 (2019). (정본 `sangros2019_dem_calendering_lib_electrode`) · [3] C. Sangrós Giménez, C. Schilde, L. Froböse, S. Ivanov, and A. Kwade, Energy Technology, 1900180 (2019). (정본 `sangros2020_lib_electrode_dem_mech_elec_ionic`) |
| 순환 응력 → 파괴 · 분해 → 전기적 고립 | 서론 | [4]–[12] (Xu 2017 Exp. Mech. · Miller 2013 · de Vasconcelos 2018 Exp. Mech. · Lang 2016 · Xu 2017 JES · McGrogan 2018 · Liu 2018 · Çapraz 2019 · Wang 1999) — 정본 카드 = [8] `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` 뿐 |
| NMC 의 국소 파괴 거동 선행 | 서론 | [8] · [13] L. S. de Vasconcelos, R. Xu, J. Li, and K. Zhao, Extreme Mechanics Letters, 9, 495 (2016). (정본 `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode`) · [14] E. J. Cheng, K. Hong, N. J. Taylor, H. Choe, J. Wolfenstine, and J. Sakamoto, Journal of the European Ceramic Society, 37(9), 3213 (2017). (카드 없음) |
| 글러브박스 평판 압입 장치 | 방법 | [15] Y. Wang and Y.-T. Cheng, Scripta Materialia, 130, 191 (2017). · [16] Y. Wang, Q. Zhang, D. Li, J. Hu, J. Xu, D. Dang, X. Xiao, and Y. T. Cheng, Advanced Energy Materials, 8(10), 1702578 (2018). (둘 다 카드 없음) |
| **식 [1]** | p. A2750 | [17] Y. Hiramatsu and Y. Oka, International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts, 3(2), 89 (1966). (카드 없음 · 후보 N-11) |
| 암석 · 알루미나 입자 압축 파괴 · 서브마이크로 입자 | p. A2749–A2750 | [18] M. Yoshida, H. Ogiso, S. Nakano, and J. Akedo, Review of Scientific Instruments, 76(9), 093905 (2005). (카드 없음) · [19] L. Ribas, G. C. Cordeiro, R. D. Toledo Filho, and L. M. Tavares, Miner. Eng., 65, 149 (2014). (카드 없음) |
| Weibull 2 모수 · 평균 강도 | SI §4 | SI [1] Yoshida 2005 (위 [18] 과 같음) · SI [2] G. Yan, J. F. Nonemacher, H. Zheng, M. Finsterbusch, J. Malzbender, and M. Krüger, Journal of Materials Science, 54 (7), 5671-5681 (2019). · SI [3] ASTM C1239-07 (2007) |

## 4. 방법 ★

### 4-1. 문제 설정 (p. A2749)
2차입자의 기계적 온전성이 중요한 이유 둘: (1) **슬러리 혼합 · 캘린더링이 2차입자를 깰 수 있다** [2,3] (2) 순환 중 **∼5 % 부피 변화** 가 1차입자 안팎에 응력을 만들어 파괴 · 분해 → 전기적 고립 · 활물질 이용률 저하 [4–12].  국소 파괴 연구 [8,13,14] 는 있었지만 *"the fracture behavior of single NMC secondary particles is still unknown"* → 평판 압입으로 **입자 하나 통째의** 파괴를 잰다.

### 4-2. 시료 · 전기화학 · 추출 (p. A2749 · SI §6)
- 전극: NMC 92 · PVDF 4 · C65 4 wt% + NMP · 유성 믹서 (Mazerustar KK250S) · Al 박 도포 · 100 °C 진공 하룻밤 · **7.3 mg cm⁻²** · **압연하지 않음** — *"To avoid damaging the NMC secondary particles during the calendering and cell disassembling processes"*.
- 셀: **Swagelok** (PFA-820-6) · Li 박 · Celgard 2400 · 1 M LiPF₆ EC : EMC 3 : 7 + VC 2 wt% 500 µL · **C/10, 3–4.3 V**, 4.3 V 정전압 유지 (C/20 까지).
- 상태: **1st delithiation** (첫 충전 끝) · **1st lithiation** (첫 방전 끝) 에서 셀 분해 → DMC 세척 (글러브박스) → 밖에서 **NMP 80 °C 30 min 용해 · 분산 + 초음파 10 s** → 매끈한 **다결정 다이아몬드 기판** 에 한 방울 → 80 °C 30 min 건조 → 글러브박스로.
- 대조: **electrolyte-soaked** = 순환 없이 Swagelok 셀에서 전해액에 **48 h** 담근 전극 (같은 방법으로 분산) · **pristine** = 분말 그대로 (분산 방법 [미확인]).
- SI §6 (Fig. S5): 같은 전극을 Swagelok → 코인셀 순으로 조립 · 분해하며 같은 자리를 SEM — Swagelok 은 변화 없음, **코인셀 분해 뒤 일부 입자 손상 · 전극 변형** (화살표).  ⇒ Swagelok 을 쓴 이유의 근거.

### 4-3. 평판 압입 (p. A2749 · SI Fig. S1)
G200 (Agilent) · **다이아몬드 평판 명목 지름 40 µm** (Fig. 1a; 리튬 덩어리에 찍은 자국 = Fig. 1b, 둥근 사각 [그림 관찰]) · 아르곤 글러브박스 (Fig. S1; 방법 출처 [15,16]) · **입자를 평판 가운데** · **하중 제어 1 mN s⁻¹** (부하 · 제하) · 건조 · 장비 내장 현미경 + SEM (FEI Quanta 250) 으로 전후 형상.  **d = 누르기 전 투영 면적에서 ImageJ 로 계산** (면적 → 지름 환산식 [미확인] — 등가원 지름으로 보인다 [카드 해석]).
F_c = 변위가 갑자기 커지는 하중 (*"When the load reaches 73.8 mN, the displacement abruptly increases, indicating the breakage of the particle"*) · 그 뒤 변위 증가가 작은 것은 *"the increased contact area between the fractured particles and the flat punch reduces the effective compression stress"* (p. A2749).

### 4-4. 강도 정의 — 식 [1] (p. A2749–A2750 · `eq_01_hiramatsu_oka_particle_strength.png`)
*"Because of the brittle nature of the NMC particles, the fracture of the NMC secondary particles should be similar to the uniaxial compression induced fracture of rock and alumina particles. Here, we adopt the fracture model proposed by Hiramatsu and Oka to determine the strength, S_t"*

**S_t ≈ 2.8 F_c / (π d²)**  … [1]

*"Eq. 1 has been widely used to determine the strength of various brittle particles, from macro to sub-micro-meter length scale, without knowing the precise shape of the brittle blocks."*  — 계수 2.8 의 유래 · 응력 상태 · 적용 조건은 원전 [17] 몫 (이 논문에 설명 없음 · 원전 카드 없음).  S_t 는 진응력이 아니라 **두 점 압축 하중의 정규화** — 실제 최대 인장 응력은 기하에 따라 다르다 (평판 FE ≈0.79–1.38 × P/D² · [2차] `wheatcroft2023_…` Fig. 3c 판독).

### 4-5. Weibull (SI §4 · 식 S1–S2 · 표 S1–S2 · Fig. 3c)
P_f = 1 − exp[−(S/S₀)^m] (S1) · S₀ = 63.2 % 파괴의 특성 강도 · m = 모양 모수 · *"The estimates of the two parameters can be obtained by performing Weibull Fit in Origin, in which P_f is estimated as P_f(S_i) = i/N"* · 평균 S_m = S₀Γ(1 + 1/m) (S2).  신뢰구간 · 적합도 · 검정 **없음**.  [카드 산술 §3-3b] 모수는 MLE 와 같다.

### 4-6. ★ 입자 처리 (우리 축 언어로) + 이 묶음의 네 질문
- **재는 대상** = 우리 DEM 구 **하나 통째** (2차입자, d 6–23 µm) 가 **두 점 (평판 – 기판) 하중** 에서 쪼개지는 하중.  다접촉 · 이웃 입자 · 바인더 · SE 없음.  [2차] `sedlatschek2026_…` 의 입계 하나 (≈1.8 µm³) 보다 **한 층 위**, `wheatcroft2023_…` 평판과 **같은 층**.
- **모델 처리** = 없음 (실험 · 통계).  해석 틀 = "취성 조각의 두 점 압축" (식 [1]) + 입계 응집 강도 논증 (정성).
- **(i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장**: **말 없음** (DEM 언급 0 회 · 서론의 [2,3] 은 캘린더링이 입자를 깰 수 있다는 근거로만).  결론부 *"We expected that the measured fracture strength of the NMC particles can be incorporated in computational models of electrodes made of NMC particles under battery operating conditions"* (p. A2751) = 입자 계산에 **파괴 강도를 넣으라는 제안** (방법 없음).
- **(ii) 소성 · 큰 변형**: 다루지 않는다 — 입자를 **취성 (brittle)** 으로 본다 (*"Both the secondary and primary particles are brittle and, therefore, vulnerable to fracture"* p. A2749).  plastic · elastic · yield 0 회.  파괴 전 부하 곡선의 곡률 (Fig. 2a) 은 분석하지 않았다.
- **(iii) 2D ↔ 3D**: 실험은 3D 입자 · **d 는 2D 투영 면적의 지름** — 구가 아니면 d 오차가 S_t 에 **제곱**으로 들어간다.  2D → 3D 전이에 대한 말 없음.
- **(iv) 압력을 뺄 때**: 하중 제어의 *"loading/unloading rate of 1 mN s⁻¹"* 만 — 제하는 **입자가 부서진 뒤 조각 덩어리** 에서만 했고 (Fig. 2a · S3: 거의 수직 제하 [판독]) 되돌아옴 분석은 없다.  파괴 전 제하 · 반복 하중 없음.

### 4-7. 기법 미니 용어집
- **평판 압입 (flat punch indentation)** — 끝이 평평한 원통 압자로 입자를 기판과 사이에 두고 누르는 시험 (입자 지름 ≪ 압자 지름이면 평행판 압축).
- **하중 제어 (load control)** — 하중을 일정 속도로 올린다.  입자가 부서지면 하중이 유지된 채 변위가 크게 튄다 (pop-in · 폭주) → 그 하중이 F_c.
- **Hiramatsu–Oka 식** — 불규칙 취성 조각을 두 점으로 눌러 인장 강도를 어림하는 경험식 (1966 · 암석) — 계수 2.8/π.
- **2 모수 Weibull** — 약한 고리 통계의 강도 분포.  m 이 클수록 균일 (세라믹 5–20 · 여기 4–5).
- **입계 (inter-granular) / 입내 (trans-granular) 파괴** — 1차입자 사이 경계를 따라 / 1차입자를 가로질러.
- **첫 탈리튬화 · 첫 리튬화** — 첫 충전 (4.3 V) 끝 · 첫 방전 (3 V) 끝 상태.

## 5. Figure set ★ (크롭 27 장 = `litdb/figures/dang2019_nmc111_secondary_particle_flat_punch_fracture_strength/`)

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig. 1** | (a) 평판 압자 사진 (100 µm 바) (b) 리튬 덩어리에 찍힌 압자 모양 (20 µm 바) (c) 첫 탈리튬화 · 첫 리튬화 셀의 전압–용량 (3.0–4.3 V · ≈184 · 185 → 163 mAh g⁻¹ [판독]) (d) 다이아몬드 기판 위 pristine 2차입자 (5 µm 바) | 압자 크기 ≫ 입자 (Ø40 vs d ≈6–23 µm) = 평행판 압축 · 상태 정의 (용량 곡선) |
| **Fig. 2** | (a) pristine d 16.2 µm 의 하중–변위 — **73.8 mN 에서 변위가 ≈11 µm 튐** → 조각 재부하 ≈80 mN (b) 광학 사진 전 / 후 (20 µm 바) (c) 부서진 입자 SEM (20 µm 바 · 조각이 원래 입자 (16.2 µm) 보다 훨씬 넓게 퍼짐 [그림 관찰]) (d) 확대 (1 µm 바 · 1차입자 면 · 일부 벽개면) | **F_c 정의의 원형** · 파괴 직전 δ/d ≈ 0.046 [판독] · 부하 곡선 → 겉보기 Hertz E\* ≈ 98 GPa [카드 산술 · 참고 §13 D9] |
| **Fig. 3** | (a) F_c vs d (4 상태) (b) S_t vs d (c) Weibull 확률지 — 상태별 맞춤선과 S_m · S₀ · m 글자 | **원 자료 (표 S2) 와 d 를 잇는 그림** — §3-3 의 126 개 짝 · 강도의 입경 의존 재검의 바탕 |
| **Fig. S1** | 글러브박스 안 G200 사진 + 확대 (평판 압자 · 내장 카메라) | 건조 · 불활성 시험 환경 |
| **Fig. S2** | 침지 · 첫 탈리튬화 · 첫 리튬화 뒤 분산된 2차입자 SEM (5 µm 바) | 추출 뒤에도 구형 2차입자 모양 유지 [그림 관찰] |
| **Fig. S3** | d ≈12.5 µm 입자들의 하중–변위 (4 상태 · 각 2–3 개) | 같은 크기에서 F_c 서열 (pristine ≈24–50 ≫ 리튬화 ≈8–14 ≫ 탈리튬화 ≈4–5 mN [판독]) · 파괴 뒤 조각 재부하 꼴 |
| **Fig. S4** | 부서진 입자: (a) 침지 (2 µm 바) (b) 첫 탈리튬화 (5 µm) (c) 첫 리튬화 (5 µm) | **입계 분리** — 1차입자 다발 · 1차입자 모양 그대로 [그림 관찰] |
| **Fig. S5** | 같은 전극 같은 자리: (a) 조립 전 (b) Swagelok 분해 뒤 (c) 코인셀 분해 뒤 — (c) 에 손상 화살표 (50 µm 바) | **셀 분해 경로가 입자를 깰 수 있다** — 사후 SEM 대조 때의 함정 |
| **Table S1** | 상태별 S_m · S₀ · m | 헤드라인 (188 · 165 · 22 · 70) |
| **Table S2** | 상태별 원 강도 S (MPa) 와 P_f (%) 전부 (33 · 34 · 29 · 33 행) | **원 자료** — 리뷰 그림 · Wheatcroft 비교값의 재계산 근거 |

### 5-1. 크롭 색인 — 27 장 (그림 · 표 10 · 식 3 · 근거 문단 14)

도구 (`extract_figures.py --clean`) 가 자른 것 5 장 (Fig. 3 · S1 · S3 · S5 · Table S1) → **전부 다시 잘랐다** (recrop) · 놓친 것 5 장 (Fig. 1 · 2 · S2 · S4 — 옆 캡션 · Table S2 — 제목이 본문 블록에 붙음) → 손 크롭 (manual_crop).  그림 크롭 = 그래픽만 (캡션은 `figures.json`) · 표 크롭 = 제목 줄 + 표.

| 파일 | 쪽 (PDF) | bbox (pt) | 확인 |
|---|---|---|---|
| `fig_1.png` | 본문 3 (A2750) | 32.1, 65.0, 326.0, 294.1 | 🖐 손 크롭 — 래스터 xref 53 + 3 pt · a–d · 스케일바 · 축 |
| `fig_2.png` | 본문 3 | 32.1, 497.9, 326.0, 755.2 | 🖐 손 크롭 — 래스터 xref 52 + 3 pt · a–d |
| `fig_3.png` | 본문 4 (A2751) | 63.2, 64.5, 255.8, 490.9 | 🔧 재크롭 — 도구 크롭은 단 전폭 (좌우 흰 여백 ≈145 px) → 래스터 + 3 pt |
| `fig_S1.png` | SI 1 | 84.4, 206.6, 338.2, 366.5 | 🔧 재크롭 — 위 본문 줄 아래 반쪽 섞임 제거 |
| `fig_S2.png` | SI 1 | 33.0, 417.4, 404.7, 528.0 | 🖐 손 크롭 — 옆 캡션 |
| `fig_S3.png` | SI 1 | 99.4, 562.2, 320.6, 743.8 | 🔧 재크롭 — 절 제목 아래 반쪽 · 쪽 번호 "1" 섞임 제거 |
| `fig_S4.png` | SI 2 | 33.0, 430.4, 402.9, 541.7 | 🖐 손 크롭 — 옆 캡션 |
| `fig_S5.png` | SI 2 | 33.0, 559.6, 402.0, 669.5 | 🔧 재크롭 — 도구 크롭이 **아래가 잘려 50 µm 스케일바 셋이 없었다** |
| `tab_S1.png` | SI 2 | 31.0, 298.2, 527.0, 400.6 | 🔧 재크롭 — 도구 크롭이 **SI 2 쪽 전체** |
| `tab_S2.png` | SI 3 | 31.0, 135.5, 559.0, 640.5 | 🖐 손 크롭 — 도구가 못 봄 (34 행 전부) |
| `eq_01_hiramatsu_oka_particle_strength.png` | 본문 3 | 126.5, 318.6, 285.7, 336.6 | 식 [1] · 400 dpi |
| `eq_S01_weibull_failure_probability.png` | SI 2 | 245.5, 88.6, 582.5, 115.8 | 식 (S1) · 400 dpi |
| `eq_S02_weibull_mean_strength.png` | SI 2 | 263.5, 204.6, 582.5, 228.8 | 식 (S2) · 400 dpi |

근거 문단 14 (카드가 숫자 · 정의 · 단정의 근거로 인용한 문단만 · 쪽 순): `txt_p2749_title_authors_abstract_doi_history.png` (서지 · 초록 · 날짜) · `txt_p2749_intro_brittle_calendering_volume_change.png` (취성 · 캘린더링 · ∼5 % · "still unknown") · `txt_p2749_experimental_electrode_cell_cycling.png` (전극 · 셀 · 무압연 이유) · `txt_p2749_harvest_dispersion_soaked_control.png` (추출 · 분산 · 침지 대조) · `txt_p2749_indentation_g200_flat_punch_40um_1mN_s.png` (장치 · 40 µm · 1 mN/s · 건조 · d 정의) · `txt_p2749_ld_curve_73p8mN_critical_load_fc.png` (73.8 mN · F_c 정의) · `txt_p2749_2750_hiramatsu_oka_brittle_particle_strength.png` (식 [1] 채택 · "without knowing the precise shape") · `txt_p2750_strength_size_independent_intergranular_cohesion.png` (입경 무관 · 입계 · 응집 강도 논증) · `txt_p2750_weibull_sequence_soaked_12pct_cycling_detrimental.png` (서열 · 12 %) · `txt_p2750_2751_delithiation_contraction_defects_mechanism.png` (∼5 % 수축 · 결함 기전) · `txt_p2751_other_factors_strength_for_computational_models.png` (계산 모델에 넣자는 제안) · `txt_p2751_summary.png` (요약) · `txt_S2_weibull_method_origin_pf_i_over_n_sm.png` (Weibull 방법 · i/N · Origin) · `txt_S2_S3_swagelok_vs_coin_cell_disassembly_damage.png` (셀 분해 손상).
판독 원자료: 같은 폴더 `digitized.csv` (143 행 — Fig. 3b 짝 126 + 가린 3 + Fig. 2a 14).
⚠ `--slug dang2019_nmc111_secondary_particle_flat_punch_fracture_strength --clean` 을 다시 돌리면 손 크롭 22 장 (manual_crop 5 · 식 3 · 글 14) 이 지워지고 재크롭 5 장이 자동 bbox 로 돌아간다 (`pdf_map.tsv` 경고 동일).

## 6. Post-processing ★
- **하중–변위**: G200 의 "Displacement into surface" 그대로 (프레임 순응 보정 · 열 표류 보정 서술 [미확인]).  E · 강성 · 에너지 추출 **없음**.
- **강도**: 식 [1] (F_c · d) · d = 누르기 전 투영 면적 (ImageJ).
- **통계**: 상태별 2 모수 Weibull (Origin · 확률지 그림은 i/N) · S_m (식 S2).  평균 ± · 신뢰구간 · 검정 · 입경 보정 비교 **없음** (§3-3 에서 우리가 함).
- **형상**: 광학 (G200 내장) · SEM (Quanta 250) — 파괴 꼴 정성.
- **도구**: ImageJ · Origin.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 출처 카드 위치를 병기해 적는다)

### 7-1. 대조표 (모든 행에서 **재료가 다르다** — 이 논문 = NMC111 2차입자 (Umicore) ↔ 우리 AM_P = NCM811 다결정)

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| 대상 | 다결정 NMC111 2차입자, d 5.7–23.1 µm (pristine 6.6–18.8) [판독] | AM_P = 다결정 NCM811, D 10–12 µm (`case_master` AM_P–AM_P R_min 5–6 µm · [2차] wheatcroft §7.1) · AM_S = 단결정 규약 | 부류 · 크기 **안** (AM_P) · AM_S 는 대상 밖 |
| 파괴 기준 | 강도 S_t = 2.8F_c/(πd²) — **두 점 지름 하중의 입자 분할** | Auerbach P_c = A·K²·R/E\* × Lawn 1 · 3 · 11 · 32 (`fracture_model.py` · [2차] wheatcroft §7.3) — 접촉별 **사후 분류** | 형식이 다르다 — 환산은 §7-3 (가정 명시) |
| 하중 기하 | 고립 입자 · 평판 – 기판 두 점 | 구–구 접촉 여러 개 (배위수 Z) | ⚠ 다접촉 입자의 분할 하중은 다를 수 있다 (논문에 없음) |
| 산포 | **Weibull m 4.8 (pristine, n 33, SI 인쇄)** | 결정론 문턱 (확률 산포 없음) | 새 입력 후보 (확률적 파쇄) |
| 입경 스케일 | pristine 강도 ≈ 무관 (기울기 −0.16, n.s.) [카드 산술] | P_c ∝ R ⇒ F/D² ∝ D^−1 | ⚠ **평판 pristine 과는 어긋난다** — 단 우리 R_min 폭 (5 ↔ 6 µm) 에서 차이 ≤ 20 % |
| E_AM · ν | 없음 | 140 GPa · 0.25 ([2차] wheatcroft §4.8) | 무관 — [카드 산술 · 참고] Fig. 2a 부하 곡선의 겉보기 Hertz E\* ≈ 98 GPa (E ≈ 91 GPa @ ν 0.25) · 인용 금지 |
| K_IC | 없음 (정성 한 문장) | K_P 0.3 · K_S 1.0 (출처 미확인 — SELF-51) | ⛔ 출처 불가 |
| 압력 · SE | 없음 (입자 하나 · 0–80 mN) | 300 MPa 복합 압밀 · LPSCl (E_eff 1.35 GPa · Heckel P_y 138 MPa · MPM E 1.53 · σ_y 0.30 · ν 0.49) · 랩 표준 순수 SE 기공 10–13 % · 진밀도 1.64 g/cm³ | 나란히 놓을 숫자 **없음** (이 논문은 SE 를 다루지 않는다) |
| MPM 의 AM | — | **동결 scaffold** (역학 응답 0) | MPM 쪽 R7 은 지금 불가 (frame [5]) |
| 순환 | 첫 충 / 방전 뒤 ×0.12 / ×0.37 (S_m) · 액체 | A10 `cycle_contact_ledger` poly 입계 void (ASSUMED-FORM) | **모양**만 — 크기 전이 금지 |

### 7-2. ★★ 판정 — 이 강도가 R7 판정의 앵커가 되나
1. **된다 — 평판 (두 점 · 무딘 접촉) 끝으로.**  같은 규약 (F/d²) 에서 Dang NMC111 **211** ↔ Wheatcroft NMC811 **207** MPa (평균) — 독립 두 연구실 · 두 조성이 2 % 안 [카드 산술].  Wheatcroft 원뿔 (67 MPa, 날카로운 접촉) 이 반대 끝 — 창은 그대로 **[67, ≈210] MPa (F/D²)**.
2. **pristine 한정** — 압밀 (성형) 은 순환 전이라 pristine 이 맞는 층.  침지 (−12 %) 는 **액체 전해질** 노출이라 ASSB 에 직접 대응하는 대조가 아니다.
3. **규약을 맞춰 쓴다** — 188 (2.8/π) 을 그대로 F/D² 문턱으로 쓰면 12 % 낮게 (보수적으로) 잡힌다.  판정 기준 등록 때 규약 열을 적는다 (§3-4).
4. **산포** — Weibull m 4.8 (n 33, 인쇄) 은 Wheatcroft 평판의 판독 m ≈4.9 (n 15, [2차] wheatcroft D7) 과 같은 자리 — "입자 강도 m ≈ 5" 는 두 독립 자료가 함께 받친다 [카드 해석].
5. **"onset" 의 앵커는 아니다** — F_c 는 하중 제어 폭주 (입자 분할) 의 하중 — 표면 아래 미세 균열은 못 본다.  우리 Lawn 사다리에서 **fragmentation 급** 에 대응.

### 7-3. Auerbach 사다리 ↔ 이 분포 (⚠ 가정: DEM 접촉력 F ≈ 두 점 지름 하중, D = 2R_min · 우리 수치 = [2차] wheatcroft §7.3 D13)

| Lawn 단계 | F/D² (R 5 µm) | F/D² (R 6 µm) | 이 논문 pristine 의 Weibull 파괴 확률 [카드 산술 — F/D² × 0.891 → S] |
|---|---|---|---|
| onset (×1) | 12.1 | 10.0 | ≈0 (< 10⁻⁴) |
| multicrack (×3) | 36.2 | 30.1 | ≤ 0.0002 (0.00014 · 0.00006) |
| **fragmentation (×11)** | **133** | **110** | **7.0 %** (R 5) · **2.8 %** (R 6 ≈ 110 → S 98) |
| pulverization (×32) | 386 | 321 | ≈100 % (99.999 · 99.3 %) |

- ⇒ 현 fragmentation 문턱은 이 논문의 **pristine 분포 아래쪽 꼬리 (1–7 %)** 에 앉는다 — Dang 의 **가장 약한 입자 (F/d² 144 MPa) 보다 낮다**.  "평판 기준이면 우리 fragmentation 은 보수적 (일찍 깬다)" — Wheatcroft 원뿔 (67) 기준이면 반대.  창 안의 자리는 Wheatcroft 카드 §7.3 의 결론과 같다.
- 첫 리튬화 분포 (액체 순환 뒤) 에서는 fragmentation 133 이 **99.7 %** — 순환 입자는 압밀 수준 하중에서 거의 다 쪼개진다 (크기 전이 금지).

### 7-4. ★ 우리 코퍼스의 AM_P 접촉은 이 분포의 어디에 앉나 ([2차] wheatcroft §7.4 · D16 의 코퍼스 값 — 작업 브랜치 `case_master.csv`, 120 케이스)
- 코퍼스 AM_P–AM_P **중앙 접촉 F/D²** = 최소 25.7 · Q1 75.4 · **중앙 109.1** · Q3 134.2 · 최대 265.3 MPa (그 카드 D16).
- 이 논문 pristine 의 Weibull 로 [카드 산술]: 중앙 109.1 → S 97.2 → **P_f 2.8 %** · Q1 75.4 → 0.5 % · Q3 134.2 → 7.3 % · 최대 265.3 → 86 %.  표 S2 의 33 개 중 F/d² < 109.1 인 입자 **0 개** (최솟값 144).  침지 분포로는 5.1 % · **첫 리튬화 분포로는 93 %** (표 S2 33 개 중 30 개가 109.1 아래).
- ⇒ **pristine 성형 단계에서 평판 기준의 AM_P 분할은 드물다** (중앙 접촉 기준) — Wheatcroft 원뿔 기준 (86 % 넘음, 그 카드 D17) 과 **정반대** = 그 카드의 *"기하 선택이 곧 결론"* 을 독립 자료가 다시 확인.
- ⚠ 한정: 중앙 접촉 하나 ≠ 입자 분할 하중 (맞은편 접촉 짝 · 배위수) · F 는 압밀 끝 시점 · 300 MPa 급 · R_min 5/6 µm 두 값 · NMC111 ↔ NCM811 · 두 점 하중 가정.

### 7-5. 층 구분 — 같은 "강도" 가 아니다 (규약 · 기하 · 상태를 같이 적는다)

| 층 | 값 | 규약 · 기하 | 출처 |
|---|---|---|---|
| 입계 고유 강도 | 745 MPa (Weibull σ_ch, n 3) | 단축 인장 (FIB) | [2차] `sedlatschek2026_…` |
| 2차입자 평판 분할 (pristine) | **188** (2.8/π) = **211** (F/d²) | 두 점 · 평판 · NMC111 · n 33 | **이 카드** |
| 2차입자 평판 분할 (pristine) | 207 (F/D²) | 두 점 · 평판 · NMC811 · n 15 | [2차] `wheatcroft2023_…` |
| 침지 48 h (액체) | 165 (2.8/π) = 185 (F/d²) | 평판 · NMC111 | 이 카드 |
| 2차입자 원뿔 분할 (pristine) | 67 (F/D²) | 두 점 · R 0.71 µm 팁 | [2차] wheatcroft |
| 첫 리튬화 (액체, 3 V) | 70 (2.8/π) = 79 (F/d²) | 평판 · NMC111 | 이 카드 |
| 첫 탈리튬화 (액체, 4.3 V) | 22 (2.8/π) = 25 (F/d²) | 평판 · NMC111 | 이 카드 |
| 4.3 V (액체, 4 번째 충전) | 11 (F/D²) | 원뿔 · NMC811 | [2차] wheatcroft |

- [카드 산술] 745 / 211 = **3.5** ([Sedl26] 의 *"≈4×"* · wheatcroft 의 745/207 = 3.6 과 같은 자리).

### 7-6. frame[5] — 어느 반쪽을 가졌나
입자 **한 개** 역학 (파괴 하중 · 산포 · 파괴 꼴) 의 반쪽만 — 다접촉 · 패킹 · 전극 · 압밀 · 수송의 반쪽은 없다.  우리 DEM 은 반대 (다접촉 하중은 있고 입자 내부 파괴는 없다) · MPM 은 AM 을 얼려 둘 다 없다.  frame[4]: 이 값은 **실험 앵커** 로 DEM 의 파괴 판정에만 댄다 — MPM 과 맞추지 않는다.

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md · 정본 카드: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / DEM AM E 140 GPa · ν 0.25 · Auerbach A 200 · K_P 0.3 ([2차] wheatcroft) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = **NMC111 (AM) 만** — SE 값 없음 · 모든 행에 "재료 다름".)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **R7 판정 기준을 결과 전에 적을 때의 꼴**: 강도 분포 (Weibull S₀ 205 · m 4.8 · n 33) + **규약 열** (2.8/π · 1 · 4/π — 같은 입자가 188 · 211 · 269, §3-4) + d 정의 (투영 면적 지름 ↔ 우리 구 지름) + Weibull 추정법 (MLE ↔ i/N 회귀가 m 4.8 ↔ 5.6 으로 다르다, §3-3b) | 기공률 연산자와는 무관 · SE 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 — SE 를 다루지 않는다 | LPSCl 값 0 |
| **단계 5** (3D 복합 압밀) | ★ **R7 결과 전 대조 항목**: 300 MPa 압밀 끝에서 AM_P 마다 max(접촉력)/d² (또는 맞은편 짝) 를 세어 이 분포의 분위 (pristine 5 % 110 · 50 % 190 MPa, 2.8/π) 를 넘는 **수 분율 · 부피 분율** 을 Auerbach 등급 옆에 — 평판 끝 (이 논문 · Wheatcroft 평판) ↔ 원뿔 끝 (Wheatcroft 67) 두 값으로 · [카드 산술] 코퍼스 중앙 접촉은 pristine P_f ≈2.8 % 자리 (§7-4) | 다접촉 입자의 분할 하중 · 압밀 중 파괴 진행 · 깨진 뒤의 재배열 (논문에 없음) |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 제하는 부서진 조각에서만 (거의 수직 · 분석 없음) | 파괴 전 제하 · 탄성 회복 (조건 R4) |
| **단계 7** (형상 · 피복 · 수송) | 서론의 사슬 *"fracture and disintegration … resulting in electrical insulation"* [4–12] (정성) — 우리 σ_ionic T1 β_F · σ_e 22.5 β_Fe (`fracture_aware_excluded_pct` · `frac_severe_force_pct`) 의 파괴 분율을 **강도 기준으로도** 셀 수 있다는 근거 | 파괴가 수송을 얼마나 바꾸는지 값 없음 |
| **후보 D0** (지금 DEM) | Auerbach 분류 옆에 **강도 기준 팔** (σ_nom = F/(2R)² vs 평판 분포 · 확률적 m 4.8) — [2차] wheatcroft §8 ① 의 제안에 평판 끝의 독립 자료 (n 33 · 원 자료) 를 더한다 · Auerbach 의 크기 스케일 (F/D² ∝ D^−1) 은 평판 pristine (≈무관) 과 다르다는 점검 | 파편 생성 · 형상 변화 (D0 는 분류만) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A** (MPM · 강체 AM + SE 한 속도장) | 강체 AM 은 못 깨진다 → **사후 R7**: AM 마다 받은 접촉 반력 (맞은편 짝의 최대) 을 F_c(d) = S·πd²/2.8 와 비교 (d = 10 µm: pristine 중앙 21 mN · 5 % 12 mN) [카드 산술] | 깨진 뒤의 하중 재분배 (강체는 계속 버틴다) |
| **후보 A′** (입자별 속도장) | AM 을 변형체로 둘 때의 **단일 입자 확인 표적**: 두 평판 압축의 부하 곡선 (Fig. 2a: 20 → 60 mN 기울기 ≈134 mN/µm · 파괴 δ/d ≈0.046 [판독]) | E · 구성식 · 파괴 법칙 값 없음 · Fig. 2a 한 입자뿐 |
| **후보 B** (입자별 FE + 접촉) | AM 응집영역 · 강도 확률 모델의 **보정 · 검증 자료**: F_c(d) 129 개 + 파괴 꼴 (입계) · Weibull m — Wheatcroft 처럼 FE 로 강도 → 응집 강도를 거꾸로 맞출 수 있다 (이 논문은 하지 않았다) | 1차입자 크기 · 입계 인성 · E 없음 |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 (AM 은 단단해 큰 변형이 아니다) · AM 을 결합구 응집체로 깨는 DEM 이면 F_c(d) · m 이 보정 표적 | — |
| **후보 C′** (항복 캡 · 다접촉 보정 DEM) | 없음 — AM 에 "항복 캡" 대신 **파쇄 문턱** 이 맞다는 정성 (취성 · 입계 분할) | — |
| **후보 M0** (균질화 압밀) | 없음 | 압밀 자료 없음 |
| **U0–U6** | **U1** (입자 하나 압축) 의 **실험 쪽 꼴** — 평판 · 하중 제어 · F_c 정의 · F_c ∝ d^1.84 (pristine) [카드 산술] · AM 이 변형체인 후보 (A′ · B) 에서만 쓸모 | U0 · U2–U6 없음 · 해상도 (지름당 셀 수) 정보 없음 |
| **R1–R7** | **R7 (AM 파괴)** = 이 카드의 몫 — 평판 끝 · 산포 · 파괴 꼴 · 순환 약화.  **R1** (AM 하중 몫): 입자 하나가 버틸 수 있는 하중의 상한 (d 10–12 µm pristine 중앙 21–30 mN [카드 산술]) — AM 골격의 하중 분담이 파괴로 끊길 수 있는 크기 [카드 해석] | R2 · R3 · R4 · R5 · R6 없음 (R6 = SE 형상 · 이 논문은 AM 취성) |
| **결과 전 대조 항목** | (1) 압밀 끝 AM_P 의 F/d² 분포를 이 논문 pristine 분포 (규약 맞춤) 와 Wheatcroft 원뿔 두 끝에 대 **분할 분율** 을 적는다 (2) Weibull m ≈5 (확률적 문턱을 넣는다면) (3) pristine 강도의 입경 무관 (기울기 −0.16 [−0.40, +0.09]) — 강도 기준 팔의 크기 스케일 점검 | 맞추는 데 쓰지 않는다 · 재료 다름 (NMC111) |

- **재료 · 차원 · 조건 차이**: NMC111 (Umicore) ↔ NCM811 · 고립 입자 두 점 하중 ↔ 다접촉 침대 · 건조 글러브박스 · 상온 (숫자 미기재) · 누른 채의 파괴 하중 · d = 2D 투영 · SE · 바인더 · 압밀 없음 · 순환 값은 액체 전해질 + NMP 80 °C 추출 이력.

## 9. 적용 인사이트 (행동 — 이 항목이 코드를 바꾸지 않는다)
1. **R7 강도 기준 팔의 평판 끝을 이 자료로 (후보 D0 · 단계 5)** — `wheatcroft2023_…` §8 ① 의 강도 기준 팔 (원뿔 66.6·(D/10)^−0.81 / 평판 207) 에서 평판 끝을 **이 논문 Weibull (S₀ 205 · m 4.8, 2.8/π → F/D² 로 ×1.122)** 로 바꾸거나 나란히 — n 33 · 원 자료 공개 · 산포가 있다.  출처 문자열: *"Dang et al., J. Electrochem. Soc. 166 (13) A2749 (2019): pristine NMC111 secondary particles, flat punch, S_t = 2.8F_c/(πd²), Weibull S_m 188 MPa (S₀ 205, m 4.8, n 33; SI Table S1–S2)"*.
2. **규약 열을 판정 기준에 붙인다 (단계 0)** — 문헌 강도를 옮길 때 2.8/π · 1 · 4/π 를 맞춘 뒤 비교 (§3-4).  우리 문서에서 "NMC 입자 강도 188 MPa" 처럼 규약 없이 쓰지 않는다.
3. **확률적 문턱 (선택)** — 결정론 문턱 대신 Weibull (m ≈5) 로 입자마다 문턱을 뽑으면 파괴 분율이 매끈해진다 — 등록 뒤에만 (결과 보고 고르면 순환).
4. **Auerbach 크기 스케일 점검** — 평판 pristine 강도는 입경과 무관 (원 자료 기울기 −0.16) · Auerbach 는 F/D² ∝ D^−1.  넓은 AM 입도 (bimodal · 6 mAh) 로 갈 때 이 차이가 판정을 바꾸는지 먼저 본다 (지금 R_min 5/6 µm 에서는 ≤ 20 %).
5. **사후 SEM 대조의 함정** — 셀 분해 (코인셀) 가 입자를 깰 수 있다 (SI §6).  실험 압밀체의 AM 파괴 분율과 대조할 때 시료 회수 경로 (분해 · 절단 · 연마) 를 같이 적는다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- *"Flat-punch compression of single pristine NMC111 secondary particles (Umicore, d ≈ 7–19 µm, dry Ar glove box) gives a Weibull mean strength S_m = 188 MPa (S₀ = 205 MPa, m = 4.8, 33 particles) with S_t ≈ 2.8F_c/(πd²) after Hiramatsu–Oka; fracture is mainly intergranular (Dang et al., J. Electrochem. Soc. 166 (13) A2749 (2019), Supplementary Table S1)."*
- *"After the first delithiation and lithiation in a liquid half-cell the mean strength drops to 22 and 70 MPa (Weibull), respectively."*
- *"Expressed in the coefficient-1 convention F/d², the flat-punch strength of NMC111 (211 MPa) and of NMC811 (207 MPa, Wheatcroft et al. 2023) agree within 2 %."* — ⚠ 계산은 **우리 산술** 임을 병기.
- ⛔ *"NMC particle tensile strength = 188 MPa"* 처럼 **규약 (2.8/π) · 기하 (평판 두 점) · 상태 (pristine · 건조)** 한정어를 떼고 쓰지 말 것.  ⛔ *"strength is size-independent at all states"* 를 그대로 옮기지 말 것 (원 자료로는 pristine 에서만).

## 11. 주의/한계 (over-claim 방지)
1. **명목 강도**: S_t 는 식 [1] 의 근사 (불규칙 취성 조각 · 계수 2.8/π) — 진응력이 아니다.  비구형이면 d (2D 투영) 오차가 제곱으로 들어간다.
2. **두 점 · 고립 · 평판**: 전극 속 다접촉 입자 · 날카로운 접촉 (1차입자 돌기) 의 분할 하중은 다를 수 있다 (Wheatcroft 원뿔 = 3 배 낮음).
3. **n · 산포가 본문에 없다** — SI 표 S2 에서만 (행 수 33 · 34 · 29 · 33).  신뢰구간 · 검정 없음.
4. **"모든 상태에서 입경 무관"** 은 원 자료 재분석으로 pristine 에서만 선다 (§3-3a) — 첫 리튬화 · 침지는 유의한 음의 기울기.  (판독 d · 순위 짝짓기 · 가린 3 점 제외 — 한정어)
5. **Weibull 추정법 서술과 값의 불일치**: SI 문장은 P_f = i/N 를 말하지만 표 S1 은 MLE 와 같다 (§3-3b).
6. **순환 조건**: 액체 LiPF₆ · C/10 · Swagelok · 첫 사이클 한 번 · NMP 80 °C + 초음파 추출 — 침지 대조로 추출 영향을 일부 분리했지만 (−12 %) **충 / 방전 입자에 대한 추출 영향의 대조는 없다**.  ASSB 로 크기 전이 금지.
7. **기전 (∼5 % 수축 → 계면 결함)** 은 측정 근거 없이 서술된 해석이다 (1차입자 크기 측정 · 출처 미제시).
8. **pristine 분산 방법 · 입자 선정 기준 · 분말 PSD · 1차입자 크기 · 온도 · 장비 보정 (프레임 순응 · 열 표류)** 미기재.
9. **E · K_IC · 경도 없음** — 이 카드에서 E_AM · K_IC_AM 의 출처를 만들지 않는다 (§13 D9 의 겉보기 E\* 는 참고 산술).
10. **frame 정리**: 실험이라 rigid-vs-plastic artifact 는 없지만 **스케일 artifact** — 이 값은 "입자 한 개 · 두 점" 층이고 우리 DEM 은 "입자 여러 개 · 다접촉 · 내부 없음" 층이다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 17 | Y. Hiramatsu and Y. Oka, International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts, 3(2), 89 (1966). | **카드 없음 (후보 표 N-11)** — 식 [1] 의 원전.  계수 2.8 의 근거 · 적용 조건 (불규칙 조각 · 두 점) — 계수 1 (Wheatcroft) 과의 12 % 차를 원전으로 판정 |
| 18 | M. Yoshida, H. Ogiso, S. Nakano, and J. Akedo, Review of Scientific Instruments, 76(9), 093905 (2005). | **카드 없음** — 서브마이크로 취성 입자 압축 장치 + Weibull (SI 참고 1 과 같음) · `paulick2015_…` [35] · `stallard2022_…` [111] 도 인용 |
| 14 | E. J. Cheng, K. Hong, N. J. Taylor, H. Choe, J. Wolfenstine, and J. Sakamoto, Journal of the European Ceramic Society, 37(9), 3213 (2017). | **카드 없음** — NMC111 (열간 가압) 의 E · H · 파괴 인성 (`sharma2023_…` · `sakka2022_…` · `stallard2022_…` [76] · `so2022_…` 가 가리킴) — 질문 c 의 NMC111 기준값 |
| 15 | Y. Wang and Y.-T. Cheng, Scripta Materialia, 130, 191 (2017). | 카드 없음 — 글러브박스 평판 압입 방법 (장비 · 보정) |
| 16 | Y. Wang, Q. Zhang, D. Li, J. Hu, J. Xu, D. Dang, X. Xiao, and Y. T. Cheng, Advanced Energy Materials, 8(10), 1702578 (2018). | 카드 없음 — 액체 전해질 속 · 순환 중 압입 (본문이 후속으로 가리킴) |
| 2 · 3 | Sangrós Giménez 외 (Powder Technology 349, 1 (2019) · Energy Technology 1900180 (2019)) | 정본 카드 있음 (`sangros2019_dem_calendering_lib_electrode` · `sangros2020_lib_electrode_dem_mech_elec_ionic`) — 이 논문이 "캘린더링이 입자를 깬다" 의 근거로 인용 |
| 8 · 13 | Xu 2017 JES · de Vasconcelos 2016 EML | 정본 카드 있음 (`xu2017_…` · `devasconcelos2016_…`) |

## 13. 🧮 파생 계산 원장 (`[카드 산술]` — 원 자료 = SI 표 S2 (인쇄) · 판독 = `digitized.csv`)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | 표 S2 상태별 n · 평균 · SD(N−1) · 중앙 · Q1/Q3 (중앙 뺀 반쪽 중앙) · 최소/최대 | §3-1 표 (pristine 33 · 188.3 · 40.9 · 182.6 · 156.3/215.95 · 128.3/289.2) | 인쇄 값만 씀 |
| D2 | Weibull MLE (표 S2) | pristine m 4.798 · S₀ 204.89 · 침지 4.818 · 179.72 · 탈리튬화 4.054 · 24.72 · 리튬화 4.052 · 77.41 | 표 S1 재현 |
| D3 | i/N 직선 회귀 (P_f = 1 제외) · Bernard · x-on-y | pristine m 5.563 · S₀ 200.1 / 5.439 · 204.1 / 6.042 · 198.6 | 표 S1 과 안 맞음 |
| D4 | S_m = S₀Γ(1+1/m) (표 S1 모수) | 187.8 · 164.9 · 22.7 · 69.9 | 인쇄 188 · 165 · 22 · 70 |
| D5 | 비 | 침지/pristine 0.878 · 리튬화/pristine 0.372 · 탈리튬화/pristine 0.117 · 리튬화/침지 0.424 · 중앙 비 리튬화/침지 0.442 · 리튬화/pristine 0.385 | "12 %" ✓ · 리뷰 "44 %" = 중앙 리튬화/침지 |
| D6 | 규약 변환 (×π/2.8 = 1.1220 · ×4/2.8 = 1.4286) | 188 → 210.9 · 268.6 / 평균 188.3 → 211.3 / 중앙 182.6 → 204.9 · 260.9 / Wheatcroft 207 → 184.5 (2.8/π) | §3-4 |
| D7 | Fig. 2a 입자 강도 | 2.8 × 73.8 /(π × 16.2²) × 10³ = 250.6 MPa (F/d² 281.2) | 표 S2 의 250.4 · 251.1 |
| D8 | Fig. 2a 부하 가지 판독 | 5 · 10 · 20 · 40 · 60 · 70 · 73 mN @ 162 · 224 · 324 · 473 · 622 · 710 · 747 nm (선 중심) · 기울기 20→60 mN 134 mN/µm · δ/d (73 mN) 0.046 | 선 굵기 ±125 nm |
| D9 | 겉보기 Hertz (두 강체 평판 사이 구, F = (4/3)E\*√R (δ/2)^{3/2}, R = 8.1 µm, 10–70 mN 의 F^{2/3}–δ 직선) | δ₀ 36 nm · **E\* ≈ 97.5 GPa** · E ≈ 91 GPa (ν 0.25) · 89 (ν 0.3) · 잔차 ≤ 2 mN | **참고 · 인용 금지** — 프레임 순응 · 비구형 · 응집체 · 한 입자 |
| D10 | Fig. 3b ↔ 표 S2 짝짓기 | 126/129 · \|차이\| 중앙 0.13–0.96 · 최대 1.72 MPa · 가린 3 (217.0 · 28.2 · 85.5) | digitized.csv 머리 |
| D11 | Fig. 3a 검산 (F_c = S·πd²/2.8) | 중앙 \|차이\| 0.08 · 0.11 · 0.20 · 0.20 mN | 식 [1] 확인 |
| D12 | ln S ~ ln d (OLS · 95 %) | pristine −0.156 [−0.398, +0.086] p 0.199 · 침지 −0.293 [−0.500, −0.085] p 0.007 · 탈리튬화 −0.297 [−0.631, +0.036] p 0.078 · 리튬화 −0.616 [−0.814, −0.417] p < 0.001 · pristine+침지 −0.253 [−0.411, −0.096] · ANCOVA 공통 −0.358 ± 0.061 | 판독 d |
| D13 | ln F_c ~ ln d | pristine 1.844 [1.602, 2.086] · 침지 1.707 · 탈리튬화 1.703 · 리튬화 1.384 | Wheatcroft 평판 1.51 · 원뿔 1.19 ([2차] D9) |
| D14 | Weibull 분위 (표 S1 모수) | pristine 1 % 78.6 · 5 % 110.4 · 50 % 189.9 · 95 % 257.6 / 침지 5 % 96.9 · 50 % 166.8 / 리튬화 5 % 37.3 · 50 % 70.4 / 탈리튬화 5 % 12.1 · 50 % 22.9 MPa · d 10 µm 의 F_c: pristine 5 % 12.4 · 50 % 21.3 mN | 2.8/π |
| D15 | 문턱에서의 P_f (F/D² × 0.891 → S) | 109.1 (코퍼스 중앙 접촉): pristine 2.8 % · 침지 5.1 % · 리튬화 92.6 % · 탈리튬화 100 % / 133 (fragmentation R 5): pristine 7.0 % · 리튬화 99.7 % / 110 (R 6): pristine ≈2.8 % / 207 (Wheatcroft 평판): pristine 45 % | 우리 값 = [2차] wheatcroft D13 · D16 |
| D16 | Fig. 1c 용량 | 탈리튬화 셀 충전 ≈184 · 리튬화 셀 충전 ≈185 → 방전 ≈163 mAh g⁻¹ · CE ≈0.88 | 판독 |
| D17 | Fig. S3 평탄 하중 → 강도 (d 12.5 µm 가정 · S = F × 5.704 MPa/mN) | pristine ≈283 · 188 · 138 · 침지 ≈216 · 164 · 161 · 리튬화 ≈80 · 69 · 45 · 탈리튬화 ≈28.5 · 21.7 | 판독 ≈ |
| D18 | 층 비 | 745 / 211 = 3.5 · 211 / 207 = 1.02 | [2차] Sedl26 · wheatcroft |
| D19 | 시험 입자 크기 분포 (126) | 5–7.5: 14 · 7.5–10: 28 · 10–12.5: 21 · 12.5–15: 27 · 15–17.5: 18 · 17.5–20: 12 · 20–22.5: 4 · 22.5–25: 2 | 판독 d |

## 14. [미확인] 목록 (본문 3 쪽 + SI 3 쪽 전수에 없음)
1. 1차입자 크기 (숫자) · 분말 PSD · 입자 선정 기준 · pristine 분말의 분산 방법.
2. 온도 · 습도 (글러브박스 수분 · 산소) · 장비 보정 (프레임 순응 · 열 표류 · 압자 면적).
3. d 계산식 (투영 면적 → 지름) · 측정 반복 · 측정 오차.
4. E · 경도 · 항복 · K_IC · 크리프 — 어느 상태에도.
5. 상태별 Li 함량 (x) — 용량 곡선 (Fig. 1c) 뿐 · 리뷰의 x ≈ 0.33 · 0.92 는 이 논문에 없다.
6. "∼5 %" 둘 (순환 부피 변화 · 첫 탈리튬화 1차입자 크기) 의 측정 방법 · 출처.
7. 신뢰구간 · 적합도 · 검정 · 상태 간 차이의 유의성.
8. 파괴 전 제하 · 반복 하중 · 되돌아옴.
9. 다접촉 · 전극 속 · 캘린더링된 입자의 강도 (무압연 전극만).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지 (저자 · 제목 · 학술지 · 권 · 호 · 쪽 · 연도 · DOI · 이력) = PDF 2 쪽 머리글 · 본문 · 초록 끝 (`txt_p2749_title_authors_abstract_doi_history.png`) — 후보 표 · 본 세션 메모 · 가리킨 카드 서지와 **같음** (호 13 · 이름 전체는 메모에 없던 것).
- 본문 + SI 글자 층 전수: 표 S1 네 줄 · 표 S2 129 값 (텍스트 층 = 렌더 크롭 대조) · 73.8 · 16.2 · 12 % · ∼5 % (두 곳) · 40 µm · 1 mN s⁻¹ · 7.3 mg cm⁻² · 48 h · 80 °C · 30 min · 10 s · 3–4.3 V · C/10 · C/20.
- 낱말 수 (본문 + SI, 표지 쪽 제외): simulat · discrete element · finite element · numerical · plastic · elastic · modulus · hardness · yield · porosity · pressure · strain = **0 회** / computational 1 · model 2 (*"fracture model"* · *"computational models"*) · toughness 1 · Weibull 9 · unload 1 · calender 3 · brittle 4 · inter-granular 4 · trans-granular 2 · cohesive 2 · stress 7 · projected area 1.
- 그림 · 표 10 장 전부 렌더로 열람 · 도구 크롭 5 장 전부 다시 자름 · 놓친 5 장 손 크롭 (§5-1).  인쇄 원문의 오타 하나: *"After the 1st-lithation"* (p. A2751, 인쇄 그대로).
- Fig. 3 은 원본 래스터 (xref 141) 에서 판독 — 눈금 최소제곱 (잔차 ≤ 0.02 µm · 0.24 MPa · 0.14 mN) · 표지 색 마스크 + 연결 성분 · 겹친 표지 = 면적 나눗셈 + k-평균 · 표 S2 와 순서 보존 짝짓기 126/129 · Fig. 3a 검산 (§3-3a).  Fig. 2a · Fig. 1c 도 원본 래스터 (xref 52 · 53) 눈금 보정으로 판독.
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI (`2.0331913jes`) · "A2749" · 제목 낱말 (*flat punch indentation*) · 제1 저자 성 · 같은 저자 (Y.-T. Cheng) grep — 이 논문 카드 없음 · 인용 카드 3 장 (stallard2022 · sedlatschek2026 · wheatcroft2023) · 같은 저자 같은 해 카드 없음.
- 이웃 카드에서 옮긴 값 (그 카드에 적힌 대로 · 원 논문 재확인 아님): `wheatcroft2023_…` 의 평판 · 원뿔 강도 · Auerbach 사다리 (§7.3 · D13) · 코퍼스 접촉 분포 (§7.4 · D16) · Weibull m 판독 (D7) / `sedlatschek2026_…` 745 MPa / `meyer2018_…` NCM111 ≈274 MPa (판독) / `stallard2022_…` 의 상자그림 판독값.

## 🔗 관련 카드
- 같은 질문 · 같은 층 (2차입자 통째 분할): `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` (NMC811 · SEM in situ · 평판 207 / 원뿔 67 · 이 논문을 [21] 로 인용) · `meyer2018_calendering_process_model_active_material_mass_loading` (활물질 6 종 미세압축 파괴 세기 · 투영 면적 규약) · `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` (σm = f/d² · 입자 파괴 판정)
- 이 논문을 인용한 카드: `stallard2022_cathode_mechanical_properties_review` ([107] · 식 4 · Fig. 10C · 13A) · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` ([32] · 입계 745 MPa 층)
- NMC 압입 · 기계 물성: `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` · `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` · `sharma2023_nmc_single_crystal_anisotropic_nanoindentation`
- 캘린더링 · DEM 에서의 입자 파괴: `sangros2019_dem_calendering_lib_electrode` · `sangros2020_lib_electrode_dem_mech_elec_ionic` · `tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond`

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
