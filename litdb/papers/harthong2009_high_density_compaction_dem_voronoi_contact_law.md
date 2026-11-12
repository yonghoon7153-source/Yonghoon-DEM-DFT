# 고밀도 압밀 DEM 의 접촉 법칙에 **입자마다의 국소 상대밀도 (Voronoï 셀)** 를 넣어 '소성 비압축' 강성을 더하다 — 단순 입방 (SC) 격자의 입자마다 FE (MDEM · ABAQUS · 3D) 에서 곡선 맞춤한 식 (10) (계수 함수 5 개 · 인쇄 숫자 10 개) → BCC · 무작위 15 입자 (YADE) 로 검증 · 고전 독립 접촉 법칙 (Storåkers) 은 상대밀도 ≈ 0.8 (무작위 15 입자 0.85) 까지 · 새 법칙은 ≈ 0.95 까지 (납 · 탄성 없는 강소성 멱법칙 K₂ 20.5 MPa · n₂ 0.24 · 마찰 없음 · 정수압 / die · 하중을 빼는 계산 없음 · 실험 없음) — Harthong · Jérier · Dorémus · Imbault · Donzé (Int. J. Solids Struct. 2009)

> slug `harthong2009_high_density_compaction_dem_voronoi_contact_law` · DOI `10.1016/j.ijsolstr.2009.05.008` · type `DEM 접촉 법칙 (입자마다 FE = MDEM (ABAQUS, 3D, 1/8 구 2차 사면체 1200 요소 · 온 구 2600 요소) 곡선 맞춤 → YADE DEM 15 입자 · 국소 상대밀도 = Voronoï 셀 · 납 강소성 멱법칙 · 마찰 없음 · 정수압 / die · 실험 없음)` · PDF `44663ddf-29._Modeling_of_high-density_compaction_of_granular_materials_by_the_discrete_element_method.pdf` (본문 8 쪽 · SI 없음) · digested `2026-11-12` · status ✅
> topic: contact_plasticity (고밀도 · 접촉 결합 (비국소) · 소성 비압축 · 맞춘 접촉 법칙 · 2 차 접촉)
> elements: Pb (납 물성만 빌린 계산 · 실험 없음)
> methods: MDEM (meshed distinct element = 입자마다 FE, ABAQUS, 3D, J2 경화 + 선형 탄성), DEM (YADE, 증분 힘 갱신 + Voronoï 국소 상대밀도), curve fitting of contact stiffness, periodic lattices (SC, BCC), random packing (single sphere + 14 random planes; 15 spheres)
>
> **원제**: *Modeling of high-density compaction of granular materials by the Discrete Element Method* [인쇄 p.3357]
> **이웃 카드 (링크만)**: [`gonzalez2012_nonlocal_contact_confined_granular`](gonzalez2012_nonlocal_contact_confined_granular.md) (이 논문을 §1 에 인용 · 탄성 비국소 · 자유변수 0 — 이 카드를 '확보 1 순위' 로 지목) · [`demirtas2021_mpfem_hollow_sphere_die_compaction`](demirtas2021_mpfem_hollow_sphere_die_compaction.md) (ref [30] — '고밀도용 최신 처방' 목록) · [`zunker2024_bulk_elastic_partII`](zunker2024_bulk_elastic_partII.md) (이 논문의 Voronoï 판정을 자유표면적 비로 바꿈) · [`mesarovicfleck2000_dissimilar_elastoplastic_indentation`](mesarovicfleck2000_dissimilar_elastoplastic_indentation.md) (이 논문이 '≈ 0.8' 의 근거로 인용) · [`storakers1997_similarity_inelastic_contact`](storakers1997_similarity_inelastic_contact.md) (식 (14) 의 원전).
> **판독 원자료**: `litdb/figures/harthong2009_high_density_compaction_dem_voronoi_contact_law/digitized.csv` (116 행 — 래스터 화소 · 눈금 보정) · 크롭 **46 장** = 그림 12 · 식 14 (번호마다 한 장) · 근거 문단 20 — `figures.json`.

<!-- 실독 기록 (2026-11-12)
     원문 = International Journal of Solids and Structures 46 (2009) 3357–3364 · 8 쪽 (PDF 1–8 = 논문 쪽 3357–3364) · SI 없음.
     PDF = Elsevier (Acrobat Distiller 8) · 텍스트 층 온전하지만 식의 그리스 문자가 라틴 글자로 바뀌고 (α₁ β₁ γ₁ δ₁ α₂ → 'a1 b1 c1 d1 a2') 음의 부호 · 괄호 · 위첨자가 빠진다
     → 식 14 개는 300 dpi 크롭 이미지에서 다시 읽었다 (예: 식 (10) 의 둘째 항은 e^(−δ₁h/R) · 식 (14) 의 c² = 1.43e^(−0.97n₂)).
     그림 12 장은 전부 내장 래스터 (≈ 200 dpi · 벡터 경로 없음) → 값 표지: [인쇄] = 본문 · 캡션 · 식 · 그림 안 글자 ·
     [판독] = 래스터 원 화소를 눈금 (또는 눈금 글자 중심) 에 선형으로 맞춰 읽은 값 (열 화소 읽기 · 3 배 확대 격자) → digitized.csv 116 행 · 판독 오차 ≈ ±1–2 화소 ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 이 카드의 해석 · [미확인] = 원문에 없음.
     크롭 46 장: 도구 (tools/litdb/extract_figures.py) 12 장은 전부 다시 자름 (캡션 빠짐 · 본문 폭 전체 여백) + 식 14 장 + 근거 문단 20 장 (여덟 장은 두 단 · 두 쪽에 걸친 문단을 위아래로 이어 붙임) — 전부 열어 확인.
     중복 확인: 정본 litdb/papers/ 목록 (git ls-tree · 547 개) · DOI · 'Harthong' · 공저자 성 · 제목 낱말 grep → 이 논문 카드 없음 (gonzalez2012 · demirtas2021 · zunker2024 partII · comparison_vs_ours_DEM 이 인용만). -->

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Grenoble 3S-R 그룹이 **입자마다 FE (MDEM = Meshed Distinct Element Method · ABAQUS · 3D)** 로 **단순 입방 (SC) 격자의 구 하나** (대칭으로 1/8 구 · 2 차 사면체 1200 요소) 를 단순 압축 · 정수압 · die 로 눌러 보니 **h/R ≲ 0.15 까지만 세 곡선이 겹치고** (= 독립 접촉 가정이 맞는 범위) 그 뒤로 갈라져 **끝에서 힘이 무한대로 간다** (소성 비압축) — 그래서 DEM 접촉 강성을 **S = S₁(h) + S₂(ρ)** (S₁ = 고립 접촉 · S₂ = 그 구의 Voronoï 셀로 잰 **국소 상대밀도 ρ** 가 1 로 갈 때 발산) 로 두고 **계수 다섯 (α₁ β₁ γ₁ δ₁ α₂ · n₂ 의 함수 · 인쇄 숫자 10 개)** 을 MDEM 곡선에 맞췄다.  재료는 **납** (탄성 없는 강소성 멱법칙 σ = K₂εⁿ² · K₂ 20.5 MPa · n₂ 0.24 — MDEM 안에서만 E 10 GPa · ν 0.435 탄성) · **마찰 없음** · 단분산.  같은 법칙을 BCC (14 면) · 무작위 (구 하나 + 무작위 면 14 장 · 15 입자 YADE) 에 옮겨 **'상대밀도 ≈ 0.95 까지'** 를 주장한다 (초록) · 고전 독립 접촉 법칙 (Storåkers) 은 15 입자 정수압에서 **ρ 0.85 까지** MDEM 과 맞고 그 뒤로 갈라진다 (p.3363).  **하중을 빼는 계산 · 실험 · 마찰 · 다분산 · 계산 시간 수치는 없다.**

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① **e** — 점접촉 (독립 접촉) 법칙이 깨지는 밀도 | **세 층의 숫자** — (가) 문헌 요약: *"For a relative density higher than about 0.8, the mutual influence of the contacts cannot be neglected (Mesarovic and Fleck, 2000; Martin et al., 2003)"* (p.3357) · 초록 *"DEM simulations are in general limited to a relative density of about 0.8"* (나) 이 논문 MDEM (SC 구 하나): 세 하중이 **h/R ≲ 0.15** 까지 겹침 · 정수압은 **≈ 0.15** · die 는 **≈ 0.35** 에서 단순 압축과 갈라짐 (p.3358) → 상대밀도로 **0.662 (정수압) · 0.635 (die)** [카드 산술 · 식 (3) · (4)] (다) 무작위 15 입자 정수압: Storåkers DEM 이 **ρ < 0.85** 에서 MDEM 과 맞고 그 뒤 갈라짐 · 그때 **h_av/R 0.24 · h_max/R 0.44** (Storåkers) / 0.22 · 0.40 (식 10) (p.3363) · ★ 저자 설명 = **두 오차의 상쇄** — Storåkers 가 단순 압축을 넘게 잡는 만큼 실제 힘도 비압축 · impingement 로 단순 압축보다 커서 *"the difference between both remains small up to a relative density of 0.85"* | [인쇄] p.3357 · 3358 · 3363 · [카드 산술] |
| ② **e** — 대안 법칙 · 맞춘 값 수 | **식 (10) = S₁ (지수 두 개) + S₂ (α₂(ρ−ρ₀)²/(1−ρ))** · 계수 **함수 5 개** (α₁ = 0.97 − 0.58n₂ · β₁ = 1.75(1 + n₂/2) · γ₁ = 15/(1 + 3n₂) − 4 · δ₁ = 8 · α₂ = 15(1 − n₂/2)) = **인쇄 숫자 10 개** (0.97 · 0.58 · 1.75 · ½ · 15 · 3 · 4 · 8 · 15 · ½) [카드 산술 — 셈] · 맞춘 대상 = **SC 격자 MDEM** (단순 압축 · 정수압 (· die) · n₂ 0–1 · h/R 0–1) · 재료 입력 = K₂ · n₂ (+ R) · ρ₀ = 접촉이 생길 때의 평균 상대밀도 (상태 변수 · 맞춘 값 아님) · 저자: *"the proposed form of Eq. (10) is just the result of the fitting procedure"* (p.3360) | [인쇄] 식 (10)–(13) · p.3360–3361 |
| ③ 접촉 결합 (비국소) 의 꼴 | **입자 단위 부피 구속**: *"Each single contact involving a sphere i modifies its relative density ρi, and this modification affects all the contacts of the sphere i."* (p.3360) · ρ_i = 구 부피 / Voronoï 셀 부피 (Gellatly–Finney) · 쌍 ρ_ij = (ρ_i + ρ_j)/2 (식 5) — **탄성 원거리 변위 중첩 (Gonzalez 2012) 이 아니다** | [인쇄] p.3359–3360 |
| ④ '탄소성' 인가 | **MDEM 입자 = 탄소성** (σ = σ_Y + K₁ε_plⁿ¹ · E 10 GPa · ν 0.435) · **DEM 법칙 = 탄성 없는 강소성 멱법칙** (σ = K₂εⁿ² · 식 2) — *"This effect of elastic compressibility is neglected in the present work."* (그림 5 캡션) · *"the choice of a simplified material, without elasticity"* (결론) · **제하 (되돌아옴) 가지 없음** | [인쇄] p.3358 · 3360 · 3363 |
| ⑤ 새 법칙의 범위 | 초록 *"up to a relative density of about 0.95"* · 그림 11a 식 (10) 끝 ρ ≈ 0.95 · 그림 12a MDEM · 식 (10) 끝 ρ ≈ 0.955–0.96 [판독] | [인쇄] · [판독] |
| ⑥ '격자별 특성화 필요' 인가 | **원문은 반대로 주장한다**: *"the new force–displacement model is derived using periodic lattices and only under certain loading conditions. Then, this model is extrapolated to random packings, under every loading."* (p.3358) · 검증 = BCC 정수압 (국소) · BCC 정수압 · die (전체 힘) · 무작위 정수압 — **무작위 die · 전단 · 제하 검증 없음** · '격자별 특성화 필요' 는 Gonzalez (2012) 쪽의 비판 (그 카드 L828–829 · L994) — 이 논문 문장 아님 | [인쇄] p.3358 · 3361–3363 |
| ⑦ **k** — DEM 한계 (원문) | 독립 접촉 가정 (위 ①) · *"Storåkers' model has been formulated for small strain kinematics … critical for high densities"* (p.3357) · 접촉 판정 (7) 이 *"neglects the sphere's deformation"* → 옆으로 흐른 재료가 만드는 **2 차 접촉을 놓친다** (BCC: ρ > 1 이 되어야 생김 · 무작위: **0.87 · 0.91 ↔ MDEM 0.80 · 0.83**) (p.3361 · 3363) — §4j | [인쇄] |
| ⑧ **l** — 소성이 왜 어려운가 · 우회 · 비용 | 이유: 고밀도에서 힘이 h 만의 함수가 아니다 (*"cannot depend only on the relative displacement h"*) · 끝의 힘 상승 = *"plastic incompressibility of the material when free space is no longer available"* (p.3358–3359) · MDEM 은 정확하지만 *"limited to assemblies of about a hundred particles"* (p.3358) · 우회 = **FE 결과를 국소 상대밀도 하나로 압축한 DEM 법칙** (맞춘 계수 다섯) · 비용 = MDEM 15 입자 (*"To keep a reasonable MDEM calculation time"*) · 벽시계 · Δt · DEM 비용 [미확인] | [인쇄] p.3358–3363 |
| ⑨ **g** — 2D ↔ 3D | 이 논문 = **3D** (1/8 구 · 온 구 · 15 입자) · 서론: *"The first MDEM studies on granular random packings were done in 2D (Gethin et al., 2003; Procopio and Zavaliangos, 2005). Then the problem of 3D packings has been analyzed …"* (p.3357–3358) · 2D → 3D 전이 서술 없음 | [인쇄] |
| ⑩ **b** — 압력을 뺄 때 | **없음** (재하만 · 식 (6) 은 증분 갱신 · 제하 강성 · 잔류 겹침 · 판 분리 언급 없음) | — |
| ⑪ **a · i** — 기공 | 순수 SE · 복합 없음 (납 단분산) · 무작위 15 입자 처음 ρ ≈ **0.44** [판독] · 압력 단위 값 없음 (힘을 F/(K₂R²) 로만) — SC 정수압의 압력 환산은 §3e [카드 산술] | [판독] · [카드 산술] |
| ⑫ **d** — 단단한 입자의 하중 몫 | 없음 (한 재료) · 대리: BCC die 의 축 · 옆 힘 (그림 10b — 식 (10) 이 옆 힘을 ρ 0.90–0.95 에서 **+19–23 %** 크게 [판독]) | [판독] |
| ⑬ ★ 읽을 때 함정 | 본문의 '잘 맞는다' 가 그림보다 후하다 [판독]: 그림 12a 에서 ρ 0.6–0.75 의 **식 (10) = MDEM 의 0.67–0.77 배** · Storåkers 는 1.06–1.20 배 · 그림 7 에서 Storåkers 점선은 h/R **0.10 에 MDEM 다발의 1.40 배 · 0.15 에 1.53 배** (본문: *"fits the simple compression curve up to an h/R of about 0.15"*) · 그림 7 die 의 식 (10) 선 = MDEM 의 ≈ 0.85 배 (h/R 0.7–0.8) — §3d · §3f | [판독] · [카드 산술] |

