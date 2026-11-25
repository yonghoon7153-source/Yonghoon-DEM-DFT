<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-36 · 정독 77) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 · 두 필수 절 §0-1 · §8) · 같은 계열 MPM 카드 = bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing.md · sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability.md (판독 방법 · 우리 MPM 대조 표의 꼴).
     원문 = 출판본 CMES vol. 31, no. 2, pp. 107–127 (2008) · Tech Science Press · PDF 22 쪽 = 본문 21 쪽 + 빈 쪽 1 (PDF 22 쪽째는 글자 · 그림 · 이미지 0) · 보충 자료 없음 · 표 없음.
     쪽 표기 = PDF 쪽 "p.n" (학술지 쪽 = n + 106 · 필요할 때 "(j.쪽)" 으로 병기).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽 (journal_page 칸 = 학술지 쪽).
     값 표지: [인쇄] = 본문 · 캡션 · 그림 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 303 행 — 그림은 전부 MATLAB 벡터라 화소가 아니라 PDF 그리기 명령의 경로 좌표에서 읽었다 ·
     축 = 주 눈금 위치 ↔ 눈금 글자의 최소제곱 (log 축은 log10) · 꺾은선 꼭짓점 = 그려진 자료점 · 축 사상 점검 = 그림 안 1 · 2 차 기준선의 기울기 2.000 · 1.000 · 2.001 · 1.001 · 1.999 [판독]) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [카드 추론] = 원문 밖으로 넓힌 판단 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug · 줄 병기) ·
     [우리 기록] = 정본 카드 · 비교 문서에 적힌 우리 쪽 값 (출처 줄 병기) · [미확인] = 본문 21 쪽 전수에 없음.
     원문 21 쪽은 글자 층 추출 + 쪽 렌더로 전부 읽었다 (식은 수식 글꼴이라 렌더 크롭에서 옮겼다).  DEM · 입자 (알갱이) 계산 · 압밀 · 소성 · 접촉 · 실험은 없다 — 탄성 neo-Hookean 검증 문제 위의 MPM 수치 해석. -->
# MPM 구현 선택 (기저 함수 · 매끈함 길이 · 경계 처리) 이 오차 · 안정에 주는 영향 — 선형 · 2차 B-spline (+ 경계 수정 B-spline · 열린 균일 매듭) · uGIMP · cpGIMP 를 '조각 상수 함수의 합성곱' 하나로 묶고 (식 31) · 노드 적분 오차 = 합성 중점 O(Δx²) + 도약 (jump) 오차 (입자 폭 > 매끈함 길이면 O(Δx) · 식 40) · 경계 기하 오차 O(h) (최대 h · 3h/2 · 2h · h + l/2) · 1D 주기 막대 · 3D 축 정렬 제조해 (MMS) 수렴 (2 차 ↔ extra (ghost) node Dirichlet 이면 1 차) · uGIMP 안정 지도 (매끈함 길이 ≥ 입자 폭 · l = h 면 CFL ≈1.2) ★ 소성 · 접촉 · 압밀 · 탈압 · 2D 계산 · 실험 없음 — 무차원 탄성 neo-Hookean 동역학 (E 10⁴ · ρ₀ 1) — Steffen · Wallstedt · Guilkey · Kirby · Berzins (CMES 2008)

> slug `steffen2008_mpm_implementation_choices_gimp_bspline_boundary` · DOI `[미확인]` (PDF 에 이 논문의 DOI 가 인쇄되지 않았다 — 원문 안의 DOI 는 인용 논문 Steffen · Kirby · Berzins 2008 IJNME 의 `10.1002/nme.2360` 하나뿐) · type `MPM (수치 해석 · 검증 — Uintah Computational Framework (UCF) 의 명시적 MPM · 기저 넷 (선형 · 2차 B-spline + 경계 수정 B-spline (열린 균일 매듭 · Cox–de Boor) · uGIMP · cpGIMP) · 운동학 경계 처리 (Dirichlet · 대칭 · 주기 · extra node) · 노드 적분 오차 해석 (식 33–42) · 제조해 (MMS · 1D 주기 막대 · 3D 축 정렬 단위 정육면체) 수렴 · 안정 지도 · 실험 없음)` · PDF `421c3148-36._Examination_and_analysis_of_implementation_choices_within_the_material_point_method_MPM.pdf` (22 쪽 = 본문 21 쪽 (학술지 107–127) + 빈 쪽 1 · 글자 층 온전 · 그림 13 장 전부 벡터 · PDF 정보 제목 "main.dvi" · 2008-10-03 dvips → Acrobat Distiller 8.1.0) · digested `2026-11-12` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 시험은 전부 **무차원 탄성 neo-Hookean** (E = 10⁴ · ρ₀ = 1.0 · 길이 1 · 파속 C = √(E/ρ₀) = 100 [카드 산술]) 의 **동역학** (탄성파 반 · 한 주기) 이다 — **LPSCl · NCM 이 아니고 분말 · 입자 층 · 접촉 · 소성 · 압밀도 아니다.  절대값 전이 0 건.**  가져오는 것은 **기저 · 경계 선택이 정하는 수렴 차수와 그 기전 (식 35–41 · p.13)**, **시험 설계 (MMS 두 꼴 · 단일 노드 힘 시험 · 안정 지도)**, **규칙 (매끈함 길이 ≥ 입자 폭 · 경계 기하 오차의 크기)** 와 **저자가 적은 한계**뿐이다.
> ② **2D 계산이 없다** (Fig. 1 · 13 은 그림 설명) · **3D 는 축 정렬 한 꼴** — 저자: *"It is not, however, representative of general material deformations usually found in most realistic engineering scenarios."* (p.16).
> ③ **접촉 · 다물체 · 소성 · 하중 제거가 없다** — 'contact' 2 회 (초록 · p.13 문장) · 'plastic' 1 회 (참고문헌 제목) · 'unload' 0 · DEM · 'discrete element' 0 [카드 전문 검색 · 리가처 처리 뒤].
> ④ 변형 진폭은 작지 않다 — 1D 막대 A = 0.05 면 F = 1 + 2πA cos(…) 가 **0.686–1.314 (±31 %)** · A = 0.02 면 0.874–1.126 [카드 산술 · 식 48] — 그러나 탄성 · 주기 운동이다.
> ⑤ 우리 MPM (MLS-MPM · APIC · 2차 B-spline) 과 **같은 2차 B-spline 기저**를 다루지만 **힘 식 (MLS 대용 기울기 ↔ ∇φ) · 입자 속도 전달 (APIC ↔ FLIP 증분 식 9) 이 다르다** (§7-4) — 수렴 차수는 유추로만 옮긴다.
> ⑥ **판독 원자료**: `litdb/figures/steffen2008_mpm_implementation_choices_gimp_bspline_boundary/digitized.csv` (303 행 — Fig. 6 곡선 국소 중앙값 · 기준선 · Fig. 7 요점 · Fig. 8 · 9 꺾은선 꼭짓점 (그림 위 끝 1 · 10⁻² 로 잘린 마지막 점 = 불안정 표지) · Fig. 10 · 11 · 12 꺾은선 꼭짓점 · 기준선 끝점 · 열 = figure, series, x_name, x, y_name, y, note) · 그림 크롭 **74 장** (그림 13 = 도구 5 중 다시 자름 1 + 손 크롭 8 · 식 41 = 번호 식 (1)–(54) 전부 · 근거 문단 20) — `figures.json`.
>
> **이웃 카드 (링크만)**: [`gritton2017_mpm_chemomechanical_coupling_silicon_anode`](gritton2017_mpm_chemomechanical_coupling_silicon_anode.md) (가리킨 카드 · 이 논문 = 그 ref. [34] · L86 · L91 · L230–235 · L349 · L358 — 같은 Utah 무리 Guilkey · Kirby · Berzins) · [`bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing`](bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing.md) (GIMP 원전 · 이 논문 §3.3 의 출발) · [`sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability`](sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability.md) (uGIMP · cpGIMP · CPDI 2D 비교 · 같은 축 정렬 MMS 의 2D 판) · [`hu2018_mls_mpm_cpic_two_way_rigid_coupling`](hu2018_mls_mpm_cpic_two_way_rigid_coupling.md) (우리 MLS-MPM 이산화의 원전 · 우리 코드 줄 대응) · [`bardenhagen2005_mpm_foam_densification_simulation`](bardenhagen2005_mpm_foam_densification_simulation.md) (이 논문 p.1 이 MPM 성공 사례로 든 발포체 치밀화 · Guilkey 공저) · [`stomakhin2013_mpm_snow_elastoplastic`](stomakhin2013_mpm_snow_elastoplastic.md) ("Steffen et al. 2008" 을 3차 B-spline 의 출처로 인용 — §0-1 대조).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Uintah (UCF) 의 명시적 MPM 에서 **기저 함수 · 매끈함 길이 · 경계 처리** 세 선택이 정하는 오차를 해석 (노드 적분 오차 식 35–41) + 제조해 (MMS) 수렴 시험으로 재면 — 선형 기저는 셀 경계에서 기울기가 끊겨 적분 오차가 O(Δx) 라 1D 막대 (4 PPC) 에서 **16 셀 뒤로 수렴하지 않고 오차가 오히려 ×6.9 커지며** [판독 · Fig. 10], 2차 B-spline 은 **주기 경계 · 경계 수정 B-spline 이면 2 차** (6 PPC · 512 셀 RMS 3.7 × 10⁻⁶ [판독]) 지만 **extra (ghost) 노드에 Dirichlet 을 걸면 경계 기하 오차 때문에 1 차** (이웃 차수 0.90–1.18 [카드 산술 · Fig. 11]) 로 떨어진다; uGIMP 는 **매끈함 길이 l 이 입자 폭보다 작으면** 입자 하나가 기울기 꺾임 둘을 걸쳐 도약 오차가 O(Δx) (식 40) 가 되고 큰 시간 간격에서 불안정해진다 (CFL 0.8 · *"2 PPC … L < h/2, 3 PPC … L < h/3, etc."* · l = h (= 2차 B-spline) 면 CFL ≈1.2 까지 안정 [인쇄 · 판독]).  **갱신 순서는 식 (1)–(10) 으로 인쇄만 하고 순서별 오차 비교는 Wallstedt · Guilkey (2008) 로 넘긴다.**

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 기저 함수 선택과 오차 (질문 f) | 선형 (C⁰) · 2차 B-spline (C¹ · 지지 3h) · uGIMP (C¹ · 지지 2h + l) · cpGIMP 를 **조각 상수 함수의 합성곱** 하나로 (식 19 · 31) — **l = h 면 2차 B-spline · l = 0 이면 선형** (p.10) · 노드 적분 오차 = 중점 O(Δx²) + 도약 C[[f^(p+1)]]Δx^(p+2) (p.11) → 선형 = O(Δx) · 매끈한 기저 = O(Δx²) (입자 폭 < l 일 때) | [인쇄] p.5–8 · p.10–12 · 식 17–41 |
| ② ★ 매끈함 길이 · 셀당 입자 · 시간 간격 (f · U1 · U6) | 단일 노드 시험 (h = 1 · l = 0.1): Δx < l 에서 기울기 ≈ 2.0 · Δx > l 에서 ≈ 1.2 [판독 · 카드 산술 · Fig. 6] · 안정: 매끈함 길이가 입자 폭 근처 · 아래면 불안정 (Fig. 8) · 안정 CFL 끝 ≈0.75 (l = h/8) → ≈0.81 (h/4) → ≈0.85 (h/3) → ≈0.91 (h/2) → ≈1.2 (l = h) [판독 · Fig. 9] · *"stability is more dependent on the smoothing length than the number of particles per cell"* (p.16) · 셀당 입자를 4 → 6 으로 늘리면 오차 바닥이 내려간다 (512 셀에서 1.45 × 10⁻⁴ → 3.7 × 10⁻⁶ = 39 배 [판독 · 카드 산술]) | [인쇄] p.12–13 · p.16–17 · [판독] Fig. 6 · 8 · 9 · 10 |
| ③ ★ 경계 처리 (후보 A′-0 · U4) | Dirichlet = 덮어쓰기 · 경계 가속도 = 0 또는 **식 (30) a_i = (v_i^{k+1} − v_i^k)/Δt** (= 투영 속도를 처방 속도로 돌리는 힘 · **UCF 의 선택**) · 대칭 (마찰 없는 면) = 법선 속도 0 · extra node 는 **경계 맞은편 노드 값의 음수** · 경계 기하 오차 = 최대 **h (선형) · 3h/2 (2차) · 2h (3차) · h + l/2 (uGIMP)** — 전부 O(h) · 주기 · 경계 수정 B-spline · cpGIMP 는 (경계를 격자에 맞춘 문제에서) 피한다 | [인쇄] p.9 · p.13–14 · 식 30 · Fig. 7 · 11 |
| ④ ★ 수치 오차를 재는 법 (f · 단계 2) | **MMS**: 해를 먼저 정하고 체적력을 해석적으로 만든다 (TL 꼴로 만들어야 자유 표면 법선 응력 0) · 1D 주기 막대 (식 47–50) · 3D 축 정렬 (식 51–53) · 오차 = 끝 시각 입자 위치 오차 (식 54) 의 RMS (1D) · 최대 (3D) 를 격자 셀 수에 대해 log–log + 1 · 2 차 기준선 · 단일 노드 상수 응력 시험 (식 42 · 노드 힘은 0 이어야) · ⚠ 고른 입자 간격은 **초수렴**으로 오차를 숨긴다 (Fig. 6 캡션) | [인쇄] p.12–16 · 식 42–54 |
| ⑤ 갱신 순서 (f) | **인쇄만** — 식 (1)–(10): σ(F_p) → 내부력 → 격자 속도 (Forward-Euler) → **갱신된 격자 속도로** ∇v_p · F_p → 입자 속도 = 격자 가속도 증분 (식 9) · 위치 = 갱신된 격자 속도 (식 10) · 엇갈린 중앙 차분 판 (식 11–15) · 순서별 오차 = Bardenhagen (2002) · Wallstedt · Guilkey (2008) 로 넘김 | [인쇄] p.4–5 · p.10 |
| ⑥ 2D → 3D (g) | 1D 해석 · 1D 계산 → 3D 축 정렬 MMS 하나 (UCF) · cpGIMP 2.13 · 2.04 · **1.54** · 주기 B-spline 2.37 · 1.68 · **1.00** (차수가 떨어짐) · 대칭 B-spline 1.47 · 1.04 · 0.91 [카드 산술 · Fig. 12] · 저자: 다차원에서 적분 오차가 더 복잡하거나 셀 넘김 오차가 쌓일 가능성 (*"many more grid crossing events occur than in 1-D"*) | [인쇄] p.16 · p.18–19 · [판독] Fig. 12 |
| ⑦ DEM 한계 · 소성 · 탈압 (k · l · b) | **말 없음 · 계산 없음** — DEM 0 회 · 소성 계산 0 · 하중 제거 0 · 큰 변형의 **수치** 어려움 (셀 넘김 · 적분 오차 · 입자 영역 추적 · 경계 기하) 만 | [인쇄] p.1 · p.3 · p.5 · p.8 · p.13 |
| ⑧ 계산 비용 | [미확인] — 시간 · 기계 · 병렬 수 없음 · 가장 큰 계산 = 3D 64³ 셀 × 64 입자 = **16.8 million** 입자 (= 16,777,216 [카드 산술]) | [인쇄] p.18 |

