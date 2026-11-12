# batch_29 정독 근거 (카드 9 장 · 전문 읽음 · 2026-11-11)

읽은 카드: `kim2025_impedance_decoupling_tlm_assb` (601 줄 · 3 번에 나눠) · `lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging` (177 · 1 번) · `li2026_electrochemomechanical_coupling_asslmb_review` (170 · 1 번) · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` (498 · 3 번) · `siroma2015_transmission_line_model_porous_electrode_impedance` (552 · 3 번) · `so2021_dem_fabrication_degradation_ductile_particles` (392 · 3 번) · `spencerjolly2023_ag_graphite_interlayer_operando_xrd` (242 · 1 번) · `tabakovic2026_mechanical_stress_eis_ica_drt_dfn` (246 · 1 번) · `tron2023_lpscl_ccd_ambient_pressure` (335 · 3 번). 끝까지 못 읽은 카드 없음 (모두 마지막 줄까지 읽음 · 가장 긴 줄 1,066 자라 잘린 줄 없음).

배치의 성격: **DEM 을 쓴 카드는 so2021 하나** (2D 소성 접촉 DEM · LPS 유리 SE + Si 음극 · 냉간 제조 → 사이클). 나머지: 임피던스 이론 · 실험 3 편 (kim2025 = 우리 랩 NCM811/LPSCl EIS-TLM · siroma2015 = TLM 해석해 전집 · tabakovic2026 = 액체 LIB DFN + 응력 모의 · 프리프린트), AM 미세역학 실험 1 편 (sedlatschek2026 = NMC811 입계 강도 · 나노압입 E), 액체 LIB 실험 + 3D 선형탄성 연속체 1 편 (lee2026), 리뷰 1 편 (li2026), Li 금속 계면 실험 2 편 (spencerjolly2023 · tron2023). **MPM 을 쓴 카드는 없다.** 순수 SE 압력별 곡선은 so2021 하나 (LPS 유리 · 2D DEM + Sakuda 2013 실험점) · 순수 LPSCl 한 점은 tron2023 (NEI · 360 MPa) 과 li2026 (song2025 경유 · 360 MPa).

적는 법: 위치의 `L숫자` = 카드 줄 번호. 표지는 카드에 적힌 그대로 (`stated` · `digitized` · `figure-read ≈` · `[인쇄]` · `[판독]` · `[정본 카드]` · `[우리 대조]` · `[우리 산술]` · `derived(ours)` · `우리 유도` · `우리 재계산` — 마지막 다섯은 **카드 작성자**의 산술 · 대조 · 유도다 (내 계산 아님)) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "카드 판정" = 카드가 내린 판단. 큰따옴표 안 영어 = 카드가 옮겨 둔 원문. 카드가 "인용 금지" 표지를 단 값은 숫자를 옮기지 않았다 (tabakovic2026 L12 · L176 · L190 · tron2023 L84 · li2026 L139 · sedlatschek2026 §3.3 L113 "인용 금지 정밀도"). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 카드 값이 다르면 "랩 표준과 다른 문헌 값" 으로만 적었다.

---

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

- [a] so2021_dem_fabrication_degradation_ductile_particles | LPS 유리 (75Li₂S·25P₂S₅ · 아지로다이트 아님) SE-only 2D DEM 상대밀도 곡선: 초기 ≈0.30 → 0.62 (50 MPa) → 0.70 (74) → 0.74 (100) → 0.83 (200) → 0.90 (360) → 0.95 (500) · α = 0.65 · Sakuda 2013 실험점 (open circle) 과 200–500 MPa 에서 일치 · <200 MPa 에서 모델 > 실험 (과치밀) | §3.2 L77–78 · Fig 4a · §5.4 L194 | digitized (곡선) · stated (일치 · 과치밀 서술) | 재료 다름 · 2D (z 두께 = 평균 SE 지름 · 국소 부피 = 2D Voronoi L244) · 진밀도 값 · 질량 기준 여부 · 누른 채인지 뺀 뒤인지 카드에 없음 (제하 springback 은 Fig 3b 에 따로) · Sakuda 실험점의 측정 상태 카드에 없음
- [a] tron2023_lpscl_ccd_ambient_pressure | NEI "fine" Li₆PS₅Cl 순수 펠릿 한 점: ≈100 mg · ⌀10 mm 경화강 다이 · ≈50 MPa 수 초 → 360 MPa 2 분 → 1.55–1.60 g/cm³ · 두께 "around 0.80 mm" (p.4) · "0.85–0.80 mm" (p.6) · 공극은 저자가 계산하지 않음 | §0 ② L27 · §3-1 L54–58 · PDF p.3 · p.4 · p.6 | [인쇄] | 밀도 측정법 (질량/부피? 몇 개?) [미확인] L56 · 두께를 잰 상태 (다이 안 / 놓은 뒤 / 꺼낸 뒤) [미확인] L27 · L58 · 온도 미기재 · 분말 입경 [미확인] · 다압력 없음 L254 · SI 미입수
- [a] tron2023_lpscl_ccd_ambient_pressure | 공극 (카드 산술): 1.64 (랩 표준) 기준 2.4 % (ρ 1.600) · 5.5 % (1.550) · 두께 역산 3.0–8.7 % — **360 MPa 값이라 랩 표준 (300 MPa · 10–13 %) 과 다른 문헌 값** · 1.86 (랩 표준과 다른 문헌 진밀도) 기준 14.0–16.7 % · 두께 역산 14.4–19.5 % · 두 기준 차 11.2–11.5 %p | §3-3 L87–98 | [우리 산술] | 식 ε = 1 − ρ/ρ_s = 질량 보존 연산자 (L87 · L243) · 질량 ±5 mg 감도 (L95)
- [a] tron2023_lpscl_ccd_ambient_pressure | 진밀도: 논문 p.3 의 "결정학 밀도" 문장 (ref 22 = Doux 2020 하나에 기댐 · 측정도 계산도 아님) 은 카드 L84 에서 **진밀도 근거로 인용 금지 표지** (값은 랩 표준 진밀도와 같은 수 · 숫자 옮기지 않음). 카드가 적은 다른 값 = **랩 표준과 다른 문헌 값**: 인용 문헌 Doux 2020 의 이론밀도 1.860 · 결정학 계산 1.860 (a 9.8591 Å, Z 4) · 피크노미터 1.874 (Ohno 랩 D) · 같은 상품명 NEI "fine" 진밀도 인쇄값 1.87 (Frankenberg 2025) | §0 ① L26 · §3-2 L64–84 | [정본 카드] · [우리 산술] · [인쇄] | Doux 원문 PDF 는 카드 작업에서 미대조 (L32 ②) · 로트가 다를 수 있음 (L79) · 1.64 의 출처는 [미확인] (L82)
- [a] tron2023_lpscl_ccd_ambient_pressure | 같은 압력대 다른 순수 LPSCl 펠릿 (정본 카드 경유): Doux 2020 (같은 NEI 분말 · 200 mg · ⌀13 mm · 370 MPa) 1.492–1.579 g/cm³ (이론 1.860 기준 상대밀도 80.3–84.9 %) · Ohno 랩 B (다른 분말 · 375 MPa · ⌀10 · 100 mg · 0.795 mm) 1.60 g/cm³ · Ohno 랩 C 1.77 (370 MPa) · G 1.70 (441 MPa) · D 1.655 (720 MPa) | §3-2 L67 · L80 · §3-3 L101 | [정본 카드] | 이 카드에서 원문 미대조 · 측정 상태 카드에 없음 · 다른 분말
- [a] li2026_electrochemomechanical_coupling_asslmb_review | 순수 LPSCl 펠릿 한 점 (리뷰 표 3 의 LPSCl 행이 song2025 값과 같다는 카드 대조): 기공 13 % · 360 MPa 냉간 · ⌀≈1 µm 입자 · mm 시편 | §3-2 L61 | [우리 대조] | 리뷰는 다공 · 측정 부류를 표시하지 않음 · 진밀도 기준 · 누른 채 / 뺀 뒤 카드에 없음 · 2 차 인용
- 나머지 여섯 카드 (kim2025 · lee2026 · sedlatschek2026 · siroma2015 · spencerjolly2023 · tabakovic2026): 순수 SE 기공 없음 (예: kim2025 L88–92 "porosity · 상대밀도 n/a").

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] so2021_dem_fabrication_degradation_ductile_particles | 순수 SE (LPS 유리) 제조 뒤 제하: 높이가 가압 중 지수 감소 → 제하 때 springback 으로 **부분 회복 · 처음 높이로 안 돌아감 (영구 h_eq)** · "higher Pfab → lower final height" · 되돌아온 양의 수치는 카드에 없음 (y 축 ×10⁴ µm · 응집체 척도 모델) | §3.2 L79 · §5.4 L193 · Fig 3b | digitized · stated | 잰 방법 = DEM 전극 높이 시계열 (모델 출력) · 2D · LPS 유리 · 복합 (Si + SE) 은 Fig 5a "지수감소 → unload → 안정" 서술만 (L197)
- [b] so2021_dem_fabrication_degradation_ductile_particles | 접촉 하나의 되돌아옴 (모델): 임계 초과 뒤 제하 곡선이 오른쪽으로 평행 이동 (h_eq > 0 영구) · F_max 50 / 100 / 200 µN · σ_H 1.0 / 1.5 / 2.0 GPa 별 이력 — σ_H 가 소성 전이점 · 최종 h_eq 를 정함 | §4.2 L144 · Fig 2c–d | stated (모식) | 수치 없음 · 가공경화 무시
- [b] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | NMC811 2 차입자 단면 flat-punch (Ø5 µm · 최대변위 5 µm · 15 s): 제하 곡선이 0 에 닿는 잔류변위가 있음 (Fig 4b · 값은 카드 §3.3 L113 "인용 금지 정밀도" 표지라 생략) · 저자: "no quantitative results could be derived" (불규칙 단면 · 바인더 주변 · 내부 결함) | §3.2 L96 · §3.3 L113–117 | stated (조건) · figure-read ≈ (곡선) | **SE 아님** · 입계 파괴 · 바인더 박리를 겪은 뒤 · 정량 불가 (저자)
- [b] tron2023_lpscl_ccd_ambient_pressure | 되돌아옴 측정 없음 — 두께를 잰 상태 (다이 안 / 놓은 뒤 / 꺼낸 뒤) · 꺼낸 뒤 지름 [미확인] | §0 ② L27 · ⛔ 한정어 ③ L32 · L58 | [미확인] | —
- 나머지 여섯 카드: 없음.

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기와 견줄 환산

- [c] so2021_dem_fabrication_degradation_ductile_particles | LPS 유리 압입 경도 σ_H = 1.9 GPa (McGrogan [31] · 비슷한 Li₂S 함량) 를 **항복으로 그대로** 씀: 접촉 최대응력 σ_max = 3/2·F/A_con (eq 7 · 포물선 분포) · 항복 임계 F_th = 2/3·σ_H·A_con (eq 8) → 접촉 최대응력이 σ_H 에 닿으면 소성 · 카드 원문 요약 "σ_yield ≈ σ_H 근사; 문헌 항복강도 부족" — **H/3 같은 일축 환산은 없다** | Table I L57 · §4.2 L136–139 · §5.4 L194 | stated | 가공경화 무시 (실험 자료 부족 L144) · 일정 하중에서 접촉면적↑ → 응력이 H 아래로 내려갈 때까지 시간 경과 감소 ("creep-like", 완화시간 t_rel 임의 L135 · L144) · 재료 LPS 유리
- [c] so2021_dem_fabrication_degradation_ductile_particles | Li₂S 파괴강도 σ_c = 2γ/δ = 5.6 GPa (γ 2.8 J/m² · δ ≈1 nm) → σ_H/σ_c = 1.9/5.6 = 0.34 → "초기 파손은 소성이 지배 (취성 아님)" = ductile particle 모델의 근거 | Table I L69–72 · eq 10 · §4.5 L158 | stated | 문헌 값 [2, 24, 31] · 분리 (융착 끊김) 조건은 σ_H 기준
- [c] li2026_electrochemomechanical_coupling_asslmb_review | 리뷰 표 3 의 경도 H: LPSCl 0.9 GPa (이 행 전체가 song2025 13 % 다공 펠릿값 [우리 대조]) · 75Li₂S–25P₂S₅ 1.9 GPa (E 18 GPa) · Li₁₀GeP₂S₁₂ 0.5 · Li₃YCl₆ 1.7 · K_Ic LPSCl 0.17 · 75Li₂S–25P₂S₅ 0.23 MPa m^½ | §3-2 L54–61 · 리뷰 p.8 | [인쇄] | 2 차 인용 · 표 3 인용 번호 +7 어긋남 (L60) · H 의 정의 (압입 방식 · 하중) 카드에 없음 · 일축 환산 없음 · LPSCl E 는 카드 L139 인용하지 않음 표지
- [c] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | NMC811 (AM): 자체 H 없음 (L29 · L87) · 인용 H 7.8 / 8.9 / 8.6 GPa (NMC532 다결정 2 차입자 [27]–[29]) · 14.2 GPa (NMC811 펠릿 [23]) · 입계 강도 Weibull σ_ch 745 MPa (m 6.91 · n 3) · 파괴변형률 ≈0.4 % · 입자 단위 파쇄강도 인용 172.8–210.6 · 207 (NMC811) · 188 MPa (NMC111) · 환산: 논문이 Stallard 2022 [30] 를 들어 "H/3 로 인장강도 추정 불가" 논거를 전함 | §3.1 L75–77 · §3.4 L136–144 · L141 | stated · 2 차 인용 | **SE 아님** · 취성 (인장은 소성 선행 없음 L75) · K_IC 는 재지 않음 (Sharma 2023 [23] 차용 · 카드 L304: 이 카드를 K_IC 출처로 인용하지 말 것)
- [c] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging | NCM92 전극 나노압입 (5 mN): H_IT 0.086 (LPC) · 0.18 GPa (SSC) · E_IT 5.17 · 6.02 GPa | §3 L34 · Fig S9 | stated (그림 값) | 전극 / 다공 2 차입자 유효값 (카드: 모델 E 191 GPa 와 다른 양 L103) · 액체 LIB · 일축 환산 없음
- 나머지 넷 (kim2025 L117 "E_SE / σ_y / ν n/a" · siroma2015 · spencerjolly2023 · tron2023): 없음. tabakovic2026 는 영률 (NMC 199 · 흑연 15 GPa) 만 · 항복 없음.

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

- [d] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | 우리 AM 하중분담 모델 (am_load_balance_jam.py) 의 H_AM 기본 4.0 GPa ("NCM811 압입 경도 문헌대 ≈ 3~6") · 역산 3.83–3.85 ↔ 논문이 인용한 NMC 경도 7.8 / 8.9 / 8.6 / 14.2 GPa **네 값 모두 3–6 밖** (인용 최저 7.8 = 상한 6 의 1.30 배 · 역산 3.85 의 2.03 배) · 카드 풀이: H_AM 은 물리적으로 "AM 크라운이 버티는 접촉 평균압" 이고 다결정 2 차입자는 압입 경도보다 낮은 압력에서 입계로 부서질 수 있음 (Fig 4) · 그 모델 자신의 등록 규칙 *"역산값이 그 밴드 밖이면 모델이 틀린 것"* 이 걸림 | §7.1 L266 · §7.5 L306–322 · §8 ② L369–374 · D19 L493 | 카드 판정 · derived(ours) | 인용 경도 원문 미확인 · 두께 예측 수치에는 영향 작음 (VACUOUS 기록 L317) · 흔들리는 것은 "문헌대 안" 교차검증 문장
- [d] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | AM–SE 접촉 E* 는 E_SE,eff (1.35 GPa) 가 지배 — AM 영률을 (138, 0.32) 로 바꿔도 AM–SE E* 차 −0.03 % · AM–AM 만 −2.9 % (힘사슬 강성 · Auerbach P_c) | §7.1 L262–263 · §7.2 L278 · D12 L486 | derived(ours) | 우리 DEM 입력 기준 산술
- [d] so2021_dem_fabrication_degradation_ductile_particles | Si (E 70 GPa) + LPS (E 24 · H 1.9 GPa) 복합 음극 제조: "LPS 무름 → SE만 소성" · 단단한 입자의 하중 몫 값은 카드에 없음 | Table I L56–57 · §5.5 L197 | stated | 2D · Si 음극
- 나머지: 없음 (li2026 의 Park 2025 · Farzanian 은 사이클 응력 L65–66 이지 압축 하중 몫 아님).

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값 수

- [e] so2021_dem_fabrication_degradation_ductile_particles | 대안 (So 2022 MethodsX 접촉 모델 계열): 비선형 Hertz + 평형 겹침 h_eq (Maxwell 완화 속도 eq 6) + 경도 항복 캡 F_th = 2/3·σ_H·A_con (eq 8) + 융착 (소성 변형한 SE 접촉은 분리 때 인장) + 거칠기 α (A_con = π·h_ov·R_eff·α, eq 9) + 과압밀 게이트 (1 − φ_solid⁴) · 출발점 Tomas [22] · Luding [23] · Storåkers [20] (spring-back) 언급 · **Luding 선형 모델은 낮은 경도 / 탄성 (σ_H/E < 0.01) 에만 유효 → 고체전해질 부적합** | §4.1–4.3 L119–148 · L117 · L125 | stated | 깨지는 범위의 정량 (겹침 · 상대밀도 문턱) 은 카드에 없음 — 과압밀은 국소 고체분율 → 1 일 때로만 적힘 (L135 · L147)
- [e] so2021_dem_fabrication_degradation_ductile_particles | 맞춘 값 수: **α 하나** (0.50 / 0.65 / 0.80 / 1.00 가운데 0.65 · Sakuda 상대밀도 200–500 MPa 에 맞춤) · t_rel 은 임의 (정상상태용 작은 값 · 데이터에 안 맞춤) · σ_H · γ · δ · E 는 문헌 · ν 0.3 · μ 0.5 · e 0.5 는 "This study" · 카드 셈 "α · t_rel · φ_solid⁴ · 융착 인장 — 4 개 보정 / 물리 인자" | Table I L58–68 · §4.7 L172 · Fig 4a | stated | 깨지는 곳: <200 MPa 에서 실험보다 과치밀 (2D · 3D 응집체 미표현, L78 · L194) · α 는 "표면 거칠기 · 2 차 접촉의 1-파라미터 프록시" (L68)
- [e] so2021_dem_fabrication_degradation_ductile_particles | 자매 So 2022 MethodsX 는 같은 목적 (과압밀 방지) 을 h_ov^max = 0.6 R_eff 로 둔다 (여기선 φ_solid⁴ 게이트) | §4.3 L147 | 카드 풀이 | So 2022 원문은 이 카드에서 미확인
- 나머지: 없음 (li2026 리뷰의 모델은 연속체 · 해석 · 위상장 · FE+ML 뿐 L90–91).

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

이 배치에 없음 (MPM 을 쓴 카드 없음). 수치 검산 방법으로 쓸 만한 것은 siroma2015 의 이산 사다리 대조 하나 (m 절).

## g. 2D 결과를 3D 로 옮길 때의 경고 · 증거

- [g] so2021_dem_fabrication_degradation_ductile_particles | 저자 명시 한계 (Shortcomings): "we simulated only in two dimensions" · "2D cluster DEM may overestimate solid fraction at low Pfab" · <200 MPa 에서 Sakuda 실험보다 과치밀 = "3D aggregate 구조 (더 큰 voids) → 시뮬 (2D) 이 과치밀" · 자매 So 2021 JPS 는 3D | L24 · §4.6 L165 · §5.4 L194 · §5.10 L218 · §7.1 L273 · §10 L381 | stated (따옴표 = 카드가 옮긴 원문) | 2D 의 z 두께 = 평균 SE 지름 가정 (L135 · L244) · 같은 재료의 3D 대조 결과는 카드에 없음
- [g] siroma2015_transmission_line_model_porous_electrode_impedance | (1D → 3D · 2D 아님) "we implicitly assume that the sample is one-dimensional." (p.315) · 카드: 이 논문과 우리 사이에 걸리는 차이는 "1D 균질 연속 ↔ 3D 비균질 접촉망" 하나이고 그 차이가 τ_e ≠ 관통 τ 를 만드는 자리 · 실제 ASSB 에서 적합된 z_A 는 "겉보기" 값 | §4-1 L159 · §7 L366–367 · §10 L493 | stated (원문) · 카드 풀이 | 임피던스 회로 · 압밀과 무관
- 나머지: 없음 (lee2026 모델은 3D 만 · sedlatschek2026 FE 2.5D 는 시편 설계용).

## h. DEM 에서 FE · MPM 으로 넘긴 선례 · 넘긴 시점

이 배치에 없음. (so2021 은 DEM 안에서 냉간 제조 → 사이클 두 단계를 잇고 FE · MPM 으로 넘기지 않는다 L150–159 · 저자 미래 과제 = 다구 (multisphere) 비구형 · DEM + 반응 / 물질전달 결합 (위상장 반응) · 취성 재료 확장 L219.)

## i. 복합 양극 (AM + SE) 의 압력별 기공

- [i] so2021_dem_fabrication_degradation_ductile_particles | Si 음극 복합 (Si AM + LPS 유리 SE · φ_AM^rel 0.4) 2D DEM: SOC24 사이클 중 기공 Pfab 100 → 0.22 · 200 → 0.155 · 500 → 0.06 (Fig 8d) · Pfab 100 사이클 기공 SOC8 0.12↔0.145 · SOC16 0.155↔0.185 · SOC24 0.18↔0.21 (Fig 8c) · "higher Pfab → lower porosity" | §3.3 L86–87 · §5.7 L204 | digitized · stated (방향) | 제조 직후 기공 수치는 카드에 없음 (Fig 5 SE 부피분율 색 0.5–1.0 만) · 사이클 중 값 · 양극 아님 · Pfab 100 · SOC24 값이 두 그림에서 엇갈림 (카드 문제)
- [i] li2026_electrochemomechanical_coupling_asslmb_review | Jeong 2024 (AEM · XCT): 작은 LPSC 복합 양극 공극 ≈11 vol % ↔ 큰 LPSC 16 vol % · 임계압 ≈400 MPa 위에서는 두 전극 응답 비슷 (공극 붕괴) · 0.1C 유지율 94.26 vs 47.33 % | §3-3 L72 · 리뷰 p.36 | [인쇄] | 2 차 인용 · 원 논문 정본 카드 없음 (L135) · 성형압 · 측정 상태 · AM 종류 카드에 없음
- [i] li2026_electrochemomechanical_coupling_asslmb_review | Oh 2026: 큰 다결정 NCWA + 작은 단결정 NCM + LPSC 바이모달이 단봉 대비 공극 35–58 % 낮음 · 큰 PC : 작은 SC 7:3 최적 · 정본 oh2026 카드의 "2D 공극" 16.80 → 7.55 → 17.96 | §3-3 L74 | [인쇄 p.46] · [우리 대조] | 압력 카드에 없음 · "2D 공극" 의 정의 (단면?) 카드에 없음
- [i] li2026_electrochemomechanical_coupling_asslmb_review | Farzanian [50] (2D 연속체): 양극 > 50 vol % 면 전극 팽창 > 5 % · 공극 > 1 % | §3-3 L65 | [인쇄 p.8] | 사이클 부피변화 결과 · 압축 기공 아님 · 2D
- [i] kim2025_impedance_decoupling_tlm_assb | 기공 미측정 — 같은 분말 40 mg · ⌀10 mm · 250 MPa 대칭셀 두께만: LNO 코팅 62 / 72 / 82 wt% = 190 / 180 / 160 µm · 비코팅 210 / 230 / 210 · LZC 170 µm (카드: "CAM↑ → 두께↓ (densification, 같은 분말질량)") | §3 L113 · §4.5 L194 · L88–92 | stated (Table S3 · S5) | 카드가 기공을 계산하지 않음 · 두께 측정 상태 카드에 없음
- 나머지: 없음.

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압 계산과 닿는 것

- [j] so2021_dem_fabrication_degradation_ductile_particles | 저자 Shortcomings: 2D · 구형 가정 · α 무차원 · AM–SE 입자 ≤1600 (수 무관성 확인 필요) · 삽입 때 상단 면 스프링 (일부 압력이 실 배터리 범위 초과) · 균일 팽창 (반응 · 물질전달 미결합) · 사이클 열화는 실험 검증 없음 (제조만 Sakuda 대조) | §4.6 L165 · §5.10 L218 · §7.1 L274 · §10 L384 | stated | —
- [j] tron2023_lpscl_ccd_ambient_pressure | 펠릿 밀도 측정법 · 두께 측정 상태 · 꺼낸 뒤 지름 미기재 · 한 압력 (360 MPa) · 다압력 Heckel 없음 · 스택압 아래 펠릿 두께 변화 없음 · 반복 수 · 표준편차 없음 · SI 미입수 | ⛔ 한정어 L32 · §3-10 L179 · §7-2 L254 | [미확인] | —
- [j] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | 압축 시험은 정성 (저자 "no quantitative results could be derived") · 두 E 모두 치밀 · 무결함 영역값 — 내부 기공 · 제조 균열을 가진 2 차입자 통째의 유효 강성은 더 낮을 수 있고 재지 않음 · 상용 캘린더링 전극 입자는 처음부터 균열 (Fig 2a → "t = 0 에 AM 무손상" 가정은 낙관적) | §3.3 L116–117 · §7.2 L280–281 · §5 L216 | stated · 카드 풀이 | AM 입력 쪽 한정
- [j] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging | 모든 입자 선형탄성 · 소변형 · 소성 · 크리프 · 파괴 없음 (본문 2.4 명시) → 300 MPa 는 "탄성 상한" 성격 · 이상 층간 계면 (본문이 한계로 명시) | §4 L52 · L54 · §10 L102 | stated · 카드 풀이 | 액체 LIB · 사이클 응력 (압밀 아님)
- [j] tabakovic2026_mechanical_stress_eis_ica_drt_dfn | 압력 = 정수압 σ_h 하나 — 실제 셀의 일축 적층압 · 편차응력 · 분리막 압축 (기공 감소) 없음 · 접촉 저항 · 접촉 면적 모델에 없음 → "압력에 따른 옴 저항 평행 이동" 은 원리적으로 재현 불가 (저자 명시) | §4.5 L124 · §10 L200 | stated | 운전 적층압 (1–10 MPa) · 압밀 아님
- [j] kim2025_impedance_decoupling_tlm_assb | 압밀 · 기공 · 역학 미산출 (두께 L 만) · 압력 3 종 구분: 제조 / 압밀 250–433 MPa ≠ EIS 측정 (셀 조립 상태) ≠ 작동압 · R_ion 은 압밀된 구조를 잰 값 | §4.5 L196–198 · §12 L547–549 · L568–569 | 카드 풀이 | —
- [j] li2026_electrochemomechanical_coupling_asslmb_review | 표 3 의 LPSCl E 는 13 % 다공 펠릿 벌크값 → 입력으로 쓰지 않음 ("측정 부류가 다르다") · 리뷰 숫자는 전부 2 차 인용 | §0 L20 · §7 L122 · §10 L142–146 | 카드 판정 | —
- siroma2015 · spencerjolly2023: 가압 · 탈압과 닿는 한계 없음.

## k. DEM 의 한계 (인용 서지 병기)

DEM 을 쓴 카드는 so2021 하나 — 논문 자신의 한계 서술은 그 카드에서만 나온다. 나머지 여덟 편은 DEM 을 쓰지 않아 "말 없음" (아래 "카드 풀이" 는 카드 작성자가 우리 DEM 을 두고 적은 서술 · 논문 문장 아님 — 인용 근거로 쓰지 않는다).

- [k] so2021_dem_fabrication_degradation_ductile_particles (So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge 2021, J. Electrochem. Soc. 168, 030538) | **입자 형상 불변** — 구만 · 소성은 접촉 수준 (평형 겹침 h_eq = 접촉점 함몰 · 융착 대리) 이고 입자 형상 흐름 (빈 곳 채움) 이 아님 · 저자 미래 과제 원문: "natural step is to extend to non-spherical particles which can be simulated in DEM by the multisphere method." | §4.6 L162 · §5.10 L219 | 카드 풀이 + 원문 인용 | —
- [k] so2021_dem_fabrication_degradation_ductile_particles (So et al. 2021, J. Electrochem. Soc. 168, 030538) | **선형 접촉 모델의 범위** — Luding 선형 모델은 "낮은 경도 / 탄성 (σ_H/E < 0.01) 에만 유효 → 고체전해질엔 부적합" → 비선형 Hertz 유지 + 평형 겹침으로 영구변형 | §4.2 L125 | 카드 풀이 (논문 Methods 요약) | —
- [k] so2021_dem_fabrication_degradation_ductile_particles (So et al. 2021, J. Electrochem. Soc. 168, 030538) | **매끈한 구 접촉 면적** A_con = π·h_ov·R_eff 는 "완전 매끈 가정 — 실제 ASSB 입자표면은 거칠다" → 무차원 α (0.65, 실험 상대밀도에 맞춤) 를 곱함 · 카드: α = "표면 거칠기 · 2 차 접촉의 1-파라미터 프록시" (= 보정값이지 물성 아님) | §4.2 L140–142 · Table I L68 | 카드 풀이 | —
- [k] so2021_dem_fabrication_degradation_ductile_particles (So et al. 2021, J. Electrochem. Soc. 168, 030538) | **과압밀** — 원문: "In order to avoid over-compaction, we inserted a term that goes to zero when the estimated equilibrium solid volume fraction tends to unity." → 국소 고체분율 → 1 에서 소성 속도를 0 으로 (1 − φ_solid⁴) | §4.3 L147 · §4.2 L135 | 원문 인용 | 문턱 고체분율 수치는 없음 · 2D Voronoi 국소 부피
- [k] so2021_dem_fabrication_degradation_ductile_particles (So et al. 2021, J. Electrochem. Soc. 168, 030538) | **2D · 입자 수 · 실현 수** — "we simulated only in two dimensions" · "2D cluster DEM may overestimate solid fraction at low Pfab" (<200 MPa 과치밀) · AM–SE 입자 ≤1600 → 수 무관성 확인 필요 · 다중 실현 명시 없음 | L24 · §4.6 L165 · §4.7 L171 | 원문 인용 · stated | —
- [k] so2021_dem_fabrication_degradation_ductile_particles (So et al. 2021, J. Electrochem. Soc. 168, 030538) | **시간 척도 · 가공경화** — 카드 요약 (원문 낱말 섞임): "real time scale → unacceptably long → t_rel arbitrary & small for steady state." (실제 완화 시간 척도는 계산 불가 → 임의) · 가공경화는 실험 자료 부족으로 무시 | §4.2 L135 · L144 | 카드 요약 | —
- [k] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile (Sedlatschek, Gertlowski, Weber, Broeckmann 2026, J. Power Sources 681, 240276) | 말 없음 (DEM 안 씀). 카드 풀이: 우리 DEM 의 AM = 탄성 구 (140 GPa · ν 0.25) · 내부 grain / 입계 없음 · 파괴 = 접촉 δ · F 에 대한 사후 분류 (Auerbach) · 입자 형상 변화 · 파편 없음 · "우리 Auerbach 임계는 단일 입자 압축 시험과 대조된 적이 없다" | §4.8 L201–209 · §8 ⑤ L388 | 카드 풀이 | 논문 근거 아님
- [k] li2026_electrochemomechanical_coupling_asslmb_review (Q. Li, Y. Li, Z. Wang, K.-Y. Park, S. Fleischmann, H. Kato, E. J. Cheng 2026, Batteries 12, 392) | 말 없음 — 리뷰 본문에 DEM · 퍼콜레이션 0 회 (카드 본문 검색) · 다룬 모델은 연속체 · 해석 · 위상장 · FE+ML | §0 L16 · §4 L91 · §6 L115 | [우리 대조] | —
- [k] tron2023_lpscl_ccd_ambient_pressure (Tron, Orue, López-Aranguren, Beutl 2023, J. Electrochem. Soc. 170, 100525) | 말 없음 (DEM 안 씀). 카드 풀이: Li 금속 (항복 ≈0.8 MPa) 의 크리프 · 공극은 우리 DEM (강체 구) · MPM (SE J2) 어느 쪽에도 없는 물리 | §4-2 L191 | 카드 풀이 | —
- [k] kim2025_impedance_decoupling_tlm_assb (S. Kim, J. Kang, J. H. Park, J.-W. Lee 2025, Electrochim. Acta 542, 147413) | 말 없음 (DEM 안 씀 · 카드: "입자 형상 · PSD · rigid/plastic 개념이 없다") | §4.4 L186–190 | 카드 풀이 | —
- [k] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging (W. Lee, S. Kim, S.Y. Yang, D.K. Kim, M.-S. Park, J.-W. Lee 2026, Energy Storage Mater. 86, 104985) | 말 없음 (DEM 안 씀 · 3D 연속체) | — | — | —
- [k] siroma2015_transmission_line_model_porous_electrode_impedance (Z. Siroma, N. Fujiwara, S. Yamazaki, M. Asahi, T. Nagai, T. Ioroi 2015, Electrochim. Acta 160, 313–322) | 말 없음 (시뮬레이션 없음 · 회로 수학) | §4-7 L300 | stated | —
- [k] spencerjolly2023_ag_graphite_interlayer_operando_xrd (D. Spencer-Jolly, V. Agarwal, … P. G. Bruce 2023, Joule 7, 503–514) | 말 없음 (DEM/MPM/FEM/DFT 0 건) | §4.1 L116 | stated | —
- [k] tabakovic2026_mechanical_stress_eis_ica_drt_dfn (J. Tabaković, T. Katrašnik, K. Zelič, SSRN 프리프린트 abstract 6915446 · 동료심사 전) | 말 없음 (DEM 안 씀 · 입자 평균장 연속체) | §4.5 L124 | stated | —

## l. 소성변형이 왜 어려운가 (인용 서지 병기)

이유를 논문이 직접 말한 카드는 so2021 하나. 우회 (소성을 빼고 선형탄성) 만 적힌 카드가 둘 (lee2026 · tabakovic2026) · AM 의 제한된 소성 관찰이 하나 (sedlatschek2026).

- [l] so2021_dem_fabrication_degradation_ductile_particles (So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge 2021, J. Electrochem. Soc. 168, 030538) | **왜 어려운가 (논문)**: 원문 "Despite the importance of ductility, to our best knowledge currently no model can simulate its effect on cold press densification and intercalation damage." · 원문 "Implementation of plasticity in DEM is novel, not only for battery electrodes but in the general context of particle simulation." · 기존 선형 응집 모델 (Luding) 은 σ_H/E < 0.01 에만 유효 · 문헌 항복강도 부족 → σ_yield ≈ σ_H · 가공경화 실험 자료 부족 → 무시 · 실제 완화 시간 척도는 너무 길어 t_rel 임의 · 융착 (원문 "… we assumed sulfide SE particles that have undergone plastic deformation upon contact will exert tensile stresses during separation.") | §5.2 L187 · §5.10 L217 · §4.2 L125 · L135 · L138 · L144 · §4.3 L148 | 원문 인용 · stated | —
- [l] so2021_dem_fabrication_degradation_ductile_particles (So et al. 2021, J. Electrochem. Soc. 168, 030538) | **택한 우회와 값**: 입자 형상은 두고 접촉 수준 소성 (h_eq Maxwell 속도 · F_th = 2/3·σ_H·A_con · 융착 인장 · α · (1 − φ_solid⁴)) · **영률은 연화 없이 실제 E 24 GPa** · 맞춘 값 1 (α 0.65 · 4 후보 중) · 맞춘 대상 = Sakuda 2013 SE-only 상대밀도 (200–500 MPa 일치 · <200 MPa 과치밀) + Sakuda SEM 과 정성 대조 (Fig 4b–g) · 사이클 열화는 실험 검증 없음 · 비용 = 자체 MATLAB DEM 을 일반 PC 에서 · AM–SE 입자 ≤1600 · 2D · 단일 실현 (카드: 보임) · 5 사이클 | §4 L113–172 · Table I L55–68 · §5.4 L194 · §7.1 L262–264 · L274 · L116 · L165 · L171 · L159 | stated · digitized (상대밀도) | 소성 = 접촉 함몰 대리 · 형상 불변 (L162) · LPS 유리
- [l] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging (W. Lee, S. Kim, S.Y. Yang, D.K. Kim, M.-S. Park, J.-W. Lee 2026, Energy Storage Mater. 86, 104985) | 어려움 설명 없음 · 택한 것 = 모든 입자 선형탄성 · 소변형 · 소성 · 크리프 · 파괴 없음 (본문 2.4) · 화학변형 Ω 값 · 솔버 · 메시 · 입자 생성법 미기재 (카드: "재현 불가") | §4 L49–55 · §10 L101–102 | stated · 카드 판정 | 액체 LIB · 사이클 응력
- [l] tabakovic2026_mechanical_stress_eis_ica_drt_dfn (J. Tabaković, T. Katrašnik, K. Zelič, SSRN 프리프린트 abstract 6915446 · 동료심사 전) | 어려움 설명 없음 · 택한 것 = 동일 · 등방 · 선형탄성 구 · 소변형 (해석해 Zhang–Shyy–Sastry 2007) · 입자 간은 평균 응력 ⟨σ^i⟩ 로만 | §4.2 L109 · §4.5 L124 | stated | 액체 LIB
- [l] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile (Sedlatschek, Gertlowski, Weber, Broeckmann 2026, J. Power Sources 681, 240276) | AM 쪽 소성 관찰 (입자 계산 아님): 인장은 파단까지 선형 · 취성 · STEM 에서 게이지 안 전위밀도 약간 증가 = 1 차입자의 제한된 소성 (단결정 NMC 에서는 소성이 입내 균열의 개시 기구) · 시편 설계 FE 는 선형탄성 — 저자 한계: 소성하는 재료에서는 게이지 응력이 균일 · 단축에서 벗어날 수 있다 · 카드: "압밀 응력에서 AM 을 탄성으로 두는 우리 처리에는 영향 없음" | §4.6 L187–188 · §4.3 L176 · §5 Fig 7 L221 | stated · 카드 풀이 | AM (NMC) · 전·후 같은 위치 비교 불가 (저자 caution)
- 나머지 넷 (kim2025 · li2026 · siroma2015 · spencerjolly2023 · tron2023): 카드에 없음.

## m. 받아들일 통찰 (무엇 → 우리 쪽 어디 → 왜)

- [m] kim2025_impedance_decoupling_tlm_assb | R_ion 앵커는 R_ion 이 깨끗이 갈린 셀 (대칭셀 · 비코팅) 값만 쓴다 — R_int/R_i 가 3 · 1 이면 이온수송과 전하전달 영역이 갈리고 1/4 · 1/16 이면 겹침 · 원문 결론 = 풀셀 단독 분석은 오해를 부르니 대칭셀 보완 필수 → 자리: 흐름 밖: 접촉망 이온 수송 계산의 실험 앵커 선택 | §5.5 L269–278 · Fig 6e · Table S7 L402–403 | stated | 코팅 풀셀 R_ion 은 R_ct 와 섞임
- [m] kim2025_impedance_decoupling_tlm_assb | R (Ω·cm²) → σ 환산엔 조성마다 다른 펠릿 두께를 쓴다 — 같은 분말 40 mg · 250 MPa 에서 62 / 72 / 82 wt% = 190 / 180 / 160 µm (CAM↑ → 얇아짐) · "82 wt% 최저 R_ion" 은 이 두께 효과 몫을 포함 → 자리: 흐름 밖: 실험 R → σ 환산 (결과 전 대조 항목 입력 검사) | §3 L113 · §5.2 L228 · §4.5 L194 | stated | 카드가 σ 로 환산하지 않음
- [m] kim2025_impedance_decoupling_tlm_assb | 문헌 그림의 막대 숫자 ≠ 표 적합값 — 막대 라벨은 다른 정규화 · 다른 칸 (용량) 일 수 있으니 SI 표 원값만 반입 (이 카드 자신도 표 칸을 엇갈려 적음 — 카드 문제 1–3) → 자리: 결과 전 대조 항목 (문헌 값 반입 검사) | §6.3 L344–348 · §12 L563–564 | 카드 풀이 | —
- [m] kim2025_impedance_decoupling_tlm_assb | 냉간 압착 LPSCl 복합체의 SE 입계 저항이 bulk 와 같은 크기 이상이고 온도에 더 민감: 62 wt% 대칭셀 R_i,bulk 9.3 → 8.0 → 6.0 vs R_i,gb 25.6 → 12.4 → 3.1 Ω·cm² (30 → 45 → 60 °C) → 자리: 흐름 밖: SE–SE 계면 저항 (Rint ②) 의 결과 전 대조 항목 후보 | Table S3 L355–359 · §5.2 L223–225 | stated | 복합 양극 R 값 (순수 SE 아님) · 조성 · 두께 함께 적어야
- [m] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging | "조성이 아니라 배치" — 같은 SSC 함량의 단층 (5:5) 은 개선 없음 · SPC (소형 다결정) 상층은 개선 없고 SPC 가 균열 → 효과는 상층 배치 + 단결정성 → 자리: 흐름 밖: 층상 양극 설계 · 설계 → 구조 ML 입력에 z-배치 변수 | §3 L45 · §7 L81 · §8 ⑤ L92 | stated · digitized | 액체 LIB
- [m] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging | 전극 나노압입 E_IT 5–6 GPa · H_IT 0.09–0.18 GPa (5 mN) 는 전극 / 다공 2 차입자 유효값 — 재료 E (191 GPa) 와 다른 양이라 AM 입력 · 대조에 쓰지 않는다 → 자리: 단계 5 (AM 입력) · 결과 전 대조 항목 | §3 L34 · §7 L85 · §10 L103 | stated · 카드 판정 | —
- [m] lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging | 관측량: 균열 면적분율을 z 위치 (분리막 쪽 ↔ 집전체 쪽) 로 나눠 보고 (3.438 vs 1.174 %, FIB-SEM 그레이스케일 이진화) → 자리: 흐름 밖: 열화 (A10 f_broken · A_rel 의 z-빈 출력) | §3 L33 · §6 L69 · §8 ② L89 | stated | 액체계 값 (형태 대조만)
- [m] li2026_electrochemomechanical_coupling_asslmb_review | 물성 표 반입 함정 — 리뷰 표 3 은 LPSCl E 를 13 % 다공 펠릿값으로 (부류 표시 없이) 적고 다른 SE 의 치밀 · DFT 값과 한 표에 섞으며 인용 번호가 전부 +7 어긋남 · 같은 이름 "E_SE" 가 다공 펠릿 · 나노압입 (28 GPa) · DFT (22 GPa) 로 갈림 → 자리: 단계 4 · 5 입력 감사 · 결과 전 대조 항목 (측정 부류 · 원 논문 확인 뒤 반입) | §0 L20 · §3-2 L60–61 · §8 L133 · §10 L142–143 | [우리 대조] · 카드 판정 | —
- [m] li2026_electrochemomechanical_coupling_asslmb_review | Shi 2020: 50 사이클 뒤 300 MPa 재가압으로 ≈80 mAh/g 회복 = 접촉 손실의 가역 기계 몫을 잰 실험 → 자리: 단계 6 (탈압 · 재가압 팔) 의 결과 전 대조 항목 후보 | §3-3 L68 · §7 L125 · §8 L134 | [인쇄 p.23] | 2 차 인용 · Shi 정본 카드 없음 · 재료 카드에 없음 · 사이클 뒤 실험
- [m] li2026_electrochemomechanical_coupling_asslmb_review | Jeong 2024: SE 입경에 따른 복합 양극 공극 차 (≈11 vs 16 vol %) 가 ≈400 MPa 위에서 사라짐 (공극 붕괴) → 자리: 단계 5 결과 전 대조 항목 후보 (SE 입경 효과는 압력 창에 매임) | §3-3 L72 · §11 L153 | [인쇄 p.36] | 2 차 인용 · 정본 카드 없음 · 측정 상태 카드에 없음
- [m] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | AM 탄성 입력은 E/(1−ν²) 로 견준다 — 나노압입이 실제로 제약하는 양이 그것이고 Hertz 접촉 강성도 같은 조합이라 ν 가정과 무관: (138, 0.32) 153.7 ↔ (140, 0.25) 149.3 GPa = −2.9 % · AM–SE E* 는 E_SE,eff 가 지배해 −0.03 % → 자리: 후보 D0 · 단계 5 (AM 입력 대조) | §7.2 L275–278 · D11–D12 L485–486 | derived(ours) | AM_P (다결정) 한정 · AM_S 는 이 출처 밖 (L283–289) · "140 GPa (Sedlatschek 2026)" 로 쓰지 말 것 (L345)
- [m] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | 층을 섞지 말 것 — 138–165 GPa 는 입계를 포함한 집합체 값 · 입계를 해상하고 GB 스프링을 따로 넣는 모델의 grain 에 넣으면 GB 순응성 이중계상 (1D 직렬 예: E_grain 210–249 + S_gb·d 312 → 125–139 GPa) → 자리: 조건 R7 · 후보 B (입계 해상 AM) | §8 ④ L380–384 · D17 L491 | derived(ours) (예시용) | S_gb 는 빌린 K 에 매임
- [m] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | DEM 입자 파쇄를 강도로 넣는다면 입자 단위 강도 (인용 172.8–210.6 · 207 NMC811 · 188 NMC111 MPa) — 745 MPa 는 무결함 ≈1.8 µm³ 입계 강도라 상한 · Weibull 체적 스케일만으로 2.3–3.0 배 · 상용 전극 입자는 처음부터 균열 (Fig 2a) → 자리: 조건 R7 · 결과 전 대조 항목 (단일 입자 압축 [32] · [38] · [39] — 우리 Auerbach 임계는 아직 대조된 적 없음) | §7.6 L327–330 · §8 ⑤ L386–388 · D18 L492 · §5 L216 | 2 차 인용 · derived(ours) · 카드 풀이 | 원문 확인 전 · 액체계 전극 맥락
- [m] sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile | H_AM (하중분담 모델) 을 "문헌 압입 경도" 로 부르지 않는다 — 인용 NMC 경도 7.8–14.2 GPa 네 값이 우리 "문헌대 3–6" 밖이고 그 모델의 등록 규칙 ("역산값이 그 밴드 밖이면 모델이 틀린 것") 이 역산 3.83–3.85 를 기각하게 됨 → 런 전에 "입자 스케일 유효 지지압 (입계 파쇄 포함)" 으로 재정의하고 판정선을 다시 등록 → 자리: 흐름 밖: AM 하중분담 모델 (조건 R1) | §7.5 L306–322 · §8 ② L369–374 | 카드 판정 | 인용 경도 원문 미확인 · 두께 수치엔 영향 작음
- [m] siroma2015_transmission_line_model_porous_electrode_impedance | EIS 에서 온 τ 를 tau2 와 견줄 때 연결형을 같이 적는다 — T형 open–open (같은 레일 양 끝 · DC → L·z_A = 관통) 은 우리 두 띠 Dirichlet 접촉망과 같은 BC 부류 · Z/E형 (de Levie · 저주파 L·z_A/3) 은 τ_e 부류 (우리 없음) → 자리: 흐름 밖: 이온 수송 (tau2) 의 실험 대조 표기 | §0 L15–19 · §3-5 L130–135 · §8-5 L461–463 | 우리 유도 (카드) · stated | 극한은 원문 문장 아님
- [m] siroma2015_transmission_line_model_porous_electrode_impedance | "R_ion = 3·R_eff" 는 균일 r · 균일 c · z_C = 0 에서만 정확 — z_C ≠ 0 이면 (R_ion + R_el)/3 · 비균질이면 ∫ r (1 − C/C_tot)² dx · 2 층 (r 3 : 1) 예 ±37.5 % · 방향 의존 (0.917 ↔ 0.417) → 자리: 흐름 밖: de Levie 적합 EIS 앵커 환산 (층상 · 구배 전극 주의) | §8-4 L449 · L455–456 · §3-5 L135 · L518 | 우리 유도 · 우리 계산 (카드) | —
- [m] siroma2015_transmission_line_model_porous_electrode_impedance | TLM 레일은 bulk · 입계 · 접촉을 한 값에 뭉친다 → Minnmann 펠릿 정규화 (τ² ≡ 1) 는 펠릿 자신의 입계 · 접촉만큼만 지운다 · 우리 짝 = 모델 T 를 순수 SE 망 T_pure 로 나눔 (원 T · 정규화 T 둘 다 보고) → 자리: 흐름 밖: 이온 수송 기준 상태 (σ₀) | §8-2 L412–430 | 카드 풀이 | Minnmann 서술은 Minnmann 카드 기록 경유 (L494)
- [m] siroma2015_transmission_line_model_porous_electrode_impedance | 수송 솔버 단위 시험 — 해석해를 세밀 이산 사다리 (구간 800 · 1600 · 끝 반가중 분로 · Richardson) 와 대조해 상대오차 ≲4·10⁻¹⁰ · 극한 (T형 DC = L·z_A · Z형 LF = L·z_A/3 · 비균질식) 을 2 층 사다리 네 경우로 5 자리 확인 → 자리: 흐름 밖: 접촉망 · 복셀 수송 솔버의 해석해 시험 | 원문 대조 기록 L523–531 | 우리 재계산 (카드) | 1D 균질 회로
- [m] so2021_dem_fabrication_degradation_ductile_particles | 과압밀 게이트 — 소성 속도에 (1 − φ_solid⁴) 를 곱해 국소 고체분율 (2D Voronoi) → 1 에서 소성을 멈춤 → 자리: 후보 C′ (항복 캡 접촉 DEM 의 과압밀 방지) | §4.2 L131–135 · §4.3 L147 | stated · 원문 인용 | 2D · 자매 So 2022 는 h_ov^max = 0.6 R_eff
- [m] so2021_dem_fabrication_degradation_ductile_particles | 항복 캡으로 실제 E 유지 — F_th = 2/3·σ_H·A_con (σ_yield ≈ σ_H) 로 접촉력을 막으면 E 24 GPa 그대로 (연화 없이) α 하나 (0.65) 만 맞춰 Sakuda 상대밀도 200–500 MPa 를 재현 → 자리: 후보 C′ · 조건 R5 (맞추는 값 하나) | Table I L55 · L57 · L68 · §5.4 L194 · §7.1 L263–264 | stated · digitized | LPS 유리 · 2D · <200 MPa 과치밀
- [m] so2021_dem_fabrication_degradation_ductile_particles | 함정 — 2D DEM 은 저압 (<200 MPa) 에서 3D 실험보다 과치밀 (3D 응집체의 큰 공극 미표현) → 2D 결과는 고압 구간만 실험과 견주고 2D 고체분율을 3D 로 옮기지 않는다 → 자리: 단계 3 · 단계 4 | §3.2 L78 · §4.6 L165 · §5.4 L194 | stated | —
- [m] so2021_dem_fabrication_degradation_ductile_particles | 관측량 분해 — κ_SE^rel = φ_SE/τ_SE 로 φ 와 τ 를 따로 보고 · 사이클 손실은 φ 변화 <10 % · τ (균열) 지배 → 자리: 단계 7 · 흐름 밖: 열화 (σ 손실을 기공 몫 · 경로 몫으로 나눔) | §3.3 L90–92 · §5.8 L208–210 | stated · digitized | κ 는 상대값 (Holm 접촉저항 없음) · Si 음극
- [m] spencerjolly2023_ag_graphite_interlayer_operando_xrd | 점착 계산할 계면 상태 목록 — 충전 상태의 SE 쪽 면 = LiC₆ + Li-rich Li–Ag · CC 쪽 = Li₁₀Ag₃ + Li 금속 · 방전 말에야 흑연 + Ag → W_ad 는 pristine 과 리튬화 상태를 둘 다 → 자리: 흐름 밖: Ag–C 인터레이어 점착 DFT | §8 ① L182 | 카드 풀이 | 어느 합금 조성이 SE 와 닿는지는 직접 안 보임
- [m] spencerjolly2023_ag_graphite_interlayer_operando_xrd | 계면이 셋 — 저 · 중율에서 Li 가 인터레이어와 CC 사이에 쌓임 = CC/인터레이어 계면이 운전 중 벌어짐 → 박리 DEM 은 인터레이어/SE 와 인터레이어/CC 둘 다 잰다 → 자리: 흐름 밖: 점착 DEM | §7 L171 · §8 ② L185 | 카드 풀이 | 점착 미측정
- [m] spencerjolly2023_ag_graphite_interlayer_operando_xrd | 함정 — 저율 (상온) ↔ 고율 (60 °C) 이라 "속도 효과" 에 온도가 섞임 · CCD 동등 ("흑연 단독 = Ag–흑연") 은 2.0 ↔ 2.5 mA/cm² 해상도의 대표 곡선 하나 → 자리: 흐름 밖: 실험 대조 시 조건 교란 점검 | 경고 ③ L12 · §10 L206–207 | stated · 카드 풀이 | —
- [m] tabakovic2026_mechanical_stress_eis_ica_drt_dfn | 압력별 EIS · DRT 비교 규약 — SoC 고정인지 전압 고정인지 적는다 (같은 셀도 SoC 에 따라 압력 효과 부호가 바뀜 · 논문 자신이 본문 "고정 전압" ↔ 부록 "같은 SoC" 로 섞음) → 자리: 흐름 밖: 적층압별 EIS 비교 · 실험 EIS 대조 | §8 ② L178–179 · §10 L195 | 카드 판정 | —
- [m] tabakovic2026_mechanical_stress_eis_ica_drt_dfn | 문헌 그림의 크기를 그 논문 자신의 식 · 표로 다시 계산 — 이 논문은 그림의 이동이 Eq. 44 + Table 3 값의 정확히 10 배 (벡터 경로 판독 + 산술 · 두 전극 모두) → 자리: 결과 전 대조 항목 (문헌 값 반입 검사) | §10 L194 · §13-2 L238–241 | derived(ours) | 이동 크기 수치 (mV/MPa) 는 인용 금지 표지라 생략
- [m] tabakovic2026_mechanical_stress_eis_ica_drt_dfn | 적층압이 임피던스에 들어가는 두 통로 — 접촉을 뺀 열역학 통로 (Ω σ_h) 는 OCV 강체 이동 (mV 급) 이지 저항 스케일이 아님 → ASSB 적층압에서는 접촉 (Holm · 면적) 이 주역이라는 구도 유지 · 열역학 통로는 보정 항 후보 → 자리: 흐름 밖: 적층압 · 계면 저항 (Rint) | §8 ① L174–176 | 카드 풀이 | 숫자 인용 금지 (자릿수만) · LIB 매개변수 · 선형 외삽
- [m] tron2023_lpscl_ccd_ambient_pressure | 실험 펠릿 기공 = 질량 ÷ 기하 부피 ÷ ρ_s = ε_sphere (질량 보존) 쪽 연산자 — DEM 의 ε_union 표적과 같은 연산자가 아님 (순수 SE 침대는 겹침 때문에 ε_union > ε_sphere) · 표적 밴드와 함께 쓰는 밀도 기준 (랩 표준) 을 같은 문서에 봉인 (같은 펠릿이 밀도 기준에 따라 ≈11 %p 옮겨짐) → 자리: 단계 0 · 단계 4 | §3-3 L87 · L98 · §7-2 L243 · §8 ② L283 | [우리 산술] · 카드 판정 | 랩 표준은 고정 (기준을 바꾸자는 뜻 아님)
- [m] tron2023_lpscl_ccd_ambient_pressure | 펠릿 기록 칸 — 질량 0.1 mg · 두께 여러 점 · 꺼낸 뒤 지름 · 두께를 잰 상태 (다이 안 / 놓은 뒤 / 꺼낸 뒤) · 성형압 · 유지 시간 · 밀도 측정법 · 반복 수: 이 논문이 빠뜨린 칸이라 문헌 대조가 막힘 → 자리: 단계 4 · 단계 6 (탈압 뒤 상태) 의 결과 전 대조 항목 입력 규칙 | §8 ③ L284 · ⛔ 한정어 L32 · §3-10 L179 | 카드 판정 | —
- [m] tron2023_lpscl_ccd_ambient_pressure | DC 분극 측정 관행 — 같은 셀형 3 셀 총 저항 흩어짐 1.46 배 · 지그만 바꿔 2.4 배 (스택압 0.20–0.28 MPa 로 비슷한데) · 스프링 느슨 7.4 배 · 표면 피막 6.3 배 · 0.2 MPa 대 저항의 ≈85–90 % 가 계면 · 두께 시리즈 n = 1 은 벌크를 못 가름 · 고정 간극 CR2032 는 시료 두께 0.1 mm 가 힘을 36 % 바꿈 → 지그 · 하중 · 두께 2 점 이상 × n ≥ 3 을 기록 · 접촉 ASR 은 SBE/DBE 비를 1 쪽으로 누름 → 자리: 흐름 밖: DC 분극 σ_e 실측 앵커 | §0 ④ L29 · §3-6 L146 · §3-9 L174–176 · §7-4 L264–269 | [인쇄] Table I–IV · [우리 산술] · 카드 판정 | Li|SE|Li 셀 (σ_e 아님) · 카드의 우리 쪽 앵커 값은 낡음 (카드 문제)

## 카드 문제

kim2025_impedance_decoupling_tlm_assb
1. 대칭셀 R_e 칸 엇갈림: §3 표 L100 "R_e (symmetric, LNO-coated) 62: 4.8 / 72: 53.1 / 82: 262.7 Ω·cm²" ↔ 같은 카드 Table S3 전사 (머리 L353 · 행 L355–357) 에서 4.8 / 53.1 / 262.7 은 CPE_i,gb C (µF·sᵑ⁻¹) 칸이고 R_e 칸은 336.8 / 7.4 / 3.7. L362–363 은 다시 "Table 의 R_e (4.8/53.1/262.7)" · "Fig 4f '336.8' 은 CPE_int C 값" 이라 적는데 전사 표의 CPE_int C 는 6.3 mF 이고, L347–348 은 "336.8 = CPE C 336.8 µF" 라 적음 — 세 서술이 서로 다르다 (L325 Fig 4f 막대 "82: 19.0/3.7" 의 3.7 은 전사 표 R_e 칸과 같다).
2. 풀셀 R_ion 62 wt%: §3 L101 · §5.3 L244 = 7.5 ↔ Table S4 전사 L368 R_i = 8.7 Ω·cm².
3. L109 "R_int (UNCOATED) symmetric 62: 127.2 / 72: 10.4 / 82: 6.2" ↔ Table S5 전사 (L381–383) 에서 이 세 수는 R_e 칸 (이온 차단 대칭셀엔 전하전달 r_int 가 없다 — L158–160) · L110 "R_w (UNCOATED) symmetric 62: 127.2 / 336.8?" 는 카드 자신의 '?' 표지이고 Table S5 에 R_w 칸이 없다.
4. L373 Table S4 주석 "(62 base? 사실 45/60 은 별도)" — 온도 행 (45 · 60 °C) 이 어느 조성인지 카드가 정하지 못함 (L418 은 같은 행을 "62 풀셀" 로 씀).
5. L122 · L567 "Cronau 단결정 3.0" — CLAUDE.md (원장 CL-91 · SELF-51, 2026-09-25) 는 3.0 을 Cronau 2021 SI 그림 S2c 의 µC 펠릿값으로 정정하고 "단결정" 라벨을 철회.

lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging
1. XPS 값: §3 L46 "Ni²⁺ 52.5 % (SLE) vs 43.9 % (BLE-10 하층), 상층 SSC Ni²⁺ 47.5 %" ↔ SI 표 L162 "S23 상층 SSC: Ni³⁺ 52.5 / Ni²⁺ 47.5 %" — 같은 수 52.5 가 SLE 의 Ni²⁺ 와 상층 SSC 의 Ni³⁺ 에 붙어 있다 (우연인지 옮겨 적은 혼동인지 카드로 판별 불가 · Fig 5h · S23 원문 확인 필요).

sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile
1. L345 "S5 (σ_ion 3.0 을 원문에 없는 논문에 붙임)" — "Cronau 2021 원문에 3.0 없음" 이라는 판단은 CLAUDE.md (CL-91, 2026-09-25 밤) 에서 거짓 음성으로 철회됨 (값은 Cronau 2021 SI 그림 S2c 에 있고 틀린 것은 "단결정" 라벨). 카드 (09-25 작성) 가 철회 전 판단을 옮겨 적음.

so2021_dem_fabrication_degradation_ductile_particles
1. **Minnmann 순수 SE 10 % 를 실험 근거로 씀**: L294 "우리 porosity@300 MPa (real_14 15.6 %) · Minnmann (10 %) = 제조-시점 조밀도" · L358 "DEM (…) 과 MPM (E=1.53 J2) 을 각각 실험 (Minnmann) 에 독립 보정" — 그 출처는 철회됨 (CLAUDE.md CL-94: Minnmann 2021 에 순수 SE 10 % @ 300 MPa 없음 · 우리 MPM 보정 수렴값).
2. 철회 · 하향된 우리 쪽 주장: L349 "porosity (15.93 %) · 두께 EMERGE" (CLAUDE.md 2026-08-12 정정: "EMERGE (no targeting)" 하향 — porosity 는 정지 프레임의 함수) · L358 "수렴 (real_14 porosity 15.6↔16.7↔exp, coverage Tabor 48–52 %) = 교차검증" (CLAUDE.md 2026-09-09 정정 CDX-16: porosity · coverage 일치는 같은 기하의 일관성 · 교차검증 철회 · 살아남는 것은 응력-정지 두께 하나).
3. L355 "σ_ionic = Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) GB · σ_e = Trevisanello 10/5 + NCM(r)" — CLAUDE.md: 3.0 = Cronau 2021 SI S2c 펠릿값 (단결정 라벨 철회 · CL-91) · Cronau(r_SE) 구간값은 Cronau 2022 에 없음 (모델 가정 · SELF-51) · σ_e 10/5 는 Trevisanello 가 크기를 뒷받침하지 않음 (A1 · 방향만).
4. 같은 조건 기공 판독 엇갈림: Fig 8c (Pfab 100 · SOC24) 0.18↔0.21 (L86 · L204) ↔ Fig 8d (SOC24 · Pfab 100) 0.22 (L87 · L204) — 어느 사이클 · 시점의 값인지 카드에 없음.
5. DOI 미확정: L3 "10.1149/1945-7111/abe796" ↔ L42 · L389 "abe796 계열" (표지 abed23 = IOP 내부) — 카드가 정식 DOI 를 확정하지 않고 권호 (168, 030538) 인용을 권함.

tron2023_lpscl_ccd_ambient_pressure
1. 낡은 우리 쪽 값: §7-4 L262–268 의 DC 분극 앵커 "SBE 4.47 · DBE 12.4 mS cm⁻¹ (비 2.77)" 와 그로 낸 벌크 ASR 2.24 · 0.81 Ω·cm² — CLAUDE.md 에서 10-19 에 앵커가 10-16 DC 분극 측정 (SBE 1.63 · DBE 4.68 mS/cm) 으로 대체됨 (카드 작성 10-14).

카드 문제 합계 13 (kim2025 5 · so2021 5 · lee2026 1 · sedlatschek2026 1 · tron2023 1). li2026 · siroma2015 · spencerjolly2023 · tabakovic2026 은 카드 자체 문제 없음.

카드가 이미 표지한 논문 쪽 문제 (카드 문제로 세지 않음): li2026 (표 3 인용 번호 +7 · 표 2 ↔ 본문 부피변화 · 단위 오기 "Ω·cm−2" — L44 · L60 · L67 · §10 L142–145) · siroma2015 (그림 12 z_B 표지 · (A.4) 부호 · 그림 2 캡션 분모 등 8 건 — L497–508) · spencerjolly2023 (Fig. 4B 캡션 ↔ 그림 — L102 · L208) · tabakovic2026 (그림 크기 10 배 · 고정 전압 ↔ 같은 SoC · 부호 서술 · 단위 오류 셋 — L194–198) · tron2023 ("결정학 밀도" ↔ 인용 문헌 · "Rct [Ω]" = Ω·cm² · 본문 ↔ 표 불일치 — L84 · L172–173 · L294–302) · sedlatschek2026 ([23] 펠릿 ↔ 단결정 · SD = 모집단 SD · 크기 효과 인용이 Li 금속 논문 — L410–415).
