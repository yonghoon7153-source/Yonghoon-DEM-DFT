# batch 56 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `choi2018_fibsem_3d_composite_cathode_microstructure_tpb_pore_decomposition` — Sungjun Choi, Minjae Jeon, Junsung Ahn, Wo Dum Jung, Sung Min Choi, Ji-Su Kim, Jaemin Lim, Yong-Jun Jang, Hun-Gi Jung, Jong-Ho Lee, Byoung-In Sang, Hyoungchul Kim, "Quantitative Analysis of Microstructures and Reaction Interfaces on Composite Cathodes in All-Solid-State Batteries Using a Three-Dimensional Reconstruction Technique", *ACS Appl. Mater. Interfaces* 10, 23740–23747 (2018) · DOI 10.1021/acsami.8b04204 — 본문 8 쪽 · SI (그림 S1–S5) 미입수 · 그림 5 · 표 3 · 번호 식 0 (그림 2 안 식 넷 + 본문 문장 식 둘) · 참고문헌 32.
현대차 · KIST 의 습식 시트 황화물 ASSB 복합 양극 (LiNbO₃ 코팅 NCM622 : LPN821 = (Li₂S)₈(P₂S₅)₂(Ni₃S₂)₁ : C65 : 바인더 = 67.6 : 29.0 : 1.4 : 2.0 wt% · 231 MPa 적층) 을 1 회 사이클 뒤 분해해 FIB-SEM (5263 µm³) 로 4 상 정량한 방법 논문.  후보 표 N-14 의도 = **일부**: 3D 재구성 · 반응 계면 정량의 방법 근거 (nakamura2020) = 채움 · Shi Fig 7a 기공 띠의 출처 = 한 값 14.99 % (일부) · "densities" = 없음 · "LPS 소성 실험관측" = 체적 탄성률 인용 해석 · SE 는 LPN821 (일부).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (복합 양극 한 조건뿐 · 순수 SE 펠릿 · 압력 계열 · 진밀도 0 — 카드 §3-3 · §13).  곁 정보: SE 물성으로 인용된 값은 Li₃PS₄ 체적 탄성률 B ≈20 GPa ([30] Baranowski 2016 · 다른 물질 · 카드 §3-5) 하나.

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 3D 시료 = 231 MPa 적층 · 코인 조립 · 1 회 사이클 · 완전 방전 · 분해 뒤 (압력 뺀 상태) 한 점 · 되튐 · 회복 · 내리는 곡선 0 (unload · spring · relax 낱말 0 회 — 카드 §4-4 (4) · 원문 대조 기록).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] choi2018_fibsem_3d_composite_cathode_microstructure_tpb_pore_decomposition | 항복 · 경도 · 크리프 값 없음 — 체적 탄성률 인용 둘: *"the solid electrolyte with a low bulk modulus (B_Li3PS4 ≈20 GPa³⁰) has excellent plastic deformation characteristics, and the cathode active material with poor deformability (B_NCM ≈140 GPa³¹) is hard and induces more pore structure"* · 둘 다 다른 물질의 문헌값 (Li₃PS₄ [30] · NCM 일반 DFT [31]) — 이 논문의 LPN821 · Nb/NCM622 값 아님 · 일축 항복 환산 없음 | 카드 §3-5 · 논문 p.23744 · `txt_p5_pdp_bulk_modulus_plastic_deformation.png` | [인쇄] | B (부피 강성) 를 소성의 척도로 읽는 근거가 원문에 없다 [카드 해석] · 우리 MPM 은 거꾸로 체적 실제값 (K 25.5 GPa) · 전단만 연화 · B_NCM 140 GPa 는 우리 DEM NCM 영률 140 GPa 와 숫자만 같다 (양 다름 · 출처로 쓰지 않음)

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] choi2018_… | 하중 몫 숫자 없음 — 정성 하나: 기공 원천 분해 (PDP · S_Pore,i = (k·S_i) ∩ S_Pore) 가 기공 부피 377.1 µm³ (59.10 %) 를 NCM · 261.0 µm³ (40.90 %) 를 LPN 에 돌림 → 결론 *"rigid cathode active materials induce more pores than sulfide electrolytes"* (단단한 AM 근처에 빈 곳이 남는다) | 카드 §3-5 · 논문 Table 3 · p.23744–23745 · Fig. 4 | [인쇄] · 두 부피 합 638.1 µm³ = 전체 기공의 80.9 % [카드 산술] | k 값 · 겹친 기공 처리 [미확인 · SI] · 입경 (SE 6 > AM 4 µm) · 부피 차 섞임 · 사이클 1 회 뒤라 압밀만의 결과 아님 · 본문 '43 % · 56 %' 는 표의 표면적 몫 (부피는 40.90 · 59.10)

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (DEM · 접촉 법칙 없음).  원문의 *"point contact(s)"* (p.23740 · p.23743 · p.23745) 는 실물 계면 (미세 기공을 낀 점 같은 접촉) 의 결함 서술이지 접촉 법칙의 한계 문장이 아니다 (카드 §4-4 (1)).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).  곁 정보 (영상 해상도 쪽): FIB 단면 100 nm · 면 화소 [미확인] — 저자: *"the conductive additive is underestimated and the pore region is overestimated"* (SEM 해상도 · 회색조 대비 · 작은 부피 [22, 26] · p.23743–23744) · 탄소 연결도 0.3331 이 해상도 산물일 수 있다 [카드 해석] (카드 §8 U0–U6).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] choi2018_… | 2D → 3D 값 전이 경고 · 증거 없음 — 동기 문장만: *"Till date, only qualitative shape and distribution observations based on scanning electron microscopy (SEM) and energy dispersive X-ray spectroscopy have been possible"* (2D 정성 → 3D 정량) · 측정 = 2D SEM 100 장을 쌓은 3D | 카드 §4-4 (3) · 논문 p.23740 · `txt_p1_intro_point_contacts.png` 다음 문장 | [인쇄] | —

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (계산 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] choi2018_… | **압력별 아님 · 한 점**: FIB-SEM 국소 5263 µm³ 의 회색조 분할 기공 **14.99 %** (원문 *"approximately 15%"*) · SE 42.52 · AM 40.05 · 탄소 2.44 % · 기공 뺀 50.01 : 47.11 : 2.87 ↔ 입력 58.48 : 38.37 : 3.15 % | 카드 §3-3 · 논문 Table 2 · p.23743 · `txt_p4_p5_pore_15pct_volume_ratio_errors.png` | [인쇄] | 조건 = 습식 시트 (바인더 2 wt% · 바인더 상 없음) · 231 MPa 적층 · 1 회 사이클 · 완전 방전 · 분해 (압력 뺀 뒤) · 진밀도 분모 없음 · LPN821 + NCM622 (고체 중 SE 30 wt%) · 랩 표준 (순수 SE 10–13 % · 1.64) 과 다른 양
- [i] choi2018_… | **국소 ↔ 셀 어긋남**: 같은 논문의 두께 79 µm · AM 11.099 mg (Ø 14 mm → 7.21 mg cm⁻²) 로는 AM 부피분율 0.19–0.20 ↔ FIB 0.4005 (FIB 가 맞으려면 두께 38–40 µm) | 카드 §3-3 | [카드 산술 · NCM622 ρ 4.5–4.7 다른 카드 (`asylbekov2023_…` · `alabdali2023_…`)] | 79 µm 의 상태 (적층 전 / 후) · FIB 위치 [미확인] · 같은 분석 안 SE 분율 61.45 → 42.52 % (원문 표본 오차)
- [i] choi2018_… | Shi 2019 Fig 7a 의 'Φ 0.1–0.2 = 실험 보고 기공' 의 출처 [29] = 이 한 값 — 띠 끝값 · "previously reported densities" 는 원문에 없다 (밀도 숫자 0 개) | 카드 §0-1 | [인쇄] · 원문 전수 | `shi2019_…` L119 의 "우리 15.6 % 가 이 범위 안" 은 우연한 가까움

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] choi2018_… | 원문이 적은 한계: SEM 해상도 · 회색조 대비 · 작은 재구성 부피 [22, 26] · 탄소 과소 · 기공 과대 · *"sampling errors due to the limited volume of the 3D reconstruction area must also be considered"* (SE 분율 61.45 → 42.52 %) | 카드 §3-9 · 논문 p.23743–23744 | [인쇄] | 반복 · 다른 위치 없음
- [j] choi2018_… | 카드가 본 한계: 상태 (압력 뺀 뒤 + 사이클 1 회 — 압밀 직후 구조 아님) · SI 미입수 (면 화소 · 문턱 · 연결 · 중심점 규칙 · k · 면적법) · 원문 안 어긋남 열 (23 % 의 분모 · PDP 백분율 · 용량 백분율 40 회 75 % ↔ 판독 69.7 % · 100 회 78 % ↔ 판독 81.6 % · 입력 부피비 재현 안 됨 · 79 µm) · 압력 계열 · 탈압 없음 | 카드 §3-9 · §11 · §13 | [카드 산술] · [판독] · [미확인] | —

