# 배치 45 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` (408 줄 · 원문 = MIT DSpace 저자 원고판 15 쪽 (PDF 16 쪽) · SI · 표 없음 ·
그림 크롭 26 장 = 도구 4 (다시 자름 2) + 패널 4 · 식 (1)–(4) · 근거 문단 14 · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 63 행).
서지 (k · l 인용용) = McGrogan F. P., Swamy T., Bishop S. R., Eggleton E., Porz L., Chen X., Chiang Y.-M., Van Vliet K. J., *Compliant Yet Brittle
Mechanical Behavior of Li₂S–P₂S₅ Lithium-Ion-Conducting Solid Electrolyte*, Adv. Energy Mater. 7 (12) 1602011 (2017), DOI 10.1002/aenm.201602011.
⚠ 재료 = **70Li₂S–30P₂S₅ 용융 급랭 유리** (Li₆PS₅Cl 아님) · 측정 논문 (계산 없음) — 아래 값은 우리 LPSCl 값으로 옮기지 않는다.
쪽 = 원고 쪽 (PDF 쪽 = 원고 쪽 + 1).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **없음** — 압력별 밀도 · 기공 곡선이 없다.  유일한 가압 = EIS 용 분말을 1.3 cm 폴리카보네이트 관에서 **360 MPa 냉간 가압** (≈1 mm 펠릿) 한 번 · 그 펠릿과 압입한 유리 덩어리 모두 **밀도 · 기공 · 진밀도 분모가 원문에 없다** ("density" = energy density 두 번뿐) | 카드 §0 ⑥ · §3-1 · §3-2 · 원고 p.9 | [인쇄] · [미확인] | 재료 70:30 유리 · 랩 표준 (1.64 · 10–13 %) 과 견줄 숫자 없음

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **없음** — 분말 · 펠릿 탈압 없음.  압입 제하 (30 s) 는 식 (1) 의 제하 초기 기울기 (dP/dh) 에만 쓰였고 **하중–깊이 곡선 · 잔류 깊이 · 회복 비율은 실리지 않았다** · Vickers 제하 뒤 방사 균열이 K 의 원자료 | 카드 §4-3 ④ · §3-3 · 원고 p.10 | [미확인] | 국소 압입 · 유리

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **H 1.9 ± 0.2 GPa** = 식 (3) H = P_max/A (투영 접촉 면적 · 이상 큐브 코너 면적 함수) · 큐브 코너 20 mN · 깊이 ≈2 µm · 부하 120 s / 유지 10 s / 제하 30 s · n 39 · 광유 침지 | 카드 §3-3 · §3-4 · 원고 p.3 · p.10–11 · 식 (3) | [인쇄] | 유리 70:30 · 하중 하나 · 압입 크기 · 속도 효과 미분리
- [c] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **항복 세기 · 일축 환산 · 크리프는 원문에 없다** (yield · Tabor · creep 0 회) · [우리 산술 · 프롬프트 규약] Tabor 꼴 H/3 = **0.63 GPa** ↔ MPM σ_y 0.30 (Hencky 문턱 · 일축 환산 0.32–0.45) · DEM σ_y_eff 46 MPa · Li₆PS₅Cl 나노압입 H 1.41 (lee2025) 의 1.35 배 | 카드 §3-7 · §3-8 · §7-1 | [우리 산술] | 구속 계수는 유리 · 큐브 코너에 맞는지 판정 안 함
- [c] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **E 18.5 ± 0.9 GPa** (식 2 · ν 0.3 가정 = Sakuda [8] · E_i 1070 · ν_i 0.07) · E_r 19.95 (인쇄 안 됨) · ν 0.36 이면 E 17.7 · **G 7.1 ± 0.3 = 계산값** (실측 아님) | 카드 §3-4 · 원고 p.3 · p.10–11 | [인쇄] · [카드 산술] | E · G 가 ν 가정에 묶임
- [c] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **K_Ic 0.23 ± 0.04 (풀림 · n 18) · 0.34 ± 0.08 MPa·m^½ (안 풀림 · n 12)** · 식 (4) K = k(E/H)^½P/c^{3/2} · k 0.016 (Anstis [12]) · P 9.81 N (Vickers 1000 gf · 유지 15 s · 기름 막) · c = 압흔 중심 ~ 균열 끝 · Welch p < 0.001 · 판독 재현 평균 0.2319 / 0.3426 · SD 0.041 / 0.082 · t 4.33 · p 6.2e-4 · 시간 경향 없음 (기울기 p 0.38 · 0.91) · K²/E 2.86 / 평면변형 2.60 J/m² | 카드 §3-5 · 원고 p.4 · p.11–12 · Fig. 2b | [인쇄] · [판독] · [카드 산술] | "plane strain Mode I 의 근사" (저자) · 원자료 (c) 숫자 없음

