---
title: "NMR 화학적 이동 읽기 — 차폐 · ppm · up-field"
date: 2026-10-28
updated: 2026-10-28
tags: [nmr, chemical-shift, shielding, ppm, up-field, paramagnetic, li7, p31, ndo-lpscl16, reading-guide]
status: 확정 (개념 카드)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: definition
evidenceScope: multi-source-mixed
---

# NMR 화학적 이동 읽기 — 차폐 · ppm · up-field

> [!info] 이 카드가 답하는 질문 (사용자, 2026-10-28)
> NdO-LPSCl1.6 원고의 NMR 문단 (Fig. 1g · 1h) 을 같이 읽다가 나온 질문이에요.
> **"낮은 ppm 쪽으로 옮겨 간 건 (up-field) Li 핵이 주변 전자에 조금 더 가려졌다는 뜻 — 쉽게 설명해줄 수 있나? NMR 에 대해서 잘 모르는 듯"**

원고의 NMR 문단은 '화학적 이동' 하나만 알면 읽혀요. 다섯 단계로 풀고, 그다음 원고 문장에 대 볼게요.
그림 안 글자는 하우스 규약대로 영어예요. 그림은 `tools/figures/build_nmr_shift_figures.py` 가 만들어요 (`docs/figures/nmr_shift/`).

---

## 1. NMR 을 쉽게 — 다섯 단계

### ① 원자핵은 작은 자석이에요

⁷Li · ³¹P 핵은 스핀이 있어서 작은 막대자석처럼 굴어요. 센 자기장 B₀ 안에 넣으면 팽이처럼 세차 운동을 해요.
그 진동수는 핵이 느끼는 자기장 세기에 비례해요.

- 비례 상수는 핵마다 달라요.
- 보통 쓰는 9.4 T 자석에서 ⁷Li 는 약 155.5 MHz, ³¹P 는 약 162.0 MHz 로 돌아요.
- 같은 자석에서 ¹H 가 400 MHz 라서 이런 장비를 '400 MHz 장비' 라고 불러요.

![Spin precession in B0](/api/file/docs/figures/nmr_shift/nmr_01_spin_precession.svg)

### ② 같은 진동수의 전파를 쏘면 흡수해요 (공명)

핵이 도는 진동수와 같은 전파를 쏘면 핵이 에너지를 받아요. 장비는 이 흡수를 봉우리로 그려요.
핵이 느끼는 자기장이 세면 진동수가 높고, 약하면 낮아요.

![Resonance gives one peak](/api/file/docs/figures/nmr_shift/nmr_02_resonance.svg)

### ③ 둘레 전자가 자기장을 조금 가려요 (차폐)

핵 둘레의 전자가 바깥 자기장에 반응해서 반대 방향의 작은 자기장을 만들어요.
그래서 핵이 실제로 느끼는 자기장은 B₀ 보다 아주 조금 작아요.

- 가리는 정도는 둘레 환경에 따라 달라요.
- 이웃 원자가 누구인지, 얼마나 가까운지, 결합이 어떤지가 영향을 줘요.
- 그래서 같은 ⁷Li 라도 놓인 자리에 따라 봉우리 위치가 조금씩 달라져요.

![Thin vs thick electron cloud](/api/file/docs/figures/nmr_shift/nmr_03_shielding.svg)

그림의 작은 아래 화살표가 전자가 만든 반대 방향 자기장 b_ind 예요. 전자가 두껍게 감쌀수록 b_ind 가 커지고,
핵이 느끼는 자기장 B_eff 가 줄어요. 이 비율 σ 를 차폐 상수라고 해요.

### ④ ppm 은 그 작은 차이를 재는 눈금이에요

차폐로 생기는 진동수 차이는 아주 작아요. 그래서 기준 물질과 견줘 백만분의 몇만큼 옮겨 갔는지로 적어요.

$$\delta\ (\mathrm{ppm}) = \frac{f - f_\mathrm{ref}}{f_\mathrm{ref}} \times 10^{6}$$

