---
title: "연구세미나 2026-10-13 — cascade 진행 브리핑 발표 대본 (장별)"
date: 2026-10-12
updated: 2026-10-15
tags: [seminar, cascade, script, briefing]
status: 진행
kind: seminars
system: cascade
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# 발표 대본 — 2026-10-13 연구세미나 (약 22 분 · 10-14 8장 · 14장 보강으로 +45 초)

> 덱: `kb/seminars/Research_Seminar_2026_10_13_cascade_progress.pptx` · **슬림판** `…_progress_lean.pptx` (같은 19장 · 같은 순서) · 흐름: `…_storyline_ko.md` · 질문 대비: `…_defense_ko.md`
> 슬림판으로 발표하면 이 대본을 그대로 쓰고, 화면에서 빠진 세부는 말로 한다 — 맨 끝 **§슬림판으로 발표할 때** 표.
> 표기: **[클릭]** 화면 넘김 · **[가리킴]** 그림이나 표 짚기 · ⏱ 누적 시간.
> 말투는 발표체(합니다)다. 숫자는 슬라이드에 있는 것만 읽는다. 없는 숫자는 질문이 와도 디펜스 문서의 '숫자 카드' 안에서만 답한다.
> ⚠ 2026-10-12 갱신: 원장 정독 뒤 **11장(September audit)을 새로 넣었다** — 그 뒤 장 번호가 하나씩 밀렸다 (19장). 옛 판의 "91개 중 89개 · 3,615" 는 틀렸다 (8월 재실행으로 91 전부 · 3,675).


> ### 🗂 장별 확정 현황 — 사용자와 한 장씩 보며 확정 (10-13 · *"대본들 계속 누적해서 마지막에 정리해서 줘"*)
> 확정된 장만 이 파일의 해당 절이 **최종본**이다. 나머지 절은 옛 판이라 그 장을 볼 때 다시 쓴다.
> 마지막에 주는 것: ① 장별 **[스토리라인 한 줄 + 대본]** 한 파일 (내부 메모 · 원장 괄호는 빼고 발표용으로) ② 덱 전체 슬라이드 노트에 같은 대본.
> 사용자 덱은 슬림판보다 한 장씩 뒤다 (앞에 한 장이 더 있다 · Overview = 사용자 4쪽).
> 장 제목은 08-18 덱 순서 그대로다 — 4–5장 *Introduction* → 6–13장 *Results & Discussion* (사용자 10-13 · 'Approach' · 'Progress' 를 되돌림) · 14장 *Plan* (사용자 10-16 자기 판 · ■ Future plans) · 15장 *Results & Discussion* (■ Discussion points) · 요약 장 없음 (사용자 10-16).
>
> | 슬림판 장 | 내용 | 상태 | 확정 커밋 |
> |---|---|---|---|
> | 2 | Background — Earlier DFT studies | ✅ 확정 10-13 | 6e568c4 · e70e1d6 (Li₂S 칸 = li2s/LPSCl 계면상) |
> | 3 | Overview — 하나씩에서 여럿으로 · 예 하나 (Al₂O₃ / Al₂S₃) | ✅ 확정 10-13 | b464c62 · fa4a120 · 9b4f498 (화살표 줄 → 다음 장 다리 · 'we must check') · 한 장 PPT + 노트 |
> | 4 | Introduction — 두 열화는 서로를 키운다 (Kang 2026 Fig. 16) | ✅ 확정 10-13 (*'됐어 저정도면'*) | 9c4bbde (문구 넷 · 출처는 랩 표준 그대로) |
> | 5 | Introduction — 선행 스크린과 이번 작업 (novelty · Muy 2025 · Jung 2026 추가) | ✅ 확정 10-13 (사용자 최종판 · 출처 오른쪽 위) · 논문별 원문 대조 뒤 재확정 (Miara n 128 · Lee 칸 · bullet 둘 · Anderson 참고문헌 뺌 · 'gate' 뺌) · **대본 최종 10-13** (기계 축 이유 한 줄) | 34adf6e · 이번 반영 커밋 · 디펜스 S5 브리핑 (Miara · Xiao · Lee 확인 ✅ · Muy · Jung 남음) |
> | 6 | Results & Discussion — 91 전구체 · 일곱 음이온족 (08-18 표로 되돌림 · 셋째 열 *anion vs host*) | ✅ 확정 10-13 (사용자 최종판 · 제목 Results & Discussion · 열 이름 *anion vs host* — 덱의 다른 'vs' 처럼 마침표 없음) | a2b62c9 · d936867 · 한 장짜리 PPT |
> | 7 | Results & Discussion — Stage 1 파이프라인 (점선 박스 다섯 단계) + 8월 방법 점수 상위 10 (91 개) | ✅ 확정 10-14 (사용자 'ㅇㅇ 진행해' · '틀린거라도 랭킹 한번 추가' · '옆에 plot' · 다음 장 = 감사) | 이번 커밋 |
| 1 · 8–19 | 나머지 — ⚠ 10-14 순서 바뀜: 8 감사 · 9 배치 표본 · 10 DFT 기준 · 11 안정창 (사용자 '감사를 8장으로, 세부 셋은 근거로') | ⏳ 그 장을 볼 때 확정 | — |

---

## 1. 표지 ⏱ 0:30
안녕하십니까, 안용훈입니다. 오늘은 Li₆PS₅Cl 도펀트 스크리닝의 **진행 상황과 앞으로의 계획**을 말씀드리겠습니다.
오늘 말씀드릴 것은 결과가 아닙니다. **시뮬레이션을 어떻게 돌렸고, 그걸 보고 무엇을 바꿨고, 지금 무엇이 돌고 있고, 무엇을 위해 돌리는지**입니다.

**[클릭]**

## 2. Background — 지금까지의 DFT ⏱ 3:00
> 화면 (사용자 10-13 최종): ■ *Earlier DFT studies: the basis of this screening* · bullet 둘 (Top row · Bottom row) · 칸 여덟에 옛 그림.
> 숫자는 하나도 읽지 않는다 — 칸 그림에 숫자가 보여도 (Nd · B₂O₃ · Li₃N · 접착) 읽지 않는다.

먼저 이번 스크리닝의 바탕이 된, 지금까지의 DFT 계산을 정리하겠습니다.

**[가리킴: 윗줄]** 윗줄은 벌크 재료와, 도핑이나 코팅으로 그 재료를 바꾼 계산입니다.
- 기준 조성 Li₆PS₅Cl 의 밴드갭, 상태방정식, 탄성을 계산해서 모든 도핑 모델의 기준선으로 씁니다.
- Nd/O 공치환은 실험팀과 함께 봤습니다. **[가리킴: 칸 안 왼쪽 → 위 → 아래]** 왼쪽이 양극 계면 모델, 위가 밴드 엣지를 본 상태밀도, 아래가 결합 분석입니다.
  (⚠ 피크 · 값은 읽지 않는다 — 실험 쪽 1저자 원고 · 질문은 디펜스 S2)
- B₂O₃ 와 산소 도핑에서는 상태방정식, 결합원자가 지형, MLIP 분자동역학을 한 계에 묶어 봤고, 이 계에서 MD 프로토콜을 처음 짰습니다.
  (칸 그림에 아레니우스 그래프가 들어간다 — 사용자 10-13 결정. 숫자 · 두 선의 비교는 읽지 않는다.)
- h-BN 을 입힌 탄소섬유에서는 Li 흡착과 이동 장벽, 층수 효과를 계산했습니다.

**[가리킴: 아랫줄]** 아랫줄은 셀 안에서 전해질이 만나는 것들입니다.
- SEI 성분인 Li₃N 은 Li 흡착과 이동 장벽을 NEB 로 계산했습니다. 범용 MLIP 가 이 계에서 치우친다는 걸 확인해서 DFT 로만 계산합니다.
- Li₂S 칸은 Li₂S 양극을 Li₆PS₅Cl, 탄소와 함께 볼밀링할 때 생기는 비정질 계면상입니다. 녹였다 식혀 만든 작은 유리 모델에서 MLIP 분자동역학으로 Li 이동을 보는 공동 연구이고, 포텐셜은 DFT 힘과 비교해 확인했습니다.
  (사용자 10-13: 이 칸 = **li2s/LPSCl 계면상 트랙** — SEI 성분 Li₂S 의 공공 NEB 가 아니다 (10-12~13 에 내가 그렇게 잘못 매핑했다). ⚠ 트랙 li2s · 판정은 공동연구 제1저자 (외부) · 해석 잠정 — 확산계수 · 전도도 · 활성화에너지 · 장벽 · *'이 상이 실제로 생긴다 / 성능을 살린다'* · *'이 온도에서 확산하지 않는다'* 는 말하지 않는다. 허용 문장 = `db/properties/li2s_brief_2026_09_28.json` `can` · 마감 `lpscl_smallcell_glass_md_closed_2026_09_30.json`)
- 계면 접착은 제가 공저자로 참여한 ACS Nano 논문에서 계산했습니다. 다섯 조성의 계면 결합 곡선에서 접착 일을 구했습니다.
  (그림 = Lee et al., ACS Nano 2026, Fig. 6 · 실린 값이지만 여기서는 읽지 않는다)
- 바인더는 SDCP 분자의 흡착을 스핀 상태별로 계산했고, 무엇을 잴지 먼저 정해야 값이 정의된다는 걸 여기서 배웠습니다.
  (⚠ 'PTFE 보다 잘 붙는다' · 수소결합 같은 접촉 기전은 말하지 않는다 — SDCP 마감 카드: 비교 보류 · 접촉 기전 철회)

**[마무리]** 이 경험들이 오늘 스크리닝의 단계가 됐습니다. 상태방정식은 기준 계산으로, 결합원자가 지형은 Li 지형 지표로, MD 는 수송 계산으로, 대권위 상도표는 안정창으로, 계면 에너지는 계면 반응성으로 이어집니다.
그 위에서 지금 하고 있는 일을 다음 장에서 말씀드리겠습니다.

**[클릭]**

## 3. Overview ⏱ 4:30
> 화면 (사용자 10-13 · 질문으로 다시 짬 · 콜론 줄 없앰): ■ *Choosing a dopant precursor for Li₆PS₅Cl* · bullet 둘 (*In the lab, dopants are added as compounds, not as bare elements.* · *This work screens 91 candidate precursors by simulation before synthesis.*) ·
> 점선 상자 *An example* — Al₂O₃ → Al + O / Al₂S₃ → Al + S } *Same Al, different partner anion* · *Does the anion change stability or Li transport?* ·
> 화살표 · 아래 줄 *To answer this question, we must check electrochemical stability, mechanical stability, and Li transport separately.*
> 아래 줄은 다음 장 (실패 모드 · *'evaluated separately'*) 으로 넘어가는 다리다 (사용자 10-13 — 옛 줄 'This talk covers …' 는 화살표와 안 맞았다).
> 상자는 **예 하나**다 (사용자 10-13 *'이건 하나의 예인거지?'*) — 1단계는 91 개 전부 · 2단계 설계 목록은 237 · Al₂O₃ 대 Al₂S₃ 는 MD 방법을 먼저 시험하는 파일럿 쌍.
> 왜 바꿨나: 사용자 10-13 *"너무 단조롭다 · 다 밝히고 하는 건 별로 · 기대를 가질 만하고 집중할 수 있는 페이지"* — 단계 상자 · 진행 숫자는 뒤 장 (11 감사 · 13 파일럿 · 15 요약) 으로.
> 말하는 흐름 (사용자 10-13 *"이런 dopant 치환을 진행하다 보니 범위를 높여 여러 도펀트를 lpscl 에 치환한 것에 관심을 갖게 되었다"*):
> 앞 장의 도핑 계산 → 범위를 넓히고 싶어짐 → 넓히려니 넣는 건 화합물 → 91 개 → 예 · 질문 → 답하려면 세 가지를 따로 → 다음 장. 화면을 위에서 아래로 읽는 순서와 같다.
> ⚠ 시기를 못 박지 않는다 — 1단계 (6–8월) 는 B₂O₃ · Nd 계산과 시기가 겹친다. '끝내고 나서' 가 아니라 '하나씩 하다 보니'.
> (사용자 덱에서는 4쪽 — 앞에 한 장이 더 있다.)

앞에서 보신 것처럼, 지금까지는 Nd 나 B₂O₃ 같은 도펀트를 하나씩 계산해 왔습니다.
하나씩 하다 보니, 범위를 넓혀서 여러 도펀트를 Li₆PS₅Cl 에 넣어 보면 어떨까 하는 데 관심이 생겼습니다.

**[가리킴: 첫 bullet]** 그런데 여러 도펀트를 넣으려고 보니, 실험에서는 도펀트를 원소가 아니라 화합물로 넣습니다.

