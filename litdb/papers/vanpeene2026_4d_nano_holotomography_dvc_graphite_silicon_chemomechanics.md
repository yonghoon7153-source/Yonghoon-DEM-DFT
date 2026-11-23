<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md · 이웃 = lu2020_insitu_nanoct_calendering_microstructural_evolution.md (누른 채 nano-CT + TauFactor) ·
     dem_mechanical_stresses_ssb_electrode_cycling.md (사이클 팽창 DEM) · intergranular_cracking_nmc811_jmca2023.md (nano-CT 균열) · korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens.md (같은 그룹).
     쪽 표기 = 본문 PDF 쪽 p.1–16 (권 · 쪽 번호 없는 출판 전 판 — 머리 'Nature Nanotechnology · Article' · 'Published online: xx xx xxxx') · SI = 보충 PDF 쪽 (54 쪽 · SI 안 인쇄 쪽 번호 = PDF 쪽 − 1).
     값 표지: [인쇄] = 본문 · 캡션 · SI 글자 · 그림 안 인쇄 글자 · [원자료 MOESMn] = 보충 엑셀 (MOESM9–14 = 그림 1d–6i 의 'source data' · openpyxl 로 읽음 · 리포에 넣지 않음) ·
     [판독] = 그림에서 읽은 값 (추세만) · [카드 산술] = 인쇄 · 원자료 값으로 이 카드가 계산 (식 병기) · [카드 추론] · [카드 관찰] = 이 카드의 해석 · [미확인] = 본문 16 쪽 · SI 54 쪽 · 원자료에 없음.
     영상 6 개 (MOESM3–8 · AVI MJPEG · 1 fps) = ffprobe 로 길이 · 해상도 → ffmpeg 정지 화면 12 장 (figures/<slug>/vid_S?_t??s.png) · 영상 · 엑셀 파일은 커밋하지 않는다. -->
# 흑연–Si 복합 음극 (액체 전해질 LIB · Li 금속 반쪽 셀 · 적층압 ≈ 23 kPa) 의 첫 화성 사이클을 중단-operando 싱크로트론 X 선 나노 홀로토모그래피 (복셀 50 nm · 한 장 9 분 · 13 상태) + DVC (창 4 µm · 입자 56 개 추적) 로 본 4D 화학기계 — 두께 60 → 75 → 64 µm · 전극 ε_V 12.4 → 7.3 % · 편차 변형률 74 % 남음 · 확산 굴곡 인자 (우리 tau2 꼴) 3.31 → 3.83 → 3.51 · 입자 활성 편차의 90 % 를 국소 인자로 설명 (거시 인자만이면 45 %) · 고체전해질 · 가압 · 계산 모델 없음 — V. Vanpeene · O. Stamati · F. Cadiou · Q. Jacquet · J. Villanova · S. Lyonnard (Nature Nanotechnology 2026)

