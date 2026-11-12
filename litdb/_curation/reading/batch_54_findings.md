# batch 54 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `stallard2022_nmc811_single_crystal_shear_strength_lithiation` — Joe C. Stallard, Sundeep Vema, David S. Hall, Anthony R. Dennis, Megan E. Penrod, Clare P. Grey, Vikram S. Deshpande, Norman A. Fleck, "Effect of Lithiation upon the Shear Strength of NMC811 Single Crystals", J. Electrochem. Soc. 169, 040511 (2022), DOI 10.1149/1945-7111/ac6244 (본문 11 쪽 + SI 1 쪽).
캘린더링 안 한 액체계 LIB 양극 층 (단결정 NMC811 1–3 µm · NMC 54 · 결합제 7 · 기공 39 vol% · 65 µm) 을 경도 50.4–946 MPa 금속 기판 위에 놓고 Vickers 로 깊게 눌러 층 평균 견인력 = 기판 경도 H 를 건 뒤, 뺀 뒤 SEM 으로 슬립 띠 · 균열 입자 분율 F(H) 를 세고 Reuss 응력 + 기저면 단일 슬립 + 방위 분포로 기저면 전단강도 τ_C 를 낸 실험 + 해석 논문.  후보 표 N-12 (c · k · l · 조건 R1 · R7) · `wheatcroft2023_…` [32] · `sharma2023_…` [12] 의 원문 · 같은 제1 저자의 *Joule* 리뷰 (`stallard2022_cathode_mechanical_properties_review`) 와 다른 논문.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 를 다루지 않는다 — 시편은 액체계 LIB 양극 층).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] stallard2022_nmc811_single_crystal_shear_strength_lithiation | 되돌아옴 **없음**.  세기는 **뺀 뒤** SEM 표면 (남는 슬립 띠 · 균열) · 누른 채 값은 in situ CT 층 두께 h(s) 한 시험 (120 N · 균일 구간 38.0 · 40.2 · 39.9 · 48.8 µm ← 처음 65 µm) 뿐 · 뺀 뒤 층 두께 · 탄성 회복 측정 없음 | 카드 §3-4 · §4-4 (4) · p.7 · Fig. 3c | [인쇄] · [판독] | 조건 R4 의 값이 아니다 · SE 없는 다공 층

