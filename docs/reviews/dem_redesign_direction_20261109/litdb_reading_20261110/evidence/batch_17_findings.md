# batch_17 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `jung2023_single_crystal_ncm_morphology` (224 줄) · `kato2018_thick_electrode_assb_cycle_tortuosity` (488) · `ketter2025_resistor_network_models_predict_transport_properties` (369) · `kim2024_carbon_volumetric_occupation_se_domain` (209) · `kim2026_a3d_air_electrode_microstructure_transport` (702) · `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` (450) · `landesfeind2016_tortuosity_eis_electrodes_separators` (534). 끝까지 못 읽은 카드 없음 (짧은 두 장은 한 번에 · 나머지 다섯 장은 세 – 다섯 번에 나눠 마지막 줄까지 읽음).

배치의 성격: 수송 · 재료 실험 묶음이다. **실험만 넷** (jung2023 = NCM 단결정 ↔ 다결정 · kim2024 = 탄소 첨가제 · kato2018 = 후막 ASSB 율속 + 1D 해석식 · landesfeind2016 = 액체 LIB 의 EIS tortuosity 측정법), **실험 + 복셀 저항망 하나** (ketter2025 = NCM83–LPSCl), **복셀 구조 해석 + 1D FEM 하나** (kim2026_a3d = Li–O₂ 공기극), **실험 + DFT · MD 하나** (kim2026_pregranulation = LIB 건식 NCA). **DEM · MPM 을 쓴 카드는 없다.** 순수 LPSCl 의 밀도 · 기공은 ketter2025 의 한 점 (등방 500 MPa · 뺀 뒤) 뿐이고 압력별 곡선은 없다. 되돌아온 양을 잰 카드도 없다. 항복 · 경도는 AM 입자 (jung2023) 와 LIB 전극 · 과립 (kim2026_pregranulation) 값뿐이고 황화물 SE 값은 0 건이다. 그래서 k (DEM 의 한계) · l (소성의 어려움) 은 일곱 장 모두 "말 없음" 이고, 그 아래에 (3) 실험이 말한 "단단한 구 가정 밖의 것" 과 (4) 카드의 풀이를 구분해 적었다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `SD` (저자 공개 Source Data) · `derived(ours)` · `[인쇄]` · `[판독]` · `[우리 산술]` · `우리 산술` · `[추정]` · `[미확인]` · `판독` · `파생` · `digitized(추세)` · `n/a`) · 없으면 "표지 없음". "카드 서술 · 카드의 풀이" = 논문 문장이 아니라 카드 작성자의 서술. 따옴표 안 영어 문장은 카드가 옮겨 둔 원문. "내 검산" = 이 정독에서 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님). 카드가 "인용 금지" 표지를 붙인 값은 숫자를 옮기지 않고 줄 번호만 적었다 (ketter2025 의 L27 치밀 쪽 되돌림 값 · L262 의 NCM σ_e 추론 · landesfeind2016 의 Separion 행 L206–212 · 그리고 landesfeind2016 은 카드 머리 L4 가 판독 값 전체를 "정밀 인용 금지" 로 적어 판독 숫자는 옮기지 않았다). "랩 표준과 다른 문헌 값" = 순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ 과 다른 값이라는 표시 (기준은 그대로다).

