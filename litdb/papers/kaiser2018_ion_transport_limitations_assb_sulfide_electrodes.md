<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     τ 묶음 형식 기준 = landesfeind2016_tortuosity_eis_electrodes_separators.md · nguyen2020_electrode_tortuosity_factor.md ·
     tjaden2018_tortuosity_review_calculation_approaches.md (같은 묶음의 선배 카드).
     이 논문은 실험 (EIS) 논문이다 — 시뮬레이션이 없다.  그래서 §4 '방법' 을 측정 사슬 (정의식 → 셀 → 압력 이력 → 적합 → τ_eff) 로 쓴다.
     쪽 표기: 본문 = 인쇄 (학술지) 쪽.  PDF n 쪽 = 인쇄 p.(174 + n)  (PDF 1 = p.175 … PDF 7 = p.181).
     SI = 별도 PDF 4 쪽 ("8. Sup) Ion transport limitations in all-solid-state lithium battery electrodes containing a sulfide-based electrolyte.pdf").
     SI 에는 인쇄 쪽 번호가 없다 → "SI p.n" = SI PDF 쪽.
     값 표지: stated = 본문·캡션·표 원문 / 판독 = 그림에서 읽은 값 (≈ · 추세 전용, 정밀 인용 불가) / 파생 = 카드 작성자 계산 (식 명시). -->
# 황화물 SE 복합 전극의 이온 수송 한계 — EIS 로 τ_eff 측정: 전송선 모델 (TLM) vs 전자 차단 Li⁺ 전류 · Li₄Ti₅O₁₂ + Li₇P₂S₈I 유리 + 카본블랙 · ε ≥ 0.4 일치 / ε 0.3 에서 한 자릿수 차 · Bruggeman 지수 5.6–5.7 — Kaiser (J. Power Sources 2018)