**[가리킴: 둘째 bullet]** 그래서 이번 작업은 원소 대신 그 화합물, 즉 전구체를 단위로 잡고, 후보 91개를 합성하기 전에 계산으로 먼저 걸렀습니다.

**[가리킴: 상자 왼쪽]** 예를 하나 들겠습니다. Al 을 넣는다면 Al₂O₃ 를 넣을 수도 있고, Al₂S₃ 를 넣을 수도 있습니다. Al₂O₃ 에는 산소가, Al₂S₃ 에는 황이 따라옵니다.

**[가리킴: 상자 오른쪽]** 같은 Al 인데 따라오는 음이온이 다르면, 전해질의 안정성이나 Li 이동도 달라질까요?
이런 질문을 전구체 하나하나에 던질 수 있고, 바로 이 Al₂O₃ 와 Al₂S₃ 쌍이 지금 첫 시험으로 돌리고 있는 계산입니다.

**[가리킴: 아래 줄]** 이 질문에 답하려면 전기화학 안정성, 기계적 안정성, 그리고 Li 이동을 반드시 따로따로 봐야 합니다.
왜 따로 봐야 하는지부터 보겠습니다.

**[클릭]**

  (⚠ 질문은 질문으로만 — 음이온이 Li 이동을 바꾼다 / 안 바꾼다는 말하지 않는다 · 파일럿 판정 전. 진행 숫자 (12/40) 는 이 장에서 말하지 않는다 — 13장에서.
  'Al + O' 는 화합물이 **가져오는 것**이다 — '격자에 들어간다' 고 말하지 않는다 (모델의 가정 · 디펜스 S3).)

## 4. 왜 따로 재나 — 두 열화는 서로를 키운다 ⏱ 6:00
> 화면 (사용자 10-13 · 사용자 덱 5쪽): ■ *Failure modes in sulfide-based all-solid-state batteries* · bullet 둘
> (*Electrochemical and mechanical degradation reinforce each other.* · *A dopant that suppresses one mode can worsen the other, and the trade-off goes undetected unless each mode is evaluated separately.*) ·
> 그림 = Kang 등 2026 Chem. Commun. **Fig. 16** (저희 그룹 리뷰 · litdb `kang2026_intertwined_…` fig_16 과 대조) · 출처 줄 *Kang et al., Chem. Commun. 62, 10277 (2026)*.
> 앞 장 마지막 줄 (*'…반드시 따로따로 봐야 합니다. 왜 따로 봐야 하는지부터 보겠습니다.'*) 에 이 장이 답한다.
> ⚠ 그림 속 'SE reductive decompostion' 오타는 **원 논문 그림 그대로**다 — 실린 그림이라 고치지 않는다.

이 그림은 저희 랩에서 낸 리뷰, Kang 등의 2026년 Chem. Commun. 논문의 요약 그림입니다.

**[가리킴: 왼쪽 빨간 제목]** 왼쪽은 전기화학 열화입니다. 양극 쪽에서는 전해질이 산화되거나 양극재 · 도전재와 만나 분해되고, 음극 쪽에서는 환원 분해와 Li 덴드라이트가 생깁니다.

**[가리킴: 오른쪽 파란 제목]** 오른쪽은 기계적 열화입니다. 만들 때 생긴 공극, 양극재와 전해질 사이의 접촉 손실, 양극재 균열, 그리고 음극의 부피 변화와 덴드라이트 전파가 있습니다.

**[가리킴: 위아래 화살표 → 첫 bullet]** 이 둘은 따로 가지 않습니다. 분해가 생기면 재료가 약해져 깨지고, 깨져서 드러난 새 표면에서 분해가 또 일어납니다. 서로를 키우는 고리입니다.

**[가리킴: 가운데 SE doping]** 그리고 전해질 도핑은 이 그림 한가운데, 두 원이 겹치는 자리에 있습니다. 도펀트 하나가 두 쪽을 동시에 바꾼다는 뜻입니다.

**[가리킴: 둘째 bullet]** 그래서 한쪽을 막으려고 고른 도펀트가 다른 쪽을 나쁘게 만들 수 있고, 이 손해는 둘을 따로 재지 않으면 보이지 않습니다.
앞 장에서 세 가지를 반드시 따로 봐야 한다고 한 이유가 이것입니다.

그러면 지금까지의 도핑 스크린은 무엇을 바꿔 가며 걸렀는지, 선행 연구부터 보겠습니다.

**[클릭]**

  (⚠ 고리 설명은 리뷰 §4 문장 그대로다 — *'reaction-induced fragility leads to fracture, and the exposed surfaces accelerate ongoing interfacial degradation'*.
  '도펀트가 한쪽을 막고 다른 쪽을 나쁘게 한 예' 를 우리 값으로 들지 않는다 — 계 간 Ea · σ 비교는 인용위험 (HZ-cross-system-Ea · HZ-b2o3-md-ea).)

## 5. 선행 스크린과 이번 작업의 차이 ⏱ 7:00
> 화면 (사용자 10-13 · novelty 장 · 사용자 덱 6쪽): ■ *Prior dopant screens and what this study adds* · bullet 둘
> (*Earlier screens varied elements, or a coating compound without a host.* · *Here one precursor compound adds its cation and anion together, in its formula ratio.*) ·
> 표 = 선행 다섯 편 + 이번 작업 (오래된 순 · **Muy 2025 · Jung 2026 를 litdb 에서 더함**) · 출처는 **오른쪽 위 다섯 줄** (랩 표준 표기 · 사용자 최종판 10-13).
> ⚠ 10-13 논문별 원문 대조 뒤 사용자 반영: Miara 행 = *Miara 2015 · one cation, 3 sites (Li, La, Zr) · 128* (45 는 Miara 원문에 없는 Anderson 의 인용 수 → 'via Anderson' 과 Anderson 참고문헌을 같이 뺌) ·
> Lee 칸 = *P-site cations and halides* · Xiao = *no host (coating layer)* · 첫 bullet 에서 'one or two' 를 뺌 (Lee 는 P 자리 양이온 셋까지 + 할로겐) ·
> mechanical axis 열에서 'gate' 를 뺌 (사용자 10-13) — Jung *(used for screening)* · this work *(not used for screening)*.
> 앞 장 끝: *'그러면 지금까지의 도핑 스크린은 무엇을 바꿔 가며 걸렀는지, 선행 연구부터 보겠습니다.'*

지금까지의 도핑 스크린 다섯 편을 이번 작업과 나란히 놓았습니다. **[가리킴: what is varied 열]** 이 열이 핵심입니다. 무엇을 바꿔 가며 걸렀는지입니다.
- **[가리킴: Miara]** 가넷 산화물에서는 Miara 등이 도펀트 128 종을 Li · La · Zr 세 자리에 하나씩 넣어 보고, 어느 자리에 들어가는지 DFT 로 예측했습니다.
  (10-13 — 화면에서 Anderson 참고문헌이 빠져서, 177 시료 실험 검증 · '공도핑이 필요하다' 는 Anderson 결론은 대본에서 뺐다. 말하려면 참고문헌
  *Adv. Energy Mater.*, 14, 2304025 (2024). 를 화면에 되살린다. 질문이 오면 디펜스 S5.)
- **[가리킴: Xiao]** Xiao 등은 호스트 없이, 코팅으로 쓸 화합물 자체를 10만 개 넘게 걸렀습니다.
- **[가리킴: Lee · Muy]** 아지로다이트에서는 P 자리 양이온과 할로겐을 바꿔 새 조성을 설계하거나, 원소 하나를 자리별로 넣어 봤습니다.
- **[가리킴: Jung]** 가장 가까운 건 올해 나온 Jung 등의 연구입니다. LGPS 에 원소 두 개를 따로 골라 넣었습니다.

**[가리킴: this work 행]** 이번 작업은 원소가 아니라 전구체 화합물 하나를 넣습니다. 양이온과 음이온이 같은 화합물에서, 그 화학식의 비율대로 함께 들어갑니다.
예를 들어 Al₂O₃ 면 Al 둘에 O 셋입니다. 실험에서 실제로 넣는 단위 그대로입니다.
  (호스트 자리와 전하가 안 맞는 만큼은 Li 빈자리나 여분 Li 로 맞춘다 — 생성 규칙 ② 전체 전하 수지 · 이건 Jung 등도 같다 → 차이로 말하지 않는다)

**[가리킴: mechanical axis 열]** 앞의 네 편에는 기계 축이 없었고, Jung 등은 ML 로 예측한 탄성 값으로 후보를 걸렀습니다.
저희는 기준 조성은 DFT 로 계산하고, 전구체마다 MLIP 지표를 기록합니다. 다만 같은 전구체 안에서도 원자 배치에 따라 이 값이 전구체끼리의 차이만큼 흔들려서,
아직 후보를 거르는 데는 쓰지 않습니다. 이건 뒤의 9월 점검에서 다시 말씀드리겠습니다.
  (화면 칸 — Jung *ML-predicted G and G/K (used for screening)* · this work *DFT reference + MLIP descriptor (not used for screening)* · 괄호는 둘째 줄.
  사용자 10-13: 'gate' 같은 말은 안 쓴다. '흔들린다' 의 근거 = 9월 감사 잡음비 — 영률 1.104 · 치환에너지 0.205 (디펜스 S8 · S11) · 11장 'spread within a precursor ≈ between precursors'.
  DFT 탄성상수는 기준 조성에만 — 한 조성에 GPU 로 몇 주 (9장 · 12 변형점 중 9). 3,675 구조 전부에 쓸 수 있는 건 MLIP 뿐.)

그러면 이 91개 전구체가 어떤 화합물들인지 보겠습니다.

**[클릭]**

  (⚠ '처음' · '유일' 이라고 말하지 않는다 — 표의 다섯 편과 비교한 차이만 말한다. Jung 2026 이 이미 가진 것 (ML 대리모형 → DFT 안정창 → AIMD 의 틀 · 'S 자리 최적 도펀트는 Cl 과 O' · O 치환 왜곡 기전) 은 우리 것으로 말하지 않는다 —
  litdb `jung2026_scalable_ai_dual_doped_lgps` §1-A. 기계 축은 새로움이 아니다. 논문별 브리핑 = 디펜스 S5.)

## 6. 후보군 ⏱ 8:00
> 화면 (사용자 10-13 · 사용자 덱 7쪽): 08-18 덱의 Candidate set 표로 되돌림 — ■ *91 precursors in seven anion families* · bullet 둘
> (*Every precursor is an existing compound, with a cation from +1 to +6.* · *Al, Li, and Mg appear in all seven families, so their partner anions can be compared.*) ·
> 표 4 열 (family · n · **anion vs host** · examples) — 'role in the design' 열을 호스트 음이온 (S²⁻ · Cl⁻) 과의 비교로 바꿨다 · 막대그림과 SiO₂ 문헌 그림은 뺐다.
> 앞 장 끝: *'그러면 이 91개 전구체가 어떤 화합물들인지 보겠습니다.'*

후보는 91 개 전구체, 일곱 음이온족입니다. **[가리킴: 첫 bullet]** 전부 실제로 있는 화합물이고, 양이온은 +1 가부터 +6 가까지입니다.

**[가리킴: anion vs host 열]** 음이온을 호스트에 있는 S²⁻, Cl⁻ 와 비교해 정리했습니다.
- 황화물과 염화물은 음이온이 호스트에 이미 있어서, 새로 들어오는 원소는 양이온뿐입니다.
- 나머지 다섯은 음이온이 다릅니다. 산화물은 S²⁻ 보다 작은 O²⁻, 플루오린화물 · 브로민화물 · 요오드화물은 Cl⁻ 보다 작거나 큰 할로겐, 질화물은 전하가 더 큰 N³⁻ 입니다.

**[가리킴: 둘째 bullet]** 그리고 Al, Li, Mg 는 일곱 족에 모두 들어 있습니다. 그래서 앞에서 본 Al₂O₃ 와 Al₂S₃ 처럼, 같은 양이온에서 짝 음이온만 바꿔 비교할 수 있습니다.

그러면 이 91 개를 1단계에서 어떻게 계산했는지 보겠습니다.

**[클릭]**

  (⚠ 'Al · Li · Mg 가 일곱 족에 다 있다' 는 91 전구체 원장 `cascade_all_302_2026_08_25.csv` 실측이다 (Ca 는 여섯 족). 목록은 사람이 고른 것이라 '그렇게 설계했다' 고 말하지 않는다.
   '양이온만 바뀐다' 로 말하지 않는다 — 새로 들어오는 원소가 양이온뿐이라는 뜻이고, S · Cl 비는 바뀔 수 있다.
   공치환 선례 (CuCl · MgF₂ · ZnO · La₂O₃ · Nd₂O₃ · SiO₂) 는 참고문헌 17장에 있다. As₂S₃ · AlI₃ 8월 재실행 이야기는 7장으로.)