**절대값 전이**: **안 된다.** 재료 = 납 (강소성 K₂ 20.5 MPa · n₂ 0.24 · MDEM 탄성 E 10 GPa) · 구 R = 5 mm / 0.19 mm · 마찰 없음 · 단분산 · 힘은 F/(K₂R²) (무차원) · 압력 · 기공 실험값 없음.  **전이되는 것은 꼴 · 판정**이다: (i) 독립 접촉이 깨지는 h/R · ρ 의 크기 감각 (ii) 고밀도 힘 발산을 **국소 상대밀도 하나**로 담는 방법과 그 값 (맞춘 계수 다섯) (iii) 강체 구 접촉 판정이 2 차 접촉을 늦게 잡는 크기 (Δρ ≈ 0.07–0.08).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-29 의 '왜' 칸)

의도 원문: *"e · k · l — 접촉 결합 (비국소) + 탄소성 + 고밀도 DEM = Gonzalez 2012 (탄성 전용) 의 '소성판' · FEM 주기격자에서 fitting 한 접촉 법칙 (자유변수 있음 · 격자별 특성화 필요 — Gonzalez §1 이 한계 명시) · Demirtas 서론의 '고밀도용 최신 처방' 목록 · 비교 문서가 '확보 1 순위 · litdb 미보유' 로 지목 → 점접촉 법칙이 깨지는 밀도와 소성 대안의 맞춘 값 수"* · 가리킨 카드 = `comparison_vs_ours_DEM` (후보 표의 줄 번호 §A L753–754 · §C L2501 · §F L3418–3428 → 이 카드 커밋 뒤 **L767–768 · L2733–2737 · L3817–3827**) · `gonzalez2012` (L617–619 · L823–829 · L959–960 · L994) · `demirtas2021` (L540–547) · `zunker2024_bulk_elastic_partII` (L20 · L71 · L250).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "접촉 결합 (비국소)" | **채움 — 꼴이 다르다** | p.3360: 각 접촉이 그 구의 ρ_i 를 바꾸고 그 변화가 **그 구의 모든 접촉**에 미친다 · ρ_i = 구 부피 (상수) / Voronoï 셀 부피 (p.3359 · Gellatly–Finney 1982) · 쌍 ρ_ij = 산술 평균 (식 5) · 결합은 **부피 (상대밀도)** 를 통하고 탄성 원거리 변위가 아니다 · 무작위 근사에서는 ρ_ij = ρ_i (*"In the case of a monodisperse packing, this consideration appears to be reasonable"* p.3362) |
| "+ 탄소성" | **일부** | MDEM 입자 = 탄소성 (식 1 · σ_Y 5 MPa · K₁ 15.5 MPa · n₁ 0.35 · E 10,000 MPa · ν 0.435 · p.3358) · **DEM 법칙 = 강소성** (식 2 · K₂ · n₂ 만 · *"the material behavior will be entirely determined by constants K2 and n2"* p.3358) · 탄성 압축성 효과 = *"neglected in the present work"* (그림 5 캡션) · 결론의 한계 *"a simplified material, without elasticity"* · 제하 가지 없음 |
| "+ 고밀도 DEM" | **채움** | 초록 *"up to a relative density of about 0.95"* · 무작위 단일 구 근사 ρ 0.675 → 0.95 (그림 11a [판독]) · 15 입자 ρ 0.44 → ≈ 0.96 (그림 12a [판독]) · 모두 **누른 채 (재하 중)** · 정수압 · 마찰 없음 · 압력 단위 없음 (F/(K₂R²)) |
| "= Gonzalez 2012 (탄성 전용) 의 '소성판'" | **일부** | 소성 쪽인 것은 맞다 · 그러나 (i) **이 논문이 3 년 앞선다** (2009 ↔ 2012 · Gonzalez 가 §1 에서 이 논문을 인용) (ii) 결합 꼴이 다르다 (FE 곡선 맞춤 · 국소 상대밀도 ↔ 닫힌형 탄성 원거리 변위 · 자유변수 0) → '소성판' 은 이 묶음의 자리 매김이지 같은 정식화의 소성 확장이 아니다 |
| "FEM 주기격자에서 fitting 한 접촉 법칙" | **채움** | SC 격자 = 구 하나 + 강체 면 · 대칭으로 1/8 구 · ABAQUS · **2 차 사면체 1200 요소** (곡선 맞춤용) · 온 구 2600 요소 (여러 입자용) · 큰 변위용 · 표면에서 잘게 (p.3358) · 단순 압축 · 정수압 · die · n₂ = 0 · 0.1 · 0.24 · 0.5 · 1 (그림 6 캡션 · 본문은 0.8 — §3f) · h/R 0–1 |
| "(자유변수 있음 …" | **채움** | 계수 함수 5 개 · 인쇄 숫자 10 개 (§4e 감사표) · 함수 꼴 (지수 둘 · (ρ−ρ₀)²/(1−ρ)) 도 곡선 맞춤으로 고름 · S₂ 는 *"could be much more simplified by restraining the values of n2 or h/R"* (p.3361) |
| "… 격자별 특성화 필요 — Gonzalez §1 이 한계 명시)" | **없음 (이 논문 안에는)** | 원문은 **한 번 맞춘 SC 법칙을 무작위 충전 · 모든 하중으로 옮긴다**고 쓴다 (p.3358 · *"under every loading"*) · 결론 *"a useful law for random packings is extracted from a simple periodic lattice"* · 검증은 BCC · 무작위 **정수압**뿐 (무작위 die 없음) · 원문 자신의 어긋남 (2 차 접촉 지연 · die · 중간 밀도 −23 – −33 % [판독]) 은 '특성화가 더 필요할 수 있다' 는 근거는 된다 · Gonzalez §1 의 문장은 이 카드에서 대조 못 함 (Gonzalez 원문 미열람 — 그 카드의 영어 인용만) |
| "Demirtas 서론의 '고밀도용 최신 처방' 목록" | **채움** | demirtas2021 카드 L547: ref **[30]** = 이 논문 · 그 목록의 공통 서술 *"require particular calibration methods, which increase the computational cost of DEM"* (Demirtas 의 말) — 보정 (MDEM 맞춤) 은 이 논문에 있다 · **DEM 계산 비용 증가의 수치는 이 논문에 없다** [미확인] |
| "비교 문서가 '확보 1 순위 · litdb 미보유' 로 지목" | **채움 (이제 낡음)** | `comparison_vs_ours_DEM` L767–768 (§A) · L3818 · L3823–3827 (§F) — 이 카드로 '미보유' 는 낡았다 |
| "→ 점접촉 법칙이 깨지는 밀도" | **채움** | 위 §0 ① — 문헌 ≈ 0.8 · SC MDEM h/R 0.15 (정수압 · ρ 0.662) / 0.35 (die · ρ 0.635) [카드 산술] · 무작위 15 입자 0.85 (h_av/R 0.24) · 단 판독상 Storåkers 의 어긋남은 그보다 이르다 (§3d) |
| "→ 소성 대안의 맞춘 값 수" | **채움** | 5 함수 · 10 숫자 (+ 함수 꼴 선택) · 맞춘 대상 = SC MDEM · Storåkers (식 14) 는 c² = 1.43e^(−0.97n₂) (출처 표기 없음 — Storåkers 1997 로 읽힌다 [카드 추론]) |
| (★ 지시서) 재료 · 입자 | **채움** | 납 · 강소성 K₂ 20.5 MPa · n₂ 0.24 ↔ σ_Y 5 · K₁ 15.5 MPa · n₁ 0.35 · E 10 GPa · ν 0.435 · 구 R = 5 mm (기본) · 0.19 mm (15 입자) · 단분산 · 마찰 없음 · 납 값의 출처 표기 없음 [미확인] |
| (★) 힘–변위 법칙 식 전부 · 변수 뜻 · 맞춘 대상 | **채움** | 식 (1)–(14) — §4 · 크롭 `eq_01` … `eq_14` |
| (★) 고전 점접촉이 깨지는 상대밀도 · 새 법칙의 최대 | **채움** | ① · ⑤ |
| (★) 압밀 곡선 DEM ↔ FE ↔ 실험 · 제하 | **일부** | DEM ↔ FE 만 (그림 7 · 8 · 10 · 11 · 12 · 힘 대 h/R 또는 ρ) · **실험 없음** (*"an experimental validation can be easily planned"* p.3358 — 계획만) · **제하 없음** · 압력 축 없음 (SC 정수압 압력 환산 = §3e [카드 산술]) |
| (★) '격자별 특성화' 원문 위치 · 비용 · 저자 한계 | **일부** | 위 · 비용 = MDEM ≈ 100 입자 한계 · 15 입자 · SC = *"simple and cheap (in terms of CPU time)"* · 숫자 [미확인] · 저자 한계 = §4j · §11 |

**2 차 인용 대조 (카드 문제 — 고치지 않음)**:
- `gonzalez2012_*` **L617–619** · **L823–829** · **L959–960**: 서지 (*IJSS 46, 3357–3364*) **같다** · 'FEM 단순 주기격자 fitting' **같다** · Gonzalez §1 영어 인용 *"… nonlocal-deformation effects during high-density compaction of elasto-plastic particles"* 은 MDEM 입자 (탄소성) 로는 맞다 · 그러나 카드 요약 **'비국소 + 탄소성 + 고밀도'** (L619 · L960 — L827 은 '비국소 + 소성 + 고밀도' 로 맞게 적음) 의 **'탄소성'** 은 **일부만 맞다** — DEM 법칙 (식 10) 은 탄성 없는 강소성 멱법칙 (식 2) 에 맞춘 것이고 탄성 효과는 버렸다 (그림 5 캡션 · 결론).  'litdb 미보유 · 확보 1 순위' 는 이 카드로 낡았다.
- `gonzalez2012_*` **L828–829** · **L994** (*"격자별 case-by-case 특성화가 필요하다 (이 논문 §1 이 그 한계를 지적한다)"* · *"쌍 상호작용을 case-by-case 특성화해야 한다"*): **Harthong 원문의 자기 진술이 아니다** — 원문은 SC 에서 맞춘 법칙을 무작위 · 모든 하중으로 옮긴다고 쓴다 (p.3358).  Gonzalez 쪽 비판으로만 인용할 것 (Gonzalez 원문은 이 카드에서 대조 안 함).
- `comparison_vs_ours_DEM` **L767–768** (§A · *"FEM 주기격자 fitting, 비국소+탄소성+고밀도 = 이 논문의 소성판"*) · **L3817–3818** (§F · *"소성 비국소는 Harthong 2009 가 유일한 후보인데 litdb 미보유 + fitting 필요"*) · **L3823–3827** (§F · 서지 + *"⚠ 그쪽은 FEM 에서 fitting 하므로 자유변수가 있고 격자별 case-by-case 특성화가 필요하다 (Gonzalez §1 이 그 한계를 명시)"*): 서지 · 'FEM 주기격자 fitting' · '자유변수' **같다** · **'탄소성' 은 일부** (위와 같음) · '격자별 특성화' 는 Gonzalez 의 비판 (이 논문 문장 아님) · '미보유' 낡음.
- `comparison_vs_ours_DEM` **L2733–2737** (§C · Demirtas 인용 *"require particular calibration methods, which increase the computational cost of DEM"*): Demirtas 의 말을 옮긴 것 — 이 논문에 **보정 (MDEM 맞춤) 은 있고 DEM 비용 수치는 없다**.
- `demirtas2021_*` **L547** (*"[30] Harthong et al., Int. J. Solids Struct. 46 (2009) 3357 | 고밀도 압밀 DEM"*): **같다**.
- `zunker2024_bulk_elastic_partII` **L20 · L250** (*"Voronoï 셀 계산 (Harthong 2009)"* · *"replacing the Voronoï-cell computation of Harthong et al."*): **같다** (p.3359 · 3363).  **L71** (*"경험적 · Voronoï 셀 · 계산비용 큼(대규모 불가) + 강소성 한정(탄성 부피변화 미고려)"*): '경험적' · 'Voronoï' · '강소성 한정 (탄성 부피변화 미고려)' **같다** · **'계산비용 큼 (대규모 불가)' 는 이 논문에 없다** (DEM 비용 · 입자 수 한계 서술 없음 — 이 논문의 '≈ 100 입자 한계' 는 MDEM 의 것) → Zunker 쪽 평가로만 인용할 것.

⇒ **의도 대조 결과: 일부** — 접촉 결합 (국소 상대밀도 · 부피 꼴) · 고밀도 (≈ 0.95) · FEM 주기격자 맞춤 · 자유변수 (함수 5 · 숫자 10) · 깨지는 밀도 (≈ 0.8 · SC h/R 0.15 / 0.35 → ρ 0.66 / 0.64 · 무작위 0.85) 는 **채움** · '탄소성' 은 **일부** (DEM 법칙은 탄성 없는 강소성 · 제하 없음) · '격자별 특성화 필요' 는 이 논문 안에 **없음** (원문은 반대로 SC → 무작위 외삽을 주장) · 'Gonzalez 의 소성판' 은 **일부** (3 년 앞선 · 다른 꼴의 결합).

