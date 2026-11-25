# batch 130 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 N-81)

대상: `hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf` — E. Hayakawa · H. Nakamura\* · S. Ohsaki · S. Watano, "Design of active-material/solid-electrolyte composite particles with conductive additives for all-solid-state lithium-ion batteries", *J. Power Sources* **555** (2023) 232379 · DOI 10.1016/j.jpowsour.2022.232379 (접수 2022-09-16 · 온라인 2022-11-17 · 권 연도 2023).
NCM523 (LiNbO₃ 1 wt% · 4.3 µm) 에 Li₆PS₅Cl (0.7 µm · 2.02 mS/cm) 을 Nara 건식 충격 블렌딩 (13,000 rpm · 5 min) 으로 입힌 코어–셸 입자 (CP) 에 아세틸렌 블랙 (CP-AB) · VGCF (CP-VGCF) 를 넣어, 같은 순 조성의 막자 혼합 (SM) 과 360 MPa 압분체 EIS (σ_ion · σ_e) · Li–In 반쪽셀 (첫 사이클 · dQ/dV · 율속 · EIS · CV · 50 사이클) 로 견준 실험 — 계산 없음.
쪽 = 인쇄 쪽 = PDF 쪽 (p.1–9) · SI p.1–2 · 판독 원자료 = `litdb/figures/hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf/digitized.csv` (332 행 · 그림 6–10 은 벡터 경로 좌표) · 고른 의도 대조 = **일부** (카드 §0-1 — 코팅 입자의 전자 경로 문제 · AB 든 껍질은 채움 · "Xs 0.3 붕괴" 는 이 논문에 없음 (kawaguchi2023 자신의 결과) · "도전재로 푼다" 는 AB 에 한정 · "후속" 은 시간 순서가 반대 (이 논문이 1 년 먼저) · "고강도 혼합" 은 짝 논문 [10] 의 내용).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 의 기공 · 밀도 · 압력 의존이 없다 (SE 2.02 mS/cm 의 측정 조건도 [미확인]).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 하중 해제 · 되돌아옴 측정 없음 (측정 때 압력 · 운전 적층압 [미확인] · 'unload' · 'spring' 0 회).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 기계 물성 값 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 하중 몫 값은 없음.  정성 가설 하나:
- [d] hayakawa2023_dry_coated_… | (가설 · 측정 없음) SM 의 높은 Rs (94.5 Ω ↔ CP 류 63.1–79.0 Ω) 를 *"the coalescence of SE was not promoted because the compression stress was not uniformly acted upon by the non-uniform distribution of AM and SE particles in the cathode"* 로 · 코어–셸은 *"the compression stress was uniform"* 로 설명 | 카드 §3-6 · p.7 (`txt_p7_rs_se_coalescence_compression_stress.png`) | 인쇄 (해석 문장) · Rs = 그림 8 안 표 [인쇄] | 응력 · 합체 · 접촉 면적 측정 없음 · Rs 는 분리막 포함 · 같은 논문 이온 차단 σ_ion 은 SM ≥ CP (유의차 없음) 라 방향이 안 맞는다 · NCM523 · 360 MPa

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).  해상도에 쓸 기하만 있다:
- [f] hayakawa2023_dry_coated_… | SE 껍질 두께 100–1000 nm (원문 범위) · 고른 치밀 껍질 가정의 어림 ≈0.36 µm (ρ_SE 1.64 랩 표준 · ρ_NCM523 4.72 다른 카드 가정) · AM 지름 4.3 µm → 껍질/지름 ≈2–23 % · 우리 MPM real_14 격자 dx 141 nm (CLAUDE.md) 로는 껍질 0.7–7 칸 (어림 ≈2.5 칸) | 카드 §3-1 · p.4 (`txt_p4_shell_100_1000nm_summary.png`) | 인쇄 (범위) · [카드 산술] (어림 · 칸 수) | 정량 영상 분석 없음 · 개수 중앙 지름 · 탄소 (AB 35 nm) 는 어느 격자로도 못 풂

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산이 없고 영상은 2D 단면 (SEM/EDX) 뿐 · 2D → 3D 에 대한 말 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 압력 한 값 (360 MPa) · 기공 · 밀도 · 두께 미인쇄.
- [i] hayakawa2023_dry_coated_… | (참고 · 기공 아님) 순 조성 SM 84.0 : 16.0 · CP 83.1 : 16.9 · CP-AB 81.4 : 15.8 : 2.79 · CP-VGCF 81.7 : 16.6 : 1.62 wt% → 고체 중 SE ≈0.35–0.37 vol (ρ_SE 1.64 · ρ_NCM523 4.72 가정) · 반쪽셀 AM 면 로딩 10.4–10.7 mg/cm² | 카드 §3-1 · §3-4 · 표 1 (`tab_1.png`) | 인쇄 (조성) · [카드 산술] (부피 · 로딩) | 기공 계산 불가 · 진밀도 원문에 없음

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] hayakawa2023_dry_coated_… | σ 를 *"conductive resistance, thickness of the composite cathode, and electrode area"* 로 냈는데 두께 · 지름 값이 인쇄되지 않았다 → σ 다시 내기 불가 | 카드 §3-3 · §13 · p.3 (`txt_p3_eis_two_semicircles_thickness_area.png`) | 인쇄 / [미확인] | 압력별 대조 불가
- [j] hayakawa2023_dry_coated_… | SM 의 25 사이클 뒤 급락 (판독 80.2 → 35.6 mAh/g · 25 → 45 사이클) 을 *"mechanical degradation [36]"* · AM 부피 변화로 AM–AM · AM–SE 접촉이 바뀌고 *"peeling the contact interface"* 로 설명 · 코어–셸은 *"could mitigate the effect of the volume change of AMs"* | 카드 §3-8 · p.8 (`txt_p8_cycle_retention_volume_change.png`) | 인쇄 (해석) · [판독] (용량) | 부피 · 박리 · 손상 측정 없음 · 운전 적층압 [미확인]
- [j] hayakawa2023_dry_coated_… | Rs (> 100 kHz) 는 분리막 + 양극 SE 저항 — *"The difference in Rs at each cell was attributed to the SE resistance of the cathode because the SE separator was prepared using the same process"* | 카드 §3-6 · p.6–7 (`txt_p6_eis_frequency_assignment.png`) | 인쇄 | 분리막 몫을 빼지 않았다 (kawaguchi2023 카드와 같은 한정)

