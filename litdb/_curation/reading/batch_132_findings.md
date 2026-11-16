# batch 132 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 N-83)

대상: `han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode` — S. Han · E.-H. Noh · S. Chae · K. Kwon · J. Lee · J.-S. Woo · S. Park · J.W. Lee · P.J. Kim · T. Song\* · W.-J. Kwak\* · J. Choi\*\*, "Mitigating PTFE decomposition in ultra thick dry-processed anodes for high energy density lithium-ion batteries", *J. Energy Storage* **96** (2024) 112693 · DOI 10.1016/j.est.2024.112693 (접수 2023-12-20 · 온라인 2024-06-24 · CC BY-NC 4.0).
건식 PTFE 흑연 음극 (흑연 : CB : PTFE = 96 : 1 : 3 · 14.4 mg/cm² · ≈92 µm · 1.55 g/cm³) 의 첫 리튬화 PTFE 환원 분해 (0.3–0.55 V vs Li) 를 전해질 첨가제 FEC 10 wt% (VC 1 wt% 기준 전해질에 더함) 가 줄인다 — 반쪽 셀 CV · ICE · 사이클 · 율속 · EIS (+ Li 대칭 셀 빼기) · XPS · HRTEM · XRD · Raman (PTFE 50 wt% 전극) · 나노압입 · SAICAS · 단면 SEM · LFP 전셀 (4.8 · 7.5 mAh/cm²) · 단층 파우치.  **액체 LIB · 압력 숫자 없음 · 계산 없음.**
쪽 = 인쇄 쪽 = PDF 쪽 (p.1–9) · SI p.1–19 (받은 사본) · 판독 원자료 = `litdb/figures/han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode/digitized.csv` (39 행 · 래스터 축 틀 화소 대응) · 고른 의도 대조 = **채움** (카드 §0-1 — 건식 음극 PTFE 분해 · 후막 · FEC · lee2026_li 서론 · 레시피 · 전해질의 출발점 모두 원문에 있음 · 'PVDF 보다 높은 전위' 는 다른 출처 ref 20).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 고체전해질이 없고 압력 · 기공 숫자도 없다 ('porosity' 0 회 · 'pressure' 는 참고 [34] 제목뿐 · 카드 원문 대조 기록).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 압밀 제하 회복 자료는 없음 ('unload' 0 회).  가까운 것 둘 (둘 다 압밀 제하가 아니다):
- [b] han2024_fec_… (Han · … · Choi 2024, J. Energy Storage 96, 112693) | 나노압입 국소 '탄성 회복' 42.87 % (FEC 없음) · 50.42 % (FEC) — 1 사이클 뒤 다공 복합 전극 · HM2000 · 정의 (깊이 비 / 일 비) · 하중 · 압입자 미기재 · 그림 4a 곡선은 0 하중 전에 끝남 (깊이 비 어림 ≈37 · ≈51 % [판독]) | 카드 §3-6 · 표 S2 (SI p.12 · `tab_S2.png`) · 그림 4a (`fig_4a.png`) | 인쇄 (표) · [판독] (곡선) | 압입 국소 응답 · 액체 LIB 흑연 음극 · 우리 단계 6 (압밀 탈압) 과 다른 양
- [b] han2024_fec_… | 첫 사이클 뒤 전극 두께 ≈92 → 149 µm (FEC 없음 · +62 %) · 109.3 µm (FEC · +19 %) — 탈리튬화 끝 · 단면 SEM 한 장씩 · 저자 *"the excellent elastic behavior during delithiation with improved binding network"* | 카드 §3-6 · p.6 · 그림 4c–d (`fig_4c.png` · `fig_4d.png` · `txt_p6_nanoindentation_saicas_thickness.png`) | 인쇄 (그림 글자) · [카드 산술] (%) | 하중 해제가 아니라 리튬화 부피 변화 + 결착망 상실 · 사이클 뒤 두께를 압밀 기공과 섞지 않는다

