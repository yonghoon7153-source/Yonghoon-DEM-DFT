# batch 127 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 N-78)

대상: `nam2018_dry_vs_slurry_mixed_electrode_binder_coverage_premixing_pouch` — Y.J. Nam · D.Y. Oh · S.H. Jung · Y.S. Jung\*, "Toward practical all-solid-state lithium-ion batteries with high energy density and safety: Comparative study for electrodes fabricated by dry- and slurry-mixing processes", *J. Power Sources* **375** (2018) 93–101 · DOI 10.1016/j.jpowsour.2017.11.031 (온라인 2017-11-23 · PDF 문서 정보의 '(2017)' 은 온라인 연도 · 인쇄 권호 연도 2018).
같은 NCM622 (LiNbO₃) · Li₆PS₅Cl · Super C65 조성에서 무바인더 막자 손혼합 펠릿 ('건식 혼합') 과 NBR · 자일렌 슬러리 시트를 견주고 (370 MPa 반쪽 셀 · 30 °C), GITT 식 (1) 로 낸 'SE 피복률' · EIS · 율 · EDXS 로 바인더의 이온 접촉 차단을 보인 뒤, 건식 볼밀 예비 혼합과 80 × 60 mm² 파우치 전셀 (492 MPa · 184 Wh/kg) · 안전 시험을 보인 실험 논문 — DEM · MPM · 계산 없음 · 기공 · 압력 곡선 없음.
쪽 = 인쇄 쪽 p.93–101 (PDF 쪽 = 인쇄 − 92) · SI p.n = SI PDF 쪽 · 판독 원자료 = `litdb/figures/nam2018_dry_vs_slurry_mixed_electrode_binder_coverage_premixing_pouch/digitized.csv` (1,046 행) · 고른 의도 대조 = **일부** (카드 §0-1 — 건식 ↔ 슬러리 비교 선행은 채움 · 'SE 층이 AM 을 감싼다' 는 원문에 없음).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 는 370 MPa 펠릿의 σ 3.2 mS/cm @ 30 °C (자일렌 노출 뒤 2.8) 뿐이고 그 펠릿의 밀도 · 두께 · 기공은 [미확인] (p.94–95 · SI 그림 S3b).
- [a] nam2018_dry_vs_slurry_… | (참고 · 순수 SE 아님) SE 층 = LPSCl 98.5 + NBR 1.5 wt% 의 겉보기 밀도 7.5 mg/cm² ÷ 45 µm = 1.67 g/cm³ (펠릿 전셀 · 370 MPa) · 4.9 ÷ 30 µm = 1.63 g/cm³ (파우치 · 492 MPa) | 카드 §3-8 · §7-2 · 표 2 (`tab_2.png`) | [카드 산술] (인쇄 부하 · 두께) | 진밀도 · 기공 미인쇄 · 두께 측정법 [미확인] · 랩 표준 진밀도 1.64 옆에 두면 기공 ≈ 0 으로 읽히지만 판정하지 않음

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 · 되돌아옴 측정 없음 (표 2 두께의 측정 시점 · 방법 [미확인] · 그림 8a 단면 SEM 의 "SE layer (~30 µm)" 뿐).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 기계 물성 값 없음.  정성 문장만: 황화물의 *"deformability"* (p.94 · 인용 [6,16,27]) — 질문 l 에 옮김.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.  원문의 '2D contacts' 는 **면 접촉** (점 접촉의 반대말) 을 뜻하는 실험 서술이다 (p.94 · p.95).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산이 없고, '2D contacts' 는 차원이 아니라 접촉 꼴 (면) 의 말이다.  영상은 2D (상단 · 단면 SEM/EDXS) 뿐 · 3D 재구성 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 압력 한 값 (370 MPa 반쪽 셀 · 492 MPa 파우치) · 기공 미인쇄.
- [i] nam2018_dry_vs_slurry_… | 전셀 양극 겉보기 밀도 2.39 g/cm³ — 펠릿 (79.2/19.5/1.3/0 wt% · 37 mg/cm² · 155 µm · 370 MPa) 과 파우치 (68.1/29.2/1.3/1.4 · 21 mg/cm² · 88 µm · 492 MPa) 가 같은 값 | 카드 §3-8 · 표 2 | [카드 산술] (부하 ÷ 두께) | NCM622 진밀도 미인쇄 → 기공으로 바꿀 수 없음 · 조성 · 압력 · 측정법이 다 달라 비교 의미 없음

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] nam2018_dry_vs_slurry_… | 최고 피복 25.2 % 는 *"incompleteness of solid-solid contacts between active materials and SEs"* · NCM 내부 미세 공극 (SE 접근 불가 [54,55]) · 식의 *"inaccurate factors"* 탓일 수 있다 | 카드 §0 ⑩ · §3-5 · p.97 (`txt_p97_gitt_coverage_25p2.png`) | 인쇄 (원문 문장) | 가압 접촉의 불완전성을 저자가 인정 — 압력 의존은 재지 않음
- [j] nam2018_dry_vs_slurry_… | 예비 혼합의 고율 무이득 = SE σ 부족 + *"Damage to SEs by mechanical impacts during the premixing process also cannot be ruled out"* · *"Further optimization … will be our next mission"* | 카드 §3-6 · p.99 (`txt_p99_premix_coverage_highrate.png`) | 인쇄 | 손상 여부 측정 없음
- [j] nam2018_dry_vs_slurry_… | 안전성은 *"more sophisticated and elaborate experiments are required to make a fairer evaluation of safety performance in terms of quantitative analysis"* | 카드 §3-9 · p.100 (`txt_p99_safety_cut_heat_111c.png`) | 인쇄 | 가압 · 탈압과 무관

