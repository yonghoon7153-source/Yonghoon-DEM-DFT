<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-30 · 정독 71) 에서 꼭 뽑으라고 한 항목.
     본 = giannis2021_stress_based_multicontact_dem.md (같은 축 · 다접촉 DEM · 절 번호 · 머리 상자 · 메타 줄 · 서지 표 · 그림 표) · 곁 = gonzalez2012_nonlocal_contact_confined_granular.md · 같은 날 꼴 = du2025_dem_fem_force_chain_collector_damage_calendering.md · 두 필수 절 = §0-1 고른 의도 대조 · §8 자세한 분석.
     원문 = 출판본 (Phys. Rev. E 91, 032201 (2015) · 6 쪽 · 보충 자료 없음).  쪽 표기 "p.n" = PDF 쪽 n = 논문 쪽 032201-n.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (그림 3–6 은 전부 벡터 경로 — 경로 꼭짓점 좌표를 눈금선 좌표로 바꿔 읽음 · 재현 = litdb/figures/<slug>/digitized.csv 1,498 행 · 방법 = figures.json 'digitized') ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · §14) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug · 줄 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md · 정본 카드가 옮긴 것 — 출처를 그 자리에 적는다) · [미확인] = 본문 6 쪽 전수에 없음.
     원문 6 쪽은 글자 층 (PyMuPDF) + 쪽 렌더 + 벡터 경로로 읽었다.  계산 = 저자 자체 코드 (첫 저자 웹사이트 공개 · 참고문헌 [23] · GNU LGPL v2 이상) — 이 카드는 코드를 받지 않았다. -->

# 같은 알의 다른 접촉이 만든 탄성 변위를 겹침에 더하는 다접촉 DEM (MC-DEM · Giannis 가 'MC-strain' 이라 부른 것) — 하이드로겔 514 알 3D 접촉력 실측과 다섯 정식화 대조 — Brodu, Dijksman & Behringer (Phys. Rev. E 2015)

> slug `brodu2015_multiple_contact_dem_dense_granular` · DOI `10.1103/PhysRevE.91.032201` · type `DEM (contact-LAW theory, non-binary multi-contact, displacement-based: point force on an elastic half-space added to the Hertz overlap, one empirical prefactor gamma; 3D spheres, own code) + comparison with the authors' own 3D contact-force experiment (514 hydrogel grains, cyclic uniaxial compression to 13.4 % strain)` · PDF `338bf74e-30._Multiple-contact_discrete-element_model_for_simulating_dense_granular_media.pdf` · digested `2026-11-12` · status ✅

> elements: (없음 — 하이드로겔 알 · 배터리 소재 0)
> methods: elastic

> **저자**: **Nicolas Brodu** ¹·² · Joshua A. Dijksman ²·³ · Robert P. Behringer ² — ¹ INRIA (200 Avenue de la Vieille Tour, 33405 Talence, France) · ² Department of Physics & Center for Nonlinear and Complex Systems, Duke University (Durham, North Carolina, USA) · ³ Laboratory of Physical Chemistry and Colloid Science, Wageningen University (The Netherlands).  접수 2014-10-23 · 출판 2015-03-02 · © 2015 American Physical Society (오픈 액세스 문구 없음 — 그림 재사용은 확인 필요).
> **이웃 카드 (링크만)**: [`giannis2021_stress_based_multicontact_dem`](giannis2021_stress_based_multicontact_dem.md) (이 논문을 'MC-strain' 이라 부르고 LIGGGHTS 에 다시 구현해 대조군으로 씀) · [`gonzalez2012_nonlocal_contact_confined_granular`](gonzalez2012_nonlocal_contact_confined_granular.md) (이 논문 모형 'Sphere to sphere' 의 원전 [14]) · [`varkey2026_multicontact_elastoplastic_dem`](varkey2026_multicontact_elastoplastic_dem.md) (MC-stress 를 쓴 배터리 DEM).
> **판독 원자료**: `litdb/figures/brodu2015_multiple_contact_dem_dense_granular/digitized.csv` (1,498 행 — 그림 3 판 힘 고리 · 그림 4 P(f) · 그림 5 Z · 그림 6 비례식 · 벡터 경로 꼭짓점 · 눈금선 보정).

> ⚠⚠ **한 줄 경고 — 하이드로겔이다.**  E 23.3 kPa 의 연한 탄성 구 · 물에 잠김 · 밀도 맞춤 · μ ≈ 0.03 · 소성 0.  **LPSCl · NCM 으로 옮길 절대값은 0 개.**  옮길 수 있는 것은 식 (1) 의 꼴 · 비교 설계 (같은 자료 · 같은 E · 접촉 표현만 바꿈) · 지표 정의 · 부호 (binary Hertz DEM 이 이 탄성 조밀 침대에서는 **너무 무르다**) 뿐이다.

> ★★ **이 카드의 핵심 셋 (원문에 없는 것 · 원문과 어긋나는 것 포함 — §0-1 · §13)**:
> ① **원문 = 하이드로겔 514 알 다입자 실측 한 벌뿐이다.**  단일 고무구 · Tatara · '광탄성 (photoelastic)' · '반복 (iteration)' 이라는 낱말이 원문 6 쪽에 없다 (글자 층 grep 0 건).  가리킨 카드들의 *"세 정식화가 같은 Tatara 곡선을 각자 복원"* · *"O(C²) + 반복"* · *"광탄성 하이드로겔"* · *"γ 이론앵커 ν → 0 에서 1"* 은 이 원문이 아니라 Giannis 2021 의 재구현 · 서술을 거친 말이다 (§13 카드 문제).
> ② **γ ≈ 1.19 = 판 힘 한 수 (Rtop = 1 · 최대 압축 13.4 %) 에 맞춘 하나뿐인 자유값**이다 (p.2 · p.5).  나머지 지표 (errf · errZ · bhat) 는 같은 실험에서 본 점검이다.  **맞추지 않은 정식화끼리도 다입자 자료에서 갈린다** — 접촉 독립 Rtop **0.43** · 구 위 점힘 **0.44** · Gonzalez–Cuitiño 근사 ('Sphere to sphere') **0.70** · 반무한 탄성체 γ = 1 **0.80** (표 I [인쇄]).
> ③ **식 (1) 의 분수는 (1 − 2ν) 항에만 걸린다** (원문 인쇄 · `eq_01_…png` · Boussinesq 반무한 해의 벡터 꼴과 같음 [카드 산술 §14-1]) — giannis2021 카드 §4.2 의 식 7 옮김은 (3 − 4ν) 항까지 분수 위에 올렸다.  그리고 그림 판독만으로 **표 I 의 errf · errZ 를 소수 둘째 자리까지 재현**했다 (§3-4 · errf 단위 = N 으로 확정).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

1. **무엇**: 고전 DEM 의 "접촉은 서로 독립 (binary)" 가정을 깨려고, 한 알의 접촉 k 의 힘 F_k 가 같은 알의 다른 접촉 c 자리에 만드는 **탄성 변위 δ_{k→c}** (반무한 탄성체 위 점힘의 해 · 식 (1)) 를 그 접촉의 겹침 δ_c 에 **더한 뒤** Hertz 를 적용한다: F ∝ (δ_c + Σ_k δ_{k→c})^{3/2} (p.2).  FEM 없음 · 형상 변형은 해석 선형 탄성으로 (p.1).  자유값 = **γ 하나** (≈ 1.19).
2. **증거**: 저자 자체 실험 [8] (하이드로겔 514 알 · 일축 압축 20 회 · 변형률 0 → 13.4 % · 접촉마다 3D 힘 벡터 + 판 힘) 과 **다섯 정식화** (원문 이름: Independent contacts · Point force on sphere · Sphere to sphere · Elastic half-space · MC-DEM) 를 같은 자료로 대조 (표 I · 그림 3–6).
3. **부호**: 측정 E 를 쓴 binary Hertz DEM 이 이 탄성 조밀 침대에서 최대 압축 판 힘의 **43 %** 만 낸다 (Rtop 0.43 · 2.3 배 모자람 [카드 산술 1/0.43]).  ↔ 우리 LPSCl DEM 은 측정 E 로는 **너무 단단해서** 18 배 연화한다 [우리 · CLAUDE.md].  같은 "binary Hertz 는 틀린다" 라도 **빠진 물리가 다르고 부호가 반대**다 (판정 아님 · giannis2021 카드 §7-3 과 같은 방향).
4. **질문 e (대안 · 맞춘 값 수)**: MC-DEM = 변위 기반 다접촉 보정 · **맞춘 값 1 개 (γ)** · 맞춘 대상 = **판 힘 한 수** (Rtop = 1) · 비용 = **O(ZN)** (Z 알당 접촉 수 · N 알당 이웃 수 · p.3).  유효 범위 = 이 실험의 최대 변형률 13.4 % 까지 · Hertz 적용 한계 문장 없음.
5. **질문 k (DEM 한계)**: *"The conventional DEM approach [1] assumes that all contact forces are binary … This is not rigorously true"* (p.1) · *"provides only a first-order description"* (p.1) · *"The traditional DEM implementation with independent contacts clearly fails to reproduce the measurements."* (p.4) — 수치 = Rtop 0.43 · errf 3.39 N (표 I).
6. **우리 18× 연화의 대안인가 → 아니다 (방향이 반대)**.  그리고 **식 (1) 은 E 와 무관**하다 (p.6 · F_k 에 E 가 들어 있어 분모 E 와 지워짐) → 다접촉 보정의 상대 크기는 **겹침 기하** (∝ γ√(δ/R) [카드 산술 §14-2]) 로 정해진다.  연화된 E 로 부푼 겹침 위에 얹으면 '연화가 만든 겹침' 에 결합을 계산하게 된다 — 설계 질문이지 판정이 아니다.
7. **2D/3D · 탈압**: 실험 · 계산 모두 3D · 2D 에 대한 말 없음.  가압–탈압 **고리 (이력)** 를 실험 · 모형 모두 보이고 errf 가 두 가지를 다 셈한다 · 되돌아옴 · 잔류 변형 값은 없다 (탄성 알).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-30 의 '왜' 칸)