## d — 단단한 입자 + 무른 입자 혼합 압축의 하중 몫 · 재밍

- [d] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **직접 없음** — 하중 몫 · 재밍 자료 없음.  크기 감각만: 그림 4 스택의 LiCoO₂ (E 178 · H 8.3 GPa · K 0.94) ÷ LPS 유리 (18.5 · 1.9 · 0.23) = E 9.6 배 · H 4.4 배 [카드 산술] ↔ 우리 DEM E_AM 140 (출처 재확인 중 · SELF-51) ÷ E_eff 1.35 = 104 배 [우리 산술] | 카드 §3-6 · §7-1 · 원고 p.7 · Fig. 4 | [인쇄 (그림 글자)] · [카드 산술] · [우리 산술] | LCO ≠ NCM · 유리 ≠ LPSCl · 판정 아님

## e — 점접촉 법칙이 깨지는 범위와 대안 · 맞춘 값 수

- [e] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **접촉 법칙 · DEM 없음.**  대신 문헌 **항복 캡 DEM (후보 C′ 류)** 의 캡 입력 원천: So 2021/2022 F_th = 2/3·H·A / min(H)·A · Shi 2019 σ_y,SE 2 GPa 가 이 논문의 **경도 1.9 GPa (큐브 코너 20 mN · 덩어리 유리)** 를 그대로 (항복으로) 썼다 — 이 논문이 준 값 1 개 · 맞춘 값 0 | 카드 §0-1 2차 인용 표 · §8 후보 C′ | [인쇄] (원 값) · [카드 해석] (정의 전환) | 경도 ≠ 항복 · 같은 계 경도 0.55–1.9 GPa 로 갈림

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

이 배치에 없음.

## g — 2D → 3D 경고 · 증거

이 배치에 없음 (3D 실물 실험 · 2D · 3D 에 대한 말 없음).

## h — DEM → FE · MPM 으로 넘긴 선례 · 시점

이 배치에 없음.

## i — 복합 양극 (AM + SE) 압력별 기공

이 배치에 없음 (그림 4 의 복합 양극은 모식뿐).

## j — 카드가 스스로 적은 한계 (가압 · 탈압과 닿는 것)

- [j] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | 저자: *"additional information such as the interfacial mechanical properties and defect population are necessary to predict modes of failure"* (p.7) · K 법 = *"best considered as an approximation of the plane strain, Mode I tensile fracture toughness"* (p.12) · Vickers 는 기름에 못 잠금 · 30 분 넘으면 산화 산물 (p.11) · 구조 (단범위 질서 · 나노결정) 미해결 (p.5) | 카드 §3-10 · §11 1–4 | [인쇄] | 가압 · 탈압 자체는 다루지 않음
- [j] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | 원문 안 어긋남: 초록 = 세 값 모두 *"instrumented nanoindentation"* ↔ K 는 Vickers 미세압입 · 풀림 150 °C = p.4 *"slightly below"* ↔ p.8 *"well below … ~220 °C"* · 서론 *"~20 GPa[8]"* (Sakuda) ↔ 측정 18.5 · Fig. 2a 윤곽으로 낸 Vickers 경도 ≈1.1–1.2 GPa < 식 (4) 에 넣은 H 1.9 [판독 + 카드 산술 · 원인 미분리] | 카드 §3-5 · §3-10 5 · §11 8 · §11 10 | [인쇄] · [판독] | —

## k — DEM 의 한계 (인용 서지 병기)

- [k] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation (McGrogan et al. 2017 · Adv. Energy Mater. 7, 1602011) | **말 없음** — DEM · discrete · particle · simulation 0 회.  모델 언급 두 문장뿐: *"These measurements provide an improved understanding of sulfide electrolyte mechanical properties necessary for predictive modeling of elastic stress distributions and fracture conditions in solid state battery structures."* (p.3) · *"the present results are a significant step towards understanding, modeling, and designing all-solid-state batteries for electro-chemo-mechanical reliability."* (p.7) | 카드 §4-3 ① | [인쇄] | 측정 논문
- [k] 같은 논문 | 간접 (카드 해석): 우리 DEM (구 · hooke/hysteresis · 연화 E_eff 1.35) 과 문헌 DEM (Shi 2019 · So 2021/2022) 의 입력 E · H 가 이 유리 한 편에서 왔다 — 문헌 DEM 이 쓴 "E 18.5 · σ_y 2 / H 1.9" 는 **ν 가정 · 경도를 항복으로** 바꾼 값 | 카드 §0-1 · §7-3 · §8 후보 D0 | [카드 해석] | DEM 한계의 직접 근거는 아님

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation (McGrogan et al. 2017 · Adv. Energy Mater. 7, 1602011) | **말 없음** (계산 없음).  소성 쪽 자료는 경도 하나 (*"plastic and fracture properties"* p.5) · 항복 · 가공 경화 · 속도 의존 없음.  주는 사실: *"Thus, overall this solid electrolyte is elastically compliant with relatively low resistance to reversible deformation, while also brittle with low resistance to fracture."* (p.5) · *"the low KIc of LPS also means that brittle fracture could occur at lower stresses, depending on details of defect size and population"* (p.7) → 무른 SE 를 "소성 흐름으로 빈틈을 채우는 재료" 로만 두면 **파괴라는 다른 출구** 를 빠뜨린다 [카드 해석] — 우리 DEM (SE 파괴 없음) · MPM (J2 · 취성 없음) 둘 다 해당 | 카드 §3-9 · §4-3 ② · §8 후보 A · A′ | [인쇄] · [카드 해석] | 유리 70:30 · 압밀 미다룸 · 맞춘 값 · 계산 비용 해당 없음