## k — DEM 의 한계
- [k] hayakawa2023_dry_coated_… (Hayakawa · Nakamura · Ohsaki · Watano 2023, J. Power Sources 555, 232379) | **말 없음** — DEM · discrete · simulation 0 회 (실험만).  DEM (단단한 구 · SE 를 구로 둠) 과 맞닿는 실험 사실만: ① SE 가 AM 둘레에 *"coalescence"* 로 합쳐진 껍질 (100–1000 nm) 로 있는 출발 상태 (그림 3 · 4) ② 그 껍질이 AM–AM 전자 접촉을 막아 압분체 σ_e 가 1/21 (그림 6b [판독]) — 구 입자 DEM 은 이 출발 상태 · 접점 차단을 따로 만들어야 한다 [카드 해석] | 카드 §4-3 · p.4 · p.7 | 인쇄 · [판독] | 말 없음

## l — 소성변형이 왜 어려운가 · 우회 · 비용
- [l] hayakawa2023_dry_coated_… (Hayakawa · Nakamura · Ohsaki · Watano 2023, J. Power Sources 555, 232379) | 소성 계산의 어려움 · 우회 · 비용에 대한 말 없음 (계산 없음).  소성과 닿는 실험 서술 둘: *"the composite particles were in a state of already promoted coalescence of SE by the dry coating process"* (p.7 — 코팅 중 SE 합체 = 압밀 전 이미 변형된 SE) · *"it was difficult to fold and incorporate the VGCF into the SE coating layer compared to AB"* (p.4 — 섬유를 껍질에 접어 넣기) | 카드 §4-3 · p.4 · p.7 (`txt_p7_rs_se_coalescence_compression_stress.png` · `txt_p4_shell_100_1000nm_summary.png`) | 인쇄 | 둘 다 측정 · 계산 없는 서술 · 맞춘 값 · 비용 없음

