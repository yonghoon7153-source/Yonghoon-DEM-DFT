---
title: Li 금속의 항복 · creep 과 스택 압력 계보 — 벌크 실측이 0.1–5 MPa 띠에 놓는 눈금
description: "Bulk polycrystalline Li at room temperature (Masias 2019): E 7.82 / G 2.83 GPa, yield 0.73–0.81 MPa, tensile power-law creep n = 6.56 measured below yield (0.2–0.6 MPa). Laid over the ASSB operating-pressure lineage (0.1–5 MPa) the band crosses diffusional creep, power-law creep, yield and power-law breakdown - a x50 pressure band is a 6–11 decade creep-rate band"
created: 2026-09-28
updated: 2026-09-29
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal.md, raw/papers/xu2024_pressure-effects-countermeasures-ssb-review.md, raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md, raw/papers/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode.md, raw/papers/zhang2025_pressure-free-si-li21si5-double-layer-anode-assb.md, raw/papers/li2025_stack-pressure-critical-importance-perspective.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: single-source
---

# Li 금속의 항복 · creep 과 스택 압력 계보 — 벌크 실측이 0.1–5 MPa 띠에 놓는 눈금

> `assb` 축의 개념 페이지. 닻은 [[assb-contact-loss-vs-lampe]], 압력 창은 [[assb-stack-pressure-operating-window]].
> 수치의 원전은 **한 편**(`assb` 61호 Masias · Felten · Garcia-Mendez · Wolfenstine · Sakamoto 2019, *J. Mater. Sci.* 54, 2585 —
> `raw/papers/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal.md`)이다. 그래서 `evidenceScope: single-source` · `confidence: low`.
> 이 페이지가 하는 일은 **압력 계보의 값들을 Li 의 눈금 위에 놓는 것**이고, Li 의 성질을 새로 주장하는 것이 아니다.

## 정의 — 원전이 인쇄한 값 (`[인쇄]`, 실온 ≈26 °C = 0.66 `T/Tm`, 다결정 벌크 원통 12.7 mm)

| 양 | 값 | 방법 · 조건 |
|---|---|---|
| Young 률 `E` | **7.82 GPa** | 펄스-에코 음향, 시편 높이 0.75 · 8.83 · 12.35 mm 평균(7.88 · 7.79 · 7.80) |
| 전단탄성률 `G` | **2.83 GPa** | 〃 (2.88 · 2.80 · 2.82) — Monroe–Newman 기준 `G_SE ≥ 2 G_Li` 의 입력(`[재현]` ≥ 5.66 GPa) |
| 체적탄성률 `K` | 11.1 GPa | 〃 (9.92 · 12.12 · 11.18 — 폭 20 %) |
| 푸아송비 `ν` | **0.381** | 〃 |
| 항복 응력 `σ_y` | **0.73–0.81 MPa** | 인장 0.2 % 오프셋(음향 `E` · 응력-변형 기울기 0.43 GPa 로 각각) · 압축 변곡 0.81 ± 0.10 MPa(4 시편) · 문헌 µm 급 다결정 0.60–0.81 |
| 인장 creep 응력 지수 `n` | **6.56** | 최소 2차 creep 속도 vs 응력, **0.2–0.6 MPa(항복 아래)** · AR ≈4 · 7 시험 — 2.0×10⁻⁷(0.2) → 3.89×10⁻⁴ s⁻¹(0.6). 정규화(Na · K 와 한 선) 6.70 |
| 기구 배정 | dislocation climb(격자 확산 율속) | `n` 5–7 · σ/G 7×10⁻⁵–2×10⁻⁴ 를 Sargent & Ashby 1984 지도와 대조 — 미세구조 증거 0 |
| 지도 경계(원전이 인쇄한 [32] 기준) | σ/G < 10⁻⁴ 확산 creep · > 10⁻³ power-law breakdown | `[재현]` `G` 2.83 GPa 로 **0.28 MPa · 2.83 MPa** |
| 압축 시간 의존 변형 | 0.8–2.4 MPa 에서 12 · 60 · 120 분 속도 1.9×10⁻⁴ → 2.6×10⁻⁶ s⁻¹ | ⚠ 응력 ↑ 에 속도 ↓(0.8 → 2.4 MPa 에서 ×0.21) — 마찰 · 배럴링 지배, **재료 법칙이 아니다**(저자 인정) |
| 활성화 에너지 `Qc` · 입도 `d` · `p` | **미측정** | 온도 1 점 · "assumed … polycrystalline" |

`[재현]` Table S1 7 점의 로그–로그 적합: `n` = 6.562 · `A` = 7.7×10⁻³ s⁻¹ MPa⁻ⁿ(0.6 MPa 점을 빼면 `n` = 6.04 — 양 끝 한 점씩이 지수를 정한다).

