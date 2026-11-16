# batch 133 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 N-84)

대상: `puls2024_interlab_benchmark_assb_cell_reproducibility_21_groups` — S. Puls · E. Nazmutdinova · F. Kalyk · H. M. Woolley · J. F. Thomsen · … (55 명) · W. G. Zeier · N. M. Vargas-Barbosa\*, "Benchmarking the reproducibility of all-solid-state battery cell performance", Nature Energy 9 (October 2024) 1310–1320 (Analysis) · DOI 10.1038/s41560-024-01634-3 · SI 42 쪽 + Source Data .xlsx 6 개 (커밋 안 함 · 셀별 발췌 = `litdb/figures/puls2024_…/source_data_cells_extract.csv`).
같은 재료 (단결정 NMC 622 · Li₆PS₅Cl MSE D50 ≈1 µm · In 박) 를 21 개 연구 그룹에 보내 같은 처방 · 같은 전기화학 절차 (0.05 C ×2 → 0.1 C ×50 · 3.0–4.3 V vs Li⁺/Li) 로 셀을 만들게 하고 조립 (압력 · 시간 · 셀 틀) 은 각자 하게 한 실험실 간 연구 — 시도 68 · 완주 39 · 0.1 C 첫 방전 21–143 mAh g⁻¹.
쪽 = 인쇄 쪽 p.1310–1320 (PDF 쪽 = 인쇄 − 1309) · SI 는 'SI p.n' (SI 인쇄 쪽) · 고른 의도 대조 = **일부** (카드 §0-1 — 21 그룹 · 같은 재료 · 같은 전기화학 절차 · 큰 흩어짐 · 세 벌 권고 = 채움 · "같은 절차" 는 전기화학 절차뿐 · "조립 조건 (적층압 등) 때문에" 는 적층압 → 유지율 동행만 · n ≥ 2 는 원문 기준 (세 벌) 아래).
인용 서지 (질문 k · l 용): Puls et al., Nat. Energy 9 (2024) 1310–1320.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 압력별 기공 · 밀도 곡선이 없다 (한 압력 펠릿 하나와 셀 표의 두께 기록뿐).
- [a] puls2024_interlab_… | (참고 · 곡선 아님) 조정 그룹 LPSCl 펠릿 250 mg · ⌀10 mm · 380 MPa 3 분 · 두께 2.02 · 2.19 mm → 겉보기 1.573 · 1.458 g cm⁻³ → 저자 'theoretical' 1.87 기준 기공 15.9 · 22.1 % ↔ 랩 표준 1.64 기준 4.1 · 11.1 % | 카드 §3-8 · SI 표 26 · p.1317 (`tab_S26.png` · `txt_p8_eis_pellet_380mpa_3min_2000um_60mpa.png`) | [인쇄] 질량 · 두께 · [카드 산술] 밀도 · 기공 | 두께를 잰 상태 (다이 안 · 밖 · 하중 중 · 뺀 뒤) 미기재 · 한 압력 · 랩 표준과 다른 문헌 값 (판정 · 맞춤에 안 씀)
- [a] puls2024_interlab_… | (참고 · 곡선으로 쓸 수 없음) 같은 분말 · 다른 실험실의 셀 분리막 겉보기 밀도 m_SE/(A·l_SE) 1.41–1.79 g cm⁻³ (27 셀 · 13 그룹 · 중앙 1.50) · 분리막이 받은 최대 압력 255–720 MPa 와 Spearman −0.30 (720 MPa 셀이 가장 낮은 1.41) · 1.64 로 나누면 F · H · K · N 이 1 초과 · S 의 l_SE 200 µm = 3.8 g cm⁻³ | 카드 §3-9 · SI 표 2–20 · MOESM6 | [카드 산술] | 셀 표의 두께 기록 (상태 · 방법 없음 · 둥근 수 많음) — 밀도 측정이 아니다

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 되돌아옴 · 탈압 곡선 측정이 없다.
- [b] puls2024_interlab_… | (정성 · 값 없음) *"the OCV could be influenced by the pressure relaxation, which is observed in ASSB cells after compression"* · *"the specific compression profiles, including how fast the pressure is applied and released, and the way the pressure was controlled (if it was controlled at all; Supplementary Table 1), was not monitored in this study but is expected to have an effect on the microstructure"* · Table 1 이 압력 이력 (올림 · 내림 속도) 을 보고 항목으로 권고 | 카드 §4-3 · p.1312 (`txt_p2_p3_thickness_similar_compression_profile_not_monitored.png`) · p.1316 Table 1 (`tab_1.png`) | [인쇄] | 이완 문장은 [22] Koerver 2017 인용 · 이 논문의 측정 아님

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 항복 · 경도 값이 없다.
- [c] puls2024_interlab_… | (인용 문장 · 값 없음) *"high pressure (>300 MPa) and long compression times (in the order of several hours) are required to densify and reduce residual void space in thiophosphate-based SEs that enable higher ionic conductivities"* — 시간 의존 치밀화 (크리프 쪽) 의 실험 쪽 진술 | 카드 §3-2 · §4-3 · p.1311 (`txt_p2_pressures_10_70_250_520_durations_300mpa_nmc_breaking.png`) | [인쇄 · refs 13–14 인용] | 원전 = Cronau 2021 · Perrenot 2024 (n 절) · 이 논문의 측정 아님

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 복합 양극 기공 측정이 없다.
- [i] puls2024_interlab_… | (함정) 셀 표의 복합 양극 두께 l_CC (14–180 µm · 같은 로딩 ≈10 mg cm⁻² CAM) 로 낸 겉보기 밀도 0.83–10.4 g cm⁻³ (Q2 10.4 · Q1 6.6 = 불가능) → 복합 양극 기공은 계산할 수 없다 | 카드 §3-9 · SI 표 2–20 · MOESM6 | [카드 산술] | 두께 기록의 상태 · 방법 미기재 · 양극 압력 50–720 MPa 가 그룹마다 다름

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] puls2024_interlab_… | 저자가 조사 못 한 것: *"the (in)homogeneity of the positive composite electrode preparation via hand grinding, microstructure of each component influenced by the compression profiles, current collector surface texture, material degradation during storage and the preparation protocol of the In/(InLi)x alloy negative electrode"* + O₂ · H₂O · 용매 · 운전 중 압력 · 온도 제어 | 카드 §3-10 · p.1316 (`txt_p7_not_investigated_hand_grinding_compression_profiles.png`) | [인쇄] | 압력 이력 → 미세구조는 가설 (이 논문 안 검증 없음)
- [j] puls2024_interlab_… | 낮은 용량 셀의 원인은 *"difficult to ascertain within the present study"* · 경험상 혼합 · 분포 불균일과 무게 오차 (측정 아님) · 처리 변수 ↔ 성능의 뚜렷한 경향 없음 (*"clear trends between the processing parameters and the electrochemical cell performance are not evident in this study"*) | 카드 §0-1 · §3-4 · p.1313 · p.1315 | [인쇄] | 조립을 일부러 풀어 변수가 함께 움직인다
- [j] puls2024_interlab_… | 적층압 > 40 MPa 셀이 잘 돌았다는 것은 *"a bias towards good cell performance and not necessarily transferability of the results to application-oriented ASSB cells"* (응용 0–10 MPa) | 카드 §3-5 · p.1314 · p.1316 | [인쇄] | 운전 적층압 = 우리 압밀 계산의 변수 아님

