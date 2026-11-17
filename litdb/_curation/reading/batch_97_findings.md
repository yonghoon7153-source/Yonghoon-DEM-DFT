# 배치 97 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-17 · 위시 W-1117-6)

카드 = `berkenkemper2023_compressibility_descriptors_binary_mixtures_deformation` (원문 = 출판본 15 쪽 (인쇄 p.1–15 = PDF p.1–15 · 논문 번호 118571) · SI 안내 없음 (*"Data will be made available on request."* p.13) · 그래픽 초록 1 · 그림 크롭 83 장 = 도구 10 (그림 1–5 · 7 · 8 + 표 1–3 → 그림 7 장 모두 캡션을 넣어 원 래스터로 다시 자름 · 표 3 장은 도구가 쪽 전체를 잘라 400 dpi 손 크롭) + 손 크롭 73 (그림 6 (도구가 놓침) · 그래픽 초록 · 패널 39 · 식 12 (번호 1–4 전부 + Table 1 의 번호 없는 식 8 · 행마다) · 근거 문단 20) — 점검 뒤 다시 자름 23 (패널 21 · 표 2) + 도구판 교체 10 (그림 7 = 캡션 없음 · 표 3 = 쪽 전체) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 349 행).
서지 (k · l 인용용) = Berkenkemper S., Klinken S., Kleinebudde P., *Investigating compressibility descriptors for binary mixtures of different deformation behavior*, Powder Technology 424 (2023) 118571, DOI 10.1016/j.powtec.2023.118571.
⚠ 재료 = **약학 부형제 넷** (소성 MCC · HPC · 취성 유당 TA · 무수 인산수소칼슘 DCP) 의 세 이원 혼합 (LPSCl · NCM 없음) — 실험만 · Ø8 mm 다이 300 MPa 한 번 · in-die 곡선 + 뺀 뒤 정제 · 계산 없음.  쪽 = 인쇄 쪽.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

이 배치에 없음 (SE 없음).  같은 꼴의 다른 재료 값만: 순물질 가압 중 (in-die · ≈297 MPa) DCP 20.7 · TA 3.1 · MCC 1.0 · HPC −6.7 % (음수) ↔ 뺀 뒤 23.8 · 7.8 · 6.9 · 1.1 % (300 MPa) · 진밀도 = He 피크노미터 (DCP 2.849 · HPC 1.208 · MCC 1.595 · TA 1.535 g/cm³ · 질량 기준 혼합 = 식 1 조화 평균) — 카드 §3-1 · §3-4 [인쇄 Table 2 · 판독 그림 1 · 4–6 · 카드 산술] · **랩 표준과 다른 문헌 값 · 다른 재료**.

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] berkenkemper2023_… | **in-die 탄성 회복 ER (식 3: (rth_id − th_id)/th_id × 100 % · 다이 안 제하 두께 회복)**: HPC 8.9 · MCC 5.4 · TA 3.5 · DCP 2.5 % (300 MPa) · 혼합은 MCC_HPC 거의 선형 · DCP 혼합 선 아래 (최대 −0.3 … −0.9 %p) | 카드 §3-2 · 그림 1C · 식 3 | [판독] · [카드 산술] | 약학 분말 · rth_id 를 읽는 시점 [미확인]
- [b] berkenkemper2023_… | **같은 정제의 가압 중 ↔ 뺀 뒤 기공 차** 3.1 (DCP) · 4.7 (TA) · 5.9 (MCC) · 7.8 %p (HPC) · in-die ER 만으로 계산한 뺀 뒤 기공은 실측보다 0.9–1.4 %p 작다 (사출 뒤 추가 회복 몫으로 읽힘) | 카드 §3-4 · §3-7 | [판독 그림 1A · 4–6] · [카드 산술] · [카드 추론] | HPC 는 가압 중 음수 기공이라 반대
- [b] berkenkemper2023_… | **제하 에너지 E3** (힘–변위 제하 곡선 아래 면적) HPC 1.33 · MCC 0.561 · TA 0.390 · DCP 0.136 J · E3 ↔ ER 상관계수 0.991 (조정 R² 0.981) | 카드 §3-3 · 그림 2A · 3E · p.6 | [판독] · [인쇄 상관] | E3 정의 = 그림 2A · 본문 '탄성 회복과 연관' 뿐

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] berkenkemper2023_… | **in-die Heckel Py** (−lnε = P/Py + a 의 두 곡률 사이 직선): HPC ≈16 · MCC 85 · DCP ≈470 MPa [인쇄 p.9] (판독 16.4 · 84.6 · 470.7) · TA 149 MPa [판독] · ⚠ *"a yield pressure of about 470 MPa does not correspond to the actual value of the material … this pressure is therefore insufficient for the Heckel analysis of a material with high resistance to deformation [40]"* (p.9) | 카드 §3-5 · 그림 7A | [인쇄] · [판독] | 일축 항복 환산 없음 · 약학 재료
- [c] berkenkemper2023_… | **Kuentz–Leuenberger C⁻¹** HPC ≈41 · MCC 139.9 · TA 323 · DCP 1875 MPa [판독] · C⁻¹ ↔ Py 상관 0.970 · 기울기 3.8 (문헌 '2–4 배' [43]) · 같은 MCC 등급 문헌 140 MPa 와 '비슷' | 카드 §3-5 · 그림 8G · p.13 | [판독] · [인쇄] | —

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

