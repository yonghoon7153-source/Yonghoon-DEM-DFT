<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018_… · ender2011_… (같은 날 앞 묶음) · 메타 줄 형식 = arzt1982_… (DOI 미인쇄 동류 카드).
     원문 = 17 쪽 스캔본 · SI 없음 · 영문 본문 + 독문 요약 (Zusammenfassung).
     쪽 표기 = 인쇄 (학술지) 쪽.  PDF n 쪽 = 인쇄 (258 + n) 쪽 → PDF 1 = p.259 · PDF 5 = p.263 · PDF 15 = p.273 · PDF 17 = p.275.  식 · 그림 번호 = 원문.
     판독 규약: 텍스트층 OCR 이 깨져 있다 (ε → "e"/"E" · κ → "K" · ρ → "p" · Schüttgüter → "Schiittgiiter" 등).  식 · 수치 · 그림 축은 전부 쪽 이미지 (2× 전쪽 + 식 영역 3.5–4× 확대) 에서 읽었다.
     값 표지: stated = 본문 · 캡션 원문 / 판독 = 그림에서 읽은 값 (추세 전용) / 파생 = 카드 작성자 산술 (식 명시 · 원문 값 아님). -->
# Theory of Yield of Cohesive Powders — 응집 분말의 항복 이론: 무작위 단분산 구 충전의 외부응력 ↔ 평균 접촉력 (식 4 · 부록 A — Arzt 1982 식 (20) 의 원전) · 소성 평탄화 (p_f ≈ 3σ_f) 로 "얼린" 반데르발스 응집력 H = κN · 유효 항복궤적 tan φ_e = (1+κ) tan ρ — Molerus (Powder Technol. 1975)
> slug `molerus1975_theory_of_yield_cohesive_powders` · DOI `[미확인]` · type `theory (analytic powder micromechanics: mean-field contact-force transmission in a random monodisperse sphere packing + Hertz/plastic-flattening van der Waals cohesion + Mohr–Coulomb yield loci) + literature shear-test comparison` · PDF `28. Theory of yield of cohesive powders.pdf` · digested `2026-10-03` · status ✅
>
> 원문 = Powder Technology, 12 (1975) 259–275 · © Elsevier Sequoia S.A., Lausanne — Printed in The Netherlands · Received December 9, 1974; in revised form April 17, 1975 · 단독 저자 O. Molerus (Institut für Mechanische Verfahrenstechnik der Universität Erlangen-Nürnberg, West Germany).  OA 표시 없음 · 사사 절 없음.
> ⚠ **DOI 가 PDF 에 인쇄돼 있지 않다** (17 쪽 텍스트층 검색 0 건 · 머리말에도 없음) → `[미확인]`.  지어내지 않는다.  서지는 p.259 머리말로 확정했다.
> ★ **이 카드가 맡는 일** = 판단 메모 v2 §8-2 의 **"힘 ↔ 외부압 f = 4πp/(ZD) — Arzt (20) 평균장의 원전"** (§6-3 · C1) 과 결정 9 (LHS-25 접촉별 추정량).  이 논문을 인용하는 정본 카드 = `arzt1982_particle_coordination_densification_spheres` (Arzt ref [14]).
> ★ **판정 한 줄** — 원문에 "f = 4πp/(ZD)" 문자열은 없다.  있는 것은 **σ = (F/d²)·k(1−ε)/π (식 4, p.263) = (F/4r²)·k(1−ε)/π (A7, p.273)** 이다.  F 로 풀면 F = 4πr²σ/[k(1−ε)] — Arzt 기호 (f = F · p = σ · Z = k · D = 1 − ε) 에 **R = r = 1** 을 넣은 것이 4πp/(ZD) 다 (지름 d 로 쓰면 상수는 π).  전제는 단분산 · 무작위 · 등방 · **점 접촉** · 정수압 · 통계 평균 접촉력 하나.  **die 압밀 · 국소압 단서는 이 원문에 없다** (Arzt 쪽 문장).
> ★ **결정 9 요약** — 원문에 Tabor 꼴 소성 접촉 법칙이 있다: **F_pl = p_f·f = p_f·π·δ·h, p_f ≈ 3σ_f** (Hencky · Isklinsky, p.264).  단 그 면적은 **표면 돌기 (asperity, δ ≈ 0.1 µm) 척도**이고, 면적식은 기하 절단 원판 (Storåkers c² = 1 에 해당) 이다.  권고 변경 없음 (§8).

---

## 0. 결론 먼저

| 질문 | 답 | 근거 (쪽) |
|---|---|---|
| f = 4πp/(ZD) 가 원문 그대로인가 | **아니다 — 같은 관계의 다른 꼴.**  원문은 σ 를 F 의 함수로 쓴다: 식 (4) σ = (F/d²)·k(1 − ε)/π (d = 입자 **지름**, k = 배위수) · (A7) σ = (F/4r²)·k(1 − ε)/π (r = **반지름**).  F 로 푼 꼴 F = πd²σ/[k(1−ε)] = 4πr²σ/[k(1−ε)] 은 원문에 인쇄돼 있지 않다 (파생).  상수 4π 는 반지름 규약에서만 맞다 — 지름과 짝지으면 4 배 틀린다 | p.263 · p.273 |
| 전제 | 단분산 구 · 무작위 충전 · (i) 접촉면적 ≪ 입자 표면 → **접촉점** (ii) 접촉점이 구 표면에 균등 확률 (iii) 충전 등방 — 임의 방향 평면의 **면적 기공률 = 부피 기공률** · 정수압 (세 주응력 같음) · 모든 방향 접촉의 반경 방향 힘이 **통계 평균에서 같다** ("at least plausible" — 가정이지 유도가 아님) · '한 점' 의 정적 평형 | p.263 · p.271–272 |
| 평균장인가 | **예.**  F 하나가 모든 접촉의 통계 평균 법선력이다.  힘 분포 (힘 사슬) 는 없다.  비정수압도 같은 틀 — 접촉력이 거시 응력과 접촉 방향만으로 정해진다 (부록 B; 카드는 이것을 "정적 가설 f_c ∝ σ·n_c" 라 부른다 — 파생) | p.263 · p.273–274 |
| kε ≈ π (식 5) 의 범위 | Smith [10] 실험 상관식 · "for porosities usually found in bulk solids" = 느슨한 분말.  Arzt (20) 는 (5) 가 아니라 (4) 꼴 (Z 를 명시) 을 쓴다.  우리 밀도 (ε ≈ 0.15) 에 (5) 를 쓰면 k ≈ 21 (Arzt 상한 13.69 초과 — 파생) → 금지 | p.263 |
| 국소압 단서 (die 압밀) | **원문에 없다** ("die" · "local" · "isostatic" 0 건 — 전문 검색 + 렌더 판독).  Molerus 의 비정수압 처리 = 세 직교 일축응력 중첩 → **방향 의존 접촉력** N(φ) = F_M + F_R cos 2φ · T(φ) = F_R sin 2φ (식 6–8 · A8–A10) | p.263 · p.273–274 |
| Tabor 꼴 F/H 가 있나 | **있다** — F_w = F_pl = p_f·f = p_f·π·δ·h (식 번호 없음).  경도 자리 = **p_f "plastic yield pressure"** > σ_f (주변 탄성 재료가 항복을 막는다) · Hencky [14] · Isklinsky [15]: **p_f ≈ 3σ_f** · 석회석 p_f = 50 kp/mm² ≈ 5×10⁸ Pa (Schönert–Steier [16]) | p.264–265 |
| 그 면적의 척도 · 기하 | **표면 돌기** (δ = δ₁/2 ≈ 0.1 µm, 입자 d = 3 µm) — 입자 척도 접촉은 여전히 점.  f = πδh 는 두 구가 합 h 만큼 깎인 **기하 절단 원판 (1차)** = Storåkers c² = 1 (파생) | p.264–265 |
| 탄성 ↔ 소성 | "The plastic characteristics are valid from that point onwards where the elastic characteristics lie above the plastic characteristics" — 같은 평탄화에서 Hertz 힘과 p_f·f 중 **작은 쪽** (Fig. 3) | p.265 |
| 응집 분말 항복 이론의 범위 | kPa 압밀 (석회석 예 σ = 7×10³ Pa · ε 0.61) · 1–20 µm 건조 미분말 · 항복까지 기공률 일정 · 접촉 Coulomb 마찰 → **H = κN** (κ = A/(6πz₀³p_f)) · **tan φ_e = (1+κ) tan ρ** · 개별 항복궤적 (25b) · (29) · 압밀 이력 이방성 (Fig. 6).  ⛔ 고밀도 압밀 · 입자 형상 소성 · 파괴 · 다분산 · 재배열 없음 | p.262–271 |
| 우리 다섯 τ 양 | **해당 없음** — 수송 양이 없다.  τ = 전단응력 · σ₀ = 정수압 압밀 응력 · κ = 응집력/압밀력 비 (기호 충돌만) | § τ 정의 대조 |
| 결정 9 | E3 (F_DEM/H) 꼴 · 평균장 합의 원전 / E2 의 c² = 1 (기하 절단) 끝 / E1 (F_real/H) "느슨한 상한" 판정의 전환 규칙 — **권고 변경 없음** | §8 |

## 1. 한 줄 요약
응집성 미분말의 항복을 **연속체 상태도 (Roscoe · Ashton · Schwedes)** 와 **입자 접촉 역학** 사이에 잇는 1975 해석 이론이다.  세 단계로 간다.
- ① 무작위 단분산 구 충전에서 거시 응력과 접촉력의 평균장 관계를 유도한다.  정수압이면 σ = (F/d²)·k(1−ε)/π (식 4, 부록 A).  일반 응력이면 접촉력도 Mohr 원 꼴 N(φ) = F_M + F_R cos 2φ 를 따른다 (식 6–8, 부록 B).
- ② 압밀 중 접촉 평형 N + F_vdW = F_w (식 9) 에 Dahneke 의 평탄화 반데르발스 힘과 Hertz/소성 저항력을 넣는다.  **소성 평탄화가 응집력을 "얼린다"** — 그래서 응집력이 압밀력에 비례한다: H = κN, κ = A/(6πz₀³p_f) (식 12b).
- ③ 접촉 Coulomb 마찰 (tan ρ) 로 항복을 판정해 **유효 항복궤적** (원점 지나는 직선, tan φ_e = (1+κ) tan ρ) 과 **개별 항복궤적** (저응력에서 휜다) 을 재료 자료로 낸다.  압밀 이력 때문에 분말이 이방성이고, "압밀궤적 하나에 항복궤적 하나" 라는 통설이 틀렸음을 Jenike 전단 셀 실험 (barytes) 으로 보인다.

