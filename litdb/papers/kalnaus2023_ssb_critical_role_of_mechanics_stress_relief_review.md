<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-5 · 정독 47) 에서 꼭 뽑으라고 한 항목.
     본 = famprikis2019_fundamentals_inorganic_sse.md (총설 카드 — "전부 소환값 · 원출처 ref 번호를 전부 붙인다" 규율) · 절 번호 체계와 두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 꼴 = mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md (같은 묶음 · 이 총설의 ref 54).
     원문 = Science 출판본 PDF 10 쪽: PDF p.1 = Review Summary (Science 381, 1300 · "1 of 1") · PDF p.2–9 = 본문 "1 of 8" – "8 of 8" (eabg5998) · PDF p.10 = 출판사 안내 쪽 (Editor's summary · 호 6664).
     쪽 표기 = 본문 쪽 p.n/8 (쪽 아래 "n of 8") · PDF 쪽 = n + 1 · 요약 쪽 = "요약 쪽 (PDF p.1)" · 크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     보충 자료 (SI) 없음 (*"All data are available in the main text"*) · 표 0 · 번호 붙은 식 0 · 그림 6 + 요약 쪽 그림 1 · 참고문헌 85.
     값 표지: 이 글은 총설이라 **모든 숫자가 2 차 인용**이다 — [인쇄 · 2 차 · ref N] = 본문에 인쇄된 값과 그 원전 번호 · [판독] = 그림에서 읽은 값 (Fig. 4 = PDF 벡터 경로 · Fig. 2 = 원본 래스터 화소 ·
     재현 = litdb/figures/<slug>/digitized.csv 113 행) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [우리 산술] = 우리 쪽 값 (CLAUDE.md · 정본 카드) 과 견준 계산 ·
     [미확인] = 원문 10 쪽 전수에 없음.
     글자 층 주의: 기호 글꼴이 µ → "m" · σ → "s" 로 추출된다 ("~6 to 10 mm" = 6–10 µm · "1 mm/min" = 1 µm/min · "sf" = σ_f) — 렌더로 확인해 옮겼다 ("2-mm-thick" 은 본문 글꼴 = 실제 mm).
     원문 10 쪽은 글자 층 추출 + 전 쪽 렌더로 전부 읽었다.  시뮬레이션 (DEM · FEM · MPM) · 분말 압밀 · 성형압은 이 글에 없다 — 사이클 (운전) 중 역학의 총설. -->
# 전고체전지에서 역학의 결정적 역할 (Science 총설 · 자체 실험 · 계산 없음 · 숫자는 전부 2 차 인용) — 응력이 생기는 곳 (NMC 2 차 입자 부피 변화 3.3 → 7.8 % · 불균일 Li 석출 · 외부 가압) · 줄이는 길 (영 변형 양극 · 평탄 석출) · 풀리는 길 (Li 소성: 벌크 ≈1 MPa ↔ 76 nm 위스커 244 MPa · 유리의 치밀화 + 전단 · 그것이 안 켜지면 파괴) 의 틀 — ★ 황화물 전해질의 역학 수치는 하나 (K ≈0.2 MPa·m^½ [ref 54 McGrogan]) · 크리프는 한 문단 (Li₂S–P₂S₅ 유리의 상온 압입 크리프 · 이완 [ref 70 Athanasiou · 값 없음]) · "세라믹 전해질은 상온에서 슬립이 켜지지 않고 깨진다" · Li₆PS₅Cl · 분말 압밀 · 성형압 · 입자 계산 (DEM) 은 0 회 · 열린 문제 = 길이 규모 · 마찰 · 접착 · 크리프를 넣은 모델링 — Kalnaus · Dudney · Westover · Herbert · Hackney (Science 381, eabg5998, 2023)

> slug `kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review` · DOI `10.1126/science.abg5998` · type `review (Science Review — 자체 실험 · 계산 없음 · 2 차 인용만: Li metal length-scale / strain-rate dependent plasticity · fracture toughness of ceramic and sulfide SE and cathode oxides · glass densification / shear flow · nanoindentation creep and recovery (Li2S–P2S5 glass · Lipon) · adhesion / friction / stack pressure — DEM · FEM · powder compaction 없음)` · PDF `f2e9af10-5._Solid-state_batteries_The_critical_role_of_mechanics.pdf` · SI 없음 · digested `2026-11-12` · status ✅
>
> **저자**: **Sergiy Kalnaus\*** ¹ · Nancy J. Dudney ² † · Andrew S. Westover ² · Erik Herbert ³ · Steve Hackney ⁴ — Oak Ridge National Laboratory 의 ¹ Computational Sciences and Engineering Division · ² Chemical Sciences Division · ³ Materials Science and Technology Division (Oak Ridge, TN) · ⁴ Department of Materials Science and Engineering, Michigan Technological University (Houghton, MI) · \* 교신 · † Emerita ORNL Corporate Fellow — *Science* **381** (6664) **eabg5998** (22 September 2023) · Review Summary = *Science* 381, 1300 (2023) · Submitted 29 December 2021 · accepted 14 August 2023 · 지원 = US DOE EERE Vehicle Technologies Office 의 Advanced Battery Materials Research Program (S. Thompson, Program Manager) · 계약 DE-AC05-00OR22725 · 이해 상충 없음 · 저자 기여 = S.K. · N.D. · A.W. · E.H. 개념 · 조사 · 초고 (S.K. 그림) · S.H. 개념 · 조사.
> **이웃 카드 (링크만)**: 이 총설이 인용한 논문 가운데 정본 카드가 있는 것 = [`famprikis2019_fundamentals_inorganic_sse`](famprikis2019_fundamentals_inorganic_sse.md) (ref 1) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) (ref 11) · [`mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation`](mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md) (ref 54 — 황화물 K 의 원전).  이 총설을 인용한 카드 (가리킨 카드 셋) = [`alharbi2026_coupled_design_ultrathin_composite_se_review`](alharbi2026_coupled_design_ultrathin_composite_se_review.md) (ref [86]) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) (ref 17) · [`yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal`](yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal.md) (ref 11).  같은 주제의 이웃 = [`papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation`](papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation.md) (Li₆PS₅Cl 압입 크리프 — 이 총설은 인용하지 않는다) · [`song2025_porous_argyrodite_modulus_fracture_toughness`](song2025_porous_argyrodite_modulus_fracture_toughness.md) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) · [`li2026_electrochemomechanical_coupling_asslmb_review`](li2026_electrochemomechanical_coupling_asslmb_review.md) · [`kollenda2024_time_sensitivity_calendered_electrode_springback_storage`](kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md) · [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) · [`fan2026_sulfide_assb_stability_review_ECERD2600097`](fan2026_sulfide_assb_stability_review_ECERD2600097.md).
> **판독 원자료**: `litdb/figures/kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review/digitized.csv` (113 행 — Fig. 4 벡터 경로: 하중 이력 유지 구간 17 · 하중–깊이 26 / Fig. 2 래스터: 곡선 28 · 표지 42) · 그림 크롭 31 장 (그림 7 = 요약 쪽 그림 + Fig. 1–6 (다시 자름 4 · 손 크롭 2 · 도구 그대로 1) · 패널 4 · 근거 문단 20 · 식 0 · 표 0) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 액체 전해질은 전극의 부피 변화를 그냥 받아 주지만 고체 전해질은 그렇지 못하니, 전고체전지의 고장은 *"first and foremost a mechanical failure"* 이고 설계는 **(i) 탄성 변형의 구배를 줄이고 (영 변형 양극 · 평탄한 Li 석출) (ii) 파괴가 아닌 응력 해소 기전 (Li 의 소성 · 유리의 치밀화와 전단 · 전위를 미리 넣은 세라믹) 을 그 길이 규모 · 온도 · 변형률 속도에서 켜는 것** 이라는 틀을 세운 ORNL 그룹의 Science 총설이다 — 자체 실험 · 계산은 없고 숫자는 전부 인용이다.
**우리 묶음의 질문 (황화물 SE 의 소성 · 크리프) 에 대해서는 문장은 있고 값은 없다**: 황화물 전해질에 붙은 역학 수치는 **K ≈0.2 MPa·m^½ 하나** [ref 54], 크리프는 **Li₂S–P₂S₅ 유리의 상온 나노압입에서 크리프와 이완이 보였다는 한 문단** [ref 70 · 값 없음], 소성은 *"ceramic electrolytes do not activate slip systems at room temperature but instead fracture"* 와 "비정질은 국소 치밀화 + 전단 흐름으로 파괴 없이 응력을 낮출 수 있다" 는 정성 문장뿐이다.
**Li₆PS₅Cl (argyrodite) · 분말 압밀 · 성형압 · 기공률 · 입자 계산 (DEM · FEM · MPM) 은 이 글에 한 번도 나오지 않는다** — 초록이 범위를 *"stress and strain that result from normal and extended battery cycling"* 으로 적는다.

| 우리 질문 (이 묶음) | 이 총설이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 황화물 SE 의 탄성 (E · G · ν) | **없다** — "modulus" 는 2 회 모두 E/H 비의 문맥 (Lipon) · 황화물의 E · G · ν 값 0 | 원문 전수 |
| ② ★ 황화물 SE 의 소성 · 경도 · 항복 | **값 없다** ("yield" 3 회 = 전부 Li 금속 · "hardness" 2 회 = E/H).  문장 둘: (a) 결정 세라믹 = *"ceramic electrolytes do not activate slip systems at room temperature but instead fracture"* (b) 비정질 (조성 계열로 *"oxides, sulfides, and a variety of mixed compositions"*) = *"At macroscale, these materials are brittle, yet locally densification and shear flow may allow stress reduction without fracture"* · 좌우하는 물성 = **E/H 와 푸아송비** | [인쇄] p.4/8 · Fig. 3 |
| ③ ★ 황화물 SE 의 크리프 · 시간 의존 | **한 문단 · 황화물 유리 · 값 없음**: *"under high enough stresses, such as those achievable by nanoindentation, viscoelastic deformation and creep were reported in sulfide glassy ionic conductors at room temperature (70). Nanoindentation of Li2S-P2S5 (LPS) demonstrated both creep and relaxation within one load-unload cycle. The latter was attributed to the reversal of viscoelastic strain (70)."* — 조성 (70 : 30 / 75 : 25) · 하중 · 유지 시간 · 크리프 지수는 인쇄되지 않았다.  유리 일반: Maxwell 이완 시간 *"~10^10 s"* | [인쇄 · 2 차 · ref 70] p.5/8 |
| ④ ★ 황화물 SE 의 파괴 | *"Sulfide electrolytes demonstrate even lower resistance to fracture in the range of 0.2 MPa m^1/2 (54). Dense halide materials would also be expected to exhibit similar fracture behavior."* — 재료 (유리 · 조성) · 방법 · 풀림 여부는 적지 않았다 (원전 = 정본 `mcgrogan2017_…`: 70Li₂S–30P₂S₅ 유리 · Vickers 9.8 N · 풀린 시편 0.23 ± 0.04) | [인쇄 · 2 차 · ref 54] p.4/8 |
| ⑤ ★ 압밀 · 성형압 · 기공 | **없다** — powder · compaction · calendering · cold-press · porosity 0 회 ("pores" 는 Li 가 석출하는 전해질 속 빈틈).  제조에 대한 문장은 요약 쪽의 둘뿐: 과제 (iii) *"manufacturing processes to form SSBs with a very thin solid electrolyte and a minimum of inactive components, including binders and structural supports"* · *"In manufacturing, as a minimum requirement, the cathode–electrolyte stacks should possess enough strength to withstand the forces applied by the equipment."* | [인쇄] 요약 쪽 (PDF p.1) |
| ⑥ ★ 스택압 (외부 압력) | 값 없음 · 문장 여섯 곳: 응력의 출처 셋째 = *"externally applied stress to the battery as a typical engineering control"* (p.4/8) · ★ *"The current practice is to negate the effects of cracking in composite cathodes by applying external pressure to the cell. This, however, creates a complex stress state inside the cathode with the possibility of local regions with high shear, which can induce further cracking (75)."* (p.5/8) · 스택압 아래 계면 유지엔 마찰이 중요 (p.6/8 · ref 76) · 모델로 스택압의 역할을 이해하려면 계면 마찰의 정량화가 필요 (p.3/8) · 요약 그림 캡션 *"eliminating the need for tremendous external pressure to keep interfaces intact"* | [인쇄] p.3/8 · 4/8 · 5/8 · 6/8 · 요약 쪽 |
| ⑦ ★ 계면 접촉 · 접착 · 마찰 | *"Adhesion and friction, two of the key variables directly related to maintaining coherent interfaces, are among the most poorly understood."* · *"quantitative measurements of adhesion remain elusive, and crude methods such as the scotch tape pull test are still widely practiced today"* — 값 0 | [인쇄] p.6/8 |
| ⑧ ★ 입자 크기 효과 | SE 입자의 크기 효과 = **없다**.  있는 것: (a) Li 금속의 "작을수록 강하다" (위스커 지름 607 → 76 nm 에 항복 12 → 244 MPa [ref 36]) (b) 양극 입자 *"~6 to 10 µm"* · 결정립은 nm 규모 (p.1/8) (c) 이온 결정은 *"inherently brittle even at very small length scales"* (p.3/8) | [인쇄 · 2 차] p.1/8 · 3/8 |
| ⑨ ★ 모델링 (DEM · FEM · 연속체) | **DEM · discrete element · finite element · phase field = 0 회.**  모델 언급은 Li 금속 쪽: 큰 변형 이론 [ref 41] · Barai–Srinivasan [42, 43] · Verma–Mukherjee [44] · Poiseuille 꼴 석출 모델 [78, 79] · Lipon 치밀화의 MD [64] (*"Simulating restoration of densification, however, is unfeasible owing to unattainable MD methods time scales"*) · 열린 문제 (vii) | [인쇄] p.3/8 · 5/8 · 6/8 · 7/8 |
| ⑩ ★ 그림 · 표 | 그림 6 + 요약 쪽 그림 1 (전부 크롭) · 표 0 · 식 0.  수치가 있는 그림 = Fig. 2 (Li 금속 · 재게재) · Fig. 4 (Lipon 반복 압입 · 재게재 · **벡터라 경로 좌표로 판독**: 유지 10 s 동안 크리프 +4.9–6.9 nm · 절반 하중에서 10 s 동안 −3.1 … −9.6 nm 회복) | §3-4 · §3-7 · §5 |
| ⑪ ★ 저자가 꼽은 열린 문제 | 일곱 (p.7/8) — (i) Li 의 응력 해소 (길이 · 온도 · 속도) (ii) **세라믹 · 유리 · 비정질 세라믹의 응력 해소 (길이 · 온도 · 속도)** (iii) **전해질에 연성 넣기** (iv) Li 음극 설계 (v) 영 변형 · 파괴 저항 · 연성 양극 (vi) **복합 양극 설계** (vii) ***"detailed modeling to help describe the evolution of stress and strain in SSBs that includes length-scale effects, friction, adhesion, and creep"*** | [인쇄] p.7/8 |
| ⑫ ★ DEM 한계 · 소성 계산의 어려움 · 2D / 3D · 탈압 | DEM 한계 = **말 없음**.  소성 계산 = 입자 계산이 없어 해당 문장 없음 — 대신 "모델에 아직 없는 것" 을 (vii) 로 적었다.  2D / 3D = 계산 없음.  탈압 = 분말 · 전지의 탈압은 없고 **압입 제하** 뿐 (황화물 유리의 한 부하–제하 안 이완 [70] · Lipon 의 부분 회복 Fig. 4) | §4-3 |
| ⑬ 절대값 전이 | **0 건** — Li₆PS₅Cl · NCM811 계 압밀 · 탈압에 넣을 숫자가 없다.  전이되는 것은 **틀과 문장** (응력의 출처 셋 · "비탄성 흐름이 안 켜지면 파괴" · 외부 압력의 두 얼굴 · 접착 · 마찰 값의 부재 · 길이 규모와 속도를 같이 적으라는 요구) | §7 · §8 |

