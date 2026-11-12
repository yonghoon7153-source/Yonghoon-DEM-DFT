# 배치 42 정독 근거 (기존 카드 보강 1 장 · 원문에서 직접 · 2026-11-11)

카드 = `pycompact2025_dem_mpfem_workflow` (보강 뒤 ≈1,090 줄 · 첫 digest 2026-08-25 · 보강 2026-11-11 = 원문 PDF 9 쪽 · 표 · 그림 ·
코드 메타데이터를 다시 읽고 대조 · 그림 폴더 신설 37 장 (그림 4 + 패널 15 · 표 4 · 식 3 + 식 문단 1 · 근거 문단 9) · 판독 원자료
litdb/figures/pycompact2025_dem_mpfem_workflow/digitized.csv — Fig 3e · 4a · 4b 는 원본 래스터에서 두 번 독립 판독해 같은 값).
서지 (k · l 인용용) = Mohammadhosseinzadeh M., Ghorbani-Menghari H., Kim J.H., *PyCompact: An integrated workflow for discrete element
method–multi-particle finite element method for powder compaction simulation*, SoftwareX 33 (2026) 102495, DOI 10.1016/j.softx.2025.102495.
⚠ 아래는 **이번에 새로 더했거나 고친 것만**이다 (보강 전부터 카드에 있던 근거는 되풀이하지 않는다).  재료 = Fe–Si–Al–P 금속 분말 ·
1400–2000 MPa — 우리 LPSCl · NCM 으로 절대값을 옮기지 않는다.

---

## a — 순수 SE 압력별 기공 곡선

보강 없음 (황화물 · SE 없음 — 금속 분말).

## b — 탈압 때 되돌아오는 양 · 잰 방법

- [b] pycompact2025_dem_mpfem_workflow | **고친 값**: Fig 4(a) 제하 — 정점 ε 0.622 / 0.576 → 100 MPa 0.603 / 0.559 → 20 MPa 0.591 / 0.540 → 응력 0 꼬리 끝 ≈0.56 / ≈0.505 (Coarse / Fine) · Δε (정점 → 꼬리 끝) 0.062 / 0.071 = 압축 높이 대비 16.4 / 16.7 % (20 MPa 까지 8.2 / 8.5 %) · 옛 판독 '잔류 ε 0.598 / 0.556 · Δε 0.024 / 0.020 (6.3 / 4.7 %)' 철회 (응력 0 에 닿기 전 값) | 카드 §9.4 · 논문 Fig 4(a) p.7 | [판독] · [카드 산술] | 변형률 정규화 길이 미인쇄 · 금속 · 2000 MPa
- [b] pycompact2025_dem_mpfem_workflow | **고친 값**: Fig 4(b) 제하 가지 기공 2000 MPa 4.4 / 3.3 → 1000 5.6 / 4.4 → 100 8.4 / 6.9 → 20 10.4 / 9.2 → P≈0 끝 17.2 / 16.9 % (Coarse / Fine) · 마지막 수직 구간 (Fine 12.1 → 16.9 %) 은 압력 0–5 MPa **한 화소 안** — 떨어진 펀치의 이동일 수 있음 · 저자 규약 = 제하 중 5 MPa 문턱의 RVE 부피 (p.6) 는 그 아래 끝 | 카드 §3.3 · §9.5 · §10 · Fig 4(b) | [판독] · [카드 추론] (원문 언급 없음) | 금속
- [b] pycompact2025_dem_mpfem_workflow | **새로 더함**: 압분체 되돌아옴 (2000 MPa → 5 MPa 규약 자리) 부피 **+12 % (Coarse) · +11 % (Fine)** = 재료 탄성 체적 P/K 1.4 % (K 141.7 GPa) 의 **≈8 배** · 저자 기전 *"elastic recovery primarily at particle peripheries"* (p.6) + 제하 단면의 틈 (Fig 4e/f) | 카드 §15.5 | [카드 산술] (하중 중 RD [판독] · 5 MPa RD stated) · [카드 추론] | 금속 · 2000 MPa
- [b] pycompact2025_dem_mpfem_workflow | **철회**: 옛 판정 '제하 후 RD 삼각형 5–7 %p 불일치' — 같은 펀치 부피로 Fig 4a ↔ 4b ↔ 본문 (85.4 %) 이 꼬리 끝 0.3–0.7 %p · 20 MPa 1.2–1.7 %p 안에서 맞는다 | 카드 §10 표 | [카드 산술] | —

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] pycompact2025_dem_mpfem_workflow | **고친 산술 · 표기**: Swift σ = K(ε + ε0)^n (식 3) 의 σ(ε=0) = 1380 × 0.0354^0.254 = **590.7 MPa** (옛 590.6) · σ(ε=1.0) 1392 MPa 는 '포화유동응력' 이 아니라 ε = 1.0 의 유동응력 (Swift 는 포화 없음) · 재료 모형 = *PIECEWISE_LINEAR_PLASTICITY* — 원문은 'J2 · von Mises 항복' 이라 쓰지 않는다 (옛 'J2형' 은 카드 해석) | 카드 §3.1 · §7.3 · 논문 식 3 p.5 · p.3 | 인쇄 · [카드 산술] | 금속 값 — 전이 0