## 7. 1단계 — 파이프라인과 그때의 점수 ⏱ 10:30
> ✅ **확정 10-14** — 사용자 *"ㅇㅇ 진행해"* · *"틀린거라도 랭킹 한번 추가해서 진행해보던가"* · *"옆에 관련 plot해서 넣어주면 좋을듯 틀렸지만 ranking이 어땠었는지"* ·
> *"점수표 관련해서는 틀린 내용이라는걸 나중에 얘기할거니까 인용해도 될듯"* · 다음 장 = 감사 (*"그 다음페이지가 이런 방향성이 왜 잘못됐어서 방향성을 바꿨는지 설명"*).
> 화면 (슬림판 7장 · 사용자 8쪽): 왼쪽 점선 박스 'Pipeline' 다섯 단계 (오른쪽 회색 = 91 · 3,675 · 693 selected · 91 · 91) + `< Stage-1 pipeline, first attempt >` (10-15 · 옛 'run from June to August') ·
> 오른쪽 회색 막대 = 8월 방법 점수 상위 10 (91 개 중) + `< Stage-1 composite score, top 10 of 91 >` (`p07_stage1_composite_score_91.csv` · 강조 없음).
> ✅ **10-15 사용자 최종 (8쪽 · 사용자 *"이게 최종이야"*)**: 오른쪽 위 주석 두 줄 *'MLIP: Machine Learning Interatomic Potential, trained on DFT energies and forces'* · *'UMA: Universal Model for Atoms, a pretrained MLIP (Meta FAIR) used in this work'* · 막대는 Origin 판 (하늘색 · 강조 없음 — 빗금 뺌) · 오른쪽 캡션 `< Stage-1 composite score, top 10 of 91 >` 되살림 · 4단계 'Descriptors (Li-site landscape (BVSE), elastic moduli, stability window, and interface reactivity)' (값은 CSV 와 일치 10-15 재확인). 덱 원본은 사용자 사본이다 — 빌더 슬림판 (회색 막대 · 주석 없음) 은 맞추지 않았다.
> 앞 장 끝: *'그러면 이 91 개를 1단계에서 어떻게 계산했는지 보겠습니다.'*
> 10-14 보강 (사용자 *"이거를 대본에 잘 녹아내면 좋을듯"*): 점수 만든 방법 두 문장 · 에너지 기준 문제와 ML 이야기는 8장 · 숫자는 디펜스 S7 · S8.

> ✎ 10-16 **1분판** (사용자 *'한장씩 보자 · 1분가량의 대본으로 이해가 가능한 내용인지도'*) — 옛 본문 397 음절 (≈ 1분 20–30초) → 약 200 음절 + 숫자. 뺀 말 (6–8월 · 에너지 정의 자세히 · 영률과 Pugh 비 · 산화 시작 전압과 창 폭 · 가중치 0.30 · 0.25 · 'Li 자리 지형은 확산계수가 아니다' · As₂S₃ · AlI₃ 재실행) 은 아래 '물으면' 으로 옮겼다. 옛 본문의 메모는 그 아래 '옛 메모' 로 그대로 둔다.

**[가리킴: 박스를 위에서 아래로]** 1단계 첫 시도로 돌린 파이프라인입니다. 91 개 전구체마다 도펀트가 들어갈 자리를 전부 열거하고, 범용 MLIP 인 UMA 로 3,675 개 구조를 완화한 뒤 부피가 크게 바뀐 것은 걸렀습니다. 그중 693 개를 골라 짧게 데우고 다시 완화했고, 그 구조로 Li 자리 지형, 탄성률, 안정창, 계면 반응성을 냈습니다.
**[가리킴: 제목 아래 두 줄]** 점수는 모체와 견준 에너지, 탄성률, 안정창에서 뽑은 항 다섯을 0 에서 1 로 맞춰 손으로 정한 가중치로 더했습니다. Li 자리 지형과 계면 반응성은 점수에 들어가지 않았습니다.
**[가리킴: 오른쪽 막대]** 이 점수로 세운 상위 10 개입니다. 그러면 이 순위를 그대로 써도 될까요?

**[클릭]**

> 옛 메모 (2분판 본문에 끼어 있던 것 · 그대로):
> ✎ 10-15 밤: '전하 균형이 맞는' 을 뺐다 — 옛 생성기는 음이온 자리 전하를 안 셌고, 1단계 237 후보 중 48 (20 %) 이 형식전하 ≠ 0 이다 (9쪽 감사 · 디펜스 S8).
> (10-15 · 옛 '이 지표들을 점수 하나로 합쳐' 는 지표 넷을 다 합친 것처럼 들린다 — 점수에는 Li 자리 지형 · 계면 반응성이 안 들어갔다 · 불렛 둘째 줄)
> 10-15 정정 (사용자 *"descriptor 가 4 개 뿐인데 하나 더 추가해야 되는 거 아닌지"*): 옛 줄 *'점수는 지표 다섯을 …'* 은 위 *'지표 네 가지'* 와 어긋났다.
> 점수 항 다섯 ≠ 지표 넷이다 — 항은 에너지 1 (2–3 단계에서 나온 값) + 탄성률 2 (영률 · Pugh 비) + 안정창 2 (산화 시작 전압 · 창 폭) 이고, Li 자리 지형과 계면 반응성은 점수에 안 들어갔다 (`tools/figures/plot_cascade_insights.py`).
> 그래서 상자에 지표를 하나 더 넣지 않고, 제목 아래 작은 불렛 두 줄로 밝힌다 —
> *'Five terms were scaled from 0 to 1 and added with hand-set weights.'* · *'The terms came from the energy, elastic moduli, and stability window only.'*
> (첫 안은 둘째 줄이 'Pipeline' 표지와 겹치고 첫 줄이 'hand-/set' 에서 갈려서, 사용자 원문 첫 줄을 살리고 둘째 줄을 한 줄로 줄였다 · 제목 'June–August' → 'first attempt' · x 축 'composite score (first attempt)')

  (말로만 · 물으면 — 1분판에서 뺀 말: 6월부터 8월까지 돌렸다 · 에너지 = 모체와 견준 원자당 에너지 · 탄성률 항 = 영률 · Pugh 비 · 안정창 항 = 산화 시작 전압 · 창 폭 · Li 자리 지형은 구조 지표이지 확산계수가 아니다 · 8월 재실행으로 채운 As₂S₃ · AlI₃ 를 더해 91 개.)
  (말로만 · 물으면: 점수 = 0.30 산화 시작 전압 + 0.25 에너지 (낮을수록) + 0.20 영률 (낮을수록) + 0.15 G/B (낮을수록) + 0.10 창 폭, 91 개 안에서 0–1 로 맞춘 값 ·
   As₂S₃ 53 위 · AlI₃ 38 위 · 8월 89 개 순서는 거의 그대로 (순위 상관 0.9999 · 상위 15 같음).
   ⛔ 순위를 결과로 말하지 않는다 · 막대에서 특정 전구체를 짚지 않는다 · 'Al₂O₃ 가 Al₂S₃ 보다 낫다' 로 읽히는 말을 하지 않는다.
   남은 것 (AlI₃ 순위 1 배치의 지표 하나 · 계면 산물 통계 보류 · 호스트 탄성 진행 중) 은 물으면.)

## 8. 9월 감사 → 2단계 ⏱ 13:00
> ⏳ 10-15 화면 (사용자 *'권고대로 해봐 · 빨간 블록 그거랑 지금 버전 둘다 줘봐'*): **빨간 블록판이 기본** — 왼쪽 감사 목록 넷 · 오른쪽 결정 넷 + 빨간 다섯째 줄 (순위 여유 δ) · **분홍 상자 한 줄** (탐색 자료 · 승인된 순위 없음 — 상세판 8장의 빨간 블록과 같은 말) · 맨 아래 줄 (실행 범위).
> 'Found on Oct 14' 두 줄은 화면에서 빼고 **말로** 한다 (녹는 에너지 시연 한 줄 포함 · 숫자 없이). 옛 판 (두 목록 + Oct 14 블록) 은 검토본으로만 줬다 — 사용자가 고르면 이 절을 그 판에 맞춘다.
> 머신러닝 단락은 한 줄로 줄였다 (세부는 디펜스 S8). 두 목록은 **행끼리 짝이 아니다** (CW P0-1).
> ✅ 10-15 저녁 사용자 캡처 (사용자 9쪽) = **빨간 블록판 그대로** → '기본 설명 포맷' (A 화면 · B 대본 · C 하지 않을 말) 으로 설명. 대본 네 곳을 원장에 맞춰 고쳤다 (✎ 표시):
> ① '주 보고량' 에 **2단계** 범위 + 세 축 가운데 Li 이동 · 설계 선택 규칙은 따로 (`D-2026-10-15-cascade-objective-scope`) ② δ 문장 — 비준은 9-12 넷 · δ 는 9-19 S3 개정의 **제안** (비준 전) ③ 10월 14일 단락 끝 — 녹는 에너지 시연 기록의 허용 문장 그대로 ④ 전하 수지 문장에 '음이온' (생성 계약 b).
> 화면 권고 셋 (사용자 결정 · 빌더는 안 바꿈): 오른쪽 첫 줄 *'One primary Stage-2 readout, …'* · δ 줄 위치 (제목 *'Decisions recorded in September'* 또는 목록 밖 빨간 줄) · 맨 아래 *'The run scope will be set after the pilot.'*
> ✎ 10-15 밤 사용자 *'너무 우리만 알고 있는 단어들은 교체해서 필드에 있는 단어로'* → 사용자 9쪽 pptx 교체본 전달 (줄 수 · 상자 크기 그대로 · Calibri 와 폭이 같은 Carlito 로 확인). 권고 셋은 교체본에서 같이 풀렸다 — 오른쪽 제목 *'Stage-2 protocol set in September'* · 빨간 줄 *'A threshold δ for claiming a D_rel difference, proposed but not yet set'* · 맨 아래 *'… will be set after the pilot study.'*
> 바꾼 말: ledger → results and inputs · concentration labels → nominal concentrations · volume filter → volume-change filter · within a precursor → across configurations · merged → combined into a single score · decisions recorded → Stage-2 protocol · readout → observable · roster of designs → candidate compositions · parent sites → host-lattice site assignment · ranking margin → threshold δ for claiming a difference · approved → established · run scope → scope of the Stage-2 simulations. 'Wyckoff' 는 안 썼다 — 부모 자리 지도가 Li 24g/48h 를 못 가른다 (`cascade_s1_contract_amendment_2026_09_12.json` §3).
> ✎ 10-15 밤 사용자 *'audit of stage 1 괜찮아?'* → 권고 (화면은 사용자가 직접 고친다 · 결정 대기): ■ 날짜 없이 *'Re-examination of Stage 1'* (또는 *'Re-examining Stage 1'* · 사용자 *'september를 왜 넣냐고'* — 날짜는 말로 한다) · 왼쪽 제목 *'Findings'* · 첫 불렛 *'All results and inputs were re-checked.'* — 'audit' 은 틀린 말은 아니지만 영어에서 회계 · 규제처럼 제3자가 하는 공식 검사로 들리고, 'September audit' 은 우리 내부 행사 이름처럼 읽힌다. 말에서는 '감사' 를 '점검' 으로 바꿨다 (화면 결정과 무관) — '1단계를 감사했습니다' 는 '고마웠습니다' 로도 들리고, 발표 끝말이 '감사합니다' 다.
> ⚠ **10-15 밤 정정 — 237 은 조성 수가 아니다** (사용자 *'237 candidate compositions 설명해줘'* 에서 원표를 다시 셈): 1단계 본 배치 3,615 행 (90 전구체) 을 조성 44 열 + cation_site + anion_site + charge_compensation 으로 묶은 수다 (묶음마다 15–30 행 · `cascade_design_contract_2026_08_28.json` 그룹키). **조성만으로는 147** · Li 24g/48h 를 합치면 (S1 계약의 'Li 전체') **215**. 비준 기록 `cascade_design_roster_amendment_2026_09_12.json` 의 '237 = 조성으로 세기' 는 키를 줄여 적은 것이다 (봉인 · 안 고침 · 정정 기록은 세미나 뒤 사용자 결정). 화면 권고 *'237 candidate composition–site combinations'* · 대표 줄 *'One median-energy configuration per candidate'*. 10-15 교체본의 'candidate compositions' 는 내가 틀림을 키운 말이다.
> ✎ 10-15 밤 사용자 *'median 으로 해도 물질 전체를 대표하나?'* · δ 설명에 *'도저히 무슨 말인지 모르겠다 · 문장도 쉽게'* → 빨간 줄 권고 *'Minimum D_rel difference to call two candidates different, not yet set'* (δ 를 남기려면 'difference (δ) to call …') · 대표 줄 말에 '구조 하나가 물질 전체를 대표하지 않는다 · 차이는 배치 여러 개의 흔들림으로' 를 붙임. 사용자 *'우선 중앙값을 기준으로 했다는 느낌 · 사람의 입김이 안 들어간다는 느낌'* → 대표 줄 권고 *'One median-energy configuration per candidate, chosen by rule, not by hand'* · 말은 '기준 구조는 사람이 고르지 않고 미리 정한 규칙대로' (규칙 자체는 1저자가 결과 전에 네 갈래 중 골랐다 — 9-12 비준) (`cascade_d_rel_amendment_2026_09_12.json` §2 물리 · S3 개정 §2-3 · §2-6).
> ✅ 10-15 밤 사용자 캡처 (사용자 9쪽 최종 후보): ■ *'Re-examination of Stage 1'* · 왼쪽 *'Findings'* · 오른쪽 *'Stage 2 protocol'* · 다섯째 줄 *'Minimum D_rel difference to call two candidates different, not yet set'* (빨간색 빠짐 → 가리킴을 '오른쪽 마지막 줄' 로) · 넷째 줄 *'…, chosen by rule, not by hand'* · 237 줄 *'composition–site combinations'*. 남은 손볼 곳 (사용자에게 권고): 분홍 상자 쉼표 이음 (', no dopant ranking …' → '; ' 또는 ', and') · 'Stage 1 results' ↔ 'Stage-1 results' 하이픈 통일.
> ⏳ 같은 옛 말이 사용자 15·16쪽 (슬림 14·15 · ranking margin · readout · 237-design roster · run scope) 과 아래 §14 · §15 · '꼭 지킬 것' 에 남아 있다 — 그 쪽에 갈 때 같은 말로 맞춘다.