우리에게 중요한 것은 ①과 ②의 **접촉 법칙 꼴**이다.  ① 은 Arzt (20) 를 거쳐 우리 LHS-25 의 평균장 판별식 (arzt 카드 L-3) 의 원전이다.  ② 의 F_pl = p_f·f (p_f ≈ 3σ_f) 는 결정 9 의 E3 (F_DEM/H) 와 같은 꼴이다.  항복궤적 이론 자체 (호퍼 설계용) 는 우리 압밀 · 수송 문제와 직접 관련이 없다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **O. Molerus** (Institut für Mechanische Verfahrenstechnik, Universität Erlangen-Nürnberg) | **Powder Technology 12 (1975) 259–275** · 접수 1974-12-09 · 수정본 1975-04-17 | `[미확인]` (PDF 미인쇄) | **소재 무관 이론** — 수치 예 = 석회석 미분 (< 15 µm, Schwedes [4]) · 실험 = barytes (< 10 µm, Jenike 셀) | 해석 미시역학 (평균장 접촉력 + 접촉 법칙 + Mohr–Coulomb) + 문헌 전단시험 대조 |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| Zusammenfassung · Summary | 259–260 | 독 · 영 요약 |
| 1.1 General remarks | 260 | 응집 = 압밀 이력에 의존하는 접촉 응집력 · 연속체 접근 (Ashton [3] · Schwedes [4]) · Calladine [5] 비판 ("coordination number of the order of 6") |
| 1.2 The state diagram of cohesive powders | 260–262 | 식 (1)–(3b) · Fig. 1 (ε–σ–τ 상태도) · Fig. 2 (항복궤적 · 압밀궤적) |
| 2. Theory — 네 부분 (i)–(iv) | 262 | 모델 구성 |
| 2.1 Transmission of stresses in a randomly packed bed of monodisperse spheres | 262–263 | ★ 식 (4)–(8) |
| 2.2 The relation between consolidation and cohesion forces | 263–266 | ★ 식 (9)–(12b) · Fig. 3 · 수치 예 |
| 2.3 The internal friction of a powder | 266 | 식 (13) |
| 2.4 The effective yield locus of a cohesive powder | 266–268 | 식 (14a)–(17b) · Fig. 4–5 |
| 2.5 Individual yield loci of a cohesive powder | 268–270 | 식 (18)–(25b) · Fig. 6 (이방성 실험) |
| 2.6 Consolidation by a hydrostatic stress | 270 | 식 (26)–(27) · Fig. 7 |
| 2.7 Consolidation including the "second step of consolidation" | 270–271 | 식 (28)–(29) · Fig. 8 · 실무 결론 |
| Appendix A: Transmission of forces in the contacts of a packing of spheres under hydrostatic stress | 271–273 | ★ (A1)–(A7) · Fig. 9–10 — 식 (4) 유도 |
| Appendix B: Transmission of forces in the contacts in the general case of stress | 273–274 | (A8)–(A10) · Fig. 11–12 — 식 (6)–(8) 근거 |
| List of symbols · References (16 편) | 274–275 | 기호 · 참고문헌 |

- 중복 확인 (2026-10-03): 정본 `litdb/papers/` 365 항목 전수 목록에 molerus 파일 없음 · `git grep -il molerus -- litdb/papers/` = `arzt1982_…` 1 건 (인용) · `0032-5910(75)` · "yield of cohesive" 0 건 → 새 카드.

## 3. 핵심 수치

### 3-1. 관계식 (stated — 식 전수는 §4-9)
| 관계 | 원문 식 | 쪽 |
|---|---|---|
| ★ 정수압 σ ↔ 등방 법선 접촉력 F | σ = (F/d²)·k(1 − ε)/π (4) · σ = (F/4r²)·k(1 − ε)/π (A7) | 263 · 273 |
| 배위수 상관 | kε ≈ 3.1 ≈ π (Smith [10]) | 263 |
| 같은 관계 (kε ≈ π 대입) | σ = [(1 − ε)/ε]·F/d² (5) | 263 |
| 일반 응력의 접촉력 | N(φ) = F_M + F_R cos 2φ · T(φ) = F_R sin 2φ (7) · σ_M = [(1−ε)/ε]F_M/d² · σ_R = [(1−ε)/ε]F_R/d² (8) | 263 |
| 압밀 접촉 평형 | N + F_vdW = F_w (9) | 264 |
| ★ 소성 저항력 | F_w = F_pl = p_f·f = p_f·π·δ·h · p_f ≈ 3σ_f | 264 |
| 탄성 저항력 (Hertz) | F_w = F_el = [2√(2δ)/(3k₁₂)]·h^{3/2} · k₁₂ = k₁ + k₂ · k_i = (1 − ν_i)/E_i (인쇄 그대로 — §3-5) | 264 |
| 응집력 ∝ 압밀력 | H = κN = [A/(6πz₀³p_f)]·N (12b) | 266 |
| 유효 마찰각 | tan φ_e = (1 + κ) tan ρ (15) | 267 |

### 3-2. 수치 (stated)
| 양 | 값 | 조건 | 쪽 |
|---|---|---|---|
| 벌크 배위수 크기 | "of the order of 6" | Calladine 비판 문맥 | 260 |
| kε | ≈ 3.1 ≈ π | Smith [10] · 벌크 분말의 보통 기공률 | 263 |
| 압밀 응력 (전형) | σ = 7×10³ Pa | Schwedes [4] 석회석 < 15 µm | 265 |
| 평균 입경 · 기공률 | d = 3 µm · ε = 0.61 | Schwedes [4] | 265 |
| 압밀 접촉력 | N = ε d²σ/(1 − ε) = **9.67×10⁻⁸ N** | 식 (5) | 265 |
| 특성 거리 | z₀ = 4 Å | 분자 반발 문턱 (Dahneke [12]) | 265 |
| 탄성 상수 | k₁₂ = 2k₁ ≈ 1.4×10⁻¹¹ 1/Pa | 석회석 E = 10⁴ kp/mm² · ν = 0.3 (추정) | 265 |
| 소성 항복압 | p_f ≈ 5×10⁸ Pa (= 50 kp/mm²) | Schönert–Steier [16] 단일 석회석 입자 | 265 |
| Hamaker 상수 | A ≈ 6×10⁻²⁰ J | 광물 6–15×10⁻²⁰ J 의 **하한** (과소평가 쪽) | 265 |
| 돌기 크기 | δ = δ₁/2 ≈ 0.1 µm | Krupp [1]: 0.1 µm 돌기가 1 µm 이상 입자의 접착을 정한다 | 265 |
| 취성 파괴 한계를 조사한 입경 범위 | 1–20 µm | 단일 미립자를 두 강체면 사이에서 누를 때 취성 파괴가 "파쇄 없는 소성 평탄화" 로 바뀌는 한계 (Schönert–Steier [16]) · p_f 는 석회석 단일 입자 실험값 | 265 |
| (12a) 수치 대입 | H = (Aδ/12z₀²)·(1.61 + 0.52)/(0.52 − 0.0518) | Fig. 3 조건 | 266 |
| H₀/N | ≅ 0.03 | 순수 탄성이면 (P_elast → H₀) — 실험보다 훨씬 작음 | 266 |
| H₀/H | ≅ 0.22 | 비압밀 응집력 ÷ 압밀 응집력 | 266 |
| H/N (이론) | ≈ **0.15** | 재료 물성으로 계산 | 266 |
| H/N (전단시험) | **0.33** | Schwedes 석회석 — 저자 해석: Hamaker 과소 또는 모세관 응축 | 266 |
| Schwedes 270 전단시험 | 내부 마찰각 22–24° (선형화 항복궤적) · 정적 파괴선 방향 α = 32° (평균) | 같은 재료 | 270 |
| 식 (28) 예 | ρ = 23° · κ = 0.33 → α = **29°** (σ_R = Σ_R) · **35°** (σ_R = 0.5 Σ_R) | Jenike 2단계 | 271 |
| Fig. 8 매개변수 | φ_e = 38° · ρ = 30° → κ = 0.35 (식 15) | 정규화 항복궤적 | 271 |

### 3-3. 그림 판독 (추세 전용)
| 그림 | 판독 | 비고 |
|---|---|---|
| Fig. 3 (p.265) | 압밀 평형점 2h/z₀ ≈ 3.5 · f(2h/z₀) ≈ 1.8 · P_elast (탄성 곡선 × 중첩선) ≈ 1.45 · vdW 선 0.05 → 0.27 (2h/z₀ 0 → 5) | 실선 · 파선 두 벌 = 정확식 · "broken parallel" 근사 (12b) 로 읽힌다 (본문 p.266) |
| Fig. 6 (p.268) | σ_E ≈ 7.2 · τ_E ≈ 6.3 (단위 [Pa·10⁻³] = kPa 로 읽힘) · Y₁ τ ≈ 3.2 → 6.0 · Y₂ ≈ 2.4 → 5.4 (σ ≈ 1.5 → 6) — 저응력에서 ≈ 0.8 kPa 차, σ_E 쪽으로 수렴 | barytes < 10 µm · Y₂ = 압밀 뒤 전단 상자를 수직축 aa 둘레로 90° 돌린 것 |
| Fig. 8 (p.271) | f_c/Σ_M ≈ 0.43 · f_c′/Σ_M ≈ 0.48 · Σ_R/Σ_M ≈ 0.62 (= sin 38° = 0.616, 파생) · 인장 절편 ≈ −0.12 | 본문 "f_c is higher in the case of hydrostatic consolidation" → 큰 쪽 (≈ 0.48) 이 정수압 압밀로 읽힌다 (추론) |

