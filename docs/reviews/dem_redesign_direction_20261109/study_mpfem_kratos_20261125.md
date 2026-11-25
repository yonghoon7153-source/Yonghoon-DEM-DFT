# [DEM 우선 (수영)] 다음 모델 공부 — MPFEM · Kratos (2026-11-25)

> **개발 자료 · 공부 메모 · 새 계산 0** · 설치 0 · 리포 쓰기 0 · 커밋 0
> 요청: 1저자 11-25 *"3D 다중 MPM 은 내꺼고 MPFEM, kratos 도 한번 study 해보자"*.  기준선 = 3D 다중 MPM (우리 코드 · `scripts/mpm3d_compaction.py` 를 입자별 속도장으로 넓히는 길 · 지금 보류).  바깥 공부 = MPFEM · Kratos.
> 표지: **[본 것]** = 쪽 · 초록 · README · 소스를 직접 엶 · **[초록]** = Crossref 초록을 직접 읽음 (본문 안 엶) · **[요약만]** = 웹 검색 요약만 (원문 안 엶) · **[서지]** = Crossref 로 제목 · 권호 · DOI 만 확인 · **[카드]** = litdb 정본 카드 (`origin/claude/friendly-meitner-lldvar` 끝 `88d81a298`) · **[코드 판독]** = 소스 파일을 열거나 있는지만 봄 · [우리 산술] · [추정] · [미확인].
> 주의: 원고 · 발표에 쓰기 전에는 원문 PDF 로 만든 litdb 카드가 먼저다 (CLAUDE.md 규율 ⑥).  이 메모의 [초록] · [요약만] · [서지] 값은 인용하지 않는다.
> ✅ **1저자 11-25 §5 Q1–Q7 = 권고대로** — Q1 2D 49 원판 MPFEM 대조 연다 (결과 전 등록부터) · Q2 Kratos 원판 하나 시험 (J26 push 뒤 · 개발 자료 · 큰 변형 평면 변형 소성이 안 되면 MOOSE) · Q3 닿으면 붙임 팔 ('S 와 같은 것 아님' 표지 · 판정은 마찰 팔 압력) · Q4 3D 생산 도구 아님 · Q5 메모 3.2 의 OpenRadioss → OpenCourant (다음 개정) · Q6 MPM–DEM 뺌 · Q7 네 편 PDF = 1저자 (제목 · 권호 = Crossref [서지] · 본문 미열람).  OpenRadioss 원 저장소 = git 으로 안 열림 · OpenCourant · PyCompact 는 열림 (본 세션 11-25 확인).

---

## 0. 한눈에

1. **MPFEM** = 입자마다 유한요소 메시 + 입자 사이 접촉.  SE 형상 변형 · 입자 미끄럼 · 분리 · 탈압 되튐을 한 이산화로 갖는다.  우리 MPM (한 속도장 · 명시 접촉 없음) 에도, 우리 DEM (구 모양 그대로) 에도 없는 조합이다 [카드: `pycompact2025_dem_mpfem_workflow` §15.3].
2. 대가는 **규모**다.  3D 선례는 수백 ~ 2,000 입자다 (Demirtas 411–1979 · 60 h 미만 / PyCompact 403–1033 · 7–24 h · CPU 수는 7 h 런에만 24 로 인쇄) [카드].  우리 real_14 침대 (SE 32,832) 에 그대로 쓰면 약 1 년 (24 CPU) 이다 [카드 산술: PyCompact §11].
3. 전고체 · 황화물 SE 압밀에 MPFEM 을 쓴 예는 **못 찾았다** (웹 검색 3 회 + litdb 정본 낱말 검색).  없다는 증명은 아니다.
4. 주의: **OpenRadioss 원 저장소가 없어졌다** (`github.com/OpenRadioss/OpenRadioss` = 404 · 11-25 [본 것]).  공동체 이어받기 = **OpenCourant** (AGPL v3 [본 것]).  메모 3.2 의 "FE 길 = LMGC90 · OpenRadioss" 와 PyCompact (OpenRadioss r2024 고정) 는 이 점을 고쳐 읽어야 한다.
5. **Kratos** = BSD · Python · pip 바퀴 (10.4.4 · 2026-09-28) [본 것].  우리에게 쓸 만한 것은 셋이다.  ① FEM + mortar 접촉 (MPFEM 꼴) ② MPM (한 속도장 · 우리 S 와 같은 부류) ③ MPM–DEM 분할 결합 (강체 구 + 연속체 · 메모 3.2 후보 A 와 같은 꼴로 읽음 [추정]).  GPU 언급이 없고, 분말 압축 예도 못 찾았다.
6. **권고**: 둘 다 3D 생산 도구는 아니다.  값싼 쓰임은 하나다.  2D 49 원판 (Q13 과 같은 질문) 을 몸에 맞춘 메시로 한 번 풀어, Q13 에서 남은 **아래판 압력 격자 오차** (같은 변위에서 12↔24 칸 S 18.24 % · F 19.25 %) 의 바깥 기준을 만든다 (§4).

---

## 1. MPFEM (다입자 유한요소)

### 1-1. 방법의 요점

