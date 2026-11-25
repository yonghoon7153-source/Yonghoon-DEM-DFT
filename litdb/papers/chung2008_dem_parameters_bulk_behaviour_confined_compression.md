<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     본 = coetzee2017_dem_calibration_review.md (DEM 보정 방법론 · 직접 측정 ↔ 벌크 역보정 두 학파 · 강성 감소 증거표) · 절 체계 = tian2017_contact_area_loss_assb_simulation.md · ohashi2020_stress_distribution_composite_electrode_sulfide_assb.md (같은 키트 · 같은 날).
     고른 의도 = 위시 11-17 W-1117-5 · 정독 batch_75 (morrissey2013) 의 n 줄 — §0-1.
     쪽 표기 = 인쇄 쪽 (학술지 pp. 83–96).  PDF 쪽 = 인쇄 쪽 − 81 (PDF p.1 = Taylor & Francis 내려받기 표지 · 논문 아님).  글 크롭 파일 이름 txt_p<n> = 인쇄 쪽 · figures.json 의 page = PDF 쪽 (도구 관례) · page_printed = 인쇄 쪽.
     보충 자료 (SI) = 원문에 안내 없음 (14 쪽 텍스트 층 전수에 'supplement' · 'supporting' 0 회) · 그래픽 초록 없음 · 받은 날 · 고친 날 · 자금 · 감사의 글 = 인쇄 없음.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 118 행 · 300 dpi 원 래스터 패널에서 열 · 행 단면의 선 중심 →
     축 = Excel 그림 영역 테두리선 = 인쇄 축 끝값 · 눈금 대조 오차 ≤ 범위의 0.4 % · 계열 = 선의 회색 농도 · 모양) · [판독 · 눈으로] = 눈어림 (오차 병기) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 · 가정 병기) ·
     [카드 해석] · [카드 추론] = 원문에 말이 없어 이 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 원문 (본문 14 쪽 + 표지) 에 없음. -->
# 구속 압축 DEM 의 매개변수 민감도 — 유리구슬 (Ø10 mm 단분산 구 · E 41 GPa) · 옥수수 (겹친 구 4 개 · E 1.66 GPa) 를 Ø145 mm 아크릴 원통 (Ko 시험기 개조) 에서 위 판으로 ≈0.8–1 kN (≈48–61 kPa) 까지 누름 · Hertz-Mindlin 무점착 탄성 접촉 · 실험 대조 — 입자 강성을 1/100 · 1/10⁴ 로 낮추면 **벌크 강성은 직접** 바뀌고 (790 N 판 변위 7.27 → 10.25 → 36.83 mm) **벽 · 바닥 하중 전달은 부차** (바닥 몫 유리 0.74 → 0.62 → 0.57 · 옥수수 0.64 → 0.64 → 0.69) · 초기 충전 (생성 간격 1.01 / 1.50 / 2.00 d · FCC · Rhombic · Random) 에 구는 민감 (K 0.34–0.70 ↔ 실험 ≈0.4) · 입자 간 마찰은 옥수수에서만 (μp 0.168 → 0.670 : K 0.47 → 0.27) · 하중 제거 없음 — Chung & Ooi (Particulate Science and Technology 2008)

