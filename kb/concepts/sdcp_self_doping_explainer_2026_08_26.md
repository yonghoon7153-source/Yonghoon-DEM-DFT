---
title: 자기도핑(self-doping)이란 무엇인가 — 프로톤이 아니라 수소 원자를 뗀다
date: 2026-08-26
updated: 2026-08-26
tags: [sdcp, self-doping, polaron, orca, manuscript-wording, concept]
status: 정리완료
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-26
verifiedBy: "우리 계산 설정(make_phaseB_doped_v2.py: charge 0 · tot_magnetization 1.0)과 에너지 검산(E(neutral)−E(doped)=0.654 Eh ≈ H 원자 0.500 Eh + O–H BDE ~4.2 eV), Loewdin 스핀 n-시리즈(sdcp_master_summary_2026_07_16.md)로 대조"
explored: false
authoredBy: agent
effort: medium
claimType: definition
evidenceScope: multi-source-primary
---

# 자기도핑(self-doping)이란 무엇인가

> **이 문서는 배경 지식 0 을 가정한다.** 원고 문장 하나를 고치려다 나온 이야기인데,
> 그 한 단어("proton" vs "hydrogen atom")가 **계산 자체를 다른 것으로 바꾼다.**
> 왜 그런지를 처음부터 푼다.

---

## 1. 등장인물 — SDCP 가 뭔가

**SDCP** = self-doped conducting polymer (자기도핑 전도성 고분자). 우리가 다루는 것은
**PEDOT-S 계열**이고, 한 단위(모노머)는 세 부분으로 되어 있다.

```
   ┌─ 티오펜 고리 ─┐   ┌─ 알킬 스페이서 ─┐   ┌─ SO₃H ─┐
   (전자가 흐르는 길)      (연결 끈)         (산성 머리)
        = 백본(backbone)                    = 술폰산기
```

- **백본** — 티오펜 고리들이 이어져 π 전자가 흐르는 길. **전기가 여기로 흐른다.**
- **SO₃H (술폰산기)** — 끈으로 백본에 묶여 있는 산성 머리. 황산기 같은 것.

## 2. "도핑" 이 전도성 고분자에서 뜻하는 것

반도체 도핑(붕소·인 넣기)과 **다르다.** 전도성 고분자에서 도핑은
**백본에서 전자를 하나 빼는 것**이다.

```
중성 백본:  π 전자가 꽉 차 있다  →  움직일 자리가 없다  →  안 흐른다
도핑 백본:  전자 하나가 빠진다  →  그 빈자리(hole)가 움직인다  →  흐른다
```

이 빈자리를 **hole(정공)** 또는 **폴라론(polaron)** 이라 부른다. **캐리어**가 그것이다.

⚠ **중성 사슬에는 캐리어가 아예 없다.** 도핑이 캐리어를 **만든다.**

## 3. 그럼 "자기(self)" 도핑은 뭐가 다른가

전자를 빼면 백본이 **양전하(+)** 를 띤다. 물질 전체가 중성이려면 **음전하 짝**이 필요하다.

| | 짝 음이온이 어디 있나 |
|---|---|
| 보통 도핑 | 밖에서 넣어준다 (예: ClO₄⁻, PSS⁻) — **따로 떠다닌다** |
| **자기도핑** | **자기 분자에 끈으로 묶여 있다** (SO₃⁻) — 도망 못 간다 |

우리 분자에서는 SO₃H 가 H 를 잃고 **SO₃⁻** 가 되면서 그 역할을 한다.
짝 음이온이 자기 몸에 붙어 있으니 **"자기"도핑**이다.

> 왜 좋은가: 밖에서 넣은 짝 음이온은 시간이 지나면 이동하거나 빠져나가 성능이 변한다.
> 끈으로 묶여 있으면 그런 일이 없다.

---

## 4. ★ 핵심 — 프로톤을 뗐나, 수소 원자를 뗐나

