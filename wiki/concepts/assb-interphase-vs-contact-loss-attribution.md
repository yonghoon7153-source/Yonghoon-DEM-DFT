---
title: "ASSB 양극의 계면층(CEI) 대 접촉 손실 — 두 비-LAM 기구를 무엇으로 가르고, 문헌은 어떻게 배정해 왔나"
description: "In sulfide ASSB composite cathodes two non-LAM mechanisms, oxidative interphase growth and chemo-mechanical contact loss, raise the cathode interface resistance and cut capacity at the same time (first charge); their source paper shows each one's existence with a dedicated channel (XPS, SEM) and assigns shares by time window, while its own SI resistance and capacitance traces let the resistance increase be classified as chemical, not area-type"
created: 2026-09-23
updated: 2026-10-02
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/truong2025_calendar-vs-cycle-aging-protocols-drt-assb.md, raw/papers/minnmann2022_designing-cathodes-cam-ssb-perspective.md, raw/papers/kim2023_argyrodite-coated-ncm-normal-pressure-assb.md, raw/papers/oruemendizabal2023_multiconfiguration-geis-drt-nmc622-lpscl-li-interfaces.md, raw/papers/koerver2017_redox-active-interphase-cutoff-voltage-ncm811-lps.md, raw/papers/zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md]
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
| ★ **집전체 쪽 층** (2026-09-28 추가, 64호) — 복합체의 집전체 면에서 SE 산화(64호 XPS 가 분해의 **주 위치**로 인쇄) | 집전체 \| 복합체 면의 **화학** — 그 면은 Li⁺ 차단 계면이라 저항으로 들어간다면 **전자 경로**(집전체 \| CAM 접촉) | `η(i)`(직렬 항) — `θ` 는 CAM 이 집전체와 전자적으로 끊길 때만 | **곱 밖의 직렬 항** — `A_eff` 도 `j₀`(CAM \| SE)도 아니다; `C` 가 저항과 다른 면에 있을 수 있다(51호 줄) |

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
| ★ **충 ↔ 방 가역 차**(같은 사이클 두 SOC, 64호) | 산화환원 계면층: 층 저항이 산화 상태를 따라 오르내린다 — `C` 불변 · `R` 비만 변함(저항형) | 가역 접촉 호흡: 충전 수축이 접촉을 줄였다 방전에 되돌린다 — `C` 가 `1/R` 을 따라감(면적형) | ✅ **전제 위** — 64호 5.0 V 저항형(τ ×2.2–2.4) · 4.6 V 면적형 쪽(τ ×1.10–1.24). ⚠ CAM 고유 `R_ct(SOC)` 가 세 번째 후보(64호 4.0 V 부호 반대) |
| ★ **깊이 XPS**(Ar⁺ 식각, 64호) | 산화종 분율이 깊이에 따라 줄고 평탄이 남는다 — **위치**(집전체 쪽 ↔ 복합체 안)의 정성 | 변화 없음 | 존재 · 위치만 — 식각 속도 미인쇄라 **두께 nm 0**, 신품 · 무전류 식각 대조가 없으면 평탄 몫이 산화인지 인공물인지 미정 |

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
| **63호 Zhang W. 2017 *ACS AMI*** (23호의 방법 원전 · 같은 연구실 LCO\|LGPS\|In · 62호 [27]) | 코팅 균열 → "local contact loss" · LGPS 산화 · 부산물 누적 — **셋 다 "may"**, 한 호(`R_MF`)에 병치(10호가 "동시 귀속" 의 원전으로 인용); 결론은 `[인쇄]` "the volume change during deintercalation increases the interfacial resistance irreversibly" 하나만 남김 | ✅ `R`·`C` **SOC 궤적**(Fig. 5 · 6, 충전 10 점) — 우리가 갈라 **앞 절반(2상 평탄) 면적형 −17 % · 뒤 절반(고전위 — 저자의 "×2") 화학형**; 코팅 쌍(표 S1 ↔ S2)도 화학 변화에 `C` 불감. ⚠ 셀 1 · α 미인쇄 |
| **64호 Koerver 2017 *JMCA*** (23호와 같은 셀 설계 · 상한 컷오프 넷 × 25 사이클 · "redox-active interphase" 원전) | 산화 계면층 하나로 SOC 의존 저항 · 감쇠 · 둘째 방전 평탄을 설명; 분해의 **주 위치는 집전체 쪽**(`[인쇄]` "predominantly in close proximity to the current collector") · CAM 쪽 "minor but steady"; 첫 사이클은 23호의 "combination" 을 "explain" 으로 받는다; 접촉 손실 · 면적 낱말 0(자기 인용 둘뿐) | ✅ `R`·`C` **사이클 축**(Fig. 4 + S7 — 원전은 `C` 해석 0) — 우리가 갈라 **노화분 저항형**(4.6 · 5.0 V) · **가역 SOC 분 4.6 V 면적형 쪽 · 5.0 V 저항형** · 4.0 V "양극 호" 는 `C` ×250–700 로 호 정체 불명. ⚠ n = 2 "representative" · 환산식 미인쇄 · 위치 미분리 |
| **84호 Orue Mendizabal 2023 *ACS Appl. Energy Mater.*** (25호 ref 23 · NMC622 \| LPSCl \| Li 금속 · 네 구성 · 2전극 GEIS → 등가회로 + DRT · 다른 연구실(CIC energiGUNE + AIT)) | 완전지 R3 증가를 `[인쇄]` "interaction products … and morphological changes" — 계면층 · 형태 변화를 **한 호에 병치**(가르지 않음) · 노화는 대칭 셀 빼기로 "exclusively" 양극 · 첫 사이클 CE 64 % 는 인용 [22,23](23호 포함)으로 CEI | ✅ `R`·`C` 세 상태 × 대칭 ↔ 완전지(그림 4b × 표 S2) — ⚠ 상태 이름표가 그림 사이에서 교차해 우리 1단계 판독이 **화학형(τ ×1.94) ↔ 면적형(τ ×0.85)** 으로 뒤집힌다 · SEM 한 시야(틈 · 균열) · Q · n · 셀 수 미인쇄 |
| **86호 Kim J.T. 2023 *J. Mater. Chem. A*** (25호 ref 17 · NCM523 \| Li₆PS₅Cl(LP2 ≈30 nm 액상 코팅 ↔ bare) \| Li₀.₅In 분말 · 2032 코인 무외압 · 셋째 연구실(KIST + 한양대)) | 코팅 쌍에 **두 기구를 한 이름("concrete contact") 아래 병치** — XPS 깊이(100 사이클): bare 산화종(Li₂Sₙ · P₂Sₓ · POₓ) ≫ 코팅 → `[인쇄]` "the solid electrolyte coating layer can provide better electrochemical stability at the interface" · SEM 공극(bare 신품부터 · 시야 하나) · Rc 이름표 "interfacial contact" 인데 "includes ionic transport" 자인 · R_bulk ×2.7–4.5 미논의 | ⚠ `R` 만(CPE 0) · 코팅 쌍 n = 1(S13 둘째 셀 산포 3–5 %) · **첫 충전 등가**(`[재현]` 202.1 ↔ 201.9 mAh g⁻¹) → 정적 접촉 차 ≈0 — 코팅 효과의 첫 사이클 몫은 화학 · 분극 쪽(전제 없이 자기 데이터 · CV 몫 · 기생 위) · 사이클 축 R 세 점(충전 상태) · GITT 피복률은 `D` 고정 |
| **90호 Truong 2025 *J. Mater. Chem. A*** (2026-10-02 사용자 공급 · NCM83 : Li₆PS₅Cl 7 : 3 \| Li₆PS₅Cl \| In/InLi · 48 h 정전위 유지 ↔ ≈48 h 1C · 시간분해 DRT(hybrid-drt) · Univ. Münster · FZ Jülich(교신 Zeier — 23 · 64호(JLU Giessen)의 공저자) · 예치 원자료) | calendar 성장을 `[인쇄]` "irreversible loss of cyclable lithium into building up resistive cathode–electrolyte interphase layer" 로 읽고 같은 문단에 "cracking or contact loss due to volume expansion from overcharging" 을 **병치** · 서두는 "the increased cathode–electrolyte interfacial resistance may also be contributed by the contact loss between them"[27](= 23호) · 이름은 한 봉우리(P_C) | ⚠ 저자 `C` 0 — 예치 DRT 로 **우리 `[재현]` C_eff**: calendar 지배 봉우리 τ ×5.7–35 · R ×4.2–27.6 동안 **C 1.6–2.5 µF 평탄 → 저항형(계면층 쪽 · 전제 위)** · cycle P_C1 R ↓ · C ↑(면적 증가형 서명 또는 상태 표류) · 사후 분석 0 · 셀 하나씩 · 유지 중 스펙트럼은 고 SOC 상태 효과 포함 |

