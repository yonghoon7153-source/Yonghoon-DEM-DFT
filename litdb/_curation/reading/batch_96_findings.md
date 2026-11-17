# 배치 96 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-17 · 위시 W-1117-5)

카드 = `chung2008_dem_parameters_bulk_behaviour_confined_compression` (원문 = 출판본 14 쪽 (인쇄 pp. 83–96 = PDF p.2–15 · p.1 = Taylor & Francis 표지) · SI 안내 없음 · 그림 크롭 54 장 = 도구 14 (그림 1–12 + 표 1–2 → 그림 12 장 모두 원 래스터에서 다시 자름 · 표 2 장은 도구가 쪽 전체를 잘라 손으로) +
손 크롭 40 (패널 18 · 식 2 (번호 1–2 전부) · 근거 문단 20 — 본 뒤 다시 자름 14) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 118 행).
서지 (k · l 인용용) = Chung Y. C., Ooi J. Y., *Influence of Discrete Element Model Parameters on Bulk Behavior of a Granular Solid under Confined Compression*, Particulate Science and Technology 26 (1) (2008) 83–96, DOI 10.1080/02726350701759381 (T&F 표지 인용 줄은 '(2007)').
⚠ 재료 = **유리구슬 Ø10 mm 단분산 구 · 옥수수 낟알 (겹친 구 4 개)** (LPSCl · NCM 없음) — 계산 = PFC3D 3D DEM (Hertz-Mindlin 탄성 무점착) + 같은 장치 구속 압축 실험 · ≤ ≈61 kPa · 싣기만 (하중 제거 · 기공 · 소성 없음).  쪽 = 인쇄 쪽.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

이 배치에 없음 (SE 없음 · 기공 · 밀도 값 0 — 유리 초기 기공 어림 38.5 % · 옥수수 32.9 % 는 카드 산술 (높이 = 실험 평균 · 명목 지름 · 무게 환산 가정 · 0 압력 · 다른 재료) · 카드 §3-6).

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] chung2008_… | **하중 제거 · 되돌아옴 계산 · 측정 없음** — 그림 8 = 싣는 곡선만 · *"the glass beads displayed more sudden unloadings especially for higher interparticle friction … The experiments did not show any significant unloading for both materials"* = **싣는 동안의 힘 급락** (원문 추정 원인 = DEM 50 vs 실험 1.5 mm/min) | 카드 §0-1 · §3-5 · p.93 | [인쇄] | 'unloading' 은 이 뜻으로만 나온다 — 탈압 근거로 쓰지 않는다

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] chung2008_… | 항복 · 경도 · 크리프 **값 없음** · 탄성 입력만: 유리 E 41 GPa (CoV 4.0 %) · ν 0.22 (제조사) / 옥수수 E 1660 MPa (CoV 31.0 %) · ν 0.40 (ASAE 1996) · E 측정법 = **단입자 압축 + Hertz 접촉 가정** (옥수수 = 접촉점 두 곡률을 레이저 스캐너로) | 카드 §3-2 · p.87 · Table 1–2 | [인쇄] | 일축 항복 환산 없음 · 재료가 유리 · 옥수수

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (단일 재료 침대뿐 · 강성이 다른 두 재료는 따로 시험 — 유리가 옥수수보다 *"over 20 times stiffer"* (E 비 24.7 [카드 산술]) 이라 입자 간 미끄럼이 모자라 마찰 효과가 안 나타났다는 비교뿐 · p.94 · 카드 §3-5).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

- [e] chung2008_… | 대안 법칙 **없음** — Hertz-Mindlin no-slip (Tsuji et al. 1992) + 감쇠 + Coulomb 미끄럼 · 큰 변형 · 유효 범위에 대한 말 없음 | 카드 §3-2 · §4-3 · p.85 | [인쇄] | kPa · 탄성
- [e] chung2008_… | 강성을 1/10⁴ 로 낮춘 런의 겹침 어림: 유리 0.0001G₀ δ/d ≈0.10 · 옥수수 0.0001G₀ δ ≈11 mm ≈ d (Hertz 유효 범위 밖) · 유리 G₀ δ/d ≈2 × 10⁻⁴ — 원문에 겹침 값 없음 | 카드 §3-4 · §3-6 | [카드 산술 · 어림 · 접촉력 = σd² · R* 2.5 / 1.6 mm 가정] · [미확인 (원문 겹침)] | 원문은 이 런을 감도 시험으로만 쓴다 — 물리 상태 아님

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

