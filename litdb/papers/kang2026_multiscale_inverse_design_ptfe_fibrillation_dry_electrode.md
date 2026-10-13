<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation.md · lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode.md (같은 팔로우 랩, 같은 날) ·
     kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md · kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md.
     쪽 표기 = 본문 "p.N" (= 학술지 인쇄 쪽 N = 받은 PDF N 쪽, 전 11 쪽) · SI "SI p.N" (= 받은 SI PDF N 쪽, 전 11 쪽 — p.1 제목 · 저자 / p.2–8 그림 S1–S7 (한 쪽에 하나) /
     p.9 표 S1–S2 / p.10 Note 1 / p.11 SI 참고문헌 2 편).  ⚠ 받은 SI 는 Word 에서 내보낸 PDF (문서 메타 작성자 "강준혁" · 생성 2025-12-09) — 학술지 게시 SI 와 같은 판인지 [미확인].
     ★ 보조 코드 (Sup2 = 확장자 .unk 인 Jupyter 노트북 JSON, 570 kB) 는 **실행 · import · 변환하지 않았다** — `python3 -I` 의 json.load 로 셀 원문 · 출력 텍스트만 읽었다
       (출력 PNG 6 장은 해독하지 않음).  노트북은 리포에 넣지 않는다.  노트북에서 가져온 값 = [SI 코드].
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 보정 검산은 파일 머리, TREND 전용) ·
     [SI 코드] = 노트북 셀 원문 · 저장된 출력 텍스트 · [우리 산술] = 인쇄 · 코드 값으로 우리가 다시 한 계산 · [추정] = 우리 해석 ·
     [미확인] = 본문 11 쪽 + SI 11 쪽 + 노트북 전수에 없음 · [미확보] = 본문이 언급하지만 받지 못한 자료 (peer review file).  SI 미확보 항목은 없다 (본문이 부르는 SI 그림 1–3 · 6 · 7 · 표 S1–S2 · 코드 모두 받음).
     크롭 19 장 (본문 그림 1–6 · 식 1 · 식 2–4 · 식 5–8 · SI 그림 S1–S7 · SI 표 S1–S2 · SI Note 1) 전부 렌더로 열람 (접촉 시트 포함). -->

# 건식 PTFE 전극에서 활물질 입경이 PTFE 섬유화를 정한다는 다중 척도 틀 — 2D FEM (Arruda–Boyce 계열 PTFE 를 두 세라믹 입자 사이에서 '입자 하중 압력 PLP' 로 끌어 늘림) + GPR + 최적화 → SiO₂ 모형 입자로 단봉 10 µm · 쌍봉 10 + 5 µm 가 최적 (PLP ≈14 MPa · 반죽기 10 rpm = 13.49 MPa · 압출기 700 rpm = 13.6 MPa, 모델 값) → LFP 쌍봉 건식 후막 7 · 10 mAh cm⁻² (214 · 280 µm) — 그러나 '섬유화' 는 구성식에 없는 사후 구간 · 입경 효과의 길이척도 원천 미기재 · 실물 공정 조건 · 전기화학 대조군 없음 · 보조 코드의 목적함수 · 그림 5e 가 본문과 어긋난다 — Jun Hyuk Kang · Woojin Jeong … Junghyun Choi · Sung Beom Cho (아주대 · 한양대 · 가천대 · 경북대 · UT Dallas, Commun. Mater. 2026)

> **[팔로우 랩: 가천대 최준현 교수 (건식 전극)]**
> slug `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` · DOI `10.1038/s43246-025-01046-0` · type `FEM (COMSOL 2D PTFE 대변형 · 반죽기/압출기 유동-열) + ML (GPR · Bayesian optimization, 보조 Jupyter 노트북) + exp (SiO₂ 모형 입자 dry electrode PTFE binder 섬유화 · PSD · 탭 밀도 · UTM · MIP porosity · SEM · LFP 반쪽셀 EIS impedance · 사이클, 액체 전해질); DEM · MPM 없음` · PDF `cf16f39a-5._Multiscale_insights_enable_rational_design_of_solvent-free_dry_electrode_processing_for_advanced_battery_electrode_fabrication.pdf` · SI `f4777437-5._Sup_Multiscale_insights_enable_rational_design_of_solvent-free_dry_electrode_processing_for_advanced_battery_electrode_fabrication.pdf` · SI 코드 `9f5a5da5-5._Sup2_Multiscale_insights_enable_rational_design_of_solvent-free_dry_electrode_processing_for_advanced_battery_electrode_fabrication.unk` (Jupyter 노트북 JSON — 텍스트로만 읽음 · 리포 미반입) · digested `2026-10-13` · status ✅
>
> elements: Si, O, Li, Fe, P, C, F
> methods: FEM, GPR, Bayesian optimization, EIS, MIP, SEM
>
> **원제**: *Multiscale insights enable rational design of solvent-free dry electrode processing for advanced battery electrode fabrication* (p.1 · 분류 "Article")
> **저자 (p.1 · SI p.1, 인쇄 순서 그대로)**: Jun Hyuk Kang^1,2 · Woojin Jeong^3 · Min Sung Kang^1,2 · Hyeon Woo Kim^2,4 · Dong Won Jeon^1,2 · Han Uk Lee^1,2 · Ji Hoon Hong^1,2 · Seungmin Han^3 · Minseok Kim^5 · Subi Yang^6 · Dongsoo Lee^5 · Patrick Joohyun Kim^6 · Taeseup Song^3 · Moonsu Yoon^5 · Laisuo Su^7 · **Junghyun Choi^5 ✉** · **Sung Beom Cho^1,2,4 ✉** (✉ = p.1 교신 표지 · SI p.1 은 *"Corresponding authors"* 로 같은 둘에 \* · 1저자 둘 = J.H.K. · W.J. *"contributed equally"* (p.10) = SI 의 †)
> **소속 (p.1 인쇄 그대로)**: 1 Department of Energy Systems Research, Ajou University, Suwon, Republic of Korea · 2 Department of Materials Science and Engineering, Ajou University, Suwon · 3 Department of Energy Engineering, Hanyang University, Seoul · 4 Ajou Energy Science Research Center, Ajou University, Suwon · 5 School of Chemical, Biological and Battery Engineering, **Gachon University**, Seongnam-si, Gyeonggi-do · 6 Department of Applied Chemistry, Kyungpook National University, Buk-gu, Daegu · 7 Department of Materials Science and Engineering, The University of Texas at Dallas, Richardson, TX, USA (SI p.1 은 같은 일곱을 a–g 로 · 우편번호까지)
> **교신 전자우편 (p.1)**: junghchoi@gachon.ac.kr · csb@ajou.ac.kr — *"Correspondence and requests for materials should be addressed to Junghyun Choi or Sung Beom Cho."* (p.10)
> **팔로우 랩 표지 근거**: 인쇄 로마자 **"Junghyun Choi"** — 소속 5 (가천대 화공 · 생명 · 배터리공학부) · **공동 교신저자** (p.1 ✉ · p.10 · SI p.1).  형제 카드 셋 (`gandla2026_…` · `kim2026_pregranulation_…` · `lee2026_li_underlayer_…`) 과 같은 전자우편 (junghchoi@gachon.ac.kr) · 같은 NRF 과제 번호 **RS-2024-00408156** (이 논문 p.10 감사의 글 첫 줄 — 세 형제 카드 모두 이 번호를 싣고, `lee2026_li_underlayer_…` 는 J. Choi 몫으로 명시) · PTFE 등급 F-106 (Daikin) 도 `lee2026_li_underlayer_…` 와 같다.  ⚠ 한글 이름은 PDF 어디에도 인쇄되지 않았다 — "Junghyun" 은 흔히 "정현" 의 로마자이므로 1저자가 말한 "최준현" 과 같은 분인지 [미확인] (같은 가천대 · 건식 전극 교신이라는 점은 PDF 로 확인됨).  주도 연구실은 아주대 조성범 (Sung Beom Cho — 1저자 J.H.K. 소속 · 계산 · 소프트웨어 담당) 으로 보인다 [추정 — CRediT]; J. Choi 의 기여 = *"Writing—review & editing, Supervision, Funding acquisition, Project administration"* (p.10).  같은 소속 5 의 Dongsoo Lee · Minseok Kim · Moonsu Yoon 은 여기서는 교신이 아니다.
> *Communications Materials* (2026) **7**:34 (11 쪽, Article) · 접수 2025-07-11 · 승인 2025-12-11 · 온라인 2025-12-25 (p.9 — 이 줄은 PDF 안에서 이미지로 박혀 있어 텍스트 추출에 안 잡힌다) · © The Author(s) 2025 · **CC BY-NC-ND 4.0** (p.11 — 개작물 배포 불가 조건, 크롭은 내부 참조용) · 연구비 NRF (MSIT) RS-2024-00408156 · RS-2024-00407282 (p.10) · 이해상충 없음 · 데이터 = *"available from the corresponding authors upon reasonable request"* (p.9) · 코드 = *"available in the Supplementary Code file"* (p.9 — = 받은 Sup2 노트북; GPR · 최적화 부분만, COMSOL 모델은 없음) · peer review file *"is available"* (p.10) [미확보] · 참고문헌 41 편 (본문) + 2 편 (SI).
> **같은 축 카드 (링크만)**: [`kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation`](kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation.md) · [`lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode`](lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode.md) (같은 팔로우 랩 · 건식 PTFE) · [`lee2024_shear_force_dry_process_cathode_coverage`](lee2024_shear_force_dry_process_cathode_coverage.md) (이 논문 ref 15) · [`matthews2024_ptfe_nanofibril_network`](matthews2024_ptfe_nanofibril_network.md) (ref 17) · [`lee2025_dual_fibrous_ptfe_dry_electrode`](lee2025_dual_fibrous_ptfe_dry_electrode.md) (PTFE 섬유 · 로프 계층) · [`cronk2026_lis_positive_electrode_geometry_fem`](cronk2026_lis_positive_electrode_geometry_fem.md) (길이척도 없는 FEM 의 입경 무감 — CL-64) · [`sun2026_dem_extrusion_recirculation_dry_electrode`](sun2026_dem_extrusion_recirculation_dry_electrode.md) (압출 건식 DEM) · [`mcgeary1961_bimodal_sphere_packing`](mcgeary1961_bimodal_sphere_packing.md) (쌍봉 충전).
> **판독 원자료**: `litdb/figures/kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode/digitized.csv` (그림 2b · 3a–c · 3h · 4a–c · 4g · 5c · 5e · 5f · 6a · 6e–g · SI 1 · SI 6 — 보정 검산 머리) · 크롭 19 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 이 논문은 "건식 PTFE 전극의 섬유화 품질은 활물질 입경 (과 입경 분포) 이 PTFE 에 거는 국소 응력으로 정해진다" 는 가설을, (i) 두 개 (쌍봉은 네 개) 의 세라믹 원 사이에 PTFE 원 하나를 넣고 원에 압력 (PLP) 을 거는 **2D COMSOL 초탄성 FEM** [판독 — 차원 미기재], (ii) 그 결과 표 (입경 × PLP → 최종 P_lm · 최종 변형률) 를 보간하는 **GPR** 과 제약 (P_lm < 45 MPa · ε < 4) 아래 최적점 찾기, (iii) 반죽기 · 압출기의 **거시 유동 FEM** 으로 rpm → 전단 응력 → PLP 환산, (iv) **SiO₂ 모형 입자** (0.1 · 1.5 · 10 · 20 µm 와 10 + 5 · 10 + 1.5 µm) 의 SEM · 응집 강도 · MIP · 탭 밀도, (v) **LFP 쌍봉 (5 + 10 µm) 건식 후막** 7 · 10 mAh cm⁻² 의 반쪽셀로 엮어 "10 + 5 µm · PLP ≈14 MPa · 반죽기 10 rpm" 을 제안한다 — 그러나 **섬유화 자체는 구성식에 없고** (응력–변형 곡선 위에 사후로 그은 구간), **입경 효과가 어디서 오는지** (PTFE 크기 · 하중 정의) 가 적혀 있지 않으며, **실물 공정 조건과 대조 전극이 없고**, 보조 코드는 본문이 말한 목적함수 ("최종 변형률 최대화") 를 쓰지 않는다 (§3-7 · §10).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도) | 실물: 150 g 배치 · 고전단 회전 혼합기 PLS-300 → 압출기 NEP-0.5K + 분쇄기 PLS-300 (섬유화) → 롤 프레스 KRM-100D3 → 캘린더 → 탄소 코팅 Al 라미네이트 (모두 KMTECH) — **rpm · 시간 · 온도 · 간극 · 압력 수치 0** · ⚠ **반죽기는 Methods 장치 목록에 없다**.  모델: 반죽기 **10 rpm = 13.49 MPa** · 압출기 **700 rpm = 13.6 MPa** (COMSOL, 벽 80 °C) — 이 rpm 으로 실제 전극을 만들었다는 문장 없음 | [인쇄] p.6 · p.8–9 |
| ② 입자 · 크기 · 조성 | SiO₂ 단봉 0.1 · 1.5 · 10 · 20 µm (최빈 ≈0.19 · 1.48 · 12.4 · 22.0 µm [판독]) · 쌍봉 10+10 · 10+5 · 10+1.5 (**섞는 비율 미기재**) · LFP 5 + 10 µm (비율 미기재) · **AM : CB (Super P) : PTFE (F-106, Daikin) = 90 : 5 : 5 wt%** · 탭 밀도 1.42 / 1.38 / 0.98 / 0.5 · 1.38 / 1.40 / 1.18 g/cc | [인쇄] p.9 · SI Fig 2–3 · [판독] Fig 3a |
| ③ 미시 모형 (FEM) | COMSOL "Nonlinear Elastic Material module" · AM–PTFE–AM 세 원 (쌍봉: 큰 둘 + 작은 둘) · PTFE = Arruda–Boyce 8사슬 (식 4) + 표 S1 의 **가지 2 개 · 흐름 저항 · 응력 지수** (점탄소성 계열 모수 — 본문 식과 안 맞음) · PLP 0.1–25 MPa · 출력 = 최종 2nd PK 응력 P_lm · 최종 변형률 · 섬유화 = P_lm < 45 MPa (데이터시트 인장 강도) · ε < 4 안의 **사후 구간** | [인쇄] p.2 · p.8 · SI 표 1 · [판독] SI Fig 1 |
| ④ ML · 최적화 | GPR (상수 × Matérn ν = 1 + 백색잡음) · 학습 270 (단봉 9 크기 × 30 PLP) · 200 (쌍봉 8 × 25) · **5-겹 CV R² 0.989 · 0.995 (응력 모형만)** · 크기별 '최적 PLP' = **제약 경계 (σ = 45 MPa) 의 격자 탐색** — 단봉 10 µm 14.41 · 9 µm 15.61 · 8 µm 16.87 MPa … · BO 결과 자체는 논문에 안 쓰임 | [인쇄] p.5 · [SI 코드] |
| ⑤ 실험 측정 | 응집 강도 (UTM, N — 시험 형상 미기재): 10 µm ≈0.74 · 20 µm ≈0.31 · 1.5 µm ≈0.05 · 0.1 µm 실패 / 10+5 ≈0.88 · 10+10 ≈0.73 · 10+1.5 ≈0.09 N [판독] · MIP 공극 37.2 / 32.2 / 46.7 % (20 / 10 / 1.5 µm) · 32.2 / 29.9 / 36.1 % (10+10 / 10+5 / 10+1.5) · SEM 정성 (섬유 vs 막) | [판독] Fig 3c · 4c · [인쇄] Fig 3h · 4g |
| ⑥ 전기화학 | LFP 반쪽셀 (Li · **1.15 M LiPF₆ 액체**) 7 · 10 mAh cm⁻² · 214 · 280 µm · R_ct **25.84 · 33.42 Ω** (면적 미정규화) · 0.1 C 50 사이클 · CE > 99 % · 10 mAh cm⁻² **≈10.1 → ≈9.2 mAh cm⁻² (≈−9 %)** [판독] 인데 본문은 *"no degradation"* · **대조군 없음** (단봉 LFP · 비최적 건식 · 습식 전기화학 0) | [인쇄] p.8 · [판독] Fig 6g |
| ⑦ 믹서 논문 V1 · V2 · V3 | V1 (코팅 상태) n/a — SE 없음 · 모형이 입자 재질에 무감 (SI Fig 6) · **V2 (혼합 시간)** — 시간 축 데이터 없음 (서론의 ref 16 진술뿐), 강도 (rpm → 응력) 사상의 **선례** · V3 (SE 함량) n/a — 단 **미세 분획 (1.5 µm, 크기비 0.15) 이 섞이면 탭 밀도 −14.5 % · 공극 +3.9 %p · 섬유화 부족** [우리 산술 · 인쇄] = 우리 SE 1 µm (SE/AM_P 0.111) 와 같은 영역의 정성 실례 (SiO₂ 대리) | [인쇄] p.1 · p.4–5 · SI Fig 3 · [추정] §7-5 |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB** (LFP 반쪽셀) — 황화물 SE 없음 ② 입경 실험은 **SiO₂ 구형 모형 입자** — LFP 로 옮긴 근거는 FEM 곡선 겹침 (SI Fig 6) 하나 ③ **실물 공정 조건 (rpm · 시간 · 온도 · 간극 · 압력) 미기재** — 모델 '최적 조건' 으로 실제 전극을 만들었다는 문장 없음 ④ 전기화학 **대조군 없음** · 셀 수 · 오차 막대 0 ⑤ FEM 은 '섬유화' 를 **구성식으로 담지 않는다** (응력–변형 곡선 위 사후 구간) ⑥ 원자료는 요청 시 (p.9) · **COMSOL 모델 파일 미공개** (보조 코드 = GPR · 최적화만) ⑦ 판독값은 TREND 전용.

