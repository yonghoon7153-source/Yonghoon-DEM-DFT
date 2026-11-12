<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 (본으로 삼은 카드) = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md · 접착 접촉 이웃 =
     johnson1971_jkr_surface_energy_contact_elastic_solids.md (이 논문 ref 1 · 우리 SJKR 대응식 §7-1) · thorntonning1998_adhesive_elastoplastic_contact.md
     (붙는 속도 V_s · 항복 속도 V_y) · thorntonyin1991_oblique_impact_elastic_spheres_adhesion.md (이 논문 ref 25) ·
     alizadeh2018_dem_adhesion_calibration_segregation_heap.md (이 논문을 ref 2 로 인용 — 후보 표 N-48 의 가리킨 카드).
     쪽 표기 = 학술지 쪽 472–482 를 PDF 쪽 p.1–11 로 (p.1 = 472 · p.11 = 482).  보충 자료: 그림 6 캡션이 *"supplementary online material
     for collision properties"* 를 가리키지만 PDF 에 딸려 오지 않았다 — 읽지 못함 [미확인].  표는 없다 (그림 13 · 식 25 + A.1–A.11).
     값 표지: [인쇄] = 본문 · 캡션 · 그림 안 글자 · [판독] = 그림의 **벡터 경로 좌표**에서 읽은 값 (래스터 아님 — 눈금 · 격자선 좌표로
     보정 · 재현 = litdb/figures/<slug>/digitized.csv 806 행) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 병기) ·
     [카드 재계산] = 이 카드가 원문 식 (7)–(13) 으로 정면 충돌을 다시 적분한 값 (조건 §3-3) · [카드 추론] · [추정] = 해석 ·
     [미확인] = 원문 (본문 11 쪽 전수) 에 없음.  원문 11 쪽은 텍스트 층 전수 + 쪽 렌더로 읽었고 숫자는 둘을 대조했다. -->
# 강성을 낮춘 접착 DEM 에서 JKR 접착을 다시 맞추는 규칙 — 분리 에너지 일정 ⇒ γ_mod = γ(E_mod/E)^{2/5} (부록 A: γ^{5/3}/E^{2/3} 불변) · 구름 저항은 (a/a₀)^{3/2} 만 바꿈 · 충돌 시간 ∝ (E/E_mod)^{2/5} · 대가 = 떼는 힘이 (E_mod/E)^{2/5} 로 줄어듦 · 검증 = Dahneke PSL–석영 반발 (E_mod/E 1 · 0.1 · 0.01 같은 곡선) · 벽 충돌 붙음 경계 λ_crit = c(e)·Ad^{5/2} — 단일 충돌 · 탄성 + 감쇠 · 소성 없음 — Hærvig · Kleinhans · Wieland · Spliethoff · Jensen · Sørensen · Condra (Powder Technol. 2017)

> slug `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` · DOI `10.1016/j.powtec.2017.07.006` · type `DEM theory (adhesive JKR contact · simplified JKR + Hertz spring + Hertz-Mindlin damping · reduced-stiffness rule · Dahneke rebound validation · single collisions only — no packing · no compaction · no plasticity)` · PDF `6f747056-48._On_the_adhesive_JKR_contact_and_rolling_models_for_reduced_particle_stiffness_discrete_element_simulations.pdf` · digested `2026-11-13` · status ✅
>
> **저자**: **J. Hærvig\*** (교신 · jah@et.aau.dk) · A.L. Jensen · K. Sørensen · T.J. Condra — Aalborg University, Department of Energy Technology (Pontoppidanstræde 111, Aalborg) · U. Kleinhans · C. Wieland · H. Spliethoff — Technical University of Munich, Institute of Energy Systems (Garching) · *Powder Technology* **319** (2017) 472–482 (본문 11 쪽 · 표 없음) · 접수 2017-03-15 · 수정 06-15 · 승인 07-03 · 온라인 07-06 · 연구비 The Danish Council for Strategic Research (no. 1305-00036B) · 제1 저자의 TU München 외부 체류 중 연구 (p.10).  키워드 (원문): Discrete Element Method · Reduced particle stiffness · Adhesive particles · JKR adhesive model · Rolling resistance torque · Computational efficiency.
> **이웃 카드 (링크만)**: [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (이 논문 = 그 ref 2 · 응집수 고정 ⇒ Γ ∝ E\*^{2/5}) · [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (ref 1 · 우리 믹서 SJKR ↔ JKR 대응식) · [`thorntonyin1991_oblique_impact_elastic_spheres_adhesion`](thorntonyin1991_oblique_impact_elastic_spheres_adhesion.md) (ref 25 · 식 17 의 근거) · [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) (V_s · V_y 식) · [`ai2011_rolling_resistance_contact_models_dem`](ai2011_rolling_resistance_contact_models_dem.md) (구름 저항 모델 분류 · 우리 cdt) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (우리 압축 덱 hooke/hysteresis 의 정의서) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md) (연화와 시간 간격 · 힘 꼬리) · [`vanlew2015_modifying_youngs_modulus_distribution`](vanlew2015_modifying_youngs_modulus_distribution.md) (연화의 역효과 F_c ∝ E\*^{2/5}) · [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) · [`lischka2025_dem_eirich_intensive_mixer_dry_mixing`](lischka2025_dem_eirich_intensive_mixer_dry_mixing.md) (연화 G + JKR γ 보정값 · 응집수로 γ 재계산) · [`deng2021_mechanical_surface_energy_tester_bond_number`](deng2021_mechanical_surface_energy_tester_bond_number.md) (Bo · 떼는 힘 시험 · SJKR 판정식).
> **판독 원자료**: `litdb/figures/haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem/digitized.csv` (806 행 — 그림 3 · 4 · 6 · 7 · 8 · 11 · 12 · 13 · 벡터 좌표) · 크롭 65 장 (그림 13 = 다시 자름 8 + 손 크롭 5 · 식 36 = 식 1–25 + A.1–A.11 하나씩 · 근거 문단 16) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 접착 입자 DEM 에서 계산 시간을 줄이려고 영률을 E → E_mod 로 낮추면 겹침이 커져 충돌이 더 끈적해지므로, **평형 겹침에서 겹침 0 까지 떼는 에너지 (분리 에너지) 를 같게** 두면 표면 에너지를 **γ_mod = γ(E_mod/E)^{2/5}** 로 함께 낮춰야 한다 (식 23–24 · 부록 A) — 그러면 이진 · 벽 충돌의 반발 (붙음 / 되튐) 이 E_mod/E 10⁻³–10³ 에서 그대로이고 (그림 8 · 13) 충돌 시간이 (E/E_mod)^{2/5} 로 늘어 시간 간격을 그만큼 키울 수 있지만, **떼는 힘은 (8/9)·3πRγ_mod 로 줄어든다** — 단일 충돌만 다룬 탄성 (Hertz + 단순 JKR + 점성 감쇠) 논문이고 소성 · 압밀 · 침대는 없다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 강성을 낮출 때 점착을 어떻게 다시 맞추나 | 분리 에너지 ∫₀^{δ₀}(F_jkr + F_spring)dδ 일정 (식 23) ⇒ **γ_mod = γ(E_mod/E)^{2/5}** (식 24) · 부록 A 의 결론 = **γ^{5/3}/E^{2/3} 일정** (A.11) · *"actually the same criterion Gu et al. [8] found for the contact independent van der Waals formulation"* (p.4) | [인쇄] p.4 · p.10 |
| ② 그 규칙이 정확한가 | 이진 정면 충돌 e_eff/e 가 E_mod/E 10⁻³ … 10³ 에서 평평 — **0.884 (Ad 5) · 0.745 (10) · 0.323 (20) · 0 (40)** (그림 8 · e 0.3) · PSL → 석영 5 m/s 충돌의 속도 곡선 세 개 (E_mod/E 1 · 0.1 · 0.01) 의 **v_final −3.593 m/s** 가 셋째 자리까지 같다 (그림 13) · 이 카드 증명: 식 (7)–(16) 은 E → E/X · γ → γX^{−2/5} 에서 겹침 ∝ X^{2/5} · 시간 ∝ X^{2/5} · 힘 ∝ X^{−2/5} · 속도 불변으로 **정확히** 옮겨진다 (감쇠 포함 · 근사 아님) | [판독] 그림 8 · 13 · [카드 산술] §3-7 |
| ③ 대가 | **떼는 힘 감소** (8/9)F_C,mod = (8/9)3πRγ_mod (p.4 · p.9) → 외력이 그보다 *"several orders of magnitude lower"* 여야 (초록) · 벽 위에서 더 멀리 굴러감 (p.5 · p.9) · 조밀 충전 (국소 부피 분율이 closed-pack 에 가까울 때) 에서 E_mod/E < 10⁻³ 이면 접착 거동이 *"might be changed slightly"* ([8, 9] 인용 · 수치 근거 없음 · p.9) · 충돌 시간 **Δt_col,mod = Δt_col(E/E_mod)^{2/5}** = 시간 간격 이득 (p.9 · Silbert [30] Δt_col/δt ≈ 50) | [인쇄] p.1 · p.4 · p.5 · p.9 |
| ④ 구름 저항 | Dominik–Tielens [2, 3] · Krijt [4] 모델 (ξ_crit = a₀(Δγ/γ)/12 · k_r = 4F_C(a/a₀)^{3/2}) 에서 **(a/a₀)^{3/2} 만 (a_mod/a₀,mod)^{3/2}** 로 · F_C · ξ_crit 은 원래 값 → 평형 (a = a₀) 의 구름 문턱 · 정지 / 구름 경계 그대로 (p.4 · 그림 4 — E_mod/E = 0.1 로 그려짐 [판독]) | [인쇄] p.4 · [판독] 그림 4 |
| ⑤ 무차원 지도 | 벽 비스듬 충돌의 붙음 / 되튐 경계 **λ_crit = c(e)·Ad^{5/2}** (식 25) · c = **5,365 (e 0.1) → 0.334 (0.9)** (그림 12) · 그림 11 아홉 선의 기울기 2.5000–2.5003 · 지수 5/2 = 식 24 와 같은 말 (λ/Ad^{5/2} ∝ (운동 에너지 ÷ 분리 에너지)^{3/2}) | [판독] 그림 11 · 12 · [카드 산술] §3-5 |
| ⑥ 실험 대조 | Dahneke [27]: PSL **⌀1.27 µm** → 연마 석영 · **E 271 MPa · γ 0.11 J/m² · ρ 1026 kg/m³ · e 0.86** (*"fitted to experimental data at high velocities"* · Krijt [28] 의 *"fitted values"*) · 실험 138 점 ↔ 계산선: 붙음 문턱 2.40 m/s · 차 평균 +0.017 · sd 0.044 · 세 E_mod/E 계산의 차 ≤ 4.7×10⁻⁵ | [인쇄] p.5 그림 6 캡션 · [판독 · 카드 산술] §3-3 |
| ⑦ DEM 한계 · 소성 | 두 입자 / 입자–벽 **단일 충돌만** · 탄성 Hertz + JKR + 점성 감쇠 — 소성 · 형상 변화 · 압밀 · 다접촉 0.  소산은 반발 계수 e 하나 (맞춤값).  이 카드 재계산: 단순 JKR 은 닿을 때 · 떨어질 때 같은 힘 경로 (둘 다 겹침 0 · 인력 (8/9)F_C) → **접착 이력 고리 넓이 0** → e → 1 이면 늘 되튄다 (0.05 · 0.5 · 2 m/s 에서 e_eff 0.977 · 0.999 · 1.000) = 붙음은 감쇠가 정한다 | [인쇄] p.2–3 · [카드 재계산] §3-7 |
| ⑧ 우리 연화와의 다리 | 이 논문 접착 = **단순 JKR** (Parteli 등 [13]) — 우리 믹서의 LIGGGHTS SJKR (인력 = CED × 겹침 면적) · 압축 덱 hooke/hysteresis (선형 + adhesion 강성) 와 꼴이 다르다.  같은 '분리 에너지 일정' 을 SJKR 에 옮기면 W_sep = (81/80)π⁵R\*³CED⁵/E\*⁴ ⇒ **CED ∝ E\*^{4/5}** (이 논문 밖) · 우리 F₀ 보존 규칙 (CED ∝ E\*^{2/3}) 은 이 논문 그림 3 · 4 의 **'강성만 낮춤'** 쪽 (떼는 힘 그대로 · 분리 에너지 ∝ E\*^{−2/3}) | [카드 산술] §7-3 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **PSL (폴리스타이렌 라텍스) ⌀1.27 µm ↔ 연마 석영 판** (검증 하나) · 나머지 그림은 **무차원** (재료 없음) — LPSCl · NCM 아님 ② **단일 충돌만** — 침대 · 충전 · 압밀 · 응집체 (다입자) 계산 0 회 (§5.2 가 예고한 *"a surface with an initial layer of particles"* 위 증착도 §5.3 에 없다) ③ 접착 = **단순 JKR** (겹침 < 0 이면 끊김) — JKR 원식 (음의 겹침에서 목이 끊김) · LIGGGHTS SJKR · 우리 hooke/hysteresis 와 다른 꼴 → **지수 2/5 는 그 꼴의 것** ④ 탄성 + 점성 감쇠 · 소성 · 마모 · 파괴 없음 ⑤ e 0.86 · E 271 MPa · γ 0.11 J/m² = Krijt [28] 의 **맞춤값** (그 보충 자료는 받지 못함 · 실물 PSL 물성 [미확인]) ⑥ 적분기 · 시간 간격 · 코드 이름 · 런 수 [미확인] ⑦ Ad 의 정의가 그림 7 캡션과 §5.1 본문에서 다르다 (같은 두 구에서 2/3 배) · 그림 8 의 기준 λ = 10⁶ 이 그림 7 에서는 λ = 2.50×10⁵ 의 값과 맞는다 (4 배 · 원인 [미확인]).
⇒ **절대값 전이**: 값 (e · E · γ · c(e)) 은 PSL 이거나 무차원 — 우리 재료로 옮기지 않는다.  옮길 수 있는 것은 **규칙 · 시험 꼴** — (1) 강성을 바꿀 때 **지킬 불변량을 먼저 고른다** (떼는 힘 ↔ 분리 에너지 — JKR 에서 둘은 (E_mod/E)^{2/5} 만큼 갈린다) (2) 지킨 불변량대로 결과가 같은지 **단일 충돌로 시험** (그림 13 꼴: 같은 v_final · 시간축만 X^{2/5}) (3) 지수는 **접촉 법칙의 꼴마다 다르다** (단순 JKR 2/5 · SJKR 4/5 [카드 산술] · 선형 hooke [미확인]).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-48 의 '왜' 칸)