⇒ `[해석]` **원전이 "expected · suspect · suggests" 로 쓴 접촉 손실이 인용을 거치며 평서문이 되고, 원전 자신의 SI 는 EIS 창 안에서
그 면적 변화를 보지 못한다.** 계면층 쪽은 XPS 라는 화학 증거가 있고 SI 궤적도 그쪽이다.
→ **2026-09-28 (64호)**: 같은 연구실의 네 달 뒤 편에서 **노화분**은 여전히 저항형이지만, **가역분**에서는 면적형(4.6 V)이 처음 나타난다 — 계면층 한 이름("redox-active") 아래 두 기구가 컷오프에 따라 번갈아 보인다(전제 위). 그리고 원전 XPS 가 계면층의 주 위치를 **집전체 쪽**에 두어, "계면층 = CAM \| SE 의 `j₀`" 등식 자체가 이 편에서 확인되지 않는다.
→ **2026-09-29 (84호)**: 다른 연구실 · Li 금속 완전지에서 같은 병치가 반복된다 — 한 R3 에 계면층 · 형태 변화를 함께 두고, 노화는 대칭 셀 빼기로 양극에 돌린다. `R`·`C` 입력이 대칭 ↔ 완전지 짝으로 있는데도 상태 이름표가 그림 사이에서 교차해, 같은 두 표가 "계면층" ↔ "접촉 면적" 을 번갈아 가리킨다(전제 위).
→ **2026-09-29 (86호)**: 셋째 연구실(KIST) · 코인셀 코팅 쌍에서 같은 병치가 반복된다 — "concrete contact" 한 이름 아래 XPS(계면층)와 SEM(공극)을 함께 두고, 정량은 Rc 와 GITT 피복률(둘 다 분극 채널)이다. 같은 지면의 첫 충전 등가가 정적 접촉 차를 ≈0 으로 묶어, 코팅이 막은 것은 첫 사이클 안의 화학 · 분극 몫이라는 쪽으로 읽힌다(전제 없이 · CV 몫 · 산포 위).
→ **2026-09-29 (87호 · 종설)**: 같은 연구실(23 · 64호 계열 — JLU Giessen · KIT BELLA)의 설계 종설이 **두 기구를 문장마다 같은 저항 이름으로** 부른다 — 그림 3b 캡션 접촉 손실 → "increased interface resistances" · §2.3 산화 계면층 → "increased interfacial resistance, thereby impeding charge transfer"[12,49,61] · 그림 3c 점접촉 → "limit electrode kinetics" — 그리고 크기 손잡이 하나가 면적 × 계면층 성장을 함께 움직인다고 인쇄한다([37,49]). 23호 원전(Koerver 2017 *Chem. Mater.*)은 인용 0(참고문헌 전수 grep) · 계면층 쪽은 [12] = 64호 · 계면 반응[6,9,11,12]로만 · 가르는 입력 · 제안 0 — 1차 자료 0 이라 계보 표에 행을 두지 않는다.
→ **2026-10-02 (90호)**: 같은 계열(Zeier — 23 · 64호 공저자)의 정전위 유지 노화에서 같은 병치가 반복된다 — 한 봉우리(P_C) 아래 계면층 · 균열 · 접촉 손실을 함께 두고 가르지 않는다. 저자 `C` 는 0 이지만 예치된 시간분해 DRT 에서 우리가 C_eff 를 내면 유지 48 h 동안 지배 봉우리의 `C` 가 평탄해(1.6–2.5 µF) **노화분은 저항형** — 23 · 64호(사이클 축 노화분)와 같은 방향이다(전제 위 · 고 SOC 상태 효과 미분리 · 위치 귀속은 τ 문헌 가정).

