# batch 73 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `thorntonyin1991_oblique_impact_elastic_spheres_adhesion` — C. Thornton, K. K. Yin, "Impact of elastic spheres with and without adhesion", *Powder Technology* 65 (1991) 153–166 · DOI [미확인 — 원문에 인쇄 없음 · PDF 문서 정보 PII 0032-5910(91)80178-L] (후보 표 N-33 · 가리킨 카드 = `pfeffer2001_dry_particle_coating_engineered_particulates` L302).
같은 탄성 구 두 개 (R 100 µm · E 70 GPa · ν 0.3 · μ 0.35 · 재료 이름 없음) 의 비스듬한 충돌을 Hertz + Mindlin–Deresiewicz 증분 접선 법칙 (Thornton–Randall 규칙) 으로 계산하고, JKR 접착 (γ 0.2 J/m²) 에는 Savkoor–Briggs 벗김 뒤 T = μ(P + 2Pc) 로 미끄러진다는 새 기준을 세워 PET 단섬유 마찰 실험 (Pc 1.6 µN) 과 대조한 14 쪽 논문 — **탄성 전용 · 감쇠 0 · 압밀 · 다입자 0**.
쪽 = PDF 쪽 n = 학술지 쪽 152 + n · SI 없음 · 쪽마다 스캔 (인용은 300 dpi 크롭으로 확인).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 없음 · 압축 없음 · 기공 보고 0).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 압밀 · 하중 제거 계산이 없다.  참고 (b 아님): 충돌 한 번 안에서 *"the work done by the normal force is fully recovered at the end of the impact"* (p.4 · 탄성 · 감쇠 0) · 접선 (전단) 일은 일부만 돌아온다 (그림 5 · θ 60° 끝 전단 일 ≈ 0.0055 nJ / 처음 운동 에너지 0.0277 nJ [판독]) | 카드 §3-2 · §4-8 (iv).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 탄성 (Hertz · JKR) + 마찰 (μ 0.35) 뿐 · 항복 · 경도 · 크리프 정의 0 (*"plastic deformation at the contact is not considered"* p.1).  참고 (c 아님): 이 계산의 최대 Hertz 압력 p₀ = 0.625 GPa (θ 0° · 탄성 가정) [카드 산술 §14-1] — 항복 값이 아니다.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (같은 구 두 개 · 한 재료).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 깨지는 범위 = **없음** (두 구 · 탄성 · 최대 접근량 ÷ 반지름 3.26 × 10⁻⁴ [카드 산술 §14-1]).  이 논문이 주는 대안은 **접선 · 접착 쪽**: 식 (42) T = μ(P + 2Pc) (벗김 뒤 · 새) · 식 (52) T = μP′[1 − (P′ − P)/(3P′)]^{3/2} (P < −0.3Pc · 반지름이 r₀ 로 줄 때) · Kendall 식 (53) T = μP′ | 카드 §4-6 · §4-7 · p.9–11 · `eq_42` · `eq_52` · `eq_53` | [인쇄] | 탄성 · 큰 변형 0
- [e] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 맞춘 값 수: 계산 = **0** (R · ρ · E · ν · μ · γ 고정 입력 · p.3 · p.11) · 실험 대조 = 기준마다 **μ 하나** (식 42 → 0.35 · 식 52 → 0.30 · *"assuming values of"* · 고른 방법 서술 없음) · Pc 1.6 µN 은 실험 실측 | 카드 §3-4 · p.10–11 | [인쇄] | 실험 = 정적 마찰 (충돌 아님) · 기하 · E 미기재
- [e] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 접선 이력 법칙: Mindlin–Deresiewicz 를 증분으로 (식 7–15 · θ 로 미끄럼 고리 크기 · 되돌림 점 T\* · T\*\* 를 μΔP 로 갱신 · 예외 경우 θ = 1) → 강체 미끄럼 전 미세 미끄럼 소산 (그림 4b · 15°).  ↔ LIGGGHTS `tangential history` = k_t = 8G*√(R*δn) (= 이 논문 식 18 처음 강성) + Coulomb 자름 [다른 카드 boschpadros2014 L186 · L192] — θ 규칙 없음 [카드 해석] | 카드 §4-2 · §7-3 | [인쇄] · [카드 해석] | 우리 덱 접선 설정은 카드가 보지 않음
- [e] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 접착 법선 선택 규칙: JKR Pc = 3πγR* · DMT 4πγR* (γ = *"the surface energy of each solid"*) · Muller 변수 μ = (32/(3πz₀))(γ²R*/E*²)^{1/3} 가 3 보다 크면 JKR · 1 보다 작으면 DMT 가 10 % 안 (p.7) — 이 계산의 z₀ 없음 → 판정 불가 [미확인] · E 를 18 배 무르게 하면 이 변수 × 6.87 (JKR 쪽) [카드 산술 §14-7] | 카드 §4-4 · `eq_19`–`eq_21` | [인쇄] · [카드 산술] | 값 전이 0

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 아님).  참고 (f 아님): 입자별 속도장 MPM (A′) 의 다물체 마찰 접촉 검증 표적으로 쓸 수 있는 두 구 충돌 표 (그림 6 · 8 · 15 · 17 · digitized.csv) — 접착 없음은 *"independent of impact velocity"* (p.12).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 접촉식은 구 (3D 해) · 충돌 운동은 한 평면 (그림 3 · 7) · 프로그램이 2D 인지 3D 인지 [미확인] · 2D → 3D 서술 없음 (카드 §4-8 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 저자 한계: *"The resulting theory, however, is not a rigorous solution, due to the approximations in existing theories and the speculative nature of the proposed sliding criteria."* · *"The authors are not aware of any experimental work that can confirm or deny this possibility."* (되튐) · *"need for detailed experimental observations of oblique impacts of micron-sized particles at low impact velocities"* (p.14) · 붙음은 *"the subject of a subsequent paper"* (p.13) | 카드 §4-9 | [인쇄] | 가압 · 탈압과는 '접착 접촉의 떨어짐 (Pc · Tc) 규칙' 으로만 닿는다
- [j] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 이론 안의 한계: r₀ ≥ a* 가정이 P < −0.3Pc 에서 깨짐 (p.10 · 카드 산술 교차 n = −0.325) · 반지름이 r₀ 로 준다고 보면 *"the correlation with the experimental results would be much improved, especially when the normal contact force is negative"* · 식 (52) 는 벗김 기준 식 (40) 과 *"not consistent"* · 비선형 접선 해석은 *"intractable"* (p.11) | 카드 §4-7 · §14-4 | [인쇄] · [카드 산술] | 탄성 · 정적
- [j] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 카드가 남긴 미확인: DOI · 재료 이름 · 시간 간격 · 사이클 · 2D/3D · 붙는 속도 식 · 값 · 반발 계수 곡선 · 그림 9–11 매개변수 (그림 11 peel 선은 ν 0.3 식보다 1–6 % 아래 · G*/E* 0.183 이면 맞음 [카드 산술]) · z₀ · PET 시편 기하 · Maw 실험 수치 | 카드 §11-1 | — | —

## k — DEM 의 한계
- [k] thorntonyin1991_oblique_impact_elastic_spheres_adhesion — Thornton & Yin 1991 (Powder Technol. 65, 153–166) | 선형 스프링 · 대시팟 DEM 을 접촉역학 법칙으로 바꾼 동기: *"The programme originally used linear springs and dashpots to model the interactions between contiguous particles but, motivated by problems associated with process engineering, more realistic algorithms based on contact mechanics theories have been incorporated [2, 3]."* · *"When dealing with large systems of particles, using either analytical or numerical models, it is essential that energy is dissipated in as natural a way as possible."* | p.1 · `txt_p1_intro_cundall_strack_linear_springs_single_impact_validation.png` | [인쇄] | 두 구 충돌 맥락
- [k] thorntonyin1991_oblique_impact_elastic_spheres_adhesion — Thornton & Yin 1991 (Powder Technol. 65, 153–166) | 반발 계수 같은 간단한 규칙의 한계: *"The results of the computer-simulated impacts show that, as a result of the complex tangential load-displacement behaviour, there would appear to be no simple rules (e.g., coefficients of restitution, scattering probability) that will satisfactorily achieve this."* — 우리 LIGGGHTS 의 반발 계수 → 점성 감쇠가 그 '간단한 규칙' 쪽 [카드 해석] | p.13 · `txt_p13_p14_conclusion_…` | [인쇄] | 탄성 구 두 개 · 입자 수송 문제 맥락
- [k] thorntonyin1991_oblique_impact_elastic_spheres_adhesion — Thornton & Yin 1991 | 접착 접촉 이론 자체의 근사: *"Horn et al. [13] point out that the complete solution is very difficult, since the stress distribution in the spheres depends on the surface interaction, which depends on the exact shape of the deformed surfaces, which is only known if the stress distribution is known."* (p.7) · *"A rigorous analysis accounting for the non-linear tangential response would appear to be intractable."* (p.11) | `txt_p7_…` · `txt_p11_…` | [인쇄] | —
- [k] thorntonyin1991_oblique_impact_elastic_spheres_adhesion — Thornton & Yin 1991 | 단단한 구 · 점접촉 · 접촉 독립 가정이 조밀 영역에서 깨진다는 문장 = **말 없음** (두 구 충돌 논문) | 카드 §4-8 (i) | — | —

## l — 소성변형이 왜 어려운가
- [l] thorntonyin1991_oblique_impact_elastic_spheres_adhesion — Thornton & Yin 1991 (Powder Technol. 65, 153–166) | 이유 = **말 없음** — *"Although the work presented is restricted to elastic spheres (plastic deformation at the contact is not considered), the purpose of the paper is to illustrate the effect of oblique impact on the dissipation and redistribution of energy."* (p.1) 로 범위만 자른다 · 우회 · 맞춘 값 · 비용 서술 0 (탄성 Hertz · JKR 그대로 · E 70 GPa 연화 없음).  같은 그룹의 법선 소성 법칙 = 7 년 뒤 Thornton–Ning 1998 [다른 카드 `thorntonning1998_…`] | p.1 · `txt_p1_elastic_spheres_only_plastic_not_considered.png` · 카드 §4-8 (ii) | [인쇄] | ⚠ pfeffer2001 L302 의 '탄소성 접촉' 표기는 이 원문과 다르다 (카드 문제)

## m — 받아들일 통찰
- [m] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 무엇: **U5 표적 — 같은 탄성 구 두 개 비스듬한 충돌의 θ 별 에너지 · 반발각 지도** (그림 6 · 8 · 15 · 17 · digitized.csv 248 행 · 접착 없음은 *"independent of impact velocity"* p.12 → 계산하기 쉬운 속도로 돌려도 같은 표적) · 어디에: U5 · 후보 A′ (입자별 속도장 MPM 다물체 마찰 접촉) · 후보 D0 (접선 법칙 점검) · 왜: 결과가 μ · ν 만의 함수이고 Hertz 산술 (P_max · 접촉 시간) 과 그림 4 · 5 가 맞음을 카드가 재현했다 (카드 §14-1)
- [m] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 무엇: **영 점검** — γ = 0 이면 JKR 식 (25) = Hertz 식 (2) · 식 (42) = μP → 점착 코드의 γ = 0 판이 접착 없음 결과와 같아야 한다 (논문은 같은 입력에서 γ 만 0 ↔ 0.2 로 바꾼 비교 = 그림 6 ↔ 17 · 그림 15) · 어디에: U0 · 단계 3 의 '한 매개변수만 바꾼 비교' 꼴 · 왜: 카드 §8 (원문에 γ = 0 시험 서술은 없음 [카드 해석])
- [m] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 무엇: **우리 DEM 접선 법칙 점검** — LIGGGHTS `tangential history` 는 이 논문 식 (18) 의 처음 강성 8G*a 를 늘 쓰고 Coulomb 으로 자른다 [다른 카드 boschpadros2014 L186 · L192] → Mindlin–Deresiewicz 의 미세 미끄럼 (θ) 소산 · 되돌림 기억이 없다 [카드 해석] · 반발 계수 감쇠는 저자 결론의 *"no simple rules"* 쪽 · 어디에: 후보 D0 (압밀 · 믹서 덱 각각) · 왜: 그림 4b (15°) 의 미끄럼 전 소산 고리 (p.4) · ⚠ boschpadros L187 의 G* 꼴은 이 논문 식 (10) 과 다르다 (카드 문제 관찰)
- [m] thorntonyin1991_oblique_impact_elastic_spheres_adhesion | 무엇: **'붙는 속도' 의 식 꼴 표지** — JKR 꼴 (TN1998 식 54 [다른 카드]: V_s ∝ Γ^{5/6}R^{−5/6}E*^{−1/3}ρ^{−1/2} · 포획 에너지 = 접착 이력 고리 · 닿을 때 −8Pc/9 로 뛰어듦) ↔ SJKR (힘 = CED × 겹침 면적 · 겹침의 한 값 함수 → 고리 넓이 0 → 붙음은 감쇠가 정함 [카드 해석]) · 연화 E ÷ 18 → JKR 꼴이면 V_s × 2.62 [카드 산술] · 어디에: 흐름 밖: 믹서 dev-u 의 *"SE–SE 붙는 속도 상한 18.7 · 46.6 mm/s (벽 103 · 지금 모델 0.16)"* [우리 · CLAUDE.md] 문장 · 왜: 이 논문 자체는 식 · 값을 주지 않고 (p.13) 이 입력의 정면 소산 [판독] 0.7–1.1 % 가 JKR 꼴 0.90 % 와 맞는다 (카드 §14-6) · johnson1971 L222 의 [추정] 과 같은 방향

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] J. Reed, in B. J. Briscoe and M. J. Adams (eds.), Tribology in Particulate Technology, Adam Hilger, Bristol, 1987, p. 123. (원문 참고문헌 21 · 인쇄 그대로) | m · e (흐름 밖: 믹서) — 정면 접착 충돌의 **붙는 임계 속도 (JKR)** 를 이 논문이 넘긴 곳 (*"see Reed [21]"* p.13) · 우리 dev-u 붙는 속도 식 꼴 대조 · 카드 §7-4 · §12 | litdb 확인: `papers/` 파일 목록 (551 · 이 카드 전) + grep "Tribology in Particulate" 0 건 · 'Reed' 카드는 다른 Reed (세라믹 · cottrino2013 인용) → 카드 없음
- [n] A. R. Savkoor and G. A. D. Briggs, Proc. Roy. Soc. Lond., A. 356 (1977) 103. (원문 참고문헌 18 · 인쇄 그대로) | e · R2 — 접착 접촉이 접선력으로 벗겨지는 (Tc) 원전 · 이 논문 새 기준의 바탕 · 카드 §4-5 · §12 | litdb 확인: grep "Savkoor" 0 건 → 카드 없음
- [n] R. D. Mindlin and H. Deresiewicz, J. Appl. Mech., Trans. ASME, 20 (1953) 327. (원문 참고문헌 6 · 인쇄 그대로) | e · m · U2 — 접선 이력 법칙의 원전 (우리 LIGGGHTS 접선 법칙 점검 · D0) · 카드 §4-2 · §12 | litdb 확인: 파일 목록에 mindlin* 없음 · 'Deresiewicz' 는 여덟 카드에 인용만 (asylbekov2023 · boschpadros2014 · chandratilleke2010 · chibwe2020 · huang2025 · jadidi2023 · pfeffer2001 · tovar2026) → 카드 없음
- [n] N. Maw, J. R. Barber and J. N. Fawcett, J. Lubrication Tech., Trans. ASME, 103 (1981) 74. (원문 참고문헌 9 · 인쇄 그대로) | m · U5 — 비스듬한 충돌 실험 (공기 받침 위 퍽 · 스트로보 · 접촉점 되튐) · 이 논문 초록이 *"excellent agreement"* 라 한 실험 (본문 그림에는 실험점 없음) · 카드 §3-2 · §11 | litdb 확인: grep "Maw" 0 건 → 카드 없음
- [n] C. Thornton and C. W. Randall, in M. Satake and J. T. Jenkins (eds.), Micromechanics of Granular Materials, Elsevier, Amsterdam, 1988, p. 133. (원문 참고문헌 2 · 인쇄 그대로) | e · m — 증분 접선 규칙 (식 7–15) 의 원전 · `ai2011_rolling_resistance_contact_models_dem` 이 인용한 Δt_crit 식 (21)–(22) 의 출처 · 카드 §4-2 · §12 | litdb 확인: grep "Randall" = ai2011 의 인용 줄뿐 → 카드 없음
- (참고 · 후보로 세지 않음) [20] B. J. Briscoe and S. L. Kremnitzer, J. Phys. D: Appl. Phys., 12 (1979) 505 (실험 원자료 · Pc 1.6 µN) · [8] Maw et al., Wear, 38 (1976) 101 (되튐 이론) · [19] K. Kendall, Nature, 319 (1986) 203 · [14] Muller et al., J. Colloid Interface Sci., 77 (1980) 91 — 모두 정본에 카드 없음 (카드 §12).