> slug `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · DOI `10.1016/j.jpowsour.2018.05.095` · type `exp (EIS 대칭셀 3 종 — 전송선 모델 TLM · 전자 차단 Li⁺ 전류 · 같은 전극 두 방법; 황화물 ASSB 복합 전극 τ_eff)` · PDF `8. Ion transport limitations in all-solid-state lithium battery electrodes containing a sulfide-based electrolyte.pdf` · digested `2026-10-03` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 τ_eff 는 **τ_eff = ε·σ_ion,electrolyte/σ_ion,eff** (Eq. 2, p.176) 이다.  이름은 *"effective (ion transport) tortuosity"* (제곱 기호 · "factor" 낱말 없음) 지만
> 값의 꼴은 **tortuosity factor (τ² 계열) = 우리 `tau2` 꼴**이다.  정규화가 우리와 두 군데 다르다: **ε = 기공 0 가정의 고체 기준 SE 부피분율** (SI Table S1–S4, vol% 합 100) ·
> **σ₀ = 순수 Li₇P₂S₈I 유리 펠릿** (276 MPa · 30 min, 25 °C; 배치별 0.68–0.81 mS/cm) — 펠릿이 τ_eff ≡ 1 인 기준이다 (같은 그룹 Minnmann 2021 과 같은 관례).
> 두 측정법은 원문에서 같은 Eq. 2 로 환산되지만 **경계조건이 다르다**: 전자 차단 Li⁺ 전류 (Li | SE | 전극 | SE | Li, DC 극한 Eq. 11) = **conventional (관통형) τ** = 우리 망 T 와 같은 꼴 ·
> 비패러데이 TLM (전극 | SE | 전극, Eq. 6 의 R_ion/3) = **τ_e 계열** (Nguyen 2020 eSCM) — 우리에게 없는 양.  ⇒ 이 논문은 **ASSB 에서 두 정의를 실측으로 맞댄 사례**다 (ε ≥ 0.4 거의 같고 ε 0.3 에서 TLM 이 한 자릿수 가까이 높다).
>
> 형제 카드: `minnmann2021_jes_charge_transport_bottlenecks` (같은 Marburg · Roling 그룹, 이 논문을 [25] 로 인용) · `landesfeind2016_tortuosity_eis_electrodes_separators` (= 이 논문 [9], 액체 LIB 차단 대칭셀 TLM 원조) ·
> `nguyen2020_electrode_tortuosity_factor` (τ ↔ τ_e 정의 구분 — 이 논문보다 2 년 뒤) · `tjaden2018_tortuosity_review_calculation_approaches` (명명 정본).  역링크: `lee2026_lpscl_coating_thickness_ncm811` 이 *"대칭셀 EIS 최저주파 저항 = DC"* 근거로 이 논문을 ref 41 로 인용.

---

## 0. 결론 먼저 (정의 판정 + 핵심 수치)

| 질문 | 답 | 근거 (식·쪽) |
|---|---|---|
| τ_eff 는 어떤 양인가 | **ε·σ₀/σ_eff** — 원문 이름 "effective tortuosity", 값의 꼴은 tortuosity factor (τ²) = 우리 `tau2` 꼴.  √ 값은 보고하지 않는다 | Eq. 1 · Eq. 2 (p.176) |
| σ₀ 기준 | **순수 Li₇P₂S₈I (LPSI) 유리 펠릿** — 276 MPa · 30 min · RT 압축, 양면 Au 스퍼터, 25 °C 값.  본문 (0.75 ± 0.1) mS/cm, 배치별 0.68 (Fig. 4) · 0.81 (Fig. 6) · 0.78 (Fig. 7).  Fig. 8B 가 ε = 1 에 이 값을 그린다 = **펠릿 ≡ τ 1** | p.178 · 캡션 p.179–180 |
| ε 기준 | SE 부피분율 — wt% 와 밀도로 계산한 **기공 0 고체 기준** (카본 12.5–14.6 vol% 를 고체 쪽에 포함).  기공률은 재지 않았다 (FIB-SEM 정성 "densely packed") | SI Table S1–S4 (SI p.2–3) · SI §4 (SI p.4) |
| 두 측정법 = 같은 정의? | **아니다** — Li⁺ 전류 (Type-B, DC 관통) = conventional τ · TLM (Type-A) = τ_e 계열.  원문은 구분하지 않고 둘 다 τ_eff 라 부른다 | Eq. 6 · Eq. 11 (p.177) · nguyen2020 카드 |
| 두 방법 일치 | ε ≥ 0.4 *"very similar"* — 같은 전극 (ε 0.66, Type-C) 에서 **2.0 ± 0.1 (TLM) vs 2.1 ± 0.1 (Li⁺)**.  ε 0.3 에서 TLM 이 *"almost one order of magnitude higher"* (판독 ≈ 2.2×10³ vs ≈ 3.3×10²) | p.178–179 · Fig. 7 · Fig. 8A |
| τ(ε) | Bruggeman 지수 **α = 5.7 (TLM) · 5.6 (Li⁺)**, ε 0.4–0.66 (구 α 0.5 의 ≈ 11 배).  ⚠ 맞춤선 절편 ≠ 0 (판독 전인자 ≈ 0.17) → 전인자 없는 Eq. 3 형이 아니다 (§10) | p.180 · Fig. 8A |
| 크기 감각 | τ_eff **1.6–2.1 @ ε 0.66** · ≈ 26–33 @ 0.40 · ≈ 3×10²–2×10³ @ 0.30 (판독).  σ_eff 0.75 mS/cm (ε 1) → **1.2·10⁻⁵ S/cm (ε 0.4)** → ≈ 10⁻⁶ S/cm (ε 0.3) | p.178–180 |
| 결론 (원문) | ε ≈ 0.4 에서 액체 LIB 와 같은 출력밀도를 내려면 SE σ **5–10 mS/cm** 필요 | p.180 · p.181 |
| 결정 4 뒤 §3 절대 대조점? | **아니오** — 입경 미보고 · 기공 미측정 · 재료 (LPSI 유리 · LTO · 카본블랙) 다름 · 펠릿 기준의 압밀 이력이 복합체와 다름.  쓰임은 정의 사례 · τ_e↔conventional 실측 · 추세 (§8-1) | §8-1 |
| springback | **원문은 다루지 않는다.**  압밀 4 t/cm² (≈ 392 MPa, 파생) → 측정 2 t/cm² (Type-A) / 마지막 1 t/cm² (Type-B · C, 측정 중 유지 미기재).  두께는 **측정 뒤 수지 단면 (ex situ)** | SI p.1–2 · p.178 |

## 1. 한 줄 요약
**Li₄Ti₅O₁₂ (LTO) + Li₇P₂S₈I 유리 (LPSI) + 카본블랙 (Super C65)** 복합 전극에서 SE 부피분율 ε 를 0.30–0.66 으로 바꾸며, 세 가지 대칭셀 임피던스로 이온 수송 저항 R_ion 을 재서
**유효 이온전도도 σ_ion,eff = d/(R_ion·A)** 와 **유효 tortuosity τ_eff = ε·σ₀/σ_ion,eff** 를 뽑은 논문이다.  방법은 (i) 전극 | SE | 전극 셀의 **비패러데이 전송선 모델 (TLM)**,
(ii) Li | SE | 전극 | SE | Li 셀의 **전자 차단 Li⁺ 전류 (DC 극한)**, (iii) 같은 전극에서 둘 다 하는 셀이다.  ε ≥ 0.4 에서 두 방법이 같은 τ_eff 를 주고 (ε 0.66 에서 1.6–2.1),
ε 0.3 에서는 TLM 이 거의 한 자릿수 높게 나온다 (원문은 TLM 의 균일 경로 가정을 의심하고 DC 값을 신뢰).  τ_eff(ε) 의 Bruggeman 지수는 **5.6–5.7** 로 액체 전극보다 훨씬 커서
"SE 분율이 줄면 협착 (constrictivity) 이 급증한다" 고 해석한다.  우리에게는 **펠릿 기준 τ² 관례의 두 번째 원문 사례**이자 **ASSB 에서 τ_e 계열 (TLM) 과 관통형 (DC) 을 맞댄 실측**이다 —
재료 (유리 LPSI · LTO · 카본) · 입경 미보고 · 기공 미측정 때문에 우리 T 의 절대 대조점은 못 된다.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **N. Kaiser** (교신), S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato, **B. Roling** — Philipps-Universität Marburg (화학과; Kaiser · Spannenberger · Schmitt · Cronau · Roling) · Toyota Motor Europe, Advanced Technology 1 Division (Kato) | **J. Power Sources 396 (2018) 175–181** | **10.1016/j.jpowsour.2018.05.095** | SE **Li₇P₂S₈I 유리** (자체 볼밀 합성) · AM **Li₄Ti₅O₁₂** (Süd Chemie, 0 % SOC) · 도전재 **Super C65** (TIMCAL) — 바인더 없음 | **실험** (대칭셀 EIS · TLM 적합 · Warburg-short 적합) — 시뮬레이션 없음 |

- 접수 2018-01-11 · 수정본 2018-04-23 · 승인 2018-05-31 · 온라인 2018-06-14 (p.175).  © 2018 Elsevier B.V. — 오픈 액세스 표기 없음.
- 사사 (p.181): Toyota Motor Corporation 재정 지원 · Rockwood Lithium (Li 분말 제공) · Jochen Mogk (SE · Super C65 밀도 측정).
- 키워드: All solid state battery · Ion transport · Transmission line model · Electrochemical impedance spectroscopy.
- Highlights (p.175): 복합 전극의 이온 수송 한계 · 임피던스로 tortuosity 결정 · 저항은 TLM 또는 Li⁺ 전류로 계산 · 고체 전지 출력밀도는 액체 전지 이상이어야 한다.
- 공저자 M. Cronau = 우리 σ₀ 3.0 mS/cm 의 출처 Cronau 2021 (원장 `CL-91`) 과 같은 그룹 — 이 논문의 σ₀ 는 다른 재료 (LPSI) 의 값이다.
- 같은 그룹 같은 권: Hlushkou et al., J. Power Sources 396, 363 (2018) (메모 v2 §8-1 순위 6) — **이 논문의 참고문헌 목록에는 없다** (21 개 전수 확인).  내용 관계 [미확인].

## 3. 핵심 수치 (★ 전부 원문 쪽 · 표지 병기)

### 3-1. 재료 · σ₀ · 조성

| 항목 | 값 | 조건 | 표지 · 쪽 |
|---|---|---|---|
| LPSI σ_ion,electrolyte,25°C | **(0.75 ± 0.1) mS/cm** | 6 mm 펠릿 · **276 MPa · 30 min · RT** · 양면 Au 스퍼터 · 자작 기밀 2-전극 셀 · Alpha-AK 1 MHz–0.1 Hz · 10 mV_RMS · −120–160 °C (±1 °C) | stated · p.178 |
| 배치별 σ₀ (그 배치의 τ 계산에 사용) | **0.68** (Fig. 4 · 5, Type-A 두께 시리즈) · **0.81** (Fig. 6, Type-B) · **0.78** (Fig. 7, Type-C) mS/cm | 25 °C | stated (캡션) · p.179–180 |
| σ₀ 측정 시 압력 | **미기재** [미확인] | — | — |
| 밀도 | LTO 3.5 · SE 2.2 · Super C65 1.9 g/cm³ | 표 값 (Mogk 측정 — 사사) | stated · SI p.2–3 |
| 카본 분율 | 본문 "approx. 13–14 vol%" · 표 12.5–14.6 vol% | 거의 고정 | stated · p.178 · SI |
| 입경 (LTO · LPSI · C65) | **보고 없음** | 본문 · SI 전수 확인 | [미확인] |
| 기공률 | **보고 없음** — FIB-SEM 에서 "densely packed", 상 구분 불가 | ε = 0.665 시료 | stated (정성) · SI p.4 |

조성표 (SI Table S1–S4, stated):

| 표 | ε (표 제목) | LTO wt% / vol% | SE wt% / vol% | C65 wt% / vol% |
|---|---|---|---|---|
| S1 | **0.665** | 30.1 / 21.0 | 60.1 / 66.5 | 9.7 / 12.5 |
| S2 | **0.493** | 48.9 / 36.8 | 41.1 / 49.3 | 10.0 / 13.9 |
| S3 | **0.398** | 59.1 / 46.7 | 31.6 / 39.8 | 9.2 / 13.5 |
| S4 | **0.297** | 67.7 / 55.8 | 22.6 / 29.7 | 9.6 / 14.6 |

- vol% 는 **wt%/ρ 를 정규화한 값**이다 (파생 검산: S1 → 8.60 · 27.32 · 5.11 → 21.0 · 66.6 · 12.5 %, 표와 0.1 %p 안).  ⇒ ε 는 **기공 0 가정**이고 실제 압분체의 SE 부피분율 (기공 포함 전체 기준) 보다 크거나 같다.
- 본문 서술 *"volume fraction of the solid electrolyte, ε, is varied between 0.3 and 0.66"* (p.176).

### 3-2. Type-A (TLM, 전극 | SE | 전극, ε 0.665) — 두께 시리즈

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 두 전극 두께 합 d_composites | **263 · 337 · 512 µm** | stated (Fig. 4 범례) · p.179 |
| R_ion (두 전극 합) | ≈ 125 · ≈ 192 · ≈ 330 Ω — "linear fashion" | 판독 (Fig. 5) · p.178–179 |
| **τ_eff 평균** | **1.8 ± 0.1** (Eq. 2) | stated · p.178 |
| Bruggeman 기대값 (구) | **1.2** | stated · p.178 (파생 0.665^−0.5 = 1.23) |
| 점별 τ (파생) | 1.6 · 1.9 · 2.2 (평균 1.9) — 판독 R · A = π(0.49 cm)² · σ₀ 0.68 · ε 0.665 | 파생 |
| 기울기 기반 τ (파생) | ≈ 2.8 — 판독 3 점 직선 기울기 ≈ 0.82 Ω/µm · 절편 ≈ −87 Ω | 파생 (§10) |
| 고주파 기울기 | **43°** (이상 TLM 45°) | stated · p.178 |
| 층간 계면 저항 | 조립 뒤 24 h 동안 "not detectable" | stated · p.178 |

### 3-3. Type-B (전자 차단 Li⁺ 전류, Li | SE | 전극 | SE | Li, ε 0.66)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 전극 두께 (평균) | **393 µm** | stated (Fig. 6 캡션) · p.179 |
| R_ion (Eq. 12 적합) | **154 Ω** | stated · p.178 |
| **τ_eff** | **1.6 ± 0.1** | stated · p.178 |
| σ_eff · f (파생) | 0.338 mS/cm · f = σ_eff/σ₀ = 0.418 (σ₀ 0.81) | 파생 |
| 주파수 범위 | 0.5 MHz – 70 mHz | stated (Fig. 6 캡션) |
| 전자 저항 R_e⁻ (ε 0.66, 231 µm, 스테인리스 사이, **4 t/cm² 고정**) | **< 1 Ω** — 고주파 극한이 R_electrolyte 와 같다는 조건 (Eq. 10) 충족 | stated · p.178 · SI p.3 (Fig. S1) |
| σ_e,eff 하한 (파생) | R_e⁻ < 1 Ω → **> 0.031 S/cm**; Fig. S1 저주파 고원 ≈ 0.28 Ω (판독, 배선 포함) 이면 > 0.11 S/cm | 파생 |

### 3-4. Type-C (같은 전극에 두 방법, ε 0.66, 두 전극 합 780 µm, σ₀ 0.78)

| 방법 | R_ion | τ_eff | 표지 · 쪽 |
|---|---|---|---|
| TLM (Type-A 단계에서) | **409 Ω** | **2.0 ± 0.1** | stated · p.178 |
| Li⁺ 전류 (SE · Li 추가 뒤) | **420 Ω** | **2.1 ± 0.1** | stated · p.178–179 |
| 재계산 (파생) | — | 2.04 · 2.09 (A = π(0.49 cm)²) — 원문 값과 1 % 안 | 파생 |
| 원문 판정 | *"both measurements yield virtually identical effective tortuosities"* | | stated · p.179 |

### 3-5. ε 스윕 — τ_eff (Fig. 8A, log–log) · Bruggeman 지수

| ε (SI 표) | log ε | TLM τ_eff (판독) | Li⁺ τ_eff (판독) | TLM / Li⁺ (파생) | ε^−0.5 (파생) | Li⁺ ÷ Bruggeman (파생) | f = ε/τ (Li⁺, 파생) |
|---|---|---|---|---|---|---|---|
| 0.665 | −0.18 | ≈ 1.8 (stated 1.8) | ≈ 1.55 (stated 1.6) | ≈ 1.2 | 1.23 | ≈ 1.3 | ≈ 0.43 |
| 0.493 | −0.31 | ≈ 8.5 | ≈ 10 | ≈ 0.8 | 1.42 | ≈ 7 | ≈ 0.05 |
| 0.398 | −0.40 | ≈ 33 | ≈ 26 | ≈ 1.3 | 1.58 | ≈ 17 | ≈ 0.015 |
| (≈ 0.36) | −0.44 | 검은 **원** 1 점 ≈ 50 — 범례에 없는 표지 · 캡션 설명 없음 · SI 조성표에 해당 ε 없음 | — | — | — | — | — |
| 0.297 | −0.53 | ≈ 2.2×10³ | ≈ 3.3×10² | ≈ 6.8 | 1.84 | ≈ 180 (TLM ≈ 1200) | ≈ 0.0009 |

- **원문 (stated)**: ε ≥ 0.4 에서 *"the tortuosity vs. volume fraction data follow the Bruggeman relation with an exponent of α = 5.7 for the TLM-based measurements and α = 5.6 for the measurements under electron-blocking conditions"* (p.180) · 맞춤 범위 ε = 0.4–0.66 (Fig. 8 캡션) · *"Both values are much higher than the value of α = 0.5 for an ideal pore structure between spherical particles"* (p.180).
- 판독 맞춤 (파생, ε ≥ 0.4 세 점): 기울기 −5.6 (두 방법) · 절편 ≈ −0.76 → **τ_eff ≈ 0.17·ε^−5.6**.  전인자 없는 Eq. 3 (τ = ε^−α, α 5.6) 이면 τ(0.665) ≈ 10 이 되어 실측 1.6–1.8 과 맞지 않는다.
- ε 0.3 에서 두 방법의 차: *"the TLM-based method yields a tortuosity value, which is almost one order of magnitude higher"* (p.179).  원문 해석: TLM 은 균일 이온 경로를 가정하는데 이는 AM 분율이 높을 때 *"highly questionable"* → 전자 차단 값이 *"more reliable"* (p.179–180).
- 국소 기울기 d ln τ/dε (Li⁺ 판독 점 사이, 파생): 0.665→0.493 **−11** · 0.493→0.398 **−10** · 0.398→0.297 **−25** /ε.

### 3-6. ε 스윕 — σ_ion,eff (Fig. 8B, Li⁺ 전류에서 계산) · LGPS 투영

| ε | LPSI σ_eff (판독, S/cm) | 본문 (stated, p.180) | LGPS 투영 (판독, σ₀ 10 mS/cm · 같은 τ_eff) |
|---|---|---|---|
| 1.0 | ≈ 7.8×10⁻⁴ | 0.75 mS/cm (순수 SE) | 10⁻² (σ₀ 10 mS/cm, 캡션) |
| 0.665 | ≈ 3.4×10⁻⁴ | — | ≈ 4.3×10⁻³ |
| 0.493 | ≈ 3.8×10⁻⁵ | — | ≈ 4.8×10⁻⁴ |
| 0.398 | ≈ 1.2×10⁻⁵ | **1.2·10⁻⁵ S/cm (ε 0.4)** | ≈ 1.5×10⁻⁴ |
| 0.297 | ≈ 7×10⁻⁷ | "about 10⁻⁶ S cm⁻¹ for ε = 0.3" | ≈ 9×10⁻⁶ |

- 기준선 (점선) 10⁻⁴ S/cm 의 근거 (p.180, stated): 액체 전해질 σ ≈ 10 mS/cm × 음이온 차단 시 Li⁺ 운반율 0.06 [19] = **0.6 mS/cm** · 상용 LFP (ε 0.38) 의 Ender τ_eff **2.10** [12] → 복합체 유효 Li⁺ 전도도 ≈ 10⁻⁴ S/cm (파생 검산 0.6 × 0.38/2.10 = 0.109 mS/cm).
- 필요 SE σ: **5–10 mS/cm** (stated; 파생 검산 10⁻⁴ × 26/0.398 ≈ 6.6 mS/cm).  예시 재료 Li₉.₅₃Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ · Li₁₀GeP₂S₁₂ · Li₁₀SnP₂S₁₂ [2, 3, 20] (원문 표기 그대로 · p.180).  고출력 시연 [2] 은 ε ≈ 0.65 라 에너지밀도가 낮다는 지적 (p.180).
- ⚠ Fig. 8 캡션은 점선을 *"10⁻⁴ mS cm⁻¹"* 로 적는다 — 그림 축 · 본문은 10⁻⁴ **S** cm⁻¹ (캡션 단위 오식, p.180).

### 3-7. 원문 서론이 모은 문헌값 (재인용 — 원 논문과 대조 안 함, p.176)

| 문헌 | 계 | ε | τ_eff | 방법 |
|---|---|---|---|---|
| Thorat [10] | LFP · LCO (액체) | 0.57 → 0.30 | 2.5 → 3.5 | 정상 Li⁺ 전류 |
| Landesfeind [9] | LFP · 흑연 · LNMO · NMC111 (액체) | 0.7 → 0.3 | 3 → 7 | TLM 형 임피던스 (landesfeind2016 카드 §5-6 의 범위와 정합) |
| Inoue & Kawase [11] | LCO (액체) | 0.28 | 3.1 (임피던스) · 4.7 (재구성 random walk) | TLM 형 + 시뮬 |
| Ender [12] | 상용 LFP 고출력 | 0.38 | 2.1 | FIB-SEM 재구성 시뮬 |
| Siroma [13] | 비정질 Li₂S-P₂S₅ + NCM523 또는 흑연 (**ASSB**) | 0.5 → 0.3 | ≈ 3 → ≈ 10 | 임피던스 — 미지의 고주파 과정 때문에 저 ε 에서 불확도 큼 |
| Zhang [14] | LCO / LLZO (ASSB) | SE 중량비 0.25–0.75 | > 10⁶ (σ < 10⁻¹⁰ S/cm, DC 분극) | DC |

## 4. ★ 방법 — R_ion 을 재서 τ_eff 로 바꾸는 사슬

### 4-1. 정의식 (Eq. 1–3, p.176 · 렌더로 확인)

| 식 | 원문 | 뜻 · 비고 |
|---|---|---|
| Eq. 1 | σ_ion,eff = d_composite / (R_ion·A_composite) | 유효 이온전도도.  A = 전극 기하 단면 (내경 9.8 mm 다이 — 카드 재계산이 A = π(0.49 cm)² 로 원문 τ 셋을 1 % 안에서 재현) · d = 전극 두께 |
| Eq. 2 | σ_ion,eff = σ_ion,electrolyte · ε / τ_eff | **τ_eff 정의**.  σ_ion,electrolyte = *"ionic conductivity of the pure solid electrolyte"* · ε = SE 부피분율 |
| Eq. 3 | τ_eff = ε^(−α) | 경험적 Bruggeman — *"For high volume fractions of a homogeneous electrolyte filling the pore space between spherical particles, the exponent is α = 0.5 [5, 8, 9]"* |

- τ_eff 의 물리 (p.176): *"In an ideal composite electrode structure, where the ions migrate across straight pathways with uniform diameter, the effective tortuosity τ_eff is unity. However, … the ion transport pathways are longer than in the ideal case, and bottlenecks (constrictivities) exist along the pathways. This leads to effective tortuosities > 1."* → **경로 길이 + 협착을 묶은 양** (Holzer 식의 τ_geo · β 분리는 하지 않는다).
- 원문 오식: Eq. 1 바로 뒤 문장 *"… respectively. is related to the ionic conductivity of the pure solid electrolyte"* — 주어 (σ_ion,eff) 가 빠져 있다 (p.176).

### 4-2. TLM 계열 (Eq. 4–6, p.176–177) — Type-A

| 식 | 원문 | 뜻 · 비고 |
|---|---|---|
| (본문) | R_ion = d·r_ion·π·r² ÷ (A·ε) · C_dl = c_dl·2·d·A·ε ÷ r | r_ion = 단위 길이당 전해질 저항, r = **원기둥 기공 반지름** (형식 매개변수) |
| Eq. 4 | Z_composite = √(R_ion/(iωC_dl)) · coth √(R_ion·iωC_dl) | 비패러데이 TLM (Fig. 1 회로; 전하전달 저항 매우 큼 + 전자 저항 무시) |
| Eq. 5 | Z_overall = R_electrolyte + √(R_ion/((iω)^α Q_dl)) · coth √(R_ion (iω)^α Q_dl) | CPE 로 바꾼 TLM + SE 분리층 직렬 [9].  α = **CPE 지수** · Q 단위 원문 "Ωcm² s^−(1−α)" |
| Eq. 6 | Z'_overall,ω→0 = R_electrolyte + (1/3)·R_ion | 저주파 실수부 극한 [16] — Nguyen 2020 Eq. 5 와 같은 관계 |

- 차단 조건의 근거 (p.178): LTO 를 **0 % SOC (Li₄Ti₅O₁₂ 조성)** 로 써서 전하전달 저항이 크다.  저주파 용량성은 *"double layer formation at the interface between the ion conducting and the electron conducting phase"* — 어느 고체가 전자전도상인지 원문은 나누지 않는다.
- 원문 머리말 (p.177): 액체 전극은 3-전극으로 단일 전극을 잴 수 있지만 고체에선 기준전극이 어려워 **두 동일 전극의 대칭셀**을 쓴다.

### 4-3. 전자 차단 Li⁺ 전류 계열 (Eq. 7–12, p.177–178) — Type-B [10]

| 식 | 원문 | 뜻 · 비고 |
|---|---|---|
| Eq. 7 | Z_overall = R_electrolyte + Z_composite | 계면 임피던스 무시 |
| Eq. 8 | Z_composite,ω→∞ = R_ion·R_e⁻ / (R_ion + R_e⁻) | 고주파: 이온 · 전자가 복합체 안에서 **병렬** (Fig. 2A) |
| Eq. 9 | Z_overall,ω→∞ = R_electrolyte + R_ion·R_e⁻/(R_ion + R_e⁻) | |
| Eq. 10 | Z_overall,ω→∞ = R_electrolyte | R_e⁻ ≪ R_ion 이고 R_e⁻ ≪ R_electrolyte 일 때 |
| Eq. 11 | Z_overall,ω→0 = R_electrolyte + R_ion | 저주파: 전자는 SE 층에 막힘 · Li 농도 분포 형성 · Li⁺ 는 이온전도상/전자전도상 계면에 **"job-sharing"** 으로 저장 [17, 18] · *"The low-frequency current is purely ionic"* (Fig. 2B) |
| Eq. 12 | Z_overall = R_electrolyte + R_ion/(iωτ)^α · tanh[(iωτ)^α] | **Warburg-short** 형.  τ = *"time constant for establishing stationary Li concentration profiles"* · 이상 α = 0.5 — ⚠ **τ · α 기호 충돌** (tortuosity · Bruggeman 아님) |

### 4-4. 셀 3 종 · 압력 이력 (본문 p.178 · Fig. 3 · SI p.1–2)

| 셀 | 층 | 목적 | 압력 이력 (SI, stated) |
|---|---|---|---|
| **Type-A** | 스테인리스 \| 전극 \| SE \| 전극 \| 스테인리스 | TLM | SE 1 t/cm² 5 min → 전극 1 장 + 1 t/cm² 5 min → 둘째 전극 + 1 t/cm² 5 min → **전체 4 t/cm² 5 min → "the pressure was relaxed to 2 t cm⁻²"** |
| **Type-B** | Li \| SE \| 전극 \| SE \| Li | 전자 차단 Li⁺ 전류 | SE 1 t/cm² 5 min → 전극 + 1 t/cm² 5 min → SE 추가 (그 쪽은 깨끗한 다이) + 1 t/cm² 5 min → **4 t/cm² 5 min** → Li 분말 (Rockwood) 양쪽 + **1 t/cm²** |
| **Type-C** | Li \| SE \| 전극 \| SE \| 전극 \| SE \| Li | 같은 전극에 두 방법 | Type-A 를 만들어 TLM 측정 → 양쪽 SE 추가 (추가마다 1 t/cm² 5 min) → **4 t/cm² 5 min** → Li 분말 + **1 t/cm²** |

- 셀 몸통: 강옥 (corundum) 관, 내경 **9.8 mm**, 스테인리스 압출 다이 (p.178).
- 압력 환산 (파생 · t = 톤힘 가정): 1 t/cm² ≈ **98 MPa** · 2 ≈ **196** · 4 ≈ **392 MPa**.  σ₀ 펠릿 276 MPa ≈ 2.8 t/cm².
- **측정 중 하중**: Type-A 는 *"relaxed to 2 t cm⁻²"* 까지만 적혀 있다 — 측정 중 유지는 명시되지 않았다 (하중 하 측정으로 읽힌다 [판독]).  Type-B · C 는 마지막 1 t/cm² 뒤의 하중 상태가 **미기재** [미확인].
  명시된 것은 SI Fig. S1 (전자 저항) 하나뿐이다 — *"The applied pressure was fixed to 4 t/cm²"*.
- Type-C 전극은 **4 t/cm² 를 두 번** 받았다 (Type-A 조립 + SE 추가 뒤 재압밀).  TLM 은 첫 압밀 뒤, Li⁺ 전류는 둘째 압밀 뒤 값이다.

### 4-5. EIS · 두께 · 분석 (p.178)
- Autolab PGSTAT302N · 정전위 모드 · 개방회로 전위 · **500 kHz – 0.3 mHz** · 10 mV_RMS · 적합 RelaxIS (RHD Instruments).  Fig. 6 시료는 0.5 MHz – 70 mHz.
- 복합 셀의 **측정 온도는 적혀 있지 않다** [미확인] (σ₀ 는 25 °C 값).
- **두께**: *"After completion of the electrochemical measurements, the cells were embedded in a resin (Specifix 40) and were then cut into two pieces using a band saw"* → 광학현미경 (Leica DM 2700 M) 단면에서 층 두께 (p.178).  = **측정 뒤 (ex situ)** · 그때의 하중 상태 미기재.
- 밀도 확인: FIB-SEM (JEOL JIB 4601F, Au 40 mA · 60 s) 단면, ε 0.665 — *"the electrode was indeed densely packed"* · *"the different phases could not be identified in an unambiguous fashion"* (SI p.4, Fig. S2).  기공률 수치 없음.
- 사슬: Type-A = Eq. 5 적합 → R_ion (두 전극 합) · Type-B = Eq. 12 적합 → R_ion → Eq. 1 (d, A) → Eq. 2 (그 배치의 σ₀, 표의 ε) → τ_eff.  α = log τ_eff vs log ε 선형 맞춤 (ε 0.4–0.66).
- 반복 수 · ±0.1 의 근거 (적합 오차인지 반복 셀인지) 는 **적혀 있지 않다** [미확인].

### 4-6. 시뮬레이션 · 입자 처리
- **시뮬레이션 없음** (실험 논문).  입자 처리 항목은 해당 없음 — 입경 · 형상 · PSD 모두 미보고.  TLM 의 "원기둥 기공 반지름 r" (p.176) 은 등가회로의 형식 매개변수이지 측정 기하가 아니다.
- DEM 관점의 위치: 이 논문은 **강체구도 연속체도 아닌 실물** — 우리 모델과의 연결은 정의 (τ_eff ↔ tau2) 와 압밀 · 측정 조건뿐이다.

### 4-7. 기법 미니 용어집
- **TLM (transmission line model, 전송선 모델)**: 다공 전극을 "이온 레일 r_ion + 전자 레일 + 둘 사이 계면 소자" 의 사다리 회로로 보는 모형.  차단 조건이면 계면 소자 = 이중층 용량 → 고주파 45° 직선 + 저주파 수직선, 실수축 길이 R_ion/3 (Eq. 6).
- **비패러데이 (non-Faradaic) 조건**: 전하전달이 일어나지 않게 (여기선 LTO 0 % SOC) 해서 계면이 용량처럼만 응답하게 한 상태.
- **CPE (constant phase element)**: 이상 축전기 대신 Z ∝ (iω)^−α 소자 — 표면 불균일 · 분포를 흡수 (Eq. 5).
- **전자 차단 (electron-blocking) 셀**: 바깥에 SE 층을 둬 전자는 못 지나고 Li⁺ 만 지나게 한 셀.  DC 극한 저항 = R_electrolyte + R_ion (Eq. 11) — 이온이 전극을 **관통**한다.
- **Warburg-short**: 유한 길이 확산의 임피던스 — tanh 꼴 (Eq. 12).  여기서는 복합체를 혼합전도체로 보고 Li 농도 분포가 서는 시간 상수 τ.
- **job-sharing**: 이온전도상과 전자전도상의 계면에 Li⁺ 와 e⁻ 가 나뉘어 저장되는 기전 (Chen · Maier [17, 18]).
- **R_electrolyte**: 전극 밖 SE 분리층 저항 — 고주파 실축 절편, 그림에서는 빼고 그린다 (Fig. 4 · 7).
- **t/cm²**: 다이 압력 표기 (톤힘/cm²) — 1 t/cm² ≈ 98 MPa (파생).
- **eSCM / eRDM** (Nguyen 2020 분류 — 이 논문은 쓰지 않는다): eSCM = 대칭셀 차단 임피던스 → τ_e (Type-A 가 이 계열) · eRDM/관통 = 정상상태 관통 flux → conventional τ (Type-B 의 DC 극한이 이 계열).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| GA | 대칭셀 (Electrolyte \| Composite \| Electrolyte \| Composite \| Electrolyte) + TLM · Li⁺ 전류 스펙트럼 겹침 | 논문 요지 그림 |
| **1** (p.177) | 비패러데이 TLM 등가회로: 원기둥 기공 (반지름 r, 길이 d_composite) · r_ion 사슬 · c_dl · R_electrolyte | **τ_e 계열의 경계조건 그림** — 이온은 분리막 쪽에서 들어오고 전자는 집전체 쪽 레일 |
| **2** (p.177) | Li \| SE \| 전극 \| SE \| Li 에서 (A) 고주파 = R_el/2 + R_ion∥R_e⁻ + R_el/2 · (B) 저주파 = R_el/2 + R_ion + R_el/2 (전자 차단) | **관통형 (conventional) 정의의 그림** — 우리 망의 두 띠 Dirichlet 와 같은 위상 |
| **3** (p.179) | 셀 Type-A · B · C 모식 + 단면 광학현미경 (500 µm 눈금) | 층 두께를 ex situ 단면으로 잰다는 증거 |
| **4** (p.179) | Type-A 스펙트럼, d 263 · 337 · 512 µm (R_electrolyte 뺌), Eq. 5 적합, σ₀ 0.68 | 고주파 43° · 저주파 용량성 — 두께에 비례해 45° 구간이 길어진다 |
| **5** (p.179) | R_ion vs d_composites (ε 0.66) 세 점 + 직선 | 원문 "linear" — 판독 절편 ≈ −87 Ω (§10) |
| **6** (p.179) | Type-B 스펙트럼 (ε 0.66, 393 µm, σ₀ 0.81, 0.5 MHz–70 mHz) + Eq. 12 적합 | Warburg-short 원호 ≈ 154 Ω = R_ion (고주파 절편 ≈ 345 Ω = 두 SE 층, 판독) |
| **7** (p.180) | Type-C: 같은 전극의 TLM (검은 사각) vs Li⁺ 전류 (파란 원), 780 µm, σ₀ 0.78 | **409 vs 420 Ω** — 같은 시료에서 두 정의가 만나는 유일한 직접 비교 |
| **8A** (p.180) | log τ_eff vs log ε, 두 방법 + 맞춤선 (ε 0.4–0.66) | ★ 핵심 데이터 — 지수 5.6–5.7 · ε 0.3 의 갈림 · 범례 밖 검은 원 1 점 |
| **8B** (p.180) | σ_ion,eff vs ε (LPSI 실측, Li⁺ 전류) + LGPS 투영 (같은 τ_eff, σ₀ 10 mS/cm) + 10⁻⁴ S/cm 점선 | ε = 1 점 = 펠릿 σ₀ (τ ≡ 1 기준) — 펠릿 기준 관례의 그림 증거 |
| SI Fig. S1 (SI p.3) | 전극 (ε 0.66, 231 µm) 을 스테인리스 사이에서 잰 Bode 선도, **4 t/cm² 고정** | 전자 저항 < 1 Ω → r_e ≪ r_ion (TLM 간이 조건) 은 ε 0.66 에서만 확인 |
| SI Fig. S2 (SI p.4) | ε 0.665 전극 FIB-SEM 단면 (×4,500, 5 µm 눈금) | 기공 수치 없음 · 상 구분 불가 |
| SI Table S1–S4 | 네 조성의 ρ · wt% · vol% | vol% 합 100 = 기공 0 가정 |

- 크롭 후보 (메인 순서대로 · 캡션 대조): **Fig. 8** (A+B) > **Fig. 2** > **Fig. 7** > **Fig. 1** > **Fig. 5** > Fig. 3 > SI Fig. S1.

## 6. Post-processing ★
- **무엇**: 등가회로 적합 (Eq. 5 TLM-CPE · Eq. 12 Warburg-short) → R_ion · R_electrolyte 분리 → R_ion vs 두께 선형성 확인 (Fig. 5) → Eq. 1–2 로 σ_eff · τ_eff → log–log 맞춤으로 Bruggeman α (ε 0.4–0.66) →
  같은 τ_eff 로 고전도 SE (LGPS 10 mS/cm) 투영 (Fig. 8B) → 액체 LFP 음이온 차단 유효 전도도 (10⁻⁴ S/cm) 와 비교.
- **도구**: RelaxIS (RHD Instruments) · 광학현미경 단면 두께 · FIB-SEM 정성.
- **수치화 · 플롯**: 스펙트럼은 R_electrolyte 를 빼고 Nyquist (Fig. 4 · 7); τ_eff 는 log–log (Fig. 8A); σ_eff 는 반로그 (Fig. 8B).  배치마다 그 배치의 σ₀ 를 캡션에 적는다.
- **기공 회계 없음**: ε 는 질량 · 밀도 계산의 고체 기준 — 압분체 부피 (두께 × 면적) 로 기공을 셈하지 않는다.  (Minnmann 2021 은 같은 그룹이지만 기공 14 % 로 φ 를 보정했다 — 관례가 다르다.)

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 = CLAUDE.md ★★ τ 명명 규약 (1저자 비준 10-03).  'tortuosity factor' 는 τ² (`tau2`) 에만 쓴다.

| 원문 기호 (쪽) | 원문 정의식 | 원문 이름 | 정규화 (어느 부피 · 어느 단면 · 어느 σ₀) | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| **σ_ion,eff** (Eq. 1, p.176) | d / (R_ion·A) | effective ionic conductivity | 전극 전체 기하 단면 (⌀ 9.8 mm) · 전극 두께 (ex situ 단면) | σ_eff (망 `sigma_full` 의 차원값) | 같은 정규화 (전체 단면 · 관통 두께) |
| σ_ion,eff/σ_ion,electrolyte | Eq. 2 의 ε/τ_eff (이름 없음) | — | σ₀ = 순수 LPSI 펠릿 | **f** (`f_ion_<mode>`) | f = ε/τ_eff.  예: 0.418 (ε 0.66, Type-B, 파생) · ≈ 0.015 (ε 0.398, 판독·파생) |
| **τ_eff** (Eq. 2, p.176) | ε·σ_ion,electrolyte/σ_ion,eff | "effective (ion transport) tortuosity" — 경로 길이 + 협착 (p.176) | **ε = 기공 0 고체 기준 SE 분율** (카본 포함 고체) · **σ₀ = 순수 SE 펠릿** (276 MPa · 30 min, 25 °C, 배치값) | **tau2 꼴** (`tau2_ion_<mode>`) — 값의 꼴이 tortuosity factor | ⚠ (i) φ 기준: τ_eff = tau2·(ε/φ_true) = tau2/(1 − p) (p = 압분체 기공률, 미측정) (ii) 기준 상태: 펠릿 ≡ 1 → 우리 T 와 맞대려면 결정 4 의 ÷ T_pure,ours (iii) 아래 두 행처럼 방법마다 경계조건이 다르다 |
| τ_eff (Li⁺-current, Type-B · C) | R_ion = Z(ω→0) − R_electrolyte (Eq. 11; Eq. 12 적합) → Eq. 1–2 | 〃 | 관통: Li 가역 전극 두 개 · 전자 차단 · DC 극한 | **tau2 (conventional, 관통형)** = Nguyen τ = Landesfeind Eq. 5 τ = 우리 망 T 와 같은 경계조건 꼴 | 원문이 *"more reliable"* 로 고른 값 (p.180) |
| τ_eff (TLM, Type-A · C) | Eq. 5 적합 R_ion (Eq. 6: Re Z(ω→0) = R_el + R_ion/3) → Eq. 1–2 | 〃 | 편측 접근: 이온은 분리막 쪽 · 전자는 집전체 쪽 · 이중층 = SE ↔ 전자전도상 계면 | **τ_e** (Nguyen "electrode tortuosity factor", eSCM 계열) — **우리 리포에 없다** | ε ≥ 0.4 에서 관통값과 ±25 % (판독), ε 0.3 에서 ≈ 7 배 (판독, 다른 셀) |
| **α** (Eq. 3, p.176) | τ_eff = ε^(−α) | Bruggeman exponent | — | T_B = φ^(−1/2) 의 지수 (Landesfeind 관례 = T 지수) | ⚠ Tjaden · COMSOL 의 f 지수 1.5 와 다른 자리.  보고 α 5.6–5.7 은 전인자 ≈ 0.17 을 가진 국소 기울기 (판독) = Landesfeind Eq. 7 (τ = f·ε^−α) 꼴 |
| ε (p.176 · Fig. 8B 축 "electrolyte volume fraction") | wt% · 밀도 계산 | volume fraction of the solid electrolyte | 기공 0 · 카본 12.5–14.6 vol% 를 고체에 포함 | ≈ φ_SE — 단 우리 φ = 상자 기준 구합 (기공 포함 분모) → ε ≥ φ_true | 액체 문헌의 ε (= 기공 = 전해질) 과 "전해질상 분율" 이라는 뜻은 같지만 기공을 세지 않는다 |
| (√τ_eff) | 보고 없음 | — | — | **tau** (`tau_ion_<mode>`) — 파생만 | √1.6 = 1.26 · √1.8 = 1.34 · √2.1 = 1.45 (파생) |
| τ_geo | 없음 | — | — | **τ_geo** — 해당 없음 | 길이와 협착을 분리하지 않는다.  "constrictivities" 는 α 의 정성 해석 (p.180) |
| τ (Eq. 12) · α (Eq. 5 · 12) | 시간 상수 · CPE/Warburg 지수 | — | — | **기호 충돌** — tortuosity · Bruggeman 과 다른 양 | 키 · 표에 옮길 때 꼬리표 필수 |

**σ₀ 기준**: 순수 LPSI 유리 **펠릿** (6 mm, 276 MPa · 30 min · RT, 양면 Au, 25 °C) — 측정 압력 미기재 · 배치값 0.68 / 0.78 / 0.81 mS/cm (본문 0.75 ± 0.1).  복합체 (4 t/cm² ≈ 392 MPa · 5 min, 다른 셀) 와 **압밀 이력이 다르다**.
우리 망 σ₀ 3.0 mS/cm (LPSCl 펠릿값, 원장 `CL-91`) 는 망 안에서 약분되지만 (메모 v2 §3-1), 실험 τ_eff 는 **가정한 σ₀ 에 정비례**한다 — 이 논문의 배치 산포 (0.68–0.81, ±9 %) 가 τ_eff 에 그대로 들어간다.

**환산 사슬 (한 줄로)**:
```
f        = σ_eff/σ₀            = ε/τ_eff                        (Eq. 2)
τ_eff    = ε·σ₀/σ_eff          ↔ tau2 (꼴) ; tau2_true = (1 − p)·τ_eff      (p = 압분체 기공률, 이 논문에 없음)
τ_eff/T_pure,ref = 1 (펠릿)    ↔ 우리 T ÷ T_pure,ours (결정 4) 와 맞대야 같은 기준
Li⁺ 전류 τ_eff = conventional (관통) ;  TLM τ_eff = τ_e 계열 — 같은 식 · 다른 양
Bruggeman: τ_eff = ε^−0.5  ⇔  f = ε^1.5                              (구, α = 0.5 — T 지수 관례)
```

**판정**:
1. Li⁺ 전류 τ_eff 는 **우리 tau2 와 같은 꼴 · 같은 관통 경계조건**이다.  다른 것은 φ 기준 (고체 기준 ε, 기공 미상) 과 σ₀ 기준 상태 (순수 펠릿 ≡ 1) 두 가지다.
2. TLM τ_eff 는 **τ_e 계열**이라 우리 tau2 와 **다른 양**이다 — 원문이 같은 이름으로 부를 뿐이다.  우리 두 σ 솔버 (DEM 접촉망 · STEP3 복셀) 는 둘 다 관통형이라 TLM 값과 맞대지 않는다.
3. 같은 그룹이 같은 양 (ε·σ₀/σ_eff) 을 2018 년에는 *"effective tortuosity τ_eff"*, 2021 년 (Minnmann) 에는 *"tortuosity factor τ²"* 로 불렀다 ⇒ **이름이 아니라 식으로 판정**한다 (결정 15).
4. Eq. 2 는 COMSOL f_e = ε/τ_F 와 같은 꼴이다 → τ_eff 숫자가 들어갈 자리는 τ_F 칸이고 σ₀ 짝은 **펠릿값**이다 (결정 5 와 정합).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 이 브랜치에서는 값 자리표시 상태 — 우리 수치는 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` 의 유도값으로 적는다)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | 수송 절반의 **실험** (EIS τ_eff) — 기계 · 형상 · 기공 · 입경 없음 | DEM 접촉망 T (conventional) · STEP3 복셀 T (CONTACT_FREE 가지) | 이 논문은 수송 쪽만 가진다.  압밀 물리 (기공 · 형상) 는 비어 있다 |
| frame[4] | 실험 — 원칙적으로 독립 보정 앵커 후보 | 각 모델을 실험에 따로 보정 | ⛔ 재료 · 카본 · 기공 미상이라 **이 값으로 우리 모델을 맞추지 않는다** |
| SE | **Li₇P₂S₈I 유리** (비정질), σ₀ 0.75 mS/cm (펠릿) | LPSCl argyrodite (결정), 망 σ₀ 3.0 mS/cm (펠릿값) | **다른 재료 · 다른 상** — 압밀성 (접촉 형성) 이 다를 수 있다 (원문 미논의) |
| AM | **LTO** (0 % SOC), 입경 미보고 | NMC811 (bimodal), 강체구 + 연화 E_eff | 다름 |
| 도전재 | **Super C65 12.5–14.6 vol%** (이온 절연 + SE 경로 차단) | DEM 망에 탄소 없음 (STEP3 일부 VGCF) | 다름 — 우리 T 는 카본 차단이 없어 **과소** 방향 |
| 입경비 | **미보고** | r_SE/r_AM 중앙 ≈ 0.13 (메모 v2 §3-3, 53 · 61 vol% 띠) | **대조 불가** |
| 기공 | 미측정 (ε = 기공 0 고체 기준) | ε_sphere 등 명시 (예: 53 vol% 띠 중앙 15.8 %, 메모 v2 §3-3) | φ 축 위치가 (1 − p) 만큼 안 정해진다 |
| 압밀 | 4 t/cm² (≈ 392 MPa, 파생) · 5 min · RT | 300 MPa 계열 냉간 압밀 | 비슷한 범위 |
| 측정 상태 | Type-A 2 t/cm² (≈ 196 MPa, 하중 하로 읽힘) · Type-B/C 마지막 1 t/cm² (유지 미기재) · 두께 ex situ | 최대 압밀 기하 (판 고정 완화) 의 망 | springback 처리가 서로 다르다 (§8-1) |
| τ 정의 | τ_eff = ε·σ₀/σ_eff | T = φ·σ₀/σ_full (`tau2`) | **같은 꼴** — φ 기준 · 기준 상태가 다름 |
| 방법 | TLM (τ_e 계열) + DC 관통 (conventional) | 관통 하나 (τ_e 없음) | 우리는 이 논문의 Li⁺ 전류 쪽만 대응 |
| 값 (판정 없이) | τ_eff (Li⁺) 1.6 @ ε 0.665 · ≈ 10 @ 0.493 · ≈ 26 @ 0.398 · ≈ 3.3×10² @ 0.297 (고체 기준 ε) | T_H 중앙 2.65 @ φ 0.613 띠 · 3.20 @ 0.444 · 5.40 @ 0.330 · 13.5 @ 0.248 (메모 v2 §3-3 · 1세대 협착식 · 기준 상태 미보정) | **비율을 내지 않는다** — φ 기준 · 재료 · 카본 · 기준 상태가 모두 다르다.  "우리가 몇 배 낮다" 로 읽지 말 것 |
| Bruggeman 배수 | ≈ 1.3 (ε 0.665) → ≈ 7 (0.493) → ≈ 17 (0.398) → ≈ 180 (0.297, Li⁺) (판독·파생) | H 중앙 3.40 (IQR 2.54–6.71) · P 5.42 (메모 v2 §3-5) | 축은 같다 (T ÷ φ^−½) — 값 대조는 위와 같은 이유로 하지 않는다 |

