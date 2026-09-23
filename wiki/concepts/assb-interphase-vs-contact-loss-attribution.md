---
title: "ASSB 양극의 계면층(CEI) 대 접촉 손실 — 두 비-LAM 기구를 무엇으로 가르고, 문헌은 어떻게 배정해 왔나"
description: "In sulfide ASSB composite cathodes two non-LAM mechanisms, oxidative interphase growth and chemo-mechanical contact loss, raise the cathode interface resistance and cut capacity at the same time (first charge); their source paper shows each one's existence with a dedicated channel (XPS, SEM) and assigns shares by time window, while its own SI resistance and capacitance traces let the resistance increase be classified as chemical, not area-type"
created: 2026-09-23
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# ASSB 양극의 계면층 대 접촉 손실 — 가르는 관측과 배정

> `assb` 축의 개념 페이지. 닻은 [[assb-contact-loss-vs-lampe]].
> 닻 물음은 **`LAM_PE` ↔ 접촉 손실**이다. 이 페이지는 그 앞 단계 — **접촉 손실 ↔ 계면층(CEI)** — 을 다룬다.
> 둘 다 `LAM_PE` 가 아니고(물질은 남는다), 둘 다 **첫 충전에** 생기고, 둘 다 **양극 계면 저항을 올리고 용량을 줄인다.**
> 그래서 계보의 편들이 이 둘을 **한 문단에 병치**하고 가르지 않는다(22호 · 23호).
> 수치의 정본은 원문 PDF 이고, 이 페이지의 값은 **사본**이다.

## 정의 — 두 기구와 그것이 건드리는 항

| 기구 | 무엇이 변하나 | [[assb-apparent-capacity-decomposition]] 에서 | [[assb-lampe-contact-product-degeneracy]] 에서 |
|---|---|---|---|
| **계면층(CEI)** — 황화물 SE 의 산화 분해(고전위에서) | 계면의 **화학**: 이온 전도가 낮은 층이 끼어든다 | `η(i)` 를 낮춘다(분극); 층이 입자를 **완전히 덮으면** `θ` 도 낮춘다 (23호 `[인쇄]` "possibly results in partial insulation of NCM particles") | `j₀` (또는 직렬 저항) — **면적은 그대로** |
| **접촉 손실** — 탈리튬 수축(NCM 단위포 부피 감소)으로 SE 와 떨어짐 | 계면의 **면적** | 부분 분리는 `η(i)`, **완전 분리는 `θ`** | `A_eff` — **면적 인자** |

⇒ **두 기구는 같은 두 항(`η`, `θ`)에 들어가고, 곱 `A_eff · j₀` 의 서로 다른 인자에 앉는다.** OCV 적합은 둘 다 못 보고,
임피던스 한 값(`R`)은 둘 다 본다. 갈리는 것은 **`R` 과 `C` 를 같이 볼 때**다.

## 채널별 서명

| 채널 | 계면층이면 | 접촉 손실이면 | 판별력 |
|---|---|---|---|
| **XPS** (S 2p · P 2p 산화종) | 새 성분 | 변화 없음 | 존재만 — 몫 0 (표면 수 nm) |
| **사후 SEM** (틈·음각) | 변화 없음(층은 nm) | 틈 | 존재만 — **분해·감압 인공물, 원인↔결과** 문제 |
| **`R` 한 값** | ↑ | ↑ | ❌ |
| **`R` 과 `C` 의 동시 궤적** | `C` 불변, `τ = RC` ↑ | `C ∝ 1/R`, `τ` 불변 | ✅ **전제 `C ∝ 면적` 위** |
| **전위 창 시점** | SE 산화 개시 전위(23호 `[인쇄]` 3.2–3.4 V vs In) | 격자 수축이 큰 구간 | ⚠ **첫 충전에서는 SOC 와 전위가 단조 동행**해 두 시점이 겹칠 수 있다 — 격자 곡선 `V(x)` 가 같은 지면에 있어야 쓸 수 있다 |
| **가역성** | 비가역(층은 남는다) | 수축은 방전에서 되돌아옴 → 부분 가역 | ⚠ 첫 사이클 손실로 양극이 덜 리튬화되면 **수축도 비가역처럼 남는다**(23호 §4-2e) |
| **무전류 이완** | 없음 (XPS 불변) | 기계 이완으로 **면적만** 변한다 | ★ **`C ∝ 면적` 전제의 양성 대조**로 쓴다 |
| **회절 봉우리 이봉**(operando, 입자 모집단) | `[인쇄]` 24호: "reduced i₀ → increased bifurcation" — 비코팅에서 뚜렷 | 접촉이 끊긴·좁아진 입자가 뒤처져도 같은 이봉 | ⚠ 자촉매 가짜 상분리(동역학)도 같은 서명 — **코팅 쌍**이 있어야 화학 몫이 떨어진다 |
| **유효 전도도 `σ_eff`**(차단 셀 EIS ↔ operando 역적합) | 입자 표면 층은 전극 척도 `σ_eff` 를 크게 안 바꾼다(`[추론]`) | **부분** 접촉 손실(점 접촉 감소)이 `σ_eff ↓` — 원전 이름은 "굴곡도 진화"(24호) | ⚠ `ε`·압력·모델과 곱 — [[assb-tortuosity-factor-effective-conductivity-split]] |