⛔ **한정어 (떼지 말 것)**: ① 무차원 탄성 neo-Hookean 동역학 (1D ν = 0 · 3D ν = 0.3) — 소성 · 거의 비압축 (ν 0.49) · 준정적 압밀 · 접촉 · 분리 · 하중 제거 없음 ② 결과 값은 벡터 경로 [판독] (원자료 표 없음) ③ 3D = 축 정렬 한 꼴 (입자 영역이 늘 축에 맞아 cpGIMP 에 유리 — 저자 p.18) ④ 2D 계산 없음 ⑤ CFL 의 식 · §6.1 격자 수 · §6.3 Δt · T · 'Max Error' 정의 · RMS 식 · 계산 시간 미인쇄 ⑥ 1D 수렴은 Δt 를 4 × 10⁻⁶ 로 고정 (CFL 0.2 at 512 셀 → 0.0032 at 8 셀 [카드 산술]) — 공간 오차만 본다 ⑦ 우리 MLS-MPM 과 힘 식 · 입자 속도 전달이 다르다.
⇒ **절대값 전이: 0 건.**  전이되는 것은 **기저 · 경계 · 매끈함 길이가 정하는 수렴 차수와 기전**, **MMS · 단일 노드 · 안정 지도의 시험 꼴**, **경계 기하 오차의 크기 (h 단위)** 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-36 의 '왜' 칸)

의도 원문: *"f — MPM 구현 선택 (갱신 순서 · 기저 함수) 의 오차 분석 · gritton2017 이 'MPM 알고리즘은 [34, 38] 대로' 라고 넘긴 자리 (카드 §4-1) → 수치 오차를 어떻게 추정했는가의 원전 후보"* (가리킨 카드 = `gritton2017_mpm_chemomechanical_coupling_silicon_anode` §4-1 · 정본 L86 · L349 · L358 · 후보 표 서지 칸 = "[34] Steffen M, Wallstedt P C, Guilkey J E, Kirby R M and Berzins M 2008 Examination and analysis of implementation choices within the material point method (MPM) Comput. Modeling Eng. Sci. 31 107–27")

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "MPM 구현 선택 … 의 오차 분석" — **기저 함수** 쪽 | **채움** | §3.2–3.3 · §4.1–4.2 · 식 17–41 · Fig. 2–6 · 8–12 — 선형 · 2차 B-spline (+ 경계 수정) · uGIMP · cpGIMP 를 합성곱 하나로 (식 31) · 적분 오차 = 중점 O(Δx²) + 도약 오차 (식 35–41) · 단일 노드 시험 (식 42 · Fig. 6) · 안정 지도 (Fig. 8–9) · 1D · 3D MMS 수렴 (Fig. 10–12).  **조건**: 무차원 탄성 neo-Hookean (E 10⁴ · ρ₀ 1 · 1D ν 0 · 3D ν 0.3) · 동역학 (T = 1/C · 2/C) · 진폭 A 0.02 · 0.05 · 압력 · 압밀 · 소성 · 접촉 없음 |
| — **갱신 순서** 쪽 | **일부** (순서는 인쇄 · 순서별 오차 분석은 **없음**) | 식 (1)–(10) (p.4) — 내부력 (4) 은 시작 시각 F_p 의 응력 · 격자 속도 Forward-Euler (6) · ∇v · F 는 **갱신된 격자 속도**로 (7)–(8) · 입자 속도 = 격자 가속도 증분 (9) · 위치 = 갱신된 격자 속도 (10) · 엇갈린 중앙 차분 판 (11)–(15) · *"the benefits of which are reviewed in detail by Wallstedt and Guilkey (2008)"* (p.5) · §4 머리: *"Bardenhagen (2002) looked at energy conservation errors in MPM, focusing on the effects of the choice of two time-stepping algorithms.  Recently, Wallstedt and Guilkey (2008) expanded on the analysis"* (p.10).  'USL' · 'update stress' 낱말 0 회 · §6 결과 런이 식 (6) 판인지 (11)–(15) 판인지 [미확인] |
| — (덧) **경계 처리** 쪽 (의도에 없던 둘째 축 · 저자는 기저와 나란한 주제로 둔다) | **채움** | §3.4 · §4.3 · 식 30 · Fig. 7 · 10–12 — 경계 기하 오차 O(h) · ghost node Dirichlet → 1 차 · 주기 · 경계 수정 B-spline · cpGIMP → 2 차 |
| "gritton2017 이 'MPM 알고리즘은 [34, 38] 대로' 라고 넘긴 자리 (카드 §4-1)" | **채움** (2008 판 Uintah 알고리즘) · **일부** (2017 계산이 실제로 쓴 선택은 이 원문으로 확정 못 함) | p.2 *"It is within this software environment [UCF] that the implementations of MPM and GIMP under consideration here exist"* · 식 1–16 (p.4–5) · UCF 경계 가속도 = 식 (30) (p.9) · UCF 는 매끈함 길이 l 을 자유 매개변수로 (p.10).  gritton §4-1 이 "적지 않은 것" 으로 둔 다섯 가운데 넷 — 격자 (균일 직교 · p.3) · 가중 함수 식 (17–29) · 갱신 순서 (식 1–10) · 속도 갱신 꼴 (FLIP 증분 · 식 9 [카드 해석]) — 을 **2008 판으로** 채운다.  2017 의 CPDI 판 (그 카드 ref. [38]) 이 같은 순서였는지 · 2017 계산의 셀당 입자 수 (3D) 는 이 원문 밖.  접촉 = 이 원문에도 없음 |
| "→ 수치 오차를 어떻게 추정했는가의 원전 후보" | **일부** | 이 논문의 오차 추정 = MMS 해석해 (식 43–53) · 입자 위치 오차 (식 54) 의 RMS (1D) · 최대 (3D) · 격자 사다리 log–log + 1 · 2 차 기준선 (Fig. 10–12) · 단일 노드 상수 응력 시험 (식 42 · Fig. 6) · 안정 지도 (Fig. 8–9) → **Utah · Uintah 무리의 검증 방법 원전으로는 채움**.  그러나 gritton2017 의 유일한 정량 검증 (1D 확산 해석해 · Fourier 급수 · 그 카드 §3-3) 은 MMS 가 아니고 [34] 를 인용하지 않는다 → **'gritton 자신의 오차 추정' 의 원전은 아니다**.  RMS 의 식 · 3D 'Max Error' 의 정의 [미확인] |

**가리킨 카드 · 같은 원문을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `gritton2017_…` **L86** (메타 표 '구현 기반') | *"Uintah computational framework 의 MPM component … · MPM 알고리즘은 ref. [34, 38] 대로 · 완전 소성 · 선형 등방 경화 모형은 Uintah 에 구현돼 있던 것 (p.10)"* | UCF 의 MPM · GIMP 구현 (p.2) · 식 1–16 · 소성 모형은 이 원문에 없다 (재료 = neo-Hookean 뿐) — 그 줄도 소성을 [34] 에 돌리지 않는다 | **채움** |
| `gritton2017_…` **L91** (저자 원문 인용) | *"The MPM algorithm as described in [34, 38] has been implemented in the Uintah compuational framework [39], and serves as the code base for this work."* | p.2 · p.3–5 (식 1–16) | **채움** |
| `gritton2017_…` **L230–235** (§4-1) | *"알고리즘 세부 · 가중 함수는 ref. [34, 37, 38] 로 넘긴다"* · *"논문이 적지 않은 것: 격자 종류 · 가중 함수의 식 · 셀당 입자 수 (3D) · 응력 갱신 순서 (USF / USL) · 속도 갱신 꼴 (FLIP / PIC) · 접촉"* | 2008 판 UCF: 균일 직교 격자 (p.3) · 가중 식 17–29 · 순서 식 1–10 (USL 꼴 [카드 해석] — 원문은 이름을 쓰지 않는다) · 입자 속도 = FLIP 증분 (식 9) · 접촉 없음 · 이 논문 자신의 3D 시험 = 방향당 4 PPC | **채움** (빈칸 넷을 2008 판으로) — 2017 판의 선택이라는 확정은 아님 |
| `gritton2017_…` **L349 · L358** (§4-8 의사코드) | P2G 다음 *"(운동량 → 격자 속도) [34, 38]"* · *"역학 격자 내부력 · 가속도 · 속도 (ρa = ∇·σ) (40) [34, 38]"* | 식 (2) · 식 (4)–(6) | **채움** |
| 후보 표 `S8_candidates.md` N-36 (서지 칸) | "Steffen M, Wallstedt P C, Guilkey J E, Kirby R M and Berzins M 2008 Examination and analysis of implementation choices within the material point method (MPM) Comput. Modeling Eng. Sci. 31 107–27" | 첫 쪽 머리 *"CMES, vol.31, no.2, pp.107-127, 2008"* · 저자 다섯 · 제목 같음 (대소문자만) | **채움** — 호 (no. 2) 빠짐 · DOI 는 원문에 없음 |
| `stomakhin2013_mpm_snow_elastoplastic` **L64** | *"보간함수: 1D cubic B-spline 의 dyadic product (Steffen et al. 2008)"* + 3차 식 N(x) = ½\|x\|³ − x² + ⅔ … | 이 원문에 **3차 B-spline 식이 없다** — 2차 식 (21) 과 열린 매듭 재귀 (식 22–23) 뿐 · 3차는 경계 수정 그림 (Fig. 3b) 과 기하 오차 *"Cubic B-splines … up to 2h"* (p.13) 에만 | **확인 필요** — 같은 해 같은 제1 저자의 IJNME 논문 (이 논문 참고문헌 *"Steffen, Kirby, Berzins (2008) … Analysis and reduction of quadrature errors in the material point method (MPM)"*) 일 수 있다 · stomakhin 원문 참고문헌과 대조 전 [미확인] |
| `bardenhagen2004_…` **L293 · L430** [그 카드 산술] | *"l_p = L/2 ⇒ 2차 B-spline"* | p.10 *"Choosing l = h would give quadratic B-spline basis functions"* + p.8 *"lp here refers to the full particle width, and not the half-width as used in the original GIMP formulation"* (반폭 L/2 = 전폭 h) | **채움** (그 카드의 산술이 원문 인쇄로 확인된다) |
| `bardenhagen2004_…` **L595** (용어집) | *"uGIMP · cpGIMP (뒤 문헌의 이름 · sadeghirad2011 …)"* | 이 2008 원문 p.8 이 **standard GIMP · uGIMP · cpGIMP** 셋을 이미 정의 | **일부** (오류 아님 — 정본 안에서 가장 이른 정의 자리가 이 카드) |
| `comparison_vs_ours_DEM.md` **L3035** ([Bardenhagen04] 블록) | *"이름 대응 (카드 판독): 예제의 'GIMP' (폭 고정) = [Sadeghirad11] 의 uGIMP · 'Finite GIMP' (폭 추적) = 1D 의 cpGIMP"* | p.8: 폭 고정 = **standard GIMP** (l_p = l_p⁰ · 입자마다) — 처음 입자가 고르면 uGIMP 와 같다 · 1D cpGIMP = l_p 를 시간 갱신된 V_p 로 | **채움** (한정: 폭 고정의 이름은 standard GIMP · uGIMP 는 '모든 입자 한 l') |
| `sadeghirad2011_…` **L109** | *"Using the cpGIMP, Wallstedt and Guilkey [23] demonstrated that the USL scheme performs dramatically better than an alternative 'update stress first (USF)' scheme"* | 이 원문은 시간 전진 비교를 Wallstedt · Guilkey (2008) 로 넘긴다 (p.5 · p.10) — 충돌 없음 | **채움** (갱신 순서 분석의 원전 = W&G 2008 · §12 · 정독 n 후보) |

⇒ **의도 대조 결과: 일부** — 기저 함수 (와 경계 처리) 의 오차 분석 · Uintah (2008 판) 알고리즘 기술은 **채움**; 갱신 순서는 순서만 인쇄하고 **순서별 오차 분석은 없음** (Bardenhagen 2002 · Wallstedt · Guilkey 2008 로 넘김); '수치 오차 추정의 원전' 은 **Uintah 무리의 MMS 검증 방법으로서는 채움, gritton2017 자신의 1D 확산 검증의 원전은 아님**.  가리킨 카드 (gritton2017) 의 2 차 인용은 원문과 맞는다.

---

## 1. 한 줄 요약
MPM 을 구현할 때 고르는 것 — **격자 기저 함수** (선형 · 2차 B-spline · 경계 수정 B-spline · uGIMP · cpGIMP), **GIMP 의 매끈함 길이**, **운동학 경계 처리** (Dirichlet · 대칭 · 주기 · extra node) — 를 하나의 틀 (조각 상수 함수의 합성곱 · 노드 적분 오차) 로 분석하고, 1D 주기 막대와 3D 축 정렬 정육면체의 **제조해 (MMS)** 로 수렴 차수 · 안정 한계를 잰다.
매끈한 기저는 적분 오차를 1 차 → 2 차로 올리지만 **매끈함 길이가 입자 폭보다 짧으면 다시 1 차 + 불안정**, 넓은 기저는 **경계에서 격자가 보는 물체가 h 단위로 번져** extra node 에 Dirichlet 을 걸면 1 차로 떨어진다 — 주기 경계 · 경계 수정 B-spline · cpGIMP 가 그것을 피한다.
저자의 요약: *"Two of the design choices which have significant impact on error properties of the method are which grid basis functions to use and how to implement boundary conditions."* (p.19).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **M. Steffen** ¹ · **P. C. Wallstedt** ² · **J. E. Guilkey** ²,³ · **R. M. Kirby** ¹ · **M. Berzins** ¹ — ¹ School of Computing, University of Utah · ² Department of Mechanical Engineering, University of Utah · ³ 교신 (Corresponding Author) · 전자우편 {msteffen, kirby, berzins}@cs.utah.edu · {philip.wallstedt, james.guilkey}@utah.edu | *CMES* (Computer Modeling in Engineering & Sciences) **31 (2) 107–127 (2008)** · © 2008 Tech Science Press | [미확인] (원문에 인쇄 없음) | 무차원 탄성 neo-Hookean 검증 재료 (E 10⁴ · ρ₀ 1 · ν 0 (1D) · 0.3 (3D)) — 실제 재료 없음 | 수치 해석 (노드 적분 오차) + 수치 시험 (MMS 수렴 · 안정 지도) · Uintah (UCF) 의 MPM · GIMP 구현 |