---

## 1. 한 줄 요약

고밀도 분말 압밀에서 접촉이 서로 독립이라는 DEM 의 가정 (Storåkers 류) 은 상대밀도 ≈ 0.8 근처에서 깨진다 — 저자들은 그 효과를 입자마다 FE (MDEM) 로 단순 입방 격자에서 재고, **접촉 강성 = 고립 접촉 항 S₁(h) + 그 입자의 Voronoï 국소 상대밀도로 발산하는 소성 비압축 항 S₂(ρ)** 로 압축한 법칙 (식 10 · 계수 다섯을 곡선 맞춤) 을 DEM (YADE) 에 넣어, BCC · 무작위 15 입자 정수압에서 MDEM 전체 힘을 상대밀도 ≈ 0.95 까지 따라간다고 보인다 — 단 강체 구 접촉 판정 때문에 2 차 접촉은 늦게 (무작위 0.87 · 0.91 ↔ MDEM 0.80 · 0.83) 잡힌다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **B. Harthong** \* · J.-F. Jérier · **P. Dorémus** \* · D. Imbault · F.-V. Donzé (\* 교신) |
| 소속 | Laboratoire 3S-R, Domaine universitaire, BP 53, 38041 Saint Martin d'Hères cedex 9, France (Grenoble) |
| 저널 | **International Journal of Solids and Structures 46 (2009) 3357–3364** (8 쪽) |
| DOI | **10.1016/j.ijsolstr.2009.05.008** (첫 쪽 아래 · PDF 정보 같음) |
| 이력 | Received 8 January 2009 · revised 27 March 2009 · available online 18 May 2009 |
| 키워드 | Discrete Element Method · Force–displacement relationship · High-density compaction · Granular media |
| 소재 | **납** (강소성 멱법칙 · 금속 분말 냉간 압밀 맥락) — 배터리 소재 없음 · 실험 없음 |
| 연구 유형 | 입자마다 FE (ABAQUS · 3D) → 해석 접촉 법칙 곡선 맞춤 → DEM (YADE) 검증 |
| SI | 없음 |
| 서지 대조 | 후보 표 N-29 (*"(비교 문서 표기 · DOI 없음)"*) 의 저자 · 제목 · 학술지 · 권 · 쪽 · 해 **같다** · DOI 는 원문 첫 쪽에 있다 (**10.1016/j.ijsolstr.2009.05.008**) · 원제의 'Discrete Element Method' 는 대문자 (PDF 파일 이름은 소문자) |

**자기 위치 선언 (초록 p.3357)**
> *"Cold compaction of metal powders is now commonly studied at a microscopic scale, to further our understanding of contact mechanics between grains. … DEM simulations are in general limited to a relative density of about 0.8, because the existing contact laws do not reproduce all the physical phenomena involved in the densification of granular media. … Thus, it will be possible with DEM modeling to reproduce high-density compaction of random packings up to a relative density of about 0.95. By introducing a local relative density parameter in the force–displacement relationship, the incompressibility effects which rule high-density behaviors can be introduced in the modeling of powder compaction."* (`txt_p01_abstract_dem_0p8_new_law_0p95_local_density`)

---

## 3. 핵심 수치 총정리 ★

### 3a. 계산 조건 (p.3358 · 그림 2 · 표지 [인쇄])

| 항목 | 값 | 위치 |
|---|---|---|
| MDEM 재료 (식 1) | 탄소성 Von Mises + 경화: σ = σ_Y + K₁ε_plⁿ¹ · **σ_Y 5 MPa · K₁ 15.5 MPa · n₁ 0.35** · 선형 등방 탄성 **E 10,000 MPa · ν 0.435** | p.3358 · `txt_p02_lead_k2_n2_sy_e_nu_r5mm_frictionless` |
| DEM 재료 (식 2) | 강소성 멱법칙 σ = K₂εⁿ² · **K₂ 20.5 MPa · n₂ 0.24 (납)** — *"The DEM approach is based on Eq. (2) whereas Eq. (1) is used in the MDEM simulations. Then Eqs. (1) and (2) are set equal to one another. By adjusting the values of the coefficients in Eqs. (1) and (2), a similar loading curve should be obtained."* | p.3358 |
| 납 값의 출처 | 표기 없음 [미확인] · *"By choosing this material, an experimental validation can be easily planned."* (실험은 이 논문에 없음) | p.3358 |
| 입자 | 같은 반지름 구 **R = 5 mm** (*"except when mentioned"*) · 무작위 15 입자 **R = 0.19 mm** · **마찰 없음** · 단분산 · 점착 없음 | p.3358 · 3363 |
| FE 코드 · 메시 | **ABAQUS** · SC 셀 = 구 하나 + 강체 면 → 대칭으로 **1/8 구** · 1/8 구 **2 차 사면체 1200 요소** (곡선 맞춤) · 온 구 **2 차 요소 2600** (여러 입자) · *"designed to investigate large displacements and to reduce computation time"* · 표면에서 잘게 | p.3358 · 그림 2 · `txt_p02_sc_eighth_sphere_abaqus_1200_2600_quadratic_tet` |
| 하중 (SC) | **단순 압축** (고립 구 두 판 사이) · **정수압** (여섯 면) · **die** (위아래만 · 옆 고정) | p.3358 · 그림 3 |
| 하중 (BCC) | 국소: 구 하나를 **강체 면 14 장**으로 (정수압만 — 미끄러지는 대각 접촉을 위한 면 회전을 피하려고) · 전체 힘: BCC 단위 셀 정수압 · die (축 · 옆 힘) | p.3361 · 그림 8 · 10 |
| 하중 (무작위) | 구 하나 + **무작위 강체 면** (14 접촉 = 처음 12 + 2 차 2) · 면은 회전 없이 평행 이동 · 이동량 ∝ 중심까지 처음 거리 · *"without any rearrangement"* · 15 입자 정수압 (MDEM ABAQUS ↔ DEM YADE) | p.3362–3363 · 그림 11 · 12 |
| DEM 코드 | **YADE** (Kozicki & Donzé 2008 · 공개) — 국소 상대밀도 계산 + 식 (10) + Storåkers 구현 | p.3363 |
| 힘의 표기 | **F/(K₂R²)** (무차원) — 압력 · 응력 단위 값 없음 | 그림 3–12 |
| 온도 · 속도 · Δt · 반복 수 | [미확인] (준정적 · 동역학 언급 없음) | — |

### 3b. 점접촉 (독립 접촉) 이 깨지는 곳 — 이 카드의 답 (e)

| 출처 | 문턱 | 상대밀도로 | 표지 · 위치 |
|---|---|---|---|
| 문헌 요약 (서론) | *"For a relative density higher than about 0.8, the mutual influence of the contacts cannot be neglected (Mesarovic and Fleck, 2000; Martin et al., 2003)"* | **≈ 0.8** | [인쇄] p.3357 · `txt_p01_independent_contacts_limit_0p8_small_strain` |
| 초록 | *"DEM simulations are in general limited to a relative density of about 0.8"* | ≈ 0.8 | [인쇄] p.3357 |
| SC MDEM — 세 하중이 겹침 | *"the three curves are superimposed (h/R less than about 0.15). This zone corresponds to the validity domain when independent contacts are assumed."* | h/R 0.15 → 정수압 ρ **0.662** · die ρ 0.566 | [인쇄] p.3358 · [카드 산술] 식 (3) (4) (ρ₀ = π/6 = 0.524) |
| SC MDEM — 정수압이 갈라짐 | *"h/R greater than about 0.15 for hydrostatic compaction"* | **0.662** | [인쇄] · [카드 산술] |
| SC MDEM — die 가 갈라짐 | *"about 0.35 for die compaction"* | **0.635** | [인쇄] · [카드 산술] |
| SC 끝 (ρ → 1) | *"the force increases to infinity for hydrostatic and die compaction"* | h/R **0.388** (정수압) · **0.953** (die) 에서 ρ = 1 | [인쇄] · [카드 산술] (2 − (4π/3)^(1/3) · 2 − π/3) |
| 무작위 15 입자 (정수압) | Storåkers DEM 이 *"good agreement … when the relative density is less than 0.85. After that, Storåkers' law diverges"* | **0.85** (그때 h_av/R 0.24 · h_max/R 0.44 — Storåkers) | [인쇄] p.3363 · `txt_p07_15_spheres_r0p19mm_yade_agreement_below_0p85` · `txt_p07_overlap_at_0p85_hmax_0p44_hav_0p24_storakers_fits` |
| 무작위 15 입자 — 0.85 까지 맞는 이유 (저자) | *"For these values of h/R, Eq. (14) overestimates the simple compression condition, as shown in Fig. 7, but because of plastic incompressibility and contact impingement, the real force is also greater than the simple compression force, such that, the difference between both remains small up to a relative density of 0.85."* | = **고전 법칙의 '맞음' 이 두 오차의 상쇄** (단일 접촉 과대 ↔ 결합 효과 누락) · 상쇄가 끝나는 곳이 0.85 | [인쇄] p.3363 · `txt_p07_overlap_at_0p85_hmax_0p44_hav_0p24_storakers_fits` |
| Storåkers ↔ 단순 압축 (그림 7) | 저자: *"Eq. (14) fits the simple compression curve up to an h/R of about 0.15, and the hydrostatic compaction of the simple cubic structure up to h/R = 0.35"* | — | [인쇄] p.3363 · ⚠ 판독은 다름 (§3d) |

★ **SC 격자에서는 '깨지는 밀도' 가 0.63–0.66** 이다 (처음 0.524 에서 +0.11–0.14) — 서론의 '≈ 0.8' 은 **무작위 충전의 문헌 값**이다 (처음 밀도가 다르다).  ⇒ '몇 % 밀도에서 깨진다' 를 한 숫자로 옮기면 안 되고 **처음 충전 · 하중 경로**를 같이 적어야 한다 [카드 추론].

### 3c. 새 법칙의 범위 · 검증 (BCC · 무작위)

| 검증 | 결과 (원문) | 판독 숫자 (digitized.csv) |
|---|---|---|
| SC 단순 압축 · 정수압 (그림 6 · n₂ 0–1) | 식 (10) 과 MDEM 비교 — 맞춤의 근거 그림 | 이 카드가 식 (12) 를 적분한 값이 그림 6a 를 h/R 0.98 에서 **2–3 % 안**으로 재현 (n₂ 0 · 0.1 · 0.24 · 0.5 · 1: 3.90 · 3.45 · 3.06 · 2.59 · 1.77 ↔ 판독 3.98 · 3.45 · 3.11 · 2.57–2.67 · 1.83) · 그림 6b h/R 0.30 정수압 (식 10 + 식 3 · ρ₀ = π/6): 2.25 · 1.81 · 1.42 · 0.98 · 0.46 ↔ 판독 2.28 · 1.87 · 1.42 · 1.03 · 0.50 [카드 산술 · 판독] |
| SC 세 하중 (그림 7 · 납) | 캡션: *"Eq. (10) shows good agreement with MDEM curves in the three cases, whereas Eq. (14) (Storåkers' model) gives the same result for all loading types."* | die: 식 (10) 선 ≈ 2.17–2.22 (h/R 0.7) · 2.99–3.08 (0.8) ↔ MDEM ≈ 2.55–2.61 · 3.55 → **≈ 0.85 배** · 단순 압축 h/R 1.0: 식 (10) ≈ 2.97 ↔ MDEM ≈ 3.23 [판독] |
| BCC 국소 정수압 (그림 8) | *"encouraging … can fit other packings with some success"* · 2 차 접촉 힘 = 0 (판정 7 → ρ > 1 에서야 생김) | 1 차 접촉 ρ 0.95: 식 (10) 1.33 ↔ MDEM 1.16 (**+14 %**) · MDEM 2 차 접촉 힘은 **ρ ≈ 0.93** 부터 0 을 넘는다 (0.06 → 0.155 @ 0.95) [판독] |
| BCC 전체 힘 (그림 10) | *"the difference between the global force calculated with the MDEM and the one calculated analytically using (10) is quite small"* · 새 접촉 → 곡률 변화 (화살표) | 정수압: 식 (10) / MDEM = **1.12 (ρ 0.85) · 1.19 (0.90)** → 0.95 에서 겹침 · die 축 힘 = 겹침 · die **옆 힘 1.19 (0.90) · 1.23 (0.95)** · 새 접촉 동그라미 ≈ 0.93 (정수압) · ≈ 0.77–0.79 · ≈ 0.97–0.98 (die) [판독] |
| 무작위 단일 구 (그림 11) | 처음 12 접촉: MDEM 산포 작음 · 식 (10) 가까움 · 2 차 2 접촉: *"0.87 and 0.91 instead of 0.8 and 0.83 for the MDEM"* | 처음 ρ ≈ 0.675 · ρ 0.90: 식 (10) 0.94 ↔ MDEM 0.71–1.08 · 0.95: ≈ 1.41 ↔ 1.19–1.58 · 2 차 접촉 ρ 0.95: 식 (10) 0.35 · 0.17 ↔ MDEM 1.02 · 0.88 (**0.34 · 0.20 배**) [판독] |
| 무작위 15 입자 (그림 12) | ρ < 0.85 에서 셋이 잘 맞고 그 뒤 Storåkers 가 갈라진다 · *"Equation (10) together with the classical contact criterion (7) can bring accurate results about the global forces on the walls"* | 처음 ρ ≈ **0.44** · ρ 0.60: Storåkers 3.76 · MDEM 3.14 · 식 (10) 2.09 · 0.70: 6.19 · 5.52 · 3.93 · 0.75: 7.19 · 6.77 · 5.23 · 0.825: 8.49 · 9.03 · 7.99 · 0.90: Storåkers 9.87 · MDEM ≈ 식 (10) ≈ 12.9–13.8 · 0.95: 10.70 · ≈ 21.4 · 그림 12b 두 법칙이 **h_av/R ≈ 0.19–0.20** 에서 엇갈림 [판독] |

### 3d. ★ 판독이 본문 서술과 다른 곳 (래스터 화소 · 눈금 보정 · digitized.csv)