- **방법 artifact 와 실제 차이의 구분**: 이 표의 어느 행도 "모델 오차 배수" 를 주지 않는다.  ① 강체구 DEM vs 실물 (형상 소성 · 유리 SE 의 흐름) ② 재료 이전 (LPSI 유리 ≠ LPSCl · LTO ≠ NMC) ③ 카본 유무 ④ φ 기준 (고체 기준 ε vs 상자 기준 구합) ⑤ 판독 vs stated — 다섯이 겹친다.
- **frame[5]** — 이 논문이 가진 반쪽 = 실험 수송 (σ_eff · τ_eff, 두 정의).  없는 반쪽 = 미세구조 (입경 · 기공 · 상 분포), 기계 (압밀 · springback), 모델.  우리 DEM 이 그 반쪽을 줄 수 있지만 재료가 달라 연결이 끊긴다.

## 8. 적용 인사이트 (내 연구에 어떻게) — 이 묶음이 닫으려는 것

### 8-1. 임피던스 → ASSB 유효 이온전도도 · tortuosity 의 두 번째 실험 경로

| 물음 | 이 논문 (쪽) | 판정 |
|---|---|---|
| 재료 (SE · AM · 입경) | SE **Li₇P₂S₈I 유리** (자체 합성, 700 rpm 약 8 h) · AM **Li₄Ti₅O₁₂** (Süd Chemie) · **Super C65** — **입경 세 성분 모두 미보고** (p.178 · SI 전수) | Minnmann (NCM622 + LPSCl, 카본 없음, SE D50 3.45 µm) 과 **다른 재료 축** |
| 조성 | ε 0.665 / 0.493 / 0.398 / 0.297 (SI Table S1–S4) · 카본 12.5–14.6 vol% | 기공 0 가정의 고체 기준 |
| 압밀 | 층마다 1 t/cm² 5 min → 전체 **4 t/cm² (≈ 392 MPa) 5 min** (SI p.1–2) · σ₀ 펠릿은 별도 **276 MPa · 30 min** (p.178) | 펠릿과 복합체의 압밀 이력이 다르다 |
| 측정 압력 | Type-A *"relaxed to 2 t cm⁻²"* (≈ 196 MPa) · Type-B · C 마지막 1 t/cm² (≈ 98 MPa) 뒤 유지 **미기재** · SI Fig. S1 전자 측정만 *"fixed to 4 t/cm²"* | 부분 하중 해제 상태 (A) / 미상 (B · C) |
| 측정 셀 — 차단 전극? TLM? | Type-A = 스테인리스 집전 대칭셀 · **비패러데이 TLM** (LTO 0 % SOC 로 차단) · Type-B = **전자 차단** Li \| SE \| 전극 \| SE \| Li · DC 극한 (Warburg-short 적합) · Type-C = 같은 전극에 둘 다 | TLM = 예 (Type-A).  두 방법은 **다른 정의** (τ_e 계열 vs conventional) |
| σ_eff 데이터 전수 | Fig. 8B 다섯 점 (판독, §3-6) + stated: 0.75 mS/cm (ε 1) · 1.2·10⁻⁵ S/cm (ε 0.4) · ≈ 10⁻⁶ S/cm (ε 0.3) + 파생: 0.338 (Type-B) · 0.253 / 0.246 (Type-C TLM / Li⁺) mS/cm (ε 0.66) | §3 |
| τ 정의 · 기호 | τ_eff = ε·σ₀/σ_eff (Eq. 2) — 이름 "effective tortuosity", 값은 tortuosity factor 꼴 | `tau2` 꼴 (§ τ 정의 대조) |
| σ₀ 기준 | **순수 SE 펠릿** (배치값을 그 배치에 사용) — Fig. 8B 의 ε = 1 점 = 펠릿 | Minnmann 과 같은 **펠릿 ≡ 1** 관례 |
| 보고된 τ 또는 τ² | τ_eff (= τ² 꼴) 만 — √ 값 · 기하 τ 없음 | — |
| **결정 4 뒤 §3 절대 대조에 넣을 수 있는가** | — | **아니오.**  ① 입경비 = 미보고 → 우리 r_SE/r_AM 축에 놓을 수 없다 ② 기공 미측정 → φ 위치가 (1 − p) 만큼 불확정 ③ 재료가 LPSI 유리 · LTO · 카본블랙 (카본은 우리 DEM 에 없다) ④ σ₀ 펠릿의 압밀 (276 MPa · 30 min) ≠ 복합체 (392 MPa · 5 min) · 측정압 미상 · 배치 산포 ±9 %.  ⇒ 쓸 수 있는 것: **정의 사례** (펠릿 기준 τ² 관례 · Eq. 2 = COMSOL 꼴) · **τ_e 계열 ↔ conventional 실측 비교** (결정 13) · **추세** (국소 log–log 기울기 −5.6, 전인자 ≈ 0.17) |
| 같은 그룹의 두 경로는 같은 축인가 | Kaiser (LTO + LPSI 유리 + 카본) vs Minnmann (NCM622 + LPSCl) | **아니다** — 아래 표 |
| springback (메모 v2 §3-8 의 **③** — 프롬프트 표기 "⑤" 는 원문 번호로 ③, ⑤ 는 "띠 끝 단락") | **원문은 다루지 않는다** — 압력 의존 · 이완 · 되튐 낱말이 본문 · SI 에 없다.  압밀 392 → 측정 196 MPa (A) / ≤ 98 MPa (B · C, 유지 미상).  두께는 측정 뒤 수지 단면 (ex situ, p.178) | 두 성분이 **반대 방향**: ① R_ion 을 부분 해제 하중에서 잼 → 최대 압밀보다 R↑ → τ↑ ② 두께를 해제 뒤 잼 → 되튐으로 d↑ → σ_eff↑ → τ↓.  크기 미상.  Type-C (409 vs 420 Ω, 2.7 %) 는 방법 차와 압력 이력 차 (2 t/cm² ↔ 4 t/cm² 재압 + 1 t/cm²) 가 **교락**되어 있어 springback 시험이 아니다 — ε 0.66 유리 SE 복합체에서 둘을 합친 효과가 수 % 안이었다는 약한 정보뿐 |

