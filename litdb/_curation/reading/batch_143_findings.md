# batch 143 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-22 · 후보 N-94)

대상: `tao2023_dry_mixing_degree_ptfe_fiberization_dry_nmc622_cathode` — R. Tao · B. Steinhoff · C. H. Sawicki · J. Sharma · K. Sardo · A. Bishtawi · T. Gibbs · J. Li\*, "Unraveling the impact of the degree of dry mixing on dry-processed lithium-ion battery electrodes", *Journal of Power Sources* **580** (2023) 233379 · DOI 10.1016/j.jpowsour.2023.233379 (6 쪽 + SI 5 쪽).
NMC622 : 카본블랙 : PTFE = 92 : 3 : 5 wt 건식 PTFE 양극 (액체 전해질 LIB · ≈7.2 mAh/cm² · ≈153 µm 로 같은 밀도) 을 진동 볼밀 (Retsch MM400) 10 · 30 · 60 분으로만 바꿔 형태 (SEM · EDX) · 기계 (박리 · 막 인장) · 전기화학 (반쪽 셀) 을 견준 실험 (계산 없음).
쪽 = 본문 인쇄 쪽 = PDF 쪽 · SI = 별도 PDF 5 쪽 · 판독 원자료 = `litdb/figures/tao2023_…/digitized.csv` (292 행 · 원 래스터 화소) · 고른 의도 대조 = **일부** (카드 §0-1 — '건식 혼합 정도 (= 시간)' 의 선례 = 채움 · 믹서 V2 의 에너지 · 순서 팔 · 혼합 지수 · SE 복합 계 = 없음 · '첫 보고' = 저자 주장).
인용 서지 (질문 k · l 용): Tao, Steinhoff, Sawicki, Sharma, Sardo, Bishtawi, Gibbs, Li, J. Power Sources 580 (2023) 233379.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 고체전해질이 없다 (액체 전해질 LIB 양극) · 압력 숫자도 없다.

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 캘린더 · 라미네이션 뒤 두께 회복 측정 없음 · 압연 조건 0 건 (카드 §0 ⑧ · §4-4 (iv)).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — SE · AM 항복 · 경도 값 0 건.
- [c] tao2023_dry_mixing_… | (값 아님 · 막의 응집 강도) 볼밀 PTFE 자립막 인장 UTS: 10 분 = 예압 0.19 MPa 단계에서 실패 (시작 ≈0.17 → 끝 ≈0.093 MPa) · 30 분 ≈0.408 MPa @ 변형 ≈0.10–0.13 % · 60 분 **0.43 MPa** (≈0.427 @ ≈0.19–0.24 %) · 곡선 끝 변형 ≈0.29 · 0.29 · 0.37 % · 응력 계단 ≈0.0185 MPa (단면 2.4 mm² 에서 ≈0.044 N) | 카드 §3-3 · p.2 · p.4 · 그림 S5 | 인쇄 (0.43 · 0.19 · 120 µm · 20 × 31 mm · 0.4 mm/min) · 판독 (나머지) · 카드 산술 (계단 → 하중) | 고분자 바인더 막의 인장 — 입자 항복 · 경도와 다른 양 · 시료 120 µm (전극 ≈153 µm 와 다름) · 반복 없음
- [c] tao2023_dry_mixing_… | (참고 · 방식 비교) Navitas 트윈스크류 압출 NMC811 막 UTS ≈2.79 MPa (92 wt% · PTFE 5 %) · ≈0.73 MPa (96 wt% · PTFE 2 %) | 카드 §3-3 · 그림 S6 · p.4 | 판독 | 다른 NMC · 랩 · 막 두께 · 시험 조건 미기재 — 통제 비교 아님

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중 · 압밀 자료 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 2D → 3D 진술 없음 (SEM 윗면 · 단면 = 2D 정성).
- [g] tao2023_dry_mixing_… | (관측 함정 · 2D 표본 위치) 전극 **윗면**에는 PTFE 섬유가 안 보이고 **단면**에만 보인다 (특히 30 분) — 저자 이유 *"higher shear at the surface disassembling the NMC secondary particles into primary particles"* · 윗면 = 조밀한 1 차 입자 층 (그림 S1) | 카드 §3-2 · p.3 · 그림 2 · S1 | 인쇄 (정성) | 2D 단면 한 장이 막 전체를 대표하지 않는다는 정성 사례 · 3D 자료 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — AM + SE 복합이 아니고 기공 숫자도 없다.
- [i] tao2023_dry_mixing_… | (참고 · SE 없는 건식 막 · 압력 미상) 세 전극을 같은 부하 (≈7.2 mAh/cm²) · 같은 두께 (≈153 µm · 그림 S1 154 · 152 · 152 µm) 로 맞춰 *"for comparable porosity"* — 겉보기 밀도 ≈2.84 g/cm³ (가정: 부하 환산 180 mA/g · 153 µm = 막 두께) · 기공은 진밀도 미인쇄로 [미확인] | 카드 §3-1 · §3-5 · §7-2 · p.2 | 인쇄 · 카드 산술 | 랩 표준 (순수 LPSCl 300 MPa 10–13 % · 1.64 g/cm³) 과 다른 문헌 값 — 판정 · 맞춤에 쓰지 않는다

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] tao2023_dry_mixing_… | 원문 스스로: *"the optimal DM time depends on the DM techniques and condition which dictate the mixing energy and heat generation. It could be different when using different DM equipment and conditions."* (p.6) · *"not only the DM, but the DM methodology and formulation can also cause a large variance in the mechanical properties of the free-standing electrodes"* (p.4) — 가압 · 탈압과 직접 닿는 원문 한계 문장은 없다 | 카드 §3-6 · `txt_p6_mechanism_summary_mixing_energy_heat.png` · `txt_p4_tse_92_96wt_nmc811_methodology.png` | 인쇄 | —
- [j] tao2023_dry_mixing_… | (카드가 적은 원문 공백) 볼밀 진동수 · 볼 · 분량 · 온도 · 투입 에너지 · 캘린더 · 라미네이션 조건 · 기공률 · 진밀도 · NMC622 입경 · 섬유화도 · 파쇄 비율 · 혼합 지수 · 반복 시료 · 오차 [미확인] | 카드 §0 한정어 · §11 · [미확인] 목록 | 카드 서술 | 혼합 이력을 우리 가압 침대 · 믹서 계산 옆에 놓을 때 에너지 · 밀도 이력 대응이 안 된다

