<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (대피 세션 · 후보 표 3 순위 N-84 · 정독 133) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 · 두 필수 절 §0-1 · §8 의 꼴).
     원문 = 출판본 (Nature Energy 9 (2024) 1310–1320 · Analysis · 11 쪽 · CC BY 4.0) + Supplementary Information (42 쪽 PDF = 표지 1 + 본문 41 · 표 S1–S26 · 그림 S1–S47)
     + Source Data 6 개 (.xlsx · MOESM2 = 그림 1 · MOESM3 = 그림 2 · MOESM4 = 그림 3 · MOESM5 = 그림 4 · MOESM6 = SI 그림 2–5 + 셀별 'Processing & Summary' + 'Stdev and median rel error' · MOESM7 = SI 그림 11–27 충방전 곡선 36 시트).
     쪽 표기 = 본문은 인쇄 쪽 "p.1310–1320" (PDF 쪽 1–11 · PDF 쪽 = 인쇄 쪽 − 1309).  SI 는 "SI p.n" = SI 인쇄 쪽 번호 (SI PDF 쪽 = n + 1 · SI PDF p.1 = 표지).  크롭 파일 이름의 pN 과 figures.json 의 page 는 **PDF 쪽**이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [원자료] = 저자가 낸 Source Data .xlsx 의 칸 값 (openpyxl read-only · data_only 로 읽음 · 파일은 커밋하지 않음 · 셀별 발췌 = litdb/figures/<slug>/source_data_cells_extract.csv) ·
     [판독] = 그림에서 읽은 값 (방법 병기) · [카드 산술] = 인쇄 · 원자료 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 11 쪽 + SI 42 쪽 + Source Data 6 개 전수에 없음.
     원문 53 쪽은 글자 층 추출 (+ 표 S2–S20 의 파란 글자 = 계산 · 가정 값을 글자 색으로 가려 읽음) + 그림 크롭 전부 열람으로 읽었다.  DEM · 입자 계산 · 압밀 시뮬레이션 · 모델은 없다 — 실험 (21 개 연구 그룹의 셀 자료 + 조정 그룹의 재료 시험 · 데이터 분석). -->
# 21 개 연구 그룹 · 같은 재료 (단결정 NMC 622 · Li₆PS₅Cl MSE D50 ≈1 µm · In 박) · 같은 전기화학 절차 · 조립은 각자 — 전고체 펠릿 셀 성능의 실험실 간 재현성 벤치마크: 시도 68 셀 중 50 사이클 완주 39 (실패 43 %) · 0.1 C 첫 방전 21–143 mAh g⁻¹ (중앙 121.9 · 33 셀) · 성형압 hand-pressed–720 MPa · 적층압 1–400 MPa (< 40 MPa = 유지율 낮음 · 첫 용량과는 무관) · 초기 OCV ≥ 2.5 V vs Li 가 성공 예측 · 세 벌 (triplicate) 평균 · 오차 보고 권고 · Source Data 로 분리막 겉보기 밀도 · porosity · σ 재계산 — Puls · Nazmutdinova · Kalyk · … · Zeier · Vargas-Barbosa (Nat. Energy 2024)

