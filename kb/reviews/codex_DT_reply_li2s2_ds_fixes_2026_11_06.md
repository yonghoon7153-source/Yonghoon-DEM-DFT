---
title: "DT 회신 — li2s-2 DS 고침 + DT 전 리뷰 3 차 확인 (63331be6): 조건부 GO · 새 P0 · P1 없음 · P2 1 (시계 차이가 늘 보수적 보류로만 실패한다는 설명이 틀림 — 같은 신뢰 시계 범위로 명문화하고 그 안에서 실행 · 판정 · 재개)"
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, reply, letter]
letter: DT
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

> 프롬프트: `codex_DT_prompt_li2s2_ds_fixes_2026_11_06.md` (기준 커밋 `63331be6`) · 트랙 li2s-2 (논문 1저자 = 외부 · 위임 10-30). 아래는 원문이다.
> `<codex>` = `C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DT_20261106`.

---

조건부 GO — DS의 P1-1·P2-1과 정상 복구 조건은 닫혔습니다. 새 P0·P1은 찾지 못했습니다. 남은 것은 시계 차이를 항상 보수적 보류로 설명한 P2 한 건입니다. 아래 시계 전제를 명문화하고 준수하는 범위에서 1단계 발사를 승인합니다.

63331be6에서 드라이버 254/254, Windows 러너 153/153 통과를 재현했습니다. 소스 지문과 카드 값 지문 086de59c484f9c32도 일치합니다.

DS 수정 확인

| 실제 재현 | 결과 |
|---|---|
| 완료130에서 plan·md_done을 옮겨 판정 → 복구·thermo 변경 | 추가 실행 0, invalid |
| 같은 경우, thermo 변경 없이 원본만 복구 | 추가 실행 0, invalid |
| 실제 71/130 진행 중 판정 → 정상 완료·일시 오류 복구 | 추가 실행 7, stage1_pass |
| MD 완료·FIRE 대기 중 판정, MD 출력 불변 | 정상 복구 |
| 같은 경우, 완료 뒤 thermo 변경 | 추가 실행 0, invalid |
| 직접 판정의 정본·이력 경로 이상 | written=False, 읽기·변경 없음 |
| 첫 시드 녹음 fail인데 판정을 못 씀 | 장부 닫힘 유지 → ACK 뒤 0실행·터미널 melt |

직접 판정은 이제 외부 링크의 판정을 이력으로 가져오거나 링크를 정상 파일로 바꾸지 않습니다. 실제 디렉터리와 모의 링크 분기로 확인했습니다.

P2-1 — 시계 차이가 반드시 보류로만 실패하지는 않습니다.

위치: [카드:531 (line 531)](<codex>/source/db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json:531), [시각 비교:2266 (line 2266)](<codex>/source/tools/ionic/melt_quench_uma.py:2266).

완료 기록을 쓰는 시계만 1시간 앞서도록 주입했습니다. 완료 기록의 시각·해시는 수동 수정하지 않았습니다.

그 뒤 완료된 산출물을 잠시 보존하고 원래 궤적의 71프레임까지만 보여 판정한 다음, 원본 완료 산출물과 원본 완료 기록을 그대로 복원했습니다. 끝 판정의 일시 오류와 ACK를 거치자 시각 비교가 성립하여 **7실행·`stage1_pass`**가 나왔습니다. 시계 차이가 없는 대조는 0실행·보류였습니다.

따라서 run_id와 해시 일치는 자료의 동일성을 확인하지만, 서로 다른 시계가 기록한 사건 순서까지 보증하지는 않습니다.

다만 완료 뒤 thermo를 변경한 경우에는, 시계가 앞서도 해시 불일치로 0실행·invalid였습니다. 변경된 완료 MD가 무검증으로 통과한 반례로 확대해서 해석하지 않습니다.

최소 수정은 설명 정정과 운영 범위 한정입니다. 다음처럼 명시하면 됩니다.
시각 비교는 동일한 신뢰 가능한 시계 기준에서만 선후관계의 근거로 사용한다. 시계 차이는 방향에 따라 면제를 허용할 수도 있다. 다른 호스트나 시계 변경으로 선후관계가 불확실한 기록은 자동 ACK 복구로 처리하지 않고 사람이 확인한다.

이번 실행·수동 판정·재개를 이 조건 안에서 수행하세요. 현재 코드가 호스트 차이와 시계 변경을 자동 탐지한다는 뜻은 아닙니다.