- **무엇**: 입자마다 연속체 메시 (2D 삼각형 · 사각형 / 3D 사면체 · 육면체) 를 두고, 입자 사이는 FE 접촉 조건으로 잇는다.  출발 충전은 DEM 으로 만든다.  PyCompact 는 LIGGGHTS 중력 침강 **직후 (압축 전 · P ≈ 0)** 의 (x, y, z, r) CSV 를 입자별 사면체 메시로 바꾼다 [카드 §4.2–4.3].  Zhou 2019 · Li 2022 도 DEM 충전을 입력으로 쓴다 [초록].
- **접촉 세 꼴**
  ① 명시 동역학 + 벌점 일반 접촉 + Coulomb µ: Abaqus/Explicit general contact (Demirtas · µ 0.1) · OpenRadioss `/TYPE26` (PyCompact · µ 0.2) [카드].
  ② 비평활 접촉 동역학 (NSCD): Signorini 비관통 + Coulomb · 비선형 Gauss–Seidel · 접촉 강성 없음 · LMGC90 (Cantor 2020 · Cárdenas-Barrantes 묶음) [카드].
  ③ 암시적 mortar · 증강 라그랑주 (MOOSE · Kratos 접촉 응용 · §1-3 · §2).  분말 압축 선례는 이번에 못 찾았다.
- **준정적 처리 (명시)**: 밀도를 인위로 올려 (mass scaling) 시간 간격을 키운다.  판정은 운동 / 위치 에너지 비 < 1 % (RD ≥ 0.6 구간) 다 [카드: Demirtas §4-5].  PyCompact 는 펀치 속도 · 질량 키움을 적지 않았다 [카드 §7.2].  명시 FE 의 시간 간격은 가장 작고 단단한 요소가 정한다 (Demirtas 식 1 [카드]).  그래서 AM (E 100 GPa 대) 을 탄성 메시로 넣으면 SE 만일 때보다 시간 간격이 준다 [추정].
- **메시 뒤틀림 · 다시 메시**: 3D 선례 둘 (Demirtas RD 0.9 · PyCompact PEEQ 1.3) 다 다시 메시를 적지 않았다 [카드].  납 구 Abaqus 연구는 다시 메시로 RD 0.97 에 닿았고 "결과에 큰 영향 없음" 이라 적었다 [요약만].  Bardenhagen 2005: *"Lagrangian meshes become too distorted"* · *"identification a priori of candidate contact surfaces"* [카드 · litdb 비교 문서].  Kratos 는 MMG 다시 메시 예제가 있다 (§2-3).
- **해상도**: 응력은 메시에 둔감하지만 **접촉 면적은 입자당 3,363 요소에서도 수렴하지 않았다** (Demirtas Fig 5) [카드 §4-6].  요소가 클수록 상대밀도가 낮다 (Ghorbani-Menghari 2024) [초록].  PyCompact 는 2,000 → 2,500 요소/입자에서 9 → 36 h 다 [카드].
- **탈압 되튐**: PyCompact 압분체 부피는 2000 MPa → 5 MPa 에서 +11–12 % 다.  재료 P/K 의 약 8 배이고, 주역은 접촉이 열리고 입자 둘레가 풀리는 것이다 [카드 §15.5 · 카드 추론].  Demirtas 는 얇은 껍질일수록 되튐 거리가 크다 [카드].  Zhou 2019 (2D 구리) · Li 2022 (3D 무른 + 단단) 는 탈압 뒤 잔류 응력이 접촉 · 모서리에 남는다고 적는다 [초록].
- **단단한 + 무른 혼합 (AM + SE 의 짝)**: Huang 2017 (2D Al/SiC) — 힘사슬은 SiC (단단) 끼리가 정한다 [요약만].  Wang 2025 (Cu–Al 쌍봉) — Cu 에 힘사슬, Al 이 오목하게 흘러 틈을 채운다 [초록].  CB20 (2D 강체 + 초탄성 1,500) [카드].

### 1-2. 분말 압축 대표 결과

| 논문 | 차원 | 입자 수 | 재료 | 도구 · 접촉 | 탈압 | 표지 |
|---|---|---|---|---|---|---|
| Zavaliangos 2002 MRS Proc 731 | 2D | 400 | [미확인] | [미확인] | [미확인] | [요약만] · [서지] |
| Procopio & Zavaliangos 2005 JMPS 53:1523 | 2D 단분산 | [미확인] | [미확인] | MPFEM.  응답이 DEM (Redanz–Fleck) 보다 무르고, 재배열 · 회전이 크다 | [미확인] | [요약만] · [서지] |
| Ransing 2000 Mater Des 21:263 · Gethin et al. MSMSE 11:101 · Frenning 2008 CMAME 197:4266 | — | — | — | 초기 이산 변형 요소 · FE/DE 결합 선례 | — | [서지] 만 |
| Cantor 2020 PRL 124:208003 | 2D | 1,500 × 삼각형 92 | neo-Hookean 비압축 | LMGC90 NSCD · µ 0–0.8 | 없음 | [카드] |
| Cárdenas-Barrantes 2020 PRE | 2D | 1,500 | 강체 + neo-Hookean | LMGC90 NSCD | 없음 | [카드] |
| Cárdenas-Barrantes 2022 Soft Matter | 3D | 50 · 100 × 사면체 808 | 탄성 ν 0.495 | LMGC90 NSCD · µ 0.3 | 없음 | [카드] |
| Huang 2017 PT 314:39 | 2D | [미확인] | Al (무름) + SiC (단단) | [미확인] | [미확인] | [요약만] · [서지] |
| Zhou 2019 MPE 5269302 | 2D | [미확인] | 구리 | DEM 충전 → FEM | 있음 | [초록] |
| Demirtas 2021 PT 391:34 | 3D | 411–1979 | 완전 탄소성 E/σ_y 100 (중공 구) | Abaqus/Explicit C3D8R 약 1,650/입자 · µ 0.1 | 있음 (되튐) | [카드] |
| Li 2022 MPE 8580849 | 3D | [미확인] | 무른 + 단단 | DEM 충전 → MPFEM · 실험 대조 | 있음 | [초록] |
| Ku 2023 PT 421:118455 | [미확인] | [미확인] | 결합력 있는 고변형 분말 | 입자 FE + 결합 접촉 | 있음 | [요약만] · [서지] |
| PyCompact 2026 SoftwareX 33:102495 | 3D | 403–1033 | Swift 경화 금속 | OpenRadioss r2024 TETRA4 2,000/입자 · TYPE26 µ 0.2 | 있음 | [카드] |
| Wang 2025 AIP Adv 15:095036 | [미확인] | [미확인] | Cu–Al 쌍봉 (크기비 1:2–1:5) | 명시 MPFEM | [미확인] | [초록] |
| Yuan 2026 Sci Rep 16:27547 | 3D | [미확인] | Al–Fe–Cr–Ti (고속 압축) | 3D MPFEM · µ 0.25–0.65 | [미확인] | [초록] |