- [d] berkenkemper2023_… | **하중 몫 측정 없음** · 간접: 기공 · Py 가 *"MCC as well as TA dominate the behavior of the mixture already from a low fraction"* (p.9) · *"particularly from a weight fraction of 30% upwards"* (p.4) · 70 % 위 기공 변화 없음 = *"a hint that the percolation threshold of MCC and TA might lay in this range"* (p.4) · Bouvard 골격 (재밍) 가설 기각 쪽: *"This again argues for Jetzer's [32] approach rather than the formed skeleton theory of less deformable material"* (p.9) | 카드 §0-1 · §3-2 · §7 | [인쇄] | '단단한' DCP = 깨지는 응집체 (Py ≈470 · 두 직선 구간 p.8) — 우리 단단한 탄성 AM 다수 계와 다름 · 크기비 0.5–0.6

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

이 배치에 없음 (접촉 법칙 · DEM 없음 — 실험 서술자뿐).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] berkenkemper2023_… | 2D 계산 없음 · 3D 에 대한 말 하나 (분율 선택): *"the use of volume fraction might be advantageous in general when describing a three-dimensional tablet [25]"* | p.2 · 카드 §4-5 (iii) | [인쇄] | 혼합 규칙의 분율 이야기 — 2D → 3D 전이 근거 아님

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

