<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 후보 표 N-89 (정독 138) 에서 꼭 뽑을 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음 카드들과 같은 꼴.
     원문 = 출판본 (J. Electrochem. Soc. 169 (2) 020539 · 2022 · ECS / IOP · PDF 14 쪽 = IOP 표지 1 + 논문 13 쪽) + Supporting Information (PDF 15 쪽 = 표지 1 + S-1 … S-14).
     쪽 표기 = 본문 "p.N" = PDF 쪽 N (p.1 = IOP 표지 · 논문 첫 쪽 = p.2 · 논문 자체엔 쪽 번호가 인쇄되지 않는다).  SI "SI p.N" = SI PDF 쪽 N (인쇄 S-(N−1) · SI p.1 = 표지).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 319 행 — 벡터 그림 = 경로 좌표 + 눈금 최소제곱 ·
     래스터 그림 = 300 dpi 렌더 + 눈금 표시 최소제곱 + 색 덩이 중심 · Fig. 11 · SI Fig. S8 = 화면 눈금 보간 ±3 mAh g⁻¹) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) ·
     [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 13 쪽 + SI 14 쪽 전수에 없음.
     원문 27 쪽 (표지 둘 제외) 은 글자 층 추출 + 그림 · 식 렌더로 전부 읽었다.  DEM · 역학 · 압밀 · 가압 · 탈압은 없다 — 정해진 기하 위의 전기화학 (정전류 충전) FEM. -->
# NCM811 / Li₆PS₅Cl 복합 양극 충전의 3D FEM 전기화학 (COMSOL 5.4 · GeoDict 구 입자 재구성 · 맞춘 값 0) — SOC 의존 D̃_Li · j₀ (같은 재료 GITT · EIS 입력) 가 곡선 모양을 정하고 · 입도 분포의 드문 큰 입자가 CAM 표면적 −35 % · 1-입자 반구 공극 (남은 계면 53 % 에서 0.2 C 공극 과전압 ≈47 mV [판독]) · 같은 덮임에서 큰 공극 둘 > 작은 공극 160 · 원뿔형 구조 전극 (a 2–20 µm · "below 5 µm" 권고) — microstructure · tortuosity 설계 (Bielefeld · Weber · Rueß · Glavas · Janek, J. Electrochem. Soc. 2022)

> slug `bielefeld2022_li_kinetics_morphology_voids_fem_composite_cathode` · DOI `10.1149/1945-7111/ac50df` · type `FEM 3D electrochemical charge simulation (COMSOL 5.4 · Butler–Volmer + CAM solid diffusion + SE Ohmic ion transport · GeoDict particle microstructure · 1-particle void model · cone-type unit cell) — no DEM · no mechanics · no pressure` · PDF `d453ae79-89._Influence_of_lithium_ion_kinetics_particle_morphology_and_voids_on_the_electrochemical_performance_of_composite_cathodes_for_all-solid-state_batteries.pdf` · SI `4481d6ea-89._Sup_Influence_of_lithium_ion_kinetics_particle_morphology_and_voids_on_the_electrochemical_performance_of_composite_cathodes_for_all-solid-state_batteries.pdf` · digested `2026-11-22` · status ✅
>
> **저자**: Anja Bielefeld ¹,²,\* · Dominik A. Weber ³ · Raffael Rueß ¹,² · Vedran Glavas ³ · Jürgen Janek ¹,²,\* — ¹ Physikalisch-Chemisches Institut, Justus-Liebig-Universität Giessen · ² Center of Materials Research (LaMa), JLU Giessen · ³ Volkswagen AG, Wolfsburg — \* 교신 (anja.bielefeld@ · juergen.janek@phys.chemie.uni-giessen.de) · *J. Electrochem. Soc.* **169** (2) **020539** (2022, 13 쪽) · 접수 2021-12-02 · 수정 2022-01-05 · 출판 2022-02-16 · © ECS (IOP) · 연구비 = Volkswagen AG · BMBF FESTBATT (03XP0177A) · ProFeLi (03XP0184C) · 감사에 Philip Minnmann (JLU).
> **이웃 카드 (링크만)**: 이 논문을 가리킨 카드 = [`kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage`](kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage.md) (L279 · L115) · [`lee2024_shear_force_dry_process_cathode_coverage`](lee2024_shear_force_dry_process_cathode_coverage.md) (L390 · L415) · 같은 1 저자 앞 두 편 = [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (ref 24 · SI [3]) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) (ref 25 · SI [6]) · 입력값을 이 논문에서 옮긴 카드 = [`benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`](benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md) · [`benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode`](benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode.md) · [`taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode`](taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode.md) · 공극 논거로 인용 = [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (ref 12) · [`lin2025_submicron_lpscl_cathode_li_kinetics`](lin2025_submicron_lpscl_cathode_li_kinetics.md) (ref 17) · [`reisacher2023_percolation_sulfide_carbon_matrix`](reisacher2023_percolation_sulfide_carbon_matrix.md) (ref 11).
> **판독 원자료**: `litdb/figures/bielefeld2022_li_kinetics_morphology_voids_fem_composite_cathode/digitized.csv` (319 행 — Fig. 7a D̃_Li · j₀ 표지 + 상수선 · SI Fig. S2 OCV 표지 · Fig. 5a 막대 (밀도 히스토그램 → 입자 수) · 끝 용량 Fig. 5b–d · 7b–f · 10 왼쪽 (벡터) · Fig. 10 오른쪽 · 8 오른쪽 · 9 오른쪽 표지 (래스터) · Fig. 11 · SI Fig. S8 (눈 판독)) · 그림 크롭 **71 장** (도구 17 중 다시 자름 7 + 손 크롭 54 = 표 · 그림 6 · 패널 5 · 식 23 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 다결정 NCM811 / Li₆PS₅Cl 복합 양극의 정전류 충전을 3D FEM (COMSOL 5.4) 으로 푸는데, 입력은 **같은 재료의 측정** (Rueß 2020 의 GITT · EIS · OCV · σ_SE 0.7 mS cm⁻¹ · Conforto 2021 의 입도) 을 그대로 쓰고 *"none of the simulation input has been fitted"* (p.5) — ① GeoDict 로 만든 구 입자 배치 (CAM 42 vol% · 40³ µm³ · **SE 는 남은 부피를 이상 접촉으로 채움 = 모델 기공 0**) 가 실험 (70 : 30 wt% · 공극 14 %) 의 0.02 · 0.1 · 0.5 C 곡선을 따라가고 (끝 용량 sim ≈190 · ≈166 · ≈106 ↔ exp ≈195 · ≈173 · ≈114 mAh g⁻¹ [판독]), ② 곡선 **모양**은 미세구조가 아니라 **SOC 의존 D̃_Li · j₀** 가 정하며 (상수 입력은 첫 전압 상승을 못 낸다 · 측정 신뢰성이 *"potential Achilles heel"*), ③ 입도 분포의 드문 큰 입자가 부피를 차지해 CAM 표면적이 S → L 에서 **0.173 → 0.113 m² g⁻¹ (−35 %)** 로 줄고 과전압이 커지고 (Table I · Fig. 5–6), ④ 7 µm 단일 입자 표면의 1.4 µm 반구 공극이 남은 계면을 **53 %** 까지 줄이면 0.2 C 공극 과전압 **≈47 mV (@50 mAh g⁻¹) · ≈40 mV (@100)** [판독 Fig. 8] — 같은 30 % 덮임에서 큰 공극 둘이 작은 공극 160 개보다 과전압이 크고 (Fig. 9), ⑤ 55 vol% 원뿔형 구조 전극은 집전체 쪽 지름 **a = 2 µm** 면 1 C 까지 평평하고 **a ≥ 10 µm** 면 나쁘다 → *"below 5 μm"* 권고 (p.12).  **역학 · 가압 · 탈압 · SE 입자 · 접촉 협착은 모델에 없다** (공극 = 고정 반구 구멍).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 모델 · 식 | SE = 단일 이온 Ohm 전도체 [4] (공간 전하 무시) · CAM = 고체 확산만 [5][6] + 전자 Ohm [7] (σ_CAM 100 S m⁻¹ 로 크게 → 전자 한계 못 봄) · 계면 Butler–Volmer [8]–[10] · j₀ 꼴 [11] · R_CT = RT/(zFAj₀) [12] · 음극 Li 석출 BV (j₀ᵃ 3 A cm⁻² · SOC 무관) · 외부 전류 = 매끄러운 계단 · x–y 주기 경계 | [인쇄] p.3–4 · SI 표 S1–S2 · 그림 S1 · S3 |
| ② 입력 (같은 재료 · 맞춤 0) | σ_SE **0.7 mS cm⁻¹** · j₀(SOC) **0.17–1.55 × 10⁻⁵ A cm⁻²** (= 0.017–0.155 A m⁻²) [판독 Fig. 7a] · D̃_Li(SOC) **0.075–6.9 × 10⁻¹² cm² s⁻¹** [판독] · OCV (x 0.22–0.99) · 200 mAh g⁻¹ · ρ_NCM 4.77 g cm⁻³ · c_ref 49 mol L⁻¹ · **T 273.15 K (인쇄 그대로)** · 4.2 / 3.5 V · 출처 표기 = Rueß 2020 | [인쇄] SI 표 S2 · [판독] Fig. 7a · SI Fig. S2 |
| ③ 미세구조 | 입자형: 40 × 40 × 40 µm³ + SE 분리막 10 µm + 집전체 1 µm · CAM 42 vol% 구 (S / M / L PSD · S 는 시드 셋) · 자리 표시 볼록 다면체 40 vol% 로 CAM 을 이어 붙임 (겹침 ≤ 3 %) · **고립 입자는 손으로 옮김** · 1-입자: d_CAM 구 + 반구 공극 · 원뿔형: 원뿔대 단위 셀 (주기) | [인쇄] p.4 · SI p.6–8 · 표 S3 · Fig. 1–3 |
| ④ 입도 → 표면적 · 이용률 | 입자 수 **266 / 249 / 248 / 177 / 128** · 표면적 **0.173 / 0.172 / 0.167 / 0.139 / 0.113 m² g⁻¹** (S a · b · c · M · L) · L 은 0.02 C 에서도 실험과 어긋남 · 큰 입자 속은 충전 끝에도 리튬화 유지 (Fig. 6) · [카드 산술] L 의 11 µm 넘는 9 입자 (수 7 %) = CAM 부피 62 % | [인쇄] Table I · p.6–8 · [판독] Fig. 5a · 6 |
| ⑤ ★ SOC 의존 입력 | 상수 네 벌 {D̃ 6.8 · 3.5 × 10⁻¹² cm² s⁻¹} × {j₀ 1.55 · 0.90 × 10⁻⁵ A cm⁻²} 과 비교 — 첫 과전압은 SOC 의존만 · 4.17 V 위는 상수가 더 맞음 · 실험에 가장 가까운 상수 = {평균 D̃ · 최대 j₀} (Fig. 7d) · D̃ 는 두 자릿수 변하고 측정 산포가 크다 → j₀ 맞춤을 *"rethought"* | [인쇄] p.8–10 · [판독] Fig. 7 · S6 |
| ⑥ ★ 공극 (1-입자) | 7 µm · 1.4 µm 반구 · 남은 계면 A 100 → 53 % · 0.2 C 공극 과전압 **4.8 → 46.6 mV (@50) · 9.4 → 39.5 mV (@100)** [판독] · 5 µm 입자는 같은 경향 · 작음 (A 50.6 % 에서 39.6 mV @50) · 공극 크기 비 d_CAM/d_Void **1.2 → 10** (A 70 %) 에서 0.2 C @100 **65.9 → 14.4 mV** [판독 로그 축] | [판독] Fig. 8 · 9 오른쪽 · [인쇄] p.10 · SI Fig. S7 |
| ⑦ 원뿔 구조 | 42 vol% 원뿔 (표면 0.17) = 입자형보다 과전압 '보통' 작음 · 55 vol% (b/a 0.6623) 표면 **≈0.51 / 0.21 / 0.11 / 0.07 m² g⁻¹** (a 2 / 5 / 10 / 20 µm) [판독] · 1 C 끝 용량 **≈153 / ≈90 / ≈32 / ≈11 mAh g⁻¹** [판독 Fig. 11] · 겹친 원뿔 (b 축소) 은 더 나쁨 · 현재 레이저 채널 ≈12 µm | [판독] Fig. 10 · 11 · SI Fig. S8 · [인쇄] p.11–12 · SI 식 (1)–(11) |
| ⑧ 저자 한계 | 공극의 이온 퍼콜레이션 영향은 못 본다 (p.10) · 구 2 차 입자 (거칠기 · 1 차 입자 없음) · 단순화는 과전압을 과소평가할 것 (구 형상만 반대 방향, p.8) · 원뿔엔 공극 없음 (p.12) · (화학–)역학 결합 필요 (p.13) · SE 미세구조를 풀지 않음 (기술적 이유, SI p.7) | [인쇄] p.3 · 8 · 10 · 12 · 13 · SI p.7 |

⛔ **한정어 (떼지 말 것)**: ① **역학 없음** — 공극 · 접촉 잃음은 압력 · 수축 계산이 아니라 **고정된 반구 구멍** ② SE = **이상 접촉 연속체** (펠릿 σ 0.7 mS cm⁻¹) — SE 입자 · 입계 · 접촉 협착 · 기공이 없다 (우리 말로 CONTACT_FREE 가지) ③ 입자형 모델 기공 **0 %** (실물 공극 14 % 자리를 SE 가 채움 · [카드 산술] 모델 SE 58 vol% ↔ 실물 SE ≈44 % + 공극 14 %) ④ 입력 출처 표기 = Rueß 2020 — 이 논문은 그 값들의 **2 차 출처** ⑤ T **273.15 K** 로 인쇄 — 실험 온도 [미확인] ⑥ 판독값은 경향용 · 정밀 인용 금지.
⇒ **절대값 전이 (역학 · 압밀 쪽): 0 건.**  전이되는 것 = 방법 (같은 재료 측정 입력 · 맞춤 0 · SOC 의존 입력 대조) · 함정 (j₀ 맞춤 · 큰 입자 부피 몫 · 공극 분포 · R_CT → j₀ 환산의 면적) · 결과 전 대조 항목 (표면적 · 공극 과전압 · 원뿔 면적).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-89 의 '왜' 칸)

의도 원문: *"수송 · 반응 — i₀,ref 0.05 A/m² 출처 (kim2024_optimal) · 공극 · 형태가 이용률에 미치는 3D 모델 (같은 질문의 3D 판 · lee2024) · 같은 1 저자의 2019 · 2020 카드는 있음"* (가리킨 카드 = kim2024_optimal L279 · lee2024_shear L390)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "수송 · 반응" | **채움** | SE 이온 Ohm 수송 [4] · CAM 고체 확산 [5][6] · 계면 BV [8] + j₀ [11] · 3D · 정전류 **충전**만 (방전 · 사이클 없음) · 압력 없음 · T 273.15 K (인쇄) · p.3–4 · SI 표 S2 |
| "i₀,ref 0.05 A/m² 출처 (kim2024_optimal)" | **없음** | 원문에 **0.05 A m⁻² (= 0.5 × 10⁻⁵ A cm⁻²) 라는 값은 인쇄되지 않았다** (본문 13 쪽 + SI 14 쪽).  j₀ 는 SOC 의존 곡선 (Fig. 7a · EIS 의 R_CT 에서 식 [12]) — 판독 **0.17–1.55 × 10⁻⁵ A cm⁻² = 0.017–0.155 A m⁻²** · 비교용 상수 j₀,₁ **1.55 × 10⁻⁵** (= 0.155 A m⁻²) · j₀,₂ **0.90 × 10⁻⁵ A cm⁻²** (= 0.090 A m⁻²) [인쇄 p.8] · 곡선이 0.05 A m⁻² 를 지나는 곳은 **≈3.65 V · ≈4.17 V** 두 점뿐 [판독] · 원 측정 출처 표기 = Rueß 2020 (SI 표 S2) |
| "공극 · 형태가 이용률에 미치는 3D 모델" | **채움 (한정)** | 공극 = **1-입자 3D** (7 · 5 µm 구 + 반구 공극 · 남은 계면 ≥ 53 / 50.6 % [판독] · 0.02–0.5 C (그림 8 오른쪽은 ≤ 0.2 C) · Fig. 8 · 9 · S7) · 형태 = 입도 (Fig. 5 · 6 · Table I — 큰 입자 속이 안 쓰임) + 원뿔 구조 (Fig. 10 · 11) · ⚠ 공극은 고정 반구 · 복합체 수준의 공극–퍼콜레이션 영향은 *"not capable to quantify"* (p.10) · '이용률' 은 끝 용량 · 농도장으로만 (이용률 숫자 표 없음) |
| "(같은 질문의 3D 판 · lee2024)" | **일부** | lee2024 (2D 단일 입자 COMSOL · 피복 10–100 % · 0.2–5 C · 이용률 [다른 카드 `lee2024_shear_force_dry_process_cathode_coverage` L44]) 와 같은 질문을 3D 단일 입자로 — 그러나 **범위가 겹치지 않는다**: 이 논문은 남은 계면 **≥ 53 %** · **≤ 0.5 C** · 공극 = 반구 구멍 (lee2024 = 단면 둘레 피복 몫) · 출력 = **공극 과전압** (lee2024 = 이용률 %) |
| "같은 1 저자의 2019 · 2020 카드는 있음" | **채움** | ref 24 (J. Phys. Chem. C 123, 1626 · 2019) = `bielefeld2019_…` · ref 25 (ACS AMI 12, 12821 · 2020) = `bielefeld2020_…` · SI 참고 [3] · [6] 도 같은 두 편 · 이 카드 = 같은 1 저자의 **2022 편 (다른 논문 · 같은 해 카드 없음)** |

**가리킨 카드 · 같은 값을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `kim2024_optimal_…` L279 (S8) | 서지 + *"i₀,ref 0.05 A/m² 출처"* | 서지 ✓ · **0.05 인쇄 없음** (위 표) | **없음 → 카드 문제** (Kim 2024 표 S2 의 인용인지 카드의 귀속인지 [미확인]) |
| `kim2024_optimal_…` L115 | 표 S2 물성 *"… D_s 5.5 × 10⁻¹⁴ m²/s · i₀,ref 0.05 A/m² …"* (출처 미표기) | 이 논문 D̃_Li 최대 **6.9 × 10⁻¹⁶ m² s⁻¹** [판독] · 상수 6.8 / 3.5 × 10⁻¹⁶ | 이 논문 값이 아님 (참고) |
| `lee2024_shear_…` L390 · L415 | 서지 · *"공극 · 형태가 이용률에 미치는 3D 모델 (같은 질문의 3D 판)"* | 서지 ✓ · 3D 단일 입자 ✓ | **일부** (범위 · 정의 차 — 위 표) |
| `benhadjali2025_…` L116 · L384 | *"i0 = SOC 의존 · ref [17] (Bielefeld 2022)"* · 서지 | ✓ (Fig. 7a) | 채움 |
| `benhadjali2026_oneway_…` L100 · L405 | *"δ_ion 0.7 'mS.cm-2'"* · *"δ_ion · i₀ · OCV · D 출처 [S1] Bielefeld 2022"* | 0.7 **mS cm⁻¹** (SI 표 S2 · 따옴표 안 단위는 그 논문의 오기) · 넷 다 원문 표 S2 가 **Rueß 2020 [1]** 을 출처로 적음 | 채움 (2 차 출처 한정) |
| `taghikhani2025_…` L108–111 | x₀ 0.9729 · V_cutoff 4.2 V · K_ed 100 S m⁻¹ · ρ 4770 kg m⁻³ "(Bielefeld et al., 2022)" | 4.2 · 100 · 4.77 g cm⁻³ ✓ · **x₀ 인쇄 없음** (SI Fig. S2 OCV 표지 x 0.970 ↔ 3.601 V · 0.978 ↔ 3.028 V [판독]) | 일부 (x₀) |
| `taghikhani2025_…` L139 · L161 · L178 | D 5 × 10⁻¹⁸ – 6.9 × 10⁻¹⁶ m² s⁻¹ · '빠른 전류' · 0.1 C 실험 끝 171.7 mAh g⁻¹ | 판독 7.5 × 10⁻¹⁸ – 6.9 × 10⁻¹⁶ ✓ (아래 끝 판독 차) · 빠른 전류 = **0.5 C** (Fig. 4 · 5 범례) · 0.1 C 실험 끝 ≈172.8 [판독] | 채움 |
| `taghikhani2025_…` L183 | 공극 6–30 % "(Bielefeld et al., 2020)" | 이 논문 (2022) 은 **6–40 %** (p.10) — 그 줄은 2020 편 인용 | 해당 없음 (다른 편) |
| `jeong2024_…` L348 | "기공의 크기 · 분포가 가역 운전에 주는 영향" 의 이론 근거 (void overpotential) | ✓ (Fig. 8 · 9 · p.10) | 채움 |
| `lin2025_…` L52 | *"SSE 는 작은 기공에 스며들지 못한다 (ref 17 Bielefeld 2022)"* | ✓ p.13 *"the SE does not infiltrate (micro-)porosities"* · p.2 | 채움 |
| `reisacher2023_…` L60 | *"J. Electrochem. Soc. 169, 20539"* | 020539 | 채움 (번호 앞 0 빠짐 · 서지 표기만) |

⇒ **의도 대조 결과: 일부** — 수송 · 반응 · 공극 · 형태의 3D 모델은 **채움** (한정: 단일 입자 · 고정 반구 · ≤ 0.5 C · 역학 없음); **"i₀,ref 0.05 A/m² 출처" 는 없음** (원문 j₀ = SOC 곡선 0.017–0.155 A m⁻² · 상수 0.155 · 0.090 A m⁻²); lee2024 와는 같은 질문의 3D 판이지만 범위 (계면 ≥ 53 % · ≤ 0.5 C) 가 겹치지 않는다; 같은 1 저자 2019 · 2020 카드는 있음.

---

## 1. 한 줄 요약
측정한 SOC 의존 입력 (D̃_Li · j₀ · OCV) 만으로 — 아무것도 맞추지 않고 — 3D 입자 배치 · 단일 입자 · 원뿔 구조 세 기하에서 NCM811 / Li₆PS₅Cl 양극의 충전 곡선을 계산한다.
결과: 곡선 모양은 SOC 의존 입력이 정하고, 드문 큰 CAM 입자가 표면적과 이용률을 깎으며, 계면 공극은 덮인 몫뿐 아니라 **크기 · 분포**가 과전압을 정하고, 구조 전극은 **수 µm 이하** 채널이어야 표면적을 지킨다.
저자의 결론: *"Optimizing the cathode microstructure in SSBs can be a way to disable tortuosity effects, but requires channels in the low μm-range to ensure sufficient surface area, because, unlike liquid electrolytes, the SE does not infiltrate (micro-)porosities"* (p.13).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| A. Bielefeld\* · D. A. Weber · R. Rueß · V. Glavas · J. Janek\* (JLU Giessen · Volkswagen AG) | J. Electrochem. Soc. 169 (2) 020539 (2022) · 13 쪽 | 10.1149/1945-7111/ac50df | **Li₆PS₅Cl** (σ 0.7 mS cm⁻¹ 입력 · 입자 없음) + **다결정 NCM811** (ρ 4.77 · 200 mAh g⁻¹) · 탄소 · 바인더 없음 · Li 금속 음극 | 계산 (3D FEM 전기화학 · COMSOL 5.4 · GeoDict 2019 SP2 · Matlab LiveLink) · 실험 비교 = 같은 그룹 기존 자료 |

- **1저자 메모 (후보 표) 와의 대조**: 저자 다섯 · 제목 · 학술지 · 169 · 020539 · 2022 — **같다**.  덧붙임: 호 (2) · 13 쪽 · DOI · 접수 · 수정 · 출판일 (위).  가리킨 두 카드의 서지도 원문과 같다.
- **글의 꼴**: 서론 → Model (Mathematical · Geometrical) → Results/Discussion (Validation · Input parameters · Particle size distribution · D̃_Li & j₀ · Void influence [Active interface area · Void distribution] · (Micro-)structured cathodes) → Conclusions → 참고문헌 67.  그림 11 · 표 1 (Table I) · 식 [1]–[12] / SI: 그림 S1–S8 · 표 S1–S3 · 식 (1)–(11) · 참고 7.
- **그룹 맥락**: Bielefeld 2019 (3D 미세구조 퍼콜레이션) · 2020 (유효 σ_ion · 바인더) 의 후속 — 정적 수송에서 **시간 전개 전기화학**으로.  입력 = 같은 그룹 Rueß 2020 (GITT · EIS) · Conforto 2021 (임피던스 입도) · 검증 셀 = Rueß 2020 · Trevisanello 2021 · Conforto 2021.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 수학 모델 (p.3–4 · 식 [1]–[12] · SI 표 S1 · 그림 S1 · S3 · `eq_01`–`eq_12` · `txt_p3_cam_electronic_assumption.png` · `txt_p4_j0_soc_rct.png`)
| 항목 | 내용 | 표지 |
|---|---|---|
| 영역 · 계면 | 재료 둘 (SE · CAM) + 계면 둘 (CAM/SE · SE/Li 금속) + 집전체 (σ_CC 300 S m⁻¹) · 모델 꼴은 Finsterbusch 2018 · Neumann 2020 과 비슷 | [인쇄] p.3 · SI 표 S2 |
| 몰 플럭스 [1] · [2] · [3] | J = −D̃∇c + D₀ (c/RT) F z ∇φ (확산 + 이동 · 대류 무시) · D̃ = D₀ (1 + ∂lnγ/∂lnc) (열역학 인자) · j = Σ F z J | [인쇄] p.3 |
| SE | **단일 이온 전도체** (전자 무시 · ref 27) → SE 안 Li⁺ 농도 기울기 없음 → **Ohm [4] j = σ_ion ∇φ** (부호 인쇄 그대로 · §3-9) · **공간 전하층 무시** (nm 급 · 계면 저항 작음 · ref 39) | [인쇄] p.3 |
| CAM 이온 | 전자 수송이 이온보다 몇 자릿수 빠름 (ref 40) → CAM 안 이온엔 전기장 없음 → **확산만 [5] J = −D̃∇c** · 연속 [6] ∂c/∂t + ∇(D̃∇c) = R_I (인쇄 그대로) · D̃ = 리튬화도 (SOC) 의존 | [인쇄] p.3 |
| CAM 전자 | Ohm [7] j = −σ∇φ · σ_CAM **100 S m⁻¹** 로 크게 잡음 → *"We accordingly loose the ability to quantify electronic limitations as reported by Neumann et al."* · 장점 = 전자 · 이온 식이 갈라져 계산이 크게 준다 (Nernst–Planck–Poisson 을 피함) | [인쇄] p.3 · SI 표 S2 |
| 계면 반응 | **BV [8]** j = j₀ [exp(αFη/RT) − exp(−(1−α)Fη/RT)] · η = (φ_CAM − φ_SE) − E_eq [9] · Li⁺ + e⁻ + V_Li ⇌ Li_I [10] · **j₀ [11]** = F exp(−αE_ex/RT) exp(−(1−α)E_in/RT) [k_ex c_LiI]^α [k_in c_Li+ c_V c_e]^(1−α) → SE 쪽 Li⁺ · 전자 농도 일정 → **j₀ = j₀(SOC)** (음의 포물선 꼴 기대) · **R_CT = RT/(zFAj₀) [12]** (EIS · ref 10 · 43) · α = 0.5 | [인쇄] p.3–4 · SI 표 S2 |
| 음극 | Li 석출도 BV · **j₀ᵃ 3 A cm⁻²** (Rueß [1]) · SOC 무관 · α_a 0.5 · V₀(Li) 0 V — 양극에 집중하려고 크게 | [인쇄] p.4 · SI 표 S2 |
| 경계 · 구동 | 외부 전류 j_ext × 매끄러운 계단 f_s(t) (SI Fig. S1 · 0 → 1 · 가로축 0–0.20 s) · 정전류 충전 · x · y 주기 경계 · 바깥 CAM 경계 Li 플럭스 0 · 집전체 바깥면 = 외부 전류 (SI Fig. S3) | [인쇄] SI p.2 · p.5 |
| 풀이 | COMSOL Multiphysics 5.4 · 시간 간격 **dt = 0.01/C (V ≤ 4.0 V) · 0.001/C (V > 4.0 V)** · 사면체 격자 (Delaunay · 기하 차수 1 차) · 격자 · 시간 수렴 시험 [미확인] | [인쇄] SI 표 S2 · SI p.10 |

### 3-2. 입력 매개변수 (SI 표 S2 · p.8 · Fig. 7a · SI Fig. S2 · `tab_S2.png` · `fig_7a.png` · `fig_S2.png` · `txt_p8_constant_inputs.png`)
| 기호 | 값 | 뜻 · 출처 표기 | 쓰인 모델 |
|---|---|---|---|
| j₀ᵃ · α_a · V₀(Li) | 3 A cm⁻² · 0.5 · 0 V | Li/Li₆PS₅Cl 계면 (Rueß [1]) | 1-입자 · 입자형 · 원뿔 |
| l_SE | 10 µm | SE 분리막 두께 | 입자형 · 원뿔 |
| σ_SE | **0.7 mS cm⁻¹** | Li₆PS₅Cl 이온 σ (Rueß [1]) | 셋 다 |
| l_c | 40 µm | 양극 두께 | 입자형 · 원뿔 |
| j₀ | Fig. 7a | NCM811/Li₆PS₅Cl · R_CT 에서 식 [12] (Rueß [1]) | 셋 다 |
| α | 0.5 | 양극 계면 대칭 인자 | 셋 다 |
| OCV | SI Fig. S2 | NCM811 vs Li⁺/Li (Rueß [1]) | 셋 다 |
| D̃_Li | Fig. 7a | NCM811 안 Li 확산 (Rueß [1]) | 셋 다 |
| c_spec | 200 mAh g⁻¹ | NCM811 비용량 (Rueß [1]) | 셋 다 |
| ρ_NCM811 | 4.77 g cm⁻³ | ("gravimetric density" 인쇄) | 셋 다 |
| σ_CAM | 100 S m⁻¹ | NCM811 부분 전자 σ (모델 가정) | 셋 다 |
| c_ref | 49 mol L⁻¹ | NCM811 기준 농도 | 셋 다 |
| σ_CC | 300 S m⁻¹ | 집전체 | 셋 다 |
| **T** | **273.15 K** | 온도 (인쇄 그대로 = 0 °C · 실험 온도와의 대조 [미확인]) | 셋 다 |
| V_max · V_min | 4.2 · 3.5 V vs Li⁺/Li | 차단 전압 | 셋 다 |

- **SOC 의존 곡선 [판독 Fig. 7a · 벡터 표지 25 + 25]**: D̃_Li (×10⁻¹² cm² s⁻¹) = 0.092 (3.61 V) → **0.075 (3.62 V · 최소)** → 1.93 (3.69) → 3.79 (3.73) → 3.26–3.64 (3.75–3.84 · 평탄) → 5.05 (3.87) → **6.88 (3.94 V · 최대)** → 4.69 (4.01) → 3.39–3.60 (4.07–4.15) → 1.75 (4.19) → **0.19 (4.22 V)** · j₀ (×10⁻⁵ A cm⁻²) = **0.17 (3.59 V)** → 0.60 (3.66) → 1.12 (3.71) → **1.55 (3.80 V · 최대)** → 1.42 (3.91) → 1.22 (4.01) → 0.79 (4.12) → **0.34 (4.19 V)**.  [카드 산술] D̃ 범위 92 배 (원문 *"typically by two orders of magnitude"* ✓) · j₀ 9 배.
- **원문 설명 (p.8)**: D̃ — 층상 구조의 2 공공 (divacancy) 도약이 활성화 에너지가 낮아 탈리튬일수록 ↑ · **4.15 V 에서 층간 거리 (산소 층 상호작용) 가 줄어 ↓** (Van der Ven 2013) · 3.7 V 까지 ↑ · ≈0.2 V 평탄 · ≈3.95 V 최대 / j₀ — 3.6 V (공공 ≈ 0) 낮음 → **3.8 V 최대** → 3.8–4.0 V 조금 감소 (입자 안 농도 기울기로 표면 Li ↓) → 4.0 V 위 급감 (Li 고갈).
- **비교용 상수 [인쇄 p.8]**: D̃_Li,1 = **6.8 × 10⁻¹²** (최대) · D̃_Li,2 = **3.5 × 10⁻¹² cm² s⁻¹** ([3.7, 3.9] · [4.05, 4.15] V 평탄값) · j₀,₁ = **1.55 × 10⁻⁵** (최대) · j₀,₂ = **0.90 × 10⁻⁵ A cm⁻²** (평균).  그림의 상수선 판독 6.80 · 3.51 · 1.554 · 0.902 ✓.
- **단위 환산 [카드 산술]**: 10⁻¹² cm² s⁻¹ = 10⁻¹⁶ m² s⁻¹ · 10⁻⁵ A cm⁻² = 0.1 A m⁻² → j₀ 0.017–0.155 A m⁻² · D̃ 7.5 × 10⁻¹⁸ – 6.9 × 10⁻¹⁶ m² s⁻¹.
- **OCV [판독 SI Fig. S2 · 벡터 표지 29]**: x 0.22 → 4.227 V · 0.40 → 4.016 · 0.55 → 3.849 · 0.70 → 3.757 · 0.85 → 3.659 · 0.97 → 3.601 · 0.978 → 3.028 · 0.99 → 2.696 V · 4.2 V ↔ x ≈0.25 (보간).  본문: Li₀.₂₂ 아래 리튬화도에서 전압 급상승은 알려진 현상 (refs 48 · 55, p.8).

### 3-3. 미세구조 · 격자 (p.4 · Fig. 1–3 · SI p.6–10 · 표 S3 · 그림 S4 · S5 · SI 식 (1)–(11) · `txt_p4_particle_type_geometry.png` · `txt_pS6_placeholder_percolation_trick.png` · `txt_pS7_1particle_no_se_microstructure.png` · `txt_pS8_workstation.png`)
- **입자형 (Fig. 1)**: Rueß 2020 의 70 wt% 다결정 NCM811 + 30 wt% Li₆PS₅Cl + 공극 14 % → **CAM 42 vol%** (SI p.6) · GeoDict 2019 SP2 GrainGeo (Park 2020 과 "not entirely analogue" · 비슷한 접근) · 무작위 구는 이 부피분율에서 전자 퍼콜레이션을 못 이룬다 (Bielefeld 2019) → **자리 표시 "trick"**: 볼록 다면체 **40 vol%** (외접 타원체 **20 × 15 × 10 µm** · "best practice") 를 먼저 뿌림 → CAM 구를 남은 60 % 에 (CAM 끼리 · 자리 표시와 겹침 목표 **≤ 3 %**) → 자리 표시를 비움 → SE 가 **남은 부피 전체** (이상 접촉) · .gad → Matlab (GeoLab · LiveLink) → COMSOL .mph 로 같은 구 재생성 · 주기 배치를 **(3 × 3 × 2) 복제** 뒤 SE 상자로 잘라 x · y 주기 · −z 쪽 CAM 이 **1 µm 집전체**에 닿고 +z 쪽은 **10 µm 분리막** · **첫 충전 계산으로 고립 입자를 찾아 손으로 옮겨** 모든 CAM 이 이어지게 (SI p.6) · 결정 방향 무시 (구 2 차 입자 · Xu 2020).  영역 **40 × 40 × 40 µm³**.
- **[카드 산술] 42 vol% 의 밀도 기준**: 70 / 4.77 = 14.68 · 42 % 가 나오려면 (42/86 = 0.488 = CAM 고체 분율) ρ_SE ≈ **1.95 g cm⁻³** 이어야 한다 (원문에 ρ_SE 없음 [미확인]) · 랩 표준 진밀도 1.64 g cm⁻³ 이면 CAM **38.3 vol%** (랩 표준과 다른 문헌 값 — 판정하지 않는다).
- **[카드 산술] 모델 SE 부피** = 100 − 42 = **58 %** (실물 = SE ≈44 % + 공극 14 %) — 공극 자리를 SE 가 채운다 → 입자형 모델 기공 0 %.
- **1-입자 (Fig. 2 · SI p.7)**: 지름 d_CAM 구를 SE 상자가 둘러쌈 (x · y 로 d/4 씩 넓게 · *"not resolving the actual SE-microstructure for technical reasons"* — SE 를 볼록 다면체로 그리면 FEM 요소가 크게 늘어남, 복셀 모델 (Bielefeld 2019 · 2020) 은 가능) · −z 로 집전체층 · **d/10 에서 잘라** 연결 · 공극 = 표면 **반구** (지름 · 덮임 지정 · 위치 무작위 · COMSOL Application Builder) · 잘린 부분 때문에 실제 덮임이 목표와 *"may differ slightly"*.
- **원뿔형 (Fig. 3 · SI p.7–9 · 식 (1)–(11) · 그림 S4)**: 단위 셀 = 가운데 원뿔대 + 모서리 1/4 넷 · x · y 주기 · 집전체 쪽 지름 a > 분리막 쪽 b · 길이 l · 겹침 dn · (1 × 2 × 2) 배열 → 이동 (√2a/2 · dn) → 셀 (l, √2a dn, √2a dn) (식 (1)–(3)) · **ν_CAM = 2V_cone/V = (π/12)(1 + x + x²) · x = b/a** (식 (4)–(8)) → **x = −1/2 ± √(1/4 − 1 + 12ν/π)** (9) · **ν 0.55 → b/a = 0.6623** (10) · **(a, b) = (2, 1.3) · (5, 3.3) · (10, 6.6) · (20, 13.3) µm** (11).  [카드 산술] 식 (9) 재현 0.6622 ✓ · ν 0.42 이면 b/a = 0.4243.  실현 상상 = 조밀 SE 분리막 위 다공 SE (기공 형성제) 에 CAM 채움 또는 두꺼운 SE 층을 레이저 천공 후 CAM 채움 (p.4).
- **격자 (SI Fig. S5 · p.10)** [인쇄]: 1-입자-공극 = 최대 요소 **0.378 µm** · 최소 **0.0162 µm** · 사면체 **1 744 880** (0.7 µm 공극) · **515 482** (2.0 µm) · **409 177** (인쇄 "7.0 µm voids") / 입자형 = **1.79** · **0.0765 µm** · **8 625 685** / 원뿔형 = **1.02** · **0.0102 µm** · **523 859** · 계면 · 좁은 틈은 더 잘게 · 주기 경계를 위해 모서리 · 면 격자를 반대편으로 **복사** (손 단계 다섯) · 계산기 = HP Z8 G4 (**130 767 MB RAM** · Xeon Gold 6134 × 2) · 계산 시간 [미확인].

### 3-4. 검증 (p.4–5 · Fig. 4 · 5b · 7b · `txt_p4_validation_surface_area.png` · `txt_p5_agreement_not_fitted.png`)
- 실험 = Rueß 2020 · Trevisanello 2021 · Conforto 2021 의 같은 재료 셀 · **첫 충전** (CEI 때문에 R_CT 가 충전 ↔ 방전에서 다름 → 같은 첫 충전 입력을 씀) · 셀 압력 · 온도 · 셀 꼴은 이 논문에 [미확인].
- **표면적**: 모델 **0.17 m² g⁻¹** vs 실험 **0.2 m² g⁻¹** (ref 11 · BET) — NCM 거칠기 (SEM, Fig. 2) 를 구가 못 그림 · 얇은 모델 전극에서 활성 면적 / 전극 단면 **≈10** → 셀 전류의 ≈1/10 이 각 CAM 표면에 (고른 분포 가정).  [카드 산술] CAM 적재 0.42 × 40 µm × 4.77 g cm⁻³ = **8.01 mg cm⁻²** → 면적 비 8.01 mg cm⁻² × 0.17 m² g⁻¹ = **13.6** · 1 C = 200 mAh g⁻¹ × 8.01 = **1.60 mA cm⁻²** · 고른 계면 전류 = 1.60 / 13.6 = 0.118 mA cm⁻² = 1.18 A m⁻² → **j/j₀,max ≈ 7.6 (1 C) · ≈ 0.76 (0.1 C)**.
- **세 실현** (시드만 다름 · PSD 조금 다름) → 곡선 모양 거의 같음 (재현성).
- **원문 대조 (Fig. 4)**: 0.02 C — 처음 같다가 50 mAh g⁻¹ 부터 sim 이 약간 높음 · 0.1 C — 실험 과전압이 더 크고 모양 조금 다름 (원문 두 문장이 둘 다 '과소' — §3-9) · 0.5 C — 시작 과전압 너무 작음 · ≈25 mAh g⁻¹ 에서 만남 · 50–100 과소 · **4.0 V 근처 전압 기울기 급증** → 총 용량은 비슷 · dQ/dV — sim 봉우리가 낮음 · 저율 sim = Märker 2019 (NCM811/Li 반쪽 셀) 의 **3.7 · 3.8 V 두 봉우리** · 실험은 0.1 C 에서 이미 하나 → *"the kinetics is limiting, already at 0.1 C rate"*.
- **끝 용량 [판독 Fig. 5b · 7b · 벡터 경로 끝 · 선 굵기 절반만큼 큼]**: S-PSD sim (세 실현) 0.02 / 0.1 / 0.2 / 0.5 C = **188.5–190.2 / 164.1–166.5 / 143.8–147.0 / 101.8–106.5** · 실험 **≈195 / ≈173 / — / ≈114 mAh g⁻¹** (0.2 C 실험 없음).
- *"none of the simulation input has been fitted to meet the experimental data"* (p.5) · 기하 · 격자 · 입력이 계산상 *"quite challenging"*.

### 3-5. ★ 입도 분포 (p.6–8 · Fig. 5 · 6 · Table I · `tab_1.png` · `fig_5a.png` · `fig_6.png` · `txt_p7_psd_surface_area.png`)
- **정의**: S-PSD **≤ 11 µm** · M-PSD **< 14 µm** · L-PSD **≤ 20 µm** · 11 µm 아래는 셋이 거의 같다 (Fig. 5a) · EIS 기반 입도 측정 (Conforto 2021) 은 큰 입자에서 유한 → 반무한 확산으로 바뀌어 불확실성 ↑.
- **Table I [인쇄]**: # AM particles **266 · 249 · 248 · 177 · 128** · Surface area **0.173 · 0.172 · 0.167 · 0.139 · 0.113 m² g⁻¹** (S a · b · c · M · L) → 본문 S → L 표면적 **−35 %** · 입자 **≈ −50 %**.
- **[카드 산술 · Fig. 5a 판독]**: 막대 높이 'Occurance' 는 **밀도 정규화** (Σ 높이 × 막대 폭 0.8264 µm = 1.000, 다섯 계열 모두) → 높이 × 0.8264 × N 이 정수 입자 수를 정확히 복원 · **M 의 11 µm 넘는 11 입자 (수 6 %) = CAM 부피 42 % · L 의 9 입자 (7 %) = 62 %** (L 의 가장 큰 셋 (≈17–20 µm) 만 ≈38 %) · 구 부피 합 24 800–26 200 µm³ ≈ 0.42 × 40³ (26 880) 의 92–98 % · 자유 구 표면적 6/(ρ d₃₂) = 0.194 · 0.188 · 0.188 · 0.154 · 0.126 m² g⁻¹ → **Table I 은 그 0.89–0.91 배** (입자 겹침 · 잘림으로 ≈10 % 표면이 묻힌 것 [카드 해석]) · Sauter 지름 d₃₂ 6.5 · 6.7 · 6.7 · 8.2 · 10.0 µm.
- **끝 용량 [판독 Fig. 5c · d]**: M **186.2 / 155.0 / 129.0 / 84.8** · L **179.5 / 135.7 / 106.4 / 64.6 mAh g⁻¹** (0.02 / 0.1 / 0.2 / 0.5 C) · 원문: 클수록 과전압 ↑ · 율이 높을수록 차이 ↑ · *"The L-PSD even shows significant deviations from the experimental data for 0.02 C"* · 0.5 C 의 4 V 위 기울기가 L 에서 더 가파름.
- **Fig. 6** (0.2 C 충전 끝 · 4.2 V · CAM 안 리튬 농도 로그 색 막대 **9.5–10.5** · 이름표 *"log(c_Li/m³mol⁻¹)"* 인쇄): L 에서 빨강 (덜 빠진) 부피가 많고 *"A significant portion of the larger particles is not activated at all and the inner parts remain highly lithiated"* (p.8).  [카드 산술] 색 막대를 자연로그 (c 단위 mol m⁻³) 로 읽으면 9.5–10.5 ↔ 1.3–3.6 × 10⁴ mol m⁻³ (c_ref 4.9 × 10⁴ 의 0.27–0.74) — 단위 표기는 거꾸로 · 밑 미기재 [카드 해석].
- **원인 둘 (p.7–8)**: 큰 입자 → 활성 면적 ↓ + 확산 경로 ↑ (기울기가 빨리 쌓여 차단 전압에 일찍).  [카드 산술] 특성 시간 R²/D̃ (D̃ 6.8 × 10⁻¹⁶ m² s⁻¹): 7 µm (R 3.5) **1.8 × 10⁴ s (5 h)** · 20 µm (R 10) **1.5 × 10⁵ s (41 h)** ↔ 0.1 C 충전 10 h · 0.5 C 2 h.
- 결론 (p.12): *"even relatively small amounts of large CAM particles in the PSD have a notable impact on the active surface area"* → 큰 입자를 피하는 PSD 설계 · 또는 작은 단결정 NCM.

### 3-6. ★ SOC 의존 D̃_Li · j₀ ↔ 상수 입력 (p.8–10 · Fig. 7 · SI Fig. S6 · `fig_7.png` · `fig_S6.png` · `txt_p9_dli_j0_measurement_reliability.png` · `txt_p10_achilles_heel.png`)
- 많은 시뮬이 상수 D̃ 를 쓴다 (refs 49–52 · Falconi 정리) · 여기선 SOC 의존 (7b) vs 상수 네 벌 (7c–f).
- **끝 용량 [판독]** (0.02 / 0.1 / 0.2 / 0.5 C · mAh g⁻¹):

| 입력 | 0.02 C | 0.1 C | 0.2 C | 0.5 C |
|---|---|---|---|---|
| 7b SOC 의존 D̃(SOC) · j₀(SOC) | 190.1 | 166.5 | 146.9 | 106.5 |
| 7c {D̃₁ 6.8 ; j₀,₁ 1.55} | 198.4 | 187.4 | 174.6 | 143.8 |
| 7d {D̃₂ 3.5 ; j₀,₁ 1.55} | 196.8 | 179.6 | 159.8 | 115.2 |
| 7e {D̃₁ 6.8 ; j₀,₂ 0.90} | 197.6 | 184.2 | 170.4 | 138.8 |
| 7f {D̃₂ 3.5 ; j₀,₂ 0.90} | 196.0 | 176.4 | 155.6 | 110.6 |
| 실험 | ≈195 | ≈173 | — | ≈114 |

- **원문 판정**: 0.02 C — 3.7–4.17 V 에서 모두 비슷 · **첫 과전압은 SOC 의존 입력만 맞춤** · 4.17 V 위는 상수가 더 맞음 · 상수끼리 차이가 작음 (저율에서 확산 · 전하 이동 모두 비제한) / 높은 율 — 7c 가 가장 작은 과전압 (실험보다도) · 7e 같은 꼴 조금 큼 · **7d (평균 D̃ · 최대 j₀) 가 실험과 가장 잘 맞음** (첫 상승은 못 냄) · 7f 과전압 ↑ 꼴 유지 / SOC 의존 곡선 = 시작의 느린 확산 · 막힌 추출 → 가파른 첫 상승 → j₀ 3.8 V 최대 · D̃ 3.95 V 최대에서 평평 → 표면 고갈 · 층간 거리 ↓ 로 끝에서 급상승 · 차단 전압에 일찍.
- **실험엔 4.0 V 위 급상승이 없는 이유 (p.8)**: 모델 밖 보상 효과 / SOC 입력이 이 범위에서 부정확 / 실험 자료 오류 — *"a combination of all"* · 마지막은 가장 가능성 낮음 (Lee 2020 Nat. Energy · 0.5 C · 2.5–4.25 V 에서 없음).
- **측정 신뢰성 (p.9)**: 두 전극 임피던스에 음극이 섞임 · **3.75–3.9 V** (j₀ 높고 D̃ 낮음) 에서 리튬화가 고르지 않아 D̃ **과소평가** · 높은 전압의 NCM **혼화 간극**이 GITT · EIS 해석 가정을 깸 → D̃ 과소평가 가능 → 끝의 급상승을 설명 · j₀ 측정은 더 정확 (CEI 성장만 → Fig. 7 j₀ 비대칭) · 심한 열화 뒤엔 BV 자체가 안 맞을 수 있음.
- ★ *"Clearly, despite its relevance, D̃_Li is not a well and reliably known input parameter … we want to emphasize this is a potential Achilles heel in electrochemical simulation and that the often performed fitting of j₀ or the reaction rate constant to the simulation should be rethought and used with caution"* (p.10) · 그래도 이후 계산은 SOC 의존 입력 (*"the best and physically correct choice"*).
- 단순화의 방향 (p.8): 계면 효과 (고전압 · 고율 열화 · 공극 · 공간 전하) 무시와 SE Ohm 가정은 **과전압을 과소평가** 쪽 · 반대 쪽은 구 2 차 입자 (1 차 입자 · 거칠기 없음 → 면적 ↓ → 과전압 ↑) 하나뿐.

### 3-7. ★ 공극 (p.10 · Fig. 2 · 8 · 9 · SI Fig. S7 · `fig_8_right.png` · `fig_9_right.png` · `fig_S7.png` · `txt_p10_void_fraction_range.png` · `txt_p10_void_overpotential_a.png` · `txt_p10_void_overpotential_b.png` · `txt_p10_void_size_ratio_types.png` · `txt_p10_void_model_limits.png`)
- **문헌 공극 (2 차 인용 · p.10)**: ASSB 양극 공극 **6–40 %** (제조법 · 셀 · 재료) · 슬러리 · 미압연 NCM622/β-Li₃PS₄ (탄소 · Oppanol) **20–40 %** (Ates 2019) · LiCoO₂ 에 Li₆PS₅Cl 침투 **6–8 %** (Kim 2017) · 실험실 프레스 셀 다결정 NCM/Li₆PS₅Cl **≈14 %** (refs 10 · 27) · LiCoO₂/Li₂S-P₂S₅-LiI **13 %** (Hlushkou 2018) — 압력 · 정의 [미확인].
- **공극의 뜻 (원문)**: 큰 공극 = NCM 수축 (탈리튬) 에 따른 CAM–SE **부분 접촉 잃음** (Koerver 2017 · 2018) — 위 경계 = SE 입자가 통째 떨어짐 → 크기 = SE 입자 크기 **1–10 µm** (ref 27) · *"Possibly, SE particles are only partly disconnected, depending on their mechanical rigidity"* / 작은 공극 = 제조 잔류 기공 · SE 입자 형태 (ref 56) · 탄소 · 바인더 같은 비활성 물질 · **< 2 µm 추정** · SE 입자 크기와 함께 커짐 (ref 59).
- **활성 계면 (Fig. 8)**: 다결정 NCM 의 흔한 크기 **7 µm** 입자 + **1.4 µm 반구** · 남은 계면 A 100 → **≥ 52 %** (본문 · 판독 53.0 %) · 0.02–0.5 C (본문) · **공극 과전압 = 공극 형상 전압 − 이상 계면 전압** (@50 · @100 mAh g⁻¹, "arbitrarily chosen").

| A (7 µm, 진한 색) | 0.2 C @50 | 0.2 C @100 | 0.1 C @50 | 0.1 C @100 | 0.02 C |
|---|---|---|---|---|---|
| 93 % | 4.8 | — | 2.7 | — | 0.7 |
| 83 % | 12.6 | 9.4 | ≈6.4 (둘 겹침) | | 1.6 |
| 73 % | 23.2 | 18.4 | 13.3 | 10.8 | 3.2 |
| 63 % | 34.1 | 27.7 | 20.5 | 16.3 | 5.0 |
| 53 % | **46.6** | **39.5** | 29.5 | 23.0 | 7.2 |

| A (5 µm, 연한 색) | 0.2 C @50 | 0.2 C @100 | 0.1 C | 0.02 C |
|---|---|---|---|---|
| 88 % | ≈5.4 (겹침) | | 3.2 | 0.8 |
| 84 % | ≈7.5 (겹침) | | 4.6 | 1.1 |
| 71 % | 18.4 | 14.6 | ≈10.5 (겹침) | 2.5 |
| 61.5 % | 29.2 | 22.6 | ≈16.3 (겹침) | 3.9 |
| 50.6 % | **39.6** | **29.5** | ≈21.5 (겹침) | 5.3 |

  (단위 mV · [판독] 래스터 색 덩이 중심 · 눈금 최소제곱 · 겹친 표지는 한 값)
  원문: 0.02 C 는 거의 영향 없음 (처음 · 끝만 조금 — 낮은 D̃) · 0.1 C 부터 A ↓ · 공극 밀도 ↑ 에 따라 과전압 ↑ · 높은 전압의 확산 제한이 일찍 · 입자 중심의 Li 가 거의 안 빠짐 · **50 mAh g⁻¹ 의 공극 과전압이 100 보다 큼** · 5 µm 입자는 같은 경향 · 확산 길이가 짧아 **작다** (SI Fig. S7 범례 40–100 %A).
  ⚠ 본문 *"The effect is even more distinctive at 0.2 and 0.5 C rate, where the overpotential rises up to 50 mV for 52% remaining interface area at 100 mAh g⁻¹"* ↔ 그림 8 오른쪽엔 **0.5 C 가 없고** 0.2 C @100 = 39.5 mV (@50 = 46.6) [판독] — 문장과 그림이 다르다 (0.5 C 값 [미확인]).
- **공극 분포 (Fig. 9)**: 7 µm · **남은 계면 70 % 고정** · 입자–공극 크기 비 d_CAM/d_Void **1.2–10** (본문: 공극 *"maximum 4 μm and minimum 0.7 μm"*) · 30 % 를 덮으려면 **0.7 µm 160 개** (고르게) vs **4 µm 2 개** (본문) → 큰 공극 = 불균일 접촉.

| d_CAM/d_Void | 1.2 | 1.4 | 2.3 | 3.5 | 5 | 7 | 10 |
|---|---|---|---|---|---|---|---|
| 0.2 C @50 | 49.7 | ≈36.0 (겹침) | 35.0 | 31.5 | 23.2 | 21.4 | 19.2 |
| 0.2 C @100 | **65.9** | | 29.8 | 25.9 | 18.4 | 16.3 | **14.4** |
| 0.1 C @50 | ≈34.9 (겹침) | 22.3 | 20.4 | 18.4 | 13.3 | 12.3 | 11.1 |
| 0.1 C @100 | | 16.9 | 17.0 | 15.0 | 10.9 | 9.8 | 8.7 |
| 0.02 C | 9.6 | 5.5 | 5.0 | 4.5 | 3.2 | 3.0 | 2.7 |

  (mV · [판독] 로그–로그 축 눈금 최소제곱 · 비는 1.20 / 1.40 / 2.30 / 3.50 / 5.00 / 7.00 / 10.0 에 정확히 앉음 · 비 1.2 에서만 0.2 C @100 (65.9) > @50 (49.7) — 다른 비에서는 @50 > @100)
  원문: 큰 공극 = 국부적으로 비활성 면이 크고 입자 안 농도 기울기가 급함 · 고르게 퍼진 작은 공극은 **입자 안 확산이 일부 메움** · *"assuming that the SE becomes more compact upon cycling due to external pressure, the influence of the smaller voids is expected to decrease"* (계산 없음).
  ⚠ [카드 산술] 비 1.2 ↔ 공극 지름 7/1.2 = **5.8 µm** (본문 '최대 4 µm' 와 안 맞음) · 중심이 구면 위에 있는 반구 공극의 구면 발자국 넓이 = **πr²** (정확) → 5.8 µm 둘 = 7 µm 구 표면의 **34.7 %** (30 % 와 맞음) · 4 µm 둘 = 16.3 % (안 맞음) · 0.7 µm 160 개 = 40 % (무작위 겹침이면 1 − e^−0.40 = 33 %) → 본문의 '4 µm' 는 오기일 가능성 [카드 해석] · SI Fig. S5 의 "7.0 µm voids" 격자 (비 1.0) 는 그림 9 에 없다 [미확인].
- **원문 한계 · 권고 (p.10)**: *"this model approach is not capable to quantify the influence of voids in the cathode composite on ionic percolation, as we are focusing on the role of the active surface area and one CAM particle only"* · 고른 입자 분포 (ref 27) 뿐 아니라 **고른 공극 분포** · 결론 (p.13): 공극 부피 최소화에 더해 **CAM/SE 계면 공극의 크기도 줄여** 고르게 · 등방 열간 가압 (Lee 2020) 이 접촉을 개선한 예 · 부분 접촉 잃음의 크기 · 모양 · 진화를 실험 · 이론으로 더 보라.

### 3-8. 원뿔형 구조 전극 (p.11–12 · Fig. 3 · 10 · 11 · SI Fig. S4 · S8 · `fig_10.png` · `fig_10_right.png` · `fig_11.png` · `fig_S8.png` · `txt_p11_cone_vs_particle_cost.png` · `txt_p12_cone_size_guideline.png`)
- **동기**: 구불구불한 이온 길 (refs 25 · 27) → 조밀 SE 층 레이저 천공 + CAM 채움 · CAM 기둥 · 등으로 tortuosity 를 '끔' (Fig. 3).
- **42 vol% 원뿔 (표면 0.17 — 원문 "0.17 g m⁻²" 단위 거꾸로 인쇄) vs 입자형 vs 실험 (Fig. 10 왼쪽 · 끝 용량 [판독])**: 원뿔 (점선) **190.7 / 169.7 / 152.0 / ≈114** · S-PSD (실선) 189.9 / 166.3 / 146.8 / 106.3 · 실험 (파선) 195.3 / 172.0 / — / ≈114 (0.02 / 0.1 / 0.2 / 0.5 C · 0.5 C 원뿔 · 실험 끝이 겹침) — 과전압이 *"generally reduced … especially at elevated C-rates"* 이지만 *"quite moderate"* · 곡선 모양은 같음 (모양 = D̃ · j₀) · 두꺼운 전극에서 더 클 것 (입자 수가 많아 계산 비용 때문에 못 함).  [카드 산술] 아래 면적 규칙이면 42 vol% 원뿔이 0.17 m² g⁻¹ 이 되는 a ≈ **7 µm** (원문 a 미기재 [미확인]).
- **55 vol% · a ∈ {2, 5, 10, 20} µm (Fig. 10 오른쪽 · 11)**: 활성 계면 [판독] **0.513 · 0.211 · ≈0.11 · 0.069 m² g⁻¹** (비교 띠: BET 0.2 · S 0.17 · M 0.14 · L 0.113 = 42 vol%) · 원문: 5 µm 원뿔 ≈ 실물 BET · 큰 원뿔 ≈0.1 · 2 µm = *"five times the interface area"* · 실험 · 입자형 (42 vol%) 과는 *"not directly comparable"*.
  [카드 산술] 원뿔대 (옆면 + 두 끝면) / (ρ V) · l 40 µm · ρ 4.77 → **0.508 · 0.210 · 0.110 · 0.061** — 2 · 5 · 10 µm 는 판독과 1–2 % 안 · **20 µm 만 −12 %** (원문 면적 계산법 미기재 [미확인]).
- **끝 용량 [판독 Fig. 11 · ±3]**:

| a | 0.02 C | 0.1 C | 0.2 C | 0.5 C | 1 C |
|---|---|---|---|---|---|
| 2 µm | 198 | 189 | 182 | 169 | **153** |
| 5 µm | 192 | 174 | 159 | 128 | **≈90** (원문 *"around 100"*) |
| 10 µm | 182 | 145 | 113 (≈4.19 V 에서 끝) | 60 | 32 |
| 20 µm | 159 | 80 | 45 | 19 | 11 (≈4.17 V 에서 끝) |

  원문: 2 µm = 높은 계면 + 짧은 확산 → **1 C 까지 평평** · 5 µm = 훨씬 가파르지만 1 C 에서 ≈100 mAh g⁻¹ · 10 · 20 µm = *"poor"*.  [카드 산술] 2 µm (R ≈1 µm) R²/D̃ ≈ 1.5 × 10³ s (0.4 h) ↔ 1 C 1 h.
- **겹친 원뿔 (SI Fig. S4 · S8 · a = 10 µm · 겹침 5–25 % · b ↓ · ν · a 고정)**: *"The overlap even worsens the performance"* — [판독 S8] 0 → 25 % 겹침 끝 용량 0.02 C 182 → 175 · 0.1 C 145 → 127 · 0.2 C 114 → 94 · 0.5 C 62 → 50 → *"a high surface area is the key for electrode optimization"*.
- **권고 (p.12)**: *"structuring of SSB cathodes has to be in the low μm-range, below 5 μm, in order to tune the electrode toward elevated current densities"* · 지금의 초고속 레이저 채널 ≈**12 µm** (NCM111 후막 · refs 60–61) · NCM 마이크로 막대 (62–63) 를 정렬하고 작은 SE 로 침투 · SE 없는 확산 의존 양극 (LiTiS₂ D̃ 10⁻⁸–10⁻⁹ cm² s⁻¹) 은 NCM811 의 D̃ 가 **세 자릿수 낮아** 불가.
- **한계 (원문)**: 거칠기 없음 (면적 ↑ → 성능 ↑ 가능) · *"the model also does not feature voids that, in practice, would occur between CAM particles, between SE particles and at the SE/CAM interface"* (성능 ↓) — 상쇄 여부 *"not straightforward to estimate"*.

### 3-9. ★ 저자가 적은 한계 · 원문 안 어긋남
**원문 한계 (인용)**
1. *"We accordingly loose the ability to quantify electronic limitations"* (σ_CAM 크게, p.3).
2. 단순화는 과전압을 **과소평가** 쪽 · 구 2 차 입자만 반대 (p.8).
3. *"not capable to quantify the influence of voids in the cathode composite on ionic percolation"* (p.10).
4. 원뿔 모델엔 CAM 사이 · SE 사이 · 계면 공극이 없다 (p.12).
5. *"coupled (chemo-)mechanical and electrochemical simulations of the cathode composite are required on the microstructure level, as these can enlighten the mechanical behavior, the formation and evolution of voids and inter-particle cracks during cycling"* (p.13).
6. *"not resolving the actual SE-microstructure for technical reasons"* (SI p.7).
7. D̃_Li 측정 신뢰성 · 문헌 산포 (p.9–10).

**원문 안 어긋남 (이 카드가 찾음)**
- a. 공극 크기 *"maximum 4 μm"* ↔ 그림 9 최소 비 1.2 (= 5.8 µm) · 덮임 산술은 5.8 µm 쪽 (§3-7).
- b. *"up to 50 mV … at 100 mAh g⁻¹"* (0.2 · 0.5 C) ↔ 그림 8 오른쪽 (0.5 C 없음 · 0.2 C @100 39.5 mV).
- c. *"active surface area of 0.17 g m⁻²"* (p.11) — 단위 거꾸로 (다른 곳 m² g⁻¹).
- d. 그림 6 색 막대 *"log(c_Li/m³mol⁻¹)"* — 단위 거꾸로 · 로그 밑 미기재.
- e. 식 [1] 이동 항 · [4] 는 **+∇φ** · 식 [7] 은 **−σ∇φ** — 부호 규약이 섞임 [카드 해석] (계산 결과와의 관계 [미확인]).
- f. T **273.15 K** (0 °C) — 실험 온도 미기재 · 오기 가능성 [미확인].
- g. SI Fig. S5 *"7.0 µm voids"* ↔ 7 µm 입자 (비 1.0 · 그림 9 에 없음).
- h. SI Fig. S7 범례 40–100 %A ↔ 그림 8 오른쪽 5 µm 표지 50.6–88 % [판독].
- i. 0.1 C 검증 두 문장 (p.4–5) — *"below 50 … and between 100 … 150 … the simulation underestimates the overpotential"* · *"Between 50 … 100 … and above 150 … the simulation overpotential is lower than the experimental one"* = 둘 다 '과소' (한쪽은 '과대' 의 뜻일 가능성 [카드 해석]).
- j. 본문 "Fig. 9 … particle-to-void-size-ratio" 과 캡션 "void-to-particle-size-ratios" (p.11) — 비의 방향 표기가 섞임 (그림 축은 d_CAM/d_Void).

---

## 4. ★ 방법 — 모델 사슬 · 입자 처리

### 4-1. 모델 사슬
GITT · EIS (Rueß 2020 · 첫 충전) → D̃_Li(SOC) · R_CT(SOC) → j₀(SOC) (식 [12]) · OCV · σ_SE (0.7) → 기하 (GeoDict 입자형 · 1-입자 공극 · 원뿔형) → COMSOL 5.4 (식 [1]–[11] · 주기 · 매끄러운 계단 전류) → 정전류 충전 0.02–1 C (차단 4.2 V) → 전압–용량 · dQ/dV · 농도장 (로그) · 공극 과전압 (같은 용량에서 전압 차) · 기하 표면적.

### 4-2. 입자 처리 ★ ("무질서 처리" 의 이 논문 판)
- **CAM**: 단단한 기하 — 구 2 차 입자 (겹침 ≤ 3 % 로 서로 이어짐 · 고립 입자는 손으로 옮김) · 거칠기 · 1 차 입자 · 결정 방향 · 부피 변화 **없음** (역학 없음).
- **SE**: **입자 없음** — 남은 부피를 채우는 연속체 (이상 접촉) · 입계 · 접촉 협착 · 기공 **없음** · σ = 펠릿 0.7 mS cm⁻¹ (Rueß 2020).
- **공극**: 1-입자 모델에서만 — **고정 반구 구멍** (접촉 잃음 · 잔류 기공 · 비활성 물질의 대리) · 크기 · 덮임 · 위치 (무작위) 지정.
- ⇒ 형상 소성 · 접촉 소성 · 겹침 대리 · 가압 이력 **모두 없음** — 기하는 생성기가 정하고 고정된다.

### 4-3. 기법 미니 용어집
- **GITT** (정전류 간헐 적정): 짧은 전류 펄스 + 휴지의 전압 응답에서 D̃ 를 뽑는 측정 — 혼화 간극 · 불균일 리튬화에서 가정이 깨진다 (p.9).
- **R_CT · j₀**: EIS 의 전하 이동 저항 → j₀ = RT/(zFA R_CT) (식 [12]) — **면적 A 가 들어간다** (모델 0.17 ↔ BET 0.2 m² g⁻¹ 이면 j₀ 가 그 비만큼 달라진다 [카드 산술 · §9]).
- **화학 확산 계수 D̃**: 자기 확산 D₀ × 열역학 인자 (1 + ∂lnγ/∂lnc) (식 [2]).
- **단일 이온 전도체**: 움직이는 것이 Li⁺ 하나라 농도 기울기가 안 생기는 전해질 → Ohm 법칙만.
- **매끄러운 계단 f_s(t)**: 전류를 0 → 1 로 부드럽게 켜는 함수 (수치 안정 · SI Fig. S1).
- **자리 표시 기법 (placeholder trick)**: 빈 부피의 40 % 를 다면체로 먼저 막아 CAM 구가 몰려 이어지게 만드는 생성 꾀 — 압밀 · 물리 과정이 아니다.
- **공극 과전압**: 같은 용량에서 (공극 있는 기하의 전압) − (이상 계면 기하의 전압).
- **입자–공극 크기 비 d_CAM/d_Void**: 같은 덮임에서 공극이 몇 개 · 얼마나 고르게 퍼지는지의 대리.
- **원뿔대 단위 셀**: 가운데 원뿔대 + 모서리 1/4 넷의 주기 셀 · ν_CAM = (π/12)(1 + x + x²).
- **dQ/dV**: 전압에 대한 미분 용량 — 봉우리 (NCM811 3.7 · 3.8 V) 가 흐려지면 동역학 제한.
- **밀도 정규화 히스토그램 · Sauter 지름 d₃₂** [카드 산술 용어]: 막대 넓이 합 = 1 · d₃₂ = Σd³/Σd² (부피당 표면을 정하는 평균).

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png`) | GeoDict → Matlab → COMSOL 입자형 생성 6 단계 (자리 표시 · CAM · 복제 · 잘라내기 · 집전체 · 분리막) | 비물리 생성 (압밀 아님) 의 꼴 — DEM 압밀 침대와 출발 상태가 다르다는 대조 |
| **Fig. 2** (`fig_2.png`) | 1-입자 모델 (이상 → 50 % 접촉) + SEM (미사용 · 1 회 · 50 회 충전 — Koerver 2017 재수록) | 접촉 잃음의 실물 그림과 반구 공극 대리를 나란히 — 우리 피복 정의 (단계 7) 의 그림 |
| **Fig. 3** (`fig_3.png`) | 구조 전극 개념 · 원뿔 단위 셀 (노랑 상자) ↔ 입자 배치 | 구조 전극 기하 (흐름 밖) |
| **Fig. 4** (`fig_4.png`) | 세 실현 · 0.02 / 0.1 / 0.5 C 전압 + dQ/dV vs 실험 | 검증 그림 — 실험 곡선 (Rueß 2020 셀) 의 끝 용량 ≈195 / ≈173 / ≈114 [판독] |
| **Fig. 5** (`fig_5.png` · 패널 `fig_5a.png`) | (a) 입도 히스토그램 (밀도 정규화) · (b–d) S · M · L 충전 곡선 | ★ 큰 입자 부피 몫 [카드 산술] · PSD → 끝 용량 (§3-5) |
| **Fig. 6** (`fig_6.png` · 다시 자름) | 0.2 C 충전 끝 CAM 안 리튬 농도 (로그) — S a · b · c · M · L | 큰 입자 속 미사용 — 이용률 지도 (정성) |
| **Fig. 7** (`fig_7.png` · 패널 `fig_7a.png`) | (a) D̃_Li · j₀ vs V + 상수선 · (b–f) SOC 의존 · 상수 네 벌의 충전 곡선 | ★ STEP4 결과 전 대조 입력 곡선 (§3-2 · §7) · 상수 vs SOC 의존 표 (§3-6) |
| **Fig. 8** (`fig_8.png` · 패널 `fig_8_right.png`) | 남은 계면 A vs 공극 과전압 (7 µm 진한 · 5 µm 연한) + 왼쪽 충전 곡선 | ★ 피복 ↔ 과전압 결과 전 대조 (§3-7) |
| **Fig. 9** (`fig_9.png` · 패널 `fig_9_right.png`) | d_CAM/d_Void vs 공극 과전압 (70 % 계면 · 로그 축) + 왼쪽 곡선 | ★ 같은 덮임 · 다른 분포 (§3-7 · §9) |
| **Fig. 10** (`fig_10.png` · 패널 `fig_10_right.png`) | (왼) 42 vol% 원뿔 vs 입자형 vs 실험 · (오) a vs 활성 계면 (55 vol%) + PSD 띠 + BET | 원뿔 면적 [판독] · 내 산술 대조 (§3-8) |
| **Fig. 11** (`fig_11.png`) | a = 2 · 5 · 10 · 20 µm 원뿔의 0.02–1 C 곡선 | 구조 크기 → 율 특성 (흐름 밖) |
| **SI Fig. S1** (`fig_S1.png` · 다시 자름) | 매끄러운 계단 함수 f_s(t) | 구동 꼴 |
| **SI Fig. S2** (`fig_S2.png`) | NCM811 OCV vs x (0.22–0.99) | STEP4 OCV 대조 (§7-3) |
| **SI Fig. S3** (`fig_S3.png` · 다시 자름) | 영역 · 경계 조건 · 식 개요 (입자형 S a) | 경계 조건 목록 |
| **SI Fig. S4** (`fig_S4.png` · 다시 자름) | 겹친 원뿔 개념 ((1 − dn)a) | — |
| **SI Fig. S5** (`fig_S5.png`) | 세 기하의 사면체 격자 + 요소 크기 · 개수 표 | ★ 해상도 · 비용 감각 (단계 1 · U1) |
| **SI Fig. S6** (`fig_S6.png`) | C 율별로 SOC 의존 · 상수 네 벌 | §3-6 표의 다른 배치 |
| **SI Fig. S7** (`fig_S7.png`) | 5 µm 입자 · 1.4 µm 공극 · 40–100 %A · 끝 확대 | 5 µm 경향 |
| **SI Fig. S8** (`fig_S8.png`) | 원뿔 크기 · 겹침별 곡선 (0.02–0.5 C) | 겹침 → 성능 ↓ [판독] |
| **Table I** (`tab_1.png`) · **표 S1–S3** (`tab_S1.png` · `tab_S2.png` · `tab_S3.png`) | PSD 입자 수 · 표면적 / 변수 목록 / 매개변수 값 / 재구성 매개변수 | ★ 입력 표 (§3-2 · 3-3 · 3-5) |
| 식 크롭 23 (`eq_01`–`eq_12` · `eq_S01`–`eq_S11`) · 근거 문단 20 (`txt_p*` · `txt_pS*`) | 식 [1]–[12] · SI 식 (1)–(11) · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **전압–용량 · dQ/dV**: 정전류 충전 곡선 · 미분 용량 (봉우리 3.7 · 3.8 V).
- **공극 과전압**: 같은 용량 (50 · 100 mAh g⁻¹) 에서 공극 기하 − 이상 계면 기하의 전압 차.
- **농도장**: CAM 안 리튬 농도의 로그 색 지도 (충전 끝).
- **기하량**: 입자 수 · CAM 표면적 (m² g⁻¹ · Table I) · 활성 계면 vs 원뿔 지름 · 격자 통계 (요소 크기 · 사면체 수).
- **통계**: S-PSD 만 시드 셋 · 나머지는 한 실현 · 오차 막대 · 반복 없음.
- **판독 (이 카드)**: 벡터 그림 = 경로 좌표 + 눈금 최소제곱 (선 끝 = 경로 최대 x · 선 굵기 절반만큼 큼) · 래스터 = 300 dpi + 눈금 표시 + 색 덩이 중심 · 그림 11 · S8 = 눈 판독 — digitized.csv note 열.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **모델 · 상태 · 재료 조건이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| SE 표현 | 남은 부피를 채우는 **이상 접촉 연속체** · σ 펠릿 0.7 mS cm⁻¹ · 입자 · 입계 · 협착 · 기공 없음 | DEM 접촉망 = 접촉마다 Holm 협착 직렬 · STEP3 복셀 FV = 면 조화평균 · **계면 항 0 = CONTACT_FREE 가지** · σ 입력 3.0 (펠릿) · 보고 σ₀ 1.5 mS cm⁻¹ [우리 · CLAUDE.md CL-81 · CL-91] | 이 논문의 SE 이온 수송 = 우리 **STEP3 와 같은 부류 (CF 상한)** · 펠릿 σ 를 연속체에 넣는 규약도 같음 (기공 · 입계 이중계상 논점 같음) |
| 기공 | 입자형 모델 **0 %** (실물 14 % 자리를 SE 로) · 1-입자 = 반구 공극 덮임만 | real_14 DEM ε_sphere 15.6 % (300 MPa) · 랩 표준 순수 SE 10–13 % (진밀도 1.64) [우리] | **다른 양** — 이 모델엔 기공이 없다 · 압밀 · 압력 없음 |
| CAM 부피분율 기준 | 70 : 30 wt% + 공극 14 % → **42 vol%** (암묵 ρ_SE ≈1.95 [카드 산술]) | 랩 표준 ρ_SE 1.64 → 같은 무게비면 38.3 vol% [카드 산술] | 밀도 기준이 다르면 같은 무게비의 부피분율이 4 %p 다르다 — 조성을 옮길 때 밀도 칸 필수 |
| CAM 형상 · 하중 | 구 (겹침 ≤ 3 %) · 고정 · 역학 없음 | DEM 강체 구 (hooke/hysteresis · NCM 140 GPa) · MPM 강체 AM 고정 골격 [우리] | 둘 다 구 · 이 논문은 하중이 아예 없다 |
| 피복 · 계면 | 남은 계면 A = 1 − 반구 공극 발자국 몫 (100 → 53 %) · 거칠기 없음 | DEM Hertz 18 % · Tabor 52 % (real_14 · AM_P/S 48.3 / 51.8 %) · MPM 소성 52 / 74 % (띠 0.13 / 0.26 µm) [우리 · CLAUDE.md] | **정의가 다르다** (구멍 몫 ↔ 간격 띠 안 몫) · 우리 Tabor ≈50 % 는 이 논문 최저 A (53 %) 근처 — 경향 대조만 |
| 반응 · 확산 입력 | j₀(SOC) 0.017–0.155 A m⁻² · D̃(SOC) 7.5 × 10⁻¹⁸ – 6.9 × 10⁻¹⁶ m² s⁻¹ [판독] · OCV x 0.22–0.99 | STEP4-v2 (비선형 BV + 구형 확산) · 다결정 D_s 기본값 3 × 10⁻¹⁴ m² s⁻¹ (FEM 사슬 · 측정 아님) · SC/PC i₀ 정량 부재 → 스윕 · 창 x0 0.264 · x100 0.9084 [우리 · CLAUDE.md STEP4 절] | 우리 D 기본값은 이 논문 SOC 곡선 최대의 **≈44 배** [카드 산술] — 같은 계 (NCM811/LPSCl) 측정 곡선이 있으니 STEP4 결과 전 대조로 등록할 자리 (값 맞춤 금지) |
| 접촉 잃음 → 저항 | 공극 과전압 (0.2 C · A 53 % ≈40–47 mV) · 율 · 용량 의존 → 확산 몫 섞임 | A10 접촉 원장 (사이클 수축 → 계면 개구 → A_rel → R_ct 몫 · CZM 은 AM–SE · SE–SE 만 · AM–AM 재폐합) [우리 · CLAUDE.md 2026-07-22] | 우리 원장의 R_ct ∝ 1/A 가정 (A 53 % → 1.9 배) 을 이 논문은 반응 + 확산 합으로 본다 — 확산 몫이 큰 고율에서 우리 원장은 과소 [카드 해석] |
| 차원 · 크기 | 3D 40³ µm³ · ≈250 입자 · 8.6 M 사면체 · 128 GB 워크스테이션 | DEM 침대 수만–십만 입자 · MPM 384–768 격자 [우리] | 크기 감각 (단계 1) |

### 7-2. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **수송 + 반응 (전기화학 시간 전개)** — 우리 분업의 DEM / STEP3 · STEP4 쪽 (전도 · 반응 분포) 의 **연속체 판**이다.  접촉망 (Holm) 도 역학 (MPM) 도 없다.
- 없는 반쪽: 압밀 · SE 소성 유동 · AM 하중 분담 · 탈압 · 수축에 따른 공극 생성 (공극은 주어진다) — 저자 스스로 역학 결합이 필요하다고 적는다 (p.13).

### 7-3. STEP3 · STEP4 로 옮길 때
- **STEP3 (복셀 σ)**: 이 모델의 SE 는 우리 STEP3 와 같은 CF 가지 — 이 논문 σ_eff 는 **협착 없는 상한** 꼬리표로 읽는다 · 이 논문은 σ_eff 숫자를 내지 않는다 (전압 곡선뿐).
- **STEP4 (반응 · 확산)**: SOC 의존 D̃ · j₀ · OCV 곡선 (Fig. 7a · S2 · digitized.csv) = 같은 계 측정 입력 — 우리 기본값 (D 3 × 10⁻¹⁴ · 측정 아님) 과의 차이를 결과 전 대조 항목으로 · ⚠ R_CT → j₀ 환산의 면적 · T 273.15 K 인쇄 · 출처 = Rueß 2020 (원 측정 카드 없음 — 정독 출력 n).

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = NCM811 + Li₆PS₅Cl 의 **전기화학 FEM** — 역학 · 압밀 · 압력 · 탈압이 없다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 반면교사 둘 — ① **모델 기공 0 %** (실물 공극 14 % 를 SE 로 채움 → 모델 SE 58 vol% [카드 산술]) — 문헌 시뮬 값을 받을 때 '모델 기공' 칸을 둔다 ② **42 vol% 의 밀도 기준이 인쇄되지 않음** (암묵 ρ_SE ≈1.95 ↔ 랩 표준 1.64 → 38.3 vol% [카드 산술]) — 조성 → 부피 환산에 밀도 출처를 함께 등록 | 기공 곡선 · 압력 없음 |
| **단계 1** (3D 메모리 · 장 수) | 입자 해상 3D 전기화학의 비용 감각: 40³ µm³ · ≈250 입자 → **8 625 685 사면체** (요소 0.0765–1.79 µm) · 128 GB RAM · 1-입자 0.41–1.74 M · 원뿔 0.52 M (SI Fig. S5) | 입자별 속도장 · 메모리 실측 · 계산 시간 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (순수 SE 기공 · 항복 없음) · σ_SE 0.7 mS cm⁻¹ (펠릿 · 조건 [미확인]) 뿐 | — |
| **단계 5** (3D 복합 압밀) | ★ 출발 상태 대조: **압밀이 아닌 생성 꾀** (자리 표시 40 % + 겹침 ≤ 3 % + 고립 입자 손 이동) 로 42 vol% CAM 이 이어진 배치 — 우리 DEM 압밀 침대와 접촉 · 겹침 · 연결이 다른 출발이다 · ★ **입도 꼬리의 부피 몫**: 수 6–7 % 의 큰 입자가 CAM 부피 42–62 % [카드 산술 Fig. 5a] → 우리 침대 PSD 보고에 부피 가중 꼬리를 함께 | 압밀 · 하중 · 압력별 결과 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 문장 하나: *"assuming that the SE becomes more compact upon cycling due to external pressure, the influence of the smaller voids is expected to decrease"* (계산 없음) | — |
| **단계 7** (형상 · 피복 · 수송) | ★ 이 논문의 중심: ① 남은 계면 A → 공극 과전압 (0.2 C · A 53 % ≈47 · 40 mV [판독]) ② **같은 덮임 (A 70 %) 에서 공극 크기 비 1.2 → 10 으로 0.2 C @100 65.9 → 14.4 mV** [판독] = 피복 몫만으론 부족 · 분포 척도 필요 ③ PSD → 표면적 (−35 %) · 큰 입자 속 미사용 (Fig. 6) ④ SE = CF 연속체 (우리 STEP3 와 같은 부류) ⑤ SOC 의존 D̃ · j₀ · OCV (STEP4 입력 대조) | 접촉 단위 협착 · 접촉망 σ · 피복의 압력 의존 없음 · 공극은 고정 반구 |
| **후보 D0** (지금 DEM) | 우리 DEM 접촉망 피복 (Tabor ≈50 %) 을 '남은 계면' 으로 읽으면 이 논문의 A 53 % 근처 → 공극 과전압 크기 감각 (정의 차 한정) · DEM 침대 PSD 의 부피 가중 꼬리 점검 | DEM 을 쓰지 않음 — 접촉 · 겹침 · 연화 언급 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 — CAM/SE 는 **완전 결합 (이상 접촉)** · 분리 · 미끄럼 없음 · 공극은 기하로만 | — |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 (역학 없음) · 다만 강체 AM + SE 연속체라는 **기하 구성**은 우리 MPM 스캐폴드 (고정 AM + SE 연속체) 와 같다 — 그 위의 전기화학 결과 (STEP4) 를 견줄 실례 | 하중 분담 · 미끄럼 값 없음 |
| **후보 B** (입자별 FE + 접촉) | 입자 해상 FE 격자의 실무: 주기 경계용 모서리 · 면 격자 복사 (SI p.10) · 좁은 목에서 요소 0.0765 µm · 1-입자 공극 0.0162 µm → 입자별 FE 의 격자 비용 감각 | 역학 · 접촉 법칙 없음 (전기화학 FE) |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 | — |
| **U0–U6** | **U1** (해상도) 쪽: 1-입자 7 µm 의 최대 요소 0.378 µm (= 지름당 ≥ 18.5) · 입자형 최대 1.79 µm (2–20 µm 입자에 지름당 ≥ 1.1–11) · 계면에서 세분 — **격자 수렴 시험 보고 없음** [미확인] · U2–U6 없음 | 수치 오차 추정 없음 |
| **R1–R7** | **R2** (미끄럼 · 분리) 대리 — 큰 공극 = CAM 수축에 따른 접촉 잃음 (1–10 µm) 을 고정 구멍으로 · **R5** (맞추는 값 하나) — ★ **맞춘 값 0** (모든 입력 = 같은 재료 측정 · p.5) — '하나보다 적게' 의 실례 · **R6** (SE 형상) — SE 입자 없음 · **R7** (AM 파괴) — 다결정 NCM811 의 3.8 V 근처 균열 (Rueß · Trevisanello) 은 액체에선 새 면을 주지만 SSB 에선 SE 가 못 스며든다 (p.2 · 문장만) | R1 · R3 · R4 없음 |
| **결과 전 대조 항목** | ① Table I 입자 수 · 표면적 (0.173 → 0.113 m² g⁻¹ · −35 %) — PSD → 면적 산술의 정답 ② 공극 과전압 vs A (Fig. 8 · 7 / 5 µm · 0.02–0.2 C) · vs d_CAM/d_Void (Fig. 9) [판독] ③ 원뿔 활성 계면 0.51 / 0.21 / 0.11 / 0.07 m² g⁻¹ [판독] (내 산술 0.508 / 0.210 / 0.110 / 0.061) ④ 같은 재료 실험 끝 용량 ≈195 / ≈173 / ≈114 mAh g⁻¹ (0.02 / 0.1 / 0.5 C · Rueß 2020 셀) [판독] — 맞추는 데 쓰지 않음 | 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 재료 계는 같다 (다결정 NCM811 + Li₆PS₅Cl) — 그러나 **압력 · 역학 · 탄소 · 바인더 없음** · CAM 42 vol% (70 : 30 wt%) · SE 연속체 (펠릿 σ 0.7) · 3D 40³ µm³ · T 273.15 K (인쇄) · 정전류 첫 충전만.

## 9. 적용 인사이트 (행동)
1. **STEP4 결과 전 대조 (흐름 밖)**: Fig. 7a D̃(SOC) · j₀(SOC) · SI Fig. S2 OCV (digitized.csv) 를 같은 계 측정 입력으로 등록 — 우리 다결정 D 기본값 3 × 10⁻¹⁴ m² s⁻¹ (측정 아님 [우리]) 는 이 곡선 최대 6.9 × 10⁻¹⁶ 의 ≈44 배 [카드 산술].  맞추지 말고 곡선 그대로 한 팔을 돌려 차이를 기록 (이 논문의 *"Achilles heel"* 경고 · 상수 입력으로는 첫 전압 상승을 못 낸다).
2. **j₀ 를 옮길 때 면적 기준을 함께 (Rint ② · 흐름 밖)**: R_CT → j₀ (식 [12]) 는 면적 A 를 품는다 — 모델 0.17 ↔ BET 0.2 m² g⁻¹ 만큼 (×1.18) 갈린다.  kim2024 의 "i₀,ref 0.05 A/m²" 처럼 원문에 없는 상수를 출처로 묶지 않는다 (카드 문제).
3. **피복 정의에 분포 척도 (단계 7)**: 같은 남은 계면 70 % 에서 공극 크기 비 1.2 ↔ 10 의 0.2 C 과전압 65.9 ↔ 14.4 mV [판독] → 우리 피복 출력 (Hertz · Tabor 띠 몫) 에 '가장 큰 덮이지 않은 조각' · 조각 수 같은 분포 척도를 결과 전에 함께 등록.
4. **PSD 부피 가중 꼬리 (단계 5 · 흐름 밖 입도 설계)**: 수 6–7 % 의 큰 입자가 CAM 부피 42–62 % · 표면적 −35 % [카드 산술 · 인쇄] — DEM 침대 · 실험 PSD 를 보고할 때 수 분포와 함께 부피 가중 꼬리 (d > d₉₀) 를 적는다.
5. **모델 기공 칸 (단계 0)**: 문헌 전기화학 시뮬을 인용할 때 '그 모델의 기공' (여기 0 % · 실물 14 %) 과 '부피분율의 밀도 기준' (여기 암묵 1.95) 을 함께 적는다.
6. **우리 A10 접촉 원장 (흐름 밖 · 열화)**: 원장의 R_ct ∝ 1/A 는 반응 몫만 — 이 논문은 공극 과전압이 율 · 용량에 따라 크게 달라 (0.02 C 7 mV ↔ 0.2 C 47 mV · @50 > @100) 확산 몫이 섞임을 보인다 → 원장 결과에 "반응 몫만 · 확산 몫 미포함" 한정어.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A 3D finite-element model of NCM811/Li₆PS₅Cl composite cathodes fed only with state-of-charge-dependent inputs measured on the same materials (no fitted parameter) reproduced experimental charge curves at 0.02–0.5 C; the curve shape was set by the SOC dependence of the Li diffusion coefficient and exchange current density rather than by the microstructure (Bielefeld et al., *J. Electrochem. Soc.* 169 (2022) 020539)."
- "In a single-particle model, hemispherical voids reducing the CAM/SE interface of a 7 µm NCM811 particle to ≈53 % raised the charge overpotential at 0.2 C by ≈40–47 mV [figure reading], and at fixed 70 % interface a few large voids cost more than many small ones (Bielefeld et al., 2022)."
- 국문 (한정어와 함께): *"같은 재료 측정 입력만으로 (맞춤 0) NCM811 / Li₆PS₅Cl 양극의 충전 곡선을 3D FEM 으로 재현했다 — 단 SE 는 이상 접촉 연속체 (기공 · 입계 · 협착 없음) 이고 역학 · 압력은 없다 (Bielefeld 2022). 계면 공극 과전압 (≈40–47 mV @0.2 C · 남은 계면 53 %) 은 그림 판독값이다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-9 의 1–7.
**카드가 본 한계**
1. **역학 · 압력 · 탈압 없음** — 공극 · 접촉 잃음은 주어진 고정 기하 · 수축 · 압력에 따른 생성 · 소멸 없음.
2. **SE 연속체 (CF 상한)** — 입계 · 협착 · 기공 없음 · 펠릿 σ 0.7 (조건 [미확인]) · 입자형 모델 기공 0 % (실물 14 %).
3. **입력은 2 차 출처** — 표 S2 의 σ_SE · j₀ · OCV · D̃ · 200 mAh g⁻¹ 는 Rueß 2020 표기 · 측정 조건 (셀 압력 · 온도 · 전극) 은 이 논문에 없다 · T 273.15 K 인쇄.
4. **공극 과전압은 그림 판독** · 0.5 C 공극 값 없음 · 본문 '50 mV' 문장과 그림이 다름 · 공극 크기 '4 µm' 오기 가능성.
5. **통계**: S-PSD 시드 셋 뿐 · 나머지 한 실현 · 격자 수렴 · 시간 수렴 보고 없음.
6. **원뿔 비교의 조건 차**: 55 vol% 원뿔 ↔ 42 vol% 실험 · 입자형 (원문도 *"not directly comparable"*) · 원뿔 면적 계산법 미기재 (20 µm 점이 내 산술과 −12 %).
7. **전이 한계**: 같은 재료 계라도 탄소 · 바인더 · 압력 없음 · 첫 충전만 · 40 µm 얇은 전극.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [10] | R. Ruess, S. Schweidler, H. Hemmelmann, G. Conforto, A. Bielefeld, D. A. Weber, J. Sann, M. T. Elm, and J. Janek, J. Electrochem. Soc., 167, 100532 (2020). | ★ 모든 SOC 의존 입력 (GITT D̃ · EIS R_CT · OCV · σ_SE 0.7) 과 검증 셀 (70 : 30 · 공극 14 %) 의 원 측정 — 카드 없음 (benhadjali · taghikhani · doerrer · stallard 카드가 인용만) |
| [47] | G. Conforto, R. Ruess, D. Schröder, E. Trevisanello, R. Fantin, F. H. Richter, and J. Janek, J. Electrochem. Soc., 168, 070546 (2021). | 임피던스 기반 입도 (PSD) · 검증 실험 — 카드 없음 (kissel2025 · li2026 · taghikhani 인용만) |
| [8] | R. Koerver, I. Aygün, T. Leichtweiß, C. Dietrich, W. Zhang, J. O. Binder, P. Hartmann, W. G. Zeier, and J. Janek, Chem. Mater., 29, 5574 (2017). | 접촉 잃음 SEM (Fig. 2 재수록) · 큰 공극의 근거 — 카드 없음 (koerver2018 은 다른 편) |
| [57] | T. Ates, M. Keller, J. Kulisch, T. Adermann, and S. Passerini, Energy Storage Mater, 17, 204 (2019). | 슬러리 · 미압연 양극 공극 20–40 % — 카드 없음 |
| [58] | D. H. Kim, D. Y. Oh, K. H. Park, Y. E. Choi, Y. J. Nam, H. A. Lee, S. M. Lee, and Y. S. Jung, Nano Lett., 17, 3013 (2017). | 침투로 공극 6–8 % — 카드 없음 |
| [38] | A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Ning, J. Marrow, F. H. Richter, J. Janek, and A. Latz, ACS Appl. Mater. Interfaces, 12, 9277 (2020). | CT 재구성 NCM622/β-Li₃PS₄ 양극의 방전 시뮬 · 전자 한계 — 카드 없음 (여러 카드 인용만) |
| [37] | M. Finsterbusch, T. Danner, C. L. Tsai, S. Uhlenbruck, A. Latz, and O. Guillon, ACS Appl. Mater. Interfaces, 10, 22329 (2018). | 이 모델 꼴의 원형 — 카드 없음 |
| [48] | K. Märker, P. J. Reeves, C. Xu, K. J. Griffith, and C. P. Grey, Chem. Mater., 31, 2545 (2019). | NCM811 dQ/dV 두 봉우리 · Li₀.₂₂ 아래 급상승 — 카드 없음 |
| [43] | M. Weiss et al., Adv. Energy Mater, 11, 2101126 (2021). | R_CT ↔ j₀ 식 [12] 의 출처 — 카드 없음 |
| [53] | A. Falconi, Electrochemical Li-Ion Battery Modeling for Electric Vehicles Thesis, Communauté Université Grenoble Alpes (2017). | 상수 D̃ 시뮬 정리 · j₀ 맞춤 관행 — 카드 없음 |
| [24] · [25] · [27] · [56] · [44] · [40] · [11] · [13] · [26] · [23] | Bielefeld 2019 · 2020 · Minnmann 2021 · Hlushkou 2018 · Park 2020 (AEM 10, 2001563) · Amin & Chiang 2016 · Trevisanello 2021 · Doerrer 2021 · Shi 2020 · Strauss 2018 | 정본 카드 있음 (`bielefeld2019_…` · `bielefeld2020_…` · `minnmann2021_…` · `hlushkou2018_…` · `park2020_digitaltwin_…` · `aminchiang2016_…` · `trevisanello2021_…` · `doerrer2021_…` · `shi2019_…` · `strauss2018_…`) |

## 13. [미확인] 목록 (본문 13 쪽 + SI 14 쪽 전수에 없음)
1. 실험 (Rueß 2020 셀) 의 셀 압력 · 온도 · 전극 두께 · 적재 · 실측 기공의 정의.
2. 모델 온도 273.15 K 가 의도인지 (실험 온도와의 대조).
3. ρ_SE (42 vol% 환산의 기준) · c_ref 49 mol L⁻¹ 의 근거.
4. 격자 · 시간 간격 수렴 시험 · 계산 시간.
5. 42 vol% 원뿔의 a · b · 원뿔 활성 계면의 계산법 (끝면 포함 여부 · 20 µm 점).
6. 0.5 C 공극 과전압 값 (본문 "50 mV" 문장) · 1-입자 모델의 분리막 · 음극 배치.
7. 공극 크기 '최대 4 µm' ↔ 비 1.2 · SI Fig. S5 "7.0 µm voids" · S7 범례 ↔ 그림 8 표지.
8. 그림 6 색 막대의 로그 밑 · 단위.
9. 식 [1] · [4] 부호 규약과 COMSOL 구현의 관계.
10. 1-입자 공극의 실제 덮임 (목표와의 차) 값.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-22)
- 본문 13 쪽 (+ IOP 표지) + SI 14 쪽 (+ 표지) 을 글자 층 추출 + 그림 · 식 렌더로 읽음.  서지 = 본문 첫 쪽 (제목 · 저자 다섯 · 소속 · DOI · 접수 · 수정 · 출판일) · 쪽 아래 "1945-7111/2022/169(2)/020539/13" (호 · 쪽 수) · 감사 (VW · FESTBATT · ProFeLi).  SI 첫 쪽 = 같은 제목 · 저자.  원문 낱말 셈 (본문): DEM = 0 · discrete 1 (p.12 *"a cone instead of discrete particles"*) · pressure 1 (p.10 *"external pressure"*) · pressing 1 (p.13 *"isostatic hot pressing"*) · press cell 2 · mechanical 4 (p.2 chemo-mechanical · p.10 *"mechanical rigidity"* · p.13 둘) · stress · strain · plastic · elastic = 0 / SI: 위 낱말 모두 0 (contact 1 = 집전체 접촉).
- 그림 크롭 **71 장** = 도구 17 (본문 그림 1–11 · SI 그림 S1 · S3 · S4 · 표 S1–S3 — **다시 자름 7**: fig_6 (본문 문장을 캡션으로 · 색 막대 이름표 잘림) · fig_S1 (실은 S2 자리 — SI 캡션이 그림 아래) · fig_S3 (위 잘림) · fig_S4 (빈 여백) · tab_S1 · tab_S2 · tab_S3 (쪽 머리글 · 본문 두 절 섞임)) + 손 크롭 54 (Table I · SI 그림 S2 · S5–S8 · 패널 5 · 식 23 · 근거 문단 20).  본 뒤 다시 렌더 = tab_1 · fig_S6 · fig_5a · fig_7a · fig_8_right · fig_9_right · fig_10_right · eq_S02 · eq_S03 · eq_S06 · txt_p4_j0_soc_rct · txt_p5_agreement_not_fitted · txt_p8_constant_inputs.  71 장 전부 Read 로 열어 확인 — `figures.json` 의 `recrop` · `manual_crop` · `note_manual`.
- 판독: digitized.csv 319 행 — 그림마다 축 보정 · 판독 방법을 note 열에.  Fig. 5a 판독이 Table I 입자 수 (266 · 249 · 248 · 177 · 128) 를 정수로 재현 · Fig. 7a 상수선 판독이 인쇄 6.8 · 3.5 · 1.55 · 0.90 재현 · 원뿔 b/a 식 (9) 재현 0.6622.
- 2 차 인용 대조: 가리킨 카드 kim2024_optimal (L115 · L279) · lee2024_shear (L44 · L390 · L415) + 인용 카드 benhadjali2025 (L116 · L384) · benhadjali2026_oneway (L100 · L405) · taghikhani2025 (L108–111 · L139 · L161 · L178 · L183) · jeong2024 (L348) · lin2025 (L52) · reisacher2023 (L60) — 고치지 않았다 (카드 문제 = 정독 출력 batch_138 의 '카드 문제' 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (bielefeld* = 2019 · 2020 만) + DOI (ac50df · 020539) · 제목 낱말 grep — 카드 없음 (인용만: 위 카드들) (2026-11-22).

## 🔗 관련 카드
- 같은 1 저자 앞 편: `bielefeld2019_microstructural_modeling_composite_cathode` (3D 복셀 퍼콜레이션 — 이 논문 SI 의 '무작위 구는 42 vol% 에서 전자 퍼콜레이션 불가' 근거) · `bielefeld2020_effective_ionic_conductivity_binder` (유효 σ_ion · 바인더).
- 이 논문 값을 입력으로 옮긴 3D · 2D 모델: `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` · `benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode` · `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode`.
- 같은 질문 (피복 · 공극 → 이용률): `lee2024_shear_force_dry_process_cathode_coverage` (2D 단일 입자 · 10–100 % · ≤ 5 C) · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` · `hlushkou2018_void_space_ion_transport_assb_cathode` (공극 → tortuosity) · `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2022_designing_cathodes_solidstate`.
- 같은 그룹 입자 · 확산: `trevisanello2021_sc_pc_ncm_cracking_diffusion` · `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` · `strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation` · `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` (ref 40).
- 입자 배치 생성기 계보: `park2020_digitaltwin_assb_foundational` (ref 44 · 같은 GeoDict 접근) · `shi2019_high_am_loading_particle_size_assb`.
- 공극 논거로 인용한 카드: `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` · `lin2025_submicron_lpscl_cathode_li_kinetics` · `reisacher2023_percolation_sulfide_carbon_matrix`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
