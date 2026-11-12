<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-43 · 정독 84) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     가리킨 카드 = benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md (이 논문 = 그 논문 ref [39] · L165 · L450) · 같은 도구를 쓴 이웃 = benhadjali2025 · benhadjali2026 (완전결합 · 한 방향) · zhang2023 · ngandjong2021 카드.
     원문 = 출판본 (ACS Omega 2019, 4, 11141−11144 · Article · 4 쪽 · CC-BY-NC-ND) + Supporting Information (4 쪽 PDF = 표지 S1 + 본문 S2–S4).
     쪽 표기 = 본문 "p.n" = PDF 쪽 n = 인쇄 쪽 11140 + n (p.1 = 11141 … p.4 = 11144) · SI "SI p.n" = SI PDF 쪽 n = 인쇄 "Sn".  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 10 행 — Fig. 3 내장 래스터 (300 dpi) 의 화소를 가장 가까운 세 색으로 나눠 센 단면 면적 몫 · 2D 조각 수 · 방법 = note 열) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug · 줄 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처 · 정본 카드 쪽은 [다른 카드]) · [미확인] = 본문 4 쪽 + SI 4 쪽 전수에 없음.
     원문 8 쪽은 글자 층 (PyMuPDF) 전수 + 전 쪽 렌더 + 내장 래스터로 읽었다.  이 논문은 **메싱 알고리즘 소개**다 — DEM · 입자 계산 · 역학 · 압밀 · PDE 풀이 결과가 없다 (입력 구조 = 같은 그룹 CGMD 가 만든 구 배치). -->
# INNOV — 단층 분할 영상 또는 CGMD 구 (중심 · 반지름 → 이진 영상 묶음) 를 모든 상 한꺼번에 사면체 메시로 바꿔 COMSOL 5.4 로 넘기는 MATLAB 복셀화 메싱 — NMC 전극 예 (AM + CBD + 기공 · 201 × 200 × 179 화소 · precision [4 4 3]) 1 737 665 요소 · 4.48 s (축소 없이 > 48 M 요소 · 177.20 s) · 기공 (porosity) 영상 50.1 % ↔ 메시 49.7 % (매끄럽게 하면 49.69 → 50.07 %) · 상별 부피 오차 < 2 % · AM 표면 CBD 36.2 / 전해질 63.8 % — 구 → 영상 변환 규칙 (겹친 구 · 상 우선 · 화소 크기 µm) 은 원문에 없다 — Chouchane · Rucci · Franco (ACS Omega 2019)

> slug `chouchane2019_innov_voxelization_multiphase_meshing` · DOI `10.1021/acsomega.9b01279` · type `tool — voxelization-based multiphase tetrahedral meshing algorithm (MATLAB INNOV: pixel = node coded by phase · cube from 4+4 nodes of two neighbouring slices split into 5 or 6 tetrahedra · Nielson–Franke separating-surface cases for mixed-phase cubes · Iso2Mesh duplicate-node removal · optional Kroon smoothing · anisotropic "precision" downsampling · scale factor m/pixel) → COMSOL 5.4 Multiphysics native mphtxt + automatic Selections · input = binary image stack from tomography segmentation, sliced 3D object files, or CGMD (LAMMPS) particle centres + radii · observables = image vs mesh porosity, per-phase volume conservation, AM interface coverage · no PDE solved, no DEM / contact / mechanics model` · PDF `3bba10e2-43._A_versatile_and_efficient_voxelization-based_meshing_algorithm_of_multiple_phases.pdf` · SI `b4ad2a77-43._Sup_A_versatile_and_efficient_voxelization-based_meshing_algorithm_of_multiple_phases.pdf` · digested `2026-11-13` · status ✅
>
> **저자**: **Mehdi Chouchane** †‡ · **Alexis Rucci** †‡ · **Alejandro A. Franco\*** †‡§∥ — † Laboratoire de Réactivité et Chimie des Solides (LRCS), UMR CNRS 7314, Université de Picardie Jules Verne, HUB de l'Energie (Amiens) · ‡ Réseau sur le Stockage Electrochimique de l'Energie (RS2E), FR CNRS 3459 · § ALISTORE-European Research Institute, FR CNRS 3104 · ∥ Institut Universitaire de France (Paris) — \* 교신 (alejandro.franco@u-picardie.fr) · *ACS Omega* **2019**, **4**, **11141−11144** (Article · 호 미인쇄) · 접수 2019-05-03 · 수락 2019-06-05 · 출판 2019-06-26 · **CC-BY-NC-ND** · 연구비 = EU Horizon 2020 ERC **772873 "ARTISTIC"** · CGMD 구조 제공 = A. C. Ngandjong · T. Lombardo (감사 · p.4) · 이해상충 없음.
> **이웃 카드 (링크만)**: [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (이 논문 = ref [39] · L165 · L262 · L450 — 가리킨 카드) · [`benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`](benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md) (ref [28] · L379) · [`benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode`](benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode.md) (ref [31] · L404) · [`benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode`](benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode.md) (INNOV [47, 48] · L82) · [`zhang2023_pfib_multiscale_imaging_4d_thick_cathode`](zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md) (INNOV ref 43/44 · L214) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (INNOV ref [67] · L277) · [`duquesnoy2020_calendering_ml_mesostructure_generator`](duquesnoy2020_calendering_ml_mesostructure_generator.md) (Chouchane = 코드 저자).
> **판독 원자료**: `litdb/figures/chouchane2019_innov_voxelization_multiphase_meshing/digitized.csv` (10 행 — Fig. 3 왼쪽 (precision 1) · 오른쪽 (precision 5) 단면의 상별 면적 몫 + CBD 2D 조각 수 · 최대 조각 몫) · 그림 크롭 **29 장** (도구 7 중 다시 자름 1 + 손 크롭 22 = 초록 그림 1 · 패널 4 · 식 0 (원문에 식이 없다) · 근거 문단 17) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 그룹 CGMD (LAMMPS) 가 만든 구 배치 (AM 반지름 1.4–9.4 µm · CBD 반지름 0.65 µm) 를 **"specific function" 으로 이진 영상 묶음으로 바꾼 뒤** (변환 규칙은 한 문장뿐 — p.3 · SI p.3), **화소 = 노드 (상 코드) · 이웃 두 장의 4 + 4 노드 = 정육면체 → 사면체** 로 모든 상을 한꺼번에 메싱해 (상이 섞인 칸만 Nielson–Franke 분리면 경우로 더 쪼갬 · p.3) COMSOL 5.4 의 mphtxt 로 넘기는 도구이고, 예시 NMC 전극에서 **영상 기공 50.1 % ↔ 메시 49.7 %** · 매끄럽게 하면 **49.69 → 50.07 %** · 상별 부피 오차 **< 2 %** · AM 표면 피복 **CBD 36.2 / 전해질 63.8 %** 를 관측량으로 낸다 (p.2 · 표 1).  **"겹친 구를 어떻게 하나의 고체로 잇는가" (상 우선 · 복셀 안 판정 · 화소 크기 µm) 는 원문에 없다** — 노드가 '상' 으로만 코드화되므로 같은 상 입자는 한 덩어리로 융합된다는 것까지가 원문에서 읽히는 전부다 [카드 해석 · p.3 · Fig. 3].

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 넘김 (입자 계산 → FE) — 무엇을 · 어떻게 | CGMD 출력 = *"coordinates of the centers and radii for each particle"* (텍스트) → MATLAB 함수 → 이진 영상 묶음 → INNOV (노드 · 요소 · 경우 판정 · 중복 노드 제거 · (선택) 매끄럽게) → COMSOL 5.4 **mphtxt** + **Selections** 자동 생성 (도메인 · 경계 *"typically thousands"*) · **넘기는 것 = 상 라벨 기하만** (입자 번호 · 접촉 · 힘 · 응력 · 이력 없음) · 넘긴 시점 (CGMD 의 슬러리 · 건조 · 압연 중 어느 상태) **[미확인]** | [인쇄] p.2–3 · SI p.3–4 · Fig. 2 · Fig. S2 · S3 |
| ② ★ 구 → 영상 규칙 (겹친 구 · 상 우선 · 화소 크기) | **원문에 없다** — *"A specific function converts this input into binary images"* (p.3) · *"A MATLAB-based function was created to convert this output into a stack of binary images"* (SI p.3) 뿐 · 'overlap' 0 회 · 'sphere' 0 회 (본문 · SI) · 화소 크기 = *"a scale factor parameter (ratio m/pixel)"* (p.3) — 값 미인쇄 · 영역 크기 (µm) 미인쇄 | [인쇄] p.3 · SI p.3 · [미확인] |
| ③ ★ 기공 연산자 · 점검 | 기공 두 값 = **영상 (stack) 50.1 % · 메시 49.7 %** · 매끄럽게 전 / 뒤 **49.69 / 50.07 %** · 상별 부피 보존 (메시 ÷ 영상) **void 99.2 · AM 101.6 · CBD 99.7 %** · 합격선 *"an error below 2% … considered satisfactory in our study"* (근거 없음) · *"these are average values and cannot highlight local deformations within the mesh"* | [인쇄] p.2 · 표 1 |
| ④ 해상도 · 축소 · 비용 | 201 × 200 × 179 화소 · **precision [4 4 3]** (축마다 *"one node out of how many"*) → **1 737 665 요소 · 339 067 노드 · 371 213 면 · 4.48 s** (책상 컴퓨터 · *"32 Gb RAM"*) ↔ 축소 없이 **> 48 M 요소 · 177.20 s** · 그 메시 위 계산은 *"up to several days in some cases"* · Fig. 3 precision 1 ↔ 5 단면 [판독: 상 면적 몫 변화 ≤ 0.011 · CBD 최대 2D 조각 0.077 → 0.049] | [인쇄] p.2–3 · [판독] Fig. 3 |
| ⑤ 계면 · 피복 | 모든 상을 한 번에 메싱 → *"the surface meshes at the interfaces are, by design, the same across a given interface between two different phases"* (적합 메시) · AM 표면 = CBD 와 **36.2 %** + 전해질과 **63.8 %** (합 100.0 % [카드 산술]) · 같은 상 입자끼리는 계면 없음 (상 코드 노드) [카드 해석] | [인쇄] p.2–3 · 표 1 |
| ⑥ 검증 | 상별 부피 보존 (평균) 뿐 — 메시 수렴 · 넓이 정확도 · 요소 품질 · PDE 해 · 실험 대조 **없음** | [인쇄] p.2 · [미확인] |
| ⑦ 이 묶음의 네 질문 | DEM 한계 = **말 없음** · 소성 · 큰 변형 = **말 없음** (역학 0) · 2D/3D = 3D 체적 메시 (2D 는 Fig. 3 단면 그림) + *"P2D models cannot capture the impact of the 3D electrode mesostructure and associated anisotropy on the LIB cell behavior"* (p.1) · 탈압 = **없음** | [인쇄] p.1 · §4-3 |

⛔ **한정어 (떼지 말 것)**: ① 이 논문은 **알고리즘 소개** (4 쪽) — 물리 계산 결과가 없다 (메시를 만들고 관측량만 셌다) ② 예시 구조 = **액체 LIB NMC 전극** (AM + CBD + 기공 · 기공 ≈50 %) · SE 없음 · CGMD 구조의 제조 단계 미기재 ③ **화소 크기 · 영역 크기 (µm) · 겹침 처리 미기재** → 지름당 칸 수 (해상도) 를 셀 수 없다 ④ 수치는 **한 구조 · 한 번** (반복 · 오차 막대 없음) ⑤ 'void' (부피 표) ↔ 'electrolyte' (피복 표) 는 같은 기공 상으로 읽힌다 [카드 해석].
⇒ **절대값 전이: 0 건** (재료 · 상태 · 해상도 · 목적이 다르다).  전이되는 것은 **넘김 절차와 점검 칸** (영상 ↔ 메시 기공 두 값 · 매끄럽게 전후 · 상별 부피 보존 · 피복 정의 · 축소 비용 감각) 과 **빠진 칸이 무엇인지** (입자 → 영상 단계의 보존 · 겹침 규칙 · 연결성) 다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-43 의 '왜' 칸)