## k — DEM 의 한계 (서지: Puls et al., Nat. Energy 9 (2024) 1310–1320)
- [k] puls2024_interlab_… (Puls et al., Nat. Energy 2024) | **말 없음** — 본문 · SI 에 DEM · discrete · simulation 낱말 0 회 · 계산 · 입자 모델 없음 | 카드 §4-3 · 원문 대조 기록 | [인쇄 전수] | 실험 셀 연구

## l — 소성변형이 왜 어려운가 · 우회 (서지: Puls et al., Nat. Energy 9 (2024) 1310–1320)
- [l] puls2024_interlab_… (Puls et al., Nat. Energy 2024) | 계산 쪽 **말 없음**.  실험 쪽 인용 문장 하나 (값 없음): *"Indeed, high pressure (>300 MPa) and long compression times (in the order of several hours) are required to densify and reduce residual void space in thiophosphate-based SEs that enable higher ionic conductivities. However, NMC (secondary) particles are prone to breaking at such pressures, especially when compressed for extended periods of time."* — 치밀화가 압력만이 아니라 시간에 달리고 (크리프 쪽) 그 조건이 AM 파괴와 맞부딪힌다는 진술 | 카드 §3-2 · §4-3 · p.1311 | [인쇄 · refs 13–15 인용] | 우회 · 맞춘 값 · 비용 없음 (계산 없음) · 원전 = Cronau 2021 (카드 있음) · Perrenot 2024 · Perrenot 2023 (n 절)

