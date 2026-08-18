---
title: LPSCl 도펀트 스크리닝 — 연구세미나 대본 (v6 · 덱과 1:1)
date: 2026-08-16
updated: 2026-08-16
tags: [seminar, cascade, screening, doping, lpscl]
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-mixed
---

# LPSCl 도펀트 스크리닝 — 연구세미나 대본 (v6)

덱: `docs/Research_Seminar_2026_08_cascade_story_v6.pptx` (29장 · 그림 24 · 표 5)
**슬라이드 번호와 이 대본의 번호가 1:1로 맞는다.** 본문 24장 + 부록 5장, 본문 약 22분.

각 장 머리의 `> ■`·`> •` 은 **슬라이드에 실제로 인쇄된 문장**이다 (읽는 게 아니라 근거).
그 아래 한국어가 말할 내용.

어체는 2026-01-13 연구세미나 덱을 모티브로 맞췄다 —
제목은 그 장에서 하는 일의 이름, ■ 헤더는 `주제 (n): 대상`, • 불릿은 마침표로 끝나는 선언문.

색 규칙: 슬라이드의 **빨강 = 한계·못 한 것**, **파랑 = 강조·우리 기여**.
빨간 글씨에서 한 박자 쉰다. 그냥 읽고 넘어가면 청중은 결과만 가져간다.

기호 · `< >` 그림 이름표 · `해설` 그림 밑 한 줄 · `💬` 말로만 · `💡` 보조 제안
### 1 — (표지)

**표지 문구 확정 (2026-08-16 사용자 결정)** — 2026-06-15 덱 커버 양식을 그대로 따른다.

```
[상단 네이비 바]                                    August 2026   ← 우측 상단, 14 pt
Research Seminar                                  ← 파란 굵게 26 pt · 고정 헤더
Technical Report on DFT Screening:                ← 검정, 보고 유형 + 방법
Dopants in Li₆PS₅Cl                               ← 검정, 대상

Yonghoon An
Division of Materials Science & Engineering, Hanyang University
(E-mail : yonghoon71@hanyang.ac.kr)

[캠퍼스 일러스트]                      [한양대 로고]
```

- `Research Seminar` 는 **고정 헤더**다. 매번 바뀌는 건 아래 두 줄뿐 — 그래서 시리즈로 읽힌다.
- `Simulation → Screening` 한 단어만 바꿨다. 6/15 덱과 나란히 놓으면 같은 계열로 보인다.
- 풀 크기(91)는 **커버에 넣지 않는다.** 숫자가 바뀌면 커버까지 고쳐야 하고, 본문에서 이미 세 번 나온다.
- 커버 자산: `docs/figures/seminar/cover_campus.jpg` · `cover_logo.png`
  (2026-06-15 덱에서 추출 — 같은 발표자 시리즈이므로 그대로 재사용)


**[30초]**

안녕하세요. Li₆PS₅Cl 이라는 황화물 고체전해질에 원소를 하나씩 넣어 보면서, 쓸 만한 게
뭔지를 계산으로 훑은 내용을 말씀드리겠습니다.

발표는 세 덩어리입니다. 왜 이걸 했는지, 어떤 순서로 좁혔는지, 무엇을 알게 됐고 다음에
무엇을 할 것인지. 수식은 쓰지 않겠습니다.

---


## ① 왜 이걸 하나

### 2 — Failure modes in sulfide solid electrolytes

> ■ Motivation (1): Electrochemical and mechanical degradation are coupled
> • Cathode-side oxidation, contact loss, cracking and dendrite growth proceed together.
> • A modifier that improves one axis can degrade another without appearing there.

**[60초]**

먼저 이 그림 한 장을 보고 가겠습니다. 가운데가 셀이고 위가 양극, 아래가 음극입니다.

황화물 전해질은 이온이 아주 잘 다닙니다. 액체 전해질에 견줄 정도예요. 그런데 문제가
한 축이 아닙니다. 왼쪽 붉은 쪽이 전기화학입니다. 양극에서 전해질이 산화돼 분해되고,
양극에서 나온 것들이 전해질을 다시 공격합니다. 오른쪽 파란 쪽은 역학입니다. 충방전마다
부피가 변해 입자 접촉이 떨어지고, 균열이 생기고, 음극 쪽에서는 덴드라이트가 뚫습니다.

이 둘이 서로를 키웁니다. 분해되면 접촉이 나빠지고, 접촉이 나빠지면 남은 자리로 전류가
몰려 다시 분해됩니다.

💬 이건 저희 계산이 아니라 문헌에서 정리한 문제 지도입니다. 오늘 저희가 계산한 건
이 지도에서 한 칸입니다.

---

### 3 — Selecting the modification lever

> ■ Motivation (2): Lattice doping can be screened before synthesis
> • Coating and anode engineering act at interfaces, which are hard to build and to predict.
> • To survey a wide chemical space at low cost, lattice doping was chosen as the variable.

**[65초]**

방금 그림에 답이 들어 있습니다. 초록 상자 세 개가 실제로 쓰이는 레버입니다. 양극 입자
코팅, 음극 공정, 그리고 전해질 자체의 조성 개질.

앞의 둘은 계면에서 벌어지는 일입니다. 만들기도 어렵고 미리 계산하기는 더 어렵습니다.
반면 도핑은 격자 안의 일이라 **합성 전에 컴퓨터로 훑을 수 있습니다.** 그래서 세 번째를
골랐습니다.

다만 대가가 있습니다. 원소를 하나 넣으면 산화만 바뀌는 게 아니라 Li 경로도, 딱딱함도
같이 바뀝니다. 축이 하나가 아닙니다. 그리고 후보 91개에 자리와 전하 보상 방법을 곱하면
구조가 수천 개가 됩니다.

그래서 질문이 "무엇이 가장 좋은가"가 아니라 **"비싼 계산을 어디에 쓸 것인가"**가 됩니다.
이게 오늘 발표 내내 깔려 있는 질문입니다.

---


## ② 남들은 어떻게 하나

### 4 — Screening strategies in the literature  ✅ 확정 (2026-08-16)

> ■ Prior work (1): Broad spaces are narrowed before accurate methods
> • One route [파랑]removes candidates[/] at every gate, so only a few reach the accurate methods.
> &nbsp;&nbsp;(band gap → phase stability → electrochemical window → reactivity · 104,082 → [파랑]3[/])
> • The other [파랑]keeps every candidate[/] and raises the accuracy stage by stage.
> &nbsp;&nbsp;(structure → band structure → fast model → first-principles MD at the last stage only)

우상단 출처 — *Joule*, 3, 1252 (2019). / *Energy Environ. Sci.*, 13, 928 (2020).

`< candidates removed at every gate >`　`< accuracy raised at every stage >`

**[60초]**

문헌도 같은 일을 합니다. 넓은 공간을 먼저 줄이고 나서 정확한 방법에 자원을 씁니다.
다만 줄이는 방식이 두 갈래예요.

왼쪽은 **후보를 자릅니다.** 밴드갭, 상 안정성, 전기화학 창, 반응성 순으로 걸러서
십만 종이 세 종이 됩니다.

오른쪽은 반대예요. **후보는 그대로 두고 정밀도를 올립니다.** 위에서는 구조만 보고,
맨 아래에서만 first-principles MD 를 돌립니다.

💬 **말로만** (슬라이드에 없음) — 공통점은 하나입니다. **비싼 계산은 살아남은 것에만.**
   화면에 안 넣기로 했으니 이 문장은 반드시 입으로 나와야 합니다. 이게 다음 장으로 가는 다리예요.