### 1-3. 오픈소스 구현

| 도구 | 라이선스 | 접촉 | 유한 변형 소성 | 병렬 · GPU | 유지 상태 | 분말 선례 | 표지 |
|---|---|---|---|---|---|---|---|
| **OpenCourant** (= OpenRadioss 이어받기) | AGPL-3.0 | 명시 · 벌점 일반 접촉 (PyCompact 는 TYPE26) | 조각 선형 소성 (PyCompact) | SMP · MPI · GPU 언급 없음 | 원 저장소 404.  이어받기 5,192 커밋 · 별 453 · Linux (x86-64 · arm64) · Windows 꾸러미 | PyCompact (3D · 403–1033) | [본 것] README · 404.  내린 경위 (Siemens · 2026-10) = [요약만] |
| ↳ PyCompact 흐름 | MIT | — | — | — | 6 커밋 · OpenRadioss r2024 · Windows | LIGGGHTS → 입자별 메시 → Radioss | [본 것] · [카드] |
| **MOOSE** | LGPL-2.1 | node/face (무마찰 · 마찰 · glued) · 벌점 · 접선 벌점 · 증강 라그랑주 · mortar (Coulomb 포함) · 여러 짝 + 중심 거리 자동 짝 (mortar 는 여러 짝 미지원) · 명시 동역학 접촉 · 강체 표면 메시 | `IsotropicPlasticityStressUpdate` · `ComputeFiniteStrain` · `ComputePlaneFiniteStrain` 파일 있음 | MPI (*"largest runs >100,000 CPU cores"*) · GPU 언급 없음 | 68,806 커밋 (next) · 별 2.4k | 못 찾음 | [본 것] 문서 · 소스 · [코드 판독] 파일 존재 |
| **LMGC90** | CeCILL (GPL 상당) | NSCD · 강체 · 변형체 · 2D/3D | [미확인] (선례는 전부 탄성) | [미확인] | PyPI 에 `pylmgc90` · `lmgc90` 없음 · 저장소는 연구소 git (허용 목록 밖) | 원판 · 구 압밀 다수 (탄성) | [요약만] · [카드] · PyPI [본 것] |
| **Kratos** FEM + 접촉 | BSD-4-Clause | mortar ALM · 벌점 (암시적 · 명시) · MPC · 자기 접촉 (주/종 자동) · KD-tree/octree + 동적 탐색 · 마찰 법칙 *"WIP (Coulomb wired)"* | 작은 변형 J2 (평면 변형 2D · 3D) · 유한 변형 일반 소성 (3D · 평면 응력) · 유한 변형 평면 변형 [미확인] | OpenMP (pip) · MPI = 소스 빌드 · GPU 언급 없음 | 112,415 커밋 · 별 1.4k · 10.4.4 (2026-09-28) | 못 찾음 | [본 것] · [코드 판독] |
| **FEBio** | MIT | `FESlidingInterface` · `FESlidingElasticInterface` · `FEFacet2FacetSliding` · `FEContactPotential` 파일 있음 | `FEReactivePlasticity` 파일 있음 | [미확인] | 8,536 커밋 · 생체역학용 | 못 찾음 | [본 것] · [코드 판독] |
| **Code_Aster** | GPL (2001 부터) | Signorini + Coulomb (`DEFI_CONTACT`) | [미확인] | MUMPS · PETSc MPI (옛 설명서) | 최신 안정판 17.4 | 못 찾음 | [요약만] |
| Akantu (더 볼 후보) | LGPLv3 | [미확인] | [미확인] | [미확인] | PyPI 5.0.7.post1 (2024-09) · 바퀴 6.6 MB | — | PyPI [본 것] |

### 1-4. 전고체 · 황화물 SE 에 쓴 예

- 못 찾았다.  웹 검색 3 회 (표준 2 · 확장 1) 와 litdb 정본 낱말 검색 (`mpfem` · `multi-particle finite`) 을 했다.  나온 카드는 금속 · 제약 · 탄성 원판뿐이다.
- 가까운 것: 코팅 입자 냉간 압축 DEM (JPS 2022) [요약만] · 완전 치밀을 가정한 연속체 RVE (MOOSE) [요약만] · Shi 2026 (아지로다이트 점소성 Abaqus · 공극 접촉 FEM · 다입자 압축 아님) [카드 `shi2026_argyrodite_stack_pressure_viscoplastic_deformation`].
- MPFEM 압분체로 전도도를 계산한 예도 못 찾았다 (검색 1 회 · 열전도 비슷한 예만 [요약만]).  PyCompact 카드도 "MPFEM 이면 변형 접촉 면적 위에서 Holm 저항을 바로 계산할 수 있다 — 이 논문은 하지 않았다" 고 적는다 [카드 §15.3].

---

## 2. Kratos Multiphysics

### 2-1. 응용 묶음 (GitHub `applications/` 60 개 중 관련 [본 것])

