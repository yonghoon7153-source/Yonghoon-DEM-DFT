# batch_15 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` (375 줄) · `beutl2024_round_robin_coin_cell_sulfide_assb` (389) · `bielefeld2019_microstructural_modeling_composite_cathode` (297) · `bielefeld2020_effective_ionic_conductivity_binder` (527) · `chen2011_percolation_micromodel_composite_electrode` (359) · `cooper2017_simulated_impedance_diffusion_porous_media` (417) · `cronk2026_lis_positive_electrode_geometry_fem` (774). 끝까지 못 읽은 카드 없음 (일곱 장 모두 두 – 네 번에 나눠 마지막 줄까지 읽음).

배치의 성격: **실험 둘** (asano2017 = NMC111 + Li₃PS₄ 유리 복합 양극의 전자 · 이온 전도도 / beutl2024 = Li₆PS₅Cl 코인셀 4 기관 round robin · 순수 LPSCl 펠릿 밀도 한 점), **역학 없는 기하 · 해석 모델 셋** (bielefeld2019 = 무작위 배치 + percolation / bielefeld2020 = 같은 기하 위의 복셀 연속체 이온 수송 + 바인더 / chen2011 = SOFC 전극의 해석적 percolation 식), **수치 방법 하나** (cooper2017 = 복셀 확산 임피던스), **FEM + 실험 하나** (cronk2026 = Li–S 양극 · 선형탄성 + eigenstrain). **DEM 을 쓴 카드도 MPM 을 쓴 카드도 없다.** 압력별 기공 곡선을 준 카드는 없고, 순수 LPSCl 은 beutl2024 의 360 MPa · 다이 밖 한 점뿐이다. 압력을 뺄 때 되돌아온 양을 잰 카드도 없다. 그래서 k (DEM 의 한계) 는 "DEM 논문의 자기 고백" 이 아니라 (1) 강체 기하 모델이 스스로 적은 한계, (2) 실험이 말한 강체 구 가정 밖의 것, (3) 카드의 풀이로 나눠 적었다. l (소성) 에서 인용문이 있는 것은 cronk2026 (관측은 소성 · 모델은 탄성) 과 asano2017 (성형성) 이다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `stated(그림)` · `판독` · `파생` · `[인쇄]` · `[판독]` · `[우리 산술]` · `[추정]` · `[미확인]` · `digitized` · `derived(ours)` · `우리 유도` · `우리 재계산`) · 없으면 "표지 없음". 따옴표 안 영어 문장은 카드가 옮겨 둔 원문이다. "카드 서술 · 카드의 풀이 · 우리 해석" = 논문 문장이 아니라 카드 작성자의 서술. "내 검산 · 내 산술" = 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님). "랩 표준과 다른 문헌 값" = 순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ 과 다른 값이라는 표시 (기준은 그대로다).