> ✎ 10-16 **1분판** (사용자 *'8pg 넘어가자는 거였어 이건 다시 봐봐'* · 장마다 1분) — 옛 본문 약 885 음절 (≈ 3분) → 약 270 음절 + 숫자. 10-14 에너지 기준 이야기 · 머신러닝 라벨 · 자리 배정 세부 · 중앙값 구조의 한계는 아래 '물으면 쓸 말 (옛 본문)' 으로 옮겼다. δ 줄은 13쪽의 ±ln 1.5 와 부딪혀 보이지 않게 '파일럿은 1.5 배로 정해 두었고' 를 넣었다 (파일럿 δ = 카드 v6 · v7 · 본 계산 δ 는 9-19 제안만 · 비준 전).

**[가리킴: 제목 아래 줄]** 9월에 1단계의 결과와 입력을 다시 점검했습니다.
**[가리킴: 왼쪽 목록]** 네 가지가 나왔습니다. 명목 농도를 바꿔도 셀 하나에 든 도펀트 수는 같았고, 부피 필터의 기준 부피가 DFT 평형보다 40 % 정도 컸습니다. 탄성률은 같은 전구체 안에서도 전구체 사이만큼 흩어졌고, 주목적 없이 지표를 점수 하나로 합쳤습니다.
**[가리킴: 분홍 상자]** 그래서 1단계 결과는 탐색 자료로 남기고, 도펀트 순위는 아직 없습니다.
**[가리킴: 오른쪽 목록]** 대신 2단계 규칙을 결과 전에 정했습니다. 보고량은 호스트 대비 Li 확산계수 비 하나이고, 후보는 조성과 자리로 센 237 개입니다. 전하 수지를 맞추고, 구조는 사람이 아니라 규칙으로 고릅니다. 두 후보가 다르다고 할 기준선은, 파일럿은 1.5 배로 정해 두었고 본 계산용은 아직 정하지 않았습니다.
**[가리킴: 맨 아래 줄]** 무엇을 얼마나 돌릴지도 파일럿 뒤에 정합니다. 그 근거를 이어서 보겠습니다.

**[클릭]**

> 물으면 쓸 말 (옛 본문 · 약 3분 · 화면에서 읽지 않는다):
> 9월에 1단계의 결과와 입력을 하나씩 다시 점검했습니다.
> **[가리킴: 왼쪽 목록]** 점검에서 네 가지를 찾았습니다.
> - 첫째, 명목 농도가 달라도 시뮬레이션 셀 하나에 든 도펀트 양은 같았습니다. 모든 구조가 같은 도핑 수준이었습니다.
> - 둘째, 부피 변화 필터가 기준으로 쓴 호스트 부피가 DFT 평형 부피보다 40 % 정도 컸습니다. 그래서 2단계는 DFT 평형 호스트에서 구조를 만듭니다.
> - 셋째, 영률은 같은 전구체의 구조끼리 흩어짐이 전구체 사이 차이만큼 컸습니다.
> - 넷째, 주목적을 정하지 않은 채 여러 지표를 점수 하나로 합쳤습니다.
> 그리고 10월 14일 점수를 다시 매기면서 하나를 더 확인했습니다. 에너지 항에 넣은 원소의 기준이 없어서, 앞 장에서 산화물이 위에 많은 데에는 결합 세기가 섞여 있었습니다. 원소 기준을 넣어 다시 매겨 보려고 했지만, 1단계 구조에서는 도핑 구조와 호스트 기준이 같은 상태에 있지 않아서 그 값도 정의되지 않았습니다. 그 값은 2단계 구조에서 다시 냅니다.
> **[가리킴: 분홍 상자]** 그래서 1단계 결과는 탐색 자료로 남기고, 확정된 도펀트 순위는 아직 없습니다. 실패가 아니라, 그 단계까지 아직 안 온 것입니다. 같은 이유로 이 값을 머신러닝 라벨로 쓰는 것도 지금은 어렵습니다 — 기법보다 라벨이 문제라서, 라벨부터 다시 만듭니다.
> **[가리킴: 오른쪽 목록]** 그리고 새 결과를 보기 **전에** 규칙을 먼저 박았습니다.
> - 2단계의 주 보고량은 하나입니다. 호스트 대비 Li 추적자 확산계수 비, D_rel 을 후보 조성끼리 비교합니다. 앞에서 따로 봐야 한다고 한 세 가지 가운데 Li 이동이고, 후보를 고르는 규칙은 결과를 보기 전에 따로 정합니다.
> - 후보는 237 개입니다. 같은 조성이라도 도펀트가 들어가는 자리가 다르면 따로 셌고, 파일 이름이 아니라 실제 조성과 자리로 셌습니다.
> - 자리 배정은 치환 전에 호스트 격자에서 정해 두고, 음이온과 Li 공공 · 침입까지 모두 넣어 전하 수지를 맞춥니다.
> - 기준 구조는 사람이 고르지 않고, 미리 정한 규칙대로 치환에너지가 중앙값인 구성으로 정합니다. 다만 이 구조 하나가 물질 전체를 대표한다고 보지는 않습니다. 차이를 말할 때는 배치 여러 개를 돌려서 흔들림까지 봅니다.
> **[가리킴: 오른쪽 마지막 줄]** 이 넷은 9월 12일에 확정했습니다. 마지막 줄은 두 후보의 D_rel 이 얼마나 달라야 '다르다' 고 할지, 그 기준선입니다. 9월 19일에 제안만 했고, 아직 정하지 않았습니다. 결과를 보기 전에 정합니다.
> **[가리킴: 맨 아래 줄]** 237 개를 다 돌린다는 뜻은 아닙니다. 2단계에서 무엇을 얼마나 돌릴지는 파일럿 뒤에 정합니다.
> 이 네 가지가 어디서 나왔는지, 1단계를 조금 자세히 보겠습니다.
> 옛 메모 (그대로):
> ✎ 10-15: 옛 '호스트 기준이 다른 바닥에 있어서' → 시연 기록의 허용 문장 ('구성과 호스트가 같은 상태에 있지 않아 정의되지 않았다 · 2단계 구조에서 다시 낸다' — `cascade_dissolution_energy_demo_readout_2026_10_14.json`). '바닥(basin)' 은 회신 BO 로 가설이라 쓰지 않는다 · 숫자 없이.
> ✎ 10-15: 옛 '공공까지 포함해' 는 결함의 핵심이 빠졌다 — 옛 생성기는 **음이온 치환의 전하를 안 셌다** (NdCl₃ 1 단위: 양이온만 −2 · 음이온까지 +1 → 보상 3 어긋남 · `cascade_s1_contract_amendment_2026_09_12.json` b_보상_수지).
> ✎ 10-15: ① 옛 '주 보고량은 하나입니다' 는 캠페인 전체가 D_rel 하나를 보는 것처럼 들렸다 — `D-2026-10-15-cascade-objective-scope` (D_rel = 2단계 주 보고량 · 수송 축 · 설계 선택은 D_rel 하나로 정하지 않는다).
> ② 옛 '이 넷은 비준을 마쳤고, 마지막 순위 여유 … 더 낫다고' — δ 는 9-12 결정이 아니라 9-19 S3 개정의 제안 (`cascade_s3_protocol_amendment_2026_09_19.json` · 비준 전 · δ 자리 비어 있음) · δ 는 두 설계의 **D_rel 차이를 주장하는 조건**이지 설계 선택 규칙이 아니라서 '더 낫다' → '다르다'.

## 9. 배치 표본과 MLIP 완화 ⏱ 14:00
> ⏳ 10-15 화면: 오른쪽 위 담금질 도식 (작게) + **오른쪽 아래 담금질 에너지 변화 히스토그램** (원장에서 다시 그림 · 693 = 7장 파이프라인 숫자 · 8월 덱 Step 5 의 681 은 8월 재실행 전) + 맨 아래 줄 'All 693 annealed structures found a lower-energy configuration (median ΔE = −0.81 eV per 52-atom cell).'
> ✎ 10-15 밤 사용자 *'그럼 그 내용이 불렛에 들어가야되는거 아니야?'* → 10쪽 v3 불렛 (둘 다 한 줄 · 이음 구절 파랑): *'Substitution sites were enumerated, not assumed, so 147 compositions gave 237 candidates.'* · *'A 500 K, 50 ps MD anneal lowered every structure's energy, so configuration choice matters.'* (사용자 *'뭘 lower 했는지 안 써져 있다'* → v4 · 'energy' 를 넣고 한 줄 유지) → v5 (사용자 *'choice matters 가 뭔 뜻?'*): *'Annealing lowered every structure's energy, so results depend on the configuration used.'* — 'matters' 의 뜻을 풀어 씀 · 500 K, 50 ps 는 도식 안에 있다 → v6 (사용자 *'추가됐다는 거 사족이니까 한 문장으로'*): 왼쪽 캡션 *'< configurations per cation–anion site pair (n = 3,615) >'* 한 줄 · 오른쪽 캡션과 같은 높이 · 말에서도 8월 재실행 60 을 뺐다 (물으면 디펜스 S9) → v7 (사용자 *'60 개는 아직 안 들어갔다는 거는 맞는 듯 · august 대신 · 3675 는 앞에 나왔으니까'*): 캡션 두 줄 *'< configurations per cation–anion site pair ⏎ (3,615 of 3,675; 60 not yet included) >'* · 둘째 줄이 오른쪽 캡션과 같은 높이 · 말도 '앞 장의 3,675 개 가운데 3,615 개 · 60 개는 아직' → v8 (사용자 *'추가해서 만드는건 안되는거야?'*): 열지도를 3,675 개 구조 전부로 다시 셈 (`p08_structures_per_site_pair_3675_matrix.csv` · Li 24g 1,050/810/615 · P 4b 390/285/195 · Li 48h 120/105/105) · 캡션 *'< structures per cation–anion site pair (n = 3,675) >'* · 8월 재실행 60 = As₂S₃ 45 + AlI₃ 15 (본 배치와 같은 이름의 재실행 — 서로 다른 구조로는 3,660 · 담금질 693 도 AlI₃ 3 이 두 번 → 690) · 237 후보는 본 배치 3,615 기준 (As₂S₃ 없음) · 히스토그램 = 8월 Origin 모양 (보라) 을 693 행으로 다시 그림 (8월 그림은 n 681) · Origin CSV `p08_anneal_energy_change_origin.csv` (중앙 −811.5 meV = −0.81 eV / 52 원자 셀).
> ✎ 10-15 밤 사용자 *'앞 페이지랑 이 페이지랑 어케 연결되는건지'* → 9쪽 (감사 · 규칙) 다음의 10–12쪽은 **발견의 근거**다: 10쪽 = 셋째 발견 (배치 흩어짐) · 자리 쌍 → 후보 237 · 대표 규칙 / 11쪽 = 둘째 발견 (DFT 평형 부피) / 12쪽 = 안정창 정의. 여는 말 · 자리 쌍 → 237 줄 · 닫는 말을 그 다리로 고침.
> ✎ 10-15 밤 사용자 10쪽 pptx (*'배치 신경 써주고 필드 언어로'*) → 교체본: 첫 불렛 *'Substitution sites were enumerated, not assumed, and every configuration was relaxed.'* (옛 'every charge-balanced placement' 는 사실과 다름 — 20 % 가 형식전하 ≠ 0) · 둘째 *'A short MD anneal (500 K, 50 ps) let selected structures escape their local minima.'* · 열지도는 필드 말로 다시 그림 (양이온/음이온 치환 자리 · S 4a (free S²⁻) · S 16e (in PS₄) · Cl 4d · `export_cascade_briefing_csvs_2026_10.py --fig-p08`) · 히스토그램 축 'per 52-atom cell' (옛 'supercell' = 4 화학식 단위 기본 셀) + 중앙값 점선 · 캡션 셋 · 배치 (왼쪽 열지도를 키워 두 열 바닥을 맞춤).
> ✎ 10-15 밤 사용자 자기 판 (v9 · 사용자 덱이 정본): 열지도 왼쪽 크게 · 도식 오른쪽 위 · **Origin 히스토그램** (보라 · 중앙 점선 · 라벨 'Median -811.5') 오른쪽 아래 · 캡션 둘 같은 높이 · 맨 아래 줄 *'All 693 annealed structures found a lower-energy configuration (median ΔE = −0.81 eV per 52-atom cell).'* — 숫자 원장과 맞음 (693 · 전부 낮아짐 · 중앙 −811.5 meV · 열지도 아홉 칸 · 백분율). 남은 권고는 사용자 선택: 히스토그램 글씨가 슬라이드에서 약 6 pt (캡션 약 11 pt) → Origin 글자 1.5 배 · x 축 제목 'ΔE (meV per 52-atom cell)' (바로 아래 캡션도 'energy change' 로 시작해 두 줄이 겹쳐 읽힘 · 도식과 맨 아래 줄은 이미 ΔE). 말에서 '감사의 셋째 항목' → '앞 장에서 말한 셋째 발견' (사용자 규칙 '감사' → '점검' 의 남은 자리).
> ✅ 10-15 밤 **최종** (사용자 *'이게 최종이야'*): x 축 제목 **'ΔE (meV per 52-atom cell)'** (Origin 코드가 글자로 들어가서 서식으로 다시 넣음) · 라벨 **'median -811.5'** (소문자) · 히스토그램 글씨 크기는 그대로 (사용자 선택 · 다시 권하지 않는다) · 나머지는 v9 그대로.
> 8월 덱의 *'the top ten of the ranking did not change'* 는 **말하지 않는다** (디펜스 §1 철회). CSV `p08_anneal_energy_change.csv`.

