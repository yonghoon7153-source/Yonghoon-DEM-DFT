# MPM 다물체 접촉 개정판 — 수직 견인력으로 분리 판정 (압축이면 접촉 유지) + 작은 격자 질량의 격자 붕괴 안정화 (γ) · 3D 구 해석해 · 원판 광탄성 대조 ★★ 제하 (unloading) 에 필요 — Bardenhagen, Guilkey 외 4 인 (CMES 2001)

> slug `bardenhagen2001_mpm_improved_contact_granular_stress_waves` · DOI `[미확인]` (PDF 에 DOI 미인쇄) · type `MPM (명시적 MPM 다물체 접촉 개정 — 견인력 기반 분리 판정 + 격자 붕괴 안정화 스케일 γ · 3D 구 해석해 검증 · Plexiglas 원판 광탄성 응력파 대조)` · PDF `59a087ce-7._An_improved_contact_algorithm_for_the_material_point_method_and_application_to_stress_propagation_in_granular_material.pdf` · digested `2026-11-09` · status ✅
>
> ⚠ **먼저 읽을 것** — ① **압밀 계산이 없다**: 검증은 고무 같은 구 1 개 (경사면 · backspin), 응용은 원판 4–5 개의 **동적 응력파**다.  ② 재료는 neo-Hookean 무른 구 (K 6 MPa) 와 **파속 단위만 맞춘 가상 Plexiglas** (G 72 GPa · K 102 GPa) — 절대값 전이 0 건.
> ③ 실험 대조는 저자 표현으로 *"excellent qualitative agreement"* — 정량 일치는 주장하지 않는다 (프레임 시간에 계통 차).
> ④ PDF 는 OCR 스캔본 (ABBYY FineReader) 이고 **PDF 메타데이터가 다른 문서의 것** (제목 *Rates of herbivory on different tropical trees*, 저자 *Coley, Phyllis D.*) — 서지는 **본문 인쇄만** 따랐다.  식은 렌더 이미지로 판독 (식 그림 `eq_*.png` 동봉).
> ⑤ 그림에서 읽은 값 (`figure-read ≈`) 은 추세 전용 — 정밀값으로 쓰지 않는다.
>
> 짝 카드: `bardenhagen2000_mpm_granular_multibody_frictional_contact` = 이 논문이 *"Bardenhagen, Brackbill, and Sulsky (2000a)"* 로 부르는 **원판 알고리즘**.  이 카드는 **무엇이 바뀌었나** 에 집중하고 공통 부분은 짝 카드로 넘긴다.

---

## 0. 이 논문이 우리에게 왜 중요한가

[DEM 우선 (수영)] 트랙은 AM + SE 를 **가압부터 제하까지** 한 모델로 누르기를 원한다.  2000 판 알고리즘 (짝 카드) 은 *"다가오면 구속, 멀어지면 자유"* 라는 **운동학 판정**만 써서, 눌렸던 계면이 되돌아갈 때 *"instantaneous removal of the boundary"* — 쌓인 변형 에너지를 제대로 돌려받지 못한다.  이 논문의 첫 개정이 바로 그 자리다:

> *"The essential modification to the contact algorithm logic is to **apply frictional contact when the normal traction is compressive**, allowing free separation otherwise."* (p.512)

즉 **수직 견인력 t_n = n·σ·n 이 아직 압축 (t_n < 0) 이면 계면을 계속 접촉으로 두고, 0 이상이 되어야 떨어뜨린다** — 제하에서 계면이 응력 0 까지 풀린 뒤 분리되게 하는 장치.  그리고 같은 절에서 **우리 AM (강성 · 탄성) + SE (무름 · 소성) 계면에 정확히 해당하는 한계**를 스스로 적는다:

> *"Because different materials respond to the same stretch with different stresses, the normal tractions which develop during contact will likely be different for different bodies.  It is even possible that uniform un-straining will result in bodies of different materials experiencing free separation at different times during departure, **particularly when material response allows for permanent set (e.g. plasticity)**.  Although traction equilibrium is not maintained at contact nodes, interfaces are unloaded to their stress free state."* (p.512)

두 번째 개정 (격자 붕괴 안정화 γ) 은 물질점이 처음 셀에 들어올 때 생기는 아주 작은 격자 질량에서 접촉 보정이 폭주하는 것을 막는다 — 수만 개 접촉이 켜지고 꺼지는 압밀에서 피할 수 없는 상황이다.

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| 후보 A′ 의 **구현 기준판** (2000 판보다 나중 · 정리된 꼴) | 식 (4)–(13) — 물체별 운동량 · 질량중심 속도 · 접촉 노드 · 접근 판정 · 견인력 판정 · 속도 갱신 한 줄 |
| **제하 · 분리** 가 물리적으로 맞으려면 무엇이 필요한가 | 견인력 기반 분리 (식 9) + 이유 (에너지) + **이종 · 소성 계면의 한계 (위 인용)** |
| 접촉 MPM 의 **수치 안정** 장치 | 식 (17)–(22) · γ = 0.5 (0.5–1 둔감, 0.5 미만 침투) |
| 3D **회귀 시험** | 구 경사면 (미끄럼 · 구름) 해석해 식 (23)(24) · backspin 식 (25)(26) · 해상도 R/2 · R/4 · R/8 |
| 접촉 조건이 **하중 경로 · 응력 전달 속도**를 바꾼다는 실험 대조 | Fig 9–11 (한 줄 · 지그재그 미끄럼 μ 0.5 · 접착 μ ∞) |
| 위상 가정의 명시 | *"no more than two bodies be represented at a contact grid node"* — 3D 조밀 압밀에 대한 경고로 읽힘 |

---

## 1. 한 줄 요약

**KR:** 2000 판 MPM 다물체 접촉 (물체별 격자 속도장 ↔ 질량중심 속도장 비교) 을 두 가지로 고친다 — ① 분리 판정에 **접촉 노드의 수직 견인력**을 넣어 압축 (t_n < 0) 인 동안은 마찰 접촉을 유지하고 그렇지 않을 때만 자유 분리 (처음 닿을 때처럼 응력이 없으면 접근 여부로 판정), ② 물체의 격자 질량이 아주 작은 노드에서 접촉 속도 보정이 셀을 무너뜨릴 만큼 크면 **ε̇_max Δt < γ** 가 되도록 보정을 비례 축소 (γ = 0.5).  운동량 보존 · 전역량만 쓰는 이웃 탐색 없는 구조 · 물체 수에 선형인 비용은 그대로.  3D 무른 구의 경사면 (미끄럼 · 구름) · backspin 이 강체 해석해로 수렴 (지름당 8 셀 이상; 4 셀이면 '평평한 점' 때문에 구르지 못함) 하고, Plexiglas 원판 광탄성 실험에서 한 줄 · 지그재그 (μ 0.5) · 접착 (μ ∞) 세 경우의 무늬 · 하중 경로를 정성적으로 재현한다 (프레임 시간은 시뮬이 빠르다 — 재료 물성 탓으로 해석).