의도 원문: *"k · l — "★ 연화 강성 JKR 의 엄밀 환산 — 우리 SJKR 연화와 직접 관련 · 카드 없음" → 강성을 낮출 때 점착을 어떻게 다시 맞춰야 하는가 (보정값이 물성이 아니라는 근거 쪽)"* (근거 = `alizadeh2018_dem_adhesion_calibration_segregation_heap` L265)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "연화 강성 JKR 의 엄밀 환산" | **채움** | 식 23 (분리 에너지 일정 · δ_n,0 = (1/3)a₀²/R) → 식 24 γ_mod = γ(E_mod/E)^{2/5} · 부록 A (A.1–A.11 · 결론 γ^{5/3}/E^{2/3} = γ_mod^{5/3}/E_mod^{2/3}) [인쇄] p.4 · p.10.  확인: 그림 8 (이진 정면 · e 0.3 · λ 기준 10⁶ · E_mod/E 10⁻³–10³ 평탄) · 그림 13 (PSL–석영 5 m/s · 세 E 의 v_final 같음).  '엄밀' 의 범위: **법선 충돌은 정확한 자기 상사** (이 카드 증명 §3-7 — 원문은 에너지 등식만 보였다) · 구름은 유도가 아니라 **처방** (평형 문턱만 보존 · p.4) · 조밀 다입자는 다루지 않음 (p.9 의 10⁻³ 경고) |
| "우리 SJKR 연화와 직접 관련" | **일부** | 이 논문의 접착 = **단순 JKR** (식 8–10 · *"In the present study, focus is on the simplified JKR model suited for DEM simulations and used in studies such as [13,21,22]"* p.2) — LIGGGHTS `cohesion sjkr` (인력 = CED × 겹침 면적 · `johnson1971_…` §7-1) 가 아니다.  지수 2/5 는 JKR 의 것 · 같은 '분리 에너지 일정' 을 SJKR 에 옮기면 **CED ∝ E\*^{4/5}** [카드 산술 §7-3] · 우리 믹서 F₀ 보존 (CED ∝ E\*^{2/3} · `johnson1971_…` §7-1 ②) 은 이 논문 그림 3 · 4 의 '강성만 낮춤' 곡선 쪽 (떼는 힘 그대로 · 분리 에너지 ∝ E\*^{−2/3}) |
| "강성을 낮출 때 점착을 어떻게 다시 맞춰야 하는가" | **채움** | 법선: γ_mod = γ(E_mod/E)^{2/5} (식 24) · 구름: *"the only way to retain the behaviour of the original model is to keep all terms but the (a/a0)3/2 term unaltered"* (p.4 · `txt_p4_p5_sec32_rolling_only_a_over_a0_modified`) · 대가: 떼는 힘 (8/9)·3πRγ_mod (p.4) · *"care should be taken … to make sure that an external force … is several orders of magnitude lower than the critical force required to separate particles"* (초록) · 시간 간격 이득 Δt_col,mod = Δt_col(E/E_mod)^{2/5} (p.9) |
| "(보정값이 물성이 아니라는 근거 쪽)" | **일부 (간접)** | 직접 문장은 없다.  (1) 연화 모델의 γ_mod 는 **고른 E_mod 에 묶인 값** (식 24) — 같은 재료라도 E_mod 마다 다른 γ 가 같은 충돌을 낸다 → DEM 의 γ 를 그 재료의 표면 에너지로 읽을 수 없다 [카드 추론] (2) 검증 값이 맞춤값: *"expected collision outcomes typically differ slightly from experiments as even small imperfections in particle or wall material result in a non-perfect collision. Therefore, the fitted values suggested by Krijt et al. [28] are used when comparing to experiments"* (p.5) · e 0.86 = *"fitted to experimental data at high velocities"* (그림 6 캡션) (3) 연화의 동기 = 계산 시간 (*"A widely used approach to decrease computational costs is to decrease the particle stiffness"* p.1) — 물성이 아니라 수치 장치 (4) 이 카드 재계산: 단순 JKR 의 붙음은 e (감쇠) 가 정한다 (§3-7) → 맞춘 e 는 실제 접착 이력까지 떠안은 모델 매개변수 [카드 추론] |
| (k) DEM 의 한계 문장 | **일부** | 연화 DEM 의 한계는 있다: 떼는 힘 감소 (p.4 · p.9 · 초록) · *"collisions involving larger agglomerates behave differently when the particle stiffness is reduced beyond a certain point"* ([8, 9] · p.7) · E_mod/E < 10⁻³ 조밀 충전 경고 (p.9) · 굴러가는 거리 (p.5 · p.9) · 나노초 시간 간격 (초록).  단단한 구 · 점접촉 · 접촉 독립의 한계는 말 없음 · 큰 입자 (*"typically dp > 10 µm"*) 에서 변형이 접착에 중요 (p.2 · Tabor [11]) |
| (l) 소성이 왜 어려운가 | **없음** | 소성 · 형상 변화 · 부피 보존 유동 · 가공 경화 · 하중 이력 · 탈압 회복 — 말 없음.  모델은 탄성 (Hertz + JKR) + 점성 감쇠 · 소산은 e 하나 |
| 가리킨 카드의 2 차 인용 | **같음 (카드 문제 없음)** | alizadeh2018 L265 서지 (저자 일곱 · 제목 · Powder Technol. 319 (2017) 472–482) = 원문 첫 쪽과 같다.  L49 *"강성 연화 JKR 해석 = Hærvig 2017 (Powder Technol. 319, 472 — ref 2, '같은 함수 꼴')"* = 그 카드 L29 의 응집수 고정 ⇒ Γ ∝ E\*^{2/5} 와 이 논문 식 24 · A.11 이 같은 꼴 ✓.  L236 *"JKR 에서 떼는 힘은 E 와 무관하지만 분리 일은 E\*^{−2/3}"* = p.4 (*"by only reducing the particle stiffness … the same force (FN = −(8/9)FC) is required to break contact"*) · A.11 과 같다 ✓ · *"(그들 E 1/6.4 연화면 ×0.48)"* = 6.4^{−2/5} = 0.476 [카드 산술] ✓.  ⚠ 기호만: 이 논문 γ = 면 하나의 표면 에너지 (F_C = 3πRγ ⇒ JKR 의 접착 일 W = 2γ) — 지수와는 무관 |

⇒ **의도 대조 결과: 일부** — '연화 강성 JKR 환산 · 점착을 다시 맞추는 법' 은 **채움** (식 24 · 이 카드가 정확한 자기 상사로 확인) · 'SJKR 과 직접' 은 접착 꼴이 달라 **일부** (SJKR 판 지수 4/5 는 이 카드 유도) · '보정값 ≠ 물성' 은 **간접** (맞춤값 · E 에 묶인 γ) · l (소성) 은 **없음**.