⛔ **한정어 (떼지 말 것)**: ① **총설 — 모든 숫자가 2 차 인용** (원전 번호를 같이 적는다 · 우리 값과 같은 칸에 놓지 않는다) ② 범위 = **사이클 (운전) 중 응력** — 제조 · 압밀 · 성형압은 범위 밖 (요약 쪽의 두 문장뿐) ③ 주인공 = **Li 금속 음극과 산화물 (LLZO) · Lipon** — 황화물은 세 곳 (K 한 값 · 비정질 조성 계열의 낱말 · 유리 크리프 한 문단) · **Li₆PS₅Cl 은 0 회** ④ "황화물 K ≈0.2" 의 원전은 **70Li₂S–30P₂S₅ 유리 · Vickers · 풀린 시편** (정본 `mcgrogan2017_…`) — 총설은 "Sulfide electrolytes" 로 일반화했다 ⑤ "황화물 크리프" 는 **유리의 나노압입** (압입 응력 수준) 이지 분말 · 펠릿의 크리프가 아니다 ⑥ Fig. 2 · Fig. 4 의 [판독] 값은 **재게재 그림**에서 읽은 것 (원 논문 = ref 4 · 35 · 36 · 64) — 재료는 Li 금속 · Lipon 박막 ⑦ *"ceramic electrolytes do not activate slip systems at room temperature"* 는 산화물 문맥 (LLZO · TiO₂ 예) 의 일반 문장이다 — 황화물 argyrodite 를 따로 시험한 근거로 쓰지 않는다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-5 의 '왜' 칸)

의도 원문: *"c · l (후보 — 근거 약함) — 세 카드 (alharbi2026 ref [86] · yuan2026 ref 11 · lee2025_heckel ref 17 "고체전지 역학 총설") 가 인용하는 역학 총설 · 카드에는 제목과 "총설" 표기뿐 → SE 의 소성 · 크리프 문장이 있는지 원문 확인"* (가리킨 카드 = alharbi2026 L470 · lee2025_heckel L240 · yuan2026 L59)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "세 카드가 인용하는 역학 총설" | **채움** | 원문 = *Science* 의 **Review** (PDF p.2 머리 "REVIEW · BATTERIES") · 제목 *"Solid-state batteries: The critical role of mechanics"* · 저자 다섯 · 381 (6664) eabg5998 · DOI 10.1126/science.abg5998 · 참고문헌 85 · 자체 자료 없음 (*"All data are available in the main text"*) |
| "카드에는 제목과 '총설' 표기뿐" | **채움 (그대로)** | alharbi2026 L470 = 서지 + *"역학 종합의 표준 문헌"* · lee2025_heckel L240 = 서지 + *"고체전지 역학 총설"* · yuan2026 L59 = 동기 문장의 인용처 — 세 카드 모두 이 총설의 내용 · 값을 옮기지 않았다 (아래 대조 표) |
| "SE 의 **소성** 문장이 있는지" | **일부** — 정성 문장은 있다 · 황화물의 값 (경도 · 항복) 은 없다 | p.3/8 *"ionic compounds are inherently brittle even at very small length scales"* · p.4/8 *"ceramic electrolytes do not activate slip systems at room temperature but instead fracture"* · p.4/8 비정질 (산화물 · 황화물 · 혼합) 의 국소 치밀화 + 전단 흐름 · E/H 와 푸아송비 · Fig. 3 · 대안 = 전위를 미리 넣기 (TiO₂ 10 % 압축 [58] · LLZO [59]) — 측정 조건이 붙은 값은 Lipon 의 E/H ≈23 (↔ 산화물 유리 10–13) 뿐 [2 차 · ref 63, 64] |
| "SE 의 **크리프** 문장이 있는지" | **일부** — 한 문단 · **황화물 유리** · 2 차 인용 · 값 없음 | p.5/8 (§0 표 ③ 의 인용문) — *"sulfide glassy ionic conductors at room temperature (70)"* · *"Li2S-P2S5 (LPS)"* · *"both creep and relaxation within one load-unload cycle"*.  조건 = 상온 · 나노압입 (압입이 내는 높은 응력) · 조성 · 하중 · 유지 시간 · 지수 [미확인].  Lipon 의 부분 회복은 Fig. 4 에 곡선으로 있다 (§3-7 판독) |
| 질문 **c** (항복 · 경도 · 크리프 **값과 정의** · 일축 항복과 견줄 환산) | **없음** (SE) | SE 의 항복 · 경도 · 크리프 값 0 · 경도 → 항복 환산 0.  값이 있는 것은 Li 금속 (유동 응력 ≈1 MPa 이하 · 위스커 항복 12–244 MPa) 과 파괴 인성들 (§3-5) |
| 질문 **l** (입자 계산에 소성을 넣기 어려운 이유 · 우회 · 비용) | **일부 (간접)** — 입자 계산이 없다 | 총설이 직접 적은 것 = "모델이 담아야 할 것" 의 목록: *"length-scale effects, friction, adhesion, and creep"* (p.7/8) · 접착 · 마찰은 *"among the most poorly understood"* · 측정값이 없다 (p.6/8) · MD 는 시간 규모 때문에 치밀화의 회복을 못 본다 (p.5/8).  우회 · 맞춘 값 · 계산 비용 · 검증 = 해당 없음 |

**가리킨 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 것 | 원문 | 판정 |
|---|---|---|---|
| `alharbi2026_…` L470 | *Kalnaus, S. et al., "Solid-state batteries: the critical role of mechanics", Science 381, eabg5998 (2023)* · "역학 종합의 표준 문헌 (우리 카드 둘이 이미 인용)" | 제목 *"Solid-state batteries: The critical role of mechanics"* (The 대문자) · 381 (6664) · eabg5998 · 2023 | **채움** — 서지 같다 (대소문자만) · DOI 는 그 카드에 없음 (원문 = 10.1126/science.abg5998) |
| `lee2025_heckel_…` L240 | *S. Kalnaus, N. J. Dudney, A. S. Westover, E. Herbert and S. Hackney, Science, 2023, 381* · "고체전지 역학 총설" | 저자 다섯 · 순서 같다 · 논문 번호 eabg5998 은 그 줄에 없다 (그 논문 목록의 인쇄 꼴로 보인다) | **채움** |
| `yuan2026_layered_…` L59 | 동기: *"고분자 전해질 (SPE) 은 계면 접촉이 좋지만 영률 · 항복강도가 낮아 … (본문 p.2, Kalnaus 2023 ref 11 인용)"* | 이 총설에 **고분자 전해질의 영률 · 항복강도 문장은 없다** — "polymer" 는 본문에 1 회 (p.2/8 · 불순물 많은 Li 박을 *"polymer electrolytes"* 와 쓸 때 결함이 계면에 모인다 [29–31]) | **없음 (받치는 문장 없음)** — 카드는 Yuan 논문의 인용 표기를 옮긴 것이라 카드 오류는 아니다.  "SPE 는 영률 · 항복강도가 낮다" 의 출처로 이 총설을 쓰지 않는다 |

⇒ **의도 대조 결과: 일부** — "SE 의 소성 · 크리프 **문장**" 은 있다 (p.3/8–5/8 · Fig. 3 · Fig. 4); **황화물의 값 · 정의 · 측정 조건은 없다** (K ≈0.2 [ref 54] 하나 · 크리프는 ref 70 을 가리킬 뿐); Li₆PS₅Cl · 압밀 · 입자 계산은 0 회.  이 총설의 쓸모는 값이 아니라 **틀** (응력의 출처 → 해소 기전 → 안 켜지면 파괴) 과 **원전으로 가는 길** (ref 70 Athanasiou 2022 · ref 75 Yamamoto 2020 · ref 74 Koerver 2017 · ref 12 Kondrakov 2017 — 넷 다 정본 카드 없음 · §12).

---

## 1. 한 줄 요약
전고체전지에서는 전극의 조성 변형 (양극 격자의 팽창 · 수축 · Li 석출) 이 곧 접촉 역학 문제가 되고, 그 응력이 **비탄성 · 점탄성 변형으로 풀리지 못하면 파괴로 풀린다** — 이 한 줄을 Li 금속 (작은 부피에서 벌크의 100 배 넘게 강해져 계면 응력을 못 푼다) · 세라믹 전해질 (전위가 안 생겨 K 가 2 MPa·m^½ 아래) · 비정질 전해질 (국소 치밀화와 전단 · Lipon 의 예) · 복합 양극 (첫 사이클의 계면 균열 · 외부 압력이 만드는 국소 전단) · 계면 (접착 · 마찰은 거의 재지 못했다) 에 차례로 대어 본 글이다.
결론은 일곱 가지 연구 과제이고, 그 마지막이 "길이 규모 효과 · 마찰 · 접착 · 크리프를 넣은 상세 모델링" 이다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **S. Kalnaus\*** · N. J. Dudney · A. S. Westover · E. Herbert · S. Hackney (Oak Ridge National Laboratory · Michigan Technological University) | *Science* 381 (6664) eabg5998 (22 September 2023) · Review Summary = *Science* 381, 1300 | 10.1126/science.abg5998 | 특정 조성 아님 — Li 금속 · 가닛 (LLZO · LLZTO) · Lipon · 황화물 유리 (Li₂S–P₂S₅) · β-Li₃PS₄ (인용 한 곳) · 층상 산화물 양극 (NMC111 · 532 · 811 · LCO) · LiMn₂O₄ · Li₄Ti₅O₁₂ · TiO₂ · 실리카 유리 | 총설 (자체 실험 · 계산 0 · 참고문헌 85) |

- **1저자 메모 (후보 표 N-5) 와의 대조**: 저자 다섯 · 순서 · 학술지 · 권 381 · 논문 번호 eabg5998 · 2023 — **같다**.  덧붙임 ① 제목은 *"The critical role…"* (The 대문자 · 후보 표 · alharbi2026 카드는 소문자 the) ② **DOI = 10.1126/science.abg5998** (후보 표 "DOI 카드에 없음") ③ 호 = **6664** (PDF p.10 *"Science 381 (6664), eabg5998"*) ④ 게재일 22 September 2023 · 접수 2021-12-29 · 수락 2023-08-14 ⑤ 같은 글의 한 쪽짜리 **Review Summary** 가 *Science* 381, **1300** (2023) 으로 따로 쪽 번호를 가진다 (PDF p.1 · "1 of 1").
- **글의 꼴**: 요약 쪽 (BACKGROUND · ADVANCES · OUTLOOK + 그림) → 본문 8 쪽: 서론 → *A mechanics perspective of a battery in operation* → *Minimizing gradients in elastic strain* (*Zero effective strain cathodes* · *Planar plating and stripping of Li metal*) → *Stress-relief mechanisms operating in SSBs* (*Plastic deformation in Li metal* · *Fracture* · *Plastic deformation in ceramics* · *Time-dependent mechanical behavior* · *Electrochemical fatigue* · *Adhesion and friction*) → *Lithium propagation in solid electrolytes* → *Conclusions* → 참고문헌 85 · 감사.
- 저자 그룹 자신의 선행 (이 총설이 기대는 측정): ref 14 · 34 (Herbert 외 — Li 나노압입) · ref 63 (Herbert 외 2011 — Lipon 나노압입) · ref 64 (Kalnaus 외 2021 — Lipon 의 파괴 저항 · Fig. 4 의 출처) · ref 61 · 62 (Dudney 그룹 박막 전지).

---

## 3. 핵심 수치 (★ 전부 쪽 · 원전 번호 병기 — 이 총설의 값은 모두 2 차 인용)

