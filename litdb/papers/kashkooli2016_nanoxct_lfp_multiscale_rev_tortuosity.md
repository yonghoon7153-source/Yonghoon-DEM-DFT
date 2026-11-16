<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 1저자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 번호 · 머리 상자 · 서지 표 · 그림 표) · 계열 이웃 = lu2020_insitu_nanoct_calendering_microstructural_evolution.md
     (LIB 양극 나노 CT 위 3D 전기화학) · tjaden2018_tortuosity_review_calculation_approaches.md (같은 열유속 방법 · Cooper 2014 LFP 값이 그 카드 표에 있다) ·
     eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell.md (LFP 나노 입자 · '입자 크기 여러 개로 P2D 를 보정' 하는 같은 문제).
     쪽 표기 = 학술지 쪽 p.496–509 (PDF 쪽 = 학술지 쪽 − 495) · 보충 = SI p.1–5 (Word 에서 만든 PDF · Figure S1–S5 그림 다섯과 캡션뿐 · 본문 글 · 표 없음) ·
     보충 영상 Video 1 · 2 는 받지 않았다.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 그림 3 원 래스터 300 dpi ·
     격자선 보정 · 표식 무게중심) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 해석] = 이 카드의 해석 ·
     [미확인] = 원문 (본문 14 쪽 + SI 5 쪽 전수) 에 없음.  색 막대 끝값 (▲ 최대 · ▼ 최소) 은 그림 안 인쇄 글자 → colorbar_extremes_printed.csv.
     원문 14 쪽 · SI 5 쪽을 전부 렌더로 읽고 숫자는 텍스트 층과 대조했다 (텍스트 층은 µ 를 'm' · = 를 '¼' · – 를 'e' 로 싣고 위첨자 음수 부호를 잃는다 — 렌더로 바로잡음). -->
# 나노 X 선 CT (복셀 16 nm · 분해능 50 nm) 로 재구성한 상용 LFP 양극에서 대표 체적 (REV 750 nm) 을 잘라 3D 미시 영역으로 두고 1D P2D 거시 영역과 매 시간 걸음 양방향으로 묶은 COMSOL 다중 스케일 모델 — 실 tortuosity (열전도 유사 · 전해질 2.2472 · 고체 1.7311 = Bruggeman 의 1.42 · 1.34 배 [카드 산술]) · 비표면적 3.6 µm⁻¹ · C/10–4C 방전 대조 (3.0 V 용량 모델 ÷ 실측 1.05–1.14 ↔ P2D 1.10 → 0.73 [판독]) · 미시 Li 농도가 원문 c_max 22,800 mol/m³ 의 최대 4.6 배 [카드 산술] — Kashkooli · Farhad · Lee · Feng · Litster · Komini Babu · Zhu · Chen (J. Power Sources 2016)

> slug `kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity` · DOI `10.1016/j.jpowsour.2015.12.134` · type `image-based multiscale continuum simulation (nano-XCT reconstruction · REV · tortuosity by steady heat-transfer analogy · COMSOL Multiphysics FEM 3D microscale solid Fick diffusion ⇄ 1D P2D macroscale · concurrent two-way coupling) + experiment (LFP coin half-cell rate test) — liquid-electrolyte LIB · DEM · MPM · compaction · ASSB 0` · PDF `340d3f0b-68._Multiscale_modeling_of_lithium-ion_battery_electrodes_based_on_nano-scale_X-ray_computed_tomography.pdf` (+ SI `f45fee9b-68._Sup_Multiscale_modeling_of_lithium-ion_battery_electrodes_based_on_nano-scale_X-ray_computed_tomography.pdf`) · digested `2026-11-16` · status ✅
>
> **저자**: **Ali Ghorbani Kashkooli** (a) · **Siamak Farhad\*** (b · 교신) · Dong Un Lee (a) · Kun Feng (a) · Shawn Litster (c) · Siddharth Komini Babu (c) · Likun Zhu (d) · **Zhongwei Chen\*\*** (a · 교신) — a = University of Waterloo (Chemical Engineering) · b = University of Akron (Mechanical Engineering) · c = Carnegie Mellon University (Mechanical Engineering) · d = Indiana University Purdue University Indianapolis (Mechanical Engineering) · *J. Power Sources* **307** (2016) 496–509 (본문 14 쪽 · Appendix A = 보충 자료 · 보충 영상 2) · 접수 2015-09-19 · 수정 12-23 · 승인 12-28 · 온라인 2016-01-14 · 연구비 NSERC (Z.C.) · University of Waterloo · University of Akron · 사의 Hey Woong Park (p.496 · p.507).
> **이웃 카드 (링크만)**: [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) (LIB 양극 나노 CT 위 전기화학 · 누른 채) · [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) (열유속 τ 방법 · 이 논문 [48] Cooper 2014 LFP 값이 그 카드 표에) · [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) (같은 정의의 τ 를 영상에서 내는 도구) · [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) (CT 영상 위 정상 전도 · 접촉 저항 0 · 황화물) · [`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`](eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell.md) (LFP 나노 입자 · 다입자 모델) · [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) (이 논문을 참고 [11] 로 인용).
> **판독 원자료**: `litdb/figures/kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity/digitized.csv` (106 행 — 그림 3a · 3b 표식 무게중심 + 3.0 V 교차) · `colorbar_extremes_printed.csv` (36 행 — 그림 4 · 7 · 8 · S3 색 막대 끝값 인쇄 글자) · 그림 크롭 59 장 (도구 15 전부 다시 자름 + 손 44: 그래픽 초록 1 · 패널 8 · 그림 S3 · 표 3 · 식 14 · 근거 문단 19) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 상용 LFP/흑연 전지에서 꺼낸 LFP 양극 조각을 나노 X 선 CT (UltraXRM-L200 · 분해능 50 nm · 복셀 16 nm · 시야 16 µm) 로 찍어 문턱 이진화 · ScanIP 7 로 3D 재구성하고 (첨가제는 활물질과 따로 다루지 않음 · 영역 확장으로 이웃 활물질을 융합 · 영상 기공 40 % ↔ BET 35 %), 그 안에서 750 nm 정육면체 (REV) 를 COMSOL 의 3D 미시 영역 (고체 Fick 확산 + 가변 고체 확산계수) 으로 두고 1D P2D 거시 영역 (Li 박 / 분리막 / 양극) 과 매 시간 걸음 양방향 (concurrent) 으로 묶었다 — 거시의 Bruggeman 은 열전도 유사로 잰 실 tortuosity (전해질 2.2472 · 고체 1.7311) 로, 비표면적은 영상 값 (3.6 µm⁻¹) 으로 바꿨고, 방전 곡선 (C/10–4C) 이 P2D 보다 실측에 가깝다고 결론짓는다 — **압밀 · 역학 · 고체전해질 · 접촉 계산은 없다**.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 영상 → 이진화 → 수송용 구조 (단계 7) | nano-XCT · 분해능 **50 nm** · 복셀 **16 nm** · 시야 **16 µm** · 990 tomograms (180°) · 문턱 이진화 · 흑 = AM 덩어리 / 백 = 기공 + 첨가제 (PVDF · 탄소) · 첨가제를 AM 과 따로 다루지 않음 · 영역 확장 (growing region) 으로 이웃 AM 융합 · 기공 **40 %** (영상) ↔ **35 %** (BET) | [인쇄] p.498–499 |
| ② REV 크기 판정 | 두 기준 — (i) 가장 큰 입자 (반지름 169 nm · AM 부피의 10 % · 다른 논문 [44] 의 '비슷한' 상용 LFP 값) 하나가 들어가는 최소 부피 → **728 nm** (ii) 부분 정육면체 (283–2122 nm) 의 ε · a 가 영역 값의 3 % · 9 % 안 (> 707 nm) → **REV 750 nm** (= 가장 큰 입자 지름의 2.2 개 · 복셀 46.9 개 [카드 산술]) | [인쇄] p.499–500 · Table 1 |
| ③ 유효 물성 (τ · a · ε) | τ (식 4 D_eff = D·ε/τ) = 정상 열전도 (기공 · AM 각각 · x · y · z) 를 같은 크기 균일 비다공 시료와 비교 (Cooper [48]) · 계산 정육면체 **1.5 µm** (REV 아님) · 전해질 2.2544 / 2.4289 / 2.0844 → τ_avg **2.2472** · 고체 1.6116 / 1.8154 / 1.7794 → **1.7311** · τ_avg = 세 방향 **조화평균** [카드 산술] · 이 τ 는 우리 **tau2 (수송 tortuosity)** 자리 · κ_eff · σ_eff 에도 같은 τ · a **3.6 µm⁻¹** · ε 0.4 | [인쇄] p.500 · Table 1 · 2 · Fig S2 · [카드 산술 · 해석] |
| ④ 미시 ↔ 거시 넘김 (질문 h) | 거시 → 미시 = 세공벽 플럭스 j_n (경계 조건 식 11) · 미시 → 거시 = C₁s 로 i₀ · OCP 를 갱신한 j_n · 가정 *"the electric potential and electrolyte concentration at the interface does not change between the two scales"* · 매 시간 걸음 (concurrent) ↔ 서열 결합 (대리 모델 · 조회표) 비판 | [인쇄] p.497 · p.499 · p.501–503 · Fig 2 |
| ⑤ 검증 | 같은 상용 양극 반쪽 셀 (1.13 cm² · 1 M LiPF6 EC:DEC) 방전 C/10 · 1 · 2 · 3 · 4C ↔ 다중 스케일 (Fig 3a) · P2D (Fig 3b) — 3.0 V 용량 모델 ÷ 실측: 다중 스케일 **1.05 · 1.08 · 1.08 · 1.09 · 1.14** / P2D **1.10 · 1.03 · 0.86 · 0.75 · 0.73** (1C 에서만 P2D 가 더 가깝다) · 오차 지표는 원문에 없음 | [판독] Fig 3 · [카드 산술] |
| ⑥ 맞춘 값 | 둘 — D_LFP (**7 × 10⁻¹⁸ m²/s**) · 고체 전기전도도 σ (**0.03 S/m**) 를 *"design adjustable parameters … determined based on the method described in Ref. [50] and compared with the obtained experimental data"* · 나머지 Table 3 · 전해질 전도도 κ 값 [미확인] | [인쇄] p.501 · p.505 |
| ⑦ 원문 결과가 물리 범위를 넘는 곳 (이 카드가 찾음) | 미시 Li 농도 최댓값 4.51 × 10⁴ (1C · SOC 0.95) · 1.06 × 10⁵ (4C 방전 끝) mol/m³ = Table 3 c_max 22,800 의 **1.98 · 4.65 배** — 원문은 c_max 와 견주지 않는다 · 인쇄 OCP 식으로 γ (식 13) 를 계산하면 **y 0.13–0.72 에서 음수 → D₁ < 0** (원인 후보 · 원문 처리 [미확인]) · OCP 하한 **2.5 V** 가 여러 칸에서 같다 (자른 흔적) | [인쇄 그림 안 글자] Fig 4 · 8 · Table 3 · 4 · [카드 산술 · 추론] |
| ⑧ 비표면적 주장 | *"The real electrode geometry provides higher surface area … compared to the spherical particle geometry"* (p.506) ↔ 원문 숫자로는 영상 a 3.6 µm⁻¹ < 구 3(1 − ε)/r = 48.6 (r 37 nm) · 25.0 (r 72 nm) µm⁻¹ — **6.9–13.5 배 낮다** · 영상 고체의 등가 구 반지름 3(1 − ε)/a = **0.50 µm** = 덩어리 (cluster) 척도 | [인쇄] p.500 · p.505–506 · [카드 산술] |
| ⑨ DEM · 소성 · 2D/3D · 탈압 | DEM · 압밀 · 역학 0 · 미시 3D (REV) + 거시 1D · 2D ↔ 3D 진술 없음 · 탈압 0 | [인쇄] 전수 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **상용 LFP 양극 (나노 입자 · 액체 전해질 LIB · 탄소 · PVDF)** — 고체전해질 · NCM · 황화물 · 압밀 없음 ② 영상 분해능 50 nm ≈ 일차 입자 크기 (반지름 37–169 nm · [44] 값) → 영상의 '입자' = **덩어리** · 이웃 융합 ③ REV = 750 nm **한** 정육면체 (그림 4 · 7 · 8 의 세 위치가 같은 기하) · τ 계산 = 1.5 µm 정육면체 ④ 검증 = 방전 곡선 한 벌 (맞춘 값 2 개를 같은 자료에 맞춤 · 오차 지표 · 반복 셀 수 없음) ⑤ 미시 농도 > c_max · OCP 2.5 V 하한 → 그림 4–8 의 '불균일' **크기**는 물리량으로 인용하지 않는다 ⑥ 보충 영상 (Video 1 · 2) 미수령 · 메시 요소 수 · 계산 시간 · 수렴 [미확인].
⇒ **절대값 전이**: **없다** — LFP 액체 LIB 의 ε · a · τ · 용량은 우리 LPSCl + NCM 복합 양극 (압밀 · SE 가 이온 통로) 에 옮기지 않는다.  옮길 것은 **방법** (REV 두 기준 · 정상 전도로 τ 를 내는 법 · τ 의 정의 (tau2) 와 방향 평균 규칙 · 미시 ↔ 거시 넘김 칸) 과 **함정** (해상도 ≈ 입자 크기 · 첨가제 합침 · 미시 농도 상한 · 비 단조 OCP).