### 3-4. 파생 환산 (카드 산술 — 원문은 이 값들을 쓰지 않았다)
| 양 | 식 · 값 | 용도 |
|---|---|---|
| ★ (4) 를 F 로 | F = πd²σ/[k(1 − ε)] = 4πr²σ/[k(1 − ε)] → Arzt 기호 f = 4πR²p/(ZD), R = 1 이면 4πp/(ZD) | Arzt (20) 대조 |
| Love–Weber 동치 | 입자 평균압 p̄ = kF/(4πr²) (법선력 · 가지 = r) 에 σ = (1 − ε)·p̄ 를 곱하면 (A7) 이 그대로 나온다 → 식 (4) = **단분산 · 점 접촉 · 등방의 Love–Weber 평균장 판** | 메모 v2 §6-3 대조 |
| 평균 법선력 ↔ 평균 응력 (σ₂ = σ₃) | 구 위 균등 평균 ⟨cos 2φ⟩ = −1/3 → ⟨N⟩ = F_M − F_R/3 ↔ (σ₁ + 2σ₃)/3 = σ_M − σ_R/3 (식 8 과 같은 계수) | 국소압 단서의 구체화 (§8) |
| N 재계산 | 0.61/0.39 × (3 µm)² × 7×10³ Pa = **9.85×10⁻⁸ N** (인쇄 9.67×10⁻⁸ 과 −1.9 %) | §3-5 |
| (11) 무차원 항 재현 | 3k₁₂N/(√δ z₀^{3/2}) = 1.605 (≈ 1.61) · 3πk₁₂p_f√δ/(2√z₀) = 0.522 (≈ 0.52) · 3k₁₂A√δ/(12z₀^{7/2}) = 0.0519 (≈ 0.0518) — 인쇄 N 9.67×10⁻⁸ 사용 | 원문 수치 내부 정합 ✓ |
| 압밀 평형 · 전환점 | 평형 2h/z₀ = (1.61 + 0.0518)/(0.52 − 0.0518) = 3.55 (Fig. 3 ≈ 3.5 ✓) · 탄성 = 소성 전환 x^{3/2} = 0.52x → 2h/z₀ ≈ 0.27 | Fig. 3 |
| H/N · H₀ | H = (Aδ/12z₀²)(1 + 3.55) = 3.125×10⁻⁹ × 4.55 = 1.42×10⁻⁸ N → H/N = 0.147 (≈ 0.15 ✓) · H₀ = Aδ/12z₀² (h = 0 의 vdW) 로 두면 H₀/N = 0.032 · H₀/H = 0.220 (인쇄 0.03 · 0.22 와 일치) | 원문 정합 ✓ |
| κ (12b) | A/(6πz₀³p_f) = 0.099 — (12a) 의 H/N 0.147 보다 작다 (12b 는 큰 N 근사 · vdW 절편 무시) | 근사의 크기 |
| k₁₂ 검산 | 인쇄식 (1 − ν)/E: 2 × 0.7/(9.81×10¹⁰ Pa) = 1.43×10⁻¹¹ ✓ (인쇄값) · Hertz 표준 (1 − ν²)/E 면 1.86×10⁻¹¹ | §3-5 |
| Fig. 8 κ · 식 (28) | tan 38°/tan 30° − 1 = 0.353 ✓ · tan α = tan 23° × 1.33 → 29.4° ✓ · × 1.66 → 35.2° ✓ | 원문 정합 ✓ |
| kε ≈ π 의 함의 | k = π/ε: ε 0.61 → 5.2 · 0.36 → 8.7 · **0.15 → 20.9** (Arzt 전밀도 13.69 초과 · Arzt 근사 Z(D=0.85) ≈ 9.3 의 ≈ 2.2 배) | 식 (5) 를 고밀도에 쓰지 않는 이유 |
| 평균장 크기 감각 (단분산 · **우리 침대 아님**) | d 1 µm · p 300 MPa · Z 6.5 · D 0.85 → F = πd²p/(ZD) = 1.7×10⁻⁴ N · F/H (H 0.85 GPa) = 0.20 µm² · a/r ≈ 0.51 · Z·(F/H)/(4πr²) = **0.415** = p/(D·H) | 전제 (i) "접촉 = 점" 이 300 MPa 에서 깨진다 (접촉이 표면의 ≈ 40 %) |
| 탄성/소성 전환을 우리 기호로 | F_el = (4/3)E*√R* h^{3/2} = p_f·2πR*h ⇔ h/R* = (9π²/4)(p_f/E*)² → E* 22.415 · p_f = H 0.85 GPa 에서 **0.032** | 메모 v2 §6-2 의 "δ/R* > 0.032 이면 겹침 원을 넘는다" 와 같은 식 (§8) |

### 3-5. 내부 정합 · 오식 점검
- **N 9.67×10⁻⁸ N** (p.265) 은 인쇄 입력 (ε 0.61 · d 3 µm · σ 7×10³ Pa) 으로 재계산하면 9.85×10⁻⁸ N (−1.9 %).  뒤의 무차원 항 1.61 은 인쇄값 9.67 과 맞는다 → 이후 수치는 9.67 기준으로 일관.
- **k_i = (1 − ν_i)/E_i** (p.264, 확대 판독 — 제곱 없음).  Hertz 표준은 (1 − ν_i²)/E_i 다.  인쇄 수치 k₁₂ ≈ 1.4×10⁻¹¹ 1/Pa 는 인쇄식과 맞는다 (§3-4).  결정 9 에는 영향 없음.
- **δ 의 규약이 두 곳에서 다르다** — 본문 (p.264) *"δ, defined by δ = δ₁δ₂/(δ₁ + δ₂) contains the diameters δ₁ and δ₂ of the two adherent spheres"* ↔ 기호표 (p.274) *"δ geometrical mean of the radii of asperities in a contact · δ₁, δ₂ radii of asperities"*.  Hamaker 구–구 식 F = A·R*/(6z₀²) 과 식 (10) 의 Aδ/(12z₀²) 이 맞으려면 δ = 2R* (지름 규약) 이어야 한다 (파생) → **본문의 지름 규약이 자기정합**이다.  지름 규약에서 f = πδh = 2πR*h = 기하 절단 원판이다.  반지름 규약이면 면적이 그 절반 (Hertz 꼴) 이 된다.  또 δ₁δ₂/(δ₁ + δ₂) 는 기하평균이 아니다 (조화평균의 절반).
- **같은 글자 다른 양 (원문 안)**: k = 배위수 (식 4) ↔ (12a) 의 k = 탄성 상수 k₁₂ · H = 응집력 (12a–b) ↔ (A1) 의 dH = 접촉 수 · f = 접촉면적 ↔ f_c = 압밀 함수 · 비구속 항복압 (Fig. 8) · σ₀ = 정수압 압밀 응력.
- H/N "0.33" 의 낱말 — *"For the limestone fraction investigated by Schwedes [4], the computation gives H/N = 0.33"* — 앞 문장이 "data calculated from shear tests" 라 전단시험 자료에서 이론으로 역산한 값으로 읽힌다 (원문 낱말 모호).
- 참고문헌 [15] 철자: 본문 "Isklinsky" (p.264) · 목록 "A.J. Insklinsky" (p.275).  정본 카드 `zunker2024_mdr_contact_model_partI` 는 같은 1944 논문을 "Ishlinsky 1944" 로 적는다.  원문 철자를 그대로 둔다.

## 4. 방법 ★

### 4-1. 모델 네 부분 (원문 (i)–(iv), p.262)
| # | 원문 | 카드 요약 |
|---|---|---|
| (i) | *"A simple model is proposed for the transmission of external stresses through a lattice of solid particles, whereby contacting points on the particles' surfaces are assumed, in which forces can be transmitted."* | 접촉점 격자의 응력 전달 (§2.1, 부록 A · B) |
| (ii) | *"a model for the magnitude of the cohesion forces produced by consolidation is evaluated."* | 압밀이 만드는 응집력 크기 (§2.2) |
| (iii) | *"The position of the end Mohr circles and thus the state of steady-state yield are derived from the condition that the end Mohr circles are just describing the limiting state between yield and consolidation."* | 유효 항복궤적 (§2.4) |
| (iv) | *"Cohesion forces of given magnitude in the interparticle contacts are considered, and based on the interaction between cohesion forces and external forces incipient yield of overconsolidated cohesive powders is investigated."* | 개별 항복궤적 (§2.5–2.7) |

### 4-2. ★ 식 (4) 유도 — 부록 A 단계별 (p.271–273, Fig. 9–10)
1. 배위수 k, 구 반지름 r → 표면 요소 dS 당 평균 접촉 수 **dH = k·dS/(4πr²)** (A1).  등방 정수압 + 등방 접촉 → 접촉력 크기가 방향에 무관 (통계 평균).
2. 평면 gg 가 n 개 입자를 자른다.  무작위 충전에서 어느 절단면이든 같은 확률이므로, 중심이 평면에서 ζ–ζ+dζ 에 있는 입자 수 = **n_ζ = n·dζ/r** (A2).
3. 잘린 입자 하나가 평면을 지나 전하는 힘 = 절단면 너머 접촉의 법선 성분 합: dK = [(k/4πr²)∫_S F cos φ dS]·n dζ/r · ∫_S cos φ dS = ∫dA_t = **π(r² − ζ²)** (투영 원판).
4. 합: **K = (kFn/4r³)∫₀^r (r² − ζ²)dζ = kFn/6** (A3).
5. 잘린 입자의 단면적 합 **A_p = (nπ/r)∫₀^r (r² − ζ²)dζ = n·2πr²/3** (A4) · 무작위 충전에서 부피 기공률 = 단면 기공률 → **A_p = A(1 − ε)** (A5) → **n = 3A(1 − ε)/(2πr²)** (A6).
6. K = (Fk/6)·3A(1 − ε)/(2πr²) → **σ = K/A = (F/4r²)·k(1 − ε)/π** (A7) → r = d/2 → **식 (4)**.
- 원문의 가정 문장 (p.272): *"With an isotropic random packing and an isotropic hydrostatic loading, the assumption of an isotropic distribution of compressive normal forces in the spatially equally distributed contacts at least seems plausible."*
- 카드 해석 (파생): 이 경로는 **절단면 정역학** (Delesse 원리 A5 사용) 이다.  Love–Weber 입자 응력과는 **점 접촉 (가지 = r) · 겹침 없는 같은 구** 에서만 같은 식이 된다 (§3-4).  접촉이 평평해져 접촉점이 중심에서 r 보다 가까워지면 (가지 r − δ/2) 같은 p 에서 평균 힘이 r/(r − δ/2) 배 커진다 — 메모 v2 §6-3 보정 ① 은 전제 (i) 를 푼 것이다.