## k — DEM 의 한계
- [k] choi2018_fibsem_3d_composite_cathode_microstructure_tpb_pore_decomposition (S. Choi · M. Jeon · J. Ahn … H. Kim · 2018 · ACS Appl. Mater. Interfaces 10, 23740–23747) | **말 없음** — DEM · discrete · simulation 0 회 (원문 낱말 셈 · 'model' 은 참고문헌 (26) 제목 'Modeling' 1 회) · 원문의 *"formation of interface pore structures through point contacts"* (p.23740) · *"The interaction between such point contact interfaces with the micropores acts as a resistance element"* (p.23743) · *"if the interface resistance induced by the point contact is reduced"* (p.23745) 는 실물 계면 서술이지 DEM 한계 문장이 아니다 | 카드 §4-4 (1) · 원문 대조 기록 | 원문 전수 | —

## l — 소성변형이 왜 어려운가
- [l] choi2018_fibsem_3d_composite_cathode_microstructure_tpb_pore_decomposition (S. Choi · … · H. Kim · 2018 · ACS Appl. Mater. Interfaces 10, 23740–23747) | 소성 계산 · 우회 · 비용 **없음** — 소성은 해석 한 문장: *"Such difference is due to the fact that the solid electrolyte with a low bulk modulus (B_Li3PS4 ≈20 GPa) has excellent plastic deformation characteristics, and the cathode active material with poor deformability (B_NCM ≈140 GPa) is hard and induces more pore structure."* (p.23744) · 근거 = PDP 기공 원천 비 + 문헌 체적 탄성률 · 압력 = 231 MPa 적층 (뒤에 1 회 사이클) · 변형 측정 · 입자 전후 영상 · 압력 계열 없음 · SE = LPN821 | 카드 §3-5 · §4-4 (2) · `txt_p5_pdp_bulk_modulus_plastic_deformation.png` | [인쇄] | Shi 2019 의 *"plastic deformation of LPS particles, which has been observed experimentally.[29]"* 의 원전이 이것 → '관찰' 이 아니라 '해석' 으로 낮춰 인용 · 정성 관찰은 *"the electrolyte and the active material were in close contact"* (p.23743) 뿐

