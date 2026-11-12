<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-27 · 정독 69) 에서 꼭 뽑으라고 한 항목.
     본 = he2026_dem_calendering_inhomogeneity_areal_density.md (같은 분야 · 액체 LIB 양극 압연 DEM · 같은 EEPA · 머리 상자 · 메타 줄 · 서지 표 · 그림 표) · 두 필수 절 = §0-1 고른 의도 대조 · §8 자세한 분석 (같은 날 카드들과 같은 자리).
     원문 = 출판본 (Journal of Energy Storage 138 (2025) 118688 · 19 쪽 · 보충 자료 없음 · 부록 A = DEM 접촉 식 pp.16–17).  쪽 표기 "p.n" = PDF 쪽 n (= 논문 쪽 · 머리글 "Journal of Energy Storage 138 (2025) 118688" 아래 쪽 번호 1–19).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (그림은 전부 300 dpi 내장 래스터 · 벡터 그림 없음 · 재현 = litdb/figures/<slug>/digitized.csv 163 행 · 방법 = 행마다 note) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · §14) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md · 정본 카드가 옮긴 것 — 출처를 그 자리에 적는다) · [미확인] = 본문 19 쪽 전수에 없음.
     원문 19 쪽은 글자 층 (PyMuPDF) + 쪽 렌더 + 내장 래스터로 읽었다.  계산 = 상용 DEM (Altair EDEM 2021) + 상용 FEM (ANSYS 2022) · 코드 · 입력 파일 공개 없음 (*"Data will be made available on request."* p.17). -->
# 액체 LIB 양극 (NMC532 : CB : PVDF = 90 : 5 : 5 · SE 없음) 의 롤 압연을 평판 근사 DEM (EDEM 2021 · 단단한 구 · 탄소성 점착 접촉 법칙 · 3D RVE 100 µm) 과 한 방향 집전체 FEM (ANSYS 2022 · Al 박 RVE 100 × 100 × 17 µm · 정적) 으로 — 힘 사슬 밀도 (접촉 쌍 23,940 → 41,816) · 방향 (직물 편차 F′zz +0.048 → −0.03) · 세기 (강한 사슬 = 평균 힘 초과 · 수 몫 21.49 → 9.73 %) · Al 박 최대 응력 256.5 MPa (압하율 40 %) · 박힘 구멍 · 입경 · 입도 폭 효과 — Du · Zhang · Du · Yang · Zhao (J. Energy Storage 138 (2025) 118688)

> slug `du2025_dem_fem_force_chain_collector_damage_calendering` · DOI `10.1016/j.est.2025.118688` · type `DEM (Altair EDEM 2021, EEPA elasto-plastic adhesive law, rigid spheres AM + CB from measured PSD, PVDF only through surface energy + pull-off force, 3D RVE 100 x 100 x 100 um periodic in x-y, steel platen approximation of the roll) + one-way DEM to FEM (EDEM-ANSYS Workbench axdt force map, 3 um one-to-one interface mesh, ANSYS 2022 Al collector RVE 100 x 100 x 17 um, C3D8R, static) + experiment (NMC532 cathode roll press 10-40 % compression, SEM, CLSM pits); liquid-electrolyte LIB cathode, no SE` · PDF `82656eb1-27._Force_chain-induced_collector_damage_in_calendering_A_DEM-FEM_study.pdf` (19 쪽 · 보충 자료 없음) · digested `2026-11-12` · status ✅

> elements: Li, Ni, Mn, Co, O, Al
> methods: elastic, adhesion

> **저자**: **He Du** ᵃ · Yuxin Zhang ᵇ · **Xiaozhong Du** ᵃ·ᵈ·\* · Kaiyue Yang ᵃ·ᶜ · Le Zhao ᵃ — ᵃ School of Mechanical Engineering, Taiyuan University of Science and Technology (Taiyuan 030024) · ᵇ School of Mechanical Engineering and Automation, Northeastern University (Shenyang 110819) · ᶜ Institute of Intelligent Manufacturing, Shanxi Vocational University of Engineering Science and Technology (Jinzhong 030619) · ᵈ School of Energy and Materials Engineering, Taiyuan University of Science and Technology — \* 교신 · *Journal of Energy Storage* **138** (2025) **118688** (논문 번호 · 19 쪽 · 섹션 *"Research Papers"*) · 접수 2025-06-05 · 수정 2025-08-17 · 승인 2025-09-26 · **온라인 2025-10-04** (p.1) · © 2025 Elsevier Ltd · 키워드 Lithium-ion battery · Calendering · Electrode · Current collector damage · Force chain · DEM-FEM coupling · 연구비 = Shanxi Scholarship Council of China 2021-137 · Fundamental Research Program of Shanxi Province 202103021224273 · Postgraduate Education Innovation Project in Shanxi Province 2025XS139 (p.16) · 자료 = *"Data will be made available on request."* (p.17).
> **이웃 카드 (링크만)**: [`he2026_dem_calendering_inhomogeneity_areal_density`](he2026_dem_calendering_inhomogeneity_areal_density.md) (이 논문을 N5 · 입자–Al 마찰 출처 [41] 로 가리킨 카드) · [`zhang2026_xct_dem_cathode_calendering_peel_calibration`](zhang2026_xct_dem_cathode_calendering_peel_calibration.md) (같은 꼴의 압연 DEM · 집전체 매립 · Love–Weber 응력) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) (CT + DEM 힘 사슬) · [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) (= 이 논문 [75] · 식 1 · θ < 1° 의 출처) · [`schreiner2020_dem_calendering_lib`](schreiner2020_dem_calendering_lib.md) (= [86]) · [`thakur2014_eepa_adhesive_elastoplastic_dem`](thakur2014_eepa_adhesive_elastoplastic_dem.md) (= [84]) · [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) (EEPA 원전 · 인용은 안 함).
> **판독 원자료**: `litdb/figures/du2025_dem_fem_force_chain_collector_damage_calendering/digitized.csv` (163 행 — 그림 5c 점 · 맞춤 곡선 · 5d · 6i 삽입 · 6j · 6m · 8j–l 골 · 8m 곡선 · 8n · 8o · 10m · 10n · 10o · 11g · 11h) · 그림 크롭 **70 장** (도구 12 → 전부 다시 자름 + 손 58 = 패널 17 · 식 21 · 근거 문단 20) — `figures.json`.

> ⚠⚠ **한 줄 경고 — 이 논문은 SE 가 없다.**  조성 NMC532 : CB : PVDF = 90 : 5 : 5 (wt) 의 **액체 전해질 LIB 양극** (고체 부피로 AM 78.9 · CB 9.3 · PVDF 11.8 % [카드 산술 · 표 1 밀도 + PVDF 1.76]) 을 **롤 압연** (지름 200 mm · 1 m/min · 선하중 14–530 N/mm) 한 것이고, DEM 은 롤이 아니라 **강철 평판** 으로 누른다.  우리 침대 (NCM811 + LPSCl · SE 가 소성 유동을 맡음 · 다이 300 MPa) 의 **AM 골격 쪽 극한** 으로만 읽는다 — 힘 · 응력 · 기공 절대값을 우리 표에 넣지 않는다.

> ★★ **이 카드의 핵심 셋 (원문에 없는 · 원문과 어긋나는 것 포함 — §3-11 · §14)**:
> ① **he2026 의 '입자–Al 마찰 0.61 / 0.12 / 0.65 · JKR 1.5 J/m² = [41] Du 2025' 는 이 논문에 없다** — 표 1 은 입자–입자 8 줄뿐이고 입자–Al · 입자–강철 접촉 줄이 통째로 없다.
> ② **'강한 힘 사슬' = 평균 힘을 넘는 접촉의 *수* 몫** (21.49 → 9.73 %) 이고 하중 몫이 아니다 — 상별 · 쌍 종류별 하중 분할은 0 → **우리 f_AM (AM–AM 망 σzz 몫 · 상별 virial) 과 견줄 양이 원문에 없다**.  게다가 그 9.73 % 는 같은 그림의 P(f) 로 재현되지 않는다 (f = 1 바로 위 세 칸만 0.128 [판독 · 카드 산술]).
> ③ **도막 응력 σzz (식 9 · Love–Weber 꼴) 이 판 압력의 0.095 배** (40 %: 25.55 ↔ 270.5 MPa [판독]) — 같은 꼴을 쓴 `zhang2026_…` 은 σzz/판 압력 ≈ 1.0 [다른 카드] → 이 논문의 응력 값은 정규화 부피가 다르거나 (미기재) 다른 양이다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 타이위안 과기대 (Taiyuan Univ. Sci. Tech.) 그룹이 NMC532 액체계 양극을 실험실 롤 프레스로 압하율 10–40 % 까지 압연하고, 같은 압하율을 **EDEM 2021 + EEPA (탄소성 점착 접촉 법칙 · 단단한 구)** 의 100 µm 입방 RVE (옆 주기 · **강철 평판** 이 롤 대신) 로 따라 누른 뒤, 그 접촉력을 **axdt 파일로 ANSYS 2022 의 Al 박 RVE (100 × 100 × 17 µm · C3D8R · 정적 · 바닥 고정)** 에 한 방향으로 옮겨 집전체 응력 · 박힘을 계산했다 — DEM 쪽 힘 사슬 통계 (접촉 쌍 수 · 직물 편차 · P(f) · 강한 사슬 수 몫 · 도막 응력) 와 FEM 쪽 집전체 응력 (최대 256.5 MPa @ 40 %) 을 실험 CLSM · SEM 의 박힘 구멍과 견주고, 입경 (7 · 9 · 13 µm) · 입도 폭 (σ 0.5 · 2 · 4) 을 바꿔 '최적 입경 9.9 µm' 를 냈다.
⇒ **고른 의도 가운데 'DEM → FEM 넘김 선례 (h)' 는 채운다 (한 방향 · 압력 단계마다 따로 · 누른 채의 접촉력).  'force-chain 정량' 은 일부 (통계는 있으나 정의 넷이 서로 · 그림과 어긋남).  'AM–AM 하중 분담과 비교' 와 'he2026 의 입자–Al 마찰 출처' 는 없음.**

| 1저자가 꼭 뽑으라고 한 것 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 전극 · 활물질 · 입경 분포 · 조성 · 바인더 · 도전재 표현 | **양극** · *"LiNi0.5Mn0.3Co0.2O2 (NMC, ρ = 2.42 g/cm³)"* · CB (ρ 1.6) · PVDF (ρ 1.76) = **90 : 5 : 5** (행성 진공 혼합 20 min → NMP · 저속 1 h + 고속 10 h · 점도 15.8–491 Pa·s *"as reported in the literature [81]"*) · AM **D10 / D50 / D90 = 3.5 / 7.2 / 13.8 µm** (레이저 회절) · CB **D50 2.5 µm [80]** · 전부 MTI · **17 µm Al 박** 위 도포 (적외선 건조 평판 도포기) · 오븐 85 °C 6 h · 건조 뒤 **≈100 µm** (p.3) · DEM: AM · CB = **단단한 구 (측정 입도 그대로 생성)** · **PVDF = 입자 없음** — 표면 에너지 γ 와 접착 f₀ 로만 (*"indirectly represented by adjusting the surface energy parameter (γ) and the adhesion force (f0) in the contact model [27]"* p.5) · 입경 실험 = 7 µm (D10/50/90 3.6/6.9/11.5) · 9 µm (7.0/9.2/12.0) · 13 µm (9.9/12.9/16.7) 세 전극 (p.3) · DEM = *"D50 values as target diameters"* (p.11) · 입도 폭 계산 = CB 2.5 µm 고정 (p.13) | [인쇄] p.3 · p.5 · p.11 · p.13 |
| ② ★ DEM 접촉 모델 (식 번호별) | **EEPA** (*"Edinburgh Elasto-Plastic Adhesive contact model"* [27, 84, 85] p.4) — 부록 A: 식 A.1 R* · A.2 m* · A.3 1/E* · A.4 1/G* (⚠ 분모가 반지름으로 인쇄) · A.5 F_N = (F_hys + F_nd) u · ★ **A.6 세 가지** (f₀ + k₁δⁿ / f₀ + k₂(δⁿ − δᵖ) (⚠ 인쇄) / f₀ − k_adhδⁿ) · A.7 **λp = 1 − k₁/k₂ = δp/δmax** · A.8 f_min = πγϕr (⚠ ϕ 정의 없음) · A.9 F_t = F_ts + F_td · A.10 구름 토크 τ_i = −μr\|F_hys\|R_iω_i · A.11 F_ct ≤ μ\|F_hys + k_adhδⁿ − f₀\| — 식 크롭 11 장 + 부록 통째 1 장 | [인쇄] p.16–17 · `eq_A01`–`eq_A11` · `eq_A_block_…` |
| ③ ★ 매개변수 표 (E · ν · 반발 · 마찰 · 구름 · 출처) | 표 1 (p.5): AM **4750 kg/m³ [75] · E 142 GPa [72] · ν 0.25 [73]** · CB 2250 [75] · **0.45 GPa** [74] · 0.2 [73] · AL 2700 [75] · 68.9 GPa [72] · 0.33 [73] · Steel 7800 [75] · 182 GPa [72] · 0.3 [73] · 입자–입자 μs **0.25** · μr **0.01** · COR **0.25** [25] · γ AM–AM **8** [86] · CB–CB **60** · AM–CB **20 J/m²** [87] · **λp 0.96** [27] · f₀ **10⁻⁵ N** [88] · ⚠ **없는 것**: 입자–벽 (강철 판 · Al) 접촉 줄 전부 · k₁ · k₂ · k_adh · n 의 값 · 감쇠 · 시간 간격 · 입자 수 · 판 속도 · 시드 수 | [인쇄] 표 1 · `tab_1.png` · [미확인] |
| ④ ★ 입자–Al 마찰 계수 · 근거 (he2026 L99 의 [41]) | **없음** — 표 1 에 입자–Al 줄이 없고 19 쪽 글자 층에 *"0.61"* · *"0.65"* · *"JKR"* · *"1.5 J"* 0 건.  이 논문 자신의 [41] = Thakur · Ooi · Ahmadian 2016 (*Powder Technol.* 293, 130–137) — p.2 의 *"these ratios typically range from 10 % to 35 % [41,42]"* 에만 인용 (같은 문헌이 [85] 로 한 번 더 실림) | [인쇄] 표 1 · p.2 · 참고문헌 |
| ⑤ 압연 조건 | **MSK-2300A** 유압 균형 전동 롤 프레스 · 롤 지름 **200 mm** · 길이 330 mm · **상온** · **1 m/min** · 간극 = 손잡이 (±0.6 µm) + 틈 게이지 (±1.5 µm · 롤 축 여러 자리 [82]) · 압연 뒤 두께 = 마이크로미터 (0.1 µm · 여러 자리) · 압하율 ε = (H₀ − H_c)/H₀ × 100 % (식 3) · **10 / 20 / 30 / 40 % ↔ 선하중 14 / 110 / 268 / 530 N/mm** (p.6) · DEM = 판 압축 근사 (식 1 θ = cos⁻¹((R − S)/R) · 식 2 v_Plate = v_Roll cos θ · 판 속도 값 없음) | [인쇄] p.3 · p.4 · p.6 |
| ⑥ DEM ↔ FEM 연계 | **한 방향** — DEM 의 집전체 = *"rigid geometry"* stl · EDEM–ANSYS Workbench 가 **접촉력 (법선 + 접선) 과 좌표** 를 axdt 파일로 FEM 절점에 · **3 µm 균일 계면 격자 = 접촉점 ↔ 절점 일대일** · **압력 단계마다 DEM 을 따로** 돌려 같은 FEM (같은 격자 · 재료 · 경계) 에 건다 · FEM = Al 박 RVE 100 × 100 × 17 µm³ · **C3D8R** · *"aluminum was assigned as the material"* (구성식 · 항복 응력 미기재) · 바닥 고정 · **정적 해석** · FEM 변형은 DEM 으로 안 돌아온다 | [인쇄] p.5–6 · 그림 4 · [미확인] |
| ⑦ ★ 힘 사슬 정의 · 문턱 · 정량 | **'힘 사슬 밀도' = 세기와 상관없이 모든 접촉 쌍** (p.7) → **23,940 · 31,484 · 36,260 · 41,816** (10–40 % · 그림 6l 인쇄) · 본문 *"76.5 % rise"* (인쇄 수로는 +74.7 % [카드 산술]) · 방향 = 직물 텐서 F_ij = δ_ij/3 + F′_ij (식 6 [99]) · **F′zz 0.048 → −0.03** · 세기 = **f = F_i / 평균 (식 7) · 문턱 f = 1** [100, 101] · P(f) = (1/N)Σn_k (식 8 · n_k · N = *입자* 수) · 분포 폭 38.34 → 26.11 · *"contact force magnitude is increased to 1.25 mN"* · **강한 사슬 몫 21.49 · 11.06 · 10.59 · 9.73 %** (그림 6k 인쇄) · 도막 응력 σ (식 9 [102, 103]) **35 → 182.6 MPa (+422 %)** · **없음**: 사슬 판정 (각 · 길이 · 이어짐) · 사슬에 든 입자 몫 · 사슬이 지는 하중 몫 · 시드 반복 | [인쇄] p.7–9 · 그림 6 · [판독] |
| ⑧ ★ AM–AM (쌍 종류별) 하중 몫 · 우리 f_AM 규약 대조 | **없음** — 상별 · 쌍 종류별 분할 0 · 식 9 는 **대칭 두 입자 (Love–Weber / Christoffersen) 꼴** 로 우리 (b) 상별 virial 과 같은 꼴이지만 **계 전체만** 보고 · σzz (그림 6m) 3.09 → 25.55 MPa [판독] = 판 압력의 0.095–0.25 배 [카드 산술] → 몫으로도 못 쓴다 · '강한 사슬 몫' = 수의 몫 | §7-2 · [판독 · 카드 산술] |
| ⑨ 집전체 손상 · 실험 검증 | FEM 최대 응력 **256.5 MPa** (40 % · 그림 7l · p.11 · 응력 = Mises (그림 10p · 11i 축)) · 구멍 수 (그림 8m) **≈148 / 443 / 546 / 640** (10–40 % [판독]) ↔ 본문 *"increases rapidly to 379"* (20 %) · 최대 깊이 · 지름 계산 ↔ 실험 (그림 8n–o [판독]) 0.80 ↔ 0.96 · 1.29 ↔ 1.25 · 1.84 ↔ 2.32 µm · 2.90 ↔ 3.81 · 3.86 ↔ 5.51 · 6.42 ↔ 7.80 µm · 본문 *"simulated values … exceed the experimental values"* (그림은 6 칸 중 5 칸 실험이 큼) · 편차 0.47 · 1.68 µm (인쇄) · DEM 법선 겹침 최대 **8.47 × 10⁻⁴ mm** (그림 9 색 막대) · 입경 7 → 13 µm: 응력 집중점 **655 → 343** · 최대 응력 **170 → 245 MPa** · '최적' **9.9 µm** (417 개 · 189 MPa) · 실험 = SEM (Zeiss Sigma 300) · CLSM (RTEC LAMBDA · NMP + 초음파로 도막 제거 · 선 주사) · **손상 문턱 없음** (저자) | [인쇄] p.10–15 · [판독] |
| ⑩ 압연 전후 기공률 · 두께 · 밀도 (누른 채 / 뺀 뒤) | 두께 100 → 90 / 80 / 70 / 60 µm (식 3 · DEM 경로 100 → 60 µm) · 기공률 (그림 5d [판독]) DEM **52.0 → 48.3 → 36.5 → 27.6 → 18.9 %** · 실험 **50.0 → 45.4 → 37.7 → 25.9 → 16.9 %** (0–40 %) · 실험 = 압연 **뒤** 마이크로미터 두께 + 질량 · 진밀도 (*"ratio of solid volume to the coating's geometric volume [79]"* p.7) = **뺀 뒤** · DEM 기공 연산자 · 상태 (누른 채 / 뺀 뒤) **미기재** · 되돌아옴 (springback) **없음** (λp 0.96 → 접촉 겹침의 4 % 만 되돌아옴 [카드 산술 · n = 1]) | [인쇄] p.6–7 · [판독] · [미확인] |
| ⑪ 저자 한계 · he2026 L689 대조 | ① *"Since the platen-based DEM model cannot capture the full dynamics of calendering, future research will focus on the effects of roller rotation …"* ② *"the lack of a quantifiable threshold for contact damage penetration into the current collector necessitates further investigation through mechanical testing"* (p.16) ③ DEM 의 단순 상호작용 · 구 형상 → 덜 치밀 (p.7) ④ 집전체 거칠기 미반영 · 손 선 따기 편향 (p.11) · he2026 L689 *"진짜 force-chain 정량 논문 · 우리 AM-AM 하중분담과 비교 가능한 유일 후보"* → **일부 / 없음** (§0-1) | [인쇄] |
| ⑫ 우리 쪽 (d · h · 하중 분담 ② · 힘 사슬 frame[5]) | d = 없음 · h = 채움 (한 방향) · MPM DO-NOT ② (AM 하중 분담) 의 문헌 값 = 없음 · 힘 사슬 = DEM 고유 관측량 (frame[5]) 의 정의 · 함정 · 재료 · 공정 차이 = **액체계 LIB 양극 · 롤 압연 (평판 근사) · SE 없음** ↔ **황화물 복합 양극 · 다이 단축 300 MPa · AM + LPSCl** (판정 없이 나란히 — §7 · §8) | §7 · §8 |