---

## 1. 한 줄 요약
마이크론 접착 입자의 DEM 은 높은 강성 때문에 나노초 시간 간격이 필요하다는 동기 (초록 · p.1) 에서, Hertz 스프링 + 단순 JKR 접착 (겹침이 음이 되는 순간 끊김) + 점성 감쇠 + Dominik–Tielens / Krijt 구름 저항으로 된 모델의 영률을 E → E_mod 로 낮출 때 **평형 겹침까지의 분리 에너지를 같게** 두는 조건을 풀어 **γ_mod = γ(E_mod/E)^{2/5}** (부록 A: γ^{5/3}/E^{2/3} 불변) 를 얻고, 구름 저항은 (a/a₀)^{3/2} 만 바꾸라고 처방한다.  Dahneke 의 PSL → 석영 반발 실험 (Krijt 의 맞춤값) 과 E_mod/E 1 · 0.1 · 0.01 계산이 같은 곡선을 내고 (그림 6), 무차원 이진 충돌은 E_mod/E 10⁻³–10³ 에서 반발이 그대로이며 (그림 8), 벽 비스듬 충돌의 붙음 경계는 λ_crit = c(e)·Ad^{5/2} (그림 11 · 12) — 대가는 **떼는 힘이 (E_mod/E)^{2/5} 로 준다** 는 것과 조밀 충전 경고 (E_mod/E < 10⁻³) 다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| J. Hærvig\* · U. Kleinhans · C. Wieland · H. Spliethoff · A.L. Jensen · K. Sørensen · T.J. Condra (Aalborg · TU München) | Powder Technol. 319 (2017) 472–482 · 11 쪽 | 10.1016/j.powtec.2017.07.006 | **재료 없음 (무차원)** + 검증 하나 = PSL ⌀1.27 µm ↔ 연마 석영 (Dahneke [27] 실험 · Krijt [28] 맞춤값) · SE · AM 없음 | 이론 (해석 유도) + DEM 단일 충돌 계산 (두 입자 정면 · 입자–벽 비스듬 · 외력) — 침대 · 압밀 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 모델 식 (식 1–22) [인쇄] — 크롭 `eq_01_*` … `eq_22_*`
- **식 (1) Tabor 매개변수** λ_T = (4Rγ²/(E²D_min³))^{1/3} · D_min = *"typically taken to be 1.65 Å [12,13]"* · JKR = λ_T > 3 · DMT = λ_T < 0.1 · Maugis = 사이 (Johnson–Greenwood [10] · p.2).  **식 (2)** 1/R = 1/r_i + 1/r_j · 1/E = (1 − ν_i²)/E_i + (1 − ν_j²)/E_j (E = 유효 영률).
- **식 (3)–(4)** m d²x/dt² = F_con + F_ext · I dω/dt = M_con + M_r (F_ext = 중력 · 시간 무관 유체력 · 자기력).  **식 (5)** F_con,n = F_spring,n + F_jkr,n + F_damp,n · **식 (6)** F_con,t = F_spring,t + F_damp,t.
- **단순 JKR (p.2–3)**: *"The simplified JKR model has the same force-displacement relation as the original model, requires the same 8/9 of the critical force F = (8/9)FC = (8/9)3πRγ to break contact but assumes contact is broken as soon as the normal overlap becomes negative in the particle separation process."* (`txt_p2_p3_simplified_jkr_model`).
- **식 (7)** a₀ = (9πγR²/E)^{1/3} (평형 접촉 반경 [23]) · **식 (8)** F_jkr,n = 4√(πγEa³) n · **식 (9)** F_spring,n = −(4E/(3R))a³ n · **식 (10)** a⁴ − 2Rδ_n a² − (4πγ/E)R²a + R²δ_n² = 0 (반복 풀이 또는 Parteli [13] 의 해석식).
- **식 (11)** F_damp,n = −2(5/6)β√(S_n m) v_n [인쇄 그대로 — 식 16 은 √(5/6) · 이 카드 재계산은 √ 가 있어야 그림과 맞는다 · §11] · **식 (12)** β = ln(e)/√(ln²(e) + π²) · **식 (13)** S_n = 2E√(Rδ_n).
- **식 (14)** F_spring,t = −S_t Δs_t · S_t = 8G√(Rδ_n) · **식 (15)** 1/G = (2 − ν_i)/G_i + (2 − ν_j)/G_j · G_i = E_i/(2(1 + ν_i)) · **식 (16)** F_damp,t = −2√(5/6)β√(S_t m) v_t · **식 (17)** 접선력 한계 \|F_con,t\| ≤ μ_s\|F_N + 2F_C\| ([24, 25] · μ_s = 미끄럼 마찰 계수 · 값 없음).
- **구름 (§2.2 · p.3–4 · `txt_p3_p4_rolling_resistance_model`)**: 마이크론 입자에서는 비틀림 · 미끄럼보다 구름이 응집체 형성 · 해체에 중요 ([19, 26]) · **식 (18)** ξ_crit = (a₀/12)(Δγ/γ) (Krijt [4] · Dominik–Tielens [2, 3] 은 원자 지름 정도) · **식 (19)** ξ = ∫v_L dt · t_r (t_r 정의 없음 [미확인]) · **식 (20)** v_L = R(ω_i − ω_j) × n + ½((r_i − r_j)/(r_i + r_j))v_S · **식 (21)** M_r = k_r ξ (ξ < ξ_crit) · k_r ξ_crit (ξ ≥ ξ_crit) · k_r = 4F_C(a/a₀)^{3/2} · **식 (22)** \|ξ\| ≤ \|ξ_crit\|.
- 맞춘 값 · 값의 수 (원문): 검증 (그림 6) 의 E · γ · e (ρ · d_p 는 실험 조건) — Krijt [28] 의 맞춤 · Δγ/γ · μ_s · ν 의 값은 본문에 없다 (SI [미확인]).

### 3-2. ★ 환산 규칙 (식 23–24 · 부록 A) [인쇄 + 카드 산술] — `eq_23_*` · `eq_24_*` · `eq_A01_*` … `eq_A11_*`
- 동기 (p.4 · `txt_p4_sec31_reduced_stiffness_needs_reduced_gamma`): *"When a reduced particle stiffness is introduced in DEM simulations, the particles will inevitably overlap more during collision. If the surface energy density γ is left unchanged, the result is a more adhesive collision as the kinetic energy lost upon collision is increased significantly. Therefore, a reduced particle stiffness has to be balanced by a reduced surface energy density for the outcome of the collision to remain the same."*
- 목적 (p.2 · `txt_p2_aim_emphasise_reducing_adhesiveness`): *"the aim of this paper is to emphasise the importance of reducing the particle adhesiveness when a reduced particle stiffness is introduced. For this purpose an analytically derived criterion on how to adjust the surface energy density to account for a reduced particle stiffness for collisions in the JKR limit (λT > 3) is presented."*
- 요약 (p.8 · `txt_p8_p9_sec61_summary`): *"When using the simplified JKR model (Eq. (8)), the particle Young's modulus can be reduced from E to Emod as long as the surface energy density is reduced as well using γmod = γ(Emod/E)^{2/5}. That way, the border between sticking and rebounding behaviour remains the same when the particle stiffness is reduced."* · 구름은 *"only the term (a/a0)3/2 should be changed to use modified values. That way, the border between rolling and sticking remains the same."*
- **식 (23)** ∫₀^{δ_n,0}(F_jkr + F_spring)dδ_n = ∫₀^{δ_n,0,mod}(F_jkr,mod + F_spring,mod)dδ_n · δ_n,0 = (1/3)a₀²/R → **식 (24) γ_mod = γ(E_mod/E)^{2/5}**.
- p.4 (`txt_p4_eq24_gu_same_criterion_pulloff_reduced`): *"The result in Eq. (24) is actually the same criterion Gu et al. [8] found for the contact independent van der Waals formulation [16] FvdW = AHR/(6D²min) with the effective Hamaker constant AH = 24πD²minγ."* · 강성만 낮추면 *"the same force (FN = −(8/9)FC) is required to break contact. However, the equilibrium overlap is increased significantly as δN,0,mod = (1/3)a²0,mod/R = (3π²γ²R/E²mod)^{1/3}"* · 둘 다 낮추면 *"the normal force required to break contact is reduced to FN = −(8/9)FC,mod = −(8/9)3πRγmod. This can pose some impracticalities for systems with large external forces acting to separate the particles."*
- 부록 A (p.10): 겹침 대신 접촉 반경 a 로 적분 (A.1) · 겹침 0 의 근 a = (4πγR²/E)^{1/3} (A.2–A.5) · 위 끝 = a₀ (A.6 · A.7) · δ_n(a) 의 두 근 중 (A.9) δ_n = a²/R − 2√(πγa/E) · (A.10) dδ_n = (2a/R − 2√(γπ)/√(Ea))da [인쇄 — (A.9) 를 미분하면 둘째 항은 √(γπ)/√(Ea) · §11] · **(A.11) γ^{5/3}/E^{2/3} = γ_mod^{5/3}/E_mod^{2/3}**.
- **이 카드 검산 [카드 산술]**: a = s·(πγR²/E)^{1/3} 로 두면 분리 에너지 **W_sep = C·γ^{5/3}R^{4/3}E^{−2/3}** · C = π^{5/3}·[(8/3)s^{7/2} − 2s² − (8/15)s⁵]_{4^{1/3}}^{9^{1/3}} = 6.739 × 2.168 ≈ **14.61** (수치 적분과 같음) · 인쇄 (A.10) 의 야코비안 그대로면 C ≈ 10.64 — **두 경우 모두 A.11 의 불변성은 성립** (E/10 · γ × 10^{−2/5} 에서 W_sep 비 1.000000).  그림 6 조건 (R = 0.635 µm · γ 0.11 J/m² · E 271 MPa) **W_sep = 4.81 × 10⁻¹⁵ J** · γ 를 그대로 두고 E/10 이면 **W_sep × 4.642 (= 10^{2/3})** — 원문 *"more adhesive collision"* 의 크기.
- 그림 3 (힘–겹침 모식도 · 눈금 숫자 없음) 의 격자선 위치 [판독]: δ_mod2/δ₀ = **2.512 (= 10^{0.4})** · δ_mod1/δ₀ = **4.642 (= 10^{2/3})** · F_C,mod2/F_C = **0.398 (= 10^{−0.4})** → 그림은 **E_mod/E = 0.1** 의 해석값으로 그려졌다.