- **1저자 메모 (후보 표) 와의 대조**: 저자 다섯 · 제목 · 학술지 · 권 31 · 쪽 107–127 · 2008 — **같다**.  덧붙임 ① 호 = **2** (첫 쪽 머리) ② DOI · 접수 · 게재 날짜는 원문에 없다 ③ 교신 = Guilkey ④ 키워드 *Material Point Method, GIMP, Meshfree Methods, Meshless Methods, Particle Methods, Smoothed Particle Hydrodynamics, Quadrature* ⑤ 연구비 = 미국 DOE · C-SAFE (Center for the Simulation of Accidental Fires and Explosions) grant **W-7405-ENG-48** (p.20).
- **글의 꼴**: 1 Introduction (p.1–2) → 2 Background (p.2–3) → 3 Overview of MPM (3.1 표준 MPM · 3.2 B-spline MPM · 3.3 GIMP · 3.4 운동학 경계 (3.4.1 전통 MPM · 3.4.2 GIMP · B-spline)) (p.3–9) → 4 Analysis and Interpretation (4.1 GIMP ↔ B-spline · 4.2 매끈함 길이 의존 적분 오차 · 4.3 경계 처리의 영향) (p.9–14) → 5 Test Problem Development (5.1 MMS · 5.2 1D 주기 막대 · 5.3 단위 정육면체 축 정렬 변위) (p.14–16) → 6 Results (6.1 1D 매끈함 길이 · 6.2 1D 공간 수렴 · 6.3 다차원 MMS 검증) (p.16–19) → 7 Summary (p.19) → 감사 · 참고문헌 33 건 (저자–연도 꼴 · p.20–21).  그림 13 · **표 0** · 번호 식 (1)–(54).
- **그룹 맥락**: C-SAFE 가 금속 용기 + 폭약 + 화재 (가열 · 점화 · 파열) 계산을 위해 만든 병렬 · AMR 플랫폼 UCF 안의 MPM · GIMP (p.1–2) — 가리킨 카드 gritton2017 (Guilkey · Kirby · Berzins 공저 · Uintah 위 CPDI) 의 9 년 앞 판이다.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 알고리즘 한 걸음 (§3.1 · 식 1–16 · p.4–5 · `eq_01_02_…` – `eq_16_…`)
| 단계 | 식 (인쇄) | 뜻 · 덧붙임 | 표지 · 쪽 |
|---|---|---|---|
| P2G 질량 | m_i = Σ_p φ_ip m_p (1) | **덩어리 (lumped) 질량** — Sulsky · Kaul 2004 의 일관 질량 M_ij = Σ_p φ_ip φ_jp m_p 의 덩어리 판 | [인쇄] p.4 |
| P2G 속도 | v_i = (Σ_p φ_ip m_p v_p)/m_i (2) | φ_ip = φ_i(x_p) | [인쇄] p.4 |
| 응력 | σ_p = σ(F_p) (3) | 이 논문 = neo-Hookean (식 46) | [인쇄] p.4 |
| 내부력 | f_i^int = −Σ_p ∇φ_ip · σ_p V_p (4) | V_p = det(F_p) V_p⁰ (변형된 입자 영역 부피) | [인쇄] p.4 |
| 가속도 | a_i = (f_i^int + f_i^ext)/m_i (5) | — | [인쇄] p.4 |
| 격자 속도 | v_i^{k+1} = v_i^k + a_i Δt (6) | 명시 **Forward-Euler** (원래 MPM 알고리즘) · 암시 판도 있다 (Guilkey · Weiss 2003 · Sulsky · Kaul 2004 · Love · Sulsky 2006b) | [인쇄] p.4 |
| 입자 속도 기울기 | ∇v_p^{k+1} = Σ_i ∇φ_ip v_i^{k+1} (7) | **갱신된** 격자 속도로 | [인쇄] p.4 |
| 변형 경사 | F_p^{k+1} = (I + ∇v_p^{k+1} Δt) F_p^k (8) | 다음 걸음의 응력 (3) 은 이 F 로 → 'F (응력) 를 마지막에' 꼴 [카드 해석 — USL 이름 미사용] | [인쇄] p.4 |
| 입자 속도 | v_p^{k+1} = v_p^k + Σ_i φ_ip a_i Δt (9) | 격자 **가속도 증분** (FLIP 꼴 [카드 해석]) | [인쇄] p.4 |
| 입자 위치 | x_p^{k+1} = x_p^k + Σ_i φ_ip v_i^{k+1} Δt (10) | 갱신된 격자 속도 | [인쇄] p.4 |
| 엇갈린 중앙 차분 | (11)–(15) — 입자 속도를 반 걸음 앞 (v_p^{−1/2}) 에서 시작하면 같은 절차가 v^{k+1/2} 판이 된다 | 비선형 FE 코드의 흔한 방법 (Belytschko 외 2000) · MPM 에서는 Sulsky 외 2007 이 씀 · *"the benefits of which are reviewed in detail by Wallstedt and Guilkey (2008)"* | [인쇄] p.4–5 |
| 외력 | 격자에 직접 (중력 f_i^ext = m_i g) 또는 입자 외력을 투영 f_i^ext = Σ_p φ_ip f_p^ext (16) | 움직이는 표면 견인력 = '표면' 입자 + (16) · 경계 노드를 움직여 경계 힘을 따라가는 것도 가능하나 *"implementing this for complex geometries in multiple dimensions is not trivial"* | [인쇄] p.5 |
| 격자 | 균일 직교 격자가 *"almost always"* — 이웃 탐색 비용을 없앤다 | 배경 격자는 원리상 어떤 꼴이든 된다 | [인쇄] p.2–3 |

⚠ §6 의 결과 런이 식 (6) 판인지 엇갈린 (11)–(15) 판인지 · 경계 가속도를 0 으로 뒀는지 식 (30) 인지는 런마다 적혀 있지 않다 (UCF 기본 = 식 30 · p.9) [미확인].

### 3-2. ★ 기저 함수 가족 (§3.2–3.3 · §4.1 · 식 17–32 · Fig. 2–4 · p.5–8 · p.10 · `eq_17_…` – `eq_32_…` · `txt_p5_…` · `txt_p6_…` · `txt_p8_…` · `txt_p10_…`)
| 기저 | 식 (인쇄) | 1D 지지 | 매끈함 | 경계 밖 extra node | 경계 기하 오차 (p.13) | 쪽 |
|---|---|---|---|---|---|---|
| 선형 (표준 MPM) | φ(x) = 1 − \|x\|/h (\|x\| < h) (17) · 다차원 = 텐서 곱 φ_i = φ_i^x φ_i^y φ_i^z (18) | 2h | C⁰ (∇φ 가 셀 경계에서 끊김 · Fig. 2a) | 필요 없음 (델타 특성 함수의 폭 0) | 최대 **h** (방향마다) | p.5 · p.9 · p.13 |
| 2차 B-spline | φ = χ ∗ χ ∗ χ/(\|χ\|)² (19) · χ = 1 (\|x\| < l/2) (20) · 풀어 쓴 꼴 (21): x²/(2h²) + 3x/(2h) + 9/8 (−3h/2 ≤ x ≤ −h/2) · −x²/h² + 3/4 (\|x\| ≤ h/2) · x²/(2h²) − 3x/(2h) + 9/8 (h/2 ≤ x ≤ 3h/2) | 3h | C¹ · 1의 분할 (덩어리 질량에 필요) | **필요** — *"requiring the use of extra, or ghost nodes, beyond the boundary to maintain a partition of unity within the domain"* · 주기는 문제없음 · Dirichlet 은 *"non-trivial"* | 최대 **3h/2** | p.5–6 · p.13 |
| 3차 B-spline | **식 없음** (경계 수정판 Fig. 3b 와 문장뿐) | (4h [카드 산술]) | (C²) | 필요 | 최대 **2h** | p.7 · p.13 |
| 경계 수정 B-spline (열린 균일 매듭) | Cox–de Boor 재귀 (22)(23) · 분모 0 이면 그 항 = 0 · 매듭 간격 h = l/(N − 1) · k 차 (다항 차수 k − 1) 함수 **N + k − 2** 개 → 노드보다 k − 2 개 많은 자유도 · 경계 함수가 경계에서 정확히 1 (Fig. 3) · 0 기울기 경계만 되는 앞 논문 (Steffen 외 2008) 판의 일반화 | — | 안쪽 = B-spline 그대로 | **없음** | 영향 없음 (경계를 격자에 맞춘 문제) | p.6–7 · p.14 |
| uGIMP | 투영을 델타 대신 특성 함수 χ_p 로 (24)–(27) · 조각 상수 χ_p (28) · 1D 가중 4 구간 (29): 1 − (4x² + l_p²)/(4hl_p) (\|x\| < l_p/2) · 1 − \|x\|/h · (h + l_p/2 − \|x\|)²/(2hl_p) · 0 · **모든 입자 · 모든 시각 한 l** | 2h + l | C¹ (*"ensures us C1 continuous basis functions"* p.11) · ∇φ̄ 는 ±l/2 · ±(h ± l/2) 에서 꺾임 (Fig. 4b) | 필요 | 최대 **h + l/2** | p.7–8 · p.11 · p.13 |
| standard GIMP | l_p = l_p⁰ (입자마다 · 시간 무관) — 처음 입자가 고르면 uGIMP 와 같다 | 2h + l_p | C¹ | 필요 | (uGIMP 부류 [카드 해석]) | p.8 |
| cpGIMP | 1D: l_p = 시간 갱신된 V_p (공간을 정확히 채움) · 다차원 근사: **l_p = l_p⁰ diag(F)** (F 의 대각만) · 직사각 χ_p 는 다차원에서 공간을 못 채움 | — | C¹ | UCF 는 두지만 경계 정렬 문제에서 투영 0 (가장 바깥 입자 = 경계 안 l_p/2 · extra node 거리 h + l_p/2 = 기저가 0 이 되는 자리) | 영향 없음 | p.8 · p.10 · p.14 |

- **합성곱 하나로** (식 31–32 · p.10): GIMP 가중 = χ_g ∗ χ_g ∗ χ_p/(\|χ_g\|\|χ_p\|) (χ_g 폭 h · χ_p 폭 l_p) — B-spline 은 세 χ 가 모두 폭 h.  ⇒ *"Choosing l = l_p⁰ would give standard GIMP.  Choosing l = h would give quadratic B-spline basis functions.  Choosing l = 0 would lead to the degenerate case of χ_p = δ(x − x_p), leaving us with the standard piecewise-linear basis functions."*  UCF 는 l 을 자유 매개변수로 둔다.  [카드 산술 확인: 식 (29) 에 l_p = h 를 넣으면 식 (21) 과 같다 — 가운데 구간 3/4 − x²/h² · 바깥 (3h/2 − \|x\|)²/(2h²)]
- **standard GIMP 로 단순화한 이유** (p.10): cpGIMP 의 직사각 χ_p 가 다차원에서 공간을 못 채우고 · *"the major benefit of GIMP is the smoother equivalent basis functions"*.
- **입자 영역 추적의 어려움** (p.3): *"Since the deformation gradient is only maintained at one point within a particle's voxel, it is unclear that the use of this information to deform particles' voxels is sufficient to maintain a partition of the deformed domain."* — Ma · Lu · Komanduri (2006) 는 질량 없는 모서리 입자로 영역을 추적.
- l_p 는 **전폭** (원 GIMP 의 반폭 아님 · p.8).

### 3-3. ★ 노드 적분 (quadrature) 오차 (§4.2 · 식 33–42 · Fig. 5–6 · p.10–13 · `eq_33_…` – `eq_42_…` · `txt_p3_…` · `txt_p11_…` · `txt_p12_…` · `txt_p13_smaller_dt_…`)
- 노드 적분 ∫_Ω f dΩ ≈ Σ_p f(x_p) V_p (33) · 내부력 f_i^int = −∫_Ω σ·∇φ_i dΩ ≈ −Σ_p σ_p·∇φ_ip V_p (34).  서론: *"Spatial integration errors were quickly determined to be the limiting factor in the accuracy and stability of MPM."* (p.3).
- **앞 논문 (Steffen · Kirby · Berzins 2008 IJNME) 의 주 결과** (p.11 인쇄): 입자 배치가 기저의 불연속을 존중하지 않으면 (입자 영역이 노드 경계를 걸치면) 도약 오차 **C[[f^(p+1)]] Δx^(p+2)** (f 가 C^p · 불연속이면 p = −1 · [[·]] = 도약 · Δx = 입자 간격) → 선형 기저의 ∇φ 는 불연속 → **O(Δx)**.
- 입자 하나의 도약 오차 E_jump = ∫_Ωp f dx − f(x_p)Δx · 전체 = 합성 중점 E_MP (늘 O(Δx²)) + E_jump (35) · 겹치지 않고 공간을 채우는 입자면 입자별 합 (36) → **C⁰ 이상 = O(Δx²) · 불연속 = O(Δx)**.
- **uGIMP · 입자 폭 Δx > l** (Fig. 5): 입자 하나가 꺾임 둘을 걸친다 → 일반 식 (37)–(39) · uGIMP 기울기 (a₁ = a₃ = 0 · a₂ = −2/(hl)) 를 넣으면 **E_jump = −(1/h)[Δx − l + 2(1 − Δx/l)δ]** (40) = **O(Δx)** · Δx < l (꺾임 하나) 이면 **E_jump = −(1/(hl))[δ² − δΔx + Δx²/4]** (41) = **O(Δx²)**.  [카드 산술: 식 (39) 에 a 값을 넣어 식 (40) 을 재현 ✓]
- **단일 노드 시험** (42): 상수 응력 σ 면 노드 내부력은 0 이어야 한다 → 남는 값 = ∇φ_i 의 적분 오차.  Fig. 6 (h = 1 · l = 1/10 · UGIMP) — 캡션 *"The particles have a global uniform density, however they have a locally non-uniform spacing.  Otherwise, super-convergent results are observed."*  [판독 · 곡선 꼭짓점 ±0.02 decade 국소 중앙값]: 1/PPC (= Δx) 0.01 → 1.1 × 10⁻³ · 0.02 → 4.6 × 10⁻³ · 0.05 → 0.027 · 0.1 (= l) → 0.13 · 0.2 → 0.44 · 0.5 → 1.5 · 1 → 3.0 → 기울기 **≈ 2.0** (0.01–0.05) · **≈ 1.2** (0.2–1) [카드 산술].
- **안정 · 시간 간격** (p.12–13): *"For stability, in addition to the typical CFL constraints one needs when smooth forces exist, we need to consider further time step restrictions when force kicks arise from these integration errors … While a time step of Δt1 may be sufficient when we are in the O(Δx²) error region, a smaller Δt2 may be required to control stability when we are in the O(Δx) error region."* (Tran · Kim · Berzins 2007 의 셀 넘김 force kick 과 같은 부류).

