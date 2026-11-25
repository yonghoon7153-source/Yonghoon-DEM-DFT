# batch 145 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-23 · 후보 표 밖 U-1123-2)

대상: `cho2026_pore_network_homogeneity_powder_compacted_se_separator` — H.-R. Cho · H.-J. Kim · J.-S. Kim · B. J. Park · Y. Kim · D. Lee · J. Kim · H. Kim · S.-K. Jung\* (서울대 · 공동 1저자 Cho · H.-J. Kim), "Pore-network homogeneity for mechanically reliable powder-compacted solid-electrolyte separators", *ChemRxiv* (2026) v2 · 게시 2026-10-08 · **동료 심사 전** · CC-BY 4.0 · DOI 10.26434/chemrxiv.15009882/v2 (PDF 66 쪽 = 본문 + 그림 + SI).
결정상 · σ 가 비슷한 상용 argyrodite 분말 셋 (넓은 PSD = BD · 중간 SE-2 · 좁은 PSD = ND) 의 순수 SE 펠릿 기공 (110–440 MPa) · FIB-SEM 공극망 · 나노압입 지도 · Sn 음극 전셀 사이클 · 사후 단면 + 이미지 기반 선형 탄성 FEM (2D 평면변형 · 3D GrainGeo) (DEM · MPM 없음).
쪽 = PDF 쪽 (원고에 인쇄 쪽 번호 없음) · 판독 원자료 = `litdb/figures/cho2026_pore_network_homogeneity_powder_compacted_se_separator/digitized.csv` (123 행 · 원 래스터 화소 · 그림 S16 은 300 dpi 크롭) · 고른 의도 대조 = **채움** (카드 §0-1 — 압력 · 기공률 · 측정법 · 진밀도 1.64 · 원고 표지 채움 · 두께는 범위 0.9–1.3 mm 만 = 일부).
인용 서지 (질문 k · l 용): Cho et al., ChemRxiv (2026), DOI 10.26434/chemrxiv.15009882/v2 (preprint, not peer reviewed).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
- [a] cho2026_pore_… | 표 S1 (평균 ± SD · 조건마다 펠릿 5 개): BD 13.78 ± 0.17 / 7.88 ± 0.23 / 4.94 ± 0.30 / 1.73 ± 0.32 % · SE-2 21.84 / 13.84 / 8.04 / 3.69 % · ND 23.75 ± 1.21 / 15.82 ± 0.91 / 9.28 ± 0.44 / 6.19 ± 0.46 % (110 / 220 / 330 / 440 MPa) | 카드 §3-2 · 표 S1 (p.64) · 그림 1c | [인쇄] | 진밀도 = Li₆PS₅Cl **1.64 g/cm³** (그림 S3 글 p.32 · 출처 인용 없음 · 분말 조성 미기재) · 질량 기준 (ρ = m/(πr²t)) · **누른 뒤 다이 안 (꺼내지 않음)** · 하중은 뺀 뒤 (그림 S2 사진 — 글에 없음) · 200 mg · ⌀13 mm PEEK · 2 분 · 상용 argyrodite (PSD 가 랩 분말과 다름 → 랩 표준과 다른 문헌 값)
- [a] cho2026_pore_… | 300 MPa 보간 (220–330 사이) 선형 ND 11.06 · SE-2 9.62 · BD 5.74 % / 로그-선형 10.73 · 9.32 · 5.61 % · Heckel (원문은 안 함) P_y ≈241 (ND) · 187 · 164 MPa (BD) (R² 0.997 · 0.985 · 0.964) | 카드 §3-2 | [카드 산술] | 누른 뒤 밀도의 Heckel (가압 중 Heckel 과 다른 양) · 압력 점 4 개
- [a] cho2026_pore_… | 두께 = *"0.9-1.3 mm depending on the applied pressure and SE type"* (조건별 값 없음) · 질량 보존 두께 0.935 (BD 440) – 1.205 mm (ND 110) · 다이째 마이크로미터 5 점 평균 (그림 S2 표시창 '1003' mm · ZERO 단추 — 영점 상대 측정으로 보임) | 카드 §3-2 · p.17 · 그림 S2 · S3 | [인쇄] · [카드 산술] · [판독 사진] | 막대 길이 처리 · 영점 · 측정력 [미확인]

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 펠릿은 누른 뒤 다이 안 한 상태만 잼 (가압 중 · 꺼낸 뒤 · 회복량 없음 · 카드 §4-3 ④) · 셀은 20 MPa 일정 체결 · FEM 도 20 MPa 일정.