## 무엇을 재면 가를 수 있나 (처방)

1. **`R` 과 `C` 를 상태축(OCV·사이클) 위 연속으로 같이 인쇄** — 16호 처방 1단계. 23호가 계보 첫 연속 사례. ★ **2026-09-28 두 번째 = 63호** — 한 충전 안 10 점에서 구간별(면적형 ↔ 화학형) 판정이 갈린다 · 조건: CPE α 를 SOC 별로 인쇄(63호는 안 했다).
   ★ **2026-09-28 세 번째 = 64호 — 첫 사이클 축**: 같은 SOC 두 점(충 · 방)을 25 사이클 — **노화분(사이클 축)과 가역분(충 ÷ 방)을 같은 호에서 따로** 분류한다. 조건: 아래 6 · 7 먼저, CPE α 인쇄(64호도 안 했다).
2. **무전류 기계 이완 대조를 같은 셀에서** — XPS 로 화학 불변을 확인하고 `R·C` 가 보존되는지 본다(전제의 양성 대조).
3. **첫 충전 뒤 · 첫 방전 뒤 SEM(또는 단층촬영)을 같은 조건으로** — 틈이 재리튬화에서 닫히는지(23호 G7 공백).
4. **격자 `V(x)` 곡선을 같은 지면에** — `ΔR` 급등 전위창이 격자 수축 구간과 겹치는지 떨어지는지(시점 판별).
5. **코팅 유무 쌍** — 코팅은 계면층만 막고 수축은 그대로 둔다(`[추론]`). ★ **2026-09-23 첫 표본 = 24호**(70 % NMC111, LLSTO 15–20 nm ↔ 비코팅): 이봉 약화 · 충전 1 구배 성격 불변 ·
   첫 사이클 비가역 `[도표]` −14 % — **첫 사이클 손실의 대부분은 코팅으로 막히는 경로가 아니다**(23호 예산과 같은 방향). ⚠ n = 1 씩 · 코팅 행의 σ 가 표끼리 안 맞는다(24호 D17).
   ★ **2026-09-29 셋째 표본 = 86호**(NCM523 · Li₆PS₅Cl_LP2 ≈30 nm 액상 코팅 ↔ bare · 2032 코인 · 0.1C · 30 °C): 첫 사이클 비가역 `[인쇄]` ICE 61.6 → 74.1 %(`[재현]` 첫 충전 등가 202 ↔ 202 mAh g⁻¹ — 손실 38.4 → 25.9 %p · **코팅이 첫 사이클 손실의 ≈1/3 을 막는다**) · 100 사이클 68.9 → 93.7 %(사이클 손실의 대부분) · XPS 깊이에서 산화종 억제 — 24호(LLSTO · −14 %)와 다른 방향이나 코팅 재료 · 두께 · 셀 · 창이 다르다 · n = 1 씩(S13 둘째 셀 3–5 %).