## k — DEM 의 한계
- [k] nam2018_dry_vs_slurry_… (Nam · Oh · Jung · Jung 2018, J. Power Sources 375, 93–101) | **말 없음** — DEM · 시뮬레이션이 없다.  DEM 의 '단단한 구 · 점접촉' 가정과 맞닿는 실험 전제 문장만 있다: *"it is extremely challenging to form favorable two dimensional (2D) contacts with active materials because of their brittleness [27]"* (산화물) ↔ *"deformability of sulfide SE materials allows the formation of 2D contacts with active materials using a simple pressing process at room temperature, without the use of Li-ion conducting organic additives [6,16,27]"* (황화물) | 카드 §4-4 · p.94 (`txt_p94_oxide_brittle_sulfide_deformable.png`) | 인쇄 (인용 근거 · 이 논문 측정 아님) | DEM 한계의 직접 근거로 쓰지 않는다 — '황화물 접촉은 면' 이라는 전제의 인용 사슬 (원 출처 [27] = `sakuda2013_sulfide_mechanical_property`)

## l — 소성변형이 왜 어려운가 · 우회 · 비용
- [l] nam2018_dry_vs_slurry_… (Nam · Oh · Jung · Jung 2018, J. Power Sources 375, 93–101) | 소성 계산의 어려움 · 우회 · 비용에 대한 말 없음 (계산 없음).  소성의 **실험적 결과** 를 전제로만 쓴다: 위 k 의 '황화물 변형성 → 상온 가압만으로 면 접촉' 문장 · 그래도 잰 피복은 최대 25.2 % (*"incompleteness of solid-solid contacts"* p.97) → 변형성 SE 를 370 MPa 로 눌러도 활물질 표면의 전기화학 접촉은 부분적 | 카드 §0 ④ · §4-4 · p.94 · p.97 | 인쇄 + [카드 추론] (두 문장의 대비) | 압력 · 형상 · 변형량 측정 없음 · 피복은 전기화학 정의 (질문 m ①)