⛔ **한정어 (떼지 말 것)**: ① **NMC532 액체계 LIB 양극 · SE 없음** — AM 이 고체 부피의 ≈79 % 이고 무른 상은 CB (E 0.45 GPa) 뿐 ② **롤을 평판으로 근사** — 롤 곡률 · 회전 · 접선 · 출구 되돌아옴 없음 ③ **한 방향 DEM → FEM · 정적** — DEM 의 집전체는 단단한 stl (박힘 = 겹침), FEM 의 변형 (구멍) 은 DEM 으로 돌아오지 않는다 ④ **'힘 사슬 밀도' = 모든 접촉 수 · '강한 사슬 몫' = f > 1 의 수 몫** — 하중 몫 아님 ⑤ **σ (전체 응력) 정의 없음 · σzz ≈ 판 압력의 1/10** ⑥ 벽 접촉 · k · n · 감쇠 · 시간 간격 · 입자 수 미기재 ⑦ 그림 값은 판독 (300 dpi 래스터) ⑧ 본문 ↔ 그림 · 식 어긋남 여럿 (§3-11).
⇒ **절대값 전이**: 힘 · 응력 · 기공 · 구멍 크기 · '최적 9.9 µm' 는 우리 계 (황화물 복합 · 다이 가압) 로 **전이 0 건**.  가져올 수 있는 것은 **정의 · 연산자 · 점검** — P(f) 와 f = 1 문턱 · 직물 편차 F′ · 식 9 의 상별 분할 (우리 (b)) · 한 방향 DEM → FE 넘김의 꼴과 그 한계 · σzz(LW)/판 압력 점검 · 고체 보존 기공 점검 · 식 1 의 접촉각.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-27 의 '왜' 칸)

의도 원문: *"d · h — '진짜 force-chain 정량 논문 · 우리 AM-AM 하중분담과 비교 가능한 유일 후보' · DEM-FEM (he2026 L689) · he2026 의 입자–Al 마찰 계수 출처 [41] (L99)"* (가리킨 카드 = `he2026_dem_calendering_inhomogeneity_areal_density` L689 · L99)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "d" (질문 d: 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍) | **없음 (정성 한 줄)** | 무른 상 = CB (E 0.45 GPa · 5 wt% · AM 1 개당 ≈2.8 개 [카드 산술 · D50 · 표 1 밀도]) 뿐 · SE 없음 · **상별 · 쌍 종류별 하중 몫 0** · 재밍 = 정성: *"The particles close to the collector are restricted in movement, exhibiting almost no displacement due to the significant reduction of local porosity after compression … However, they still form part of the force chain structure by transmitting contact forces through static interparticle contacts."* (p.11 · 그림 7d–f) · 조건 = 평판 근사 · 압력 단계마다 따로 누른 상태 · 상온 |
| "h" (질문 h: DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점) | **채움 (한 방향)** | §3.2 (p.5–6 · 그림 4 · `txt_p5_p6_dem_limit_coupling_axdt_3um_one_way.png`): EDEM 2021 → axdt (접촉력 법선 + 접선 · 좌표) → ANSYS 2022 Al 박 RVE · 3 µm 일대일 · **압력 단계 (10 · 20 · 30 · 40 %) 마다 따로 DEM → 같은 FEM** (= 누른 채의 접촉력 상태를 넘김) · FEM 결과는 DEM 으로 돌아가지 않음 · 양방향 선례 = [29] Song 2023 (*"a DEM-FEM bidirectional coupled model"* p.2 · 카드 없음 · n 후보) |
| "진짜 force-chain 정량 논문" | **일부** | 있음: 접촉 쌍 수 (그림 6l 인쇄) · 직물 편차 (식 6 · 그림 6j) · P(f) (식 7–8 · 그림 6i) · 강한 사슬 몫 (그림 6k 인쇄) · 도막 응력 (식 9 · 그림 6m) · 3D 사슬 그림 (그림 6a–d · 7g–i · 10d–f) · **없음**: 사슬 판정 (각 · 길이 · 이어짐 · 공선) · 사슬에 든 입자 몫 · 사슬이 지는 하중 몫 · 시드 반복 · ⚠ **정의 어긋남 넷** — (i) 9.73 % 가 P(f) 의 f > 1 합으로 재현 안 됨 (ii) P(f) 분모 = 입자 수 (iii) F′zz 감소를 '수직 정렬' 로 읽음 (iv) σ 정의 없음 · σzz ≈ 판 압력의 1/10 (§3-6 · §3-11) |
| "우리 AM-AM 하중분담과 비교 가능한 유일 후보" | **없음** | AM–AM · AM–CB · 입자–벽 접촉의 하중 분할 **0** · 식 9 = 우리 (b) 상별 virial 과 **같은 대칭 두 입자 꼴** 이지만 **계 전체만** 보고 · σzz(40 %) **25.55 MPa = DEM 판 압력 270.5 MPa 의 0.095** [판독 · 카드 산술] → 몫 · 비로 옮길 수 없다 · '강한 사슬 몫' = 접촉 (또는 입자) 의 **수** 몫 (§7-2) |
| "DEM-FEM (he2026 L689)" | **채움** | 위 'h' 행 · 그림 4 (결합 고리) · 7j–l (집전체 응력) · 8a–c (집전체 '변형' 지도) · 10g–i · 10p · 11i |
| "he2026 의 입자–Al 마찰 계수 출처 [41] (L99)" | **없음** | 표 1 (p.5 · `tab_1.png`) = 재료 넷 (AM · CB · AL · Steel) 의 ρ · E · ν + **입자–입자 8 줄뿐** — 입자–Al · 입자–강철 마찰 · 구름 · 반발 · 점착 줄 **없음** · 19 쪽 글자 층 전수: *"0.61"* · *"0.65"* · *"0.12"* · *"JKR"* · *"1.5 J"* **0 건** · 이 논문의 [41] = Thakur · Ooi · Ahmadian 2016 (p.2 압하율 범위 문장에만) |

**가리킨 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `he2026_…` **L99** | 입자–Al 집전체 μ / 구름 / COR **0.61 / 0.12 / 0.65** · *"[41] Du 2025"* | 없음 (표 1 에 입자–Al 줄 없음 · 글자 층 0 건) | **없음** (카드 문제 ①) |
| `he2026_…` **L100** | JKR 표면에너지 **1.5 J m⁻²** · *"[41]"* | 없음 — 이 논문의 접촉 법칙은 EEPA (JKR 아님) · 표면 에너지는 입자–입자 8 · 60 · 20 J/m² 뿐 | **없음** (카드 문제 ①) |
| `he2026_…` **L98** | f₀ **1.5 × 10⁻⁵ N** · *"[39–41]"* | 이 논문 표 1 f₀ = **10⁻⁵ N** (출처 [88] Schreiner 2023) | **다름** — [41] 이 이 논문이라면 값이 다르다 (카드 문제 ②) |
| `he2026_…` L92–L96 | 입자–입자 μ **0.25** · 구름 **0.014** · COR **0.25** · 표면에너지 **8 J m⁻²** · λp **0.96** · *"[39] Ge 2022 · [39,40]"* | 이 논문 표 1: μ 0.25 · μr **0.01** · COR 0.25 (모두 [25] Ge 2022) · γ AM–AM 8 ([86] Schreiner 2020) · λp 0.96 ([27] Zhang 2022) | 값 4/5 같음 · 구름 0.014 ↔ 0.01 · 출처 표기 다름 — he2026 원문 ([39] · [40]) 은 이 트리에 PDF 가 없어 확인 불가 (관찰 · 카드 문제 아님) |
| `he2026_…` L80–L83 (참고) | 표 1: NCM 4570 · 47 · 0.25 · SP 2250 · 0.45 · 0.20 · AL 2700 · 70 · 0.33 · Steel 7800 · 200 · 0.30 | 이 논문 표 1: AM **4750** · **142** · 0.25 · CB 2250 · 0.45 · 0.2 · AL 2700 · **68.9** · 0.33 · Steel 7800 · **182** · 0.3 | 관찰 — he2026 의 SP 줄 · 밀도 · ν 는 이 논문 표 1 과 같은 수 (E 와 NCM 밀도만 다름) · 출처 관계는 원문 없이 판정하지 않음 |
| `he2026_…` **L368** | *"그들의 ref [41] Du 2025 … 가 진짜 force-chain 논문 → 백로그 후보"* · 우리 f_AM 두 규약 (AM–AM 0.517 … · phase 0.726 …) 칸 | 힘 사슬 통계 있음 · **상별 하중 몫 없음** | **일부** — 'f_AM 과 비교' 는 원문으로 서지 않는다 (카드 문제 ③) |
| `he2026_…` **L689** (N5) | *J. Energy Storage* 138, 118688 · *"Force chain-induced collector damage in calendering: a DEM-FEM study"* · *"진짜 force-chain 정량 논문. 우리 AM-AM 하중분담과 비교 가능한 유일 후보"* | 서지 ✓ (원문 제목 *"… A DEM-FEM study"* — 대소문자만) · 내용 = 위 표 | 서지 **채움** · 내용 **일부 / 없음** (카드 문제 ③) |

⇒ **의도 대조 결과: 채움 (h · DEM → FEM 한 방향 넘김의 선례 · 서지) · 일부 (force-chain 정량 — 수 · 방향 · P(f) · 강한 사슬 수 몫은 있으나 정의가 서로 · 그림과 어긋남) · 없음 (d · AM–AM 하중 몫 · he2026 L99 · L100 의 입자–Al 마찰 · JKR 값 — 이 논문에 없다 · L98 의 f₀ 는 다른 값).**

---

## 1. 한 줄 요약

NMC532 : CB : PVDF = 90 : 5 : 5 액체계 양극을 압하율 10 → 40 % 로 압연하면 DEM 에서 접촉 쌍이 23,940 → 41,816 으로 늘고, 직물 편차 F′zz 가 +0.048 → −0.03 으로 바뀌며, '강한 사슬' (평균 힘 초과 접촉) 의 수 몫이 21.49 → 9.73 % 로 줄고, 도막 '전체 응력' σ 가 35 → 182.6 MPa 로 오른다 — 저자는 30 % 를 넘으면 강한 사슬이 집전체 쪽으로 옮겨 Al 박 응력 (최대 256.5 MPa) 과 박힘 구멍을 만든다고 읽고, 큰 입자 · 넓은 입도가 집중점은 줄이되 점마다 응력을 키운다며 '최적 입경 9.9 µm' 를 낸다 — 계산 사슬은 평판 근사 DEM → 한 방향 정적 FEM 이다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 · 소속 | 위 머리 상자 (타이위안 과기대 3 · 동북대 1 · 산시 직업대 1) |
| 학술지 | *Journal of Energy Storage* **138** (2025) **118688** · 19 쪽 · ISSN 2352-152X · © 2025 Elsevier Ltd |
| DOI | `10.1016/j.est.2025.118688` (p.1 · PDF 메타데이터 *"Journal of Energy Storage, 138 (2025) 118688. doi:10.1016/j.est.2025.118688"*) |
| 이력 | 접수 2025-06-05 · 수정 2025-08-17 · 승인 2025-09-26 · 온라인 2025-10-04 |
| 연구유형 | 계산 (DEM + 한 방향 FEM) + 실험 (압연 · SEM · CLSM · 두께 · 질량) |
| 계산 규모 | DEM RVE 100 × 100 × 100 µm³ (x · y 주기) · FEM RVE 100 × 100 × 17 µm³ · 3 µm 계면 격자 · 입자 수 · 계산 시간 · 시간 간격 · 시드 수 **[미확인]** |
| 보충 자료 | 없음 (부록 A = DEM 접촉 식) · 원자료 *"on request"* |
| 서지 메모와의 차이 | 후보 표 N-27 *"Du 2025 (J. Energy Storage 138, 118688) "Force chain-induced collector damage in calendering: a DEM-FEM study""* (저자 성만) ↔ 원문 저자 다섯 (He Du · Yuxin Zhang · Xiaozhong Du · Kaiyue Yang · Le Zhao) · 제목 *"… A DEM-FEM study"* (대소문자만) · 권 · 논문 번호 · 연도 · DOI 같음 · he2026 L689 서지도 같음 |

### 계보 — 정본 litdb 안 액체계 LIB 양극 압연 DEM (이 카드가 더하는 자리)

| 카드 | 접촉 · 결합 | 집전체 처리 | 힘 사슬 정량 | 형상 소성 |
|---|---|---|---|---|
| `sangros2019_dem_calendering_lib_electrode` (= 이 논문 [75]) | Thornton–Ning + bond [다른 카드 · he2026 계보 표] | — | — | ✗ |
| `schreiner2020_dem_calendering_lib` (= [86]) | EEPA + bonding [다른 카드] | — | — | ✗ |
| `lyu2025_3d_dem_drying_calendering_lib` (= [90]) | PFC3D bond [다른 카드 · he2026 계보 표] | — | — | ✗ |
| `he2026_dem_calendering_inhomogeneity_areal_density` | EEPA (bond 없음) + JKR 집전체 [다른 카드] | 벽 (JKR) | 정량 0 (색 막대뿐) [다른 카드 L368] | ✗ |
| `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` | 탄성 구 + 평행 결합 [다른 카드] | — | 정성 (굵은 사슬 관통 30–35 %) [다른 카드] | ✗ |
| `zhang2026_xct_dem_cathode_calendering_peel_calibration` | Hertz–Mindlin + 평행 결합 · 입자–집전체 결합 박리 보정 [다른 카드] | 벽 (결합) · 매립 = 겹침 | 사슬 그림 + 응력 텐서 (σzz/판 ≈ 1.0) [다른 카드] | ✗ |
| **이 논문 (Du 2025)** | **EEPA (bond 없음) · PVDF = γ · f₀** | **벽 (단단한 stl) → 한 방향 FEM (Al 박 탄성체 · 정적)** | **접촉 수 · F′ · P(f) · 강한 사슬 수 몫 · σ (정의 결손)** | **✗** |