### 3-3. ★ 실험 검증 (그림 6 · Dahneke [27] · p.5)
- 조건 [인쇄 · 그림 6 캡션]: *"PSL spheres colliding with a plane wall of polished quartz. Collision properties are dp = 1.27 µm, E = 271 MPa, γ = 0.11 J/m², ρp = 1026 kg/m³ and e = 0.86 (fitted to experimental data at high velocities), see Krijt et al. [28] and supplementary online material for collision properties."*  E_mod/E = 10⁰ · 10⁻¹ · 10⁻² (γ 는 식 24).
- 원문 판정 (p.5 · `txt_p5_sec4_validation_dahneke_krijt_fitted`): *"by reducing the particle stiffness from E to Emod and modifying the surface energy density by analytical solution in Eq.(24), the exact same results are indeed obtained."*
- [판독 · 벡터 좌표]: Dahneke 점 **138 개** (v 2.418–14.94 m/s · 가장 느린 점 e_eff 0.394 · 12 m/s 위 평균 0.834) · 계산선 (E_mod/E = 1) = **2.40 m/s 까지 0** → 2.50 m/s 0.2236 · 5.0 m/s 0.7186 · 10 m/s 0.8112 · 16 m/s 0.8345 · 네모 (10⁻¹) ↔ 가위표 (10⁻²) 차 **≤ 4.7 × 10⁻⁵** (33 쌍) · 표식 ↔ 선 ≤ 1 × 10⁻⁴.  실험 − 계산선 = 평균 **+0.017 · sd 0.044** [카드 산술 · 선 보간].
- **[카드 재계산]** 식 (7)–(13) 을 입자–벽 정면 충돌로 (R = r_p = 0.635 µm · m = 1.100 × 10⁻¹⁵ kg · E 271 MPa 를 식 2 의 유효 E 로 · 식 11 에 √(5/6) · RK4) 풀면: **e_eff(5 m/s) 0.7186 · 붙음 문턱 2.4005 m/s** · e_eff 0.2236 (2.5) · 0.4833 (3) · 0.6506 (4) · 0.7924 (8) · 0.8345 (16 m/s) — 그림 선과 넷째 자리까지 같다.  인쇄 식 (11) (√ 없음) 이면 0.7428 · 문턱 2.271 m/s → 그림과 안 맞음 ⇒ **식 11 은 √ 가 빠진 조판** [카드 재계산].
- [카드 산술]: 이 조건의 **λ_T = 45.3** (D_min 1.65 Å · 원문은 계산하지 않음) > 3 → JKR 영역 · F_C = 3πRγ = 6.58 × 10⁻⁷ N · a₀ = 0.167 µm · δ₀ = 14.6 nm · 붙음 문턱의 운동 에너지 ½mv\*² = 3.17 × 10⁻¹⁵ J = **분리 에너지 W_sep 의 0.659 배** (e 0.86 감쇠와 함께).

### 3-4. ★ 이진 정면 충돌 (그림 7 · 8 · §5.2 · p.6–7)
- 무차원 (§5.1 · `txt_p5_p6_sec51_dimensionless_lambda_ad`): **λ = E/(ρ_p v²)** (탄성 매개변수) · **Ad = 3γ/(ρ_p v² r_i)·(1 + β³)/((1 + β²)β)** [29] (β 정의 없음 — 감쇠 β 와 같은 글자) · ê = e_eff/e · 벽: λ = E/(ρ_p v² sin²ω) · Ad = 3γ/(ρ_p v² sin²(ω) r_p) · 구름: F̂ = F_ext/F_yield · F_yield = M_r/R → *"Fyield = 4FCa0(Δγ/γ)/12"* (a = a₀ · 인쇄식에 /R 없음 — 차원이 토크 [카드 산술] · §11).  ⚠ 그림 7 캡션은 **Ad = γ/(ρ_p v² R)** — 같은 크기 두 구 (β = 1 · R = r/2) 에서 캡션 값 = 본문 값의 **2/3** [카드 산술] · 그림이 어느 정의인지 [미확인].
- **그림 7** (수정 없는 모델 · e 0.3 · Ad 5 · 10 · 20 · 40 · λ 10³–10⁹) [판독 — 곡선 꼭짓점 0.1 decade 간격]: 붙음 → 되튐 전환 Ad 5 = λ 5,012 → 6,310 (ê 0.170) · Ad 10 = 31,624 → 39,809 (0.260) · Ad 20 = 158,500 → 199,515 (0.157) · Ad 40 = 1.000 × 10⁶ → 1.259 × 10⁶ (0.252) · **λ = 10⁶ 의 ê = 0.936 · 0.865 · 0.698 · 0**.  원문 (p.7 · `txt_p7_sec52_restitution_changes_agglomerate_caveat`): *"decreasing the particle stiffness does, in most cases, result in a different effective coefficient of restitution. The exception is at sufficiently low elasticity parameters, where the particle stay attached upon collision. Furthermore, … as long as eeff/e ≈ 1, corresponding to high elasticity parameters, the elasticity parameter can be reduced with only small changes in effective coefficient of restitution as the collision behaves as non-adhesive."*
- **그림 7 의 붕괴 [카드 산술 · 판독]**: 같은 ê 에서 λ/Ad^{5/2} = **117.8–119.3 (ê 0.2) · 219.7–220.7 (0.5) · 1,331.7–1,332.4 (0.8) · 6,273–6,305 (0.9)** — 네 곡선이 λ/Ad^{5/2} 한 변수의 **같은 곡선** (±0.7 %) = 아래 §3-7 의 자기 상사를 원문 자료가 스스로 보여 준다.  두 입자 붙음 경계 λ_crit/Ad^{5/2} ≈ 100–112 (네 구간의 교집합 · e 0.3) ↔ 그림 12 의 벽 c(0.3) = 147.3 — Ad 정의 · 질량 · 반지름 규약이 달라 직접 견줄 수 없다.
- **그림 8** (γ 를 식 24 로 바꾸며 E_mod/E = 10⁻³ … 10³ · 표식 7 점 · λ 기준 10⁶ · e 0.3) [판독]: 평탄 **0.884 (Ad 5) · 0.745 (10) · 0.323 (20) · 0.000 (40)**.  원문: *"the effective coefficient of restitution eeff/e retains the values from λ = 10⁶ in Fig. 7"* (p.7).
- ⚠ **그림 7 ↔ 8 어긋남 [카드 산술]**: 그림 8 의 평탄값은 그림 7 의 λ = 10⁶ 값 (0.936 · 0.865 · 0.698) 이 **아니라** λ = **2.499 · 2.501 · 2.504 × 10⁵** 의 값과 같다 (4.00 배 · 세 곡선 모두 ±0.15 %).  원인 [미확인] — λ 에만 속도를 다른 규약 (상대 ↔ 입자 속도 · 2 배) 으로 넣으면 정확히 4 배 [추정].  Ad 40 은 두 그림 모두 0 (문턱이 1.0–1.26 × 10⁶ 사이).  ⇒ 그림 8 의 결론 (평탄) 은 흔들리지 않는다 — 어긋남은 기준점 표기다.
- 원문 경고 (p.7): *"Even though the stiffness of particles undergoing binary particle-particle collisions can be greatly reduced, studies by Kobayashi et al. [9] and Gu et al. [8] show that collisions involving larger agglomerates behave differently when the particle stiffness is reduced beyond a certain point. In this study, this phenomenon is addressed in the following section where particle deposition on both a clean surface and a surface with an initial layer of particles is investigated."* — 그러나 §5.3 은 **깨끗한 벽의 입자 하나**뿐이다 (입자 층 위 증착 없음 · §11).

### 3-5. ★ 벽 비스듬 충돌 · 붙음 경계 (그림 9–12 · 식 25 · §5.3 · p.7–8)
- 그림 9: 벽 쪽으로 ω 각 · 벽에 나란한 외력 F_ext → (e1) 되튐 · (e2) 붙어서 일정 각속도로 구름 · (e3) 붙어서 멈춤.  그림 10 (모식도): λ > λ_crit = 되튐 · 그 아래 F̂ < 1 = 멈춤 · F̂ ≥ 1 = 구름.  *"For most DEM simulations of particulate deposition, it is important that the outcome (rebound, rolling or sticking) remains the same when the particle stiffness is reduced."* (p.7).
- 이분법 · 수렴 기준 **\|δ_n/r_p\| = 10⁻⁷** (p.8 · `txt_p8_bisection_lambda_crit_c_of_e`).  ω ∈ ]0; π/2].
- **그림 11** [판독]: e 0.1–0.9 아홉 선 · Ad 10²–10³ · λ_crit 10⁴–10¹² · **기울기 2.5000–2.5003** · **식 (25) λ_crit = c·Ad^{5/2}** · *"where the value of c is solely a function of the coefficient of restitution e"*.
- **그림 12 c(e) [판독 · 벡터 네모 중심]**:

| e | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
|---|---|---|---|---|---|---|---|---|---|
| c | 5,365 | 584.6 | 147.3 | 50.96 | 20.44 | 8.666 | 3.613 | 1.336 | 0.3338 |

- 그림 11 선 절편으로 다시 낸 c 와 그림 12 점의 차 ≤ 0.05 % [카드 산술].
- **식 25 의 뜻 [카드 산술]**: λ/Ad^{5/2} = Eρ_p^{3/2}v³r_p^{5/2}/(3^{5/2}γ^{5/2}) ∝ (½mv² ÷ W_sep)^{3/2} (W_sep ∝ γ^{5/3}r^{4/3}E^{−2/3} · §3-2) → 경계 = **운동 에너지 ÷ 분리 에너지 일정 (e 마다)** · 식 24 로 E 와 γ 를 같이 바꾸면 W_sep 가 그대로라 경계가 그대로 — 식 25 의 지수 5/2 는 식 24 의 2/5 와 같은 말이다.
- 교차 검산 [카드 산술]: 그림 6 조건 (e 0.86 · 정면 ω = π/2) 에서 c(0.86) ≈ 0.609 (log c 를 e 0.7–0.9 세 점 이차 보간) → **v\* ≈ 2.37 m/s** ↔ 재계산 문턱 2.4005 m/s (그 점의 λ/Ad^{5/2} = 0.633 = c(0.86) 직접) · 5 m/s 정면 충돌의 λ = 1.06 × 10⁴ · Ad = 20.3.