---

## 1. 한 줄 요약

용매 없는 PTFE 건식 공정은 전단으로 PTFE 를 섬유로 늘려 활물질 · 도전재를 묶지만, 섬유화가 부족하면 전극이 부서지고 지나치면 섬유가 막 (film-like) 으로 바뀌어 역시 취성이 된다 (서론 · ref 16).  저자들은 거시 장비 (반죽기 · 압출기) 의 전단이 미시 입자–PTFE 상호작용으로 어떻게 넘어가는지 모른다는 점을 문제로 세우고 (p.1–2), (a) 두 세라믹 원이 엇갈린 압력 (PLP) 으로 PTFE 원을 끌어 늘리는 COMSOL 초탄성 FEM 의 응력–변형 곡선을 탄성 · 소성 · 섬유화 · 막 네 구간으로 나눈 뒤 (Fig 2), (b) SiO₂ 모형 입자로 "20 µm 는 막 · 10 µm 는 섬유화 · 1.5 µm 는 섬유화 부족 · 0.1 µm 는 탄성만" 이라는 입경 순서를 FEM 곡선과 SEM · 응집 강도 · MIP 로 맞추고 (Fig 3), (c) 10 µm 에 5 µm 를 섞으면 섬유화가 늘고 (본문 "7.4 %") 1.5 µm 를 섞으면 줄어든다고 보이고 (Fig 4), (d) FEM 결과 표를 GPR 로 보간해 입경별 '최적 PLP' (P_lm < 45 MPa · ε < 4 경계) 를 찾고 반죽기 · 압출기 유동 FEM 으로 그 응력을 rpm 으로 바꿔 "10 + 5 µm · 반죽기 10 rpm (13.49 MPa)" 을 제안한다 (Fig 5).  마지막으로 SiO₂ 결과를 형상이 비슷한 LFP 로 옮겨 5 + 10 µm 쌍봉 LFP 건식 후막 (7 · 10 mAh cm⁻², 214 · 280 µm) 을 만들고 균열 없는 사진 · 작은 R_ct 증가 · 3.43 V 근처 평탄 전압 · 50 사이클 CE > 99 % 를 보인다 (Fig 6 · SI Fig 7).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (AM / 도전재 / 바인더 / 전해질) | 연구유형 |
|---|---|---|---|---|
| J. H. Kang† · W. Jeong† · M. S. Kang · H. W. Kim · D. W. Jeon · H. U. Lee · J. H. Hong · S. Han · M. Kim · S. Yang · D. Lee · P. J. Kim · T. Song · M. Yoon · L. Su · J. Choi\* · S. B. Cho\* (아주대 · 한양대 · 가천대 · 경북대 · UT Dallas) | *Commun. Mater.* 7 (2026) 34 | 10.1038/s43246-025-01046-0 | SiO₂ (모형) · LiFePO₄ (5 + 10 µm) / Super P / PTFE F-106 (Daikin) / 액체 1.15 M LiPF₆ EC/EMC/DEC | FEM (미시 초탄성 + 거시 유동-열) + GPR · 최적화 + 실험 (분말 · 막 · 반쪽셀) |

- † = 공동 1저자 (p.10 *"contributed equally"*) · \* = 교신.
- CRediT (p.10): J.H.K. = 초고 · 착상 · 방법 · **소프트웨어** · 조사 · 분석 · 시각화 / W.J. = 초고 · 방법 · 조사 · **검증** · 분석 / M.S.K. = 소프트웨어 · 분석 / H.W.K. · H.U.L. · J.H.H. = 시각화 / D.W.J. = 분석 · 시각화 / S.H. · M.K. · S.Y. = 조사 · 검증 / D.L. · P.J.K. · T.S. · M.Y. · L.S. = 지도 / **J.C. · S.B.C. = 검토 · 지도 · 연구비 · 과제 관리**.
- 계산 (FEM · GPR) = 아주대 쪽 (J.H.K. · M.S.K. 소프트웨어), 전극 · 셀 실험 = W.J. (한양대) · 가천대 · 경북대 쪽으로 보인다 [추정 — CRediT · 소속].
- Woojin Jeong 은 이 논문에서 소속 3 (한양대) 만 인쇄 — 형제 카드 `lee2026_li_underlayer_…` 의 Woojin Jeong 은 가천대 + 한양대 (b, c) 로 인쇄 (같은 사람인지 [미확인]).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 조성 · 공정 · 셀 (Methods p.8–9 · SI Fig 2–3 · 7)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 모형 활물질 | SiO₂ — *"small particles (0.1, 1.5, and 5 μm), large particles (10 and 20 μm), and bimodal mixtures"* · PSD = 레이저 산란 LA-950 (Horiba, 증류수 + 초음파 분산) · 구매/합성 출처 [미확인] (본문은 *"can be synthesized with uniform PSD"* 에 ref 33 을 단다 — §10-17) | [인쇄] p.9 · p.2 |
| PSD 최빈 | 0.1 µm 시료 ≈**0.19 µm** (41 %) · 1.5 → ≈1.48 · 10 → ≈12.4 (넓음, ≈5–30 µm) · 20 → ≈22.0 µm · 5 µm 단봉 PSD 는 어디에도 없다 | [판독] Fig 3a |
| 쌍봉 | 10 + 10 · 10 + 5 · 10 + 1.5 µm — **섞는 비율 (질량 · 부피) [미확인]** · Fig 4a 의 10 + 5 는 따로 선 ~5 µm 봉우리 없이 주봉 ≈12.8 µm + ≈1.9 µm 작은 혹 | [인쇄] p.4 · [판독] Fig 4a |
| LFP | 5 + 10 µm 쌍봉 (SEM 한 입자 ≈4.6 · ≈9.3 µm, 거친 응집 구) · 비율 · 공급사 [미확인] | [인쇄] p.7 · p.9 · [판독] Fig 6a |
| 도전재 · 바인더 | carbon black (Super P) · PTFE (F-106, Daikin Industries) | [인쇄] p.9 |
| 조성 | **90 : 5 : 5 wt%** (AM : 도전재 : 바인더) — SiO₂ 막 · LFP 전극 공통 | [인쇄] p.9 |
| 공정 (실물) | 150 g 배치 · ① 고전단 회전 혼합기 PLS-300 *"under controlled shear stress and time conditions"* ② 섬유화 = 압출기 NEP-0.5K + 분쇄기 PLS-300 ③ 롤 프레스 KRM-100D3 → 자립막 → 롤 프레스 캘린더 (목표 두께) → 탄소 코팅 Al 라미네이트 (전부 KMTECH) — **수치 0** | [인쇄] p.9 |
| LFP 로딩 · 밀도 · 두께 | Methods **43 · 69 mg cm⁻²** (7 · 10 mAh cm⁻²) · 목표 밀도 **2.3 g/cc** / SI Fig 7 **44.06 · 63.22 mg cm⁻²** / 단면 **214 · 280 µm** | [인쇄] p.9 · SI p.8 · Fig 6c–d |
| 습식 대조 | 7 mAh cm⁻² · 20 g 슬러리 (쌍봉 LFP · CB · PVDF 90:5:5, NMP) · 닥터 블레이드 · 80 °C 진공 하룻밤 · 로딩 본문 **48.47** ↔ SI **43.42 mg cm⁻²** · 전기화학 측정 없음 (사진만) | [인쇄] p.8–9 · SI p.8 |
| 셀 | CR2032 (Wellcos) · 이슬점 < −50 °C 드라이룸 · PE 분리막 · Li 금속 · **1.15 M LiPF₆ EC/EMC/DEC 2:4:4 (vol) + VC 1 wt% + FEC 10 wt% + LiDFP 1 wt%** | [인쇄] p.9 |
| 시험 | CC–CV **0.1 C · 2.5–4.0 V** vs Li/Li⁺ (WBCS3000L32, WonATech) · EIS Biologic VSP · 5 mV · 250 kHz–10 mHz | [인쇄] p.9 |
| 분석 | 응집 강도 = UTM Autograph AGS-X (Shimadzu) — **시험 방식 · 시료 폭 · 속도 · 반복 수 [미확인]** · MIP AutoPore IV (Micromeritics; ≈0.4 g · 0.10–60,000 psia · 배기 "50 Torr Hg" (인쇄 그대로) · 10 min · Hg 충전 0.43 psia · 평형 10 s) · SEM 장비 [미확인] | [인쇄] p.9 |

**[우리 산술] 로딩 · 두께 · 용량 정합** (기준 질량 = AM 인지 전극 전체인지 인쇄 안 됨):

| | 7 mAh cm⁻² | 10 mAh cm⁻² | 비고 |
|---|---|---|---|
| 용량 ÷ 로딩 — Methods (43 · 69) | 0.163 | **0.145** mAh mg⁻¹ | 두 전극이 11 % 다르다 |
| 용량 ÷ 로딩 — SI (44.06 · 63.22) | 0.159 | 0.158 mAh mg⁻¹ | 서로 같고 Fig 6f 방전 ≈159.7 · ≈158.2 mAh g⁻¹ [판독] 와 맞는다 → SI 로딩이 Fig 6f 와 **같은 질량 기준** [추정] |
| 로딩 ÷ 두께 — Methods | 2.01 | 2.46 g cm⁻³ | 목표 2.3 과 양쪽으로 어긋남 |
| 로딩 ÷ 두께 — SI 를 전극 전체로 | 2.06 | 2.26 g cm⁻³ | |
| 로딩 ÷ 두께 — SI 를 AM 로딩으로 (÷0.9) | **2.29** | 2.51 g cm⁻³ | 7 mAh 만 목표와 맞음 · 두께에 집전체 포함 여부 [미확인] |
| 2.3 g/cc 면 두께 (Methods 로딩) | 187 | 300 µm | 측정 214 · 280 µm |

### 3-2. ★ PTFE 미시 FEM (Fig 2 · SI Fig 1 · SI 표 1 · 식 2–4 · p.2 · p.8)