💡 십만이라는 숫자에서 청중이 놀랍니다. "저희는 91 개입니다"를 여기서 한 번 짚어 두면
뒤에서 스케일 오해가 없습니다.

---

### 5 — Screening with a trained model  ✅ 확정 (2026-08-16)

> ■ Prior work (2): A trained model can replace the slowest gate
> • One track runs three physical branches and merges them into a candidate list.
> &nbsp;&nbsp;(stoichiometry · electronic structure · atomistic structure → most promising candidates)
> • The other trains a classifier on measured conductivity and [파랑]feeds it back into the screen[/].
> &nbsp;&nbsp;(measured pairs → feature extraction → superionic classifier)

우상단 출처 — *Energy Environ. Sci.*, 10, 306 (2017).
`< a trained model feeds back into the screen >`

**[55초]**

세 번째 갈래는 계산 대신 **데이터**를 씁니다. 그림이 상자 두 개로 나뉘어 있죠.

**왼쪽이 스크리닝입니다.** 위에서 만 이천 종으로 시작해 세 갈래로 갈라집니다.
조성에서는 원소 값이랑 매장량을 보고, 전자구조에서는 밴드갭·산화 전압·hull 에너지를
보고, 원자구조에서는 특징을 뽑습니다. 그 셋이 아래로 모여서 유망 후보가 나와요.

**오른쪽이 모델입니다.** 실측 전도도가 있는 데이터로 특징을 뽑아 분류기를 학습시킵니다.

여기 이 굵은 화살표를 봐 주세요. **오른쪽에서 학습한 모델이 왼쪽 스크린으로 다시
들어갑니다.** 전도도가 계산으로는 제일 비싼 축인데, 그 자리를 모델이 대신하는 구조예요.

💬 **말로만** — 저희도 나중에 같은 자리를 고민하게 됩니다. 오늘 발표에서 전도도는
   결국 프록시로만 봤거든요. 그 얘기가 뒤에 나옵니다.
   (이 한 마디가 STEP 6·9 로 가는 다리다. 안 하면 이 장이 그냥 남의 논문 소개로 끝난다.)

⛔ **말하지 말 것** — "저희가 이 논문에서 무엇을 채택했다" 류.
   본문을 안 읽었으므로 그림에 보이는 것까지만 말한다.
   숫자도 **12,831 만** 그림에 있다. 21 종·40 종은 본문 값이라 쓰지 않는다.

⚠ 슬라이드 상단 섹션명이 `Results & Discussion` 으로 돼 있는데, 이 장은 아직 문헌 소개다.
   `Introduction` 이 맞다.

---

## ③ 후보군

### 6 — Where prior screening stops  ✅ 확정 (2026-08-16)

> ■ Prior work (3): Site-resolved screening already exists
> • One cation is placed on three candidate sites, and the site is chosen by energy.
> &nbsp;&nbsp;(Li site · La site · Zr site → the lowest defect energy wins)
> • A dopant enters as [파랑]a precursor, not an element[/], so a cation and an anion are placed at once.

우상단 출처 — *Adv. Energy Mater.*, 14, 2304025 (2024). / *Chem. Mater.*, 27, 4040 (2015).
`< 45 dopants × 3 sites in a garnet >`　`해설` one cation at a time
`< 91 compounds in our sulfide host >`　`해설` one precursor at a time
`[표]` study / host / what is varied / n / mechanical axis
하단 — Lee 2024: *J. Mater. Chem. A*, 12, 7272.　Xiao 2019: *Joule*, 3, 1252.
　　　 Left: Anderson et al. (2024) Fig. 3d — defect energies taken from Miara et al. (2015), as stated in that caption.

⚠ **그림 crop 주의 (2026-08-17 정정)** — Anderson Fig. 3 은 세로 4패널이다.
   (a) Total LLZO wt % · (b) Cubic LLZO wt % · (c) Bond valence mismatch · (d) Defect energy.
   우리가 쓸 것은 **(d) 뿐**이고 원본 높이의 **0.762 ~ 1.0** 구간이다.
   앞 판은 0.695 에서 잘라 **(c) 의 x축 라벨 띠가 같이 들어가** 두 줄로 보였다 — 그래서
   "출처가 이 그림 맞나" 하는 의심이 생겼다. 재크롭 완료.

**[70초]**

여기서 하나 분명히 하고 가겠습니다. **이런 스크리닝을 아무도 안 한 건 아닙니다.**

왼쪽이 2015년 Ceder 그룹 결과입니다. LLZO 가넷에서 **도펀트 45종을 Li·La·Zr 세 자리에
각각 넣어 결함 에너지를 계산**했어요. 자리를 계산으로 고른 겁니다. 앞에서 본 실험 논문이
이 예측을 받아서 59종을 실제로 합성한 거고요.

황화물 쪽에도 있습니다. 2024년에 argyrodite 구조 84개를 기계학습 퍼텐셜 MD로 전수
계산한 연구가 있어요.

그러면 저희는 뭐가 다르냐. 표 **세 번째 칸**을 봐 주세요. **무엇을 바꾸느냐**가 다릅니다.

왼쪽 연구는 **양이온 하나**를 바꿉니다. 아래 두 번째 연구는 **이미 화학식 안에 있는
원소**를 다른 걸로 바꿔요. 둘 다 격자 안의 한 원소를 교체하는 겁니다.

저희는 **전구체를 하나 더 넣습니다.** 이게 실제 합성이랑 같은 단위예요. LPSCl 은
Li₂S 랑 P₂S₅ 랑 LiCl 을 섞어서 볼밀하고 소성해서 만드는데, 도핑할 때는 그 혼합물에
**전구체를 하나 더 얹습니다.** 문헌에서도 GaF₃ 를 넣거나 CuBr₂ 를 넣는 식이고요.

그러면 **원소 하나가 아니라 화합물 하나가 들어갑니다.** MgO 를 넣으면 Mg 랑 O 가 같이
들어가는 거고, 그러면 양이온 자리와 음이온 자리를 **동시에** 정해야 하고 전하도 맞춰야
합니다. 오른쪽 그림이 그 결과예요.

그리고 표 **맨 오른쪽 칸.** 기계 물성 축은 넷 중 저희만 있습니다.

💬 **말로만** — 코팅 스크리닝이 상대적으로 쉬운 이유가 여기 있습니다. 코팅 물질은
   **따로 존재하는 화합물**이라 데이터베이스에서 꺼내 열역학만 보면 돼요. 십만 종을
   돌릴 수 있었던 이유가 그겁니다. 반면 도핑은 그 화합물이 세상에 없어서 구조를 직접
   만들고, 자리를 고르고, 전하를 맞춰야 합니다. 이게 어려운 지점이고, **뒤에 나올 결과 1이
   정확히 그 대가**입니다.

💡 이 장이 발표의 포지셔닝이다. **"아무도 안 했다"고 말하면 질문 한 방에 무너진다.**
   "했는데 무엇을 바꾸느냐가 다르다" 가 방어 가능한 주장이고, 실제로도 그렇다.

💡 프리커서 프레이밍의 근거 (질문 오면) — 우리 litdb 실물:
   · GaF₃ 도핑: 전구체 Li₂S · P₂S₅ · LiCl **+ GaF₃**  (`liyaru_gaf3_codoping_argyrodite`)
   · CuBr₂ 도핑: Li₂S + P₂S₅ + LiCl **+ CuBr₂** → ball-milling → 소결
     ("dual-dopant 단일전구체 전략", `li2025_cubr2_dualdoping_argyrodite`)
   즉 **실험에서 도핑의 단위는 원소가 아니라 화합물**이다. 우리 스크리닝 단위가
   자의적인 선택이 아니라 합성 관행을 따른 것이라는 근거가 된다.

