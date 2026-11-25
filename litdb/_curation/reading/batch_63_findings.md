# batch 63 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct` — T. M. M. Heenan, A. Wade, C. Tan, J. E. Parker, D. Matras, A. S. Leach, J. B. Robinson, A. Llewellyn, A. Dimitrijevic, R. Jervis, P. D. Quinn, D. J. L. Brett, P. R. Shearing, "Identifying the Origins of Microstructural Defects Such as Cracking within Ni-Rich NMC811 Cathode Particles for Lithium-Ion Batteries", *Adv. Energy Mater.* 10 (47), 2002655 (2020), DOI 10.1002/aenm.202002655 (후보 표 N-20 · 고른 의도 = 조건 R7 출발 상태 · 질문 l).
캘린더링된 상용 NMC811 시트 둘 (NEI · LG MJ1) 을 X 선 나노 · 마이크로 CT 와 싱크로트론 XRD/XRF 로 운전 전 · 흑연 상대 5 사이클 (4.2–4.5 V) 뒤에 본 실험 영상 논문 — 역학 시험 · 압력 · 모델 계산 없음 · SE 없음 (액체계 LIB).
쪽 = PDF 쪽 = 인쇄 "(n of 13)" · SI 는 PDF 쪽 (SI 인쇄 쪽 = PDF − 1).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 없음 · 압력별 측정 없음).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (하중 · 탈압 실험 없음 — 캘린더링 **뒤** 상태만 무하중 CT 로 봄 · 캘린더링 압력 · 되튐 미기재 p.4).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (값 0 개). 원문의 '소성' 은 한 문장 — 알루미늄 집전체: *"several particles have been pressed into the current collector, suggesting that (at least locally) the calendaring pressure was high enough to exceed the yield point of Al and plastically deform the dense metal current collector sheet."* (p.4 · Al 항복값 없음) · NMC 경도 · 항복 · 크리프 서술 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 정성뿐 — 입자가 집전체에 박혀 Al 을 소성 변형 (AM 이 하중을 집전체로 전달 · p.4) · 두꺼운 고로딩 전극에서 *"the likelihood of particles stacking and forming localized stress peaks would be higher"* (저자 가설 · p.4) → 상용 (두꺼운) 쪽 shatter 7.0 ↔ 3.2 % · multi-prong 8.2 ↔ 5.4 % (Table 1) | 카드 §7.2 ③ · §8 (R1) · 논문 p.3–4 · Table 1 | [인쇄] · 가설 | 하중 몫 값 없음 · 무른 상 = 결합제 · 탄소 (SE 아님) · 압력 미상

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙 · 모델 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 아님). (참고 · f 아님: 영상 해상도 ↔ 통계 상충 — *"there is a trade-off between resolution and statistical representation"* p.3 · 결함 입자를 1200 nm 복셀로 묶어도 회색값 분산으로 구분 (Fig. 2d) — 영상 쪽 해상도 규칙이지 계산 격자 규칙이 아니다.)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (2D → 3D 전이 서술 없음). 측정 차원만: 3D CT · 표시 = 2D 직교 단면 · 그림 4 = **2D XRF 지도의 입자 전체 평균** ↔ 그림 5 = **XRF-CT** (속 정보 · p.7) — 2D 평균이 입자 속 Mn 변동 (균열 양옆 4 → 6 %) 을 지운다는 함의는 카드 해석.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (DEM · FE · MPM 계산 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (SE 없음 · 전극 기공률 · 밀도도 미기재). 관련 값 (i 아님): **AM 2차입자 안 1차입자 사이 공극** 사이클 전 13.5 % · 4.5 V 5 사이클 뒤 19.6 % (Fig. 7d [판독] · 32 nm · 서로 다른 두 입자) — 복합 양극 기공률을 실험과 견줄 때의 밀도 기준 문제 (카드 §7.3).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 캘린더링 변수를 저자도 모름: *"Although the exact calendaring parameters are not known to the authors"* (p.4) · 압력 ↔ 파괴는 **질문으로만**: *"is a certain critical calendaring pressure or electrode loading required in order to deteriorate a micro-crack into a shattered particle? Can we achieve similar areal loadings without surpassing this point? Future work may explore this"* (p.4) | 카드 §0 ④ · §11-B 12 · 논문 p.4 | [인쇄] | 압력별 결함 곡선 없음 → 우리 300 MPa 결과와 크기 비교 불가
- [j] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 해상도 · 대표성: *"there may be nano-particles that occupy what appears to be void-space at this resolution, artificially increasing the void-fraction"* (p.11) · *"ideally there should be tens or even hundreds of secondary particles … unrealistic with the current imaging capabilities"* (p.10) · 고전압 시료의 박리 · 거시 균열은 *"attributed to the sample preparation"* (p.4) | 카드 §3.5 · §11-B · 논문 p.4 · p.10 · p.11 | [인쇄] | 내부 공극 13.5 % 는 n = 1 · 상한 쪽일 수 있음

## k — DEM 의 한계
- [k] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct — Heenan et al. 2020 (Adv. Energy Mater. 10, 2002655) | **말 없음** — DEM · 모델을 쓰지 않는다. 다만 구 DEM 의 'AM = 치밀 · 무손상 강체 구' 가정과 부딪히는 실측을 준다: 사이클 전 2차입자도 *"neither structure is fully dense"* (p.9) · 1차입자 사이 공극 13.5 % [판독 Fig. 7d] · 캘린더링된 시트에서 *"approximately one-third of particles being defective before operation"* (p.11) | 카드 §7.2 · §7.3 · §11-C (i) · 논문 p.9 · p.11 · Fig. 7d · Table 1 | [인쇄] · [판독] | 액체계 롤 캘린더링 · 126 / 32 nm 해상도 · DEM 한계 '문장' 으로 인용하지 말고 '실측 반례' 로만

## l — 소성변형이 왜 어려운가
- [l] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct — Heenan et al. 2020 (Adv. Energy Mater. 10, 2002655) | **말 없음** — 소성 계산 · 우회 · 비용 서술 없음. 고른 의도의 *"캘린더링 중 AM 전위 활주"* 는 원문에 없다: 'dislocation' 은 p.2 에 한 번 *"this is also often described as the dislocation of primary particles, that is, the cracking and separation of primary particles"* (운전 중 Ni–Li 반자리 결함 [19] 문맥) = 1차입자 분리이지 결정 전위가 아니다 · 원문의 '소성' 은 Al 집전체 항복 (p.4) 뿐 · AM 은 균열 (취성) 범주로만 기술 | 카드 §0 ②③ · §11-C (ii) · 논문 p.2 · p.4 | [인쇄] | AM 소성 근거로 인용 금지 — 그쪽은 `stallard2022_nmc811_single_crystal_…` (슬립 띠) · `wheatcroft2023_…` (팁 밑 1차입자 소성)

## m — 받아들일 통찰
- [m] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 무엇: 'AM t = 0 무손상' 을 **두 문장으로 나눈다** — 압밀 전 분말 = 무손상 (원분말 *"minimal particle cracking"* · [18] 2차 인용 · p.2) / 압밀 뒤 = 결함은 우리 Auerbach 분류가 **만들어야 할 결과** (캘린더링된 시트 사이클 전 30.2 · 34.2 % · Table 1) · 어디: 조건 R7 · 후보 D0 · 왜: p.2 · p.3 · p.11 결론
- [m] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 무엇: 복합 양극 기공률을 실험과 견주는 표마다 **실험 밀도 기준 (결정 진밀도 ↔ 2차입자 외피 ↔ Archimedes) 과 AM 내부 공극 몫** 을 결과 전에 적는다 — 결정 진밀도 기준이면 ε_sphere 와의 차 ≈ φ_AM × 0.135 (φ 0.5–0.7 → 6.8–9.5 %p [카드 산술 · 가정]) · 어디: 단계 0 · 결과 전 대조 항목 · 왜: Fig. 7d (13.5 % [판독]) · p.9 *"neither structure is fully dense"* · `stallard2022_cathode_…` §9-5 의 열린 질문
- [m] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 무엇: 압밀 뒤 AM 파괴의 **결과 전 대조 항목 셋** — 입자 단위 결함 비율 (균열 26–34 % · 쪼개짐급 18–25 % [카드 산술]) · 범주 비 (Table 1 7 범주 ↔ Lawn 사다리 대응은 카드 해석) · 누르는 면 쪽 집중 (> 50 % · Fig. 1c 마지막 칸 64.7 % [판독]) — 방향 · 꼴만 · 입자 단위 정의를 먼저 적는다 · 어디: 단계 5 · 후보 D0 · 조건 R7 · 왜: Table 1 · Fig. 1c · p.4
- [m] heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct | 무엇: **함정 다섯** (이 논문 인용 때) — 'dislocation' = 1차입자 분리 · 'Raw' = 사이클 안 한 시트 입자 (원분말 아님) · 0.14 → 0.19 = 서로 다른 두 입자 · 결함 비율은 판정 해상도에 묶인다 (126 nm ↔ `wheatcroft2023_…` XCT 0.56 µm 의 0.7 % — 무압연 전극) · NMC811 σ_e 2.8 × 10⁻⁵ S/cm 는 인용 번호 없음 · 어디: 흐름 밖: 원고 · SI · 보고의 인용 규율 · 왜: p.2 · p.9 · Fig. 7 범례 · p.12

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] T. M. Heenan, A. V. Llewellyn, A. S. Leach, M. D. Kok, C. Tan, R. Jervis, D. J. Brett, P. R. Shearing, Adv. Sci. 2020, 7, 2000362. (원문 참고 [18] · 인쇄 그대로) | 조건 R7 · k — 원분말 (전극 제조 전) 결함 · *"minimal particle cracking"* · 내부 공극의 원전 (이 논문은 2차 인용) — 'AM 압밀 전 무손상' 의 1 차 근거 · 카드 §3.6 · §14 | litdb 확인: `papers/` 목록에 heenan* 없음 · '2000362' grep 0 건
- [n] T. M. M. Heenan, A. Jnawali, M. Kok, T. G. Tranter, C. Tan, A. Dimitrijevic, R. Jervis, D. J. L. Brett, P. R. Shearing, Data Brief 2020, 32, 106033. (원문 참고 [32] · 인쇄 그대로) | m · 흐름 밖: Material 2 (LG MJ1 양극) 영상 원자료 공개 — 실측 3D 양극 구조 (AM 결함 · 패킹) 를 우리 DEM · 결함 분류 대조에 · 카드 §2 · §14 | litdb 확인: '106033' · 'Data Brief' grep 0 건
- [n] A. Quinn, H. Moutinho, F. Usseglio-Viretta, A. Verma, K. Smith, M. Keyser, D. P. Finegan, Cell Rep. Phys. Sci. 2020, 1, 100137. (원문 참고 [28] · 인쇄 그대로) | 조건 R7 기전 — 결정 방위가 응력 · 균열을 지배한다는 근거 (p.11) · 카드 §14 | litdb 확인: '100137' = `sharma2023_…` 가 인용만 · 카드 없음
- [n] P. C. Tsai, B. Wen, M. Wolfman, M. J. Choe, M. S. Pan, L. Su, K. Thornton, J. Cabana, Y. M. Chiang, Energy Environ. Sci. 2018, 11, 860. (원문 참고 [17] · 인쇄 그대로) | 조건 R7 — 단일 입자 나노 CT 2차입자 균열 (낮은 Ni NMC) · 이 논문의 비교 원전 (p.2 · p.8) · 카드 §14 | litdb 확인: 'Tsai' · '11, 860' = `lee2024_…` 가 다른 용도 (i0) 로 인용만 · 카드 없음
- [n] Y. Mao, X. Wang, S. Xia, K. Zhang, C. Wei, S. Bak, Z. Shadike, X. Liu, Y. Yang, R. Xu, P. Pianetta, Adv. Funct. Mater. 2019, 29, 1900247. (원문 참고 [23] · 인쇄 그대로) | 조건 R7 · m — 2차입자 내부 공극이 (탈)리튬화 팽창 · 수축 응력을 덜어 준다는 근거 (p.3) — AM 내부 공극 · 역학 · 카드 §3.6 · §14 | litdb 확인: '1900247' grep 0 건 · `papers/` 에 mao* 없음
- (참고 · 후보로 세지 않음) 원문 참고 [16] Daemi 2020 PCCP 22, 17814 · [19] Lin 2020 Nano Energy 76, 105021 · [20] Märker 2019 Chem. Mater. 31, 2545 · [31] Xu 2018 JMCA 6, 21859 = 카드 없음 (카드 §14 에 서지) · [30] Daemi 2018 ACS AEM 1, 3702 = 카드 없음 (`lu2020_…` · `park2020_…` 참고 목록에 인용만 · `papers/` 에 daemi* 없음 · 세 상 분할 방법이라 a–m 직접 쓰임 약함).