### 3-1. 글의 범위 · 틀 (요약 쪽 · p.1/8–2/8 · `txt_p2_title_authors_abstract.png` · `txt_p1_outlook_challenges_manufacturing.png` · `txt_p3_stress_relief_mechanisms_or_fracture.png`)
- 초록: *"This review will focus on stress and strain that result from normal and extended battery cycling and the associated mechanisms for stress relief, some of which lead to failure of these batteries."*
- 서론: *"The majority of failures in SSBs are first and foremost a mechanical failure."* · *"This article will not be a comprehensive overview (1, 3, 10) of SSB materials but rather will focus on providing a framework by which one can analyze and identify the most critical mechanical properties and gaps in the research"* (p.1/8).
- ★ 길이 규모와 속도: *"We especially want to emphasize the importance of considering the mechanical response to strain in materials as a function of length scale and strain rate. In an SSB cathode, particles are typically ~6 to 10 µm in size with individual grains on the nanometer scale, whereas nonuniform Li deposits can range from nanometers to millimeters in scale."* (p.1/8).
- ★ 틀 (p.2/8): *"The goal is to activate inelastic or viscoelastic strain to reduce the stress magnitude. … When the inelastic flow cannot be activated at a specific length and time scale, the stress relief proceeds through fracture."*
- 설계 요구 둘 (p.2/8): *"(i) minimize or eliminate the sources of elastic strain, in particular, localized gradients in elastic strain, and (ii) engineer materials with efficient stress relief mechanisms (for example, enable localized ductility) capable of operating over a wide range of battery-relevant length scales, temperatures, and strain rates without resorting to stress relief by fracture."* · 방전 · 충전이 뒤집힐 때 계면 접촉이 유지되려면 *"this requirement may necessitate a form of reversible strain"*.
- 요약 쪽의 세 과제: (i) 불균일 Li 석출과 전해질 안 석출 (ii) 사이클 부피 변화에 따른 계면 접촉 상실 (*"at electrode contacts and also at grain boundaries"*) (iii) 얇은 전해질 · 비활성 성분 (바인더 · 지지체) 최소의 제조.  수치 = 에너지 밀도 *"more than double"* · 충전 *"5 min or less"*.

### 3-2. 응력의 출처 — 양극 부피 변화 · Li 석출 속도 · 외부 가압 (p.1/8–2/8 · p.4/8 · `txt_p2_mechanics_perspective_nmc_dilatation.png` · `txt_p3_anode_rates_stress_relief_requirements.png`)
| 값 | 맥락 | 표지 · 쪽 · 원전 |
|---|---|---|
| **3.3 % (NMC111) → 7.8 % (NMC811)** | *"secondary cathode particles dilatation"* — 충전 때 격자 상수 감소 · 방전 때 증가 → 양극–SSE 계면 응력 → 인장 성분이 강도를 넘으면 취성 파괴 (입자 안 · 계면 · 전해질 안) | [인쇄 · 2 차 · ref 12 Kondrakov 2017] p.1/8 |
| 부피 변화의 크기 · 부호 · 비대칭은 조성 · 구조에 달렸다 | 층상 산화물 가정 | [2 차 · ref 11 Koerver 2018] p.1/8 |
| **4C = > 1 µm/min** Li 석출 · **20C = > 5 µm/min** Li 박리 (짧은 펄스) | 전기차 급속 충전 · 펄스 — 작은 부피에 갇힌 Li 가 버티는 압력은 변형률 속도 (전류 밀도) 에 크게 달렸다 [14, 15] | [인쇄] p.2/8 |
| 응력의 출처 셋 | *"(i) Li plating into defects in the solid electrolyte, (ii) stress due to expansion of cathode particles constrained by the solid electrolyte, and (iii) externally applied stress to the battery as a typical engineering control"* | [인쇄] p.4/8 |

- [카드 해석] 3.3 · 7.8 % 는 "2 차 입자" 의 부피 변화로 적혀 있다 — 정본 `li2026_electrochemomechanical_…` 카드 L44 가 같은 원전 (Kondrakov) 으로 옮긴 "단위포 부피 변화 최대 5.1 % (NCM811) · 1.2 % (NCM111)" 와 숫자가 다르다 (입자 수준 ↔ 격자 수준으로 보이나 원전 카드가 없어 확정 못 한다 → §12).

### 3-3. 탄성 변형 구배를 줄이는 길 (p.2/8)
- **영 변형 양극**: Li₄Ti₅O₁₂ (스피넬 · 전압이 낮다) [11] · 리튬화 스피넬 LiCoO₂ 에 Al 소량 도핑 [16] · 부피 변화를 줄인 NMC [17] · 제일원리 설계 변수 셋 (조성 · 이온 배열 · 금속 배위) 과 준 영 변형 무질서 암염 Li₁.₃V₀.₄Nb₀.₃O₂ · Li₁.₂₅V₀.₅₅Nb₀.₂O₁.₉F₀.₁ [18].
- **부호가 반대인 두 양극 섞기**: *"pair cathode active materials with negative strain (LCO) and positive strain (NMC)"* [11] — 단 *"local strain and associated stress may still result in substantial degradation in cathode particles"* (전극 전체 부피는 상쇄해도 입자 국소 변형은 남는다).
- **평탄한 Li 석출 · 박리**: Ag–C 중간층 [22] · Li 와 합금되는 금속 박막 [23, 24] · 젖음 개선 (표면 탄산리튬 제거 [25] · Al₂O₃ 코팅 [24]) — 그래도 *"room-temperature critical currents beyond 1 to 2 mA/cm², high rates still result in cracking and ultimate failure"* · 박리 때 계면 공극 [26–28] · 상용 Li 박의 결함 [29–31].

### 3-4. Li 금속의 소성 — 길이 · 속도 의존 (p.2/8–3/8 · Fig. 2 · `txt_p4_li_metal_flow_stress_size_effect.png` · `txt_p7_conclusions_li_100x_stronger.png`) — 흐름 밖 (음극) · 틀의 근거
| 값 | 맥락 | 표지 · 원전 |
|---|---|---|
| 벌크 Li 유동 응력 **σ_f ∼ 1 MPa 이하** | 넓은 운전 조건 · 높은 상동 온도 (전위 활주 + 크리프) · 상온에서 가공 경화 거의 없음 (속도가 충분히 높지 않으면) | [인쇄 · 2 차 · ref 4, 32, 33] p.3/8 |
| 작은 부피의 Li = **> 200 MPa** | 나노압입 · 미세 / 나노 기둥 | [2 차 · ref 34–36] p.3/8 |
| 위스커 항복 **12 → 244 MPa** (지름 **607 → 76 nm**) | 일축 압축 · 전위 생성 지배 소성 (제안) | [2 차 · ref 36] p.3/8 |
| Li 필라멘트 두께 **~300 nm** (단결정 LLZTO) · 압입 깊이 **< ∼300 nm** 에서 **거의 200 MPa** | 위스커 치수와 맞는다 · 전위 흐름 → 확산 흐름 전환 (Herbert [14]) · 결함 "danger zone" | [2 차 · ref 8 · 14 · 40] p.3/8 |
| *"at small length scales, Li is more than 100 times stronger than in bulk"* | 결론 첫 문단 | [인쇄] p.6/8 |

**Fig. 2 판독** (재게재 그림 · 래스터 xref 3388 · 축 눈금 화소 맞춤 잔차 ≤ 0.009 % · 0.001 MPa / 0.4 nm · 0.16 MPa · `digitized.csv` fig2_left · fig2_right):

| ε̇_true,SS (s⁻¹) | σ_true @ ε 1 % | @ 10 % | @ 20 % | @ 24.5 % (MPa) |
|---|---|---|---|---|
| 2 × 10⁻² (점선 · 맨 위) | 0.98 | 1.23 | 1.39 | 1.45 |
| 3 × 10⁻³ | 0.77 | 0.87 | 0.94 | 0.97 |
| 3 × 10⁻⁴ | 0.55 | 0.59 | 0.62 | 0.63 |
| 4 × 10⁻⁵ (맨 아래) | 0.45 | 0.47 | 0.48 | 0.49 |

- [카드 산술] 양 끝 속도 (500 배) 사이의 속도 민감도 m = Δln σ / Δln ε̇ = **0.12 (ε 1 %) · 0.16 (10 %) · 0.17 (20 %)** → 응력 지수 n = 1/m ≈ 8 · 6.4 · 5.9.  가장 빠른 곡선은 ε 1 → 24.5 % 에 +47 %, 가장 느린 곡선은 +8 % — 본문의 *"no notable capacity for work hardening at room temperature unless the strain rate is sufficiently high"* 와 맞는다.
- 오른쪽 (항복 응력 vs 등가 지름 · 방위 ⟨110⟩ · ⟨112⟩ · ⟨111⟩ · ⟨001⟩ · 표지 42 개 [판독 — 겹친 표지는 하나로 잡혔을 수 있다]): 최고 **≈245 MPa** 는 지름 **≈97 nm** (⟨111⟩) · 최저 **≈13 MPa** 는 **≈573 nm** (⟨112⟩) · 지름이 가장 작은 점 (**≈75 nm**) 은 **≈122 MPa** (⟨110⟩) · 가장 큰 점 (**≈607 nm**) 은 **≈60 MPa** (⟨110⟩).  ⇒ 본문의 *"from 12 to 244 MPa when the diameter decreases from 607 to 76 nm"* 는 **항복 범위와 지름 범위의 끝값을 따로 짝지은 문장**이다 (같은 점이 아니다 · §3-12).
- 모델 (p.3/8 · `txt_p4_li_models_stack_pressure_friction.png`): *"Building on the work of Narayan (41), who uses large deformation theory to model the shear flow of lithium, the incorporation of Nabarro-Herring (volume diffusion), Harper-Dorn (nonconservative dislocation motion), and interface diffusional flow would enable much needed insight … and potentially contribute to our understanding of the role of external pressure (stack pressure). This can be achieved by quantifying interface friction and examining the radial stress distribution and its dependence on the radius of contact between the Li and SSE relative to the thickness of the Li anode."*

### 3-5. ★ 파괴 — 세라믹 · 황화물 · 양극재의 파괴 인성 (p.3/8–4/8 · p.6/8 · `txt_p4_fracture_ionic_crystals_toughness_cap.png` · `txt_p5_sulfide_halide_cathode_fracture_toughness.png`)
| 재료 | K_C (MPa·m^½) | 조건 · 방법 (총설이 적은 만큼) | 원전 번호 · 쪽 |
|---|---|---|---|
| 이온 결정 일반 (예: 입방 스피넬 MgAl₂O₄) | 상한 **~2** | *"even for relatively tough ionic crystals"* · K 는 Pugh 비 · 원자당 부피와 상관 [45] | [2 차 · ref 45] p.3/8 |
| 무기 세라믹 전해질 | *"generally below 2"* | LLTO · LLZO · LATP 문헌 모음 | [2 차 · ref 46–53] p.3/8 |
| LLZO 입계 근처 ↔ 결정립 안 | *"little difference"* | 나노압입 · 잘 치밀화된 시편은 방법과 무관하게 비슷 · 단결정 ≈ 다결정 [49–51] | [2 차 · ref 51] p.3/8 · 6/8 |
| 단결정 Li₆La₃ZrTaO₁₂ | *"as low as 0.6"* | 입내 균열 전파를 설명 [80] | [2 차 · ref 9] p.6/8 |
| ★ **황화물 전해질** | ***"in the range of 0.2"*** | *"even lower resistance to fracture"* — 재료 · 방법 미기재 | [2 차 · **ref 54** McGrogan 2017] p.4/8 |
| 치밀 할라이드 | (값 없음) | *"would also be expected to exhibit similar fracture behavior"* — 추정 문장 | [인쇄] p.4/8 |
| NMC532 "단결정" | **0.3** | *"single-crystal fracture toughness of LiNi0.5Mn0.3Co0.2O2"* | [2 차 · ref 55] p.4/8 |
| NMC532 다결정 응집 입자 | **0.1** | *"polycrystalline agglomerate particles"* | [2 차 · ref 55] p.4/8 |
| 소결 LiCoO₂ 펠릿 | **0.2 – 6.5** · 압입의 2/3 는 **< 1.1** | 나노압입 | [2 차 · ref 56 Qu 2012] p.4/8 |
| LiMn₂O₄ | **0.24** | 미세 기둥 쪼개기 | [2 차 · ref 57] p.4/8 |
| 양극재 전체 어림 | ***"K_C ~ 1"*** | *"Overall, cathode materials are brittle"* — 저자의 어림 문장 (바로 앞의 개별 값은 0.1–0.3 · LCO 2/3 가 1.1 아래) | [인쇄] p.4/8 |

- 왜 취성인가 (p.3/8): *"in ionic crystals (i.e., cathode materials and ceramic electrolytes), dislocation nucleation must overcome a large energy penalty, and therefore ionic compounds are inherently brittle even at very small length scales despite their much higher cohesive energy relative to metals."*
- 결론 문장 (p.4/8): *"This underscores the need for the development of materials that do not produce hard contacts and that can relieve the stress buildup by means other than fracturing."*

### 3-6. ★ 세라믹의 소성 · 비정질의 치밀화 + 전단 · E/H (p.4/8 · Fig. 3 · `txt_p5_plastic_deformation_in_ceramics.png` · `txt_p5_amorphous_densification_shear_flow_lipon.png` · `txt_p5_lipon_e_over_h_time_dependent_behavior.png`)
- 목표: *"A combination of battery materials that can reversibly deform in a SSB and limit the stress without creating fractures is the goal for SSB engineering."*
- ★ 결정 세라믹: *"While limiting the stress buildup by either diffusional flow or via dislocation glide is a suitable mechanism for metallic Li, ceramic electrolytes do not activate slip systems at room temperature but instead fracture."*
- 대안 = 공정 단계에서 결정 결함을 일부러 넣는다 — 전위를 새로 만드는 것이 아니라 **있는 전위를 움직여** 인성을 얻는다 (균열 끝 근처 작은 부피에 전위가 충분히 있을 확률) · 방법 = flash sintering · aerosol deposition · 사례 = flash sintering 한 TiO₂ 가 *"deform up to 10% in compression without fracture"* (슬립 띠 관찰) [58] · LLZO 에서 전위 도입 · 연성 개선 가능성 [59].
- ★ 비정질 · 유리 (p.4/8): 비정질은 결정 구조 쪽으로, 유리는 액체 구조 쪽으로 이완한다 [60] · 비정질은 스퍼터 · 플라스마 응축 · **고에너지 밀링** 등 초급랭으로 만든다 · 조성 계열 *"oxides, sulfides, and a variety of mixed compositions"* · *"At macroscale, these materials are brittle, yet locally densification and shear flow may allow stress reduction without fracture (Fig. 3). This is believed to be critical to the Li interface behavior. These processes manifest differently depending on the composition and mechanical properties, of which modulus to hardness ratio, E/H, and Poisson's ratio seem to have the most influence."*
- Lipon (비정질 박막 전해질 [61]): **10,000 회 넘게 사이클 · 용량 유지 95 % · Li 침투 없음** · 전류 밀도 **10 mA/cm²** 까지 [62] · 역학 연구는 드물다 [63, 64] · ★ **E/H ≈23** (나노압입) ↔ 전형적 산화물 유리 **E/H = 10 – 13** → *"indicating some degree of ductility in Lipon"* · 치밀화하고 전단 변형해 응력 확대를 줄인다 [64].  [인쇄 · 2 차 · ref 61–64]

