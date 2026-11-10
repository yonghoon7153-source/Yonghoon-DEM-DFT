---
title: "EA 회신 — b2o3 어닐 시간 진단 (개정 3): 개정 3 문구 · 비교 규칙 그대로의 최종 판정은 보류 (P0 0 · P1 2 · P2 2) — D1 · D2 진단은 찬성 · 54 런은 계속 · 해제 조건 셋 (판정 사유 분리 · 성공 집합 불일치 처리 · 결과 공개 전 도구 결속 · 정상/음성 경로)"
date: 2026-11-10
updated: 2026-11-10
tags: [review, b2o3, doping, uma, anneal, placement, codex, reply, letter]
letter: EA
track: b2o3
channel: codex
kind: reply
status: 원문 보존 (사용자 붙여넣기 2026-11-10) · 반영 = 카드 개정 4 · 진단 도구 고침 (결과 전)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: low
claimType: mixed
evidenceScope: single-source
---

> 원문 그대로 (사용자가 2026-11-10 에 붙여 넣은 Codex 회신 · 프롬프트 `codex_EA_prompt_b2o3_anneal_time_diagnostic_2026_11_10.md`). 기준 커밋 b018b14d (진단 도구 c0ed861c 이전 판 — 회신은 "새 진단 도구는 아직 구현되지 않았다" 고 적었다). 붙여넣은 글의 첫 줄이 '-GO —' 로 시작한다 (앞 글자가 잘린 채 붙었다 · 내용상 '현재 개정 3 그대로의 최종 판정은 보류'). 끝의 JSON 두 덩이는 회신이 링크한 재현 자료 (`synthetic_reproductions.json` · `cohort_reproductions.json` 으로 보임) 를 사용자가 같이 붙인 것이다. 링크의 로컬 경로는 Codex 쪽 작업 폴더다.

---

-GO — 현재 개정 3의 문구와 비교 규칙 그대로 최종 판정을 내리는 것은 보류입니다. D1·D2 진단 자체에는 찬성하며, 진행 중인 54런을 중단하거나 다시 돌릴 이유는 찾지 못했습니다.
`b018b14d` 기준으로 카드·결정·판독기·어닐 실행기를 확인했습니다. 판독기와 실행기는 DY 확인판과 동일합니다. 판독기 selftest 69/69, 어닐 실행기 selftest 통과를 재현했습니다.
추가 검증은 합성 에너지·시험용 구조로 수행했습니다. 8단계 생산 에너지와 궤적은 열지 않았고, UMA·DFT·생산 MD도 실행하지 않았습니다. 새 진단 도구는 아직 구현되지 않았으므로, 아래는 규칙 심사와 구현 전 확인 조건입니다.
P0 — 이번 범위에서 재현한 사항은 없습니다.
P1-1. 판정 부족을 실제 순서 역전으로 바꿔 말합니다.
위치: [카드:284 (line 284)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/db/properties/b2o3_bo_placement_estimand_2026_11_09.json:284)
현재 규칙은 50 ps가 다른 승자이든, 회색 띠이든, 보류이든 모두 “순서가 어닐 시간에 따라 바뀐다”고 씁니다. 실제 `anneal_judge`로 다음을 재현했습니다.

* 순서가 그대로인데 역전이라고 쓰는 경우: 50 ps의 최저–차점 차가 0.10 eV, 100 ps는 0.40 eV. 두 시점 모두 `F_B < F_P < F_free`지만, 50 ps가 승자 문턱을 못 넘었다는 이유로 “순서 변화”가 됩니다.
* 비교할 자료가 부족한데 역전이라고 쓰는 경우: 50 ps의 한 가족 성공 수가 14/18이라 G1 보류. 이 경우에도 “순서 변화”가 됩니다.
* 승자만 같은데 전체 순서가 같다고 쓰는 경우: 두 시점 모두 F_B 승자이지만 F_P와 F_free의 순서는 뒤집혀도 “같은 순서”가 됩니다.