> ✎ 10-16 **1분판** (사용자 장마다 1분 점검) — 옛 본문 약 440 음절 (≈ 1분 30초) → 약 210 음절 + 숫자. '지표에 따라 같은 전구체 안 흩어짐 ≈ 전구체 사이' 는 화면에 없는 말이라 아래 '물으면 쓸 말' 로 옮겼다. 같은 날 화면 제안: 둘째 불렛 *'Annealing lowered every structure's energy'* 는 3,675 개 전부를 데운 것처럼 읽힌다 (실제는 선별한 693 · 10-13 Codex 뒤 7장에서도 같은 정정) → *'All annealed structures dropped in energy, so results depend on the configuration used.'* (16 pt 한 줄 · 사용자 판단).

**[가리킴: 제목 아래 첫 줄]** 1단계에서는 도펀트가 들어갈 자리를 미리 가정하지 않고 전부 늘어놓았습니다. 같은 조성이라도 자리가 다르면 따로 세서, 조성 147 개가 후보 237 개가 됐습니다.
**[가리킴: 왼쪽 열지도]** 만든 구조 3,675 개를 양이온 자리와 음이온 자리 짝으로 나눈 표입니다. 아홉 짝이 모두 쓰였습니다.
**[가리킴: 오른쪽 위 도식]** 완화만 하면 가장 가까운 골짜기에 멈추기 때문에, 선별한 693 개는 500 K 에서 50 ps 짧게 데운 뒤 다시 완화했습니다.
**[가리킴: 오른쪽 아래 히스토그램 → 맨 아래 줄]** 그랬더니 693 개 전부가 더 낮은 에너지를 찾았고, 중앙값으로 52 원자 셀당 0.81 eV 낮아졌습니다.
**[가리킴: 둘째 줄]** 즉 어떤 배치를 쓰느냐에 따라 결과가 달라집니다. 그래서 2단계에서는 대표 구조를 규칙으로 고릅니다.

**[클릭]**

> 물으면 쓸 말 (옛 본문 · 약 1분 30초 · 화면에서 읽지 않는다):
> 앞 장의 발견이 어디서 나왔는지, 1단계에서 구조를 만든 방법부터 보겠습니다. **[가리킴: 왼쪽 열지도]**
> - 치환 자리를 미리 가정하지 않고 자리 조합을 하나씩 다 늘어놓았고, 만든 배치는 **전부** 완화했습니다.
> - 양이온 자리 셋과 음이온 자리 셋, 아홉 쌍이 모두 쓰였습니다. 앞 장의 3,675 개 구조를 모두 자리 쌍으로 나눈 표입니다.
> - 같은 조성이라도 이 자리 쌍이 다르면 다른 후보로 셌습니다. 그래서 조성 147 개가 앞 장의 후보 237 개가 됐습니다.
> - 지표에 따라서는 **같은 전구체의 배치끼리 차이가 서로 다른 전구체 사이 차이만큼 큽니다.** 그러면 그 지표로는 순위를 매길 수 없어서, 지금 지표는 탐색용으로만 씁니다. 이것이 앞 장에서 말한 셋째 발견입니다.
> **[가리킴: 오른쪽 위 도식]** 완화만 하면 가장 가까운 국소 최소에 멈춥니다. 그래서 선별한 구조는 500 K 에서 50 ps 짧게 데워 그 골짜기에서 빼낸 뒤 다시 완화했습니다.
> **[가리킴: 오른쪽 아래 히스토그램 → 맨 아래 줄]** 담금질한 693 개 구조가 모두 에너지가 더 낮은 배치를 찾았습니다. 중앙값으로 52 원자 셀 하나당 0.81 eV 낮아졌습니다. 완화만으로는 국소 최소에 머문다는 뜻이고, 이 단계가 하는 일이 그것입니다. 어느 배치를 쓰느냐에 따라 값이 달라진다는 뜻이기도 해서, 앞 장에서 대표 구조를 규칙으로 정했습니다.

## 10. DFT 기준 계산 ⏱ 15:00
> ⏳ 10-14 순서 바뀜 (옛 9장 → 감사 둘째 항목의 근거). 이 장을 볼 때 다시 확정한다.
> ✎ 10-15 밤 **부록 장 새로** (사용자 *'그리고 appendix 에 이걸 좀 수정해서 넣음 좋을듯'* · 08-18 'Step 3' 장): ■ *'Stage-1 volume-change filter and its reference volume'* · 불렛 *'The Stage-1 reference (27.48 Å³ per atom) was the MLIP-relaxed volume of the template.'* · *'The 100 structures the filter removed lay within 6 % of the DFT host volume.'* · 두 칸 히스토그램 (같은 3,615 구조 · 27.48 기준 vs 19.56 = DFT 호스트를 같은 MLIP 로 완화 · 빨강 = 걸러진 100) · 맨 아래 줄 *'Re-filtering against the DFT host flags 1,284 instead of 100, so Stage 2 rebuilds from the DFT host.'* · 원장 재앵커 기록과 같은 산술 (100 → 1,284). 08-18 장의 오른쪽 산점도 ('energies look like the rest') 는 뺐다. 발표에서는 넘기지 않고, '왜 그 부피였나 · 다시 거르면?' 질문이 오면 연다 (디펜스 S8).
> ✎ 10-15 밤 사용자 11쪽 pptx (*'이것도 내용에 맞게 수정을 해줘용'*) → 교체본 v2 (사용자 판이 원본 · 빌더는 안 바꿈): 이 장은 9쪽 **둘째 발견의 근거**인데 화면에 그 연결이 없었다 → 맨 아래 줄 *'The Stage-1 volume-change filter used a host volume of 27.48 Å³ per atom, 1.41 times the DFT V₀ of Li₆PS₅Cl.'* (원장 `cascade_reanchor_comp1k444_2026_09_12.json` 27.478 · `eos.json` comp1_v3 V₀ 1016.62 Å³ ÷ 52 = 19.550 · 비 1.406) · 불렛 *'A Birch–Murnaghan fit gives the bulk modulus B₀ and the equilibrium volume V₀.'* (옛 줄은 마침표 붙은 조각 · V₀ 를 여기서 정의) · *'Elastic constants (C_ij) come from finite strains, and a supercell convergence check is in progress.'* (옛 'are running on GPU' 는 사실과 다름 — 단일 셀 relaxed-ion C_ij 는 원장에 있고 · 진행 중인 것은 Li₅.₄PS₄.₄Cl₁.₆ 2 배 셀 확인 modelc_2x 12 점 중 9 점 · 13_m 은 Li₃Nd r2 때문에 EXIT 정지 · 10-14 결정으로 수렴까지 계속) · 라벨 'V₀ = … per f.u.' + Li₆PS₅Cl 에 '(19.55 Å³ per atom)' 파랑 (맨 아래 줄의 파랑과 짝) · '−4.3 %' 참 마이너스 · 캡션 *'< DFT equations of state of Li₆PS₅Cl and Cl-rich Li₅.₄PS₄.₄Cl₁.₆ >'* ('LPSCl1.6' · 'undoped' · 'vs' 를 뺌) · 출처는 랩 표준 (저자 없음 · 저널 기울임) 으로 8쪽처럼 오른쪽 위.
> ✎ 10-16 1분 점검 (사용자 장마다 1분): 본문 약 283 음절 ≈ 1분 — 그대로 둔다. 오른쪽 위 출처 둘 (Deng 2016 *J. Electrochem. Soc.* · Torii 2025 *J. Phys. Chem. C*) 이 무엇의 근거인지 말이 없어서 탄성 줄에 한 문장 넣었다 — 같은 종류의 탄성 계산이라는 근거로만 · 그 논문들의 숫자와 나란히 말하지 않는다 (B_VRH ≠ BM3 B₀ · `cascade_briefing_2026_10_direction.md` · 디펜스 S10).
앞에서 점검의 둘째 발견으로 부피 기준을 말씀드렸는데, 그 비교의 기준이 되는 DFT 계산입니다. **[가리킴: 두 곡선]**
- 에너지–부피 곡선에 Birch–Murnaghan 상태방정식을 맞춰 부피탄성률 B₀ 와 평형부피 V₀ 를 얻습니다.
  - B₀ 는 Li₆PS₅Cl 이 26.2 GPa, Cl 이 많은 Li₅.₄PS₄.₄Cl₁.₆ 가 21.7 GPa 입니다.
  - 두 조성은 셀에 든 화학식 단위 수가 달라서, 부피는 화학식 단위당으로 비교합니다.
  - **[가리킴: 왼쪽 파란 숫자]** Li₆PS₅Cl 의 평형부피는 원자당 19.55 Å³ 입니다.
- 탄성상수는 셀을 조금씩 변형시키고, 변형마다 원자 위치를 다시 완화해서 구했습니다 (relaxed-ion). 오른쪽 위 두 논문도 같은 종류의 DFT 탄성 계산입니다. 더 큰 슈퍼셀로 수렴을 확인하는 계산이 진행 중이라 값은 오늘 말씀드리지 않습니다.
  > ✎ 10-15 밤 사용자: 탄성 불렛의 상태 구절을 뺐다 (*'Elastic constants (C_ij) come from finite strains.'*) · *'relaxed ion 으로부터 온다는 거 표현하는 게 낫지 않아?'* → 제안 *'Relaxed-ion elastic constants (C_ij) come from finite strains.'* · 사용자 가설 *'초기 cascade 는 UMA 인데 clamped 로 해서'* 는 코드와 다르다 — 1단계 UMA 탄성도 변형마다 이온을 완화했다 (`tools/doping/run_mlip_postproc.py` `elastic_finite_strain` · FIRE fmax 0.05 eV/Å · 300 스텝 · ε ±0.005) · `tier_cascade.sh:238` 의 'clamped-ion' 은 틀린 주석 (08-19 정독 기록 `cascade_pipeline_anatomy_2026_08_13.md` §A).

**[가리킴: 맨 아래 줄]** 1단계의 부피 변화 필터는 원자당 27.48 Å³ 를 호스트 부피로 썼습니다. 이 DFT 평형부피의 1.41 배이고, 점검에서 말씀드린 '약 40 %' 가 이것입니다. 그래서 2단계는 DFT 평형 호스트에서 구조를 만듭니다.

**[클릭]**

