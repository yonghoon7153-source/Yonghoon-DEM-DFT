# batch_19 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` (458 줄) · `reisacher2023_percolation_sulfide_carbon_matrix` (431) · `sangros2020_dem_electrical_conductive_paths_assb` (272) · `song2025_porous_argyrodite_modulus_fracture_toughness` (228) · `taufactor_tortuosity_factor_tomography_tool` (309) · `thorat2009_quantifying_tortuosity_porous_liion` (449) · `tjaden2018_tortuosity_review_calculation_approaches` (484). 끝까지 못 읽은 카드 없음 (일곱 장 모두 셋 – 여섯 번에 나눠 마지막 줄까지 읽음).

배치의 성격: **수송 (tortuosity · 퍼콜) 묶음 다섯** (pouraghajan · thorat = 액체 LIB 측정법 · taufactor = 복셀 계산 도구 · tjaden = 정의 · 계산법 리뷰 · reisacher = LPSCl + C65 퍼콜 실험) + **DEM 한 장** (sangros = LFP + CB + 폴리머, 탄성 Hertz-Mindlin + vdW, 구조 생성용) + **역학 실험 한 장** (song = 다공 LPSCl 펠릿의 벌크 E · K_Ic). **MPM 카드는 없다.** 순수 LPSCl 의 압력별 기공 곡선은 없고 (song 의 한 점 13 ± 2 % @ 360 MPa 뿐), 되돌아옴 (springback) 을 직접 잰 카드도 없다. 단단한 입자 하중 몫 · 재밍, 큰 변형 접촉 법칙 대안 (MDR · EEPA · Storåkers) 을 준 카드도 없다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `판독` · `digitized` · `그림 인쇄값` · `파생` · `우리 유도` · `우리 산술` · `derived(ours)` · `figure-read ≈` · `[미확인]` · `2차 인용`) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "내 검산" = 이 정독에서 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님 · 카드 문제 절에만 씀). 따옴표 안 문장은 카드가 옮겨 둔 원문 (한국어 따옴표는 카드의 옮김). **"인용 금지" 표지가 붙은 값은 이 배치에 없다** (tjaden L410 은 CL-81 협착 배수를 "이 카드에는 옮겨 적지 않는다" 고 적었다 — 숫자 없음). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 다른 값은 "랩 표준과 다른 문헌 값" 으로만 적었다.

---

## a. 순수 SE (LPSCl · 황화물) 압력별 기공 곡선 · 진밀도

- [a] song2025_porous_argyrodite_modulus_fracture_toughness | 순수 LPSCl 펠릿 **한 점**: 다공도 13 ± 2 % (겉보기/이론 밀도) @ 360 MPa 단축 압착 + 60 °C 2 h, 입경 ≈1 µm — 압력별 곡선 없음 (한 조건뿐) | §3.1 L51 · §3.3 L67 · L12 · §10 L188 | stated | 뺀 뒤 (압착 해제 · 열처리 뒤) 시편 · 이론 밀도 값과 기공 계산식은 카드에 없음 · 랩 표준 범위와 겹침
- [a] song2025_porous_argyrodite_modulus_fracture_toughness | 논문 서론 서술 "LPSCl 은 ≈10 % 다공" (국소–벌크 차가 특히 큰 이유로) | §11 L200 | 표지 없음 (카드의 서론 요약) | 출처 · 압력 · 조건 카드에 없음 — 측정값 아님
- [a] song2025_porous_argyrodite_modulus_fracture_toughness | 다공도–영률 자료는 **다른 황화물** (Li₃PS₄, Baranowski 2016) 2차 인용뿐: 밀도 58 / 67 / 80 % → 초음파 E 3.49 / 5.01 / 9.80 · 나노압입 4.53 / 8.74 / 12.07 GPa | §3.4 L87–88 · L12 | 2차 인용 (원문 미확인) | Li₃PS₄ — LPSCl 아님 · 압력 축 아님
- [a] reisacher2023_percolation_sulfide_carbon_matrix | 기공 · 상대밀도 n/a (미측정). 분리막 375 MPa 압밀 · 매트릭스 셀 안 2.07 MPa. 밀도 LPSCl 1.83 · C65 1.60 g/cm³ (wt% → vol% 환산에 씀) | §3 L88 · L123 · L92 | stated | LPSCl 1.83 g/cm³ 은 랩 표준과 다른 문헌 값 · 카드 Table 1 vol% 는 1.83 과 맞지 않음 (카드 문제 1)
- 나머지 다섯 장 (pouraghajan · sangros · taufactor · thorat · tjaden): 해당 없음 (SE 압밀 없음 · 액체 LIB 전극 다공도는 압력별이 아님).

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] song2025_porous_argyrodite_modulus_fracture_toughness | 되돌아옴 직접 측정 없음. 압밀 · 열처리 뒤 펠릿의 소변형 굽힘 힘–처짐이 "거의 선형·가역 (약한 이력 = 소량 비탄성)", 파괴 직전 작은 평탄부 = 소성/손상 개시; 대표 외팔보 최대 ≈215 mN @ ≈0.042 mm → 강성 ≈5.1 N/mm | §4.1 L108–111 · §3.2 L58 · Fig 1e | stated (관찰) · figure-read ≈ | 탈압 과정이 아니라 탈압 **뒤** 시편의 굽힘 · 잰 방법 = 하중계 (21 N/mm 이중 외팔보 · 광섬유 변위센서) + 현미경 DIC 처짐 (L72 · L108)
- [b] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte | 집전체에서 막을 떼면 (화학 박리) 두께 +12 % (양극 3) · +5 % (음극); 명목 건조 두께로 계산한 τ 가 박리 전후 BE 끼리 ≈ −40 % · −21 % 다름 | §3-1 L60–61 · §3-2 L78 | stated (두께) · 판독/파생 (τ 차) | 압력 해제가 아니라 구속 (집전체) 제거 · 두께를 잰 방법 카드에 없음 · 액체 LIB
- 나머지: 해당 없음.

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 환산