의도 원문: *"e · k — 변위 기반 다접촉 보정 (Giannis 가 'MC-strain' 이라 부른 baseline · γ 1 개 · O(C²) + 반복) 과 광탄성 하이드로겔 다입자 실측 = '접촉끼리 독립' 가정이 깨지는 것을 다입자에서 잰 자료 (단일 고무구 곡선은 세 정식화를 구분 못 하고 구분력은 다입자 예측에 있음)"* (가리킨 카드 = `comparison_vs_ours_DEM` §A (후보 표의 L743 · L747–753 → 지금 L744 · L757–L767) · `giannis2021_stress_based_multicontact_dem` · `gonzalez2012_nonlocal_contact_confined_granular`)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "e" (질문 e: 점접촉 법칙이 깨지는 범위와 대안 · 맞춘 값 수) | **채움** | 대안 다섯 (§4-3) · MC-DEM 맞춘 값 1 개 (γ ≈ 1.19 · p.2) · 대상 = Rtop = 1 (p.5) · 범위 = 변형률 0 → 13.4 % (p.3) — 깨지는 **범위의 문턱** (몇 % 부터인지) 은 원문에 없다 [미확인] |
| "k" (질문 k: DEM 의 한계) | **채움** | p.1 §II binary 가정 문장 · p.1 §I 두 효과 · p.2–3 *"which the basic DEM model is unable to achieve"* · p.4 *"clearly fails"* (§4-6 (i)) |
| "변위 기반 다접촉 보정" | **채움** | 식 (1) (p.2 · `eq_01_cross_contact_displacement_point_force_half_space.png`) + 본문 식 F ∝ (δ_c + Σ_k δ_{k→c})^{3/2} (p.2 · `eq_unnumbered_sIII_multicontact_hertz_law_in_text.png`) — 보정은 **겹침 (변위)** 에 더한다 |
| "Giannis 가 'MC-strain' 이라 부른 baseline" | **일부** | 원문 이름 = **"MC-DEM"** (*"a method dubbed multicontact DEM (MC-DEM)"* p.1) — 'MC-strain' 은 원문에 없다 (Giannis 의 명명 · giannis2021 L132 · L564 경유).  baseline 이라는 자리는 Giannis 쪽 일 |
| "γ 1 개" | **채움** | *"We therefore let γ be an adjustable parameter in order to account empirically for the geometry."* (p.2) · *"We found a best fit at γ ≈ 1.19"* (p.2) · *"MC-DEM, adjusting γ so that Rtop = 1"* (p.5).  ⚠ 그 밖에 '최선 추정' 으로 고른 값: E 23.3 kPa · μ ≈ 0.03 ± 0.02 · 반발 계수 *"close to one"* (값 [미확인]) (p.3) — 맞춤은 아니지만 고른 값이다 |
| "O(C²)" | **일부** | 원문 = **"O(ZN), where Z is the number of contacts per grain and N the number of neighbors per grain"** (p.3) — 변위를 접촉점뿐 아니라 가장 가까운 이웃 방향의 알 표면에서도 계산하기 때문 (p.2) · 접촉점끼리만 보면 Z² 꼴 [카드 해석] |
| "+ 반복" | **없음** | 원문 6 쪽에 'iterat' **0 건** · 원문은 *"At each simulated time step, the total displacements Σ_k δ_{k→c} are computed …"* (p.2) 만 적는다 · F_k 가 그 스텝의 힘인지 앞 스텝의 힘인지 · 자기 일관으로 푸는지 **[미확인]** — '반복 · 불안정' 은 Giannis 의 서술 (giannis2021 L144–L146) |
| "광탄성" | **없음 ([미확인])** | 원문에 'photoelastic' · 'birefring' **0 건** · 측정법은 [8] (*"Spanning the scales of granular materials through microscopic force imaging"*, Nat. Commun. 6, 6361) 로 넘김 · 이 논문이 적은 것: *"50 full 3D scans"* (p.3) · *"immersed hydrogel particles"* (p.3) · *"With density matching"* (p.5) |
| "하이드로겔 다입자 실측" | **채움** | 514 알 · 일축 20 회 연속 · 변형률 0 → 13.4 % · 사이클마다 판이 닿은 3D 스캔 50 + 판이 위에 뜬 스캔 10 · 처음 5 사이클 버림 · 가압 · 탈압 따로 · 접촉마다 3D 힘 벡터 + 스캔마다 판 힘 (p.3 §V · `txt_p3_experiment_514_hydrogel_20_cycles_13p4pc_3d_forces.png`).  측정 조건 = **누른 채 (가압 · 탈압 가지)** · 압력 (Pa) · 온도 · 알 크기 **[미확인]** |
| "'접촉끼리 독립' 가정이 깨지는 것을 다입자에서 잰 자료" | **채움 (모형 대조로)** | 표 I: 접촉 독립 Rtop 0.43 · errf 3.39 · errZ 0.51 · bhat × 10² 7.21 ↔ MC-DEM 1.00 · 0.41 · 0.26 · 0.98 (p.4 [인쇄]).  ⚠ 잰 것은 **접촉력 · Z · 판 힘**이고 접촉 사이 변위 결합 자체를 잰 것은 아니다 — 결합의 필요는 **같은 자료에 다섯 모형을 대 본 결과**로 드러난다 |
| "단일 고무구 곡선은 세 정식화를 구분 못 하고" | **없음** | 원문에 단일 구 · 고무 · Tatara **0 건** — 단일 입자 곡선 대조가 이 논문에 없다.  그 문장의 근거는 Giannis 2021 그림 4 (Giannis 가 MC-strain 을 다시 구현해 **γ 0.55** 로 맞춤 · giannis2021 L70 · L85) 와 Gonzalez 2012 그림 7 |
| "구분력은 다입자 예측에 있음" | **일부** | 다입자 한 벌에서 정식화가 갈린다 (Rtop 0.43 / 0.44 / 0.70 / 0.80 / 1.00 · errf 3.39 → 0.41 N).  ⚠ MC-DEM 의 1.00 은 **맞춘 값** · '예측' 은 맞추지 않은 넷 (특히 Sphere to sphere 0.70 · Elastic half-space 0.80) 뿐 · **침대는 하나** — 두 번째 침대로 옮기는 시험이 이 논문에 없다 (그 시험은 Giannis 2021 그림 14 · 1921 이봉 침대 [다른 카드 giannis2021 L73]) |

**가리킨 카드의 2 차 인용 대조** (자세히는 §13):

| 카드 · 줄 | 그 카드의 말 | 원문 | 판정 |
|---|---|---|---|
| giannis2021 L132 · L454 · gonzalez2012 L575 · L831 | 서지 *"Brodu, Dijksman, Behringer, Phys. Rev. E 91 (2015) 032201"* | p.1 머리글 · DOI 같음 | ✓ |
| giannis2021 L136–L140 (§4.2 식 7) | 분수 막대가 *"(3−4ν)n_k·n_c − (1−2ν)(n_k + u_kc)·n_c"* 전체 위 | 식 (1): 분수는 (1 − 2ν) 항의 (n_k + u_kc)·n_c ÷ (1 + n_k·u_kc) **에만** | ✗ (옮김) |
| giannis2021 L144–L146 · L458 | *"O(C²) … 원리적으로 반복 … Brodu 는 준정적 가정으로 1회 반복만"* | O(ZN) · 반복 낱말 0 건 · 준정적 문장 = 반발 계수 고른 이유뿐 (p.3) | ✗ (원문에 없음) |
| giannis2021 L567 | *"Brodu 2015 [23] / Barés 2020 [50]: 하이드로겔 구 패킹의 광탄성 3D 실험 데이터 공개 논문"* | 광탄성 0 건 · 공개 = 시뮬레이션 **소스 코드** [23] · 실험 출처 = [8] | ✗ |
| giannis2021 L86 (그림 11a) | 고전 ≈ 245 · MC-strain (γ = 1) ≈ 455 · 실험 ≈ 555 Pa | 같은 실험 · 다른 구현: 고전 Rtop 0.43 ↔ 245/555 = **0.44** · γ = 1 Rtop 0.80 ↔ 455/555 = **0.82** [카드 산술] | ✓ (정합) |
| giannis2021 L72 · L274 | 514 하이드로겔 MC-strain **γ 1.12** (*"[49] 가 제안한 값"*) | 이 논문의 맞춤 = **γ ≈ 1.19** | 차이 (카드는 출처를 [49] 로 적음 · 문제 아님) |
| gonzalez2012 L607 · L609 | *"셋 다 Tatara 1989 고무구 … 로 검증한다"* | Brodu 원문에 Tatara · 단일 구 0 건 | ✗ |
| gonzalez2012 L502 · L592 · L737 | Brodu 의 γ *"이론앵커 있음 (ν→½ 0.5 / ν→0 1)"* | 원문 = **γ = 1 반무한 (half-space) · γ = 0.5 = ν 0.5 의 무한 공간 (full-space)** (p.2) · ν = 0 에서는 식 (1) 이 직교 접촉에 결합을 **잘못** 준다고 저자가 적음 (p.5) | ✗ |
| gonzalez2012 L541 · L591 · comparison L744 · L761 | *"O(C²) + 반복"* | O(ZN) · 반복 없음 | ✗ / 일부 |
| gonzalez2012 L834 · comparison L767 | *"광탄성 하이드로겔 (구 패킹) 다입자 실측 (데이터가 딸려 있어)"* | 광탄성 0 건 · 데이터 공개 문장 0 건 | ✗ |
| comparison L763–L766 | *"세 정식화가 같은 실험 (Tatara 1989 고무구) 을 각자 복원한다"* | MC-strain 의 Tatara 복원은 **Giannis 의 재구현** (γ 0.55) · Brodu 원문은 Tatara 를 쓰지 않음 | ✗ ('각자' 는 원문으로 서지 않음) |
| gonzalez2012 L614–L615 · comparison L765–L766 | *"구분력은 다입자 · 다배치 예측에 있다 … [Gonzalez 2012 는] 그런 시험을 하지 않았다"* | 맞다 — 그리고 **Brodu 가 Gonzalez–Cuitiño 근사식 (그 논문 식 (3)) 을 다입자 자료로 시험했다**: Rtop 0.70 · errf 1.82 · errZ 0.34 · bhat × 10² 2.57 (표 I) | ✓ + 새 정보 |

---

## 1. 한 줄 요약

**접촉 독립 (binary) DEM 에 "같은 알의 다른 접촉이 만든 반무한 탄성체 변위 × γ" 를 겹침에 더하는 3D 다접촉 DEM** 을 제안하고, 저자 자체의 하이드로겔 514 알 3D 접촉력 실측 (변형률 ≤ 13.4 %) 에 다섯 정식화를 대어 **binary Hertz 는 최대 압축 판 힘의 43 % 만 내고 (Rtop 0.43) · 맞추지 않은 결합 모형도 0.70–0.80 까지 올리며 · γ ≈ 1.19 하나로 판 힘 · 접촉력 분포 · 접촉 수를 함께 맞춘다** 고 보고한 6 쪽 논문.  ⚠ **탄성 전용** (소성 · 점착 없음) · 단단한 재료에 대한 타당성은 저자 스스로 *"open question"* (p.6).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **Nicolas Brodu**¹² · Joshua A. Dijksman²³ · Robert P. Behringer² | **Phys. Rev. E 91, 032201 (2015)** · 6 쪽 · 접수 2014-10-23 · 출판 2015-03-02 · PACS 45.70.−n | **10.1103/PhysRevE.91.032201** | **하이드로겔 알** (E 23.3 kPa) — 배터리 소재 **0** | **DEM 접촉 법칙 (non-binary · 변위 기반) + 자체 3D 실험 대조** |

- ¹ INRIA (Talence) · ² Duke University Physics & CNCS · ³ Wageningen University (Physical Chemistry and Colloid Science).
- 자금: NASA NNX10AU01G · NSF DMR12-06351 · ARO W911NF-1-11-0110 (p.6).
- 코드: *"The source code for the simulations, including the new model, is available as free software on the first author's website [23]"* — [23] = http://nicolas.brodu.net/code/dymo/ · GNU LGPL v2 이상 (p.6 · `txt_p6_source_code_available_ref23.png`).  **실험 자료 공개 문장은 없다.**
- 절 구성: I Introduction · II Background · III Introducing multiple interactions · IV Models · V Experiment · VI Microscopic variable scaling · VII Discussion · VIII Conclusion · 참고문헌 23 개.
- **계보**: 측정 = 같은 저자의 [8] (*"Spanning the scales of granular materials through microscopic force imaging"*) — **방법은 이 논문에 적히지 않았다.**  비교 정식화 'Sphere to sphere' = Gonzalez & Cuitiño 2012 [14] (정본 `gonzalez2012_…`) · 이 논문 = Giannis 2021 [23] 의 'MC-strain' (정본 `giannis2021_…`).
- **후보 표 서지와의 차이**: 없음 (후보 표는 *"제목 · DOI 비교 문서에 없음"* 이라 적었고 원문에서 제목 *"Multiple-contact discrete-element model for simulating dense granular media"* · DOI 10.1103/PhysRevE.91.032201 를 확인).

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 기준 실험 · 재료 (p.3 §V · `txt_p3_experiment_514_hydrogel_20_cycles_13p4pc_3d_forces.png` · `txt_p3_e_23p3kpa_inflation_cor_mu_0p03_saturated_friction.png`)

