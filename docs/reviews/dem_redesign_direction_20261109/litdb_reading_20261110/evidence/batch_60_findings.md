# 배치 60 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` (원문 = 출판본 10 쪽 + SI mmc1.docx (그림 S1 · S2 · 표 S1 · S2) + 보충 영상 셋 (mmc2–4.mp4 · 각 2.4 s · 72 프레임 — 본문 언급 없음) · 그림 크롭 51 장 = 도구 8 (그대로) + 손 43 (패널 12 · SI 5 · 식 9 · 근거 문단 17) · 다시 자름 3 (식 4 · 근거 문단 2) + 같은 규칙 경계 다듬음 8 · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 96 행 — PDF 안 원본 300 dpi JPEG 를 눈금선 · 틀선으로 보정).
서지 (k · l 인용용) = Ben Hadj Ali S., Alabdali M., Viallet V., Seznec V., Franco A. A., *A computational workflow for the simulation of solid state battery electrodes from manufacturing to electrochemical performance*, J. Power Sources 630, 236131 (2025), DOI 10.1016/j.jpowsour.2024.236131 (CC BY 4.0).
⚠ 계산만 (실험 대조 0) · 재료 = NMC622 + Li₆PS₅Cl + CBD 38–40 vol% (습식) · 압력 축 없음 (두께 감소 0 · 20 · 35 %) · 역학 없음 (응력 · 부피 변화 · 되튐 · 탈압 0).
쪽 = 인쇄 쪽 = PDF 쪽 (1–10) · SI 쪽 = LibreOffice 변환 PDF 의 쪽.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode | **없음** — 순수 SE 침대 · 압력 · 진밀도 없음 (NMC622 ρ 4.77 g/cm³ 만 · 표 S2) | 카드 §3-1 · §3-3 · 표 S2 | [인쇄] | 복합 양극만 · 습식 CBD 38–40 vol%

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] benhadjali2025_… | **없음** — 넘긴 구조 = 목표 두께 그대로 (표 S1 두께 36.8 · 29.9 µm = 46 × 0.80 · × 0.65 → 되튐 없음) · 판 분리 · 이완 · 응력 서술 없음 · 전기화학은 *"without the application of any external forces, with the calendering process applied exclusively before the electrochemical simulation"* | 카드 §3-2 · §4-3 (iv) · 원문 p.3 · 표 S1 | [인쇄] · [카드 산술] · [미확인] | 원 CGMD 논문 (alabdali2023 카드) 도 'springback n/a' [다른 카드]

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- 이 배치에 없음 (역학 물성 0 — 표 S2 는 전기화학 · 전도도뿐 · 본문 'plastic' 낱말 0 회)

## d — 단단한 입자 + 무른 입자 혼합 압축의 하중 몫 · 재밍

- [d] benhadjali2025_… | 하중 몫 · 재밍 숫자 **없음** · 정성 하나: 원 CGMD 모델이 >35 % 압연에서 *"partial occupation of the volume of CBD particles by other materials due to high pressure"* → 전기전도 감소 (p.2) — 강체 구 압밀의 겹침 인공물 | 카드 §3-1 · §4-3 (i) · 원문 p.2 | [인쇄] | 압력 · 응력 출력 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안

- [e] benhadjali2025_… | 범위 = **캘린더링 (두께 감소) ≤35 %** 만 사용 (그 위에서 CBD 부피 잠식 → 전기전도 감소 · [13] 에서 논의) · 대안 없음 — 겹친 부피를 우선순위 (AM → SE → CBD) 로 재배정하는 **기하 후처리** 로 모양만 '불규칙' 하게 (맞춘 값 0) | 카드 §3-1 · §3-2 · 원문 p.2–3 | [인쇄] | 접촉 법칙 (LJ + Hertz) 자체는 이 논문에 없음 [13] 몫 · 압력 축 없음

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙

- 이 배치에 없음 (MPM 없음).  해상도 반례 하나: 3D 결과를 내면서 **복셀 크기 · 요소 수 · 메시 수렴을 보고하지 않음** (INNOV 복셀화 다상 메싱 [27, 28] 만 · 본문에 µm 숫자 0) — 카드 §3-2 · §13 · [미확인]

## g — 2D → 3D 전이 경고 · 증거

- [g] benhadjali2025_… | **말 없음** — 3D (+ 시간 = *"4D (3 spatial coordinates, and time)"* · 초록) 만 | 카드 §4-3 (iii) · 원문 p.1 | [인쇄] | —

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

- [h] benhadjali2025_… | ★ **선례 (전기화학 FE 로)**: 습식 CGMD 제조 모의 (LAMMPS · 슬러리 → 건조 → 평판 등속 하강 캘린더링 · 0 · 20 · 35 % 두께 감소 · [13]) → 겹침 우선순위 후처리 (AM → SE → CBD · *"For each instance of overlap between AM and CBD or between AM and SE, we adjust the volume calculations by reducing the volume attributed to the CBD and adding this reduced volume to the AM or SE, respectively"*) → INNOV 복셀화 다상 체적 메시 → COMSOL 3D 반쪽 셀 방전 (AM 안 3D Fick · AM/CBD/CC 옴 · SE 옴 t⁺ = 1 · AM–SE BV · C/5–C/50) | 카드 §3-2 · §3-3 · §7-1 · 원문 p.2–4 · 그림 1 · 2 · S2 | [인쇄] | 역학 FE 아님 · 복셀 크기 · 메시 [미확인] · 실험 대조 0
- [h] benhadjali2025_… | ★ **넘긴 시점** = 캘린더링 목표 두께에 닿은 '누른 상태' (두께 = 명목 그대로 → 되튐 없음 [카드 산술: 46 × 0.80 = 36.8 · × 0.65 = 29.9]) · 기하만 (응력 · 접촉력 · 겹침량 안 넘김) · 전기화학은 외력 없이 | 카드 §3-2 · 원문 p.3 · 표 S1 | [인쇄] · [카드 산술] | 판 분리 · 이완 여부 [미확인] · 우리 사슬 (DEM 300 MPa 도달 후 판 고정 이완 덤프 → MPM 재압밀) 도 '누른 상태' 를 넘긴다 [우리 CLAUDE.md FAM 줄]
- [h] benhadjali2025_… | 넘김 연산자의 **부피 비보존**: (1 − ε) × 두께 38.18 → 32.02 → 28.11 µm (−16 · −26 %) · 단단한 AM 몫까지 −14–16 % · 원 논문 같은 0 % 침대 (기공 35 % · CBD ≈0.20 [다른 카드 alabdali2023]) ↔ 표 S1 (기공 17 · CBD 40 %) | 카드 §3-9 ⑤ ⑥ | [카드 산술] · [다른 카드] | 원문 설명 없음

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] benhadjali2025_… | 압력 대신 **두께 감소율** 별: 0 · 20 · 35 % → 기공 **17 · 13 · 6 %** (표 S1 · 그림 2f 판독 17.0 · 12.0 · 6.1) · AM : SE : CBD 22 : 21 : 40 → 23 : 25 : 39 → 29 : 27 : 38 vol% · 두께 46 → 36.8 → 29.9 µm | 카드 §3-1 · 표 S1 · 그림 2c–f | [인쇄] · [판독] | CBD 를 고체로 셈 · 질량 비보존 · 압력 없음 · 습식 CBD 40 vol% — 압밀 앵커로 쓰지 않음

## j — 카드가 스스로 적은 한계 중 가압 · 탈압과 닿는 것