- **DEMApplication**: 구 · 덩어리 · 선형 / Hertz / JKR / DMT 접촉 · 결합 (continuum) 입자 · FEM 벽과의 상호작용 [본 것 README].
- **MPMApplication** (PyPI 에서 `ParticleMechanics` 가 9.4.6 에서 멈추고 10.x 는 `MPM` — 이름이 바뀐 것으로 읽음 [본 것 · 추정]): 갱신 라그랑주 · 암시적 (Newmark/Bossak · 정적 · 준정적 · 동적) · 명시 · 혼합 u–p.  재료 = 선형 탄성 · neo-Hookean · Mohr–Coulomb (유한 변형 · 평면 변형) · 연화 MC · 수정 Cam-Clay · Johnson–Cook 열소성 (명시만).  격자 경계 (미끄럼 · 무미끄럼) · 물질점 경계 (벌점 · 라그랑주 승수) · FEM · DEM · 강체와 분할 결합.  **입자끼리 접촉 · 다물체 언급 없음** [본 것 README].  소스에 `hencky_mc_plane_strain_2D_law` · `johnson_cook_thermal_plastic_plane_strain_2D_law` 가 있다 [코드 판독].
- **StructuralMechanics + ContactStructuralMechanics + ConstitutiveLaws**: §1-3 표의 Kratos 줄.  접촉 결과로 `AUGMENTED_NORMAL_CONTACT_PRESSURE` 등을 출력한다 [본 것 README].
- **CoSimulation**: `dem_wrapper.py` · `mpm_dirichlet_wrapper.py` · `mpm_neumann_wrapper.py` · `structural_mechanics_wrapper.py` [본 것 파일 이름].
- **MPM–DEM**: Singer et al. 2022 (AMSES 9:16) — 분할 · 블랙박스 · 공유 경계로 통신 · 산사태 흐름이 바위와 장애물에 부딪히는 문제 [초록].  DEM 을 먼저 풀고 힘을 MPM 외력으로 넘긴 뒤 MPM 경계 운동을 DEM 에 돌려주는 약한 결합이다 [요약만].
- 이름만 본 것: DemStructuresCoupling · FemToDem (깨지면 DEM 으로) · PfemSolidMechanics · ContactMechanics · DelaunayMeshing · SPH (기능 미확인).

### 2-2. 라이선스 · Python · 설치 · GPU

- 라이선스 BSD-4-Clause (PyPI) · GitHub README *"BSD"* [본 것].
- PyPI `KratosMultiphysics` 10.4.4 (2026-09-28) · Python ≥ 3.8 (cp38–cp314) · manylinux glibc 2.28+ x86-64 · Windows · 코어 바퀴 34.8 MB [본 것].
- 응용 바퀴 (cp310 Linux): DEM 4.9 · MPM 4.0 (+ LinearSolvers 3.0) · Structural 9.7 · ContactStructural 17.2 · ConstitutiveLaws 8.3 · CoSimulation 2.8 · Mapping 2.7 MB [본 것].  우리가 쓸 묶음은 받기만 약 87 MB 다 [우리 산술 · 풀면 더 큼].  FemToDem 은 10.2.3 (2025-06) 에서 멈췄다 [본 것].
- MPI: 설치 문서가 *"advanced configuration"* (소스 빌드 + Trilinos) 이라 적는다.  PyPI 에 Trilinos 응용이 없다 [본 것].  그래서 pip 바퀴는 공유 메모리 (OpenMP) 로 읽힌다 [추정].
- GPU: 설치 문서에 CUDA · GPU 가 0 회 나온다 [본 것].

### 2-3. 분말 압축 · 입자 변형 예

- Kratos `Examples` 저장소에 `mmg_remeshing_examples` · `parmmg_remeshing_examples` 폴더가 있고, 접촉 응용 README 는 다시 메시용으로 MeshingApplication 을 든다 [본 것].
- 같은 저장소의 README 에 compaction · powder · tablet 이 없다.  가까운 것은 "Ironing with die" (접촉) 와 "Granular Flow 2D" (MPM) 뿐이다 [본 것].  웹 검색 1 회에서도 Kratos 분말 압축 선례를 못 찾았다.
- litdb 에 Kratos 카드가 없다.  낱말 'Kratos' 는 XPS 장비 이름과 CIMNE 소속 표기에만 나온다 (`giannis2021_stress_based_multicontact_dem` 42 행) [카드].

---

## 3. 우리 기준으로 견주기

● 됨 · ◐ 부분 · ○ 안 됨 · ? 미확인.  기준선 줄은 리포 기록 (CLAUDE.md MPM 절 · 수영 메모 3.2 · Q13 반환) 만으로 채웠다.