**EN:** Two improvements to the 2000 MPM multi-body contact algorithm: (i) the release logic now uses the normal traction at contact nodes — frictional contact is kept while the traction is compressive and free separation is allowed only otherwise (approach alone decides for stress-free bodies), so strain energy is extracted on departure instead of the boundary being "instantaneously removed"; (ii) a cell-collapse stability criterion, ε̇_max Δt < γ, scales the contact velocity change when a body's grid mass is tiny ("unfortunate registration"), with γ = 0.5.  Momentum conservation, use of global grid quantities (no neighbour search) and linear cost are preserved.  3D deformable-sphere tests (incline slip/no-slip, backspin) converge to rigid-body solutions once the sphere spans ≥ 8 cells (4 cells → flat spot, no rolling), and photoelastic stress-wave experiments on Plexiglas disks (collinear, zig-zag sliding μ 0.5, glued μ ∞) are reproduced qualitatively, with simulated fringes systematically faster — attributed to uncertain material properties (Poisson's ratio).

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **An Improved Contact Algorithm for the Material Point Method and Application to Stress Propagation in Granular Material** |
| 저자 | **S.G. Bardenhagen** (1) · **J.E. Guilkey** (2) · **K.M. Roessig** (3) · **J.U. Brackbill** (4) · **W.M. Witzel** (5) · **J.C. Foster** (6) |
| 소속 | (1) Dept. of Mechanical Engineering, University of Utah, Salt Lake City, UT 84112, USA — *Presently on leave from Group ESA-EA, MS P946, Los Alamos National Laboratory* · (2) Dept. of Mechanical Engineering, University of Utah · (3) Air Force Research Laboratory, Munitions Directorate, Eglin AFB, FL 32542, USA · (4) Theoretical Division, Los Alamos National Laboratory, Los Alamos, NM 87545, USA · (5) Dept. of Computer Science, University of Utah · (6) Air Force Research Laboratory, Munitions Directorate, Eglin AFB |
| 교신저자 | **[미확인]** (표지 없음) |
| 저널 | **CMES, vol. 2, no. 4, pp. 509–522, 2001** · Copyright © 2001 **Tech Science Press** — 저널 전체 이름은 PDF 에 인쇄돼 있지 않다 (약어 *CMES* 만) → 전체 이름 [미확인] |
| DOI | **[미확인]** (PDF 미인쇄) |
| 접수 · 게재일 | **[미확인]** (미인쇄) |
| 키워드 (인쇄) | Contact Algorithm, Material Point Method, Wave Propagation, Granular Material |
| 분량 | 14 쪽 (pp. 509–522) · Figure 1–11 · 식 (1)–(26) · 표 없음 |
| 연구 유형 | 수치 방법 (접촉 알고리즘 개정) + 3D 검증 (강체 해석해) + 원판 응력파 시뮬 (차원 미기재) ↔ 광탄성 실험 대조 |
| 자금 | U.S. Department of Energy — **Center for the Simulation of Accidental Fires and Explosions**, grant **W-7405-ENG-48** |
| 인용하는 선행 판 | *Bardenhagen, Brackbill, Sulsky (2000a)* = CMAME 187, 529–541 (짝 카드) · (2000b) Phys. Rev. E 62, 3882–3890 (2D 전단 응력 분포) · (2000c) 11th Int. Detonation Symp., 547–555 (전단 변형 — 견인력 논리를 *"described in detail 하지 않고"* 이미 사용) |
| PDF 상태 | ABBYY FineReader OCR 스캔 · 배경 쪽 이미지 150 dpi + 그림은 ≈ 300–350 dpi 내장 래스터 (Fig 1–4 · 6–11; Fig 5 는 배경 쪽 이미지에만) · **메타데이터 오기 (다른 문서)** |

---

## 3. ★★★ 2000 → 2001: 무엇이 바뀌었나 · 왜

| 축 | 2000 판 (짝 카드) | 2001 판 (이 카드) | 왜 바꿨나 (원문 근거) |
|---|---|---|---|
| **분리 (해제) 판정** | 운동학만: (v^g − v)·n > 0 이면 구속, 아니면 자유 분리 | **수직 견인력 포함**: t_n^α = n^α·σ^α·n^α 가 **압축 (< 0) 이면 마찰 접촉 유지**, 아니면 자유 분리 · 응력 없는 첫 접촉은 접근 여부로 | 강체 벽에 부딪혀 되튀는 변형체에서 *"If free separation is prescribed as soon as departure begins, the equivalent scenario is instantaneous removal of the boundary"* → 되튈 때 변형 에너지 회수가 안 맞음.  *"Without this logic modification, frictionless collisions were found to slightly increase system energy"*; 고친 판은 *"slightly dissipative"* (2000c) |
| **수치 안정** | 없음 | **격자 붕괴 조건** ε̇_max Δt < γ (0 < γ ≤ 1) 로 접촉 속도 보정을 비례 축소 · γ = 0.5 | 물질점이 처음 셀에 들어올 때 그 물체의 격자 질량이 아주 작아 (*"unfortunate registration"*) 보정 속도가 폭주 → 운동학이 갑자기 튐 (시간 간격에 따라 발생) |
| 기호 · 꼴 | 알갱이 g, 노드 i, 속도 비교 | 물체 α, **운동량 p^α / 질량 m^α** (식 4) · 질량중심 v^cm = Σp^α/M (식 5) | 운동량으로 쓰면 질량이 작은 노드에서도 위치 · 속도 갱신이 깔끔 (Sulsky, Zhou, Schreyer 1995) — 단 변형률 계산엔 격자 속도가 필요해 여전히 문제 |
| 접촉 노드 | "두 장이 다르면" | **v^cm − v^α ≠ 0** (식 7) · *"Resolution of the interface is commensurate with the computational grid cell size"* | 같은 정의를 명시 |
| 법선 | 요소 중심 밀도 (2차 B-spline) 의 기울기 (식 24, 2000) | *"Spatial differentiation of the individual body masses on the grid, m^α"* (세부 미기재) | 서술만 바뀜 — 같은 방법인지 [미확인] |
| 갱신식 | ṽ = v − [(v−v_cm)·n](n + μ′ n × ω̂) | **ṽ^α = v^α − Δv_n^α (n^α + μ′ t^α)**, μ′ = min(μ, Δv_t^α/Δv_n^α) (식 10) | 같은 내용을 Δv_n · Δv_t 로 정리 |
| 위상 가정 | 명시 없음 (알갱이 수 제한 없음) | **접촉 노드당 물체 ≤ 2** 로 분석을 좁힘 · N > 2 에선 일부 성질 불성립 | 붙음/미끄럼 동시성 · 운동량 보존을 증명하려고 |
| 운동량 보존 | "공통 법선이 아니라 작은 오차" | 붙음 = **정확히 보존** (식 15) · 미끄럼 = 법선이 공선 (n² = −n¹, t² = −t¹) 일 때만 (식 16) | 오차의 원인을 *"poor resolution of interface curvature"* 로 특정 |
| 검증 차원 | 2D 원판 | **3D 구** (경사면 · backspin) | — |
| 실험 대조 | 문헌 정성 비교 (전단) | **특정 미세구조의 광탄성 실험과 직접 대조** (처음이라고 명시) | *"a direct comparison of experimental and numerical results for a specific microstructure was never made"* |
| 지킨 것 | — | 운동량 보존 · 전역량만 사용 (이웃 탐색 없음) · 물체 수에 선형 · 물체 모양이 복잡해도 알고리즘 복잡도 불변 | 초록 · §2.1 |

---

## 4. 핵심 수치

> **라벨 규약** · `stated` = 본문 · 캡션 · `derived(ours)` = stated 에서 산술로만 · `figure-read ≈` = 그림 판독 (추세 전용)

### 4-1. 3D 검증 — 구 경사면 · backspin (§3.1–3.2, Fig 2–8)