### 4-3. 비정수압 — 부록 B (p.273–274, Fig. 11–12)
- 정수압 = 세 직교 일축응력의 중첩.  일축응력 σ 에서 구 표면의 접촉점 P (반지름 벡터가 σ 방향과 φ) 에 **σ 방향의 힘 F cos φ** 가 전달되고, σ = [(1 − ε)/ε]·F/d² (A8).
- 그 힘의 법선 · 접선 성분: **N(φ) = F cos²φ = (F/2)(1 + cos 2φ) · T(φ) = F sin φ cos φ = (F/2) sin 2φ** (A9).
- 일축응력의 경사면 응력 σ(φ) = (σ/2)(1 + cos 2φ) · τ(φ) = (σ/2) sin 2φ (A10) 와 **같은 각도 의존** → *"As any state of stress may be represented as a superposition of three orthogonal uniaxial stresses, this property holds in general"* → 식 (6)–(8).
- 카드 해석 (파생): 접촉력 벡터가 거시 응력을 접촉 방향에 투영한 꼴 **f_c = c·σ·n_c** (정수압 → 반경 방향 같은 크기 · 일축 → 하중축에 평행한 F cos φ) 이다 = 미시역학의 **정적 (응력 아핀) 가설**.  힘 사슬 · 국소 요동은 원리적으로 없다.  ⚠ (8) 과 (A8) 은 식 (5) 의 계수 (kε ≈ π) 로 쓰였다.  식 (4) 계수로 바꿔도 각도 구조는 같다.

### 4-4. 접촉 법칙 — 식 (9)–(12b) · Fig. 3 (p.264–266)
- 근사 전제 (p.264): *"the formation of the contact area between particles and therefore the formation of cohesion forces is determined by only the normal components of the contact forces due to the external stress applied."*
- 평형 (9): 외부 법선력 N + vdW 인력 F_vdW = 재료 저항력 F_w.
- vdW (10): Dahneke [12] 가 Hamaker [11] 를 고쳐 평탄화 h 로 커지는 힘 F_vdW = (Aδ/12z₀²)(1 + 2h/z₀).  두 번째 항 = (A/(6πz₀³))·(πδh) — 평판 vdW 압력 × 평탄화 면적 (파생).
- 탄성 저항 (Hertz [13]): F_el = [2√(2δ)/(3k₁₂)]h^{3/2}.  순수 탄성이면 하중을 빼면 원상태로 돌아가 응집력이 압밀에 무관해진다 — *"which is in sharp contrast to all experimental experience with cohesive powders"* → 비가역 소성 변형이 응집력을 **"frozen"** 한다 (p.264).
- 소성 저항: **F_pl = p_f·f = p_f·π·δ·h** — *"For the resulting small deformations simple considerations yield"* · p_f > σ_f (*"As the surrounding material which is elastically deformed is hindering yield"*) · **p_f ≈ 3σ_f** (Hencky [14] · Isklinsky [15]).
- 무차원형 (11) 과 Fig. 3: 탄성 특성 (2h/z₀)^{3/2} 와 소성 특성 (직선) 을 평탄화 2h/z₀ 에 그린다.  **탄성 특성이 소성 특성 위에 놓이는 점부터 소성 특성이 유효**하다.  압밀 평형 = 소성 특성 × (N + vdW) 중첩선의 교점.
- Fig. 3 이 주는 세 통찰 (p.266): (1) 큰 응집력의 원인은 **접촉 소성 변형**이다.  배위수 증가로 설명하면 응집력/압밀력 비가 실험에서 본 적 없이 작아진다.  (2) 비압밀 응집력 H₀ 는 작다 (H₀/H ≅ 0.22).  (3) 이론 H/N ≈ 0.15 < 전단시험 0.33.
- 결과 (12a) · 근사 **(12b) H = κN, κ = A/(6πz₀³p_f)** — κ 는 재료 상수 (Hamaker · z₀ · p_f) 다.  "for sufficiently high consolidations the broken parallel may be used".

### 4-5. 항복 — 식 (13)–(29)
- 접촉 마찰 (13) T/N ≤ μ = tan ρ (ρ = 접촉 간 마찰각).  항복 = *"at least in some of the contacts the shear force transmitted has reached the limiting value"*.
- **유효 항복궤적** (§2.4): end Mohr 원 = 항복 · 압밀의 경계.  접촉 φ 의 압축력 C(φ) = (1 + κ)(F_M + F_R cos 2φ), 접선력 F_R|sin 2φ| → (14a–c) → 최대 φ = π/4 + φ_e/2 (16) → F_R = sin φ_e F_M (17a) → **Σ_R = sin φ_e Σ_M** (17b, 원점 지나는 직선) · **tan φ_e = (1 + κ) tan ρ** (15).  전제 둘: 응집력 ∝ 생성 법선력 · 응집력의 공간 분포 = 생성 법선력 분포.
- **개별 항복궤적** (§2.5): 압밀 응력 (σ_VM, σ_VR) 이 만든 응집력 분포 H(φ) = H_M + H_R cos 2φ (18) 위에 항복 응력의 법선력 (19) 을 더해 C(φ) (20) · 접선력 (21) · 미끄럼 조건 (22) → 파괴 방향 φ = π/4 + α/2 (23) · tan α (24a/b) · σ_R(σ_M) (25a/b).  범위 0 ≤ σ_VR/σ_VM ≤ sin φ_e (0 = 정수압 압밀 · sin φ_e = Jenike 2단계).
- **정수압 압밀** (§2.6): α = ρ (26) · sin ρ = σ_R/(σ_M + κσ₀) (27) → 기울기 ρ 의 직선 항복궤적 (Fig. 7).  절편 = 삼축 인장강도 σ_Z3 (일축 인장강도 σ_Z1 은 더 작다).  압밀압이 다르면 평행선.
- **Jenike 2단계** (§2.7): tan α = tan ρ(1 + κΣ_R/σ_R) (28) → 파괴 방향이 연속체 예측 π/4 + ρ/2 보다 크다 (Schwedes 파괴선 32° 설명) · 정규화 항복궤적 (29) 은 저응력에서 휜다 (Fig. 8).
- **이방성** (§2.5, Fig. 6): 정수압으로 압밀한 분말만 등방이다.  비정수압 압밀은 최대 응집력 방향을 남긴다 → 같은 압밀에서도 전단 방향에 따라 다른 항복궤적.  ⇒ "압밀궤적 하나에 항복궤적 하나" (Ashton [3] · Schwedes [4]) 는 틀렸다 · 장치가 다른 항복궤적은 단순 비교할 수 없다.

### 4-6. 시뮬레이션 · 입자 처리 ★
- **시뮬레이션 없음** — 해석 이론 + 손계산 수치 예 + 문헌 전단시험 대조.
- 입자 = **단분산 구** · 무작위 등방 충전 · 배위수 k 는 상수 (Smith 상관식으로만 ε 과 연결) · 항복 개시까지 기공률 일정 (*"small changes in the elastic deformations during unloading ... may be neglected"*, p.268).
- 소성의 자리 = **접촉 (돌기) 소성** — 돌기가 강-완전소성 p_f 로 평평해져 면적 f = πδh 를 만든다.  **입자 형상 소성 (shape flow) 은 없다** (입자 척도에서는 점 접촉 그대로).  우리 분류로는 DEM 의 "접촉 법칙 소성" 쪽이지 MPM 의 형상 흐름 쪽이 아니다.
- 재배열 · 직물 변화 · 파괴 · 다분산: 없음.  이방성은 **응집력 분포**로만 들어온다 (충전 기하는 등방 그대로).

### 4-7. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| Mohr 원 (σ_M, σ_R) | 중심 (σ₁ + σ₃)/2 · 반지름 (σ₁ − σ₃)/2.  σ₂ = σ₃ 만 다룬다 |
| end Mohr circle (Σ_M, Σ_R) | 개별 항복궤적의 끝 원 = 항복과 압밀의 경계 (정상 유동 상태) |
| yield locus / consolidation locus | 항복 개시 / 추가 압밀을 일으키는 최대 Mohr 원들의 포락선 (같은 기공률) |
| effective yield locus (φ_e) | end Mohr 원들의 포락선 — 원점 지나는 직선 |
| critical state line (φ_crit) | end Mohr 원 최대 전단응력을 잇는 선.  tan φ_crit = σ_R/σ_M |
| Roscoe 상태도 | ε–σ–τ 공간의 압밀면 · 항복면 · 임계상태선 (Fig. 1).  공극비 e = ε/(1 − ε) |
| Jenike 전단 셀 · "second step of consolidation" | 주어진 하중에서 정상 상태까지 전단해 압밀 → 시작 상태 = end Mohr 원 |
| 비구속 항복압 f_c | 호퍼 출구 설계 값 (Fig. 8) |
| overconsolidated | 현재 응력보다 큰 응력으로 압밀된 상태 |
| Hamaker 상수 A · z₀ | vdW 세기 · 분자 반발 문턱 거리 (4 Å) |
| Dahneke 평탄화 vdW | 평평해진 접촉에서 커지는 vdW (식 10) |
| Hencky · Isklinsky 구속 계수 | 주변 탄성 재료의 구속으로 항복압 p_f ≈ 3σ_f |
| 배위수 k | "the statistical mean number of contacts of one particle with neighbouring particles" (= Arzt Z) |

### 4-8. ★ 기호 대조 — Molerus ↔ Arzt 1982 ↔ 우리 (메모 v2 · 코드)
| 양 | Molerus | Arzt (arzt 카드) | 우리 | ⚠ |
|---|---|---|---|---|
| 접촉 법선력 | **F** (정수압) · N (압밀) | **f** | F_ij · F_DEM · F_real | Molerus **f = 접촉면적** · 우리 **f = σ_eff/σ₀** (`f_ion_<mode>`) — 세 겹 충돌 |
| 접촉면적 | **f** = πδh | a | A_ij · A_tabor · A_overlap | |
| 배위수 | **k** | Z | CN | Molerus k 는 탄성 상수 k_i · k₁₂ 와도 겹침 |
| 고체 분율 / 기공률 | 1 − ε / **ε** | D / 1 − D | 1 − ε_sphere / ε_sphere | Molerus e = 공극비 (우리 꼬리표 `_e` 와 무관) |
| 외부압 | **σ** (σ₀ = 정수압 압밀 응력) | p | p (300 MPa) | 우리 **σ₀ = 기준 전도도** (3.0 mS/cm) |
| 경도 / 항복압 | **p_f** ≈ 3σ_f | 3σ_f (f/a, 식 19) | **H** = 0.85 GPa | Molerus **H = 응집력 (힘)** |
| 응집력 비 | **κ** = H/N | — | κ_i = ΣF_real/ΣF_DEM (메모 v2 §6-3) | Tjaden **κ = τ²** (tortuosity factor) · 열전도 κ 와도 충돌 |
| 겹침 · 평탄화 | **h** (두 상대 합) | — (R′ 성장) | **δ** (DEM 겹침) | Molerus **δ = δ₁δ₂/(δ₁+δ₂) = 2R*** (지름 규약) |
| 전단응력 | **τ** | — | — | 우리 τ = 굴곡도 (명명 규약 10-03) |
| 접촉 마찰각 | **ρ** (ρ_s = 부피밀도) | — | μ (DEM 마찰계수) | |

