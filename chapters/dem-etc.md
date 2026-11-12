# 그 밖의 문헌

전극 미세구조 · 공정 · 장 `dem-etc` · 논문 12편 · 읽기 카드 11편

> 위 묶음에 들지 않은 DEM 축 문헌. 저장소 인덱스에서도 '기타'로 남아 있다.

## 장 서문 — 옮길 것은 방법의 뼈대이고 수치는 아니다

*읽기 카드 11편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10 · 낡음: 그 뒤 이 장의 카드가 바뀌었다 (센서가 자정 뒤 다시 쓴다)*

DEM 축의 기타 문헌은 두 부류로 나뉜다. 하나는 DEM 보정, 복셀 표면적 추정, 다축척 결합, 입도분포 역산 같은 방법 문헌이다. 다른 하나는 액체·수계 전지의 계면 문헌이다. [근거: Windreich et al. 2003 (`windreich2003_voxel_based_surface_area_estimation`); Coetzee 2017 (`coetzee2017_dem_calibration_review`); Balasubramanian et al. 2026 (`balasubramanian2026_rfb_electrolyte_kmc_lbm_preprint`); Eizenhammer et al. 2026 (`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`); Cho et al. 2026 (`cho2026_eipc_zn_anode_azib`); Park et al. 2026 (`park2026_ceramic_pp_separator`)]

방법 문헌에서는 보정과 계산의 뼈대를 가져올 수 있다. 검토 측은 그 안의 파라미터 값과 가드레일은 옮길 수 없다고 본다. [근거: Coetzee 2017 (`coetzee2017_dem_calibration_review`); Shenouda & Hoff 2020 (`shenouda2020_dem_metal_powder_am_liggghts_tutorial`); Eizenhammer et al. 2026 (`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`)]