- [h] berkenkemper2023_… | DEM 없음 · FE 언급만: van der Haven 등 [70] 이 FEM 으로 이원 혼합 F–D 곡선을 예측 (*"gave useful results"*) · 이 논문 판단 *"The effort of using FEM for predicting those parameters seems unnecessary, since there are also experimental data needed and the data of pure materials was observed to be sufficient"* | p.6 · 카드 §3-3 · §8 후보 B | [인쇄] | 넘김 선례 아님 (인용)

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (전지 재료 없음 · 300 MPa 한 압력) — 이원 혼합 기공–조성 곡선의 **꼴** 만: DCP 혼합은 선형 규칙 아래로 볼록 · 85 % (w/w) 에서 순물질보다 낮은 얕은 극소 (MCC_DCP 6.43 < 6.88 · TA_DCP 7.37 < 7.80 % [판독 · 원문 언급 없음]) — 카드 §3-2.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] berkenkemper2023_… | 높은 압력이 필요: *"Experiments at a higher compression pressure would be beneficial to further investigate the behavior of the TA_DCP mixtures"* (p.11) · DCP Py 는 300 MPa 로 불충분 (p.9) | 카드 §11 | [인쇄] | —
- [j] berkenkemper2023_… | 입도 · 형상 · 다성분: *"Further investigations of different material combinations, also of different particle sizes and shapes, are necessary to prove the suitability of these three descriptors for binary mixtures. A detailed investigation of the three analyses applied to ternary and multi-component mixtures would gain deeper insights"* (p.13) | 카드 §1 · §11 | [인쇄] | —
- [j] berkenkemper2023_… | 서술자 하나로 부족: *"A single parameter does not seem to be sufficient in any case to fully describe the tableting behavior"* (p.13) · Heckel 은 낮은 기공에서 부적합 (*"not suitable to describe volume changes at low porosity"* p.8) | 카드 §4-5 (ii) | [인쇄] | —
- [j] berkenkemper2023_… | 진밀도 오차: HPC · MCC He 밀도 과대 (물 > 4 %) — *"it was assumed that the magnitude of this error would not significantly affect the interpretation"* (p.4) · *"Heckel analysis is highly susceptible to errors in density determination"* (p.13) | 카드 §3-1 · §11 | [인쇄] | 가압 중 기공의 분모

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] berkenkemper2023_… (Berkenkemper, Klinken & Kleinebudde 2023, Powder Technol. 424, 118571) | **말 없음** — DEM 언급 0 (실험 논문 · 계산 쪽 언급은 FEM [70] 하나) | 카드 §4-5 (i) | — | k 질문의 근거로 쓰지 않는다
- [k] (관련 — 연속 압밀식의 한계) berkenkemper2023_… (Berkenkemper et al. 2023) | Heckel 의 낮은 기공 한계와 음수 기공: *"Heckel equation is not suitable to describe volume changes at low porosity. The cause of the curvature and a porosity decrease up to negative porosity values is reversible elastic deformation of the material under pressure [72]"* | p.8 · 카드 §3-4 | [인쇄] | DEM 한계 아님 — 가압 중 기공 측정 · 해석의 한계

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] berkenkemper2023_… (Berkenkemper et al. 2023) | 계산 없음 · '소성을 하나의 수로 재기' 의 어려움을 실험 쪽에서 보임: *"E2 cannot only be related to the plasticity of a material, but is also a measure of the resistance of a material to deformation"* (p.6) · *"The use of Pf or E2 to characterize a substance in terms of its compressibility or plasticity is not recommended"* (p.11) · *"the compression analyses appear to focus on different material properties. A single parameter does not seem to be sufficient"* (p.13) · 우회 = 서술자 여럿 (K · W · ab) | 카드 §3-3 · §3-5 · §4-5 (ii) | [인쇄] | 맞춘 값 = 곡선 맞춤 서술자 (모델 보정 아님) · 계산 비용 없음

## m — 받아들일 통찰