> slug `vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics` · DOI `10.1038/s41565-026-02327-6` · type `experiment (interrupted-operando synchrotron X-ray nano-holotomography ESRF ID16B · DVC local + discrete (SPAM) · image-based tortuosity factor (TauFactor) · porosity · microstructure · particle morphology — liquid-electrolyte LIB graphite–Si anode · Li metal half cell · no SE · no compaction · no DEM / MPM / FEM)` · PDF `f9daec4d-Four-dimensional_X-ray_nano-holotomography_reveals_multiscale_chemomechanics_in_composite_graphite_silicon_battery_electrodes.pdf` · digested `2026-11-23` · status ✅
>
> **저자**: **Victor Vanpeene\*** ¹ · Olga Stamati ² · Francois Cadiou ³ · Quentin Jacquet ¹ · Julie Villanova ⁴ · **Sandrine Lyonnard\*** ¹ — ¹ SyMMES (Univ. Grenoble Alpes · CEA · CNRS · Grenoble INP · IRIG) · ² 3SR (UGA · CNRS · Grenoble INP) · ³ LITEN (UGA · CEA · DEHT) · ⁴ ESRF — *Nature Nanotechnology* (2026) · **권 · 쪽 없음 (출판 전 판 · 'Published online: xx xx xxxx')** · 접수 2025-08-08 · 승인 2026-10-12 · CC BY-NC-ND 4.0 · 본문 16 쪽 (방법 p.13–16) + SI 54 쪽 (그림 S1–S24 · 표 S1–S4 · 주석 S1–S11) + 영상 6 (MOESM3–8) + 원자료 엑셀 6 (MOESM9–14) · 연구비 EU Horizon 2020 BIGMAP (957189) · CEA Science Impulse · 빔타임 ESRF 장기 과제 MA4929 · 기여: V.V. · J.V. · S.L. = 착상 / V.V. = 싱크로트론 실험 · 처리 · 초고 / O.S. · V.V. · F.C. = DVC · 영상 분석 / Q.J. · S.L. = WAXS (p.16) · 교신 = Vanpeene · Lyonnard.
> **이웃 카드 (링크만)**: [`korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens`](korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens.md) (같은 SyMMES 그룹 · Vanpeene 공저 · 순수 LPSCl 누른 채 μ-CT + ex situ 나노 홀로토모그래피 — 이 논문을 인용하지 않는다) · [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) (누른 채 nano-CT · TauFactor · 같은 '영상 → 수송' 사슬) · [`dem_mechanical_stresses_ssb_electrode_cycling`](dem_mechanical_stresses_ssb_electrode_cycling.md) (AM ±6 % 부피 팽창 · 수축 DEM) · [`gritton2017_mpm_chemomechanical_coupling_silicon_anode`](gritton2017_mpm_chemomechanical_coupling_silicon_anode.md) (규소 화학기계 MPM) · [`intergranular_cracking_nmc811_jmca2023`](intergranular_cracking_nmc811_jmca2023.md) (nano-CT 균열) · [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) (이 논문 ref 50) · [`nguyen2020_electrode_tortuosity_factor`](nguyen2020_electrode_tortuosity_factor.md) (ref 63) · [`landesfeind2016_tortuosity_eis_electrodes_separators`](landesfeind2016_tortuosity_eis_electrodes_separators.md) · [`landesfeind2018_tortuosity_impedance_vs_tomography`](landesfeind2018_tortuosity_impedance_vs_tomography.md) (refs 51 · 52) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (ref 4 · SI [18]).
> **원자료 · 크롭**: 크롭 77 장 — 그림 1–6 (6 다시 자름) · SI 그림 S1–S24 (22 다시 자름 + S17 · S18 손 크롭) · SI 표 S1–S4 (3 다시 자름 + S4 손 크롭) · 식 11 (본문 식 1–8 · SI 주석 6 · SI 식 1–2) · 근거 문단 20 · 영상 정지 화면 12 — `figures.json`.  그림 숫자는 판독 대신 **원자료 엑셀 (MOESM9–14)** 에서 옮겼다 (§3-11).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 액체 전해질 리튬이온 흑연–Si 복합 음극 (흑연 74 · nano-Si@C 11 · SBR:CMC 14 · Super C45 1 wt% · 압연 · 두께 60–65 µm · 지름 0.7 mm) 을 Li 금속 반쪽 셀 (적층압 ≈ 23 kPa 추정) 에 넣고 첫 화성 사이클 (110 mA g⁻¹ · 5 mV ↔ 1 V · 12 h) 을 한 시간마다 멈춰 ESRF ID16B 나노 홀로토모그래피 (복셀 50 nm · 시야 102 µm · 9 분) 로 13 번 찍고, 그 영상에 분할 · DVC (국소 4 µm 창 + 입자 56 개 이산 추적) · TauFactor 를 얹어 — **전극은 두께 방향으로 크게 (ε_zz 9.3 %) 옆으로 작게 (ε_yy 2.1 · ε_xx 1.0 %) 부풀고 편차 변형률의 74 % 가 남으며, 입자의 활성 (= 5 mV 에서의 입자 부피 변형률) 은 깊이보다 '빠른 기하 경로' 근접 · 전해질 접촉 면 몫이 더 강하게 가른다** 고 결론짓는다 — 고체전해질 · 압밀 · 가압 · 탈압 · 계산 모델이 없는 **측정 논문**이다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 시료 · 셀 | 흑연 (Imerys GHDR15-4 · D50 17 µm) 74 · nano Si@C (BET 48 nm) 11 · SBR:CMC (1:1) 14 · Super C45 1 wt% · 수계 슬러리 · Cu 10 µm · 압연 선하중 5 MPa (목표 기공 30–35 %) · 3.3 mAh cm⁻² · 적재 6.67 mg_Gr + 1 mg_Si cm⁻² · 레이저로 지름 0.7 mm · 두께 65 µm (방법) / 60 µm (본문) · PFA 셀 (바깥 3.14 mm · 속 1.5 mm) · Li 금속 1 mm · 유리섬유 GF/D 2 장 · 1 M LiPF₆ EC:EMC (3:7) + 10 wt% FEC 5 µl · 적층압 ≈ 23 kPa (토크 렌치 추정) | [인쇄] p.2 · p.13 |
| ② 측정 | ESRF ID16B · 원뿔빔 (초점 55 × 60 nm) 홀로토모그래피 (거리 4 개) · 29.4 keV · 3.4 × 10¹¹ ph s⁻¹ · operando 50 nm 복셀 · 시야 102 × 102 µm² · 2,205 투영 · 9 분 / ex situ 50 · 25 nm (3,203 투영 × 35 ms · 12 분) · 저배율 257 nm (시야 526 µm · 1 분 30 초) · 위상 복원 δ/β 2744 · PyHST2 · 고리 제거 · 경계 해상도 140 nm (보정 뒤) · 선량 0.52 / 0.39 MGy (전해액 / AM · 문턱 1.5 MGy) | [인쇄] p.13–14 · SI 주석 3 · 10 |
| ③ 절차 | 정전류 110 mA g⁻¹ (C/6) · 5 mV 에서 정전위 유지 · 매시간 (또는 정한 전위) 전류를 끄고 OCP 이완 (≈ 50 mV / 12 분) 중 촬영 · 다시 켜면 1 분 안에 전위 회복 · 23 ± 0.05 °C · 13 상태 (OCP · 리튬화 7 · 탈리튬화 5) | [인쇄] p.2 · p.13–14 · [원자료 MOESM9–14] |
| ④ ★ DVC (요소 · 정확도 · 정의) | SPAM · 창마다 아핀 Φ (4 × 4 · 12 미지수 · x′ = Φ·x) · 피라미드 20 → 8 → 4 µm (50 % 겹침 · 마디 2 µm) · total (OCP 기준) · 전극 질량 중심 강체 운동 뺌 · Q8 (2 × 2 × 2 마디) → F → 극분해 · **ε_V = det F − 1 (식 7) · ε_D = ‖det(F)^(−1/3) U − I‖ (식 8)** · 이산 DVC = 입자 바운딩 박스 창 · 불확도: 국소 4 µm 창 ε_zz 0.14 · ε_xx 0.21 · ε_yy 0.24 · ε_V 0.36 · ε_D 0.53 % [원자료 오차 칸] · 이산 ≈ 0.26 % (20 입자 · 무충방전 두 스캔) · **변위 정확도 (µm) = [미확인]** | [인쇄] p.15–16 · SI 주석 11 · [원자료 MOESM11 · 13] |
| ⑤ ★ 전극 변형 | 두께 **60 → 75 → 64 µm** [인쇄 그림 1e 렌더 표지] (+25.0 % / 끝 +6.7 % [카드 산술]) · DVC 평균 ε_zz **9.32** · ε_yy 2.08 · ε_xx 0.98 % (5 mV) → 5.87 · 1.21 · 0.23 % (1 V) · **ε_V 12.42 → 7.35 %** · **ε_D 7.23 → 5.38 % (74 % 남음)** [원자료 MOESM11] ↔ 본문 'ε_zz 8.8 · ε_xx 1.24 · ε_yy 2.43 %' (원자료로 재현 안 됨 · §11) | p.5 · 그림 3 |
| ⑥ 상분율 · 기공 | OCP 흑연 64.7 %v · 기공 + 바인더/Si 35.3 %v (= 입자 사이 23 + 입자 안 12) · 리튬화 끝 기공 상대 변화 **−17.16 %** → 1 V −1.60 % · ⚠ 흑연 상대 변화 = −0.627 × 기공 상대 변화 (13 상태 모두 · 두 곡선은 한 측정) [카드 산술] · '기공' 에 CBD–Si 군집이 들어 있다 (SI 주석 4) | [인쇄] p.2 · SI 표 1 · [원자료 MOESM10] |
| ⑦ Si | CBD–Si 군집 회색값 봉우리 면적 (Si 부피 대리) **+116.0 ± 23.2 %** (5 mV) → +22.1 ± 17.3 % (1 V) [원자료] (본문 '120 %' · '+30 %') · 해상 Si 4.1 %v ↔ 이론 18 %v → **Si 의 75 % 는 영상에서 안 보인다** | p.2–3 · 그림 2f |
| ⑧ ★ 입자 | 164 → 66 (가장자리 제외) → **56 개 (85 %) 추적** · 고체의 45.5 %v · 등가 지름 11.3 ± 2.39 µm · 내부 기공 24.7 ± 4.72 % · 전해질 접촉 면 몫 79.1 ± 6.79 % · 입자 평균 ε_V 11.63 % (5 mV) → 7.45 % (1 V) · 깊이 띠 평균 차 ≤ 1.4 %p (5 mV) · 입자 하나 최대 ≈ 17.6 % (#28 · 0.122 V) | p.6–7 · SI 그림 15 · [원자료 MOESM13] |
| ⑨ 수송 | **tortuosity factor (우리 tau2 · 수송 tortuosity)** 두께 방향 3.31 → 3.83 (5 mV) → 3.51 (1 V) · 면내 2.38 → 2.68 → 2.40 [원자료 MOESM12] · McMullin 9.4 = τ/ε [인쇄 · 3.3125/0.353 = 9.38 카드 산술] · 기하 τ_geo 두께 1.36 · 면내 1.21 [인쇄 SI 표 1] · 빠른 기하 경로 (L_geo/L_E < 1.2) 9 → 3 (0.122 V) → 13 개 [원자료] | p.5–6 · 그림 4 |
| ⑩ 영향 인자 | 활성: 빠른 경로 근접 IF **1.00** · 전해질 접촉 0.585 · 깊이 −0.539 · 국소 흐름 −0.294 · 내부 기공 0.286 · CBD–Si −0.160 · 기하 τ −0.160 / 비가역: 비가역 편차 변형률 −0.855 · 빠른 경로 거리 −0.789 · 이웃 수 +0.714 · 최대 ε_V −0.642 · CBD–Si 거리 +0.461 [원자료 MOESM14] · 설명 몫 **90 % ↔ 거시 인자만 45 %** [인쇄 p.10] | 그림 6 · SI 그림 18 · 표 S3 |
| ⑪ 균열 · 박리 | 균열 **정량 없음** — 흑연 판 벗겨짐 (exfoliation) · 입자 안 새 기공 (정성 · p.2) · DVC 잔차에 비선형 변화 없음 = 56 입자 붙음 · 사라짐 없음 (p.16) · 집전체 박리 *"no delamination was qualitatively observed"* (p.5) · 바인더 파괴 가능성 = 문헌 CMC 7 % 인장 변형률 (SI 주석 7 · 2 차 인용) | p.2 · p.5 · p.16 · SI 주석 4 · 7 |
| ⑫ 계산 · DEM | DEM · MPM · FEM · 압밀 계산 **없음** (TauFactor 정상 확산만) · DEM 의 한계를 말한 문장 **없음** · '평균 기술자 모델은 3D 복잡성을 못 담는다' 는 일반 문장만 (p.1 refs 2–4 · SI 주석 9 refs 17–18 — 그 [4] · [18] = Ngandjong 2021 DEM 디지털 트윈) | §4-7 |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB · 흑연–Si 음극** — 고체전해질 없음 · 우리 (LPSCl + NCM811 양극 · 고체) 와 재료 · 전해질 · 극이 다 다르다 ② **가압 없음** — 셀 적층압 ≈ 23 kPa (토크 렌치 추정 · 측정 아님) = 우리 300 MPa 의 ≈ 1/13 000 [카드 산술] ③ 하중 = **리튬화 팽창 (화학 하중)** · '되돌아옴' = 탈리튬화 수축 (압력 제거 아님) ④ **한 셀 · 한 사이클 · 한 부피** (분할 102 × 102 × 40 µm³) — 빔 밖 쌍둥이 셀은 처음 · 끝 두 영상뿐 ⑤ '기공' = 기공 + CBD–Si (해상도 밑 Si · 바인더 · 탄소) ⑥ '활성' = 5 mV 입자 부피 변형률의 **대리** (전류 · SOC 를 재지 않음) ⑦ 본문 숫자 여럿이 원자료 · SI 와 어긋난다 (§11) · 원자료 값도 그림 좌표 격자에 놓인다 (§3-11).
⇒ **절대값 전이**: 없다 (재료 · 전해질 · 하중 종류 · 압력이 모두 다르다).  옮길 것은 **방법** — (a) DVC 변형률 정의 (식 7–8) · total · 강체 운동 뺌 규약을 우리 MPM 장 후처리에 그대로 (b) 입자 번호를 붙인 채 입자마다 아핀 F 를 재는 이산 DVC = 우리 Ⓑ (DEM → MPM) '입자 형태 변형' 의 측정 꼴 (c) REV 절차 · 경계 반치폭 해상도 · 해상도 밑 상 장부 (d) 이웃 수 (배위수) ↔ 비가역 변형률 상관 = DEM 이 바로 내는 양의 실측 대조 꼴 (흐름 밖).

---

## 0-1. ★ 고른 의도 대조 (후보 표 행 아님 — 1저자 11-23 업로드)

의도 원문: *"논문에이전트 하고 잘 크롭핑해서 litdb로 보내줘용"* (두 편 중 하나 · 후보 표 · 가리킨 카드 없음) + 지시서 '이 논문만의 덧붙임' (꼭 뽑을 것 · 견줄 자리).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "잘 크롭핑해서 litdb 로" | **채움** | 그림 6 · SI 그림 24 · SI 표 4 **전부** + 식 11 + 근거 문단 20 + 영상 정지 화면 12 = 77 장 · 자동 크롭이 패널 글자 · 반쪽을 놓친 본문 그림 6 장은 다시 자름 · 도구가 놓친 SI 그림 S17 · S18 (그림 쪽과 캡션 쪽이 다름) · SI 표 S4 (표 S3 크롭 안에 섞임) 는 손 크롭 |
| 시료: 흑연 : Si 비 | **채움** | 74 : 11 wt% [인쇄 p.2 · p.13] · 적재 6.67 mg_Gr : 1 mg_Si cm⁻² (p.13) · 해상 부피분율 Si 4.1 %v ↔ 이론 18 %v (p.2) |
| 바인더 · 도전재 | **채움** | SBR:CMC (1:1) 14 wt% (SBR Zeon BM-451B 40 % · CMC Chempoint W2000 3 %) · Super C45 1 wt% (D50 100–200 nm · BET 45 m² g⁻¹) (p.13) |
| 두께 | **채움 (값 여럿)** | 60 µm (본문 p.2 그림 1e · 방법 p.14 '60-µm height' · WAXS p.14 '60 µm') · 65 µm (방법 p.13 '평균 두께') · 62 µm (SI 그림 3 SEM 표지) · 63 µm (SI 그림 10 표지) |
| 기공률 | **채움 (정의 한정)** | 35 %v = 입자 사이 23 + 입자 안 12 (OCP · p.2) · 35.3 %v '기공 + 바인더/Si' (SI 표 1 · 50 nm · 젖은 operando) · 압연 사양 30–35 % (p.2 · p.13) · ⚠ CBD–Si 군집을 전해질로 셌다 (SI 주석 4) |
| 셀 꼴 | **채움** | 자체 PFA 셀 바깥 3.14 mm · 길이 35.2 mm · 속지름 1.5 mm · 벽 0.8 mm · 스테인리스 커넥터 (아래 24.2 · 위 11 mm) · UV 접착 밀봉 · Li 1 mm (750 µm 판에서 펀칭) · Cu 집전체 1 mm · 240 µm · 분리막 GF/D 2 장 (지름 2 mm · 670 µm · 기공 2.7 µm) · 적층압 ≈ 23 kPa (p.13) |
| 전해질 | **채움** | 1 M LiPF₆ EC:EMC (3:7) + 10 wt% FEC · 5 µl (p.13) · WAXS 셀 = LP57 (FEC 없음 · p.14) |
| 측정: 빔라인 · 에너지 | **채움** | ESRF ID16B · 29.4 keV · 3.4 × 10¹¹ ph s⁻¹ · 초점 55 × 60 nm (p.13–14) — ⚠ 그림 1a '50 × 50 nm²' |
| 화소 · 시야 | **채움** | operando 50 nm · 102 × 102 µm² (p.2 · p.14) — SI 표 1 · 2 캡션은 '108 × 108 µm²' · 저배율 257 nm · 526 µm · ex situ 25 nm · 51 µm (방법) / 52 µm (SI 그림 2 캡션) · 경계 해상도 140 nm (보정 뒤) · 180 nm (원 영상) (SI 주석 10) |
| 스캔 시간 | **채움** | 9 분 = 거리 4 개 × 1.5 분 + 거리마다 45 초 안정 (SI 주석 3) · 2,205 투영 (p.14) · ex situ 12 분 · 3,203 투영 × 35 ms |
| 중단-operando 절차 | **채움** | 매시간 또는 정한 전위에서 전류를 끄고 OCP 이완 중 촬영 · 이완 ≈ 50 mV / 12 분 · 전류 다시 켜면 1 분 안에 회복 · 23 ± 0.05 °C (p.13–14) · 빔 영향: 첫 노출 +30 mV · 누적 7 분 노출 뒤 +50 mV (SI 주석 3) |
| 충방전 조건 | **채움 (전류값 어긋남)** | 110 mA g⁻¹ (C/6) · 5 mV ↔ 1 V · 5 mV 정전위 유지 · 12 h (p.2 · p.13–14 · SI 주석 3) · 전류 **20 µA** (방법 p.14) ↔ **5.15 µA** (그림 1 캡션) ↔ 지름 0.7 mm · 적재량으로 ≈ 3.25 µA [카드 산술 §11] |
| DVC 요소 크기 | **채움** | 4 µm 창 · 2 µm 마디 · 50 % 겹침 · 피라미드 20 → 8 → 4 µm (p.15 · SI 주석 11 · SI 그림 22) |
| 변위 정확도 | **없음 (변위 단위)** · 일부 (변형률) | 변위 불확도 (µm) 숫자 없음 · 변형률 불확도만: 국소 4 µm 창 (원자료 오차 칸 · SI 그림 21 과 같은 크기 [판독 대조]) · 이산 ≈ 0.26 % (SI 주석 11) · 그림 5c 원자료의 이산 오차 칸 0.119 % |
| 변형률 정의 | **채움** | 식 7 · 8 (p.16) · Q8 · 극분해 · total (OCP 기준) · 강체 운동 뺌 (p.15 · 그림 3 캡션) |
| 정량: 입자 | **채움** | §3-8 |
| 전극 부피 변화 · 두께 변화 | **채움** | ε_V 12.42 → 7.35 % [원자료] · 두께 60 → 75 → 64 µm [인쇄 그림 1e] (측정 방법 · 위치 [미확인]) |
| 변형률 장 | **채움** | 그림 3d–e · 영상 S3 · S4 · SI 그림 17 |
| 기공률 변화 | **채움** | §3-4 · §3-5 |
| 균열 | **일부 (정성만)** | 판 벗겨짐 · 입자 안 새 기공 (p.2) · 잔차 비선형 없음 (p.16) — 크기 · 개수 · 검출 문턱 없음 |
| 박리 | **채움 (정성 '없음')** | p.5 · SI 주석 4 · SI 그림 10 · 입자–바인더 탈착 *"is prone to occur"* (SI 주석 7 · 추론) |
| 식 번호별 크롭 | **채움** | 본문 식 (1)–(8) + SI 주석 6 (Sneed–Folk) · SI 식 1 · 2 |
| 보충 영상 6 개 | **채움** | §3-10 — S1–S5 는 본문이 가리킴 · **S6 (MOESM8) 은 본문 · SI 어디에도 언급 없음** · SI 에 영상 설명 없음 (영상 S? = 무엇은 본문 언급 + 정지 화면으로 정함) |
| 원자료 엑셀 6 개 | **채움** | §3-11 (MOESM9 = 그림 1d … MOESM14 = 그림 6f–i) |
| 견줄 자리 (사이클 화학기계 · DEM 반경 · 부피 진동 선례 · DEM ↔ MPM · 해상도 ↔ 격자) | **채움 (방법 · 정성)** | §7-3 · §7-4 · §8 |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음** | 후보 표 행 · 가리킨 카드 없음.  정본의 'Vanpeene' (korjus2025 카드 L13 · L76 · L389 · INDEX.md L228 · reading/batch_61) = **Korjus 2025 (Energy Storage Mater. 82, 104589) 의 공저자 이름** — 이 논문 · 다른 Vanpeene 1 저자 논문의 인용이 아니다 (그 카드 · batch_61 에 'ACS Nano' · 's41565' 0 회 · 카드의 'nano-holotomography' = Korjus 자신의 ex situ 382 MPa 펠릿 측정) |

⇒ **의도 대조 결과: 일부 (거의 채움)** — 시료 · 측정 · 절차 · DVC 정의 · 전극 · 입자 · 기공 · 영상 · 원자료는 있다; **변위 정확도 (µm) 와 균열 정량은 원문에 없다**.

---

## 1. 한 줄 요약
흑연–Si 복합 음극의 '평균 기술자 (입도 · 기공률) 로는 안 잡히는 3D 다척도 복잡성' 을 겨냥해, 자체 소형 Li 금속 셀 (PFA · 지름 3.14 mm) 을 ESRF ID16B 에 올려 첫 화성 사이클을 13 번 멈춰 찍는다 (50 nm · 9 분).  분할 (Ilastik) 로 흑연 · 기공 (입자 사이 / 안) · CBD–Si 를 나누고, 국소 DVC (4 µm) 로 전극 변형률 장을, 입자 라벨 + 이산 DVC 로 56 입자의 부피 · 편차 변형률을, 측지 거리 지도 + TauFactor 로 기하 · 확산 tortuosity 와 '빠른 기하 경로' 를 잰다.  결과: 두께 방향 우세의 비등방 팽창 (ε_zz 9.3 ≫ ε_yy 2.1 > ε_xx 1.0 %) · 편차 변형률 74 % 비가역 · 5 mV 아래 Si 활동과 함께 기공 −17 % · tortuosity factor 3.31 → 3.83 → 3.51 · 빠른 경로 9 → 13 · 입자 활성은 빠른 경로 근접 (IF 1.0) 이 깊이 (0.54) 보다 강하고, 이웃 흑연 입자 > 10 개는 비가역을 줄인다 — 국소 인자 열넷으로 입자 편차의 90 % (거시 인자만이면 45 %) 를 설명한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| V. Vanpeene\* · O. Stamati · F. Cadiou · Q. Jacquet · J. Villanova · S. Lyonnard\* (Grenoble SyMMES · 3SR · LITEN · ESRF) | Nature Nanotechnology (2026) · 권 · 쪽 없음 (출판 전 판) · 본문 16 + SI 54 쪽 | 10.1038/s41565-026-02327-6 | **SE 없음 · CAM 없음** — 액체 전해질 LIB **음극**: 흑연 74 + nano-Si@C 11 + SBR:CMC 14 + Super C45 1 wt% · Li 금속 반쪽 셀 (WAXS 는 LiNiO₂ 전전지) | 실험 — 중단-operando 나노 홀로토모그래피 + DVC + 영상 기반 정상 확산 (TauFactor) + operando WAXS + 동전지 100 사이클 대조 — **역학 · 압밀 계산 없음** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 시료 · 셀 (p.13 · p.2)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 흑연 | 합성 탄소코팅 흑연 C-NERGY Actilion GHDR15-4 (Imerys · 99.95 %) · D50 17 µm · BET 4.1 m² g⁻¹ · '기공률 사양 없음' · 74 wt% · 영상 평균 지름 12 µm (p.2) · 추적 입자 등가 지름 11.3 µm (p.7) | [인쇄] p.13 · p.2 · p.7 |
| Si | nano Si@C · BET 48 nm · 11 wt% · O 2 % · C 1.69 % · 공칭 200 nm (p.2) · CBD–Si 군집 5–15 µm | [인쇄] p.13 · p.2 |
| 바인더 · 도전재 | SBR:CMC (1:1) 14 wt% · Super C45 1 wt% (D50 100–200 nm) | [인쇄] p.13 |
| 공정 | 수계 (고체 : 액 = 1 : 0.8) · 5 L 유성 믹서 · Coatema 롤투롤 블레이드 코팅 · 70 / 80 / 90 °C 건조 · **간극 모드 압연 선하중 5 MPa (목표 30–35 %)** · CIDETEC (BIGMAP) 제조 | [인쇄] p.13 |
| 용량 · 적재 | 3.3 mAh cm⁻² = '670 mAh g⁻¹' (흑연 가역 364 mAh g⁻¹ · 첫 쿨롱 효율 93 %) · 6.67 mg_Gr cm⁻² · 1 mg_Si cm⁻² — 세 수가 닫히지 않는다: 3.3 ÷ 7.67 mg cm⁻² = 430 mAh g⁻¹ [카드 산술] | [인쇄] p.13 |
| 시편 | 펨토초 레이저 절단 지름 0.7 mm · 평균 두께 65 µm · 80 °C 진공 24 h 건조 | [인쇄] p.13 |
| 셀 | PFA 몸체 (바깥 3.14 mm · 속 1.5 mm · 벽 0.8 mm · 길이 35.2 mm) · 316L 커넥터 나사 (아래 L 24.2 · 위 11 mm) · **'constant pressure (23 kPa estimated with a dynamometric wrench)'** · UV 경화 접착 밀봉 · 글러브박스 H₂O · O₂ ≤ 0.5 ppm | [인쇄] p.13 |
| 반대극 · 분리막 · 전해액 | Li 금속 (750 µm 판 · 지름 1 mm) on Cu (1 mm · 240 µm) · GF/D 2 장 (지름 2 mm · 670 µm · 기공 2.7 µm) · 1 M LiPF₆ EC:EMC (3:7) + 10 wt% FEC 5 µl | [인쇄] p.13 |
| WAXS 셀 (다른 셀) | Swagelok PFA 속 3 mm · 스프링 6.2 N (→ ≈ 0.88 MPa [카드 산술: 6.2 N ÷ π(1.5 mm)² · 속지름 3 mm 전면에 걸린다고 가정]) · Gr–Si ‖ LiNiO₂ (94 wt% · 3.1 mAh cm⁻²) · GF/A 260 µm · LP57 · 22.5 mA g⁻¹ (C/10 · C = 225 mAh g_LNO⁻¹) · 4.4 V 까지 | [인쇄] p.14 |
| 동전지 대조 (SI 그림 7) | CR2032 · LiNiO₂ 3.1 ‖ Gr–Si 3.44 mAh cm⁻² · Celgard 2500 · 50 µl · 7 kN 압착 · 화성 3 회 (CC-CV, I < 11.2 mA g⁻¹ · CC 22.5 mA g⁻¹ · 2.5–4.2 V · 25 °C) 뒤 1 C 100 회 · 5 셀 평균 · 방전 용량 ≈ 200 대 → ≈ 50 mAh g⁻¹ [판독 · 추세만] | [인쇄] p.13 · SI 그림 7 |

### 3-2. 측정 · 영상 처리 (p.13–14 · SI 주석 1 · 3 · 4 · 10)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 빔 | ESRF ID16B · 홀로토모그래피 (원뿔빔 · 기하 확대) · 초점 H 55 × V 60 nm · 29.4 keV · 3.4 × 10¹¹ ph s⁻¹ | [인쇄] p.13–14 |
| 검출기 | PCO edge 5.5 CMOS (2,048 × 2,048) · 30 µm LSO 섬광체 · 기준 20 · 암 21 장 | [인쇄] p.14 |
| 배율 사다리 | 257 nm (시야 526 µm · 1 분 30 초 · in situ) · 50 nm (102 µm) · 25 nm (51 µm) ex situ 각 12 분 · 3,203 투영 × 35 ms · 360° | [인쇄] p.13–14 |
| operando | 시료 ↔ 초점 52 mm · ↔ 검출기 280 mm · 50 nm · 시야 102 × 102 µm² · 투영 2,205 · **9 분** · 거리 4 개 | [인쇄] p.14 |
| 재구성 | Paganin 꼴 위상 복원 (δ/β 2744 · 자체 octave) → PyHST2 여과 역투영 · 32 bit → 고리 제거 (극좌표 중간값 + 가우스 · MATLAB) · 16 bit | [인쇄] p.14 |
| 화질 | 경계 해상도 (회색값 미분 반치폭) 140 nm (보정 뒤) · 180 nm (원) · CNR 6.1 → 10.4 (SI 표 4 · 그림 S19) ↔ SI 주석 10 글 'from 10.2 to 12.8' | [인쇄] SI 주석 10 · 표 S4 |
| REV | 257 nm 영상 377³ µm³ 에서 무작위 부분 부피 10 개 · 한 변 23–350 µm (25 µm 간격 · 방법 p.14 는 '22 to 250 µm') · '95 % 신뢰 · 오차 < 5 %' 최소 = **90³ µm³** → operando 102³ µm³ 택함 | [인쇄] SI 주석 1 · SI 그림 1 |
| 분석 부피 | 재구성 102³ µm³ (전극 = 60 µm 높이) · 분할 · DVC = 102 × 102 × 40 µm³ (집전체 근처 위상 인공물 제외) · CBD–Si = 20 × 20 × 13 µm³ × 3 (SI 주석 4 = 20 × 20 × 10 µm³ × 5) · tortuosity = 62 × 62 × 40 µm³ · 입자 라벨 = 깊이 5–40 µm | [인쇄] p.14 · SI 주석 4 |
| 분할 | Ilastik 랜덤 포레스트 (흑연 · 기공 · CBD–Si) · 입자 안 기공 = 최대 필터 (2 복셀 × 3 회 (방법) / 4 회 (SI 주석 4)) 로 메운 뒤 남은 것 = 입자 사이 · CBD–Si 는 전해질로 셈 · 회색값 정렬 기준 = 분리막 전해질 봉우리 | [인쇄] p.14–15 · SI 주석 4 |
| 선량 | 전 실험 전해액 0.52 · AM 0.39 MGy (< 1.5 MGy) · WAXS 흑연 2 · Si 3 MGy (*"below the reported threshold"*) | [인쇄] SI 주석 3 · p.14 |

### 3-3. 전기화학 (그림 1d · 원자료 MOESM9 · 5,519 행)
- 최대 비용량 **761.8 mAh g⁻¹** (t 6.93 h · 5.02 mV) — CC 로 5.1 mV 에 닿은 때 679.8 mAh g⁻¹ (6.19 h) · **5 mV 정전위 유지가 82.2 mAh g⁻¹ 를 더함** [원자료 · 카드 산술] (그림 2–4 의 'C = 760 mAh g⁻¹').
- 끝 (1.0 V · 11.71 h) **237.4 mAh g⁻¹** → 탈리튬화 524.4 mAh g⁻¹ · **첫 쿨롱 효율 68.8 %** [카드 산술: (761.8 − 237.4)/761.8] — 방법의 '첫 쿨롱 효율 93 %' (전극 · 흑연 사양 문장) 와 다른 양 [카드 추론].
- 기울기 dC/dt = +109.85 / −109.85 mAh g⁻¹ h⁻¹ (리튬화 · 탈리튬화) = 110 mA g⁻¹ [카드 산술].
- 전위 이정표 (리튬화): 0.1 V 첫 도달 1.31 h (143 mAh g⁻¹) · 35 mV 3.44 h (378) · 20 mV 5.13 h (563) / (탈리튬화) 0.15 V 8.84 h (553) · 0.175 V 10.01 h (424) · 0.25 V 11.05 h (309) · 0.5 V 11.54 h (256) [원자료].
- 촬영 13 상태 (원자료 공통 시간 축): 0 h 2.53 V (OCP) · 1–7 h 0.130 · 0.065 · 0.063 · 0.036 · 0.031 · 0.021 · 0.005 V (리튬화) · 8–11 h 0.122 · 0.151 · 0.168 · 0.237 V · 11.67 h 1.0 V (탈리튬화) [원자료 MOESM10–13].
- WAXS: Si 는 흑연 stage 2/2L 이 순수할 때 (≈ 600 mAh g⁻¹) 주로 · 완전 리튬화 (≈ 800 mAh g⁻¹) 에서 덜 반응 (p.5 · SI 그림 5) — LNO 전전지 · 다른 셀 · C/10 이라 nano-CT 와 같은 시료 아님 (SI 주석 2).
- 빔 영향 · 재현: X 선 노출마다 +30 mV (가역) · 누적 +50 mV (SI 그림 6a) · operando ↔ 빔 밖 쌍둥이 셀 전위 곡선 겹침 (SI 그림 6b) — ⚠ 그 그림의 탈리튬화 곡선은 ≈ 135–145 mAh g⁻¹ 에서 1 V 에 닿는다 [판독] ↔ 원자료 MOESM9 237.4.

### 3-4. ★ 상분율 · 기공 (그림 2a–c · SI 그림 8 · SI 표 1–2)
- OCP: 입자 사이 23 %v + 입자 안 12 %v = 35 %v (*"in agreement with electrode specifications after calendering (30–35%)"* p.2) · SI 표 1 (50 nm · 시야 '108 µm'): 건조 ex situ 흑연 64.6 / 기공 + 바인더/Si 35.4 · operando 64.7 / 35.3 · 빔 밖 64.8 / 35.2 %v · 257 nm 에서 65.6 / 34.4 · 65.5 / 34.5 · 66.3 / 33.7 [인쇄].
- 평균 기공 크기는 해상도에 강하게 달린다: 50 nm 0.91 µm ↔ 257 nm 3.04 µm (operando · ×3.3 [카드 산술]) — 상분율은 ±0.8 %v 안.
- 리튬화: 60 mV 이상에서 흑연 · 기공 '균형' (전극 부풂) · 35 mV 아래 (Si 활동) 기공 **−7.5 → −17 %** (p.2) · 원자료: −7.42 (36 mV) → −17.16 % (5 mV) [MOESM10].
- 탈리튬화: 175 mV 를 넘어 −10 → −2.5 % 큰 계단 (p.2) · 원자료 −10.25 (168 mV) → −2.80 (237 mV) → −1.60 % (1 V).
- 본문 기공 두 종: 리튬화 입자 안 몫 '40 %' → 35 mV 아래 '20 %' → 탈리튬화 끝 '50 %' · 입자 안 +18 % · 입자 안 평균 기공 280 → 420 nm · 입자 사이 −15 % · 흑연 판 벗겨짐 (p.2 · SI 그림 8) — ⚠ 원자료의 입자 안 몫 (입자 안 변화 ÷ 전체 변화) 은 **OCP 뒤 12 상태 모두 18.8–23.0 %** (20 % 만 맞음 · 40 · 50 % 재현 안 됨) · 또 원자료의 입자 안 기여 (입자 안 + 입자 사이 = 전체 기공 상대 변화 · 13 상태 모두 덧셈 성립) 는 끝 (1 V) 까지 **음수 (−0.33 %)** — 본문 '입자 안 기공이 OCP 수준을 넘는다 (+18 %)' 와 부호가 반대.  SI 그림 8a [판독 · 점 위치] 는 본문 쪽이다: 입자 안 ≈ −23 % (5 mV) → ≈ +19 % (1 V) · 사이 ≈ −14 → ≈ −14.5 % — 그 두 값을 OCP 입자 안 : 사이 = 12 : 23 으로 더하면 5 mV 전체 ≈ −17.1 % (원자료 −17.16 과 맞음) 인데 입자 안 몫은 ≈ 46 % [카드 산술] → 그림 2b–c 원자료 (몫 20.6 %) 와 SI 그림 8a 는 입자 안 · 사이를 다르게 가른 두 결과다 [카드 추론 · 어느 쪽이 본문 숫자의 근거인지 [미확인]] [원자료 MOESM10 · 카드 산술].
- ⚠ **흑연과 기공의 상대 변화는 한 측정이다**: 흑연 Δ = −0.627 × 기공 Δ 가 12 상태 모두 소수 셋째 자리까지 같다 [카드 산술] — 고정된 분석 상자 안 이진 분할 (흑연 + 기공 = 1) 의 닫힘 (비 0.627 은 그 상자의 기공 : 흑연 ≈ 0.385 : 0.615 를 뜻한다 [카드 산술 · 두 상 닫힘 가정] · 35.3 : 64.7 이면 0.546).
- 화성 끝 (SI 표 2 · 50 nm): operando 흑연 64.7 → 65.3 %v · 입자 크기 11.3 → 12.2 µm · 평균 기공 0.91 → 0.78 µm · τ_geo 1.21/1.36 → 1.21/1.4 · τ_diff 2.38/3.31 → 2.40/3.51 · 빔 밖 쌍둥이 64.8 → 65.6 · 11.7 → 12.8 · 0.83 → 0.75 · 1.20/1.32 → 1.20/1.36 · 2.25/3.02 → 2.22/3.25 [인쇄].

### 3-5. ★ 상태별 원자료 한 표 (MOESM10–13 · 13 상태)
| t (h) | E (V) | 흑연 Δ % | 기공 Δ % | 입자 안 몫 % [카드 산술] | CBD–Si 봉우리 Δ % (± SD) | ε_zz | ε_xx | ε_yy | ε_V | ε_D | 입자 평균 ε_V (이산) | τ 두께 | τ 면내 | 빠른 경로 수 | 빠른 경로 / 기공 % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2.53 (OCP) | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3.31 | 2.38 | 9 | 5.86 |
| 1 | 0.130 | 3.06 | −4.88 | 23.0 | 7.0 ± 4.9 | 2.73 | 0.15 | 0.16 | 2.95 | 2.35 | 2.55 | 3.43 | 2.52 | 9 | 5.97 |
| 2 | 0.065 | 3.75 | −5.98 | 22.7 | 13.5 ± 3.5 | 4.73 | 0.30 | 0.45 | 5.23 | 3.79 | 4.56 | 3.50 | 2.43 | 8 | 4.82 |
| 3 | 0.063 | 3.97 | −6.33 | 23.0 | 29.8 ± 8.6 | 5.04 | 0.38 | 0.53 | 5.83 | 4.62 | 4.63 | 3.26 | 2.27 | 7 | 4.15 |
| 4 | 0.036 | 4.66 | −7.42 | 21.8 | 43.4 ± 9.9 | 5.42 | 0.42 | 0.79 | 6.52 | 4.55 | 5.56 | 3.39 | 2.34 | 5 | 3.22 |
| 5 | 0.031 | 5.27 | −8.39 | 22.2 | 60.0 ± 18.8 | 5.87 | 0.49 | 1.06 | 7.46 | 6.29 | 6.40 | 3.08 | 2.21 | 8 | 4.68 |
| 6 | 0.021 | 6.97 | −11.12 | 22.8 | 87.9 ± 17.4 | 7.27 | 0.64 | 1.52 | 9.39 | 6.25 | 7.88 | 3.21 | 2.29 | 9 | 5.00 |
| 7 | **0.005** | **10.77** | **−17.16** | 20.6 | **116.0 ± 23.2** | **9.32** | **0.98** | **2.08** | **12.42** | **7.23** | **11.63** | 3.83 | 2.68 | 6 | 3.17 |
| 8 | 0.122 | 10.85 | −17.29 | 19.8 | 110.1 ± 34.7 | 8.94 | 0.87 | 1.93 | 11.78 | 7.05 | 11.84 | **3.86** | 2.48 | **3** | **1.52** |
| 9 | 0.151 | 8.79 | −14.02 | 19.5 | 93.1 ± 28.6 | 8.03 | 0.64 | 1.70 | 10.57 | 6.48 | 10.55 | 3.60 | 2.37 | 6 | 2.65 |
| 10 | 0.168 | 6.43 | −10.25 | 18.8 | 86.6 ± 25.8 | 7.65 | 0.57 | 1.63 | 9.89 | 6.29 | 9.34 | 3.63 | 2.38 | 5 | 2.02 |
| 11 | 0.237 | 1.76 | −2.80 | 21.6 | 29.6 ± 13.0 | 7.23 | 0.49 | 1.59 | 9.39 | 6.06 | 8.56 | 3.57 | 2.39 | 10 | 5.44 |
| 11.67 | **1.0** | 1.01 | −1.60 | 20.4 | 22.1 ± 17.3 | 5.87 | 0.23 | 1.21 | **7.35** | **5.38** | **7.45** | 3.51 | 2.40 | **13** | 5.78 |
- 전부 [원자료] (MOESM10 그림 2b–c · 2f / MOESM11 그림 3b–c / MOESM12 그림 4e–f / MOESM13 그림 5c) · 변형률 단위 % · ε 오차 칸 = 상태마다 같은 상수 (ε_zz 0.14 · ε_xx 0.21 · ε_yy 0.24 · ε_V 0.36 · ε_D 0.53 · 이산 ε_V 0.119 %).
- 끝/최대 [카드 산술]: ε_zz 0.63 · ε_yy 0.58 · ε_xx 0.23 · ε_V 0.59 · ε_D **0.743 (본문 '74 %' ✓)** · 5 mV 에서 ε_zz + ε_xx + ε_yy = 12.39 ≈ ε_V 12.42 (작은 변형 근사와 맞음).
- ⚠ 같은 양 '국소 DVC 평균 ε_V' 가 두 원자료에서 0.237 V 상태만 다르다: 9.39 (MOESM11 그림 3c) ↔ 8.13 (MOESM13 그림 5c) — 나머지 상태의 차는 ≤ 0.15 %p (0.151 V 0.13 · 1 V 0.15 %p) [원자료 관찰].

### 3-6. ★ 전극 규모 변형 (그림 1e · 그림 3 · 영상 S2–S4)
- 변위: 전극이 **질량 중심에서 분리막 쪽 · 집전체 쪽으로** 함께 부풀고 줄어든다 (p.5 · 그림 3a · 화살표 ×10 · 강체 운동 뺌).
- 비등방: *"highly anisotropic electrode deformation, dominated by the through-thickness component (ϵzz = 8.8%; Fig. 3b)"* · *"(ϵxx = 1.24%, ϵyy = 2.43%)"* (p.5) — 원자료 최댓값은 9.32 · 0.98 · 2.08 % · 13 상태 평균 6.01 · 0.47 · 1.13 % [카드 산술] · 끝 5.87 · 0.23 · 1.21 % → 본문 세 수는 원자료의 최댓값 · 13 상태 평균 · 끝값 어느 것과도 맞지 않는다 (ε_xx 1.24 · ε_yy 2.43 은 원자료 최댓값보다 크다 · §11).  *"Notably, the ϵyy component exhibits large irreversibility"* (p.5) — 원자료 끝/최대 ε_yy 0.58 · ε_zz 0.63 (ε_zz 도 비슷하게 크다) [카드 산술].
- 두께 (그림 1e 렌더 표지): 60 → 75 → 64 µm = **+25.0 % → +6.7 %** [카드 산술] ↔ DVC 평균 ε_zz 최대 9.3 % — 2.7 배 차 (DVC = 40 µm 부분 부피 · 집전체 근처 제외 · 강체 운동 뺌 · 두께 측정 방법 [미확인]) [카드 산술 · 해석 [미확인]].
- 편차 변형률: 리튬화에서 70 · 35 · 20 mV 계단 (흑연 stage 고원과 대응 · p.5) · *"important irreversibility (74%) of the deviatoric contribution is measured after formation"* (p.5).
- 장 (그림 3d–e · 영상 S3 · S4): *"both volumetric and deviatoric strain fields are rather homogeneous"* · 열점 = CBD–Si 군집 근처 (높은 부피 + 전단) · 흑연 입자 계면의 높은 전단 · 분리막 쪽 계면 전단 (*"mechanical incompatibility between the compliant separator and dynamically expanding and contracting electrode"*) · Cu 집전체 쪽은 박리 가능성을 말하나 *"no delamination was qualitatively observed in our case"* (p.5).
- 창 크기: *"4–40 times smaller correlation window size compared with standard mesoscale DVC works"* (p.5) · SI 그림 21: 창이 작을수록 무충방전 오차가 커진다 (2 µm 창 ε_D ≈ 2.0 · ε_V ≈ 1.6 % [판독]) → 4 µm 택함.

### 3-7. ★ tortuosity · 빠른 기하 경로 (그림 4 · SI 그림 11–13 · 표 1–2 · 영상 S5)
- 확산 tortuosity factor (식 1 · TauFactor · 기공상 62 × 62 × 40 µm³ · 반응 결합 무시): 두께 방향 **3.3 (OCP · 'McMullin number of 9.4')** → 최대 3.83 (5 mV) · 3.86 (0.122 V) → 끝 ≈ 3.5 · 면내 2.38 → 2.68 → 2.40 [인쇄 p.5–6 · 원자료 MOESM12] (본문 면내 최대 '2.6').
- 이름 · 정의: Deff = D·ε/τ (식 1) = **우리 tau2 (수송 tortuosity · √ 아님)** · McMullin = τ/ε (3.3125/0.353 = 9.38 [카드 산술]) = 문헌 N_M = 1/f 꼴.  ε 에 CBD–Si 가 들어 있다.
- 본문 비교: *"consistent with previously reported electrochemical impedance spectroscopy measurements for graphite-based battery electrodes51,52"* — 높은 해상도가 micro-CT 보다 EIS 값에 가깝게 한다는 주장 (p.5 · 수치 비교 없음).
- 기하 τ_geo (식 3 · 측지 거리 · city-block 전파 · 두 방향 평균): OCP 면내 1.21 · 두께 1.36 (SI 표 1) · 히스토그램 봉우리 1.22 / 1.38 (SI 주석 5) · 두께 방향 1.35 → 1.42 (리튬화 끝 · 중간에 두 봉우리) · 면내 35 mV 에서 1.2 → 1.25 (SI 주석 5).
- **빠른 기하 경로** = L_geodesic/L_Euclidean < 1.2 인 기공 복셀 (*"quasi-straight lines crossing the entire composite Gr–Si electrode thickness"*) · 흐름 극대와 겹침 · 흑연 쌓임 ('기둥') 과 위치가 엇갈린다 (SI 그림 12) · 개수 9 → 13 · 기공 대비 부피 5.86 → 1.52 (0.122 V) → 5.78 % [원자료] · 화성 끝 빠른 경로 위 흐름 ≤ 0.3 (상대) · *"opening new fast geometric paths leads to more regularly distributed high-ways"* (p.6 · 가정이라고 적음).
- 반응–확산 결합: C/6 에서는 Thiele 수가 작아 보정항 무시 (SI 주석 5 · Lenne 2024).

### 3-8. ★ 입자 규모 (그림 5 · SI 그림 14–17 · 영상 S6)
- 분할 사슬 (방법 p.15 · SI 그림 14): 최대 필터로 내부 기공 메움 → Chan–Vese 레벨셋 (scikit-image) 으로 바깥 모양 → 거리 지도 → 극대 씨앗 (최소 크기 · 씨앗 간격 문턱) → watershed · 이유 = *"limitations of conventional watershed algorithms to separate particles presenting large internal porosity that are, typically for graphite, folded and pressed against each other"*.
- 수: 깊이 5–40 µm 에서 164 입자 → 가장자리 닿은 것 빼고 66 → **56 개 (85 %) 추적** · 고체의 **45.5 %v** (p.6–7) — 원자료 그림 5b 는 165 행 [원자료 MOESM13].
- 분포 (SI 그림 15 · n = 56): 등가 지름 μ **11.3** · σ 2.39 µm · 내부 기공 μ 24.7 · σ 4.72 % · 전해질 접촉 면 몫 μ 79.1 · σ 6.79 % · 빠른 경로까지 거리 μ 2.34 · σ 1.28 µm [인쇄 그림 안] · 모양 = 길쭉 (Sneed–Folk · SI 주석 6) · 원자료 165 입자: ψ_M 중앙 0.634 · S/L 중앙 0.595 · 정규화 지름 중앙 0.538 × 최대 19.04 µm = 10.2 µm [원자료 · 카드 산술] · ⚠ '(L-l)/(L-S)' 열 1.03–8.76 (정의상 0–1) [원자료 관찰].
- 전극 ↔ 입자 평균: 국소 DVC ε_V 12.44 ↔ 이산 11.63 % (5 mV) · 끝 7.50 ↔ 7.45 % [원자료 MOESM13] — *"confirming consistency between bulk electrode-scale analysis and averaging a representative set of individual particles"* (p.7).
- 깊이 (그림 5d · 15 입자씩 · 띠가 겹친다 10–20 · 15–25 · 20–30 · 25–35 µm): 0.065 V 에서 6.17 ± 0.84 · 4.82 ± 0.85 · 4.26 ± 0.70 · 3.96 ± 0.78 % (분리막 쪽이 크다) · 5 mV 에서 12.58 ± 0.65 · 12.97 ± 1.82 · 11.55 ± 1.22 · 11.87 ± 1.16 % (띠 평균 차 1.4 %p · 띠 안 입자 SD 0.6–1.8 %p) · 끝 8.10 · 9.00 · 7.81 · 7.71 % [원자료] · 본문: *"the entire particle population shows a lower variability during lithiation than delithiation"* · 깊이 경향은 *"does not uniformly hold when examining individual particle responses"* (p.8).
- 네 입자 (그림 5e–f · 그림 · 본문 표지 기준): #28 (깊이 15 µm · 빠른 경로 근처 · 전해질 접촉 64 %) 5 mV 16.8 · 최대 17.6 (0.122 V) → 끝 8.6 % · #124 (15 µm · 89 %) 12.1 → 8.4 % · #157 (35 µm · 빠른 경로 근처) 13.5 → 8.1 % · #144 (35 µm) 10.5 → 6.1 % [원자료 MOESM13 · ⚠ 엑셀 열 이름은 28 ↔ 124 가 뒤바뀐 꼴] — *"particle #28 displays higher electrochemical activity than particle #124 despite a lower particle/electrolyte surface fraction (64% versus 89%)"* (p.9).
- 무리 (SI 주석 7 · 그림 17): CBD–Si 군집 둘레 무리 (#1 · 2 · 5 · 6) 는 서로 비슷하게 움직이고 ε_V 가 조금 크다 · 흑연만 무리 (#3 · 4) 는 평균에서 ≥ σ 벗어남 · 전극 (국소) 편차 변형률 > 입자 평균 (CBD–Si · 입자–바인더 계면 몫) · 입자 #4 · #138 = 큰 비가역 · 그 둘의 ε_V 는 탈리튬화 끝에 오히려 커짐 (최대 13 %) ↔ 나머지는 8 % 줄어듦 → *"partial lithium trapping"* 추론 · *"dilatant shearing behavior, typical of dense granular and/or cohesive materials"* (SI p.42).

### 3-9. ★ 영향 인자 · 상관 (그림 6 · SI 그림 18 · SI 표 3 · 원자료 MOESM14)
- 정의: 활성 X_ac = 리튬화 끝 입자 ε_V (*"used as proxy for electrochemical activity"*) · Pearson corr (식 4–5) · 영향 인자 IF (식 6 · 두 점 정규화 기울기 · '0–1') · 오차 = 다변량 델타법 (SI 식 2) · 효과 크기 r² 등급 (0.01–0.2 매우 작음 · 0.2–0.41 작음 · 0.41–0.5 중간 · 0.63–0.8 큼 · > 0.87 매우 큼 — 0.5–0.63 · 0.8–0.87 은 빈 칸) (SI 주석 8).
- 인자 열넷 · 넷 묶음 (p.10): 형태 (등가 지름 · 부피 · 표면적 · 구형도 · 내부 기공) · 확산 (국소 τ_geo · 국소 흐름 Φ/Φ_max · 전해질 접촉 면 몫) · 위치 (깊이 · CBD–Si 거리 · 지속하는 빠른 경로 거리 · 이웃 흑연 수) · 역학 (리튬화 끝 최대 ε_V · ε_D · 비가역 편차) — 구형도 · 지름은 corr ≤ 0.3 으로 뺌 (SI 주석 8).
- **활성 (그림 6g · 원자료)**: 빠른 경로 거리 (그림 표지 '근접') IF **1.000** (corr 0.793) · 전해질 접촉 면 몫 0.585 (0.966) · 깊이 −0.539 (−0.891) · 국소 흐름 −0.294 (−0.668) · 내부 기공 0.286 (0.896) · CBD–Si 근접 (그림 표지 · 원자료 열 이름은 'Distance') −0.160 (−0.628) · 국소 τ_geo −0.160 (−0.686) — 불확도 0.006–0.093 [원자료 MOESM14] · *"Within the top 33% most active graphite particles, 70% connect to constant fast geometric paths"* (p.10).
- **비가역 (그림 6i · 원자료)**: 비가역 편차 변형률 −0.855 (−0.923) · 빠른 경로 거리 −0.789 (−0.369) · 이웃 수 +0.714 (0.828) · 최대 ε_V −0.642 (−0.908) · CBD–Si 거리 +0.461 (0.610) · 전해질 접촉 +0.424 (0.933) · 깊이 −0.301 (−0.866) · 내부 기공 +0.261 (0.881) [원자료] · *"Regions with important irreversible deviatoric strain (≥20%) present high local volumetric irreversibility (+17%)"* · *"a high number of neighbouring graphite particles (>10) preserves the composite electrode microstructural integrity and reduces local irreversibility, probably due to constraining effects in locally compacted areas with numerous contact points"* (p.10).
- 설명 몫: *"up to 90% of the particle deviation from ensemble behaviour can be rationalized … compared with only 45% when restricted to conventional macroscale parameters"* · *"9 exhibit correlation factors exceeding 0.35"* (p.10) — 어느 회귀 · 변수 묶음인지 식 없이 한 문장 (방법 p.15 '잔차 제곱합 ÷ 편차 제곱합') → 재현 불가 [미확인].
- ⚠ 부호 규약: 원자료 · SI 표 3 의 '거리' 칸 corr +0.79 (활성) 인데 SI 그림 18a 산점은 거리와 함께 줄어든다 — 그림 6f 원자료 (정규화 삼각 좌표 · 세 값 합 = 1 · n = 46) 로 계산하면 빠른 경로 거리 ↔ 활성 r = −0.74 [카드 산술] → 표 값은 '근접' 쪽 부호 (그림 6g 의 표지대로) 로 읽는다 (삼각 좌표라 크기는 견주지 않는다).
- ⚠ SI 표 3 ↔ 원자료 · 그림 6g/6i · SI 그림 18 어긋남은 §11.

### 3-10. 보충 영상 S1–S6 (MOESM3–8 · ffprobe · 정지 화면)
| 영상 (파일) | ffprobe | 무엇 (본문 언급 + 정지 화면) | 대표 정지 화면 |
|---|---|---|---|
| S1 (MOESM3) | MJPEG 2052 × 2048 · 1 fps · 13 장 · 13 s | 두께 방향 재구성 단면 (분리막 위 · 전극) 의 13 상태 · E/C 표지 — 본문 *"Fig. 2b,c and Supplementary Video 1"* (상분율 변화) | `vid_S1_t07s` (5 mV) · `vid_S1_t12s` (1.0 V) · ½ 축소 |
| S2 (MOESM4) | 660 × 632 · 1 fps · 12 장 | 3D 변위 벡터장 (OCP 기준 · 12 상태) — *"Fig. 3a and Supplementary Video 2"* · ⚠ 영상 색막대 0–25 ↔ 그림 3a 0–2.5 µm [판독] | `vid_S2_t06s` (5 mV) · `vid_S2_t11s` (1 V) |
| S3 (MOESM5) | 820 × 600 · 1 fps · 12 장 | 부피 변형률 장 ε_V (−30 … 30 %) — *"Supplementary Video 3 and 4"* (그림 3d) | `vid_S3_t06s` · `vid_S3_t11s` |
| S4 (MOESM6) | 820 × 600 · 1 fps · 12 장 | 편차 변형률 장 ε_D (0 … 20 %) (그림 3e) | `vid_S4_t06s` · `vid_S4_t11s` |
| S5 (MOESM7) | 1252 × 824 · 1 fps · 13 장 | 빠른 기하 경로 (L_geo/L_E < 1.2) 13 상태 — *"Fig. 4c,f and Supplementary Video 5"* | `vid_S5_t00s` (OCP · 9 개) · `vid_S5_t12s` (1 V · 13 개) |
| S6 (MOESM8) | 1306 × 958 · 1 fps · 12 장 | 추적 흑연 입자별 부피 변형률 (0 … 16 %) — **본문 · SI 어디에도 언급 없음** (MOESM 순서 · 내용으로 '영상 6' 으로 둔다 [카드 추론]) | `vid_S6_t06s` · `vid_S6_t11s` |
- 영상 한 장 = 촬영 한 상태 (12 장 영상 = DVC 라 OCP 기준 상태 빠짐 · 13 장 = OCP 포함) [ffprobe · 정지 화면 E/C 표지 대조].  SI PDF 에는 영상 설명이 없다.

### 3-11. 원자료 엑셀 지도 (MOESM9–14 · openpyxl)
| 파일 | 시트 → 그림 | 내용 |
|---|---|---|
| MOESM9 | 'Panel 1d' → 그림 1d | 5,519 행 · 시간 (h) · 전위 (V) · 전극 용량 (mAh g⁻¹) |
| MOESM10 | 'Panel 2b and 2c' · '2e' · '2f' | 13 상태 흑연 · 기공 · 입자 안 · 사이 상대 변화 / 회색값 히스토그램 13 × (1,000 행) / CBD–Si 봉우리 면적 평균 ± SD |
| MOESM11 | 'Panel 3b' · '3c' | ε_zz · ε_xx · ε_yy · ε_V · ε_D (+ 상수 오차) |
| MOESM12 | 'Panel 4e' · '4f' | 면내 · 두께 tortuosity factor · 빠른 경로 수 · 기공 대비 부피 % |
| MOESM13 | 'Panel 5b' · '5c' · '5d' · '5f' | 입자 165 개 모양 · 정규화 지름 (최대 19.04 µm) / 전극 ↔ 입자 평균 ε_V / 깊이 띠 4 개 평균 ± SD / 입자 28 · 124 · 144 · 157 |
| MOESM14 | 'Panel 6f' · '6g' · '6h' · '6i' | 46 입자 삼각 좌표 + 정규화 최대 ε_V / 활성 IF · corr · 불확도 7 행 / 56 입자 삼각 좌표 + 정규화 비가역 / 비가역 IF · corr · 불확도 8 행 |
- ⚠ **원자료 값도 그림 좌표 격자에 놓인다**: 그림 3b · 3c 값은 1/132 % 의 정수배 (편차 ≤ 0.07 칸) · 그림 5c 국소 = 1/16 · 이산 = 1/80 · 그림 4e 면내 = 0.00625 의 정수배 [카드 산술] → 계산 원값이 아니라 그림 좌표에서 다시 읽은 값일 수 있다 [카드 추론] · 같은 값 겹침 (ε_zz 5.87121 = 0.031 V 와 1 V · ε_V 9.39394 = 0.021 V 와 0.237 V) — 소수 둘째 자리 아래는 믿지 않는다.

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 계산

### 4-1. 셀 · 장치 (그림 1a–b · p.13)
소형 PFA 원통 (X 선 · 가시광 투과) 안에 Gr–Si 전극 (지름 0.7 mm) · 젖은 유리섬유 분리막 · Li 금속을 쌓고 스테인리스 커넥터 나사로 조인다 — 압력은 *"constant pressure (23 kPa estimated with a dynamometric wrench)"* (측정 아님 · 시간 변화 [미확인]).  위 커넥터를 짧게 해 회전 중 흔들림을 줄였다.  ID16B 는 끝단 온도를 23 ± 0.05 °C 로 잡는다 (나노 초점 광학 안정).

### 4-2. 측정 사슬 (재구성)
압연 전극 (레이저 절단) → 셀 조립 (글러브박스) → 빔라인 → OCP 영상 → [정전류 110 mA g⁻¹ 한 시간 → 전류 끔 (OCP 이완) → 9 분 홀로토모그래피 (거리 4 개) → 전류 다시] × 12 (5 mV 정전위 유지 포함 · 탈리튬화는 정한 전위에서) → 재구성 (위상 · FBP · 고리 · 16 bit) → 분할 (Ilastik) · CBD–Si 회색값 봉우리 · 국소 DVC (total · 강체 뺌) · 입자 라벨 → 이산 DVC · 측지 지도 · TauFactor → 입자 주변 지표 14 개 ↔ 활성 · 비가역 상관 (IF · Pearson).  대조: 빔 밖 쌍둥이 셀 (처음 · 끝 영상) · 무충방전 두 스캔 (DVC 오차) · 동전지 100 사이클 (가속 열화) · operando WAXS (다른 셀).
- **'탈압'**: 기계적 하중 제거는 없다.  탈리튬화 = 화학 하중이 빠지는 쪽 — 끝 (1 V) 에서 ε_V 7.35 % (최대의 59 %) · ε_D 5.38 % (74 %) 가 남는다 [원자료 · 카드 산술].

### 4-3. 영상 처리 · 분할 · REV (p.14–15 · SI 주석 1 · 4 · 10)
§3-2 표.  핵심 규약: (i) CBD–Si 는 회색값이 흑연 · 전해질 봉우리와 겹쳐 분할 오차가 커서 '전해질' 로 셌다 → '기공' 35 %v 는 기공 + CBD–Si · (ii) 입자 안 기공 = 최대 필터로 흑연을 부풀려 메운 뒤의 차 · (iii) 집전체 근처 단면은 위상 인공물로 정량에서 뺐다 · (iv) REV 는 부분 부피 분율의 표준편차가 공칭값 대비 5 % (95 %) 안에 드는 최소 크기.

### 4-4. ★ DVC (p.15–16 · 식 7–8 · SI 주석 11)
| 항목 | 내용 | 표지 |
|---|---|---|
| 소프트웨어 · 운동학 | SPAM (Stamati 2020) · 창마다 선형 · 균일 변형 함수 Φ (4 × 4 · 12 미지수 = 이동 · 회전 · 수직 · 전단) · x′ = Φ·x · 기울기 기반 반복 · 수렴 = Φ 증분의 노름 | [인쇄] p.15 |
| 기준 | **total** (OCP 부피 102 × 102 × 42 µm³ ↔ 각 상태) · 증분 아님 · 쌍마다 전극 질량 중심 강체 정합을 먼저 하고 국소 장에서 뺌 | [인쇄] p.15 |
| 국소 (연속) | 기준 영상에 마디 · 정육면체 창 · 피라미드 20 → 8 → 4 µm · 50 % 겹침 · 4 µm 는 오차 연구로 택함 (*"with many nodes falling well inside the graphite grains and their respective interfaces"*) | [인쇄] p.15 · SI 그림 21–22 |
| 변형률 | 변위 = Φ 의 이동 성분 → 2 × 2 × 2 마디 Q8 형상 함수 → F → 극분해 F = RU → **ε_V = det F − 1 (식 7) · U^dev = det(F)^(−1/3) U · ε_D = ‖U^dev − I‖ (식 8)** ('finite large-strain framework') | [인쇄] p.15–16 |
| 이산 (입자) | 라벨 입자 바운딩 박스를 창으로 · 입자 질량 중심의 Φ · 그 F 의 극분해로 입자 ε_V · ε_D | [인쇄] p.16 |
| 잔차 | *"apart from reconstruction artefacts, no nonlinear changes (violating the conservation of optical flow) were identified in the DVC residual fields … no particle agglomeration/disappearance was observed for the 56 particles"* | [인쇄] p.16 |
| 불확도 | 같은 조건 · 쌍둥이 셀 · 충방전 없는 두 스캔 — 국소: 창 크기 사다리 (SI 그림 21 · 2–16 µm) · 이산: 20 입자 평균 ≈ 0.26 % (*"an order of magnitude smaller than the strains recorded"*) · 잔차 장 (SI 그림 24): 입자 경계 국소 고잔차 없음 | [인쇄] SI 주석 11 |
| 못 하는 것 | 변위 불확도 (µm) 숫자 · 창 안 불연속 (균열 · 미끄럼면) 의 직접 측정 (아핀 가정 → 잔차로만) | [미확인] · [카드 관찰] |

### 4-5. tortuosity (식 1–3 · p.14–15 · SI 주석 5)
- 식 (1) Deff = D·ε/τ (τ = tortuosity factor · Nguyen 2020 [63] 의 '표준 정의' 인용) · 식 (2) ∇²C = 0 · 옆면 ∇C·n = 0 · C_collector = 0 · C_separator = 1 (TauFactor · 같은 크기 치밀 대조 부피와 정상 흐름 비교) · 식 (3) τ_geo = L_geodesic/L_Euclidean (Chen-Wiegart 2014 기반 자체 ImageJ 스크립트 · Fiji 플러그인 J. Lachambre).
- SI 주석 5 의 단서: 실제 전극은 반응–확산 결합 · 죽은 기공 때문에 순수 확산 τ 가 맞지 않을 수 있다 (Nguyen 2020 · Lenne 2024) — C/6 에서는 결합 무시.

### 4-6. 통계 (식 4–6 · SI 주석 8 · SI 식 1–2)
Pearson (식 4–5) · 영향 인자 (식 6 = SI 식 1 · 맞춤선 양쪽의 두 점 · 고르는 규칙 숫자 없음) · 불확도 = 다변량 델타법 (SI 식 2 · 인쇄 꼴 (corr_n − σ)/(σ/√n)) · 효과 크기 r².  '설명 몫 90 % ↔ 45 %' = '잔차 제곱합 ÷ 편차 제곱합' 한 문장 (p.15) — 모형 꼴 [미확인].

### 4-7. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — DEM 을 쓰지 않는다.  가까운 문장 둘 (평균 기술자 모델 일반): *"Empirical tuning of averaged parameters (particle size distribution and porosity) often fails to capture the three-dimensional (3D) multiscale complexity that governs electrochemical performance2–4."* (p.1 · [4] = Ngandjong 2021 DEM 압연 디지털 트윈) · *"While current approaches rely on ensemble and space-averaged descriptors,[17, 18] few works incorporate actual microstructures as simulation inputs.[19–21] To our knowledge, no detailed modeling has been attempted using operando nano-CT data on battery materials."* (SI 주석 9 · SI p.46 · [18] = 같은 Ngandjong 2021).
- **(ii) 소성 · 큰 변형을 계산에 넣는 어려움 = 논의 없음** — 계산이 없고 측정이다.  입자 집단 역학을 말한 문장 셋: *"Transient and irreversible phenomena relate directly to particle rearrangements and sliding within the binder matrix, involving changes in ionic diffusion pathways, pore clogging and particle–binder debonding."* (p.9–10) · *"This dilatant shearing behavior, typical of dense granular and/or cohesive materials, develops heterogeneously in the electrode microstructure."* (SI p.42) · *"… probably due to constraining effects in locally compacted areas with numerous contact points."* (p.10).  측정 쪽 가정 = **창마다 아핀 (선형 · 균일) 변형** — 입자 안 비선형 · 불연속은 잔차로만 본다 (p.15–16).  흑연 = 구조 골격: *"dominated by graphite particle deformation rather than silicon, demonstrating graphite's role as the structural backbone, with localized particle movements driving microstructural rearrangements"* (p.10).
- **(iii) 차원**: 측정 · 분석 모두 **3D** (2D 단면은 표시용) · 2D → 3D 전이 진술 없음.
- **(iv) 탈압**: 기계 하중 제거 없음 (≈ 23 kPa 그대로) · 탈리튬화 수축 뒤 남는 변형 (ε_V 59 % · ε_D 74 % · ε_zz 63 %) 이 '되돌아오지 않는 몫' [원자료 · 카드 산술].

### 4-8. 기법 미니 용어집
- **나노 홀로토모그래피** = 시료–검출기 거리를 넷으로 바꿔 찍은 투영에서 위상을 복원하는 X 선 CT — 가벼운 원소 (탄소 · 규소 · 전해액) 대비를 높인다.  **원뿔빔 기하 확대** = 초점 (55 × 60 nm) 에서 퍼지는 빔에서 시료 위치로 배율을 정한다 (52 mm · 280 mm → 50 nm).
- **중단-operando (interrupted-operando)** = 충방전을 진행하다 촬영하는 동안만 전류를 끔 (OCP 이완) — 시료 움직임 · 빔 영향을 줄인다.
- **DVC (digital volume correlation)** = 두 3D 영상의 회색값 무늬를 맞춰 변위 · 변형률 장을 얻는 방법.  **국소 (local)** = 겹치는 정육면체 창마다 · **이산 (discrete)** = 입자 하나 = 창 하나.  **total** = 늘 첫 영상 (OCP) 과 비교.
- **Q8 형상 함수** = 정육면체 8 마디의 3 선형 보간 → 마디 변위에서 변형 구배 F.  **극분해** F = RU (회전 R · 오른쪽 늘임 U).  **ε_V = J − 1** · **ε_D = ‖J^(−1/3)U − I‖** (등체적 늘임의 노름 = 모양 변화).
- **REV (대표 요소 부피)** = 상분율이 공칭값에서 정한 오차 안에 드는 최소 부분 부피.
- **경계 해상도 (edge resolution)** = 경계 회색값 미분의 반치폭 — 복셀 크기 (50 nm) 와 다르다 (140 nm).
- **tortuosity factor τ** (식 1) = 우리 tau2 · **McMullin 수** = τ/ε · **기하 τ_geo** = 측지 / 직선 거리 · **빠른 기하 경로** = τ_geo < 1.2 인 기공 복셀 다발.
- **영향 인자 (IF)** = 활성과 인자를 각자 최댓값 · 최솟값으로 나눈 두 점 사이 기울기의 절댓값 (이 논문 정의).
- **Sneed–Folk 삼각도** = 타원체 맞춤 세 축 (S ≤ l ≤ L) 의 S/L · (L − l)/(L − S) 로 10 모양 등급 (C · P · B · E · V).

---

## 5. Figure set ★
| 그림 | 내용 | 우리 활용 |
|---|---|---|
| 1 (a–e) | 빔라인 · 셀 · 3D 렌더 (257 · 50 nm) · 다척도 단면 · CBD–Si 3D · 첫 사이클 전위 · 용량 (촬영 시점) · 두께 60 → 75 → 64 µm | 측정 설계 예 · 두께 변화 |
| 2 (a–f) | 분할 단면 5 상태 · 흑연 / 기공 상대 변화 (리튬화 · 탈리튬화) · CBD–Si 단면 · 회색값 히스토그램 · 봉우리 면적 변화 | 상분율 연산자 · CBD–Si 장부 (§3-4 · §3-5) |
| 3 (a–e) | 변위장 · ε_zz · ε_yy · ε_xx · ε_V · ε_D 곡선 · ε_V · ε_D 3D 장 | ★ 변형률 정의 · 비등방 · 비가역 (식 7–8) |
| 4 (a–f) | τ_geo 지도 · 흐름 지도 · 빠른 경로 · 경로 위 흐름 · tortuosity factor 곡선 · 빠른 경로 수 / 부피 | 수송 tortuosity (tau2) 실측 꼴 · 새 기술자 (빠른 경로) |
| 5 (a–f) | 입자 라벨 · Sneed–Folk · 전극 ↔ 입자 평균 · 깊이 띠 · 네 입자 | ★ 입자 번호 승계 · 입자 형태 변형 |
| 6 (a–i) | 입자 주변 지표 · 삼각 지도 · 영향 인자 (활성 · 비가역) | 국소 기술자 ↔ 결과 상관의 보고 꼴 |
| S1 · S2 · S3 · S4 | REV · 다척도 영상 + WAXS Si 지도 · SEM · ex situ ↔ in situ 대비 | 방법 (REV · 대비 확인) |
| S5 · S6 · S7 | operando WAXS · 빔 영향 · 쌍둥이 셀 · 동전지 100 회 | 측정 신뢰성 |
| S8 · S9 · S10 | 기공 두 종 · 기공 크기 · 회색값 정렬 · 집전체 계면 (박리 없음) | 기공 정의 · 박리 |
| S11 · S12 · S13 | τ_geo 히스토그램 · 빠른 경로 ↔ 흑연 기둥 · τ_geo 분포 변화 · 농도장 · 흐름장 | 수송 |
| S14 · S15 · S16 · S17 | 입자 분할 사슬 · 입자 분포 · 입자별 곡선 · 무리 6 개 | 입자 처리 |
| S18 | 영향 인자 산점 10 개 (IF · corr · r²) | 상관 근거 (표 S3 와 같은 수) |
| S19 · S20–S24 | 고리 보정 · DVC 오차 (쌍둥이 · 창 크기 · 격자 · 이산 · 잔차) | ★ DVC 정확도 |
| 표 S1 · S2 · S3 · S4 | 상분율 · 기공 크기 · τ (해상도 · 시료별 · 처음 · 끝) · 상관 표 · CNR | 숫자 원천 |
| 식 크롭 11 | `eq_01`–`eq_08` (본문 식 1–8) · `eq_si_n6_*` (Sneed–Folk) · `eq_si_n8_eq1_*` · `eq_si_n8_eq2_*` | 보고서 측정 · 후처리 절에 붙일 정의식 |
| 근거 문단 20 | `txt_p2_*` · `txt_p3_*` · `txt_p5_*` · `txt_p5_p6_*` · `txt_p6_p7_*` · `txt_p10_*` · `txt_p13_*` · `txt_p13_p14_*` · `txt_p14_*` · `txt_p15_*` · `txt_p16_*` · `txt_si_p42_*` · `txt_si_p48_*` | 원문 인용용 |
| 영상 정지 12 | `vid_S1_t07s` … `vid_S6_t11s` | §3-10 |

## 6. Post-processing ★
- **무엇을**: 위상 복원 · 고리 제거 · 분할 (Ilastik) · 상분율 · 기공 크기 (국소 두께) · CBD–Si 회색값 봉우리 분해 · 국소 / 이산 DVC (SPAM) · Q8 → F → ε_V · ε_D · 측지 거리 지도 (ImageJ · city-block) · TauFactor (정상 확산 · 흐름 지도) · 빠른 경로 (문턱 1.2) · 입자 라벨 (레벨셋 + watershed · Python) · Sneed–Folk · Pearson · 영향 인자 · 델타법 오차 · WAXS (방위각 적분 · 흑연 (002) 이동 → Li 농도 · Si (111) 감소).
- **안 한 것**: 변위 불확도 (µm) · 균열 검출 · 정량 · 입자 접촉 수 · 접촉 면적 (이웃 수만) · 전극 두께의 측정 규약 · 반복 셀 · 두 번째 사이클 · 기계 하중 측정 · 반응 결합 tortuosity · 회귀 모형 식 ('90 %').
- **이 카드의 후처리**: 원자료 6 엑셀 전부 읽음 (13 상태 한 표 · §3-5) · 전기화학 이정표 · 첫 쿨롱 효율 · 정전위 몫 [카드 산술] · 흑연 ↔ 기공 닫힘 비 0.627 · 입자 안 몫 · 끝/최대 비 · 원자료 격자 (1/132 % 등) 검사 · 그림 6f 원자료로 부호 점검 (r = −0.74) · 전류 · 용량 산술 (§11) · 영상 6 ffprobe + 정지 화면 12.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 · 극 | 흑연 + nano-Si + SBR:CMC + C45 · **음극** · 액체 전해질 | LPSCl SE + NCM811 · **양극** · 고체 | 다름 — 전이 0 |
| 하중 | 리튬화 팽창 (화학) · 적층압 ≈ 23 kPa | 300 MPa 압밀 (기계) · 판 고정 이완 | 다름 — 같은 '되돌아옴' 단어라도 원인이 다르다 |
| 입자 크기 · 해상도 | 흑연 등가 지름 11.3 µm · 복셀 50 nm · 경계 해상도 140 nm → 지름당 ≈ 226 복셀 · ≈ 81 해상 길이 [카드 산술] | SE ⌀ ≈ 1 µm · STEP3 복셀 0.15–0.4 µm (SE 지름당 2.5–7 셀) · MPM real_14 n_grid 384 (dx ≈ 141 nm · CLAUDE.md) | 우리 MPM 격자 간격 ≈ 그들의 '해상 한계' — 그들의 Si (200 nm) 가 그 크기에서 75 % 미해상 (§7-4) |
| 변형률 측정 · 정의 | DVC 4 µm 창 · total · 강체 뺌 · ε_V = J − 1 · ε_D = ‖J^(−1/3)U − I‖ | MPM: 판 반력 wallP · σzz · 소성 변형률 장 · 입자 단위 변형률 정의는 아직 없음 | ★ 그대로 옮길 정의 (§8 · §9) |
| 입자 추적 | 라벨 56 입자 · 입자별 아핀 F (이산 DVC) | DEM 입자 번호 → MPM 씨앗 (Ⓑ '입자 번호 승계' 설계) | 같은 질문 · 측정 쪽 선례 |
| 기공 정의 | '기공' = 기공 + CBD–Si (해상도 밑 상을 전해질로) · 고정 상자 상분율 | ε_sphere (구 부피 합) · ε_union · MPM 관례 · 랩 표준 = 진밀도 1.64 기준 | 정의 · 상 규약을 같이 적어야 비교 가능 |
| 수송 | TauFactor tortuosity factor (tau2) 3.31 → 3.83 → 3.51 · 액체 기공상 | 접촉망 tau2 (Hertz · Physics) · STEP3 복셀 FV (CONTACT_FREE · CL-81) | 같은 이름 규약 (tau2) · 다른 상 (액체 기공 ↔ SE 고체) |
| 배위 | 이웃 흑연 수 > 10 이면 비가역 ↓ (IF 0.71) | DEM 배위수 Z · AM–AM CN 이 기본 출력 | 측정 ↔ DEM 양의 꼴 대응 (흐름 밖) |
| 균열 · 박리 | 균열 정량 없음 · 박리 정성 '없음' · 바인더 탈착 추론 | DEM Auerbach 분류 · MPM 파괴 없음 · A10 사이클 원장 (CZM) | 실측 표적 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 계 | 상태 | 기준 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | 진밀도 **1.64** (고정) | **10–13 %** |
| 이 논문 | 액체 LIB 흑연–Si 음극 (압연 선하중 5 MPa) | ≈ 23 kPa 셀 · OCP · 전해액 젖음 | 영상 이진 분할 (50 nm · 기공 + 바인더/Si) | 35.3 %v (OCP) → 리튬화 끝 상대 −17.2 % → 끝 −1.6 % |
- **"랩 표준과 다른 문헌 값"** 의 자리다 — 재료 · 전해질 · 압력 · 기공 정의 (CBD–Si 포함) 가 모두 다르다.  비교 대상 아님 (같은 줄에 놓는 것만).

### 7-3. ★ 사이클 화학기계 선례 대조 (값은 정본 카드에서)
| 카드 | 방법 · 계 | 하중 · 팽창 | 이 논문과의 대조 |
|---|---|---|---|
| `dem_mechanical_stresses_ssb_electrode_cycling` (Alabdali · … · Franco, ESM 2024) | LIGGGHTS · Hertz · **강구** · LPSCl + NMC532 · 단축 375 MPa → 등방 1/3/5 MPa | AM 을 **5 사이클 ±6 % 부피** 로 팽창 · 수축 · **균일 속도 (확산 분포 무시 · 저자 명시)** (그 카드 L1–9) | 이 논문은 팽창이 **균일하지 않다** 는 실측 — 같은 상태에서 깊이 띠 평균 차 (0.065 V 6.17 ↔ 3.96 %) · 띠 안 입자 SD 0.6–1.8 %p (5 mV) · 입자 #28 ↔ #144 5 mV 16.8 ↔ 10.5 % [원자료] → DEM 반경 · 부피 진동을 균일 배율로 줄 때의 한정어 근거 (액체 · 흑연 · 값 전이 없음) |
| `gritton2017_mpm_chemomechanical_coupling_silicon_anode` | 명시적 CPDI-MPM · a-Si 나노기둥 · **접촉 알고리즘 없음 (한 속도장)** · 부피 팽창 280 % (규소 전용 · 출처 없는 물성) | 리튬화 → 탈리튬화 한 바퀴 | 이 논문은 입자 사이 미끄럼 · 재배열 · 바인더 탈착을 '비가역의 원인' 으로 든다 → 한 속도장 (붙음) MPM 으로는 못 내는 몫 (후보 A′-0 · A′ 의 동기 · 정성) |
| `intergranular_cracking_nmc811_jmca2023` (Parks 2023) | 실험실 nano-CT · 화소 ≈ 124 nm · NMC811 입계 균열 (< 124 nm 균열 미해상) | 4.5 V 충전 | 이 논문 경계 해상도 140 nm — 같은 급 · 흑연 '판 벗겨짐' 은 보이나 균열 정량 · 검출 문턱 없음 |
| `lu2020_insitu_nanoct_calendering_microstructural_evolution` | 실험실 nano-CT 복셀 64 nm · NMC111 액체 양극 · 기둥 압축 ≤ 24 % · TauFactor tortuosity factor | 기계 압축 (누른 채) | 같은 '영상 → tau2' 사슬의 기계 하중판 — 두 논문 다 tortuosity factor = tau2 |
| `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` (같은 그룹) | 순수 LPSCl 누른 채 μ-CT 76–510 MPa + ex situ 나노 홀로토모그래피 (382 MPa 펠릿 기공 9.5 vol%) | 기계 압밀 | 같은 그룹 · 같은 기법 계열의 SE 판 — 이 논문의 DVC · 입자 추적은 그 SE 압밀에 아직 안 쓰였다 [카드 관찰] |

### 7-4. ★ 측정 해상도 ↔ 우리 복셀 격자
| 양 | 이 논문 | 우리 | 읽는 법 |
|---|---|---|---|
| 격자 · 복셀 | 50 nm | STEP3 0.15–0.4 µm · MPM real_14 dx ≈ 141 nm (n_grid 384) | 우리 MPM dx 가 그들 경계 해상도 (140 nm) 와 같은 급 [CLAUDE.md · 인쇄] |
| 실제 해상도 | 140 nm (경계 반치폭) = 복셀의 2.8 배 [카드 산술] | 우리는 '해상도' 를 따로 재지 않는다 (d_h/dx ≳ 3.5 규칙만) | 복셀 ≠ 해상도 — 우리 보고에 '셀 몇 개가 한 특징인가' 를 같이 적는다 |
| 대표 입자 | 흑연 11.3 µm → 226 복셀 · 81 해상 길이 [카드 산술] | SE ⌀ 1 µm → STEP3 2.5–7 셀 · MPM ≈ 7 dx | 그들은 입자 '모양' 을 재고 우리는 입자 '자리' 정도만 푼다 |
| 해상도 밑 상 | Si 200 nm (해상의 1.4 배) → 75 % 미해상 · 4.1 %v ↔ 18 %v | 우리 SDCP (Ø0.30 µm) 표현 부피 / 참부피 = 4.311 (vox 0.4) … 0.238 (vox 0.15) (CLAUDE.md CL-25) | 같은 부류의 장부 문제 — 그들은 '덜 보임' (영상) · 우리는 '더 / 덜 그림' (스탬프) |
| 측정 창 | DVC 4 µm 창 = 입자 지름의 0.35 · 오차 ε_V 0.36 % (4 µm) | MPM 장은 격자 그대로 (창 평균 없음) | 측정 장과 견주려면 우리 장도 4 µm 창 평균 · 같은 F 정의로 줄여야 한다 (§9) |

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실제 3D 구조의 **변형 (역학) 측정** (전극 · 입자 변형률 장 · 비가역) + 그 구조 위 **수송 (액체 기공 확산)** + 국소 지표 ↔ 활성 상관.
- **없는 것**: 계산 모델 (DEM · MPM · FEM 0) · 압력 · 고체전해질 · 접촉 수 · 접촉 면적 · 균열 정량.  ⇒ MPM (역학) 쪽에는 '측정 장과 같은 정의의 변형률 후처리' 를, DEM (수송 · 망) 쪽에는 '배위 ↔ 비가역 · 빠른 경로 ↔ 활성' 의 측정 꼴을 준다 — 둘 다 **방법** 전이다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) **상 규약이 기공을 바꾼다** — 해상도 밑 상 (CBD–Si) 을 '전해질' 로 세어 '기공' 35 %v · 연산자 등록에 '어느 상을 기공에 넣었나' 칸 (2) **고정 상자 상분율의 닫힘** — 흑연 Δ = −0.627 × 기공 Δ (12 상태) → 두 곡선을 독립 증거로 세지 않는다 (3) **REV 절차** (무작위 부분 부피 10 개 · 공칭 대비 5 % · 95 %) 를 우리 RVE 크기 판정에 (4) 해상도에 따라 평균 기공 크기는 ×3.3 · 상분율은 ±0.8 %v — '크기' 지표는 격자와 같이 적는다 | 압밀 · 순수 SE 기공 값 없음 |
| **단계 1** (3D 메모리 · 장 수) | 102³ µm³ ÷ 50 nm = 2,040³ ≈ 8.5 × 10⁹ 복셀 · 32 bit 34 GB / 16 bit 17 GB 한 장 [카드 산술] × 13 상태 · DVC 마디 ≈ 51 × 51 × 21 ≈ 5.5 × 10⁴ (2 µm 간격 · 102 × 102 × 42 µm³) [카드 산술] — 장 저장 크기의 실측 감 | 역학 장 수 · 입자별 속도장 메모리 아님 |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 맞춤) | 없음 (SE 없음) | — |
| **단계 5** (3D 복합 압밀) | 없음 (압밀 없음) · 정성: 단단한 골격 (흑연) 이 변형을 지배한다는 측정 문장 (R1 과 같은 방향) | 하중 몫 숫자 없음 |
| **단계 6** (탈압 · 되돌아옴) | ★ 측정 **규약** — 기준 = 첫 상태 (total) · 강체 운동 뺌 · 끝/최대 비 (ε_V 0.59 · ε_D 0.743 · ε_zz 0.63) 를 '남는 몫' 으로 보고하는 꼴 · 우리 언로딩에서 MPM 장 ε_V · ε_D 를 같은 식으로 내면 측정 꼴과 맞춰 읽힌다 | 압력 제거 아님 (화학 수축) · 값 전이 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★ (1) tortuosity factor (tau2) 를 같은 부피 · 상태별로 재는 꼴 (3.31 → 3.83 → 3.51) · 해상도 · 시료별 (SI 표 1: 257 nm ↔ 50 nm · 건조 ↔ 젖음 · operando ↔ 빔 밖) 같이 보고 (2) **빠른 기하 경로** (τ_geo < 1.2 다발 · 개수 · 부피 몫) — 우리 SE 망 τ_geo 지도 (`tau_geo_SE_dij`) 위에 바로 셀 수 있는 새 기술자 (흐름 밖 후보) (3) '전해질 접촉 면 몫' = 우리 피복 (coverage) 의 액체판 (입자 표면 중 전해질이 닿은 몫 · 79.1 ± 6.79 %) | 액체 기공 확산 (고체 SE 망 아님) · 문턱 1.2 의 물리 근거 없음 |
| **후보 D0** (지금 DEM) | 배위 ↔ 비가역 (이웃 > 10 → 비가역 ↓ · IF 0.71) · 분리막 쪽 계면 전단 · *"dilatant shearing … dense granular"* = DEM 이 자연스럽게 내는 거동의 측정 문장 · 사이클 팽창 DEM (Alabdali 2024 · ±6 % 부피 · 균일) 에 '불균일 팽창' 한정어 | 압밀 · 강성 · 겹침 값 없음 |
| **후보 A′-0** (판 · 벽 · AM 접촉 규칙) | 집전체 (단단한 Cu) · 분리막 (무른 섬유) 계면 전단 열점 · 박리 없음 (정성) — 벽 접촉 규칙이 '붙음 + 전단' 을 내야 할 측정 근거 | 계면 마찰 · 접착 값 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 입자 미끄럼 · 재배열 · 입자–바인더 탈착이 비가역을 만든다는 측정 해석 → 한 속도장 (붙음) 으로는 못 낸다 (A′ 의 동기) · 이산 DVC = 입자별 아핀 F (A′ 결과 후처리 꼴) | 정량 접촉 · 분리 값 없음 |
| **후보 B · C · C′ · M0** | 없음 | — |
| **U0–U6** | **U6** (해상도 수렴) 의 측정판: DVC 창 크기 사다리 (2–16 µm) 에서 오차가 창이 작을수록 커지는 교환 (SI 그림 21) · 경계 반치폭으로 해상도 재기 (SI 주석 10) · REV · 무충방전 두 스캔 대조 (U0 '아무 일도 없을 때 0 인가' 의 측정판) | 시뮬레이션 단위 시험 아님 |
| **R1–R7** | **R1** 흑연 = 구조 골격 (*"dominated by graphite particle deformation rather than silicon"*) · **R2** 미끄럼 · 재배열 · 탈착 (정성) · 박리 없음 · **R3** 입자 경계 기억 = 라벨 입자 56 개 사이클 내내 추적 (붙음 · 사라짐 없음) · **R4** 남는 변형 (ε_V 59 % · ε_D 74 %) · **R6** 입자 모양 변화 = 입자 ε_D (그림 5 · S16) · **R7** 흑연 판 벗겨짐 · 입자 안 새 기공 (정성 · 정량 없음) | R5 없음 · 전부 액체 LIB 흑연 |
| **결과 전 대조 항목** | 없음 (계 · 하중이 달라 우리 계산 결과와 견줄 외부 값으로 쓰지 않는다) — 방법 대조만: 우리 MPM 사이클 · 언로딩 계산을 만들면 '전극 ε_V 끝/최대' · '깊이 띠 차' · '배위 ↔ 비가역 부호' 를 같은 정의로 보고 | 값 비교 금지 (재료 · 전해질 · 하중) |

