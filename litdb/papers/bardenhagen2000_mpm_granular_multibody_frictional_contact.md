# MPM 다물체 마찰 접촉의 원전 — 알갱이별 격자 속도장 ↔ 질량중심 속도장 비교로 침투 금지 · 자유 분리 · Coulomb 미끄럼 (알갱이 수에 선형) · no slip (= 우리 단일 속도장) ↔ 마찰 전단 대비 ★★ 후보 A′ 기반 — Bardenhagen, Brackbill & Sulsky (CMAME 2000)

> slug `bardenhagen2000_mpm_granular_multibody_frictional_contact` · DOI `[미확인]` (PDF 에 DOI 미인쇄 — 인쇄된 식별자는 PII `S0045-7825(99)00338-2`) · type `MPM (2D 명시적 FLIP-MPM · 다물체 마찰 접촉 — 알갱이별 격자 속도장 ↔ 질량중심 속도장 · 원판 경사면 검증 + 원판 369 개 전단)` · PDF `666fc549-6._The_material-point_method_for_granular_materials.pdf` · digested `2026-11-09` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 계산은 **전부 2D** 다 (원판 = 원기둥).  ② **압밀 (치밀화) 계산이 없다** — 검증은 경사면 원판 1 개, 시연은 **전단** (부피 일정 · 주기 경계) 뿐이다.
> ③ 재료는 고무 같은 탄성 원판 (G 2.5 MPa) 과 HMX 근사 von Mises 원판 — **LPSCl · NCM 이 아니다.  절대값 전이 0 건**, 가져오는 것은 알고리즘 · 해상도 규칙 · 정성 결론뿐.
> ④ PDF 는 스캔본 (Acrobat 3.0 Capture · PDF 생성 2001-07) 이라 텍스트 층의 식이 깨져 있다 — 이 카드의 식은 **렌더 이미지를 보고 옮겼다** (식 그림 `eq_*.png` 동봉).
> ⑤ 그림에서 읽은 값 (`figure-read ≈`) 은 추세 전용 — 정밀값으로 쓰지 않는다.
>
> 짝 카드: `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 같은 저자의 **개정판** (분리 판정에 수직 견인력 · 격자 붕괴 안정화 · 3D 검증).  이 카드의 알고리즘을 "2000a" 로 인용한다.

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

우리 MPM (Taichi MLS-MPM, `scripts/mpm3d_compaction.py`) 은 격자 속도장이 **하나** (`grid_v` · `grid_m`) 다.  이 논문 §2 가 그 결과를 한 문장으로 적는다:

> *"Because the velocity field is single-valued, interpenetration of material is precluded, and also **no-slip contact between impinging bodies is automatic**."* (p.531)

즉 **우리 MPM 은 이 논문의 '접촉 알고리즘을 넣기 전' 기준선** 이다 — SE 알갱이끼리 닿으면 붙고 (미끄럼 없음), 떨어지려면 연속체처럼 끊어져야 한다 (분리 판정이 없다).  이 논문은 바로 그 단일 속도장을 **알갱이마다 하나씩의 격자 속도장 + 그것들의 질량 가중 평균 (질량중심 속도장)** 으로 바꿔, 둘을 비교하는 것만으로

- 침투 금지 (법선 성분을 질량중심 값으로),
- **자유 분리** (멀어질 때는 아무 구속도 안 검),
- **Coulomb 마찰 미끄럼** (붙임에 필요한 접선력을 μ·법선력으로 자름),
- 구름 (rolling)

을 **짝 (pairwise) 탐색 없이, 반복 없이, 알갱이 수에 선형인 비용**으로 얻는다.  그리고 같은 초기 배치에서 **no slip (= 단일 속도장)** 과 **마찰 미끄럼 (μ 0.3)** 을 나란히 돌려 (Fig 6), no slip 이면 *"extensive plastic deformation of the grains and large voids are created"*, 마찰 미끄럼이면 *"accommodated by grain rolling and sliding with fairly little plastic deformation"* 임을 보인다.

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| [DEM 우선 (수영)] 후보 **A′** (다물체 · 다중 속도장 접촉 MPM) 의 **원전 알고리즘** | §3 식 (12)–(24) 전부 — 이 카드 §4-2 에 단계별로 옮김 |
| "단일 속도장 = 붙음" 이라는 우리 진단의 **제3자 진술** | §2 원문 (위 인용) + §1 의 Benson 혼합이론 비판 *"inability to model sliding in a single-valued velocity field"* |
| 미끄럼이 **변형 양상을 바꾼다** 는 그림 증거 | Fig 6 (a) no slip ↔ (b) 마찰 미끄럼 |
| A′ 구현의 **회귀 시험 표적** | 경사면 원판 해석해 식 (25) · Fig 2–4 (μ 와 θ 로 미끄럼/구름 체제가 갈림) |
| 해상도 규칙 | "지름당 ≈ 8 요소면 접촉력 해상 · 4 요소는 내부 응력에 부족" + Fig 4 격자 수렴 |
| 우리 3D 규모에서의 **비용 · 메모리** 판단 근거 | 비용 = 알갱이 수에 선형 (계산) — 단, 알갱이별 격자장의 **저장** 문제는 논문이 다루지 않는다 (§4-4 에 우리 산술) |

---

## 1. 한 줄 요약

**KR:** FLIP 계열 MPM 에서 각 알갱이를 물질점 묶음 (연속체 구성식) 으로 두고, 알갱이마다 격자 속도장 v_i^g 를 따로 풀어 모든 알갱이의 질량 가중 평균인 질량중심 속도장 v_i 와 노드마다 비교한다 — 둘이 다르면 접촉, 다가오면 [(v_i^g − v_i)·n_i^g > 0] 법선 성분을 v_i 의 것으로 바꾸고 접선 성분은 Coulomb 법칙으로 자른다 (식 23).  알갱이를 짝지어 비교하지 않으므로 한 번 훑기 · 반복 없음 · 알갱이 수에 선형.  2D 경사면 원판의 강체 해석해를 거친 격자 (지름 4 요소) 에서도 체제까지 재현하고 지름 16 요소면 거의 일치하며, HMX 근사 원판 369 개 전단 (> 80 %) 에서 no slip 과 마찰 미끄럼이 **전혀 다른 변형** 을 내고, 마찰 쪽이 실험에서 보던 일시적 힘 사슬 · 평균 지름 7 개 폭의 전단 띠를 보인다.

**EN:** A multi-body contact algorithm for the material point method: each grain is integrated on its own background-grid velocity field v_i^g and compared node-by-node to the mass-weighted centre-of-mass field v_i; nodes where the two differ are contact nodes, and when a grain approaches [(v_i^g − v_i)·n_i^g > 0] its normal velocity is set to that of the centre-of-mass field while the tangential correction is capped by Coulomb friction (Eq. 23); separation is free.  Comparing each grain to one common field — never pairwise — gives one sweep, no iteration and cost linear in the number of grains.  Validated on a 2D deformable disk rolling/sliding on an incline (rigid-disk analytic solutions; 16 elements per diameter ≈ exact) and demonstrated on large shear of 369 HMX-like von Mises disks, where no-slip and frictional contact produce dramatically different deformation and frictional contact shows transient force chains and a ~7-diameter shear band.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **The material-point method for granular materials** |
| 저자 | **S.G. Bardenhagen** (a) · **J.U. Brackbill** (b, 교신 \*) · **D. Sulsky** (c) |
| 소속 | (a) ESA-EA, MS P946, Los Alamos National Laboratory, Los Alamos, NM 87545, USA · (b) T-3, MS B216, Los Alamos National Laboratory, Los Alamos, NM 87545, USA · (c) Department of Mathematics and Statistics, University of New Mexico, Albuquerque (인쇄 철자 *Albuguerqe*), NM 87131, USA |
| 저널 | **Comput. Methods Appl. Mech. Engrg. 187 (2000) 529–541** (Elsevier Science S.A., © 2000) |
| DOI | **[미확인]** — PDF 에 DOI 가 인쇄돼 있지 않다.  인쇄된 것은 `0045-7825/00/$ - see front matter` · **PII: S0045-7825(99)00338-2** (Elsevier 의 PII→DOI 관례로는 `10.1016/S0045-7825(99)00338-2` 이겠으나 **PDF 로 확인 안 됨**) |
| 접수 · 게재일 | **[미확인]** (PDF 에 인쇄 없음) |
| 키워드 | **[미확인]** (인쇄 없음) |
| 분량 | 13 쪽 (pp. 529–541) · Fig 1–8 · 표 없음 · refs 24 |
| 연구 유형 | 수치 방법 (MPM 접촉 알고리즘) + 2D 검증 (해석해) + 2D 시연 (전단) · **실험 없음** |
| 자금 | Los Alamos National Laboratory, US DOE contract **W-7405-ENG-36**; D. Sulsky 는 LANL **BOA 040950004-3P** 일부 지원 |
| PDF 상태 | 스캔본 (Creator *Acrobat 3.0 Capture Plug-in*, 1-bit 300 dpi 띠 이미지 27 장/쪽 + OCR 텍스트 층) — 식은 텍스트 층이 깨져 렌더 이미지로 판독 |

**자기 위치 (저자 원문, §1)**
> *"Our goal is not only to allow each grain to deform according to continuum constitutive models, but also to describe the interactions between grains, including separation, sliding, and rolling.  Our approach combines features of the micromechanical modeling approach, as described by Williamson [24], and the distinct element method [6]."*

> *"The ultimate goals of simulations on this scale are to understand under what circumstances homogenized constitutive theories of granular materials are valid, and to suggest new theories based on observed behavior."*

---

## 3. 핵심 수치

> **라벨 규약** · `stated` = 본문 · 캡션에 적힌 값 · `derived(ours)` = stated 값에서 산술로만 유도 (논문에 없는 수) · `figure-read ≈` = 그림 픽셀에서 눈으로 읽은 값 (추세 전용, ±5–10 %)

### 3-1. 검증 — 경사면 위 원판 (§4.1, Fig 1–4)

| 항목 | 값 | 라벨 |
|---|---|---|
| 차원 | **2D** (원판 = 원기둥) | stated |
| 원판 반지름 R | **50 cm** | stated |
| 중력 | **9.8 m/s²** — 계산에서는 면을 격자 경계에 맞추고 중력을 θ 만큼 기울임 (Fig 1b) | stated |
| 상대 | **계산 영역 경계 (강체 벽)** — "a grain interacts with the boundary of the computational domain, where friction is applied" | stated |
| 격자 (기본) | 정사각 요소 **25 cm = 0.5R** → 지름당 **4 요소** · 요소당 물질점 **9 개** | stated |
| 원판 재료 | **선형 탄성 · 압축성**: 전단계수 **2.5 MPa** · 체적계수 **10 MPa** · 밀도 **3000 kg/m³** | stated |
| ⇒ E · ν · c_L | **6.92 MPa · 0.385 · 66.7 m/s** | derived(ours) |
| 초기 응력 | 물질점 압력을 정적 해 ∇p = ρg 로 초기화 | stated |
| 사례 | (μ, θ) = **(0.3, π/3) · (0.9, π/3)** [Fig 2]; **(0.5, π/3) · (0.5, π/6)** [Fig 3] | stated |
| 강체 해석해 | 식 (25): 미끄럼 if tanθ > 3μ, 아니면 미끄럼 없는 구름 | stated |
| 체제 판정 | (0.3, π/3): tan 1.732 > 0.9 → 미끄럼 · (0.9, π/3): 1.732 < 2.7 → 구름 · (0.5, π/3): 1.732 > 1.5 → 미끄럼 · (0.5, π/6): 0.577 < 1.5 → 구름 | derived(ours) |
| 결과 (정성) | 모든 사례에서 **변형 원판이 강체보다 느리다**; 거친 격자의 최대 오차 = (0.5, π/6) | stated |
| 격자 수렴 | 요소 0.5R · 0.25R · 0.125R (지름당 4 · 8 · 16) — **16: "excellent"**, **8: "discrepancy is small"** | stated |
| t = 0.3 에서 변위 (x − 0.15) 의 계산/해석 비 | (0.3, π/3) ≈ 0.76 · (0.9, π/3) ≈ 0.87 · (0.5, π/3) ≈ 0.86 · (0.5, π/6) ≈ **0.17** | figure-read ≈ (해석해는 식 25 로 산출) |
| t = 0.4, (0.5, π/6) 격자별 변위비 | 0.125R ≈ 1.0 · 0.25R ≈ 0.77 · 0.5R ≈ 0.23 | figure-read ≈ |
| ⚠ 그림 세로축 단위 | Fig 2–4 의 세로축 라벨은 'cm' 인데, 해석해 (g 9.8 m/s², 시간 s) 로 곡선 끝값이 재현되려면 **m** 이어야 한다 (예: (0.3, π/3) 해석해 0.15 + 3.509·0.3² = 0.466 = 그림 끝값) | derived(ours) |

### 3-2. 시연 — 원판 369 개 전단 (§4.2, Fig 5–8)

| 항목 | 값 | 라벨 |
|---|---|---|
| 알갱이 | **원기둥 (2D 원판) 369 개**, 지름 **31–250 µm**, 평균 **57 µm** ("representative of a granular explosive") | stated |
| 재료 (HMX 근사) | **von Mises + 선형 경화**: 전단계수 **7.5 GPa** · 체적계수 **11.4 GPa** · 항복강도 **0.3 GPa** · 경화계수 **0.01 GPa** · 밀도 **1900 kg/m³** | stated |
| ⇒ E · ν · E/σ_y | **18.5 GPa · 0.230 · 61.5** | derived(ours · 3D 등방 관계식 가정 — 2D 계산의 평면 가정은 미기재) |
| ⇒ c_L · c_S | **3,356 m/s · 1,987 m/s** | derived(ours) |
| 경계 | 좌우 경계에 겹친 알갱이를 경계에 고정; **왼쪽 고정 (tied), 오른쪽 위로 0.1 mm/µs (= 100 m/s)**; 세로 방향 **주기** (위로 나간 물질이 아래로 들어옴 = 무한 주기 판) | stated |
| 평균 전단 변형률 속도 | **8 × 10⁴ /s** | stated (산술 100 m/s ÷ 1.2 mm = 8.3 × 10⁴ /s) |
| ⇒ 경계 속도 / 파속 | **V/c_L ≈ 0.030 · V/c_S ≈ 0.050** | derived(ours) |
| 계산 영역 · 격자 | **1.2 mm 정사각 · 150 × 150 균일 격자 · 요소당 물질점 4 개** | stated |
| ⇒ 요소 크기 | **8 µm** | derived(ours) |
| 지름당 요소 | 최소 **4** (31 µm), 평균 **≈ 8**, 최대 **≈ 32** ("about 4 to 32 elements across the diameter, with the average being about 8") | stated (산술 31/8 = 3.9 · 57/8 = 7.1 · 250/8 = 31) |
| 마찰계수 (마찰 미끄럼 경우) | **μ = 0.3** | stated |
| 총 전단 · 비용 | 평균 전단 **> 80 %** · **Cray YMP 단일 프로세서 ≈ 30 h · 25,124 계산 주기** | stated |
| ⇒ 평균 Δt | 80 % 전단까지 25,124 주기라 가정하면 **≈ 0.38 ns** — dx/c_L (2.4 ns) 의 ≈ 0.16 배 | derived(ours) · 가정 포함 |
| 비교 그림 | Fig 6 = **75 % 전단**에서 (a) no slip vs (b) 마찰 미끄럼 · Fig 7 = **63 % · 71 %** 주응력차 · Fig 8 = **25 · 50 · 75 %** 열 평균 수직 변위 | stated |
| 전단 띠 폭 | 영역의 **≈ 1/3** = 평균 지름 **7 개** | stated (산술 0.4 mm / 57 µm = 7.0) |
| 문헌 대조 | 저속 전단 실험 **5–15** 평균 지름 · 고속 알루미나 (파괴 없을 때) **20–40** 평균 지름 | stated |
| 고체 분율 (초기 배치) | **[미확인]** — 그림은 검정 (공극) 이 넓은 성긴 2D 배치 (Fig 5) | — |

### 3-3. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 압밀 · 치밀화 · 기공률 | **없음** — 전단 (부피 일정) 과 경사면뿐 |
| 3D 계산 | **없음** (§4 첫 문장 *"carried out in two dimensions"*) |
| 시간 간격 · CFL 수 · 총 물질점 수 | **[미확인]** (주기 수 25,124 만) |
| 접촉 보정의 시간 단계 내 위치 | 단계 목록 (1–4) 은 단일 속도장 기준으로만 적혀 있다 — 식 (15) 의 /Δt 꼴로 보아 **운동량 갱신 (9) 뒤 갱신 속도에 거는 보정**으로 읽힌다 [우리 판독] |
| 알갱이별 격자장의 **저장 방식 · 메모리** | **없음** — *"since the shape functions have compact support, only those nodes in the vicinity of the grain will have a meaningful velocity"* 한 줄뿐 |
| 법선 n_i^g 의 부호 규약 | "∇ρ_e^g 가 법선 방향을 준다" 뿐 — 바깥 단위 법선이면 −∇ρ/‖∇ρ‖ 이어야 한다 [우리 판독] |
| 힘 사슬 · 전단 띠의 정량 통계 | **없음** (그림 + 정성 서술) |
| 실험 대조 | **없음** (문헌 서술과의 정성 비교만) |
| 반발 · 감쇠 계수 (COR) | **없음** — 접촉은 속도 보정이라 반발 계수 자리가 없다 |
| 회전 · 구름 저항 마찰 | **없음** — *"As a first approximation, the above sliding friction algorithm is felt to be reasonable"* |

---

## 4. 방법 ★

### 4-1. MPM 기본 알고리즘 (§2, 식 1–11) — FLIP 계열

- **지배식**: 운동량 ρ dv/dt = ∇·σ (1), 물질미분 d/dt = ∂/∂t + v·∇ (2).  Lagrangian 단계에서 풀어 **대류항이 없다**.
- **격자**: 계산 영역 전체를 덮는 배경 격자 (알갱이 경계에 맞추지 않음).  각 알갱이 = 물질점 묶음.  물질점이 질량 · 속도 · 응력 · 이력변수를 실어 나른다 ("transport material properties assigned to them without error").
- **P2G (가중 최소제곱 → 집중 질량)**: Σ_j m_ij^n v_j^n = Σ_p m_p v_p^n N_i(x_p^n) (3), 일관 질량 m_ij^n = Σ_p m_p N_i(x_p^n) N_j(x_p^n) (4) → 실제로는 **집중 질량** m_i^n v_i^n = Σ_p m_p v_p^n N_i(x_p^n) (5), m_i^n = Σ_p m_p N_i(x_p^n) (6).
- **형상함수**: **1차 B-spline 의 텐서곱** (이 논문의 계산 전부).
- **내부력**: f_i^int = −Σ_p G_pi^n m_p σ_p^n / ρ_p (7), G_pi^n = ∇N_i at x_p (8).  "MPM" 이라는 이름의 뜻 = FLIP 와 달리 **변형구배 · 응력 · 이력변수를 물질점에 싣는다**.
- **격자 갱신**: m_i^n [v_i^{n+1} − v_i^n] = Δt f_i^int (9).
- **G2P (FLIP 꼴)**: x_p^{n+1} = x_p^n + Δt Σ_i v_i^{n+1} N_i(x_p^n) (10), v_p^{n+1} = v_p^n + Σ_i [v_i^{n+1} − v_i^n] N_i(x_p^n) (11) — **속도 증분**을 보간한다.  이어 변형구배 · 변형률 · 응력 갱신, 필요하면 격자 재정의 (4 단계).

★ 우리 코드와의 차이 [우리 코드 판독]: 우리 MLS-MPM 은 **2차 B-spline** 가중치 (`w = [0.5(1.5−fx)², 0.75−(fx−1)², 0.5(fx−0.5)²]`, 3×3×3 지지) · **APIC 꼴** (입자 속도 = 격자 속도 보간 + 아핀 행렬 C) · f32 · 응력을 P2G 운동량에 접어 넣는 MLS 꼴이다 (`scripts/mpm3d_compaction.py` 2943–3034 행, 파일 커밋 `cb5a6a445`).  접촉 보정은 "격자 속도를 고치는 단계" 라 P2G 와 G2P 사이에 들어가므로 전달 방식 (FLIP/APIC) 과 원리상 충돌하지 않는다 [우리 추론].

### 4-2. ★★★ 접촉 알고리즘 (§3, 식 12–24) — 단계별

**(1) 알갱이별 속도장과 질량중심 속도장.**  단일 속도장 v_i (식 5) 는 모든 물질점의 질량 가중 평균이라 **질량중심 속도장 (center-of-mass velocity field)** 이라 부른다.  같은 절차를 **한 알갱이의 물질점만** 돌리면 그 알갱이 혼자의 운동 방정식이 풀린다 → 노드마다 알갱이별 속도 v_i^g (g = 1…N_g, i = 1…N_n).  "형상함수가 compact support 라 알갱이 근처 노드만 의미 있는 속도를 갖고 나머지는 0".  알갱이별 노드 질량은 그 알갱이의 물질점만으로 m_i^g = Σ_{p=1}^{N_p^g} m_p N_i(x_p) (16).

**(2) 접촉 = 두 장이 다른 노드.**  혼자 떨어진 알갱이 근처에서는 v_i^g 와 v_i 가 같다.  *"we define contact precisely when these fields differ"*.  ⇒ **별도의 접촉 탐색 단계가 없다** (PIC 의 장점, 초록).

**(3) 접근할 때만 구속 (= 자유 분리).**
> (v_i^g − v_i)·n_i^g > 0    (12)   — 알갱이 속도가 법선 방향으로 질량중심 속도를 "앞지를 때"

조건이 서면 법선 성분을 질량중심 값으로:
> ṽ_i^g·n_i^g = v_i·n_i^g    (13)  ⇔  ṽ_i^g = v_i^g − [(v_i^g − v_i)·n_i^g] n_i^g    (14)

이유: *"We know that the center-of-mass velocity does not allow interpenetration of the grains, so this choice is natural.  Note that the inequality in (12) allows grains to separate freely without constraints."*
동치인 법선력: f_{n,i}^g = −m_i^g[(v_i^g − v_i)·n_i^g]/Δt = m_i^g[(ṽ_i^g − v_i^g)·n_i^g]/Δt (15).

**(4) 마찰 = 붙임에 필요한 접선력을 Coulomb 한계로 자른다.**
상대 접선 속도: (v_i^g − v_i) − [(v_i^g − v_i)·n_i^g] n_i^g = n_i^g × [(v_i^g − v_i) × n_i^g] (17).
완전히 붙이는 접선력 (no-slip): f_{stick,i}^g = −m_i^g n_i^g × [(v_i^g − v_i) × n_i^g]/Δt (18).
Coulomb: f_{fric,i}^g = (f_{stick,i}^g / ‖f_{stick,i}^g‖) · min(μ‖f_{n,i}^g‖, ‖f_{stick,i}^g‖) (19) — 작은 접선력이면 붙임, 크면 μ·법선력 (접촉면적 무관) 으로 미끄럼.
다시 쓰면 f_{fric,i}^g = −(m_i^g/Δt) μ′ [(v_i^g − v_i)·n_i^g] (n_i^g × ω̂) (20), 여기서
> μ′ = min( μ, ‖(v_i^g − v_i) × n_i^g‖ / ((v_i^g − v_i)·n_i^g) )    (21)
> ω̂ = (v_i^g − v_i) × n_i^g / ‖(v_i^g − v_i) × n_i^g‖    (22)

n_i^g × ω̂ = (상대 접선 속도 방향의 단위 벡터) [벡터 항등식 — 우리 확인].

**(5) 최종 갱신 (법선 + 마찰 한 줄).**
> **ṽ_i^g = v_i^g − [(v_i^g − v_i)·n_i^g] (n_i^g + μ′ n_i^g × ω̂)**    (23)

*"It is this condition that gives the complete kinematical constraint required to ensure no normal penetration and sliding friction."*  μ′ = 비율이면 접선 상대속도가 0 이 되는 붙음, μ′ = μ 면 미끄럼.  μ → ∞ 이면 **접근하는 노드에서** ṽ_i^g = v_i (붙음) 가 되지만, 멀어질 때는 여전히 자유 분리라 **단일 속도장 (분리 판정 없음) 과 같지 않다** [우리 산술].

**(6) 법선 계산.**  알갱이마다 물질점 질량을 **요소 중심** x_e 에 보간해 요소 부피 Ω_e 로 나눈 밀도
> ρ_e^g = Σ_{p=1}^{N_i^g} m_p^g S^(2)(x_e − x_p) / Ω_e    (24)   (S^(2) = **2차 B-spline** 텐서곱; 합의 상한이 인쇄상 N_i^g — 식 (16) 은 N_p^g)

의 기울기를 **노드에서** 계산해 법선 방향으로 쓴다.  ⚠ *"The interaction between grains is therefore not along a common normal, which results in small errors in momentum conservation."* — 두 알갱이가 각자 법선을 쓰므로 n¹ ≠ −n² 일 수 있다.

**(7) 비용.**  *"we do not compare the grain velocities v_i^g pairwise, rather we compare each v_i^g to the common center-of-mass field v_i.  Therefore, the adjustment of v_i^g for all g is done in one sweep through the grains without any iteration.  The resulting algorithm is linear in the number of grains."*  (no slip 은 기본 알고리즘에 *"at no additional cost"* 로 들어 있다.)

**(8) 마찰 모형의 범위.**  건조 미끄럼 마찰만.  운동 마찰 (미끄러지면 μ 감소) · 구름 마찰은 *"might be more appropriate"* 하나 넣지 않았다 — *"not much is known experimentally about the true magnitude of the frictional forces."*

### 4-3. 의사코드 — 한 시간 단계 (우리 전사 · 논문에 이 꼴로는 없음)

```
# (논문 식 번호) · [우리 판독/추론] 표시
for 각 알갱이 g:                       # 알갱이별 P2G
    m_i^g  = Σ_{p∈g} m_p N_i(x_p)        (16)
    (m v)_i^g = Σ_{p∈g} m_p v_p N_i(x_p)