| 항목 | 값 | 라벨 |
|---|---|---|
| 차원 | **3D** (대칭면이 있고, 그에 수직한 방향은 구와 원기둥을 구분하는 용도뿐) | stated |
| 구 반지름 R · 평판 길이 | **1.6 m · 20 m** | stated |
| 중력 | **10 m/s²** (모든 계산) | stated |
| 경사 표기 | θ = z 방향 (평판 법선) 과 중력 사이 각 | stated |
| 격자 | 균일 · 등간격 · **셀당 물질점 8 개** · 기본 셀 **R/4** (지름당 8 셀) | stated |
| 재료 | 구 · 평판 모두 **압축성 neo-Hookean 초탄성** — 구: 체적계수 **6 MPa** · 전단계수 **3 MPa** · 밀도 **1000 kg/m³** ("roughly approximating … natural rubber"); 평판: 탄성상수 · 밀도 **10 배** (같은 파속, 훨씬 단단) | stated |
| 종파속 | **100 m/s** | stated (산술 √((6 + 4)·10⁶/1000) = 100 ✓) |
| ⇒ 구 E · ν | **7.71 MPa · 0.286** | derived(ours) |
| 시간 단계 수 | R/4 해상도에서 전형 **500 time steps** | stated |
| 접촉 스케일 γ | **0.5** (모든 사례) · 0.5 ≤ γ ≤ 1 에서 둔감 · **γ < 0.5 이면 접촉 중 침투** · 권장 0.5 ≤ γ ≤ 1 | stated |
| 사례 1 "no slip" | θ = **π/4**, μ = **0.495** → 강체 해: x(t) = (25√2/14) t² (식 23) | stated |
| 사례 2 "slip" | θ = **π/3**, μ = **0.286** → 강체 해: x(t) = (5/2)(√3 − 2/7) t² (식 24) | stated |
| ⇒ 체제 문턱 (속 찬 구) | 미끄럼 iff tanθ > (7/2)μ — 사례 1: 1 < 1.733 (구름) · 사례 2: 1.732 > 1.001 (미끄럼) | derived(ours) |
| t = 2 s 위치 (강체 해) | 사례 1 **10.10 m** · 사례 2 **14.46 m** | derived(ours) (식 23 · 24) |
| t = 2 s 위치 (변형 구, R/4) | 사례 1 ≈ 7.5 m · 사례 2 ≈ 13 m | figure-read ≈ (Fig 3) |
| 해상도 연구 (사례 1) | 셀 **R/2 (지름 4 셀) · R/4 (8) · R/8 (16)** — R/2 는 **'평평한 점' 때문에 구르지 못함** (x = 0 그대로, 속도는 0 둘레 진동), R/4 · R/8 은 강체 해로 수렴 | stated |
| t = 2 s 위치 (해상도별) | R/2 = 0 · R/4 ≈ 7.4 · R/8 ≈ 9.7 · 강체 10.1 m | figure-read ≈ (Fig 5) |
| backspin | θ = 0 (수평), **R = 1 m**, μ = **0.5**, 초기 각속도 **5 rad/s**, 초기 질량중심 속도 0 · 해상도 R/4 · R/8 | stated |
| backspin 강체 해 | x − x0 = (5/2) t² (t ≤ 2/7) · = (5/2)(2/7)² + (10/7)(t − 2/7) (t > 2/7) — **t = 2/7 s 에 미끄럼 끝** | stated (식 25 · 26) |
| ⇒ 정착 속도 | **10/7 ≈ 1.43 m/s** (= (2/7)·ω₀R) | derived(ours) |
| backspin 변형 구 (t = 3 s) | 강체 ≈ 4.08 · dx = 0.125 ≈ 3.95 · dx = 0.250 ≈ 3.5 m · 속도는 1.43 둘레 진동 (dx 0.250: ≈ 1.05–1.75 m/s) | figure-read ≈ (Fig 7 · 8) |

### 4-2. 광탄성 응력파 — 원판 실험 ↔ 시뮬 (§3.3, Fig 9–11)

| 항목 | 값 | 라벨 |
|---|---|---|
| 실험 원판 | **Plexiglas, 지름 2 in, 두께 1/4 in** | stated |
| 실험 장치 | mild steel 하중 틀 (치수 조절) · 원판을 평면에 잡는 **1/4 in 홈** · **split Hopkinson bar** 하중 · 원판과 같은 두께의 하중 핀 → 평면응력 · 고속 카메라 (Hopkinson bar 의 파동으로 트리거) | stated |
| 타격자 속도 | **5.6 m/s** | stated |
| 도착 시각 불확도 | **± 10 µs** (첫 원판, "impact") — 프레임 사이 간격은 훨씬 정밀 | stated |
| 실험 종파속 · 통과 시간 | **0.27 cm/µs** (Marsh 1980) → 원판 하나 **19 µs** | stated (산술 5.08/0.27 = 18.8 ✓) |
| 시뮬 원판 · 재료 | 지름 **1 cm** · **선형 hypoelastic** · 전단계수 **72 GPa** · 체적계수 **102 GPa** · 밀도 **1900 kg/m³** → 종파속 **1 cm/µs** (통과 1 µs) — 실제 Plexiglas 가 아니라 **단위 기하 · 파속을 지정**한 값 | stated |
| ⇒ ν | **0.214** (논문: ν = 0.22) | derived(ours) ✓ |
| 시뮬 해상도 | 원판 지름당 **80 셀 · 셀당 물질점 1 개** | stated |
| 무늬 계산 | 응력 텐서 대각화 → 면내 주응력차 (∝ 면내 최대 전단) → **cos(차 / 무늬 밀도 계수)** · 계수는 한 줄 배치로 눈으로 맞춘 뒤 고정 | stated |
| 무차원 프레임 시간 | (충격 뒤 시간) / (원판 하나 종파 통과 시간) | stated |
| **Fig 9 한 줄 4 원판** | 실험 **2.6 · 6.6 · 9.2** ↔ 시뮬 **2.2 · 5.5 · 7.7** | stated |
| **Fig 10 지그재그 5 원판, μ 0.5 (벽 무마찰)** | 실험 **5.3 · 10.5 · 15.8** ↔ 시뮬 **3.0 · 6.0 · 9.0** | stated |
| **Fig 11 지그재그 접착 (시뮬 μ = ∞, 벽 무마찰)** | 실험 **1.6 · 4.2 · 6.8** ↔ 시뮬 **1.4 · 3.6 · 5.8** | stated |
| ⇒ 시뮬/실험 시간비 | 한 줄 **≈ 0.84** · 지그재그 미끄럼 **≈ 0.57** · 지그재그 접착 **≈ 0.86** | derived(ours) |
| ν 민감도 (한 줄 배치, 종파속 고정) | ν **0.22 → 0.48** 에서 무늬 속도 **2 배 넘게 감소** · 무늬 모양은 덜 민감 | stated |

### 4-3. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 압밀 · 치밀화 · 기공률 · 제하 곡선 | **없음** |
| 에너지 시계열 (증가 · 소산의 크기) | **없음** — 산문 진술뿐 ("slightly increase" · "slightly dissipative") |
| 광탄성 시뮬의 차원 (2D/3D) | **[미확인]** (원판 · 평면응력 실험이나 시뮬 차원은 명시 없음) |
| 광탄성 시뮬의 시간 간격 · 총 단계 | **[미확인]** |
| 접근 판정 (8) 과 견인력 판정 (9) 을 합치는 정확한 규칙 | 산문뿐 — 아래 §5-3 은 **우리 판독** |
| t_n^α 를 노드에 보간하는 가중 · 법선 계산 세부 | **[미확인]** ("interpolating individual material point contributions using the surface normals") |
| 노드당 물체가 3 이상일 때의 처리 | **없음** (분석을 N = 2 로 좁힘) |
| 반발 · 감쇠 계수 | **없음** — *"perfectly inelastic collision"* |

---

## 5. 방법 ★

### 5-1. MPM 요약 (§2, 식 1–3)

질량 보존 dρ/dt = −ρ∇·v (1) · 물질미분 (2) · 운동량 ρ dv/dt = ∇·σ (3).  물질점에 고정 질량 → 질량 보존은 자동.  운동량은 격자에서 풀고 **변화량만** 물질점에 보간 (FLIP 꼴 — 수치 확산 감소).  에너지 보존 오차는 시간 간격의 제곱에 비례 (Brackbill & Ruppel 1986; Bardenhagen 2001).  구성식: 초탄성 · hypoelastic · 소성 · 점탄성 구현.  세부 명시적 알고리즘은 Sulsky 1994 · 1995 · 1996 로 넘긴다.

### 5-2. ★★★ 접촉 알고리즘 개정판 — 단계별 (§2.1, 식 4–13)