- [j] benhadjali2025_… | 모델 쓸 범위 ≤35 % 압연 (p.2) · AM 부피 변화 미반영 (*"we did not account for the volume change in AM during lithiation"* · 부산물 · 접촉 손실이 *"significant uncertainties"* 라 깨끗한 AM 매개변수 · p.4) · 단축 압연 → *"suboptimal tortuosity, even at low porosity levels"* · *"need for alternative calendering techniques (e.g. isostatic calendering)"* · 등방 압축이 사이클 중 AM–SE 응력을 줄인다 (DEM 선행 [32] 인용) · 앞으로 = AM 부피 변화 · 실험 대조 (p.9) | 카드 §0 ⑦ · §4-3 · 원문 p.2 · p.4 · p.9 | [인쇄] | —
- [j] benhadjali2025_… | 원문 안 어긋남 15 건 (카드 §3-9) — 그림 2 캡션 '10 %' · 표 S1 머리 '10' · 표 S1 ↔ 그림 2c/2f 1 %p · 부피 비보존 · 원 논문과 상 분율 차 · GeoDict ↔ COMSOL 입력 σ 차 · 결론 '200 mAh/g' (= C_spec 입력) · 피복 % ↔ 비계면적 분모 · δ_e 원 논문과 ≈100 배 · 참고문헌 [25] = [37] · 활성화 과전압 강조 ↔ 그림 6 · 영상 시간 · 식 (7) ↔ 그림 8 (Cal0 9 %) | 카드 §3-9 | [인쇄] · [판독] · [카드 산술] | —

## k — DEM 의 한계 (인용할 서지 = Ben Hadj Ali et al. 2025, J. Power Sources 630, 236131)

- [k] benhadjali2025_… (Ben Hadj Ali et al., *J. Power Sources* 2025) | 한 문장: *"The usability of this model is limited for calendering degrees under or equal to 35 %, as it was discussed in Ref. [13] because above 35 % a decrease in the electrical conductivity was observed due to the partial occupation of the volume of CBD particles by other materials due to high pressure."* (p.2) — 강체 구 (CGMD) 압밀을 더 누르면 겹침이 다른 상의 부피를 잠식하는 인공물 · 그리고 *"The transformation from spherical to irregular particle shapes in our FEM electrochemical modeling environment is a result of a specific postprocessing step performed on the CGMD simulation data."* (p.2–3) — 입자 모양은 모의 안에서 안 변한다 | 카드 §4-3 (i) · 원문 p.2–3 | [인쇄] | 겹침 · 상대밀도 상한 · 접촉 독립 가정 · 보정값 지위에 대한 말 없음 · 'DEM' 낱말은 [32] 인용 한 번 (p.9)

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용 (인용할 서지 = Ben Hadj Ali et al. 2025, J. Power Sources 630, 236131)

- [l] benhadjali2025_… (Ben Hadj Ali et al., *J. Power Sources* 2025) | **말 없음** ('plastic' 0 회) · 서론만 *"thiophosphate-based SEs stand out also due to their unique mechanical properties, especially their malleability caused by low Young's moduli, which allows the electrodes to be densified at low temperatures without the need for energy-intensive sintering processes [11,12]"* (p.2) · 우회 = **기하 후처리** (겹침 우선순위 · CBD 부피 이동 → *"irregular shapes"* · 맞춘 값 0 · 검증 0) · AM 부피 변화도 불확실성 때문에 뺐다 (p.4) · 비용 = COMSOL 1 노드 500 GB RAM · Xeon E5-2680 v4 28 코어 (실행 시간 · 자유도 [미확인]) · GeoDict = 표준 데스크톱 (p.4) | 카드 §4-3 (ii) · §0 ⑤ · 원문 p.2–4 | [인쇄] · [미확인] | 소성 모델 없음 — '소성이 어려운 이유' 의 근거로는 쓸 수 없고 '모양 변화를 기하 후처리로 우회한 사례' 로만

## m — 받아들일 통찰