여기가 원고 문장이 걸린 자리다. 두 표현이 **완전히 다른 계산**을 뜻한다.

수소 원자 하나는 **양성자 1개 + 전자 1개** 로 되어 있다. 그래서 "뗀다" 에 두 가지가 있다.

| | 뗀 것 | 남은 것 | 알짜 전하 | 전자 수 | 껍질 |
|---|---|---|---|---|---|
| **프로톤 제거** | H⁺ (양성자만) | 전자는 남는다 | **−1 (음이온)** | 162 (짝수) | 닫힌껍질 singlet |
| **수소 원자 제거** | H• (= H⁺ + e⁻) | 전자도 같이 나간다 | **0 (중성)** | 161 (홀수) | **열린껍질 doublet** |

**분자식은 둘 다 C₁₁H₁₅O₆S₂ 로 똑같다.** 그래서 식만 보면 구분이 안 된다 —
**문장이 유일한 구분 장치다.** 이게 이 문제가 사소하지 않은 이유다.

### 전자 수 세보기

```
C 11개 × 6 = 66
H 15개 × 1 = 15
O  6개 × 8 = 48
S  2개 × 16 = 32
─────────────────
합계         161개   ← 홀수!
```

중성일 때 161 전자 = **홀수** = 짝을 못 이룬 전자가 하나 남는다 = **doublet 라디칼**.
프로톤만 뗐다면 162 전자 = 짝수 = 닫힌껍질. **두 계산은 전자 하나와 스핀 다중도가 다르다.**

### 그리고 자기도핑의 정의상 중성이어야 한다

3절에서 본 대로 자기도핑은 "백본의 + 를 SO₃⁻ 가 상쇄" 하는 것이다.
⇒ **알짜 중성이 되어야 자기도핑이다.** 음이온(−1)이면 상쇄가 안 된 상태다.

⇒ **"수소 원자 제거" 가 맞다.**

---

## 5. 우리 계산이 그걸 확정한다 — 두 겹의 증거

### ① 입력 설정

`tools/sdcp/make_phaseB_doped_v2.py`

```
charge 0 · tot_magnetization 1.0 (doublet)
"proton -> the doped radical (C11H15O6S2, 34 at)"
```

**charge 0 + doublet** = 중성 라디칼. 4절 표의 아래 칸이다.

### ② ⭐ 에너지 검산 (이게 결정적이다)

중성 분자와 도핑 분자의 에너지 차이를 보면 **무엇이 떨어져 나갔는지** 역산할 수 있다.

```
E(neutral) − E(doped) = 0.654 Eh
                      ≈ H 원자 (0.500 Eh) + O–H 결합해리에너지 (~4.2 eV)  ✓
```

- **H 원자** 를 뗐다면 → 그 원자의 에너지 + 끊은 결합 에너지만큼 차이가 난다. **맞는다.**
- **프로톤(H⁺)** 만 뗐다면 → 전자가 남으므로 이 값이 안 나온다.

즉 우리 계산은 **처음부터 수소 원자를 뗀 것**이고, 원고 원문의 "removing the sulfonate
proton" 은 그 계산을 잘못 기술한 것이다.

---

## 6. ⚠ 그런데 수정안의 뒷부분은 과하다

제안된 수정문:

> "…leaving a charge-neutral unit with an **oxidized backbone** compensated by
> the tethered sulfonate group"

앞부분(charge-neutral, hydrogen atom)은 맞다. 그런데 **"산화된 백본"** 은
**우리 모노머 데이터가 반박한다.**

### 스핀이 실제로 어디 있나 (Löwdin 스핀 분포)

hole 이 백본에 있는지 SO₃ 에 있는지는 **짝 없는 전자(스핀)가 어디 앉아 있나**로 본다.