1. **물체별 P2G**: 물질점의 질량 · 운동량을 **물체마다** 격자에 보간.  물체 α 의 격자 속도 **v^α = p^α / m^α, α = 1…N** (4).
2. **질량중심 속도 (전역량)**: **v^cm = Σ_α p^α / M** (5), **M = Σ_α m^α** (6) — *"the global quantities which enable the determination of contact grid nodes and precisely what the contact constraints should be"*.
3. **접촉 노드**: **v^cm − v^α ≠ 0** (7).  계면 해상도 = 격자 셀 크기.
4. **법선**: 물체별 격자 질량 m^α 의 공간 미분 → n^α.
5. **접근 판정**: **(v^α − v^cm)·n^α > 0** (8).
6. **견인력 판정 (개정 ①)**: 접촉 노드에서 물질점 응력을 법선으로 보간 — **t_n^α = n^α·σ^α·n^α** · 압축 = 음수 → **t_n^α < 0** (9).  *"apply frictional contact when the normal traction is compressive, allowing free separation otherwise"* · 응력 없는 물체 (처음 닿음) 는 접근 여부로 충분.
7. **마찰 접촉 갱신** (붙음/미끄럼 자동 선택):
   > **ṽ^α = v^α − Δv_n^α (n^α + μ′ t^α),   μ′ = min(μ, Δv_t^α / Δv_n^α)**    (10)
   > Δv^α = v^α − v^cm (11) · Δv_n^α = Δv^α·n^α (12) · Δv_t^α = Δv^α·t^α (13)

   μ = 계면 마찰계수, **t^α = 미끄럼 방향의 단위 접선**.  ⚠ 괄호 *"(t = ω × n in Bardenhagen, Brackbill, and Sulsky (2000a))"* 는 2000 판 식 (22)(23) 의 **n × ω̂** 와 곱 순서가 반대 — ω̂ 정의가 같다면 부호가 뒤집힌다 [우리 판독].  본문 정의 (미끄럼 방향 = 상대 접선 속도 방향) 를 따르면 두 판은 같은 갱신이다.
8. **자유 분리**: 아무 구속도 걸지 않는다 (v^α 그대로).
9. **효율**: 견인력 논리가 효율을 해치지 않음 — 질량중심 틀이라 별도 접촉 탐지 없음 · 격자 한 번 훑기 · 물체 수에 선형 · **물체 모양이 복잡해도 알고리즘 복잡도는 같다** (*"complex initial geometries and large deformations can easily be modeled"*).

### 5-3. 분리 판정 — 2000 ↔ 2001 (산문을 표로 · **우리 판독**)

| 접촉 노드의 상태 | 2000 판 (운동학) | 2001 판 (견인력) |
|---|---|---|
| 접근 · 응력 없음 (처음 닿음) | 마찰 접촉 | 마찰 접촉 (접근으로 판정) |
| 접근 · 압축 (t_n < 0) | 마찰 접촉 | 마찰 접촉 |
| **이탈 · 아직 압축 (t_n < 0)** — 되튀는 중 | **자유 분리** (경계 즉시 제거) | **마찰 접촉 유지** → 변형 에너지 회수 |
| 이탈 · t_n ≥ 0 | 자유 분리 | 자유 분리 |
| 접근 · 인장 (t_n > 0) | 마찰 접촉 | 산문 "압축이 아니면 자유 분리" 와 "접근이면 접촉" 이 엇갈림 — **명시 없음 [미확인]** |

### 5-4. N = 2 성질 · 운동량 (식 14–16)

- 위상 가정: *"Resolution of the topology of contacting surfaces on the computational grid requires **no more than two bodies** be represented at a contact grid node.  The remaining contact node analyses are specialized for N = 2.  It should be noted that **not all of the properties derived below hold for N > 2**."*
- 질량중심 정의에서 **Σ_{α=1}^{2} m^α Δv^α = 0** (14) → Δv_t¹/Δv_n¹ = Δv_t²/Δv_n² → **두 물체가 함께 붙거나 함께 미끄러진다** (이 비 등식은 두 법선이 공선일 때 성립 — 우리 판독).
- **붙음 = 운동량 정확 보존**: Σ m^α(ṽ^α − v^α) = −Σ m^α Δv^α = 0 (15).
- **미끄럼**: Σ m^α(ṽ^α − v^α) = −Σ m^α Δv^α·n^α n^α − μ Σ m^α Δv^α·n^α t^α (16) — 일반적으로 보존 안 됨; 오차는 *"non-collinearity in the calculation of body normals and tangents, i.e. poor resolution of interface curvature"* · n² = −n¹, t² = −t¹ 이면 정확 보존.

### 5-5. 격자 붕괴 안정화 (개정 ②, §2.2, 식 17–22)

- **문제**: 물체의 물질점이 그 물체가 없던 셀에 처음 들어가면 그 노드의 보간값 (격자 질량) 이 아주 작다 — 물체 가장자리에서 생기므로 접촉에 특히 중요.  두 물체가 다가가고 떨어질 때 한쪽 격자 질량이 0 으로 가는 것이 흔한 장면.  그때 접촉이 지시하는 속도 변화가 매우 커진다 (식 15 참조).  운동량으로 쓰면 위치 · 속도 갱신은 괜찮지만 **변형률 계산엔 격자 속도가 필요해 여전히 문제** · *"these unfortunate registration events are marked by abrupt changes in the kinematics of the contacting bodies, the occurance of which is time step size dependent."*
- **기준 (Courant 와 느슨히 닮음)**: 접촉이 한 시간 간격에 셀을 무너뜨리거나 뒤집을 만큼 속도를 바꾸면 안 된다.
  - 접촉이 부과한 순간 변형률 속도 **ε̇_j^α = (ṽ_j^α − v_j^α)/Δx_j** (17) (Δx_j = 좌표 방향 격자 간격)
  - 조건 **ε̇_max^α Δt < 1** (18), ε̇_max^α = max_j ‖ε̇_j^α‖
  - (14) 로 두 물체를 잇는다: ε̇_j² = −(m¹/m²) ε̇_j¹ = m¹/(M − m¹) ε̇_j¹ (19) — ⚠ 두 번째 등호에서 부호가 빠졌다 (M − m¹ = m² 이므로) [우리 판독]; 크기만 쓰는 (20) 에는 영향 없음.
  - 두 물체 중 가장 심한 값을 물체 하나의 양 + 전역량으로: **ε̇_max = max_j( max(m^α/(M − m^α), 1) ‖ε̇_j^α‖ )** (20)
  - 안전계수: **ε̇_max Δt < γ, 0 < γ ≤ 1** (21)
  - 비례 축소: **ṽ^α_scaled = v^α − max(γ/(ε̇_max Δt), 1) Δv_n^α (n^α + μ′ t^α)** (22) — ⚠ **인쇄된 'max' 는 그대로면 보정을 늘리기만 한다** (계수 ≥ 1).  본문 ("필요할 때 줄인다" · "γ < 0.5 면 침투") 과 맞으려면 **min** 이어야 한다 [우리 판독 — 구현 시 min].
- **성질**: 물체 하나의 양과 전역량만 필요 → 효율 유지 · 운동량 보존 성질 (15)(16) 유지.
- **왜 물질점 변형률은 괜찮나**: 큰 격자 변형률은 보간 함수값이 작은 노드에서 생기고, 같은 가중으로 물질점에 되돌리면 물질점 변형률 증분은 *훨씬* 작다 — 접촉이 격자 속도를 고칠 때만 문제.
- **기각한 대안**: 그 걸음의 시간 간격을 줄여 다시 시작 — *"it is the initial registration of the particle data on the grid which is ultimately responsible … traceable ultimately to the low order of the interpolation scheme"*; 바로잡으려면 **이전** 걸음 간격을 줄여야 하는데 격자 경계 근처 물질점을 찾는 탐색 없이는 모든 노드에서 동시에 보장할 수 없다.