⚠ 인용 규율 — 왼쪽 그림은 **Anderson 2024 Fig. 3d** 이고 그 안의 값은 **Miara 2015** 다.
   둘 다 적어야 출처가 맞다. Miara 원본은 아직 우리 litdb 에 digest 가 없다
   (kb/open_items.md 「선행연구 대비 위치 규정」 A1 — 사용자 제공 예정).

---

### 7 — Candidate chemistry space  ✅ 확정 (2026-08-18)

> ■ Candidate set (1): 91 compounds across seven anion families
> • Each candidate is one precursor compound, chosen along two axes —
> &nbsp;&nbsp;[파랑]cations from +1 to +6[/], anions across seven families (strong M–O → soft, bulky I⁻).
> • Only compounds that already exist can go in — a safe list, and that matters later.

`[표]` family / n / role in the design / examples

⚠ **소불릿은 계열 설명이 아니라 선정 논리다** (2026-08-18 1저자 판정). 앞 장에서
  "precursor, not an element" 를 이미 말했으므로 여기서 되풀이하지 않고 **축 두 개**만
  남긴다. 계열별 사유는 표의 세 번째 칸이 담당한다 — 소불릿에 또 쓰면 표를 두 번 읽힌다.
⚠ **두 번째 줄에 빨강을 쓰지 않는다.** "나쁜 결과" 가 아니라 차분한 설계 한계라,
  칠하면 실제보다 세게 읽힌다. 이 장은 명세 슬라이드라 강조색 하나(파랑)로 충분하다.
⚠ 표 합계 = 37+19+11+10+5+5+4 = **91**. 황화물은 **계획 11** 이다.
  실제 완주는 10 (As₂S₃ 가 stage-01 에서 `n_structures = 0`). 이 장은 *넣은 것*의
  명세라 11 이 맞고, **빠지는 건 funnel/결과 장에서** 한 문장으로 짚는다.

**[45초]**

후보를 어떻게 골랐는지 말씀드리겠습니다. 축이 두 개입니다.

**양이온은 산화수를 +1부터 +6까지** 훑었습니다. 산화수가 달라지면 전하를 맞추는 방법이
달라지니까, 이걸 안 훑으면 한쪽 전하만 보게 됩니다. **음이온은 계열 일곱 개**로,
결합이 제일 센 산화물부터 제일 무르고 큰 요오드까지 폈고요.

표가 그 결과입니다. 산화물이 37 개로 가장 많고, 나머지는 상당 부분 **대조군**이에요.
산화물만 넣으면 "산화물이라서 좋은 건지 그 원소가 좋은 건지" 를 가를 수가 없습니다.

하나 미리 말씀드리면 — **이미 존재하는 화합물만 넣을 수 있습니다.** 세상에 없는 걸
전구체로 쓸 수는 없으니까요. 그래서 목록이 **안전하고 익숙한 것들로 채워져 있고**,
이게 뒤에서 결과로 돌아옵니다.

💡 마지막 줄의 "세상에 없는 걸 전구체로 쓸 수는 없다" 를 빼지 말 것 — 편향이 게으름이
   아니라 **전구체를 단위로 잡은 것의 필연적 대가**라는 게 드러나야 방어가 된다.

---

### 8 — Candidate set on the periodic table

> ■ Candidate set (2): 36 cation elements, colored by their best score
> • Late transition metals (Fe–Cu) form the [빨강]red[/] block — their oxidation window is the narrowest.
> • [파랑]Group trends[/] are robust, the exact order is not — the same elements stay at both ends.

`< best score per element, 89-species pool (2026-08-13) >`
`해설` [빨강]no approved ranking yet[/] — the same elements stayed top and bottom when the set doubled (47 → 89)

⚠ **풀 교체 (2026-08-18)** — 색을 **89종 풀**(`cascade_v23_ranked_v2.csv`)로 다시 그렸다.
   앞 판은 47종(2026-06-29)이었다. 바꾼 근거는 **패턴이 안 바뀐다는 실측**이다:
   · 원소 집합 36개 **동일** · 상위10 집합 **동일** · 최하위10 집합 **동일**
   · Mn·Fe·Co·Ni·Cu 가 두 풀 모두 최하위12 안 — 대본이 "red" 라고 부르는 그 블록
   · 점수는 평균 **+0.050** 오르는데 이는 순위 변화가 아니라 min-max 정규화
     모집단이 커진 데 따른 **수평 이동**이다
   v2 는 v1 의 **완전한 상위집합**이다(v1 전용 종 0, +42종).
   ⚠ AlI₃ 는 **두 풀 모두** 없다 — v2 만의 결함이 아니라 캠페인 공백이다.
   이 일치는 `plot_seminar_2026_08.py --selftest` 가 검사한다 — 깨지면 위 캡션이
   거짓말이 되므로 그림보다 selftest 가 먼저 막는다.

**[60초]**

같은 목록을 주기율표에 올리면 이렇게 됩니다. 양이온 원소로 36 종입니다.

칸 색이 **그 원소의 화합물 중 가장 좋았던 종합 점수**입니다. 청록이 높고 붉은 쪽이
낮습니다. 아래 작은 숫자는 host 대비 안정성이고요.

가운데를 봐 주세요. **Fe, Co, Ni, Cu 가 통째로 붉습니다.** 이 넷이 36 개 원소 전체에서
제일 낮아요. 전이금속이라서 나쁜 게 아닙니다 — 오히려 1등과 2등이 **Sc 와 Cr** 로 둘 다
전이금속이에요. 갈리는 지점이 전이금속 **안**입니다. 왼쪽 early 쪽은 평균 0.61 인데
오른쪽 late 쪽은 0.34 예요.

이유는 **산화 창**입니다. d 오비탈이 차면서 환원이 쉬워지니까 버티는 전압 범위가 좁아집니다.
그래서 뒤에 나올 결과 2 — 후기 전이금속에서 산화 창이 붕괴한다 — 와 **같은 얘기**입니다.
반대로 Sc, Y, Gd 같은 3가 양이온과 In, Ga 쪽이 청록입니다.

⚠ 단서를 하나 달겠습니다. **아직 승인된 순위가 없습니다.** 그러니까 "Sc 가 1등"처럼
읽으시면 안 됩니다. 대신 **덩어리는 믿으셔도 됩니다.** 후보를 47 종에서 89 종으로
**두 배 늘려서 다시 매겨 봤는데, 위에 있던 원소도 아래에 있던 원소도 그대로**였어요.
점수만 평균 0.05 올라가고 순서는 안 흔들렸습니다.

즉 이 그림에서 신뢰할 수 있는 건 **화학군 단위의 패턴**이지 개별 순서가 아닙니다.

💡 **"late transition metals" 을 쓴 근거** (`db/properties/seminar_table_tm_split.csv`)

| d-블록 구간 | n | 평균 점수 |
|---|---|---|
| early (3–6족) | 11 | **0.609** |
| Mn (7족) | 1 | 0.459 |
| late (8–11족) | 5 | 0.338 |
| **late 3d 만 (Fe–Cu)** | 4 | **0.312** |

· **`transition metals` 라고만 쓰면 틀린다** — 전체 1·2등이 Sc 0.83 · Cr 0.82 로 둘 다
  전이금속이다. 갈리는 지점이 전이금속 **안**이라 `late` 가 문장의 핵심어다.
· `3d transition metals` 도 안 된다 — Sc·Ti·V·Cr 이 전부 3d 다.
· Cu 0.26 · Ni 0.29 · Co 0.32 · Fe 0.38 이 **36개 원소 전체의 최하위 4**다. 그다음이 Ti 0.41.