### 4-9. 원문 식 전수 (식 번호 · 쪽 · 확대 판독)
| 식 | 쪽 | 원문 식 | 뜻 |
|---|---|---|---|
| (1) | 261 | ρ_s = F_y(J₁, J₂, J₃) · ρ_s = F_c(J₁, J₂, J₃) | 항복 개시 · 압밀 상태식 (Ashton [3]) |
| — | 261 | e = ε/(1 − ε) | 공극비 (Roscoe [6]) |
| (2) | 261 | ε = f_y(σ₁, σ₂, σ₃) · ε = f_c(σ₁, σ₂, σ₃) | (1) 과 동등 |
| (3a) | 262 | ε = f_y(σ₁, σ₃) · ε = f_c(σ₁, σ₃) | 최대 Mohr 원만 결정 |
| — | 262 | σ_M = (σ₁ + σ₃)/2 · σ_R = (σ₁ − σ₃)/2 | Mohr 원 중심 · 반지름 |
| (3b) | 262 | ε = f_y(σ_M, σ_R) · ε = f_c(σ_M, σ_R) | 이후 σ₂ = σ₃ |
| — | 262 | sin φ_e = σ_R/σ_M · tan φ_crit = σ_R/σ_M | Fig. 2 |
| **(4)** | 263 | **σ = (F/d²)·k(1 − ε)/π** | ★ 정수압 ↔ 평균 접촉력 |
| — | 263 | kε ≈ 3.1 ≈ π | Smith [10] |
| (5) | 263 | σ = [(1 − ε)/ε]·F/d² | (4) + kε ≈ π |
| (6) | 263 | σ(φ) = σ_M + σ_R cos 2φ · τ(φ) = σ_R sin 2φ | 경사면 응력 |
| (7) | 263 | N(φ) = F_M + F_R cos 2φ · T(φ) = F_R sin 2φ | 같은 방향 접촉의 힘 |
| (8) | 263 | σ_M = [(1 − ε)/ε]·F_M/d² · σ_R = [(1 − ε)/ε]·F_R/d² | Mohr 원 꼴이 접촉력에도 성립 |
| (9) | 264 | N + F_vdW = F_w | 압밀 접촉 평형 |
| (10) | 264 | F_vdW = (Aδ/12z₀²)(1 + 2h/z₀) · δ = δ₁δ₂/(δ₁ + δ₂) | Dahneke [12] |
| — | 264 | F_w = F_el = [2√(2δ)/(3k₁₂)]·h^{3/2} · k₁₂ = k₁ + k₂ · k_i = (1 − ν_i)/E_i | Hertz [13] (인쇄 그대로) |
| — | 264 | **F_w = F_pl = p_f·f = p_f·π·δ·h** · **p_f ≈ 3σ_f** | ★ 소성 저항 (Hencky [14] · Isklinsky [15]) |
| (11) | 265 | 3k₁₂N/(√δ z₀^{3/2}) + [3k₁₂A√δ/(12z₀^{7/2})](1 + 2h/z₀) = (2h/z₀)^{3/2} (탄성) 또는 [3πk₁₂p_f√δ/(2√z₀)]·(2h/z₀) (소성) | (9) 의 무차원형 · Fig. 3 |
| (12a) | 266 | H = (Aδ/12z₀²)[3kN/(√δ z₀^{3/2}) + 3πkp_f√δ/(2√z₀)][3πkp_f√δ/(2√z₀) − 3kA√δ/(12z₀^{7/2})]⁻¹ | 압밀 접촉의 접착력 (여기 k = k₁₂) |
| (12b) | 266 | H = κN = [A/(6πz₀³p_f)]·N | 근사 |
| (13) | 266 | T/N ≤ μ = tan ρ | 접촉 마찰 |
| (14a) | 267 | F_R\|sin 2φ\| ≤ (1 + κ) tan ρ (F_M + F_R cos 2φ) | 미끄럼 개시 |
| (14b) | 267 | F_R sin 2φ ≤ (1 + κ) tan ρ (F_M + F_R cos 2φ) | φ ≥ 0 |
| (15) | 267 | tan φ_e = (1 + κ) tan ρ | ★ 유효 마찰각 |
| (14c) | 267 | F_R(sin 2φ − tan φ_e cos 2φ) ≤ tan φ_e F_M | |
| (16) | 267 | φ = π/4 + φ_e/2 | 좌변 최대 |
| (17a) | 267 | F_R = sin φ_e F_M | |
| (17b) | 267 | Σ_R = sin φ_e Σ_M | 유효 항복궤적 |
| (18) | 268 | H(φ) = κ[εd²/(1 − ε)](σ_VM + σ_VR cos 2φ) = H_M + H_R cos 2φ | 압밀이 남긴 응집력 분포 |
| (19) | 269 | N(φ) = [εd²/(1 − ε)](σ_M + σ_R cos 2φ) = F_M + F_R cos 2φ | 항복 응력의 법선력 |
| (20) | 269 | C(φ) = N(φ) + H(φ) = C_M + C_R cos 2φ | 합성 압축력 |
| (21) | 269 | \|T(φ)\| = [εd²/(1 − ε)]σ_R\|sin 2φ\| = F_R\|sin 2φ\| | 접선력 |
| (22) | 269 | F_R sin 2φ − C_R tan ρ cos 2φ ≤ tan ρ C_M (φ ≥ 0) | 미끄럼 조건 |
| (23) | 269 | φ = π/4 + α/2 | 파괴 접촉 방향 |
| (24a) | 269 | tan α = tan ρ (F_R + H_R)/F_R | |
| (25a) | 270 | F_R = sin ρ[√((F_M + H_M)² − H_R² cos²ρ) − H_R sin ρ] | |
| (24b) | 270 | tan α = tan ρ (σ_R + κσ_VR)/σ_R | |
| (25b) | 270 | σ_R = sin ρ[√((σ_M + κσ_VM)² − κ²σ_VR² cos²ρ) − κσ_VR sin ρ] | 개별 항복궤적 |
| (26) | 270 | α = ρ | 정수압 압밀 |
| (27) | 270 | sin ρ = σ_R/(σ_M + κσ₀) | 기울기 ρ 직선 (Fig. 7) |
| (28) | 270 | tan α = tan ρ (1 + κΣ_R/σ_R) | Jenike 2단계 |
| (29) | 271 | σ_R/Σ_M = sin ρ[√((σ_M/Σ_M + κ)² − κ² sin²φ_e cos²ρ) − κ sin φ_e sin ρ] | 정규화 항복궤적 (Fig. 8) |
| (A1) | 271 | dH = k·dS/(4πr²) | 표면 요소당 접촉 수 |
| (A2) | 272 | n_ζ = n·dζ/r | |
| (A3) | 272 | K = (kFn/4r³)∫₀^r (r² − ζ²)dζ = kFn/6 | |
| (A4) | 272 | A_p = (nπ/r)∫₀^r (r² − ζ²)dζ = n·2πr²/3 | |
| (A5) | 272 | A_p = A(1 − ε) | 면적 기공률 = 부피 기공률 |
| (A6) | 272 | n = 3A(1 − ε)/(2πr²) | |
| **(A7)** | 273 | **σ = (F/4r²)·k(1 − ε)/π** | ★ r = d/2 → (4) |
| (A8) | 273 | σ = [(1 − ε)/ε]·F/d² | 일축응력 · σ 방향 힘 F cos φ |
| (A9) | 273 | N(φ) = F cos²φ = (F/2)(1 + cos 2φ) · T(φ) = F sin φ cos φ = (F/2) sin 2φ | Fig. 12 |
| (A10) | 273 | σ(φ) = (σ/2)(1 + cos 2φ) · τ(φ) = (σ/2) sin 2φ | 같은 각도 의존 → (6)–(8) |

## 5. Figure set ★
| Fig (쪽) | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 (p.261) | ε–σ–τ 상태도: 정수압 압밀선 f₁f₂ · 임계상태선 e₁e₂ · 최대 인장응력선 t₁t₂ · 압밀면 · 항복면 · 팽윤곡선 ACH (Schwedes 판) | 연속체 상태도 — 우리 Heckel · 다압력 트랙의 배경 개념.  직접 사용 없음 |
| 2 (p.262) | 항복궤적 · 압밀궤적 · 유효 항복궤적 (φ_e) · 임계상태선 (φ_crit) | 기하 정의 (sin φ_e = σ_R/σ_M) |
| ★ 3 (p.265) | 식 (11) 의 그림: 탄성 특성 (h^{3/2}) · 소성 특성 (직선) · vdW 선 · N 중첩선 · 압밀 평형 · P_elast · H₀ · H | **결정 9** — 같은 평탄화에서 둘 중 작은 힘이 유효하다는 전환 규칙 = E1 (F_real/H) 이 상한인 이유의 원형 |
| 4 (p.267) | end Mohr 원 E · 항복 Y · 압밀 C | 정상 유동 = 항복과 압밀의 경계 |
| 5 (p.267) | 유효 항복궤적 = end Mohr 원 포락선 · 압밀 응력 (σ_VM, σ_VR) · σ₀ | |
| 6 (p.268) | **유일한 실험 그림** — barytes < 10 µm, Jenike 셀: Y₁ (그대로) vs Y₂ (전단 상자 90° 회전) 두 곡선 | 압밀 이력 이방성 — 접촉력 · 응집력 분포가 방향을 기억한다.  우리 die 압밀 침대의 접촉 방향 분포 (직물) 진단 동기 |
| 7 (p.270) | 정수압 압밀 항복궤적 (기울기 ρ 직선) · σ_Z3 · σ_Z1 | |
| 8 (p.271) | 정규화 항복궤적 (Jenike 2단계, 실선) vs 정수압 압밀 (파선) · φ_e 38° · ρ 30° · κ 0.35 · f_c · f_c′ | 저응력 곡률 |
| ★ 9 (p.272) | 충전을 지나는 평면 gg 와 활성 접촉 | **식 (4) 의 유도 기하** = Arzt (20) 원전 |
| ★ 10 (p.272) | 접촉력 F 와 성분 F cos φ · F sin φ · 절단 구의 dS · dA | 같은 유도 — 투영 원판 π(r² − ζ²) |
| 11 (p.273) | 정수압에서 접촉력 F 의 x · y · z 성분 | 정수압 = 세 일축 중첩 |
| ★ 12 (p.273) | 일축응력에서 접촉력 F cos φ 의 법선 (F cos²φ) · 접선 ((F/2) sin 2φ) 성분 | 비정수압 (die 압밀) 의 방향 의존 접촉력 — 국소압 단서의 Molerus 판 |

