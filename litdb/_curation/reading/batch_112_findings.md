# batch 112 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-73 · 대피 세션)

대상: `chouchane2021_innov_webapp_stochastic_generation_meshing` — M. Chouchane · A. A. Franco, "An Invitation to Engage with Computational Modeling: User-Friendly Tool for In Silico Battery Component Generation and Meshing", *Batteries & Supercaps* **4** (2021) 1451–1456 (9 호 · Concepts) · DOI 10.1002/batt.202100096
INNOV 웹 앱 (GUI · ARTISTIC 서버 계산) — 3D 전지 부품 구조를 가져오거나 (영상 묶음 · MATLAB 행렬 · AM + 반지름 일정 CBD 구 좌표 → 슬라이싱) 확률적으로 만들어 (구 AM · SI 식 1 경계 규칙 · AM–AM 겹침 목표 · PSD · 주기 경계 · 화소 단위 CBD (w) · ASSB 기공 상 · 분리막 · 집전체) 2019 복셀화 알고리즘 [11] 으로 다상 사면체 메시를 짜 .mphtxt (COMSOL 선택 내장) · .bdf · .mat · .stl · .ply · .tif 로 내보낸다 — DEM · 역학 · 압밀 · 탈압 · 수렴 시험 없음.
쪽 = 인쇄 쪽 p.1451–1456 (PDF 쪽 n = 1450 + n) · SI p.n = SI PDF 쪽 · 판독 원자료 = `litdb/figures/chouchane2021_innov_webapp_stochastic_generation_meshing/digitized.csv` (42 행 · Fig. 5c) · 고른 의도 = '넘김 도구 (h 이웃) — INNOV · benhadjali2026 의 넘김 = 0.2 µm 등방 복셀화 → INNOV [38] · 복셀 메싱 [39]' → 의도 대조 결과 **일부** (도구 원전 · 단계 · 형식 · 상 표지 = 채움 · 0.2 µm = 이 논문 값 아님 · 메시 세부 = [11] 에 맡김 · 슬라이싱 규칙 · 해상도 · 수렴 · 계단 처리 = 없음).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 압밀 · 측정이 없다.  기공 값은 전부 **생성기 입력** 이다: 반쪽 전지 예 30 % (p.1455) · ASSB 예 전극 10 % · SE 분리막 20 µm 의 15 % (p.1455) · 영상 전전지 예 35 % [영상 관찰] — 진밀도 · 질량 기준 · 압력 없음 (카드 §7-2 · 랩 표준과 판정 없이 나란히).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음.

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중 · 역학이 없다 (구 AM 은 겹침 규칙으로만 배치).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙이 없다.  '압연' 은 접촉 역학이 아니라 **AM–AM 겹침 % 를 올리고 기공 % 를 낮춘 확률적 구조** (p.1453 · Fig. 3c–d) — 맞춘 값 0 개 (겹침 · 기공을 입력으로 넣는다).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 MPM 없음.  해상도 · 메시 쪽 근거만:
- [f] chouchane2021_innov_webapp_stochastic_generation_meshing | 해상도 = *"a resolution that can be modified by the user"* (SI p.5) · 요소 수 = 'Precision' (축별 숫자 셋) · 지침 한 문장 *"The precision should always be adapted to the size of the system, the characteristic length of the system, and to the computational power available"* — 정량 규칙 · 수렴 · 오차 추정 없음 | 카드 §0 ③ · §3-3 · p.1455 · SI p.5 | [인쇄] | 메시 · 해상도 수렴 미시험
- [f] chouchane2021_… | 화면 기본값의 지름당 칸 수 (d / 화소): 반지름 2–4 µm @ 0.25 µm → 16–32 · @ 0.33 µm → 12–24 · 영상 1 µm → 4–8 · 영상 가우스 2–8 µm @ 0.5 µm → 8–32 · CBD 는 화소 하나 단위 (d / 화소 = 1) | 카드 §7-3 · Fig. 1b · 2a · 영상 | [그림 글자 · 영상 관찰 · 카드 산술] | 화면 한 상태 · 권장값 아님
- [f] chouchane2021_… | 요소 / 화소 0.177–0.490 (192 777 · 204 378 · 416 975 · 313 874 요소 · 2–5 s) · 칸당 12–23 사면체 → *"elements finer at the interface between materials and coarser in the bulk"* 와 맞는 크기 | 카드 §3-3 · p.1454 | [그림 글자 · 영상 관찰 · 카드 산술] | 계면 넓이 · 요소 품질 미기재

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 전부 3D (*"time dependent 3D-resolved computational modeling"* p.1451) · 판 보기 (xy · xz · yz) 는 화면 표시용 2D 단면.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] chouchane2021_innov_webapp_stochastic_generation_meshing | ★ 넘김 경로의 원형: '(x,y,z,radius) · Manufacturing Simulation Output' → *Slicing* → 'Binary segmented images' → *Meshing* → 'Volumetric Mesh' (Fig. S4) · *"With spheres coordinates, either they arose from manufacturing simulation or from the AM in INNOV's embedded stochastic generation algorithm, an additional step is needed to convert them into a stack of images. Indeed, a slicing process takes place to generate the 3-D structure, with a resolution that can be modified by the user."* (SI p.5) | 카드 §0-1 · §4-1 · SI p.5 · Fig. S4 | [인쇄 · 그림 글자] | 'DEM' · 'CGMD' 0 회 · 넘긴 시점 미기재 · 넘기는 자료 = 위치 · 반지름 · 상 뿐
- [h] chouchane2021_… | 구 좌표 가져오기 = *"a list of the coordinates and radii of AM and CBD spheres, with the CBD having a constant radius"* (p.1453) — **SE 구 범주 없음** → ASSB 입자 모의 출력은 바깥에서 먼저 복셀화해야 한다 (benhadjali 들의 0.2 µm 복셀화 + 겹침 부피 이동이 그 예 [다른 카드 benhadjali2025 · benhadjali2026_wip L165]) | 카드 §3-6 · §9 ② | [인쇄 · 카드 해석] | 슬라이싱 규칙 (겹친 구 · 상 우선 · 부분 부피) [미확인]
- [h] chouchane2021_… | 내보내는 것 = 상 라벨 다상 사면체 메시 (.mphtxt 에 'built-in selections' · .bdf (Nastran) · .mat · .stl · .ply) + 구조 .tif (TauFactor · GeoDict) — 입자 번호 · 접촉 · 힘 · 응력 없음 | 카드 §3-6 · p.1454 | [인쇄 · 카드 해석] | 선택이 도메인만인지 경계까지인지 이 논문 기준 [미확인]

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — ASSB 예의 기공 10 % (전극) · 15 % (SE 분리막) 는 생성기 입력 (p.1455) · 압력 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] chouchane2021_… | 원문 앞으로 할 일: *"several new features such as the generation of non-spherical particles, CBD with PSD, or adding a separate app to perform basic image segmentation will be considered in the future"* → 지금은 구 입자 · CBD 크기 분포 없음 (R6 · 형상 변형 없음) | p.1456 · 카드 §0 ⑩ | [인쇄] | 가압 · 탈압 언급 없음
- [j] chouchane2021_… | 카드가 적은 빈칸: 슬라이싱 규칙 · 해상도 · 수렴 · 겹침 % 정의 · 생성기 기공 맞춤 방법 · ASSB 기공 상 알고리즘 · COMSOL 모델 | 카드 §11 · [미확인] 목록 | [미확인] | —

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Chouchane · Franco 2021, Batteries & Supercaps 4, 1451–1456)
- [k] chouchane2021_innov_webapp_stochastic_generation_meshing (Chouchane · Franco 2021 · Batteries & Supercaps 4, 1451–1456) | **말 없음** — 본문 · SI 에 DEM · discrete · LAMMPS · CGMD 0 회 (전수 검색).  구 입자 가정은 도구 자신의 한계로 적힘: *"the AM particles are considered as spheres"* (p.1453) + 비구형 입자는 앞으로 (p.1456) | 카드 §4-4 | [인쇄] | DEM 한계 진술로 인용하지 않는다

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Chouchane · Franco 2021, Batteries & Supercaps 4, 1451–1456)
- [l] chouchane2021_… (Chouchane · Franco 2021) | 소성을 다루지 않는다 — '압연' 을 기하로 대리: *"to capture the structural changes upon a calendering process, with the AM particles being brought closer to each other, one can increase the AM-AM overlap and decrease the porosity to have a more packed structure"* (p.1453) · 반쪽 전지 예 *"To simulate a calendered electrode, a porosity of 30% was set with 20% (in volume) of overlap between AM particles"* (p.1455) — 구가 파고들 뿐 형상 · 부피 보존 흐름 · 응력 없음 · 맞춘 값 = 겹침 % · 기공 % (입력) · 검증 없음 · 비용 = 생성 ≈9 s (80³ 화소) · 메시 2–5 s (서버) [영상 관찰] | 카드 §0 ⑥ · §4-4 (ii) | [인쇄 · 영상 관찰] | 이유 설명 없음 (어려움을 논하지 않는다)