## m — 받아들일 통찰
- [m] nam2018_dry_vs_slurry_… | ① **관측량 정의**: GITT '피복' = 식 (1) 접촉 면적 ÷ BET = **1.2355 × (ΔE_s/ΔE_t)** — 질량이 지워지고 D^(−1/2) (액체 셀 D) · V_M/M (NCM111 V_M · Li 뺀 M) · BET 분모 (내부 표면 포함) 에 걸린 전기화학 양 → 우리 기하 피복 (DEM Hertz ≈18 · Tabor ≈52 % · MPM 띠) 과 절대값 비교 금지 · 같은 논문 안 비로만 · 자리 = 단계 7 · 단계 0 (정의를 결과 전에) | 카드 §3-5 · §4-2 · §7-3 · 식 (1) (`eq_01_gitt_contact_area.png`) · p.95 | [카드 산술] (원문 상수로) | 원문은 이 축퇴를 적지 않음 (저자는 'inaccurate factors' 만)
- [m] nam2018_dry_vs_slurry_… | ② **혼합 경로 폭**: 같은 조성 · 같은 압력에서 공정 경로만으로 전기화학 접촉 0.45–0.91 배 (슬러리/건식) · 1.62 배 (예비 혼합/없음) · R₂ 1.6–4.4 배 → 우리 무작위 초기 침대 (혼합 축 없음) 결과를 실전극과 견줄 때 공정 불확도로 적는다 · 자리 = 흐름 밖: 믹싱 (Ⓒ) · 결과 전 대조 항목 | 카드 §3-2 · §7-1 · 표 1 · 비교 문서 §H | 인쇄 + [카드 산술] | 바인더 · 용매 · 건조 · 시트화가 함께 바뀐 결합 효과
- [m] nam2018_dry_vs_slurry_… | ③ **검증 시험 (방향)**: 부하 1.4 배에서 용량비 (H/L) 가 SE wt% ↓ 일수록 작다 (건식 0.96 · 0.96 · 0.65 = 149/155 · 146/152 · 85/130) · 저자 *"bottleneck in overall kinetics for the thicker electrodes relates to Li-ion transport in the SE regions"* → 우리 σ_ion · tau2 · STEP4 에서 'SE 비 ↓ × 두께 ↑' 교차가 같은 방향인지 결과 전 대조 · 자리 = 단계 7 · 흐름 밖: 수송 대조 | 카드 §0 ⑥ · §8 · p.95 · p.101 (`txt_p100_conclusion_bottleneck.png`) | 인쇄 + [카드 산술] | NCM622 · 손혼합 · 30 °C · 절대값 전이 금지
- [m] nam2018_dry_vs_slurry_… | ④ **함정 (보고)**: 본문 ↔ 표 · 그림이 어긋난다 — 예비 혼합 92 → 129 (본문) vs 95 → 127 (표 1 · 그림 7d) · 전셀 시험 온도 뒤바뀜 · '0.1C = 0.17 mA g⁻¹' (1C = 1.7 mA/g 로는 용량 불가) · 예비 혼합 비교 부하 20 ↔ 22 mg/cm² → 이 논문을 인용할 때 표 1 · 2 값을 쓰고 부하 차를 적는다 · 자리 = 흐름 밖: 문헌 인용 규약 | 카드 §3-10 | 인쇄 + [카드 산술] | —

