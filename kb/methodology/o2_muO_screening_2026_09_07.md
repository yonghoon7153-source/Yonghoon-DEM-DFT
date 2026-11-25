---
title: "LPSCl + O₂ — 산소 화학퍼텐셜(μ_O) 전방향 스크리닝"
date: 2026-09-07
updated: 2026-09-07
tags: [oxidation, o2, grand-potential, convex-hull, lpscl, modelc, screening, muO]
status: 1차 결과
kind: methodology
system: lpscl
confidence: medium
verificationStatus: verified
verifiedAt: 2026-09-07
verifiedBy: "MP GGA_GGA+U hull 232상에서 get_element_profile(O) 실행 · 도구 selftest 15건"
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---

# LPSCl 이 O₂ 를 만나면 — μ_O 전방향 스크리닝

> **값의 정본**: `db/properties/o2_muO_screen_lpscl_2026_09_07.json`
> **도구**: `tools/oxidation/esw_grand_potential.py --open_element O`
> **요청 배경**: *"lpscl 이 O2 랑 만났을때 생기는 반응 관련해서 convex hull 로 전방향 스크리닝"*

---

## 1. 쉬운 설명 — 뭘 한 건가

**"LPSCl 을 산소가 조금 있는 방에 두고, 산소를 아주 조금씩 늘리면서 매 순간
*'지금 뭐로 변하는 게 제일 이득인가'* 를 물어본 것."**

가설을 안 세운다. **Li–P–S–Cl–O 조합 전부**(MP 상 232개) 중에서 제일 낮은 걸 컴퓨터가 고른다.
그래서 **"전방향"** 이다.

## 2. 원리 — 왜 "전압" 이 아니라 "산소압" 인가

우리는 원래 **ESW staircase** 를 그린다: *"전압을 올리면 전해질이 뭐로 분해되나"*.
그 도구가 최소화하는 것은 grand potential 이다:

```
Φ = E − μ_Li · N_Li        (Li 저장소를 연다 = 전압을 건다)
```

**리튬 자리에 산소를 넣으면 그대로 산소 얘기가 된다:**

```
Φ = E − μ_O · N_O          (O 저장소를 연다 = 산소압을 건다)
```

`μ_O` 는 **"산소가 얼마나 들어오고 싶어 하는가"** 다. 온도·산소압이 정한다.
`get_element_profile` 은 원래 원소를 인자로 받게 돼 있었고 **Li 가 박혀 있었을 뿐**이라,
새 도구 없이 **플래그 하나**로 열었다.

### ⚠ 부호의 뜻이 원소마다 반대다 (제일 큰 함정)

| 열린 원소 | 받아들임 (+) | 내보냄 (−) |
|---|---|---|
| **Li** | **환원** | 산화 |
| **O** | **산화** | 환원(탈산소) |

그래서 결과 키를 `reduction/oxidation` 으로 박지 않고 **`uptake/release`** 로 중립화하고,
원소별 해석 문자열을 결과에 같이 실어 보낸다. **O 를 열면 전압 칸을 아예 안 찍는다** —
산소압을 전압으로 읽게 두면 안 된다.

## 3. 결과 — 산소가 세질수록 이 순서로 간다

```
낮은 μ_O (산소 적음)
  │  Li₃PO₄ (인산염) + LiS₄ (폴리설파이드)      ← ★ 산화 개시
  │  Li₄P₂O₇ (피로인산염)
  │  Li₂SO₄ (황산염) + 유리 S
  │  SCl / SCl₄
  │  Li₂S₂O₇ (이황산염) + LiPO₃ (메타인산염)
  ▼  Cl₂ → ClO₂ → ClO₃ → Cl₂O₇                ← 염소는 제일 마지막
높은 μ_O (산소 많음)
```

| | 산화 개시 Δμ_O | 첫 반응 |
|---|---|---|
| **LPSCl** (Li₆PS₅Cl) | −2.917 eV | O 4개를 **한꺼번에** 먹고 `Li₃PO₄` 1개 완성 |
| **modelc** (Li₅.₄PS₄.₄Cl₁.₆) | **−3.319 eV** | O 2.8개만 먹고 `Li₃PS₄` 0.3 을 **남긴 채 부분 산화** |

두 계의 **산소 없는 자기분해**는 같다 (Δμ_O = −3.373, `Li₃PS₄ + Li₂S + LiCl`).

## 4. 세 원소가 각자 다른 길을 간다 ★

