<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-73 · 정독 112) 에서 꼭 뽑으라고 한 항목.
     본 = kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     가리킨 카드 = benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md (이 논문 = 그 논문 ref [38] · L165 · L262 · L449) · 같은 도구 (INNOV) 의 알고리즘 원전 = chouchane2019_innov_voxelization_multiphase_meshing.md (이 논문의 ref [11] = benhadjali2026 의 [39]).
     원문 = 출판본 (Batteries & Supercaps 2021, 4, 1451–1456 · 'Concepts' · 6 쪽) + Supporting Information (6 쪽 PDF = 표지 SI p.1 + 본문 SI p.2–6 · 쪽 번호 인쇄 없음) + 보충 영상 1 개 (inbox 'Sup2' mp4 · 267.8 s — 논문 · SI 어디에도 영상 언급이 없다).
     쪽 표기 = 본문 "p.n" = 인쇄 쪽 (PDF 쪽 n = 인쇄 1450 + n) · SI "SI p.n" = SI PDF 쪽 n.  크롭 파일 이름의 pN 과 figures.json 의 page 는 그 파일의 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI 의 글자로 적힌 값 · [그림 글자] = 래스터 그림 안의 글자 (GUI 화면 캡처 그림 1b · 2 · S3 · 흐름도 S2 · 표지) — 화면 한 상태의 입력 칸 값이지 '권장값' 이 아니다 ·
     [영상 관찰] = 보충 영상 프레임에서 본 화면 글자 · 순서 (시각 병기 · 재현 = figures.json 의 movies) · [판독] = 그림에서 읽은 값 (Fig. 5c 방전 곡선 — litdb/figures/<slug>/digitized.csv 42 행 ·
     내장 래스터 (xref 51 · 6686 × 3515 px) 화소를 곡선 색으로 나누고 축 눈금 (x 0–200 · y 3.2–4.2 V) 에 선형으로 맞춤 · 맞춤 잔차 x ≤ 0.022 mAh/g · y ≤ 0.0002 V · 선 굵기 ≈ 0.012 V) ·
     [카드 산술] = 인쇄 · 그림 글자 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 6 쪽 + SI 6 쪽 + 영상 어디에도 없음.
     원문 12 쪽은 글자 층 (PyMuPDF 줄 좌표 · 단 나눔) 전수 + 전 쪽 렌더 + 내장 래스터 확대로 읽었고, 영상은 15 s 간격 접촉 시트 (18 칸) + 전 해상도 정지 화면 13 장으로 봤다.
     이 논문은 **도구 소개 (Concept)** 다 — DEM · 입자 역학 · 압밀 · 하중 · 수렴 시험이 없고, 계산 결과는 COMSOL 반쪽 전지 방전 예시 하나 (모델 식 · 매개변수 미기재) 뿐이다. -->
# INNOV 웹 앱 — 3D 전지 부품 미세구조 (microstructure) 를 가져오거나 (영상 묶음 · MATLAB 행렬 · AM / CBD 구 좌표 → 슬라이싱) 확률적으로 만들어 (구 AM · 경계 규칙 d > r × α · AM–AM 겹침 목표 · PSD · 주기 경계 · 화소 단위로 자라는 CBD (w) · ASSB 용 기공 상 · 분리막 · 집전체) 2019 복셀화 알고리즘으로 다상 사면체 메시를 짜 COMSOL (.mphtxt + 선택 내장) · .bdf · .mat · .stl · .ply 로 넘기는 GUI 도구 — '압연' 은 겹침 ↑ · 기공 ↓ 의 기하 대리 (역학 없음) · 해상도 · Precision 은 사용자 몫 (수렴 규칙 없음) · 반쪽 전지 예 35³ µm³ · 기공 30 % · 겹침 20 vol% · ≈650 000 사면체 — Chouchane · Franco (Batteries & Supercaps 2021)