- ¹H 가 400 MHz 인 자석이면 ¹H 의 1 ppm 은 400 Hz 예요. ⁷Li 의 1 ppm 은 약 156 Hz 예요.
- ppm 으로 적으면 자석 세기가 달라도 같은 물질은 같은 숫자가 나와요. 그래서 논문끼리 바로 견줄 수 있어요.
- 0 ppm 은 정해 둔 기준 물질이에요. ⁷Li 는 보통 LiCl 수용액, ³¹P 는 보통 85 % H₃PO₄ 를 써요.

### ⑤ 'up-field' 는 낮은 ppm 쪽이에요

NMR 스펙트럼은 보통 그래프와 반대로, 왼쪽이 높은 ppm 이고 오른쪽으로 갈수록 ppm 이 줄어요.
오른쪽으로 갈수록 더 가려진 핵이에요.

이름은 옛날 장비에서 왔어요. 진동수를 고정하고 자기장을 올려 가며 공명을 찾았는데,
더 가려진 핵은 자기장을 더 올려야 (up) 공명했어요. 그래서 낮은 ppm 쪽을 up-field, 높은 ppm 쪽을 down-field 라고 불러요.

![ppm axis, up-field and down-field](/api/file/docs/figures/nmr_shift/nmr_04_ppm_axis.svg)

---

## 2. NdO-LPSCl1.6 원고 문단에 대 보면

### ⁷Li (Fig. 1g)

원고 문장의 숫자대로면 ⁷Li 봉우리가 1.48 → 1.16 ppm 으로, 오른쪽으로 0.32 ppm 옮겨 갔어요.
Li 핵이 평균적으로 조금 더 가려졌다는 뜻이고, Li 둘레의 이웃이나 거리가 바뀌었다는 신호예요.

argyrodite 에서는 Li 가 여러 자리를 빠르게 오가서, 자리마다의 봉우리가 하나로 평균돼 보여요.
그래서 이 숫자는 Li 전체의 평균 환경이 옮겨 간 것으로 읽어요.

![7Li peak shift (schematic positions)](/api/file/docs/figures/nmr_shift/nmr_05_li7_shift.svg)

위 그림은 원고 문장의 숫자로 위치만 맞춘 모식도예요. 봉우리 모양과 폭은 임의예요.

> [!note] 화학적 이동은 사진이지 속도계가 아니에요
> 화학적 이동은 "지금 어떤 환경에 있나" 를 찍은 사진이에요. Li 가 얼마나 빨리 움직이는지는 직접 말하지 않아요.
> 속도는 NMR 의 다른 측정 (봉우리 폭이 좁아지는 정도 · T₁ 이완) 으로 봐요.
> 그래서 원고도 이온전도도 · 활성화 에너지와는 'consistent with' 로만 이었어요.

### ³¹P (Fig. 1h)

PS₄³⁻ 안의 P 는 고유한 자리에 봉우리를 세워요. 그 봉우리가 그대로 있으면 PS₄ 가 남아 있다는 뜻이에요.
조금 옮겨 가면 PS₄ 둘레가 바뀌었다는 뜻이에요.

원고는 치환량이 늘수록 (x = 0 · 0.02 · 0.04) 봉우리가 조금씩 낮은 ppm 쪽으로 갔다고 적었어요.
원인으로 Nd 가 만든 국소 왜곡과, O 가 S 대신 P 에 붙는 P–O 결합을 들어요.

![31P peak shift (schematic, direction only)](/api/file/docs/figures/nmr_shift/nmr_06_p31_schematic.svg)

방향만 보인 모식도예요. 원고 문장에 ³¹P 숫자가 없어서 축에 값을 적지 않았어요.

### Nd³⁺ 상자성

Nd³⁺ 는 4f 궤도에 짝 없는 전자가 셋 있어서 그 자체가 작은 자석이에요.
가까운 핵이 느끼는 자기장을 바꿔 봉우리를 옮기거나 넓혀요. Nd 에서 멀어질수록 이 효과는 빠르게 약해져요.
결합 변화와는 다른 원인이라 원고는 '가능성' (possible contribution) 으로만 적었어요.

![Paramagnetic Nd3+ (schematic)](/api/file/docs/figures/nmr_shift/nmr_07_paramagnetic_nd.svg)

---

## 3. 해석 — 원고가 말하려는 흐름