- **도구 · 기하**: COMSOL *"Nonlinear Elastic Material module"* (p.8, 인쇄 이름 그대로).  Fig 2a = 세라믹 AM – PTFE – 세라믹 AM 세 원 · PLP 화살표가 왼쪽 AM 은 아래로 · 오른쪽 AM 은 위로 (엇갈려 전단) — *"each ceramic AM exerts PLP, generating shear force within the PTFE matrix"* (p.2).  쌍봉 모형 = 큰 원 둘 + 작은 원 둘 + X 자로 늘어난 PTFE (Fig 5g–h 삽화) [판독].  **2D 인지 3D 인지 · 원 치수 · PTFE 초기 크기 · 메시 · 접촉 (접합 / 마찰) · 하중 속도 · 해석 시간 [미확인]** — SI Fig 1 · Fig 1b 의 축이 x · y (µm) 라 2D 단면으로 보인다 [판독].
- **SI Fig 1 (캡션에 하중 없음 — 본문 p.2 가 13 MPa 의 Fig 3b 에 *"the corresponding FEM simulation results"* 라 부른다)**: 0.1 µm AM 이 ≈1 µm PTFE 몸체 양끝에 붙어 거의 변형 없음 (a) · 1.5 µm (b) 는 PTFE 가 타원으로 늘어남 · 10 µm (c) 는 두 원 사이 얇은 띠 (두께 ≲1 µm) · 20 µm (d) 는 더 얇은 막 · 색 막대 ×10⁷ N/m² (0–5 = 0–50 MPa) [판독].  PTFE 몸체 크기가 패널마다 달라 보인다 — (a) ≈1 µm · (b)–(d) 변형 뒤 면적의 원상당 지름 ≈3.6–4.5 µm [판독 · 우리 산술, 2D 비압축 가정] → **AM 대 PTFE 크기 규칙이 적혀 있지 않다**.
- **구성식 (p.8)**: *"the Arruda-Boyce model was chosen … eight-chain molecular network theory, where the Helmholtz free energy is derived from the inverse Langevin function"*.  식 (2) ρ ∂²u/∂t² = ∇·(FS)ᵀ + Fν · 식 (3) F = I + ∇μ · 식 (4) Wₛ = μ₀ Σ_{p=1}^{5} C_p/N^{p−1} (λ₁ᵖ + λ₂ᵖ + λ₃ᵖ) + ¼K(J_el² − 1 − 2 ln J_el) (인쇄 꼴 그대로 — §10-5).  합 항을 *"plastic deformation region"*, 부피 항을 *"elastic deformation region"* 이라 부르고, *"We employed Simo-Taylor"* 를 정의 없이 쓴다.
- **물성 출처 (p.8)**: 인장 강도 · 연신 = F-106 제조사 데이터시트 (값 자체는 본문에 없고 제약 'P_lm < 45 MPa · strain < 4' 로만 등장, p.5) · 영률 · 포아송비 = ref 41 (Bi & Mueller, *Friction* 2019 — PTFE 핀-판 마찰 논문) — 값 미기재.
- **SI 표 1 (SI p.9, 인쇄 그대로)**: energy-storage factor branch 1 **220** · branch 2 initial **29.3** / final **7.91** · relative contribution of I₂ **30** · locking stretch **5.6** · PTFE bulk modulus **2.72 GPa** · flow resistance branch 1 **9.014 MPa** / branch 2 **4.845 MPa** · stress exponent **1** · initial shear modulus **223.7 MPa** · macroscopic shear modulus **200 MPa** · temperature **80 °C**.  → 흐름 저항 · 응력 지수 · 가지 둘은 순수 초탄성 Arruda–Boyce 에 없는 **점탄소성 다중 가지 모형 계열** 모수다 [추정 — 본문 식과 표가 다른 모형을 가리킨다, §10-5].
- **[우리 산술] 탄성 상수**: μ = 200 MPa · K = 2.72 GPa → E = 9Kμ/(3K+μ) = **585.6 MPa** · ν = **0.464** (μ = 223.7 이면 653.2 MPa · 0.460).  Arruda–Boyce 표준 급수 μ_init = μ₀(1 + 3/(5N) + 99/(175N²) + …) 에 μ₀ 200 MPa · N = λ_L² = 31.36 을 넣으면 **203.9 MPa** — 표의 223.7 과 9.7 % 차 (223.7 이 다른 가지 값인지 [미확인]) [우리 산술 · 표준 급수 가정].
- **응력–변형 네 구간 (Fig 2b · p.2)**: I 탄성 (선형) · II 소성 (비선형 누적) · III 섬유화 (*"shear-induced deformation leads to fiber formation"*) · IV 막 (*"If the applied stress exceeds the PTFE tensile strength, the fibrillar structure collapses into the film-like morphology"*).  [판독] I/II 경계 ≈ε 0.30 · 14.2 MPa · II/III 경계 = 축 눈금 **ε 1.13 · 16.8 MPa** · 끝점 ≈ε 2.62 · 29.0 MPa.
- **"검증" (p.2)**: *"the model identifies the fibrillation onset at a strain of 1.13 … where the simulated stress was 16.9 MPa — a value comparable to the experimental result of 16.4 MPa"* · 탄소성 전이도 일치 · 파단 연신은 다름 (*"likely due to variations between the PTFE grades"*).  ⚠ **비교한 실험 곡선은 그림에 없고** 출처 문장 끝 인용이 ref 33 (PTFE 굽힘 응력 곁사슬 절단 논문) 이다 (§10-4).
- **응력 척도**: P_lm = 2nd Piola–Kirchhoff (*"accurately reflects stress under large deformation conditions"*, p.2) · 변형률 정의 (공학 · Green–Lagrange · 로그) · 어느 점 (최대 · 평균) 의 값을 '최종' 으로 뽑는지 [미확인].

### 3-3. ★ 단봉 SiO₂ — 입경 순서 (Fig 3 · SI Fig 1–2 · p.2–4)

- **FEM (13 MPa, p.2)**: 20 µm → 곡선이 실패 영역 (막) 으로 들어감 · 10 µm → *"adequate stress and strain to initiate fibrillation without exceeding the material tensile strength"* — 본문 수치 **항복 ≈27 MPa (ε 0.6) · 섬유화 시작 최고 30 MPa (ε 1.8) · 인장 강도 45 MPa 아래** · 1.5 µm → 과립은 형성되나 섬유화 영역에 못 듦 · 0.1 µm → 탄성 구간에 머묾 (*"the limited contact area restricts stress transfer and the extremely narrow interparticle spacing confines the deformation space of PTFE chains"*).
- **Fig 3b [판독]**:

| 입경 | 항복 (원) | 섬유화 시작 (네모) | 끝점 | 비고 |
|---|---|---|---|---|
| 20 µm | ε 0.64 · 27.0 MPa | ε 1.70 · 28.8 MPa | ε 3.11 · 58.8 MPa (σ_T 를 ε 2.50 에서 넘음) | 본문의 '10 µm' 수치 (27 @0.6 · 30 @1.8) 와 더 가깝다 🔴 |
| 10 µm | ε 0.575 · 25.1 MPa | ε 1.67 · 26.1 MPa | ε 2.69 · 40.3 MPa | 노트북 10 µm @13 MPa = 38.28 MPa · 2.767 [SI 코드] (근사 일치) |
| 1.5 µm | ε 0.255 · 11.2 MPa | — | ε 0.975 · 13.9 MPa | 노트북 1.5 µm @13 MPa = **8.87 · 0.596**, @20 MPa = 13.43 · 0.943 [SI 코드] 🔴 |
| 0.1 µm | — | — | ε 0.175 · 2.4 MPa | |
| 청색 (섬유화) 구간 시작 | | ε ≈1.67 | | Fig 2b 는 1.13 · Fig 4b 는 ≈1.32 🔴 |

- **SEM (Fig 3d–g)**: 20 µm = 큰 구 사이 막 같은 PTFE · 10 µm = 구 사이 가는 섬유 다발 · 1.5 µm = 작은 구 덩어리 사이 섬유 드묾 · 0.1 µm = 나노 입자 덩어리 + 굵은 줄 몇 가닥 (눈금 2 µm) [정성].
- **응집 강도 (Fig 3c, UTM, 단위 N)**: 0.1 µm *"Failure"* · 1.5 µm ≈**0.045** · 10 µm ≈**0.736** · 20 µm ≈**0.311 N** [판독] = 10 µm 가 20 µm 의 ×2.4 [우리 산술].
- **MIP (Fig 3h, 자립막)**: 공극 **20 µm 37.2 % · 10 µm 32.2 % · 1.5 µm 46.7 %** (0.1 µm 은 취성이라 측정 불가) [인쇄 그림] · 최빈 기공 ≈2.3 · ≈0.86 · ≈0.36 µm [판독].  해석 (p.3): 20 µm 은 막 같은 PTFE 가 미세 기공을 줄이지만 불균일 섬유화로 공극이 높고, 1.5 µm 은 흐름성 저하 · 응력 전달 부족으로 PTFE 가 덩어리에 갇혀 미세 기공 · 공극 증가.
- **탭 밀도 (SI Fig 2, 20 g)**: 20 µm **1.42** · 10 µm **1.38** · 1.5 µm **0.98** · 0.1 µm **0.5 g/cc** [인쇄 표] — *"attributed to the increased specific surface area and particle agglomeration of smaller particles"* (p.3).  SiO₂ 진밀도 미기재 → 충전율 환산 불가.
- **결론 문장 (p.4)**: *"optimal particle size selection, approximately within the 5–10 µm range, is essential"* — ⚠ 5 µm **단봉**은 FEM 그림 · 실험 어디에도 없다 (GPR 학습표에만 5 µm 행).

### 3-4. ★ 쌍봉 SiO₂ (Fig 4 · SI Fig 3 · p.4–5)

- **조합 (13 MPa)**: 10 µm 를 늘 포함 + 5 또는 1.5 µm.  10 + 5 = *"enhanced fibrillation, corresponding to a 7.4% increase, compared with the unimodal distribution, likely due to improved particle packing and efficient stress transfer"* (p.4) — **7.4 % 의 정의 미기재**.  [판독] Fig 4b 끝 변형률 10+5 ≈2.88 / 10+10 ≈2.68 = **×1.075** → '최종 변형률 증가' 로 보인다 [추정]; 노트북 13 MPa 값으로는 변형률 ×1.082 · 응력 ×0.957 (10+5 vs '10' 행) [SI 코드 · 우리 산술].
- 10 + 1.5 = 과립 형성은 되나 섬유화 부족 (SEM Fig 4f) · *"Smaller particles (1.5 µm) appear to concentrate stress unevenly, hindering uniform fiber development"* · *"overly broad PSDs lead to inefficient fibrillation owing to the dominance of smaller particles"* (p.4).
- **Fig 4b [판독]**: 10+10 항복 ε 0.595 · 25.5 / 시작 ε 1.39 · 24.9 / 끝 ε 2.68 · 40.7 MPa · 10+5 항복 ε 0.571 · 23.7 / 시작 ε 1.33 · 24.2 / 끝 ε 2.88 · 41.0 MPa · 10+1.5 항복 ε 0.463 · 18.3 / 시작 ε 1.31 · 19.1 / 끝 ε 1.41 · 19.6 MPa · 청색 구간 시작 ε ≈1.32.
- **응집 강도 (Fig 4c)**: 10+10 ≈**0.734** (= Fig 3c 10 µm 값과 같다 — 같은 시료로 보임) · 10+5 ≈**0.884** (+20 %) · 10+1.5 ≈**0.089 N** [판독 · 우리 산술].
- **MIP (Fig 4g)**: 공극 **10+10 32.2 % · 10+5 29.9 % · 10+1.5 36.1 %** [인쇄 그림] · 최빈 기공 ≈0.91 · ≈0.82 · ≈0.30 µm [판독].
- **탭 밀도 (SI Fig 3)**: 10+10 **1.38** · 10+5 **1.4** · 10+1.5 **1.18 g/cc** (본문 *"increased from 1.18 to 1.40"*, p.5) — 10+5 는 10+10 대비 +1.4 % 뿐, 10+1.5 는 −14.5 % [우리 산술].
- **개념도 (Fig 4h–j)**: 단봉 망 · 중간 크기 입자가 망 안에 들어간 '강화 섬유화' · 작은 입자가 PTFE 둘레에 *"Dispersion force"* 로 뭉친 '섬유화 부족'.
- **[우리 산술] 크기비**: 5/10 = 0.50 · 1.5/10 = **0.15** (삼각 틈 통과 문턱 0.1547 바로 아래 — 문턱 값은 메인 리포 `scripts/make_mixer_deck.py` 주석) · 비교: 메인 믹서 생성기의 소재 실측 지름 AM_P 9 · AM_S 4 · SE 1 µm → AM_S/AM_P **0.444** · SE/AM_P **0.111**.

### 3-5. ★ GPR · 최적화 · 역설계 (Fig 5 · SI Fig 4–5 · SI 표 2 · 식 1 · 5–8 · p.5–6 · p.8–9)