### 3-4. ★ 경계 처리 (§3.4 · §4.3 · 식 30 · Fig. 7 · p.8–9 · p.13–14 · `eq_30_…` · `txt_p9_…` 둘 · `txt_p13_geometric_error_up_to_2h.png` · `txt_p14_…`)
| 처리 | 원문 | 쪽 |
|---|---|---|
| 처리 없음 | 입자가 계산 영역 밖으로 흘러감 = *"zero gradient Neumann condition"* 꼴 · *"This important part of the algorithm has received scant treatment in the literature"* | p.9 |
| 전통 MPM · Dirichlet | 영역 끝 노드에만 · 투영 속도 (2) · 갱신 속도 (6) · 가속도 (5) 에 건다 · 속도 = 처방값으로 **덮어쓰기** · 가속도 = 0 (흔한 방법) 또는 **a_i = (v_i^{k+1} − v_i^k)/Δt (30)** = 조건 건 뒤 속도 − 조건 전 투영 속도 → *"the force required to bring the velocity at those nodes from the projected value to the prescribed value"* · 두 방법 차 *"very subtle"* · MMS 로 *"the superiority of either is not apparent"* · **UCF = 식 (30)** | p.9 |
| 대칭 (마찰 없는 면) | 법선 속도만 0 의 Dirichlet · 다른 성분은 계산값 · 가속도 법선 성분 0 또는 식 (30) | p.9 |
| GIMP · B-spline 의 extra (ghost) node | 넓은 지지 때문에 영역 밖 노드가 입자와 주고받는다 · Dirichlet = 일반 경계 노드처럼 덮어쓰기 · **대칭 = extra node 의 법선 속도를 0 이 아니라 경계 맞은편 노드 값의 음수로** (*"two objects approaching a collision plane symmetrically"*) | p.9 |
| 경계 기하 오차 | *"In MPM, the union of the particles' voxels are assumed to fill space and define the material of interest"* — 그런데 격자의 '활성' 기저 · 셀은 그 합과 기하가 다르다 · 최대 **h** (선형 · 방향마다) · **2h** (3차 B-spline) · **3h/2** (2차 B-spline) · **h + l/2** (uGIMP) · 전부 O(h) · 정렬과 **기저 선택의 함수** · *"We postulate that, in general, all of the methods here can suffer from O(h) geometric errors."* | p.13 |
| 경계 정렬 문제 | extra node 로 투영하는 방법 (uGIMP · 표준 B-spline) = Neumann · Dirichlet 에서 O(h) 영향 · **주기면 영향 없음** · extra node 를 안 쓰는 방법 (선형 · 경계 수정 B-spline · cpGIMP) = 영향 없음 | p.14 |
| 넓은 기저와 접촉 | *"we can see from Fig. 7 how implementing boundary conditions and modeling contact can present a challenge when wider basis functions are used"* | p.13 |
| Fig. 7 (밀도 투영) | ρ(x) = Σ_i ρ_i φ_i(x) · ρ_i = m_i/(Σ_p φ_ip V_p) · 상수 밀도 [0, 1] · 격자 [−0.2, 1.2] · [판독] 선형 기저 밀도가 x ≈ −0.099 까지 0.005 를 넘고 · 2차 B-spline 은 그림 끝 x = −0.19 에서도 0.0055 · 입자 30 개 (간격 0.0333) → **h ≈ 0.1 · 셀당 3 개** [카드 해석 — 격자 간격 미인쇄] | p.13–14 |
| 대안 | Wallstedt (2008) — 재료 경계의 MLS 표현을 MPM 적분에 넣음 (학위논문) · 이 논문은 경계를 격자에 맞춘 시험으로 비켜 간다 | p.13 |

### 3-5. ★ 제조해 (MMS) 시험 문제 (§5 · 식 43–54 · p.14–16 · `eq_43_44_…` – `eq_54_…` · `txt_p15_…` · `txt_p16_axis_aligned_…`)
- MMS (Schwer 2002 · Knupp · Salari 2003 · Banerjee 2006): 해를 먼저 정하고 그것을 만드는 외력을 해석적으로 → *"It is argued [Knupp and Salari (2003)] that MMS is sufficient to verify a code, not merely necessary."* (p.14) · **TL 꼴로 만든다** — *"within GIMP it is necessary to manufacture solutions in the Total Lagrange formulation so that zero normal stress can be applied to free surfaces as a boundary condition"* · GIMP 는 UL 로 구현되지만 두 꼴이 동등해 비교된다 (p.15).
- 운동 식 ∇P + ρ₀b = ρ₀a (43, TL) · ∇σ + ρb = ρa (44, UL) · neo-Hookean P = λ lnJ F⁻¹ + μ F⁻¹(FFᵀ − I) (45) · σ = (λ lnJ / J) I + (μ/J)(FFᵀ − I) (46) · 외력 가속도 b = MMS 원천항.

| 시험 | 해 · 외력 (인쇄) | 재료 | 이산화 | 시간 | 오차 | [카드 산술] |
|---|---|---|---|---|---|---|
| **1D 주기 막대** (§5.2 · §6.1–6.2) | u = A sin(2πX) cos(Cπt) (47) · F = 1 + 2Aπ cos(2πX) cos(Cπt) (48) · b = C²π²u(2F⁻² + 1) (49) · 경계에서 속도 · 변위 0 → Dirichlet · 주기 둘 다 시험 | σ = (E/2)(F − 1/F) (50) (식 46 의 1D · ν = 0) · E 10⁴ · ρ₀ 1.0 · C = √(E/ρ₀) | 처음 = 고른 X_p⁰ → x_p = X_p⁰ + u(X_p⁰, 0) · F_p = F(X_p⁰, 0) · §6.1 uGIMP · PPC 2 · 3 · 4 · 8 · §6.2 선형 · 2차 B-spline (주기 · 경계 수정 Dirichlet · ghost node Dirichlet) · PPC 4 · 6 · 격자 8–512 셀 | §6.1: A 0.02 · T = 2/C (한 주기) · CFL 0.8 (Fig. 8) · 0.7–1.3 (Fig. 9) · §6.2: A 0.05 · T = 1/C (반 주기) · **Δt = 4 × 10⁻⁶ 고정** (*"a CFL number of approximately 0.2 for 512 grid cells"*) | 입자 위치 오차 = \|x_p^T − X_p⁰ − u(X_p⁰, T)\| (54) · 그림 = RMS (식 미인쇄) | C = 100 · T = 0.02 / 0.01 · §6.2 걸음 2,500 · CΔt/h = **0.2048** (512 셀 — 인쇄 '≈0.2' 와 맞음 → CFL = CΔt/h 로 읽힌다) … 0.0032 (8 셀) · F 범위 0.874–1.126 (A 0.02) · **0.686–1.314** (A 0.05) · 식 (49) = 식 (43) + (50) 에서 유도 ✓ |
| **3D 축 정렬 단위 정육면체** (§5.3 · §6.3) | u = (A sin(2πX) sin(Cπt), A sin(2πY) sin(2π/3 + Cπt), A sin(2πZ) sin(4π/3 + Cπt)) (51) · F 대각 (52) · b = π²(u_X[4μ/ρ₀ − C² − 4(λ(K − 1) − μ)/(ρ₀F_XX²)], …) (53) · K = ln(F_XX F_YY F_ZZ) · 주기도 쓸 수 있게 2 의 배수 | neo-Hookean · E 10⁴ · ρ₀ 1.0 · **ν 0.3** | B-spline (대칭 · 주기 경계) · cpGIMP · **방향마다 4 PPC (셀당 64)** · 8³ 셀 (32,768 입자) – 64³ 셀 (16.8 million 입자) | A 0.05 · T · Δt [미확인] · Fig. 13 은 t = .005 | 'Max Error' (정의 [미확인]) | C = 100 · 성분마다 F 0.686–1.314 · 64³ × 64 = 16,777,216 ✓ · 식 (53) 은 식 (43) + (45) 로 같은 방법 유도 ✓ |

- 3D 꼴의 뜻과 한계 (p.15–16): GIMP 입자의 모서리 · 변이 늘 같은 선 위 → *"This choice allows direct demonstration that GIMP can achieve the same spatial accuracy characteristics in multiple dimensions that have been shown in a single dimension.  It is not, however, representative of general material deformations usually found in most realistic engineering scenarios."*
- [다른 카드] 같은 축 정렬 MMS 의 **2D 판**이 `sadeghirad2011_…` §3-1 (L126 · A 0.05 · ν 0.3 · C 100 · 방향당 2 PPC · 8² – 64²) 에 있다 — 그 카드는 uGIMP · cpGIMP · CPDI · 표준 MPM 을 같은 시험으로 비교.

### 3-6. ★ 결과 — 1D 안정 지도 (§6.1 · Fig. 8 · 9 · p.16–17 · `fig_8.png` · `fig_9.png` · `txt_p16_1d_smoothing_length_stability_runs.png`)
**Fig. 8 — CFL 0.8 · RMS 오차 vs 매끈함 길이 (h 의 몫)** [판독 · 벡터 꼭짓점 · 그림 위 끝 (1) 로 잘린 점 = 불안정]
| PPC (입자 폭) | 불안정 (잘림) | 처음 정상인 l | 안정 구간 오차 |
|---|---|---|---|
| 8 (h/8 = 0.125) | l = 0.15 | 0.175 (1.6 × 10⁻⁴) · 0.20 (3.0 × 10⁻⁵) | 2.5–6.4 × 10⁻⁶ (l ≥ 0.25) |
| 4 (h/4 = 0.25) | l = 0.20 | 0.225 (2.3 × 10⁻⁴) · 0.25 (5.0 × 10⁻⁶) | 3.7–13 × 10⁻⁶ |
| 3 (h/3 = 0.333) | l = 0.275 | 0.30 (1.9 × 10⁻⁵) | 4.9–14 × 10⁻⁶ |
| 2 (h/2 = 0.5) | l = 0.45 | 0.475 (6.6 × 10⁻³) · 0.50 (8.6 × 10⁻⁶) | 0.9–2.0 × 10⁻⁵ |

- 저자: *"We see that the simulations go unstable when the smoothing length is close to, or less than the initial width of the particles.  The 2 PPC simulation goes unstable for L < h/2, the 3 PPC simulation goes unstable for L < h/3, etc."* (p.16) — ⚠ [판독] 3 PPC 는 l = 0.30h (< h/3) 에서 정상 · 8 PPC 는 l = 0.15h (> h/8) 에서 불안정 → 문턱은 '입자 폭 근처' 이고 'L < h/PPC' 가 정확한 선은 아니다 (앞 문장의 *"close to"* 와는 맞다).

**Fig. 9 — RMS 오차 vs CFL** [판독 · 마지막 정상 CFL – 처음 뛴 (또는 잘린) CFL]
| l | (a) 4 PPC | (b) 8 PPC |
|---|---|---|
| h/8 | 0.74 – 0.75 (원문 *"approximately 0.75"*) · 정상 구간 오차도 1.4–2.1 × 10⁻⁴ (다른 l 의 ≈ 7 배 — l < 입자 폭 h/4 인 O(Δx) 영역 [카드 해석]) | 0.76 – 0.78 (정상 구간 1.4–1.6 × 10⁻⁵ — l = 입자 폭) |
| h/4 | 0.80 – 0.82 | 0.80 – 0.82 |
| h/3 | 0.84 – 0.85 | 0.84 – 0.86 |
| h/2 | 0.90 – 0.92 | 0.90 – 0.92 |
| h (= 2차 B-spline) | 1.20 – 1.25 (원문 *"stable up to a CFL number of approximately 1.2"*) | 1.20 – 1.25 |

- 저자: *"the time-step stability restrictions do not change significantly between the 4 PPC and 8 PPC simulations, suggesting that the stability is more dependent on the smoothing length than the number of particles per cell."* (p.16) · §6.1 의 격자 수 · 입자 수 · CFL 의 식 [미확인].

### 3-7. ★ 결과 — 1D 공간 수렴 (§6.2 · Fig. 10 · 11 · p.16–18 · `fig_10.png` · `fig_11.png` · `txt_p17_…` 둘)
**RMS 입자 위치 오차** [판독 · 벡터 꼭짓점] · 이웃 차수 = log₂(e_k/e_{k+1}) [카드 산술]
| 줄 (그림) | 8 | 16 | 32 | 64 | 128 | 256 | 512 셀 | 이웃 차수 |
|---|---|---|---|---|---|---|---|---|
| 4PPC 선형 · Dirichlet (10) | 7.34e-3 | 1.38e-3 | **9.30e-4** | 1.68e-3 | 6.01e-3 | 9.50e-3 | 7.53e-3 | 2.41 · 0.57 · −0.85 · −1.84 · −0.66 · 0.33 |
| 4PPC 2차 B-spline · 주기 (10) | 1.03e-2 | 2.10e-3 | 4.62e-4 | 1.24e-4 | **5.68e-5** | 7.62e-5 | 1.45e-4 | 2.30 · 2.18 · 1.90 · 1.12 · −0.42 · −0.93 |
| 4PPC 경계 수정 B-spline · Dirichlet (10) | 1.00e-2 | 1.90e-3 | 4.53e-4 | 1.25e-4 | **5.74e-5** | 7.62e-5 | 1.45e-4 | 2.40 · 2.06 · 1.86 · 1.13 · −0.41 · −0.93 |
| 6PPC 경계 수정 2차 · Dirichlet (10) | 1.00e-2 | 1.92e-3 | 4.46e-4 | 1.05e-4 | 2.38e-5 | 5.69e-6 | **3.73e-6** | 2.39 · 2.11 · 2.09 · 2.14 · 2.06 · 0.61 |
| ghost node 2차 · Dirichlet (11) | 1.25e-2 | 5.53e-3 | 2.97e-3 | 1.53e-3 | 7.76e-4 | 3.92e-4 | 1.95e-4 | **1.18 · 0.90 · 0.96 · 0.98 · 0.99 · 1.01** |
| 경계 spline 2차 · Dirichlet (11) | = Fig. 10 의 6PPC 줄 (모든 점 차 ≤ 0.05 %) | | | | | | | 2.39 … 0.61 |
| 주기 2차 (11) | 1.02e-2 | 2.08e-3 | 4.56e-4 | 1.07e-4 | 2.40e-5 | 5.60e-6 | 3.73e-6 | 2.30 · 2.19 · 2.10 · 2.15 · 2.10 · 0.59 |