- **재료 · 차원 · 조건 차이**: 흑연–Si 음극 ↔ LPSCl + NCM811 양극 · 액체 ↔ 고체 · 23 kPa ↔ 300 MPa · 화학 하중 ↔ 기계 하중 · 3D = 같음 · 입자 11 µm ↔ SE 1 µm · 한 사이클.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **MPM 장 후처리를 DVC 정의로 맞춘다** (단계 6 · 후보 A′) — 기준 = 첫 상태 (total) · 질량 중심 강체 운동 뺌 · 4 µm 급 창마다 F → 극분해 → ε_V = J − 1 · ε_D = ‖J^(−1/3)U − I‖ (식 7–8).  그래야 언로딩 · 사이클의 '남는 변형' 을 측정 논문들과 같은 이름 · 같은 정의로 적는다 (p.15–16).
2. **입자 번호 + 입자별 아핀 F** (Ⓑ DEM → MPM 연계 · R3 · R6) — 이산 DVC 는 입자를 라벨로 묶어 질량 중심의 F 하나를 잰다.  우리 MPM 에서 DEM 입자 번호를 승계한 물질점 무리마다 최소제곱 아핀 F 를 맞추면 '입자 형태 변형' 이 측정과 같은 꼴의 한 수 (입자 ε_V · ε_D) 가 된다 (p.16 · 그림 5).
3. **해상도 밑 상 장부를 숫자로 남긴다** (단계 0 · STEP3) — 그들은 '해상 Si 4.1 %v ↔ 이론 18 %v → 75 % 미해상' 을 본문에 적었다 (p.2).  우리 복셀 σ 보고에도 '표현 부피 / 참부피' (CL-25) 를 같은 꼴로 상마다 적는다.
4. **흐름 밖: 배위수 ↔ 비가역 상관을 DEM 기술자로** — 이웃 흑연 > 10 이면 비가역 ↓ (IF 0.71 · p.10) · DEM 은 입자별 배위수를 공짜로 낸다 → 사이클 접촉 원장 (A10) 의 결과를 입자 배위수로 쪼개 보는 보고 꼴.
5. **고정 상자 상분율 두 곡선을 두 증거로 세지 않는다** (단계 0) — 그림 2b–c 의 흑연 · 기공 곡선은 비 0.627 로 묶인 한 측정 [카드 산술].

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Interrupted-operando nano-holotomography (50 nm voxels, 9 min per scan) with digital volume correlation (4 µm windows) shows that a calendered graphite–silicon anode swells anisotropically during its first lithiation (mean ε_zz ≈ 9 % vs in-plane 1–2 %) and retains about 74 % of its deviatoric strain after delithiation (Vanpeene et al., Nature Nanotechnology 2026; values from the source data)."
- "Particle tracking of 56 graphite particles indicates that proximity to quasi-straight pore paths and the particle/electrolyte surface fraction correlate more strongly with local lithiation strain than electrode depth (impact factors 1.0, 0.59 and −0.54; Vanpeene et al. 2026)."
- 국문: *"흑연–Si 액체 음극의 첫 화성 사이클에서 전극 부피 변형률은 12.4 % 까지 올랐다가 7.3 % 가 남았다 (DVC · 원자료 · Vanpeene 2026) — 고체전해질 · 압력 없는 계."*
- 국문: *"그 논문의 '기공' 35 %v 에는 해상도 밑 탄소-바인더-Si 군집이 들어 있다 (SI 주석 4)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **본문 변형률 세 수** 'ε_zz 8.8 · ε_xx 1.24 · ε_yy 2.43 %' (p.5) ↔ 원자료 최댓값 9.32 · 0.98 · 2.08 · 13 상태 평균 6.01 · 0.47 · 1.13 · 끝 5.87 · 0.23 · 1.21 % — 이 셋 어느 것과도 맞지 않는다 [원자료 MOESM11 · 카드 산술].
2. **CBD–Si '120 %' · '+30 %'** (p.3) ↔ 원자료 116.0 ± 23.2 % · 끝 22.1 ± 17.3 % (0.237 V 에서 29.6) [원자료 MOESM10].
3. **기공 두 종의 '40 %' · '50 %' · '+18 %'** (p.2) ↔ 원자료 입자 안 몫 18.8–23.0 % (OCP 뒤 12 상태) · 입자 안 기여는 끝까지 음수 (−0.33 % · 1 V) [원자료 MOESM10 · 카드 산술].
4. **흑연 · 기공 곡선 = 한 측정** (비 0.627 고정) — 본문 *"the graphite fraction and porosity remain balanced"* 은 닫힘의 결과일 수 있다 [카드 산술 · 추론].
5. **전류**: 방법 '20 µA' (p.14) ↔ 그림 1 캡션 '5.15 µA' ↔ 지름 0.7 mm · (6.67 + 1) mg cm⁻² · 110 mA g⁻¹ 로 ≈ 3.25 µA [카드 산술].  용량 3.3 mAh cm⁻² · '670 mAh g⁻¹' · 적재량 셋이 닫히지 않는다 (430 mAh g⁻¹) [카드 산술].
6. **첫 쿨롱 효율** 68.8 % [원자료 MOESM9 · 카드 산술] — 본문에 숫자로 안 적혔다 · SI 그림 6b 의 탈리튬화 끝 ≈ 135–145 mAh g⁻¹ [판독] 과 원자료 237.4 가 어긋난다.
7. **두께**: 60 (p.2 · p.14) · 65 (p.13) · 62 (SI 그림 3) · 63 µm (SI 그림 10) · 그림 1e 두께 변화 (+25 %) ↔ DVC ε_zz 최대 9.3 % — 측정 방법 [미확인].
8. **시야**: 본문 102 × 102 µm² ↔ SI 표 1 · 2 캡션 '108 × 108 µm²' · 25 nm 시야 51 (방법) ↔ 52 (SI 그림 2 캡션) ↔ '51.2 µm' (그림 안) · 초점 '50 × 50 nm²' (그림 1a) ↔ 55 × 60 nm (방법).
9. **REV 범위**: 방법 '22 to 250 µm' ↔ SI 주석 1 '23 µm … 350 µm'.  **CBD–Si 부분 부피**: 방법 20 × 20 × 13 µm³ × 3 ↔ SI 주석 4 20 × 20 × 10 µm³ × 5.  **최대 필터**: 방법 3 회 ↔ SI 주석 4 4 회.
10. **SI 표 3** ↔ 원자료 MOESM14 · 그림 6g · 6i · SI 그림 18: (a) 활성 Φ_av ↔ τ_geo,av 줄이 뒤바뀜 (표 Φ_av 0.16 / −0.69 / 0.476 = 그림 18g τ_geo 의 수) (b) N_ngh 활성 줄 'IF 0 · corr 0.79 · r² 0.624' = d_fast 줄과 같은 수 (그림 18d 의 평평한 선과 맞지 않음) (c) 가역성 열 Z_depth corr −0.67 ↔ 원자료 −0.866 · f_elec IF 0.9 · corr −0.37 ↔ 원자료 0.424 · 0.933 (그림 6i 막대 ≈ 0.42) · N_ngh corr −0.83 ↔ +0.828 (부호 규약) — 활성 · 가역성 '거리' 칸 부호는 '근접' 규약으로 읽힌다 (§3-9).
11. **SI 주석 5 '+9.4 % · +8.0 %'** ('irreversible graphite particle volumetric strain') = SI 표 2 입자 크기 (등가 **지름**) 비 12.8/11.7 = 1.094 · 12.2/11.3 = 1.080 과 같은 수 [카드 산술] — 지름 비라면 부피로는 +31 % · +26 % [카드 산술] · 순서도 'exposed (operando) → non-exposed' 와 반대 · operando 입자 이산 DVC 끝값은 7.45 % [원자료] — 어느 양인지 [미확인].
12. **SI 주석 10 'CNR from 10.2 to 12.8'** ↔ SI 표 4 · 그림 S19 6.1 → 10.4 · 표 4 'Before' 관심 복셀 평균 409676 (CNR 식이 맞으려면 ≈ 40968 [카드 산술]).
13. **SI 식 2** 인쇄 꼴 (corr_n − σ)/(σ/√n) — 분자에서 상관계수에 표준편차를 뺀다 · **효과 크기 등급**에 빈 칸 (0.5–0.63 · 0.8–0.87) · **영향 인자 0–1** 은 식 (6) 에서 보장되지 않는다 · 두 점 고르는 규칙 숫자 없음.
14. **선량 문턱**: nano-CT 1.5 MGy (SI 주석 3) ↔ WAXS 2 · 3 MGy 를 *"below the reported threshold"* (p.14).
15. **원자료 품질**: 값이 그림 좌표 격자 (1/132 % 등) 위 · 같은 값 겹침 · 국소 DVC ε_V 가 두 엑셀에서 0.237 V 상태만 다름 (9.39 ↔ 8.13) · 그림 5b 원자료 165 행 ↔ 본문 164 · '(L-l)/(L-S)' 값 > 1 · 그림 5f 열 이름 28 ↔ 124 뒤바뀐 꼴 · 그림 6f 원자료 46 행 ↔ n = 56.
16. **그림 5e 색막대** 'z_depth (mm)' 5–40 (µm 의 오기) · **SI 그림 18 캡션** 'see Supplementary Note 9' (상관 = 주석 8) · **영상 S2 색막대** 0–25 ↔ 그림 3a 0–2.5 µm [판독].
17. **'90 % ↔ 45 %'** 설명 몫 — 모형 · 변수 묶음 식 없음 (재현 불가) · '활성' = 변형률 대리 (전류 · SOC 아님).
18. **한 셀 · 한 사이클 · 한 부피** — 쌍둥이 셀은 처음 · 끝 두 영상 · *"reliable and reproducible55"* (p.10) 은 다른 셀의 전위 곡선 · 상분율 일치로 받친다.
19. ⚠ 이 카드의 [판독] 값 (SI 그림 6b · 7 · 21 · 23 · 12) 은 추세 전용 · 숫자는 원자료 우선.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 25 | Vanpeene, V. et al. Comparative study of the quantitative analysis of battery materials with X-ray nano-tomography: from ex situ toward operando measurements. ACS Nano 19, 9994–10012 (2025). | 같은 셀 · 같은 측정 흐름의 방법 논문 (선량 · ex situ ↔ operando 정량 비교) | 없음 (papers/ grep 'acsnano.4c16419' · 'Comparative study of the quantitative' 0) |
| 30 | Pietsch, P. et al. Quantifying microstructural dynamics and electrochemical activity of graphite and silicon–graphite lithium ion battery anodes. Nat. Commun. 7, 12909 (2016). | 흑연 · Si–흑연 전극 DVC (mesoscale) 의 선행 — 창 크기 · 변형률 값 대조 | 없음 ('12909' 0) |
| 31 | Valisammagari, A. et al. Study of microstructural evolution and strain analysis in SiOx/C negative electrodes using in-situ X-ray tomography and digital volume correlation. Batteries Supercaps 8, 202400416(2025). | Si 음극 DVC · 집전체 박리 사례 (이 논문 p.5 가 박리 근거로 듦) | 없음 ('202400416' 0) |
| 43 | Lu, X. et al. Unravelling electro-chemo-mechanical processes in graphite/silicon composites for designing nanoporous and microstructured battery electrodes. Nat. Nanotechnol. 20, 1656–1666 (2025). | 같은 계 (흑연/Si) 의 화학기계 · ε_zz 비등방 '이전 보고' | 없음 (grep 0) |
| 48 | Eastwood, D. S. et al. Lithiation-induced dilation mapping in a lithium-ion battery electrode by 3D X-ray microscopy and digital volume correlation. Adv. Energy Mater. 4, 1300506 (2014). | DVC 로 리튬화 팽창 지도를 낸 첫 예 (깊이 의존) | 없음 ('1300506' 0) |
| 65 | Stamati, O. et al. ‘spam‘: software for practical analysis of materials. J. Open Source Softw. 5, 2286 (2020). | DVC 소프트웨어 (우리 MPM 장 · 실험 CT 대조에 쓸 도구) | 없음 |
| SI 28 | Nelson, D.L., Sandoval, S.E., Pyo, J., Bistri, D., Thomas, T.A., Cavallaro, K.A., Lewis, J.A., Iyer, A.S., Shevchenko, P., Di Leo, C.V., McDowell, M.T.: Fracture dynamics in silicon anode solid-state batteries. ACS Energy Lett. 9(12), 6085– 6095 (2024) | **고체** Si 음극의 파괴 역학 — 우리 고체 쪽 사이클 화학기계 | 없음 ('Fracture dynamics' 0) |
| 50 · 51 · 52 · 63 · 4 · 7 | TauFactor (Cooper 2016) · Landesfeind 2016 · 2018 · Nguyen 2020 · Ngandjong 2021 · Lu 2020 Nat. Commun. 11, 2079 | tortuosity 정의 · 대조 · DEM 디지털 트윈 · nano-CT 설계 | taufactor · landesfeind2016 · landesfeind2018 · nguyen2020 · ngandjong2021 카드 있음 · Lu 2020 Nat. Commun. 은 없음 (정본 `lu2020_…` = Joule 2020 다른 논문) |
| 2 | Chouchane, M., Rucci, A., Lombardo, T., Ngandjong, A. C. & Franco, A.A. Lithium ion battery electrodes predicted from manufacturing simulations: Assessing the impact of the carbon-binder spatial location on the electrochemical performance. J. Power Sources 444, 227285 https://doi.org/10.1016/j.jpowsour.2019.227285 (2019). | CBD 자리 → 전기화학 (제조 모의) | 없음 (정본 `chouchane2019_innov_…` = ACS Omega 다른 논문 · 227285 는 다른 카드의 참고문헌으로만) |