## 왜 중요한가 — 계보의 압력 띠는 한 물리가 아니다

[[assb-stack-pressure-operating-window]] 가 모은 운전 압력 요구치는 **여덟 편 · 0.1–5 MPa · 확인된 원전 0**(59 · 60 · 61호). (2026-09-29 81호: 8호가 가리킨 원문 Xu 2024 도
`< 1 MPa` 를 인용 0 으로 인쇄 — 아홉 편 · 독립 인쇄 여덟 · 원전 0 그대로.) 그 띠를 Li 의 눈금 위에 놓으면:

| 계보 값 (MPa) | 출처 | σ/G | Li 눈금 | `[재현]` 인장 멱법칙(`n` 6.56)으로 1 % 변형에 걸리는 시간 |
|---:|---|---:|---|---|
| 0.1 | 59호 요구치 | 3.5×10⁻⁵ | 시험 범위 밖 · **확산 creep 영역** — 멱법칙 외삽은 하한(그 영역은 `n` ≈ 1 로 더 빠르다) | ≈55 일(하한) |
| 0.2 · 0.4 · 0.6 | 61호 인장 creep 측정 | 0.7–2.1×10⁻⁴ | **멱법칙 creep(측정)** | 14 h · ≈12 분 · ≈26 s(측정값) |
| **0.73–0.81** | **항복** | 2.6–2.9×10⁻⁴ | | ≈10 → 5 s(외삽) |
| 0.8 | 60호 정변위 지그 예압 · 61호 압축 하한 | 2.85×10⁻⁴ | 항복 자리 | |
| 1 | 61호 기준값("we believe sufficient") · 8호 ≈1(= 81호 < 1 의 재인용) · 39호 1 · 5호 아래 벽 최저점 | 3.5×10⁻⁴ | 항복 바로 위 · 압축 시험 범위 | ≈1 s(외삽) |
| 2 | 33호 <2 · 4호 ~2 · 6호 2–4 | 7.1×10⁻⁴ | 압축 시험 범위 | ms(외삽) |
| ≈2.3 | 60호 첫 충전 총(0.8 + 1.51) | 8.2×10⁻⁴ | 압축 상한 근처 | |
| **2.83** | σ/G = 10⁻³ | 10⁻³ | **power-law breakdown 경계** — 위로는 멱법칙 외삽 무효 | |
| 5 | 5호 운전("optimal") · 13호 <5 · 25호 ≤5 | 1.8×10⁻³ | breakdown 영역 · 항복의 6× | (무효) |
| 10–75 | 5호 위 벽(474 h → 0 h 단락) | 3.5×10⁻³–2.7×10⁻² | 항복의 13–94× | |

- `[재현]` 0.1 → 5 MPa 는 멱법칙으로 creep 속도 **×1.4×10¹¹**(11 자릿수); 외삽이 유효한 0.28–2.83 MPa 만 잡아도 **×3.8×10⁶**. **압력 ×50 이 Li 시간 척도 6–11 자릿수다.**
- `[해석]` 띠 안에서 결정되는 것은 "Li 이 한 번의 충전(12–120 분) 안에 1 % 변형만큼 계면을 채우는가(≥0.4 MPa) · 하루(0.2) · 두 달(0.1) 인가" 다.
  13호 항의 "≈1–5 MPa 수렴"(59호가 반박)은 설령 섰더라도 **한 눈금이 아니었다**. 5호의 "optimal 5 MPa" 는 항복의 6배 · breakdown 영역이고, 5호 아래 벽(1 → 5 MPa 에서
  임피던스 > 500 → 110 Ω)은 Li 가 항복 바로 위에서 breakdown 경계로 넘어가는 구간과 겹친다 — 단 5호 셀은 Li₆PS₅Cl 이고 원전은 SE 0 이다.

## 인용 귀속 — 이 원전에 매달린 명제들의 판정