## c — 항복 · 경도 · 크리프 값과 정의
- [c] han2024_fec_… (Han 2024, J. Energy Storage) | 1 사이클 뒤 건식 흑연 음극 (PTFE 3 wt%) 국소 나노압입: 경도 3.95 (FEC 없음) · 1.33 MPa (FEC) · 탄성률 54.60 · 17.80 MPa — *"mechanical properties of the PTFE binder in local region of the dry-processed anodes"* | 카드 §3-6 · 표 S2 · p.6 (`txt_p6_nanoindentation_saicas_thickness.png`) | 인쇄 | 경도 종류 (Martens · 압입 경도) · 압입자 · 하중 · 횟수 · 자리 미기재 · 일축 항복으로의 환산 없음 · 다공 망 응답 (PTFE 고유값 아님)
- [c] han2024_fec_… | ⚠ 단위 함정: 그림 4a x 축 글자 'Penetration Depth (nm)' ↔ 표 MPa — F/(26.43 h²) 를 µm 로 계산하면 2.62 mN · 5.37 → 3.43 MPa · 2.42 mN · 8.83 → 1.17 MPa (표 3.95 · 1.33 · 비 2.94 ↔ 2.97) · nm 이면 TPa 급 ⇒ 깊이 단위는 µm 로 읽어야 맞다 | 카드 §3-6 · §11-2 · 그림 4a | [판독] · [카드 산술] | 원문 축 글자 오기로 보임 (원문은 말 없음)
- [c] han2024_fec_… | 최대 하중 유지 중 깊이 증가 ≈0.5 (FEC 없음) · ≈0.8 (FEC) 깊이 단위 (크리프꼴) — 유지 시간 미기재 | 카드 §3-6 · 그림 4a | [판독] | 크리프 정의 · 시간 없음
- [c] han2024_fec_… | 다른 카드 대조: PTFE 초기 전단 탄성률 223.7 MPa · 체적 탄성률 2.72 GPa (`kang2026_multiscale_*` SI 표 1) ↔ 이 전극 국소 탄성률 17.8–54.6 MPa = 1/4–1/13 | 카드 §3-6 · §7-3 | [카드 산술 · 다른 카드] | 재료 · 시험 · 상태가 다르다 — 배수 전이 금지

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중 · 압력 측정 없음 (흑연 + PTFE 3 wt% 단일 활물질 전극).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산이 없고 영상은 2D 단면 · 윗면 (SEM · HRTEM) 뿐 · 2D → 3D 진술 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 복합 양극 · SE · 압력 · 기공 없음.
- [i] han2024_fec_… | (참고 · 기공 아님 · 음극) 건식 흑연 음극 밀도 1.55 g/cm³ (14.4 mg/cm² · ≈92 µm) · 1.3 g/cc (24.8 mg/cm²) — 진밀도 미기재 · ρ_t 2.2–2.3 g/cm³ 가정 시 기공 29.5–32.6 % · 40.9–43.5 % | 카드 §3-1 · §7-2 · p.3 (`txt_p2_p3_electrode_fabrication.png`) · 그림 S13 | 인쇄 (밀도) · [카드 산술 · ρ_t 가정] | 액체 LIB 음극 · 압연 압력 미기재 — 랩 표준과 다른 문헌 값

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] han2024_fec_… | 압연 · 섬유화 조건 전부 미기재 — *"the kneaded sheet was not subjected to enough force for a uniformly fibrillated electrode. To solve this problem, we bent it in half and repeat the calendered by utilizing roll-to-roll calender machine"* (접기 횟수 · 간극 · 하중 · 롤 온도 없음) | 카드 §3-1 · p.2 (`txt_p2_p3_electrode_fabrication.png`) | 인쇄 · [미확인] | 압력 대응 불가 · 믹서 V2 앵커 불가
- [j] han2024_fec_… | 후막 (24.8 mg/cm²) 은 압연 뒤 균열 유무 사진 (슬러리 = *"significant cracking after the calendering process"* · 건식 = 없음) 과 FEC 전셀만 — 분해 · 기계 측정 없음 | 카드 §3-7 · p.7 · 그림 S13 (`fig_S13.png` · `txt_p7_ultrahigh_loading_pouch.png`) | 인쇄 (정성) | 균열 정량 · 압력 없음
- [j] han2024_fec_… | 원문에 'limitation' 절 없음 · 셀 수 · 오차 막대 · 코인 온도 미기재 · 나노압입 · SAICAS 조건 미기재 | 카드 §0 ⑧ · §11-8 · §11-13–14 | [미확인] | 모든 비교가 한 쌍