## m — 받아들일 통찰
- [m] chouchane2021_… | 무엇을: **넘김 매니페스트 칸** — 구 → 화소 규칙 (상 우선 · 겹침 · 부분 부피) · 해상도 · d / 화소 · 표현 부피 비 · (FE 면) Precision · 요소 수 · 수렴을 넘김 산출물에 결과 전 칸으로 둔다 · 우리 쪽 어디에: 단계 0 · 단계 7 · 왜: INNOV 원문은 이 칸들을 하나도 적지 않아 같은 구 목록의 기공 · 피복이 해상도에 얼마나 기대는지 알 수 없다 (SI p.5 · p.1455 · 카드 §9 ①)
- [m] chouchane2021_… | 무엇을: **SE 구는 우리 규약으로 먼저 복셀화** — INNOV 구 가져오기 = AM + 반지름 일정 CBD 뿐 · 우리 쪽 어디에: 후보 D0 → 단계 7 넘김 · 왜: p.1453 가져오기 문장 · benhadjali 가 0.2 µm · 겹침 부피 이동을 스스로 정한 것 [다른 카드] (카드 §9 ②)
- [m] chouchane2021_… | 무엇을: **화소 단위로 자라는 상은 해상도가 형상 척도** — CBD 를 전해질 화소 하나씩 바꾸는 규칙 → 해상도를 바꾸면 같은 부피에서도 형상 · 연결성이 바뀐다 · 우리 쪽 어디에: 흐름 밖: STEP3 첨가제 표현 (CL-25 와 같은 부류) · Rint ② 탄소 접합 · 왜: SI p.3 · Fig. S2 · Fig. 3 (카드 §3-5 · §7-3 ②)
- [m] chouchane2021_… | 무엇을: **.tif → TauFactor 를 τ 교차 점검 출구로** — 같은 복셀 구조의 tortuosity factor (= tau2) 를 STEP3 복셀 FV 의 tau2 와 견준다 · 우리 쪽 어디에: 흐름 밖: τ 규약 · 왜: p.1454 · `taufactor_tortuosity_factor_tomography_tool` (카드 §9 ⑤)

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] M. Chouchane, A. Rucci, T. Lombardo, A. C. Ngandjong, A. A. Franco, J. Power Sources 2019, 444, 227285. (원문 목록 [6] 그대로 · 제목 미인쇄 — 서지 일부만) | 같은 그룹의 '제조 모의 → 3D 전기화학' 반쪽 전지 모델 [6, 19, 20] 출처 — h · 단계 7 (p.1455 *"a half-cell model similar to those already reported by our group"*) | litdb 확인: papers/ 의 chouchane* = chouchane2019 (ACS Omega · 다른 논문) · chouchane2021 (이 카드) 뿐 · '227285' grep = benhadjali2025 (인용만)
- [n] A. P. Tran, S. Yan, Q. Fang, NPh 2020, 7, 015008. (원문 목록 [18] 그대로 · 제목 미인쇄 — 서지 일부만) | Iso2mesh — *"The mesh 3D rendering as well as several other functions were reused from Iso2 mesh"* (p.1454) · 메싱 함수 원전 — f · h | litdb 확인: papers/ 에 tran* 없음 · '015008' grep 0 · 'Iso2mesh' grep = chouchane2019 · cronk2026 (둘) · zhang2026 (인용만)
- [n] J. Joos, A. Buchele, A. Schmidt, A. Weber, E. Ivers-Tiffée, Energy Technol. 2021., n/a 2000891. (원문 목록 [10] 그대로 · 제목 미인쇄 — 서지 일부만) | 확률적 미세구조 생성 [8–10] 의 하나 — 흐름 밖: 합성 구조 생성 · 단계 0 (생성 구조의 기공 · 연결성 정의) | litdb 확인: papers/ 에 joos* 없음 · '2000891' grep 0 ('Joos' grep 은 다른 Joos 논문 인용만)

