# batch 139 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-22 · 후보 N-90)

대상: `park2022_am_shape_size_pressure_tortuosity_electron_blocking_al2o3` — S.-Y. Park · J. Jeong · H.-C. Shin\*, "Geometrical Effect of Active Material on Electrode Tortuosity in All-Solid-State Lithium Battery", *Applied Sciences* **12** (2022) 12692 · DOI 10.3390/app122412692 (17 쪽 · SI 없음).
Li₆PS₅Cl 3 µm + 가상 활물질 Al₂O₃ (구 · 판 · 섬유 · 10 / 70 / 100 µm) + 카본블랙 펠릿의 이온 tortuosity 를 전자 차단 셀 직류 (정전위 ΔE 100 mV) 로 재고, 모양 · 크기 · 성형압 (44–655 MPa) · SE 부피분율 (0.32–0.72) 효과를 본 실험 (계산 없음).
쪽 = MDPI 인쇄 쪽 'n of 17' = PDF 쪽 · 판독 원자료 = `litdb/figures/park2022_…/digitized.csv` (198 행 · 원 래스터 화소) · 고른 의도 대조 = **채움 (한정)** (카드 §0-1 — 압력 축 · 전자 차단 셀 · τ 식 출처 = 채움 · '20–75 @40 → 5–15 @660 MPa' = 그림 판독 범위로 근사 일치 · 숫자 미인쇄 · 가상 AM).
인용 서지 (질문 k · l 용): Park, Jeong, Shin, Appl. Sci. 12 (2022) 12692.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 압밀 자료 없음 (복합 전극만).
- [a] park2022_… | (참고 · 곡선 아님) 셀의 SE 층 σ_electrolyte = **0.174 S/m (1.74 mS/cm)** · 두께 ≈600 µm · 면적 1.33 cm² — 기공 · 압력 · 온도 · 출처 [미확인] | 카드 §3-1 · §3-2 · p.4 (`txt_p4_cell_dc_100mv_sigma_0174.png`) | 인쇄 | 순수 SE 기공 · 진밀도 없음 · 랩 표준 (10–13 % · 1.64) 옆에 둘 숫자 없음

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 · 되돌아옴 · 시간 의존 측정 없음 (성형 뒤 펠릿을 셀로 짰다고 읽히나 측정 때 압력 상태 [미확인]).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 기계 값 0 건 (정성: SE 의 *"limited ductility"* — 질문 l).
- [c] park2022_… | (값 아님 · 복합 겉보기 Heckel) ln(1/n) vs 성형압 5 점 기울기 구 5.2 × 10⁻⁴ · 판 6.6 × 10⁻⁴ · 섬유 8.8 × 10⁻⁴ /MPa → P_y ≈ 1.9 · 1.5 · 1.1 GPa | 카드 §3-6 · 그림 9b | 카드 산술 (판독 기공) | 단단한 Al₂O₃ 68 vol% 골격이 하중을 지는 복합의 느린 치밀화 — SE 항복 세기가 아니다 · 일축 항복 환산 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] park2022_… | 단단한 비활성 Al₂O₃ 68 vol% (ε_SE 0.32) 복합은 44 → 655 MPa 에서 기공이 구 20.4 → 15.4 % · 판 23.5 → 15.3 % 로만 준다 (655 MPa 에서도 15 % 근처) · SE 많은 ε_SE 0.72 는 109 MPa 에 이미 ≈17 % | 카드 §3-3 · §3-6 · §8 R1 · 그림 4c · 4d · 9b | 판독 | 하중 몫 측정 없음 (정성 증거) · 가상 AM · 이론 밀도 분모 미인쇄
- [d] park2022_… | 섬유 응집체는 저압에서 기공 50.6 → 32.1 % (영역 A · SE 가 미세 기공을 채움) 뒤 545–655 MPa 에서 29.5 · 29.3 % 평탄 (영역 B) | 카드 §3-6 · 그림 9b · p.13–14 (`txt_p13p14_contact_regions_ductility.png`) | 판독 · 인쇄 (해석) | 응집 미세 기공 = 압력으로 못 메우는 빈틈의 실측 예

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 2D → 3D 진술 없음 (3D 펠릿 관통 방향 측정 · 2D 단면 SEM 은 정성).
- [g] park2022_… | (참고) 판 입자가 기판과 나란히 누워 (단면 그림 5a · [21] Usseglio-Viretta) 같은 기공 (≈20 %) 에서 관통 τ 가 구의 ≈2.3 배 — 한 방향 (두께) 만 쟀다 | 카드 §3-3 · 그림 4a · 5a · p.8 (`txt_p8_shape_two_three_times.png`) | 판독 · 인쇄 | 이방성은 방향 하나로만 보였다

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] park2022_… | 가상 AM (Al₂O₃) + LPSCl 3 µm + 카본블랙 (ε_SE 0.32) 펠릿 성형압 44 · 109 · 327 · 545 · 655 MPa: 구 20.4 · 20.0 · 16.4 · ≈15 · 15.4 % · 판 23.5 · 19.5 · 18.1 · 15.0 · 15.3 % · 섬유 50.6 · 43.6 · 32.1 · 29.5 · 29.3 % (327 · 545 MPa 는 가로축 판독) | 카드 §3-6 · 그림 9b | 판독 (1 px = 0.20 %p) | 기공 = 1 − V_theo/V_real (이론 밀도 · CB 양 미인쇄) · 성형 뒤 · 측정 시점 · 방법 [미확인] · NCM 아님 · 랩 표준과 다른 문헌 값
- [i] park2022_… | 109 MPa 고정 · 모양별: ε_SE 0.32 구 19.7 · 판 19.5 · 섬유 43.2 % · ε_SE 0.72 ≈17.4 · ≈17.8 · 20.0 % · 크기별 (구 · 0.32) S10 18.9 · S70 17.7 · S100 ≈22 % | 카드 §3-3 · §3-5 · 그림 4c · 4d · 8b | 판독 | 같은 한정

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] park2022_… | 원문: 계산 모사는 *"it is difficult to implement the non-uniform distribution of particles or closed pores in a solid electrode"* (p.2) · *"not easy to use computer simulation … in which active material aggregation and insufficient electrolyte filling occur"* (p.10) | 카드 §4-4 (i) · `txt_p2_simulation_eis_limits_high_am.png` · `txt_p10_low_am_bruggeman_313_simulation.png` | 인쇄 | 계산 쪽 일반 한계 (DEM 특정 아님)
- [j] park2022_… | (카드가 적은 원문 공백) 온도 · 셀 체결 압력 · 측정 때 압력 상태 · 카본블랙 양 · 이론 밀도 · σ_electrolyte 출처 · 시료 수 · 상자 수염 정의 · 압력 연구 ε_SE · α 에 쓴 ε [미확인] · Li \| SE 계면 저항 안 뺌 | 카드 §0 한정어 · §11 · [미확인] 목록 | 카드 서술 | 실험 tau2 를 우리 망 결과 옆에 놓을 때 필요한 칸이 비어 있다