## m — 받아들일 통찰
- [m] puls2024_interlab_… | **실험 앵커 등록 양식 = 원문 Table 1 여덟 칸 + 셀 수 · SD 식 · 실패 셀 수** (압력 p_x · 시간 t_x · 압력 이력 (올림 · 내림 속도) · 적층압과 제어 · In : Li 원자비 · CAM 로딩 · 초기 OCV · 휴지 시간) — 이 논문에서 시도 68 셀 중 43 % 가 실패했고 *"The number of non-working cells is generally not reported in the literature"* | 자리: 단계 0; 결과 전 대조 항목 (실험값을 받을 때 칸이 비면 '조건 미확인' 표지) | 왜: p.1312 · p.1316 Table 1 · 카드 §9 ①
- [m] puls2024_interlab_… | **"n ≥ 2 평균" 통계의 함정** — 원문 SD 는 모집단 식 (n = 2 이면 두 값 차의 절반) · 두 셀 10.0 → 세 셀 7.0 mAh g⁻¹ 는 평균만 줄었고 중앙은 4.58 ↔ 4.49 · OCV 이상 셀을 빼면 7.2 ↔ 5.9 · 50 사이클은 4.3 ↔ 5.0 (거꾸로) · 모집단 식이면 세 셀 쪽 기대값이 오히려 크다 ⇒ 차이 주장은 평균의 표준오차 (SD/√n) 와 셀 수 · SD 식을 함께 | 자리: 흐름 밖: 실험 대조 통계 (문헌 앵커의 셀 수 표지) · 우리 시드 산포 보고 | 왜: p.1315 · MOESM6 'Stdev and median rel error' · 카드 §3-6
- [m] puls2024_interlab_… | **셀 표의 두께 · 질량으로 순수 SE 기공을 만들지 않는다** — 같은 분말 · 255–720 MPa 의 분리막 겉보기 밀도가 압력 경향 없이 1.41–1.79 g cm⁻³ · 랩 표준 1.64 를 넘는 그룹 넷 · 복합 양극 두께로는 0.83–10.4 g cm⁻³ | 자리: 단계 0 (문헌 기공 등록 = 두께를 잰 상태 · 방법 · 진밀도 분모 칸 필수) | 왜: 카드 §3-9 · SI 표 2–20
- [m] puls2024_interlab_… | **σ₀ 는 한 값이 아니라 띠** — 같은 MSE LPSCl: 펠릿 1.63 · 1.85 mS cm⁻¹ (25 °C · 380 MPa · 60 MPa 틀) · 셀 분리막 겉보기 l_SE/R0 0.89–2.81 (중앙 1.41 · 20 셀 · 2 번째 충전 R0) — 우리 σ₀ 보고 기준 1.5 는 띠 안 · 솔버 상수 3.0 은 띠 위 | 자리: 결과 전 대조 항목; 단계 7 (σ_ion 절대값 대조의 σ₀ 민감도 표지) | 왜: SI 표 25 · 카드 §3-8 · §3-9 · §7-3

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] Perrenot, P. et al. Room‐temperature sintering of amorphous thiophosphate solid electrolyte (Li3PS4): coupling morphological evolution to electrochemical properties. Adv. Funct. Mater. https://doi.org/10.1002/adfm.202310739 (2024). | c · l · 단계 4 · M0 — *">300 MPa"* · *"several hours"* 시간 의존 치밀화의 인용처 (p.1311) — 카드 §3-2 · §12 | papers/ 목록 · 'perrenot' · '2310739' grep = 카드 없음 (jeong2024 [20] · korjus2025 [18] · thompson2026 [2] 가 인용만)
- [n] Perrenot, P., Bayle-Guillemaud, P. & Villevieille, C. Composite electrode (LiNi0.6Mn0.2Co0.2O2) engineering for thiophosphate solid-state batteries: morphological evolution and electrochemical properties. ACS Energy Lett. 8, 4957–4965 (2023). | d · l · R7 · 단계 5 — NMC 2 차 입자가 고압 · 긴 압축에서 깨진다는 인용처 (p.1311) · NMC 622 복합 양극의 형태 변화 — 카드 §12 | 'perrenot' · '4957' grep = 카드 없음 (jeong2024 [17] 은 같은 저자 · 같은 해를 'ACS Energy Lett. 8, 4531' 로 적는다 — 같은 논문인지 [미확인])
- [n] Koerver, R. et al. Capacity fade in solid-state batteries: interphase formation and chemomechanical processes in nickel-rich layered oxide cathodes and lithium thiophosphate solid electrolytes. Chem. Mater. 29, 5574–5582 (2017). | b · 단계 6 — 압축 뒤 *"pressure relaxation"* 의 인용처 (p.1312) — 카드 §4-3 · §12 | 'koerver' · '5574' grep = 카드 없음 (`koerver2018_…` 은 다른 논문 · clausnitzer2024 · jung2019 · kalnaus2023 · liu2024 · nam2018 · strauss2018 · tian2020 이 인용만)
- [n] Randau, S. et al. Benchmarking the performance of all-solid-state lithium batteries. Nat. Energy 5, 259–270 (2020). | m · 흐름 밖 — 셀 수준 벤치마크 · 목표 비에너지 250–400 Wh kg⁻¹ (p.1316 [1,35]) — 카드 §12 | 'randau' · '259–270' grep = 카드 없음 (beutl2024 [36] 이 인용만)