---

## [미확인] 목록
- 변위 불확도 (µm) · 균열 크기 · 개수 · 검출 문턱 · 전극 두께 측정 규약 (그림 1e 의 60 · 75 · 64 µm) · 적층압의 시간 변화.
- 실제 인가 전류 (20 · 5.15 · 3.25 µA 중) · 용량 정규화 질량 · 첫 쿨롱 효율 93 % 의 대상.
- '90 % ↔ 45 %' 설명 몫의 모형 · 영향 인자 두 점 선택 규칙 · SI 표 3 의 부호 규약.
- '+9.4 % · +8.0 %' 의 정체 (지름 비 ↔ 부피 변형률) · 그림 1e 'Imaged volume 5.3 × 10⁻³ mm³' 가 무엇의 부피인지 (102³ µm³ = 1.06 × 10⁻³ mm³ [카드 산술]).
- 원자료가 계산 원값인지 그림 좌표에서 다시 읽은 값인지 · 원자료 엑셀 열 이름 (입자 28 ↔ 124 · '(L-l)/(L-S)') · 그림 2b–c 원자료 (입자 안 몫 ≈ 20 %) 와 SI 그림 8a (≈ 46 % · 끝 +19 %) 중 어느 가름이 본문 '40 · 20 · 50 % · +18 %' 의 근거인지.
- 영상 S6 (MOESM8) 의 공식 설명.
- 두 번째 이후 사이클 · 반복 셀 · 다른 전류.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-23)
- 서지: 1저자 메모 (V. Vanpeene · O. Stamati · F. Cadiou · Q. Jacquet · J. Villanova · S. Lyonnard · 제목 · Nature Nanotechnology (2026) · DOI 10.1038/s41565-026-02327-6) = 원문 첫 쪽과 같음 · **권 · 쪽 없음** · 'Published online: xx xx xxxx' (미기입) · 접수 2025-08-08 · 승인 2026-10-12 · PDF 메타데이터 (제목 · 'Victor Vanpeene' · 'Nature Nanotechnology, doi:10.1038/s41565-026-02327-6' · 생성 2026-11-06) · SI 첫 쪽 *"In the format provided by the authors and unedited"*.
- 숫자: 본문 16 쪽 · SI 54 쪽 텍스트 층 전수 읽음 · 그림 · 표 · 식 · 근거 문단 크롭 77 장 전부 직접 열어 봄 · 원자료 엑셀 6 개 (MOESM9–14) 시트 전부 · 영상 6 개 ffprobe + 정지 화면 (첫 · 가운데 · 끝 → 대표 12 장).
- 크롭: 도구 자동 크롭 31 장 중 본문 그림 6 장은 패널 글자 · 반쪽 누락으로 벡터 쪽에서 다시 렌더 · SI 그림 22 장은 원 래스터에서 다시 자름 (S1 은 쪽 제목까지 들어 있었음) · 표 S1–S3 다시 렌더 · S17 · S18 · 표 S4 손 크롭 · 캡션은 두 단 · 두 쪽에 걸친 것을 텍스트 층에서 전부 복원.
- 정본 중복 확인: papers/ 목록 (616) · DOI · 'Four-dimensional X-ray nano-holotomography' · 'vanpeene' grep — 이 논문 카드 없음 · 'Vanpeene' 는 korjus2025 카드의 공저자 이름뿐.

## 🔗 관련 카드
- 같은 그룹 · 같은 기법 계열 (공저 Vanpeene · Lyonnard): `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` (순수 LPSCl 누른 채 μ-CT + ex situ 나노 홀로토모그래피 · 서로 인용 없음).
- 영상 기반 tortuosity: `taufactor_tortuosity_factor_tomography_tool` · `nguyen2020_electrode_tortuosity_factor` · `landesfeind2016_tortuosity_eis_electrodes_separators` · `landesfeind2018_tortuosity_impedance_vs_tomography` · `lu2020_insitu_nanoct_calendering_microstructural_evolution` · `kashkooli2016_nanoxct_lfp_multiscale_rev_tortuosity` (nano-CT REV).
- 사이클 화학기계 (계산 · 실측): `dem_mechanical_stresses_ssb_electrode_cycling` · `gritton2017_mpm_chemomechanical_coupling_silicon_anode` · `intergranular_cracking_nmc811_jmca2023` · `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` · `bucci2017_chemomech_failure_assb_cycling_czm`.
- DEM 디지털 트윈 (이 논문 ref 4 · SI [18]): `ngandjong2021_dem_calendering_digital_twin`.
- 누른 채 CT (SE): `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` (형식 본).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