- **GPR (p.5 · p.9)**: 입력 = (입경, PLP) · 출력 = 각 시뮬레이션 응력–변형 곡선의 **최종 P_lm · 최종 변형률** (*"represent the final deformation state of the PTFE"*) · Matérn 커널 · MLE 초모수 · *"The entire dataset was used to train the GPR model without explicit division into training and test sets"* · k-겹 CV **R² 0.989 (단봉) · 0.995 (쌍봉)**.
- **최적화 (p.5)**: *"The optimization objective was to maximize the final strain, subject to the PTFE material constraints (Plm < 45 MPa, strain < 4)"* · 탐색 = 단봉 1.5–10 µm · 쌍봉 3–10 µm · 대표 결과 = 13 MPa 고정 (Fig 5a · 5d) · 10 µm 고정 (5b) · 10 + 5 µm 고정 (5e — 본문은 *"(Fig. 5)"* 로 패널 문자 누락).
- **결과 (p.6)**: 단봉 — *"larger particle sizes require lower shear stress to initiate fibrillation"* · 10 µm ≈**14 MPa** · 쌍봉 — *"the top-three performing secondary particle sizes were 4.5, 5.0, and 6.0 µm"* → 둘째 입경 **4.5–6.0 µm · 13.5–14.7 MPa**.
- **거시 FEM (p.5–6 · p.8)**: COMSOL Fluid Flow + Heat Transfer in Fluids · 반죽기 기하 = *"the experimental equipment used in this study"* (SI Fig 4a, 두 방 ±0.04 m [판독]) · 압출기 = 문헌 (refs 34, 35; SI Fig 4b, 길이 ≈0.25 m [판독]) · 과립 = 비뉴턴 **멱법칙 유체 τ = Kγ̇ⁿ (식 1) — K · n 값 미기재** · 식 (5) 0 = ∇·[−pI + K] + F · (6) ρ∇·μ = 0 · (7) ρCₚμ·∇T + ∇·q = Q + Qₚ + Q_vd · (8) q = −k∇T · 벽 80 °C · 외기 25 °C 대류 (*"validated by our in-situ monitoring"* — 그 자료는 없음) · SI 표 2 = LFP density **3.6 g/cc** · Cₚ **778 J/kg·K** · k **0.27 W/(m·K)** · **80 °C** · *"Shear rates obtained from macroscale simulations were subsequently converted into PLP values"* (환산식 미기재).
- **역설계 결론 (p.6)**: *"A kneader speed of 10 rpm (13.49 MPa) and extruder speed of 700 rpm (13.6 MPa) are determined as the optimal parameters … in both the 10 µm unimodal system and 10–5 µm bimodal system"* → *"we propose the 10 + 5 µm bimodal configuration combined with a kneader speed of 10 rpm"*.  SI Fig 5: *"Bayesian optimization results for the kneader model (MSE: 0.229 MPa) … extruder model (MSE: 0.779 MPa)"*.
- **Fig 5 대 노트북 대조 [판독 · SI 코드]**: 5a (13 MPa · 1.5–10 µm 의 점 9 개) · 5b (10 µm) · 5d (쌍봉 13 MPa) 의 점 = 노트북 학습표 값과 일치 · **5e 의 점 (15–20 MPa: 57.5 · 61.5 · 58.3 · 55.9 · 48.7 · 46.3) = 노트북 쌍봉 '10' 행** (57.684 · 61.593 · 58.407 · 56.02 · 48.679 · 46.309) — 캡션 · 노트북 셀 (`bi_fixed_particle_size = 5.0`) 이 말하는 '5' 행은 16–20 MPa 에서 73.8–82.0 MPa 라 같은 그림이 될 수 없다 🔴 · 5c · 5f 의 45 MPa 경계 ≈14.2 MPa (10 µm) · ≈13.1 MPa (쌍봉 6–10 µm) [판독].
- **[우리 산술 · 노트북 학습표 선형 보간] P_lm = 45 MPa 가 되는 PLP 와 그때 변형률**:

| 단봉 입경 (µm) | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 1.5 |
|---|---|---|---|---|---|---|---|---|---|
| 45 MPa 경계 PLP (MPa) | 14.38 | 15.57 | 16.88 | 17.96 | 19.25 | 20.54 | 22.00 | 23.74 | 25 까지 안 닿음 (최대 21.78) |
| 그때 변형률 | 3.288 | 3.291 | 3.313 | 3.174 | 3.024 | 2.775 | 2.464 | 2.099 | — |
| 13 MPa 의 P_lm (MPa) | 38.28 | 31.94 | 27.19 | 25.07 | 21.59 | 18.90 | 16.57 | 13.81 | 8.87 |

| 쌍봉 둘째 입경 (µm) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| 45 MPa 경계 PLP (MPa) | 15.38 | 14.44 | 13.61 | 13.27 | 13.16 | 13.62 | 13.40 | 13.26 |
| 그때 변형률 | 3.109 | 3.107 | **3.111** | 3.106 | 2.340 | 2.606 | 2.667 | 2.769 |
| 13 MPa 의 P_lm (MPa) | 32.15 | 36.68 | 40.86 | 42.71 | 43.40 | 39.52 | 41.28 | 42.69 |

  → 단봉: 경계 PLP ∝ d^−0.41 (R² 0.966, 3–10 µm) · 13 MPa 의 P_lm ∝ d^0.73 (R² 0.979, 1.5–10 µm) [우리 산술] = 본문 *"larger particle sizes require lower shear stress"* 방향 그대로 · 10 µm 경계 ≈14.4 MPa = 본문 *"approximately 14 MPa"* ✓.
  → 쌍봉: 응력 제약 경계에서의 변형률이 **3, 4, 5, 6 µm 에서 3.106–3.111 로 사실상 같다** (7–10 µm 은 2.34–2.77) → "4.5 · 5.0 · 6.0 µm 상위 셋" 은 이 표로는 갈리지 않고 (3 µm 도 같은 값) 4.5 µm 는 표에 없다 · 4–6 µm 의 경계 PLP 13.3–14.4 MPa ≈ 본문 13.5–14.7 MPa (근사) [우리 산술].

### 3-6. LFP 전극 · 전기화학 (Fig 6 · SI Fig 6–7 · SI Note 1 · p.6–8)

- **SiO₂ → LFP 이전 근거**: *"shares similar morphological characteristics, particularly the spherical shape and fine particle distribution"* (p.6) + SI Fig 6 (10 µm SiO₂ · LFP 를 넣은 PTFE 응력–변형 곡선이 겹침 — 평탄 ≈18–19 MPa · 끝 ≈44 MPa @ ε 2.63 [판독]) · SI Note 1 (PTFE 마찰계수 ≈0.2 → 입자 형상이 섬유화에 중요, refs S1 · S2).
- **설계 → 제조**: *"inverse process design was developed to determine the optimal LFP particle size distribution and kneading conditions, leading to the selection of 5 and 10 µm particles"* (p.7) · 실제 반죽 · 압출 조건 [미확인].
- **미세구조**: PTFE 섬유 망 (Fig 6b, 노란 점선 강조) · 단면 **214 · 280 µm** *"dense and uniform"* (Fig 6c–d) · 10 mAh cm⁻² 막도 균열 없이 라미네이트 (SI Fig 7a–b) · 습식 7 mAh cm⁻² 은 표면 균열 (SI Fig 7c — *"due to binder migration during solvent drying"*).
- **EIS (Fig 6e)**: 등가회로 R_s – (R_ct–W) ∥ CPE_electrode · **R_ct 25.84 · 33.42 Ω** (7 · 10 mAh cm⁻², 면적 정규화 없음 · 전극 지름 [미확인]) [인쇄] · [판독] 고주파 절편 ≈0.5 · ≈2.4 Ω · 반원 끝 ≈27.7 · ≈35.8 Ω.  해석: *"Although thicker electrodes generally exhibit substantially increased Rct owing to extended ion diffusion pathways, the observed increase is small"* (p.8) · [우리 산술] R_ct 비 **1.29** ≈ 두께비 **1.31** (로딩비 1.43–1.60).
- **첫 사이클 (Fig 6f)**: *"nominal capacity plateau near 3.43 V and low hysteresis ΔV"* (p.8; 문헌 슬러리 로딩 증가 시 ΔV 최대 0.22 V, ref 40) · [판독] 충전 ≈3.51 · 방전 ≈3.37 V (ΔV ≈0.14 V) · 방전 끝 ≈**159.7 · ≈158.2 mAh g⁻¹** (2.5 V).
- **사이클 (Fig 6g)**: *"both cathodes maintained over 99% Coulombic efficiency and stable capacity over 50 cycles. The cathode with an areal capacity of 10 mAh cm−2 exhibited no degradation"* (p.8) ↔ [판독] 7 mAh cm⁻² ≈7.08 평탄 · **10 mAh cm⁻² ≈10.14 (1) → ≈9.24 (50) mAh cm⁻² = −8.9 %** (≈25 사이클부터 내려감) 🔴.

### 3-7. ★ SI 코드 (Sup2 노트북) — 무엇을 계산하나 [SI 코드]

- **형식**: Jupyter nbformat 4.2 · Python 3.13.2 · 14 셀 (마크다운 6 · 코드 8) · 라이브러리 = scikit-learn (GaussianProcessRegressor · Matern · ConstantKernel · WhiteKernel · RBF · KFold · cross_val_score · 오차 지표) · `bayes_opt` (BayesianOptimization) · numpy · matplotlib.  **FEM 코드 · COMSOL 모델은 없다** — FEM 결과는 하드코딩 표다.  ⛔ 이 카드는 노트북을 실행 · import · 변환하지 않았다 (JSON 텍스트만 읽음).
- **셀 지도**:

| 셀 | 실행 번호 | 내용 | 대응 그림 |
|---|---|---|---|
| 0–1 | — | 마크다운 "## Unimodal" · 빈 셀 | |
| 2 | 2 | 단봉 학습표 + GPR 둘 (응력 · 변형률) + BO + 크기별 격자 탐색 · 출력 텍스트 저장 | |
| 3 | 3 | 5-겹 CV (응력 모형) | 본문 R² 0.989 |
| 4 | 4 | GPR 평균 ± 1.96σ: 13 MPa 고정 (1.5–10 µm) · 10 µm 고정 (xlim 0–21) · σ_T = 45 점선 · PNG 저장 | Fig 5a · 5b |
| 5 | **35** | 50 × 50 격자 등고 (응력 GnBu 0–45, > 45 투명 · 변형률 등고선 linspace(0, 4, 10) "%.2f") | Fig 5c |
| 6 | — | 마크다운 "## Bimodal" | |
| 7 | **24** | 쌍봉 학습표 + GPR + BO + 크기별 루프 | |
| 8 | 25 | 5-겹 CV (응력 모형) | 본문 R² 0.995 |
| 9 | **6** | 쌍봉 GPR 그림: 13 MPa 고정 (3–10 µm) · **5.0 µm 고정 · ylim(0, 60)** | Fig 5d · 5e (5e 는 불일치 🔴) |
| 10 | 34 | 쌍봉 등고 (3–10 µm × 0.1–20 MPa) | Fig 5f |
| 11–12 | — | 빈 셀 · "## Practical process optimization" | |
| 13 | **미실행** | 반죽기 · 압출기 rpm → 전단 응력 표의 1차원 GPR (1.0·RBF(50) + White(1.0)) · 그림만 (MSE 계산 없음) | SI Fig 5 |

- **학습표**: 단봉 = 입경 [10, 9, 8, 7, 6, 5, 4, 3, 1.5] µm × PLP [0.1, 0.3, 0.5, 0.7, 0.9, 1, 2, …, 25] (30) = **270 쌍** · 쌍봉 = 둘째 입경 [3, 4, …, 10] × PLP [0.1 … 20] (25) = **200 쌍** (출력 "X_train shape: (270, 2)" · "(200, 2)").  행마다 PLP 에 대해 변형률은 단조 증가 · 응력은 큰 입자 행에서 끝에 감소 (예: 단봉 10 µm 88.88 @21 → 83.99 @25 MPa · 쌍봉 '10' 행 61.59 @16 → 46.31 @20 MPa).  쌍봉 '10' 행 (13 MPa 42.69 MPa · 2.674) 은 단봉 10 µm 행 (38.28 · 2.767) 과 다르다 = 두 모형의 기하가 다르다 [우리 산술].
- **GPR**: `C(1.0, (1e-3, 1e5)) * Matern(length_scale=5.0, nu=1.0) + WhiteKernel(noise_level=1e-5)` · `n_restarts_optimizer=10` · 씨앗 50 (단봉) / 42 (쌍봉) · **학습 R² 1.000 · MSE 0.000** (보간) · 5-겹 CV (shuffle, 응력 모형만): 단봉 0.9841 · 0.9925 · 0.9907 · 0.9939 · 0.9860 → **평균 0.98945** · 쌍봉 0.9903 · 0.9952 · 0.9961 · 0.9990 · 0.9929 → **평균 0.99470** (= 본문 0.989 · 0.995) · **변형률 모형은 검증하지 않았다**.
- **단봉 목적함수**: `particle_size + pressure` − 100·(σ̂ − 45)₊ − 100·(ε̂ − 4)₊ (본문의 '최종 변형률 최대화' 가 아니다) · 범위 입경 **6–10 µm** (본문 1.5–10) · PLP 0.1–25 · 초기 10 + 반복 30 → 최적 **(6.1036 µm, 17.2507 MPa)** · 목적 23.3543 · σ̂ 36.55 MPa · ε̂ 2.595 · 마지막 줄 *"The particle size with the highest strain is: 6.10"* (목적이 변형률이 아니므로 이름표가 틀림) — 이 결과는 논문에 안 쓰였다.
- **단봉 크기별 '최적 PLP'** (PLP 0.1–20 을 300 점 격자, σ̂ < 45 · ε̂ < 4 안에서 목적 최대 = 경계 PLP): 1.5 · 3 · 4 · 5 µm → **20.0 (격자 상한)** · 6 → 19.20 · 7 → 17.94 · 8 → 16.87 · 9 → 15.61 · **10 → 14.41 MPa (σ̂ 44.99 · ε̂ 3.30)**.
- **쌍봉 목적함수**: `exp(−(σ̂ − 45)²/10)` (ε̂ ≥ 4 이면 −1e5) = "응력을 45 MPa 에 붙여라" (역시 변형률 최대화 아님) · 범위 입경 **6–20 µm** (학습 3–10 → 10 µm 위는 외삽) · PLP 0.1–25 (학습 ≤ 20) · BO 표 최고 0.6937 @ (6.058 µm, 13.04 MPa) · 크기별 루프 (학습 PLP 격자에서): 3 → 15 · 4 → 14 · 5–10 → 13 MPa · 목적 7 µm **0.774** > 6 0.592 > 10 0.587 > 3 0.532 > 4 0.385 > 9 0.251 > 5 **0.180** > 8 0.050 — 본문 "상위 셋 4.5 · 5.0 · 6.0 µm · 13.5–14.7 MPa" 는 **저장된 출력 어디에도 없다**.
- **거시 표 (셀 13)**: 압출기 rpm [350, 500, 700, 1000, 1200] → 전단 응력 [9.2, 10.0, 13.6, 17.4, 19.8] · 반죽기 rpm [5, 10, 15, 20] → [8.35, 13.49, 17.86, 21.80] (단위 표기 없음 — 본문은 MPa) = SI Fig 5 의 점 · 본문의 "10 rpm (13.49 MPa) · 700 rpm (13.6 MPa)" = **시뮬레이션한 격자점 그대로** (연속 최적화 결과가 아니다).
- **실행 순서**: 저장된 실행 번호 2 · 3 · 4 · **35** · 24 · 25 · **6** · 34 · 미실행 — 셀 9 (쌍봉 그림, 6) 이 셀 7 (쌍봉 학습, 24) 보다 먼저 돌았다 → 저장된 그림 출력과 저장된 코드 · 데이터가 같은 상태라는 보장이 없다 (Fig 5e 불일치의 한 설명 후보 [추정]).  주석도 낡았다: "(particle_size, pressure) 2차원 조합 150개" (실제 270) · "# 5개" (실제 9) · "임의 공식 + 노이즈로 생성합니다. 실제로는 실측 데이터를 길이 150에 맞춰 넣으시면 됩니다" (실제 배열은 하드코딩) · "9 × 25 = 225" (실제 8 × 25 = 200) · `return` 뒤에 닿지 않는 `return -bi_stress_diff`.