## m — 받아들일 통찰
- [m] hayakawa2023_dry_coated_… | ① **'층 σ_e ≠ AM 전자 공급' — 관측량을 둘로**: CP-VGCF 는 압분체 σ_e 최고 (5.02 × 10⁻⁴ S/cm · SM ×17.6) 인데 CV 산화 전류가 봉우리 없이 0.25 mA (CP-AB 0.53 mA) · 2 C 방전 30.7 (CP-AB 97.7) mAh/g — 원문 *"these electrical conductivities … are not an indicator of the ease of supplying electrons to AM particles"* → 우리 판–판 망 σ_e 옆에 **AM 입자별 전자 접근성** (판에 이어진 전자망에 붙은 AM 몫 · AM 입자별 전류) 을 같이 보고 (탄소를 넣어 층 σ_e 가 오를 때 특히) | 카드 §7-2 · §3-7 · p.7 (`txt_p7_conductivity_not_electron_supply.png`) · 그림 6b · 9 | 인쇄 · [판독] | 자리 = 단계 7; 흐름 밖: 접촉망 σ_e 수송 · STEP3 탄소
- [m] hayakawa2023_dry_coated_… | ② **코어–셸 출발 상태의 결과 전 대조 항목**: 같은 순 조성 (SE ≈16–17 wt%) · 360 MPa 에서 무탄소 껍질 ÷ 막자 혼합 σ_e **0.048** · σ_ion **0.91 (유의차 없음)** · 같은 그룹 Nakamura 2020 (Li₃PS₄ · DC) σ_e −94 % · σ_ion +58 % (다른 카드) — 우리 침대에 AM 둘레 SE 껍질 (AM 하나당 0.7 µm SE ≈136 개 [카드 산술]) 을 둔 출발 상태로 망 σ_e 가 같은 쪽으로 무너지는지 (방향 · 자릿수만 · 맞추지 않음) | 카드 §8 · §3-3 · 그림 6 | [판독] · [카드 산술] | 자리 = 단계 5; 단계 7; 후보 D0; 결과 전 대조 항목
- [m] hayakawa2023_dry_coated_… | ③ **조성은 순 (net) 으로 · 탄소 자리는 기하 규칙으로**: 건식 코팅이 투입 SE 의 37–46 % · VGCF 의 42–65 % 를 장치 벽에 잃는다 (AM 추적자 [카드 산술] · 원문 *"owing to the SE adhesion to the inner wall"*) · 껍질 두께 (100–1000 nm) 보다 작은 CA (AB 35 nm) 는 껍질 안 · 긴 섬유 (VGCF 6 µm) 는 입자 사이 (SEM/EDX 정성) → 코팅 팔 등록 · 첨가제 표현에 '투입 ↔ 순' 두 칸과 탄소 자리 판정 근거를 결과 전에 적는다 | 카드 §3-1 · §3-2 · 표 1 · SI 그림 S1 · p.3–4 | 인쇄 · [카드 산술] | 자리 = 단계 0; 흐름 밖: 믹서 Ⓒ 코팅 팔 · 첨가제 표현 (STEP3)
- [m] hayakawa2023_dry_coated_… | ④ **함정 (보고 대조)**: 본문 CP 첫 방전 "ca. 87 mAh/g" ↔ 그림 7a 방전 끝 81.7 (효율 77.0 % 와 맞는 쪽) · 본문 SM 유지율 32.2 % ↔ 그림 10 29.9 % (다른 셋은 ±0.1 %p 재현) · 그림 8 나이키스트는 가로 · 세로 축척이 다름 (1.0225 ↔ 0.878 pt/Ω) → 문헌 값을 결과 전 대조에 쓸 때 본문 · 그림 판독을 둘 다 적는다 | 카드 §3-9 · 그림 7a · 10 · 8 | 인쇄 · [판독] | 자리 = 단계 0 (결과 전 대조 등록 꼴)