### 3-6. ★ 충돌 시간 · 시간 간격 (그림 13 · §6.2 · p.9)
- 그림 13: PSL → 석영 · 5 m/s · E_mod/E = 10⁰ · 10⁻¹ · 10⁻² (γ 식 24).  원문 (`txt_p9_sec62_timestep_collision_time_scaling`): *"the separation velocity is unaffected by a change in particle stiffness when the surface energy density is modified using Eq. (24). However, the particle collision process now takes place over significantly longer time periods. When resolving a collision over fixed number of time steps (Silbert et al. [30] suggest Δtcol/δt ≈ 50), the time step size can now be greatly increased. … Δtcol,mod = Δtcol(E/Emod)^{2/5}"*.
- [판독]: 세 곡선 모두 **v_max 5.615 · v_min −4.879 · v_final −3.593 m/s** (e_eff 0.7186) · v = 0 시각 **0.008855 · 0.022242 · 0.055870 µs** (비 2.512 = 10^{0.4}) · 접촉 끝 ≈ 0.0188 · 0.0475 · 0.1192 µs (선 끝 · 표본 간격 한정).  닿은 직후 속도가 5 → 5.615 m/s 로 오른다 = 접촉 순간 인력 (8/9)F_C 로 끌려 들어감 [카드 해석].
- [카드 재계산]: v_max 5.6156 · v_min −4.8800 · v_final −3.5932 m/s · t(v = 0) 0.008855 · 0.022242 · 0.055869 µs — 판독과 넷째 자리까지 같다.
- 시간 간격 이득 [카드 산술]: (E/E_mod)^{2/5} = **2.51 (E_mod/E 0.1) · 6.31 (0.01) · 15.8 (10⁻³)**.

### 3-7. ★ 이 카드의 증명 — 왜 '정확히' 같은가 (자기 상사) [카드 산술 · 카드 재계산]
- 변환 **E → E/X · γ → γX^{−2/5}** (식 24): a ∝ (γ/E)^{1/3} → X^{1/5} · 겹침 δ ∝ a²/R → X^{2/5} · F_spring ∝ Ea³/R → X^{−2/5} · F_jkr ∝ √(γEa³) → X^{−2/5} · S_n ∝ E√(Rδ) → X^{−4/5} · 감쇠 계수 ∝ √(S_n m) → X^{−2/5} · 감쇠 힘 (계수 × 속도) → X^{−2/5} · 시간 δ/v → X^{2/5} · 가속도 δ/t² → X^{−2/5} = 힘/질량 ✓.  ⇒ 운동 방정식의 양변이 같은 배수로 옮겨지고 접촉 생성 · 끊김 (겹침 0) 기준도 그대로 → **δ(t) → X^{2/5}δ(t/X^{2/5}) · 속도 곡선은 시간축만 늘어남 · e_eff 정확히 같음** (그림 13 의 v_final 이 셋째 자리까지 같은 이유).  원문은 에너지 등식 (식 23) 만 보였다.
- 접선 (식 14–17): S_t ∝ G√(Rδ) → X^{−4/5} · 접선 변위 ∝ X^{2/5} → F_t ∝ X^{−2/5} ✓ · 마찰 한계 μ_s(F_N + 2F_C) 는 **F_C 에 γ_mod 를 쓸 때만** 같은 배수 — 원문은 식 17 의 F_C 가 원래 값인지 바뀐 값인지 적지 않았다 [미확인].
- 구름 (식 18–22 + §3.2): k_r = 4F_C(a/a₀)^{3/2} 에 **원래 F_C** · ξ_crit 에 **원래 a₀** → 평형 (a = a₀) 의 M_r · F_yield 그대로 = 멈춤 / 구름 **문턱** 보존 · 회전 동역학은 상사가 아니다 (구름 토크 ∝ X⁰ ↔ 접선력 토크 ∝ X^{−2/5}) → 멈출 때까지 굴러간 거리가 늘어난다 (원문 p.5 · p.9 와 같은 방향).
- **단순 JKR 의 이력 고리 = 0**: 닿을 때 (겹침 0 에서 인력 (8/9)F_C 로 뛰어듦) 와 떨어질 때 (겹침 0 에서 끊김) 가 같은 힘 경로 → 고리 넓이 0 → 소산은 감쇠뿐.  재계산: e → 1 (0.999999) 이면 **0.05 · 0.5 · 2.0 m/s 모두 되튐 (e_eff 0.977 · 0.999 · 1.000)** · e 0.86 이면 0.5 m/s 에서 붙음.  ⇒ 이 모델의 붙는 속도는 e (감쇠) 와 W_sep 가 같이 정한다 — JKR 원식의 이력 고리 (음의 겹침에서 목이 끊김 · `thorntonning1998_…` 의 V_s 식 54) 와 다른 기전 [카드 추론].

### 3-8. 인쇄 어긋남 (요약 — 자세히 §11)
식 11 의 √ 누락 · (A.10) 둘째 항 2 배 · 그림 4 캡션 선 모양 열쇠 반대 · 그림 7 캡션 ↔ 본문 Ad 정의 · 그림 7 ↔ 8 기준 λ 4 배 · F_yield 식의 /R 누락 · 초록의 구름 토크 기호 · §5.2 가 예고한 입자 층 증착 없음 · 그림 1 의 접촉 반경 'α'.

---

## 4. ★ 방법 — 수치 · 입자 처리

### 4-1. 수치 · 비용
- 적분: *"simulation results obtained by integrating Eq. (3)"* (p.5) — 적분기 · 시간 간격 · 코드 이름 [미확인].  시간 간격 지침은 Silbert [30] 의 Δt_col/δt ≈ 50 을 인용만 (p.9).
- 붙음 경계: 이분법 · \|δ_n/r_p\| = 10⁻⁷ (p.8).
- 런 수 (그림에서 셈 [판독]): 그림 6 계산선 꼭짓점 119 + 네모 33 + 가위표 33 · 그림 7 곡선 꼭짓점 55 · 62 · 40 · 33 (0.1 decade) · 그림 8 은 Ad 마다 7 점 · 그림 11 은 직선 아홉 (밑의 이분법 점은 안 그려짐).
- 계산 비용 · 입자 수: 단일 충돌이라 보고 없음 · 원문의 비용 주장은 시간 간격 배수 (E/E_mod)^{2/5} 하나.

### 4-2. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술** — 연화의 한계만 말한다: (a) *"the mechanistic models in DEM combined with high particle stiffness for most common materials require time step sizes in the order of nanoseconds, which makes DEM simulations impractical for more complex applications"* (초록 · `txt_p1_abstract`) (b) *"As each particle-particle collision is resolved over numerous time steps, the required computational time is high compared to other methods [6]"* (p.1) (c) 떼는 힘 감소 → *"care should be taken when introducing reduced particle stiffness to make sure that the critical force FC = 3πRγmod still remains significantly higher than typical external forces trying to separate the particles"* (p.9 · `txt_p9_sec62_critical_force_closepack_limit`) (d) *"for collisions involving many particles with a local volume fraction approaching the closed-pack solution, the adhesive behaviour might be changed slightly if the particle stiffness is reduced too much, Emod/E < 10−3 [8,9]"* (p.9) (e) 응집체 경고 (p.7 · §3-4) (f) *"the particles will travel longer distances upon collision due to the changed force-displacement relation"* (p.4–5) · 앞선 연구의 가정: *"Common for these studies is the fact that they assume particle deformation to play a negligible role on the adhesive force upon collision. This assumption is valid for sufficiently small particles, where particle deformation is negligible [10]. When the particle diameter is large (typically dp > 10 µm), particle deformation cannot be neglected when describing the adhesive force."* (p.2 · `txt_p1_p2_intro_stiffness_reduction_kobayashi_gu` · `txt_p2_large_particle_tabor_jkr_validity`).  단단한 구 · 점접촉 · 접촉 독립 · 형상 고정의 한계는 **말 없음**.
- **(ii) 소성 · 큰 변형 = 논의 없음** — 접촉은 탄성 (Hertz + JKR) · 소산은 점성 감쇠 하나 (e) · 원문의 'particle deformation' 은 접착에 기여하는 **탄성 접촉 변형** (Tabor) 뜻.  우회 = 없음 (해당 문제를 다루지 않음) · 맞춘 값 = 검증의 E · γ · e (Krijt [28]) · 비용 = 단일 충돌.
- **(iii) 차원**: 두 입자 / 입자–벽 **단일 충돌** — 식은 3D 벡터 꼴 (n · 토크 · 각속도) · 정면 충돌은 사실상 1D · 비스듬 충돌 + 구름 · 2D ↔ 3D 진술 없음.
- **(iv) 탈압**: 압밀 · 하중 제거 없음 — '떼는 힘' (분리) 과 충돌 되튐만 다룬다 (식 23 의 분리 에너지 · p.4 의 −(8/9)F_C,mod).