| 인용처 | 매단 명제 | 원전 | 판정 |
|---|---|---|---|
| 5호 Doux 2020 ref 15(5호 digest 문장 기준) | E · G · ν 측정 · 항복 ≈0.8 · Tariq 2003 과 일치 | 7.82 · 2.83 · 0.381 · 0.73–0.81 · Tariq 0.76 | ✅ |
| 〃 | **"그 위에서 creep 시작"** | `[인쇄]` "studied at loads **below** the 0.8 MPa yield point between 0.2 and 0.6 MPa" | ❌ — creep 은 항복 아래에서 쟀다; 항복은 creep 의 문턱이 아니라 눈금이다 |
| [[assb-stack-pressure-operating-window]] §정의 | "Li 가 항복강도(≈0.8 MPa)를 넘어 크리프하고" | 위와 같음 | ❌ 정정 — "creep 속도가 σ^6.56 로 커져 항복 근처에서 1 % 변형이 초 단위" |
| 21호 Sedlmeier 2023 ref 49 | 원통 펠릿에서 Li 가 In 가장자리 · 벽 사이로 분리막 쪽에 기어드는 Li creep | 펠릿 · In · 분리막 0; Fig. 10a–c 모식("no hydrostatic pressure in Li" → Li 가 옆으로 흐름) | ✅ 재료 전제 · ⚠ 기하 명제는 21호 자신의 것 |
| 21호 Li\|Li 셀 3 MPa "Li creep 방지" | | 3 MPa = 항복 ≈4× · σ/G 1.06×10⁻³ | `[해석]` 압력이 막은 것이 아니라 분리막 두께(네 장)로 막은 것 |
| 46호 Schlenker 2020 ref 51 → Wang & Sakamoto 2018 | "Li 항복 2 MPa" | 같은 실험실 1 년 뒤 0.73–0.81 | ⚠ 2.5× — Wang 2018 미열람; 46호 논증(Li 경도로는 44 MPa 까지의 계면 임피던스 감소를 설명 못 함)은 항복이 낮을수록 강해진다 |
| 14호 · 5호 → LePage 2019 | "10 MPa 는 Li creep 을 일으키기에 충분" | 10 MPa = 항복 13× · breakdown 영역 | ✅ 방향(a fortiori) — LePage 미열람 |
| 61호 자신 → [9] Sharafi 2016 · [10] Wang & Sakamoto 2018 | "stack pressures in the 1.0 MPa range are necessary to achieve low and stable cell resistance" | 같은 지면: "How much compressive stress is not known … We believe 1 MPa was sufficient" | ⚠ 요구치와 미지가 같은 지면 — 계보 "≈1 MPa" 의 가장 이른 인쇄(2018); 원전 둘 미열람 |

⚠ **2026-09-29 (81호 Xu 2024 *Adv. Energy Mater.* — 종설 · 1차 측정 0) 주석 — 이 눈금에 대조 넷.** 81호는 이 원전을 [68] 로 인용하되 Li 연성 문장("[66–68]")에만 붙이고 수치를 옮기지 않는다.
같은 지면의 다른 Li 값을 이 페이지 눈금과 맞대면:

| 81호 인쇄 · 재수록 | 값 | 이 눈금과 | 판정 |
|---|---|---|---|
| Fig. 5b 이론 띠 [69](`[도표]` 그림 속 글자) | Li 경도 `H_Li` = 2–8 MPa | `[재현]` Tabor(H ≈3 σ_y) × 항복 0.73–0.81 = 2.2–2.4 MPa | 띠의 아래 끝과 맞는다 — 위 끝 8 MPa 는 항복의 ≈10 배 |
| Monroe–Newman 문장 [95] | `G_Li` "4.8 GPa at 298 K" | 이 원전 실측 2.83 GPa | ×1.7 — 기준 `G_SE ≥ 2 G_Li` 가 9.6 ↔ 5.66 GPa 로 갈린다 |
| Ding 2021 [67] | Li 박 압축 creep 0.6–3.6 MPa · "notable … even at applied pressures below 2 MPa" | 멱법칙 · 항복 · breakdown 경계(2.83)를 가로지른다 | 방향 일치(Li 박 · 압축 — 원전 미열람) |
| Wang 2019 [7] 재수록(Fig. 6c) | "critical stack pressure" ≈0.4 MPa · `[재현]` 두 변형률 교차 ≈0.64–0.67 · 공극 봉우리 ≈0.25 MPa | 항복 0.73–0.81 바로 아래 · 멱법칙 영역 | 모형의 아래 벽이 이 원전의 creep 측정 구간(0.2–0.6) 가까이 앉는다 — Wang 2019 은 같은 실험실 |

⇒ "≈1 MPa 가닥 = Sakamoto 실험실 한 뿌리" 가설은 81호로 진전이 없다 — 81호 참고문헌에 Sharafi 2016 · Wang & Sakamoto 2018 · Wang 2021 *Joule* 은 0 이고, Sakamoto 실험실 편 여덟은 인용되지만
"< 1 MPa" 문장에는 붙지 않는다.

## 이 위키에서의 적용