### 5-6. 의사코드 — 한 시간 단계 (우리 전사 · 논문에 이 꼴로는 없음)

```
for α in bodies:                       # 물체별 P2G
    m^α_i, p^α_i  ← Σ_{p∈α} (m_p, m_p v_p) N_i(x_p)      (4)
    n^α_i ← normalize(∇ m^α)_i                          [세부 미기재]
    t_n^α_i ← n^α·σ^α·n^α (물질점 응력을 노드로 보간)      (9) [가중 미기재]
M_i = Σ_α m^α_i ;  v^cm_i = Σ_α p^α_i / M_i              (5)(6)
(내부력 · 외력으로 각 장을 전진)                           [순서 = 2000 판과 같다고 읽음]
for 노드 i, 물체 α (m^α_i > 0, 노드에 물체 ≥ 2):         (7)
    Δv = v^α − v^cm ;  Δv_n = Δv·n^α                      (11)(12)
    contact = (Δv_n > 0 and 응력 없음) or (t_n^α < 0)      (8)(9) [§5-3 우리 판독]
    if contact:
        t̂ = 접선 상대속도 방향 ; Δv_t = Δv·t̂               (13)
        μ' = min(μ, Δv_t/Δv_n)                            (10)
        dv = Δv_n (n^α + μ' t̂)
        ε̇_max = max_j( max(m^α/(M − m^α), 1) · |dv_j|/Δx_j )   (17)(20)
        s = min(γ/(ε̇_max Δt), 1)                          (22) ['min' = 우리 판독]
        v^α ← v^α − s · dv
    (else: 자유 분리)
G2P: 물질점은 자기 물체의 장에서 (FLIP 꼴 증분)
```

### 5-7. ★ 입자 처리

| 축 | 이 논문 |
|---|---|
| 물체 | 구 1 개 + 평판 (검증) · 원판 4–5 개 + 벽 (응용) — **알갱이 집합의 통계 없음** |
| 변형 | neo-Hookean (구) · 선형 hypoelastic (원판) — **소성 없음** (소성 계면의 분리 시점 문제는 서술로만) |
| 접촉 | 위 개정판 · μ 0.495 · 0.286 · 0.5 · ∞ · 벽 무마찰 (응력파) |
| 강체 | 없음 (평판도 변형체, 10 배 단단) |
| 무작위성 | 없음 (정렬 배치) |

---

## 6. 결과 — 절별

### 6-1. 구 경사면 (§3.1, Figure 2–6)

- **Figure 2**: 3D 문제 모식 + R/4 이산화 (구 · 평판 물질점 구름).
- **Figure 3 · 4 (R/4)**: 두 사례 모두 강체 해와 비슷하되 **변형 구가 더 천천히** 구르고 미끄러진다.  속도 곡선의 *"abrupt changes in velocity, most evident in the no slip case, are due to the application of the contact algorithm"*.
- **Figure 5 · 6 (해상도, no slip)**: R/2 는 *"too crude to resolve the geometry on a rectangular grid and the sphere fails to roll because of a flat spot"* (Figure 1 의 3D 판) — 초기 배치 둘레 진동만.  R/4 · R/8 은 *"quickly converges toward the rigid sphere case"* · *"although the material properties correspond to a very soft material, it is resolution of the geometry that is most important"*.
- **강체 해 = 속도 상한처럼 보임**: 변형 구는 위치 에너지가 변형 에너지로도 가기 때문.  단 구가 **약간 건너뛰고 (skips)** 공중에선 접촉 중보다 빨리 가속하므로 *"If the simulation was carried out long enough, the sphere would eventually travel more quickly in the numerical simulation, due to skipping"*.

### 6-2. Backspin (§3.2, Figure 7–8)

- 정지 상태에서 회전만 하는 구 (θ = 0) — 강체는 미끄러지며 가속하다 t = 2/7 s 에 접점 속도가 맞으면 일정 속도로 구른다 (식 25 · 26).
- 위치 · 속도 모두 해상도를 올리면 강체 해로 수렴 — *"indicating the importance of resolving the geometry accurately"*.
- 높은 각속도에서는 **변형이 더 큰 역할**: 무름 + 건너뜀 → 속도의 강한 진동.  *"Analogous to stick–slip like behavior, the sphere catches briefly causing acceleration … followed by free spinning"*; 앞쪽 접촉부가 압축됐다가 공중에서 풀리며 다음 접촉에서 앞으로 튀고 유효 backspin 이 생겨 다시 느려진다.

### 6-3. 광탄성 응력파 (§3.3, Figure 9–11) + ν 연구

- **동기**: 미끄럼 마찰은 알갱이 물질의 정의적 특성 → 2000 판들의 '거시' 정성 일치를 넘어 **특정 미세구조 하나를 실험과 직접 대조**.
- **Figure 9 (한 줄 4 원판, 오른쪽 충격)**: 단순 배치라 해상도는 주로 기하용 · 압축 하중과 대칭으로 접촉은 사실상 no slip.  무늬 · 원판과 접촉에서의 무늬 속도 변화를 정확히 재현, 단 **시뮬 무늬가 상대적으로 빠르다**.  실험 사진은 노출 시간 때문에 약간 흐리다 (시뮬은 순간).
- **Figure 10 (지그재그 5 원판, 중심선이 90° 지그재그, μ 0.5, 벽 무마찰)**: *"Because contacts can slide, load carrying paths first develop between disk contacts and a wall.  Only after sufficient normal traction builds up and the next disk contact sticks do fringes propagate into the next disk"* → 한 줄보다 **훨씬 느린** 전파 (실험 · 시뮬 모두).  실험 홈이 벽 접촉부 무늬를 가린다.
- **Figure 11 (같은 지그재그, 실험 = 접착 · 시뮬 = μ ∞, 벽 무마찰)**: *"When contacts support shear immediately, the primary load path across a disk first develops between disk contact points.  Load paths connecting disk contact points to the boundary develop later"* → 미끄럼 경우보다 **훨씬 빠른** 전파.
- **원인 분석**: 세부 차이 일부는 경계조건 (시뮬은 원판 · 벽이 처음부터 닿음, 실험은 작은 틈) — 가장 큰 계통 차 (프레임 시간) 는 **재료 응답 모형 오차** 탓일 가능성이 크다.  ν 연구 (한 줄 배치 · 종파속 고정): 무늬 속도는 ν 에 강하게, 무늬 모양은 약하게 의존 — ν 0.22 → 0.48 에서 2 배 넘게 느려짐 (광탄성은 전단응력 기울기를 보고 ν↑ 면 전단계수 · 전단파속↓).  ν > 0.22 (고분자에 정당한 수정) 면 계통 차가 줄 것.  Plexiglas 특성화는 후속 (Roessig 2001).
- **결론**: *"Fringe wave speeds are strongly dependent on contact conditions, specifically the amount of slippage."*

---

## 7. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/bardenhagen2001_mpm_improved_contact_granular_stress_waves/` · 300 dpi · 캡션 문자 제외 · 11 장 + 식 5 장.  [우리 …] 표지는 논문 밖 판단.

