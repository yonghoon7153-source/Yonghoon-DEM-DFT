<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-12 · 정독 54) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음의 카드들과 같은 꼴.
     원문 = 출판본 (J. Electrochem. Soc. 169, 040511 (2022) · CC BY 4.0) PDF 12 쪽 (p.1 = IOP 내려받기 표지 · 논문 = p.2–12) + Supplementary Information 1 쪽 (Table S1).
     쪽 표기 = **PDF 쪽** (p.n).  논문 쪽에는 인쇄 쪽 번호가 없다 (머리글 "Journal of The Electrochemical Society, 2022 169 040511" 뿐) — 논문 안 쪽 = PDF 쪽 − 1.  SI = "SI p.1".
     크롭 파일 이름의 p<n> 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 262 행 —
     Fig. 3c · 6 · 7 은 PDF 벡터 경로 좌표를 직접 읽었고 (축 = 틀 선 + 격자선 · 표지 중심 = 흰 내부 도형 중심 · 막대 = 같은 색 사각형 끝),
     Fig. 1b 는 200 dpi 래스터를 400 dpi 로 렌더해 색 화소 평균 (축 = 벡터 눈금 글자 중심) · 방법은 note 열에) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 ·
     [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] / [우리 산술] = 우리 쪽 값 (CLAUDE.md 출처) 과 견주는 계산 · [미확인] = 본문 11 쪽 + SI 1 쪽 전수에 없음.
     원문 12 쪽은 글자 층 추출 + 식 · 그림 영역 렌더로 전부 읽었다 (식 [1]–[10] 은 렌더에서 옮겼다).  DEM · FEM · 입자 계산 · 압밀 시뮬레이션은 없다 — 실험 + 해석 미시역학. -->
# 단결정 NMC811 (1–3 µm) 의 기저면 분해 전단강도가 탈리튬화로 준다 — 캘린더링 안 한 다공 양극 층 (액체계 LIB) 을 경도 50–946 MPa 금속 기판 위에 놓고 Vickers indentation 으로 평균 압축 견인력 = 기판 경도 H 를 걸어, 뺀 뒤 SEM 으로 슬립 띠 · 균열 입자 분율 F(H) 를 세고 Reuss 응력 + 기저면 단일 슬립 + 방위 분포 모형으로 τ_C = 86 ± 12 MPa (y = 1) → 39 ± 5 MPa (y = 0.14) — Stallard · Vema · Hall · Dennis · Penrod · Grey · Deshpande · Fleck (J. Electrochem. Soc. 2022)

> slug `stallard2022_nmc811_single_crystal_shear_strength_lithiation` · DOI `10.1149/1945-7111/ac6244` · type `experiment (Vickers indentation of an uncalendered single-crystal NMC811 cathode layer on metal substrates of hardness 50-946 MPa · post-indentation SEM particle counting · in situ CT layer thickness · Reuss stress + basal single-slip + orientation-distribution analysis — DEM · FEM · particle simulation 없음)` · PDF `58b8e04a-12._Effect_of_lithiation_upon_the_shear_strength_of_NMC811_single_crystals.pdf` · SI `188d6013-12._Sup_Effect_of_lithiation_upon_the_shear_strength_of_NMC811_single_crystals.pdf` · digested `2026-11-12` · status ✅
>
> **제목**: *Effect of Lithiation upon the Shear Strength of NMC811 Single Crystals* (p.2 · SI 머리는 대문자 *"EFFECT OF LITHIATION UPON THE SHEAR STRENGTH OF NMC811 SINGLE CRYSTALS"*).
> **저자**: Joe C. Stallard ¹,² · Sundeep Vema ¹,²,³,\* · David S. Hall ²,³,\* · Anthony R. Dennis ¹ · Megan E. Penrod ²,³ · Clare P. Grey ²,³,\*\* · Vikram S. Deshpande ¹,² · **Norman A. Fleck** ¹,²,ᶻ — ¹ Department of Engineering, University of Cambridge · ² The Faraday Institution (Harwell Campus, Didcot) · ³ Department of Chemistry, University of Cambridge — ᶻ 교신 · \* ECS Member · \*\* ECS Fellow · *J. Electrochem. Soc.* **169** (2022) **040511** (논문 번호 · 호 표기 없음) · 접수 2022-01-06 · 수정 2022-02-23 · 출판 2022-04-06 · **CC BY 4.0** (open access) · 보충 = stacks.iop.org/JES/169/040511/mmedia (Table S1 한 쪽) · 연구비 = ERC "Multilat" 669764 · Faraday Institution "FutureCat" FIRG017 · "Degradation" FIRG001 · FIRG024 · Henry Royce Institute EP/P024947/1.
> **이웃 카드 (링크만)**: [`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`](wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md) (이 논문 = 그 논문 [32] · p.7 · 카드 L196) · [`sharma2023_nmc_single_crystal_anisotropic_nanoindentation`](sharma2023_nmc_single_crystal_anisotropic_nanoindentation.md) (이 논문 = 그 논문 [12] · 카드 L191) · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) (**같은 제1 저자 · 같은 해의 다른 논문** = *Joule* 6, 984–1007 리뷰 — 그 리뷰 표에 "단결정 NMC: 없음") · [`dang2019_nmc111_secondary_particle_flat_punch_fracture_strength`](dang2019_nmc111_secondary_particle_flat_punch_fracture_strength.md) · [`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`](sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md) · [`jung2023_single_crystal_ncm_morphology`](jung2023_single_crystal_ncm_morphology.md) (우리 랩 SC/PC 구분의 실험 기준점).
> **판독 원자료**: `litdb/figures/stallard2022_nmc811_single_crystal_shear_strength_lithiation/digitized.csv` (262 행 — Fig. 6 표지 + 막대 42 · Fig. 7a/7b 표지 + 막대 48 · 7c τ_C 3 · 7d p(π/4) · 최댓값 2 · Fig. 3c h(s) 꺾은선 4 개 138 꼭짓점 · Fig. 1b c/c₀ · a/a₀ 23) · 그림 크롭 **51 장** (도구 9 = Fig. 1–8 + Table S1 · 손 크롭 42 = 패널 9 · 식 13 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 캘린더링 안 한 액체계 LIB 양극 층 (단결정 NMC811 54 · 결합제 7 · 기공 39 vol% · 65 µm) 을 경도 H 가 50.4–946 MPa 인 금속 기판 위에 놓고 Vickers 압자로 층 두께의 3.0–3.5 배까지 누르면 층에 걸리는 평균 압축 견인력이 기판 경도 H 와 같아진다는 원리로, **뺀 뒤** SEM 에서 슬립 띠 · 균열이 보이는 입자의 분율 F 를 H 에 대해 세면, F 는 H₀ = **93 · 51 · 42 MPa** (리튬 함량 y = 1 · 0.58 · 0.14) 위에서 오르기 시작하고, Reuss 균일 응력 σ = H/(1 − f) (f = 0.46) 과 기저면 분해 전단 τ = σ sin2φ/2 로 바꾸면 **기저면 전단강도 τ_C = 86 ± 12 MPa (완전 리튬화) → 39 ± 5 MPa (y = 0.14, 충전)** 이다 (p.2 초록 · p.12 결론 · Fig. 7c).  저자는 이 값이 *"upper estimates"* 라고 적고 (p.11), 캘린더링 · 압밀 전극 사이클에서 슬립 · 파괴가 일어날 것이라는 **함의**를 말한다 — 캘린더링 · 압밀 압력 실험은 없다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 시편 (단결정 NCM811 · 크기 · 리튬화 상태 · 준비) | Li-Fun Technology (중국 호남) 단결정 NMC811 양극 (테이프 캐스팅 · **캘린더링 안 함**) · NMC 면 밀도 0.167 kg m⁻² · 양극 **65 µm** + Al 15 µm (CT) · ρ 4780 kg m⁻³ 로 **NMC 54 % · 흑연 스민 고분자 결합제 7 % · 기공 39 %** · 입자 대부분 지름 **1–3 µm** · 판상 (c 축 = 판 두께 방향으로 가정) · **y = 1 (받은 그대로) · 0.58 (3.8 V) · 0.14 (4.4 V)** = 흑연 음극 · 액체 전해질 전지에서 C/20 충전 → 20 h 전압 유지 → Ar 안 분해 · DMC 헹굼 · 진공 건조 · pristine 입자 분율 = 깨끗 0.88 · 슬립 띠만 0.11 · 균열 < 0.01 | [인쇄] p.3 · Fig. 1b · Fig. 2 |
| ② ★ 시험 (방법 · 장비 · 하중 속도) | Vickers 다이아몬드 압자 (UK Calibrations · 면 경사 22° · 끝 반지름 2 µm) · Instron 5944 (2 kN 로드셀) · Ar 글러브박스 (O₂ · H₂O < 0.1 ppm) · **2 µm s⁻¹** 로 P_I 까지 → 뺌 · 기판 9 종 (Pb 50.4 · Sn-Cu 127 · Al 179 · 283 · 406 · Cu 436 · 575 · 796 · 946 MPa · 두께 ≥ 6 mm · Table S1) · P_I **25–520 N** (압흔 변위 = 층 두께의 3.0–3.5 배 · 면적 거의 같게) · 압입 뒤 SEM (×10⁴) 압자 면 가운데 (꼭짓점에서 √A_P/4) 네 장 × ≈100 입자 · 조건마다 압흔 **한 개** · 미세 압축 필라 · 평판 압축 **아님** | [인쇄] p.4–9 · SI p.1 |
| ③ ★ 전단 강도 · 리튬화 상태별 값 | **τ_C (기저면 분해 전단강도) = 86 ± 12 (y = 1) · ≈ 47 (y = 0.58, Fig. 7c 만) · 39 ± 5 MPa (y = 0.14)** · 맞춘 개시 경도 **H₀ = 93 · 51 · 42 MPa** · 모양 매개변수 **α = 20** (세 y 공통) · F₀ = 0.12 · f = 0.46 · [카드 산술] τ_C = H₀/(2(1 − f)) = **86.1 · 47.2 · 38.9** = Fig. 7c 벡터 좌표 86.11 · 47.22 · 38.89 · 막대 ±12.06 · ±6.61 · ±5.44 = 모두 값의 **14.0 %** (± 를 어떻게 냈는지 [미확인]) | [인쇄] p.2 · p.10–12 · [판독] Fig. 7c |
| ④ ★ 슬립 (면 · 방향) · 소성 흔적 · 균열 | 슬립면 = **기저면** (*"The slip plane is always parallel to the prismatic direction—that is parallel to the basal plane of the layered lattice"*, p.10 — 문장 앞 반은 c 를 '판 두께 방향' 으로 정의한 p.2 와 엇갈림) · **슬립 방향 [미확인]** (모형은 기저면 안 최대 전단 방향을 가정한 꼴) · 흔적 = 표면 슬립 띠 (Fig. 2b · 4b–d) · 균열은 슬립 뒤 — *"A negligible proportion of particles crack without slip"* (p.10) · [판독 · 벡터 Fig. 6a, y = 1] 균열 입자 분율 0.01 (pristine) → 0.16 (179) → 0.29 (283) → 0.36 (406) → 0.47 (575) → **0.62–0.63 (796–946 MPa)** · 슬립 띠만 0.21–0.29 (283–946 MPa 에서 거의 평탄) · F = 둘의 합 → 0.52–0.59 (283–436) · **0.85–0.87 (796–946)** | [인쇄] p.7 · p.9–10 · [판독] Fig. 6 · 7a |
| ⑤ ★ 슬립 ↔ 캘린더링 · 압밀 압력 (sharma2023 표기 확인) | 저자의 말 = **함의**뿐: 초록 *"This implies that particle slip and fracture will occur under mild mechanical loading, for example by calendering during manufacture and by electrical cycling of the compacted cathode"* · 결론 *"… might occur because of mild mechanical loading (e.g., via a calendaring operation) …"* · 시편 자체가 **캘린더링 안 한 층**이고 캘린더링 · 다이 압밀 실험은 없다 · 원문 낱말은 **"slip bands"** (14 회) — **"shear band" 0 회** | [인쇄] p.2 · p.12 |
| ⑥ 모델 (식 · 매개변수 · 맞춘 값) | 식 [1] σ = H/(1 − f) (Reuss) · [2] τ = H sin2φ/(2(1 − f)) · H₀ = 2(1 − f)τ_C · [3] sin2φ_U = H₀/H · [4]–[5] 방위 분포 p(φ) (횡등방) 의 누적 · [6] 맞춤 곡선 F − F₀ = (1 − F₀)[1 − ((H/H₀ − α)/(1 − α))²]^½ · [7]–[10] 역산 (p(φ_L) = p(φ_U) 가정) · 맞춘 값 = **y 마다 H₀ 하나 + 공통 α 하나** · 결정 소성 FE · 슬립계 강도 계산 **없음** | [인쇄] p.10–11 · 식 크롭 13 |
| ⑦ 저자 한계 | 층의 구성 거동 미상 · *"plastic Poisson ratio"* ≈ 0 (일축 응력 → 일축 변형) 가정 → 가로 압축 응력이 있으면 더 낮을 것 = **"upper estimates to the actual values"** (p.11) · 자료가 H/H₀ ≈ 10 = α/2 까지라 φ_L · φ_U 근처 p(φ) 불확실 (p.11) · 항복과 파괴를 가르지 않음 (*"slipped" or "unslipped"*, p.10) | [인쇄] p.10–11 |
| ⑧ 우리 쪽 (AM 강체 · 탄성 구 가정 · 300 MPa) — 판정 없이 숫자만 | 가장 유리한 방위 (φ = 45°) 의 일축 슬립 개시 응력 2τ_C = **172 MPa (y = 1)** · 94 (0.58) · 78 (0.14) [카드 산술 · f 0.46 규약 · 상한 추정] — f 를 0 으로 두면 93 · 51 · 42 MPa (= H₀) · 우리 300 MPa 압밀 끝 AM 평균 축응력 어림 **≈ 325–385 MPa** [우리 산술 · f_AM 0.675 (AM–AM) – 0.794 (상 비리얼) · φ_AM ≈ 0.62 — 세 가정 · §7-2] · 우리 DEM AM = 탄성 구 (E 140 GPa · 항복 없음) · MPM AM = 얼림 (변형 0) · **조건 차이**: 액체계 다공 층 (SE 없음 · 결합제) ↔ 황화물 복합 · Reuss 균일 응력 ↔ 접촉망 · 뺀 뒤 세기 ↔ 누른 채 · 1–3 µm 단결정 ↔ 우리 AM_P 다결정 / AM_S 단결정 | [카드 산술] · [우리] · §7 · §8 |

⛔ **한정어 (떼지 말 것)**: ① τ_C 는 **Reuss 균일 응력 + 처음 기공 f = 0.46 (결합제를 기공으로 셈)** 으로 바꾼 값이다 — Fig. 3c 의 누른 채 두께 (평탄 구간 38–49 µm ← 처음 65 µm [판독]) 는 층이 크게 치밀해졌음을 보이므로 같은 H 에서 입자 응력은 H/0.54 보다 작을 수 있다 → f ∈ [0, 0.46] 이면 τ_C(y = 1) ∈ **[46.5, 86.1] MPa** [카드 산술] — 저자도 "상한 추정" ② 세기는 **뺀 뒤** SEM 표면에서 '보이는' 슬립 띠 · 균열 — 누르는 동안의 슬립은 보지 않았다 ③ 시편 = **액체계 LIB 다공 층** (결합제 · 탄소 · 기공 39 %) — SE 없음 · 황화물 ASSB 아님 ④ 조건 (H, y) 마다 압흔 **하나** · 네 장 · ≈ 400 입자 [카드 산술] ⑤ y = 0.58 · 0.14 의 H₀ 는 사실상 **H = 50.4 MPa 한 점 + 맞춤 모양 (α 공통)** 이 정한다 (아래 시험은 0 과 50.4 MPa 뿐) — 두 상태의 막대 (40.6–53.8 ↔ 33.4–44.3 MPa) 가 겹친다 ⑥ 방위 분포 p(φ) 는 p(φ) = p(π/2 − φ) 대칭 가정의 결과 — c 가 하중과 나란한 입자와 수직인 입자를 가르지 못한다.
⇒ **절대값 전이: 0 건.** 전이되는 것은 **방향 · 크기 자릿수** (단결정 NMC811 은 기저면에서 수십 MPa 분해 전단으로 슬립하고, 탈리튬화로 절반 가까이 약해지며, 균열은 슬립 뒤에 온다) 와 **측정 · 보고 꼴** (기판 경도로 평균 압력 걸기 · 뺀 뒤 세기 · pristine 기준 F₀ 빼기 · 경도 ≠ 3σ_y) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-12 의 '왜' 칸)