형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계` (k · l 은 slug 옆에 인용할 서지 · m 은 `무엇을 | 우리 쪽 어디에 | 근거 위치`)

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

압력별 곡선이 있는 카드 = **0**. 순수 LPSCl 을 잰 카드 = **1** (beutl2024 — 360 MPa **한 점** · 질량 ÷ 기하 부피 · 다이에서 **꺼낸 뒤**).

- [a] beutl2024_round_robin_coin_cell_sulfide_assb | 순수 Li₆PS₅Cl (NEI "LPSCl fine") 펠릿 100 mg · ⌀10 mm · 예압 50 MPa → 360 MPa 한 점: 겉보기 밀도 *"1.6–1.50 g cm−3"* (p.5) / *"at least 1.49 g cm−3"* (p.9) · 상대밀도 RC1 > 91 · RC2 > 94 · RC3 > 93 · RC4 > 93 % | §3-2 L78–87 · §3-4 Table 2 L121–126 · 논문 p.4–5 · p.9 | [인쇄] | 압력 한 점 (곡선 아님) · 4 기관 각 한 값 (n · SD 없음) · 범위 하한이 1.50 ↔ 1.49 로 본문 안 불일치 · 예압 50 MPa 의 밀도 미보고
- [a] beutl2024_round_robin_coin_cell_sulfide_assb | 진밀도 (분모) · 질량 기준 · 상태: 분모 = *"crystallographic density of Li6PS5Cl is 1.64 g cm−3"* [10,37] (p.9 · p.5 는 [37]) — 이 논문이 재거나 계산한 값이 아님 (격자상수 정련 · 비중병 없음) · 밀도 = 질량 ÷ 기하 부피 (*"use the weight and geometric volume of the sample to calculate its apparent density and further compare it with the reported crystallographic one"*) · 두께는 압력을 뺀 뒤 (*"After removing the sample from the die set a free-standing pellet with a thickness of approximately 0.8 mm is obtained."*) | §3-2 L83–85 · §3-3 L102–103 · 논문 p.4 · p.5 · p.9 | [인쇄] (인용문은 텍스트 층에서 그대로 · L376) | 분모 1.64 는 랩 표준과 같은 값 · 그 값의 출처 ([37] Zhou 2019 ACS Energy Lett. 4, 265 · [10] Tron 2023 Nanomaterials 13, 327) 는 원문 미확보 [미확인] · 두께 측정 도구 · 오차 [미확인]
- [a] beutl2024_round_robin_coin_cell_sulfide_assb | 같은 펠릿을 공극으로 읽은 값 (카드 계산): ε = 2.4–9.1 % (진밀도 1.64) ↔ 14.0–19.9 % (진밀도 1.86) · 함축 두께 0.796–0.855 mm · ln(1/(1 − D)) = 2.39–3.71 (1.64) / 1.61–1.97 (1.86) @360 MPa | §3-2 L89–99 · §7-2 ⑤ L309 | [우리 산술] | 1.86 (결정학 산술 · Z = 4 · a ≈ 9.86 Å) · 1.874 (Ohno 2020 비중병 · 카드 인용) · 1.87 (Frankenberg 2025 같은 이름 분말 · 카드 인용) 은 **랩 표준과 다른 문헌 값** · 1.64 기준 2.4–9.1 % 는 360 MPa · 다이 밖이라 랩 기준 (10–13 %) 과 압력 · 상태가 같은 점이 아님
- [a] beutl2024_round_robin_coin_cell_sulfide_assb | 카드가 300 MPa 로 옮긴 어림: 같은 계열 ρ ≈ 1.41–1.54 g/cm³ (ε × e^(K·60) · K ≈ 32 × 10⁻⁴ MPa⁻¹) — 랩 기준 창을 1.64 로 정의한 밀도 1.427–1.476 g/cm³ (0.1 g · ⌀10 mm 면 두께 0.892–0.863 mm) 이 그 안에 듦 | §7-2 ⑤ L300–307 | [우리 산술 · 어림] (K 는 다른 카드 lee2025_heckel 의 다른 분말 · 다이 안 값) | 300 MPa · 다이 밖 실측은 없음 (카드: "확인은 아님") · 인용 불가
- [a] beutl2024_round_robin_coin_cell_sulfide_assb | 순수 SE 펠릿의 σ_ion (25 °C · 측정 중 ≈ 0.2 MPa (인용값) · 두께 ≈ 0.8 mm): SS|SE|SS 0.3 · 0.4 · 0.3 · 0.3 mS/cm (RC1–4) · Al/C|SE|Al/C 0.4 · 0.4 · 0.3 (RC2–4) · Al/C 를 360 MPa · 3 min 함께 누른 셀 1.8 (RC3 · Table 2) ↔ 본문 *"1 × 10−3 S cm−1"* | §3-4 L119–134 · Table 2 · 논문 p.9 | [인쇄] | 표 1.8 ↔ 본문 1 불일치 · 한 자리 유효숫자 · 압력 · 온도 계열 없음
- [a] cronk2026_lis_positive_electrode_geometry_fem | 순수 SE 압력별 기공 없음. 닿는 값: FEM 입력 ρ_SE = 1.6 g/cm³ (Table S6) · 비에너지 계산의 가정 "SSE 상대밀도 85 %" (Table S8) · 분리막 = 3 ton (375 MPa) · 3 min → 450–500 µm (질량 없음 → 밀도 못 냄) · LPSCl 촉매전해질 σ = 2 mS/cm (Ti|composite|Ti · 75 MPa · 25 °C · Fig S8a) | §2 L58 · §4.2 L221 · §6.1 L401 · §6.7 L510–526 · §10-11 L661–663 | stated (Table S6 · S8) · σ 는 표지 없음 | ρ_SE 1.6 은 **랩 표준과 다른 문헌 값** (출처 표기 없는 FEM 입력) · 85 % 는 가정치 (카드: "측정도, 양극 미세구조 값도 아니다")
- [a] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 순수 SE (Li₃PS₄ 유리) 의 기공 – 압력 자료 없음. 카드가 옮긴 다른 논문 값만: 같은 그룹 [13] (Sakuda 2013) 의 같은 조성 유리 "상대밀도 > 90 % @ > 350 MPa · 냉간 360 MPa 펠릿 σ 3.1 × 10⁻⁴ · 열간 프레스 3.4 × 10⁻⁴ S/cm" | §3-1 L69 | "sakuda2013 카드 (stated)" | 이 논문의 값이 아님 · 유리 (LPSCl 아님) · 이 논문의 순수 SE σ₀ 4 × 10⁻⁴ S/cm @25 °C 는 측정 셀 · 압밀 · 밀도 미기재 (L67)
- [a] bielefeld2019 · bielefeld2020 · chen2011 · cooper2017 | 해당 없음 — 기공은 입력이거나 (bielefeld 5 / 10 / 15 / 20 % · chen 30 %) 없음 (cooper) | — | — | —

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

되돌아온 두께 · 기공을 잰 카드는 **이 배치에 없다**. 가까운 것 = 압력을 뺀 뒤의 한 상태만 잰 펠릿 (beutl2024) · 제조압과 작동압을 따로 적은 셀 (cronk2026).

- [b] beutl2024_round_robin_coin_cell_sulfide_assb | 되돌아온 양은 재지 않음. 잰 것은 압력을 뺀 뒤의 한 상태: 다이에서 꺼낸 자유 펠릿 두께 ≈ 0.8 mm (하중 중 두께가 없어 차를 낼 수 없음) | §0 L33 ④ · §3-2 L83 · §7-3 L315 · 논문 p.4 | [인쇄] (두께) · "꺼낸 뒤 (스프링백 · 취출 포함)" 은 카드 서술 | 측정 도구 · 오차 [미확인] · "하중 중 두께 · 언로딩" 은 카드가 이 논문에 없는 것으로 적음
- [b] beutl2024_round_robin_coin_cell_sulfide_assb | 카드가 붙인 우리 쪽 어림 (논문 값 아님): 다이 안으로 옮기면 "회복 1.6–7 % 만큼 더 치밀 (−1.4 – −4 %p, 세대 2 계획 표 B)" | §7-2 ⑤ L305 | [우리 산술 · 어림] | 근거 식 · 자료가 이 카드에 없음 (작업 브랜치 계획 문서를 가리킴) · 인용 불가
- [b] beutl2024_round_robin_coin_cell_sulfide_assb | 압력을 뺀 뒤 (코인셀 ≈ 0.2 MPa) 에서 잰 수송: *"In a recent study, the pressure inside a CR2032 setup was determined as 0.2 MPa,[15] considering a total sample thickness of 1.9 mm (without the spring)"* · 그 상태의 σ_ion 0.3–0.4 mS/cm ↔ 전극을 360 MPa 로 함께 누른 셀 1.0–1.8 mS/cm · 카드: "코인셀 자료와 맞대려면 언로딩 끝 상태가 대응 상태" | §3-1 L67 · §3-4 L130–134 · §7-1 L271 · §8-5 L324 | [인쇄] · 대응 상태는 카드 판단 | 0.2 MPa 는 이 논문이 잰 값이 아님 · 재료의 접촉 손실과 전극 접촉 규약이 갈리지 않음
- [b] cronk2026_lis_positive_electrode_geometry_fem | 탈압 되돌아옴 측정 없음. 닿는 것: 제조압 (375 MPa · 파우치 WIP 500 MPa @80 °C) 과 작동압 (75 MPa · 10 MPa) 을 따로 적음 · operando 적층압 변화 (75 MPa 기준 |Δ| ≈ 1.6 MPa (LiSi‖S) · 밴드 ≈ 0.4 (µSi‖Li₂S) · +4.7 (LiSi‖LCO)) 는 사이클 부피 변화 · FEM 은 "1st 리튬화 1회 스냅샷 — 사이클 누적·springback·재습윤 없음" | §2 L58–60 · §6.6 L487–495 · §10-13 L666 | digitized · TREND only (압력) | 리튬화 팽창 (탈압 아님) · Li–S
- [b] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 이 카드에 없음 — "성형 360 MPa 실온 · 측정 하중 · 5 층 셀 조건 미기재 → springback 이력 비교 불가" | §7 L245 · §8-1 L266 | 카드 판단 | —
- [b] bielefeld2019 · bielefeld2020 · chen2011 · cooper2017 | 이 카드들에 없음 (역학 없음) | — | — | —

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산

황화물 SE 의 항복 · 경도 · 크리프 값을 준 카드는 **없다**. 있는 것은 탄성 입력뿐 (cronk2026: LPSCl E 22 GPa · ν 0.3 / bielefeld: ≈ 25 GPa). **일축 항복 세기로의 환산은 어느 카드에도 없다.**

- [c] cronk2026_lis_positive_electrode_geometry_fem | 항복 · 경도 · 크리프 값 없음 — FEM 파라미터 표에 "항복응력 σ_y 없음 · 경화 없음 · 소성 없음 · 파괴/CZM 없음" (카드 서술). 탄성 입력: E_SE 22 GPa · ν_SE 0.3 (LPSCl) · E_S 17.8 GPa · ν_S 0.32 (황) | §4.2 L214–227 · SI p43 Table S6 | stated (표) · "없음" 은 카드의 표 전수 확인 | ν 0.3 은 출처 표기 없는 FEM 입력 (L14) · 측정값 아님
- [c] cronk2026_lis_positive_electrode_geometry_fem | LPSCl 탄성상수 대조 (카드 계산): Cronk FEM E 22 · ν 0.3 → G 8.462 · K 18.333 GPa / Deng 2016 (논문 ref 57) E 22.1 · ν 0.37 · G 8.1 · K 28.7 / 우리 DFT E 22.06 · ν 0.360 · G 8.11 · B₀ 26.23 — E 는 0.3 % 안 · K 만 −30~−36 % (ν 선택 탓) · 계면 von Mises 에 주는 영향은 ≈ +12 % | §4.7 L296–317 | derived(ours) | 탄성만 · 일축 항복 환산 없음
- [c] cronk2026_lis_positive_electrode_geometry_fem | 소성 개시와 닿는 논문 문장: *"The plastic deformation of the SSE matrix is not surprising, as the simulated stresses estimated above is **near the shear modulus of LPSCl**"* (p10 · ref 57 = Deng 2016) — 계산된 von Mises 평균 2.42 / 2.40 GPa · *"beyond 5 GPa"* · 꼬리 8 GPa ↔ G 8.1 GPa (평균은 G 의 30 % — 카드 계산) | §5.1 L331–335 · §5.2 L344–346 | stated (인용문 · 그림 주석) · 비율은 derived(ours) | 선형탄성 · 기공 0 · 경계 고정의 상한 응력 — 항복 세기 값이 아님
- [c] cronk2026_lis_positive_electrode_geometry_fem | 파괴 쪽 환산 (카드 계산): K_IC 0.3 MPa·m^½ (Fan 2026 의 0.2–0.4) → 임계 결함 a_c ≈ K_IC²/(πσ²) = 0.8 nm @6 GPa · 5 nm @2.4 GPa · G_c 환산 3.24 J/m² (E 24 사용) | §5.2 L368–374 | derived(ours) | 2 차 인용 + 카드 계산 · 항복 아님
- [c] bielefeld2019_microstructural_modeling_composite_cathode | E_SE ≈ 25 GPa (LPS · 논문 refs 32–34) — SE 다면체의 겹침을 허용하는 근거 ("낮은 영률 + 연성") 로만 쓰고 계산에는 안 씀 | §3 L59 · §4 L71 · 논문 p.1628 | stated | thiophosphate 일반 (LPSCl 특정 아님) · 항복 · 경도 없음
- [c] bielefeld2020_effective_ionic_conductivity_binder | 같은 근거를 이어 씀: "LPS의 낮은 Young's modulus ~25 GPa·연성을 기하 겹침으로 근사" | §2.1 L106–108 | 표지 없음 (카드 서술) | 항복 · 경도 없음
- [c] beutl2024_round_robin_coin_cell_sulfide_assb | SE 값 없음. 다이 재료만: *"compressive strength of PEEK is around 118–130 MPa[38]"* (자작 PEEK 다이는 고압 치밀화를 못 견딜 수 있다) | §3-2 L87 · 논문 p.5 | [인쇄] | 다이 재료 (공급사 자료 인용)
- [c] asano2017 · chen2011 · cooper2017 | 이 카드들에 없음 (chen2011: "E·ν·μ·COR·σ_y 전혀 없음" L82) | — | — | —

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

하중 몫을 수로 준 카드는 **없다** (가압 역학을 계산하거나 잰 카드가 없다). 닿는 것만 적는다.

- [d] cronk2026_lis_positive_electrode_geometry_fem | 하중 몫 없음 (압밀 모델 없음). 닿는 결과: 팽창하는 개재물 (S) 둘레의 기지 (LPSCl) 응력이 입자 표면 껍질에 몰림 — *"most of the SSE matrix does not experience stress since only 30 wt% of sulfur is used"* · 히스토그램 이봉 (0 근처 + ≈ 4.1–4.3 GPa) | §5.1 L324–333 | stated (인용문) · 봉 위치는 그림 읽기 | 가압이 아니라 리튬화 팽창 · 선형탄성 · Li–S
- [d] beutl2024_round_robin_coin_cell_sulfide_assb | 수치 없음. 논문 서술 (카드의 한국어 옮김): "복합 양극 치밀화에는 보통 300–800 MPa 를 쓰고 그 응력이 활물질을 깬다 · 단결정이 더 견딘다 · 가압 순서가 계면 품질에 중요" | §4-1 L197 · 논문 p.5–6 | 카드 옮김 (서술) | 정성 · 하중 몫 아님
- [d] bielefeld2019_microstructural_modeling_composite_cathode | 역학 없음. 재밍과 닿는 기하 한계만: 겹침 없는 단일 크기 구 AM 은 ≈ 65 vol% 에서 겹침 ≈ 1 vol% 가 남음 (등구 조밀 충전 ≈ 74 vol% 근접) | §3 L57–58 · §5.2 L99 · 논문 p.1628 | stated | 기하 배치 (힘 없음)
- 나머지 (asano2017 · bielefeld2020 · chen2011 · cooper2017): 이 카드들에 없음.

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값의 수

**이 배치에 없음** — 기계 접촉 법칙을 쓴 카드가 없다 (cronk2026 FEM 표에는 "마찰/접촉 없음" · L227).

- [e] chen2011_percolation_micromodel_composite_electrode | 참고 (힘 법칙 아님): 접촉을 기하로만 정의 — 접촉각 θ (예시 29.5° · 자유 파라미터) 로 접촉 둘레 2π·min(r)·sinθ · 면적 π(min(r)·sinθ)² | §3 L67 · §5.2 L118 · L127 | stated | 겹침 · 변형 개념 없음 · SOFC

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

MPM 을 쓴 카드는 **없다**. 복셀 · FEM 계산의 해상도 규칙과 오차 추정법만 적는다.

- [f] cooper2017_simulated_impedance_diffusion_porous_media | 복셀 유한차분의 격자 규칙: 가장 작은 특징 = 5 × 5 voxel ("격자 무관 해를 위해" · Sierpinski carpet) — 수렴 자료는 없음. 오차 추정법 = 해석해 대조: 곧은 개방 기공은 tanh(s)/s, 곧은 폐쇄 기공은 coth(s)/s (저주파 실수부 1/3 · 그림 판독 0.330) 를 되찾아야 함 | §3-2 L77 · §3-6 L112–117 · §4-5 L157 · §4-7 L181 · 논문 p.683 | stated (규칙) · 우리 재계산 (해석해 값) | MPM 아님 · 확산 문제 · 카드 계산: 주파수 창 상한에서 침투 깊이 ≈ L/45 → L = 128 voxel 이면 ≈ 2.8 voxel (우리 산술 · L254)
- [f] cronk2026_lis_positive_electrode_geometry_fem | 해상도를 적지 않은 사례와 그 귀결: voxel 크기 · 주기경계 · 겹침 · 시드 · 메시 크기가 본문 + SI 에 0 건 (카드의 전수 grep) · 복셀 껍질 분율 f ≤ 3h/R → 보고값 87.6 % 면 R/h ≤ 3.4 (sub-micron 입자가 반지름 3 셀 이하) · 상자 변당 입자 지름 개수 2.0–2.5 (Bulk) / 6.7 / 18.7 · 수치 오차 추정 없음 (3 반복인데 산포 미보고 · 상자 수렴 검사 없음) | §3.2 L87–98 · §3.3 L100–112 · §3.4 L134–147 | derived(ours) · 미기록은 카드 확인 | MPM 아님 · FEM 요소 크기도 미기록
- [f] cronk2026_lis_positive_electrode_geometry_fem | 카드가 옮긴 우리 쪽 규칙: d_h/dx ≳ 3.5 (좁은 채널 2.65 셀이면 격자 정밀화에 +23.8 % · 7.71 셀이면 +4.0 %) | §3.5 L183–184 | 우리 쪽 값 (카드 표기 "CLAUDE.md 2026-08-07") | 논문 값 아님
- [f] bielefeld2019 · bielefeld2020 | 복셀 0.2 µm → "3 µm 입자까지 합리적" · "입경 3 µm 가 모델 하한" (지름당 15 voxel — 내 산술) · 수치 오차 추정은 카드에 없음 (2020 의 검증은 실측 한 점: 0.68 ↔ 0.73 mS/cm) | bielefeld2019 §3 L60 · §5.2 L102 · bielefeld2020 §2.4 L160–162 · §3.1.1 L211 | stated | MPM 아님
- [f] chen2011_percolation_micromodel_composite_electrode | 격자 없음 (해석식). 이산화 인공물 하나: 입경 분포를 9 크기로 나누면 곡선에 여러 전이가 생기고 "더 많은 크기로 표현하면 사라짐" | §5.4 L141 | 카드 서술 | —

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] cooper2017_simulated_impedance_diffusion_porous_media | 같은 2D 틀을 기둥 (prismatic 2D) 과 회전체 (축대칭 3D) 로 만들어 견줌 (Keiser 폐쇄 기공 5 개 · 그림 1): "3D 가 2D 보다 형상 효과가 크다" · Keiser 1976 결과는 이 논문의 2D 와 3D 사이 | §5 L213 · §6-bis L230 · 논문 p.684–685 | 표지 없음 (그림 설명) | 확산 임피던스 (역학 아님) · 차이의 크기 수치는 카드에 없음 (정성)
- [g] cooper2017_simulated_impedance_diffusion_porous_media | 차원을 줄인 모델의 오차 방향: 1D 균질화 (pseudo-3D) 는 3D 보다 저주파 저항을 과소 — Z̃′(ω = 0) 14.0 ↔ 17.3 (단면비 0.01) · 3.0 ↔ 3.0 (1) · 1.7 ↔ 2.2 (3) → −19 % · 0 · −23 % · 이유 = 등농도면이 흐름에 수직이라는 가정 (가로 확산 무한대) | §3-3 L82–88 · §4-6 L171 · 그림 6 (p.687) | stated(그림) · 비는 우리 재계산 | 그림 6 의 정규화 (A · L) 미기재 → 비만 씀 · 1D ↔ 3D (2D ↔ 3D 아님)
- [g] cooper2017_simulated_impedance_diffusion_porous_media | 카드의 경고: "2D 사례는 개념 증명 — 절대 크기 전이 금지" · "2D 사례가 대부분 (그림 1–3 · 6) … 3D 는 Keiser 회전체 · 구배 구 충전 하나 · 분리막 영상 둘" | §7 L252 · §10 L354 | 카드 서술 | —
- [g] cronk2026_lis_positive_electrode_geometry_fem | 2D → 3D 로 옮긴 사례: eigenstrain 계수 β_H 를 *"a **2-D simulation** consisting of the exact same model for a **single S particle**"* 로 목표 부피팽창에 맞춘 뒤 3D 전극 FEM 에 씀 — 2D ↔ 3D 차이에 대한 검토 · 경고는 카드에 없음 | §4.1 L207 · §9 L623 | stated (인용문) | 팽창 계수 보정 (접촉 아님) · 카드는 "β_H 값은 이식 불가능 (C_Li 미기재)" 만 지적 (L280)
- [g] bielefeld2020_effective_ionic_conductivity_binder | 3D 계산 — 2D 결과 없음 ("본 논문 3D … 우리 3D 와 차원 일치") | §10 L493 | 카드 서술 | —
- 나머지 (asano2017 · beutl2024 · bielefeld2019 · chen2011): 해당 없음.

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

DEM 에서 넘긴 선례는 **이 배치에 없다** (DEM 을 쓴 카드 0). 닿는 것:

- [h] cronk2026_lis_positive_electrode_geometry_fem | 생성 기하 (DEM 아님) → FE 로 넘긴 사슬: MATLAB 확률적 voxel 기하 (S = 구 · 탄소 = aggregate · 기공 10 vol% 입력) → Iso2Mesh 로 사면체 메시 → COMSOL 6.1 Solid Mechanics. 넘기면서 기공을 지움 (*"the electrode was assumed to be **fully compact (no porosity)**"*) · 박스도 25 / 10 µm 로 그려져 생성 상자 (50 / 15 µm) 와 다름 (본문 언급 없음) | §3.2 L97 · §4.1 L207 · §4.4 L241–245 · §9 L618–622 | stated (인용문) · 박스 불일치는 카드 관찰 | 넘긴 시점 = 생성 직후 (압밀 없음) · 넘길 때 기하가 바뀌었는데 어느 상이 기공을 흡수했는지 미기록
- [h] bielefeld2019 → bielefeld2020 | 같은 무작위 배치 기하 위에서 percolation 세기 (2019) → 복셀 연속체 flux 풀이 (2020) 로 넘어감 — *"We use the AM microstructures generated in our **previous work**"* | bielefeld2020 §2.1 L105 | stated (인용문) | DEM · 역학 아님 (수송 솔버만 더함)

## i. 복합 양극 (AM + SE) 의 압력별 기공

복합 양극의 압력별 기공을 준 카드 = **0**.

- [i] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 기공 미보고 — *"NMC volume ratios of 48%, 55% and 62%"* 뿐 · 기준 (고체 / 전체) · 밀도 · 시료 질량 없음 · 압밀은 360 MPa · 실온 한 조건 | §0 L30 · §3-1 L73–75 · §6 L196 · 논문 p.A3960–A3961 | stated (조성 · 압력) · 미보고는 카드 확인 | Li₃PS₄ 유리 + NMC111
- [i] beutl2024_round_robin_coin_cell_sulfide_assb | 복합 bilayer (양극 10 mg 을 SE 100 mg 위에 360 MPa · 2–3 min) 의 기공 값 없음 · 조성 57:40:3 wt% (본문 vol% "65:31:4" 는 이름 순서가 뒤바뀐 것으로 카드가 계산) | §3-3 L115 · §3-7 L162 | [인쇄] · 순서 뒤바뀜은 [우리 산술] | 기공 없음
- [i] cronk2026_lis_positive_electrode_geometry_fem | 양극 기공 실측 0 건 — 모델은 10 vol% 입력 · 실험은 *"an increase in porosity"* 정성 서술 | §3.2 L98 · §10-11 L661–664 | stated · 카드 확인 | Li–S
- [i] bielefeld2019 · bielefeld2020 | 기공은 입력 — 압력과의 관계 없음. 입력 기공에 대한 결과만: 이상 조성 62/38 → 66/34 → 72/28 vol% (porosity 5 → 10 → 20 %) · 5 % void 가 20 % void 대비 σ_eff 2 배 @고-AM | bielefeld2019 §3 L48 · bielefeld2020 §3 L246–251 | stated (2019) · 표지 없음 (2020) | 압력 없음
- chen2011 (porosity 30 % 입력) · cooper2017: 해당 없음.

## j. 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)

가압 · 탈압을 계산한 카드가 없어, 한계 문장은 대부분 "역학을 건너뛰었다" 쪽이다.

- [j] bielefeld2019_microstructural_modeling_composite_cathode | 저자가 뒤로 미룬 것: 입자 – 입자 계면 저항과 협착 저항 — *"do not take into account possible resistances occurring at particle–particle interfaces and constriction resistances ... regarded as a large number of interacting microcontacts"* (p.1629 · ref 36 = Greenwood 1966) · 입경 분포 (bi/tri-modal) 는 향후 과제 · 실셀은 시간에 따라 변함 (입자 균열 · 부피 변화) — 범위 밖 | §4 L74 · L76 · §5.6 L130 | stated (인용문) | 가압 · 탈압 계산은 애초에 없음 (porosity = 입력) → 한계 문장은 수송 쪽
- [j] bielefeld2019_microstructural_modeling_composite_cathode | 얇은 전극의 "겉보기 favorable" 은 유한크기 효과 — 긴 확산 경로 · 충방전 성능은 "이 모델이 못 반영" | §5.5 L124 · §10 L291 | 카드 옮김 | —
- [j] bielefeld2020_effective_ionic_conductivity_binder | 카드가 든 한계: (i) 연속체 flux 풀이라 SE–SE 점접촉 협착이 없음 (ii) porosity · 조성 · 입경 = 입력 ("소성-보정 없음, 입력값") (iii) 분포는 trimodal 한 경우 · 전류 추정은 "good case" (전하전달 · AM 확산 무시 — 저자 명시) | 머리 L66–69 · §5 L332 · §10 L470–492 | 카드 서술 ("저자 명시" 는 L491) | 가압 · 탈압과 닿는 것은 (ii) 뿐
- [j] cronk2026_lis_positive_electrode_geometry_fem | 저자 명시: *"These simulations only capture stress after the 1st lithiation"* · FEM 가정 *"fully compact (no porosity)"* · *"uniformly lithiated"* · *"the external boundaries of the electrode were fixed"* | §4.1 L207 · §4.5 L266 | stated (인용문) | 리튬화 팽창 계산 (가압 아님) · "사이클 누적·springback·재습윤 없음" 은 카드 정리 (L666)
- [j] beutl2024_round_robin_coin_cell_sulfide_assb | 실험의 빈 곳 (카드 정리): 압력 계열 · 하중 중 두께 · 언로딩 · 단면 공극 영상 · 접촉 정량 없음 · 코인셀 내부 압력은 "측정 · 조절 불가" | §4-5 L220 · §7-3 L315 | 카드 서술 | —
- [j] cooper2017_simulated_impedance_diffusion_porous_media | 저자 명시: 대류 · 전기 이동 · 이중층 없음 (그건 PNP 모델 필요) · 실측 EIS 대조는 후속 · 임피던스로 구조를 되짚는 것은 유일하지 않음 | §4-7 L176 · §6 L225 · §10 L352 | stated | 가압 · 탈압과 닿지 않음
- [j] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 원문 서론이 적은 DC 법의 위험: *"The DC technique possibly causes the resistance including interfacial resistance when non-negligible resistance exists at the interface between the electrode and the solid electrolyte (SE) or between the SE and composite sample layer."* (p.A3960) | §4-1 L143 | stated (인용문) | 측정 한계 (가압 · 탈압 아님)
- chen2011: 가압 · 탈압과 닿는 한계 문장 없음 (역학 없음).

## k. DEM 의 한계 (논문이 직접 말한 문장 · 수치)

**DEM 을 쓴 카드가 없다** → "DEM 논문이 스스로 적은 한계" 로 인용할 문장 · 수치 (믿을 수 있는 겹침 · 상대밀도의 상한 등) 는 이 배치에 없다. 아래는 (1) 힘 없는 강체 기하 모델이 적은 한계 (bielefeld2019), (2) 실험이 말한 "강체 구 가정 밖의 것" (asano2017 · beutl2024), (3) 카드의 풀이다 — 인용할 때 셋을 구분한다.

- [k] bielefeld2019_microstructural_modeling_composite_cathode (A. Bielefeld, D. A. Weber, J. Janek, J. Phys. Chem. C 2019, 123, 1626–1634) | DEM 아님 (힘 없는 기하 배치) — "단단한 입자 · 점접촉" 그림이 놓치는 것을 수송 쪽에서 직접 적은 문장: *"do not take into account possible resistances occurring at particle–particle interfaces and constriction resistances ... regarded as a large number of interacting microcontacts"* (p.1629 · ref 36 = Greenwood 1966) | §4 L74 · A.1 L177 | stated (인용문 · 가운데 생략은 카드 그대로) | 수송 (접촉 저항) 에 대한 말 — 가압 역학의 한계 문장이 아님
- [k] bielefeld2019_microstructural_modeling_composite_cathode (같은 서지) | 겹침 없는 강체 구 배치의 밀도 상한: AM 겹침을 되풀이해 지워도 ≈ 65 vol% AM 에서 ≈ 1 vol% 가 남음 (등구 조밀 충전 ≈ 74 vol% 근접 · ref 31) · 그래서 SE 는 "낮은 영률 (~25 GPa) + 연성" 을 근거로 겹침을 허용한 볼록 다면체로 둠 | §3 L57–59 · §4 L77–78 · §5.2 L99 · 논문 p.1628 | stated | 압력과 무관한 기하 침투 ("겹침은 기하 침투지 변형 흐름 아님" 은 카드 서술 L78)
- [k] bielefeld2020_effective_ionic_conductivity_binder (A. Bielefeld, D. A. Weber, J. Janek, ACS Appl. Mater. Interfaces 2020, 12, 12821–12833) | DEM 아님 — 말 없음. 카드 서술만: SE 겹침 = "기하 근사 (연성 흉내), SHAPE flow ✗" · porosity 는 "소성-보정 없음, 입력값" | §5 L332 · §6.1 L355 | 카드 서술 | 논문 문장 아님
- [k] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity (T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, M. Tatsumisago, J. Electrochem. Soc. 164 (14) A3960–A3963 (2017)) | DEM 안 씀 (실험) — DEM 에 대한 말 없음. 강체 구 가정 밖의 것을 실험이 말한 문장으로 인용 가능: *"As expected, these are larger than those using a liquid electrolyte, but they are rather small considering that they are tortuosity of room temperature molded bodies of an inorganic solid powder. This is due to the high formability of the sulfide solid electrolytes.[13]"* (p.A3963) | §3-5 L115 · §4-5 L167 | stated (인용문) | Li₃PS₄ 유리 (LPSCl 아님) · 형태 증거 (SEM · 기공) 는 이 논문에 없음 · "우리 강체구 DEM 에 없는 입자 형상 소성" 은 카드의 해석 (L167)
- [k] beutl2024_round_robin_coin_cell_sulfide_assb (A. Beutl, A. Orue, P. López-Aranguren, A. I. Pitillas Martinez, M. H. Braga, V. Kekkonen, A. Tron, Electrochem. Sci. Adv. 2024, 4, e2400004) | DEM 안 씀 (실험) — 말 없음. 구 입자 모델이 놓치는 것으로 쓸 수 있는 관찰: 공급사 "∼1 µm" 는 1 차 입자이고 SEM (5 µm 막대) 에서는 수 – ≈ 20 µm 응집체 · 같은 이름 분말의 레이저 x50 17 ± 2 µm (다른 카드 인용) → 실제 다짐은 "응집체 해체 + 재배열" 을 지남 | §3-1 L70–71 · §7-2 ⑤ L311 · §8-7 L326 | [인쇄] (1 µm) · [판독] (응집체) · [추정] (기전) | 논문은 기전을 나누지 않음 (L215) · 응집체 해석은 카드의 것
- [k] beutl2024_round_robin_coin_cell_sulfide_assb (같은 서지) | "밀도가 맞는 것 ≠ 구조가 맞는 것" 의 실험 사례: RC2 는 상대밀도 하한이 가장 높았는데 (> 94 %) Li|Li 는 가장 먼저 단락 (175 h) — 저자: *"The quality of the prepared electrolyte pellets, especially parameters like porosity and remaining defects, can highly influence dendrite formation and propagation"* | §3-5 L138–140 · §7-2 ④ L294 · §8-6 L325 | [인쇄] (값 · 인용문) | "DEM 에서도 공극이 맞는 것이 결함 · 접촉 · 파괴 구조가 맞는 것을 뜻하지 않는다" 는 카드의 적용 문장
- [k] chen2011_percolation_micromodel_composite_electrode (D. Chen, L. Lu, J. Li, Z. Yu, W. Kong, H. Zhu, J. Power Sources 196 (2011) 3178–3185) | DEM 안 씀 (해석식) — 말 없음. 전제만: 강체 구의 무작위 조밀 충전 · 평균 배위수 6 가정 · 접촉은 둘레 / 면적 기하 ("겹침·overlap 개념조차 없음" 은 카드 서술) | §4 L81 · L93–94 | stated (가정) · 카드 서술 | SOFC
- [k] cooper2017_simulated_impedance_diffusion_porous_media (S. J. Cooper, A. Bertei, D. P. Finegan, N. P. Brandon, Electrochim. Acta 251 (2017) 681–689) | DEM 안 씀 — 말 없음. 카드의 풀이 (논문 문장 아님): 접촉망은 "입자 하나 = 노드 하나라 l_δ < 입자 크기 영역을 원리적으로 못 그린다" | §7 L254 | 우리 해석 | 임피던스 (역학 아님)
- [k] cronk2026_lis_positive_electrode_geometry_fem (A. Cronk 외 18 인 · 교신 J. B. Lee · Y. S. Meng, Nat. Commun. 17:3298 (2026)) | DEM 안 씀 — 말 없음. 기하 생성기에서 S 는 "강체 구, 형상 불변" (카드 서술 L551) · 인용할 문장은 l 항목의 소성 문장 | §7.2 L551 | 카드 서술 | —

## l. 소성변형이 왜 어려운가 · 택한 우회와 그 값

입자 계산에 소성을 **넣은** 카드는 없다. 그래서 "왜 어려운가" 를 저자가 직접 설명한 문장은 이 배치에 없고, 있는 것은 (1) 소성을 빼고 계산한 결과가 관측과 어긋난다고 저자가 적은 문장 (cronk2026), (2) 역학을 건너뛴 우회 (bielefeld · chen), (3) 성형성이 수송을 만든다는 실험 문장 (asano2017) 이다.

- [l] cronk2026_lis_positive_electrode_geometry_fem (A. Cronk 외 18 인 · 교신 J. B. Lee · Y. S. Meng, Nat. Commun. 17:3298 (2026) · DOI 10.1038/s41467-026-69750-0) | **관측은 소성인데 모델은 탄성** — 본문: *"the resulting stress on the SSE matrix causes it to **plastically deform** to accommodate particle expansion"* (p9–10) · *"The plastic deformation of the SSE matrix is not surprising, as the simulated stresses estimated above is **near the shear modulus of LPSCl**"* (p10). 모델 (Table S7 전수): 선형탄성 S = C : ε_el · ε_inel = ε_HS = β_H·M_m·C_Li (등방 eigenstrain) · 소변형 · 바깥 경계 u = 0 · 기공 0 · 항복 · 경화 · 접촉 · 파괴 없음 | §4.1–4.4 L207–256 · §5.1 L334–335 · SI Table S6 · S7 | stated (인용문 · 표) | 소성을 왜 뺐는지에 대한 저자 설명은 카드에 없음 · Li–S · 리튬화 팽창 (가압 아님)
- [l] cronk2026_lis_positive_electrode_geometry_fem (같은 서지) | 택한 우회와 그 값: 우회 = 등방 eigenstrain (COMSOL "Hygroscopic Swelling" 노드) · 맞춘 값 = β_H 하나 / 케이스 (micron 22.5 × 10⁻³ · sub-micron 24 × 10⁻³ m³/kg) — 2D 단일 입자 계산에서 목표 부피팽창 (71 % · 75 % · Fig S32) 이 나오게 역보정 · 검증 = 응력 실측 없음 (cryo-FIB 의 정성 관측뿐) · 결과 응력 = 평균 2.42 / 2.40 GPa · *"beyond 5 GPa"* — 카드: 소성 · 공극 · 거시 팽창 (실측 두께 26 → 32 µm · +23 %) 을 모두 막은 "세 겹으로 부풀려진 상한" · 계산 비용 (요소 수 · 시간) 은 카드에 없음 | §4.2 L222–223 · §4.4 L247–256 · §4.6 L271–282 · §9 L623 | stated (값) · "상한" 은 카드 판정 | 조건당 3 전극 · 산포 미보고 · 메시 크기 미기록
- [l] cronk2026_lis_positive_electrode_geometry_fem (같은 서지) | 탄성만으로는 크기 효과가 나오지 않는다는 해석적 근거 (카드 계산): 등방 eigenstrain 구형 개재물의 계면 von Mises = E·ε*/(1 − ν) 로 반경과 무관 (Eshelby) → 6.15 GPa (ΔV 71 %) · 6.44 GPa (75 %) — 보고된 "beyond 5 GPa" 와 꼬리 8 GPa 를 재현 · 평균 응력 차 0.8 % (2.42 ↔ 2.40) ↔ 부과 팽창 차 5 % → "진짜 크기효과를 얻으려면 길이척도를 넣어야 한다: 항복응력 … 파괴길이 … cohesive law" | §5.2 L337–366 · §10-1 L637–640 | derived(ours) | 논문 문장이 아니라 카드의 해석 계산 — 인용할 때 구분
- [l] bielefeld2019_microstructural_modeling_composite_cathode (A. Bielefeld, D. A. Weber, J. Janek, J. Phys. Chem. C 2019, 123, 1626–1634) | 소성을 넣지 않은 미세구조 모델의 우회: 압밀 역학 자체를 건너뜀 — porosity · 조성을 입력으로 두고 무작위 배치 · SE 의 변형성은 "겹침 허용 볼록 다면체" 로 대신 (근거 E ≈ 25 GPa + 연성) · 맞춘 값 0 개 · 검증 = Strauss 등 (ref 13) 실험과 정성 비교만 · 계산 비용은 카드에 없음 (80 × 80 × 140 µm³ · 0.2 µm/voxel · 전이영역은 분율당 10 실현) | §4 L70–80 · §5.0 L90 | stated (방법) · "CONTACT 소성도, SHAPE 소성도 없음" 은 카드 서술 | 왜 어려운지에 대한 저자 설명은 카드에 없음 (목표가 "압밀역학·실험 없이 … 편의적으로 많이 생성" 이라고만 · L90)
- [l] bielefeld2020_effective_ionic_conductivity_binder (A. Bielefeld, D. A. Weber, J. Janek, ACS Appl. Mater. Interfaces 2020, 12, 12821–12833) | 같은 우회를 그대로 씀 (*"We use the AM microstructures generated in our **previous work**"*) — 더한 것은 수송 풀이뿐 · 재료 입력 σ_bulk,SE 2.7 mS/cm · AM/SE 계면 저항 40 Ω·cm² (맞춘 값이 아니라 문헌 입력) · 검증 한 점 (0.68 ↔ 0.73 mS/cm · LCO + LGPS) | §2.1 L105–110 · §2.2 L128–130 · §3.1.1 L211 | stated | 역학 없음
- [l] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity (T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, M. Tatsumisago, J. Electrochem. Soc. 164 (14) A3960–A3963 (2017)) | 계산 없음 (실험). 소성 (성형성) 이 수송 경로를 만든다는 실험 쪽 문장: *"This is due to the high formability of the sulfide solid electrolytes.[13]"* (낮은 "tortuosity … 4 to 6" 의 이유로 · p.A3963) | §3-5 L115 | stated (인용문) | Li₃PS₄ 유리 · 그 "tortuosity" 는 식 없는 값 · 형태 증거 없음
- [l] beutl2024_round_robin_coin_cell_sulfide_assb (A. Beutl 외 6 인, Electrochem. Sci. Adv. 2024, 4, e2400004) | 계산 없음 (실험). 카드: 성형 = "재배열 · 응집체 해체 · 소성 변형이 섞인 실제 과정 — 이 논문은 기전을 나누지 않는다" | §4-4 L215 | 카드 서술 | 인용할 논문 문장 없음
- [l] chen2011 (D. Chen 외, J. Power Sources 196 (2011) 3178–3185) · cooper2017 (S. J. Cooper 외, Electrochim. Acta 251 (2017) 681–689) | 말 없음 — 역학 · 소성을 다루지 않음 (chen2011: 무작위 충전 가정 · porosity 입력 / cooper2017: 기하 복셀) | chen2011 §4 L81–84 · cooper2017 §4-8 L184–185 | 카드 서술 | —

## m. 받아들일 통찰 (무엇을 | 우리 쪽 어디에 | 근거 위치)

- [m] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 기공 · vol% 기준이 없는 실험과는 f = σ_eff/σ₀ 로만 견준다 — f 는 부피분율 없이 원문 값만으로 정해지는 유일한 무차원 양 (0.125 / 0.078 / 0.055) 이고, tortuosity factor 꼴 (φσ₀/σ_eff) 은 상한으로만 정해짐 | 단계 7 · 결과 전 대조 항목 (수송 대조 양을 f 로 미리 적기) · 흐름 밖: 접촉망 수송의 실험 대조 | §0 L36–37 · §τ L208 · L220–227
- [m] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 실험 대조점마다 적을 장부 네 칸: σ₀ 출처 (본문값 4 × 10⁻⁴ ↔ 그림값 ≈ 3.5 × 10⁻⁴ ↔ 다른 논문 3.1 × 10⁻⁴ — 같은 원자료의 tortuosity factor 가 × 1.3 움직임) · vol% 기준 (고체 / 전체 — 기준이 섞이면 두 실험의 f 비가 × 1.2–2.8 ↔ × 29) · 측정 경계형 (관통 / 차단) · "정의 재구성 (식 없음)" 표지 | 단계 7 · 결과 전 대조 항목 · 흐름 밖: 실험과의 대조 | §8-1 L283–286 · §8-2 L290–296
- [m] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 전자 전도 대조에는 AM 상태 (SOC) 를 붙인다 — 복합체 σ_e 가 SOC 0 → 50 % 에서 × 26 / 34 / 45 (조성마다 다름) 라 한 σ₀ 로 묶이지 않음 | 흐름 밖: 전자 수송 계산 (σ_AM 고정값은 한 상태의 대리값이라는 한정) · 충방전 계산 | §3-3 L92–100 · §8-2 ② L293–294
- [m] asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity | 함정: 전자 차단 DC 셀은 SE 층 저항을 빼서 σ_ion 을 얻는다 — 48 vol% 에서 뺀 몫이 전체의 13–14 % (Fig 2b 판독 · 파생) 이고 무엇을 어떻게 뺐는지가 미기재 → 실험 대조점을 고를 때 "SE 층 저항 차감 방법" 을 확인 항목으로 | 흐름 밖: 실험과의 대조 · 계면 저항 | §3-4 L107 · §4-1 L143 · §8-3 L299
- [m] beutl2024_round_robin_coin_cell_sulfide_assb | 두께 · 밀도를 견줄 때는 잰 상태 (다이 안 · 꺼낸 뒤 · 지그 안) 를 값 옆에 적고, 밀도 (g/cm³) 로 먼저 맞댄다 — 이 논문 펠릿 = 360 MPa · 꺼낸 뒤 · 1.49–1.60 g/cm³ (0.1 g · ⌀10 mm → 함축 두께 0.80–0.85 mm) | 단계 0 (연산자 · 상태 적기) · 단계 4 · 단계 6 · 결과 전 대조 항목 | §7-2 ⑤ L298–308 · §8-2 L321 · §10 L355
- [m] beutl2024_round_robin_coin_cell_sulfide_assb | 실험 σ 를 대조점으로 쓸 때의 관문: 전극 접촉 규약이 결과를 × 2.5–5.5 움직임 (SS · Al/C 0.3–0.4 → 함께 누른 Al/C 1.0–1.8 mS/cm) ↔ 기관 차는 × 1.33 → 낮은 압력 · 차단 전극 값은 재료 값의 근거에서 빼고, 대조 실험의 전극 접촉 · 측정 중 압력을 먼저 확인 | 단계 7 · 흐름 밖: 실험 σ 와의 대조 · 계면 (접촉) 저항 | §0 L23 · §3-4 L134 · §7-2 ③④ L287–292 · §8-3 L322
- [m] beutl2024_round_robin_coin_cell_sulfide_assb | 두 시료의 전도도 비를 쓰려면: 시료 ≥ 3 개씩 · 두 두께 (R_total = R_contact + l/(σA) 의 기울기로 접촉 몫 제거) · 같은 지그 · 측정 압력 기록 (이 논문은 두께 한 값이라 접촉을 등가회로 R_int 로만 다룸) | 흐름 밖: 전극 σ_e DC 분극 대조 · 실험과의 대조 설계 | §7-2 ④ L291–293 · §8-4 L323
- [m] beutl2024_round_robin_coin_cell_sulfide_assb | SE 입자 크기를 고를 때 1 차 입자와 다짐 단위를 구분해 적는다 — 공급사 "∼1 µm" 분말이 SEM 에서 수 – ≈ 20 µm 응집체 [판독] · 같은 이름 분말 x50 17 µm (다른 카드 인용) | 단계 4 (순수 SE 가루의 출발 상태 · 입자 크기 선택) · 후보 D0 | §3-1 L70–71 · §7-2 ⑤ L311 · §8-7 L326
- [m] bielefeld2019_microstructural_modeling_composite_cathode | 연결 문턱의 조작적 정의와 실현 수: 문턱 = 무작위 실현 10 개 중 과반이 양 경계를 잇는 분율 (= 평균 이용률 40 %) · 전이영역 (48–52 vol%) 은 분율당 10 실현 평균 — 같은 분율에서 이용률이 ≈ 30 % ↔ ≈ 70 % 로 갈림 | 단계 7 (연결 · 고립 관측량과 시드 수) · 흐름 밖: 접촉망 수송 (문턱 근방 침대는 한 시드로 판정하지 않기) | §4 L80–81 · §5.3 L106–108 · Fig 3 · 6
- [m] bielefeld2019_microstructural_modeling_composite_cathode | 함정: 얇은 구조에서는 집전체 쪽 첫 층 입자가 전체의 큰 몫이라 전자 연결이 좋아 보임 (문턱이 낮은 AM 분율로 이동) = 유한크기 인공물 · 이온 쪽은 두께 무관 (140 µm 구조를 20–120 µm 로 잘라 본 결과) | 단계 5 · 단계 7 (얇은 침대 · 작은 상자의 연결성 결과 읽기) · 흐름 밖: 접촉망 수송 | §5.5 L124 · Fig 10
- [m] bielefeld2019_microstructural_modeling_composite_cathode | 부피분율 두 장부를 기호로 가름: 위첨자 V = 총부피 기준 (기공 포함) · S = 고상 기준 · g_AM^V = (1 − g_SE^S)(1 − φ) (식 4) · 활성 계면의 기하 상한 A_spec,geo = g_AM^V·6/d (식 7) · 이용률 θ = V_cluster/V_phase (식 6) | 단계 0 · 단계 7 (조성 · 계면 면적 보고 — 기준을 값 옆에) | §3 L54–55 · §5.2 L100
- [m] bielefeld2019_microstructural_modeling_composite_cathode | 저자 권고: 실험 연구도 porosity 를 재고 보고해야 서로 견줄 수 있다 ("porosity 가 결정적") | 결과 전 대조 항목 (기공을 보고하지 않은 실험은 대조점에서 한 등급 낮춤) | §5.6 L129
- [m] bielefeld2020_effective_ionic_conductivity_binder | τ² 를 σ 에서 되짚는 식과 그 장부: τ² = (σ_bulk,SE/σ_eff,ion)·ε_SE · ε_SE = (1 − φ)·ν_SE (기공 포함 전체 부피 기준) — 견준 실험 (Kato 2018) 이 void 를 빼고 계산해 "ambiguous" 하다고 저자가 지적 · void 15 % 는 가정 | 단계 7 (τ 정의 · 실험 대조 때 분율 기준과 void 가정 표지) | §2.2 L131–136 · §3.1.1 L207–213 · §11 L519
- [m] bielefeld2020_effective_ionic_conductivity_binder | Bruggeman 을 예측식으로 쓰지 않는다: 표준 τ² = ε^(−1/2) 가 모델 τ² 를 최대 4 배 과소 · 맞춘 꼴 γ·ε^(−α) 는 α 1.21–2.02 · γ 0.32–0.67 로 표준값 (0.5 · 1) 에서 멀고 "추가 과학적 통찰을 주지 않는다" | 단계 7 · 흐름 밖: 접촉망 수송 (Bruggeman 은 기준선 비교용으로만) | §3.1 L217–227
- [m] bielefeld2020_effective_ionic_conductivity_binder | 바인더 · 첨가제의 부피 회계: 바인더 부피를 AM 부피에 묶은 비 V(B):V(AM) 로 두면 wt% 는 조성에 따라 변함 · 활성 계면 손실이 고-AM 에서 비선형 (0.05 → 17 % (저-AM) ↔ 43 % (고-AM) · 0.10 → 29 % ↔ 82 %) · 바인더 없는 τ² 4.2 → 6.4 / 10 (70:30) | 흐름 밖: 첨가제 (PTFE · 바인더) 의 이온 경로 차단 · 계면 저항 계산의 면 가림 | §2.5 L164–178 · §3.2 L258–280
- [m] bielefeld2020_effective_ionic_conductivity_binder | 검증 방식: 문헌 SEM 으로 입자 꼴 · 부피분율을 재구성한 구조에서 계산값을 실측 한 점과 견줌 (σ_eff 0.68 ↔ 0.73 mS/cm · τ² 2.29 ↔ 2.47) — 보고되지 않은 void 는 가정 (15 %) 이라고 밝힘 | 단계 7 · 결과 전 대조 항목 (대조 실험에 빠진 입력을 가정으로 채웠으면 그 사실을 표지) | §3.1.1 L207–215 · §4 L317–318
- [m] chen2011_percolation_micromodel_composite_electrode | 종 사이 배위수의 닫힌식 (무작위 충전 · 평균 배위수 6): Z_{k,ℓ} = 0.5(1 + r_k²/r_ℓ²)·Z̄·(ψ_ℓ/r_ℓ)/Σ(ψ_k/r_k) — 수치 무작위 충전 재구성 (Kenney) 과 맞음 (Fig 3) | 단계 7 · 결과 전 대조 항목 (계산으로 센 AM–SE · SE–SE 배위수를 견줄 예측 — 방향 · 범위) · 흐름 밖: 접촉망 수송 · 입도 설계 | §5.1 L109–113 · §5.4 L140
- [m] chen2011_percolation_micromodel_composite_electrode | 같은 상끼리의 접촉수로 연결을 미리 어림하는 식: P = [1 − ((3.764 − ΣZ_같은 상)/2)^2.5]^0.4 — 같은 상 접촉수가 1.764 아래면 P = 0 (식에서 · 내 산술) | 단계 7 (SE–SE 접촉수로 이온 경로 연결 여부를 미리 점검) · 흐름 밖: 접촉망 수송 | §3 L50 · §5.2 L120–122
- [m] chen2011_percolation_micromodel_composite_electrode | 함정: 연속 입경 분포를 몇 개 크기로 나누면 곡선에 크기별 문턱이 계단 (여러 전이) 으로 나타남 — 더 많은 크기로 나누면 사라지는 이산화 인공물 | 단계 5 · 단계 7 (크기 몇 종만 쓰는 침대의 조성 스윕 곡선에서 꺾임을 물리로 읽지 않기) · 흐름 밖: 입도 설계 | §5.4 L141
- [m] chen2011_percolation_micromodel_composite_electrode | 분포의 두 축을 따로 다룸: 분포 폭 σ′ ↑ → 두 상이 함께 이어진 경계 길이 (percolated TPB) 32–48 % ↓ 인데 이어지는 조성 범위는 넓어짐 ([0.30, 0.70] → [0.20, 0.80]) · 입경비 r̄_el/r̄_ed ↑ → 문턱 ↓ · 입자 간 이온 전도 ↑ | 흐름 밖: 입도 설계 (SE 분포 폭과 SE/AM 입경비를 한 변수로 뭉치지 않기) | §5.5 L145–151 · §5.7 L166–169 · A.4 L247–251
- [m] cooper2017_simulated_impedance_diffusion_porous_media | DC 관문: 수송 솔버에 주파수 (임피던스) 기능을 붙이면 개방 (관통) 계의 ω → 0 절편이 기존 정상상태 값 τ/ε = 1/f 을 되찾아야 한다 (정규화 Z̃ = Z·A·D/L · A = 전체 단면) | 단계 7 · 흐름 밖: 접촉망 · 복셀 수송에 임피던스를 붙일 때의 단위 시험 | §4-3 L144–149 · §8-1 L288 · §8-3 L326
- [m] cooper2017_simulated_impedance_diffusion_porous_media | 해석해 벤치마크 둘: 곧은 개방 기공 = tanh(s)/s (ω = ωc 에서 0.886 − 0.287i) · 곧은 폐쇄 기공 = coth(s)/s (저주파 실수부 → 1/3 · 고주파 45°) · s = √(iω/ωc) · ωc = D/L² | 흐름 밖: 임피던스 계산 (접촉망 · 충방전 EIS) 의 단위 시험 | §3-6 L112–117 · §4-5 L157
- [m] cooper2017_simulated_impedance_diffusion_porous_media | 함정 둘: (i) ε · τ 가 같아도 스펙트럼은 다르다 (2D 기하 7 개) → 두 이산화를 정상상태 tortuosity factor 하나로만 견주고 끝내지 않기 (ii) 다공도 구배 구조는 순수 확산만으로 두 호 · DRT 2 차 봉우리를 냄 (*"both from a purely diffusive process"*) → 실측 EIS 의 둘째 호를 계면 과정으로 단정하지 않기 | 단계 7 · 흐름 밖: 실측 EIS · DRT 와의 대조 · 계면 저항 해석 | §0 ③④ L31–32 · §6-bis L231–234 · §8-2 ④ L321
- [m] cooper2017_simulated_impedance_diffusion_porous_media | 관통형 값은 방향을 못 본다: 같은 구배 충전을 뒤집으면 개방 절편은 같고 (≈ 4.1–4.2) 차단형 저주파 실수부는 ≈ 0.74 ↔ 2.27 (× 3.1 · 판독) · 1D 균질화 환산은 단면이 변하면 3D 보다 −19 / −23 % 과소 | 단계 7 (두께 방향 구배가 있는 침대를 관통 tortuosity factor 로만 순위 매기지 않기) · 흐름 밖: 전송선 (TLM) 적합으로 이온 저항을 뽑는 실험과의 대조 | §3-3 L82–88 · §3-4 L99–100 · §8-2 L318–320 · §8-5 L333
- [m] cronk2026_lis_positive_electrode_geometry_fem | 해석해 벤치마크: 등방 eigenstrain ε* 를 가진 구형 개재물 (같은 물성의 무한 기지) 의 계면 von Mises = E·ε*/(1 − ν) · 반경과 무관 (Eshelby) — E 22 GPa · ν 0.3 · ΔV 71 % → 6.15 GPa | U3 옆의 탄성 한계 단위 시험 (팽창 개재물) · 단계 6 뒤의 사이클 부피 변화 계산 · 흐름 밖: 열화 (팽창 · 수축에 따른 접촉 손실) | §5.2 (iii) L349–359 · §11 U1 L675 · §13 L748–749
- [m] cronk2026_lis_positive_electrode_geometry_fem | 함정: 복셀 개수로 센 "활성 표면 (%)" = 껍질 분율 ≤ 3h/R 이라 격자를 조이면 0 으로 감 — 보고된 대비 1 : 3.36 : 14.1 ↔ 참 비표면적 대비 1 : 10.7 : 100 (≈ 7 배 압축) → 표면 · 피복은 차원이 있는 양 (µm⁻¹) 과 격자 간격을 함께 보고 | 단계 0 · 단계 7 (피복 · 계면 면적의 정의) | §3.3 L100–128 · §11 U8 L682
- [m] cronk2026_lis_positive_electrode_geometry_fem | 함정: 역학과 수송을 다른 기하에서 계산 (τ · 표면적은 기공 10 vol% 기하 · 응력은 "fully compact" 기하) — 한 그림 안에서 두 전극을 견준 셈이고, 넘길 때 기공을 어느 상이 흡수했는지 미기록 | 단계 5 → 단계 7 (누른 구조와 수송 계산의 기하가 같은 상태임을 결과와 함께 적기) | §4.4 L241–245 · §10-2 L641–642
- [m] cronk2026_lis_positive_electrode_geometry_fem | 상자 대표성 보고 항목과 스케일 불변 진단: 상자 변당 입자 지름 개수 (2.0–2.5 / 6.7 / 18.7) · 상자 안 입자 수 (≈ 8–10 / 200 / 3,300) · 반복 수와 산포를 함께 적는다 · 고정 부피분율에서 구형 장애물의 τ 는 스케일 불변이므로 입경만 바꿔 τ 가 달라지면 원인은 (상자 / 입경 비 · 격자 / 입경 비 · 분포 폭) 셋 가운데 하나 | 단계 5 · 단계 7 · U6 (작은 조밀 충전의 수렴 보고) · 흐름 밖: 입도 설계 결과 읽기 | §3.4 L134–147 · §3.5 L173–182 · §10-4 · 5 L646–649

## 카드 문제

(고치지 않고 적는다. 이 배치의 일곱 장에 "Minnmann 의 순수 SE 10 % @300 MPa" 를 실험 근거로 적은 서술은 **없다** — Minnmann 이 나오는 자리는 복합 양극 값이거나 무엇을 가리키는지 적히지 않은 "실험 앵커" 이고, 뒤쪽은 아래에 따로 적었다.)

**asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity**

1. 원문 내부 불일치를 카드가 §10 에 적어 둠 (원문 문제): Fig 2 조성이 본문 "45 vol. %" ↔ 캡션 48 · Fig 3 을 본문은 62 vol% 로 부르는데 캡션 · 삽입값은 48 vol% · Fig 3 x 축 표지 "Z''/Ω cm²" · 캡션 600 s ↔ 본문 300 s · 초록의 (a)(b) 순서 · 전위 환산에 붙은 [12] (L316–324).
2. "tortuosity 4 to 6" 을 σ₀ 4 × 10⁻⁴ · φ = 1 − x 로 다시 계산하면 62 vol% 가 6.9 로 범위를 넘음 (L15 · L121 · L313) — 원문 입력 [미확인] (카드가 스스로 표지).
3. 다른 카드의 서술이 이 원문과 어긋남 (카드 §10-2 가 지적 · 고치지 않음): minnmann2021 카드의 "49 vol% 최적 (p.7)" 은 이 원문에 없음 (조성은 48 · 55 · 62 뿐 · "optimum" 낱말 없음) · cronau2022 카드의 "입경 감소 성공" 은 이 원문 수치로 뒷받침되지 않음 (분쇄 뒤 입경 미보고) · hlushkou2018 카드의 "같은 실험 축 두 번째 점" 은 측정 축만 같음 (L338–342).
4. AC 법의 연결형 (T형 open–open) 대응은 Siroma 2015 표와의 "우리 판독" — 원문이 인용한 것은 Siroma 2016 (정본 카드 없음) (L151).
5. SE 층 차감 몫: R_tot "≈ 920–940 Ω" 에서 807 Ω 를 뺀 값을 "≈ 116–137 Ω" 로 적음 (L107) — 적힌 숫자 그대로 빼면 113–133 Ω (내 검산 · 반올림 차 · "13–14 %" 결론은 같음).
6. 우리 쪽 값: 연화 E_eff 1.35 GPa (L254) · 망 σ₀ 3.0 mS/cm "펠릿값 CL-91" (L218 · L241) · σ_AM 50 mS/cm "모델 기준값 CL-92" (L242) — 카드 안에서 서로 다른 값은 없음. our_dem_baseline.md 가 "값 자리표시 상태" 라 우리 수치는 메모 v2 유도값이라고 표지 (L235).
7. Minnmann: "Minnmann 2021 (기공 14 % 로 φ 보정)" (L196) 은 복합 양극 값으로 읽힘 · 순수 SE 서술 없음.

**beutl2024_round_robin_coin_cell_sulfide_assb**

1. 머리 결론 (L23) 의 "정본 litdb 에서 1.64 를 인쇄한 카드들 가운데 '결정학' 라벨과 인용 번호가 함께 붙은 첫 사례" ↔ §3-3 L116 의 ⛔ 정정 (같은 그룹 tron2023 이 먼저 같은 라벨에 다른 인용 (Doux 2020) 을 붙였다) — 정정이 머리 문단에는 반영되지 않음 (tron2023 은 정본 미등록이라 "정본 카드 가운데" 라는 한정으로는 맞을 수 있음).
2. 원문 안 불일치 15 건을 카드가 §10 에 적어 둠 (원문 문제): 밀도 범위 하한 1.50 ↔ 1.49 · 함께 누른 셀 σ 표 1.8 ↔ 본문 1 × 10⁻³ · 유지 3 min ↔ 2 min · Table 1 "−25 °C" · Table 5 단위 · vol% 이름 순서 · NMC 입경 10–15 µm ↔ SEM ≈ 1–4 µm [판독] · Fig 10a 가 Fig 9a 와 같은 자료로 보임 [판독] · 로딩 2.0 ↔ 1.52 mAh/cm² · R_int 안정 120 h ↔ 200 h · CE 99 % ↔ 95 % · 옴 법칙 σ 7.6 × 10⁻⁴ 재현 안 됨 (L334–349).
3. 함께 누른 셀 σ 의 범위 표기가 자리마다 다름: "1.0–1.8" (L8 · L23) ↔ "0.9–1.8" (L134 · L270 · L287 · L322) — 0.9 는 Fig 5b 절편 판독 (0.92–0.94) 에서 온 값.
4. 랩 표준과 다른 문헌 값 (기준은 그대로): 결정학 산술 1.859–1.860 g/cm³ · Ohno 2020 비중병 1.874 · Frankenberg 2025 "fine" 1.87 · Doux 2020 이론밀도 1.860 (L27 · L106–116). 카드에는 이 값들에 기댄 "[우리 판단 — 결정은 1저자]" 문장 (L307) 과 공극을 두 줄로 적자는 제안 (L320) 이 들어 있음 — 여기서는 옮기지 않음.
5. 우리 쪽 SE 밀도가 카드 안에 두 값: "세대 2 D10 = SE 1.64 (1저자 보고 표 · 랩 측정법 미기록) · 세대 1 덱 2.0" (L269) — 세대가 다르다는 설명이 붙어 있음.
6. 우리 쪽 표적 서술: "세대 2 순수 SE 보정 표적 (300 MPa + 이완 끝 ε_union 10–13 % · 1.64 기준)" (L31 · L297 "랩 표준 · 측정법 미확인") — 값은 랩 기준과 같음 · Minnmann 순수 SE 서술 없음.
7. [미확인] 으로 남은 것: 1.64 의 출처 ([37] · [10] 원문 미확보) · 기관당 n · 두께 측정 도구 · 면적 A 의 기준 (⌀10 펠릿인지 ⌀8 전극인지) · SI 전부 (Table S1 · Fig S5 · S6).
8. 영문 원제가 카드에 없음.

**bielefeld2019_microstructural_modeling_composite_cathode**

1. 우리 σ_grain 의 출처 서술이 같은 배치의 다른 카드와 다름: "Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) sub-µm GB 인자 + Trevisanello NCM(r) + Wang" (L249) ↔ asano2017 L218 · L241 · cooper2017 L273 "펠릿값, CL-91" · beutl2024 L270 "Cronau 2021 SI S2c 펠릿 평탄 하단 — CL-91". "+ Wang" 의 서지는 카드에 없음. (프로젝트 지침은 "단결정" 라벨과 그 Wang 인용을 철회한 것으로 적는다.)
2. "Bazzoun 2026" 을 "같은 Janek 그룹" 이 스스로 걸어온 궤적으로 적음 (L22 · L182 · L260 · L270 · L278) — 근거 (저자 · 소속) 가 카드에 없고, 프로젝트 지침의 Bazzoun 2026 소속 표기 (Mercedes-Benz + Stuttgart) 와 맞지 않아 보임 (확인 필요).
3. 문턱 p_c 의 vol% 기준이 카드에 없음: 식 8 · Fig 3–6 의 "vol% AM" 이 총부피 기준 (g^V) 인지 고상 기준 (g^S) 인지 — Fig 7 의 69–79 vol% 는 AM/SE 합이 100 이라 고상 기준으로 읽힘.
4. 식 8 계산값 p_c(15 µm) = 57.9 vol% 가 본문 전이영역 "52–57 vol%" (L47 · L108) 의 0.9 vol% 밖 (내 검산 · 카드가 말한 적합 산포 ± 1–2 vol% 안).
5. 우리 쪽 값이 카드 안에 둘: "우리 ~20 % = 강체 구 압밀 floor" (L147 · L197 · L287) ↔ "우리 15.6 % (DEM) · 16.7 % (MPM)" (L159 · L287) — 다른 양이라고 적혀 있으나 20 % 의 출처가 카드에 없음.
6. "Minnmann 실험 앵커" (L167) · "우리 소재계 절대값은 Minnmann/Bazzoun/Cronau 소유" (L286) — 어느 값인지 (복합 σ 인지 순수 SE 기공인지) 카드에 없음 · "순수 SE 10 % @300 MPa" 라는 명시 서술은 없음.
7. 데이터 CSV 줄 (L8) 이 같은 파일 이름을 두 번 적음 ("이 digest 전용 …" · "기존 … 도 같은 내용 (병존)").
8. 영문 원제가 카드에 없음.

**bielefeld2020_effective_ionic_conductivity_binder**

1. 바인더 wt% 가 카드 안에 두 값: V(NBR):V(AM) = 0.10 → "~2.5 → ~3.4 wt%" · 0.05 → "~1.2 → ~1.8 wt%" (L173–174 · L260–261) ↔ "70 vol% AM 에서 1.8 wt% (0.10) / 0.9 wt% (0.05) NBR" (L279–280 · L429) · "2 wt% 미만" (L175 · L263). 내 검산 (카드 숫자만 · ρ_NBR 1.0 · ρ_NCM811 4.76): NBR 의 상한은 0.10 × 1.0 ÷ (4.76 + 0.10) = 2.06 wt% (SE 질량 0 인 극한) → 2.5–3.4 wt% 는 NBR 로 나올 수 없음 (PVDF 1.78 이면 상한 3.6 wt% 라 맞음).
2. Table 1 high-power 열의 τ² = 1.7 (L97 · L298): 식 14 에 카드 값 (σ 3.2 mS/cm · 60:40 · φ 15 % · ΔU 0.1 V · l 100 µm) 을 넣으면 j = 6.4 mA/cm² 이고 표의 7.25 는 τ² = 1.5 일 때 나옴 (내 검산 · 다른 두 열은 τ² 10 · 4 로 0.18 · 1.46 이 재현됨). 또 Fig 1b 는 50:50 에서 τ² ≈ 2 (L82 · L201) 인데 AM 이 더 많은 60:40 이 1.7.
3. Fig 1 축 대응: "하축 40 → 67 vol% AM, 상축 AM:SE 50:50 → 70:30" (L195 · L200) — porosity 15 % 이면 70:30 은 59.5 vol% 이고 67 vol% 는 ≈ 79:21 (내 검산). 같은 맥락에서 "67 vol% 에서 15 µm 은 ~3.5" (L202) ↔ Fig 2 적합식 0.668·ε_SE^(−1.213) 은 ε_SE 0.18 에서 5.3 (3.5 는 70:30 · ε_SE 0.255 의 값과 맞음 — 내 검산).
4. "vanishing 입경 극한 τ²_mono = 6.40" (L234 · L237): 식 τ² = 6.40·(d/µm)^(−0.246) 에서 6.40 은 d = 1 µm 의 값이고 d → 0 이면 발산 — 표현이 식과 안 맞음 (원문 표현인지 카드에 없음).
5. Kato 대조의 방향 서술: "ε_SE 를 void 빼고 잡으면 τ² 약간 낮아짐" (L213) ↔ 식 11 (τ² ∝ ε_SE) 로는 void 를 뺀 고상 기준 (0.571) 이 더 큰 τ² 를 줌 (3.2 ÷ 0.73 × 0.571 = 2.50 ≈ 보고 2.47 · void 포함 0.485 면 2.13 — 내 검산 · σ_bulk 는 LGPS 3.2 mS/cm (L32) 를 썼다고 가정).
6. trimodal "1:1:2" 를 한 곳은 "입경비" (L69), 다른 곳은 "개수비" (L235) 로 적음.
7. AM 이온 σ 의 출처 재료: "NMC523값" (L28) ↔ "NMC532" (L159 · L313). SE 표기도 LPSCl (L30) ↔ "NCM811:LPS:NBR" (L279) · "LPS 의 낮은 Young's modulus" (L107).
8. 식 16–17 전사: 분모 첫 항이 "ε_AM" (L184) — 내 검산으로는 비용량 (196 mAh/g) × 4.76 × ν_AM × (1 − φ) × l 이 표의 C-rate (0.19 · 1.5 · 0.010) 를 재현.
9. 머리 메타: type "FEM·digital-twin" (L3) ↔ 본문은 복셀 면 조화평균의 flux 풀이 (EJ-HEAT) · "methods: dft, elastic" (L12) 는 내용과 무관.
10. 이름 규약: 논문 τ² (식 11) 를 "우리 τ_Laplace,eff 정의와 同형" 이라 적음 (L135–136 · L505) ↔ 같은 배치 asano2017 · cooper2017 카드 (10-03 규약) 는 φσ₀/σ_eff 를 tau2, √ 값을 tau 로 구분.
11. "우리 MPM 은 transport σ 를 못 준다" (L154–155 · L385) ↔ 같은 배치 asano2017 L239 · cooper2017 L241 은 "MPM STEP3 복셀 σ" 를 우리 쪽 계산으로 적음.
12. "Bazzoun 2026 (… 같은 Janek 그룹)" (L59–60 · L380 · L392–405) — bielefeld2019 문제 2 와 같음 (L407 은 Hong 2026 만 "같은 그룹 아님" 이라 적음).
13. 우리 쪽 값: "σ_grain 3.0, E_eff 1.35/real 24" (L357) ↔ 같은 배치 cronk2026 카드는 LPSCl E 를 22 (문헌) · 우리 DFT 22.06 으로 적음 (카드 사이 차). "우리 15.6 % · ~10 % = 측정 결과" (L376) 의 ~10 % 가 무엇인지와 "측정" 의 뜻이 카드에 없음. "Minnmann/Bazzoun 앵커" (L358) 도 어느 값인지 없음.

**chen2011_percolation_micromodel_composite_electrode**

1. 문턱 접촉수가 두 값: 1.764 (L50 · L95 — 식 7 에서 P = 0 이 되는 값 = 3.764 − 2 · 내 검산) ↔ "~1.882 접촉 × 2 = 3.764" (L51 · L122). L122 는 ΣZ 를 "분모" 라 적으나 식에서는 분자.
2. 최대 TPB 위치의 이동 방향이 반대로 두 번: "ψ_ed 낮은값 → 높은값" (L55) ↔ "높은 → 낮은 값" (L150 — 범위 0.46–0.82 → 0.10–0.37 과 맞는 쪽).
3. 범위 0.46–0.82 의 조건: L54 는 "σ′ = 0.4 … r̄_el/r̄_ed = 0.5 예" ↔ L150 은 σ′ = 0 · r̄_el/r̄_ed = 0.5 의 값 (σ′ = 0.4 면 0.32–0.89).
4. 예시 값 1.3 S/m 의 이름: L65 "ion σ^ter,eff_el = 1.3" ↔ L161 · L168 은 σ^tra,eff_el (입자 내부) = 1.3 · σ^ter,eff_el (입자 간) = 0.87.
5. "이온전도 회복" 이라 쓰고 기호는 σ̃^tra,eff_ed (전자상) 0.59 → 0.72 (L58 · L159 · L189) — 문장과 첨자가 안 맞음.
6. 식 전사의 차원: 식 10 · 19 의 (a·n^V·Z·P)/δ 는 1/길이² 이라 σ 비가 무차원이 되지 않음 (L87 · L126) · 식 8 의 n^S 는 r² 이 분자에 있어 1/면적이 아님 (L123) · 식 15 의 부피분율이 r² 가중 (L136 — 카드도 "부피 ~ r³ 이나 여기선 r²" 라 적음) — 원문 대조 표지 없음.
7. Kenney ref[20] 을 "Bielefeld 의 ref[20] · Bielefeld 의 검증 출처" 라 적음 (L8 · L22) ↔ ref[20] 은 Chen 2011 의 번호 (L61 · L95 · L105) 이고, 같은 배치 bielefeld2019 카드의 비교 대상은 Strauss (ref 13) 뿐.
8. 우리 쪽: "Cronau 3.0 mS/cm × Cronau(r_SE) GB × Trevisanello NCM(r) = 실제 LPSCl/NMC811 재료 σ" (L319) — bielefeld2019 문제 1 과 같은 서술 차. "Bazzoun/Minnmann 실험 앵커" (L215) 는 어느 값인지 없음.
9. 영문 원제가 카드에 없음.

**cooper2017_simulated_impedance_diffusion_porous_media**

1. 원문 오식 · 내부 불일치를 카드가 표로 적어 둠 (원문 문제): p.685 차단 끝 극한 문장 (−1/√(2ω) 는 고주파 45° 점근) · 확산도 단위 "m s⁻²" · ω 를 "Hz" 로 표기 · 그림 1 의 둘째 정규화 Ẑ 정의 없음 · 그림 6 정규화 미기재 (L361–370).
2. 다른 카드와의 어긋남 (카드가 지적 · 고치지 않음): nguyen2020 카드의 "부록에 eSCM 과의 수학 대응 (p10)" — Cooper 원문에 "eSCM" 낱말 0 회 · 대응은 일정 단면에서만 같음 · kim2025 의 figures.json 연결은 검색 오탐으로 보임 (L372–378).
3. [미확인] 으로 남은 것: 공개 코드의 판 · URL · TauFactor 모드 4 내부 · 개방 7 기하 · 구 충전 · 분리막의 격자 크기 · 이완 계수 · 계산 시간 · 격자 수렴 자료 (L53 · L76–80 · L153–154).
4. 영문 원제가 서지 칸에 없고 PDF 파일명으로만 있음 (L11).
5. 카드 안 수치끼리의 모순은 찾지 못함 (검산한 것: 1.57 ÷ 0.5 = 3.14 · 14.0 ÷ 17.3 = 0.809 · 1.7 ÷ 2.2 = 0.773 · 2.27 ÷ 0.74 = 3.07 · 5·3⁶ = 3645 — 카드와 같음).

**cronk2026_lis_positive_electrode_geometry_fem**

1. 인용 금지 값: L579 가 우리 쪽 복셀 계산의 격자 세 점 (vox 0.15 / 0.125 / 0.115) 의 비를 숫자로 적어 둠 — 프로젝트 지침은 그 세 값을 인용 금지 (원장 hold) 로 둔다. 값은 여기 옮기지 않음.
2. 적층압 변동이 세 가지로 적힘: "1 MPa 미만" (L42 · 한 줄 요약) ↔ 판독 |Δ| ≈ 1.6 MPa (L491 · L604 · L679) ↔ "ΔP/P < 1.5 %" (L495 — 1.6 ÷ 75.5 = 2.1 % · 내 검산). 본문 "five times" (L492) 도 판독값 4.7 ÷ 1.6 = 2.9 배와 맞지 않음 (판독은 TREND only 표지).
3. 부피 상쇄 비교의 단위: S 양극 "4.9 µm mAh⁻¹" (6 µm ÷ 1.22 mAh · L471) ↔ Li "4.85 µm mAh⁻¹ cm²" (면적용량당 · L473) — 셀 면적 0.785 cm² (L58) 을 넣으면 6 ÷ (1.22 ÷ 0.785) = 3.9 µm/(mAh/cm²) (내 검산) · 1.22 가 면적당 값인지 카드에 없음 → "1 % 이내 일치" (L474 · L678) 는 단위 확인 필요.
4. 우리 쪽 LPSCl 영률이 카드 안에 둘: DFT E_VRH 22.06 · "3 자 합의 22 / 22.1 / 22.06" (L8 · L302–305 · L540 · L676) ↔ G_c 환산은 "E 24" (L369). 우리 E_CAM 도 "161.5 / 175" 두 값으로만 적힘 (L570 — 어느 것이 무엇인지 없음).
5. 생성기 원논문의 1 µm/pixel 을 Cronk 2026 의 voxel 크기처럼 적음 ("Cronk 의 sub-micron S 입자는 1–2 복셀로 그려진다" L702 · "확정한다" L77) ↔ Cronk 원문에는 voxel 크기가 0 건 (L87–91) · 같은 카드의 다른 추정은 R/h ≤ 3.4 (L110).
6. 카드 머리 (L10) 가 "계면상 화학은 다른 카드가 정본 · 어긋나면 그쪽이 이긴다 (예: 탄소 없는 milled S/LPSCl 의 Raman 152 cm⁻¹ 은 이동이 없다)" 라 적는데 §6.1 L390 은 "152 cm⁻¹ 적색이동" 그대로.
7. 원문 · 자료의 불일치 (카드가 적어 둠): Methods 의 표 번호 S3/S4 ↔ 실제 S6/S7 · Source Data 의 Fig 5b/5c 계열 이름이 전부 "Sub-Micron S" · Fig S32 Bulk ΔV 63 (그림) ↔ 93 (XLSX) · Fig 5g 박스 25 / 10 µm ↔ 생성 상자 50 / 15 µm · S 양 30–60 % 의 단위 (wt ↔ vol 혼합) · ν 0.3 ↔ 인용한 Deng 2016 의 0.37 (L81 · L97 · L197 · L209 · L308 · L484–486).
8. ρ_SE 1.6 g/cm³ (FEM 입력 · Table S6 · S8) = 랩 표준과 다른 문헌 값 · 카드는 "1.64 (Bazzoun) ≈ 일치" 라 적음 (L541).
9. Table S4 pristine 행: 1.2 mg ÷ 5.61 mg = 21 % 인데 "20 % 반응" (L444 · 내 검산 · 원문 표 값일 수 있음).
10. 영문 원제가 카드에 없음.