- [m] berkenkemper2023_… | **복합 기공 예측의 혼합 규칙 한정**: 변형 거동이 비슷하면 (소성–소성) 기공 · Py 가 선형 규칙을 따르고, 다르면 (소성–취성 · 취성–취성) 끝점 차의 37–46 % (무게) · 24–30 % (부피) 만큼 선 아래 — 우리 복합 (AM + SE) 기공을 순물질 선형 보간으로 쓰지 않는다 · 분율은 부피로 (NCM/LPSCl 밀도비 ≈2.9) | 단계 5 · 후보 M0 · 결과 전 대조 항목 | 카드 §3-6 · §8 · 그림 1 · 7
- [m] berkenkemper2023_… | **서술자 공간 대조**: DEM · MPM 가압 중 P–ε 곡선을 Heckel Py · Kawakita ab · Walker W · Johanson K 로 요약해 같은 in-die 실험과 견준다 — ab · K 는 조성에 선형 · K 는 압력 영향에 더 둔감 (*"K is more robust to the influence of the tableting pressure than Py"* p.11) · ⚠ K · W 의 식 ↔ 그림 값 어긋남 (그림 K = 기울기 역수 · W = 기울기) → 정의를 식으로 적는다 | 후보 D0 · 단계 4 | 카드 §3-7 · §3-8 · §4-2
- [m] berkenkemper2023_… | **가압 중 ↔ 뺀 뒤 한 표 + 자기 점검**: ε_in (네 경로가 DCP · TA · MCC 에서 0.5 %p 안) · ER (두께 회복) · E3 (제하 면적 · ER 과 r 0.991) · ε_out — 우리 언로딩 보고 꼴 · 진밀도 분모로 낸 가압 중 기공이 음수면 (HPC −6.7 %) 분모 · 가역 탄성 · 기계 보정을 먼저 본다 (우리 DEM ε_sphere 음수 경고 칸과 같은 자리) | 단계 0 · 단계 6 · 조건 R4 | 카드 §3-4 · §8
- [m] berkenkemper2023_… | **Heckel Py 의 최대 압력 경고**: 최대 압력이 Py 근처 이하이면 Py 는 재료 값이 아니다 (DCP ≈470 MPa @300 MPa · 원문) — 300 MPa 까지의 순수 SE Heckel 을 표적 · 대조에 쓸 때 선형 구간과 최대 압력 / Py 비를 결과 전에 적는다 | 단계 4 · 결과 전 대조 항목 | 카드 §3-5 · p.9

## n — 논문 에이전트 후보

litdb 확인 = 정본 `litdb/papers/` 600 장 (`ls`) + grep (제1 저자 성 · 제목 낱말 · 권 · 쪽 · DOI) + `_curation/wishlist.md` grep — 다섯 모두 카드 없음 · 위시에도 없음.

- [n] D.L.H. van der Haven, F.H. Ørtoft, K. Naelapää, I.S. Fragkopoulos, J.A. Elliott, Predictive modelling of powder compaction for binary mixtures using the finite element method, Powder Technol. 403 (2022), 117381, https://doi.org/10.1016/j.powtec.2022.117381. | h · 후보 B · M0 — 이원 혼합 압축을 FEM 으로 예측한 계산 선례 (이 논문 p.6 이 인용 · '쓸 만한 결과') · 혼합 매개변수를 순물질에서 어떻게 만드는지 · 카드 §3-3 · §12 | litdb 확인: `ls` 'haven' 없음 · '117381' · 'Predictive modelling of powder compaction for binary' grep 0 건 → 카드 없음
- [n] C.C. Sun, D.J.W. Grant, Influence of elastic deformation of particles on Heckel analysis, Pharm. Dev. Technol. 6 (2) (2001) 193–200, https://doi.org/10.1081/PDT-100000738. | b · c · 단계 0 — 가압 중 음수 기공 · Heckel 둘째 곡률 = 입자 탄성 변형 (p.8 [72]) · 우리 ε_sphere 음수 경고 칸의 실험 쪽 근거 · 카드 §3-4 · §12 | litdb 확인: `ls` 'sun2001' 없음 · 'Influence of elastic deformation of particles on Heckel' · 'PDT-100000738' grep 0 건 → 카드 없음
- [n] J. Ilkka, P. Paronen, Prediction of the compression behaviour of powder mixtures by the Heckel equation, Int. J. Pharm. 94 (1–3) (1993) 181–187, https://doi.org/10.1016/0378-5173(93)90022-8. | d · M0 — 혼합 Heckel 선형성 · 덜 변형하는 쪽의 지배 (MCC_DCP 음의 차 · DCP_Lactose 양의 차) · 밀도 차가 크면 부피 분율 · 낮은 기공 Heckel 비판 (p.2 · p.8 · p.9 [24]) · 카드 §12 | litdb 확인: `ls` 'ilkka' 없음 · 'Ilkka' · 'Paronen' · 제목 grep 0 건 → 카드 없음
- [n] S. Berkenkemper, P. Kleinebudde, Compressibility analysis as robust in-die compression analysis for describing tableting behaviour, RPS Pharm. Pharmacol. Rep. 1 (1) (2022), https://doi.org/10.1093/rpsppr/rqac004. | c · m · 후보 D0 — 이 논문의 자료 처리 · 회귀 구간 · K 정의 (표 1 식 ↔ 그림 값 어긋남을 가를 원전) · DCP Py 가 300 MPa 에서 고원에 안 닿는다는 근거 (p.3 · p.9 [40]) · 카드 §3-8 · §12 | litdb 확인: `ls` 'berkenkemper2022' 없음 · 'rqac004' · 'Compressibility analysis as robust' grep 0 건 → 카드 없음
- [n] G. Vreeman, C.C. Sun, Mean yield pressure from the in-die Heckel analysis is a reliable plasticity parameter, Int. J. Pharmaceut. X 3 (2021), 100094, https://doi.org/10.1016/j.ijpx.2021.100094. | c · 단계 4 — in-die Heckel Py 의 신뢰성 (둘째 곡률 [71] · 이 논문 p.8) · 우리 DEM 가압 중 P_y · lee2025 in-die P_y 대조의 근거 · 카드 §12 | litdb 확인: `ls` 'vreeman' 없음 · 'Vreeman' · 'Mean yield pressure from the in-die' · 'ijpx.2021.100094' grep 0 건 → 카드 없음