형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계` (k · l 은 slug 옆에 인용할 서지 · m 은 `무엇을 | 우리 쪽 어디에 | 근거 위치`)

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

압력별 곡선이 있는 카드 = **0**. 순수 황화물 SE 를 눌러 밀도 · 기공을 잰 카드 = **1** (ketter2025 — LPSCl · 한 점). 밀도 값만 있는 카드 = 2 (kim2024 — Archimedes · kato2018 — 표의 명목 밀도).

- [a] ketter2025_resistor_network_models_predict_transport_properties | 순수 Li₆PS₅Cl 펠릿 (열확산 LFA 용): 370 MPa 3 min 선압 → 등방 500 MPa 60 min · ρ_geo 1.634 ± 0.012 g/cm³ · ρ_theo 1.86 g/cm³ · 상대밀도 87.87 ± 0.64 % → 기공 12.13 % (3 회) | §0 L14 · §3-1 L74 · §3-3 L102 · SI §S7 · SD `FigS18a` | 측정 (stated + SD) | 한 압력 (곡선 아님) · 등방압 60 min (일축 300 MPa 아님) · 하중을 뺀 뒤의 기하 밀도 (카드 L25 "등방 500 MPa 성형 후 무하중 LFA") · ρ_theo 1.86 은 랩 표준 (1.64) 과 다른 문헌 값 — 기공 12.13 % 는 그 1.86 기준 값 · 도메인 ≈ 20 µm · 소프트 밀링 (15 Hz 15 min) 을 거친 분말
- [a] ketter2025_resistor_network_models_predict_transport_properties | 진밀도의 출처 · 기준: 부피비 계산에 쓴 밀도 LPSCl 1.86 · NCM83 4.78 g/cm³ (refs Deiseroth 2008 · Woo 2009) · 상대밀도 = ρ_geo/ρ_theo (기하 밀도를 어떻게 쟀는지의 식은 카드에 없음) | §4-5 L186 · §3-1 L74 | stated (밀도) · 표지 없음 (식) | 피크노미터 실측이 아니라 문헌의 결정 밀도 (카드 표기 "ρ_theo") · 랩 표준과 다른 문헌 값
- [a] ketter2025_resistor_network_models_predict_transport_properties | 전기 셀의 순수 LPSCl (100 mg): 370 MPa 3 min 성형 → 50 MPa 누른 채 EIS → σ_ion 2.33 mS/cm @25 °C · 셀 지름 · 두께 · 성형 뒤 밀도는 n/a | §3-1 L68 · §4-5 L188 | 측정 → 입력 (stated + SD) · n/a (밀도) | 기공 값 0 — 같은 논문의 LFA 펠릿 (등방 500 MPa) 과 압밀 상태가 다름
- [a] ketter2025_resistor_network_models_predict_transport_properties | (인용 사례) Böger 2023 의 다공 LPSCl: 상대밀도 75.4–90.9 % 의 실측점 6 개 (열전도 0.269–0.498 W/m·K) — 밀도 축만 있고 압력 · 누른 방법은 카드에 없음 | §0 L17 · §3-5 L136 | stated (입력) · SD · "Böger 원문 미확인" | 열전도용 자료 · 압력 축 없음
- [a] kim2024_carbon_volumetric_occupation_se_domain | SE (Li₆PS₅Cl₀.₅Br₀.₅ · 카드 표기 LPSCl) 밀도 1.86 g/cm³ — Archimedes (이소프로판올) · 탄소 SC 0.67 g/cm³ | §3 L50–51 · §6 L127 | stated | 기공 · 압력 곡선 없음 (카드 L64 n/a) · Br 이 든 조성 · 무엇의 밀도인지 (분말 · 펠릿) 는 카드에 없음 ("치밀한 황화물 SE" 라고만) · 1.86 은 랩 표준과 다른 문헌 값
- [a] kato2018_thick_electrode_assb_cycle_tortuosity | 순수 SE 냉간 압분 펠릿 (σ₀ 용): 알루미나 실린더 420 MPa · 25 °C · Ar — Li₁₀GeP₂S₁₂ 3.2 · 75Li₂S–25P₂S₅ 유리 0.28 · LiI 유리 1.2 mS/cm · 펠릿 두께 · 상대밀도 · 측정 중 가압 = [미확인] · 조성 표의 SE 밀도는 세 SE 모두 2.00 g/cm³ | §3-1 L74–78 · §3-2 L88 · L92 · SI p.4–6 · Table 2 | stated (σ · 조건 · 2.00) · [미확인] (밀도 · 가압) | LGPS · 황화물 유리 — LPSCl 아님 · 기공 값 0 · 2.00 은 재료가 다른 문헌 값
- [a] kato2018_thick_electrode_assb_cycle_tortuosity | 같은 LGPS 분말의 냉간 펠릿 3.2 ↔ 소결 펠릿 8.3 mS/cm (× 2.6) · 유리 75Li₂S–25P₂S₅ 는 냉간 0.31 @ 360 MPa ↔ 열간 0.34 mS/cm (sakuda2013 카드 값) — 결정 SE 와 유리 SE 의 "냉간 ↔ 치밀" 차가 다름 | §3-1 L74–80 · SI p.4 | stated (3.2 · 8.3) · 우리 산술 (× 2.6) · 타 카드 · 교차 산술 | 전도도로 본 치밀화 차이지 기공 측정이 아님 · LPSCl 아님
- [a] jung2023 · kim2026_a3d · kim2026_pregranulation · landesfeind2016 | 해당 없음 — 순수 SE 를 다루지 않음 (jung2023 은 SE 분리막 100 mg 을 437 MPa 로 눌렀다는 것뿐 · 밀도 없음 L48) | — | — | —

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

되돌아온 양을 잰 카드 = **0**. 닿는 것은 "누른 압력과 잰 압력이 다르다" 는 기록뿐이다.

- [b] kato2018_thick_electrode_assb_cycle_tortuosity | 재지 않음. 세 층을 500 MPa 로 함께 누른 뒤 10 MPa 로 집전체 접합 → 하우징 50 MPa 에서 전기화학 측정 · 두께는 기공 0 의 명목값 (실측 언급 없음) — 카드 서술: 되튐 · 기공은 치밀 장부 (용량 밀도 q) 의 오차로 들어가 상자 기준 τ 를 낮추는 쪽 | §4-4 L243–245 · §3-3 L107 · §7 L338 · §10-3-6 L450 | stated (압력 이력) · [미확인] (두께 실측) · 카드 서술 (방향) | 되돌아온 양 · 하중 중 두께 0 건 · LGPS · 유리 + LCO
- [b] ketter2025_resistor_network_models_predict_transport_properties | 재지 않음. 두 상태만 있음 — LFA 펠릿 = 등방 500 MPa 뒤 하중 없이 잰 기하 밀도 · 전기 셀 = 370 MPa 성형 뒤 50 MPa 누른 채 (밀도 n/a) | §0 L25 · §4-5 L188 · L191 | 카드 서술 · n/a | 같은 시료의 누른 채 ↔ 뺀 뒤 비교 없음
- [b] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 압밀의 되돌아옴 아님 — 전극 나노압입의 탄성 회복 (%): 기존 전극 25.2 → 36.5 · 과립화 전극 38.4 → 44.2 (사이클 전 → 전셀 10 사이클 뒤) | §3-8 L183–188 · 표 S3 | [인쇄] | LIB 건식 전극 (NCA + PTFE + 탄소) 의 겉보기 값 · 압입 회복이지 탈압 두께 회복이 아님 · 깊이 축 단위 의심 (L191)
- [b] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 탈압 아님 — 사이클에 따른 두께 팽창: 144 µm → 10 사이클 뒤 162 µm (+12.5 %) / 156 µm (+8.33 %) · 저자: 원인 "remains uncertain" | §3-8 L194 · Fig 5h–j | [인쇄] | 전기화학 사이클 팽창 — 되돌아옴 자료 아님
- [b] kim2024_carbon_volumetric_occupation_se_domain | 재지 않음. σ 를 SE/복합체/SE 적층 517 MPa 와 103 MPa 가압 뒤 쟀다고만 적혀 있음 (두께 · 밀도 · 압력별 σ 값 없음) | §2 L43 · §6 L121 | 표지 없음 | —
- [b] jung2023 · kim2026_a3d · landesfeind2016 | 이 카드들에 없음 | — | — | —

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산

황화물 SE 의 항복 · 경도 · 크리프 값을 준 카드는 **없다**. 있는 것은 AM 입자 경도 (jung2023) 와 LIB 전극 · 과립 · DFT 값 (kim2026_pregranulation), 다른 카드에서 옮긴 SE 탄성 (kato2018) 뿐이다. **일축 항복 세기로의 환산은 어느 카드에도 없다.**

- [c] jung2023_single_crystal_ncm_morphology | NCM 입자 경도 (particle hardness): 단결정 SC 972.7 MPa · 다결정 PC ~113.3 MPa (≈ 8.6 배) — 정의 = micro-indenter (MCT-W500 · Shimadzu) 응력–변형 곡선의 peak · 액체 전해질 침지 뒤 PC 는 급감 · SC 는 유지 (정성) | §3 L60–61 · Fig 3c (L100) · Fig S8 (L112) | stated · stated(정성) | AM (NCM · Ni 82 %) 입자 값 — SE 아님 · D50 5.0 / 4.9 µm · 시료 수 · 하중 조건은 카드에 없음 · 일축 항복 환산 없음
- [c] jung2023_single_crystal_ncm_morphology | 분말 값: tap density SC 2.10 / PC 2.02 g/cm³ · BET 0.23 / 0.28 m²/g | §3 L62–63 · Fig S5 | stated | 압밀 밀도 아님
- [c] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 과립 압축 강도 C₁₀: 1.832 → 3.889 kgf/mm² (= 17.97 → 38.14 MPa · × 2.12) — NCA + PTFE (+ 탄소) 과립 · 미세 압축 시험 (MCT-510) · C₁₀ 의 정의 · 시료 수 · 과립 크기는 [미확인] | §3-2 L92 · Fig 1i | [인쇄] · [우리 산술] (MPa 환산) | LIB 건식 과립 — SE 아님
- [c] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 전극 나노압입 (G200): 경도 24.5 / 19.3 MPa (기존 / 과립화 · 사이클 전) → 5.6 / 9.0 MPa (10 사이클 뒤) · 탄성률 774.65 / 327.13 → 125.66 / 163.58 MPa | §3-8 L183–190 · 표 S3 | [인쇄] | 다공 복합 전극의 겉보기 값 (입자 물성 아님 — 카드 L191) · LIB · 가로축 단위 의심
- [c] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 전극 인장 (UTM): 최대 응력 0.61 MPa (연신 7.4 %) / 0.59 MPa (23.6 %) · toughness 36.6 → 121.2 kJ/m³ | §3-3 L102 · Fig 2g · S16 | [인쇄] | PTFE 로 묶인 막의 인장 — 압축 항복 아님
- [c] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | DFT (NCM622 대리 모형 · PBE · 힘 수렴 0.2 eV/Å): pristine B 128 · E 141 · G 54 GPa · ν 0.315 · Vickers 4.40 GPa — 경도는 B · G 의 경험식 재표현 (카드 재현 ≤ 3 %) 이라 독립 지표가 아님 | §3-5 L140–156 | [인쇄] · [우리 산술] (ν · 경도 재현) | AM (그것도 NCA 가 아닌 NCM622) · 느슨한 수렴 · 구조 하나 · 카드: 앵커로 쓰지 않음 (L307)
- [c] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | PTFE · PVDF 물성 표 (표 S1) 가 있으나 출처 인용이 없어 카드가 입력으로 옮기지 말라고 적음 — 숫자 옮기지 않음 | §5 L284 · §7-4 L323 | [인쇄] (출처 없음) | —
- [c] kato2018_thick_electrode_assb_cycle_tortuosity | SE 의 탄성만 (다른 카드에서 옮김): LGPS E 21.7 GPa (deng2016 카드 · DFT 결정) · 75Li₂S–25P₂S₅ 유리 E 24 GPa (Sakuda 카드 · 실험) — 원문은 "thiophosphates exhibit similar elastic properties³⁶ and can be easily deformed by cold pressing" (SI p.8) 라고만 | §4-2 L220–221 | 타 카드 값 · stated (인용문) | 항복 · 경도 · 크리프 0 건 · LPSCl 아님
- [c] ketter2025 · kim2024 · kim2026_a3d · landesfeind2016 | 이 카드들에 없음 (kim2024 L64 · L203 "E_SE · σ_y · 소성 데이터 없음") | — | — | —

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

하중 몫을 수로 준 카드는 **없다**. 닿는 것은 (1) 같은 조건으로 눌렀을 때 조성에 따라 남는 기공 (ketter2025 — 실측), (2) AM 등급에 따른 균열 (jung2023 · kim2026_pregranulation — 정성), (3) LIB 전극에서의 정성 해석 (landesfeind2016 · kato2018).

- [d] ketter2025_resistor_network_models_predict_transport_properties | 단단한 NCM83 + 무른 LPSCl 을 같은 조건 (370 MPa 선압 → 등방 500 MPa 60 min) 으로 누른 뒤 남는 기공 (하중 몫 아님 · 결과만): φ_NCM 0 / 20 / 40 / 60 / 80 / 100 vol% → 12.13 / 15.62 / 21.16 / 22.42 / 25.33 / 29.24 % | §3-3 L102–107 · SD `FigS18a` | SD (측정) | 한 압력 · 뺀 뒤 · LPSCl ≈ 20 µm ≫ NCM ≈ 2 µm (우리와 크기 계층 반대 — 카드 L291) · ρ_theo 1.86 / 4.78 기준 · 누가 하중을 지는지는 재지 않음
- [d] ketter2025_resistor_network_models_predict_transport_properties | 저자 문장: 조성과 밀도 사이에 선형 관계가 있다 — "a linear relationship between composition and density exists" | §4-1 L162 · SI §S7 | stated (인용문) | 밀도에 대한 문장 · 하중 몫 아님
- [d] ketter2025_resistor_network_models_predict_transport_properties | VGCF 를 넣은 복합 (φ_NCM 40 %) 의 기하 밀도: 2.387 (0 wt%) → 2.567 → 2.529 → 2.514 → 2.409 → 1.991 g/cm³ (5 wt% 에서 급락) | §3-4 L120–125 · SD `FigS18b` | SD · 단일 측정 | 섬유 첨가제가 많으면 덜 눌린다는 방향의 자료 한 줄 · 기공률 환산은 카드에 없음
- [d] jung2023_single_crystal_ncm_morphology | 크기가 같은 (D50 4.9 / 5.0 µm) AM 두 등급: 다결정 PC (1차 입자 ~600 nm 응집 · 입계 + 내부 공극) 는 제조 · 사이클 중 입계 따라 균열 · 단결정 SC 는 억제 — 입자 경도 ~113.3 ↔ 972.7 MPa · ASSB 제조 압력 437 MPa | §1 L27–32 · §3 L60 · L74 · §7-B L145–147 | stated · stated(정성) | 하중 몫 · 균열 분율 수치 없음 · 균열 사진은 100–150 사이클 뒤 (제조 직후 균열의 정량 없음)
- [d] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 캘린더링 직후 균열은 큰 (≈ 10 µm) NCA 2차 입자에서 보이고 작은 각진 입자 (1–3 µm) 에는 안 보임 (정성). 저자 주장 = 섬유로 묶인 과립이 점진 변형 · 조절된 파괴로 응력을 흡수 · 재분배 ("not from the fibril network confining individual secondary particles like a physical corset" p.7) — 힘 · 응력 측정 0 인 가설이고 과립화 전극의 기공률이 더 높음 (0.333 ↔ 0.305) | §3-3 L100–101 · §3-2 L93 · §7-2 L310–312 | [인쇄] (균열 유무 · 인용문) · [판독] (크기 의존) · 카드 서술 (가설 판정) | LIB 건식 전극 · 압력 값 [미확인] · 균열 분율 없음 · 카드의 "접촉력 ∝ R² · 임계력 ∝ R" 은 [추정]
- [d] landesfeind2016_tortuosity_eis_electrodes_separators | 저자의 기전 해석 (정성): 도전재는 단단해 비압축 지지체로 LFP 응집체 사이를 벌림 · 높은 압축에서 LFP 응집체가 깨져 판상화 (도전재가 적을수록 넓은 판) · 흑연은 무른 입자 자체가 눌려 기공이 줄어듦 | §5-6 L283–284 · A1384–A1385 · Fig 18 | stated (원문 해석 — 카드의 한국어 옮김) | LIB 전극 · 하중 몫 수치 없음
- [d] kato2018_thick_electrode_assb_cycle_tortuosity | 원문: 황화물 SE 는 냉간 압분으로 쉽게 변형되어 SE 부피분율이 높을 때 전극 형태가 비슷해진다 (두 SE 의 τ 가 같다는 가정의 근거 ③) · SEM 은 SE 영역의 void · crack 을 보임 (정성) | §4-2 L220 · SI p.8 · §0 L44 · p.610 | stated | 가정의 근거로 쓴 문장 — 측정 아님
- [d] kim2024 · kim2026_a3d | 이 카드들에 없음 | — | — | —

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값의 수

**이 배치에 없음** — 접촉 법칙을 다룬 카드가 없다 (DEM 을 쓴 카드 0).

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

**이 배치에 없음** — MPM 을 쓴 카드가 없다. 아래 둘은 MPM 이 아니라 복셀 수송 계산의 해상도 자료 (참고용 — 쓸 수 있는 부분은 m 에 옮김).

- [f] ketter2025_resistor_network_models_predict_transport_properties | (MPM 아님 · 복셀 저항망) NCM 입자 = 복셀 1 개 (2 µm) · LPSCl 도메인 = 500 복셀 덩어리 (등가 지름 19.7 µm) · 거친 망 60³ (10 µm/복셀) 은 문턱 근처에서 자릿수로 무너짐 (σ_e @ φ_NCM 20 %: 3.3 × 10⁻¹¹ ↔ 300³ 0.00918 mS/cm) · 오차 관리 = 잔차 r < 10⁻⁹ K + 직렬 · 병렬 층상 해석해 재현 + Yuge 수정 EMT 재현 · 실현 (시드) 수는 n/a | §3-6 L142–151 · §4-2 L165–169 | SD · derived(ours) (부피 등가) · stated · n/a | 수송 계산 — 역학 · 접촉 없음
- [f] kim2026_a3d_air_electrode_microstructure_transport | (MPM 아님 · GeoDict 복셀) 0.01 µm/복셀 (≈ 8 µm 영역 · 축당 약 800 복셀) · foam 은 8 µm/복셀 로 두께 120 µm — 고른 이유는 "충분한 구조 정확도 + 합리적 계산 비용" 의 타협 · 수렴 시험은 카드에 없음 | §2.1 L145–155 | 표지 없음 | 수송 계산 · Li–O₂

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

2D → 3D 의 경고 · 증거를 직접 준 카드는 **없다**. 닿는 두 줄:

- [g] landesfeind2016_tortuosity_eis_electrodes_separators | 문헌 대조표의 한 줄: Ebner & Wood [16] 이 SEM 상면 · 단면 (2D 영상) 에서 Bruggeman Estimator 로 관통 방향 지수 α = 0.83 을 얻어 N_M 을 계산 (LCO) · 3D 재구성 기반 τ 가 EIS 보다 낮게 나오는 이유로는 영상 해상도 (도전재 · 바인더 미해상) 를 지목 | §5-8 L308 · §5-5 L269 · §5-6 L285 | stated | 2D → 3D 전환의 정확도를 따진 문장은 카드에 없음 · LIB
- [g] kim2026_a3d_air_electrode_microstructure_transport | 2D → 3D 는 아님 — 3D 구조를 1D 로 평균화할 때의 한계를 저자가 적음: "1D framework relies on volume-averaged effective properties... cannot explicitly capture pore-scale heterogeneities and microstructure-resolved deposition" | §6-(d) L615–616 · 논문 p.7 | stated (인용문) | Li–O₂
- [g] 그 밖의 카드 | 이 배치에 없음 (kato2018 의 모형은 1D 해석식) | — | — | —

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

DEM 에서 넘긴 선례 = **0**. 닿는 것은 "3D 구조 → 유효 물성 → 1D 전기화학" 으로 넘긴 한 건이다.

- [h] kim2026_a3d_air_electrode_microstructure_transport | DEM 아님 — CAD 단위셀 (STL) → 복셀 (GeoDict) → 유효 물성 (기공 · 비표면적 · σ_e · σ_ion · D_O₂) → 1D FEM (COMSOL) 로 넘긴 선례. 넘긴 시점 = 고정된 구조에서 유효 물성을 뽑은 뒤 · 구조에서 못 얻는 동역학 값은 문헌 + 실험 방전 곡선에 맞춰 고정 | §2.1 L134–165 · §2.2 L226–231 · Table S2 L233–257 | 표지 없음 | Li–O₂ · 압력 · 입자 없음
- [h] ketter2025_resistor_network_models_predict_transport_properties | DEM 아님 — 계산용 미세구조는 합성 (복셀 클러스터 무작위 삽입) 이고 FIB-SEM 도 DEM 도 아님 | §4-3 L171–176 | stated | —
- [h] 그 밖의 카드 | 이 배치에 없음 | — | — | —

## i. 복합 양극 (AM + SE) 의 압력별 기공

AM + SE 복합의 **압력별** 기공 곡선 = **0**. 한 압력에서의 **조성별** 기공이 ketter2025 에 있다. 압력별 세 점은 SE 가 없는 LIB 전극 (landesfeind2016) 것이다.

- [i] ketter2025_resistor_network_models_predict_transport_properties | NCM83 + LPSCl 복합 펠릿 (탄소 · 바인더 없음) 의 조성별 기공 — 한 조건 (370 MPa 선압 → 등방 500 MPa 60 min): 15.62 / 21.16 / 22.42 / 25.33 % @ φ_NCM 20 / 40 / 60 / 80 vol% (= w_NCM 39 / 63 / 79 / 91 wt%) · 양 끝 순수상 12.13 % (LPSCl) · 29.24 % (NCM83) | §3-3 L102–107 · §4-5 L187 · SD `FigS18a` | SD (측정 · 3 회) | 압력별 곡선 아님 · 뺀 뒤 · 크기 계층 반대 (LPSCl 20 µm ≫ NCM 2 µm) · ρ_theo 1.86 / 4.78 기준 (랩 표준과 다른 문헌 값) · 카드: "porosity 매핑은 LFA 펠릿만 가능" (L292)
- [i] ketter2025_resistor_network_models_predict_transport_properties | 카드의 조성 환산: AM 70 / 75 / 80 / 82 wt% ↔ φ_NCM 47.6 / 53.9 / 60.9 / 63.9 vol% (2 원계 · 밀도 1.86 / 4.78) | §7-5 L290 | derived(ours) | 환산일 뿐 그 조성의 실측 기공은 없음
- [i] landesfeind2016_tortuosity_eis_electrodes_separators | (ASSB 아님 · LIB 전극) LFP-highC (LFP : PVDF : 탄소 = 70 : 15 : 15) 를 50 / 150 / 400 MPa 로 누른 뒤 기공률 0.49 / 0.34 / 0.27 (질량 수지 · 뺀 뒤) | §5-7 L291–293 · §9 ⑫ L443 · Fig 12 | 표지 없음 | SE 가 없는 액체계 전극 — 카드: "수치 전이 불가" · 세 점
- [i] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | (ASSB 아님 · LIB 건식 전극) NCA : 탄소 : PTFE = 96 : 1.8 : 2.2 · 144 µm · 복합 밀도 3.3–3.4 g/cm³ · 기공률 0.305 (기존) / 0.333 (과립화) — 캘린더링 압력 값 · 기공 측정법 [미확인] | §3-1 L73 · §3-4 L111 · 표 S2 | [인쇄] · [미확인] | 압력 축 없음 · SE 없음
- [i] kato2018_thick_electrode_assb_cycle_tortuosity | 기공을 재지 않음 — ε · 용량 밀도 · 두께가 모두 기공 0 명목 (500 MPa 압밀) · SEM 에서 void · crack 은 정성 | §3-2 L91 · §3-3 L107 · §6 L288 | stated · 우리 산술 (명목값 재현) | 기공 값 0
- [i] kim2024 · jung2023 | 기공 값 없음 (kim2024 의 30.0 → 13.9 vol% 는 SE 의 상 부피분율이지 기공이 아님 L191 · jung2023 은 437 MPa 제조만 L34) | — | — | —
- [i] kim2026_a3d | 해당 없음 (금속 골격 공기극의 설계 기공 45.6–56.9 %) | — | — | —

## j. 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] ketter2025_resistor_network_models_predict_transport_properties | 모델에 기공 구조가 없다는 저자 문장: "As the input parameters … were taken from porous samples and a linear relationship between composition and density exists, porosity is accounted for in the simulation to a certain extent, although the actual pore structure is not explicitly simulated" | §4-1 L162 · SI §S7 | stated (인용문) | 수송 모델 — 압력은 실험에만 있고 모델에는 기하로도 들어오지 않음 (카드 L181)
- [j] ketter2025_resistor_network_models_predict_transport_properties | 첨가제 · 불명확한 구조는 못 다룸: VGCF 는 "additives that cannot be simply modelled by a voxel approach" (p.6) · Si–LPSCl–C 사례 실패의 이유 "no well-defined microstructure" | §3-4 L129 · §3-5 L138 | stated (인용문) | —
- [j] kato2018_thick_electrode_assb_cycle_tortuosity | 원문: tortuosity 추정은 "challenging due to the complex battery reactions taking place" (p.610) · 10 mS/cm 를 넘는 재료 값은 소결 · 열간압 상태라 "materials exhibiting high conductivities in the compressed state are desirable" (p.612) | §4-2 L218 · §3-9 L192 | stated (인용문) | 가압 계산이 아니라 "눌린 상태의 전도도" 가 문제라는 실험 쪽 문장
- [j] kato2018_thick_electrode_assb_cycle_tortuosity | (논문의 고백이 아니라 카드가 찾은 빈 곳) 본문 · SI 어디에도 기공률 · 두께 실측 여부 · 펠릿 측정 중 가압 · SE 입도 분포가 없음 | 원문 대조 기록 L477 | [미확인] | —
- [j] kim2026_a3d_air_electrode_microstructure_transport | "1D framework relies on volume-averaged effective properties... cannot explicitly capture pore-scale heterogeneities and microstructure-resolved deposition" (p.7) · 충전은 모델하지 않음 (생성물 산화는 방전의 역으로 기술 못 함) | §6-(d) L615 · §2.2 L172–174 | stated (인용문) · 표지 없음 | Li–O₂ — 가압 · 탈압과는 "평균화하면 국소 불균일을 못 본다" 는 점에서만 닿음
- [j] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 저자: 10 사이클 두께 팽창의 원인은 "remains uncertain" (p.10) · DFT 의 군집 탈리 모형은 "bounding case rather than a unique structural assignment" · 반쪽 셀 실패에 Li 금속 음극 문제가 섞일 수 있음 (p.9) | §3-8 L194 · §3-5 L154 · §3-7 L175 | [인쇄] | 가압 계산 없음 — 캘린더링 압력 · 응력은 재지도 계산하지도 않음 (카드 판정 L31)
- [j] landesfeind2016_tortuosity_eis_electrodes_separators | effective τ 는 시료마다 실험으로 정하는 값이라 다른 기하 (입자 형상 · 기공률) 로 외삽할 수 없음 (A1374) · 형태 · 도전재 의존이 커서 문헌 값과의 엄밀 비교는 불가능 (A1385–A1386) · 3D 재구성과의 직접 비교는 조성 · 입경 · 형상이 같을 때만 (A1385) | §3-1 L70 · §5-8 L312 · §5-6 L285 | stated (카드의 한국어 옮김) | 수송 측정 — "눌러 바뀐 구조의 값은 그 구조에서만 유효" 라는 점에서 닿음
- [j] jung2023 · kim2024 | 논문이 적은 한계는 카드에 없음 (카드 자신의 한계 절 §10 뿐 — 기공 · 전도도 · 압밀 미측정) | — | — | —

## k. DEM 의 한계 (논문이 직접 말한 문장 · 수치)

**DEM 을 쓴 논문이 이 배치에 없다** → "DEM 을 쓰면서 한계를 말한 문장" 은 0 건이고 일곱 장 모두 "말 없음" 이다. 아래는 (3) 실험이 말한 "단단한 구 · 점접촉 가정 밖의 것" 과 (4) 카드의 풀이다 — 인용할 때 "DEM 논문의 고백" 으로 쓰지 않는다.

- [k] landesfeind2016_tortuosity_eis_electrodes_separators — Landesfeind, Hattendorff, Ehrl, Wall, Gasteiger, J. Electrochem. Soc. 163 (7) A1373–A1387 (2016) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 비슷한 기공률대에서 판상 흑연의 N_M "18–19" ↔ 구형 NMC "10–11" (약 2 배) — 판상 입자가 집전체와 수평으로 정렬해 관통 이온 전도를 막음 · 구형 입자 Bruggeman 은 전극에서 ~1.5–3 배 과소 | §5-5 L260–267 · §0 L32 · A1383 · A1386 | stated | 액체 LIB · 구 입자 모델에 대한 문장이 아님 — 카드의 풀이: "구 DEM 이 표현 못 하는 축" (L346) · "'강체 구' 근사와 반대 극 — 형상 효과가 결과의 주인공" (L169)
- [k] landesfeind2016_tortuosity_eis_electrodes_separators — 같은 서지 | (3) 원문 문장: "the experimental data of N_M or τ vs. ε could only be properly represented when a variable prefactor f was used … could not be represented by a generalized Bruggeman equation with the prefactor f = 1, contrary to what was reported in studies with 3D reconstructed electrodes" | §5-6 L280–281 · A1385 | stated (인용문) | Bruggeman · 3D 재구성에 대한 문장 (DEM 아님)
- [k] landesfeind2016_tortuosity_eis_electrodes_separators — 같은 서지 | (3) 누르면 입자 모양이 바뀐다는 관찰: 높은 압축에서 LFP 응집체가 깨져 판상화 · 흑연은 무른 입자 자체가 눌림 (압축 50–400 MPa · SEM Fig 18) | §5-6 L283–284 · §4-6 L168 · §5-7 L291–293 · A1384–A1385 | stated (카드의 한국어 옮김) | 정성 · LIB
- [k] kato2018_thick_electrode_assb_cycle_tortuosity — Kato, Shiotani, Morita, Suzuki, Hirayama, Kanno, J. Phys. Chem. Lett. 9, 607–613 (2018) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 흑연이 막자 전단으로 변형되어 세로로 퍼져 음극의 tortuosity factor 가 높음 (3.32 ↔ 양극 2.47) · 황화물 SE 는 "can be easily deformed by cold pressing" (SI p.8) · SE 영역의 void · crack 이 이온 전달을 방해 (p.610 · 정성) | §4-6 L254 · §0 L39 · §4-2 L220 · §0 L44 | stated | 카드의 풀이: "입자 형상 변화가 τ 를 올린다는 정성 증거 (강체구 DEM 이 못 그리는 쪽)" (L254) · "강체구 DEM vs 실물 (유리 SE 의 흐름 · 흑연 변형)" (L346) — 논문 문장이 아님
- [k] jung2023_single_crystal_ncm_morphology — Jung, Kim, Suh, Kim, You, Park, Song, Yu, Lee, Cho, Park, Chem. Eng. J. 470, 144381 (2023) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 크기가 같은 (D50 4.9 / 5.0 µm) AM 이 결정성에 따라 경도 8.6 배 · 균열 거동이 갈림 — 다결정 2차 입자는 1차 입자 (~600 nm) 응집체로 입계 · 내부 공극을 갖고 깨짐 | §3 L60–66 · L74 · §7-A L134–136 | stated · stated(정성) | 카드 서술: 우리 DEM 은 AM 을 보통 단단한 구로 둔다 (L171 · L217) — 한 개의 구에는 내부 공극 · 입계가 없다는 연결은 카드의 풀이
- [k] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation — Kim, Oh, …, Lee, Choi, Sun, Chem. Eng. J. 545, 179740 (2026) | DEM 을 쓰지 않음 — 말 없음. (4) 카드의 풀이: 강체 구 · Hertz/hysteresis · 파괴 판정 · 점착으로는 PTFE 섬유 · 바인더 막 · 결합 (bond) 된 과립 · 첨가 순서가 표현되지 않음 · 과립 ≈ 2 mm 와 서브 µm 결합 단위는 입자 상자 (≈ 100 µm 급) 의 양 끝 밖 | §4-3 L223 · §7-6 L337 | [추정] | 논문 문장 아님 · LIB
- [k] ketter2025_resistor_network_models_predict_transport_properties — Ketter, Greb, Bernges, Zeier, Nat. Commun. 16, 1411 (2025) | DEM 을 쓰지 않음 — 말 없음. 닿는 것 ("맞춘 · 묶은 값은 물성이 아니다" 부류): 저항망은 기공 · 입계 · 입자 간 접촉을 순수상 펠릿 값에 묶어 넣는데, 복합체 속 그 상의 상태가 순수상 펠릿과 다르면 틀림 — 순수상 기공 12 · 29 % ↔ 복합 15.6–25.3 % · 이온 문턱 근처 (φ_NCM 60–80 %) 에서 σ_ion 10.7–58 배 과대 | §4-1 L162 · §7-4 L287 · §3-2 L89–90 | stated (입력의 성격) · SD (비) · 카드 서술 (풀이) | 복셀 수송 모델의 한계지 DEM 의 한계가 아님
- [k] kim2024_carbon_volumetric_occupation_se_domain — Kim, Park, Kang, Jung, Kim, Yu, Kim, Lee, Sun, Cho, Adv. Funct. Mater. 34, 2409318 (2024) | DEM 을 쓰지 않음 — 말 없음. (3) 실험: 탄소 첨가제는 저밀도 (0.67 g/cm³) 라 SE 영역 (1.86 g/cm³) 을 부피로 차지하는 제 3 상이고 구 ↔ 섬유 형태가 이온 전도를 가름 (0.087 ↔ 0.105 mS/cm) | §3 L50–52 · L59 · §4 L76–79 | stated | 카드 서술: 우리 쪽 탄소 표현은 전자 전도 기여만 · 부피 점유는 부분적 (L139)
- [k] kim2026_a3d_air_electrode_microstructure_transport — Kim, Jung, Jo, Bae, Hyun, Gang, Jeon, Kang, Lee, J. Power Sources 686, 240471 (2026) | DEM 을 쓰지 않음 — 말 없음 (입자가 없는 정렬 골격). 카드 서술: 복셀 계산은 접촉 목이 복셀로 풀릴 때만 협착을 잡는다 | §6-(a) L557–562 | 카드 서술 | 복셀 계산에 대한 풀이 — DEM 한계 문장 아님

## l. 소성변형이 왜 어려운가 (논문의 설명 · 택한 우회 · 그 값)

**입자 계산에 소성을 넣은 논문이 이 배치에 없다.** "왜 어려운가" 를 설명한 문장도 없다 (일곱 장 모두 "말 없음"). 아래는 닿는 주변 근거다.

- [l] kato2018_thick_electrode_assb_cycle_tortuosity — Kato et al., J. Phys. Chem. Lett. 9, 607–613 (2018) | 말 없음 (입자 계산 없음). SE 의 변형은 계산하지 않고 가정의 근거로만 씀: "thiophosphates exhibit similar elastic properties³⁶ and can be easily deformed by cold pressing, the electrode morphology would be comparable especially at high SE volumic fractions" → "두 SE 의 tortuosity factor 가 같다" 로 놓음. 맞춘 값 = SE 계마다 하나씩 2 개 (X_j) · 검증 = 임피던스 정합 (자유 값이 넷이라 독립 검정이 아님) | §4-2 L216–221 · §3-8 L184 · SI p.8 | stated (인용문) · 카드 서술 (독립 검정 아님) | 수송 추출에서의 우회지 소성 계산의 우회가 아님
- [l] landesfeind2016_tortuosity_eis_electrodes_separators — Landesfeind et al., J. Electrochem. Soc. 163 (7) A1373–A1387 (2016) | 말 없음 (시뮬레이션 없음). 누르면 입자 모양 · 배열이 바뀌어 수송이 달라진다는 실험 쪽 근거만: LFP-lowC 는 기공률 50 → 30 % 에서 τ ~4.5 → ~7 로 급증 (응집체 파쇄 · 판상화) · 흑연은 τ 가 기공률에 거의 무관 (~4.8 → ~5.2) | §5-6 L275–276 · L283–284 · A1384–A1385 | stated | LIB — 하중 이력 · 되돌아옴 없음
- [l] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation — Kim et al., Chem. Eng. J. 545, 179740 (2026) | 말 없음 (입자 · 전극 스케일 계산 0). 저자가 택한 우회 = 원자 스케일 계산으로 입자 스케일 역학을 설명: DFT (NCM622 2×3×2 · 480 / 420 원자 · 모드당 구조 하나) + CHGNet MD (NPT 50 ps → NVT 1 ns · 300 K). 맞춘 값 0 · 실험 대조 0 (응력 흡수는 한 번도 측정되지 않음) · 스케일 차 4–6 자릿수 (nm ↔ 2 mm 과립 · 10 µm 입자) | §4-2 L216–218 · §7-8 L344 · §0 L31 | [인쇄] (설정) · 카드 서술 (스케일 차 · 미측정) | 카드: 실험 쪽에서 NCA 는 "형상 소성 없음, 파괴만" 이고 형상을 바꾸는 상은 PTFE 뿐 (L221)
- [l] ketter2025_resistor_network_models_predict_transport_properties — Ketter et al., Nat. Commun. 16, 1411 (2025) | 말 없음 (역학 없음 — 카드 서술 "압밀 · 재배열 · CONTACT 소성도 SHAPE 소성도 없다" L181). 역학을 건너뛴 우회와 그 값: 순수상 펠릿 실측 넷 (σ_ion 2.33 · σ_e 5.22 mS/cm · κ 0.32 / 0.71 W/m·K) 을 입력 + 맞춘 값 하나 (계면 열저항 2 × 10⁻⁶ m²K/W · "it is found empirically") + 구조 값 하나 (클러스터 500 복셀 — SEM 도메인 크기에 맞춘 선택으로 읽힌다는 카드 풀이) · 검증 = 같은 조성 6 점의 EIS · DC · LFA + 문헌 3 건 (+ 실패 1 건) · 비용 300³ "up to 5 days, HPC" ↔ 60³ "< 1 hour, Laptop" | §1 L45 · §3-3 L110 · §3-6 L149–150 · §4-4 L181 | stated · SD · 카드 서술 | 소성 계산의 우회가 아니라 "압밀을 계산하지 않고 눌린 시료의 값을 입력으로 받는" 길
- [l] jung2023_single_crystal_ncm_morphology — Jung et al., Chem. Eng. J. 470, 144381 (2023) | 말 없음 (시뮬레이션 없음). 카드 서술: AM 을 단단한 구로 두면 경도 차 (8.6 배) 는 탄성 압밀이 아니라 파괴 문턱 · 접촉 면적 상한에서만 작동하고 "압밀은 SE 소성이 지배" | §10 L217–219 | 카드 서술 | 논문 문장 아님
- [l] kim2024 · kim2026_a3d | 말 없음 (kim2024 L80 "입자 형상 소성은 이 논문 범위 밖" · kim2026_a3d 는 고정 구조) | — | — | —

## m. 받아들일 통찰 (무엇을 · 우리 쪽 어디에 · 왜)

**jung2023**
- [m] jung2023_single_crystal_ncm_morphology | AM 을 크기만이 아니라 등급 (다결정 = 입계 + 내부 공극 · 무름 / 단결정 = 치밀 · 단단) 으로 나눠 입력표에 적는다 — 같은 D50 (4.9 / 5.0 µm) 에서 경도가 8.6 배 다르고 균열 거동이 갈림 | 조건 R7 · 단계 5 (AM 입력표의 결정성 칸) | §3 L60–66 · L74 · §7-A L134–136
- [m] jung2023_single_crystal_ncm_morphology | 결과 전 대조 (방향): 437 MPa 로 만든 NCM : LPSCl : Super P = 60 : 35 : 5 양극에서 다결정은 균열 · 단결정은 억제 · 5C 용량 유지 74.0 ↔ 41.6 % — 순서만 견준다 (절대값 대조 금지 — 카드 L195) | 결과 전 대조 항목 (R7 · 단계 7) | §3 L71–74 · §8-④ L193–195
- [m] jung2023_single_crystal_ncm_morphology | 함정: 같은 재료 대비가 매질에 따라 뒤집힌다 (액체 LIB 에서는 다결정이 분극이 작고 ASSB 에서는 단결정) — 액체계 문헌의 방향을 고체계로 옮기지 않는다 | 흐름 밖: 실험과의 대조 (문헌 선별 규칙) | §5 Fig 4 · 6 (L101 · L103) · §10 L212–214
- [m] jung2023_single_crystal_ncm_morphology | 재료 값의 정의를 값과 같이 적는다 — 여기의 "입자 경도" 는 미세 압축 응력–변형 곡선의 peak 이라 압입 경도 · 항복 세기와 같은 칸에 놓지 않는다 | 단계 0 (재료 값의 정의 칸) | §3 L60

**kato2018**
- [m] kato2018_thick_electrode_assb_cycle_tortuosity | 장부 규칙: 실험 tortuosity factor 를 상자 기준으로 옮길 때 두께를 실측한 논문은 (1−p)¹ · 용량 밀도를 치밀 명목으로 쓴 논문은 (1−p)² 로 환산 (p 0.10–0.20 이면 2.47 → 2.00–1.58) · 그리고 σ₀ 펠릿 420 MPa ↔ 복합체 500 MPa ↔ 측정 50 MPa 처럼 누른 압력과 잰 압력을 따로 적는다 | 단계 0 · 단계 7 · 단계 6 (결과 전 대조 항목의 장부 칸) | §3-5 L134–137 · §4-4 L243–245 · §8-2 L391
- [m] kato2018_thick_electrode_assb_cycle_tortuosity | 기준 상태가 값을 정한다: 같은 분말의 냉간 펠릿 3.2 ↔ 소결 8.3 mS/cm 이면 같은 자료가 τ 2.47 ↔ 6.48 — "같은 미세구조 = 같은 τ" 는 σ₀ 의 기준 상태를 정해야 뜻이 생긴다 | 단계 7 (σ₀ 를 순수 SE 의 어느 상태로 둘지 결과 전에 적기) · 단계 4 (순수 SE 침대가 그 기준 상태) | §3-1 L74–80 · §8-2 ① L388–390
- [m] kato2018_thick_electrode_assb_cycle_tortuosity | 실험 값에도 방법 내부 띠가 있다: 같은 셀의 V–t 기울기 경로와 용량 적합 경로가 ≈ 15–25 % 어긋남 → 대조 판정선에 실험 쪽 띠로 미리 넣는다 | 결과 전 대조 항목 (실험 불확도 칸) | §3-7 L158–163 · §8-2 ③ L395
- [m] kato2018_thick_electrode_assb_cycle_tortuosity | 옴 한계의 닫힌 꼴 C(i) = X·(ΔU − R_o·i)/i (X = q·κ_eff) 을 율속 계산의 상한 검산으로 쓴다 — 전제 (좁은 반응 앞면 · 상수 OCV) 가 원 자료에서도 ≈ 0.2–0.4 V 어긋나므로 상한으로만 | 흐름 밖: 율속 전기화학 계산 (STEP4) 의 검산 | §0 L37 · §8-2 ⑥ L398

**ketter2025**
- [m] ketter2025_resistor_network_models_predict_transport_properties | 면 직렬 계면항의 구현 형식: 이종상 면 링크 = (0.5/κ_a + 0.5/κ_b + R_int/dx)⁻¹ — 면적당 저항을 면마다 직렬로 넣는 꼴 · 값 (2 × 10⁻⁶ m²K/W) 은 해상도에 묶인 맞춤값이라 가져오지 않는다 (60³ 에서는 계면 수가 적어 효과가 약함) | 단계 7 · 흐름 밖: 계면 저항 (복셀 수송) | §4-1 L159 · §7-6 L295–299 · §3-6 L151
- [m] ketter2025_resistor_network_models_predict_transport_properties | 수송 솔버의 최소 검증 세트: 직렬 · 병렬 층상 구조의 해석해 재현 + Yuge 1977 수정 EMT (30³ · 무상관 혼합) 재현 + 잔차 기준 (r < 10⁻⁹ · 문턱 근처에서 완화한 경우는 "treated with caution" 표기) | 단계 7 (단위 시험 — U0 류의 수송판) | §4-2 L165–168 · Fig S3 (L207)
- [m] ketter2025_resistor_network_models_predict_transport_properties | 해상도 함정: 거친 망은 조성 추세는 맞지만 퍼콜레이션 문턱 근처에서 자릿수로 틀린다 (σ_e @ φ_NCM 20 %: 60³ 3.3 × 10⁻¹¹ ↔ 300³ 0.00918 ↔ 실측 0.0147 mS/cm) → 문턱 근처 조성은 고해상으로만 판정한다 | 단계 7 · U6 (해상도 수렴을 문턱 근처에서 따로 보기) | §3-6 L142–151 · §8-⑤ L320
- [m] ketter2025_resistor_network_models_predict_transport_properties | 입력 규약 통일: 한 상의 입력이 "펠릿 유효값" (기공 · 접촉 포함) 인지 "치밀 고유값" 인지를 채널마다 같게 둔다 — 섞이면 기공 · 접촉을 이중으로 센다 · 그리고 묶은 값은 복합체 속 상태가 순수상 펠릿과 다르면 틀린다 (문턱 근처 10.7–58 배) | 단계 7 (입력표의 규약 칸) · 단계 4 (순수 SE 침대 = 기준 상태) | §0 L24–25 · §7-4 L287 · §3-2 L89–90

**kim2024**
- [m] kim2024_carbon_volumetric_occupation_se_domain | 첨가제 부피 장부: 질량비를 부피로 바꿀 때 실측 밀도 (탄소 0.67 ↔ SE 1.86 g/cm³ · Archimedes) 를 쓰면 탄소는 같은 질량의 SE 보다 ≈ 2.78 배 부피 — 탄소를 SE 영역을 차지하는 상으로 둔다 | 단계 0 (부피 장부) · 단계 5 · 흐름 밖: 첨가제 표현 | §3 L50–52 · §8-① L151–155
- [m] kim2024_carbon_volumetric_occupation_se_domain | 대조 설계: 같은 시료에서 이온 · 전자 전도를 함께 재면 조성 축에서 반대로 움직인다 (AM 80 → 90 wt%: σ_ion 0.125 → 0.0138 ↔ σ_e 38.6 → 65.2 mS/cm) → 두 채널을 같은 구조에서 동시에 견준다 | 결과 전 대조 항목 (단계 7 · 방향) | §3 L53–54 · §8-③ L161–164
- [m] kim2024_carbon_volumetric_occupation_se_domain | 원인을 가르는 관측량: 표면적으로 정규화한 산화 전류가 구 ≈ 섬유 → 섬유의 이점은 표면 화학이 아니라 SE 와의 접촉 면적 · 부피 점유 → 탄소–SE 접촉 면적을 열화 쪽 관측량으로 둔다 | 흐름 밖: 열화 (탄소 표면의 SE 산화) · 피복 정의 | §3 L61–62 · §10 L201–202
- [m] kim2024_carbon_volumetric_occupation_se_domain | 함정: 계열마다 탄소 함량이 다르고 (펠릿 3 wt% ↔ 건식 1 wt%) SE vol% 는 기공이 아니라 상 부피분율 — 값을 계열 사이로 · 기공률 자리로 옮기지 않는다 | 흐름 밖: 실험과의 대조 | §10 L190–196

**kim2026_a3d**
- [m] kim2026_a3d_air_electrode_microstructure_transport | 결합 절차: 구조에서 얻지 못하는 동역학 값은 문헌 + 한 벌의 실험 방전 곡선에 맞춘 뒤 고정하고, 그다음 구조 변수만 바꾼다 (구조 효과 분리) | 단계 7 · 흐름 밖: 전기화학 결합 | §2.2 L229–231 · §6-(b) L582–583
- [m] kim2026_a3d_air_electrode_microstructure_transport | 영역별 출처 표기: 핵심 영역은 구조에서 계산한 유효 물성 · 보조 영역 (기체 확산층) 은 Bruggeman ε^1.5 — 한 모델 안에서 섞어 쓸 때 어느 칸이 어느 쪽인지 표에 적는다 | 흐름 밖: COMSOL · 1D 모델 인계 | Table S2 L244–252 · L259–262
- [m] kim2026_a3d_air_electrode_microstructure_transport | 관측량: "가장 열린 연속 수송 채널의 지름" (최대 퍼콜레이션 경로 지름) — 단위셀 주기를 줄이면 비표면적은 단조로 늘지만 이 지름과 유효 확산도는 비단조 | 단계 7 (형상 관측량 — 채널 폭) | §3.3 L374–385 · Fig 3c
- [m] kim2026_a3d_air_electrode_microstructure_transport | 함정: 한 변수만 올린 민감도가 비단조일 수 있다 (확산도 1.5 배에서 고율 용량이 오히려 나빠지고 2 배에서 회복) → 변수 하나씩의 스윕에 중간점을 넣고 단조를 가정하지 않는다 · 지금 조건에서 무엇이 율속인지 (여기서는 전도도가 아님 — 곡선이 겹침) 를 먼저 확인한다 | 흐름 밖: 설계 변수 귀속 · 민감도 그림 | §3.2 L338–354

**kim2026_pregranulation**
- [m] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 비교 설계: 공정 (또는 모델) 두 변형을 견줄 때 같은 최종 기공률 조건과 같은 압력 조건을 나눠 적는다 — 기공률이 다르면 (0.305 ↔ 0.333) 수송 개선의 ≈ 45 % 가 기공률만으로 설명된다 (Bruggeman 가정) | 단계 5 · 단계 7 · 결과 전 대조 항목 | §3-4 L130–131 · §8-2 L356–359
- [m] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 대칭셀 식의 단위 함정: τ = R_ion·A·κ·ε/(2d) 의 R 을 Ω 로 넣는지 Ω·cm² 로 넣는지 · 면적을 몇 번 곱하는지 결과 전에 못박는다 (이 논문은 표기 Ω·cm² ↔ 계산 Ω) · tortuosity factor 를 길이 비로 읽지 않는다 (18.6 % ↔ 제곱근으로 −9.7 %) | 단계 7 · 흐름 밖: 대칭셀 이온 측정 | §3-4 L112–129 · §7-3 L318
- [m] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 누른 직후의 AM 균열을 사이클 계산의 초기 조건으로 넘기는 연결이 비어 있다 — 전셀 300 사이클 차이 5.2 %p 가 그 사례 (정량 없음 · 반쪽 셀 값은 Li 음극 몫이 섞임) | 조건 R7 · 흐름 밖: 열화 계산의 초기 조건 | §7-5 L327–328 · §8-3 L361–364
- [m] kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation | 믹싱 실험 설계: "첨가 순서 효과" 와 "투입 에너지 · 시간 효과" 가 섞인다 (과립화 전극 = 기존 공정 + 2000 rpm 10 분) → (a) 같은 총 시간 · 다른 순서 (b) 같은 순서 · 다른 시간으로 나눈다 · 혼합 상태 지표 후보 = 과립 압축 강도 · 분말 BET · 분말 SEM | 흐름 밖: 믹싱 | §7-6 L333–335 · §10-12 L386

**landesfeind2016**
- [m] landesfeind2016_tortuosity_eis_electrodes_separators | σ₀ 불변 검사: 같은 구조를 전도상 전도도 두 값으로 풀어 수송 tortuosity 가 같아야 한다 — 실험판 = τ 가 κ 0.41–12.5 mS/cm 에서 4.03 ± 0.24 (분리막) · 0.46–9.56 mS/cm 에서 4.3 ± 0.6 (흑연 전극). 다르면 σ₀ 에 비례하지 않는 항 (면적당 계면 저항 등) 이 켜져 있거나 식의 σ₀ 가 계산에 쓴 값과 어긋난 것 | 단계 7 (단위 시험) · 흐름 밖: 계면 저항을 켠 수송 계산의 이름 | §4-2 L126 · §4-3 L140–141 · §9 ④ L435 · §11-③ L473
- [m] landesfeind2016_tortuosity_eis_electrodes_separators | 두께 선형성 검사: R·A 가 두께 (장수) 에 선형이고 절편이 ≈ 0 인지 본다 (실험: 절편 0.10 Ω·cm² · R² 0.998 = 한 장 저항의 < 3 %) — 절편 = 경계 · 접촉 기여 · 기울기 = 벌크 | 단계 7 (단위 시험 — 얇은 구조에서 경계 몫 가르기) | §4-2 L124 · §11-④ L475
- [m] landesfeind2016_tortuosity_eis_electrodes_separators | 실험 값의 자격 규칙: 이상 축전기 전송선 맞춤은 R_Ion 을 > 30 % 과대 (40.6 ↔ 31.0 Ω) → 대조 값은 CPE 를 쓴 맞춤 (또는 그래프법) 만 받는다 · 같은 분리막 (Celgard 2500) 의 문헌 N_M 이 8.5 · 13 · 18 ↔ 이 논문 4.5 로 흩어진 원인 (가장자리 우회 전류 · 2 단자 접촉 저항 · 유효 면적) 을 확인한다 | 결과 전 대조 항목 (실험 값의 자격) | §4-3 L133–136 · §5-1 L202 · §5-2 L218–225 · §11-⑤ L476
- [m] landesfeind2016_tortuosity_eis_electrodes_separators | 정의 · 보고: τ = ε·N_M (제곱 없음) 과 제곱근 관례를 섞지 않고, 문헌 비교는 기공률 정의에 덜 휘둘리는 N_M 으로 한다 · 기공률은 질량 수지 (무게 + 두께 + 밀도) 로 내고 두께 오차 (± 2 µm → 20–50 µm 코팅에서 4–10 %) 를 같이 적는다 | 단계 0 (기공률 연산자 · 오차 예산) · 단계 7 (관측량 정의) | §3-3 ⑥ L94 · §4-1 L115 · §4-5 L160 · §8-4 L405–409

## 카드 문제

**철회된 출처를 실험 앵커로 적은 서술 (3 건)**
1. jung2023 L35 — "우리 압밀/전달 앵커(Minnmann 10 %, Bazzoun σ 등)" 라고 적음.
2. kim2024 L146 — 비교표의 우리 쪽 칸에 "DEM 15.6% / MPM 16.7% @300 (Minnmann 10%)".
3. kim2026_a3d L35 · L66 · L541 · L694 — "σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)·#266 이 담당" (값은 안 적었지만 Minnmann 을 순수 SE 냉간 압분의 기공 앵커로 지목).

**우리 쪽 값 · 서술이 카드 안 (또는 배치 안 카드끼리) 에서 어긋남**
4. AM 영률 140 GPa 의 지위 — jung2023 (L171 · L217) · kato2018 (L334) 은 표지 없이 "E 140 GPa" 로 적고, kim2026_pregranulation (L307) 은 같은 값을 "출처 철회 상태 (CL-90)" 로 적음 (배치 안 카드끼리 다름).
5. ketter2025 — 방법 대조표 L277 은 우리 접촉망 · 복셀 솔버의 입력 σ 를 "고체상 고유값" 으로 적는데, 같은 카드 §0 L25 는 "σ_grain 3.0 = 펠릿 lumping 값 — SE 입력 규약이 이미 섞여 있다" 고 적음.
6. ketter2025 L277 · L287 — "VGCF σ = 100 = 분말값 lumping (CL-47)". (카드 밖 근거 — 프로젝트 지침의 10-03 정정은 "분말값" 귀속을 철회했다. 카드는 09-25 작성본의 옛 서술.)
7. kim2024 — SE 를 "LPSCl (Li₆PS₅Cl₀.₅Br₀.₅)" 로 적고 (L33 · 합성에 LiBr L42) 비교표 · 인사이트에서는 "AM·SE 동일" · "우리 소재(NCM811+LPSCl)" 라고 적음 (L138 · L174) — Br 조성 차를 판정에 반영하지 않음.

**카드 안의 숫자 · 서술 모순 · 오기**
8. kim2024 — "+22 %" (L59 · L107 · L165 · L185) ↔ 같은 카드의 0.087 → 0.105 mS/cm 는 +20.7 % (내 검산). 원문 표기인지 카드 산술인지 표지 없음.
9. kim2024 — "carbon ↑ → σ_ionic ↓ 를 실험으로 정량" (L86 · L172) ↔ 같은 카드의 자료는 "탄소 0–3 wt% 에서 σ_ionic 거의 평탄 (Fig S3a · digitized 추세)" (L57 · L113). 1/10 붕괴는 AM 분율 축 (SE 양이 주는 쪽) 의 자료다.
10. kim2024 L143 · L166 — "Lee 2025 … SuperP 0.0168 < VGCF 0.0298 mS/cm σ_e". 같은 카드의 탄소 든 복합체 σ_e (5.08–65.2 mS/cm) 보다 세 자릿수 낮아 단위 (S/cm ↔ mS/cm) 확인이 필요 (이 카드만으로는 판정 불가).
11. kim2024 — SE 부피분율 30.0 → 13.9 vol% 의 산출에 쓴 AM 밀도 · 식이 카드에 없음 (재현 불가).
12. kato2018 — 같은 어긋남 (기울기 경로 ↔ 용량 경로) 을 세 범위로 적음: "≈ 20–25 %" (L23 · L346 · L395 · L410) · "≈ 15–25 %" (L162 · L272 · L426) · "18–28 %" (L162 · 비의 방향이 반대).
13. kato2018 — slug 의 "cycle" ↔ 카드 자신의 판정 "사이클 기반이 아니라 율속 기반" (L24 · L368).
14. kim2026_a3d — 머리 태그 "methods: dft" (L12) ↔ 본문 type "FEM·digital-twin" (L3) · DFT 없음.
15. kim2026_a3d — "A3D 가 foam 의 6 배 이상" (L275 · L286) ↔ 카드 숫자 2.51 × 10⁵ ↔ 0.40 × 10⁴ S/cm 의 비는 62.75 (내 검산). 지수 또는 배수 표기 중 하나가 어긋남.
16. kim2026_a3d — 골격 재료가 Ni (L30 · L77) 인데 Table S1 의 고유 σ_e 는 "(Cu) 6.04 × 10⁵ S/cm" (L280) · Table S3 각주는 "(Ni) 1.42 × 10⁵" (L372). 같은 구조 (기공 45.6 % · SSA 1.02 × 10⁷) 의 유효 σ_e 가 2.51 × 10⁵ (L244 · L275) ↔ 5.92 × 10⁴ S/cm (L369) — 고유값 대비 비는 둘 다 ≈ 0.416 (내 검산) · 카드에 설명 없음.
17. kim2026_a3d L351 — "σ_ion (0.5/1.0/1.5/2.0 × 10⁴ S/cm 범위)". 다른 곳은 10⁻⁴ S/cm (L247 · L370) → 지수 부호 오기로 보임.
18. kim2026_a3d — Table S3 에서 유효 σ_ion ÷ 전해질 전도도와 유효 D_O₂ ÷ 벌크 D_O₂ 의 비가 B600 은 같고 (0.221 · 0.221) B500 · B400 · B300 은 확산 쪽이 ≈ 1.12 배 큼 (내 검산) — 카드에 설명 없음 (원문 값인지 옮김 오류인지 미확인).
19. jung2023 L147 — "Auerbach P_c ∝ K_IC²/E, 경도↑ 보통 K_IC↑" 는 표지 없는 카드 추론 (논문 문장 아님).
20. jung2023 L134 — "PC = 우리 AM_P (보통 더 큰·다결정)" 로 잇지만 이 논문의 PC · SC 는 D50 4.9 / 5.0 µm 로 같은 크기 → 크기 축 대응은 이 논문에서 나오지 않음.
21. ketter2025 — "인용 금지" 표지 값 둘 (L27 의 치밀 쪽 되돌림 값 · L262 의 NCM σ_e 추론). 그런데 L27 값이 만든 폭이 L37 (선택지 D) · L343 (§10-13) 에 표지 없이 다시 나옴.

**카드가 스스로 표지한 원문 불일치 · 미확인 (고치지 않고 위치만)**
22. kato2018 §10-1 L420–432 — 원문 오식 13 항 (Fig 1 패널 표지 뒤바뀜 · 15.7 ↔ 15.8 mAh/cm² · Table S1 각주 a/b 뒤바뀜 · Eq S1 분자 · Eq S4 · R_o 출처 미기재 등).
23. ketter2025 — SI p.S16 문장의 σ_e/σ_ion 뒤바뀜 (L95) · VGCF "<2 wt.%" (본문) ↔ "above 2 wt.%" (SI) (L127) · Source Data 의 "4wt%" 중복 표기 (L339) · 80 % 복합체 κ(T) 계단 하락 (논문 무언급 L113) · 같은 밀도에서 이 논문 0.323 ↔ Böger 0.440 W/m·K (L27 · L343) · Böger 의 0.66 이 무엇인지 미확인 (L365).
24. kim2026_pregranulation §10 L373–397 — 원문 불일치 · 빠진 조건 23 항 (박리 0.91 ↔ 그림 0.191 N/mm · R_ion 단위 · N_M 7.02 ↔ 재계산 7.11 · 전셀 0.2C 유지율 본문 ↔ 그림 · 나노압입 축 단위 · DFT 모형이 NCA 가 아닌 NCM622 등).
25. kim2026_pregranulation — 팔로우 랩 표지의 교신저자 한글 이름 [미확인] (L22) · 받은 SI 가 학술지 게시판과 같은 판인지 [미확인] (L5).
26. landesfeind2016 — 정오표 미열람 (L15 · L489) · Table II 의 Separion 행 내부 불일치 = 카드가 인용 금지 (L210–212) · 판독 값 전체가 "정밀 인용 금지" (L4) · 요약 "전극 ~1.5–3 배" 보다 큰 판독 · 파생값이 있음 (L32 · L323 · L493) · Fig 12 캡션 ↔ 본문의 분리막 장수 · 흑연 ε 0.42 ↔ 0.43 (L496–497) · Eq. 4 의 지수 [미확인] (L69 · L491).
27. landesfeind2016 §8-6 L415–424 — 우리 리포의 표기 상태는 카드가 스스로 "2026-10-02 관찰" 이라고 날짜를 붙인 서술 — 현재 상태는 이 카드로 알 수 없음.
28. kim2026_a3d — 해상도 (0.01 µm/복셀) 를 고른 근거 · 수렴 시험 · 온도가 카드에 없음 (L145–147) · 본문 수치 대부분에 표지 (stated · 판독) 가 붙어 있지 않음 (Fig 3c 의 경로 지름만 "디지타이즈 TREND" L383).