⇒ 일곱 편 모두 **입자 = 단단한 구 (또는 고정 형상) · 소성 = 접촉 법칙 · 입자 형상 변화 0** — frame[5] 분업 (DEM = 망 · 패킹 / MPM = 형상 소성) 의 같은 쪽.  이 논문의 고유 자리는 **집전체를 FEM 연속체로 넘긴 것 (한 방향)** 과 **힘 사슬 통계를 이름 붙여 낸 것**.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 전극 · 재료 · 압연 (p.3 · `txt_p3_materials_nmc532_psd_ratio_al17_roll_press.png` · `txt_p3_three_particle_size_groups_7_9_13um.png`)

| 양 | 값 | 표지 |
|---|---|---|
| 활물질 | LiNi0.5Mn0.3Co0.2O2 (NMC532) · *"ρ = 2.42 g/cm³"* (p.3 · 표 1 의 4750 kg/m³ 과 다름 — 탭 · 겉보기 밀도로 보임 [카드 해석]) | [인쇄] |
| 도전재 · 바인더 | CB (*"ρ = 1.6 g/cm³"*) · PVDF (*"ρ = 1.76 g/cm³"*) | [인쇄] |
| 조성 | **NMC : CB : PVDF = 90 : 5 : 5** (행성 진공 혼합기 20 min → NMP · 저속 1 h · 고속 10 h) | [인쇄] |
| 고체 부피 몫 (표 1 밀도 AM 4750 · CB 2250 + PVDF 1760) | AM **78.9** · CB **9.3** · PVDF **11.8 %** | [카드 산술] |
| AM 입도 | D10 / D50 / D90 = **3.5 / 7.2 / 13.8 µm** (레이저 회절) | [인쇄] |
| CB 입도 | D50 **2.5 µm** *"[80]"* (같은 그룹 Yang 2024 인용 — 측정인지 옮긴 값인지 문장상 모호) | [인쇄] |
| CB 수 / AM 수 | ≈ **2.8** (D50 · 표 1 밀도 · 단분산 가정) | [카드 산술 · 가정] |
| 슬러리 점도 | 15.8–491 Pa·s *"as reported in the literature [81]"* (측정 아님) | [인쇄] |
| 집전체 | **17 µm Al 박** | [인쇄] |
| 건조 | 적외선 건조 평판 도포기 → 오븐 **85 °C 6 h** | [인쇄] |
| 압연 전 도막 두께 | **≈100 µm** | [인쇄] |
| 롤 프레스 | MSK-2300A (유압 균형 · 전동) · 지름 **200 mm** · 길이 330 mm · **상온** · **1 m/min** | [인쇄] |
| 간극 · 두께 측정 | 손잡이 ±0.6 µm · 틈 게이지 ±1.5 µm (롤 축 여러 자리 [82]) · 압연 뒤 마이크로미터 0.1 µm (길이 · 폭 여러 자리) | [인쇄] |
| 압하율 ↔ 선하중 | **10 · 20 · 30 · 40 % ↔ 14 · 110 · 268 · 530 N/mm** (p.6) | [인쇄] |
| 입경 실험 세 전극 | 7 µm (D10 3.6 · D50 6.9 · D90 11.5) · 9 µm (7.0 · 9.2 · 12.0) · 13 µm (9.9 · 12.9 · 16.7) — 같은 배합 · 같은 압연 · *"D50 of commercially available materials"* | [인쇄] |
| 단면 · 표면 관찰 | 100 mm × 50 mm 시편 · SEM (Zeiss Sigma 300) · 도막 = NMP + 초음파 세척으로 제거 → CLSM (RTEC LAMBDA) 거칠기 · 단면 선 | [인쇄] p.3 |
| 면적 하중 (mg/cm²) · 전극 밀도 · 양면 / 단면 | **[미확인]** (원문에 없음) | — |

### 3-2. ★ DEM 매개변수 — 표 1 (p.5 · `tab_1.png`)

| 줄 | 값 | 원문 출처 번호 | 출처 문헌 (원문 목록 그대로 · 줄임) |
|---|---|---|---|
| AM 밀도 | 4750 kg/m³ | [75] | Giménez 2019 *Powder Technol.* 349 = `sangros2019_…` (그 카드: ρ_NMC 4.75 g/cm³ [다른 카드 L37]) |
| AM 영률 | **142 GPa** | [72] | Stershic 2015 *J. Power Sources* 297 (직물 텐서 DEM 논문) — `sangros2019_…` 도 E_NMC 142 [다른 카드 L34] |
| AM ν | 0.25 | [73] | Giménez 2018 *Adv. Powder Technol.* 29 |
| CB 밀도 · E · ν | 2250 · **0.45 GPa** · 0.2 | [75] · [74] · [73] | [74] = Lundkvist 2023 *Powder Technol.* 425 |
| AL 밀도 · E · ν | 2700 · 68.9 GPa · 0.33 | [75] · [72] · [73] | |
| Steel 밀도 · E · ν | 7800 · 182 GPa · 0.3 | [75] · [72] · [73] | |
| 입자–입자 정지 마찰 μs | **0.25** | [25] | Ge 2022 *Powder Technol.* 403 117366 |
| 구름 마찰 μr | **0.01** | [25] | 〃 |
| 반발 계수 | **0.25** | [25] | 〃 |
| 표면 에너지 AM–AM | **8 J/m²** | [86] | Schreiner 2020 *Procedia CIRP* 93 = `schreiner2020_…` — ⚠ 그 카드는 NMC–NMC **5** · PVDF–NMC 20 · PVDF–PVDF 60 J/m² [다른 카드 L42] |
| 표면 에너지 CB–CB · AM–CB | **60 · 20 J/m²** | [87] | Schreiner 2021 *Procedia CIRP* 104 (카드 없음) — 수는 `schreiner2020_…` 의 PVDF–PVDF 60 · PVDF–NMC 20 과 같다 [다른 카드] |
| 접촉 소성비 λp | **0.96** | [27] | Zhang 2022 *Powder Technol.* 409 117828 (카드 없음) |
| 상수 접착 f₀ | **10⁻⁵ N** | [88] | Schreiner 2023 *Energy Technol.* 11 2200442 (= [82] = [93] 같은 문헌) |
| ⚠ **표에 없는 것** | 입자–강철 판 · 입자–Al 벽 접촉 (μ · μr · COR · γ) · k₁ · k₂ · k_adh · n · 감쇠 · 시간 간격 · 입자 수 · 판 속도 · 시드 수 · 결합 (bond) | — | **[미확인]** |

- [카드 산술] 같은 두 AM 구의 접촉 E* = E/(2(1 − ν²)) = **75.7 GPa** (우리 AM 140 GPa · ν 0.25 → 74.7 GPa [우리 — CLAUDE.md · `devasconcelos2019_…` §7 이 옮긴 `input_real_14.liggghts` L29–30]) · AM–Al 51.2 · AM–강철 86.2 · CB–CB 0.234 GPa.
- [카드 산술] λp = 1 − k₁/k₂ = 0.96 ⇒ **k₂ = 25 k₁** · δp/δmax = 0.96 (n = 1 일 때 — 원문은 n 값을 적지 않는다; 비선형이면 δp/δ = C_p^(1/n) [다른 카드 `morrissey2013_…` L39]) → 접촉 겹침의 **4 %** 만 되돌아오는 매우 소성적인 접촉.  `schreiner2020_…` 의 λ_P = NMC–NMC 0.8 · PVDF–NMC 0.9 · PVDF–PVDF 0.975 → 0.985 [다른 카드 L41] 와 같은 자릿수.
- ⚠ he2026 의 같은 표 (EEPA · μ 0.25 · COR 0.25 · 8 J/m² · λp 0.96) 와 **값 넷이 같다** — 출처 표기만 다르다 (§0-1).

### 3-3. ★ 접촉 법칙 — 부록 A (p.16–17 · `eq_A01`–`eq_A11` · `eq_A_block_eepa_appendix_with_text.png`)

| 식 | 인쇄 꼴 | 뜻 · 관찰 |
|---|---|---|
| A.1 | R* = r_i r_j / (r_i + r_j) | 등가 반지름 (*"contact radius r_i and r_j"* 로 적힘 — 입자 반지름의 뜻) |
| A.2 | m* = m_i m_j / (m_i + m_j) | 등가 질량 |
| A.3 | 1/E* = (1 − ν_i²)/r_i + (1 − ν_j²)/r_j | ⚠ **분모가 반지름 r** 로 인쇄 — 표준 꼴은 E_i · E_j [카드 관찰] |
| A.4 | 1/G* = (2 − ν_i)/r_i + (2 − ν_j)/r_j | ⚠ 같은 인쇄 (표준 꼴 분모 = G_i · G_j) [카드 관찰] |
| A.5 | F_N = (F_hys + F_nd) u | 법선력 = 이력 탄성력 + 법선 감쇠 · u = 접촉점 → 질량 중심 단위 벡터 |
| A.6 | F_hys = f₀ + k₁δⁿ (k₂(δⁿ − δ_pⁿ) ≥ k₁δⁿ) · f₀ + k₂(δⁿ − δᵖ) (k₁δⁿ > k₂(δⁿ − δ_pⁿ) > −k_adhδⁿ) · f₀ − k_adhδⁿ (−k_adhδⁿ ≥ k₂(δⁿ − δ_pⁿ)) | ★ 하중 · 제하 · 점착 분리 세 가지 · ⚠ 둘째 가지의 힘 항은 **δᵖ** (조건 쪽은 δ_pⁿ) 로 인쇄 · 점착 가지 지수도 **n** — EEPA 원전은 점착 가지에 따로 **X** [다른 카드 `morrissey2013_…` L31] |
| A.7 | λp = (1 − k₁/k₂) = δp/δmax | 접촉 소성비 · 원문 설명 *"represents the proportion of elastic to plastic deformation"* — 식은 최대 겹침 중 소성 몫 [카드 관찰] |
| A.8 | f_min = πγϕr | 최대 끌어당김 (r = 접촉 반지름 · γ = 표면 에너지) · ⚠ **ϕ 정의 없음** — EEPA 원전 f_min = πΔγψa · ψ = 3/2 [다른 카드 `morrissey2013_…` L32] |
| A.9 | F_t = F_ts + F_td | 접선 = 탄성 + 감쇠 (강성 식 · 값 없음) |
| A.10 | τ_i = −μr\|F_hys\|R_iω_i | 표준 구름 마찰 토크 (R_i = 접촉점까지 거리 · ω_i = 단위 각속도 벡터) |
| A.11 | F_ct ≤ μ\|F_hys + k_adhδⁿ − f₀\| | 점착을 넣은 쿨롱 미끄럼 한계 |

- 본문 (p.4): *"the Edinburgh Elasto-Plastic Adhesive contact model (EEPA) is used to reproduce the contact between the particles and the mechanical behaviors when undergoing large deformation [27,84,85]"* — **'큰 변형' 의 범위 (겹침 · 밀도 상한) 는 적지 않는다** (`txt_p4_eepa_large_deformation_claim.png`).  EEPA 는 항복 캡이 없는 조각 선형 이력 법칙이다 (*"항복점 없음"* [다른 카드 `morrissey2013_…` §3-5 · `schreiner2020_…` L71]).
- 부록 첫 문단: *"Unlike the classical Hertzian models, the EEPA model captures the transition from elastic to plastic behavior and the loading-unloading hysteresis induced by adhesion forces."* (p.16).

### 3-4. ★ 모델 · 경계 · 결합 (p.4–6 · 그림 3 · 4 · `txt_p4_platen_approximation_theta_rve_periodic.png` · `txt_p5_pvdf_implicit_fem_rve_c3d8r_static.png` · `txt_p5_p6_dem_limit_coupling_axdt_3um_one_way.png` · 식 1–2)

- **평판 근사**: Schreiner [82] 가 롤 회전의 접선력 · 회전 에너지가 *"vortex-like rearrangement"* 를 만든다고 했지만 *"this study focuses on the instantaneous normal force exerted by particles on the current collector during calendering, and thus uses a platen compression approximation"* · *"the maximum value of θ always remains less than 1° [75]"* (p.4).
  - [카드 산술] 식 1 θ = cos⁻¹((R − S)/R) · R = 100 mm (지름 200 mm) 로 S = 10 · 20 · 30 · 40 µm → **0.81 · 1.15 · 1.40 · 1.62°** · 1° 를 넘는 압하 = **S ≥ 15.2 µm** (압하율 ≥ 15 %).  [75] 의 1° 는 그 논문의 롤 (지름 430 mm · θ 0.66–0.96° [다른 카드 `sangros2019_…` L101]) 값이다.
  - 식 2 *"vPlate = vRollcosθ"* — 본문은 *"reaching its maximum at position A, dropping to zero at position B, and increases in reversed direction until position C"* 라 적는다.  cos θ 는 B (θ = 0) 에서 최대 → **본문 서술과 맞는 것은 연직 성분 v_Roll sin θ** [카드 관찰 · 판정 아님].  판 속도 값은 원문에 없다.
- **RVE**: 100 × 100 × 100 µm³ · 높이 100 µm = 실험 초기 도막 두께 · **x · y 주기 경계** (*"to prevent particle loss at the boundaries"*) · 강철 판 = 롤 면 · Al 박 = 집전체 · 입자는 측정 입도대로 생성 · EDEM 2021 · ANSYS 2022 (p.4).
- **바인더**: *"PVDF is not explicitly modeled as individual particles in the DEM simulations. Instead, the contribution of the PVDF binder to the mechanical behavior between particles is indirectly represented by adjusting the surface energy parameter (γ) and the adhesion force (f0) in the contact model [27]."* (p.5).
- **FEM**: *"a representative volume element (RVE) of the current collector was created with dimensions of 100 × 100 × 17 μm3 … meshed with C3D8R solid elements, and aluminum was assigned as the material. Surface loads were applied via the DEM–FEM coupling interface, and the bottom surface was fixed … A static analysis was performed"* (p.5).  ⚠ C3D8R 은 Abaqus 의 요소 이름 (ANSYS 에서의 대응 요소는 원문 없음 [카드 관찰]) · Al 의 구성식 (탄성 / 탄소성 · 항복 응력 · 경화) · 요소 수 · 두께 방향 격자 **[미확인]**.
- **결합 (§3.2)**: stl 이 DEM 안의 집전체 *"rigid geometry"* · DEM · FEM 격자를 계면에서 맞춤 · *"The EDEM-ANSYS Workbench coupling interface then transfers contact forces, including normal and tangential components, and coordinates from the DEM model to the FEM mesh nodes … exported from EDEM as an axdt file"* · *"A uniform interfacial mesh of 3 μm ensures one-to-one mapping between DEM contact points and FEM nodes"* · *"Separate DEM simulations are conducted for each pressure level"* → 각 axdt 를 *"identical FEM models with consistent mesh topology, material properties, and boundary conditions"* 에 건다 (p.6).
  - [카드 산술] 3 µm 계면 격자 = AM D50 7.2 µm 지름당 **2.4 칸** · D10 3.5 µm 은 1.2 칸 · 계산 구멍 지름 2.90 µm (20 %) 은 한 칸보다 작다.

### 3-5. 검증 — 압력–두께 · 기공률 (p.6–7 · 그림 5 · `fig_5c.png` · `fig_5d.png` · `txt_p6_compression_rate_line_loads_validation_3p66pc.png` · `txt_p7_porosity_method_spherical_morphology_limit.png`)

| 양 | 값 | 표지 |
|---|---|---|
| 압력 정의 | *"The calendering pressure was calculated from the total force applied to the electrode divided by the electrode's cross-sectional area."* — DEM 쪽 문장으로 읽힘 · 실험 쪽 (선하중 → MPa) 환산식 없음 | [인쇄] p.6 · [미확인] |
| DEM 점 (두께 µm, 압력 MPa) | (60.1, **270.5**) · (62.0, 247.5) · (65.0, 194.5) · (70.2, 137.9) · (75.2, 88.9) · (80.1, 52.0) · (85.0, 15.2) · (90.1, ≈4) | [판독] 그림 5c |
| 실험 점 | (59.7, **262**) · (68.2, 174.6) · (77.9, 80.7) · (85.7, 32.5) · (89.0, 19.8) — 점 다섯 (압하율 네 개와 수가 다름) | [판독] |
| 맞춤 곡선 60 · 70 · 80 · 90 µm | 실험 ≈ 257 · 150 · 70 · 21 · DEM ≈ 270 · 140 · 58 · 12 MPa (곡선 열 훑기 내삽) | [판독 · 카드 산술] |
| 원문 편차 | *"maximum deviation of 3.66 % observed in the low-pressure region (0–100 MPa)"* · *"When the pressure reaches 200 MPa, the deviation decreases to 0.073 %"* | [인쇄] p.6 |
| 판독 곡선의 상대 차 (DEM − 실험)/실험 | 60 µm **+4.9 %** · 70 µm −6.5 % · 80 µm **−17.7 %** · 90 µm **−41.7 %** — '3.66 %' 의 정의 · 기준점은 원문에 없다 · 두 곡선이 ≈66 µm (≈200 MPa) 에서 **교차** → '0.073 % @ 200 MPa' 는 교차점 근처의 차로 보인다 | [카드 산술 · 카드 해석] |
| 선하중 ÷ 접촉 길이 √(R·S) (R 100 mm) | 14 · **77.8** · 154.7 · **265.0** MPa (10–40 %) — 40 % 는 실험 점 262 와 1 % 안 · 20 % 는 실험 곡선 70 과 +11 % · 30 % 는 150 과 +3 % · 10 % 는 21 과 −33 % | [카드 산술 · 가정 = 원문에 없는 환산] |
| 기공률 (압하율 0 · 10 · 20 · 30 · 40 %) | DEM **52.0 · 48.3 · 36.5 · 27.6 · 18.9 %** · 실험 (*"SEM experiment"* 표지) **50.0 · 45.4 · 37.7 · 25.9 · 16.9 %** | [판독] 그림 5d |
| 고체 보존 기공 ε = 1 − (1 − ε₀)/(1 − CR) 와의 차 | DEM **+1.6 · −3.5 · −3.9 · −1.2 %p** · 실험 +0.9 · +0.2 · −2.7 · +0.2 %p — DEM 은 20–30 % 에서 같은 두께 · 고체량으로 낼 수 있는 값보다 3.5–3.9 %p 낮다 → DEM 기공 연산자 (두께 · 부피 · 겹침 셈) 가 판 간격 기준이 아니다 [카드 해석] | [카드 산술] |
| 기공 연산자 (실험) | *"The porosity of the electrode coating is determined from the ratio of solid volume to the coating's geometric volume [79]. The solid volume is calculated from the mass fractions and true densities … the coating geometric volume is derived from the measured surface density and coating thickness."* — 어느 진밀도를 썼는지 (p.3 의 2.42 인지 표 1 의 4750 인지) **[미확인]** | [인쇄] p.7 |
| 기공 연산자 (DEM) · 상태 (누른 채 / 뺀 뒤) | **[미확인]** | — |
| 저자 해석 | *"the simulated values are slightly higher than those of the experimental data … the simplified particle interactions and spherical morphology in the DEM model yield fewer compact contacts and simulated volume loss"* (p.7) — 판독으로는 20 % 에서만 DEM < 실험 | [인쇄] · [판독] |
| crude Heckel ln(1/ε) vs P (압력 = 맞춤 곡선 · 기공 = 그림 5d · 10–40 %) | 실험 P_y ≈ **236 MPa** (R² 0.999) · 20–40 % 만 234 · DEM ≈ **285 MPa** (R² 0.978) · 20–40 % 324 · DEM 점 압력 294 / 333 | [카드 산술] — ⚠ 압력 = 누른 채 · 실험 기공 = 뺀 뒤 · DEM 기공 상태 미상 → 섞인 상태의 어림 |