## c — 항복 · 경도 · 크리프 값과 정의
- [c] cho2026_pore_… | in-SEM Berkovich (PI 89) · 최대 10 mN · 부하 5 s – 유지 2 s – 제하 5 s · 깊이 ≈0.4–2.3 µm · Oliver–Pharr (H = P_max/A_c · h_c = h_max − 0.75 P_max/S · E_r = (√π/2β) S/√A_c) · 440 MPa 펠릿 E_r BD ≈31.0 ± 7.1 ↔ ND ≈38.4 GPa (SD ≲1.9) · H ≈2.21 ± 0.75 ↔ ≈2.72 GPa · 중앙값 E_r 110 → 440 MPa BD ≈10.1 → 32.1 · ND ≈14.6 → 38.5 GPa | 카드 §3-4 · p.17 · SI 노트 1 (p.51) · 그림 1i · 2a–b | [인쇄] 조건 · [판독] 값 | 다공 펠릿 조각 윗면의 **국소 유효값** (*"they reflect not only the mechanical response of the SE phase but also local porosity, particle packing, and surface condition"* SI p.51) · 조건마다 펠릿 하나 · 일축 항복 (σ_y) 환산 없음 · 크리프 없음
- [c] cho2026_pore_… | 국소 E_r · H 가 성형압에 선형 — ND E_r y = 0.06566x + 11.752 (Pc 0.985) · H y = 0.004377x + 1.058 (Pc 0.974) · BD 0.05469x + 6.371 (Pc 0.705) · 0.003706x + 0.518 (Pc 0.471) (x = MPa · y = GPa) | 카드 §3-4 · 그림 S8g–h | [인쇄 그림 안] | 110 · 330 · 440 MPa 세 압력 · 펠릿 하나씩
- [c] cho2026_pore_… | FEM 의 SE = 선형 등방 탄성 · E = BD 펠릿 E_r **33.13 GPa** 를 *"approximate Young's modulus"* 로 두 분리막에 같이 · ν 0.37 (Torii 2025 DFT) · 항복 없음 | 카드 §3-7 · §3-9 ③ · 표 S2 (p.65) · SI 노트 3 (p.59–60) | [인쇄] | 33.13 ↔ 그림 1i BD 판독 ≈31.0 GPa 어긋남 (출처 [미확인])

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 순수 SE 펠릿 · 복합 양극 하중 몫 측정 없음 (FEM 의 Sn 은 단단한 골격이 아니라 리튬화로 팽창하는 탄성 하중원 · 카드 §8 후보 A · A′).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음 (모든 고체 계면 접합 · 변위 연속 · SI p.60).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
- [f] cho2026_pore_… | (MPM 아님 · 이미지 FE 의 해상도) GrainGeo 3D 복셀 0.2 µm · 100 × 100 × 75 (20 × 20 × 15 µm) · D50 1.584 µm = ≈8 칸 · 공극 크기 봉우리 0.3 µm = 1.5 칸 · 2D 모형은 FIB-SEM 45 nm 영상 기반 (기공 경계 0–0.1 µm 칸 ≈2 화소) · 격자 · 요소 수 · 수렴 · 수치 오차 추정 없음 | 카드 §3-8 · §8 U6 · SI p.56 | [인쇄] · [카드 산술] | 공극 둘레 응력 꼬리는 이 해상도에서 미해상일 수 있음 (우리 d_h/dx ≳ 3.5 규칙과 견줄 반례 · 원문 말 없음)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] cho2026_pore_… | 전기화학–역학 모형 = 2D 평면변형 (그림 S14 *"Plane strain (2D)"*) · 원문 경고 *"Because the highly interconnected Sn morphology cannot be fully represented in a two-dimensional cross section, the apparent connectivity of individual Sn domains in the 2D geometry does not necessarily represent their actual three-dimensional electronic connectivity"* → 음극 전자 수송은 빠르다고 가정 · 분리막 2D 단면은 *"cropping slices whose porosity matched that of the corresponding 3D volume"* | 카드 §3-7 · §3-10 ④ · §4-3 ③ · SI p.58 · 그림 S11 캡션 (p.40) | [인쇄] | 응력장 자체의 2D ↔ 3D 차이는 다루지 않음 · 3D (GrainGeo) 는 20 MPa 역학만이라 2D (Sn 팽창 하중 · GPa) 와 하중이 달라 숫자로 잇지 못함

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] cho2026_pore_… | (DEM 아님) 기하를 넘긴 두 길: ① top-down = 누른 뒤 펠릿의 FIB-SEM 분할 영상 → COMSOL 2D 영역 ② bottom-up = GeoDict **GrainGeo** 알갱이 생성 (그림 5a 의 PSD 입력 · 기공 6.752 % 고정 · 동역학 · 압밀 없음) → 복셀 → 메시 → COMSOL 3D 탄성 · 넘긴 시점 = 압밀이 끝난 뒤의 기하 (압밀은 계산하지 않음) | 카드 §3-7 · §3-8 · §4-2 · SI p.53–56 | [인쇄] | 알갱이 모양 · 겹침 · 6.752 % 맞춘 법 · 접촉 · 경계 처리 [미확인] · 그림 5 입력 판독 관찰 (§3-9 ①②)

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 복합 양극 (LiNbO₃-NCM622 : ND : CNF 65 : 30 : 5 · 220 MPa 2 분) 은 공정만 · 기공 없음 (카드 §3-5).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] cho2026_pore_… | 원문 한계: *"Explicit fracture and interfacial separation were not simulated."* (p.19) · *"does not explicitly simulate crack initiation, crack propagation, or interfacial separation. The calculated stress fields should therefore be interpreted as indicators of mechanically vulnerable regions rather than as direct predictions of fracture."* (p.12) · 국소 기공 *"should not be interpreted as direct substitutes for pellet-averaged porosity"* (p.7) · D50 · PSD 폭 · 기공 *"change simultaneously in the experimentally compacted powders"* (p.13) · 3D 결론 *"within the present model framework"* (p.14) | 카드 §3-10 | [인쇄] | —
- [j] cho2026_pore_… | 카드가 본 공백: 가압 중 두께 · 꺼낸 뒤 · 되돌아옴 없음 · 두께 조건별 값 없음 · TD 1.64 출처 · 실제 밀도 없음 · 나노압입 지도 펠릿 간 반복 · Moran's I 유의성 없음 · FEM 격자 · 비용 · β_Sn–γ_V 식 (인쇄 깨짐 'βSn=¿') 없음 · 그림 5a 좁은 PSD 곡선 없음 · 5d ≈ 그림 S6 | 카드 §11 · §13 · §3-9 | [미확인] · [판독] | —