최소 수정: `같은 승자 / 다른 승자 / 여유 부족 / 판독 보류`를 구분하세요. 확인하는 것이 승자 일치라면 표현도 **“두 시점에서 같은 가족이 선택됐다”**로 한정하면 됩니다. 전체 순서 일치를 새 조건으로 추가할 필요는 없습니다.
P1-2. 성공한 런이 시점마다 달라지면, 시간 효과와 비교 대상 변경이 섞입니다.
위치: [카드 D2:278 (line 278)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/db/properties/b2o3_bo_placement_estimand_2026_11_09.json:278), [판독기:586 (line 586)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/tools/doping/b2o3_bo_readout.py:586)
각 시점에 G1을 적용하는 것만으로는 두 시점이 같은 런 집합의 최저값을 비교한다는 보장이 없습니다.
다음 반례를 재현했습니다.

* 각 런의 에너지는 50·100 ps에서 전혀 변하지 않습니다.
* F_B에 낮은 에너지 런 두 개가 있습니다. 50 ps에서는 그중 하나가 실패하고, 100 ps에서는 다른 하나가 실패합니다.
* 두 시점 모두 F_B 성공 17/18, F_B 승자, 차이 1.00 eV입니다.
* 그러나 두 시점에 공통으로 성공한 런만 보면 F_P 승자, 차이 0.50 eV입니다. 이때도 F_B 성공은 16/18로 G1을 통과합니다.

반대로 실패한 런만 바꿔 에너지 변화 없이 승자 역전도 만들었습니다. 따라서 지금 규칙의 일치·불일치 모두 실패 집합에 영향을 받을 수 있습니다.
최소 수정으로는 다음을 권합니다.
시간 비교에 쓰는 성공 런 이름 집합이 가족별로 두 시점에서 같아야 한다. 다르면 100 ps 본 판정은 보존하되, 시간 일치 확인은 보류한다.
이는 54개 전부 성공하라는 요구가 아닙니다. 양쪽의 성공 집합이 같고 기존 G1을 통과하면 됩니다. 공통 성공 집합으로 추가 판독하는 대안도 가능하지만, 그 방식을 택한다면 원래 계획의 분모를 유지하는 규칙까지 결과 전에 고정해야 합니다.
P2-1. Δ의 ‘중앙·IQR·최대’는 최저값을 움직인 큰 하강을 놓칠 수 있습니다.
위치: [카드:280 (line 280)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/db/properties/b2o3_bo_placement_estimand_2026_11_09.json:280)
`최대`를 부호 있는 `max(Δ)`로 구현하면 문제가 됩니다.
합성 시험에서 세 가족 모두 Δ 중앙값 −0.4 eV, IQR≈0, 최댓값 −0.4 eV였습니다. 그런데 F_B 한 런만 −3.0 eV 내려가면서 승자–차점 차가 0.30→2.73 eV, F_B 최저 런도 다른 런으로 바뀌었습니다.
최소 수정: 기존 항목에 최솟값·최댓값, 두 시점의 가족 최저 런 ID, 그 런들의 Δ를 추가하세요. “최대 변화”를 뜻했다면 `max|Δ|`라고 명시해야 합니다. 런별 Δ 전체를 남기는 현재 계획은 유지하면 됩니다.
P2-2. 도구 고정 시점을 100 ps 결과 공개 전으로 명확히 해야 합니다.
위치: [카드:286 (line 286)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/db/properties/b2o3_bo_placement_estimand_2026_11_09.json:286)
현재 문구는 D1을 “본 판독이 끝난 뒤” 수행하고, 새 도구는 “진단 결과를 읽기 전” 커밋한다고 합니다. 그대로면 100 ps 승자를 본 다음 진단 구현의 빈칸을 결정할 여지가 있습니다. 이미 그렇게 했다는 지적은 아닙니다.
최소 수정: 카드 개정·실패 처리·비교 집합·진단 도구와 음성시험을 50 ps 및 100 ps의 본 결과를 읽기 전에 고정하세요. D1 계산 자체를 8단계 완료 뒤에 수행하는 것은 괜찮습니다.
Q1. 두 시점 일치 규칙은 충분한가?
제한된 시간 민감도 확인으로는 유효합니다. 수렴 증거로는 부족합니다.
같은 궤적의 앞뒤를 비교하는 것은 여기서 결함이 아닙니다. 출발 구조와 난수 경로를 공유하므로, 서로 다른 궤적 두 개보다 시간 변화의 영향을 직접 볼 수 있습니다. 다만 독립 재현 두 번으로 세면 안 됩니다.
고친 규칙이 확인하는 것은 다음뿐입니다.
선언한 탐색에서 50 ps와 100 ps의 이완 끝점을 비교했을 때, 같은 초기 가족이 두 시점 모두 0.20 eV 문턱을 만족했다.
다음은 확인하지 못합니다.

