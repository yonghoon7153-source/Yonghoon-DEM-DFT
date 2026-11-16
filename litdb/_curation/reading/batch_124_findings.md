# batch 124 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 기존 카드 보강 · 68-2 번 파일)

대상: `lyu2025_3d_dem_drying_calendering_lib` — Yuhang Lyu · Shaohai Dong · Li Ting Gao · Zhan-Sheng Guo, "Three-dimensional discrete element simulation of electrode structural evolution in lithium-ion batteries during drying and calendering", *International Journal of Electrical Power and Energy Systems* 165 (2025) 110521 · DOI 10.1016/j.ijepes.2025.110521 · 12 쪽 + 보충 영상 4 (mp4) · 원문 PDF `e896e74a-68-2._…pdf` 를 처음부터 끝까지 다시 읽고 (텍스트 층 + 식 · 그림 렌더 · 원 래스터 판독 129 행 · 영상 정지 화면 8) 2026-06 옛 양식 카드 (252 줄) 를 576 줄로 보강했다 (정정 표지 21 · 보강 표지 33 · 새 절 §11–§18).
PFC3D 5.00 로 슬러리 RVE (AM 13 µm 구 + CBD 2.2 µm 구 · 200 µm 상자) 를 유체 대리 (부력 · 중력 · 점성 감쇠) 로 '건조' 시켜 쌓고, 그 건조 끝 구조 (≈80 µm · 거친 위 표면) 를 그대로 평판 (0.01 m/s) 으로 40 µm 까지 누른다 — AM = 선형 접촉 결합 · CBD = 선형 병렬 결합 (모멘트 전달) · 탄성 (3/2 승 증분) 접촉 · 항복 · 소성 · 파쇄 · 탈압 없음 · 수송 수치 없음.
쪽 = PDF 쪽 p.1–12 · 판독 원자료 = `litdb/figures/lyu2025_3d_dem_drying_calendering_lib/digitized.csv` · 보강 의도 = '이 논문의 참고문헌이 후보 표 (N-55 · N-67 · N-68 · N-69) · wishlist 의 원 인용처 → 참고문헌 목록 원문 + 카드 2 차 서술 대조' → **일부 다름** (카드 §11).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE 없음 (액체 LIB 양극 'NCM' + CBD).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 계산 없음 (판 하강만 · 그림 7–9 는 무차원 시간 0–1 의 가압).  주의 하나: 검증 그림 3 의 실험 점 [45] 은 **압연 뒤** 값 (정본 sangros2019 카드 표 1) — DEM (누른 채) 과 상태가 다르다 (카드 §11 · §13-3 · [카드 추론]).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] lyu2025_3d_dem_drying_calendering_lib (Lyu · Dong · Gao · Guo, Int. J. Electr. Power Energy Syst. 165 (2025) 110521) | 항복 · 경도 · 크리프 값 없음 · 인용 하나: *"The experiment showed that particle fracture occurred when the stress of the electrode reached 200 MPa [57]"* (전극 응력 200 MPa · 정의 = 'stress of the electrode') · 정본 stershic2015 카드 기준 = Ebner 2013 의 명목 2000 bar 압연에서 깨진 입자가 보인 것 (문턱 측정 아님) | 카드 L35 · §11 [57] 행 · 원문 p.11 | [인쇄] · 해석은 그 카드 기준 | 일축 항복 환산 없음 · NMC 파쇄 (SE 아님)

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] lyu2025_… | 몫 숫자 없음 · *"the contact force is mainly along the thickness"* (그림 9a 삽화 · p.11) · σ_zz −163.9 · σ_xx −127.4 · σ_yy −129.5 MPa (t 1) → 측압 비 0.78 · 판 힘 ÷ 단면 121 MPa · 집전체 140–142 MPa ↔ 접촉 virial σ_zz 164 MPa (1.36 배) | 카드 §12-2 · §12-3 · 그림 9 | [판독] · [카드 산술] | 무른 상 = CBD (E 0.65 GPa · 결합) — SE 아님 · 단면 유지 가정 · V 미기재

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] lyu2025_… | 대안 없음 — 탄성 (인장 없음) 법선 F^l_n = (F^l_n)₀ − k_n(Δδ_n)^{3/2} (식 6 · 앞 문장 [46] 귀속 = 원문 인용 문제) + 선형 접선 + 감쇠 (식 8–9 · δ̇) · k_n = AE*/L (식 14 — 식 6 과 함께면 차원이 맞지 않는다 [카드 산술]) · 1/E* = (1 − ν)²/E 로 인쇄 (식 10) · 결합 2 종 (식 15–23 · λ 1.67) · 맞춘 값 0 (표 1 = 문헌 [45,49,50] · 결합 · 감쇠 값 미기재) · 항복 캡 없음 | 카드 §13-1 · L53–L62 정정 · 보강 표지 · 원문 p.3–4 | [인쇄] · [카드 산술] | 큰 변형 범위 · 겹침 상한 논의 없음

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 — MPM 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] lyu2025_… | *"Two-dimensional (2D) models are commonly used."* · *"Compared with 2D models, three-dimensional (3D) models can better characterize the changes in the electrode structure."* (p.1–2) — 정성 · 숫자 대조 없음 · 같은 그룹 2D 판 [22] (Energ Technol 2024;12:2400583 · 제목상 건조 + 압연) 의 값과 견주지 않는다 | 카드 §15 (iii) | [인쇄] | 2D ↔ 3D 정량 증거 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (DEM → FE · MPM 넘김 없음).  대신 **건조 DEM → 압연 DEM (같은 코드 · 같은 구조)** 넘김: *"The end of the drying simulation is the initial calendering condition, which meant that the electrode structure from the drying simulation is the input parameter for the calendering simulation."* (p.4) — 출발 상태 선례 (단계 5).  서론의 FE 선례 = Sun [47] *"developed a finite element model to study the evolution of electrode microstructure and mechanical properties during calendering"* (p.2 · 정본 카드 없음 → n) · 같은 그룹 DEM → FEM 은 정본 `lyu2026_two_layer_gradient_electrode_calendering_dem_fem`.

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] lyu2025_… | AM + CBD (SE 아님) 압연: 그림 3 DEM 57.0 · 43.0 · 38.0 · 31.0 · 23.0 % (≈0 · 20 · 43 · 79 · 159 MPa · 누른 채) ↔ 실험 [45] 52.2 · 41.6 · 37.2 · 29.5 · 21.7 % (압연 뒤 · = sangros2019 카드 표 1) · 압연 곡선 그림 7b 57.0 (t ≤ 0.2) → 53.3 (0.4) → 45.3 (0.6) → 33.3 (0.8) → 21.7 % (1.0) · 본문 ≈57 → ≈22 % (p.8) · (1 − P)·h 34.4 → 31.3 µm (−9 %) | 카드 §12 · digitized.csv | [판독] · [인쇄] · [카드 산술] | 액체 LIB · SE 없음 · 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 과 다른 문헌 값 · 판정 · 맞춤에 쓰지 않음

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] lyu2025_… | 원문: 파쇄는 경고뿐 (*"it is necessary to ensure that the stress in the direction of the electrode thickness is less than the fracture stress of the particles during calendering"* p.11) · *"only moderate calendering can reduce the electronic resistance"* (p.10) · 다음 일 = *"an in-depth evaluation of the different structures after drying in order to adjust the drying process and its influence on the subsequent calendering process"* · 전기화학 · 열전도 분석 가능성 (p.11) · 카드 §10 · §17: 탈압 · 수송 수치 · 결합 · 감쇠 값 · 입자 수 · V_reg 없음 | 카드 §10 · §15 · §17 | [인쇄] | 탈압 · 되돌아옴 계산 자체가 없다

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Y. Lyu, S. Dong, L.T. Gao, Z.-S. Guo, Int. J. Electr. Power Energy Syst. 165 (2025) 110521)
- [k] lyu2025_… | **말 없음** — DEM 의 한계 (구 · 점접촉 · 겹침 · 조밀 영역) 를 말하지 않는다.  가까운 문장: *"Both AM and CBD particles are assumed to be spherical for simple."* (p.4) · *"direct numerical description of the fluid phase is avoided by utilizing a variety of fluid substitution models, which greatly reduces simulation time and computational cost [28]"* (p.4) · *"The selection of an appropriate contact model from numerous available options is of importance in DEM."* (p.3) · 다른 DEM 비판: *"randomly generated DEM models that do not consider the final structure state of drying are inappropriate for calendering simulation analysis"* (p.2) — 출발 상태의 한계 | 카드 §15 (i) | [인쇄] | 모델 물리의 한계 진술 아님

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = 위와 같음)
- [l] lyu2025_… | 이유 논의 없음 · 계산에 소성 없음 — 접촉 = 탄성 + 마찰 + 감쇠 (식 3–14) · 결합 = 선형 탄성 + 최대 응력 (식 15–22) · 우회 = **무른 CBD 상 (E 0.65 GPa · AM 의 1/218) + 결합** 으로 압밀 흡수 · 맞춘 값 0 (표 1 문헌) · 검증 = 그림 3 (DEM 누른 채 ↔ 실험 압연 뒤) · 비용 (입자 수 · 시간) 미기재 — 입자 수 [카드 산술 · 추정] AM ≈960–1050 · CBD ≈2.7–3.0 × 10⁴ | 카드 §15 (ii) · §12-3 | [인쇄] · [카드 산술] | 소성 · 형상 변화 · 파쇄를 넣는 어려움에 대한 원문 문장 없음