이 배치에 없음 (MPM · 연속체 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] chung2008_… | 3D (PFC3D) · 2D 는 충전 민감도 근거로만 인용: *"Bout and McPherson (2002) performed 2-D discrete element simulations and compared different methods of particle deposition … Their simulation results indicated that different packings may cause very different behaviors albeit with identical contact parameters"* | 카드 §4-4 (iii) · p.87 | [인쇄] | 2D → 3D 전이에 대한 말 없음 · 참고문헌 표기는 'Boutt' (본문 'Bout')

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (전지 재료 · 기공 값 없음).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] chung2008_… | 입도 분포를 안 넣었다: *"The DEM simulations in this study assumed monodispersed particles although small particle size variation did exist in the physical experiments. The influence of polydispersity should be further investigated."* | p.94–95 · 카드 §4-4 | [인쇄] | —
- [j] chung2008_… | 판 속도 33 배: *"the higher rate may introduce a larger degree of local force fluctuations. Further investigation into the rate effect is being conducted."* | p.86 | [인쇄] | 하중 곡선의 힘 급락 원인 후보로 원문이 지목 (p.93)
- [j] chung2008_… | 구가 왜 안 맞는지 모름 · 충전 분석 필요: *"It is not totally clear why spherical assemblies produced poorer match with experiments. A more thorough investigation of the influence of initial packing on the loading behavior is needed."* · *"Analysis of the packing structure and force transmission is needed to provide further insight"* | p.90 · p.88 | [인쇄] | —
- [j] chung2008_… | 체 낙하 채움을 모사하지 않음 (*"large and impractical"*) → 격자 'switched on' 근사 | p.86 | [인쇄] | 출발 상태 근사의 감도는 생성 간격 · 결정 충전 비교로만 확인

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] chung2008_… (Chung & Ooi 2008, Particulate Sci. Technol. 26, 83–96) | **완전 구 = 부적절**: *"One explanation is that the DEM model of perfect spheres with perfect symmetry, which have a tendency to form crystalline structure and a tendency to spin more than nonspherical particles, is not an appropriate representation even for the uniform glass beads with their slight natural imperfections. This cast doubt on many of the DEM studies in the literature based on perfect spheres."* | p.95 (결론 1) · 카드 §4-4 (i) | [인쇄] | 근거 = 유리구슬 DEM 의 K · μbulk 불일치 (K 0.66–0.70 ↔ ≈0.4 [판독]) · 원인은 가설
- [k] chung2008_… (Chung & Ooi 2008) | **입력값이 흔히 재지 않고 가정된다**: *"In many DEM studies, the input parameters were often not measured and the values were sometimes assumed without any proper justification."* (초록) · *"the input parameters used in DEM simulations were often given without any explanation as to where they came from and seldom measured in laboratory tests, so the influence of the model parameters on the prediction outcomes can be rather obscure"* (서론) | p.83–84 | [인쇄] | '보정값이 물성이 아니다' 의 반대편 진술 (그래서 직접 잼)
- [k] chung2008_… (Chung & Ooi 2008) | **구 DEM 은 실험과 안 맞았다**: *"the DEM simulations produced a reasonable agreement with the experiments for the corn grains but not for the glass beads"* | p.90 | [인쇄] | 유리 · 옥수수 · kPa
- [k] chung2008_… (Chung & Ooi 2008) | **강성은 벌크 강성을 직접 정한다** (연화의 대가): *"As expected, the bulk stiffness in confined compression was directly influenced by the particle stiffness."* · *"Reducing the particle stiffness by a few orders only has secondary effects on the load transmission in the quasi-static assembly, while providing a huge computational advantage."* | p.91 · p.95 | [인쇄] | '부차' = 벽 · 바닥 힘 전달에 한정 · 유리는 그것도 0.74 → 0.57 [판독]
- [k] 겹침 상한 · 상대밀도 · 접촉 독립 가정이 깨지는 밀도 = **말 없음** (kPa 영역).

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] chung2008_… (Chung & Ooi 2008) | **소성 · 형상 변형 다루지 않음** (탄성 Hertz-Mindlin · 형상 = 구 / 겹친 구 4 개 고정) · 강성을 낮추는 우회는 소성 대리가 아니라 **계산 시간** 때문: *"Particle stiffness is sometimes reduced in DEM simulations to reduce computational time, since the critical time step is inversely proportional to √G"* · G₀ → 0.01G₀ · 0.0001G₀ (유리 G 16.8 GPa → 1.68 MPa · 옥수수 0.593 GPa → 59.3 kPa [카드 산술]) | p.90 · 카드 §3-2 · §3-4 | [인쇄] · [카드 산술] | 맞춘 값 0 (모두 측정 · 입자–입자 μ · e 만 가정) · 검증 = 같은 장치 실험 4 회 · 계산 비용 [미확인] ('computationally very intensive' · 'huge computational advantage' 뿐) · 입자 수 3,591 · 4,672