의도 원문: *"h · 단계 0 — benhadjali2026 의 넘김 = 이완 뒤 0.2 µm 등방 복셀화 → GeoDict · PoreSpy · INNOV [38] · 복셀 메싱 [39] (L165) · "복셀 메싱 (겹친 구를 어떻게 하나의 고체로 잇는지 = 기공 정의 §10-5 의 열쇠)" (L450)"* (가리킨 카드 = `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L165 · L450)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "h" — 입자 계산 → FE 넘김의 선례 · 넘긴 시점 | **채움 (방법) · 일부 (시점)** | 방법 = CGMD (LAMMPS) 구 중심 · 반지름 텍스트 → MATLAB 함수 → 이진 영상 묶음 → INNOV 사면체 다상 메시 → COMSOL 5.4 mphtxt (p.2 §2 · p.3 §4.1 · §4.5 · SI p.3 · Fig. S2) · 넘기는 것 = **상 라벨 기하만** (*"each node is coded with a particle type depending on its phase (AM, CBD, electrolyte, separator, etc.)"* p.3) · 시점 = 예시 구조가 CGMD 의 어느 제조 단계인지 원문에 없다 [미확인] (구조 출처 = [10] Ngandjong 2017 · [16] Rucci 2019 · 제공 = Ngandjong · Lombardo) · 압력 · 하중 상태 없음 |
| "단계 0" — 기공 연산자 · 판정 기준 | **일부** | 영상 기공 **50.1 %** ↔ 메시 **49.7 %** · 매끄럽게 **49.69 → 50.07 %** · 상별 보존 99.2 · 101.6 · 99.7 % · 합격선 '< 2 %' (p.2 · 표 1) — '같은 구조에서 연산자 (영상 · 메시 · 매끄럽게) 에 따라 0.4 %p 흔들린다' 의 실례 · **없음**: 입자 → 영상 단계의 보존 (구 부피 합 ↔ 영상) · 진밀도 · 질량 기공 대조 · 해상도 (µm) |
| "benhadjali2026 의 넘김 = 이완 뒤 0.2 µm 등방 복셀화 → GeoDict · PoreSpy · INNOV [38] · 복셀 메싱 [39]" | **일부** | INNOV = **이 논문이 이름 붙이고 소개한 알고리즘** (*"INdefinite Number Of phases meshing through Voxelization (INNOV)"* p.2) ✓ — [38] (Chouchane & Franco 2021 B&S · 후보 표 N-73) 은 같은 도구의 뒤 논문이다 · **"0.2 µm 등방" 은 benhadjali2026 의 선택**: 이 논문은 화소 크기를 인쇄하지 않고 (scale factor 매개변수만) · 예시 축소는 **비등방 [4 4 3]** (p.2 · p.3 *"This can be scalar (isotropic) or vector (anisotropic)"*) · GeoDict 는 서론의 무작위 배치 생성기 예로만 (p.1) · PoreSpy 낱말 0 · "이완 뒤" (DEM 판 분리 · 이완) 는 이 논문에 없다 (역학 0) |
| "복셀 메싱 = 겹친 구를 어떻게 하나의 고체로 잇는지" | **없음** | 구 → 이진 영상 규칙이 원문에 없다 — 변환 함수 한 문장 (p.3 · SI p.3) · 'overlap' · 'sphere' 0 회 · 복셀 안 판정 (중심 · 부분 부피) · 다른 상끼리 겹친 복셀의 우선 (AM ↔ CBD) · 화소 크기 미기재.  원문에서 읽히는 것 [카드 해석]: 이진 영상은 복셀 하나에 값 하나라 **같은 상의 겹친 부피는 두 번 셀 수 없다 (영상 기공 = 합집합 꼴 · 구 부피 합 아님)** · 노드가 '상' 으로만 코드화 (p.3) 되므로 **같은 상 입자는 한 영역으로 융합** (Fig. 3 왼쪽: 맞닿은 초록 원들이 경계 없는 한 덩어리 [판독]) |
| "= 기공 정의 §10-5 의 열쇠" | **없음** | §10-5 (benhadjali2026 보고 DEM 기공 26.5 · 15 % 가 질량 보존 · Fig. 6 상 분율과 안 맞음 [다른 카드 · 그 카드 L172 · §10-5]) 를 이 논문으로 풀 수 없다 — 이 논문의 연산자 정보는 '영상 ↔ 메시 ↔ 매끄럽게' 세 값 (차 ≤ 0.4 %p) 뿐이고 구 → 영상 규칙 · 분석 부피 정의가 없다 · 같은 사슬의 **겹침 규칙 (CBD 부피를 줄여 AM / SE 로 옮김 · AM → SE → CBD 우선)** 은 이 논문이 아니라 뒤 논문들의 본문에 있다 [다른 카드 · `benhadjali2025_…` L28 · L64 · `benhadjali2026_oneway_…` L81 ([46] 인용)] |

**가리킨 카드 · 같은 논문을 인용한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `benhadjali2026_wip_…` L450 (ref [39]) | 서지 *"M. Chouchane, A. Rucci, A.A. Franco, A Versatile and Efficient Voxelization-Based Meshing Algorithm of Multiple Phases, ACS Omega 4 (2019) 11141–11144. https://doi.org/10.1021/acsomega.9b01279."* · 이유 칸 *"카드 없음 — 복셀 메싱 (겹친 구를 어떻게 하나의 고체로 잇는지 = 기공 정의 §10-5 의 열쇠)"* | 서지 ✓ (저자 · 제목 · 권 · 쪽 · DOI) · **겹친 구 → 고체 규칙 = 원문에 없음** | **일부** — 서지는 같고, 괄호의 기대가 원문에 없다 (카드 문제) |
| `benhadjali2026_wip_…` L165 · L262 · L289 | *"자체 INNOV [38] · 복셀 메싱 [39] → COMSOL"* · *"INNOV: Franco 그룹의 미세구조 생성 · 메싱 도구 [38] (복셀 기반 다상 메싱 [39])"* · *"INNOV 메시 → COMSOL"* | INNOV 의 이름 · 알고리즘 · COMSOL 수입 = 이 논문 (p.2–3) ✓ · '미세구조 생성' 은 이 논문의 기능이 아니다 (입력 = 이진 영상 · 구 좌표) | **채움** (한정: INNOV 원전 = [39]) |
| `benhadjali2025_…` L379 (ref [28]) | 서지 (소문자 제목 꼴) · *"카드 없음 (후보 표 N-43) — 넘김 메싱의 원전 (겹친 구 → 상 · 복셀 크기 규칙)"* | 서지 ✓ (제목 대소문자만 다름) · **'겹친 구 → 상' · '복셀 크기 규칙' = 원문에 없음** (화소 크기는 scale factor 매개변수 · 축소 precision 만) | **일부** — 기대가 원문에 없다 (카드 문제) |
| `benhadjali2025_…` L64 (그 카드의 의도 대조) | *"이 논문 §2.2 가 겹침 규칙 (AM → SE → CBD · CBD 부피 이동) 을 인쇄 (p.3) \| 일부 — 같은 그룹 규칙 하나는 확인 · 2026 판이 같은 규칙을 썼는지는 미확인"* | 겹침 규칙은 2019 메싱 논문에 없다 — 그 카드가 본 2025 본문이 출처 | **채움** (이 카드와 맞다) |
| `benhadjali2025_…` L105 · L245 | INNOV *"relies on a voxelization technique to create multi-phase volumetric meshes for FEM calculations"* · *"INNOV: Franco 그룹의 미세구조 생성 · 메싱 도구 [27] (복셀화 다상 메싱 [28])"* | ✓ (p.2–3) · 복셀 크기 · 요소 수 · 수렴 미기재는 이 논문도 같다 | **채움** |
| `benhadjali2026_fully_…` L404 (ref [31]) · L110 · L248 | *"카드 없음 … — 복셀 다상 메싱 (복셀 크기 · 겹침 처리의 열쇠)"* · *"used to voxelize and reconstruct multi-phase volumetric meshes"* | 서지 ✓ · **'복셀 크기 · 겹침 처리' = 원문에 없음** · 메싱 서술 ✓ | **일부** — 기대가 원문에 없다 (카드 문제) |
| `benhadjali2026_oneway_…` L82 · L243 | *"INNOV [47, 48] (… used to voxelize and reconstruct multiphase volumetric meshes …)"* · 복셀 크기 · 요소 [미확인] | ✓ (이 논문도 미기재) | **채움** |
| `zhang2023_…` L33 · L75 · L214 · L370 | *"INNOV(ref 43/44, Chouchane·Rucci·Franco 의 복셀화 기반 다중상 메싱 알고리즘) 로 약 2.3 M 요소 메시로 변환 → COMSOL"* | 저자 · 알고리즘 ✓ · 2.3 M 은 zhang2023 자신의 메시 (이 논문 값 아님) | **채움** |
| `ngandjong2021_…` L277 | *"INNOV 자체 복셀화(ref [67])로 메시 생성"* | ✓ | **채움** |
| 후보 표 N-43 서지 | *"M. Chouchane, A. Rucci, A.A. Franco, A Versatile and Efficient Voxelization-Based Meshing Algorithm of Multiple Phases, ACS Omega 4 (2019) 11141–11144. https://doi.org/10.1021/acsomega.9b01279"* | 첫 쪽 ✓ (덧붙임: 출판 2019-06-26 · CC-BY-NC-ND · 호 미인쇄) | **같음** |

⇒ **의도 대조 결과: 일부** — "h" (입자 계산 구조 → 이진 영상 → 사면체 → COMSOL 넘김의 원전 · 넘기는 것 = 상 라벨 기하만) 와 "단계 0" 의 점검 꼴 (영상 50.1 ↔ 메시 49.7 · 매끄럽게 50.07 % · 상별 부피 < 2 %) 은 **채움**; "0.2 µm 등방" 은 이 논문이 아니라 benhadjali2026 의 선택이고 (원문 예시는 비등방 [4 4 3] · 화소 크기 미인쇄); **"겹친 구를 어떻게 하나의 고체로 잇는지 = §10-5 의 열쇠" 는 없음** (변환 규칙 한 문장 · 겹침 낱말 0) — 세 카드 (benhadjali2026_wip L450 · benhadjali2025 L379 · benhadjali2026_fully L404) 의 같은 기대가 원문과 다르다.

---

## 1. 한 줄 요약
P2D 균질화 모델은 3D 전극 미세구조와 그 이방성을 못 담고 (p.1), 기존 3D 해상 모델은 탄소-바인더 (CBD) 를 유효 기공 · 굴곡도로 지우거나 AM 과 한 고체로 합쳤다 (p.1) — CBD (반지름 0.65 µm) 와 AM (1.4–9.4 µm) 을 따로 메싱하려면 "바위와 산을 같은 붓으로" 칠해야 한다는 문제를, **복셀화 (화소 = 노드 · 모든 상을 한 번에 사면체로)** 로 풀어 상 경계 면이 저절로 맞는 다상 체적 메시를 만들고 COMSOL 5.4 로 바로 넘기는 MATLAB 도구 **INNOV** 를 소개한다.
예시 NMC 전극 (AM + CBD + 기공) 에서 화소 축소 precision [4 4 3] 이면 1.74 M 요소를 4.48 s 에 만들고 (축소 없이 > 48 M · 177.20 s), 영상 ↔ 메시 기공 (50.1 ↔ 49.7 %) · 상별 부피 보존 (오차 < 2 %) · AM 표면 피복 (CBD 36.2 · 전해질 63.8 %) 을 '기하 온전성' 관측량으로 내놓는다.
저자의 결론: *"INNOV generates a volumetric mesh able to contain an unlimited number of phases … It offers a time-efficient tool to perform meshing without requiring substantial computational resources"* (p.2).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 · 대상 | 연구유형 |
|---|---|---|---|---|
| M. Chouchane · A. Rucci · **A. A. Franco\*** (LRCS UPJV · RS2E · ALISTORE-ERI · IUF) | ACS Omega 4, 11141–11144 (2019) · CC-BY-NC-ND | 10.1021/acsomega.9b01279 | 예시 = 액체 LIB **"three-phased LiNiMnCo electrode (AM + CBD + void)"** (CGMD 구 배치 · AM 반지름 1.4–9.4 µm · CBD 0.65 µm) · SE 없음 · 조성 · 기공 외 물성 없음 | 도구 · 알고리즘 (MATLAB 메싱) — 계산 결과 · 실험 없음 |

- **후보 표 메모와의 대조**: 저자 · 제목 · 학술지 · 권 4 · 쪽 11141–11144 · 2019 · DOI — **같다**.  덧붙임 ① 출판 2019-06-26 (접수 05-03 · 수락 06-05) ② 호 번호는 PDF 에 없다 ③ PDF 문서 정보의 제목 'research 1..4' 는 조판 파일 이름 (논문 제목 아님).
- **글의 꼴**: 초록 (+ 캡션 없는 초록 그림) → 1 서론 → 2 결과 · 논의 (2.1 메싱 · 2.2 관측량) → 3 결론 → 4 방법 (4.1 입력 · 4.2 노드 · 4.3 요소 · 4.4 알고리즘 · 4.5 수입) → 참고문헌 20.  그림 3 · 표 1 · **번호 식 0 · 문장 안 식 0** / SI: 표지 + 그림 S1–S3 (각 한 문단 설명).
- **그룹 맥락**: ARTISTIC (ERC) 의 "제조 모의 구조 → 3D 전기화학" 사슬의 메싱 고리.  같은 도구가 뒤에 [다른 카드]: ngandjong2021 (DEM 캘린더링 구조 → INNOV → COMSOL) · zhang2023 (PFIB 영상 → INNOV → COMSOL) · benhadjali2025 · 2026 세 편 (CGMD 구조 → 겹침 후처리 → INNOV → COMSOL) 에 쓰였다.  같은 도구의 사용자용 판 = Chouchane & Franco, Batteries & Supercaps 4 (2021) 1451–1456 (후보 표 N-73 · 이 논문 참고문헌에는 없다 — 뒤 논문).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 입력 · 예시 구조 (p.2–3 · SI p.3 · `txt_p2_innov_name_comsol54_am_cbd_radii.png` · `txt_p2_three_phase_input_precision_443_counts_4p48s.png` · `txt_p3_cgmd_input_node_generation_precision_timing.png` · `txt_si_p3_lammps_centers_radii_to_binary_stack.png` · `fig_S2.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 예시 전극 | *"a three-phased LiNiMnCo electrode (AM + CBD + void) generated from CGMD calculations using LAMMPS software"* — [10] Ngandjong 2017 · [16] Rucci 2019 의 방법 · 구조 제공 = Ngandjong · Lombardo | [인쇄] p.2 · p.4 |
| 입자 크기 | AM **반지름 1.4–9.4 µm** (*"multiple sizes"*) · CBD **반지름 0.65 µm** | [인쇄] p.2 |
| 크기 비 | AM ÷ CBD 반지름 = **2.2–14.5** (1.4/0.65 · 9.4/0.65) — 저자의 '바위와 산' 비유의 크기 | [카드 산술] |
| 입력 꼴 | *"a text file with coordinates of the centers and radii of each of the particles"* → *"A specific function converts this input into binary images"* (MATLAB) — 또는 단층 분할 영상 · 3D 물체 파일을 자른 영상 | [인쇄] p.2–3 · SI p.3 |
| 이진 영상 크기 | **201 × 200 × 179 화소** (§4.2 의 예 · 세 상 AM · CBD · 전해질) = **7 195 800 화소** [카드 산술] | [인쇄] p.3 |
| 화소 크기 · 영역 크기 (µm) | *"a scale factor parameter (ratio m/pixel) ensures the geometric dimensions"* — **값 미인쇄** | [미확인] |
| 상 이름 | 부피 표 = 'void' · 피복 표 = 'electrolyte' · §4.2 예 = 'electrolyte' — 같은 기공 (액체 전해질 자리) 상으로 읽힌다 | [카드 해석] |
| ⚠ 같은 구조인가 | §4.2 의 201 × 200 × 179 예 (4.48 s · [4 4 3]) 와 Fig. 1 · 표 1 의 메시 (4.48 s · [4 4 3]) 는 시간 · 축소가 같아 **같은 구조로 읽힌다** — 원문은 같다고 명시하지 않는다 | [카드 해석] |

### 3-2. 메시 크기 · 시간 (p.2–3 · `txt_p2_three_phase_input_precision_443_counts_4p48s.png` · `txt_p3_downsized_1p5m_vs_48m_scale_factor.png`)
| 양 | 값 | 표지 · 쪽 |
|---|---|---|
| precision [4 4 3] 메시 (Fig. 1 a · b) | **339 067 노드 · 371 213 면 · 1 737 665 요소** (매끄럽게 전 · 뒤 같음) | [인쇄] p.2 |
| 시간 · 기계 | 매끄럽게 하지 않은 메시 **4.48 s** · *"a desktop computer (32 Gb RAM)"* · 매끄럽게 하기 시간 미기재 | [인쇄] p.2 · [미확인] |
| 축소 없이 | **> 48 million elements** · **177.20 s** (축소 [4 4 3] 은 *"more than 1.5 million elements"* · 4.48 s) | [인쇄] p.3 |
| 그 메시 위 계산 | *"the simulation time (which can be up to several days in some cases) of the downsized mesh will also decrease"* — 숫자 없음 | [인쇄] p.3 |
| 축소 뒤 격자 노드 | 첫 노드 + N 칸마다 하나를 남긴다고 보면 ⌈201/4⌉ × ⌈200/4⌉ × ⌈179/3⌉ = 51 × 50 × 60 = **153 000** → 보고 노드 339 067 = **2.2 배** (상이 섞인 칸에서 분리면 꼭짓점이 더 생긴다고 읽힌다) | [카드 산술 · 해석] |
| 요소 / 정육면체 | 축소: 1 737 665 ÷ (50 × 49 × 59 = 144 550) = **12.0** · 축소 없이: > 48 M ÷ (200 × 199 × 178 = 7 084 400) = **≥ 6.8** (한 상 칸 = 사면체 5 또는 6 · 섞인 칸 = 더 많이 → 거친 격자일수록 섞인 칸 몫이 커진다) | [카드 산술 · 해석] |
| 축소 효과 | 요소 수 **≥ 27.6 배** · 시간 **39.6 배** ↔ 화소 수 비 4 × 4 × 3 = **48** · 요소당 시간 ≈ **2.6 µs** (축소) · **≤ 3.7 µs** (축소 없이) | [카드 산술] |
| 분할 방식 | 정육면체 → **5 또는 6 사면체** (6 = *"more precise and easier to implement"* · 요소 더 많음 / 5 = 추가 연산) — **예시에 어느 쪽을 썼는지 미기재** | [인쇄] p.3 · [미확인] |

### 3-3. ★ 관측량 — 기공 두 값 · 상별 부피 보존 · 표면 피복 (p.2 · 표 1 · `tab_1.png` · `txt_p2_two_porosities_stack_501_mesh_497.png` · `txt_p2_volume_conservation_2pct_coverage.png` · `txt_p2_staircase_smoothing_porosity_4969_5007.png`)
**표 1 (원문 · "Observables Provided by INNOV after the Meshing of the Electrode in Figure 1a" — 매끄럽게 하기 전 메시)** [인쇄 p.2]:

| 상 | 메시 부피 % | 부피 보존 (메시 ÷ 영상) | 영상 부피 % [카드 산술 = 메시 ÷ 보존] | 메시 − 영상 [카드 산술] |
|---|---|---|---|---|
| void | **49.7 %** | **99.2 %** | 50.10 % (본문 *"the porosity of the stack is 50.1%"* ✓) | −0.40 %p |
| AM | **30.5 %** | **101.6 %** | 30.02 % | +0.48 %p |
| CBD | **19.8 %** | **99.7 %** | 19.86 % | −0.06 %p |
| 합 | 100.0 % | — | 99.98 % | — |

- 표 1 둘째 줄 (피복): **AM with CBD 36.2 % · AM with electrolyte 63.8 %** — 본문 *"the surface area of the interfaces between the active material and CBD (36.2%) or the active material and electrolyte (63.8%)"* [인쇄 p.2] · 합 **100.0 %** [카드 산술] → AM 표면을 두 갈래로만 나눴다 (AM–AM 면은 같은 상이라 없고 · 상자 바깥 면의 처리는 [미확인]) [카드 해석] · 넓이 계산법 (삼각면 넓이 합?) [미확인].
- **'보존' 의 정의**: 원문에 식이 없다 — '메시 ÷ 영상' 으로 읽으면 본문의 영상 기공 50.1 % 를 정확히 재현한다 (49.7 / 0.992 = 50.10) [카드 산술].
- **합격선**: *"Here, the meshing step introduces an error below 2% on the volume of each phase, which is considered satisfactory in our study"* — 가장 큰 오차 = AM **+1.6 %** (부피비) [인쇄 · 카드 산술] · 2 % 의 근거 없음.
- **매끄럽게 하기** (Kroon's function [17, 18]): *"the smoothing algorithm tends to shrink the volume of the elements, resulting in a slight increase in the porosity (for the example here, 49.69% before and 50.07% after smoothing)"* [인쇄 p.2] → **+0.38 %p** · 매끄럽게 한 메시는 영상 기공과 −0.03 %p [카드 산술] · 노드 · 면 · 요소 수는 같다 (*"both have …"*).
- **저자 한계**: *"these are average values and cannot highlight local deformations within the mesh"* [인쇄 p.2].
- 다른 관측량 (요소 품질 · 계면 넓이 절대값 · 연결성 · 굴곡도) **없음**.

### 3-4. 축소 (precision) — 원문 서술 + Fig. 3 판독 (p.3 · `fig_3.png` · `fig_3_left.png` · `fig_3_right.png` · digitized.csv fig3)
- **정의** [인쇄 p.3]: *"the function embeds an anisotropic downsizing tool in the form of a "precision" parameter. This can be scalar (isotropic) or vector (anisotropic), indicating the downsizing factor along each axis, that is, one node out of how many will be saved for the node generation. While slightly losing in precision, the gain in time can be tremendous."* — 축소 = **화소를 N 개 중 하나만 노드로 남기는 표본 추출** (평균 · 다수결 아님으로 읽힘 [카드 해석]) → 실제 메시 칸 크기 = precision × 화소 크기.
- **Fig. 3** (캡션 *"Slices of a mesh (left) without downsizing (precision = 1) and (right) with downsizing (precision = 5). AM is in green, CBD is in yellow, and void is in purple."*) — 정량 서술은 원문에 없다.  [판독 · 내장 래스터 xref 212 (300 dpi) 화소를 세 색 중 가장 가까운 색으로 분류 · 단면 하나의 **2D 면적** 몫 (부피 아님)]:

| 단면 | AM (초록) | 기공 (보라 · 테두리 띠 포함) | CBD (노랑) | CBD 2D 조각 (≥ 30 px) | 가장 큰 CBD 조각 (단면 몫) |
|---|---|---|---|---|---|
| 왼쪽 precision 1 | 0.507 | 0.329 | 0.164 | 16 | 0.077 |
| 오른쪽 precision 5 | 0.518 | 0.319 | 0.163 | 20 | 0.049 |

  → 면적 몫은 **≤ 0.011** 만 바뀌는데 (AM +, 기공 −) CBD 의 **가장 큰 조각이 0.077 → 0.049** 로 줄고 조각 수가 16 → 20 으로 는다 [판독] — 얇은 CBD 목이 계단 모양 · 대각선 블록 사슬로 끊긴 것이 눈에도 보인다 (오른쪽 왼쪽 위 · 가운데).  ⚠ 2D 연결성은 3D 연결성이 아니다 · 그림 화소 (메시 복셀 아님) 위 셈 · 단면 위치가 같은지 · 보라 테두리 띠가 기공인지 영역 밖인지 원문 설명 없음.
- ⚠ Fig. 3 의 단면 AM 면적 ≈0.51 은 표 1 의 AM 부피 30.5 % 와 다르다 — 단면 하나라 견줄 수 없고, Fig. 3 이 표 1 과 같은 구조인지도 원문에 없다 [미확인].

### 3-5. ★ 원문 안 어긋남 · 결손 (카드가 본 것 — 고치지 않고 적는다)
1. **INNOV 풀이 두 가지**: p.2 *"INdefinite Number Of phases meshing through Voxelization (INNOV)"* ↔ p.4 약어 목록 *"INNOV, infinite number of phase meshing through voxelization"*.
2. **그림 번호**: p.2 *"the input is a text file with coordinates of the centers and radii of each of the particles (see Figure S3)"* — 구 좌표 입력 · 영상 변환은 **SI Fig. S2** 에 그려져 있다 (S3 = 화소 → 노드 → 요소).  p.3 §4.1 은 같은 내용을 *"(see Figure S2)"* 로 맞게 가리킨다.
3. **낱말**: §4.3 *"the 4 pixels associated on the next slide"* — 'slice' 의 오기로 읽힌다 (SI p.4 *"two neighboring slices"*) · SI Fig. S2 캡션 *"Meshing process of meshing from CGMD structure to the volumetric mesh"* (낱말 겹침) · 서론 *"thecarbon−binder domain"* (띄어쓰기) · *"32 Gb RAM"* (Gb = GB 로 읽힘).
4. **상 이름 두 벌**: 부피 = 'void' ↔ 피복 = 'electrolyte'.
5. **미기재**: 화소 · 영역 크기 (µm) · scale factor 값 · 예시 구조의 제조 단계 · 분할 방식 (5 / 6) · 매끄럽게 하기의 반복 수 · 강도 · 'faces' 의 정의 (경계 삼각면 수로 읽힘) · 피복 넓이 계산법 · Fig. 2 '입력' 칸의 *"Dimension of the box (x,y,z)"* 의 쓰임.
6. (확인 — 어긋남 아님) 표 1 보존 99.2 % ↔ 기공 49.7 / 50.1 = 0.992 ✓ · 본문 '메시 49.7 %' ↔ '매끄럽게 전 49.69 %' ✓ · '> 1.5 million' ↔ 1 737 665 ✓.

---

## 4. ★ 방법 — 알고리즘 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 알고리즘 사슬 (원문 순서 · Fig. 2 · SI Fig. S2 · S3)
0. **입력** (p.2–3 §4.1 · SI p.3): 이진 영상 묶음 — ① 단층 영상 분할 ② 3D 물체 파일 자르기 ③ 입자 중심 · 반지름 파일 (CGMD) → *"A specific function converts this input into binary images to feed the algorithm with and to reconstruct the electrodes"* (규칙 미기재).  *"Once the binary stacks of images are generated"* (p.2 · 복수) — 상마다 이진 묶음 하나일 수 있다 [카드 해석].
1. **노드 생성** (p.3 §4.2 · Fig. 2 입력 = Images · Scale factor · Precision): 화소 하나 = 노드 하나 · 노드에 상 코드 · *"Since the number of nodes is equal to the number of pixels, aiming for high-resolution images can be a double-edged sword"* · precision 축소 · scale factor (m/pixel).  **계산 시간을 정하는 단계** (*"computational time-limiting step"*).
2. **요소 생성** (p.3 §4.3 · SI p.4 · Fig. S3): 이웃 두 장의 4 + 4 노드 = 정육면체 → 사면체 5 개 또는 6 개.
3. **경우 판정 · 알고리즘** (p.3 §4.4): 요소 노드들의 상 조합 **네 경우** — 모두 같은 상 = 그대로 · 나머지 셋 = *"a decomposition into several more tetrahedrons and the creation of triangular faces to effectively separate the phases"* · 분할 수학 = **Nielson & Franke [19] 분리면** (p.2 §4) · 모든 상을 한 번에 → 계면 면 메시가 양쪽에서 같다.  *"the more intricate the phases are, the more surface area there is between them, and the higher the number of elements and faces"*.
4. **중복 노드 제거**: Iso2Mesh [20] 의 함수 (p.2 §4).
5. **(선택) 매끄럽게**: Kroon's function [17, 18] — 계단 모양 완화 · 요소 부피 줄어 기공 ↑ (p.2).
6. **관측량**: 영상 · 메시 기공 · 상별 부피 보존 · 계면 피복 (p.2 §2.2 · 표 1).
7. **수입**: COMSOL 5.4 mphtxt · "Selections" 자동 생성 — *"manual selections would have been prohibitory since there are typically thousands of domains and boundaries in the imported mesh in COMSOL"* (p.3 §4.5).

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **입자 → 상 라벨**: *"each node is coded with a particle type depending on its phase (AM, CBD, electrolyte, separator, etc.)"* (p.3) → 입자 번호가 없다 · **같은 상 입자는 한 덩어리** (입자 경계 · 계면 없음) [카드 해석 · Fig. 3 왼쪽의 맞닿은 초록 원들이 한 영역 [판독]].  COMSOL 의 '도메인 수천 개' 는 상별 연결 성분일 것으로 읽힌다 [카드 해석 · 원문 정의 없음].
- **겹친 구**: 규칙 미기재.  이진 영상의 성질상 같은 상의 겹친 부피는 한 번만 세진다 (합집합) [카드 해석] · 서로 다른 상 (AM ↔ CBD) 이 같은 복셀을 차지할 때의 우선 [미확인] · 복셀 안 판정 (중심 · 부분 부피) [미확인].
- **접촉 · 계면**: 같은 상 접촉 = 융합 (계면 없음 → 그 위 수송에는 접촉 저항 항이 없다) · 다른 상 접촉 = 공유 삼각면 (적합 메시) · 접촉 저항 · 미끄럼 · 분리 모형 없음 [카드 해석].
- **형상**: 구 배치를 그대로 화소화 → 계단 모양 (매끄럽게 하면 완화) · 형상 변화 · 변형 계산 없음.
- **DEM · 역학**: 없음 (입력 구조의 입자 계산은 다른 논문의 CGMD).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · SI 에 'DEM' · 'discrete' 0 회 · 'contact' 1 회 = *"Where the AM and the CBD are in contact, the elements of the mesh of the AM should be finer to match the ones of the CBD"* (p.1 · 적응 메시 크기 맞춤의 어려움)).  입력 구조는 구 (*"The spherical active material particles"* · Fig. 1 캡션) 이지만 그 한계를 다루지 않는다.  원문이 비판한 한계는 **3D 전기화학 모델의 CBD 표현** 이다: *"reported 3D-resolved models rely on oversimplifications, such as an implicit representation of the CBD through the use of effective parameters for porosity and tortuosity or by merging CBD with the active material (AM) as a single solid phase"* (p.1).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **말 없음** (역학 0 · 'plastic' 은 참고문헌 제목뿐).  원문의 비용 논의는 **메시 크기 ↔ 시간** 뿐: 축소 없이 > 48 M 요소 · 177.20 s ↔ [4 4 3] 1.74 M · 4.48 s · 그 위 계산 *"up to several days"* (p.3).
3. **2D / 3D** — 3D 체적 메시 (Fig. 1) · 2D 는 Fig. 3 단면 그림뿐.  원문의 차원 문장 = *"P2D models cannot capture the impact of the 3D electrode mesostructure and associated anisotropy on the LIB cell behavior"* (p.1) — 균질화 (의사 2 차원) 전기화학 ↔ 3D 해상의 대조이지, **2D 해상 계산 → 3D 해상 계산의 전이에 대한 말이 아니다**.
4. **압력을 뺄 때의 거동** — **다루지 않았다** (압력 · 하중 0).

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| INNOV | INdefinite (p.2) / infinite (p.4) Number Of phases meshing through Voxelization — 이 논문의 MATLAB 알고리즘 |
| 복셀화 메싱 | 화소 격자를 그대로 노드로 쓰고 이웃 두 장 사이 정육면체를 사면체로 나누는 메싱 (경계 맞춤 메싱이 아님) |
| precision | 축마다 'N 개 중 하나' 노드만 남기는 축소 배수 (스칼라 = 등방 · 벡터 = 비등방) |
| scale factor | m / 화소 — 메시의 실제 치수 |
| 분리면 (Nielson–Franke) | 상이 섞인 칸을 사면체로 더 나누고 상 사이에 삼각면을 만드는 방법 [19] |
| 계단 모양 · 매끄럽게 | 복셀 경계의 계단 — Kroon 함수로 노드를 옮겨 완화 (요소 부피가 줄어 기공 ↑) |
| 부피 보존 | 상별 메시 부피 ÷ 영상 부피 (평균 · 국소 변형은 못 본다) |
| 피복 % | AM 표면 가운데 CBD 와 · 전해질과 맞닿은 넓이 몫 |
| mphtxt · Selections | COMSOL 고유 메시 글 형식 · 도메인 / 경계 묶음 자동 지정 |
| CBD · CGMD | carbon–binder domain · coarse-grained molecular dynamics (LAMMPS) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **TOC** (`fig_TOC.png` · 손 크롭) | 초록 그림 (캡션 없음) — 'INNOV' 글자를 오려 낸 다색 메시 판 + 메시 새 | 도구가 배터리 밖 물체도 메싱한다는 표지 (값 없음) |
| **Fig. 1** (`fig_1.png` · 패널 `fig_1a` · `fig_1b`) | NMC 전극 메시 (a) 매끄럽게 전 (b) 뒤 — AM 빨강 · CBD 노랑 · 339 067 노드 · 1 737 665 요소 | 다상 메시 겉모습 · CBD 가 AM 을 덮은 그림 — 기공 49.69 → 50.07 % 의 짝 |
| **Fig. 2** (`fig_2.png` · 다시 자름) | 작업 흐름: 노드 생성 (Images · Scale factor · Precision) → 요소 생성 (Dimension of the box) → 경우 판정 (Case 3 그림) → 알고리즘 | 넘김 절차 그림 (보고서 붙임) |
| **Fig. 3** (`fig_3.png` · `fig_3_left` · `fig_3_right`) | 단면 precision 1 ↔ 5 — AM 초록 · CBD 노랑 · 기공 보라 | ★ 축소가 얇은 CBD 목을 끊는 그림 [판독: 면적 ≤ 0.011 · 최대 조각 0.077 → 0.049] — 해상도 · 연결성 점검의 근거 |
| **Table 1** (`tab_1.png`) | 상별 부피 % · 보존 % · AM 피복 % | ★ 기공 두 값 · 보존 · 피복 정의 |
| **SI Fig. S1** (`fig_S1.png`) | LIB 셀 개략 (Li 박 · 분리막 · 전해질 · AM · 탄소 · 바인더) | 상 이름 맥락 (액체 LIB) |
| **SI Fig. S2** (`fig_S2.png`) | CGMD 출력 (x, y, z, radius) → 이진 분할 영상 → INNOV → 체적 메시 (가운데 초록 판이 낀 두 전극 판 — 색 설명 없음) | ★ 넘김 사슬 그림 (입자 → 영상 → 메시) |
| **SI Fig. S3** (`fig_S3.png`) | 노드 망 (화소 = 색 점) → 요소 생성 (두 장 · 정육면체) → 사면체 | 화소 = 노드 · 4 + 4 노드 정육면체 그림 |
| 식 크롭 **0** | 원문에 번호 식 · 문장 안 식이 없다 | — |
| 근거 문단 17 (`txt_p*` · `txt_si_p*`) | 카드가 인용한 문장 · 숫자 · 정의 | 보고서 붙임 · 원문 확인 |

## 6. Post-processing ★
- **기공**: ① 영상 기공 = 이진 영상의 기공 화소 몫 (50.1 %) ② 메시 기공 = 기공 상 사면체 부피 몫 (49.7 %) ③ 매끄럽게 뒤 메시 기공 (50.07 %) — 진밀도 · 질량 · 구 부피 합 기공 없음.
- **상별 부피 보존**: 메시 상 부피 ÷ 영상 상 부피 (평균) · 합격선 2 %.
- **피복**: AM 표면의 상별 넓이 몫 (CBD · 전해질) — 메시가 끝나면 나온다 (*"provided once the mesh is done"*).
- **크기 · 시간**: 노드 · 면 · 요소 수 · 메싱 시간 (축소 전 / 뒤).
- **판독 (이 카드)**: Fig. 3 내장 래스터 화소 → 가장 가까운 세 색 · 단면 면적 몫 · scipy.ndimage 연결 성분 (≥ 30 px) — digitized.csv note 열에 방법 전부.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태 · 목적이 다르다** — 이 논문은 물리 계산이 아니라 넘김 도구)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 입자 → 격자 변환 규칙 | 미기재 (*"A specific function"*) | STEP3 래스터화: 점 스탬프 (입자당 한 칸) · 구 스탬프 (`--step3-sdcp-sphere-d` · 게이트 d/vox ≥ 2) · 상 우선 결함 시험 `sdcp-prio` · `--step3-sdcp-yield-to-vgcf` [우리 · CLAUDE.md] | 우리는 규칙이 코드 · 시험에 있다 · 그들 원문엔 없다 |
| 변환의 보존 점검 | **영상 → 메시** 만 (상별 99.2 · 101.6 · 99.7 %) | **입자 → 격자** 원장 (CL-25: 점 스탬프 SDCP 표현 부피 ÷ 참 부피 4.311 (vox 0.4) → 0.238 (vox 0.15) · 구 스탬프 0.986) [우리 · CLAUDE.md] | 점검하는 단계가 다르다 — **둘 다 필요** (§7-2) |
| 기공 연산자 차이 | 영상 50.1 ↔ 메시 49.7 ↔ 매끄럽게 50.07 % (≤ 0.4 %p · 같은 영상 위) | ε_sphere ↔ ε_union 13.47 ↔ 14.98 % (≈1.5 %p · 2mAh_real_9) · MPM 관례 ↔ ε_sphere 1.251 %p (real_14 · SE–SE 0.402 + AM–SE 0.848) [우리 · CLAUDE.md] | **부류가 다르다** — 그들 = 메싱 · 매끄럽게 차이 · 우리 = 겹침 부피 부기 규약 차이 → 같은 표에 놓지 않는다 |
| 같은 상 접촉 | 상 코드 노드 → 융합 (계면 없음) [카드 해석] | STEP3 복셀 FV = CONTACT_FREE 가지 (조화 평균 · Holm 항 0 · CL-81) · 접촉망 = 접촉마다 Holm 1/(2σa) [우리 · CLAUDE.md] | 그들 메시 위 수송도 **CF 부류** (접촉 저항 없음) [카드 해석] — 접촉망 FULL 과 비교 금지 |
| 피복 | AM 표면 CBD 36.2 · 전해질 63.8 % (한 해상도 · 메시 삼각면) | real_14 AM–SE 기하 16 % (틈 ≤ 0) · 49 % (0.14 µm 안) ≈ Hertz 18 · Tabor 52 % · MPM 복셀 인접 피복 (~26 %) 은 격자에 묶여 수렴하지 않아 보고하지 않는다 [우리 · CLAUDE.md] | 정의 · 상 (CBD vs SE) 다름 · 그들 값도 해상도 의존일 수 있다 (수렴 시험 없음) |
| 해상도 규칙 | 없음 (축소 비용만 · 화소 크기 미기재) | d_h/dx ≳ 3.5 (MPM SE 응력) · 구 스탬프 d/vox ≥ 2 [우리 · CLAUDE.md] | 그들 지름당 칸 수를 셀 수 없다 |
| 3D 크기 | 7.2 M 화소 → > 48 M 사면체 (≥ 6.8 / 칸) | STEP3 dof (풀이 미지수 = 전도 칸) 45.4 M (vox 0.125) · 86.8 M (vox 0.10) [우리 · CLAUDE.md] | 그 dof 수만큼의 칸을 같은 방식으로 사면체화해도 ≈3–6 × 10⁸ 요소 [카드 산술 · 그들 비 ≥ 6.8 가정 · 전체 복셀 수는 더 크다] — 책상 컴퓨터 범위 밖 |
| 재료 · 상 | 액체 LIB NMC + CBD + 기공 (≈50 %) | LPSCl + NCM (+ 탄소 · PTFE · SDCP) · 300 MPa 압밀 | 다름 — 값 대조 없음 |