## k — DEM 의 한계 (서지: Park, Jeong, Shin, Appl. Sci. 12 (2022) 12692)
- [k] park2022_… (Park 2022 · Appl. Sci.) | **DEM 을 직접 겨냥한 문장은 없다** — 계산 모사 일반: *"Although computational simulation is suitable for simplifying and realizing complex microstructures, there is a limit to perfectly simulating the microstructure of an actual electrode because it is difficult to implement the non-uniform distribution of particles or closed pores in a solid electrode."* (p.2) · *"It should be mentioned that it is not easy to use computer simulation to investigate the microstructure of an electrode for an all-solid-state battery in which active material aggregation and insufficient electrolyte filling occur. … The result may have a significant error compared to the actual result."* (p.10) · DEM 사례 인용 = So 2021 [22] | 카드 §4-4 (i) · p.2 · p.10 | 인쇄 | 응집 · 닫힌 기공 · 불충분 충전을 표현하기 어렵다는 '계산 일반' 진술 — 구 DEM 의 형상 · 점접촉 한계를 말한 것은 아님

## l — 소성변형이 왜 어려운가 · 우회 (서지: Park, Jeong, Shin, Appl. Sci. 12 (2022) 12692)
- [l] park2022_… (Park 2022 · Appl. Sci.) | **계산 쪽 논의 없음** — 실험 관찰 · 해석: *"the limited ductility of a solid electrolyte makes it difficult to cover the rough surface of the active material and penetrate the micropores of the electrode"* (p.1 · [4]) · 섬유 영역 B *"when electrolyte penetration into the micropores of the aggregate was no longer possible because of the limited electrolyte ductility"* (p.14) | 카드 §3-7 · §4-4 (ii) · `txt_p1_limited_ductility_filling.png` · `txt_p13p14_contact_regions_ductility.png` | 인쇄 | 소성 SE 도 미세 기공을 다 못 채운다는 정성 근거 · SE 기계 물성 · 우회 · 비용 없음
- [l] park2022_… (Park 2022) | 압력 효과의 해석 = SE 입자끼리 맞닿음 개선 (*"reduction in lithium-ion migration resistance at electrolyte grain boundaries"* [46]) · 구 · 판 기공은 거의 그대로 (SE 의 전체 부피 몫 +6 % · τ ×1/4.05 [카드 산술]) | 카드 §3-6 · p.13 | 인쇄 · 카드 산술 | 입계 · 접촉 · SE 고유 σ 변화를 분리하지 않았다