## 카드 문제

- `yano2024_eepa_binary_mixture_plasticity_compression_dem` L89 (§2 동기 · 원문 일본어 문장 미인용 요약) · L402 (§8 후보 M0) · L495 (§15 참고문헌 표 [17]) — *"이종 혼합의 압축 매개변수와 조성의 선형 관계 [17]"* · *"소성 · 취성 혼합의 압축 서술자와 조성의 선형 관계"* 는 **일부만 맞다**: 원문 (Berkenkemper 2023) 은 세 조합 (소성–소성 · 소성–취성 · 취성–취성) 이고, 조성에 선형인 것은 K · W · ab (· F–D 에너지) 뿐 — Heckel Py · 기공은 소성–소성 (MCC_HPC) 에서만 선형이고 **소성–취성 (MCC_DCP) 에서는 비선형** (p.9).  값 인용은 없고 서지는 원문 첫 쪽과 같다.  (고치지 않음 · 같은 꼴이 `wishlist.md` 의 batch_65 n 줄)
- 새 카드 자체 — 원문 안 어긋남 9 건은 카드 §3-8 · `figures.json` note_manual (혼합 비 목록 '30:70' 두 번 · Table 1 압축성 식 (K = 기울기) ↔ 그림 7C 의 K = 기울기의 역수 · Walker 식 (−W) ↔ 그림 W < 0 · 그림 8B · 8F 축 제목 'Weight fraction' · Kawakita a 선형 ↔ 비선형 두 문장 · E1 · E3 미정의 · Walker DCP 선형 시작 30 ↔ 50 MPa · 캡션 'MCC … and TA' · 'puches').
- 새 카드의 판독 검산 — 그림 8E ab ↔ Table 3 a/b⁻¹ 는 25 조성 중 24 가 ±0.0002 MPa⁻¹ 안 · 순수 MCC 한 점만 0.00044 (점선 끝에 가린 작은 마커 핵심) — 카드 §3-5 · `figures.json` key_note 에 같은 문구.
- (덤으로 발견 · 다른 카드) `chung2008_dem_parameters_bulk_behaviour_confined_compression` §5 Figure set 표 — 행 첫 칸이 `Fig. N` 으로 시작해 웹앱 `paper_figure_notes()` 가 그 행들을 **표 머리** (`_FIGTBL_HEAD`) 로 읽고 건너뛴다 → 그 카드의 그림 주석 팝업 = `t1` 하나뿐 (2026-11-17 `webapp/data.py` 로 확인) · 해석기 관례 = 첫 칸 번호만 (`1a,b`) — 새 카드는 '1 (패널 A–F)' 꼴로 써서 f1–f8 · t1–t3 가 붙는다.  (고치지 않음)