황화물 전고체 쪽 외부 기준점은 Beutl et al. 2024 한 편이다. 검토 측은 그 측정값이 기관보다 전극 접촉 규약에 더 크게 묶인다고 본다. [근거: Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`)]

### DEM 파라미터 정하기

DEM 입력값은 직접 재기보다 벌크 실험에 맞춰 역보정하는 일이 가장 흔하다. Coetzee 2017은 25년치 문헌을 훑어 직접측정 접근과 벌크 보정 접근의 두 학파로 정리했다. 원문은 형상 단순화와 접촉모델 가정의 영향을 다른 파라미터가 보상한다는 점을 벌크 보정의 장점으로 들었다. 대가는 해가 유일하지 않다는 것이다. 원문은 실험마다 파라미터 하나를 고립시키거나 여러 실험을 합치라고 처방했고, 파라미터가 응력에 의존한다고도 적었다. [근거: Coetzee 2017 (`coetzee2017_dem_calibration_review`)]

이 장의 두 DEM 문헌은 모두 소성 압밀을 다루지 않는다. 검토 측은 Coetzee 2017이 저응력 벌크 취급 문헌이라 방법론은 전이되지만 파라미터 값은 전이되지 않는다고 본다. Shenouda & Hoff 2020은 LIGGGHTS-PUBLIC 입문 튜토리얼이고, 데모 접촉은 Hertz에 SJKR 점착을 더한 것뿐이라 소성 항복 분기가 없다. 점착에너지밀도를 높이자 안식각이 24.7°에서 73.08°로 커졌지만, 검토 측은 소재와 무관한 데모 값이라 옮길 수 없다고 본다. 우리 냉간압축 보정은 300 MPa에서의 porosity를 목표로 E_eff 하나를 맞추는 구속 단축압축 시험에 해당한다. 이 보정이 유일하다고 말하려면 마찰과 COR을 바꾸는 OAT 민감도표가 필요하다. [근거: Coetzee 2017 (`coetzee2017_dem_calibration_review`); Shenouda & Hoff 2020 (`shenouda2020_dem_metal_powder_am_liggghts_tutorial`)]

### 구조를 숫자로 읽기

복셀 표현에서 기하량을 읽을 때는 추정기 자체의 편향을 먼저 따져야 한다. Windreich et al. 2003은 MV 추정기에 극단 부류 가중치를 새로 정했다. MV는 노출 면을 배치에 따라 아홉 부류로 나눠 가중하는 추정기다. 물체·배경 평균을 쓰면 반경 2 voxel 구에서도 평균 상대오차가 < 1 %였고, 최악 경우인 평면의 CV는 2.33 %였다. 원문은 국소 추정기라 multigrid 수렴이 없다고 밝혔고, 검토 측은 오목 형상과 접촉 계면이 시험되지 않았다고 본다. 우리 STEP4의 A_face는 노출 면 하나를 h²로 세는 가중 없는 면 세기라, MV가 줄이려 한 편향을 그대로 안고 있다. [근거: Windreich et al. 2003 (`windreich2003_voxel_based_surface_area_estimation`)]

다축척 결합과 입도분포 역산은 방법의 뼈대만 우리 쪽에 닿는다. Balasubramanian et al. 2026은 kMC 결과를 RBF 대리모델로 보간해 LBM 계산에 일방으로 결합했다. 결합 가정이 깨지는 경계 복셀 비율은 CA라는 지표로 따로 냈다. 우리 DEM에서 접촉망, STEP3, STEP4로 이어지는 단계 결합도 이와 구조가 같고, 되먹임이 없다는 한계도 같다. Eizenhammer et al. 2026은 C/50 반쪽셀 곡선에서 LFP 입도분포를 역산해 모드 반경 34.48 nm를 얻었지만, 검토 측은 이 분포가 영상으로 검증되지 않았다고 본다. 우리 NCM811은 고용체이고 반경이 µm 수준이라 이 역산이 원리적으로 안 되며, 가져올 것은 층화 역변환 표본과 가중 대표입자 같은 방법뿐이다. [근거: Balasubramanian et al. 2026 (`balasubramanian2026_rfb_electrolyte_kmc_lbm_preprint`); Eizenhammer et al. 2026 (`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`)]

### 측정은 규약에 묶인다

같은 이름의 측정값이라도 전극 접촉 규약에 따라 크게 움직인다. Beutl et al. 2024에서 네 기관이 같은 지시서로 잰 SS 차단 전극 이온전도도는 0.3–0.4 mS/cm로 모였다. 같은 셀의 C/20 방전 용량은 102–144 mAh/g로 흩어졌다. 원문은 Al/C 박을 펠릿과 함께 누른 co-press가 전극과 전해질의 기계적 접촉을 개선했다고 해석했다. 검토 측은 규약 차가 기관 차보다 크며, 규약을 바꾸면 ×2.5–5.5가 된다고 본다. 그래서 우리는 코인셀 SS 값을 σ₀ 1.5 mS/cm의 근거에서 빼고, co-press처럼 접촉을 만든 값만 같은 층으로 본다. [근거: Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`)]