## m — 받아들일 통찰

- [m] mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation | **무엇**: 문헌 SE 물성을 받을 때 원장 칸에 '원 정의 (경도/항복 · 나노/미세압입) · 재료 (조성 · 결정/유리) · ν 가정 · 하중 · 시편 밀도' 를 필수로 · **어디**: 단계 0; 결과 전 대조 항목 · **왜**: 이 한 편의 값이 문헌을 옮겨 다니며 경도→"항복" (Shi 2019 · So) · Vickers→"나노압입" (bucci2017 · song2025 표) · 70:30→"75:25" (li2026 리뷰 표) · Sakuda 인용 "~20 GPa"→"McGrogan 측정" (du2022) 으로 바뀜 | 카드 §0-1 2차 인용 표 · §9 1 | [인쇄] 대조 | —
- [m] 같은 논문 | **무엇**: A10 CZM 앵커 "Bucci G_c 2.8 ± 1.8" 의 꼬리표 = 70:30 유리 · 풀린 시편 · Vickers 근사의 K²/E (평면응력 2.86 · 평면변형 2.60 · 안 풀림 6.25 / 5.69 J/m²) · ±1.8 은 원문 표준편차로 재현 안 됨 (±1.0) · **어디**: 흐름 밖: 사이클 열화 (A10 · backlog D6) · **왜**: 카드 §3-5 · §7-3 | [카드 산술] | Li₆PS₅Cl 벌크 실측 (song2025 5.31/6.15) 과 나란히
- [m] 같은 논문 | **무엇**: 압입 E 는 ν 가정의 함수 (0.3 → 18.5 · 0.36 → 17.7 GPa) — 물성 행 (DFT ν 0.360) 과 설정값 (DEM ν 0.3) 을 나눠 적는다 · **어디**: 단계 4; 조건 R5 · **왜**: 식 (2) · 카드 §3-4 | [카드 산술] | —
- [m] 같은 논문 | **무엇**: 공기 민감 SE 압입 셋업 — 광유 침지 유체 셀 + 지렛대 팔 (E · H) · 기름 막 + 15–30 분 창 (Vickers) · 건식 기체 퍼지는 실패 · **어디**: 흐름 밖: 실험 측 원측정 요청 (같은 시료의 경도 · 인성) · **왜**: 원고 p.9–11 · 카드 §3-3 · §3-5 | [인쇄] | —

## n — 논문 에이전트 후보