- [c] song2025_porous_argyrodite_modulus_fracture_toughness | 경도 H **미측정** (n/a) | §3.1 L50 · L11 | stated | —
- [c] song2025_porous_argyrodite_modulus_fracture_toughness | 일축 항복 환산이 카드에 있다 — 단 빌린 값: 항복변형 2.0 % (**황화물 유리** ref 24 인용) × E 4.7 GPa → σ_Y ≈ 94 MPa; 이로부터 "균열선단 소성역" 8.2 µm = 2.5 (K_Ic/σ_Y)² (ASTM E399 꼴 · Irwin 꼴 (1/2π)(K/σ_Y)² 이면 0.52 µm) | §3.1 L49 · §10 L189 · §13 L224 | stated (식) + 이 digest 산술 | 다른 재료의 항복변형으로 만든 추정 — LPSCl 항복 측정 아님
- [c] song2025_porous_argyrodite_modulus_fracture_toughness | 벌크 E 4.7 ± 1.1 GPa (13 % 다공 · mm 시편) ↔ 나노압입 Ning 2023 E 28.0 ± 1.8 GPa · K 0.69 ± 0.12 (400 MPa + 300 °C 20 min 소결 · 10 µm) → ≈⅙ · ≈¼ | §3.1 L43 · §3.4 L81 · §1 L20 | stated · 2차 인용 (Ning) | 측정 척도 · 공정이 달라 같은 물리량 아님 (L10)
- [c] song2025_porous_argyrodite_modulus_fracture_toughness | 크리프 · 점소성: 같은 재료 나노압입 점소성 시간척도 10⁵ s (ref 23) vs 이 시험 상한 4 × 10³ s → 하중속도 1–40 µm/s 무관과 모순 아님 | §4.4 L123 · §3.1 L48 | stated | ref 23 은 인쇄 전 (2차 인용)
- [c] song2025_porous_argyrodite_modulus_fracture_toughness | 2차 인용 탄성값: Papakyriakou 2021 환산 탄성률 42.1 (−40 °C) · 29.4 (300 °C) GPa · Deng 2016 DFT 22.1 GPa · McGrogan 2017 Li₂S–P₂S₅ 유리 E 18.5 ± 0.9 · K 0.23 ± 0.04 | §3.4 L82–84 · L91 | 2차 인용 (원문 미확인 · 카드 경고) | 항복 값 아님
- [c] reisacher2023_percolation_sulfide_carbon_matrix | E_SE · σ_y · ν n/a (역학 미모델) | §3 L124 | — | —
- [c] sangros2020_dem_electrical_conductive_paths_assb | 항복 값 없음 — DEM 입력 탄성값만: E LFP 123.90 · CB 5.00 GPa · ν 0.28 / 0.23 · COR 0.40 / 0.40 | §3 L41–43 · Table 2 | stated (입력, ref 26–28) | LFP · CB (SE 아님) · 항복 캡 없음

## d. 단단한 + 무른 입자 혼합 압축의 하중 몫 · 재밍

이 배치에 없음. (sangros2020 은 단단한 LFP (E 123.9 GPa) 와 무른 CB (E 5 GPa) 를 함께 누르지만 하중 몫 · 재밍 값은 카드에 없다 — §3 L41.)

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안

- [e] sangros2020_dem_electrical_conductive_paths_assb | 이 논문 접촉 법칙 = Hertz-Mindlin + van der Waals (항복 캡 없음). 카드는 같은 그룹 2019 자매편이 Thornton–Ning 탄소성 (p_y 캡) 을 썼다고 대비만 한다 | §4.2 L66–67 · §7 L148 | stated (법칙 이름) · 카드 풀이 (대비) | 점접촉이 깨지는 겹침 · 밀도 범위, 대안의 맞춘 값 수는 카드에 없음
- 나머지: 해당 없음.

## f. MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차 추정

(MPM 카드 없음 — 아래는 복셀 · FE · DEM 쪽 해상도 · 수치 오차 규칙)
- [f] taufactor_tortuosity_factor_tomography_tool | voxel 표면적 과대: 1 구 = 1 voxel → ×~2, 여러 voxel 구 → 최소 ×1.5, sub-voxel 복잡 구조 → 임의 과소 (Marching Cubes 안 씀 · 일관성 우선) | §3 L39 · Fig 7 · §10 L133 | stated | 면적 · 피복 metric 을 voxel 로 뽑으면 같은 한계
- [f] taufactor_tortuosity_factor_tomography_tool | sub-voxel 목 (throat) 소실 → τ 가 bulk 쪽으로 편향 (카드 예: SE ⌀1 µm 을 1 µm 격자로) | §10 L134 · L187 | 카드 풀이 | 우리 쪽 예시는 카드 서술
- [f] taufactor_tortuosity_factor_tomography_tool | 실증 사례 (Duquesnoy 2020): 1 µm/voxel · d_h/dx ≈ 1.00–1.03 → τ 가 같은 그룹 EIS (τ_TLM 1.3808 @ ε 31.5 %) 의 2.4–2.7 배 · active surface 가 100·ε/(1−ε) 와 R² 0.9964 (포화) — "TauFactor 는 정확했고, 입력 voxel 이 미해상이었다" | 역링크 절 L218–225 | 카드 산출 | 우리 규칙 d_h/dx ≳ 3.5 대조는 카드 서술
- [f] taufactor_tortuosity_factor_tomography_tool | 수렴 판정 = 상대변화 < 0.5 % 를 5 회 연속 + 위 · 아래 면 τ 차 < 4 % · 보고값 = 두 면 평균 · 이완 w = 2 − π/(1.5a); RVE 충분성 = RVA 4 종 (≈5 % 증분 · metric–부피 그래프) | 코드 대조 L239 · L249 · L253–254 · §4C L73 | 코드 대조 (1.424.0) · stated | MATLAB 실행 안 함 (정적 읽기)
- [f] tjaden2018_tortuosity_review_calculation_approaches | flux 알고리즘끼리 (RW vs LBM · RW vs FVM) 축별 τ 차 ≤ 0.04; RW 는 walker 10⁵ · step 10⁷ 로 정확도 확보; mesh 방법은 매개변수 감도 분석 필요 ("care must be taken … and sensitivity analyses should be carried out") | §3-C L86–91 · §3-A L55 · §4.4.3 L205 | stated · 우리 산술 | 기공상 · SOFC/LIB
- [f] tjaden2018_tortuosity_review_calculation_approaches | 해상도: 같은 Li-ion 양극 micro (597 nm) vs nano (65 nm) CT — ε 36.3 / 38.0 % · 기하 τ 2.0 / 1.9 비슷, 비표면적 0.6 / 1.3 µm²/µm³ (×2 이상) | §3-A L59 · §4.5 L219 | stated | 기공상 · 기하 τ
- [f] tjaden2018_tortuosity_review_calculation_approaches | RVE: Joos — l_cat > 10 µm 에서 평탄, 시료 2 LSCF 는 거의 2 배 두께 필요; Wilson vs Iwai 부피 9 배 차에도 τ 차 없음 (균질 시료) | §3-A L56 · L60 · §4.5 L221 | stated · 우리 산술 (9.24) | SOFC
- [f] song2025_porous_argyrodite_modulus_fracture_toughness | FE 수치 설정: 외팔보 3D C3D20 · 두께방향 요소 < 60 µm; CT 평면응력 CPS8/CPS6 · 1/4-점 중간절점 · 선단 요소 0.04–0.2 mm 로그 분포 · > 15 000 요소 · J 적분 5 경로 평균; 장치 검증 = Al 합금 영률 기지값과 < 2 % | §4.1 L110 · §4.2 L115 · §3.3 L75 | stated | 연속체 FE (입자 없음)
- [f] sangros2020_dem_electrical_conductive_paths_assb | DEM 쪽: 입자 6000 고정을 위해 조성마다 상자 크기를 바꿈 (6.8 → 2.43 µm · 고-CB 1.69 µm) · 조성당 구조 1 개 위주 (반복 수 불명) · x·y 주기 | §3 L49 · §4.6 L102–104 | stated · 카드 판독 (반복 수 불명) | 시드 반복으로 수치 산포를 재지 않음