> slug `chouchane2021_innov_webapp_stochastic_generation_meshing` · DOI `10.1002/batt.202100096` · type `tool / Concept article — web-app GUI (INNOV, computed on the ARTISTIC project servers; reads and writes MATLAB matrices — the 2021 paper does not name the implementation language) that imports (image stack · native MATLAB matrix · AM + constant-radius CBD sphere coordinates → slicing at a user-set resolution) or stochastically generates (spherical AM with boundary rule d > radius × α, AM–AM overlap target, uniform / Gaussian / imported / built-in PSD, periodic cut at the box; voxel-scale CBD grown with morphology parameter w; extra void phase for ASSB; separators homogeneous / tomography-based / stochastic / filaments; homogeneous current collector and Li foil) 3D battery component structures and meshes them with the 2019 voxelization algorithm ([11] = chouchane2019) into multiphase tetrahedral meshes (finer at interfaces, coarser in the bulk; 'Precision' downsampling; Iso2mesh functions) exported as .mphtxt (COMSOL, built-in selections) · .bdf (Nastran) · .mat or surface .stl · .ply; whole structure as .tif (TauFactor · GeoDict) — demo: COMSOL NMC-111 half-cell discharge C/10 · 1C · 2C; no DEM, no mechanics, no mesh-convergence study` · PDF `757279e0-73._An_invitation_to_engage_with_computational_modeling_user_friendly_tool_for_in_silico_battery_component_generation_and_meshing.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **Mehdi Chouchane** (a, b) · **Alejandro A. Franco\*** (a, b, c, d) — a Laboratoire de Réactivité et Chimie des Solides (LRCS), UMR CNRS 7314, Université de Picardie Jules Verne, Hub de l'Energie (Amiens) · b Réseau sur le Stockage Electrochimique de l'Energie (RS2E), FR CNRS 3459 · c ALISTORE-European Research Institute, FR CNRS 3104 · d Institut Universitaire de France (Paris) — \* 교신 (alejandro.franco@u-picardie.fr) · *Batteries & Supercaps* **2021**, **4**, **1451–1456** · 머리글 'Concepts' · 호 = **9** (제목 옆 표지 기사 그림의 '9/2021' — 본문 서지 줄에는 호가 없다) · 원고 접수 2021-04-29 · 수정본 2021-06-02 · 승인 원고 온라인 2021-06-02 · 확정본 온라인 2021-06-17 · © 2021 Wiley-VCH GmbH · 연구비 = EU Horizon 2020 ERC grant **772873 "ARTISTIC"** · A.A.F. = Institut Universitaire de France · 이해 충돌 없음 · 키워드 3D modeling · battery · carbon binder domain · mesh · structure generation [인쇄 p.1451 · p.1456 · 그림 글자 표지].
> **이웃 카드 (링크만)**: [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (이 논문 = ref [38] · L165 · L262 · L449 — 가리킨 카드) · [`chouchane2019_innov_voxelization_multiphase_meshing`](chouchane2019_innov_voxelization_multiphase_meshing.md) (이 논문의 ref [11] = 메싱 알고리즘 원전 · 같은 1 저자 · 다른 해) · [`benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`](benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md) (이 논문 = ref [27] · L380) · [`benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode`](benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode.md) (ref [30] = 이 논문의 **표지 기사** 서지 · L403) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (이 논문의 ref [20]) · [`duquesnoy2020_calendering_ml_mesostructure_generator`](duquesnoy2020_calendering_ml_mesostructure_generator.md) (ref [9]) · [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) (ref [16]) · [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) (ref [7]).
> **판독 원자료**: `litdb/figures/chouchane2021_innov_webapp_stochastic_generation_meshing/digitized.csv` (42 행 — Fig. 5c 방전 곡선 세 개를 10 mAh/g 간격으로 + 3.2 V 축 끝 용량) · 그림 크롭 **35 장** (도구 8 → 전부 다시 자름 + 손 27 = 패널 7 · Fig. S1 1 · 식 1 (SI 식 1) · 표지 그림 1 · 근거 문단 15 · 영상 정지 화면 2) — `figures.json`.  **번호 붙은 식은 SI 식 (1) 하나뿐** (경계 규칙 d > radius × α) — 본문에는 식이 없다 (도구 소개 · 알고리즘은 2019 논문 [11] 에 맡김 · 생성 규칙은 흐름도 S2 와 SI 문장).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: INNOV 는 3D 전극 · 분리막 구조를 **(가) 단층 영상 묶음 · MATLAB 행렬 · '제조 모의 출력' 구 좌표 (x, y, z, radius) 로 가져오거나 (나) 내장 확률적 생성기 (구 AM · 경계 규칙 d > radius × α · AM–AM 겹침 목표 · PSD · 주기 경계 · 화소 단위 CBD 규칙 w · ASSB 기공 상) 로 만든 뒤** 구는 **사용자 해상도로 슬라이싱 (= 복셀화)** 해 2019 복셀화 메싱 [11] 으로 **모든 상을 한 번에 사면체 메시** (계면에서 잘고 덩어리에서 굵음 · 'Precision' 으로 요소 수 조절 · Iso2mesh 함수 재사용) 로 바꿔 **.mphtxt (COMSOL · 선택 내장) · .bdf · .mat · .stl · .ply · .tif** 로 내보내는 **서버 계산형 웹 앱** 이다 — 그러나 **구 → 화소 규칙 (겹친 구 · 상 우선 · 부분 부피) · 해상도 선택 규칙 · 메시 수렴 · 생성기의 기공 맞춤 방법은 원문에 없고**, '압연' 은 **겹침 ↑ · 기공 ↓ 라는 기하 대리** 일 뿐 역학이 없다.  benhadjali2026 이 쓴 **0.2 µm 등방 복셀화는 이 논문의 값이 아니다** (해상도는 사용자 선택 · 화면 기본값 0.25 · 0.33 · 0.5 · 1 µm [그림 글자 · 영상 관찰]).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 도구가 하는 일 — 단계별 | (1) **입력**: 영상 묶음 · MATLAB 행렬 · AM + CBD 구 좌표 (CBD 반지름 일정) → 슬라이싱 (2) **확률적 생성**: Dimension → 구 AM (α · 겹침 · PSD · 주기 경계) → CBD (w) → (선택) 기공 상 (ASSB) → 분리막 (균질 · 단층 영상 Celgard · Targray · 확률적 · 섬유) → 균질 집전체 · Li 박 (3) **메시**: 2019 복셀화 · 다상 · 계면 가늘게 · Precision · 3D 보기 (4) **내보내기**: 표면 .ply · .stl / 체적 .bdf · .mphtxt · .mat / 구조 .tif (5) 내장 예 셋 (반쪽 전지 · 전전지 · ASSB) · 서버 계산 · 사용 안내서 (GUI 안) — 단계별 = §4-1 | [인쇄] p.1451–1455 · SI p.2–6 · Fig. 1 · S2 · S4 |
| ② ★ 구 → 화소 (슬라이싱) 규칙 | *"an additional step is needed to convert them into a stack of images. Indeed, a slicing process takes place to generate the 3-D structure, with a resolution that can be modified by the user"* (SI p.5) — **그 밖 규칙 (구 중심 / 부분 부피 · 겹친 구 · 다른 상 겹침 우선) = 원문에 없음** · 구 좌표 가져오기는 **AM 과 반지름 일정 CBD 만** (SE 구 범주 없음) | [인쇄] p.1453 · SI p.5 · [미확인] |
| ③ ★ 해상도 · Precision · 요소 수 · 수렴 | 해상도 = 사용자 선택 (GUI 드롭다운: 그림 1b **0.25 µm** · 그림 2a **0.33 µm** · 영상 기본 **1 µm** · 영상 예 **0.5 µm** [그림 글자 · 영상 관찰]) · 요소 수 = 'Precision' (축마다 숫자 셋: 4·4·4 · 4·4·8 · 3·3·5 · 3·3·4) · 지침은 *"The precision should always be adapted to the size of the system, the characteristic length of the system, and to the computational power available"* 한 문장 · **메시 · 해상도 수렴 시험 없음** · 반쪽 전지 예 *"ca. 650 000 tetrahedrons"* (해상도 · Precision 값 미인쇄) · 화면 · 영상 로그: 100³ px → **192 777** 요소 (2 s) · 80×80×180 px → **204 378** (2 s) · 80×80×151 px → **416 975** (5 s) · 80×80×100 px → **313 874** (3 s) | [인쇄] p.1454–1455 · [그림 글자] Fig. 1b · [영상 관찰] |
| ④ ★ 상 · 계면 표지 | 상마다 색 → 상 (AM · CBD · Void · Separator · Li Foil · Cur. Coll.) 지정 (가져오기 칸) · *"indefinite number of domains in the mesh"* · COMSOL **.mphtxt 에 '선택 (selections)' 내장** · 계면 = 상 경계 (같은 상 입자끼리는 경계 없음 — 입자 번호를 싣지 않는다) [카드 해석 · 2019 카드와 같음] | [인쇄] p.1453–1454 · [그림 글자] Fig. 1b |
| ⑤ 확률적 생성 규칙 | **SI 식 (1)** d > radius × α (α = 1 → 모든 구가 상자 안 · 주기 없음 · α = 0 → 중심이 경계여도 받아들이고 잘린 반은 주기 경계로) · AM: 무작위 반지름 → 무작위 좌표 → 경계 규칙 → 겹침 규칙 → 받아들임 (실패하면 좌표 다시 · **10 000 번** 넘으면 반지름 다시) · 겹침 규칙: 총 겹침 > 목표면 '겹치는' 구 거절 · 아니면 '충분히 겹치는' 구만 · CBD: 무작위 전해질 **화소** 하나씩 → 고체와 맞닿아야 → CBD 와 맞닿으면 확률 ω · 아니면 1 − ω 로 받아들임 (흐름도) — ⚠ **SI 본문 (b) 의 w 서술과 규칙이 다르다** (§11) | [인쇄] SI p.2–3 · [그림 글자] Fig. S1 · S2 |
| ⑥ '압연' 의 표현 | *"to capture the structural changes upon a calendering process, with the AM particles being brought closer to each other, one can increase the AM-AM overlap and decrease the porosity to have a more packed structure"* — **겹침 % · 기공 % 를 입력으로 바꾼 확률적 구조** (Fig. 3c · d · 값 미인쇄) · 반쪽 전지 예 '압연 전극' = 기공 30 % + AM–AM 겹침 20 vol% · **역학 · 하중 · 입자 변형 없음 · 구는 겹칠 뿐 모양이 안 바뀐다** | [인쇄] p.1453 · p.1455 |
| ⑦ ASSB | GUI 에 'ASSB' 칸 · 'Example: ASSB' 단추 [그림 글자] · *"An option to generate an additional "void" phase, particularly relevant for all-solid-state batteries"* · 내장 예 = NMC · CBD · 고체전해질 + **기공 10 %** 반쪽 전지 + 자동으로 붙는 **SE 분리막 20 µm · 기공 15 %** — 고체전해질 재료 · SE 상을 만드는 규칙 · 기공 상 알고리즘 [미확인] · 이 값들은 **입력** (측정 · 압밀 결과 아님) | [인쇄] p.1453 · p.1455 |
| ⑧ 계산 예 (COMSOL 반쪽 전지) | 35×35×35 µm³ · AM 94 wt% · 실험 PSD NMC-111 · CBD 막 · 5 µm 균질 분리막 (기공 안 풀음) · 암묵 Li 박 · ≈650 000 사면체 · 우리 그룹 반쪽 전지 모델 [6, 19, 20] · C/10 · 1C · 2C → 3.2 V 축 끝 용량 **183.5 · 129.4 · 96.1 mAh/g** [판독] (2C/C10 = 0.52 [카드 산술]) · 2C 끝 리튬화 지도에서 *"the solid diffusion can be identified as the limiting phenomenon"* · 모델 식 · 매개변수 · 실험 대조 [미확인] | [인쇄] p.1455 · Fig. 5 · [판독] Fig. 5c |
| ⑨ 식 | **SI 식 (1) 하나** (경계 규칙) — 메싱 · 전기화학 식 없음 (메싱 = [11] · 전기화학 = [6, 19, 20] 에 맡김) · 겹침 규칙 · CBD 규칙은 흐름도 · 문장으로만 (수식 없음) | [인쇄] SI p.2 |
| ⑩ 저자 한계 · 앞으로 | *"several new features such as the generation of non-spherical particles, CBD with PSD, or adding a separate app to perform basic image segmentation will be considered in the future"* → **지금은 구 입자 · CBD 크기 분포 없음 · 분할 기능 없음** · 반쪽 전지 예의 분리막 기공은 *"not resolved since the impact of the separator is out of the scope"* | [인쇄] p.1455–1456 |
| ⑪ benhadjali2026 [38] 서술과 같은가 | **같다** — '자체 INNOV [38] · 복셀 메싱 [39] → COMSOL' (L165) · 'Franco 그룹의 미세구조 생성 · 메싱 도구 [38] (복셀 기반 다상 메싱 [39])' (L262) · 서지 (L449) 모두 원문과 맞음 · **0.2 µm 등방 복셀화는 benhadjali2026 자기 설정** (이 논문에 0.2 µm 없음) | §0-1 |

⛔ **한정어 (떼지 말 것)**: ① **도구 소개 (Concept)** — 정량 검증 · 수렴 · 실험 대조가 없다 ② 예시 구조 = **액체 LIB NMC-111 + CBD** (ASSB 예는 기능 소개 한 문단 · 재료 미상) ③ **해상도 · 슬라이싱 규칙 · 생성기의 기공 맞춤 방법 = [미확인]** — 그 결과 이 도구로 만든 구조의 기공 · 피복 · 연결성이 해상도에 얼마나 기대는지 이 논문으로는 알 수 없다 ④ 'calendered' 구조 = 기하 대리 (겹침 · 기공 입력) — **압밀 결과로 읽지 않는다** ⑤ GUI 화면 · 영상의 수치는 **그 화면 한 상태** (예: 그림 1b 의 Generate 칸 30 µm @ 0.25 µm = 120 칸인데 표시된 구조는 가져온 100³ px 행렬 [카드 산술]).
⇒ **절대값 전이**: 0 건 (재료 · 해상도 · 목적이 다르다).  **전이 가능한 것** = (i) 입자 모의 → 복셀 → FE 메시 넘김의 **단계 구성과 빠진 칸** (슬라이싱 규칙 · 해상도 규칙 · 입자 번호 · 수렴) (ii) 화소 단위로 자라는 상 (CBD) 은 **해상도가 곧 그 상의 형상 척도** 라는 구조적 사실 [카드 해석] (iii) 메시 크기 · 시간 감각 (0.64–1.15 M 화소 → 0.19–0.42 M 사면체 · 2–5 s · 서버 [그림 글자 · 영상 관찰]) (iv) .tif → TauFactor · GeoDict 로 tortuosity factor (= 우리 tau2 · 수송 tortuosity) 를 잴 수 있는 출구.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-73 의 '왜' 칸)

의도 원문: *"넘김 도구 (h 이웃) — "INNOV" · benhadjali2026 의 넘김 = 0.2 µm 등방 복셀화 → INNOV [38] · 복셀 메싱 [39] (L165 · L262)"* · 가리킨 카드 = `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (L449 · L165 · L262) · 지시서 덧붙임: 도구가 하는 일 (구조 가져오기 · 확률적 생성 · 메시 알고리즘 · 내보내는 형식 · 상 / 계면 표지 · 해상도 한계) 을 단계별로 · 식이 없으면 이유 · 우리 쪽 대응 (DEM → MPM 스캐폴드 · STEP3 복셀 격자 — 계단 표면 · 격자 의존) 을 이 도구가 어떻게 다루는지.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "넘김 도구 (h 이웃)" | **채움 (도구로서)** | SI Fig. S4 = *"Workflow to achieve a volumetric mesh from spheres coordinates input in INNOV"* — '(x,y,z,radius) · Manufacturing Simulation Output' → *Slicing* → 'Binary segmented images' → *Meshing* → 'Volumetric Mesh' [그림 글자] · SI p.5 *"With spheres coordinates, either they arose from manufacturing simulation or from the AM in INNOV's embedded stochastic generation algorithm, an additional step is needed to convert them into a stack of images"* · p.1453 가져오기 꼴 셋.  **단 'DEM' · 'CGMD' · 'LAMMPS' 낱말 0 회** — '제조 모의' 가 무엇인지 · 넘기는 시점 (슬러리 · 건조 · 압연 어디) · 넘기는 자료 = **위치 · 반지름 · 상 뿐** (힘 · 접촉 · 입자 번호 · 이력 없음) [카드 해석] |
| "INNOV" (낱말) | **채움** | *"INdefinite Number Of phases meshing through Voxelization" (INNOV)* — 2019 [11] 에 보고한 메싱 알고리즘, *"Since then, this algorithm has been deeply improved with several new features that have been implemented into a graphic user interface (GUI)"* (p.1451) · *"INNOV is a Web App freely accessible through our ARTISTIC project website [13]"* · *"All the computation will be performed in the project servers"* (p.1453) |
| "benhadjali2026 의 넘김 = 0.2 µm 등방 복셀화" | **없음 (이 논문 값 아님)** | 이 논문에 0.2 µm 없음 · 해상도는 *"a resolution that can be modified by the user"* (SI p.5) · GUI 'Resolution (µm)' 칸은 **값 하나** (그림 1b 0.25 · 그림 2a 0.33 · 영상 1 · 0.5) [그림 글자 · 영상 관찰] → 정육면체 화소 = '등방' [카드 해석] · 메시 'Precision' 은 **축마다 숫자 셋** (4·4·4 · 4·4·8 · 3·3·5 · 3·3·4) = 메시 거칠게 하기는 비등방 가능 [그림 글자 · 영상 관찰] ⇒ 0.2 µm 는 benhadjali2026 의 선택 (그 카드 L165 [인쇄 p.21]) |
| "→ INNOV [38]" (서지) | **채움** | L449 서지 = 원문 첫 쪽 · 머리글과 같음 (저자 둘 · 제목 · Batteries & Supercaps 4 (2021) 1451–1456 · DOI 10.1002/batt.202100096) · 원문에만 있는 것 = 머리글 'Concepts' · 호 9 (표지 기사 그림) |
| "· 복셀 메싱 [39]" | **일부 (원전에 맡김)** | p.1454 *"The meshing algorithm used in INNOV is based on the voxelization approach published by us in a previous article [11]"* (= benhadjali2026 의 [39] = 정본 `chouchane2019_*`) — 노드 · 사면체 분할 · 섞인 칸 경우 · 중복 노드 제거 · 매끄럽게 하기 = **이 논문에 없음** [다른 카드 chouchane2019 §4].  이 논문이 더한 것 = *"elements finer at the interface between materials and coarser in the bulk"* · 'Precision' · Iso2mesh [18] 재사용 · 내보내기 형식 |
| L262 "INNOV: Franco 그룹의 미세구조 생성 · 메싱 도구 [38]" | **채움** | 제목 *"… In Silico Battery Component Generation and Meshing"* · 확률적 생성 (p.1453 · SI 1) + 메싱 (p.1454) |
| L165 "… · 자체 INNOV [38] · 복셀 메싱 [39] → COMSOL" | **채움** | *"INNOV facilitates the importation of the mesh to COMSOL Multiphysics® by using its native format .mphtxt into which built-in selections are embedded"* (p.1454) · GeoDict 는 이 논문에서 **.tif 를 받는 바깥 소프트웨어** (*"TauFactor [16] or GeoDict® [17] to calculate tortuosity factors"* p.1454) — INNOV 의 일부 아님 · PoreSpy 언급 없음 |
| (지시서) 단계별 — 구조 가져오기 · 확률적 생성 · 메시 알고리즘 · 내보내는 형식 · 상 / 계면 표지 · 해상도 한계 | **채움 (알고리즘 내부 · 슬라이싱 규칙 제외)** | §4-1 단계표 · 가져오기 (p.1453) · 생성 (p.1453 · SI 1 · Fig. S2) · 메시 (p.1454) · 형식 (p.1454) · 상 지정 (Fig. 1b 가져오기 칸 [그림 글자]) · 해상도 (SI p.5 · p.1455 한 문장) |
| (지시서) 식 | **일부 — 식 하나** | SI 식 (1) `d > radius × α` 만 (크롭 `eq_S1_alpha_boundary_acceptance.png`) · 이유 = 도구 소개 글 · 메싱 알고리즘은 [11] · 전기화학 모델은 [6, 19, 20] 에 맡김 · 생성 규칙 둘 (겹침 · CBD) 은 흐름도 (Fig. S2) 와 문장으로만 |
| (지시서) 우리 쪽 대응 — 계단 표면 · 격자 의존을 다루는가 | **없음 (다루지 않음)** | 메싱 정의가 *"without deforming the original geometry"* (p.1451) = 복셀 기하를 그대로 넘김 [카드 해석] · 이 논문에 매끄럽게 하기 언급 0 회 (2019 원전에는 선택 기능 · 기공 +0.38 %p [다른 카드 chouchane2019 §3-3]) · 판 보기 · 렌더에 계단이 그대로 (Fig. 1b · 3 · 5a · 영상) · 해상도 · 수렴 규칙 없음 (§0 ③) · CBD 는 **화소 하나씩** 자란다 → 그 형상 척도 = 화소 (§3-5) |