⚠ **Ag 를 조심할 것.** Ag 도 11족(late)인데 **0.44** 로 중간이다. 그래서 슬라이드가
  `late transition metals` 로 끝내지 않고 **`(Fe–Cu)` 로 범위를 박았다** — 주장이 정확한
  범위는 **3d 행**이다. 질문이 오면: "Ag 는 4d 라 다릅니다. 3d 행에서 8족부터 떨어집니다."
⚠ Mn(7족) 0.46 은 경계다. 그림에서도 붉지 않고 살구색이라 문장과 안 어긋난다.

💡 청중이 반드시 "그래서 Sc 를 쓰면 되나요"라고 묻습니다. 답은 "그 순위는 아직 승인 안
했습니다. 결과 1 을 보시면 왜 그런지 나옵니다"입니다. 미리 준비해 두세요.

---

### 9 — Substitution site and charge compensation  ✅ 확정 (2026-08-18, 2판)

> ■ Step 1: The substitution site is enumerated before a structure is built
> • Li, P, S and Cl are separate sublattices — an oxide has to take [파랑]one cation and one anion site[/].
> • A 2+ dopant on a Li site leaves extra charge — [빨강]each way of balancing it is a different structure[/].
> &nbsp;&nbsp;⚠ 이 줄은 PowerPoint 에서 **다시 타이핑하지 말 것** — 자동서식이 `2+` 를 위첨자로 올려 `A²⁺` 가 된다.

`< site preference vs ionic radius >`
`해설` only Si always takes the P framework; 19 of 26 always take Li — [빨강]6 switch with the doping level[/]
하단 용어 — Sublattice: equivalent positions of one element  ·  Charge compensation: adding or removing Li to keep the cell neutral  ·  bars = three doping levels, not repeat runs

⛔⛔ **2026-08-18 정정 — 앞 대본이 틀렸다.** 자세한 근거는
   `kb/results/site_preference_bar_meaning_2026_08_18.md`. 요지 셋:
   ① 막대는 **시드 재현이 아니라 세 도핑 수준**이다. 덱 캡션 "spread across our three
      runs" 는 틀렸다. 그래서 0 을 걸치는 막대는 잡음이 아니라 **자리가 바뀐다는 실측**이다.
   ② "아래로 내려간 게 셋 — Si, Ge, Sn" 도 틀렸다. **전 농도 P 는 Si 하나**이고
      Ge·Sn 은 바뀌는 쪽이다. 정산: **Li 19 · P 1 · 바뀜 6**(B·Al·Cr·Ge·Ni·Sn).
   ③ 미수렴 3건(Al x002 · Ag x002 · Ag x010)은 **지우지 않고 표시**했다(속 빈 회색 사각).
      dE 가 상한이라 지우면 Ag 평균이 +1.94 → +2.44 로 뛰어 실제보다 확실해 보인다.
⛔ **`x = 0.02 / 0.05 / 0.10` 숫자를 말하지 말 것.** 그건 폴더 라벨이다. 실측된 한 건은
   `Y2O3_x005` = 47원자에 Y 2개 = **P 자리의 33 %**. 다른 캠페인(cascade)에서는 같은
   라벨이 **전부 actual 0.25** 라 농도시리즈가 무효였던 전례도 있다. "세 도핑 수준" 으로만.

**[65초]**

첫 단계의 질문은 **"이 원소를 격자 어디에 넣을 수 있는가"** 입니다.

Li₆PS₅Cl 에는 Li, P, S, Cl 자리가 각각 있습니다. 산화물을 넣으면 금속은 양이온 자리로,
산소는 음이온 자리로 가야 하는데 **어느 자리로 갈지가 미리 정해져 있지 않습니다.**
전구체 하나를 넣는다는 게 자리를 **두 개** 정하는 일이 됩니다.

그림이 그걸 보여줍니다. 가로가 이온 반지름, 세로가 두 자리 사이의 에너지 차이입니다.
0 보다 위면 Li 자리, 아래면 P 골격이고요. **막대는 세 도핑 수준의 폭입니다** —
같은 계산을 세 번 돌린 게 아니라, 도핑을 묽게·중간·진하게 넣어 본 겁니다.

먼저 크기 얘기부터 하면, 오른쪽 큰 것들 — Ba, Na, Ag, Sr — 은 전부 위, **Li 자리**입니다.
Ba 가 +2.7 로 제일 확실하고요. 왼쪽 아래로 내려간 건 **Si 하나뿐**입니다. 4가이고 작아서
P 를 밀어내고 골격에 들어갑니다.

그런데 **가운데가 재미있습니다.** 속이 빈 것들 보이시죠. 이 여섯 개 — B, Al, Cr, Ge, Ni,
Sn — 은 **도핑을 얼마나 넣느냐에 따라 자리가 바뀝니다.** B 를 보면 묽을 때는 Li 자리인데
진해지면 P 로 갑니다. Sn 은 아예 왔다갔다 하고요.

⭐ 그러니까 **자리는 그 원소의 고정된 성질이 아닙니다.** 26 종 중 19 종은 늘 Li, 하나는
늘 P, 그리고 **여섯은 조건에 따라 다릅니다.** 이게 스크리닝을 자리마다 따로 돌려야 하는
이유예요.

그리고 여기서 두 번째 문제가 나옵니다. Mg 처럼 **2가 이온을 1가인 Li 자리에** 넣으면
플러스가 하나 남습니다. 셀을 중성으로 맞추려면 Li 를 하나 빼야 하는데, **어느 Li 를 뺄지가
정해져 있지 않습니다.** 방법마다 **다른 구조**가 되고요.

⭐ 그러니까 후보 하나가 구조 하나가 아닙니다. **자리 조합 × 전하 보상 방법** 만큼
불어납니다. 다음 장이 그 얘기고, 이게 **결과 1 로 돌아옵니다.**

💬 **말로만 (질문 오면)**
· 속 빈 **회색 사각**은 이완이 안 끝난 점입니다(3/78). 지우지 않고 남겼어요 —
  그 값이 상한이라 빼면 그림이 실제보다 확실해 보입니다.
· Y 는 전 농도에서 Li 자리입니다(+0.47 → +2.31 → +2.51, 단조). 문헌(Wang 2025)은
  Y 를 P(4b)로 보는데 **부호가 반대**고, 아직 결정 실험이 안 끝났습니다.
· Sn 과 Ni 는 반지름이 같은데(0.690) 방향이 반대입니다 — 크기만이 아니라 **원자가**도
  본다는 뜻이에요 (Sn⁴⁺ vs Ni²⁺).

---

### 10 — Candidate structure generation  ✅ 확정 (2026-08-18)

> ■ Step 2: Each allowed placement becomes a separate structure
> • One compound became [파랑]30 structures[/] on average, and 3,615 in total.
> • No site was assumed — every allowed placement was [파랑]built[/], and the ranking picked the winner.

`< where the anion landed  ·  structures per site pair >`
`해설` all nine site pairs were populated — [파랑]the site was never fixed by design[/]
하단 용어 — Configuration: one specific arrangement of atoms in the cell ·
　　　　　　 24g / 48h / 4b / 4a / 16e / 4d: Wyckoff labels for the sublattice positions

