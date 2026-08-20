---
title: "cascade 세미나 — 덱 3~7장 대본 (재정비판)"
date: 2026-08-20
updated: 2026-08-20
tags: [seminar, cascade, screening, script, intro]
status: 초안 — 본 대본 병합 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# cascade 세미나 — 덱 3~7장 대본 (재정비판)

> ⚠ **번호는 덱 기준**이다. 본 대본(`cascade_dopant_screening_story_2026_08.md`)과
> 어긋나 있어 그쪽 번호를 쓰지 않는다:
>
> | 덱 | 본 대본 | 비고 |
> |---|---|---|
> | 3 Failure modes | 2 + **3** | 본 대본 3장(lever)이 **덱에서 이 장 그림에 흡수**됐다 — 초록 상자 3개가 그것 |
> | **4 The standard route** | — | **본 대본에 없는 장.** 여기서 신설 |
> | 5 Prior work (1) | 4 | |
> | 6 Prior work (2) | 5 | |
> | 7 Prior work (3) | 6 | |
>
> ⇒ 본 대본에 병합할 때 **덱에 "Selecting the modification lever" 장이 따로 있는지
> 먼저 확인**할 것. 없으면 본 대본 2·3장을 아래 3장으로 합치고 이후 번호를 +1 한다.

색 규칙: 빨강 = 한계·못 한 것, 파랑 = 강조·우리 기여. **빨간 글씨에서 한 박자 쉰다.**
기호 · `< >` 그림 이름표 · `해설` 그림 밑 한 줄 · `💬` 말로만 · `💡` 보조 · `⛔` 금지

---

## 3 — Failure modes in sulfide solid electrolytes

> ■ Failure modes in sulfide solid electrolytes
> • Electrochemical and mechanical degradation are coupled.
> • Because these failure modes are coupled, improving one of them can [빨강]degrade another[/],
>   and the loss is [빨강]not detected[/] unless each mode is evaluated separately.

**[85초]** — 본 대본 2장 + 3장(레버 선택)을 합쳤다. 덱에서 두 내용이 이 그림 한 장에 있다.

먼저 이 그림 한 장을 보고 가겠습니다. 가운데가 셀이고 위가 양극, 아래가 음극입니다.

황화물 전해질은 이온이 아주 잘 다닙니다. 액체 전해질에 견줄 정도예요. 그런데 문제가
한 축이 아닙니다. 왼쪽 붉은 쪽이 전기화학입니다. 양극에서 전해질이 산화돼 분해되고,
양극에서 나온 것들이 전해질을 다시 공격합니다. 오른쪽 파란 쪽은 역학입니다. 충방전마다
부피가 변해 입자 접촉이 떨어지고, 균열이 생기고, 음극 쪽에서는 덴드라이트가 뚫습니다.

이 둘이 서로를 키웁니다. 분해되면 접촉이 나빠지고, 접촉이 나빠지면 남은 자리로 전류가
몰려 다시 분해됩니다.

[빨강에서 쉼] 그래서 **한쪽을 고치면 다른 쪽이 나빠질 수 있는데, 각각을 따로 재지 않으면
그 손해가 안 보입니다.** 이게 오늘 발표가 축을 여러 개 보는 이유입니다.

**— 여기서 레버 선택으로 넘어간다 —**

가운데 초록 상자 세 개가 실제로 쓰이는 레버입니다. 양극 입자 코팅, 음극 공정,
그리고 전해질 자체의 조성 개질.

앞의 둘은 계면에서 벌어지는 일입니다. 만들기도 어렵고 미리 계산하기는 더 어렵습니다.
반면 도핑은 격자 안의 일이라 **합성 전에 컴퓨터로 훑을 수 있습니다.** 그래서 세 번째를
골랐습니다.

💬 이건 저희 계산이 아니라 문헌에서 정리한 문제 지도입니다. 오늘 저희가 계산한 건
이 지도에서 **한 칸**입니다.

⛔ 이 장에서 우리 수치를 말하지 않는다. 문헌 개념도다.

---

## 4 — The standard route: accurate but slow