| 길 | 가압 → 탈압 | SE 형상 변형 | AM 강체 / 탄성 | 접촉망 판독 | 3D 수백 ~ 수천 입자 | 우리 기계 (GPU 24–48 GB · CPU 60 · WSL) | LIGGGHTS 침대 출발 | 배우는 비용 |
|---|---|---|---|---|---|---|---|---|
| **기준선: 3D 다중 MPM (우리 코드 · 보류)** | ◐ 지금은 가압 + 판 고정 이완.  입자별 장이면 ● (U3 · U4 뒤) | ● J2 소성 형상 변형 (SEM 대조는 2D 챔피언) | ◐ 지금 AM = 얼린 장애물 (속도 0 · 하중 0 → 목표까지 누르면 과압축 · R1).  움직이는 AM = 새 코드 | ○ 명시 접촉망 없음 (근접 coverage · 복셀 σ = CONTACT_FREE 가지) | ◐ real_14 (SE 32,832 + AM 457) 를 한 속도장으로는 돌렸다.  입자별 장은 48 GB 카드에 담기는 장 수가 435 격자 약 11 (붓기 높이) · 7 (0.35 높이) / 384 격자 약 17 · 12 [메모 3.2 우리 산술] — 필요한 장 수 K 는 아직 안 셈 (단계 1) | ● GPU (Taichi).  real_14 (두께 약 30 µm) 는 384 격자로 돌았다 · 두께 100 µm 급 침대는 384 에서 약 35 GB 가 든다 | ● `--se-dump` · `--am-scaffold` · 무작위 0.35 출발 | 새 도구 0.  3D A 1–2 주 · A′ 2–4 주 더 [메모 추정] · 3D 성능 근거 0 |
| MPFEM · OpenCourant (+ PyCompact) | ● | ● | ◐ 탄성 메시 (선례는 단일 재료 · 강체 = 다이) | ◐ 접촉 면 · 힘을 직접 (전달 계산 선례 0) | ◐ 403–1033 · 7–24 h (CPU 수는 7 h 런만 24 로 인쇄).  real_14 = 약 1 년 [카드 산술] | ◐ CPU SMP · MPI.  GPU 안 씀 | ● PyCompact 그대로 (Windows 노트북 · r2024 고정 · 압축 전 상태) | 중.  상류가 사라진 위험 |
| MPFEM · MOOSE | ● [추정 · 문서] | ● 평면 · 유한 변형 J2 파일 있음 | ◐ 탄성 메시 · 강체 표면은 정한 운동만 | ◐ 접촉 압력 · 짝 [추정] | ? 선례 못 찾음 | ◐ CPU MPI | ◐ 좌표 → 메시 변환기를 우리가 짠다 [추정] | 높음 (C++ 틀 · conda · 입력 문법) |
| MPFEM · LMGC90 (NSCD) | ◐ 선례는 가압만 | ? 소성 미확인 | ● 강체 + 무른 혼합 선례 (2D) | ◐ 접촉 단위로 푼다 [추정] | ◐ 3D 50 · 100 구 | ? | ◐ Python 전처리 [요약만] | 중–높음 (PyPI 없음 · 소성 확인 먼저) |
| Kratos FEM + mortar 접촉 | ● [추정 · README] | ◐ 작은 변형 J2 평면 변형.  유한 변형 평면 변형 ? | ◐ 탄성 메시 [추정] | ◐ 접촉 압력 출력 → 쌍별 면적은 후처리 [추정] | ? 다물체 분말 선례 없음 | ◐ CPU OpenMP.  MPI 는 소스 빌드 | ◐ `.mdpa` 변환을 짠다 [추정] | 중 (pip 쉬움 · 문서가 흩어짐) |
| Kratos MPM (한 속도장) | ◐ 입자끼리 미끄럼 · 분리 없음 (우리 S 와 같은 부류) | ● (Hencky–MC · JC 명시) | ◐ MPM–DEM 결합일 때 강체 구 | ○ | ? | ◐ CPU | ◐ 몸 메시 → 물질점 [추정] | 중 |
| Kratos MPM–DEM 결합 | ? 고압 준정적 선례 없음 | ● (MPM 쪽) | ● DEM 강체 구 (AM–AM 은 DEM 이 푼다) [추정] | ◐ AM–AM (DEM) 만 | ? 선례 = 산사태 · 장애물 | ◐ CPU | ◐ DEM 쪽은 구 좌표 [추정] | 중–높음 (CoSimulation 설정) |
| (참고) Kratos DEM | ● [추정] | ○ 구 그대로 | ● | ● (DEM 접촉) | ● [추정] | ◐ CPU | ◐ 구 좌표 변환 [추정] | 중.  우리 D0 (LIGGGHTS) 와 같은 부류라 새 정보가 적다 |

**기준선 줄 근거**: AM 얼림 · 하중 0 · R1 과압축 = CLAUDE.md DO-NOT 블록 (`fam_platen_prereg_20260812.md` §11) · 명시 접촉망 없음 · 복셀 σ 지위 = CLAUDE.md frame [1] · CL-81 절 · 384 메모리 = CLAUDE.md "격자 판정" ① · 입자별 장 K = 메모 3.2 §4 단계 1 판정 (우리 산술) · 개발 어림 = 메모 3.2 §3-3 A′ 줄 · 개발 어림 절 · 조건 표 = 메모 3.2 §3-3 · 2D S/F = Q13 반환 (`docs/reviews/suyoung_q13_return_20261125/README.md` · 가지 `codex/suyoung-q13-return-1125` · `f0519d86f`).

**표에서 읽는 것**
- R6 (SE 형상) · R2 (미끄럼 · 분리) · R4 (탈압) 를 한꺼번에 갖춘 길은 MPFEM 뿐이다.  우리 기준선은 입자별 장 (A′) 을 다 짜야 같은 칸에 닿는다.
- 3D 수백 ~ 수천 입자는 MPFEM 선례의 위 끝이다.  실제 입경비 (real_14: AM_P 반경 6 µm · SE 0.5 µm) 로 2,000 입자 상자를 만들면 PC 가 약 2.6 개라 대표성이 없다 (메모 3.2 §3-3 B · 사전 공격 1 부록 A · 우리 산술).  그래서 MPFEM 은 3D 에서 "작은 상자 검산" 자리다.
- Kratos 는 FEM 접촉 · MPM · DEM 이 한 도구 · 한 설치 (pip) 에 있다는 것이 장점이다.  어느 칸에서도 우리 기준선보다 앞선 실증이 없다.

---

## 4. 시험 설계 초안 — 2D 49 원판 (실행 없음 · 1저자 GO 뒤)

### 4-1. 고정 (리포 등록 그대로)