## 6. Post-processing ★
- **무엇**: 해석 유도 (부록 A · B) → 손계산 수치 예 (석회석 · Fig. 3 · 식 12a) → 문헌 전단시험 (Schwedes 270 회) 과 비 (H/N) · 각도 (α) 대조 → Jenike 셀 이방성 실험 1 건 (Fig. 6).
- **도구**: 해석 · 손계산.  통계 · 불확실성 · 반복 수 (Fig. 6 "repeated measurements only confirmed") 의 정량 보고 없음.
- **수치화 · 기록**: 식 (12a) 수치를 분수 그대로 인쇄 (1.61 + 0.52)/(0.52 − 0.0518) — 재현이 쉽다 (§3-4 에서 재현됨).  정규화 항복궤적 (Σ_M 나눔) 으로 재료 비의존 표현.

## § τ 정의 대조 — 우리 규약 매핑

| # | 원문 기호 (식 · 쪽) | 원문 정의 · 이름 | 정규화 (부피 · 단면 · σ₀) | 우리 양 | 비고 |
|---|---|---|---|---|---|
| ① | **τ** (식 6 · Fig. 1–8, p.261–271) | "shear stress" (기호표 p.274) — Mohr 원의 전단응력 | — | **해당 없음** | 우리 다섯 τ (f · tau2 · tau · τ_geo · τ_e) 어느 것도 아니다.  철자만 같다 |
| ② | **σ₀** (p.268 · 270 · 식 27) | "hydrostatic consolidating stress" | — | **해당 없음** | ⚠ 우리 σ₀ = 기준 전도도 (펠릿 3.0 mS/cm, CL-91) 와 기호 충돌 |
| ③ | **κ** (식 12b · 15 · 18, p.266–268) | "ratio of cohesion force to consolidation force" | — | **해당 없음** | ⚠ Tjaden κ = τ² (tortuosity factor) · 열전도 κ · 메모 v2 §6-3 κ_i (= ΣF_real/ΣF_DEM) 와 세 겹 충돌 |
| ④ | **ε** (식 2 · 4 · 5) | porosity — 부피 = 단면 기공률 (전제 iii · A5) | 전 부피 | f 의 짝 φ **아님** | 고체 분율 1 − ε 은 단일 고체상.  우리 φ 는 전도상 (SE) 부피분율 |
| ⑤ | **f** (기호표) | "contact area" | — | 우리 f (= σ_eff/σ₀) **아님** | ⚠ Arzt f = 접촉력 · Molerus f = 접촉면적 · 우리 f = 무차원 전도 비 |
| ⑥ | **e** | pore number e = ε/(1 − ε) | — | — | 우리 꼬리표 `_e` (Nguyen τ_e) · `_el_` (전자) 와 무관 |
| — | tortuosity · τ_geo · τ_e · σ_eff · 수송 | **없다** | — | f · tau2 · tau · τ_geo · τ_e 모두 n/a | 수송 양 0 |

- **σ₀ 기준 (한 줄)**: n/a — 이 논문에는 전도도 · 확산 · 수송 양이 없다.  원문의 σ₀ 는 **정수압 압밀 응력**이다.
- **판정**: τ 규약에 직접 기여하지 않는다.  이 절의 쓰임은 둘이다: (1) LHS-25 사전등록 문서에 Molerus · Arzt 식을 옮길 때 **f · κ · H · σ₀ · τ** 가 우리 규약의 같은 글자와 다른 양임을 표시한다 (§4-8).  (2) 우리 접촉망 T 의 SE–SE 협착 면적 (Holm R = 1/(2σa)) 이 결국 접촉력 ↔ 면적 법칙에 걸린다 — 이 논문은 그 **면적 쪽 입력** (F = p_f·f) 의 원형만 준다.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 이 브랜치에서는 자리표시 — 값 없음.  아래 우리 쪽 서술은 CLAUDE.md · 메모 v2 기준)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 목적 | 응집성 미분말의 항복 · 유동 (호퍼 설계) | LPSCl + NCM811 복합 양극 냉간 압밀 → 접촉망 · 복셀 수송 | 다름 |
| 응력 수준 | 압밀 7×10³ Pa (예) · Fig. 6 σ_E ≈ 7 kPa (판독) | 300–400 MPa | **4–5 자릿수 차** — 접촉 상태가 다르다 |
| 기공률 | ε 0.61 (예) | ε_sphere ≈ 10–20 % | 다름 — kε ≈ π 는 우리 밀도에서 불가 (§3-4) |
| 입자계 | 단분산 구 (d 3 µm) | 다분산 · 이종 (AM 강체 140 GPa · SE 연질 E_eff 1.35 GPa, 12:4:1) | **다름** — 식 (4) 의 단분산 전제가 깨진다 → 입자별 Love–Weber 필요 (메모 v2 §6-3 그대로) |
| 접촉력 ↔ 응력 | 평균장 (정적 가설) 식 (4) · (A7) · (6)–(8) | DEM 접촉 목록의 실측 힘 + 입자별 Love–Weber (arzt 카드 L-3) | 우리는 분포를 재고 Molerus 는 평균 하나를 준다 → 평균장 = **대조선** (C1) |
| 접촉 점/면 | 점 (전제 i) | 평균장 산술로 접촉이 표면의 ≈ 40 % (§3-4) · 코퍼스 관찰은 메모 v2 §6 | 전제 (i) 가 우리 영역에서 깨진다 → 가지 길이 보정 (R − δ/2) |
| 접촉 법칙 | Hertz (실제 E) ↔ 강-완전소성 p_f·πδh 전환 + Dahneke vdW | hooke/hysteresis (연화 E) · 소성 없음 · Stage-E 사후 면적 (E1 = F_real/H, H 0.85 GPa) | Molerus 는 소성을 **접촉 법칙 안**에, 우리는 **사후 면적**에만 둔다 |
| 소성 면적 | f = πδh (기하 절단 · c² = 1 · 돌기 척도) | E1 상한값 · 제안 E2 = c²·A_overlap (c² 1.27–1.40) · E3 = F_DEM/H | E3 꼴 = Molerus 꼴 · E2(c² = 1) = Molerus 면적 = 우리 hertz 모드 면적 (c_cpl[22] 교차 원판, 1차) |
| 경도 | p_f ≈ 3σ_f (구속 항복압) | H = 0.85 GPa | 같은 구속 계수 3 의 자리.  3σ_f = H 면 σ_f ≈ 0.28 GPa — MPM σ_y 0.30 과 같은 자릿수지만 σ_y 0.30 은 외부 앵커가 없다 (결정 7) → 검증으로 쓰지 않는다 |
| 점착 | 핵심 (H = κN) | 생산 DEM 의 점착 설정 — 이 카드에서 확인하지 않았다 [미확인] | — |
| 밀도 규약 | 1 − ε = 구 부피 고체 분율 (겹침 없음) | ε_sphere (구 부피 합) | 같은 규약 (겹침 없는 극한).  Love–Weber 의 V_i = 구 부피와 짝 |
| 전달 (σ) | 없음 | 접촉망 σ (Holm) · STEP3 복셀 σ | 이 논문은 접촉력 ↔ 면적 쪽만 |
| 차원 | 3D 해석 | DEM 3D | 같음 |

- **frame [5]**: Molerus 는 **역학 쪽 (접촉력 미시역학 → 연속체 항복)** 만 가진다.  수송 · 충전 구조 (k 고정 · 재배열 없음) · 입자 형상 소성은 없다.  소성은 **접촉 (돌기) 소성**이지 형상 흐름이 아니다.  DEM 의 자리 = 접촉망 힘 (우리는 실측) · MPM 의 자리 = 형상 흐름 (이 논문에 없음).
- **frame [4]**: 이 논문에 DEM · MPM 을 맞추지 않는다.  쓰는 것은 평균장 **대조선** (C1 의 p̄ = p/D) 과 접촉 법칙의 **꼴** (E3) 뿐이다.

## 8. 적용 인사이트

### 힘 ↔ 외부압 f = 4πp/(ZD) — Arzt (20) 평균장의 원전
(판단 메모 v2 §8-2 · §6-3 · C1)

| 묻는 것 | 원문 답 | 쪽 |
|---|---|---|
| 정확한 식 · 번호 | **식 (4)** σ = (F/d²)·k(1 − ε)/π — *"where d denotes the particle diameter and k means the coordination number, i.e. the statistical mean number of contacts of one particle with neighbouring particles."*  **(A7)** σ = (F/4r²)·k(1 − ε)/π — *"With r = d/2 then eqn. (4) results"* | p.263 · p.273 |
| f = 4πp/(ZD) 와의 관계 | 같은 관계 · 다른 꼴.  원문은 σ(F) 꼴이고 F 로 풀지 않았다.  대응 f ↔ F · p ↔ σ · Z ↔ k · D ↔ 1 − ε · R ↔ r → **f = 4πR²p/(ZD)**, R = 1 일 때만 4πp/(ZD) (파생).  지름 규약이면 F = πd²σ/(kD) | 파생 |
| 전제 | 단분산 · 무작위 충전 (*"a randomly packed bed consisting of monodisperse spheres is assumed throughout"*) + (i) 점 접촉 (ii) 접촉점 균등 분포 (iii) 등방 (면적 = 부피 기공률) + 정수압 + 통계 평균 접촉력 하나 (*"the absolute values of the radial contact forces are equal for any orientation of contacts in the statistical mean"*) + 정적 평형 | p.263 · p.271–272 |
| 평균장의 뜻 | 접촉력이 거시 응력과 접촉 방향만으로 정해진다 (정수압: 반경 방향 같은 크기 · 일축: 하중축에 평행한 F cos φ) = **정적 (응력 아핀) 가설** (§4-3).  힘 사슬 · 요동 없음 | p.263 · p.273 · 파생 |
| 배위수 · 밀도 | k 는 Smith 상관식 kε ≈ π 로만 ε 과 연결 (*"for porosities usually found in bulk solids"*).  Arzt (20) 는 식 (5) 를 쓰지 않고 (4) 꼴에 자기 Z(D) 를 넣는다 — 그래서 고밀도 외삽이 가능하다 | p.263 |
| 국소압 단서 | **원문에 없다.**  Molerus 의 비정수압 = 방향 의존 접촉력 N(φ) = F_M + F_R cos 2φ (식 6–8, 부록 B).  파생: 평균 법선력 ⟨N⟩ = F_M − F_R/3 ↔ 평균 응력 σ_M − σ_R/3 (σ₂ = σ₃) 가 같은 계수로 묶인다 → die 압밀에서 Arzt 의 "국소압" 자리에는 **국소 평균 응력 −tr σ/3** 을 넣는 것이 Molerus 틀과 정합하고, 방향 분포는 F_R cos 2φ 항이 따로 준다 | p.263 · p.273–274 · 파생 |
| 소성 접촉면적 관계 | **Tabor 꼴이 있다**: F_w = F_pl = p_f·f = p_f·π·δ·h.  경도 자리 = 소성 항복압 p_f (*"the plastic yield pressure p_f is greater than the yield stress σ_f observed in unhindered yielding"*) · Hencky [14] · Isklinsky [15] p_f ≈ 3σ_f · 석회석 5×10⁸ Pa.  ⚠ 척도 = 돌기 (δ ≈ 0.1 µm) · 하중 = N + F_vdW (식 9) · "small deformations simple considerations".  면적식 = 기하 절단 원판 (c² = 1, 파생) | p.264–265 |
| 응집 분말 항복 이론의 범위 | kPa · 1–20 µm 건조 미분말 · vdW 지배 · 기공률 일정 · 접촉 Coulomb → H = κN · tan φ_e = (1+κ) tan ρ · 이방성.  고밀도 압밀 · 형상 소성 · 파괴 · 다분산 · 재배열 · 직물 진화는 범위 밖 | p.262–271 |