## g. 2D → 3D 이전의 경고 · 증거

- [g] tjaden2018_tortuosity_review_calculation_approaches | 2D → 3D 경고: "Taiwo [2]: stereology 값은 3D 측정과 상당히 어긋날 수 있다"; 반면 BruggemanEstimator (2D 영상 두 장 → 차원별 α) 는 수치 τ 와 잘 맞았다 [58] | §4.2 L156 | stated (리뷰 인용) | 기공상 상관식 · 사례별
- [g] tjaden2018_tortuosity_review_calculation_approaches | 2D 단면 사슬 방법 (pore centroid) 의 인공물: 특징이 제어부피보다 작으면 단면 무게중심이 중앙으로 몰려 τ → 1 ("resulting in a tortuosity of unity", Cooper [118]) · 축당 값 하나 | §4.4.1 L196 · Fig 7 | stated (원문 인용) | 기하 τ 방법
- [g] song2025_porous_argyrodite_modulus_fracture_toughness | 2D 평면 가정의 규약 차: CT 의 K 는 2D 평면응력 FE · G_c = K²/E (평면응력, 6.15) vs K²(1−ν²)/E (평면변형, 5.31) = × 0.863 | §4.2 L115 · §10 L191 · §3.1 L45–46 | stated · derived(ours) | 2D 입자 계산을 3D 로 옮기는 증거는 아님
- 나머지: 해당 없음.

## h. DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

- [h] sangros2020_dem_electrical_conductive_paths_assb | DEM → (FE · MPM 아님) 그래프 후처리: 목표 부피분율에 닿아 멈춘 **마지막 구조 하나**를 입자 파일 (ID · 반경 · 위치) + 접촉 파일 (쌍 · 접촉면적) 로 내보내 Python A* · 등가회로 (σ_e) · MATLAB skeleton (τ) 로 넘김 | §4.1 L61–63 · §4.6 L103 | stated | FE/MPM 선례 아님 · 압밀 중간 상태는 넘기지 않음
- 나머지: 해당 없음.

## i. 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (AM + 황화물 SE 복합 양극의 압력별 기공을 준 카드 없음).
- [i] sangros2020_dem_electrical_conductive_paths_assb (가장 가까운 것) | 폴리머 SSB 양극 (LFP + CB + PEO-LiTFSI): 캘린더 뒤 실측 porosity ≈ 0; DEM 의 'porosity' 로 쓴 전해질 함량 60.00 / 48.80 / 48.80 / 47.20 / 46.6 % (CB 0 / 0.5 / 2 / 3.7 / 5.2 wt%) | §3 L29–30 · Table 4 | stated | 압력별 아님 · 전해질 = 폴리머 (공극 취급)

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압과 닿는 것

- [j] song2025_porous_argyrodite_modulus_fracture_toughness | 한 다공도 · 한 공정 (13 ± 2 %, 360 MPa, 60 °C, 1 µm) — 다공도 의존 자료 없음; 경도 미측정; ν 0.37 은 조밀 결정 DFT 값을 13 % 다공체에 씀; 개시 인성뿐 (R-곡선 없음); 광유가 기공에 스민 영향 미논의 | §10 L188–196 | 카드 경고 | 압밀 상태 하나라 압력 축 대조 불가
- [j] reisacher2023_percolation_sulfide_carbon_matrix | 도전 매트릭스는 셀 안 2.07 MPa 미압밀 → 절대 σ 를 300 MPa 압밀 케이스와 비교 금지 (0 wt% 6.6e-5 S/cm ≪ 분리막 0.43 mS/cm) · 향후 = AM 포함 full-cell · 전자 차단 EIS | §14 L423 · §4.4 L159 · §5.7 L215 | 카드 경고 · stated | 압밀 상태가 측정값을 바꾼다는 실례
- [j] sangros2020_dem_electrical_conductive_paths_assb | 압밀 = 부피분율 목표 정지 (압력 sweep 아님) → P–기공 곡선 없음 · porosity 를 '전해질 함량' 으로 재정의; DEM 이 탄성 (소성 · 항복 캡 · 파쇄 없음) 이라 접촉면적 = 탄성 Hertz 면적 | §10 L263 · L267 | 카드 경고 | —
- [j] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte | 박리 팽창 (두께 +12 % · +5 %) 을 명목 건조 두께 · 다공도로 계산해 두 방법이 서로 다른 시료 상태를 잼 · 다공도 3/4 이 공급사 또는 '통상값' 36 % | §8-0 ③ L350 · §10-1 L395 · L63 | 카드 판독 · stated | 측정 시점의 두께 정의 문제
- [j] thorat2009_quantifying_tortuosity_porous_liion | 다공도 = 무게 · 두께 계산, 쓴 밀도 미기재 [미확인] · 다른 ε 점의 막 두께 미기재 · 외부 압축 68 kPa 만 (압밀 · 소성 해당 없음) | §10-1 L359 · §3-2 L80 · §4-7 L186 | [미확인] · stated | 기공 연산자 (단계 0) 와 닿음
- [j] taufactor_tortuosity_factor_tomography_tool | voxel 해상도 의존 — 거친 격자로 SE 목이 뭉개지면 τ 가 bulk 쪽으로 편향 | §10 L134 · L187 | 카드 경고 | 가압 · 탈압 자체가 아니라 그 뒤 수송 (단계 7)
- [j] tjaden2018_tortuosity_review_calculation_approaches | 가압 · 탈압과 닿는 한계 없음 (기공상 리뷰).

## k. DEM 의 한계 (인용 서지 포함)