| 그림 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | 원판의 물질점 이산화 예 | 셀당 물질점 2 × 2, 지름 4 셀이라 표면이 계단.  이 해상도의 3D 판 (R/2) 에서 구가 '평평한 점' 으로 아예 구르지 못했다 (Fig 5).  우리 SE 1 µm 는 n_grid 384 · dx ≈ 0.141 µm 에서 ≈ 7 셀 — 이 그림보다 낫지만 논문이 구름을 확인한 8 셀 (R/4) 바로 아래 [우리 산술] → A′ 의 첫 해상도 조건 |
| 2 | `fig_2.png` | 경사면 문제 모식 + R/4 셀 MPM 이산화 | 구 · 평판 **둘 다 변형체** (셀당 물질점 8) — 물체 2 개 = 속도장 2 개의 가장 작은 3D 다물체 문제라 A′ 를 Taichi 에 넣으면 그대로 재현할 회귀 시험 (해석해 식 23 · 24) [우리 추론].  단일 속도장 (지금 MPM) 은 구–평판 접촉 노드에서 속도를 하나로 만들어 미끄럼을 막고 분리 판정이 없다 |
| 3 | `fig_3.png` | 구 중심 x 위치, 미끄럼 · 구름 두 경우 + 강체 해석해 | 변형 구 (R/4) 는 두 경우 모두 강체보다 느리다 (t = 2 s: ≈ 13 vs 14.5 m · ≈ 7.5 vs 10.1 m, 판독).  체제 문턱 tanθ ≷ 3.5μ 를 사이에 둔 두 사례라 '마찰계수가 체제를 가른다' 를 시험하는 형식 [문턱 = 우리 산술] — 우리 MPM 에는 μ 가 없어 이 구분 자체가 없다 |
| 4 | `fig_4.png` | 구 중심 x 속도, 미끄럼 · 구름 두 경우 + 강체 해석해 | 구름 경우 속도에 계단 · 정체 구간 (t ≈ 0.4–0.7, 1.55–1.75 s, 판독) = 접촉 알고리즘이 걸릴 때의 갑작스런 속도 변화 (논문).  수천 접촉이 켜지고 꺼지는 압밀에서는 이 충격 잡음이 판 반력 (wallP) 판독에 섞일 수 있어, A′ 에서 판 반력을 읽을 땐 시간 평균 창과 재하율 대조가 필요 [우리 추론] |
| 5 | `fig_5.png` | no slip 구 중심 위치, 해상도 R/8 · R/4 · R/2 + 강체 | ★ R/2 (지름 4 셀) 는 '평평한 점' 때문에 **아예 구르지 않는다** (x = 0) — 해상도 부족이 정성 실패로 나타남.  R/4 ≈ 7.4 · R/8 ≈ 9.7 → 강체 10.1 m (t = 2 s, 판독).  SE 1 µm 를 8 셀 이상으로 풀려면 dx ≤ 0.125 µm [우리 산술] |
| 6 | `fig_6.png` | no slip 구 중심 속도, 해상도별 + 강체 | R/2 는 0 둘레 진동 (±0.1 m/s 급) 만, R/4 는 건너뜀으로 멈칫 (≈ 1.5–1.7 s), R/8 ≈ 강체 (판독).  접촉이 잠깐 떨어졌다 붙는 skip 은 해상도가 낮을수록 크다 — 압밀 중 SE 가 판 · AM 에 닿았다 떨어지는 과정도 같은 잡음을 낼 수 있다 [우리 추론] |
| 7 | `fig_7.png` | backspin 5 rad/s 구 중심 위치, dx 0.250 (R/4) · 0.125 (R/8) + 강체 | 미끄럼 → 구름 전환 (t = 2/7 s) 시점까지 맞추는지 보는 시험 — dx 0.125 가 강체 해에 붙고 0.250 은 뒤처짐 (t = 3 s ≈ 3.95 · 3.5 vs 4.08 m, 판독).  A′ 마찰 구현의 두 번째 회귀 표적 [우리 추론]; 우리 MPM 엔 이 전환이 없다 |
| 8 | `fig_8.png` | backspin 구 중심 속도, 같은 해상도 + 강체 | 강체 해는 10/7 ≈ 1.43 m/s 로 일정, 변형 구는 그 둘레로 크게 진동 (무름 + 건너뜀, stick–slip 비슷 — 논문).  우리 SE 는 전단만 연화 (μ 0.51 GPa · ν 0.49 → K 25.5 GPa) 라 CFL 시간 간격은 SE 종파 탄성률 M = λ + 2µ ≈ 26.2 GPa 로 정해진다 (`scripts/mpm3d_compaction.py` 1912–1929 행) — 실물 쌍 (DFT B₀ 26.23 · μ 8.11 GPa) 으로 올려도 M ≈ 37 이라 시간 간격은 ≈ 1.2 배만 준다.  대신 전단 강성이 ≈ 16 배라 접촉의 붙음/미끄럼 · 건너뜀 양상이 달라질 수 있다 → A′ 회귀 시험은 두 물성으로 [우리 산술 · 추론] |
| 9 | `fig_9.png` | 한 줄 4 원판 응력파, 실험 (위) ↔ 시뮬 (아래), 프레임 2.6/6.6/9.2 ↔ 2.2/5.5/7.7 | 압축 · 대칭이라 접촉이 사실상 no slip — **단일 속도장도 같은 답을 낼 조건** (대조군).  지름당 80 셀 · 셀당 물질점 1.  무늬 재현은 정확, 시간은 시뮬 ≈ 0.84 × 실험 [우리 산술] — 원인은 Plexiglas 물성 (ν) 불확실 (논문) |
| 10 | `fig_10.png` | 지그재그 5 원판, μ 0.5, 프레임 5.3/10.5/15.8 ↔ 3.0/6.0/9.0 | ★ 미끄러질 수 있으면 하중 경로가 먼저 '원판 접촉 ↔ 벽' 으로 생기고 다음 접촉이 붙은 뒤에야 다음 원판으로 간다 (전달이 늦음).  **단일 속도장 MPM 이 원리상 못 내는 응답** — 우리 MPM 은 모든 접촉이 붙어 Fig 11 처럼만 행동.  시간비 ≈ 0.57 로 붙은 두 배치 (≈ 0.84–0.86) 보다 크게 벗어남 [우리 산술] — 미끄럼 접촉이 들어간 경우 오차가 가장 크다 (마찰 모형 또는 벽 조건 몫 후보 · 우리 추론) |
| 11 | `fig_11.png` | 지그재그 5 원판, 접착 (붙음), 프레임 1.6/4.2/6.8 ↔ 1.4/3.6/5.8 | 미끄럼이 없으면 하중 경로가 즉시 원판 접촉점 사이로 생겨 전파가 훨씬 빠르다 (논문).  **우리 SE–SE · SE–AM 접촉이 바로 이 '붙음' 체제** (게다가 분리 판정도 없음 — 시뮬의 μ = ∞ 는 분리는 허용) → 지금 MPM 의 하중 경로 · 응력장은 붙음 쪽으로 치우쳐 있을 수 있다 [우리 추론].  Fig 10 ↔ 11 대비 = A′ 의 정성 검증 형식 |

**식 그림**: `eq_04_08_com_velocity_contact_nodes.png` (물체별 속도 · 질량중심 · 접촉 노드 · 법선 · 접근 판정) · `eq_09_traction_release_criterion.png` (견인력 t_n 과 핵심 개정 문장) · `eq_10_11_contact_velocity_update.png` (갱신식 10 · Δv 11 · t = ω × n 괄호) · `eq_12_16_stick_slip_momentum.png` (N = 2 가정 · 붙음/미끄럼 · 운동량) · `eq_17_22_cell_collapse_scaling.png` (격자 붕괴 조건 · 스케일 — 식 22 의 'max' 인쇄 그대로).

---

## 8. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 해석해 대조 | 구 중심 위치 · 속도 vs 강체 해 (해상도별) | A′ 3D 회귀 시험 형식 |
| 광탄성 모사 | 응력 텐서 대각화 → 면내 주응력차 → cos(차/계수) 무늬 · 계수는 한 줄 배치로 맞춘 뒤 고정 | 우리 MPM 응력장으로 같은 지도 가능 (단 3D → 단면 선택 필요) [우리 추론] |
| 프레임 짝짓기 | 무늬가 맞는 프레임을 **눈으로** 고르되 실험과 같은 프레임 간격 제약 · 무차원 시간 = 시간/통과 시간 | 정량 판정 아님 — 우리 쪽 대조엔 결과 전 등록한 지표가 필요 |
| 민감도 | ν 를 바꾸되 종파속 고정 | 무른 SE (ν 0.49) 는 전단파가 느리다는 경고 (§10) |