밀도 기준과 문헌 라벨에도 규약 문제가 남아 있다. Beutl et al. 2024는 1.64 g cm−3를 결정학 밀도라 부르고 상대밀도를 냈다. 검토 측은 Z = 4 결정학 산술로 1.86 g/cm³이 나오며, 이 기준이면 같은 펠릿의 공극이 14.0–19.9 %라고 본다. Lee et al. 2026의 학습용 CE는 문헌에서 모은 값인데 프로토콜 정규화 언급이 없어, 모델이 측정 관례를 배웠을 가능성이 있다. Park et al. 2026의 이온전도도는 액체전해질을 머금은 분리막의 값이라, 고체전해질 접촉망의 σ_ionic과 이름만 같다. [근거: Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`); Lee et al. 2026 (`lee2026_eecfp_dnn_electrolyte_ce_lmb`); Park et al. 2026 (`park2026_ceramic_pp_separator`)]

### 지표끼리 엇갈리는 곳

한 지표가 좋다고 다른 지표가 따라오지 않는 사례가 여러 계에서 되풀이된다. Park et al. 2026에서 DB-PP는 이온전도가 가장 높았지만 Li 연속 도금 시험에서 46 h에 단락됐다. 원문은 이온수송과 단락 저항이 trade-off 관계라고 적었다. Al₂O₃ 코팅 뒤에는 단락시간이 77 h로 늘었다. Lee et al. 2026에서 DBE:Toluene은 풀셀 평균 CE가 두 번째로 높았지만 20사이클 만에 80 %로 떨어졌고, 검토 측은 이를 CE 하나만 최적화하면 부족하다는 교훈으로 읽는다. [근거: Park et al. 2026 (`park2026_ceramic_pp_separator`); Lee et al. 2026 (`lee2026_eecfp_dnn_electrolyte_ce_lmb`)]

미세구조 지표와 계면 지표 사이에서도 순위가 조건에 따라 갈린다. Balasubramanian et al. 2026은 표면적 큰 전극이 δV̄에, 투과율 큰 전극이 CA에 유리하다고 적었다. 검토 측은 그림이 본문 서술과 어긋나는 예외를 세 곳 짚는다. Cho et al. 2026에서 PAA-rGO의 핵생성 과전위는 26 mV로, CMC-rGO의 21 mV보다 조금 높았다. DFT 결합에너지 순위도 bilayer 형상에서는 CMC-GO가 PAA-GO보다 강해, 검토 측은 이 순위를 형상에 따라 달라지는 결과로 읽는다. [근거: Balasubramanian et al. 2026 (`balasubramanian2026_rfb_electrolyte_kmc_lbm_preprint`); Cho et al. 2026 (`cho2026_eipc_zn_anode_azib`)]

### 우리 계와의 거리

액체·수계 전지의 계면 문헌 세 편은 우리 황화물 복합양극 모델과 물리가 달라 수치를 가져오지 않는다. Cho et al. 2026은 Zn 음극 위 GO와 PAA 복합막을 다룬다. Choi et al. 2026은 탄성 집전체 위 Li 도금을, Park et al. 2026은 Li metal 셀의 분리막을 다룬다. Choi et al. 2026의 유효 탄성률 31.4 MPa는 ν=0.50 가정과 diamond compliance 무시를 깐 근사값이며, 검토 측은 이 논문을 σ나 porosity의 수치 앵커로 쓰지 말라고 적었다. 유일한 접점은 부드러운 계면의 응력완화라는 주제가 우리 MPM 소성역학과 spring-back 주제에 멀리서 닿는다는 점이다. [근거: Cho et al. 2026 (`cho2026_eipc_zn_anode_azib`); Choi et al. 2026 (`choi2026_elastomeric_li_metal_anode`); Park et al. 2026 (`park2026_ceramic_pp_separator`)]

Lee et al. 2026은 전해질 계보다 방법이 우리에게 닿는다. 우리 47-dopant cascade 결과에 가벼운 모델과 SHAP을 얹으면, 어떤 도펀트 성질이 어떤 축을 끌어올리는지 정량 규칙을 얻을 수 있다. 원문에서 Linear 모델은 train RMSE 0.16에서 test 3.05로 무너졌다. 우리 표본은 47개로 더 작으므로 이 사례를 경고로 삼아 트리 기반 모델과 교차검증을 쓰는 편이 현실적이다. 검토 측은 원문이 도출한 설계 규칙이 이미 확립된 커뮤니티 지식의 재발견이라고 본다. [근거: Lee et al. 2026 (`lee2026_eecfp_dnn_electrolyte_ce_lmb`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| MV 추정 구 평균 상대오차, 반경 2 voxel | < 1 % | Windreich et al. 2003 (`windreich2003_voxel_based_surface_area_estimation`) |
| DEM 보정 리뷰가 다룬 참고문헌 수 | 238 | Coetzee 2017 (`coetzee2017_dem_calibration_review`) |
| Hertz+SJKR 안식각 최고값 | 73.08° | Shenouda & Hoff 2020 (`shenouda2020_dem_metal_powder_am_liggghts_tutorial`) |
| Li₆PS₅Cl 코인셀 SS 이온전도도 | 0.3–0.4 mS/cm | Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`) |
| Beutl 상대밀도 기준 결정학 밀도 | 1.64 g cm−3 | Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`) |
| LFP 역산 PSD 모드 반경, C/50 | 34.48 nm | Eizenhammer et al. 2026 (`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`) |
| MeTHF:TTE 실측 Aurbach CE | 99.72 % | Lee et al. 2026 (`lee2026_eecfp_dnn_electrolyte_ce_lmb`) |
| DB-PP 분리막 단락시간 | 46 h | Park et al. 2026 (`park2026_ceramic_pp_separator`) |

### 아직 열린 문제

- Li₆PS₅Cl 펠릿의 상대밀도 기준이 정해지지 않았다. 원문은 1.64 g cm−3를 결정학 밀도로 썼고, 검토 측은 결정학 산술로 1.86 g/cm³이 나온다고 본다. 1.64의 근거는 원문과 인용 문헌 어디에서도 확인되지 않았다. [근거: Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`)]
- 고압 소성 압밀에서 DEM 보정의 유일성을 뒷받침할 문헌이 이 장에 없다. Coetzee 2017에는 강성을 치밀화 목표에 맞춘 사례가 없다. Shenouda & Hoff 2020은 소성 항복 분기가 없는 탄성 접촉만 다룬다. [근거: Coetzee 2017 (`coetzee2017_dem_calibration_review`); Shenouda & Hoff 2020 (`shenouda2020_dem_metal_powder_am_liggghts_tutorial`)]
- 오목 형상과 두 물체가 닿는 계면에서 복셀 면적 추정기가 얼마나 정확한지는 시험되지 않았다. 원문의 성능 시험은 볼록한 구와 타원체뿐이고, 디지털화 규칙도 적혀 있지 않다. [근거: Windreich et al. 2003 (`windreich2003_voxel_based_surface_area_estimation`)]
- Eizenhammer et al. 2026의 정밀도 주장은 검토 측 판독과 어긋난다. 검토 측은 반경 불확도가 < 5 %가 아니라 −8.7 / +10.5 %라고 본다. 또 C/2 충전 RMSE 7.4 mV가 그림의 11.7 mV, 8.3 mV와 맞지 않는다고 본다. [근거: Eizenhammer et al. 2026 (`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`)]