---

## 0-1. ★ 이 논문을 넣는 까닭 (후보 밖 — 68 번 파일)

1저자가 11-12 에 *"지금 먹여준 것들 다 논문 에이전트 돌린다"* 며 68 번 파일로 준 논문이다.  후보 표 (`_curation/S8_candidates.md`) 의 어느 행도 아니다 — 같은 번호의 후보 N-68 (Sonzogni 2024 · Powder Technol. 442, 119891) 과 다른 논문이고, 그 후보를 가리킨 zhang2026 · lyu2025 의 참고문헌 목록에도 없다 (S8 L277).  그래서 **'고른 의도' 가 없다** — 지어내지 않는다.  정본에서는 [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) 이 참고 [11] 로 서지만 싣는다 (L408 *"카드 없음 — 나노 CT 실구조 다중스케일"* · 값 인용 없음).  아래 표는 이 논문이 우리 계획에 주는 것을 원문에서 뽑아 같은 꼴 (우리 쪽 자리 · 원문 위치 · 값 · 조건) 로 적은 것이다.

| 우리 쪽 자리 | 판정 (줌 / 일부 / 없음) | 원문 위치 · 값 · 조건 |
|---|---|---|
| 단계 7 — 영상 구조 → 유효 수송 물성 (ε · a · τ) 사슬 | **줌 (방법)** · 값은 LFP | p.498–500 · Table 1 · 2 · Fig S2 — 16 nm 복셀 이진 영상 → ScanIP 7 메시 → 정상 열전도 (기공 · AM) → τ · ε 0.4 · a 3.6 µm⁻¹ · 액체 LIB · 압밀 없음 (상용 전극 그대로 · 압연 이력 [미확인]) |
| 단계 7 — 대표 체적 (REV) 크기를 정하는 규칙 | **줌 (규칙 둘)** · 일부 (기준이 느슨) | p.499–500 · Table 1 — (i) 가장 큰 입자 하나가 들어가는 부피 → 728 nm (ii) 부분 정육면체 ε 3 % · a 9 % 안 (> 707 nm) → 750 nm — ⚠ Table 1 의 ≥ 707 nm ε 는 0.36–0.42 (0.40 대비 −10 / +5 %) [카드 산술] |
| 단계 7 · 비교 문서 J 절 — τ 의 정의 (√ 인가 제곱인가) | **줌** | 식 (4) D_eff = D·ε/τ → 이 τ = 우리 tau2 (수송 tortuosity · ε/τ = f) · τ_avg = 조화평균 [카드 산술] · κ_eff · σ_eff 에도 같은 τ (p.500) |
| 질문 h — 입자 규모 3D 구조 ↔ 전극 규모 연속체 넘김 선례 | **일부** (DEM → MPM 이 아니라 영상 → 연속체 · 규모 사이 결합) | Fig 2 · §4 · §4.3 — 넘기는 것 = j_n (거시 → 미시 경계 조건) · 갱신된 j_n (미시 → 거시) · 가정 = 계면의 전위 · 전해질 농도가 두 규모에서 같다 · 시점 = 매 시간 걸음 (concurrent) · 서열 결합 (대리 모델 · 조회표) 의 오차 비판 (p.497) |
| 검증 · 결과 전 대조 항목 방식 | 일부 | Fig 3 — 방전 곡선 5 개 율 · 정량 지표 0 · 맞춘 값 2 개를 같은 자료에 맞춤 → 이 카드의 3.0 V 용량 비 (§3-5) |
| 해상도 규칙 (U1 · U6 · 지름당 셀 수) | 일부 (**부정적 사례**) | p.498 · p.505 — 분해능 50 nm · 복셀 16 nm ↔ 일차 입자 지름 74 nm (P2D 반지름 37 nm) = 4.6 복셀 [카드 산술] · 영역 확장 융합 → 영상의 고체 = 덩어리 (등가 반지름 0.50 µm [카드 산술]) |
| 단계 0 — 기공을 세는 연산자 | 일부 | p.499 — 영상 기공 40 % (필터 · 영상 처리 뒤) ↔ BET 35 % · 차이 = *"unconnected pores which cannot be detected by BET"* (저자 설명 · 시험 안 함) · 백색 상에 첨가제 포함 (p.498) → 연산자 · 문턱 · 상 규약을 같이 적어야 하는 사례 |
| 단계 1–6 · 후보 D0 · A′-0 · A · A′ · B · C · C′ · M0 · 조건 R1–R7 | **없음** | 압밀 · 역학 · 접촉 · 탈압 · 고체전해질 계산 0 (본문 14 쪽 · SI 5 쪽 전수) |
| 가리킨 카드의 2 차 인용 | 해당 없음 (값 0) | wang2027 L408 서지 (저자 8 · 제목 · J. Power Sources 307 (2016) 496–509) = 원문 첫 쪽과 같음 |

⇒ **넣는 까닭 대조 결과: 일부** — 단계 7 (REV · τ · 영상 연산자) 과 넘김 (h) 의 방법 · 정의 · 함정은 준다 · 압밀 · 탈압 · 우리 재료의 값은 주지 않는다.

---

## 1. 한 줄 요약
P2D (같은 크기 구 · 균질 · Bruggeman) 가 실제 전극의 불균일과 높은 율의 성능 저하를 못 잡는다는 동기 (p.497) 에서, 나노 XCT 로 재구성한 상용 LFP 양극의 750 nm REV 를 3D 미시 (고체 확산) 로 두고 1D 거시 (P2D 식 · 실 tortuosity · 영상 비표면적) 에 매 시간 걸음 양방향으로 붙인 COMSOL 모델을 세워, C/10–4C 방전이 P2D 보다 실측에 가깝고 (P2D 는 저율 과대 · 고율 과소) REV 안 Li 농도 · OCP · 과전압 분포가 P2D 보다 넓고 위치마다 달라진다고 정리한 논문 — 다만 미시 농도가 원문 자신의 c_max 를 최대 4.6 배 넘고, 인쇄 OCP 로는 γ 가 플래토에서 음수라 그 분포의 **크기**는 물리량이 아니다 [카드 산술 · 추론].

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| A.G. Kashkooli · S. Farhad\* · D.U. Lee · K. Feng · S. Litster · S. Komini Babu · L. Zhu · Z. Chen\*\* (Waterloo · Akron · CMU · IUPUI) | J. Power Sources 307 (2016) 496–509 · 14 쪽 + SI 5 쪽 + 영상 2 | 10.1016/j.jpowsour.2015.12.134 | 상용 LFP/흑연 전지의 LFP 양극 (AM 90 wt% · PVDF · 탄소 · 양면 코팅 → 한 면 제거) · 반쪽 셀 상대극 Li 박 · 1 M LiPF6 EC:DEC 1:1 · Celgard 2500 · **SE · NCM 없음** | 영상 (nano-XCT · SEM) + 영상 기반 다중 스케일 연속체 계산 (COMSOL · FEM) + 반쪽 셀 율 시험 — DEM · MPM · 역학 0 |

- 키워드 (p.496): Lithium-ion battery · Inhomogeneous electrodes · Micro/nanostructure · Multiscale modeling · X-ray computed tomography.
- 하이라이트 (p.496): 다중 스케일 모델 · XCT 재구성 · *"The model predicts experimental data more accurately than the homogenous models"* · *"Inhomogeneity causes wider distribution of properties compared to homogenous models"* · *"The developed model is applicable to any lithium ion battery electrode material"*.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 시료 · 영상 · 실험 (p.498–499)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 시료 | 상용 LFP/흑연 전지를 Ar 글로브박스 (H₂O < 0.5 ppm · O₂ < 0.5 ppm) 에서 분해 · Al 집전체는 6 M KOH 에 담가 떼어 냄 [27] · 제조사 · 전지 모델 · 압연 조건 | [인쇄] p.498 · [미확인] |
| 영상 장비 | UltraXRM-L200 (Xradia, Pleasanton CA) · Carnegie Mellon University [38] | [인쇄] p.498 |
| 분해능 · 복셀 · 시야 | **50 nm** · **16 nm** 정육면체 · **16 µm** (*"A high resolution scan of region of interest"*) — 시야 = 1000 복셀 [카드 산술] | [인쇄] p.498 |
| 투영 · 단면 | *"A total of 990 tomograms were obtained by rotating the sample over 180° with 16 nm distance between slices"* — 990 × 16 nm = 15.84 µm ≈ 시야 → '990' 은 단면 수와 같다 [카드 산술] · 투영 수 · 노출 · 에너지 | [인쇄] · [미확인] |
| 분할 | 문턱 (thresholding) 으로 회색조 → 이진 · ScanIP 7 (Simpleware) 3D 재구성 · 문턱 값 · 필터 종류 | [인쇄] · [미확인] |
| 상 규약 | 흑 = AM 덩어리 · 백 = 기공 + 첨가제 (PVDF · 탄소) · 저원자번호 첨가제는 흡수 대비 + Zernike 위상 대비 두 방식이 있어야 갈린다 [39] · *"In this work, additives are not considered separately from the active material because it is hard to clearly distinguish them from active material. Moreover, treating them as separate region provokes an excessive computational load."* | [인쇄] p.498 |
| AM 질량 분율 | **90 wt%** — *"obtained by Thermogravimetric Analysis (TGA) [41]"* (직접 측정인지 [41] 의 값인지 문장으로 갈리지 않음) | [인쇄] · [미확인] |
| 탄소 처리 | *"we assumed that the carbon material is randomly distributed among the active material to provide electronic connectivity. For this, a growing region image processing algorithm was applied on the active material region to provide fusion of neighbors active material together."* | [인쇄] p.498 |
| 기공률 | 영상 *"pore volume became 40% after filtering and image processing improvement which came in agreement with the 35% porosity of the real electrode obtained by Brunauer Emmett Teller (BET) measurement"* (저자는 5 %p 차를 '일치' 로 부른다) ↔ BET **35 %** — *"The difference could be attributed to the unconnected pores which cannot be detected by BET."* · BET 로 기공률을 낸 방법 | [인쇄] p.499 · [미확인] |
| 반쪽 셀 | 한 면 코팅 제거 (NMP 묻힌 면봉 · 스카치 테이프) · 원판 **1.13 cm²** (지름 ≈ 12.0 mm [카드 산술: 2√(1.13/π)]) · LIR2032 · Li 박 · Celgard 2500 · 1 M LiPF6 EC:DEC 1:1 · Neware CT-3008-5V 10 mA | [인쇄] p.499 |
| 시험 | 화성 5 회 (CCCV 충전 · CC C/5 2.5–4.2 V · CV I < C/25 · 휴지 30 분 · CC 방전 4.2 → 2.5 V) · 평형 전위 = 완충 뒤 C/25 CC 방전 → *"the result is presented in Table 3"* · 율 시험 C/25–4C (2.5–4.2 V · 충전 CCCV · CV I < C/25) · 반복 셀 수 · 오차 | [인쇄] p.499 · [미확인] |