---

## 4. ★ 방법 — 측정 사슬 · 시뮬레이션 · 입자 처리

### 4-1. 측정 사슬
SiO₂ (단봉 4 · 쌍봉 3) 분말 → PSD (LA-950) · 탭 밀도 (20 g 실린더) → 90 : 5 : 5 혼합 (PLS-300) → 섬유화 (압출 NEP-0.5K + 분쇄) → 롤 프레스 자립막 (KRM-100D3) → (i) SEM (섬유 vs 막) (ii) UTM 응집 강도 (N) (iii) MIP (공극 · 기공 분포) — 같은 공정으로 LFP (5 + 10 µm) 후막 7 · 10 mAh cm⁻² → 캘린더 → 탄소 코팅 Al 라미네이트 → 사진 (균열) · 단면 SEM (두께) → CR2032 반쪽셀 (액체) → EIS (R_ct) · 첫 사이클 · 0.1 C 50 사이클.  FEM · GPR 은 이 사슬과 **같은 시료 · 같은 공정 조건으로 이어져 있지 않다** (PLP 를 잰 적 없음).

### 4-2. 시뮬레이션 요약 (세부는 §3-2 · §3-5 · §3-7)
- **미시 FEM**: COMSOL · 2D 로 보임 [판독] · AM 원 2 (쌍봉 4) + PTFE 원 1 · PTFE = Arruda–Boyce (+ 표 S1 가지 모수) · 80 °C · PLP 0.1–25 MPa 경계 하중 (방향 = 엇갈린 전단) · 출력 = 최종 P_lm · 최종 변형률 · 섬유화 / 막 = 사후 구간.
- **대리 모형**: 2 입력 GPR 둘 (응력 · 변형률) · 270 · 200 점 · 5-겹 CV · 크기별 최적 = 제약 경계 격자 탐색 (BO 는 부수 출력).
- **거시 FEM**: COMSOL 유동 + 열 · 반죽기 (자체 장비 기하) · 압출기 (문헌 기하) · 멱법칙 유체 (K · n 미기재) · 4–5 rpm 점 → 1차원 GPR.
- **입자 스케일 다체 모형 (DEM · MPM · 망)**: 없음.  본문의 *"particle dynamics"* 는 2–4 개 원의 정적 연속체 FEM 을 가리킨다 (입자 운동 · 충돌 · 충전 없음).

### 4-3. ★ 입자 처리 (우리 축 언어로)
- **실험 쪽**: SiO₂ · LFP = 형상이 안 바뀌는 강체에 가까운 구 (LFP 는 거친 응집 구) · PTFE = 전단으로 섬유 · 막이 되는 **유일한 대변형 상** · CB = 언급만.
- **FEM 쪽**: AM 원 = 압력을 거는 단단한 몸 (재질 무감 — SI Fig 6) · PTFE 원 = 초탄성 (+ 점성 가지) 연속체 — **섬유 · 막 · 파단 · 접촉 해제는 표현되지 않는다** (형상 변화 = 늘어난 연속체) · **다입자 충전 · 힘 사슬 · 입경 분포는 없다** (쌍봉 = 큰 둘 + 작은 둘 고정 배치).
- **우리 DEM 과의 대응** [추정]: 강체 구 · Hertz/hysteresis · Auerbach 파괴 판정 · SJKR 점착 (믹서) — PTFE 섬유 · 막 · 바인더 다리는 표현되지 않는다 (믹서 DEM 은 PTFE 를 뺀 3 상).  우리 MPM 은 SE J2 한 상 — 바인더 상 없음.

### 4-4. 기법 미니 용어집
- **PLP (particle-loaded pressure)**: 이 논문 용어 — 각 AM 원이 PTFE 에 거는 압력 (경계 하중).  본문은 '전단 응력 (shear stress)' 과 섞어 쓴다.
- **P_lm**: 본문이 2nd Piola–Kirchhoff 응력이라 부르는 출력 (어느 성분 · 어느 점인지 미기재).  2nd PK 는 기준 형상 기준이라 큰 변형에서 공칭 · 참 응력과 크게 다르다 (단축 비압축: P = λS · σ = λ²S).
- **Arruda–Boyce 8사슬 모형**: 고분자 사슬 망을 정육면체 대각선 8 사슬로 본 초탄성 모형 — 역 Langevin 함수로 사슬 잠금 (locking stretch λ_L) 을 표현.  초탄성 = 가역 (소성 · 손상 없음).
- **GPR (Gaussian process regression)**: 커널로 정한 공분산의 가우스 과정으로 표를 보간 — 학습점에서 거의 정확히 지나간다 (학습 R² 1.000).
- **Bayesian optimization**: GPR 같은 대리 모형 위에서 획득 함수로 다음 시험점을 고르는 최적화 — 이 논문 결과는 사실상 격자 탐색 (§3-7).
- **멱법칙 유체**: τ = Kγ̇ⁿ (K 일관성 지수 · n 흐름 지수) — n < 1 이면 전단 담화.
- **MIP**: 수은 압입 기공 측정 — 압력 → Washburn 지름 · 누적 부피 → 공극.
- **탭 밀도**: 정해진 두드림 뒤의 분말 겉보기 밀도 (응집 · 흐름성 지표).

---

## 5. Figure set ★ (크롭 19 장 = `litdb/figures/kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 건식 공정 개념도 (건식 혼합 → 과립 형성 (스크루) → 캘린더 · 라미네이트 → 섬유 망 전극 vs 균열 전극) (b) 다중 척도 흐름 (FEM → GPR → BO → 역설계 → 공정 처방) | 개념도 (정성) |
| 2 | (a) AM–PTFE–AM 세 원 · 엇갈린 PLP (b) 응력–변형 곡선 네 구간 · ε 1.13 · 16.8 MPa 눈금 · 끝 ≈29 MPa | ★ 섬유화 '창' 의 정의 (사후 구간) |
| 3 | (a) SiO₂ PSD (b) FEM 응력–변형 (20 · 10 · 1.5 · 0.1 µm, 13 MPa) (c) 응집 강도 (d–g) SEM (h) MIP 37.2 · 32.2 · 46.7 % (i–k) 막 · 섬유 · 부족 개념도 | ★ 입경 → PTFE 형태 실례 · 🔴 본문 수치 · 1.5 µm 끝점 |
| 4 | (a) 쌍봉 PSD (b) FEM (10+10 · 10+5 · 10+1.5) (c) 응집 강도 (d–f) SEM (g) MIP 32.2 · 29.9 · 36.1 % (h–j) 개념도 ('Dispersion force') | ★ 미세 분획 응집 실례 (SE 1 µm 대응, §7-5) |
| 5 | (a)(b)(d)(e) GPR 평균 ± 1.96σ (c)(f) 응력 색 + 변형률 등고 (g) 반죽기 · (h) 압출기 FEM 전단 응력 (±15 MPa) + 쌍봉 미시 모형 삽화 | ★ 공정 강도 → 입자 하중 사슬 · 🔴 5e |
| 6 | (a) LFP 5 · 10 µm (b) PTFE 섬유 망 (c–d) 단면 214 · 280 µm (e) Nyquist R_ct (f) 첫 사이클 (g) 50 사이클 | LFP 건식 후막 기준점 · 🔴 10 mAh 감쇠 |
| 식 1 | 멱법칙 τ = Kγ̇ⁿ (K · n 없음) | 재현 불가 표지 |
| 식 2–4 | 운동량 · 변형 구배 · 변형 에너지 (인쇄 꼴 · 오식 후보) | 구성식 확인 |
| 식 5–8 | 유동 · 연속 · 열 · Fourier | 거시 모형 확인 |
| SI S1 | 0.1 · 1.5 · 10 · 20 µm FEM 변형장 (2D, ×10⁷ N/m²) | ★ 기하 · PTFE 크기 단서 |
| SI S2 · S3 | 탭 밀도 사진 + 표 (단봉 · 쌍봉) | ★ 분말 응집 앵커 형식 (§7-5) |
| SI S4 | 반죽기 · 압출기 기하 (m) | 거시 기하 |
| SI S5 | 반죽기 · 압출기 rpm → 전단 응력 1차원 GPR ('MSE 0.229 · 0.779 MPa') | 🔴 BO 아님 · 미실행 셀 |
| SI S6 | 10 µm SiO₂ vs LFP 응력–변형 (완전 겹침) | 🔴 구성상 당연한 겹침 |
| SI S7 | 7 · 10 mAh cm⁻² 건식 (44.06 · 63.22 mg cm⁻²) · 습식 7 (43.42, 균열) 사진 | 🔴 로딩 불일치 |
| 표 S1 | PTFE 모형 모수 12 줄 | ★ 바인더 구성식 모수 (출처 주의) |
| 표 S2 | 거시 모형 모수 4 줄 (LFP 밀도 · Cₚ · k · 80 °C) | K · n 없음 |
| Note S1 | SiO₂ ↔ LFP 이전 논리 ('Supplementary Fig. 7' 오인용) | 🔴 |

## 6. Post-processing ★
- **무엇을**: FEM 응력–변형 곡선에서 '최종' P_lm · 변형률 뽑기 · 항복 (원) · 섬유화 시작 (네모) 표지 (기준 미기재) · GPR 적합 · 5-겹 CV · 제약 경계 격자 탐색 · 등고 지도 · 거시 FEM 전단 응력 → (미기재 환산) → PLP · SEM 정성 · UTM 하중 막대 · MIP 미분 침투 곡선 + 공극 · 탭 밀도 · Nyquist 등가회로 적합 · 전압 곡선 · 사이클.
- **안 한 것**: 섬유 지름 · 길이 통계 · 섬유화 정도의 정량 지표 (SEM 면적 · 비표면적 · DSC 결정화도 등) · 응집 강도 시험 형상 · 반복 · 오차 · 실물 공정의 토크 · 온도 · 응력 측정 · 전극 공극 (LFP) · 전기화학 대조군 · 셀 반복 · 면적 정규화 R_ct · 메시 수렴 · 하중 속도 의존 · 변형률 모형 CV · 입경 한 개 빼기 검증.
- **우리 후처리 (이 카드)**: 노트북 JSON 을 텍스트로만 읽어 학습표 · 출력 재확인 · 학습표 선형 보간으로 45 MPa 경계 PLP · 변형률 · 멱지수 · 로딩 · 밀도 · 용량 정합 · PTFE E · ν · Arruda–Boyce 초기 전단 계수 · 그림 판독 (digitized.csv, 보정 검산 머리) · Fig 5e ↔ 학습표 행 대조.

---

## 7. ★ 우리 작업에 주는 것 (→ `our_dem_baseline.md` 는 정본 브랜치에서 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md · 원장 `docs/reviews/claims.json` · `docs/mixer_paper_pipeline_draft_20261013.md` 의 해당 줄을 병기)

### 7-1. 비교표 — 같은 이름 · 다른 양 주의

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 입자가 바인더에 거는 하중 | **PLP** = AM 원 경계의 압력 한 값 (0.1–25 MPa) · 실물에서 잰 적 없음 · rpm → 전단 응력 → PLP 환산식 미기재 | DEM 접촉력 **분포** (힘 사슬) · 상별 Love–Weber 입자 응력 열 (메인 CLAUDE.md J20-s ④b · 값은 접촉 단계 재실행 뒤) | 그들은 한 값, 우리는 분포 — 같은 양 아님.  DEM 이 'PLP 분포' 를 줄 수 있다 (§8-1) |
| PTFE 형태 | 섬유 (fibril) vs 막 (film-like) 가 입경 · PLP 에 달림 (FEM 사후 구간 + SEM 정성) | STEP3 `ptfe_stamp = centerline` (CL-60 본문 규약) · `PTFE_D = 0.25 µm` 앵커 (CL-66) · 형태 = 공정 무관 고정 규약 · 표면 막 (sub-voxel 코팅) 은 복셀이 못 봄 (CL-49: 부피 점유 −25 % 뿐) | 우리 모델은 **입경 → PTFE 형태** 의존을 낼 수 없다 (F 목록) |
| 바인더 구성식 | Arruda–Boyce 8사슬 + 가지 모수 (μ 200 MPa · K 2.72 GPa · λ_L 5.6 · 흐름 저항 9.0 / 4.8 MPa · 80 °C) → E ≈0.59 GPa · ν ≈0.46 [우리 산술] | MPM = SE J2 한 상 (E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa) · 믹서 DEM 생산 덱 = AM_P · AM_S · SE 3 상 (PTFE 없음, 계획 §6-3) · STEP3 = 섬유 씨더 + centerline 절연 스탬프 (CL-60) | 바인더 대변형 상이 우리 어느 모델에도 없다 |
| 입경 효과의 원천 | 13 MPa 에서 P_lm ∝ d^0.73 · 경계 PLP ∝ d^−0.41 [우리 산술] — 모형 PTFE 크기 · 하중 정의 미기재 | **CL-64**: 길이척도 없는 탄성 모델은 입경 효과를 낼 수 없다 (Cronk 2026 FEM: 두 입경 σ̄_vM 0.8 % 차) | 이 논문의 입경 효과도 같은 검사를 받아야 한다 (§7-2) |
| 쌍봉 크기비 | 10 + 5 µm (0.5) '최적' · 10 + 1.5 µm (0.15) '섬유화 부족 · 응집' | 믹서 소재 실측 지름 AM_P 9 · AM_S 4 · SE 1 µm (`make_mixer_deck.py`) → 0.444 · 0.111 | AM 쌍봉 비는 그들의 '최적' 근처, SE 미세 분획은 그들의 '나쁨' 영역보다 더 작다 [추정 — SiO₂ 대리 · PTFE 5 wt%] |
| 공극 | MIP 자립막 29.9–46.7 % (SiO₂ 90 : CB 5 : PTFE 5 · 캘린더 압력 미기재) | 압밀 DEM 정확 union 공극 — 사양 다섯 조성 중 최저 16.49 % (P:S 7:3, 믹서 계획 §1-1) | 다른 계 · 다른 공정 · 다른 측정 → 수치 비교 금지 |
| 수송 | σ_ion · σ_e · κ 측정 0 · R_ct (Ω, 면적 미정규화) 만 | 접촉망 σ 삼중항 · STEP3 복셀 σ (CONTACT_FREE 가지, CL-81) | 대조할 수송 수치 없음 |