### 3-7. ★ 시간 의존 거동 — 유리 치밀화의 되돌아옴 · 황화물 유리의 크리프 · Lipon 반복 압입 (p.4/8–5/8 · Fig. 4 · `txt_p6_sulfide_glass_creep_relaxation_recovery.png`)
- 유리 · 비정질의 응력 해소 = 비탄성 변형이 **등적 전단 (isochoric shear) 과 치밀화 (densification)** 로 나뉜다 — "정상" 유리 ↔ "변칙 (anomalous)" 유리의 분류 근거 [65, 66] · ★ *"stress-induced densification in glass can be partially recoverable, unlike permanent plastic shear flow"* · 회복은 유리 전이 온도 아래의 풀림으로 [67, 68] · 실리카 유리 = 치밀화만으로 변형하는 변칙 유리 · 밀도가 낮을수록 취성 [66] · 실리카의 치밀화 에너지 ≈ 회복의 활성화 에너지 **~50 kJ/mol** [69].
- 유리 전이 온도 아래의 유리 = "frozen liquid" · Maxwell 이완 시간 ***"~10^10 s"*** — ★ 그런데 *"under high enough stresses, such as those achievable by nanoindentation, viscoelastic deformation and creep were reported in sulfide glassy ionic conductors at room temperature (70). Nanoindentation of Li2S-P2S5 (LPS) demonstrated both creep and relaxation within one load-unload cycle. The latter was attributed to the reversal of viscoelastic strain (70)."* [인쇄 · 2 차 · ref 70]
- Lipon: *"partial recovery similar to that in LPS glass has been observed at room temperature in Lipon (63, 64)"* · MD 는 치밀화가 P–O–P 결합각 변화로 일어난다고 시사 [64] · *"Simulating restoration of densification, however, is unfeasible owing to unattainable MD methods time scales."* · *"An ability to recover the densified volume at least partially, without requiring external energy input, warrants further investigation. Under cyclic loading, such partial recovery creates a hysteresis-like cyclic behavior (Fig. 4)."*

**Fig. 4 판독** (Lipon 반복 나노압입 · ref 64 재게재 · 그림 전체가 벡터 → PDF 경로 좌표를 눈금 선으로 축 환산 · 맞춤 잔차 ≤ 0.07 s · 0.11 nm · 0.004 mN · 하중 이력 1,014 점 · 하중–깊이 19,224 점 · 유지 구간의 처음 · 끝 30 점 중앙값 · 흔적 잡음 sd 0.3–0.8 nm · `digitized.csv` fig4_left · fig4_right).  하중 이력 = 0 하중 22 s → 봉우리 9 개 (0.98 · 1.52 · 2.18 · 2.94 · 3.84 · 4.84 · 5.94 · 7.18 · 8.54 mN) · 매번 봉우리의 **0.50–0.53 배**로 제하 · 유지 **10.1–10.3 s** (봉우리 · 골 모두) · 램프 1.6–2.0 s.

| 회 | 봉우리 하중 (mN) | 봉우리 유지 중 깊이 변화 (nm) | 유지 끝 깊이 (nm) | 골 하중 (mN) | 제하 중 즉시 변화 (nm) | 골 유지 중 변화 (nm) | 골 유지 끝 깊이 (nm) |
|---|---|---|---|---|---|---|---|
| 1 | 1.00 | +5.8 | 97.9 | 0.50 | −11.6 | −3.1 | 83.2 |
| 2 | 1.53 | +5.6 | 118.9 | 0.77 | −15.0 | −4.5 | 99.4 |
| 3 | 2.19 | +6.9 | 138.0 | 1.10 | −18.9 | −5.3 | 113.8 |
| 4 | 2.96 | +6.3 | 154.8 | 1.48 | −22.1 | −6.6 | 126.1 |
| 5 | 3.84 | +5.6 | 169.0 | 1.92 | −25.4 | −7.5 | 136.1 |
| 6 | 4.84 | +5.6 | 181.7 | 2.42 | −29.0 | −8.1 | 144.6 |
| 7 | 5.95 | +5.6 | 192.1 | 2.98 | −31.7 | −9.1 | 151.3 |
| 8 | 7.19 | +5.1 | 201.2 | 3.59 | −34.8 | −9.6 | 156.8 |
| 9 | 8.53 | +4.9 | 209.3 | (끝점 4.32 mN · 172.0 nm — 제하 도중에 흔적이 끝난다) | — | — | — |

- [카드 산술] ① 봉우리 유지 ≈10 s 의 크리프 = 깊이의 **6.3 % (1 회) → 2.4 % (9 회)** ② 절반 하중으로 뺀 뒤 유지 ≈10 s 동안 **더 되돌아오는 양 = 제하 중 즉시 변화의 0.27–0.30 배** (아홉 회 가운데 여덟 회에서 거의 일정) ③ 그 회복 ÷ 직전 크리프 = 0.54 (1 회) → 1.89 (8 회) ④ 절반 하중 + 10 s 뒤 깊이 감소 ÷ 봉우리 끝 깊이 = **15.0 % → 22.1 %**.
- [카드 해석] 봉우리에서는 깊이가 늘고 (+) 골에서는 줄어 (−) 부호가 번갈아 바뀌므로 한 방향의 열 표류만으로는 이 꼴이 나오지 않는다 — 다만 표류 보정 · 압자 꼴 · 막 두께 · 기판은 이 총설에 없다 [미확인 · 원전 = ref 64].  **재료는 Lipon 박막** (황화물 · Li₆PS₅Cl 아님).

### 3-8. 전기화학 피로 · 복합 양극의 균열 · 외부 압력 (p.5/8 · Fig. 5 · `txt_p6_electrochemical_fatigue_cathode_damage.png` · `txt_p6_first_cycle_cracking_external_pressure_shear.png`)
- 양극의 비가역 손상 = 두 길이 · 시간 규모: *"(i) intergranular fracture in polycrystalline cathode particles, and (ii) lithiation-induced dislocation dynamics and transgranular fracture in single cathode particles"* — (i) 은 액체 전해질 전지에서 잘 기록됐고 [71] (ii) 는 덜 이해됐고 층상 산화물에서 피할 수 없어 보인다 [72, 73].
- 계면: 입자의 치수 변화는 SE–양극 계면 균열을 전파시키기에 충분 · 전해질 안에도 균열 (계면 균열의 연장 또는 새 파면) · ★ *"Available experimental evidence suggests that the majority of such interfacial fracturing occurs within the first cycle and is responsible for the initial capacity loss (74)."* · 그 뒤의 성장이 피로 균열 성장 꼴인지는 *"at present, there is insufficient experimental information to support or reject this hypothesis with confidence"* · NMC811/β-Li₃PS₄ 양극의 계속되는 용량 손실은 균열 손상의 점진적 누적을 시사 [74].
- ★ 외부 압력: *"The current practice is to negate the effects of cracking in composite cathodes by applying external pressure to the cell. This, however, creates a complex stress state inside the cathode with the possibility of local regions with high shear, which can induce further cracking (75)."* [인쇄 · 2 차 · ref 75 Yamamoto 2020] — 압력 값 · 전단 크기는 없다.

### 3-9. ★ 접착 · 마찰 (p.5/8–6/8 · `txt_p7_adhesion_friction_stack_pressure.png`)
- *"The adhesion or wetting of Li metal to the solid electrolyte, as well as the adhesion of the cathode active material to the solid electrolyte, are key for robust cyclic performance of an SSB."* · 외부 압축 스택압의 효용은 입증됐다.
- ★ *"Adhesion and friction, two of the key variables directly related to maintaining coherent interfaces, are among the most poorly understood. The knowledge gap is primarily due to the experimental challenges associated with measuring adhesion and quantifying the effects of friction."* — 측정법 (bulge · scratch · 나노압입) 은 미세 전자 · 박막 산업에서 쓰여 왔지만 *"quantitative measurements of adhesion remain elusive, and crude methods such as the scotch tape pull test are still widely practiced today"* · SSB 에서는 길이 규모 효과와 운전 조건 (온도 · 변형률 속도) 이 더 어렵게 한다.
- 마찰: *"Friction effects become important to maintaining coherent interfaces in the context of stack pressure."* — Li–SSE 계면에서 Li 의 바깥쪽 방사 흐름은 불균일한 계면 전단 응력에 막히고, 그것은 마찰 계수 · 스택압 · Li 의 상대 두께 (사이클 중 변한다) · 마찰 조건에 달렸다 [76].  값 0.

### 3-10. Li 의 전해질 침투 (p.6/8 · Fig. 6) — 흐름 밖 (음극)
- 입계를 따라 [7] · 단결정을 뚫고 (단결정 Li₆La₃ZrTaO₁₂ 가닛 [9]) · **10 mA/cm² 에서 37 s 만에 단락 (2 mm 두께 LLZO 단결정)** [9].
- Na β-알루미나 선례 [77, 78] · Poiseuille 꼴 모델 [78, 79]: Li 로 찬 결함 = 길고 가는 바늘 → 끝의 응력 상태가 정수압이라 전위 활주가 안 되고 확산 거리도 너무 길다 → 압력은 전위 생성 임계 · SSE 파괴 · 또는 국소 전위 변화로 석출이 멈출 때까지 [79] 오른다.
- 세 꼴 (Fig. 6): Mode I (표면 결함에서 · 결정성 무관 [8, 78]) · Mode II (전해질 안 빈틈에 석출 [80, 82, 83] — 입계의 띠 간격 감소 = 전자 전도 [84]) · 입계를 따른 균일 석출 (높은 누설 전류일 때).  균열은 Li 석출보다 훨씬 빨라 Li 없는 관통 균열도 관찰 [81].
- 온도: 195 °C 의 용융 Li 는 임계 전류 밀도가 한 자릿수 오른다 [85] — 용융 Li 는 전해질 파괴에 필요한 응력을 버티지 못하기 때문.

### 3-11. ★ 저자가 꼽은 열린 문제 (p.7/8 · `txt_p8_conclusions_framework_open_problems.png`)
틀 셋: *"(i) identifying and understanding the sources of localized strain; (ii) understanding the stresses generated by this strain in particular at the battery interfaces and how the battery materials respond to such stresses; and (iii) designing battery materials and battery cells with the needed stress and strain evolution."*
과제 일곱 (원문 그대로): *"(i) stress relief mechanisms in Li metal as a function of length scale, temperature, and strain rate (current density); (ii) stress relief mechanisms in ceramics, glasses, and amorphous ceramics as a function of length scale, temperature, and strain rate; (iii) engineering ductility into ceramic and/or glassy electrolytes; (iv) designing Li metal anodes that can either eliminate inhomogeneous plating and stripping of Li metal or that can relieve stresses at the Li–electrolyte interface; (v) engineering cathode active materials that either exhibit zero strain on cycling, are resistant to fracture, or have some measure of ductility; (vi) designing composite cathodes to minimize strain and maximize stress relief; and (vii) detailed modeling to help describe the evolution of stress and strain in SSBs that includes length-scale effects, friction, adhesion, and creep."*
- 본문 곳곳의 "모른다" 문장: 계면 균열의 피로 성장 여부 (p.5/8) · 접착 · 마찰의 정량값 (p.6/8) · 비정질 · 유리 전해질의 변형 · 파괴 연구 자체가 *"rather limited"* (p.5/8) · 양극재의 미세 · 나노 역학 문헌이 *"scarce"* (p.4/8) · 치밀화 회복의 모사 불가 (p.5/8).

### 3-12. 원문 안 어긋남 · 표기 (카드가 본 것)
1. **위스커 문장 ↔ Fig. 2**: *"increases from 12 to 244 MPa when the diameter decreases from 607 to 76 nm (36)"* — 그림에서 607 nm 점은 ≈60 MPa · 76 nm 점은 ≈122 MPa 이고 244 MPa 는 ≈97 nm · 12 MPa 는 ≈573 nm 점이다 [판독] → 두 범위의 끝값을 따로 짝지은 문장 (경향 자체는 그림과 같다).
2. **Fig. 5 캡션의 인용 순서**: *"Images, clockwise from top right, are from (71, 73–75)"* → 문자 그대로면 Interface Cracking = (71) · Transgranular = (73) · Intergranular = (74) · SE Cracking = (75).  그런데 본문은 (71) 을 *"intergranular fracture in polycrystalline cathode particles"* (액체 전지) 의 근거로, (74) 를 계면 균열 · 첫 사이클 용량 손실의 근거로 쓴다 → 캡션 순서와 본문 쓰임이 (71) · (74) 에서 엇갈려 보인다 [카드 해석 · 원전 그림 미확인].
3. **부호 표기**: *"negative strain (LCO) and positive strain (NMC)"* (p.2/8) ↔ 같은 쪽 앞 문장은 충전 때 격자가 줄어든다고 적는다 — 방전 (리튬 삽입) 방향 기준으로 읽어야 정본 `koerver2018_…` 카드 (충전 때 NCM 수축 · LCO 팽창) 와 맞는다 [카드 해석].
4. **NMC532 K 의 라벨** — 원문 (p.4/8): *"The single-crystal fracture toughness of LiNi0.5Mn0.3Co0.2O2 was reported as 0.3 MPa m1/2 and that of polycrystalline agglomerate particles was measured as 0.1 MPa m1/2 (55)"* ↔ 정본 `xu2017_…` 카드 (같은 Purdue 그룹 · Xu 2017 JES) 의 **소결 펠릿 0.309 ± 0.04 · 2 차 입자 계면 0.102 ± 0.03** 과 같은 수 짝이다 — 그 카드에서 0.3 은 "단결정" 이 아니라 결정립 ≈10 µm 의 소결 펠릿 값이다.  ref 55 (de Vasconcelos 2019 Exp. Mech. · 카드 없음 · 후보 표 N-24 = 대기) 원문을 보기 전에는 "단결정" 표기를 옮기지 않는다 [원전 확인 필요].  ⚠ 같은 그룹의 **2016** 논문 카드 `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` (N-23 · Extreme Mech. Lett. 9, 495) 는 정본에 있지만 **다른 논문** 이고 E · H (격자 압입) 만 잰다 — 이 K 0.3 · 0.1 의 출처로 쓰지 않는다.
5. **"K_C ~ 1"** 어림 ↔ 바로 앞의 개별 값 (0.1 · 0.24 · 0.3 · LCO 의 2/3 가 < 1.1) — 어림이 개별 값들의 위쪽 끝이다.
6. 본문은 *"Verma and Mukherjee (44)"* 라 부르지만 ref 44 의 제1 저자는 B. S. Vishnugopi (목록: *"B. S. Vishnugopi, A. Verma, P. P. Mukherjee"*) · ref 7 은 *"E. J. Cheng, Sharafi, J. Sakamoto"* 로 인쇄 (둘째 저자 이름 머리글자 없음) · ref 22 는 *"L.-G. Lee et al."* 로 인쇄 — 서지를 옮길 때는 원 논문에서 다시 확인한다.
7. 조판: *"attemptto"* (요약 쪽) · *"mechanicsof"* (p.4/8) · *"far too long to for efficient transport"* (p.6/8).
8. 황화물 유리의 조성 · Lipon 압입의 압자 · 막 두께는 어디에도 없다 [미확인].