> ■ The standard route: accurate but slow
> • All four stages below were run for every composition, ending in DFT validation.
> • The cost per composition is [빨강]large[/], and it grows with every candidate added.
>
> `[박스] Standard route per composition`
> 1. Enumerate substitutions (site × charge recipe)
> 2. MLIP screen + anneal (Li ordering)
> 3. DFT validation (EOS, elastic, band structure)
> 4. Long MD (conductivity, multi-seed)
>
> To cover **91** candidates at **low cost**, a screening route was devised instead.
> 47 completed all three axes — the rest is [빨강]unfinished, not screened out[/].

**[70초]**

도핑 조성 하나를 제대로 보려면 이 네 단계를 돕니다. 자리와 전하 보상을 열거하고,
기계학습 퍼텐셜로 훑어서 어닐하고, DFT 로 확인하고, 마지막에 긴 MD 로 전도도를 잽니다.

과제를 하면서 이걸 여러 번 돌려봤습니다. **각 단계는 정확합니다. 문제는 비용이에요.**
조성 하나당 네 단계가 다 돌아야 하고, 후보가 늘면 그만큼 곱해집니다.

그래서 앞단에 싸게 훑는 경로를 하나 만들었고, 그걸 91종에 돌렸습니다.
오늘 발표가 그 얘기입니다.

**— 91 과 47 을 여기서 가른다 (뒤에서 반드시 질문이 나오는 자리) —**

여기 91은 **돌리려고 계획한 입력 목록**입니다. 그중 세 축을 끝까지 완주한 게 **47종**이고,
뒤에 나오는 깔때기는 그 47에서 시작합니다.

[빨강에서 쉼] 나머지 44종은 **떨어진 게 아니라 아직 안 끝난 겁니다.**
계산이 밀린 것이지 물리로 거른 게 아니에요.

💬 이 구분을 여기서 해두겠습니다. 뒤에서 47이 나올 때 "44개는 어디 갔냐"가 먼저 나오거든요.

⛔ `x = 0.02 / 0.05 / 0.10` 을 **농도로 말하지 말 것.** 폴더 라벨이다.

---

## 5 — Prior work (1): two ways to narrow a broad space

> ■ Prior work (1): two ways to narrow a broad space
> • One route [빨강]removes candidates[/] at every gate, so only a few reach the accurate methods.
>   (band gap → phase stability → electrochemical window → reactivity · 104,082 → 3)
> • The other [파랑]keeps every candidate[/] and raises the accuracy stage by stage.
>   (structure → band structure → fast model → first-principles MD at the last stage only)
>
> `< candidates removed at every gate >` · `< accuracy raised at every stage >`

**[65초]**

문헌도 같은 일을 합니다. 넓은 공간을 먼저 줄이고 나서 정확한 방법에 자원을 씁니다.
다만 줄이는 방식이 두 갈래예요.

왼쪽은 후보를 자릅니다. 십만 종에서 밴드갭, 상 안정성, 전기화학 창, 반응성 순으로 걸러
마지막에 세 종을 남깁니다.

오른쪽은 반대입니다. 후보는 그대로 두고 정밀도를 올립니다. 위에서는 구조만 보고,
아래로 갈수록 비싼 방법을 쓰다가 **맨 아래에서만** first-principles MD 를 돌립니다.

공통점은 하나예요. **비싼 계산은 마지막에, 살아남은 소수에만.**

💡 앞 장(4)에서 91/47 을 이미 갈랐으면 **여기서 스케일 얘기를 반복하지 않는다.**
두 번 말하면 방어적으로 들린다.

⛔ 우리 수치와 섞지 않는다. 104,082 는 **소환값**이다.

---

## 6 — Prior work (2): a model fed back into the screen

> ■ Prior work (2): A model fed back into the screen
> • The screen runs three physical branches and merges them into one candidate list.
>   (stoichiometry · electronic structure · atomistic structure → most promising candidates)
> • A classifier trained on measured conductivity is [파랑]fed back into that screen[/].
>   (measured pairs → feature extraction → superionic classifier)
>
> `< a trained model feeds back into the screen >`