## c — 항복 · 경도 · 크리프 값과 정의
- [c] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **기저면 임계 분해 전단 τ_C = 86 ± 12 (y = 1) · ≈47 (y = 0.58 · Fig. 7c 만) · 39 ± 5 MPa (y = 0.14)** — 정의: Reuss σ = H/(1 − f) (f 0.46 = 결합제 + 공기) · τ = H sin2φ/(2(1 − f)) · 첫 슬립 H₀ = 2(1 − f)τ_C (H₀ 93 · 51 · 42 MPa) · 맞춤 F − F₀ = (1 − F₀)[1 − ((H/H₀ − α)/(1 − α))²]^½ (α 20 · F₀ 0.12) | 카드 §0 · §3-6 · p.2 · p.10–12 · Fig. 7c · 식 [1]–[6] | [인쇄] · [판독] | 저자 *"upper estimates to the actual values"* (p.11) · 액체계 다공 층 · 뺀 뒤 세기
- [c] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **일축 환산** (카드): σ = 2τ_C/sin2φ → 가장 유리한 방위 (φ = 45°) 개시 **172 · 94 · 78 MPa** (f 0.46) · f → 0 이면 93 · 51 · 42 MPa (= H₀) · 누른 채 CT 두께가 거의 치밀 (65 → 38–40 µm ≈ 고체 두께 39.7 µm) 이라 τ_C(y = 1) ∈ [46.5, 86.1] MPa 로 읽는다 | 카드 §3-4 · §3-6 · §7-2 | [카드 산술] · [판독] | 규약 (고체 분율) 하나가 τ_C 를 1.85 배 바꾼다
- [c] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **경도 ≠ 3σ_y (층상 결정)** — *"The usual interpretation that the macroscopic hardness of a polycrystal equals three times its uniaxial strength is only valid for a crystal that possesses at least 5 slip systems."* (p.3) · 다결정 NMC 2 차입자 압입 경도 5–8 GPa (2 차 인용 [15, 21]) · MAX 상 Ti₃SiC₂ 기저면 CRSS 16.5 MPa ↔ 압축 ≈4 GPa (2 차 인용 [33]) · 크리프 · 속도 의존 없음 (2 µm/s 하나) | 카드 §3-7 · §4-4 (2) · p.3 · p.11 | [인쇄] | 우리 `analyze_tabor_regime.py` σ_y,AM = H/3 에 한정어 거리

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] stallard2022_nmc811_single_crystal_shear_strength_lithiation | 하중 몫 값 **없음**.  모형 = Reuss (모든 결정이 같은 응력) + **재밍 가정** *"the degree of slip on the basal plane is limited by jamming of the slipped particle against its neighbours, so that, post-yield, the particle can bear a shear stress on the basal plane that exceeds τC"* (p.10 · 측정 아님) · 결합제를 기공으로 셈 | 카드 §3-6 · §4-3 · p.10 | [인쇄] | 무른 기지 (SE) 없음 — 결합제 · 기공 층 · 조건 R1 의 근거로는 '가정' 만

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (계산 · 접촉 법칙 없음).  카드 §8 후보 C′ 행: AM 접촉 항복압 p_y 를 경도에서 옮기는 H = 3σ_y 가 층상 결정에선 성립하지 않는다는 원문 근거 (p.3 · p.11) 뿐.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).  카드 §8 후보 A 행: 얼린 AM 가정의 반례 후보 — 단결정 AM 의 가장 유리한 방위 슬립 개시 (일축 172 MPa [카드 산술]) 가 우리 MPM SE 문턱 (일축 0.318 GPa · 보정값) 보다 낮다 (양 · 재료 다름).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] stallard2022_nmc811_single_crystal_shear_strength_lithiation | 실물 3D 층 · 방위 분석은 3D (구면 좌표 · 횡등방 p(φ)) · 세기는 **표면 SEM 2D 관찰** (표면에 보이는 슬립 띠 · 균열만 셈) · 2D ↔ 3D 전이에 대한 말 없음 | 카드 §4-4 (3) · §4-3 · p.8–10 | [인쇄] | 보이지 않는 슬립의 비율 [미확인]

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (SE 없는 액체계 LIB 층 · 압력별 기공 곡선 없음 — 누른 채 CT 두께 한 시험뿐).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] stallard2022_nmc811_single_crystal_shear_strength_lithiation | 입자 응력 = Reuss + 처음 기공 f 0.46 (누른 채 거의 치밀 [판독 Fig. 3c]) · 뺀 뒤 표면 세기 (누르는 동안의 슬립 · 슬립 양 · 하중 몫 · 회복 없음) · 조건마다 압흔 1 개 · 4 장 (반복성은 283 MPa 한 조건 0.49 ± 0.04 뿐) · H₀ 는 아래쪽 시험점 0 · 50.4 · 127 MPa 와 맞춤 모양 (α 공통) 이 정함 · 방위 p(φ) = p(π/2 − φ) 대칭 가정 (c ∥ 하중 / c ⊥ 하중 못 가름) · 슬립 방향 · 온도 · 크기 의존 [미확인] | 카드 §0 한정어 · §11 · §13 | [카드 해석] · [미확인] | 우리 300 MPa 압밀 AM 의 슬립 판정에 바로 쓰지 못하는 이유
- [j] stallard2022_nmc811_single_crystal_shear_strength_lithiation | 원문 안 어긋남: Fig. 3a 하중 12 N (p.7 본문) ↔ 120 N (캡션 · CT 문장) · p(π/4) = (1 − F₀)√(2/(α − 1)) = 0.2855 (p.11) ↔ 그림 7d ≈0.325 = √(2/19) (인쇄된 식 (8) · (10) 에 (1 − F₀) 가 남는 꼴 — 식 (10) 정규화 0.88) · *"several orders of magnitude"* ↔ 58–205 배 · 슬립면 문장 ('parallel to the prismatic direction—that is parallel to the basal plane') | 카드 §3-8 · §3-6 | [카드 산술] · [판독] | τ_C 값 자체에는 영향 없음 (H₀ 만으로 정해진다)