## m — 받아들일 통찰
- [m] choi2018_… | **기공 연산자 표에 '국소 ↔ 셀 대표성' 칸**: 문헌 FIB · CT 기공을 받을 때 부피 (µm³) · 위치 · 같은 논문의 질량 · 두께 기공과의 일치를 함께 적는다 | 자리: 단계 0 · 결과 전 대조 항목 | 왜: 이 논문 자신이 AM 부피에서 2 배 어긋난다 (79 µm · 7.21 mg cm⁻² → 0.19–0.20 ↔ FIB 0.4005 · 카드 §3-3 [카드 산술]) · SE 분율이 같은 분석 안에서 61.45 → 42.52 % (p.23744)
- [m] choi2018_… | **계면 면적 밀도 · 최대 덩어리 분율을 우리 DEM 출력에 같은 정의로**: a_AM–SE = Σ A_contact(AM–SE) ÷ 상자 부피 (Hertz · Tabor 둘) 와 Max(V)/ΣV 꼴 (`se_largest_comp_frac`) 을 결과 전에 등록 — 값은 견주지 않고 단위 · 정의만 맞춘다 | 자리: 단계 7 · 후보 D0 · 결과 전 대조 항목 | 왜: 원문 정의 = 그림 2 식 (연결도) · 밀도 = 면적 / 5263 µm³ (네 값 재현 [카드 산술]) · AM–SE 0.213 µm⁻¹ · AM 피복 어림 26–35 % 는 우리 기하 '1 복셀 안' (49 %) 쪽 정의 (카드 §3-6 · §7-3)
- [m] choi2018_… | **함정 — 'TPB' 와 '23 %'**: 이 논문 'TPB' = two-phase boundary (triple-phase 아님) · "≈23 %" = 세 '유효' 두 상 경계 면적 ÷ 기공 포함 전체 경계 면적 (AM–SE 만이면 15.4 %) — 초록 · 결론의 'of the total volume' 은 옮기지 않는다 | 자리: 흐름 밖: Rint 계면 몫 · 피복 문서 · 덱 | 왜: 카드 §3-6 · Table 2 [카드 산술 1674/7284 = 0.2298 · 1120/7284 = 0.1538]
- [m] choi2018_… | **함정 — 'tortuosity' 와 '소성' 의 이름**: τ = 중심점 경로 L/H (그림 2 식) 는 tau2 · τ_geo 어느 열에도 넣지 않고, "낮은 B = 소성 좋음" 은 인용하지 않는다 (소성 근거는 압입 · Heckel 카드) | 자리: 단계 4 · 조건 R6 · 흐름 밖: τ 규약 J 절 | 왜: 원문이 L/H 를 바로 σ_eff = (ε/τ)σ 에 연결 (Bruggeman 의 3.9–5.1 배 [카드 산술]) · B 는 다른 물질의 부피 강성 (카드 §3-4 · §3-5)