### 7-2. DEM + MPM (frame[5] · CL-64)
- **"입경 효과는 어디서 오나" — CL-64 검사**.  Arruda–Boyce 초탄성에는 재료 길이척도가 없다: 기하가 상사이고 경계 하중이 같은 압력이면 응력장은 크기에 무관해야 한다 (Cronk 2026 FEM 이 두 입경에서 거의 같은 응력을 낸 것과 같은 이유 — CL-64).  그런데 노트북 학습표는 같은 13 MPa 에서 P_lm 이 1.5 → 10 µm 사이 ×4.3 (∝ d^0.73) 커진다 [우리 산술] → 이 입경 효과는 (a) **PTFE 원 크기를 고정 (또는 따로 정하고) AM 만 키운 기하** (= AM : PTFE 크기비 효과) 이거나 (b) **'압력 × AM 표면 = 힘' 이 AM 크기와 함께 커지는 하중 정의** 에서 온다 [추정] — SI Fig 1a 는 0.1 µm AM 두 개가 ≈1 µm PTFE 를 누르는 기하라 (a) · (b) 와 맞는 그림이다 [판독].  어느 쪽이든 **'최적 입경 ≈10 µm' 는 모형 PTFE 크기 (미기재) 에 상대적인 값** 이다.  표 S1 의 점성 가지가 실제로 쓰였다면 하중 속도 · 시간도 척도로 들어온다 (미기재).
- **DEM 이 줄 수 있는 것**: 그들은 PLP 를 한 값으로 둔다.  실제 쌍봉 충전층에서는 같은 거시 응력이라도 입자별 접촉력이 넓게 퍼지고 (힘 사슬) 큰 입자가 강한 사슬을 진다 — 평균장으로는 접촉력 ∝ σ·d² [추정].  그들의 "큰 입자 → 응력 집중 → 막" 방향과 같다.  우리 압밀 DEM 의 상별 Love–Weber 입자 응력 (J20-s ④b) · 접촉 덤프가 **'상별 PLP 분포'** 를 바로 줄 수 있다 → 그 분포를 그들의 '섬유화 창' 같은 바인더 기준과 겹치면 "어느 크기 분획의 접촉이 막 / 섬유 / 부족 영역에 드는가" 를 분포로 말할 수 있다 [추정 · 후보 과제].
- **MPM**: 우리 MPM 은 SE J2 한 상 — 바인더 (PTFE) 상 · 섬유화 · 파단 없음.  그들의 FEM 은 변형률 3–6 (학습표 최대 5.91) 의 대변형을 라그랑주 메시로 다룬다 (재메시 · 메시 수렴 언급 없음 [미확인]) — MLS-MPM 은 메시 엉킴이 없어 이런 대변형 바인더에 원리적으로 맞는 도구다 [추정], 단 구성식 (AB + 점성 가지) 과 '섬유화' 판정을 새로 정의해야 한다.
- **해상도 질문**: SI Fig 1c–d 의 PTFE 띠는 두께 ≲1 µm 로 입자 (10–20 µm) 보다 한 자릿수 얇다 [판독] — 메시 크기 · 수렴 시험 미기재.  우리 MPM 의 `d_h/dx ≳ 3.5` 규칙 (좁은 채널이 미해상이면 응력을 과소평가, 메인 CLAUDE.md 08-06 절) 과 같은 질문을 던져야 하는 그림이다 [추정].

### 7-3. STEP3 복셀 · 접촉망 σ
- **수송 측정이 없다** (σ_ion · σ_e · κ 0) → 우리 접촉망 · 복셀 σ 와 대조할 숫자가 없다.
- **PTFE 막 (film-like) = AM 표면을 덮는 sub-voxel 층** — 우리 복셀 스탬프가 못 보는 표면 차단 (CL-49 — 부피 점유로는 −25 % 뿐, 문헌의 수천 배 붕괴는 표면 코팅 효과).  이 논문은 "막이 생기는 조건 = 국소 응력 > 인장 강도 (큰 입자)" 를 FEM 문장으로 준다 — 실험으로는 SEM 정성뿐이고 수송 결과 없음.  ⇒ 앞으로 PTFE 형태 모듈을 만든다면 '입경 · 국소 응력 → 섬유 / 막' 규칙의 후보 문헌 (검증 전) [추정].
- **R_ct 가 두께에 비례 (1.29 vs 1.31)** [우리 산술] — 활물질은 1.4–1.6 배 늘었는데 '전하전달' 저항이 두께만큼 늘었다면 후막 기공 이온 저항이 Randles 꼴 반원에 섞였을 가능성 [추정] (반쪽셀 Li 상대 전극 몫도 분리 불가).  우리 `scripts/eis_drt_ica.py` (Randles + Warburg 를 STEP3/STEP4 물리에서 유도) 의 R_ct 를 두께가 다른 전극 사이에서 비교할 때 TLM 이 필요하다는 외부 사례.
- **접촉망 대응**: 그들의 2-입자 FEM 셀은 우리 접촉망의 '한 간선' (AM–바인더–AM 다리) 을 연속체로 푼 것과 같은 자리 — 그러나 그 다리의 전자 · 이온 저항은 다루지 않는다.

### 7-4. 건식 PTFE 작업 · 팔로우 랩 공정 기준점
- **조성**: 90 : 5 : 5 (PTFE **5 wt%** · Super P 5 wt%) — 우리 믹서 조성 PTFE 1 wt% (`make_mixer_deck.py` WT) · SDCP 캠페인 0.5–1 wt% 의 5–10 배.  형제 카드 (`kim2026_pregranulation_…` 2.2 wt% · `lee2026_li_underlayer_…` 3 wt%) 보다도 높다.
- **LFP 후막**: 7 · 10 mAh cm⁻² · 214 · 280 µm · 목표 2.3 g/cc · 0.1 C 반쪽셀 · R_ct 25.84 · 33.42 Ω — 같은 그룹 계열 건식 LFP (ref 40 Kwon 2024) 와 묶어 볼 기준점.
- **장비**: KMTECH PLS-300 (혼합 · 분쇄) · NEP-0.5K (압출) · KRM-100D3 (롤) — 조건 수치 0.  형제 카드 `kim2026_pregranulation_…` 은 Thinky 유성 혼합기 2000 rpm × 2 min × 5 (PGP 단계) 만 수치가 있다 → 팔로우 랩 공정 조건 표는 아직 비어 있다.
- **PTFE 등급**: F-106 (Daikin) 명시 (형제 카드 `lee2026_li_underlayer_…` 와 같은 등급 · `kim2026_pregranulation_…` 은 Solvay) — 그러나 섬유 지름 · 길이 측정 없음 → CL-66 (`PTFE_D 0.25 µm`) · CL-67 (씨더 끝점 거리 중앙 4.13 µm) 의 앵커로 쓸 수 없다.
- **표 S1 모수 (PTFE 80 °C)**: 출처 = 데이터시트 + ref 41 (마찰 논문) — 원문 확인 전에는 우리 입력으로 옮기지 않는다 (규율 ⑥).

### 7-5. ★ 믹서 DEM 캠페인 · 믹서 논문 계획 (메인 `docs/mixer_paper_pipeline_draft_20261013.md` V1 · V2 · V3) 과 이종기술 논지
- **위치**: 우리 믹서 DEM = 3 상 (AM_P 9 · AM_S 4 · SE 1 µm) 저-G 드럼 (Fr 0.0827) · PTFE · VGCF 는 모델에서 먼저 뺐다 (계획 §6-3 · G12 "PTFE 섬유화 · 캘린더링 없음 · parcel 은 깨지지 않는다") → 이 논문의 기전 (PTFE 섬유화) 은 **우리 믹서 모델 밖**이다.
- **V1 (코팅 상태 · 같은 SE 총량)**: n/a — SE · 코팅 없음.  그들 FEM 은 입자 재질에 무감 (SI Fig 6) → 코팅으로 표면 재질이 바뀌어도 그들 틀로는 차이가 안 난다 [추정].  V1 의 건식 극판 실험 (PTFE 포함) 에서는 코팅 NCM 의 겉보기 입경 · 표면 거칠기 변화가 PTFE 섬유화를 함께 바꿀 수 있다 (교락 후보 [추정]) → 계획에 있는 **"섬유화 전 분말 EDS"** 가 맞는 측정점이다.
- **V2 (혼합 시간 · 강도 고정)**: 이 논문은 **시간이 아니라 강도** (rpm → 전단 응력) 를 다룬다; 서론의 *"insufficient kneading time … excessive kneading time causes over-deformation, altering the fibrous structure into a film-like morphology"* (p.1, ref 16) 는 이 논문 데이터가 아니다.  → 계획 D10 (강도 = Bo/G 한 수준) 에 **'공정 강도 → 입자 하중' 사상의 선례** 로만 쓰고 수치 (13.49 MPa) 는 옮기지 않는다 (K · n 미기재 · 환산식 미기재).  PTFE 가 있는 실험이면 시간에 따라 섬유화도 진행 → SE 분산과 섬유화가 섞인다 → 섬유화 전 분말에서 V2 를 재라는 계획 방향과 맞다 [추정].
- **V3 (SE 함량)**: n/a — 단 **미세 분획이 많아지면 PTFE 섬유화 · 충전이 나빠지는 방향** (10 + 1.5 µm) [인쇄 · SiO₂ 대리] → V3 의 건식 극판 실험에서 SE (1 µm) 함량이 PTFE 상태를 함께 바꿀 수 있다 (교락 후보 [추정]).
- **P1 (비코팅 SE–SE 응집 생존) 과의 관계**: 10 + 1.5 µm SiO₂ 의 미세 분획 응집 (탭 밀도 −14.5 % · MIP 공극 +3.9 %p · 섬유화 부족 · Fig 4j *"Dispersion force"* 개념도) 은 "미세 입자 응집이 건식 공정에서 남는다" 의 **정성 실례** — 그러나 SiO₂ (LPSCl 아님) · PTFE 5 wt% 존재 · 혼합 조건 미기재 · 응집을 정량하지 않음 → 논지 근거로 인용하지 않는다 (배경 수준).  이종기술 논지 (메인 `docs/hetero_thesis.md` 비준 블록) 의 '하지 않는 말' 을 넘지 않게 쓸 것.
- **D3 앵커 (분말 응집 수준)**: SiO₂ 4 입경 + 3 쌍봉 탭 밀도 (20 g, 실린더) = 계획 D3 (안식각 · Hausner 비) 와 같은 종류의 '응집 보정' 자료 형식.  SiO₂ 진밀도 · 두드림 횟수 미기재 → 충전율 · Hausner 비 환산 불가.

### 7-6. 패킹 / Furnas (D 축)
- **[우리 산술 · 인쇄 값]** 10 + 5 (크기비 0.5): 탭 밀도 **+1.4 %** · 막 공극 **−2.3 %p** / 10 + 1.5 (크기비 0.15): 탭 밀도 **−14.5 %** · 막 공극 **+3.9 %p** (둘 다 10 + 10 대비).  강체 구 기하 (Furnas · de Larrard · McGeary) 는 크기비가 작을수록 틈 채움 이득이 커지는 방향을 주는데 실측은 반대 — **미세 분획 응집이 기하 이득을 뒤집은 사례** [추정 · SiO₂ · 섞는 비율 미기재].  우리 압밀 DEM (점착 없음) 은 이 역전을 낼 수 없다 (D 축 = 기하 소유).
- 크기비 0.15 는 삼각 틈 통과 문턱 0.1547 바로 아래 (체질 영역 입구) — 메인 믹서 생성기의 SE/AM_P 0.111 도 같은 영역.

### 7-7. ML 대리 모형 · 설계 폐루프
- 그들의 GPR 은 2 입력 · 촘촘한 격자 보간이다.  무작위 5-겹 CV 0.989 / 0.995 는 같은 입경 곡선 안 인접 PLP 사이 보간 성능이지 **입경 사이 일반화 시험이 아니다** (한 입경 빼기 검증 없음) · 변형률 모형은 검증 0.  → 우리 `scripts/ml_design_structure.py` 의 중첩 CV · leverage 외삽 관문 (메인 CLAUDE.md 2026-08-03 절) 과 대비되는 외부 사례.
- 최적화 결과는 실제로 **격자 탐색** (크기별 제약 경계) 이고 BO 결과는 쓰이지 않았다 — 싼 2-D 대리 모형 위에서는 격자가 정답이다.  우리 `scripts/ml_design_loop.py` (Sobol 검증 · BO) 를 쓸 때도 "BO 를 썼다" 보다 "탐색 공간 · 격자 · 제약 경계" 를 보고하는 편이 정직하다.