### 7-2. ★ 넘김 연산자 — §10-5 질문에 대한 답과 우리에게 줄 것
- **질문**: benhadjali2026 (WIP ↔ CUP) 의 DEM 보고 기공 26.5 · 15 % 가 질량 보존 ((1 − ε) × 두께 33.6 ↔ 31.8 µm · −5.4 %) · 상 분율 평균과 맞지 않는다 [다른 카드 · 그 카드 L172 · §10-5] → "겹친 구를 하나의 고체로 잇는 규칙" 을 그 넘김의 메싱 원전 (이 논문) 에서 찾으려 했다.
- **답**: 이 논문엔 그 규칙이 없다.  말할 수 있는 것 [카드 해석]: 이진 영상 기공은 합집합 꼴 (구 부피 합이 아니다) · 같은 상 입자는 융합 · 다른 상 겹침 규칙은 미기재 · 영상 → 메시 단계에서 기공이 바뀌는 크기는 이 예시에서 ≤ 0.4 %p (매끄럽게 포함) 다 — §10-5 의 어긋남 (기공 수 %p 급) 은 메싱 단계의 크기로는 설명되지 않는다 (구조 · 도구 · 해상도가 달라 크기 비교는 어림).  같은 사슬의 겹침 규칙 (CBD 부피를 AM / SE 로 옮김) 은 뒤 논문들의 본문에 있다 [다른 카드 · benhadjali2025 L28 · L64 · benhadjali2026_oneway L81].
- **우리에게 줄 것 — 넘김마다 보존 점검 둘을 결과 전에 등록**: (가) **입자 → 격자**: 상별 표현 부피 ÷ 참 부피 (구 부피 합 또는 합집합 — 어느 것인지 명시) + 겹침 처리 (상 우선 순서 · 부피 이동 여부) (나) **격자 → 메시 · 해**: 상별 부피 보존 + 기공 두 값 (격자 · 메시) + 매끄럽게 전후.  이 논문은 (나) 만 했고, 우리 CL-25 원장은 (가) 만 한다.