## d — 단단한 입자의 하중 몫 · 재밍

보강 없음 (1 상 분말).

## e — 점접촉 법칙이 깨지는 범위와 대안 · 맞춘 값 수

- [e] pycompact2025_dem_mpfem_workflow | **새로 정리**: 대안 = 입자별 FE (MPFEM) — DEM 접촉 법칙 (Hertz–Mindlin · μ 0.5 · μr 0.05 · e 0.7) 은 넘긴 뒤 쓰이지 않고 (CSV 칸에 안 들어감) FE 벌칙 접촉 + Coulomb **μ 0.2** 로 바뀐다 · 맞춘 값 = FE 마찰 **하나** (*"selected for best experimental agreement"* p.6) · 재료 상수 5 개 (K · n · ε0 · E · ν) 는 [17] 에서 가져옴 · DEM 재료 값 (E · ν · 밀도 · 시간 간격) 은 사용자 템플릿 안 — 원문 미인쇄 (p.3 *"The template file provides … definitions of material properties …"*) | 카드 §4.7 (마) · §7.1 | 인쇄 | 금속

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

- [f] pycompact2025_dem_mpfem_workflow | **고친 값 (FE 해상도 규칙 — MPM 아님)**: 95 % 밀도 축응력 그림 다섯 점 1641 · 1529 · 1469 · 1398 · 1379 MPa (500 → 2500 요소/입자) — 마지막 증분 **−1.4 %** (그림 = 평탄화) ↔ 본문 2500 = **1310** MPa (−6.3 %) — 수렴 판정이 원문 안에서 갈린다 · 옛 '−5 % · 미수렴' 철회 · 지름당 요소 변 ≈4.8 → 8.3 개 (2000 요소 ≈7.7 개) | 카드 §3.4 · §9.1 · Fig 3(e) p.5 · 본문 p.6 | [판독] (1 화소 = 4.8 MPa · 두 판독 일치) · [카드 산술 — 같은 크기 정사면체 가정] | Coarse 만 · 금속

## g — 2D → 3D 경고 · 증거

보강 없음 (3D 만 · 2D 대조 없음).

## h — DEM 에서 FE · MPM 으로 넘긴 선례 (★ 이번 보강의 중심 — 카드 §4.7 · §15.6)