두 실험 경로 맞대기 (Kaiser Li⁺ 전류 τ_eff ↔ Minnmann SI Table S2 τ_ion² — 메모 v2 §3-3 의 Minnmann φ_SE · T; **판독 + ln 보간 · 우리 산술 · 추세 전용**):

| Minnmann φ_SE | Minnmann T | Kaiser τ_eff @ 명목 ε = φ (기공 0 그대로) | 비 Kaiser/Minnmann | Kaiser 점을 가상 기공 p = 0.14 로 옮기면 (φ = 0.86 ε, τ × 0.86) | 그 φ 의 Minnmann 보간 | 비 |
|---|---|---|---|---|---|---|
| 0.613 | 2.40 | ≈ 2.7 | ≈ 1.1 | (ε 0.665 →) φ 0.572 · τ ≈ 1.3 | ≈ 2.8 | ≈ 0.5 |
| 0.536 | 3.23 | ≈ 6.4 | ≈ 2.0 | (ε 0.493 →) φ 0.424 · τ ≈ 8.8 | ≈ 5.3 | ≈ 1.7 |
| 0.444 | 4.27 | ≈ 17 | ≈ 3.9 | (ε 0.398 →) φ 0.342 · τ ≈ 23 | ≈ 13 | ≈ 1.7 |
| 0.330 | 15.3 | ≈ 1.5×10² | ≈ 9.5 | (ε 0.297 →) φ 0.255 · τ ≈ 2.8×10² | ≈ 1.1×10² | ≈ 2.7 |