### 먼저 읽을 논문

1. Coetzee 2017 (`coetzee2017_dem_calibration_review`) — DEM 파라미터를 왜 역보정하고 그 해가 왜 유일하지 않은지 알아야, 우리 E_eff 보정이 어디에 서 있는지 볼 수 있다.
2. Beutl et al. 2024 (`beutl2024_round_robin_coin_cell_sulfide_assb`) — 이 장에서 유일하게 황화물 전고체를 다룬 외부 기준점이고, 측정값이 접촉 규약에 묶이는 모양을 보여 준다.
3. Windreich et al. 2003 (`windreich2003_voxel_based_surface_area_estimation`) — 우리 STEP4 계면 면적이 안고 있는 면 세기 편향과 그 진단 설계를 알려 준다.
4. Eizenhammer et al. 2026 (`eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`) — 입도분포를 DEM 입자 템플릿으로 바꾸는 층화 역변환 표본 규약의 출처다.
5. Shenouda & Hoff 2020 (`shenouda2020_dem_metal_powder_am_liggghts_tutorial`) — 우리 LIGGGHTS 입력 스크립트와 명령어 골격이 같아 input을 읽는 입문서로 쓸 수 있다.

## 이 장의 논문 (12편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `bzox_dry_zro2x_nmc_shell_coating_sulfide_assb` |  | superseded by choi2026_bzox_dry_zro2x_nmc_shell_coating.md | 이 기록은 보조자료(SI)만으로 만든 구판이며, 본문을 확보한 뒤 내용이 통합본으로 모두 옮겨졌다. |
| `windreich2003_voxel_based_surface_area_estimation` | Windreich et al. 2003 | Voxel-based surface area estimation: from theory to practice | 노출 면 배치로 가중하는 MV 추정기에 물체·배경 평균을 쓰면 반경 2 voxel 구에서도 넓이 오차가 1 % 아래다. |
| `chandratilleke2012_particle_scale_mixing_index` | Chandratilleke et al. 2012 | A particle‐scale index in the quantification of mixing of particles | (카드 없음) |
| `coetzee2017_dem_calibration_review` | Coetzee 2017 | Review: Calibration of the discrete element method | DEM 파라미터는 벌크 역보정으로 정하는 일이 가장 흔하다. 다만 해가 유일하지 않아 여러 실험과 별도 검증이 필요하다. |
| `shenouda2020_dem_metal_powder_am_liggghts_tutorial` | Shenouda & Hoff 2020 | Discrete Element Method Analysis for Metal Powders Used in Additive Manufacturing, and DEM Simulation Tutorial Using LIGGGHTS-PUBLIC | LIGGGHTS-PUBLIC 입문 튜토리얼이다. Hertz와 SJKR 접촉으로 점착이 커질수록 금속 AM 분말의 안식각이 오르고 유량이 떨어짐을 보였다. |
| `beutl2024_round_robin_coin_cell_sulfide_assb` | Beutl et al. 2024 | Round‐robin test of all‐solid‐state battery with sulfide electrolyte assembly in coin‐type cell configuration | 네 기관이 같은 재료와 지시서로 CR2032 코인셀을 만들자 이온전도도는 모였고, 셀 성능과 수명은 흩어졌다. |
| `balasubramanian2026_rfb_electrolyte_kmc_lbm_preprint` | Balasubramanian et al. 2026 | Insights into Electrolyte Effects on Interfacial Kinetics and Transport in Porous Redox Flow Battery Electrodes: A Multiparadigm Modelling Study | MV 농도를 높이면 이중층 동역학은 좋아지지만 기공 수송은 나빠지고, 전극 표면적과 투과율은 서로 다른 지표를 좌우한다. |
| `cho2026_eipc_zn_anode_azib` | Cho et al. 2026 | Electronic-ionic polymer composite with proton-coupled electron transfer reaction: From low N/P ratio to high zinc utilization for aqueous zinc ion batteries | GO와 PAA 복합막을 Zn 음극에 입히면 PCET로 탈용매가 쉬워지고, 002 배향 도금으로 낮은 N/P 파우치셀까지 버틴다. |
| `choi2026_elastomeric_li_metal_anode` | Choi et al. 2026 | High‐Performance Elastomeric Lithium Metal Anodes Enabled by a Lithiophilic Monolayer‐Assembled Nano‐Crumpled Micro‐Concave Architecture | 부드러운 PDMS 집전체에 이중 주름 구조와 TREN 단분자층을 더하면 Li 핵생성 과전위가 낮아지고 덴드라이트가 억제된다. |
| `eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell` | Eizenhammer et al. 2026 | Determining the Particle Size Distribution of an LiFePO₄ Electrode for Full-Cell Many-Particle Modeling | 입자 크기마다 다른 스피노달 간극 덕분에 C/50 반쪽셀 곡선에서 LFP 입도분포를 읽고, 그 분포로 풀셀 전압을 재현했다. |
| `lee2026_eecfp_dnn_electrolyte_ce_lmb` | Lee et al. 2026 | Interpretable enhanced-ECFP-guided deep learning for rational electrolyte design and Coulombic efficiency prediction in lithium metal batteries | 농도 가중 분자지문으로 학습한 DNN을 SHAP으로 해석해 얻은 규칙대로 조합한 전해질이 Li–Cu CE 99.72 %를 냈다. |
| `park2026_ceramic_pp_separator` | Park et al. 2026 | Ultra-thin ceramic-coated dry-biaxially stretched polypropylene separator achieving balanced ionic transport and short-circuit resistance in lithium metal batteries | 건식 이축연신 PP 분리막에 스퍼터 Al₂O₃ 초박막을 입히면 기공구조는 그대로 두고 이온전도와 단락 저항이 함께 오른다. |