| 항목 | 값 | 위치 · 표지 |
|---|---|---|
| 알 수 | **514** hydrogel grains | p.3 [인쇄] |
| 재료 · 환경 | 하이드로겔 · 액체에 잠김 (*"immersed hydrogel particles"*) · 밀도 맞춤 (*"With density matching, we can neglect hydrostatic pressure gradients"*) | p.3 · p.5 [인쇄] — 액체 종류 [미확인] |
| 알 모양 | *"not completely spherical in their uncompressed state"* → 계산에서는 **같은 부피 · 같은 처음 질량중심의 구**로 바꾸고 이완 → 시뮬레이션 침대가 약간 부풀어 가장 낮은 압축에서 판 힘이 0 이 아님 (*"negligible in the most compressed states"*) | p.3 [인쇄] |
| 알 크기 · 크기 분포 · 상자 · 판 면적 · 처음 높이 | **원문에 없음** | [미확인] ([8] 에 있을 것 [카드 해석]) |
| E | **23.3 kPa** (*"our best estimate"*) | p.3 [인쇄] · 측정법 · 불확도 [미확인] |
| ν | 입력값으로 적힌 문장 없음 — **0.5 로 읽힘** | [카드 해석: p.2 *"for ν = 0.5 (and only that case) the half-space solution is the same as in Ref. [14]"* + p.5 *"these two models are equivalent when the contact positions are restricted to the surface of a sphere"* + p.5 *"Future models also need to account for lower Poisson's ratios ν < 0.5"*] |
| μ (알–알) | **≈ 0.03 ± 0.02** (실험 오차) · 계산은 늘 포화 F_t = μF_n | p.3 [인쇄] |
| 반발 계수 | *"a constant coefficient of restitution [19] close to one"* — 값 없음 (판 운동량을 흩고 침대를 가라앉히려 1 은 아님) | p.3 [인쇄] · 값 [미확인] |
| 압축 | 일축 · **20 회 연속** · 변형률 **0 → 13.4 %** (초록: *"experimental maximum limit of 13%"*) | p.3 · p.1 [인쇄] |
| 압축 수준 축 | 그림 3 · 5 x 축 = **Δ 0 → 25 mm** | [판독] → 25 mm ↔ 13.4 % 이면 기준 높이 ≈ **187 mm** · Δ 18 mm ↔ **9.6 %** [카드 산술 = 25/0.134 · 18/186.6] — 원문은 변형률의 기준 길이를 정의하지 않는다 |
| 스캔 | 사이클마다 판이 알에 닿은 **3D 스캔 50** + 판이 위에 뜬 스캔 **10** · 처음 **5 사이클 버림** (→ 15 사이클: 그림 6 캡션 *"the 15 retained compression or unloading phases"*) · 가압 · 탈압 **따로** (*"some hysteresis is observed, which the simulations also reproduce"*) | p.3 · p.5 [인쇄] |
| 측정량 | 접촉마다 **3D 힘 벡터** [8] · 스캔마다 **판 힘** · 같은 가압 · 탈압 단계끼리 평균 = *"ground truth"* | p.3 [인쇄] — 측정법 (영상 · 재구성 · 힘 추론) **[미확인]** |
| 약한 힘 해상도 | 약한 힘 하한 τ ≈ **4 mN** (MC-DEM 의 최적 문턱으로 어림 · 표 I) · [8] 의 가장 낮은 압축 수준 평균 접촉력 **⟨f⟩ = 10 mN** | p.4 [인쇄] |
| 응력 (Pa) · 압력 | **없음** (판 힘만 N 으로) | [미확인] |
| 온도 | 없음 | [미확인] |

### 3-2. ★ γ — MC-DEM 의 하나뿐인 자유값 (p.2 · `txt_p2_gamma_full_space_0p5_half_space_1_adjustable.png` · `txt_p2_models_list_gamma_1p19.png`)

| γ | 뜻 (원문) | 위치 · 표지 |
|---|---|---|
| **1** | 반무한 탄성체 위 점힘 해 그대로 ([17] Bower §5.4.4) = 모형 **'Elastic half-space'** | p.2 [인쇄] |
| **0.5** | **비압축 재료 (ν = 0.5)** 의 **무한 공간 (full-space)** 해 ([17] §5.4.3) — *"only induces a change in prefactor"* | p.2 [인쇄] |
| **≈ 1.19** | **MC-DEM** 최적 맞춤 — 맞춘 대상 = **Rtop = 1** (최대 압축 판 힘) | p.2 · p.5 [인쇄] |

- ⚠ **1.19 는 두 이론값 [0.5, 1] 밖이다** (반무한보다도 결합이 세다) [카드 관찰].  저자는 γ 를 *"an empirical prefactor"* · *"to account empirically for the geometry"* 라 부른다 (p.2 · p.5) — **이론값으로 정해지는 수가 아니다.**
- ⚠ **"ν → 0 에서 γ = 1"** 이라는 말은 원문에 없다.  ν = 0 에 대해 원문이 하는 말은 반대 방향이다: *"In the particular case of ν = 0, no correlation should be introduced between orthogonal contacts. Yet both the linear elasticity half-space solution [Ref. [17] and Eq. (1)], as well as the sphere-to-sphere contact approximation [14], predict some cross-contact displacements δ_{k→c} in this situation."* (p.5) — 식 (1) 이 ν = 0 에서 틀린 결합을 준다는 것 (§14-3 에서 괄호 값 −0.086 ≠ 0 확인).
- ★ **γ 와 E 는 판 힘 한 수로 나뉘지 않는다** [카드 산술 §14-4]: 식 (1) 이 E 와 무관하고 Hertz 힘이 E 에 비례하므로, 중력 없는 준정적 변위 제어에서 MC-DEM 의 판 힘은 **E 에 정비례** → Rtop ∝ E.  E (23.3 kPa · 'best estimate' · 불확도 미기재) 가 x % 틀리면 같은 Rtop = 1 을 위해 γ 가 그만큼을 흡수한다.  같은 산술로 **binary DEM 도 E 를 2.3 배 (1/0.43) 올리면 Rtop = 1** 이 된다 (원문에 그런 팔은 없다).

### 3-3. ★ 표 I — 다섯 정식화 × 지표 (p.4 · `tab_1.png` · [인쇄])

| Model (원문 이름) | Rtop | errf | errZ | bhat × 10² | τ (mN) |
|---|---|---|---|---|---|
| Independent contacts | **0.43** | **3.39** | 0.51 | 7.21 | 2.89 |
| Point force on sphere | 0.44 | 3.23 | 0.53 | 6.51 | 2.93 |
| Sphere to sphere | 0.70 | 1.82 | **0.34** | 2.57 | 3.35 |
| Elastic Half Space | 0.80 | 1.26 | 0.40 | 1.90 | 3.45 |
| MC-DEM | **1.00** | **0.41** | **0.26** | **0.98** | 4.00 |
| *Perfect fit* | *1.00* | *0* | *0* | *0* | *< 10* |

- 지표 정의 (p.3–4 · `txt_p3_rtop_errf_definitions.png` · `eq_unnumbered_sV_bhattacharyya_distance_in_text.png` · `txt_p4_fig4_weak_forces_errz_tau_4mn_z_6p4.png`):
  **Rtop** = 계산 ÷ 측정 판 힘 (최대 압축 수준 · 평균) · **errf** = 모든 압축 수준 (가압 + 탈압) 판 힘의 RMS 오차 (단위 미기재 → **N** 확정 [카드 산술 §3-4]) · **bhat** = Bhattacharyya *"distance"* d = −log B, B = ∫₀^∞ √(p(f)q(f)) df 를 모든 압축 수준에서 평균한 D = −log⟨B⟩ · **errZ** = 시뮬레이션에서 f < τ 인 약한 힘의 접촉을 뺀 뒤 알당 접촉 수 Z 의 RMS 오차 · **τ** = errZ 를 가장 작게 하는 문턱 (= 실험의 약한 힘 해상도 어림).
- 원문 판정: *"The classic DEM model and the point force on sphere solutions are both off by more than 50%. The sphere-to-sphere and linear half-space models come closer, but the geometric correction by γ is necessary to reach a Rtop = 1."* (p.3) · *"The seminal multiple-contacts model proposed by Gonzalez and Cuitiño [14] offers good performance, but not as good as the half-space approximation from linear elasticity."* (p.5).
- ⚠ [카드 관찰] errZ 만은 **Sphere to sphere (0.34) 가 Elastic half-space (0.40) 보다 낫다** — 원문의 *"not as good as"* 는 Rtop · errf · bhat 에서만 선다.
- ⚠ MC-DEM 의 Rtop 1.00 은 **맞춘 결과**다 — *"MC-DEM, adjusting γ so that Rtop = 1, yields the best results on all quantifiers."* (p.5).

### 3-4. ★ 그림 판독 (벡터 경로 · `digitized.csv`)

**(a) 그림 3 — 판 힘 F [N] (위 가지 = 가압 · 아래 = 탈압)** [판독 · μ = 0.03]

| 모형 | Δ 5 mm (가압/탈압) | Δ 10 | Δ 15 | Δ 20 | **Δ 25 (최대)** | 실험 대비 (가압 · Δ 5 / 10 / 15 / 20 / 25) |
|---|---|---|---|---|---|---|
| **실험** | 0.46 / 0.19 | 2.05 / 1.05 | 4.98 / 3.29 | 9.50 / 7.62 | **15.68** | — |
| Independent contacts | 0.67 / 0.38 | 1.45 / 0.96 | 2.68 / 1.95 | 4.44 / 3.58 | **6.68** | 1.47 · 0.71 · 0.54 · 0.47 · **0.426** |
| Point force on sphere | 0.71 / 0.43 | 1.61 / 1.07 | 2.98 / 2.15 | 4.79 / 3.82 | **6.86** | 1.55 · 0.79 · 0.60 · 0.50 · **0.438** |
| Sphere to sphere | 0.79 / 0.50 | 1.93 / 1.31 | 3.72 / 2.80 | 6.69 / 5.50 | **11.00** | 1.75 · 0.94 · 0.75 · 0.70 · **0.702** |
| Elastic half space | 0.76 / 0.49 | 1.95 / 1.36 | 4.04 / 3.06 | 7.46 / 6.27 | **12.57** | 1.68 · 0.95 · 0.81 · 0.79 · **0.802** |
| MC-DEM | 0.88 / 0.58 | 2.18 / 1.62 | 4.61 / 3.54 | 8.77 / 7.41 | **15.75** | 1.93 · 1.07 · 0.92 · 0.92 · **1.004** |

- **Δ 25 mm 끝점의 비 = 표 I Rtop 과 같다** (0.426 · 0.438 · 0.702 · 0.802 · 1.004 ↔ 0.43 · 0.44 · 0.70 · 0.80 · 1.00) [카드 산술].
- ★ **errf 재현**: 가압 Δ 0–25 (26 점) + 탈압 Δ 1–24 (24 점) 의 (모형 − 실험) RMS = **3.388 · 3.230 · 1.819 · 1.262 · 0.415** ↔ 표 I 3.39 · 3.23 · 1.82 · 1.26 · 0.41 → **errf 단위 = N · 그림 3 의 1 mm 격자 50 점에서 셈** [카드 산술].
- ★ **MC-DEM 도 곡선 모양은 다르다**: Δ 5 mm 에서 실험의 1.93 배 (모든 모형이 1.5–1.9 배 = 침대 부풂 · p.3) · Δ 15–20 mm 에서 0.92 배 · 끝점만 1.00 (맞춤) [카드 산술].
- **이력 고리** (Δ 1–25 mm · 사다리꼴 1 mm) [카드 산술]: 고리 넓이 ÷ 가압 일 = 실험 **25.7 / 121.4 N·mm = 0.212** · MC-DEM 19.4 / 119.0 = **0.163** · Independent 13.4 / 62.8 = 0.214 · Point force 14.7 / 67.5 = 0.218 · Sphere to sphere 17.4 / 92.1 = 0.189 · Elastic half space 17.4 / 100.8 = 0.172 (N·mm = mJ).  → 판 힘–변위 평면에서는 **MC-DEM 의 고리가 실험보다 작다** (그림 6 평면의 *"more hysteresis"* (p.5) 와는 다른 평면).
- 탈압 끝: Δ ≈ 1 mm 에서 실험 0.03 N · 모형 0.12–0.18 N [판독] — 판 힘이 거의 0 으로 돌아온다 (탄성 알 · 잔류 변형 값 없음).
- 가지 판정: 위 가지 = 가압 (MC-DEM 의 위 가지 − F_min 이 그림 6 의 범례 'Compression' 계열과 점마다 같음 [카드 산술]).

**(b) 그림 4 — Δ 18 mm 탈압 가지의 p(f)** [판독 · 그려진 범위 f ≤ 0.2 N]

| 모형 | 봉우리 f (N) · p | 평균 f (mN) [카드 산술] | 곡선 끝 f (N) | 이 한 수준의 Bhattacharyya d = −ln B (공통 범위) [카드 산술] |
|---|---|---|---|---|
| **실험** | **0.034 · 10.6** | **62.6** (적분 0.964) | 0.200 (축 끝) | — |
| Independent contacts | 0.009 · 18.9 | 35.8 | **0.135** | 0.130 |
| Point force on sphere | 0.009 · 19.5 | 37.4 | 0.168 | 0.110 |
| Sphere to sphere | 0.015 · 14.2 | 49.2 | 0.182 | 0.055 |
| Elastic half space | 0.006 · 12.7 | 53.2 | 0.198 | 0.046 |
| MC-DEM | 0.037 · 11.3 | 61.4 | 0.200 | 0.041 |

- 원문: *"As expected, the weak forces show the most discrepancy. Nevertheless, MC-DEM reproduces both the experimental distribution peak and the largest force values."* (p.4).  binary 계열은 **약한 힘이 너무 많고 큰 힘 꼬리가 없다** (판 힘이 모자라는 것과 같은 그림).
- ⚠ d 는 이 한 수준의 값이라 표 I bhat (모든 수준 평균 D) 과 **같은 양이 아니다** — 순서만 같다.
- ⚠ 캡션 *"force on the top plate is about half the maximum"* — 판독 탈압 가지 Δ 18 mm 판 힘 5.57 N = 최대의 **0.36** · 가압 가지는 7.53 N = 0.48 [판독 · 카드 산술] (어림 표현 · 판정 아님).