## n — 논문 에이전트 후보 (원문 참고문헌 목록 서지 그대로 · papers/ 목록 + grep 으로 카드 없음 확인)
- [n] [16] E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Characterization of solid-electrolyte/active-material composite particles with different surface morphologies for all-solid-state batteries, Adv. Powder Technol. 33 (2022), 103470, https://doi.org/10.1016/j.apt.2022.103470. | m ② · ③ · 흐름 밖 (믹서 Ⓒ 코팅 팔) — 이 논문 공정 조건의 근거 [13,16] · 껍질 표면 형태별 성능 = 코어–셸 출발 상태를 그리는 입력 (카드 §2 · §12) | papers/ 에 hayakawa* 없음 · '103470' grep = kawaguchi2023 이 인용만 (후보 표에는 개수만 · '어긋남' 표의 둘째 번호)
- [n] [19] M. Iwao, R. Sakurai, H. Nakamura, E. Hayakawa, S. Ohsaki, S. Watano, Solid electrolyte/graphite composite particle for an all-solid-state lithium-ion battery, Adv. Powder Technol. 33 (2022), 103633, https://doi.org/10.1016/j.apt.2022.103633. | R7 · m — 깨지기 쉬운 핵 (흑연) 에 같은 건식 코팅을 *"by controlling the preparation conditions"* (p.2) — 코팅 공정의 핵 손상 · 조건 창 (카드 §12) | papers/ 에 iwao 없음 · '103633' grep 0 건
- [n] [27] W. Zhang, T. Leichtweiß, S.P. Culver, R. Koerver, D. Das, D.A. Weber, W.G. Zeier, J. Janek, The detrimental effects of carbon additives in Li10GeP2S12-based solid-state batteries, ACS Appl. Mater. Interfaces 9 (2017) 35888–35896, https://doi.org/10.1021/acsami.7b11530. | 흐름 밖 (탄소–SE 부반응 · STEP3/STEP5 탄소 촉매 분해) — CA 셀이 3.6 V 전에 10–15 mAh/g 를 쓰는 부반응의 인용처 (카드 §3-4 · §12) | papers/ 에 zhang2017 없음 · '35888' grep = kato2018 이 인용만
- [n] [26] K. Yoon, J.-J. Kim, W.M. Seong, M.H. Lee, K. Kang, Investigation on the interface between Li10GeP2S12 electrolyte and carbon conductive agents in all-solid-state lithium battery, Sci. Rep. 8 (2018) 8066, https://doi.org/10.1038/s41598-018-26101-4. | m ① · 흐름 밖 — "VGCF 의 1 차원 꼴이 전자 공급을 쉽게 한다" (p.6) 의 인용처 · CA 차원 효과 (카드 §3-4 · §12) | papers/ 에 yoon2018 없음 · '8066' · 's41598-018-26101' grep 0 건
- (세지 않음) [10] Hayakawa 2022 *Adv. Powder Tech.* 33, 103705 (고전단 혼합기) = 후보 표 N-87 · [36] Shi 2020 (*J. Mater. Chem.* 8, 17399 — 원문 목록 표기) = 후보 표 N-101 · [11] Sakuda 2011 = 정본 카드 `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode`.

## 카드 문제
- `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` **L288** (ref 26): *"★ 코팅 입자의 전자 경로 문제 (이 논문 Xs 0.3 붕괴) 를 도전재로 푸는 같은 그룹 후속"* — 같은 그룹 · 방향은 맞지만 **'후속' 은 시간 순서가 반대**다: 이 논문 접수 2022-09-16 · 온라인 2022-11-17 (p.1) ↔ Kawaguchi 2023 온라인 2023-11-01 (그 카드 L15) · Kawaguchi 2023 이 이 논문을 인용한다 → 선행 논문.  또 "도전재로 푸는" 은 AB 에 한정 (VGCF 는 율속 · 수명 못 품 · AB 도 압분체 σ_e 는 막자 혼합의 0.22).  서지 (저자 · 제목 · 권 · 번호) 는 원문과 같다.  고치지 않음.
- `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` **L363** (refs 63 · 64): 두 논문 (이 논문 = 건식 충격 블렌딩 **코팅** · [64] = 이 논문 ref [10] 고전단 **혼합기** 건식 혼합) 을 한 줄 *"고강도 혼합 코팅 (오사카 그룹)"* 으로 묶었다 — 이 논문 자체에는 혼합기가 없다.  서지 둘은 원문 (이 논문 목록 [10] 포함) 과 같다.  고치지 않음.
- `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` **L508** · `kawaguchi2023_…` **L287** (ref 25 = 이 논문 ref [16] · 호 "(3)" 은 이 논문 목록에 없음) · 후보 표 N-81 서지: 원문과 같음 — 문제 없음.