6. ★ **호 정체 검사** (2026-09-28, 64호) — 같은 이름의 호("양극 호")를 셀 · 컷오프 · 온도 사이에서 비교하기 전에 `C` 자릿수와 τ 대역을 본다. 64호 4.0 V 셀의 "양극 호" `C` 0.1–0.85 mF 는 다른 셀의 ×250–700 · 음극 호 자릿수다 — 비교에서 뺀다.
   ★ **2026-10-02 시간 축 판 = 90호** — 한 셀의 봉우리가 시간에 따라 다른 이름의 τ 창으로 넘어갈 때 C_eff 연속성을 본다: 90호 calendar 봉우리는 P_A 창(τ 0.19 · 0.54 s)에 들어가도 `C` 1.6–2.5 µF 평탄(같은 요소 — 이름 유지 지지) · 같은 τ 대역 cycle P_A 는 ≈1.5–3.3 mF(다른 요소) — 우리 `[재현]`(저자 `C` 0).
7. ★ **위치** (2026-09-28, 64호) — 계면층이 CAM \| SE 에 있는지 집전체 \| 복합체 면에 있는지를 **집전체 쪽 면 · 분리막 쪽 면 · 단면**의 깊이 XPS 쌍으로 가른다. 64호는 집전체 쪽 면만 쟀다. 집전체 쪽 층은 곱 밖의 직렬 항이다(정의 표 셋째 행).
8. ★ **휴지 시간 · SOC 고정** (2026-09-28, 64호) — EIS 직후 ↔ 24 h 휴지 뒤 양극 호가 `[도표]` ×1.3–1.9 다르고, 충 ↔ 방이 ×0.2–2.5 다르다. `R(N)` 을 노화 축으로 쓰려면 둘을 고정하고 값 옆에 적는다.
   ★ **2026-10-02 (90호)** — 시간분해 EIS 를 calendar 는 유지 전위(고 SOC) · cycle 은 1C 방전 끝(30 분 휴지 · 사이클마다 표류)에서 재고, RPT 비교는 한 셀 스펙트럼을 여섯 셀 공통 기준선으로 쓴다 — 자기 셀 기준이면 cycle 저주파 Re 는 −40 · −30 · −4 Ω(`[도표·화소]` S4 · `[데이터]`). 상태 · 기준 셀을 값 옆에 적어야 하는 표본.