## k — DEM 의 한계
- [k] stallard2022_nmc811_single_crystal_shear_strength_lithiation (Stallard · Vema · Hall · Dennis · Penrod · Grey · Deshpande · Fleck 2022, J. Electrochem. Soc. 169, 040511) | **말 없음** — DEM · discrete · 입자 계산을 쓰지도 언급하지도 않는다 (본문 · SI 0 회).  DEM 한계의 근거 문헌으로 인용할 수 없다.  간접으로 쓸 수 있는 것: AM 을 탄성 구로 두는 가정의 물성 근거가 없었다는 문장 *"The mechanical properties of NMC single crystals have not been reported in the open literature to the best of the authors' knowledge."* (p.2) + 단결정 NMC811 은 기저면 τ_C 39–86 MPa 에서 슬립한다는 실측 | 카드 §4-4 (1) · §0-1 · p.2 | [인쇄] | 액체계 다공 층 · 뺀 뒤 세기 — 우리 AM 탄성 · 강체 가정의 '한정어 인용처' 로만

## l — 소성변형이 왜 어려운가
- [l] stallard2022_nmc811_single_crystal_shear_strength_lithiation (Stallard et al. 2022, J. Electrochem. Soc. 169, 040511) | 층상 산화물 입자 소성은 **슬립계가 모자라 방위 의존 · 매우 이방성** — *"Layered polycrystalline ceramics have a much-reduced availability of slip systems, and consequently their macroscopic hardness may be dictated by the activation of secondary slip systems of slip strength much above that of the basal plane, or by the granular flow of the polycrystalline ceramic after it has suffered extensive fragmentation along its grain boundaries."* (p.3) · *"General yield requires slip on at least 5 independent slip systems, and a high yield strength of the required secondary slip systems results in a hardness (and uniaxial compressive strength) much above that of the basal plane shear strength."* (p.11) · 층의 응력 상태도 모름 *"The precise stress state within the layer depends upon its constitutive response, and this is unknown for the cathode layer."* (p.11) | 카드 §4-4 (2) · p.3 · p.11 | [인쇄] | 우회 = 해석 모형 (Reuss + 단일 슬립 + 방위) · 맞춘 값 = y 마다 H₀ 하나 + 공통 α · 결정 소성 계산 없음 — 계산 비용 해당 없음