---

## 4. ★ 방법 — 글의 성격 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 글의 성격
- 총설 — 자체 측정 · 계산 0.  *"Data and materials availability: All data are available in the main text."*  그림 가운데 자료 그림은 둘 (Fig. 2 · Fig. 4) 이고 둘 다 **재게재** (Fig. 2 = ref 4 · 35 · 36 / Fig. 4 = ref 64 — 저자 그룹 자신의 Lipon 측정) · Fig. 5 는 네 논문의 사진 (71, 73–75) 을 모은 것 · Fig. 1 · 3 · 6 과 요약 쪽 그림은 모식도.
- 맞춘 값 · 검증 · 계산 비용 = 해당 없음.  인용 85 편 가운데 정본 카드가 있는 것은 셋 (ref 1 · 11 · 54).
- 이 카드가 한 일: 본문 전수 정독 · 인쇄 수치와 원전 번호의 대응표 · Fig. 4 벡터 판독 · Fig. 2 래스터 판독 · 정본 카드 값과의 대조 (§7-2).

### 4-2. 입자 처리
- **없다** — 입자 · 분말 · 접촉망 · 충전 구조를 다루지 않는다.  "particle" 은 본문 10 회 전부 **양극 활물질 입자** (크기 6–10 µm · 2 차 입자 부피 변화 · 입자 안 균열) 이고 SE 입자라는 말은 없다 (SE 는 연속 고체 · 결정립 · 입계 · 박막으로 다뤄진다).
- 우리 대응: DEM = 구 + hooke/hysteresis 접촉 (형상 불변 · SE 파괴 없음 · 연화 E_eff 1.35 GPa) · MPM = J2 연속체 (형상 소성 · 등적 · 속도 무관 · 취성 파괴 없음) — 이 총설의 두 축 (**파괴** 와 **시간 의존**) 은 우리 두 모델 어디에도 없다.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말 없음.**  DEM · discrete element · finite element · continuum · phase field 낱말 0 회.  가장 가까운 문장은 접촉에 대한 재료 쪽 요구 하나: *"the need for the development of materials that do not produce hard contacts and that can relieve the stress buildup by means other than fracturing"* (p.4/8) 과 모델링 과제 (vii) (p.7/8).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 입자 계산이 없어 직접 문장은 없다.  있는 것 셋: (a) Li 금속의 큰 변형 모델 [41] 에 확산 크리프 (Nabarro–Herring · Harper–Dorn · 계면 확산 흐름) 와 **계면 마찰** 을 더해야 한다 (p.3/8) (b) 치밀화 회복은 MD 시간 규모로 못 본다 (p.5/8) (c) 모델에 넣어야 할 넷 = 길이 규모 효과 · 마찰 · 접착 · 크리프 (p.7/8) — 그런데 접착 · 마찰은 측정값이 없다고 같은 글이 적는다 (p.6/8).  우회 (연화 영률 · 항복 캡 · 입자별 FE · MPM) · 맞춘 값 수 · 비용 = 해당 없음.
3. **2D 인가 3D 인가** — 계산이 없다.  2D → 3D 전이에 대한 말 없음.
4. **압력을 뺄 때의 거동** — 분말 · 펠릿 · 전지의 탈압은 다루지 않았다.  있는 것은 **압입 제하**: 황화물 유리가 한 번의 부하–제하 안에서 이완 (점탄성 변형의 되돌아옴) 을 보였다는 문장 [70] 과 Lipon 의 부분 회복 곡선 (Fig. 4 · §3-7 판독 = 절반 하중에서 10 s 동안 즉시 회복의 0.27–0.30 배만큼 더 회복).  설계 요구로서 *"reversible strain"* (p.2/8) · *"reversibly deform"* (p.4/8).

### 4-4. 기법 미니 용어집
- **상동 온도 (T_H)**: 절대 온도 ÷ 녹는점 (절대) — Li 는 상온에서 이 값이 높아 계속 풀림이 일어나고 크리프가 같이 돈다 (원문은 값을 인쇄하지 않았다).
- **유동 응력 (flow stress)**: 소성 흐름이 이어지는 동안의 응력 (Fig. 2 왼쪽 세로축 σ_true).
- **크기 효과 ("smaller is stronger")**: 시편 · 응력 부피가 작아지면 흐름을 켤 전위가 그 안에 있을 확률이 줄어 강도가 오른다 (압축 · 굽힘 [37] · 인장 [38] · 비틀림 [39]).
- **danger zone**: 응력 부피가 확산 흐름에는 너무 크고 (확산 거리 김) 전위 흐름에는 너무 작은 결함 크기 구간 — 국소 응력이 최대가 된다 [14].
- **파괴 인성 K_C**: 있는 균열을 전파시키는 임계 응력의 함수 (MPa·m^½) — 이 총설은 방법별 값 (압입 균열 · 미세 기둥 쪼개기 · pop-in) 을 구분 없이 나란히 적는다.
- **E/H (탄성률 ÷ 경도)**: 유리 · 비정질이 압입 아래에서 치밀화 · 전단으로 흐르는 정도를 가르는 지수로 쓰였다 (Lipon ≈23 ↔ 산화물 유리 10–13).
- **등적 전단 (isochoric shear) ↔ 치밀화 (densification)**: 유리의 비탄성 변형 두 몫 — 전단 흐름은 부피가 안 변하고 영구적 · 치밀화는 부피가 줄고 일부 되돌아온다.  "정상" 유리는 전단, "변칙" 유리 (실리카) 는 치밀화가 지배.
- **Maxwell 이완 시간**: 점탄성 재료가 응력을 푸는 특성 시간 (점도 ÷ 탄성률) — 유리 전이 온도 아래 유리는 ~10¹⁰ s.
- **Lipon**: lithium phosphorus oxynitride — 스퍼터 증착 비정질 박막 전해질.
- **Mode I / Mode II (이 글의 용법)**: Li 침투 꼴 — I = 표면 결함에서 안쪽으로 · II = 전해질 안에서 먼저 석출 (파괴역학의 하중 모드 I · II 와 다른 뜻).
- **전기화학 피로**: 리튬의 삽입 · 탈리 반복이 구조재의 반복 하중처럼 손상을 쌓는 것.

---

## 5. Figure set ★
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| 요약 쪽 그림 (`fig_summary.png` · 손 크롭) | 응용 (항공기 · 드론 · 자동차) → 전지 → 세 과제 패널 (Control of Li Metal · Cathode Engineering · Electrolyte Microstructure) · 캡션 *"eliminating the need for tremendous external pressure to keep interfaces intact"* | "큰 외부 압력 없이 계면 유지" 라는 분야 목표의 인용처 (스택압 논의 서두) |
| Fig. 1 (`fig_1.png` · 손 크롭 — 캡션이 옆에 있어 도구가 놓침) | Li 금속 SSB 모식 (LITHIUM / SE + CATHODE 구들) · 검은 칸 = 역학 · 흰 칸 = 수송.  **양극 쪽**: Fatigue · Fracture · Stress Relaxation / Concentration Gradients · Loss of contact · Poor transport.  **Li 쪽**: Fracture · Stress Relaxation · **Plasticity · Creep** / 'Dendrites' · Voids · Non-uniform current | ★ 이 총설의 지도에서 **Plasticity · Creep 은 Li 쪽 칸에만** 있다 — 양극 복합체 쪽은 피로 · 파괴 · 응력 이완 (우리가 SE 의 소성으로 모사하는 영역을 이 총설은 소성 칸에 두지 않았다) |
| Fig. 2 (`fig_2.png` · 다시 자름) · 패널 (`fig_2_left_li_bulk.png` · `fig_2_right_li_micro_nano.png`) | Li 금속: (왼쪽) 벌크 리본 인장 — DIC 변형률 지도 (ε_true 0–25 %) · σ_true–ε_true 네 속도 [ref 4] (오른쪽) 미세 기둥 · 위스커 사진 + 항복 응력 vs 등가 지름 (방위 넷) [ref 35, 36] | 길이 · 속도 의존의 대표 그림 (우리 재료 아님) — 판독 §3-4 (속도 민감도 m 0.12–0.17 · 본문 문장과 그림의 짝 어긋남) |
| Fig. 3 (`fig_3.png` · 다시 자름) | 압입 아래 균열 (위) ↔ 비정질 / 유리: Densification · Shear ↔ 결정 세라믹: Dislocation toughening | ★ 보고서 그림 후보 — "SE 가 응력을 푸는 세 길 (치밀화 · 전단 · 전위) 과 실패 (균열)" · 우리 MPM J2 = 이 가운데 **Shear 한 칸** |
| Fig. 4 (`fig_4.png` · 다시 자름) · 패널 (`fig_4_left_load_profile.png` · `fig_4_right_load_depth.png`) | Lipon 반복 나노압입 [ref 64]: 하중 이력 (봉우리 9 · 절반 제하 · 유지 ≈10 s) · 하중–깊이 (이력 고리) | ★ **U3 (눌렀다 떼기) · 단계 6 의 실험 쪽 '모양'** — 유지 중 크리프 + 절반 하중에서의 시간 의존 회복 (§3-7 표 · 재료 = Lipon) |
| Fig. 5 (`fig_5.png` · 다시 자름) | 복합 양극의 피로 손상 네 꼴: SE Cracking · Interface Cracking · Transgranular Cracking · Intergranular Cracking (가운데 = SE 상자 속 NMC 2 차 입자) [ref 71, 73–75] | 단계 7 · 사이클 원장의 손상 분류 넷 (우리 원장 = 계면 debond + AM 내부 void · **SE 균열 칸은 없다**) |
| Fig. 6 (`fig_6.png` · 도구 그대로) | Li 침투 세 꼴: Mode I (표면 결함) · Mode II (전해질 안 석출) · GB Plating | 흐름 밖 (음극 · 분리막) |
| 근거 문단 20 장 (`txt_p1_outlook_challenges_manufacturing.png` · `txt_p2_title_authors_abstract.png` · `txt_p2_mechanics_perspective_nmc_dilatation.png` · `txt_p3_anode_rates_stress_relief_requirements.png` · `txt_p3_stress_relief_mechanisms_or_fracture.png` · `txt_p4_li_metal_flow_stress_size_effect.png` · `txt_p4_li_models_stack_pressure_friction.png` · `txt_p4_fracture_ionic_crystals_toughness_cap.png` · `txt_p5_sulfide_halide_cathode_fracture_toughness.png` · `txt_p5_plastic_deformation_in_ceramics.png` · `txt_p5_amorphous_densification_shear_flow_lipon.png` · `txt_p5_lipon_e_over_h_time_dependent_behavior.png` · `txt_p6_sulfide_glass_creep_relaxation_recovery.png` · `txt_p6_electrochemical_fatigue_cathode_damage.png` · `txt_p6_first_cycle_cracking_external_pressure_shear.png` · `txt_p7_adhesion_friction_stack_pressure.png` · `txt_p7_conclusions_li_100x_stronger.png` · `txt_p8_conclusions_framework_open_problems.png` · `txt_p9_refs_54_57_sulfide_cathode_toughness_sources.png` · `txt_p9_refs_70_76_creep_cracking_pressure_sources.png`) | 요약 쪽 OUTLOOK (제조 문장) · 제목 · 초록 (범위) · 양극 부피 변화 · 석출 속도와 설계 요구 · 응력 해소의 틀 · Li 유동 응력 · 모델과 스택압 · 파괴 (이온 결정) · ★ 황화물 · 양극재 K · ★ 세라믹의 소성 · ★ 비정질의 치밀화 + 전단 · ★ E/H 와 시간 의존 · ★★ 황화물 유리 크리프 · 전기화학 피로 · ★ 첫 사이클 균열과 외부 압력 · ★ 접착 · 마찰 · 결론 · ★★ 열린 문제 일곱 · 참고문헌 54–57 · 70–76 | 인쇄 숫자 · 인용 문장의 근거 (파일 이름의 pN = PDF 쪽 = 본문 쪽 + 1) |

- 식 크롭 0 — 원문에 식이 없다 (전 쪽 렌더 확인 · "Eq." · "equation" 0 회).  표 0.