- 배치 = 7 × 7 정사각 · 같은 지름 원판 49 개 · 시작 Φ_m 0.78 (`docs/reviews/suyoung_u6_first_development_20261118/README.md`).
- 재료 = E 10 MPa · ν 0.45 · 단축 항복 0.4 MPa (경화 0) · 위판 속도 0.034 c_S · F 마찰 µ 0.5 (같은 README).  식의 꼴 = fixed-corotated 응력 + 면내 두 주로그변형률의 편차로 하는 반환 (문턱 = 항복 / (2µ)) [코드 판독: `scripts/dem_suyoung_sf2d_dev.py` `stress()` · `plastic_project()`].
- 경계 = 옆벽 · 바닥 = 무마찰 강체 (벗어나는 수직 속도만 0) · 위판 = 한쪽 접촉 [코드 판독: `scripts/suyoung_u6_first_dev.py` `walls()`].  2D 식은 면내 두 성분만 쓴다 — 평면 변형 J2 와 같은 것은 등적 변형일 때뿐이다 [우리 산술] (4-5).
- 판독 = 아래판 압력 (MPM 은 충격량 / (dt · 폭)) · Φ_m = ΣA₀ / (폭 · 높이) · 목표 Φ_m 0.84 · 0.90 (필수) · 0.95 (보조) · 1.2 MPa 도달.
- MPM 답 (36 칸 · Q13 반환): S 0.262294 · 0.431529 · 0.617308 MPa / F 0.258217 · 0.429284 · 0.614044 MPa.  S/F 구간 0.90 = 0.835296–1.196974 · 0.95 = 0.828541–1.197032 · 0.84 = 미확정.  같은 변위의 압력 격자 차이 8↔16 = S 78.10 % · F 79.25 % · 12↔24 = S 18.24 % · F 19.25 %.

### 4-2. MPFEM 팔

| 팔 | 접촉 | MPM 쪽 짝 | 보는 것 |
|---|---|---|---|
| FE-F | Coulomb µ 0.5 · 분리 허용 | F 의 h → 0 짝 | 메시 수렴 구간 안의 압력 P(Φ_m) |
| FE-G | 닿으면 붙임 (glued · 미끄럼 · 분리 없음) | S 의 이상 극한 후보 [추정 · 같은 것이 아니다] | FE-G / FE-F 압력비 |
| FE-F0 | µ 0 | 한계 대조 | 마찰 몫 |
| (선택) 탈압 | FE-F 를 0 까지 뺌 | 아직 없음 (R4) | 되튐 Φ_m · 접촉 열림 |

### 4-3. 순서

0. 결과 전 등록: Φ_m 정의 · 판독 · 메시 사다리 · 허용폭 · 재료식 차이 표지 · 판정 문장.
1. **원판 하나 시험** (메모 3.2 U1 꼴 · 상자 속 원판 하나 압축): MPM (fixed-corotated 응력 + 로그 변형률 반환 [코드 판독]) 과 FE J2 의 같은 φ_p 압력 차를 먼저 잰다.  49 원판 차이에서 재료식 몫을 뗀다.
2. **49 원판 FE**: 메시 사다리 (원판 지름당 요소 약 16 · 32 · 64 [제안]) × 팔 셋.  명시라면 판 속도를 0.034 c_S 와 그 절반으로 둘 다 돌린다.  암시적이라면 준정적 하나로 한다.
3. **비교**: (a) FE-F 압력 수렴 구간 ↔ MPM S36 · F36 = MPM 아래판 판독의 격자 치우침 크기.  (b) FE-G / FE-F 가 1 을 벗어나면 "MPM 격자 오차가 S/F 차이를 가렸다" 가 후보다.  1 근처면 "이 배치는 원래 차이가 작다" 가 후보다.  (c) 접촉 길이 · 원판 원형도 · 되튐은 보고만 한다.
4. (선택) **Kratos MPM 으로 S 팔 독립 구현**: 지름당 12 · 16 · 24 · 36 칸.  아래판 압력의 격자 민감도가 우리 코드만의 것인지 본다.  Kratos MPM 에는 순수 J2 암시적 재료가 없다.  Mohr–Coulomb φ = 0 을 쓰면 Tresca 꼴이라 재료식 차이가 하나 더 생긴다 [추정].

### 4-4. 비용 [추정]

- FE 2D: 원판 지름당 36–64 요소면 원판당 사각형 약 1,000–3,200 개 × 49 = 5만–16만 요소 [우리 산술].  명시는 같은 해상도의 MPM F36 한 팔 (1 스레드 2 h 51 m) 과 같은 자릿수로 어림한다 (MPM 물질점 = 칸당 4 개 · 사각형 요소 적분점 = 4 개 · 시간 간격 비슷 [우리 산술 · 접촉 탐색 몫 미포함]).  암시적은 수 시간 이내로 어림한다 [추정].
- 원판 하나 시험: 분 단위.
- 사람 시간: 설치 · 입력 · 메시 생성기 · 판독기에 1–2 주.  Kratos (pip) 면 설치가 하루, MOOSE 면 더 든다.
- GPU 0 · CPU 만.  Rint ② R 런 기계와 코어를 나눠 쓰면 된다.
- 3D 로 넓힐 때 (뒤): 순수 SE 100–500 구 작은 상자는 하루 안팎이다 (PyCompact 569 입자 9 h · CB22-3D 50 · 100 구 [카드]).

### 4-5. 한정

