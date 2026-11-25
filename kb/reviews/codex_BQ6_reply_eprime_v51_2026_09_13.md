---
title: 회신 BQ-6 — ①③ 해제 · ② 미해제 (도구가 검사하는 것 ≠ 카드가 선언한 것)
kind: review-reply
date: 2026-09-13
updated: 2026-09-13
tags: [cascade, eos, cell-policy, review, codex, bq6, eprime, estimand, msd]
status: 회신됨-②미해제
confidence: high
verificationStatus: unverified
explored: false
authoredBy: external
claimType: prescriptive
---

# 회신 BQ-6 (2026-09-13 심야 · 원문 그대로)

> 요청: `codex_BQ6_prompt_eprime_v51_2026_09_13.md` (대상 커밋 `0fcdfdbc`)
> ⛔ 리뷰어 원문이다. 고쳐 쓰지 않는다. 리뷰어 로컬 경로는 저장소 상대경로로 읽는다.

---

카드 확정은 아직 NO-GO예요. ①의 일차 집계와 ③의 비용 승인 절차는 해제 가능하지만, ②에는 핵심 P0 두 건이 남습니다.
0fcdfdbc의 v5.1 카드와 실제 함수를 대조했고, 합성 MSD 두 사례로 확인했습니다. 파일 수정이나 UMA·MD·DFT 계산은 하지 않았어요.

## Q1. 집계·결측·구간식 — 일차는 해제, ΔEa는 한 줄 명확화

속도 시드 산술평균 → 부모별 비 → 로그 집계, df=1 구간, 구간 위치 판정과 결측 처리는 앞선 요구대로입니다. 소표본 작업 가정도 명시했으므로 다시 문제 삼지 않겠습니다.
다만 [카드 67행 (line 67)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json:67)의 ΔEa에 "집계식 3·4와 동일"이라고만 쓰면, 4번의 지수변환까지 따라갈 여지가 있어요. 다음처럼 풀어 쓰세요.

\[
a_k=\Delta E_{a,k},\quad
\bar a=(a_A+a_B)/2,\quad
SE_a=|a_A-a_B|/2
\]
\[
CI_a=\bar a\pm12.706\,SE_a
\]

meV 척도에서 로그·지수변환 없이 ±30 meV와 비교합니다. 두 부모의 ΔEa가 모두 유효해야 해요. 이 명시로 ①은 닫을 수 있습니다.
또 "문턱이 로그이므로 집계도 반드시 로그여야 한다"는 필요조건은 아닙니다. 이번에 기하평균을 선택했다고 쓰면 충분해요.

## Q2. 도구 규약으로 바꾼 판정 — 미해제

β를 경보로 내리고, 골격 이동을 결합 재배열로 단정하지 않은 방향은 맞습니다. 하지만 기존 도구를 선택했다고 그 도구의 의미까지 검증된 것은 아니에요.

**P0-1. MSD/d²는 실제 독립 홉 수가 아닙니다**
[해당 함수 (line 213)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/tools/ionic/msd_diffusive_check.py:213)는 궤적의 사건을 읽지 않고 max(MSD)/9만 계산합니다.
실제 함수에 합성 MSD를 넣으면 다음과 같아요.

| 합성 MSD, t=1–100 ps | MSD 기반 값 | 판정 |
|---|---|---|
| 0.1t | 1.111 | HOLD |
| 27 + 0.1t | 4.111 | CITABLE |

두 곡선은 기울기 D가 같고 D_inc 네 창도 모두 plateau입니다. 절편만으로 "홉 충분성" 판정이 바뀌어요.
따라서 이것은 MSD 크기에 의존하는 대용값이지, 실제 독립 사건 수가 아닙니다. 일반적인 사건 수 하한이라는 설명도 성립하지 않아요. 길이 d의 이동을 같은 방향으로 두 번 하면 사건은 2개지만 순변위 제곱/d²은 4입니다. 다른 계에서 관측한 상관계수를 이 파일럿에 자동 승계할 수도 없어요.
최소 수정은 역할을 분명히 선택하는 것입니다.
- 기존 2.5 Å 사건 계수를 유지한다면, 독립성이 입증된 사건 수가 아니라 선언한 변위 사건 수라고 쓰세요.
- MSD 기반 값을 유지한다면, MSD 규모에 대한 운영 기준으로 명명하고 실제 홉·독립 표본수·정밀도 확보의 증거로 사용하지 마세요. 기존 사건 게이트를 제거한 정책 변경도 명시해야 합니다.
새 MD를 더 돌리라는 요구는 아닙니다.

