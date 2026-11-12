<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-33 · 정독 73) 에서 꼭 뽑으라고 한 항목.
     본 = thorntonning1998_adhesive_elastoplastic_contact.md (같은 그룹 · 같은 계보 접촉 법칙 카드 · 메타 줄 · 서지 표 · 그림 표) · 곁 = brodu2015_multiple_contact_dem_dense_granular.md (같은 날 꼴 · 두 필수 절 = §0-1 고른 의도 대조 · §8 자세한 분석).
     원문 = 출판본 (Powder Technology, 65 (1991) 153–166 · 14 쪽 · 보충 자료 없음 · 표 없음).  쪽마다 스캔 한 장 + OCR 글자 층 (글자 층은 숫자 · 기호가 자주 깨짐 — 인용은 300 dpi 렌더로 확인한 글).  쪽 표기 "p.n" = PDF 쪽 n = 학술지 쪽 152 + n.
     값 표지: [인쇄] = 본문 · 그림 안 글자로 적힌 값 · [판독] = 스캔 그림에서 읽은 값 (눈금 보정 + 표지 무게중심 · 겹친 표지는 눈 · 재현 = litdb/figures/<slug>/digitized.csv 248 행 · 방법 = figures.json 'digitized') ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · §14) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug · 줄 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md · 정본 카드가 옮긴 것 — 출처를 그 자리에 적는다) · [미확인] = 본문 14 쪽 전수에 없음. -->

# 탄성 구 두 개의 비스듬한 충돌 — 접착 없으면 Hertz + Mindlin–Deresiewicz 증분 접선 법칙, 접착 (JKR) 이면 '벗겨진 뒤 미끄러진다' 는 새 미끄럼 기준 T = μ(P + 2Pc) — Thornton & Yin (Powder Technology 1991)

> slug `thorntonyin1991_oblique_impact_elastic_spheres_adhesion` · DOI `[미확인 — 원문에 인쇄 없음 · PDF 문서 정보의 PII 0032-5910(91)80178-L]` · type `DEM (contact-LAW theory: Hertz normal + Mindlin-Deresiewicz incremental tangential law with Thornton-Randall loading/unloading/reloading rules; JKR adhesive normal law + Savkoor-Briggs peeling + new peel-then-slide criterion T = mu(P + 2Pc); explicit Cundall-Strack scheme, two-sphere oblique impact, elastic spheres only, no damping) + comparison with published friction data (Briscoe & Kremnitzer 1979, PET monofilaments)` · PDF `8eb4154e-33._Impact_of_elastic_spheres_with_and_without_adhesion.pdf` · digested `2026-11-12` · status ✅

> elements: (없음 — 재료 이름 없는 탄성 구 · 배터리 소재 0)
> methods: elastic, adhesion