### 7-8. frame[4] · frame[5]
- **frame[5]**: 이 논문은 '역학' 반쪽 중 **바인더 대변형 (연속체)** 과 **거시 유동 (추정 응력)** 을 가졌고, '충전 · 접촉망' 반쪽 (실제 다입자 충전 · 접촉력 분포 · 수송) 이 비어 있다 — 그 빈칸이 DEM (힘 사슬 · 접촉망 σ) 의 영역.
- **frame[4]**: FEM 은 실험 응력–변형 한 점 (16.4 MPa, 곡선 미제시) 에, GPR 은 FEM 에, 거시 모형은 장비 기하에 맞췄다 — **실물 공정 측정 (토크 · 온도 · 응력 · 섬유화 정도) 과의 독립 대조가 0** 이라 '역설계' 는 교차검증되지 않았다.  SiO₂ 실험은 입경 순서의 **정성 일치** 까지만 준다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 'PLP' 는 DEM 이 분포로 줄 수 있는 양이다.**
- 논문: 바인더 섬유화를 정하는 입력을 '입자가 거는 압력 한 값' 으로 두고, 그 값을 거시 유동 FEM 의 전단 응력에서 (미기재 환산으로) 가져온다.
- 뜻: 실제 충전층의 입자별 하중은 분포이고 크기 분획마다 다르다 — frame[5] 상 DEM 고유 몫.
- 할 일: 우리 압밀 DEM (ps45 · real_14) 의 상별 Love–Weber 응력 · 접촉 덤프로 '상별 접촉 압력 분포' 를 뽑아 바인더 기준 (예: σ_T 45 MPa 같은 문턱) 과 겹치는 후보 과제를 적는다 (1저자 판단 · 바인더 기준값의 출처 확인이 먼저).

**8-2. 입경 효과는 모형 PTFE 크기에 상대적이다 (CL-64 부류).**
- 논문: 초탄성 FEM 이 같은 PLP 에서 P_lm ∝ d^0.73 을 낸다 · PTFE 크기 · 하중 정의 미기재.
- 뜻: 길이척도 없는 구성식에서 나온 입경 효과는 기하 크기비 · 하중 정의의 산물 — '최적 10 µm' 를 다른 PTFE 등급 · 공정으로 옮길 수 없다.
- 할 일: 이 논문 수치를 인용할 때 "모형 PTFE 크기 미기재 · 입경 = AM : PTFE 크기비" 한정어를 붙인다.  우리 MPM 에 바인더를 넣게 되면 같은 검사 (크기 상사 시험) 를 먼저 등록한다.

**8-3. 미세 분획 응집이 Furnas 이득을 뒤집는다 (SiO₂ 실측).**
- 논문: 10 + 1.5 µm (크기비 0.15) 에서 탭 밀도 −14.5 % · 막 공극 +3.9 %p · 섬유화 부족.
- 뜻: 우리 압밀 DEM 의 Furnas dip 은 점착 없는 기하 결과다 — SE 1 µm (SE/AM_P 0.111) 처럼 미세한 분획이 응집하면 실측 충전은 기하 예측과 반대로 갈 수 있다.  믹서 논지 (SE–SE 응집) 의 배경과 같은 방향.
- 할 일: `comparison_vs_ours_DEM.md` D 절에 한 줄 (공유 파일이라 이 커밋에서는 손대지 않고 문안만 보고).

**8-4. 이 논문 숫자를 쓸 때의 함정.**
- Fig 5e = 노트북 '10' 행 (캡션 '10 + 5') · Fig 3b 의 1.5 µm 곡선 끝 = 노트북 20 MPa 값 · 본문의 10 µm 항복 · 섬유화 수치 = 그림의 20 µm 표지 · 10 mAh cm⁻² 는 50 사이클 ≈−9 % (본문 "no degradation") · 로딩 43/69 ↔ 44.06/63.22 mg cm⁻² · 최적화 목적함수가 본문과 다름 — 인용 시 그림 · 코드 값을 병기한다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Kang et al. (*Commun. Mater.* 2026) coupled a 2D COMSOL hyperelastic (Arruda–Boyce-type) model of a PTFE particle sheared between ceramic particles with GPR and a constraint-based search, and reported that 10 µm (unimodal) and 10 + 5 µm (bimodal) SiO₂ model particles gave the best PTFE fibrillation at a particle-loaded pressure of ≈14 MPa (≈13.5 MPa in a kneader at 10 rpm, model value); fibrillation itself is not part of the constitutive law, and the experimental validation is qualitative (SEM, cohesive load, MIP) with SiO₂ and liquid-electrolyte LFP half-cells without a control electrode."
- 국문: *"건식 PTFE 전극에서 활물질 입경이 섬유화를 정한다는 FEM–GPR 틀이 보고됐다 (Kang 2026) — 단 섬유화는 구성식이 아니라 응력–변형 구간으로 정의됐고, 입경 효과의 길이척도 원천과 실물 공정 조건이 적혀 있지 않다."*

## 10. 🔴 레드 플래그 — 원문 불일치 · 빠진 조건 · 해석 과장 (over-claim 방지)

1. **Fig 3a 캡션 "nominal diameters of 0, 1.5, 10, and 20 µm"** — '0' 은 0.1 의 오식 · 그 '0.1 µm' 시료의 PSD 최빈 ≈0.19 µm [판독] (명목의 ≈2 배).
2. **10 µm 의 항복 · 섬유화 수치**: 본문 p.2 *"yield point … at approximately 27 MPa (strain = 0.6) and an onset of robust fibrillation … at a peak stress of 30 MPa (strain = 1.8)"* ↔ Fig 3b 초록 (10 µm) 표지 ≈25.1 @0.58 · ≈26.1 @1.67 — 본문 값은 검정 (20 µm) 표지 ≈27.0 @0.64 · ≈28.8 @1.70 에 더 가깝다 [판독] · 변형률 1.8 은 어느 표지와도 안 맞음.
3. **'섬유화 구간' 의 시작 변형률이 그림마다 다르다**: Fig 2b **1.13** · Fig 3b ≈**1.67** · Fig 4b ≈**1.32** [판독] · Fig 2b 눈금 16.8 MPa ↔ 본문 16.9 MPa.
4. **'검증' 대상 실험 곡선 부재**: 계산 16.9 vs 실험 16.4 MPa 라는데 실험 곡선은 그림에 없고, 문장 끝 인용 *"fibrillation33”"* 의 ref 33 = PTFE 굽힘 응력 곁사슬 절단 논문 (*Appl. Surf. Sci.* 2023) · 같은 문장에 *"value comparable to the experimental result of 16.4 MPa"* 가 두 번 반복 인쇄.
5. **구성식이 무엇인지 모호**: Methods = 순수 초탄성 Arruda–Boyce (식 4) ↔ SI 표 1 = 가지 2 · 흐름 저항 · 응력 지수 · energy-storage factor (점탄소성 다중 가지 계열 [추정]) · *"We employed Simo-Taylor"* 정의 없음 · 식 (4) 괄호 (λ₁ᵖ + λ₂ᵖ + λ₃ᵖ) 는 Arruda–Boyce 원형의 (Ī₁ᵖ − 3ᵖ) 와 다르다 [추정 — 오식 후보] · 식 (3) ∇μ (= ∇u) · *"F is the strain"* (변형 구배) · 합 항 (사슬 엔트로피 탄성) 을 *"plastic deformation region"* 이라 부름 — 초탄성은 가역이고 '소성 · 섬유화 · 막 · 파단' 은 구성식에 없다 (응력–변형 곡선 위 사후 구간).  표 S1 의 초기 전단 223.7 MPa ↔ μ₀ 200 · λ_L 5.6 의 AB 급수 203.9 MPa [우리 산술 · 표준 급수 가정].
6. **응력 척도 불일치 가능성**: 출력 P_lm = 2nd Piola–Kirchhoff 인데 문턱 45 MPa 는 데이터시트 인장 강도 (보통 공칭) — 변형률 2–3 에서는 단축 비압축 기준 P = λS · σ = λ²S 로 수 배 차이 [추정] · 변형률 정의 · '최종' 값을 뽑는 점 [미확인].
7. **입경 효과의 원천 미기재 (CL-64 부류)**: 길이척도 없는 구성식인데 같은 PLP 에서 P_lm ∝ d^0.73 [우리 산술] → AM : PTFE 크기비 · 하중 정의에서 온 효과로 보임 [추정] · PTFE 초기 크기 · 2D/3D · 경계 · 메시 · 하중 속도 · 해석 시간 [미확인] · SI Fig 1 의 PTFE 몸체 크기가 패널마다 다르게 보인다 [판독].
8. **Fig 3b 의 1.5 µm 곡선 끝 (≈13.9 MPa @ ε ≈0.98)** ≠ Fig 5a · 노트북의 같은 입경 13 MPa 값 (8.87 MPa · 0.596) — 노트북 20 MPa 값 (13.43 · 0.943) 에 가깝다 [판독 · SI 코드] · 본문은 Fig 3b 를 *"under 13 MPa"* 라 한다.
9. **Fig 5e**: 캡션 *"fixed particle size combination of 10 + 5 µm"* ↔ 그림의 점 = 노트북 쌍봉 '10' 행 (15–20 MPa 57.7 · 61.6 · 58.4 · 56.0 · 48.7 · 46.3) — 노트북 셀은 `bi_fixed_particle_size = 5.0` · `ylim(0, 60)` 이고 '5' 행은 16–20 MPa 에서 73.8–82.0 MPa [판독 · SI 코드] · 그림 y 축도 60 을 넘는다 · 본문 패널 문자 누락 *"(Fig. 5)"*.
10. **최적화 목적함수가 본문과 다르다**: 본문 = "최종 변형률 최대화 (P_lm < 45 · ε < 4)" ↔ 노트북 단봉 = `입경 + PLP` (벌점) · 쌍봉 = `exp(−(σ̂ − 45)²/10)` — 크기별 '최적 PLP' 는 BO 가 아니라 제약 경계 격자 탐색 · BO 최적점 (6.10 µm · 17.25 MPa) 은 쓰이지 않음 · 단봉 BO 범위 6–10 µm (본문 1.5–10) · 쌍봉 BO 범위 6–20 µm (학습 3–10 → 외삽) · PLP 0.1–25 (쌍봉 학습 ≤ 20) [SI 코드].
11. **"상위 셋 4.5 · 5.0 · 6.0 µm · 13.5–14.7 MPa" 재현 불가**: 저장 출력에 없음 · 크기별 루프는 정수 입경만 · 학습표 선형 보간에서 45 MPa 경계 변형률이 3 · 4 · 5 · 6 µm 에서 3.106–3.111 로 같다 (3 µm 도 같은 값) [우리 산술] → 순위가 표의 셋째 자리 안에서 갈리지 않는다.
12. **GPR 검증의 범위**: 학습 R² 1.000 (보간) · CV 는 응력 모형만 · 무작위 5-겹 = 같은 입경 곡선 안 보간 시험 · 입경 하나 빼기 없음 · *"The entire dataset was used to train … without explicit division"* 과 'k-겹 검증' 이 한 논문에 함께 있다.
13. **노트북 상태**: 실행 번호 2 · 3 · 4 · 35 · 24 · 25 · 6 · 34 · 미실행 (셀 9 그림이 셀 7 학습보다 먼저) → 저장 출력 ↔ 저장 코드 일치 보장 없음 · 낡은 주석 ("150개" · "# 5개" · "임의 공식 + 노이즈로 생성" · "9 × 25 = 225") · 닿지 않는 `return` · **COMSOL 모델 없음** → *"Codes used to generate the simulation result"* (p.9) 는 GPR · 최적화 부분만 덮는다.
14. **SI Fig 5 'Bayesian optimization results'** = rpm 4–5 점의 1차원 GPR 적합 · 그 셀은 저장본에서 미실행 · MSE 계산 코드 없음 · MSE 를 MPa 로 표기 (제곱 단위여야) · 축 'Shear Stress' 단위 없음 · 본문의 '최적 rpm' (10 · 700) = 시뮬레이션한 격자점 그대로.
15. **PLP ↔ 전단 응력 혼용 · 환산식 없음**: *"Shear rates … converted into PLP values"* 의 식 없음 · 멱법칙 K · n 없음 · 과립을 'LFP density 3.6 g/cc' 로 둠 (복합 반죽 밀도 아님 [추정]) · *"validated by our in-situ monitoring"* 자료 없음.
16. **장비 · 공정 조건**: 반죽기 모형은 *"the experimental equipment used in this study"* 인데 Methods 장치 목록에 반죽기가 없다 · 실제 섬유화 장비 (압출기 NEP-0.5K) 는 *"based on the literature"* 기하로 모형화 · 실물 전극의 rpm · 시간 · 온도 · 간극 · 캘린더 압력 [미확인] · 10 rpm / 700 rpm 을 실제로 썼다는 문장 없음 · SiO₂ 막을 13 MPa PLP 로 만들었다는 연결 없음.
17. **인용 번호 어긋남 후보**: *"uniform particle size distribution (PSD)33"* (ref 33 = PTFE 곁사슬 절단; 실리카 합성은 ref 34) · 압출기 *"literature34,35"* (ref 34 = 실리카 나노입자 합성) · 끝 따옴표 *"33”"*.
18. **SI 교차 참조 오류**: 반죽기 기하 *"(Supplementary Fig. 2)"* = 실제 SI Fig 4 (SI Fig 2 는 탭 밀도) · SI Note 1 *"Supplementary Fig. 7 presents the SS curves"* = 실제 SI Fig 6 · SI Fig 5 는 본문 인용 없음.
19. **로딩 · 밀도 불일치**: Methods 43 · 69 ↔ SI Fig 7 44.06 · 63.22 mg cm⁻² · 습식 본문 48.47 ↔ SI 43.42 · 목표 2.3 g/cc ↔ 로딩/두께 2.01 · 2.46 (Methods) 또는 2.06 · 2.26 (SI) g cm⁻³ · 용량/로딩 0.163 vs 0.145 (Methods) ↔ 0.159 vs 0.158 (SI ≈ Fig 6f) [우리 산술 · 판독] · 로딩의 질량 기준 (AM · 전체) 미기재.
20. **"10 mAh cm−2 exhibited no degradation"** ↔ Fig 6g ≈10.14 → ≈9.24 mAh cm⁻² (−8.9 %, ≈25 사이클부터) [판독].
21. **대조군 없음**: 단봉 LFP · 비최적 조건 건식 · 습식 전기화학이 없다 (습식은 사진만) → *"enhanced electrochemical properties are experimentally validated"* (초록) · *"experimentally demonstrated its enhanced fibrillation and electrochemical properties"* (결론) 은 비교 근거가 없다 · 셀 수 · 오차 막대 0.
22. **R_ct**: Ω (면적 정규화 없음 · 전극 지름 미기재) · R_ct 비 1.29 ≈ 두께비 1.31 [우리 산술] → 기공 이온 저항이 섞였을 가능성 [추정] · 반쪽셀 Li 상대 전극 몫 분리 불가 · *"These results suggest that well-developed PTFE fibrillation … increasing the ion-transport efficiency"* 는 대조 없는 해석.
23. **응집 강도 시험**: UTM 방식 (박리 · 인장 · 굽힘) · 시료 폭 · 속도 · 반복 · 정규화 [미확인] — 'Load (N)' 막대 하나씩.
24. **MIP 공극의 교락**: 막의 캘린더 상태 · 두께 · 밀도 미기재 → 공극 차이를 섬유화 차이로 읽을 근거 부족 · LFP 전극 공극은 보고되지 않음.
25. **쌍봉 정의 결손**: 섞는 비율 (10 : 5 등) 미기재 · Fig 4a 의 10 + 5 PSD 에 따로 선 5 µm 봉우리 없음 [판독] · 5 µm 단봉 PSD · SEM · FEM 그림 없음 · *"optimal … within the 5–10 µm range"* (p.4) 의 5 µm 단봉은 시험되지 않았다.
26. **SiO₂ → LFP 이전 근거의 순환**: SI Fig 6 의 완전 겹침은 AM 을 PTFE 보다 훨씬 단단한 압자로 둔 모형에서 재질과 무관하게 나오는 결과 [추정] — 형상 · 표면 차이 (LFP 는 거친 응집 구, Fig 6a) 는 모형에 없다 · SI Note 1 의 '마찰계수 ≈0.2 → 형상 중요' 논리 연결 근거 없음.
27. **과장 · 용어**: *"We accurately predicted the optimal rotational speed conditions"* (p.6 — rpm 실험 대조 없음) · *"transformative 'game changer'"* (p.2) · *"particle dynamics"* = 2–4 개 원의 정적 FEM (입자 동역학 아님) · *"10–5 µm"* ↔ *"10 + 5 µm"* 혼용 · MIP *"evacuation pressure of 50 Torr Hg"* (인쇄 그대로 — 단위 확인 필요 [추정]).
28. **자료 공개**: 원자료 요청 시 · FEM 모델 미공개 · peer review file 은 언급만 [미확보].