**P0-2. run_verdict에는 부창 선형성 검사가 없습니다**
[판정 함수 225행 (line 225)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/tools/ionic/msd_diffusive_check.py:225)은 D_inc plateau와 위 MSD 대용값을 검사합니다. 카드의 세 부창 기울기 비 [0.8,1.2] 검사는 호출하지 않습니다.
합성 재현에서도:
- D_inc 창 끝점을 유지하는 변동을 MSD 중간에 추가하면 plateau 산포는 0입니다.
- 부창 기울기 비는 0.773 / 1.501 / −0.118로 모두 기준 밖입니다.
- 그런데 run_verdict는 CITABLE을 반환합니다.
따라서 [카드 133행 (line 133)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json:133)의 "run_verdict 세 축"은 사실과 다릅니다.
카드 단계에서는 어떤 검사들을 합쳐 최종 집계 자격을 정하는지를 명시하면 됩니다. 구현에서는 부창 실패가 실제로 집계를 막는지 위 같은 합성 사례로 확인하세요. 함수 하나의 CITABLE을 전체 통과로 승격하면 안 됩니다.

**P1. 골격 경보의 실제 범위도 적어야 합니다**
[`framework_com_split` (line 1015)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/tools/ionic/msd_diffusive_check.py:1015)은 모든 비-Li 원자의 이동을 동일하게 검사하지 않아요.
- 판정용 평균에서 원소 수가 8 미만인 종을 제외하므로 Al₂·O₃는 빠집니다.
- 첫 프레임 대비 마지막 프레임의 MSD를 사용합니다. 일차 D의 시간원점 평균·2–50 ps 적합창과는 다른 양입니다.
이 범위로 경보를 사용할 수는 있지만, 전체 비-Li 연결성·이동을 인증한다고 쓰면 안 됩니다. 입력 궤적의 구간·좌표계를 명시하고, 함수가 None을 반환하면 "경보 없음"이 아니라 검사 불가로 처리하세요.

## Q3. 비용 승인 절차와 실패 전파 — 절차는 해제

수정한 네 단계는 맞습니다.
- 첫 준비 전에 총상한 승인.
- 첫 H0 런은 30런에 포함하고 별도 소상한 적용.
- 실측으로 남은 배치의 비용을 판단.
- 실제 누적 사용량에서도 중단.
두 숫자의 크기는 요청대로 판정하지 않았습니다. 현재는 제안값·미비준이므로 실행 승인은 아닙니다.
실패 전파 일곱 규칙도 앞선 표를 충족합니다. 구현 조건은 누적 사용량 = 상한이 아니라 **≥ 상한**으로 쓰세요.

## Q4. 확정 전에 남은 문구 정리

새 절을 추가했지만 구판 문장이 본문에 남아 있습니다.

| 위치 | 남은 충돌 |
|---|---|
| [카드 125행 (line 125)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json:125) | 여전히 "골격 연결성(β_framework로 감시)" — 새 92행과 충돌 |
| [131행 (line 131)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json:131) | "다섯 중 하나 실패→그 부모" — H0 예외가 없음. 새 실패 전파 규칙을 참조하도록 통일 |
| [113행 (line 113)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json:113) | "H0가 1.96% 작다" 잔존 — 1.923%로 정정 |
| [결정 원장 1994행 (line 1994)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_bq6_20260913_0fcdfdbc/checkout/db/governance/decisions.json:1994) | "완화 상태 다수성 실측" 잔존 — 두 준비 경로의 종료 구조 차이로 한정 |

4066.480은 정상적인 반올림 표시이므로 오류가 아닙니다. 중요한 조건은 이미 채택한 원본 셀 행렬 유지예요.
정리하면, ①은 ΔEa의 단위·변환 명시로 해제, ③은 절차 해제·저자 비준 대기, ②는 미해제입니다. 남은 핵심은 보고량을 다시 설계하는 일이 아니라, 도구가 실제로 검사하는 것과 카드가 검사한다고 선언한 것을 맞추는 일입니다.