## k — DEM 의 한계 (서지: Cho et al., ChemRxiv (2026) 10.26434/chemrxiv.15009882/v2 · preprint)
- [k] cho2026_pore_… (Cho 2026 · ChemRxiv 원고) | **말 없음** — DEM · discrete element 0 회 (66 쪽 전수) · 입자 계산 없이 영상 → 연속체 FE 로 감 · 관련 문장 = 압분체는 *"residual pores, interparticle boundaries, locally constrained contacts, and load-bearing ligaments whose spatial arrangement emerges during powder consolidation"* (p.4) 를 가진다 — 그 배열을 만드는 압밀 계산은 없다 | 카드 §4-3 ① · §0 ⑨ | 카드 서술 · [인쇄] | —

## l — 소성변형이 왜 어려운가 · 우회 (서지: Cho et al., ChemRxiv (2026) 10.26434/chemrxiv.15009882/v2 · preprint)
- [l] cho2026_pore_… (Cho 2026 · ChemRxiv 원고) | **어려움의 설명 없음** · 우회 = 누른 뒤의 실측 구조 (FIB-SEM) 를 그대로 기하로 써서 압밀 · 소성을 건너뜀 · SE 선형 탄성 · 모든 계면 접합 · 단방향 결합 (*"the resulting mechanical stress was not fed back into the lithium chemical potential or electrochemical reaction kinetics"* SI p.60) · **맞춘 값 0** (E = BD E_r 33.13 · ν 0.37 DFT · κ 측정 · Sn · NCM 문헌) · 검증 = 첫 충전 곡선 정성 비교 (*"compared qualitatively"* — 실험 0.1C ↔ 계산 0.2C · 끝 전압 실험 4.34 · 4.16 ↔ 계산 4.46 · 4.52 V [판독 그림 S16]) + 응력 지도 ↔ 사후 균열 위치 정성 일치 · 비용 (요소 수 · 시간) [미확인] · 결과 응력이 GPa 급 (P95 ≤12.7 GPa · 꼬리 ≈100 GPa 계급 [판독]) = 압입 경도 (≈2–3 GPa) 위 | 카드 §3-7 · §4-1 · §4-3 ② · SI p.59–61 | [인쇄] · [판독] | 소성이 들어가면 응력 꼬리가 잘린다 — 크기 비교 금지 (상대 비교만)