### 3-2. ★ REV 선택 (Table 1 · p.499–500)
| 정육면체 변 (nm) | ε [인쇄] | a (1/µm) [인쇄] | ε − 0.40 [카드 산술] | a ÷ 3.6 − 1 [카드 산술] |
|---|---|---|---|---|
| 2122 | 0.41 | 3.62 | +0.01 | +0.6 % |
| 1415 | 0.36 | 3.59 | −0.04 | −0.3 % |
| 1132 | 0.42 | 3.73 | +0.02 | +3.6 % |
| 849 | 0.42 | 3.71 | +0.02 | +3.1 % |
| 707 | 0.39 | 3.51 | −0.01 | −2.5 % |
| 566 | 0.35 | 4.27 | −0.05 | +18.6 % |
| 424 | 0.6 | 4.92 | +0.20 | +36.7 % |
| 283 | 0.58 | 4.87 | +0.18 | +35.3 % |

- 원문 (p.500): *"For the sizes above 707 nm, when the subdivision size increases, the porosity of the subdivisions remains within the 3% of the domain porosity. On the other hand, the average specific surface area of the electrode is around 3.6 (1/µm) where it remains within the 9% of the domain specific surface area for the subdivisions above 707 nm."* · *"Using the results of both approaches, a REV with 750 nm each side … was chosen"*.
- **점검 [카드 산술]**: ≥ 707 nm 의 ε 는 0.36–0.42 → 영역 0.40 대비 상대 −10 % / +5 % · 절대 −0.04 / +0.02 → '3 %' 는 영역 기공률을 0.39 로 보고 3 % 를 절대 0.03 으로 읽을 때만 맞는다.  a 는 ±3.6 % 로 원문 9 % 안.  707 nm 아래에서는 a 가 +19–37 % 로 튄다 (작은 정육면체 = 경계 효과).
- **기준 (i) 재현 시도 [카드 산술 · 가정]**: 반지름 169 nm 구 부피 = 0.0202 µm³ · 그런 입자가 AM 부피의 10 % · AM (고체) 부피 분율 0.6 이면 필요한 부피 = 0.0202 ÷ (0.1 × 0.6) = 0.337 µm³ → 변 **696 nm** · 원문 **728 nm** 는 고체 분율 0.52 에 해당 · 원문에 계산 과정 없음.
- 결정 REV **750 nm** = 가장 큰 입자 지름 (338 nm) 의 2.2 개 · 복셀 46.9 개 (≈ 10.3 만 복셀) · 부피 0.422 µm³ [카드 산술] · 메시 = ScanIP 7 사면체 (Fig S1 · 요소 수 [미확인]).
- 169 nm · 10 vol% 는 이 시료가 아니라 [44] (Majdabadi 외 2015) 가 *"similar to the one we disassembled"* 상용 LFP 에서 본 값 (p.499) — 이 시료의 입도 분포 [미확인].
- ⚠ 그림 4 · 7 · 8 의 세 위치 (x = l_pos/10 · l_pos/2 · l_pos) 가 같은 REV 기하로 그려진다 [카드 관찰] — 거시 마디마다 같은 REV 를 붙였는지 · 거시 마디 수 [미확인].

### 3-3. ★ tortuosity (Table 2 · p.500 · Fig S2)
- **정의**: 식 (4) *"D_eff = D ε/τ … where D is the intrinsic diffusivity and τ is the electrode tortuosity which accounts for the obstruction to diffusion by porous network"* (p.500) — 원문 이름 'tortuosity' ('factor' 낱말 없음).
- **방법**: *"using heat and mass transfer analogy, the steady state conductive heat transfer was simulated on both pore network and active material microstructure"* · *"(cube side is 1.5 µm)"* · *"applying temperature gradient in x, y, z directions separately"* · *"results obtained from the pore network must be compared to the one obtained through a uniform, non-porous sample with the same dimensions as discussed in Ref. [48] by cooper et al."* (p.500).

| 상 | 부피 분율 [인쇄] | τ_x | τ_y | τ_z | τ_avg [인쇄] | 조화평균 [카드 산술] | 산술평균 [카드 산술] | f = ε/τ_avg [카드 산술] | Bruggeman ε^−0.5 [카드 산술] | τ_avg ÷ Bruggeman |
|---|---|---|---|---|---|---|---|---|---|---|
| 고체 | 0.6 | 1.6116 | 1.8154 | 1.7794 | **1.7311** | 1.7308 | 1.7355 | 0.347 | 1.291 | **1.34** |
| 전해질 | 0.4 | 2.2544 | 2.4289 | 2.0844 | **2.2472** | 2.2471 | 2.2559 | 0.178 | 1.581 | **1.42** |

- **τ_avg 는 세 방향의 조화평균**이다 (2.2471 ↔ 인쇄 2.2472 · 1.7308 ↔ 1.7311) — 방향별 f = ε/τ 의 산술평균과 같다 [카드 산술] · 원문은 평균 규칙을 적지 않는다.
- 방향별 f [카드 산술]: 전해질 0.177 / 0.165 / 0.192 · 고체 0.372 / 0.331 / 0.337 · 방향 비 (최대 ÷ 최소 τ) 전해질 1.165 · 고체 1.126 · x 가 두께 방향인지 · 거시 1D 에 어느 값 (x 또는 평균) 을 넣었는지 [미확인].
- **같은 이름 다른 양 주의 [카드 해석]**: 식 (4) 의 꼴 (D_eff = D·ε/τ) 이면 이 τ 는 우리 **tau2 (수송 tortuosity · φ/f)** 이고 √ 값이 아니다.  이웃 대조 — 같은 열유속 방법 · 같은 재료 계열인 Cooper 2014 LFP (ε 0.410) 의 κ (= τ²) 2.70 / 2.19 / 3.32 · τ 1.64 / 1.48 / 1.82 (`tjaden2018_…` 카드 표 · 2 차 인용) → 이 논문 전해질 2.08–2.43 은 그 κ (tau2) 띠 쪽에 있어 tau2 해석과 맞는다.
- *"Since tortuosity is a geometric characteristics of the electrode, it is not related to the transport processes. Therefore, κ_eff can also be calculated using eq. (4) by replacing diffusivity, D with conductivity, κ using tortuosity values listed in Table 2. This is also valid for all upcoming effective parameters."* (p.500) — 고체 σ_eff 에도 고체 τ (1.7311) 를 쓴 것으로 읽힌다 [카드 해석 · 원문에 σ_eff 식 없음].
- 계산 정육면체 1.5 µm = REV (750 nm) 의 8 배 부피 · 한 변 93.75 복셀 [카드 산술] · Fig S2 색 막대 ▲1 ▼−2.69 × 10⁻⁷ (정규 온도) [인쇄 그림 안 글자] · 경계 조건 (옆면 단열 등) · 메시 · 수렴 [미확인].

### 3-4. 모델 매개변수 (Table 3 · p.501) + OCP 식 점검
| 기호 | 뜻 (원문) | 값 [인쇄] |
|---|---|---|
| A | Area of the electrode | 1.13 cm² |
| l_pos | Positive electrode thickness | 50 µm |
| l_sep | Separator thickness | 52 µm |
| ε_pos | Porosity of positive electrode | 0.4 |
| ε_sep | Porosity of separator | **1** |
| D_LFP | Solid state binary diffusion coefficient of LFP | **7 × 10⁻¹⁸ m²/s** (맞춘 값) |
| σ | Electrical conductivity of positive electrode | **0.03 S/m** (맞춘 값) |
| k₀ | Reaction rate constant in positive electrode | 2.5 × 10⁻¹³ mol m⁻² s⁻¹ (mol m⁻³)^−1.5 |
| α_a · α_c | Anodic · cathodic transfer coefficient | 0.5 · 0.5 |
| i_f | Exchange current density of lithium foil | 19 A/m² |
| c_ini | Initial salt concentration in the electrolyte | 1000 mol/m³ |
| c_max | Maximum lithium concentration in the LFP particles | **22,800 mol/m³** |
| D_LiPF6 | Salt diffusivity of electrolyte | 3 × 10⁻¹⁰ m²/s |
| t₊⁰ | Lithium ion transference number | 0.343 |
| T | Cell temperature | 298 K |
| U | Open circuit potential of LFP | U_c/50 = 3.382 + 0.00470 y + 1.627 exp(−81.163 y^1.0138) + 7.6445 × 10⁻⁸ exp(25.36 y^2.469) − 8.4410 × 10⁻⁸ exp(25.262 y^2.478) |

- **빠진 것**: 전해질 전도도 κ (식 5 · 거시) · 분리막 tortuosity · 활동도 계수 미분 (상수 가정 · p.500) · P2D 입자 반지름 (본문 37 nm) · 거시 경계 조건 [미확인].  ε_sep = 1 (Celgard 2500 인데 기공률 1) → 분리막을 전해질 층으로 둔 셈 [카드 해석].
- **이론 용량 [카드 산술]**: c_max · F · (1 − ε_pos) · l_pos = 22,800 × 96,487 (명명표 F) × 0.6 × 50 µm = **1.833 mAh/cm²** (고체 전부를 LFP 로 본 상한 — 실제는 AM 90 wt% 라 더 작다) · 실측 C/10 (3.0 V) 1.700 = 92.8 % · 다중 스케일 1.785 = 97.4 % · **P2D 1.863 = 101.6 %** (상한을 넘는다 → P2D 입력 ε · 두께가 Table 3 과 달랐을 가능성 [카드 추론 · 원문 설명 없음]).
- ★ **OCP 식 점검 [카드 산술 · R 8.314 J/(mol K) 가정 (원문 값 미인쇄) · F 96,487 (명명표) · T 298 K → F/RT = 38.94 V⁻¹]**:

| y | 0 | 0.02 | 0.05 | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 | 0.95 | 0.97 | 0.98 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U (V) | 5.009 | 3.732 | 3.415 | 3.383 | 3.383 | 3.384 | 3.385 | 3.265 | **2.420** | 1.134 | **−0.092** | −5.41 |

  - 플래토 (y 0.15–0.7) 에서 ∂U/∂y ≈ **+0.0047 V** (선형항 0.00470 y 가 지배) → γ = −(F/RT) y(1 − y) ∂U/∂y ≈ −0.019 (y 0.15) · −0.046 (y 0.5) → **γ < 0 구간 = y ≈ 0.13–0.72** → D₁ = D_LFP γ ≈ −1 × 10⁻¹⁹ … −3.2 × 10⁻¹⁹ m²/s (음의 확산) · 그 밖은 γ > 0 (y 0.02 에서 20.8 · 0.95 에서 74.9).
  - 읽는 법 [카드 추론]: 음의 확산계수 = 오르막 확산 (상분리 흉내) — 기울기 에너지 항이 없는 Fick 식에서는 잘 정의되지 않는 문제다 · 그림 4 · 8 의 국소 고농도 (c > c_max) 와 같은 방향 · 원문이 γ < 0 구간을 어떻게 다뤘는지 (자르기 · 다른 OCP · 절대값) [미확인].
  - y 의 뜻: 식 (13) 은 *"state of charge of the electrode, y"* 라 부르지만 OCP 식은 y = 0 → 5.0 V 이므로 **y = 리튬화 분율** (그림의 'SOC' 와 반대 방향 — SOC 0.95 = 방전 초기) [카드 추론].
  - OCP 자료 출처 표기 어긋남: 실험 절 *"discharged at CC at C/25 and the result is presented in Table 3"* (p.499) ↔ Table 3 의 기호 U_c/50 · p.507 *"half-cell discharge at C/50 (shown in Table 3)"*.