## m — 받아들일 통찰
- [m] lyu2025_… | **검증 상태 섞임을 결과 전에 막는다** — 그림 3 이 같은 압력 칸에 DEM (누른 채) 과 실험 (압연 뒤 · sangros2019 표 1) 을 넣었다 → 우리 등록 칸 = 압력 + 상태 + 연산자 + 측정 영역 | 단계 0 | 카드 §11 [45] · §13-3
- [m] lyu2025_… | **고체 보존 자기 점검 (1 − ε)·두께 = 상수** — 이 논문은 0.430 × 80 = 34.4 ↔ 0.783 × 40 = 31.3 µm (−9 %) 로 어긋난다 (측정 영역 미기재) → 우리 기공 보고마다 한 줄로 붙이면 연산자 · 영역 실수가 바로 보인다 | 단계 0 · 단계 5 | 카드 §12-3
- [m] lyu2025_… | **'압력' 읽기 두 개를 같이 적는다** — 벽 반력 ÷ 단면 (판 121 · 집전체 140 MPa) ↔ 접촉 virial σ_zz (164 MPa) 이 1.36 배 · 위 · 아래 벽도 ≈15 % 다르다 → 우리 MPM wallP ↔ σ_zz · DEM 판 압력 규약 등록과 같은 질문 (방향은 MPM 부피 평균 희석과 반대 — V 정의에 달림) | 단계 0 · 후보 A′-0 | 카드 §12-3 · 그림 9
- [m] lyu2025_… | **출발 상태가 압밀 앞 구간을 정한다** — 건조 끝 거친 위 표면 때문에 t ≤ 0.2 동안 기공 57.0 % 그대로 · 응력은 t ≈ 0.15–0.2 에야 서고 · 배위수는 먼저 3.6 → 2.28 로 떨어진다 → 우리 침대도 판 접촉 시작점 · 위 표면 처리를 결과 전에 적는다 | 단계 5 | 카드 §13-2 · 그림 7b · 7c · 9a

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] Sun W, Huang C. Elucidating the effect of electrode calendering on electrochemical performance using 3D image-based modelling. J Power Sources 2024;611:234774. (원문 참고 [47] 그대로) | h — 압연 미세구조 · 기계 성질의 유한요소 계산 (원문 p.2 *"developed a finite element model …"*) = DEM 밖 연속체 선례 · 단계 7 (전기화학) | litdb 확인: papers/ ls · '234774' · 'Elucidating the effect of electrode calendering' grep 0 · wishlist 0
- [n] Xu J, Hu H, Zhu L, Li X, Xiao L, Jung J-C-Y, et al. Pore-scale modeling and investigation on the effect of calendering on lithium-ion battery cathodes. J Storage Mater 2024;77:109939. (원문 참고 [48] 그대로 · 학술지 이름 인쇄 그대로) | 단계 7 · i — 이 논문이 '과압연 → 이온 저항↑' (p.10) 과 '압연할수록 셀 성능↑' (p.2) 을 같은 [48] 에 귀속 → 원문으로 어느 쪽인지 닫을 자료 · 카드 L22 정정의 근거 | litdb 확인: '109939' · 'Pore-scale modeling and investigation' grep 0 · wishlist 0
- [n] Zhang J, Sun J, Huang H, Yuan Z. Influence of calendering process on the structural mechanics and heat transfer characteristics of lithium-ion battery electrodes via DEM simulations. Particuology 2024;85:252–67. (원문 참고 [50] 그대로) | 흐름 밖: DEM 압연 구조의 **열전달** (우리 σ_thermal 망 계산의 선례) · d (구조 역학) · 표 1 입력의 출처 [45,49,50] | litdb 확인: '252–67' grep 0 · 'heat transfer characteristics' = sonzogni2024 카드의 인용뿐 · wishlist 0 ([49] Zhang 2022 는 wishlist L232 에 이미 있음)
- [n] Lischka C, Nirschl H. Calibration of Li-ion cathode materials for discrete element method simulations. Energ Technol 2022;11:2200849. (원문 참고 [54] 그대로) | e · R5 — 양극 재료의 DEM 매개변수 보정 (이 논문의 DEM · 접촉력 정의 [54,55] 의 출처) | litdb 확인: '2200849' = lischka2025 · tovar2026 카드의 인용뿐 (lischka2025 = 다른 논문) · wishlist 0
- [n] Becker V, Birkholz O, Gan Y, Kamlah M. Modeling the influence of particle shape on mechanical compression and effective transport properties in granular lithium-ion battery electrodes. Energ Technol 2021;9:2000886. (원문 참고 [55] 그대로) | k — 입자 **모양**이 압축 · 유효 수송에 주는 영향 (구 DEM 의 한계를 정량할 자료) · 이 논문의 접촉력 분해 [54,55] 출처 | litdb 확인: '2000886' · 'influence of particle shape on mechanical compression' grep 0 · wishlist 0