**인 (P) — 점점 응축된다**
```
PS₄ → Li₃PO₄ (ortho, P당 O 4)
    → Li₄P₂O₇ (pyro, P당 O 3.5 · P–O–P 다리)
    → LiPO₃   (meta, P당 O 3 · 사슬)
```
산소가 늘수록 **P당 산소는 줄고** P–O–P 다리가 는다. 유리 형성 화학 그대로다.

**황 (S) — 두 방향으로 갈린다**
```
낮은 μ_O:  Li₂S → LiS₄(폴리설파이드) → 유리 S
높은 μ_O:  Li₂SO₄(sulfate) → Li₂S₂O₇(disulfate)
```
중간 구간에서 **둘이 공존한다** (Δμ_O −2.382 에서 `Li₂SO₄` 2개 + 유리 S 3개 동시).
즉 **황 일부는 산화되고 일부는 환원된 채 남는다** — 불균등화(disproportionation).

**염소 (Cl) — 끝까지 버티다 한꺼번에 나간다**
```
LiCl (Δμ_O −0.909 까지 그대로) → SCl/SCl₄/PCl₅ → Cl₂ → ClO₂ → ClO₃ → Cl₂O₇
```

## 5. 왜 P 가 먼저인가 — ⚠ 이건 **해석**이지 계산 결과가 아니다

**P–O 결합이 P–S 보다 훨씬 세다.** 인산염(`PO₄³⁻`)은 자연에서 가장 안정한 음이온 중
하나다. 그래서 산소가 조금만 들어와도 먼저 P 로 간다.

⛔ **계산은 *"이 조합이 제일 낮다"* 만 말한다.** 위 문장은 그 결과에 대한 화학적 해석이고,
계산이 뽑아낸 결론이 아니다. 원고에 쓸 때 그 구분을 지운다.

## 6. ⛔ 금지 서술 (정본 JSON §4 와 같은 내용)

| 금지 | 왜 |
|---|---|
| **Δμ_O 절대값 인용** | PBE 가 O₂ 를 ~1 eV 과결합 · MP anion correction — 축이 **MP 보정 기준계**의 것이다 |
| **pO₂ · 온도 환산** | 기준 선택이 결과를 지배하는 자리 → §7 앵커 뒤에 별도로 |
| **UMA 등 다른 방법과 혼용** | 축이 통째로 밀린다 |
| **"산화 개시 전압/압력"** | 이건 **열역학 임계 μ** 지 동역학이 아니다. 실제 개시는 표면·입계·속도가 정한다 |
| **"어느 쪽이 공기 중에 더 안정하다"** | ★ 아래 |
| **계간 차이의 *크기* 인용** | 순서만 읽는다 (modelc 가 먼저 — 여기까지) |

### ★ 마지막 것이 제일 중요하다 — hull 은 passivation 을 안 본다

**hull 은 "끝까지 가면 어디로 가나" 를 말하지 "언제 멈추나" 를 말하지 않는다.**

실물 안정성을 정하는 건 **passivation** 이다 — 분해 산물이 막을 만들어 더 이상의 반응을
막느냐. 그건 산물이 전자를 통하는지·치밀한지에 달렸고 **이 계산은 거기까지 안 본다.**

> **알루미늄은 열역학적으로 엄청 잘 산화된다. 그런데 실제로는 안 녹슨다** — Al₂O₃ 막이
> 즉시 덮어서다. hull 만 보면 *"알루미늄은 불안정하다"* 가 나온다. **그게 이 계산의 한계다.**

## 7. 축을 읽을 수 있게 만들기 — landmark 앵커 (2026-09-07 추가)

절대값을 못 쓴다는 제약을 **기준 반응으로 우회**한다:

```
2 Li + ½ O₂ → Li₂O          이 평형의 μ_O 를 같은 hull 에서 낸다
```

그러면 우리 개시점을 *"Li/Li₂O 평형보다 얼마나 위/아래"* 로 말할 수 있고,
**기준이 양쪽에서 지워져** PBE 과결합·anion correction 이 차이에서 상쇄된다.

```bash
python3 tools/oxidation/esw_grand_potential.py \
  --target "Li6PS5Cl:LPSCl" "Li5.4P1S4.4Cl1.6:modelc" \
  --elements Li P S Cl O --open_element O \
  --landmarks Li,Li2O Li2S,Li2SO4 Li3PS4,Li3PO4 \
  --out /data/work/runs/o2_screen/lpscl_muO_anchored.json
```

⚠ **완전 상쇄는 아니다.** 두 반응의 O 결합환경이 다르면 보정 오차가 완전히는 안 지워진다.
**원소 기준 절대값보다 훨씬 낫다** — 그것이 이 기능의 전부다.

