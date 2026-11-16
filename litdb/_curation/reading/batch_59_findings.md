# batch 59 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` — S. Ben Hadj Ali, A. Valisammagari, P.T. Bhutia, A.H. Dao, V. Viallet, V. Seznec, A.A. Franco, "Fully coupled mechano-electrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet processing", ChemRxiv v1 (2026-03-22 · CC-BY 4.0 · 비심사), DOI 10.26434/chemrxiv.15001135/v1 (26 쪽 · SI 미포함 — 후보 표의 출판본 ESM 90 (2026) 105304 은 이 PDF 로 확인 안 됨).
같은 그룹 CGMD 습식 제조 모의의 '두께 20 % 압연' 구조 하나를 복셀 메시로 COMSOL 에 넘겨, AM 안 응력 의존 확산 · 평형 전위 (양방향) 와 AM · SE · CBD 선형 탄성 + 리튬 고유변형을 C/10 5 사이클 동안 푼 반쪽 셀 FEM — 68 MPa · 측벽 고정 · 분리막 · 집전체 강체 · 소성 · 파괴 · 접촉 없음 · 물성 표는 SI (없음) · 검증 = 전압 곡선.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (순수 SE 압밀 자료 없음 — 실험 SE 펠릿 100 mg · 2 t (Ø10 이면 249.7 MPa [카드 산술]) 의 두께 · 기공은 인쇄 안 됨 · p.5).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 탈압 계산 **없음** — 적층압 68 MPa 를 5 사이클 내내 유지 · 제하 · 되튐 없음 · 위 경계가 *"allows for minor displacement"* 라 방전 끝 압력이 준다는 서술뿐 · 넘겨받은 CGMD 구조의 판 분리 · 되튐 서술 없음 | 카드 §4-3 (iv) · §3-2 · 논문 p.8 · p.21 | [인쇄] | 그림 4 의 두께 변화 (−0.68 → −3.29 → ≈+0.04 %) 는 탈압 되돌아옴이 아니라 리튬 고유변형 + 경계의 결과

## c — 항복 · 경도 · 크리프 값과 정의
- [c] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 값 없음 — AM · SE · CBD 선형 탄성 (식 11) · *"The plasticity as a material property is ignored in this study"* · E · ν · Ω · C_total = 표 S1 · S2 (SI · PDF 에 없음 · *"at XXX"*) · 인쇄된 물성 = NMC622 부피 변화 ~4.8 % 하나 | 카드 §3-3 · §3-4 · §13 · 논문 p.11 · p.12 · p.15 · p.23 | [인쇄] · [미확인] | 일축 항복 환산 없음 · 같은 그룹 2026-11 판 카드도 E · ν [미확인]

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (하중 몫 · 재밍 출력 없음 — AM σzz 지도 (그림 5a) 는 색 포화 · 분위수 없음 · 거시로는 겉보기 구속 탄성률 ≈10 GPa (68 MPa ↔ 두께 −0.68 % [카드 산술 §3-6]) 뿐).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (연속체 FEM · 접촉 법칙 없음 — 제조 단계 접촉은 이전 논문 [27] (정본 `alabdali2023_…`) 몫).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 아님 — FEM 복셀 메시의 크기 · 요소 수 · 수렴 미기재 · 계산 자원만 노드 하나 500 GB RAM · 28 코어 · p.8).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 3D 해상 · 2D 는 선행 분류 한 줄: *"Fully coupled models have already been reported for simplified representations, such as 1D configuration [19], 2D domains [20], single cathode particle [21–24], or following homogenized approaches"* · 3D 해상 연구가 한 방향 결합에 머문 이유 = *"due to the complexity of the multiphase microstructure and the high computational cost [25,26]"* | 카드 §4-3 (iii) · 논문 p.4 | [인쇄] | 2D ↔ 3D 정량 대조 · 경고 수치 없음 · 2D 완전결합 [20] = 정본 `taghikhani2025_…`

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | ★ CGMD (LAMMPS) 습식 제조 모의 (Alabdali 2023 [27] · 슬러리 → 건조 → 압연) 의 **'두께 20 % 압연' 구조 하나** → 복셀화 (*"overlaps between CBD and AM or between CBD and SE were handled by adding the volume of overlapping regions to AM or SE, respectively"*) → INNOV 다상 메시 → COMSOL · 넘긴 것 = **기하만** (판 분리 · 되튐 · 잔류 응력 서술 없음 · FEM 은 응력 0 + 68 MPa 경계로 출발) · 같은 구조를 [29] (전기화학) · [26] (한 방향 역학) 에서 이미 씀 | 카드 §3-2 · §7-1 · 논문 p.6–8 · p.16 | [인쇄] | 복셀 크기 · AM–SE 겹침 규칙 · 메시 수렴 [미확인] · 그림 2a 양극 44.6 µm · 40 × 40 µm ↔ 같은 구조라는 [29] 표 S1 36.8 µm · 41 × 41 µm [다른 카드 benhadjali2025] — 숫자로 같은 구조인지 확인 안 됨

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 압력별 기공 없음 — 모델 구조 기공 12 % (한 점 · '20 % 압연' · 정의 [미확인]) · 실험 양극은 3 t 로 눌렀으나 (Ø18 이면 ≈116 MPa [카드 산술]) 두께 · 질량 · 기공 미인쇄 | 카드 §3-1 · §3-2 · 논문 p.5 · p.7 | [인쇄] · [미확인] | 모델은 두께 감소율 축 (압력 축 대응 없음) · 습식 CBD 포함 구조라 랩 표준 (순수 SE 10–13 %) 과 나란히 놓지 않음

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 저자 한계: 소성 무시 (p.15) · *"a future model should include the plastic deformation and fracture of AM particles and SE, which may lead to contact loss, crack formation, and mechanical failure during cycling. The integration of damage mechanics …"* (p.22) · 위 경계가 실험 (나사 고정) 과 다름 (p.21) · 분리막 · 집전체 강체 (p.12) · Li-In 부피 변화 0 (p.16) · SEI 미반영 (p.21) | 카드 §0 ⑨ · §4-3 · §11 | [인쇄] | 제조 압밀 · 탈압은 한계 목록에도 없음 (애초 범위 밖) · 카드 해석: 이 논문의 '완전결합' 은 사이클 중 전기화학 ↔ 탄성이지 가압부터 한 모델이 아니다