### 7-3. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **DEM 도 MPM 도 아닌 넘김 층** (입자 · 영상 구조 → FE 메시).  역학 · 압밀 · 수송 해 없음.
- 우리 사슬의 같은 자리: DEM 덤프 → STEP3 복셀 (FV 를 복셀 위에서 바로 풀어 사면체 메싱이 없다) · MPM scaffold (DEM 좌표로 SE 씨앗) · COMSOL 쪽은 2D 내보내기 (`f_ion` 행 · τ 규약 절) [우리 · CLAUDE.md].  3D COMSOL 로 넘기려면 이 논문 꼴 (이진 영상 → 사면체 · mphtxt) 이 한 경로다 — 단 입자 번호 · 접촉 저항은 이 경로에서 사라진다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 액체 LIB NMC 전극의 메싱 도구 — **SE 0 · 압력 0 · 역학 0** 이라 랩 표준 · DEM · MPM 값과 나란히 놓을 숫자가 없다 (예시 기공 ≈50 % 는 랩 표준과 다른 문헌 값 · 다른 재료 · 다른 상태).)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ ① **같은 구조의 기공이 연산자마다 다르다** — 영상 50.1 · 메시 49.7 · 매끄럽게 50.07 % (≤ 0.4 %p) → 기공 보고 칸에 '격자 / 메시 / 매끄럽게 여부' ② **상별 부피 보존 + 결과 전 합격선** (그들은 2 % — 근거 없음) 의 꼴 ③ 피복 = 'AM 표면 넓이의 상별 몫' 정의 ④ ★ 빠진 칸이 무엇인지: **입자 → 격자 단계의 보존 · 겹침 규칙 · 화소 크기** (§7-2) | 압력별 기공 · 진밀도 · 질량 기공 · 랩 표준 대조값 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각: 7.2 M 화소 → > 48 M 사면체 (≥ 6.8 / 칸) · 177 s · 32 Gb 책상 컴퓨터 / 축소 [4 4 3] → 1.74 M · 4.48 s (요소 ≥ 1/27.6 · 시간 1/39.6) [인쇄 · 카드 산술] · 같은 도구 쓰임 [다른 카드]: zhang2023 (L33) 33 × 33 × 71.5 µm³ → ≈2.3 M 요소 · ngandjong2021 (L84) 25.8 × 25.8 × 133.8–165.0 µm³ → > 0.8 M 요소 | 입자별 장 · 메모리 숫자 · PDE 풀이 비용 없음 (*"several days"* 만) |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 맞춤) | 없음 | — |
| **단계 5** (3D 복합 압밀) | 없음 (압밀 없음) | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ 눌린 구조를 3D FE 로 넘길 때의 경로 (이진 영상 → 사면체 · 계면 적합 · COMSOL Selections) · 피복 정의 · **같은 상 융합 = 접촉 저항 0 (CF 부류)** 표지 · ★ **축소가 부피는 지키고 연결성을 바꾼다** (Fig. 3 [판독]: 면적 몫 ≤ 0.011 · CBD 최대 2D 조각 0.077 → 0.049) → 수송 넘김의 점검에 상별 연결 성분 · 관통을 더할 근거 | 수송 해 · 굴곡도 · 접촉 저항 · 3D 연결성 수치 없음 |
| **후보 D0** (지금 DEM) | 우리 DEM 덤프 (중심 · 반지름 · 종류) = INNOV 입력 꼴 그대로 → 같은 경로로 3D FE 넘김 가능 — 단 겹침 처리 (ε_sphere ↔ 합집합 · 상 우선) 를 **우리가** 정해 적어야 한다 | DEM 결과 · 한계 서술 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | MPM 으로 변형된 SE (구 아님) 를 FE 로 넘길 때 '이진 영상' 입력이 형상을 가리지 않는다 (3D 물체 파일 자르기 · 영상 경로) | 입자별 장 · 번호를 실어 나르지 못한다 (상 코드 노드) — A′ 의 입자 정체가 넘김에서 사라진다 |
| **후보 B** (입자별 FE + 접촉) | 반례로서의 자리: 이 메시는 **상 단위** (같은 상 입자 융합 · 접촉면 없음) — 입자별 FE + 접촉이 아니다 · COMSOL '도메인 수천 개' 는 상별 연결 성분으로 읽힘 [카드 해석] | 입자 경계 · 접촉 요소 · 마찰 없음 |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 (서론이 비판한 '유효 기공 · 굴곡도로 CBD 를 지우는' 균질화는 전기화학 쪽 이야기) | — |
| **U0–U6** | **U1** (해상도 · 지름당 칸 수) 쪽: 축소 precision 의 비용 ↔ 정밀도 거래와 Fig. 3 의 정성 그림 · '해상도는 양날의 칼' 문장 — 수렴 시험이 없다는 반면교사 | 화소 크기 미기재 → 지름당 칸 수를 못 센다 · U0 · U2–U6 없음 |
| **R1–R7** | **R3** (SE 입자 경계 기억) 의 반례 — 상 코드 넘김은 입자 경계를 지운다 (같은 상 융합) · **R6** (형상 변형) — 영상 경로는 임의 형상을 받는다 (변형 입자를 넘긴 예는 없음) | R1 · R2 · R4 · R5 · R7 없음 |
| **결과 전 대조 항목** | 없음 — 외부 대조값 (물리 결과) 이 없다.  내부 점검 꼴 (상별 부피 < 2 % · 기공 두 값) 만 가져온다 | 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 액체 LIB NMC + CBD (SE 없음) · 3D · 압력 0 · CGMD 구조 단계 미기재 · 화소 크기 미기재 · 한 구조 한 번 — 우리 (LPSCl + NCM · 300 MPa · DEM / MPM / STEP3) 와 값으로 견줄 자리가 없고, **방법 · 점검 꼴**만 견준다.