⛔ `landmark_mu` 가 못 하는 것: 두 상이 hull 위인지 확인 안 함 · 비-O 조성이 비례하지
않으면 **억지로 균형 잡지 않고 None** · 실험 생성에너지와 대조하지 않음.

## 8. ⚠ 문헌 함정 — 이름이 같다고 같은 게 아니다

높은 μ_O 에서 **`Li₂S₂O₇` = 이황산염 = polysulfate** 가 나온다. 그런데
`litdb/papers/deng2026_polysulfate_layer_moisture_oxidation_lpsc.md` 제목에도
**"polysulfate layer"** 가 있다.

⛔ **같은 게 아니다.** 그 논문의 poly(sulfate) 는 **DTD(C₂H₄O₄S)로 일부러 입힌 개질층**이지
**분해 산물이 아니다.** *"우리 계산이 그 논문의 폴리설페이트를 예측했다"* 는 **틀린 말**이다.

💡 **대신 진짜로 대조할 수 있는 것**: 그 논문의 **XPS (S 2p · P 2p)**.
우리 예측이 *"P 가 먼저, S 가 나중"* 이니 그 스펙트럼으로 검증할 수 있다. **아직 안 했다.**

## 9. 단계 — 어디까지 왔나

| | 무엇 | 상태 |
|---|---|---|
| **S1** | 도구를 O 로 열기 (`--open_element`) | ✅ `e3735dd56` |
| **S2** | MP hull μ_O 스크리닝 | ✅ 이 문서 · GPU 0 · CPU 수 분 |
| **S2.5** | landmark 앵커 (`--landmarks`) | ✅ 구현 · ⏳ **gabia 재실행 대기** |
| **S3** | 상위 산물만 UMA 자기일관 hull | ⏳ 앵커 확정 뒤 |
| **S4** | MD | ⛔ **검증 게이트 통과 전에는 안 던진다** |

### S4 — MD 로 무엇을 말할 수 있나 (미리 정해 둔다)

⛔ **못 하는 것**
- **반응 자체를 UMA 로 믿으면 안 된다.** O₂ 해리·S 산화는 결합 끊기다. 검증 없이는
  결과가 아니라 그림이다 (Li₃N 금지 선례).
- **200 ps 로 핵생성을 못 본다** (T3 에 기록 — 결정 핵생성 11 ns).
- **반응 중 궤적에서 D·Ea 를 뽑으면 안 된다** — 상이 바뀌는 중이라 확산이 정의 안 된다.

✅ **할 수 있는 것** (우리 도구가 이미 내는 관측량)
1. **화학종 계수** — P 의 CN(S)/CN(O) 분포로 `PS₄ → PS₄₋ₓOₓ`, S–S 이황화, 유리 S
   (`tools/oxidation/hydrolysis_speciation.py` 가 H₂O 로 하던 것)
2. **1순위 관측량 = 잔존 PS₄ 층수 vs 시간** (D 가 아니다 — T3 와 같은 논리)
3. **z-binned 밀도** — O 가 표면에서 몇 nm 까지 파고드나
4. **반응 전/후를 따로 평형 MD** 로 재서 수송 변화 — 이건 정당하다

**검증 게이트(먼저 정한다)**: UMA 스냅샷 vs QE/VASP 단일점 힘·에너지 대조.
통과 못 하면 MD 는 **정성 그림**으로만 쓰고 숫자를 안 낸다.

## 10. 이 문서가 못 하는 것

- **새 판정을 하지 않는다.** 값은 `db/properties/o2_muO_screen_lpscl_2026_09_07.json` 이 정본.
- **실험과 대조하지 않았다.** deng2026 XPS 대조는 §8 대로 미실시.
- **속도를 말하지 않는다.** 전부 열역학 종점이다.
- **modelc 가 왜 더 일찍 산화되는지 모른다.** Cl 이 많고(1.6) Li 가 적은(5.4) 것과
  관련 있어 보이지만 **확인하지 않았다.**

## 관련
- `db/properties/o2_muO_screen_lpscl_2026_09_07.json` (값 정본)
- `tools/oxidation/esw_grand_potential.py` · `hydrolysis_speciation.py`
- `kb/methodology/esw_grandpotential_staircase_explained.md` (같은 방법의 Li 판 · 해설)
- `kb/reviews/codex_BG_prompt_webapp_aw_release_2026_09_07.md` §B-3 (Q6·Q7 회신 대기)
- `litdb/papers/deng2026_polysulfate_layer_moisture_oxidation_lpsc.md`