- [n] A. Sakuda, A. Hayashi, Y. Takigawa, K. Higashi, M. Tatsumisago, J. Ceram. Soc. Japan 2013, 121, 946. (원문 ref [8]) | c · k — 이 논문이 E · G 환산에 넣은 **ν 0.3** 과 서론 **"~20 GPa"** 의 출처 (du2022 · famprikis2019 의 "황화물 ≈20 GPa" 관용구의 끝) · 초음파 + 압축 시험 | litdb 확인: `ls` 에 sakuda2013_sulfide_mechanical_property 하나 (Sci. Rep. 3, 2261 — **다른 논문**) · "Takigawa" grep = janek2016 · papakyriakou2021 (인용만) → 카드 없음
- [n] G. R. Anstis, P. Chantikul, B. R. Lawn, D. B. Marshall, J. Am. Ceram. Soc. 1981, 64, 533. (원문 ref [12]) | c · R7 — 식 (4) K = k(E/H)^½P/c^{3/2} · k 0.016 의 원전 (적용 조건 · 균열 꼴) — 우리 SE · AM 파괴 입력의 측정법 원전 | litdb 확인: `ls` anstis* 없음 · "Anstis" grep 0 건 → 카드 없음
- [n] J. G. Swallow, W. H. Woodford, F. P. McGrogan, N. Ferralis, Y.-M. Chiang, K. J. Van Vliet, J. Electrochem. Soc. 2014, 161, F3084. (원문 ref [19]) | c · R7 — 그림 4 LiCoO₂ E 178 · H 8.3 · K 0.94 → 0.25 (탈리튬) = 활물질 인성의 리튬 함량 의존 | litdb 확인: `ls` swallow* 없음 · "F3084" grep = stallard2022 · xu2017 (인용만) → 카드 없음
- [n] M. Qu, W. H. Woodford, J. M. Maloney, W. C. Carter, Y.-M. Chiang, K. J. Van Vliet, Adv. Energy Mater. 2012, 2, 940. (원문 ref [33]) | c · R7 — 팝인으로 Li 삽입 전극의 파괴 인성을 재는 법 (이 논문이 SE 에서 시도했다가 못 쓴 방법) | litdb 확인: `ls` qu20* 없음 · "Maloney" grep = sharma2023 · stallard2022 (인용만) → 카드 없음
- [n] W. C. Oliver, G. M. Pharr, J. Mater. Res. 2004, 19, 3. (원문 ref [30]) | b · c · U3 — 식 (1) 해석법 (제하 기울기 · 면적 함수) 의 원전 · U3 (눌렀다 떼기) 판독 정의 | litdb 확인: `ls` oliver* · pharr* 없음 · "Oliver … Pharr … 2004" grep 0 건 → 카드 없음

## 카드 문제

(원문을 직접 읽고 정본 카드의 2 차 인용을 대조해 본 것 — 어느 카드도 고치지 않았다.)

1. `famprikis2019_fundamentals_inorganic_sse` L112 · L429 · L522–523 · L606 — G ≈ 7 GPa 를 "나노인덴테이션 실측" 으로 적음 ↔ 원문 G 7.1 ± 0.3 은 **ν 0.3 가정 계산값** · L522 "DFT E_VRH 22.06 과 +10 % 정합" 은 반올림 E 20 기준 (원문 18.5 이면 1.19 배) · L606 "+ 시편 밀도" ↔ 원문에 밀도 없음.
2. `du2022_lmro_lpscl_reversible_redox_assb` L406 · L497–498 — "≈20 GPa 의 출처는 McGrogan 유리 나노인덴테이션" ↔ McGrogan 의 "~20 GPa" 는 서론 문장 (p.2) 이고 그 인용은 **Sakuda [8] (J. Ceram. Soc. Jpn. 2013)** · 측정은 18.5 ± 0.9 (출처 사슬 한 단 더).
3. `shi2019_high_am_loading_particle_size_assb` L19 · L120 · L176 · L337–341 · L434 — ν_SE 0.3 · σ_y,SE 2 GPa 를 [1] McGrogan 으로 귀속 ↔ 원문은 ν 를 가정 (Sakuda [8]) · 항복 세기 없음 (H 1.9 ± 0.2 = P_max/A) — Shi 원문의 귀속을 카드가 그대로 옮긴 것 (L185 의 추정 "2 = H 1.9" 은 맞다).
4. `song2025_porous_argyrodite_modulus_fracture_toughness` L84 — K 0.23 ± 0.04 의 방법을 "나노압입" 으로 적음 ↔ 원문 K 는 **Vickers 9.8 N 미세압입** (E 만 계기 압입) · 값은 같다.
5. `bucci2017_chemomech_failure_assb_cycling_czm` L260 (· `xu2017_…` L307 경유) — K 를 "nanoindentation" 으로 · G_c "2.8 ± 1.8" ↔ 원문 표준편차만으로 전파하면 ±1.0 (평면응력 2.86) — ±1.8 의 산출은 Bucci 원문 확인 필요.
6. `li2026_electrochemomechanical_coupling_asslmb_review` L54 — 리뷰 표 3 의 "75Li₂S–25P₂S₅ 유리" 행에 McGrogan 70:30 값 (G 7.1 · H 1.9 · K 0.23) — 조성 표기 다름 (리뷰의 문제를 카드가 그대로 옮김).
7. 후보 표 N-3 의 '왜' 칸 — "그 값들은 song2025 카드가 … 숫자를 옮기지 않음" ↔ song2025 L84 는 E 18.5 ± 0.9 · K 0.23 ± 0.04 를 표에 옮겨 적었다 (2 차 인용 표지 + L91 "원문 확인 전 인용 금지").
8. `faka2026_particle_size_consolidation_strain_lpscl` L110 — DEM Li₆PS₅Cl "Y 18.5 GPa · ν 0.3" (행 끝 "(출처 Alabdali 2024)") 은 McGrogan 70:30 유리의 E · 가정 ν 와 같은 숫자 짝 — 사슬 [미확인] (같은 수라는 사실만 · 문제로 단정하지 않음).