* 100 ps 뒤에도 같은 가족이 선택되는가.
* 다른 속도·잡음 시드에서도 같은가.
* 같은 구조적 골짜기에 머물렀는가.
* 전체 구조 공간의 최저 상태인가.

파일럿의 마지막 변화 0.358 eV가 0.20 eV보다 크다는 사실도 가족 간 비교가 자동으로 무효라는 뜻은 아닙니다. 절대 에너지 변화와 가족 간 차의 변화는 다른 양입니다. 또한 세 점 지수 적합의 “잔여 ≈0.1 eV”는 오차 상한으로 쓰지 마세요.
Q2. 가족 최저를 계속 써도 되는가? 중앙값이나 짝 규칙을 필수로 걸어야 하는가?
선언한 탐색에서 찾은 최저 구조를 비교하려는 목적이라면 최저값을 유지해도 됩니다. 중앙값으로 바꾸면 보고량이 달라집니다.
다만 최저값이 항상 “가장 많이 내려간 런”인 것은 아닙니다. 시작 에너지와 내려간 정도가 함께 결정합니다. 정확한 우려는 유한한 탐색에서 드물게 도달한 낮은 끝점 하나가 가족 대표가 된다는 것입니다.
실제 함수로 다음을 확인했습니다.
F_B는 18개 중 하나만 −1.0 eV이고 나머지 17개는 +0.2 eV, F_P는 전부 0 eV인 경우, 두 시점 모두 F_B 승자가 될 수 있습니다. 그러나 중앙값은 F_P가 낮고, F_B가 낮은 공통 짝은 1/18뿐입니다.
이것은 최저값 보고량의 오류는 아닙니다. “F_B가 전반적으로 유리하다”는 확장이 틀리는 경우입니다.
따라서 이번에는 중앙값·짝 일치를 새 승자 게이트로 강제하지 않고, 최저값 판정 옆에 분포와 기존 짝 판정을 함께 표시하는 쪽을 권합니다. 그리고 F_B 등의 라벨은 초기 가족입니다. 최저 구조의 실제 끝 꼴도 함께 적어야 하며, “F_B 출발군이 최저를 찾았다”를 바로 “B–O 꼴이 가장 안정하다”로 바꾸면 안 됩니다.
Q3. 추가 진단 셋 중 무엇을 할까?
제 권고는 이번에는 D1·D2와 md.log 진단까지입니다. 추가 MD를 승인 조건으로 걸지는 않겠습니다.

* (가) 같은 파일럿 구조의 추가 시드 3개: 그 출발 구조의 궤적 간 산포를 확인하는 데 유효합니다. 세 초기 가족·18바탕의 탐색 불확실성을 대표하지는 못합니다. 실시한다면 초기 속도뿐 아니라 Langevin 잡음 시드도 독립적으로 바뀌는지 확인해야 합니다.
* (나) md.log 구간 평균: 비용 없이 볼 가치가 있습니다. 비교 구간을 먼저 고정하고 온도와 함께 보세요. 다만 MD 중 열적 요동을 포함한 에너지와, 셀까지 이완한 끝점 에너지는 다른 양입니다. 로그가 평평해도 D1을 대신하지 못합니다. 열적 배치와 그 배치를 이완해 도달한 최소를 구분하는 근거는 [Stillinger–Weber의 원 논문](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.25.978)에 있습니다.
* (다) 승자·차점만 200 ps: 선택한 구조가 더 내려가는지 보는 탐침으로는 가능합니다. 그러나 이것으로 가족 순위를 갱신하면 일부 가족·구조에만 탐색 시간을 더 준 비교가 됩니다. 특히 세 번째 가족을 배제한 채 “순위가 안정됐다”고 할 수 없습니다. 이번 판정 구제용으로 쓰지 말고, 필요하면 후속 탐색 규칙으로 별도 고정하세요.