## m — 받아들일 통찰
- [m] park2022_… | **Bruggeman 지수는 꼴 · ε 기준 · 전인자를 함께 등록** — 이 논문 'α' = τ = ε^−α (σ = σ₀ε^(1+α)) · Kaiser 같은 꼴 · Froboese τ = γφ^(1−α_F) (α_F = 1 + α) · 인쇄 3.13 ↔ 그려진 점선 ε^−2.78 · ε 를 고정하면 α 는 ln τ 의 재표현이라 '연결성' 의 따로 된 증거가 아니다 (그림 9c α 는 9a τ 와 ε 0.32 로 다시 안 나옴) | 자리: 단계 0; 흐름 밖: τ 명명 규약 · 문헌 대조 | 왜: 카드 §3-4 · §3-6 · §7-4 [판독 · 카드 산술]
- [m] park2022_… | **압력별 tau2 변화를 기공으로 읽지 않는다 — 협착 몫부터** — 구 · 판 전극은 44 → 655 MPa 에서 기공 20 → 15 % · τ 4–7 배 ↓ (SE 부피 몫 +6 %) → 우리 망의 tau2(P) 비교 때 협착 (FULL/CF) 분해를 같이 낸다 · 결과 전 대조 후보 = 구 계열 τ(109)/τ(327) 1.51 · τ(327)/τ(655) 1.84 (판정 아님) | 자리: 단계 7; R3; 결과 전 대조 항목 | 왜: 카드 §3-6 · 그림 9a · 9b [판독 · 카드 산술]
- [m] park2022_… | **DC 전자 차단 셀의 '빼는 저항' 장부** — 식 (4) 는 SE 층 bulk 만 빼고 (51.85 Ω) Li \| SE 계면 · 층 사이 저항은 남는다 · SE 많은 쪽 (ε_SE 0.72) 은 빼는 몫이 총 저항의 34–35 % → σ₀ 를 같은 분말 · 같은 압력으로 재고 두께 여러 개로 계면을 분리하는 칸을 대칭셀 계획에 둔다 | 자리: 단계 0; 흐름 밖: 대칭셀 실험 설계 | 왜: 카드 §3-2 · 식 (4) [카드 산술]
- [m] park2022_… | **섬유상 첨가 · 응집 미세 기공 함정** — 섬유 Al₂O₃ 응집체는 SE 가 못 채운 미세 기공으로 기공 ×2 (43 %) · τ ×3.9 (ε_SE 0.32) · 고압에서도 29 % — 섬유상 첨가제 (VGCF) 가 많은 설계를 구 DEM · 복셀로 볼 때 놓치는 빈틈 후보 | 자리: 흐름 밖: 첨가제 분산 · R6 | 왜: 카드 §3-3 · §3-6 · 그림 4 · 5b · 9b [판독 · 인쇄]

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] Usseglio-Viretta, F.L.E.; Finegan, D.P.; Colclasure, A.M.; Heenan, T.M.M.; Abraham, D.P.; Shearing, P.R.; Smith, K. Quantitative relationships between pore tortuosity, pore topology, and solid particle morphology using a novel discrete particle size algorithm. J. Electrochem. Soc. 2020, 167, 100513. (ref [21]) | g · m — 판 입자 정렬 → tortuosity (이 논문 판 효과 해석의 근거) — 카드 §3-3 · §12 | papers/ 목록 (usseglio* 없음) · 'Usseglio' grep = 다른 카드 인용만 → 카드 없음
- [n] Vadakkepatt, A.; Trembacki, B.; Mathur, S.R.; Murthy, J.Y. Bruggeman's exponents for effective thermal conductivity of lithium-ion battery electrodes. J. Electrochem. Soc. 2015, 163, A119. (ref [42]) | m — 'α = 연결성' 해석의 출처 · Bruggeman 지수 관례 — 카드 §3-2 · §12 | papers/ 목록 (vadakkepatt* 없음) · grep = `tjaden2018_…` 인용만 → 카드 없음
- [n] Clennell, M.B. Tortuosity: A guide through the maze. Geol. Soc. Lond. Spec. Publ. 1997, 122, 299–344. (ref [38]) | m — 식 (1) 기하 정의 · '식 (1) ≡ 식 (2)' 주장 대조 (τ 명명) — 카드 §11 · §12 | papers/ 목록 (clennell* 없음) · grep = hlushkou2018 · holzer2013 · landesfeind2016 · tjaden2018 인용만 → 카드 없음
- [n] Parikh, D.; Christensen, T.; Li, J. Correlating the influence of porosity, tortuosity, and mass loading on the energy density of LiNi0.6Mn0.2Co0.2O2 cathodes under extreme fast charging (XFC) conditions. J. Power Sources 2020, 474, 228601. (ref [47]) | i · m — 액체 LIB 압연 → τ ↑ (이 논문 '반대' 결론의 대비 근거) — 카드 §3-7 · §12 | papers/ 목록 (parikh* 없음) · 'Parikh' grep = 0 → 카드 없음