## m — 받아들일 통찰
- [m] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **AM 탄성 · 강체 가정의 한정어 + 결과 전 검사** — 단결정 NMC811 기저면 τ_C 86 ± 12 → 39 ± 5 MPa (상한 추정) → DEM (AM E 140 GPa 탄성) · MPM (얼린 AM) 의 AM 에 '소성 · 슬립 미포함' 을 원전으로 달고, real_14 AM_S (단결정) 입자별 Love–Weber 편차 응력 (σ₁ − σ₃)/2 분포를 τ_C 범위 [46.5, 86] MPa 에 대는 판정 문장을 계산 전에 적는다 (방위 무시 = 상한 · 등방 가중 두 꼴 · AM_P 다결정에는 쓰지 않음) | 후보 D0 · 후보 A · 단계 5 · 결과 전 대조 항목 | 카드 §7-2 · §9-1 · §9-2 | 우리 AM 평균 축응력 어림 ≈325–385 MPa 은 축응력이라 판정에 쓰지 않는다 (다이 안 옆 압축)
- [m] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **경도 → 항복 환산 금지 (층상 결정)** — H = 3σ_y 는 독립 슬립계 ≥ 5 일 때만 → `analyze_tabor_regime.py:79-81` σ_y,AM = H/3 (= 2.0 GPa) 과 AM 접촉 항복압을 경도에서 옮기는 안 (후보 C′) 에 한정어 | 후보 C′ · 단계 0 | 카드 §7-1 · §8 · §9-3 · p.3 · p.11 | 대체 값은 이 논문에 없다 (2 차 슬립 강도 미측정)
- [m] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **문헌 강도 값 원장에 '고체 분율 규약 · 누른 채 / 뺀 뒤' 칸** — 같은 자료가 f 0.46 ↔ 0 에서 τ_C 86 ↔ 46.5 MPa · pristine 기준 F₀ (0.12) 를 빼는 보고 꼴 | 단계 0 · 결과 전 대조 항목 | 카드 §0 한정어 · §8 단계 0 | [카드 산술]
- [m] stallard2022_nmc811_single_crystal_shear_strength_lithiation | **실험 쪽 (흐름 밖)** — 경도가 다른 기판 위에서 층을 눌러 평균 압력을 거는 방법 (깊이 > 2–2.5 × 층 두께면 견인력 = 기판 경도 · 박리 없음 확인 · 같은 자리 √A_P/4 에서 세기) 은 우리 건식 복합 양극 층의 AM 손상 분율 vs 압력 실측 (조건 R7 검증) 에 쓸 수 있다 — SE 기지라 견인력 = H 근거를 다시 세워야 한다 | 조건 R7 (실험 대조) · U3 | 카드 §3-3 · §9-5 · p.6–8 | 액체계 다공 층에서만 확인된 규칙

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Y. Bi et al., Science, 370, 1313 (2020). (원문 참고 [20] · 인쇄 그대로 · 제목은 목록에 없음) | c · m · 조건 R7 — 단결정 NMC811 이 전기화학 사이클 중 슬립 띠를 내고 계산 전단응력이 *"did not exceed a few hundred MPa"* (p.3) — 이 논문의 동기 · 사이클 슬립의 원전 (A10) | papers/ 목록 + "370, 1313" grep — 카드 없음 (`kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` 이 인용만)
- [n] L. Feng, X. Lu, T. Zhao, and S. Dillon, J. Am. Ceram. Soc., 102, 372 (2019). (원문 참고 [19] · 인쇄 그대로) | c · l — LCO 단결정 기둥 압축 2–4 GPa · 두 변형 모드 (기울어진 면 전단 2 GPa ↔ 균일 전위 소성 4 GPa) = 층상 산화물 단결정 항복의 1 차 자료 (이 논문 p.2–3 의 해석 출발점) | papers/ 목록 + "102, 372" grep — 카드 없음 (`feng2020_li_deficient_argyrodite_cl_disorder` 는 다른 논문)
- [n] V. S. Deshpande and N. A. Fleck, J. Mech. Phys. Solids, 48, 1253 (2000). (원문 참고 [34] · 인쇄 그대로) | e · 후보 M0 — 다공 발포 금속의 등방 구성식 · 'plastic Poisson ratio ≈ 0' (일축 응력 → 일축 변형) 의 근거 = 이 논문 τ_C '상한' 의 원인 가정 · 캡 · 다공체 소성 모형의 원형 | papers/ 목록 + "48, 1253" grep — 카드 없음
- [n] A. K. Bhattacharya and W. D. Nix, Int. J. Solids Struct., 24, 1287 (1988). (원문 참고 [29] · 인쇄 그대로) | U3 · m — 박막 + 기판 압입에서 깊이 > 막 두께 2 배면 막 위 평균 견인력 ≈ 기판 경도 (이 시험법의 근거 규칙) · '층 + 기판 누르기' 단위 시험의 해석 짝 | papers/ 목록 + "24, 1287" grep — 카드 없음
- [n] K. Märker, P. J. Reeves, C. Xu, K. J. Griffith, and C. P. Grey, Chem. Mater., 31, 2545 (2017). (원문 참고 [18] · 인쇄 그대로 — 연도 표기 원문 그대로 · 확인 [미확인]) | c · A10 — NMC811 첫 충전의 c/c₀ · a/a₀ vs 리튬 함량 (Fig. 1b 의 원전) · 이 논문 리튬화 시편 (C/20 · 3.8 · 4.4 V) 의 전지 조건 | papers/ 목록 + "31, 2545" grep — 카드 없음
- (참고 · 후보로 세지 않음) 원문 참고 [5] T. M. M. Heenan et al., Adv. Energy Mater., 10, 2002655 (2020) = **후보 표 N-20 에 이미 있다** · [15] L. S. de Vasconcelos, N. Sharma, R. Xu, and K. Zhao, Exp. Mech., 59, 337 (2019) = **후보 표 N-24 에 이미 있다** · [21] R. Xu et al. JES 164, A3333 (2017) · [13] E. Trevisanello et al. Adv. Energy Mater. 11, 2003400 (2021) = 정본 카드 있음 (`xu2017_…` · `trevisanello2021_…`) · [22] Hill 1950 = 교과서.