| n (사슬 길이) | SO₃ 지분 | 백본 π 지분 | 성격 |
|---|---|---|---|
| **1 ← C₁₁H₁₅O₆S₂ 가 이것** | **~65 %** | **~35 %** | **SO₃ 중심 라디칼** |
| 2 | 62.3 % | 32.6 % | 아직 SO₃ 우세 |
| 3 (끝 고리 도핑) | 54.6 % | 39.8 % | 여전히 SO₃ 우세 |
| **3 (가운데 고리 도핑)** | 42.3 % | **50.1 %** | ★ **백본 폴라론으로 역전** |

**모노머에서는 스핀의 2/3 가 SO₃ 위에 있다.** "백본이 산화되고 SO₃⁻ 가 보상한다" 는
그림은 **n=3 내부 도핑에서야 성립**한다. 우리는 이 전환을 **폴라론 백본화 크로스오버**
라 부른다.

> **왜 사슬이 길어지면 백본으로 가나** — π 컨쥬게이션이 길수록 hole 이 퍼질 자리가 많아져
> 에너지가 낮아진다. 짧으면 퍼질 곳이 없어 SO₃ 의 산소 론페어에 머문다.
> 부수 관찰: 컨쥬게이션 이웃이 **둘**인 가운데 고리가 스핀을 우선 받는다(π-허브 효과).

---

## 7. 그래서 원고에 이렇게 쓴다

> the self-doped form C₁₁H₁₅O₆S₂ was obtained by removing a **hydrogen atom**
> (H⁺ + e⁻) from the sulfonic acid group, giving a **charge-neutral, open-shell
> (doublet)** species in which the tethered sulfonate serves as the internal
> counter-anion. At the monomer length the resulting spin is **predominantly
> sulfonate-centred** (backbone π share ≈ 35 %); it crosses over to a backbone
> polaron only for the internally doped trimer (≈ 50 %).

**`(H⁺ + e⁻)` 괄호가 핵심이다.** 이 한 조각이 "왜 중성인데 H 를 뗐나" 를 그 자리에서
설명하고, 리뷰어가 charge/multiplicity 를 되묻는 것을 막는다.

크로스오버 문장을 넣기 싫다면 최소한 **`in which the tethered sulfonate serves as the
internal counter-anion` 까지만** 쓰고 `oxidized backbone` 은 뺀다 — 그건 n=3 이야기다.

### 원고에서 같이 확인할 것

분자식만으로는 음이온/중성이 구분되지 않으므로, **원고 다른 곳에서 이 화학종을
음이온으로 적고 있지 않은지** 확인해야 한다. 있으면 내부 모순이다.
계산이 charge 0 / doublet 이므로 **원고 전체가 중성 doublet 으로 통일**되어야 한다.

---

## 8. ⛔ 이 문서가 말하지 않는 것

- **실험에서 실제로 무엇이 떨어지는지 말하지 않는다.** 실제 자기도핑은 산화제와
  짝염기가 관여하는 화학이고, 우리 계산은 그 알짜 결과(H 원자 하나 제거)를 모형화한 것이다.
  떨어진 H 의 행선지는 "산화제/짝염기" 로 부기한다.
- **전도도를 말하지 않는다.** 캐리어가 생겼다는 것과 그것이 잘 흐른다는 것은 다르다.
- **스핀 지분 수치는 Löwdin 분석 값**이다. 분할 방식(Mulliken/Hirshfeld 등)에 따라
  숫자가 달라진다 — **크로스오버라는 경향**이 결론이고 절대 %가 아니다.
- 사슬 길이는 n=1–3 만 계산했다. "n↑ 에서 백본 지배" 는 **외삽**이다.

## 근거 위치

- 계산 설정: `tools/sdcp/make_phaseB_doped_v2.py`
- 에너지 검산 · 스핀 n-시리즈: `kb/results/sdcp_master_summary_2026_07_16.md` §2–3
- 그림: `sdcp_monomer_MO_scheme.png` (모노머 MO 사다리 + HOMO 에서 전자가 빠지는 자리)
