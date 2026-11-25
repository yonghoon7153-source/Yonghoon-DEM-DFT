# batch 102 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `lu2020_insitu_nanoct_calendering_microstructural_evolution` — X. Lu, S. R. Daemi, A. Bertei, M. D. R. Kok, K. B. O'Regan, L. Rasha, J. Park, G. Hinds, E. Kendrick, D. J. L. Brett, P. R. Shearing, "Microstructural Evolution of Battery Electrodes During Calendering", Joule 4 (2020) 2746–2768, doi:10.1016/j.joule.2020.10.010 (본문 24 쪽 + Supplemental Information 15 쪽 · 카드 = `litdb/papers/lu2020_insitu_nanoct_calendering_microstructural_evolution.md`).
리튬이온 양극 (NMC111 + 탄소-바인더 · 액체 전해질) 의 in situ 나노 CT 기둥 압축 + 영상 기반 전기화학 모델이다.  고체전해질이 없고 가압 압력이 인쇄돼 있지 않다 — 아래 '없음' 은 그 때문이다.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질이 없는 리튬이온 양극 · 진밀도 · 질량 기준 기공률 없음).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] lu2020_insitu_nanoct_calendering_microstructural_evolution | 되돌아옴을 재지 않았다.  단계 영상은 모두 핀으로 누른 채이고 마지막 단계 뒤 하중을 뺀 영상이 없다.  '뺀 뒤' 자료는 다른 시료 하나 — 롤 압연 AM_L (44.3 → 35.4 µm · '20% Cal') 의 기공률 0.203 · tortuosity 8.34 ↔ 누른 채 22.5 % 기둥의 0.188 · 8.85 (차 7.3 % · 6.1 %) | 카드 §3-2 · §3-7 · §4-4 (iv) · 논문 p.2765 · Table S3 · Fig S10 | 인쇄 | 압축률이 다르고 (22.5 ↔ 20 %) 시료 · 가압 방식이 달라 되돌아옴으로 읽을 수 없다 · 리튬이온 양극 (탄소-바인더 기지)

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (역학 물성 · 하중 측정 없음).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] lu2020_insitu_nanoct_calendering_microstructural_evolution | 하중 몫 · 응력 숫자 없음.  정성 관찰만: 큰 입자 전극 (7.3 µm · STD 3.1) 은 눌리는 동안 활물질이 회전 · 미끄럼 · 구름으로 자리를 바꾸고 (*"inter-particle sliding and rolling"*), 작은 입자 전극 (5.2 µm · STD 1.8) 은 이웃 구속으로 집단 변형 (*"high lateral constraints from neighboring particles"*).  *"even distribution of the compressive stress and strain"* 은 기공 연결성에서 끌어낸 추론 문장이다 | 카드 §3-4 · §3-5 · 논문 p.2748–2751 · Fig 1G · 1H · Fig 2 | 인쇄 (정성) | 무른 상이 고체전해질이 아니라 다공 탄소-바인더 · 옆 구속 없는 기둥 · 압력 미기록 · 응력 측정 · 계산 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙을 다루지 않는다 · DEM 을 쓰지 않았다).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).  영상 해상도 참고: 평균 기공 = AM_L 6.6 → 4.8 · AM_S 6.3 → 4.4 복셀 · 입자 지름 = 114 · 81 복셀 (64 nm · 카드 §3-2 [카드 산술]).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (영상 · 정량 · 모델 전부 3D · 전이에 대한 말 없음 — 카드 §4-4 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.  (가까운 것: 눌린 구조를 **영상** 에서 받아 유한요소 전기화학 모델의 격자로 쓴다 — Simpleware 격자 → COMSOL · 카드 §4-3 · 논문 p.2766.  입자 계산에서 넘긴 것이 아니다.)

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] lu2020_insitu_nanoct_calendering_microstructural_evolution | AM + SE 복합이 아니다 (AM + 탄소-바인더 · 액체 전해질용).  압력 대신 압축률별 기공률만 있다 — AM_L 0.330 → 0.300 → 0.250 → 0.190 (0 → 7 → 15 → 22.5 %) · AM_S 0.350 → 0.300 → 0.270 → 0.195 (0 → 8.5 (라벨 7) → 13.5 → 24 %) · 표 인쇄값 0.325 → 0.188 · 0.354 → 0.195 · 누른 채 · 영상 3 상 분할 (탄소-바인더 안 나노 기공 포함) | 카드 §3-1 · §3-2 · 논문 Table 1 (p.2757) · Fig 3I | 양 끝 인쇄 · 가운데 판독 | 압력 축 없음 · 옆 구속 없음 (고체 보존이 12–15 % 안 닫힘 [카드 산술]) · 재료가 다름 → 우리 압력별 기공과 견주지 않는다

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] lu2020_insitu_nanoct_calendering_microstructural_evolution | 원문이 건 적용 범위: 활물질 90–94 wt% · 초기 두께 < 50 µm · 압연 ≈23 % 까지 (*"for uncalendered NMC electrodes with a mass loading 90 — 94 wt % and an initial thickness less than 50 µm … calendered up to approx. 23%"*) | 카드 §0 ⑩ · 논문 p.2759 | 인쇄 | 전기화학 결론의 범위이고 가압 역학의 한계 진술은 없다
- [j] lu2020_insitu_nanoct_calendering_microstructural_evolution | 카드가 적은 한계: 가압 압력 · 하중 · 유지 · 이완 기록 없음 · 옆 구속 없는 기둥 압축을 '압연 모사' 로 씀 (근거 = Table S3 *"within 8%"* 하나) · 단계마다 시료 하나 · 재현 · RVE · 문턱 점검은 압축 전 큰 입자 전극에만 | 카드 §11 1–3 · 논문 p.2765 · Table S3 · S4 · Fig S14 | 카드 관찰 · 미확인 | —