### 4-3. 기법 미니 용어집
- **JKR / DMT / Maugis** = 접착 접촉 이론의 세 극한 — 무르고 큰 입자 (Tabor λ_T > 3) 는 JKR (접촉 가장자리에 인장 · 목) · 단단하고 작은 입자 (λ_T < 0.1) 는 DMT (접촉 밖 인력) · 사이는 Maugis.
- **Tabor 매개변수 λ_T** = 접착이 만드는 탄성 변형 높이 ÷ 원자 간 거리 — 클수록 JKR 쪽.
- **단순 JKR (simplified JKR)** = JKR 의 힘–겹침 관계를 쓰되 **겹침이 0 보다 작아지면 바로 끊는** DEM 용 판 (JKR 원식은 음의 겹침에서 목이 늘다 끊김) — 이 논문 · Parteli [13] 등.
- **SJKR (LIGGGHTS cohesion sjkr)** = 인력 = 응집 에너지 밀도 CED (J/m³) × 겹침 면적 — 이 논문의 단순 JKR 과 **다른 꼴** (§7-3).
- **분리 에너지 (separation energy)** = 평형 겹침에서 겹침 0 까지 떼는 데 드는 일 (식 23).
- **접착 이력 Δγ/γ** = 붙일 때와 뗄 때 표면 에너지가 다른 정도 (구름 문턱 ξ_crit 의 재료 매개변수 · Krijt [4]).
- **구름 저항 토크 M_r** = 접촉 중심이 질량 중심 투영에서 밀려날 때 되돌리는 토크 · ξ_crit 넘으면 비가역 구름 (그림 2).
- **탄성 매개변수 λ** = E/(ρv²) (강성 ÷ 관성) · **접착 매개변수 Ad** = 3γ/(ρv²r) (접착 ÷ 관성) · **ê** = e_eff/e (접착이 줄인 반발 몫).
- **자기 상사 (self-similarity)** = 매개변수를 함께 바꿀 때 해가 축척만 바뀐 같은 꼴로 옮겨지는 것 (§3-7).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 두 접착 입자의 접촉 힘 (법선 스프링 · JKR · 감쇠 · 접선 스프링 · 감쇠 · 겹침 δ · 접촉 반경 'α') | 접촉 힘 분해 그림 (보고서 DEM 절) |
| 2 (a · b) | 벽 위 평형 입자 — 외력 없음 (중심 일치) · 외력 있음 (접촉 중심 ↔ 질량 중심 투영 어긋남) | 구름 저항의 뜻 |
| 3 | ★ 힘–겹침: 원 모델 · 강성만 낮춤 · 강성 + 접착 낮춤 (E_mod/E = 0.1 로 그려짐 [판독]) | **우리 F₀ 보존 = '강성만 낮춤' 곡선** (§7-3) — 떼는 힘 그대로 · 평형 겹침 × 10^{2/3} |
| 4 | ★ 구름 토크–구름 거리: 같은 세 경우 (E_mod/E = 0.1 [판독]) · ⚠ 캡션 선 모양 열쇠 반대 | 구름 문턱 보존 처방의 그림 |
| 5 | 두 입자 충돌 단계 (접근 → 최대 겹침 → 분리 → 붙음 e1 / 떨어짐 e2) | U5 시험 꼴 |
| 6 | ★ Dahneke PSL → 석영 실험 ↔ 계산 (E_mod/E 10⁰ · 10⁻¹ · 10⁻²) | 결과 전 대조 꼴 · 연화 규칙 회귀 시험 (계산 세 줄이 겹쳐야 함) |
| 7 | 수정 없는 모델: ê vs λ (Ad 5–40 · e 0.3) | 연화만 하면 반발이 바뀐다는 그림 · λ/Ad^{5/2} 로 붕괴 (§3-4) |
| 8 | ★ 식 24 적용: ê vs E_mod/E (10⁻³–10³) 평탄 | 연화 규칙의 단위 시험 꼴 (U5) |
| 9 | 벽 비스듬 충돌 단계 · 결과 셋 (되튐 · 구름 · 멈춤) | 판 · 벽 접착 시험 꼴 |
| 10 | 결과 지도 모식도 (λ ↔ F̂) | 결과 지도 꼴 |
| 11 | ★ λ_crit vs Ad (e 0.1–0.9) — 기울기 5/2 | 붙음 경계의 무차원 꼴 |
| 12 | ★ c(e) | 붙음 경계 계수 (벽 · 단순 JKR · 이 감쇠 꼴 한정) |
| 13 | ★ 5 m/s 충돌 속도–시간 (E_mod/E 10⁰ · 10⁻¹ · 10⁻²) | **회귀 시험 표적**: v_final −3.593 m/s · 시간축 10^{0.4} 배 |
| 식 크롭 36 장 | `eq_01_*` … `eq_25_*` (식 1–25 하나씩) · `eq_A01_*` … `eq_A11_*` (부록 A) | 보고서 접촉 법칙 절 · 연화 규칙 유도 |
| 근거 문단 16 장 | `txt_p1_*` (초록 · 연화 동기 · Kobayashi · Gu) · `txt_p2_*` (Tabor · JKR 범위 · 목적 · 단순 JKR) · `txt_p3_p4_*` (구름 모델) · `txt_p4_*` (식 24 동기 · Gu 같은 기준 · 떼는 힘 감소 · 구름 처방) · `txt_p5_*` (Krijt 맞춤값 · 무차원) · `txt_p7_*` (반발 변화 · 응집체 경고) · `txt_p8_*` (이분법 · 식 25 · 요약) · `txt_p9_*` (시간 간격 · 떼는 힘 · 10⁻³ 경고) | 원문 인용용 |

## 6. Post-processing ★
- **원문이 한 것**: 단일 충돌 적분 → e_eff · ê · 붙음 / 되튐 / 구름 분류 · 이분법으로 λ_crit · 로그 축 직선 맞춤 (식 25) · c(e).
- **안 한 것**: 다입자 · 침대 · 응집체 계산 · 시간 간격을 실제로 키운 비용 비교 · 접선 · 구름 매개변수 (μ_s · Δγ/γ · ν) 값 보고 · 식 17 의 F_C 선택 · 해상도 (δt) 수렴.
- **이 카드의 후처리**: PDF 벡터 경로 좌표로 그림 3 · 4 · 6 · 7 · 8 · 11 · 12 · 13 판독 (806 행 · 축 눈금 직선 보정 · 그림 11 격자 log 잔차 ≤ 10⁻⁵) · 그림 7 의 λ/Ad^{5/2} 붕괴 · 그림 7 ↔ 8 대조 · 그림 11 ↔ 12 대조 · 분리 에너지 적분 (닫힌 꼴 C ≈ 14.61) · 식 (7)–(13) 정면 충돌 재계산 (그림 6 · 13 재현 · 식 11 판별 · 이력 0 확인) · 자기 상사 증명 · SJKR 판 유도 (§7-3).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 정본 카드의 우리 쪽 표기를 출처와 함께 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 연화의 목적 | 시간 간격 (접착 마이크론 입자 · 나노초) | 압축 DEM = 기공 보정 (E_eff 1.35 GPa · 18 배 · 재배열 · 입계 미끄럼 · 미세 파괴의 대리 — CLAUDE.md frame[2]) · 믹서 = 시간 간격 + 겹침 천장 (SE 1×10⁷ Pa · AM 1.037×10⁹ Pa — `alizadeh2018_…` L222 · `johnson1971_…` §7-1) | 압축 연화는 **보정**이라 이 논문의 '결과 불변' 규칙과 목적이 다르다 · 믹서는 같은 목적 |
| 접착 꼴 | 단순 JKR (식 8–10 · 겹침 < 0 끊김) | 압축 = hooke/hysteresis + adhesion 강성 (Luding 식 6 꼴 · `luding2008_…` §7.1) · 믹서 = Hertz + SJKR (CED × 겹침 면적) | **셋 다 다른 꼴** — 지수 2/5 는 단순 JKR 의 것 |
| 강성을 바꿀 때 지킨 양 | **분리 에너지** (γ^{5/3}/E^{2/3}) | 믹서 = **떼는 힘 F₀ · Bo_code** (CED ∝ E\*^{2/3} · `johnson1971_…` §7-1 ② · `alizadeh2018_…` L236) · 압축 = [미확인] (adhesion 강성을 E 와 어떻게 정했는지 이 카드에서 확인하지 않음) | 믹서는 이 논문 그림 3 의 '강성만 낮춤' 쪽 |
| 연화 배수 | 검증 10⁻¹ · 10⁻² · 시험 10⁻³–10³ · 경고 < 10⁻³ (조밀) | 압축 SE 1.35/24 = 0.056 · 믹서 SE 1×10⁷/22.06×10⁹ = **4.5×10⁻⁴** (ref 2×10⁸ = 9.1×10⁻³) · AM 1.037/140 = 7.4×10⁻³ [카드 산술] | 믹서 soft SE 는 **경고 문턱 10⁻³ 아래** (조밀 흐름) |
| 시험 | 단일 충돌 반발 · 붙음 경계 · 구름 문턱 | 믹서 E0 정지 벽 계약 · 겹침 천장 1 % (CLAUDE.md 믹서 절) · 압축 = 기공 · 두께 | 우리에게 **단일 충돌 회귀 시험이 없다** → U5 (§8) |
| 소성 | 없음 | 압축 DEM = 접촉 소성 (hysteresis) · MPM = 입자 소성 (σ_y 0.30 · ν 0.49) | 이 논문은 소성 축에 아무것도 주지 않는다 |
| 차원 · 규모 | 단일 충돌 (식 3D 벡터) | 3D 침대 (DEM ≈ 수만 입자 · 믹서 100,000) | 침대 거동 (응집체 · 조밀 흐름) 은 이 논문 밖 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl | 300 MPa | **1.64** (고정) | **10–13 %** |
| 이 논문 | PSL ⌀1.27 µm · 무차원 | 압력 없음 (단일 충돌) | 없음 | **없음** |
- 이 논문은 기공 · 밀도 · 압력 자료가 없다 — "랩 표준과 다른 문헌 값" 의 자리도 비어 있다.

### 7-3. ★ 우리 믹서 SJKR (CED) 에 옮기면 — 에너지 불변 ↔ 힘 불변 [카드 산술 · 이 논문 밖]
- SJKR (`johnson1971_…` §7-1: 인력 2πR\*·CED·δ · 반발 (4/3)E\*√R\*δ^{3/2}) 의 평형 겹침 δ_eq = (9/4)π²R\*CED²/E\*² · 떼는 힘 F_po = (2/3)π³R\*²CED³/E\*² (그 카드 · `deng2021_…` L252 와 같은 식) · **분리 에너지 W_sep,SJKR = ∫₀^{δ_eq}(인력 − 반발)dδ = (81/80)π⁵R\*³CED⁵/E\*⁴** (수치 적분과 비 1.000000).
- E\* → E\*/X 에서 W_sep 을 지키려면 **CED ∝ E\*^{4/5}** · 그때 δ ∝ X^{2/5} · 힘 ∝ X^{−2/5} · 시간 ∝ X^{2/5} — 이 논문의 단순 JKR 과 같은 축척 (LIGGGHTS Hertz 감쇠도 √(S_n m) 꼴이면 감쇠까지 정확히 상사) · 떼는 힘 F_po ∝ X^{−2/5}.
- 우리 F₀ 보존 (CED ∝ E\*^{2/3}) 이면 떼는 힘 · Bo_code 는 그대로 · **W_sep,SJKR ∝ E\*^{−2/3}** — 이 논문 그림 3 의 '강성만 낮춤' 과 같은 쪽.
- ⚠ 이름 주의: `johnson1971_…` §7-1 ② 의 *'F₀ 보존 규칙 = W 보존'* 의 W 는 JKR **접착 일** (W = 2γ · 표면 성질) — 이 논문의 'γ 그대로' 와 같은 말이다.  이 카드의 W_sep (이 논문 식 23 의 **분리 에너지** = 평형 접촉을 떼는 일 · E 에 걸림) 과 다른 양이다 — 두 문장은 서로 어긋나지 않는다.
- 차원 해석: SJKR + 같은 감쇠 꼴의 정면 충돌은 Π = m v² A⁴/B⁵ (A = (4/3)E\*√R\* · B = 2πR\*CED · Π ∝ 운동 에너지 ÷ W_sep) 와 e 만의 함수 → 붙는 속도 v\* ∝ √(W_sep/m).
- **숫자 (SE–SE · 쌍 R\* 37.75 µm 의 parcel)**: soft E → ref ×20 에서 F₀ 규칙 CED 10,458 → 77,057 J/m³ (×20^{2/3} = 7.37 · `johnson1971_…` §7-1 표) ↔ 에너지 규칙이면 → **≈ 114,900 J/m³ (×20^{4/5} = 10.99 · F₀ 규칙의 1.49 배)** · F₀ 규칙 아래 ×20 경화의 W_sep,SJKR × **0.136** · 붙는 속도 × **0.37** (감쇠 고정).
- 연화 쪽으로 보면: 믹서 soft SE (E_mod/E ≈ 4.5×10⁻⁴) 에 이 논문 규칙 (에너지 보존) 을 쓰면 떼는 힘이 실물의 **0.046 배** (= (4.5×10⁻⁴)^{2/5}) — 힘 보존 (F₀) 과 에너지 보존은 우리 연화 배수에서 **22 배** 갈린다.
- ⇒ **어느 불변량을 지킬지가 결과를 바꾼다** — `alizadeh2018_…` L236 (insight 3) 의 결정을 이 논문이 JKR 꼴로 엄밀하게 준다.  논지 (`docs/hetero_thesis.md` §2-4 '살아남는 접촉 = 충돌 에너지 ↔ 접착 에너지' — 그 카드 L236 이 적은 대로) 가 맞다면 에너지 쪽이 직접 불변량일 수 있다 [추정] · 결정 = 등록 문서 몫.