## 9. 적용 인사이트 (행동)
1. **넘김 보존 점검 둘을 결과 전에 등록 (단계 0 · 단계 7)**: (가) 입자 → 격자 = 상별 표현 부피 ÷ 참 부피 (구 부피 합 / 합집합 명시) + 겹침 처리 규칙 (상 우선 · 부피 이동) (나) 격자 → 메시 · 해 = 상별 부피 보존 + 기공 두 값 + 매끄럽게 전후.  이 논문은 (나) 만, 우리 CL-25 원장은 (가) 만 한다.
2. **기공 보고 칸 하나 더 (단계 0)**: '기공을 센 자리 (격자 · 메시 · 매끄럽게 여부)' — 같은 구조에서 그들은 0.4 %p, 우리 겹침 부기 규약은 1.25–1.5 %p [우리] 흔들린다.
3. **부피 보존만으로는 모자란다 — 연결성 점검 (단계 7 · U1)**: 축소 · 해상도 변경 뒤 상별 연결 성분 수 · 관통 여부를 같이 본다 (Fig. 3 [판독]: 면적은 그대로인데 CBD 최대 조각 0.077 → 0.049).
4. **CF 표지 (흐름 밖: 수송)**: 상 코드 메시 · 복셀 위 수송 결과에는 'CONTACT_FREE (같은 상 접촉 저항 없음)' 를 붙인다 — 우리 STEP3 (CL-81) 와 같은 규약을 문헌 값에도 적용 (benhadjali · zhang2023 계열 COMSOL 결과를 읽을 때).
5. **겹침 규칙 출처를 바로잡아 인용**: "INNOV 이 겹친 구를 고체로 잇는다" 고 쓰지 않는다 — 그 사슬의 겹침 규칙은 benhadjali2025 · benhadjali2026 (한 방향) 본문 [다른 카드] 이다.
6. **흐름 밖 (3D COMSOL 넘김을 할 때)**: mphtxt + Selections 경로 · 6-사면체 분할 (정밀 · 요소 많음) ↔ 5 (요소 적음) · 축소 [4 4 3] 꼴의 비용 (요소 ≥ 1/27.6 · 시간 1/39.6) — 우리 격자 (STEP3 dof 수천만) 를 그대로 사면체화하면 ≈10⁸ 요소대 [카드 산술] → 축소 · 부분 영역이 불가피하고, 그 대가는 3 번 점검으로 잰다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "INNOV (Chouchane, Rucci and Franco, *ACS Omega* 4 (2019) 11141–11144) meshes all phases of a voxelized electrode at once — each pixel becomes a node coded by its phase and each voxel is split into tetrahedra, so that interface surface meshes coincide — and imports the result into COMSOL; for a CGMD-generated NMC electrode it reported 50.1 % porosity in the image stack versus 49.7 % in the mesh (50.07 % after smoothing) and per-phase volume errors below 2 %."
- "The conversion of particle centres and radii into the binary image stack is described only as 'a specific function' (Chouchane et al., 2019); rules for overlapping particles and the voxel size are not reported."
- 국문 (한정어와 함께): *"INNOV (Chouchane 2019) 는 이진 영상의 화소를 상 코드 노드로 삼아 모든 상을 한꺼번에 사면체로 메싱한다 — 같은 상 입자는 한 영역으로 융합되고 (접촉 저항 없음), 예시 전극에서 기공은 영상 50.1 · 메시 49.7 · 매끄럽게 50.07 % 였다.  겹친 구를 영상으로 바꾸는 규칙과 화소 크기는 원문에 없다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: ① 부피 보존은 평균 — *"cannot highlight local deformations within the mesh"* (p.2) ② 축소는 *"slightly losing in precision"* (p.3) ③ 매끄럽게 하면 요소 부피가 줄어 기공이 는다 (p.2) ④ 고해상도 영상은 *"a double-edged sword"* (p.3).
**카드가 본 한계**
1. **구 → 영상 규칙 없음** — 겹친 구 · 상 우선 · 복셀 안 판정 · 화소 크기 (µm) · 영역 크기 미기재.  세 정본 카드의 '겹침 · 복셀 크기 규칙의 원전' 기대가 원문과 다르다 (§0-1).
2. **물리 결과 없음** — PDE 해 · 수송 · 역학 · 실험 대조 없음.  '기하 온전성' 은 상별 부피 평균과 기공 두 값으로만 보였다.
3. **수렴 · 품질 없음** — 메시 수렴 · 요소 품질 · 계면 넓이 정확도 · 피복의 해상도 의존 미시험.
4. **한 구조 한 번** — 반복 · 다른 구조 · 오차 막대 없음 · Fig. 3 구조가 표 1 과 같은지 미기재.
5. **연결성 미점검** — Fig. 3 판독상 축소가 CBD 2D 조각을 쪼갠다 (면적은 그대로) — 원문은 연결성을 말하지 않는다.
6. **재료 · 목적 다름** — 액체 LIB NMC + CBD · SE 없음 · 압력 없음 · 예시 기공 ≈50 % (랩 표준과 다른 문헌 값).
7. **표기 어긋남** (§3-5): INNOV 풀이 두 벌 · 그림 번호 (S3 ↔ S2) · 'slide' · 'void' ↔ 'electrolyte' · 'Gb'.
8. **판독 한계**: Fig. 3 값 = 그림 화소 · 단면 하나 · 2D (부피 · 3D 연결성 아님) · 보라 테두리 띠의 뜻 미기재.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| (19) | Nielson, G. M.; Franke, R. Computing the separating surface for segmented data. Proceedings of IEEE Visualization 1997, Phoenix, USA; IEEE: 1997, 229−233. | ★ 이 알고리즘의 분리면 수학 (상이 섞인 칸의 네 경우 · 5 / 6 사면체) — 계면 면이 어디에 놓이는지의 원전 · 카드 없음 |
| (20) | Fang, Q.; Boas, D. A. Tetrahedral mesh generation from volumetric binary and gray-scale images. Proceedings of the Sixth IEEE international conference on Symposium on Biomedical Imaging: From Nano to Macro 2009; Boston, USA IEEE: 2009, 1142−1145. | Iso2Mesh — 영상 → 사면체 메싱의 다른 경로 (cronk2026 · zhang2026 이 직접 씀) · 카드 없음 |
| (10) | Ngandjong, A. C.; Rucci, A.; Maiza, M.; Shukla, G.; Vasquez-Arenas, J.; Franco, A. A. Multiscale Simulation Platform Linking Lithium Ion Battery Electrode Fabrication Process with Performance at the Cell Level. J. Phys. Chem. Lett. 2017, 8, 5966−5972. | ★ 예시 구조의 CGMD 원전 (구 배치 · 제조 단계) — 넘긴 시점 [미확인] 을 닫는 자리 · 카드 없음 (xu2023 카드가 ref [23] 으로 인용) |
| (16) | Rucci, A.; Ngandjong, A. C.; Primo, E. N.; Maiza, M.; Franco, A. A. Tracking variabilities in the simulation of Lithium Ion Battery electrode fabrication and its impact on electrochemical performance. Electrochim. Acta 2019, 312, 168−178. | 같은 CGMD 사슬 · 구조 변동의 전기화학 영향 · 카드 없음 (alabdali2023 카드가 [23] 으로 인용) |
| (7) | Mai, W.; Yang, M.; Soghrati, S. A particle-resolved 3D finite element model to study the effect of cathode microstructure on the behavior of lithium ion batteries. Electrochim. Acta 2019, 294, 192−209. | 입자 해상 3D FE 의 다른 메싱 선례 (경계 맞춤 쪽) — h · 후보 B 대조 · 카드 없음 |
| (12) | Hein, S.; Latz, A. Influence of local lithium metal deposition in 3D microstructures on local and global behavior of Lithium-ion batteries. Electrochim. Acta 2016, 201, 354−365. | 원문이 'CBD 를 AM 과 한 고체로 합친' 3D 모델의 예로 든 논문 · 카드 없음 |
| (뒤 논문 · 이 목록 밖) | Chouchane, Franco, Batteries & Supercaps 4 (2021) 1451–1456 (후보 표 N-73) | 같은 도구 (INNOV) 의 사용자 판 — benhadjali2026 의 [38] |