의도 원문 (후보 표 `S8_candidates.md` N-12 '왜' 칸 그대로): c · k · l · 조건 R1 · R7 — 단결정 NCM811 1 차입자 전단강도가 탈리튬에 따라 준다 (Wheatcroft p.7 인용) · sharma2023 은 이 논문 주제를 "캘린더링 슬립 / 전단띠" 로 적음 (미확인) → 가압 중 AM 이 미끄럼 · 소성을 하는지 = AM 을 강체 · 탄성 구로 두는 가정 (후보 A · D0) 의 한계 근거 후보 (가리킨 카드 = wheatcroft2023 L196 · sharma2023 L191)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "단결정 NCM811 1 차입자 전단강도가 탈리튬에 따라 준다" | **채움** | p.2 초록 *"the shear strength of fully lithiated NMC811 single crystals along their basal plane is 86 ± 12 MPa, and decreases to 39 ± 5 MPa upon cell charging (delithiation of the cathode)"* · p.12 결론 같은 값 · Fig. 7c 에 y = 0.58 의 ≈ 47 MPa [판독] — **측정 조건**: 캘린더링 안 한 다공 층 (NMC 54 vol%) 속 단결정 1–3 µm · 기판 경도 = 평균 견인력 · 뺀 뒤 SEM 세기 · Reuss f = 0.46 환산 · Ar 글러브박스 · 온도 [미확인] · y 는 액체 전지에서 C/20 충전 뒤 꺼낸 상태 · "1 차입자" = 단결정 입자 그 자체 (다결정 2 차입자의 1 차 결정립이 아님) |
| "(Wheatcroft p.7 인용)" | **채움** | `wheatcroft2023_…` L196 *"단결정 NMC811 탈리튬 시 1차입자 전단강도 감소 \| p. 7 \| [32] …"* — 서지 (저자 8 명 · JES 2022 · 169 · 040511) 와 방향이 원문과 같다 (값은 옮기지 않았다) |
| "sharma2023 은 이 논문 주제를 '캘린더링 슬립 / 전단띠' 로 적음 (미확인)" (원 칸의 큰따옴표를 작은따옴표로) | **일부** | 원문 = **캘린더링 안 한 층**의 Vickers 압입 시험 · 관찰 낱말 = **"slip bands"** (본문 14 회) — **"shear band" 는 0 회** · 캘린더링은 초록 · 결론의 **함의 문장**뿐 (*"for example by calendering during manufacture"* · *"e.g., via a calendaring operation"*) · 캘린더링 압력 · 시험 없음 · sharma2023 카드의 "(값 없음)" 과 달리 원문엔 τ_C 값이 있다 |
| "→ 가압 중 AM 이 미끄럼 · 소성을 하는지" | **일부** | 단결정 NMC811 이 압축 견인력 아래 기저면으로 **슬립하고 (슬립 띠) 슬립 뒤 깨진다** — 개시 H₀ 93 MPa (y = 1) · F 0.55 (H 283) · 0.87 (796 MPa) [판독 Fig. 7a] · 그러나 ⓐ **뺀 뒤** 표면 관찰 (누르는 동안의 슬립 · 슬립 양 (변형률) 측정 없음) ⓑ 결합제 · 기공이 있는 액체계 층 (SE 기지 없음) ⓒ 입자 응력은 Reuss 어림 (접촉 응력 · 하중 몫 측정 없음) |
| "= AM 을 강체 · 탄성 구로 두는 가정 (후보 A · D0) 의 한계 근거 후보" | **일부 (근거 후보로는 채움 · 판정 근거로는 부족)** | 근거 후보 = 단결정 NMC811 은 **GPa 까지 탄성인 물체가 아니다**: 기저면 단일 슬립 τ_C 39–86 MPa · 일축 개시 2τ_C 78–172 MPa (가장 유리한 방위 [카드 산술]) · *"post-yield, the particle can bear a shear stress on the basal plane that exceeds τC"* (재밍 가정 = 슬립해도 하중을 진다 · R1) · 판정에 모자란 것 = 우리 300 MPa 복합 압밀에서 AM 입자의 **편차 응력 분포** (논문에 없음 · 우리 DEM 으로 계산할 양 · §7-2 · §9) · 논문은 DEM · ASSB 를 말하지 않는다 |
| (덧) "c — 항복 · 경도 값과 정의 · 일축 환산" | **채움** | τ_C = 기저면 임계 분해 전단 (CRSS 꼴) · 일축 환산 σ = 2τ_C/sin2φ (φ = 45° 에서 2τ_C) [식 2 에서 카드 산술] · 경도 = 3σ_y 는 *"only valid for a crystal that possesses at least 5 slip systems"* (p.3 · Hill [22]) · 다결정 NMC 2 차입자 압입 경도 **5–8 GPa** (2 차 인용 [15, 21]) · 크리프 · 속도 의존 측정 없음 (하중 속도 2 µm s⁻¹ 하나) |
| (덧) "k — DEM 의 한계" | **없음 (말 없음)** | 본문 · SI 에 DEM · discrete · particle simulation 낱말 0 회 — 간접 근거만 (위 줄) |
| (덧) "l — 소성이 왜 어려운가" | **일부** | 층상 산화물은 약한 기저면 슬립계 하나 + 훨씬 강한 2 차 슬립계 (LCO 축응력 ≈ 4 GPa, 2 차 인용 [19]) → 다결정 경도는 2 차 슬립 또는 입계 파쇄 뒤 *"granular flow"* 가 정한다 (p.3) · 일반 항복 = 독립 슬립계 5 개 필요 (p.11) ⇒ 입자 소성이 **방위 의존 · 매우 이방성 · 재밍 제한** — 계산 우회는 없다 (해석 모형 · 맞춘 값 H₀ 3 + α 1) |
| (덧) "조건 R1 · R7" | **일부** | R1 = 재밍 가정 (하중 몫 측정 없음) · R7 = 균열 분율 vs 견인력 (Fig. 6) · 균열은 슬립을 거친다 |

**가리킨 카드 · 같은 값을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `wheatcroft2023_…` L196 | *"단결정 NMC811 탈리튬 시 1차입자 전단강도 감소 \| p. 7 \| [32] J. C. Stallard, S. Vema, D. S. Hall, A. R. Dennis, M. E. Penrod, C. P. Grey, V. S. Deshpande, N. A. Fleck, J. Electrochem. Soc. 2022, 169, 040511."* | 서지 ✓ · 방향 ✓ (86 ± 12 → 39 ± 5 MPa) | **채움** (값 없이 방향만 · 이제 카드 있음) |
| `sharma2023_…` L191 | *"(값 없음) 리튬화가 NMC811 단결정의 전단강도에 미치는 영향 · 캘린더링 슬립/전단띠 \| NMC811 단결정 \| [12] J.C. Stallard, … N.A. Fleck, JES 169 (2022) 040511 \| 미확인"* | 서지 ✓ · 주제 ✓ · **"전단띠" ≠ 원문 "slip bands"** · **"캘린더링 슬립" = 함의 문장 (시편은 캘린더링 안 함 · 캘린더링 실험 없음)** · 원문엔 값 86 ± 12 → 39 ± 5 MPa | **일부** — 카드 문제 (정독 출력 batch_54 끝 절) |
| 후보 표 `S8_candidates.md` N-12 | 서지 (제목 · DOI 없음) | 저자 · 학술지 · 권 · 번호 · 연도 = 원문 첫 쪽과 같다 | **채움** — 덧붙임: 제목 · DOI `10.1149/1945-7111/ac6244` · 출판 2022-04-06 |
| `stallard2022_cathode_mechanical_properties_review` L122 (리뷰 표) | *"단결정 NMC \| — \| 없음 (구조 대책으로만 언급)"* | 같은 제1 저자의 이 논문이 단결정 NMC811 의 **첫 역학값** (기저면 τ_C) — 리뷰 자체엔 없다 (그 카드에 040511 언급 없음 · 리뷰의 단결정 NMC 인용 = [11, 137–139] 합성 · 전기화학) | 문제 아님 (그 카드 §14 에 관련 카드 한 줄만 더함) |