- 저자 문장: 선형 4PPC *"showing no significant convergence beyond a modest 16 grid cells"* · 2차 B-spline *"demonstrating O(h²) convergence, with an error plateau occurring past 128 grid cells"* · 주기 ↔ 경계 수정 Dirichlet *"nearly identical"* · *"nodal integration will always give some quadrature error which can explain the error plateaus starting at 128 grid cells"* · 6 PPC *"helps lower the quadrature error and lower the error plateau"* · ghost node Dirichlet = *"the error convergence is in fact reduced to O(h)"* (p.17–18).
- [카드 산술] 오차를 진폭 A (0.05) 로 나누면: 6PPC 512 셀 **0.0075 %** · ghost node 512 셀 **0.39 %** · 선형 최소 (32 셀) **1.9 %** · 4 → 6 PPC 에서 512 셀 오차 **39 배** 감소 (1.45 × 10⁻⁴ → 3.73 × 10⁻⁶).
- ⚠ 4PPC B-spline 은 128 → 512 셀에서 오차가 **×2.55 커진다** (원문 "plateau") · 선형은 16 → 256 셀에서 **×6.9 커진다** (원문 "no significant convergence") [판독 · 카드 산술] — §3-9.
- ⚠ Fig. 11 의 PPC 는 인쇄되지 않았다 — 경계 spline 줄이 Fig. 10 의 6PPC 줄과 모든 점에서 같고 (≤ 0.05 %) · 주기 줄은 Fig. 10 의 4PPC 주기 줄과 64 셀부터 갈린다 (512 셀 3.73 × 10⁻⁶ ↔ 1.45 × 10⁻⁴) [판독] → **6 PPC 로 읽힌다** [카드 해석].

### 3-8. ★ 결과 — 3D 축 정렬 MMS (§6.3 · Fig. 12 · 13 · p.18–19 · `fig_12.png` · `fig_13.png` · `txt_p18_3d_mms_setup_results.png`)
**'Max Error'** (정의 [미확인]) [판독 · 벡터 꼭짓점] · 이웃 차수 [카드 산술]
| 줄 | 8³ | 16³ | 32³ | 64³ | 이웃 차수 | 64³ 오차 ÷ A [카드 산술] |
|---|---|---|---|---|---|---|
| B-spline · 대칭 (범례 "Symetric") | 2.63e-2 | 9.52e-3 | 4.63e-3 | 2.47e-3 | 1.47 · 1.04 · 0.91 | 4.9 % |
| B-spline · 주기 | 1.26e-2 | 2.45e-3 | 7.66e-4 | 3.84e-4 | 2.37 · 1.68 · **1.00** | 0.77 % |
| cpGIMP | 9.13e-3 | 2.08e-3 | 5.04e-4 | 1.74e-4 | 2.13 · 2.04 · **1.54** | 0.35 % |

- 저자: *"The results in Fig. 12 clearly show O(h²) convergence with cpGIMP for all grid resolutions in the study.  Using B-spline basis functions with periodic boundary conditions did nearly as well, with convergence rates trailing off at higher grid resolutions."* · ghost node (대칭) = O(h) · *"It is not surprising that cpGIMP outperforms other methods, as this problem is well suited for cpGIMP since particles remain axis-aligned and their voxels area [sic] a true partition of the domain."* · 주기 B-spline 의 차수 하락: *"It is still unclear … There are a number of possibilities, including a more complicated quadrature error behavior in multi-D, or the buildup of grid crossing errors (similar to those analyzed by Tran, Kim, and Berzins (2007)), which may be more significant in multi-D since many more grid crossing events occur than in 1-D simulations using similar resolutions."* (p.18–19).
- Fig. 13: 해석해 (식 51) 의 2D 단면 (t = .005) · 변형된 입자 위치 + 축 정렬 입자 영역 개념도 (*"rounded and their sizes slightly reduced for visual clarity"*).

### 3-9. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① 3D 축 정렬 = *"not … representative of general material deformations"* (p.16) ② 3D 주기 B-spline 차수 하락의 원인 *"still unclear"* (p.18) ③ 경계 기하 오차는 *"We postulate"* (p.13) ④ 직사각 χ_p (cpGIMP) 는 다차원에서 공간을 못 채운다 (p.8 · p.10) · F 한 점으로 입자 영역 분할을 지킬 수 있는지 *"unclear"* (p.3) ⑤ *"nodal integration will always give some quadrature error"* (p.17) ⑥ 경계 가속도 두 방법의 우열 불명 (p.9) ⑦ 경계 노드를 움직여 경계 힘을 따라가는 것은 다차원 복잡 형상에서 *"not trivial"* (p.5).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. 식 (24) 의 δ 를 *"with δ the Kronecker delta"* (p.7) — 적분 안의 δ(x − x_p) 는 Dirac 이다 (p.9 는 *"the zero width of the Dirac delta characteristic functions"*).
2. 열린 균일 매듭의 끝 겹침 *"a multiplicity of k − 1 for a k-order B-spline"* + 예 (4 차 · x₀ 세 번 · p.7) ↔ 같은 문단의 함수 수 *"N + k − 2"* 와 Fig. 3 (2차 **7** 개 · 3차 **8** 개 · 끝 함수 = 경계에서 1 [판독 · 벡터 경로 곡선 수 · 0–5 구간]).  겹침 k − 1 이면 함수가 N + k − 4 개이고 경계에서 1 인 함수가 없다 [카드 산술 — 식 (22)(23) 으로 2차 · 매듭 (0, 0, 1, 2) 의 첫 함수를 직접 계산하면 x = 0 에서 0] → **겹침 k 의 오기로 읽힌다** [카드 해석].
3. Fig. 10 의 4PPC B-spline *"error plateau occurring past 128 grid cells"* ↔ 128 → 512 셀에서 ×2.55 증가 [판독].
4. 선형 4PPC *"no significant convergence beyond a modest 16 grid cells"* ↔ 16 → 256 셀에서 ×6.9 증가 (발산 쪽) [판독].
5. 3D cpGIMP *"clearly show O(h²) convergence … for all grid resolutions in the study"* ↔ 32 → 64 기울기 1.54 [판독 · 카드 산술].
6. 안정 문턱 *"2 PPC … L < h/2, the 3 PPC … L < h/3, etc."* ↔ 3 PPC 0.30h 정상 · 8 PPC 0.15h 불안정 [판독].
7. Fig. 11 의 PPC 미인쇄 (값으로 6 PPC [카드 해석]).
8. 1D 막대의 A 를 *"the maximum deformation percentage"* (p.15) 라 부르나 §6.2 는 *"5% maximum displacement"* — A 는 **변위** 진폭이고 변형 (F − 1) 진폭은 2πA (A 0.05 → ±31 %) [카드 산술].
9. 표기 · 조판: 범례 "Symetric" (Fig. 12) · "Dirchlet" (Fig. 10) · "Piola-Kirchoff" (p.15) · "substitutingstress" · "conditionon" · "multipledimensions" · "liketo" · "area a true partition" (p.18) · 기호 l 이 매끈함 길이 · χ 폭 · 1D 영역 길이 (p.7 *"domain of length l"*) 에 겹쳐 쓰임 · Fig. 8–9 축과 본문 §6.1 은 'L', §3–4 는 'l'.
10. 미인쇄 (§13): CFL 의 식 · §6.1 격자 수 · §6.3 Δt · T · 'Max Error' · RMS 식 · 계산 시간 · 결과 런의 시간 전진 판 · 경계 가속도 판.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
- **분석**: 기저를 합성곱으로 다시 씀 (식 19 · 31) → 노드 적분 = 비균일 중점 적분 (앞 논문 결과 · 식 35–36) → uGIMP 의 '입자 폭 > l' 경우를 새로 (식 37–41) → 단일 노드 힘 시험 (식 42 · Fig. 6) · 경계 기하 오차를 기저 지지로 셈 (p.13) · 밀도 투영 그림 (Fig. 7).
- **시험**: MMS 해 → TL 체적력 (식 49 · 53) → 고른 처음 배치 + 처음 변위 · F → UCF 명시 적분 (식 1–10 · 경계 처리 선택) → 끝 시각 입자 위치 오차 (식 54) → RMS (1D) · Max (3D) → 격자 사다리 log–log + 기준선 · 매끈함 길이 · CFL 지도.
- **코드**: UCF (C-SAFE · 병렬 · AMR 기반) 의 MPM · GIMP 구성 요소 — 3D 시험은 UCF 에서 (*"implemented in the UCF"* p.18) · 1D 계산의 코드 [미확인].

### 4-2. 이 논문이 고르지 않은 것 (= 우리 결정의 자리)
응력 갱신 순서의 비교 (USL / USF · 엇갈린 중앙 차분의 이득) · 입자 속도 전달 (FLIP / PIC / APIC) 의 비교 · 암시 적분 · 접촉 · 다물체 · 소성 · 준정적 · 하중 제거 · 거의 비압축 재료.