- [h] pycompact2025_dem_mpfem_workflow | **무엇을**: (x, y, z, r) CSV 하나 — *"This file forms the interface between DEM and MPFEM"* (p.2) · Fig 2(a) '.CSV File (x, y, z, r)' · Fig 1 'Initial powder configuration (size, center)' · 파일 position.csv · DEM cm → mm ×10 (`unit_scale`) · 입자 ID 는 VTK 에 있으나 CSV 칸에 없고 FE 쪽 pid · secid = i 로 다시 매김 (Fig 2c) · 접촉 · 겹침 · 속도 · 응력 · 재료 값은 넘어갈 칸이 없음 | 카드 §4.7 (가) · §4.3 | 인쇄 · [카드 추론] | —
- [h] pycompact2025_dem_mpfem_workflow | **언제**: raindrop 삽입 → 중력 침강 뒤 · **가압 전 (P = 0)** (p.2 · Fig 3c 'after DEM settlement') · 그 순간 충전율 · 층 높이 · 겹침 미인쇄 — FE 판독으로 압력이 뜨는 점의 기공 Fine 42.8 · Coarse 42.4 % (충전율 ≈0.57–0.58 · 윗면 요철 틈 포함) | 카드 §4.7 (나) · Fig 4(b) | 인쇄 · [판독] · [미확인] | —
- [h] pycompact2025_dem_mpfem_workflow | **넘긴 뒤 어떻게**: 구마다 사면체 메시 (MeshMatGen.ipynb → LS-PrePost cfile · 평균 2000 요소/입자 · 총 0.81 M (Coarse) / 1.14 M (Fine)) · 면 · part 집합 · material.k (pid = secid = i · mid = 1) · 다이 · 펀치 · 접촉 · 재료 · 경계는 손으로 · **겹친 구 · 틈 · 재평형 · 초기 응력 · FE 중력 처리 문장 없음** · 벌칙 접촉 *"preventing physical overlap"* (p.3) · 'Initial stage' 무응력 색 · 펀치가 층 위에서 출발 (Fig 4a 응력 0 구간 = Fig 4b P≈0 수직 구간) | 카드 §4.7 (다)(라) | 인쇄 · [판독] · [카드 산술] · [미확인] | —
- [h] pycompact2025_dem_mpfem_workflow | **두 풀이 값을 다르게**: DEM Hertz–Mindlin μ 0.5 · μr 0.05 · e 0.7 (E 미인쇄) ↔ FE Coulomb μ 0.2 · E 170 GPa · Swift; 경계 = 강체 금형 완전 구속 + 펀치 지정 운동 → 최고 압력 → 같은 계산에서 제하 (p.5) · 펀치 속도 · 시간 간격 · 질량 스케일링 · 준정적 판정 미인쇄 · *"A peak pressure of 2000 MPa was applied in all simulations"* ↔ 그림 1400–2000 MPa 다섯 점 | 카드 §4.7 (마)(바) | 인쇄 · [미확인] | —
- [h] pycompact2025_dem_mpfem_workflow | **우리와 대조**: 넘김 시점이 우리 **계획** (느슨한 충전부터 한 모델로 · 단계 4–6 · 후보 B = 이 논문의 꼴) 과 같고 우리 **지금** (압밀 끝난 `atom_2060000` 의 AM 골격 + SE 씨앗 → MPM) 과 정반대 · 넘기는 내용 (중심 + 반지름) 은 셋이 같음 · 넘긴 직후의 겹침 · 평형 처리는 이 논문도 비웠다 = 결과 전에 정할 빈칸 | 카드 §15.6 대조 표 · 비교 문서 C 절 ⑦ | [카드 추론] | 우리 쪽 칸 = 카드 · 비교 문서 시점의 서술

## i — 복합 양극 (AM + SE) 의 압력별 기공

보강 없음 (1 상 금속 분말).

## j — 카드가 스스로 적은 한계 (가압 · 탈압과 닿는 것)