## 카드 문제
- `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` L191 — *"(값 없음) 리튬화가 NMC811 단결정의 전단강도에 미치는 영향 · 캘린더링 슬립/전단띠 | NMC811 단결정 | [12] … | 미확인"*: 서지 · 주제는 원문과 같다.  다른 점 ① **"전단띠"** — 원문 낱말은 *"slip bands"* (본문 14 회) · "shear band" 0 회 ② **"캘린더링 슬립"** — 시편은 **캘린더링 안 한 층** (*"tape cast but uncalendered"*, p.3) · 캘린더링은 초록 · 결론의 함의 문장뿐 (*"for example by calendering during manufacture"* · *"e.g., via a calendaring operation"*) · 캘린더링 압력 · 시험 없음 ③ **"(값 없음)"** — 원문엔 τ_C 86 ± 12 → 39 ± 5 MPa (p.2 · p.12) 가 있다 → 의도 대조 '일부' · 고치지 않음 (이 카드로 "미확인" 이 풀리는 갱신 거리).
- `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` L196 — *"단결정 NMC811 탈리튬 시 1차입자 전단강도 감소 | p. 7 | [32] …"*: 서지 (저자 8 명 · JES 2022 · 169 · 040511) · 방향 모두 원문과 **같다** — 문제 아님 ('1차입자' = 단결정 입자 그 자체).
- **낡은 "카드 없음 · 미확인" 표기**: 후보 표 N-12 행과 가리킨 카드 둘 (sharma2023 L191 '미확인' · wheatcroft2023 L196) 이 이 논문을 인용만으로 적는다 — 이 카드가 생겨 낡음 (고치지 않음).
- 후보 표 (`litdb/_curation/S8_candidates.md`) N-12 행 — 서지 (저자 · J. Electrochem. Soc. · 2022 · 169 · 040511) 는 원문과 같다 · 제목 · DOI 는 원문에서 채움 (*Effect of Lithiation upon the Shear Strength of NMC811 Single Crystals* · 10.1149/1945-7111/ac6244) · '왜' 칸의 "NCM811" 은 원문 표기 NMC811.
- `stallard2022_cathode_mechanical_properties_review` L122 — *"단결정 NMC | — | 없음"*: 리뷰 원문 기준으로는 맞다 (그 카드에 040511 언급 없음) — 문제 아님 · 그 카드 §14 에 관련 카드 한 줄만 더함.