## m — 받아들일 통찰

- [m] chung2008_… | **연화의 효과를 두 칸으로**: 벌크 강성 · 압축 변위 = '직접' (790 N 변위 7.27 → 10.25 → 36.83 mm) ↔ 경계 힘 전달 = '부차' (바닥 몫 유리 0.74 → 0.57 · 옥수수 0.64 → 0.69) · 우리 18 배 연화는 '직접' 쪽 (기공) 에 맞춘 보정값 — 이 논문으로 '연화해도 결과 불변' 을 말하지 않는다 | 후보 D0 · 단계 4 | 카드 §3-4 · §7 · p.91 · p.95
- [m] chung2008_… | **출발 상태 감도 팔**: 단분산 구에서 생성 간격 1.01d ↔ 1.50d 만으로 바닥 힘 1.26 배 (578 ↔ 458 N · 동원 벽 마찰 0.080 ↔ 0.141) · 결정 충전 (FCC · Rhombic) 은 바닥 몫 0.75 · 0.85 ↔ Random 0.58 [판독] → 단분산 SE 덱 · 정착 단계에 '간격 두 개 + 결정화 검사' 를 결과 전에 | 단계 4 | 카드 §3-3 · 그림 3 · 5
- [m] chung2008_… | **정착 판정 = 힘 비**: 운동 에너지 < 10⁻⁸ J + 평균 불균형 힘 < 10⁻⁶ N (한 알 무게 1.3 × 10⁻² N 의 7.7 × 10⁻⁵ [카드 산술]) — 단위 없는 문턱으로 우리 정착 · 판 정지 판정을 결과 전에 등록 | 단계 0 | 카드 §3-2 · p.86
- [m] chung2008_… | **경계 관측량 + 자기 점검**: K = σH/σ̄V · μbulk = τ̄/σH (식 1–2 · 원문 '근사') · 링 구간 벽 마찰 · 바닥 몫 ↔ Janssen exp(−4Kμh/D) (실험 K · μ 로 49 · 65 % = 본문 50 · 65 % · DEM 결정 충전 0.003 안 [카드 산술]) · 'sudden unloadings' = 빠른 판 속도의 힘 급락 → 우리 하중 · 언로딩 곡선에서 먼저 의심 | 결과 전 대조 항목 · 단계 6 | 카드 §3-6 · §4-1 · p.85 · p.93

## n — 논문 에이전트 후보

