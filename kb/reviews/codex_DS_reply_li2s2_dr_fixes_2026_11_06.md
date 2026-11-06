---
title: "DS 회신 — li2s-2 DR 고침 + DS 전 리뷰 3 차 확인 (6b124717): NO-GO · P1 1 (완료 여부 미확인을 md_complete_seen=False 로 기록해 완료 뒤 입력 변경을 '진행 중' 으로 면제) · P2 1 (판독기가 거부하는 판정 링크를 직접 수동 판정은 읽고 정상 파일로 바꿈)"
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, reply, letter]
letter: DS
date: 2026-11-06
track: li2s
channel: codex
kind: reply
status: 수령 2026-11-06 (사용자 붙여넣기 · 원문 보존 · 마크다운 링크의 Codex 로컬 경로 머리만 `<codex>` 로 줄임 · 탭으로 붙은 표는 표 꼴로)
confidence: medium
verificationStatus: verified
verifiedAt: 2026-11-06
verifiedBy: self
explored: false
authoredBy: external
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트: `codex_DS_prompt_li2s2_dr_fixes_2026_11_06.md` (기준 커밋 `6b124717`) · 트랙 li2s-2 (논문 1저자 = 외부 · 위임 10-30). 아래는 원문이다.
> `<codex>` = `C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DS_20261106`.

---

NO-GO — P1 1건이 남았습니다. 추가 P2 1건도 있습니다. DR의 기존 두 반례는 막혔지만, 완료 여부를 확인하지 못한 상태를 ‘진행 중’으로 면제하는 경로가 남아 있습니다.

대상은 6b124717입니다. 드라이버 252/252, Windows 러너 150/150 통과를 재현했고, 카드 값 지문 086de59c484f9c32도 일치했습니다. 생산 계산은 실행하지 않았습니다.

P1-1 — 완료 여부 미확인을 False로 기록해, 완료 후 입력 변경을 면제합니다.

위치: [stage1_verdict:1194 (line 1194)](<codex>/source/tools/ionic/melt_quench_uma.py:1194), [md_complete_seen:2213 (line 2213)](<codex>/source/tools/ionic/melt_quench_uma.py:2213), [pre_anchor_exempt:2236 (line 2236)](<codex>/source/tools/ionic/melt_quench_uma.py:2236).

plan.json이 없거나 깨져 있으면 일정·프레임 검사를 수행하지 않습니다. 이때 md_done.json까지 없으면, 완료 여부가 불명인데도 md_complete_seen=False가 됩니다. pre_anchor_exempt는 이를 실제 진행 중이라는 근거로 사용합니다.

실제 판정기·러너로 다음을 재현했습니다.
1. traj.xyz 130프레임, thermo 마지막 시각 129 ps, final.xyz·`result.json`까지 있는 상태를 만듭니다.
2. plan.json과 md_done.json을 잠시 보관 위치로 옮기고 수동 판정합니다.
3. 판정은 incomplete, md_complete_seen=False를 기록합니다. final/result의 존재는 지문에 남아 있습니다.
4. 두 파일을 복구하고 thermo 값을 변경한 뒤, 러너 끝 판정에 일회성 I/O 오류를 주입합니다.
5. 일반 STOP 확인으로 재개하면 앞선 기록이 면제되어 추가 7실행 → stage1_pass → 2단계 시드 선정으로 이어집니다.
장부나 판정 이력을 고쳐서 만든 결과가 아닙니다. 다만 정상 producer의 쓰기 순서에서 자연스럽게 생기는 경주도 아닙니다. 완료 기록과 plan의 이동·손실·복구가 필요한 반례입니다. 이번 검토 범위인 입력 복구 경로에 해당합니다.

최소 수정: ‘완료’, ‘진행 중 확인’, ‘확인 불가’를 구분하세요. plan을 못 읽어 검사를 생략한 경우에는 진행 중 면제를 주면 안 됩니다. final/result 같은 후속 산출물의 존재도 plan 판독과 독립적으로 면제 배제에 사용해야 합니다. 완료를 확정하지 못하더라도, 진행 중으로 승인할 필요는 없습니다.

메모리에서 좁은 방어를 적용한 대조 결과는 다음과 같습니다.

| 경우 | 추가 실행 | 결과 |
|---|---|---|
| 현재 코드의 위 반례 | 7 | stage1_pass |
| 확인 불가·완료 산출물을 면제하지 않는 방어 | 0 | invalid |
| 같은 방어 아래 실제 71/130 진행 중 정상 복구 | 7 | stage1_pass |

[재현 기록](<codex>/ds_preanchor/boundary_results.json)

P2-1 — 판독기가 거부하는 판정 링크를 직접 수동 판정은 읽고 정상 파일로 바꿀 수 있습니다.