## k — DEM 의 한계
- [k] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode — Ben Hadj Ali et al. 2026 (ChemRxiv preprint v1, DOI 10.26434/chemrxiv.15001135/v1) | 직접 문장 하나: 겹침 후처리가 *"implicitly considers the microporosity of the CBD, and enables the transformation of ideal spherical shapes in CGMD into more realistic, irregular shapes of all the composite cathode phases"* (구 모양이 비현실적이라는 전제) · 겹침 상한 · 밀도 상한 · 연화 · 접촉 독립 가정에 대해서는 **말 없음** | 카드 §4-3 (i) · 논문 p.8 | [인쇄] | 모양은 역학이 아닌 기하 후처리로 만든다 — 'SE 형상 변형' (R6) 의 근거로 쓰지 않는다

## l — 소성변형이 왜 어려운가
- [l] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode — Ben Hadj Ali et al. 2026 (ChemRxiv preprint v1, DOI 10.26434/chemrxiv.15001135/v1) | 이유 · 우회: *"most of the active material is expected to operate predominantly within the elastic regime under typical cycling conditions [17,18]. This simplification is commonly employed in electrochemical-mechanical modelling studies … as it allows stress evolution investigation with minimum computational cost."* (p.11) · *"The plasticity as a material property is ignored in this study, however at the electrode scale, due to microstructural rearrangement it might have an irreversibility in the material response."* (p.15–16) · 3D 해상 결합이 드문 이유 = *"the high computational cost"* (p.4) · 우회 = 선형 탄성 + 리튬 고유변형 (역학 맞춤 값 0 · 물성 SI [미확인]) · 비용 = 노드 하나 500 GB RAM · 28 코어 · C/10 5 사이클 (실행 시간 · 요소 수 [미확인]) · 앞으로 = 소성 · 파괴 · 손상 역학 (p.22) | 카드 §4-3 (ii) · §3-4 · 논문 p.4 · p.8 · p.11 · p.15–16 · p.22 | [인쇄] | '이유' 는 비용 · 관행뿐 (입자 모양 변화 · 이웃 접촉 상호작용 · 이력 설명 없음) · 역학 검증 0

