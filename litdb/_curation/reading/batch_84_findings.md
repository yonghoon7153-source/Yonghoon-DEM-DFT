# batch 84 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-13)

대상: `chouchane2019_innov_voxelization_multiphase_meshing` — Mehdi Chouchane, Alexis Rucci, Alejandro A. Franco, "A Versatile and Efficient Voxelization-Based Meshing Algorithm of Multiple Phases", *ACS Omega* 4 (2019) 11141–11144 · DOI 10.1021/acsomega.9b01279 (후보 표 N-43 · 가리킨 카드 = `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L165 · L450).
MATLAB 메싱 도구 (INNOV) — 이진 영상 (단층 분할 영상 또는 CGMD 구 중심 · 반지름을 바꾼 것) 의 화소를 상 코드 노드로 삼아 모든 상을 한꺼번에 사면체로 쪼개 COMSOL 5.4 로 넘긴다 · 예시 = 액체 LIB NMC 전극 (AM + CBD + 기공) · 물리 계산 · 역학 · 실험 없음.
쪽 = PDF 쪽 p.1–4 (= 인쇄 11141–11144) · SI p.1–4 (= S1–S4) · 판독 원자료 = `litdb/figures/chouchane2019_innov_voxelization_multiphase_meshing/digitized.csv` (10 행 · Fig. 3).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 0 · 압력 0 — 액체 LIB 전극의 메싱 예시뿐).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (역학 · 하중 0).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙 없음 — 같은 상 입자는 메시에서 한 영역으로 융합된다 [카드 해석]).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
- [f] chouchane2019_innov_voxelization_multiphase_meshing | (MPM 아님 · 복셀 → 사면체 메싱의 해상도 · 오차) 화소 1 개 = 노드 1 개 · 축소 precision = 축마다 'N 개 중 하나' 노드 (스칼라 = 등방 · 벡터 = 비등방) · 201 × 200 × 179 화소에서 축소 없이 > 48 M 요소 · 177.20 s ↔ [4 4 3] 1 737 665 요소 · 339 067 노드 · 4.48 s · 오차 추정 = 상별 부피 보존 (메시 ÷ 영상) void 99.2 · AM 101.6 · CBD 99.7 % · 합격선 '< 2 %' · 매끄럽게 하면 기공 49.69 → 50.07 % · 요소 / 정육면체 ≥ 6.8 (축소 없이) · 12.0 (축소) | 카드 §3-2 · §3-3 · p.2–3 · 표 1 | [인쇄] · [카드 산술] | 화소 크기 (µm) 미기재 → 지름당 칸 수 규칙 없음 · 메시 수렴 · 요소 품질 · 넓이 정확도 미시험 · 한 구조 한 번 · 접촉 · 다물체 · 강체 결합 없음
- [f] chouchane2019_innov_voxelization_multiphase_meshing | 축소의 대가 (판독): Fig. 3 precision 1 ↔ 5 단면의 상 면적 몫 변화 ≤ 0.011 인데 CBD 최대 2D 조각 0.077 → 0.049 · 조각 (≥ 30 px) 16 → 20 — 부피 보존 점검은 통과해도 연결성이 바뀐다 | 카드 §3-4 · Fig. 3 · digitized.csv | [판독] (그림 화소 · 2D 단면 하나) | 3D 연결성 아님 · 같은 위치 단면인지 미기재 · 원문은 정량 서술 없음 (*"While slightly losing in precision"*)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] chouchane2019_innov_voxelization_multiphase_meshing | 원문의 차원 문장 = *"P2D models cannot capture the impact of the 3D electrode mesostructure and associated anisotropy on the LIB cell behavior"* — 균질화 의사 2 차원 전기화학 ↔ 3D 해상의 대조이고, 2D 해상 계산 → 3D 의 전이 경고 · 증거는 없다 · 메시는 3D (Fig. 3 은 단면 그림) | 카드 §4-3 (iii) · p.1 | [인쇄] | 역학 · 접촉의 2D/3D 이야기가 아니다 (질문 g 의 뜻과 다름 · 참고 줄)

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] chouchane2019_innov_voxelization_multiphase_meshing | ★ 입자 계산 구조 (CGMD · LAMMPS 구 중심 · 반지름 텍스트) → MATLAB 함수 → 이진 영상 묶음 → INNOV 사면체 다상 메시 (화소 = 상 코드 노드 · 4 + 4 노드 정육면체 → 5 / 6 사면체 · 섞인 칸 = Nielson–Franke 분리면 · Iso2Mesh 중복 노드 제거) → COMSOL 5.4 mphtxt + Selections (도메인 · 경계 *"typically thousands"*) · 넘기는 것 = **상 라벨 기하만** (입자 번호 · 접촉 · 힘 · 응력 · 이력 없음) · 시점 = 예시 구조의 제조 단계 [미확인] · 이 도구를 쓴 뒤 사례 [다른 카드]: ngandjong2021 L277 (DEM 캘린더링 → INNOV) · zhang2023 L214 (PFIB 영상 → INNOV ≈2.3 M 요소) · benhadjali2025 · 2026 세 편 (CGMD 압연 → 겹침 후처리 → INNOV) | 카드 §0 ① · §4-1 · §4-2 · p.2–3 · SI p.3–4 · Fig. 2 · S2 · S3 | [인쇄] · [카드 해석 (같은 상 융합)] | **구 → 영상 규칙 (겹침 · 상 우선 · 화소 크기) 미기재** — 가리킨 카드 L450 이 기대한 '겹친 구를 하나의 고체로 잇는 규칙' 은 없다 · 압력 · 하중 상태 없음 · 넘긴 구조의 물리 결과 없음

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] chouchane2019_innov_voxelization_multiphase_meshing | 압력 없음 · 한 구조 한 점: 액체 LIB NMC 전극 (AM + CBD + 기공 · CGMD) 의 기공 = 이진 영상 50.1 % · 메시 49.7 % · 매끄럽게 한 메시 50.07 % | 카드 §3-3 · p.2 · 표 1 | [인쇄] | SE 없음 · 압력 · 제조 단계 미기재 · 이진 영상 연산자 (같은 상 겹침 한 번만 = 합집합 꼴 [카드 해석]) — '압력별' 은 없음 (참고 줄) · 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 과 다른 문헌 값

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] chouchane2019_innov_voxelization_multiphase_meshing | 원문 한계: 부피 보존은 평균 — *"cannot highlight local deformations within the mesh"* · 축소 *"slightly losing in precision"* · 매끄럽게 하면 요소 부피가 줄어 기공 ↑ · 고해상도 영상 = *"a double-edged sword"* · 카드 한계: 구 → 영상 규칙 · 화소 크기 미기재 · 물리 결과 · 수렴 · 연결성 점검 없음 | 카드 §11 · p.2–3 | [인쇄] · [카드 해석] | 가압 · 탈압과 직접 닿지 않는다 (눌린 구조를 다른 계산으로 넘길 때의 넘김 단계 한계로만)

## k — DEM 의 한계
- [k] chouchane2019_innov_voxelization_multiphase_meshing (Chouchane · Rucci · Franco 2019 · ACS Omega 4, 11141–11144) | **말 없음** — 'DEM' · 'discrete' 0 회 · 'contact' 1 회 (*"Where the AM and the CBD are in contact, the elements of the mesh of the AM should be finer to match the ones of the CBD"* = 적응 메시 크기 맞춤) · 입력 구조는 구 (*"The spherical active material particles"* Fig. 1 캡션) 이지만 그 한계를 다루지 않는다 · 원문이 비판한 한계는 3D 전기화학 모델의 CBD 표현: *"reported 3D-resolved models rely on oversimplifications, such as an implicit representation of the CBD through the use of effective parameters for porosity and tortuosity or by merging CBD with the active material (AM) as a single solid phase"* | 카드 §4-3 (i) · p.1 · Fig. 1 | [인쇄] | DEM 한계의 인용처로 쓰지 않는다

## l — 소성변형이 왜 어려운가
- [l] chouchane2019_innov_voxelization_multiphase_meshing (Chouchane · Rucci · Franco 2019 · ACS Omega 4, 11141–11144) | **말 없음** (역학 0 · 'plastic' 은 참고문헌 제목뿐) — 원문의 비용 논의는 메시 크기 ↔ 시간 뿐: *"the simulation time (which can be up to several days in some cases) of the downsized mesh will also decrease compared to the original one. Indeed, the downsized mesh has more than 1.5 million elements, while the mesh without downsizing has more than 48 million elements"* | 카드 §4-3 (ii) · p.3 | [인쇄] | 소성 · 큰 변형 어려움의 인용처로 쓰지 않는다

## m — 받아들일 통찰
- [m] chouchane2019_innov_voxelization_multiphase_meshing | 무엇: **넘김 보존 점검 둘** — (가) 입자 → 격자: 상별 표현 부피 ÷ 참 부피 (구 부피 합 / 합집합 명시) + 겹침 처리 (상 우선 · 부피 이동) (나) 격자 → 메시 · 해: 상별 부피 보존 + 기공 두 값 + 매끄럽게 전후 — 이 논문은 (나) 만 (상별 99.2 · 101.6 · 99.7 % · < 2 %) · 우리 CL-25 원장은 (가) 만 · 어디에: 단계 0 · 단계 7 · 후보 D0 · 왜: 카드 §7-2 · §9-1 · p.2 · 표 1
- [m] chouchane2019_innov_voxelization_multiphase_meshing | 무엇: **기공 보고의 '센 자리' 칸** — 같은 구조에서 영상 50.1 · 메시 49.7 · 매끄럽게 50.07 % (≤ 0.4 %p) · 우리 겹침 부기 규약 차이 (ε_sphere ↔ ε_union ≈1.5 %p · MPM 관례 1.251 %p [우리]) 와는 부류가 다르니 칸을 따로 둔다 · 어디에: 단계 0 · 왜: 카드 §3-3 · §7-1 · §9-2
- [m] chouchane2019_innov_voxelization_multiphase_meshing | 무엇: **연결성 점검을 부피 점검 옆에** — 축소 · 해상도 변경 뒤 상별 연결 성분 · 관통 (Fig. 3 판독: 면적 몫 변화 ≤ 0.011 · CBD 최대 2D 조각 0.077 → 0.049) · 어디에: 단계 7 · U1 · 왜: 카드 §3-4 · §9-3 · Fig. 3
- [m] chouchane2019_innov_voxelization_multiphase_meshing | 무엇: **CF 표지** — 상 코드 메시 · 복셀은 같은 상 입자를 융합 (접촉 저항 0) → 이 계열 COMSOL 수송 결과 (benhadjali · zhang2023 · ngandjong2021) 를 우리 접촉망 FULL 과 견주지 않는다 (STEP3 CL-81 과 같은 규약) · 어디에: 흐름 밖: 수송 · 문헌 값 대조 · 왜: 카드 §4-2 · §7-1 · §9-4 · p.3 §4.2

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Nielson, G. M.; Franke, R. Computing the separating surface for segmented data. Proceedings of IEEE Visualization 1997, Phoenix, USA; IEEE: 1997, 229−233. (원문 참고 (19) · 인쇄 그대로) | f · h · 단계 0 — INNOV 의 분리면 수학 (상이 섞인 칸의 네 경우 · 5 / 6 사면체) = 상 경계 면 · 계면 넓이가 어디에 놓이는지의 원전 · 카드 §4-1 · §12 | litdb 확인: papers/ 파일 목록에 nielson* 없음 · 'Nielson' · 'separating surface' grep 0 건 (wishlist · S8 0 건)
- [n] Fang, Q.; Boas, D. A. Tetrahedral mesh generation from volumetric binary and gray-scale images. Proceedings of the Sixth IEEE international conference on Symposium on Biomedical Imaging: From Nano to Macro 2009; Boston, USA IEEE: 2009, 1142−1145. (원문 참고 (20) · 인쇄 그대로) | h — Iso2Mesh (영상 → 사면체) 의 원전 · 정본 cronk2026 · zhang2026 카드가 Iso2Mesh 를 직접 썼다 (cronk2026 의 서지는 다른 논문 = Tran 2020) · 카드 §12 | litdb 확인: fang* = fang2022_argyrodite_transport_beyond_paddlewheel (다른 논문) 뿐 · 'Tetrahedral mesh generation' grep 0 건 · 'Iso2Mesh' = 도구 이름 언급뿐 (wishlist · S8 0 건)
- [n] Ngandjong, A. C.; Rucci, A.; Maiza, M.; Shukla, G.; Vasquez-Arenas, J.; Franco, A. A. Multiscale Simulation Platform Linking Lithium Ion Battery Electrode Fabrication Process with Performance at the Cell Level. J. Phys. Chem. Lett. 2017, 8, 5966−5972. (원문 참고 (10) · 인쇄 그대로) | h — 예시 구조의 CGMD 원전 (구 배치 · 제조 단계) = 넘긴 시점 [미확인] 을 닫는 자리 · 카드 §12 · §13-2 | litdb 확인: ngandjong* = ngandjong2021_dem_calendering_digital_twin (다른 논문) 뿐 · 'Multiscale Simulation Platform Linking' grep 0 건 (xu2023 카드에 'ref [23] = Ngandjong 2017 멀티스케일' 이름 언급뿐) (wishlist · S8 0 건)
- [n] Rucci, A.; Ngandjong, A. C.; Primo, E. N.; Maiza, M.; Franco, A. A. Tracking variabilities in the simulation of Lithium Ion Battery electrode fabrication and its impact on electrochemical performance. Electrochim. Acta 2019, 312, 168−178. (원문 참고 (16) · 인쇄 그대로) | h · m — 같은 CGMD 사슬의 구조 변동 → 전기화학 (예시 구조의 둘째 출처) · 카드 §12 | litdb 확인: rucci* 없음 · 'Tracking variabilities' grep 0 건 (alabdali2023 카드의 '[23 Rucci 2019]' 이름 언급뿐) (wishlist · S8 0 건)
- [n] Mai, W.; Yang, M.; Soghrati, S. A particle-resolved 3D finite element model to study the effect of cathode microstructure on the behavior of lithium ion batteries. Electrochim. Acta 2019, 294, 192−209. (원문 참고 (7) · 인쇄 그대로) | h · 후보 B — 입자 해상 3D FE 의 다른 메싱 선례 (복셀화와 대조할 자리) · 카드 §12 | litdb 확인: mai* 없음 · 'Soghrati' · 'particle-resolved 3D finite element' grep 0 건 (wishlist · S8 0 건)
- (참고 · 후보로 세지 않음) 같은 도구의 사용자 판 Chouchane & Franco, Batteries & Supercaps 4 (2021) 1451–1456 = 후보 표 N-73 (이 논문 참고문헌 밖) · (11) Hein 2016 J. Power Sources 336, 161 · (12) Hein & Latz 2016 Electrochim. Acta 201, 354 = 정본 카드 없음 (질문 a–m 직접 근거 약함).

## 카드 문제
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L450 — 이유 칸 *"카드 없음 — 복셀 메싱 (겹친 구를 어떻게 하나의 고체로 잇는지 = 기공 정의 §10-5 의 열쇠)"* — 원문에 구 → 영상 규칙 (겹침 · 상 우선 · 복셀 안 판정 · 화소 크기) 이 없다 (*"A specific function converts this input into binary images"* p.3 · *"A MATLAB-based function was created to convert this output into a stack of binary images"* SI p.3 · 'overlap' · 'sphere' 0 회) → 기대가 원문과 다르다 · 서지는 같다 · 고치지 않음.
- `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` L379 — *"넘김 메싱의 원전 (겹친 구 → 상 · 복셀 크기 규칙)"* — 둘 다 원문에 없다 (화소 크기 = *"a scale factor parameter (ratio m/pixel)"* · 값 미인쇄 · 축소 precision 만) · 서지 제목이 소문자 꼴 (원문 = 단어 첫 글자 대문자 · 내용 같음) · 고치지 않음.
- `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` L404 — *"복셀 다상 메싱 (복셀 크기 · 겹침 처리의 열쇠)"* — 같은 문제 · 고치지 않음.
- (참고 · 문제 아님) `benhadjali2026_wip_…` L165 · L262 의 'INNOV [38] · 복셀 메싱 [39]' — INNOV 이름 · 알고리즘의 원전은 [39] (이 논문) · '미세구조 생성' 은 이 논문의 기능이 아니다 (그 카드가 원 논문 본문을 옮긴 줄이라 오류로 세지 않음).  `benhadjali2025_…` L64 (겹침 규칙의 출처 = 2025 본문) · `zhang2023_…` L214 · `ngandjong2021_…` L277 · `benhadjali2026_oneway_…` L82 = 원문과 맞다.
- (관찰 · 원 논문 자체의 어긋남 — 카드 §3-5 에 기록) INNOV 풀이 두 벌 (p.2 *"INdefinite Number Of phases"* ↔ p.4 *"infinite number of phase"*) · p.2 *"(see Figure S3)"* ↔ 내용은 SI Fig. S2 · §4.3 *"next slide"* (slice) · 'void' ↔ 'electrolyte' · SI Fig. S2 캡션 *"Meshing process of meshing"*.
- (참고) 후보 표 N-43 서지 = 원문과 같음 (덧붙임: 출판 2019-06-26 · CC-BY-NC-ND · 호 미인쇄).