## 카드 문제
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` **L251** *"넘김: 0.2 µm 복셀 → 메시 — 겹친 구의 공통 부피는 한 번만 세어진다 (복셀 기하의 성질 [추정]) · 계면 = 복셀 면."* — '계면 = 복셀 면' 은 이 논문 (INNOV 2021) 에 해당 문장이 없고 (*"elements finer at the interface"* 만), 메싱 원전은 상이 섞인 칸을 분리면 (Nielson–Franke 경우) 으로 잘라 사면체를 만든다 [다른 카드 `chouchane2019_innov_voxelization_multiphase_meshing` L12 · §4] → 그 줄은 원전과 어긋날 수 있다 (경미 · 고치지 않음).
- 그 밖에 확인한 2 차 인용 — 같음: `benhadjali2026_wip_*` L449 (서지 · 호 · 'Concepts' 만 없음) · L165 · L262 · `benhadjali2025_*` L380 ([27] · 9 호 포함) · `chouchane2019_*` L300.  `benhadjali2026_fully_coupled_*` L403 ([30] = 표지 기사 서지 · 1375 쪽 · 10.1002/batt.202100202) 은 이 PDF 로 확인할 수 없다 ([미확인] — 표지 그림만 있고 그 기사의 쪽 · DOI 는 인쇄돼 있지 않다 · 그 카드가 본 논문 DOI 와 이미 구분해 둠).