### 3-5. ★ 검증 — 방전 곡선 (Fig 3 · p.501) [판독]
| C-rate | 실측 (a 의 점) | 실측 (b 의 점) | 다중 스케일 (a 선) | 다중 ÷ 실측 | P2D (b 선) | P2D ÷ 실측 |
|---|---|---|---|---|---|---|
| C/10 | 1.700 | 1.699 | 1.785 | **1.05** | 1.863 | **1.10** |
| 1C | 1.446 | 1.442 | 1.557 | **1.08** | 1.485 | **1.03** |
| 2C | 1.329 | 1.323 | 1.434 | **1.08** | 1.143 | **0.86** |
| 3C | 1.217 | 1.216 | 1.320 | **1.09** | 0.915 | **0.75** |
| 4C | 1.073 | 1.077 | 1.224 | **1.14** | 0.786 | **0.73** |

(단위 mAh/cm² · 3.0 V 에서의 방전 용량)
- 방법: 원 래스터 (xref 98 · 1541 × 626 px · 300 dpi) · 격자선으로 축 보정 (a: x 0–1.8 · y 2.5–4.0 V 를 화소 직선으로 · 격자선 잔차 ≤ 0.7 px · b: x 0–2.0 · 잔차 ≤ 0.3 px) · 실측 점 = 같은 색 화소의 어둠 가중 무게중심 (손 씨앗 ± 6 px · 옅은 4C '+' 는 ± 4 px) · 3.0 V 교차 = 이웃 두 점의 직선 보간 · 모델 = 3.0 V 화소 행에서 선의 색 중심 → digitized.csv 106 행.
- **판독 재현성**: 두 패널의 실측 점은 표식 모양 · 표본 간격이 다른데 3.0 V 교차가 0.0009–0.0066 mAh/cm² 안에서 같다 → 같은 실측 자료 [카드 산술].
- 원문 문장과 대조: *"the P2D model over predicts the capacity at discharge rates lower than 1 and under predicts the capacity for higher discharge rates"* (p.506) — 판독과 같은 방향 (C/10 +9.6 % · 2–4C −14 … −27 %).  *"the multiscale model could also predict the discharge curves at different rates without further assumption"* (p.506) — 판독으로는 **모든 율에서 +5 … +14 % 높고 율이 오를수록 커진다** · **1C 는 P2D (+3 %) 가 다중 스케일 (+8 %) 보다 가깝다** [판독 · 카드 산술].
- 율 유지 (4C ÷ C/10 · 3.0 V): 실측 0.631 · 다중 스케일 0.686 · P2D 0.422 [카드 산술].
- 그림 3 의 율 = C/10 · 1 · 2 · 3 · 4C (범례 'Crate 1/10' …) ↔ 본문 *"C-rates ranging from C/25 to 4 C"* (C/25 곡선 없음) · x 축 끝 1.8 (a) · 2.0 (b) · C/10 다중 스케일 선은 1.8 mAh/cm² 에서 ≈ 2.68 V 로 축 밖으로 나간다 [판독].  실측 오차 막대 · 반복 셀 수 [미확인].

### 3-6. ★ 미시 분포 (Fig 4–8 · Table 4 · Fig S3–S5)
- **표 4 (p.507 · 방전 끝 범위 · mol/m³) = 색 막대 (최대 − 최소)** [인쇄 · 카드 산술 6/6 일치]:

| C-rate | l_pos/10 | l_pos/2 | l_pos |
|---|---|---|---|
| 1 | 3.50 × 10⁴ (= 4.28 × 10⁴ − 7806) | 2.33 × 10⁴ (= 3.4 × 10⁴ − 1.07 × 10⁴) | 1.37 × 10⁴ (= 2.9 × 10⁴ − 1.53 × 10⁴) |
| 4 | 1.05 × 10⁵ (= 1.06 × 10⁵ − 1127) | 7.40 × 10⁴ (= 7.57 × 10⁴ − 1694) | 3.91 × 10⁴ (= 4.31 × 10⁴ − 4011) |

- **농도 색 막대 끝값 [인쇄 그림 안 글자] 과 c_max 대비 [카드 산술]** (c_max = 22,800 mol/m³ · Table 3):

| 그림 · 상태 | x = l_pos/10 (▲ / ▼) | x = l_pos/2 | x = l_pos |
|---|---|---|---|
| 그림 4 · 1C · SOC 0.95 | 7023 / 230 | 7456 / 230 | **4.51 × 10⁴** (1.98 c_max) / 233 |
| 그림 4 · 1C · SOC 0.5 | 1.22 × 10⁴ / 1346 | 1.93 × 10⁴ / 1530 | 3.46 × 10⁴ (1.52 c_max) / 7126 |
| 그림 4 · 1C · 방전 끝 | 4.28 × 10⁴ (1.88 c_max) / 7806 | 3.4 × 10⁴ (1.49 c_max) / 1.07 × 10⁴ | 2.9 × 10⁴ (1.27 c_max) / 1.53 × 10⁴ |
| 그림 8 · 4C · 방전 끝 | **1.06 × 10⁵** (4.65 c_max) / 1127 | 7.57 × 10⁴ (3.32 c_max) / 1694 | 4.31 × 10⁴ (1.89 c_max) / 4011 |

- ⛔ **미시 농도가 c_max 를 넘는다** — 색 막대 열두 칸 (그림 4 아홉 · 그림 8 셋) 가운데 **여덟 칸**의 최댓값이 22,800 위 (최대 4.65 배) · 그림 5 히스토그램에서도 막대가 22,800 위로 넓게 이어진다 (SOC 0.95 · x = l_pos 칸 축 5,000–45,000 mol/m³ · 막대 ≈ 43,000 까지 · 1C 방전 끝 세 칸도) [판독 · 축 · 막대 위치] — 작은 '날카로운 곳' 만의 일이 아니다 · 원문은 이 고농도를 *"lithium ion concentration in microstructure is much higher in the region with smaller cross section area perpendicular to lithium intercalation pathway"* · *"Such low area regions would intercalate ca. 10 times higher than the area with an average concentration"* 로 읽고 c_max 와 견주지 않는다 (p.507).  식 (9) 의 (C_max − C₁s)^α 는 C₁s > C_max 에서 정의되지 않는다 [카드 산술] · 미시 Fick 식 (10) 에 상한 장치가 없고 플래토의 γ < 0 (§3-4) 이 오르막 확산을 만든다 [카드 추론 — 원인 후보].  P2D 히스토그램 (그림 6 · 1C) 은 축 · 막대가 c_max 아래 (방전 끝 막대 ≤ 약 21,700 mol/m³) [판독 · 축 범위] · 그림 S5 (4C) 는 축 오른쪽 끝 (≈ 20,000) 이 가려져 판단 못 한다.
- **본문 ↔ 그림 어긋남**: *"At SOC = 0.5, the maximum lithium ion concentration is 4.51 × 10⁴ mol/m³ … (cal. around 10 times compared to average lithium ion concentration in the REV)"* (p.507) ↔ 그림 4 의 4.51 × 10⁴ 는 **SOC 0.95 · x = l_pos** 칸 (SOC 0.5 · l_pos 최대 = 3.46 × 10⁴) · 같은 문단의 *"sharp region at SOC = 0.95, have higher concentration than the maximum concentration at the end of discharge (4.51 × 10⁴ compared to 2.9 × 10⁴)"* 는 그림과 맞는다 · '평균' 값은 미인쇄 [미확인].
- **OCP 하한 2.5 V**: 그림 S3 (1C) · 그림 8 (4C) 의 OCP 색 막대 최소가 여러 칸에서 정확히 2.5 V (S3: SOC 0.95 · x = l_pos · SOC 0.5 · l_pos · 방전 끝 세 칸 / 그림 8 세 칸) · 인쇄 OCP 식은 y 0.95 에서 2.42 V · y ≥ 0.98 에서 음수 (§3-4) → **2.5 V 에서 자른 값** [카드 추론 · 원문 설명 없음] · 그림 S4 (4C) 히스토그램에서 OCP 의 ≈ 50 % · 52 % (x = l_pos/10 · l_pos) 가 2.5 V 칸 [판독 · 막대 높이].
- **그림 S4 가운데 OCP 히스토그램 ↔ 그림 8 색 막대 어긋남**: 같은 상태 (4C 방전 끝 · x = l_pos/2 · 둘 다 고체/전해질 계면 값) 인데 그림 S4 의 OCP 축은 2.8–4.0 V (오른쪽 끝 가림) · 3.37 V 칸 ≈ 48 % · 3.4 V 위 막대가 4.0 V 까지 이어지고 2.5 V 칸이 없다 [판독] ↔ 그림 8 같은 칸 OCP 색 막대 ▲3.41 ▼2.5 V [인쇄 그림 안 글자] — 두 그림이 맞지 않는다 (원문 설명 없음).
- ★ **과전압 지도 = OCP 지도의 뒤집힌 판 [카드 산술 · 색 막대 끝값]**: 한 REV 안에서 φ₁ − φ₂ = η + U 가 일정하다 — 1C SOC 0.95: 3.40 / 3.40 / 3.38 V (l_pos/10 · l_pos/2 · l_pos · η 끝값 (그림 7) + U 끝값 (그림 S3) 을 양 끝에서 각각 맞춘 값) · 1C 방전 끝: 2.45 / 2.45 / 2.44 V · 4C 방전 끝: 2.54 / 2.48 / 2.31 V (그림 8 의 η · OCP 행) → η = (φ₁ − φ₂) − U 로 계산된 값과 맞는다 · 인쇄 식 (8) *"η = U − φ₁ − φ₂"* 와 부호 꼴이 다르다 · 1C SOC 0.95 · 0.5 · x = l_pos 의 **양의 η 0.88 · 0.86 V** = OCP 2.5 V (자른 값) 자리.  원문도 *"at a certain point along the thickness direction, the overpotential variations is primary due to OCP changes"* (p.507) 라 적는다 — 미시 안 φ₁ · φ₂ 는 넘김 가정 (§4-4) 으로 일정하므로 η 지도는 새 정보가 없다.
- 과전압 색 막대 [인쇄 그림 안 글자]: 그림 7 (1C) SOC 0.95 = −2.24 × 10⁻³ / −0.26 · −3.29 × 10⁻³ / −0.23 · **0.88** / −0.03 · SOC 0.5 = −7.19 × 10⁻³ / −0.01 · 4.55 × 10⁻³ / −0.02 · **0.86** / −0.04 · 방전 끝 = −0.05 / −0.95 · −0.05 / −0.95 · −0.06 / −0.96 · 그림 8 (4C 방전 끝) = 0.04 / −0.87 · −0.02 / −0.93 · −0.18 / −1.09 (V).
- **그림 S3 의 중복 칸**: SOC 0.5 · x = l_pos/2 칸이 SOC 0.95 · x = l_pos/2 칸과 **같은 그림 객체** (SI PDF xref 21 이 두 자리에 놓임 · 색 막대 3.63 / 3.4 도 같음) [PDF 객체 대조] — SOC 0.5 · l_pos/2 의 OCP 분포는 원문에 없다 · 위 φ₁ − φ₂ 대조를 이 칸에 하면 −0.02 + 3.63 = 3.61 ↔ 4.55 × 10⁻³ + 3.4 = 3.40 V 로 그 칸만 어긋난다 (다른 칸은 0.01 V 안) [카드 산술] — 중복과 맞는 증거.
- 그림 S4 패널은 SI 원본에서 서로 겹쳐 놓여 각 히스토그램 x 축 오른쪽 끝이 가려진다 (원문 상태) · 그래픽 초록 = 그림 8 의 첫 행 (같은 색 막대 끝값 · 율 표기 없음).