## n — 논문 에이전트 후보
- [n] (30) Baranowski, L. L.; Heveran, C. M.; Ferguson, V. L.; Stoldt, C. R. Multi-Scale Mechanical Behavior of the Li3PS4 Solid-Phase Electrolyte. ACS Appl. Mater. Interfaces 2016, 8, 29573−29579. | c (· a) — B_Li₃PS₄ ≈20 GPa 의 출처 (밀도 · 방법) 와 다공 Li₃PS₄ 탄성의 원전 · 카드 §3-5 · §12 · Shi 의 'LPS 소성' 사슬의 마지막 고리 | litdb 확인: papers/ 538 파일 목록에 baranowski* 없음 · "29573" · "Baranowski" grep = `lee2025_heckel_…` · `papakyriakou2021_…` · `song2025_porous_argyrodite_…` · `thompson2026_…` · `var2026_…` (인용만) → 카드 없음
- [n] (31) Sun, H.; Zhao, K. Electronic Structure and Comparative Properties of LiNixMnyCozO2 Cathode Materials. J. Phys. Chem. C 2017, 121, 6002−6010. | c — B_NCM ≈140 GPa (DFT) 의 출처 · 우리 DEM NCM 영률 140 GPa (출처 미검증) 와 섞이지 않게 NCM 탄성 상수 원문 확인 · 카드 §3-5 · §12 | litdb 확인: sun2017* 없음 · "Sun, H.; Zhao" grep 0 · "6002" grep = `sharma2023_…` · `sedlatschek2026_…` · `xu2017_…` · `nolan2018_…` (인용만) → 카드 없음
- [n] (29) Kehrwald, D.; Shearing, P. R.; Brandon, N. P.; Sinha, P. K.; Harris, S. J. Local Tortuosity Inhomogeneities in a Lithium Battery Composite Electrode. J. Electrochem. Soc. 2011, 158, A1393−A1399. | j · m — 국소 부피마다 tortuosity 가 다름 (FIB 국소 부피 대표성 문제의 정량 · `tjaden2018_…` L58 이 "12 개 부분부피 · 국소 τ 3 배 차" 로 요약) · 카드 §12 | litdb 확인: kehrwald* 없음 · "A1393" grep 0 · "Kehrwald" grep = `froboese2019_…` · `tjaden2018_…` (인용만) → 카드 없음
- [n] (26) Zielke, L.; Hutzenlaub, T.; Wheeler, D. R.; Chao, C.-W.; Manke, I.; Hilger, A.; Paust, N.; Zengerle, R.; Thiele, S. Three-Phase Multiscale Modeling of a LiCoO2 Cathode: Combining the Advantages of FIB-SEM Imaging and X-Ray Tomography. Adv. Energy Mater. 2015, 5, 1401612. | f · j — 저자가 'SEM 해상도 · 작은 부피' 오차의 근거로 든 FIB-SEM + XCT 다중 스케일 (탄소 · 바인더 상 해상도 · 대표 부피) · 카드 §3-3 · §12 | litdb 확인: zielke* 없음 · "1401612" grep 0 · "Zielke" grep = `landesfeind2016_…` · `landesfeind2018_…` · `ngandjong2021_…` · `pouraghajan2018_…` (인용만) → 카드 없음
- [n] (6) Park, M.; Jung, H.-G.; Jung, W. D.; Cho, S. Y.; Yun, B.-N.; Lee, Y. S.; Choi, S.; Ahn, J.; Lim, J.; Sung, J. Y.; Jang, Y.-J.; Ahn, J.-P.; Lee, J.-H.; Kim, H. Chemically Evolved Composite Lithium-Ion Conductors with Lithium Thiophosphates and Nickel Sulfides. ACS Energy Lett. 2017, 2, 1740−1745. | 흐름 밖 (· c) — LPN821 의 합성 · 상 · 전도도 (이 카드의 SE 물성 [미확인] 을 채움) · 카드 §3-1 · §12 | litdb 확인: park2017* 없음 · "Chemically Evolved" · "Ni3S2" · "1740" grep 0 → 카드 없음