Q4. 공통 드리프트의 기준을 미리 정할 수 있는가?
먼저 무엇이 상쇄되는지를 구분해야 합니다.
같은 바탕 \(i\)에서 가족 F와 G의 차가 얼마나 변했는지는
\[ \delta_{FG,i} =(E_{F,i}^{100}-E_{G,i}^{100}) -(E_{F,i}^{50}-E_{G,i}^{50}) =\Delta_{F,i}-\Delta_{G,i} \]
로 직접 계산할 수 있습니다.
그러나 바탕마다 공통인 변화가 가족 최저값 비교에서도 상쇄되는 것은 아닙니다. 실제 합성 시험에서 각 바탕의 세 가족에 똑같은 변화를 줘 모든 짝 차를 보존했는데도, 서로 다른 바탕에서 최저값이 선택되면서 F_B 승자→F_P 승자로 바뀌었습니다.
따라서 둘을 함께 남겨야 합니다.

1. 같은 바탕·같은 런의 가족 차 변화 \(\delta_{FG,i}\).
2. 각 시점의 가족 최저값 \(m_F(t)\), 그 ID, 그리고 \(m_G(t)-m_F(t)\)의 변화.

이번에는 ‘공통 드리프트 통과’라는 새 수치 게이트를 만들지 않는 쪽을 권합니다. 파일럿 세 점에서 그 허용폭을 도출할 수는 없습니다. 위 차들을 그대로 보고하고, 이미 선언한 0.20 eV 선택 규칙과 두 시점 일치 조건으로 제한하세요.
분포가 비슷하다는 관측을 **“Li 재배열이라는 공통 과정이 원인”**으로 해석하는 것도 별도 구조 근거 없이는 불가합니다.
Q5. 승자·하향 문구는 어떻게 쓸까?
승자 문구는 아래 정도면 충분합니다.
선언한 초기점 생성·탐색 절차에서, 초기 가족 F의 최저 이완 에너지가 500 K·100 ps 어닐 뒤 가장 낮았다. 동일한 유효 런 집합의 50 ps 판독에서도 같은 가족이 선택됐으며, 두 시점 모두 차점과의 차가 0.20 eV/B₂O₃ 이상이었다. 이는 두 시점의 선택 일치이며, 어닐 시간 수렴·독립 재현·전역 최저 상태를 뜻하지 않는다.
하향 판정은 이유를 나누세요.

* 유효한 판독끼리 다른 승자: “50 ps와 100 ps에서 선택된 초기 가족이 달라, 이번 탐색에서는 시간에 일관된 승자를 보고하지 않는다.”
* 50 ps에서 차이 부족: “100 ps에서는 승자 문턱을 만족했으나, 50 ps에서는 여유가 부족해 두 시점 일치 조건을 충족하지 못했다.”
* 자료·게이트 문제: “시간 비교의 유효성 조건이 충족되지 않아 최종 승자 서술을 보류한다.”

마지막 둘을 “순서가 바뀌었다”고 쓰면 안 됩니다.
Q6. 새 진단 도구에서 무엇을 확인해야 하나?
가장 중요한 점은 `anneal_judge`는 검증기 전체가 아니라 검증된 기록을 받는 판정 함수라는 것입니다.
[함수:571 (line 571)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/tools/doping/b2o3_bo_readout.py:571)에 정체성·파일 해시가 없는 합성 기록을 직접 넣어도 승자가 나옵니다. 이는 함수의 명시된 전제에 맞는 동작입니다. 기존 경로는 [anneal_readout:646 (line 646)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/tools/doping/b2o3_bo_readout.py:646)이 앞에서 결속을 검사합니다. 새 도구가 그 전제를 충족해야 합니다.
최소 확인 항목은 다음입니다.