- [k] sangros2020_dem_electrical_conductive_paths_assb (Sangrós Giménez et al. 2020, Chem. Eng. Technol. 43(5), 819–829, DOI 10.1002/ceat.201900501) | DEM 을 구조 생성용으로만 썼다고 적음: "LIGGGHTS는 원래 입자 운동·효과 분석용인데, 여기선 *구조 생성*용으로만 씀" (카드가 옮긴 본문 명시) · 접촉 법칙 원문: "Hertz-Mindlin contact model, with the additional implementation of van der Waals forces" | §4.1 L61 · §4.2 L66 | 카드 인용 (본문 명시 · 한국어 옮김) · 원문 인용 | 믿을 수 있는 겹침 · 밀도 상한 같은 수치 한계는 말하지 않음 → 그 부분은 "말 없음"
- [k] sangros2020_dem_electrical_conductive_paths_assb (같은 서지) | 입자 형상 불변 · δ-overlap 은 접촉면적 계산용 기하량 (소성 흐름 아님) · 파쇄 미모델 (bond 없이 vdW 만) · CB 응집 (fractal) 을 65 nm 구로 단순화 | §4.5 L96–99 · §10 L269 | 카드 풀이 | 논문 문장으로 확인된 것은 법칙 이름 · 65 nm 근사뿐
- [k] sangros2020_dem_electrical_conductive_paths_assb (같은 서지) | 경로 모델의 자인 한계: "모든 경로를 *마지막에 병렬로만* 묶어 — *경로 간 상호작용(interconnected paths)*을 무시" → 고-CB (3.7 · 5.2 wt%) 에서 σ_e 과소 (Fig 4) | §7 L158 · §10 L265 · §3 L32 | 카드가 옮긴 본문 자인 (한국어) · digitized | DEM 접촉 법칙이 아니라 후처리 (A*) 의 한계
- [k] sangros2020_dem_electrical_conductive_paths_assb (같은 서지) | 논문은 "the selected pathways corresponded to the electrically most favorable path, taking into consideration the contact resistance between the particles." 라고 쓰지만, 카드 판독으로 저항은 R = ρ·l_cyl/Ā (접촉면적으로 나눈 벌크) 뿐 — 구속 (Holm) 항 없음; 카드 풀이: 구속저항 누락 (σ_e 과대 쪽) 과 경로 누락 (과소 쪽) 이 부분 상쇄해 Fig 4 가 그럭저럭 맞음 | §4.3 L81 · L85 · §7 L164 | 원문 인용 · 카드 풀이 | 상쇄 판단은 카드 작성자의 것 (정량 없음)
- [k] song2025_porous_argyrodite_modulus_fracture_toughness (Song et al. 2025, ACS Appl. Energy Mater. 8(9), 5636–5644, DOI 10.1021/acsaem.4c03143) | 논문은 DEM 을 쓰지 않음 → DEM 한계에 대해 **말 없음**. 논문 서술: 다공 펠릿을 "reasonably approximated as a continuum with homogenized properties" 로 보아 E · K_Ic 는 입자 + 접촉 + 공극을 모두 품은 겉보기 값 | §4.3 L120 | 원문 인용 | —
- [k] song2025_porous_argyrodite_modulus_fracture_toughness (같은 서지) | 카드 서술 (우리 모델에 대해): 우리 DEM E_eff 1.35 · MPM E 1.53 은 "느슨한 분말을 300 MPa 까지 누르는 과정의 접선 강성 대리" 라 압밀 펠릿 소변형 탄성과 같은 물리량이 아님; 벌크값을 입자 입력으로 넣으면 접촉 유연성 이중 계상; 22.1 → 4.7 GPa 를 다공도 0.13 만으로 설명하려면 (1 − p)ⁿ 의 n ≈ 11 · exp(−bp) 의 b ≈ 12 (소결 세라믹 통상 2–4 의 3 배) ⇒ "입자 간 접촉·목(neck)의 유연성이 지배" | §7 L153–154 · §8 ④ L175 · §13 L226 | 카드 풀이 · derived(ours) | 논문 문장 아님 · 통상 범위 2–4 는 교과서 범위 (논문 값 아님, L226)
- [k] thorat2009_quantifying_tortuosity_porous_liion (Thorat et al. 2009, J. Power Sources 188, 592–600, DOI 10.1016/j.jpowsour.2008.12.032) | DEM 미사용 → **말 없음**. 구 가정에 대한 원문: "the Bruggeman relation is a limiting case for particulate systems" — 비단분산 · 비구형 입자 + 탄소의 실제 막은 더 큰 τ (γ 1.8) | §4-7 L185 · Eq 18 | 원문 인용 (p.598) | 구 기반 유효매질 상관식에 대한 말 (DEM 아님) · 액체 LIB
- [k] tjaden2018_tortuosity_review_calculation_approaches (Tjaden et al. 2018, Int. Mater. Rev. 63(2), 47–67, DOI 10.1080/09506608.2016.1249995) | DEM 언급 없음 → **말 없음**. 구 가정 관련 원문: "the Bruggeman relationship is valid only for spherical structures and is generally unfit to predict accurate values for complex porous networks" (p.62) · "spherical structures … adhere to the correlation. The correlation, however, is less suitable for connected solid phases and complex porous networks." (p.50) | §4.6 L230 · §4.2 L157 | 원문 인용 | 기공상 상관식에 대한 말
- [k] tjaden2018_tortuosity_review_calculation_approaches (같은 서지) | 점 연결의 과대 계상: "small connections consisting only of one voxel would contribute only a negligible amount to the overall flux of transported species, while they are fully included in the above calculation methods." (p.57) · "the geometrically shortest path through a structure is not always the path of least resistance for a flux, owing to the presence of constrictions and pore necks." (p.56) — 카드 풀이: 작은 a 접촉이 우리 Dijkstra 에는 온전한 간선 · Kirchhoff 에서는 큰 R_c 인 것과 같은 논리 | §4.4.2 L199 · §4.4.1 L195 · §7 L302 | 원문 인용 · 카드 풀이 | voxel 기하 τ 에 대한 말 (DEM 직접 아님)
- [k] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte (Pouraghajan et al. 2018, J. Electrochem. Soc. 165(11), A2644–A2653) · reisacher2023_percolation_sulfide_carbon_matrix (Reisacher et al. 2023, Batteries 9(12), 595) · taufactor_tortuosity_factor_tomography_tool (Cooper et al. 2016, SoftwareX 5, 203–210) | DEM 미사용 — **말 없음** | pouraghajan §4-7 L224 · reisacher §4 L136 · taufactor §4D L76 | — | —

## l. 소성변형이 왜 어려운가 · 택한 우회와 값 (인용 서지 포함)