## 13. [미확인] 목록 (본문 4 쪽 + SI 4 쪽 전수에 없음)
1. 구 → 이진 영상 변환 규칙 (겹친 구 · 상 우선 · 복셀 안 판정 · 부분 부피).
2. 화소 크기 (scale factor 값) · 영역 크기 (µm) · 예시 구조의 제조 단계 (슬러리 · 건조 · 압연).
3. 예시에 쓴 분할 (5 / 6 사면체) · 매끄럽게 하기 설정 · 매끄럽게 하기 시간.
4. 'faces' 의 정의 · 피복 넓이 계산법 · 상자 바깥 면 처리.
5. 메시 수렴 · 요소 품질 · 계면 넓이 정확도.
6. Fig. 3 구조가 표 1 · Fig. 1 과 같은지 · 단면 위치 · 보라 테두리 띠의 뜻.
7. §4.2 의 201 × 200 × 179 예가 Fig. 1 구조와 같은지 (시간 · 축소가 같아 같다고 읽음 [카드 해석]).
8. COMSOL '도메인 수천 개' 의 단위 (연결 성분인지).
9. 호 번호.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-13)
- 본문 4 쪽 + SI 4 쪽을 글자 층 (PyMuPDF 쪽별 · 블록 · 줄 좌표) + 쪽 렌더로 읽음.  서지 = 본문 첫 쪽 (제목 · 저자 3 명 · 소속 4 곳 · *"Cite This: ACS Omega 2019, 4, 11141−11144"* · 접수 · 수락 · 출판일 · DOI · 라이선스) · p.4 (교신 · 감사 · 약어) · SI 첫 쪽 (같은 제목 · 저자).  원문 낱말 셈 (본문 · SI): 'overlap' 0 · 'sphere' 0 ('spherical' 1 = Fig. 1 캡션) · 'DEM' 0 · 'discrete' 0 · 'contact' 1 (p.1) · 'pressure' 0 · 'calender' 0 · 'plastic' 0 (본문 · 참고문헌 제목 1) · 'µm' 2 (반지름 둘) · 'resolution' 1.
- 그림 크롭 **29 장** = 도구 7 (Fig. 1–3 · 표 1 · SI Fig. S1–S3) — **fig_2 다시 자름** (그림 왼쪽 빈 여백 ≈93 pt) + 손 크롭 22 (초록 그림 1 · 패널 4 · 식 0 · 근거 문단 17).  내장 래스터 = 본문 그림 300 dpi (xref 40 · 209 · 211 · 212) · SI 그림 116–146 dpi (300 dpi 로 렌더) · SI Fig. S1 의 자동 크롭이 래스터 아래 1.1 pt 를 자르지만 그 줄은 흰색 (최솟값 ≥ 252) 이라 그대로 둠.  29 장 전부 Read 로 열어 확인.  `figures.json` 의 `recrop` · `manual_crop`.
- 판독: digitized.csv 10 행 — Fig. 3 왼쪽 · 오른쪽 단면의 상별 면적 몫 (세 색 최근접 · 흐린 경계 화소 2.9 %) · CBD 2D 연결 성분 (4 / 8 연결 같음 · ≥ 30 px) · 최대 조각 몫.  표 1 산술 (영상 % = 메시 % ÷ 보존) 이 본문 영상 기공 50.1 % 를 재현.
- 2 차 인용 대조: 정본 카드 benhadjali2026_wip (L165 · L262 · L289 · L450) · benhadjali2025 (L64 · L105 · L245 · L379) · benhadjali2026_fully (L110 · L248 · L404) · benhadjali2026_oneway (L82 · L243) · zhang2023 (L33 · L75 · L214 · L370) · ngandjong2021 (L277) — 고치지 않았다 (카드 문제 = 정독 출력 batch_84 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (chouchane* 없음 · 2026-11-13) + DOI (`acsomega.9b01279` · `11141`) · 제목 낱말 · 저자 (Chouchane · Rucci) grep — 카드 없음 (인용만: benhadjali2025 · benhadjali2026_wip · benhadjali2026_fully · zhang2023 (INNOV) · ngandjong2021 (INNOV)).  같은 제1 저자 · 같은 해의 다른 카드 없음.
- 그림 도구가 `figures/_sources.json` 의 남의 항목 (choi2018 · heenan2020 · 다른 한 항목의 pdfs 목록) 까지 바꿨다 → 되돌리고 이 카드 항목만 더함.

## 🔗 관련 카드
- **같은 도구 · 같은 사슬 (CGMD → 메싱 → COMSOL)**: `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` (겹침 우선 AM → SE → CBD 를 그 본문이 인쇄) · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (가리킨 카드 · 0.2 µm 복셀화 · §10-5) · `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` · `benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode` (CBD 겹침 부피 → AM / SE · [46]) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (CGMD 구조 원전) · `ngandjong2021_dem_calendering_digital_twin` (DEM 캘린더링 구조 → INNOV) · `xu2023_realistic_am_shape_cgmd_calendering` · `duquesnoy2020_calendering_ml_mesostructure_generator` (Chouchane = 코드 저자) · `dem_mechanical_stresses_ssb_electrode_cycling`.
- **영상 → 메시 · FE 넘김**: `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` (PFIB → INNOV ≈2.3 M 요소) · `cronk2026_lis_positive_electrode_geometry_fem` · `zhang2026_dryprocess_electrode_architecture_cell_level` (Iso2Mesh = 이 논문 ref (20) 계열).
- **복셀 넓이 · 기공 연산자**: `windreich2003_voxel_based_surface_area_estimation` · `lindblad2005_surface_area_weighted_local_configurations` · `ziegel2010_surface_area_measure_digitizations` (복셀 면 넓이 편향 — 이 논문의 피복 % 는 분리면 삼각형이라 면 세기와 다르지만 정확도는 미기재) · `taufactor_tortuosity_factor_tomography_tool` · `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` · `cottrino2013_insitu_xct_granulated_alumina_die_compaction` (영상 기공의 최소 크기 칸) · `choi2018_fibsem_3d_composite_cathode_microstructure_tpb_pore_decomposition`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