### 3-6. ★ 힘 사슬 — 밀도 · 방향 · 세기 · 도막 응력 (p.7–9 · 그림 6 · 식 4–9 · `fig_6l.png` · `fig_6jk.png` · `fig_6i.png` · `fig_6m.png` · `txt_p9_…` 넷)

| 양 | 정의 (원문) | 값 | 표지 |
|---|---|---|---|
| **'힘 사슬 밀도'** | *"force chain density refers to the density of the entire contact force network, including all particle contact pairs, regardless of force strength"* (p.7) | 접촉 쌍 **23,940 · 31,484 · 36,260 · 41,816** (10 · 20 · 30 · 40 %) · 본문 *"nearly linear increase from 23,940 to 41,816. This increase led to a 76.5 % rise"* | [인쇄] 그림 6l · p.9 |
| 〃 비 | — | 41,816/23,940 = **1.747 (+74.7 %)** ↔ 인쇄 +76.5 % · 단계비 1.315 · 1.152 · 1.153 (선형 아님) | [카드 산술] |
| 접촉력 크기 · 정규화 | 식 4 F_i = √(F²x,i + F²y,i + F²z,i) (*"Fi represents the arithmetic mean of the contact force"* 로도 적힘) · 식 5 F_normalised = F_i / max(F₁ … F_N) | — | [인쇄] p.8 |
| **방향 — 직물 텐서** | 식 6 F_ij = (1/3)δ_ij + F′_ij [99] (*"The fabric tensor Fij, a two-dimensional vector"* — 원문 표기) · 그림 6e–h 3D 장미 (색 = 접촉력 0–0.1 mN) | 본문 **F′zz 0.048 → −0.03** · 판독 F′xx / F′yy / F′zz = −0.025 / −0.028 / **+0.048** (10 %) · −0.013 / −0.017 / +0.029 (20 %) · +0.003 / 0.000 / −0.003 (30 %) · +0.019 / +0.011 / **−0.030** (40 %) (대각 합 \|Σ\| ≤ 0.004) | [인쇄] p.9 · [판독] 그림 6j |
| 〃 뜻 | ⟨n_z²⟩ = 1/3 + F′zz | **0.382 → 0.363 → 0.331 → 0.304** — 압하가 커질수록 법선이 z 쪽인 접촉의 몫이 **준다** | [카드 산술 · 표준 직물 정의 가정] |
| 〃 원문 해석 | *"the eigenvalue F′zz decreases from 0.048 to −0.03, suggesting that the dominant orientation of the force chains gradually shifts toward the negative Z-axis. This implies that particle contacts progressively align along the vertical loading direction"* · 앞 문단 *"fabric shape at low compression rates exhibits an approximately spherically symmetric structure. However, when the calendering rate reaches 30 %, the contact fabric gradually stretches in the normal direction, constituting a spindle-like structure"* | ⚠ 판독값과 반대 — 10 % 의 이방성 (F′zz +0.048) 이 넷 가운데 가장 크고, 30–40 % 는 z 쪽이 **덜** 하다 | [카드 관찰 · 판정 아님] |
| **세기 — 상대 접촉력** | 식 7 f = F_i / ((1/N)ΣF_i) · *"strong (f > 1) and weak (f ≤1) force chains. Therefore, the global mean contact force (f = 1) is adopted as the threshold"* [100, 101] | — | [인쇄] p.9 |
| P(f) | 식 8 P(f) = (1/N)Σ_k n_k · *"nk represents the number of particles within the kth contact force interval and N denotes the total number of particles"* | ⚠ 분모 = **입자 수** (접촉 수 아님) | [인쇄] p.9 |
| 분포 폭 · 최대 힘 | *"the range of contact force distribution narrows from 38.34 to 26.11"* · *"the contact force magnitude is increased to 1.25 mN"* (그림 7g–i 색 막대 0.25–1.25 mN) | | [인쇄] |
| P(f) 삽입 그림 (f 0–1.5) | 그림 6i 안의 확대 (f 0–1.5) | ε = 10 %: P 0.251 · 0.129 · 0.103 · 0.083 · 0.072 (f 0.08–0.75) · ε = 40 %: **0.058 · 0.167 · 0.162 · 0.128 · 0.097 · 0.074** (f ≤ 1 · 합 **0.686**) · **0.055 · 0.041 · 0.032** (f 1.08 · 1.25 · 1.42 · 합 **0.128**) | [판독 · 카드 산술] 그림 6i |
| **강한 사슬 몫** | 캡션 (k) *"the proportion of strong force chains, which can be obtained from the contact force probability distribution curve"* | **21.49 · 11.06 · 10.59 · 9.73 %** (10 · 20 · 30 · 40 %) · 본문 *"reaches 21.49 % … declines to 11.06 % and tends to stabilize … Eventually, 9.73 % of them align with the principal loading direction"* | [인쇄] 그림 6k · p.9 |
| 〃 재현 점검 | — | 40 % 의 f = 1 바로 위 세 칸만 **0.128 > 0.0973** → 9.73 % 는 이 P(f) 의 f > 1 합이 **아니다** (꼬리 f > 1.5 를 더하면 더 커짐) · 본문은 같은 9.73 % 를 '하중 방향으로 정렬한 강한 사슬의 몫' 으로도 읽는다 | [카드 산술 · 판독] |
| **도막 응력** | 식 9 σ_ij = (1/2V) Σ_{α=1}^{N} (r_{1i}F_{1j} + r_{2i}F_{2j}) [102, 103] · *"σxx, σyy and σzz refer to the stress components in the horizontal and normal directions, respectively, and σ means the overall stress of the particle layer"* | 본문 **σ 35 → 182.6 MPa (+422 %)** · 판독 σxx **2.19 · 4.88 · 10.28 · 21.17** · σyy 2.08 · 4.77 · 9.83 · 20.61 · σzz **3.09 · 7.02 · 12.07 · 25.55** · σ **34.9 · 50.1 · 100.0 · 180.3 MPa** | [인쇄] p.9 · [판독] 그림 6m |
| 〃 점검 | — | σ/σzz = 11.3 · 7.1 · 8.3 · 7.1 · σ ≠ 대각 합 (7.4 · 16.7 · 32.2 · 67.3) · ≠ 평균 · ≠ von Mises (1.0–4.7) · **σzz / DEM 판 압력 (맞춤) = 0.25 · 0.12 · 0.086 · 0.095** (40 %: 25.55 / 270.5 = **0.0945**) · 측압 비 K = (σxx + σyy)/2σzz = 0.69 · 0.69 · 0.83 · 0.82 | [카드 산술] |
| 〃 다른 카드 | 같은 Love–Weber 꼴 · RVE 부피로 정규화 | σzz/목표 압력 = **1.013 (30) · ≈1.11 (60) · 0.993 (200 MPa)** · K 0.40 → 0.68 | [다른 카드 `zhang2026_xct_…` §3.9] |

### 3-7. 집전체 응력 · 손상 기전 (p.10–11 · 그림 7 · `fig_7.png` · `txt_p10_p11_collector_stress_2565_weak_buffer_displacement.png`)

- 그림 7: (a–c) 입자 구조 · (d–f) 입자 변위 · (g–i) 힘 사슬 (색 0.25–1.25 mN · 파랑 = 약 · 빨강 = 강) · (j–l) 집전체 표면 응력 (색 0–280 MPa · 비선형 눈금) — ⚠ 캡션 *"(a-c) … 10 %, 20 %, and 30 %"* ↔ 본문 *"(20 %, 30 %, and 40 %)"* · 본문 *"Fig. 7e-h shows the evolution of the 3D force chain structure"* (캡션은 g–i).
- 20 %: *"limited stress concentration areas"* · 30 %: *"strong force chains run through the entire network … visible increase in stress concentration points"* · 40 %: 강한 사슬이 *"gradual migration toward the current collector side"* · **최대 256.5 MPa** · *"The weak force chain acts as a 'buffer zone' for stress transfer"* (p.10–11).
- 변위: *"Along the z-axis direction, the particle displacement exhibits a distinct gradient layering, with a gradual attenuation from top to bottom. The particles close to the collector are restricted in movement, exhibiting almost no displacement …"* (p.11).
- 결론 쪽 문장: *"The strong force chains migrate to the current collector side when the compression rate reaches 30 %"* (p.16) · 초록: *"when the calendering rate exceeds 30 %"* (p.1) — '30 %' 의 판정 기준 (강한 사슬의 높이 분포 등) 은 정량으로 없다 [미확인].

### 3-8. 손상 진화 · 실험 검증 (p.11 · 그림 8 · 9 · `fig_8.png` · `fig_8jl.png` · `fig_8mo.png` · `fig_9.png` · `txt_p11_…` 둘)

| 양 | 값 | 표지 |
|---|---|---|
| 측정 | CLSM 선 주사 (압연 방향) → 2D 단면 선 · 깊이 = 골 바닥까지 · 지름 = 골 폭 · *"the data shown in Fig. 8j-l represent typical values obtained from a single line scan, while the maximum pit depth and diameter were determined by comparing measurements across multiple line scans"* | [인쇄] p.11 |
| 20 % | *"the current collector surface remains smooth and intact, showing no visible deformation (Fig. 8a, d, g)"* — 같은 쪽 다음 문단 *"the number of craters increases rapidly to 379"* (20 %) 와 엇갈림 | [인쇄] |
| '평균 박힘 깊이' | **1.43 µm** (30 % · 그림 8k) · **1.86 µm** (40 % · 그림 8l) | [인쇄] |
| 그림 8j–l 한 줄의 가장 깊은 골 (선 중심 · 아래 가장자리) | 20 %: −0.79 (−0.81) µm @ 36 µm · 30 %: **−1.40 (−1.44)** @ 97 µm · 40 %: **−1.83 (−1.87)** @ 78.5 µm · 40 % 의 다른 골 −1.54 · −1.45 | [판독] — 1.43 · 1.86 은 그 한 줄의 **가장 깊은 골** 과 같고 골 평균이 아니다 (40 % 깊은 골 셋 평균 1.61 [카드 산술]) |
| 최대 깊이 · 지름 (그림 8n–o · 20 · 30 · 40 %) | 깊이 계산 / 실험 **0.80 / 0.96 · 1.29 / 1.25 · 1.84 / 2.32 µm** · 지름 **2.90 / 3.81 · 3.86 / 5.51 · 6.42 / 7.80 µm** | [판독] |
| 원문 판정 | *"the simulated values at different compression rates exceed the experimental values, and the maximum deviations of the embedding depth and diameter are 0.47 μm and 1.68 μm"* | [인쇄] |
| 판독 대조 | 계산 − 실험 = −0.16 · +0.05 · **−0.48** µm · −0.91 · **−1.65** · −1.39 µm → 6 칸 중 **5 칸 실험이 크다** · 최대 편차 크기 (0.48 · 1.65) 는 인쇄 0.47 · 1.68 과 맞는다 · 같은 문단 끝 *"more and deeper indentations are likely to form in the actual calendering process than predicted by the simulation"* 은 그림 쪽과 맞음 | [카드 산술] |
| 30 % 엇갈림 | 그림 8n 실험 '최대' 깊이 1.25 µm < 그림 8k '한 줄' 의 골 1.40–1.44 µm | [판독 · 카드 관찰] |
| 원인 (저자) | ① 집전체 거칠기 미반영 [104, 105] ② 손 선 따기 — *"the manual line method often fails to capture the lowest point of the indentation, resulting in depth values significantly lower than those obtained by automated methods"* (Hille [58]) | [인쇄] |
| 구멍 수 (그림 8m · 곡선 · 계산 / 실험 표지 없음) | 0 % ≈2 · 10 % **≈148** · 20 % **≈443** · 25 % ≈472 · 30 % **≈546** · 35 % ≈610 · 40 % **≈640** · 구간 표지 *"Rapid growth"* (0–≈21 %) · *"Transition"* (≈21–25 %) · *"Slow growth"* (≈25–40 %) | [판독] |
| 본문 | *"During the moderate calendering (ε = 20%) … the number of craters increases rapidly to 379"* · *"As calendering progresses (ε = 20 ∼30%), the number of damage points shows no significant change. However, when the calendering rate exceeds 30 % … significantly slowing pit quantity growth"* · Mayr [57]: 압연 안 한 전극 < 50 · 350 kN 압연 ≤ 350 개 | [인쇄] — 그림은 20 → 30 % 에 +103 · 30 → 40 % 에 +94 [카드 산술] |
| 40 % 최대 구멍 | *"the maximum pit depth and diameter reach 1.83 μm and 6.37 μm"* (= 그림 8n–o 의 **계산** 막대) | [인쇄] |
| DEM 법선 겹침 (그림 9 · 입자–집전체 · 10–40 %) | 네 패널 공통 색 막대 1.33 × 10⁻⁶ – **8.47 × 10⁻⁴ mm** (= 0.847 µm) · 빨강 (최대 근처) 점은 40 % 패널 (d) 에만 · *"contact area size indicates embedding depth"* · 축 표지 Z–X | [인쇄 색 막대] · [판독] |
| FEM 구멍 깊이 ÷ DEM 최대 겹침 (40 %) | 1.843 / 0.847 = **2.18** (색 막대 최대 = 40 % 패널로 읽음) — DEM 의 박힘 (겹침) 과 FEM 의 구멍은 다른 양 | [카드 산술 · 판독] |
| 그림 8a–c | 캡션 *"strain distributions on the collector surface"* · 색 막대 이름 *"Depth"* — 무엇을 그렸는지 원문 안에서 갈림 | [인쇄 · 카드 관찰] |

### 3-9. 입경 효과 (p.11–13 · 그림 10 · `fig_10.png` · `fig_10mn.png` · `fig_10o.png` · `fig_10p.png` · `txt_p13_particle_size_655_343_170_245_optimum_9p9um.png`)

| 양 | 값 | 표지 |
|---|---|---|
| DEM 세 모델 | *"three DEM models were generated using the corresponding D50 values as target diameters"* (7 · 9 · 13 µm · 40 %) · 측정 = 실험 CLSM 단면 선 ↔ 계산 *"strain distribution analysis"* | [인쇄] p.11 |
| 깊이 계산 / 실험 (그림 10m) | 7 µm **1.19 / 1.32** · 9 µm 1.69 / 1.70 · 13 µm **2.15 / 2.59 µm** | [판독] |
| 지름 계산 / 실험 (그림 10n) | 7 µm 6.57 / 7.42 · 9 µm 7.71 / 8.31 · 13 µm 10.22 / 12.00 µm | [판독] |
| 응력 집중점 수 | 본문 **655 → 343** (7 → 13 µm) · 판독 652 · 469 · 343 | [인쇄] · [판독] 그림 10o |
| 최대 응력 | 본문 **170 → 245 MPa** · 판독 169.5 · 179.5 · 245.3 · 13 µm / 7 µm = 1.45 (인쇄) = 1.447 [카드 산술] | [인쇄] · [판독] |
| '최적' 입경 | *"the optimal particle diameter of 9.9 μm was determined from the intersection of the damage points and current collector strength curves in Fig. 10o"* → **417 개 · 189 MPa** (40 %) | [인쇄] — ⚠ 서로 다른 두 축 (왼 · 오른) 곡선의 교점이라 축 범위를 바꾸면 교점이 움직인다 [카드 관찰] |
| 압하율 기울기 | 7 · 9 µm: *"each 1 % increase in compression rate raises the current collector stress by 5.63 MPa and 5.65 MPa"* · 9 µm · 30 % 를 넘으면 비선형 | [인쇄] p.13 (그림 10p · 곡면은 판독 안 함) |

### 3-10. 입도 분포 폭 효과 (p.13–15 · 그림 11 · `fig_11.png` · `fig_11gh.png` · `fig_11i.png` · `txt_p15_psd_sigma_0p5_2_4_pits_212mpa_115_139.png`)