## n — 논문 에이전트 후보 (원문 참고문헌 목록 서지 그대로 · papers/ 목록 + grep 으로 카드 없음 확인)
- [n] [16] K.H. Park, D.Y. Oh, Y.E. Choi, Y.J. Nam, L. Han, J.-Y. Kim, H. Xin, F. Lin, S.M. Oh, Y.S. Jung, Adv. Mater 28 (2016) 1874–1883. | m ① — GITT 접촉 면적 (식 1) 피복 정의의 첫 인용 · LiNbO₃ 코팅법 · EIS 해석 (카드 §12) | papers/ 에 park2016 없음 · '1874' grep = miss2026 · kaiser2018 이 인용만
- [n] [21] D.H. Kim, D.Y. Oh, K.H. Park, Y.E. Choi, Y.J. Nam, H.A. Lee, S.-M. Lee, Y.S. Jung, Nano Lett. 17 (2017) 3013–3020. | m ② · j — '바인더가 접촉을 막는다' 해석 · 펠릿의 기계적 불안정의 출처 (카드 §3-2 · p.95 [21]) | papers/ 에 kim2017 없음 · '3013' grep = lee2024 등 인용만
- [n] [22] Y.E. Choi, K.H. Park, D.H. Kim, D.Y. Oh, H.R. Kwak, Y.-G. Lee, Y.S. Jung, ChemSusChem 10 (2017) 2605–2611. | m ① — GITT 피복 식의 세 번째 인용 (같은 그룹 · 같은 정의) | papers/ 에 choi2017 없음 · '2605–2611' grep 0 건
- [n] [54] R. Koerver, I. Aygün, T. Leichtweiß, C. Dietrich, W. Zhang, J.O. Binder, P. Hartmann, W.G. Zeier, J. Janek, Chem. Mater 29 (2017) 5574–5582. | j · R7 — NCM 내부 미세 공극 · 접촉 손실 (피복이 낮은 이유 후보 · p.97) | papers/ 에 koerver2017 없음 (`koerver2018_*` 은 다른 논문) · 여러 카드가 인용만
- [n] [39] W. Zhang, D.A. Weber, H. Weigand, T. Arlt, I. Manke, D. Schröder, R. Koerver, T. Leichtweiss, P. Hartmann, W.G. Zeier, J. Janek, ACS Appl. Mat. Inter 9 (2017) 17835–17845. | i · m ③ — 'SE 영역의 긴 Li⁺ 경로' (조성 · 두께 효과 · p.95 [38,39]) | papers/ 에 zhang2017 없음 · '17835' grep = choi2018 · lee2024 · ncube2026 이 인용만

## 카드 문제
- `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` **L274** (참고문헌 표 · ref 18): *"건식 vs 슬러리 혼합 · "SE 층이 AM 을 감싼다" 의 인용 원전"* — Nam 2018 원문은 SE 가 AM 을 감싼다는 것을 측정 · 문장으로 보이지 않는다 (본문 = *"SEs make 2D contacts with active materials"* p.95 · GITT 피복 5.8–25.2 % · *"incompleteness of solid-solid contacts"* p.97 · 감싼 그림은 예비 혼합 모식도 그림 7a 뿐 · 그 실측 피복 9.4 %).  그 카드 본문에 ref 18 이 그 문장에 쓰인 자리가 없다 — Hippauf 원문의 ref 18 위치 [미확인 · PDF 없음].  고치지 않음.
- `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` **L103**: *"슬러리 바인더는 σ 를 "easily drops by a factor of 10" (refs 18 · 33)"* — Nam 2018 원문에 '10 배' 값이 없다 (R₂ 비 1.6–4.4 [카드 산술] · 자일렌 노출 σ −12.5 % · 피복 비 0.45–0.91).  Hippauf 문장을 옮긴 줄이라 카드 오류는 아니나, Nam 2018 을 ×10 의 근거로 인용하면 안 된다 (ref 33 쪽 값일 수 있음 [미확인]).  고치지 않음.
- (가리킨 카드 밖) `doux2020_pressure_effects_sulfide_se_jmca` **L329**: *"대면적 셀 · 낮은 적층압"* — 대면적 (80 × 60 mm²) 은 맞지만 운전 중 적층압은 Nam 2018 원문에 서술 · 값이 없다 (제조 가압 492 MPa 만).  Doux 원문의 문장 [미확인].  고치지 않음.
- `lee2024_shear_force_dry_process_cathode_coverage` **L392** · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` **L332**: 서지 · '건식 vs 슬러리 혼합 비교 (선행)' 모두 원문과 같음 — 문제 없음 (다만 Nam 의 '건식' = 무바인더 막자 손혼합).