> **저자**: **C. Thornton** · K. K. Yin — Department of Civil Engineering, Aston University (Aston Triangle, Birmingham B4 7ET, U.K.).  0032-5910/91/$3.50 · © Elsevier Sequoia / Printed in The Netherlands (p.1).  접수 · 게재 날짜 [미확인] (원문에 없음).  둘째 저자 장학 = Unilever Research (Port Sunlight Laboratory) · Overseas Research Studentship Scheme (p.14).
> **이웃 카드 (링크만)**: [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) (같은 그룹 · **다른 논문** — 법선 탄소성 + 접착 · 정면 충돌 · 붙는 속도 식) · [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (JKR 원전 = 이 논문 [10]) · [`dmt1975_adhesion_contact_deformation`](dmt1975_adhesion_contact_deformation.md) (DMT = [11]) · [`boschpadros2014_dem_liggghts_msc_thesis`](boschpadros2014_dem_liggghts_msc_thesis.md) (LIGGGHTS `tangential history` 식) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (우리 압밀 DEM 접촉 법칙) · 가리킨 카드 [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (L302) · [`tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond`](tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond.md) ([47]).
> **판독 원자료**: `litdb/figures/thorntonyin1991_oblique_impact_elastic_spheres_adhesion/digitized.csv` (248 행 — 그림 6 · 8 · 11 · 12 · 13 · 14 · 15 · 17 표지 + 그림 4 · 5 · 16 요점 · 스캔 판독).

> ⚠⚠ **한 줄 경고 — 탄성 구 두 개의 충돌 하나다.**  재료 이름 없는 구 (R 100 µm · ρ 2.65 Mg/m³ · E 70 GPa · ν 0.3 · μ 0.35 · 접착 계산은 γ 0.2 J/m²) · 소성 0 · 감쇠 0 · 압밀 0 · 다입자 0.  **LPSCl · NCM 으로 옮길 절대값은 0 개.**  옮길 수 있는 것 = 접선 이력 법칙의 증분 규칙 (식 7–15) · JKR 접착 위의 '벗김 → 미끄럼' 기준의 꼴 (식 40 · 42 · 52) · 접착이 비스듬한 충돌의 소산 · 되튐을 바꾸는 방식 · 접착 없는 반발각이 속도에 무관하다는 성질 (U5 벤치마크 꼴) · *"반발 계수 같은 간단한 규칙은 없다"* 는 결론.

> ★★ **이 카드의 핵심 셋 (원문에 없는 것 · 원문과 어긋나는 것 포함 — §0-1 · §13)**:
> ① **탄성 전용이다 — '탄소성' 이 아니다.**  원문 p.1 *"Although the work presented is restricted to elastic spheres (plastic deformation at the contact is not considered), the purpose of the paper is to illustrate the effect of oblique impact on the dissipation and redistribution of energy."* · 제목도 *"Impact of elastic spheres with and without adhesion"*.  가리킨 카드 pfeffer2001 L302 의 *"탄소성 접촉"* 표기는 원문과 다르다 (§13 카드 문제).  소산은 **접선 미세 미끄럼 · 강체 미끄럼 (+ 접착 이력)** 에서만 나오고 *"the work done by the normal force is fully recovered at the end of the impact"* (p.4).
> ② **접착 접선 법칙의 새 기준**: JKR 법선 + Savkoor–Briggs '벗김 (peeling)' 이 끝나면 접촉 반지름 a* (식 41) 위에 유효 법선력 P + 2Pc 의 Hertz 꼴 응력이 있다고 보고 Mindlin 미세 미끄럼 → **T = μ(P + 2Pc)** (식 42) 에서 미끄럼.  P < −0.3Pc 에서는 그 가정 (r₀ ≥ a*) 이 깨져 **식 (52) T = μP′[1 − (P′ − P)/(3P′)]^{3/2}** 를 이어 붙인다 (p.10–11).  실험 대조 = Briscoe–Kremnitzer PET 단섬유 마찰 (Pc = 1.6 µN 실측) — **고른 값 = 마찰 계수 μ 하나 · 기준마다 다름 (식 42 → 0.35 · 식 52 → 0.30)** · 저자 = 식 (52) μ 0.30 이 *"best overall fit"* (p.11).
> ③ **붙는 (sticking) 임계 속도 식 · 값은 이 논문에 없다.**  p.13 *"For colinear impacts with adhesion, the computer-simulated experiments identified critical impact velocities, above which particles bounce and below which particles stick together; as expected, the observations agreed with the predictions of JKR theory, see Reed [21]. … This will be the subject of a subsequent paper."*  반발 계수 vs 속도 곡선도 없다 (결론: *"no simple rules (e.g., coefficients of restitution, scattering probability)"* p.13).  이 논문의 유일한 접착 계산 (γ 0.2 · v_rel 0.1 m/s) 의 정면 충돌 소산 [판독] 0.7–1.1 % 는 Thornton–Ning 1998 의 JKR 식 [다른 카드] 으로 **0.90 % · V_s 9.5 mm/s (V/V_s ≈ 10.6)** [카드 산술 §14-6] 와 맞는다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

1. **무엇**: Cundall–Strack 꼴 명시 DEM 프로그램 (선형 스프링 · 대시팟 → 접촉역학 법칙으로 바꾼 것 · p.1) 으로 **같은 탄성 구 두 개의 비스듬한 충돌**을 충돌각 θ 0–90° 로 계산.  (a) 접착 없음 = Hertz 법선 (식 1–6) + Mindlin–Deresiewicz 접선을 Thornton–Randall 증분 규칙 (식 7–18) 으로.  (b) 접착 = JKR 법선 (식 19–34) + Savkoor–Briggs 벗김 (식 35–41) + 새 미끄럼 기준 (식 42–46 · 대안 식 47–53).
2. **계산 입력** (p.3 · p.11 [인쇄]): R = 100 µm · ρ = 2.65 Mg/m³ · E = 70 GPa · ν = 0.3 · μ = 0.35 · 세로 속도 ±0.05 m/s (상대 0.1 m/s) · 접착 계산 γ = 0.2 J/m² (*"effective surface energy"*).  시간 간격 · 사이클 수 · 계산 시간 [미확인] (*"the very small time step"* 만 · p.3).
3. **접착 없음 결과** [판독 · 그림 6 · 8]: 남은 선 운동 에너지 최소 **0.54 (θ 60°)** · 회전 에너지 최대 **0.28 (60°)** · 소산 최대 **0.25 (70°)** (처음 운동 에너지 대비) · 접촉점 반사각이 **≈ 26–67° 에서 음수** (Maw 류 '되튐' · 최소 ≈ −32°) · 중심 반발각은 늘 양수 · 충돌각보다 작다.  완전 탄성 · 무감쇠인데도 소산이 생긴다 (p.4).
4. **접착 결과** [판독 · 그림 15 · 17]: 작은 충돌각 (≤ ≈ 22°) 에서 **중심 · 접촉점이 처음 경로로 되튄다** (중심 반발각 ≈ −0.95θ) · ≈ 22–30° 에서 빠르게 접착 없음 쪽으로 · 소산 θ 25° **0.21** (접착 없음 ≈ 0.05 [카드 산술 보간]) · 회전 최대가 70° 로 옮김 (0.30) · 큰 각에서 중심 반발각은 접착 없음과 비슷 (40° 28.7 ↔ 27.0°) 하나 접촉점 반사각은 다르다 (70° −39 ↔ +17°).  임계 충돌각은 속도가 낮을수록 커진다 (서술만 · 값 없음 · p.12–13).
5. **질문 e (점접촉 법칙이 깨지는 범위 · 대안 · 맞춘 값 수)**: 이 논문은 큰 변형 · 조밀 충전을 다루지 않는다 (최대 접근량 ÷ 반지름 ≈ 3.3 × 10⁻⁴ [카드 산술]).  주는 것 = **접선 · 접착 쪽 접촉 법칙** — 계산은 맞춘 값 0 (입력 고정), 실험 대조에서 μ 하나 (식마다 다름).  저자 자신이 법칙을 *"not a rigorous solution"* · *"speculative"* 라 적는다 (p.14).
6. **질문 k (DEM 한계 문장)**: 선형 스프링 · 대시팟 DEM 을 접촉역학 법칙으로 바꾼 이유 (p.1) · *"it is essential that energy is dissipated in as natural a way as possible"* (p.1) · 반발 계수 같은 *"simple rules"* 로는 반발을 못 맞춘다 (p.13).  '단단한 구 · 점접촉이 조밀 영역에서 깨진다' 는 문장은 **없다**.
7. **2D/3D · 탈압**: 접촉식은 구 (3D Hertz · Mindlin · JKR) · 충돌 운동은 한 평면 (그림 3 · 7) · 프로그램이 2D 인지 3D 인지 [미확인] · 2D → 3D 서술 없음.  '탈압' = 충돌 한 번 안의 법선 싣기 → 빼기 (탄성 · 다 돌아옴) 와 접선 빼기 · 다시 싣기 규칙 (식 12–13) 뿐 · 압밀 압력을 빼는 계산은 없다.
8. **우리 믹서 '붙는 속도' 와 견줄 자리 (판정 없이)**: 이 논문은 식을 주지 않는다 (③).  JKR 계열의 꼴은 Thornton–Ning 1998 식 (54) V_s ∝ (Γ⁵R*⁴/E*²)^{1/6}/√m* [다른 카드] — **접착 이력 (닿을 때 −8Pc/9 로 뛰어듦 ↔ 떨어질 때 다른 자리) 이 감쇠 없이도 에너지를 뺏는 꼴**이다.  우리 믹서 SJKR (CED × 겹침 면적) 은 힘이 겹침의 한 값 함수 (목 · 점프 없음 [다른 카드 johnson1971 L222]) 라 그 이력 고리가 0 이다 [카드 해석 §7-4] → **같은 꼴이 아니다**.  우리 dev-u 의 *"SE–SE 붙는 속도 상한 18.7 · 46.6 mm/s (벽 103 · 지금 모델 0.16)"* [우리 · CLAUDE.md] 를 낸 식은 이 카드가 보지 않았다 [미확인].

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-33 의 '왜' 칸)

의도 원문: *"e (근거 약함) — pfeffer2001 의 표기 '탄소성 접촉 — 카드 없음' 뿐 · 접촉 법칙 계보 (정본 thorntonning1998 은 다른 논문)"* (가리킨 카드 = `pfeffer2001_dry_particle_coating_engineered_particulates` L302 · 서지 상태 = 일부만 (제목 없음))

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "e" (질문 e: 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값 수) | **일부** | 큰 변형 · 조밀 충전 · 깨지는 범위의 문턱 = **없음** (두 구 · 탄성 · α/R ≤ 3.3 × 10⁻⁴ [카드 산술 §14-1]).  주는 것 = 접선 · 접착 쪽 법칙 계보와 대안 셋: 식 (42) T = μ(P + 2Pc) · 식 (52) T = μP′(1 − (P′−P)/(3P′))^{3/2} · Kendall 식 (53) T = μP′ (p.9–10 · `eq_42` · `eq_52` · `eq_53`).  맞춘 값: 계산 0 개 (입력 고정 · p.3 · p.11) · 실험 대조 μ 1 개 (식 42 → 0.35 · 식 52 → 0.30 · *"assuming values of"* p.10) · Pc 1.6 µN 은 실험 실측 (p.10) |
| "(근거 약함)" | **맞음 (근거 약했다)** | 원문은 탄성 · 충돌 하나라 e 의 '큰 변형' 축에는 직접 근거가 없다 — 접촉 법칙의 **접선 · 접착 층** 근거다 |
| "pfeffer2001 의 표기 '탄소성 접촉'" | **없음** | 원문 = 탄성 전용: *"restricted to elastic spheres (plastic deformation at the contact is not considered)"* (p.1 · `txt_p1_elastic_spheres_only_plastic_not_considered.png`) · 제목 *"Impact of elastic spheres with and without adhesion"* (p.1) · 'plastic' 낱말은 그 한 곳뿐 (글자 층 [카드 확인]).  '탄소성 접촉' 은 같은 그룹의 **Thornton–Ning 1998** (정본 `thorntonning1998_…`) 의 일 [다른 카드] |
| "카드 없음" | **맞음** | 정본 `litdb/papers/` 파일 목록 (551 · 이 카드 전) + grep "Thornton … Yin" = pfeffer2001 L302 · tovar2026 L86–L87 · L343 의 인용 줄뿐 (원문 대조 기록) |
| "접촉 법칙 계보" | **채움** | Hertz [4] → Mindlin [5] (무미끄럼 · 부분 미끄럼) → Mindlin–Deresiewicz [6] (이력 의존 · 순간 컴플라이언스) → **Thornton–Randall [2] 증분 규칙** (식 7–13 · 되돌림 점 T* · T\*\* 갱신 · Szalwinski [7] 경우는 θ = 1 규칙 · 식 15) → JKR [10] · DMT [11] · Muller [14] 전이 변수 (식 21) → **Savkoor–Briggs [18] 벗김** (식 35–41) → **이 논문의 새 기준** (식 42 · 대안 52 · Kendall [19] 식 53) (§7-2 표) |
| "(정본 thorntonning1998 은 다른 논문)" | **채움 (맞음)** | TN1998 = Powder Technol. 1998 · DOI 10.1016/S0032-5910(98)00099-0 [다른 카드 L3] · 법선 (정면) **탄소성 + 접착** · 항복압 캡 p_y · 붙는 속도 V_s (식 54) [다른 카드 L70 · L138].  이 논문 = **접선 · 비스듬한 충돌 + 접착 · 탄성**.  서로 보완하는 두 편이고 TN1998 카드 본문에는 이 논문 언급이 없었다 (이 작업 전 grep 'Yin' 0 건 [카드 확인] — 이번에 그 카드 '🔗 관련 카드' 에 이 카드를 가리키는 한 줄만 더함) |

**가리킨 카드 · 인용 카드의 2 차 인용 대조** (자세히는 §13):

| 카드 · 줄 | 그 카드의 말 | 원문 | 판정 |
|---|---|---|---|
| pfeffer2001 L302 | *"\| 117 \| C. Thornton, K.K. Yin, Powder Technol. 65 (1991) 153–166. \| 탄소성 접촉 — 카드 없음 \|"* | 저자 · 학술지 · 권 · 쪽 · 연도 = p.1 머리글과 같음 · 내용 = **탄성 전용** (p.1) | 서지 ✓ · 내용 표기 ✗ (카드 문제) · 제목 없음 |
| pfeffer2001 (본문) | [117] 을 쓰는 본문 줄 없음 (grep '117' = L302 한 줄) | — | 원 논문 (Pfeffer 2001) 이 [117] 을 어디에 썼는지는 이 카드로 [미확인] |
| tovar2026 L86 | *"접선 Mindlin–Deresiewicz 정지마찰 (하중–변위 이력 반영) → Coulomb 상한 μFⁿ_c 에서 미끄럼 [47]"* | p.2–3 (식 7–18 · 미끄럼 ITI = μP) | ✓ |
| tovar2026 L87 | *"F_cd … (K_c = Thornton & Yin [47])"* (감쇠 식 (21)(22) 의 강성만 [47]) | 강성 kⁿ = 2E*a (식 6) · kᵗ (식 9 · 17 · 18) — 감쇠 식은 이 논문에 **없다** (감쇠 0 · p.4) | ✓ (카드가 강성만 [47] 로 돌림 · 감쇠 식은 tovar 원문 몫) |
| tovar2026 L343 | *"[47] C. Thornton & K. K. Yin, Powder Technol. 65 (1991) 153 \| 접촉 강성 · 접선 이력 \| 없음 (같은 저자 계열 thorntonning1998 은 있음 — 다른 논문)"* | 같음 | ✓ |

---

## 1. 한 줄 요약

**같은 탄성 구 두 개 (R 100 µm · E 70 GPa · μ 0.35) 의 비스듬한 충돌을 Hertz + Mindlin–Deresiewicz 증분 접선 법칙으로 계산해 감쇠 없이도 미끄럼 소산 · 회전 · 접촉점 되튐이 충돌각에 따라 복잡하게 변함을 보이고, JKR 접착 (γ 0.2 J/m²) 에는 '벗겨진 뒤 유효 법선력 P + 2Pc 로 미끄러진다' 는 새 접선 기준 (T = μ(P + 2Pc) · P < −0.3Pc 에서는 다른 식) 을 세워 PET 단섬유 마찰 실험 (Pc 1.6 µN) 과 대조한 뒤, 접착이 작은 충돌각에서 입자를 처음 경로로 되튀게 한다** 고 보고한 14 쪽 논문.  ⚠ **탄성 전용** (소성 고려 안 함 · p.1) · 붙는 임계 속도 식 · 값 없음 (Reed [21] 로 넘김 · p.13).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **C. Thornton** · K. K. Yin (Aston University, Civil Engineering) | **Powder Technology, 65 (1991) 153–166** · 14 쪽 | [미확인] (인쇄 없음 · PDF 문서 정보 PII 0032-5910(91)80178-L) | **재료 이름 없는 탄성 구** (E 70 GPa · ρ 2.65 Mg/m³) + 실험 대조 = PET 단섬유 (다른 논문의 자료) — 배터리 소재 **0** | **DEM 접촉 법칙 (접선 이력 · 접착) + 두 구 충돌 계산 + 남의 마찰 실험 대조** |

- 절 구성 (원문 제목): Abstract · Introduction · Oblique loading without adhesion · Computer-simulated impact tests (no adhesion) · Normal loading with adhesion · Oblique loading with adhesion · The sliding criterion · Computer-simulated oblique impact (with adhesion) · Conclusions · Acknowledgements · References (21 개).
- **계보**: 이 프로그램에 접촉역학 법칙을 넣은 일 = Thornton–Randall [2] (1988 · *Micromechanics of Granular Materials*) · Randall 박사논문 [3] (Aston 1989).  같은 그룹의 뒤 논문 = Thornton–Ning 1998 (법선 탄소성 + 접착) [다른 카드].
- **후보 표 서지와의 차이**: 후보 표 · pfeffer2001 = *"C. Thornton, K.K. Yin, Powder Technol. 65 (1991) 153–166"* (제목 없음) → 원문 제목 **"Impact of elastic spheres with and without adhesion"** · 저자 표기 원문 *"C. Thornton and K. K. Yin"* · DOI 는 원문에 인쇄되지 않음 (PDF 문서 정보 제목 칸 = *"PII: 0032-5910(91)80178-L"*).  나머지 (학술지 · 권 · 쪽 · 연도) 같음.

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 계산 입력 (p.3 · p.11 · `txt_p3_simulation_properties_r100um_e70gpa_mu035_v005.png` · `txt_p11_adhesion_simulation_gamma_0p2.png`)

| 양 | 값 | 표지 · 위치 |
|---|---|---|
| 입자 | 같은 구 2 개 · 반지름 R = **100 µm** | [인쇄] p.3 |
| 밀도 ρ | **2.65 Mg/m³** | [인쇄] p.3 |
| 영률 E · 포아송비 ν | **70 GPa · 0.3** | [인쇄] p.3 |
| 마찰 계수 μ | **0.35** (접착 계산도 같음) | [인쇄] p.3 · p.11 |
| 처음 속도 | 세로 **±0.05 m/s** (상대 0.1 m/s · p.13 · p.14) · 처음 회전 0 [카드 해석 — 그림 7 · 'no initial spin' 은 Maw 실험 서술] | [인쇄] p.3 · p.11 |
| 충돌각 θ | 0–90° (그림 3: 공통 접선과 수평선 사이 · 0 = 정면) · 표지 간격 2–10° | [판독] 그림 6 · 8 · 15 · 17 |
| 표면 에너지 γ (접착 계산) | **0.2 J/m²** (*"an effective surface energy"*) · γ = *"the surface energy of each solid"* (p.7) → 접착 일 Γ = 2γ = 0.4 J/m² [카드 해석 · TN1998 의 Γ 규약 [다른 카드 L71]] | [인쇄] p.11 · p.7 |
| 감쇠 | **없음** — *"For all impacts, the work done by the normal force is fully recovered at the end of the impact."* | [인쇄] p.4 |
| 시간 간격 · 사이클 수 · 계산 시간 · 프로그램 이름 | *"the very small time step"* (값 없음) · *"a sufficient number of calculation cycles"* | [미확인] p.3 |
| 재료 이름 | 없음 | [미확인] |

### 3-2. ★ 접착 없음 결과 (그림 4–8 · p.4–6)

- **그림 4 (a)** T–P 경로 [판독 · 눈]: P_max 15° ≈ **2.03** · 30° ≈ **1.78** · 45° ≈ **1.40 mN** (Hertz 산술 2.044 · 1.793 · 1.406 mN [카드 산술 §14-1] 과 같음) · T 범위 15° −0.17…0.25 · 30° −0.24…0.45 · 45° ≈ −0.15…0.48 mN · **45–75° 의 처음 경로 기울기 ≈ 0.35 = μ** (강체 미끄럼으로 시작).  원문: θ 가 마찰각보다 작으면 (15°) ITI = μP 는 끝에만 · 그 전에 미세 미끄럼 소산 · 30° · 45° 는 처음부터 미끄럼 → 접선력 반전 → 끝에 다시 미끄럼 · 60° 는 미끄럼이 회복 단계까지 · 75° 는 내내 미끄럼 · 반전 없음 (p.4).
- **그림 4 (b)** T–접선 변위 (µm 축) 고리 = *"That energy is dissipated during the oblique impact of two perfectly elastic spheres is clearly demonstrated by the force–displacement curves shown in Fig. 4(b)."* (p.4).
- **그림 5** (θ 30 · 60 · 80°) [판독 · 눈]: 처음 운동 에너지 ≈ **0.0277 nJ** (카드 산술 0.02775 nJ) · 접촉 시간 ≈ 1.0 · 1.1 · 1.33 µs (Hertz 0.986 · 1.101 · 1.360 µs [카드 산술]) · 끝 선 운동 에너지 ≈ 0.0241 · 0.015 · 0.0213 nJ (그림 6 의 비 × 0.02775 = 0.0240 · 0.0150 · 0.0217 [카드 산술]) · 60° 의 끝 회전 일 ≈ 0.0079 · 접선 (전단) 일 ≈ 0.0055 nJ (그림 6: 0.280 · 0.191 × 0.02775 = 0.0078 · 0.0053).  법선 일은 끝에 다 돌아온다 · 비스듬한 충돌의 선 운동 에너지는 0 이 되지 않는다 (p.4).
- **그림 6** (처음 운동 에너지 대비 비 · 축 0–1) [판독 · digitized.csv]:

| θ (°) | 0 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| 남은 선 운동 | 1.00 | 0.99 | 0.949 | 0.864 | 0.740 | 0.613 | **0.540** | 0.610 | 0.782 | 0.998 |
| 얻은 회전 | 0 | ≈0.003 | ≈0.018 | ≈0.065 | 0.166 | 0.261 | **0.280** | 0.145 | 0.041 | 0 |
| 소산 | 0 | ≈0.008 | ≈0.033 | ≈0.068 | 0.097 | 0.135 | 0.191 | **0.247** | 0.191 | 0 |

  셋의 합 ≈ 1.00 ± 0.014 [카드 산술] → 그린 '선 운동' 은 **남은 몫**이다 (본문은 *"percentage loss in linear kinetic energy"* 라 적음 · p.5 [카드 해석]).  10–30° 의 작은 값은 표지가 겹쳐 눈으로 읽음 (≈).  원문: 회전 이득 · 선 손실은 *"until the impact angle is sufficiently large to produce rigid body sliding throughout the impact"* 까지 커지고 · 소산은 그 뒤에도 늘다가 *"decreases at very high impact angles due to the frictional limited tangential force"* (p.5).
- **그림 8** (접촉점 반사각 · 중심 반발각) [판독]: 중심 = 6° 5.3 · 10° 8.8 · 20° 15.7 · 30° 21.5 · 45° 30.5 · 60° 47.2 · 70° 64.2 · 80° 78.5 · 90° 89.6 (늘 양수 · 충돌각보다 작다) · 접촉점 = 6° 2.9 · ≈14° 4.4 (최대) · 25° 1.0 · 30° −4.8 · 45° −20.9 · 55° −31.9 · 60° −30.9 · 65° −16.8 · 70° +16.8 · 80° 72.8 → **음수 구간 ≈ 26–67°** [카드 산술 · 선형 보간].  원문: 음수 구간은 *"primarily dictated by the interparticle friction but also slightly affected by the Poisson ratio of the spheres"* (p.6).

### 3-3. ★ 접착 결과 (그림 12 · 15–17 · p.10–13)

- **그림 17** (γ 0.2 · v_rel 0.1 m/s · 처음 운동 에너지 대비) [판독]:

| θ (°) | 0 | 10 | 20 | 25 | 30 | 35 | 40 | 50 | 60 | 70 | 80 | 85 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 남은 선 운동 | 0.989 | 0.980 | 0.952 | 0.762 | 0.800 | 0.780 | 0.730 | 0.616 | 0.519 | **0.463** | 0.526 | 0.567 |
| 얻은 회전 | ≈0 | 0.000 | 0.001 | 0.020 | 0.033 | 0.072 | 0.108 | 0.211 | 0.282 | **0.298** | 0.184 | 0.151 |
| 소산 | ≈0.009 (0.007–0.011) | 0.021 | 0.051 | **0.207** | 0.166 | 0.152 | 0.152 | 0.171 | 0.197 | 0.244 | **0.292** | 0.281 |

  원문: 벗김이 법선력이 커지는 동안 일어나면 그림 6 과 비슷하나 *"with the optimum occurring at a larger impact angle"* · 벗김이 끝에서만 끝나는 작은 각에서는 *"there is no rotational kinetic energy developed, but there is a loss in linear kinetic energy due to the energy dissipated in adhesive peeling"* (p.13).  ⚠ 접착 없음 25° 의 소산은 그림 6 에 표지가 없다 → 20 · 30° 보간 ≈ 0.05 [카드 산술].
- **그림 15** (접착 ↔ 없음) [판독]: (b) 중심 반발각 — 접착 2° −1.9 · 10° −9.3 · 20° **−18.9** (≈ −0.95θ · 처음 경로로 되튐) · 25° +11.0 · 40° 28.7 (없음 27.0 · 그림 8) · 70° 60.8 (없음 64.0) / (a) 접촉점 반사각 — 접착 22° −19.9 · 24° −9.0 · ≈27–30° ≈ 0 · 45° −15.6 · **70° −39.1 (최소)** · 80° +11.0 (없음: 70° +17.3 · 80° +72.6).  원문: 작은 각에서 *"adhesion provides sufficient kinematic constraint on the particle movements that the contact behaviour is simply that of an oblique elastic spring, resulting in both the contact patch and particle centroid rebounding back along the initial impact trajectory"* · 임계각 위에서는 *"rapid transition"* · 중심 반발각에 대한 접착 효과는 *"negligible"* · 접촉점은 *"significant"* (p.11–12) · *"The rebound trajectories are independent of impact velocity if there is no adhesion but, in the presence of adhesion, the impact angle at which the simple elastic spring effect breaks down increases with decrease in initial impact velocity."* (p.12–13 · 값 없음).
- 결론의 정리 (p.14 · `txt_p13_p14_conclusion_…`): *"although adhesion affects the dissipation and redistribution of energy for all angles of impact, the effect is most pronounced when peeling is only completed at the end of the impact. The angles of impact at which this occurs depend on the impact velocity. For all impact angles, if the impact velocity is not large enough to complete the peeling process when the normal force is increasing, then the particles will rebound back along the initial impact trajectory, unless the impact velocity is sufficiently small that sticking occurs."* — 붙음의 문턱 값은 없다.
- **그림 16** (T–P 경로 · 15/30/45/60/75°) [판독 · 눈]: 접착 시 처음 법선력 ≈ **−0.08 mN** (= JKR 의 뛰어듦 −8Pc/9 = −0.084 mN [카드 산술]) · 원문: 처음 ΔT/ΔN 은 거의 일정 · *"slightly greater than tan θ … due to the difference between the tangential and normal contact stiffnesses"* (p.13) · (a) 15° 꼭짓점 ≈ (2.07, 0.53) mN (평균 기울기 ≈ 0.25 ↔ tan 15° 0.268 — 판독은 평균이라 처음 기울기와 다를 수 있음) · (b) 30° 벗김 ≈ (0.6, 0.45) → ≈ (0.65, 0.28) = μ(P + 2Pc) 로 뚝 · T 최대 0.49 (P 1.45) · P_max ≈ 1.85 · T 최소 −0.31 mN · (d) 60° 꼭짓점 ≈ (1.0, 0.41) = μ(1.0 + 0.188) = 0.416 [카드 산술] · (e) 75° 미끄럼 선 접착 (0, 0.065) → (0.49, 0.238) · 없음 0 → (0.42, 0.147).
- **그림 12** (접선 힘–변위 · 접착 · 정적) [판독]: (a) **P = 10 mN** — 벗김 끝 Tc ≈ **1.78 mN** (δ ≈ 13 nm · 화살표) → 미끄럼 고리 → 판 **3.55 mN** (마지막 표지 40.4 nm) / (b) **P = 0** — Tc **0.171 mN** (4.75 nm) → 미끄럼 값 **0.067 mN** 로 뚝 · 처음 기울기 ≈ 0.041 mN/nm.  카드 산술 (§14-3): Tc 1.770 · δc 13.0 nm · μ(P+2Pc) 3.566 mN / Tc 0.1711 · δc 4.75 nm · 0.0660 mN · 8G*a₀ 0.0454 mN/nm — 그림 12 = 식 (40) · (42) · (43) 의 그림이다 (P = 10 mN > P* = 2.25 mN → (a) 꼴 · P = 0 < P* → (b) 꼴).

### 3-4. ★ 실험 대조 (Briscoe–Kremnitzer [20] · PET 단섬유 · 그림 13–14 · p.10–11 · `txt_p10_p11_r0_condition_briscoe_kremnitzer_pc_1p6_mu_0p35_0p30.png`)

- 자료 = 남의 마찰 측정 (*"results of friction measurements reported by Briscoe and Kremnitzer [20] for polyethylene terephthalate monofilaments"*) · **Pc = 1.6 µN** = 그들이 잰 떼는 힘 (p.10 [인쇄]) · 시편 기하 · E · R · 하중 범위의 절대값 [미확인].
- 겹친 선: 식 (42) μ = **0.35** · 식 (52) μ = **0.30** (*"assuming values of"* · 고른 방법 서술 없음) · *"Both the theoretical curves agree well with the experimental data over the complete range of experimental results."* · 음의 하중 (그림 14) 에서는 *"the sliding criterion defined by eqn. (52), with μ = 0.30, provides the best overall fit"* (p.10–11).
- 그림 13 실험점 [판독 ±0.2 · P/Pc, T/Pc]: (10.4, 4.2) · (12.9, 4.9) · (14.5, 5.4) · (16.9, 5.9) · (18.7, 7.0) · (21.4, 8.05) · (23.5, 9.1) — P/Pc < 10 의 점은 선과 겹쳐 따로 못 읽음.  식 값 P/Pc 25: 식 42 (μ 0.35) **9.45** · 식 52 (μ 0.30) **9.38** [카드 산술].
- 그림 14 실험점 [판독 ±0.03]: (−1.00, 0.00) · (−0.80, 0.14) · (−0.76, 0.24) · (−0.57, 0.48) · (≈ −0.40, ≈ 0.48 불확실) · (−0.13, 0.62) · (0.00, 0.59) · (0.12, 0.77) · (0.26, 0.86) · (0.44, 0.95) · (0.73, 0.78) · (0.75, 1.17) · (1.65, 1.19).  식 값 [카드 산술]: P = −Pc 에서 식 42 (0.35) 0.35 · 식 52 (0.35) 0.067 · 식 52 (0.30) 0.058 / P = 0 에서 0.70 · 0.762 · 0.653 → **떼는 힘 근처에서 T → 0 인 실험을 식 (52) 만 따른다**.
- ⚠ 이 대조는 **충돌이 아니라 정적 마찰** 이다 — 비스듬한 충돌 (되튐) 을 확인할 실험은 저자도 모른다 (*"The authors are not aware of any experimental work that can confirm or deny this possibility"* p.14).

### 3-5. 이론 그림 (그림 9–11)

- **그림 9** JKR P/Pc vs α/α_c (곡선만 · ⚠ α_c 는 본문 정의 없음 — 본문은 a_c · 식 34) · **그림 10** JKR 법선 응력 (가운데 압축 · 가장자리 a 에서 무한 인장 · r₀ < a).
- **그림 11** 파괴 포락선 Tc/Pc vs P/Pc [판독]: peel = 1: 2.53 · 2: 3.05 · 5: 4.26 · 10: 5.69 · 15: 6.90 · 20: 7.84 · 25: 8.73 · 29.5: 9.45 / slide = 1: 1.16 · 2: 1.44 · 5: 2.46 · 10: 4.20 · 15: 5.88 · 20: 7.61 · 25: 9.29 · 29.5: 10.88 · 교점 ≈ P/Pc 21–23 · Tc/Pc ≈ 8.0–8.3.  slide 선 = μ 0.35 의 식 (42) 와 n ≥ 2 에서 ±3 % 안 · peel 선은 ν 0.3 (G*/E* 0.206) 의 식 (40) 보다 5–6 % 아래 (G*/E* ≈ 0.183 이면 맞음) → **그림 11 의 매개변수는 원문에 없다 [미확인]** (식 45 로 χ 6.72 면 교점 23.85 · 9.05 [카드 산술]).

### 3-6. 계산 비용 · 규모

- 입자 2 개 · 충돌 한 번 · 충돌각 사다리 (그림 6 열 각 · 그림 8 스물두 각 · 그림 17 열두 각) · 시간 간격 · 사이클 · 하드웨어 · 시간 [미확인].
- 접촉 시간 ≈ 1 µs (그림 5 [판독] · Hertz 0.96–1.36 µs [카드 산술]).

## 4. ★ 방법 — 모델을 식 수준으로 (식 크롭 = `eq_NN_<뜻>.png` · 53 개 전부)

### 4-1. 접착 없음 — Hertz 법선 (p.2 · 식 1–6)

α³ = 9P²/(16R*E*²) (1) · a³ = 3PR*/(4E*) (2) · 1/R* = 1/R₁ + 1/R₂ (3) · 1/E* = (1−ν₁²)/E₁ + (1−ν₂²)/E₂ (4) · α = a²/R* (5) · **kⁿ = 2E*a** (6).  α = 두 중심의 접근량 · a = 접촉 반지름.

### 4-2. 접착 없음 — Mindlin · Mindlin–Deresiewicz 접선 (Thornton–Randall 증분 · p.2–3 · 식 7–18)

- 물리 (p.2 · `txt_p2_…`): 일정 법선력에서 접선력이 원 둘레에서부터 미끄럼 고리를 안쪽으로 키우고 T = μP 에서 강체 미끄럼 · 접선력을 줄이면 둘레에서 반대 미끄럼이 새로 퍼짐 → *"the tangential stiffness is dependent on the loading history"* · 법선력마다 기하적으로 닮은 곡선 무한 집합 (그림 2).  Mindlin–Deresiewicz [6] 의 해는 *"instantaneous compliances which … could not be integrated a priori"* → 증분 접근: 법선력 · 접촉 반지름을 먼저 갱신하고 새 P · a 로 ΔT 를 계산.
- **증분 접선 변위 (Thornton–Randall [2])**: Δδ = (1/(8G*a))[±μΔP + (ΔT ∓ μΔP)/θ] (7) · 예외 조건 |Δδ| < μΔP/(8G*a), ΔP > 0 (8) · **kᵗ = 8G*θa ± μ(1−θ)ΔP/Δδ** (9 · 음 부호 = 빼기 때만) · 1/G* = (2−ν₁)/G₁ + (2−ν₂)/G₂ (10).
- θ: 싣기 θ³ = 1 − (T + μΔP)/(μP) (11) · 빼기 θ³ = 1 − (T* − T + 2μΔP)/(2μP) (12) · 다시 싣기 θ³ = 1 − (T − T\*\* + 2μΔP)/(2μP) (13).  되돌림 점 T* · T\*\* 는 *"need to be continuously updated (T* = T* + μΔP and T\*\* = T\*\* − μΔP) to allow for the effect of varying normal force"* (p.3).
- 새 곡선으로 가는 증분 |Δδ| = μΔP/(8G*a) (14) · 식 (8) 경우 (Szalwinski [7] 가 해석) 는 *"by setting θ = 1 in eqn. (9) until the following condition is satisfied"* 8G*aΣ|Δδ| > μΣΔP (15) (p.3 · `txt_p3_load_reversal_update_theta_one_rule.png`).
- 일정 P 단조: δ = (3μP/(16G*a))[1 − (1 − T/(μP))^{2/3}] (16) · kᵗ = 8G*a(1 − T/(μP))^{1/3} (17) · T = 0 에서 **kᵗ = 8G*a** (18 · Mindlin 'no-slip').

### 4-3. 계산 순서 (p.3–4 · `txt_p3_p4_explicit_calculation_cycle.png`)

첫 사이클: 처음 속도 × 아주 작은 시간 간격 → 변위 → 위치.  둘째부터: 현재 위치 · 속도 → 접촉의 법선 · 접선 상대 변위 증분 (*"having accounted for any relative spin"*) × 현재 법선 · 접선 강성 → 힘 증분 → 힘 갱신 → 불균형 힘 · 모멘트 ÷ 질량 · 관성 모멘트 → 가속도 × 시간 간격 → 속도 → 위치 · 충돌이 끝날 때까지 반복 (Cundall–Strack [1] 꼴 · 명시 유한 차분).

### 4-4. 접착 법선 — JKR (p.6–8 · 식 19–34)

- JKR · DMT 논쟁 (p.6–7 · `txt_p7_…`): JKR = 표면 에너지 변화가 접촉 면에서만 (무한히 짧은 거리) · 가장자리 무한 인장 · DMT = 접촉 밖의 유한 거리 인력 · 형상 불변.  *"Horn et al. [13] point out that the complete solution is very difficult, since the stress distribution in the spheres depends on the surface interaction, which depends on the exact shape of the deformed surfaces, which is only known if the stress distribution is known."*
- 떼는 힘: **JKR Pc = 3πγR*** (19) · DMT Pc = 4πγR* (20) · *"where γ is the surface energy of each solid"* (p.7) · Muller 변수 μ = (32/(3πz₀))(γ²R*/E*²)^{1/3} (21 · ⚠ 마찰 계수와 같은 글자) · *"JKR and DMT theories were accurate to within 10% for values of μ > 3 and μ < 1, respectively"* (p.7).  저자 선택: *"we will adopt the JKR model for normal loading of adhered elastic spheres"* (p.7) — 이 계산의 Muller 값은 z₀ 가 없어 계산 못 함 [미확인].
- 에너지: U_E (22) · U_M (23) · U_S = −2πγ(3R*P′/(4E*))^{2/3} (24) → 접촉 반지름 **a³ = (3R*/(4E*))[P + 2Pc + (4PPc + 4Pc²)^{1/2}]** (25) = (3R*/(4E*))P′ (26 · P′ = 유효 법선력).
- 응력 σ(r) = (3P′/(2πa²))(1 − r²/a²)^{1/2} − ((P′ − P)/(2πa²))(1 − r²/a²)^{−1/2} (27 · 그림 10) · 압축 구역 r₀ = a[1 − (P′ − P)/(3P′)]^{1/2} (28 · Hertz 반지름보다 큼).
- 강성: α = (πa/(2E*))(p₀ + 2p₀′) (29) · P = πa²(2p₀/3 + 2p₀′) (30) · p₀ = 2aE*/(πR*) (31) · p₀′ = −(4γE*/(πa))^{1/2} (32) → **kⁿ = 2E*a[3 − 3(a_c³/a³)^{1/2}]/[3 − (a_c³/a³)^{1/2}]** (33) · a_c³ = 3PcR*/(4E*) (34 · P = −Pc 의 반지름).

### 4-5. 접착 접선 — Savkoor–Briggs 벗김 (p.8 · 식 35–41)

Mindlin 무미끄럼 견인 τ(r) = (T/(2πa²))(1 − r²/a²)^{−1/2} (35) · T = 8G*aδ (36) · 접선력이 위치 에너지를 Tδ/2 낮춘다 → 총 에너지 U_T (37) · ∂U_T/∂a = 0 (38) → **a³ = (3R*/(4E*))[P + 2Pc ± (4PPc + 4Pc² − T²E*/(4G*))^{1/2}]** (39 · 접선력이 접촉 반지름을 줄임 = 벗김) → 임계 **Tc = 4[(PPc + Pc²)G*/E*]^{1/2}** (40) · 그때 a*³ = (3R*/(4E*))(P + 2Pc) (41).  Savkoor–Briggs 는 Tc 를 넘으면 *"the rate of energy release was more rapid than the rate at which the work of adhesion could absorb the energy and, hence, the quasi-static approach became inappropriate"* · 접촉이 Hertz 면적으로 준다고 보았다 (p.8 · `txt_p8_…`).

### 4-6. ★ 새 가설 · 미끄럼 기준 (p.9 · 식 42–46 · `txt_p9_hypothesis_peel_to_slide_effective_force.png`)

*"it is suggested that there is a smooth transition from peeling to sliding in that, when T = Tc the contact radius is given by eqn. (41). Recognising that the JKR model is only an approximation to the true solution, … the contact area defined by eqn. (41) is subject to an equivalent Hertzian-like normal stress distribution corresponding to an effective normal force (P + 2Pc)."* → Mindlin 미세 미끄럼 (P → P + 2Pc) → **T = μ(P + 2Pc)** (42) · 단조 T = μ(P + 2Pc)[1 − (1 − δ/δs)^{3/2}] (43) · δs = 3μ(P + 2Pc)/(16G*a) (44).  두 파괴 기준 (벗김 40 → 미끄럼 42) 의 교점 **P* = 2Pc{(χ − 1) ± [χ(χ − 1)]^{1/2}}** (45) · χ = 4G*/(μ²E*) (46).  P > P*: 벗김 뒤 미끄럼 고리가 안으로 퍼지다 미끄럼 (그림 12a) · P < P*: 벗김 끝의 T 가 미끄럼 값보다 커서 T 가 식 (42) 로 떨어짐 (그림 12b).  *"once sliding has occurred, there is no readhesion of the contact"* (가정) · 재접착을 허용하면 stick-slip — *"this type of stick-slip behaviour will not occur when the normal load P is greater than that given by eqn. (45)"* (p.9 · `txt_p9_failure_envelopes_stick_slip_no_readhesion.png`).

### 4-7. 가정 점검 · 대안 기준 (p.10–11 · 식 47–53)

- 가정 (a* 면적이 압축만 받음) 의 조건 r₀ ≥ a*: r₀/a* = (m/(n + 2))^{1/3}((n + 2m)/(3m))^{1/2} (47) · m = n + 2 + 2(1 + n)^{1/2} (48) · P = nPc (49) → *"the condition r₀ ≥ a* is satisfied except when P < −0.3Pc"* (p.10 · 카드 산술 교차 n = −0.325).
- *"if the theory was modified by assuming that the contact radius reduced to r₀ after peeling then the correlation with the experimental results would be much improved, especially when the normal contact force is negative"* → r₀³ = (3R*/(4E*))P′[1 − (P′ − P)/(3P′)]^{3/2} (50) · P′ = P + 2Pc + 2(PPc + Pc²)^{1/2} (51) → **T = μP′[1 − (P′ − P)/(3P′)]^{3/2}** (52) · Kendall [19] T = μP′ (53 · *"who did not consider the need for peeling to occur prior to sliding"*).
- 저자의 판단 (p.11 · `txt_p11_sliding_criterion_choice_m0p3pc_intractable.png`): Savkoor–Briggs 의 Tδ/2 는 선형 응답 가정 (a 가 T 로 변하는데) · *"A rigorous analysis accounting for the non-linear tangential response would appear to be intractable. Consequently, in the context of the JKR model of adhesion, eqn. (52), may well be the true sliding criterion. It must be noted, however, that the sliding criterion given by eqn. (52) is not consistent with the peeling criterion eqn. (40)"* → **계산 규칙 = P > −0.3Pc 에서 식 (42) · P < −0.3Pc 에서 식 (52) (같은 μ)**.

### 4-8. ★ 이 묶음의 네 질문 (원문 문장과 위치)

- **(i) DEM 한계 문장**: *"The programme originally used linear springs and dashpots to model the interactions between contiguous particles but, motivated by problems associated with process engineering, more realistic algorithms based on contact mechanics theories have been incorporated [2, 3]."* (p.1) · *"When dealing with large systems of particles, using either analytical or numerical models, it is essential that energy is dissipated in as natural a way as possible."* (p.1) · *"as a result of the complex tangential load-displacement behaviour, there would appear to be no simple rules (e.g., coefficients of restitution, scattering probability) that will satisfactorily achieve this."* (p.13).  ⚠ 단단한 구 · 점접촉 · 접촉 독립 가정이 **조밀 영역에서** 깨진다는 문장은 없다 (두 구 충돌 논문).
- **(ii) 소성 · 큰 변형이 어려운 이유와 우회**: 이유 서술 **없음** — *"restricted to elastic spheres (plastic deformation at the contact is not considered)"* 로 범위만 자른다 (p.1).  어려움의 말은 접착 쪽뿐: JKR · DMT 는 근사 · *"complete solution is very difficult"* (Horn · p.7) · 접선 비선형 *"intractable"* (p.11).  우회 · 비용 서술 없음.  같은 그룹의 법선 소성 법칙은 7 년 뒤 Thornton–Ning 1998 [다른 카드].
- **(iii) 2D/3D**: 접촉식 = 구 (3D 해) · 충돌 = 한 평면 · 프로그램 차원 [미확인] · 2D → 3D 서술 없음.
- **(iv) 탈압**: 충돌 한 번 안의 법선 싣기 → 빼기 (탄성 · 다 돌아옴 · p.4) · 접선 빼기 · 다시 싣기 규칙 (식 12–13) · 접착 접촉의 떨어짐 (벗김 · 떼는 힘) — 압밀 압력을 빼는 계산 · 되돌아옴 측정은 없다.

### 4-9. 저자 한계 · 미래 (원문 그대로 · p.13–14 · `txt_p13_p14_conclusion_no_simple_rules_not_rigorous_no_experiment.png`)

- *"The resulting theory, however, is not a rigorous solution, due to the approximations in existing theories and the speculative nature of the proposed sliding criteria. Nevertheless, it is believed that the proposed theoretical model is qualitatively correct in describing the tangential response as one which requires peeling to occur prior to sliding."*
- *"A significant consequence of this for oblique impacts is the possible bouncing back of a particle along the initial impact trajectory, as shown in Fig. 15(b). The authors are not aware of any experimental work that can confirm or deny this possibility. There is, therefore, a need for detailed experimental observations of oblique impacts of micron-sized particles at low impact velocities in order to test the theoretical ideas presented in the paper."*
- 붙음: *"For oblique impacts, the sticking probability is complicated by other possibilities. This will be the subject of a subsequent paper."* (p.13).
- ⚠ 결론의 *"Savkoor and Briggs [5]"* 는 목록상 [5] = Mindlin 1949 → [18] 의 오식 [카드 확인].

### 4-10. 기법 미니 용어집

- **미세 미끄럼 (micro-slip)**: 접촉 둘레의 고리에서만 미끄러지는 것 — 강체 미끄럼 전에도 에너지를 뺏는다 (그림 4b).
- **θ (식 11–13)**: 미끄럼 고리 크기를 담는 무차원 수 (θ = 1 → 무미끄럼 강성 8G*a · θ → 0 → 강체 미끄럼).
- **되돌림 점** (T\* · T\*\*): 접선력이 방향을 바꾼 자리 — 접촉이 기억해야 하는 이력.
- **벗김 (peeling)**: 접선력이 접착 접촉의 반지름을 줄이는 과정 (식 39) · Tc 에서 끝.
- **유효 법선력 P′ · P + 2Pc**: 접착 때문에 실제 하중 P 보다 큰 Hertz 꼴 하중 (식 26 · 41).
- **Pc**: 떼는 힘 (pull-off) — JKR 3πγR* (γ = 각 고체의 표면 에너지).

## 5. Figure set ★ (그림 17 + 식 53 + 근거 글 20 = 90 장 · 표 없음)

| 그림 | 쪽 | 내용 | 우리 쓰임 |
|---|---|---|---|
| 1 | 2 | 견인 분포 도식 (Hertz · Mindlin 무미끄럼 · 부분 미끄럼) | 접선 견인의 가장자리 특이 · 미끄럼 고리 |
| 2 | 2 | 접선 힘–변위 도식 (N · N + ΔN · 되돌림 T* · T\*\* · 점 1→2→3) | 증분 규칙 (식 7–15) 의 그림 |
| 3 | 3 | 충돌 배치 (±v · θ) | U5 배치 |
| 4 | 4 | (a) T–P 경로 15–75° (b) T–접선 변위 | 미끄럼 시작 · 반전 · 소산 고리 |
| 5 | 5 | 에너지 시간 변화 30 · 60 · 80° | 법선 일 다 돌아옴 · 접선 · 회전 일 |
| 6 | 6 | ★ 선 · 회전 · 소산 vs 충돌각 (접착 없음) | U5 표적 (digitized.csv) |
| 7 | 6 | 궤적 도식 (접촉점 되튐 · 중심 앞으로) | 관측량 정의 |
| 8 | 6 | ★ 접촉점 반사각 · 중심 반발각 vs 충돌각 | U5 표적 · 속도 무관 (접착 없음) |
| 9 | 7 | JKR P/Pc vs α/α_c | 접착 법선 곡선 |
| 10 | 8 | JKR 법선 응력 (a · r₀) | 식 27 · 28 |
| 11 | 9 | 파괴 포락선 (peel · slide) | P* · 매개변수 [미확인] |
| 12 | 10 | ★ 접착 접선 힘–변위 P = 10 mN · 0 | 식 40 · 42 · 43 의 수치 점검 |
| 13 | 10 | 미끄럼 기준 ↔ PET 실험 (P/Pc 0–25) | 실험 대조 (μ 고름) |
| 14 | 11 | 작은 · 음의 하중 실험 ↔ 식 42 · 52 | 식 (52) 쪽 |
| 15 | 11 | ★ 반발각 접착 ↔ 없음 (a 접촉점 · b 중심) | 되튐 · 임계각 |
| 16 | 12 | T–P 경로 접착 ↔ 없음 15–75° | 벗김 → 미끄럼의 실제 경로 |
| 17 | 13 | ★ 선 · 회전 · 소산 vs 충돌각 (접착) | 접착 소산 · U5 표적 |

### 5-1. 크롭 색인 — `litdb/figures/thorntonyin1991_oblique_impact_elastic_spheres_adhesion/`

- `fig_1` … `fig_17` (다시 자름 15 = 도구가 쪽 너비 전체를 잘라 이웃 단 글이 섞임 · 손 2 = 그림 10 (도구가 놓침) · 그림 13 (도구가 백지로 뺌)) · 캡션 포함 · 300 dpi (스캔 해상도).
- `eq_01_hertz_relative_approach` … `eq_53_kendall_criterion` (식 번호 순 · 뜻 = figures.json `mpm_note_ko`).
- 근거 글 20 (`txt_p<쪽>_<뜻>`): p1 초록 · 서론 (선형 스프링 · 단일 충돌 검증) · 탄성 전용 / p2 Mindlin 이력 · 증분 / p3 되돌림 갱신 · θ = 1 · 계산 입력 · 계산 순서 / p4 탄성 소산 · 법선 일 회수 / p5 그림 6 읽기 · Maw 실험 · Randall 일치 / p7 JKR · DMT · γ 정의 · Muller / p8 Savkoor–Briggs / p9 새 가설 · 포락선 · 재접착 없음 / p10–11 r₀ 조건 · PET 실험 / p11 기준 선택 · intractable · 접착 계산 입력 · 되튐 · 임계각 속도 의존 / p13 붙는 속도 (Reed) / p13–14 결론 · 한계.
- `digitized.csv` (248 행).

## 6. Post-processing ★

- 관측량: 처음 운동 에너지 대비 남은 선 운동 · 얻은 회전 · 소산 (그림 6 · 17) · 접촉점 반사각 · 중심 반발각 (그림 8 · 15 · 그림 7 정의) · T–P 경로 (그림 4a · 16) · T–δ (그림 4b · 12) · 에너지 시간 변화 (그림 5: 운동 · 법선 · 접선 · 회전 · 전체 일).
- 평균 · 앙상블 없음 (결정론적 두 구) · 오차 막대 없음.
- 검증: (a) 접착 없음 = Randall [3] 의 계산이 Maw 이론 [8] 과 *"exact quantitative agreement"* (p.6 · 이 논문 그림에 이론 · 실험점 없음) · (b) 정면 접착 충돌의 붙는 임계 속도 = JKR 이론 (Reed [21]) 과 일치 (서술만 · p.13) · (c) 정적 미끄럼 기준 = PET 마찰 실험 (그림 13–14).

## 7. 우리 DEM+MPM 대비 (우리 수치는 CLAUDE.md · 정본 카드가 적은 출처를 그 자리에)

### 7-1. 층위 — 접촉 힘–변위 법칙 층의 **접선 이력 · 접착** 축

이 논문은 입자 모양 · 소성 · 다입자 상호작용 층에는 오지 않는다.  **두 구 사이 접촉 법칙 하나** (접선이 이력을 기억하는 방법 · 접착이 미끄럼 기준을 바꾸는 방법) 의 원전이다.  frame[5] 로는 DEM 쪽 (접촉 법칙) 일이다.

### 7-2. ★ 계보 표 (이 카드 = 원문 확인 · TN1998 = [다른 카드])

| 단계 | 원전 (이 논문 목록) | 무엇을 더했나 | 이 논문 식 |
|---|---|---|---|
| 법선 탄성 | Hertz [4] (Johnson Contact Mechanics) | 접근량 · 접촉 반지름 · kⁿ = 2E*a | 1–6 |
| 접선 탄성 | Mindlin [5] (1949) | 무미끄럼 kᵗ = 8G*a · 부분 미끄럼 고리 | 16–18 · 35–36 |
| 접선 이력 | Mindlin–Deresiewicz [6] (1953) | 하중 이력 · 순간 컴플라이언스 (적분 불가) | (서술) |
| 증분 규칙 | Thornton–Randall [2] (1988) · Szalwinski [7] | 싣기 · 빼기 · 다시 싣기 θ · 되돌림 점 갱신 · θ = 1 규칙 | 7–15 |
| 접착 법선 | JKR [10] (1971) · DMT [11] · Muller [14] | 떼는 힘 · 유효 하중 · 가장자리 인장 · JKR/DMT 선택 변수 | 19–34 |
| 접착 접선 (벗김) | Savkoor–Briggs [18] (1977) | 접선력이 접촉을 줄임 · Tc | 35–41 |
| **이 논문** | — | 벗김 → 미끄럼 매끈한 전이 · T = μ(P + 2Pc) · P < −0.3Pc 에서 식 52 · 재접착 없음 · 두 구 충돌 소산 · 되튐 지도 | 42–53 |
| 대안 | Kendall [19] (1986) | T = μP′ (벗김 고려 없음) | 53 |
| 뒤 (7 년) | Thornton–Ning 1998 [다른 카드] | **법선 소성** (항복압 캡 p_y · 소성 제하 R_p*) + JKR · 붙는 속도 V_s (식 54) · 반발 계수 식 | — |

→ TN1998 이 더한 것 = **법선 쪽 소성 · 붙는 속도 · 반발 계수 닫힌 식** · 이 논문이 먼저 준 것 = **접선 이력 · 접착 접선 기준 · 비스듬한 충돌**.  둘을 합친 법칙 (소성 + 접착 + 접선) 이 이 논문 안에 있는지 = 없음.

### 7-3. 우리 쪽 법칙과 한 줄씩 (판정 없이)

| 항목 | 이 논문 | 우리 (출처) |
|---|---|---|
| 법선 | Hertz (탄성) · JKR (접착) | 압밀 DEM = `hooke/hysteresis` (Luding · 접착 없음) [우리 · CLAUDE.md] · 믹서 DEM = Hertz + SJKR 점착 (CED × 겹침 면적) [다른 카드 johnson1971 L196] |
| 접선 | Mindlin–Deresiewicz 증분 (θ · 되돌림 점 · 미세 미끄럼 소산) | LIGGGHTS `tangential history` = k_t = 8G*√(R*δn) 스프링 + Coulomb 자름 [다른 카드 boschpadros2014 L186 · L192] = 이 논문 식 (18) 의 **처음 강성을 늘 쓰는 꼴** (θ 규칙 · 미세 미끄럼 없음) [카드 해석] · 우리 덱의 접선 설정은 이 카드가 보지 않음 [미확인] |
| 소산 | 감쇠 0 · 미끄럼 (+ 접착 이력) 에서만 | LIGGGHTS 반발 계수 → 점성 감쇠 β [다른 카드 boschpadros2014 L192] — 이 논문 결론의 *"simple rules (e.g., coefficients of restitution)"* 쪽 |
| 접착 미끄럼 기준 | T = μ(P + 2Pc) (벗김 뒤) · 식 52 | SJKR 덱에서 Coulomb 상한이 어떤 법선력을 쓰는지 [미확인] (LIGGGHTS 소스 · 우리 덱 미확인) |
| E | 70 GPa (연화 없음) | DEM E_eff 1.35 GPa (18 배 연화) · MPM 1.53 GPa [우리 · CLAUDE.md] |
| ν | 0.3 | DEM 입력 0.3 · MPM 0.49 [우리 · CLAUDE.md] |
| 크기 | R 100 µm | SE r 0.5 µm (⌀ 1.0 · 생산 기본) [우리 · CLAUDE.md] |

### 7-4. ★ 붙는 속도 — 우리 믹서 dev-u 와 견줄 자리 (식의 꼴만 · 판정 없이)

- **이 논문**: 식 · 값 없음 (p.13 · ③).  정면 충돌 계산이 JKR 이론과 맞았다는 서술뿐 (Reed [21]).
- **JKR 계열 꼴 (TN1998 · [다른 카드 L70 · L136–L139])**: V_s = (14.18/m*)^{1/2}(Γ⁵R*⁴/E*²)^{1/6} (식 54) · 접촉 파괴 일 W_s = 7.09(Γ⁵R*⁴/E*²)^{1/3} (식 52) · 닿을 때 P = −8Pc/9 로 뛰어듦 · 떨어질 때 다른 점 → **힘–겹침 고리의 넓이 = 이력 소산** (감쇠 없이도).  같은 재료 구로 쓰면 V_s ∝ Γ^{5/6} R^{−5/6} E*^{−1/3} ρ^{−1/2} [카드 산술].
- **이 논문 계산에 대 보기** [카드 산술 §14-6]: Γ = 2γ = 0.4 J/m² → V_s **9.47 mm/s** · W_s 2.49 × 10⁻⁴ nJ = 처음 운동 에너지의 **0.90 %** · V/V_s ≈ 10.6 → 되튐 (e 0.9955) ↔ 그림 17 0° 소산 [판독] 0.7–1.1 % · 그림 15 정면 근처도 되튐 ✓.  (Γ = γ 로 읽으면 5.3 mm/s · 0.28 % → 판독과 덜 맞음.)
- **우리 쪽 [우리 · CLAUDE.md]**: 믹서 dev-u (U = 코팅 세계 LC 의 CED 전부 ×10 · ×14.42) 의 *"SE–SE 붙는 속도 상한 18.7 · 46.6 mm/s (벽 103 · 지금 모델 0.16 = 사실상 안 붙음)"*.  그 산술은 SJKR 식 기준이라고 johnson1971 카드 L222 가 적는다 [다른 카드] — 식 자체는 이 카드가 보지 않았다 [미확인].
- **꼴 비교 [카드 해석]**: SJKR 힘은 그 순간 겹침의 한 값 함수 (목 · 점프 없음 · δ → 0 에서 연속으로 0 [다른 카드 johnson1971 L222]) → 닫힌 경로 적분 = 0 → **점착 자체는 충돌 에너지를 뺏지 않고**, 붙음은 다른 소산 (점성 감쇠 · 마찰) 이 우물 깊이를 넘는 운동 에너지를 뺏을 때만 생긴다.  JKR 은 이력 고리 자체가 소산이다.  ⇒ **두 '붙는 속도' 는 같은 꼴이 아니다** (johnson1971 L222 의 *"충돌 포획 · 이탈 에너지 … JKR 과 다르다 [추정]"* 와 같은 방향).
- **연화의 몫 [카드 산술 · 꼴만]**: JKR 꼴 V_s ∝ E*^{−1/3} → E 를 18 배 무르게 하면 **× 2.62** · Muller 변수 ∝ E*^{−2/3} → **× 6.87** (JKR 쪽으로) · Pc = 3πγR* 는 E 무관 · Tc/Pc (P = 0) = 4√(G*/E*) 는 ν 만의 함수 (ν 0.3 → 1.815 · 0.37 → 1.758 · 0.49 → 1.644).  크기: R 100 → 0.5 µm 이면 같은 Γ · E · ρ 에서 V_s × 200^{5/6} ≈ **83** [카드 산술 — 꼴만 · LPSCl 값 아님].

### 7-5. 항목 대조표

| 항목 | 이 논문 | 우리 DEM | 우리 MPM | 비고 |
|---|---|---|---|---|
| 재료 | 이름 없는 탄성 구 (E 70 · ρ 2.65) | LPSCl · NCM (E_eff 1.35 GPa SE) | SE E 1.53 · σ_y 0.30 · ν 0.49 | 재료 다름 · 값 전이 0 |
| 소성 | 없음 | hooke/hysteresis (접촉 이력 · 형상 불변) | J2 (형상 변함) | 이 논문 = 탄성 |
| 압밀 | 없음 | 300 MPa · 순수 SE Heckel P_y 138 MPa | 300 MPa | 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 옆에 놓을 숫자 없음 |
| 최대 접촉 압력 | Hertz p₀ 0.63 GPa (0°) [카드 산술] | — | σ_y 0.30 GPa | 크기 자리만 (탄성 구 · 판정 아님) |
| 접착 | JKR γ 0.2 J/m² | 압밀 = 없음 · 믹서 = SJKR CED | `--coh` | §7-4 |
| 접선 | MD 증분 (이력) | tangential history (탄성 + Coulomb) | 연속체 (접촉 규칙은 A′-0) | §7-3 |
| 차원 | 구 · 평면 운동 | 3D | 2D · 3D | — |

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정하지 않음.  **이 논문의 값은 전부 랩 표준과 다른 재료 (이름 없는 탄성 구 · PET) 의 문헌 값**이다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 없음 (기공 · 진밀도 0) · 간접: *"it is essential that such apparently simple simulations be performed in order to validate the new algorithms"* (p.1) — 새 접촉 규칙은 **단일 충돌 시험** 을 먼저 통과시키라는 원칙 | 랩 표준 옆에 놓을 숫자 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 간접: 두 구 충돌의 해석 · 계산 기준표 (그림 6 · 8 · 15 · 17) 를 접촉 코드 단위 시험의 표적으로 | 2D 가 아님 (구 해) · MPM 아님 |
| **단계 3** (2D 접촉 표현만 바꿔 누르는 힘 비교) | 같은 꼴의 설계 (충돌판): **같은 입력에서 접착 γ 하나만** 0 ↔ 0.2 로 바꿔 소산 · 회전 · 반발각을 견줌 (그림 6 ↔ 17 · 그림 15) — 한 매개변수만 바꾼 비교의 예 | 압축 아님 · 힘 비 없음 |
| **단계 4** (3D 순수 SE · 항복 세기 하나를 실험 기공에 맞춤) | 없음 (소성 0) | — |
| **단계 5** (3D 복합 AM + SE) | 없음 (한 재료 · 두 구) | — |
| **단계 6** (탈압 · 되돌아옴) | 탄성 접촉의 **법선 일은 다 돌아오고 접선 일은 일부만** (p.4 · 그림 5) → 되돌아옴을 법선 탄성 몫 · 접선 미끄럼 몫으로 나눠 적는 꼴 · 접착 접촉의 떨어짐 조건 (Pc · Tc · 식 40 · 42) | 소성 되돌아옴 · 잔류 변형 0 · 압밀 탈압 0 |
| **단계 7** (형상 · 피복 · 수송) | 접착 접촉 반지름이 Hertz 보다 크다 (식 25 · 하중 0 에서도 a₀ = 0.716 µm [카드 산술]) · 벗김 뒤 a* (식 41) — 접촉 면적 규약 (Stage-E 면적) 의 '접착이 키운 면적' 자리 | 수송 · 피복 계산 0 · 탄성 · 작은 변형 |
| **후보 D0** (지금의 DEM) | ★ D0 접선 법칙 점검표: Mindlin–Deresiewicz 증분 (θ · 되돌림 점) ↔ LIGGGHTS `tangential history` (식 18 강성 + Coulomb [다른 카드]) — 후자는 강체 미끄럼 전 미세 미끄럼 소산이 없다 [카드 해석] · 결론 *"no simple rules (e.g., coefficients of restitution …)"* 는 D0 의 반발 계수 감쇠에 대한 한정어 | 압밀 영역 · 큰 겹침 · 연화 E 에 대한 말 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | ★ 접착 접촉의 **분리 · 미끄럼 규칙 꼴**: 떼는 힘 Pc (19) · 벗김 Tc (40) · 미끄럼 μ(P + 2Pc) (42) · P < −0.3Pc 식 (52) · 재접착 없음 (가정) — SE 냉간 접합 접촉 규칙을 세울 때의 후보 꼴 | 힘 수준 기준 → 연속체 견인 수준으로 옮기려면 접촉 면적 규약이 필요 [카드 해석] · 탄성 |
| **후보 A** (MPM · AM 강체 + SE 한 속도장) | 없음 | — |
| **후보 A′** (MPM · 입자별 속도장) | ★ **다물체 마찰 접촉 검증 표적**: 같은 탄성 구 두 개 비스듬한 충돌 · 반발각 · 에너지 지도 (그림 6 · 8) · *"The rebound trajectories are independent of impact velocity if there is no adhesion"* (p.12) → 계산하기 쉬운 속도로 돌려도 같은 표적 (μ · ν 만) | 실험점 없음 (Maw 실험은 이 논문 그림에 없음 · Randall 학위논문 [3] 경유) · 탄성 |
| **후보 B** (입자별 FE · MPFEM · NSCD) | 저자가 *"intractable"* · *"not a rigorous solution"* 이라 한 접착 접선 응답을 FE 가 기준해로 줄 자리 [카드 해석] | FE 결과 0 |
| **후보 C** (MDR 류 큰 변형 접촉) | 접선 증분 규칙 (식 7–15) 은 법선 법칙이 주는 a 만 쓴다 → 다른 법선 법칙 위에도 얹을 수 있는 꼴 [카드 해석] | 큰 변형 · 부피 보존 0 |
| **후보 C′** (항복 캡 탄소성 + 다접촉 보정) | ★ Thornton 계열 법칙의 **접선 · 접착 반쪽** (법선 소성 반쪽 = TN1998 [다른 카드]) — C′ 을 세울 때 접선은 이 논문 · 법선은 TN1998 | 소성 접촉 위의 접선 · 접착 규칙은 이 논문에 없다 [미확인] |
| **후보 M0** (균질화 캡 소성) | 없음 | — |
| **U0** (접촉 끈 것과 같은지) | 영 점검의 꼴: γ = 0 → JKR 식 (25) = Hertz 식 (2) · 식 (42) = μP — 접착 코드를 γ = 0 으로 돌리면 접착 없음 결과 (그림 6 · 8) 와 같아야 [카드 해석] | 원문에 그 시험 서술 없음 |
| **U1** (입자 하나 압축 · 해상도) | Hertz 해 (식 1–6) — 두 구 탄성 접촉의 해석 표적 (이 논문 값: α_max 32.6 nm · a 1.28 µm · P 2.13 mN · 0° [카드 산술]) | 해상도 규칙 없음 |
| **U2** (경사면 마찰 접촉 회귀) | ★ 마찰 미끄럼 회귀: 45–75° 처음 경로 T = μP (그림 4a) · 그림 13–14 의 T–P 선 (접착 미끄럼) | 경사면 시험 그 자체는 아님 |
| **U3** (단단한 구를 소성 블록에 눌렀다 떼기) | 없음 (소성 0) | — |
| **U4** (판 분리) | 접착 접촉이 떨어지는 힘의 해석 꼴 (Pc · 그림 9) | 판 · 소성 0 |
| **U5** (비슷한 강성 입자끼리 충돌 · 다물체) | ★★ **바로 이 시험**: 같은 구 두 개 · θ 0–90° · 접착 0 / 0.2 J/m² · 표 (그림 6 · 8 · 15 · 17 · digitized.csv) · 접착 없음은 속도 무관 | 탄성 · 소성 0 · 실험 대조 없음 (저자도 실험 부재를 적음) |
| **U6** (작은 조밀 충전 해상도 수렴) | 없음 | — |
| **조건 R1** (AM 이 움직이고 하중을 나눔) | 없음 | — |
| **조건 R2** (미끄럼 · 분리) | ★ **채움 (탄성 · 접착 접촉 한정)**: 미세 미끄럼 · 강체 미끄럼 · 벗김 · 떼는 힘 · 재접착 없음 · stick-slip 조건 (P < P*) | 소성 접촉 · 다입자 0 |
| **조건 R3** (SE 입자 경계 기억) | 간접: 접촉 수준의 이력 기억 (되돌림 점 T* · T\*\* · θ) | 입자 경계 기억과는 다른 것 |
| **조건 R4** (탈압 · 되돌아옴) | 부분: 법선 탄성 회수 · 접선 일부 회수 (그림 5) | 소성 0 |
| **조건 R5** (맞추는 값은 모델마다 하나) | ✅ 계산 = 맞춤 0 (입력 고정) · 실험 대조 = 기준마다 μ 하나 (0.35 · 0.30) | μ 를 고른 방법 서술 없음 |
| **조건 R6** (SE 입자 형상 변형) | 없음 (구 · JKR 목은 해석 안에서만) | — |
| **조건 R7** (AM 파괴) | 없음 | — |
| **결과 전 대조 항목** | ① U5 표 (θ 별 소산 · 회전 · 반발각 · 접착 0 / 0.2) ② 정면 접착 충돌 소산 ≈ 0.9 % (JKR · 이 입력) ③ 접착 첫 접촉 법선력 −8Pc/9 ④ 그림 12 의 Tc · 미끄럼 값 (P = 0 · 10 mN) — 결과 전에 **어느 법칙 (JKR / SJKR) 의 표적인지** 적는다 | 값 앵커 아님 (재료 다름) |

## 9. 적용 인사이트 (행동)

- ① **U5 벤치마크 등록 후보**: 그림 6 · 8 · 15 · 17 (digitized.csv) — 입자별 속도장 MPM (A′) · DEM 접선 법칙 점검 · 결과 전 대조 항목으로 (접착 없음 = 속도 무관 · μ 0.35 · ν 0.3).
- ② **우리 DEM 접선 법칙 확인 (덱 · 소스)**: `tangential history` 가 식 (18) 고정 강성 + Coulomb 인지 · 미세 미끄럼 (θ) 이 없는지 — 믹서 · 압밀 덱 각각 (이 카드는 덱을 보지 않음).
- ③ **믹서 '붙는 속도' 서술에 꼴 표지**: JKR 꼴 (이력 소산 · V_s ∝ Γ^{5/6}R^{−5/6}E*^{−1/3}ρ^{−1/2}) ↔ SJKR (이력 0 · 감쇠가 정함) — 연화 E 의 몫 (JKR 꼴이면 × 2.62) 을 결과 전에 적기.
- ④ **pfeffer2001 L302 카드 문제 보고** (§13) — '탄소성' → '탄성' (고치는 일은 그 카드 담당).
- ⑤ **n (정독 출력)**: Reed [21] · Savkoor–Briggs [18] · Mindlin–Deresiewicz [6] · Maw 1981 [9] · Thornton–Randall [2] (§12).

## 10. 인용 가능 문장 (deck/paper 용 — 표지 그대로)

- "Thornton & Yin simulated oblique impacts of two identical elastic spheres (R = 100 µm, E = 70 GPa, ν = 0.3, μ = 0.35, relative velocity 0.1 m/s) using a Hertz normal law and the Mindlin–Deresiewicz tangential law applied incrementally; with no damping, energy was still dissipated by micro-slip and sliding, and they concluded that 'there would appear to be no simple rules (e.g., coefficients of restitution, scattering probability) that will satisfactorily achieve this' (Thornton & Yin, Powder Technol. 65 (1991) 153–166)."
- "Their work is explicitly 'restricted to elastic spheres (plastic deformation at the contact is not considered)' (Thornton & Yin 1991, p. 153)."
- "For adhesive (JKR) elastic spheres they proposed that the contact first peels (Savkoor–Briggs) and then slides at T = μ(P + 2Pc), noting that the resulting theory 'is not a rigorous solution, due to the approximations in existing theories and the speculative nature of the proposed sliding criteria' (p. 166)."
- (우리 해석 표기 필수) "Thornton & Yin (1991) do not give a sticking-velocity formula; for colinear impacts they state agreement with JKR theory (citing Reed 1987). A JKR-type capture energy comes from adhesion hysteresis, whereas a cohesion force that is a single-valued function of overlap (e.g., SJKR) returns all its work over a closed path — **this is our reading, not the authors' claim.**"

## 10-1. 쉽게 말하면

구슬 두 개가 비스듬히 부딪히면 미끄러지고 굴러서, 완전히 탄성인 구슬이어도 에너지가 조금 빠지고 튀어나가는 방향이 충돌각에 따라 이상하게 변한다.  이 논문은 그 접선 방향 힘이 '지난 이력을 기억하는' 공식을 계산에 넣었고, 표면이 서로 달라붙으면 (JKR) 먼저 '벗겨진 다음 미끄러진다' 는 새 규칙을 만들어 섬유 마찰 실험과 맞춰 보았다.  달라붙으면 살짝 비스듬히 부딪힌 구슬이 오던 길로 되튀기도 한다.  하지만 구슬은 탄성일 뿐 찌그러지지 않고 (소성 없음), 언제 아예 붙어 버리는지 (붙는 속도) 는 이 논문에 식이 없다.

## 11. 주의/한계 (over-claim 방지)

**논문 자신의 한계 (저자 명시)** — §4-9 · p.10 (r₀ ≥ a* 는 P < −0.3Pc 에서 깨짐 · r₀ 가정이면 실험과 더 맞음) · p.11 (비선형 접선 해석 intractable · 식 52 ↔ 식 40 불일치) · p.7 (JKR · DMT 는 근사).

**우리가 추가로 다는 한계**
- ⚠ **두 구 · 충돌 한 번 · 탄성 · 감쇠 0** — 압밀 · 다입자 · 소성 · 큰 변형 0.  재료 이름 없음.
- ⚠ **실험 대조가 둘 다 간접**: 접착 없음 = Randall 학위논문 [3] 의 계산이 Maw 이론 [8] 과 맞았다는 서술 (실험 [9] 의 점은 이 논문 그림에 없음 — 초록의 *"excellent agreement with the experimental work of Maw et al."* 은 본문에서 이 경로로만 뒷받침) · 접착 = 정적 마찰 (PET 단섬유) 이고 충돌이 아님.
- ⚠ **μ 는 기준마다 따로 고른 값** (0.35 · 0.30) · Pc 1.6 µN 외의 실험 조건 [미확인].
- ⚠ **붙는 속도 · 반발 계수 곡선 없음** — 정면 충돌의 임계 속도는 서술만 (Reed [21]).
- ⚠ **그림 11 의 매개변수 미기재** (peel 선이 ν 0.3 식보다 5–6 % 아래 [판독 · 카드 산술]).
- ⚠ **기호 겹침 · 오식** [카드 확인]: Muller 변수와 마찰 계수가 같은 μ · 그림 9 의 α_c 정의 없음 · 그림 2 · 12 는 법선력을 N (본문 P) · 그림 12 의 *"T = μN"* = μ(P + 2Pc) · 그림 15 캡션 *"contact pitch"* (= patch) · 본문 *"positive square root in eqn. (46)"* (± 는 식 45) · 결론 *"Savkoor and Briggs [5]"* (= [18]) · 본문 그림 6 설명은 *"percentage loss"* 인데 그림 축은 남은 몫 (0–1).
- ⚠ **스캔 판독 오차**: 표지 겹침 구간 (그림 6 · 10–30° · 그림 15a 60°) 은 눈 판독 · 그림 4 · 5 · 16 은 요점만 눈으로.
- ⚠ **소재가 배터리가 아니다** — E 70 GPa 탄성 구 ↔ LPSCl E 22–24 GPa (실제) · DEM 1.35 GPa (연화) [우리].  옮길 수 있는 것 = 법칙의 꼴 · 시험 설계 · 관측량 정의 · 결론의 방향.

## 11-1. [미확인] 목록 (본문 14 쪽 전수에 없음)

1. DOI (인쇄 없음 · PDF 문서 정보 PII 0032-5910(91)80178-L) · 접수 · 게재 날짜.
2. 재료 이름 (E 70 GPa · ρ 2.65 Mg/m³ 구).
3. 시간 간격 · 사이클 수 · 계산 시간 · 프로그램 이름 · 2D/3D 여부.
4. **붙는 임계 속도 식 · 값** (정면 · 비스듬) — Reed [21] · *"subsequent paper"*.
5. 반발 계수 vs 충돌 속도 곡선.
6. 그림 9 · 10 · 11 의 계산 매개변수 (μ · ν · G*/E*) · α_c 정의.
7. Muller 변수의 z₀ → 이 계산의 JKR/DMT 판정.
8. Briscoe–Kremnitzer 시편 기하 · E · R · 하중 절대값 · μ 를 고른 방법.
9. Maw 실험 [9] 의 수치 (이 논문 그림에 없음).
10. 접착 계산의 임계 충돌각이 속도에 따라 바뀌는 수치 (서술만 · p.12–13).
11. 접착 계산이 'P < −0.3Pc' 구간에 실제로 들어갔는지 · 그 빈도.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 원문 서지 | 왜 | 정본 litdb |
|---|---|---|---|
| [21] | J. Reed, in B. J. Briscoe and M. J. Adams (eds.), Tribology in Particulate Technology, Adam Hilger, Bristol, 1987, p. 123. | 정면 접착 충돌의 **붙는 임계 속도** (JKR) — 이 논문이 넘긴 곳 · 우리 믹서 dev-u 붙는 속도 꼴 대조 | 없음 (파일 목록 · grep "Tribology in Particulate" 0 건 · 'Reed' 는 다른 Reed) |
| [18] | A. R. Savkoor and G. A. D. Briggs, Proc. Roy. Soc. Lond., A. 356 (1977) 103. | 접착 접촉의 벗김 (Tc) 원전 — 질문 e · R2 | 없음 (grep "Savkoor" 0 건) |
| [6] | R. D. Mindlin and H. Deresiewicz, J. Appl. Mech., Trans. ASME, 20 (1953) 327. | 접선 이력 법칙의 원전 — D0 접선 (LIGGGHTS) 점검 · U2 | 없음 (여러 카드에 인용만) |
| [9] | N. Maw, J. R. Barber and J. N. Fawcett, J. Lubrication Tech., Trans. ASME, 103 (1981) 74. | 비스듬한 충돌 실험 (공기 받침 · 퍽 · 스트로보) — U5 실험 표적 | 없음 (grep "Maw" 0 건) |
| [2] | C. Thornton and C. W. Randall, in M. Satake and J. T. Jenkins (eds.), Micromechanics of Granular Materials, Elsevier, Amsterdam, 1988, p. 133. | 증분 규칙 (식 7–15) 의 원전 · Δt_crit 식 (ai2011 카드가 인용) | 없음 (ai2011 카드에 인용만) |
| [8] | N. Maw, J. R. Barber and J. N. Fawcett, Wear, 38 (1976) 101. | 비스듬한 충돌 이론 (되튐) — Randall 계산이 맞춘 대상 | 없음 |
| [20] | B. J. Briscoe and S. L. Kremnitzer, J. Phys. D: Appl. Phys., 12 (1979) 505. | 접착 마찰 실험 원자료 (Pc 1.6 µN) | 없음 |
| [19] | K. Kendall, Nature, 319 (1986) 203. | T = μP′ 기준 원전 | 없음 |
| [14] | V. M. Muller, V. S. Yushchenko and B. V. Derjaguin, J. Colloid Interface Sci., 77 (1980) 91. | JKR/DMT 전이 변수 (식 21) | 없음 |
| [3] | C. W. Randall, Ph.D. thesis, Aston Univ. (1989). | 접착 없음 검증 (Maw 이론과 일치) 의 실제 근거 | 없음 |
| [10] | K. L. Johnson, K. Kendall and A. D. Roberts, Proc. Roy. Soc. Lond., A, 324 (1971) 301. | JKR | ✅ `johnson1971_jkr_surface_energy_contact_elastic_solids` |
| [11] | B. V. Derjaguin, V. M. Muller and Y. P. Toporov, J. Colloid Interface Sci., 53 (1975) 314. | DMT | ✅ `dmt1975_adhesion_contact_deformation` |
| [1] | P. A. Cundall and O. D. L. Strack, Geotechnique, 29 (1979) 47. | DEM 원전 | 없음 (파일 목록에 cundall* 없음) |
| [4] · [5] · [7] · [12] · [13] · [15] · [16] · [17] | Johnson Contact Mechanics (1985) · Mindlin (1949) · Szalwinski (1985) · Tabor (1978) · Horn et al. (1987) · Muller et al. (1983) · Greenwood–Johnson (1981) · Johnson (1976) | 배경 | 확인 안 함 (우선순위 낮음) |

## 13. ★ 가리킨 카드 대조 · 카드 문제 (고치지 않음 — 정독 출력 `batch_73_findings.md` 끝 절에도 같은 목록)

1. **`pfeffer2001_dry_particle_coating_engineered_particulates` L302**: *"| 117 | C. Thornton, K.K. Yin, Powder Technol. 65 (1991) 153–166. | 탄소성 접촉 — 카드 없음 |"* — 서지 (저자 · 학술지 · 권 · 쪽 · 연도) 는 원문과 같다.  **'탄소성 접촉' 은 원문과 다르다**: 원문은 *"restricted to elastic spheres (plastic deformation at the contact is not considered)"* (p.1) · 제목 *"Impact of elastic spheres with and without adhesion"*.  탄소성 접촉 법칙은 같은 그룹의 Thornton–Ning 1998 (정본 `thorntonning1998_…`) 의 일이다.  (그 카드 본문에는 [117] 을 쓰는 줄이 없다 — 원 논문이 [117] 을 어떤 뜻으로 인용했는지는 [미확인].)
- (관찰 · 문제 아님) `tovar2026_…` L86 · L87 · L343 = 원문과 맞다 (Mindlin–Deresiewicz 접선 이력 · Coulomb · 강성 K_c).  L87 의 감쇠 식 (21)(22) 는 이 논문에 없지만 카드는 강성만 [47] 로 돌린다.
- (관찰 · 가리킨 카드 아님 · 고치지 않음) `boschpadros2014_dem_liggghts_msc_thesis` L187 의 *"1/G* = 2(2+ν₁)(1−ν₁)/Y₁ + 2(2+ν₂)(1−ν₂)/Y₂ (4.7)"* ↔ 이 논문 식 (10) 1/G* = (2−ν₁)/G₁ + (2−ν₂)/G₂ = 2(2−ν₁)(1+ν₁)/E₁ + … [카드 산술 · G = E/(2(1+ν))] — 두 꼴이 다르다 (ν 0.3 에서 1.61 ↔ 2.21 · G* 1.37 배).  그 thesis 원문 · LIGGGHTS 문서의 인쇄를 이 세션에서 보지 않아 옮김 문제인지 원문 문제인지 [미확인].  (같은 카드 L186 의 k_t = 8G*√(R*δn) 는 이 논문 식 (18) 과 같은 꼴 ✓.)
- (관찰) 후보 표 N-33 의 서지 상태 *"일부만 (제목 없음)"* → 원문 제목 *"Impact of elastic spheres with and without adhesion"*.

## 14. 🧮 카드 산술 원장 (원문 숫자 · 판독값만으로 · 재현 = 식 그대로)

**14-1. 질량 · 환산량 · Hertz 충돌.**  m = ρ(4/3)πR³ = 2650 × 4.18879 × 10⁻¹² = **1.110 × 10⁻⁸ kg** · m* = m/2 = 5.55 × 10⁻⁹ kg · R* = R/2 = 50 µm · E* = E/(2(1 − ν²)) = **38.46 GPa** · G = E/(2(1 + ν)) = 26.92 GPa · G* = G/(2(2 − ν)) = **7.919 GPa** · G*/E* = (1 − ν)/(2(2 − ν)) = **0.2059**.  처음 운동 에너지 = 2 × ½m(0.05)² = **0.02775 nJ** (= ½m*v_rel² · 그림 5 ≈ 0.0277 [판독] ✓).  식 (1) 을 에너지 균형 ½m*v_n² = (8/15)E*√R* α^{5/2} 에 넣어 α_max = (15m*v_n²/(16E*√R*))^{2/5} · v_n = 0.1 cos θ · 접촉 시간 t_c = 2.94 α_max/v_n (표준 Hertz 충돌 적분 — 이 논문에 인쇄 안 됨) · a = √(R*α) · p₀ = 2aE*/(πR*) (식 31):

| θ (°) | α_max (nm) | P_max (mN) | t_c (µs) | a (µm) | p₀ (GPa) |
|---|---|---|---|---|---|
| 0 | 32.6 | 2.131 | 0.958 | 1.276 | 0.625 |
| 15 | 31.7 | 2.044 | 0.965 | 1.258 | 0.616 |
| 30 | 29.0 | 1.793 | 0.986 | 1.205 | 0.590 |
| 45 | 24.7 | 1.406 | 1.027 | 1.111 | 0.544 |
| 60 | 18.7 | 0.927 | 1.101 | 0.967 | 0.474 |
| 75 | 11.0 | 0.421 | 1.256 | 0.743 | 0.364 |
| 80 | 8.0 | 0.261 | 1.360 | 0.633 | 0.310 |

  α_max/R = 3.26 × 10⁻⁴ (0°).  그림 4a · 16 의 P_max · 그림 5 의 접촉 시간과 맞음 (§3-2).
**14-2. 그림 6 · 17 합.**  남은 선 + 회전 + 소산 = 1.000–1.011 (그림 6) · 0.989–1.002 (그림 17) → 그려진 선 운동 = 남은 몫.  접착 없음 25° 소산 = (0.033 + 0.068)/2 ≈ 0.05 (보간).
**14-3. JKR · 벗김 · 미끄럼 (γ 0.2 · 식 19 · 25 · 34 · 40–46).**  Pc = 3πγR* = **0.0942 mN** · −8Pc/9 = −0.0838 mN (TN1998 의 뛰어듦 [다른 카드 L135] · 그림 16 ≈ −0.08 [판독] ✓) · a₀ (P = 0) = ((3R*/(4E*))·4Pc)^{1/3} = **0.716 µm** · a_c = 0.451 µm · 8G*a₀ = 0.0454 mN/nm (그림 12b 처음 기울기 ≈ 0.041 [판독]).  P = 10 mN: Tc = 4[(PPc + Pc²)G*/E*]^{1/2} = **1.770 mN** · a* = 2.150 µm · δc = Tc/(8G*a*) = **13.0 nm** · μ(P + 2Pc) = **3.566 mN** · δs = 39.3 nm (그림 12a: 1.78 · ≈13 · 3.55 [판독] ✓).  P = 0: Tc = **0.1711 mN** · a* = 0.569 µm · δc = **4.75 nm** · 2μPc = **0.0660 mN** (그림 12b: 0.1713 · 4.75 · 0.0667–0.0672 [판독] ✓).  χ = 4G*/(μ²E*) = **6.723** → P*/Pc = 23.85 (T/Pc = μ(P* + 2)/1 = 9.05) · 다른 근 −0.96 · P* = 2.25 mN.
**14-4. r₀ ≥ a* 교차 (식 47–49).**  n = −0.9: 0.817 · −0.5: 0.974 · −0.33: 0.9994 · **−0.325: 1.000** · −0.3: 1.003 · 0: 1.029 · 10: 1.065 → 원문 *"except when P < −0.3Pc"* ✓.
**14-5. 식 (42) · (52) 값 (μ 0.35 / 0.30).**  P = 0: P′ = 4Pc · (P′ − P)/(3P′) = 1/3 → (2/3)^{3/2} = 0.5443 → 식 52 = 2.177μPc = **0.762** (0.35) · **0.653** (0.30) · 식 42 = 2μPc = 0.70.  P = −Pc: P′ = Pc → (1/3)^{3/2} = 0.1925 → 식 52 = 0.067 (0.35) · 0.058 (0.30) · 식 42 = 0.35.  P = 25Pc: 식 42 (0.35) = 9.45 · P′ = 27 + 2√26 = 37.198 → (1 − 12.198/111.59)^{3/2} = 0.8406 → 식 52 (0.30) = **9.38**.
**14-6. 붙는 속도 · 접착 소산 (TN1998 식 52 · 54 [다른 카드 L136–L138]).**  Γ = 2γ = 0.4 J/m²: X = Γ⁵R*⁴/E*² = 4.33 × 10⁻⁴¹ · V_s = (14.18/m*)^{1/2}X^{1/6} = **9.47 mm/s** · W_s = 7.09 X^{1/3} = **2.49 × 10⁻⁴ nJ** = 처음 운동 에너지의 **0.90 %** · V/V_s = 0.1/0.00947 = 10.6 → e = [1 − (V_s/V)²]^{1/2} = 0.9955 (TN1998 식 57 [다른 카드 L139]).  Γ = γ = 0.2 로 읽으면 5.32 mm/s · 0.28 %.  ↔ 그림 17 0° 소산 0.007–0.011 [판독].
**14-7. 비례 (꼴만).**  V_s ∝ (Γ⁵R*⁴/E*²)^{1/6}/√m* · 같은 재료 구 (R* = R/2 · m* ∝ ρR³) → V_s ∝ Γ^{5/6}R^{−5/6}E*^{−1/3}ρ^{−1/2}.  E* ÷ 18 → V_s × 18^{1/3} = **2.62** · Muller 변수 ∝ E*^{−2/3} → × 18^{2/3} = **6.87** · R 100 → 0.5 µm → V_s × 200^{5/6} = **82.7**.  Tc/Pc (P = 0) = 4√(G*/E*) = 4√((1 − ν)/(2(2 − ν))): ν 0.3 → 1.815 · 0.36 → 1.767 · 0.37 → 1.758 · 0.49 → 1.644 · χ (μ 0.35): 6.72 · 6.37 · 6.31 · 5.51.
**14-8. 그림 11 peel 선 점검.**  식 (40) 을 Pc 로 나누면 Tc/Pc = 4[(n + 1)G*/E*]^{1/2}: ν 0.3 → n = 1: 2.57 · 10: 6.02 · 25: 9.26 ↔ 판독 2.53 · 5.69 · 8.73 (−1 … −6 %) · G*/E* = 0.183 이면 2.42 · 5.67 · 8.73 · χ = 5.98 → 교점 P*/Pc 20.9 · T/Pc 8.0 (판독 교점 ≈ 21–23 · 8.0–8.3 과 맞음) [카드 산술] → 그림 11 의 G*/E* (또는 ν · 같은 재료면 ν ≈ 0.42) 가 0.3 의 값과 다를 수 있다 [미확인 · 원문에 매개변수 없음].  slide 선 0.35(n + 2): n = 2 1.40 · 5 2.45 · 10 4.20 · 20 7.70 · 25 9.45 ↔ 판독 1.44 · 2.46 · 4.20 · 7.61 · 9.29 (±3 % 안).
**14-9. G* 두 꼴 (§13 관찰).**  같은 재료: 이 논문 식 (10) → 1/G* = 2(2 − ν)/G = 4(2 − ν)(1 + ν)/E (몸 하나 몫 2(2 − ν)(1 + ν)/E = 4.42/E · ν 0.3) ↔ boschpadros L187 몸 하나 몫 2(2 + ν)(1 − ν)/Y = 3.22/Y → 비 1.37.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)