- 재료식 꼴이 다르다.  MPM 2D 는 면내 두 성분만으로 편차를 잡는다.  평면 변형 J2 는 zz 성분까지 넣으므로, 부피 변형이 있으면 둘이 갈린다 (등적이면 같다 [우리 산술]).  E/σ_y 25 라 탄성 변형도 작지 않다.  4-3 의 1 단계로 재고, 필요하면 FE 쪽에 같은 2D 식을 사용자 재료로 넣는다 [추정].
- 명시 FE 의 질량 키움 ↔ MPM 판 속도 0.034 c_S 는 재하율 함정과 같은 부류다 (CLAUDE.md 2026-08-06).  판 속도를 맞춘 팔을 반드시 둔다.
- FE-G 는 S 와 같지 않다.  S 는 셀 거리 안에서 붙는다.
- 7 × 7 정사각 배열은 대칭이라 FE 에서도 갈래가 생길 수 있다.  작은 흔들림 시드를 둔다 [제안].
- 이 시험은 검산 (verification) 이다.  값을 MPM 에 맞추지 않는다 (frame [4] · 메모 3.2 §3-2 규칙 4).
- 2D 결과를 3D 로 옮기지 않는다 (CB22-3D · 판정문 DRD-02).

---

## 5. 1저자가 정할 것

| # | 질문 | 권고 |
|---|---|---|
| Q1 | 2D 49 원판 MPFEM 대조를 열까 | 연다.  2D · CPU · 1–2 주로, Q13 에 남은 아래판 압력 격자 오차를 바깥 기준으로 잡는 가장 싼 길이다.  결과 전 등록부터 한다 |
| Q2 | 첫 도구 | Kratos 를 pip 로 깔고 원판 하나 시험부터 한다 (FEM 접촉 + MPM 한 속도장이 한 도구에 있다).  유한 변형 평면 변형 J2 가 서지 않으면 FE 기준은 MOOSE 로 바꾼다 |
| Q3 | S 의 FE 짝 (FE-G) 을 넣을까 | 넣는다.  "S 와 같은 것이 아니다" 표지를 붙이고, 판정은 FE-F 압력 기준값으로만 한다 |
| Q4 | 3D | MPFEM · Kratos 를 3D 생산 도구로 고르지 않는다.  3D 는 기준선 (우리 다중 MPM · Rint ② R 런 뒤) 결정에 맡긴다.  MPFEM 은 3D 작은 상자 검산 (순수 SE 100–500 구) 후보로만 둔다 |
| Q5 | OpenRadioss 표기 | 메모 3.2 · 계획서의 "OpenRadioss" 를 "OpenCourant (OpenRadioss 이어받기 · AGPL v3)" 로 고쳐 적는다 (다음 개정 때 한 줄) |
| Q6 | Kratos MPM–DEM (강체 구 + SE MPM) | 이번 시험에서는 뺀다.  단단한 + 무른 혼합 (3b) 을 볼 때 후보 A 와 견주는 자리로 둔다 |
| Q7 | 새 문헌 카드 | Singer 2022 · Huang 2017 · Li 2022 · Zhou 2019 네 편부터 PDF 를 받아 litdb 카드로 만든다 (PDF 받기는 1저자) |

---

## 6. 확인 못 한 것

- Kratos FEM 에 유한 변형 **평면 변형** 소성이 있는지 · 49 몸 mortar 접촉이 실제로 도는지 · 마찰 법칙 "WIP" 의 뜻.
- Kratos MPM 에서 원판 여러 개를 몸 하나로 묶는 입력 방법 · 아래판 반력 판독.
- MOOSE 설치 크기 · conda 방법 (웹사이트가 허용 목록 밖) · 자동 짝이 압밀 중 새 이웃을 잡는지 (시작 때 중심 거리로 정한다 [코드 판독]).
- LMGC90 의 소성 · 병렬 · 설치.
- OpenCourant 가 PyCompact (r2024 입력) 와 맞는지 · 2D 요소가 있는지.
- FEBio 병렬 · 분말 선례 · Code_Aster 17.x 접촉 병렬.
- 대표 논문의 입자 수 · 도구 (Huang 2017 · Li 2022 · Zhou 2019 · Wang 2025 · Yuan 2026) — 초록에 없다.  Ku 2023 의 방법은 원문이 막혀 못 봤다.
- 전고체 MPFEM 부재는 검색 범위 안의 결과다.
- 막힌 호스트: `jzhao.people.ust.hk` · `amses-journal.springeropen.com` (허용 목록 밖) · `doaj.org` 기사 쪽 (403).  필요하면 세션 네트워크 설정에서 허용해야 한다.

---

## 부록 A. 출처

**litdb 정본 카드** [카드]: `pycompact2025_dem_mpfem_workflow` · `demirtas2021_mpfem_hollow_sphere_die_compaction` · `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` · `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` · `cantor2020_compaction_model_highly_deformable_particles` · `cardenasbarrantes2021_soft_pentagons_compaction_micromechanics_nscd` · `harthong2009_high_density_compaction_dem_voronoi_contact_law` · `clemmer2024_bpm_elastic_grain_compaction_beyond_jamming` · `bardenhagen2005_mpm_foam_densification_simulation` · `shi2026_argyrodite_stack_pressure_viscoplastic_deformation` · `giannis2021_stress_based_multicontact_dem` · 비교 문서 `litdb/comparison_vs_ours_DEM.md`.

**리포 기록**: CLAUDE.md (MPM 절 · DO-NOT 블록 · frame [1] · CL-81 절) · `docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md` (§0 · §3-2 · §3-3 · §4) · `docs/reviews/dem_redesign_direction_20261109/seminar_feedback_20261113.md` · `docs/reviews/suyoung_q13_return_20261125/README.md` (가지 `codex/suyoung-q13-return-1125`) · `docs/reviews/suyoung_q13_setting2_20261125/registration.md` · `docs/reviews/suyoung_stage3_fork_20261125/decision.md` · `docs/reviews/suyoung_u6_first_development_20261118/README.md` · `scripts/suyoung_u6_first_dev.py` · `scripts/dem_suyoung_sf2d_dev.py`.