⚠ **왼쪽 그림 + 오른쪽 표 (2026-08-18)** — 왼쪽은 음이온이 앉은 자리(3 막대),
   오른쪽은 **(양이온 자리 × 음이온 자리) 3×3 표**다. 왼쪽만 있으면 "음이온 얘기" 로만
   읽혀서 Step 2 의 요점(자리 조합을 훑었다)이 안 보였다.
   ⚠ 9칸은 **confusion matrix 양식 그림**이다 (1저자 지정) — 칸 안에 수 + 비율 두 줄,
     컬러바, 축 제목. 표보다 '어느 조합이 두꺼운가' 가 즉시 보인다.
   ⚠ Origin 재작도용 CSV: `db/properties/seminar_table_anion_site.csv` (왼쪽 막대) ·
     `seminar_table_site_grid.csv` (오른쪽 표, 행·열 합계 포함).
⚠ 왼쪽 막대의 **부격자 이름이 빠져 있었다** (`set_yticks([])`). 막대 셋이 무엇인지
   화면만 봐서는 알 수 없었다 — 범주 라벨은 축 라벨이지 '그림 안 문장' 이 아니다. 복구함.

**[60초]**

두 번째 단계입니다. 앞 장에서 자리를 정할 수 없다고 했으니, **가능한 배치를 전부
만들어 버립니다.** 자리 조합마다 하나, 전하 보상 방법마다 하나씩입니다.

**얼마나 불어나냐면** — 화합물 하나가 평균 **30 개** 구조가 됐고, 다 합치면 **3,615 개**
입니다. 적은 건 15 개, 많은 건 150 개고요. 화합물은 90 종인데 구조는 삼천 개가 넘습니다.

오른쪽부터 보겠습니다. 세로가 **양이온이 앉은 자리**, 가로가 **음이온이 앉은 자리**입니다.
칸 안 숫자가 그 조합으로 만든 구조 수예요.

**아홉 칸이 전부 채워져 있습니다.** Li 24g 에 free sulfide 조합이 1,050 개로 제일 많고,
Li 48h 쪽은 100 개 남짓으로 적습니다. 그런데 **빈 칸이 없어요.** 자리 조합을 실제로 다
훑었다는 뜻입니다.

왼쪽은 음이온만 따로 센 겁니다. 할라이드 자리, 자유 황화물, PS₄ 모서리의 황 —
**세 부격자가 98·89·83 으로 거의 비슷하게 나눠 가졌습니다.** 한쪽으로 쏠리지 않았어요.

⭐ 여기서 짚고 갑니다. **어느 자리가 이길지는 저희가 정한 게 아닙니다.** 가능한 배치를
전부 만들어서 순위를 매겼고, 1등이 된 구조의 자리가 그 자리입니다. 앞 장에서 본 것처럼
자리가 농도에 따라 바뀌기도 하니까, **미리 정해 놓고 들어갈 수가 없었습니다.**

💬 **말로만 (질문 오면)**
· 두 그림의 **분모가 다릅니다.** 왼쪽(98·89·83)은 **최종적으로 뽑힌 구조**들이고,
  오른쪽(합 3,615)은 **만든 구조 전부**입니다. 같은 "음이온 자리" 를 세지만 다른 집합이에요.
· 오른쪽 숫자는 **구조 수**이지 화합물 수가 아닙니다. 화합물은 90 종입니다.
· 순위는 에너지 하나로 매긴 게 아니라 **종합 점수**입니다. 그 구성은 뒤 STEP 에서 나옵니다.

⛔ **말하지 말 것** — "제일 안정한 구조가 이겼다". 실측으로 챔피언이 최저 에너지인 경우가
   9건 중 1건뿐이다(2026-08-18 확인). 종합 점수로 뽑는다고 해야 맞다.

---

### 11 — Low-cost structure relaxation  ✅ 확정 (2026-08-18)

> ■ Step 3: Machine-learned potential screening before DFT
> • To relax 3,615 structures within budget, a [파랑]machine-learned potential[/] was used.
> • Structures were removed by [파랑]geometry, not by energy[/].

`< how far each structure moved  ·  the same structures on both screening axes >`
`해설` [빨강]100 of 3,615 changed by more than 25 %[/]; their energies look like the rest.
하단 용어 — Relaxation: moving atoms until the forces vanish ·
　　　　　　 MLIP: a fast stand-in trained on DFT forces

⭐ **오른쪽 그림이 이 장의 핵심 근거다 (2026-08-18 신설).** 앞 판은 히스토그램 하나뿐이라
   "왜 부피로 자르나, 에너지로 자르면 되지 않나" 라는 당연한 반문에 답이 없었다. 실측:
   · |ΔV| > 25 % 로 떨어뜨린 **100 개**와 에너지 상위 100 개는 **겹치는 것이 0 개**
   · 떨어진 것들의 에너지 중앙값이 오히려 **더 낮다** (−0.619 vs −0.480 eV/atom)
   ⇒ 에너지만 봤으면 **오히려 좋아 보여서 통과**했을 구조들이다. 부피 게이트가 독립적으로 일한다.
⚠ 세로축은 **이 스크린 안에서만** 비교 가능한 상대에너지다. 생성에너지도 hull 거리도 아니다.
⚠ 앞 판 슬라이드의 문제 — 빨간 줄이 `were droppe / d` 로 단어 중간에서 잘렸고,
   본문 밖에 문장 하나(`This stage answers one question…`)가 떠 있었다. 둘 다 정리.

**[65초]**

세 번째 단계입니다. 구조가 삼천 개가 넘으니 **DFT 로는 못 돌립니다.** 그래서 기계학습
퍼텐셜을 씁니다. DFT 힘을 학습한 모델이라 훨씬 빠르고, 구조를 이완시키는 데는 충분해요.

왼쪽이 그 결과입니다. 가로가 **이완하는 동안 셀 부피가 얼마나 움직였나**, 세로가 구조 수예요.
대부분 10–20 % 안에서 자리를 잡았습니다. 그런데 오른쪽 꼬리에 **25 % 를 넘어간 것들**이
있어요. 이건 이완이 아니라 **구조가 무너진 겁니다.** 3,615 개 중 **100 개**를 여기서 뺐습니다.

그러면 당연히 이런 질문이 나옵니다 — **"에너지로 자르면 되지 않나?"**

오른쪽 그림이 그 답입니다. 가로는 같고, 세로가 이번엔 **에너지**입니다. 붉은 점이 방금
뺀 100 개예요. **세로로 보면 파란 무리 한가운데 있습니다.** 에너지로는 평범해요. 오히려
중앙값은 **더 낮습니다.**

⭐ 점선이 **같은 개수를 에너지로 잘랐다면 어디였을지** 보여주는 선인데, 맨 위에 있죠.
   두 방법이 잡는 게 **완전히 다릅니다.** 겹치는 게 **하나도 없어요.**
   그러니까 **에너지만 봤으면 이 백 개는 오히려 좋아 보여서 그대로 통과했을 겁니다.**

⚠ 그리고 단서 하나. 세로축 에너지는 **이 스크린 안에서만** 비교되는 값입니다.
생성에너지도 hull 거리도 아니에요. "이게 몇 eV 니까 안정하다" 로 읽으시면 안 됩니다.

💬 **말로만 (질문 오면)**
· 25 % 는 물리 상수가 아니라 **저희가 정한 선**입니다. 분포에 꼬리가 끊기는 자리라 골랐어요.
· 이완 자체는 3,615 개 **전부 수렴**했습니다. 수렴 실패로 뺀 건 없습니다.
· 여기서 뺀 100 개는 "나쁜 물질" 이 아니라 **"이 모델로는 구조를 못 믿겠는 것"** 입니다.

---

### 12 — Representative structure selection

> ■ Step 4: One converged structure per candidate is carried forward
> • Structures were kept if they converged and the cell volume stayed within 25 %.
> • Candidate counts differ per compound, so this selection is not a ranking of elements.
`해설` on this axis the three runs agree — the bars are short

**[55초]**

