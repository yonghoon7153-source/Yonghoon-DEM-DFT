# batch 115 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 밖 · 68 번 파일 · 대피 세션)

대상: `kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity` — A. G. Kashkooli · S. Farhad · D. U. Lee · K. Feng · S. Litster · S. Komini Babu · L. Zhu · Z. Chen, "Multiscale modeling of lithium-ion battery electrodes based on nano-scale X-ray computed tomography", *J. Power Sources* **307** (2016) 496–509 · DOI 10.1016/j.jpowsour.2015.12.134
상용 LFP 양극을 나노 XCT (분해능 50 nm · 복셀 16 nm · 시야 16 µm) 로 재구성해 750 nm REV 를 3D 미시 (고체 Fick 확산 + 가변 고체 확산계수) 로 두고 1D P2D 거시와 매 시간 걸음 양방향으로 묶은 COMSOL 모델 · 거시 Bruggeman 대신 열전도 유사로 잰 τ (전해질 2.2472 · 고체 1.7311) · 영상 비표면적 3.6 µm⁻¹ · C/10–4C 방전 대조 — 액체 LIB · 압밀 · 역학 0.
쪽 = 학술지 쪽 p.496–509 (PDF 쪽 = 학술지 쪽 − 495) · SI p.1–5 · 판독 원자료 = `litdb/figures/kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity/digitized.csv` (106 행 · 그림 3) · `colorbar_extremes_printed.csv` (36 행 · 그림 4 · 7 · 8 · S3 색 막대 끝값) · 후보 표의 행이 아니다 (1저자 11-12 *"지금 먹여준 것들 다 논문 에이전트 돌린다"* · S8 L277) → '고른 의도' 없음 · 넣는 까닭 대조 결과 **일부** (단계 7 · 넘김 h 의 방법 · 정의 · 함정만 · 압밀 · 탈압 · 우리 재료 값 0).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE · 압력 없음.  같은 전극의 기공 둘만 (영상 40 % · BET 35 % · p.499 [인쇄]) = 랩 표준 (순수 SE 기공 10–13 % · 진밀도 1.64 g/cm³) 과 다른 문헌 값 · 다른 계 (액체가 채울 기공) — 나란히만 둔다 (카드 §7-2).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음.

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙이 없다 (영역 확장으로 이웃 활물질을 융합 · p.498).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 MPM 없음.  영상 해상도 · 수치 오차 쪽 근거만 (넓이 · 수송 측정의 규칙 — MPM 역학 규칙 아님):
- [f] kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity | 분해능 50 nm · 복셀 16 nm ↔ P2D 일차 입자 지름 74 nm (본문 37 nm 반지름) = 복셀 4.6 개 · 분해능 1.5 개 [카드 산술] → 영상 고체 = 덩어리 (등가 반지름 3(1 − ε)/a = 0.50 µm) · 영상 a 3.6 µm⁻¹ = 같은 논문 구 모형 (반지름 37 · 72 nm → 48.6 · 25.0 µm⁻¹) 의 1/13.5 · 1/6.9 [카드 산술] | 카드 §3-7 · p.498 · p.500 · p.505 | [인쇄 · 카드 산술] | 해상도 수렴 시험 없음 · 영역 확장 융합이 넓이를 더 줄인다 [카드 추론]
- [f] kashkooli2016_… | 수치 오차 추정 = REV 크기 sweep 하나 (부분 정육면체 283–2122 nm 의 ε · a · 표 1) — 707 nm 이상에서 a ±3.6 % · ε 0.36–0.42 (원문 '3 % 안' 보다 넓다 [카드 산술]) · 메시 · 시간 걸음 · 해상도 · 전기화학 결과의 REV 수렴 없음 | 카드 §3-2 · §4-5 · p.499–500 · 표 1 | [인쇄 · 카드 산술 · 미확인] | 기하 지표만 수렴 확인

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 미시 3D + 거시 1D · 2D 는 표시용 단면 (그림 1a) 뿐 · 2D ↔ 3D 진술 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity | (DEM 아님 · 영상 → 연속체 · 같은 식의 두 규모) 3D REV ↔ 1D P2D 를 **매 시간 걸음 양방향** (concurrent) — 넘기는 양 = 세공벽 플럭스 j_n (거시 → 미시 경계 조건 · 식 11) · C₁s 로 i₀ (식 9) · OCP 를 갱신한 j_n (미시 → 거시) · 같다고 둔 양 = *"To update the flux we assume that the electric potential and electrolyte concentration at the interface does not change between the two scales"* (p.502) · 고리는 *"until the stop operation condition of the cell is satisfied"* (p.503) | 카드 §4-4 · 그림 2 · p.502–503 | [인쇄] | 역학 넘김 아님 · 우리 DEM → MPM 스캐폴드 (압밀 끝 한 번 · 기하 · 한 방향) 와 시점 · 방향 · 넘기는 양이 다르다 · 거시 마디 수 · REV 를 마디마다 따로 두었는지 [미확인]
- [h] kashkooli2016_… | 서열 결합 (대리 모델 · 조회표) 비판: *"Although using serial method diminishes computational time, it includes error due to uncertainty in fitting the empirical model to microstructural data. In addition, the assumption of quasi steady state in microscale is highly questionable in a mainly time dependent model."* | 카드 §4-4 · p.497 | [인쇄] | 저자 주장 — 같은 계에서 서열 ↔ 동시 결합을 계산으로 견주지 않았다 [카드 해석]

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
이 배치에 없음 — 가압 · 탈압 · 역학 0 (카드 §4-6 (iv) · §7-5).  원문이 적은 한계는 영상 쪽뿐 (*"In this work, additives are not considered separately from the active material because it is hard to clearly distinguish them from active material. Moreover, treating them as separate region provokes an excessive computational load."* · p.498).

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Kashkooli et al. 2016, J. Power Sources 307, 496–509)
- [k] kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity (Kashkooli et al. 2016 · J. Power Sources 307, 496–509) | **말 없음** — DEM 을 쓰지 않는다.  가까운 문장 = 연속체 P2D (같은 크기 · 균질 · 등방 구 · Bruggeman) 비판: *"However, it fails to predict the phenomena related to inhomogenous structure of the electrode microstructure such as performance drop at high rates [20,21]."* (p.497) · *"These assumptions are not valid for real battery electrodes where the electrode microstructure is inhomogeneous, non-isotropic with 3D pores and constructed from different size and shape particles."* (p.504–505) | 카드 §4-6 (i) | [인쇄] | 단단한 구 · 점접촉 DEM 의 한계 진술로 인용하지 않는다 (구 · 균질 연속체 가정의 비판)

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Kashkooli et al. 2016)
- [l] kashkooli2016_… (Kashkooli et al. 2016) | 해당 없음 — 소성 · 역학 · 압밀 0.  우회 꼴만: 변형이 끝난 상용 전극 형상을 영상으로 가져와 고정 (접촉은 영역 확장 융합으로 형상에 묻음) · 맞춘 값 2 개 (D_LFP · σ — 같은 방전 곡선 · p.505) · 비용 주장 = 나노 입자 전극을 통째 3D 로 풀면 *"around 10⁶ times more mesh elements in 3D"* (p.497 · 실측 계산 시간 · 요소 수 [미확인]) | 카드 §4-5 · §4-6 (ii) | [인쇄 · 미확인] | 소성이 어려운 이유의 근거로 인용하지 않는다

