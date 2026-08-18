---
title: 자리 선호 그림의 막대는 시드가 아니라 도핑 수준이다 — 그리고 6종은 자리가 바뀐다
date: 2026-08-18
updated: 2026-08-18
tags: [site-preference, doping, seminar, provenance, uma, concentration]
status: 확정
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-18
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 자리 선호 그림의 막대는 시드가 아니라 도핑 수준이다 — 그리고 6종은 자리가 바뀐다

세미나 9장(`Step 1 — 치환 자리`)의 그림을 손보다 **세 가지 오류**가 한꺼번에 나왔다.
전부 1저자 지적에서 출발했고, 전부 그림·대본에 이미 인쇄돼 있던 것이다.

## 1. 막대의 정체 — 시드가 아니다 ⛔

덱 캡션이 **"Bars are the spread across our three runs"** 라고 했다. **틀렸다.**

```
site_preference_raw_78.csv 헤더:
  "78 systems (26 dopant oxides x 3 nominal x)"
  x_nominal 열 = 0.02 / 0.05 / 0.10
```

세 점은 **세 도핑 수준**이다. 재현 산포가 아니다.

⇒ **막대가 0 을 걸치는 것은 잡음이 아니라 실측이다** — "농도에 따라 자리가 바뀐다".
   앞 판은 그걸 오차로 읽고 넘어갔다.

## 2. "작은 4가는 P 자리" 가 너무 셌다

1저자 지적: *"이건 섵부른게 B같은경우에는 P 경우도 Li 경우도 있어"* — 맞다.

| 판정 | 수 | 원소 |
|---|---|---|
| 전 농도 **Li 자리** | 19 | Y·Ba·Na·Mg·Ca·Sr·Ag·Cu·Fe·Zn·Sc·Co·Mn·In·Gd·Sm·Nd·La·Ga |
| 전 농도 **P 골격** | **1** | **Si 뿐** |
| **농도에 따라 바뀜** | **6** | **B · Al · Cr · Ge · Ni · Sn** |

바뀌는 6종의 실제 경로:

```
B    x002:Li → x005:P  → x010:P     (+0.76 / −0.41 / −0.21)
Al   x002:Li → x005:Li → x010:P
Cr   x002:Li → x005:Li → x010:P
Ge   x002:P  → x005:P  → x010:Li
Ni   x002:P  → x005:Li → x010:Li
Sn   x002:P  → x005:Li → x010:P     ← 단조도 아니다
```

⇒ 앞 대본의 **"아래로 내려간 게 셋 — Si, Ge, Sn"** 은 틀렸다. Ge·Sn 은 바뀌는 쪽이고,
   **전 농도 P 는 Si 하나**다. "크기가 거의 다 정한다" 도 6종에는 안 통한다.

## 3. 미수렴 3건이 표시 없이 그려져 있었다

`Al x002` · `Ag x002` · `Ag x010` (3/78). 원본 헤더의 규정:

> `converged=n` → M@P did not reach fmax (big cation on P is high strain);
> **dE is an UPPER bound**, the SIGN stays trustworthy for large cations.

처리: **지우지 않고 표시**한다(속 빈 회색 사각). 지우면 Ag 평균이
**+1.94 → +2.44** 로 뛰어 그림이 실제보다 확실해 보인다.
Ag(r 1.15)는 큰 양이온이라 부호는 유효하고, Al(r 0.535)은 작아서 부호도 덜 믿을 만한데
Al 은 이미 "바뀜" 으로 분류돼 있어 판정이 달라지지 않는다.

## 4. ⚠⚠ 라벨 함정 — `x005` 를 실제 농도로 읽지 말 것

1저자 질문: *"도핑농도 관련해서 0.25로 들어갔다고 닫힌거 아니였어? 모순아니야?"*

**모순은 아니다 — 다른 캠페인이다.** 그런데 그 질문이 진짜 함정을 건드렸다.

| | site_preference (이 그림) | cascade (점수·순위) |
|---|---|---|
| 위치 | gabia `/data/work/runs/site_preference/` (2026-06-19) | `multi_category_2026_05_26_v23` |
| 라벨 | x002 / x005 / x010 | **x002 / x005 / x010 (같은 이름!)** |
| 실제 x | 셋이 **진짜 다름** (아래 검증) | **셋 다 0.25** — 시리즈 **무효** |

cascade 쪽 기록(`kb/methodology/hard_dopant_handling_protocol.md`):

> 3 농도(x002/x005/x010) **actual_x 전부 0.25**, 구조/에너지 동일 → 농도시리즈 무효.

**같은 병인지 검사했다 — 아니다:**

```
세 농도 dE 가 완전히 같은 원소: 1/26 (Mn 만 두 값 중복)
농도 간 dE 폭: 중앙값 1.53 eV · 최소 0.10 · 최대 2.48
```

cascade 처럼 "구조·에너지 동일" 이었다면 dE 가 똑같이 나왔을 것이다. 안 그렇다.

**그래도 라벨을 실제 농도로 인용하면 안 된다.** 실측된 한 건
(`kb/results/site_preference_findings_2026_06_19.md`):

```
Y2O3_x005 = 47원자 셀에 Y 2개 = 4.3 at% = P 자리의 33 %
```

명목 5 % 가 아니다. 그 카드 자신이 *"과도핑 비판은 쌍방에 적용된다"* 고 적어 뒀다.
⇒ 슬라이드·대본은 **"세 도핑 수준"** 으로만 쓰고 0.02/0.05/0.10 숫자는 넣지 않는다.

## 5. 반영한 곳

| 무엇 | 어디 |
|---|---|
| 6종 분리(속 빈 앰버) · 미수렴 표시(속 빈 회색) · 범례 4줄 | `tools/figures/plot_seminar_2026_08.py: fig_site_choice` |
| 원소별 세 농도 dE · 판정 · 미수렴 농도 | `db/properties/seminar_table_site_preference.csv` |
| 라벨 함정 경고 | 위 CSV 헤더 + fig_site_choice docstring |
| 슬라이드 문장·대본 | `kb/seminars/cascade_dopant_screening_story_2026_08.md` 9장 |

## 이 카드가 말하지 않는 것

- **왜 6종이 농도에 따라 바뀌는가** — 기구를 안 봤다. Sn 은 단조도 아니라(P→Li→P)
  단순한 농도 효과로 설명되지 않는다.
- **x002/x005/x010 각각의 실제 원자수** — CSV 에 없다. 실측은 `Y2O3_x005` 한 건뿐이다.
- **UMA 가 이 자리 판정에 충분한가** — Wang 2025 는 Y 를 P(4b)로 보고 우리는 Li 로 본다.
  `site_preference_findings_2026_06_19.md` 가 그 충돌을 다루고, **결정 실험은 아직**이다
  (comp1 host 에서 동일 조성·동일 범함수로 Y@4b vs Y@24g DFT 1쌍).
- **antisite 벌점** — same-composition swap 이라 밀려난 host 원자의 벌점이 섞여 있다
  (원본 헤더의 CAVEAT). 절대값이 아니라 부호·순위로만 쓴다.

## 재현

```bash
python3 -c "
import sys,os; sys.argv=['x']; sys.path.insert(0,'tools/figures')
import plot_seminar_2026_08 as m; m.fig_site_choice()"
python3 tools/figures/plot_seminar_2026_08.py --selftest
```