**2 차 인용 대조 (가리킨 카드 · 이웃 카드)**:
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` **L449** (서지) — 원문과 같음 ✓ (호 · 'Concepts' 만 없음).  *"카드 없음 — INNOV"* 칸은 이 카드로 해소 (그 카드는 고치지 않음).
- 같은 카드 **L165** · **L262** — 원문과 맞음 ✓ (위 표).
- 같은 카드 **L251** *"넘김: 0.2 µm 복셀 → 메시 — 겹친 구의 공통 부피는 한 번만 세어진다 (복셀 기하의 성질 [추정]) · 계면 = 복셀 면"* — 이 논문에는 '계면 = 복셀 면' 에 해당하는 문장이 없고 *"elements finer at the interface"* 만 있다 · 메싱 원전은 상이 섞인 칸을 **분리면 (Nielson–Franke 경우) 으로 잘라** 사면체를 만든다 [다른 카드 chouchane2019 L12 · §4] → **'계면 = 복셀 면' 은 원전과 어긋날 수 있다 — 카드 문제 (경미 · 고치지 않음 · 정독 출력 끝 절).**
- `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` **L380** ([27] · *"Batt. Supercaps 4 (9) (2021) 1451–1456"*) — 원문과 같음 ✓ (호 9 = 표지 그림과 맞음).
- `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` **L403** ([30] = *"Cover Feature: … (Batteries & Supercaps 9/2021), Batteries & Supercaps 4 (2021) 1375–1375. https://doi.org/10.1002/batt.202100202"*) — 이 PDF 에는 표지 기사 그림만 있고 그 기사의 쪽 · DOI 는 인쇄돼 있지 않다 → **표지 기사 서지 확인 = [미확인]** (그 카드가 이미 '본 논문 = 10.1002/batt.202100096' 이라고 구분해 두었다 ✓).
- `chouchane2019_innov_voxelization_multiphase_meshing` L300 (*"뒤 논문 · 이 목록 밖 … Batteries & Supercaps 4 (2021) 1451–1456 (후보 표 N-73) | 같은 도구 (INNOV) 의 사용자 판"*) — ✓.

⇒ **의도 대조 결과: 일부** — '넘김 도구 INNOV 의 원전 (무엇을 받아 무엇을 내는가 · 단계 · 형식 · 상 표지)' 은 **채움**; '0.2 µm 등방 복셀화' 는 **이 논문 값이 아님 (benhadjali2026 의 선택)** · 메시 알고리즘 세부는 **2019 원전 [11] 에 맡김 (일부)** · 슬라이싱 규칙 · 해상도 · 수렴 · 계단 표면 처리는 **없음**.

---

## 1. 한 줄 요약
배터리 모델링 논문이 지난 30 년 전체의 20 % 미만 (Web of Science · 2021-04-19 · 'battery' 와 'battery modeling') 인 이유를 '전기화학자 밖의 전문성 (단층 영상 없이 미세구조 만들기 · 메싱)' 으로 보고, 2019 년에 낸 복셀화 다상 메싱 알고리즘 INNOV 를 **인터넷 브라우저로 쓰는 무료 GUI 웹 앱** (계산은 ARTISTIC 서버) 으로 키워 소개한다 — 영상 · 행렬 · 구 좌표를 가져오거나 구 AM + 화소 CBD + (ASSB) 기공 + 분리막 · 집전체를 확률적으로 만들고, 모든 상을 한 번에 사면체 메시로 짜 COMSOL · Nastran · MATLAB · STL · PLY · TIF 로 내보낸다.  내장 예 셋 (NMC-111 반쪽 전지 · 전전지 · ASSB 반쪽 전지) 가운데 반쪽 전지는 COMSOL 방전 (C/10 · 1C · 2C) 까지 보여 준다.  압연은 겹침 · 기공 입력으로 흉내 내고, 해상도 · Precision 은 사용자에게 맡기며, 비구형 입자 · CBD 크기 분포 · 영상 분할은 앞으로 할 일이다.

## 2. 메타
| 저자 | 저널 / 년 | DOI | 소재 | 연구 유형 |
|---|---|---|---|---|
| M. Chouchane · A.A. Franco\* (LRCS · RS2E · ALISTORE-ERI · IUF) | Batteries & Supercaps 4 (2021) 1451–1456 · 9 호 · 'Concepts' · 6 쪽 + SI 6 쪽 + 영상 1 | 10.1002/batt.202100096 | **도구** — 예시 = 액체 LIB NMC-111 양극 (+ CBD · 분리막 · Li 박) · 전전지 · ASSB 반쪽 전지 (NMC · CBD · 고체전해질 (재료 미상) · 기공) | 도구 소개 + 내장 예 + COMSOL 방전 예시 하나 — **DEM · 역학 · 실험 없음** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. GUI 화면의 칸 · 값 (그림 1b · 2 · S3 + 영상) [그림 글자 · 영상 관찰]
| 칸 | 그림 1b | 그림 2a | 영상 t ≈ 5 s (빈 화면) | 영상 t ≈ 30 s ('Example: Full Cell' · 음극 칸) | 영상 t ≈ 210–240 s (양극 칸) |
|---|---|---|---|---|---|
| Alpha | 0 | 0 | 0 | 0.1 | 0.1 |
| Overlap (%) | 10 | 10 | 10 | 30 | 30 |
| Porosity (%) | 30 | 30 | 30 | 35 | 35 |
| AM weight ratio (%) | 90 | 90 | 90 | 92 | 92 |
| AM density (g/cm3) | 4.65 | 4.65 | 4.65 | 2.26 | 4.65 |
| Radius min · max (µm) | 2 · 4 | 2 · 4 | 2 · 4 | (Advanced PSD) | (Advanced PSD) |
| Dimension (µm) | 30 · 30 · 30 | 30 · 30 · 30 | 30 · 30 · 30 | 40 · 40 · 40 | 40 · 40 · 40 |
| Stochastic CBD w (단위 칸) | 0.5 (voxel) | 0.5 (voxel) | 0.5 (voxel) | 0.75 (voxel) | 1 (voxel) |
| Resolution (µm) — 생성 | **0.25** | **0.33** | **1** | **0.5** | **0.5** |
| Advanced PSD | 꺼짐 | 꺼짐 (그림 2b: 가우스 평균 5 · 표준편차 1 · 하한 3.5 · 상한 7.8 µm) | 꺼짐 | 켬: 가우스 평균 4 · 표준편차 2 · 2–8 µm (반지름) | 켬: 평균 6 · 표준편차 2 · 3–8 µm |
| ASSB 칸 | 꺼짐 | 꺼짐 | 꺼짐 | 꺼짐 | 꺼짐 |
| Separator | (Type of Separator) | — | 'Separator Options' w 0 (pixel) | Homogeneous · 10 µm | Celgard PP · 10 µm |
| Thickness CC · Li Foil (µm) | 0 · 0 | — | 0 · 0 | 0 · 0 | 0 · 0 |
| 메시: Decomposition · Resolution · Precision | 5 · 0.25 µm · 4 4 4 | — | 5 · 1 µm · (빈칸) | 5 · 0.5 µm · 4 4 8 | 5 · 0.5 µm · 3 3 4 |
| 'Structure' 칸 | 100 × 100 × 100 pixels · 3 phases | — | — | 80 × 80 × 180 pixels · 4 phases | 80 × 80 × 100 pixels · 4 phases |
- 가져오기 칸 (그림 1b): 'Load xyz file' (회색) · 'Load Images' · 'Load 3D Matrix' · 'Finalize' · 상 지정 AM · CBD · Void · Separator · Li Foil · Cur. Coll. ('Choose Color') · 'Crop' x · y · z (1 to 100) · 'Generate Mesh' · 'Save Mesh' · 'Save Structure as Images' · 'Save Mesh as Matrice' · 예 단추 'Example: Half-cell · Full Cell · ASSB' · 'Documentation' [그림 글자].
- 분리막 종류 (그림 S3): **Targuay PE** (화면 오타 — 본문 'Targray®') · Celgard PP · Homogeneous · Stochastic · Filaments · Crossed Filaments · 두께 (µm) [그림 글자].
- 영상 GUI 의 참고문헌 칸: [1] Chouchane, Rucci, Franco ACS Omega (2019) · [2] Chouchane, Rucci, …, Franco JPS (2019) · [3] Shodiev, Primo, Chouchane …, Franco JPS (2020) [영상 관찰 t ≈ 45 s].
- ⚠ [카드 산술] 그림 1b 의 Generate 칸 (30 µm @ 0.25 µm → 120 칸) ≠ 표시된 구조 100 × 100 × 100 px — 로그 *"Matrix is being imported … Matrix was imported"* 대로 **표시된 구조는 가져온 행렬** 이다 (Generate 칸 값과 무관).  그림 1b ↔ 그림 2a 의 생성 해상도도 다르다 (0.25 ↔ 0.33 µm · 다른 화면).
- [카드 산술] 영상 전전지 예: 80 칸 × 0.5 µm = 40 µm (전극 Dimension 과 같음) · 180 칸 = 40 + 10 (분리막) + 40 µm ✓ · 양극만 + Celgard 10 µm = 80 × 80 × 100 ✓.
- 'Decomposition 5' · 'All ▼' · 'voxel ▼' / 'pixel ▼' 드롭다운의 뜻 = **원문 설명 없음** [미확인] — 'Decomposition' 은 2019 원전의 '정육면체 → 사면체 5 개 또는 6 개' 선택일 수 있다 [카드 해석 · 다른 카드 chouchane2019].

### 3-2. 내장 예 셋 (p.1455 · `txt_p5_halfcell_example_30pct_20pct_overlap_650k_tets.png` · `txt_p5_fullcell_assb_examples_void_10_15pct.png`) [인쇄]
| 예 | 구성 | 수치 | 메시 · 계산 |
|---|---|---|---|
| ① 반쪽 전지 (양극) | 암묵 Li 박 (*"i.e. no thickness considered"*) · NMC-111 (실험 PSD) · CBD = NMC 를 덮는 막 · 5 µm 균질 분리막 (*"The pores in the separator were not resolved"*) | **기공 30 %** · **AM–AM 겹침 20 % (in volume)** (*"To simulate a calendered electrode"*) · **35 × 35 × 35 µm³** · **AM 94 wt%** | Precision *"slightly refined to reach a mesh composed of ca. 650 000 tetrahedrons"* · COMSOL 반쪽 전지 모델 [6, 19, 20] · **C/10 · 1C · 2C** 방전 · 해상도 · Precision 값 [미확인] |
| ② 전전지 | 양극 = 균일 PSD · 균질 분리막 · 음극 AM = 사용자 가우스 PSD (*"more realistic than a uniform distribution"*) | 값 인쇄 없음 (영상의 'Example: Full Cell' 화면 = §3-1 [영상 관찰]) | 메시만 (전기화학 계산 언급 없음) |
| ③ ASSB 반쪽 전지 | NMC · CBD · **고체전해질** + 기공 · 그 위에 **고체전해질 분리막 자동 추가** | 전극 **기공 10 %** · SE 분리막 **20 µm · 기공 15 %** | 언급 없음 · 고체전해질 재료 · SE 상 생성 규칙 [미확인] |

### 3-3. 메시 크기 · 시간 (원문 · 화면 · 영상)
| 출처 | 구조 (화소) | 해상도 | Precision | 요소 (사면체) | 걸린 시간 | 요소 / 화소 [카드 산술] |
|---|---|---|---|---|---|---|
| 반쪽 전지 예 (p.1455) | 35³ µm³ (화소 수 [미확인]) | [미확인] | "slightly refined" | **≈650 000** [인쇄] | [미확인] | — |
| 그림 1b 로그 [그림 글자] | 100 × 100 × 100 = 1 000 000 | 0.25 µm (메시 칸) | 4 · 4 · 4 | **192 777** | 17:29:10 → 17:29:12 (≈2 s) | 0.193 |
| 영상 t ≈ 45 s [영상 관찰] | 80 × 80 × 180 = 1 152 000 (전전지) | 0.5 µm | 4 · 4 · 8 | **204 378** | 14:16:49 → 14:16:51 (≈2 s) | 0.177 |
| 영상 t ≈ 72–85 s | 80 × 80 × 151 = 966 400 (양극 칸에서 Crop z 10–60 = 51 칸 → 80 + 20 + 51 [카드 산술] · 다시 메시) | 0.5 µm | 3 · 3 · 5 | **416 975** | 14:17:29 → 14:17:34 (≈5 s) | 0.431 |
| 영상 t ≈ 240 s | 80 × 80 × 100 = 640 000 (양극 + Celgard 10 µm) | 0.5 µm | 3 · 3 · 4 | **313 874** | 14:20:11 → 14:20:14 (≈3 s) | 0.490 |
- [카드 산술] 거친 칸 수 (각 축 화소 ÷ Precision 의 곱) 로 나누면 칸당 **12.3 · 22.7 · 19.4 · 17.7** 사면체 — 정육면체 하나를 사면체 5–6 개로 쪼개는 것보다 많다 → 원문의 *"elements finer at the interface … coarser in the bulk"* 와 맞는 크기 [카드 해석].  Precision 숫자가 작을수록 (3 < 4) 요소가 는다 (0.18 → 0.43–0.49 / 화소).
- 생성 시간 [영상 관찰]: 80 × 80 × 80 px 양극 생성 14:18:24 → 14:18:33 (≈9 s) · Celgard PP 분리막 14:18:58 → 14:19:13 (≈15 s) · w = 1 로 양극 다시 14:19:40 → 14:19:49 (≈9 s) — 서버 계산.
- 비교 [다른 카드 chouchane2019 §3-2]: 2019 원전 예 201 × 200 × 179 화소 · precision [4 4 3] → 1 737 665 요소 · 4.48 s (축소 없이 > 48 M · 177.20 s).

### 3-4. 방전 곡선 — Fig. 5c [판독 · digitized.csv]
| 용량 (mAh/g) | C/10 (V) | 1C (V) | 2C (V) |
|---|---|---|---|
| 10 | 4.20 | 4.00 | 3.89 |
| 25 · 30 | 4.06 (30) | 3.81 (30) | 3.70 (30) |
| 50 | **3.94** | **3.72** | **3.63** |
| 75 · 80 | 3.82 (80) | 3.64 (80) | 3.51 (80) |
| 100 | 3.77 | 3.58 | — |
| 120 | 3.74 | 3.47 | — |
| 150 | 3.68 | — | — |
| 170 | 3.62 | — | — |
| **3.2 V 축 끝 용량** | **183.5** | **129.4** | **96.1** |
- 첫 전위 (용량 ≈1 mAh/g): C/10 4.29 V · 1C · 2C 는 처음 몇 mAh/g 에서 가파르게 떨어져 선 굵기로 가를 수 없다 (윗 축 끝 = 4.31 V [판독]).
- [카드 산술] 용량 유지 1C / C/10 = **0.705** · 2C / C/10 = **0.524**.  끝 용량은 '3.2 V 축 바닥' 에서 읽었다 — 차단 전압이 3.2 V 라는 문장은 원문에 없다 [미확인].
- Fig. 5d (2C 끝 리튬화): 색 막대가 없어 값을 읽을 수 없다 · 원문 해석 = *"the solid diffusion can be identified as the limiting phenomenon because of the steep Li concentration gradient in the NMC"* (p.1455).
- 반쪽 전지 모델의 식 · 확산계수 · 전도도 · 교환전류 · 온도 = **[미확인]** ([6, 19, 20] 에 맡김) · 실험 곡선 대조 없음.

### 3-5. ★ 확률적 생성 규칙 (SI p.2–4 · 그림 S1 · S2 · `txt_si_p2_p3_alpha_boundary_rule_periodic_cut.png` · `txt_si_p3_w_cbd_pixel_probability_rule.png`)
- **SI 식 (1)** `d > radius × α` — *"A particle can be accepted if the distance d between its center and the closest electrode boundary follows"* [인쇄 SI p.2] · 그림 S1: (a) α = 0.5 받아들임 · (b) α = 1 거절 [그림 글자].
  - *"with α = 1, all the particles will be inside the electrode boundaries and no periodic conditions would be applied since no sphere is intersected by an electrode boundary"* · *"With α = 0, the particles can be accepted even if the center is on an electrode boundary, meaning that such particle would be cut in half, with the other half inserted with periodic boundary conditions"* [인쇄 SI p.3] · 본문: *"For particles that are intersected by the boundaries of the box, periodic boundary conditions are applied to have a more realistic representative volume"* (p.1453).
- **AM 흐름 (그림 S2 위 칸)** [그림 글자]: Random radius r → Random coordinates (x,y,z) → 'Is (x,y,z) inside the system?' (아니면 좌표 다시) → 'Distance to boundaries > r x α' (아니면 좌표 다시) → 'Overlap rule respected?' → 예 = Accepted / 아니오 = 'Iteration < 10000' 이면 좌표 다시 · 아니면 반지름 다시.
- **겹침 규칙 (그림 S2 가운데)** [그림 글자]: 'Is the total overlap > overlap target?' — 예 → 'Is the current particle overlapping?' (예 = Rejected · 아니오 = Accepted) / 아니오 → 'Is the current particle overlapping enough?' (예 = Accepted · 아니오 = Rejected).  본문: *"based on the overall AM-AM overlap"* (p.1453) · 반쪽 전지 예 *"20% (in volume) of overlap between AM particles"* (p.1455).  **'겹침 %' 의 분모 (AM 부피? 상자?) · '충분히 겹침' 의 문턱 · AM 배치를 멈추는 조건 (기공 목표? AM wt% + 밀도?) = [미확인]**.
- **CBD 흐름 (그림 S2 아래)** [그림 글자]: 'Select a random electrolyte pixel' → 'Is this pixel in contact with solid?' (아니오 = 다시 고르기) → 'In contact with CBD?' → Yes: 확률 **ω** 로 Accepted · 1 − ω 로 다시 / No: 확률 **1 − ω** 로 Accepted · ω 로 다시.
- **SI 본문 (b) Parameter w** [인쇄 SI p.3]: *"The value of w varies between 0 (film) and 1 (aggregate) and reflects the probability that a new location for CBD will be randomly generated if the previous one was in contact with AM. Indeed, at each iteration a pixel of electrolyte is randomly chosen, if this pixel has not as a neighbor at least one pixel of AM, then there is a probability 1 - w that this pixel of electrolyte will not be converted to CBD."*
  - ⚠ **두 규칙이 다르다** [카드 해석]: 본문 = 'AM 이웃이 없는 화소는 확률 1 − w 로 거절 (w 로 받아들임)' · 흐름도 = '고체 (solid) 와 맞닿지 않으면 늘 거절 · 맞닿으면 CBD 이웃 여부로 ω / 1 − ω'.  기호도 w (본문) ↔ ω (흐름도).  w = 0 막 · w = 1 덩어리 라는 **방향** 은 흐름도 쪽과 맞는다 (ω = 1 → CBD 옆에만 붙음 = 덩어리 · ω = 0 → CBD 옆이 아닌 고체 표면에만 = 막).  CBD 양 (멈추는 조건) · CBD 밀도 [미확인].
  - ★ **CBD 는 '화소 하나' 단위로 자란다** [인쇄 SI p.3 · 그림 글자] → CBD 의 형상 척도 = 해상도 그 자체 [카드 해석] (그림 3 · 5a · 영상의 노란 칸이 모두 한 화소 블록).  GUI 'voxel ▼' 드롭다운의 다른 선택지는 [미확인] · 구 좌표 가져오기에서는 CBD 가 반지름 일정한 구 (p.1453).
- 분리막: 균질 · 단층 영상 (Celgard® · Targray® [14, 15]) · CBD 와 같은 알고리즘의 확률적 · 섬유 (p.1453–1454 · 그림 S3) — 단층 영상 분리막을 전극 해상도에 맞추는 규칙 [미확인].

### 3-6. 가져오기 · 내보내기 · 상 표지 (p.1453–1454 · SI p.5 · `txt_p3_import_images_matrix_spheres_slicing.png` · `txt_p4_meshing_precision_iso2mesh_export_formats.png` · `txt_p3_p4_separator_collectors_tif_taufactor_geodict.png`)
| 단계 | 원문 | 표지 |
|---|---|---|
| 가져오기 | *"as a stack of images, as a matrix with the native MATLAB format, or, for the case of electrodes for instance, as a list of the coordinates and radii of AM and CBD spheres, with the CBD having a constant radius. For the latter, an additional slicing step will be required"* | [인쇄] p.1453 |
| 슬라이싱 | 구 좌표 (제조 모의 · 내장 생성) → 영상 묶음 · *"with a resolution that can be modified by the user"* | [인쇄] SI p.5 |
| 상 지정 | 가져오기 칸에서 색 → AM · CBD · Void · Separator · Li Foil · Cur. Coll. | [그림 글자] 그림 1b |
| 메시 | 2019 복셀화 [11] · *"indefinite number of domains"* · 계면 가늘게 · 덩어리 굵게 · 'Precision' · 3D 보기 · *"The mesh 3D rendering as well as several other functions were reused from Iso2 mesh [18]"* | [인쇄] p.1454 |
| 내보내기 | 표면 **.ply · .stl** · 체적 **.bdf · .mphtxt · .mat** · COMSOL 고유 **.mphtxt 에 built-in selections 내장** · *".bdf (Nastran) format is accepted by most software"* · *".mat format allows the user to convert it to its desired format"* · 구조 전체 **.tif** → *"TauFactor [16] or GeoDict® [17] to calculate tortuosity factors"* | [인쇄] p.1454 |
| 처음 목적 | *"to ease the importation of volumetric multiphase meshes into COMSOL Multiphysics® (each phase being a different material or porous media) by its native format and embedded domain selections"* | [인쇄] p.1453 |
- 내보내는 것 = **상 라벨 기하** (+ COMSOL 선택) — 입자 번호 · 접촉 · 힘 · 응력 · 생성 이력 = 없음 [카드 해석 · 2019 카드와 같음].  선택이 도메인만인지 경계까지인지는 이 논문에 없다 (2019 원전 = 도메인 · 경계 *"typically thousands"* [다른 카드]).

### 3-7. 보충 영상 (inbox 'Sup2' · 267.8 s · 1340 × 918 · 48 fps · 소리 트랙 무음 −91 dB) [영상 관찰]
논문 · SI 어디에도 영상 언급이 없다 — 이 영상의 소속은 inbox 파일 이름뿐이다.  내용 = INNOV 웹 앱 화면 녹화 (말 · 자막 없음):
1. t ≈ 0–20 s: 빈 GUI (해상도 1 µm 기본) → 'Example: Full Cell' 누름 → 전전지 생성.
2. t ≈ 30–50 s: 80 × 80 × 180 px · 4 상 · Precision 4·4·8 → 204 378 요소 (≈2 s) · 3D 렌더 (전극 AM 빨강 · CBD 노랑 · 분리막 초록) — `vid_S2_t30s.png` · `vid_S2_t45s.png`.
3. t ≈ 60–90 s: 양극 z 를 잘라 (Crop z) 80 × 80 × 151 px → Precision 3·3·5 → 416 975 요소 (≈5 s).
4. t ≈ 120–190 s: 지우고 양극만 생성 (80 × 80 × 80 px · 3 상 · ≈9 s) → Celgard PP 분리막 10 µm (≈15 s · 80 × 80 × 100 px).
5. t ≈ 200–265 s: w = 1 로 양극 다시 (≈9 s) → Precision 3·3·4 → 313 874 요소 (≈3 s) · 3D 렌더 (덩어리 CBD + 분리막).
- 판 보기의 모든 구 경계와 CBD 는 0.5 µm 화소 계단이고, 메시 렌더는 계면에서 요소가 잘다 [영상 관찰].

---

## 4. ★ 방법 — 도구가 하는 일 · 알고리즘 · 계산 예

### 4-1. ★ 도구가 하는 일 — 단계별 (의도의 핵심)
| # | 단계 | 입력 → 출력 | 규칙 · 매개변수 | 원문 | 빠진 것 |
|---|---|---|---|---|---|
| 1 | 구조 가져오기 | 영상 묶음 · MATLAB 행렬 → 3D 상 배열 | 색 → 상 지정 · Crop | p.1453 · 그림 1b | 영상 분할 기능 없음 (앞으로) |
| 1′ | 구 좌표 가져오기 | AM + CBD (반지름 일정) 구 목록 → **슬라이싱** → 영상 묶음 | 해상도 = 사용자 | p.1453 · SI p.5 · 그림 S4 | 구 → 화소 규칙 · 겹친 구 · 상 우선 · **SE 구 범주** [미확인] |
| 2 | 확률적 생성 — 상자 | Dimension (µm) | — | p.1453 · 그림 2a | — |
| 3 | 〃 — AM 구 | 반지름 (균일 2 한계 · 가우스 · 목록 · 내장 NMC-111 · 구형 흑연) → 좌표 → 경계 규칙 (SI 식 1 · α) → 겹침 규칙 (총 겹침 목표) · 10 000 번 | 주기 경계 (경계에 걸린 구) | p.1453 · SI p.2–4 · 그림 S2 | 겹침 % 정의 · 멈춤 조건 [미확인] |
| 4 | 〃 — CBD | 전해질 화소를 하나씩 CBD 로 (w · ω) | 막 (0) ↔ 덩어리 (1) | p.1453 · SI p.3 · 그림 S2 · 3a–b | 본문 ↔ 흐름도 규칙 불일치 · 양 · 밀도 [미확인] |
| 5 | 〃 — 기공 상 (ASSB) | 'void' 상 추가 | — | p.1453 · p.1455 | 알고리즘 [미확인] |
| 6 | 〃 — 분리막 · 집전체 · Li 박 | 균질 · 단층 영상 · 확률적 · 섬유 / 균질 판 | 두께 (µm) | p.1453–1454 · 그림 S3 | 단층 영상 분리막의 크기 맞춤 [미확인] |
| 7 | 메시 | 상 배열 → 다상 사면체 | 2019 복셀화 · Precision · (Decomposition) · Iso2mesh | p.1454 · 그림 4 | 수렴 · 요소 품질 · 매끄럽게 하기 언급 없음 |
| 8 | 내보내기 | 메시 → .mphtxt (선택 내장) · .bdf · .mat · .stl · .ply / 구조 → .tif | — | p.1454 | 입자 번호 · 접촉 없음 |
| 9 | (밖) 계산 | COMSOL 전기화학 · 수송 · TauFactor · GeoDict tortuosity | [6, 19, 20] · [16] · [17] | p.1454–1455 | 모델 식 · 매개변수 [미확인] |

### 4-2. 메시 알고리즘 — 이 논문이 말한 것 / 원전에 맡긴 것
- 이 논문: *"The meshing algorithm used in INNOV is based on the voxelization approach published by us in a previous article [11]. This algorithm enables to have an indefinite number of domains in the mesh with elements finer at the interface between materials and coarser in the bulk. The number of elements in the mesh can be controlled through the "Precision" parameter"* (p.1454) · 메싱 정의 *"Meshing is the way to divide the component mesostructure into finite elements (usually tetrahedrons) without deforming the original geometry"* (p.1451).
- 원전 [11] 의 내용 (화소 = 상 코드 노드 · 이웃 두 장의 4 + 4 노드 정육면체 → 사면체 · 상이 섞인 칸 = Nielson–Franke 분리면 경우 · Iso2mesh 중복 노드 제거 · 선택 Kroon 매끄럽게 하기 (기공 49.69 → 50.07 %) · precision = 축마다 'N 개 중 하나' 노드) = [다른 카드 `chouchane2019_innov_voxelization_multiphase_meshing` §3–4] — **이 논문에는 다시 적혀 있지 않다**.
- ⇒ 이 논문만 읽고는 계면이 복셀 면인지 잘린 면인지 · 매끄럽게 하기를 켰는지 알 수 없다 [카드 해석].

### 4-3. 계산 예 — COMSOL 반쪽 전지 (p.1455 · 그림 5)
- 구조: 반쪽 전지 예 (§3-2 ①) → 메시 ≈650 000 사면체 → COMSOL 로 가져가 *"a half-cell model similar to those already reported by our group [6, 19, 20]"* · C/10 · 1C · 2C 방전 → 율이 낮을수록 용량 ↑ (Fig. 5c) · 2C 끝에 NMC 안 리튬 농도 기울기가 가파름 → 고체 확산 지배 (Fig. 5d).
- 숫자는 판독뿐 (§3-4).  모델 식 · 매개변수 · 경계 조건 · 실험 검증 = **[미확인]**.

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — 본문 · SI 에 'DEM' · 'discrete' · 'LAMMPS' · 'CGMD' 0 회.  입자 모의는 *"manufacturing simulation"* (SI p.5 · 그림 S4) 로만 나오고, 인용 [20] (Ngandjong 2021 · 정본 `ngandjong2021_dem_calendering_digital_twin` = DEM 캘린더링) 은 '반쪽 전지 모델' 출처로만 쓰인다.
- **(ii) 소성 · 큰 변형 = 다루지 않음** — 입자는 **구** (*"the AM particles are considered as spheres"* p.1453 · 비구형 = 앞으로 p.1456) · '압연' = **AM–AM 겹침을 늘리고 기공을 줄인 확률적 구조** (p.1453 · Fig. 3c–d) — 구가 서로 파고들 뿐 모양 · 부피 보존 흐름 · 응력이 없다.  우회 비용 = 0 (역학을 안 푼다) · 맞춘 값 = 겹침 % · 기공 % 를 입력으로 [카드 해석].
- **(iii) 차원** — 전부 **3D** (*"time dependent 3D-resolved computational modeling"*) · 판 보기 (xy · xz · yz) 는 화면용 2D 단면일 뿐 · 2D → 3D 전이 진술 없음.
- **(iv) 탈압** — 다루지 않음.

### 4-5. 기법 미니 용어집
- **INNOV** = *"INdefinite Number Of phases meshing through Voxelization"* — 상 수에 제한 없는 복셀화 메싱 (2019) + 이 논문의 GUI 웹 앱.
- **슬라이싱 (slicing)** = 구 좌표를 정해진 해상도의 영상 (화소) 묶음으로 바꾸는 단계 = 복셀화.
- **확률적 생성 (stochastic generation)** = 무작위 배치로 구조를 만드는 일 — 같은 입력에도 매번 다른 출력 (p.1451).
- **α (Alpha)** = 경계에 가까운 구를 받아들이는 문턱 (d > radius × α) · 0 = 주기 경계로 잘라 넣기 · 1 = 모두 상자 안.
- **w (ω)** = CBD 형태 매개변수 — 0 막 · 1 덩어리 (화소 단위 성장 확률).
- **Precision** = 메시 요소 수를 정하는 축별 숫자 셋 (클수록 거칠게) — 원전의 '축마다 N 개 중 하나 노드' [다른 카드].
- **선택 (selection)** = COMSOL 에서 도메인 (· 경계) 묶음 — .mphtxt 에 넣어 두면 상별 물성 지정이 쉬워진다.
- **.bdf (Nastran)** = 여러 FE 소프트웨어가 읽는 체적 메시 형식 · **.mphtxt** = COMSOL 고유 메시 형식.
- **tortuosity factor** (TauFactor · GeoDict 가 내는 양) = 우리 명명 **tau2 (수송 tortuosity)** — √ 값 아님 (CLAUDE.md τ 규약 표 [우리]).

---

## 5. Figure set ★
| 그림 | 내용 | 크롭 | 우리 활용 |
|---|---|---|---|
| Fig. 1a | 입력 셋 (단층 영상 · 확률적 생성 · 구 좌표) → INNOV → 체적 메시 | `fig_1.png` · `fig_1a.png` | 넘김 그림 (보고서 · 단계 7) |
| Fig. 1b | GUI 전체 — 가져오기 (빨강) · 전극 생성 (파랑) · 메시 (초록) · 로그 192 777 요소 | `fig_1b.png` | §3-1 화면 값 · 판 보기의 화소 계단 |
| Fig. 2a | 'Generate Electrode' 칸 (해상도 0.33 µm) | `fig_2.png` · `fig_2a.png` | 생성 매개변수 목록 |
| Fig. 2b | 'Advanced PSD' 가우스 (평균 5 · 표준편차 1 · 3.5–7.8 µm 반지름) | `fig_2b.png` | PSD 입력 꼴 |
| Fig. 3a–b | 막 CBD (w = 0) ↔ 덩어리 CBD (w = 1) 판 보기 | `fig_3.png` · `fig_3ab.png` | ★ 화소 단위 첨가 상 (CL-25 와 같은 부류 — §7-3) |
| Fig. 3c–d | 압연 전 ↔ 뒤 (겹침 ↑ · 기공 ↓ · 값 없음) | `fig_3cd.png` | ★ '압연 = 기하 대리' 의 반면교사 |
| Fig. 4 | 양극 메시 3D 렌더 (NMC 빨강 · CBD 노랑) | `fig_4.png` | 계단 표면이 메시에 그대로 |
| Fig. 5 | 반쪽 전지 전체 흐름 (생성 → 메시 → 방전 → 리튬화) | `fig_5.png` | 흐름 밖 (전기화학 예시) |
| Fig. 5c | 방전 곡선 C/10 · 1C · 2C | `fig_5c.png` | [판독] 183.5 · 129.4 · 96.1 mAh/g |
| Fig. S1 | α 규칙 (0.5 받아들임 · 1 거절) | `fig_S1.png` (손 · 캡션은 SI p.3) | 식 (1) 그림 |
| Fig. S2 | 확률적 생성 흐름도 (AM · 겹침 규칙 · CBD) | `fig_S2.png` | ★ 생성 규칙 원문 (§3-5) |
| Fig. S3 | 분리막 종류 팝업 | `fig_S3.png` | — |
| Fig. S4 | 구 좌표 (제조 모의 출력) → 슬라이싱 → 이진 영상 → 메싱 → 체적 메시 | `fig_S4.png` | ★ 넘김 경로 (h) |
| SI 식 (1) | d > radius × α | `eq_S1_alpha_boundary_acceptance.png` | 유일한 식 |
| 표지 그림 | Batteries & Supercaps 9/2021 Cover Feature | `ga_cover_feature.png` | 호 = 9 의 근거 |
| 영상 정지 화면 | t = 30 s (전전지 설정 · 80 × 80 × 180 px · 판 보기) · t = 45 s (전전지 메시 · 204 378 요소) | `vid_S2_t30s.png` · `vid_S2_t45s.png` | 해상도 · Precision · 요소 수 짝 |
| 근거 문단 15 | 초록 · 문헌 몫 · 확률적 정의 · 메싱 정의 · 목적 · 가져오기 · 생성 · 압연 대리 · 분리막 · .tif · 메시 · 예 셋 · 결론 · α · w · 슬라이싱 | `txt_p*.png` · `txt_si_*.png` | 원문 인용용 |
- 그림 크롭은 도구 관례대로 **캡션 제외** (캡션은 `figures.json`).  원문에 **표 없음**.  도구가 만든 8 장은 머리글 줄 · 내려받기 도장 · 옆 단 글 · 고르지 않은 여백 · (S3) 팝업 아래 절반 잘림 때문에 전부 다시 잘랐다 (`recrop` · `auto_bbox` 보존).

## 6. Post-processing ★
- **무엇을 (원문)**: 판 보기 · 3D 렌더 (GUI) · COMSOL 방전 곡선 · 리튬화 지도 · (밖) TauFactor · GeoDict tortuosity.
- **안 한 것**: 메시 · 해상도 수렴 · 요소 품질 · 생성 구조의 기공 · 겹침 · 피복 · 연결성 측정 · 실측 구조와의 대조 · 생성 반복 산포 (같은 입력 다른 출력의 크기) · 실험 방전 대조.
- **이 카드의 후처리**: Fig. 5c 래스터 판독 42 점 (`digitized.csv`) · 화면 · 영상 로그로 요소 / 화소 · 칸당 사면체 · 생성 시간 · 화소 수 ↔ 두께 대조 · d / 화소 (지름당 칸 수) 산술 (§7-3).  재현 스크립트 = 작업 스크래치 (`fig5_digitize.py` · `fig5_csv.py` · `recrop.py` · `txtcrop.py`) — 값은 csv 와 이 카드에 있다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 (INNOV) | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 넘김의 출발 | 구 좌표 (x, y, z, radius) — '제조 모의 출력' 또는 내장 생성 · AM + 반지름 일정 CBD | LIGGGHTS 덤프 (AM 2 크기 + SE 구) → MPM 스캐폴드: AM = 격자 장애물 (`--am-scaffold`) · SE = DEM 중심마다 구 (`--se-dump` · 비 AM 칸 합집합 · real_14 SE 32 832 개) [우리 · CLAUDE.md] | 같은 꼴 (구 → 화소) · **SE 구 범주가 INNOV 가져오기에 없다** → ASSB 구조는 바깥에서 먼저 복셀화 (benhadjali 들이 한 일 [다른 카드]) |
| 구 → 화소 규칙 | '슬라이싱' 한 문장 · 해상도 = 사용자 · 겹친 구 · 상 우선 [미확인] | AM 우선 (SE 는 비 AM 칸만) · 구 스탬프 d / 화소 ≥ 2 관문 · 점 스탬프는 표현 부피가 해상도에 따라 4.31 → 0.238 배 (CL-25) [우리 · CLAUDE.md] | 우리는 규칙과 그 오차를 **잰다** · INNOV 원문은 규칙을 적지 않는다 |
| 해상도 · 수렴 | 사용자 선택 (0.25–1 µm 화면) · Precision · 수렴 시험 없음 | MPM d_h / dx ≳ 3.5 (SE 응력) · STEP3 σ_e 격자 스윕 = 점 스탬프 vox 0.4 → 0.25 µm 에서 비가 계속 움직이고 (CL-24) 구 스탬프 0.15 → 0.115 µm 에서 이득이 단조 증가 · 멱법칙 외삽 불성립 (CL-41) · '하한' 이라 부르지 않음 (CL-72) — 격자 수렴 미확인 [우리 · CLAUDE.md] | 둘 다 '격자 의존' 문제를 가진다 — INNOV 는 말하지 않을 뿐 |
| 계단 표면 | 복셀 기하 그대로 메시 (*"without deforming the original geometry"*) · 매끄럽게 하기 언급 없음 | STEP3 복셀 FV = 계단 면 그대로 · MPM 복셀 인접 피복 (~26 %) 은 격자에 묶여 보고하지 않음 [우리 · CLAUDE.md] | 같은 부류 — 계면 넓이 · 피복 · 협착이 계단에 묶인다 |
| 계면 · 입자 번호 | 상 라벨만 · 같은 상 입자 융합 | STEP3 도 상 라벨 → 같은 상 면 = 계면 항 0 (CONTACT_FREE · CL-81) · Rint ② 는 SE 입자 번호가 필요 (① 상 경계 → ② VGCF 번호 → ③ SE 번호) [우리 · CLAUDE.md] | 같은 한계 — **입자 번호를 실어 나르지 않는 넘김은 SE–SE 계면 저항을 못 싣는다** |
| 압밀 | 겹침 % · 기공 % 입력 (기하 대리) | DEM 접촉 역학 (E_eff 1.35 GPa · 18 배 연화 · Heckel P_y 138 MPa) + MPM 소성 (E 1.53 · σ_y 0.30 GPa · ν 0.49) [우리 · CLAUDE.md] | INNOV '압연' 구조의 기공은 **결과가 아니라 입력** |
| 수송 해법 | COMSOL FE (사면체 · 계면 가늘게) · (밖) TauFactor · GeoDict | 접촉망 Kirchhoff + Holm (DEM) · STEP3 복셀 FV (MPM 격자 · 균일 화소) [우리] | 같은 상 융합이면 둘 다 CF 부류 · 메시 세분 유무만 다름 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이 · **이 논문의 값은 측정이 아니라 생성기 입력** — 랩 표준과 다른 문헌 값의 자리)
| 출처 | 재료 | 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 반쪽 전지 예 | NMC-111 94 wt% + CBD (막) · 액체 LIB 전해질 공간 | 생성기 입력 ('압연 모사' = AM–AM 겹침 20 vol%) | AM 밀도 · CBD 밀도 [미확인] (화면 기본 AM 4.65 g/cm³) | **30 %** (입력) |
| 이 논문 ASSB 예 | NMC + CBD + 고체전해질 (재료 미상) | 생성기 입력 | [미확인] | 전극 **10 %** · SE 분리막 **15 %** (입력) |
| 영상 'Example: Full Cell' | 양극 (AM 밀도 4.65 g/cm³) · 음극 (2.26 g/cm³) [영상 관찰] | 생성기 입력 | 화면값 | **35 %** (입력) |
- 압력 · 측정 조건이 없는 **입력값** 이라 랩 표준과 맞다 · 틀리다를 가를 수 없다.  나란히 놓을 수 있는 뜻은 하나 — '기공 10 % · 15 % 의 ASSB 구조' 를 이 도구는 **압밀 없이** 만든다는 것 (우리 순수 SE 랩 표준 10–13 % 와 같은 범위의 수를 생성 입력으로 쓴다).

### 7-3. ★ 우리 넘김 (DEM → MPM 스캐폴드 · STEP3 복셀 격자) 과 같은 자리 — 이 도구는 그 문제를 어떻게 다루나
1. **계단 표면** — 다루지 않음.  이 논문의 메싱은 *"without deforming the original geometry"* = 복셀 기하 보존이고, 매끄럽게 하기 언급이 없다 → COMSOL 의 계면 넓이 · 피복은 화소 계단을 그대로 물려받는다 [카드 해석].  (2019 원전의 선택 매끄럽게 하기는 기공을 +0.38 %p 바꾼다 [다른 카드].)  우리 STEP3 도 같은 계단 위에서 FV 를 푼다 → '계단 넓이 편향' 은 둘의 공통 문제 (정본 `windreich2003_*` · `lindblad2005_*` · `ziegel2010_*` = 복셀 면 넓이 편향 카드 [다른 카드]).
2. **격자 의존** — 다루지 않음.  해상도 · Precision 을 사용자에게 맡기고 지침은 '크기 · 특성 길이 · 계산 능력에 맞추라' 한 문장 (p.1455).  [카드 산술] 화면 기본값의 지름당 칸 수 (d / 화소): 반지름 2–4 µm @ 0.25 µm → **16–32** · @ 0.33 µm → **12–24** · 영상 기본 @ 1 µm → **4–8** · 영상 가우스 2–8 µm @ 0.5 µm → **8–32** — AM 은 우리 구 스탬프 관문 (d / 화소 ≥ 2) 과 MPM 해상 규칙 (d_h / dx ≳ 3.5 [우리]) 을 넘는 설정이지만, **CBD 는 화소 하나로 정의된다** (지름당 칸 수가 1 — 해상도를 바꾸면 CBD 의 형상 · 연결성이 바뀐다) [카드 해석].  우리 CL-25 (SDCP 점 스탬프의 표현 부피가 해상도에 따라 18.1 배 변동) 와 **같은 부류** 의 결함을 생성 규칙 자체가 갖는다.
3. **구 → 화소 규칙** — 적혀 있지 않다 (겹친 구 · 상 우선 · 부분 부피).  우리 쪽은 AM 우선 · SE 합집합 · 구 스탬프 (참 지름) 를 규약으로 두고 표현 부피 비 (0.986 등) 를 잰다 [우리] — INNOV 를 쓰는 다른 논문 (benhadjali) 의 기공 · 피복을 읽을 때 **그 논문이 스스로 적은 복셀화 규칙** (0.2 µm · 겹침 부피 이동) 을 봐야 한다 [다른 카드 benhadjali2025 · 2026].
4. **입자 번호** — 싣지 않는다 (상 라벨 메시).  우리 R3 (SE 입자 경계 기억) · Rint ② (SE 번호 → SE–SE 계면 저항) 의 반례 — 같은 상 입자는 메시에서 하나로 녹는다 [카드 해석 · 2019 카드와 같음].
5. **계면 가늘게 · 덩어리 굵게** — 우리 STEP3 (균일 화소 FV) 에는 없는 기능.  같은 화소 수에서 요소를 0.18–0.49 / 화소 로 줄인다 (§3-3) — 우리가 STEP3 격자를 FE 로 넘길 일이 생기면 쓸 수 있는 '계면만 해상' 방식의 선례 (수렴 근거는 없음).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 구조 생성 (확률적) · 복셀 → 다상 FE 메시 · 형식 내보내기 = **넘김 층** 하나.
- **없는 것**: DEM 의 반쪽 (접촉망 · 힘 사슬 · 패킹 · 퍼콜레이션 계산) 도, MPM 의 반쪽 (소성 형상 변화 · 공극 메움 · 응력장) 도 없다.  ⇒ 우리 계획에서 이 논문은 **어느 모델의 입력도 아니고**, 단계 7 (형상 · 피복 · 수송) 로 넘기는 다리의 **설계 점검표** (규칙 · 해상도 · 번호 · 수렴을 적었는가) 로 쓴다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) **복셀화 연산자를 연산자의 일부로 등록해야 하는 이유의 예** — 이 도구는 구 → 화소 규칙과 해상도를 적지 않아, 같은 구 목록이 해상도마다 다른 기공 · 피복 · CBD 형상을 낼 수 있다 [카드 해석] (2) 생성기 '기공' = **입력 목표** (30 · 35 · 10 · 15 %) — 결과 기공과 섞지 않는다 (3) .tif 로 내보내 TauFactor · GeoDict 로 tortuosity factor (= tau2) 를 잴 수 있다 — 결과 전 대조 칸에 **'어느 복셀화 · 어느 해상도의 .tif 인가'** 를 같이 적는다 | 압력 · 순수 SE · 진밀도 분모 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각: 0.64–1.15 M 화소 → 0.19–0.42 M 사면체 · 2–5 s (서버) [그림 글자 · 영상 관찰] · 35³ µm³ 반쪽 전지 ≈650 000 사면체 [인쇄] | 입자별 속도장 · 장 수와 무관 |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 (SE 압밀 없음) | — |
| **단계 5** (3D 복합 압밀) | 반면교사 하나: '압연' 을 **겹침 ↑ · 기공 ↓ 입력** 으로 흉내 낸 구조 (Fig. 3c–d) — 우리 DEM δ 겹침 대리 · ε_sphere 관례와 겉모양은 같지만 힘의 균형이 없다 → 그런 구조의 기공 · 겹침을 압밀 결과처럼 대조하지 않는다 | 역학 · 압력 · 응력 없음 |
| **단계 6** (탈압) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ (1) **넘김 경로의 원형**: 구 좌표 → 슬라이싱 → 상 영상 → 다상 사면체 (계면 가늘게) → .mphtxt (선택) / .bdf → COMSOL 전기화학 (§4-1) (2) 내보내는 것은 상 라벨 기하뿐 → 같은 상 접촉 저항 0 (CF 부류 · CL-81) · 입자 번호 없음 (3) CBD 화소 규칙 → 첨가 상의 형상 = 해상도 (4) Fig. 5c 방전 예 (액체 LIB · 흐름 밖) | 수렴 · 계면 넓이 정확도 · 피복 정의 없음 |
| **후보 D0** (지금 DEM) | 우리 덤프 (x, y, z, r, 상) 는 INNOV 가 받는 '제조 모의 출력' 꼴과 같다 — 단 **SE 구 범주가 없어** ASSB 덤프는 바깥 복셀화가 먼저 [카드 해석] | DEM 언급 0 회 |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 (MPM 없음) · 다만 '다상 한 메시' 는 우리 MPM 한 속도장 격자와 같은 위상 (상 구분만 · 입자 구분 없음) [카드 해석] | — |
| **후보 B** (입자별 FE · MPFEM) | **반대 근거** — INNOV 메시는 상 단위라 같은 상 입자가 한 도메인으로 녹는다 → 입자별 FE 의 메시원으로 쓸 수 없다 [카드 해석] | — |
| **후보 C · C′ · M0** | 없음 | — |
| **U1** (입자 하나 · 지름당 칸 수) | 화면 기본값의 d / 화소 4–32 [카드 산술] · '해상도 · Precision 은 크기 · 특성 길이 · 계산 능력에 맞추라' 한 문장 — 정량 규칙 없음 | 수렴 시험 없음 |
| **U6** (조밀 충전 해상도 수렴) | 없음 — **수렴을 재지 않은 도구** 라는 사실 자체가 우리 U6 의 필요를 뒷받침한다 | — |
| **U0 · U2–U5** | 없음 | — |
| **R3** (SE 입자 경계 기억) | 반례: 상 라벨 메시는 입자 경계를 지운다 | — |
| **R6** (SE 형상 변형) | 없음 — 구뿐 (비구형 = 앞으로) | — |
| **R1 · R2 · R4 · R5 · R7** | 없음 | — |
| **결과 전 대조 항목** | 없음 (흐름 밖 표지로만: Fig. 5c 액체 LIB NMC-111 반쪽 전지 C/10 · 1C · 2C 끝 용량 183.5 · 129.4 · 96.1 mAh/g [판독]) | ASSB 비교 금지 |

- **재료 · 차원 · 조건 차이**: 액체 LIB NMC-111 + CBD (예시) ↔ 우리 ASSB NCM811 + LPSCl · 3D (같음) · 압력 · 역학 없음 ↔ 300 MPa 압밀 · 생성기 입력 기공 ↔ 우리 결과 기공.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **넘김의 규칙을 넘김 산출물에 같이 싣는다** — INNOV 는 구 → 화소 규칙 · 해상도 · Precision 을 결과물에 적지 않는다.  우리 DEM → MPM 스캐폴드 · STEP3 · (앞으로) FE 넘김 매니페스트에 **상 우선 · 겹침 처리 · 해상도 · d / 화소 · 표현 부피 비** 를 칸으로 둔다 (단계 0 · 7).
2. **SE 구를 받는 넘김은 우리가 정의한다** — INNOV 가 받는 구는 AM + 반지름 일정 CBD 뿐 (p.1453).  ASSB 덤프 (AM + SE 구) 를 FE 로 넘길 때 복셀화는 우리 규약 (AM 우선 · SE 합집합 · 구 스탬프) 으로 먼저 하고 그 산출물을 메싱에 넘긴다 — benhadjali 의 0.2 µm · 겹침 부피 이동이 그 예 [다른 카드].
3. **화소 단위로 자라는 상은 해상도가 형상 척도다** — CBD 를 전해질 화소 하나씩 바꾸는 규칙 (SI p.3 · 그림 S2) 은 해상도를 바꾸면 같은 부피에서도 형상 · 연결성이 바뀐다.  우리 STEP3 첨가제 (SDCP · PTFE · VGCF) 를 화소 단위로 찍는 모든 규약에 같은 위험이 있다 (CL-25) — 구 스탬프 (참 지름 · d / 화소 ≥ 2) 나 해상도 사다리로 다룬다 (흐름 밖: Rint ② · STEP3 첨가제 표현).
4. **기하 '압연' 구조를 압밀 결과로 읽지 않는다** — 겹침 % · 기공 % 를 입력으로 넣은 구조 (Fig. 3c–d · 반쪽 전지 예) 는 힘의 균형이 없다.  INNOV 계열 구조 위의 수송 결과를 우리 압밀 구조와 견줄 때 '그 구조가 역학으로 나왔는가 (CGMD · DEM) · 생성기로 나왔는가' 를 먼저 적는다.
5. **.tif → TauFactor 를 τ 교차 점검 출구로** — 같은 복셀 구조를 .tif 로 내보내 TauFactor 의 tortuosity factor (= 우리 tau2) 와 STEP3 복셀 FV 의 tau2 를 견주는 길이 표준 도구로 열려 있다 (흐름 밖: τ 규약 · `taufactor_tortuosity_factor_tomography_tool`).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "INNOV (Chouchane and Franco, *Batteries & Supercaps* 4 (2021) 1451–1456) is a free web application, computed on the ARTISTIC project servers, that imports (image stacks, MATLAB matrices, or AM and constant-radius CBD sphere coordinates, which are sliced at a user-chosen resolution) or stochastically generates battery component structures and meshes all phases at once into tetrahedral meshes — finer at interfaces, coarser in the bulk, controlled by a 'Precision' parameter — exported as .mphtxt (with built-in COMSOL selections), .bdf, .mat, .stl or .ply."
- "In INNOV's generator, calendering is represented geometrically — 'one can increase the AM-AM overlap and decrease the porosity to have a more packed structure' (p. 1453) — e.g. a 35 × 35 × 35 µm³ NMC-111 half-cell with 30 % porosity and 20 vol% AM–AM overlap meshed into ca. 650 000 tetrahedra (p. 1455); no mechanics is solved."
- "The carbon-binder domain is grown pixel by pixel (SI, Fig. S2), so its morphology is defined at the voxel scale of the chosen resolution (card interpretation)."
- 국문: *"INNOV 는 구 좌표 · 영상을 받아 사용자 해상도로 복셀화한 뒤 모든 상을 한 번에 사면체 메시로 짜 COMSOL 등으로 넘기는 도구다 — 슬라이싱 규칙 · 해상도 수렴은 원문에 없다 (Chouchane & Franco 2021)."*
- 국문 (금지 표지): *"Chouchane & Franco 2021 을 '0.2 µm 등방 복셀화' 의 출처로 인용하지 않는다 — 그 값은 benhadjali2026 의 설정이다.  이 논문의 'calendered' 구조를 압밀 계산 결과로 인용하지 않는다 — 겹침 · 기공 입력이다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **도구 소개 · 검증 없음** — 메시 · 해상도 수렴 · 요소 품질 · 생성 구조의 통계 (같은 입력 다른 출력의 산포) · 실험 대조가 없다.
2. **슬라이싱 규칙 미기재** — 구 중심 / 부분 부피 · 겹친 구 · 다른 상 겹침 우선 · 화소 크기의 기본값.
3. **생성기의 핵심 정의 미기재** — 'overlap %' 의 분모 · '충분히 겹침' 의 문턱 · AM 배치를 멈추는 조건 · 기공 목표를 맞추는 방법 · CBD 양 · 밀도 · 기공 상 (ASSB) 알고리즘 · SE 상을 만드는 규칙.
4. **SI 본문 (b) 와 흐름도 S2 의 CBD 규칙이 다르다** — 본문 = AM 이웃 없는 화소를 1 − w 로 거절 · 흐름도 = 고체 접촉 필수 + CBD 이웃이면 ω · 아니면 1 − ω · 기호 w ↔ ω (§3-5).
5. **예시의 해상도 · Precision 미인쇄** — '≈650 000 사면체' 를 화소 수와 이을 수 없다.
6. **COMSOL 모델 미기재** — 식 · 매개변수 · 차단 전압 · 실험 검증 없음 ([6, 19, 20] 에 맡김) · Fig. 5d 색 막대 없음 · Fig. 5c 세로축 제목이 래스터에서 잘림.
7. **그림 캡션 결함** — Fig. 3 *"c) uncalendered and 750\*.8 – d) calendered electrodes"* (깨진 글자) · *"in green the AM"* ↔ 그림은 청록 · Fig. 3c–d 의 겹침 · 기공 값 없음.
8. **화면 캡처 안의 불일치** — 그림 1b Generate 칸 (30 µm @ 0.25 µm = 120 칸) ↔ 표시 구조 100³ px (가져온 행렬) · 그림 1b (0.25 µm) ↔ 그림 2a (0.33 µm) 해상도 · 'Targuay PE' (화면) ↔ 'Targray®' (본문).
9. **영상은 원문에 언급되지 않는다** — 소속은 파일 이름뿐 · 소리 없음.
10. **표기**: *"to avoid to avoid introducing errors"* (p.1451) · *"Iso2 mesh"* (p.1454) · 참고문헌 목록에 제목 없음 (Wiley 양식 — §12 는 원문 그대로 제목 없이).
11. 문헌 몫 '< 20 %' 의 근거 = 검색 날짜 · 낱말뿐 (건수 미인쇄).
12. ⚠ 이 카드의 [판독] 은 래스터 화소 판독 (선 굵기 ≈ 0.012 V · 끝 용량 ±1 mAh/g 수준) · [그림 글자] · [영상 관찰] 은 그 화면 한 상태의 값 · 요소 / 화소 · d / 화소 · 칸당 사면체는 **[카드 산술]**.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 — 이 논문 목록에는 제목이 없다 · 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 11 | M. Chouchane, A. Rucci, A. A. Franco, ACS Omega 2019, 4, 11141–11144. | INNOV 메싱 알고리즘 원전 | `chouchane2019_innov_voxelization_multiphase_meshing` |
| 6 | M. Chouchane, A. Rucci, T. Lombardo, A. C. Ngandjong, A. A. Franco, J. Power Sources 2019, 444, 227285. | 반쪽 전지 모델 출처 [6, 19, 20] · 제조 모의 → 3D 전기화학 사슬의 같은 그룹 앞 논문 (h · 단계 7) | 없음 |
| 19 | M. Chouchane, E. N. Primo, A. A. Franco, J. Phys. Chem. Lett. 2020, 11, 2775–2780. | 반쪽 전지 모델 출처 | 없음 |
| 20 | A. C. Ngandjong, T. Lombardo, E. N. Primo, M. Chouchane, A. Shodiev, O. Arcelus, A. A. Franco, J. Power Sources 2021, 485, 229320. | 반쪽 전지 모델 출처 · DEM 캘린더링 | `ngandjong2021_dem_calendering_digital_twin` |
| 18 | A. P. Tran, S. Yan, Q. Fang, NPh 2020, 7, 015008. | Iso2mesh — 메시 렌더 · '다른 여러 함수' 재사용 (f · h) | 없음 |
| 8 · 9 · 10 | A. N. Mistry, K. Smith, P. P. Mukherjee, J. Phys. Chem. Lett. 2018, 10, 6317–6326 · M. Duquesnoy, T. Lombardo, M. Chouchane, E. N. Primo, A. A. Franco, J. Power Sources 2020, 480, 229103 · J. Joos, A. Buchele, A. Schmidt, A. Weber, E. Ivers-Tiffée, Energy Technol. 2021., n/a 2000891. | 확률적 생성 알고리즘 [8–10] (흐름 밖: 합성 구조 생성) | [9] = `duquesnoy2020_calendering_ml_mesostructure_generator` · [8] [10] 없음 |
| 16 · 17 | S. J. Cooper, A. Bertei, P. R. Shearing, J. A. Kilner, N. P. Brandon, Software X 2016, 5, 203–210 · https://www.math2market.com/. | .tif → tortuosity factor (TauFactor · GeoDict) | [16] = `taufactor_tortuosity_factor_tomography_tool` |
| 12 | 2021, https://github.com/NREL/MATBOX_Microstructure_analysis_tool-box. | 비슷한 공개 도구 (Matbox) | 없음 |
| 1–5 · 7 | A. Gayon-Lombardo, L. Mosser, N. P. Brandon, S. J. Cooper, npj Comput. Mater. 2020, 6, 1–11 · M. E. Ferraro, B. L. Trembacki, V. E. Brunini, D. R. Noble, S. A. Roberts, J. Electrochem. Soc. 2020, 167, 013543 · X. Lu, A. Bertei, D. P. Finegan, C. Tan, S. R. Daemi, J. S. Weaving, K. B. O. Regan, T. M. M. Heenan, G. Hinds, E. Kendrick, D. J. L. Brett, P. R. Shearing, Nat. Commun. 2020, 11, 1–13 · A. A. Franco, A. Rucci, D. Brandell, C. Frayret, M. Gaberscek, P. Jankowski, P. Johansson, Chem. Rev. 2019, 119, 4569–4627 · T. Danner, M. Singh, S. Hein, J. Kaiser, H. Hahn, A. Latz, J. Power Sources 2016, 334, 191–201 · X. Lu, S. R. Daemi, A. Bertei, M. D. R. Kok, K. B. O'Regan, L. Rasha, J. Park, G. Hinds, E. Kendrick, D. J. L. Brett, P. R. Shearing, Joule 2020, 4, 2746–2768. | '높은 해상도 · 전기화학-역학 결합' 성과 [1–5] · 3D 모델의 쓸모 [6, 7] | [7] = `lu2020_insitu_nanoct_calendering_microstructural_evolution` · 나머지 없음 |
| 13 · 14 · 15 | https://www.u-picardie.fr/erc-artistic/computational-portal/ · M. F. Lagadec 2016, https://doi.org/10.5905/ethz-1007-32 · M. F. Lagadec 2018, https://doi.org/10.3929/ethz-b-000265085. | 웹 앱 주소 · 분리막 단층 영상 자료 (Celgard · Targray) | — |

---

## [미확인] 목록
- 슬라이싱 (구 → 화소) 규칙 · 겹친 구 · 상 우선 · 부분 부피 · 기본 해상도.
- 'overlap %' 의 분모 · '충분히 겹침' 문턱 · AM 배치 멈춤 조건 · 기공 목표를 맞추는 방법 · CBD 양 · 밀도.
- 기공 (void) 상 · 고체전해질 상의 생성 알고리즘 · ASSB 예의 재료 · 크기.
- 세 예의 해상도 · Precision · (반쪽 전지 외) 요소 수 · 생성 시간.
- COMSOL 반쪽 전지 모델의 식 · 매개변수 · 차단 전압 · 실험 검증.
- 'Decomposition' · 'All ▼' · 'voxel ▼' / 'pixel ▼' 드롭다운의 뜻.
- 메시에 넣는 '선택' 이 도메인만인지 경계까지인지 (이 논문 기준).
- 단층 영상 분리막 (Celgard · Targray) 을 전극 해상도에 맞추는 방법.
- 보충 영상의 출처 · 설명 (논문 · SI 에 언급 없음).
- 표지 기사 (Cover Feature) 의 쪽 · DOI (이 PDF 에 인쇄 없음 — `benhadjali2026_fully_coupled_*` L403 의 10.1002/batt.202100202 는 이 작업에서 확인 못 함).
- 문헌 몫 '< 20 %' 의 검색 건수.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 서지: 1저자 메모 (M. Chouchane, A. A. Franco · 제목 · Batteries & Supercaps 2021, 4, 1451–1456 (Concept) · doi 10.1002/batt.202100096 · 본문 6 쪽 · SI 6 쪽 · 영상 1) = 원문 첫 쪽 · 머리글 · 마지막 쪽과 같음 · 후보 표 N-73 서지 · 가리킨 카드 L449 서지와도 같음 · 원문에만 있는 것 = 머리글 'Concepts' · 호 9 (표지 그림 '9/2021') · 날짜 넷 (p.1456).  **다른 점 없음**.
- 숫자 (본문 · SI 글자 층 + 렌더): < 20 % · 30 년 · 2021-04-19 · 2019 [11] · 'INdefinite Number Of phases meshing through Voxelization' · 0 · 1 (w) · 30 % · 20 % (in volume) · 35×35×35 μm³ · 94 % · NMC-111 · 5 μm · ca. 650 000 · C/10 · 1C · 2C · 10 % · 20 μm · 15 % · .ply · .stl · .bdf · .mphtxt · .mat · .tif · d > radius × α (1) · α = 1 · α = 0 · 1 − w · ERC 772873 · 날짜 넷 — 전부 위치 확인.
- 그림 글자 · 영상: 그림 1b · 2 · S2 · S3 를 내장 래스터 (≈220–1555 dpi) 로 확대해 읽음 · 영상은 15 s 간격 접촉 시트 (18 장) + 전 해상도 정지 화면 (5 · 30 · 45 · 62 · 72 · 78 · 85 · 92 · 140 · 185 · 210 · 240 · 265 s) 로 로그 시각 · 요소 수 · 칸 값 확인.
- 판독: Fig. 5c 내장 래스터 (xref 51) 의 축 틀 (x 252.5–1627.5 px · y 123.5–1186 px) · 눈금 표시 (위 · 아래 · 왼 · 오른 축이 서로 같음) 로 맞춤 · 곡선 색 거리 < 70 · 범례 상자 가림.
- 원문 전수 검색 (DEM · discrete · LAMMPS · CGMD · video · movie · smooth · converge): 0 회.
- 정본 중복 확인: `litdb/papers/` 목록 (chouchane* = `chouchane2019_*` 하나 · 다른 논문 ACS Omega 2019) + DOI (`batt.202100096`) · 'Invitation to Engage' · 'INNOV' grep — 이 논문 카드 없음 (인용만: benhadjali2025 · benhadjali2026_wip · benhadjali2026_fully_coupled).

## 🔗 관련 카드
- **같은 도구 (INNOV) 의 알고리즘 원전**: `chouchane2019_innov_voxelization_multiphase_meshing` (이 논문의 ref [11] · 같은 1 저자 · 2019 · 노드 · 사면체 · 분리면 경우 · 매끄럽게 하기 · precision 정의).
- **이 논문을 인용한 카드 (같은 사슬 CGMD → 복셀화 → INNOV → COMSOL)**: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (ref [38] · L165 · L262 · L449 — 가리킨 카드 · 0.2 µm 복셀화) · `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` (ref [27] · L380) · `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` (ref [30] = 표지 기사 서지 · L403) · `benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode` (INNOV [47, 48]).
- **이 논문이 인용한 정본 카드**: `ngandjong2021_dem_calendering_digital_twin` ([20]) · `duquesnoy2020_calendering_ml_mesostructure_generator` ([9]) · `taufactor_tortuosity_factor_tomography_tool` ([16]) · `lu2020_insitu_nanoct_calendering_microstructural_evolution` ([7]).
- **복셀 넘김 · 계단 넓이**: `windreich2003_voxel_based_surface_area_estimation` · `lindblad2005_surface_area_weighted_local_configurations` · `ziegel2010_surface_area_measure_digitizations` · `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` (영상 → INNOV).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