## m — 받아들일 통찰
- [m] kashkooli2016_… | 무엇을: **tau2 방향 평균 규칙을 값과 함께** — 표 2 의 τ_avg 는 세 방향 조화평균 (2.2471 · 1.7308 ↔ 인쇄 2.2472 · 1.7311 · 산술평균 2.2559 · 1.7355 과 다름) = 방향별 f = ε/τ 의 산술평균 [카드 산술] · 원문은 규칙을 적지 않는다 · 우리 쪽 어디에: 단계 7 · 흐름 밖: STEP3 · 접촉망 tau2 보고 · 비교 문서 J 절 · 왜: 같은 표의 두 평균이 0.4 % 갈리고 방향 비 1.13–1.17 이라 규칙이 없으면 대조가 모호하다 (카드 §3-3)
- [m] kashkooli2016_… | 무엇을: **REV 두 규칙을 결과 전에 등록** — (i) 가장 큰 입자 하나가 들어가는 부피 (ii) 부분 정육면체를 키우며 기하 지표가 정한 띠 안에 드는 크기 · 그들은 ε · a 만 보고 전기화학 결과로는 REV 를 보지 않았다 · 우리 쪽 어디에: 단계 0 · 단계 7 · U6 (σ · tau2 · 피복으로도 같은 sweep) · 왜: 카드 §3-2 · 표 1 (707 nm 아래 a +19–37 % · 위 ±3.6 %)
- [m] kashkooli2016_… | 무엇을: **물리 범위 점검을 결과 전 항목으로** — 미시 농도 ≤ c_max · OCP 단조 (γ > 0) · 잘린 하한 (2.5 V) 표시 · 지도 끝값의 내부 일관 (한 REV 안 φ₁ − φ₂ 일정 → η 지도 = OCP 지도의 뒤집힌 판) · 이 논문은 c_max 의 4.65 배 · γ < 0 (y 0.13–0.72) 를 그대로 그렸다 · 우리 쪽 어디에: 흐름 밖: STEP4 반응 · 확산 결과 검사 · 결과 전 대조 항목 · 왜: 카드 §3-4 · §3-6
- [m] kashkooli2016_… | 무엇을: **넘김 매니페스트 칸** — 결합마다 '무엇이 · 언제 · 어느 방향으로 건너가고 · 무엇을 같다고 두는가' 를 한 표로 (그들의 그림 2 + p.502–503 한 문장) · 우리 쪽 어디에: 흐름 밖: 질문 h · DEM → MPM 스캐폴드 · STEP2 → STEP3 · 왜: 카드 §4-4 · §7-4

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] S.J. Cooper, D.S. Eastwood, J. Gelb, G. Damblanc, D.J.L. Brett, R.S. Bradley, et al., Image based modelling of microstructural heterogeneity in LiFePO4 electrodes for Li-ion batteries, J. Power Sources 247 (2014) 1033–1039 (원문 목록 [48] 그대로 · 목록에 DOI 10.1016/j.jpowsour.2013.04.156) | 이 논문 τ 방법 (열유속 · 균일 비다공 시료 대비) 의 원전 · 같은 LFP 의 방향 τ · 부분 부피 — 단계 7 · 비교 문서 J 절 · 카드 §3-3 | litdb 확인: papers/ 에 cooper2014* 없음 (cooper2017 = 다른 논문) · DOI grep 0 · 'Image based modelling' grep = `tjaden2018_…` · `landesfeind2016_…` (인용만)
- [n] D.-W. Chung, M. Ebner, D.R. Ely, V. Wood, R. Edwin García, Validity of the Bruggeman relation for porous electrodes, Model. Simul. Mater. Sci. Eng. 21 (2013) 074009 (원문 목록 [23] 그대로) | Bruggeman 대체의 근거 — 단계 7 · 비교 문서 J 절 · 카드 §1 · §12 | litdb 확인: papers/ 에 chung20* 없음 · DOI grep 0 · 제목 grep = `malifarge2017_…` · `tjaden2018_…` (인용만)
- [n] B. Yan, C. Lim, L. Yin, L. Zhu, Three dimensional simulation of galvanostatic discharge of LiCoO2 cathode based on X-ray nano-CT images, J. Electrochem. Soc. 159 (2012) A1604–A1614 (원문 목록 [27] 그대로) | 영상 기반 3D 방전 직접 계산 (같은 공저자 L. Zhu) — 다중 스케일 없는 쪽의 대조 · h · 단계 7 · 카드 §12 | litdb 확인: papers/ 에 yan20* 없음 · DOI grep 0 · 제목 grep 0
- [n] S. Komini, A. Mohamed, J. Whitacre, Multiple imaging mode X-ray computed tomography for distinguishing carbon additives in lithium battery cathodes, J. Power Sources 283 (2015) 1–16 (원문 목록 [39] 그대로) | 탄소 첨가제 상을 영상에서 가르는 법 (흡수 + Zernike 위상 대비) — 이 논문이 못 한 상 규약 · 단계 7 · 단계 0 · 카드 §3-1 · §12 | litdb 확인: papers/ 에 komini* 없음 · DOI grep 0 · 제목 grep 0
- [n] W. Du, N. Xue, W. Shyy, J.R.R.A. Martins, A surrogate-based multi-scale model for mass transport and electrochemical kinetics in lithium-ion battery electrodes, J. Electrochem. Soc. 161 (2014) E3086–E3096 (원문 목록 [37] 그대로) | 서열 결합 (대리 모델) 의 대표 — 이 논문이 비판한 쪽 · h · 카드 §4-4 · §12 | litdb 확인: papers/ 의 du* = du2022 · du2025 (다른 논문) · DOI grep 0 · 제목 grep 0