9. ★ **상태 이름표 대조** (2026-09-29, 84호) — `R`(그림)과 `C`(표)를 상태 이름표로 짝지어 1단계를 걸기 전에, 막대 값을 다른 그림(사이클 궤적 · 대칭 셀 궤적)의 같은 상태와 대조한다. 84호는 그림 4b '1st discharge' 가 그림 4c · 2c 의 10 사이클과 성분별 ±3 Ω·cm² 로 같고, 그 대조 여부에 따라 노화 판독이 계면층(화학형) ↔ 접촉 면적(면적형)으로 뒤집힌다.

## 이 페이지가 주장하지 않는 것

- **23호 셀에서 접촉 손실이 없었다고 주장하지 않는다.** "EIS 창(7 MHz–1 Hz) 안의 양극 저항 증가는 면적 형이 아니다(전제 위)" 까지다.
  완전 고립 입자(호에서 빠짐)·창 밖 과정·분해 뒤 생긴 틈은 판정 밖이다.
- **`C ∝ 면적` 전제가 섰다고 주장하지 않는다.** 18·19호에서 깨졌고, 23호의 양성 대조는 **두 호 중 하나**, 판 a ↔ c 크기 불일치(D10) 위다.
- **손실 예산의 ≳85 % 를 접촉 손실로 돌리지 않는다** — `η(i)`(0.25 C 에서 이미 66 mAh g⁻¹)와 상대극 고갈(무 Li 상대극, 방전 끝 `C_anode`
  두 자릿수 붕괴)이 같은 칸에 있다.
- 근거는 **실험 다섯 편**이고 그중 `R`·`C` 입력이 있는 것은 **두 편(18·23호)** 뿐이다. 24호는 `R`·`C` 대신 **코팅 쌍(화학 대조)** 을 준다 — 그 쌍은 n = 1 씩이다.
  → **2026-09-28 (63호)**: 실험 **여섯 편** · `R`·`C` 입력 **세 편(18 · 23 · 63호)** — 63호는 코팅 쌍도 준다(n = 1).
  → **2026-09-28 (64호)**: 실험 **일곱 편** · `R`·`C` 입력 **네 편(18 · 23 · 63 · 64호)** — 64호는 사이클 축이지만 컷오프당 셀 2 "representative" 이고 환산식이 없다.
  → **2026-09-29 (84호)**: 실험 **여덟 편** · `R`·`C` 입력 **다섯 편(18 · 23 · 63 · 64 · 84호)** — 84호는 대칭 ↔ 완전지 짝까지 주지만 상태 이름표 교차로 판정 보류(셀 수 미인쇄).
  → **2026-09-29 (86호)**: 실험 **아홉 편** · `R`·`C` 입력 **다섯 편 그대로**(86호는 `R` 만 · CPE 0) — 86호는 코팅 쌍(n = 1 · 산포 3–5 %)과 첫 충전 등가를 준다.
  → **2026-10-02 (90호)**: 실험 **열 편** · `R`·`C` 입력 **다섯 편 그대로**(90호는 저자 `C` 0 — 예치 DRT 로 우리가 C_eff 를 낸 첫 편) — 90호는 컷오프 다섯 × 노화 둘 · 셀 하나씩 · 사후 분석 0 이다.