- [j] pycompact2025_dem_mpfem_workflow | **새로 더함 — 넘김에서 원문에 없는 것 9**: 넘긴 순간 충전율 · 층 높이 · 겹침 · 침강 정지 판정 / 겹친 구 · 틈 처리 / 재평형 · 초기 응력 · FE 중력 / 펀치 속도 · 시간 간격 · 질량 스케일링 · 감쇠 · 준정적 판정 / DEM 재료 값 / 메시 매개변수 값 / 1400–1800 MPa 점 얻은 방법 / 압력 면적 정의 · 충격량 미분 평활 / 저장소 구성 (원문은 파일 이름만) | 카드 §4.7 끝 [미확인] 목록 | [미확인] | —
- [j] pycompact2025_dem_mpfem_workflow | **새로 더한 원문 내부 불일치**: Fig 3e 2500 점 ≈1379 ↔ 본문 1310 MPa · 9 h 가 두 곳 (Table 1 Fine RVE 210 ↔ p.6 Coarse 2000 요소) 인데 Table 3 의 Coarse 2000 요소는 7 h (24 CPU) · Fig 4(a) 캡션 'Coarse' 만 ↔ 그림 두 곡선 · Table 2 의 ABAQUS 칸 Solver · Friction 빈칸 · '모든 계산 2000 MPa' ↔ 그림 다섯 압력 | 카드 §18 항목 10–13 · §9.1 | 인쇄 · [판독] | —
- [j] pycompact2025_dem_mpfem_workflow | **철회한 카드 판정**: Fig 3e '−5 % 미수렴' · '제하 후 RD 삼각형 5–7 %p' · 'Fine 이 더 성기게 쌓였다' (압력이 뜨는 점 42.8 vs 42.4 % = 판독 오차 안 · 61 % 는 펀치 접촉 전 구간) · 'Fig 4a 제하부 계단' (그림에 없음) · 569 입자 9 h 에 붙인 '24 CPU' (Table 1 에 CPU 수 없음) | 카드 §8 · §9.1 · §10 · §11 · §14 · §18 | — | —

## k — DEM 의 한계 (서지 병기)

- [k] pycompact2025_dem_mpfem_workflow (Mohammadhosseinzadeh · Ghorbani-Menghari · Kim 2026, SoftwareX 33, 102495) | **새로 더한 원문**: *"The DEM captures the initial particle interactions and packing behaviour, while the MPFEM extends traditional FEM to explicitly mesh and simulate the deformation of individual particles [13,14]."* (p.2) · DEM 장점 *"applicability to processes involving flow and initial packing [11]"* (p.2) — 역할 나눔의 한 줄 근거.  (보강 전부터 있던 *"assumptions of rigid or simplified particle shapes that neglect internal deformation"* 의 원문 단 크롭 `txt_p2_dem_fem_limits_and_mpfem_role.png` 신설) | 카드 §5 (f) · p.2 | 인쇄 | 금속 고압 압축 맥락

## l — 소성변형이 왜 어려운가 (서지 병기)

- [l] pycompact2025_dem_mpfem_workflow (Mohammadhosseinzadeh 외 2026, SoftwareX 33, 102495) | **고친 비용 귀속**: 우회 = 입자별 FE · 비용 569 / 874 / 1033 입자 = 9 / 16 / 24 h (Table 1 — CPU 수 미인쇄; 옛 카드의 '24 CPU' 귀속 정정) · Coarse 403 입자 24 CPU 7 h ↔ ABAQUS 5 h (Table 3) · 2500 요소/입자 36 h 는 **Coarse** 메시 시험 (옛 '569 입자' 귀속 정정, p.5–6) | 카드 §11 · §4.7 (자) | 인쇄 | —
- [l] pycompact2025_dem_mpfem_workflow (Mohammadhosseinzadeh 외 2026) | **새로 더한 것 — 탈압의 어려움**: 압분체 되돌아옴 (+11–12 % 부피) 이 재료 탄성 체적 P/K (1.4 %) 의 ≈8 배 → 되돌아옴은 재료가 아니라 접촉이 열리는 데서 온다 (저자 *"elastic recovery primarily at particle peripheries"* p.6) — 입자 형상 소성을 넣은 모형도 접촉 분리를 못 하면 탈압을 놓친다 | 카드 §15.5 | [카드 산술] · [카드 추론] | 금속 · 2000 MPa