질문 1–5 답변
1. ‘진행 중 확인’ 경계 — 찬성입니다. DS 반례는 막히고 71/130 정상 복구는 유지됩니다. plan만 있는 단계, 모르는 파일, 판독 오류 등을 보류하는 것은 현재 정책에서 수용할 수 있습니다.
2. 시각 규칙의 신뢰 — 조건부 찬성입니다. 완료 기록의 시각·해시를 의도적으로 고치고 관측까지 꾸미는 것은 선언한 기록 위조 범위로 둘 수 있습니다. 다만 시계 오차는 기록 위조가 아니므로, 위 P2처럼 별도로 다뤄야 합니다.
3. quench_ps 및 유도값 대조 — 확인한 경로에서는 닫혔습니다. 일정·밀도·조성 등 38개 입력 변이를 차단했고, 실제 schedule → build_plan → JSON 왕복 → 판정 108조합에서 유도값 불일치로 인한 거짓 invalid는 없었습니다. 현재 일정·기대 프레임·녹음 창·유지 창에서 추가 미결속 유도값은 찾지 못했습니다.
4. 선언한 한계 — 시계 설명을 제외하면 수용합니다. 진행 중 기존 내용 변경 미탐지는 무결성 한계로 유지하세요. 첫 시드 판정을 못 쓴 경우도 닫힘은 장부에 남아 다음 시작을 막습니다. FIFO의 운영상 멈춤과 보수적인 복구 보류도 설명한 범위와 맞습니다.
5. 새 조용히 틀린 경로 — 위 시계 설명 문제가 남습니다. 새 세 필드는 정상적인 입력 동일성·요약 대조를 불필요하게 깨지 않았습니다. 잘못된 어휘·타입은 invalid로 처리됐습니다. 검토한 범위에서 추가 P0·P1은 없습니다.

닫힘 판정

| 항목 | 판정 |
|---|---|
| DS P1-1 | 닫힘 |
| DS P2-1 | 닫힘 |
| DS 반례 차단 조건 | 닫힘 — 변경·무변경 복구 모두 보류 |
| DS 71/130 정상 복구 조건 | 닫힘 |
| DR 재승인 조건 ① | 닫힘 — 위 신뢰 가능한 시계 범위 |
| DJ Q5 | 이번 검토 범위에서 닫힘 — 명시한 한계 유지 |

검증 기록은 [VERIFICATION.json](<codex>/VERIFICATION.json)에 남겼습니다. 생산 계산은 하지 않았고, 전체 변이 501건·Linux 고유 시험·실제 링크/FIFO는 독립 재실행하지 않았습니다.