## 원전(23호)이 한 일 — 채널 분담 + 시간 분할 배정

`raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md` (Koerver 외 2017, *Chem. Mater.* 29, 5574).

- XPS 가 계면층의 **존재**를, SEM 이 접촉 손실의 **존재**를 보인다. **몫은** 첫 사이클 = `[인쇄]` "combination",
  이후 = 계면층(`[인쇄]` SEM 1 ↔ 50 사이클 "similar" 에 기댄 소거법).
- 양극 호 `ΔR = +140 Ω` 은 본문·결론에서 계면층, **초록에서는 접촉 손실에도** 배정된다.
- ★ **SI 가 가른다(우리 조합)**: `[도표]` S2 · S7 에서 `R_SE/Cathode` 가 ×1.5–2.45 오를 때 `C_SE/Cathode` 는 ×0.96–1.05
  (면적 가설 예측 ×0.41–0.66) — **두 셀 · 다섯 구간 전부 화학 형**. 그리고 S3 무전류 이완의 한 호가 `R·C` 를 +5 % 로 보존해
  **면적 서명이 이 복합체에서 실제로 나올 수 있음**을 보인다(부분 양성 대조).
- ★ **손실 예산**(`[재현]`): 계면층의 **패러데이 몫** ≈4 %(양극 SE 기준, "≈1 % of SE") + **옴 몫** ≲3 %(방전 무릎 기울기
  ≈12 mAh g⁻¹ V⁻¹ × 25–100 mV) ⇒ **첫 사이클 손실 52 mAh g⁻¹ 의 ≳85 % 가 미배정**이고, 거기에 `θ` · `η(i)` · 상대극 고갈이 함께 있다.

## 계보의 배정 — 같은 두 기구, 다른 선택

| 편 | 두 기구의 처리 | 가르는 입력이 지면에 있었나 |
|---|---|---|
| **23호 Koerver 2017** (원전) | 채널 분담 + 시간 분할; 초록 ↔ 결론 모순 | ✅ `R`·`C` 연속 궤적(SI) — 원전은 조합 안 함 |
| **22호 Strauss 2018** | 두 기구를 한 문단에 병치, 둘 다 "kinetic" 으로 묶음 → `j₀` 끝 선택 | ❌ `impedan*` 0 |
| **18호 Fukunishi 2023** | `[인쇄]` "chemical composition **or** the contact area" — 갈림을 인쇄하고 남김; 원전을 **공간전하층**으로 인용(기구 치환) | ✅ `R`·`C` 두 상태 — 우리가 갈라 LPSI = 면적 + 화학, LPSCl = 화학 |
| **9호 Huo 2025** | 원전 **초록**의 "contact loss … increased resistance" 를 인용하고 `A_eff` 하나로 적합 | ❌ 적합 파라미터 하나 |
| **1호 Bielefeld 2019** | 원전을 "contact loss **throughout** the composite cathode" 로 강화 인용 | — (모델) |
| **24호 Stavola 2023** | 이봉은 **계면층**(`[인쇄]` "decomposition products … a higher i₀ … less bifurcation"), 수송 저하는 **접촉**(`[인쇄]` "rearrangement of particle contacts")을 기구로 대고 **이름은 `τ`** 로 — 세 번째 이름 **"굴곡도 진화"** | ⚠ **코팅 쌍**(화학 대조, 계보 첫) — 이봉의 코팅 의존분은 화학 형; 첫 사이클 비가역은 코팅으로 ≈14 % 만 줄어듦(`[도표]`, n = 1) |
| **53호 Ren · Danner 2023** (⚠ Perspective, **산화물** LLZO) | **시간 배정을 뒤집어 인용**: `[인쇄]` 첫 사이클 = "electrochemical oxidation of the interface"(인용 [56a,103]) · 이후 = "fatigue failure of the CAM/SE interface and loss of electrochemically active surface area"(**인용 0**) — 두 영역 문장의 [103] 이 23호. 같은 편 §5.2(황화물)는 23호를 원문대로("irreversible resistance increase in the first cycle"). 33호(2025)에 앞선 **첫 역전 표본**(발행 2022) | ⚠ 공정 대조만 재인용 — FAST/SPS 치밀 셀 "cracking … ruled out" → 전기화학([105]); 근거 채널 · n 0 |

