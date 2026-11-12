# batch_14 정독 근거 (카드 8 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `so2022_dem_compaction_coated_particles_assb` (236 줄) · `nisar2024_dem_effective_electrical_conductivity_sps` (302) · `doux2020_stack_pressure_assb` (374) · `sakuda2013_sulfide_mechanical_property` (261) · `lee2024_multiphysics_dem_fem_initial_pressure_assb` (430) · `kakar1967_deformation_theory_hot_pressing` (349) · `deysher2022_transport_mechanical_aspects_assb_review` (304) · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` (413). 끝까지 못 읽은 카드 없음 (kakar1967 은 두 번 · kang2026 은 세 번에 나눠 끝까지 읽음).

배치의 성격: **DEM 을 쓴 카드 셋** (so2022 = LPS + NCM 의 3D 냉간 압밀 · 접촉 소성 + 경도 캡 / lee2024 = LGPS + LLZO 의 DEM → FEM / nisar2024 = NiAl 소결체의 DEM 저항망), **실험 둘** (doux2020 = Li₆PS₅Cl 펠릿과 적층압 / sakuda2013 = Li₂S–P₂S₅ 유리의 밀도 – 압력 · 탄성률), **고전 이론 + 실험 하나** (kakar1967 = 납 · 사파이어 구), **리뷰 둘** (deysher2022 · kang2026 — 수치는 전부 2 차 인용). LPSCl (Li₆PS₅Cl) 자체를 잰 카드는 doux2020 하나뿐이고 370 MPa 한 점이다 (곡선 아님). MPM 을 쓴 카드는 없다. 압력을 뺄 때 되돌아온 두께 · 기공을 잰 카드도 없다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `digitized` · `판독` · `우리 산술` · `우리 유도` · `[미확인]` · "2 차 인용") · 없으면 "표지 없음". 따옴표 안 영어 문장은 카드가 옮겨 둔 원문이고, 카드가 한국어로 옮긴 요지는 "카드의 한국어 옮김" 이라고 따로 적었다. "카드의 풀이 · 우리 쪽 해석" = 논문 문장이 아니라 카드 작성자의 서술. "내 검산 · 내 산술" = 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님). "랩 표준과 다른 문헌 값" = 순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ 과 다른 값이라는 표시 (기준은 그대로다).