> slug `puls2024_interlab_benchmark_assb_cell_reproducibility_21_groups` · DOI `10.1038/s41560-024-01634-3` · type `experiment (interlaboratory round robin · 21 research groups, same NMC 622 / Li₆PS₅Cl / In materials · own assembly, prescribed electrochemical protocol · press cells · impedance gDRT · source-data reanalysis · no DEM, no simulation)` · PDF `fe6a2acf-84._Benchmarking_the_reproducibility_of_all-solid-state_battery_cell_performance.pdf` · SI `a67389f4-84._SupZ_01_41560_2024_1634_MOESM1_ESM.pdf` · digested `2026-11-16` · status ✅
>
> **저자 (55 명 · 소속 36)**: Sebastian Puls ¹ · Elina Nazmutdinova ²,³ · Fariza Kalyk ¹ · Henry M. Woolley ³,⁴ · Jesper Frost Thomsen ³,⁵ · Zhu Cheng ⁶ · Adrien Fauchier-Magnan ⁷ · Ajay Gautam ⁶ · Michael Gockeln ⁸ · So-Yeon Ham ⁹ · Md Toukir Hasan ¹⁰ · **Min-Gi Jeong** ¹¹ · Daiki Hiraoka ¹² · Jong Seok Kim ¹³ · Tobias Kutsch ¹⁴,¹⁵ · Barthélémy Lelotte ¹⁶ · **Philip Minnmann** ¹⁷ · Vanessa Miß ¹⁸ · Kota Motohashi ¹² · Douglas Lars Nelson ¹⁹ · Frans Ooms ⁶ · Francesco Piccolo ²⁰,²¹ · Christian Plank ²²,²³ · Maria Rosner ²⁴,²⁵ · Stephanie E. Sandoval ¹⁹,²⁶ · Eva Schlautmann ² · Robin Schuster ¹⁴,¹⁵ · Dominic Spencer-Jolly ²⁷,²⁸ · Yipeng Sun ²⁹ · Bairav S. Vishnugopi ¹⁰ · Ruizhuo Zhang ³⁰ · Huang Zheng ³¹ · Philipp Adelhelm ²⁰,²¹ · Torsten Brezesinski ³⁰ · Peter G. Bruce ²⁷,³² · Michael Danzer ²²,²³ · Mario El Kazzi ¹⁶ · Hubert Gasteiger ¹⁴ · Kelsey B. Hatzell ¹¹ · Akitoshi Hayashi ¹² · Felix Hippauf ²⁴ · Jürgen Janek ¹⁷ · Yoon Seok Jung ¹³ · Matthew T. McDowell ¹⁹,²⁶ · Ying Shirley Meng ³³,³⁴ · Partha P. Mukherjee ¹⁰ · Saneyuki Ohno ³¹,³⁵ · Bernhard Roling ¹⁸ · Atsushi Sakuda ¹² · Julian Schwenzel ⁸ · Xueliang Sun ²⁹ · Claire Villevieille ⁷ · Marnix Wagemaker ⁶ · Wolfgang G. Zeier ¹,² · **Nella M. Vargas-Barbosa\*** ¹,²³,³⁶ — ¹ IMD-4 Helmholtz-Institut Münster (FZ Jülich) · ² U. Münster 무기 · 분석화학 · ³ BACCARA (Münster) · ⁶ TU Delft · ⁷ Grenoble (LEPMI) · ⁸ Fraunhofer IFAM · ⁹ UCSD · ¹⁰ Purdue · ¹¹ Princeton · ¹² Osaka Metropolitan · ¹³ Yonsei · ¹⁴ TUM · ¹⁶ PSI · ¹⁷ JLU Giessen · ¹⁸ Marburg · ¹⁹ Georgia Tech · ²⁰ HU Berlin · ²² · ²³ Bayreuth (전기에너지 시스템 · 배터리 센터) · ²⁴ Fraunhofer IWS · ²⁷ Oxford · ²⁹ Western Ontario · ³⁰ KIT · ³¹ Kyushu · ³⁵ Tohoku · ³⁶ Bayreuth 전기화학 (나머지 번호 = 원문 p.1320) — \* 교신 **한 사람** (n.vargas-barbosa@uni-bayreuth.de · p.1310 · p.1319) · *Nature Energy* **9**, **1310–1320** (**October 2024** · 기사 종류 **Analysis** · 호수 미인쇄) · 접수 2024-04-30 · 수락 2024-08-15 · 온라인 2024-09-18 · **CC BY 4.0** (오픈 액세스 = Universität Bayreuth) · 조정 연구비 = FESTBATT (BMBF 13XP0428A) · 심사 = Hong Li + 익명 · 코드 = EC-Idea 툴박스 (Bayreuth).
> **이웃 카드 (링크만)**: [`ohno2020_interlab_ionic_conductivity_argyrodite`](ohno2020_interlab_ionic_conductivity_argyrodite.md) (이 논문 ref [31] · 같은 분야의 앞선 실험실 간 연구 · σ_ion) · [`beutl2024_round_robin_coin_cell_sulfide_assb`](beutl2024_round_robin_coin_cell_sulfide_assb.md) (황화물 코인셀 4 기관 round robin · 인용 관계 없음) · [`kissel2025_cathode_mixing_quality_cam_utilization_reproducibility_press_cells`](kissel2025_cathode_mixing_quality_cam_utilization_reproducibility_press_cells.md) (이 논문을 ref [26] 으로 인용 · 혼합 질 = 실험실 안 흩어짐의 원천) · [`alharbi2026_coupled_design_ultrathin_composite_se_review`](alharbi2026_coupled_design_ultrathin_composite_se_review.md) (ref [110] · L164 · L466 · 가리킨 카드) · [`schmitt2026_chemomech_stability_dry_cathode_separator_sheets`](schmitt2026_chemomech_stability_dry_cathode_separator_sheets.md) (ref [12] · L404 · 가리킨 카드) · [`doux2020_pressure_effects_sulfide_se_jmca`](doux2020_pressure_effects_sulfide_se_jmca.md) (ref [11]) · [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) (ref [13]) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (ref [10]) · [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (ref [16]).
> **원자료 발췌**: `litdb/figures/puls2024_interlab_benchmark_assb_cell_reproducibility_21_groups/source_data_cells_extract.csv` (41 셀 × MOESM6 'Processing & Summary' 64 행 + 카드 산술 열: 분리막이 받은 최대 압력 · 겉보기 밀도 m_SE/(A·l_SE) 와 1.87 · 1.64 대비 · 겉보기 분리막 σ = l_SE/R0 (1 · 2 · 51 번째 충전) · 표지) · 그림 크롭 **92 장** (도구 60 중 다시 자름 39 + 손 크롭 32 = 본문 그림 3 · SI 표 S24 · 식 10 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 상용 단결정 NMC 622 · Li₆PS₅Cl (MSE Supplies · D50 ≈1 µm) · In 박을 **21 개 연구 그룹**에 보내 **같은 처방** (양극 m(CAM) : m(SE) = 70 : 30 손 막자 · CAM 10 mg cm⁻² · 분리막 ≈70–75 mg cm⁻² · In/(InLi)ₓ 음극) 과 **같은 전기화학 절차** (0.05 C 2 회 → 0.1 C 50 회 · 3.0–4.3 V vs Li⁺/Li · PEIS) 로 셀을 만들게 하되 **조립 (압력 · 시간 · 셀 틀) 은 각자** 하게 했더니 — 시도 **68 셀** 중 **39 셀 (57 %)** 만 50 사이클을 돌았고 (실패의 대부분 = 조립 21 셀), 0.1 C 첫 방전은 **21–143 mAh g⁻¹ (중앙 121.9 · 평균 103.7 · 33 셀)** 로 흩어졌으며 (p.1312), 저자는 **처리 변수와 성능 사이 뚜렷한 경향은 없다** 고 적으면서도 (*"clear trends between the processing parameters and the electrochemical cell performance are not evident in this study"*, p.1315) 적층압 **1–10 MPa** 셀의 유지율이 낮다는 것 · 초기 OCV **≥ 2.5 V vs Li⁺/Li** 가 성공 셀을 가른다는 것 (초록은 *"an initial open circuit voltage of 2.5 and 2.7 V vs Li+/Li is a good predictor of successful cycling"* · 그림 3g–i 본문은 *"OCV ≥ 2.5 V"*) · 결과는 **세 벌 (triplicate) 평균과 오차** 로 보고하라는 것을 내놓는다 (p.1316).  **압밀 · 기공 측정 · 탈압 · 모델은 없다** — 셀 수준 재현성 연구다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ "여러 연구실 · 같은 재료 · 같은 절차 → 크게 흩어짐" 의 원전 숫자 | **21 개 연구 그룹** (재료를 보낸 곳 · 자료를 낸 곳) · 그림 · 표에 나오는 그룹 문자는 **19 개** (A–U 중 C · I 없음 · 차이 설명 없음) · 시도 68 · 완주 39 · 0.1 C 해석 33 셀 · 첫 방전 21–143 (결론 문장은 23.7–143.1) · IQR 75.8–132.1 · 50 번째 IQR 44.2–125.3 mAh g⁻¹ | [인쇄] p.1310–1312 · p.1316 · SI 표 1 · S23 · [원자료] |
| ② ★ "조립 조건 (적층압 등) 때문에" | 조립 조건은 실제로 크게 다르다: 분리막 압력 hand-pressed–720 MPa · 양극 압력 50–720 MPa (본문 "평균" 250–520) · 압축 시간 0.02–10 분 · 적층압 1–400 MPa (본문 "대부분 10–70") · 적층압 제어 4 그룹뿐 · In : Li 원자비 0.66–6.61.  **그러나 성능과의 인과는 적층압 → 유지율 한 갈래뿐**: D · F · G (1–10 MPa) 유지율 < 50 % (F1 은 53.9 % [원자료]) · *">25 MPa are required for stable cycling"* (p.1313) ↔ 결론 *">40 MPa"* (p.1316) · 첫 용량은 적층압과 무관 (D1 131.7 · F2 139.6) · 첫 용량은 *"mostly influenced by the processing of the materials during cell assembly"* 이고 낮은 용량의 원인은 경험상 **복합 양극 혼합 · 분포 불균일 + 무게 오차** (p.1313 · 측정 아님) | [인쇄] p.1311 · p.1313 · p.1315–1316 · SI 표 1 · [원자료] |
| ③ ★ 셀 재현성 기준 (n ≥ 2 평균의 해석) | 권고 = *"report … at least the average and error ranges of triplicates"* · 실패 셀 수 보고 (p.1316 · 초록 *"advocate for reporting data in triplicate"*) · 근거 = 두 셀 그룹의 SD 평균 **10.0** ↔ 세 셀 그룹 **7.0 mAh g⁻¹** (p.1315).  ⚠ [카드 산술 · 원자료]: SD 는 **모집단 식 (ddof = 0)** — 두 셀이면 SD = 두 값 차의 절반 · 같은 시트의 **중앙값은 4.58 ↔ 4.49 (거의 같다)** · 10.0 ↔ 7.0 에는 "모든 통계에서 뺐다" 던 OCV 이상 셀 그룹 (A · F) 이 들어 있다 → 빼면 **7.2 ↔ 5.9** · 50 번째 사이클에서는 **4.3 ↔ 5.0 (거꾸로)** (§3-6) | [인쇄] p.1310 · p.1315–1316 · [원자료] MOESM6 'Stdev and median rel error' · [카드 산술] |
| ④ 순수 SE (LPSCl) 펠릿 값 | 조정 그룹 펠릿: 250 mg · ⌀10 mm PEEK · **380 MPa 3 분** → 두께 2.02 · 2.19 mm (≈2,000 µm) · **60 MPa 틀 압력 아래** PEIS · 25 °C **1.63 · 1.85 mS cm⁻¹** · Ea 0.388 · 0.400 eV.  [카드 산술] 겉보기 밀도 **1.573 · 1.458 g cm⁻³** = 저자 이론 밀도 1.87 의 84.1 · 77.9 % · 랩 표준 1.64 의 95.9 · 88.9 % (두께를 잰 상태 [미확인]) | [인쇄] p.1317 · SI 표 25 · 26 · 그림 S47 · [카드 산술] |
| ⑤ [카드 산술] 같은 분말 · 다른 실험실의 분리막 | 셀별 m_SE · l_SE · 지름으로 겉보기 밀도 **1.41–1.79 g cm⁻³** (27 셀 · 13 그룹 · 중앙 1.50) — 분리막이 받은 최대 압력 (255–720 MPa) 과 **양의 상관이 없다** (Spearman −0.30) · 랩 표준 1.64 로 나누면 F · H · K · N 이 1 을 넘는다 · S 의 l_SE 200 µm 는 3.8 g cm⁻³ (불가능).  겉보기 분리막 σ = l_SE/R0 = **0.89–2.81 mS cm⁻¹** (20 셀 · 10 그룹 · 중앙 1.41 · 2 번째 충전 R0) — ⇒ **두께 기록은 밀도 측정이 아니다** (상태 · 방법 미기재) · σ 띠는 우리 σ₀ 보고 기준 1.5 를 품는다 (§3-9) | [원자료] MOESM6 · SI 표 2–20 · 22 · [카드 산술] |
| ⑥ 압력 · 탈압 · 기공 · 소성 | 압력별 기공 **없음** · 탈압 회복 **없음** (*"compression profiles, including how fast the pressure is applied and released … was not monitored in this study but is expected to have an effect on the microstructure"*, p.1312 · Table 1 이 보고 항목으로 권고) · 압축 뒤 *"pressure relaxation"* 은 OCV 에 영향을 줄 수 있다는 한 문장 (p.1312 · ref [22]) · SE 치밀화엔 *">300 MPa"* + *"several hours"* 가 필요하고 NMC 2 차 입자는 그 압력에서 깨지기 쉽다는 인용 문장 (p.1311 · [13–15]) | [인쇄] p.1311–1312 · p.1316 |
| ⑦ DEM · 계산 | **없음** (DEM · discrete · simulation 낱말 0 회) · 모델 · 입자 계산 없음 | 전수 |

⛔ **한정어 (떼지 말 것)**: ① 이 논문의 흩어짐은 **조립을 일부러 풀어 둔** 설계의 결과다 — "같은 절차" 는 전기화학 절차뿐이다 ② 21 그룹 중 자료 · 그림의 그룹 문자는 19 개 · 0.1 C 해석 33 셀 · 사전처리 (0.05 C) 자료는 "11 그룹 · 23 셀" (p.1312 · [원자료] 그림 2b 의 23 셀은 **9 그룹** — 11 은 OCV 이상 셀만 낸 A · F 를 센 수) ③ 성능 ↔ 처리 변수의 인과는 측정되지 않았다 (적층압 ↔ 유지율의 동행 · OCV · 분극 ↔ 성능의 동행만) ④ 펠릿 · 분리막의 밀도는 저자가 내지 않았다 — 카드가 질량 · 두께 · 지름으로 계산한 **겉보기** 값이고 두께를 잰 상태 (가압 중 / 하중 뺀 뒤 / 셀 안 / 밖) · 방법은 [미확인] ⑤ 재료: 단결정 NMC 622 (EDX Ni : Mn : Co = 60.3 : 20.0 : 19.7 at%) · Li₆PS₅Cl (MSE · Li₂S 반사 있음 · SI 그림 44) · In–Li 음극 · 25 °C 근처 — 우리 (NCM811 · 다른 LPSCl · 300 MPa 침대) 와 다르다.
⇒ **절대값 전이: 성능 수치 0 건.**  전이되는 것은 **실험 쪽 흩어짐의 크기** (같은 재료라도 첫 용량 ×7 · 중앙 대비 오차 최대 77 %) · **보고 · 통계 규칙** (세 벌 · 실패 수 · OCV · 압력 이력) · **σ₀ 의 실험실 간 띠** (겉보기 분리막 0.9–2.8 mS cm⁻¹ · 펠릿 1.63–1.85) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-84 의 '왜' 칸)

의도 원문: *"실험과의 대조 · 결과 전 대조 항목 — 여러 연구실이 같은 재료 · 같은 절차로도 조립 조건 (적층압 등) 때문에 크게 흩어졌다는 2 차 서술 (연구실 수 등 숫자는 카드가 '원전 확인 전 인용 금지') · 셀 재현성 기준 (n ≥ 2 평균의 해석)"* (가리킨 카드 = `alharbi2026_coupled_design_ultrathin_composite_se_review` L164 · L466 · `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` L404)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "여러 연구실이 … 크게 흩어졌다" | **채움** | p.1310 초록 *"The results show large variability in assembly and electrochemical performance"* · p.1316 결론 *"the differences in cycling behaviour, specific capacities and voltages between cells prepared by different groups are huge"* · 0.1 C 첫 방전 21–143 mAh g⁻¹ (p.1312 · 33 셀 · 25 °C 근처 (그룹 L · Q · R 은 23–26 °C · U 30 °C) · 운전 적층압 각자) · 그룹 평균 28.3–142.4 · 중앙 대비 오차 1.4–76.8 % [원자료 그림 4a] |
| "같은 재료" | **채움** | 조정 그룹이 같은 로트를 보냈다: 그룹마다 LPSCl 250 mg + NMC 622 100 mg + In 박 3 장 (⌀12 mm · 한 그룹 16 mm) · Ar 포장 (p.1316) · **Li 금속은 각자** (p.1316) |
| "같은 절차로도" | **일부** | 같은 것 = **전기화학 절차** (OCV · PEIS · 0.05 C 2 회 · 0.1 C 50 회 · 3.0–4.3 V vs Li⁺/Li · 200 mAh g⁻¹ 기준 · p.1317) 와 처방 (70 : 30 · 10 mg cm⁻² · 75 mg cm⁻²) · **조립 절차는 일부러 각자** (*"Each group was asked to use their own cell assembly protocol but follow a specific electrochemical protocol"*, p.1310) |
| "조립 조건 (적층압 등) 때문에" | **일부** | 조립 조건의 차이는 표로 실렸다 (SI 표 1 · 그림 1b · 1c) — 그러나 원문은 **흩어짐 전체를 적층압으로 돌리지 않는다**: 처리 변수 ↔ 성능의 뚜렷한 경향 없음 (p.1315) · 적층압 < 40 MPa ↔ 낮은 유지율 (p.1315 · 그림 3d–f) 이지 첫 용량과는 상관 없음 · 첫 용량의 흩어짐은 조립 처리 (혼합 · 분포 · 무게 오차 · 경험) 로 추정 (p.1313) · R0 는 조립 최대 압력과 함께 준다 (SI 그림 9A · 최선 셀에서 가장 뚜렷) · In 비 60–75 at% 가 최적 (그림 3a–c) |
| "(연구실 수 등 숫자는 원전 확인 전 인용 금지)" | **채움 (확인됨)** | **21** = p.1310 초록 · p.1311 *"dataset contributed by 21 groups"* · p.1316 *"sent to 21 different groups"* — 단위는 **연구 그룹** (기관이 아님) · 그림 · 표의 그룹 문자는 19 개 (C · I 없음 · 이유 [미확인]) · 시도 68 · 완주 39 · 실패 29 (43 %) [인쇄 p.1312 · p.1316] |
| "셀 재현성 기준 (n ≥ 2 평균의 해석)" | **채움 (한정 셋)** | 원문 권고 = **세 벌 평균 + 오차 범위** (p.1316) · 두 셀 그룹 SD 평균 10.0 ↔ 세 셀 7.0 mAh g⁻¹ (p.1315) · RME 10 % 안의 네 그룹 (S · M · Q · B) 모두 ≥ 2 셀 (p.1315).  한정: ① SD = 모집단 식 (n = 2 이면 차의 절반) ② 중앙 SD 는 4.58 ↔ 4.49 로 같다 ③ 10.0 ↔ 7.0 은 OCV 이상 셀을 넣은 값 (빼면 7.2 ↔ 5.9 · 50 사이클 4.3 ↔ 5.0) [카드 산술 · §3-6] — "**셀이 늘면 SD 가 준다**" 는 문장은 SD 자체가 아니라 평균의 표준오차 (SD/√n) 에 맞는 말이다 [카드 해석] |
| "→ 실험과의 대조 · 결과 전 대조 항목" | **일부** | 셀 성능 값은 우리 계산 출력이 아니다 · 쓸 수 있는 것 = σ₀ 띠 (펠릿 1.63–1.85 · 분리막 겉보기 0.9–2.8 mS cm⁻¹) · 실험 앵커 등록 칸 (Table 1) · 흩어짐의 크기 (§8) |

**가리킨 카드 · 같은 원전을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `alharbi2026_…` L164 | *"다기관 재현성 \| **21 개 연구실** · 같은 재료 · 같은 시험 절차 → 조립 조건 (적층압 · 음극 조성 등) 때문에 'immense spread' \| [2차 · ref 110] \| p.25"* | 21 ✓ (단위 = research groups) · 같은 재료 ✓ · 같은 **시험** 절차 ✓ (전기화학) · 조립 변수 목록 ✓ (*"processing pressures, pressing durations and In-to-Li ratios"*) · 'immense' 는 원문 낱말이 아니다 (원문 *"huge"* · *"large variability"*) · "때문에" = 원문은 인과를 세우지 않는다 | **일부** — 수 · 재료 · 절차 맞음 · 인과 (적층압 → 흩어짐) 는 원문보다 강하다 |
| `alharbi2026_…` L466 | *"[110] 'Benchmarking …', Nat. Energy 9, 1310–1320 (2024) \| 21 기관 재현성 — 조립 편차 (적층압) 의 크기"* | 서지 ✓ · 21 ✓ (기관 → 그룹) · "조립 편차 (적층압) 의 크기" = 적층압이 정량된 것은 유지율 (D · F · G) 뿐 | **일부** (단위 · 인과 범위) |
| `alharbi2026_…` L332 | *"[110] 의 저자가 'Zeier, W. G. & Vargas-Barbosa, N. M.' 두 사람으로만 … (교신저자만 남긴 것으로 보인다)"* | 저자 55 명 · 제1 저자 Puls · 마지막 둘 = Zeier · Vargas-Barbosa · **교신은 Vargas-Barbosa 한 사람** (p.1310 · p.1319) | **일부** — 리뷰가 마지막 두 저자만 남긴 것은 맞다 · "교신저자만" 은 원문과 다르다 (Zeier 는 교신 아님) |
| `alharbi2026_…` L386 | *"적층압 … 조립 변수로서 재현성을 지배 [110]"* | p.1315 *"clear trends between the processing parameters and the electrochemical cell performance are not evident"* · 적층압 ↔ 유지율 (첫 용량과는 무관) | **일부 (과장)** |
| `alharbi2026_…` L482 (인용 초안) | *"A shared test protocol does not remove the spread caused by cell assembly, in particular the applied stack pressure [Nat. Energy 9, 1310 (2024)]."* | 앞 절반 ✓ · "in particular the applied stack pressure" = 흩어짐의 주원인으로 적층압을 꼽은 문장은 원문에 없다 | **일부** — 원전 확인판 문장 = §10 |
| `alharbi2026_…` L243 · L266 | "*Standardizing how a cell is tested did not standardize how a cell is built*" (리뷰 문장) · "[110] 황화물 계 [추정]" | 리뷰 자신의 문장 (원문에 없음 — 리뷰 인용으로만) · 황화물 계 ✓ (Li₆PS₅Cl · 이제 원문 확인) | **채움** (리뷰 문장 표지 유지) |
| `schmitt2026_…` L404 | *"S. Puls, et al., Benchmarking the reproducibility of all-solid-state battery cell performance, Nat Energy 9 (2024) 1310–1320. \| 카드 없음 — 셀 재현성 기준 (n ≥ 2 평균의 해석)"* | 서지 ✓ · 원문 기준 = **세 벌** — 원문은 특히 *"when discussing the effect of low-content (in)active additives (for example, polymer electrolytes, binder and so on)"* 세 벌이 표준이 되어야 한다고 적는다 (p.1316) · 그 카드 L38 · L122 의 *"Data are averaged from at least two identical cells"* (결착제 건식 시트) 는 이 기준보다 한 벌 적다 | **채움** (서지) · 기준 대조는 §8 · §9 |
| `kissel2025_…` L63 · L336 | *"실험실마다 (round robin [26])"* · *"[26] S. Puls, E. Nazmutdinova, F. Kalyk, … et al., Nat. Energy 2024, 9, 1310."* | 저자 순서 ✓ · 권 · 쪽 ✓ | **채움** |

⇒ **의도 대조 결과: 일부** — "21 그룹 · 같은 재료 · 같은 전기화학 절차 → 큰 흩어짐" 과 "세 벌 평균 · 오차 보고" 기준은 **채움**; "같은 절차" 는 전기화학 절차에 한정되고 (조립은 일부러 각자), "조립 조건 (적층압 등) 때문에" 는 **일부** (원문은 적층압 → 유지율의 동행만 보이고 처리 변수 ↔ 성능의 뚜렷한 경향은 없다고 적는다); "n ≥ 2 평균" 은 원문 기준 (세 벌) 보다 약하고, 원문의 "두 셀 10.0 → 세 셀 7.0" 은 SD 식 · 이상 셀 포함 · 중앙값으로 보면 흔들린다 (§3-6).

---

## 1. 한 줄 요약
NMC 622 (단결정) · Li₆PS₅Cl · In 박을 21 개 연구 그룹에 보내 같은 처방 · 같은 전기화학 절차로 **각자 조립한** 펠릿 셀의 성능을 모아 보니, 조립 압력 · 시간 · 셀 틀 · In : Li 비가 그룹마다 크게 다르고 (분리막 hand-pressed–720 MPa · 압축 0.02–10 분 · 적층압 1–400 MPa), 셀의 43 % 가 50 사이클 전에 실패했으며 (대부분 조립 단계), 0.1 C 첫 방전은 21–143 mAh g⁻¹ 로 흩어졌다.
처리 변수와 성능의 뚜렷한 경향은 없고, 성공 셀의 공통점은 (원문) 분리막 R0 18–42 Ω cm² (원자료와 어긋남 · §3-5) · 양극 300–590 MPa 1–5 분 · 적층압 > 40 MPa · OCV > 2.5 V · 초기 분극 0.10–0.25 V 이다.
저자 결론: *"publications reporting cycling data should not only report the data of one battery but at least the average and error ranges of triplicates"* · 실패 셀 수 · 압력 · 시간 · 압력 이력 · 적층압 제어 · In : Li 비 · CAM 로딩 · 초기 OCV · 휴지 시간을 늘 같이 적으라 (Table 1 · p.1316).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| S. Puls · E. Nazmutdinova · F. Kalyk · … (55 명) · W. G. Zeier · **N. M. Vargas-Barbosa\*** (조정 = Münster · FZ Jülich IMD-4 · Bayreuth) | Nature Energy 9 (October 2024) 1310–1320 · Analysis · CC BY 4.0 | 10.1038/s41560-024-01634-3 | **Li₆PS₅Cl** (MSE Supplies · 99.99 % · Mesh 325 · D50 ≈1 µm) + **단결정 NMC 622** (MSE Supplies) · In 박 (MaTecK 99.999 % · 100 µm) + 각자의 Li · 무첨가 (탄소 · 결착제 없음) | 실험 — 21 그룹 실험실 간 연구 (셀 조립 · 전기화학 · PEIS) + 조정 그룹의 재료 시험 (XRD · SEM · EDX · LPSCl PEIS · 액체 LIB 기준 셀) · 데이터 분석 (조정 그룹 · DRT = Bayreuth Danzer 랩) |

- **1저자 메모 (후보 표 행) 와의 대조**: "S. Puls, et al., … Nat Energy 9 (2024) 1310–1320" — **같다**.  덧붙임 ① 기사 종류 = **Analysis** ② 저자 55 명 · 교신 = Vargas-Barbosa 한 사람 ③ 호수는 PDF 에 인쇄되지 않았다 (October 2024) ④ 출판 2024-09-18 (온라인).
- **글의 꼴**: 초록 → 서론 → 조립 조건의 흩어짐 (그림 1) → 초기 OCV 의 흩어짐 (그림 2a) → 사이클 성능의 흩어짐 (그림 2b–d) → 처리 변수 ↔ 성능 상관 (그림 3) → 셀 재현성 · Ragone (그림 4) → 결론 (Table 1) → 방법 (재료 · XRD · SEM · PEIS · 액체 기준 셀 · 조립 처방 · 사이클 처방 · 자료 처리 식 (1)–(6) · 외삽 Ragone · 임피던스 처리 식 (7)) · 참고문헌 38.  그림 4 · 표 1 · 번호 식 7 / SI: 표 S1–S26 · 그림 S1–S47 · Source Data 6 개.
- **참여 그룹과 우리 정본 카드의 저자 (그룹 문자와의 짝은 원문이 밝히지 않는다 — 문자는 익명)**: Min-Gi Jeong · Kelsey B. Hatzell (`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`) · Philip Minnmann · Jürgen Janek (`minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2024_microstructure_porosity_visualization`) · Eva Schlautmann · Wolfgang G. Zeier (`schlautmann2023_se_particle_size_composite_transport`) · Vanessa Miß · Bernhard Roling (`miss2026_*`) · Saneyuki Ohno (`ohno2020_interlab_ionic_conductivity_argyrodite`) · Hubert Gasteiger · Bairav S. Vishnugopi · Partha P. Mukherjee · Claire Villevieille · Adrien Fauchier-Magnan (Perrenot 계열 [14] · [15]).  ⚠ "그룹 X = 저자 Y 의 랩" 으로 읽지 않는다.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 처방 (p.1311 · p.1316–1317 · SI 표 24 · 그림 S44–S46 · `txt_p2_protocol_21_groups_70_30_10mg_70mg_own_assembly.png` · `txt_p7_methods_materials_mse_d50_1um_sc_nmc622.png` · `txt_p8_assembly_spec_75mg_300_400um_cycling_protocol.png` · `tab_S24.png` · `fig_S44.png`–`fig_S46.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | Li₆PS₅Cl · MSE Supplies · 99.99 % · Mesh 325 · **D50 ≈1 µm** · 받은 그대로 보냄 · XRD 에 **Li₂S 반사 (\*)** | [인쇄] p.1316 · SI 그림 44 |
| CAM | **단결정** LiNi₀.₆Mn₀.₂Co₀.₂O₂ (MSE Supplies) · 150 °C 24 h 진공 건조 뒤 발송 · EDX 12 점 **Ni 60.3 ± 0.5 · Mn 20.0 ± 0.4 · Co 19.7 ± 0.3 at%** · 코팅 [미확인 · 언급 없음] | [인쇄] p.1316 · SI 표 24 |
| SEM | LPSCl: ≈0.5–1 µm 입자가 뭉친 수–수십 µm 덩이 + 각진 큰 조각 (≈5–10 µm) 섞임 · NMC 622: ≈1–5 µm 의 둥글거나 각진 단결정 (작은 덩이 일부) [판독 · 눈금 막대 20 · 4 µm 대비 픽셀 · 정량 입도 아님] | SI 그림 45 · 46 |
| 음극 | In 박 (MaTecK 99.999 % · 100 µm · 40 °C 24 h 진공) + **각 그룹의 Li** → In/(InLi)ₓ (x ≈0.3 · 두께 ≈100 µm) | [인쇄] p.1316–1317 |
| 발송량 | 그룹마다 LPSCl **250 mg** + NMC 622 **100 mg** + In 박 3 장 (⌀12 mm · 한 그룹 16 mm) · Ar (O₂ < 1.0 · H₂O < 0.5 ppm) — 셀 3–4 개 분 | [인쇄] p.1316 · p.1312 |
| 양극 처방 | m(CAM) : m(SE) = **70 : 30** · 무첨가 · 막자 **최대 15 분** · CAM 로딩 **10 mg cm⁻²** | [인쇄] p.1311 · p.1317 |
| 분리막 처방 | 순수 LPSCl **≈70 mg cm⁻²** (p.1311) ↔ 방법 **75 mg cm⁻² · 두께 300–400 µm** (p.1317) ↔ 서론 *"about 500 µm thick"* (p.1310 · p.1316).  [카드 산술] 75 mg cm⁻² 로 300–400 µm 가 되려면 겉보기 밀도 **1.88–2.50 g cm⁻³** = 저자 이론 밀도 1.87 이상 — 처방 두께는 이 질량으로 닿을 수 없다 · 실제 기록 l_SE 는 420–543 µm (S 200 µm 제외) | [인쇄] · [카드 산술] |
| 전기화학 절차 | OCV + PEIS (7 MHz–100 mHz · 10 mV · 10 점/decade) → 대칭 정전류 · 이론 200 mAh g⁻¹ · **3.0–4.3 V vs Li⁺/Li** (0 V vs Li⁺/(In-InLi) = 0.62 V vs Li⁺/Li) · 0.05 C 2 회 (충전 · 방전 뒤 1 h OCV + PEIS) → **0.1 C 50 회** (단계 사이 5 분) → 충 · 방전 상태 PEIS | [인쇄] p.1317 |
| 액체 기준 셀 (조정 그룹) | NMC 622 : PVdF : C65 = 94 : 3 : 3 · CAM 6 mg cm⁻² · CR2032 · Li · 1 M LiPF₆ EC : EMC 3 : 7 · 같은 절차 (PEIS 없음) · n = 3 | [인쇄] p.1317 |

### 3-2. ★ 조립 조건의 흩어짐 (그림 1 · SI 표 1 · `fig_1.png` · `tab_S1.png` · `txt_p2_pressures_10_70_250_520_durations_300mpa_nmc_breaking.png` · `txt_p2_p3_thickness_similar_compression_profile_not_monitored.png`)
- 단계 (그림 1a): ① 분리막 압축 p₁ t₁ ② 그 위에 양극 분말을 펴고 함께 압축 p₂ t₂ ③ 반대편에 합금 음극을 놓고 전체 압축 p₃ t₃ ④ 운전 적층압 p₄ 고정.
- 본문 요약: 운전 적층압 *"mostly in the range of 10–70 MPa"* · 양극 압축 *"range from 250–520 MPa"* · 압축 시간은 *"several orders of magnitude"* 차이 (p.1311).  [원자료] 실제 범위 = 양극 압력 **50 (G) – 720 MPa (P)** · 적층압 **1 (G) – 400 MPa (Q)** · 휴지 (조립 → OCV) **0.17–24 h** — 본문 범위는 '대부분' 의 말이다.
- 같은 문단의 인용 문장: *"high pressure (>300 MPa) and long compression times (in the order of several hours) are required to densify and reduce residual void space in thiophosphate-based SEs that enable higher ionic conductivities. However, NMC (secondary) particles are prone to breaking at such pressures, especially when compressed for extended periods of time"* (p.1311 · refs [13–15]).
- 두께: *"the reported thicknesses of all cells are similar (Supplementary Tables 2–20), showing again that the processing protocol mostly plays a role in the resulting microstructure"* · 압력 이력 (올리고 내리는 속도 · 제어) 은 *"not monitored"* (p.1311–1312).

[인쇄 SI 표 1 + 원자료 MOESM2 · MOESM5 — 그룹 19 개]
| 그룹 | ⌀ mm | p₁ / t₁ (MPa / 분) | p₂ / t₂ | p₃ / t₃ | p₄ 적층 MPa · 제어 | T °C | OCV 까지 h | 0.1 C 첫 방전 그룹 평균 (셀 수 · RSD %) | 50 번째 |
|---|---|---|---|---|---|---|---|---|---|
| A | 10 | 100 / 0.02 | 370 / 3 | 100 / 0.02 | 70 · N | 25 | 12 | 40.4 (2 · 18.9) — OCV 이상 | 74.7 |
| B | 10 | hand-pressed / – | 380 / 3 | – | 50 · N | 25 | 5 | **126.0 (3 · 0.33)** ★ | 124.4 |
| D | 10 | 300 / – (원자료 0) | 350 / 2 | 10 / 0 | – (원자료 0.01 · 그림 3 원자료 0) · N | 25 | 0.5 | 105.7 (3 · 20.9) | 38.3 |
| E | 10 | 127 / 1 | 304 / 5 | 50 / 1 | 50 · N | 25 | 1.67 / 0.83 | 39.8 (2 · 48.1) | 27.5 |
| F | 9.5 | 350 / 5 | 350 / 5 | 25 / 5 | 10 · N | 25 | 12 | 107.3 (2 · 30.1) — OCV 이상 | 53.9 |
| G | 5 | 50 / 1 | 50 / 1 | 400 / 5 | 1 · N | 25 | 0.5 | 80.5 (3 · 17.0) — G3 OCV 이상 | 9.2 |
| H | 10 | 70 / 1 | 300 / 3 | hand-pressed / – | 60 · N | 25 | 0.17 | **142.4 (2 · 0.53)** ★ | 141.6 |
| J | 10 | 460 / 3.5 | 400 / 3.5 | 100 / 2 | 60 · **Y** | 25 | 3 | 66.8 (1) — 창 틀림 · 통계 제외 | 61.3 |
| K | 10 | 62 / 1 | 434 / 3 | – (원자료 0) | 81 · N | 25 | 0.25 | 134.9 (3 · 1.13) ★ K2 | 113.8 |
| L | 10 | 370 / 1 | 370 / 1 | 150 / 0.5 | 75 · N | 23–26 | 0.2 | 108.2 (1) | 105.6 |
| M | 7 | 255 / 10 | 255 / 10 | 50 / 0.05 | 50 · N | 25 | 2 | 124.7 (3 · 4.29) | 99.2 |
| N | 10 | 395 / 3 | 395 / 3 | 55 / – | 55 · N | 25 | 3 | 48.6 (1 · 0.072 C) | 44.2 |
| O | 8 | **590** / 5 | **590** / 5 | 195 / 5 | 40 · **Y** | 25 | 2 | 135.4 (3 · 1.21) ★ | 126.3 |
| P | 10 | **720** / 3 | **720** / 3 | 36 / 2 | 50 · **Y** | 25 | 24 | 용량 자료 없음 (임피던스만) | – |
| Q | 7 | 380 / 1 | 510 / 1 | 400 / – | **400** · N | 23–25 | 0.5 | 125.9 (2 · 3.16) ★ Q1 | 117.2 |
| R | 10 | 98 / 1 | 395 / 1 | 68 / – | 68 · **Y** | 24–26 | 4.25 / 6.5 / 0.3 | 71.8 (3 · 6.26) | 72.1 |
| S | 10 | 100 / 1 | 380 / 3 | – | 50 · N | 25 | 0.5 | 120.2 (2 · 1.59) ★ | 126.7 |
| T | 13 | 25 / 0.5 | – | 360 / 1 | 25 · N | 25 | 0.5 | 28.3 (2 · 16.2) | 18.1 |
| U | 13 | 72 / 1 | 370 / 3 | 40 / 3 | 70 · N | 30 | 6 | 83.3 (1) | 77.7 |

(★ = 최선 셀이 있는 그룹 · RSD = 모집단 SD / 평균 · 원자료 그림 4a · 4b 시트 · 그룹 셀 수 = "Amount of cells working")

- [원자료 MOESM6] 글러브박스에 용매를 두는 그룹 (Y · 모두 용매 필터 있음 — SI 표 1 각주) = **5** (B · N · O · R · T) · H₂O < 0.1 – < 3 ppm (B 는 1.3) · O₂ < 0.1 – < 5 ppm — 저자: 모든 그룹이 H₂O/O₂ < 5 ppm 이라 성능과의 직접 상관은 안 보인다 (p.1313).

### 3-3. 실패 · 초기 OCV (그림 1d · 2a · `txt_p3_failures_68_attempted_39_working_21_preparation.png` · `txt_p3_ocv_2p6_outliers_in_li_ratio_1p33_6p61.png` · SI 표 21)
- **실패**: 시도 **68** · 50 사이클 완주 **39 (57 %)** · 조립 실패 **21 (31 %)** (깨진 펠릿 · 양극의 불균일 분포 · 글러브박스 수분) · 사이클 중 실패 **5 (7 %)** (단락 등) · 기타 (사람 실수 · 플러그 뽑힘) **3 (< 5 % · 원자료 4.41 %)** → 실패율 **43 %** (p.1312 · p.1316) · *"The number of non-working cells is generally not reported in the literature"* · *"once a cell attains some initial capacity, cycling it up to 50 cycles is not very problematic"*.
- **OCV 환산**: E(Li⁺/Li) = E(Li⁺/In-(InLi)ₓ) + 0.62 V [21] · 액체 기준 셀 OCV 2.8 ± 0.2 V (조립 직후 · n = 3) → 5 h 뒤 3.0 ± 0.1 V (원자료 2.967 ± 0.135) · ASSB 대부분은 액체 셀 직후 범위 (2.64–3.02 V) 의 아래 끝.
- **이상 셀 5 개** (낮은 OCV): A1 · A2 (1.803 · 1.845) · F1 · F2 (2.122 · 1.822) · G3 (2.209) → *"excluded from all further statistical analyses and box plots"* · J1 은 틀린 전위 창 (3.0–4.3 V **vs In/(InLi)ₓ** = 3.62–4.92 V vs Li⁺/Li) 이라 모든 통계에서 제외 · 나머지 평균 OCV **2.6 ± 0.1 V** ([카드 산술 · 원자료] 34 셀 2.564 ± 0.107 ✓).
- **In : Li 원자비** 1.33 : 1–6.61 : 1 (N 0.77 : 1) · 중앙 2.48 : 1 → N 만 두 상 (In + InLi) 영역 밖에서 시작 (N 의 첫 0.1 C 방전 48.6 mAh g⁻¹ · N 은 0.072 C 로 돌림) · [인쇄 SI 표 21] A 1.21 · P 0.66 (통계 밖 그룹) · L · U 무게 미보고.
- [원자료] 그림 2a 의 n = 39 셀 = 이상 셀 5 개를 포함하고 J1 · P1 을 빼며 Q3 (OCV 만 · 용량 없음) 를 넣는다 — 그림 1d 의 'working 39' 와 같은 집합인지 원문에서 가를 수 없다.

### 3-4. ★ 전기화학 성능의 흩어짐 (그림 2b–d · SI 표 23 · SI 그림 1–7 · 28 · `fig_2.png` · `tab_S23.png` · `txt_p3_p4_capacity_0p1c_21_143_median_121p9_bimodal.png` · `txt_p4_retention_cycling_pressure_25mpa_mixing_weighing.png`)
| 지표 (n) | 중앙 | 평균 | 상자 (IQR) | 수염 | 액체 기준 (n = 3) | 표지 |
|---|---|---|---|---|---|---|
| OCV V vs Li (39 · 이상 셀 포함) | 2.54 | 2.49 | 2.47–2.63 | 2.29–2.79 | 2.97 (5 h) | [인쇄 SI 표 23] |
| 사전처리 충전 0.05 C mAh g⁻¹ (23) | 179.3 | 160.6 | 127.0–188.5 | 71.2–194.6 | 197.8 ± 0.9 | 〃 · [원자료] |
| 사전처리 방전 0.05 C (23) | 137.2 | 122.6 | 95.3–144.5 | 46.6–152.9 | 174.8 ± 0.6 | 〃 |
| 0.1 C 첫 방전 (33) | **121.9** | **103.7** | 75.8–132.1 | 20.7–143.1 | 169.1 ± 0.8 | 〃 |
| 0.1 C 50 번째 방전 (33) | 105.6 | 86.0 | 44.2–125.3 | 12.7–145.9 | 166.8 ± 0.5 | 〃 |
| 유지율 % (33) | **91.6** | **81.1** | 76.1–97.6 | 49.5–107.0 | [카드 산술] 98.6 | 〃 |
| CE 사전처리 % (23) | 77.0 | 75.7 | 75.4–78.1 | 73.8–80.6 | 88.4 | 〃 |
| CE 50 번째 % (33) | 99.8 | 98.6 | 99.3–100.1 | 99.0–100.7 | 99.7 | 〃 |
| 분극 ΔV V 1 번째 (30 · D 전압 없음) | 0.20 | 0.25 | 0.15–0.24 | 0.13–0.33 | 0.057 | 〃 |
| 분극 ΔV 50 번째 (30) | 0.23 | 0.29 | 0.20–0.30 | 0.13–0.43 | 0.047 | 〃 |

- 본문 해석: 평균 ≠ 중앙 = 정규분포가 아니다 · 0.1 C 첫 방전은 **두 봉우리** (110–145 ↔ 60–80) · 0.1 C 는 둘째 0.05 C 보다 평균 ≈16 mAh g⁻¹ 낮다 (LPSCl 셀의 율속 한계 [10,24]) · 50 사이클 뒤 평균 · 중앙이 18 · 16 mAh g⁻¹ 준다 · 유지율 > 100 % 다섯 셀 (H1 · R1 · R3 · S1 · S2 · 최대 107 %) · D · F · G 의 유지율 < 50 % 와 적층압 1–10 MPa → *">25 MPa are required for stable cycling in these types of cells"* (p.1313) · 첫 CE > 75 % (네 셀 제외 [카드 확인: E1 · E2 · T1 · T2]) · 분극 중앙 +30 mV · 평균 +40 mV (p.1314).
- [카드 산술 · 원자료 대조] 본문 퍼센트 둘은 Source Data 로 재현되지 않는다: *"most cells (59%) … 170–195 … 130–155 mAh g⁻¹"* (p.1312) ↔ 23 셀 중 충전 15 (65 %) · 방전 16 (70 %) · *"Most of the ASSB (69%) have low initial polarization voltages between 0.10 V and 0.25 V"* (p.1314) ↔ 30 셀 중 23 (77 %) — 둘 다 OCV 이상 셀 · J1 까지 넣어 세면 맞는다: 59 % = 방전 16/27 (충전은 15/27 = 56 %) · 69 % = 25/36 (A1 · A2 · F1 · F2 · G3 · J1 를 더함 · F2 0.210 · G3 0.22 V 가 띠 안) [카드 산술 · 그렇게 셌다는 말은 원문에 없다 · 같은 문단은 *"the number n of cells considered for this statistic is 30"*].  F1 의 유지율은 53.9 % (< 50 % 문장의 반례 · F2 48.2 %).
- 결론 문장의 첫 방전 범위 *"23.7 mAh g⁻¹ and 143.1"* (p.1316) ↔ 본문 *"21 to 143"* (p.1312) — 최소값 20.68 (E1) 과 23.71 (T1) 중 어느 것인지가 다르다 [원자료].
- 액체 기준 셀 (SI 그림 28): 0.1 C 50 사이클 169 → 167 mAh g⁻¹ · CE ≈99.7 % · 분극 ≈0.04–0.05 V — ASSB 최고 방전은 액체보다 ≈20 mAh g⁻¹ 낮다 (사전처리 방전 152.9 ↔ 174.8 · p.1312).

### 3-5. 최선 셀과 상관 (그림 3 · SI 그림 7–9 · `fig_3.png` · `fig_S9.png` · `txt_p5_best_performers_120mahg_four_commonalities.png` · `txt_p6_cycling_pressure_40mpa_r0_vs_max_pressure.png` · `txt_p6_ocv_2p5_polarization_rtot_correlation.png`)
- **최선 셀** = 50 사이클 뒤 > 120 mAh g⁻¹ — **12 셀 · 6 그룹**: B1–B3 · H1–H2 · K2 · O1–O3 · Q1 · S1–S2 · 공통: OCV > 2.5 V · 초기 분극 0.10–0.25 V · 유지율 > 85 % (p.1314).  [원자료] S2 OCV 2.493 · K 2.500 (경계).
- **네 공통점** (p.1314): ① 분리막 R0 **18–42 Ω cm²** (분리막 압력은 B 의 손 누름 ~ O 의 590 MPa) ② 분리막 + 양극을 **300–590 MPa · 1–5 분** 압축 ③ 전체 셀 압축은 6 그룹 중 4 그룹이 안 했다 ④ 적층압 > 40 MPa (*"showing a bias towards good cell performance and not necessarily transferability of the results to application-oriented ASSB cells"*).  ⚠ [원자료 SI 표 22] H1 · H2 의 R0 = 48.5–50.6 Ω cm² (1 · 2 번째 충전) — 인쇄 범위 18–42 밖 · B 는 임피던스 자료 없음.
- 저자 결론: *"the reproducible preparation of the positive electrode composite is decisive for good cell performance"* — 재료 보관 · 혼합 질 · 분리막 위 분포 · 압력 이력 (p.1314).
- **상관 (그림 3)**: In 60–75 at% 에서 용량 · 유지율 최적 (그림 3a–c · 최선 셀 셋이 > 85 at% — 합금 조립 방향 (In · Li 중 어느 쪽이 분리막을 보는지) 차이로 추정 · 미보고) · 적층압 < 40 MPa = 낮은 유지율 · **첫 용량과 R_tot 는 적층압과 무관** (그림 3d–f · 120–350 MPa 축 끊김 · Q 400 MPa) · OCV ≥ 2.5 V 에서 높은 용량 · 유지율 · 낮은 저항 (그림 3g–i) · 초기 분극 < 0.2 V 에 좋은 셀 군집 · R_tot ↔ 분극 강한 선형 (그림 3j–l · 51 사이클까지 · SI 그림 9B · C).
- **R0 ↔ 조립 최대 압력 (SI 그림 9A)**: *"a decrease of the separator resistance R0 with increasing maximum pressure is observed, most clearly for the best performers"* (p.1315).  [판독 SI 그림 9A · 눈금 보간] 가로축 200–600 MPa · H ≈49–51 (300) · S ≈32 (380) · K2 ≈29 (434) · Q1 ≈19 (510) · O ≈17–22 (590) — 원자료의 2 번째 충전 R0 와 맞는다 (K2 29.3 · 1 번째 충전 27.8).  [카드 산술 · 원자료 31 셀 · 2 번째 충전 R0 · 최대 압력 = max(p₁, p₂, p₃)] Spearman ρ(R0, p_max) = **−0.61** · 그림 범위 밖 **P1 (720 MPa · R0 51.2 Ω cm²)** 을 빼면 −0.76 (1 번째 충전 R0 로는 −0.63 · −0.78) — 가장 높은 압력의 셀이 그림에 없다.

### 3-6. ★★ 셀 재현성 통계 — "n ≥ 2 평균" 을 어떻게 읽나 (그림 4a · b · SI 그림 1 · 식 RME/RSE · `fig_4.png` · `fig_S1.png` · `eq_00a_rme_rse_relative_errors.png` · `txt_p6_p7_reproducibility_rme_10pct_sd_10_to_7.png`)
- **정의** (p.1315): RME = abs(study median − group average capacity) / study median · RSE = abs(group standard deviation) / group average capacity · 그룹을 RME 순으로 정렬 (*"The RME is a better indicator of how each group compares to the resulting statistics of the study"*).
- **본문 숫자**: RME 10 % 문턱을 넘지 않는 그룹 = 첫 0.1 C 에서 **S · M · Q · B 넷** (셋이 최선 그룹 · 모두 ≥ 2 셀) · RSD < 10 % = B · H · K · O · S · Q · M · R (8 그룹 중 5 가 세 셀) · 50 번째 RSD < 10 % = M · K · Q · B · O · S · A · R · H · T (10 중 5 가 세 셀) · **SD 평균: 두 셀 그룹 10.0 → 세 셀 그룹 7.0 mAh g⁻¹** · *"Statistically, the error ranges become smaller, the more cells are prepared"* (p.1316).
- ★ **[카드 산술 · 원자료 MOESM5 그림 4a · MOESM6 'Stdev and median rel error']**:

| 경우 (0.1 C 첫 방전) | 두 셀 그룹 (n) · SD 평균 / 중앙 | 세 셀 그룹 (n) · SD 평균 / 중앙 |
|---|---|---|
| 원문 그대로 (모집단 SD · ddof 0 · OCV 이상 셀 포함) | 7 · **10.04 / 4.58** (A 7.65 · E 19.14 · F 32.26 · H 0.75 · Q 3.98 · S 1.91 · T 4.58) | 7 · **7.03 / 4.49** (B 0.41 · D 22.05 · G 13.71 · K 1.53 · M 5.35 · O 1.64 · R 4.49) |
| OCV 이상 셀 (A1 · A2 · F1 · F2 · G3) 을 뺌 (본문 p.1312 의 방침) | 6 · 7.23 / 4.28 (G 가 두 셀로) | 6 · 5.91 / 3.07 |
| 표본 SD (ddof 1) · 이상 셀 포함 | 7 · 14.20 / 6.48 | 7 · 8.60 / 5.50 |
| 50 번째 방전 · 이상 셀 포함 / 뺌 | 5.61 / 4.28 (평균) | 5.16 / 4.97 (평균) — **뺀 쪽은 두 셀 < 세 셀** |

  ① 원문 SD 는 **모집단 식** (B 세 값 → 0.4102 · S 두 값 → 차의 절반 1.908 = 원자료 칸과 같다) — n = 2 의 SD 는 두 값 차의 절반이고 표본 SD 의 1/√2 다.  ② 같은 원자료 시트가 **중앙 SD 4.58 ↔ 4.49** 를 함께 적는다 — 줄어든 것은 평균뿐이고, 평균은 큰 SD 그룹 몇 (F 32.3 · D 22.0 · E 19.1 · G 13.7) 이 정한다.  ③ 본문은 OCV 이상 셀을 *"all further statistical analyses"* 에서 뺐다고 적지만 그림 4 · 이 평균에는 A · F 그룹이 들어 있다.  ④ 셀이 늘어 작아지는 것은 **평균의 표준오차** (SD/√n) 다 — 모분산이 같으면 표본분산 (ddof 1) 의 기대값은 n 과 무관하고, 원문 식 (ddof 0) 으로는 기대값이 오히려 세 셀 쪽이 크다 (E[s²] = σ²(n−1)/n → n = 2 는 σ²/2 · n = 3 은 2σ²/3) [카드 산술] ⇒ 10.0 → 7.0 은 'n 이 늘어서' 가 아니라 그룹 구성의 차이다.  원문도 *"due to the large number of failed batteries, some groups in this work reported fewer than the targeted number of three batteries"* (p.1312 · 재료는 그룹당 3–4 셀 분) — 두 셀 그룹 가운데 셋째 셀이 실패한 그룹이 섞여 **선택 효과** 가 있을 수 있다 [카드 해석].
- **⇒ "n ≥ 2 평균" 의 해석 규칙** [카드 해석 · 이 논문 자료로]: 두 셀 평균은 원문 기준 (세 벌) 아래이고, 두 셀 SD (모집단 식이면 차의 절반) 는 흩어짐을 작게 보인다 — 비교 대상과 함께 **셀 수 · SD 식 · 실패 셀 수** 를 적고, 실험실 간 비교에는 **그룹 안 SD (좋은 그룹 0.4–5 mAh g⁻¹ · RSD 0.3–4 %)** 가 아니라 **그룹 사이 흩어짐 (중앙 대비 오차 1.4–76.8 %)** 을 띠로 쓴다.
- SI 그림 1 (그룹별 평균 · RSD): [판독] H 가 '세 셀' 색 (진한 파랑) 으로 칠해졌다 — 원자료는 H 두 셀.

### 3-7. Ragone (그림 4c · d · 식 (5)–(6) · 외삽 질량 식 · `eq_05_specific_energy_e_spec_cell_mass.png` · `eq_06_specific_power_p_spec.png` · `eq_00b_extrapolated_masses_li_lpscl_1p87.png`)
- 셀 무게 = 양극 복합 + 분리막 + In/(InLi)ₓ (케이스 제외) · 첫 0.1 C 방전: 비출력 **2.5–5 W kg⁻¹** · 비에너지 **2.5–31 Wh kg⁻¹** (원자료 2.6–4.9 · 3.0–30.2) — 로딩 10 mg cm⁻² · 0.1 C 가 같아 출력이 비슷하다 (본문 p.1316 의 *"loading of 10 mAh cm⁻²"* 는 단위 오기 · 처방은 10 mg cm⁻²).
- 외삽 (그림 4d): 분리막 30 µm LPSCl + 음극 20 µm Li · m_Li = A_cell × 0.002 cm × 0.534 g cm⁻³ · **m_LPSCl = A_cell × 0.003 cm × 1.87 g cm⁻³** (*"theoretical densities of LPSCl"* — **랩 표준 1.64 와 다른 문헌 값**) · 용량 · 전압 불변 가정 → *"up to 220 Wh kg⁻¹ higher"* ([원자료] 외삽 최대 219.5 Wh kg⁻¹ (H2) · 증가폭 최대 190 Wh kg⁻¹ [카드 산술] — '220 높아진다' 가 아니라 '≈220 까지') · 목표 250–400 Wh kg⁻¹ · 1 C 의 아래 끝 근처.

### 3-8. ★ LPSCl 펠릿 σ_ion (조정 그룹 · SI 표 25 · 26 · 그림 47 · `tab_S25.png` · `tab_S26.png` · `fig_S47.png` · `eq_S01_ionic_conductivity_l_over_r_a.png` · `txt_p8_eis_pellet_380mpa_3min_2000um_60mpa.png`)
| 항목 | 측정 1 | 측정 2 | 표지 |
|---|---|---|---|
| 성형 | 250 mg · ⌀10 mm PEEK · **380 MPa 3 분** | 같음 | [인쇄] p.1317 |
| 질량 · 두께 | 249.5 mg · **2.02 mm** | 250.7 mg · **2.19 mm** | [인쇄] SI 표 26 |
| 측정 | SS 이온 차단 · **틀 압력 60 MPa 아래** · 7 MHz–100 mHz · 10 mV · 온도마다 2 h 평형 · R–CPE 맞춤 · σ = l/(R·A) | 같음 | [인쇄] p.1317 · SI 표 25 |
| σ_ion 10 · 20 · **25** · 30 · 60 °C (mS cm⁻¹) | 0.83 · 1.28 · **1.63** · 2.14 · 7.35 | 0.89 · 1.46 · **1.85** · 2.45 · 8.72 | [인쇄] SI 표 25 |
| Ea | 0.3884 eV | 0.3996 eV | [인쇄] SI 표 26 |
| 겉보기 밀도 m/(πr²·l) | **1.573 g cm⁻³** | **1.458 g cm⁻³** | [카드 산술] |
| ÷ 저자 이론 밀도 1.87 (랩 표준과 다른 문헌 값) | 0.841 (기공 15.9 %) | 0.779 (22.1 %) | [카드 산술] |
| ÷ 랩 표준 1.64 | 0.959 (4.1 %) | 0.889 (11.1 %) | [카드 산술] |

- ⚠ 두께를 잰 상태 (다이 안 · 밖 · 하중 중 · 뺀 뒤) [미확인] · 더 두꺼운 (덜 치밀한) 측정 2 의 σ 가 더 높다 — 두께 측정 오차 또는 시편 차이 [카드 해석] · 두 측정의 σ 차는 13.5 % (25 °C · 1.85/1.63 [카드 산술]).
- σ_ion 1.63–1.85 mS cm⁻¹ (25 °C) = 우리 σ₀ 보고 기준 1.5 mS cm⁻¹ (1저자 10-12) 와 솔버 상수 3.0 (펠릿값 · CL-91) 사이 · 문헌 LPSCl 펠릿 1.0–2.2 띠 안 [우리].

### 3-9. ★ [카드 산술] 같은 분말 · 다른 실험실의 분리막 — 겉보기 밀도 · 겉보기 σ (원자료 MOESM6 · SI 표 2–22 · `tab_S2.png` · `tab_S8.png` · `tab_S14.png` · `tab_S22.png`)
식: 겉보기 밀도 ρ_app = m_SE / (π(d/2)² · l_SE) · 겉보기 분리막 σ_app = l_SE / R0 (R0 = 그룹별 DRT 의 고주파 집중 저항 · 면적 정규화 · 저자 *"the resistance of the separator"* p.1314) · 분리막이 받은 최대 압력 p_max = max(p₁, p₂, p₃).  ⚠ l_SE 의 측정 상태 · 방법 [미확인] · 많은 그룹이 둥근 수 (500 µm) · B 의 두께는 파란 글자 (= 계산 · 가정 값 · SI p.3 *"Provided data is shown in black, calculated or assumed values are shown in blue"*) 라 뺐다 · S 의 l_SE 200 µm 는 ρ 3.82 g cm⁻³ 로 불가능해 뺐다.

| 그룹 | p_max MPa | ρ_app g cm⁻³ (셀별) | ÷ 1.87 | ÷ 1.64 (랩 표준) | σ_app mS cm⁻¹ (2 번째 충전) |
|---|---|---|---|---|---|
| M | 255 | 1.497 · 1.467 · 1.449 | 0.80 · 0.78 · 0.77 | 0.91 · 0.89 · 0.88 | 1.11 · 1.14 · 1.26 |
| H | 300 | 1.690 · 1.694 | 0.90 · 0.91 | **1.03 · 1.03** | 0.92 · 0.89 |
| E | 304 | 1.495 · 1.490 | 0.80 · 0.80 | 0.91 · 0.91 | 1.61 · 2.09 |
| F | 350 | 1.693 · 1.678 | 0.91 · 0.90 | **1.03 · 1.02** | (임피던스 없음) |
| D | 350 | 1.528 (셋 같음) | 0.82 | 0.93 | 0.91 · 0.92 |
| L | 370 | 1.468 | 0.78 | 0.89 | 1.53 |
| A | 370 | 1.497 (둘 같음) | 0.80 | 0.91 | – |
| N | 395 | 1.737 | 0.93 | **1.06** | 0.90 |
| K | 434 | 1.780 · 1.783 · 1.794 | 0.95 · 0.95 · 0.96 | **1.09 · 1.09 · 1.09** | 1.54 · 1.47 · 1.36 |
| J | 460 | 1.447 | 0.77 | 0.88 | – |
| Q | 510 | 1.416 · 1.468 · 1.469 | 0.76 · 0.78 · 0.79 | 0.86 · 0.89 · 0.90 | 2.79 · 2.23 (Q3 임피던스 없음) |
| O | 590 | 1.440 · 1.490 · 1.485 | 0.77 · 0.80 · 0.79 | 0.88 · 0.91 · 0.91 | 2.23 · 2.24 · 2.81 |
| P | 720 | 1.408 | 0.75 | 0.86 | 1.02 |

- **겉보기 밀도**: 27 셀 · 13 그룹 · **1.41–1.79 g cm⁻³ (중앙 1.50)** · p_max 와 Spearman **−0.30** (양의 경향 없음 · 가장 높은 압력 P 720 MPa 가 가장 낮은 1.41) · 1.64 기준으로는 F · H · K · N 이 1 을 넘는다 (기공 음수).  ⇒ 이 두께 기록은 **밀도 측정으로 쓸 수 없다** — 셀 문헌의 '두께 · 질량' 으로 순수 SE 기공을 만들지 않는다 (저자도 *"thicknesses of all cells are similar"* 로만 썼다).
- **겉보기 σ**: 20 셀 · 10 그룹 · **0.89–2.81 mS cm⁻¹ (중앙 1.41 · 2 번째 충전 R0 · 1 번째 충전 R0 로는 0.91–2.79)** · p_max 와 Spearman +0.53 · ρ_app 와 −0.42 (밀도가 높을수록 σ 가 낮게 나온다 — 두께 기록 오차 · R0 에 분리막 밖 저항이 섞임 [카드 해석]) · S (l_SE 200 µm) 를 넣으면 0.62.  조정 그룹 펠릿 1.63 · 1.85 (25 °C · 60 MPa) 와 같은 띠 · **우리 σ₀ 보고 기준 1.5 는 띠 안, 솔버 상수 3.0 은 띠 위** [우리].
- 복합 양극 두께 l_CC (14–180 µm · 같은 로딩) 로 낸 겉보기 밀도는 **0.83–10.4 g cm⁻³** (Q2 10.4 · Q1 6.6 = 불가능) [카드 산술] → 복합 양극 기공은 계산하지 않는다.

### 3-10. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① 압력 이력 (올림 · 내림 속도 · 제어) 을 재지 않았다 (p.1312) ② 낮은 용량 셀의 원인은 *"difficult to ascertain within the present study"* (p.1313) ③ 조사 못 한 것 = 손 막자 혼합의 (불)균일 · 압력 이력이 정하는 미세구조 · 집전체 표면 · 보관 중 열화 · 합금 음극 준비 · O₂ · H₂O · 용매 · 운전 중 압력 · 온도 제어 (p.1316) ④ 적층압 > 40 MPa 는 응용 쪽 0–10 MPa 로 옮겨지지 않는다 (p.1314 · p.1316) ⑤ 셀 무게에 케이스를 넣지 않았다 · 외삽 Ragone 은 용량 · 전압 불변 가정.
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. 연구 그룹 21 ↔ 그림 · 표의 그룹 문자 19 (C · I 없음).
2. 첫 0.1 C 방전 범위 21–143 (p.1312) ↔ 23.7–143.1 (p.1316).
3. 퍼센트 59 % (p.1312) · 69 % (p.1314) ↔ 그림의 셀 집합으로는 65–70 % · 77 % — OCV 이상 셀 · J1 까지 넣어 세면 16/27 · 25/36 으로 맞는다 (§3-4 · 그렇게 셌다는 말은 원문에 없다).
4. 최선 셀 R0 18–42 Ω cm² ↔ H1 · H2 48.5–50.6 (SI 표 22).
5. "유지율 < 50 %" 의 F1 = 53.9 % · "OCV > 2.5 V" 의 S2 = 2.493.
6. 적층압 문턱 *">25 MPa"* (p.1313) ↔ *">40 MPa"* (p.1314 · p.1316).
7. 분리막 처방 ≈70 (p.1311) ↔ 75 mg cm⁻² · 300–400 µm (p.1317 · 그 질량으로 닿을 수 없는 두께) ↔ *"about 500 µm"* (p.1310).
8. 본문 *"loading of 10 mAh cm⁻²"* (p.1316) = 단위 오기 (10 mg cm⁻²) · *"up to 220 Wh kg⁻¹ higher"* = 외삽값이 ≈220 까지 (증가폭 ≤190).
9. OCV 이상 셀을 "모든 통계에서 뺐다" ↔ 그림 4 · SD 평균 10.0 / 7.0 에 A · F 포함.
10. SI 표 9 의 J1 OCV 1.720 (머리글 'vs Li⁺/Li') = vs In/InLi 값 (원자료 2.3398 = 1.720 + 0.62).
11. SI 표 14 의 O 전류 0.0522–0.0559 mA ('I (0.1C)') = 0.05 C 값 (원자료 0.104–0.112 mA = m_CAM × 20 mA g⁻¹).
12. SI 표 22 의 T2 51 번째 '–' ↔ 원자료 R_tot 1327.3 · R0 26.9 Ω cm² (SI 그림 42 는 그 측정을 'defective' 로 표시).
13. D 의 적층압: SI 표 1 · MOESM6 '–' ↔ 그림 1b 원자료 0.01 ↔ 그림 3 원자료 0 MPa.
14. SI 그림 9A 가로축 200–600 MPa — 720 MPa 인 P1 이 빠진다 · SI 그림 1 의 H 색 (세 셀) ↔ 두 셀 · SI 표 26 캡션 *"Error! Reference source not found."* (워드 상호참조 오류).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬 (`eq_01`–`eq_07` · `txt_p9_impedance_validation_truncated_500khz_lambda.png`)
- **조정 그룹**: 재료 구매 · 시험 (XRD Stoe STADI P · Cu Kα · Ge(111) · 10–70° / SEM Zeiss AURIGA 3 kV · 10 nm Au / EDX 12 점 / LPSCl PEIS) · 포장 · 발송 · 원자료 수집 · 사이클 자료 분석 (S.P. · E.N. · F.K. · H.M.W. · J.F.T. · N.M.V.-B.) · 임피던스 분석 = C.P. · M.D. (Bayreuth) · *"The data analysis was performed by the coordinating group to minimize variability sources in the results"* (p.1311 · [12] Gittins 2023 슈퍼커패시터 실험실 간 연구와 같은 방식).
- **각 그룹**: 셀 조립 (각자의 틀 · 압력 · 시간) · 사이클 · 원자료 (시간 · 전압 · 전류 · 사이클 번호) 제출 · 셀별 두께 · 질량 · OCV · 전류 보고 (SI 표 2–20 · 파란 글자 = 조정 그룹이 계산 · 가정).
- **자료 처리 식** (p.1317–1318): (1) Q_spec = I·t / m_CAM · (2) ΔV = U_avg,charge − U_avg,discharge · (3) Q_irr = Q_charge − Q_discharge · (4) Q_AIC = Σ Q_irr(n) · (5) E_spec = Q·U_avg / m_Cell = Q·U_avg / (m_Li + m_In + m_Separator + m_Cathode composite) · (6) P_spec = I·U_avg / m_Cell · (7) R_tot = Σ h_RC · 상대 오차 RME · RSE (p.1315).
- **임피던스**: 선형 · 정상 · 시불변 검사 = 확장 Kramers–Kronig 시험 [36] + Z-HIT [28] → **f ≥ 500 kHz 잘라냄** · gDRT (Danzer [27] · Tikhonov L2 · λ = 수학적 최적 근처에서 비교 가능성을 위해 조정 · 0.1–0.3 · SI 표 22) · 시간상수 범위 위아래 한 decade 넓힘 · 시간상수 수 = 측정점의 3 배 · R0 · C0 · L0 = 집중 직렬 요소 · R_tot = RC 분포의 합 · 1 · 2 번째 (0.05 C) · 51 번째 (0.1 C) 충전 상태.

### 4-2. 입자 처리
- 계산 없음 — **입자 · 미세구조를 다루지 않는다** (단면 · 기공 · 영상 없음 · SEM 은 원료 분말만).  미세구조는 *"expected"* 의 말로만 나온다 (압력 이력 · 두께 · 혼합).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · SI 에 DEM · discrete · simulation 낱말 0 회).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 계산이 없다.  실험 쪽 문장 하나: *"high pressure (>300 MPa) and long compression times (in the order of several hours) are required to densify and reduce residual void space in thiophosphate-based SEs … However, NMC (secondary) particles are prone to breaking at such pressures, especially when compressed for extended periods of time"* (p.1311 · [13–15] 인용) — 시간 의존 치밀화 (크리프 쪽) 와 AM 파괴의 **실험 쪽 진술** (값 없음).
3. **2D / 3D** — 해당 없음 (계산 없음).
4. **압력을 뺄 때의 거동** — **재지 않았다**: *"the specific compression profiles, including how fast the pressure is applied and released, and the way the pressure was controlled (if it was controlled at all …), was not monitored in this study but is expected to have an effect on the microstructure"* (p.1312) · 압축 뒤 *"pressure relaxation, which is observed in ASSB cells after compression"* 이 OCV 에 영향을 줄 수 있다 (p.1312 · [22] Koerver 2017) · Table 1 이 **압력 이력 (올림 · 내림 속도)** 을 보고 항목으로 권고.

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 실험실 간 연구 (interlaboratory study · round robin) | 같은 시료 · 같은 지시를 여러 그룹이 각자 재서 그룹 기인 흩어짐을 재는 연구 — 여기선 조립을 일부러 풀었다 |
| press cell | 두 금속 스탬프 사이에 분리막 (≈500 µm) 과 전극을 누르고 틀 · 나사로 적층압 (5–400 MPa) 을 거는 실험실 셀 |
| p₁–p₄ · t₁–t₃ | 분리막 · 분리막 + 양극 · 전체 셀 압축 압력 · 시간 · 운전 적층압 (그림 1a) |
| 최선 셀 (best performers) | 50 사이클 뒤 > 120 mAh g⁻¹ (12 셀) |
| OCV 이상 셀 | 상자 그림의 1.5 × IQR 밖 낮은 초기 OCV (5 셀) — 통계에서 제외 |
| RME · RSE | 연구 중앙값 대비 그룹 평균의 상대 오차 · 그룹 SD / 그룹 평균 |
| 분극 전압 ΔV | 한 사이클의 평균 충전 전압 − 평균 방전 전압 (식 2) |
| Q_AIC | 0.1 C 사이클 비가역 용량 누적 (식 3–4) — 분해 반응 · Li 손실의 지표 |
| gDRT · R0 · R_tot | 일반화 이완 시간 분포 · 고주파 집중 저항 (저자: 분리막 저항) · RC 분포 합 (전체 셀 저항) |
| 겉보기 밀도 · 겉보기 σ (이 카드) | 기록 두께 · 질량 · 지름 · R0 로 카드가 낸 값 — 저자 값 아님 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 다시 자름) | (a) 단계별 조립 모식 (p₁t₁ → p₄) · (b) 그룹별 p₁–p₄ 막대 (0–750 MPa) · (c) t₁–t₃ + OCV 전 휴지 (10⁻²–10⁵ 분 로그) · (d) 원그래프: 작동 57 · 조립 실패 31 · 사이클 실패 7 · 기타 5 % | ★ 실험 앵커 등록 칸 (압력 · 시간 · 휴지) 의 실제 흩어짐 — 우리 300 MPa 단일 조건과 견줄 때 실험 쪽 조건 띠 |
| **Fig. 2** (`fig_2.png` · 다시 자름) | 바이올린: (a) OCV (n 39) · (b) 사전처리 충 · 방전 · 0.1 C 첫 · 50 번째 방전 · (c) CE · (d) 분극 (1 · 50 사이클) · 액체 기준 셀 삼각형 | ★ 셀 성능의 실험실 간 분포 (중앙 · IQR) — 결과 전 대조 띠의 표본 |
| **Fig. 3** (`fig_3.png` · 수동 크롭) | 4 × 3 산점: In at% · 적층압 (120–350 MPa 끊김) · OCV · 초기 분극 ↔ 첫 방전 · 유지율 · R_tot · 최선 = 주황 마름모 · 이상 = 빈 원 | 적층압 ↔ 유지율 (첫 용량 아님) · OCV ≥ 2.5 V · 분극 < 0.2 V 의 선별 규칙 |
| **Fig. 4** (`fig_4.png` · 다시 자름) | (a) 첫 0.1 C · (b) 50 번째: 그룹별 RSD · RME + 셀별 막대 (RME 순) · (c) Ragone · (d) 외삽 Ragone (30 µm SE · 20 µm Li) | ★ 그룹 안 ↔ 그룹 사이 흩어짐 (§3-6) |
| **Table 1** (`tab_1.png` · 다시 자름) | 보고 항목: p_x · t_x · 압력 이력 · 적층압과 제어 · In : Li 원자비 · CAM 로딩 · 초기 OCV · 휴지 시간 | ★ 실험 앵커 · 문헌 값 등록 칸 (단계 0) |
| **SI 표 1** (`tab_S1.png` · 다시 자름 — 도구가 차례 쪽을 잘랐다) | 그룹별 지름 · 압력 · 시간 · 적층압 · 제어 · 온도 · OCV 까지 시간 · 각주 (J · N) | §3-2 표의 원전 |
| **SI 표 2–20** (`tab_S2.png` = 2–7 · `tab_S8.png` = 8–13 · `tab_S14.png` = 14–20) | 셀별 l_In · l_SE · l_CC · m_Li · m_In · m_SE · m_CC · m_CAM · 로딩 · OCV · 전류 (파랑 = 계산 · 가정) | §3-9 겉보기 밀도 · σ 의 입력 · 두께 기록의 함정 |
| **SI 표 21–26** (`tab_S21.png`–`tab_S26.png`) | In : Li 비 · DRT 매개변수 (R_tot · R0 · C0 · L0 · λ) · 바이올린 통계 · EDX · LPSCl σ(T) · PEIS 시편 | σ₀ 펠릿 값 · R0 |
| **SI Fig. 1** (`fig_S1.png` · 다시 자름) | 그룹별 RSD (2 · 3 셀 색) · 평균 첫 방전 + SD 막대 | §3-6 (H 색 오류 [판독]) |
| **SI Fig. 2–5** (`fig_S2.png`–`fig_S5.png`) | 그룹 18 칸: 셀별 방전 용량 · CE · 분극 · Q_AIC vs 사이클 | 셀별 궤적 (G · D · F 의 감쇠 · S · H 의 평탄) |
| **SI Fig. 6–9** (`fig_S6.png`–`fig_S9.png`) | 유지율 바이올린 · 최선 정의 (120 mAh g⁻¹ 선) · R0 · R_tot (2 · 51 번째) · R0 vs 최대 압력 · R_tot vs 분극 | ★ SI 그림 9A = R0 ↔ 조립 압력 (P1 빠짐 · §3-5) |
| **SI Fig. 10** (`fig_S10.png`) | K1 51 번째 스펙트럼 · eKKT · Z-HIT 잔차 · gDRT (R_tot 181.5 · R0 34.3 Ω cm²) | DRT 처리의 예 |
| **SI Fig. 11–27** (`fig_S11.png`–`fig_S27.png`) | 그룹별 셀별 충방전 곡선 (1 · 2 · 10 · 20 · 30 · 40 · 50 사이클 · D 없음) · J 는 3.6–4.9 V | 셀 곡선 (원자료 MOESM7) |
| **SI Fig. 28** (`fig_S28.png` · 다시 자름) | 액체 기준 셀: 방전 · CE · 분극 · 곡선 | 재료 기준 (≈169 mAh g⁻¹ @ 0.1 C) |
| **SI Fig. 29–43** (`fig_S29.png`–`fig_S43.png` · 다시 자름) | 그룹별 Nyquist (1 · 2 · 51 번째 충전) + gDRT + 집중 요소 표 (T2 51 번째 'defective') | R0 · R_tot 의 원 스펙트럼 |
| **SI Fig. 44–47** (`fig_S44.png`–`fig_S47.png`) | XRD (LPSCl + Li₂S \* · NMC 622) · SEM (LPSCl · NMC 622 · 20 · 4 µm 눈금) · Arrhenius (Ea 0.39–0.40 eV) | 원료 입자 꼴 · σ₀ |
| 식 크롭 10 (`eq_01`–`eq_07` · `eq_00a` · `eq_00b` · `eq_S01`) · 근거 문단 20 (`txt_p*`) | 자료 처리 식 · 상대 오차 · 외삽 질량 (1.87) · σ = l/(R·A) · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **셀 자료**: 원자료 → 식 (1)–(6) (조정 그룹이 한 곳에서) · 사이클 1 = 사전처리 뒤 첫 0.1 C · 유지율 = 50 번째 / 첫 0.1 C 방전 (SI 그림 6).
- **통계**: 바이올린 (커널 밀도) + 상자 (IQR · 1.5 × IQR 수염) · 이상 셀 = 초기 OCV 하나로만 정함 (다른 그림의 이상점은 표시만 · 순차 제거 없음 · p.1312) · RME (중앙 대비) · RSD (모집단 SD) · 최선 셀 = 50 번째 > 120 mAh g⁻¹.
- **임피던스**: eKKT · Z-HIT 검증 → 500 kHz 이상 잘라냄 → gDRT (λ 조정 · SI 표 22) → R0 · C0 · L0 · R_tot.
- **Ragone**: 식 (5)–(6) · 외삽 = 얇은 SE · Li 질량만 바꿈.
- **이 카드의 처리**: Source Data 6 개를 openpyxl (read-only · data_only) 로 읽어 셀별 발췌 CSV · SD 재계산 (ddof 0 / 1 · 이상 셀 넣고 / 빼고) · 겉보기 밀도 · σ_app · Spearman (동률 평균 순위) · 본문 퍼센트 재계산 — 숫자는 §3 의 [카드 산술] 표지.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **측정 대상 · 상태 · 재료가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 압밀 압력 | 그룹마다 분리막 hand-pressed–720 · 양극 50–720 MPa (최선 300–590) · 0.02–10 분 | 300 MPa 침대 (DEM · MPM) [우리] | 우리 300 MPa 는 실험 띠 안 (양극 압력 p₂ 18 그룹 중앙 375 MPa [카드 산술]) · 압력 이력 (속도 · 시간) 은 실험 쪽도 미기록 |
| 적층압 (운전) | 1–400 MPa · 유지율에 > 25–40 MPa 필요 | 망 계산은 압축 뒤 판 고정 상태 (하중 제거 회복 없음) [우리] | 운전 적층압은 우리 계산 변수가 아니다 — 수송 σ 를 셀 성능에 잇는 단계 (STEP4) 에서 조건 표지로만 |
| 순수 LPSCl 펠릿 기공 | [카드 산술] 380 MPa 3 분 펠릿 겉보기 1.573 · 1.458 g cm⁻³ = 1.64 기준 4.1 · 11.1 % (1.87 기준 15.9 · 22.1 %) · 두께 상태 [미확인] | 랩 표준 순수 SE 300 MPa 10–13 % (1.64 기준) [우리 · 고정] | **랩 표준과 다른 문헌 값** · 압력 다름 (380) · 두께 상태 미상 → 판정 · 맞춤에 쓰지 않는다 |
| 분리막 겉보기 밀도 (셀 안 기록) | 1.41–1.79 g cm⁻³ · 압력 경향 없음 · 1.64 기준 > 1 인 그룹 넷 | (해당 없음) | **두께 기록 ≠ 밀도 측정** — 문헌 셀 표의 두께로 기공을 만들지 않는다 (단계 0 함정) |
| SE σ₀ | 펠릿 1.63 · 1.85 mS cm⁻¹ (25 °C · 60 MPa · 380 MPa 성형) · 셀 분리막 겉보기 0.89–2.81 (R0 · 기록 두께) | σ₀ 보고 1.5 · 솔버 3.0 mS cm⁻¹ (펠릿값 · CL-91) [우리] | 1.5 는 실험실 간 띠 안 · 3.0 은 띠 위 끝 (2.81) 보다 높다 — 같은 분말도 실험실에 따라 ×3 |
| 셀 성능 | 첫 0.1 C 방전 21–143 mAh g⁻¹ (중앙 121.9) | STEP4 (BV 반응 분포 · 시간 전개) 는 있으나 셀 성능 대조 없음 [우리] | 흐름 밖 — 우리 셀 성능 예측의 대조값은 단일 실험실 값이 아니라 **띠** 로 받아야 한다 |
| 재현성 | 그룹 안 RSD 0.3–4 % (좋은 그룹) ↔ 그룹 사이 RME 1.4–77 % | DEM 시드 산포 (σ_ionic 폼 LOOCV 0.975 · 형제 시드 이상점) [우리] | 계산 쪽 '시드 산포' 는 실험 쪽 '그룹 안 SD' 에 해당 · 그룹 사이 흩어짐에 해당하는 계산 쪽 양은 없다 (조립 이력 변수) [카드 해석] |

### 7-2. ★ "같은 재료 · 다른 조립" 의 흩어짐을 우리 계획에 들일 때
- 쓸 수 있는 것: 실험값 하나를 우리 계산의 '정답' 으로 두지 않는 근거 (같은 재료 · 같은 전기화학 절차라도 첫 용량 중앙 대비 오차가 최대 77 %) · 실험 앵커를 받을 때 Table 1 칸 (압력 · 시간 · 압력 이력 · 적층압 · 제어 · In : Li · 로딩 · OCV · 휴지) 과 **셀 수 · SD 식 · 실패 수** 를 함께 받는 규칙.
- 붙여야 할 꼬리표: 이 흩어짐은 **조립을 풀어 둔** 설계의 결과 · 처리 변수 ↔ 성능의 인과는 측정되지 않음 · 단결정 NMC 622 · MSE LPSCl · In–Li.
- 쓰지 말 것: "적층압이 재현성을 지배한다" (원문보다 강함) · 셀 표의 두께로 만든 기공 · 이 논문의 첫 용량 띠를 우리 NCM811 침대의 절대 대조값으로.

### 7-3. ★ σ₀ 띠 (우리 B 축)
- 펠릿 1.63 · 1.85 mS cm⁻¹ (25 °C · 380 MPa · 60 MPa 틀) = 우리 σ₀ 보고 기준 1.5 (1저자 10-12 · *"문헌 LPSCl 펠릿 1.0–2.2"* 근거) 의 근거 목록에 하나 더 (재료 = MSE D50 ≈1 µm · Li₂S 섞임).
- 같은 분말의 셀 분리막 겉보기 σ 0.89–2.81 (중앙 1.41) — 실험실 조립 차이만으로 ×3.  우리 망 σ 절대값을 실험과 견줄 때 **σ₀ 쪽 불확실성 띠** 로 쓴다 (맞춤 표적 아님 · R0 에 분리막 밖 저항이 섞일 수 있음 · 두께 기록 미검증).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 · 셀 수준 · 통계** 만.  DEM 쪽 (망 · 기공 · 수송) 도 MPM 쪽 (형상 · 응력) 도 직접 주지 않고, 두 쪽 모두의 **실험 대조 규칙** (어떤 실험값을 어떤 띠 · 표지로 받나) 을 준다.
- 없는 반쪽: 압밀 과정 · 미세구조 · 기공 · 탈압 · 입자 파괴의 정량 — 원문 스스로 *"not monitored"* · *"could not investigate"* 로 적는다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님 · σ₀ 보고 1.5 · 솔버 3.0 mS cm⁻¹.  이 논문 재료 = 단결정 NMC 622 + Li₆PS₅Cl (MSE) + In–Li · 셀 수준 · 실험만.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 셋 — ① **두께 기록 ≠ 밀도 측정**: 같은 분말 분리막의 겉보기 밀도가 압력과 무관하게 1.41–1.79 g cm⁻³ 로 흩어지고 1.64 기준으로 1 을 넘는 그룹이 넷 [카드 산술] → 문헌 기공을 등록할 때 **두께를 잰 상태 · 방법** 칸이 없으면 받지 않는다 ② **분모가 둘**: 저자 1.87 ↔ 랩 표준 1.64 — 같은 펠릿이 기공 15.9 % ↔ 4.1 % (§3-8) — 표지 없는 기공끼리 비교 금지 ③ **Table 1 칸** (압력 · 시간 · 압력 이력 · 적층압 · 제어 · 로딩 · OCV · 휴지) 을 실험 앵커 등록 양식에 넣는다 | 압력별 기공 곡선 · 진밀도 측정 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 맞춤 표적은 **주지 않는다** — 380 MPa 펠릿 두 개의 겉보기 밀도 (1.573 · 1.458 · 두께 상태 [미확인]) 만 · 같은 압력 · 같은 분말에서 두 펠릿이 8 % 다르다 (두께 2.02 ↔ 2.19 mm) = 실험 한 점의 재현 폭 감각 | 압력 곡선 · 항복 · 경도 없음 |
| **단계 5** (3D 복합 압밀) | 없음 (복합 양극 두께 기록이 0.83–10.4 g cm⁻³ 로 물리 범위 밖 · 기공 계산 불가 [카드 산술]) | 기공 · AM 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 보고 항목 하나: **압력 이력 (올림 · 내림 속도) 과 제어** (Table 1) — 저자가 *"not monitored … expected to have an effect on the microstructure"* 라 적은 변수 · 압축 뒤 *"pressure relaxation"* 은 OCV 에 영향 (정성) | 회복량 · 두께 변화 · 탈압 곡선 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★ σ₀ 띠: 펠릿 1.63 · 1.85 mS cm⁻¹ (25 °C) · 셀 분리막 겉보기 0.89–2.81 (실험실 간) · Ea 0.39–0.40 eV — 우리 σ_ion 절대값 대조의 σ₀ 불확실성 (§7-3) · R0 ↔ 조립 최대 압력의 음의 상관 (2 번째 충전 R0 · Spearman −0.61 · P1 빼면 −0.76 [카드 산술]) = 분리막 치밀화 방향의 실험 쪽 동행 (인과 아님) | 복합 양극 σ_ion · σ_e · 피복 · tortuosity 없음 |
| **후보 D0** (지금 DEM) | 없음 (계산 대조값 없음) · 실험 쪽 '조립 이력' 이 성능을 흩는다는 진술은 D0 의 단일 압력 · 단일 이력 침대가 실험 띠의 **한 점** 이라는 꼬리표의 근거 | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 인용 문장 (*">300 MPa"* + *"several hours"* 가 치밀화에 필요 · [13] Cronau 2021 · [14] Perrenot 2024) — 시간 의존 치밀화 (크리프 쪽) 가 있다는 실험 쪽 진술 · M0 가 시간 항 없이 압력만 쓰면 놓치는 축 | 값 없음 |
| **U0–U6** | 없음 | — |
| **R1–R7** | **R4** (탈압) — 압력 이력이 미세구조를 바꾼다는 진술 (측정 없음) · **R7** (AM 파괴) — NMC 2 차 입자가 고압 · 긴 압축에서 깨지기 쉽다는 인용 문장 (이 논문 CAM 은 단결정 · 파괴 측정 없음) | R1 · R2 · R3 · R5 · R6 없음 |
| **결과 전 대조 항목** | ① σ₀ 띠: 같은 MSE LPSCl 의 펠릿 1.63 · 1.85 mS cm⁻¹ (25 °C) · 셀 분리막 겉보기 0.89–2.81 (중앙 1.41 · 20 셀 · 10 그룹) — 우리 σ₀ 보고 1.5 (띠 안) · 솔버 3.0 (띠 위) 표지와 함께 ② 셀 첫 0.1 C 방전의 실험실 간 띠 (중앙 121.9 · IQR 75.8–132.1 · NMC 622) — 우리 STEP4 셀 예측을 실험과 견줄 때 '한 실험실 값' 이 아니라 띠로 · 다른 CAM 이라 값은 흐름 밖 ③ **실험 앵커의 셀 수** — 우리 σ_e DC 분극 앵커 (SBE 1.63 · DBE 4.68 mS cm⁻¹ · 10-16 — 이 논문 펠릿 σ_ion 1.63 과 숫자만 같다 · 다른 양) · Bazzoun 2026 EIS 0.137 의 셀 수 · SD 식 · 실패 수를 적어 두고, 셀이 2 개 이하면 이 논문 기준 (세 벌) 아래라는 표지 | 맞추는 데 쓰지 않음 · 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 단결정 NMC 622 (우리 NCM811 · P/S 이봉) · Li₆PS₅Cl MSE D50 ≈1 µm (Li₂S 섞임 · 우리 DEM r_SE 0.5 µm = 지름 1 µm 와 크기는 비슷) · 무첨가 · In–Li 음극 · 실험 3D 셀 · 그룹마다 다른 압력 (우리 300 MPa) · 상온 (23–30 °C).

## 9. 적용 인사이트 (행동)
1. **실험 앵커 등록 양식 (단계 0)**: Table 1 의 여덟 칸 + 셀 수 · SD 식 (모집단 / 표본) · 실패 셀 수 · 두께를 잰 상태 · 진밀도 (1.64 / 1.87 표지) 를 앵커마다 적는다 — 칸이 비면 '조건 미확인' 표지로만 쓴다 (CLAUDE.md 의 DC 앵커 *"측정 조건 미확인"* 과 같은 꼴).
2. **"n ≥ 2 평균" 의 표지**: 두 셀 평균 · 모집단 SD 는 이 논문 기준 (세 벌) 아래 — 문헌 값 (예: `schmitt2026_…` 의 *"at least two identical cells"*) 을 받을 때 그 표지를 붙이고, 차이를 주장할 때는 평균의 표준오차 (SD/√n) 로 판단한다 [카드 해석].
3. **σ₀ 불확실성 띠 (단계 7 · B 축)**: 같은 분말 · 다른 실험실 겉보기 0.89–2.81 · 펠릿 1.63–1.85 mS cm⁻¹ — 우리 σ_ion 절대값의 실험 대조에서 σ₀ 를 한 값으로 두지 않고 이 띠로 민감도를 적는다 (보고 1.5 는 띠 안).
4. **셀 표의 두께로 기공을 만들지 않는다**: 같은 분말 분리막의 겉보기 밀도가 압력 경향 없이 1.41–1.79 (1.64 를 넘는 그룹 넷) — 두께 기록은 상태 · 방법이 없으면 밀도 측정이 아니다.
5. **흐름 밖 (STEP4 · 셀 성능)**: 셀 예측을 실험과 견줄 땐 OCV ≥ 2.5 V · 초기 분극 < 0.2–0.25 V · 적층압 ≥ 25–40 MPa 의 '건강한 셀' 조건을 먼저 맞춘 셀끼리 — 낮은 적층압 (0–10 MPa) 셀의 유지율 저하를 수송 망 탓으로 읽지 않는다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "When 21 research groups assembled Li₆PS₅Cl/single-crystal NMC 622 cells with their own assembly protocols but a common electrochemical protocol, 43 % of 68 cells failed before 50 cycles and the initial 0.1 C discharge capacities ranged from 21 to 143 mAh g⁻¹ (median 121.9 mAh g⁻¹, 33 cells); low cycling pressures (1–10 MPa) coincided with poor capacity retention, whereas initial capacities did not correlate with cycling pressure (Puls et al., *Nat. Energy* 9 (2024) 1310–1320)."
- "Puls et al. recommend reporting at least the average and error range of triplicate cells, the number of failed cells, the processing pressures and times, the compression profile, the cycling pressure and its control, the In-to-Li ratio, the CAM loading, the initial OCV and the rest time (Nat. Energy 2024, Table 1)."
- (σ₀) "A Li₆PS₅Cl pellet pressed at 380 MPa for 3 min showed 1.63–1.85 mS cm⁻¹ at 25 °C under 60 MPa (two pellets; Puls et al. 2024, Supplementary Table 25)."
- 국문 (한정어와 함께): *"같은 재료 (단결정 NMC 622 · Li₆PS₅Cl · In) 로 21 개 연구 그룹이 각자 조립한 셀의 0.1 C 첫 방전은 21–143 mAh g⁻¹ 로 흩어졌다 (Puls 2024 · 전기화학 절차만 공통) — 낮은 적층압 (1–10 MPa) 은 유지율 저하와 함께 갔지만 첫 용량과는 상관이 없었고, 저자는 처리 변수와 성능의 뚜렷한 경향은 없다고 적는다."*
- ⛔ 쓰지 말 것: "적층압이 실험실 간 재현성을 지배한다" · "21 개 기관" · "셀이 늘면 SD 가 줄어든다" (원문 표현이지만 평균의 표준오차와 섞인 말 — 쓰려면 원문 인용 표지 + §3-6 한정).

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-10 의 ①–⑤.
**카드가 본 한계**
1. **인과 없음** — 처리 변수 ↔ 성능은 동행 · 상관뿐 (그룹마다 여러 변수가 함께 다르다 · 조립을 일부러 풀었다).
2. **표본** — 그룹당 1–3 셀 · 0.1 C 해석 33 셀 · 사전처리 23 셀 (본문 '11 그룹' · 원자료로는 9 그룹) · 그림의 그룹 19 (21 과 차이 설명 없음).
3. **통계 표기** — 모집단 SD · 이상 셀의 포함 여부가 그림 · 문장마다 다름 (퍼센트 두 개는 이상 셀까지 넣어야 맞고 · 그림 4 · SD 평균도 A · F 포함) (§3-4 · §3-6).
4. **두께 · 밀도** — 셀 표의 두께는 상태 · 방법 미기재 · 겉보기 밀도가 물리 범위 밖인 셀이 있다 (S 분리막 · Q 양극) → 카드의 겉보기 밀도 · σ 는 '기록이 얼마나 흩어지나' 의 예로만.
5. **R0 의 뜻** — 저자는 분리막 저항이라 부르지만 고주파 집중 저항에 무엇이 들어가는지 (분리막 벌크 · 입계 · 접촉 · 배선 · 양극 이온 경로 일부) 는 분리되지 않았다 · 500 kHz 위를 잘라냈다.
6. **재료 전이** — NMC 622 단결정 · MSE LPSCl (Li₂S 섞임) · In–Li · 무첨가 · 그룹마다 다른 압력 — 우리 NCM811 침대의 절대값 대조 불가.
7. **압력 이력 · 탈압 · 미세구조 미측정** — 원문의 핵심 가설 (*"processing protocol mostly plays a role in the resulting microstructure"*) 은 이 논문 안에서 검증되지 않았다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [14] | Perrenot, P. et al. Room‐temperature sintering of amorphous thiophosphate solid electrolyte (Li3PS4): coupling morphological evolution to electrochemical properties. Adv. Funct. Mater. https://doi.org/10.1002/adfm.202310739 (2024). | ★ *"high pressure (>300 MPa) and long compression times (in the order of several hours)"* 의 인용처 (치밀화) — 시간 의존 치밀화 (단계 4 · M0 · 질문 a · c) · 정본 카드 없음 (`jeong2024_…` [20] · `korjus2025_…` [18] · `thompson2026_…` [2] 가 인용만) |
| [15] | Perrenot, P., Bayle-Guillemaud, P. & Villevieille, C. Composite electrode (LiNi0.6Mn0.2Co0.2O2) engineering for thiophosphate solid-state batteries: morphological evolution and electrochemical properties. ACS Energy Lett. 8, 4957–4965 (2023). | ★ NMC 2 차 입자가 고압 · 긴 압축에서 깨진다는 인용처 (R7 · 질문 d) — 카드 없음 · ⚠ `jeong2024_…` 의 [17] 은 같은 저자 · 같은 해 ACS Energy Lett. 8, **4531** 로 적는다 (다른 논문인지 [미확인]) |
| [22] | Koerver, R. et al. Capacity fade in solid-state batteries: interphase formation and chemomechanical processes in nickel-rich layered oxide cathodes and lithium thiophosphate solid electrolytes. Chem. Mater. 29, 5574–5582 (2017). | ★ 압축 뒤 *"pressure relaxation"* 의 인용처 (질문 b · 단계 6) — 카드 없음 (정본 `koerver2018_…` 은 다른 논문) |
| [1] | Randau, S. et al. Benchmarking the performance of all-solid-state lithium batteries. Nat. Energy 5, 259–270 (2020). | 셀 수준 벤치마크 · 목표 비에너지 (250–400 Wh kg⁻¹) 의 출처 — 카드 없음 (`beutl2024_…` 가 인용만) |
| [11] · [13] · [10] · [16] · [31] | Doux 2020 · Cronau 2021 · Minnmann 2021 · Bielefeld 2019 · Ohno 2020 | 정본 카드 있음 (`doux2020_pressure_effects_sulfide_se_jmca` · `cronau2021_stack_pressure_ionic_conductivity` · `minnmann2021_jes_charge_transport_bottlenecks` · `bielefeld2019_microstructural_modeling_composite_cathode` · `ohno2020_interlab_ionic_conductivity_argyrodite`) |
| [12] · [32]–[34] | Gittins 2023 (슈퍼커패시터) · Ehelebe 2022 (연료전지) · Hill 1992 (Rietveld) · Tesch 2023 (OER) | 다른 분야 실험실 간 연구 — 방법 계보 (우리 흐름 밖) |

## 13. [미확인] 목록 (본문 11 쪽 + SI 42 쪽 + Source Data 6 개 전수에 없음)
1. 21 그룹 ↔ 그림 · 표의 19 그룹 문자 (C · I) 의 차이.
2. 셀 두께 (l_In · l_SE · l_CC) 를 잰 상태 (셀 안 · 밖 · 하중 중 · 뺀 뒤) · 방법 · 조정 그룹 PEIS 펠릿 두께의 측정 상태.
3. 압력 이력 (올림 · 내림 속도 · 유지 중 이완) · 운전 중 적층압의 실제 값 (제어 없는 15 그룹).
4. NMC 622 의 진밀도 · 코팅 여부 · 입경 분포 · LPSCl 의 진밀도 측정 (1.87 은 'theoretical' 로만 인쇄 · 출처 없음).
5. 59 % · 69 % 를 실제로 어떤 셀 집합으로 셌는지 (이상 셀까지 넣으면 맞는다는 것은 카드 산술 · 원문 서술 없음) · 'Average Stabw' 열 (10.70 · 7.39) 의 정의 (원자료 칸 이름뿐).
6. R0 에 들어간 저항 성분 (분리막 벌크 · 입계 · 접촉 · 배선) 의 분리.
7. 최선 셀 셋의 In > 85 at% 가 합금 조립 방향 때문인지 (저자 추정 · 미보고).
8. 그림 2a 의 39 셀 ↔ 그림 1d 'working 39' 의 같은 집합 여부 (Q3 · J1 · P1).
9. [15] Perrenot 2023 의 쪽 (4957 ↔ 다른 카드의 4531).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 본문 11 쪽 + SI 42 쪽을 글자 층 추출로 전부 읽고, SI 표 2–20 의 글자 색 (파랑 = 계산 · 가정) 을 span 색으로 가렸다.  서지 = 본문 첫 쪽 (제목 · 저자 55 · 접수 · 수락 · 온라인 · DOI) · 머리글 (Nature Energy | Volume 9 | October 2024 | 1310–1320) · p.1319 (교신 · 기여 · 연구비 · 심사) · p.1320 (CC BY 4.0 · 소속 36).  SI 첫 쪽 = 같은 제목 · DOI.  원문 낱말 셈: DEM · discrete · simulation = 0 · triplicate 2 (p.1310 · p.1316) · immense = 0.
- Source Data MOESM2–MOESM7 (.xlsx) 을 python3 -I + openpyxl (read_only · data_only) 로 읽음 — 파일은 커밋하지 않고 MOESM6 'Processing & Summary' 41 셀 발췌만 CSV 로 (`source_data_cells_extract.csv`).  본문 수치 대조: OCV 2.6 ± 0.1 (34 셀 2.564 ± 0.107) · SD 10.0 / 7.0 (10.04 / 7.03) · RME (S 1.41 · M 2.31 · Q 3.27 · B 3.37 · K 10.66) · 최선 12 셀 · 유지율 > 100 % 다섯 셀 · 첫 CE < 75 % 네 셀 = 재현 · 59 % · 69 % = 그림 셀 집합으로는 재현 안 됨 (이상 셀까지 넣으면 맞음) · R0 18–42 = 재현 안 됨 (H 48.5–50.6) (§3-4 · §3-5).
- 그림 크롭 **92 장** = 도구 60 (본문 그림 3 · 표 1 · SI 그림 47 · SI 표 9) 중 **다시 자름 39** (본문 그림 1 · 2 · 4 = 패널 잘림 · 표 1 = 주석 · SI 표 1 = 차례 쪽을 잘랐음 · SI 표 2 = 색 범례 문단 넣음 · SI 표 23 = 오른쪽 열 · 아래 행 · SI 그림 1 · 3–9 · 12 · 28 = 아래 축 이름 (S6 은 빈 오른쪽 여백도) · S17 · S19 · S21 · S27 · S47 = 빈 오른쪽 여백 · S45 · S46 = 위 2 pt · S29–S43 = 빈 오른쪽 여백 → 본문 3 + 표 4 + SI 그림 32) + **손 크롭 32** (본문 그림 3 · SI 표 24 = 도구 '영역 없음' · 식 10 · 근거 문단 20).  SI 표 3–7 · 9–13 · 15–20 은 쪽 단위 크롭 (tab_S2 · S8 · S14) 안에 있다.  92 장 전부 열어 확인 (축 이름 · 표 아래 행 · 식 번호 · 이웃 줄 섞임).
- 2 차 인용 대조: `alharbi2026_…` (L164 · L243 · L266 · L332 · L386 · L466 · L482) · `schmitt2026_…` (L38 · L122 · L404) · `kissel2025_…` (L63 · L336) — 고치지 않았다 (카드 문제 = 정독 출력 batch_133 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (588) + DOI (`s41560-024-01634`) · 제목 (`Benchmarking the reproducibility`) · 제1 저자 (`Puls`) grep — 카드 없음 (인용만: alharbi2026 · schmitt2026 · kissel2025 · `kissel2026_…` L517 의 Puls 는 다른 논문 (*Opportunities and limitations of partial transport quantification …*)) (2026-11-16).

## 🔗 관련 카드
- 실험실 간 · 실험실 안 재현성: `ohno2020_interlab_ionic_conductivity_argyrodite` (σ_ion · 이 논문 [31]) · `beutl2024_round_robin_coin_cell_sulfide_assb` (황화물 코인셀 4 기관) · `kissel2025_cathode_mixing_quality_cam_utilization_reproducibility_press_cells` (혼합 질 · 이 논문을 [26] 으로 인용).
- 압력 · 적층압 · 펠릿 σ: `doux2020_pressure_effects_sulfide_se_jmca` ([11]) · `cronau2021_stack_pressure_ionic_conductivity` ([13]) · `wang2024_hot_pressed_lpscl_pressure_invariant_conductivity` · `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens`.
- 복합 양극 · 수송: `minnmann2021_jes_charge_transport_bottlenecks` ([10]) · `bielefeld2019_microstructural_modeling_composite_cathode` ([16]).
- 가리킨 카드: `alharbi2026_coupled_design_ultrathin_composite_se_review` ([110]) · `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` ([12]).
- 🔗 **같은 저자 · 같은 해 (2024) 카드** (이 논문의 공저자가 제1 저자): [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (Min-Gi Jeong · Hatzell · Vishnugopi · Mukherjee — NCM811 복합 양극 SE 입경 · XCT 기공 · 재압축) · [`minnmann2024_microstructure_porosity_visualization`](minnmann2024_microstructure_porosity_visualization.md) (Philip Minnmann · Janek — 복합 양극 기공 시각화) — 이 논문의 그룹 문자와 그 랩의 짝은 원문이 밝히지 않는다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