## k — DEM 의 한계 (서지: Tao et al., J. Power Sources 580 (2023) 233379)
- [k] tao2023_dry_mixing_… (Tao 2023 · J. Power Sources) | **말 없음** — 계산 · 시뮬레이션이 없다 (본문 + SI 전수: simulation · model · DEM 낱말 0 · 모델은 Randles 등가회로 맞춤뿐).  입자 거동은 실험 해석 낱말로만: *"the NMC secondary particles were mostly intact"* · *"few NMC secondary particles are broken into primary particles"* · *"more NMC secondary particles fracture into primary particles"* · *"attributed to the grinding and its generated heat"* (p.3) | 카드 §4-4 (i) · `txt_p3_powder_morphology_fiber_fracture_heat.png` | 인쇄 | 우리 믹서 DEM (단단한 구 + SJKR CED) 이 못 내는 것 (파쇄 · 섬유화 · 발열) 의 실험 쪽 목록으로만 쓸 수 있다 — DEM 한계를 논문이 말한 것은 아니다

## l — 소성변형이 왜 어려운가 · 우회 (서지: Tao et al., J. Power Sources 580 (2023) 233379)
- [l] tao2023_dry_mixing_… (Tao 2023) | **계산 쪽 논의 없음** — 변형 이야기는 공정 · 바인더 쪽뿐: 짧은 혼합 = *"not sufficient to fully fiberize PTFE"* · 긴 혼합 = *"can break the PTFE fibers and turn them into a PTFE-carbon black film, possibly due to excessive heat"* (p.3 · p.6) · 우회 = 공정 (혼합 시간을 중간으로) · 맞춘 값 · 계산 비용 없음 | 카드 §3-6 · `txt_p6_mechanism_summary_mixing_energy_heat.png` · `txt_p3_adhesion_5_8_4_Nm.png` | 인쇄 | 고분자 섬유화 (바인더) — 입자 소성 (SE 형상 변화) 과 다른 현상 · 섬유화도 숫자 없음