⇒ **의도 대조 결과: 일부** — "단결정 NCM811 (원문 표기 NMC811) 전단강도가 탈리튬으로 준다" 는 **채움** (86 ± 12 → 39 ± 5 MPa · Wheatcroft 2 차 인용 일치) · sharma2023 의 "캘린더링 슬립 / 전단띠" 는 **일부** (원문 = 캘린더링 안 한 층의 Vickers 압입 · "slip bands" · 캘린더링은 함의) · "가압 중 AM 미끄럼 · 소성 → 강체 · 탄성 AM 가정의 한계 근거" 는 근거 후보로는 채움이나 조건 (액체계 다공 층 · 뺀 뒤 SEM 세기 · Reuss 응력 · 단결정 1–3 µm) 이 달라 **판정 근거로는 일부** · DEM 한계 (k) 는 **없음 (말 없음)**.

---

## 1. 한 줄 요약
층상 산화물 단결정은 기저면 단일 슬립이 수십 MPa 에서 일어날 수 있는가 — LCO 기둥 압축 (2–4 GPa, 2 차 인용) 의 해석에서 출발해, **수백 개 단결정을 양극 층 안에서 한 번에** 시험하려고, 다공 층 (65 µm) 을 경도를 아는 금속 기판 위에 놓고 Vickers 로 깊게 눌러 층에 **기판 경도와 같은 평균 압축**을 걸고 (Bhattacharya–Nix 박막 압입 규칙), 뺀 뒤 슬립 · 균열 입자 분율 F(H) 를 센다.  F(H) 는 세 리튬화 상태에서 **H/H₀ 로 접히고** (Fig. 7b), Reuss 응력 + 기저면 분해 전단 + 방위 분포의 역산으로 τ_C(y) 와 p(φ) 를 낸다.
저자의 결론: *"This low strength suggests that fracture or plastic slip of the NMC811 single crystals might occur because of mild mechanical loading (e.g., via a calendaring operation) or due to mechanical loads generated during electrical cycling of a compacted cathode."* (p.12)

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| J. C. Stallard · S. Vema · D. S. Hall · A. R. Dennis · M. E. Penrod · C. P. Grey · V. S. Deshpande · **N. A. Fleck** (교신) — Cambridge Engineering · Chemistry · Faraday Institution · 제목 *"Effect of Lithiation upon the Shear Strength of NMC811 Single Crystals"* | J. Electrochem. Soc. **169**, 040511 (2022) · CC BY 4.0 | 10.1149/1945-7111/ac6244 | **단결정 LiNi₀.₈Mn₀.₁Co₀.₁O₂** (Li-Fun Technology) 테이프 캐스팅 양극 (흑연 스민 고분자 결합제 · Al 집전체 15 µm) · 기판 = Pb · Sn-Cu · Al 1080 · Cu C101 · 리튬화는 흑연 음극 + 액체 전해질 전지 | 실험 (Vickers 압입 + 기판 경도 · SEM 입자 세기 · in situ CT · XRD 격자는 [18] 인용) + 해석 미시역학 (Reuss · 슬립 · 방위 분포) |