## m — 받아들일 통찰
- [m] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 무엇: 사이클 (고유변형) 응력을 낼 때 **경계 (측벽 미끄럼 / 고정 · 위판 압력 / 변위 · 분리막 강체 여부) 를 결과 전에 등록** 하고 모델 값이 아니라 측정 고정 틀 축 응력과 견준다 · 어디: 단계 6 · 후보 A′-0 · 결과 전 대조 항목 · 왜: 순수 압력 위면 + 미끄럼 벽이면 집전체 면 평균 σzz 가 인장 (+35 MPa) 이 될 수 없다 (힘 평형) — 그들 진폭 ≈113 MPa 는 구속 방식의 몫 · 측정 (정본 `koerver2018_…`: LTO/NCM-811 ≈ −0.05 MPa · InLi ≈ +1.06 MPa) 과 2–3 자릿수 차 | 카드 §3-9 ③ · §8 · 논문 p.12 · p.16 · 그림 2a · 4a | [인쇄] · [판독] · [카드 해석] | 물성 미공개 · 재료 (NMC622 ↔ NCM-811) · 셀이 달라 자릿수만
- [m] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 무엇: '비가역' 을 쓸 때 **정의 (시작 ↔ 끝 차 · 사이클 경계 처리 · 쌓임 여부) 와 모형 안의 기전 이름 (소성 · 접촉 열림 · 기공 닫힘)** 을 같이 적는다 · 어디: 단계 0 · 단계 6 · 왜: 그림 4 는 다섯 사이클마다 같은 꼴 (σzz 35.1–35.5 / −109.4 – −109.8 MPa) 로 되풀이되고 사이클 경계에서 ≈ −76 MPa · −0.71 % 로 되돌아가는데 [판독] 본문은 *"only during the first cycle"* · '재배열 · 영구 압밀' (탄성 연속체에 없는 기전) 이라 적는다 · 방전 끝 두께는 처음보다 두껍다 | 카드 §3-6 · §3-9 ④ ⑤ · 논문 p.17–18 · p.22 · 그림 4 | [판독] · [카드 해석] | 원인 (휴지 · 경계 재설정) [미확인]
- [m] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 무엇: 장 지도의 최대값은 **색 막대 끝이 아니라 분위수 · 포화 몫** 으로 보고 · 어디: 단계 7 · 흐름 밖: MPM 응력장 보고 (EM-06) · 왜: 결론 *"local stress magnitudes reaching up to 2.5 GPa in compressive and 1 GPa in tensile"* = 그림 5 색 막대 양끝 (−2.5 · +1 × 10⁹ N/m²) · 양끝 색 포화 | 카드 §3-7 · 논문 p.19 · p.22 · 그림 5 | [판독] · [카드 해석] | —
- [m] benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode | 무엇: STEP4 에 응력 결합 (μ − Ωσ_h · E_eq = −μ/F) 을 넣기 전 **크기 견적** — Ωσ_h/F ≈ 3 mV (Ω 3 cm³/mol · |σ_h| 100 MPa [카드 산술 · Ω = koerver2018 카드 그림 2b 판독]) · 그들 평균 과전압 차 ≈2.3 mV (평탄부 −53.3 ↔ −51.0 mV) · 끝 용량 151.9 ↔ 155.6 mAh/g [판독] · 어디: 흐름 밖: STEP4 율속 · 반응 분포 · 왜: 식 (5) (6) (9) · 그림 3b | 카드 §3-3 · §3-5 · 논문 p.9–10 · p.13–14 | [인쇄] · [판독] · [카드 산술] | 비교 조건 (율 · 충방전 · 사이클) [미확인] · 물성 미공개

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] C.P. Schmidt, S. Sinzig, V. Gravemeier, W.A. Wall, A three-dimensional finite element formulation coupling electrochemistry and solid mechanics on resolved microstructures of all-solid-state lithium-ion batteries, Computer Methods in Applied Mechanics and Engineering 417 (2023) 116468. https://doi.org/10.1016/j.cma.2023.116468. (원문 참고 [24] · 인쇄 그대로) | h · f · 후보 B — 3D 해상 미세구조 위 전기화학 + 고체역학 결합 FE (이 논문이 *"single cathode particle [21–24]"* 로 묶은 것 · 이 논문의 '3D 해상 완전결합 = 새로움' 주장 확인) · 카드 §0-1 · §3-9 ⑩ | papers/ 목록 + DOI `cma.2023.116468` · "Sinzig" grep — 카드 없음 (benhadjali2025 카드에 인용만)
- [n] S. Mičky, E. Šimon, J. Todt, K. Végsö, P. Nádaždy, P. Krížik, E. Majková, J. Keckes, J. Li, P. Siffalovic, Operando Spatial and Temporal Tracking of Axial Stresses and Interfaces in Solid-state Batteries, Small 20 (2024) 2307837. https://doi.org/10.1002/smll.202307837. (원문 참고 [6] · 인쇄 그대로) | 결과 전 대조 항목 · b — 사이클 축 응력 · 계면의 operando 측정 (모델 σzz 와 견줄 실측 후보) · 카드 §8 결과 전 대조 항목 | papers/ 목록 + DOI `smll.202307837` grep — 카드 없음
- [n] W. Zhang, D. Schröder, T. Arlt, I. Manke, R. Koerver, R. Pinedo, D.A. Weber, J. Sann, W.G. Zeier, J. Janek, (Electro)chemical expansion during cycling: monitoring the pressure changes in operating solid-state lithium batteries, J. Mater. Chem. A 5 (2017) 9929–9936. https://doi.org/10.1039/C7TA02730C. (원문 참고 [10] · 인쇄 그대로) | 결과 전 대조 항목 — 운전 중 셀 압력 변화 측정 (Koerver 2018 앞선 측정) · 카드 §8 | papers/ 목록 + DOI `C7TA02730C` grep — 카드 없음
- [n] N. Iqbal, J. Choi, C. Lee, H.M.U. Ayub, J. Kim, M. Kim, Y. Kim, D. Moon, S. Lee, Effects of Diffusion-Induced Nonlinear Local Volume Change on the Structural Stability of NMC Cathode Materials of Lithium-Ion Batteries, Mathematics 10 (2022) 4697. https://doi.org/10.3390/math10244697. (원문 참고 [23] · 인쇄 그대로) | m · 흐름 밖: 고유변형 입력 — 식 (15)–(16) Ω · λ 의 원전 (식 (16) 둘째 꼴 오기 확인 · 할선 Ω 의 x 범위) · 카드 §3-3 · §3-9 ① | papers/ 목록 + DOI `math10244697` · "Iqbal" grep — 카드 없음 (benhadjali2026 WIP 카드에 인용만)
- [n] Y. Shao, X. Shao, L. Sang, H. Liu, A Fully Coupled Mechano-Electrochemical Model for All-Solid-State Thin-Film Li-Ion Batteries with Non-Porous Electrodes: Effects of Chemo-Mechanical Expansions on Battery Performance and Optimization Strategies for Stress Evolution, J. Electrochem. Soc. 169 (2022) 080529. https://doi.org/10.1149/1945-7111/ac8b3a. (원문 참고 [19] · 인쇄 그대로) | j · m — 1D 완전결합 선례 (같은 결합 꼴의 단순 기하 검산 후보) · 카드 §4-3 (iii) | papers/ 목록 + DOI `ac8b3a` grep — 카드 없음
- (참고 · 후보로 세지 않음) 원문 참고 [26] (Batteries & Supercaps 9 (2026) e202500540) · [36] (그 ChemRxiv 판) = **후보 표 N-42 에 이미 있다** · [38] Lundkvist 2024 · [17] Naik 2023 · [7] Naik 2024 = **wishlist 에 이미 있다** · [8] · [20] · [27] · [29] = 정본 카드 있음.