## k — DEM 의 한계
- [k] lu2020_insitu_nanoct_calendering_microstructural_evolution (Lu 외, Joule 4 (2020) 2746–2768) | DEM 압연 계산 (ref 19 = Sangrós Giménez 외, Powder Technol. 349 (2019) 1–11) 을 두고: *"Spherical particles were used to study the mechanical responses and porosity variation of the electrode under different calendering steps.19 However, these studies were conducted based on simplified electrode geometries that were artificially synthesized with spherical particles, ignoring the influence of particle shape and orientation on mass transport and electrochemical performance. More importantly, the carbon-binder domain (CBD), which is critical in determining the microstructural heterogeneities and electronic conductivity,20,21 especially under compression, was not taken into account."* — 꼽은 한계 = 구 가정 (형상 · 방향 무시) · 인공 합성 구조 · 탄소-바인더 누락 | 카드 §4-4 (i) · 논문 p.2747 (서론) | 인쇄 | 믿을 수 있는 겹침 · 상대밀도 상한 · 접촉 독립 가정 · 보정값의 지위에 대한 말은 없다 (말 없음) · 이 논문은 DEM 을 직접 쓰지 않았다 · 리튬이온 양극 문맥

## l — 소성변형이 왜 어려운가
- [l] lu2020_insitu_nanoct_calendering_microstructural_evolution (Lu 외, Joule 4 (2020) 2746–2768) | 원문은 입자 소성을 계산에 넣기 어려운 이유를 논하지 않는다 (말 없음).  택한 우회 = 계산하지 않고 찍는다 — 눌린 실제 구조 (입자 변형 · 탄소-바인더 압축 포함) 를 나노 CT 로 얻어 수송 · 전기화학 계산의 격자로 쓴다.  맞춘 역학 값 0 개 · 대가: 한 단계 1,201 장 × 60 s ≈ 20 h [카드 산술] · 시야 64 µm (입자 지름의 9–12 배) · 전극당 시료 하나 · 응력 정보 없음 · 영상이 있는 상태만 계산할 수 있다 (조성 · 압력을 바꿔 보는 예측 불가) | 카드 §4-4 (ii) · §7-4 · 논문 p.2765–2766 | 인쇄 + 카드 산술 | 검증 = 모델 방전 곡선 ↔ NMC622 전극 한 쌍 (*"except for a noticeable discrepancy at 5C"*) · 격자 · 계산 비용 미확인