**[본 것] 쪽 · README · 소스**
- Kratos: https://github.com/KratosMultiphysics/Kratos · `.../tree/master/applications` · README 원문 (raw) — `applications/{DEMApplication,MPMApplication,ContactStructuralMechanicsApplication,ConstitutiveLawsApplication}/README.md` · `INSTALL.md` · 폴더 `ConstitutiveLawsApplication/custom_constitutive/finite_strains/plasticity` · `CoSimulationApplication/python_scripts/solver_wrappers/kratos` · 소스 파일 존재 (`small_strain_j2_plasticity_plane_strain_2d.h` · `generic_finite_strain_isotropic_plasticity.h` · `hencky_mc_plane_strain_2D_law.hpp` · `johnson_cook_thermal_plastic_plane_strain_2D_law.hpp`) · https://github.com/KratosMultiphysics/Examples
- PyPI: https://pypi.org/project/KratosMultiphysics/ 와 JSON (`KratosDEMApplication` · `KratosMPMApplication` · `KratosParticleMechanicsApplication` · `KratosStructuralMechanicsApplication` · `KratosContactStructuralMechanicsApplication` · `KratosDemStructuresCouplingApplication` · `KratosFemToDemApplication` · `KratosCoSimulationApplication` · `KratosConstitutiveLawsApplication` · `KratosLinearSolversApplication` · `KratosMappingApplication` · `KratosMultiphysics-all` · `pylmgc90` (없음) · `lmgc90` (없음) · `akantu`)
- MOOSE: https://github.com/idaholab/moose · raw https://github.com/idaholab/moose/blob/next/modules/contact/doc/content/modules/contact/index.md · https://github.com/idaholab/moose/blob/next/modules/contact/doc/content/syntax/Contact/index.md · https://github.com/idaholab/moose/blob/next/modules/contact/src/actions/ContactAction.C · 파일 존재 (`IsotropicPlasticityStressUpdate.C` · `ComputeFiniteStrain.C` · `ComputePlaneFiniteStrain.C` · `ExplicitDynamicsContactAction.C`)
- FEBio: https://github.com/febiosoftware/FEBio · 파일 존재 (`FEReactivePlasticity.h` · `FESlidingInterface.h` · `FESlidingElasticInterface.h` · `FEFacet2FacetSliding.h` · `FEContactPotential.h`)
- OpenRadioss: https://github.com/OpenRadioss/OpenRadioss (404 · 11-25) · https://github.com/OpenCourant/OpenCourant · https://github.com/plaslab-kimjh/PyCompact

**[초록] (Crossref API 로 초록을 읽음)**
- Singer et al. 2022 · AMSES 9:16 · doi:10.1186/s40323-022-00229-5
- Li et al. 2022 · Math Probl Eng 2022:8580849 · doi:10.1155/2022/8580849
- Zhou et al. 2019 · Math Probl Eng 2019:5269302 · doi:10.1155/2019/5269302
- Wang et al. 2025 · AIP Adv 15:095036 · doi:10.1063/5.0297327
- Yuan et al. 2026 · Sci Rep 16:27547 · doi:10.1038/s41598-026-62634-9
- Wang et al. 2025 · Crystals 15:526 (MSC Marc) · doi:10.3390/cryst15060526
- Ghorbani-Menghari 2024 · Mater Res Proc 41:2554 · doi:10.21741/9781644903131-281

**[서지] (Crossref 로 제목 · 권호 · DOI 만)**
- Procopio & Zavaliangos 2005 · JMPS 53:1523–1551 · doi:10.1016/j.jmps.2005.02.007
- Zavaliangos 2002 · MRS Proc 731 W7.1 · doi:10.1557/proc-731-w7.1
- Ransing et al. 2000 · Mater Des 21:263–269 · doi:10.1016/S0261-3069(99)00081-3
- Gethin, Lewis, Ransing · MSMSE 11:101–114 · doi:10.1088/0965-0393/11/1/308
- Frenning 2008 · CMAME 197:4266–4272 · doi:10.1016/j.cma.2008.05.002
- Huang, An, Zhang, Yu 2017 · Powder Technol 314:39–48 · doi:10.1016/j.powtec.2017.03.017
- Ku, Zhao, Mollon, Zhao 2023 · Powder Technol 421:118455 · doi:10.1016/j.powtec.2023.118455
- Demirtas & Klinzing 2021 · Powder Technol 391:34–45 · doi:10.1016/j.powtec.2021.06.004 (카드 있음)
- Dadvand, Rossi, Oñate 2010 · Arch Comput Methods Eng 17:253–297 · doi:10.1007/s11831-010-9045-2 (Kratos 틀 논문)

**[요약만] (웹 검색 요약 · 원문 안 엶)**
- OpenRadioss 를 내렸다는 보도 · OpenCourant 이어받기: itsfoss.com · phoronix.com · tech.slashdot.org (2026-10)
- LMGC90 라이선스 · 방법: hal.archives-ouvertes.fr (LMGC) · csma2026.sciencesconf.org
- Code_Aster GPL · 17.4: csma2026.sciencesconf.org · 옛 설명서 (ericca.uqtr.ca)
- Procopio & Zavaliangos 2005 내용 · Zavaliangos 2002 (400 입자): researchdiscovery.drexel.edu · cambridge.org
- 납 구 다시 메시 RD 0.97: koreascience.kr
- Huang 2017 내용: research.monash.edu
- Ku 2023 내용: jzhao.people.ust.hk (PDF 는 막힘)
- 전고체 · 황화물 MPFEM 부재 검색 3 회 · MPFEM 전도도 계산 부재 검색 1 회