m_i = Σ_g m_i^g ;  v_i = Σ_g (m v)_i^g / m_i      (5)(6) 질량중심장
각 장을 운동량 갱신 (9) 으로 전진 → v_i^g(n+1), v_i(n+1)   [우리 판독: 보정은 갱신 뒤]
n_i^g = 바깥 단위 법선 ← −∇ρ_e^g (24) 를 노드에서           [부호 = 우리 판독]
for 각 노드 i, 각 알갱이 g (m_i^g > 0):
    d = v_i^g − v_i
    if d · n_i^g > 0:                    (12) 접근 → 구속
        dn = d · n_i^g ;  dt_vec = d − dn n_i^g          (17)
        mu' = min(μ, ‖dt_vec‖ / dn)                      (21)
        t̂ = dt_vec / ‖dt_vec‖  (= n × ω̂)                 (22)
        v_i^g ← v_i^g − dn (n_i^g + mu' t̂)              (23)
    else: 그대로 (자유 분리)
G2P: 각 물질점은 **자기 알갱이의 장** v_i^g 에서 (10)(11)
```

### 4-4. 비용 · 확장성 — 논문 진술과 **우리 3D 규모** 산술

| 항목 | 논문 (2D 전단) | 우리 3D (real_14 침대) | 라벨 |
|---|---|---|---|
| 알갱이 수 | 369 | SE 씨앗 **32,832** + AM **457** (`docs/data/real14_se_scaffold.csv` · `real14_am_scaffold.csv`) | stated / 우리 기록 |
| 격자 노드 | 151² ≈ 2.3 × 10⁴ | n_grid 384 · nz ≥ n_grid (코드 기본) → ≥ 384³ ≈ **5.7 × 10⁷** | derived(ours) |
| 장 하나 (질량 1 + 속도 d) | 2D f64 가정 시 ≈ 0.5 MB | f32 · 16 B/노드 → **≈ 0.91 GB** (지금 `grid_v` + `grid_m` 과 같은 크기) | derived(ours) · 가정 |
| 알갱이마다 장을 통째로 | 369 × 2.3 × 10⁴ ≈ 8.4 × 10⁶ 노드-칸 (가능) | 32,832 × 0.91 GB ≈ **30 TB** → **불가능** | derived(ours) |
| 대안 1 — 희소 슬롯 | — | 노드당 물체 칸 S 개 (번호 + 질량 + 속도 + 법선 …) — 2001 개정판이 "접촉 노드당 물체 ≤ 2" 로 분석을 좁힌 것과 맞물림; S = 2 · 칸당 36 B 가정 시 ≈ 4 GB | 우리 추론 · 가정 |
| 대안 2 — '색칠' 장 | — | 같은 노드를 공유할 수 있는 알갱이끼리 다른 색 → 색 K 개의 장만 둔다 (K × 0.91 GB + 법선 등) · 압밀 중 이웃이 바뀌므로 주기적으로 다시 칠해야 하고, 같은 색끼리 닿으면 그 걸음에서 붙는다 | **논문에 없음 — 우리 추론** |
| 계산 비용 | 알갱이 수에 선형 · 반복 없음 · Cray YMP 30 h | 접촉 보정 자체는 노드당 상수 — 비용은 장 수 (P2G 반복) 와 메모리 대역폭이 정할 것 | stated / 우리 추론 |

⇒ 논문의 "선형 비용" 은 **계산** 이야기이고, 3D 수만 알갱이에서의 병목은 **저장 · 위상 (한 노드에 몇 알갱이)** 이다.  이것이 후보 A′ 의 첫 설계 질문이다 (§10).

### 4-5. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 형상 | 원판 (2D) — 구 형상이 시작점이나 **변형 연속체**라 형상이 바뀐다 |
| 크기 분포 | 다분산 (31–250 µm, 평균 57 µm) — 분포 함수는 [미확인] |
| 소성 표현 | **진짜 형상 소성** — 알갱이 내부를 von Mises + 선형 경화 연속체로 푼다 (δ-겹침 대리가 아님) |
| 접촉 | 알갱이 간 **명시적 접촉 법칙** (침투 금지 + Coulomb 마찰 + 자유 분리) — 접촉은 노드 단위, 짝 목록 없음 |
| 강체/변형체 | 전부 변형체 (경사면은 계산 영역 경계 = 강체 벽) |
| 파괴 · 결합 · 점착 | 없음 |
| 무작위성 | 초기 배치 하나 · 시드 · 반복 없음 |

---

## 5. 결과 — 절별

### 5-1. 경사면 위 원판 (§4.1, Fig 1–4)

- **배치 (Fig 1)**: (a) 실제 경사면 · (b) 계산 — 면을 격자 경계에 정렬하고 중력을 θ 만큼 기울인다.  원판은 영역 경계와 마찰 접촉 (강체 벽 시험).
- **해석해 (식 25)**: 정지에서 출발한 강체 원판의 질량중심 x 좌표 — tanθ > 3μ 이면 미끄러지며 구름 x0 + ½|g|t²(sinθ − μcosθ), 아니면 미끄럼 없이 구름 x0 + ⅓|g|t² sinθ.
- **Fig 2 (μ 0.3 · 0.9, θ π/3, 0.5R)**: μ 0.3 은 *"slides as it rolls"*, μ 0.9 는 접점이 미끄러지지 않는다; 두 경우 모두 **변형 원판이 강체보다 늦다**.  계산 곡선의 순서 (μ 0.3 위) 도 해석해와 같다.
- **Fig 3 (μ 0.5, θ π/3 · π/6, 0.5R)**: 변형 원판이 강체 해와 *"compare well"*; 이 격자에서 **최대 차이 = μ 0.5 · θ π/6 (구름)** 경우 (그림 판독: t = 0.3 에서 해석해 변위의 ≈ 0.17 배).
- **Fig 4 (격자 수렴, μ 0.5 · θ π/6)**: 0.5R · 0.25R · 0.125R → *"With 16 elements across the diameter, the agreement … is excellent; and with 8 elements across the diameter the discrepancy is small."*  (그림 판독 t = 0.4: 변위비 ≈ 0.23 · 0.77 · 1.0.)
- **해상도 규칙 (저자)**: 다음 절의 다분산 시료는 지름당 4–32 요소 (평균 8) 라 *"The contact forces should therefore be reasonably resolved, even for the smallest grains."*

### 5-2. 원판 369 개 전단 (§4.2, Fig 5–8)

- **왜 이 문제인가 (저자)**: 큰 전단은 많은 알갱이 + 정확한 접촉력 · 변형이 필요하고, 각 알갱이가 많은 상대를 만나 *"a priori determination of contacting faces is essentially impossible"* — 효율적 접촉 알고리즘 없이는 문제 크기가 막힌다.
- **설정 (Fig 5)**: 위 표 3-2.  가장 작은 알갱이는 지름당 4 요소라 *"clearly insufficient to resolve the stress distribution within the small grains.  The objective is to accurately calculate the contact forces and find the load carrying paths."*  비슷한 해상도의 충돌 운동량 · 에너지 전달은 선행 연구 [2] 에서 좋은 결과.
- **Fig 6 — 핵심 대비 (75 % 전단)**: (a) 접촉 알고리즘 **구현 전** = no slip, (b) 구현 후 μ 0.3.  *"For the no slip case, there is extensive plastic deformation of the grains and large voids are created.  For the case where contact is frictional slip, the situation is completely different.  Shear deformation is accommodated by grain rolling and sliding with fairly little plastic deformation."*  (색이 두 그림에서 다른 것은 입력 처리 방식 차이일 뿐 — 초기 배치 · 해상도 · 전단량은 같다.)
- **Fig 7 — 일시적 힘 사슬 (63 % · 71 %)**: 주응력차 (광탄성이 밝히는 양) 가 큰 영역 = 흰색.  여러 알갱이를 잇는 사슬이 두 프레임 모두에 있고, 8 % 전단 사이에 오른쪽 위 사슬은 사라지고 주대각선 근처 사슬은 다른 알갱이로 옮겨 가며 왼쪽 아래 사슬은 남는다.  기전 (저자): *"Force chains are created when the grains bind, i.e. translation and sliding are insufficient to accommodate the deformation, and the grains deform."*  ★ 저자 서술: *"In the case where granular material is compressed uniaxially the network of force chains is stationary in time over a range of deformation"* (이 문장엔 인용 번호 없음) — 반면 일정 부피 전단에서는 구속력이 크게 출렁이고 망이 잠깐 생겼다 바뀐다 (실험 [13]).
- **Fig 8 — 전단 띠 (25 · 50 · 75 %)**: 계산 요소 열마다 모든 물질의 수직 변위를 평균 (점선) ↔ 균일 변형 (실선).  움직임이 오른쪽 이동 경계 근처에 몰린다; 작은 출렁임은 알갱이 회전 탓.  띠 폭 ≈ 영역 1/3 ≈ **평균 지름 7 개** — 저속 실험 5–15 와 맞고 고속 알루미나 20–40 보다 작다.  (⚠ 본문의 인용 번호: 저속 5–15 에 [14], 고속 알루미나 20–40 에 [16] 을 붙였는데 참고문헌 목록에서 [14] = Nesterenko 외 *고속* 알루미나, [16] = Scarpelli & Wood *직접 전단 시험* — **번호가 뒤바뀐 것으로 보인다** [우리 판독].)
- **결론 (§5)**: *"A comparison of a simulation using noslip contact with one using sliding frictional contact shows a dramatic change in the predicted deformation and highlights the need for accurate contact algorithms."*

---

## 6. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/bardenhagen2000_mpm_granular_multibody_frictional_contact/` · 300 dpi · 캡션 문자 제외 · 8 장 + 식 5 장.  MPM 관점의 [우리 …] 표지는 논문 밖 판단이다.

| 그림 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | 경사면 위 원판 모식 (a) 과 계산 배치 (b — 면을 격자 경계에 맞추고 중력을 θ 만큼 기울임) | 원판은 **계산 영역 경계 (강체 벽)** 와 마찰 접촉한다.  우리 MPM 의 바닥 · 옆벽은 법선 속도만 막고 접선 마찰이 없고, AM 장애물은 노드 속도를 통째로 0 으로 놓아 '붙음' 이다 [우리 코드 판독, 2985–3003 행].  식 (23) 을 벽 · AM 노드에 적용 (v_i 자리에 벽 · AM 속도) 하는 것이 다중 속도장 없이 할 수 있는 A′ 의 가장 작은 첫 단계 [우리 추론] |
| 2 | `fig_2.png` | 변형 원판 질량중심 x 위치 (점선) vs 강체 해석해 (실선), μ 0.3 · 0.9, θ π/3 — 두 해 모두 μ 0.3 이 위 | 지름 4 요소 거친 격자로도 미끄럼 (μ 0.3) · 구름 (μ 0.9) 두 체제를 순서대로 재현, 변형 원판은 느리다 (t = 0.3 변위비 ≈ 0.76 · 0.87, 판독).  우리 MPM 에는 μ 가 없어 이 체제 구분이 원리상 없다 — 물체 1 + 벽 = 장 2 개짜리 2D 회귀 시험 [우리 추론].  ⚠ 세로축 'cm' 는 해석해와 맞추면 m [우리 산술] |
| 3 | `fig_3.png` | 같은 그림, μ 0.5 · θ π/3 과 π/6 — θ π/3 이 위 | 이 격자의 최대 오차 = **구름 경우 (π/6)** (변위비 ≈ 0.17 vs 미끄럼 ≈ 0.86, 판독).  구름은 법선 · 표면 기하 정확도에 민감 → 압밀 초기 SE 가 AM 표면을 따라 굴러 재배열하려면 해상도 조건이 먼저 걸린다 [우리 추론] |
| 4 | `fig_4.png` | μ 0.5 · θ π/6 에서 격자 0.5R · 0.25R · 0.125R | 지름당 16 요소 ≈ 해석해, 8 요소 '작은 차이' (판독 ≈ 0.77), 4 요소 ≈ 0.23 → 실용 문턱 **지름당 ≥ 8 요소**.  우리 SE 1 µm 는 n_grid 384 · dx ≈ 0.141 µm 에서 ≈ 7 셀 — 문턱 바로 아래 [우리 산술]; A′ 에서는 SE 크기 선택이 격자 · 메모리 예산을 정한다 |
| 5 | `fig_5.png` | 전단 계산 초기 배치 (색 = 알갱이 구분, 검정 = 공극) | HMX 근사 von Mises 원판 369 개, 논문은 **알갱이마다 격자장 하나**.  우리 3D (SE 32,832 · 384³ 급) 에서 알갱이별 장은 ≈ 30 TB (f32 · 장당 0.91 GB 가정) 라 불가 → 소수의 '색칠' 장이나 노드당 희소 슬롯이 필요 (논문에 없음 · 우리 추론).  물질점마다 알갱이 번호도 필요 — 지금 MPM 은 SE 를 DEM 중심 구의 합집합으로 심어 번호가 없다 → 입자 번호 승계 (Ⓑ) 가 선행 조건 |
| 6 | `fig_6.png` | 75 % 전단 변형: (a) no slip, (b) 마찰 미끄럼 접촉 | ★ (a) = 접촉 알고리즘 없는 **단일 속도장** — 큰 소성 변형 + 큰 공극; (b) μ 0.3 — 구름 · 미끄럼, 소성 적음.  **우리 MPM 은 (a) 쪽**이다: 재배열 (미끄럼 · 구름 · 분리) 이 막혀 변형이 소성 유동으로만 간다.  우리 기록 '단일 속도장 연속체 MPM 은 연화 없이 압밀을 재현 못 했다' 의 기전 후보 — A′ 로 시험할 가설 (이 그림은 압밀이 아니라 전단 · 우리 추론) |
| 7 | `fig_7.png` | 주응력차로 본 힘 사슬, 63 % 와 71 % 전단 | 마찰 접촉 계산에서 사슬이 생겼다 사라진다 (광탄성 관찰과 같은 꼴).  우리 scaffold MPM 은 AM 을 얼려 AM 을 지나는 사슬이 원리상 없고 AM 하중 분담 f 를 DEM 에서 빌린다; AM 을 움직이는 물체로 넣은 A (+ A′) 라면 이 지도로 f 를 계산할 수 있다 [우리 추론].  논문: 일축 압축에서는 사슬망이 변형 구간 동안 정지에 가깝다 |
| 8 | `fig_8.png` | 열 평균 수직 변위 (점선) vs 균일 변위 (실선), 25 · 50 · 75 % 전단 | 전단 띠 ≈ 영역 1/3 ≈ 평균 지름 7 개.  같은 판독 (높이별 평균 변위 · 밀도) 을 가압에 쓰면 벽 마찰에 따른 밀도 구배를 볼 수 있는데, 우리 MPM 은 벽 마찰이 없어 그 구배를 원리상 못 낸다 [우리 추론] |

**식 그림 (텍스트 층이 깨져 렌더로 동봉)**: `eq_12_16_normal_constraint.png` (접근 판정 · 법선 구속 · 법선력 · 알갱이 노드 질량) · `eq_17_18_stick_force.png` (상대 접선 속도 · 붙임 접선력) · `eq_19_23_coulomb_friction_update.png` (Coulomb 마찰 · μ′ · ω̂ · 최종 갱신 23) · `eq_24_grain_density_normal.png` (2차 B-spline 밀도 · 법선 · "공통 법선 아님") · `eq_25_rigid_disk_solution.png` (강체 원판 해석해).

---

## 7. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 질량중심 x 위치 vs 시간 | 계산 (점선) ↔ 강체 해석해 (실선) 겹쳐 그림 | A′ 회귀 시험 판정 형식 그대로 |
| 격자 수렴 | 요소 0.5R · 0.25R · 0.125R 세 곡선 | 지름당 요소 수로 말하는 해상도 규칙 |
| 변형 지도 | 같은 시점 (75 %) 의 두 접촉 조건 나란히 (Fig 6) | "단일 속도장 vs 접촉" 대비 그림의 원형 |
| 힘 사슬 | **주응력차** 를 영역 전체에 그림 (광탄성 모사) | 우리 MPM 응력장에서 바로 만들 수 있는 지도 [우리 추론] |
| 전단 띠 | 계산 요소 **열**마다 모든 물질의 수직 변위 평균 → 균일 변형 직선과 비교 | 가압 판독으로는 '높이별 평균 변위 · 밀도' 로 옮김 [우리 추론] |
| 도구 | [미확인] | — |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | Bardenhagen 2000 | 우리 DEM (LIGGGHTS) | 우리 MPM (Taichi scaffold) |
|---|---|---|---|
| 알갱이 표현 | 변형 연속체 (물질점 묶음) | 영원한 강체 구 (겹침 δ = 소성 대리) | SE = 연속체 (알갱이 정체성 없음 · DEM 중심 구의 합집합) · AM = 얼린 장애물 |
| 알갱이 간 접촉 | 알갱이별 장 ↔ 질량중심 장 비교 · Coulomb · 자유 분리 · 구름 | hooke/hysteresis (탄성 + 이력) · 마찰 · 분리 | **단일 속도장 = 붙음** (미끄럼 없음 · 분리 판정 없음) |
| 벽 · 강체 | 영역 경계와 마찰 접촉 | 판 · 벽 메시 | 바닥 · 옆벽 = 법선만 막음 (분리 가능 · 마찰 없음) · 판 = 판 위 노드 법선 속도를 판 속도로 **양방향** 고정 · AM = 노드 속도 0 (붙음) [우리 코드 판독] |
| 형상 소성 | 있음 (von Mises + 선형 경화) | 없음 | 있음 (J2) |
| 접촉망 (어느 쌍이 닿나) | 접촉 노드로 암묵 — 짝 목록 없음 | 명시 짝 목록 (Kirchhoff 수송의 입력) | 없음 |
| 차원 · 규모 | 2D · 369 | 3D · 10⁴–10⁵ | 3D · SE 씨앗 3.3 만 |
| 압밀 | **없음** | 300 MPa | DEM 끝에서 짧은 재압축 |
| 제하 | 없음 | 있음 | 부분 (재시작 제하) |
| 재료 강성 | HMX 근사 E ≈ 18.5 GPa · σ_y 0.3 GPa (연화 없음) | SE E_eff 1.35 GPa (≈ 18 배 연화) | SE E 1.53 GPa (연화) · ν 0.49 · σ_y 0.30 GPa |

### 8-2. 전이되는 것 / 안 되는 것

- ✅ **알고리즘 전체** (식 12–24) — 재료 무관.
- ✅ **해상도 규칙** — 지름당 ≥ 8 요소 (접촉력 · 구름), 4 요소는 내부 응력 · 구름에 부족.
- ✅ **정성 결론** — 같은 배치에서 접촉 조건 (붙음 ↔ 마찰 미끄럼) 만 바꿔도 변형 양상 (소성 ↔ 재배열) 이 바뀐다.
- ✅ **시험 문제** — 경사면 원판 (해석해 식 25).
- ❌ HMX · 고무 원판의 수치, 전단 띠 폭 (7 지름), 힘 사슬 모양 — 재료 · 2D · 전단 (압밀 아님) 이라 전이 불가.
- ❌ 비용 30 h (1999 Cray YMP) — 하드웨어 · 차원이 달라 의미 없음.
- ⚠ HMX 근사 알갱이의 강성 (E ≈ 18.5 GPa, σ_y 0.3 GPa — derived) 은 실제 LPSCl (E 22–24 GPa, σ_y 0.05–0.30 GPa) 과 **자릿수가 비슷하다** — 다만 이것은 숫자 관찰일 뿐 재료 전이가 아니다.

### 8-3. frame 판정

- **frame [5] (분업)**: 이 논문은 MPM 쪽 (형상 소성) 에 **접촉 자유도**를 더한다 — DEM 고유로 둔 "알갱이 재배열 · 미끄럼" 의 일부를 MPM 이 가져올 수 있다는 뜻.  단 접촉은 **노드 단위**라 짝 목록 (접촉당 Holm 협착의 입력) 은 바로 나오지 않는다 — 노드의 물체 쌍을 모아 후처리로 만들 수 있다 [우리 추론].  ⇒ 수송 (DEM 접촉망 · STEP3 복셀) 분업은 그대로.
- **frame [4] (교차 맞춤 금지)**: A′ 를 만들면 DEM 이 아니라 **실험** (1저자 11-09: 실험실 표준 기공률 10–13 % · 진밀도 1.64 g/cm³ · 질량 기준) 에 따로 보정해야 한다.
- **frame [1]/[2] (연화)**: 우리 기록의 "연화는 빠진 알갱이 재배열을 뭉뚱그린 것" 이라는 해석과 이 논문의 Fig 6 은 **같은 방향**이다 — 빠진 것이 구성식 항이 아니라 **접촉 자유도** 일 수 있다 (가설, §9-①).

---

## 9. 깊은 통찰

① **빠진 자유도는 구성식이 아니라 운동학 (접촉) 일 수 있다.**  우리의 막다른 길 (DPC cap · shear-jam · bulk-jam, `docs/mpm_dpc_cap_crosscheck.md`) 은 전부 **단일 속도장 안의 구성식** 탐색이었다.  이 논문은 단일 속도장이 곧 "자동 no slip" 이고, 접촉만 바꿔도 변형이 소성 → 구름 · 미끄럼으로 바뀜을 보인다 (Fig 6).  ⇒ 정확한 문장 = *"단일 속도장 MPM 에서는 연화를 구성식으로 대체하지 못했다"* — 접촉을 푼 MPM 에서의 연화 필요성은 **미시험** (같은 결론을 MPM + contact dynamics 계열 Nezamabadi 2022 카드도 낸다 — stage B 반입 예정).

② **"알갱이 수에 선형" 은 계산 이야기, 3D 병목은 저장 · 위상.**  알갱이별 장을 통째로 두면 우리 규모에서 ≈ 30 TB (§4-4).  색칠 장 · 희소 슬롯 같은 저장 설계가 A′ 의 첫 결정이고, 논문은 이를 다루지 않는다.  2001 개정판이 스스로 "접촉 노드당 물체 ≤ 2" 로 분석을 좁힌 것은 희소 슬롯 설계와 맞물리지만, 조밀 3D 압밀의 삼중점 (한 노드에 셋) 에서는 그 성질이 깨진다.

③ **접촉 판정 거리 = 셀 크기 → 압밀 기공률의 계통 오차 후보.**  "두 장이 다르면 접촉" 은 두 알갱이의 물질점이 **같은 노드를 공유하는 순간** (표면이 실제로 닿기 전) 성립한다 — 2001 판은 *"Resolution of the interface is commensurate with the computational grid cell size"* 라 적는다.  기공 10–13 % 를 표적으로 하는 우리 압밀에서는 이 '셀 크기 틈' 이 기공률을 올리는 쪽으로 작용할 수 있고, 우리 2차 B-spline (지지 3 셀) 은 1차 (지지 2 셀) 보다 그 거리가 길다 [두 논문 밖 · 우리 추론 — 격자 수렴으로 반드시 확인].

④ **벽 · AM 은 이미 '접촉' 이다 — 종류가 틀렸을 뿐.**  우리 코드: 바닥 · 옆벽 = 한쪽 법선 구속 (마찰 0), 판 = 양방향 법선 고정 (분리 판정 없음), AM = 속도 0 (붙음) [우리 코드 판독].  강체의 속도는 알려져 있으므로 식 (23) 의 v_i 자리에 그 속도를 넣으면 **다중 속도장 없이** 마찰 · 분리 가능한 벽 · AM 접촉이 된다.  구형 AM 은 법선을 기하에서 정확히 줄 수 있어 식 (24) 의 법선 오차도 피한다 [우리 추론].  → 다이 벽 마찰 · AM–SE 미끄럼 · 판 분리 (제하) 를 가장 싸게 시험하는 길.

⑤ **해상도 규칙이 SE 크기 선택과 묶인다.**  지름당 ≥ 8 요소 → SE 1 µm 면 dx ≤ 0.125 µm.  더 작은 SE 는 A′ 에서 사실상 못 푼다 — 후보 C/C′ (DEM) 에는 없는 제약.

⑥ **검증 사다리가 이미 있다.**  강체 해석해 (식 25) → 2D 다물체 → 3D (2001: 구 경사면 · backspin, R/2 의 '평평한 점' 실패가 음성 대조).  A′ 를 Taichi 에 넣으면 압밀 전에 이 사다리부터 오른다 [우리 추론].

⑦ **반발 계수가 없다.**  접촉이 속도 보정이라 에너지 손실이 알고리즘에서 나온다 (2001 판: "완전 비탄성 충돌").  DEM 의 COR 을 A′ 로 옮길 자리가 없다 — 성긴 패킹 생성 (낙하 · 정착) 을 A′ 로 하면 DEM 패킹과 다를 것 → 성긴 초기 패킹은 DEM (P ≈ 0) 이 만들고 압축만 A′ 가 하는 PyCompact · Demirtas 꼴 인계가 자연스럽다 [우리 추론].

⑧ **일축 압축의 힘 사슬망은 정지에 가깝다 (논문의 문헌 요약).**  압밀에서 접촉 위상 (이웃) 이 천천히 바뀐다면 색칠을 자주 다시 할 필요가 없을 수 있다 — 단 성긴 시작의 재배열 구간은 예외 [우리 추론].

---

## 10. [DEM 우선 (수영)] — 후보별 함의 + 구체 행동

| 후보 | 이 논문의 함의 | 판정 |
|---|---|---|
| **A′** (다물체 · 다중 속도장 접촉 MPM) | **직접 기반** — 알고리즘 · 검증 형식 · 해상도 규칙.  그러나 2D · 369 알갱이 · 전단 · 압밀 없음 → **우리 영역 (3D · 수만 · 고밀도 압밀 · 제하) 의 성능 근거는 0** | ✅ 기전 지지 · ⚠ 규모 · 저장 · 이른 접촉 · 삼중점 위험 |
| **A** (움직이는 강체 AM) | 강체와의 마찰 접촉 (영역 경계) 이 이 알고리즘에 들어 있다 → AM 을 강체 물체로 넣으면 AM–SE 마찰 · 분리 · AM 사슬 (→ f 계산) 이 같은 틀에서 나온다 | ✅ 부분 지지 (SE–SE 는 여전히 붙음) |
| **B** (입자 분해 FE / NSCD+FE) | §1 이 Eulerian 미시역학 (Williamson: 알갱이 간 전단 전달 0 = 마찰 무시) · Benson 혼합이론 (단일 속도장이라 미끄럼 불가 → 오차) 의 접촉 한계를 지적 — B 는 FE 접촉으로 이를 피하지만 비용 문제는 이 논문 밖 | 중립 |
| **C / C′** (MDR · 두 재료 항복 캡 DEM) | §1 의 DEM 전제 *"deformations of individual grains are small in comparison with the deformation of the granular assembly"* — 무른 SE 의 큰 변형에서 약해지는 전제.  MDR 이 그 자리를 메우려는 것이라 이 논문은 C 를 반박하지 않는다 | 중립 |
| **D0** (LIGGGHTS gen-2) | 관련 없음 | — |

**구체 행동 (순서 = 싼 것 → 비싼 것; 전부 [우리 추론] · 결과 전 등록 대상)**
1. **A′-0 (장 추가 없음)** — 지금 MPM 의 AM 노드 · 벽에 식 (23) (+ 2001 판의 견인력 분리 판정) 을 넣는다: v_i := AM · 벽 속도, 법선 = 구형 AM 은 기하, 벽은 축.  얻는 것: 다이 벽 마찰 μ_w · AM–SE 미끄럼 · 판 분리 (제하).  시험: 식 (25) 원판-벽 2D · 2001 구 경사면 3D.
2. **위상 사전 점검 (GPU 불요)** — real_14 SE 씨앗 (32,832) 의 물질점을 가장 가까운 DEM 중심 알갱이로 표지해 알갱이별 P2G → 노드당 물체 수 분포 (≥ 2 · ≥ 3 비율) + '노드 공유' 그래프의 탐욕 색칠 색 수 K.  압축 끝 (겹침 큼) 이라 최악 경우이고, 성긴 시작 침대로 한 번 더.
3. **입자 번호 승계 (Ⓑ, `docs/reviews/mpm_coverage_interface_design_memo_20261103.md` §4) 를 A′ 의 선행 조건으로 묶는다** — 같은 번호가 피복 · SE–SE 계면 (Rint ②) · A′ 의 물체 번호가 된다.
4. **해상도 · 메모리 예산표** — SE 지름당 ≥ 8 셀 · 장당 16 B/노드 (f32) · K 장 + 법선 · 견인력 → 침대 크기별 GPU 메모리.
5. **이른 접촉 (셀 크기 틈) 시험** — 순수 SE 압밀을 dx 사다리로 돌려 300 MPa 기공률이 dx 에 따라 움직이는지 (움직이면 거리 기반 판정 보강 필요).
6. **보정 표적 등록** — A′ 는 실험 (기공 10–13 % · 1.64 g/cm³ · 질량 기준) 에 **따로** 보정, DEM 과 맞추지 않는다 (frame [4]).  가설 등록: "A′ 는 실제 SE 강성 (연화 없음) 으로 표적에 닿는가".

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 계산은 **2D** | §4 *"carried out in two dimensions"* |
| 2 | 정확한 접촉은 **모양이 격자로 해상된 매끈한 알갱이**에서만 | 초록 *"contacts are modeled accurately for smooth granules whose shape is resolved by the computation mesh"* |
| 3 | 법선이 공통이 아니어서 **운동량 보존 오차** | §3 *"not along a common normal, which results in small errors in momentum conservation"* |
| 4 | 마찰은 **건조 미끄럼만** (운동 · 구름 마찰 없음) | §3 *"As a first approximation …"* |
| 5 | 작은 알갱이 (지름 4 요소) 의 **내부 응력은 부정확** | §4.2 *"clearly insufficient to resolve the stress distribution within the small grains"* |
| 6 | 거친 격자 (0.5R) 에서 **구름 경우 오차 큼** | §4.1, Fig 3–4 |
| 7 | 비용 | 369 알갱이 · 25,124 주기 · Cray YMP ≈ 30 h |

## 12. 불확실 · PDF 에 없는 것

- DOI · 접수/게재일 · 키워드: PDF 미인쇄 → [미확인] (PII 만 인쇄).
- 시간 간격 · CFL · 총 물질점 수 · 초기 고체 분율: 미기재.
- 접촉 보정의 시간 단계 내 위치 · 법선 부호 · 알갱이별 장의 저장 방식: 명시 없음 (§3-3).
- 그림 세로축 'cm' ↔ 해석해 m 불일치 (우리 산술), 전단 띠 문단의 [14]/[16] 번호 뒤바뀜 (우리 판독), 식 (24) 상한 N_i^g (식 16 은 N_p^g).
- 힘 사슬 · 전단 띠의 정량 통계 · 실험 대조: 없음.
- **압밀에서 이 알고리즘이 어떻게 행동하는지 (고밀도 · 다접촉 노드) 는 이 논문으로 알 수 없다.**

## 13. 인용 가능 문장 (덱 · 원고용)

- "단일 속도장 MPM 에서는 침투가 막히는 대신 닿는 물체 사이 no-slip 접촉이 자동으로 걸린다 (Bardenhagen, Brackbill & Sulsky, CMAME 187, 2000, p.531)."
- "알갱이별 격자 속도장을 하나의 질량중심 속도장과 비교하면 침투 금지 · 자유 분리 · Coulomb 미끄럼 · 구름을 짝 탐색 없이, 알갱이 수에 선형인 비용으로 줄 수 있다 (같은 문헌 §3)."
- "같은 2D 다분산 시료의 큰 전단에서 no-slip 접촉은 큰 소성 변형과 공극을, 마찰 미끄럼 접촉은 구름 · 미끄럼과 적은 소성을 낸다 (같은 문헌 Fig 6)." — ⚠ 전단이지 압밀이 아님을 함께 적을 것.

## 14. 기법 미니 용어집

- **PIC / FLIP** — 입자-격자 혼합법.  FLIP 은 격자의 속도 **증분**을 입자에 보간해 수치 확산을 줄인다 (식 11).
- **MPM** — FLIP 에서 변형구배 · 응력 · 이력변수를 물질점에 실은 고체역학판.
- **집중 질량 (lumped mass)** — 일관 질량 행렬 (식 4) 을 대각으로 바꾼 것 (식 6).
- **질량중심 속도장 (center-of-mass velocity field)** — 모든 물질점의 질량 가중 평균 격자 속도 = 단일 속도장.  다물체 접촉의 공통 기준틀.
- **접촉 노드** — 알갱이 속도장과 질량중심 속도장이 다른 노드 (= 둘 이상 알갱이가 질량을 가진 노드).
- **자유 분리** — 멀어지는 쪽 (식 12 불성립) 에는 아무 구속도 걸지 않는 것.
- **μ′ (유효 마찰계수)** — min(μ, 붙임에 필요한 비).  μ′ < μ 면 붙음, = μ 면 미끄럼.
- **1차 / 2차 B-spline** — MPM 형상함수 (이 논문: 전달 1차, 법선용 밀도 2차).  우리 코드는 전달에 2차.
- **주응력차 (principal stress difference)** — 광탄성 무늬가 보여 주는 양 (최대 전단응력에 비례).

## 15. 관련 카드

- **짝**: `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 이 알고리즘의 개정 (견인력 기반 분리 · 격자 붕괴 안정화 · 3D 검증 · 광탄성 대조).
- `devaucorbeil2020_mpm_after_25_years_review` — MPM 리뷰가 이 다물체 알고리즘을 표준으로 소개 (§5) · 우리 MPM 계보.
- `stomakhin2013_mpm_snow_elastoplastic` · `klar2016_dp_sand_animation` — 우리 MLS/탄소성 MPM 의 계보 (단일 속도장).
- `pycompact2025_dem_mpfem_workflow` · `demirtas2021_mpfem_hollow_sphere_die_compaction` — 입자 분해 FE (후보 B) 와 "DEM 은 패킹만, 압축은 연속체" 인계 꼴.
- `zunker2024_mdr_contact_model_partI` · `zunker2025_dem_large_deformation_compaction` — 후보 C.
- `giannis2021_stress_based_multicontact_dem` · `varkey2026_multicontact_elastoplastic_dem` — DEM 쪽 다접촉 보정.
- (같은 날 stage B 반입 예정) `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` — 입자별 격자 + contact dynamics 로 **압밀**까지 간 2D 후속 (이 카드가 못 보여 주는 고밀도 구간).
- (같은 날 stage A 반입 예정) `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` — 강체 + 무른 입자 혼합 압밀 (후보 B 쪽 유비).
- `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` — 같은 제1 저자의 GIMP 원전 (보간 일반화 · MPM = 델타 특수형 · contiguous particle GIMP · 셀 넘김 잡음 · 1D 초탄성 · 접촉 없음 · 이 논문을 참고문헌에 듦 · 2026-11-12 반입).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