## m — 받아들일 통찰
- [m] tao2023_dry_mixing_… | **혼합 팔은 관측량을 둘 이상 결과 전에 등록** — 같은 시간 축에서 접착 5 · 8 · 4 N/m · Rct 228.6 · 183.1 · 240.1 Ω · C/2 79.1 · 88.6 · 59.3 mAh/g 는 역 U (30 분 최선) 인데 막 인장은 단조 (60 분 최고 0.43 MPa) → '최적 혼합' 은 관측량 이름과 함께 말한다 | 자리: 단계 0; 결과 전 대조 항목; 흐름 밖: 믹서 V2 | 왜: 카드 §0 · §3-3 · §3-4 · §9-1 · 그림 3 · S5 · 표 S1 · S2
- [m] tao2023_dry_mixing_… | **'균일' ≠ '성질 최적'** — 세 전극 모두 EDX 에서 탄소 ↔ NMC 가 갈려 있는데 (S2–S4) 성질은 30 분 최선 · 저자 기전 = 섬유 ↔ 막 · 2 차 입자 파쇄 (정성) → 우리 조성 균일 지표 (Lacey M) 가 1 근처여도 혼합 정도가 다른 경로 (바인더 · 파쇄 · 표면 덮임) 로 결과를 바꿀 수 있다 [카드 추론] | 자리: 흐름 밖: 믹서 (지표 설계) · 후보 D0 | 왜: 카드 §7-1 · §9-2 · 그림 S2–S4 · p.3
- [m] tao2023_dry_mixing_… | **혼합 '정도' 의 단위 = 시간만이면 옮겨지지 않는다** — 저자 p.6 *"the optimal DM time depends on the DM techniques and condition which dictate the mixing energy and heat generation"* → 믹서 V2 시간 팔에 에너지 · 회전 수 · 온도 칸 · 같은 역 U 를 비에너지 (J/g) 로 준 정본 = `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` (그 카드 제목 ≈500 ± 100 J/g) | 자리: 단계 0; 흐름 밖: 믹서 V2 | 왜: 카드 §0-1 · §7-3 · §9-3 · p.6
- [m] tao2023_dry_mixing_… | **혼합은 가압 전에 AM 을 깬다 (R7) + 혼합 팔은 같은 최종 밀도에서 견준다** — 10 분 *"mostly intact"* → 30 분 *"few"* → 60 분 *"more"* 2 차 입자 파쇄 (SEM) · 세 전극 부하 · 두께를 같게 맞춘 설계 → 우리 초기 침대 AM_P 크기 분포 = 원료 PSD 라는 가정에 표지 · 혼합 → 가압 팔은 '같은 최종 기공' 과 '같은 압력' 비교를 따로 | 자리: R7; 단계 5; 단계 0 | 왜: 카드 §3-2 · §7-4 · §8 R7 · p.2–3 · 그림 1 · S1

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
litdb 확인 = 정본 `litdb/papers/` 파일 목록 611 장 (`git ls-tree`) + `git grep` (DOI · 권 · 쪽 · 제1 저자 성) — 아래 셋 모두 자기 카드 없음.  Elsevier JPS 꼴이라 원문 목록에 제목이 없다 (서지 일부만).