litdb 확인 = 정본 `litdb/papers/` 599 장 (`ls`) + grep (제1 저자 성 · 제목 낱말 · 권 · 쪽) — 다섯 모두 자기 카드 없음 · 위시에도 없음 (O'Sullivan & Bray 2004 는 morrissey2013 참고문헌 표에만).

- [n] Chung, Y. C. 2006. Discrete element modelling and experimental validation of a granular solid subject to different loading conditions. PhD diss. University of Edinburgh, UK. | e · l · m · 후보 D0 — 벌크 강성 ↔ 입자 강성 관계식 (*"have been derived from these results (Chung, 2006)"* p.91 · 이 논문에 식 없음) · 속도 효과 · 측정 절차 전부 · 카드 §3-4 · §12 | litdb 확인: `ls` chung* 없음 · 'experimental validation of a granular solid' grep 0 건 → 카드 없음
- [n] Chung, Y. C. & J. Y. Ooi. 2006. Confined compression and rod penetration of a dense granular medium: Discrete element modelling and validation. In Modern Trends in Geomechanics, ed. by W. Wu and H. S. Yu. Berlin: Springer, 223–239. | e · m — 같은 시험 + 관입 · coetzee2017 의 'Chung & Ooi [161] 구형 캡 로드 관입 · 강성 ÷10⁴' 의 정체 (그 카드에 서지 없음) · 카드 §12 · 카드 문제 | litdb 확인: 'rod penetration' grep = nairn2015 (MPM · 다른 뜻) 뿐 → 카드 없음
- [n] O'Sullivan, C. & J. D. Bray. 2004. Selecting a suitable time step for discrete element simulations that use the central difference time integration scheme. Eng. Comput. 21 (2–4): 278–303. | m — 임계 시간 간격 × 0.20 규칙의 원전 (p.85) · 우리 DEM 시간 간격 규칙과 대조 · 카드 §3-2 | litdb 확인: `ls` 'sullivan' 없음 · 'Selecting a suitable time step' grep = morrissey2013 참고문헌 표뿐 → 카드 없음
- [n] Boutt, D. & B. McPherson. 2002. The role of particle packing in modeling rock mechanical behavior using discrete elements. In Discrete Element Methods: Numerical Modeling of Discontinua: Proceedings of the Third International Conference September 23–25, 2002, Santa Fe, New Mexico, ed. by B. K. Cook and R. P. Jensen. Reston, Va.: American Society of Civil Engineers. | g · 단계 4 — 같은 접촉 매개변수에서 퇴적 방법만으로 거동이 달라진다는 2-D 근거 (p.87) · 카드 §4-4 (iii) | litdb 확인: 'Boutt' · 'McPherson' · 'role of particle packing' grep 0 건 → 카드 없음
- [n] Chung, Y. C., J. Y. Ooi, & J. F. Favier. 2004. Measurement of mechanical properties of agricultural grains for DE models. Paper presented at 17th ASCE Engineering Mechanics Conference, Newark, N.J. | c · m — 단입자 압축 + Hertz 로 E · 세 입자 미끄럼 μ · 낙하 시험 e 의 절차 (p.87 'Details … can be found in Chung et al. (2004)') = 직접 측정 입력의 원전 · 카드 §3-2 | litdb 확인: 'agricultural grains for DE' grep 0 건 · 'Favier' grep = ai2011 · jadidi2023 (다른 Favier 인용) → 카드 없음

## 카드 문제

- `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` L458 (참고문헌 표) — 이 논문의 litdb 칸 *"없음 (`coetzee2017_*` 가 인용만)"* 은 정본 coetzee2017 카드로 확인되지 않는다: 그 카드 §7 표 (L224) 의 *"Chung & Ooi [161] | 구형 캡 로드 관입 | ÷10⁴ | 평균 관입력 둔감, 단 힘 요동 크기 감소"* 는 관입 시험 — 이 논문에는 관입이 없다 → 다른 Chung & Ooi 논문 (예: 참고문헌의 2006 'Confined compression and rod penetration' 장) 으로 보인다 [카드 추론] · coetzee2017 카드에는 [161] 서지가 없다 [미확인].  같은 꼴이 `wishlist.md` L113 (*"coetzee2017 · 이 카드가 언급만"*).  (고치지 않음)
- `morrissey2013_…` L458 · `wishlist.md` L113 — 서지 연도 '(2007)' = T&F 표지 인용 줄과 같지만 인쇄 호 머리는 *"Particulate Science and Technology, 26: 83–96, 2008"* (p.83) → 새 카드 slug = 2008.  내용 요약 (구속 압축 DEM 매개변수 민감도 · 충전 의존) 은 원문과 맞다.  (고치지 않음)
- 새 카드 자체 — 원문 안 어긋남 7 건은 카드 §3-7 · `figures.json` note_manual (벽 구간 수 · 높이 ↔ 그림 10 점 간격 · 강성 연구 유리 생성 미기재 (그림은 1.01d) · Bout/Boutt · 0.24/0.244 · EDEM 그림 ↔ PFC3D 계산 · 2007/2008 · 'respectively' 순서).