## 6. Post-processing ★
- **원문이 한 것**: 없다 (문헌 값의 서술 · 재게재 그림).
- **이 카드의 후처리**: ① Fig. 4 의 PDF 벡터 경로 (검은 하중 이력 9 조각 · 빨간 하중–깊이 한 경로 19,224 점) 를 눈금 선 좌표의 1 차 맞춤으로 축 환산 → 하중이 일정한 유지 구간 17 개를 찾아 구간 처음 · 끝 30 점 중앙값으로 깊이 변화 (크리프 · 회복) · 제하 중 즉시 변화 · 비율 계산 ② Fig. 2 원본 래스터 (xref 3388 · 1439 × 1019 px) 에서 축 눈금 화소 → 왼쪽 네 곡선의 높이 (ε 1 · 5 · 10 · 15 · 20 · 24 · 24.5 %) · 오른쪽 표지를 색 마스크 + 연결 성분으로 42 개 (범례 표지 넷 제외) ③ 속도 민감도 m · 응력 지수 n ④ 본문 낱말 셈 (DEM · powder · compaction · argyrodite · Li₆PS₅Cl = 0 등) ⑤ 정본 카드 값과의 대조 (K · 부피 변화 · E/H · 크리프).  스크립트 = 이 묶음 scratchpad (`dig_fig4.py` · `ana_fig4b.py` · `dig_fig2d.py` · `write_digitized.py`) — 결과는 `digitized.csv` 에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (이 총설 = 사이클 중 역학의 2 차 문헌 값 ↔ 우리 = Li₆PS₅Cl + NCM811 복합 양극의 300 MPa 압밀 · 접촉망 수송)
| 항목 | 이 총설 | 우리 (CLAUDE.md) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 범위 | 운전 (사이클) 중 응력의 발생 · 해소 · 파괴 — 제조 · 압밀 없음 | 압밀 (DEM · MPM) → 접촉망 수송 · 사이클은 후처리 원장 (A10) | **겹치는 곳은 사이클 원장과 스택압뿐** — 압밀 값의 대조점 0 |
| SE 재료 | 황화물은 유리 (Li₂S–P₂S₅) 와 β-Li₃PS₄ (인용) · 주로 LLZO · Lipon | Li₆PS₅Cl (argyrodite) | 재료 다름 — Li₆PS₅Cl 0 회 |
| SE 탄성 | 값 없음 | DFT E_VRH 22.06 GPa (ν 0.360 · B₀ 26.23) · DEM E_eff 1.35 GPa (18 배 연화) · MPM E 1.53 GPa (ν 0.49 · K 25.5 GPa) | 대조 불가 |
| SE 소성 · 항복 | 값 없음 · "세라믹은 상온에서 슬립 없음 → 파괴" · 비정질은 국소 치밀화 + 전단 · 지수 = E/H · 푸아송비 | MPM J2 (등적 전단만) σ_y 0.30 GPa (Hencky 편차 변형 문턱 · 일축 압축 환산 0.318 GPa) · DEM 은 겹침이 소성의 대리 (Heckel P_y 138 MPa · σ_y_eff 46 MPa) | 우리 MPM 은 Fig. 3 의 **Shear 칸 하나** — 치밀화 (재료 수준 부피 감소) · 전위 인성 · 파괴 칸이 없다.  어느 칸이 Li₆PS₅Cl 냉간 압밀을 지배하는지는 이 총설이 말하지 않는다 (압밀을 다루지 않음) |
| SE 파괴 | 황화물 K ≈0.2 MPa·m^½ [2 차 · ref 54] | DEM · MPM 모두 **SE 파괴 없음** · A10 접촉 원장의 CZM 앵커 = Bucci 2.8 ± 1.8 J/m² (= McGrogan K · E 의 환산 — 정본 `mcgrogan2017_…` §7-3) | 같은 원전 (McGrogan 유리) 을 다른 길로 인용한 것 — 독립 근거가 아니다 |
| 크리프 · 속도 | 황화물 유리 압입 크리프 · 이완 (값 없음) · Li 금속은 속도 500 배에 응력 2.2 배 (ε 1 %) – 2.9 배 (ε 20 %) [판독 · 카드 산술] | DEM · MPM 속도 무관 (점소성 없음) | 우리 한정어 "점소성 미포함" 을 받치는 문헌 문장 (재료 = 유리 · 압입) · 크기는 정본 `papakyriakou2021_…` (Li₆PS₅Cl n 21.3) 에서 |
| AM 파괴 | NMC532 0.3 ("단결정") · 0.1 (다결정 응집체) · LCO 0.2–6.5 · LMO 0.24 · 어림 "~1" [2 차] | Auerbach 파괴 열의 K_IC_AM_P 0.3 · K_IC_AM_S 1.0 MPa·m^½ (정본 `xu2017_…` L40 · `stallard2022_…` L25 가 옮긴 우리 입력 · 출처 재확인 중 — CLAUDE.md `SELF-51`) | 우리 P (다결정) 0.3 = 이 총설의 "단결정 0.3" 과 같은 수 · 우리 S (단결정) 1.0 = 이 총설의 어림 "~1" 과 같은 수 — **라벨이 서로 엇갈린다** (§3-12 ④ · 판정 아님 · 원전 확인 전) |
| AM 부피 변화 | 2 차 입자 3.3 % (NMC111) – 7.8 % (NMC811) [2 차 · ref 12] | 사이클 원장 `--dv-pct` 5.1 (NMC811 3.0–4.3 V · help 글이 Kondrakov 2017 로 적는다 — 정본 `koerver2018_…` L35 · L55 가 옮긴 우리 값) | 같은 원전에 두 숫자 (7.8 ↔ 5.1) — 입자 수준 ↔ 격자 수준으로 보인다 [카드 해석] · Kondrakov 2017 원문 확인 필요 (§12) |
| 첫 사이클 | 계면 균열의 대부분이 첫 사이클 · 초기 용량 손실의 원인 [2 차 · ref 74] | 사이클 원장 첫 실런: "즉시 파단" 꼴 (CLAUDE.md A10) | 방향 같다 (정성) — 원전 (Koerver 2017) 카드 없음 |
| 외부 압력 | 균열 효과를 지우는 관행 ↔ 국소 고전단으로 균열 유발 [2 차 · ref 75] | 스택압 ↔ 재습윤 매핑 = 미결 (CLAUDE.md A10 §5) | 우리 미결 항목에 넣을 문헌 문장 — 값 없음 |
| 접착 · 마찰 | "가장 이해가 덜 된 변수" · 정량 측정 없음 | DEM 마찰 · 응집 = 모델 선택값 · 믹서 SE–SE 점착 앵커 (D3) 실측 보류 | 문헌에 값이 없다는 것 자체가 근거 문장 |
| 탈압 | 압입 제하의 이완 · 부분 회복 (유리 · Lipon) | 언로딩 시험 (등록 단계) · MPM 은 속도 무관 탄소성 | 시간 의존 회복은 우리 모델에 없다 — 측정 시점을 적어야 한다 (§9) |
| 수송 | 없음 (Fig. 1 의 흰 칸 낱말뿐) | 접촉망 σ 삼중 · 복셀 σ | 대조 불가 |

### 7-2. ★ 이 총설의 2 차 값 ↔ 정본 카드 (원전 · 이웃) — 재료 · 방법 칸을 꼭 본다 (판정 없음 · 기존 카드는 고치지 않는다)
| 양 | 이 총설 (인쇄 · 원전 번호) | 정본 카드의 값 (재료 · 방법) | 같음 / 다름 |
|---|---|---|---|
| 황화물 K | *"in the range of 0.2 MPa m^1/2 (54)"* | `mcgrogan2017_…` (원전): 70Li₂S–30P₂S₅ **유리** · Vickers 9.8 N · 풀린 시편 **0.23 ± 0.04** · 안 풀린 시편 0.34 ± 0.08 / `song2025_porous_…`: Li₆PS₅Cl 다공 펠릿 (13 %) CT **0.17 ± 0.03** / `fan2026_…` (미출판 draft): 0.2–0.4 | 반올림 일치 (풀린 유리 값) · 총설은 유리 · 조성 · 방법 · 풀림을 떼고 "Sulfide electrolytes" 로 적었다 |
| 황화물 크리프 | 값 없음 · *"both creep and relaxation within one load-unload cycle"* (70) | `papakyriakou2021_…`: **Li₆PS₅Cl** 열간 펠릿 · 2 mN 유지 150 s 에 +13.9 nm (깊이의 7 %) · n 21.3 ± 3.7 (25 °C) [판독] — 이 총설의 인용 목록에 없다 / `song2025_porous_…` L86: Athanasiou 2022 = Li₂S–P₂S₅ 유리 나노압입 E 10 GPa (그 논문의 2 차 인용) | 총설에 견줄 값이 없다 — 황화물 크리프의 **크기** 는 정본 `papakyriakou2021_…` 가 유일 |
| NMC532 K | "단결정" 0.3 · 다결정 응집체 0.1 (55) | `xu2017_…`: 소결 펠릿 (결정립 ≈10 µm) **0.309 ± 0.04** · 2 차 입자 계면 **0.102 ± 0.03** · SOC 100 % ≈0.058 · 100 사이클 0.036 ± 0.018 | 같은 수 짝 · 표기 다름 · 원전 번호 다름 (55 = de Vasconcelos 2019 ↔ Xu 2017) → §3-12 ④ |
| LCO K | 0.2–6.5 · 2/3 < 1.1 (56) | `stallard2022_…` L41: LCO 큰 결정립 입내 인성 0.2–6.5 | 같다 (2 차끼리 · 원전 = Qu 2012 · 카드 없음) |
| NMC 부피 변화 | 2 차 입자 3.3 % (NMC111) – 7.8 % (NMC811) (12) | `koerver2018_…`: 단위 격자 NCM-811 **−6.5 %** (x ≈0.15 · 판독) · **−6 %** (4.3 V · 인쇄) · NCM-111 −2.0 % (판독) / `li2026_electrochemomechanical_…` L44: Kondrakov — 단위포 최대 **5.1 %** (NCM811) · **1.2 %** (NCM111) | 세 묶음의 숫자가 다르다 — 양 (입자 ↔ 격자) · 전압 창이 다를 수 있다 · 원전 미확인 |
| Li 유동 응력 | 벌크 ≈1 MPa 이하 (4, 32, 33) | `famprikis2019_…` L115: Li 항복 ~0.8 MPa (Masias 2019 = 이 총설의 ref 33) · `doux2020_stack_pressure_assb` L74: Li 항복 ≈0.8 MPa (Masias 외) · 상온 항복은 크리프 지배 (LePage 외 = 이 총설의 ref 4) | 자릿수 같다 (같은 원전들) |

### 7-3. E/H 지수로 본 재료들 — 이 총설의 잣대를 정본 카드 값과 우리 모델 재료에 대 본다 [우리 산술 · 크기 감각 · 판정 아님]
| 재료 | E (GPa) | H (GPa) | E/H | 출처 |
|---|---|---|---|---|
| Lipon 박막 | — | — | **≈23** | 이 총설 p.4/8 [인쇄 · 2 차 · ref 63, 64] |
| 전형적 산화물 유리 | — | — | **10 – 13** | 이 총설 p.4/8 [인쇄] |
| 70Li₂S–30P₂S₅ 유리 | 18.5 (ν 0.3 가정) | 1.9 | 9.7 | 정본 `mcgrogan2017_…` (그 카드의 산술) |
| Li₆PS₅Cl 치밀 펠릿 | 27.6 | 1.41 | 19.6 [우리 산술] | 정본 `lee2025_heckel_…` L111–112 |
| Li₆PS₅Cl 열간 펠릿 (25 °C) | E_r 33.8 | 1.87 | 18.1 (E_r/H) [우리 산술] | 정본 `papakyriakou2021_…` L23 [판독값] |

- 이 잣대로는 황화물 **유리** (9.7) 가 산화물 유리 범위의 아래 끝이고 **Li₆PS₅Cl** (18–20) 은 산화물 유리와 Lipon 사이다 — 압자 · 하중 · 시편이 서로 다르고 (큐브 코너 20 mN ↔ 8 mN ↔ Berkovich 2 mN) E_r 은 E 가 아니므로 순위를 매기지 않는다.
- **우리 MPM 재료** [우리 산술 · CLAUDE.md frame [1] 주석의 일축 환산]: 연화 재료 (E 1.53 GPa · ν 0.49) 의 일축 압축 항복 0.318 GPa → **항복 변형률 0.318 / 1.53 ≈ 21 %** ↔ 실제 강성 (E 22.06 · ν 0.36) 이면 0.363 / 22.06 ≈ 1.6 %.  E/H 9.7–23 인 실제 재료의 Tabor 꼴 어림 H / (3E) = 1 / (3 · E/H) 은 **1.4 – 3.4 %** 다.  ⇒ 연화 영률을 쓴 모델 재료는 항복까지 쌓이는 탄성 변형이 실제의 한 자릿수 위다 — 압력을 뺄 때 되돌아오는 탄성 몫 (단계 6) 을 읽을 때 연화의 부작용으로 같이 적는다 (연화값은 물성이 아니라 재배열의 대리 — CLAUDE.md frame [2] · 판정 아님).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 모델이 아니라 **틀과 지도** — 응력의 출처 셋 · 해소 기전의 분류 (Li 소성 / 유리의 치밀화 + 전단 / 세라믹의 전위 / 파괴) · 손상 꼴 넷 (Fig. 5) · 모델이 담아야 할 넷 (길이 규모 · 마찰 · 접착 · 크리프).  역학 (MPM) 쪽 개념의 2 차 문헌.
- **없는 것**: 접촉망 · 수송 (DEM 쪽) · 압밀 · 기공 · 복합체의 정량 · 황화물 argyrodite 의 값 전부.  ⇒ DEM (수송) · MPM (형상 소성) 어느 쪽의 검증 표적도 아니다 — **우리 두 모델에 없는 두 축 (SE 파괴 · 시간 의존) 을 한정어로 적을 때의 인용처**이고, 값은 원전 (ref 54 · 70 · 74 · 75 · 12) 에서 가져와야 한다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 총설 = 사이클 중 역학 · 2 차 값 · Li₆PS₅Cl 0 회 — 모든 행에 "재료 · 범위 다름".)