- [n] H. Bockholt, W. Haselrieder, A. Kwade, Powder Technol. 297 (2016) 266–274, https://doi.org/10.1016/j.powtec.2016.04.011. (원문 ref [23] · 서지 일부만 — 제목 없음) | m (흐름 밖: 믹서 V2) — *"the mixing process … dictates the homogeneity of electrode composition and fiberization of pre-polytetrafluoroethylene (PTFE) binder [13,23]"* (p.2) 의 출처 · 고강도 혼합 원전 계열 (비교 문서 H 절이 Bockholt 2013 · Meyer–Bockholt 를 이미 인용) — 카드 §12 | papers/ 에 bockholt* 없음 · 'powtec.2016.04.011' · '297 (2016) 266' · 'Powder Technol. 297' grep 0 (정본의 Bockholt 인용 = 2013 ECS Trans. · 2016 JPS 325 등 다른 논문) → 카드 없음
- [n] Y. Lu, C.-Z. Zhao, H. Yuan, J.-K. Hu, J.-Q. Huang, Q. Zhang, Matter 5 (2022) 876–898, https://doi.org/10.1016/j.matt.2022.01.011. (원문 ref [13] · 서지 일부만) | m (흐름 밖: 건식 막 공정) — 같은 문장 (혼합 → 조성 균일 · PTFE 섬유화) 의 둘째 출처 — 카드 §12 | 'matt.2022.01.011' · 'Matter 5 (2022)' · '876–898' grep 0 ('Lu, C.-Z. Zhao' = tron2023 의 다른 논문 Adv. Funct. Mater. 2021 인용) → 카드 없음
- [n] R. Tao, B. Steinhoff, X.-G.S. Sun, Kahla, B. Skelly, H. Meyer, C. Sawicki, G. Polizos, X. Lyu, Z. Du, J. Yang, K. Hong, L. Jianlin, Chem. Eng. J. (2023), doi: 10.1016/j.cej.2023.144300. (원문 ref [17] · 저자 표기 깨짐 원문 그대로 · 서지 일부만) | m (흐름 밖: 건식 공정 · 혼합 방식) — 같은 그룹 (ORNL · Navitas) 의 건식 공정 논문 · 그림 S6 의 Navitas 트윈스크류 압출 막과 같은 계열인지 [미확인] — 카드 §12 | 'cej.2023.144300' grep 0 · '144300' = `lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode` 인용만 (제목 "High-throughput and high-performance lithium-ion batteries via dry processing" 과 함께) → 카드 없음
- (참고 · 후보로 세지 않음) 원문 ref [22] A. Gyulai, W. Bauer, H. Ehrenberg, ACS Appl. Energy Mater. 6 (2023) 5122–5134 = **후보 표 N-103 에 이미 있다** (이 논문 '첫 보고' 주장의 비교 대상).

## 카드 문제
- 가리킨 카드 둘 다 **문제 없음**: `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` **L397** (ref 19 · *"Tao, R. et al. … J. Power Sour. 580, 233379 (2023)."* + '건식 혼합 정도 = 믹서 V2 선례') · `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` **L422** (ref 28 · 저자 8 명 · 제목 · J. Power Sources 580 (2023) 233379) — 원문 첫 쪽과 같고 값 인용이 없어 대조할 2 차 수치가 없다.
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §3-7 · §11 에 적음): '과혼합 = 응집 (cohesion) 약화' (p.6 · 결론) ↔ 자기 인장 자료 (60 분 UTS · 연신 최고 · p.4 · 그림 S5) · 60 분 *"diminishes the formed PTFE fibers"* (p.3) ↔ 같은 DPE-60 의 높은 UTS 를 *"degree of PTFE fibrilization can be increased"* 로 설명 (p.4) · 그림 1e '100 µm' 막대가 1a · 1c 의 2 배 길이 (127 vs 63 px · 배율 2 배) · 그림 2 캡션 '(d – e)' (= d – f) · 인장 시료 120 µm ↔ 전극 ≈153 µm · 하이라이트 'roll-to-roll' ↔ 실험실 볼밀 · '첫 보고' ↔ 자기 인용 [22] · 표 S1 'Zw' 단위 없음 · 오탈자 (*"were Ded"* · *"Ahigher"* · *"tThe"* · *"free-sanding"* · *"owing to i high toxicity"*) · 그림 S4 O 지도 큰 글자 표지 없음.