형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계` (k · l 은 slug 옆에 인용할 서지 · m 은 `무엇을 | 우리 쪽 어디에 | 근거 위치`)

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

순수 황화물 SE 의 압력별 곡선이 있는 카드 = **1** (sakuda2013 — 단 Li₃PS₄ 조성 **유리** 이고, 본문에 적힌 값은 한 점 · 나머지는 그림 판독). LPSCl 을 잰 카드 = **1** (doux2020 — 370 MPa **한 점** · 곡선 아님). 두 장 모두 밀도를 누른 채 쟀는지 뺀 뒤 쟀는지와 밀도 측정법이 카드에 없다.

- [a] sakuda2013_sulfide_mechanical_property | 순수 황화물 유리 (75Li₂S·25P₂S₅ = Li₃PS₄ 조성 유리) 의 상대밀도 – 몰딩 압력 (Fig 2a) 에서 본문이 적은 값은 하나: *"The relative density … exceeds 90 % when the 75Li₂S·25P₂S₅ glass powder is compressed by a pressure of over 350 MPa."* → 기공 < 10 % @ > 350 MPa | §3 L51 · §11-A L163–164 · 논문 p.2 | stated (본문) | LPSCl 아님 (유리) · 300 MPa 는 본문에 특정값으로 나오지 않음 (본문 명시 압력 = 70 · 74 · 350 · 360 MPa · L169)
- [a] sakuda2013_sulfide_mechanical_property | 같은 곡선의 그림 판독: ≈ 30 % (저압) → ≈ 50 % (≈ 30 MPa) → ≈ 60–65 % (≈ 75) → ≈ 75 % (≈ 150) → ≈ 80 % (≈ 200) → **≈ 85–88 % (≈ 300 · "≈ 87 %" → 기공 ≈ 12–15 %)** → ≈ 90 % (≈ 350) → ≈ 93–95 % (≈ 450) | §3 L52–53 · §5 L94 · §11-A L165–166 · Fig 2a | digitized (Fig 2a) · "추세만 · ± 몇 %p" | 카드: "stated 정밀값으로 인용 금지" · 판독값이 L53 과 L94 에서 조금 다름 (카드 문제 18) · 2026-10-21 원문 대조 때 다시 읽지 않음 (L213)
- [a] sakuda2013_sulfide_mechanical_property | 진밀도 (분모) · 질량 · 상태: 상대밀도 = ρ_coldpress ÷ ρ_hotpress · 분모 = 75Li₂S·25P₂S₅ 를 약 200 ℃ (Tg 근처) 로 열간 프레스한 **투명 유리 펠릿 1.88 g/cm³** (결정 밀도 아님) — *"The total relative density was determined using 75Li₂S·25P₂S₅ transparent glass prepared by hot pressing at about 200 °C (see Fig. 3b and Ref. 9); the density of the glass was 1.88 g cm⁻³."* · *"The density of hot press glass was almost the same as that estimated from the density of the crystal."* · 시료 = 10 mm 몰드 · 500 mg · 상온 단축 냉간 프레스 | §3 L54 · §4 L74–76 · §13-1 L216–221 · 논문 p.2 · p.5 | stated (p.2 · 원문 확인 2026-10-21) · 인용문 = verbatim | 밀도 측정법 (아르키메데스 · 치수 · 기체 치환) 미기재 · 누른 채 / 뺀 뒤 미기재 · 어느 결정상인지와 그 값 미기재 · 열간 프레스 펠릿의 남은 공극 몫 미상 (카드: 참 유리 밀도 ≥ 1.88) · 재료가 달라 랩 표준 (LPSCl 1.64 g/cm³) 과 견줄 값이 아님
- [a] doux2020_stack_pressure_assb | **순수 Li₆PS₅Cl (NEI 구매품 그대로) 펠릿 · 370 MPa 냉간 가압 한 점**: 펠릿 4 개의 상대밀도 80.3 / 84.9 / 80.3 / 83.0 % → 평균 82.1 % → 기공 ≈ 18 % · 이론밀도 1.860 g/cm³ 기준 · 실측 1.522 g/cm³ · 본문 *"A porosity of 18% within the electrolyte provides connecting pathways"* | §6 L202–204 · §9 L277 · SI Table S2 | 표지 없음 (Table S2 · 인용문은 카드가 "본문도 … 라 명시") | **랩 표준과 다른 문헌 값** (기공 18 % ↔ 10–13 % · 기준 밀도 1.860 ↔ 1.64 g/cm³) · 압력 한 점 (곡선 아님) · 밀도 측정법과 누른 채 / 뺀 뒤가 카드에 없음 · 내 검산: 1.522 ÷ 1.860 = 81.8 % (평균 82.1 % 와 0.3 %p 차 · 카드 문제 13) · 펠릿 = 분말 200 mg · 13 mm PEEK 다이 · 두께 ≈ 1 mm (L85–86 — 내 산술로 200 mg ÷ (13 mm 단면 × 1 mm) ≈ 1.51 g/cm³ 이라 실측값과 같은 자릿수)
- [a] doux2020_stack_pressure_assb | 같은 펠릿의 이온전도도 σ_ion = 2–2.5 mS/cm (EIS) | §2.1 L85–87 | 표지 없음 | 한 조건 (압력별 σ 아님)
- [a] so2022_dem_compaction_coated_particles_assb | 순수 SE 곡선 없음 — 복합 (LPS + NCM) 만. 카드: "relative-density 곡선은 MethodsX/So2021; 이 논문 본문엔 porosity-vs-P 풀곡선 없음" | §3.2 L72 | — | —
- [a] lee2024_multiphysics_dem_fem_initial_pressure_assb | 순수 SE 기공 곡선 없음 — SE 혼합 (LGPS + LLZO · LLZO 0 / 33 / 41 / 58 / 66 / 100 wt%) 의 punch 응력 곡선만 (LGPS 압축성 ≫ LLZO) 이고 기공 값은 카드에 없음. 밀도 입력 LGPS 2000 · LLZO 5500 kg/m³ | §3 L67 · §5 L205 · Fig 2 | 밀도 = stated | LGPS · LLZO (LPSCl 아님) · 모의
- [a] nisar2024_dem_effective_electrical_conductivity_sps | 해당 없음 (NiAl). 기공 정의만: 1 − ρ/ρ₀ (Archimedes) · ρ₀ 5910 kg/m³ | §3 L35 · L38 | stated | 금속
- [a] kakar1967_deformation_theory_hot_pressing | 해당 없음 (납 · 사파이어). 밀도 정의만: 압분체 무게 / 부피 ÷ 비중병 진밀도 — 하중을 걷고 꺼낸 뒤 | §0 L25 · §4-4 L165 · 논문 p.3227 | stated | 다른 재료
- [a] deysher2022_transport_mechanical_aspects_assb_review | 순수 SE 압력별 기공 자료 없음 (리뷰) | §3 L103–104 | — | —
- [a] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 순수 SE 압력별 기공 자료 없음 (리뷰). 인용만: "370 MPa 고압에서도 3D tomography 로 비-무시 불규칙 공동 확인" (Doux et al., ref 100) | §5.1 L126 · §9 L262 | 2 차 인용 | 값 없음 · ref 100 이 doux2020 카드와 같은 논문인지 카드에 없음 (카드 문제 40)

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

되돌아온 두께 · 기공을 잰 카드는 **이 배치에 없다**. 가까운 것 = 접촉 임피던스의 압력 이력 (doux2020) · 영구 변형만 재는 절차와 재적층 몫 분리 (kakar1967) · 접촉 법칙의 제하 분기 (lee2024 · so2022) · 사이클 뒤 재가압 회복 (리뷰 둘의 인용).

- [b] doux2020_stack_pressure_assb | 두께 되돌아옴은 재지 않음. 접촉의 이력: Li 대칭셀 임피던스 > 500 Ω (1 MPa) → ≈ 110 (5) → ≈ 50 (10) → ≈ 40 (15) → 35 (20) → 32 Ω (25 MPa) → 5 MPa 로 내리면 ≈ 50 Ω (처음 5 MPa 값의 절반 이하) = 비가역 | §4 L144–163 · Fig 4c | 본문 stated (L365–366) | Li/SE 계면 접촉 (흐르는 것은 Li 금속) — SE 펠릿의 두께 · 기공 회복이 아님 · 25 → 5 MPa 한 번
- [b] doux2020_stack_pressure_assb | 잰 방법: 3-ton 로드셀을 셀 축 아래에 둔 홀더로 적층압 0–220 MPa 를 실측 · 제어 (100 kN Instron 5982 로 교정) · 나사 조임으로 압력을 바꾸며 EIS · 전압을 같이 측정 | §2.2 L97–100 · Fig 2a | 표지 없음 | 변위 (두께) 측정은 카드에 없음
- [b] doux2020_stack_pressure_assb | 저자의 가정 (측정 아님): "5/25/75 MPa stack pressure 의 (펠릿 자체) 기계적 성질은 단락 메커니즘에 영향을 주지 않을 것으로 본다 — 펠릿은 이미 370 MPa 로 cold-press 되어 있기 때문." (카드의 한국어 옮김) | §8 L235–236 | 카드 표기 "본문 명시" | 370 MPa 에서 놓은 뒤 펠릿이 얼마나 되돌아왔는지는 카드에 없음
- [b] kakar1967_deformation_theory_hot_pressing | 되돌아온 양은 재지 않음 — 잰 것은 영구 변형: 납 압분의 영구 변형 = Instron 차트의 처음 · 끝 읽기 차 (초기 하중 10 lb 가 기준점 · 고온은 2 lb) · 접촉 평면은 하중을 걷고 꺼낸 구의 잔류 평면 (측각기) | §3-A L64 · §4-2 L145 · §10 L302 · 논문 p.3227 | stated | 납 · 사파이어 · 카드: "탄성 회복 논의 없음"
- [b] kakar1967_deformation_theory_hot_pressing | 소성 전 재적층 몫을 떼는 법 (유리 구 380–400 µ · 다이 지름 1.25 in × 높이 0.25 in · 총하중 1000 lb): 초기 하중 2 · 5 · 10 · 40 lb 별 잔류 변형을 0 하중으로 외삽 → **10 psi 에서 약 1.5 % 부피 변화** · *"This strain is attributed to restacking or repacking alone"* · 구리 구는 1.3–4.3 % @10 psi (Duffield & Grootenhuis [21]) | §3-A L63 · §4-3 L150 · 논문 p.3226–3227 | stated | 유리 · 구리 구 · 10 psi (카드 환산 0.069 MPa)
- [b] lee2024_multiphysics_dem_fem_initial_pressure_assb | 수치 없음. 접촉 법칙에 제하 분기만: 하중 F = min(K_nl·S, F_prev + K_nl·ΔS) · 제하 F = max(F_prev + K_nu·ΔS, λ·K_nl·S) · K_nu = K_nl/ε² (ε = 반발계수) — 제하 강성이 하중 강성보다 커서 잔류 겹침이 남는 꼴 | §4.2 L118–124 · 식 3 · 6 | stated (식) | 침대 수준의 되돌아온 두께 · 기공은 카드에 없음 · 외부압 0–100 MPa 는 FEM 경계 조건 (탈압 계산 아님) · λ 값 없음
- [b] so2022_dem_compaction_coated_particles_assb | 탈압 단계 없음 (위 벽 PID 로 목표 몰드압 유지). 접촉 법칙의 관련 부품: 평형 겹침 h_eq (영구 잔류 겹침) · F_spring < −F_th 에서 detachment (융착 / 코팅 박리) · detachment 때 F_th = 0 (같은 응집체가 아니거나 기존 융착이 끊긴 경우) | §4.1 L87–94 · §4.6 L124 · 식 5–7 | stated (식) | 침대의 되돌아옴 값 없음
- [b] deysher2022_transport_mechanical_aspects_assb_review | 되돌아옴 자료 없음. 관련 인용: 첫 수십 사이클 뒤 370 MPa 재가압 → 잃은 용량 상당 회복 (Li₃PS₄ + NMC · [121] Koerver) | §3 L81 | stated (인용) | 사이클 열화의 접촉 손실 (탈압 되돌아옴 아님) · 리뷰
- [b] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 되돌아옴 자료 없음. 관련 인용: 300 MPa 재가압 → 용량 상당 부분 회복 · 30 사이클 뒤 저주파 저항이 재가압으로 ≈ 1/3 (Fig 8a · b · ref 105) ; 사이클 중 적층압 변동 ≈ 3.8 MPa (Li–In 셀) ↔ ≈ 0.2 MPa (LTO 셀) (ref 120) | §5.1 L134 · §6.2 L172 | 2 차 인용 | 재가압 압력이 deysher 카드 (370 MPa) 와 다름 (카드 문제 36)
- [b] sakuda2013_sulfide_mechanical_property | 이 카드에 없음 | — | — | —
- [b] nisar2024_dem_effective_electrical_conductivity_sps | 이 카드에 없음 | — | — | —

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산

황화물 SE 의 항복 · 경도 · 크리프를 직접 잰 카드는 없다. 값이 있는 것 = DEM 입력 경도 (so2022: LPS 1.9 GPa · 인용값) · 탄성률 (sakuda2013: 유리 18–25 GPa) · Li 금속 항복 ≈ 0.8 MPa (doux2020 · deysher2022 의 인용) · CAM 항복 ≈ 100 MPa (kang2026 의 인용). **일축 항복 세기로의 환산은 어느 카드에도 없다.**

- [c] so2022_dem_compaction_coated_particles_assb | DEM 입력: H_SE (LPS) 1.9 GPa (McGrogan [7]) · H_AM (NCM) 11.2 GPa (Cheng [37]) · E_SE 24 GPa (Sakuda [8]) · E_AM 199 GPa (Cheng [37]) · ν 0.32 / 0.25 · 마찰 0.5 · 반발계수 0.5. 항복 문턱 F_th = min(H_i, H_j)·A_con (카드: "σ_yield ≈ H 근사") | §3.1 L43–49 · §4.1 L94 · Table 1 · 식 7 | stated (Table 1) | LPS (LPSCl 아님) · 접촉 평균 압력을 경도 H 로 둔 것이고 일축 항복 세기 환산은 카드에 없음 · 완화 시간 t_rel 값 없음
- [c] sakuda2013_sulfide_mechanical_property | 탄성률 (초음파 펄스법 · Tg 근처 열간 프레스 고밀도 펠릿 · 10 mm φ × 수 mm): xLi₂S·(100−x)P₂S₅ x = 50–80 에서 18–25 GPa · 75Li₂S·25P₂S₅ = 24 GPa · 50Li₂S·50P₂S₅ = 18 GPa (원문 p.3 인쇄는 "18 Pa" 오식) · 75Na₂S·25P₂S₅ = 18 GPa · Fig 5 점 ≈ 17.5 / 22 / 23.5 / 25 GPa @50 / 70 / 72 / 80 mol% | §3 L55–60 · §13-5 L256 · Fig 5 | stated · 네 점은 digitized (Fig 5) | 유리 (LPSCl 아님) · 항복 · 경도 · 크리프 값 없음 ("small-scale plasticity" 는 정성 설명 · L119) · 일축 항복 환산 없음
- [c] doux2020_stack_pressure_assb | Li 금속 항복강도 ≈ 0.8 MPa (Masias 외 / Tariq 외) · 그 위에서 creep · LePage 외: 상온 Li 항복은 creep 지배. 작동압 5 MPa 가 그 ≈ 6 배 · 75 MPa 가 ≈ 100 배 | §1 L72–75 | 표지 없음 (카드: "본문 인용") | Li 금속 값 — LPSCl 의 항복 · 경도 · 크리프 값은 카드에 없음 (카드: "creep 주체는 Li metal")
- [c] deysher2022_transport_mechanical_aspects_assb_review | Li 크리프 항복 ≈ 0.8 MPa (1–7 MPa 적층압에서 소성 + creep · [107] Masias) | §3 L94 | stated (인용) | Li 금속 · SE 값 없음 · 리뷰
- [c] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | CAM (Ni-rich 산화물) 항복강도 σ_y ≈ 100 MPa · 불균일 탈리튬에서 수 GPa 응력 (ref 111 계산) · CAM E 150–200 GPa (ref 101 / 102) · 황화물 SE E 20–30 GPa · Li 는 점성 거동 (diffusional creep · 정성) | §5.1 L127 · L138 · §5.2 L151 · §9 L258–261 | 2 차 인용 | 리뷰 인용값 · ≈ 100 MPa 의 원전 번호가 카드에 없음 · SE 항복 · 경도 없음
- [c] lee2024_multiphysics_dem_fem_initial_pressure_assb | 항복 · 경도 없음 (접촉에 항복 캡 없음). 탄성 입력 E: LGPS 37.2 · LLZO 150.3 · NMC 144 · graphite 1 · carbon black 80 GPa · ν 0.3 / 0.26 / 0.25 / 0.3 / 0.3 (LGPS / LLZO / NMC / graphite / CB) | §3 L59–64 · Table 1 | stated (Table 1) | LGPS · 저자 한계: FEM 이 항복 응력 초과 변형 / 파괴 미반영
- [c] kakar1967_deformation_theory_hot_pressing | 항복 · 경도 값 없음 (카드: "힘 · 경도 법칙은 없다 (순수 기하)"). 크리프와 닿는 절차: 사파이어는 순간 변형이 수 초 안에 둔화 → 30 s 만 유지 (확산 크리프가 아닌 소성 흐름 보장 목적) · 평면 크기 산포의 원인 가운데 하나로 "구 부위별 경도 차" | §3-A L65 · L67 · §4-4 L160 · 논문 p.3227–3228 | stated | 사파이어 1570–1700 ℃ · 납
- [c] nisar2024_dem_effective_electrical_conductivity_sps | 역학 값 (E · σ_y · ν) 본문 미보고 — 소결 모델 [43] 에 위임 | §3 L46 · §4 L63–64 | — | —

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

단단한 입자가 지는 하중 분율을 수로 준 카드는 **없다**. 닿는 것 = AM 손상과 그 위치 (so2022) · 혼합의 압밀 추세 (lee2024 · 수치 없음) · 리뷰의 원인 서술 (kang2026).

- [d] so2022_dem_compaction_coated_particles_assb | 하중 몫 수치는 없음. 관련 결과: (i) AM 손상 f^AM = AM–AM 융착 결합의 상대 감소율 (식 9) ≈ 12 % @500 MPa (혼합 ≈ 코팅) (ii) 위치별: 위 · 아래 벽 (집전체 · SE 층 경계) 근처 ≈ 25 % ↔ 가운데 ≈ 5 % @360 MPa (iii) AM–AM 융착 결합 4.2 × 10⁴ → 3.7 × 10⁴ (0 → 500 MPa) (iv) 코팅 쉘이 AM–AM 접촉을 가림: AM 퍼콜 부피 ≈ 0.3 @25 MPa → ≈ 1.0 @100 MPa | §3.2 L63 · L66–67 · L70 · §4.4 L112–113 · Fig 4c · 6 | 12 % · 0.3 → 1.0 = stated · 나머지 digitized | LPS + NCM · 손상 정의가 융착 결합 감소율 (깨진 입자 수 아님) · 시드 1 개로 보임
- [d] lee2024_multiphysics_dem_fem_initial_pressure_assb | (i) SE 혼합에서 LGPS 가 LLZO 보다 훨씬 압축됨 · 고압축성 상 (LGPS 66 wt%) 이 압밀 개선 (Fig 2) (ii) 양극 혼합이 NMC 단독보다 압밀이 잘 됨 — 작은 입자가 큰 공극을 채움 (Fig 3b) (iii) graphite 를 과하게 넣으면 응력이 분산돼 불완전 압밀 (Fig 3e) (iv) 위 punch · 아래 punch 응력을 따로 그림 | §5 L205–206 | 표지 없음 (그림 설명) | LGPS · LLZO · graphite (E 1 GPa) · 하중 몫 · 기공 수치는 카드에 없음 · 재밍 판정 없음
- [d] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 리뷰 서술: 냉간 가압 뒤 공동이 남는 원인 ③ = 변형 거동 불일치 — 단단한 산화물 CAM (E 150–200 GPa) ↔ 무른 황화물 SE (E 20–30 GPa) → "SE 는 소성변형하나 CAM 강성 수용 못 함 → 구조 불균일 잔존" (카드의 한국어 옮김) · 원인 ② = 불균일 가압 → 국소 force concentration + 가압 방향에 수직으로 남는 공동 · NCM 비 ↑ → 응력 국소화 · 인장 / 압축 기울기 (Fig 11a · ref 37) | §5.1 L124–128 · §6.1 L166 | 2 차 인용 | 하중 몫 수치 없음 · Fig 11a 는 80 % 방전 상태의 응력 (가압 아님)
- [d] kakar1967_deformation_theory_hot_pressing | 단분산 한 재료라 혼합 없음. 재배열 실측만: 납 상온 a/R = 0.15 에서 밀도 곡선 급변 = 미끄러짐 (Z 곡선 단절과 같은 자리) · Z ≈ 7.6 → 9–10 · 결론 (a) 하중 즉시 입자 미끄러짐 (b) 재배향 · 재적층이 변형 내내 계속 | §3-A L68 · L71 · §3-B L78 · 논문 p.3228–3230 | stated · Z 는 판독 | 납 · 단분산
- [d] sakuda2013_sulfide_mechanical_property | 이 카드에 없음 (Fig 6a 는 SE 코팅이 부피 변화의 버퍼라는 모식뿐 · L99) | — | — | —
- [d] doux2020_stack_pressure_assb | 이 카드에 없음 | — | — | —
- [d] nisar2024_dem_effective_electrical_conductivity_sps | 이 카드에 없음 (단상) | — | — | —
- [d] deysher2022_transport_mechanical_aspects_assb_review | 이 카드에 없음 | — | — | —

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값의 수

범위를 수로 준 것 = kakar1967 (구 반지름이 안 자라는 구간 a/R ≤ 0.25 · 접촉끼리 닿는 임계 밀도 — 단 1967 년 기하 이론). 대안의 꼴 = 부피 보존 잘린 구 (kakar1967 · 맞춘 값 0) · 부피 보존 neck + 입자 표면 예산 보정 (nisar2024 · 힘 법칙이 아니라 수송용 면적 · 맞춘 값은 접촉 저항 쪽 2 개) · 평형 겹침 속도식 + 경도 캡 (so2022). multi-contact · MDR · EEPA · Thornton–Ning · Storåkers 를 직접 다룬 카드는 이 배치에 없다 (kakar 카드가 다른 카드로 이어 주는 줄만 있다).

- [e] kakar1967_deformation_theory_hot_pressing | 겹침 원 (구 반지름 고정) 기하가 통하는 범위: *"up to a value of a/R = 0.25, R is approximately equal to R₀ (the initial radius) and for this reason all experimental work was limited to a/R = 0.25"* · 그 뒤 R 급증 (Fig 2: R ≈ 0.620 = R₀ 가 a/R ≈ 0.3 까지 거의 평평 · 0.5 에서 ≈ 0.643–0.656) · 그 구간의 부피 보존 보정 = 면적 +1–7 % (사방) · 능면체 ≤ +11 % | §0 L21 · §3-A L57 · §3-B L82 · §3-C L89–92 · 논문 p.3226 · Fig 2 | 인용문 = stated · Fig 2 = 판독 · 보정 % = 우리 산술 | 단분산 정규 격자 · 납 / 사파이어
- [e] kakar1967_deformation_theory_hot_pressing | 한 입자의 접촉끼리 닿는 임계 단계: 이웃 평면이 닿는 순간 = 단순입방 a = R/√2 · 나머지 a = 0.5R → 그때 밀도 D(R_c) = 96.51 % (단순입방) · 83.51 % (사방) · 96.41 % (능면체) · 93.95 / 99.45 % (체심 1 · 2 단계) · 그 뒤는 다면체로 가는 다른 기하 (모델 밖) | §3-A L54–55 · §4-1 L132 · §4-5 L172 · Table I · 논문 p.3225 | stated | 정규 격자 (무작위 충전 아님) · 능면체 R_c 본문값은 오식으로 보임 (카드 §3-D ③)
- [e] kakar1967_deformation_theory_hot_pressing | 대안의 꼴 = 부피 보존 잘린 구 + 균일 반경 성장: V_p = α(2R² + a²)(R² − a²)^{1/2} − βR³ = (4/3)πR₀³ (식 1) · 1 차식 D − D₀ = (3/2)D₀(a/R)² (식 6) · **맞춘 값 0 개** (순수 기하). 카드 산술: 같은 접근량에서 실제 면 ÷ 겹침 원 c²_KC = 1.008–1.106 (a/R 0.10–0.25) · 1.146–1.345 (a/R 0.40) · 1.263–1.733 (a/R 0.50) · 1 차 꼴 c² ≈ 1 + Z(a/R)²/8 · 우리 평균 a/r_SE 0.30–0.44 에 대응하는 칸 ≈ 1.08–1.46 | §3-A L50 · L59 · §3-C L85–107 | 식 = stated · c² = 우리 산술 · 1 차 꼴 = 우리 유도 | 원문에 c² 없음 (접촉별 접근량 미측정) · 원거리 균일 재분배 가정 · 정규 격자 · 쌓임 의존
- [e] kakar1967_deformation_theory_hot_pressing | 다른 대안과 이어 주는 줄 (카드 표기): Storåkers c² ≈ 1.43 = 이상소성 단일 접촉의 국소 pile-up (밀도 무관) · Arzt 1.27–1.40 (D 0.84–0.90) = 원거리 재분배 · `zunker2024_mdr_contact_model_partI` = 입자별 겉보기 반경 성장 (그 카드: 기하 교차 면적이 δ/R > 0.3 에서 과소) · `martinbouvard2003_dem_composite_cold_compaction` = Storåkers A = 2πc²rh 를 DEM 접촉 면적에 쓴 선례 | §8 L269 · L285–288 | 다른 카드 인용 (우리 판단) | 이 논문의 값이 아님
- [e] nisar2024_dem_effective_electrical_conductivity_sps | 겹침 → 접촉 (neck) 반지름: Coble 식 a = √(2r*h) (h = 겹침) 는 "[36] 에서 Coble 은 고밀도 (큰 overlap) 서 neck 과대평가라 명시 → 기각" → 대안 = 두 입자 소결 기하 + 부피 보존 (겹침 부피를 원통 neck 으로 재분배해 a 결정) | §4 L85–89 · Fig 4 · 식 21 | 표지 없음 (카드 서술) | 과대평가가 시작되는 겹침 값은 카드에 없음 · 소결 neck (가압 접촉 아님) · NiAl
- [e] nisar2024_dem_effective_electrical_conductivity_sps | 다접촉 보정: 두 입자 상호작용만 보는 탓에 고밀도에서 한 입자의 neck 합이 입자 표면을 넘음 → f_i^gbf = Σ_j S_ij^neck / S_i ≤ 1 (식 22–23) 을 넘으면 그 입자의 모든 neck 을 a_ij^corr = α_i·a_ij (식 24) · α_i ≤ 2r_i/√(Σ a_ij²) (식 25) 로 줄임 · 이 보정에 맞춘 값 0 개 · 접촉 저항 쪽 맞춘 값 **2 개** (δ_gb 0.23 µm · ε 0.16 — Sample 3 한 점) | §4 L90–93 · L99–100 | stated (식) | 수송 (전기) 용 면적 보정이지 힘 법칙이 아님 · 기공 0.05–0.216 범위
- [e] so2022_dem_compaction_coated_particles_assb | 대안의 꼴 = 평형 겹침 속도식 + 경도 캡: F_spring = k_n(h_ov − h_eq) · k_n = (4/3)E_eff·h_ov^{1/2}·R_eff^{1/2} · ∂h_eq/∂t = (F_spring − F_th)/(t_rel·k_n) (F > F_th) / 0 (사이) / (F_spring + F_th)/(t_rel·k_n) (F < −F_th) · F_th = min(H_i, H_j)·A_con · 기공 → 0 쪽 보정인자 c_area · k_n 은 MethodsX [31] 참조. Table 1 에서 "This study" 로 적힌 값 = 마찰 0.5 · 반발계수 0.5 · "fit" 으로 적힌 값 = AM primary 1 µm · SE 응집체 / primary 1.5 / 0.5 µm | §3.1 L48–51 · §4.1 L86–94 · 식 1–7 | stated | 점접촉 법칙이 깨지는 겹침 범위는 이 카드에 없음 (동반 MethodsX 카드 소관) · 맞춘 값의 총 개수를 카드가 세지 않음 · t_rel 값 없음 · LPS + NCM
- [e] lee2024_multiphysics_dem_fem_initial_pressure_assb | 대안 아님 — 이력 선형 스프링 (Hertz 아님 · 항복 캡 없음): K_nl,p = E_p·L_par · K_nu = K_nl/ε² · 맞춘 값 표기 없음 | §4.2 L118–126 · 식 3–8 | stated | 큰 변형 범위에 대한 말 없음
- [e] doux2020_stack_pressure_assb | 이 카드에 없음 | — | — | —
- [e] sakuda2013_sulfide_mechanical_property | 이 카드에 없음 | — | — | —
- [e] deysher2022_transport_mechanical_aspects_assb_review | 이 카드에 없음 | — | — | —
- [e] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 이 카드에 없음 | — | — | —

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

이 배치에 없음 — 여덟 장 모두 MPM 을 쓰지 않는다. (so2022 는 입자를 3D 격자에 옮겨 TauFactor 를 돌리지만 격자 해상도는 카드에 없고 [§4.3 L108], nisar2024 의 수렴 기준 2 × 10⁻⁴ 는 저항망 반복 해의 것이다 [§4 L76].)

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

경고 · 증거는 이 배치에 없음. 차원에 관한 사실 두 줄만 있다.

- [g] so2022_dem_compaction_coated_particles_assb | 계보: So 2020 (2D · ASSB 제조 · 셀 인터칼레이션 DEM) → So 2021 = "그 2D 의 3D 확장" → 이 논문 (3D · 양극 · 코팅). 2D 값과 3D 값의 차이나 옮길 때의 경고는 카드에 없음 | §2 L27–29 | 표지 없음 | —
- [g] lee2024_multiphysics_dem_fem_initial_pressure_assb | FEM 이 pseudo-3D (2D 거시 경계 조건 + 대표 AM 입자 안 1D 확산 · Wolff 2018 기반) · DEM 의 차원은 카드에 없음 | §4.3 L143–144 | 표지 없음 | 3D 로 옮길 때의 경고 · 증거 없음

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

선례 = **1** (lee2024: DEM → FEM · 균질화 스칼라 · 압밀이 끝난 압축률 상태에서 한 방향). so2022 는 압밀 끝 구조를 격자 수송 계산으로만 넘긴다.

- [h] lee2024_multiphysics_dem_fem_initial_pressure_assb | DEM (Ansys Rocky 4.5) → FEM (COMSOL 6.0 · 전기화학 – 역학 결합) 한 방향. **넘긴 것** = 균질화 스칼라: 압축률 · 압축률에 따른 유효 영률 · 부피분율 · 표면적 S_a = 3ε_AM/R_p (식 34) · 굴곡도 τ = −11.7·ε_SE + 8.54 (식 38). **넘긴 시점** = DEM 압밀이 정한 압축률 (0.7 · 0.5) 상태 — 그 뒤의 외부압 (0 / 10 / 50 / 100 MPa) · 충방전 · 인터칼레이션 부피 변형 응력은 FEM 이 품 · 되먹임 없음. 저자 주장 "DEM+FEM 동시 예측은 처음" | §1 L22–23 · §4.1 L98–113 · §4.3 L158 · L163–166 · Fig 1 | stated · 식 38 의 출처 귀속 [미확인] (카드 정정 2026-10-13) | 입자 위치가 아니라 유효 물성만 넘김 (카드: 입자 정보 소실) · LGPS + LLZO · 실험 검증 없음 · DEM (graphite 14 · NMC 12 µm) 과 FEM (10 · 5 µm) 의 입경이 다름
- [h] so2022_dem_compaction_coated_particles_assb | DEM 입자 → 3D 격자 매핑 [30] → TauFactor (라플라스 확산) 로 SE 상 · AM 상의 τ — 압밀 끝 구조를 격자 수송 계산으로 넘긴 선례 (역학을 FE · MPM 으로 넘긴 것은 아님) · 주기 (PBC) · 비주기 두 판을 계산했고 비주기가 FIB-SEM 실험 (Nakamura) 과 더 잘 맞음 | §4.3 L108 · Fig 7 | 표지 없음 | 격자 해상도는 카드에 없음 · σ 값은 내지 않음 (τ 와 퍼콜 부피만)
- [h] nisar2024_dem_effective_electrical_conductivity_sps | FE · MPM 으로 넘기지 않음. 소결 DEM (열 – 점탄성 모델 [43]) 을 중간중간 멈춰 여러 기공률의 기하를 뽑아 같은 DEM 틀의 저항망에 넣음 · 연속체 비교는 [20] FEM 열전도 인용으로 대체 | §4 L59–62 · L66 | 표지 없음 | —
- [h] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 인용만: phase-field (ref 39) · FEM 으로 균열 · 응력 — DEM 에서 넘긴 선례는 아님 | §6.1 L166 · §12 L333 | 2 차 인용 | —
- [h] doux2020 · sakuda2013 · kakar1967 · deysher2022 | 이 카드에 없음 | — | — | —

## i. 복합 양극 (AM + SE) 의 압력별 기공

압력별 곡선을 준 카드는 **없다**. 한 점 = so2022 (LPS + NCM · 360 MPa · 모의). 나머지는 입력값이나 리뷰 인용이다.

- [i] so2022_dem_compaction_coated_particles_assb | 복합 (LPS + NCM · 고체 중 AM 부피분율 f_AM 0.734 · 3D DEM · 누른 채) 360 MPa 한 점: 기공 (= 1 − AM − SE) 혼합 ≈ 17 % · 코팅 ≈ 16 % · 부피분율 AM / SE = 혼합 0.61 / 0.22 · 코팅 0.59 / 0.25 · FIB-SEM (Nakamura [17]) 과 부피분율은 잘 맞고 AM–pore 면적은 과대 | §3.1 L53 · §3.2 L60–61 · Fig 3a | digitized (Fig 3a) — §10 L222 는 같은 값을 "stated" 로 적음 (카드 문제 2) | LPS (LPSCl 아님) · 압력별 곡선 없음 · 겹침 부피를 어떻게 세는지 (합집합인지) 카드에 없음 · 시드 1 개로 보임
- [i] lee2024_multiphysics_dem_fem_initial_pressure_assb | 초기 공극 0.44 (압축 전 · 양극 · 음극 모두) · 초기 부피분율 양극 NMC 0.18 / SE 0.38 · 음극 graphite 0.32 / SE 0.24 — 압축 뒤 기공 – 압력 값은 카드에 없음 ("압축으로 감소") | §3 L69–71 · Table 2 | stated | LGPS · 모의 입력값
- [i] deysher2022_transport_mechanical_aspects_assb_review | 인용: 고 CAM wt% 에서 완전 이용률에 기공 < 20 % 필요 · > 55 % 면 이용률 ↓ ([66] Bielefeld · 미세구조 모델링) | §3 L82–83 · §10 L297–298 | stated (인용) | 압력 축 없음 · 확률적 배치의 입력 기공 (눌러서 나온 기공 아님)
- [i] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 인용: 가압 ↑ → 기공 ↓ · 접촉 면적 ↑ · 성능 ↑ (저율속 · Fig 7b) · 370 MPa 에서도 공동 잔존 (ref 100) · 12 µm NCM + 1.5 µm SE → ≈ 50 vol% CAM 로딩에서 거의 완전 용량 유지 (Shi · ref 106 · cold-press) | §5.1 L126 · L129 · L135 | 2 차 인용 | 기공 수치 없음
- [i] sakuda2013_sulfide_mechanical_property | 복합 양극 (PLD 로 SE 를 입힌 LiCoO₂ : SE 막 ≈ 90 : 10 · 360 MPa 3 층 펠릿) 단면이 "매우 치밀, 공극 거의 없음" (Fig 6b) — 수치 없음. 카드가 적은 다른 논문 값: Minnmann 2021 JES 복합 (NCM622 + LPSCl · 380 MPa) 기공 13–17 % (복합 · 순수 SE 아님) | §4 L81–83 · §5 L100 · §11-C L186 | 정성 · 다른 논문 값은 표지 없음 | 이 논문 값 아님 · doux 카드는 같은 Minnmann 복합을 14 % 로 적음 (카드 문제 19)
- [i] doux2020_stack_pressure_assb | 복합 양극 (LNO 코팅 NCA : LPSCl : carbon black = 11 : 16 : 1 · 12 mg · 370 MPa) 의 기공 값 없음 | §2.1 L91–93 | — | 카드: "양극 microstructure 수치는 전사 금지"
- [i] nisar2024 · kakar1967 | 이 카드에 없음 | — | — | —

## j. 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)

- [j] so2022_dem_compaction_coated_particles_assb | 저자 한계 (논문 §4.3 · 카드의 한국어 옮김): "rough spherical AM 으로 제한 — 비구형·구조화 배열은 안 함 → 구형/타원에서 크게 벗어난 입자엔 결론 적용 불가" · "AM-pore 면적 과대평가 (시뮬이 AM 내부 소공극을 너무 많이 만듦)" · "SE 코팅이 실험보다 덜 매끈 → AM 표면이 부분 노출" · "20 µm 는 AM 응집체 (5 µm) 대비 크지 않다 → aggregate-수 의존성 배제 못 함" | §4.5 L119 · §4.6 L122 | 카드 표기 "명시 한계 (저자 스스로)" | 원문 영어 문장은 카드에 없음
- [j] so2022_dem_compaction_coated_particles_assb | 계보상의 한계 (카드 서술): So 2021 은 "AM 은 구, intraparticle cracking 은 future work" → 이 논문은 응집체 수준 균열만 (primary 구 자체의 균열 · 모양 변화는 안 함) · 시드 다중 실현 · 통계 명시 없음 · 전체 sweep ≈ 10 일이라 상자를 키우기 어려움 | §4.5 L117 · §4.6 L122 · L125 | 표지 없음 | —
- [j] lee2024_multiphysics_dem_fem_initial_pressure_assb | 저자 한계: "FEM 이 항복 응력 초과 변형 / 파괴를 미반영, 향후 추가 예정" (카드의 한국어 옮김) · 한 방향 전달 (충방전 중 입자 재배열 · 힘 사슬 변화 미반영) · 실험 검증 없음 · 외부압 50 MPa 이상에서 효과 포화 | §A.3 L281–282 · §10 L415 · L422–424 | 카드 표기 "한계에서 명시" | —
- [j] kakar1967_deformation_theory_hot_pressing | 저자 한계: 실험을 a/R ≤ 0.25 로 묶음 · 이론은 정수압인데 실험은 일축 다이 (압력 분포 불균일) · *"the width of the die does not permit an integral number of spheres"* · 한 구 안 평면 a 가 평균에서 100–150 % 까지 벗어남 · *"It is believed that no particular model governs the deformation"* · 이웃 평면이 닿는 임계 단계 뒤는 모델 밖 · 정방 쌓임은 *"does not seem to conform to a regular polyhedron on deformation and so cannot result in complete densification"* 이라 제외 | §3-A L48 · L57 · L67 · L70 · §8 L280 · §10 L301–302 · 논문 p.3224 · p.3226 · p.3228 · p.3230 | stated | —
- [j] nisar2024_dem_effective_electrical_conductivity_sps | 저자 서술: 소결 시뮬은 두 입자 상호작용만 보고 다중 접촉을 무시 → 고밀도에서 neck 합이 입자 표면을 넘는 비물리 (그래서 α 보정) · neck 안에도 공극이 남음 (SEM Fig 2) · 시드 / 실현 수 미명시 (시료당 기하 1 개로 보임) | §4 L83 · L90–91 · L98 | 표지 없음 | 소결 (가압 · 탈압 아님)
- [j] doux2020_stack_pressure_assb | 저자 가정 (측정 아님): 작동 적층압 5 / 25 / 75 MPa 에서 펠릿 자체의 기계적 성질은 영향이 없을 것 — 이미 370 MPa 로 눌렸으므로. 카드 한계: Fig 4c 는 계면 접촉 저항이지 SE 벌크의 σ – 압력이 아님 | §8 L235–236 · §13 L358–360 | 카드 표기 "본문 명시" | 탈압 뒤 펠릿 상태를 잰 것은 아님
- [j] sakuda2013_sulfide_mechanical_property | 저자 서술: *"preparing Li₂S–P₂S₅ bulk glass is quite difficult and has not been reported"* → 기준 밀도를 열간 프레스 펠릿으로 대신 · 황화물의 기계 물성은 대기 불안정 (inert 취급 필요) 때문에 측정이 어려워 그간 정량화되지 않았다 (카드의 서사 요약) | §13-1 L218–219 · §7 L112–113 · 논문 p.5 | 인용문 = verbatim · 뒤쪽은 표지 없음 | —
- [j] deysher2022_transport_mechanical_aspects_assb_review | 리뷰의 공백 선언: *"significant knowledge gap in the understanding of the mechanical properties of solid electrolyte materials and their composites"* · 앞으로의 방향 = 사이클 성능 예측 + 장기 역학 안정성 · 적층압 아래의 operando / paired reconstruction (FIB) | §4 L118–119 · §B.2 L215–216 | 인용문 (카드가 따옴표로 옮김) | 리뷰 · 원문 쪽 번호는 카드에 없음
- [j] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 리뷰가 꼽은 미해결: 각 열화 메커니즘의 기여를 떼어 재는 방법 · 전기화학 – 기계 열화가 폭주하는 임계 조건 (threshold) 규명 · in situ / operando · 다중 스케일 실험 × 계산 · *"Modifying one parameter inevitably alters others, often producing unintended consequences."* | §8 L224 · L227–230 | 인용문 (카드가 따옴표로 옮김) | 리뷰 · 가압 · 탈압 계산 자체에 대한 말은 아님

## k. DEM 의 한계 (논문이 직접 말한 문장 · 수치)

DEM 을 쓴 카드는 셋 (so2022 · lee2024 · nisar2024). 저자가 구 – DEM 의 한계를 직접 적었다고 카드가 옮긴 것은 so2022 (한국어 옮김) 와 nisar2024 (두 입자 가정 · Coble 식 과대) 이고, **lee2024 는 말 없음**. 믿을 수 있는 겹침 · 상대밀도의 **수치 상한을 준 DEM 논문은 이 배치에 없다** — 가장 가까운 것이 kakar1967 의 a/R = 0.25 (구 반지름이 안 자라는 구간) 와 임계 단계 밀도 (한 입자의 접촉끼리 닿는 기하 한계) 인데 DEM 논문이 아니라 1967 년 기하 이론이다. 영어 원문 문장이 따옴표로 남아 있는 것은 kakar1967 · sakuda2013 (한 구) 뿐이다.

- [k] so2022_dem_compaction_coated_particles_assb (M. So, G. Inoue, K. Park, K. Nunoshita, S. Ishikawa, Y. Tsuge, J. Power Sources 530 (2022) 231279) | 저자가 적은 구 – DEM 의 한계 (논문 §4.3 · 카드의 한국어 옮김 — 영어 원문은 카드에 없음): ① "rough spherical AM 으로 제한 — 비구형·구조화 배열은 안 함 → 구형/타원에서 크게 벗어난 입자엔 결론 적용 불가" ② "SE 코팅이 실험보다 덜 매끈 → AM 표면이 부분 노출" ③ "AM-pore 면적 과대평가 (시뮬이 AM 내부 소공극을 너무 많이 만듦)" ④ "20 µm 는 AM 응집체(5 µm) 대비 크지 않다 → aggregate-수 의존성 배제 못 함" | §4.5 L119 · §4.6 L122 · 논문 §4.3 | 카드 표기 "명시 한계 (저자 스스로)" | LPS + NCM · 겹침 · 상대밀도의 상한 수치는 카드에 없음 · 인용하려면 원문 문장을 PDF 에서 다시 따야 함
- [k] so2022_dem_compaction_coated_particles_assb (같은 서지) | 카드의 풀이 (논문 문장 아님 — 인용할 때 구분): "입자 외형은 절대 변하지 않는다. 소성은 CONTACT 소성 (h_eq = 접촉점 함몰/융착 proxy) 이며 진짜 입자 SHAPE 흐름 (void-fill flow) 아님" · SE 쉘의 박리 · 재부착은 모델하나 SE 가 흘러 AM 을 감싸는 연속 막을 이루는 것은 안 함 | §4.5 L116–118 | 표지 없음 (카드 서술) | 우리 쪽 해석
- [k] nisar2024_dem_effective_electrical_conductivity_sps (F. Nisar, J. Rojek, S. Nosewicz, J. Szczepański, K. Kaszyca, M. Chmielewski, Comput. Part. Mech. 11 (2024) 2191–2201) | **두 입자 (접촉 독립) 가정이 고밀도에서 깨진다**: 소결 시뮬은 두 입자 상호작용만 보고 다중 접촉을 무시 → 고밀도에서 한 입자의 neck 들이 합쳐 입자 표면을 초과하는 비물리 → 입계 분율 f_i^gbf = Σ_j S_ij^neck / S_i ≤ 1 (식 22–23) 로 추적하고 넘으면 a_ij^corr = α_i·a_ij · α_i ≤ 2r_i/√(Σ a_ij²) (식 24–25) 로 그 입자의 모든 neck 을 줄임 | §4 L90–93 · 논문 §3.4 · 식 22–25 | 표지 없음 (카드 서술) | 원문 문장을 따옴표로 옮긴 것은 없음 · 깨지기 시작하는 밀도 · 겹침 값은 카드에 없음 (시료 기공 0.05–0.216) · 소결 neck 의 수송용 면적 (힘 법칙 아님) · NiAl
- [k] nisar2024_dem_effective_electrical_conductivity_sps (같은 서지) | **겹침에서 접촉 반지름을 내는 통상식이 큰 겹침에서 과대**: Coble 식 a = √(2r*h) 는 "[36] 에서 Coble 은 고밀도 (큰 overlap) 서 neck 과대평가라 명시 → 기각" ([36] = Rojek 2022, Powder Technol. 405:117521) | §2 L27 · §4 L85–87 · 논문 §3.3 · 식 21 | 표지 없음 (카드 서술) | 과대의 크기 · 시작점은 카드에 없음 · 원 서술은 [36] 의 것
- [k] nisar2024_dem_effective_electrical_conductivity_sps (같은 서지) | **보정값이 물성이 아니다**: 접촉 (neck 내 입계) 저항의 δ_gb 0.23 µm · ε 0.16 은 "보정 fitting param" — Sample 3 (기공 0.106) 한 점에 맞추고 나머지 3 점으로 검증 · 보정 지도 (δ_gb 0.1–0.3 µm × ε 0.1–0.5) 에서 실험 오차 띠 안 조합이 여럿이고 그중 하나를 채택 · SEM 으로 잰 GB 두께는 0.15–0.4 µm (단일 0.36) | §3 L40–41 · §4 L99–100 · Fig 5 · 9 | stated | 전기 전도 (역학 아님) · NiAl
- [k] kakar1967_deformation_theory_hot_pressing (A. K. Kakar, A. C. D. Chaklader, J. Appl. Phys. 38(8), 3223–3230 (1967)) | DEM 논문은 아님 (해석 + 실험) — DEM 에 대한 말은 없음. "구 반지름 고정 + 겹침 원" 기하가 통하는 범위로 인용할 수 있는 원문: *"up to a value of a/R = 0.25, R is approximately equal to R₀ (the initial radius) and for this reason all experimental work was limited to a/R = 0.25"* (p.3226) · 부피 보존의 전제: *"As the radius a of the face increases, the radius R of the sphere must increase to maintain a constant volume. This is true only if the material at the faces spreads symmetrically to maintain the sphericity of the particle."* (p.3224) | §0 L21 · §3-A L57 | stated (인용문) | 단분산 정규 격자 · 납 / 사파이어 · a/R ≤ 0.25 를 "믿을 수 있는 상한" 으로 읽는 것은 카드의 읽기 (원문은 R ≈ R₀ 구간이라고만 함) · 카드: 우리 평균 a/r_SE 0.30–0.44 는 그 밖 (L214)
- [k] kakar1967_deformation_theory_hot_pressing (같은 서지) | **한 입자의 접촉끼리 닿는 (접촉 독립이 기하로 끝나는) 밀도**: 이웃 평면이 닿는 임계 단계 a = 0.5R (단순입방은 R/√2) 에서 D = 83.51 % (사방 Z 8) · 93.95 % (체심 1 단계) · 96.41 % (능면체 Z 12) · 96.51 % (단순입방 Z 6) | §3-A L54–55 · Table I · 논문 p.3225 | stated | 정규 격자의 기하 한계 (무작위 다분산 침대의 값 아님) · DEM 을 두고 한 말이 아님
- [k] kakar1967_deformation_theory_hot_pressing (같은 서지) | **접촉 평면화만으로는 치밀화를 설명 못 한다는 실측**: 같은 a/R 에서 실측 겉보기 부피 변형률이 아핀 접촉 모델의 ≈ 1.3–2.4 배 (Fig 8) · 원문은 미끄러짐 · 재적층 · 배위수 증가에 돌림 (p.3229) · 납 Z ≈ 7.6 → 9–10 | §3-B L78–79 · §8 L272 | 판독 · 비는 우리 산술 | 납 · 사파이어 · D ≲ 0.71 · 그림 판독
- [k] lee2024_multiphysics_dem_fem_initial_pressure_assb (Y. K. Lee, C. Sung, J. Kim, C. Hong, J. Choi, J. Energy Storage 82 (2024) 110431) | **말 없음** — DEM (구 · 이력 선형 스프링 · 항복 캡 없음) 을 쓰면서 DEM 의 한계를 논문이 말했다는 내용은 카드에 없음. 저자가 한계로 적은 것은 FEM 쪽뿐 ("항복 응력 초과 변형 / 파괴 미반영, 향후 추가 예정") | §A.3 L281–282 · §10 L411 | 카드 표기 | "구만 · 진짜 SHAPE 소성 아님" 은 카드의 서술 (L134–137)
- [k] sakuda2013_sulfide_mechanical_property (A. Sakuda, A. Hayashi, M. Tatsumisago, Sci. Rep. 3, 2261 (2013)) | DEM 안 씀 (실험) — DEM 에 대한 말 없음. 구 입자 가정과 어긋나는 실측 증거로 인용 가능: 가압 전 → 74 MPa → 360 MPa 파단면 SEM 에서 입자가 서로 붙어 입자 크기가 커지고 입계 · 공극이 줄어듦 (Fig 2b–d) · 360 MPa 상온 가압 이온밀링 단면에서 "입계 거의 안 보임 (grain boundaries hardly visible)" (Fig 3a · 80Li₂S·20P₂S₅) · 가압 뒤 XRD 비정질 유지 · Raman 국소 환경 거의 불변 (SI S1 · S2) | §4 L85–88 · §5 L95–96 · §6 L105–106 | 표지 없음 (그림 설명) · 괄호 안 영어는 카드가 옮긴 원문 구 | 황화물 유리 (LPSCl 아님) · "강체 구 DEM 한계를 실험이 직접 지적" 은 카드의 해석 (L143) · SI 는 PDF 미첨부 (본문 인용만)
- [k] doux2020_stack_pressure_assb (J.-M. Doux, H. Nguyen, D. H. S. Tan, A. Banerjee, X. Wang, E. A. Wu, C. Jo, H. Yang, Y. S. Meng, Adv. Energy Mater. 10 (2020) 1903253) | 말 없음 (실험 · DEM 을 쓰지 않음). 카드의 "실험 LPSCl 펠릿 18 % ≈ 우리 rigid-sphere floor ~20 %" (L208–209) 는 우리 쪽 해석이고 논문 문장이 아님 | §6 L207–209 | — | DEM 한계의 근거로 이 논문을 인용할 수 없음
- [k] deysher2022_transport_mechanical_aspects_assb_review (G. Deysher, P. Ridley 외, Mater. Today Phys. 24 (2022) 100679) | 말 없음 (리뷰 · 자체 모델 없음). 카드는 리뷰가 인용한 미세구조 모델 [66, 67] 이 "강체-구 + voxel 기반" 이라고만 적음 | §4 L117 | — | —
- [k] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review (J. Kang, H. R. Shin, Y. Lee, J.-W. Lee, Chem. Commun. 62 (2026) 10277–10294) | 말 없음 (리뷰 · DEM 언급 없음) | — | — | —

## l. 소성변형이 왜 어려운가 · 택한 우회와 그 값

논문이 "왜 어려운지" 를 직접 설명했다고 카드가 옮긴 문장은 거의 없다 — 대부분 **택한 우회와 그 결과로 드러난 한계** 다. 인용할 수 있는 원문 문장이 있는 것 = kakar1967 (전제 문장 · "no particular model governs") · deysher2022 (역학 물성 지식 공백) · sakuda2013 (기준 밀도 문장). 탈압 때의 되돌아옴까지 다룬 우회는 이 배치에 없다.

- [l] so2022_dem_compaction_coated_particles_assb (So 외, J. Power Sources 530 (2022) 231279) | **우회 = 접촉에만 소성을 넣은 구 DEM**: 평형 겹침 h_eq 속도식 + 경도 문턱 F_th = min(H_i, H_j)·A_con (σ_yield ≈ H 근사) + 융착 / 박리 (인장 쪽 문턱) + 기공 → 0 보정인자 (c_area · k_n — MethodsX [31]). 값: H_SE 1.9 · H_AM 11.2 GPa · E 24 / 199 GPa 는 문헌값 · "This study" = 마찰 0.5 · 반발계수 0.5 · "fit" = 입자 / 응집체 크기. 검증 = Nakamura [17] FIB-SEM (부피분율 · 계면 면적 · τ · 퍼콜) 과 360 MPa 에서 대조 — 부피분율은 잘 맞고 AM–pore 면적은 과대. 비용 = 한 점 ≈ 4 h · 전체 sweep ≈ 10 일 (Intel Xeon W-2145 8 코어 · 자체 MATLAB · Verlet 2 차) | §3.1 L43–51 · §3.2 L60 · §4.0 L82 · §4.1 L86–95 · §6 L147 | stated | "왜 어려운지" 를 설명한 문장은 카드에 없음 — 결과로 드러난 한계만 (코팅이 실험보다 덜 매끈 = 구가 흘러 막을 이루지 못함) · 탈압 미계산 · 입자 수 · t_rel 값 없음 · LPS + NCM
- [l] so2022_dem_compaction_coated_particles_assb (같은 서지) | 재료마다 소성을 다르게 넣은 이유 (카드 서술): LPS 는 상온 압력 소결로 융착 가능 [8] → SE–SE · AM–SE 융착 허용 · NCM 은 고온 소결이 필요하고 H_AM 11.2 GPa 로 "소성 거의 안 함" → AM–AM 은 냉간에서 새 융착 금지 · 응집체 안의 기존 융착이 끊기면 손상 | §3.1 L45–46 · §4.1 L95 | 표지 없음 | —
- [l] lee2024_multiphysics_dem_fem_initial_pressure_assb (Lee 외, J. Energy Storage 82 (2024) 110431) | **우회 = 이력 선형 스프링 + 균질화 넘김**: 하중 강성 K_nl ↔ 제하 강성 K_nu = K_nl/ε² (항복 캡 없음) 으로 누르고, 입자는 그대로 둔 채 압축률에 따른 유효 영률 · 부피분율을 연속체 FEM 에 넘김. 맞춘 값 표기 없음 · 검증 없음 (실험 0) · 입자 1000–30000 · 계산 시간은 카드에 없음. 저자 한계 "FEM 이 항복 응력 초과 변형 / 파괴를 미반영, 향후 추가 예정" | §4.2 L118–139 · §A.3 L281–282 | stated · 한계는 카드의 한국어 옮김 | 어려운 이유의 설명은 카드에 없음 · LGPS + LLZO
- [l] kakar1967_deformation_theory_hot_pressing (Kakar & Chaklader, J. Appl. Phys. 38, 3223–3230 (1967)) | **모양 변화를 닫힌 기하로 넣은 원형**: 잘린 구 + 균일 반경 성장 (부피 보존 · 식 1) — 맞춘 값 0 개 · 전제 *"This is true only if the material at the faces spreads symmetrically to maintain the sphericity of the particle."* · 검증 범위 = 납 · 사파이어 a/R ≤ 0.235 · D ≲ 0.71 · 계산 = a/R 마다 식 1 을 R 에 대해 풂 (*"all theoretical calculations have been carried out using an IBM computer"*) | §0 L21 · §3-A L50 · §4-1 L133 · §10 L301 · 논문 p.3224–3226 | stated | 단분산 정규 격자 · 힘 – 경도 법칙 없음 · 이론에 재배열 · 배위수 증가 없음
- [l] kakar1967_deformation_theory_hot_pressing (같은 서지) | **어려운 이유로 인용할 수 있는 실측**: ① 소성 평면화와 재배열이 같이 일어남 — 결론 (a) 하중 즉시 미끄러짐 (b) 재배향 · 재적층이 변형 내내 계속 · 실측 치밀화가 아핀 접촉 모델의 ≈ 1.3–2.4 배 (Fig 8) · 배위수가 늘어남 (Z ≈ 7.6 → 9–10 · 이론은 Z 고정) ② 한 구 안에서도 평면 크기가 평균에서 100–150 % 까지 벗어남 · *"the newly formed faces gave low values of a/R"* · 원인 = 일축 가압이라 정수압이 아님 · 구 부위별 경도 차 · 결정 방위 ③ *"It is believed that no particular model governs the deformation"* | §3-A L67 · L70–71 · §3-B L78–79 · 논문 p.3228–3230 | stated · 비 · Z 는 판독 (비는 우리 산술) | 납 · 사파이어 · 저밀도 띠 (D ≲ 0.71)
- [l] sakuda2013_sulfide_mechanical_property (Sakuda, Hayashi, Tatsumisago, Sci. Rep. 3, 2261 (2013)) | **황화물 유리의 치밀화 기구** (실험 논문의 설명): "room-temperature pressure sintering" — 가압 때 Li⁺ 와 PS₄³⁻ 이온이 입계로 확산 · 회전해 이웃 입자가 유합 → 입계 · 공극 감소 · Li–S 결합이 약하고 공유결합성이 커서 응력 아래 이온이 국소 재배열 (small-scale plasticity) · 유리 구조 (큰 자유부피 · 낮은 Tg) · 가압 뒤 XRD 비정질 유지 · Raman 불변 = 상전이가 아닌 물리적 치밀화 | §7 L114–119 · §8 L129–134 | 표지 없음 (서사 요약 · 따옴표 안 용어는 원문 것) | 모델 없음 (우회 없음) · 유리 (LPSCl 아님) · 유지 시간 · 속도 의존은 카드에 없음 · 입자 경계가 사라지는 기구라 입자 계산에 넣기 어렵다는 연결은 카드의 해석 (L143)
- [l] nisar2024_dem_effective_electrical_conductivity_sps (Nisar 외, Comput. Part. Mech. 11 (2024) 2191–2201) | 소성은 다루지 않음 — 형상은 별도 열 – 점탄성 소결 모델 [43] 에서 만들고 입자는 구 · neck 만 별도 기하. 이웃 접촉의 상호 영향에 대한 우회 = α 보정 (맞춘 값 0) · 접촉 저항에 맞춘 값 2 개 (1 점 보정 · 3 점 검증) · 입자 > 17,000 · 반복 ≈ 40 회 · 계산 시간은 카드에 없음 | §4 L59–62 · L76 · L90–100 | stated | 소결 · 전기 · NiAl
- [l] doux2020_stack_pressure_assb (Doux 외, Adv. Energy Mater. 10, 1903253 (2020)) | **하중 이력 의존의 실험 증거** (모델 없음): 25 MPa 까지 올렸다 5 MPa 로 내리면 임피던스가 처음 5 MPa 값 (≈ 110 Ω) 의 절반 이하 (≈ 50 Ω) 로 남음 · Li 는 항복 ≈ 0.8 MPa 의 ≈ 6–100 배 압력에서 SE 공극으로 creep (25 MPa 는 plate / strip 때만 ≈ 48 h 뒤 단락 · 75 MPa 는 즉시) | §3 L121–135 · §4 L152 · L159–163 | 본문 stated | Li 금속의 흐름 · Li/SE 계면 — SE 입자 소성의 증거로 직접 쓰지 않는다 (카드 §13 L355–357)
- [l] deysher2022_transport_mechanical_aspects_assb_review (Deysher, Ridley 외, Mater. Today Phys. 24 (2022) 100679) | **어려운 이유로 인용할 수 있는 리뷰 문장**: *"significant knowledge gap in the understanding of the mechanical properties of solid electrolyte materials and their composites"* | §4 L118–119 (카드 C.1 은 "§1 끝" 이라고 적음 · L231) | 인용문 (카드가 따옴표로 옮김) | 리뷰 · 원문 쪽 번호는 카드에 없음
- [l] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review (Kang, Shin, Lee, Lee, Chem. Commun. 62, 10277–10294 (2026)) | 리뷰 서술 (2 차 인용 · 현상): 고압 냉간 가압에도 나노 – 마이크로 공동이 남음 — 단단한 산화물 CAM (E 150–200 GPa) 과 무른 황화물 SE (E 20–30 GPa) 의 변형 거동 불일치 ("SE 는 소성변형하나 CAM 강성 수용 못 함 → 구조 불균일 잔존" — 카드의 한국어 옮김) · 불균일 가압 → 국소 force concentration | §5.1 L124–128 | 2 차 인용 (ref 100–102) | 계산이 어렵다는 말은 아님 · 원전 확인 필요

## m. 받아들일 통찰 (무엇을 | 우리 쪽 어디에 | 근거 위치)

- [m] so2022_dem_compaction_coated_particles_assb | 코팅된 (코어 – 쉘) AM 출발 상태를 만드는 4 단계: AM 응집체 구성 → AM subparticle 위치의 3D Delaunay 삼각분할에서 긴 모서리 사면체를 지워 표면 삼각망을 추정 → 그 표면에 SE 입자 (0.5 µm) 를 무작위 배치 → shoving 으로 겹침 제거 | 흐름 밖: 코팅 활물질 믹싱 (Ⓒ) 의 코팅 침대 초기 배치 · 단계 5 에서 코팅 AM 을 다룰 때의 출발 상태 | §4.2 L99–104 · Fig 1d
- [m] so2022_dem_compaction_coated_particles_assb | 손상 · 접촉 분리를 두께 방향 (z) 수평 단면 평균으로 보고 — 벽 (집전체 · SE 층 경계) 근처 ≈ 25 % ↔ 가운데 ≈ 5 % 라 전체 평균 하나 (≈ 12 %) 로는 벽 효과가 숨는다 | 단계 5 · 조건 R7 의 관측량 정의 (판 쪽 층과 가운데를 따로) · 결과 전 대조 항목의 꼴 | §3.2 L66–67 · §4.4 L113 · Fig 6d
- [m] so2022_dem_compaction_coated_particles_assb | 격자 수송 계산의 경계 조건을 주기 · 비주기 둘 다 계산해 실험과 견줌 — 비주기가 FIB-SEM 과 더 잘 맞았다 | 단계 7 (수송 계산의 옆면 경계 조건을 결과 전에 적고 둘 다 보고) · 흐름 밖: 복셀 수송 계산 | §4.3 L108
- [m] so2022_dem_compaction_coated_particles_assb | 계면 결합의 수지 식: accumulated = initial + attached − delaminated (식 8) — 떨어진 수와 새로 붙은 수를 따로 세어 순증감을 냄 (코팅 @500 MPa: 5.0 × 10⁴ + 1.8 × 10⁴ − 1.3 × 10⁴ = 5.5 × 10⁴ — 내 검산) | 단계 6 · 조건 R2 (탈압 때 계면 분리를 "떨어진 수 · 다시 붙은 수" 로 따로 세는 관측량) | §3.2 L68–69 · §6 L145 · Fig 5b
- [m] nisar2024_dem_effective_electrical_conductivity_sps | 입자별 표면 예산 진단: f_i = Σ_j (접촉 면적) ÷ (입자 표면적) ≤ 1 · 넘는 입자는 접촉 독립 가정이 깨진 입자 (그 논문은 α_i ≤ 2r_i/√(Σ a_ij²) 로 줄임) | 후보 D0 의 신뢰 범위 진단 (f_i > 1 인 입자 수를 결과 전에 진단 항목으로) · 단계 0 · 단계 7 의 접촉 면적 상한 | §4 L90–93 · 식 22–25
- [m] nisar2024_dem_effective_electrical_conductivity_sps | 검증 설계: 맞춘 값 2 개를 시료 1 개 (기공 0.106) 에만 맞추고 나머지 3 개 (0.216 · 0.164 · 0.050) 로 검증 · "접촉 저항 없이 → 일관 과대 (Fig 8)" 와 "넣으면 근사 일치 (Fig 10)" 를 같은 축에 나란히 | 조건 R5 · 단계 4 (한 압력에 맞추고 다른 압력은 검증 점으로 남김) · 흐름 밖: 접촉망 수송 검증 (협착 없는 해 → 있는 해 → 실측) | §4 L99–100 · §5 L114–116 · Fig 8–10
- [m] nisar2024_dem_effective_electrical_conductivity_sps | 겹침 → 접촉 반지름의 부피 보존 규칙: 겹침 렌즈 부피 = 원통 neck 부피로 두어 a 를 정함 (Coble a = √(2r*h) 는 큰 겹침에서 과대라 기각) | 단계 7 · 흐름 밖: 접촉망 수송 계산의 접촉 면적 추정량 교차 대조 | §4 L85–89 · Fig 4
- [m] nisar2024_dem_effective_electrical_conductivity_sps | 선형 저항망을 대각 용량 + forward-Euler 반복으로 푸는 길: 안정 조건 Δt < 2C_ij/K_ij (식 42–43) 이 곧 수렴 조건 (부록 증명) · 수렴 지표 max|ΔV/V| ≤ 2 × 10⁻⁴ · ≈ 40 회 | 흐름 밖: 접촉망 솔버 (CG 가 수렴하지 않는 망의 대안 해법) | §4 L73–78 · 부록 식 32–43
- [m] doux2020_stack_pressure_assb | 같은 조건으로 만든 펠릿의 산포: 370 MPa · 200 mg · 13 mm 로 만든 LPSCl 펠릿 4 개의 상대밀도가 80.3–84.9 % (폭 4.6 %p) → 실험 기공을 한 값이 아니라 산포와 함께 적는다 | 단계 4 의 결과 전 대조 항목 (맞춤 표적의 허용 폭) · 단계 0 | §6 L202–203 · Table S2 (값 자체는 랩 표준과 다른 문헌 값 — 산포의 크기만)
- [m] doux2020_stack_pressure_assb | 접촉 이력 시험의 꼴: 낮은 압력 (5 MPa) → 높은 압력 (25 MPa) → 같은 낮은 압력으로 되돌려 같은 양을 다시 잼 (110 → 32 → 50 Ω) | 단계 6 의 결과 전 대조 형식 (탈압 뒤 같은 압력에서의 접촉 · 수송을 가압 전과 견줌) · 흐름 밖: 계면 저항 실험 대조 | §4 L144–163 · Fig 4c
- [m] doux2020_stack_pressure_assb | 압력을 실측하는 셀: 로드셀을 셀 축 아래에 두고 0–220 MPa 를 재며 Instron 으로 교정 · 나사 조임으로 압력을 바꾸는 동안 EIS · 전압을 같이 | 흐름 밖: 실험과의 대조 (같은 시료 원측정을 청할 때 "압력 실측 · 교정" 항목) | §2.2 L97–99 · Fig 2a
- [m] doux2020_stack_pressure_assb | 함정: 압력 셋을 섞지 않는다 — 제작 370 MPa · 접촉 형성 25 MPa · 작동 5 MPa 가 정하는 것이 다르다 (저자는 작동압이 이미 눌린 펠릿을 더 누르지 않는다고 가정) | 단계 6 · 단계 7 (탈압 뒤 수송을 어느 압력 상태에서 평가하는지 결과 전에 적기) | §8 L235–244 · 머리 L36–38
- [m] sakuda2013_sulfide_mechanical_property | 상대밀도의 분모 확인: 이 논문은 결정 밀도가 아니라 약 200 ℃ 열간 프레스 유리 펠릿 1.88 g/cm³ 으로 나누고 측정법은 적지 않았다 → 문헌 기공을 옮길 때 분모의 상 · 값 · 측정법을 같이 적는다 | 단계 0 (기공 연산자 · 문헌 대조 규칙) | §3 L54 · §13-1 L216–221 · §13-2 L226–230
- [m] sakuda2013_sulfide_mechanical_property | stated ↔ 판독 구분: 본문이 적은 밀도는 "> 90 % @ > 350 MPa" 하나 · 흔히 쓰던 "87 % @300 MPa" 는 Fig 2a 눈 판독 (≈ 85–88 %) | 결과 전 대조 항목의 표기 규칙 (단계 0 · 단계 4) | §11-A L162–174
- [m] sakuda2013_sulfide_mechanical_property | 같은 시료에서 밀도 – 압력과 σ – 압력을 나란히: σ 가 70 MPa 에서 ≈ 10⁻⁴ S/cm 로 급상승한 뒤 360 MPa 3.1 × 10⁻⁴ (열간 프레스 bulk 3.4 × 10⁻⁴ 의 0.91 — 내 산술) | 단계 7 의 결과 전 대조 형식 (냉간 가압 σ ÷ 완전 치밀 σ 를 압력별로 · 유리라 값은 못 옮김) | §3 L61–63 · Fig 4
- [m] sakuda2013_sulfide_mechanical_property | 재료 E 는 공극을 뺀 시료에서: 열간 프레스 고밀도 펠릿에 초음파 펄스법 (공극이 음속을 왜곡) — 재료의 E (24 GPa) 와 침대의 유효 강성은 층위가 다르다 | 단계 4 (SE 탄성 입력의 출처 · 층위 표기) · 조건 R5 | §3 L60 · §8 L132 · §12 L198–199
- [m] lee2024_multiphysics_dem_fem_initial_pressure_assb | 출발 혼합의 균일 검사: 침대를 8 구역으로 나눠 두 분말의 부피비와 표준편차를 봄 (NMC 0.695 / 0.118 · graphite 0.682 / 0.047) | 단계 5 (출발 상태 검사 항목) · 흐름 밖: 믹싱 (Ⓒ) 의 혼합도 지표 | §4.2 L130–131 (부피비의 정의는 카드에 불명 — 꼴만)
- [m] lee2024_multiphysics_dem_fem_initial_pressure_assb | 판 응력을 위 punch · 아래 punch 둘 다 기록 (충격량 적분 σ = ΣΣJ ÷ (A·Δt·N_p) · boundary collision statistics) | 단계 3 · 단계 4 · 단계 5 의 누르는 힘 관측량 (위 · 아래 판 반력을 따로 적어 전달 손실을 봄) | §4.2 L127–129 · §5 L205–206 · Fig 2a · 3
- [m] lee2024_multiphysics_dem_fem_initial_pressure_assb | 넘기는 방식의 함정: 균질화 스칼라 (E · ε · S_a · τ) 만 넘기면 입자 수준 정보가 사라지고 σ 는 연속체 식 (Maxwell · Bruggeman · 선형 굴곡도) 의 값이 된다 | 단계 7 (눌린 구조에서 수송 계산으로 무엇을 넘기는지 결과 전에 적기) | §4.1 L112–113 · §4.3 L163–171 (σ 가 상한이라는 읽기는 카드의 해석 · L169–171)
- [m] lee2024_multiphysics_dem_fem_initial_pressure_assb | 인용할 때 걸리는 원문 인쇄 이상: 식 36 의 σ_SE0 0.002 > σ_SEmax 0.0002 S/cm · D_Li 2.61 × 10⁻⁴ m²/s · DEM 과 FEM 의 입경 불일치 | 흐름 밖: 문헌 값 인용 (이 논문의 수송 파라미터를 그대로 옮기지 않는다) | §3 L74–75 · §10 L417–421
- [m] kakar1967_deformation_theory_hot_pressing | 함정: 질량 보존으로 묶인 두 양의 일치는 검증이 아니다 — Fig 9 (밀도 ↔ 겉보기 부피 변형률) 는 D = D_init/(1 + ε_b) 항등식인데 원문은 그것을 *"justifies the assumption that the proposed models are operative"* 의 근거로 썼다 | 단계 0 (판정 기준에서 항등식으로 묶인 쌍 — 기공 ↔ 판 높이 등 — 을 제외) · 결과 전 대조 항목 고르기 | §3-D ⑤ L120 · §8 L278 · 논문 p.3229
- [m] kakar1967_deformation_theory_hot_pressing | 소성 전 재적층 몫을 떼는 절차: 초기 하중 여러 개 (2 · 5 · 10 · 40 lb) 의 잔류 변형을 0 하중으로 외삽 (유리 구 ≈ 1.5 % @10 psi · 구리 구 1.3–4.3 %) | 단계 4 (느슨하게 부은 출발 상태의 재배열 몫을 항복 세기 맞춤에서 분리) · 단계 6 | §3-A L63 · §4-3 L150 · 논문 p.3226–3227
- [m] kakar1967_deformation_theory_hot_pressing | 표본 규칙: 다이 가운데 구만 측정 — 옆벽 · 위아래 층은 a/R 이 약간 크고 Z 가 작다 · 벽 층을 뺀 층 평균이 무작위 20 구 평균의 3–4 % 안 | 단계 5 · 단계 7 · U6 (접촉 · 배위수 통계에서 벽 층을 빼고 그 영향을 같이 보고) | §3-A L66 · 논문 p.3228
- [m] kakar1967_deformation_theory_hot_pressing | D – (a/R)² 축 하나를 두 곳에: (가) 규칙 쌓임 단분산 구를 누르는 작은 시험의 기하 대조선 — D − D₀ = (3/2)D₀(a/R)² (a/R ≤ 0.25) · 충전율 52.36 / 60.46 / 74.05 % · 이웃 평면이 닿는 임계 밀도 96.51 / 83.51 / 96.41 % (나) 접촉 목록에서 상별 ⟨(a/r)²⟩ 대 상대밀도를 그리고 a/R 0.25 를 넘는 접촉의 몫을 표시 | (가) U6 (해석해가 아니라 균일 재분배 가정의 기하식 — 실측은 같은 a/R 에서 더 치밀했다는 한정과 함께) · (나) 후보 D0 의 신뢰 범위 표지 · 단계 0 | §3-A L53–59 · §6 L203 · §7 L214 · 식 6 · Table I
- [m] deysher2022_transport_mechanical_aspects_assb_review | 이온 · 전자 전도를 나눠 재는 조건: EIS (이온) + DC 분극 (전자 · 낮은 바이어스 ≈ 50 mV) 를 함께 · 혼합 전도체는 전자 차단층 + 복합 탄소 전극이 있어야 함 | 단계 7 의 결과 전 대조 항목 (견줄 실험값의 측정법 조건을 같이 적기) · 흐름 밖: 실험과의 대조 | §6 L147–149 · Fig 6c–e
- [m] deysher2022_transport_mechanical_aspects_assb_review | 적층압을 건 채 FIB 밀링 + 짝 재구성으로 공동 형성을 정량 ([121]) | 단계 6 · 단계 7 (접촉 손실 · 공동의 실험 대조 방법 후보) · 흐름 밖: 열화 | §6 L152
- [m] deysher2022_transport_mechanical_aspects_assb_review | 기공 문턱의 종류 구분: "기공 < 20 % 면 완전 이용률" ([66] Bielefeld) 은 확률적 배치의 입력 기공이지 눌러서 나온 기공이 아니다 | 단계 0 (기공 연산자 · 문헌 대조 규칙) | §3 L82 · §10 L297–298
- [m] deysher2022_transport_mechanical_aspects_assb_review | 인용 규칙: 리뷰의 값은 원전 (ref 번호) 으로 인용 — 예 기공 < 20 % → Bielefeld [66] · 재가압 370 MPa → Koerver [121] | 흐름 밖: 보고 방식 (메모 · 발표의 서지) | §10 L291–292
- [m] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 눌린 뒤 남는 공동의 원인 네 가지를 관측량으로: ① 입경 불일치 (CAM 5–15 µm ↔ SE 1–5 µm) ② 불균일 가압 → 가압 방향에 수직으로 남는 공동 ③ 변형 거동 불일치 ④ 잔류 용매 → 계산 결과에서 공동의 방향성 · AM 주변 몫을 따로 셈 | 단계 5 의 결과 전 대조 항목 (공동의 방향 · 자리) · 단계 7 | §5.1 L124–128 (2 차 인용 — 원전 ref 100 확인 뒤)
- [m] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 재가압 대조: 사이클 뒤 300 MPa 재가압 → 용량 상당 회복 · 저주파 저항 ≈ 1/3 → 접촉 손실이 되돌릴 수 있는 기계 문제인지 가르는 시험 | 단계 6 · 흐름 밖: 열화 (접촉 손실 ↔ 화학 열화 분리) | §5.1 L134 · Fig 8 (ref 105)
- [m] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 응력을 평균이 아니라 조성별 · 위치별 지도로: NCM : SE 비가 오르면 응력이 국소화되고 인장 / 압축 기울기가 날카로워짐 (Fig 11a · ref 37) · 리뷰 문장 *"it is not the decomposition or stress itself but their heterogeneities that trigger and accelerate the degradation"* | 단계 5 · 조건 R7 · 조건 R1 (AM 응력의 분포 · 최댓값 · 자리를 보고) | §6.1 L166 · §6 L178 · §8 L221
- [m] kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review | 작동 중 적층압은 고정값이 아니다: Li–In 셀 ≈ 3.8 MPa 변동 ↔ LTO 셀 ≈ 0.2 MPa (ref 120) | 흐름 밖: 열화 · 작동 조건 · 단계 6 (탈압 뒤 수송 평가 압력을 한 값으로 못 박지 않기) | §6.2 L172 · §9 L263–264

## 카드 문제

(고치지 않고 적는다. ★ = Minnmann 순수 SE 값을 실험 근거로 적은 서술 — 그 출처는 철회됐다.)

**so2022_dem_compaction_coated_particles_assb**

1. 코팅의 전자 가림이 사라지는 압력이 두 값: L14 · L231 "200 MPa 초과 고압에서 사라진다" ↔ L63 · L136 "AM 퍼콜 0.3 @25 → 1.0 @100 MPa" (τ_AM 은 360 MPa 에서 합류 · L65).
2. 기공 ≈ 16–17 % @360 MPa 의 표지가 두 가지: L60 "digitized (Fig 3a)" ↔ L222 "stated (porosity ~16 % …)".
3. L69 의 숫자 (delam 1.3 × 10⁴ · attach 1.8 × 10⁴) 와 비고 ("박리된 SE > 재부착 인데도 순증") 가 맞지 않음 — attached 와 reattach 가 같은 양인지 카드가 가르지 않음 (L137 도 같은 서술). 숫자끼리는 L68 과 맞음 (5.0 + 1.8 − 1.3 = 5.5).
4. 상자 크기: L54 · L122 "20×20 µm" ↔ L134 Fig 2 "box 22.9/23.9 µm" — 둘의 관계 설명 없음.
5. ★ L200 "DEM … 과 MPM … 을 서로가 아니라 각각 실험 (Minnmann) 에 독립 보정" · L166 "검증 앵커 … Minnmann/Doux/Bazzoun (LPSCl) + MPM 독립" — 철회된 출처를 실험 보정 근거로 적음.
6. 우리 쪽 서술의 낡은 표현: L191 "porosity (15.93 %) · 두께 (29.95 µm) … 가 EMERGE" · L200 "수렴 … 은 교차검증" · L197 "Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) sub-µm GB 인자" · "Trevisanello endpoint (10/5)" — CLAUDE.md 가 정정 · 철회한 표현들.
7. 정보 결손: 입자 수 (L54 는 "Table 2 (MethodsX)" 로 넘김) · t_rel · 온도 값이 없음 · AM 이 NCM 인지 LiCoO₂ 인지 "NCM/LiCoO₂" 로만 적음 (L24 · 머리 elements 에는 Ni · Mn 없음) · Sakuda 가 [8] (L43 · L95) 과 [13] (L47) 두 번호로 나옴.

**nisar2024_dem_effective_electrical_conductivity_sps**

8. L38 "5910 kg/m³ (= 5.90 g/cm³)" — 환산이 5.91 이어야 맞음.
9. 소결 시간 L48 "10 min" (Table 1) ↔ L107 "60 min 사이클" (Fig 1 · Sample 1) 의 관계 설명 없음 · L60 "[43] Nosewicz 2013/2017" 연도가 둘 · "3D" 낱말이 카드에 없음 (원통 도메인으로만).
10. 우리 쪽 서술의 낡은 표현: L248 "σ_grain = 3.0 mS/cm (Cronau 2022 단결정)" · L249 "Trevisanello 10/5 mS/cm (LOCKED) … 재료 물성을 문헌에서 고정" · L240 "porosity 15.93 % · 두께 29.95 µm 가 EMERGE" · L143 · L188 "외부 실측은 Bazzoun/Minnmann 차용" (σ_ionic 쪽 — 순수 SE 기공 서술은 아님). [철회된 출처 — 카드에 적힌 것을 옮긴 줄 · 인용 금지]

**doux2020_stack_pressure_assb**

11. 머리 메타 L3 `type DEM` · L12 `methods: dft` ↔ 본문 "실험 (no simulation)" (L361).
12. ★ L304 "우리 SE 자체의 creep / 소성은 별도 근거 (Minnmann pure-SE 10 %, MPM SEM morphology, So 2021 H-cap) 로 정당화" — 철회된 출처를 실험 근거로 적음. 같은 카드 L363 은 "Minnmann 복합 14 %" 라고 적어 서로 다른 두 귀속이 한 카드에 있음 (L290 · L323 · L364 의 "pure-SE ~10 %" 는 우리 모델 값으로 적힘).
13. L202–203 평균 82.1 % ↔ 실측 1.522 g/cm³ ÷ 이론 1.860 = 81.8 % (내 검산 · 0.3 %p 차).
14. 펠릿 밀도의 측정법과 누른 채 / 뺀 뒤가 카드에 없음.
15. L208–209 · L290 · L321–323 · L341: 실험 18 % 를 "우리 강체-구 floor ≈ 20 % 의 실험 확증" 으로 읽는 우리 쪽 해석이 적혀 있음 — 순수 SE 기공 18 % · 기준 밀도 1.860 g/cm³ 은 랩 표준과 다른 문헌 값. L368 "우리 채택 σ_grain 3.0 (단결정-라벨)" · L91 비율 "11 : 16 : 1" 에 wt% 표기.

**sakuda2013_sulfide_mechanical_property**

16. 머리 메타가 둘: L3 `type DEM · digested 2026-07-28` ↔ L9 `type exp · digested 2026-06-26`.
17. 입도 정정이 일부만 반영: L67 "수 µm–10 µm (이전 판 '수~수십 µm' 정정)" ↔ L95 "입자 수~수십 µm" · L201 "정성 '수~수십 µm'".
18. 곡선 판독값이 자리마다 조금 다름: L53 "≈ 60–65 % (≈ 75 MPa) · ≈ 93–95 % (≈ 450)" ↔ L94 "≈ 65 % (≈ 75) · ≈ 95 % (≈ 450)" · Fig 2a · Fig 5 판독은 2026-10-21 원문 대조 때 다시 읽지 않음 (L213).
19. L140 · L173 · L185 가 "우리 DEM pure-SE ~10 % @300" 을 Sakuda stated (> 90 % @ > 350 MPa) 와 "정합" 으로 적음 — 재료 (LPSCl ↔ Li₃PS₄ 유리) · 압력이 다른 값끼리 (카드도 L174 · L188–189 에서 한정). Minnmann 복합 기공이 카드마다 다름: 이 카드 L186 "13–17 %" ↔ doux 카드 L363 "14 %". L190 "절대 porosity 의 소재-특정 정밀값은 LPSCl 쪽 Minnmann/Doux/우리 DEM 이 소유".
20. 우리 쪽 서술의 낡은 표현: L144 "σ_grain 3.0 mS/cm (Cronau LPSCl 단결정)" · L134 "우리 σ_y 0.05–0.30 GPa (soft sulfide)" (CLAUDE.md 는 이 범위를 [미확인 · 카드 없음] 으로 둠).
21. 원문 오식 (카드가 적음): p.3 "18 Pa" → 18 GPa · 참고문헌 15 "McSram" → McSkimin. 셀 전압 L66 "2.8–4.6 V" ↔ L101 Fig 6c "1–5 V 영역" — 뒤쪽이 그림 축인지 카드가 적지 않음.

**lee2024_multiphysics_dem_fem_initial_pressure_assb**

22. DEM 입경 표기 "radius/size" (L65) — 반지름인지 지름인지 불명.
23. DEM 조성 (L133 양극 NMC 60 / LGPS 35 / CB 5 wt%) 과 FEM 초기 부피분율 (L70–71 양극 NMC 0.18 / SE 0.38) 이 같은 조성인지 카드에 없음 — 카드의 밀도 (4750 · 2000 kg/m³) 로 바꾸면 NMC : LGPS ≈ 0.42 : 0.58 (내 검산) ↔ 0.18 : 0.38 = 0.32 : 0.68. L130–131 혼합 균일성의 "부피비 0.695 · 0.682" 가 무엇 대 무엇인지 정의 없음.
24. "내부 압력" (L87 · L211) 과 "von Mises" (L84 · L208) 의 이름 혼용 — 같은 양인지 불명.
25. Doux 가 ref 45 (L167 · 식 36 의 자료 "Doux 2020 ref45 데이터 외삽") 와 ref 6 (L194) 두 번호로 나옴 — 같은 논문인지 카드에 없음 (doux2020 카드에는 σ – 압력 자료가 없고 임피던스만 있음).
26. 원문 인쇄 이상 (카드가 적음): σ_SE0 0.002 > σ_SEmax 0.0002 S/cm (L74 · L417) · D_Li 2.61 × 10⁻⁴ m²/s (L75 · L419). 식 38 의 출처 귀속 [미확인] (L166 정정 2026-10-13).
27. 정보 결손: DEM 의 차원 (2D / 3D) · 제조압 값 · 온도 · 계산 시간 · λ 값이 카드에 없음.
28. 우리 쪽 서술의 낡은 표현: L365 "Cronau 2022 단결정 3.0 mS/cm" · L244 "Minnmann/Doux/Bazzoun 앵커". backlog 번호 B6 이 이 카드 (L34 · L301 "σ-vs-compaction") 와 deysher 카드 (L215 사이클 열화) 에서 다른 뜻으로 쓰임. [철회된 출처 — 카드에 적힌 것을 옮긴 줄 · 인용 금지]

**kakar1967_deformation_theory_hot_pressing**

29. 원문 오식 · 불일치 (카드가 찾아 적음): 능면체 R_c 본문 0.65560 → D 96.59 % ≠ Table I 96.41 % (0.65600 이면 맞음 · §3-D ③) · 체심 θ 35°16′30″ ↔ 정확값 35°15′52″ · Fig 9 캡션의 사파이어 온도 기호가 다른 그림과 다름 · "for a/R = 0.25, R = R₀" 는 문맥상 ≤ · "the vacuum was 0.5 atm" (인쇄 그대로).
30. 카드 간: `mcgeary1961_bimodal_sphere_packing` 카드의 단순입방 충전율 53.36 % ↔ 이 논문 Table I 52.36 % (= π/6) (L331 · 카드가 "확인 필요" 로 적음).
31. L215–216: "이 논문 값을 우리 침대에 댈 때 ε_union 을 쓰면 안 된다" 고 하면서 우리 밀도 띠 0.84–0.95 를 ε_sphere 값 (15.6 % · 13.47 %) 과 union 값 (5.43–9.43 %) 을 섞어 만듦.
32. 원문에 없는 것 (카드가 [미확인] · n/a 로 적음): 실험의 D₀ 정의 · R 측정 방식 · 납의 하중 · 압력 · 다이 치수 · 맞춤 계수와 오차 막대. arzt 카드의 기호 ◇ 미확인 (L29 · L319).

**deysher2022_transport_mechanical_aspects_assb_review**

33. 기공 문턱이 둘 (L82 "< 20 % 필요" · L83 "> 55 % 면 이용률 ↓") — 둘 다 [66] 이고 관계 설명 없음.
34. L91 표지 "stated (digit. Fig 5)" ↔ L301 "digitized" · 머리 메타 L28 `methods: arrhenius, bandgap` (리뷰).
35. 우리 쪽 서술의 낡은 표현: L186 · L248 "frame[4] DEM↔MPM 독립 교차검증 (각각 실험 보정)" · L177 · L200 · L262 · L287 "우리 porosity ~10–15.6 % (pure-SE ~10 %)" (우리 값으로 적힘 — Minnmann 귀속은 아님) · L295 "LPSCl 쪽은 Minnmann 1.6 / Cronau 3.0 이 직접 앵커" (σ 쪽).
36. 카드 간 서로 다른 값: 재가압 370 MPa ([121] Koerver · L81) ↔ kang2026 카드 300 MPa (ref 105 · L134) — 같은 원전인지 두 카드 모두 적지 않음. NMC 부피 변화 1–3 % ([86] · L79) ↔ kang2026 카드 Ni-rich 격자 수축 6–8 % (ref 103 · L132).
37. 원문 쪽 번호가 카드에 없음 (인용문 위치를 절로만 · 같은 인용문을 L118–119 는 §4 입자 처리 자리에 · L231 은 "§1 끝" 이라고 적음).

**kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review**

38. 우리 DFT E_VRH 가 이 카드에는 **52.3 GPa** (L360 · L389 "comp1 ≈ modelc") — CLAUDE.md 는 **22.06 GPa** (modelc 27.66) 로 적음. B₀ 26.2 (L353) 는 같음 → 서로 다른 두 값.
39. L190 옥시설파이드 예시 화학식 "Li₆.₂₅PS₄.₂₅Cl₀.₇₅" 에 O 가 없음 (같은 줄의 Fig 13c 는 Li₆PS₄OCl).
40. L138 · L258 CAM 항복강도 ≈ 100 MPa 의 원전 번호 없음 · L126 "Doux et al., ref 100: 370 MPa … 3D tomography" 가 doux2020 카드 (단층촬영은 Li 침투 관찰 · 기공 18 % 는 밀도 표) 와 같은 논문인지 카드에 없음 · 원문 쪽 번호가 카드에 없음.