### 4-3. 입자 처리 ★
- 물질점 = **연속체를 나눈 적분점** (알갱이가 아님) · 한 물체 · 한 속도장 · *"the union of the particles' voxels are assumed to fill space and define the material of interest"* (p.13).
- 처음 배치 = 고른 간격 (셀당 2–8 · 3D 방향당 4) · 단일 노드 시험만 **국소 불균일 간격** (고른 간격은 초수렴 · Fig. 6 캡션).
- 입자 영역: uGIMP = 고정 폭 l · cpGIMP = l_p⁰ diag(F) (축 정렬만 정확) · 선형 · B-spline = 영역 없음 (델타).
- DEM 같은 '입자 무질서' (무작위 배치 · 크기 분포 · 접촉망) 는 **없다**.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete element 0 회).  다른 방법에 대한 말은 FE 뿐: *"… large deformation problems, especially those involving complex geometries and contact where typical finite element type methods frequently fail"* (초록 p.1) · *"The ability to handle solid mechanics problems involving large deformations and/or fragmentation of structures, which are sometimes problematic for finite element methods, has led, in part, to the method's success."* (p.1).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **소성 계산 없음** ('plastic' = 참고문헌 Love · Sulsky 2006 의 제목 *"… dynamic finite deformation plasticity"* 한 번).  다루는 것은 큰 변형의 **수치** 어려움 넷: ① 셀 넘김 — *"lack of regularity in ∇φ is conjectured to be the root cause of what is referred to as 'grid cell crossing instabilities'"* (p.5) ② 적분 오차 — *"Spatial integration errors were quickly determined to be the limiting factor in the accuracy and stability of MPM"* (p.3) ③ 입자 영역 추적 — *"Since the deformation gradient is only maintained at one point within a particle's voxel, it is unclear that the use of this information to deform particles' voxels is sufficient to maintain a partition of the deformed domain"* (p.3) ④ 경계 기하 오차 O(h) (p.13).  우회 = 매끈한 기저 (B-spline · GIMP) + 매끈함 길이 ≥ 입자 폭 + 주기 · 경계 수정 기저.  비용 [미확인] (가장 큰 계산 16.8 million 입자 · 시간 없음).
3. **2D / 3D** — 해석 · 계산은 1D, 3D 는 축 정렬 MMS 하나 (UCF), **2D 계산 없음**.  전이 문장: *"show that many of the 1-D convergence results from the previous section are also valid in 3-D"* (p.18) ↔ 한계 *"It is not, however, representative of general material deformations"* (p.16) · 3D 주기 B-spline 차수 하락 *"may be more significant in multi-D since many more grid crossing events occur than in 1-D simulations using similar resolutions"* (p.18–19).
4. **압력을 뺄 때의 거동** — **다루지 않았다** ('unload' 0 회).  탄성 진동 (반 · 한 주기) 의 되돌아옴뿐 · 접촉 분리 · 잔류 변형 없음.

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 노드 적분 (nodal integration) | 격자 적분을 물질점 위치 값 × 입자 부피의 합으로 (식 33) — 입자가 적분점 |
| 도약 오차 (jump error) | 입자 영역이 피적분 함수의 불연속 (또는 도함수 불연속) 을 걸칠 때 생기는 중점 적분 오차 — C[[f^(p+1)]]Δx^(p+2) |
| 초수렴 (super-convergence) | 고른 간격 입자에서 오차가 상쇄돼 이론보다 빨리 주는 것 — 그래서 Fig. 6 은 국소 불균일 간격 |
| 매끈함 길이 (smoothing length) l | uGIMP 의 특성 함수 χ 폭 · l = h → 2차 B-spline · l = 0 → 선형 |
| uGIMP · standard GIMP · cpGIMP | 모든 입자 한 l · 입자마다 처음 폭 고정 · 폭을 변형 (1D V_p · 다차원 l_p⁰ diag(F)) 으로 갱신 |
| extra (ghost) node | 넓은 지지 기저 때문에 계산 영역 밖에서 입자와 주고받는 노드 |
| 경계 수정 B-spline | 열린 균일 매듭 (끝 겹침) 으로 경계 함수가 경계에서 1 이 되게 한 B-spline — extra node 없이 Dirichlet |
| 경계 기하 오차 | 입자 영역의 합 (물체) 과 격자의 활성 기저 · 셀이 보는 물체의 차 — O(h) |
| MMS (제조해) | 해를 정해 두고 그 해를 만드는 체적력을 해석적으로 더해 코드의 수렴 차수를 재는 법 |
| TL / UL | Total Lagrange (처음 배치 기준 · P) / Updated Lagrange (현재 배치 · σ) — 동등 |
| force kick | 입자가 기저 불연속을 넘거나 걸칠 때 생기는 내부력의 튐 — 시간 간격을 더 줄이게 한다 |
| CFL | 시간 간격 · 파속 / 격자 간격 — 이 논문은 식을 안 적는다 (§6.2 의 값으로 CΔt/h [카드 산술]) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 도구 · p.4 · j.110) | 2D MPM 문제 설정 (점선 = 물체 경계 Ω · 닫힌 점 = 물질점 · 정사각 배경 격자 · x_i · x_p) | 개념 그림 (보고서 MPM 절 설명용) |
| **Fig. 2** (`fig_2.png` · 손 · p.6 · j.112) | 1D 기저 세 벌 (a 선형 · b 2차 B-spline · c GIMP) + 입자 (높이 = 속도) + 투영된 격자 속도장 — 선형은 노드에서 기울기가 끊기고 B-spline · GIMP 는 매끈 · 경계 밖 extra node 에도 값 | ★ 우리 2차 B-spline 이 경계 밖 노드에 값을 싣는 그림 (판 · 바닥 · AM 마스크 경계 논의) |
| **Fig. 3** (`fig_3.png` · 손 · p.7 · j.113) | 경계 수정 B-spline (a 2차 k = 3 · b 3차 k = 4 · 0–5) — 경계 함수가 경계에서 1 | 함수 7 · 8 개 [판독] — 원문 매듭 겹침 오기의 근거 (§3-9 ②) |
| **Fig. 4** (`fig_4.png` · 손 · p.8 · j.114) | GIMP 가중 (a) · 기울기 가중 (b · ±1/h · 점선 = 연속성 깨지는 자리 ±l/2 · ±(h ± l/2)) | 적분 오차가 생기는 자리 (식 35–41) |
| **Fig. 5** (`fig_5.png` · 손 · p.12 · j.118) | 입자 영역이 꺾임 둘을 걸치는 경우 — (a) 일반 · (b) uGIMP 기울기 · Δx > l | 식 (40) 의 그림 |
| **Fig. 6** (`fig_6.png` · 도구 · p.13 · j.119) | 단일 노드 내부력 오차 vs 1/PPC (h = 1 · l = 1/10 · UGIMP · C₁x · C₂x² 기준선) | ★ Δx < l 2 차 → Δx > l 1 차 [판독 §3-3] · 국소 불균일 간격 시험 꼴 |
| **Fig. 7** (`fig_7.png` · 손 · p.14 · j.120) | 상수 밀도 [0, 1] 투영 — 참 밀도 · 선형 · 2차 B-spline · 입자 위치 | ★ 격자가 보는 물체가 경계 밖으로 번진다 (B-spline 이 더 멀리) — 우리 판 · AM 경계 |
| **Fig. 8** (`fig_8.png` · 도구 · p.17 · j.123) | uGIMP 안정 — RMS 오차 vs l/h (CFL 0.8 · PPC 2 · 3 · 4 · 8) | ★ '매끈함 길이 ≥ 입자 폭' 규칙 (§3-6) |
| **Fig. 9** (`fig_9.png` · 손 · p.17 · j.123) | RMS 오차 vs CFL (a 4 PPC · b 8 PPC · l = h/8 … h) | ★ 안정 CFL 끝 ≈0.75 → ≈1.2 (§3-6) |
| **Fig. 10** (`fig_10.png` · 손 · p.18 · j.124) | 1D 막대 공간 수렴 (선형 · B-spline 주기 · 경계 수정 Dirichlet · 6PPC · 2 차 기준선) | ★ U6 · U2 의 대조 곡선 (§3-7) |
| **Fig. 11** (`fig_11.png` · 손 · p.18 · j.124) | 2차 B-spline 경계 처리 셋 (ghost node Dirichlet · 경계 spline Dirichlet · 주기 · 1 · 2 차 기준선) | ★ extra node Dirichlet = 1 차 — 우리 판 경계의 예상 (§7-2) |
| **Fig. 12** (`fig_12.png` · 다시 자름 · p.19 · j.125) | 3D 축 정렬 MMS 수렴 (B-spline 대칭 · 주기 · cpGIMP · Max Error · 1 · 2 차 기준선) | 3D 차수 (§3-8) · 1D → 3D 전이 경고 |
| **Fig. 13** (`fig_13.png` · 도구 · p.19 · j.125) | 해석해 2D 단면 (t = 0.005) · 변형 입자 + 축 정렬 영역 | 축 정렬 MMS 의 모양 |
| 식 크롭 **41** | P2G (`eq_01_02_p2g_mass_velocity`) · 응력 · 내부력 (`eq_03_04_…`) · 가속도 (`eq_05_…`) · Forward-Euler (`eq_06_…`) · ∇v (`eq_07_…`) · 입자 갱신 (`eq_08_10_…`) · 엇갈린 차분 (`eq_11_…` · `eq_12_15_…`) · 외력 (`eq_16_…`) · 기저 (`eq_17_…` – `eq_21_…`) · 열린 매듭 (`eq_22_23_…`) · GIMP (`eq_24_…` – `eq_29_…`) · 경계 가속도 (`eq_30_…`) · 합성곱 (`eq_31_…` · `eq_32_…`) · 적분 오차 (`eq_33_…` – `eq_42_…`) · MMS (`eq_43_44_…` – `eq_54_…`) | 보고서 MPM 절 붙임 (번호 식 (1)–(54) 전부) |
| 근거 문단 **20** (`txt_p1_…` – `txt_p18_…`) | 카드가 인용한 문장 (초록 · 적분 오차 · 셀 넘김 · ghost node · GIMP 셋 정의 · 경계 가속도 · 대칭 거울 · 매끈함 길이 · 도약 오차 · force kick · 기하 오차 · 주기 · TL · 축 정렬 한계 · 시험 설정 셋 · 3D 결과) | 인용 확인 |

## 6. Post-processing ★
- **오차**: 끝 시각 입자 위치 오차 \|x_p^T − X_p⁰ − u(X_p⁰, T)\| (식 54) · 1D 그림 = 'RMS Error' (식 미인쇄) · 3D 그림 = 'Max Error' (정의 미인쇄) · 단일 노드 시험 = 노드 내부력 (0 이어야).
- **수렴**: 격자 셀 수 (8–512 · 3D 8–64 방향마다) 에 대한 log–log · 1 · 2 차 기준선 · 차수는 그림으로만 (기울기 숫자 인쇄 없음).
- **안정**: 오차 vs 매끈함 길이 (CFL 고정) · 오차 vs CFL (l 고정) — 불안정 = 그림 위 끝 밖.
- **판독 (이 카드)**: digitized.csv 303 행 — PDF 벡터 경로 (MATLAB) · 축 = 주 눈금 위치 ↔ 눈금 글자 최소제곱 (log 축 log10) · 꺾은선 꼭짓점 = 그려진 자료점 (Fig. 8 의 2 PPC 는 사각 표지 중심 · 3 PPC 꺾은선은 0.55h 꼭짓점이 경로에 없음 · Fig. 9a 의 h/2 는 0.76 꼭짓점이 없음) · Fig. 6 곡선 = 꼭짓점 2,000 개의 ±0.02 decade 국소 중앙값 · Fig. 7 = 요점 셋 · 기준선 끝점으로 축 사상 점검.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 정본 카드 · 비교 문서의 출처 줄을 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 하중 · 이산화가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 이산화 | 선형 · 2차 B-spline (+ 경계 수정) · uGIMP · cpGIMP · 덩어리 질량 · ∇φ 내부력 (식 4) · 입자 속도 = FLIP 증분 (식 9) · Forward-Euler | MPM = **MLS-MPM · APIC · 2차 B-spline · 명시 · f32** [다른 카드 `hu2018_…` L498 (우리 코드 판독)] | **기저 = 같은 2차 B-spline** · 힘 식 다름 (MLS 대용 기울기 · §7-4) · 입자 속도 다름 (APIC ↔ FLIP 증분) · 입자 위치 갱신은 같은 값 (식 10 = x_p + Δt Σ_i φ_ip v_i^{k+1} ↔ 우리 `x[p] += dt * v[p]` · v_p = Σ w v_i^{k+1}) [카드 산술 · `hu2018_…` L31] |
| 갱신 순서 | 식 1–10 — σ(F_p) → 힘 → 격자 속도 → **갱신된 격자 속도로** ∇v · F → v_p · x_p | P2G (MLS 힘 · APIC) → 격자 · 경계 → G2P (APIC · C_p) → F = (I + dt C_p) F → J2 반환 → x += dt v [다른 카드 `hu2018_…` L26–L31] | 같은 '갱신된 격자 속도로 F' 순서 [카드 해석] |
| 셀당 물질점 | 1D 2 · 3 · 4 · 8 (안정) · 4 · 6 (수렴) · 3D 방향당 4 (셀당 64) | 방향당 2 (셀당 8) [다른 카드 `homel2017_…` L499 · `sadeghirad2011_…` L516] | 우리가 적다 — 이 논문에 2 PPC **수렴** 시험은 없다 (2 PPC 는 안정 지도만) |
| 시간 간격 | CFL (식 미인쇄 · CΔt/h 로 읽힘) 0.2 (수렴) · 0.7–1.3 · 0.8 (안정) · l = h 안정 끝 ≈1.2 (1D · ν 0) [판독] | dt = 0.4 dx/√M (ρ = 1 규약) + 판 Mach [다른 카드 `gritton2017_…` L538 (우리 코드 판독)] · M 의 뜻 [미확인 — `sadeghirad2011_…` L520 도 미확인] | M = P파 계수면 Courant 0.4 · 막대 E 면 ν 0.49 에서 P파 기준 **1.65** (c_P/c_bar = √[(1 − ν)/((1 + ν)(1 − 2ν))] = 4.14 [카드 산술 · 그 카드 1.66]) — 후자면 이 논문 1D 안정 끝 (≈1.2) 위 (1D ν 0 → 3D ν 0.49 전이는 안 된다 · 확인할 것 = 우리 M) |
| 재료 | neo-Hookean 탄성 (식 45–46) · E 10⁴ · ρ₀ 1 · ν 0 · 0.3 (무차원) | MPM J2 · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 · μ 0.51 GPa) [우리 기록 · `sadeghirad2011_…` L518] · DEM E_eff 1.35 GPa (18 배 연화) | 소성 · 거의 비압축 없음 → 수치 크기 전이 불가 · 차수 · 기전만 |
| 하중 · 변형 | MMS 체적력 · 탄성파 동역학 · 반 · 한 주기 · F 0.686–1.314 (A 0.05) [카드 산술] | 판 압축 ≈ 300 MPa · 판 Mach 0.01–0.03 (준정적) [우리 기록 · `sadeghirad2011_…` L519] | 하중 꼴 · 시간 척도 다름 |
| 경계 | Dirichlet 덮어쓰기 + 경계 가속도 식 (30) (UCF) · 대칭 = 법선 0 + extra node 거울 · 주기 · 경계 수정 B-spline | 판 = 판 위 (`k * dx > wall_z`) 노드에 판 속도 (slip · 양방향 · 분리 없음) · 바닥 = 음의 속도만 0 (separate · μ 0) · 옆벽 separate μ 0 · AM 마스크 노드 = 0 (sticky) [다른 카드 `hu2018_…` L515–L518 (우리 코드 판독)] | 우리 판 · AM 마스크 = **extra node 까지 처방 속도를 거는 Dirichlet 부류** (거울 아님) → 이 논문 기준 경계 근처 **1 차** 예상 [카드 추론 · §7-2] · 바닥의 '한쪽만' 조건은 이 논문에 없다 |
| 판 반력 | 식 (30) = 처방 속도로 돌리는 힘 (반력을 읽지는 않는다) | wallP = Σ m_i (v_i − V_판) (판이 막은 운동량) [다른 카드 `hu2018_…` L521] | **같은 꼴** (식 30 × m_i 의 합) [카드 해석] |
| 오차 추정 | MMS · 입자 위치 오차 · RMS · Max · 격자 사다리 + 기준선 · 단일 노드 시험 · 안정 지도 | 해석해 단위 시험 없음 · 격자 사다리 (192 · 288 · 384) 의 비수렴 [우리 기록 · `bardenhagen2004_…` L494 · 비교 문서 L3038] | 우리 U2 · U6 에 바로 쓸 틀 (§9) |

### 7-2. ★ 우리 판 · 바닥 · AM 마스크 = 'extra node 에 건 Dirichlet' 부류 → 경계 근처 1 차 (카드 추론) + 크기 감각 (카드 산술)
- 원문 근거: 넓은 지지 (2차 B-spline) 에서 extra node 로 투영된 정보에 Dirichlet 을 걸면 경계 기하 오차 O(h) 가 남고 (p.14) 1D 막대 수렴이 **1 차** (Fig. 11 · 이웃 차수 0.90–1.18) · 3D 대칭도 1 차 (Fig. 12 · 1.47 · 1.04 · 0.91).  우리 판은 `k * dx > wall_z` 인 모든 노드에 판 속도를 걸고 (거울 아님) 우리 AM 마스크는 AM 안 노드를 0 으로 둔다 [다른 카드 `hu2018_…` L515–L516] → **같은 부류** [카드 추론].
- 크기 감각 [카드 산술 · 상한 감각 · 측정 아님]: 2차 B-spline 의 경계 기하 오차 최대 3h/2 · 우리 real_14 MPM dx = 0.141 µm (n_grid 384) [우리 기록 · 비교 문서 L2963] → **0.21 µm** = DEM 두께 30.28 µm [우리 기록 · 비교 문서 L3618 · `cardenasbarrantes2020_…` L469] 의 **0.70 %** · 고체 부피를 고정하고 두께로 바꾸면 기공 (1 − 0.156) × 0.70 % ≈ **0.6 %p** (ε 15.6 % = real_14 LIGGGHTS [우리 기록 · `benhadjali2025_…` L294]) · SE 지름 ≈ 1 µm ≈ 7 셀 [우리 기록 · 비교 문서 L2963] 의 **21 %** — AM 표면 둘레에서 '격자가 보는 경계' 가 SE 한 알의 1/5 폭으로 번질 수 있다.
- ⚠ 우리 기공 읽기는 판 위치 (wall_z) 로 두께를 세므로 이 오차는 **읽기의 오차가 아니라 판과 물질 사이의 어긋남** (물질이 판을 h 단위로 일찍 · 늦게 느낌) 으로 나타난다 [카드 해석].  움직이는 판은 격자선에 맞지 않아 이 논문의 처방 (경계 수정 B-spline = 경계 = 격자선) 이 그대로 맞지 않는다 [카드 해석].
- ⇒ 확인할 것 (결과 전 등록): 정지 때 판 아래 물질점 맨 위 z ↔ wall_z 의 차를 dx 단위로 (≤ 3h/2 인지) · 판 근처 응력 · 기공의 판 거리별 분포.