- **arzt 카드 문장 대조** (정본 카드는 고치지 않는다 — 판단은 메인):
  - L-3 *"Σ_j F_ij = 4πR²·p/D = Z·f ← Arzt 식 (20) [Molerus 14] 그대로"* — **원문과 정합** (A7 를 F 로 푼 꼴 · R = r · 점 접촉).
  - §4-6 *"등방압 (식 20). die 압밀이면 p 를 국소압으로"* — Molerus 에는 없다.  Arzt 쪽 문장으로만 읽어야 한다 (Arzt 원문은 이 작업에서 열람하지 못했다 — PDF 미보유).
  - §4-7 *"등방 압축에서 국부 접촉력 ↔ 외부압 [14] (Molerus)"* — Molerus 의 F 는 "국부" 힘이 아니라 **통계 평균** 접촉력이다 (p.263).  낱말 차이.
  - 참고문헌 *"O. Molerus, Powder Technol. 12, 259 (1975)."* — 원문 머리말 (12 (1975) 259–275) 과 일치.
  - §7 *"3σ_f = H → σ_f ≈ 0.28 GPa"* — Arzt (19) 의 계수 3 (Hill [13]) 은 Molerus 에서도 같은 값 (Hencky · Isklinsky) 이다.  독립 출처 하나가 더 있다.

### 결정 9 — LHS-25 접촉별 추정량 (E1 · E2 · E3)
| 판 | 메모 v2 의 정의 · 지위 | Molerus 가 주는 것 | 지위에 미치는 영향 |
|---|---|---|---|
| E1 (현행) F_real/H | 실제 E 로 다시 만든 Hertz 힘 ÷ H — "느슨한 상한" | 같은 평탄화에서 탄성 특성이 소성 특성 위에 있으면 **소성 특성이 유효** (p.265, Fig. 3) → 힘 = 둘 중 작은 쪽.  메모 v2 §6-2 의 A_tabor/A_overlap = (2/3π)(E*/H)√(δ/R*) > 1 ⇔ δ/R* > 0.032 는 Molerus 전환점과 **같은 식**이다 (파생 §3-4: c² = 1 · p_f = H · 1/k₁₂ ↔ E*).  그 너머의 F_real 은 Molerus 모형에서 힘이 아니다 | **지지** — "physics (상한값)" 표지에 원전 근거 하나 추가 |
| E2 c²·A_overlap | 부피 보존 · c² 런 전 고정 (Arzt 1.27–1.40 · Storåkers ≈ 1.4) | f = πδh = **c² = 1 기하 절단** (*"small deformations simple considerations"*).  완전소성 p_f 와 짝지었지만, 완전소성 자기상사 해의 c² 는 ≈ 1.43 (`storakers1997_…` 카드) → Molerus 면적은 pile-up 을 뺀 **하단 근사**다.  또 이 면적은 우리 **hertz 모드 면적 (c_cpl[22] 교차 원판)** 과 1차에서 같은 양이다 | **변경 없음** — c² = 1 을 E2 값으로 쓰지 않는다.  쓰려면 "기하 절단 하단" 감도 행으로만 |
| E3 F_DEM/H | DEM 힘 = 평형 하중 · 단일 접촉 하한 | **이 꼴의 원전** — 평형 힘 (식 4 · 정적 평형) ÷ 구속 항복압 (p_f ≈ 3σ_f).  평균장 합 Σ_j A/(4πR²) = p/(D·p_f) (A7 + p_f) = arzt 카드 L-3 · 메모 v2 §6-3 의 0.35–0.42 와 같은 식.  ⚠ 평형식 (9) 는 N + F_vdW = p_f·f — 점착이 있으면 같은 N 에서 면적이 1/(1 − κ′) 배 (κ′ = A/(6πz₀³p_f)).  LPSCl 의 A · z₀ 는 이 논문에 없다 [미확인] — 보정의 크기는 n/a | **지지 + 한정어**: "점착 하중 제외 · 점 접촉 전제 · 단분산 평균장 대조선" |

- **C1 (진단 전용) 에 주는 것**:
  - ① 평균장 대조선 = **p̄ = p/D** (식 A7 ⇔ Love–Weber · 단분산 기대값).  300 MPa · D 0.84–0.90 에서 0.33–0.36 GPa (파생).  AM 의 p̄_i 분포를 이 선과 같은 축에 둔다.
  - ② Σ 에는 **법선 성분**만 넣는다.  원문 분해 (A9) 에서 평균 응력에 묶이는 것은 N(φ) 이고 T(φ) 는 아니다.  구에서는 가지 벡터 ∥ 법선이라 접선력이 trace 에 0 이다 (파생) → c_cpl 의 힘 벡터를 법선에 투영해서 쓴다 (|F| 를 쓰면 과대).
  - ③ 다분산 · 이종 (SE 기지 속 AM) 은 Molerus 범위 밖이다 → 입자별 Love–Weber (메모 v2 §6-3 그대로).  Molerus 는 그 항등식의 단분산 평균장 판을 **절단면 정역학**으로 준다.

### 결정별 인사이트 (메모 v2 §0-2 번호)
| 결정 | 이 논문이 주는 것 | 권고 변경 |
|---|---|---|
| 9 (LHS-25) | 위 표 — E1 상한 판정의 전환 규칙 (Fig. 3) · E2 c² = 1 은 하단 근사 · E3 꼴과 평균장 합의 원전 · C1 대조선 p/D · 법선 성분만 | **no** (근거 보강 · E3 한정어 추가) |
| 3 (hertz 먼저) | 우리 hertz 모드 면적 (c_cpl[22] 교차 원판) = Molerus 소성 평탄화 면적 f = πδh (c² = 1, 1차) — 탄성 Hertz 면적의 ≈ 2 배 (메모 v2 L1-04 의 2 − δ/(2r) 와 같은 사실).  ⇒ "hertz" 라는 이름이 탄성 Hertz 면적으로 오독될 위험 — 이 면적의 역학적 정체는 "기하 절단 (c² = 1) 면적" 이다 | **no** (열 사전 한정어 후보: "hertz = LIGGGHTS 교차 원판 = 기하 절단 면적, 탄성 Hertz 면적 아님") |
| 15 (키 이름) | f · κ · H · σ₀ · τ 다섯 글자가 Molerus · Arzt 와 우리에서 다른 양이다 (§4-8) | **no** (LHS-25 사전등록 문서에 F_c (접촉력) · A_c (접촉면적) · p_f/H (경도) 같은 꼬리표 강제 · 메모 v2 §6-3 의 κ_i 를 다른 글자로 바꾸는 것 고려) |
| 4 · 5 · 11 · 13 · 14 | 수송 양이 없어 직접 관련 없음 | — |

### 그 밖의 적용
- ① **총 소성 접촉면적은 배위수에 무관** (평균장): A_c = F/p_f 와 F = 4πr²σ/(kD) 를 곱하면 Σ A = kF/p_f = 4πr²σ/(D·p_f) — k 가 약분된다 (파생).  Molerus 가 "응집력 증가를 접촉 수 증가로 설명할 수 없다" (p.266 (1)) 고 쓴 것과 같은 구조이고, Arzt 의 "총 접촉면적 a·Z 만 들어간다" 의 원형이다.  ⇒ LHS-25 에서 "배위수가 높아 포화한다" 는 설명은 평균장에서 성립하지 않는다 — 포화는 p̄_i (응력 꼬리) 나 면적 추정량 (E1 상한) 에서 온다 (메모 v2 §6-3 의 H0 · H1 과 같은 쪽).
- ② **압밀 이력 이방성** (Fig. 6): 비정수압 압밀은 접촉 응집력 분포에 방향을 남긴다.  우리 die 압밀 (일축) 침대도 접촉 방향 분포가 등방이 아닐 것이다 — 접촉망 σ 의 z 방향 해석과 측면 해석이 다를 수 있다는 정성 경고 (검정은 DEM 접촉 방향 텐서로 — 이 논문 범위 밖).
- ③ **Rumpf 꼴과의 유사**: 식 (5) σ = (1 − ε)/ε·F/d² 는 정본 카드 `thakur2014_eepa_adhesive_elastoplastic_dem` 이 적는 "Rumpf 모델" (강도가 (1 − η)·Z 에 선형) 과 같은 (1 − ε)·k·F/d² 구조다 (카드 관찰 — 원문은 식 (4) 를 Rumpf 식이라 부르지 않는다.  Rumpf [2] 는 인장강도 문헌으로만 인용).
- ④ **입경에 따른 취성 → 소성 경계**: Schönert–Steier [16] 는 1–20 µm 단일 미립자에서 취성 파괴가 파쇄 없는 소성 평탄화로 바뀌는 한계를 조사했다 (p.265 — 원문은 그 경계 입경 값을 인용하지 않는다).  황화물 SE 의 "작으면 협동 변형 · 크면 파쇄" 와 **같은 종류의 개념**일 뿐 — 석회석 수치를 LPSCl 로 옮기지 않는다.
- ⑤ **응집력 ∝ 하중** (H = κN): 우리 DEM 이 점착을 쓰는 경우 (설정 [미확인]) 그 점착을 최대 하중 · 소성 평탄화에 묶는 접촉 법칙 계열 (`luding2008_…` · `thakur2014_…` · `pasha2014_…` · `zunker2024_…`) 의 물리적 동기가 이 논문의 "frozen cohesion" 이다 — 그 카드들이 Molerus 를 인용하는지는 확인하지 않았다.