---

## 9. 우리 DEM + MPM 대비

| 축 | 2001 판 | 우리 DEM | 우리 MPM |
|---|---|---|---|
| 분리 판정 | **수직 견인력** (압축이면 접촉 유지) | 겹침 기반 힘 법칙의 힘이 0 이 되면 접촉 끝 (탄성 + 이력) | 없음 (붙음) — 바닥 · 옆벽은 한쪽 법선 구속 (속도 판정), 판은 양방향 고정, AM 은 붙음 [우리 코드 판독] |
| 이종 계면 | 견인력 평형 **안 맞음** (균일 늘림 가정) — 소성이면 분리 시점이 어긋날 수 있다고 명시 | 접촉 법칙에 E* 로 들어감 | AM 은 얼린 장애물 (응력 없음) |
| 에너지 | 완전 비탄성 · 약간 소산 | COR (감쇠) 로 지정 | 운동량 싱크 (AM) |
| 해상도 | 지름당 ≥ 8 셀 | 해당 없음 | SE ≈ 7 셀 @ 384 |
| 차원 · 규모 | 3D 구 1 개 · 원판 ≤ 5 | 3D 수만 | 3D SE 씨앗 3.3 만 |
| 실험 대조 | 광탄성 (정성) | 압밀 기공률 · EIS (따로) | 기공률 · SEM 모양 (따로) |

- **전이**: 개정된 알고리즘 · 분리 판정 논리 · γ 안정화 · 3D 시험 문제 · 해상도 규칙 · "접촉 조건이 하중 경로를 바꾼다" 는 정성 결론.
- **전이 안 됨**: 고무 구 · 가상 Plexiglas 수치 · 프레임 시간 · 동적 응력파 영역 (우리 압밀은 준정적).
- **frame [5]**: 분리 판정이 견인력으로 바뀌면 MPM 이 **제하** 를 가질 수 있게 된다 — 지금 우리 정의 문서가 "탈압 = 없음 (부분만)" 으로 둔 칸.  수송 분업 (DEM 접촉망 · STEP3) 은 그대로.
- **frame [4]**: 접촉 MPM 의 기공률은 실험에 따로 보정, DEM 과 맞추지 않는다.

---

## 10. 깊은 통찰

① **제하 (unloading) 의 물리는 분리 판정에 들어 있다.**  운동학 판정이면 되튈 때 계면이 즉시 사라져 에너지 회수가 어긋난다; 견인력 판정이면 계면이 응력 0 까지 풀린 뒤 떨어진다.  [DEM 우선 (수영)] 의 "가압 → 제하" 에서 스프링백 · 접촉 열림을 MPM 이 내려면 **이 개정판이 최소 조건**이다.

② **그런데 우리 계는 논문이 경고한 바로 그 경우다.**  AM (E ≈ 140 GPa · 탄성) 과 SE (연화 · J2 소성) — *"different materials … free separation at different times … particularly when material response allows for permanent set (e.g. plasticity)"*, 그리고 *"traction equilibrium is not maintained at contact nodes"* (균일 늘림 가정).  ⇒ A′ 의 제하 · 스프링백 값을 쓰기 전에 **이종 · 소성 계면 하나** (강체 구 + 소성 블록의 가압-제하) 를 FE 나 해석해와 대조하는 단위 시험이 먼저다.  저자는 *"implicit formulation"* 이면 이 오차를 없앨 수 있다고 적는다.

③ **식 (22) 'max' 는 구현 함정.**  인쇄대로면 보정이 커지기만 하고, 본문 (필요할 때 줄인다 · γ < 0.5 면 침투) 과 모순된다 → 'min' 으로 구현 [우리 판독].  같은 부류: (19) 의 부호 누락 · t = ω × n 의 곱 순서 (2000 판 n × ω̂ 와 반대).  **글로 쓴 정의를 기준으로 구현**해야 한다.

④ **"노드당 물체 ≤ 2" 는 조밀 3D 압밀의 실제 위험.**  SE ≈ 7 셀 지름 · 2차 B-spline 지지 3 셀이면 삼중점 (한 노드에 SE 셋 · 또는 SE 둘 + AM) 이 흔할 것이고 그 노드에서 붙음/미끄럼 동시성 · 운동량 보존이 깨진다 [우리 추론].  이 비율은 계산 없이 씨앗만으로 미리 잴 수 있다 (§11 행동 2).

⑤ **이른 접촉 (셀 크기 틈).**  접촉 노드 = 두 물체가 질량을 가진 노드 → 표면이 실제로 닿기 전 (지지 폭 안에 들어오면) 접촉이 걸린다 · 논문 스스로 *"Resolution of the interface is commensurate with the computational grid cell size"*.  10–13 % 기공을 표적으로 하는 압밀에서 기공률을 올리는 계통 오차가 될 수 있고, 2차 B-spline 은 1차보다 그 거리가 길다 [두 논문 밖 · 우리 추론 — dx 사다리로 확인].

⑥ **해상도가 마찰보다 먼저다.**  *"it is resolution of the geometry that is most important"* — 무른 재료여도 4 셀 지름이면 아예 구르지 못한다.  재설계에서 SE 크기 · 영역 크기 · dx 를 정하는 첫 제약.

⑦ **미끄럼이 있는 배치에서 오차가 가장 컸다** (시간비 0.57 vs 붙은 배치 0.84–0.86 — 우리 산술).  저자는 재료 (ν) 로 설명하지만, 세 배치에 같은 재료를 썼으므로 미끄럼 배치에만 추가로 벌어진 차이는 **마찰 · 접촉 모형 쪽 몫** — 또는 미끄럼 배치에서 하중이 먼저 벽으로 가므로 **벽 조건 (시뮬 무마찰 ↔ 실험 홈)** 의 몫 — 일 수 있다 [우리 추론 — 논문 주장 아님].  ⇒ A′ 의 마찰 계수 · 접촉 판정 · 벽 조건은 **미끄럼이 지배하는 시험**으로 따로 검증해야 한다.

⑧ **ν 0.49 는 전단 동역학을 느리게 만든다.**  논문: ν 0.22 → 0.48 에서 무늬 속도 2 배 넘게 감소 (종파속 고정).  우리 SE (ν 0.49) 는 c_L/c_S = √(2(1−ν)/(1−2ν)) ≈ 7.1 [우리 산술] — 판 속도를 c_L 기준 Mach 0.03 으로 맞춰도 c_S 기준으로는 ≈ 0.21 이다.  미끄럼 · 전단이 지배하는 A′ 에서는 준정적 판정을 **c_S 기준**으로 등록해야 한다 [우리 추론].

⑨ **"완전 비탄성 충돌" = 반발 계수 없음.**  접촉 에너지 손실이 알고리즘에서 나와 DEM COR 을 옮길 자리가 없다 → 성긴 초기 패킹은 DEM (P ≈ 0, 정착) 이 만들고 압축 · 제하만 A′ 가 하는 인계가 자연스럽다 [우리 추론].

---

## 11. [DEM 우선 (수영)] — 후보별 함의 + 구체 행동

| 후보 | 이 논문의 함의 | 판정 |
|---|---|---|
| **A′** | **구현 기준판** — 견인력 분리 판정 (제하) · γ 안정화 · 3D 회귀 시험 · 실험 정성 대조.  그러나 압밀 · 다알갱이 3D 성능 근거 0, N ≤ 2 가정, 이종 · 소성 계면 견인력 불평형 (명시) | ✅ 기전 · 구현 지지 · ⚠ 제하 정확도 · 삼중점 · 이른 접촉 위험 |
| **A** (움직이는 강체 AM) | 변형체 ↔ 강체 벽 접촉 · 되튐 논의가 이 논문의 분리 판정 동기 그 자체 → 강체 AM 과 SE 의 마찰 · 분리 · 제하를 같은 틀로 | ✅ 부분 지지 |
| **B** (입자 분해 FE / NSCD+FE) | 저자가 *"implicit formulation"* 에서 계면 견인력 평형 오차가 사라진다고 적음 — 암시적 · 접촉 해결형 (NSCD 등) 의 장점 쪽 근거 | ↗ 간접 지지 (제하 정확도 축) |
| **C / C′** (MDR · 두 재료 캡 DEM) | 관련 서술 없음 | 중립 |
| **D0** | 관련 없음 | — |