- **Li 쪽**: Nd/O 치환 → Li 둘레 환경이 바뀜 (⁷Li 봉우리 이동) → Li 도약이 쉬워질 수 있음 → σ 증가 · Ea 감소와 들어맞음 (consistent with).
- **P 쪽**: PS₄³⁻ 주 봉우리가 그대로 남음 → PS₄ 골격은 유지 · 봉우리가 조금 이동 → 둘레가 바뀜 (Nd 국소 왜곡 · P–O 결합 · Nd³⁺ 상자성 가능성).
- **마무리**: Rietveld 결과와 함께 "Nd 와 O 가 argyrodite 격자에 들어갔다" 로 묶어요.

---

## 4. 우리 계산과의 관계

우리 캠페인은 NMR 화학적 이동을 **계산하지 않았어요** (GIPAW 같은 NMR 계산이 없어요). 그래서 숫자로 견줄 자리는 없고,
같은 방향인지만 볼 수 있어요. 값은 아래 원장 경로에서만 읽어요 (여기에 숫자를 옮기지 않아요).

| 원고가 말하는 것 | 우리 계산 | 원장 |
|---|---|---|
| Li 둘레 배위가 바뀌었다 | Nd/O 모델에서 Li 일부가 O 를 이웃으로 가져요. Li 의 Bader 전하 평균은 도핑 전과 거의 같아요 — 바뀐 건 Li 원자 자체보다 '이웃이 누구냐' 쪽이에요 | `db/properties/nd_q3_bader_elf_runlog_2026_10_19.json` (Bader · ELF) |
| PS₄³⁻ 가 남는다 | 모델에서 P 는 전부 4 배위 사면체를 유지하고, P–S 결합 세기 (결합당 ICOHP) 도 호스트와 거의 같아요 | `db/properties/canonical_registry.json` (ICOHP_PS · modelc 대 modelc_nd_doped) |
| O 가 P–O 결합을 만든다 | 9 월 O 배치 비교에서 검색한 세 배치 중 O 가 P 에 붙는 배치가 가장 낮았어요 (세 배치만 봤고 카드는 비준 전) | `db/properties/ndo_lpscl16_o_motif_estimand_2026_09_09.json` |
| Nd 가 국소 기하를 흐트러뜨린다 | Nd 를 P 자리 (4b) 에 넣은 셀은 이완하면 Nd 가 사면체를 안 지키고 6 배위로 바뀌어요 | `db/properties/ndo_lpscl16_n5fu_icohp_2026_09_10.json` |
| Li 도약이 쉬워져 σ↑ · Ea↓ | **못 견줘요.** Nd 를 넣은 MD 가 없고, Nd+O BVSE 는 인용 금지, O 만 넣은 MD 비교는 원장이 'O 효과' 로 읽지 못하게 막아요 | `db/properties/bvse_nd_doping_2026_09_18.json` · 레지스트리 금지 `difference_with_lpsocl_as_O_effect` |
| Nd³⁺ 상자성 | **못 견줘요.** 우리 Nd 계산은 4f 를 코어에 얼린 계산이라 상자성을 다루지 않아요 | — |

⚠ 우리 Nd 셀은 원고 목표 조성보다 Nd 가 10 배 넘게 진해요. 그래서 이동 크기는 견주지 않고 방향만 봐요.

---

## 5. 이 카드가 못 하는 것

- **NMR 을 계산하지 않는다.** 그림은 개념 모식도예요. ⁷Li 그림의 봉우리 위치만 원고 문장 숫자에 맞췄고, 모양 · 폭은 임의예요.
- **⁷Li 숫자 (1.48 · 1.16 ppm) 는 원고 문장에 적힌 값이에요** — 우리 계산값이 아니에요. ³¹P 그림에는 숫자가 없어요.
- 상자성 이동의 크기 · 거리 의존은 다루지 않아요 (원고도 '가능성' 까지만 적었어요).
- 기준 물질 · 장비 숫자 (9.4 T · 155.5 · 162.0 MHz) 는 교과서 값이에요. 원고의 실제 측정 조건 (자기장 · MAS 속도 · 기준 물질) 은 원고 Methods 를 봐요.