위치: [stage1_verdict:1274 (line 1274)](<codex>/source/tools/ionic/melt_quench_uma.py:1274), [교체:1292 (line 1292)](<codex>/source/tools/ionic/melt_quench_uma.py:1292).

러너 시작 점검과 _verdict_records는 canonical 판정 링크를 거부하지만, 직접 --stage1_verdict는 vf.is_file()로 들어가 링크 대상의 판정을 읽습니다. 이후 외부 판정을 이력에 넣고, 링크 자체를 새 일반 파일로 교체할 수 있습니다.

최소 수정: stage1_verdict 진입 시 canonical 판정·이력 경로에도 동일한 path_kind 검사를 적용하고, 비정상 경로라면 읽기·이력 추가·교체 전에 거부하세요.

이 항목은 코드 확인과 경로·읽기 분기 모의시험으로 확인했습니다. 실제 심볼릭 링크 생성은 Windows 권한 부족으로 시험하지 못했습니다. 외부 판정은 이력에 남으므로 ‘증거 삭제’라고 판정한 것은 아닙니다. 문제는 판독 경로와 쓰기 경로의 보류 규칙이 다르다는 것입니다.

질문 1–5 답변
1. 실제 진행 중 경계 — 아직 너무 넓습니다. 위 P1이 남습니다. 반면 MD 완료 후 입력이 같고 FIRE 산출물만 추가되는 복구를 허용한 두 번째 갈래는 타당하며, 정상 복구도 재현했습니다.
2. 경로 상태 구분 — 현재 목적에 충분합니다. 부재·일반 파일·파일 링크·그 밖의 구분으로 DR P1-2를 막았습니다. 상태 종류를 더 늘리기보다 P2의 수동 쓰기 경로까지 같은 규칙을 적용해야 합니다.
3. 이중 방어 — 각각 독립적으로 작동합니다. 불일치 분류만 제거하면 경로 지문이 막고, 경로 지문만 None으로 바꾸면 불일치 분류가 막았습니다. 둘 다 제거했을 때만 7실행·통과가 재현됐습니다. 결과만 초록인 헛시험으로 보지 않습니다.
4. 선언한 한계 — 대체로 수용 가능합니다.
   - 진행 중 기존 내용 변경 미탐지는 무결성 보장의 한계로 남겨야 합니다. ‘이미 본 자료의 변경까지 탐지한다’고 주장할 수는 없습니다. 이번 P1의 완료 후 복구까지 그 한계에 포함하면 안 됩니다.
   - 진행 중 예외, 마지막 저장 간격, final/result 기록 도중 관측, 구판 기록의 보수적 보류는 수용합니다.
   - FIFO에서 멈추는 것은 운영상 한계입니다. 자동으로 안전하게 거부한다는 보장과 구분해야 합니다.
   - rc=0 뒤 incomplete여도 계속 실행하는 정책은 비용상한 안에서 수용 가능합니다. 시험에서는 전 잡 실행 후 pending·2단계 없음, 낮춘 상한에서는 상한 STOP을 확인했습니다.
5. 새 조용히 틀린 경로 — P1이 해당합니다. ‘검사하지 못함’이 ‘완료 아님’으로 바뀌면서 입력 변경 증거가 면제됩니다. 추가로 P2의 경로 처리 불일치가 있습니다. 검토 범위에서 새 P0는 찾지 못했습니다.

닫힘 판정

| 항목 | 판정 |
|---|---|
| DR P1-1 | 기존 반례는 닫힘. 일반 경계는 이번 P1 때문에 미해제 |
| DR P1-2 | 닫힘 — 비정상 raw 복구는 0실행·invalid, 실제 부재 복구는 정상 통과 |
| DR P2-1 | 닫힘 |
| DR 재승인 조건 ① | 미해제 — 확인 불가 상태의 진행 중 면제 제거 필요 |
| DR 재승인 조건 ② | 닫힘 |
| Q5 문구 | 닫힘 — 장부 pass/fail 우선과 나머지 이력 규칙이 구분됨 |
| DJ Q5 | 미해제 — 이번 P1의 자동 복구 우회가 남음 |

재승인에는 P1의 확인 불가 상태 처리, P2의 직접 판정 경로 검사를 고치고, 위 반례 차단과 71/130 정상 복구를 함께 확인하면 됩니다. 새 생산 계산이나 문턱 변경은 필요하지 않습니다.

검증 범위와 지문은 [VERIFICATION.json](<codex>/VERIFICATION.json)에 남겼습니다. 전체 변이 472건과 Linux 고유 신호·FIFO 시험은 독립 재실행하지 않았습니다.