### 3-7. 비표면적 · 입자 크기 (p.500 · p.505–506)
- 영상 a = **3.6 µm⁻¹** (Table 1 · p.500) [인쇄].
- P2D 입자 크기 — 세 가지가 인쇄되어 있다: *"the average spherical particle diameter was chosen to be 37 nm based on the single particle distribution obtained by SEM (see Fig. 1c) [44]"* · *"calculated for spherical particles with radius of 37 nm"* (p.505) ↔ 그림 6 · S5 캡션 *"spherical particles with radius of 72 nm"* [인쇄 대조].
- 구의 비표면적 a = 3(1 − ε)/r [카드 산술]: r 18.5 nm (지름 37) → 97.3 · r 37 nm → **48.6** · r 72 nm → **25.0** µm⁻¹ → 영상 a 는 그 **1/6.9 – 1/27**.
- 영상 고체의 등가 구 반지름 3(1 − ε)/a = **0.50 µm** [카드 산술] → 재구성 고체 = 덩어리 (*"the reconstructed 3D microstructure of the electrode consists of cluster of particles"* · p.498) · 일차 입자 지름 74 nm = 복셀 4.6 개 · 분해능 50 nm 의 1.5 배 [카드 산술].
- ⛔ 원문 주장 *"The real electrode geometry provides higher surface area for the lithium to intercalate compared to the spherical particle geometry with average size in the P2D"* (p.506) 은 원문 숫자와 **반대** [카드 산술] · 원문은 P2D 의 a 값을 인쇄하지 않는다.
- 확산 시간 척도 L²/D_LFP (γ 배율 전) [카드 산술]: 덩어리 L 0.5 µm → 3.6 × 10⁴ s · 구 L 37 nm → 196 s — 같은 D_LFP 라도 기하에 따라 두 자릿수 다르다 → 맞춘 D_LFP 는 그 기하에 묶인 값 (P2D 에 같은 D_LFP 를 썼는지 [미확인]).

---

## 4. ★ 방법 — 영상 사슬 · 모델 · 결합 · 계산

### 4-1. 영상 사슬 (재구성)
상용 전지 분해 → KOH 로 Al 제거 → nano-XCT (50 nm / 16 nm / 16 µm · 180° · 990) → 문턱 이진 (흑 AM · 백 기공 + 첨가제) → 필터 · 영상 처리 · 영역 확장 (이웃 AM 융합 · 탄소가 AM 사이에 고르게 있다는 가정) → 기공 40 % → ScanIP 7 → (i) 부분 정육면체 ε · a (Table 1) (ii) 1.5 µm 정육면체 정상 열전도 → τ (Table 2 · Fig S2 · Video 2) (iii) 750 nm REV 사면체 메시 (Fig S1) → COMSOL Multiphysics® (판 [미확인]).

### 4-2. 거시 1D 지배식 (식 1–9 · p.500–501 · 크롭 `eq_*`)
| 식 | 인쇄 꼴 | 뜻 · 이 카드의 메모 |
|---|---|---|
| (1) | xLi⁺ + xe⁻ + Li_yFePO₄ ⇌ Li_(x+y)FePO₄ | 양극 반응 |
| (2) | Li ⇌ Li_(1−x) + xLi⁺ + xe⁻ | Li 박 음극 |
| (3) | ε ∂c₂/∂t = ∂/∂x (D_eff ∂c₂/∂x) + a j_n (1 − t₊⁰) | 전해질 물질 수지 (농축 용액 이론) · a = 영상 값 |
| (4) | D_eff = D ε/τ | ★ τ = Table 2 (우리 tau2 자리) |
| (5) | ∂φ₂/∂x = −i₂/κ_eff + (RT/F)(1 − t₊)(1 + ∂ln f₂/∂ln c₂) ∂ln c₂/∂x | 전해질 전위 · f₂ 상수 가정 · [카드 해석] 이진 전해질의 흔한 꼴은 2RT/F — 인쇄본에 2 가 없다 (오식인지 [미확인]) |
| (6) | I − i₂ = −σ_eff ∂φ₁/∂x | 고체상 옴 법칙 (I = 겉보기 전체 전류 밀도) |
| (7) | j_n = I/F = (i₀/F)(exp(α_aFη/RT) − exp(−α_cFη/RT)) | Butler–Volmer · 'I/F' 는 인쇄 그대로 (I = 셀 전체 전류 밀도 (명명표) — 국소 전류 밀도의 오기로 보인다 [카드 추론]) |
| (8) | η = U − φ₁ − φ₂ | 인쇄 꼴 그대로 — 그림은 η = φ₁ − φ₂ − U 로 계산된 값과 맞는다 (§3-6) |
| (9) | i₀ = F k₀ (c₂s)^α (C_max − C₁s)^α C₁s^α | 교환 전류 밀도 · α = 0.5 이면 k₀ 단위 (mol m⁻³)^−1.5 와 맞는다 [카드 산술] · C₁s > C_max 에서 정의되지 않음 |

- 단위 어긋남 [카드 산술 · 차원]: 명명표의 j_n = *"pore-solid flux of lithium ions (mol/(m³ s))"* (p.508) ↔ 식 (3) 의 a·j_n (a = m²/m³) · 식 (11) −D₁∇c₁·n 은 면적당 플럭스 (mol m⁻² s⁻¹).
- 거시 경계 조건 (집전체 · Li 박 쪽) · 분리막 영역 식 · 시간 적분 · 해석기 [미확인].

### 4-3. 미시 3D REV 지배식 (식 10–13 · p.501 · p.504)
| 식 | 인쇄 꼴 | 뜻 |
|---|---|---|
| (10) | ∂c₁/∂t = ∇·(D₁∇c₁) | REV 고체 안 Li 확산 (Fick) — 농도 상한 장치 없음 |
| (11) | j_n = −D₁∇c₁·n (고체 · 전해질 계면) | 거시 → 미시 넘김 자리 · 본문 *"Boundary condition for the eq. (11)"* 은 식 (10) 의 오기 [카드 추론] |
| (12) | D₁ = D_LFP γ | 가변 고체 확산계수 [44,52,54] |
| (13) | γ = −(F/RT) y(1 − y) ∂U/∂y | 열역학 인자 · 인쇄 OCP 로는 플래토에서 γ < 0 (§3-4) |

- 코어–셸 대신 가변 확산: *"The validity of the Core-Shell model has been controversial [52–54] since it has shown to be incompatible with experimental observation [55]. To account for phase change, here we have used the variable solid-state diffusivity model [44,52,54]"* (p.504).
- **미시 안에서 풀리는 것은 고체 농도 c₁ 하나** — 기공 (전해질) 상 · 전위는 미시에서 풀지 않는다 (§4-4 의 가정) [카드 해석] ⇒ REV 안 '불균일' 은 고체 확산 기하 + 계면 OCP(C₁s) · i₀(C₁s) 에서만 나온다.

### 4-4. ★ 결합 — 무엇이 언제 건너가나 (Fig 2 · p.497 · p.499 · p.501–503)
1. 거시 초깃값으로 j_n (그림 2 의 빨간 공) → 2. 미시 경계 조건 (식 11) 으로 식 (10) 풀기 → c₁ · C₁s 갱신 → 3. C₁s 로 i₀ (식 9) · OCP · j_n 갱신 — *"To update the flux we assume that the electric potential and electrolyte concentration at the interface does not change between the two scales"* (p.502) → 4. 갱신된 j_n 을 거시로 (*"mapped from microscale to macroscale"*) → 거시 식 (3 · 5 · 6) 으로 상태 변수 갱신 → 다음 시간 걸음 (반시계 고리) · *"This loop continues until the stop operation condition of the cell is satisfied"* (p.503).
- 동시 (concurrent) ↔ 서열 (serial) — *"all the governing equations are solved concurrently in two scales and state variables are transferred between them in real time"* ↔ 서열 결합 = 미시 모의 자료로 만든 대리 모델 · 데이터베이스 · 조회표 [36,37] · *"Although using serial method diminishes computational time, it includes error due to uncertainty in fitting the empirical model to microstructural data. In addition, the assumption of quasi steady state in microscale is highly questionable in a mainly time dependent model."* (p.497).
- 거시 마디 수 · 마디마다 REV 를 따로 두었는지 (세 위치 그림이 같은 기하) · 평균 연산 (REV 플럭스 → 거시 j_n) 의 식 · 시간 걸음 · 수렴 판정 [미확인].

### 4-5. 맞춘 값 · 검증 · 비용
| 항목 | 내용 | 표지 |
|---|---|---|
| 맞춘 값 | **2 개** — D_LFP · σ (*"design adjustable parameters … determined based on the method described in Ref. [50] and compared with the obtained experimental data"*) · 어느 율 · 어떤 지표로 맞췄는지 · P2D 에도 같은 값을 썼는지 | [인쇄] p.505 · [미확인] |
| 검증 | 같은 반쪽 셀 자료의 다섯 율 (Fig 3) · 독립 시료 · 정량 오차 지표 없음 · 이 카드의 판독은 §3-5 | [인쇄] · [판독] |
| 다른 대조 | P2D (같은 매개변수 · 평균 구 · Bruggeman 1.5) · 미시 분포는 P2D 히스토그램 (그림 6 · S5) 과만 비교 | [인쇄] p.505–507 |
| 계산 | COMSOL Multiphysics · 판 · 메시 요소 수 · 시간 걸음 · 계산 시간 · 메모리 · 해상도 · REV 크기 수렴 (전기화학 결과로) | [미확인] |
| 비용 주장 | 나노 입자 전극을 통째 3D 로 풀면 *"around 10⁶ times more mesh elements in 3D"* (길이 척도 10⁻⁸–10⁻² m ↔ 마이크로 입자 10⁻⁶–10⁻² m · p.497) — 다중 스케일로 줄인 비용의 실측 숫자는 없다 | [인쇄] · [미확인] |

### 4-6. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — 이 논문은 DEM 을 쓰지 않는다.  가까운 문장은 **연속체 P2D 의 구 · 균질 가정** 비판이다: *"Newman's pseudo-2D (P2D) model assumes that the porous electrode is made of equally sized, isotropic, homogenous spherical particles [9]."* · *"However, it fails to predict the phenomena related to inhomogenous structure of the electrode microstructure such as performance drop at high rates [20,21]. In addition, the well-known method of estimating the specific surface area based on spherical particles and the electrode tortuosity using Bruggeman correction has been controversial [22,23]."* (p.497) · *"in the P2D model it is assumed that the porous electrode consists of isotropic, homogeneous, mono-dispersed spherical particles [27]. These assumptions are not valid for real battery electrodes where the electrode microstructure is inhomogeneous, non-isotropic with 3D pores and constructed from different size and shape particles."* (p.504–505) — 단단한 구 · 점접촉 DEM 의 한계 진술이 아니다.
- **(ii) 소성 · 큰 변형 = 논의 없음** — 우회는 **변형이 끝난 실제 형상 (상용 전극 · 압연 뒤) 을 영상으로 가져와 고정** 하는 것 · 비용 = 해상도 (50 nm ≈ 입자) · 첨가제 합침 · REV 하나 · 영역 확장 융합 (접촉을 형상에 묻음).
- **(iii) 차원**: 미시 3D (REV) · 거시 1D · τ 는 3D 세 방향 · 2D 는 표시용 단면 (그림 1a) 뿐 · 2D ↔ 3D 전이 진술 없음.
- **(iv) 탈압**: 압력 · 하중 · 역학 0.