- p = 0.14 는 **Minnmann 의 평균 기공을 빌린 가정**이다 (Kaiser 실측 아님).  기공 가정 하나가 비를 **×1.1–9.5 ↔ ×0.5–2.7** 로 흔든다 ⇒ Kaiser 는 기공 미측정 때문에 φ 축 절대 위치가 안 정해지고,
  두 "실험 경로" 는 같은 축의 반복 측정이 아니라 **재료 · 카본 · φ 관례가 다른 두 계**다.  같은 그룹의 실험끼리도 같은 명목 SE 분율에서 τ² 가 수 배 갈린다 — 메모 v2 결론 ④ ("SE 적은 쪽 = 다른 미세구조의 비교") 와 같은 방향의 실험 쪽 증거.
- 국소 기울기 비교 (파생): Kaiser d ln τ/dε ≈ −11 (ε 0.665→0.493) · −10 (0.493→0.398) · −25 (0.398→0.297) ↔ Minnmann −3.9 → −3.0 → −11 → −26 (메모 v2 §3-8 ②) — Kaiser 는 SE 많은 쪽에서 이미 가파르다.

### 8-2. 결정별 인사이트 (메모 v2 §0-2 결정 번호)
- ① **결정 13 (τ_e)** — 이 논문은 **ASSB (황화물) 에서 τ_e 계열 (TLM) 과 conventional (DC 관통) 을 맞댄 실측**이다: ε ≥ 0.4 에서 ±25 % (판독; 같은 전극 ε 0.66 은 2.0 vs 2.1), ε 0.3 에서 TLM 이 ≈ 7 배 (판독, 셀이 다를 수 있음).
  원문은 DC 값을 신뢰 (TLM 균일 가정 의심, p.179–180), Nguyen 2020 은 P2D 에 τ_e 를 권한다 — **목적이 다르다** (유효 전도도 vs P2D 매개변수).  ⇒ 권고 **불변** (P2D 열 보류 · "부호 불정").
  한정어 보강 제안: *"ASSB 실측 1 사례에서 두 정의는 잘 퍼콜된 조성 (ε ≥ 0.4, 고체 기준) 에서 만나고 문턱 근처 (ε 0.3) 에서 TLM 쪽으로 한 자릿수 가까이 갈렸다"*.