**[60초]**

세 번째 갈래는 계산 대신 데이터를 씁니다. 그림이 상자 두 개로 나뉘어 있죠.

왼쪽이 스크리닝입니다. 위에서 만 이천 종으로 시작해 세 갈래로 갈라집니다. 조성에서는
원소 값이랑 매장량을, 전자구조에서는 밴드갭·산화 전압·hull 에너지를, 원자구조에서는
특징을 뽑습니다. 그 셋이 아래로 모여서 유망 후보가 나와요.

오른쪽이 모델입니다. **실측 전도도가 있는 데이터로** 특징을 뽑아 분류기를 학습시킵니다.

여기 이 굵은 화살표를 봐 주세요. 오른쪽에서 학습한 모델이 왼쪽 스크린으로 **다시
들어갑니다.** 전도도가 계산으로는 제일 비싼 축인데, 그 자리를 모델이 대신하는 구조예요.

💬 이 논문은 "정확도 90 %" 라고 쓰지 않습니다. 좋은 재료가 드물어서 **전부 나쁨이라고
찍어도 정확도가 높게** 나오니까요. 대신 **무작위 대비 몇 배**로 보고합니다.
저희도 그렇게 할 겁니다.

💬 저희도 나중에 같은 자리를 고민하게 됩니다. 오늘 발표에서 전도도는 결국 **프록시로만**
봤거든요. 그 얘기가 뒤에 나옵니다. *(→ 15장 Li 길 프록시 · 18장 못 한 것)*

⛔ **`40종`·`21종` 을 말하지 않는다** — 그림에 없는 본문 값이다. 그림에 찍힌 건
`12,831` 하나뿐이다. *(2026-08-20 정정: 앞 판 대본이 이 금지를 적어놓고 본문에서
"40종으로 학습한" 이라고 써서 자기모순이었다.)*

---

## 7 — Prior work (3): what each study actually varies

> ■ Prior work (3): What each study actually varies
> • One cation is placed on three candidate sites, and the site is chosen by energy.
>   (Li site · La site · Zr site → the lowest defect energy wins)
> • In this work a dopant enters as [파랑]a precursor, not an element[/], so two sites are
>   filled at once.
>
> `< defect energy on three garnet sites >`
> `해설` one cation at a time
>
> `< 26 dopant cations placed in our sulfide host >`
> `해설` one precursor at a time · Li 19 / P 1 / changes with x 6
>
> `[표]` study / host / what is varied / n / mechanical axis
> `this work | argyrodite sulfide | an added precursor compound | 47 (91 planned) |`
> `Included (reported as sensitivity, not a gate)`

**[75초]**

여기서 하나 분명히 하고 가겠습니다. 이런 스크리닝을 아무도 안 한 건 아닙니다.

왼쪽이 2015년 결과예요. LLZO 가넷에서 도펀트를 Li·La·Zr 세 자리에 각각 넣어 결함
에너지를 계산했습니다. 어느 자리에 앉을지를 계산으로 고른 거죠.
💬 **이 값은 후속 논문을 통해 인용했습니다.**

황화물 쪽에도 있습니다. 2024년에 argyrodite 구조 84개를 기계학습 퍼텐셜 MD 로 전수
계산한 연구가 있어요.

그러면 저희는 뭐가 다르냐. 표 세 번째 칸입니다. **무엇을 바꾸느냐**가 달라요.

위 두 연구는 원소 하나를 바꿉니다. 하나는 양이온을, 하나는 화학식 안에 이미 있는 원소를요.

저희는 **전구체를 하나 더 넣습니다.** 실제 합성이랑 같은 단위예요. LPSCl 은 Li₂S 랑
P₂S₅ 랑 LiCl 을 섞어 만드는데, 도핑할 땐 거기에 전구체를 하나 더 얹거든요.

그러면 원소가 아니라 **화합물이 들어갑니다.** MgO 면 Mg 랑 O 가 같이 들어가고,
양이온 자리와 음이온 자리를 **동시에** 정해야 합니다. 오른쪽 그림이 그 결과예요.