1. **그림 12a 중간 밀도 (ρ 0.55–0.80)**: 식 (10) 이 MDEM 보다 **낮다** — 비 0.66 (0.55) · 0.67 (0.60) · 0.69 (0.65) · 0.71 (0.70) · 0.77 (0.75) · 0.85 (0.80) [판독 · 카드 산술] · Storåkers 는 MDEM 보다 **높다** (1.24 · 1.20 · 1.19 · 1.12 · 1.06 → 0.8 근처에서 엇갈림) — 본문 *"good agreement … when the relative density is less than 0.85"* 는 이 폭 (−34 – +24 %) 을 '맞음' 으로 부른 것이다.  ρ ≥ 0.85 에서는 식 (10) 이 MDEM 과 1 단위 안 · Storåkers 는 0.90 에서 MDEM 의 ≈ 0.74 배 · 0.95 에서 ≈ 0.5 배.
2. **그림 7 Storåkers 점선 ↔ 단순 압축**: 점선 = 식 (14) (R₀ = R/2 · n₂ 0.24 → F/(K₂R²) = **7.05 (h/R)^1.12** [카드 산술]) 이 판독과 2–3 % 안에서 맞는다 (0.431 · 0.647 · 0.853 · 3.980 @ h/R 0.08 · 0.12 · 0.15 · 0.60 ↔ 계산 0.417 · 0.656 · 0.842 · 3.979).  그런데 세 하중 MDEM (+ 식 (10)) 다발은 h/R 0.10 에서 **0.382**, 0.15 에서 **0.559** [판독] → 점선 (0.10 = 식 (14) 값 0.535 · 0.15 = 판독 0.853) 이 **1.40 · 1.53 배**.  식 (12) 적분 (단순 압축 · n₂ 0.24) 으로도 0.417 · 0.557 → Storåkers / 식 (12) = **1.28 (0.10) · 1.51 (0.15) · 2.24 (0.35) · 2.52 (0.50)** [카드 산술].  ⇒ *"fits the simple compression curve up to an h/R of about 0.15"* 는 0–5 축에서 차가 0.15–0.29 라 작아 보인 것 · **같은 h/R 에서 Storåkers 가 단순 압축을 넘기 시작하는 곳은 h/R ≈ 0.05–0.06** (점선 · 다발이 한 화소 줄로 붙어 있는 마지막 점) [판독].  같은 문장의 *"and the hydrostatic compaction of the simple cubic structure up to h/R = 0.35"* 도 같은 꼴이다: Storåkers / (식 (10) + 식 (3) 정수압 적분 · 그림 6b 판독 재현) = **1.43 (h/R 0.15) · 1.52 (0.20) · 1.48 (0.25) · 1.29 (0.30) · 1.00 (0.34) · 0.90 (0.35)** [카드 산술] — 두 곡선이 h/R ≈ 0.34 에서 **엇갈리는** 것이지 0.35 까지 붙어 있는 것이 아니다.
3. **그림 7 die**: 식 (10) 선이 MDEM 의 ≈ 0.85 배 (h/R 0.7–0.8) [판독] — 캡션은 세 하중 모두 *"good agreement"*.  ⚠ 이 카드가 인쇄된 식 (10) + 식 (4) + ρ₀ = π/6 으로 적분하면 **2.58 (0.7) · 3.78 (0.8)** — 그림의 MDEM 점에 더 가깝고 그림의 식 (10) 선과 다르다 · ρ₀ 을 0.60 으로 두면 die 선 (2.13 · 2.97) 은 맞지만 그때 그림 6b 의 정수압 (1.42 @ 0.30) 이 1.13 으로 어긋난다 → 그림 7 die 선의 계산 세부 (ρ₀ · ρ 정의) [미확인].
4. **그림 7 단순 압축 h/R 1.0**: 식 (10) 선 ≈ 2.97 [판독] ↔ 식 (12) 적분 3.175 · 그림 6a 의 같은 n₂ 선 ≈ 3.1 — ≈ 6 % 낮다 · 원인 [미확인].
5. **그림 5 세로값**: 같은 h/R 의 그림 3 · 6b 정수압 (n₂ 0.24) 의 **≈ 1/3.6 – 1/5** (0.18–0.20 @ 0.20 · 0.38–0.41 @ 0.30 · 0.61–0.68 @ 0.35 ↔ 0.77 · 1.42 · 2.41) [판독 · 카드 산술] · 그림 5 의 하중 경로 · n₂ · 힘 정의는 캡션에 없다 — 1/8 모델 면의 힘 (접촉의 1/4) 이면 비 4 가 되지만 [카드 추론 · 확인 불가] 근거 없음 [미확인].  ★ 그림 5 의 결론 (R 1 ↔ 100 mm · K₂ 1 ↔ 100 MPa 곡선이 겹침) 은 이와 무관하게 선다.

### 3e. 카드 산술 — 검산 · 환산 (표지 [카드 산술] · 식은 이 카드가 크롭에서 다시 읽은 식)

| 항목 | 계산 | 값 |
|---|---|---|
| 처음 상대밀도 | SC π/6 · BCC π√3/8 | **0.524 · 0.680** (그림 10 의 곡선 시작 0.68 [판독] 과 맞음) |
| 강체 구 판정의 BCC 2 차 접촉 | 둘째 이웃 (거리 a) 이 2R 이 될 때 — 정수압 ρ = 2·(4/3)πR³/(2R)³ = π/3 · die (축만 줄임 · 옆 a 고정) ρ = π/4 | **1.047 (정수압 — 원문 '> 1')** · **0.785 (die — 원문 '일찍 생긴다 · 판정 7 이 충분히 맞다')** |
| 같은 숫자의 이웃 카드 | `gonzalez2012` §3.4 의 *"Hertz ρ_R = 1.04 (정수압) · 0.786 (die)"* | = π/3 · π/4 (Hertz 접촉 판정 = 순수 기하 · 법칙 무관) |
| S₁ 계수 (n₂ 0.24) | α₁ 0.8308 · β₁ 1.96 · γ₁ 4.7209 · δ₁ 8 · α₂ 13.2 | h = 0 의 강성 S/(K₂R) = α₁ + γ₁ = **5.55** (n₂ 0: 11.97 · n₂ 1: 0.14) · γ₁ 은 n₂ > 11/12 (≈ 0.917) 에서 음수 · S₁ 최소 h/R = ln(γ₁δ₁/α₁β₁)/(β₁+δ₁) ≈ **0.32** (본문 '처음엔 강성이 줄다가 늘어난다') |
| 식 (12) 적분 (단순 압축) | F/(K₂R²) = (α₁/β₁)(e^(β₁x) − 1) + (γ₁/δ₁)(1 − e^(−δ₁x)) | n₂ 0.24: 0.417 (0.10) · 0.557 (0.15) · 1.285 (0.50) · 3.175 (1.0) |
| SC 정수압 압력 (모형 지표 · 인용 금지) | 식 (10) + 식 (3) 적분 · P = F/(2R − h)² · 납 K₂ 20.5 MPa | h/R 0.15 · ρ **0.662** → P/K₂ 0.17 (3.5 MPa) · h/R 0.30 · **0.853** → 0.49 (10.1 MPa) · h/R 0.35 · **0.933** → 0.89 (18.2 MPa) · h/R 0.37 · **0.967** → 1.30 (26.7 MPa) · h/R 0.38 · **0.985** → 1.78 (36.6 MPa) (ρ → 1 근처라 h/R 둘째 자리에 민감) |
| SC die 축 압력 (모형 지표 · 인용 금지) | P = F/(2R)² | h/R 0.5 · ρ 0.698 → 7.4 MPa · h/R 0.7 · 0.806 → 13.2 · h/R 0.8 · 0.873 → 19.3 · h/R 0.9 · 0.952 → 34.4 MPa |
| 이 카드의 우리 쪽 환산 | 순수 SE ⟨δ⟩/d ≈ 0.11 (CLAUDE.md · 18 배 연화 DEM) → δ/R = 2 × 0.11 | **0.22** (= 이 논문 무작위 15 입자 ρ 0.85 의 h_av/R 0.22 (식 10) · SC 정수압 독립 범위 0.15 의 1.5 배) — 판정 아님 · 재료 · 법칙이 다르다 |
| E/σ_Y 비 | 납 MDEM 10,000/5 · 우리 MPM 1.53/0.30 · 우리 DEM E_eff 1.35 / Heckel σ_y,eff 0.046 GPa | **2000 · 5.1 · 29** — 이 논문이 탄성을 버린 근거 (E ≫ σ_Y) 는 우리 무르게 맞춘 MPM · DEM 매개변수에는 서지 않는다 |

### 3f. 원문 안의 어긋남 · 미정의 (원문 비판 — §11 에 다시)

1. 그림 6 의 n₂ 목록: 본문 *"n2 = 0, 0.1, 0.24, 0.5 and 0.8"* (p.3360) ↔ 캡션 · 그림 *"n2 = 0, 0.1, 0.24, 0.5, 1"* (p.3361 · 화살표 끝 'n₂=1').  이 카드의 식 (12) 적분이 n₂ = 1 로 그림 6a 의 맨 아래 선 (1.83 [판독] ↔ 1.77) 과 맞는다 → **그림은 1** 로 읽힌다 [카드 추론].
2. 본문의 일치 서술 ↔ 판독 (§3d 1–4).
3. 그림 5 의 세로 크기 ↔ 그림 3 · 6b (§3d 5).
4. ρ₀ (*"the average relative density when the contact is identified"*) 의 실제 값 · 단순 압축에서 ρ = 0 (*"the volume of the Voronoï cell is infinity"*) 일 때 S₂ 처리 · 무작위 근사의 처음 셀 · 15 입자 처음 충전 (≈ 0.44 [판독]) 의 생성법 [미확인].
5. 그림 4 캡션 *"Vorono cell"* (ï 빠짐 · 본문은 *"Voronoï"*) [인쇄 그대로].
6. 텍스트 층: 식의 그리스 문자가 라틴 글자로 바뀐다 (*"a1; b1;c1; d1;a2"* = α₁ β₁ γ₁ δ₁ α₂ · *"c2"* = c²) — 원문 오류 아님 · 인용 · 검색 때 주의.

---

## 4. ★ 방법 — 식 수준으로 (크롭 `eq_01` … `eq_14` · [인쇄 — 크롭 이미지에서 다시 읽음])

### 4a. 두 재료 법칙 — MDEM 과 DEM 이 **다른 재료**를 쓴다 (식 1 · 2)

```
(1)  σ = σ_Y + K₁ ε_pl^{n₁}          ← MDEM (ABAQUS) · Von Mises · 등방 경화 · + 선형 등방 탄성 (E 10 GPa · ν 0.435)
(2)  σ = K₂ ε^{n₂}                    ← DEM 접촉 법칙의 바탕 (Storåkers 1997 처럼) · 탄성 없음
     납: K₂ 20.5 MPa · n₂ 0.24  ↔  σ_Y 5 MPa · K₁ 15.5 MPa · n₁ 0.35   ("adjusting the values … a similar loading curve")
```
- *"In the following, the material behavior will be entirely determined by constants K2 and n2."* (p.3358)
- ⇒ **DEM 쪽 '탄소성' 은 강소성** (σ_Y · E 가 DEM 법칙에 없다).  그림 5 캡션: K₂ 1 ↔ 100 MPa 곡선의 작은 차 = 같은 E · ν 로 σ_Y · 항복 변형률이 달라진 *"elastic compressibility"* · *"neglected in the present work"*.

### 4b. 상대밀도 — 격자 공식과 DEM 의 Voronoï (식 3 · 4 · 5)

```
(3)  ρ = (4/3 π R³) / (2R − h)³                정수압 · SC 셀
(4)  ρ = (4/3 π R³) / ((2R − h)(2R)²)          die · SC 셀
(5)  ρ_ij = (ρ_i + ρ_j) / 2                    두 입자 상대밀도의 산술 평균
```
- SC: *"the ratio between the volume of the sphere (assumed to be constant) and the volume of the polyhedral cell formed by the rigid compressing planes"* (p.3359).
- DEM: *"If, for each contact, a contact plane is defined, as represented in the MDEM models by rigid planes, each sphere is then isolated in a polyhedron the volume of which can be calculated (Fig. 4a). The ratio of the sphere's volume (constant) and the Voronoï cell's volume (variable) gives the relative density ρ for each sphere in a random packing."* (`txt_p03_voronoi_cell_relative_density_per_sphere`) · 근거 문헌 Gellatly & Finney 1982a · b (*"the radical alternative to the voronoï polyhedron"* — 원문 참고문헌 제목).
- 쌍 평균의 이유: *"the contact force tends to infinity when the density of both particles reaches one"* (p.3359).
- ⚠ 구 부피를 **상수**로 둔다 (겹친 부분을 빼지 않음) — 셀이 구보다 작아지면 ρ > 1 이 가능하다 → 식 (13) 의 1/(1−ρ) 가 그 앞에서 발산해 막는다 [카드 추론].

### 4c. 힘 갱신 — 두 극한과 보간 (식 6 · 7 · 8)

```
If h_ij ≥ 0:   F_ij(t + Δt) = F_ij(t) + S_ij(h_ij, ρ_ij) · Δh_ij(t + Δt)      (6)   증분 (접선 강성)
If h_ij < 0:   F_ij(h_ij, ρ_ij) = 0                                           (7)   고전 DEM 접촉 판정 (처음 반지름)
               S_ij = S₁(h_ij) + S₂(ρ_ij)                                      (8)
```
- 두 극한: *"In the first part of compaction, the contacts are independent and the contact force depends only on h; then at the end, when ρ tends to 1, plastic incompressibility prevails and the contact force essentially depends on ρ."* · 중간 = *"an interpolation between the two limiting cases"* (p.3360 · `txt_p04_two_limit_cases_h_then_rho_interpolation`).
- h_ij (겹침) ≡ MDEM 의 압입 깊이 h (그림 3 · 4b) — 두 구 중심 거리가 2R − h.
- 결합: *"Each single contact involving a sphere i modifies its relative density ρi, and this modification affects all the contacts of the sphere i."* (`txt_p04_s1_s2_impingement_all_contacts_criterion7`).
- ⚠ 식 (6) 은 증분형이라 Δh < 0 (제하) 이면 같은 S 로 힘이 줄어든다 — 이력 · 잔류 겹침 · 제하 강성은 **정의되지 않았다** [카드 추론 · 원문 서술 없음].