## 카드 문제
- `pfeffer2001_dry_particle_coating_engineered_particulates` **L302** (가리킨 줄): *"\| 117 \| C. Thornton, K.K. Yin, Powder Technol. 65 (1991) 153–166. \| 탄소성 접촉 — 카드 없음 \|"* — 서지 (저자 · 학술지 · 권 · 쪽 · 연도) ✓ · 제목 없음.  **'탄소성 접촉' 은 원문과 다르다**: 원문 = *"restricted to elastic spheres (plastic deformation at the contact is not considered)"* (p.1) · 제목 *"Impact of elastic spheres with and without adhesion"* — 탄소성 접촉 법칙은 같은 그룹의 Thornton–Ning 1998 (`thorntonning1998_adhesive_elastoplastic_contact`) 이다.  그 카드 본문에 [117] 을 쓰는 줄은 없다 (grep '117' = L302 한 줄) → 원 논문 (Pfeffer 2001) 이 [117] 을 어떤 뜻으로 인용했는지는 [미확인].
- (참고 · 문제 아님) `tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond` L86 · L87 · L343 ✓ — Mindlin–Deresiewicz 접선 이력 · Coulomb 미끄럼 · 접촉 강성 K_c = 원문과 맞음.  L87 의 감쇠 식 (21)(22) 는 이 논문에 없으나 (감쇠 0) 그 카드는 강성만 [47] 로 돌린다.
- (관찰 · 가리킨 카드 아님 · 고치지 않음) `boschpadros2014_dem_liggghts_msc_thesis` **L187**: *"1/G* = 2(2+ν₁)(1−ν₁)/Y₁ + 2(2+ν₂)(1−ν₂)/Y₂ (4.7)"* ↔ 이 논문 식 (10) 1/G* = (2−ν₁)/G₁ + (2−ν₂)/G₂ = 2(2−ν₁)(1+ν₁)/E₁ + … [카드 산술 · G = E/(2(1+ν))] — 꼴이 다르다 (ν 0.3 에서 몸 하나 몫 3.22/Y ↔ 4.42/E · G* 1.37 배).  thesis 원문 · LIGGGHTS 문서를 이 세션에서 보지 않아 옮김 문제인지 원문 문제인지 [미확인].  (같은 카드 L186 의 k_t = 8G*√(R*δn) 는 이 논문 식 (18) 과 같은 꼴 ✓.)
- (관찰 · 원문 자체의 어긋남 — 카드 §11 에 기록) 그림 15 캡션 *"contact pitch"* (= patch) · 결론 *"Savkoor and Briggs [5]"* (목록 [5] = Mindlin 1949 → [18]) · 본문 *"positive square root in eqn. (46)"* (± 는 식 45) · Muller 변수와 마찰 계수가 같은 기호 μ · 그림 9 의 α_c 본문 정의 없음 · 그림 2 · 12 는 법선력을 N (본문 P) · 그림 12 의 *"T = μN"* = μ(P + 2Pc) · 그림 6 설명은 *"percentage loss"* 인데 그림 축은 남은 몫 (0–1 · 셋의 합 ≈ 1 [카드 산술]) · 초록의 Maw 실험 *"excellent agreement"* ↔ 본문은 Randall 학위논문 [3] 의 계산과 Maw 이론 [8] 의 일치만 서술.
- (참고 · 카드 아님) 후보 표 `litdb/_curation/S8_candidates.md` N-33 서지 상태 *"일부만 (제목 없음)"* → 원문 제목 *"Impact of elastic spheres with and without adhesion"* · DOI 는 원문에 인쇄되지 않음 (PDF 문서 정보 PII 0032-5910(91)80178-L).
- (참고 · 카드 아님) `litdb/figures/_sources.json`: 이 배치의 `extract_figures.py` 가 다른 카드 줄을 바꿨으나 HEAD 값으로 되돌리고 이 카드 줄만 더했다 (batch_69 · 71 · 72 와 같은 현상).