1. **압력 값에 영역을 붙인다** — 계보 · 합성 truth · 이식판의 운전 압력을 적을 때 `< 0.28`(확산) · `0.28–2.83`(멱법칙 · 항복 포함) · `> 2.83 MPa`(breakdown) 을 괄호로 붙인다(카드 새 제약 1, 61호).
2. **"Li creep 이 계면을 채운다" 는 감도 구조까지만** — 원전이 준 것은 `n` 하나다. 채움 실험 · `Qc` · 입도 · 접착 계수는 0(카드 새 제약 2).
3. **압력을 걸고 잰 시각을 적는다** — 음극 계면의 압력 응답은 σ^6.56 의 시간 상수(0.2 MPa ≈14 h · 1 MPa ≈1 s, 1 % 변형 · 외삽). [[assb-pressure-reapplication-separation-test]] D1 에 유지 시간 ·
   회복 시간 곡선을 붙이고, **회복의 시간 상수로 음극/양극 몫을 가르는 것**을 제안으로 둔다(실측 0).
4. **3 항 분해에서의 자리** — [[assb-apparent-capacity-decomposition]] 의 `η(i, P)` 음극 몫에 시간 의존을 준다. 양극 `θ_AM` · [[assb-lampe-contact-product-degeneracy]] 의 곱에는 직접 닿지 않는다.
5. **합성 truth 로 옮길 때 빠지는 것 여덟**(61호 (c)) — 셀 · SE · 계면 0 · 형상비 1–4.6 ↔ 셀 Li 박 ≈10⁻⁴(원전 자신의 추정) · 마찰 · 접착 계수 미지 · 온도 1 점 · 반복 · 진동 하중 0 ·
   도금 Li 미세구조 0 · 계면 void 채움의 경계값 문제 ≠ 단축 시험 · 양극 0. [[assb-synthetic-truth-contact-loss-requirements]] 의 압력 의존 `θ(P, t)` 는 아직 없는 요구다.

## 원전 안의 어긋남 — 값을 옮길 때 주의 (61호 digest D 목록에서)

- 인장 항복 0.81/0.73 의 SS/PE 대응이 본문과 Table 3 에서 **반대**(D1) — Table 3(PE 7.82 GPa → 0.73 · SS 0.43 GPa → 0.81)이 물리적으로 맞다; `[도표]` 인셋 교점은 ≈0.63 / ≈0.76.
- 본문 "0.4 % 이후 응력 감소" ↔ Fig. 2 는 `[도표]` ≈4 % 에서 ≈0.93 MPa 정점(D2).
- σ/G 저/고 응력 값이 본문에서 뒤바뀜(D3) · Fig. 7 정규화의 `D` 인쇄값(3.1×10⁻¹ cm² s⁻¹)으로는 그림이 재현되지 않음 — `[재현]` 그림은 ≈9×10⁻¹¹ 을 썼다(D4).
- 크로스헤드 "1 mm/s" ↔ 1.22×10⁻³ s⁻¹ 는 1 mm/min 으로만 성립(D5).

## 이 페이지가 주장하지 않는 것

- **Li 이 계면을 creep 으로 채우지 않는다고 하지 않는다** — 원전이 그 명제를 재지 않았다는 것까지.
- **멱법칙 외삽값(1 % 변형 시간)을 셀의 값으로 쓰지 않는다** — 벌크 · 인장 · AR 4 · 실온 · 단조 하중의 외삽이고, 0.28 MPa 아래는 하한 · 2.83 MPa 위는 무효다.
- **압축 표(0.8–2.4 MPa)의 값을 Li 의 creep 속도로 쓰지 않는다** — 응력 순서가 역전된 장치 값이다.
- **계보의 값들이 틀렸다고 하지 않는다** — 서로 다른 물리 영역의 값이라는 것까지.
- **Doux 2020 · Wang & Sakamoto 2018 의 원문 어구를 확인했다고 하지 않는다** — 5호 · 46호 digest 문장 기준이다.
- **"≈1 MPa 가닥 = Sakamoto 실험실 한 뿌리" 는 가설이다** — 원전 넷(Sharafi 2016 · Wang 2018 · Masias 2019 · Wang 2021) 중 열어 본 것이 Masias 뿐이다.

## 관련
- [[assb-stack-pressure-operating-window]] — 이 눈금이 놓이는 창. §정의의 "항복을 넘어 creep" 정정은 61호 절.
- [[assb-pressure-reapplication-separation-test]] — `P↑` 연산자에 붙는 유지 시간 · 회복 시간 상수(61호 절).
- [[assb-apparent-capacity-decomposition]] — `η(i, P)` 의 음극 몫이 시간 의존이 되는 자리.
- [[assb-lampe-contact-product-degeneracy]] — 양극 곱에는 닿지 않는다(마흔네 번째 적용 · 대상 없음).
- [[assb-synthetic-truth-contact-loss-requirements]] — 압력 의존 `θ(P, t)` 를 넣을 때의 입력 · 빠지는 것 여덟.
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 페이지는 그 질문의 우회로(압력 축)에 재료 눈금을 준다.