### 4d. 스케일 가정 (식 9 · 그림 5)

`F/(K₂R²) (h_ij/R, ρ_ij)` 가 K₂ · R 에 무관 — MDEM 이 확인 (그림 5: R 1 ↔ 100 mm 겹침 · K₂ 1 ↔ 100 MPa 거의 겹침) · 뜻: 같은 h/R 이면 접촉면 응력 분포가 같다 · F ∝ 접촉면 ∝ R² · 응력 ∝ K₂ (식 2) (`txt_p04_scaled_form_independent_k2_r`).  ⇒ **크기 효과 없음** (길이 척도 없는 법칙) — 우리 frame[5] 의 '크기 효과 = 충전 몫' 과 같은 방향 [카드 추론].

### 4e. ★ 맞춘 법칙 (식 10–13) + 계수 (식 11) — 맞춘 값 감사

```
(10)  S_ij = K₂R [ α₁(n₂) e^{β₁(n₂) h_ij/R} + γ₁(n₂) e^{−δ₁ h_ij/R} + α₂(n₂) [max(0, ρ_ij − ρ₀_ij)]² / (1 − ρ_ij) ]
(11)  α₁(n₂) = 0.97 − 0.58 n₂ ;  β₁(n₂) = 1.75 (1 + n₂/2) ;  γ₁(n₂) = 15/(1 + 3n₂) − 4 ;  δ₁ = 8 ;  α₂(n₂) = 15 (1 − n₂/2)
(12)  S₁ = K₂R [ α₁ e^{β₁ h_ij/R} + γ₁ e^{−δ₁ h_ij/R} ]                    고립 접촉 (단순 압축 곡선)
(13)  S₂ = K₂R [ α₂ (max(0, ρ_ij − ρ₀_ij))² / (1 − ρ_ij) ]                  소성 비압축 · ρ_ij < ρ₀ 이면 0 · ρ_ij → 1 이면 ∞
```
- *"where α1, β1, γ1, δ1, α2 are constants or functions of n2. ρ0ij is the average relative density when the contact is identified."* (`txt_p04_a1_b1_c1_d1_a2_functions_of_n2_rho0`).
- *"In any case, the proposed form of Eq. (10) is just the result of the fitting procedure. Here the choice has been made to take into account extreme values of n2 and a range of h/R from 0 to 1. In particular, the form of the S2 term could be much more simplified by restraining the values of n2 or h/R."* (`txt_p05_eq10_just_fitting_extreme_n2_hR_0_1`)
- S₂ 를 작게 두는 이유: *"For small values of ρij − ρ0ij, S2 remains small to ensure that it remains negligible compared to S1 in the first stage of compaction."* (p.3361)

| 기호 | 식 (11) | n₂ 0.24 (납) [카드 산술] | 뜻 | 맞춘 대상 |
|---|---|---|---|---|
| α₁ | 0.97 − 0.58n₂ (숫자 2) | 0.831 | 늘어나는 지수 항의 크기 | SC MDEM 단순 압축 (그림 6a) |
| β₁ | 1.75 (1 + n₂/2) (숫자 2: 1.75 · ½) | 1.96 | 큰 h/R 에서 강성이 오르는 빠르기 | 같음 |
| γ₁ | 15/(1 + 3n₂) − 4 (숫자 3) | 4.72 | 처음 강성의 대부분 (n₂ 작을수록 큼) | 같음 |
| δ₁ | 8 (숫자 1) | 8 | 처음 강성이 줄어드는 빠르기 | 같음 |
| α₂ | 15 (1 − n₂/2) (숫자 2: 15 · ½) | 13.2 | 소성 비압축 항의 크기 | SC MDEM 정수압 (· die) (그림 6b · 7) [어느 하중을 썼는지 미확인] |
| ρ₀_ij | (상태 변수) | SC 접촉이 처음 생길 때 = π/6 = 0.524 [카드 추론] | S₂ 가 켜지는 기준 밀도 | 맞춘 값 아님 |
| K₂ · n₂ · R | 재료 · 기하 입력 | 20.5 MPa · 0.24 · 5 mm | 식 (2) 의 재료 상수 | 재료 응력–변형 곡선 (납 · 출처 표기 없음) |

⇒ **맞춘 값 = 계수 함수 5 개 · 인쇄 숫자 10 개 + 함수 꼴 (지수 둘 · (ρ−ρ₀)²/(1−ρ))** · 맞춘 기준 = **FE (MDEM) 단일 구 격자 곡선 · 실험 아님**.  이웃 카드의 같은 축과 나란히: Gonzalez 2012 = 0 (닫힌형) · Brodu 2015 = γ 1 개 · Giannis 2021 = β 1 개 (그 카드들 기록) · Storåkers 1997 = c² 함수 (숫자 2) · 이 논문 = 10.

### 4f. Storåkers 법칙 (식 14 · 비교용)

```
(14)  F_ij = 2^{1 − 3n₂/2} 3^{1 − n₂} π c^{2+n₂} K₂ R₀^{1 − n₂/2} h_ij^{1 + n₂/2} ,   1/R₀ = 1/R_i + 1/R_j ,   c² = 1.43 e^{−0.97 n₂}
```
- h 만의 함수 → *"gives the same results in every case as it only depends on h"* (p.3361).
- 같은 크기 구 (R₀ = R/2) · n₂ 0.24: **F/(K₂R²) = 7.05 (h/R)^1.12** [카드 산술] — 그림 7 의 점선과 2–3 % 안 (§3d 2).
- 큰 변위에서 단순 압축을 넘는 이유: *"a consequence of the assumption of small strain kinematics initially used by Storåkers et al. (1997)"* (`txt_p05_storakers_overestimates_simple_compression_small_strain`).

### 4g. 검증 설정 — SC → BCC → 무작위 → 15 입자 (그림 1)

- **1 차 (BCC · 국소)**: 구 하나를 강체 면 **14 장** (BCC 이웃) 으로 정수압 — *"A hydrostatic compaction has been chosen to simplify the simulation by avoiding rotations of the rigid planes which would be necessary to represent the sliding of the diagonal contacts."* (`txt_p05_bcc_14_planes_second_contact_zero_rho_gt1`).
- **1 차 (BCC · 전체)**: 주기 셀 벽의 합력 (정수압 · die 의 축 · 옆) 을 식 (10) 에서 기하로 해석 계산 ↔ MDEM (그림 10).
- **2 차 (무작위 · 국소)**: 구 하나 + 무작위 면 (14 접촉) · 면은 회전 없이 이동 · 이동량 ∝ 처음 거리 · 변형된 구의 '중심' = 힘 평형으로 정의 · *"without any rearrangement"* · ρ_ij = ρ_i (`txt_p06_random_planes_no_rearrangement_same_rho_monodisperse`).
- **2 차 (무작위 · 전체)**: 15 입자 (R 0.19 mm) 정수압 · 마찰 없음 · MDEM (ABAQUS) ↔ DEM (YADE · 식 10 / 식 14).  처음 충전 생성법 [미확인].

### 4h. 계산 규모 · 비용

| 항목 | 값 | 표지 |
|---|---|---|
| MDEM 한계 | *"limited to assemblies of about a hundred particles"* (p.3358) · *"it still requires a really long calculation time compared to the DEM"* (결론) | [인쇄] |
| 곡선 맞춤 모형 | 1/8 구 · 2 차 사면체 1200 요소 (SC · *"simple and cheap (in terms of CPU time)"*) | [인쇄] |
| 15 입자 MDEM | 온 구 2600 요소 × 15 ≈ **39,000** 2 차 요소 | [카드 산술] (15 입자에 온 구 메시를 썼다는 직접 문장은 없음 — '여러 입자' 용이라고만) |
| DEM | YADE · 15 입자 · Voronoï 국소 상대밀도를 매 단계 계산 · Δt · 단계 수 · 시간 [미확인] | — |
| 벽시계 · CPU | 숫자 없음 | [미확인] |

### 4i. 입자 처리 (우리 '무질서 처리' 칸)

- **단분산** (같은 R) · **마찰 없음** · 점착 없음 · 구 (DEM) ↔ FE 메시 구 (MDEM — 모양이 실제로 바뀐다: 그림 3 · 8c · 10 · 11 · 12 의 다면체 모양).
- 무작위 근사에 **재배열 없음** (면이 정해진 방향으로만 이동) — 실제 분말의 재배열 · 마찰은 앞으로 (*"tangential and cohesive behavior … adjusted to fit the behavior of a real powder which is composed of irregular grains and lubricants"*).
- 다분산이면 ρ_ij = ρ_i 근사 (이웃 밀도 차 작음) 가 깨질 수 있다고 저자가 한정 (*"In the case of a monodisperse packing, this consideration appears to be reasonable"*).

### 4j. ★ 네 항목 — DEM 한계 · 소성이 어려운 이유와 우회 · 2D/3D · 탈압

**(i) DEM (단단한 구 · 점접촉) 의 한계 — 원문 문장**
- p.3357 (서론): *"Nevertheless, those approaches are limited in relative density, because this type of model is based on the assumption that the contacts between the particles can be considered as independent. In other words, each contact reacts as if it was isolated, the contact zones being far enough from each other that they do not interact. For a relative density higher than about 0.8, the mutual influence of the contacts cannot be neglected (Mesarovic and Fleck, 2000; Martin et al., 2003). Moreover, Storåkers' model has been formulated for small strain kinematics (Storåkers et al., 1997), and this assumption may be considered as critical for high densities."* (`txt_p01_independent_contacts_limit_0p8_small_strain`)
- p.3358–3359 (§3.2): *"Fig. 3 clearly shows that the force developed at the contact between two spheres for different loading types cannot depend only on the relative displacement h, except at the beginning of compaction when the contacts are independent."* (`txt_p03_force_not_h_only_incompressibility_rho_to_1`)
- p.3361 (§4): *"However, it should be observed that the DEM model predicts that the force is zero for the second contact. This can be explained by the contact criterion (7) which neglects the sphere's deformation. The spheres' deformation creates a material flow in the directions which remain free, and a contact can be created between two particles even though criterion (7) is not respected (the distance between the centers is more than the sum of the radii). … In the case presented in Fig. 8, criterion (7) predicts that the second contacts appear for a relative density greater than one."* · *"Thus the secondary contacts are quite badly reproduced by the DEM model."*
- p.3363: *"criterion (7) generates an important delay in the contact identification. The new contacts appear at a relative density of 0.87 and 0.91 instead of 0.8 and 0.83 for the MDEM."* (`txt_p07_secondary_contacts_0p87_0p91_vs_mdem_0p8_0p83`)

**(ii) 소성 · 큰 변형을 넣기 어려운 이유와 이 논문의 우회 · 비용**
- 이유 (원문): 끝의 힘 상승 = *"plastic incompressibility of the material when free space is no longer available and relative displacement cannot take place anymore"* (p.3358–3359) → h 하나로는 못 담는다 · 입자마다 FE 는 *"accurate description of the particles' deformation and produce accurate results up to high densities. Unfortunately, because of its high computational cost, this type of simulation is limited to assemblies of about a hundred particles."* (`txt_p02_mdem_2d_3d_hundred_particles_periodic_lattice_extrapolated`) · 무작위 충전에서 접촉 상호작용을 직접 재려면 *"numerous simulations and a lot of computational time"* (p.3358).
- 우회: ① 입자 소성 → **강소성 멱법칙 (K₂ · n₂) + 접촉 강성 곡선 맞춤** (탄성 버림) ② 접촉 상호작용 · 비압축 → **입자 Voronoï 상대밀도 하나** (S₂) ③ 무작위 대신 **SC 격자 하나**에서 맞추고 옮김 ④ 2 차 접촉은 강체 판정 그대로 (지연을 받아들이고 *"at the macroscopic scale, a relatively small force"* 로 정당화).
- 맞춘 값 · 대상 · 검증 범위: §4e · §3c (정수압 위주 · 무작위 die 없음 · 실험 없음).
- 비용: §4h (MDEM 15 입자 · 숫자 없음).

**(iii) 2D / 3D**: 이 논문 = **3D** (FE 1/8 구 · 온 구 · YADE).  서론이 MDEM 의 2D 선행 (Gethin 2003 · Procopio–Zavaliangos 2005) → 3D (Chen 2006 · Frenning 2008 · Chen 2008) 를 적을 뿐 · 2D → 3D 전이 서술 없음.

**(iv) 압력을 뺄 때**: **다루지 않았다** — 재하만 · 제하 가지 · 잔류 겹침 · 되돌아옴 · 판 분리 없음.  (식 (6) 의 증분형은 제하를 정의하지 않는다 [카드 추론].)

---

## 5. 결과 — 그림별 (전부 크롭해 봄)

### 5.1 Fig. 1 — 방법 흐름도
SC 격자 MDEM (단순 · die · 정수압) → 매개변수 고르기 · DEM 해석식 → 1 차 검증 BCC (die · 정수압) → 2 차 검증 무작위 (정수압).