- 본문 14 쪽 = 쪽마다 스캔 한 장 (래스터) + OCR 글자 층.  글자 층은 숫자 · 기호가 깨진다 (예: *"PC = 1.6 pN"* = 렌더로 확인한 *"Pc = 1.6 µN"* · *"( 10.05 m/s)"* = *"(±0.05 m/s)"* · *"R = 100 pm"* = *"R = 100 µm"*) → 이 카드의 인용 · 식은 전부 300 dpi 렌더 (크롭) 로 확인.
- 서지 = PDF 1 쪽 머리글 *"Powder Technology, 65 (1991) 153-166"* · 제목 · 저자 · 소속 · 초록 · 아래 줄 *"0032-5910/91/$3.50 © Elsevier Sequoia/Printed in The Netherlands"*.  PDF 문서 정보의 제목 칸 = *"PII: 0032-5910(91)80178-L"* · 저자 칸 비어 있음 · DOI 인쇄 없음.
- 글자 층 낱말 점검: 'plastic' 1 (p.1) · 'restitution' 1 (p.13) · 'stick' 8 (p.2 Mindlin 붙음 구역 · p.9 stick-slip · p.13 stick together · sticking · p.14 *"sticking occurs"*) · 'Reed' 2 (p.13 · 목록) · 'Maw' (p.1 · 5 · 6 · 목록) · 'damping' 0 · 'dashpot' 1 (p.1).
- 식 53 개 전부 300 dpi 크롭으로 확인 (식 번호 포함) · 그림 17 개 · 근거 글 20 개 열어 확인 · 모음 그림 (세션 scratchpad).
- 그림 판독: 스캔이라 벡터 없음 · 눈금 픽셀 보정 + 표지 무게중심 (겹침 = 눈) · 카드 산술 (Hertz · JKR · 식 40–52) 과 그림 4 · 5 · 12 · 13 · 16 · 17 이 맞음을 확인 (§14).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (ls-tree · 551 개 · 이 카드 전) + "Thornton … Yin" · "Savkoor" · "Maw" · "Kremnitzer" · "Deresiewicz" grep — **이 논문 카드 없음** (pfeffer2001 · tovar2026 에 인용만).  같은 저자 다른 카드 = `thorntonning1998_adhesive_elastoplastic_contact` (다른 논문 · 1998) → slug 를 다르게 · 서로 '관련 카드' 한 줄.

## 🔗 관련 카드
- 같은 그룹 · 다른 논문 (법선 탄소성 + 접착 · 붙는 속도 식): [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) — 계보 §7-2.
- 이 논문을 가리킨 카드: [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (L302 · '탄소성' 표기 = 카드 문제 §13) · [`tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond`](tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond.md) (L86 · L87 · L343 · 맞음).
- 접착 원전 · 대조: [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (JKR · SJKR 대응 §7-1 · 7-2) · [`dmt1975_adhesion_contact_deformation`](dmt1975_adhesion_contact_deformation.md).
- 우리 쪽 법칙: [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (hooke/hysteresis) · [`boschpadros2014_dem_liggghts_msc_thesis`](boschpadros2014_dem_liggghts_msc_thesis.md) (LIGGGHTS tangential history · SJKR).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