⇒ `[해석]` **원전이 "expected · suspect · suggests" 로 쓴 접촉 손실이 인용을 거치며 평서문이 되고, 원전 자신의 SI 는 EIS 창 안에서
그 면적 변화를 보지 못한다.** 계면층 쪽은 XPS 라는 화학 증거가 있고 SI 궤적도 그쪽이다.

## 무엇을 재면 가를 수 있나 (처방)

1. **`R` 과 `C` 를 상태축(OCV·사이클) 위 연속으로 같이 인쇄** — 16호 처방 1단계. 23호가 계보 첫 연속 사례.
2. **무전류 기계 이완 대조를 같은 셀에서** — XPS 로 화학 불변을 확인하고 `R·C` 가 보존되는지 본다(전제의 양성 대조).
3. **첫 충전 뒤 · 첫 방전 뒤 SEM(또는 단층촬영)을 같은 조건으로** — 틈이 재리튬화에서 닫히는지(23호 G7 공백).
4. **격자 `V(x)` 곡선을 같은 지면에** — `ΔR` 급등 전위창이 격자 수축 구간과 겹치는지 떨어지는지(시점 판별).
5. **코팅 유무 쌍** — 코팅은 계면층만 막고 수축은 그대로 둔다(`[추론]`). ★ **2026-09-23 첫 표본 = 24호**(70 % NMC111, LLSTO 15–20 nm ↔ 비코팅): 이봉 약화 · 충전 1 구배 성격 불변 ·
   첫 사이클 비가역 `[도표]` −14 % — **첫 사이클 손실의 대부분은 코팅으로 막히는 경로가 아니다**(23호 예산과 같은 방향). ⚠ n = 1 씩 · 코팅 행의 σ 가 표끼리 안 맞는다(24호 D17).

## 이 페이지가 주장하지 않는 것

- **23호 셀에서 접촉 손실이 없었다고 주장하지 않는다.** "EIS 창(7 MHz–1 Hz) 안의 양극 저항 증가는 면적 형이 아니다(전제 위)" 까지다.
  완전 고립 입자(호에서 빠짐)·창 밖 과정·분해 뒤 생긴 틈은 판정 밖이다.
- **`C ∝ 면적` 전제가 섰다고 주장하지 않는다.** 18·19호에서 깨졌고, 23호의 양성 대조는 **두 호 중 하나**, 판 a ↔ c 크기 불일치(D10) 위다.
- **손실 예산의 ≳85 % 를 접촉 손실로 돌리지 않는다** — `η(i)`(0.25 C 에서 이미 66 mAh g⁻¹)와 상대극 고갈(무 Li 상대극, 방전 끝 `C_anode`
  두 자릿수 붕괴)이 같은 칸에 있다.
- 근거는 **실험 다섯 편**이고 그중 `R`·`C` 입력이 있는 것은 **두 편(18·23호)** 뿐이다. 24호는 `R`·`C` 대신 **코팅 쌍(화학 대조)** 을 준다 — 그 쌍은 n = 1 씩이다.

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻. 이 페이지는 그 앞 단계(비-LAM 두 기구의 분리).
- [[assb-lampe-contact-product-degeneracy]] — `A_eff · j₀` 곱과 처방 표. 23호가 일곱 번째 적용.
- [[assb-apparent-capacity-decomposition]] — 두 기구가 `θ`·`η` 에 들어가는 자리; 23호 손실 예산.
- [[composite-cathode-percolation-utilization]] — 완전 분리(`θ`) 쪽의 기하 모델.
- [[assb-li-in-reference-potential-window]] — 23호 셀의 방전 끝을 상대극이 끊는 경로(용량 배정의 세 번째 후보).
- [[assb-tortuosity-factor-effective-conductivity-split]] — 부분 접촉 손실이 `σ_eff`·`τ²` 로 들어가는 자리(24호의 "굴곡도 진화").