```json
{
  "review": "DT",
  "commit": "63331be657de7b0408e6e9c05425e0b10d7cd9d5",
  "base_commit": "6b124717ba9de26e2627c5fa1daeab8c6788243f",
  "verified_at_utc": "2026-11-06T11:47:46.456931+00:00",
  "verdict": "CONDITIONAL GO",
  "sources": {
    "AGENTS.md": {
      "sha256": "ee9dcddc9eae096540fd74d6af20ef84cc684975c64618f0e67f6e3582379448",
      "unchanged": true
    },
    "CLAUDE.md": {
      "sha256": "0ed81f37382e018dc6a9c7ddfd6f375edddeeaec2c86b7b11852ce9c80db33c1",
      "unchanged": true
    },
    "tools/ionic/melt_quench_uma.py": {
      "sha256": "1ca75960fa21f4e84fe0b975c7aaeb462b6f9c315103633fb44877c7b0c60b88",
      "unchanged": true
    },
    "tools/ionic/li2s2_stage1_runner.py": {
      "sha256": "00e08de0f75a7869ac82aa423564e1648b444d76b8310b23061c11767c693b0a",
      "unchanged": true
    },
    "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json": {
      "sha256": "6b6a810e21771420169b2a0cf9955d7e92885f2cded83c9c16d8c275ee98c985",
      "unchanged": true
    },
    "db/governance/decisions.json": {
      "sha256": "af75634a651d874a1a9d861fd2112d1b685d1aa1c173386d71de2b25605841a2",
      "unchanged": true
    },
    "db/raw/li2s2_dt_mutation_2026_11_06/README.md": {
      "sha256": "78a6149310b3edcc312f1f64972d661beef6c24c98782d7e138134446e3599f7",
      "unchanged": true
    },
    "db/raw/li2s2_dt_mutation_2026_11_06/dt_mutate.py": {
      "sha256": "991c2e05bc9000e06803850e6ea909bd9bfa5f2aae49809adeddcd554e9486e0",
      "unchanged": true
    },
    "db/properties/lpscl_li2s_layer1_amendment_2026_09_12.json": {
      "sha256": "251f6057889842a123b484e29dd426950ed32367ae75474b9a7d60fde0d718f7",
      "unchanged": true
    }
  },
  "card_values_sha16": "086de59c484f9c32",
  "selftests": {
    "driver": {
      "passed": 254,
      "failed": 0,
      "log": "driver_selftest.txt"
    },
    "runner": {
      "passed": 153,
      "failed": 0,
      "log": "runner_selftest.txt"
    }
  },
  "platform": "Windows; runner 6 POSIX-only and 1 native-symlink-permission test skipped; driver internal symlink/FIFO subcases skipped.",
  "method": "Immutable source snapshot; actual file parser, verdict, recovery, ledger and summary with FakeQuench children; deterministic file/IO/clock injections. Link branch probes modeled because native symlink creation is denied.",
  "production_simulations_executed": false,
  "native_posix_signal_tests_executed": false,
  "native_symlink_or_fifo_tests_executed": false,
  "full_501_mutation_suite_rerun": false,
  "findings": [
    {
      "id": "DT-P2-1",
      "severity": "P2",
      "file": "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json",
      "lines": [
        523,
        531
      ],
      "code": "tools/ionic/melt_quench_uma.py:_utc_before/pre_anchor_exempt",
      "description": "Clock skew does not always cause conservative holding. A completed run viewed as a restored 71-frame prefix can satisfy judged_at < completion_at when the completion clock is ahead, without editing the completion record.",
      "reproduction": "Actual completion writer clock injected +3600 seconds; preserve completed artifacts, inspect original prefix, restore original completed MD and completion record; one final I/O error then ACK produces 7 launches and stage1_pass. Equal-clock control holds with 0 launches. Changing thermo after completion still holds via hash mismatch.",
      "interpretation": "Chronology/support-boundary wording defect, not demonstrated acceptance of modified completed MD or falsified science. No new P0/P1 found in tested scope.",
      "minimum_change": "Correct conservative-skew claim and explicitly constrain automatic in-progress exemption to one trusted common clock domain; uncertain cross-host clock/clock-step cases require manual hold rather than automatic acknowledgment recovery.",
      "evidence": "dt_progress_time/results.json"
    }
  ],
  "conditions_for_stage1_go": [
    "Adopt corrected clock support-boundary wording before launch.",
    "Run and judge recovery within the same trusted clock domain; do not automatically recover ambiguous chronology across unsynchronized hosts or clock changes."
  ],
  "closures": {
    "DS_P1_1": "closed",
    "DS_P2_1": "closed in actual directory and modeled link paths; native Linux link replay not independently performed",
    "DS_release_counterexample": "closed, changed and unchanged restoration both held",
    "DS_release_71_of_130": "closed, 7 fixture launches and stage1_pass",
    "DR_release_1": "closed within declared trusted-clock scope",
    "DJ_Q5": "closed within reviewed and declared limits; no claim of universal defect absence"
  },
  "root_clock_checks": {
    "completion_record_matches_current_md_hashes": true,
    "no_manual_at_utc_edit_in_clock_probe": true,
    "changed_thermo_remains_blocked": true
  },
  "evidence_sha256": {
    "dt_progress_time/results.json": "2697863ed6c1592bac159d38ce5fd2b3bd14851d23c0c718df813a76d9fea987",
    "dt_progress_time/clock_probe.py": "8b8b3c139880d0400e519834353eacadde69dbb1851b6ef365de83e36caf55de",
    "dt_progress_time/replay.py": "f213b2662044284e12e9cadaa99dfd353378b26e45fd722f681837b74b33e039",
    "dt_schedule_inputs/results.json": "daf44f0d0111b2ada360b9c164413fba071ec7397f9fdf5328368c1e61ffc24d",
    "dt_schedule_inputs/probe.py": "159626f3d93a02763d00a4ae120697e290a80733c5a6e2f6bdb8186edc4bb79f",
    "dt_paths_written/results.json": "0689d816ec0636bab850eacaf3d347d20c0d018d3fef2331ad77e157fb16ca44",
    "dt_paths_written/direct_replay_results.json": "a10678b4b1b9f70b7b5d225a6c97c25bc256a7a8a09cb5dad3618d1012a767b7",
    "dt_paths_written/probe.py": "6d29e95be906e5dc2105be81136e9dd49f98e5dc8a62dd5b2b39a3fb142d955b",
    "dt_paths_written/direct_replay.py": "8970f399c5a0f4f4f755e2c021ef1c972f30cd956f8bb583098c06878d64ef1e"
  }
}
```