**(c) 그림 5 — 약한 힘을 뺀 알당 접촉 수 Z** [판독 · 패널마다 같은 실험 곡선 · 두 가지 중 어느 쪽이 가압인지 표지 없음]

| 모형 | Z (Δ 0) | Z (Δ 1 · 다른 가지) | Z (Δ 10 · 두 가지) | **Z (Δ 25)** | (모형 − 실험) 평균 |
|---|---|---|---|---|---|
| **실험** | 3.37 | 3.46 | 7.15 / 6.73 | **8.97** | — |
| Independent contacts | 3.80 | 4.07 | 6.71 / 6.54 | 8.30 | −0.29 |
| Point force on sphere | 3.74 | 4.07 | 6.69 / 6.50 | 8.33 | −0.31 |
| Sphere to sphere | 3.52 | 3.83 | 6.78 / 6.61 | 8.70 | −0.20 |
| Elastic half space | 3.56 | 3.86 | 6.78 / 6.58 | 8.61 | −0.22 |
| MC-DEM | 3.42 | 3.68 | 6.79 / 6.58 | 8.86 | −0.15 |

- ★ **errZ 재현**: 경로 순서로 짝지은 50 점 RMS = **0.515 · 0.533 · 0.340 · 0.396 · 0.264** ↔ 표 I 0.51 · 0.53 · 0.34 · 0.40 · 0.26 [카드 산술].
- 문턱 없이 세면 가장 낮은 압축에서 계산 Z = **6.4–6.5** (잔류 압축의 부작용 · 약한 마찰 구가 쉬면 4–5 [20]) (p.4 [인쇄]).

**(d) 그림 6 — 식 (2) 검증: F − F_min vs ⟨f − f_min⟩⟨Z⟩⟨φ⟩⟨b⟩** [판독 · 최소제곱 · 이동 (MC-DEM +5 · 고전 +10 × 10⁻³ N m) 을 뺀 값]

| 계열 | 가압 기울기 | 탈압 기울기 | x 최대 (10⁻³ N m) | F − F_min 최대 (N) |
|---|---|---|---|---|
| 실험 | **1.12** | 1.12 | 14.0 | 15.72 |
| MC-DEM | 0.99 | 0.93 | 16.1 | 15.56 |
| 고전 DEM (접촉 독립) | 1.04 | 0.97 | 6.33 | 6.56 |

(기울기 단위 = N per 10⁻³ N m = 10³ m⁻¹.)  원문: *"Remarkably, the slope is nearly the same in all three cases, despite the top force being halved for the same compression level in the classic DEM case."* · MC-DEM 은 *"a slightly lower coefficient of proportionality … as well as more hysteresis between the compression and unloading phases"* (p.5) → 판독으로 가압 기울기 MC-DEM −11 % · 고전 −7 % (실험 대비) [카드 산술].

### 3-5. 계산 비용 · 규모

- 비용 서술 = **O(ZN)** 뿐 (p.3).  벽시계 시간 · 하드웨어 · 시간 간격 · 스텝 수 · 반복 수 **[미확인]**.
- 계산 알 수 = 실험과 같은 514 개 [카드 해석 — 실험 알을 같은 부피 구로 바꿨다는 문장 (p.3)].
- 시드 · 앙상블 · 산포 **없음** (계산은 15 사이클 평균에 대는 한 벌로 보임 [카드 해석]).

## 4. ★ 방법 — 모델을 식 수준으로

### 4-1. 고전 DEM (참조 모형 'Independent contacts' · p.1–2)

- *"nondeformable overlapping spheres [2] and independent contacts with Hertz's law"* (p.2) · 법선 힘 ∝ δ^{3/2} (p.1) · 접선 = 늘 포화 **F_t = μF_n** (μ = 0.03 · 미끄럼 반대 방향 · p.3) · 반발 계수 *"close to one"* (p.3) · 중력 = 밀도 맞춤으로 정수압 기울기 무시 (p.5 · DEM 에 중력 항을 넣었는지 [미확인]).
- 원문이 든 일반 DEM 의 덧붙임: *"Depending on the model, various features are added: plasticity, cohesion, tangential forces to account for surface friction, etc."* (p.1) — **이 논문의 모든 모형은 소성 · 점착 없음.**

### 4-2. ★ MC-DEM 식 — 식 (1) (p.2 · `eq_01_…png`) + 본문 식 (`eq_unnumbered_sIII_…png`)

```
            (1+ν) F_k  ⎧                                                                  (n_k + u_kc)·n_c ⎫
δ_{k→c} = −γ ───────── ⎨ (n_k·u_kc)(n_c·u_kc) + (3 − 4ν) n_k·n_c − (1 − 2ν) ─────────────────── ⎬      (1)
            2π E d_kc  ⎩                                                                   1 + n_k·u_kc   ⎭

F_c ∝ ( δ_c + Σ_k δ_{k→c} )^{3/2}                                                (본문 · 식 번호 없음 · p.2)
```
- 기호 (그림 2): F_k = 접촉 k 의 힘 · E = 영률 · ν = 포아송 비 · d_kc = 두 접촉점 사이 거리 · n_k · n_c = 접촉면 법선 (알 **안쪽**) · u_kc = k → c 단위벡터.  ★ **분수는 (1 − 2ν) 항에만 걸린다** (원문 인쇄 · §14-1 대수 점검).
- 출처: Bower [17] §5.4.4 의 반무한 탄성체 위 점힘 해를 벡터 꼴로 (p.2).  접촉 c 에서 법선 성분만 쓰고 **접선 성분은 버린다** (*"we discard the tangential terms in Eq. (1)"* p.3).
- **접촉점 위치는 구 표면에 묶지 않는다** — 현재 변형된 위치를 쓴다 (그림 2 캡션 · p.2: *"considering the current positions of contact points as in Fig. 2, without having to resort to a spherical approximation"*).
- ★ **왜 반무한인가 (원문 논거)**: *"there is no theoretical justification for choosing a solution based on a spherical boundary condition for dense packings, where that boundary may be a very complicated set of free surfaces between contacts. In this work, we therefore simply consider the solution for a point force on an infinite half-space, arguing that the dense packing more closely resembles this situation than that of an isolated sphere."* (p.2 · `txt_p2_half_space_rationale_spherical_bc.png`).
- 무한 공간 (full-space) 해는 ν = 0.5 에서 앞 인자만 바뀐다 (γ = 0.5) → *"We therefore let γ be an adjustable parameter in order to account empirically for the geometry."* (p.2).

### 4-3. ★ 비교한 다섯 정식화 (원문 이름 그대로 · p.2 §IV · `txt_p2_models_list_gamma_1p19.png`)

| 원문 이름 | δ_{k→c} 의 출처 | 자유값 | Rtop |
|---|---|---|---|
| **Independent contacts** | 없음 (binary · 변형 안 되는 겹치는 구 [2] + Hertz) | 0 | 0.43 |
| **Point force on sphere** | Bondareva [15] 의 구 위 점힘 해 — [15] 식 (7) · (8) 의 반지름 성분 | 0 | 0.44 |
| **Sphere to sphere** | Gonzalez & Cuitiño [14] 의 구–구 접촉 [16 Zhupanska] 근사 — [14] 식 (3) | 0 | 0.70 |
| **Elastic half-space** | 식 (1), **γ = 1** | 0 | 0.80 |
| **MC-DEM** | 식 (1), **γ ≈ 1.19** (Rtop = 1 에 맞춤) | **1** | 1.00 |

- 원문 관계: *"If the contacts k and c are restricted to be exactly on the surface of a nondeformable sphere, then for ν = 0.5 (and only that case) the half-space solution is the same as in Ref. [14]"* (p.2) · *"when ν = 0.5, the only difference with the sphere-to-sphere solution is that contact points are applied at the location of the deformed grain surface, rather than being projected on a sphere"* (p.2) → 0.70 → 0.80 의 차이 = 접촉점을 구 위에 투영하느냐 · *"this confirms that even slight surface deformations are important to accurately reproduce the experimental measures"* (p.5).
- 선형 스프링은 시험하지 않았다 — *"Implementing a linear spring model would make the match between numerics and experiments even less accurate, due to the lack of nonlinear stiffening at the contact level [1]."* (p.4 · 실행 결과 아님).

### 4-4. ★ 계산 순서 · 새 접촉 · 접촉 위치 · 관성 · 비용 (p.2–3 · `txt_p2_p3_new_contacts_inertia_cost_ozn.png`)

1. 매 시간 스텝마다 Σ_k δ_{k→c} 를 **접촉점에서** + **가장 가까운 이웃 방향의 알 표면에서** 계산 (그림 1(b)).
2. 표면 변형으로 두 알이 겹치게 되면 **새 접촉** 생성 — 처음 힘 0 (표면이 막 닿음) → 식 (1) 의 교차 영향도 0 → *"the creation of new contacts is a continuous process"* · *"which the basic DEM model is unable to achieve"*.
3. **접촉 위치** = 두 표면 위치의 평균 (같은 E 면 변형이 두 알에 반반 [18 Landau–Lifshitz]) → 반지름이 접촉마다 달라짐 → 기하 토크 f_t × r 가 생김 (*"handled at no additional cost"*).
4. **관성 = 구의 관성 그대로** — *"recomputing the inertia matrix of each grain using the surface deformations would be very costly, so we keep the inertia of a sphere"* · 접촉이 고르게 퍼져 있으면 등방이라는 가정.
5. **비용** = *"only the δ_{k→c} computations themselves significantly add to the simulation cost as O(ZN)"*.
- ⚠ **반복 · 자기 일관**: 원문에 없다 — F_k 가 같은 스텝의 힘인지 앞 스텝의 힘인지, 식 (1) 을 스텝 안에서 수렴시키는지 [미확인] (코드 [23] 를 보면 정해짐).

### 4-5. 실험 대조 지표 (p.3–4) — §3-3 정의 참조

- ★ **맞춘 지표 1 개 (Rtop) + 점검 지표 셋 (errf · errZ · bhat)** 의 구조.  점검 셋도 같은 실험 · 같은 침대에서 나온다 (독립 자료 아님).
- 약한 힘 문턱 τ 는 **실험 해상도 어림**으로 쓴다 (계산 쪽 약한 접촉을 실험이 못 보는 만큼 지운 뒤 Z 를 견줌).

### 4-6. ★ 이 묶음의 네 질문 (원문 문장과 위치)

- **(i) DEM (단단한 구 · 점접촉) 의 한계 문장**:
  *"The conventional DEM approach [1] assumes that all contact forces are binary, i.e., independent of forces acting elsewhere on a particle. This is not rigorously true, since the deformation of a particle at a contact generates strain that propagates internally, thereby correlating with deformations at other contacts on the same particle."* (p.1 §II) ·
  *"The binary assumption avoids computational complexity and makes conventional DEM feasible."* (p.1) ·
  *"Without correlation between contacts, this method is similar in spirit to a mean-field approach and provides only a first-order description of the granular assembly properties."* (p.1) ·
  *"The situation is different in dense granular packings near or above jamming."* (p.1) ·
  *"two key effects that are not taken into account in traditional DEM: (i) shape deformations induce the formation of new contacts; (ii) every contact force is affected by other contact forces in its vicinity."* (p.1 §I) ·
  *"getting quantitative agreement between experimental results and DEM simulations is often a challenge"* (p.1) ·
  *"The traditional DEM implementation with independent contacts clearly fails to reproduce the measurements."* (p.4) ·
  *"Unlike the standard DEM, where spheres are not deformable, the radius now effectively changes per contact."* (p.3).
  수치 = Rtop 0.43 · errf 3.39 N · 판 힘 *"halved"* (p.5).  ⚠ 믿을 수 있는 겹침 · 변형률 **상한은 적지 않았다**.