| 이름 | 이 총설이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 문헌 역학 값을 받을 때 적을 칸 = **길이 규모 · 변형률 속도 · 온도** — 총설의 중심 주장 (*"as a function of length scale and strain rate"*) · Li 가 벌크 ≈1 MPa ↔ 76 nm 244 MPa 로 두 자릿수 갈리는 예.  나노압입 경도 (깊이 0.2–2 µm · 초 단위) 를 µm 입자의 300 MPa 압축 (우리 속도) 에 옮길 때 같은 물음이 선다 | 기공 · 밀도 · 기공 연산자 숫자 0 · 랩 표준 (10–13 % · 1.64) 과 나란히 놓을 값 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 구성식 선택의 지도 (Fig. 3): 등적 전단 (J2) 만으로는 유리의 치밀화 몫 · 파괴가 빠진다는 분류 | 구성식 · 시험 해 · 값 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | σ_y 를 문헌 경도 · 항복과 견줄 값은 **주지 않는다** (CLAUDE.md `SELF-160` 의 빈 곳 그대로).  주는 것 = 한정어 문장: 결정 세라믹은 상온에서 슬립이 안 켜진다 → 맞춘 σ_y 는 "전위 소성의 항복" 이 아니라 **압밀을 내는 모든 기전 (파괴 · 재배열 · 국소 흐름) 의 대리** 라고 적는 근거 [카드 해석] | 황화물 argyrodite 를 시험한 문장이 아니다 (산화물 문맥) · 맞춤 표적은 랩 표준 |
| **단계 5** (3D 복합 압밀) | 응력의 출처 셋 가운데 (iii) 외부 가압 · *"hard contacts"* 를 만들지 않는 재료라는 요구 · AM 파괴 인성 (NMC532 0.1–0.3) | 복합 기공 · 하중 몫 · 성형압 값 0 — 압밀은 범위 밖 |
| **단계 6** (탈압 · 되돌아옴) | ★ 되돌아옴에 **즉시 (탄성) 몫과 시간 의존 몫** 이 있다는 실험 쪽 근거: 황화물 유리의 부하–제하 안 이완 [70] · Lipon Fig. 4 [판독] = 절반 하중에서 10 s 동안 즉시 회복의 **0.27–0.30 배** 더 회복 · 유리 치밀화는 일부 되돌아오고 전단 흐름은 영구 · 설계 요구 *"reversible strain"* | 재료 = Lipon 박막 · 황화물 **유리** (Li₆PS₅Cl 아님) · 압입 (nm · mN) ↔ 펠릿 · 분말 침대 · 완전 탈압이 아니라 절반 제하 · 수치 표적 아님 |
| **단계 7** (형상 · 피복 · 수송) | 손상 꼴 넷 (Fig. 5) · 첫 사이클에 계면 균열의 대부분 [74] · Fig. 1 양극 쪽 흰 칸의 그림 글자 'Loss of contact' · 'Poor transport' (글자 층에 없음 · 렌더로 읽음) | 접촉 손실의 크기 · 저항 증가 값 0 |
| **후보 D0** (지금 DEM) | DEM 을 말하지 않는다.  쓸 문장 둘: 접착 · 마찰 값은 문헌에 없다 (우리 μ · 응집 = 모델 선택값이라고 적는 근거) · 우리 DEM 에 없는 SE 파괴의 크기 (K ≈0.2) | 연화 영률을 정당화 · 반박하는 내용 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 미끄럼 · 분리 규칙을 넣어야 하는 이유의 문헌 문장: *"Friction effects become important to maintaining coherent interfaces in the context of stack pressure"* · 계면 전단 응력이 마찰 계수 · 스택압 · 두께비에 달렸다 [76] (Li–SSE 계면) | 마찰 계수 · 접착 에너지 값 0 · AM–SE 계면의 측정 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 사이클 고유 변형 입력: NMC 2 차 입자 3.3–7.8 % [2 차 · ref 12] · 부호가 반대인 두 양극을 섞어도 입자 국소 변형은 남는다는 경고 | 압밀 단계에는 해당 없음 |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM) | 없음 (접촉 법칙을 다루지 않는다) | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 캡 값의 출처가 될 황화물 경도 · 항복은 없다 — "세라믹은 깨진다" 는 문장은 캡이 소성이 아니라 파괴를 대리할 수 있음을 뜻한다 [카드 해석] | 값 0 |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U3** (단단한 구를 소성 블록에 눌렀다 떼기): Fig. 4 의 꼴 — 유지 중 깊이 증가 (+4.9–6.9 nm / 10 s) · 부분 제하 뒤 시간 의존 회복 · 이력 고리.  속도 무관 탄소성 모델은 유지 중 변화 0 · 제하 뒤 변화 0 을 낸다 → U3 결과를 실험 곡선과 견줄 때 **"유지 구간의 변화는 모델 범위 밖"** 이라고 미리 적는다.  **U2 · U4** 는 값이 없다는 문장만 | U0 · U1 · U5 · U6 없음 · 재료 = Lipon |
| **R1–R7** | **R2** (미끄럼 · 분리): 접착 · 마찰이 핵심 변수이나 값이 없다 · **R4** (탈압 · 되돌아옴): 가역 변형 요구 · 시간 의존 회복 · **R6** (SE 입자 형상 변형): 반대편 문장 — 결정 세라믹은 슬립 없음 · 비정질은 국소 치밀화 + 전단 (형상 변형의 기전을 하나로 단정하지 말 것) · **R7** (AM 파괴): NMC532 0.1 / 0.3 · LCO 0.2–6.5 · 어림 ~1 [2 차] | R1 · R3 · R5 없음 |
| **결과 전 대조 항목** | Li₆PS₅Cl · 압밀에 대한 수치 0.  적어 둘 정성 항목 둘: (a) 사이클 모사에서 계면 손상의 대부분이 첫 사이클에 나는가 [74] (b) 외부 압력을 올릴 때 국소 전단이 큰 곳에서 균열이 느는가 [75] — 둘 다 원전 확인 뒤 등록 | 값은 원전 (카드 없음) 에서 |

- **재료 · 차원 · 조건 차이**: 재료 다름 (Li 금속 · LLZO · Lipon · 황화물 유리 ↔ 결정 Li₆PS₅Cl 분말) · 운전 중 응력 ↔ 제조 압밀 · 나노압입 규모 ↔ 침대 규모 · 계산 없음 (2D / 3D 해당 없음).

## 9. 적용 인사이트 (행동)
1. **한정어의 인용처로 쓴다 (값의 출처로 쓰지 않는다)** — 우리 모델에 없는 것 둘을 적을 때: "SE 파괴 미포함" ← *"Sulfide electrolytes demonstrate even lower resistance to fracture"* (값은 정본 `mcgrogan2017_…` · `song2025_porous_…` 에서) · "점소성 · 시간 의존 미포함" ← 황화물 유리의 상온 압입 크리프 · 이완 문장 (크기는 정본 `papakyriakou2021_…` 에서).
2. **탈압 결과에 측정 시점을 적는다 (단계 6 · R4)** — 되돌아옴은 즉시 몫 + 시간 의존 몫이다 (Lipon Fig. 4 [판독]: 10 s 안에 즉시 몫의 0.27–0.30 배 추가 · 황화물 유리도 같은 꼴이라는 문장).  실험 쪽 두께 · 기공을 받을 때 "압력을 뺀 뒤 얼마 뒤에 쟀나" 를 결과 전 등록 칸에 넣는다 — 정본 `kollenda2024_…` 의 '측정 유효 기간' 과 같은 요구.
3. **문헌 역학 값의 원장에 "길이 규모 · 속도 · 온도" 칸 (단계 0)** — 이 총설의 중심 주장.  나노압입 경도 · 크리프를 입자 규모 압밀에 옮길 때 무엇이 달라지는지 (압입 깊이 ↔ 입자 지름 · 유지 시간 ↔ 가압 시간) 를 같이 적는다.
4. **모델 재료의 "항복 변형률 (또는 E/H)" 을 보고 칸으로 (단계 2 · 4 · 6)** — 연화 영률 (1.53 GPa) + σ_y 0.30 GPa 의 항복 변형률 ≈21 % [우리 산술] ↔ 실제 재료 1.4–3.4 % (§7-3).  탈압 되돌아옴의 탄성 몫이 연화 때문에 커질 수 있다는 점을 단계 6 보고의 한정어로.
5. **사이클 원장 입력의 수준을 가른다 (흐름 밖: A10 사이클 열화)** — `--dv-pct` 5.1 (help 글 = Kondrakov 2017) ↔ 이 총설이 같은 원전으로 적은 "2 차 입자 7.8 %" — 격자 수준인지 입자 수준인지 원문에서 확인하기 전에는 어느 쪽도 "Kondrakov 값" 이라 단정하지 않는다 (§12 후보).
6. **스택압 ↔ 재습윤 매핑 (A10 §5 미결) 에 "압력의 두 얼굴" 을 넣는다 (흐름 밖)** — 외부 압력은 균열 효과를 지우지만 국소 고전단으로 균열을 낸다 [2 차 · ref 75] — 원전 (Yamamoto 2020) 을 본 뒤.
7. **AM 파괴 인성 라벨 점검 (R7 · CLAUDE.md `SELF-51` 계열)** — 우리 K_IC_AM_P 0.3 · K_IC_AM_S 1.0 ↔ 이 총설 "단결정 0.3 · 다결정 응집체 0.1 · 어림 ~1" ↔ 정본 `xu2017_…` "소결 펠릿 0.309 · 2 차 입자 0.102" — 세 곳의 라벨이 엇갈린다.  ref 55 (de Vasconcelos 2019 = 후보 표 N-24) 원문으로 닫는다.
8. **DEM 마찰 · 응집 값의 지위 문장 (후보 D0 · 믹서 D3)** — "접착 · 마찰은 SSB 에서 가장 이해가 덜 된 변수이고 정량 측정이 없다" (Kalnaus 2023 p.6/8) → 우리 값은 '모델 선택값 · 실측 앵커 없음' 이라고 적는 근거.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In solid-state batteries the majority of failures are 'first and foremost a mechanical failure'; when inelastic flow cannot be activated at the relevant length and time scale, 'the stress relief proceeds through fracture' (Kalnaus et al., *Science* 381 (2023) eabg5998)."
- "The review lists 'detailed modeling … that includes length-scale effects, friction, adhesion, and creep' among the open problems, and notes that adhesion and friction 'are among the most poorly understood' variables."
- "External pressure is the current practice to negate cracking in composite cathodes, but it 'creates a complex stress state inside the cathode with the possibility of local regions with high shear, which can induce further cracking' (Kalnaus et al. 2023, citing Yamamoto et al. 2020)."
- 국문 (2 차 인용 표지와 함께): *"황화물 전해질의 파괴 인성은 0.2 MPa·m^½ 수준이고 (Kalnaus 2023 이 McGrogan 2017 의 유리 값을 인용), 황화물 유리는 상온 나노압입에서 크리프와 이완을 보인다 (같은 총설이 Athanasiou 2022 를 인용 · 값은 원전에서) — 우리 모델은 SE 의 파괴와 시간 의존 변형을 담지 않는다."*
- ⚠ 이 총설을 근거로 쓰지 않을 문장: "Li₆PS₅Cl 은 소성 변형한다 / 크리프한다" (argyrodite 0 회) · "고분자 전해질은 영률 · 항복강도가 낮다" (그런 문장 없음) · "NMC532 단결정 K 0.3" (라벨 미확인).

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**
1. 포괄적 개관이 아니다 (*"will not be a comprehensive overview"* p.1/8) · 범위는 사이클 중 응력 (초록).
2. 양극재의 미세 · 나노 역학 문헌은 *"scarce"* (p.4/8) · 비정질 · 유리 전해질의 변형 · 파괴 연구는 *"rather limited"* (p.5/8) · Lipon 역학 연구도 *"limited"* (p.4/8).
3. 계면 균열의 피로 성장 가설은 실험 정보 부족으로 가리지 못한다 (p.5/8).
4. 접착 · 마찰의 정량 측정이 없다 (p.6/8) · 치밀화 회복은 MD 로 못 본다 (p.5/8).
5. 불균일 석출의 기원은 *"not well understood"* (p.2/8).

**카드가 본 한계 · 원문 안 어긋남**
6. **모든 수치가 2 차 인용** — 방법 · 시편 · 조건이 떨어져 나갔다 (황화물 K 는 유리 · Vickers · 풀림 여부가 빠졌고, NMC532 "단결정" 은 라벨이 의심스럽다 · §3-12).
7. **황화물은 주변부** — 역학 수치 하나 · 크리프 한 문단 · argyrodite 0 회 · 할라이드는 "비슷할 것" 이라는 추정 한 줄.
8. **압밀 · 제조 · 기공이 없다** — SE 를 분말이 아니라 연속 고체 · 박막으로 본다.  "ceramic electrolytes … instead fracture" 를 냉간 압밀의 기전 서술로 읽으면 과하다.
9. **Fig. 2 · Fig. 4 는 재게재** — 판독값은 이 PDF 의 그림에서 읽은 것이고 원 논문의 자료 처리 (표류 보정 · 압자 · 시편) 는 모른다.  본문 문장과 그림이 문자 그대로는 안 맞는 곳이 있다 (위스커 12–244 MPa ↔ 607–76 nm).
10. **저자 그룹의 시각** — Li 금속의 길이 · 속도 의존과 Lipon 은 저자들 자신의 측정 (ref 14 · 34 · 63 · 64) 이다.
11. **전이 한계**: Li 금속 · LLZO · Lipon · 황화물 유리의 나노 규모 · 운전 중 역학 ↔ Li₆PS₅Cl + NCM811 분말의 300 MPa 압밀.  절대값 전이 0 건.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

**★ 1 차 원전 후보 (논문 에이전트 후보) — 이 총설이 황화물 · 복합 양극 역학의 출처로 든 논문 가운데 정본 카드가 없는 것** (정본 `litdb/papers/` 파일 목록 534 개 (`_TEMPLATE.md` 포함 · 이 카드 넣기 전) + DOI · 제목 · 저자 grep 으로 확인 · 2026-11-12 · push 직전 원격 끝에서 다시 확인):