이제 후보 하나당 대표 구조를 하나 고릅니다. 기준은 둘입니다. 수렴했는가, 그리고 부피가
25 % 안에 있는가. 부피가 크게 부는 건 물리가 아니라 계산이 잘못 간 신호일 때가 많습니다.

그림의 세로 막대가 같은 종을 세 번 돌렸을 때의 흩어짐입니다. 이 축에서는 막대가 짧습니다.
종끼리의 차이에 비하면 실행 간 차이가 작다는 뜻이고, 그러면 대표 하나를 골라도 됩니다.

⚠ 다만 후보 개수가 화합물마다 다릅니다. 다섯 개 중에 고른 것도 있고 오십 개 중에 고른
것도 있습니다. **이건 원소 순위가 아닙니다.**

---

### 13 — Thermal perturbation of the selected structure

> ■ Step 5: A short anneal tests whether the arrangement survives
> • To escape the nearest local minimum, each structure was heated briefly and relaxed again.
> • The trajectory is not an equilibrium structure and not a conductivity measurement.

`< energy gained by shaking the structure >`
`해설` every structure found a lower-energy arrangement once it could move

**[55초]**

구조 최적화는 가장 가까운 골짜기로 굴러떨어지는 것입니다. 처음 앉힌 자리 근처만 봅니다.
실제 합성은 열을 받으며 훨씬 넓게 돌아다니다 자리를 잡습니다.

그래서 짧게 흔들어 줍니다. 500 K 에서 50 피코초. 작은 언덕 하나를 넘을 만큼은 되고
후보 전체에 돌릴 만큼은 쌉니다. 그러고 다시 이완합니다.

그림이 그 결과입니다. 전부 왼쪽 — 음의 값입니다. **모든 구조가 움직일 기회를 주니까 더
낮은 배치를 찾았습니다.** 그만큼 처음 이완이 가까운 최소에 멈춰 있었다는 뜻입니다.

⚠ 50 피코초는 합성 시간이 아닙니다. 평형 구조라고 주장할 수 없고, 전도도 계산도
아닙니다.

---

### 14 — Static lithium transport pathway

> ■ Step 6: The Li energy landscape is mapped on the annealed geometry
> • To flag transport risk without dynamics, a bond-valence landscape was computed.
> • Low-energy valleys are structural pathways, not diffusion coefficients.
`해설` valleys are low-energy regions, not verified channels

**[65초]**

이온 전도체이니 결국 궁금한 건 "Li 가 잘 다니는가"입니다.

제대로 하려면 MD 로 실제 이동을 재야 하는데 후보 하나당 며칠입니다. 그래서 이 단계에서는
**지도만 그립니다.**

결정 안을 촘촘한 격자로 쪼개고 각 점마다 "여기 Li 가 있으면 주변 결합이 얼마나
어긋나는가"를 계산합니다. 그러면 그림처럼 골짜기와 고원이 나옵니다. 파란 골짜기가 Li 가
편한 곳, 붉은 고원이 넘기 힘든 곳입니다. 그다음 **낮은 골짜기가 결정 이쪽 끝에서 저쪽
끝까지 이어지는지**를 봅니다. 그리고 도펀트가 그 길목에 앉아 통행을 막는지도 셉니다.

⚠ 이건 구조적 경로입니다. 확산계수도 전도도도 아닙니다. 골짜기가 이어져 있어도 실제로
잘 다닌다는 보장은 없습니다.

💡 질문이 가장 많이 나오는 장입니다. "Li 길이 넓다"는 표현을 쓰실 거면
"Li 가 넘어야 하는 언덕이 낮고, 그 낮은 구간이 끊기지 않는다"로 풀어 주세요.

---

### 15 — Mechanical response of the doped lattice

> ■ Step 7: Stiffness and compressibility are obtained from finite strains
> • To assess particle contact under stack pressure, elastic moduli were computed.
> • The DFT comparison shown here is a single case, not a pool-wide validation.
`해설` a single case — not a pool-wide DFT validation

**[55초]**

전고체전지는 액체가 없어 입자끼리 직접 붙어야 합니다. 그래서 기계 물성이 성능에 바로
들어옵니다.

너무 딱딱하면 압력을 걸어도 입자가 붙지 않고 틈이 남습니다. 너무 무르면 층이 흐릅니다.
그리고 충방전으로 부피가 변할 때 잘 늘어나면 균열이 덜하고 잘 깨지면 금이 갑니다.

그래서 부피를 조금씩 바꿔 에너지를 재고, 여러 방향으로 작은 변형을 줘 딱딱함과 연성을
구합니다. 그림이 그중 한 사례를 DFT 로 맞대 본 것입니다.

⚠ **한 건 검증입니다.** 91 종 전부를 DFT 로 확인한 것이 아닙니다.

---

### 16 — Electrochemical stability window

> ■ Step 8: The oxidation onset from a grand-potential construction
> • To locate decomposition, the Li chemical potential was scanned as a voltage axis.
> • The result is 0 K bulk thermodynamics — not a rate, and not a passivation prediction.

`< stability window of every candidate >`
`해설` five candidates lose the window entirely — all late transition metals

**[65초]**

앞의 문제 지도에서 첫 칸이 "양극 쪽 산화"였습니다. 그걸 여기서 봅니다.

전압을 올린다는 건 전기화학적으로 Li 를 빼내는 것과 같습니다. 그래서 Li 를 조금씩 빼면서
매 지점마다 "이 조성이 그대로 있는 게 유리한가, 다른 상들로 쪼개지는 게 유리한가"를
계산합니다. 쪼개지는 쪽이 유리해지는 전압이 산화 한계입니다.

그림에서 막대 하나가 후보 하나이고, 막대 길이가 **아무 일도 일어나지 않는 전압 구간**
입니다. 점선이 도펀트 없는 host 의 산화 지점입니다.

아래쪽 붉은 다섯 개가 **창이 아예 사라진 후보**입니다. 전부 후기 전이금속인데, 이건
한계가 옮겨진 게 아니라 붕괴입니다.

⚠ 이건 0 K 벌크 열역학입니다. 분해가 가능하다는 것만 말하지, 얼마나 빨리 분해되는지도
분해층이 덮고 멈추는지도 말하지 않습니다.

💡 "실험 CV 에서는 왜 3 V 넘게 버티나"가 반드시 나옵니다. 답은 "열역학은 가능하다고
하지만 실제로는 분해층이 덮어 느려지기 때문"입니다.

---

### 17 — Calculations that were not performed

> ■ Step 9: Two designed stages produced no evidence
> • Conductivity from dynamics — days per candidate; Step 6 stands in as a proxy.
> • The cathode interface — not attempted; the figure shows what such a screen looks like.

**[70초]**

솔직하게 말씀드릴 부분입니다. **설계에 있었는데 돌리지 못한 계산이 둘 있습니다.**

하나는 진짜 전도도입니다. Step 6 은 지도만 그린 것이라 상위 후보에는 MD 를 돌려 실제
확산을 재려 했습니다. 후보 하나당 며칠 걸리는 계산인데 결국 못 돌렸습니다. 그래서 오늘
전도도 얘기는 전부 구조 프록시입니다.

또 하나는 계면입니다. 도핑한 전해질이 양극과 만나면 무슨 일이 나는지 — 손도 못 댔습니다.

이 그림이 그게 왜 중요한지 보여줍니다. 같은 산화물 코팅을 네 계면에서 각각 계산한 건데,
주기율표 네 장이 서로 다르게 칠해져 있습니다. 전해질 쪽에서 진초록이던 원소가 음극
쪽에서는 허옇습니다. **같은 물질인데 어디서 보느냐에 따라 답이 바뀝니다.**