### 4-7. 기법 미니 용어집
- **nano-XCT (나노 X 선 CT)** = 시료를 돌리며 X 선 투영을 모아 3D 를 재구성하는 영상 — 여기서는 실험실 장비로 분해능 50 nm · 복셀 16 nm.  분해능보다 작은 입자 · 틈은 이웃과 합쳐 보인다.
- **REV (Representative Elementary Volume · 대표 체적)** = 그보다 크게 잘라도 평균 물성이 거의 안 바뀌는 가장 작은 부피 — 이 논문은 '가장 큰 입자 하나 + 부분 정육면체 ε · a 수렴' 으로 정했다.
- **영역 확장 (growing region)** = 정한 상의 화소에서 출발해 조건에 맞는 이웃 화소로 넓혀 가는 영상 처리 — 여기서는 이웃 활물질을 이어 붙이는 데 썼다 (탄소가 그 사이를 잇는다는 가정).
- **열전도 유사 tortuosity** = 한 상에만 전도도를 주고 정상 열전도 (Laplace) 를 풀어 흐른 열량을 같은 크기의 꽉 찬 시료와 비교 → ε/τ = 유효 ÷ 고유 (Cooper 방법 · TauFactor 와 같은 정의).
- **동시 결합 (concurrent) ↔ 서열 결합 (serial)** = 두 규모의 식을 매 시간 걸음 함께 풀며 상태를 주고받기 ↔ 미시를 미리 풀어 만든 대리 모델 · 조회표를 거시에서 부르기.
- **가변 고체 확산계수 · 열역학 인자 γ** = D₁ = D·γ · γ = −(F/RT) y(1 − y) ∂U/∂y — OCP 기울기로 확산을 키우거나 줄여 상분리 물질 (LFP) 을 흉내 내는 방법.  OCP 가 단조 감소가 아니면 γ < 0.
- **P2D (Newman pseudo-2D)** = 전극 두께 1D + 각 점의 대표 구 입자 반지름 1D — 같은 크기 · 균질 · Bruggeman 유효 물성.
- **Bruggeman 관계** = 유효 = 고유 × ε^1.5 (τ = ε^−0.5) — 구 충전에서 유도된 관계.
- **BET** = 기체 흡착 등온선으로 비표면적을 재는 방법 — 이 논문은 이것으로 '기공률 35 %' 를 적었다 (방법 [미확인]).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| GA | 그래픽 초록 = 그림 8 첫 행 (4C 방전 끝 미시 농도 · 같은 색 막대 끝값 · 율 표기 없음) | — |
| 1 (a–c) | (a) 이진화 나노 XCT 단면 5 µm (흑 AM · 백 기공 + 첨가제) (b) 재구성 3D 5 µm (c) SEM (100 nm 막대) | 영상 사슬 · 해상도 ≈ 입자 크기 (덩어리 구조) 의 그림 |
| 2 | 다중 스케일 고리 — 거시 식 (3 · 5 · 6 · 7) ↔ 미시 식 (10 · 11) · j_n · ∇c₁ · c₁ · C₁s · i₀ 공 · 'Next time step' | 넘김 (h) 의 '무엇이 건너가나' 그림 |
| 3 (a · b) | ★ 방전 곡선 C/10–4C · 다중 스케일 (a) · P2D (b) · 점 = 실측 | 검증 판독 §3-5 (3.0 V 용량 비) |
| 4 | 1C 미시 Li 농도 지도 (3 위치 × SOC 0.95 · 0.5 · 방전 끝) | c > c_max 의 증거 (색 막대) · 본문 SOC 표기 어긋남 |
| 5 | 다중 스케일 1C 농도 히스토그램 | 분포 폭 (c_max 위 몫) |
| 6 | P2D 1C 히스토그램 (캡션 반지름 72 nm) | P2D 는 c_max 아래 |
| 7 | 1C 과전압 지도 | η = (φ₁ − φ₂) − U 확인 (OCP 지도의 뒤집힌 판) |
| 8 (행 a–c) | 4C 방전 끝 농도 · OCP · 과전압 | 최대 4.65 c_max · OCP 2.5 V 하한 · 표 4 = 색 막대 범위 |
| S1 | REV 750 nm + 사면체 메시 | REV 크기 · 메시 꼴 (요소 수 없음) |
| S2 | 1.5 µm 정육면체 기공상 정상 열전도 (y 방향) | τ 계산 영역 = REV 와 다름 |
| S3 | 1C OCP 지도 | OCP 2.5 V 하한 · ⚠ 중복 칸 (SOC 0.5 · l_pos/2) |
| S4 | 4C 방전 끝 농도 · OCP · η 히스토그램 | OCP 두 봉우리 (2.5 · 3.4 V · x = l_pos/10 · l_pos) · 가운데 OCP 칸 2.8–4.0 V ↔ 그림 8 색 막대 3.41 / 2.5 V 어긋남 · 패널 겹침 (원문 상태) |
| S5 | P2D 4C 방전 끝 히스토그램 (캡션 반지름 72 nm) | 가장 낮은 칸 (≈ 0–1,000 mol/m³) 몫 ≈ 64 · 45 · 23 % (l_pos/10 · l_pos/2 · l_pos) [판독 · 막대 높이] · 축 오른쪽 끝 가림 |
| 표 1 | REV 판정 (정육면체 변 · ε · a) | §3-2 |
| 표 2 | 방향 τ (고체 · 전해질) | §3-3 · 우리 J 절 |
| 표 3 | 모델 매개변수 + OCP 식 | §3-4 |
| 표 4 | 미시 농도 범위 (1C · 4C · 세 위치) | = 색 막대 범위 |
| 식 크롭 14 장 | `eq_01_*` – `eq_13_*` (식 1–13) · `eq_T3_lfp_ocp_fit_table3` (OCP 식) | 보고서 수송 · 다중 스케일 절에 붙일 지배식 |
| 근거 문단 19 장 | `txt_p1_*` (초록) · `txt_p2_*` (P2D 비판 · 길이 척도 · 결합 방식) · `txt_p3_*` (영상 조건) · `txt_p3_p4_*` (상 규약 · 융합 · 기공) · `txt_p4_*` (실험 · 결합) · `txt_p4_p5_*` (REV) · `txt_p5_*` (τ 방법 · τ 하나로 모든 유효 물성) · `txt_p6_p8_*` (결합 가정) · `txt_p8_p9_*` (가변 확산) · `txt_p10_*` (맞춘 값 · P2D 크기) · `txt_p11_*` (P2D 비교 · 비표면적 주장) · `txt_p12_*` (최댓값 문장 · OCP · 4C · 결론) · `txt_p13_*` (명명표 단위) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을 (원문)**: 영상 → ε · a (부분 정육면체 · ScanIP) · τ (정상 열전도 · 세 방향) · 방전 곡선 (모델 ↔ 실측 겹쳐 그리기) · 미시 농도 · OCP · 과전압 3D 지도 (세 위치 × 세 상태) · 부피 % 히스토그램 · 범위 표 (표 4).
- **안 한 것**: 오차 지표 (RMSE 등) · 전기화학 결과의 REV 크기 · 메시 수렴 · 해상도 · 문턱 민감도 · 기공 연결성 (닫힌 기공 몫) · 첨가제 상 분리 · P2D 의 a 값 인쇄 · 미시 농도와 c_max 비교.
- **이 카드의 후처리**: 그림 3 원 래스터 판독 (106 행 · 3.0 V 교차 · 두 패널 실측 일치 확인) · 색 막대 끝값 전사 36 행 · 표 4 = 색 막대 범위 대조 · c/c_max · OCP 식 · γ 부호 · 이론 용량 · 구 비표면적 · 등가 반지름 · τ 조화평균 · Bruggeman 비 · REV 재현 시도 · φ₁ − φ₂ 일정성 점검 · SI PDF 객체 대조 (중복 칸).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 원장 CL 번호를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 계 · 재료 | 액체 전해질 LIB · 상용 LFP 양극 (나노 입자 · PVDF · 탄소) | 전고체 · NCM (μm) + LPSCl + 첨가제 · 압밀 300 MPa | 다름 — 이온 통로가 **액체 기공** ↔ **눌린 SE 입자망** |
| 구조 출처 | 실측 영상 (상용 전극 · 압연 뒤 · 고정) | DEM 압밀 침대 (구) · MPM 소성 침대 (복셀) | 다름 — 그들은 형상을 계산하지 않는다 |
| 수송 해석기 | 영상 메시 위 정상 열전도 → τ → 거시 1D (P2D 식) | 접촉망 Kirchhoff (Holm 협착 · DEM) · STEP3 복셀 FV (CONTACT_FREE · CL-81) | 그들의 τ 계산 = STEP3 와 **같은 부류** (융합 복셀 · 계면 저항 0) |
| τ 정의 | D_eff = Dε/τ → tau2 · 조화평균 | tau2 = φ σ₀/σ_eff (CLAUDE.md τ 명명 규약) | **같은 양** · 이름만 'tortuosity' |
| REV | 750 nm (가장 큰 입자 지름 2.2 개) · τ 는 1.5 µm | DEM · MPM 주기 RVE (침대마다) | 그들은 ε · a 수렴 sweep 으로 정했다 — 우리 침대의 RVE 크기 수렴 기록은 이 카드에서 확인하지 않았다 [미확인] |
| 해상도 | 복셀 16 nm · 일차 입자 지름 74 nm = 4.6 복셀 · 분해능 50 nm | STEP3 SE ⌀1 µm 에 vox 0.15–0.4 µm = 2.5–7 복셀 · MPM d_h/dx ≳ 3.5 규칙 | **같은 등급의 '겨우 풀린' 해상도** — 그들은 덩어리로 융합 · 우리는 격자 미수렴 (CL-41) |
| 결합 | 미시 3D ↔ 거시 1D · 매 시간 걸음 · 양방향 | DEM → MPM 스캐폴드 (한 번 · 한 방향 · 기하만) | 결합 대상 · 시점 · 방향 모두 다름 (§7-4) |
| 역학 · 압밀 · 탈압 | 없음 | DEM 18 배 연화 E_eff 1.35 GPa · Heckel P_y 138 MPa · MPM E 1.53 · σ_y 0.30 · ν 0.49 · 언로딩 키트 진행 | 견줄 값 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 · 상태 | 기공 | 비고 |
|---|---|---|---|
| **랩 표준** | 순수 LPSCl · 300 MPa · 진밀도 **1.64 g/cm³** (고정) | **10–13 %** | 판정 대상 아님 |
| 이 논문 — 영상 | 상용 LFP 양극 (액체 LIB · 압력 없음) · 분해능 50 nm · 첨가제 포함 백색 상 | 40 % | 랩 표준과 다른 문헌 값 · 다른 계 |
| 이 논문 — BET | 같은 전극 | 35 % | 방법 [미확인] · 닫힌 기공 제외 (저자 설명) |
| 우리 DEM 순수 SE | LPSCl · 300 MPa (E_eff 1.35 GPa) | ε_union ≈ 10 % | CLAUDE.md 2026-06-06 (MPM 보정 절의 대조값) |
| 우리 MPM 순수 SE | LPSCl · 300 MPa | 10.0 % (σ_y 0.30) | 보정 표적 · 외부 앵커 아님 (`CL-94`) |

- 이 논문의 기공은 **액체가 채울 공간** (LIB) 이고 우리 기공은 **압밀 SE 망의 빈틈** 이다 — 숫자를 나란히 두어도 같은 양이 아니다.  옮길 것은 '영상 40 ↔ BET 35 처럼 연산자마다 기공이 다르다' 는 사례뿐.