- [l] sangros2020_dem_electrical_conductive_paths_assb (Sangrós Giménez et al. 2020, Chem. Eng. Technol. 43(5), 819–829) | 소성을 넣지 않음 (Hertz-Mindlin + vdW, 항복 캡 없음). "왜 탄성인가" 는 **카드 풀이**: "목적이 *구조 생성 + 접촉면적 추출*이라 … 압밀경로 정밀도가 σ_e 추출에 1차적이지 않음" — 논문이 소성의 어려움을 말한 문장은 카드에 없음 | §4.2 L69 | 카드 풀이 | 논문 근거 아님
- [l] sangros2020_dem_electrical_conductive_paths_assb (같은 서지) | 우회 · 값: 맞춘 값 = 고유저항 **2 개** (LFP 분말 σ 0.023 S/cm @ ε 0.60 → ρ 6177.91 Ω·mm · CB 4.390 S/cm @ ε 0.74 → 0.07 Ω·mm; 카드: "σ_e의 *유일한* fit 입력") · 무엇에 = 분말 측정 (전극 σ 와 별도) · 검증 = 실측 전극 σ_e (CB 0–5.2 wt%, Table 4) + percolation 이론 대조 · 입자 6000 · 판 0.75 mm/s · 계산 시간 카드에 없음 | §4.8 L114 · §3 L39–40 · L49–50 · Fig 4 | stated | 소성 없는 구조라 접촉면적 = 탄성 Hertz 면적
- [l] song2025_porous_argyrodite_modulus_fracture_toughness (Song et al. 2025, ACS Appl. Energy Mater. 8(9), 5636–5644) | 입자 소성의 어려움은 말하지 않음 (입자 없는 균질 연속체 FE). 관찰: 힘–처짐 거의 선형 · 가역 (약한 이력 = 소량 비탄성), 파괴 직전 작은 평탄부 = 소성/손상 개시; 나노압입 점소성 시간척도 10⁵ s vs 시험 4 × 10³ s | §4.1 L111 · §4.4 L123 | stated | 소성 · 손상 개시는 정성 관찰
- [l] song2025_porous_argyrodite_modulus_fracture_toughness (같은 서지) | 우회 · 값: 시편마다 실제 형상 (두께 변화 포함) 을 3D FE 로 만들어 선형 구간에 맞춰 **E 하나**를 역산 (등방 선형탄성 · ν 0.37 고정 · DFT 인용); K 는 2D 평면응력 FE + J 적분 5 경로 평균 + 킹크 기준 · 시편 수: E 미기재 · K 18 점 (6 속도 × 3) | §4.1 L109–110 · §4.2 L115–116 · §3.2 L57 · §10 L190 | stated · 판독 (18 점) | 소성 · 손상은 모델에 없음 (선형탄성)
- [l] reisacher2023_percolation_sulfide_carbon_matrix (Reisacher et al. 2023, Batteries 9(12), 595) | 소성 모델 없음 (실험). 375 MPa 압밀 분리막 표면 SEM (Fig 1c) 이 plastic compaction 거동을 보이고, 카드가 옮긴 본문 표현: "LPSCl 은 *soft nature* 로 알려짐" | §5.1 L170 · Fig 1c | 카드가 옮긴 본문 표현 · 정성 | 입자 계산의 어려움에 대한 말 아님 — 소성 압밀이 실제로 있다는 실험 근거 (조건 R6 쪽)
- [l] pouraghajan2018 (Pouraghajan et al. 2018, J. Electrochem. Soc. 165(11), A2644–A2653) · thorat2009 (Thorat et al. 2009, J. Power Sources 188, 592–600) · taufactor (Cooper et al. 2016, SoftwareX 5, 203–210) · tjaden2018 (Tjaden et al. 2018, Int. Mater. Rev. 63(2), 47–67) | **말 없음** (입자 · 압밀 계산 없음; thorat 은 외부 압축 68 kPa 만, L186 · tjaden 은 입자 모형을 다루지 않음, L239) | — | — | —

## m. 받아들일 통찰