## m — 받아들일 통찰 (무엇을 · 우리 쪽 어디에 · 근거)

- [m] pycompact2025_dem_mpfem_workflow | **넘김 계약을 결과 전에 적는다** — 넘기는 칸 (중심 · 반지름 · 상 · 번호) · 넘김 시점 · 겹침/틈 검사 · 출발 응력 · 재평형 여부 · 단위 환산; 이 논문은 칸 (x, y, z, r) 과 시점만 적고 나머지를 비웠다 | 단계 4; 후보 B; 후보 A′ | 카드 §4.7 [미확인] 목록 · §15.6 · §20 P-7
- [m] pycompact2025_dem_mpfem_workflow | **제하 판독 규칙** — 판독 문턱 (그들 5 MPa) 을 결과 전에 정하고 그 민감도를 같이 보고 · 응력 0 꼬리 (판이 떨어진 뒤의 판 이동) 를 압분체 되돌아옴으로 세지 않는다 (그들 Fine 12.1 → 16.9 % 가 0–5 MPa 한 화소 안) | 단계 6; 조건 R4; 결과 전 대조 항목 | 카드 §10 · §9.4
- [m] pycompact2025_dem_mpfem_workflow | **압분체 되돌아옴 ≫ 재료 P/K (≈8 배)** — 우리 MPM 의 K 25.5 GPa 가 맞아도 한 속도장 (붙은 계면) 은 접촉 열림을 못 내 되돌아옴을 과소평가할 것 → 단계 6 의 되돌아옴은 분리 가능한 접촉 (후보 A′) 로 보는 것이 맞다 (가설 — 비교 문서 C 절 '단일 속도장 MPM 은 제하를 원리적으로 과소평가' 와 같은 방향) | 단계 6; 후보 A′; 조건 R2; 조건 R4 | 카드 §15.5 [카드 산술 · 추론]
- [m] pycompact2025_dem_mpfem_workflow | **그림 판독 · 보고 함정** — 압력 축 0 눈금이 틀 왼끝이 아니다 (−204 MPa) · 축선 위로 겹친 꼬리는 색으로만 보인다 · 수렴 그림의 점과 본문 숫자가 어긋날 수 있다 (1379 ↔ 1310) → 외부 값은 눈금 표시 화소로 등록해 두 번 독립 판독하고, 우리 수렴 보고는 마지막 증분을 숫자로 함께 적는다 | 흐름 밖: 문헌 판독 규율 · 결과 전 대조 항목 뽑기; U6 | 카드 §9.5 · §9.4 · §9.1

## n — 논문 에이전트 후보 (litdb 에 카드 없음 · 많아야 다섯)

litdb 확인 = 정본 `litdb/papers/` 파일 목록 + `git grep` (DOI · 제1 저자 성) — 다섯 모두 자기 카드 없음 (Ghorbani · Kahhal 은 이 카드에만 인용으로 등장).