| 양 | 값 | 표지 |
|---|---|---|
| 모델 | NMC 입도 표준편차 σ = 0.5 · 2 · 4 (단위 미기재 · 평균 11 µm 로 읽힘 — *"the 11 μm case"*) · CB **2.5 µm 고정** (*"this simplification does not reflect the actual particle size distribution of CB"*) · 40 % | [인쇄] p.13–15 |
| 구멍 지름 분포 | σ 0.5 · 2: 평균 **7.35 · 7.86 µm** · 표준편차 **1.50 · 1.70 µm** · σ 4: 평균 **8.5 µm** · 표준편차 **5 µm** | [인쇄] p.15 |
| 그림 11g 판독 | σ 0.5 (주황) 꼭대기 7.24 µm · 반치폭 → sd ≈1.70 · σ 2 (초록) 7.71 µm · sd ≈1.50 · σ 4 (파랑) 꼭대기 ≈8.5 µm · 반치폭 7.5 µm → sd ≈**3.2 µm** | [판독 · 카드 산술 · 정규 분포 가정] — 표준편차 짝 (1.50 · 1.70) 이 본문과 반대 · σ 4 는 5 ↔ 3.2 |
| 최대 응력 | σ 4: **212 MPa** (그림 11i) · 평균 7 µm 따로 계산: σ 0.5 → 4 에서 **+115 MPa** ↔ 11 µm **+139 MPa** | [인쇄] |
| 그림 11h 판독 | 범례 파랑 *"D50 = 11 µm"* 51.9 → 167.0 MPa (+115.1) · 주황 *"D50 = 7 µm"* 73.2 → 212.5 MPa (+139.3) | [판독] — 증가량 짝이 본문과 반대 · 212 MPa 도 범례로는 7 µm → 본문 세 문장 (212 = 11 µm 본 계열 · +115 = 7 µm · +139 = 11 µm) 이 서로 맞으므로 **범례가 바뀐 것으로 보인다** [카드 해석] |

### 3-11. ★ 저자가 적은 한계 · 원문 안 어긋남

**저자 한계 (원문 문장)**:
1. *"Since the platen-based DEM model cannot capture the full dynamics of calendering, future research will focus on the effects of roller rotation on stress transfer and its relationship with the current collector's elongation properties."* (p.16)
2. *"Additionally, the lack of a quantifiable threshold for contact damage penetration into the current collector necessitates further investigation through mechanical testing."* (p.16)
3. *"the simplified particle interactions and spherical morphology in the DEM model yield fewer compact contacts and simulated volume loss"* (p.7) · *"This deviation may be attributed to the simplified particle-particle interactions in the DEM model."* (p.6)
4. 집전체 거칠기 미반영 · 손 선 따기 편향 (p.11) · CB 입도 고정의 단순화 (p.13).
5. 장기 사이클 검증 · 입도 분포 확장은 다음 일 (p.16).

**원문 안 어긋남 (카드 관찰 · 판정 아님)**:
1. 식 2 v_Plate = v_Roll cos θ ↔ 본문 'A 최대 · B 0' (sin θ 와 맞음) · θ < 1° [75] ↔ 이 롤에서 1.62° (40 %) [카드 산술].
2. 접촉 쌍 +76.5 % ↔ 인쇄 수로 +74.7 %.
3. F′zz 감소 (z 쪽 접촉 몫 감소) 를 '수직 정렬' 로 읽음 · '낮은 압하 = 거의 구 대칭' ↔ 10 % 이방성 최대.
4. 강한 사슬 몫 9.73 % ↔ P(f) 의 f > 1 합 (위 세 칸만 0.128) · P(f) 분모 = 입자 수 · 9.73 % 를 '정렬한 몫' 으로도 읽음.
5. σ 정의 없음 · 대각 성분 · 판 압력과 어긋남 (σzz ≈ 판 압력 × 0.095).
6. 그림 7 캡션 10/20/30 % ↔ 본문 20/30/40 % · 본문 *"Fig. 7e-h"* (캡션 g–i) · 본문 *"Section 4.2"* 가 자기 절을 가리킴 · 사슬 색 *"blue and red"* ↔ *"red and green"*.
7. 20 % *"smooth and intact"* ↔ 같은 20 % 에서 구멍 379 개 · 그림 8m 의 20 % ≈443 · '20–30 % 변화 없음' ↔ 그림 +103.
8. *"simulated values … exceed the experimental values"* ↔ 그림 8n–o 5/6 칸 실험이 큼.
9. *"average embedding depth"* 1.43 · 1.86 = 그림 8k · 8l 한 줄의 가장 깊은 골 · 30 % 실험 '최대' 1.25 < 그 골.
10. 그림 8a–c 캡션 'strain' ↔ 색 막대 'Depth'.
11. 그림 11h 범례 짝 ↔ 본문 증가량 짝 · 그림 11g 표준편차 짝 ↔ 본문.
12. 식 A.3 · A.4 분모 = 반지름 · 식 A.6 δᵖ · 점착 가지 지수 n · 식 A.8 ϕ 정의 없음 · λp 설명 ('탄성 대 소성 비').
13. 밀도 두 벌 (p.3 NMC 2.42 · CB 1.6 ↔ 표 1 4750 · 2250 kg/m³).
14. 참고문헌 중복 — [41] = [85] (Thakur 2016) · [82] = [88] = [93] (Schreiner 2023) · [28] = [66] (Schreiner 2019) · [72] (Stershic 2015 · 직물 텐서 DEM) 가 *"copper and aluminum foil … [71,72]"* 와 표 1 의 E 출처 둘로 쓰임 · 표 1 의 AM–AM 8 J/m² = [86] 인데 [86] 의 정본 카드 값은 NMC–NMC 5 J/m² [다른 카드 `schreiner2020_…` L42].
15. C3D8R (Abaqus 요소 이름) 을 ANSYS 2022 해석에 씀.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
실험: NMC532 · CB · PVDF 혼합 → NMP 슬러리 → 17 µm Al 박 도포 → 85 °C 6 h → ≈100 µm → MSK-2300A 롤 (지름 200 mm · 1 m/min · 상온) 압하율 10–40 % (선하중 14–530 N/mm) → 마이크로미터 두께 · 질량 → 기공률 · SEM 단면 · 도막 제거 뒤 CLSM 선 주사 (구멍 깊이 · 지름 · 수).
계산: 측정 입도로 AM · CB 구 생성 (EDEM 2021) → 100 µm 입방 RVE (x · y 주기 · 위 = 강철 판 · 아래 = 단단한 Al stl) → 판을 내려 압하율 10 · 20 · 30 · 40 % 를 **각각 따로** 만든 상태 → 접촉 통계 (쌍 수 · 직물 · P(f) · 강한 사슬 몫) · 도막 응력 (식 9) · 입자 변위 → 집전체 면의 접촉력 (법선 + 접선) · 좌표를 axdt 로 → ANSYS 2022 Al 박 RVE (C3D8R · 바닥 고정 · 정적) → Mises 응력 · '변형' 지도 → 구멍 깊이 · 지름 · 집중점 수.
맞춘 값: 이름 붙은 것 **없음** — 표 1 은 전부 문헌 값 · 절 제목은 *"Model calibration and validation"* (§3.3) 이지만 조정한 매개변수가 적혀 있지 않다 (압력–두께 · 기공 곡선은 검증으로만 쓰임) [미확인].

### 4-2. 입자 처리
- **AM · CB = 단단한 구** (측정 입도) · 소성은 **접촉 법칙 안** (EEPA λp 0.96 = 제하 강성 25 배) · **입자 형상 변화 0** · 파쇄 없음 (*"the increase in the number of force chains does not necessarily accompany particle fracture [97,98]"* p.9).
- **PVDF = 매개변수** (γ · f₀) · CB 는 E 0.45 GPa 의 구 (AM 의 1/316).
- **집전체**: DEM 에서는 단단한 면 (박힘 = 입자–면 겹침 · 그림 9) → FEM 에서만 변형 (구멍).  둘은 다른 양 (FEM 구멍 / DEM 겹침 = 2.18 [카드 산술]).
- 우리: DEM = 탄성-이력 구 (hooke/hysteresis) · SE 18 배 연화 (E_eff 1.35 GPa) · AM E 140 GPa · ν 0.25 [우리 — CLAUDE.md frame[2] · `devasconcelos2019_…` §4-2 가 옮긴 `input_real_14.liggghts` L29–30] · MPM = SE 형상 소성 (E 1.53 · σ_y 0.30 · ν 0.49) · AM 동결 scaffold [우리 — CLAUDE.md].

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)

| 질문 | 원문 | 위치 |
|---|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계 | ① *"However, DEM has limitations in describing the macroscopic mechanical behavior of materials (e.g., stress distribution, continuum deformation of materials). To address this, the coupled method of DEM and finite element method (FEM) has gradually become an effective tool …"* ② *"For porous electrodes, the DEM has limitations in obtaining the stress distribution of the current collector. Relying solely on the FEM faces challenges due to the difficulty in capturing the complex properties of the current collector."* ③ *"the simplified particle interactions and spherical morphology in the DEM model yield fewer compact contacts and simulated volume loss"* ④ *"This deviation may be attributed to the simplified particle-particle interactions in the DEM model."* ⑤ *"Since the platen-based DEM model cannot capture the full dynamics of calendering …"* — **수치 한계 (믿을 겹침 · 밀도 상한) 는 없다** · 반대로 EEPA 가 *"large deformation"* 을 다룬다고 범위 없이 적는다 | ① p.2 (`txt_p2_dem_limitation_and_song29_bidirectional.png`) ② p.5–6 ③ p.7 ④ p.6 ⑤ p.16 |
| (ii) 입자 소성 · 큰 변형이 어려운 이유 · 우회 · 비용 | 이유 문장은 위 ① · ③ (연속체 변형 · 구 형상) 뿐 · **우회 = 접촉 법칙의 소성 (EEPA λp 0.96 · k₂ = 25 k₁)** + **집전체만 FEM 연속체로 넘김 (한 방향 · 정적)** · *"the EEPA model represents the deformation and elastic recovery of particles during the coating's loading and unloading processes through the plastic contact ratio (λp)"* (p.5) · 입자 소성 · 형상 변화 · 다접촉 보정 없음 · **비용 (입자 수 · 계산 시간 · 시간 간격) 원문에 없음** · *"To reduce computational costs, a cubic representative volume element (RVE) with dimensions of 100 × 100 × 100 μm3 was constructed"* (p.4) 한 줄 | p.2 · p.4 · p.5 · p.7 |
| (iii) 2D 인가 3D 인가 · 2D → 3D | **3D** (DEM RVE 100³ µm³ · FEM C3D8R) · 그림 3a 는 *"a two-dimensional schematic"* · 2D → 3D 전이에 대한 말 없음 · 실험 구멍 측정은 CLSM **선 주사 (2D 단면 선)** — *"A line scan along the calendering direction was performed to obtain two-dimensional cross-sectional profiles"* (p.11) — 3D 계산 구멍과 2D 단면 측정을 견준다 | p.4 · p.11 |
| (iv) 압력을 뺄 때의 거동 | **다루지 않음** — 전극 되돌아옴 (springback) 값 없음 · DEM 상태는 압력 단계마다 누른 상태로 읽힘 (탈압 단계 서술 없음) · 실험 기공 · 두께는 압연 **뒤** 측정 (= 뺀 뒤) · 접촉 수준 = λp 0.96 (겹침의 4 % 회복 [카드 산술]) · 그림 3a 의 h3 > h2 (출구 두께) 는 도식뿐 · 서론의 [10] Diener 2022 (롤 간극 직접 측정으로 빠른 탄성 회복) 인용 = 정본 카드 `diener2022_roll_gap_springback_calendering` | p.5 · p.7 · 그림 3a · p.2 |

### 4-4. 기법 미니 용어집
- **압하율 (compression rate) ε**: (H₀ − H_c)/H₀ × 100 % (식 3) — 도막 두께가 준 몫 (H₀ ≈ 100 µm).  우리 다이 가압의 '목표 압력' 이 아니라 **두께 목표** 다.
- **평판 근사 (platen approximation)**: 롤 대신 평평한 강철 판을 내려 누름 — 롤의 곡률 · 회전 · 접선 · 출구 되돌아옴을 버린다.
- **RVE**: 100 µm 입방 (DEM) · 100 × 100 × 17 µm (FEM) 대표 부피 · DEM 은 x · y 주기 경계.
- **EEPA (Edinburgh Elasto-Plastic Adhesive)**: 하중 강성 k₁ · 제하 강성 k₂ · 점착 강성 k_adh · 상수 점착 f₀ 의 조각 이력 접촉 법칙 (식 A.6) — 항복 캡 없음 · 입자는 단단한 구.
- **λp (contact plasticity ratio)**: 1 − k₁/k₂ = δp/δmax (식 A.7) — 최대 겹침 가운데 남는 (소성) 겹침의 몫.
- **axdt**: EDEM 이 ANSYS Workbench 로 내보내는 하중 자료 파일 (접촉력 · 좌표).
- **C3D8R**: 8 절점 감차 적분 육면체 요소 (Abaqus 이름 — 원문은 ANSYS 와 함께 씀).
- **'힘 사슬 밀도'**: 이 논문에서는 **모든 접촉 쌍의 수** (세기 무관).
- **직물 텐서 (fabric tensor)**: 접촉 법선 n 의 2 차 모멘트 F_ij = ⟨n_i n_j⟩ (식 6 은 구 부분 δ_ij/3 + 편차 F′_ij 로 나눔) — F′zz > 0 = z 쪽 접촉 많음.
- **상대 접촉력 f · 강한 / 약한 사슬**: f = 접촉력 / 평균 (식 7) · f > 1 강 · ≤ 1 약 (Kruyt [100] 의 문턱).
- **P(f)**: 접촉력 구간별 분포 (식 8 · 분모 = 입자 수).
- **도막 응력 σ_ij (식 9)**: 접촉마다 두 입자 중심 → 접촉점 가지 벡터와 힘의 곱을 더해 부피로 나눈 Love–Weber · Christoffersen 꼴.
- **CLSM**: 공초점 레이저 주사 현미경 — 도막을 벗긴 Al 박 표면의 높이 단면 선.
- **응력 집중점 (stress concentration point · damage point)**: FEM 집전체 면의 국소 고응력 자리 (그림 7j–l 초록 원 · 10o 의 수) — 판정 문턱은 원문에 없다.

## 5. Figure set ★

| 그림 · 표 | 무엇을 보여주나 | 우리가 쓸 점 |
|---|---|---|
| **그림 1** (`fig_1.png`) | 전극 제조 사슬 (혼합 · 도포 · 건조 · 압연) | 공정 도식 |
| **그림 2** (`fig_2.png` · `fig_2d.png`) | (a) 도막 미세구조 도식 (b) SEM 입자 접촉 · 힘 전달 경로 (빨간 원 · 노란 점선) (c) DEM 의 같은 표시 (d) EEPA 법선력–겹침 도식 (k₁δⁿ · k₂(δⁿ − δpⁿ) · −k_adhδⁿ · f₀ · f_min · δ_min · δp · δ_max) | (d) = 식 A.6 의 그림 · 축 수치 없음 |
| **그림 3** (`fig_3.png` · `fig_3a.png` · `fig_3b.png`) | (a) 롤 기하 (R · θ · S · A/B/C · h1/h2/h3 · v_Plate · v_Roll) (b) A · B · C 의 DEM RVE (지름 색 1.0–16.0 µm · *"Current collector-Al foil"*) | 평판 근사의 기하 · 본문은 hA/hB/hC 로 적음 |
| **그림 4** (`fig_4.png`) | DEM ↔ FEM 결합 고리 (stl · axdt 하중 자료 · FEM 격자 · 경계) | ★ 한 방향 넘김 도식 |
| **그림 5** (`fig_5.png` · `fig_5c.png` · `fig_5d.png`) | (a) DEM 단면 (b) SEM 단면 (ZX) (c) 압력–두께 (DEM 점 8 · 실험 점 5 · 맞춤 곡선 둘) (d) 기공률–압하율 | ★ 검증 두 곡선 · 판독값 = digitized.csv |
| **그림 6** (`fig_6.png` · `fig_6eh.png` · `fig_6i.png` · `fig_6jk.png` · `fig_6l.png` · `fig_6m.png`) | (a–d) 접촉력 망 10–40 % (e–h) 3D 직물 장미 (i) P(f) (+ 삽입 f 0–1.5) (j) 직물 편차 대각 (k) 강한 사슬 몫 (l) 접촉 쌍 수 (m) 도막 응력 대각 + σ | ★★ 이 카드의 힘 사슬 숫자 원천 |
| **그림 7** (`fig_7.png`) | (a–c) 입자 구조 (d–f) 변위 (g–i) 힘 사슬 (0.25–1.25 mN) (j–l) 집전체 응력 (0–280 MPa) | 정성 · 캡션 압하율 표기 어긋남 |
| **그림 8** (`fig_8.png` · `fig_8jl.png` · `fig_8mo.png`) | (a–c) 집전체 '변형' 지도 (d–f) CLSM 표면 (g–i) SEM (j–l) CLSM 높이 단면 한 줄 (m) 구멍 수 곡선 (n–o) 최대 깊이 · 지름 계산 ↔ 실험 | ★ 실험 검증 · 판독값 = digitized.csv |
| **그림 9** (`fig_9.png`) | 입자–집전체 법선 겹침 지도 10–40 % (공통 색 막대 ≤ 8.47 × 10⁻⁴ mm) | DEM 쪽 '박힘' = 겹침 |
| **그림 10** (`fig_10.png` · `fig_10mn.png` · `fig_10o.png` · `fig_10p.png`) | (a–c) 7 · 9 · 13 µm 모델 (d–f) 힘 사슬 (g–i) 집전체 응력 (j–l) 표면 (m–n) 깊이 · 지름 계산 ↔ 실험 (o) 집중점 수 · 최대 응력 vs 입경 (p) Mises 응력 곡면 (압하율 × 입경) | '최적 9.9 µm' 의 근거 그림 |
| **그림 11** (`fig_11.png` · `fig_11gh.png` · `fig_11i.png`) | (a–c) σ 0.5 · 2 · 4 모델 (d–f) 법선 겹침 (≤ 3.20 × 10⁻³ mm) (g) 구멍 지름 분포 (h) 최대 응력 막대 (σ 0.5 · 4 × D50 7 · 11 µm) (i) Mises 응력 곡면 (압하율 × σ) | 범례 짝 의심 (§3-10) |
| **표 1** (`tab_1.png`) | DEM 매개변수 (재료 넷 + 입자–입자 8 줄 · 출처 번호) | ★ 입자–Al 줄이 없다는 증거 |
| 식 1–9 (`eq_01`–`eq_09`) · 부록 식 A.1–A.11 (`eq_A01`–`eq_A11`) · 부록 통째 (`eq_A_block_…`) | 접촉각 · 판 속도 · 압하율 · 힘 크기 · 정규화 · 직물 · 상대 힘 · P(f) · 응력 텐서 · EEPA 전부 | 보고서 붙임용 |