## 카드 문제
- `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` L199 — *"초기 사이클 입계 균열 · 캘린더링 중 전위 활주 | p. 1, p. 6 | [17] T. M. M. Heenan … P. R. Shearing, Adv. Energy Mater. 2020, 10, 2002655."* — 서지 ✓ · 앞 절반 ✓ · **뒤 절반 *"캘린더링 중 전위 활주"* 는 원문에 없다** (원문 'dislocation' = *"the cracking and separation of primary particles"* · 운전 중 · p.2 · 캘린더링 · 슬립 · 소성 서술 0) · Wheatcroft 원문 문장은 이 트리에 PDF 가 없어 확인 못 함 — 오역이 그 원문인지 카드 요약인지 가르지 못한다 (고치지 않음).
- `stallard2022_cathode_mechanical_properties_review` L92 (+ L284 · L376 · L459) — *"NMC811 이차입자 기공 0.14 → 0.19 (5 사이클)"* = 리뷰 문장을 그대로 옮긴 것 (카드 잘못 아님) · 원문은 **그림에만** 있는 값 (Fig. 7d [판독] 13.5 → 19.6 % · 0.19 는 판독보다 0.6 %p 낮음) · **서로 다른 두 입자 (n 1 + 1)** 비교 · 32 nm · 나노입자로 과대 가능 (p.11) — 한정어가 빠짐 (경미 · 고치지 않음).
- `stallard2022_nmc811_single_crystal_shear_strength_lithiation` L337 — *"캘린더링 → 다결정 NMC 파쇄 · 미분화 (CT) — 압밀 압력 ↔ AM 파괴 (R7) · 카드 없음"* — 파쇄 · 미분화 (shatter 3.2 · 7.0 %) ✓ · '압밀 압력 ↔ AM 파괴' 는 원문에 압력 숫자가 없어 질문으로만 (p.4) · *"카드 없음"* 은 이제 낡음 (= 이 카드) — 고치지 않음.