### 7-4. 우리 압축 DEM (18 배 연화 · hooke/hysteresis) 에 옮기면 [카드 산술 · 카드 추론]
- 압축 덱 = 선형 스프링 꼴 (Luding 식 6 · k₁ · k₂ · k_c) — 이 논문의 2/5 는 Hertz + JKR 의 것이라 **그대로 옮겨지지 않는다**: 선형 꼴의 불변량 (k_c/k₁ 등 비) 을 따로 세워야 한다.
- 만약 Hertz + JKR 꼴이었다면 (참고만): E 24 → 1.35 GPa (÷17.78) 에서 에너지 규칙 γ × 0.316 · 충돌 시간 × 3.16 · 평형 접촉 반경 × 1.78 (γ 그대로면 × 2.61) · 붙는 속도 (γ 그대로) × 2.61 (`thorntonyin1991_…` 비교 문서 줄의 ×2.62 와 같은 산술).
- 시간 간격 배수는 기준에 따라 다르다: Hertz 충돌 시간 (이 논문) 17.78^{2/5} = **3.16** ↔ Rayleigh 기준 √17.78 = **4.22** (`paulick2015_…` L127 · L129).
- 이 논문의 '결과 불변' 규칙은 **연화를 수치 장치로 쓸 때** 의 것 — 우리 압축 연화는 보정 (기공 맞춤) 이라 '원래 결과를 지킨다' 는 기준점이 없다 (실물 E 의 DEM 은 기공을 못 맞춘다 · frame[2]).  ⇒ 압축 DEM 에는 규칙이 아니라 **한정어** 로만 온다: 연화 DEM 의 SE–SE 접착값은 연화 E 에 묶인 모델 매개변수 [카드 추론].

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 단일 접촉 · 충돌 수준의 접착 동역학 (DEM 쪽 · 혼합 단계).
- **없는 것**: 침대 · 압밀 · 소성 · 형상 · 수송 · 다접촉 — 압축 MPM / DEM 반쪽 어디에도 직접 값을 주지 않는다.  주는 것은 **연화 + 접착의 짝 규칙과 그 시험 꼴**.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 없음 (기공 · 밀도 없음) — 등록 칸 하나만: 연화 E 를 쓰는 계산이면 **'점착 매개변수를 어느 불변량으로 정했나'** (떼는 힘 ↔ 분리 에너지) 를 결과 전에 적는다 | 기공 연산자 · 판정 기준 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 접착 · 분리를 넣을 때의 해석 기준 꼴: 떼는 힘 (8/9)·3πRγ (단순 JKR) · 분리 에너지 W_sep ≈ 14.61γ^{5/3}R^{4/3}E^{−2/3} [카드 산술] | MPM 접촉 · 점착 (`--coh`) 은 응력 꼴이라 직접 대응 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 원칙 하나: 연화한 강성에 붙는 접착값은 강성과 **짝** 으로 정해야 같은 충돌을 낸다 (식 24) → 순수 SE 보정에 점착을 함께 쓰면 R5 (맞추는 값 하나) 와 충돌하는지 등록 | 압밀 · 기공 · σ_y 없음 |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 떼는 힘의 축척: 에너지 규칙이면 떼는 힘 ∝ (E_mod/E)^{2/5} (우리 압축 배수면 0.316 · 믹서 soft SE 면 0.046 [카드 산술]) → 탈압 · 판 분리에서 SE–SE 접착이 남는지 볼 때 **연화 모델의 떼는 힘이 실물보다 작다** 는 한정어 | 침대 탈압 · 되돌아옴 자료 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 | — |
| **후보 D0** (지금 DEM) | (1) 연화 + 점착의 짝 규칙 (JKR: γ ∝ E^{2/5}) 과 그 '꼴마다 다른 지수' 경고 (SJKR 4/5 · 선형 [미확인]) (2) 단순 JKR · SJKR 은 접착 이력 고리 0 → 붙음은 감쇠가 정한다 [카드 재계산] (3) 연화 배수 경고 E_mod/E < 10⁻³ (조밀 · [8, 9]) — 믹서 soft SE 4.5×10⁻⁴ 가 걸린다 | 압밀 체제 (조밀 · 300 MPa) 의 근거 아님 · 경고 문턱의 수치 근거는 [8, 9] 원문 [미확인] |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 판 · 벽 접착 시험 꼴 (그림 9–12: 되튐 · 구름 · 멈춤 지도 · λ_crit = c(e)Ad^{5/2}) | MPM 판 접착 규칙 아님 |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 연화와 함께 바꿀 양의 지수를 꼴마다 세우는 법 (분리 에너지 · 시간 축척) — Thornton–Ning 꼴로 넓히면 항복 속도 V_y ∝ (p_y⁵/E\*⁴)^{1/2} (`thorntonning1998_…` 식 10) 를 지키려면 p_y ∝ E\*^{4/5} [카드 산술 · 이 논문 밖] | 소성 접촉 법칙 · 캡 값 없음 |
| **후보 M0** (균질화 압밀 · Heckel · 캡) | 없음 | — |
| **U0–U6** | ★ **U5** (비슷한 강성 입자 충돌): 그림 8 · 13 꼴 — 같은 매개변수를 E_mod/E 1 · 0.1 · 0.01 로 돌려 v_final 같음 · 시간축 10^{0.4} 배 (PSL–석영 5 m/s: v_final −3.593 m/s · v_max 5.615 · t(v = 0) 0.008855 µs) · **U0**: γ → 0 이면 e_eff = e (접착 없음과 같음) · **U4** (판 분리): 떼는 힘 (8/9)F_C (단순 JKR) · F_po (SJKR) 해석값 대조 | U1 · U2 · U3 · U6 없음 |
| **R1–R7** | **R5** (맞추는 값은 모델마다 하나): 검증의 E · γ · e 셋이 맞춤값 (Krijt) — γ_mod 는 맞춘 값이 아니라 식 24 로 **유도** · **R2** (미끄럼 · 분리): 식 17 μ_s(F_N + 2F_C) — 연화 때 F_C 선택 [미확인] · **R4** (탈압): 떼는 힘 축척만 | R1 · R3 · R6 · R7 없음 |
| **결과 전 대조 항목** | 그림 6 Dahneke 138 점 (PSL–석영 · 맞춤값과 함께) · 그림 13 속도 곡선 · 그림 12 c(e) — **접착 충돌 코드의 회귀 표적** (재료 값 전이 금지) | LPSCl · NCM 충돌 자료 아님 |