### 7-3. ★ 셀당 입자 · 매끈함 · Courant
- 2차 B-spline = uGIMP 의 l = h (p.10) → 기울기 꺾임 간격 h · 우리 방향당 2 PPC 면 입자 폭 Δx = h/2 < l → 이 논문의 **'Δx < l' (식 41 · O(Δx²)) 쪽**이고 Fig. 8 에서 2 PPC · l = h 는 CFL 0.8 에서 정상 (RMS 9.0 × 10⁻⁶ [판독]) [카드 산술 · 1D uGIMP 지도의 유추].
- 다만 고정 PPC 의 격자 사다리는 적분 오차 바닥에서 멈추거나 **오히려 커질 수 있다** (4 PPC · 128 → 512 셀 ×2.55 [판독]) — 우리 사다리 (192 · 288 · 384) 를 읽을 때 PPC 를 엇갈려 돌린 대조 팔이 필요하다 (U6 · `bardenhagen2004_…` L494 와 같은 결론 · 이 논문이 1D 정량 근거).
- Courant: §7-1 의 M 확인 — P파 기준이면 0.4 (여유) · 막대 E 기준이면 1.65 (이 논문 1D 끝 ≈1.2 위).  우리 재료는 ν 0.49 라 막대 · P파 차가 4.14 배 [카드 산술].

### 7-4. MLS-MPM 과 다른 곳 (전이 한계)
- **힘 식**: MLS-MPM 은 ∇N_i(x_p) 자리에 M_p⁻¹ N_i(x_p)(x_i − x_p) (M_p = Δx²/4 · 2차) 를 쓴다 — 1D 에서 노드 바로 옆 1.5 배 · s = ½ · 1 에서 같음 [다른 카드 `hu2018_…` L253–L259].  이 대용 기울기는 C¹ (2차 B-spline) × 일차식이라 이 논문 식 (35) 의 틀로는 도약 항이 O(Δx³) 이하 → 전체 O(Δx²) 가 중점 오차로 정해질 것 [카드 추론 — 원문은 MLS 를 다루지 않는다].
- **입자 속도**: APIC (G2P 에서 v_p = Σ w v_i^{k+1} + 아핀 C_p) ↔ 이 논문 식 (9) FLIP 증분 — 소산 · 잡음 특성이 다르다 [카드 해석] · 위치 (식 10) 는 같은 값.
- **질량**: 둘 다 덩어리 질량.
- ⇒ 이 논문의 **수치 결과 (오차 값 · 안정 CFL)** 는 우리 코드로 다시 재야 하고, **차수 · 기전 · 시험 꼴** 만 옮긴다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = MPM 반쪽의 **수치 정확도 · 검증 도구** (기저 · 경계 · 적분 · 안정) — 물리 (소성 · 압밀 · 형상) 는 없다.  우리 frame 의 MPM 역할 (소성 형상 · 공극 메움 · 응력장) 을 **믿을 수 있게 하는 시험 틀**을 준다.
- 없는 반쪽: DEM 쪽 전부 (접촉망 · 패킹 · 수송) · 다물체 접촉 · 소성 · 탈압.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = 지시서 · 정본 카드: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  **이 논문에는 기공 · 밀도 · 압력 값이 없다 — 랩 표준과 나란히 놓을 숫자 0 개.**  재료 = 무차원 탄성 — 우리 재료 · 차원 · 하중과 모두 다르다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **물체 = 입자 영역의 합** (*"the union of the particles' voxels are assumed to fill space and define the material of interest"* p.13) 이고 격자가 보는 물체는 그것과 h 단위로 다르다 (최대 h · 3h/2 · 2h · h + l/2) → 우리 기공 연산자를 적을 때 **무엇으로 고체 · 두께를 세는지** (물질점 부피 합 · 격자 밀도 · 판 위치) 와 그 차의 상한 (2차 B-spline 3h/2 = 0.21 µm @ dx 0.141 µm · 두께의 0.70 % · 기공 ≈ 0.6 %p [카드 산술 · §7-2]) 을 결과 전에 함께 등록 · 격자 밀도 (Fig. 7 꼴) 로 기공을 세면 경계에서 번진다 | 기공 · 밀도 값 없음 · 압밀 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각: 3D 64³ 셀 × 64 PPC = 16.8 million 입자 (한 속도장 · UCF) | 메모리 · 시간 [미확인] · 입자별 장 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★★ **이 논문의 몫** — MMS 두 꼴 (1D 주기 막대 식 47–50 · 3D 축 정렬 식 51–53 → 2D 판은 Z 를 뺀 꼴 · `sadeghirad2011_…` §3-1 이 2D 판을 썼다 [다른 카드]) · 체적력 유도 (TL · 식 43) · 오차 식 (54) · 단일 노드 상수 응력 시험 (식 42 · 노드 힘 = 0) · 안정 지도 (매끈함 길이 · CFL) · 경계 처리 셋의 수렴 차수 (Fig. 10–12) | 2D 계산 결과 없음 · 소성 · 거의 비압축 시험 없음 |
| **단계 3** (2D 접촉 표현 비교) | 넓은 기저가 접촉을 어렵게 한다는 문장 (*"modeling contact can present a challenge when wider basis functions are used"* p.13) · 대칭 경계의 extra node 거울 규칙 = 두 물체가 대칭으로 다가오는 가장 단순한 접촉 꼴 (p.9) → 한 속도장 ↔ 입자별 장 비교에서 **기저 지지 (3h) 가 가를 수 있는 최소 틈을 정한다** — 기저 · h · PPC 를 같이 적는다 [카드 추론] | 접촉 알고리즘 · 다물체 시험 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 경고만: 고정 PPC 격자 사다리가 적분 오차 바닥에서 멈추거나 커진다 (4 PPC 128 → 512 ×2.55 · 6 PPC 면 39 배 낮음 [판독]) → σ_y 를 기공에 맞출 때 격자 × PPC 수렴을 먼저 | 순수 SE · 항복 · 기공 없음 |
| **단계 5** (3D 복합 압밀) | AM 마스크 (AM 안 노드 0) = extra node Dirichlet 부류 → AM 표면 둘레 경계 기하 오차 최대 3h/2 = SE 지름의 21 % [카드 산술 · §7-2] — 피복 · 계면 응력을 AM 표면에서 h 거리 안으로 읽을 때 표지 | 복합 · 다물체 · AM 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 판 반력 wallP = 식 (30) 의 경계 가속도 × 질량 합과 같은 꼴 [카드 해석] → 판이 물러날 때 판 노드가 물질을 끌어당기는 (음의) 반력이 나오면 **분리 조건 없이 읽지 않는다** (이 논문의 Dirichlet 에도 분리가 없다) | 하중 제거 · 되튐 · 분리 없음 |
| **단계 7** (형상 · 피복 · 수송) | 격자에 투영한 장 (밀도 · 상 분율) 은 경계에서 h–3h/2 번진다 (Fig. 7) — 격자 장으로 피복 · 접촉을 세는 연산자에 같은 번짐 [카드 추론] | 피복 · 수송 없음 |
| **후보 D0** (지금 DEM) | 없음 (DEM 0 회) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | ★ Dirichlet 덮어쓰기 · 경계 가속도 두 방법 (0 ↔ 식 30 · UCF = 식 30 · *"very subtle"*) · 대칭 = 법선 0 (마찰 없는 미끄럼) · extra node 거울 (음수) · 주기 · 경계 수정 B-spline → 우리 판 (slip · 양방향) · 바닥 (separate) 규칙을 적을 때 **extra node 처리 (덮어쓰기 ↔ 거울) 를 따로 명시** · 1 차 수렴 예상을 시험으로 확인 | 분리 · 마찰 · 한쪽 조건 · 움직이는 경계 없음 |
| **후보 A** (MPM 강체 AM + SE 한 속도장) | AM 마스크 = 정지 Dirichlet 부류의 기하 오차 (§7-2) · 매끈한 기저일수록 AM 경계가 더 번진다 (h → 3h/2) | AM 운동 · 강체 결합 없음 (→ `hu2018_…` CPIC) |
| **후보 A′** (입자별 속도장) | 넓은 기저 = 접촉 어려움 (p.13) · 대칭 거울 = 두 물체 대칭 충돌의 경계 꼴 (p.9) | 다물체 마찰 접촉 없음 (→ `bardenhagen2000_…` · `homel2017_…`) |
| **후보 B** (입자별 FE + 접촉) | TL ↔ UL 동등 (p.15) — MMS 를 TL 로 만들어 UL 코드와 견주는 법은 FE 에도 같다 | 입자별 FE 없음 |
| **후보 C · C′** (큰 변형 · 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U0 꼴 '0 이어야 하는 양' 시험** = 상수 응력 → 노드 힘 0 (식 42) · **U1** = 입자 폭 ↔ 매끈함 길이 규칙 (Δx < l → 2 차 · Δx > l → 1 차 + 불안정 · Fig. 6 · 8) — 우리 2 PPC · 2차 B-spline 은 2 차 쪽 [카드 산술] · **U2** = MMS 수렴 시험 꼴 (경사면 마찰 회귀 자체는 없음) · **U4** = 판 분리 없음 (식 30 반력만) · **U6** = 고정 PPC 사다리의 바닥 · 상승 (Fig. 10) + 경계 처리에 따른 1 차 (Fig. 11–12) → 격자 × PPC × 경계 처리 엇갈림 · 시험 입자 배치는 국소 불균일 (초수렴 회피 · Fig. 6) | U3 (압흔 · 떼기) · U5 (입자 충돌) 없음 |
| **R1–R7** | **R2** — 대칭 = 마찰 없는 미끄럼 (분리 없음) · **R6** — 입자 영역 추적의 어려움 (F 한 점 · 직사각 χ_p 는 공간을 못 채움 · cpGIMP 는 대각만) = 'SE 형상' 을 입자 영역으로 들고 가기 어렵다는 2008 년 진술 (우리 MPM 은 입자 영역을 안 든다 [다른 카드 `sadeghirad2011_…` L515 · L522]) | R1 · R3 · R4 · R5 · R7 없음 |
| **결과 전 대조 항목** | ① 이 논문 1D 막대 MMS (A 0.05 · E 10⁴ · ρ₀ 1 · T = 1/C · Δt 4 × 10⁻⁶ · 8–512 셀) 를 우리 MPM 으로 — **주기 경계 = 2 차 (6 PPC 512 셀 RMS 3.7 × 10⁻⁶)** · **판 (extra node Dirichlet) = 1 차 (0.90–1.18)** 이 나오는지 · 고정 PPC 의 바닥이 몇 셀에서 오는지 ② 3D 축 정렬 MMS (ν 0.3) 의 차수 (cpGIMP 2.13 · 2.04 · 1.54 · 주기 B-spline 2.37 · 1.68 · 1.00) ③ uGIMP 안정 지도 (l = h 에서 CFL ≈1.2 · 1D) — 전부 [판독] 값 · 맞추는 데 쓰지 않음 | 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 무차원 탄성 (E 10⁴ · ρ₀ 1) ↔ 우리 MPM J2 소성 · E 1.53 GPa · ν 0.49 (거의 비압축) · DEM E_eff 1.35 GPa · 1D · 3D 축 정렬 ↔ 우리 3D 무질서 침대 · 탄성파 동역학 ↔ 준정적 판 압축 (≈300 MPa · 판 Mach 0.01–0.03) · 고른 입자 배치 ↔ DEM 덤프에서 씨앗 · 한 물체 ↔ AM 마스크 + SE.  ⇒ 값은 하나도 옮기지 않고 **시험 꼴 · 차수 · 기전 · 경계 오차의 크기 규칙**만 옮긴다.

## 9. 적용 인사이트 (행동)
1. **단위 시험 U2 · U6 = 이 논문 1D 막대 MMS 그대로** (식 47–50 · A 0.05 · E 10⁴ · ρ₀ 1 · T = 1/C · Δt 4 × 10⁻⁶ · 8–512 셀 · PPC 2 · 4 · 6 · 경계 = 주기 · 우리 판 방식 Dirichlet) — 결과 전 등록: 주기 = 2 차 · 판 방식 = 1 차 (Fig. 10–11) · 고정 PPC 바닥 위치.  같은 2차 B-spline 이라 차수 대조가 바로 된다 (힘 식 · APIC 차이는 한정으로).
2. **3D 축 정렬 MMS** (식 51–53) 를 ν 0.3 그대로 + **ν 0.49 판 하나** (우리 재료 쪽 · 거의 비압축에서 차수가 지켜지는지) — Fig. 12 와 대조.
3. **판 · AM 경계의 기하 오차 진단**: 정지 때 판 아래 물질점 맨 위 z ↔ wall_z (dx 단위) · AM 표면 둘레 h · 3h/2 띠 안의 응력 · 피복을 따로 보고 — 이 논문의 상한 감각 3h/2 (= 0.21 µm @ n_grid 384) 와 견준다.
4. **격자 사다리는 PPC 와 엇갈려** (2 · 3 · 4 PPC × 192 · 288 · 384) — 고정 PPC 사다리는 적분 오차 바닥에서 멈추거나 커진다 (Fig. 10) · 우리 비수렴 (d_h 절) 이 기하 해상인지 적분 바닥인지 가르는 대조 팔.
5. **시험 입자 배치는 국소 불균일하게** — 고른 간격은 초수렴으로 적분 오차를 숨긴다 (Fig. 6 캡션) · 우리 침대 씨앗은 원래 무질서라 시험 쪽만 해당.
6. **Courant 정의 확인**: dt = 0.4 dx/√M 의 M 이 P파 계수인지 — 막대 E 면 ν 0.49 에서 P파 기준 1.65 > 이 논문 1D 안정 끝 ≈1.2 (l = h) [카드 산술 · 1D ν 0 → 3D 전이 한정].
7. **판 반력 = 식 (30) 꼴**: 탈압 (단계 6) 에서 판 노드가 물질을 끌어당기는 음의 반력이 나오면 분리 규칙 (A′-0) 없이 해석하지 않는다.
8. **오차 보고 = RMS + 최대 둘 다, 정의 식과 함께** (이 논문은 RMS · Max 식을 안 적어 재현이 어렵다 · `gritton2017_…` §3-3 · `sadeghirad2011_…` §3-2 의 ÷N 노름 함정과 같은 부류).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In explicit MPM, the grid basis and the kinematic boundary treatment set the observed spatial convergence order: in 1-D manufactured-solution tests, piecewise-linear bases did not converge beyond 16 cells, whereas quadratic B-splines converged at second order with periodic boundaries or modified-boundary splines but only at first order when Dirichlet conditions were applied through extra (ghost) nodes (Steffen et al., *CMES* 31 (2008) 107–127)."
- "The grid representation of a material boundary can be in error by up to h, 3h/2, 2h and h + l/2 for piecewise-linear, quadratic B-spline, cubic B-spline and uGIMP bases, respectively (Steffen et al., 2008)."
- "For uGIMP, the internal-force quadrature error is second order in particle spacing when the smoothing length exceeds the particle width and first order otherwise; simulations became unstable when the smoothing length was close to or below the particle width (Steffen et al., 2008)."
- 국문 (한정어와 함께): *"명시적 MPM 에서 2차 B-spline 은 주기 경계 · 경계 수정 기저일 때 2 차로 수렴하지만, 경계 밖 (ghost) 노드에 Dirichlet 을 걸면 경계 기하 오차 (최대 3h/2) 때문에 1 차로 떨어진다 (Steffen 외 2008 · 1D · 3D 탄성 제조해 시험 · 소성 · 접촉 · 압밀 없음)."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-9 의 ①–⑦.
**카드가 본 한계**
1. **재료 · 하중이 우리와 다르다** — 무차원 탄성 · 탄성파 동역학 · 소성 · 거의 비압축 · 준정적 압밀 · 접촉 · 하중 제거 없음 → 오차 값 · 안정 CFL 을 우리 코드 기준으로 쓰지 않는다.
2. **3D 는 축 정렬 한 꼴** — 입자 영역이 늘 축에 맞아 cpGIMP 에 유리 · 일반 변형 대표 아님 (저자).
3. **2D 결과 없음** — 2D 판은 `sadeghirad2011_…` (다른 무리 · 2011).
4. **결과 그림의 정의 결손** — RMS · Max 식 · CFL 식 · §6.1 격자 수 · §6.3 Δt · T 미인쇄 → 값 대조는 [판독] · 정의 가정과 함께.
5. **원문 안 어긋남** (§3-9 의 1–10) — 매듭 겹침 오기 · '평탄' 이 실제로 상승 · cpGIMP '모든 해상도 2 차' 의 마지막 1.54 · 안정 문턱의 'etc.'.
6. **갱신 순서의 오차 분석은 이 논문에 없다** — 인용할 때 "구현 선택 = 기저 · 경계 · 매끈함 길이" 로 한정.
7. **우리 MLS-MPM 과 힘 식 · 입자 속도 전달이 다르다** (§7-4) — 차수 전이는 유추.
8. **경계 기하 오차의 '0.6 %p' 는 상한 감각** (카드 산술) — 측정 · 원문 값이 아니다.
9. 계산 비용 [미확인].

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄 · 정본 카드 없음 확인 = `papers/` 파일 목록 + grep)
| 서지 (원문 목록 그대로) | 왜 |
|---|---|
| Wallstedt, P. C.; Guilkey, J. E. (2008): An evaluation of explicit time integration schemes for use with the generalized interpolation material point method. To Appear In Journal of Computational Physics. | ★ **갱신 순서 (의도의 빠진 절반)** — 이 논문이 엇갈린 중앙 차분의 이득 · 시간 전진 비교를 넘긴 곳 (p.5 · p.10) · `sadeghirad2011_…` L109 의 USL ↔ USF 비교 원전 · 카드 없음 (정독 출력 wishlist 에 같은 논문 줄 있음) |
| Bardenhagen, S. (2002): Energy conservation error in the material point method for solid mechanics. Journal of Computational Physics, vol. 180, pp. 383–403. | ★ 두 시간 전진 알고리즘 (USL · USF) 의 에너지 오차 원전 (p.10) · 카드 없음 (bardenhagen 2000 · 2001 · 2004 · 2005 만 있다) |
| Steffen, M.; Kirby, R. M.; Berzins, M. (2008): Analysis and reduction of quadrature errors in the material point method (MPM). International Journal for Numerical Methods in Engineering. DOI: 10.1002/nme.2360. | ★ 도약 오차 C[[f^(p+1)]]Δx^(p+2) 의 원 분석 (p.11) · 0 기울기 경계 수정 B-spline (p.6) · `stomakhin2013_…` L64 의 'Steffen et al. 2008' 3차 B-spline 출처 후보 · 카드 없음 |
| Tran, L. T.; Kim, J.; Berzins, M. (2007): Solving Time-Dependent PDEs using the Material Point Method, A Case Study from Gas Dynamics. Technical Report UUSCI-2007-010, SCI Institute, University of Utah, 2007. | 셀 넘김 오차의 정밀 결정 · force kick 이 주는 시간 간격 제한 (p.5 · p.12–13 · p.18) · 카드 없음 |
| Wallstedt, P. C. (2008): On the Order of Accuracy of the Generalized Interpolation Material Point Method. PhD thesis, University of Utah, 2008. | 재료 경계의 MLS 표현을 적분에 넣은 일 (p.13) — 우리 판 · AM 경계의 기하 오차 대안 · GIMP 정확도 차수 · 카드 없음 |
| Wallstedt, P. C.; Guilkey, J. E. (2007): Improved velocity projection for the material point method. CMES: Computer Modeling in Engineering and Sciences, vol. 19, pp. 223–232. | 속도 투영 오차와 줄이는 법 (p.10) — 우리 APIC 전달과 견줄 자리 · 카드 없음 |
| Ma, J.; Lu, H.; Komanduri, R. (2006): Structured mesh refinement in generalized interpolation material point method (GIMP) for simulation of dynamic problems. CMES: Computer Modeling in Engineering and Sciences, vol. 12, pp. 213–227. | 질량 없는 모서리 입자로 입자 영역 추적 (p.3) — R6 · 카드 없음 |
| Love, E.; Sulsky, D. L. (2006): An energy-consistent material-point method for dynamic finite deformation plasticity. International Journal for Numerical Methods in Engineering, vol. 65, no. 10, pp. 1608–1638. | MPM 의 큰 변형 소성 · 에너지 일관 (참고문헌 안 유일한 'plasticity') · 카드 없음 |
| Nairn, J. A. (2006): Numerical simulations of transverse compression and densification in wood. Wood and Fiber Science, vol. 38, no. 4, pp. 576–591. | MPM 으로 세포 구조를 압축 · 치밀화한 선례 (p.1 이 성공 사례로 든 셋 가운데 하나) — 우리 압밀 MPM 의 선례 후보 · 카드 없음 (정본 `nairn2015_…` 는 같은 저자의 다른 논문 = 축대칭 GIMP) |
| Sulsky, D.; Kaul, A. (2004): Implicit dynamics in the material-point method. Computer Methods in Applied Mechanics and Engineering, vol. 193, no. 12-14, pp. 1137–1170. | 일관 질량 행렬 (p.4) · 암시 MPM · 카드 없음 |
| Bardenhagen, S.; Kober, E. (2004) · Bardenhagen, S. G.; Brydon, A. D.; Guilkey, J. E. (2005) · Sulsky, D.; Chen, A.; Schreyer, H. L. (1994) | 정본 카드 있음 (`bardenhagen2004_…` · `bardenhagen2005_…`) · Sulsky 1994 = 후보 표 N-40 |