- [m] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte | 무엇을: 실험 tau2 앵커는 전 스펙트럼 모델 맞춤값만 쓰고 추출법을 장부에 적는다 · 어디에: 결과 전 대조 항목 (흐름 밖: EIS 앵커) · 왜: 같은 스펙트럼에서 빠른 추출법만으로 τ 가 −10.3 % (선형 외삽) … +4.3 % (drop-down) 흔들림 | §3-3 L87–90 · §8-0 ⑦ L373 · Fig 4b | 그림 인쇄값 · 파생 | 액체 LIB 한 스펙트럼
- [m] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte | 무엇을: 복합 양극 EIS 앵커마다 TLM 에 전자 레일 β = k_eff/σ_eff 가 들어갔는지 기록하고 우리 침대마다 모델 β (σ_ion,eff/σ_e,eff) 를 계산해 둔다 · 어디에: 결과 전 대조 항목 · 흐름 밖: EIS 앵커 판독 · 왜: β 를 무시한 그래프법 3·(R_l − R_h) 는 R_ion × [(1+β) − 3β/(1+β)] (β 0.1 → 0.83 · 최소 ≈ 0.46 @ β ≈ 0.73) | §8-0 ⑤ L360 · ⑦ L371 | 우리 유도 (원문에 없음 · 검산 §10-3) | 카드 유도식 · σ_AM 50 이 모델 기준값이라 모델 β 가 작게 나올 수 있음 (L371)
- [m] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte | 무엇을: 비교는 같은 시료 상태끼리 — 측정 시점의 두께 (누른 채 / 뺀 뒤 · 판 간격 / 질량보존) 를 관측량마다 명시 · 어디에: 단계 0 · 단계 6 · 단계 7 · 왜: 박리 팽창막 (PI) 과 미박리 전극 (BE) 을 잰 두 방법이 +62 % 어긋났고 박리 자체가 τ 를 −40 % · −21 % 바꿈; 두께 오차는 BE 에 1 승 · PI 에 2 승으로 들어감 | §3-2 L78 · §8-0 ③ L350 · §8-1 ④ L381 | 판독 · 파생 · 우리 판독 | 액체 LIB
- [m] pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte | 무엇을: 문헌 · 망 대조는 f (= 1/N_M) 끼리 해 ε 정의 논쟁을 피한다 · 어디에: 단계 7 · 왜: 두 방법의 비 BE/PI 는 ε 와 무관 (같은 ε 를 곱함), ε 가정은 τ 절대값에만 들어감 | §3-2 L79 · §8-1 ② L379 | 파생 | —
- [m] reisacher2023_percolation_sulfide_carbon_matrix | 무엇을: 탄소 퍼콜 임계 비교는 매트릭스 기준 wt% = C/(C+SE) 로 환산해 한다 · 어디에: 흐름 밖: 첨가제 σ_e 게이트 · 조성 설계 · 왜: p_c 4 wt% 는 매트릭스 기준이고 70 wt% AM 양극 전체로는 1.2 wt% | §0.1 L29 · L121 · §11.1 L371 · §11.4 L387 | stated · 카드 매핑 | AM 없는 매트릭스 값
- [m] reisacher2023_percolation_sulfide_carbon_matrix | 무엇을: 이온 · 전자 지배를 가르는 관측량 = σ_eff 의 온도 부호 (≤ 1 wt% T↑ → σ↑ / ≥ 3 wt% T↑ → σ↓) + 임피던스 주파수 무관 · 용량 없음 (단일 R 맞춤) · 어디에: 흐름 밖: 실험 대조 (σ_e/σ_ion 분리) · 단계 7 · 왜: 3 wt% 부근에서 부호가 뒤집혀 지배상 전환을 직접 보임 | §5.3 L183–184 · §5.4 L188–191 · §4.2 L149 | stated · digitized | 매트릭스 · 미압밀
- [m] reisacher2023_percolation_sulfide_carbon_matrix | 무엇을: 실험 σ 앵커를 장부에 올릴 때 '압밀 압력 · 누른 채 여부' 칸을 둔다 · 어디에: 결과 전 대조 항목 · 왜: 같은 LPSCl 이 셀 안 2.07 MPa 에서 6.6e-5 S/cm, 375 MPa 분리막에서 0.43 mS/cm | §3 L107 · L114 · §4.4 L159 | digitized · stated | 셀 형상 · 온도 차도 섞임 (L129)
- [m] reisacher2023_percolation_sulfide_carbon_matrix | 무엇을: 탄소 시드 검증 = 매트릭스 4 wt% 부근에서 3D 연결 (spanning) 여부를 시드 형상 · 비표면적을 바꾸며 본다 · 어디에: 흐름 밖: 첨가제 시드 · 믹싱 · 왜: 논문 해석 — 임계는 밀도 (1.83 vs 1.60) 가 아니라 비표면적 (62 m²/g) 이 정한다 · SEM 1 wt% 고립 → 5 wt% SE 표면 피복 | §5.6 L204–209 · §11.2 L376 | stated (해석) | C65 ≠ SuperP/VGCF (L427)
- [m] sangros2020_dem_electrical_conductive_paths_assb | 무엇을: 실험 일치를 검증으로 쓰기 전에 모델이 뺀 항마다 오차 부호를 따로 적는다 · 어디에: 결과 전 대조 항목 · 왜: 구속저항 누락 (σ_e 과대 쪽) 과 경로 교차연결 누락 (과소 쪽) 이 부분 상쇄해 Fig 4 가 그럭저럭 맞았을 수 있다 | §7 L164 · L158 | 카드 풀이 | 상쇄 크기는 정량되지 않음
- [m] sangros2020_dem_electrical_conductive_paths_assb | 무엇을: 같은 침대에서 FULL (R_bulk + R_c) 과 bulk_only (R_c = 0) 를 함께 내 협착 기여를 문헌 두 점 (협착 없음 Sangrós · Holm 있음 Bazzoun) 사이에 놓는다 · 어디에: 단계 7 · 흐름 밖: 계면 저항 · 왜: Sangrós 의 R = ρ·l/Ā 은 우리 bulk_only 토글과 같은 식 | §B ③ L210 · §7 L163–165 | 카드 풀이 | 우리 코드 줄 번호는 카드 시점 값
- [m] sangros2020_dem_electrical_conductive_paths_assb | 무엇을: 재료 상수는 대상 측정과 독립인 실험으로 정하고 대상은 예측한다 · 어디에: 조건 R5 · 결과 전 대조 항목 · 왜: LFP · CB 고유저항 2 개를 분말 σ (기지 ε) 에서 단일입자 ρ 로 역산하고 전극 σ_e (CB 0–5.2 wt%) 는 예측해 실측과 대조 | §4.8 L114 · §3 L39–40 · Table 3 · Table 4 | stated | 맞춘 값 2 개 (R5 는 하나)
- [m] sangros2020_dem_electrical_conductive_paths_assb | 무엇을: 기공 연산자를 결과 전에 정의한다 — '측정 기공' 과 '모델의 빈 공간' 이 같은 양인지 · 어디에: 단계 0 · 왜: 실측 porosity ≈ 0 (캘린더) 인데 DEM 'porosity' 는 전해질 함량 46.6–60 % 로 재정의됨 | §3 L29–30 · §10 L267 | stated | 폴리머 전해질
- [m] song2025_porous_argyrodite_modulus_fracture_toughness | 무엇을: 탈압 뒤 순수 SE 침대에 작은 굽힘 · 제하 변형을 걸어 겉보기 영률을 재고 4.7 ± 1.1 GPa (13 ± 2 %, 360 MPa) 와 견준다 — 맞추지 않음 · 어디에: 단계 6 · 결과 전 대조 항목 · 왜: 다공도 외의 두 번째 독립 대조 · 어긋나면 연화 프록시의 제하 거동 한계를 정량 | §8 ② L166–169 · §7 L158 | 카드 제안 | 입경 · 열처리 · 순수 SE 만 해당 (L169)
- [m] song2025_porous_argyrodite_modulus_fracture_toughness | 무엇을: 입자 입력 = 결정 · 나노압입 층 값, 침대 성질 = 모델 출력으로 나누고 벌크 측정값을 입자 입력으로 넣지 않는다 · 어디에: 단계 4 · 단계 5 · 조건 R5 · 왜: 나노압입 (28 · 0.69) ↔ 벌크 (4.7 · 0.17) 가 6 배 · 4 배 — 벌크값을 넣으면 접촉 유연성 이중 계상 | §8 ④ L175 · §3.4 L81 | 카드 풀이 · stated | —
- [m] song2025_porous_argyrodite_modulus_fracture_toughness | 무엇을: 탈압 되돌아옴은 접촉 (입자 경계 · 목) 표현에 민감할 것이라는 예측을 결과 전에 적는다 · 어디에: 단계 6 · 조건 R3 · R4 · 왜: 22.1 → 4.7 GPa 를 다공도 0.13 만으로 설명하려면 n ≈ 11 (통상 2–4) → 압밀체 강성은 접촉 · 목 유연성이 지배 | §7 L154 · §13 L226 | derived(ours) · 카드 풀이 | 통상 범위는 교과서 범위 (논문 값 아님)
- [m] song2025_porous_argyrodite_modulus_fracture_toughness | 무엇을: 파괴에너지 인용 시 규약 (평면응력 K²/E vs 평면변형 K²(1−ν²)/E, × 0.863) 과 E 가정을 함께 적는다 · 어디에: 흐름 밖: SE 파괴에너지 · 점착 트랙 · 왜: 같은 K 로 6.15 vs 5.31 J/m² · G_c 앵커 셋 (Bucci · Fan · Song) 의 E 가정이 18.5 · 24 · 4.7 GPa 로 다름 | §3.1 L45–46 · §8 ③ L172 · §10 L191 | stated · derived(ours) | —
- [m] taufactor_tortuosity_factor_tomography_tool | 무엇을: 복셀 · 망 교차검증에서 측면 경계를 맞춘다 — DEM 접촉망 ↔ mode 2 (측면 주기), STEP3 ↔ mode 1 (측면 거울), 비교는 협착 없는 가지 · 어디에: 단계 7 · 왜: 코드 대조로 두 면 잇는 성분만 풀이 · 전체 단면 정규화 · ε 비관통 포함이 같음 | 코드 대조 절 L286–292 | 코드 대조 | ε 장부 차는 남음
- [m] taufactor_tortuosity_factor_tomography_tool | 무엇을: ε 장부를 결과 전에 적는다 — TauFactor ε = 고립 · dead-end 포함 전체 voxel 분율 (flux 는 두 면 잇는 성분만) · D_eff = 상자 전체 단면; 우리 = 구 부피 합 (겹침 이중계상) · 어디에: 단계 0 · 단계 7 · 왜: 같은 τ 식이라도 ε 장부가 다르면 값이 달라짐 | L237–238 · L288 | 코드 대조 | —
- [m] taufactor_tortuosity_factor_tomography_tool | 무엇을: 수렴 · 보고 규칙 차용 — 상대변화 < 0.5 % 5 회 연속 + 위 · 아래 면 추정 차 < 4 %, 보고 = 두 면 평균 · 어디에: 단계 7 (복셀 · 망 풀이 수렴 기준) · 왜: 느린 수렴과 대칭계를 둘 다 잡는 hybrid 기준 | §4B L63 · 코드 L239 · L253–254 | stated · 코드 대조 | —
- [m] taufactor_tortuosity_factor_tomography_tool | 무엇을: 복셀 결과를 쓰기 전 d_h/dx 를 본다 (미해상 함정) · 어디에: 단계 7 · 흐름 밖: STEP3 해상도 점검 · 왜: Duquesnoy 1 µm/voxel · d_h/dx ≈ 1.00–1.03 → τ 가 EIS 의 2.4–2.7 배 · 면적 포화 — "TauFactor 는 정확했고, 입력 voxel 이 미해상이었다" | 역링크 절 L218–225 | 카드 산출 | 다른 논문 사례
- [m] thorat2009_quantifying_tortuosity_porous_liion | 무엇을: 두께 시리즈로 끝 (경계) 효과를 가른다 — τ_app·N = τ·N + τ*, 기울기 = 끝 효과 없는 값 · 절편 = 끝 효과 · 어디에: 단계 7 (망 tau2 의 띠 끝 단락 진단) · 왜: 분리막 1 장 τ_app 6.12 가 true τ 3.15 의 1.94 배 — 얇은 층에서 계면이 겉보기 값을 두 배로 | §4-6 L176–181 · Fig 7 · §8-0 ⑦ L333–334 | stated · 파생 · 카드 제안 (미구현) | 우리 띠 끝은 부호 반대 (T↓) 예상 (L278)
- [m] thorat2009_quantifying_tortuosity_porous_liion | 무엇을: 실험 이온 앵커는 전자 차단 배치에서 잰 것만 쓴다 · 어디에: 결과 전 대조 항목 · 왜: 혼합 전도 막의 고주파 R∞ 는 (κ+σ)_avg (국소 음의 상관이면 κ_avg + σ_avg 보다 큼) 라 우리 이온 · 전자 σ 를 따로 풀어 더한 값과 다른 양 — "we make no attempt in this work to extract κ_avg and hence τ from R∞ values" | §4-4 L161–164 · Eq 13–15 · §8-0 ⑦ L336 | stated · 카드 풀이 | —
- [m] thorat2009_quantifying_tortuosity_porous_liion | 무엇을: 실험 tau2 는 가정한 고유값에 비례한다는 점을 장부에 적는다 (PI → τ ∝ D_가정, AC → ∝ κ_ref) · 어디에: 결과 전 대조 항목 · 왜: 단층 이완 감쇠율 π²D/(τL²) 에서 ε 가 약분돼 PI 는 τ/D 를 잰다 | §4-3 L152–153 · §8-1 ② L340 | 우리 유도 (원문에 없음) | 카드 유도
- [m] thorat2009_quantifying_tortuosity_porous_liion | 무엇을: 지수를 비교할 때 관례 (f · tau2 · √) 와 앞계수 γ 처리를 같이 적는다 · 어디에: 단계 7 보고 · 왜: γ 를 1 로 묶으면 지수가 앞계수 결손을 흡수 (Froboese 같은 자료에서 α 3.67 ↔ 2.9) — "Without multiple experiments at different ε values, one cannot determine the proper relationship between τ and ε, if any." | §8-1 ③ L341 · §3-4 L106 | stated · 카드 풀이 | —
- [m] tjaden2018_tortuosity_review_calculation_approaches | 무엇을: 'τ_Lap,eff / τ_Dij = Constriction overhead' 처럼 flux ÷ 기하 비를 협착으로 읽지 않고, 협착 배수는 같은 망 FULL/CF 로만 정의 · 어디에: 단계 7 (관측량 정의) · 왜: 협착 없는 연속 기공상에서도 같은 단층영상의 flux τ 가 기하 τ 의 1.24–1.59 배 | §3-E L126 · 판정표 L369 · §8 ③ L410 | 우리 산술 (원문 표값) | 같은 시료 3 쌍뿐 (L426)
- [m] tjaden2018_tortuosity_review_calculation_approaches | 무엇을: 보고 형식 — 축별 τ 와 τ² 를 같이, 픽셀 · 부피 · ε 를 열로; 우리는 z 한 축이라 3 축 조화평균 τ_C 와 직접 비교 금지 · 어디에: 단계 7 보고 방식 · 왜: 리뷰 Table 4 본보기 · 식 21 | §5 L282 · D10 L337 · N1 · N6 L377 · L382 | stated | —
- [m] tjaden2018_tortuosity_review_calculation_approaches | 무엇을: 해상도 감도는 τ 보다 면적 · 피복이 먼저 흔들린다는 예측을 결과 전에 적는다 · 어디에: 단계 7 · 단계 2 (U1 해상도) · 왜: 같은 양극 micro/nano CT 에서 기하 τ · 공극률은 비슷, 비표면적은 2 배 이상 | §3-A L59 · §4.5 L219 · §8 ⑦ L414 | stated | 기공상 · 기하 τ
- [m] tjaden2018_tortuosity_review_calculation_approaches | 무엇을: CF 가지에 '곧은 단일 SE 사슬' 해석해 단위 시험을 둔다 (기대 tau2_CF → 2/3 < 1 · 겹침 d < 2r 이면 (4/3)·r/d) · 어디에: 흐름 밖: 접촉망 수송 단위 시험 · 왜: 리뷰 정의 (곧은 경로 = 1, 항상 ≥ 1) 와 우리 원기둥 R_bulk 정규화의 차를 기록 | D3′ L330 · §8 ④ L411 | 우리 산술 (실행 시험 안 함, L429) | 미검증 산술