## 9. 인용 가능 문장 (deck/paper용)
- "For a random, isotropic packing of monodisperse spheres with point contacts under hydrostatic stress, Molerus (Powder Technol. 12, 259, 1975; Eq. 4 and Appendix A) derived σ = F·k(1−ε)/(π d²), i.e. a mean contact normal force F = π d² σ/[k(1−ε)] = 4π r² σ/[k(1−ε)]; with the particle radius set to unity this is the relation f = 4πp/(ZD) used by Arzt (1982)."
- "Molerus modelled the plastic resistance of a flattened contact as F_pl = p_f·π·δ·h, with a constrained plastic yield pressure p_f ≈ 3σ_f (after Hencky and Ishlinsky), and took the plastic branch wherever the elastic Hertz characteristic lies above it."
- "Because plastic flattening freezes in the van der Waals adhesion, the cohesion force becomes proportional to the consolidating force, H = κN with κ = A/(6π z₀³ p_f), which makes the effective yield locus a straight line through the origin with tan φ_e = (1+κ) tan ρ."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **kPa 응집 분말 이론**이다 — 수치 예 7×10³ Pa · ε 0.61 · 석회석 · barytes.  300 MPa · ε ≈ 0.15 의 LPSCl 복합체로 수치를 옮기지 않는다.  옮기는 것은 식의 **꼴** (평균장 · 접촉 법칙) 뿐이다.
- ⚠ **식 (4) 는 점 접촉 (전제 i) · 단분산 · 등방 · 정수압 · 통계 평균 힘**의 결과다.  300 MPa 평균장에서는 접촉이 표면의 ≈ 40 % 라 (i) 이 깨진다 (§3-4 파생).  다분산 · 이종 침대의 입자별 판은 이 논문에서 나오지 않는다 (Love–Weber 필요).
- ⚠ **등방 법선력 분포는 가정**이다 (*"at least plausible"*, p.263 · p.272).  힘 사슬 · 응력 꼬리를 원리적으로 못 본다 — LHS-25 포화 (응력 꼬리 가설) 는 이 평균장으로 판정할 수 없다.
- ⚠ **kε ≈ π (식 5) 는 느슨한 분말 상관식** (Smith [10]) — 고밀도에 쓰면 k 를 ≈ 2 배 과대 (§3-4).  식 (8) · (18)–(21) 도 이 계수로 쓰였다.
- ⚠ **소성 면적식 f = πδh 는 돌기 척도 · "small deformations simple considerations"** 이다.  기하 절단 (c² = 1) 이라 완전소성 pile-up (Storåkers c² ≈ 1.43) 을 뺀다.  입자 척도 평탄화에 쓰는 것은 Arzt 의 확장이지 Molerus 의 검증 범위가 아니다.
- ⚠ **이론 H/N 0.15 vs 전단시험 0.33** (2 배 차) — 저자 스스로 Hamaker 과소 · 모세관 응축을 후보로 든다.  이론의 정량 정확도는 이 정도다.
- ⚠ 이방성 실험 (Fig. 6) 은 **1 재료 · 1 장치 (Jenike 셀)** — 저자도 "well-known shortcomings of the Jenike shear cell" 을 인정한다.
- ⚠ 원문 수치 · 기호 오식: N 9.67 vs 재계산 9.85 (−1.9 %) · k_i = (1 − ν_i)/E_i (Hertz 표준과 다름 — 인쇄값은 인쇄식과 정합) · δ 지름 (본문) ↔ 반지름 (기호표) · "geometrical mean" 오기 · [15] 철자 "Isklinsky" / "Insklinsky" · k · H 의 이중 사용 (§3-5).
- ⚠ §3-4 의 평균장 크기 감각 (F 1.7×10⁻⁴ N · 0.415) 은 **카드 산술 (단분산 · 가정 대입)** 이다 — 우리 침대 값으로 쓰지 않는다.
- **arzt 카드와의 어긋남** (§8 상세 · 카드는 고치지 않는다): ① "die 압밀이면 p 를 국소압으로" 는 Molerus 원문에 없다 (Arzt 원문은 이 작업에서 미열람) ② "국부 접촉력" ↔ 원문 "statistical mean" 접촉력 ③ 그 밖의 옮김 (L-3 식 · 서지 · 계수 3) 은 원문과 정합.
- **메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`):
  - ① **§6-3 셋째 하위 줄** *"(20) 자체가 Molerus 의 등방 평균장 결과이고, die 압밀에는 국소압으로 바꾸라는 단서가 붙어 있다"* — 앞 절반은 원문과 맞다 (식 4 · A7, p.263 · p.273).  뒤 절반의 단서는 **Molerus 에 없다** (p.259–275 전수).  출처를 나눠 적을 후보: *"(20) 은 Molerus 식 (4)/(A7) (σ = F·k(1−ε)/(πd²) — 단분산 · 점 접촉 · 등방 · 정수압 평균장) 을 R = 1 로 푼 것이다.  die 압밀 단서는 Arzt 의 것이고, Molerus 의 비정수압 처리는 방향 의존 접촉력 N(φ) = F_M + F_R cos 2φ (식 6–8 · 부록 B, p.263 · p.273–274) 다 — 평균 법선력은 평균 응력 −tr σ/3 에 묶인다 (파생)."*
  - ② **§6-3 첫 줄의 "보정 셋" 중 "접선력"** — 평균압 (trace) 항등식에는 접선력이 들어가지 않는다 (구: 가지 벡터 ∥ 법선 → x·f_t = 0, 파생).  원문 분해 (A9) 도 평균 응력에 묶이는 것은 N(φ) 뿐이다 (p.273).  보정 항목이 아니라 **"Σ 에 법선 성분만 쓴다 (|F| 금지)"** 라는 사용 규칙으로 바꿀 후보 (작은 정정).
  - ③ **§8-2 Molerus 행** *"힘 ↔ 외부압 f = 4πp/(ZD)"* — 원문 꼴은 σ(F) (식 4 · A7) 이고 4πp/(ZD) 는 R = 1 로 푼 Arzt 판이라는 괄호를 덧붙일 후보 (상수 4π ↔ 반지름 규약).

## 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 원문 ref | 목록 서지 (그대로, p.274–275) | 왜 |
|---|---|---|
| [10] | W.O. Smith, P.D. Foote and P.F. Busang, Phys. Rev., 34 (1929) 1271. | kε ≈ π 상관식의 원자료 — 배위수 ↔ 기공률 (우리 CN 대조의 고전 기준) |
| [14] | H. Hencky, Z. Angew. Math. Mech., 3 (1923) 241. | p_f ≈ 3σ_f 의 이론 원전 (평면 소성) — E3 의 H ↔ σ_y 환산 근거 |
| [15] | A.J. Insklinsky, J. Appl. Math. Mech. (USSR), 8 (1944) 233 (Engl. transl.). | 같은 계수의 축대칭 원전 (본문 철자 "Isklinsky") |
| [12] | B. Dahneke, J. Colloid Interface Sci., 40 (1972) 1 - 13. | 평탄화 vdW (식 10) · z₀ · 광물 Hamaker 범위 |
| [16] | K. Schönert and K. Steier, Chem. Ing. Tech., 43 (1971) 773 - 777. | 단일 미립자의 취성 → 소성 경계 (1–20 µm) · p_f 측정 |
| [1] | H. Krupp, Adv. Colloid Interface Sci., 1 (1967) 111. | 돌기 척도 접착 (0.1 µm) |
| [2] | H. Rumpf, Chem. Ing. Tech., 46 (1974) 1 - 11. | 벌크 인장강도 (Rumpf 꼴) |
| [4] | J. Schwedes, Dr.-Ing. Thesis, Karlsruhe, 1971. | 석회석 전단시험 270 회 · 수치 예 입력 |
| [9] | A.W. Jenike, Storage and flow of solids, Utah Univ. Eng. Exp. Stn. Bull. 123 (1964). | 2단계 압밀 · 호퍼 설계 |
| [3] | M.D. Ashton, D.C.-H. Cheng, R. Farley and F.H.H. Valentin, Rheol. Acta, 4 (1965) 206 - 218. | 연속체 상태식 (식 1) |
| [6] | K.H. Roscoe, Bergbauwissenschaften, 14 (1967) 464 - 472. | 상태도 · 공극비 |
| [5] | C.R. Calladine, Géotechnique, 21 (1971) 391 - 415. | 점토의 미시 구조 해석 (저자 비판 대상) |
| [7] | J.C. Williams and A.H. Birks, Rheol. Acta, 4 (1965) 170 - 180. | 저강도 분말의 상태도 |
| [8] | J. Leipholz, Einführung in die Elastizitätstheorie, G. Braun, Karlsruhe, 1968. | Mohr 원 교재 |
| [11] | H.C. Hamaker, Physica, 4 (1937) 1058. | vdW 구–구 고전식 |
| [13] | H. Hertz, Derivation of Hertz's eqns., see for example I. Szabó, Höhere Techn. Mechanik, Springer, Berlin, 4th edn., 1964, p. 169. | 탄성 접촉 |

## 🔗 이 정의 · 방법을 쓰는 corpus 카드
- `arzt1982_particle_coordination_densification_spheres` — ref [14] 로 이 논문을 식 (20) f = 4πp/(ZD) 의 출처로 인용 · L-3 포화 판별식의 평균장 원전 (대조 §8 · §10).
- `storakers1997_similarity_inelastic_contact` — A = 2πc²rh 의 c² (완전소성 ≈ 1.43 · 전환 1 · 선형 0.5) — Molerus f = πδh 의 c² = 1 자리매김.
- `zunker2024_mdr_contact_model_partI` — 구속 항복압 p̄/Y 2.75 · 인정 범위 2.61–2.84 (Ishlinsky 1944 포함) — Molerus 의 "≈ 3" 과 같은 계수.
- `thakur2014_eepa_adhesive_elastoplastic_dem` · `luding2008_cohesive_frictional_contact_models` · `pasha2014_linear_elastoplastic_adhesive_contact` — 점착을 소성 변형에 묶는 DEM 접촉 법칙 계열 (이 논문 인용 여부 미확인).
- `giannis2021_stress_based_multicontact_dem` — 입자 응력 (Love–Weber) 로 접촉을 묶는 비이체 DEM — 평균장 너머의 다접촉 처리.
- 메인 리포 정본: 판단 메모 v2 §6-2 · §6-3 · §6-4 · §8-2 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