### 5.2 Fig. 2 — (a) 정수압 SC 의 기하 단순화 (격자 → 셀 → 1/8 구 + 대칭면 · 강체 면 RP) (b) 메시 (1/8 구 · 온 구 · 사면체)
### 5.3 Fig. 3 — SC 세 하중의 F/(K₂R²) 대 h/R + 변형 모양 셋
정수압 곡선은 h/R ≈ 0.38 에서 F/(K₂R²) ≈ 4.75–5 로 치솟음 · die 는 h/R ≈ 0.88 에서 5 · 단순 압축은 h/R 1 에서 ≈ 3.2 [판독 · 눈] · 동그라미 (h/R ≈ 0.08 · 0.28 · 0.38) 에 변형 모양 (구 → 다면체) [판독 · 눈] · 왼쪽 그림 = h 의 정의 (위 판이 h 만큼 내려옴).
### 5.4 Fig. 4 — (a) Voronoï 셀 2D 그림 (접촉면이 셀을 만든다) (b) DEM 기호 (F_ij · h_ij · R)
### 5.5 Fig. 5 — 스케일 가정 (R · K₂ 영향) → §4d · §3d 5
### 5.6 Fig. 6 — 식 (10) ↔ MDEM (a) 단순 압축 (b) SC 정수압 · n₂ 다섯 → §3c (이 카드의 적분 검산)
### 5.7 Fig. 7 — 납 SC 세 하중 · 식 (10) · 식 (14) → §3d 2–4
### 5.8 Fig. 8 — BCC 국소 정수압: (a) 면 14 장 (b) 1 차 · 2 차 접촉 힘 (c) 접촉 모양 → §3c (2 차 접촉 MDEM ρ ≈ 0.93 부터 · 식 (10) 은 0)
### 5.9 Fig. 9 — 옆으로 흐른 재료가 접촉을 앞당긴다 (강체 판정이 못 보는 것)
### 5.10 Fig. 10 — BCC 셀 전체 힘 (a) 정수압 (b) die 축 · 옆 → §3c
### 5.11 Fig. 11 — 무작위 근사 (a) 처음 12 접촉 (b) 2 차 2 접촉 → §3c · 2 차 접촉 시작 0.80 · 0.83 (MDEM) ↔ 0.87 · 0.91 (식 10) [인쇄 · 판독 일치]
### 5.12 Fig. 12 — 15 입자 정수압 (a) 힘 대 ρ (b) DEM 힘 대 h_av/R → §3c · §3d 1

### 5.13 결론 (p.3363–3364, 요지)
MDEM 은 정확하나 오래 걸린다 · MDEM 에서 뽑은 해석식을 DEM 에 다시 씀 · 주기 격자 접근이 매개변수 분석을 싸게 해 준다 · **국소 상대밀도** 가 DEM 에서 소성 비압축 · 고밀도 효과를 낸다 · 2 차 접촉 판정 때문의 어긋남이 있으나 *"encouraging"* · **탄성 없는 단순 재료** 가정은 식 (10) 에는 영향이 있으나 접근법에는 아니다 · 앞으로: 탄성 · 다분산 · 다른 재료 · 접선 · 점착 (뒤 둘은 실제 분말에 맞춤) (`txt_p08_no_elasticity_future_polydisperse_tangential_cohesive`).

---

## 6. 우선 질문 — 원문 대조

### e. 점접촉 법칙 · 대안 · 맞춘 값 수
§0 ① ② · §3b · §4e.  고전 법칙 = Storåkers (강소성 · 독립 접촉 · 작은 변형) · 대안 = 식 (10) (FE 맞춤 · 국소 상대밀도) · 맞춘 값 = 함수 5 / 숫자 10 · 이 논문은 Thornton–Ning · MDR · EEPA · Hertz 를 다루지 않는다 (Hertz 는 서론에서 비선형 탄성용으로만 언급 · Vu-Quoc 2001 = 작은 소성 변형용으로만 언급).

### k · l · g · b → §4j.

### d. 단단한 입자의 하중 몫 · 재밍
없음 (한 재료 · 단분산).  대리 정보: BCC die 에서 식 (10) 이 옆 힘을 1.19–1.23 배 크게 (ρ 0.90–0.95 · 축 힘은 맞음) [판독] — 하중 방향 분배를 S₂ 가 등방으로 다루기 때문일 수 있다 [카드 추론].

### a · i. 기공
없음 — 납 단분산 · 힘만 · 압력 없음.  SC 정수압 · die 의 압력 환산은 §3e (모형 지표 · 인용 금지).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 가지에서는 값 자리표시 상태 — 우리 수치는 지시서 · CLAUDE.md 출처를 병기해 적는다)

### 7a. 비교표

| 항목 | 이 논문 | 우리 DEM (LIGGGHTS) | 우리 MPM |
|---|---|---|---|
| 접촉 법칙 | 증분 S = S₁(h) + S₂(ρ) · 강소성 · 맞춘 계수 5 | hooke/hysteresis (탄성–이력) · pairwise (접촉끼리 독립) | 접촉 법칙 없음 (연속체 · 한 속도장) |
| 강성 크기의 손잡이 | K₂ (소성 경화 상수) · E 는 법칙에 없음 | **E_eff 1.35 GPa (SE · 24 GPa 의 18 배 연화)** | E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa |
| 고밀도 발산 | **1/(1 − ρ) 로 ρ → 1 에서 무한대** (Voronoï 국소) | 없음 (겹침이 선형으로 늘 뿐 — 순수 SE 에서 ε_sphere 가 음수까지) | 부피 보존 소성 흐름 + K 25.5 GPa (ν 0.49) 가 구멍이 닫히면 버팀 |
| 2 차 접촉 | 강체 판정 (7) — 늦게 잡음 (Δρ ≈ 0.07–0.08) | 같은 판정 (δ > 0) | 입자 경계 없음 (접촉면 용접) |
| 탄성 · 제하 | 없음 | 있음 (이력) | 있음 (J2 탄소성) |
| 재료 | 납 (강소성 K₂ 20.5 MPa · n₂ 0.24) | LPSCl + NCM | LPSCl (SE) + 고정 AM 골격 |
| 크기 | 단분산 구 R 5 mm · 0.19 mm · 15 입자 | 다분산 · 수만 입자 | 격자 n_grid 192–512 |
| 마찰 | 없음 | 있음 | 판 · 벽 |
| 차원 | 3D | 3D | 2D · 3D |

### 7b. ★ 랩 기준과 나란히 (판정 없이 · **랩 표준과 다른 문헌 값 = 다른 재료 · 다른 상태**)
- 랩 표준: 순수 SE 기공률 10–13 % → 상대밀도 **0.87–0.90** · LPSCl 진밀도 1.64 g/cm³ (고정 · 판정하지 않는다).
- 이 논문의 밀도 표지 (납 모형 · 누른 채 · 마찰 없음): 고전 독립 접촉 한계 **≈ 0.8** (문헌) · 무작위 15 입자 Storåkers 갈라짐 **0.85** · 새 법칙 범위 **≈ 0.95** · 무작위 2 차 접촉 시작 0.80 · 0.83 (MDEM) · SC 독립 범위 끝 0.66 (정수압) · 0.64 (die) [카드 산술].
- ⇒ 랩 표준 밀도대 (0.87–0.90) 는 이 논문에서 '독립 접촉이 깨진 뒤 · 새 법칙의 범위 안' 에 놓인다 — **재료 · 상태 · 처음 충전이 달라 같은 축의 비교가 아니다** (나란히 놓기만).

### 7c. ★ 18 배 연화와 견줄 자리 (frame [2])
- 우리 DEM 은 E 를 18 배 낮춰 (24 → 1.35 GPa) **겹침으로** 소성 압밀을 흉내 낸다 · 이 논문은 E 를 법칙에서 **빼고** (강소성) 경화 상수 K₂ 와 **상대밀도 발산 항**으로 고밀도를 담는다 — 같은 문제 (점접촉 DEM 이 고밀도 소성 압밀을 못 냄) 의 다른 우회.
- 우리 순수 SE 의 평균 겹침 ⟨δ⟩/d ≈ 0.11 → **δ/R ≈ 0.22** [카드 산술] = 이 논문 SC 정수압의 독립 접촉 범위 (h/R 0.15) 를 넘고 무작위 15 입자 ρ 0.85 의 h_av/R (0.22 · 식 10 / 0.24 · Storåkers) 와 같은 크기 — **판정 아님** (우리 δ 는 연화 탄성 겹침 · 재료 · 법칙 · 처음 충전이 다르다).
- 우리 순수 SE DEM 의 ε_sphere 음수 (구 부피 합 > 상자) 는 '국소 상대밀도 1 을 넘는 상태' 와 같은 꼴이다 — 이 논문의 S₂ 는 바로 그 상태를 막는 항 [카드 추론].
- Heckel: 우리 DEM 순수 SE P_y 138 MPa · σ_y,eff 46 MPa ↔ 이 논문 Heckel 없음 (SC 압력 환산은 모형 지표 · §3e · 인용 금지).

### 7d. frame [3] / [4] / [5]
- frame [4] (따로 실험에 맞추고 비교): 이 논문은 **DEM 법칙을 FE 에 맞춘다** (실험 없음) — 우리 규율 ('DEM ↔ MPM 을 서로 맞추지 말 것') 과 반대 방향의 설계이고, 그래서 이 법칙을 들여오면 **FE (MDEM) 를 기준으로 한 순환**이 생긴다 [카드 추론].  우리라면 FE 결과를 '결과 전 대조 항목' 으로만 쓴다.
- frame [5] (분업): MDEM 이 입자 형상 · 2 차 접촉 · 비압축을 보고 · DEM 은 그 요약 (국소 밀도) 만 받는다 — '형상 소성은 연속체 소관 · DEM 은 그 효과를 접촉 법칙에 접어 넣을 뿐' 이라는 우리 층 지도와 같은 그림.
- frame [3] (Heckel · 조성 dip): 다루지 않음.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