## 13. [미확인] 목록 (본문 21 쪽 전수에 없음)
1. DOI · 접수 · 게재 날짜.
2. CFL 의 식 (§6.2 의 'Δt 4 × 10⁻⁶ ↔ 512 셀 ≈ 0.2' 는 CΔt/h 로 맞는다 [카드 산술]).
3. §6.1 (Fig. 8 · 9) 의 격자 수 · 입자 수 · 걸음 수.
4. §6.3 의 Δt · T · 걸음 수 · 'Max Error' 정의 · 1D 'RMS Error' 의 식.
5. §6 런의 시간 전진 판 (식 6 ↔ 식 11–15) · 경계 가속도 판 (0 ↔ 식 30).
6. Fig. 11 의 PPC (값으로 6 [카드 해석]) · Fig. 7 의 격자 간격 · 입자 수 (h ≈ 0.1 · 셀당 3 [카드 해석]).
7. 계산 시간 · 기계 · 병렬 수 · 1D 계산의 코드.
8. 3차 B-spline 의 식 (원문에 없다) — `stomakhin2013_…` 의 'Steffen et al. 2008' 이 어느 논문인지.
9. cpGIMP 다차원 갱신 (l_p⁰ diag(F)) 의 비대각 (전단 · 회전) 처리.
10. 1D 안정 시험의 매끈함 길이 사다리 간격 (그림 꼭짓점 0.025h [판독]) · 8 PPC 의 l = h/8 점 (그림 축 시작 0.1 · 첫 점 0.15).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 21 쪽 (+ 빈 22 쪽째: 글자 0 · 그리기 0 · 이미지 0) 을 글자 층 추출 + 쪽 렌더로 읽음.  서지 = 첫 쪽 머리 (*"Copyright © 2008 Tech Science Press · CMES, vol.31, no.2, pp.107-127, 2008"*) · 저자 다섯 · 소속 · 교신 (Guilkey) · 감사 (C-SAFE · W-7405-ENG-48) · 참고문헌 33 건 (저자–연도 꼴) · PDF 정보 (main.dvi · 2008-10-03 · dvips 5.96 → Acrobat Distiller 8.1.0).  이 논문 DOI 는 원문 어디에도 없다 (원문 안 DOI = 인용 IJNME 논문 하나).
- 원문 낱말 셈 (리가처 처리 뒤): DEM 0 · 'discrete' 1 (discretizing) · 'plastic' 1 (참고문헌 제목) · 'contact' 2 (초록 · p.13) · 'unload' 0 · 'friction' 1 (frictionless) · 'granular' · 'powder' · 'sphere' 0 · 'USL' · 'update stress' 0 · 'Kronecker' 1 · 'Dirac' 1 · 'UCF' 9 · 'PPC' 17.
- 그림 크롭 **74 장** = 그림 13 (도구 5 = Fig. 1 · 6 · 8 · 12 · 13 · 그 가운데 도구의 fig_12 는 같은 쪽 Fig. 13 그림이라 **다시 자름** · 손 크롭 8 = Fig. 2 · 3 · 4 · 5 · 7 · 9 · 10 · 11 — 도구가 벡터 그림을 "그래픽 없음 · 영역 없음" 으로 놓침) + 식 **41** (번호 식 (1)–(54) 전부 · 인쇄 덩어리대로 묶음 · 400 dpi · 다시 자름 2 = `eq_34` 의 이웃 줄 'tion:' · `eq_45_46` 의 'respectively:' 조각) + 근거 문단 **20** (300 dpi).  74 장 전부 Read 로 열어 확인 · `figures.json` 의 `manual_crop` · `recrop` · `note_manual` · `missing_labels_resolved`.  표 없음.
- 판독: digitized.csv 303 행 — 기준선 기울기 점검 2.000 · 1.000 · 2.001 · 1.001 · 1.999 [판독] · Fig. 11 경계 spline 줄 = Fig. 10 6PPC 줄 (≤ 0.05 %) · Fig. 11 주기 줄 ≠ Fig. 10 4PPC 주기 줄 · Fig. 3 곡선 수 (2차 7 · 3차 8 · 끝 함수 = 1 — 경로 꼭짓점의 값이 식 (22)(23) 의 2차 · 3차 B-spline 값과 맞음 (예: x = 1.739 에서 N₁ = 0.034 · N₂ = 0.693 · N₃ = 0.273 [판독 · 카드 산술])).
- 식 확인 [카드 산술]: 식 (39) + (a₁ = a₃ = 0 · a₂ = −2/(hl)) → 식 (40) · 식 (49) = 식 (43) + (50) 에서 유도 · 식 (53) 같은 방법 · 식 (29) 에 l_p = h → 식 (21) · CΔt/h = 0.2048 (512 셀) · 입자 수 32,768 · 16,777,216 (인쇄 16.8 million) · 매듭 겹침 k − 1 ↔ 함수 수 N + k − 2 (§3-9 ②).
- 2 차 인용 대조: `gritton2017_…` (L86 · L91 · L230–235 · L349 · L358) · `stomakhin2013_…` L64 · `bardenhagen2004_…` (L293 · L430 · L494 · L595) · `comparison_vs_ours_DEM.md` L3035 · `sadeghirad2011_…` L109 — 고치지 않음 (카드 문제 = 정독 출력 `batch_77_findings.md` 의 '카드 문제' 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + 'steffen' · 'Examination and analysis of implementation' · 'Wallstedt' grep → 카드 없음 (stomakhin2013 L64 의 인용 · sadeghirad2011 L109 의 Wallstedt 인용뿐) (2026-11-12).

## 🔗 관련 카드
- 가리킨 카드 (이 논문 = ref. [34] · 같은 Utah · Uintah 무리): `gritton2017_mpm_chemomechanical_coupling_silicon_anode`.
- GIMP 계보: `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` (GIMP 원전 · 이 논문 §3.3) · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` (uGIMP · cpGIMP 뒤의 CPDI · 같은 축 정렬 MMS 2D) · `bardenhagen2005_mpm_foam_densification_simulation` (cpGIMP 의 3D 큰 압축 · Guilkey 공저 · 이 논문 p.1 의 성공 사례) · `nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions` (uGIMP · CPDI 의 축대칭 판 · 축 r = 0 에서 입자 영역 자르기 — 이 논문의 경계 처리 · 기하 오차와 같은 부류의 축 경계 문제 · 같은 날 반입).
- 우리 MPM 이산화 · 경계: `hu2018_mls_mpm_cpic_two_way_rigid_coupling` (MLS-MPM · 우리 코드 줄 대응 · CPIC 경계) · `stomakhin2013_mpm_snow_elastoplastic` (B-spline 기저 인용).
- MPM 접촉 · 다물체: `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact`.
- MPM 개관 · 압밀: `devaucorbeil2020_mpm_after_25_years_review` · `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