- ② **결정 4 (순수 SE 게이트)** — 이 논문도 **펠릿 ≡ τ 1** 관례다 (Fig. 8B ε = 1 점) → 정규화 방향은 Minnmann 과 같다.  그러나 펠릿의 압밀 (276 MPa · 30 min) · 측정 셀 · 측정압이 복합체와 달라,
  실험 쪽 기준 상태도 "같은 압밀 이력의 순수 SE" 가 아니다 (우리 DEM 순수 SE 침대는 같은 압밀을 받는다).  펠릿 정규화는 순수 SE 의 접촉 상태를 1 로 둘 뿐이고, 복합체 안 SE 의 다른 압밀 상태 (AM 하중 차폐 — 우리 DEM 지식, 원문에 없음) 는 τ 안에 남는다.
  ⇒ 권고 **불변**.  보강 제안: σ₀ 메타 (`ion_sigma0_mScm` · `ion_sigma0_T_C`) 옆에 **기준 시료의 압밀 · 측정 상태**를 적는다 (실험 대조값마다).
- ③ **결정 15 · 5 (이름 · COMSOL)** — 같은 Roling 그룹이 같은 양을 2018 "effective tortuosity τ_eff" → 2021 "tortuosity factor τ²" 로 바꿔 불렀다 → 식으로 판정하는 원칙 재확인.  Eq. 2 = COMSOL f_e = ε/τ_F 꼴 → τ_eff 숫자는 τ_F 칸, σ₀ 짝은 펠릿 (§ τ 정의 대조 판정 4).  권고 **불변**.
- ④ **결정 11 (CF · 협착 비)** — 원문의 "constrictivity" 는 α 의 **정성 해석**이다 (경로 길이와 협착을 나눈 수치 없음) → FULL/CF 이름표 결정의 근거가 못 된다.  불변.
- ⑤ (LGPS 투영의 전제) — Fig. 8B 주황 점은 **같은 τ_eff 를 다른 SE 로 옮긴** 투영이다.  τ_eff 안에는 SE–SE 접촉 (재료의 압밀성) 이 들어 있으므로 SE 를 바꾸면 τ 도 바뀔 수 있다 (원문 미논의).  우리 망에서 접촉 면적이 E · H 에 걸리는 것과 같은 논리 — **τ 는 재료 무관 미세구조 상수가 아니다**.