그리고 표 맨 오른쪽 칸. **기계 물성 축은 넷 중 저희만 있습니다.** 다만 그 축은
게이트가 아니라 **민감도로 보고**합니다 — 뒤에서 왜 그런지 말씀드리겠습니다.

💬 표의 `n` 은 연구마다 세는 게 다릅니다. 저희는 **완주한 47**을 적었고, 계획은 91이었습니다.

💬 한 가지 덧붙이면 — 코팅 스크리닝은 상대적으로 쉽습니다. 코팅 물질은 따로 존재하는
화합물이라 데이터베이스에서 꺼내면 됩니다. 십만 종을 돌릴 수 있었던 이유가 그거예요.
반면 도핑은 그 화합물이 **세상에 없습니다.** 구조를 직접 만들어야 하고, 자리를 골라야
하고, 전하를 맞춰야 합니다. 이게 어려운 지점이고, 뒤에 나올 결과가 정확히 그 대가입니다.

💡 이 장이 발표의 **포지셔닝**이다. "아무도 안 했다" 고 말하면 질문 한 방에 무너진다.
"했는데 **무엇을 바꾸느냐**가 다르다" 가 방어 가능한 주장이고 실제로도 그렇다.

⛔ **풀 정의로 우위를 주장하지 않는다.** 저쪽 풀은 "선행 실험 30 ∪ 선행 DFT 예측 45"
라는 **문헌 정의 집합**이고 한 문장으로 방어된다. 우리 47 은 사람이 큐레이션한 후보군이라
JSON 블록으로 길게 해명해야 한다 — **풀 정의의 문헌적 방어가능성은 그쪽이 우위**다
(`litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md`).
이 장에서 우리가 내세울 것은 **"무엇을 바꾸는가" 와 "기계 축"** 둘뿐이다.

---

## 이 재정비에서 고친 것 (원 대본 대비)

| # | 고친 것 |
|---|---|
| 1 | **덱 4장(standard route) 신설** — 본 대본에 없던 장. 네 단계 + 91/47 |
| 2 | **91 vs 47 정의를 4장에 심었다** — `unfinished, not screened out` (digest 의 `attrition_is_not_screening`) |
| 3 | 6장에서 **`40종` 삭제** — 같은 대본이 그걸 금지해놓고 본문에서 썼다 (자기모순) |
| 4 | 7장 왼쪽 그림 이름표 `45 dopants × 3 sites` → **`defect energy on three garnet sites`** (그 그림은 Anderson Fig 3d 이고 45개가 아니다) |
| 5 | 7장 오른쪽 이름표 `91 compounds` → **`26 dopant cations`** + `Li 19 / P 1 / changes with x 6` |
| 6 | 7장 표 `n = 91` → **`47 (91 planned)`** |
| 7 | 7장 `mechanical axis` = **`Included (reported as sensitivity, not a gate)`** — codex 판정으로 G5 를 선발 게이트에서 뺐다 |
| 8 | 7장에 **Miara 인용 경로 한 줄** + **풀 정의 우위를 주장하지 말라는 금지** 추가 |
| 9 | 5장의 "저희는 91 개입니다" 보조 제안 **삭제** — 4장에서 이미 갈랐다 |

## 관련

- 본 대본: `kb/seminars/cascade_dopant_screening_story_2026_08.md`
- 그림 생성: `tools/figures/plot_seminar_2026_08.py::fig_site_choice`
  → `docs/figures/seminar/step1_site_choice.png` (2026-08-20 재생성)
- 자리 선호 원자료: `db/properties/seminar_table_site_preference.csv` (26종)
- 인용 digest: `litdb/papers/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md` ·
  `xiao2019_cathode_coating_screening.md` · `kahle2020_ht_aimd_screening.md` ·
  `sendek2017_ml_screening_12k_conductors.md` · `anderson2024_llzo_comprehensive_dopant_screening.md` ·
  `lee2024_multicomponent_argyrodite_mixed_oxidation_mtp.md`
- 깔때기 판정: `kb/reviews/codex_C_funnel_2026_08_20.md`