저희는 저 네 장 중 한 장도 그리지 않았습니다.

---


## ⑤ 결과

### 18 — Inventory of available evidence

> ■ Result summary: The screen is broad in structure and thin in transport
> • Structures, relaxation, anneal, Li maps, mechanics and oxidation windows all exist.
> • Conductivity, explicit interfaces and pool-wide DFT confirmation do not exist.

`[표]` what / how many of 270 / status

**[50초]**

정리하면 이렇습니다. 표 위쪽 여섯 줄이 **파란 글씨, 있는 것**입니다. 구조, 이완, 어닐,
Li 지도, 기계 물성, 산화 창 — 270 슬롯 전부 있습니다.

아래 두 줄이 **붉은 글씨, 없는 것**입니다. 진짜 전도도와 계면 — 0 입니다.

그리고 없는 건 없는 겁니다. 프록시가 순서를 바꿀 수는 있어도 답을 대신할 수는 없습니다.

💡 이 장은 짧게 지나가되 마지막 문장은 또박또박 말하세요. 뒤의 결과 세 장을 어디까지
읽어야 하는지가 여기서 정해집니다.

---

### 19 — Effect of structural identity on the measured value

> ■ Result 1: The dopant name did not define a controlled comparison
> • Across the three runs, 59 of 90 species kept one exact formula and 31 did not.
> • Where the site moved the value moved with it, so averaging mixes different materials.

`< spread of the three runs, species by species >`
`해설` one species over three runs spans as much E as thirteen species

`[표]` axis / unit / within one species / across species / ratio / read as

**[70초]**

첫 번째 결과이자 가장 뼈아픈 결과입니다.

후보 하나를 세 조건으로 돌렸습니다. 처음엔 이걸 농도 세 점이라고 생각했는데, 셀이 작아
세 조건이 전부 같은 치환량으로 반올림돼 있었습니다. 농도 축이 아니었습니다.

더 중요한 건 그다음입니다. 90 종 중 **59 종만 세 조건의 화학식이 같고 31 종은 조건마다
화학식이 달랐습니다.** 전하 보상 방법이 달라지며 Li 개수가 바뀐 겁니다. 그러니까 세 개를
평균 냈는데 사실 서로 다른 조성 세 개를 평균한 셈입니다.

그림이 그 크기입니다. 회색 막대 하나가 한 종의 세 실행이 벌어진 폭인데, **막대 하나가
서로 다른 열세 종을 담을 만큼 넓습니다.**

아래 표에서 맨 오른쪽 칸을 봐 주세요. **안정성과 Pugh 비는 파랑 — 화학이 이깁니다.**
그런데 **탄성률과 Li 길 지표는 빨강 — 자리가 이깁니다.** 전부 못 믿는 게 아니라 어느
축을 못 믿는지를 알게 된 겁니다.

---

### 20 — Dependence of oxidation onset on dopant chemistry

> ■ Result 2: Sulfur sets the limit; shifts away from it are conditional
> • The valence-band edge is sulfur, so sulfur is oxidised first regardless of the dopant.
> • Late transition metals are the clear loss: the window collapses rather than shifting.

`< valence band edge of the host >`

`< onset by dopant chemistry >`

`[표]` dopant chemistry / n / median onset (V) / range (V) / windows lost

**[65초]**

두 번째는 산화입니다. 왼쪽 그림이 배경입니다.

가장 위에 차 있는 전자 — 그러니까 먼저 뺏길 전자가 **황**에서 옵니다. Cl 은 그보다
아래입니다. 그래서 무엇을 넣든 **먼저 산화되는 건 여전히 황**입니다. 문헌에서 확립된
얘기이고 저희 계산도 같은 답을 줍니다.

오른쪽이 저희 결과입니다. 대부분이 점선 근처, 즉 host 값에 몰려 있습니다. 표를 보시면
주족·알칼리토·알칼리는 중앙값이 셋 다 2.140 으로 **host 와 같습니다.**

눈에 띄는 건 전이금속입니다. 표 맨 오른쪽 "창을 잃은 개수"가 **전이금속만 5**이고 나머지는
전부 0 입니다. 조금 옮겨진 게 아니라 손해입니다.

⚠ 위로 올라간 예외 몇 개는 **아직 특정 원소 덕이라고 말하지 못합니다.** 같은 자리라도
전하 보상 방법에 따라 부호가 뒤집힙니다. 결과 1 이 정확히 그 얘기였습니다.

💡 예전에 "B₂O₃ 가 산화 한계를 0.18 V 올린다"고 말한 적이 있고 그건 철회했다고 덧붙이면
발표가 단단해집니다. 이 발표의 결론이 "자리를 고정하지 않으면 원소 효과를 말할 수 없다"
라서 오히려 가장 센 근거가 됩니다.

---

### 21 — Trade-off between stability and lithium transport

> ■ Result 3: Lattice stabilisation and Li mobility oppose each other
> • Across our candidates the two axes correlate negatively — the trend is not noise.
> • The same trade-off appears in the literature for an unrelated material set.

`< stability against blocked Li traffic >`
`해설` the more a dopant stabilises the lattice, the more Li traffic it blocks (r = −0.63)

**[60초]**

세 번째는 더 일반적인 얘기입니다. **공짜가 없더라**는 것.

왼쪽이 저희 후보입니다. 가로가 host 대비 안정성, 세로가 도펀트가 Li 자리를 얼마나
막는지입니다. **격자를 안정시키는 도펀트일수록 Li 길을 더 막습니다.** 상관이 −0.63 이고
추세가 분명합니다.

오른쪽은 남의 데이터인데 같은 얘기를 합니다. Xiao 가 411 개 산화물에서 잰 건데, Li 가
많을수록 산화에 약합니다. 그런데 Li 가 많아야 이온이 잘 다니고요.

재료도 축도 다른데 **모양이 같습니다.** 하나 얻으면 하나 잃는 구조입니다.

💬 그래서 오늘 결론이 "몇 번이 1 등"이 아닙니다. 이 그림 위에서는 1 등이 정의되지
않습니다. 어느 축을 얼마나 포기할지를 먼저 정해야 합니다.

---


## ⑥ 다음 판

### 22 — Design of the next campaign

> ■ Future work (1): Control is strengthened before scale is increased
> • To separate chemistry from placement, the formula and site will be frozen before repeats.
> • Real low concentrations require larger cells; only boundary cases are promoted upward.

**[65초]**

다음 판은 셋입니다.

첫째, **자리와 화학식을 고정합니다.** 지금은 한 후보 안에 자리도 전하 보상도 섞여
있습니다. 같은 자리, 같은 처방으로 맞춘 뒤 원소만 바꿔야 원소 효과를 말할 수 있습니다.
결과 1 이 그대로 다음 실험 설계가 됩니다.

둘째, **셀을 키웁니다.** 큰 셀에서 목표 농도를 정수로 구현하면 그때 진짜 농도 축이
생깁니다. 비싸지지만 후보를 좁힌 다음에 하면 됩니다.

셋째, **경계에 걸린 후보만 위로 올립니다.** 확실히 좋거나 확실히 나쁜 건 더 볼 필요가
없습니다.

💬 그리고 목록이 안정한 화합물 쪽으로 치우쳐 있다고 했죠. 실제로 열역학 안정성으로
걸러 봤더니 **아무도 안 떨어졌습니다.** 기준이 잘못된 줄 알았는데 아니었습니다. 게이트가
일을 하게 하려면 위험한 후보도 목록에 넣어야 합니다.

---


## ⑦ ML

### 23 — Use of the data for machine learning