- **(ii) 입자 변형 · 큰 변형을 넣기 어려운 이유와 우회 · 비용**: 우회 = **FEM 대신 해석 선형 탄성** (*"our method does not involve finite-element method (FEM) calculations. Particle shape deformations are computed with analytic linear elasticity calculations."* p.1) · 정확한 경계 조건은 *"very complicated and any solution would need to be updated at every simulation step"* (p.5) → γ 로 대신 · 관성 행렬 재계산은 *"very costly"* → 구 관성 유지 (p.3) · 비용 O(ZN).  **소성은 다루지 않는다** (탄성 알 · 소성은 일반 DEM 덧붙임 목록에만 p.1).
- **(iii) 2D / 3D**: 실험 · 계산 모두 **3D** (*"full 3D scans"* · *"contact force distributions in full 3D"*).  2D 결과 · 2D → 3D 전이에 대한 말 **없음**.
- **(iv) 압력을 뺄 때**: 가압 · 탈압 가지를 **따로** 다룬다 (*"We explicitly separate loading and unloading phases as some hysteresis is observed, which the simulations also reproduce."* p.3) · errf 가 탈압까지 셈한다 · 그림 4 = 탈압 가지 · 그림 6 = *"the scaling for the simulations presents some curvature in the unloading phase, which does not show up in the experimental data"* (원인 후보 = Coulomb 마찰 가정 · p.5).  되돌아옴 · 잔류 변형 **값 없음**.

### 4-7. 저자 한계 · 미래 (원문 그대로 · p.5–6 · `txt_p5_discussion_gamma_boundary_nu_lt_0p5_nu0.png` · `txt_p5_p6_conclusion_validity_soft_particles_gamma_z_phi.png`)

- *"Ideally, γ should be replaced by a correct accounting for the boundary conditions within the packing, but this is very complicated and any solution would need to be updated at every simulation step."* (p.5)
- *"replacing the complex boundaries within the packing with a functional dependency on statistics at the grain level [22] would be an interesting option"* (p.5)
- *"Future models also need to account for lower Poisson's ratios ν < 0.5."* · ν = 0 직교 접촉 문제 (p.5)
- *"The full extent of the validity of this model is, however, an open question. In particular, we have only compared our simulations to experiments on soft particles."* (p.6)
- *"Although Eq. (1) does not depend on the Young's modulus, which appears both in the force in the numerator and in the denominator, it may be that MC-DEM becomes less relevant with harder materials, except perhaps close to jamming, where a proper accounting for the creation of new contacts is likely to matter most."* (p.6)
- *"Perhaps more importantly, the empirical parameter γ in Eq. (1) may itself depend on other microstructural parameters, like the number of contacts per grain Z and the packing fraction φ, which are likely to affect the quality of the elastic half-space approximation."* (p.6)
- 마찰: *"It is likely that friction between immersed hydrogel particles is not Coulombian."* (p.3) · 큰 μ 에서는 접선 힘에도 다른 접촉의 기여를 비슷한 식으로 더할 수 있다 [17] (p.3).

### 4-8. 기법 미니 용어집

- **binary / non-binary**: 접촉 하나의 힘을 그 쌍의 겹침만으로 정하면 binary.  non-binary (= multi-contact) 는 같은 알의 다른 접촉이 이 접촉을 바꾼다.
- **반무한 탄성체 점힘 해 (Boussinesq)**: 평평한 탄성 반공간 표면에 수직 점힘을 줄 때의 변위장.  이 논문은 조밀 침대의 알 하나를 구보다 반공간에 가깝다고 보고 이 해를 쓴다.
- **γ (prefactor)**: 식 (1) 앞의 무차원 수.  1 = 반무한 · 0.5 = (ν 0.5) 무한 공간 · 1.19 = 맞춤.
- **Rtop · errf · errZ · bhat · τ**: §3-3.
- **Bhattacharyya distance**: 두 분포 p · q 의 겹침 B = ∫√(pq) 로 d = −log B (0 = 같음).
- **'MC-strain' / 'MC-stress'**: Giannis 2021 이 붙인 이름 (각각 이 논문 · Giannis 의 응력 기반 모형).  이 논문 자신의 이름은 **MC-DEM**.

## 5. Figure set ★ (그림 6 + 표 1 + 식 5 + 근거 글 16 = 28 장)

| Fig | 무엇을 보여주나 | 우리가 쓸 점 |
|---|---|---|
| **1** (`fig_1.png`) | (a) 보통 DEM: 접촉 독립 F_c = f(δ_c) · 변형 안 되는 구 / (b) 제안: F_c = f(δ_c, δ_i, δ_j, δ_k, δ_l) · 표면 변형이 새 접촉을 만듦 / (c) 접촉 c 에 이웃 접촉 넷의 변위가 더해짐 | non-binary 축 설명 한 장 |
| **2** (`fig_2.png`) | 식 (1) 기하: n_c · n_k (안쪽 법선) · u_kc · u_ck · d_kc · 접촉점이 구 표면에 묶이지 않음 | 식 (1) 구현 · 단위 시험 기하 |
| **3** ★★ (`fig_3.png`) | 판 힘 F [N] vs Δ [mm] 0–25 · 실험 + 다섯 모형 · 가압/탈압 고리 · Rtop 표지 | binary 0.43 · 결합 0.70–1.00 (§3-4 (a)) |
| **4** ★ (`fig_4.png`) | Δ 18 mm 탈압 가지 p(f) · 실험 + 다섯 모형 | binary = 약한 힘 과다 · 꼬리 없음 (§3-4 (b)) |
| **5** ★ (`fig_5.png`) | 문턱 뒤 알당 접촉 수 Z vs Δ · 모형별 다섯 패널 | Z 3.4 → 9.0 (실험) · errZ 재현 (§3-4 (c)) |
| **6** ★ (`fig_6.png` · 손으로 다시 자름) | F − F_min vs ⟨f − f_min⟩⟨Z⟩⟨φ⟩⟨b⟩ · 실험 · MC-DEM (+5) · 고전 (+10) | 판 힘 ↔ 미시량 비례 점검 (§3-4 (d)) |
| **표 I** ★★ (`tab_1.png`) | 다섯 모형 × Rtop · errf · errZ · bhat · τ | §3-3 |

### 5-1. 크롭 색인 — `litdb/figures/brodu2015_multiple_contact_dem_dense_granular/`

- 그림 · 표 (7): `fig_1` – `fig_5` (도구 그대로 · 열어 확인) · `fig_6` (도구 크롭이 위의 식 (2) 를 삼킴 → 300 dpi 벡터 재렌더 · recrop) · `tab_1` (도구가 로마 숫자 'TABLE I' 를 못 잡음 → 400 dpi 손 크롭 · 캡션 문단 포함).
- 식 (5): `eq_01_cross_contact_displacement_point_force_half_space` (식 (1)) · `eq_02_top_force_microscopic_scaling` (식 (2)) · `eq_unnumbered_sIII_multicontact_hertz_law_in_text` (F ∝ (δ_c + Σδ_{k→c})^{3/2}) · `eq_unnumbered_sV_bhattacharyya_distance_in_text` (d · B · D) · `eq_unnumbered_sVI_packing_stress_tensor_in_text` (σ = 1/V Σ b_c ⊗ f_c · ½Zφ).
- 근거 글 (16): `txt_p1_abstract_mc_dem_full_3d_13pc` · `txt_p1_two_key_effects_no_fem_analytic_elasticity` · `txt_p1_binary_assumption_mean_field_dense_jamming` · `txt_p2_half_space_rationale_spherical_bc` · `txt_p2_gamma_full_space_0p5_half_space_1_adjustable` · `txt_p2_models_list_gamma_1p19` · `txt_p2_p3_new_contacts_inertia_cost_ozn` · `txt_p3_experiment_514_hydrogel_20_cycles_13p4pc_3d_forces` · `txt_p3_e_23p3kpa_inflation_cor_mu_0p03_saturated_friction` · `txt_p3_rtop_errf_definitions` · `txt_p4_fig4_weak_forces_errz_tau_4mn_z_6p4` · `txt_p4_p5_independent_fails_linear_spring_gc_vs_half_space` · `txt_p5_scaling_slope_same_more_hysteresis_friction` · `txt_p5_discussion_gamma_boundary_nu_lt_0p5_nu0` · `txt_p5_p6_conclusion_validity_soft_particles_gamma_z_phi` · `txt_p6_source_code_available_ref23`.
- 판독: `digitized.csv` (1,498 행 · figures.json 'digitized' 에 보정 눈금 · 점검).

## 6. Post-processing ★