* 54개 계획 항목과 부모 런을 이름·바탕·초기 가족으로 결속: 정렬한 두 목록을 위치로 짝짓지 않습니다. 누락·중복·계획 밖 기록을 거부합니다.
* 부모 런 검증: 8단계 목적·입력·설정·정체성·궤적 SHA를 확인하고, `md_traj`는 필수로 요구합니다.
* 시간→프레임 변환: 검증된 기록의 `dt_fs × log_every_steps`로 계산합니다. 현재 설정에서는 50번이 맞지만, 저장 간격이 250걸음이면 50 ps는 100번입니다. 기존 [_frame_index:419 (line 419)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/source/tools/doping/b2o3_bo_readout.py:419)를 재사용할 수 있습니다. ASE도 저장 간격을 `loginterval`로 정합니다. [공식 문서](https://ase.gitlab.io/ase/ase/md.html#file-output)
* 프레임→이완 입력 결속: 원소 순서·좌표·셀·PBC가 실제 선택 프레임과 같아야 합니다. 추출 파일의 SHA만 자체 확인하는 것으로 끝내지 않습니다.
* 이완 입력→E₅₀ 결속: 새 출력 폴더, 이완 전용 목적, `time_ps=0`, 같은 모델·셀 이완·힘 기준·걸음 상한을 검사합니다. 유한한 `E_post_relax`를 사용하며, `E_md_final`이나 원자당 에너지와 섞지 않습니다.
* 실패 처리: 100 ps 끝 이완 실패와 부모 MD 궤적 부재를 구분합니다. 가능한 50 ps 결과를 조용히 버리지 말고 시점별 성공·실패를 기록합니다. 최종 시간 비교는 앞서 정한 집합 조건을 따릅니다.

음성시험에는 다른 런의 프레임, 49 ps 프레임, 저장 간격 변경, 스냅숏 교체, 미수렴·비유한 E₅₀, 한 시점만 실패한 경우를 포함하세요. 검증된 100 ps 기록과 50 ps 기록을 끝까지 연결하는 정상 경로도 있어야 합니다.
카드에 넣을 최소 개정안
본 판독은 기존 100 ps 판독으로 보존한다. 50 ps 진단은 본 판독을 승격하지 않는다. 시간 비교에는 원래 계획을 유지하며, 가족별 성공 런 이름 집합이 두 시점에서 같고 기존 게이트를 통과한 경우만 두 시점 일치를 판정한다. 집합이 다르면 시간 비교 보류로 기록한다.
두 시점 모두 같은 초기 가족이 0.20 eV/B₂O₃ 이상의 여유로 선택된 경우에만 “두 시점에서 같은 가족이 선택됐다”고 쓴다. 다른 승자·여유 부족·판독 보류는 서로 다른 사유로 기록한다. 전체 가족 순서나 동일 구조적 골짜기의 유지를 뜻하지 않는다.
런별 에너지 변화, 시점별 성공·실패, 가족별 변화의 중앙값·IQR·최솟값·최댓값, 두 시점의 최저 런 ID·끝 꼴·가족 간 차를 보존한다. 없는 값은 결측으로 남긴다.
개정 규칙과 진단 도구·음성시험은 50 ps 및 100 ps 본 결과 공개 전에 고정한다. 어닐 길이는 운영 규칙이며, 두 시점 일치는 시간 수렴이나 독립 재현의 증거로 쓰지 않는다.
해제조건은 세 가지입니다: ① 판정 사유 분리, ② 성공 집합 불일치 처리 고정, ③ 결과 공개 전 진단 도구의 결속·정상/음성 경로 검증. 추가 200 ps나 속도 시드 계산은 이번 해제조건에 넣지 않습니다.
재현 자료: [판정·드리프트 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/synthetic_reproductions.json), [성공 집합 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EA_20261110/cohort_reproductions.json).

## 첨부 — 사용자가 같이 붙인 재현 자료 (원문 그대로)

```json
{
  "margin_only": {
    "50": {
      "winner": null,
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "UMA 로는 못 가른다 (승자–차저 0.100 < 0.2)",
      "winner_runner_up_gap_eV": 0.1,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "100": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 0.400 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.4,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "amend3_text_branch": "order_changed_claim"
  },
  "unavailable_50": {
    "50": {
      "winner": null,
      "order": null,
      "decision": "승자 보류",
      "winner_runner_up_gap_eV": null,
      "hold_reasons": [
        "F_P: G1 실패 (성공 14 < 15 · 탈락)"
      ],
      "pairs": null
    },
    "100": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 0.400 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.4,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "amend3_text_branch": "order_changed_claim"
  },
  "runner_up_changed": {
    "50": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 1.000 ≥ 0.2)",
      "winner_runner_up_gap_eV": 1.0,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "100": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_free",
        "F_P"
      ],
      "decision": "승자 F_B (차저 F_free 와 0.500 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.5,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "amend3_text_branch": "same_order_claim"
  },
  "outlier_minimum": {
    "50": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 1.000 ≥ 0.2)",
      "winner_runner_up_gap_eV": 1.0,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 1,
        "같은_방향": false
      }
    },
    "100": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 1.000 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.9999999999999999,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 1,
        "같은_방향": false
      }
    },
    "median50": {
      "F_B": 0.2,
      "F_P": 0.0,
      "F_free": 1.0
    },
    "amend3_text_branch": "same_order_claim"
  },
  "same_drift_summaries": {
    "50": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 0.300 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.3,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "100": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 2.730 ≥ 0.2)",
      "winner_runner_up_gap_eV": 2.73,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 18,
        "같은_방향": true
      }
    },
    "delta_stats": {
      "F_B": {
        "median": -0.4,
        "IQR": 5.551115123125783e-17,
        "max": -0.39999999999999997,
        "min": -3.0
      },
      "F_P": {
        "median": -0.4,
        "IQR": 0.0,
        "max": -0.4,
        "min": -0.4
      },
      "F_free": {
        "median": -0.4,
        "IQR": 0.0,
        "max": -0.4,
        "min": -0.4
      }
    },
    "argmin50": {
      "F_B": 0,
      "F_P": 0,
      "F_free": 0
    },
    "argmin100": {
      "F_B": 17,
      "F_P": 0,
      "F_free": 0
    }
  },
  "common_per_base_drift_not_common_minimum_drift": {
    "50": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 0.300 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.3,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 17,
        "같은_방향": true
      }
    },
    "100": {
      "winner": "F_P",
      "order": [
        "F_P",
        "F_B",
        "F_free"
      ],
      "decision": "승자 F_P (차저 F_B 와 0.500 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.5,
      "hold_reasons": null,
      "pairs": {
        "n": 18,
        "same_sign_as_order": 1,
        "같은_방향": false
      }
    },
    "paired_differences_unchanged": true
  },
  "direct_judge_without_identity": {
    "winner": "F_B",
    "order": [
      "F_B",
      "F_P",
      "F_free"
    ],
    "decision": "승자 F_B (차저 F_P 와 1.000 ≥ 0.2)",
    "winner_runner_up_gap_eV": 1.0,
    "hold_reasons": null,
    "pairs": {
      "n": 18,
      "same_sign_as_order": 18,
      "같은_방향": true
    }
  },
  "frame_mapping": {
    "2fs_500steps": 50,
    "2fs_250steps": 100,
    "truncated_rejected": "⛔ 50 ps 프레임 50 가 궤적에 없다 (프레임 50 개) — 연속 궤적이 짧다"
  }
}
```

```json
{
  "false_time_reversal": {
    "50": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 1.300 ≥ 0.2)",
      "winner_runner_up_gap_eV": 1.3,
      "hold_reasons": null,
      "pairs": {
        "n": 17,
        "same_sign_as_order": 17,
        "같은_방향": true
      }
    },
    "100": {
      "winner": "F_P",
      "order": [
        "F_P",
        "F_B",
        "F_free"
      ],
      "decision": "승자 F_P (차저 F_B 와 1.200 ≥ 0.2)",
      "winner_runner_up_gap_eV": 1.2,
      "hold_reasons": null,
      "pairs": {
        "n": 17,
        "same_sign_as_order": 0,
        "같은_방향": false
      }
    },
    "all_underlying_energies_identical": true,
    "amend3_text_branch": "order_changed_claim"
  },
  "false_same_winner_sensitivity": {
    "50": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 1.000 ≥ 0.2)",
      "winner_runner_up_gap_eV": 1.0,
      "hold_reasons": null,
      "pairs": {
        "n": 17,
        "same_sign_as_order": 1,
        "같은_방향": false
      }
    },
    "100": {
      "winner": "F_B",
      "order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "decision": "승자 F_B (차저 F_P 와 1.000 ≥ 0.2)",
      "winner_runner_up_gap_eV": 1.0,
      "hold_reasons": null,
      "pairs": {
        "n": 17,
        "same_sign_as_order": 1,
        "같은_방향": false
      }
    },
    "common_success_both_times": {
      "winner": "F_P",
      "order": [
        "F_P",
        "F_B",
        "F_free"
      ],
      "decision": "승자 F_P (차저 F_B 와 0.500 ≥ 0.2)",
      "winner_runner_up_gap_eV": 0.5,
      "hold_reasons": null,
      "pairs": {
        "n": 16,
        "same_sign_as_order": 16,
        "같은_방향": true
      }
    },
    "all_underlying_energies_identical": true,
    "amend3_text_branch": "same_order_claim"
  }
}
```