### 5-1. 크롭 색인 — `litdb/figures/du2025_dem_fem_force_chain_collector_damage_calendering/`
- 도구 (`tools/litdb/extract_figures.py`, 300 dpi) 12 장 (그림 1–11 + 표 1) — **12 장 모두 다시 자름**: 그림 11 장 = 쪽 폭 띠 (양옆 흰 여백 · 캡션에 본문이 이어 붙은 것 여럿) → 각 그림의 **내장 원본 래스터** (300 dpi · 재표본 없음) 에서 잉크 상자 + 고른 6 pt (25 px) 여백 · 표 1 = 도구 크롭이 쪽 위에서 시작해 그림 3 과 왼 단까지 삼켰음 → 벡터 쪽을 400 dpi 로 다시 렌더 (clip [304, 528.5, 559.5, 742.5] pt).  놓친 번호 0.
- 손 크롭 58 = **패널 17** (`fig_2d` · `3a` `3b` · `5c` `5d` · `6eh` `6i` `6jk` `6l` `6m` · `8jl` `8mo` · `10mn` `10o` `10p` · `11gh` `11i` — 패널 사이 전부 흰 행 · 열에서만 자름 · 옆 패널 축 제목 곁에 표지가 붙은 세 쌍 (6j–k · 8m–o · 11g–h) 은 같이 둠 · `fig_2d` 의 SEM 조각 8 px · `fig_10o` 의 옆 패널 '(p)' 표지 · `fig_10p` 의 (o) 오른 축 제목 끝은 흰색으로 지움 — figures.json `manual_crop` 에 상자 기록) + **식 21** (식 1–9 · A.1–A.11 · 부록 통째 — 식 줄 + 번호 · 400 dpi 벡터 · 윗줄 꼬리가 걸리던 자리는 글자 층 줄 상자로 자를 줄을 다시 정함) + **근거 문단 20** (`txt_p1_…` – `txt_p16_…` · 이 카드가 숫자 · 정의 · 단정의 근거로 인용한 문단만 · 400 dpi 벡터 · 여러 단은 3.4 pt 간격으로 위 → 아래).
- 그림 이미지가 없는 패널 (2a–c · 5a–b · 6a–d · 7a–l · 8a–i · 9a–d · 10a–l · 11a–f) 은 값이 없는 그림이라 따로 자르지 않음 — 전체 그림 크롭 안에 있다.
- 70 장 전부 Read 로 열어 확인 (잘림 · 이웃 문단 · 쪽 머리글 · 쪽 번호 없음).  모음 그림 = 세션 scratchpad `litcards/du2025_dem_fem_force_chain_collector_damage_calendering_sheet_1.png` · `_sheet_2.png` (식 크롭 포함).

## 6. Post-processing ★
- **원문 쪽**: 접촉 쌍 수 · 직물 편차 (구 장미 → 대각 성분) · P(f) (구간 · 분모 = 입자 수) · 강한 사슬 몫 (*"can be obtained from the contact force probability distribution curve"* — 계산식 없음) · 도막 응력 (식 9 · V 의 정의 · σ 의 정의 없음) · FEM Mises 응력 · 집중점 수 (문턱 없음) · 구멍 깊이 · 지름 (계산 = *"strain distribution analysis"* · 실험 = CLSM 선 · 손 따기 · 여러 줄 가운데 최대) · '최적 입경' = 두 축 곡선 교점.  통계 · 시드 반복 · 오차 막대 · 소프트웨어 이름 (EDEM · ANSYS 밖) **없음**.
- **이 카드의 판독**: 그림은 전부 내장 래스터 (300 dpi) — numpy + Pillow 로 축의 안쪽 눈금 (최소제곱) · 색 가면 연결 성분 (점 중심 = 거리 변환 핵 주변 창 · 상자 중심) · 막대 윗변 (색 띠마다 첫 어두운 행 − 0.5 px) · 곡선 열 훑기 · 붙은 막대 쌍 (그림 8n 30 % · 10m 9 µm) 은 띠를 나눠 따로 · 그림 8j–l 골 = 열마다 가장 낮은 어두운 화소 (눈금 열 · 범례 제외 · 빨간 0 점선이 0.00 ± 0.02 µm 에 오는지 점검) → `digitized.csv` 163 행 (행마다 눈금 화소 위치 · 방법 note).  점검: 그림 6j 대각 합 \|Σ\| ≤ 0.004 · 그림 5c 실험 점 하나 (59.7 µm) 는 DEM 원에 반쯤 가려 삼각형 무게 중심 (꼭짓점에서 2/3) 으로 읽음.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md · 정본 카드가 적은 출처를 그 자리에 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 공정 · 상태가 다르다** — 이 논문 = 액체계 LIB 양극 · 롤 압연 (평판 근사) · SE 없음)

| 항목 | 이 논문 | 우리 | 판정 (판정 없이 나란히 · 차이의 이유) |
|---|---|---|---|
| 계 · 조성 | NMC532 : CB : PVDF 90 : 5 : 5 (고체 부피 AM 78.9 %) · 액체 전해질 | NCM811 + LPSCl (+ 첨가제) 황화물 복합 양극 · 예 real_14: AM 36 (AM_P) + 421 (AM_S) · SE 32,832 [우리 — CLAUDE.md scaffold 절] | 무른 상이 다르다 — 이 논문의 무른 상 = CB (E 0.45 · 5 wt%) · 우리 = SE (부피로 수십 %) |
| 공정 · 하중 | 롤 (지름 200 mm · 1 m/min) 압하율 10–40 % · 선하중 14–530 N/mm · DEM 판 압력 ≈4 → 270 MPa [판독] | 다이 단축 **300 MPa** (DEM 서보 · 다압력 100/200/300/600) [우리 — CLAUDE.md] | 두께 목표 ↔ 압력 목표 · 롤 ↔ 다이 · 압력 크기는 같은 자릿수 (DEM 판 270 ↔ 300) |
| 접촉 법칙 | **EEPA** (λp 0.96 · k₂ = 25 k₁ · 점착 γ · f₀) · 연화 없음 · AM E 142 GPa | LIGGGHTS **hooke/hysteresis** · SE E 24 → **1.35 GPa (18 배 연화)** · AM E 140 · ν 0.25 [우리 — CLAUDE.md frame[2] · `devasconcelos2019_…` §7-1] | 같은 '이력 탄소성 접촉' 계열 · 이 논문은 점착 가지가 있고 우리는 없다 (he2026 L362 의 관찰과 같음) · AM–AM E* 75.7 ↔ 74.7 GPa [카드 산술] — AM 쪽은 같은 자릿수 · 연화는 우리 SE 쪽 일 (대칭 관계 — he2026 L363) |
| 형상 소성 | 0 (단단한 구) · 집전체만 FEM 연속체 | DEM 0 · MPM 이 SE 형상 소성 (J2 · E 1.53 · σ_y 0.30 · ν 0.49) [우리 — CLAUDE.md] | frame[5] 같은 쪽 (§2 계보) |
| ★ **힘 사슬 · 하중 분담** | 접촉 쌍 수 · F′ · P(f) · 강한 사슬 **수** 몫 21.49 → 9.73 % · σ (정의 결손) · **상별 하중 몫 0** | f_AM 두 규약 — (a) AM–AM 접촉망 σzz 몫 **0.517 · 0.598 · 0.675 · 0.620** · (b) 상별 virial **0.726 · 0.768 · 0.794 · 0.763** (P = 100 · 200 · 300 · 600 MPa) [우리 — CLAUDE.md '조건부 wallP' 절 · he2026 L368 이 옮김] | **같은 양이 없다** — §7-2 |
| 응력 텐서 점검 | σzz (식 9) = 판 압력의 **0.095** (40 %) · 0.25 · 0.12 · 0.086 (10–30 %) | Love–Weber 입자 응력 열 (`stress_cv_lw` · `stress_ratio_<상>_lw`) · 검사 = 전체 virial ↔ c_strs [우리 — CLAUDE.md J20-s ④b] | 우리 LW 구현이 판 압력을 되찾는지 (σzz(LW)/P_platen ≈ 1) 를 등록 점검으로 — `zhang2026_…` 은 ≈1.0 [다른 카드] |
| 기공 · 연산자 | DEM 52.0 → 18.9 % · 실험 50.0 → 16.9 % (0–40 %) · DEM 연산자 · 상태 미기재 · 고체 보존과 −3.9 %p 까지 어긋남 | ε_sphere 규약 (고체 = 구 부피 합) · real_14 15.6 % @ 300 MPa · 랩 표준 **순수 SE 10–13 % · LPSCl 진밀도 1.64 g/cm³** (고정 · 판정 대상 아님) [우리 — CLAUDE.md] | 이 논문 값 = **랩 표준과 다른 문헌 값** (다른 재료 · 공정) — 같은 표에 놓지 않는다 · 가져올 것 = '연산자 · 상태를 적는 칸' |
| Heckel | crude P_y 실험 ≈236 · DEM ≈285–333 MPa [카드 산술 · 섞인 상태] | 순수 SE DEM P_y **138 MPa** (R² 0.965 · σ_y_eff 46 MPa) [우리 — CLAUDE.md frame[3]] | 다른 상 (NMC 골격 ↔ 연화 SE) · 다른 상태 — 나란히 인용 금지 |
| 집전체 · 판 | DEM: 단단한 stl · FEM: Al 박 탄성 (구성식 미기재) 정적 → 구멍 · Mises 256.5 MPa | DEM: 판 = 메시 (mesh/surface/stress) · 집전체 없음 · MPM: 단단한 판 (hold / servo) [우리 — CLAUDE.md] | 우리에게 없는 축 (집전체 손상) — 가져올 것 없음 · 방법 (한 방향 넘김) 만 §8 |
| 재하율 | 판 속도 · 시간 간격 미기재 | MPM `--platen-mach` 0.03 · 재하율 함정 [우리 — CLAUDE.md] | 비교 불가 |
| 시드 · 반복 | 없음 (설계점마다 한 런) | 같은 설계점 다시드 (예 `input_particulate_12` S1–S5 · `input_72_seed1..5`) [우리 — CLAUDE.md σ_ionic 절] | 이 논문 값의 산포 (시드 · RVE 위치) 는 알 수 없다 |

### 7-2. ★ 정의 대조 — "같은 이름 · 다른 양"
- **"force chain density" (이 논문)** = 세기와 무관한 **모든 접촉 쌍의 수** — 우리 배위수 (CN) · 접촉 수 열과 같은 종류 (사슬 판정 아님).
- **"strong force chain fraction" (이 논문)** = f = F_i / ⟨F⟩ > 1 인 접촉 (또는 식 8 대로면 입자) 의 **수 몫** — 그 사슬이 지는 **하중 몫이 아니다**.  하중 몫 (Σ_{f>1} f · P(f) / Σ f · P(f)) 은 원문 P(f) 의 꼬리 (f 1.5–38) 를 못 읽어 계산할 수 없다 · 그 9.73 % 는 같은 P(f) 와 맞지도 않는다 (§3-6).
- **우리 f_AM (a) AM–AM 접촉망 σzz 몫** = Love–Weber 합을 **AM–AM 접촉에만** 한정한 σzz ÷ 전체 σzz · **(b) 상별 virial** = 식 9 꼴의 두 가지 벡터 항을 **입자 상별로** 나눠 AM 입자 몫만 더한 σzz ÷ 전체 (= (a) + ½ × AM–SE 몫) [우리 — CLAUDE.md].  **이 논문의 식 9 는 (b) 를 만들 수 있는 꼴** (r_{1i}F_{1j} 와 r_{2i}F_{2j} 를 입자마다 따로 가진다) 이지만 원문은 **합만** 낸다 → 계산하려면 원자료 (접촉 쌍 · 가지 벡터 · 입자 상) 가 필요하다 (*"on request"*).
- **"σ — overall stress of the particle layer"** = 정의 없음 · 대각 성분과도 판 압력과도 맞지 않는다 (§3-6) — 우리 '전체 virial' 과 같은 양으로 읽지 않는다.
- **"F′zz"** = 직물 편차 (접촉 **법선** 방향 분포) — 힘 사슬의 '방향' 이 아니라 접촉 방향 (힘 가중 직물이 아님 · 원문 식 6 에 힘 가중 없음).
- **"embedding depth"**: DEM = 입자–면 겹침 (≤ 0.847 µm) · FEM = 구멍 깊이 (≤ 1.84 µm) · 실험 = CLSM 골 깊이 (한 줄 · 여러 줄 최대) — 셋이 다른 양.
- **"calibration"** (§3.3 제목) = 매개변수 조정 없이 검증만 — 우리 R5 의 '맞추는 값 하나' 와 같은 뜻이 아니다.

### 7-3. 나란히 놓을 정본 카드 (값 · 조건 그대로 · 기존 카드는 고치지 않는다)