## 9. 인용 가능 문장 (deck/paper용)
- "Kaiser et al. defined an effective ion-transport tortuosity τ_eff = ε·σ_SE/σ_eff (their Eq. 2) — numerically a tortuosity-factor (τ²-type) quantity referenced to the conductivity of a pure solid-electrolyte pellet, with ε the porosity-free, solid-basis volume fraction of the electrolyte (J. Power Sources 396 (2018) 175)."
- "On the same Li₄Ti₅O₁₂/Li₇P₂S₈I-glass/carbon-black electrode (ε = 0.66), the transmission-line and the electron-blocking DC methods gave τ_eff = 2.0 ± 0.1 and 2.1 ± 0.1, respectively; at ε = 0.3 the transmission-line value was almost an order of magnitude higher."
- "The reported Bruggeman exponents of 5.6–5.7 (ε = 0.4–0.66) are local log–log slopes of fits that do not pass through τ_eff = 1 at ε = 1; they should not be inserted into the prefactor-free relation τ = ε^−α."
- "Because ε was computed from weight fractions and densities without a porosity correction, and no particle sizes were reported, these values constrain the definition and the trend of τ_eff but cannot serve as an absolute benchmark for a particle-resolved model."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **재료 전이**: SE = **Li₇P₂S₈I 유리** (0.75 mS/cm) ≠ 우리 LPSCl argyrodite · AM = **LTO** ≠ NMC811 · **카본블랙 12.5–14.6 vol%** (우리 DEM 망에 없음).  수치를 우리 계로 옮기지 않는다.
- ⚠ **입경 미보고 · 기공 미측정** — ε 는 고체 기준 (기공 0).  τ_eff 를 상자 기준 φ 로 다시 쓰면 (1 − p) 배 작아지는데 p 를 모른다.
- ⚠ **σ₀ 기준 상태** — 펠릿 (276 MPa · 30 min · 별도 셀 · 측정압 미기재) ≠ 복합체 (392 MPa · 5 min).  배치 산포 0.68–0.81 mS/cm (±9 %) 가 τ_eff 에 비례로 들어간다.
- ⚠ **α 5.6–5.7 은 국소 기울기** — Fig. 8A 맞춤선은 τ_eff = 1 @ ε = 1 을 지나지 않는다 (판독 전인자 ≈ 0.17).  원문 Eq. 3 (전인자 없음) 에 α 5.7 을 넣으면 τ(0.665) ≈ 10 이 되어 실측 1.6–1.8 과 어긋난다.  "Bruggeman 지수 5.7" 을 단독으로 옮겨 쓰지 말 것.
- ⚠ **Fig. 5 의 선형성** — 판독 점별 τ 가 두께와 함께 1.6 → 1.9 → 2.2 로 오르고 맞춤 직선 절편 ≈ −87 Ω (판독) → 기울기로 정하면 τ ≈ 2.8 (파생).  원문은 "linear" 와 평균 1.8 ± 0.1 만 적고 절편을 논하지 않는다.
- ⚠ **Fig. 8A 의 범례 밖 점** — log ε ≈ −0.44 (ε ≈ 0.36) 의 검은 원 (τ ≈ 50, 판독).  캡션 설명 · SI 조성표 모두 없다.
- ⚠ **ε 0.66 외의 TLM ↔ DC 비교는 같은 전극인지 원문에 없다** (Type-C 는 ε 0.66 하나) → ε 0.3 의 ≈ 7 배에는 셀 간 편차가 섞일 수 있다.
- ⚠ ±0.1 의 근거 · 조성당 셀 수 · 복합 셀 측정 온도가 **미기재**.
- ⚠ 두께는 측정 뒤 ex situ 단면 — 하중 하 두께가 아니다 (springback 성분, §8-1).
- ⚠ **LGPS 투영 (Fig. 8B)** 은 같은 τ_eff 를 가정한 척도 계산이다 — 측정 아님.  "액체 LIB 이상의 출력밀도" 결론은 전도도 척도 논증 (t⁺ 0.06 [19] · Ender τ 2.10 [12]) 이지 셀 시험이 아니다.
- ⚠ 원문 표기 오류 (그대로 두고 표지만): "Li4T5O12" (p.176, = Li₄Ti₅O₁₂) · Eq. 1 뒤 주어 누락 (p.176) · Fig. 8 캡션 점선 단위 "10⁻⁴ mS cm⁻¹" (그림 · 본문은 S cm⁻¹, p.180) · "higly" (p.180) · SI 절 제목 "Electrode Compostions" (SI p.2).
- ⚠ 시뮬레이션 없음 — DEM · MPM 어느 쪽의 검증도 아니다 (frame[4]: 실험 쪽 앵커 후보일 뿐, 이 계에서는 연결 조건 미충족).