## 11. 다른 카드 정정 후보 (보고만 — 이 커밋에서 손대지 않음)
1. `gandla2026_layered_cathode_degradation_diagnostics_review` 참고문헌 표 ref **127** 행 (*"★ 카드 없음 — 건식 공정 다중 척도 (권 · 연도 표기 충돌 §10-10)"*) → 이제 이 카드 (`kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode`) 가 있다.  그리고 §10-10 의 권호 충돌은 이 PDF 로 풀린다: 논문 자신이 **"Communications Materials | (2026) 7:34"** 로 인쇄하고 온라인 게재 2025-12-25 · © 2025 이므로, 7 권 = 2026 권 (그 총설의 "7 (2025)" 의 2025 는 온라인 · 저작권 해로 보인다) — [135] 의 "6 (2025)" 와 모순이 아니다.
2. (가드, 정정 아님) `kim2026_pregranulation_…` §11-2 의 *"정본에서 'Gachon' 이 나오는 기존 카드 셋 … 에 Junghyun Choi 는 없다"* 는 그 시점 사실 — 이제 Junghyun Choi 카드는 넷 (`gandla2026_…` · `kim2026_pregranulation_…` · `lee2026_li_underlayer_…` · 이 카드).  팔로우 랩 묶음을 셀 때 이 넷을 쓴다.
3. (참고) Woojin Jeong — 이 논문은 소속 3 (한양대) 만, `lee2026_li_underlayer_…` 는 b (가천대) + c (한양대) 로 인쇄.  같은 사람인지 [미확인] — 카드 정정 대상은 아니다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

**건식 공정 · 같은 계열 후보 (목록이 "et al." 표기라 같은 그룹인지 [미확인])**

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 7 | Lee, J. et al. Anode interface-stabilizing dry process employing a binary binder system for ultra-thick and durable battery electrode fabrication. Chem. Eng. J. 503, 158271 (2025). | 카드 없음 — `kim2026_pregranulation_…` §12 ref 20 과 같은 논문 (그 목록에는 J. Choi 가 저자로 인쇄) |
| 8 | Kim, J. et al. 10 mAh cm−2 cathode by roll‐to‐roll process for low cost and high energy density Li‐ion batteries. Adv. Energy Mater. 14, 2303455 (2024). | 카드 없음 — 10 mAh cm⁻² 건식 양극 R2R (`kim2026_pregranulation_…` §12 ref 16 의 전체 저자 목록에 J. Choi 인쇄) |
| 9 | Han, S. et al. Mitigating PTFE decomposition in ultra-thick dry-processed anodes for high energy density lithium-ion batteries. J. Energy Storage 96, 112693 (2024). | 카드 없음 — PTFE 분해 |
| 16 | Oh, H. et al. Development of a feasible and scalable manufacturing method for PTFE-based solvent-free lithium-ion battery electrodes. Chem. Eng. J. 491, 151957 (2024). | 카드 없음 — **반죽 시간 과부족 → 막 · 취성** 진술의 출처 (믹서 V2 의 공정 쪽 근거 후보) |
| 40 | Kwon, K. et al. Low‐resistance LiFePO4 thick film electrode processed with dry electrode technology for high‐energy‐density lithium‐ion batteries. Small Sci. 4, 2300302 (2024). | 카드 없음 — 건식 LFP 후막 (ΔV 0.22 V 비교의 출처 · `kim2026_pregranulation_…` §12 ref 23 의 전체 저자 목록에 J. Choi 인쇄) |

**우리 축에 직접 닿는 것**

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 3 | Chouchane, M., Yao, W., Cronk, A., Zhang, M. & Meng, Y. S. Improved rate capability for dry thick electrodes through finite elements method and machine learning coupling. ACS Energy Lett. 9, 1480–1486 (2024). | 카드 없음 — `comparison_vs_ours_DEM.md` 가 '확보 1순위 정본 (papers/ 미보유)' 로 적은 논문 |
| 12 | Horst, M. et al. Effect of active material morphology on PTFE-fibrillation, powder characteristics and electrode properties in dry electrode coating processes. Powder Technol. 451, 120451 (2025). | 카드 없음 — AM 형상 → PTFE 섬유화 (이 논문 이전 논리의 근거) |
| 15 | Lee, D. et al. Shear force effect of the dry process on cathode contact coverage in all-solid-state batteries. Nat. Commun. 15, 4763 (2024). | 정본 카드 `lee2024_shear_force_dry_process_cathode_coverage` |
| 17 | Matthews, G. A. B., Wheeler, S., Ramírez-González, J. & Grant, P. S. Solvent-free NMC electrodes for Li-ion batteries: unravelling the microstructure and formation of the PTFE nano-fibril network. Front. Energy Res. 11, 1336344 (2024). | 정본 카드 `matthews2024_ptfe_nanofibril_network` |
| 18 | Yonaga, A. et al. Effects of dry powder mixing on electrochemical performance of lithium-ion battery electrode using solvent-free dry forming process. J. Power Sour. 581, 233466 (2023). | 카드 없음 — 건식 분말 혼합 → 성능 (믹서 V2) |
| 19 | Tao, R. et al. Unraveling the impact of the degree of dry mixing on dry-processed lithium-ion battery electrodes. J. Power Sour. 580, 233379 (2023). | 카드 없음 (`kim2026_pregranulation_…` 도 인용) — **건식 혼합 정도** = 믹서 V2 선례 |
| 20 | Patil, P. D., Feng, J. J. & Hatzikiriakos, S. G. Constitutive modeling and flow simulation of polytetrafluoroethylene (PTFE) paste extrusion. J. Non-Newton. Fluid Mech. 139, 44–53 (2006). | 카드 없음 — PTFE 페이스트 유변 구성 모형 (K · n 대신 볼 곳) |
| 23 | Bergström, J. S. & Hilbert, L. B. A constitutive model for predicting the large deformation thermomechanical behavior of fluoropolymers. Mech. Mater. 37, 899–913 (2005). | 카드 없음 — 표 S1 의 다중 가지 모수의 원형 후보 [추정] |
| 27 | Arruda, E. M. & Boyce, M. C. A three-dimensional constitutive model for the large stretch behavior of rubber elastic materials. J. Mech. Phys. Solids 41, 389–412 (1993). | 카드 없음 — 식 (4) 원형 대조용 |
| 35 | Haarmann, M., Grießl, D. & Kwade, A. Continuous processing of cathode slurry by extrusion for lithium‐ion batteries. Energy Technol. 9, 2100250 (2021). | 카드 없음 — 압출기 모형 기하의 출처 |
| 36 | Lavrov, A. Numerical modeling of steady-state flow of a non-Newtonian power-law fluid in a rough-walled fracture. Comput. Geotech. 50, 101–109 (2013). | 카드 없음 — 멱법칙 식 출처 (전극 반죽 값은 아님) |
| 41 | Bi, Z. & Mueller, D. W. Friction predication on pin-to-plate interface of PTFE material and steel. Friction 7, 268–281 (2019). | 카드 없음 — PTFE E · ν 출처라는 논문 (마찰 논문 — 값 확인 필요) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 11 쪽 · SI 11 쪽 텍스트 층 전수 (pdftotext · PyMuPDF) · 저자 · 소속 · 교신 · 날짜 · DOI · 라이선스 · 연구비 · 데이터 · 코드 진술 = p.1 · p.9–11 · SI p.1 그대로 · 저자 줄의 위첨자 · ✉ 는 p.1 을 300 dpi 로 렌더해 확인 · 'Published online: 25 December 2025' 는 p.9 의 이미지 줄 (텍스트 층에 없음) 을 렌더로 확인.
- 본문 식 (2)–(8) · (1) 은 텍스트 추출이 깨져 300 dpi 렌더로 읽음 (크롭 eq_1 · eq_2-4 · eq_5-8).
- 노트북: `python3 -I` · json.load 로 14 셀 원문 · 출력 텍스트 전수 · 학습 배열은 셀 원문에서 리스트 리터럴만 `ast.literal_eval` 로 꺼내 길이 (270 · 200) · 행 (13 · 20 MPa) · 45 MPa 경계를 우리 산술로 계산 — **노트북 실행 · import · 변환 0** · 출력 PNG 6 장 미해독.
- 크롭 19 장 손 크롭: 본문 그림 = 래스터 원본 300 ppi (덧그림 벡터 · 텍스트 없음 확인) · SI 그림 = 원본 150–220 ppi 를 220 dpi 로 · 식 · 표 · Note = 벡터 300 dpi · 전부 렌더로 열람 (접촉 시트 포함).
- 판독 보정 검산: Fig 5e 점 ↔ 노트북 '10' 행 |차| ≤ 0.2 MPa · Fig 5c 경계 ≈14.2 ↔ 보간 14.38 MPa · Fig 2b · 3b σ_T 선 45.0 · 44.7 MPa · Fig 6g 7 mAh 계열 7.08 (명목 7).
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 433 장 전수 + 체크아웃 전 `git grep` (DOI `s43246-025-01046` · 제목 낱말 · 저자 이름) — 카드 없음, `gandla2026_…` 의 참고문헌 행 하나만 (§11-1).
- 팔로우 랩 표지: 인쇄 "Junghyun Choi" · 소속 5 = 가천대 · 교신 (✉) 확인 · 한글 이름 인쇄 없음.

## 🔗 관련 카드
- 같은 팔로우 랩: `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` · `lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode` · `gandla2026_layered_cathode_degradation_diagnostics_review`.
- PTFE 건식 전극 · 섬유: `matthews2024_ptfe_nanofibril_network` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · `kang2025_bollard_anchored_binder_dry_electrode` · `lee2024_shear_force_dry_process_cathode_coverage` · `nam2026_primer_layer_dry_electrode_collector`.
- 건식 공정 총설 · 구조: `liu2025_dry_processing_high_energy_li_batteries_review` · `mun2025_dry_electrode_technology_assb_review` · `nam2026_dpe_microstructure_review` · `zhang2026_dryprocess_electrode_architecture_cell_level` · `yoo2026_porosity_gradient_dry_electrode` · `wang2026_dryprocess_thick_cathode_failure_ncm94` · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure`.
- 공정 모의 (DEM · FEM): `sun2026_dem_extrusion_recirculation_dry_electrode` · `zhang2026_xct_dem_cathode_calendering_peel_calibration` · `lim2025_virtual_calendering_framework` · `cronk2026_lis_positive_electrode_geometry_fem` (CL-64) · `duquesnoy2023_ml_multiobjective_manufacturing_optimization`.
- 혼합 · 응집 · 충전 (믹서 논문): `otani2025_dem_se_dispersion_aggregation_compression` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `jarray2019_cohesion_driven_mixing_segregation_drum` · `alizadeh2018_dem_adhesion_calibration_segregation_heap` · `geldart2006_powder_flowability_angle_of_repose_tester` · `mcgeary1961_bimodal_sphere_packing`.
- LFP 입경: `eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