## 카드 문제
- `miss2026_pressure_tortuosity_composite_cathode_coating` **L136** (ref 16): *"전자 차단 셀 τ_ion 20–75 @40 MPa → 5–15 @660 MPa [인쇄] p.2"* — 원문 그림 9a [판독] 44 MPa 17.8 · 40.0 · 74.4 · 655 MPa ≈4.4 · 5.5 · 12.9 와 **반올림으로 일치** — 카드 문제 아님.  보탤 한정어 (그 카드는 고치지 않음): 숫자는 원문에 인쇄되지 않은 그림 값 · 가상 AM (Al₂O₃) 세 모양 · ε_SE 0.32 [추정] · σ₀ 1.74 mS/cm 고정 · '40 / 660' = 원문 §4.3 표현 (방법 절 44 / 655).
- `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` **L280** (SI ref S11): *"카드 없음 — τ 식 출처"* — 식 (2) τ = (σ_electrolyte/σ_eff)·ε 와 같은 꼴 · 문제 아님 (이 논문도 식을 [39] Kaiser 2018 에서 가져왔다).
- 후보 표 (`S8_candidates.md` N-90 서지 칸) 의 메모 *"kim2024_optimal L280 · miss2026_pressure L269 은 제목 없이 같은 권 번호"* — kim2024 L280 은 **제목까지** 적었다 (제목 없는 쪽은 miss2026 L269 뿐) · 카드 문제 아님 (후보 표 메모의 작은 오기).
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §11 에 적음): 그림 1b 첫 식 I_ss/ΔE (본문 ΔE/I_ss) · 그림 4 캡션 (a,b)/(c,d) ↔ 패널 (a,c)/(b,d) · 'AM ≥ 60 % (ε_SE < 0.6)' · 초록 '45 까지' ↔ 그림 47–50 (74) · 'approximately 3.13' ↔ 점선 ≈ε^−2.78 · 그림 9c α ↔ 9a τ · 방법 44–655 ↔ §4.3 '40–660 MPa' · 섬유 카탈로그 2–6 nm × 200–400 nm ↔ SEM µm 굵기 · S10 막대 ↔ '<10 µm 뺌' · 그림 3 ↔ 그림 4 함축 두께 (섬유 698 µm) · 'R_ion,cell' 기호.