- [n] Ghorbani-Menghari H, Kim HJ, Choi H, Cha PR, Kim JH. Optimizing powder compaction for enhanced relative density: insights from multi-particle finite element simulations and genetic algorithm. Mater Res Proc 2024;41(1):2554–61. https://doi.org/10.21741/9781644903131-281. | h · b · j — 이 논문이 실험 · ABAQUS 참조 모형을 가져온 원전 [15] (카드 §4.7 (아) · Table 2) — 펀치 속도 · 질량 스케일링 · 넘김 설정 등 이 논문이 비운 [미확인] 을 채울 수 있는 자리 | papers/ 에 없음 (DOI · 'Ghorbani' grep = 이 카드뿐)
- [n] Ghorbani-Menghari H, Kim HJ, Choi H, Cha PR, Kim JH. Integrating simulation and experimentation for optimized compaction powder forming: a study on RVE size, friction, and particle size distribution. IOP Conf Ser 2024;1307(1):012023–32. https://doi.org/10.1088/1757-899X/1307/1/012023. | h · f — RVE 크기 · 마찰 · PSD 민감도의 원전 [16] (카드 §9.2 · §9.3) · 실험 RD 값의 출처 | papers/ 에 없음
- [n] Han P, An X, Zhang Y, Huang F, Yang T, Fu H, Yang X, Zou Z. Particulate scale MPFEM modeling on compaction of Fe and Al composite powders. Powder Technol 2017;314(1):69–77. https://doi.org/10.1016/j.powtec.2016.11.021. | d · i · h — 두 금속 (Fe 단단 · Al 무름) 복합 분말의 입자별 FE 압축 = 단단한 입자의 하중 몫 · 복합 기공 (카드 §5 (f) 의 [13,14] 인용 자리) | papers/ 에 없음 (DOI grep 0)
- [n] Huang F, An X, Zhang Y, Yu AB. Multi-particle FEM simulation of 2D compaction on binary Al/SiC composite powders. Powder Technol 2017;314(1):39–48. https://doi.org/10.1016/j.powtec.2017.03.017. | d · g — 무른 Al + 단단한 SiC 이분 혼합의 2D 입자별 FE (하중 몫 · 2D 결과) · 편차 문헌 밴드 [8] (카드 §3.3 '0.5–4 %') | papers/ 에 없음 (DOI grep 0)
- [n] Wang W, Zhao Y, Weng M, Dong K, Qi H, Wang W, Li C. DEM-FEM simulation of double compaction of Cu and Al composite metal powders with multiple particle sizes. Crystals 2025;15(6):526–42. https://doi.org/10.3390/cryst15060526. | h · d · i — DEM → FE 넘김의 또 다른 선례 (복합 · 다입도) · FEM 한계 인용 [10] (카드 §5 (c)) | papers/ 에 없음 (DOI grep 0)

## 카드 문제

- 고친 것 (보강 전 카드의 문제 — 이번 커밋에서 정정, 원문 위치 병기): ① Fig 3e 판독 · '−5 % 미수렴' (§9.1 · Fig 3e p.5 · p.6) ② Fig 4a '잔류 ε' 판독 · '제하 RD 삼각형 5–7 %p' (§9.4 · §10 · Fig 4a/4b p.7) ③ Fig 4b 가압 가지 500/1000/1500 MPa 값 (§9.5) ④ 'Fine 이 더 성기게 쌓였다' (§8) ⑤ σ_y 590.6 · '포화유동응력' (§3.1) ⑥ 탄성 체적 P/E ↔ P/K 혼용 (§14 · §15.5 · 비교 문서 F 절) ⑦ 36 h 메시 시험을 Fine 569 입자에 붙임 (§11 · p.5–6) ⑧ 569 입자 9 h 에 '24 CPU' (§11 · §15 · 비교 문서 C 절 ⑤ · Table 1) ⑨ RVE '정육면체' (§3.2 · Fig 3c) ⑩ 'J2형' (§7.3 · p.3) ⑪ 'Fig 4a 제하부 계단' (§14) ⑫ Minnmann 앵커에 CL-94 표지 없음 (§10 · §15.1 · §15.5 · §20 · 비교 문서 F 절).
- 남은 것: ① §15.3 의 목록 속 표 (들여 쓴 표 · 검사기 '고아 행' 5) 는 손대지 않았다 — 렌더 확인 [미확인] ② '우리 지금' 칸 (제하 '안 푼다' 등) 은 카드 · 비교 문서 시점 서술 — 지금 상태는 정본 밖 문서로 확인해야 한다 ③ Fig 4e/f 라벨 120 µm ↔ 너비 비로 잰 높이 ≈96 µm (Fine) — 단면이 RVE 전폭인지 [미확인] (§9.6).