## k — DEM 의 한계
- [k] han2024_fec_… (S. Han et al., J. Energy Storage 96 (2024) 112693) | **말 없음** — DEM 을 쓰지 않았다 ('DEM' · 'discrete' · 'simulat' · 'finite' 0 회 · 'model' 은 참고 [27] 제목뿐) | 카드 §4-4 (i) · 원문 대조 기록 | 원문 전수 검색 | —

## l — 소성변형이 왜 어려운가
- [l] han2024_fec_… (S. Han et al., J. Energy Storage 96 (2024) 112693) | **입자 소성 · 계산의 어려움 = 말 없음.**  기계 이야기는 바인더 쪽만: PTFE 는 *"undergoes fibrilization through shear mixing and calendering with other electrode materials [25–27]"* (p.2) · 분해 부산물이 *"rigid C=C bonds can cause PTFE to lose its flexible properties, thereby reducing the ability of PTFE as a binder through fiberization [38]"* (p.4) · 1 사이클 뒤 FEC 없는 전극이 더 뻣뻣하고 (54.60 vs 17.80 MPa) 접착이 약하고 (0.223 vs 0.272 kN/m) 두껍다 (149 vs 109.3 µm) | 카드 §3-5 · §3-6 · §4-4 (ii) · p.2 · p.4 · p.6 (`txt_p2_ptfe_fibrillation_lumo_defluorination.png` · `txt_p4_xps_hrtem_sei.png` · `txt_p6_nanoindentation_saicas_thickness.png`) | 인쇄 | 계산 · 우회 · 맞춘 값 없음 · 흑연 입자 자체의 변형 · 파쇄 측정 없음

## m — 받아들일 통찰
- [m] han2024_fec_… | **PTFE 의 Li 재고 상한식을 결과 전에 쓴다**: 식 (1) (C₂F₄ 당 Li 4 개) → Q_PTFE ≤ 1072 mAh/g × w_PTFE · 3 wt% · 흑연 96 wt% 에서 ≤ 33.5 mAh/g_흑연 (0.463 mAh/cm²) < 관측 비가역 차 56.6 mAh/g → 첨가제 효과를 '바인더 보호' 로 통째 귀속하지 않는다 | 흐름 밖: R_int · STEP4 풀셀 Li 재고 · A10 원장 (첫 사이클 손실 항목 나누기) | 카드 §3-3 · 식 (1) (`eq_01_ptfe_defluorination.png`) · 그림 2b–c | [카드 산술] — 가정: mAh/g = 흑연 기준 · 전량 반응
- [m] han2024_fec_… | **STEP3 'PTFE = 불활성 절연' (centerline · CL-60) 에 전위 창 표지**: 음극 전위 ≲ 0.55 V (vs Li) 에서 PTFE 는 반응 상 (탈불소 → LiF + 탄소) · 양극 쪽 불활성은 `schmitt2026_*` (황화물 ASSB) — ASSB 음극 복합체 · 분리막 PTFE 계산에는 반응 · 상 전환 항을 결과 전에 등록 · A10 #31 의 30 사이클 감쇠꼴의 근거는 아니다 (음극 쪽 분해는 첫 리튬화의 일 — CV 혹이 2 · 3 번째 사이클에 없음 [판독 · 그림 S3]) | 흐름 밖: STEP3 PTFE 스탬프 · A10 #31 | 카드 §7-4 · p.3 · 그림 2a · S3 | 인쇄 · [판독]
- [m] han2024_fec_… | **반쪽 셀 EIS 에서 상대 전극 몫을 대칭 셀로 빼는 꼴**: Li ‖ Li 반원 153.2 · 121.8 Ω 의 반 (76.6 · 60.9) 을 반쪽 셀 합 235.5 · 154.6 Ω 에서 빼 전극 158.9 · 93.7 Ω — 두 셀의 Li 계면이 같다는 가정은 검사 안 함 | 흐름 밖: 실험 대조 EIS (반쪽 셀 · In/InLi 상대 전극) · R_int 트랙 | 카드 §3-4 · p.4 · 표 S1 · 그림 S6 (`txt_p4_eis_symmetric_cell_resistance.png`) | 인쇄 · [카드 산술 검산]
- [m] han2024_fec_… | **문헌 압입 곡선은 표 값과 단위 검산 뒤에만 쓴다** — 그림 4a 'nm' 축이 표 S2 MPa 와 10⁶ 배 어긋난다 (F/26.43 h² 로 바로 드러남) | c 질문 · 결과 전 대조 항목 (문헌 경도 · 항복 값 옮길 때) | 카드 §3-6 · §11-2 | [판독] · [카드 산술]