| 카드 | 재료 · 방법 | 힘 사슬 · 응력 · 하중 몫 | 이 카드와의 관계 |
|---|---|---|---|
| **이 카드** | NMC532 LIB 양극 · EEPA DEM + 한 방향 FEM · 평판 | 접촉 쌍 23,940 → 41,816 · 강한 사슬 수 몫 21.49 → 9.73 % · σzz 3.1 → 25.5 MPa (판 압력의 0.09–0.25) · 하중 몫 없음 | — |
| `he2026_dem_calendering_inhomogeneity_areal_density` | NCM622 LIB 양극 · EEPA DEM · 평판 · 면적 하중 축 | 정량 0 · 최대/평균 접촉력 11 배 [다른 카드 L368] | 이 논문을 N5 · [41] 로 가리킨 카드 (§0-1) |
| `zhang2026_xct_dem_cathode_calendering_peel_calibration` | NMC111 · X-CT 초기 구조 · Hertz–Mindlin + 결합 · 입자–집전체 결합 박리 보정 · 가압–제하 | σ_zz/목표 = 1.013 · ≈1.11 · 0.993 (30 · 60 · 200 MPa) · 최대 매립 (겹침) 0.937 µm @ 200 MPa · 힘 사슬 = NMC 가 짐 (정성) [다른 카드 §3.7–3.9] | 같은 Love–Weber 꼴인데 판 압력을 되찾는다 · 매립 (겹침) 자릿수 = 이 논문 그림 9 (≤ 0.847 µm) 와 같음 |
| `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` | NCM9055 · in situ CT + 등가 구 DEM (결합) | 압축비 30–35 % 에서 굵은 사슬이 위에서 아래까지 관통 (정성) [다른 카드 L34 · §3-7] | '30 % 근처 사슬 관통' 정성이 이 논문의 '30 % 뒤 강한 사슬 이동' 과 같은 쪽 (다른 정의) |
| `yano2024_eepa_binary_mixture_plasticity_compression_dem` | EEPA 이원 혼합 (λp 0.38 ↔ 0.70) 단축 압축 | **하중 몫 재지 않음** · 접촉 종류별 수 · 면적만 [다른 카드 L34 · L55] | 질문 d 의 같은 빈칸 — EEPA 혼합에서도 하중 몫 정량은 정본에 없다 |
| `sangros2019_dem_calendering_lib_electrode` | NMC LIB 양극 · Thornton–Ning + 결합 · 롤 기하 (지름 430 mm) | 탄성 회복 ER 10.25 → 17 % (시뮬) [다른 카드 L28] | 이 논문 [75] = 식 1 · θ < 1° · 밀도 출처 — 되돌아옴은 이 논문이 다루지 않은 축 |
| `schreiner2020_dem_calendering_lib` | NMC622 · EEPA + bonding | λ_P 0.8–0.985 · 표면 에너지 5 · 20 · 60 J/m² [다른 카드 L41–L42] | 이 논문 [86] — AM–AM 8 J/m² 의 인용처인데 그 카드 값은 5 |
| `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` · `thakur2014_eepa_adhesive_elastoplastic_dem` | EEPA 원전 (학위논문 · 학술지 판) | f_min = (3/2)πΔγa · 점착 가지 지수 X · 항복점 없음 [다른 카드] | 식 A.6 · A.8 의 표기 차이를 닫는 곳 |
| `bazzoun2026_dem_fem_rnm_ionic` | LPSCl + NMC811 · LIGGGHTS DEM → FEM (이온 수송) · RNM | (역학 하중 몫 아님) | 같은 'DEM 구조 → 연속체' 넘김의 수송 쪽 선례 (h) |

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **DEM (접촉망 · 힘 사슬 · 패킹) + 집전체 연속체 FEM** — 우리 분업으로는 DEM 고유 관측량 (힘 사슬 · 접촉망) 쪽 + '입자 아래 단단한 바탕을 연속체로' 라는 넘김.
- 없는 반쪽: 입자 형상 소성 (MPM 쪽) · SE · 상별 하중 분담 · 탈압 · 수송.
- ★ **넘김의 방향**: DEM → FEM 은 **후처리** (FEM 변형이 DEM 으로 돌아오지 않는다 · 박힘이 DEM 에서는 겹침) — 우리 11-09 주간보고 피드백 ("DEM → MPM 은 결합이 아니라 후처리") 이 가리킨 바로 그 꼴의 **문헌 실례** [카드 해석 · 우리 — CLAUDE.md 11-09 줄].  양방향의 선례는 [29] Song 2023 (원문 *"a DEM-FEM bidirectional coupled model to simulate particle embedding in the current collector"* p.2 · 카드 없음).

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = NMC532 + CB + PVDF 액체계 LIB 양극 — **SE 가 없고** · 롤 압연 (평판 근사) 이고 · AM 조성도 다르다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **연산자 · 상태 칸의 반례 셋** — ① 기공: 실험 = 압연 **뒤** 두께 · 질량 · 진밀도 (어느 진밀도인지 미기재 — p.3 의 2.42 ↔ 표 1 의 4750) · DEM = 연산자 · 상태 **미기재** · 고체 보존 산술과 DEM 이 −3.5 · −3.9 %p 어긋남 (§3-5) → 우리 등록 문서에 **'연산자 · 누른 채 / 뺀 뒤 · 고체 보존 점검'** 세 칸 ② 검증 지표: *"maximum deviation of 3.66 %"* · *"0.073 %"* — 정의 · 기준점 없음 · 0.073 % 는 두 맞춤 곡선의 **교점 근처** (≈66 µm · ≈200 MPa) [카드 해석] → '편차 = 무엇 ÷ 무엇 · 어느 점' 을 결과 전에 ③ '최적' = 서로 다른 두 축 곡선의 교점 (축 범위 의존) → 판정 규칙이 축 척도에 기대면 안 된다는 반례 | 판정 기준을 결과 전에 적은 흔적 없음 · 시드 · 오차 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 (입자 수 · 메모리 · 시간 미기재) — 규모 자리표: DEM RVE 100³ µm³ · AM D50 7.2 µm · CB D50 2.5 µm (AM 1 개당 ≈2.8 [카드 산술]) | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (SE 없음) | 랩 표준 (10–13 % · 1.64) 옆에 놓을 값 없음 |
| **단계 5** (3D 복합 압밀) | **AM 골격 쪽 극한** (고체 부피 AM 79 % · 무른 CB 9 %) 의 압밀 한 벌: 두께 100 → 60 µm 에서 DEM 판 압력 ≈4 → 270 MPa · 기공 52.0 → 18.9 % [판독] · 접촉 쌍 ×1.75 · 측압 비 K 0.69 → 0.82 · z 쪽 접촉 몫 ⟨n_z²⟩ 0.38 → 0.30 [카드 산술] · 바닥 입자 거의 안 움직임 (정성) | SE 없음 · 하중 몫 없음 · 응력 정규화 미상 (σzz ≈ 판 압력 × 0.1) |
| **단계 6** (탈압 · 되돌아옴) | 없음 — λp 0.96 (접촉 겹침의 4 % 회복 [카드 산술]) 뿐 · 실험 기공은 뺀 뒤 값 · 되돌아옴 원전은 정본 `diener2022_roll_gap_springback_calendering` ([10]) · `sangros2019_…` ER 10.25 → 17 % ([75]) | 전극 두께 회복 · 탈압 경로 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 (수송 계산 없음) · '박힘' 의 세 정의 (DEM 입자–면 겹침 ≤ 0.847 µm · FEM 구멍 ≤ 1.84 µm · CLSM 골) — 우리 피복 · 계면 면적을 셀 때 **겹침 ≠ 형상 변화** 를 적는 근거 | — |
| **후보 D0** (지금 DEM) | ★ AM 입력 E 142 ≈ 우리 140 GPa (AM–AM E* 75.7 ↔ 74.7 GPa [카드 산술]) · ν 0.25 같음 · EEPA = 우리 hooke/hysteresis 와 같은 이력 계열 + 점착 가지 · λp 0.96 · 우리 18 배 연화는 SE 쪽 — 이 논문엔 대응물 없음 (he2026 L363 의 대칭 관계와 같다) · ★★ **힘 사슬 관측량을 우리 DEM 출력에 둘 때의 함정 넷**: 수 몫 ↔ 하중 몫 · P(f) 분모 (입자 ↔ 접촉) · F′zz 부호 뜻 · 응력 텐서 정규화 (σzz(LW)/판 압력) | 하중 몫 · 상별 값 0 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 반례: **벽 (강철 판 · Al 면) 접촉 매개변수를 하나도 적지 않은 DEM** — 판 · 벽 접촉 규칙 (마찰 · 구름 · 반발 · 점착 · 분리) 을 등록 칸으로 둘 이유 · 그 빈칸을 he2026 이 0.61 / 0.12 / 0.65 · JKR 1.5 J/m² 로 채워 이 논문을 출처로 달았다 (카드 문제 ①) | 값 없음 |
| **후보 A** (MPM 강체 AM · SE 한 속도장) | ★ **'단단한 쪽 ↔ 넘겨받는 연속체' 한 방향 꼴의 문헌 실례** — DEM 안의 집전체 = 단단한 stl (변형 0) · FEM 에서만 변형 → DEM 박힘 (겹침 0.847 µm) ↔ FEM 구멍 (1.84 µm) **2.2 배** [카드 산술] · 변형이 하중 경로로 돌아오지 않는다.  우리 AM 동결 scaffold (MPM 이 AM 을 단단한 장애물로 · DO-NOT ②: AM 하중 0 → SE 100 %) 와 **같은 부류의 문제 — 동결된 쪽이 하중 · 변형 되먹임을 받지 못한다** [카드 해석 · 우리 — CLAUDE.md DO-NOT] | AM 하중 몫 값 없음 · 한 방향 |
| **후보 A′** (입자별 속도장 · 다물체 마찰 접촉) | 없음 | — |
| **후보 B** (입자별 FE + 접촉) | 이 논문은 아님 (FE = 집전체만) · **양방향** DEM-FEM 선례 = [29] Song 2023 (*"a DEM-FEM bidirectional coupled model to simulate particle embedding in the current collector"* p.2 · 카드 없음 · n 후보) · DEM 하중 → 집전체 결정립 소성 FE (CPFEM) 의 선행 = [49] Yang 2023 (*"incorporated load distributions from DEM into a crystal plasticity finite element model (CPFEM) to capture the current collector's stress response and plastic evolution at the grain scale"* p.2 · 저자 이름 K. Yang · X. Du · Y. Zhang 이 이 논문 저자와 같음 · 카드 없음) | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | EEPA 를 *"large deformation"* 용으로 부르지만 범위 · 상한 없음 · 최대 입자–벽 겹침 0.847 µm = D50 반지름 3.6 µm 의 **0.24** [카드 산술 · 그 입자의 크기는 미상] — '큰 변형' 주장의 크기 자리표 | 겹침 · 밀도 상한 · 다접촉 보정 없음 |
| **후보 C′** (항복 캡 탄소성 접촉 DEM · Thornton–Ning · 다접촉) | EEPA = **항복 캡 없는 조각 이력** [다른 카드 `morrissey2013_…` · `schreiner2020_…` L71] · λp 0.96 의 '소성' = 제하 강성비 · 캡 · 다접촉 없이 문헌 값만으로 판 압력–두께 맞춤 곡선이 60–70 µm 에서 **+4.9 · −6.5 %**, 80–90 µm 에서 **−17.7 · −41.7 %** [판독 · 카드 산술] (원문 '3.66 %') | AM 단독 · 기공 ≥ 17 % (조밀 영역 아님) · 맞춘 매개변수 이름 없음 |
| **후보 M0** (균질화 압밀 · 캡 · Heckel) | crude Heckel P_y — 실험 ≈**236** · DEM ≈**285–333 MPa** [카드 산술 · 압력 = 누른 채 · 기공 = 뺀 뒤 (실험) / 미상 (DEM)] · 롤 압연 경험식은 정본 `meyer2017_…` ([22]) · `meyer2018_…` ([11]) · DEM + FEM 롤 압밀 = [78] Mazor 2018 (카드 없음 · n 후보) | 다른 상 (NMC 골격) — 우리 순수 SE P_y 138 MPa 와 나란히 인용 금지 |
| **U0–U6** | **U3 의 실측 꼴** — 단단한 입자가 무른 판 (Al) 에 박혔다 떨어진 뒤의 **잔류 구멍** 깊이 · 지름 (CLSM · 압하율별 0.96 / 1.25 / 2.32 µm · 입경별 1.32 / 1.70 / 2.59 µm [판독]) · 재료 (NMC → Al) · 측정 (손 선 따기 · 한 줄 / 여러 줄 최대) 이 우리 U3 (단단한 구 → 소성 블록) 와 다르다 · **U1 · U6 유비**: 3 µm 계면 격자 = D50 지름당 2.4 칸 · 계산 구멍 지름 2.9 µm < 한 칸 [카드 산술] → 박힘 · 접촉을 푸는 **해상도 칸** 을 등록할 이유 | 해석해 · 수렴 시험 없음 |
| **R1** (AM 이 움직이며 하중을 나눠 짐) | 정성 — *"particles close to the collector … almost no displacement … still form part of the force chain structure"* (p.11) · 강한 사슬이 30 % 뒤 바닥으로 (정량 판정 없음) | 하중 몫 0 |
| **R2** (미끄럼 · 분리) | 식 A.9–A.11 (점착 쿨롱 한계 · 구름 토크) · 분리 · 제하 계산 없음 | — |
| **R3** (SE 입자 경계 기억) | 없음 | — |
| **R4** (탈압 · 되돌아옴) | 없음 (λp 만) | — |
| **R5** (맞추는 값은 모델마다 하나) | 맞춘 값 이름 **없음** (표 1 = 문헌 값 · 출처 어긋남 하나 = [86] 의 8 ↔ 5 J/m²) · 절 제목만 'calibration' | — |
| **R6** (SE 형상 변형) | 없음 (단단한 구) | — |
| **R7** (AM 파괴) | 없음 (*"does not necessarily accompany particle fracture [97,98]"* p.9) · 집전체 손상 문턱도 없음 (저자 한계 ②) | — |
| **결과 전 대조 항목** | ① **σzz(LW · 접촉 합) ÷ 판 압력** — 우리 DEM 침대마다 결과 전 점검 (이 논문 0.095 · `zhang2026_…` ≈1.0 [다른 카드]) ② **강한 사슬의 수 몫과 하중 몫을 둘 다** (f > 1 · 분모 = 접촉) — 우리 f_AM (a) · (b) 옆에 ③ **고체 보존 기공 점검** ε = 1 − (1 − ε₀)/(1 − 압하율) ④ **직물 편차의 부호 규약** (⟨n_z²⟩ = 1/3 + F′zz) — 출력에 넣기 전에 적는다 | 값 전이 0 (모두 정의 · 점검) |

- **재료 · 차원 · 조건 차이**: 계 (액체계 LIB 양극 ↔ 황화물 ASSB 복합 양극) · 무른 상 (CB 5 wt% · E 0.45 GPa ↔ LPSCl 수십 vol% · 18 배 연화) · AM (NMC532 · D50 7.2 µm ↔ NCM811 AM_P/AM_S 이봉) · 공정 (롤 · 두께 목표 · 평판 근사 ↔ 다이 · 압력 목표 300 MPa) · 경계 (DEM RVE x · y 주기 + 위 강철 판 + 아래 단단한 Al 면 ↔ 우리 가로 주기 + 판) · 상태 (압력 단계마다 따로 누른 상태 · 실험은 뺀 뒤 ↔ 우리 누른 채 / hold 이완) · 3D (같음) · 온도 (상온 · 같음).
- **우리 계획 문장과의 접점 [카드 해석]**: [DEM 우선 (수영)] 피드백 ① *"지금 DEM → MPM 은 결합이 아니라 후처리"* [우리 — CLAUDE.md 11-09] — 이 논문의 DEM → FEM 은 **같은 부류의 한 방향 후처리** 이고, 그 비용이 '박힘' 의 정의 갈림 (겹침 0.847 ↔ 구멍 1.84 µm) 으로 숫자에 남았다.  피드백 ② (*"가압부터 한 모델"*) 의 반대편 예로 인용할 수 있다 (판정이 아니라 사례).

## 9. 적용 인사이트 (행동)
1. **he2026 의 입자–Al 값 (L99 · L100) 을 'Du 2025' 로 인용하지 않는다** — 이 논문에 없다 (§0-1 · 카드 문제 ①).  우리가 입자–판 · 입자–집전체 마찰 · 점착을 정할 때 그 값의 원전은 **[미확인]** 으로 둔다.
2. **힘 사슬 · 하중 분담 출력의 정의를 먼저 등록** (D0 · 단계 0) — 수 몫과 하중 몫을 같이 · P(f) 분모 = 접촉 · F′ 부호 · σzz(LW)/판 압력 점검 (우리 `stress_cv_lw` 계열 [우리 — CLAUDE.md J20-s ④b] 에 붙일 칸).
3. **우리 f_AM (b) = 이 논문 식 9 를 입자 상별로 나눈 것** — 같은 식이라 원자료 (*"on request"*) 가 오면 AM 몫을 계산해 우리 0.726–0.794 와 나란히 놓을 수 있다 (요청 여부 = 1저자 결정 · 이 카드는 값을 만들지 않는다).
4. **한 방향 넘김의 한계 문장** — 방향 메모 ([DEM 우선 (수영)]) 에서 'DEM 결과를 연속체로 넘기면 변형이 돌아오지 않고 접촉 · 박힘의 정의가 둘로 갈린다' 의 문헌 사례로 이 카드 §7-4 · §8 후보 A 줄을 쓴다.
5. **문헌 근사 조건은 우리 기하로 다시 계산** — 이 논문이 [75] 의 'θ < 1°' 를 지름 200 mm 롤에 옮겨 40 % 에서 1.62° 가 된 것처럼, 우리가 평판 · 준정적 근사를 인용할 때 근사 조건을 우리 두께 · 속도로 다시 센다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Du et al. coupled an EEPA-based DEM of an NMC532 : CB : PVDF (90 : 5 : 5) cathode — rigid spheres in a 100 µm periodic RVE compressed by a flat steel platen as an approximation of the roll — one-way to a static FEM of the 17 µm Al collector through EDEM–ANSYS axdt contact-force maps on a 3 µm one-to-one interface mesh (Du et al., *J. Energy Storage* 138 (2025) 118688)."
- "From 10 to 40 % compression the number of contact pairs rose from 23,940 to 41,816 and the fraction of contacts carrying more than the mean force fell from 21.49 % to 9.73 %, while the maximum collector stress reached 256.5 MPa; the strong-chain fraction is a count fraction, and no phase-resolved (AM–AM vs AM–CB) load partition was reported."
- 국문 (한정어와 함께): *"Du 2025 의 '강한 힘 사슬 몫' (21.49 → 9.73 %) 은 평균 힘을 넘는 접촉의 **수** 몫이다 — 하중 몫 · 상별 분담은 원문에 없다 (액체계 NMC532 양극 · 평판 근사 DEM · 한 방향 DEM → FEM)."*
- ⛔ 쓰지 말 것: *"입자–Al 마찰 0.61 / 구름 0.12 / 반발 0.65 (Du 2025)"* · *"Du 2025 의 AM–AM 하중 분담"* · *"강한 사슬이 하중의 9.73 % 를 진다"* · *"DEM 이 실험 압력 곡선을 0.073 % 안으로 맞춘다"* · *"최적 입경 9.9 µm"* 를 우리 계 (황화물 · 다이) 에 · *"30 % 를 넘으면 강한 사슬이 집전체로 옮긴다"* 를 정량 판정처럼.