## 카드 문제
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L443 (참고 [31]) — 저자 7 · 순서 · 제목 = 원문 (p.2) 과 같다 · **학술지 · 권 · 논문 번호 · DOI (Energy Storage Materials 90 (2026) 105304 · 10.1016/j.ensm.2026.105304) 는 이 PDF (ChemRxiv v1 · 10.26434/chemrxiv.15001135/v1) 로 확인 불가** · "★ … (이 논문 FEM 의 정의 · 물성 · 경계 · 검증)" 가운데 **물성은 원 논문 본문에도 없다** (SI) · "카드 없음" 은 이 카드로 낡음 (고치지 않음 · 🔗 관련 카드 한 줄만 더함).
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L18 (zhang2026 줄 *"그 둘의 정본 카드는 없음"*) · L441 (참고 [29] *"카드 없음"*) — 둘 다 낡음 ([29] = `benhadjali2025_…` · [31] = 이 카드 · 고치지 않음).
- `zhang2026_polymer_electrolyte_modeling_perspective` L64 — *"Ben Hadj Ali 2025 (…; 완전결합 기계-전기화학, ref 164)"*: ref 164 = 이 논문 · 게시 2026-03-22 (ChemRxiv) → "2025" 가 ref 164 에도 걸리면 연도가 다르다 (Zhang 원문의 표기인지는 그 카드로 못 가림) · L122 제목 조각 · 저자 처음 · 끝은 원문과 같다 · *"정본 카드 없음"* 은 낡음 (고치지 않음).
- (기록만 · 문제 아님) `benhadjali2026_wip_vs_cup_…` §4-3 의 λ = (V_x/V₀)^{1/3} − 1 은 맞다 — 원 논문 식 (16) 의 둘째 꼴 ((V_x − V₀)/V_x + 1)^⅓ − 1 이 오기다.
- (내 몫 아님 · 보고만) `litdb/figures/_sources.json` 의 `choi2018_fibsem_3d_composite_cathode_microstructure_tpb_pore_decomposition` 항목 figures **8** ↔ 그 `figures.json` 항목 **32** (pdf_map 주석도 "크롭 32 장") — 이번 추출 도구 실행이 32 로 고치려 해 되돌렸다 (이 커밋에는 내 항목만).
- 후보 표 (`litdb/_curation/S8_candidates.md`) N-17 행 — 서지는 출판본 (ESM 90 (2026) 105304) 으로 적혀 있고 받은 PDF 는 ChemRxiv v1 프리프린트 (2026-03-22 · 비심사 · SI 없음) — 저자 · 제목은 같다.