---

## 카드 문제

1. **reisacher2023 — 밀도 ↔ vol% 불일치**: L88 은 LPSCl 1.83 · C65 1.60 g/cm³ 라 적는데 L120 · L251–259 (Table 1, stated) 의 vol% (1.16 / 3.47 / 4.62 / 5.77 / 11.44) 는 1.83 으로는 나오지 않고 1.86 으로 나온다 (내 검산: 1.83 이면 4 wt% → 4.55 vol% · 10 wt% → 11.28 vol%). 같은 카드 L48 의 Kim 2024 행이 1.86 을 적는다 (다른 논문). 어느 쪽이 원문 값인지 카드에 없다. (둘 다 랩 표준 1.64 와 다른 문헌 값.)
2. **reisacher2023 — 증가분 불일치**: L109 "CM-3 1.66×10⁻⁴ … CM-1 대비 +1.20×10⁻⁴" 는 카드의 CM-1 판독값 9.5×10⁻⁵ (L108 · L254 — R 522 Ω 과도 맞음) 과 맞지 않는다 (차 7.1×10⁻⁵ · 내 검산). 기준 불명.
3. **reisacher2023 — 철회된 라벨**: Cronau 3.0 을 "단결정" 으로 적음 (L128 "Cronau 단결정 3.0" · L130 "Cronau 3.0(단결정-라벨) 유지" · L322) — CLAUDE.md 원장 `CL-91` · `SELF-51` 에서 철회된 라벨 (3.0 = Cronau 2021 SI 의 µC 펠릿값).
4. **reisacher2023 — Minnmann 앵커 서술**: L61 이 Minnmann 2021 을 "우리 porosity/σ_ion/τ 앵커 1차 출처" 로 적음 — 순수 SE 기공 앵커로서의 Minnmann (10 % @ 300 MPa) 은 철회됨 (`CL-94`). 어떤 porosity 를 뜻하는지 카드에 없다.
5. **sangros2020 — Minnmann 을 실험 보정 앵커로**: L155 "solver=ground truth(Minnmann·Cronau·Bazzoun 외부 앵커)" · L240 "DEM(전달) + MPM(역학) 을 *각각 독립적으로* 실험에 보정(Minnmann·Cronau·Bazzoun)" — MPM 실험 앵커로서의 Minnmann 은 철회됨 (`CL-94`).
6. **sangros2020 — 철회된 교차검증 서술**: L228 "real_14 porosity 16.7↔15.6 % cross-val" — CLAUDE.md 2026-09-09 정정 (CDX-16) 에서 철회 (같은 기하 공유 + 관례 오프셋 1.251 %p). reisacher L323 의 "MPM 16.7 %(real_14)" 도 같은 옛 관례 값이다.
7. **sangros2020 — 철회된 출처 표기**: L234–236 "문헌-근거 σ_grain / σ_AM (Cronau + Trevisanello)" · "σ_ionic은 Cronau(r_SE) σ_grain" · "Trevisanello σ_S/σ_P" (L191 · L152 도) — Cronau(r_SE) 는 모델 가정 (`SELF-51`), Trevisanello 는 GB 방향만 뒷받침하고 σ_S/σ_P 크기는 코퍼스 맞춤값 (A1).
8. **sangros2020 — 증가율 기준 불명**: L38 "σ 증가율 2→3.7 wt%: +85.89 %" (stated) — 같은 카드 Table 4 실측 σ 비 (6.20e-3 → 1.59e-2) 는 +156 %, Fig 4 모델 판독 (≈0.006 → ≈0.013) 은 ≈ +117 % (내 검산). 무엇의 증가율인지 카드에 없다.
9. **sangros2020 — 단위 표기**: D_el 을 L52 "2×10⁻⁴ S/cm⁻¹" · L92 "2×10⁻⁴ S/cm" 로 두 번 다르게 적고, 확산계수에 전도도 단위를 붙였다.
10. **sangros2020 — 소속 서술 [미확인]**: L251 · L257 이 Bazzoun 2026 을 "같은 그룹 후속" · "the Braunschweig group's … later companion" 이라 적는데 카드 안에 근거가 없고, CLAUDE.md 의 Bazzoun 절은 소속을 Mercedes-Benz + Stuttgart 로 적는다.
11. **song2025 — 철회된 Minnmann 앵커**: L167 "우리 순수 SE 앵커는 Minnmann ≈10 % @300 MPa(다공도)뿐이다" — 철회된 출처 (`CL-94`: Minnmann 2021 에 순수 SE 기공값 · 300 MPa 없음 · 10 % 는 우리 MPM 보정 수렴값). L168 의 "(둘 다 실험 독립 보정 …)" 도 그 앵커에 기댄다.
12. **taufactor — τ/τ² 대응이 절마다 다름**: L10 · L110 · L156 · L176 은 "TauFactor τ ↔ 우리 τ_Laplace,bulk" (√ 쪽 이름) 로, L147 · L288 · L304 는 "TauFactor τ ≡ Minnmann τ² ≡ 우리 τ_Laplace²" (제곱) 로 적는다 — 10-03 규약 (tortuosity factor = tau2) 으로는 뒤쪽이 맞다.
13. **taufactor — 상한/하한 섞임**: L10 · L110 · L156 "기하/상한 tortuosity", L119 "bulk 하한(상한 τ)", L132 "그 상한 하한값" — τ 기준인지 σ 기준인지 섞였다 (협착 없는 τ 는 τ 의 하한 = σ 의 상한).
14. **taufactor — 우리 기록과 어긋남**: L177 "만약 우리 σ_ionic 이 TauFactor bulk-σ 보다 높으면 버그 신호" — CLAUDE.md 의 Codex 판정 `RINT-09` ("FULL ≤ vox ≤ CF 는 불변식 아님") 과 어긋난다.
15. **tjaden2018 — 카드 안 모순**: L41 이 Thorat 활물질 막 τ 의 방법을 "AC impedance + polarisation-interrupt" 로 적는데, 같은 카드 L178 과 thorat2009 카드 (L164 · L392 · 원문 p.596) 는 막 = PI 만 · AC 는 분리막 전용이라 적는다.
16. **tjaden2018 — 경미 둘**: L480 서지 "J Power Sour. 2009;188(2)" 의 호 (2) 는 Thorat PDF 로 확인 불가 (thorat L45 · L394 [미확인]); L41 "τ² … 우리 해석" 은 Thorat 원문이 직접 정의한다 (thorat L391).
17. **tjaden2018 — 날짜 참고**: L13 · L342 · L356 · L408 의 웹앱 · 내보내기 "COMSOL input = τ_Lap,eff (√)" 서술은 10-02 시점이다 — CLAUDE.md 는 10-04 라벨 묶음에서 고쳤다고 적는다 (`TAU-01` claimed_fixed). 현재형으로 읽지 말 것.
18. **thorat2009 — 두께 두 값**: ε 0.45 막이 L77 (Fig 8 대표 맞춤) 115 µm · L80 · L301 "Fig 9 의 ε 0.45 점 ≈ 100 µm" — 같은 막인지 카드에 없다.
19. **pouraghajan2018 — 경미 반올림**: L74 양극 3 "BE 박리막/PI − 1 ≈ −3.6 %" 는 같은 줄 판독값 (2.78 / 2.88) 으로는 −3.5 % (내 검산) — 반올림 전 픽셀값 차일 수 있음.
20. **pouraghajan2018 ↔ thorat2009 — 용어 충돌**: "apparent tortuosity" 를 pouraghajan L146 · L233 은 "PI 모델이 측정 기울기를 재현하는 τ" 로, thorat 은 "Li 계면 저항이 섞인 분리막 값" 으로 쓴다 (thorat L407 이 표지 필요로 기록) — 원문 용어인지 카드 오류인지 미확인.

(이 배치 밖 카드에 대한 기록) tjaden L448 은 `minnmann2021_jes_charge_transport_bottlenecks` 카드 안에 Eq 4 의 두 형태 (물리적으로 맞는 꼴 l.44 · 인쇄 그대로 l.158) 가 공존한다고 적는다.