**구체 행동 (전부 [우리 추론] · 결과 전 등록 대상)**
1. **A′-0 확장** — 짝 카드 행동 1 (AM 노드 · 벽에 식 23 적용) 에 **식 (9) 견인력 분리 판정 + 식 (22, min) 스케일**을 함께 넣는다.  특히 판: 지금은 판 위 노드를 판 속도에 양방향 고정 (분리 판정 없음) → 제하 때 판에서 떨어지지 못한다 [우리 코드 판독, `scripts/mpm3d_compaction.py` 2996–2998 행] — 견인력 판정으로 바꾸면 판 분리가 생긴다.
2. **위상 사전 점검 (GPU 불요)** — real_14 씨앗 알갱이별 P2G 로 노드당 물체 수 (≥ 3 비율) · 색 수 K 측정 (짝 카드 행동 2 와 같은 일).
3. **이종 · 소성 계면 단위 시험** — 강체 구 (AM 대리) 를 J2 블록 (SE 대리) 에 눌렀다 떼기: 분리 시점 · 잔류 압흔 · 스프링백을 FE (또는 해석해) 와 대조.  통과 전에는 A′ 제하 값을 보고하지 않는다.
4. **회귀 시험 묶음** — 3D 구 경사면 (식 23 · 24, R/2 음성 대조 포함) · backspin (식 25 · 26) · 2D 지그재그 원판 μ 0.5 ↔ μ ∞ (하중 경로가 갈리는가).  Taichi 구현의 CI 시험으로.
5. **이른 접촉 dx 사다리** — 순수 SE 가압을 dx 3 단으로: 300 MPa 기공률이 dx 에 따라 움직이면 거리 기반 판정 보강.
6. **준정적 판정을 c_S 기준으로** 등록 (ν 0.49 · c_L/c_S ≈ 7.1).

---

## 12. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 계면 해상도 = 셀 크기 | §2.1 |
| 2 | 접촉 노드당 물체 ≤ 2 로 분석 · **N > 2 에선 일부 성질 불성립** | §2.1 |
| 3 | 미끄럼은 법선이 공선이 아니면 **운동량 비보존** (계면 곡률 해상 부족) | §2.1 식 (16) 아래 |
| 4 | 접촉 노드에서 **견인력 평형 불성립** · 이종 · 소성 물체는 분리 시점이 어긋날 수 있음 · 암시적 MPM 이면 제거 가능 | §2.1 |
| 5 | 작은 격자 질량 (등록) → 접촉 보정 폭주 · 저차 보간의 산물 · 시간 간격 의존 | §2.2 |
| 6 | γ < 0.5 면 침투 | §3 |
| 7 | R/2 (지름 4 셀) 는 구르지 못함 | §3.1 |
| 8 | 무름 + 건너뜀 → 속도 진동 · 오래 돌리면 수치 구가 더 빨라질 것 | §3.1–3.2 |
| 9 | 실험 대조는 정성 · 프레임 시간 계통 차 · 재료 (Plexiglas) 미확정 · 경계 틈 | §3.3 |
| 10 | 접촉 = 완전 비탄성 충돌 | §4 |
| 11 | 시험 재료는 큰 시간 간격을 위해 일부러 무르게 (*"rather soft"*) | §3.1 |

## 13. 불확실 · PDF 에 없는 것

- DOI · 저널 전체 이름 · 접수/게재일 · 교신저자: 미인쇄 → [미확인].  PDF 메타데이터는 다른 문서의 것 (무시).
- 광탄성 시뮬의 차원 · 시간 간격 · 단계 수: 미기재.
- 견인력 · 법선의 격자 보간 세부, 접근 + 견인력의 결합 규칙 (특히 '접근 · 인장'): 산문뿐.
- 인쇄 오류 후보 (전부 [우리 판독]): 식 (22) max → min · 식 (19) 부호 · t = ω × n 곱 순서.
- 에너지 증가 · 소산의 크기: 수치 없음.
- **압밀 · 다알갱이 3D 에서의 거동**: 이 논문으로 알 수 없다.

## 14. 인용 가능 문장 (덱 · 원고용)

- "MPM 다물체 접촉에서 분리를 운동학으로만 판정하면 되튐 때 경계가 즉시 사라지는 꼴이 되므로, 접촉 노드의 수직 견인력이 압축인 동안은 접촉을 유지해야 한다 (Bardenhagen et al., CMES 2(4), 2001, §2.1)."
- "이 접촉 판정은 서로 다른 재료의 계면에서 견인력 평형을 지키지 않으며, 소성처럼 영구 변형이 있으면 분리 시점이 어긋날 수 있다 (같은 문헌 §2.1)." — 우리 AM–SE 제하에 대한 한정어로.
- "광탄성 원판 실험에서 접촉의 미끄럼 정도가 하중 경로와 응력파 전달 속도를 크게 바꿨다 (같은 문헌 §3.3, Fig 10–11)."

## 15. 기법 미니 용어집

- **수직 견인력 t_n** — n·σ·n.  이 논문의 부호 규약에서 압축이 음수.
- **해제 (release) 논리** — 접촉을 언제 끊을지 정하는 규칙.  2001 판 = 견인력 기반.
- **등록 (registration)** — 물질점 정보가 격자 노드에 실리는 것.  "불운한 등록" = 물질점이 막 들어와 노드 질량이 아주 작은 상태.
- **격자 붕괴 조건** — 접촉이 부과한 속도 변화가 한 걸음에 셀을 무너뜨리지 않게 하는 Courant 비슷한 조건 (ε̇_max Δt < γ).
- **완전 비탄성 충돌** — 법선 상대속도를 0 으로 만드는 접촉 (반발 없음) — 운동 · 변형 에너지 교환이 최대.
- **광탄성** — 응력 받은 투명 고분자가 최대 전단응력 등고선에 어두운 무늬를 내는 현상.
- **split Hopkinson bar** — 막대 속 응력파로 시편에 계단형 속도를 주는 동적 하중 장치.
- **무차원 프레임 시간** — 충격 뒤 시간 / 원판 하나의 종파 통과 시간.

## 16. 관련 카드

- **짝 (원판 알고리즘)**: `bardenhagen2000_mpm_granular_multibody_frictional_contact` — 식 (12)–(24), 2D 전단 · no slip ↔ 마찰 대비.
- `devaucorbeil2020_mpm_after_25_years_review` — 이 다물체 알고리즘을 MPM 접촉의 표준으로 소개.
- `stomakhin2013_mpm_snow_elastoplastic` — 우리 MLS/탄소성 MPM 계보 (단일 속도장).
- `pycompact2025_dem_mpfem_workflow` · `demirtas2021_mpfem_hollow_sphere_die_compaction` — 입자 분해 FE 쪽 (후보 B) · 제하 · 스프링백을 다룬 연속체 선례.
- `zunker2024_mdr_contact_model_partI` · `zunker2025_dem_large_deformation_compaction` — 후보 C.
- (같은 날 stage B 반입 예정) `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` — 입자별 격자 + contact dynamics (암시적) 로 압밀까지 간 2D 후속.
- (같은 날 stage A 반입 예정) `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic` — 무른 + 단단한 2D 입자 압밀 실험 (A′ 의 준정적 정성 검증 후보).
- `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` — 같은 제1 저자의 GIMP 원전 (보간 일반화 · 셀 넘김 잡음 · 1D 초탄성 · 접촉 없음 · 이 논문을 참고문헌에 듦 · 2026-11-12 반입).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