## 11. 주의/한계 (over-claim 방지)
1. **SE 없음 · 액체계 · NMC532** — 우리 황화물 복합 양극과 무른 상 · 조성 · 공정이 다르다.
2. **롤 → 평판 근사 · 한 방향 정적 FEM** — 롤 곡률 · 회전 · 접선 · 출구 되돌아옴 · FEM → DEM 되먹임 없음.
3. **힘 사슬 정의**: '밀도' = 모든 접촉 · '강한 몫' = 수 몫 · P(f) 분모 = 입자 · F′zz 해석 반대 · σ 정의 없음.
4. **응력 정규화**: σzz 가 판 압력의 0.09–0.25 배 — 절대 응력으로 쓰지 않는다.
5. **매개변수 결손**: 벽 접촉 · k · n · 감쇠 · 시간 간격 · 입자 수 · 판 속도 · FEM 구성식.
6. **검증 지표 정의 없음** ('3.66 %' · '0.073 %') · 판독 곡선 차는 저압에서 −18 · −42 %.
7. **본문 ↔ 그림 어긋남 15 가지** (§3-11) — 값을 옮길 때 그림과 본문 가운데 무엇을 옮겼는지 적는다.
8. 그림 값은 **판독** (300 dpi 래스터) · 시드 · 오차 없음.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [29] | Y. Song, K. Gao, C. He, Y. Wu, S. Yang, N. Li, et al., Exploring particle-current collector contact damage in Li-ion battery using DEM-FEM scheme, Appl. Energy 351 (2023) 121904, https://doi.org/10.1016/j.apenergy.2023.121904. | **양방향** DEM-FEM 입자 박힘 — 질문 h · 후보 B · 이 논문의 직계 선행 · 카드 없음 (wishlist L107 에 이미 있음) |
| [100] | N.P. Kruyt, On weak and strong contact force networks in granular materials, Int. J. Solids Struct. 92–93 (2016) 135–140, https://doi.org/10.1016/j.ijsolstr.2016.02.039. | f = 1 강 · 약 망 문턱의 원전 · 강한 망이 지는 응력 몫의 정의 — 질문 d · 카드 없음 |
| [78] | A. Mazor, L. Orefice, A. Michrafy, A. De Ryck, J.G. Khinast, A combined DEM & FEM approach for modelling roll compaction process, Powder Technol. 337 (2018) 3–16, https://doi.org/10.1016/j.powtec.2017.04.053. | DEM + FEM 롤 압밀 — 질문 h · 후보 M0 · 카드 없음 |
| [56] | J. Zhang, J. Sun, H. Huang, C. Ji, M. Yan, Z. Yuan, Deformation and fracture mechanisms in the calendering process of lithium-ion battery electrodes, Appl. Energy 373 (2024) 123900, https://doi.org/10.1016/j.apenergy.2024.123900. | 도막 · 집전체 DEM-FEM 결합 틀 (*"Zhang et al. [56] developed a coupled modeling framework"* p.2) · 파괴 기전 — 질문 h · R7 · 카드 없음 |
| [25] | R. Ge, D.J. Cumming, R.M. Smith, Discrete element method (DEM) analysis of lithium ion battery electrode structures from X-ray tomography-the effect of calendering conditions, Powder Technol. 403 (2022) 117366, https://doi.org/10.1016/j.powtec.2022.117366. | 입자–입자 μ 0.25 · μr 0.01 · COR 0.25 (이 논문 · he2026 공통 출처) · 힘 정규화 (식 4–5) — 질문 e · 카드 없음 |
| [27] | J. Zhang, H. Huang, J. Sun, Investigation on mechanical and microstructural evolution of lithium-ion battery electrode during the calendering process, Powder Technol. 409 (2022) 117828, https://doi.org/10.1016/j.powtec.2022.117828. | λp 0.96 · PVDF = γ · f₀ · '큰 변형' 주장의 근거 — 질문 e · l · 카드 없음 (wishlist L232 에 이미 있음) |
| [41] = [85] | S.C. Thakur, J.Y. Ooi, H. Ahmadian, Scaling of discrete element model parameters for cohesionless and cohesive solid, Powder Technol. 293 (2016) 130–137, https://doi.org/10.1016/j.powtec.2015.05.051. | EEPA 매개변수 척도화 · 이 논문은 압하율 범위 (10–35 %) 문장에만 인용 — 질문 e · 카드 없음 |
| [102] | J. Christoffersen, M.M. Mehrabadi, S. Nemat-Nasser, A micromechanical description of granular material behavior, J. Appl. Mech. 48 (2) (1981) 339, https://doi.org/10.1115/1.3157619. | 식 9 (입상체 평균 응력) 원전 — 우리 LW · 상별 virial 의 정의 근거 · 카드 없음 (`zhang2026_…` · `zunker2024_mdr_contact_model_partI` · `zunker2025_…` 가 이름 언급) |
| [99] | K. Ken-Ichi, Distribution of directional data and fabric tensors, Int. J. Eng. Sci. 22 (2) (1984) 149–164, https://doi.org/10.1016/0020-7225(84)90090-9. | 직물 텐서 (식 6) 원전 · 카드 없음 |
| [49] | K. Yang, X. Xie, X. Du, Y. Zuo, Y. Zhang, Research on micromechanical behavior of current collector of lithium-ion batteries battery cathode during the calendering process, Processes 11 (6) (2023) 1800, https://doi.org/10.3390/pr11061800. | 같은 이름의 저자 셋 · DEM 하중 → 집전체 CPFEM (결정립 소성) — 질문 h · 이 논문 FEM 의 Al 구성식 단서 · 카드 없음 |
| [87] · [88] | D. Schreiner, J. Lindenblatt, F.J. Günter, G. Reinhart, DEM simulations of the calendering process: parameterization of the electrode material of lithium-ion batteries, Procedia CIRP 104 (2021) 91–97 · D. Schreiner, J. Lindenblatt, R. Daub, G. Reinhart, Simulation of the calendering process of NMC-622 cathodes for lithium-ion batteries, Energy Technol. 11 (5) (2023) 2200442 | 표면 에너지 60 · 20 J/m² · f₀ 10⁻⁵ N 의 출처 — 카드 없음 |
| 카드 있음 | [10] Diener 2022 (`diener2022_roll_gap_springback_calendering`) · [11] Meyer 2018 (`meyer2018_…`) · [22] Meyer 2017 (`meyer2017_…`) · [75] Giménez 2019 (`sangros2019_dem_calendering_lib_electrode`) · [84] Thakur 2014 (`thakur2014_eepa_adhesive_elastoplastic_dem`) · [86] Schreiner 2020 (`schreiner2020_dem_calendering_lib`) · [90] Lyu 2025 (`lyu2025_3d_dem_drying_calendering_lib`) | 열어서 견줄 것 — §0-1 · §3-2 · §7-3 |

## 13. [미확인] 목록 (본문 19 쪽 전수에 없음)
1. 입자 수 (AM · CB) · 시드 수 · 계산 시간 · 시간 간격 (Rayleigh 비) · 판 속도 · 판 정지 · 유지 · 제하 규약.
2. EEPA 강성 k₁ · k₂ · k_adh · 지수 n · 법선 · 접선 감쇠 · 접선 강성.
3. 입자–벽 (강철 판 · Al stl) 접촉 매개변수 전부 (μ · μr · COR · γ) — he2026 L99 · L100 의 값 포함.
4. DEM 기공 연산자 · 상태 (누른 채 / 뺀 뒤) · 실험 기공 계산의 진밀도 (2.42 ↔ 4.75 g/cm³).
5. 실험 압력 환산식 (선하중 → MPa) · 그림 5c 실험 점 다섯이 어느 압하율인지.
6. 검증 편차 '3.66 %' · '0.073 %' 의 정의 · 기준점.
7. FEM Al 구성식 (탄성 / 탄소성 · 항복 · 경화) · 요소 수 · 두께 방향 격자 · 비선형 여부.
8. 강한 사슬 몫 (그림 6k) 의 계산식 · 분모 · σ (식 9) 의 정의와 V.
9. 응력 집중점 · 손상점 · 계산 구멍의 판정 문턱 · 규칙.
10. 그림 8m (구멍 수) 이 계산인지 실험인지.
11. 입도 폭 σ 의 단위 · 그 계산의 평균 입경 (본문 *"the 11 μm case"* 로 읽힘) · 그림 10m–n 의 압하율 (본문 흐름상 40 %).
12. 면적 하중 (mg/cm²) · 전극 밀도 · 양면 / 단면 도포.
13. '30 % 뒤 강한 사슬의 집전체 쪽 이동' 의 정량 판정 (높이별 분포 등).
14. he2026 원문의 [41] 이 정말 이 논문인지 (he2026 PDF 가 이 트리에 없다 · 그 카드 L368 · L689 의 기록만).

## 14. 🧮 카드 산술 원장 (원문 숫자 · 판독값만으로 · 재현 = 식 그대로)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | 고체 부피 몫 = (w/ρ)/Σ(w/ρ) · AM 90/4750 · CB 5/2250 · PVDF 5/1760 | AM **0.789** · CB 0.093 · PVDF 0.118 | 표 1 밀도 + p.3 PVDF |
| D2 | CB 수 / AM 수 = (5/2250/2.5³)/(90/4750/7.2³) | **2.80** | D50 · 단분산 가정 |
| D3 | θ = cos⁻¹((R − S)/R) · R 100 mm · S 10–40 µm | **0.81 · 1.15 · 1.40 · 1.62°** · 1° 는 S = 15.2 µm | 식 1 · [75] 의 'θ < 1°' |
| D4 | 접촉 길이 √(R·S) · 선하중 ÷ 길이 | 1.000 · 1.414 · 1.732 · 2.000 mm → **14.0 · 77.8 · 154.7 · 265.0 MPa** | 환산 가정 (원문에 없음) |
| D5 | 접촉 쌍 비 | 41,816/23,940 = **1.747** · 단계비 1.315 · 1.152 · 1.153 | 인쇄 '+76.5 %' |
| D6 | ⟨n_z²⟩ = 1/3 + F′zz | **0.382 · 0.363 · 0.331 · 0.304** | 판독 F′zz |
| D7 | 직물 대각 합 | \|−0.0041\| · \|−0.0004\| · 0.0003 · 0.0001 | 판독 점검 (0 이어야) |
| D8 | P(f) 삽입 · 40 % | f ≤ 1 여섯 칸 합 **0.686** · f 1.08–1.42 세 칸 합 **0.128** · 아홉 칸 합 0.813 | ↔ 그림 6k 9.73 % |
| D9 | P(f) 삽입 · 10 % (f 0.08–0.75 다섯 칸) | 0.638 | |
| D10 | σzz / DEM 판 압력 (맞춤 곡선 12.3 · 57.7 · 140.0 · 270.0) | **0.251 · 0.122 · 0.086 · 0.095** (40 % 점 270.5 기준 0.0945) | 그림 6m · 5c 판독 |
| D11 | σ / σzz · 대각 합 · 평균 · von Mises | σ/σzz 11.3 · 7.1 · 8.3 · 7.1 · 합 7.4 · 16.7 · 32.2 · 67.3 · 평균 2.5 · 5.6 · 10.7 · 22.4 · vM 0.96 · 2.20 · 2.05 · 4.69 MPa | σ 34.9 · 50.1 · 100.0 · 180.3 와 어느 것도 안 맞음 |
| D12 | 측압 비 K = (σxx + σyy)/(2σzz) · σzz/σxx | K **0.69 · 0.69 · 0.83 · 0.82** · σzz/σxx 1.41 · 1.44 · 1.17 · 1.21 | `zhang2026_…` K 0.40 → 0.68 [다른 카드] |
| D13 | 맞춤 곡선 상대 차 (DEM − 실험)/실험 · 60 · 70 · 80 · 90 µm | **+4.9 · −6.5 · −17.7 · −41.7 %** | 인쇄 '3.66 %' |
| D14 | 고체 보존 기공 1 − (1 − ε₀)/(1 − CR) | DEM (ε₀ 0.520) 46.7 · 40.0 · 31.5 · 20.1 % → 판독과 차 **+1.6 · −3.5 · −3.9 · −1.2 %p** · 실험 (0.500) 44.4 · 37.5 · 28.6 · 16.7 % → +0.9 · +0.2 · −2.7 · +0.2 %p | 그림 5d 판독 |
| D15 | Heckel ln(1/ε) = K·P + A (10–40 % · 압력 = 맞춤 곡선) | 실험 K 0.00424 → **P_y 236 MPa** (R² 0.999) · 20–40 % 234 · DEM 맞춤 0.00351 → **285** (0.978) · 20–40 % 324 · DEM 점 294 · 333 | 섞인 상태 (누른 채 압력 · 뺀 뒤 / 미상 기공) |
| D16 | 접촉 E* | AM–AM 142/(2·0.9375) = **75.7** · 우리 140 → 74.7 · AM–Al 51.2 · AM–강철 86.2 · CB–CB 0.234 GPa | 표 1 |
| D17 | λp = 1 − k₁/k₂ = 0.96 | k₂/k₁ = **25** · 회복 몫 1 − λp = 0.04 (n = 1) | 식 A.7 |
| D18 | 그림 8m 증분 · 기울기 | 10 → 20 % +295.5 · 20 → 30 % **+102.3** · 30 → 40 % +94.4 · 기울기 (개/%) 10–20 % 29.6 · 21–25 % 4.7 · 25–30 % 14.7 · 30–35 % 12.9 · 35–40 % 6.0 | 본문 '20 % 379 · 20–30 % 변화 없음' |
| D19 | 그림 8n–o 계산 − 실험 | 깊이 −0.16 · +0.05 · **−0.48** µm (−17 · +4 · −21 %) · 지름 −0.91 · **−1.65** · −1.39 µm (−24 · −30 · −18 %) | 인쇄 최대 편차 0.47 · 1.68 |
| D20 | FEM 구멍 깊이 / DEM 최대 겹침 (40 %) | 1.843/0.847 = **2.18** | 그림 8n · 9 |
| D21 | 겹침 / D50 반지름 | 0.847/3.6 = **0.24** | 그 입자 크기 미상 |
| D22 | 3 µm 격자 · 입경 | D50 7.2 → 2.4 칸 · D10 3.5 → 1.2 칸 · 계산 구멍 2.90 µm < 1 칸 | §3-4 |
| D23 | 그림 10o 비 · 그림 11h 증분 | 245.3/169.5 = 1.447 (인쇄 1.45) · 파랑 167.0 − 51.9 = **+115.1** · 주황 212.5 − 73.2 = **+139.3** | 범례 짝 ↔ 본문 |
| D24 | 그림 11g σ = 4 반치폭 → 표준편차 | 반치 교차 4.77 · 12.23 µm → FWHM 7.46 → sd **3.17 µm** | 정규 분포 가정 · 인쇄 5 µm |
| D25 | 그림 8j–l 40 % 깊은 골 셋 평균 | (1.83 + 1.54 + 1.45)/3 = **1.61 µm** | 인쇄 '평균' 1.86 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 19 쪽을 글자 층 (PyMuPDF) + 쪽 렌더 + 내장 래스터로 읽음.  서지 = PDF 1 쪽 (제목 · 저자 다섯 · 소속 넷 · 이력 · 키워드 · DOI · © 줄) + PDF 메타데이터 (*"Journal of Energy Storage, 138 (2025) 118688. doi:10.1016/j.est.2025.118688"* · 작성 2025-10-30) + 쪽 머리글 *"H. Du et al. Journal of Energy Storage 138 (2025) 118688"*.  보충 자료 · 데이터 파일 없음.
- ★ 입자–Al 접촉 값 확인: 표 1 을 벡터 렌더 (400 dpi · `tab_1.png`) 로 열어 줄을 셈 (재료 넷 × 3 + 입자–입자 8) · 19 쪽 글자 층에서 *"0.61"* · *"0.65"* · *"0.12"* · *"JKR"* · *"1.5 J"* · *"restitution"* (1 건 = 표 1 입자–입자) 를 찾음 → he2026 L99 · L100 값 0 건.
- 그림 판독: 전부 내장 래스터 (xref 47 · 60 · 79 · 105 · 114 · 127 · 158 · 199 · 203 · 218 · 222 · 300 dpi) — 축 눈금 화소 · 방법은 `digitized.csv` 행마다.  점검: 그림 6j 대각 합 ≈ 0 · 그림 8j–l 의 0 점선 0.00 ± 0.02 µm · 그림 10o 비 1.447 = 인쇄 1.45 · 그림 8n–o 최대 편차 크기 = 인쇄 0.47 · 1.68.
- 크롭 70 장 (§5-1) · 전부 열어 확인 · 모음 그림 두 장.
- 참고문헌 109 개를 글자 층에서 번호별로 나눠 읽음 — 중복 셋 ([41] = [85] · [82] = [88] = [93] · [28] = [66]).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (ls-tree · 547 개) + DOI (`est.2025.118688`) · "118688" · "Force chain-induced" · 제1 저자 "Du" grep — **이 논문 카드 없음** (he2026 L99 · L100 · L368 · L689 에 인용만) · `du2022_lmro_lpscl_reversible_redox_assb` 는 다른 저자 · 다른 논문 (slug 를 다르게 함).

## 🔗 관련 카드
- 이 논문을 가리킨 카드: [`he2026_dem_calendering_inhomogeneity_areal_density`](he2026_dem_calendering_inhomogeneity_areal_density.md) — N5 (L689) · 입자–Al 마찰 · JKR · f₀ 의 [41] 출처 (L98–L100) · 힘 사슬 · 하중 분담 칸 (L368) — 이 카드 §0-1 이 대조 (입자–Al · JKR 은 이 논문에 없음 · f₀ 다름 · 하중 분담 없음).
- 같은 꼴의 액체계 압연 DEM: [`zhang2026_xct_dem_cathode_calendering_peel_calibration`](zhang2026_xct_dem_cathode_calendering_peel_calibration.md) (σzz/판 압력 ≈1.0 · 매립 0.937 µm) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) (CT + DEM 힘 사슬 · Song 2023 을 인용한 카드) · [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) ([75]) · [`schreiner2020_dem_calendering_lib`](schreiner2020_dem_calendering_lib.md) ([86]) · [`lyu2025_3d_dem_drying_calendering_lib`](lyu2025_3d_dem_drying_calendering_lib.md) ([90]).
- 압연 경험식 · 되돌아옴: [`meyer2017_calendering_compaction_resistance_line_load_exponential_model`](meyer2017_calendering_compaction_resistance_line_load_exponential_model.md) ([22]) · [`meyer2018_calendering_process_model_active_material_mass_loading`](meyer2018_calendering_process_model_active_material_mass_loading.md) ([11]) · [`diener2022_roll_gap_springback_calendering`](diener2022_roll_gap_springback_calendering.md) ([10]).
- EEPA 원전 · 혼합: [`thakur2014_eepa_adhesive_elastoplastic_dem`](thakur2014_eepa_adhesive_elastoplastic_dem.md) ([84]) · [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) · [`yano2024_eepa_binary_mixture_plasticity_compression_dem`](yano2024_eepa_binary_mixture_plasticity_compression_dem.md) (이원 혼합 · 하중 몫 같은 빈칸).
- DEM → 연속체 넘김 (수송 쪽): [`bazzoun2026_dem_fem_rnm_ionic`](bazzoun2026_dem_fem_rnm_ionic.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