## 카드 문제
- **보강 대상 카드 (`lyu2025_3d_dem_drying_calendering_lib`) — 이번에 원문과 대조해 그 자리에 정정 표지 21 곳** (옛 표기 남김 · 줄 번호 그대로): 모델 활물질 'NCM811' (원문 'NCM' · L13 · L20 · L38 · L117 · L121 · L236 · L246) · 집전체 접촉 '+230 %' (원문 문장 그대로 옮김 — 2038/897 = 2.27 → +127 % · L13 · L32 · L93 · L236) · 서론 계보 L22 (Xu [48] = 서론 '압연할수록 셀 성능↑' · Zhang [49,50] ≠ '응력 분포' · Lyu [22] 제목 = 건조 + 압연) · L29 중간 두께 60 µm 의 시각 t 0.5 (원문 없음) · L43 '실측' (원문 없음) · L56 식 (8)–(9) (δ̇ · 식 (9) k_s) · L57 식 (10) 인쇄 꼴 (1 − ν)² · 우리 쪽 출처 L120 · L163 (Minnmann = 원장 CL-94 출처 철회) · L213 (Cronau '단결정' = CL-91 · SELF-51).
- 다른 정본 카드의 lyu2025 2 차 인용 — 원문과 다른 것 없음: `lyu2026_two_layer_gradient_electrode_calendering_dem_fem` L90 (표 1 · 94 : 6) · L180 (건조 끝 구조) · L321 (식 21–22 의 굽힘 / I · 비틀림 / J) · L353 (ref [82] 서지) · `lippke2023_dem_drying_structure_formation_lib` L644 (142 GPa) · L658 ('Hertz류' 는 원문 이름이 아닌 카드 추론 수준 · 고치지 않음) · `meyer2017_…` L439 · `sonzogni2024_…` (정독 122 기록 = 이번 원문 확인과 같다: 서론 [46] 문장 같음 · 식 (6) [46] 귀속은 원문 인용 문제).
- 원문 자체 문제 (카드 문제 아님 · 판정 안 함): [25]–[27] 이름 ↔ 목록 번호 한 칸씩 어긋남 · [26] (목록 = 수계 양극 CGMD) 에 NMP · PVDF 사례 조성을 귀속 · [46] 식 (6) · [56] So 2021 결합 모델 (so2021 카드 L58 = cohesive 융착 결합) · [57] 200 MPa 의 성격 (stershic2015 카드) · [32] '수은 압입 57 %' (meyer2017 카드: 57 % = 기하 기공) · [48] 서론 ↔ p.10 방향 · 'an increase of approximately 230 %' · 본문 'Fig. 8a' (= 그림 9a · p.11 두 번) · 축 이름 'Domensionless' (그림 8) · 'Dimensionles' (그림 9b) · 식 (6) ↔ (14) 차원 · 그림 6 끝 3.45 ↔ 본문 3.6 · 그림 7c 끝 8.10 ↔ 본문 8.3 · (1 − P)·h 9 % 어긋남 · [41] 'spproach' (목록 그대로).
- 받은 자료 쪽: inbox 영상 파일의 Sup 번호가 원문 S 번호와 거꾸로다 (Sup4 = S1 건조 3D · Sup3 = S2 건조 접촉망 · Sup2 = S3 압연 3D · Sup1 = S4 압연 접촉망 — 정지 화면으로 맞춤 [관찰]) · 그림 폴더의 정지 화면 이름은 원문 S 번호 (`figures.json` src = 실제 파일 이름).