### 10-1. 메모 v2 정정 후보 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`)
1. **§8-1 순위 8** — *"[25] … 임피던스 → ASSB 유효 이온전도도 · tortuosity 선행 — 같은 축의 두 번째 실험 경로 | §3 절대 대조 (게이트 뒤)"*.
   원문으로는 **절대 대조점이 될 수 없다** (입경 미보고 — p.178 · SI 전수; 기공 미측정 — SI p.4; ε 기공 0 기준 — SI p.2–3; 재료 LPSI 유리 + LTO + 카본블랙 — p.178).  측정 축 (EIS τ) 은 같지만 **재료 축이 다르다**.
   → 닫는 항목을 *"결정 13 (TLM ↔ DC 실측 비교, p.178–180) · 결정 4 (펠릿 ≡ 1 관례의 두 번째 원문 사례, p.178 · Fig. 8B)"* 로 바꾸는 것을 제안.
2. **§3-8 ③ (springback)** — *"springback 은 실험 T 를 올린다 (우리가 낮게 보이는 방향)"* 는 **두께를 하중 하에서 잴 때만** 단방향이다.  두께를 하중 해제 뒤 재면 (Kaiser p.178 — 측정 뒤 수지 단면) 되튐의 d 증가가 τ 를 **낮추는** 반대 성분이 된다.
   → *"부호는 R 측정 하중과 두께 측정 상태에 따라 갈린다"* 로 정밀화 제안.  Minnmann 의 두께 측정 상태는 [미확인] (minnmann 카드 §0 — 재압 뒤 두께 재측정 여부 미확인).
3. (보강 · 정정 아님) **§1 τ_e 행 · §7** 의 *"Minnmann (전자 차단 + 양단 Li-In → 관통형) [판독]"* — 같은 그룹의 이 논문이 그 배치 (Li \| SE \| 전극 \| SE \| Li) 의 저주파 극한을 **Z = R_electrolyte + R_ion** (Eq. 11, p.177) 으로 유도한다 → 관통형 판독의 이론 근거 (Li ↔ Li-In 차이는 남는다).
4. (보강) **§1 명명 표**에 이 논문 열을 더할 수 있다: "effective tortuosity" τ_eff = T 꼴 (Eq. 2, p.176) · Bruggeman α 0.5 = T 지수 (Eq. 3, p.176, Landesfeind 관례와 같음).
5. (보강) **§3-5 Bruggeman 배수** 문헌 칸에 ASSB 실측 하나: ≈ 1.3–1.5 (ε 0.665) → ≈ 17–21 (0.398) → ≈ 180 (Li⁺) / ≈ 1200 (TLM) (0.297) — 판독·파생 · 고체 기준 ε · 카본 포함 계.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|
| [13] Z. Siroma, T. Sato, T. Takeuchi, R. Nagai, A. Ota, T. Ioroi, AC impedance analysis of ionic and electronic conductivities in electrode mixture layers for an all-solid-state lithium-ion battery, J. Power Sources 316 (2016) 215–223. | 황화물 ASSB 전극의 임피던스 τ (ε 0.5 → 0.3 에서 ≈ 3 → ≈ 10) — 이 논문 이전의 유일한 같은 축 자료.  ⚠ 메모 v2 §8-1 순위 7 (Siroma, Electrochim. Acta 160, 313 (2015)) 과 **다른 논문** | 없음 |
| [16] N. Ogihara, Y. Itou, T. Sasaki, Y. Takeuchi, Impedance spectroscopy characterization of porous electrodes under different electrode thickness using a symmetric cell for high-performance lithium-ion batteries, J. Phys. Chem. C 119 (2015) 4612–4619. | Eq. 6 (R_ion/3) 와 TLM 회로의 출처 — τ_e 계열 측정의 원전 | 없음 |
| [11] G. Inoue, M. Kawase, Numerical and experimental evaluation of the relationship between porous electrode structure and effective conductivity of ions and electrons in lithium-ion batteries, J. Power Sources 342 (2017) 476–488. | 같은 전극에서 임피던스 τ 3.1 ↔ 재구성 시뮬 4.7 — 측정 ↔ 미세구조 계산의 차 | 없음 |
| [14] L. Zhang, X. Zhan, Y.T. Cheng, M. Shirpour, Charge transport in electronic-ionic composites, J. Phys. Chem. Lett. 8 (2017) 5385–5389. | 산화물 SE 복합체 τ > 10⁶ — 접촉 지배 극단 | 없음 |
| [17] C.-C. Chen, L. Fu, J. Maier, Synergistic, ultrafast mass storage and removal in artificial mixed conductors, Nature 536 (2016) 159–164. | 저주파 job-sharing 저장 (Eq. 11 의 해석) | 없음 |
| [19] F. Wohde, M. Balabajew, B. Roling, Li+ transference numbers in liquid electrolytes obtained by very-low-frequency impedance spectroscopy at variable electrode distances, J. Electrochem. Soc. 163 (2016) A714–A721. | 액체 비교 기준 (t⁺ 0.06) 의 출처 | 없음 |
| [10] I.V. Thorat, D.E. Stephenson, N.A. Zacharias, K. Zaghib, J.N. Harb, D.R. Wheeler, Quantifying tortuosity in porous Li-ion battery materials, J. Power Sources 188 (2009) 592–600. | Type-B (정상 Li⁺ 전류) 방법의 원조 [10] — 메모 v2 §8-2 에도 있음 | 없음 |
| [12] M. Ender, J. Joos, T. Carraro, E. Ivers-Tiffée, Quantitative characterization of LiFePO4 cathodes reconstructed by FIB/SEM tomography, J. Electrochem. Soc. 159 (2012) A972–A980. | 10⁻⁴ S/cm 기준선의 τ 2.10 출처 — 메모 v2 §8-2 (landesfeind [34]) 와 같은 논문 | 없음 |
| [9] J. Landesfeind, J. Hattendorff, A. Ehrl, W.A. Wall, H.A. Gasteiger, Tortuosity determination of battery electrodes and separators by impedance spectroscopy, J. Electrochem. Soc. 163 (2016) A1373–A1387. | 액체 차단 대칭셀 TLM · Bruggeman α 관례 | ✅ `landesfeind2016_tortuosity_eis_electrodes_separators` |
| [21] K.H. Park, D.Y. Oh, Y.E. Choi, Y.J. Nam, L. Han, J.-Y. Kim, H. Xin, F. Lin, S.M. Oh, Y.S. Jung, Solution-processable glass LiI-Li4 SnS4 superionic conductors for all-solid-state Li-Ion batteries, Adv. Mater. 28 (2016) 1874–1883. | 원문이 저 ε 협착을 줄일 방법으로 든 AM 의 SE 코팅 | 없음 |
| [2] Y. Kato, S. Hori, T. Saito, K. Suzuki, M. Hirayama, A. Mitsui, M. Yonemura, H. Iba, R. Kanno, High-power all-solid-state batteries using sulfide superionic conductors, Nat. Energy 1 (2016) 16030. | 고출력 ASSB 시연 (ε ≈ 0.65 — 원문의 에너지밀도 지적) | 없음 |

- 정본 카드 유무 = `litdb/papers/` 파일 목록 + 낱말 grep 으로 확인 (2026-10-03).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- 본문 7 쪽 · SI 4 쪽 전부 렌더로 읽었다 (식 1–12 · 그림 1–8 · SI Table S1–S4 · Fig. S1 · S2).
- 원문 τ 세 개를 A = π(0.49 cm)² (내경 9.8 mm) 로 재현: Type-B 1.58 (stated 1.6) · Type-C TLM 2.04 (2.0) · Li⁺ 2.09 (2.1) ⇒ Eq. 1 의 A 는 다이 전체 단면이다.
- SI 표 vol% = wt%/ρ 정규화 (기공 0) 재현.  Fig. 8B 의 ε 0.4 점 (1.2·10⁻⁵ S/cm, stated) 과 Fig. 8A Li⁺ 판독 τ ≈ 26 이 정합 (0.75·10⁻³ × 0.398/26 ≈ 1.1·10⁻⁵).
- 본문 · SI 어디에도 없는 것: 입경 · PSD · 기공률 수치 · 복합 셀 측정 온도 · 반복 수 · σ₀ 측정압 · springback/압력 의존 논의 · Hlushkou 2018 인용.

## 🔗 이 논문을 인용하는 corpus 카드
- `minnmann2021_jes_charge_transport_bottlenecks` — [25] (그 카드 참고문헌 표: 임피던스 τ 선행 · ">10 mS/cm 필요" 결론의 비교 대상).  이 논문 자신의 수치는 **5–10 mS/cm** (ε ≈ 0.4, p.180–181).
- `lee2026_lpscl_coating_thickness_ncm811` — ref 41 (대칭셀 EIS 최저주파 저항 = DC 교차검증 근거).

## 🗨️ Q&A 로그
- (아직 없음)