## n — 논문 에이전트 후보
- [n] D.J. Lee, J. Jang, J.-P. Lee, J. Wu, Y.-T. Chen, J. Holoubek, K. Yu, S.-Y. Ham, Y. Jeon, T.-H. Kim, J.B. Lee, M.-S. Song, Y.S. Meng, Z. Chen, Physio-electrochemically durable dry-processed solid-state electrolyte films for all-solid-state batteries, Adv. Funct. Mater. 33 (28) (2023) 2301341. | m · F 목록 — **황화물 ASSB 의 건식 PTFE SE 막**의 전기화학 안정성 (PTFE 분해 Raman D · G 비대칭의 출처 · 카드 §3-5 · §12) — 우리 계 (LPSCl + PTFE) 에 가장 가까운 PTFE 안정 창 자료 | papers/ 목록 · 'Physio-electrochemically durable' grep = `lee2024_shear_force_*` · `schmitt2026_*` 가 인용만 · 카드 없음
- [n] Y. Zhang, F. Huld, S. Lu, C. Jektvik, F. Lou, Z. Yu, Revisiting polytetrafluorethylene binder for solvent-free lithium-ion battery anode fabrication, Batteries 8 (6) (2022) 57. | m — 음극 PTFE 환원 (carbyne) 의 직접 자료 (카드 §12 [22] · `matthews2024_*` 도 인용만) | 'Revisiting polytetrafluor' grep 0 건 · 카드 없음
- [n] G. Li, R. Xue, L. Chen, The influence of polytetrafluorethylene reduction on the capacity loss of the carbon anode for lithium ion batteries, Solid State Ionics 90 (1) (1996) 221–225. | m — PTFE 환원 → 탄소 음극 용량 손실의 원전 (0.3–0.55 V 근거 [29] · 카드 §3-3 상한식 대조) | 'polytetrafluorethylene reduction' grep = `schmitt2026_*` 인용만 · 카드 없음
- [n] S. Shiraishi, T. Kobayashi, A. Oya, Electrochemical lithium ion doping and undoping behavior of carbyne-like carbon film electrode, Chem. Lett. 34 (12) (2005) 1678–1679. | m — 식 (1) 의 출처 (C₂F₄ 당 Li 4 개 · 카드 §11-1 'Soshi et al.') | 'carbyne' grep = `matthews2024_*` 낱말만 · 이 서지 카드 없음
- [n] Y. Zhang, S. Lu, F. Lou, Z. Yu, Leveraging synergies by combining polytetrafluorethylene with polyvinylidene fluoride for solvent-free graphite anode fabrication, Energy Technol. 10 (11) (2022) 2200732. | l · m — PTFE + PVDF 혼합 바인더로 건식 흑연 음극의 PTFE 환원 · 결착 상실을 줄이는 다른 길 (카드 §12 [33]) | 'Leveraging synergies' grep 0 건 · 카드 없음

## 카드 문제
- `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` **L411** (참고 [17]): 저자 목록이 *"… P.J. Kim, T. Song,"* 에서 끝남 ↔ 원문 첫 쪽 · SI 첫 쪽 = **12 명** (… Taeseup Song, **Won-Jin Kwak, Junghyun Choi**) — 교신저자 둘 빠짐 (Kim 2026 원문 인쇄를 옮긴 것인지 카드 누락인지 [미확인]).  후보 표 N-83 행의 서지도 이 줄을 따름.  고치지 않음.
- `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` **L384** (참고 [9]): 제목 *"ultra-thick"* ↔ 원문 *"ultra thick"* (붙임표 없음) — 사소한 표기 차.  고치지 않음.
- `lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode` **L353** (§11-2): "원 논문 저자 목록 [미확인]" 으로 남긴 kim2026 ↔ lee2026_li 표기 차는 이 원문으로 풀림 — lee2026_li L363 (12 명) 이 맞다.  고치지 않음 (그 카드의 정정 후보).
- 세 카드 (kang2026 L384 · kim2026 L411 · lee2026_li L363) 의 "카드 없음" → 이제 `han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode` 가 있다 (링크 갱신 후보 · 고치지 않음).