- [m] benhadjali2025_… | **넘김 연산자 + 상별 부피 보존표**: 겹침 규칙 (우선순위 · union · 부피 이동) 을 글로 적고 넘기기 전 ↔ 후 상별 (분율 × 두께) 를 같이 낸다 — 그들 규칙은 (1 − ε)·t 를 −26 % 만들었다 (AM 몫까지) | 단계 0; 단계 7; 흐름 밖: DEM → MPM 씨앗 · MPM → STEP3 래스터 넘김 | 카드 §3-9 ⑤ · §9 ① · 표 S1 · p.3
- [m] benhadjali2025_… | **'쓸 범위' 문지기**: 압밀 정도별 수송량 (전도도) 이 단조가 아니면 강체 구 겹침 인공물로 보고 그 압밀은 쓰지 않는다 (그들 35 % 한계의 근거) — 결과 전 등록에 | 단계 5; 후보 D0 | 카드 §8 단계 5 · p.2
- [m] benhadjali2025_… | **손실 분해 두 곡선 보고 꼴** (평균 활성화 과전압 · SE 전위 vs 용량 · 세 C-rate): 그들 그림 6 판독으로 압밀 효과는 SE 옴 쪽이 압도 (C/10 · 50 mAh/g 에서 SE 전위 0.090 → 0.017 V (−81 %) ↔ 활성화 0.079 → 0.071 V (−10 %)) — 본문은 활성 면적을 앞세웠다 | 흐름 밖: STEP4 분극 분해 보고 · 단계 7 | 카드 §3-6 · §9 ⑤ · 그림 6a/6b
- [m] benhadjali2025_… | **함정 — 계산마다 다른 입력 σ · 다른 이름의 τ**: GeoDict (σ_AM 0.005 · σ_CBD 15.93 S/m · σ_SE 1.25 mS/cm) ↔ COMSOL (100 · 200 S/m · 0.7) · *"geometric tortuosity"* = √(φ_SE/D_eff) = 우리 tau (√tau2) · *"McMullin number"* = f (문헌 1/f 의 역수) → 문헌 값을 옮길 때 우리 키로 다시 이름 붙이고 STEP3 · STEP4 의 σ 표 일치를 매니페스트로 보인다 | 흐름 밖: τ 이름 규약 · STEP3/STEP4 입력 일치 | 카드 §3-4 · §3-9 ⑦ · §7-3 · 식 (7) · (9)

## n — 논문 에이전트 후보