> slug `chung2008_dem_parameters_bulk_behaviour_confined_compression` · DOI `10.1080/02726350701759381` · type `DEM (PFC3D 3.0 · Hertz-Mindlin no-slip + damping + Coulomb slider · 3,591 monosized glass beads d 10 mm / 4,672 four-sphere corn clumps · grid generation switched on + 2.56 m/s fall · top platen 50 mm/min to about 0.8-1 kN in a 145 mm cylinder) + experiment (Ko-type confined compression tester, Instron 1.5 mm/min, bottom load cell + four wall strain rosettes) — sensitivity to initial packing, particle stiffness (G0, 0.01G0, 0.0001G0) and interparticle friction; loading only, no unloading, no plasticity, no adhesion` · PDF `Influence_of_discrete_element_model_parameters_on_bulk_behavior_of_a_granular_solid_under_confined_compression.pdf` · digested `2026-11-17` · status ✅
>
> **저자 (머리글 그대로)**: **Y. C. Chung**¹ · **J. Y. Ooi**² (교신) — ¹ Department of Civil and Environmental Engineering, Nanya Institute of Technology, Chungli, Taoyuan, Taiwan · ² Institute for Infrastructure and Environment, University of Edinburgh, Edinburgh, United Kingdom · *Particulate Science and Technology* **26** (1) **83–96** (**2008** = 인쇄 머리 *"Particulate Science and Technology, 26: 83–96, 2008"* · p.83) · ⚠ T&F 표지의 인용 줄은 *"Y. C. Chung & J. Y. Ooi (2007) … 26:1, 83-96"* · 표지 *"Published online: 03 Mar 2011"* (`txt_cover_p83_to_cite_2007_printed_2008_online_2011.png`) — **slug 연도 = 인쇄 호 2008** · 위시 · morrissey2013 참고문헌의 '(2007)' 은 표지 인용 줄 · 학위논문 목록과 같은 꼴 (§0-1) · Copyright © Taylor & Francis Group, LLC · ISSN 0272-6351 print / 1548-0046 online · 받은 날 · 자금 · 감사의 글 [미확인 — 인쇄 없음].
> **이웃 카드 (링크만)**: [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) (같은 그룹 (Edinburgh · Ooi) 학위논문 · 이 논문 = 그 참고문헌 · p.94 · 95 · 152 · 203 · 같은 꼴 K0 시험기 (그 카드 §5.5 요약 — 아크릴 원통 높이 380 mm · 지름 144 mm [다른 카드]) · 고른 의도의 출처 · §0-1) · [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md) (두 학파 — 이 논문 = '직접 측정' 학파의 검증 예 [카드 해석] · ⚠ 그 카드 §7 표의 *"Chung & Ooi [161] 구형 캡 로드 관입 ÷10⁴"* 는 **이 논문이 아니다** — 이 논문에 관입 시험 없음) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md) (입자 탄성 물성 → DEM 결과 리뷰 · 강성 감소 규칙) · [`thakur2014_eepa_adhesive_elastoplastic_dem`](thakur2014_eepa_adhesive_elastoplastic_dem.md) (같은 그룹 · 접촉 소성 + 점착) · [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (벌크 역보정 학파 예) · [`walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem`](walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem.md) (다른 Walton — 이 논문 인용은 Walton 1994 워크숍 판 · 마찰 · 형상 → 안식각).
> **판독 원자료**: `litdb/figures/chung2008_dem_parameters_bulk_behaviour_confined_compression/digitized.csv` (118 행 — 그림 3–12 · 원 래스터 패널 열 / 행 단면 · 방법은 행마다) · 크롭 **54 장** (도구 14 = 그림 1–12 + 표 1–2 → 그림 12 장 모두 원 래스터에서 다시 자름 (도구 판 = 300 dpi 재렌더 = 리샘플 · 그림 6 = 캡션 폭으로 넓힌 여백) · 표 2 장 = 도구가 쪽 전체 (두 표 + 사이 본문) 를 같은 그림으로 잘라 손으로 다시 / 손 크롭 40 = 패널 18 · 식 2 (번호 1–2 전부) · 근거 문단 20 — 본 뒤 다시 자름 14 (글 크롭 가장자리가 이웃 줄을 물었다)) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 이 논문은 **입자 물성을 벌크 시험에 맞추지 않고 입자 수준에서 따로 잰 뒤** (E = 단입자 압축 + Hertz 가정 · 마찰 = 세 입자 미끄럼 · 반발 = 낙하 시험 · 입자–입자 값은 입자–면 값과 같다고 가정, p.86–87) PFC3D 로 **아크릴 원통 구속 압축 (≤ ≈1 kN ≈ 61 kPa)** 을 그대로 풀어 실험의 **바닥 판 힘 · 측압비 K · 벽 마찰 동원 μbulk** 와 견주고, 세 매개변수를 흔든다: ① **초기 충전** — 단분산 구 (유리) 는 생성 방법에 민감해 FCC · Rhombic (조밀 결정) 과 거의 맞닿은 생성 (1.01d) 은 바닥 힘이 크고, Random · 1.50d · 2.00d 는 실험 바닥 힘 (≈50 %) 과 맞지만 **K 는 실험 ≈0.4 와 맞지 않는다** (DEM 0.34–0.70 [판독]); 옥수수 (겹친 구 4 개) 는 덜 민감 (실험 65 % · K ≈0.35 · μbulk ≈0.32 와 '합리적 일치') ② **입자 강성** (G₀ → 0.01G₀ → 0.0001G₀) — *"the bulk stiffness in confined compression was directly influenced by the particle stiffness"* · 그러나 벽 · 바닥으로 가는 힘 전달은 덜 (옥수수 1/100 에서 차이 없음 · 유리는 무를수록 벽 마찰이 더 동원돼 바닥 힘 감소) ③ **입자 간 마찰** — 유리 (μp 0.12–0.98) 는 바닥 힘이 그대로 · 옥수수는 마찰을 반으로 줄이면 더 많은 접촉이 한계 마찰에 닿아 K ↑ · 바닥 힘 ↓ (유리는 옥수수보다 20 배 넘게 단단해 미끄럼이 모자람).  **하중을 빼는 계산 · 측정은 없다** (p.93 의 'sudden unloadings' = 싣는 동안의 힘 급락).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 어떤 매개변수가 벌크 응답을 정하나 — 벌크 강성 · K0 · 응력–변형 · 하중 제거 | **벌크 강성 (하중–변위)** = 입자 강성 (G) 이 직접 (790 N 판 변위 유리 7.27 · 10.25 · 36.83 mm · 950 N 옥수수 7.77 · 17.86 · 77.86 mm — G₀ · 0.01G₀ · 0.0001G₀) · **K** = 충전 구조 (유리 Rhombic 0.34 · FCC 0.51 · Random 0.70 · 간격 셋 ≈0.66) + 입자 간 마찰 (옥수수 μp 0.168 · 0.335 · 0.670 → 0.47 · 0.36 · 0.27) · **μbulk (벽 마찰 동원)** = 미끄럼 변위 (무른 입자일수록 입력값 0.24 · 0.34 에 다가감) · **바닥 몫** = K·μbulk 곱 · **하중 제거 = 없음** · 구름 저항 · 감쇠 · 입도 = **흔들지 않음** | [인쇄] p.89–94 · [판독] 그림 4 · 5 · 7–12 |
| ② 보정 방법 — 벌크 응답으로 입자 매개변수를 고르나 · 실험 대조 · 재료 | **고르지 않는다** — 입자 수준 독립 측정 (Table 1–2 · CoV 병기) → 벌크 실험과 **검증** 대조 (*"The key properties of the particles were independently measured"* p.83) · 입자–입자 μ · e 만 가정 (입자–면 값) · 재료 = **유리구슬 (Sigmund Lindner · Ø10 ± 0.5 mm) · 옥수수 낟알** (전지 재료 아님) · 시험 4 회씩 | [인쇄] p.83 · p.86–87 · Table 1–2 |
| ③ 못 하는 것 — 형상 · 소성 · 파쇄 · 조밀 영역 | 형상 = 구 / 겹친 구 4 개 (변형 없음) · 소성 · 파쇄 · 점착 = **없음** (탄성 Hertz-Mindlin) · 입도 분포 없음 (*"Particle size variation was not considered"*) · 조밀 영역 한계 = **말 없음** (응력 ≤ ≈61 kPa) · 원문 스스로: *"the DEM model of perfect spheres with perfect symmetry … is not an appropriate representation even for the uniform glass beads … This cast doubt on many of the DEM studies in the literature based on perfect spheres"* (p.95) | [인쇄] p.85 · p.94–95 |
| ④ 우리 E_eff 18 배 연화 · 다압력 Heckel · 언로딩 해석 기준 | 연화가 **바꾸는 것 (벌크 강성 = 압축 변위)** 과 **덜 바꾸는 것 (벽 · 바닥 힘 전달)** 을 실험 대조와 함께 가른 DEM 예 — 우리 18 배 연화는 바로 '바꾸는 쪽' (기공 · 두께) 에 맞춘 것이라 **물성이 아니라 벌크 보정 손잡이** 임을 뒷받침 [카드 해석] · 이 논문의 강성 감소 목적은 계산 시간 (*"critical time step is inversely proportional to √G"* p.90) · Heckel · 다압력 · 기공 = **없음** · 하중 제거 = **없음** | [인쇄] p.90–91 · p.95 · [카드 해석] |
| ⑤ 충전 (초기 구조) 의존 — 단계 4 의 출발 상태 | 격자 생성 + 'switched on' + 2.56 m/s (= 335 mm 낙하) 자유 낙하 · 정착 = 운동 에너지 < 10⁻⁸ J · 평균 불균형 힘 < 10⁻⁶ N · 간격이 충분하면 (≥ 1.5d) 무작위 충전이 되어 실험 바닥 힘과 맞음 · 거의 맞닿게 (1.01d) 생성하면 벽 마찰 동원이 작아 (μbulk 0.08 ↔ 0.14) 바닥 힘이 큼 · 체 낙하를 그대로 모사하는 것은 *"large and impractical"* | [인쇄] p.86–89 · [판독] 그림 3b · 5b |
| ⑥ DEM 한계 · 소성의 어려움 · 2D/3D · 탈압 (묶음 공통) | DEM 한계 = 완전 구 (결정화 · 회전 과다) · 단분산 · 판 속도 33 배 · 입력값이 흔히 재지 않고 가정됨 (초록) · 소성 = 다루지 않음 · 3D (PFC3D) — 2D 는 Boutt & McPherson 2002 의 2-D 충전 연구를 근거로만 · 탈압 = 없음 | [인쇄] p.83 · p.86–87 · p.93 · p.95 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **유리구슬 · 옥수수 낟알** (mm 크기 · LPSCl · NCM 없음) ② 응력 = 위 하중 ≈0.8–1 kN ÷ 원통 단면 0.01651 m² = **≈48–61 kPa** [카드 산술] — 우리 300 MPa 의 약 1/6,200 ③ 접촉 = **탄성 Hertz-Mindlin 무점착** (소성 · 파쇄 · 점착 0) ④ 단분산 · 원통 지름 / 입경 = **14** (실험 산포의 원인으로 원문이 지목) ⑤ DEM 판 속도 **50 mm/min = 실험 1.5 의 33 배** ⑥ **하중 제거 없음** ⑦ 숫자의 대부분이 **그림 판독** (본문 숫자 = 실험 K · μbulk · 바닥 몫 · 입력값 · 생성 · 정착 · 속도 조건뿐) ⑧ **유리구슬 DEM 은 실험과 맞지 않는다** — 원문 스스로 (p.90) · K 는 DEM 0.66–0.70 ↔ 실험 ≈0.4, μbulk 0.08–0.15 ↔ ≈0.35 [판독] ⑨ 강성 감소 연구에 쓴 유리구슬 생성은 원문이 밝히지 않았고, 그림으로는 1.01d 로 읽힌다 (§3-7).
⇒ **절대값 전이**: 하지 않는다 (재료 · 크기 · 응력 · 접촉 법칙이 모두 다르다).  옮길 수 있는 것 = **꼴과 절차** — (i) 입자 강성 → 벌크 강성은 '직접', 벽 하중 전달은 '부차' (이 응력 범위 · 탄성) (ii) 단분산 구는 생성 방법에 민감 — 간격이 너무 좁으면 (1.01d) 벽 마찰 동원이 달라진다 · 결정 충전 (FCC · Rhombic) 은 바닥 힘을 키운다 (iii) 바닥 몫은 K·μbulk 의 곱이 정한다 (실험 값 둘을 Janssen 꼴에 넣으면 바닥 몫 49 · 65 % 가 그대로 나온다 [카드 산술 §3-6]) (iv) 벽 마찰은 미끄럼 변위가 있어야 동원된다 — 단단한 입자 · 작은 변형에서는 입력 마찰보다 훨씬 작게 동원 (v) 입자 물성은 입자 수준에서 따로 재고 벌크 시험은 **검증** 으로 남긴다.

---

## 0-1. ★ 고른 의도 대조 (위시 11-17 W-1117-5 · batch_75 n 줄 + 본 세션 의도 셋)

의도 원문 (wishlist 원문 그대로): *"[n] Chung, Y.C. and Ooi, J.Y. (2007). Influence of Discrete Element Model Parameters on Bulk Behavior of a Granular Solid under Confined Compression. Particulate Science and Technology, 26(1): pp. 83–96, doi:10.1080/02726350701759381. | 구속 압축 DEM 의 매개변수 민감도 · 충전 의존 (p.94 · p.152 · p.203) — 단계 4 · 단계 6 (구속 압축 · K0) · 질문 b | litdb 확인: chung 카드 없음 (coetzee2017 · 이 카드가 언급만)"* (쪽 = morrissey2013 학위논문 안의 쪽).  본 세션이 덧붙인 의도 = ① [DEM 우선 Ⓐ] 구속 (일축) 압축 DEM 에서 어떤 매개변수 (입자 강성 · 마찰 · 구름 · 감쇠 · 입도 · 충전 밀도 · 충전 방법) 가 벌크 강성 · K0 · 응력–변형 곡선 · 하중 제거 (제하 · 탈압) 곡선을 정하나 — 우리 DEM 보정 (E_eff 18 배 연화 · 다압력 Heckel) 과 언로딩 키트 · 탈압 A 의 해석 기준 ② 보정 방법 (벌크 응답으로 입자 매개변수를 고르는 꼴 · 실험 대조 여부 · 재료) ③ 못 하는 것 (입자 형상 · 소성 · 파쇄 · 조밀 영역 한계).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 (계산) 조건 |
|---|---|---|
| "구속 압축 DEM 의 매개변수 민감도" | **채움** | 세 매개변수: 초기 충전 (그림 3–7 · p.87–90) · 입자 강성 G₀ · 0.01G₀ · 0.0001G₀ (그림 8–10 · p.90–92) · 입자 간 마찰 μp 유리 0.122 · 0.244 · 0.488 · 0.976 (×0.5 · 1 · 2 · 4) · 옥수수 0.168 · 0.335 · 0.670 (×0.5 · 1 · 2) (그림 11–12 · p.92–94) · 조건 = 아크릴 원통 Ø145 mm · 위 판 DEM 50 mm/min (실험 1.5) · 위 하중 0 → ≈800 N (유리) · ≈1000 N (옥수수) = ≈48 · 61 kPa [카드 산술] · **누른 채 (싣는 중)** 만 · 상온 (온도 [미확인]) |
| "충전 의존" | **채움** | 유리 785 N 바닥 몫 Rhombic 0.85 · FCC 0.75 · Random 0.58 · 간격 1.01d 0.74 · 1.50d 0.58 · 2.00d 0.56 ↔ 실험 ≈0.50 [판독 그림 3 · 인쇄 p.87] · K Rhombic 0.34 · FCC 0.51 · Random 0.70 · 간격 셋 ≈0.66 ↔ 실험 ≈0.4 [판독 그림 4a · 5a] / 옥수수 950 N 바닥 몫 1.01d 0.64 · 2.00d 0.57 · 1.50d 0.55 ↔ 실험 65 % · K (880 N) 0.36 · 0.40 · ≈0.43 ↔ ≈0.35 [판독 그림 6 · 7a · 인쇄 p.90] · ⚠ **충전 밀도 (기공률) 는 보고하지 않는다** — 생성 방법 · 간격만 |
| "단계 4 (구속 압축)" | **일부** | 구속 압축 실험 · DEM 은 있다 · 그러나 mm 크기 탄성 입자 · kPa · 단분산 · 기공률 없음 — 우리 단계 4 (순수 SE 가루를 붓고 300 MPa 로 눌러 항복 세기 하나를 기공에 맞춤) 의 **출발 상태 만들기 (생성 · 정착 판정) 와 경계 관측량 (K · 벽 마찰)** 만 옮길 수 있다 [카드 해석] |
| "단계 6 (탈압) · 질문 b (되돌아옴)" | **없음** | 하중 제거 · 되돌아옴 계산 · 측정 0 · 그림 8 = 싣는 곡선만 · p.93 *"the glass beads displayed more sudden unloadings especially for higher interparticle friction … The experiments did not show any significant unloading for both materials"* = **싣는 동안의 힘 급락** (원문 원인 추정 = 50 vs 1.5 mm/min 속도) — 탈압 뜻 아님 (`txt_p93_glass_bottom_same_mu_0p12_0p98_sudden_unloadings_rate.png`) |
| "K0" | **채움 (정의 · 값) · 한정** | 원문 용어 = *"lateral pressure ratio K"* (사일로 설계 · EN 1991-4) · 장치 = *"modified from the Ko tester by Masroor et al. (1987)"* (p.84) · 정의 = 식 1 K = σH/σ̄V (σ̄V = 위 · 아래 판 하중 평균 · σH = 게이지 높이 원주 변형으로) · *"can be approximately evaluated"* (p.85) · 실험 K ≈0.4 (유리) · ≈0.35 (옥수수) [인쇄 p.88 · p.90] · DEM K = 벽 경계 힘에서 (p.89) · ⚠ 아크릴 벽이 변형한다 (원주 변형을 재서 σH 를 냄) → 엄밀한 '측방 변형 0' K0 가 아니라 **거의-K0** [카드 해석] · 뺄 때 K 의 변화 = 없음 |
| ① 벌크 강성을 정하는 매개변수 | **채움 (강성)** | *"the bulk stiffness in confined compression was directly influenced by the particle stiffness. The relationships between bulk stiffness and particle stiffness have been derived from these results (Chung, 2006)"* (p.91) — 관계식 자체 [미확인 — Chung 2006 학위논문] · 판독 값 §3-4 |
| ① K0 를 정하는 매개변수 | **채움 (충전 · 마찰) · 강성 = 말 없음** | 충전 (유리 · 그림 4a) · 입자 간 마찰 (옥수수 · 그림 12a) · *"K is a bulk property that relates to the propensity for lateral expansion and has been shown to relate well to the Poisson's ratio of the bulk material"* (p.89) · 강성별 K 그림 없음 [미확인] |
| ① 응력–변형 곡선 | **채움 (싣기만)** | 그림 8 (위 하중 vs 판 변위 · 강성 셋) · 변위 영점 정의 [미확인] (곡선이 ≈4–5 mm 에서 일어선다 [판독]) |
| ① 하중 제거 곡선 | **없음** | 위 행 |
| ① 구름 저항 · 감쇠 · 입도 · 충전 밀도 | **없음 · 없음 · 없음 · 일부** | 구름 저항 = 모델에 없음 (Hertz-Mindlin + 감쇠 + 미끄럼 · p.85 — 옥수수 형상은 겹친 구로) · 감쇠 = 있다고만 (값 · 종류 [미확인]) · 입도 = 단분산 (*"The influence of polydispersity should be further investigated"* p.94–95) · 충전 밀도 = 생성 간격 · 구조만 (밀도 · 기공 값 없음) |
| ① 우리 18 배 연화 · Heckel 의 해석 기준 | **일부** | 강성을 낮추면 압축 변위가 늘고 (벌크 강성 직접) 경계 힘 전달은 덜 바뀐다 (§3-4) — 우리 연화의 '바뀌는 쪽' 이 기공 · 두께라는 점을 정리하는 근거 [카드 해석] · Heckel · 다압력 · 300 MPa 급 · 기공 = 없음 |
| ① 언로딩 키트 · 탈압 A 의 해석 기준 | **없음** | 하중 제거 0 · 옮길 것 = 정착 판정 꼴 (불균형 힘 / 입자 무게) · 경계 관측량 (판 · 벽 힘 · 링 구간 벽 마찰) 뿐 [카드 해석] |
| ② 벌크 응답으로 입자 매개변수를 고르는 꼴 | **없음 (반대 꼴)** | 이 논문은 고르지 않는다 — 입자 수준 측정 → DEM → 벌크 실험 대조 (직접 측정 학파 [카드 해석 · coetzee2017 §1 의 용어]) · 흔든 값은 감도 · 원인 분석용 · 입자–입자 μ · e = 입자–면 값 가정 (p.87 · p.92) |
| ② 실험 대조 여부 | **채움** | 같은 장치 실험 4 회씩 (Test 1–4) · 바닥 힘 · K · μbulk · 원통 지름 / 입경 14 → 산포 큼 (p.90) · 결과: 옥수수 '합리적 일치' · 유리 '일치 아님' (p.90) |
| ② 재료 (어떤 입자?) | **채움** | 유리구슬 Ø10 ± 0.5 mm · ρ 2530 · E 41 GPa · ν 0.22 / 옥수수 10.11 × 9.11 × 6.69 mm · ρ 1280 · E 1660 MPa (CoV 31 %) · ν 0.40 (Table 1–2 [인쇄]) |
| ③ 못 하는 것 | **채움 (원문 스스로 셋 + 말 없음 둘)** | 형상 (완전 구 부적절 · 옥수수 = 4 구 근사 '충분') · 입도 (단분산) · 속도 (33 배) = 원문 · 소성 · 파쇄 · 조밀 영역 = **말 없음** |
| `morrissey2013_…` L458 (2 차 인용) | **같음 (서지 연도 꼴만 다름)** | L458: *"Chung, Y.C. and Ooi, J.Y. (2007). … Particulate Science and Technology, 26(1): pp. 83–96, doi:10.1080/02726350701759381. (p. 94, 95, 152, 203) \| 구속 압축 DEM 매개변수 민감도 · 충전 의존 \| 없음 (`coetzee2017_*` 가 인용만)"* — 내용 요약은 원문과 맞다 · '(2007)' = 표지 인용 줄과 같고 인쇄 호는 2008 · ⚠ *"`coetzee2017_*` 가 인용만"* 은 정본 coetzee2017 카드로 확인되지 않는다 (그 카드의 Chung & Ooi [161] = 관입 시험 · 이 논문에 없음 → 다른 Chung & Ooi 논문으로 보인다 [카드 추론]) — **카드 문제로 보고 · 고치지 않음** |
| 위시 줄 *"litdb 확인: … (coetzee2017 · 이 카드가 언급만)"* | **일부** | morrissey2013 은 언급 맞음 · coetzee2017 은 위 행 (같은 꼴의 혼동) |

⇒ **의도 대조 결과: 일부** — '구속 압축 DEM 의 매개변수 민감도 · 충전 의존' · 'K0 정의 · 값' · '실험 대조 · 재료' 는 **채움**; '단계 6 · 질문 b (탈압 · 되돌아옴)' 는 **없음** (하중 제거 0); '단계 4' 는 **일부** (kPa · mm 탄성 입자 · 기공 없음).

---

## 1. 한 줄 요약

DEM 입력값이 흔히 재지 않고 가정된다는 문제에서 출발해 (*"In many DEM studies, the input parameters were often not measured and the values were sometimes assumed without any proper justification"* p.83), 저자들은 유리구슬 · 옥수수의 E · ν · μ · e 를 입자 수준에서 따로 재 (Table 1–2) PFC3D 로 계측 원통 (Ko 시험기 개조 · 바닥 하중계 + 벽 변형 게이지) 구속 압축을 그대로 풀고, 초기 충전 · 입자 강성 · 입자 간 마찰을 흔들어 바닥 힘 · K · μbulk 에 주는 영향을 본다 — 결론 넷 (p.95): 구는 초기 충전에 더 민감하다 (완전 구 = 부적절 표현) · 초기 충전은 실제를 본떠야 한다 · 입자 강성은 벌크 강성을 직접 바꾸지만 벽 하중 전달은 부차적이다 (몇 자릿수 낮춰도 *"huge computational advantage"*) · 입자 간 마찰은 옥수수에서만 벽 하중을 바꾼다 (강성 차이 때문).

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 서지 | Y. C. Chung · J. Y. Ooi, *Influence of Discrete Element Model Parameters on Bulk Behavior of a Granular Solid under Confined Compression*, Particulate Science and Technology **26** (1) 83–96 (2008) · DOI 10.1080/02726350701759381 (표지 인용 줄 = 2007 · 온라인 표지 날짜 2011-03-03) |
| 소속 | Nanya Institute of Technology (대만) · University of Edinburgh (영국 · Institute for Infrastructure and Environment) |
| 재료 | 유리구슬 (Sigmund Lindner · 제조사 값 = 지름 · 밀도 · ν) · 옥수수 낟알 (ν = ASAE 1996 값) |
| 방법 | 실험 (Ko 꼴 구속 압축 시험기 · Instron 1.5 mm/min · 바닥 하중계 · 벽 변형 게이지 로제트 4 개) + 3D DEM (PFC3D 3.0 · Itasca 2003) |
| 접촉 법칙 | Hertz-Mindlin no-slip (Tsuji et al. 1992) + 감쇠 + 접선 Coulomb 미끄럼 (p.85) — 점착 · 구름 저항 · 소성 없음 |
| 입자 | 유리 3,591 개 (단분산 Ø10 mm 구) · 옥수수 4,672 개 (겹친 구 4 개 집합체 · 반지름 3 · 3.345 mm [판독 그림 2]) |
| 영역 | 원통 Ø145 mm (실험과 같은 지름) · 시료 높이 실험 평균 185 mm (유리) · 141 mm (옥수수) · DEM 높이 [미확인] |
| 시간 적분 | 임계 시간 간격 × 0.20 (O'Sullivan & Bray 2004) · 값 [미확인] |
| 하중 | 위 판 변위 제어 DEM 50 mm/min (실험 1.5) · 위 하중 ≈800 N (유리) · ≈1000 N (옥수수) 까지 [판독 그림 8] |
| 산출 | 위 · 아래 판 힘 · 벽 접촉 힘 → K · μbulk (식 1–2 와 같은 정의) · 링 구간 벽 마찰 분포 (그림 10) |
| 계산 비용 | [미확인] — *"computationally very intensive"* (p.86) · *"huge computational advantage"* (p.95) 뿐 |
| 실험 반복 | 재료마다 Test 1–4 [판독 범례] |
| 시드 · 반복 런 | [미확인] (경우마다 런 하나로 보인다 [카드 추론]) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 실험 장치 · 시료 (p.84–85 · 그림 1 · Table 1–2)

- **장치** [인쇄 p.84]: *"modified from the Ko tester by Masroor et al. (1987) and is similar to the test apparatus proposed by the European Standard for measuring the lateral pressure ratio for silo design (EN 1991-4, 2004)"* · 위 판 = Instron · **1.5 mm/min** 일정 변위 속도 · 위 하중 · 위 변위 · 바닥 하중계 (F_B) · 벽 = **변형 게이지 로제트 4 개** (원주 등간격 · 원주 · 축 방향) (`txt_p84_p85_ko_tester_instron_1p5_mm_min_bottom_load_cell_rosettes.png`).
- **원통** [인쇄 p.85]: 지름 **145 mm** · 두께 **3.33 mm** · 높이 **380 mm** · 아크릴 (그림 1 표지 *"Acrylic cylinder (Wall thickness=3.33 mm)"*) · 벽 E_w · ν_w [미확인 — 이 논문에 없음 · Chung 2006].
- **시료** [인쇄 p.85]: 평균 높이 유리 **185 mm** · 옥수수 **141 mm** · 게이지 높이 = 시료 바닥에서 **94 mm** · **76 mm** · 원주 변화는 안 보고 게이지 4 개 평균 (*"As a first analysis"*) (`txt_p85_eq2_symbols_cylinder_145_3p33_380mm_beds_185_141_gauges_94_76.png`) · 그림 1 의 '140mm' = 아크릴 받침 윗면에서 게이지까지 (그림 안 글자 · 본문 94 · 76 mm 와 기준이 다르다 [카드 해석]).
- **채움** [인쇄 p.86]: 체를 **335 mm** 높이에 두고 낟알 · 구슬이 체를 지나 원통에 'rain' (떨어짐).
- **원통 지름 / 입경 = 14** [인쇄 p.90] (145/10 = 14.5 · 145/10.11 = 14.3 [카드 산술]) — 실험 산포의 원인: *"This is thought to be largely caused by the nature of these experiments, with the ratio of sample diameter to mean particle size of only 14. The natural variation in initial packing in the experiments gave rise to significant scatter in the bulk responses, particularly at the initial loading stages when the forces are small"* (p.90 · `txt_p90_corn_65pct_K_mu_product_K0p35_mu0p32_D_over_d_14.png`).
- **실험 결과 (본문 숫자 전부)** [인쇄]:
  - 유리: 바닥 힘이 위 하중에 선형 · **≈50 %** 가 바닥에 닿음 (p.87) · **K ≈ 0.4 · μbulk ≈ 0.35** (산포 있음 · p.88)
  - 옥수수: **65 %** (p.90) · 반복성 좋음 (Test 2 빼고) · **K ≈ 0.35 · μbulk ≈ 0.32** (*"at larger loads"* p.90)
  - 원문 설명: 옥수수 벽 마찰이 더 큰데도 바닥 몫이 더 큰 까닭 = *"the bottom load depends on the product K μbulk, rather than μbulk alone"* (p.90)
- **실험 시험 끝 (판독 · 눈으로 ±0.02)**: 유리 K Test 1 ≈0.48 · Test 2 ≈0.46 · Test 3 ≈0.30 · Test 4 ≈0.33 · μbulk ≈0.27 · 0.29 · 0.47 · 0.36 (그림 4–5 의 마지막 점 · 위 하중 ≈640–760 N) / 옥수수 (880 N) K Test 1 0.30 · Test 2 0.43 · Test 4 0.32 · Test 3 ≈0.36 · μbulk Test 1 · 3 · 4 ≈0.33 · Test 2 0.24 [판독 digitized.csv · 그림 7 · 12] · 최대 하중 유리 ≈710–760 N · 옥수수 ≈930 N [판독 · 눈으로].

### 3-2. DEM 설정 (p.85–87 · Table 1–2 · 그림 2)

- **코드 · 법칙** [인쇄 p.85–86]: PFC3D (Itasca 2003 = *"PFC3D—Particle Flow Code in Three Dimensions, Version 3.0"*) · soft contact · **Hertz-Mindlin no-slip** (Tsuji et al. 1992) + 감쇠 + 접선 마찰 미끄럼 · 감쇠 종류 · 값 [미확인] (`txt_p85_p86_hertz_mindlin_dt_0p20_3591_4672_monosize_four_spheres.png`).
- **시간 간격** [인쇄 p.85]: 계산된 임계 시간 간격 × **0.20** (*"chosen to achieve numerical stability without increasing computational cost (O'Sullivan & Bray, 2004)"*) · 임계 시간 간격 ∝ 1/√G (p.90).
- **입자 수** [인쇄 p.85]: 유리 **3,591** · 옥수수 **4,672** — *"The number of particles was calculated to produce a very close match with the physical experiments"* · **단분산** (*"Particle size variation was not considered"*).
- **옥수수 형상** [인쇄 p.85–86 · 판독 그림 2]: 겹친 구 4 개 (Favier et al. 1999; Itasca 2003) 로 주 · 중간 · 부 치수 10.11 · 9.11 · 6.69 mm 를 맞춤 · 반지름 3 mm (위 둘) · 3.345 mm (아래 둘) · 중심 간격 1.6 · 2.42 · 3.765 mm (그림 안 글자) · 4 개는 계산 비용 때문에 시작했고 *"sufficient to give satisfactory predictions"* 라 유지 (Chung 2006; Chung & Ooi 2006).
- **생성 · 정착** [인쇄 p.86 · `txt_p86_layers_1p50d_1p01d_2p56ms_settle_ke_1e-8_platen_50mm_min.png`]: 격자에 띄워 놓고 처음부터 'switched on' · 바닥부터 층으로 · 중심 간격 **1.50d** (유리) · **1.01d** (옥수수) (d = 주 치수) · 모두 초기 속도 **2.56 m/s** = 실험 낙하 높이 335 mm 에 해당 (√(2gh) = 2.564 m/s [카드 산술]) · 중력으로 떨어져 채움 · 정착 = 계 운동 에너지 **< 10⁻⁸ J** · 평균 불균형 힘 **< 10⁻⁶ N** (유리구슬 한 알 무게 **1.3 × 10⁻² N** · 옥수수 **4.2 × 10⁻³ N**) — 불균형 힘 / 한 알 무게 = 7.7 × 10⁻⁵ (유리) · 2.4 × 10⁻⁴ (옥수수) [카드 산술] · 유리 한 알 무게 = 2530 × 9.81 × (π/6)(0.01)³ = 1.30 × 10⁻² N 로 본문 값과 맞다 [카드 산술].
- **누름** [인쇄 p.86]: 채운 뒤 위 판을 **50 mm/min** (실험의 33.3 배 [카드 산술]) · 다른 하중 경우 (Chung 2006) 에서 속도를 올려도 *"not found to produce noticeable effect in the overall bulk loading response, but the higher rate may introduce a larger degree of local force fluctuations"* · 속도 효과 추가 연구 중.
- **입력 (Table 1–2 [인쇄] · `tab_1.png` · `tab_2.png`)**:

| 항목 | 유리구슬 (CoV %) | 옥수수 (CoV %) |
|---|---|---|
| 크기 (mm) | 지름 10 ± 0.5 (제조사) | 주 10.11 (8.2) · 중간 9.11 (4.9) · 부 6.69 (16.5) |
| 밀도 (kg/m³) | 2530 (제조사) | 1280 (1.1) |
| 영률 | 41 GPa (4.0) | 1660 MPa (31.0) |
| 포아송비 | 0.22 (제조사) | 0.40 (ASAE 1996 에서 채택) |
| 정지 마찰 (입자–아크릴) | 0.24 (6.4) | 0.34 (8.4) |
| 정지 마찰 (입자–입자) | 0.24 (CoV 칸 비움 · 본문 p.87 = 입자–면 값으로 가정) | 0.34 (같음) |
| 반발 계수 (입자–아크릴) | 0.79 (2.2) | 0.59 (7.5) |
| 반발 계수 (입자–입자) | 0.79 (같음) | 0.59 (같음) |
| 개수 | 3591 (0.4) | 4672 (6.3) |

- **측정법** [인쇄 p.87 · `txt_p86_p87_pfc3d_poisson_hertz_single_particle_tests_interparticle_assumed.png`]: E = **단입자 압축 + Hertz 접촉 가정** (옥수수는 접촉점의 두 직교 곡률을 레이저 스캐너로) · 입자–면 정지 마찰 = **세 입자 미끄럼 시험** · 반발 = **낙하 시험** (비구형은 회전을 포함한 궤적) · *"Individual particle-particle friction and restitution coefficient measurement has rarely been attempted before in irregularly shaped agricultural grains"* → 입자–입자 μ · e = 입자–면 값과 같다고 처음 가정.
- **전단 계수 (강성 연구의 G₀)** [카드 산술 · G = E/(2(1 + ν)) · ν 고정 가정]: 유리 G₀ **16.8 GPa** → 0.01G₀ 168 MPa → 0.0001G₀ **1.68 MPa** / 옥수수 G₀ **0.593 GPa** → 5.93 MPa → 0.0001G₀ **59.3 kPa** (옥수수 0.0001G₀ 의 G 가 최대 축 응력 ≈61 kPa 와 같은 크기 — §3-6).
- **마찰 연구 기준값** [인쇄 p.92]: 유리 μp 기준 **0.244** (×0.5 · 2.0 · 4.0) · 옥수수 **0.335** (반 · 두 배) — 표의 0.24 · 0.34 와 셋째 자리만 다름 (그림 10 범례도 0.24 · 0.34 · 그림 11–12 범례 0.244 · 0.335).

### 3-3. 초기 충전 (생성) 민감도 (그림 3–7 · p.87–90)

유리구슬 — 위 하중 780–785 N [판독 digitized.csv · 그림 3 · 4 · 5]:

| DEM 생성 | 바닥 힘 (N) · 몫 | K | μbulk |
|---|---|---|---|
| FCC packing | 585 · 0.75 | 0.51 | 0.111 |
| Rhombic packing | 670 · 0.85 | 0.34 | 0.091 |
| Random generation | 452 · 0.58 | 0.70 | 0.135 |
| 간격 1.01d | 578 · 0.74 | ≈0.66 (세 간격 한 선) | 0.080 |
| 간격 1.50d (기본) | 458 · 0.58 | ≈0.66 | 0.141 |
| 간격 2.00d | 436 · 0.56 | ≈0.66 | 0.154 |
| 실험 (본문) | ≈50 % | ≈0.4 | ≈0.35 |

- 원문 해석 [인쇄 p.87–89]: Random 이 실험 바닥 힘과 *"very well"* · FCC · Rhombic (매우 조밀) 은 *"much larger force"* → 체 낙하가 *"quite random"* 충전을 만들었을 것 · 1.50d · 2.00d 는 맞고 *"almost touching"* 1.01d 는 크다 · 충분히 띄우면 무작위 충전이 된다 · K 는 Rhombic 최소 · Random 최대 (*"not surprising since the lateral pressure ratio K is a bulk property that relates to the propensity for lateral expansion and has been shown to relate well to the Poisson's ratio of the bulk material"*) · 간격은 K · μbulk 에 영향 없음 — 1.01d 만 벽 마찰이 작게 동원되어 바닥 힘이 큼 (`txt_p87_p88_bottom_50pct_random_matches_fcc_rhombic_1p01d_larger.png` · `txt_p89_K_rhombic_smallest_random_largest_bulk_poisson_1p01d.png`).
- ⚠ **원문이 숫자로 말하지 않은 것** [판독]: 바닥 힘이 맞는 Random · 1.50d · 2.00d 도 **K 는 실험의 ≈1.6–1.75 배 (0.66–0.70 ↔ ≈0.4), μbulk 는 ≈0.4 배 (0.135–0.154 ↔ ≈0.35)** — 둘이 서로를 상쇄해 바닥 몫이 맞은 것으로 보인다 (K·μbulk 0.092–0.101 ↔ 실험 0.14 · §3-6 Janssen 대조) [카드 해석].  원문의 요약: *"the DEM simulations produced a reasonable agreement with the experiments for the corn grains but not for the glass beads … It is not totally clear why spherical assemblies produced poorer match with experiments"* (p.90 · `txt_p90_summary_corn_agree_glass_not_spheres_packing_sensitive.png`).

옥수수 — [판독 digitized.csv · 그림 6 · 7]:

| DEM 생성 | 바닥 힘 (950 N) · 몫 | K (880 N) | μbulk (880 N) |
|---|---|---|---|
| 간격 1.01d (기본) | 606 · 0.64 | 0.36 | ≈0.27 |
| 간격 1.50d | 521 · 0.55 | 0.40 | 0.29 |
| 간격 2.00d | 539 · 0.57 | ≈0.43 (Test 2 와 겹침) | ≈0.27 |
| 실험 | 900 N 에서 612 (Test 1 · 2 · 4) · 573 (Test 3) = 0.68 · 0.64 · 본문 65 % | Test 0.30–0.43 · 본문 ≈0.35 | Test 0.24–0.33 · 본문 ≈0.32 |

- 원문 [인쇄 p.90]: 세 간격 모두 *"reasonable match"* · 1.01d 가 *"best match"* → *"nonspherical particles may be less sensitive to particle generation schemes"* · 간격은 K 에 *"some noticeable influence"* · μbulk 에 *"negligible influence"*.

### 3-4. ★ 입자 강성 민감도 (그림 8–10 · p.90–92)

- **목적** [인쇄 p.90]: *"Particle stiffness is sometimes reduced in DEM simulations to reduce computational time, since the critical time step is inversely proportional to √G (G is the particle shear modulus). For some classes of problems, particle stiffness may not have a significant influence on the prediction and may therefore be reduced to gain computational advantage."* → 잰 G₀ 를 0.01G₀ · 0.0001G₀ 로 (`txt_p90_p91_stiffness_reduced_dt_sqrtG_0p01_0p0001_bulk_stiffness_direct.png`).
- **하중–변위 (그림 8 · 싣기만)** [판독 digitized.csv]:

| 재료 · 강성 | 변위 at 790 N (유리) / 950 N (옥수수) | 하중이 일어서는 곳 | 접촉 뒤 압축 · 변형률 [카드 산술] |
|---|---|---|---|
| 유리 G₀ | 7.27 mm | 5.5 mm 에서 10.8 N · 6.5 mm 에서 34 N | ≈2.3 mm · ≈1.2 % |
| 유리 0.01G₀ | 10.25 mm | (같은 곳) | ≈5.3 mm · ≈2.8 % |
| 유리 0.0001G₀ | 36.83 mm (600 N 32.54 · 20 mm 190 N · 35 mm 710 N) | | ≈31.8 mm · ≈17 % |
| 옥수수 G₀ | 7.77 mm (900 N 7.77) | 5.0 mm 에서 16.6 N · 6.0 mm 에서 36 N | ≈3.3 mm · ≈2.3 % |
| 옥수수 0.01G₀ | 17.86 mm (900 N 17.61) | | ≈13.4 mm · ≈9.5 % |
| 옥수수 0.0001G₀ | 77.86 mm (900 N 76.12 · 100 N 29.0) | | ≈73.4 mm · ≈52 % |

  ⚠ 변위 영점 [미확인] — 곡선이 유리 ≈5 mm · 옥수수 ≈4.5 mm 에서 일어서므로 판이 시료 위에서 출발했다고 보고 그 값을 빼서 '접촉 뒤 압축' 을 냈다 (±1 mm) · 변형률 분모 = 실험 평균 높이 185 · 141 mm (DEM 높이 [미확인]) [카드 산술 · 가정].
- **원문 결론** [인쇄 p.91]: *"As expected, the bulk stiffness in confined compression was directly influenced by the particle stiffness. The relationships between bulk stiffness and particle stiffness have been derived from these results (Chung, 2006)."* — 관계식 [미확인 — 학위논문].
- **[카드 산술 · 어림] 강성 배수 ↔ 변위 배수**: 순수 Hertz 겹침이 압축을 다 맡는다면 G 를 1/100 · 1/10⁴ 로 하면 겹침은 100^(2/3) = **21.5** · 10⁴^(2/3) = **464** 배 — 판독 '접촉 뒤 압축' 비는 유리 2.3 · 14 · 옥수수 4.1 · 22 배 (G₀ 기준) 로 훨씬 작다 ⇒ **G₀ 에서의 압축은 대부분 접촉 겹침이 아니다** (재배열 · 판 밑 정착 [카드 해석]).  어림: 유리 G₀ 접촉력 ≈ σd² = 48 kPa × (10 mm)² ≈ 4.8 N → Hertz 겹침 ≈ **2.2 µm** (δ/d 2.2 × 10⁻⁴) × 높이 18.5 d ≈ **0.04 mm** (관측 ≈2.3 mm 의 ≈2 %) · 0.0001G₀ → ≈**1.0 mm** (δ/d ≈0.10) × 18.5 ≈ 19 mm (관측 ≈32 mm 의 ≈60 %) / 옥수수 0.0001G₀ → δ ≈ **11 mm ≈ d** (Hertz 유효 범위 밖) [카드 산술 · 어림 · 접촉력 = σd² · 한 기둥 · R* 2.5 mm (유리) · 1.6 mm (옥수수) 가정 · 원문에 겹침 값 없음 [미확인]].
- **바닥 힘 (그림 9)** [판독]: 유리 600 N 에서 G₀ **444 N (0.74)** · 0.01G₀ **371 (0.62)** · 0.0001G₀ **342 (0.57)** · 770 N 에서 0.01G₀ 470 (0.61) · 0.0001G₀ 446 (0.58) / 옥수수 900 N 에서 G₀ ≈ 0.01G₀ **572 (0.64)** · 0.0001G₀ **624 (0.69)** — 원문 [인쇄 p.91]: *"While particle stiffness directly influences the bulk stiffness of the system, these results show that it has much less influence on the force transmission onto the boundary surfaces. Especially for corn, reducing stiffness by 100 times produced no noticeable effect on the force transmission. For glass beads, reducing particle stiffness did cause a reduction in the force transmitted to the bottom platen"*.
- **벽 마찰 높이 분포 (그림 10 · 유리 800 N · 옥수수 900 N)** [판독 · 마커 중심 · 20 mm 간격]:
  - 유리 G₀: 0.084 · 0.011 · 0.052 · 0.083 · 0.075 · 0.046 · 0.090 · 0.113 · 0.140 (높이 10 → 170 mm · 평균 **0.077**) · 0.01G₀: 0.059 · 0.056 · 0.149 · 0.169 · 0.176 · 0.183 · 0.174 · 0.175 · 0.207 (평균 **0.150**) · 0.0001G₀: 0.131 · 0.198 · 0.232 · 0.228 · 0.231 · 0.233 · 0.225 · 0.220 (10 → 150 mm · 평균 **0.212**) ↔ 입력 0.24 (점선 0.244 [판독])
  - 옥수수 G₀: 0.240 · 0.288 · 0.293 · — · 0.289 · 0.301 · 0.233 · 0.258 (70 mm 는 다른 계열과 겹침 · 7 점 평균 **0.272**) · 0.01G₀: 0.314 · 0.328 · 0.326 · 0.332 · 0.332 · 0.324 (30 → 150 mm · 10 · 70 mm 겹침 · 평균 **0.326**) · 0.0001G₀ ≈0.31–0.33 (마커 네 개 · 10 → 70 mm [판독 · 눈으로]) ↔ 입력 0.34 (점선 0.335 [판독])
  - 원문 [인쇄 p.92]: *"reducing the particle stiffness generates a larger slip displacement under load, further mobilizing the wall friction. This is particularly true for glass beads, which at the full stiffness Go did not generate sufficient slip displacement to mobilize the limiting wall friction. The increasing wall friction as particle stiffness reduces is the reason the bottom load decreases in Figure 9(a)."* (`txt_p92_wall_segments_8_15_slip_mobilises_wall_friction_glass_G0.png`)
  - 0.0001G₀ 의 점이 적은 것 (유리 8 · 옥수수 4) = 압축이 커서 시료가 낮아진 것과 맞다 (유리 ≈32 mm · 옥수수 ≈73 mm 압축) [카드 해석].

### 3-5. 입자 간 마찰 민감도 (그림 11–12 · p.92–94)

- **유리** [판독 그림 11a · 인쇄 p.93]: μp 0.122 · 0.244 · 0.488 · 0.976 네 선이 780 N 에서 **425–451 N (0.54–0.58)** 두 띠 안 — *"the bottom contact force remained essentially the same for the range of interparticle frictions studied (μp = 0.12–0.98) and agreed well with the experiments"* · *"the glass beads displayed more sudden unloadings especially for higher interparticle friction"* (싣는 중 힘 급락 · 실험엔 없음 · 원문 추정 원인 = 속도 50 vs 1.5 mm/min).
- **옥수수** [판독 그림 11b · 12 · 인쇄 p.93–94]: 바닥 힘 μp 0.168 → 950 N 에서 **514 N (0.54)** · 985 N 535 N ↔ μp 0.335 · 0.670 · 실험 ≈608 N at 900 N (0.68) · K (880 N) **0.47 · 0.36 · 0.27** (μp 0.168 · 0.335 · 0.670) · μbulk 0.28 · 0.27 · 0.29 (벽 마찰 고정이라 그대로) — 기전 (원문): *"reducing the interparticle friction has allowed more of the particle contacts to reach limiting friction, resulting in larger lateral forces under loading and therefore a larger K value. The larger lateral forces gave rise to a large frictional traction being generated on the cylindrical walls, resulting in a smaller force on the bottom platen"* · 유리에서 안 생긴 까닭 = *"being over 20 times stiffer than the corn grains, there were insufficient interparticle slip displacements to mobilize the contact friction in the majority of the contacts"* (E 비 41 / 1.66 = 24.7 [카드 산술]) (`txt_p93_p94_corn_K_rises_friction_halved_glass_20x_stiffer.png`).

### 3-6. ★ 카드 산술 묶음 (원문에 없는 수 · 식과 가정 병기)

- **응력 크기**: 원통 단면 A = π/4 × (0.145 m)² = 0.016513 m² → 790 N **47.8 kPa** · 800 N **48.4 kPa** · 900 N **54.5 kPa** · 950 N **57.5 kPa** · 1000 N **60.6 kPa** (위 하중 ÷ A · 벽 마찰로 아래로 갈수록 작아짐) · 우리 300 MPa ÷ 48.4 kPa = **≈6.2 × 10³**.
- **초기 기공률 어림** (DEM 이 실험 평균 높이까지 찼다고 가정 · 원문에 기공 · 밀도 값 없음): 유리 3591 × (π/6)(10 mm)³ = 1.880 × 10⁶ mm³ ÷ (16,513 mm² × 185 mm) = **고체 분율 0.615 · 기공률 38.5 %** · 겉보기 밀도 1557 kg/m³ / 옥수수 한 알 부피 = 무게 ÷ (ρg) = 4.2 × 10⁻³ ÷ (1280 × 9.81) = 334.5 mm³ (같은 부피 구 지름 8.61 mm) → 4672 알 ÷ (16,513 × 141 mm³) = **고체 분율 0.671 · 기공률 32.9 %** · 겉보기 밀도 859 kg/m³ — 가정 셋 (높이 = 실험 평균 · 유리 지름 = 명목 10 mm · 옥수수 부피 = 무게 환산) 에 묶인 어림.
- **Janssen 대조 (위 하중만 · 자기 무게 무시 · K · μbulk 높이 균일)**: F_B/F_T = exp(−4 K μbulk h / D)
  - 실험 유리 (K 0.4 · μ 0.35 · h/D = 185/145): **0.49** (본문 ≈50 %) · 실험 옥수수 (0.35 · 0.32 · 141/145): **0.65** (본문 65 %) — 본문 숫자 셋이 서로 맞는다
  - DEM 유리 (판독 K · μbulk): FCC 0.748 (판독 바닥 몫 0.745) · Rhombic 0.854 (0.854) · Random 0.619 (0.576) · 1.01d 0.765 (0.736) · 1.50d 0.624 (0.584) · 2.00d 0.597 (0.555) — 결정 충전 둘은 0.003 안 · 나머지는 4–8 % 높다 (DEM K 를 어느 높이 벽 힘으로 냈는지 [미확인]) ⇒ 원문의 *"the bottom load depends on the product K μbulk"* 를 수로 확인 + 판독값의 자기 일치 점검.
- **σ/E (최대 축 응력 ÷ 입자 영률 · ν 고정이라 E 도 G 와 같은 배수)**: 유리 G₀ **1.2 × 10⁻⁶** · 0.01G₀ 1.2 × 10⁻⁴ · 0.0001G₀ **0.012** / 옥수수 G₀ 3.6 × 10⁻⁵ · 0.01G₀ 3.6 × 10⁻³ · 0.0001G₀ **0.36** ↔ [우리] DEM 300 MPa ÷ E_eff 1.35 GPa = **0.22** · MPM ÷ 1.53 GPa = 0.20 — 우리 연화 DEM 의 무른 정도는 이 논문의 **옥수수 0.0001G₀ 와 같은 자릿수** (같은 양 아님 · 접촉 법칙 · 응력 · 입경 모두 다름).
- **K ↔ 포아송비** (원문 *"relate well to the Poisson's ratio of the bulk material"* 을 측방 변형 0 탄성 K₀ = ν/(1 − ν) 로 읽으면): 실험 K 0.4 · 0.35 → 벌크 ν **0.29 · 0.26** · 입자 ν 0.22 · 0.40 을 넣으면 K 0.28 · 0.67 — 실험 · DEM K 와 맞지 않는다 ⇒ **K 는 입자 포아송비가 아니라 충전 · 마찰에서 나오는 벌크 성질** [카드 해석] · [우리] MPM ν_SE 0.49 → 0.96 (탄성 연속체면 거의 정수압).

### 3-7. 원문 안 어긋남 (고치지 않고 적는다 · `figures.json` note_manual)

1. **벽 구간 수 · 높이**: 본문 *"A total of 8 and 15 ring segments were used for the glass beads and corn grains respectively. These equate to a segment height of 37.5 mm for glass beads and 20 mm for corn grains"* (p.92) ↔ 그림 10a 유리 점은 **10 · 30 · … · 170 mm (20 mm 간격 · 9 점)** [판독 — 마커 중심 10.4 · 31.0 · 48.4 · 69.7 · 90.1 · 109.3 · 129.1 · 149.7 · 170.2 mm] · 8 × 37.5 = 15 × 20 = 300 mm (벽 300 mm 를 나눈 수로 보인다 [카드 추론]).
2. **강성 연구의 유리구슬 생성이 원문에 없다 · 그림은 1.01d 로 읽힌다**: 그림 9a 의 G₀ 곡선이 그림 3b 의 *"Particle spacing 1.01d"* 곡선과 겹친다 (350 N 262 ↔ 263 N · 450 N 335 ↔ 336 · 550 N 411 ↔ 414 (고리의 아래 가지)) · 그림 10a G₀ 벽 마찰 평균 0.077 ≈ 그림 5b 1.01d 0.080 (1.50d 0.141) [판독 대조] ↔ 본문의 유리 기본 생성 = 1.50d (p.86) ⇒ 강성 연구 (그림 8–10) 의 유리 G₀ 는 1.01d 생성 런으로 보인다 [카드 추론] — '강성을 낮추면 바닥 힘이 준다' (그림 9a) 의 출발점이 **벽 마찰이 덜 동원된 1.01d 충전** 이라는 뜻.
3. 본문 *"Bout & McPherson (2002)"* (p.86 · p.87) ↔ 참고문헌 *"Boutt, D. & B. McPherson. 2002"* (p.95).
4. 마찰 기준 표 0.24 · 0.34 ↔ 본문 · 그림 11–12 범례 0.244 · 0.335 (그림 10 범례 0.24 · 0.34).
5. 그림 2 부제 *"Four-sphere corn representation from EDEM graphics (DEM Solutions, Edinburgh)"* ↔ 계산은 PFC3D (p.86) — 그림만 EDEM 으로 그렸다고 읽힌다 [카드 해석].
6. 표지 인용 줄 '(2007)' ↔ 인쇄 머리 '2008'.
7. 본문 p.92 *"were adopted as the interparticle friction coefficients μp in the DEM simulations for corn grains and glass beads respectively"* — 'respectively' 순서가 표 (1 = 유리 · 2 = 옥수수) 와 반대 (뜻은 같음).

---

## 4. ★ 방법 — 측정 사슬 · DEM · 입자 처리

### 4-1. 측정 사슬 (식 1–2 · p.85 · `eq_01_K_mu_bulk_definitions.png` · `eq_02_sigmaV_sigmaH_tau_from_platen_loads_wall_strains.png`)

- 식 (1): **K = σH / σ̄V** · **μBulk = τ̄ / σH**
- 식 (2): **σ̄V = 2(F_T + F_B) / [πD²(1 + ε_θ)²]** · **σH = 2tE_w(ε_θ + ν_w ε_a) / [D(1 − ν_w²)]** · **τ̄ = (F_T − F_B) / [πDh(1 − ε̄_V)]**
- 기호 (p.85): D · t · E_w · ν_w = 원통 지름 · 두께 · 영률 · 포아송비 · ε_θ · ε_a = 게이지 높이의 평균 원주 · 축 변형 · F_T · F_B = 위 · 아래 판 하중 · ε̄_V = 평균 수직 변형 · h = 시료 높이.
- 뜻 [카드 해석]: σ̄V = 위 · 아래 판 힘의 평균 ÷ (원주 변형으로 넓어진) 단면 · σH = 얇은 벽 원통의 원주 응력 σ_θ = E_w(ε_θ + ν_w ε_a)/(1 − ν_w²) 와 σ_θ = pD/(2t) 의 평형에서 낸 벽 압력 · τ̄ = (F_T − F_B) ÷ 압축으로 줄어든 벽 접촉 면적 = 벽이 진 평균 전단.  원문 스스로 *"approximately evaluated"* — 수직 응력은 판 힘 평균 · 수평 응력은 한 높이 (게이지) 값 (*"It should be noted that the evaluation of lateral pressure ratio K and mobilized bulk wall friction μbulk is only approximate here …"* p.88 · `txt_p88_p89_glass_K_0p4_mu_0p35_approximate_gauge_vs_boundary.png`).
- DEM 쪽 같은 양 = *"from boundary forces in the DEM simulations"* (p.89) · 그림 10 의 높이 분포 = 벽을 링 구간으로 나눠 구간마다 입자–벽 접촉의 법선 · 수직 전단 힘을 더하고 구간 면적으로 나눈 값의 비 (p.92).

### 4-2. DEM 의 빈칸 (원문에 없는 것)

감쇠 종류 · 값 · 시간 간격 값 · 벽 (아크릴) 강성 · 벽–입자 μ · e 의 DEM 입력 (표의 입자–아크릴 값으로 보인다 [카드 추론]) · 시료 높이 · 정착 뒤 기공 · 배위수 · 판 출발 위치 · 계산 시간 · 시드 · 반복 런 — 전부 [미확인].

### 4-3. ★ 입자 처리 (우리 축 언어로)

- **구 ↔ 형상**: 유리 = 완전 구 (단분산) · 옥수수 = 겹친 구 4 개 (강체 집합체 · 형상 변하지 않음).
- **입도**: 단분산 (둘 다) — 실험의 작은 크기 차이는 무시 (p.94–95).
- **접촉 소성 ↔ 형상 소성**: **둘 다 없다** — 탄성 Hertz-Mindlin (겹침 δ 로 힘을 내는 강체 입자) · 점착 · 파쇄 · 구름 저항 없음.  강성 감소 런의 큰 겹침 (옥수수 0.0001G₀ 는 겹침이 입자 크기 수준 [카드 산술 §3-4]) 은 **수치 감도 시험** 이지 물리 상태가 아니다 [카드 해석].
- **소성의 대리**: 없다 — 응력이 kPa 라 소성이 필요 없는 영역 (원문은 소성을 말하지 않는다).

### 4-4. 이 묶음의 네 질문 (i)–(iv)

- **(i) DEM 한계 문장** [인쇄]: ① *"One explanation is that the DEM model of perfect spheres with perfect symmetry, which have a tendency to form crystalline structure and a tendency to spin more than nonspherical particles, is not an appropriate representation even for the uniform glass beads with their slight natural imperfections. This cast doubt on many of the DEM studies in the literature based on perfect spheres."* (p.95) ② *"It is not totally clear why spherical assemblies produced poorer match with experiments."* (p.90) ③ *"In many DEM studies, the input parameters were often not measured and the values were sometimes assumed without any proper justification."* (p.83) ④ *"While the DEM software has the capability to simulate the filling procedure used in this study, i.e., raining through a sieve, the computational effort would be large and impractical to conduct."* (p.86) ⑤ *"The DEM simulations in this study assumed monodispersed particles although small particle size variation did exist in the physical experiments."* (p.94) ⑥ 속도: *"the simulations were performed using a significantly higher displacement rate than the experimental rate to make the computational effort manageable"* (p.86) — 겹침 상한 · 상대밀도 · 접촉 독립 가정 = **말 없음**.
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용**: **다루지 않음** · 강성을 낮추는 것은 계산 시간 때문 (임계 시간 간격 ∝ 1/√G · p.90) · 우회 = 없음 · 비용 [미확인].
- **(iii) 2D ↔ 3D**: 3D (PFC3D) · 2D 는 *"Bout and McPherson (2002) performed 2-D discrete element simulations and compared different methods of particle deposition … different packings may cause very different behaviors albeit with identical contact parameters"* (p.87) 를 충전 민감도의 근거로만 — 2D → 3D 전이에 대한 말 없음.
- **(iv) 압력을 뺄 때**: **다루지 않음** (§0-1).

### 4-5. 기법 미니 용어집

- **측압비 K (lateral pressure ratio)** = 수평 / 수직 응력비 (사일로 설계 · EN 1991-4) · 측방 변형 0 이면 **K₀ (정지 토압 계수)** · Ko 시험기 = K₀ 를 재는 구속 원통.
- **동원 벽 마찰 μbulk (mobilized bulk wall friction)** = 벽 전단 / 벽 수직 응력 — 미끄럼이 충분하면 입자–벽 마찰 계수에 닿고, 모자라면 그보다 작다.
- **Janssen 꼴** = 벽 마찰이 깊이에 따라 수직 응력을 덜어 내는 고전 해 (위 하중만이면 바닥 몫 = exp(−4Kμh/D)) — 원문은 이 식을 쓰지 않는다 (§3-6 의 대조는 이 카드의 산술).
- **Hertz-Mindlin no-slip** = 법선 Hertz + 미끄럼 없는 Mindlin 접선 강성 + Coulomb 한계 (Tsuji et al. 1992).
- **임계 시간 간격** = 명시적 적분이 안정한 최대 간격 · ∝ √(m/k) → 강성을 1/10⁴ 로 하면 100 배 긴 간격.
- **겹친 구 집합체 (clump · multi-sphere)** = 구 여러 개를 강체로 묶어 비구형을 근사.
- **'switched on' 생성** = 격자 위치에 미리 만들어 두고 한 번에 움직이게 함 (이송 · 낙하 모사 대신).
- **평균 불균형 힘 (mean unbalanced force)** = 입자에 걸린 알짜 힘의 평균 — 정적 평형 판정 (PFC 관례).
- **sudden unloading** = 이 논문에서는 **싣는 동안의 힘 급락** (stick-slip 꼴 [카드 해석]) — 하중 제거 (unloading) 가 아니다.

---

## 5. Figure set ★

| 그림 | 무엇을 보이나 | 우리가 쓸 것 |
|---|---|---|
| Fig. 1 | 장치 (위 판 · 바닥 하중계 · 벽 게이지 4 개 · Ø145 × 380 mm · 벽 3.33 mm) | 구속 압축의 경계 관측량 (위 · 아래 판 힘 · 벽 압력) 을 한 장으로 설명할 때 |
| Fig. 2 | 옥수수 겹친 구 4 개 (치수) | 형상 근사의 예 (변형 없음) |
| Fig. 3 (`Fig. 3a` · `Fig. 3b`) | 유리 바닥 힘 vs 위 하중 — 충전 구조 · 생성 간격 | 출발 상태 민감도 (§3-3) · 1.01d 곡선 = 그림 9a G₀ 와 겹침 (§3-7) |
| Fig. 4 (`Fig. 4a` · `Fig. 4b`) | 유리 충전 구조별 K · μbulk | K 가 충전 구조에 민감 (0.34–0.70) |
| Fig. 5 (`Fig. 5a` · `Fig. 5b`) | 유리 생성 간격별 K · μbulk | K 둔감 · μbulk 1.01d 만 작음 |
| Fig. 6 | 옥수수 바닥 힘 — 생성 간격 | 비구형은 덜 민감 · 1.01d 최선 |
| Fig. 7 (`Fig. 7a` · `Fig. 7b`) | 옥수수 K · μbulk — 생성 간격 | DEM ↔ 실험 일치 범위 |
| Fig. 8 (`Fig. 8a` · `Fig. 8b`) | ★ 강성 셋의 하중–변위 (싣기만) | 벌크 강성 = 입자 강성 '직접' (§3-4) |
| Fig. 9 (`Fig. 9a` · `Fig. 9b`) | 강성 셋의 바닥 힘 | 경계 힘 전달 = '부차' |
| Fig. 10 (`Fig. 10a` · `Fig. 10b`) | 강성 셋의 벽 마찰 높이 분포 (800 · 900 N) | 미끄럼 → 벽 마찰 동원 · ⚠ 점 간격 20 mm (§3-7) |
| Fig. 11 (`Fig. 11a` · `Fig. 11b`) | 마찰별 바닥 힘 | 유리 둔감 · 옥수수 μp 반이면 감소 |
| Fig. 12 (`Fig. 12a` · `Fig. 12b`) | 옥수수 마찰별 K · μbulk | 마찰 ↓ → K ↑ 기전 |
| Table 1–2 | 입력값 (CoV) | 직접 측정 입력 표의 꼴 (값 · 변동 · 출처 · 가정 표시) |

---

## 6. Post-processing ★

- 원문: 위 · 아래 판 힘 → σ̄V · τ̄ (식 2) · 벽 게이지 (실험) / 벽 경계 힘 (DEM) → σH · K · μbulk (식 1) · 벽 링 구간 합 → μbulk(높이) (그림 10) · 하중–변위 (그림 8) · 모든 그림 = 위 하중 축 (응력 환산 없음 · 기공 · 밀도 · 배위수 · 힘 사슬 · 접촉 수 없음).
- 이 카드의 판독 (`digitized.csv` · 118 행): 원 래스터 (300 dpi · 회색조) 패널을 그림 영역 테두리선으로 눈금 맞춤 (Excel 그림 영역 = 인쇄 축 끝값 · 눈금 표시 대조 ≤ 범위의 0.4 % — 예: 200 · 400 · 600 눈금 199.8 · 400.3 · 599.5 · 0.7 눈금 0.701 · 그림 10 입력 점선 0.244 · 0.335 = 본문 기준 마찰과 같음) · 지정 x 의 세로 단면 (또는 지정 하중의 가로 단면) 에서 회색 < 215 인 런의 중심 · 계열 = 선 농도 (검정 실선 · 회색 파선 · 옅은 점선) 와 모양 · 그림 10 = 마커 중심 (20 mm 간격 확인) — 방법 · 메모는 행마다.
- 카드 산술 (§3-6): 응력 환산 · 기공 어림 · Janssen · σ/E · Hertz 겹침 어림 · K ↔ ν — 식과 가정은 본문에.

---

## 7. 우리 DEM+MPM 대비 (우리 값 = CLAUDE.md 출처 · `comparison_vs_ours_DEM.md` A · F 절 2026-11-17 줄)

| 축 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 입자 강성의 지위 | 잰 값 (G₀) 이 기준 · 낮춘 값은 계산 시간 · 감도용 | DEM E_eff 1.35 GPa = 실재 E (≈22–24 GPa) 의 18 배 연화 · **300 MPa 기공에 맞춘 보정 손잡이** (frame [2]) · MPM 1.53 GPa (전단 연화 · ν 0.49) | **목적이 반대** — 이 논문은 '강성을 낮춰도 경계 힘은 덜 바뀐다' 를 보이려 했고, 원문이 '직접 바뀐다' 고 한 벌크 강성 (압축 변위) 이 바로 우리가 연화로 맞추는 양 [카드 해석] ⇒ 우리 연화를 '계산 편의 · 무해' 라고 이 논문으로 정당화하면 안 된다 |
| 무른 정도 σ/E | 유리 1.2 × 10⁻⁶ → 0.012 · 옥수수 3.6 × 10⁻⁵ → 0.36 | DEM 0.22 · MPM 0.20 [카드 산술] | 우리 DEM 은 이 논문의 **가장 무른 옥수수 런** 과 같은 자릿수 — 그 런은 '경계 힘 전달 거의 그대로 · 압축 ≈52 %' [판독 · 카드 산술] · 응력 · 입경 · 법칙이 달라 숫자 비교는 안 함 |
| 겹침 | 원문 값 없음 · 어림 유리 G₀ δ/d ≈2 × 10⁻⁴ · 0.0001G₀ ≈0.10 · 옥수수 0.0001G₀ ≈1 | 순수 SE @1.35 GPa ⟨δ⟩ ≈ 지름의 11 % (CLAUDE.md 06-06 절) | 같은 자릿수 (유리 0.0001G₀) [카드 산술 · 어림 · 같은 양 아님] |
| 접촉 법칙 | Hertz-Mindlin 탄성 · 점착 · 소성 없음 | hooke/hysteresis (접촉 이력 소성 대리) · Stage-E 면적 보정 · 믹서는 SJKR 점착 | 우리는 접촉 소성 대리가 있다 · 형상 소성은 둘 다 없음 |
| 출발 상태 | 격자 'switched on' + 2.56 m/s 낙하 · 간격 1.01 · 1.50 · 2.00 d · 결정 충전 비교 · 정착 = KE < 10⁻⁸ J · 불균형 힘 < 10⁻⁶ N | LIGGGHTS 넣기 (insert) + 정착 (settling) 단계 → 판 압축 (CLAUDE.md 재개 체크리스트의 단계 이름) | 우리 PSD (다분산) 는 결정화 위험이 작다 · **생성 간격 · 방법 민감도는 우리가 재지 않은 축** [카드 해석] |
| 경계 관측량 | 바닥 판 힘 · 벽 압력 (K) · 벽 마찰 동원 (μbulk) · 높이 분포 | 판 반력 (wallP) · 주기 경계가 많아 벽 압력 · K 를 보고하지 않는다 [카드 해석] | K · μbulk 는 **우리가 안 낸 관측량** — 벽이 있는 침대면 낼 수 있다 (§8) |
| 하중 범위 | ≤ ≈61 kPa | 300 MPa (Heckel P_y 138 MPa) | 6,200 배 · 다른 영역 |
| 탈압 | 없음 | 언로딩 키트 (ULR1 · G2c′ 진행 중) | 이 논문은 빈칸 |
| 순수 SE 기공 · 랩 표준 (10–13 % · 1.64 g/cm³) | 없음 (유리 초기 기공 어림 38.5 % [카드 산술] 은 랩 표준과 다른 축) | — | 나란히 놓을 값 없음 |
| frame[5] | DEM 반쪽 (충전 · 힘 전달 · 벽 하중) 만 · 소성 · 형상 반쪽 없음 | DEM = 수송 · 충전 · MPM = 소성 · 형상 | 이 논문은 DEM 반쪽의 **보정 · 검증 방법론** 을 준다 |

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

| 계획 이름 | 이 논문이 주는 것 | 못 주는 것 |
|---|---|---|
| 단계 0 (관측량 · 판정 기준) | ① **정착 판정 꼴** = 운동 에너지 + **평균 불균형 힘 ÷ 한 알 무게** (원문 10⁻⁶ N ÷ 1.3 × 10⁻² N = 7.7 × 10⁻⁵ [카드 산술]) — 우리 정착 · 판 정지 판정에 '힘 비' 문턱을 결과 전에 적는 근거 ② **경계 관측량 정의** — K = σH/σ̄V (σ̄V = 위 · 아래 판 평균) · μbulk = τ̄/σH · 벽 링 구간 합 (원문 = '근사' 라고 스스로 표시) → 벽이 있는 침대에서 벽 압력 · 벽 마찰을 등록 칸으로 | 기공 연산자 · 판정 숫자 (기공 · 밀도 값 0) |
| 단계 1 (3D 메모리 · 장 수) | 없음 | — |
| 단계 2 · 3 (2D MPM · 접촉 표현) | 없음 (DEM 만) | — |
| 단계 4 (순수 SE 붓고 누르기) | ★ **출발 상태 만들기** — ① 격자 생성 후 'switched on' + 낙하 높이 속도 · ② 간격이 너무 좁으면 (1.01d) 벽 마찰 동원 · 바닥 힘이 달라진다 · ③ 단분산 구는 결정 충전 (FCC · Rhombic) 을 만들어 K · 바닥 힘을 바꾼다 — 등록 전 '생성 간격 두 개 이상 + 결정화 검사' 를 감도 팔로 [카드 해석] ④ 체 낙하 모사는 비싸다 (원문) — 대신 감도로 막는다 | 300 MPa · 항복 · 기공 맞춤 (kPa · 탄성) |
| 단계 5 (복합 압축) | 없음 (단일 재료 · 두 상 혼합 없음) | AM 하중 몫 · 재밍 |
| 단계 6 (탈압 · 되돌아옴) | 없음 — 단 *"sudden unloadings"* (싣는 중 힘 급락 · 마찰 클수록 · 빠른 판 속도) 는 우리 하중 곡선 · 언로딩 곡선 판독에서 **속도 인공물로 먼저 의심할 꼴** [카드 해석] | 하중 제거 곡선 · 잔류 K |
| 단계 7 (형상 · 피복 · 수송) | 없음 | — |
| 후보 D0 (지금 DEM) | ★ ① 강성 감소의 두 얼굴 — 벌크 강성 (압축) '직접' · 경계 힘 '부차' (kPa · 탄성 · 원문 p.91 · p.95) → 우리 18 배 연화는 '직접' 쪽 (기공) 에 맞춘 보정값이라 **물성으로 읽지 않는다** 를 뒷받침 ② 무른 입자일수록 미끄럼 ↑ → 벽 마찰이 입력값까지 동원 (유리 평균 0.077 → 0.150 → 0.212 ↔ 0.24) — 연화가 벽 · 판 마찰 동원도 바꾼다 (우리 판 · 벽 마찰 부작용 목록에 넣을 자리) ③ 직접 측정 입력 표 (값 · CoV · 출처 · 가정) 의 꼴 | 300 MPa 급 겹침 영역 · 소성 대리 |
| 후보 A′-0 · A · A′ (MPM 접촉) | 벽 마찰 동원 = 미끄럼 변위가 있어야 — 벽 · 판 접촉 규칙 (미끄럼 · 분리) 을 넣으면 '동원된 μ' 를 같은 링 구간 꼴로 보고할 수 있다 [카드 해석] | MPM 계산 |
| 후보 B · C · C′ · M0 | 없음 (탄성 점접촉만) | 큰 변형 법칙 · 캡 소성 |
| U0–U6 | U5 (비슷한 강성 입자 충돌 · 다물체) — 반발 계수를 **낙하 시험** 으로 재고 비구형은 회전 궤적까지 본다는 측정 절차 (p.87) | U1 · U3 · U6 의 해석해 · 수렴 |
| 조건 R1 (AM 하중 분담) | 없음 | — |
| 조건 R2 (미끄럼 · 분리) | 벽 미끄럼이 모자라면 입력 마찰보다 훨씬 작게 동원 (유리 G₀ 평균 0.077 ↔ 0.24) — 'μ 입력 = 동원 μ' 로 읽지 않는다 | 분리 |
| 조건 R3 · R6 · R7 | 없음 (경계 기억 · 형상 변형 · 파괴 0) | — |
| 조건 R4 (탈압) | 없음 | — |
| 조건 R5 (맞추는 값은 모델마다 하나) | 이 논문은 **0 개 맞춤** (전부 측정 · 입자–입자 값만 가정) — 그 대가 = 유리구슬은 K · μbulk 가 실험과 안 맞는다는 것을 그대로 보고 (맞추지 않으니 불일치가 정보로 남는다) | — |
| 결과 전 대조 항목 | 벽이 있는 우리 침대에서 **K (측압비) · 바닥 / 위 판 힘 비 · 동원 벽 마찰** 을 결과 전에 '보고만' 칸으로 — LPSCl 실측 K 는 [미확인] (이 논문 아님) | 우리 재료 값 |
| 랩 기준 (순수 SE 10–13 % · LPSCl 1.64 g/cm³) | 나란히 놓을 값 없음 (유리 초기 기공 어림 38.5 % = 랩 표준과 다른 문헌 값 · 다른 재료 · 0 압력) | — |
| 우리 DEM (E_eff 1.35 · 18 배 연화 · Heckel P_y 138 MPa) | σ/E 0.22 ↔ 이 논문 옥수수 0.0001G₀ 0.36 (같은 자릿수) · 그 런에서도 경계 힘 전달은 거의 그대로 (0.64 → 0.69) [판독] — '연화가 힘 전달 구조를 크게 바꾸지 않는다' 는 방향의 증거 하나 (단 kPa · 탄성 · 옥수수) | Heckel · 다압력 |
| 우리 MPM (E 1.53 · σ_y 0.30 · ν 0.49) | 탄성 연속체 K₀ = ν/(1 − ν) = 0.96 ↔ 실험 가루 K 0.35–0.4 — 가루의 K 는 입자 ν 가 아니라 충전 · 마찰 (§3-6) → MPM 의 벽 압력을 실험 K 와 견주려면 정의 (근사 · 높이) 를 같이 적어야 [카드 해석] | MPM 계산 |
| [DEM 우선 Ⓐ] 신뢰성 · 언로딩 | 출발 상태 · 정착 판정 · 경계 관측량 · 속도 인공물 경고 | 하중 제거 · 300 MPa |
| [DEM 우선 (수영)] 한 모델 가압 → 탈압 | 없음 | — |

★ **가장 큰 함정 넷** (우리 쪽에서 이 논문을 인용할 때):
1. **'강성을 낮춰도 결과가 안 바뀐다' 로 인용하지 않는다** — 원문은 벌크 강성 (압축 변위) 이 **직접** 바뀐다고 하고, '부차' 는 **벽 · 바닥 힘 전달** 에만 한정 · kPa · 탄성 · 유리는 그것도 바뀌었다 (0.74 → 0.57).
2. **'sudden unloadings' 를 탈압 · 되돌아옴으로 읽지 않는다** — 싣는 동안의 힘 급락 (p.93).
3. **유리구슬 DEM 을 '실험 검증됨' 으로 인용하지 않는다** — 바닥 힘은 맞았지만 K (0.66–0.70 ↔ ≈0.4) · μbulk (0.14 ↔ ≈0.35) 는 안 맞았다 (원문 p.90 · 판독).
4. **K 를 엄밀한 K₀ 로 · 원문 K 를 입자 ν 로 읽지 않는다** — 원문 스스로 '근사' · 벽이 변형 · 한 높이 σH · K 는 충전 · 마찰의 산물.

---

## 9. 적용 인사이트 (내 연구에 어떻게)

1. **연화는 '바뀌는 양' 과 '안 바뀌는 양' 을 나눠 적는다** — 이 논문 꼴로: 압축 변위 · 기공 (직접) ↔ 경계 힘 비 · 벽 마찰 동원 (부차 · 그러나 미끄럼으로 바뀜).  우리 18 배 연화의 부작용 목록 (언로딩 되돌아옴 · 판 마찰 · 점착 · 겹침 기반 면적) 을 같은 두 칸으로 정리할 근거 [카드 해석].
2. **출발 상태 감도를 등록 팔로** — 생성 간격 (예: 1.0 · 1.5 · 2.0 배 지름) × 결정화 검사 (단분산 SE 덱에서) · 원문은 간격 하나 (1.01d) 만으로 벽 마찰 동원 · 바닥 힘이 1.26 배 (578 ↔ 458 N [판독]) 바뀌었다.
3. **정착 판정 = 힘 비** — 평균 불균형 힘 ÷ 한 알 무게 (원문 ≈10⁻⁴ 자릿수) 를 운동 에너지와 함께 · 우리 덱의 정착 · 판 정지 판정에 단위 없는 문턱으로 [카드 해석].
4. **측정 입력 표의 꼴** — 값 · CoV · 출처 (제조사 · 표준 · 실측) · '가정' 표시를 한 표에 (Table 1–2) · 우리 Methods SI 물성 표 (E · ν · μ · e) 의 출처 칸 규율 (CLAUDE.md 규율 ⑥) 과 같은 방향.
5. **K·μ 곱 점검** — 벽이 있는 계산에서 바닥 / 위 판 힘 비를 Janssen exp(−4Kμh/D) 로 다시 계산해 판독 · 출력의 자기 일치를 본다 (이 카드 §3-6 에서 결정 충전 둘은 0.003 안).

---

## 10. 인용 가능 문장 (deck / paper 용 · 영문 초안 · 표지 그대로)

- "Chung and Ooi (2008) measured the particle properties of glass beads and corn grains independently and simulated a confined compression test with PFC3D; reducing the particle shear modulus to 1 % and 0.01 % of the measured value changed the bulk stiffness directly but had only a secondary effect on the load transmitted to the walls and the bottom platen." [인쇄 p.91 · p.95]
- "Assemblies of perfect spheres were more sensitive to the initial packing than non-spherical grains; the authors concluded that the perfect-sphere DEM model 'is not an appropriate representation even for the uniform glass beads' and 'cast doubt on many of the DEM studies in the literature based on perfect spheres'." [인쇄 p.95]
- "In their simulations, softer particles slipped more and mobilised more wall friction; at the measured stiffness the glass beads did not mobilise the limiting wall friction." [인쇄 p.92]
- 한정 (같이 적는다): ≤ ≈61 kPa · mm-sized elastic particles · Hertz–Mindlin without plasticity or adhesion · loading only (no unloading).

---

## 11. 주의 / 한계 (over-claim 방지 · 원문 비판)

1. **응력 영역** — kPa (사일로 · 저장) · 탄성 입자 · 우리 300 MPa 압밀과 기전 영역이 다르다 (소성 · 파쇄 · 큰 겹침 없음).
2. **유리구슬 DEM 은 실험과 맞지 않는다** — 원문이 인정 (p.90) · 원인 불명 · 충전 · 완전 구 가설만.
3. **원문 숫자가 적다** — DEM 쪽 값은 거의 전부 그림 판독 (이 카드 §3-3–3-5) · 이 카드의 판독은 선 겹침 · 점선 끊김 때문에 계열을 잘못 고를 수 있다 (겹친 계열은 표에 '겹침' 으로 표시).
4. **경우마다 런 하나** (시드 · 반복 [미확인]) — 충전 민감도와 시드 잡음이 갈리지 않는다.
5. **속도 33 배** — 원문은 다른 하중 경우에서 '벌크엔 영향 없음' 이라고만 (Chung 2006) · 힘 급락 · 국소 요동의 원인으로 남김.
6. **강성 연구의 유리 생성 미기재 · 그림은 1.01d 로 읽힌다** (§3-7) — 유리 바닥 힘 감소 (그림 9a) 의 출발점이 벽 마찰이 덜 동원된 특수 충전일 수 있다.
7. **K · μbulk 는 근사** — 수직 응력 = 판 평균 · 수평 = 한 높이 · 실험과 DEM 의 σH 출처가 다르다 (게이지 ↔ 벽 경계 힘).
8. **하중 제거 · 기공 · 배위수 · 힘 사슬 · 계산 비용 없음**.

---

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 서지 (p.95–96 목록 그대로) | 왜 | litdb |
|---|---|---|
| Chung, Y. C. 2006. Discrete element modelling and experimental validation of a granular solid subject to different loading conditions. PhD diss. University of Edinburgh, UK. | 벌크 강성 ↔ 입자 강성 관계식 (p.91 이 '여기서 유도' 라고만) · 속도 효과 · 측정 전부 · 실험 산포 설명 | 없음 (`ls` · grep 0) |
| Chung, Y. C. & J. Y. Ooi. 2006. Confined compression and rod penetration of a dense granular medium: Discrete element modelling and validation. In Modern Trends in Geomechanics, ed. by W. Wu and H. S. Yu. Berlin: Springer, 223–239. | 같은 시험 + 관입 · coetzee2017 의 Chung & Ooi [161] (관입 · 강성 ÷10⁴) 의 정체 확인 | 없음 |
| Chung, Y. C., J. Y. Ooi, & J. F. Favier. 2004. Measurement of mechanical properties of agricultural grains for DE models. Paper presented at 17th ASCE Engineering Mechanics Conference, Newark, N.J. | 단입자 압축 + Hertz 로 E · 세 입자 미끄럼 · 낙하 시험의 절차 (직접 측정 입력) | 없음 |
| O'Sullivan, C. & J. D. Bray. 2004. Selecting a suitable time step for discrete element simulations that use the central difference time integration scheme. Eng. Comput. 21 (2–4): 278–303. | 임계 시간 간격 × 0.20 규칙의 출처 | 없음 (morrissey2013 참고문헌에만) |
| Boutt, D. & B. McPherson. 2002. The role of particle packing in modeling rock mechanical behavior using discrete elements. In Discrete Element Methods: Numerical Modeling of Discontinua … ASCE. | 같은 접촉 매개변수에서 충전 (퇴적 방법) 만으로 거동이 달라진다는 2-D 근거 | 없음 |
| Ooi, J. Y. & J. M. Rotter. 1989. Elastic and plastic predictions of the storing pressures in conical hoppers. Trans. Inst. Eng. Aust. Mech. Eng. ME 14 (3): 165–169. | 'K 는 벌크 포아송비와 잘 맞는다' 의 근거 | 없음 |
| Masroor, S. A., L. W. Zachary, & R. A. Lohnes. 1987. A test apparatus for determining elastic constants of bulk solids. Paper presented at SEM Spring Conference on Experimental Mechanics, Houston, TX, USA. | Ko 시험기 원형 (벌크 탄성 상수) | 없음 |
| Tsuji, Y., T. Tanaka, & T. Ishida. 1992. Lagrangian numerical-simulation of plug flow of cohesionless particles in a horizontal pipe. Powder Technol. 71 (3): 239–250. | Hertz-Mindlin no-slip 접촉의 원전 | 없음 |

---

## [미확인] 목록

1. 감쇠 종류 · 값 · 시간 간격 값 · 벽 (아크릴) 강성 · DEM 벽–입자 μ · e 입력 (표의 입자–아크릴 값으로 보이나 명시 없음).
2. DEM 시료 높이 · 정착 뒤 기공 · 밀도 · 배위수 (원문 0) — 이 카드의 기공 어림은 가정 셋에 묶임 (§3-6).
3. 그림 8 변위 영점 (판 출발 위치).
4. 벌크 강성 ↔ 입자 강성 관계식 (Chung 2006).
5. 강성 연구 (그림 8–10) 의 유리구슬 생성 방법 (그림으로는 1.01d [카드 추론]).
6. 시드 · 반복 런 · 계산 시간 · 하드웨어.
7. 원통 벽 E_w · ν_w (식 2 의 입력).
8. 온도 · 습도 (옥수수 함수율 포함).
9. DEM K 를 낸 벽 높이 (게이지 높이 한 구간인지 벽 전체인지).
10. coetzee2017 의 Chung & Ooi [161] 이 어느 논문인지 (그 카드에 참고문헌 서지 없음).

---

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-17)

- PDF 15 쪽 = T&F 표지 1 + 본문 14 (인쇄 83–96) · 텍스트 층 전수 · 그림은 모두 300 dpi 회색조 원 래스터 (xref 107 · 163 · 188 · 189 · 198 · 199 · 213 · 222 · 223 · 237 · 253 · 254) · 표 · 식 = 벡터 글자.
- 서지: 인쇄 머리 (p.83) *"Particulate Science and Technology, 26: 83–96, 2008"* · 표지 *"(2007) … 26:1, 83-96 … Published online: 03 Mar 2011"* (`txt_cover_p83_to_cite_2007_printed_2008_online_2011.png`).
- 지수 (텍스트 층이 깨짐): 정착 *"(< 10⁻⁸ J)"* · *"(< 10⁻⁶ N)"* · *"1.3 × 10⁻² N"* · *"4.2 × 10⁻³ N"* — 400 dpi 렌더로 확인 (`txt_p86_layers_…`).
- 식 1–2 의 막대 (σ̄V · τ̄ · ε̄V) · 원주 변형 기호 ε_θ (본문 텍스트 층은 'eh') — 렌더로 확인.
- 판독 눈금 대조: 그림 3a · 4a · 8a · 10a · 12b 의 눈금 표시가 0.4 % 안 · 그림 10 입력 점선 = 0.244 · 0.335 (본문 기준 마찰).
- 그림 9a G₀ ↔ 그림 3b 1.01d 겹침 · 그림 10 점 간격 20 mm — §3-7.
- 정본 중복 확인: `papers/` 599 장에 chung · ooi 파일 없음 · DOI · 'Chung … Ooi' grep = morrissey2013 (참고문헌 표) · coetzee2017 (다른 [161]) 뿐.

---

## 🔗 관련 카드

- 같은 그룹 · 같은 꼴 시험기 (정본): `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` (EEPA · 구속 압축 → 하중 뺌 → 무구속 · K0 0.24–0.35 · 이 논문을 인용) · `thakur2014_eepa_adhesive_elastoplastic_dem`.
- DEM 보정 방법론 (정본): `coetzee2017_dem_calibration_review` (직접 측정 ↔ 벌크 역보정 · 강성 감소 증거표 — 그 표의 [161] 은 다른 Chung & Ooi 논문) · `paulick2015_elastic_particle_properties_dem_review` · `paulick2015_particle_contact_stiffness_two_particle_method` · `roessler2019_dem_cohesive_aor_cylinder_lift_calibration`.
- 접촉 법칙 (정본): `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` (다른 Walton) · `ai2011_rolling_resistance_contact_models_dem` (이 모델에 없는 구름 저항).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