- **재료 · 차원 · 조건 차이**: PSL (고분자) ⌀1.27 µm ↔ LPSCl (E 22.06 GPa · DFT) · NCM (≈ 140 GPa) · 단일 충돌 ↔ 3D 침대 · 압력 없음 ↔ 300 MPa · 단순 JKR ↔ SJKR / hooke/hysteresis.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **강성을 바꾸는 덱마다 '지킨 불변량' 칸** — 믹서 SE ref ×20 · ×40 · 압축 ÷18 의 등록 문서에 떼는 힘 (F₀ · Bo) ↔ 분리 에너지 (Coh · 붙는 속도) 중 무엇을 지켰는지 적는다: JKR 에서 둘은 (E_mod/E)^{2/5} 만큼 갈리고 우리 믹서 배수에서는 떼는 힘 기준 22 배 차이 (§7-3).
2. **SJKR 판 지수는 4/5** — 믹서에서 에너지를 지키고 싶으면 CED ∝ E\*^{4/5} (F₀ 규칙 2/3 아님 · ×20 에서 1.49 배 차) [카드 산술 · 이 논문 밖 — 단위 시험으로 확인 전].
3. **단일 충돌 회귀 시험 (U5)** — 그림 13 꼴: 같은 입자쌍을 E 배수 셋으로 충돌시켜 v_final 이 같고 시간축이 X^{2/5} 로 늘어나는지 — 연화 규칙 · 감쇠 꼴 · 접착 구현을 한 번에 점검 (SJKR 이면 CED ∝ E\*^{4/5} 에서 같아야 함).
4. **붙음은 감쇠가 정한다 (단순 JKR · SJKR)** — 이력 고리가 0 이라 SE–SE '붙는 속도' 는 e 에 강하게 걸린다 → 붙는 속도 산술 (dev-u 의 18.7 · 46.6 mm/s — CLAUDE.md) 에 e · 감쇠 꼴을 같이 적는다 [카드 추론].
5. **연화 배수 경고 10⁻³** — 믹서 soft SE (4.5×10⁻⁴) 는 원문이 조밀 충전에서 접착 거동이 바뀔 수 있다고 한 범위 — 근거는 [8, 9] (카드 없음 · §12) 라 크기는 모른다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "When the particle stiffness of a Hertz–JKR DEM model is reduced from E to E_mod, the surface energy must be reduced to γ_mod = γ(E_mod/E)^{2/5} to keep the separation energy — and hence the sticking/rebound outcome — unchanged; the pull-off force then drops to (8/9)·3πRγ_mod (Hærvig et al., Powder Technol. 319 (2017) 472)."
- "Collision duration scales as Δt_col,mod = Δt_col(E/E_mod)^{2/5} under this rule (Hærvig et al. 2017, Fig. 13); the authors caution that for near close-packed local volume fractions the adhesive behaviour may change for E_mod/E < 10⁻³."
- 국문: *"연화 DEM 의 표면 에너지는 강성과 짝으로 정해지는 모델 매개변수다 — Hertz–JKR 에서 같은 충돌 결과를 내려면 γ ∝ E^{2/5} (Hærvig 2017)."*
- 국문: *"강성을 낮출 때 떼는 힘을 지키느냐 분리 에너지를 지키느냐에 따라 접착 매개변수가 (E_mod/E)^{2/5} 배 갈린다 (Hærvig 2017 식 24 · 이 카드 산술)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **단일 충돌만** — §5.2 끝 (p.7) 이 *"particle deposition on both a clean surface and a surface with an initial layer of particles is investigated"* 라고 예고하지만 §5.3 은 깨끗한 벽의 입자 하나뿐 · 응집체 · 조밀 충전 경고는 [8, 9] 인용으로만.
2. **식 (11) F_damp,n = −2(5/6)β√(S_n m)v_n** — 식 16 은 −2√(5/6)β… · 그림 6 · 13 은 √ 가 있어야 재현된다 (√ 없으면 e_eff 0.7428 ↔ 그림 0.7186) [카드 재계산].
3. **(A.10)** 둘째 항 2√(γπ)/√(Ea) — (A.9) 의 미분은 √(γπ)/√(Ea) · (A.11) 결론은 영향 없음 (두 항이 같은 축척) [카드 산술].
4. **그림 4 캡션** 의 선 모양 열쇠 (점선 = 강성만 · 파선 = 둘 다) 가 그림 안 범례 (파선 = 'Reduced stiffness' · 점선 = 'Reduced stiffness and adhesiveness') 와 반대 — 그려진 곡선은 범례와 맞다 (파선 = 같은 기울기 · 구름 거리 × 10^{1/3} = 강성만) [판독].  그림 3 은 캡션 · 곡선이 맞다.
5. **Ad 정의 둘** — 그림 7 캡션 γ/(ρ_p v² R) ↔ §5.1 3γ/(ρ_p v² r_i)·(1 + β³)/((1 + β²)β) (β 미정의 · 감쇠 β 와 같은 글자) · 같은 두 구에서 2/3 배.
6. **그림 8 ↔ 그림 7** — *"retains the values from λ = 10⁶ in Fig. 7"* 인데 평탄값은 그림 7 의 λ = 2.50×10⁵ 값 (차 0.05 · 0.12 · 0.38) [판독 · 카드 산술].
7. **F_yield = 4F_C a₀(Δγ/γ)/12** (p.6 · 그림 10 캡션) — F_yield = M_r/R 라 했으니 /R 이 빠졌다 (차원 = 토크) [카드 산술].
8. **초록의 구름 토크** *"Mr,mod = −4FC(a/a0)3/2ξ"* — 고친 꼴 (a_mod/a₀,mod)^{3/2} 를 말하는 문장인데 기호가 원래 꼴 · 부호 (−) 는 본문 식 21 에 없다.
9. **식 17 의 F_C · 식 19 의 t_r** — 연화 때 어느 F_C 를 쓰는지 · t_r 이 무엇인지 정의 없음.
10. **맞춤값 의존** — E 271 MPa · γ 0.11 · e 0.86 은 Krijt [28] 의 맞춤 (SI 미수령) · 실물 PSL · 석영 물성 · Tabor 값은 원문에 없다 (λ_T 45.3 은 이 카드 산술).
11. **10⁻³ 경고의 근거** — *"might be changed slightly"* 의 크기 · 조건은 [8, 9] 원문에 있을 것 [미확인].
12. **그림 1** 의 접촉 반경 기호 'α' (본문 a) · *"it is important that the particles will deposit predicted by the original model"* (p.4 · 문장 불완전).
13. ⚠ **판독 값** 은 벡터 좌표 (래스터보다 정밀) 이지만 원문 수치가 아니다 — [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 8 | Y. Gu, A. Ozel, S. Sundaresan, A modified cohesion model for CFD-DEM simulations of fluidization, Powder Technol. 296 (2016) 17–28. http://dx.doi.org/10.1016/j.powtec.2015.09.037 | vdW 판 같은 기준 (식 24 = Gu) · E_mod/E < 10⁻³ 조밀 경고의 근거 · 응집체 거동 변화 | 없음 (papers/ ls · DOI grep) |
| 9 | T. Kobayashi, T. Tanaka, N. Shimada, T. Kawaguchi, DEM-CFD analysis of fluidization behavior of Geldart Group A particles using a dynamic adhesion force model, Powder Technol. 248 (2013) 143–152. http://dx.doi.org/10.1016/j.powtec.2013.02.028 | 접착력 ∝ √(k_mod/k) 규칙 (힘 축척의 다른 판) · 응집체 경고 | 없음 |
| 28 | S. Krijt, G. Güttler, D. Heißelmann, C. Dominik, A.G.G.M. Tielens, Energy dissipation in head-on collisions of spheres, J. Phys. D Appl. Phys. 46 (2013) 435303. http://dx.doi.org/10.1088/0022-3727/46/43/435303 | 검증 맞춤값 (E · γ · e) 의 출처 · 맞춤 절차 | 없음 |
| 10 | K.L. Johnson, J.A. Greenwood, An adhesion map for the contact of elastic spheres, J. Colloid Interface Sci. 192 (1997) 326–333. http://dx.doi.org/10.1006/jcis.1997.4984 | JKR · DMT · Maugis 영역 지도 (λ_T) — 우리 SE–SE 접착이 어느 영역인지 | 없음 |
| 13 | E.J.R. Parteli, J. Schmidt, C. Brümel, K.-E. Wirth, W. Peukert, T. Pöschel, Attractive particle interaction forces and packing density of fine glass powders, Nat. Sci. Rep. 4 (2014) 1–7. http://dx.doi.org/10.1038/srep06227 | 단순 JKR 의 출처 · 접착이 충전 밀도를 바꾸는 크기 | 없음 (hare2026 카드가 인용만) |
| 1 | K.L. Johnson, K. Kendall, A.D. Roberts, Surface energy and the contact of elastic solids, Proc. R. Soc. Lond. 324 (1971) 301–313. | JKR 원전 | `johnson1971_jkr_surface_energy_contact_elastic_solids` |
| 25 | C. Thornton, K.K. Yin, Impact of elastic spheres with and without adhesion, Powder Technol. 65 (1991) 153–166. | 식 17 (접착 마찰 한계) | `thorntonyin1991_oblique_impact_elastic_spheres_adhesion` |
| 27 | B. Dahneke, Further Measurements of the bouncing of small latex spheres, J. Colloid Interface Sci. 51 (1975) 58–65. | 검증 실험 원자료 | 없음 |
| 29 | S. Chen, S. Li, M. Yang, Sticking/rebound criterion for collisions of small adhesive particles: effects of impact parameter and particle size, Powder Technol. 274 (2015) 431–440. | Ad 정의 (β 의 뜻) | 없음 |
| 30 | L.E. Silbert, D. Ertas, G.S. Grest, T.C. Halsey, D. Levine, S.J. Plimpton, Granular flow down an inclined plane: Bagnold scaling and rheology, Phys. Rev. (2001) 051302. | Δt_col/δt ≈ 50 | 없음 (후보 표 S8 N-71) |
| 2 · 3 · 4 | C. Dominik, A.G.G.M. Tielens, Philos. Mag. A 72 (1995) 783–803 · Astrophys. J. 480 (1997) 647–673 · S. Krijt, C. Dominik, A.G.G.M. Tielens, J. Phys. D. Appl. Phys. 47 (2014) 175302. | 구름 저항 모델 (ξ_crit · k_r) | 없음 |

---

## [미확인] 목록
- 보충 자료 (그림 6 캡션의 *"supplementary online material for collision properties"*) — PDF 에 없음.  Krijt [28] 맞춤값의 나머지 (ν · Δγ/γ · μ_s · 벽 물성).
- 적분기 · 시간 간격 · 코드 이름 · 런 수 · 해상도 (δt) 수렴.
- 식 17 의 F_C (원래 ↔ 바뀐 값) · 식 19 의 t_r · §5.1 Ad 의 β · 그림 7 이 쓴 Ad 정의.
- 그림 7 ↔ 8 의 λ 4 배 어긋남의 원인.
- E_mod/E < 10⁻³ 경고의 크기 · 조건 ([8, 9] 원문).
- 실물 PSL · 석영의 E · ν · 표면 에너지 (원문 값은 맞춤값).
- 우리 압축 덱 hooke/hysteresis 의 adhesion 강성을 18 배 연화와 함께 어떻게 정했는지 (이 카드는 리포를 보지 않음).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-13)
- 서지: 후보 표 N-48 서지 (저자 일곱 · 제목 · Powder Technol. 319 (2017) 472–482) = 원문 첫 쪽 · 쪽 머리글과 같다 · DOI = 첫 쪽 하단 · PDF 메타데이터와 같다 · 다른 점 없음.
- 숫자: 텍스트 층 + 쪽 렌더로 대조 — 1.65 Å · λ_T > 3 · < 0.1 · 10 µm · 8/9 · 3πRγ · 5/6 · 2/5 · 1.27 µm · 271 MPa · 0.11 J/m² · 1026 kg/m³ · 0.86 · e 0.3 · λ 10⁶ · 10⁻⁷ · 0.1–0.9 · Δt_col/δt ≈ 50 · 10⁻³ · 1305-00036B — 전부 위치 확인.
- 보충 자료: 그림 6 캡션에 한 번 (*"supplementary online material"*) · 본문 다른 곳 0 회 · 표 0 개.
- 판독 보정: 각 그림의 축 눈금 · 격자선 벡터 좌표로 직선 보정 (그림 11 격자 log 잔차 ≤ 10⁻⁵ · 그림 12 x 잔차 1.9×10⁻⁶) · 그림 6 · 13 은 식 재계산과 넷째 자리까지 일치 (판독 사슬 점검).
- 정본 중복 확인: papers/ 목록 · DOI `10.1016/j.powtec.2017.07.006` · 'haervig' · 'hærvig' · 제목 낱말 grep — 카드 없음 (alizadeh2018 이 인용만).  같은 저자 · 같은 해 다른 카드 없음.

## 🔗 관련 카드
- 이 논문을 인용한 카드: `alizadeh2018_dem_adhesion_calibration_segregation_heap` (ref 2 · L49 · L236 · L265).
- 접착 접촉 이론 · 충돌: `johnson1971_jkr_surface_energy_contact_elastic_solids` · `thorntonyin1991_oblique_impact_elastic_spheres_adhesion` · `thorntonning1998_adhesive_elastoplastic_contact` · `pasha2014_linear_elastoplastic_adhesive_contact` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` · `luding2008_cohesive_frictional_contact_models`.
- 구름 저항: `ai2011_rolling_resistance_contact_models_dem`.
- 연화 · 보정 인식론: `paulick2015_elastic_particle_properties_dem_review` · `vanlew2015_modifying_youngs_modulus_distribution` · `coetzee2017_dem_calibration_review` · `chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer`.
- 접착 보정 · 혼합 DEM: `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · `deng2021_mechanical_surface_energy_tester_bond_number` · `jarray2019_cohesion_driven_mixing_segregation_drum` · `boschpadros2014_dem_liggghts_msc_thesis` (LIGGGHTS SJKR 구현).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