## m — 받아들일 통찰
- [m] lu2020_insitu_nanoct_calendering_microstructural_evolution | 무엇을: 이 논문 (과 TauFactor 로 잰 문헌) 의 'tortuosity' 는 tortuosity factor 다 — *"Tortuosity, also called tortuosity factor"* · Q_p/Q_b = ε/τ → 우리 표에 옮길 때 tau2 (수송 tortuosity) 열에 넣고 √ 열에 넣지 않는다.  어디에: 흐름 밖: 접촉망 수송 · tortuosity 이름 규약 (비교 문서 J 절) | 카드 §3-6 · 논문 SI p.2 식 (1)–(3) · p.2765 | 인쇄 | 기공상 · 탄소-바인더 포함 3 상 · 방향 미기재
- [m] lu2020_insitu_nanoct_calendering_microstructural_evolution | 무엇을: 영상 기공률을 대조에 쓸 때 결과 전에 적을 칸 — 분할 문턱 ±10 % → 기공률 0.288–0.353 (0.325 기준) · 시료 간 표준편차 0.016 · RVE (기공률은 부피 20 % · tortuosity 는 60 % 부터 수렴) · 누른 채 / 뺀 뒤 · 제 3 상 포함 여부.  어디에: 단계 0 | 카드 §3-7 · 논문 Fig S12 · S14 · Table S4 | 인쇄 · 판독 (RVE) | 점검은 압축 전 큰 입자 전극에만 있다
- [m] lu2020_insitu_nanoct_calendering_microstructural_evolution | 무엇을: 옆 구속 없는 기둥 압축 자료는 일축 압밀 곡선이 아니다 — 두께 감소의 81–84 % 만 기공 감소로 가고 활물질 기둥 부피 (분율 × 두께) 가 12–15 % 준다 → in situ CT 문헌을 결과 전 대조 항목으로 고를 때 '다이 안인지 기둥인지' 를 먼저 적는다.  어디에: 단계 5 (결과 전 대조 항목 선정) | 카드 §3-1 · §3-2 · 논문 Table 1 (p.2757) · Fig 3I | 카드 산술 | 분석 부피 차 · 시료 차와 가를 수 없다 (롤 압연품 AM_LH 도 12 % 안 닫힘)
- [m] lu2020_insitu_nanoct_calendering_microstructural_evolution | 무엇을: 지배 인자를 가르는 민감도 두 팔 — 고체 확산 계수를 올리면 용량이 늘고 (≈117 → ≈138 mAh/g) 반응 속도 상수를 올리면 전압만 오른다 → 한계가 확산인지 반응 면적인지 한 그림으로 가른다.  어디에: 흐름 밖: STEP4 반응분포 진단 설계 | 카드 §3-8 · 논문 Fig 6G · p.2758–2759 | 인쇄 · 눈대중 (용량) | 액체 전해질 반쪽 셀 모델 · NMC622 물성

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Daemi, S.R., Lu, X., Sykes, D., Behnsen, J., Tan, C., Palacios-Padros, A., Cookson, J., Petrucco, E., Withers, P.J., Brett, D.J.L., et al. (2019). 4D visualisation of in situ nano-compression of Li-ion cathode materials to mimic early stage calendering. Mater. Horiz. 6, 612–617. | i · l · 조건 — 같은 나노 압축 시험대의 선행판 (ref 35).  이 논문에 없는 하중 · 변위 기록 · 시험대 구속 조건이 거기 있는지 (카드 §4-1 · [미확인] 목록 첫 줄) | litdb 확인: ls 'daemi' 없음 · 'nano-compression' · '4D visualisation' · '612–617' grep 0 건 → 카드 없음
- [n] Lu, X., Bertei, A., Finegan, D.P., Tan, C., Daemi, S.R., Weaving, J.S., O'Regan, K.B., Heenan, T.M.M., Hinds, G., Kendrick, E., et al. (2020). 3D microstructure design of lithium-ion battery electrodes assisted by X-ray nano-computed tomography and modelling. Nat. Commun. 11, 2079. | m · 흐름 밖 (STEP4) — DSS 3 상 재구성과 3D 미세구조 분해 모델의 원 논문 (ref 25 · *"as described elsewhere"*) — 이 논문이 적지 않은 격자 · 영역 · 검증 세부 (카드 §4-3 · [미확인]) | litdb 확인: ls 'lu2020' = 이 카드뿐 · '11, 2079' grep 0 건 · 제목 grep = nguyen2020 · pan2026 (인용만) → 카드 없음
- [n] Usseglio-Viretta, F.L.E., Colclasure, A., Mistry, A.N., Claver, K.P.Y., Pouraghajan, F., Finegan, D.P., Heenan, T.M.M., Abraham, D., Mukherjee, P.P., Wheeler, D., et al. (2018). Resolving the discrepancy in tortuosity factor estimation for Li-ion battery electrodes through micro-macro modeling and experiment. J. Electrochem. Soc. 165, A3403–A3426. | m · 흐름 밖 (tortuosity 규약) — 영상 tortuosity factor ↔ 전기화학 측정의 불일치와 제 3 상 (탄소-바인더) 의 몫 (ref 27 · 카드 §3-6 의 '탄소-바인더를 넣으면 2.1–2.6 배' 를 실제 전극에서 확인할 자리) | litdb 확인: ls 'usseglio' 없음 · 'A3403' grep = nguyen2020 (인용만) → 카드 없음
- [n] Ebner, M., Chung, D.W., García, R.E., and Wood, V.J.A.E.M. (2014). Tortuosity anisotropy in lithium-ion battery electrodes. Adv. Energy Mater. 4, 1301278. | m · 단계 7 — 입자 형상 · 방향이 방향별 tortuosity 를 가르는 크기 (ref 30 · 이 논문은 방향을 적지 않았다 — 카드 [미확인]) | litdb 확인: ls 'ebner' 없음 · '1301278' grep 0 건 · 제목 grep = hlushkou2018 · malifarge2017 (인용만) → 카드 없음 (후보 표 N-66 은 다른 논문 = Ebner 2013)
- [n] Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W.D., and Kendrick, E. (2020). Development of experimental techniques for parameterization of multi-scale lithium-ion battery models. J. Electrochem. Soc. 167, 080534. | 흐름 밖 (STEP4 매개변수) — 이 논문이 GITT 고체 확산 계수를 뽑은 방법 (ref 52 · 카드 §3-8 · Fig S7).  메인 리포의 STEP4 기록이 'Chen2020' 이라 부르는 출처와 같은 논문인지 [미확인] — 같다면 원문 카드가 없는 채 쓰이고 있는 값이다 | litdb 확인: ls 'chen2020' 없음 · 제목 grep 0 건 · '080534' grep = 무관한 한 건 (honrao2021 의 물질 번호 mp-1080534) → 카드 없음
- (참고 · 후보로 세지 않음) ref 18 Günther 외 (2020) Energy Technol. 8, 1900026 = wishlist 에 이미 있음 · ref 12 · 13 Meyer 2018 · 2017 = 후보 표 N-61 · N-55 (차례 대기).