(우리 계획 = 단단한 AM (NCM) + 무른 SE (LPSCl) 복합 양극을 ≈ 300 MPa 로 누르고 압력을 빼는 과정을 한 모델로.  랩 기준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 · 판정하지 않는다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 재료 · 차원 · 조건 차이 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **국소 연산자 정의 예**: 입자 상대밀도 = 구 부피 (상수) / Voronoï (radical) 셀 부피 · 쌍 = 산술 평균 · 고립 구 = 0 (셀 무한대) · 처음 접촉 시 ρ₀ — 우리 기공 연산자 등록에 '전체 밀도 ↔ 입자 셀 밀도' 를 따로 적을 근거 · ★ 같은 '깨지는 밀도' 가 처음 충전에 따라 0.64–0.85 로 갈린다 (§3b) → 판정 기준에 처음 충전 · 하중 경로를 같이 적는다 | 셀 부피에서 겹침을 빼지 않아 ρ > 1 이 가능 · 납 모형 값 |
| **단계 1** (입자별 속도장 3D 메모리 · 장 수) | 규모 감각: 입자마다 FE 는 ≈ 100 입자 한계 · 15 입자 ≈ 39,000 2 차 요소 [카드 산술] · 1/8 구 1200 요소 (곡선 맞춤) | 메모리 · 시간 숫자 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (3D) · 2D MDEM 선행 (Gethin 2003 · Procopio 2005) 이름만 | — |
| **단계 3** (2D 접촉 표현만 바꿔 누르는 힘 비교) | ★ **보고 꼴**: 같은 15 입자 침대 · 같은 하중에서 **접촉 법칙만 바꿔** (Storåkers ↔ 식 10) 기준 (FE) 과 벽 힘을 비교 (그림 12) · 국소 (접촉 하나) 와 전체 (벽 합력) 를 따로 보고 (그림 8 ↔ 10) — 국소에서 틀린 2 차 접촉이 전체 힘에서는 작게 보일 수 있다는 예 | 3D · DEM ↔ FE (MPM 아님) · 정수압 위주 |
| **단계 4** (3D 순수 SE 붓고 눌러 항복 세기 하나를 실험 기공에 맞춤) | 15 입자 처음 ρ ≈ 0.44 [판독] (생성법 [미확인]) · 맞춘 값이 실험이 아니라 FE 라는 반례 — '맞추는 값은 실험 기공 하나' 원칙 (R5) 과 대비 | 순수 SE 없음 · 실험 없음 · 압력 단위 없음 |
| **단계 5** (3D 복합 AM + SE 압축) | 없음 — 단분산 한 재료 · 저자가 다분산 · 다른 재료를 앞으로의 일로 적음 · ρ_ij = ρ_i 근사는 단분산에서만 *"reasonable"* | 강성 대비 · 크기 대비 없음 |
| **단계 6** (압력 빼고 되돌아옴) | 없음 (재하만 · 식 (6) 은 제하를 정의하지 않음) | — |
| **단계 7** (눌린 구조의 형상 · 피복 · 수송) | ★ **접촉망 위상 경고**: 강체 구 판정 (δ > 0) 은 옆으로 흐른 재료가 만드는 2 차 접촉을 **Δρ ≈ 0.07–0.08 늦게** 잡는다 (0.87 · 0.91 ↔ 0.80 · 0.83) · BCC 정수압은 ρ > 1 이 되어야 (π/3 = 1.047 [카드 산술]) — 우리 접촉망 수송 (σ_ion · σ_e) 은 고밀도에서 접촉 수를 적게 셀 수 있다 (`gonzalez2012` 의 '겹침 0 접촉' 과 같은 방향) | 수송 계산 없음 · 납 |
| **후보 D0** (지금 DEM: 구 · 탄성-이력 · 무른 E) | ★ 같은 층의 외부 진단: 독립 접촉 법칙은 무작위 충전 ≈ 0.8–0.85 넘어 FE 와 갈라진다 · 고밀도 힘은 국소 밀도로 발산해야 하는데 D0 에는 그 항이 없다 (순수 SE ε_sphere 음수와 같은 꼴 [카드 추론]) · 우리 δ/R ≈ 0.22 의 자리 (§7c) | D0 는 탄성–이력 + 연화 · 이 논문은 강소성 (E 없음) |
| **후보 A′-0** (MPM 판 · 벽 · AM 자리에만 접촉 규칙) | 없음 (마찰 없는 강체 면 = 이 논문의 경계 · 면 회전을 피하려고 정수압만 — 미끄러지는 접촉은 다루지 않았다) | — |
| **후보 A** (MPM: AM 강체 + SE 한 속도장) | 없음 | — |
| **후보 A′** (MPM: 입자별 속도장 · 다물체 마찰) | 간접: 그림 9 의 '옆 흐름이 만드는 접촉' 은 입자 경계를 지키는 연속체 (A′ · B) 만 낼 수 있다 | — |
| **후보 B** (입자마다 FE + 접촉) | ★ **이 논문의 MDEM 이 B 다**: ABAQUS · 2 차 사면체 · 1/8 대칭 · 마찰 없음 · 1200 / 2600 요소 · ≈ 100 입자 한계 · 15 입자 · 그리고 **B 에서 DEM 법칙을 뽑아 내는 방법** (격자 하나에서 맞추고 옮기기) | 메시 수렴 시험 없음 · 시간 숫자 없음 · 납 |
| **후보 C** (큰 변형 접촉 DEM — MDR 류) | 앞선 경험적 형태: h/R 0–1 의 큰 겹침에 맞춘 S₁ · ρ 로 발산하는 S₂ · 그 뒤 Zunker 2024 II 가 Voronoï 판정을 자유표면적 비로 바꿈 (그 카드 L20) | 탄성 · 제하 없음 |
| **후보 C′** (항복 캡 탄소성 접촉 DEM — Thornton–Ning · 다접촉 보정) | ★ **다접촉 보정의 밀도 판**: 같은 입자의 접촉을 국소 상대밀도로 묶는다 (Giannis 의 응력 기반 · Brodu 의 변위 기반과 다른 셋째 꼴) · 맞춘 숫자 10 개 ↔ Giannis β · Brodu γ 한 개 | 항복 캡 (탄성 → 소성 전이) 없음 · 강소성 |
| **후보 M0** (균질화 압밀 — 캡 소성 · Heckel) | S₂ ∝ (ρ − ρ₀)²/(1 − ρ) = 밀도 캡 꼴 · SC 격자에서 닫힌 ρ(P) 를 낼 수 있다 (§3e 표) — M0 와 입자 법칙을 잇는 다리의 예 | 실험 압밀 곡선 없음 · SC 격자 값은 모형 지표 |
| **U0** (접촉을 끈 것과 같은지) | 없음 | — |
| **U1** (입자 하나 압축 · 해상도) | ★ **단일 구 단순 압축 기준 곡선**: 강소성 멱법칙 구를 두 강체 판 사이에 h/R 0 → 1 (그림 6a · n₂ 0 · 0.1 · 0.24 · 0.5 · 1 · 식 (12) 적분값 §3e) · Storåkers (작은 변형) 가 큰 h/R 에서 과대 (2.2–2.5 배 @ h/R 0.35–1) — 우리 MPM 단일 입자 압축 시험의 '결과 전 대조 항목' 후보 (같은 멱법칙 재료로 돌릴 때만) | 우리 MPM 재료는 J2 (σ_y 0.30 · 경화 없음) — 그대로 겹치지 않는다 · 메시 수렴 자료 없음 |
| **U2** (경사면 마찰) | 없음 (마찰 없음) | — |
| **U3** (단단한 구를 소성 블록에 눌렀다 떼기) | 없음 (제하 없음) | — |
| **U4** (판 분리) | 없음 | — |
| **U5** (비슷한 강성 입자 충돌 · 다물체) | 없음 (준정적) | — |
| **U6** (작은 조밀 충전 압축의 해상도 수렴) | ★ **격자 기준 문제**: SC (구 하나 · 6 면) · BCC (14 면) 정수압 · die — 끝 밀도가 기하로 정해짐 (SC 정수압 h/R 0.388 에서 ρ = 1 · BCC 2 차 접촉 π/3 · π/4) · 힘이 무한대로 가는 모양 (그림 6b · 8 · 10) — MPM 해상도 사다리의 해석적 끝점으로 쓸 수 있다 | 재료가 납 강소성 · 마찰 없음 |
| **R1** (AM 이 움직이고 하중을 나눠 짐) | 없음 | — |
| **R2** (미끄럼 · 분리) | 없음 (마찰 없음 · 분리 없음) | — |
| **R3** (SE 입자 경계 기억) | MDEM 은 입자마다 따로 메시 (경계 유지) — B 의 성질 · DEM 은 구 | — |
| **R4** (탈압 · 되돌아옴) | 없음 | — |
| **R5** (맞추는 값은 모델마다 하나) | ⚠ 반례: 계수 함수 5 · 숫자 10 (FE 에 맞춤) — 이 법칙을 들이면 R5 를 지키려면 FE 맞춤을 '모델의 일부' 로 고정하고 실험 맞춤 값 하나를 따로 둬야 한다 [카드 추론] | — |
| **R6** (SE 입자 형상 변형) | MDEM 에서 실제로 일어남 (그림 3 · 8c · 11 · 12 의 다면체) · DEM 법칙은 그 결과를 국소 밀도로 요약할 뿐 | — |
| **R7** (AM 파괴) | 없음 | — |
| **결과 전 대조 항목** | ① 우리 DEM 에 순수 단분산 구 대조 팔을 둔다면: 독립 접촉 법칙이 FE 와 갈라지기 시작하는 밀도 ≈ 0.8–0.85 (무작위) · 0.64–0.66 (SC) ② 강체 판정의 2 차 접촉 지연 Δρ ≈ 0.07–0.08 (무작위) · BCC 2 차 접촉 π/3 · π/4 (기하) ③ Storåkers / 단순 압축 비 1.28 (h/R 0.10) · 1.51 (0.15) [카드 산술] | 실제 LPSCl · NCM 의 기대값 아님 |

---

## 9. Figure set ★ (크롭 46 장 — `litdb/figures/harthong2009_high_density_compaction_dem_voronoi_contact_law/`)

| 그림 · 식 | 내용 | 파일 | 우리 활용 |
|---|---|---|---|
| Fig. 1 | 방법 흐름도 (SC → 법칙 → BCC → 무작위) | `fig_1.png` (다시 자름 — 캡션 넣음) | 검증 사다리 꼴 |
| Fig. 2 | (a) SC 기하 단순화 (1/8 구 · 강체 면) (b) FE 메시 | `fig_2.png` (다시 자름) | 후보 B 설정 |
| Fig. 3 | SC 세 하중 힘–h/R + 변형 모양 · h 정의 | `fig_3.png` (다시 자름) | ★ 독립 접촉 범위 h/R 0.15 / 0.35 |
| Fig. 4 | (a) Voronoï 셀 2D (b) DEM 기호 | `fig_4.png` (다시 자름) | 단계 0 연산자 |
| Fig. 5 | R · K₂ 스케일 가정 | `fig_5.png` (다시 자름) | 크기 무관 · 세로 크기 어긋남 (§3d 5) |
| Fig. 6 | 식 (10) ↔ MDEM (a) 단순 압축 (b) SC 정수압 · n₂ 다섯 | `fig_6.png` (다시 자름) | U1 기준 곡선 · 이 카드 적분 검산 |
| Fig. 7 | 납 SC 세 하중 · 식 (10) · (14) | `fig_7.png` (다시 자름) | ★ Storåkers 과대 (§3d 2) |
| Fig. 8 | BCC 국소 정수압 · 1 차 · 2 차 접촉 | `fig_8.png` (다시 자름) | ★ 2 차 접촉 힘 0 (판정 7) |
| Fig. 9 | 옆 흐름이 접촉을 앞당김 | `fig_9.png` (다시 자름) | DEM 한계 그림 (k) |
| Fig. 10 | BCC 셀 전체 힘 (정수압 · die 축 · 옆) | `fig_10.png` (다시 자름) | 국소 ↔ 전체 |
| Fig. 11 | 무작위 근사 (처음 · 2 차 접촉) | `fig_11.png` (다시 자름) | ★ 2 차 접촉 지연 |
| Fig. 12 | 15 입자 정수압 (힘 대 ρ · 대 h_av/R) | `fig_12.png` (다시 자름) | ★ 0.85 · 중간 밀도 어긋남 |
| 식 (1)–(14) | 번호마다 한 장 | `eq_01_uniaxial_elastoplastic_hardening_mdem.png` · `eq_02_rigid_plastic_power_law_dem.png` · `eq_03_relative_density_hydrostatic_sc_cell.png` · `eq_04_relative_density_die_sc_cell.png` · `eq_05_pair_mean_relative_density.png` · `eq_06_incremental_force_update_overlap_ge0.png` · `eq_07_no_contact_overlap_lt0.png` · `eq_08_stiffness_sum_s1_s2.png` · `eq_09_scaled_force_function_h_over_r_rho.png` · `eq_10_contact_stiffness_fitted_law.png` · `eq_11_fitted_coefficients_functions_of_n2.png` · `eq_12_s1_isolated_sphere_stiffness.png` · `eq_13_s2_plastic_incompressibility_stiffness.png` · `eq_14_storakers_force_overlap_law_r0_c2.png` | 보고서 DEM 절 (재료 둘 · 상대밀도 · 증분 갱신 · 맞춘 강성 · 계수 · Storåkers) |
| 근거 문단 20 | 카드가 숫자 · 정의 · 단정의 근거로 인용한 문단 | `txt_p01_…` … `txt_p08_…` (아래) | — |

근거 문단 크롭 (파일 이름의 p = PDF 쪽 · 논문 쪽 = 3356 + p): `txt_p01_abstract_dem_0p8_new_law_0p95_local_density` (초록 ★) · `txt_p01_independent_contacts_limit_0p8_small_strain` (p.3357 ★ DEM 한계) · `txt_p02_mdem_2d_3d_hundred_particles_periodic_lattice_extrapolated` (p.3357–3358 · 두 쪽 이어 붙임 ★ 100 입자 · 외삽) · `txt_p02_lead_k2_n2_sy_e_nu_r5mm_frictionless` (p.3358 · 두 단 이어 붙임) · `txt_p02_sc_eighth_sphere_abaqus_1200_2600_quadratic_tet` (p.3358) · `txt_p02_independent_contacts_until_hR_0p15_0p35_force_infinite` (p.3358 ★) · `txt_p03_force_not_h_only_incompressibility_rho_to_1` (p.3358–3359 · 두 쪽 ★) · `txt_p03_voronoi_cell_relative_density_per_sphere` (p.3359 · 두 단) · `txt_p04_two_limit_cases_h_then_rho_interpolation` (p.3360) · `txt_p04_s1_s2_impingement_all_contacts_criterion7` (p.3360 ★ 결합) · `txt_p04_scaled_form_independent_k2_r` (p.3360 · 두 단) · `txt_p04_a1_b1_c1_d1_a2_functions_of_n2_rho0` (p.3360 ★ 맞춘 값) · `txt_p05_eq10_just_fitting_extreme_n2_hR_0_1` (p.3360–3361 · 두 쪽 ★) · `txt_p05_storakers_overestimates_simple_compression_small_strain` (p.3361) · `txt_p05_bcc_14_planes_second_contact_zero_rho_gt1` (p.3361 ★) · `txt_p06_random_planes_no_rearrangement_same_rho_monodisperse` (p.3362) · `txt_p07_secondary_contacts_0p87_0p91_vs_mdem_0p8_0p83` (p.3362–3363 · 두 쪽 ★) · `txt_p07_15_spheres_r0p19mm_yade_agreement_below_0p85` (p.3363 ★) · `txt_p07_overlap_at_0p85_hmax_0p44_hav_0p24_storakers_fits` (p.3363 · 두 단 ★) · `txt_p08_no_elasticity_future_polydisperse_tangential_cohesive` (p.3363–3364 · 두 쪽 ★ 한계).

## 10. Post-processing ★
- **원문**: 접촉 힘 F/(K₂R²) 대 h/R (SC) · 대 ρ (BCC · 무작위) · 벽 합력 (BCC 셀 · 15 입자) · 평균 · 최대 겹침 h_av/R · h_max/R (15 입자 ρ 0.85) · 새 접촉 시점 (곡률 변화 화살표) · 2 차 접촉 시작 ρ.  오차 막대 · 반복 · 시드 없음.
- **이 카드**: 래스터 화소 판독 116 행 (digitized.csv) · 식 (10)–(12) 적분 검산 (그림 6a · 6b) · Storåkers 계수 (7.05 · 지수 1.12) 와 그림 7 점선 대조 · SC ρ(h/R) 환산 · SC 압력 환산 · BCC 기하 2 차 접촉 (π/3 · π/4) · 우리 δ/R 환산 · E/σ_Y 비.

## 11. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **'탄소성 DEM' 이 아니다** — DEM 법칙은 **탄성 없는 강소성** (K₂ · n₂) · 제하 없음 · 탄성은 MDEM 에만 (그리고 그 효과도 버림).
2. **실험 검증 없음** — 기준은 FE (MDEM) · 납을 고른 이유는 *"an experimental validation can be easily planned"* (계획).
3. **'잘 맞는다' 의 폭이 넓다** — 그림 12a 중간 밀도 (ρ 0.55–0.75) −23 – −34 % · 그림 7 die −15 % · BCC 옆 힘 +19 – +23 % · 2 차 접촉 0.20–0.34 배 [판독] (§3d).  본문의 문턱 숫자 (0.15 · 0.35 · 0.85) 는 눈으로 잡은 '대략' 값이다 (*"about"*).
4. **검증이 정수압 위주** — 무작위 충전 die · 전단 · 다분산 · 마찰 · 재배열 없음 · 무작위 근사 (구 하나 + 면) 는 재배열 없는 이상화.
5. **SC 하나에서 맞추고 '모든 하중' 으로 옮긴다는 주장** (p.3358) 은 BCC · 무작위 정수압에서만 확인됐다 — 다른 하중 경로의 S₂ 등방 가정 (옆 힘 과대) 은 열려 있다.
6. **Voronoï 국소 밀도의 비용 · 정의** — 셀 계산 비용 · 구 부피에서 겹침을 빼지 않는 정의 · 경계 (벽) 입자 처리 [미확인].
7. **원문 안 어긋남** (§3f): n₂ 0.8 ↔ 1 · 그림 5 세로 크기 · 그림 7 die 선 ↔ 인쇄식 적분.
8. **절대값 전이 금지** — 납 · mm 구 · 무차원 힘 · 마찰 없음.

## 12. 적용 인사이트

1. ★ **'깨지는 밀도' 는 처음 충전 · 하중 경로와 한 묶음으로 적는다** — 같은 논문 안에서 SC 0.64–0.66 ↔ 무작위 0.85 ↔ 문헌 0.8 (단계 0 · 결과 전 대조 항목).
2. ★ **강체 구 접촉 판정은 고밀도에서 접촉망을 늦게 닫는다** (Δρ ≈ 0.07–0.08) — 우리 접촉망 수송 (σ_ion · σ_e) 의 고밀도 접촉 수를 하한으로 읽을 근거 (단계 7 · 흐름 밖: 접촉망 수송 계산).
3. ★ **고밀도 힘 발산을 국소 상대밀도로 담는 꼴** — 우리 순수 SE DEM 의 ε_sphere 음수 (과압축) 가 생기는 자리를 이 항이 막는다 · 들일 때는 FE 맞춤 계수 10 개가 따라오고 (R5 충돌) 제하가 정의되지 않는다 (후보 C′ · D0).
4. **국소 ↔ 전체 를 따로 보고한다** — 접촉 하나에서 0 인 2 차 접촉 힘이 벽 합력에서는 작게 보인다 (그림 8 ↔ 10 · 단계 3 보고 꼴).
5. **Storåkers (작은 변형) 는 h/R ≳ 0.05–0.1 부터 단순 압축을 넘는다** (1.28 배 @ 0.10 [카드 산술]) — 문헌의 Storåkers 기반 DEM 결과를 고밀도에서 인용할 때 같이 적는다 (후보 C′ · e).
6. ★ **점접촉 법칙이 기준 (FE · 실험) 과 맞는 것이 두 오차의 상쇄일 수 있다** — 이 논문 저자 자신이 무작위 15 입자의 ρ 0.85 까지 일치를 '단일 접촉 과대 ↔ 비압축 · impingement 누락' 의 상쇄로 설명하고 SC 정수압에서는 두 곡선이 h/R ≈ 0.34 에서 엇갈린다 (§3d 2) — 우리 쪽 '일치 = 검증' 문장을 쓰기 전에 각 성분의 부호를 따로 본다 (단계 0 · 결과 전 대조 항목 · 후보 D0).

## 13. 인용 가능 문장 (deck/paper 용 — 표지 그대로)
- *"DEM simulations are in general limited to a relative density of about 0.8, because the existing contact laws do not reproduce all the physical phenomena involved in the densification of granular media (Harthong et al., Int. J. Solids Struct. 46 (2009) 3357)."*
- *"For a relative density higher than about 0.8, the mutual influence of the contacts cannot be neglected (Harthong et al. 2009, p. 3357, citing Mesarovic and Fleck 2000; Martin et al. 2003)."*
- *"The meshed distinct element method gives an accurate description of the particles' deformation up to high densities, but because of its high computational cost it is limited to assemblies of about a hundred particles (Harthong et al. 2009, p. 3358)."*
- *"In a rigid-sphere DEM, the contact criterion neglects particle deformation, so contacts created by lateral material flow are identified late — at relative densities of 0.87 and 0.91 instead of 0.80 and 0.83 in the finite-element reference (Harthong et al. 2009, p. 3363)."*
- 국문: *"Harthong 등 (2009) 은 접촉 강성에 입자 Voronoï 셀로 잰 국소 상대밀도 항 (ρ → 1 에서 발산) 을 더해 무작위 15 입자 정수압을 상대밀도 ≈ 0.95 까지 FE 에 맞췄다 — 계수는 단순 입방 격자 FE 에 곡선 맞춤한 다섯 함수 (숫자 10 개) 이고 재료는 탄성 없는 강소성 납이다."*
- ⛔ 인용 금지: '탄소성 DEM 접촉 법칙' (DEM 법칙은 강소성) · '격자별 특성화가 필요하다고 저자가 인정' (원문은 반대 주장) · SC 압력 환산값 · 판독 비 (−23 – −34 % 등) 를 원문 값처럼.

## 14. 기법 용어 미니사전
- **MDEM (Meshed Distinct Element Method)**: 입자마다 FE 메시를 주는 계산 (= MPFEM · 후보 B).
- **독립 접촉 (independent contacts)**: 각 접촉이 고립된 것처럼 반응한다는 가정 — Storåkers · Hertz 류 점접촉 DEM 의 바탕.
- **강소성 멱법칙**: σ = K₂εⁿ² — 탄성 없음 · K₂ = 경화 상수 · n₂ = 경화 지수 (0 = 완전 소성).
- **국소 상대밀도 ρ_i**: 구 부피 / 그 구의 Voronoï (radical) 셀 부피 · ρ_ij = 쌍 평균 · ρ₀_ij = 접촉이 생길 때의 쌍 평균.
- **S₁ · S₂**: 고립 접촉 강성 · 소성 비압축 강성 (ρ → 1 에서 발산).
- **2 차 접촉 (secondary contacts)**: 압축 중 새로 생기는 접촉 (BCC 의 둘째 이웃 등).
- **impingement**: 이웃 접촉들의 소성 영역이 서로 겹쳐 드는 현상 (원문 용어).
- **단순 압축 (simple compression)**: 고립 구를 두 강체 판 사이에서 누름 · **정수압**: 여섯 (또는 열네) 면이 같이 · **die**: 위아래만 · 옆 고정.

## 15. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로)

| 서지 (원문 목록) | 왜 · 정본 카드 |
|---|---|
| Chen, Y., Imbault, D., Dorémus, P., 2006. Numerical simulation of cold compaction of 3d granular packings. Materials Science Forum, 301–304. | 같은 그룹 3D MDEM (권 없음 [인쇄 그대로]) — 카드 없음 |
| Chen, Y., 2008. Contribution a la modélisation de la compression des poudres par une methode d'éléments discrets maillés. Ph.D. thesis, Institut Polytechnique de Grenoble. | 같은 그룹 MDEM 학위논문 — 카드 없음 |
| Frenning, G., 2008. An efficient finite/discrete element procedure for simulating compression of 3d particle assemblies. Computer Methods in Applied Mechanics and Engineering 197, 4266–4272. | 3D FE/DE (후보 B) — 카드 없음 (giannis2021 · gonzalez2012 · zunker2024 partII 에 이름만) |
| Gellatly, B.J., Finney, J.L., 1982a. Calculation of protein volumes: an alternative to the vorono procedure. Journal of Molecular Biology 161, 305–322. · Gellatly, B.J., Finney, J.L., 1982b. Characterisation of models of multicomponent amorphous metals: the radical alternative to the vorono polyhedron. Journal of Non-Crystalline Solids 50, 313–329. | 국소 상대밀도의 셀 정의 (radical) — 카드 없음 |
| Gethin, D.T., Lewis, R.W., Ransing, R.S., 2003. A discrete deformable element approach for the compaction of powder systems. Modelling and Simulation in Materials Science and Engineering 11, 101–114. | 2D MDEM (g) — 카드 없음 |
| Heyliger, P.R., McMeeking, R.M., 2001. Cold plastic compaction of powders by a network model. Journal of the Mechanics and Physics of Solids 49, 2031–2054. | Storåkers 류 접촉 압밀 — 카드 없음 |
| Kozicki, J., Donzé, F.-V., 2008. A new open-source software developed for numerical simulations using discrete modelling methods. Computer Methods in Applied Mechanics and Engineering 197, 4429–4443. | YADE — 카드 없음 |
| Martin, C.L., Bouvard, D., 2003. Study of the cold compaction of composite powders by the discrete element method. Acta Materialia 51, 373–386. | 정본 `martinbouvard2003_dem_composite_cold_compaction` |
| Martin, C.L., Bouvard, D., Shima, S., 2003. Study of particle rearrangement during powder compaction by the discrete element method. Journal of the Mechanics and Physics of Solids 51, 667–693. | ★ '≈ 0.8' 의 근거 둘 중 하나 (e · k) — 카드 없음 |
| Martin, C.L., 2004. Elasticity, fracture and yielding of cold compacted metal powders. Journal of the Mechanics and Physics of Solids 52, 1691–1717. | DEM 이 재배열을 잘 낸다는 근거로 인용 (p.3357) · 제목상 압밀 뒤 탄성 · 파괴 · 항복 — 탈압 (b) · R4 후보 [제목 근거 · 미열람] — 카드 없음 |
| Mesarovic, S.D., Fleck, N.A., 2000. Frictionless indentation of dissimilar elastic–plastic spheres. International Journal of Solids and Structures 37, 7071–7091. | 정본 `mesarovicfleck2000_dissimilar_elastoplastic_indentation` (그 카드: B2 단위셀 독립 접촉 D < 0.82) |
| Mesarovic, S.D., Fleck, N.A., 1999. Spherical indentation of elastic–plastic solids. Proceedings of the Royal Society of London A 455, 2707–2728. | 탄소성 구 압입 (c · U3) — 카드 없음 |
| Procopio, A.T., Zavaliangos, A., 2005. Simulation of multi-axial compaction of granular media from loose to high relative densities. Journal of the Mechanics and Physics of Solids 53, 1523–1551. | ★ MDEM 고밀도 (후보 B · l) — 카드 없음 (cantor2020 · demirtas2021 · gonzalez2012 에 이름만) |
| Skrinjar, O., Larsson, P.-L., 2004. On discrete element modelling of compaction of powders with size ratio. Computational Materials Science 31, 131–146. | 크기비 압밀 DEM (d) — 카드 없음 |
| Storåkers, B., Biwa, S., Larsson, P.-L., 1997. Similarity analysis of inelastic contact. International Journal of Solids and Structures 34, 3061–3083. | 정본 `storakers1997_similarity_inelastic_contact` (식 14) |
| Storåkers, B., Fleck, N.A., McMeeking, R.M., 1999. The viscoplastic compaction of composite powders. Journal of the Mechanics and Physics of Solids 47, 785–815. | ★ 복합 분말 (단단 + 무름) 압밀 (d) — 카드 없음 |
| Vu-Quoc, L., Zhang, X., Lesburg, L., 2001. Normal and tangential force–displacement relations for frictional elasto-plastic contact of spheres. International Journal of Solids and Structures 38, 6455–6489. | 작은 소성 변형 접촉 (e) — 카드 없음 |
| Drucker, D.C., Prager, W., 1952. Soil mechanics and plastic analysis or limit design. Quarterly Journal of Mechanics and Applied Mathematics 10, 157–175. | 연속체 캡 모형 (M0) — 서론 언급만 |

## [미확인] 목록
- 납 K₂ 20.5 MPa · n₂ 0.24 (· σ_Y 5 · K₁ 15.5 · n₁ 0.35 · E 10 GPa · ν 0.435) 의 출처 · 맞춘 방법.
- 식 (11) 맞춤에 쓴 하중 (S₂ = 정수압만인지 die 도인지) · 목적 함수 · 데이터 점 · 맞춤 오차.
- ρ₀_ij 의 실제 값 · 무작위 근사 · 15 입자의 처음 충전 생성법 · Voronoï 셀의 벽 처리 · 겹침 부피 처리.
- 계산 비용 (MDEM · DEM 벽시계 · Δt · 단계 수 · 15 입자 MDEM 의 요소 수 직접 서술).
- 그림 5 의 n₂ · 하중 경로 · 힘 정의 (세로 크기가 그림 3 · 6b 의 ≈ 1/3.6–1/5).
- 그림 7 die 의 식 (10) 선 계산 세부 (인쇄식 적분과 다름) · 단순 압축 선이 식 (12) 적분보다 ≈ 6 % 낮은 이유.
- Storåkers c² = 1.43e^(−0.97n₂) 의 출처 표기.
- 제하 · 마찰 · 다분산 · 다른 재료에서의 법칙 (저자가 앞으로의 일로 적음).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: PDF 첫 쪽 *"International Journal of Solids and Structures 46 (2009) 3357–3364"* · *"doi:10.1016/j.ijsolstr.2009.05.008"* · 저자 *"B. Harthong \*, J.-F. Jérier, P. Dorémus \*, D. Imbault, F.-V. Donzé"* · 접수 · 수정 · 온라인 날짜 — 후보 표 서지와 **같고** DOI 만 후보 표에 없었다.
- 식 14 개를 300 dpi 크롭에서 다시 읽었다 (텍스트 층의 'a1 b1 c1 d1 a2' = α₁ β₁ γ₁ δ₁ α₂ · 식 (10) 둘째 지수의 음의 부호 · 식 (14) 의 c²).
- 식 (10)–(12) 를 적분해 그림 6a (n₂ 다섯 · h/R 0.98) 를 2–3 % · 그림 6b (h/R 0.30) 를 0–9 % 안에서 재현 → 계수 옮겨 적기 확인.
- 식 (14) (R₀ = R/2 · n₂ 0.24) 를 그림 7 점선과 h/R 0.08–0.60 에서 2–3 % 안으로 대조 → 그림 7 의 축 보정 확인.
- BCC 2 차 접촉 (원문 '> 1') = π/3 = 1.047 · die = π/4 = 0.785 (기하) · 그림 10 곡선 시작 0.68 = π√3/8.
- 무작위 2 차 접촉 시작 (원문 0.80 · 0.83 · 0.87 · 0.91) 을 그림 11b 판독과 대조 — 같다.
- 판독 116 행: 축 = 눈금 표시 (그림 5a · 6 · 7 · 8b · 11 · 12) 또는 눈금 글자 중심 (그림 10 — 처음 눈 보정이 틀려 글자 중심으로 다시 맞춤).
- 중복 확인: 정본 `litdb/papers/` 목록 · DOI · 'Harthong' · 공저자 성 · 제목 낱말 grep — 이 논문 카드 없음 (gonzalez2012 · demirtas2021 · zunker2024 partII · comparison_vs_ours_DEM 이 인용만).

## 🔗 관련 카드
- 같은 축 (접촉 결합 · 다접촉 · 고밀도): `gonzalez2012_nonlocal_contact_confined_granular` (탄성 비국소 · 자유변수 0 · 이 논문을 §1 에 인용) · `giannis2021_stress_based_multicontact_dem` (응력 기반 다접촉 β) · `varkey2026_multicontact_elastoplastic_dem` (Thornton–Ning × 다접촉) · `zunker2024_mdr_contact_model_partI` · `zunker2024_bulk_elastic_partII` (Voronoï 판정 → 자유표면적 비) · `zunker2025_dem_large_deformation_compaction`.
- 원전 · 근거: `storakers1997_similarity_inelastic_contact` (식 14) · `mesarovicfleck2000_dissimilar_elastoplastic_indentation` ('≈ 0.8' 근거 · B2 D < 0.82) · `martinbouvard2003_dem_composite_cold_compaction` (인용 문헌) · `thorntonning1998_adhesive_elastoplastic_contact` (C′ 의 다른 꼴).
- 입자마다 FE · 연속체 (후보 B): `demirtas2021_mpfem_hollow_sphere_die_compaction` (ref [30] 으로 인용) · `pycompact2025_dem_mpfem_workflow` · `cantor2020_compaction_model_highly_deformable_particles` · `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