## 카드 문제
없음 — 이 논문을 인용한 정본 카드는 `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` 하나 (L408 참고 [11]) · 서지 (저자 8 · 제목 · J. Power Sources 307 (2016) 496–509) 가 원문 첫 쪽과 같고 값 인용이 없다.  같은 줄의 *"카드 없음 — 나노 CT 실구조 다중스케일"* 은 이 카드로 낡았다 (기록만 · 고치지 않음 · 그 카드 🔗 관련 카드 절에 한 줄만 더함).
- 서지 메모: 지시서의 'S. K. Babu' ↔ 원문 첫 쪽 'Siddharth Komini Babu' (성이 'Babu' 인지 'Komini Babu' 인지 원문으로 못 가름 · 같은 논문 참고 [39] 는 'S. Komini') — 원문 표기를 따랐다.
- 원문 안 어긋남 (카드 §11 · 원문 문제 · 카드 문제 아님): 본문 'SOC 0.5 에서 최대 4.51 × 10⁴' ↔ 그림 4 의 SOC 0.95 칸 · 식 (8) η 부호 꼴 ↔ 그림 · P2D 입자 지름 37 / 반지름 37 / 반지름 72 nm · '모든 율에서 더 정확' ↔ 판독 (1C 는 P2D 가 더 가깝다) · 'higher surface area' ↔ 3.6 < 25–49 µm⁻¹ · OCP 자료 C/25 ↔ C/50 · 그림 S3 중복 칸 (SI xref 21) · 그림 S4 가운데 OCP 히스토그램 (2.8–4.0 V) ↔ 그림 8 색 막대 (3.41 / 2.5 V) · j_n 단위 · 식 번호 (eq. 11 ↔ 10) · ε_sep = 1.