## 카드 문제
- `alharbi2026_coupled_design_ultrathin_composite_se_review` **L332**: *"[110] 의 저자가 'Zeier, W. G. & Vargas-Barbosa, N. M.' 두 사람으로만 적혀 있다 — … (교신저자만 남긴 것으로 보인다)."* — 원문 저자 55 명 · 마지막 둘이 Zeier · Vargas-Barbosa · **교신은 Vargas-Barbosa 한 사람** (p.1310 · p.1319 · e-mail 하나).  "교신저자만" 은 원문과 다르다 (마지막 두 저자를 남긴 것).
- `alharbi2026_…` **L164** · **L466**: *"21 개 연구실 … 조립 조건 (적층압 · 음극 조성 등) 때문에 'immense spread'"* · *"21 기관 재현성 — 조립 편차 (적층압) 의 크기"* — 수 21 · 같은 재료 · 같은 시험 절차는 맞다.  단위는 **연구 그룹** (원문 *"21 research groups"* · 기관 아님) · 'immense' 는 원문 낱말이 아니다 (원문 *"huge"* · *"large variability"*) · 원문은 흩어짐을 적층압 탓으로 돌리지 않는다 — 적층압 (1–10 MPa) 은 유지율과만 함께 가고 첫 용량과는 무관 (p.1313) · *"clear trends between the processing parameters and the electrochemical cell performance are not evident in this study"* (p.1315).  (L164 의 '[2차 · ref 110]' 표지가 있어 리뷰 서술을 옮긴 것일 수 있다 — 그 리뷰 원문 p.25 는 확인 안 함.)
- `alharbi2026_…` **L386** · **L482** (인용 초안): *"조립 변수로서 재현성을 지배 [110]"* · *"… in particular the applied stack pressure [Nat. Energy 9, 1310 (2024)]"* — 원문보다 강하다 (위와 같은 근거).  원전 확인판 문장 = 카드 §10.
- `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` **L38** · **L122** · **L383** (기준 대조 · 오류 아님): *"Data are averaged from at least two identical cells"* — 그 카드 L404 가 이 논문을 '셀 재현성 기준 (n ≥ 2 평균의 해석)' 으로 적었는데, 원문 기준은 **세 벌 평균 + 오차 범위** 이고 특히 *"low-content (in)active additives (for example, polymer electrolytes, binder and so on)"* 의 효과를 논할 때라고 적는다 (p.1316) — PTFE 0.5 wt% 결착제 시트를 다루는 그 논문은 이 기준보다 한 벌 적다.  L404 의 서지는 원문과 같다.