| 번호 | 서지 (원문 목록 그대로) | 이 총설이 무엇의 출처로 들었나 | 우리 쪽 쓰임 | 정본 확인 |
|---|---|---|---|---|
| [70] | C. E. Athanasiou et al., Rate-dependent deformation of amorphous sulfide glass electrolytes for solid-state batteries. Cell Rep. Phys. Sci. 3, 100845 (2022). doi: 10.1016/j.xcrp.2022.100845 | ★★ 황화물 유리의 상온 나노압입 크리프 · 점탄성 · 한 부하–제하 안의 이완 (p.5/8) — 이 총설의 유일한 황화물 크리프 근거 | 질문 b · c · l · 단계 6 · U3 — 값 (하중 · 유지 시간 · 속도 의존 · 조성) | 카드 없음 (`song2025_porous_…` L86 이 E 10 GPa 로 2 차 인용) |
| [75] | M. Yamamoto, Y. Terauchi, A. Sakuda, A. Kato, M. Takahashi, Effects of volume variations under different compressive pressures on the performance and microstructure of all-solid-state batteries. J. Power Sources 473, 228595 (2020). doi: 10.1016/j.jpowsour.2020.228595 | ★ 외부 압력 → 양극 안 복잡한 응력 · 국소 고전단 → 균열 (p.5/8) · Fig. 5 사진 | 질문 b · d · i · 단계 5–6 · 스택압 ↔ 재습윤 (A10 §5) — 압력별 부피 변화 · 미세구조 | 카드 없음 ("228595" grep 0 · 같은 1 저자의 다른 논문 (2017 J. Ceram. Soc. Jpn. · 2018 Sci. Rep.) 은 `doerrer2021_…` · `hippauf2019_…` 가 인용만) |
| [74] | R. Koerver et al., Capacity fade in solid state batteries: Interphase formation and chemomechanical processes in nickel rich layered oxide cathodes and lithium thiophosphate solid electrolytes. Chem. Mater. 29, 5574–5582 (2017). doi: 10.1021/acs.chemmater.7b00931 | ★ 계면 균열의 대부분이 첫 사이클 · 초기 용량 손실 · NMC811/β-Li₃PS₄ (p.5/8) · Fig. 5 사진 | 단계 7 · 사이클 원장의 "즉시 파단" 대조 · 질문 j | 카드 없음 (DOI "chemmater.7b00931" grep 0 · 제목 "Capacity fade in solid" grep = `barai2021_…` · `jung2019_…` · `koerver2018_…` 가 인용만 — `koerver2018_…` 은 같은 1 저자의 다른 논문) |
| [12] | A. O. Kondrakov et al., Anisotropic lattice strain and mechanical degradation of high- and low-nickel NCM cathode materials for Li-ion batteries. J. Phys. Chem. C 121, 3286–3294 (2017). doi: 10.1021/acs.jpcc.6b12885 | NMC 2 차 입자 부피 변화 3.3 % (NMC111) – 7.8 % (NMC811) (p.1/8) | 사이클 원장 `--dv-pct` 5.1 의 원전 대조 (입자 ↔ 격자 수준) · 후보 A · A′ 의 고유 변형 | 카드 없음 (`koerver2018_…` · `li2026_electrochemomechanical_…` · `intergranular_cracking_nmc811_jmca2023` 이 인용만) |
| [64] | S. Kalnaus, A. S. Westover, M. Kornbluth, E. Herbert, N. J. Dudney, Resistance to fracture in the glassy solid electrolyte Lipon. J. Mater. Res. 36, 787–796 (2021). doi: 10.1557/s43578-020-00098-x | Fig. 4 (Lipon 반복 압입) · E/H ≈23 · 치밀화 + 전단 · MD (p.4/8–5/8) | U3 · 단계 6 의 실험 곡선 원자료 (압자 · 막 두께 · 표류 보정) — 같은 1 저자 · 다른 해 | 카드 없음 ("s43578" grep 0) |

**그 밖에 볼 것** (원문 목록 그대로):

| 번호 | 서지 | 왜 |
|---|---|---|
| [54] | F. P. McGrogan et al., Compliant yet brittle mechanical behavior of Li2S-P2S5 Lithium-ion-conducting solid electrolyte. Adv. Energy Mater. 7, 1602011 (2017). | 황화물 K 0.2 의 원전 — **정본 카드 있음** (`mcgrogan2017_…`) |
| [55] | L. S. de Vasconcelos, N. Sharma, R. Xu, K. Zhao, In-situ nanoindentation measurement of local mechanical behavior of a Li-ion battery cathode in liquid electrolyte. Exp. Mech. 59, 337–347 (2019). | NMC532 K 0.3 · 0.1 의 인용처 — 후보 표 **N-24** 와 같은 논문 (이 목록은 연도를 **2019** 로 인쇄 · 후보 표는 59 (3) (2018) · status = 대기) · "단결정" 라벨 확인.  같은 그룹 2016 논문 카드 `devasconcelos2016_…` (N-23) 는 있으나 다른 논문 (E · H 만) |
| [56] | M. Qu et al., Nanomechanical quantification of elastic, plastic, and fracture properties of LiCoO2. Adv. Energy Mater. 2, 940–944 (2012). | LCO K 0.2–6.5 — wishlist batch_45 에 이미 있음 (McGrogan 의 ref [33]) |
| [11] | R. Koerver et al., Chemo-mechanical expansion of lithium electrode materials–on the route to mechanically optimized all-solid-state batteries. Energy Environ. Sci. 11, 2142–2158 (2018). | 영 변형 · 섞기 전략의 원전 — **정본 카드 있음** (`koerver2018_…`) |
| [1] | T. Famprikis, P. Canepa, J. A. Dawson, M. S. Islam, C. Masquelier, Fundamentals of inorganic solid-state electrolytes for batteries. Nat. Mater. 18, 1278–1291 (2019). | **정본 카드 있음** (`famprikis2019_…`) |
| [10] | M. J. Wang, E. Kazyak, N. P. Dasgupta, J. Sakamoto, Transitioning solid-state batteries from lab to market: Linking electro-chemo-mechanics with practical considerations. Joule 5, 1371–1390 (2021). | 이 총설이 "포괄적 개관" 으로 미룬 글 — 제조 · 스택압의 실용 쪽 |
| [76] | C. G. Haslam, J. B. Wolfenstine, J. Sakamoto, The effect of aspect ratio on the mechanical behavior of Li metal in solid-state cells. J. Power Sources 520, 230831 (2022). | 계면 마찰 · 스택압 · 두께비 (Li 금속) |
| [41] | S. Narayan, L. Anand, On modeling the detrimental effects of inhomogeneous plating-and-stripping at a lithium-metal/solid-electrolyte interface in a solid-state-battery. J. Electrochem. Soc. 167, 040525 (2020). | 큰 변형 이론의 Li 금속 모델 (흐름 밖) |
| [4] · [33] | W. S. LePage et al., J. Electrochem. Soc. 166, A89–A97 (2019) · A. Masias et al., J. Mater. Sci. 54, 2585–2600 (2019) | 벌크 Li 의 속도 · 온도 의존 · 탄성 · 소성 · 크리프 (Fig. 2 왼쪽의 원전) |
| [63] | E. G. Herbert, W. E. Tenhaeff, N. J. Dudney, G. M. Pharr, Mechanical characterization of LiPON films using nanoindentation. Thin Solid Films 520, 413–418 (2011). | Lipon E · H (E/H ≈23 의 원자료) |
| [58] · [59] | J. Li et al., Sci. Adv. 5, eaaw5519 (2019) · L. Porz et al., Mater. Horiz. 8, 1528–1537 (2021) | 세라믹에 전위를 넣어 상온 소성 · 인성을 얻는 길 |

## 13. [미확인] 목록 (원문 10 쪽 전수에 없음)
1. 황화물 전해질의 E · G · ν · 경도 · 항복 · 크리프 지수 — 값 0.
2. ref 70 의 황화물 유리 조성 · 압입 하중 · 유지 시간 · 깊이 · 이완 크기.
3. ref 54 값의 재료 (유리) · 방법 (Vickers) · 풀림 여부 — 총설에 없음 (정본 `mcgrogan2017_…` 로 확인).
4. Li₆PS₅Cl (argyrodite) 에 대한 모든 것 · 분말 압밀 · 성형압 · 기공률 · 진밀도.
5. 외부 압력의 값 · 국소 전단의 크기 (ref 75) · 접착 에너지 · 마찰 계수.
6. Fig. 4 의 압자 꼴 · Lipon 막 두께 · 기판 · 표류 보정 · 온도 · 유지 시간의 인쇄값 (판독 ≈10 s).
7. Fig. 2 의 원 논문 그림 번호 · 방위별 시편 수 · 오차 막대의 정의.
8. NMC 부피 변화 3.3 · 7.8 % 의 전압 창 · 측정법 (2 차 입자를 어떻게 쟀나).
9. NMC532 "single-crystal" 0.3 의 시편 정의 (ref 55 원문).
10. 상동 온도의 값 · 유리 전이 온도 값.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- PDF 10 쪽을 글자 층 추출 + 전 쪽 렌더로 읽음.  서지 = PDF p.1 (Cite this article as … Science 381, eabg5998 (2023). DOI) · p.2 (제목 · 저자 · 소속) · p.9 (Submitted / accepted · 10.1126/science.abg5998 · 감사) · p.10 (Science 381 (6664)).  SI · 표 · 식 없음.
- 원문 낱말 셈 (본문 p.1/8–7/8 · 참고문헌 앞): DEM · discrete element · finite element · continuum · phase field · powder · compact · calender · cold-press · argyrodite · Li₆PS₅Cl · Supplement = **0** · sulfide 3 (+ 요약 쪽 1) · creep 4 · yield 3 (Li 금속 2 + 동사 1) · hardness 2 · modulus 2 · plastic 9 · ductil 7 · brittle 6 · fracture toughness 12 · densif 11 · stack pressure 4 · adhesion 9 · friction 8 · particle 10 · model 6 · simulat 2 · polymer 1.
- 그림 크롭 **31 장** = 도구 5 (Fig. 2–6 — **Fig. 6 그대로** · **Fig. 2 다시 자름** (오른쪽 끝에 단 사이 괘선 · 괘선 이음매 점) · **Fig. 3 · 4 · 5 다시 자름** (위쪽에 괘선 이음매의 1 화소 점)) + 손 크롭 26 (요약 쪽 그림 · **Fig. 1** (캡션이 그림 옆에 있어 도구가 "그래픽 없음" 으로 놓침) · 패널 4 = Fig. 2 좌 · 우 · Fig. 4 좌 · 우 · 근거 문단 20) · 식 0 · 표 0 · 전체 쪽 그림 0.  31 장 전부 열어 확인.  손 크롭을 다시 렌더한 것: fig_1 (아래 범례 아이콘 잘림) · fig_3 · fig_4 (이음매가 첫 clip 안) · Fig. 2 패널 (가르는 선) · Fig. 4 패널 (400 → 600 dpi) · 근거 문단 20 (첫 렌더의 위 · 아래 여백에 이웃 줄이 걸림 → 줄 사이 틈에서 끊고 흰 여백을 덧댐).  모든 쪽 오른쪽 여백의 세로 내려받기 표지 (x ≥ 563 pt) 는 어느 크롭에도 들어가지 않게 잘랐다.  `figures.json` 의 `recrop` · `manual_crop` · `note_manual` · `note_ko`.
- 판독: Fig. 4 = PDF 벡터 경로 (잔차 ≤ 0.07 s · 0.11 nm · 0.004 mN) · Fig. 2 = 원본 래스터 xref 3388 (잔차 ≤ 0.009 % · 0.001 MPa / 0.4 nm · 0.16 MPa) → `digitized.csv` 113 행.
- 2 차 인용 대조: 가리킨 카드 셋의 줄 (§0-1) · 정본 카드 값 여섯 묶음 (§7-2) — 카드는 고치지 않았다 (카드 문제 = 정독 출력 batch_47 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + "Kalnaus" · "eabg5998" · "abg5998" · 제목 낱말 grep — 카드 없음 (인용만: alharbi2026 · lee2025_heckel · yuan2026) (2026-11-12).
- 이어받은 마무리 (같은 날 · 앞 조수가 사용량 한도로 멈춘 뒤): 원 PDF 글자 층을 다시 내려 앞 조수의 덤프와 10 쪽 모두 같음을 확인 · 카드의 영어 인용 127 개를 글자 층에 대조 (없는 것 5 = 가리킨 카드 인용 1 · 한국어 문장 2 · 그림 글자 1 · 인용 안에 원전 번호를 붙인 것 1 → 고친 것: §7-2 의 "(70)" 을 인용 밖으로 · §3-12 ④ 를 영어 원문으로 · §8 의 Fig. 1 그림 글자 표기 · 고친 뒤 126 개 중 없는 것 2 = 가리킨 카드의 한국어 인용 · §10 의 한국어 발표 문장) · 숫자 · 서지 (호 6664 · 접수 · 수락 · 참고문헌 [12] · [54]–[57] · [64] · [70]–[76]) 를 글자 층에서 다시 대조 · 판독 원자료로 §3-4 · §3-7 의 [카드 산술] 을 다시 계산 (같음) · 다른 정본 카드 줄 번호 인용 12 곳과 가리킨 카드 세 줄을 지금 정본에서 다시 열어 같음을 확인 · 크롭 31 장을 다시 열어 봄 (다시 자른 것 0) · 원격 끝에 있는 `devasconcelos2016_…` (ref 55 와 다른 논문) 를 §3-12 ④ · §12 · 관련 카드에 적음 · §12 의 파일 수 "535 장" → 534 개 (`_TEMPLATE.md` 포함) 로 고침 · 짧은 표기 `li2026_…` · `song2025_…` · `yuan2026_…` 는 같은 앞머리 카드가 여럿이라 앞머리를 늘림.

## 🔗 관련 카드
- 이 총설을 인용한 카드 (가리킨 카드): `alharbi2026_coupled_design_ultrathin_composite_se_review` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal`.
- 이 총설이 인용한 논문의 정본 카드: `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` (ref 54) · `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (ref 11) · `famprikis2019_fundamentals_inorganic_sse` (ref 1).
- 황화물 SE 의 역학 값 (이 총설에 없는 크기): `papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation` (Li₆PS₅Cl 크리프) · `song2025_porous_argyrodite_modulus_fracture_toughness` · `var2026_sulfide_se_mechanical_properties_local_indentation_pellet` · `sakuda2013_sulfide_mechanical_property` (황화물 유리의 상온 가압 소결) · `fan2026_sulfide_assb_stability_review_ECERD2600097` (K 0.2–0.4 · 입경 창).
- 양극재 파괴 · 부피 변화: `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` · `stallard2022_cathode_mechanical_properties_review` · `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` · `intergranular_cracking_nmc811_jmca2023` · `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` (ref 55 와 같은 그룹의 **다른** 2016 논문 — E · H 만 · §3-12 ④).
- 같은 주제의 총설 · 모델: `li2026_electrochemomechanical_coupling_asslmb_review` · `deysher2022_transport_mechanical_aspects_assb_review` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` · `bucci2017_chemomech_failure_assb_cycling_czm` · `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` · `barai2021_delamination_cathode_llzo_multiscale`.
- 스택압 · 시간 의존 되돌아옴: `doux2020_stack_pressure_assb` · `kollenda2024_time_sensitivity_calendered_electrode_springback_storage` · `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