- [n] Schmidt, C.P.; Sinzig, S.; Gravemeier, V.; Wall, W.A. A Three-Dimensional Finite Element Formulation Coupling Electrochemistry and Solid Mechanics on Resolved Microstructures of All-Solid-State Lithium-Ion Batteries. Comput. Methods Appl. Mech. Eng. 2023, 417, 116468, doi:10.1016/j.cma.2023.116468. | h · 후보 B · j — 해상 미세구조 위 전기화학 + 고체역학 결합 FE (이 논문이 못 한 역학 결합) · 표 S2 CC/AM 접촉 저항 2 × 10⁻³ Ω m² 의 출처 [S4] (카드 §12 · §3-3) | litdb 확인: `ls papers` 'schmidt' 없음 · grep `cma.2023.116468` · 'Sinzig' 0 → 카드 없음 (후보 표에도 없음)
- [n] M. Alabdali, F.M. Zanotto, B. Notredame, V. Viallet, V. Seznec, A.A. Franco, Experimental and computational analysis of slurry-based manufacturing of solid-state battery composite cathode, Batt. Supercaps (2024) e202400709, https://doi.org/10.1002/batt.202400709. | h · i — 같은 습식 ASSB 사슬의 실험 + 계산 (원문 [23] · 슬러리 · 건조 · 캘린더링 세부를 맡긴 논문) · 이 사슬의 실험 검증점이 있을 자리 (카드 §12) | litdb 확인: grep `batt.202400709` · 'slurry-based manufacturing of solid' 0 → 카드 없음
- [n] Naik, K.G.; Jangid, M.K.; Vishnugopi, B.S.; Dasgupta, N.P.; Mukherjee, P.P. Interrogating the role of stack pressure in transport-reaction interaction in the solid-state battery cathode. Adv. Energy Mater. n/a, 2403360, doi:10.1002/aenm.202403360. (서지 일부만 — 권 *"n/a"* 그대로) | d · j · 단계 6 — 적층압이 양극 수송-반응에 주는 효과 (원문 [38] · p.5 운동학 ↔ 열역학 영역 근거) (카드 §12) | litdb 확인: grep `aenm.202403360` · 'stack pressure in transport' 0 → 카드 없음
- [n] R. Ruess, S. Schweidler, H. Hemmelmann, G. Conforto, A. Bielefeld, D.A. Weber, J. Sann, M.T. Elm, J. Janek, Influence of NCM particle cracking on kinetics of lithium-ion batteries with liquid or solid electrolyte, J. Electrochem. Soc. 167 (2020) 100532, https://doi.org/10.1149/1945-7111/ab9a2c. | 흐름 밖: STEP4 입력 (D_AM · V0 · R_CT 의 출처 [31]) · R7 (AM 균열 ↔ 운동학) (카드 §3-3 · §12) | litdb 확인: `ls papers` 'ruess' 없음 · `ab9a2c` 는 `stallard2022_cathode_mechanical_properties_review` 의 인용뿐 → 카드 없음
- [n] M. Chouchane, A. Rucci, A.A. Franco, A versatile and efficient voxelization-based meshing algorithm of multiple phases, ACS Omega 4 (2019) 11141–11144, https://doi.org/10.1021/acsomega.9b01279. | h · 단계 0 — 넘김 메싱 (겹친 구 → 상 · 복셀 크기 규칙) 의 원전 (원문 [28]) (카드 §3-2 · §12) | litdb 확인: `acsomega.9b01279` = benhadjali2026 인용뿐 → 카드 없음 · ⚠ 후보 표 N-43 에 이미 있음 (같은 이유 보강) — Bielefeld 2022 ([17] · N-89) 도 이미 후보 표에 있어 따로 적지 않음

## 카드 문제

- `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` §3-2 의 δ_e 판독 2.43 → 3.15 S m⁻¹ (= 24.3 → 31.5 mS/cm · 같은 미세구조 · 같은 입력 σ_AM 0.005 · σ_CBD 15.93 S/m) ↔ 이 논문 그림 8b · 본문 **0.24 → 0.31 mS/cm** — 비 (1.30 ↔ 1.29) 같고 크기 ≈100 배 (101 · 101 · 102) → 둘 중 한 원문의 축 단위가 틀렸거나 카드 판독 단위가 틀렸다 · alabdali2023 카드의 그림 4a 축 단위 재확인 필요 (카드는 고치지 않음).
- `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` §3-1 (0 % 침대: 두께 46 µm · ε_dry 35 % · 판독 CBD ≈0.20) ↔ 이 논문 표 S1 (같은 46 µm · 기공 17 % · CBD 40 %) — 같은 침대의 상 분율이 다르다 (CBD 나노 기공을 CBD 상에 넣었는지 원문 설명 없음) · 두 카드를 같은 표에 넣을 때 정의 표지 필요.
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L295 · §7-3 의 '이 논문 geometric tortuosity 정의 [미확인] · √(φ/f) 꼴에 가깝다' — 같은 그룹 2025 판 식 (7) τ_g = √(φ_SE/D_eff) 로 그 카드의 산술이 뒷받침된다 (2026 판 자체 정의는 여전히 미확인 · 문제 아님 · 정보 보강).
- `sankar2026_fiber_scale_dem_carbon_felt_manufacturing` L45 *"ref 64 Ben Hadj Ali 2025"* — 서지 없음 (이 논문인지 못 가림 · 서지 일부만).
- 원문 안 어긋남 15 건은 카드 §3-9 (논문 쪽 문제 · 카드 문제 아님).