## 11. 안정창과 계면 반응성 ⏱ 16:30
> ⏳ 10-14 순서 바뀜 (옛 10장 → 감사 뒤 · 같은 검토에서 고친 정의). 이 장을 볼 때 다시 확정한다.
> ✎ 10-15 밤 사용자 12쪽 pptx (*'이것도 스토리에 맞게 부탁할게용'*) → 교체본 v2 (사용자 판이 원본 · 빌더는 안 바꿈): 이 장의 줄거리 = **정의를 바로잡았고 그래서 91 개를 다시 냈다** 인데 화면에 정의도 이유도 없었다 ('this definition' 이 가리키는 문장이 없었음) → 불렛 *'The window is the voltage range with no Li exchange on a grand-potential phase diagram.'* · *'The earlier lower limit lay in the Li-uptake range, so all 91 precursors were recomputed.'* (옛 둘째 줄은 마침표 붙은 조각) · 왼쪽 그림에 옛 하한 1.242 V 를 회색 점선으로 더함 (축 1.1–2.5 V · `export_cascade_briefing_csvs_2026_10.py --fig-p10` · 값은 원장 `first_reduction_plateau_V` · CSV `p10_stability_window_host_legacy.csv`) · 맨 아래 줄 *'For Li₆PS₅Cl, the window is 0.423 V wide, less than half the earlier 0.898 V.'* · 문헌 꼬리표의 콜론을 뺌 *'Literature (decomposition and intrinsic windows)'* · 출처 랩 표준 · 오른쪽 위. 91 = 본 배치 90 + As₂S₃ (`oxidation_stability_cascade_v3_pinned.json` + 10-13 부록 · 전구체 이름 기준 91/91). 계면 반응성은 화면에 없어서 말 한 줄로 줄였다 ('오른쪽 글' · 'Sundar 그림' 가리킴은 슬림판에 없는 자리였다).
> ✎ 10-16 사용자: 문헌 꼬리표와 'Reproduced from' 줄을 빼고 *'두 번째 figure 에 caption 으로'* → 교체본 v3 캡션 *'< decomposition and intrinsic windows reported in JACS Au, 1, 1488 (2021) >'* (무엇 · 문헌 · 출처를 한 줄에). 사용자 질문 *'대본에 이 내용이 다 들어가?'* → 출처 네 편 중 셋을 쓰는 자리에서 말로 밝힘: Zhu 2015 = 방법 (첫 불렛) · Schwietert 2021 = 오른쪽 그림 · Richards 2016 = 계면 한 줄. Xiao 2020 (계면 안정성 리뷰) 은 일반 참고라 말하지 않는다. · 사용자 *'MP 설명도 넣자 · 이런식으로'* (덱의 'MLIP: … / UMA: …' 약어 상자 형식) → v4 왼쪽 캡션 아래 *'MP: Materials Project, ⏎ an open database of DFT (GGA/GGA+U) phase energies'* (12 pt · 왼쪽 정렬) · 말 두 줄 (MP 가 무엇인지 · 왜 쓰고 우리 DFT 와 왜 안 섞는지 · 0 K 의 뜻). · 사용자 *'주된 reference 로만 넣자'* → v5 오른쪽 위 출처 두 줄 (*ACS Appl. Mater. Interfaces*, 7, 23685 (2015) = 방법 · *JACS Au*, 1, 1488 (2021) = 오른쪽 그림) · Richards 2016 · Xiao 2020 은 화면에서 빼고 말에서도 뺐다 (계면 줄은 출처 없이 한 줄 · 물으면 디펜스 S11).
> ✅ 10-16 **최종** (사용자 *'이게 최종이고'*): MP 상자는 오른쪽 위 (머리글 옆) · 출처 두 줄은 그 아래 · 두 캡션은 같은 높이 · 오른쪽 캡션은 *'< decomposition and intrinsic windows >'* (출처를 캡션에서 뺌 → **'Schwietert 등 (2021) 의 그림입니다' 는 말로 꼭 한다** — 우리 결과로 읽히지 않게) · 쪽 번호 12.
다음은 안정창입니다. 점검하면서 정의도 하나 바로잡았습니다. **[가리킴: 첫 불렛]**
- 대권위 상도표에서 Li 화학퍼텐셜을 전압으로 바꿔 훑습니다. Zhu 등 (2015) 의 방법입니다.
- **[가리킴: 오른쪽 위 MP 설명]** 상 에너지는 Materials Project, 줄여서 MP 에서 가져왔습니다. 무기 화합물의 DFT 에너지를 같은 설정 (GGA/GGA+U) 으로 모아 둔 공개 데이터베이스입니다. 상도표에는 경쟁하는 상의 에너지가 모두 필요해서 이 값을 썼고, 우리 DFT 값과는 섞지 않습니다.
- 0 K 열역학이라 온도와 반응 속도는 들어가지 않습니다. 그래서 이 창은 '열역학적으로 분해가 가능한 범위' 입니다.
- 안정창은 **전극과 Li 을 주고받는 반응이 없는 전압 구간**입니다. 그런 구간이 없으면 '안정창 없음' 으로 기록합니다.

**[가리킴: 왼쪽 그림]** 호스트 Li₆PS₅Cl 로 보면,
- 1.717 V 아래에서는 Li 을 받아들이고, 2.140 V 위에서는 Li 을 내놓으며 산화됩니다.
- 그 사이 0.423 V 가 Li 교환이 없는 구간입니다.
- **[가리킴: 회색 점선]** 예전 계산은 하한을 1.242 V 에 두었습니다. 이 자리는 아직 Li 을 받아들이는 구간이라, 창이 0.898 V 로 넓게 나왔습니다.
- **[가리킴: 둘째 불렛]** 그래서 91 개 전구체를 모두 이 정의로 다시 계산했습니다.

**[가리킴: 오른쪽 그림]** Schwietert 등 (2021) 의 그림입니다. 이 논문은 이 정의를 decomposition window 라고 부르고, Li₆PS₅Cl 하한 1.72 V 가 우리 1.717 V 와 맞습니다. 옅은 막대 intrinsic window 는 정의가 달라서 비교하지 않습니다.

계면 반응성도 같은 상 자료로 계산해 두었지만, 반응 산물을 판정하는 규칙을 정하기 전이라 오늘은 쓰지 않습니다.

**[클릭 전에]** 여기까지가 1단계를 다시 점검하며 고친 것들입니다. 이렇게 먼저 박은 규칙으로 지금 도는 것이 2단계 파일럿입니다.

**[클릭]**

## 12. 2단계 파일럿 — 설계 · 온도 · 한계 (사용자 13쪽 · 한 장) ⏱ 18:00
> ✎ 10-16 사용자 13–14쪽 pptx (*'이거 한 페이지로 부탁하고 요 내용은 빼도 될듯'* — 40 런 진행표) → 한 장 교체본 v1: 제목 그대로 · 불렛 넷 (한 줄 · 문장 · 콜론 없음 — 옛 'Reported: …' · '600 K, this UMA cell: …' · 'Predefined probe: …' · 'Our pilot: …' · 'Cell ≈ 1.6 nm at 1000 K: …' 의 콜론을 다 풀었다) · 문헌 그림 둘 나란히 (He 2018 Fig. 3 · Jung 2026 Fig. 5b · 같은 높이) · 캡션은 12쪽 최종판처럼 *'< run-to-run spread and fit-window sensitivity >'* · *'< temperature-dependent ordering >'* (출처는 오른쪽 위 랩 표준 셋 *npj Comput. Mater.*, 4, 18 (2018). · *eTransportation*, 28, 100570 (2026). · *Chem. Mater.*, in press (2026). — Phuthi 2026 은 권·쪽 미부여 (litdb · 10-16 웹 확인 안 됨) 라 'in press' · v1 파일은 doi 로 적었다) · 맨 아래 줄 *'With a 1.6 nm cell at 1000 K, the result will be relative and condition-specific.'* · 40 런 진행표 (10-12 기준 12/40) 는 화면에서 뺐다 — 진행은 말로도 안 읽고, 물으면 발표 직전 숫자 (디펜스 S13). 숫자 대조: δ = ln 1.5 · 자격 기준 · 2–50 ps · 400 ps · 204 원자 (`cascade_estimand_card_v7_probe*` · `cascade_v7_main_runlog_2026_10_07.json`) · 600 K 판 마감 (`cascade_d_rel_closed_2026_10_01.json`).
> ✅ **사용자 최종 (10-16)** — v1 그대로 (불렛 넷 · 그림 둘 · 캡션 둘 · 맨 아래 줄) + 오른쪽 위 출처 셋을 He → Jung → Phuthi (in press) 순서로. 캡션에 출처가 없으니 그림 출처는 **말로** 댄다 (아래 '왼쪽은 He 등 (2018)' · 'Jung 등 (2026)'). 같은 날 말 두 군데 보탬: 셋째 불렛에 판정 세 갈래 · 넷째 불렛에 탐침 대표 쌍 (1000 K 에서 부모 C 의 P1·P2 × 시드 3·4 까지 통과 · 탐침 출력에 D 없음 · 최종 집계에서 뺌 — `cascade_v7_probe_runlog_2026_10_03.json` · 개정 CP ③④).
> ✎ 10-16 셋째 불렛 한 줄 교체안 전달 (사용자 *'이 내용이 들어가는 … 한줄을 만들어줘'*) — *'After preset checks, D(Al₂O₃)/D(Al₂S₃) is judged different, equivalent, or inconclusive (±ln 1.5).'* (옛 'tested for equivalence' 는 세 갈래 중 하나만 말했다 · 15 pt Carlito 946/973 px 로 한 줄 · 'once' 는 화면에 안 들어가 말로 — 아래 '한 번만'). 대본 셋째 불렛 말도 '동등성 검정' → '95 % 구간을 1.5 배 폭과 비교' 로 맞췄다 (옛 줄 · 새 줄 어느 쪽에도 맞는 말).
> ✅ 10-16 사용자 반영 (*'이렇게 했어'* — 셋째 불렛 교체안 그대로 · 한 줄). 같은 때 전달한 문법 제안 둘 (사용자 판단): ① 둘째 불렛 *'…, fitted over a fixed 2–50 ps window'* 는 'fitted' 가 주어 (precursor) 에 매달린 분사 · 'precursor runs' 도 어색 → *'Each precursor uses 10 start configurations × 2 seeds and a fixed 2–50 ps fitting window.'* (892/973 px · 'fit window' 는 'fit' 이 형용사로 읽혀 'fitting') ② 오른쪽 Jung 그림의 '(b)' 는 원 논문 패널 표지라 왼쪽 He 그림의 (b) 와 이름이 겹친다 (가리거나 말로 'Jung 그림').
> ✅✅ 10-16 **사용자 최종** (*'이런식으로 할게요'*) — ① ② 둘 다 반영: 둘째 불렛 *'Each precursor uses 10 start configurations × 2 seeds and a fixed 2–50 ps fitting window.'* (파랑 그대로) · Jung 그림의 '(b)' 지움. 남은 선택 하나: 왼쪽 캡션 *'fit-window sensitivity'* 를 불렛과 같은 말 *'fitting-window sensitivity'* 로 (사용자 판단 · 말할 내용은 그대로).
지금 돌고 있는 파일럿입니다. 질문은 두 겹입니다.
**전구체의 음이온, 즉 Al₂O₃ 냐 Al₂S₃ 냐가 Al 을 도핑한 Li₆PS₅Cl 의 Li 확산을 바꾸는가 — 그리고 이 프로토콜이 그 차이를 가려낼 수 있는가.**

**[가리킴: 첫 불렛]**
- 두 경우 모두 Al 두 개와 Li 공공 네 개는 같고, Al₂O₃ 쪽만 황 셋이 산소로 바뀝니다.
- 같은 시작 구조, 같은 셀 부피에서 **음이온만 다릅니다.**

**[가리킴: 둘째 불렛 → 왼쪽 그림]**
- 전구체마다 시작 구조 10 개 × 난수 시드 2 개, 모두 40 런입니다. UMA, NVT, 1000 K, 생산 400 ps, 204 원자 셀이고, MSD 는 2–50 ps 로 고정한 구간에서 맞춥니다.
- 왼쪽은 He 등 (2018) 의 그림입니다. 같은 계를 여러 번 돌려도 MSD 가 크게 흩어지고 (a), 맞춤 구간을 길게 잡을수록 맞춤이 나빠집니다 (b). 그래서 반복 수와 맞춤 구간을 미리 정했습니다.