> ■ Future work (2): The data schedules calculations, not replaces them
> • 90 candidates give about 4,000 pairs — not computable, but rankable for prioritisation.
> • Trained on today's data a model would also learn our placement noise; Result 1 comes first.

**[60초]**

이 데이터의 진짜 쓸모는 순위표가 아니라 **학습 데이터**라고 봅니다.

후보마다 산화 창, 안정성, 기계 물성, Li 길이 한 세트로 있습니다. 이게 수십 종 있으면
어떤 원소 성질이 어떤 축을 움직이는지 학습시킬 수 있습니다.

왜 필요하냐면 **두 원소를 같이 넣는 경우** 때문입니다. 후보가 90 개면 둘씩 조합이 사천
가지가 넘습니다. 전부 계산할 수 없습니다. 그런데 단일 도펀트로 학습한 모델이 있으면
유망한 것부터 계산할 수 있습니다.

⚠ 다만 순서를 지켜야 합니다. **지금 데이터로 학습하면 결과 1 의 자리 섞임까지 같이
배웁니다.** 그러면 모델이 원소 효과가 아니라 저희 생성기 버릇을 배웁니다. 자리 고정이
먼저이고 학습이 다음입니다.

💬 그림에서 세로축 확률만 보면 안 됩니다. 가로축이 훈련 데이터에서 얼마나 멀리 떨어져
있느냐인데, 멀리서 자신 있게 틀리는 게 이런 모델의 전형적인 실패입니다.

---


## ⑧ Discussion

### 24 — Discussion

> ■ Open questions for the group
> • What exists is a map of where the comparison is reliable, not a shortlist.
> • The next decision is which expensive calculation reduces uncertainty the most.

**[60초]**

정리하면, 이번에 얻은 것은 후보 하나가 아니라 **비교가 어디서 흔들리는지에 대한
지도**입니다. 그리고 지금 없는 것은 shortlist 인데, 저는 그걸 발표하기보다 제대로
얻고 싶습니다.

여쭙고 싶은 게 넷 있습니다.

하나. 다음에 무엇을 먼저 할까요. 자리를 고정한 농도 시리즈일지, 첫 계면 계산일지.

둘. "가장 좋다"를 무엇으로 정의할까요. 가장 좋은 한 구조인지, 다시 만들어도 살아남는
후보인지.

셋. 몇 번 반복해야 충분할까요. 자리 몇 개, 시드 몇 개.

넷. 이게 가장 궁금한데요. 계면을 보지 않은 상태에서 벌크 결과만으로 실험에 후보를
넘기는 게 의미가 있는지, 아니면 계면까지 봐야 넘길 수 있는지.

감사합니다.

---


## 부록 (질문 나올 때만)

### 25 — Experimental counterpart in a garnet electrolyte

> ■ Appendix A1: The same survey performed by synthesis
> • 59 dopants were synthesised and measured — the closest experimental analogue.
> • 32 of our 36 cation elements also appear in that study.

**[질문 시에만]**

LLZO 에 도펀트 59 종을 **실제로 합성해** 전도도와 전기화학 창을 전부 측정한 연구입니다.
저희 계산판의 실험 버전이고 체급도 비슷합니다. 저희 양이온 36 종 중 32 종이 이 표 안에
있습니다. 노란 칸이 이 논문에서 처음 시도한 원소입니다.

💬 이 사람들도 **어느 자리에 들어가는지를 계산으로 먼저 정하고** 실험했습니다. 자리 문제가
실험에서도 그만큼 크다는 뜻입니다.

---

### 26 — Mapping of talk steps onto the executed workflow

> ■ Appendix A2: Nine questions, and where each one was answered
> • Each talk step is named by the question it answers; folders are named by what ran.
> • Two designed stages produced no evidence and are marked not run.

**[질문 시에만]**

본문에서 아홉 개 질문으로 묶었지만 실제 실행 폴더는 더 잘게 나뉩니다. 이 표가 둘을
연결합니다. 9 번이 붉은 건 설계에는 있었지만 돌리지 않은 것입니다.

---

### 27 — Interpretation of the three campaign labels

> ■ Appendix A3: The labels are neither concentrations nor repeats
> • All three collapsed to the same substitution in a small cell — no concentration axis.
> • Regrouping by exact formula gives 59 same-formula and 31 changed-formula species.

**[질문 시에만]**

세 라벨이 왜 농도도 반복도 아닌지의 상세입니다. 셋 다 작은 셀에서 같은 치환량으로
뭉개졌고, 화학식 기준으로 다시 묶으면 59 종은 같고 31 종은 다릅니다.

앞으로는 **화학식·자리를 고정하고 시드만 바꾸는 반복**과, **셀 크기를 바꿔 만드는 농도
축**을 분리해야 합니다.

---

### 28 — Boundaries of each computational method

> ■ Appendix A4: Every method named by the question it can answer
> • The left column is what the method answers; the right is what it is assumed to answer.
> • Every entry on the right is a calculation that has not been run.

**[질문 시에만]**

발표에서 쓴 방법을 "무슨 질문에 답하는가"로 정리한 표입니다. 화살표 왼쪽이 그 방법이
답하는 것, 오른쪽이 사람들이 답한다고 오해하는 것입니다. 오른쪽은 전부 아직 돌리지 않은
계산입니다.

---

### 29 — Full candidate roster

> ■ Appendix A5: All 91 compounds, grouped by anion family
> • Every compound that entered the campaign is listed — this is the denominator.
> • As₂S₃ was planned but stopped during structure generation.

**[질문 시에만]**

캠페인에 들어간 91 개 화합물 전부입니다. 계열별로 상자에 넣었습니다. **이게 분모입니다.**
발표에서 말한 비율은 전부 이 목록 기준입니다.

As₂S₃ 하나는 계획에는 있었지만 구조 생성 단계에서 멈췄습니다.

---

## 발표 전 점검

- 빨간 글씨에서 쉰다. 파란 글씨에서 목소리를 올린다.
- 16장(못 한 것)과 17장(있는 것/없는 것)은 한 호흡으로 묶는다.
- 8~16장은 레이아웃이 반복된다. 리듬이 생기니 장당 50~60초로 짧게 끊는다.
- 부록은 넘기지 않는다. 질문이 나올 때만.
- 예상 질문 3순위: ① Li 길이 뭔가(13장) ② 실험 창은 왜 더 넓나(15장)
  ③ 그래서 뭘 쓰면 되나(20·23장 — "지금은 못 정합니다"가 정답)

## Origin 용 CSV

| 슬라이드 | CSV |
|---|---|
| 6 후보군 | `db/properties/seminar_table_roster.csv` |
| 8 주기율표 근거 | `db/properties/seminar_table_tm_split.csv` |
| 9 자리 선호 | `db/properties/seminar_table_site_preference.csv` |
| 10 음이온 자리 · 자리 격자 | `db/properties/seminar_table_anion_site.csv` · `seminar_table_site_grid.csv` |
| 풀 정산 91→89 | `db/properties/cascade_pool_accounting.csv` |
| 17 있는 것/없는 것 | `db/properties/seminar_table_evidence.csv` |
| 18 결과 1 | `db/properties/seminar_table_label_spread.csv` |
| 19 결과 2 | `db/properties/seminar_table_oxidation_by_group.csv` |
| 18 그림 원자료 | `db/properties/cascade_label_spread_E_young.csv` |

그림은 전부 `python3 tools/figures/plot_seminar_2026_08.py` 로 재생성.
**그림 안에는 글을 넣지 않는다** — 문구는 슬라이드의 `< >` 이름표와 그 밑 해설 줄이 진다
(도구 selftest 가 `ax.text`·`ax.annotate` 사용을 위반으로 잡는다).