- **1저자 메모와의 대조**: 저자 8 명 · 제목 · 학술지 · 권 169 · 논문 번호 040511 · 2022 — **같다**.  덧붙임 ① DOI 10.1149/1945-7111/ac6244 ② 출판 2022-04-06 (접수 01-06 · 수정 02-23) ③ 호 표기 없음 (논문 번호만) ④ PDF p.1 은 IOP 내려받기 표지 (본문 아님).
- **글의 꼴**: 서론 (캘린더링 · 단결정 · LCO 기둥 두 기전 · Scope) → Test Protocol (시편 · 리튬화 · 압입 · 층 변형 · 슬립/균열 분율) → An Estimation of Basal Plane Shear Strength (식 [1]–[10]) → 논의 (MAX 상 비유 · 리튬화 추세 · 가정 한계) → Conclusions → 참고문헌 34.  그림 8 · 표 0 (본문) · 번호 식 10 / SI = Table S1 한 쪽.
- 그룹 맥락: 같은 Fleck 그룹의 리뷰 (`stallard2022_cathode_mechanical_properties_review`, *Joule* 6) 와 2 차입자 파괴 (`wheatcroft2023_…`) 사이의 **단결정 한 알** 층.  격자 상수 · 전압 ↔ y 는 Grey 그룹 [18] (원문 목록 표기 그대로 "K. Märker, P. J. Reeves, C. Xu, K. J. Griffith, and C. P. Grey, Chem. Mater., 31, 2545 (2017)") 에서 가져온다.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 시편 · 재료 (p.2–3 · Fig. 2 · `txt_p3_test_material_composition_pristine.png` · `fig_2.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 활물질 | 단결정 LiNi₀.₈Mn₀.₁Co₀.₁O₂ · R3̄m · 단일 상 (*"exists as a single phase"*) · Li-Fun Technology Corporation Ltd. (Hunan) | [인쇄] p.2–3 |
| 입자 | 대부분 지름 **1–3 µm** · 다수가 판상 (prismatic) · c 축 = 판 두께 방향으로 **가정** (*"it is assumed that the c-axis … is aligned with the prismatic direction"*) · 서론에 단결정 입자 *"(and bi-crystals)"* (두 결정 입자) 언급 · 입자 크기 분포 · D50 [미확인] | [인쇄] p.2–3 · [판독] Fig. 2a 눈금 5 µm |
| 양극 층 | 테이프 캐스팅 · **캘린더링 안 함** · NMC 면 밀도 **0.167 kg m⁻²** · 두께 **65 µm** + Al **15 µm** (Zeiss Xradia 520 Versa CT) | [인쇄] p.3 |
| 부피 분율 | ρ_NMC811 = **4780 kg m⁻³** [23, 24] → **NMC 54 % · 흑연 스민 고분자 결합제 7 % · 기공 39 %** — [카드 산술] 0.167 / 4780 = 34.9 µm 상당 ÷ 65 µm = **0.537** ✓ | [인쇄] p.3 |
| 모형의 기공 f | **0.46** = 결합제 7 % + 공기 39 % 를 모두 기공으로 셈 (p.10) | [인쇄] p.10 |
| pristine 손상 | 10 장 × ≈100 입자 (×10⁴): 깨끗 **0.88** · 슬립 띠만 **0.11** · 균열 (단독 · 다중 · 슬립과 함께) **< 0.01** — 원인 (제조 · 취급) 에 대한 말 없음 | [인쇄] p.3 |
| 서론의 전형 값 (2 차 인용) | 캘린더링 전 활물질 0.40–0.60 · 탄소 스민 고분자 < 0.1 · 기공 30–50 % [3, 4] · 다결정 2 차입자 3–20 µm (1 차 0.1–1 µm) · 단결정 셀 4,000 사이클 뒤 > 90 % [17] | [인쇄] p.2 |

### 3-2. ★ 리튬화 상태 · 격자 (p.2–3 · Fig. 1b · `fig_1b.png` · `txt_p3_lithiation_states_c20.png`)
- **만드는 법** [인쇄 p.3]: 받은 양극 + 흑연 음극 + 액체 전해질 Li-ion 전지 ([18] 에 자세히) · **C/20** 충전 → **3.8 V (y = 0.58) · 4.4 V (y = 0.14)** → 그 전압 **20 h** 유지 → Ar 글러브박스 안 분해 · **DMC** 로 전해질 헹굼 · 진공 건조.  *"this procedure … does not change the number fraction of slipped and fractured grains prior to the indentation tests"* — F₀ 가 세 상태에서 **0.12** (scatter 안) 로 같다는 것으로 보인다 (p.10).  [판독 · 벡터] H = 0 의 F = 0.125 · 0.101 · 0.091 (y = 1 · 0.58 · 0.14) · y = 0.14 의 막대 0.066–0.117 은 0.12 를 살짝 밑돈다.
- **격자 (Fig. 1b, [18] 의 첫 충전 · 캡션 *"at 10 mAh g⁻¹"* 그대로)** [판독 · 래스터 400 dpi]: c/c₀ 는 y 가 줄면 오르다가 y ≈ **0.35 에서 최대 ≈ 1.0205** 뒤 떨어진다 (본문 p.2 *"falls for y < 0.3"* · p.11 *"decreases noticeably beyond y = 0.35"* — 두 표기) · y = 0.58: c/c₀ ≈ **1.014** · a/a₀ ≈ **0.989** · y = 0.14: c/c₀ ≈ **0.993** (가파른 구간 · ±0.003) · a/a₀ ≈ **0.980** · 전압 ↔ y 는 본문 값 (3.8 V ↔ 0.58 · 4.4 V ↔ 0.14 [인쇄 p.3]) 을 쓴다 — 그림의 전압 곡선은 판독하지 않았다.  [카드 산술] 단위포 부피비 (a/a₀)²(c/c₀) ≈ **0.991 (−0.9 %) · 0.953 (−4.7 %)**.
- **저자 해석** [인쇄 p.11 · p.12]: τ_C 는 y 1 → 0.58 에서 Li⁺ 가 빠지며 c (층 간격) 가 늘 때 빠르게 떨어지고, 0.58 → 0.14 에서 덜 변하는 것은 *"presumably because the interlayer spacing decreases noticeably beyond y = 0.35, approximately"* · 결론은 *"loss of the Li⁺ ions which hold the negatively charged metal oxide layers of the cathode together"*.
- [카드 해석] y = 0.14 에서 c 는 c₀ 보다 **작은데** τ_C 는 가장 낮다 — 층 간격만으로는 순서를 다 설명하지 못하고 (저자도 *"presumably"*), y = 0.58 ↔ 0.14 의 차이는 막대 안이다 (§3-6).

### 3-3. ★ 시험 · 기판 · 하중 (p.4–7 · Table S1 · `tab_S1.png` · `txt_p4_…` · `txt_p5_…` · `txt_p6_…` · `txt_p7_load_range_ct_rig_120N.png` · `eq_00a_hardness_PI_over_AP.png`)
- **원리** [인쇄 p.4]: Vickers 로 탄성–완전소성 고체를 누를 때 압자 면의 압축 견인력은 거의 균일하고 **크기 ≈ 기판 일축 항복강도의 3 배** (FE [25–28]) · 박막이 있어도 압입 깊이 ≫ 막 두께면 압입 압력이 거의 안 바뀐다 [29, 30] → 층의 평균 압축 = 기판 경도 H.  *"It is assumed that slip or fracture of any particle occurs when the resolved shear stress on the basal slip plane of that particle attains a critical value."*
- **기판 (Table S1, SI p.1)** [인쇄]: Pb (99.9 %) **50.4** · Sn-Cu (99/1 · Stannol) **127** · Al 1080 풀림 400 °C 1 h **179** · 풀림 343 °C 1 h **283** · 받은 그대로 **406** · Cu C101 풀림 400 °C 2 h **436** · 풀림 + 압축 가공경화 (진응력 100 MPa) **575** · (200 MPa) **796** · 받은 그대로 **946 MPa** — *"varied by a factor of almost 20"* ([카드 산술] 946/50.4 = 18.8) · 경도 = 기판만 눌렀을 때 **H = P_I/A_P** (p.6).
- **압자 · 장비** [인쇄 p.5]: Vickers 다이아몬드 (사각뿔 · 면이 바닥에서 22° · 끝 반지름 2 µm) · Instron 5944 (스크루 · 2 kN 로드셀) · Ar 글러브박스 (O₂ · H₂O < 0.1 ppm) · 2 µm s⁻¹ 로 P_I 까지 → 뺌 · 기판 두께 ≥ 6 mm · 연마.
- **반복성 (예비)** [인쇄 p.6 · p.8–9]: Al **283 MPa** · **P_I = 155 N** · y = 1 · 압흔 10 개 → 양극 표면 잔류 압흔 투영 면적 평균 **1.04 mm²** (변동 ≤ 6 %) · 슬립 또는 균열 분율 **0.49 ± 0.04** (SD).  [카드 산술] 같은 하중에서 기판만의 면적 = 155/283 = 0.548 mm² → 양극 표면 압흔이 **1.9 배** 크고 P_I/A_P(양극) = 149 MPa = **0.53 H** — 저자는 층 위 견인력 = H 를 *"the indent size of the substrate beneath the cathode layer is close to the indent size for indentation of the substrate alone"* (p.7) 로 뒷받침하고, 표면 압흔 면적과 H 의 차이는 말하지 않는다.
- **깊이 규칙** [인쇄 p.6–7]: Cu (436) · Sn-Cu (127) 에서 *"observed hardness was independent of indentation depth provided the indentation depth was greater than 2.5 times the coating thickness"* · 압입 깊이 > 층 두께 2 배면 층 위 평균 수직 견인력 ≈ H [29] · 본 시험은 P_I **25–520 N** 로 압흔 변위 = 층 두께의 **3.0–3.5 배** ([카드 산술] 195–228 µm) · 면적 거의 같게 ([카드 산술] 기판만 25/50.4 = 0.50 · 520/946 = 0.55 mm²) · 집전체에서 박리 없음.
- **세기** [인쇄 p.8–9]: 압흔 꼭짓점에서 **√A_P/4** (압자 면 가운데 · Fig. 3d 의 균일 압밀 구간) 에서 ×10⁴ SEM · 장당 ≈ 100 입자 · **조건 (기판, y) 마다 압흔 하나 · 네 장 (면마다 한 장)** → [카드 산술] 조건당 ≈ 400 입자 · 점 수 = 10 (y = 1, H = 0 포함) + 7 + 7 = 24.

### 3-4. 층의 변형 — in situ CT (p.7 · Fig. 3 · Fig. 4a · Fig. 5 · `fig_3c.png` · `txt_p7_traction_equals_H_no_delamination.png`)
- **CT 압입** [인쇄 p.7]: 자체 제작 CT 안 압입 장치 · 80 kV · 기판 = 연마한 풀림 Al 원기둥 Ø10 mm · **하중 120 N 에서 누른 채** 단면 (Fig. 3b) · 두께 h(s) (압자 면에 수직) vs 꼭짓점 거리 s (Fig. 3c) · 구간 해석 (Fig. 3d): 끝 근처 · **균일 압밀** · 전이 · 기판과 접촉 잃음.
- ⚠ **12 N ↔ 120 N**: 본문 p.7 은 Fig. 3a 를 *"annealed aluminium substrate of hardness H = 179 MPa and an indentation load P_I = 12 N"* 으로, 캡션과 CT 문장은 **120 N** 으로 적는다 (원문 그대로).  [카드 산술] 기판만이면 12 N/179 MPa = 0.067 mm² (대각 0.37 mm) · 120 N → 0.670 mm² (대각 1.16 mm) · Fig. 3a 의 양극 표면 압흔 대각 ≈ 1.57 mm [판독 · 500 µm 막대 대비 · 거칢] → 면적비 ≈ 1.8 = 155 N/283 MPa 예비 시험의 1.9 와 같은 꼴 → **120 N 쪽과 맞는다** (12 N 은 오식으로 읽힌다 [카드 해석]) · CT 기판의 경도가 179 MPa 인지 [미확인].
- **h(s) (Fig. 3c · 벡터 꺾은선 네 개)** [판독]: 끝 (s = 0) **6.8 · 13.7 · 11.0 · 15.1 µm** · 균일 구간 (s 150–350 µm) 평균 **38.0 · 40.2 · 39.9 · 48.8 µm** · s ≈ 490–540 µm 에서 71–89 µm (접촉 끝 밖) · 값이 ≈ 1.37 µm 계단 (CT 복셀로 보인다).
- [카드 산술 · 가정 = 일축 변형 (저자의 'plastic Poisson ratio ≈ 0') · h = 코팅만 · 고체 = NMC 54 + 결합제 7 %] 처음 65 µm 의 고체만 남기면 **39.7 µm** (결합제를 빈 곳으로 셈 = 35.1 µm) → 균일 구간 h 38–40 µm 셋은 **고체 분율 ≈ 1.0**, 48.8 µm 는 ≈ 0.81 — 즉 그 하중에서 층이 **거의 다 치밀해졌거나** 옆으로 흘렀다 (둘 다 일축 · f = 0.46 Reuss 가정과 어긋남).  ⇒ 같은 H 에서 입자 평균 응력은 H/(1 − 0.46) = 1.85H 보다 작을 수 있고 (치밀하면 → H), τ_C 는 **[46.5, 86.1] MPa (y = 1) · [25.5, 47.2] (0.58) · [21.0, 38.9] (0.14)** 사이 [카드 산술 · f ∈ [0, 0.46]] — 방향은 저자의 "upper estimates" 와 같다 · 개시 H₀ (≈ 93 MPa) 에서의 치밀도는 [미확인] (Fig. 3 은 H ≈ 179 MPa 급 · Fig. 5 는 H 가 클수록 더 치밀).
- **압밀 정도** [인쇄 p.7–8]: 꼭짓점 높음 → 면 따라 *"uniform state of moderate compaction"* → 가장자리 낮음 · 압흔 밖은 압밀 없음 (Fig. 4a) · 같은 자리 (√A_P/4) 의 압밀은 H 가 클수록 크다 (Fig. 5: Sn-Cu 127 · Al 406 · Cu 946 MPa).

### 3-5. ★ 슬립 · 균열 분율 (p.9–10 · Fig. 6 · 7a · 7b · `fig_6a/b/c.png` · `fig_7a.png` · `fig_7b.png` · `txt_p9_…` · `txt_p10_slip_plane_F0_H0.png`)
**[판독 · PDF 벡터 경로]** — 흑 = 슬립 띠만 · 적 = 균열 (슬립 동반 포함) · F = 둘의 합 (Fig. 6 의 합이 Fig. 7 의 F 와 ±0.0001 안에서 같다 [카드 산술]) · 막대 = 1 SD (캡션) · H 판독값은 Table S1 값과 1.1 MPa 안.

| H (MPa) | y = 1: 슬립만 / 균열 / F | y = 0.58: 슬립만 / 균열 / F | y = 0.14: 슬립만 / 균열 / F |
|---|---|---|---|
| 0 (pristine) | 0.118 / 0.007 / **0.125** | 0.075 / 0.027 / **0.101** | 0.077 / 0.014 / **0.091** |
| 50.4 | 0.107 / 0.064 / **0.171** | 0.104 / 0.080 / **0.183** | 0.181 / 0.040 / **0.220** |
| 127 | 0.164 / 0.097 / **0.261** | 0.290 / 0.173 / **0.463** | 0.324 / 0.206 / **0.530** |
| 179 | 0.221 / 0.158 / **0.379** | 0.255 / 0.308 / **0.563** | 0.347 / 0.259 / **0.606** |
| 283 | 0.258 / 0.291 / **0.548** | 0.298 / 0.459 / **0.758** | 0.400 / 0.394 / **0.794** |
| 406 | 0.235 / 0.359 / **0.594** | 0.305 / 0.538 / **0.844** | 0.386 / 0.486 / **0.873** |
| 436 | 0.209 / 0.314 / **0.523** | 0.359 / 0.442 / **0.801** | 0.426 / 0.404 / **0.829** |
| 575 | 0.287 / 0.469 / **0.756** | — | — |
| 796 | 0.251 / 0.616 / **0.867** | — | — |
| 946 | 0.221 / 0.631 / **0.852** | — | — |

- **저자의 읽기** [인쇄 p.9–10]: 모든 y 에서 슬립 + 균열이 압력과 함께 는다 · y = 1 의 슬립 띠만 분율은 *"initially rises … up to a pressure of approximately 400 MPa. This number fraction then decreases … as many of the slipped particles proceed to fracture"* · *"A negligible proportion of particles crack without slip"* · F₀ = 0.12 (세 y) · H₀ = 93 · 51 · 42 MPa · *"the dependence of F upon H/H₀ is independent of the lithiation state y"* (Fig. 7b).
- [카드 해석] 판독 값으로는 y = 1 의 슬립 띠만 분율이 283–946 MPa 에서 **0.21–0.29 로 거의 평탄**하고 최댓값은 575 MPa (0.287) 다 — "≈ 400 MPa 에서 꺾인다" 는 막대 (±0.03–0.08) 안의 흔들림과 가르기 어렵다.  균열 분율은 단조에 가깝게 는다 (406 → 436 의 0.36 → 0.31 만 예외).
- [카드 산술] **같은 H = 127 MPa** 에서 F = 0.26 (y = 1) · 0.46 (0.58) · 0.53 (0.14) — 탈리튬 쪽이 확실히 먼저 슬립한다 (방향은 자료가 직접 보인다) · H = 50.4 MPa 에서는 0.17 · 0.18 · 0.22 로 비슷하다.  아래쪽 시험 경도가 0 · 50.4 · 127 뿐이라 **H₀ 의 위치는 맞춤 모양이 정한다** — 특히 y = 0.58 (51) · 0.14 (42) 는 50.4 MPa 한 점 근처다.
- **맞춤 품질** [카드 산술 · 식 (6) · F₀ 0.12 · α 20 · H₀ 93 · 51 · 42]: 잔차 RMS **0.050 (y = 1) · 0.043 (0.58) · 0.031 (0.14) · 전체 0.043** (n = 21, H > 0) · 가장 큰 잔차 −0.118 (y = 1, 436 MPa) · H = 50.4 MPa 에서 F 가 F₀ 보다 이미 +0.05 (y = 1, H/H₀ = 0.54) · +0.06 (y = 0.58, 0.99) — 식 (6) 은 H < H₀ 에서 F = F₀ 로 둔다.
- **그려진 맞춤선 = 인쇄 매개변수** [판독 · 벡터]: Fig. 7a 의 세 곡선 외곽 점이 식 (6) (H₀ 93 · 51 · 42 · α 20 · F₀ 0.12) 에서 평균 0.18–0.24 pt 안 (Fig. 7b 의 H/H₀ 곡선 0.12 pt) · 다른 H₀ 로 그리면 (y = 1: 85 · 90 · 96 · 100 / 0.58: 45 · 57 / 0.14: 38 · 46) 2 pt 안에 남는 곡선 조각이 적거나 없고 (90 · 100 · 45 · 57 · 38 · 46) 평균 차가 −1.9 · −1.6 pt (85 · 96) 로 커진다 → 그림과 본문 매개변수가 같다 (검사 스크립트 = 정독 작업 폴더 `check_fig7_curves.py` · 외곽 점과 식 (6) 의 세로 거리).

### 3-6. ★ 모델 · 식 [1]–[10] · 맞춘 값 · 검산 (p.10–11 · Fig. 7c · 7d · Fig. 8 · `eq_01_…` – `eq_10_…` · `eq_00b_H0_onset_2tauC.png` · `eq_00c_p_pi4_value.png` · `fig_7c.png` · `fig_7d.png` · `fig_8.png`)
- **식 (렌더에서 옮김)**:
  - [1] **σ = H/(1 − f)** — *"the Reuss lower bound assumption such that the uniaxial stress σ within each crystal is related to the substrate hardness H and cathode porosity f"* · f = 0.46.
  - [2] **τ = H sin2φ / (2(1 − f))** — φ = 기저면 법선 c 와 하중 방향 (3 축) 사이 각 · τ = 0 (φ = 0, π/2) · 최대 φ = π/4.
  - (본문) **H₀ = 2(1 − f)τ_C** — 가장 유리한 방위의 항복을 여는 경도.  재밍 가정: *"the degree of slip on the basal plane is limited by jamming of the slipped particle against its neighbours, so that, post-yield, the particle can bear a shear stress on the basal plane that exceeds τC"*.
  - [3] sin2φ_U = 2(1 − f)τ_C/H = H₀/H (φ_L + φ_U = π/2).
  - [4] ∫_S p(c) ds = 1 (넓이 1 인 구 · 반지름 1/(2√π)) · 횡등방 → p(φ).
  - [5] **F − F₀ = (1 − F₀) ∫_{π/2−φ_U}^{φ_U} p(φ) sinφ dφ**.
  - [6] **F − F₀ = (1 − F₀)[1 − ((H/H₀ − α)/(1 − α))²]^½** — α > 1 (H/H₀ = α 에서 F = 1) · *"A best fit gives α = 20 for all values of y, and H₀ = 93 MPa, 51 MPa and 42 MPa"*.
  - [7] F′(H) (식 6 미분) · [8] F′(H) = [p(φ_U) sinφ_U + p(π/2 − φ_U) sin(π/2 − φ_U)] dφ_U/dH · [9] (2cos2φ_U) dφ_U/dH = −H₀/H² = −sin2φ_U/H · [10] p(φ_U) = (7) = (8) 에 p(φ_L) = p(φ_U) 를 넣은 닫힌 꼴.
- **τ_C(y)** [인쇄 · 판독 · 카드 산술]: 86.1 · 47.2 · 38.9 MPa = H₀/(2 × 0.54) 그대로 · 막대 14.0 % · 본문 ± 12 · ± 5 ([미확인]: 막대를 어떤 불확도에서 냈는지 — H₀ 의 맞춤 불확도 · 조건당 압흔 1 개의 산포 등 설명 없음) · y = 0.58 값은 본문에 숫자 없음.  [카드 산술] 2τ_C (φ = 45° 일축 개시) = **172 · 94 · 78 MPa** · y 1 → 0.58 에서 **−45 %** · 0.58 → 0.14 에서 −18 % (막대 겹침).
- **방위 분포 p(φ) (Fig. 7d)** [판독 · 벡터]: 두 봉우리 ≈ **6.8** (φ ≈ 0.03–0.04 rad 와 π/2 − 같은 값) · π/4 의 최솟값 ≈ **0.325** · φ < ≈ 0.025 rad · > π/2 − 0.025 rad 에서 0.  [카드 산술] 등방 (p ≡ 1) 이면 F(H/H₀ = 2) = 0.74 · F(4.37) = 0.89 인데 맞춤은 0.40 · 0.62 — **F 가 느리게 오르는 몫을 모형은 모두 방위 (c 가 하중과 나란하거나 수직인 입자 = 슬립이 어려운 방위) 로 돌린다**.
- ⚠ **p(π/4) 의 어긋남 (식 · 본문 ↔ 그림)** [카드 산술]: 본문 *"p(π/4) equals (1 − F₀)√(2/(α − 1))"* = 0.88 × 0.3244 = **0.2855** · 그림의 최솟값 ≈ 0.325 = **√(2/19) = 0.3244** ((1 − F₀) 없음) · 인쇄된 식 (10) 을 그대로 적분하면 ∫ p sinφ dφ = **0.880** (식 4–5 의 정규화 1 이 아님) · (1 − F₀) 를 빼면 **1.000** — 식 (5) 를 미분하면 dF/dH 에 (1 − F₀) 가 붙는데 인쇄된 식 (8) 엔 없다.  ⇒ **그림 7d 는 바르게 정규화된 역산과 맞고, 인쇄된 식 (8) · (10) · p(π/4) 문장에 (1 − F₀) 가 남는 꼴** (원문 그대로 적는다 · τ_C 에는 영향 없음 — τ_C 는 H₀ 만으로 정해진다).
- 다른 산술 메모: 본문 *"φ_L ≈ (1/α)"* — [카드 산술] H/H₀ = α 에서 φ_L = ½ asin(1/α) = **0.025 rad = 1/(2α)** (1/α = 0.05 의 절반) · 자료 끝 H/H₀ = 10.17 (y = 1, 946/93) 의 φ_L = **0.049 rad (2.8°)** → 그 밖 (φ < 2.8° 또는 > 87.2°) 에 놓인 방위 몫 = (1 − F(10.17))/(1 − F₀) = **14.4 %** — 각도로는 작지만 (저자 *"this interval of uncertainty is small"*) p(φ) 가 그 근처에서 크므로 **입자 몫으로는 1/7** · 본문 *"The derivative dφ_U/dF is obatined"* = dφ_U/dH 의 오식.
- **그림 8 의 각** [카드 해석]: (a) 안쪽 그림의 φ 호는 기저면 자취와 3 축 사이, (b) 와 본문은 **법선 c** 와 3 축 사이 — sin2φ 가 φ ↔ π/2 − φ 에 대칭이라 τ 결과는 같다.

### 3-7. τ_C 를 강도 사다리에 놓기 (★ 다른 양 · 다른 재료 — 같은 표에 넣되 견주지 않는다)
| 양 | 값 | 재료 · 상태 · 정의 | 출처 |
|---|---|---|---|
| 기저면 τ_C | **86 ± 12 → (47) → 39 ± 5 MPa** | 단결정 NMC811 1–3 µm · y 1 → 0.58 → 0.14 · Reuss f 0.46 · 상한 추정 | 이 논문 [인쇄 · 판독] |
| 일축 개시 (φ = 45°) | 172 · 94 · 78 MPa (f = 0 이면 93 · 51 · 42) | 위에서 [카드 산술] | 이 카드 |
| LCO 단결정 기둥 | 일축 압축강도 2–4 GPa · 기울어진 면 전단 모드 2 GPa (CRSS ~100 MPa 로 해석) · 균일 전위 소성 4 GPa | LCO pristine · 기둥 | 이 논문 p.2–3 의 2 차 인용 [19] (Feng 2019) |
| 다결정 NMC 2 차입자 압입 경도 | 5–8 GPa | Vickers | 이 논문 p.3 의 2 차 인용 [15, 21] |
| NMC811 다결정 2 차입자 평판 분할 | 207 ± 49 MPa (F/D²) · 원뿔 67 ± 21 | pristine · 고립 입자 | [다른 카드] `wheatcroft2023_…` |
| NMC111 다결정 2 차입자 평판 | 188 MPa (2.8F/πd²) = 211 (F/D²) | pristine | [다른 카드] `dang2019_…` |
| 단결정 NCM "입자 경도" (미세 압입기 응력–변형 최고값) | **972.7 MPa** (SC) ↔ 113.3 MPa (PC) | 우리 랩 SC-NCM D50 5 µm · 다른 양 | [다른 카드] `jung2023_single_crystal_ncm_morphology` |
| NMC811 입계 인장 | 745 MPa | 미세 인장 | [다른 카드] `sedlatschek2026_…` |
| NMC 결정립 나노 경도 | 9.4–14.3 GPa | 소결 펠릿 · 작은 압흔 | [다른 카드] `sharma2023_…` |
| LPSCl 나노압입 경도 | 1.41 GPa | 아지로다이트 | [다른 카드] `lee2025_heckel_…` (CLAUDE.md 인용) |
[카드 해석] 단결정 NMC811 의 **슬립 개시** (172 MPa, y = 1) 는 다결정 2 차입자가 **통째로 쪼개지는** 명목 응력 (≈ 200 MPa) 과 같은 자릿수이고, 우리 랩 SC-NCM 입자 압축 최고값 (973 MPa) 의 ≈ 1/6 이다 — 개시 (가장 유리한 방위 · 첫 슬립 띠) 와 최고값 (재밍 · 여러 방위 · 다중 슬립) 은 **다른 양**이라 모순이 아니다.

### 3-8. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① 층의 구성 거동 미상 → 'plastic Poisson ratio' ≈ 0 (발포 금속 비유 [34]) → *"upper estimates"* (p.11) ② 자료가 H/H₀ ≈ 10 까지 → φ_L · φ_U 근처 p(φ) 불확실 (p.11) ③ 항복 · 파괴 구분 없음 (p.10) ④ 단결정 NMC 의 역학 성질은 공개 문헌에 없었다 (p.2 · 그래서 비교 대상이 LCO · MAX 상).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. Fig. 3a 시험 하중 **12 N (p.7 본문) ↔ 120 N (캡션 · CT 문장)** (§3-4).
2. **p(π/4) = (1 − F₀)√(2/(α − 1)) = 0.2855 (p.11) ↔ 그림 7d ≈ 0.325**; 인쇄된 식 (8) 에 (1 − F₀) 없음 · 식 (10) 의 정규화 0.88 (§3-6).
3. 슬립면: *"parallel to the prismatic direction—that is parallel to the basal plane"* (p.10) ↔ p.2 의 *"The prismatic direction is denoted by the unit vector c"* (c 는 기저면 법선) — 앞 반이 뒤 반과 엇갈린다 (계산은 기저면 · 법선 c).
4. 경도 5–8 GPa 의 인용 번호: p.3 *"[15, 21]"* ↔ p.11 *"polycrystalline NMC secondary particles.15,20"* ([20] = Bi 2020 Science · 단결정 사이클 슬립 띠 논문).
5. *"several orders of magnitude less than the measured Vickers hardness"* (p.11) — [카드 산술] 5000–8000 / 86 = 58–93 · / 39 = 128–205 → **약 2 자릿수**.
6. c/c₀ 꺾임 y: p.2 *"falls for y < 0.3"* ↔ p.11 *"beyond y = 0.35"* ↔ Fig. 1b 최대 ≈ 0.35 [판독].
7. φ_L ≈ 1/α ↔ ½ asin(1/α) ≈ 1/(2α) (§3-6) · *"dφ_U/dF is obatined"* (dφ_U/dH · 오탈자).
8. y = 1 슬립 띠만 분율의 "≈ 400 MPa 최대" ↔ 판독 최대 575 MPa · 283–946 평탄 (§3-5).
9. Fig. 7b 가로축 *"H/H₀ (MPa)"* (무차원 비에 단위) · Fig. 1 캡션 *"at 10 mAh g⁻¹"* (전류 자리에 용량 단위).
10. 표기: *"uncalendered"* ↔ *"uncalendared"* · *"calendaring"* 혼용 · 본문 "Table SI" = SI 의 "TABLE S1".

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **시편**: 받은 양극 (y = 1) / 액체 전지 C/20 충전 → 분해 · 헹굼 (y = 0.58 · 0.14) → 양극을 (Al 집전체째) 기판 위에 놓음.
- **압입**: Vickers · 2 µm s⁻¹ · P_I 25–520 N (깊이 3.0–3.5 × 층 두께) → 뺌.
- **세기**: 압흔 면 가운데 네 장 × ≈100 입자 · ×10⁴ → 슬립 띠만 / 균열 (± 슬립) / 깨끗 → F = 슬립 띠 + 균열 · 평균 ± 1 SD.
- **검증**: 예비 10 압흔 (0.49 ± 0.04) · 깊이 규칙 (> 2.5 × 두께) · CT 로 기판 압흔 = 기판만의 압흔 · 박리 없음.

### 4-2. 모델 사슬
H → (Reuss) σ = H/(1 − f) → (기저면 분해 전단) τ = σ sin2φ/2 → 첫 슬립 H₀ = 2(1 − f)τ_C → F(H) 를 식 (6) 으로 맞춤 (H₀ · α) → 식 (10) 으로 p(φ) 역산.  **수치 계산 (FE · 결정 소성 · DEM) 없음** — 압입 응력장은 문헌 FE [25–28] 결과를 쓴다.

### 4-3. 입자 처리 ★
- 실험: 실제 입자 (단결정 판 1–3 µm · 결합제 · 탄소 · 기공 속) — 모양 · 크기는 세지 않고 **슬립 · 균열 유무만** 센다 (크기 의존 [미확인]).
- 모형: 입자 = **모두 같은 일축 응력 σ** (Reuss · 접촉망 · 힘 사슬 없음) 을 받는 결정 · 슬립계 = **기저면 하나** (면 안 방향은 최대 전단 쪽으로 가정한 꼴) · 2 차 슬립계 · 균열 기준 · 크기 효과 없음 · 슬립 뒤 재밍 (하중을 계속 짐).
- [카드 해석] 입자마다 응력이 다른 효과 (접촉 수 · 힘 사슬 · 크기) 를 모형은 전부 **방위 분포 p(φ)** 에 흡수한다 — 같은 F(H) 는 "등방 방위 + 응력 산포" 로도 나올 수 있고 원문은 이 둘을 가르지 않는다.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete · particle simulation 0 회).  간접: *"The mechanical properties of NMC single crystals have not been reported in the open literature to the best of the authors' knowledge."* (p.2) — 그래서 AM 을 탄성 구로 둘 때의 근거도 없었다.
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — *"The usual interpretation that the macroscopic hardness of a polycrystal equals three times its uniaxial strength is only valid for a crystal that possesses at least 5 slip systems. Layered polycrystalline ceramics have a much-reduced availability of slip systems, and consequently their macroscopic hardness may be dictated by the activation of secondary slip systems of slip strength much above that of the basal plane, or by the granular flow of the polycrystalline ceramic after it has suffered extensive fragmentation along its grain boundaries."* (p.3) · *"General yield requires slip on at least 5 independent slip systems, and a high yield strength of the required secondary slip systems results in a hardness (and uniaxial compressive strength) much above that of the basal plane shear strength."* (p.11) · *"The precise stress state within the layer depends upon its constitutive response, and this is unknown for the cathode layer."* (p.11) — 우회 = 해석 모형 (Reuss + 슬립 + 방위) · 맞춘 값 = H₀ (y 마다) + α (공통) · 비용 = 실험 24 조건 × 압흔 1 × 4 장.
3. **2D / 3D** — 실물 3D 층 · 분석은 3D 방위 (구면 좌표 · 횡등방) · 2D → 3D 에 대한 말 **없음**.
4. **압력을 뺄 때의 거동** — 세기는 **뺀 뒤** (압입 뒤 SEM: 슬립 띠 · 균열 = 남는 손상) · 누른 채는 CT 두께 h(s) 하나 · 되돌아옴 (탄성 회복 · 층 두께 회복) 측정 **없음**.

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 기저면 (basal plane) | 층상 R3̄m 의 금속–산소 층과 나란한 면 (법선 c) — 이 논문의 유일한 슬립면 |
| τ_C | 기저면 임계 분해 전단 응력 (shear strength of the basal plane) |
| 분해 전단 τ = σ sin2φ/2 | 일축 σ 가 법선이 φ 기운 면에 만드는 최대 전단 (Schmid 인자 ½ sin2φ) |
| 기판 경도 H | 기판만 눌렀을 때 P_I/A_P — 층이 얇고 깊이 눌리면 층의 평균 압축 견인력 = H |
| Reuss 가정 | 모든 결정이 같은 응력 — 입자 응력 = H/(고체 분율) |
| F · F₀ | 슬립 띠 또는 균열이 보이는 입자 분율 · pristine 값 (0.12) |
| H₀ · α | 첫 슬립 경도 · 맞춤 곡선이 F = 1 에 닿는 H/H₀ |
| p(φ) | 기저면 법선 방위 분포 (횡등방 · p(φ) = p(π/2 − φ) 가정) |
| 재밍 (jamming) | 슬립한 입자가 이웃에 막혀 슬립이 제한되고 τ_C 넘는 전단도 짐 |
| plastic Poisson ratio | 소성 변형에서 옆 변형/세로 변형 — ≈ 0 이면 일축 응력 = 일축 변형 (다공체) |
| 슬립 띠 (slip band) | 표면에 보이는 기저면 따라 어긋난 계단 줄 (Fig. 2b · 4b) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 패널 `fig_1b`) | (a) 단결정 판 · c · 층 모식 (b) c/c₀ · a/a₀ · 전지 전압 vs y (첫 충전 · [18]) · y = 0.14 · 0.58 점선 | 리튬화 상태와 격자 — A10 사이클 원장의 격자 변화 참고 (−0.9 % · −4.7 % 부피 [카드 산술]) |
| **Fig. 2** (`fig_2.png`) | SEM: (a) y = 1 층 평면 (눈금 5 µm) (b) 슬립 띠 (c) 균열 (눈금 1 µm) | 단결정 판 꼴 (구가 아님) · pristine 손상의 예 |
| **Fig. 3** (`fig_3.png` · 패널 `fig_3c`) | (a) 압흔 SEM (A–A 선) (b) in situ CT 단면 (120 N) (c) h(s) 네 곡선 (d) 변형 구간 | ★ (c) 누른 채 층 두께 38–49 µm ← 65 µm [판독] — 층 치밀화 · f 규약 검산 (§3-4) |
| **Fig. 4** (`fig_4.png`) | (a) 압흔 안 압밀 정도 (꼭짓점 · 면 · 가장자리) (b) 슬립 띠 (c)(d) 슬립 + 균열 | 슬립 → 균열 순서의 그림 |
| **Fig. 5** (`fig_5.png`) | 받은 그대로 vs Sn-Cu 127 · Al 406 · Cu 946 MPa 의 같은 자리 (√A_P/4) | 압력이 클수록 치밀 — 입자 형상 변화 · 파쇄 정성 |
| **Fig. 6** (`fig_6.png` · `fig_6a/b/c`) | 슬립만 · 균열 분율 vs H (y = 1 · 0.58 · 0.14 · ± 1 SD) | ★ R7 (AM 파괴) 분율 vs 평균 압축 [판독 · 벡터 표 §3-5] |
| **Fig. 7** (`fig_7.png` · `fig_7a/b/c/d`) | (a) F vs H + 식 (6) 맞춤 (b) F vs H/H₀ (c) τ_C vs y (d) p(φ) | ★ τ_C 86 → 47 → 39 MPa · H/H₀ 접힘 · 방위 분포 (식 ↔ 그림 어긋남 §3-6) |
| **Fig. 8** (`fig_8.png`) | (a) 압입 중 층 · 입자 · 기저면 응력 모식 (b) c · φ · θ 정의 | 모형 정의 (φ 호 그림 두 가지 · §3-6) |
| **Table S1** (`tab_S1.png`) | 기판 9 종 조성 · 열처리 · 가공경화 · 경도 | 시험 압력 사다리 50.4–946 MPa |
| 식 크롭 13 (`eq_00a` · `eq_00b` · `eq_00c` · `eq_01`–`eq_10`) · 근거 문단 20 (`txt_p*`) | H = P_I/A_P · H₀ = 2(1 − f)τ_C · p(π/4) · 식 [1]–[10] · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **세기**: 사람이 SEM 사진에서 입자 분류 (슬립 띠만 / 균열 / 깨끗) · 평균 ± SD (네 장) · 도구 [미확인].
- **H 변환**: Table S1 경도 그대로 = 층 견인력 · σ = H/0.54 · τ = σ sin2φ/2.
- **맞춤**: 식 (6) 으로 H₀ (y 마다) · α (공통) — 원문은 *"A best fit gives …"* 뿐 (최소제곱인지 · 가중 · 불확도 [미확인]) · Fig. 7b 는 H/H₀ 로 정규화한 한 곡선.
- **역산**: 식 (10) 로 φ_U(H) ↔ p(φ_U) 닫힌 꼴.
- **CT**: h(s) 를 압자 면에 수직으로 잼 (Fig. 3c) · 재구성 · 분할 방법 [미확인].
- **판독 (이 카드)**: Fig. 3c · 6 · 7 = PDF 벡터 경로 좌표 (축 틀 + 격자 선형 · 잔차 < 1e-5) · Fig. 1b = 래스터 색 화소 · 식 (6) · (10) 의 수치 검산 (정규화 · 맞춤선 대조) — digitized.csv note 열에 방법 전부.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태 · 정의가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| AM 의 역학 표현 | 단결정 NMC811: 기저면 슬립 τ_C 86 (y = 1) – 39 MPa (y = 0.14) · 슬립 뒤 균열 · 재밍 (하중 계속 짐) | DEM: AM = 탄성 구 E **140 GPa** · ν 0.25 · 항복 없음 · 파괴 = Auerbach (K_IC_AM_P 0.3 · AM_S 1.0) [우리 · CLAUDE.md · `stallard2022_…` 리뷰 카드 §7] / MPM: AM **얼림** (변형 0) [우리] | **다르다** — 이 논문은 AM (단결정) 이 수십 MPa 분해 전단에서 소성 (슬립) 함을 보인다 · 우리 두 모델 모두 AM 소성 0 · 판정은 우리 AM 편차 응력 계산 뒤 (§7-2) |
| 압밀 압력 | 기판 경도 50.4–946 MPa = 층 평균 견인력 (Vickers · 2 µm s⁻¹ · 뺀 뒤 세기) | 300 MPa 일축 다이 · 끝 상태 = 누른 채 (판 고정 완화 · 언로딩은 별도 트랙) [우리 · CLAUDE.md] | 압력 범위는 겹친다 · 하중 경로 (압흔 면 · 박막) ↔ 다이 · 상태 (뺀 뒤 ↔ 누른 채) 다름 |
| 입자 응력 | Reuss σ = H/(1 − f) · 모두 같음 | DEM 접촉망 (입자마다 다름 · 힘 사슬) · AM 하중 몫 f_AM 300 MPa: AM–AM **0.675** · 상 비리얼 **0.794** (두 운용 규약 · 미검증) [우리 · CLAUDE.md] | **정의가 다르다** — 우리는 입자별 응력 분포를 낼 수 있다 (Love–Weber) |
| AM 경도 | 다결정 2 차입자 5–8 GPa (2 차 인용) · H = 3σ 환산은 독립 슬립계 ≥ 5 일 때만 (p.3 · p.11 요지) | H_AM **3.83–3.85 GPa** (역산 · AM 하중분담) · `analyze_tabor_regime.py` σ_y,AM = H/3 = 2.0 GPa (H 6.0) [우리 · CLAUDE.md · `stallard2022_cathode_…` 카드 L26 · L373] | 이 논문은 층상 결정에서 **H/3 환산이 성립하지 않는다**고 말한다 → σ_y,AM = H/3 에 한정어 |
| SE | 없음 (결합제 · 탄소 · 기공 39 %) | LPSCl · DEM E_eff 1.35 GPa · Heckel P_y 138 MPa / MPM σ_y 0.30 GPa (일축 0.318) · E 1.53 · ν 0.49 [우리] · 랩 표준 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ (고정 · 판정 대상 아님) | **견줄 SE 값 없음** — 이 논문엔 SE 가 없다 |
| 층 치밀화 | 다공 NMC 층 65 → 38–49 µm (누른 채 · H ≈ 179 MPa 급 · 120 N) [판독] | real_14 기공 15.6 % (300 MPa) [우리] | **다른 계** (SE 없는 LIB 층 ↔ 복합) — 값 대조 아님 |
| AM 크기 · 종류 | 단결정 1–3 µm (판상) | AM_S 단결정 · AM_P 다결정 (우리 랩 구분 · `jung2023_…`) · real_14 AM_S 421 · AM_P 36 입자 [우리 · CLAUDE.md] | AM_S 쪽만 같은 부류 · 크기 의존 [미확인] |

### 7-2. ★ 300 MPa 압밀에서 AM 이 슬립하는가 — 판정하지 않고 숫자 · 조건만 놓는다
- **이 논문 쪽 문턱** (가장 유리한 방위 φ = 45°, y = 1 = 방전 상태 = 우리 압밀 상태): 일축 개시 **2τ_C = 172 MPa** (f 0.46 규약 · 저자 "상한") · f → 0 이면 **93 MPa** [카드 산술].  편차 응력으로 쓰면 최대 전단 (σ₁ − σ₃)/2 ≥ **46.5–86 MPa** 에서 가장 유리한 방위의 입자가 슬립을 연다.
- **우리 쪽 어림** [우리 산술 · 세 가정]: AM 평균 축응력 ≈ f_AM · P / φ_AM = (0.675 – 0.794) × 300 MPa / ≈ 0.62 ≈ **325–385 MPa** (φ_AM = (1 − 0.156) × (1 − SE/고체 0.26) ≈ 0.62 · real_14 · CLAUDE.md) — 비로는 172 MPa 의 **1.9–2.2 배** (93 MPa 면 3.5–4.1 배).  코퍼스 AM_P–AM_P 중앙 접촉 F/D² **109 MPa** [다른 카드 · `comparison_vs_ours_DEM.md` [Wheat23]] 은 다결정 AM_P 의 명목 접촉 응력 (다른 양).
- **이 비교가 아직 판정이 아닌 이유**: ① 다이 안 입자는 옆으로도 눌린다 — 슬립을 미는 것은 **편차 응력 (σ_zz − σ_xx)** 이지 축응력이 아니다 (이 논문도 가로 응력이 있으면 τ_C 가 더 낮게 나올 것이라 적는다 · p.11) ② 이 논문의 τ_C 는 Reuss · 다공 LIB 층 · 뺀 뒤 세기의 값 ③ 우리 AM_S (단결정) 의 크기 · 공급사가 다르다 ④ 우리 f_AM 두 규약은 플래튼 반력 분율로 검증되지 않았다 (CLAUDE.md).
- ⇒ **우리가 할 수 있는 계산** (흐름 안 · §9-1): 300 MPa 압밀 끝 DEM 침대 (real_14) 의 **AM_S 입자별 Love–Weber 응력 텐서** → (σ₁ − σ₃)/2 분포 → τ_C 범위 [46.5, 86] MPa 위에 있는 입자 분율 (방위 무시 = 상한 · 등방 방위 가정 = 중간) — 결과 전에 판정 문장을 등록한다.

### 7-3. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **AM 입자 안쪽의 역학 실측** (단결정 슬립 문턱 · 슬립 → 균열 순서) — 우리 분업의 어느 쪽에도 그 자리 (AM 소성) 가 아직 없다 (DEM = AM 탄성 구 · MPM = AM 얼림).
- 없는 반쪽: SE 기지 · 복합 압밀 · 하중 몫 · 누른 채 슬립 · 접촉 응력 · 수송.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) · AM 얼림 / DEM AM E 140 GPa · 탄성 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = 단결정 NMC811 액체계 LIB 다공 층 — **SE 없음 · 결합제 있음 · 뺀 뒤 세기**.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 규약 하나가 강도를 바꾸는 예: f 를 결합제 포함 0.46 으로 둘지 공기 0.39 로 둘지 → τ_C 86 ↔ 76 MPa (−12 %) · 누른 채 치밀화 (f → 0) 면 46.5 MPa [카드 산술] → 문헌 강도 값을 받을 때 **'고체 분율 규약 · 누른 채 / 뺀 뒤'** 칸을 둔다 · F₀ (pristine 손상 0.12) 를 기준으로 빼는 보고 꼴 | 기공 연산자 자체 (복합 · SE) 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (AM 을 변형체로 넣을 때만 아래 U1 참고) | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나) | 없음 (SE 없음).  덧: 우리 MPM SE 문턱 (일축 0.318 GPa · 보정값 · 물성 아님) 은 이 논문의 AM 단결정 슬립 개시 (172 MPa, 가장 유리한 방위) 보다 **높다** [카드 산술 · 양 · 재료 다름] — "AM 이 SE 보다 늘 단단하다" 는 가정이 방위에 따라 깨질 수 있다는 정성 경고 | 순수 SE 기공 · 항복 없음 |
| **단계 5** (3D 복합 압밀) | ★ **결과 전 대조 항목 후보**: 300 MPa 끝 AM_S (단결정) 의 편차 응력 분포 ↔ τ_C(y = 1) [46.5, 86] MPa (§7-2) · AM 소성을 넣는다면 최소 꼴 = **입자마다 기저면 슬립계 하나 + τ_C + 재밍 (슬립 뒤 하중 유지)** | 복합 속 하중 몫 · 누른 채 슬립 · 슬립 양 없음 |
| **단계 6** (탈압 · 되돌아옴) | 압력을 뺀 뒤 **남는** AM 손상 (슬립 띠 · 균열) 분율이 견인력에 따라 0.12 → 0.85 (y = 1, 946 MPa) [판독] — 탈압 뒤 관측량의 실측 꼴 · 누른 채 층 두께 (CT) 와 뺀 뒤 관찰이 섞인 보고 | 회복량 · 스프링백 · 탈압 곡선 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 (수송 · 피복 없음) · 균열 AM 은 전자 경로 · 접촉 면적을 바꿀 것 (말 없음) | — |
| **후보 D0** (지금 DEM) | ★ 한정어 근거: AM 을 **GPa 까지 탄성인 구**로 두는 가정은 단결정 NMC811 에서 기저면 슬립 (수십 MPa 분해 전단) 으로 깨질 수 있다 · AM 파괴 판정 (Auerbach 원뿔 균열 · K_IC_AM_S 1.0 *Assumed*) 과 다른 기전 — 균열이 **슬립 뒤** 온다 | DEM 의 접촉 · 겹침 한계 문장 없음 · 값 전이 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A** (MPM 강체 AM · SE 한 속도장) | ★ **AM 얼림 가정의 정면 반례 후보** — 단결정 AM 의 가장 유리한 방위 슬립 개시 (일축 172 MPa [카드 산술]) 가 우리 MPM SE 문턱 (일축 0.318 GPa · 보정값) 보다 낮다 (양 · 재료 다름 · 슬립은 재밍으로 제한 · 다결정 AM_P 는 별개) · 얼림을 유지한다면 한정어: *"AM 소성 · 슬립 미포함 (단결정 NMC811 기저면 τ_C 39–86 MPa — Stallard 2022 JES)"* | 얼림을 풀었을 때의 크기 효과 정량 없음 |
| **후보 A′** (입자별 속도장 · 다물체) | AM 을 변형체로 둘 때의 구성식 최소 꼴 (위 단계 5) · 방위 분포가 결과를 정한다 (등방 p ≡ 1 이면 H/H₀ = 2 에서 F 0.74 ↔ 맞춤 0.40 [카드 산술]) → 방위 · 조직을 입력으로 둬야 한다 | 슬립계 2 차 강도 · 경화 · 크기 효과 없음 |
| **후보 B** (입자별 FE + 접촉) | 결정 소성 FE 를 AM 에 넣는다면 τ_C (기저면) 와 "2 차 슬립 ≫" (LCO 4 GPa 축응력, 2 차 인용) 가 첫 입력 · 단결정 판 꼴 (Fig. 2) | 2 차 슬립 τ · 경화 · 탄성 이방성 없음 (탄성은 `sharma2023_…` C_ij) |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM · Thornton–Ning 류) | ⚠ AM–AM · AM–SE 접촉 항복압 p_y 를 **경도에서 옮기면** (H = 3σ_y) 층상 결정에선 틀린다 — *"only valid for a crystal that possesses at least 5 slip systems"* · 단결정 접촉 항복은 방위에 따라 기저면 슬립 쪽이 먼저 | p_y 값 없음 |
| **후보 M0** (균질화 압밀 · 캡 · Heckel) | 다공 층의 'plastic Poisson ratio ≈ 0' 가정 (발포 금속 [34]) — 낮은 밀도에서 캡 모형의 일축 변형 근사 · 다공 NMC 층 (SE 없음) 이 H ≈ 179 MPa 급에서 65 → 38–49 µm (누른 채) [판독] | 압력별 밀도 곡선 없음 · 복합 아님 |
| **U0–U6** | **U1** (입자 하나 압축) — 단결정 하나의 일축 슬립 개시 σ = 2τ_C/sin2φ 는 이방 AM 구성식의 해석해 검산 · **U3** (단단한 구를 소성 블록에 눌렀다 떼기) — 구가 아니라 Vickers (사각뿔) 지만 같은 부류: 박막 + 기판 압입에서 깊이 > 2–2.5 × 막 두께면 막의 평균 견인력 = 기판 경도 (실측 · [29, 30] · Fig. 3c) · 잔류 압흔 투영 면적 1.04 mm² = 기판만의 1.9 배 [인쇄 · 카드 산술] — '층 + 기판 누르기 · 떼기' 단위 시험의 실측 짝 (되돌아옴 측정은 없음) | U0 · U2 · U4 · U5 · U6 없음 |
| **R1–R7** | **R1** — 재밍 가정 (슬립한 AM 도 하중을 진다 · 측정 아님) · **R2** — 이 논문의 '미끄럼' 은 **입자 안 슬립** (접촉 미끄럼 · 마찰이 아님) · **R4** — 뺀 뒤 남는 손상만 · **R5** — 모형의 맞춘 값 = y 마다 H₀ 하나 + 공통 α (모양) · **R7** — 균열 분율 vs 견인력 (y = 1: 0.01 pristine → 0.16 @179 → 0.63 @946 MPa [판독]) · 균열은 슬립 뒤 | R3 · R6 (SE) 없음 |
| **결과 전 대조 항목** | ① 300 MPa 끝 AM_S 편차 응력 분포 ↔ 단결정 NMC811 τ_C(y = 1) = 86 ± 12 MPa (f 0.46 규약 · 상한) · 범위 [46.5, 86] [카드 산술] ② (AM 슬립을 넣는다면) F(H/H₀) 모양 (α = 20) 을 정성 표적 ③ (A10 사이클) τ_C 의 리튬화 의존 86 → 47 → 39 MPa — 맞추는 데 쓰지 않음 | 랩 표준 (순수 SE 10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 단결정 NMC811 (Li-Fun · 1–3 µm 판) · 액체계 LIB 다공 층 (결합제 7 % · 기공 39 % · 캘린더링 안 함) · SE 없음 · 압입 (박막 + 기판) · 뺀 뒤 SEM · 3D 실물 · Ar 글러브박스 · 온도 [미확인] · 리튬화는 액체 전지에서 — 우리 = LPSCl 복합 · 다이 300 MPa · 누른 채 계산 · 우리 AM_P 다결정 · AM_S 단결정 (크기 · 공급사 다름).

## 9. 적용 인사이트 (행동)
1. **AM 슬립 검사 (단계 5 · 결과 전 등록 뒤)**: real_14 (300 MPa) AM_S 입자별 Love–Weber 응력 → 최대 전단 (σ₁ − σ₃)/2 분포를 τ_C(y = 1) 범위 [46.5, 86] MPa 와 견준다 — 방위 무시 (상한) · 등방 방위 (½ sin2φ 가중) 두 꼴로 보고 · 판정 문장 ("AM 탄성 가정이 몇 % 입자에서 깨질 수 있다") 은 계산 전에 적는다.  AM_P (다결정) 에는 이 τ_C 를 쓰지 않는다.
2. **AM 강체 · 탄성 가정의 한정어 문장 (원고 · SI)**: *"Active-material particles are treated as elastic (DEM) or rigid (MPM); single-crystal NMC811 is reported to slip on the basal plane at resolved shear stresses of 86 ± 12 MPa (lithiated) to 39 ± 5 MPa (delithiated) in uncalendered liquid-electrolyte cathode layers (Stallard et al., J. Electrochem. Soc. 169 (2022) 040511), so AM plasticity is a model limitation."* — 값을 우리 계에 옮기지 않는다.
3. **σ_y,AM = H/3 에 한정어 (`analyze_tabor_regime.py:79-81` · `stallard2022_cathode_…` 카드 L373 의 'H/3 는 압축 소성의 대용' 한정어에 더할 원전 근거)**: 층상 결정은 슬립계가 모자라 H/3 이 일축 항복이 아니다 (p.3 · p.11).
4. **A10 사이클 원장 (흐름 밖)**: 단결정 AM_S 의 슬립 문턱이 충전 쪽에서 절반 (86 → 39–47 MPa) — 사이클 중 접촉 응력으로 단결정 슬립을 판정할 때 상태 (y) 칸 필수 · 격자 부피 −0.9 % (y 0.58) · −4.7 % (0.14) [판독 · 카드 산술] 은 Koerver 2018 카드의 값과 같은 자리에 둔다 (출처 · 상태 병기).
5. **실험 쪽 (흐름 밖 · 랩)**: 기판 경도로 평균 압력을 거는 이 방법은 우리 건식 복합 양극 (LPSCl + NCM811) 층에도 쓸 수 있다 — 같은 층을 경도가 다른 기판 위에서 눌러 뺀 뒤 AM 손상 분율을 세면 DEM 의 AM 파괴 판정 (Auerbach) 과 견줄 실측이 된다 (SE 기지라 견인력 = H 근거를 다시 세워야 한다).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Single-crystal NMC811 particles in an uncalendered cathode layer slip on the basal plane: the basal shear strength inferred from substrate-controlled Vickers indentation is 86 ± 12 MPa in the fully lithiated state and 39 ± 5 MPa after delithiation to Li₀.₁₄ (Stallard et al., *J. Electrochem. Soc.* 169 (2022) 040511); the authors note these are upper estimates."
- "For layered oxides the hardness is not three times the uniaxial yield strength, because general yield requires at least five independent slip systems (Stallard et al., 2022)."
- 국문 (한정어와 함께): *"캘린더링 안 한 액체계 양극 층의 단결정 NMC811 은 기저면에서 분해 전단 86 ± 12 MPa (완전 리튬화) – 39 ± 5 MPa (y = 0.14) 로 슬립하고 균열은 슬립 뒤에 온다 (Stallard 2022 · Reuss 환산 · 상한 추정 · 뺀 뒤 SEM 세기) — 우리 DEM · MPM 은 AM 소성을 넣지 않는다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-8 의 ①–④.
**카드가 본 한계**
1. **Reuss + f 0.46** — 누른 채 층이 거의 치밀 (Fig. 3c [판독 · 카드 산술]) → τ_C 는 [46.5, 86.1] MPa (y = 1) 범위로 읽는다.
2. **입자 응력 산포 무시** — 접촉망 · 힘 사슬 · 크기 효과를 전부 방위 p(φ) 가 흡수 · p(φ) 는 대칭 가정이라 c ∥ 하중 / c ⊥ 하중을 못 가른다.
3. **조건마다 압흔 하나 · 네 장** — 반복성은 한 조건 (283 MPa · 155 N) 의 0.49 ± 0.04 뿐.
4. **H₀ 는 맞춤값** — 아래쪽 시험 경도가 0 · 50.4 · 127 MPa 뿐 · y = 0.58 · 0.14 차이는 막대 안.
5. **± 출처 미상** (모두 14.0 %).
6. **뺀 뒤 표면 관찰** — 누르는 동안의 슬립 · 양 · 하중 몫 · 탄성 회복 없음 · 표면에 슬립 띠가 안 보이는 슬립은 세지 않는다.
7. **재료 · 계** — 액체계 LIB 다공 층 (SE 없음) · Li-Fun 단결정 1–3 µm · 액체 전지 + DMC 헹굼 · 우리 황화물 복합으로 값 전이 금지.
8. **원문 안 어긋남 10 건** (§3-8) — 12 ↔ 120 N · p(π/4) 식 ↔ 그림 · 슬립면 문장 · 인용 번호 · 자릿수 표현 등.
9. **슬립 방향 · 슬립계 · 크기 효과 · 온도 [미확인]**.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [20] | Y. Bi et al., Science, 370, 1313 (2020). | ★ 단결정 NMC811 사이클 중 슬립 띠 관찰 · 전단 응력 계산 (*"did not exceed a few hundred MPa"*, p.3) — R7 · 사이클 슬립의 원전 · 카드 없음 (kim2026 카드가 인용만) |
| [19] | L. Feng, X. Lu, T. Zhao, and S. Dillon, J. Am. Ceram. Soc., 102, 372 (2019). | ★ LCO 단결정 기둥 압축 2–4 GPa · 두 변형 모드 — 층상 산화물 단결정 항복의 원전 · 카드 없음 |
| [15] | L. S. de Vasconcelos, N. Sharma, R. Xu, and K. Zhao, Exp. Mech., 59, 337 (2019). | 다결정 NMC 2 차입자 압입 경도 5–8 GPa (이 논문 · sedlatschek2026 · sharma2023 이 2 차 인용) — 카드 없음 (`devasconcelos2016_…` 은 다른 논문) |
| [5] | T. M. M. Heenan et al., Adv. Energy Mater., 10, 2002655 (2020). | 캘린더링 → 다결정 NMC 파쇄 · 미분화 (CT) — 압밀 압력 ↔ AM 파괴 (R7) · 카드 없음 (stallard2022 · wheatcroft2023 카드가 인용만) |
| [34] | V. S. Deshpande and N. A. Fleck, J. Mech. Phys. Solids, 48, 1253 (2000). | 'plastic Poisson ratio ≈ 0' 의 근거 (다공 발포 금속 구성식) — 후보 M0 (캡 · 다공체 소성) · 카드 없음 |
| [18] | K. Märker, P. J. Reeves, C. Xu, K. J. Griffith, and C. P. Grey, Chem. Mater., 31, 2545 (2017). | Fig. 1b 격자 상수 · 전압 ↔ y 의 원전 (목록의 연도 표기 그대로) — A10 격자 변화 |
| [29] · [30] | A. K. Bhattacharya and W. D. Nix, Int. J. Solids Struct., 24, 1287 (1988). · M. F. Doerner, D. S. Gardner, and W. D. Nix, J. Mater. Res., 1, 845 (1986). | 박막 + 기판 압입에서 견인력 = 기판 경도 규칙 (U3 꼴) |
| [32] · [33] | M. W. Barsoum and M. Radovic, Annu. Rev. Mater. Res., 41, 195 (2011). · M. Higashi, S. Momono, K. Kishida, N. L. Okamoto, and H. Inui, Acta Mater., 161, 161 (2018). | MAX 상 (Ti₃SiC₂) 기저면 CRSS 16.5 MPa ↔ 압축 4 GPa 비유 |
| [21] · [13] · [22] | R. Xu … JES 164 A3333 (2017) · E. Trevisanello … Adv. Energy Mater. 11, 2003400 (2021) · R. Hill, The Mathematical Theory of Plasticity (1950) | 정본 카드 있음 (`xu2017_…` · `trevisanello2021_…`) · Hill = 교과서 |

## 13. [미확인] 목록 (본문 11 쪽 + SI 1 쪽 전수에 없음)
1. 슬립 **방향** · 2 차 슬립계 · 슬립 양 (변형률).
2. 시험 **온도** (Ar 글러브박스만).
3. τ_C 막대 (모두 14.0 %) · ± 12 · ± 5 의 계산 방법 · 식 (6) 맞춤 방법 · 가중.
4. CT 시험 기판의 경도 (Fig. 3a 문장의 179 MPa 와 같은지) · 12 N ↔ 120 N 의 바른 값 · CT 복셀 · 분할.
5. 층의 누른 채 / 뺀 뒤 기공 · 고체 분율 (f 는 처음 값 0.46 만).
6. 입자 크기 · 공급사 사양 (D50) · 크기와 슬립 · 균열의 관계.
7. pristine 슬립 띠 (0.11) 의 원인.
8. SEM 세기의 분류 기준 · 판정자 · 도구 · 보이지 않는 슬립의 비율.
9. 액체 전지 조건 ([18] 로 미룸) · DMC 헹굼이 표면 · 강도에 주는 영향.
10. 탄성 회복 · 층 두께 회복 (뺀 뒤 두께).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 PDF 12 쪽 (p.1 = IOP 내려받기 표지) + SI 1 쪽을 글자 층 추출 + 식 · 그림 · 문단 영역 렌더로 읽음.  서지 = p.2 (제목 · 저자 8 명 · 소속 · DOI · 접수 · 수정 · 출판일 · CC BY) · p.12 (감사 · ORCID · 참고문헌 34) · PDF 메타데이터 (*"Journal of The Electrochemical Society, 169(2022) 040511. doi:10.1149/1945-7111/ac6244"*).  SI = 같은 제목 · 저자 + TABLE S1.
- 원문 낱말 셈: DEM · discrete = 0 · "slip band" 14 · "shear band" 0 · calend… 11 · solid-state / sulfide = 표지 쪽의 다른 논문 광고 · 참고문헌 학술지 이름에만.
- 크롭 **51 장** = 도구 9 (Fig. 1–8 · Table S1 — 9 장 모두 그대로 씀) + 손 크롭 42 (패널 9 · 식 13 · 근거 문단 20).  본 뒤 다시 렌더 3 (fig_3c 여백 · eq_00a 이웃 낱말 · txt_p11 아래 조각).  51 장 전부 Read 로 열어 확인.  `figures.json` 의 `manual_crop` · `viewed_how`.
- 판독: digitized.csv 262 행 — Fig. 6 · 7 표지의 H 가 Table S1 경도를 1.1 MPa 안에서 재현 · Fig. 6 의 두 분율 합 = Fig. 7 의 F (±0.0001) · Fig. 7c τ_C = H₀/(2 × 0.54) (86.11 · 47.22 · 38.89) · Fig. 7a 맞춤선 = 식 (6) 인쇄 매개변수 · Fig. 7d p(π/4) ≈ 0.325 ↔ 본문 식 0.2855 (§3-6) · 식 (10) 수치 적분 0.880 / 1.000.
- 2 차 인용 대조: `wheatcroft2023_…` L196 · `sharma2023_…` L191 · 후보 표 N-12 — 고치지 않았다 (카드 문제 = 정독 출력 batch_54 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + `040511` · *"Effect of Lithiation"* · *"lithiation upon the shear"* · `Stallard` · `Vema` grep — 카드 없음 (인용만: wheatcroft2023 · sharma2023 · 같은 제1 저자의 다른 논문 = `stallard2022_cathode_mechanical_properties_review` (*Joule* 리뷰)) (2026-11-12).

## 🔗 관련 카드
- 같은 제1 저자 · 같은 해의 다른 논문 (*Joule* 6, 984–1007 리뷰 · 단결정 NMC 값 없음): [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md).
- 이 논문을 인용한 카드: `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` ([32] · p.7) · `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` ([12]).
- NCM 입자 강도 · 경도 사다리: `dang2019_nmc111_secondary_particle_flat_punch_fracture_strength` · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` · `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` · `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` · `kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review`.
- 단결정 ↔ 다결정 NCM (우리 랩 AM_S / AM_P 구분 · ASSB): `jung2023_single_crystal_ncm_morphology` · `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` · `trevisanello2021_sc_pc_ncm_cracking_diffusion`.
- 격자 · 부피 변화 (리튬화): `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`.
- 같은 Fleck 그룹 접촉 소성 이론: `mesarovicfleck2000_dissimilar_elastoplastic_indentation`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