**[가리킴: 셋째 불렛]**
- 보고하는 양은 **두 확산계수의 비**이고, 절대 전도도가 아닙니다.
- 먼저 각 런이 정말 확산 영역에 있는지 미리 정한 점검을 합니다: MSD 부분 구간의 기울기 비, 확산계수 흩어짐, Li 홉 수, 골격 유지.
- 그 다음 시작 구조마다 로그 비를 내고, 그 평균의 95 % 구간을 ±ln 1.5, 즉 1.5 배 폭과 비교합니다. 결과는 셋 중 하나입니다 — 1.5 배 넘게 다르다, 1.5 배 안에서 같다, 아니면 판정 불가. 40 런이 다 끝난 뒤 **한 번만** 분석합니다.

**[가리킴: 넷째 불렛]**
- 처음에는 600 K 에서 같은 설계로 돌렸습니다. Li 은 런마다 4,000 번 정도 홉했지만, 2–100 ps 구간에서 MSD 가 끝내 직선이 되지 않아 **확산계수를 보고하지 않았고** 그 판은 닫았습니다. UMA, 이 셀, 이 부피에서의 이야기입니다.
- 그 뒤 온도는 **미리 정한 짧은 탐침 규칙**으로 골랐습니다. 도핑하지 않은 셀로 먼저 봤는데 800 K 는 점검에서 떨어졌고, 1000 K 에서는 도핑 셀 대표 쌍까지 모두 통과했습니다. 탐침에서는 확산계수 값을 열지 않았고, 그 런들은 최종 집계에 넣지 않습니다.

**[가리킴: 오른쪽 그림 → 맨 아래 줄]** 한계도 분명히 말씀드립니다.
- 셀 크기 약 1.6 nm 는, Phuthi 등이 MLIP 수송 계산에 제안한 벌크 하한 약 2 nm 보다 작습니다.
- 고온에서의 순서가 상온까지 그대로 가지 않을 수 있습니다. Jung 등 (2026) 의 이 그림에서도 1300 K 에서 가장 느린 물질이 700 K 에서는 가장 빠릅니다.
- 그래서 이 결과는 **이 조건에서의 상대 비교**로만 말할 것입니다.

**[클릭]**

## 13. (사용자 13쪽으로 합침 — 위 §12)
> 10-16 사용자 요청으로 옛 13장 (온도 선택 · 진행 · 한계) 은 §12 한 장에 합쳤다. 진행표 (40 런 · 10-12 기준) 는 화면과 말에서 뺐다 — 물으면 디펜스 S13.

## 14. Future plans (사용자 14쪽 · 사용자 틀 유지) ⏱ 21:15
> ✎ 10-16 사용자 14쪽 ('Plan') → v2 (글만 · 사용자 예시 양식) 를 거쳐 사용자 *'이걸 잘 수정해서 reference 빼고 등등'* · *'stage 2 라는 이름은 안들어가나?'* → **v4 = 사용자 틀 그대로** (빨간 점선 'Milestones' 상자 + Phuthi 2026 Fig. 1a). 고친 것: 제목 'Plan' → 'Results & Discussion' (장 순서 규칙 · 사용자 예시) · ■ 'Next calculations' → 'Future plans' (실험까지 들어가는 목록) · 항목 1 'Stage 2 pilot verdict (late October)' · 2 'Stage 2 transport runs beyond the pilot' (옛 'Run scope and ranking margin δ' 는 10-15 결정과 어긋난다 — 목적은 다축 · D_rel 은 수송 한 축 · `D-2026-10-15-cascade-objective-scope`) · 3 'Stage 1 descriptors vs. Stage 2 transport' (명사구 목록에 질문 하나가 섞여 있었다) · 4 'More screening axes for all 91 precursors' (안정창은 12쪽에서 끝 · 계면은 10-15 축 확장 계획의 첫 묶음 · `D-2026-10-15-cascade-screening-axes-plan` · 계산 승인 아님) · 5 그대로 · 그림 위 'Literature:' 꼬리표와 그림 밑 'Reproduced from …' 줄을 빼고 캡션 *'< length and time scales needed for each property >'* + 오른쪽 위 *Chem. Mater.*, in press (2026). (12 · 13쪽과 같은 방식) · 맨 아래 줄 콜론 없앰 *'Next runs will use simulation cells ≥ 2 nm (now ≈ 1.6 nm).'* ('cell' 은 배터리 셀과 헷갈려서 'simulation cells').
> ✎ 10-16 v5 (사용자 *'milestones이라는 단어를 쓰나'*) — 상자 이름 'Milestones' → **'Next steps'**. 'Milestone' 은 랩 덱에 없던 말이다 (08-18 덱은 'Future plan' · 'next step' · 'Milestone' 은 10-13 슬림판 빌더가 처음 넣었다) · 날짜가 붙은 산출물 목록이라는 과제 관리 말이라 순서 목록인 이 상자와 맞지 않는다.
> ✅ 10-16 **사용자 최종** (*'이렇게 했고 각각 설명해줘'*) — v5 에서 제목만 'Plan' 으로 되돌렸다 (사용자 판) · 'vs' 마침표 없음 · 출처 줄은 구분선 아래 오른쪽. 나머지 (Next steps 1–5 · 캡션 · 맨 아래 줄) 는 v5 그대로.

다음 계획입니다. **[가리킴: 왼쪽 상자, 위에서 아래로]**
- 1번, 2단계 파일럿 판정입니다. 이번 달 말쯤 40 런이 끝나면 한 번만 분석합니다. 결과가 차이, 동등, 판정 불가, 기준 미달 중 어느 쪽이든 다음에 할 일을 분석 전에 적어 둡니다.
- 2번, 2단계 수송 계산을 파일럿 밖으로 넓힙니다. 어떤 설계를 몇 런씩 돌릴지는 결과를 보기 전에 정합니다.
- 3번, 1단계 지표가 2단계에서 잰 수송을 예측하는지 봅니다. 순위상관을 신뢰구간과 같이 봅니다.
- 4번, 스크리닝 축을 91 개 전구체 전부에 더합니다. 먼저 NCM 양극과 닿았을 때의 계면 분해와, 가수분해로 H₂S 가 나오는 구동력을 보고, 그 다음 기계적 축과 다른 축으로 넓힙니다. 축마다 보고량을 먼저 정한 뒤에 계산합니다.
- 5번, 모든 축을 묶는 선택 규칙을 결과 전에 정해서 짧은 목록을 만들고, DFT 로 검증한 뒤 실험팀과 합성 · 평가로 넘깁니다. 수송은 그 축 중 하나입니다.

**[가리킴: 오른쪽 그림 → 맨 아래 줄]** Phuthi 등 (2026) 의 그림입니다. 성질마다 계산이 담아야 하는 길이와 시간 규모를 보여 주는데, 벌크 이온전도에는 약 2 nm, 0.3 ns 이상을 제안합니다. 파일럿은 400 ps 라 시간은 넘지만 셀이 1.6 nm 라서, 다음 런부터는 시뮬레이션 셀을 2 nm 이상으로 키웁니다.

**[클릭]**

## 15. Discussion points (사용자 15쪽 · 초안) ⏱ 21:45
> 10-16 새 장 — 요약 장 대신 (사용자 *'summary는 굳이 안들어가용'*). 첫 초안 (선택 규칙의 무게 · GPU 예산 · 새 축 순서 · 실험 조건) 은 사용자 *'이걸 discussion point라고 할 수 있나? 교수님이 대답할 수 있는 거리로 · 우리거에 너무 치중'* 로 바꿨다 — 우리 내부 결정이 아니라 **교수님이 경험으로 답할 수 있는 질문** 넷: ① 같은 도펀트의 산화물 대 황화물 전구체가 실험에서 다른지 (파일럿 질문의 실험 쪽) ② NCM 복합 양극에서 황화물 고체전해질 열화의 주된 원인 (어느 계산 축을 먼저 볼지) ③ 계산 후보를 검증할 측정 ④ 독성 전구체 (As₂S₃) 를 미리 뺄지. 질문 글은 사용자가 고친다.
> ✅ 10-16 **사용자 최종** — 질문 **셋** (넷째 As₂S₃ 독성 전구체 질문은 사용자가 뺐다 · 말에서도 뺐다).

마지막으로 의견을 여쭙고 싶은 것들입니다. **[가리킴: 위에서 아래로]**
- 첫째, 오늘 파일럿 질문을 실험 쪽에서 여쭙고 싶습니다. 도펀트 원소가 같아도 산화물로 넣을 때와 황화물로 넣을 때 상 순도나 이온전도도, 안정성에 차이가 나타나는지요.
- 둘째, 이 스크리닝은 양극재 코팅용 황화물 고체전해질을 대상으로 합니다. NCM 복합 양극에서 열화의 주된 원인이 고전압 산화 분해인지, 계면 접촉 손실인지, 수분인지에 따라 어떤 계산 축을 먼저 볼지가 달라집니다.
- 셋째, 계산이 후보를 추리면 실험으로 검증해야 하는데, 이온전도도, 산화 안정성, 전고체 셀 사이클 중 무엇을 먼저 보는 것이 좋을지 여쭙고 싶습니다.

아직 어느 도펀트가 좋다고 말씀드리지 않습니다. **스크린이 제안하고, 미리 정한 시험이 결정합니다.** 감사합니다.

**[클릭 — Thank you]**

---

### 시간이 모자라면 줄일 곳 (우선순위)
1. 5장의 'Related screens' 는 이름만 읽는다 (−30 초).
2. 7장 표는 1–4 를 "구조와 지표 단계" 로 한 번에 말한다 (−40 초).
3. 10장은 B₀ 두 값만 읽는다 (−20 초).
4. 2장은 둘째 줄 칸을 "SEI 성분 장벽 · 계면 접착 · 바인더 흡착" 한 문장으로 줄인다 (−30 초).
5. 8장의 머신러닝 단락은 첫 문장과 '그래서 라벨부터 다시 만들기로 했습니다' 만 (−25 초).
⚠ 8장(감사)의 네 항목과 에너지 기준 문제는 줄이지 않는다 — 1단계에서 2단계로 넘어가는 이유가 여기 있다.

### 꼭 지킬 것 (말이 새기 쉬운 곳)
- 13장: "Li 이 확산하지 않는다" 라고 말하지 않는다 → "MSD 가 직선이 되지 않아 **확산계수를 정의하지 않았다**".
- 13장: "1000 K 는 확산이 시작되는 온도" 라고 말하지 않는다 → "미리 정한 점검을 통과한 온도".
- 6장 · 7장: "89 개만 계산했다" 고 말하지 않는다 → 91 개 전부 완화·담금질·지표·점수까지 있다 (점수는 8월 표가 89 였고 10-14 에 같은 방법으로 재실행 둘을 더했다).
- 8장: "원소 X 가 Y 효과" 를 1단계 값으로 말하지 않는다 → "지금 라벨로는 원소 효과를 읽을 수 없어서 라벨부터 다시 만든다". 잡음비 숫자는 감사 값 (1.1 · 0.2) 만 말한다 — 10-14 빠른 점검 값은 표본이 달라 디펜스에만.
- 7장: 점수 순위를 결과로 말하지 않는다 → "8월 방법의 탐색 점수이고, 다음 장에서 왜 순위로 못 쓰는지 말씀드리겠다". 막대에서 특정 전구체를 짚지 않는다.
- 8장: "가짜 basin 이 확정됐다" 고 말하지 않는다 → "기준 부피가 같은 조성의 DFT 평형보다 40 % 정도 컸다". 237 을 "계산한 수" 로 말하지 않는다 → "설계 목록".
- 10장 (사용자 11쪽): "탄성상수가 GPU 에서 돌고 있다" 고 말하지 않는다 → "슈퍼셀 수렴 확인이 진행 중" (지금은 다른 계산 때문에 세워 둠). 단일 셀 탄성 값 · 두 조성의 탄성 비교는 말하지 않는다 (확인 전 · `HZ-elastic-cross-composition`). 27.48 을 "UMA 가 부피를 부풀렸다" · "가짜 basin" 으로 말하지 않는다 (둘 다 가설) — 물으면 디펜스 S8 · S10.
- 8장 오른쪽 아래 블록: "9월 감사에서 찾았다" 고 말하지 않는다 → "이번에 점수를 다시 매기면서 찾았다". 근거 숫자 (상관 · 데모) 를 화면 근거로 들지 않는다 — 물으면 디펜스 S8 (정의 · 음이온족 평균) 까지.
- 7장 · 9장 · 14–15장: "어느 도펀트가 좋다" 는 답을 하지 않는다 → "지금 지표는 탐색용이고, 고르는 것은 모든 축을 묶는 규칙을 결과 전에 정한 뒤" (10-15 결정 — D_rel 하나로 고르지 않는다 · '순위 여유' 라는 말은 쓰지 않는다).
- 2장: 숫자는 하나도 읽지 않는다 (접착에너지 값 · li2s 수송값은 어디서도 말하지 않는다).