- **63호 셀에서 접촉 손실이 없었다고 주장하지 않는다** (2026-09-28) — 앞 절반의 면적형 감소는 오히려 면적 쪽 서명이다; 주장은 "뒤 절반의 ×2 는 면적형이 아니다(전제 위)" 까지다.
- **64호의 가역 면적형(4.6 V)을 접촉 호흡의 측정으로 주장하지 않는다** (2026-09-28) — τ 비 1.10–1.24 는 전제 · CPE 환산 · 로그 축 판독 위다. 그리고 **집전체 쪽 층이 셀 저항에 기여하지 않는다고 하지 않는다** — Li⁺ 차단 계면이라는 물리에서 그 경로를 묻는 것까지다.
- **84호 셀의 노화를 계면층으로도 접촉 손실로도 배정하지 않는다** (2026-09-29) — 1단계 판독이 상태 이름표 해석에 따라 뒤집히고(τ ×1.94 ↔ ×0.85), Q · n 미인쇄 · 창 밖 과정 · 셀 하나씩이다. 저자도 두 기구를 한 R3 에 병치했다.
- **86호 셀의 코팅 효과를 계면층 억제로도 접촉 면적 증가로도 배정하지 않는다** (2026-09-29) — 첫 충전 등가는 정적 고립 차의 상한(CV 몫 · 기생 전하 · 산포)이고, Rc · GITT 피복률은 분극 채널이며 `C` · 대칭 셀 · 온도가 없다. 저자도 두 기구를 "concrete contact" 한 이름 아래 병치했다.
- **87호(종설)의 저항 어휘를 두 기구 중 어느 쪽의 근거로도 쓰지 않는다** (2026-09-29) — 1차 자료 0 이고, "한 이름 아래 병치" 가 설계 어휘에서도 반복된다는 표본까지다. 실험 편 수(아홉) · `R`·`C` 입력 편 수(다섯)는 그대로다.
- **90호 calendar 셀의 노화를 계면층으로 확정하지 않는다** (2026-10-02) — C_eff 평탄은 우리 판독(골–골 적분 · 창 경계 ±≈30 % · 전제 `C ∝ 면적` · 기하 면적)이고, 유지 중 스펙트럼은 고 SOC 상태 효과를 포함하며, 면적 대조 · 온도 · 3전극 · 사후 분석이 없다. 저자도 계면층 · 균열 · 접촉 손실을 한 P_C 에 병치했다.

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻. 이 페이지는 그 앞 단계(비-LAM 두 기구의 분리).
- [[assb-lampe-contact-product-degeneracy]] — `A_eff · j₀` 곱과 처방 표. 23호가 일곱 번째 적용.
- [[assb-apparent-capacity-decomposition]] — 두 기구가 `θ`·`η` 에 들어가는 자리; 23호 손실 예산.
- [[composite-cathode-percolation-utilization]] — 완전 분리(`θ`) 쪽의 기하 모델.
- [[assb-li-in-reference-potential-window]] — 23호 셀의 방전 끝을 상대극이 끊는 경로(용량 배정의 세 번째 후보).
- [[assb-tortuosity-factor-effective-conductivity-split]] — 부분 접촉 손실이 `σ_eff`·`τ²` 로 들어가는 자리(24호의 "굴곡도 진화").