- **계산한 것**: 판 힘 (가압 · 탈압 · 모든 Δ) · 접촉력 분포 p(f) (압축 수준별 · 그림은 Δ 18 mm 탈압) · 알당 접촉 수 Z (문턱 τ 뒤) · 판 힘 ↔ ⟨f⟩⟨Z⟩⟨φ⟩⟨b⟩ (φ = 벽에서 알 지름 하나 떨어진 안쪽 부피 분율 · 그림 6 캡션) · 지표 넷.
- **계산하지 않은 것**: 기공률 · 상대 밀도 · 응력 (Pa) · 접촉 겹침 δ 의 분포 · 힘 사슬 · 직물 텐서 · 알 모양 (계산상 구 + 접촉별 반지름) · 수송 · Heckel · 시드 산포 · 계산 시간.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` · `contact_models_layer_map.md` (우리 수치는 CLAUDE.md · 정본 카드가 적은 출처를 그 자리에)

### 7-1. 층위 판정 — 접촉 힘-변위 법칙 층의 **non-binary 축 · 변위 기반**

| 층위 | 이 논문 | 근거 |
|---|---|---|
| (1) 접촉 힘-변위 법칙 | ✅ 여기 — 탄성 non-binary (겹침에 이웃 접촉 변위를 더함) | 식 (1) · 본문 Hertz 식 |
| (2) 접촉 면적 소성 | ✗ | 탄성만 |
| (2.5) 다중 이웃 결합 (zunker2024 표 이름) | ✅ (탄성 원거리 결합 · 반무한 해 × γ) | [다른 카드 · comparison §A L739–L742 의 권고 이름] |
| (3) 입자 형상 소성 | ✗ (탄성 표면 변위만 · 새 접촉 판정에 씀 · 관성은 구) | p.2–3 |
| 항복 캡 | ✗ | — |

### 7-2. ★ 같은 축 세 정식화 나란히 (이 카드 = 원문 확인 · 나머지 = [다른 카드])

| | Gonzalez–Cuitiño 2012 | **Brodu 2015 (이 논문 · MC-DEM)** | Giannis 2021 (MC-stress) |
|---|---|---|---|
| 무엇에 더하나 | 접근량 g (g + g_NL) [다른 카드] | **겹침 δ_c + Σ δ_{k→c}** (p.2) | 힘 (β ν A_ij P_ij) [다른 카드] |
| 원거리 해 | 유한 구 [다른 카드] | **반무한 탄성체 점힘** (구 위 해는 '근거 없음' · p.2) | 응력 trace (방위 없음) [다른 카드] |
| 자유값 | 0 [다른 카드] | **γ 1 개** (1.19 · 이론값 1 / 0.5 밖) | β 1 개 [다른 카드] |
| 비용 | O(n̄N_c) + 고정점 반복 [다른 카드 L216] | **O(ZN)** · 반복 [미확인] | O(C) · 2-pass [다른 카드] |
| 다입자 실험 대조 | 없음 [다른 카드 L615] | **있음 (자체 514 알)** · GC 근사도 여기서 시험됨 (Rtop 0.70) | 있음 (Brodu 실험을 다시 씀 · 1921 이봉 침대로 전이) [다른 카드] |
| 단일 구 (Tatara) 대조 | 있음 [다른 카드] | **없음** | 있음 (MC-strain 을 다시 구현해 γ 0.55) [다른 카드] |
| 강성 부호 | 뻣뻣 | **뻣뻣** (Rtop 0.43 → 1.00) | 뻣뻣 |

★ **이 논문이 더하는 것**: (a) 'GC 계열 근사도 다입자 자료로 0.70 까지만' 이라는 **원문 시험 결과** (GC 카드는 그런 시험이 없다고 적었다 — 맞는 말이고, 그 빈칸을 이 논문이 채운다) · (b) γ 가 **같은 식에서 단일 구 (0.55 · Giannis) ↔ 조밀 침대 (1.19 · Brodu · 1.12 Giannis/[49])** 로 두 배 넘게 다르다 [다른 카드 + 원문] — 저자의 *"γ … may itself depend on … Z and … φ"* (p.6) 와 같은 방향의 관찰 (구현 · 경계 (판) · 식 7 옮김 차이로 섞여 있어 **정량 비교는 아님**).

### 7-3. ★ 우리 18× 연화와의 관계 — 부호 · 크기 · 겹침 기하 (판정 없이)

| 축 | 이 논문 (하이드로겔) | 우리 DEM (LPSCl · NCM) [우리 · CLAUDE.md] |
|---|---|---|
| 측정 E 로 binary Hertz 를 돌리면 | **판 힘이 모자란다** (Rtop 0.43 · 너무 무름) | 300 MPa 에서 **덜 압밀** (너무 단단) → E 24 → 1.35 GPa (18× 연화) |
| 빠진 물리 (저자 · 우리 해석) | 같은 알 안 탄성 결합 + 새 접촉 생성 | 재배열 · 입계 미끄럼 · 미세 파괴 · 소성 흐름 (frame [2]) |
| 처방 | 결합 항 추가 (γ) — **E 는 측정값 그대로** | E 를 낮춤 — **측정 물성 자리를 덮어씀** |
| 처방 방향 | **뻣뻣하게** | **무르게** |

- ★ **크기를 정하는 것은 E 가 아니라 겹침 기하**다: 식 (1) 이 E 와 무관하므로 (원문 p.6) 한 접촉쌍의 상대 보정 δ_{k→c}/δ_k ∝ γ√(δ/R) [카드 산술 §14-2].  맞대 선 두 접촉 (ν 0.5 · γ 1.19) 이면 δ/R 0.05 · 0.10 · 0.22 에서 **4.0 · 5.6 · 8.4 %** [카드 산술 · 예시 · 다른 각의 접촉 합은 아님].
- ★ **그래서 우리 침대에 얹을 때의 설계 질문**: 우리 순수 SE DEM 의 ⟨δ⟩/d ≈ 11 % (δ/R ≈ 0.22) 는 **연화된 E (1.35 GPa) 의 겹침**이다 [우리 · CLAUDE.md].  같은 접촉력에서 실제 E (24 GPa) 의 Hertz 겹침은 (1.35/24)^{2/3} ≈ **0.15 배** (δ/d ≈ 1.6 %) [카드 산술].  다접촉 항을 연화된 침대 위에 얹으면 **연화가 만든 겹침에 결합을 계산**하게 된다 → (가) 연화 겹침 기준 · (나) 실제 E 겹침 기준 중 무엇으로 결합을 셀지가 결과 전 등록 칸이 된다 (판정 아님).
- 저자 자신의 단서: *"it may be that MC-DEM becomes less relevant with harder materials, except perhaps close to jamming"* (p.6) — 우리 압밀은 재밍 위 (조밀) 이고 재료는 단단하다.  둘이 반대 방향이라 이 문장만으로는 우리 쪽 크기가 정해지지 않는다.
- 결론 (판정 없이): MC-DEM 은 **우리 18× 연화의 대안이 아니다** (방향 반대 · giannis2021 §7-3 · gonzalez2012 §10.4 와 같은 결론 [다른 카드]) — 대신 **binary 가정이 탄성 조밀 침대에서 판 힘을 2.3 배 틀리게 한다는 정량 사례**로 쓴다.

### 7-4. 항목 대조표

| 항목 | 이 논문 | 우리 [우리 · CLAUDE.md] | 차이 / 이유 |
|---|---|---|---|
| 코드 | 자체 (공개 [23]) | LIGGGHTS | 다름 |
| 기반 법선 법칙 | Hertz (δ^{3/2}) | hooke/hysteresis (Luding) | 다름 |
| 접촉 결합 | **non-binary** (식 (1)) | binary | 우리에게 없는 축 |
| 소성 · 항복 캡 | 없음 | 없음 (DEM) · MPM 은 J2 | — |
| E 취급 | 측정 E (23.3 kPa) 그대로 | E 18× 낮춤 (1.35 GPa) | 처방 자리가 다름 (§7-3) |
| ν | 0.5 로 읽힘 [카드 해석] | DEM 0.3 입력 · DFT 0.360 · MPM 0.49 | MPM 0.49 와 비압축 근처라는 점만 닮음 |
| 마찰 | 0.03 (포화) | (DEM 입력 값 — 이 카드가 확인하지 않음) | 하이드로겔은 거의 마찰 없음 |
| 경계 · 하중 | 일축 **변위 제어** · 20 회 반복 · 최대 13.4 % | 300 MPa **정압 서보** · 한 번 | BC 다름 |
| 변형 | 침대 변형률 ≤ 13.4 % (접촉 겹침 [미확인]) | 순수 SE ⟨δ⟩/d ≈ 11 % (접촉 겹침) | **다른 양** — 같은 칸에 놓지 않는다 (§8 단계 4 행) |
| 기공률 | 0 (보고 없음) | 핵심 관측량 | 전이 불가 |
| 탈압 | 가압/탈압 고리 · 이력 21 % (실험) | DEM 탈압 = 키트 · 언로딩 트랙 | §8 단계 6 |
| 차원 · 알 수 | 3D · 514 | 3D · 수만 | — |
| 재료 | 하이드로겔 (탄성 · 물속) | LPSCl (소성 · 취성) + NCM | 절대값 전이 0 |

### 7-5. Giannis 재구현과의 정합 (같은 실험 · 다른 코드) [다른 카드 giannis2021 L86–L87 · 카드 산술]

| | Brodu (이 논문 · Rtop) | Giannis 그림 11 (판독값 ÷ 실험 555 Pa) |
|---|---|---|
| 고전 (binary Hertz) | **0.43** | 245/555 = **0.44** |
| γ = 1 (반무한) | **0.80** | 455/555 = **0.82** |
| 맞춘 γ | γ 1.19 → **1.00** | γ 1.12 → 525/555 = **0.95** |

→ 두 독립 구현이 binary · γ = 1 에서 **2–3 % 안**으로 같다 [카드 산술] — 이 실험에서 'binary 2.3 배 모자람' 은 한 코드의 인공물이 아니다.  Giannis 의 γ 1.12 가 1.00 에 못 미치는 것은 Brodu 가 1.19 를 쓴 것과 같은 방향.
- 단위 다리 (참고 · 판정 아님): 판 면적을 giannis2021 §4.8 의 514 침대 단면 0.165 × 0.165 m² [다른 카드 L256] 로 두면 이 논문의 최대 판 힘 15.68 N [판독] → **576 Pa** ↔ Giannis 그림 11a 실험 ≈ 555 Pa (+4 %) [카드 산술].  ⚠ 같은 카드의 침대 높이 0.167 m 로는 25 mm 가 15.0 % 이지 13.4 % 가 아니다 (이 논문 기준 높이 ≈ 187 mm [카드 산술 §14-5]) — 판 면적 · 처음 높이 · 변형률 기준은 이 원문에 없어 [미확인] ([8] 필요).

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa (σ_y_eff 46 MPa) / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정하지 않음.  **이 논문의 값은 전부 랩 표준과 다른 재료 (하이드로겔) 의 문헌 값**이다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **맞춘 지표 1 · 점검 지표 3 의 표 구조** (표 I) — 무엇을 맞췄고 (Rtop) 무엇이 점검인지 (errf · errZ · bhat) 를 한 표로 · ★ 분포 일치 지표 **D = −log⟨B⟩** (압축 수준 평균 뒤 로그) · ★ **측정 해상도 문턱 τ** (약한 접촉을 지운 뒤 Z 비교) | 기공 연산자 · 진밀도 0 (기공 보고 없음) · 점검 지표가 맞춘 자료와 같은 침대에서 나옴 (독립 아님) |
| **단계 1** (3D 메모리 · 장 수) | 없음 | 비용 O(ZN) 서술뿐 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현만 바꿔 누르는 힘 비교) | ★ **같은 꼴의 비교 설계 (3D 판)**: 같은 침대 · 같은 E · 같은 마찰에서 **접촉 표현만** 바꿔 판 힘을 견줌 → 탄성 조밀 침대 13.4 % 에서 binary ÷ 결합 = **0.43** (맞춤 기준) · 맞추지 않은 결합끼리 **0.70 ↔ 0.80** (표 I) | 2D 아님 · MPM 아님 · 탄성 알 — '접촉 표현 하나로 판 힘이 2 배 넘게 바뀔 수 있다' 의 크기 자리표로만 |
| **단계 4** (3D 순수 SE · 항복 세기 하나를 실험 기공에 맞춤) | ★ **경고 사례**: 한 스칼라 (γ) 를 한 수 (판 힘) 에 맞추면 같은 수를 움직이는 다른 입력 (E · 'best estimate') 과 **나뉘지 않는다** (MC-DEM 판 힘 ∝ E [카드 산술 §14-4]) — 우리 σ_y 하나를 기공 하나에 맞출 때도 E (MPM 1.53 GPa) 와 엉킴을 결과 전에 적어야 함 | SE · 기공 0 · 랩 표준 (10–13 % · 1.64) 옆에 놓을 숫자 **없음**.  ⚠ '13 %' 끼리 놓지 말 것: 이 논문 13.4 % = **침대 일축 변형률** (판 변위 ÷ 처음 높이 · 기준 ≈ 187 mm [카드 산술]) · 우리 ⟨δ⟩/d ≈ 11 % = **접촉 겹침 ÷ 지름** — 다른 양 |
| **단계 5** (3D 복합 AM + SE) | 없음 (한 재료 · 크기 분포 미기재) | — |
| **단계 6** (탈압 · 되돌아옴) | 탄성 침대의 **가압/탈압 고리** 실측 + 모형 (그림 3) — 고리 넓이 ÷ 가압 일: 실험 **0.21** · MC-DEM 0.16 · binary 0.21 [카드 산술] · 탈압 끝 판 힘 ≈ 0 · 이력 원인 = 마찰 (비 Coulomb 가능) (p.3 · p.5) | 소성 되돌아옴 · 잔류 변형 **0** · 하이드로겔 (탄성) · 우리 언로딩 키트의 값 앵커로 쓰지 않는다 — '탈압 가지를 따로 맞추고 RMS 에 넣는' 보고 꼴만 |
| **단계 7** (형상 · 피복 · 수송) | Z (문턱 뒤) · p(f) · **식 (2) F ∝ ⟨Z⟩⟨φ⟩⟨b⟩⟨f⟩** 의 모형 무관 비례 (기울기 실험 1.12 · MC-DEM 0.99 · 고전 1.04 N per 10⁻³ N m [판독]) — 우리 DEM 침대의 **판 힘 ↔ 접촉 합 응력** 자기 점검 꼴 | 수송 · 피복 0 · Z 정의가 문턱 τ 에 달림 |
| **후보 D0** (지금의 DEM) | ★ **binary 가정의 정량 반례 (탄성판)**: 측정 E 의 binary Hertz 가 판 힘 0.43 · 약한 힘 과다 · 큰 힘 꼬리 없음 · Z 과소 (−0.29) — D0 의 binary 가정이 조밀 영역에서 틀릴 수 있다는 **인용 가능한 수치** | D0 의 문제 (너무 단단 → 연화) 와 **부호가 반대** · 하이드로겔 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A** (MPM · AM 강체 + SE 한 속도장) | 간접: 연속체는 알 안 탄성 결합을 **저절로** 가진다 — MC-DEM 의 γ 가 근사하려는 것 | 탄성 알 다입자 판 힘이 연속체에서 얼마인지 수치 없음 |
| **후보 A′** (MPM · 입자별 속도장) | ★ **검증 표적 후보**: 3D 탄성 다입자 침대 · 접촉마다 힘 · Z · 판 힘 실측 ([8]) — A′ 의 접촉 표현이 binary DEM (0.43) 과 결합 모형 (1.00) 중 어디에 오는지 재는 외부 자료 (U5) | 실험 자료 공개 여부 · 알 크기 · 판 면적 **[미확인]** ([8] 원문 필요 · §12) |
| **후보 B** (입자별 FE · MPFEM · NSCD) | 저자는 FEM 을 **피하려고** 이 방법을 냈다 (*"does not require the use of costly finite-element methods"* p.1) — B 는 γ 를 유도할 기준 계산 자리 (Giannis 도 같은 말 [다른 카드]) | FEM 결과 0 |
| **후보 C** (MDR 류 큰 변형 접촉) | 원거리 탄성 결합 = MDR 이 비운 칸 (zunker partII 의 *"원거리 응력 결합 미고려"* [다른 카드 · comparison §A L748–L750]) 을 채우는 한 방법 (γ 1 개) | 부피 보존 · 소성 0 |
| **후보 C′** (항복 캡 탄소성 + 다접촉 보정) | ★ **다접촉 보정의 변위 기반 원전** — 맞춘 값 1 개 (γ) · 대상 = 판 힘 · 비용 O(ZN) · 원문 식 (1) (분수 범위 주의) · E 무관 → 상대 보정 ∝ γ√(δ/R) | 항복 캡과 결합 0 (탄성 Hertz 위) · 우리 hooke/hysteresis 위 이식 시 이력 가지 충돌 (giannis2021 §7-2 의 가드 ① 과 같은 부류 [다른 카드]) |
| **후보 M0** (균질화 캡 소성) | 없음 | — |
| **U0** (접촉 끈 것과 같은지) | 식 (1) 이 γ 에 비례 → **γ = 0 이면 binary 와 비트 같아야** 한다 [카드 해석] — 다접촉 항을 넣을 때의 영(0) 점검 | 원문에 그 시험 서술 없음 |
| **U1** (입자 하나 압축 · 해상도) | 없음 (단일 입자 대조 없음 — Tatara 는 Giannis · Gonzalez 쪽) | — |
| **U2 · U3 · U4** | 없음 | — |
| **U5** (비슷한 강성 입자 충돌 · 다물체) | ★ 같은 강성 탄성 알 514 개의 3D 다물체 실측 (접촉력 · Z · 판 힘 · 15 사이클 평균) = 다물체 접촉 표현의 외부 시험대 | 자료 접근 [미확인] |
| **U6** (작은 조밀 충전 해상도 수렴) | 없음 | — |
| **조건 R1** (AM 이 움직이고 하중을 나눔) | 없음 (한 재료) | — |
| **조건 R2** (미끄럼 · 분리) | 마찰 = 늘 포화 F_t = μF_n (μ 0.03) — 미끄럼 규칙의 단순화 예 | 분리 · 점착 0 |
| **조건 R3** (SE 입자 경계 기억) | 없음 | — |
| **조건 R4** (탈압 · 되돌아옴) | 가압/탈압 고리 · 탈압 가지 RMS (errf) | 소성 되돌아옴 0 |
| **조건 R5** (맞추는 값은 모델마다 하나) | ✅ 1 개 (γ) — 단 E · μ · 반발 계수는 '최선 추정' 으로 고정 · 맞춘 대상과 점검이 같은 실험 | — |
| **조건 R6** (SE 입자 형상 변형) | **부분** — 해석 선형 탄성으로 표면 변위를 계산해 새 접촉 판정에 씀 · 접촉별 반지름 · 관성은 구 | 소성 형상 변화 0 · 모양 자체를 들고 다니지 않음 |
| **조건 R7** (AM 파괴) | 없음 | — |
| **결과 전 대조 항목** | ① 같은 자료 · 같은 E 에서 접촉 표현만 바꾼 판 힘 비 (binary ÷ 결합) — 이 논문 0.43 (탄성 · 13.4 %) ② 맞춘 지표와 점검 지표를 결과 전에 나눠 적기 ③ 판 힘 ↔ ⟨Z⟩⟨φ⟩⟨b⟩⟨f⟩ 비례 점검 | 값 앵커 아님 (재료 다름) |

## 9. 적용 인사이트 (행동)

- ① **비교 문서 · 두 가리킨 카드의 Brodu 서술을 원문 기준으로 다시 읽을 것** (§13) — 특히 *"세 정식화가 Tatara 를 각자 복원"* · *"O(C²) + 반복"* · *"광탄성"* · *"γ 이론앵커 ν → 0 1"* 은 이 원문으로 서지 않는다.  고치는 일은 그 카드 담당 (이 카드는 고치지 않는다).
- ② **binary 가정의 크기 인용은 이 논문 표 I 로**: "탄성 조밀 3D 침대 (13.4 %) 에서 binary Hertz DEM 은 판 힘의 43 % (Brodu 2015 · 표 I)" — 원문 수치 · 실험 대조 · 두 독립 구현 정합 (§7-5).
- ③ **다접촉 항을 우리 DEM 에 넣는 실험을 등록한다면**: 영 점검 (γ = 0 ≡ binary) · 겹침 기준 (연화 / 실제 E) 칸 · 맞춘 지표 하나 + 점검 지표 (분포 · Z) 를 결과 전에 (§7-3 · §8).
- ④ **[8] (Nat. Commun. 6, 6361) 확보** — 측정법 · 알 크기 · 판 면적 · 자료 공개 여부를 닫는다 (U5 · A′ 검증 표적 여부가 거기서 정해짐).

## 10. 인용 가능 문장 (deck/paper 용 — 표지 그대로)

- "In a dense 3D packing of 514 elastic hydrogel grains compressed to 13.4 % strain, a conventional DEM with independent (binary) Hertz contacts and the measured Young's modulus reproduced only 43 % of the measured top-plate force (Brodu, Dijksman & Behringer, Phys. Rev. E 91, 032201 (2015), Table I)."
- "Brodu et al. state that 'the conventional DEM approach assumes that all contact forces are binary, i.e., independent of forces acting elsewhere on a particle. This is not rigorously true …', and that without such correlations DEM 'provides only a first-order description of the granular assembly properties'."
- "Their multi-contact DEM adds to each overlap the elastic half-space displacement induced by the other contacts of the same grain, scaled by a single empirical prefactor γ (best fit γ ≈ 1.19, fitted to the maximum top-plate force); the authors note that γ 'may itself depend on … the number of contacts per grain Z and the packing fraction φ'."
- (우리 해석 표기 필수) "Because the cross-contact displacement is independent of Young's modulus, the relative size of such a correction is set by contact geometry (∝ γ√(δ/R)), not by stiffness — applied on top of a softened-modulus DEM it would act on softening-inflated overlaps.  **This is our reading, not the authors' claim.**"

## 10-1. 쉽게 말하면

알 하나를 위에서 누르면 옆구리도 부풀어 옆 알을 민다.  보통 DEM 은 이것을 모르고 접촉마다 따로 계산한다.  이 논문은 "옆 접촉이 민 만큼" 을 겹침에 더하는 공식 하나 (식 (1)) 와 조절 손잡이 하나 (γ) 를 붙였고, 물에 잠긴 젤리 공 514 개를 실제로 눌러 잰 힘과 비교했더니 보통 DEM 은 힘을 절반도 못 냈다.  다만 젤리 공은 우리 전해질 가루와 정반대로 무르고 탄성이라, 숫자가 아니라 "따로 계산하면 틀릴 수 있다 · 얼마나 틀리는지 재는 법" 을 가져온다.

## 11. 주의/한계 (over-claim 방지)

**논문 자신의 한계 (저자 명시)** — §4-7.

**우리가 추가로 다는 한계**
- ⚠ **실험이 하나 · 침대가 하나**다.  γ 를 그 실험에 맞췄고 점검 지표도 같은 실험에서 나왔다 → 이 논문 안에는 **독립 예측 시험이 없다** (두 번째 침대 전이는 Giannis 2021 그림 14 [다른 카드]).
- ⚠ **측정법이 이 논문에 없다** ([8] 로 넘김) · 알 크기 · 크기 분포 · 상자 · 판 면적 · 응력 · 온도 · 액체 종류 · E 측정법 **[미확인]**.
- ⚠ **ν = 0.5 는 읽은 값** [카드 해석] · 반발 계수 값 [미확인] · 시간 간격 · 스텝 · 계산 시간 [미확인].
- ⚠ **반복 · 자기 일관 여부 [미확인]** — 원문은 '매 스텝 계산' 만 적는다.
- ⚠ γ 1.19 와 E 23.3 kPa 는 판 힘 한 수로 **나뉘지 않는다** (§3-2 · §14-4).
- ⚠ 그림 5 의 두 가지 중 어느 쪽이 가압인지 **표지 없음** (값은 두 가지 다 적었다).
- ⚠ 판독값은 벡터 경로라 그림 해상도 오차는 없지만, 원 자료의 평균 · 보간 방식은 원문에 없다 — 판독으로 표 I 의 errf · errZ · Rtop 를 재현해 그림 = 표 I 의 원 자료임을 확인했다 (§3-4).
- ⚠ **소재가 배터리가 아니다** — 하이드로겔 (E 23.3 kPa ↔ LPSCl 22–24 GPa [우리] = 10⁶ 배) · 탄성 · 물속 · 마찰 0.03.  옮길 수 있는 것 = 식의 꼴 · 비교 설계 · 지표 정의 · 부호.

## 11-1. [미확인] 목록 (본문 6 쪽 전수에 없음)

1. 3D 접촉력 **측정법** (영상 · 재구성 · 힘 추론) · '광탄성' 여부 — [8] 로 넘김.
2. 알 **크기** · 크기 분포 · 상자 · **판 면적** · 처음 높이 · 변형률의 기준 길이 (25 mm ↔ 13.4 % → 187 mm 는 [카드 산술]).
3. 응력 (Pa) · 압력 — 판 힘 (N) 만 있다.
4. 액체 종류 · 온도 · E 의 측정법과 불확도.
5. 계산의 ν (0.5 로 읽힘 [카드 해석]) · 반발 계수 값 · DEM 의 중력 항.
6. 시간 간격 · 스텝 수 · 계산 시간 · 하드웨어 · **스텝 안 반복 · 자기 일관 여부** (F_k 가 어느 스텝의 힘인지).
7. 그림 5 의 두 가지 중 어느 쪽이 가압인지.
8. 실험 자료 공개 여부 (공개 문장은 코드 [23] 뿐) · 시드 · 앙상블 · 산포.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 원문 서지 | 왜 | 정본 litdb |
|---|---|---|---|
| [8] | N. Brodu, J. A. Dijksman, and R. P. Behringer, Spanning the scales of granular materials through microscopic force imaging, Nat. Commun. 6, 6361 (2015). | 실험의 측정법 · 알 크기 · 판 면적 · 자료 공개 여부 — 이 카드 [미확인] 넷을 닫는다 · 광탄성 여부 확인 | 없음 (grep "Spanning the scales" · "microscopic force imaging" 0 건) |
| [14] | M. Gonzalez and A. Cuitino, A nonlocal contact formulation for confined granular systems, J. Mech. Phys. Solids 60, 333 (2012). | 'Sphere to sphere' 원전 | ✅ `gonzalez2012_nonlocal_contact_confined_granular` |
| [16] | O. Zhupanska, Contact problem for elastic spheres: Applicability of the Hertz theory to non-small contact areas, Int. J. Eng. Sci. 49, 576 (2011). | Hertz 를 큰 접촉면적으로 넓힐 때의 한계 (질문 e · k) | 없음 (gonzalez2012 카드에 언급만) |
| [6] | M. Saadatfar et al., Mapping forces in a 3D elastic assembly of grains, J. Mech. Phys. Solids 60, 55 (2012). | 3D 탄성 알 접촉력 실측 — 다물체 검증 자료 후보 (U5) | 없음 |
| [20] | L. E. Silbert, D. Ertaş, G. S. Grest, T. C. Halsey, and D. Levine, Geometry of frictionless and frictional sphere packings, Phys. Rev. E 65, 031304 (2002). | 마찰 구 침대의 Z (쉴 때 4–5) — 우리 CN 해석 기준 | 없음 (두 카드에 언급만) |
| [22] | M. Clusel, E. Corwin, A. O. N. Siemens, and J. Brujić, A "granocentric" model for random packing of jammed emulsions, Nature 460, 611 (2009). | γ 를 알 단위 통계로 바꾸자는 저자 제안의 근거 | 없음 |
| [15] | V. F. Bondareva, On the effect of an axisymmetric normal loading on an elastic sphere, J. Appl. Math. Mech. 33, 1001 (1969). | 'Point force on sphere' 원전 (성능 낮음 · 우선순위 낮음) | 없음 |
| [1] | S. Luding, Introduction to discrete element methods: Basics of contact force models and how to perform the micro-macro transition to continuum theory, Eur. J. Env. Civil Eng. 12, 785 (2008). | 'binary' DEM 의 기준 서술 · 선형 스프링 비선형 강화 문장의 출처 | 없음 (정본 `luding2008_cohesive_frictional_contact_models` 는 다른 논문 [카드 해석 — 제목 비교]) |

## 13. ★ 가리킨 카드 대조 · 카드 문제 (고치지 않음 — 정독 출력 `batch_71_findings.md` 끝 절에도 같은 목록)

1. **`gonzalez2012_nonlocal_contact_confined_granular` L607 (· L609)**: *"★ 두 계보의 진짜 공통점 = 같은 실험 앵커. 셋 다 Tatara 1989 고무구 … 로 검증한다."* — Brodu 2015 원문 6 쪽에 Tatara · 단일 구 · 고무 **0 건**.  MC-strain 의 Tatara 대조는 Giannis 2021 의 재구현 (γ 0.55) 이다.
2. **`comparison_vs_ours_DEM` §A L763–L766**: *"★ 세 정식화가 같은 실험(Tatara 1989 고무구)을 각자 복원한다"* — 같은 이유로 '각자' 가 원문으로 서지 않는다 (Brodu 는 Tatara 를 쓰지 않음 · MC-strain 쪽 복원은 Giannis 의 γ 0.55 맞춤).  *"구분력은 다입자 · 다배치 예측에 있다"* 는 맞다 — 그리고 그 다입자 시험이 Brodu 표 I 에 있다 (GC 근사 0.70 · γ = 1 0.80).
3. **`gonzalez2012_…` L502 · L592 · L737**: Brodu 의 γ 에 *"이론앵커 있음 (ν→½ 0.5 / ν→0 1)"* — 원문 = γ = 1 은 **반무한 (half-space) 해**, γ = 0.5 는 **ν = 0.5 의 무한 공간 (full-space) 해** (p.2) · ν = 0 에서는 식 (1) 이 직교 접촉에 결합을 **잘못** 준다고 저자가 적음 (p.5).  (giannis2021 L77 · L459 의 같은 말은 [41 Greaves 2011] 출처로 적혀 있어 Giannis 원문의 서술일 수 있다 — Giannis PDF 를 이 세션에서 보지 않아 [미확인] · Brodu 원문의 말은 아니다.)
4. **`gonzalez2012_…` L541 · L591 · `comparison_vs_ours_DEM` L744 · L761** (그리고 후보 표 N-30 '왜' 칸): *"O(C²) + 반복"* — 원문 = **O(ZN)** (p.3) · 'iterat' **0 건**.  giannis2021 L144–L146 · L458 의 *"원리적으로 반복 … Brodu 는 준정적 가정으로 1회 반복만"* 도 Brodu 원문에 없다 (원문의 '준정적' 은 반발 계수를 1 근처로 고른 이유 한 줄뿐 · p.3).
5. **`giannis2021_…` L567 · `gonzalez2012_…` L834 · `comparison_vs_ours_DEM` L767** (그리고 후보 표 '왜' 칸): *"광탄성 하이드로겔 … 실험 데이터 공개 (딸려 있어)"* — 원문에 'photoelastic' **0 건** · 측정법은 [8] 로 넘김 · 공개한 것은 **시뮬레이션 소스 코드** [23] 뿐 (자료 공개 문장 0 건).  [8] 의 실제 측정법은 [미확인].
6. **`giannis2021_…` L135–L140 (§4.2 식 7 옮김)**: 분수 막대가 (3 − 4ν)n_k·n_c − (1 − 2ν)(n_k + u_kc)·n_c 전체 위에 있다 — Brodu 식 (1) 은 (1 − 2ν) 항의 (n_k + u_kc)·n_c ÷ (1 + n_k·u_kc) 에만 분수를 건다 (원문 인쇄 · §14-1).  Giannis 원문 식 7 의 인쇄가 어떤지는 [미확인] — 카드 옮김의 문제인지 Giannis 원문의 문제인지 가리지 못했다.
- (관찰 · 문제 아님) giannis2021 L72 · L274 의 514 하이드로겔 γ **1.12** (*"[49] 가 제안한 값"*) ↔ 이 논문의 맞춤 **1.19** — 출처가 [49] 로 적혀 있어 문제는 아님.  giannis2021 L86 의 그림 11a 판독값은 이 논문 Rtop 과 2–3 % 안으로 정합 (§7-5).

## 14. 🧮 카드 산술 원장 (원문 숫자 · 판독값만으로 · 재현 = 식 그대로)

**14-1. 식 (1) 의 분수 범위 — 대수 점검.**  Boussinesq 반무한 해 (표면 점힘 P, 안쪽 법선 n, 점힘에서 본 위치 r û) 의 성분식 u_x = C[(n·û)û_x − (1−2ν)û_x/(1+n·û)] · u_z = C[(n·û)² + 2(1−ν)] (C = (1+ν)P/(2πEr) · 표준 탄성론 · 원문 [17] §5.4.4 가 출처로 든 해) 를 벡터로 묶으면 u = C[(n·û)û + 2(1−ν)n − (1−2ν)(û − (n·û)n)/(1+n·û)] = C[(n·û)û + (3−4ν)n − (1−2ν)(n+û)/(1+n·û)] (2(1−ν) + (1−2ν) = 3 − 4ν).  → δ_{k→c} = −γ u·n_c 가 **식 (1) 과 같은 꼴 · 분수는 (1−2ν) 항에만**.
**14-2. E 무관 · 상대 크기.**  같은 구 (반지름 R) 두 알: F_k = (4/3)E*√R* δ_k^{3/2}, E* = E/(2(1−ν²)), R* = R/2 → δ_{k→c} = −γ B √(R/2) δ_k^{3/2} / (3π(1−ν) d_kc) (B = 식 (1) 괄호) → **E 가 지워진다** (원문 p.6 문장과 같음) · δ_{k→c}/δ_k ∝ γ√(δ_k/R).  맞대 선 두 접촉 (d_kc = 2R · B = −3 + 2ν): δ_{k→c}/δ_k = γ(3 − 2ν)/(6√2 π(1−ν)) · √(δ_k/R) = **0.150 γ√(δ/R)** (ν 0.5) · 0.135 γ√(δ/R) (ν 0.37).  γ 1.19 · ν 0.5 · δ/R 0.05 / 0.10 / 0.22 → **0.040 / 0.056 / 0.084**.
**14-3. ν = 0 직교 접촉.**  k = 남극 (n_k = +z) · c = 적도 (n_c = −x) · u_kc = (x + z)/√2 → n_k·u = 1/√2 · n_c·u = −1/√2 · n_k·n_c = 0 · (n_k + u)·n_c = −1/√2 → B = −0.5 + 0.4142(1 − 2ν) → **ν 0: −0.086 (≠ 0)** · ν 0.37: −0.392 · ν 0.5: −0.5.  저자의 ν = 0 문장 (p.5) 확인.  맞대 접촉 B = −3 + 2ν < 0 → 앞의 −γ 와 곱해 δ_{k→c} > 0 (겹침 증가 → 뻣뻣).
**14-4. 판 힘 ∝ E (준정적 · 중력 없음).**  식 (1) 이 E 무관 → 유효 겹침이 E 무관 → 모든 접촉 힘 ∝ E · 마찰 F_t = μF_n 도 ∝ E · 중력 없음 (밀도 맞춤) → 변위 제어 평형 배치는 E 와 무관 → 판 힘 ∝ E → Rtop ∝ E.  binary 가 Rtop 1 이 되는 E 배수 = 1/0.426 = **2.35** (판독) · 1/0.43 = 2.33 (표 I).
**14-5. 변형률 기준 길이.**  Δ_max 25 mm (판독 · 마지막 꼭짓점 25.005) ↔ 13.4 % → 25/0.134 = **186.6 mm** · Δ 18 mm → 18/186.6 = **9.6 %**.
**14-6. Rtop · errf · errZ 재현.**  그림 3: Δ 25 mm 끝점 비 6.676/15.678 = 0.426 · 6.862/15.678 = 0.438 · 11.001/15.678 = 0.702 · 12.569/15.678 = 0.802 · 15.747/15.678 = 1.004.  errf = √(mean((F_m − F_e)²)) · 가압 Δ 0–25 (26) + 탈압 Δ 1–24 (24) · 1 mm 선형 보간 → 3.388 · 3.230 · 1.819 · 1.262 · 0.415.  errZ = 그림 5 경로 순서 50 점 짝 RMS → 0.515 · 0.533 · 0.340 · 0.396 · 0.264.
**14-7. 이력 고리.**  ∫₁²⁵ (F_load − F_unload) dΔ (사다리꼴 1 mm · 탈압 가지 끝에 가압 끝점 25 mm 를 붙임) ÷ ∫₀²⁵ F_load dΔ: 실험 25.71/121.38 = 0.212 · MC-DEM 19.36/119.03 = 0.163 · Independent 13.45/62.77 = 0.214 · Point force 14.69/67.47 = 0.218 · Sphere to sphere 17.38/92.09 = 0.189 · Elastic half space 17.37/100.83 = 0.172.
**14-8. 그림 4.**  평균 f = ∫f p df / ∫p df (그려진 범위) · d = −ln ∫√(p q) df (모형 · 실험의 공통 f 범위 · 600 점 선형 보간): Independent 0.130 · Point 0.110 · S-S 0.055 · Half 0.046 · MC 0.041.
**14-9. 그림 6 기울기.**  x 에서 이동 (5 · 10) 을 빼고 최소제곱: 실험 1.120 / 1.122 · MC-DEM 0.994 / 0.930 · 고전 1.041 / 0.974 (가압 / 탈압) · MC-DEM 가압 ÷ 실험 = 0.887 (−11 %) · 고전 0.929 (−7 %).
**14-10. Giannis 그림 11a 정합.**  [다른 카드 giannis2021 L86–L87 판독값] 245/555 = 0.441 · 455/555 = 0.820 · 400/555 = 0.721 (MC-stress β 1) · 525/555 = 0.946 (MC-strain γ 1.12).
**14-11. 우리 겹침의 실제 E 환산.**  Hertz 같은 접촉력에서 δ ∝ (1/E*)^{2/3} → (1.35/24)^{2/3} = **0.147** → ⟨δ⟩/d 11 % → ≈ 1.6 % [우리 값 = CLAUDE.md · ν 같다고 둠].

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)

- 본문 6 쪽을 글자 층 (PyMuPDF) + 쪽 렌더 (100 dpi 전 쪽 · 식 (1) 300 dpi) + 벡터 경로로 읽음.  서지 = PDF 1 쪽 (머리글 *"PHYSICAL REVIEW E 91, 032201 (2015)"* · 제목 · 저자 셋 · 소속 셋 · 이력 · 초록 · DOI · PACS · © 줄 · *"1539-3755/2015/91(3)/032201(6)"*).  PDF 문서 정보의 제목 · 저자 칸은 비어 있음 (creator *"LaTeX with hyperref package"*).
- 글자 층 낱말 점검: 'Tatara' 0 · 'photoelast' 0 · 'birefring' 0 · 'iterat' 0 · 'rubber' 0 · 'glass' 0 · 'LIGGGHTS' 0 · 'Poisson' 3 · '1.19' 1 · '23.3' 2 · '13.4' 2.
- 식 (1) 의 분수 범위: 글자 층 줄 상자 (분모 *"1 + n_k · u_kc"* 가 x 207.3–253.4 pt = (n_k + u_kc)·n_c 아래에만) + 300 dpi 렌더로 확인.
- 그림 3–6 은 전부 벡터 (내장 래스터 0) — 눈금선 좌표로 보정 · 범례 획 제거 · 표 I 과 Rtop · errf · errZ 재현으로 판독 확인.  그림 3 가지 = MC-DEM 의 위 가지 − F_min 이 그림 6 범례 'Compression' 과 같음.
- 크롭 28 장 (§5-1) 전부 열어 확인 · 모음 그림 (세션 scratchpad).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (ls-tree · 548 개) + DOI (`PhysRevE.91.032201`) · 제목 낱말 · 제1 저자 "Brodu" · "Dijksman" grep — **이 논문 카드 없음** (giannis2021 · gonzalez2012 에 인용만).  같은 저자 · 같은 해 다른 카드 없음 ([8] Nat. Commun. 2015 카드 없음).

## 🔗 관련 카드
- 이 논문을 가리킨 카드: [`giannis2021_stress_based_multicontact_dem`](giannis2021_stress_based_multicontact_dem.md) ('MC-strain' · §3.2 · §4.2 · §7-7 · L567) · [`gonzalez2012_nonlocal_contact_confined_granular`](gonzalez2012_nonlocal_contact_confined_granular.md) (§10.2 · L502 · L541 · L592 · L607 · L737 · L834) · `comparison_vs_ours_DEM.md` §A (L744 · L757–L767) — 대조 결과 §0-1 · §13.
- 같은 축 (non-binary 접촉): [`varkey2026_multicontact_elastoplastic_dem`](varkey2026_multicontact_elastoplastic_dem.md) (MC-stress + Thornton–Ning · 배터리 DEM) · [`zunker2024_mdr_contact_model_partI`](zunker2024_mdr_contact_model_partI.md) (층 2.5 다중 이웃 결합) · [`zunker2024_bulk_elastic_partII`](zunker2024_bulk_elastic_partII.md) (원거리 결합 미고려 = 이 논문이 채우는 칸).
- 우리 접촉 법칙 원전: [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (hooke/hysteresis).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