### 슬림판으로 발표할 때 (`…_progress_lean.pptx`)
교수님용 슬림판은 장 순서 · 번호 · 메시지가 같다. **08-18 덱의 문법**으로 짰다 — ■ 한 줄 + bullet ≤ 2 (핵심어 파랑 · 주의 빨강) + 그림/표 하나 + `< 캡션 >` + 색 강조 한 줄,
과정은 08-18 덱 4장의 **빨간 점선 번호 박스 + 아래 화살표**. 카드 · 배지 · 아이콘 · 큰 숫자 타일은 쓰지 않았다 (10-12 사용자 *"딱 ai가 만든 느낌"* 뒤 다시 짬).
아래 '말로 채울 것' 은 위 대본의 같은 장에 이미 있다 — 화면에 없으니 **읽지 말고 말한다**.

**10-13 Codex 미감 리뷰 (편지 CW · 조건부 GO) 반영** — 화면 관계를 잘못 읽힐 세 곳 (11 · 12 · 13장) 을 먼저 고쳤고, 그림을 키우고 그림 밑 마무리 문장을 말로 옮겼다.
문헌 그림 다섯은 전부 **그림 위 꼬리표 'Literature: …' + 아래 'Reproduced from …'** 이다 — 우리 결과로 읽히지 않게. '순위는 아직 없다' 는 화면에서 **8장 분홍 상자에 한 번** 나온다 (15장 요약은 10-16 에 뺐다).

| 장 | 슬림판 화면 | 말로 채울 것 |
|---|---|---|
| 2 | ■ 'Earlier DFT studies: the basis of this screening' · bullet 둘 (Top row: bulk materials and their doped or coated forms · Bottom row: SEI components, interfaces, and binders in a battery cell) + 그림 자리 8칸 (제목 + `< 키워드 >`) | 칸마다 한 줄 (대본 2장) · 마무리 '이 경험들이 스크리닝의 단계가 됐다' + 짝 다섯 (EOS → 기준 계산 · BVSE → Li 지형 · MD → 수송 · 대권위 상도표 → 안정창 · 계면 에너지 → 계면 반응성) — 숫자는 0 개 |
| 3 | ■ 'Choosing a dopant precursor for Li₆PS₅Cl' · bullet 둘 (In the lab, dopants are added as compounds, not as bare elements. · This work screens 91 candidate precursors by simulation before synthesis.) + 점선 박스 'An example' (Al₂O₃ → Al + O · Al₂S₃ → Al + S · Same Al, different partner anion · Does the anion change stability or Li transport?) + 화살표 + 'To answer this question, we must check electrochemical stability, mechanical stability, and Li transport separately.' | 앞 장의 도핑 계산 → 범위를 넓힘 → 넣는 건 화합물 → 예 · 질문 → 세 가지를 따로 (대본 3장) · 아래 줄 = 다음 장으로 가는 다리 · 상자는 예 하나 · 답은 말하지 않는다 · 진행 숫자는 13장에서 |
| 4 | ■ 'Failure modes in sulfide-based all-solid-state batteries' · bullet 둘 (reinforce each other · A dopant that suppresses one mode can worsen the other, and the trade-off goes undetected unless each mode is evaluated separately.) + Kang 2026 Fig. 16 + 출처 'Kang et al., …' | 앞 장 '왜 따로' 에 답 · 두 열화 → 서로 키우는 고리 → 가운데 SE doping → 따로 재는 이유 (대본 4장) · 그림 오타는 원 논문 그대로 |
| 5 | ■ 'Prior dopant screens and what this study adds' · bullet 둘 + 표 6 행 (Miara 2015 · Xiao 2019 · Lee 2024 · Muy 2025 · Jung 2026 · this work · 출처는 오른쪽 위 다섯 줄) | what is varied 열이 핵심 → this work 행 → 기계 축은 새로움이 아님 (대본 5장 · 논문별 브리핑 = 디펜스 S5) |
| 6 | 08-18 덱의 족별 표 (family · n · examples — 'role in the design' 열은 뺐다 · 사용자 10-13) + **[문헌] 'Literature example: SiO₂ co-doping'** Jung 2026 Fig. 3d | 족별 역할은 말로: 산화물 = 강한 M–O 결합 · 염화물 = 호스트에 이미 Cl · 황화물 = 호스트와 같은 음이온 (대조) · 플루오르화물 = 가장 강한 결합 · 이동성 위험 · 브로민화물 · 요오드화물 = 더 큰 할라이드 (대조) · 질화물 = 더 높은 음이온 전하 (대조) · 공치환 실험 선례 CuCl · MgF₂ · ZnO · La₂O₃ · Nd₂O₃ · SiO₂ (17장) · 문헌 그림은 '선례' 이지 우리 후보의 검증이 아니다 · As₂S₃ 재실행은 7장 |
| 7 | ■ 'Stage 1: screening pipeline (first attempt)' + 작은 불렛 둘 (항 다섯 · 0–1 · 손 가중치 / 에너지·탄성률·안정창에서만) + 왼쪽 점선 박스 'Pipeline' 다섯 단계 (오른쪽 회색 = 91 · 3,675 · 693 selected · 91 · 91) + 오른쪽 **8월 방법 점수 상위 10 막대** (91 개 · 강조 없음) + 캡션 둘 — 10-14 사용자 *'예전 파이프라인'* → *'틀린거라도 랭킹 한번 추가 · 옆에 plot'* | 단계마다 한 줄 · 점수는 8월 방법 그대로 + 재실행 둘 (91) · 끝 질문 '이 순위를 그대로 써도 될까요?' → 8장 감사 · 점수식 · As₂S₃ 53 위 · AlI₃ 38 위 · 남은 것 셋은 물으면 · ⛔ 막대에서 전구체를 짚지 않는다 |
| 8 | (10-15 **빨간 블록판 기본**) 두 목록 (Audit findings 4 · Decisions recorded on Sep 12 4 + 빨강 다섯째 'A ranking margin δ, proposed but not yet set') + 분홍 상자 'Stage-1 outputs are kept as exploratory data; no dopant ranking has been approved.' + 'The run scope is set after the pilot.' · 옛 판 (Oct 14 블록) 은 검토본 | 'Found on Oct 14' 두 줄 + 녹는 에너지 시연 한 줄은 말로 (숫자 없이) · 두 목록은 행끼리 짝이 아니다 · 머신러닝은 한 줄 |
| 9 · 10 | 9 (10-15): 열지도 + 담금질 도식 (작게) + **담금질 에너지 변화 히스토그램 (693)** + 맨 아래 줄 (모두 더 낮아짐 · 중앙 −0.81 eV / 52 원자 셀) · 10 (10-15 사용자 11쪽 교체본 v2): 불렛 둘 (B₀ · V₀ / 탄성 + 슈퍼셀 수렴 확인 진행 중) · 라벨 V₀ per f.u. + Li₆PS₅Cl 원자당 19.55 (파랑) · 캡션 · 출처 오른쪽 위 랩 표준 · **맨 아래 줄 27.48 Å³/원자 = DFT V₀ 의 1.41 배** | 9: '지표에 따라 같은 전구체 안 흩어짐 ≈ 전구체 사이' 는 말로 (8장 감사 셋째 항목의 근거) · 8월의 'top ten unchanged' 는 말하지 않는다 · 10: '그래서 2단계는 DFT 평형 호스트에서' 는 말로 · 탄성 값은 말하지 않는다 |
| 11 | (10-14 감사 뒤) ■ Decomposition stability window · 호스트 창 그림 + **[문헌] 'Literature: decomposition and intrinsic windows'** Schwietert 2021 Fig. 1 (크게) | 우리 정의 = 그 논문의 decomposition window · 옛 정의가 넓었던 이유 · 계면 산물은 10-14 에 바닥상태 상으로 다시 냈고 아직 안 쓴다 (둘 다 화면 줄은 뺐다) · 화면 bullet 은 91 전구체 · '창 없음' |
| 12 | **[문헌] 'Literature: run-to-run spread and fit-window sensitivity'** He 2018 Fig. 3 + 'Our pilot: 10 start configurations × 2 seeds per precursor; 2–50 ps fit window.' | 그림은 '왜 반복과 고정 창이 필요한가' 의 근거이고, **10 × 2 · 2–50 ps 는 우리가 정한 값**이다 (그림에서 나온 숫자가 아니다) · 설정 UMA · NVT 1000 K · 400 ps · 204 원자 · 40 런 (화면 줄은 뺐다) · 점검 넷 · 동등성 검정 (±ln 1.5) |
| 13 | ■ Stage 2 pilot at 1000 K · 명단 (끝 12 · 진행 1 · 대기 27) + **[문헌] 'Literature: temperature-dependent ordering'** Jung 2026 Fig. 5b | 600 K 판을 닫은 이유 · 한계 둘 · 끝나는 날 10월 21일 무렵 (화면에서 뺐다) · 오른쪽은 **문헌 물질** (Li₉P₃OS₁₁ 등) 이다 — 우리 Al₂O₃ / Al₂S₃ 순서를 말하는 그림이 아니다 |
| 14 | (10-16 사용자 14쪽 · 사용자 틀) ■ Future plans · 빨간 점선 'Next steps' 1–5 (1–3 에 Stage 이름) + Phuthi 2026 Fig. 1a + 캡션 '< length and time scales needed for each property >' + 맨 아래 줄 'Next runs will use simulation cells ≥ 2 nm (now ≈ 1.6 nm).' · 출처 오른쪽 위 (*Chem. Mater.*, in press (2026).) | 항목마다 한 줄 (대본 14장) · 결과 네 경우별 다음 일 · 축마다 보고량 먼저 · 수송은 한 축 · 그림은 Phuthi 의 하한 약 2 nm · 0.3 ns |
| 15 | (10-16 · 요약 장 대신) ■ Discussion points · 한국어 질문 셋 (교수님이 경험으로 답할 수 있는 것 · 사용자 최종) | 질문마다 한 문장 배경 (대본 15장) · 마무리 '스크린이 제안하고, 미리 정한 시험이 결정한다' |
| 20–23 | **백업 (10-15 · 사용자 '권고대로')** — 08-18 덱 Step 3 · 4 · 5 · 8 을 **그대로** (고치지 않음) · 머리 'Backup' + 오른쪽 위 빨간 표지 'August 18 version, superseded' 와 바뀐 이유 한 줄 | 질문이 올 때만 꺼낸다 · 각 장 표지대로 무엇이 바뀌었는지 말한다 (부피 기준 · '상위 3' 아님과 에너지 축 · 'top ten' 철회 · 안정창 정의) — 숫자는 디펜스 §1 표 안에서만 |

- 우리 그래프 넷은 CSV 에서 그린 **수수한 미리보기**다 (`kb/seminars/assets_2026_10_13/fig_p06 · p07 · p10 · p13` · 생성 `export_cascade_briefing_csvs_2026_10.py --figures`). Origin 으로 다시 그리면 같은 자리에 바꿔 넣는다. 10-13 부터 p06 (가로 막대) 은 **슬라이드에 들어가는 크기로** 그려서 (p07 커버리지 그림 `fig_p07_stage1_coverage.png` 은 10-14 에 슬림판에서 빠졌다 — 파이프라인 박스로 바꿈 · CSV 는 질문용으로 남김) 그림 속 글씨가 화면 글씨와 같다 (13–14 pt) — Origin 판도 그 크기에서 글씨를 맞춘다. 족별 구조 수 CSV (`p07_structures_by_anion_family.csv`) 는 Origin 용으로 남겼다.
- **[문헌] 그림 다섯은 litdb 크롭을 그대로 잘라 썼다** (다시 그리지 않음 · 우리 숫자와 한 그림에 안 섞음) — `lit_jung2026_sio2_fig3d` · `lit_schwietert2021_fig1` · `lit_he2018_fig3` · `jung2026_fig5b` · `lit_phuthi2026_fig1a`. 10-12 에 직접 봤다.
- 3장 화살표는 08-18 덱 4장의 **원래 그림 그대로**다 — 사용자 표준 (10-13 *'화살표는 원복했어 저게 표준이야'*). Codex CW 가 흐리다며 벡터를 권했지만 쓰지 않는다.
- 11장 (10-14 전 10장) 질문 대비: 우리 환원 끝 1.717 V 는 Schwietert 2021 decomposition window 의 1.72 V 와 같고, 산화 끝은 MP 보정 규약 때문에 다르다 — **화면에는 숫자 비교를 안 싣는다** (디펜스 S11).
- 진행 숫자(3 · 13 · 15장의 12/40 과 명단 그림)는 **두 덱 모두** 발표 전에 바꾼다 — run log 를 갱신하고 `--figures` 를 다시 돌리면 명단 그림도 따라온다.
- 빌드: `python3 kb/seminars/build_cascade_briefing_2026_10.py <08-18 덱> <출력.pptx> <pptx 스킬 폴더> kb/seminars/assets_2026_10_13 --lean` (플래그 없으면 상세판).