## 카드 문제
- `he2026_dem_calendering_inhomogeneity_areal_density` L691 — "압연 중 미세구조 진화의 **XCT operando**": 원문은 처음부터 끝까지 "in situ" 이고 (촬영 중 전기화학 없음) 'operando' 는 ref 4 의 제목에만 나온다.  같은 줄의 "소입자일수록 균일변형 · 저tortuosity" 는 원문 요약 문장 (*"more homogeneous deformation and a lower tortuosity"* · p.2746) 과 같지만 비교는 두 전극 (5.2 ↔ 7.3 µm · 분포 폭 · 형상 · 공급사 동반) 이라 '작을수록' 의 경향은 원문에 없다.  서지 (Joule 4, 2746) 는 맞다.  그 카드는 고치지 않았다.
- `lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode` L380 — 서지 원문과 같음 · 숫자 인용 없음 · 문제 없음 ('후막 미세구조 설계' = 가상 거울상 전극 ≤ 70 µm 모델 + 실험 ≤ 74 µm 라는 한정만 붙는다).
- 후보 표 N-53 의 '왜' 칸 "단계 5 (결과 전 대조 후보)" — 이 논문은 압력 · 옆 구속 · 재료 · 수송 상이 달라 대조 값을 주지 못한다 (카드 §0-1 · §8).  후보 표는 고치지 않았다 (메인 세션 소관).