### 7-3. ★ 우리 STEP3 복셀 · 접촉망 ↔ 이 논문의 τ · REV
- 그들의 τ = 영상 메시 위 정상 전도 · 한 상에만 전도도 · 같은 상 화소는 그대로 이어짐 · 계면 저항 항 0 = **우리 STEP3 와 같은 CONTACT_FREE 부류** (CL-81) [카드 해석].  액체 기공상에는 '입자 접촉' 개념이 없으므로 그들에게는 맞는 근사다 — 같은 꼴을 우리 SE 상 (입자망) 에 쓰면 Holm 협착이 빠진다 (우리 접촉망 FULL ↔ CF 차이).
- 고체상 (AM + 첨가제) 은 영역 확장으로 이웃을 **융합**하고 σ 0.03 S/m 을 **맞춤** → 접촉 · 탄소망의 실제 저항을 '맞춘 유효 σ' 하나에 묻었다 = 우리 σ_VGCF 100 S/cm 이 융합 결손을 묻은 유효 망 상수라는 CL-47 과 같은 꼴 [카드 해석].
- 방향 평균: 그들의 τ_avg = 조화평균 = f 의 산술평균 [카드 산술] → 우리 tau2 를 방향 평균해 보고할 때 규칙 (f 평균 ↔ tau2 산술평균) 을 함께 적는다.
- REV: 그들의 두 규칙 (가장 큰 입자 · 부분 정육면체 ε · a 수렴) 은 우리 STEP3 · MPM 침대에도 바로 쓸 수 있는 점검이다 — 다만 그들의 수렴 띠 (ε ±0.04 · a ±4 %) 와 '전기화학 결과의 REV 수렴은 안 봄' 은 그대로 한정어.

### 7-4. 넘김 (질문 h) — 이 논문의 미시 ↔ 거시 결합 ↔ 우리 DEM → MPM 스캐폴드
| 칸 | 이 논문 | 우리 (CLAUDE.md DEM→MPM SCAFFOLD 절) |
|---|---|---|
| 무엇과 무엇 | 같은 연속체 식의 두 규모 (3D REV ↔ 1D 전극) | 다른 두 방법 (DEM 구 침대 → MPM 소성 연속체) |
| 언제 | 매 시간 걸음 (concurrent) | DEM 압밀이 끝난 뒤 한 번 |
| 방향 | 양방향 (j_n ↔ 갱신된 j_n) | 한 방향 (AM 위치 · SE 씨앗 → MPM) |
| 건너가는 양 | j_n · C₁s (농도 · 플럭스) | 기하 (AM 골격 · SE 중심 · 반지름) |
| 같다고 둔 양 | 계면의 φ · c₂ (두 규모에서 같음) | AM 골격 고정 (MPM 에서 움직이지 않음) |
| 대리 모델 비판 | 서열 결합 = 맞춤 오차 + 준정상 가정 의심 (p.497) | 우리 쪽에 같은 꼴의 대리 결합은 없다 (설계 → 구조 ML 예측기는 규모 사이 결합이 아니라 입력 예측 [카드 해석]) |

- 가져올 것: **넘김 매니페스트 칸** — '무엇이 경계를 건너는가 · 언제 · 어느 방향 · 무엇을 같다고 두는가' 를 결합마다 적는 꼴 (그들의 Fig 2 + p.502–503 한 문장).

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실측 3D 구조 위의 **수송 · 반응 연속체** (τ · a · 고체 확산 · 거시 방전) · 미시 ↔ 거시 결합.
- **없는 것**: 구조를 만드는 **역학** (압밀 · 소성 · 접촉 · 파괴 · 탈압) · 고체전해질 · 접촉 저항.  ⇒ 우리 수송 (DEM 접촉망 · STEP3) 쪽에 방법 · 정의 · 함정을 주고, 역학 (MPM) 쪽에는 주는 것이 없다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 영상 40 % ↔ BET 35 % — 같은 전극 · 연산자 둘 · 5 %p 차 · 저자 설명 = 닫힌 기공 (시험 안 함) · 백색 상에 첨가제 포함 → 연산자 등록에 '상 규약 · 문턱 · 해상도 · 연결 기공만인가' 칸 | 우리 재료 · 압력의 기공 값 0 |
| **단계 1** (3D 메모리 · 장 수) | REV 750 nm = 46.9³ ≈ 10.3 만 복셀 · τ 정육면체 1.5 µm = 93.75³ [카드 산술] — 크기 감각뿐 · 원문 주장 '통째 3D 면 10⁶ 배 요소' | 메모리 · 시간 · 요소 수 [미확인] · 역학 장 아님 |
| **단계 2 · 3** (2D MPM 코드 · 접촉 표현 비교) | 없음 | — |
| **단계 4 · 5 · 6** (순수 SE · 복합 압밀 · 탈압) | 없음 | 압밀 · 역학 0 |
| **단계 7** (형상 · 피복 · 수송) | ★ (1) τ 를 정상 전도로 내는 절차 (상별 · 방향별 · 균일 시료 대비) (2) τ 정의 = tau2 · 방향 평균 = 조화평균 (3) REV 두 규칙 (4) 비표면적은 해상도에 묶인다 (구 25–49 ↔ 영상 3.6 µm⁻¹) (5) 고체 융합 + σ 맞춤 = 접촉 결손을 유효 σ 에 묻는 꼴 (CL-47 과 같은 꼴) | 값 전이 0 (LFP · 액체 · 압밀 없음) · 피복 · 협착 계산 없음 |
| **후보 D0** (지금 DEM) | 없음 — P2D (구 · 균질) 비판이 DEM 한계 진술은 아니다 | — |
| **후보 A′-0 · A · A′ · B** | 없음 | — |
| **후보 C · C′** | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 (압밀) · 다만 '균질 1D (P2D) 에 미시 3D 를 매 걸음 붙이는' 꼴은 M0 의 거시 ↔ 입자 규모 결합의 한 선례 [카드 해석] | 역학 결합 아님 |
| **U0–U6** | U1 · U6 의 부정적 사례: 일차 입자 지름 = 복셀 4.6 개 · 분해능 1.5 개 → 입자가 덩어리로 합쳐져 a 가 구 모형의 1/7–1/14 · 해상도 수렴 시험 0 | 수렴 시험 자체는 없다 |
| **R1–R7** | 없음 (R1 하중 분담 · R2 미끄럼 · R3 경계 기억 · R4 탈압 · R5 · R6 형상 변형 · R7 파괴 모두 0) | — |
| **결과 전 대조 항목** | 없음 (우리 재료 아님) · 방법 대조용: 같은 열유속 방법의 LFP tau2 (전해질 2.08–2.43 · ε 0.4) | 값 비교 금지 |
| **질문 h (넘김)** | ★ 미시 3D ↔ 거시 1D 동시 결합 · 건너가는 양 (j_n · C₁s) · 같다고 둔 양 (계면 φ · c₂) · 서열 결합의 맞춤 오차 · 준정상 가정 비판 | DEM → FE · MPM 넘김이 아니다 · 넘김 시점 = 매 걸음 (우리 = 압밀 끝 한 번) |