## 카드 문제
- `shi2019_high_am_loading_particle_size_assb` L103: *"ref [29] = Choi et al. ACS AMI 2018 = 'LPS 입자의 소성변형 을 실험관측'"* ↔ 원문 = 체적 탄성률 인용 해석 (*"has excellent plastic deformation characteristics"* · B_Li₃PS₄ ≈20 GPa [30] · p.23744) · SE = LPN821 ((Li₂S)₈(P₂S₅)₂(Ni₃S₂)₁ · LPS 유리 아님) · 변형 측정 · 영상 없음 — '실험관측' 은 Shi 원문 문장을 옮긴 것이고 Choi 원문으로는 '해석'.
- `shi2019_…` L36–37 · L193 · L291 · L499: 같은 '[29] = LPS 소성 (관측)' 귀속 — 위와 같은 정정 대상 (L583 · L622 · L670 · L696 · L719 는 Shi 자신의 "정확한 접촉면적엔 LPS 소성 모델 필요" 문장이라 해당 없음).
- `shi2019_…` L45 · L104–107: *"[29] Choi 2018 … 정본 litdb 에 카드가 없다 … 내용은 [미확인]"* → 이 카드로 해소 (갱신 대상) · 같은 줄 *"[29] 는 Fig 7a 의 'previously reported densities and composite cathode porosities' (Φ 0.1–0.2) 의 출처"* ↔ 원문 = 기공 한 값 14.99 % (국소 FIB · 231 MPa 적층 · 사이클 1 회 뒤 분해) · 밀도 숫자 0 개.
- `shi2019_…` L119: *"Φ ≈ 0.1–0.2 (그림 음영대 = 실험 보고 porosity) · SSB 양극 복합, ref [29] … 우리 15.6 % 가 이 범위 안"* ↔ [29] = 한 값 14.99 % (띠 끝값은 Shi 의 선택 · 측정 조건 위와 같음).
- `shi2019_…` L289: *"f_CAM=80 wt% ≈ 50 vol% (이전 보고 밀도·porosity 로 환산, ref [29])"* ↔ [29] 에 밀도 없음 (Shi Fig 7a 의 밀도 = Shi SI 표 1 · 그 카드 L140).
- `nakamura2020_dry_coating_ncm_li3ps4_core_shell` L331: *"카드 없음 — 3D 재구성 · 반응 계면 정량 (방법 근거)"* → 이 카드로 해소 (갱신 대상 · 판정 = 채움).
- `nakamura2020_…` L227: *"분할 · 재구성 · Poisson 풀이 소프트웨어 [미확인] (방법 근거 refs 12 · 30 · 31)"* ↔ ref 12 (이 논문) 는 분할 · 재구성 · 계면 면적의 근거이고 Poisson (복셀 σ_eff) 풀이는 쓰지 않는다 (τ = 중심점 경로 L/H) — nakamura 원문에서 ref 12 가 붙은 문장은 이 카드가 확인하지 못함 [미확인] (확인 거리).
- `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` L346: *"(23) … 카드 없음 (shi2019 · nakamura2020 카드가 인용만)"* → 이 카드로 해소 (갱신 대상) · *"14.7 % 공극/탄소가 'similar to prior studies' 의 근거"* ↔ [23] 기공만 14.99 % (탄소 2.44 % 따로 · 합 17.43 % [카드 산술]) — 값 수준은 맞고 정의 (기공만 ↔ 기공 + 탄소) · 재료 · 공정이 다르다.
- 후보 표 `litdb/_curation/S8_candidates.md` N-14 행 (카드 아님): *"제목 카드에 없음"* → 제목 = "Quantitative Analysis of Microstructures and Reaction Interfaces on Composite Cathodes in All-Solid-State Batteries Using a Three-Dimensional Reconstruction Technique" · 저자 12 명 · DOI 10.1021/acsami.8b04204 (서지 자체는 원문과 같다).
- (참고 · 원문 자체 · 카드 §3-9) PDP 본문 '43 % · 56 %' (표의 표면적 몫) ↔ 부피 40.90 · 59.10 % · "≈23 %" 의 분모 (경계 면적 ↔ 초록 · 결론 'of the total volume') · 결론의 '23 % = AM–SE TPB' (AM–SE 만 15.4 %) · 용량 백분율 (40 회 75 % ↔ 판독 69.7 % · 100 회 78 % ↔ 판독 81.6 %) · 입력 부피비 재현 안 됨 · 두께 79 µm ↔ FIB AM 40 % · 기공 분해 합 = 전체 기공의 80.9 % · 흑연 완전 셀 전압 'vs Li/Li⁺' 표기 — 원문의 문제이지 정본 카드의 문제가 아니다.