## m — 받아들일 통찰
- [m] cho2026_pore_… | **기공 등록 칸에 분말 PSD 를 넣는다** — 같은 분모 (1.64) · 같은 다이 (⌀13 mm · 200 mg) · 같은 상태 (다이 안 뺀 뒤) 에서 PSD 만으로 기공이 2–4 배 (440 MPa 1.73 ↔ 6.19 % · 110 MPa 13.78 ↔ 23.75 %) → 랩 표준 (10–13 %) 을 MPM σ_y 표적으로 쓸 때 {분말 D10 · D50 · D90 · 유지 시간 · 측정 상태} 꼬리표 | 자리: 단계 0 · 단계 4 | 표 S1 (p.64) · 카드 §7-2 · §9 ① | [인쇄] | —
- [m] cho2026_pore_… | **공극망 균일성 = ε 옆의 둘째 관측량** — z 투영 국소 기공 지도의 평균 · SD (그림 S5 정의) + Moran's I (상하좌우 이웃 가중 1 · 자기쌍 제외 · 행 표준화 없음 · p.18) — ε 하나로는 BD (1.73 %) 가 가장 좋아 보이나 국소 8.129 % · SD ≈4.4 %p 로 가장 고르지 않다 | 자리: 단계 7 · 흐름 밖: SE 입도 설계 (50 kg) | 카드 §3-3 · §9 ② · 그림 1d–f · S5 | [인쇄] · [판독] | 지도 시야 · 해상도 · 분할 문턱을 같이 적어야 견줄 수 있다
- [m] cho2026_pore_… | **두 조건의 장 비교는 공통 (pooled) 백분위 문턱으로** — BD + ND 분포를 모아 P90 · P95 (기계) · P20 (압입) 를 잡고 넘는 몫을 비교 · 검산 = 몫의 평균이 문턱 몫 근처 (VM P90 (14.4 + 4.8)/2 = 9.6 % · 압입 P20 낮은 몫 자리 수 65 + 20 + 3 + 0 = 88 = 440 × 0.20) · 기공 경계 거리 칸 (0–0.1 · 0.1–0.3 · 0.3–0.5 µm) 평균 · P95 | 자리: 단계 7 (MPM 응력장 후처리) · 결과 전 대조 | SI p.62–63 · p.18 · 카드 §3-4 · §3-7 | [인쇄] · [카드 산술] | 인장 몫은 σ_h > 0 만 문턱을 잡아 평균 검산이 안 선다
- [m] cho2026_pore_… | **함정 — '같은 D50 · 같은 기공' 디지털 구조 비교의 입력을 그림끼리 대조한다** — 그림 5a 에 좁은 PSD 곡선이 없고 (화소 0) 보이는 '넓은 PSD' 곡선은 그림 1a 의 ND 실측 PSD 와 같은 꼴 · 그림 5d (GrainGeo 공극 크기) 가 그림 S6 (FIB-SEM) 과 같은 꼴 (봉우리 비 1.71 = 1.71) · 모형 E 33.13 ↔ 그림 1i 판독 31.0 → 문헌의 '통제된 디지털 비교' 를 인용 · 재현할 때 입력 분포 · 값을 원 그림과 맞춰 본 뒤 쓴다 | 자리: 결과 전 대조 · 단계 0 (등록 시 입력 출처) | 카드 §3-9 · `digitized.csv` | [판독] | 원인 미확인 (저자 확인 전) · 원고 v2

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] Diallo, M. S. et al. Effect of solid-electrolyte pellet density on failure of solid-state batteries. Nat. Commun. 15, 858 (2024). (원문 참고 [38] 그대로 · DOI 없음) | a · j (펠릿 밀도 ↔ 파괴 · 이 원고 p.5 가 '넓은 PSD = 치밀 · 저항 낮춤' 과 '뭉친 공극 · 고르지 않은 하중 길' 의 근거로 인용) — 카드 §12 | papers/ 목록 (diallo* 없음) · 'Diallo' grep = faka2026 · miss2026 (인용만)
- [n] Li, J. et al. Processing-structure-property relationships in practical thin solid-electrolyte separators for all-solid-state batteries. J. Phys. Energy 6, 025023 (2024). (원문 참고 [35] 그대로 · DOI 없음) | a · m (얇은 SE 분리막의 공정–구조–물성 · 분리막 기공 · 두께) — 카드 §12 | papers/ 목록 (li2024_inf3_argyrodite_ultrathin_film = 다른 논문) · '025023' · 'Processing-structure-property' grep 0
- [n] Han, S. Y. et al. Stress evolution during cycling of alloy-anode solid-state batteries. Joule 5, 2450–2465 (2021). (원문 참고 [11] 그대로 · DOI 없음) | 흐름 밖: 적층압 해석 · 합금 음극 하중 (이 원고 p.9 의 *"alloy-anode expansion and contraction as major contributors to cell-level pressure evolution"* 근거) — 카드 §12 | papers/ 목록 (han2021* 없음) · 'Stress evolution during cycling of alloy' grep 0
- [n] Sammis, C. G. & Ashby, M. F. The failure of brittle porous solids under compressive stress states. Acta Metall. 34, 511–526 (1986). (원문 참고 [28] 그대로 · DOI 없음) | k · l · m (다공 취성체의 압축 파괴 — 공극 둘레 응력 집중 → 균열 · 이 원고 공극 ↔ 응력 논리의 원전) — 카드 §12 | papers/ 목록 (sammis* · ashby* 없음) · 'Sammis' grep 0
- [n] Park, C. et al. Electrochemical Properties of Composite Cathode Using Bimodal Sized Electrolyte for All-Solid-State Batteries. J. Electrochem. Soc. 166, A5318–A5322 (2019). (원문 참고 [37] 그대로 · DOI 없음) | i · m (두 봉우리 SE 입도 복합 양극 — BD 와 같은 꼴 · 이 원고 p.5 '넓은 PSD = 저항 낮춤' 근거) — 카드 §12 | papers/ 목록 (park2019_electrode_design_methodology_assb_3d = 다른 논문 · ESM) · 'A5318' grep = cronau2022 · kawaguchi2023 · park2020 (인용만)

## 카드 문제
없음 — 후보 표 행이 아니라 가리킨 카드가 없고, 정본 `papers/` 에 이 원고 (DOI `15009882` · 제목 'pore-network homogeneity' · 저자 Hyeok-Rae · Hyeong-Jong) 를 인용한 카드가 없다 (git grep 0 건 · 2026-11-23).
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §3-9 에 적음): 표 S2 · SI 노트 3 의 분리막 E *"Er = 33.13 GPa; Figure 1i"* ↔ 그림 1i BD 판독 ≈31.0 GPa · 그림 5a 좁은 PSD 곡선 없음 · 그림 5d ≈ 그림 S6 · 화학 변형 식 인쇄 깨짐 ('βSn=¿') · NCM622 i₀ *"2.254872 A cm⁻²"* (단위 의문) · 장비 이름 Hysitron (Methods) ↔ Bruker (그림 S7).