- **재료 · 차원 · 조건 차이**: LFP 나노 입자 (액체 LIB) ↔ NCM + LPSCl (전고체) · 미시 3D + 거시 1D ↔ 3D 침대 · 압력 0 ↔ 300 MPa · 상용 전극 고정 형상 ↔ 압밀 계산 · REV 0.75 µm ↔ 우리 침대 (수십 µm).

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **REV 를 결과 전에 두 규칙으로 등록한다** — (i) 가장 큰 입자 하나가 들어가는 부피 (ii) 부분 정육면체를 키우며 ε · 비표면적 (우리는 피복 · 접촉 수도) 이 정한 띠 안에 드는 크기.  그들의 띠 (ε ±0.04 · a ±4 %) 는 느슨했고 전기화학 결과로는 REV 를 보지 않았다 → 우리는 σ · tau2 로도 같은 sweep 을 본다 (단계 7 · 단계 0).
2. **τ 를 보고할 때 정의 · 방향 평균을 함께** — D_eff = Dε/τ 꼴이면 tau2 · 방향 평균은 f 의 산술평균 (= tau2 의 조화평균) · 그들 표의 τ_avg 가 정확히 그 값 (카드 §3-3) (단계 7 · 비교 문서 J 절).
3. **해상도 ≈ 입자면 '실 구조' 는 덩어리 구조다** — 비표면적이 구 모형보다 7–14 배 작게 나오고 그 위에 맞춘 확산계수 · σ 는 그 기하에 묶인다 · 우리 STEP3 (SE 지름당 2.5–7 복셀) 도 같은 등급 → 피복 · 계면 넓이를 격자 무관량으로 쓰지 않는다 (U1 · U6 · 단계 7).
4. **물리 범위를 결과 전 점검 항목으로** — 농도 ≤ c_max · OCP 단조 (γ > 0) · 잘린 하한 (2.5 V) 표시 · 지도 끝값으로 내부 일관 (φ₁ − φ₂ 일정) 확인.  이 논문 그림은 c_max 의 최대 4.65 배 · 인쇄 OCP 로 γ < 0 (흐름 밖: STEP4 반응 · 확산 결과 검사).
5. **넘김 매니페스트** — 결합마다 '무엇이 · 언제 · 어느 방향으로 건너가고 · 무엇을 같다고 두는가' 를 한 표로 (질문 h · §7-4).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Kashkooli et al. reconstructed a commercial LiFePO₄ cathode by laboratory nano-XCT (50 nm resolution, 16 nm voxels), selected a 750 nm representative elementary volume from the convergence of porosity and specific surface area of sub-cubes, and coupled it concurrently to a 1D P2D cell model in COMSOL (J. Power Sources 307 (2016) 496–509)."
- "Image-based tortuosity from a steady heat-conduction analogy, defined through D_eff = D·ε/τ, was 2.25 for the electrolyte (ε = 0.4) and 1.73 for the solid (ε = 0.6) — 1.42 and 1.34 times the Bruggeman value; the reported averages are the harmonic means of the three directions (our arithmetic on Table 2)."
- "In that model the microscale lithium concentration exceeds the stated maximum concentration of LiFePO₄ (22,800 mol m⁻³) by up to a factor of 4.6 at 4 C (colour-bar labels of Fig. 8; our arithmetic) — the distributions should not be cited as physical magnitudes."
- 국문: *"영상 기반 τ (D_eff = D·ε/τ) 는 수송 tortuosity (tau2) 이고 방향 평균은 조화평균이었다 (Kashkooli 2016 표 2 · 카드 산술)."*
- 국문: *"분해능이 일차 입자 크기와 같으면 재구성 구조는 덩어리 구조다 — Kashkooli 2016 의 영상 비표면적 3.6 µm⁻¹ 은 같은 논문 P2D 구 (반지름 37–72 nm) 의 1/7–1/14 이다 (카드 산술)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **미시 농도 > c_max** — 그림 4 · 5 · 8 · 표 4 가 c_max 22,800 의 최대 4.65 배 (1.06 × 10⁵) [카드 산술] · 원문은 다루지 않는다 · *"ca. 10 times higher"* (결론) 도 이 값에서 나온 문장 [카드 해석].
2. **인쇄 OCP 로 γ < 0** (y 0.13–0.72 · D₁ < 0) [카드 산술] · OCP 가 y ≥ 0.98 에서 음수 · 그림의 하한 2.5 V = 자른 값 [카드 추론] — 원문 처리 [미확인].
3. **식 (8) 부호 꼴** — 인쇄 *"η = U − φ₁ − φ₂"* ↔ 그림 7 · 8 은 η = φ₁ − φ₂ − U 와 맞는다 [카드 산술].
4. **'모든 율에서 더 정확'** ↔ 판독: 다중 스케일은 모든 율에서 +5 … +14 % 과대 · 1C 는 P2D 가 더 가깝다 [판독] · 오차 지표 · 반복 셀 없음 · 맞춘 값 2 개를 같은 자료에 맞춤.
5. **비표면적 주장 반대** — *"higher surface area"* ↔ 영상 3.6 < 구 25–49 µm⁻¹ [카드 산술].
6. **P2D 입자 크기 셋** — 지름 37 nm · 반지름 37 nm (p.505) · 반지름 72 nm (그림 6 · S5 캡션).
7. **P2D C/10 용량이 Table 3 값의 이론 상한 (1.833 mAh/cm²) 을 1.6 % 넘는다** [카드 산술] — P2D 입력이 Table 3 과 달랐을 가능성.
8. **SOC 표기 어긋남** — 본문 'SOC = 0.5 에서 최대 4.51 × 10⁴' ↔ 그림 4 의 SOC 0.95 칸.
9. **OCP 자료 C/25 ↔ C/50** (p.499 ↔ Table 3 · p.507) · 율 시험 'C/25 to 4C' ↔ 그림 3 의 C/10 · 1 · 2 · 3 · 4C.
10. **REV 기준 문장 ↔ 표 1** — ≥ 707 nm ε 0.36–0.42 는 '3 % 안' 보다 넓다 · 728 nm 의 계산 과정 없음 (재현 시도 696 nm @ 0.6).
11. **상 규약 모순** — 백색 = 기공 + 첨가제 (p.498) 라 하고 같은 문단에서 첨가제를 AM 과 따로 다루지 않는다고 적는다 → 영상 기공 40 % 에 첨가제가 섞였을 수 있다 [카드 추론] · 40 ↔ 35 의 '닫힌 기공' 설명은 시험되지 않았다.
12. **단위 · 식 번호** — j_n 단위 (mol/(m³ s)) ↔ 식 (3) · (11) 의 면적 플럭스 · 식 (7) 'j_n = I/F' · *"Boundary condition for the eq. (11)"* (→ 식 10) · *"c₁, is updated inside whole microstructure using eq. (11)"* · 식 (5) 의 RT/F (흔한 꼴 2RT/F [카드 해석]).
13. **ε_sep = 1** (Celgard 2500) · 전해질 전도도 κ 미인쇄.
14. **SI 그림 S3 중복 칸** (SOC 0.5 · l_pos/2 = SOC 0.95 · l_pos/2 · 같은 객체 xref 21) · 그림 S4 패널 겹침 · 그림 S4 가운데 OCP 히스토그램 (2.8–4.0 V · 2.5 V 칸 없음) ↔ 그림 8 같은 칸 색 막대 (3.41 / 2.5 V) [판독 · 인쇄 그림 안 글자].
15. **분해능 50 nm ≈ 입자** · REV 하나 (세 위치 같은 기하) · τ 는 다른 정육면체 (1.5 µm) · 메시 · 계산 시간 · 수렴 · 보충 영상 [미확인].
16. **169 nm · 10 vol%** 는 이 시료가 아니라 [44] 의 '비슷한' 상용 전극 값 · 90 wt% 도 [41] 인용과 섞인 문장.
17. ⚠ 판독 값 (그림 3) 은 원 래스터 격자선 보정 · 두 패널 실측 일치 (≤ 0.007) — 그래도 [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 48 | S.J. Cooper, D.S. Eastwood, J. Gelb, G. Damblanc, D.J.L. Brett, R.S. Bradley, et al., Image based modelling of microstructural heterogeneity in LiFePO4 electrodes for Li-ion batteries, J. Power Sources 247 (2014) 1033–1039. | τ (열유속 · 균일 시료 대비) 방법의 원전 · 같은 LFP · 방향 τ (tjaden2018 카드 표에 2 차 인용) | 없음 (papers/ ls · grep — tjaden2018 · landesfeind2016 이 인용만) |
| 23 | D.-W. Chung, M. Ebner, D.R. Ely, V. Wood, R. Edwin García, Validity of the Bruggeman relation for porous electrodes, Model. Simul. Mater. Sci. Eng. 21 (2013) 074009. | Bruggeman 대체의 근거 (비교 문서 J 절) | 없음 (malifarge2017 · tjaden2018 이 인용만) |
| 27 | B. Yan, C. Lim, L. Yin, L. Zhu, Three dimensional simulation of galvanostatic discharge of LiCoO2 cathode based on X-ray nano-CT images, J. Electrochem. Soc. 159 (2012) A1604–A1614. | 영상 기반 3D 방전 계산 (같은 공저자 L. Zhu) · 다중 스케일 없는 직접 3D (질문 h) | 없음 |
| 39 | S. Komini, A. Mohamed, J. Whitacre, Multiple imaging mode X-ray computed tomography for distinguishing carbon additives in lithium battery cathodes, J. Power Sources 283 (2015) 1–16. | 첨가제 (탄소) 상을 영상에서 가르는 법 — 이 논문이 못 한 것 (단계 7 상 규약) | 없음 |
| 37 | W. Du, N. Xue, W. Shyy, J.R.R.A. Martins, A surrogate-based multi-scale model for mass transport and electrochemical kinetics in lithium-ion battery electrodes, J. Electrochem. Soc. 161 (2014) E3086–E3096. | 서열 결합 (대리 모델) 의 대표 — 이 논문이 비판한 쪽 (질문 h) | 없음 |
| 44 | M. Mastali Majdabadi, S. Farhad, M. Farkhondeh, R.A. Fraser, M. Fowler, Simplified electrochemical multi-particle model for LiFePO4 cathodes in lithium-ion batteries, J. Power Sources 275 (2015) 633–643. | 169 nm · 37 nm · 다입자 · 가변 확산 · OCP 의 출처 사슬 | 없음 |
| 22 | D. Kehrwald, P.P.R. Shearing, N.P.N. Brandon, P.K.P. Sinha, S.J.S. Harris, Local tortuosity inhomogeneities in a lithium battery composite electrode, J. Electrochem. Soc. 158 (2011) A1393. | 국소 τ 불균일 (REV 판단) | 없음 (choi2018 · froboese2019 · tjaden2018 이 인용만) |
| 50 | V. Srinivasan, J. Newman, Discharge model for the lithium iron-phosphate electrode, J. Electrochem. Soc. 151 (2004) A1517. | 맞춤 방법 ('the method described in Ref. [50]') · 코어–셸 | 없음 |

---

## [미확인] 목록
- 시료: 상용 전지 제조사 · 모델 · 압연 이력 · 시료 입도 분포 (169 nm · 37 nm 는 [44] 값) · AM 90 wt% 가 직접 측정인지.
- 영상: 투영 수 · 노출 · 에너지 · 문턱 값 · 필터 · 영역 확장 조건 · 첨가제 몫 · BET 로 기공률을 낸 방법 · 닫힌 기공 몫.
- 모델: 전해질 전도도 κ · 분리막 tortuosity · 거시 경계 조건 · 거시 마디 수 · 마디마다 REV 를 따로 두었는지 · REV → 거시 평균 식 · γ < 0 처리 · OCP 하한 처리 · 미시 농도 상한 · y 정의.
- τ: 경계 조건 · 메시 · x 가 두께 방향인지 · 거시에 넣은 값 (x 또는 평균) · 평균 규칙 (조화평균은 이 카드 산술).
- 계산: COMSOL 판 · 요소 수 · 시간 걸음 · 계산 시간 · 메모리 · 수렴 · 해상도 · REV 의 전기화학 수렴.
- 맞춤 · 검증: 맞춘 율 · 지표 · P2D 에도 같은 D_LFP · σ 를 썼는지 · P2D 입자 크기 (37 / 72 nm) · 실측 반복 셀 수 · 오차 막대.
- 보충 영상 Video 1 · 2 (받지 않음).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 서지: 지시서의 서지 (메인 세션이 첫 쪽에서 확인 · A. G. Kashkooli, S. Farhad, D. U. Lee, K. Feng, S. Litster, S. K. Babu, L. Zhu, Z. Chen · 제목 · J. Power Sources 307 (2016) 496–509 · DOI 10.1016/j.jpowsour.2015.12.134) = 원문 첫 쪽 · PDF 메타데이터 (title · author · subject 'Journal of Power Sources, 307 (2016) 496-509. doi:10.1016/j.jpowsour.2015.12.134') 와 같다 · 다른 점 하나: 첫 쪽 저자 표기는 **'Siddharth Komini Babu'** (지시서 'S. K. Babu') — 성이 'Babu' 인지 'Komini Babu' 인지 원문으로 가를 수 없다 (같은 논문 참고 [39] 는 'S. Komini' 로 적는다 [미확인]).  교신 저자 둘 (Farhad \* · Chen \*\*).
- 숫자: 텍스트 층 + 14 쪽 렌더로 대조 — 50 nm · 16 nm · 16 µm · 990 · 180° · 6 M · 0.5 ppm · 90 % · 40 % · 35 % · 1.13 cm² · C/5 · C/25 · 2.5–4.2 V · 30 min · 169 nm · 10 % · 728 · 750 · 707 nm · 3 % · 9 % · 3.6 · 1.5 µm · Table 1–4 전 칸 · 37 nm · 72 nm · 1.5 (Bruggeman) · 4.51 × 10⁴ · 2.9 × 10⁴ · 10 times · 10⁻⁶ · 10⁻⁸ · 10⁻² m · 10⁶ · 100 µm — 전부 위치 확인.  텍스트 층의 '5 mm each side' · '16 mm field of view' · '50 mm' · '(1/mm)' 는 렌더에서 µm (글리프 대응 문제).
- SI: Word 에서 만든 5 쪽 (Figure S1–S5 · 캡션뿐) · 그림 S3 의 SOC 0.5 · l_pos/2 칸 = SOC 0.95 · l_pos/2 칸과 같은 그림 객체 (xref 21) · 그림 S4 패널 겹침 (원문 배치).
- 판독 보정: 그림 3 의 격자선 화소 위치를 직선으로 맞춤 (a: x 잔차 ≤ 0.7 px · y 정확 · b: ≤ 0.3 px) · 두 패널 실측 3.0 V 교차 일치 (≤ 0.007 mAh/cm²) 로 재현성 확인 · 색 막대 끝값은 원 래스터 확대로 읽고 표 4 와 6/6 대조.
- 정본 중복 확인: papers/ 목록 (574 장) · 'kashkooli' · DOI '2015.12.134' · 제목 grep — 카드 없음 (wang2027 이 참고 [11] 로 인용만) · 같은 저자 · 같은 해 다른 카드 없음.

## 🔗 관련 카드
- 이 논문을 인용한 카드: [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) (참고 [11] · 서지만).
- 영상 기반 수송 · tortuosity 정의: [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) (Cooper 2014 LFP 열유속 κ · τ) · [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) · [`landesfeind2018_tortuosity_impedance_vs_tomography`](landesfeind2018_tortuosity_impedance_vs_tomography.md) · [`cooper2017_simulated_impedance_diffusion_porous_media`](cooper2017_simulated_impedance_diffusion_porous_media.md) · [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) (CT 위 정상 전도 · 접촉 저항 0).
- LIB 양극 영상 · 다중 스케일: [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) · [`zhang2023_pfib_multiscale_imaging_4d_thick_cathode`](zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md) · [`heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct`](heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct.md) · [`chouchane2019_innov_voxelization_multiphase_meshing`](chouchane2019_innov_voxelization_multiphase_meshing.md) (영상 → 다상 메시).
- LFP 나노 입자 · 다입자 모델: [`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`](eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell.md) (P2D 를 입자 크기 분포로 보정하는 같은 문제 — 그 카드의 'MPM' = many-particle model).
- 수송 대조의 깊이 기준: [`bazzoun2026_dem_fem_rnm_ionic`](bazzoun2026_dem_fem_rnm_ionic.md) (접촉망 ↔ 연속체 FEM).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
