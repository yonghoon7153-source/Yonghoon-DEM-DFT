---
title: Lean Review Backlog (실행 보류 중인 중복 정리)
description: "Duplication candidates found by the lean ladder, deferred because refactoring changes source_digest during an open gate-review round"
created: 2026-08-11
updated: 2026-08-20
type: query
tags: [design, tooling, gate-review]
sources: [raw/repositories/2026-08-11-agent-harness-repos.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-opus-5
effort: medium
claimType: prescriptive
evidenceScope: single-source
---

# Lean Review Backlog

`/lean-review` ([[agent-harness-patterns]]) 를 처음 돌려 나온 실제 후보와, **왜
지금 실행하지 않는지**. ponytail 의 `/ponytail-debt`(미룬 것을 원장으로 모아
영구 부채가 되지 않게)에 해당하는 자리다.

## 왜 보류인가

리팩터링은 `src/` 를 건드리므로 `source_digest` 가 바뀐다. 리뷰 중에 identity 를
바꾸면 "리뷰받은 코드"와 "실행한 코드"가 갈리고, 이미 생산된 artifact 는
fail-closed 로 무효화된다 ([[provenance-fail-closed-verification]] 원칙 1).
→ **리뷰 라운드가 닫힌 직후, 다음 실행 전**이 적기다.

- **[2026-08-11]** 13차 리뷰가 `c9970ebc` 대상으로 열려 있어 보류.
- **[2026-08-20]** 그 라운드는 닫혔고 본 실행도 끝났다. **그런데 보류는 유지된다** —
  이제는 다른 이유다: 모델 오차 민감도 스윕이 진행 중이라 그 다리들이 **같은
  `source_digest` 위에서 비교돼야** 한다. 스윕이 끝나 다리 집합이 닫히는 시점이
  다음 적기다. 이 항목이 영구 부채가 되지 않게, 그때 다시 이 페이지를 연다.

## 후보 1 — env 결정축 비교가 3곳에 중복 (사다리 2: 이미 있나)

- `src/baseline.py:172-173` (완방 캐시 hit 판정)
- `src/halfcell.py:282-283` (half-cell 캐시 hit 판정)
- `src/halfcell.py:386-387` (`validate_halfcell_cache` 의 `runtime_identity`)

세 곳 모두 같은 일을 한다: `env_fingerprint()` 를 결정축(`_ENV_KEYS`)으로 좁혀
저장본과 비교하고, 다른 키 목록을 만든다. 게다가 `_ENV_KEYS` 는 물리 모듈인
`baseline.py` 에 살면서 `halfcell.py` 가 import 해 쓴다 — 레이어링도 어긋난다.

제안: `src/io.py` 에 `env_fingerprint()` 와 나란히
`env_decision_axes(env) -> dict` + `env_diff(old, new) -> list[str]` 를 두고 세
호출부가 그것을 쓴다. `_ENV_KEYS` 도 `io.py` 로 이동 (fingerprint 를 만드는 곳이
어떤 축이 결정적인지도 소유해야 한다).

- 예상: 각 호출부 2~4줄 → 1~2줄, `_ENV_KEYS` cross-import 제거
- **행동 변화 없음**이어야 한다 → 리팩터링 후 `pytest tests/ -q` 전량 통과 +
  `test_discharged_cache_rejects_foreign_runtime` ·
  `test_halfcell_cache_binds_runtime` 이 그대로 잡는지 확인
- carve-out 저촉: **없음** (검사 자체를 줄이는 게 아니라 같은 검사를 한 곳에서
  정의). 단 검증 코드에 닿으므로 리뷰 라운드 밖에서 한다.

## 다음 라운드에 다시 볼 것

- validator 의 `checks[...] = (bool, 사유문자열)` 보일러플레이트 — 헬퍼로 줄일
  여지가 있으나, 사유 문구가 각각 발견 번호와 실측을 담고 있어 **가치 있는
  중복**일 수 있다. 줄이기 전에 원장 대조 필요.
- `scripts/smoke_e2e.sh` 의 python heredoc 반복 — 단계마다 검사 내용이 달라
  공통화하면 오히려 읽기 어려워질 수 있다. 판단 보류.

## 관련
- [[agent-harness-patterns]] · [[provenance-fail-closed-verification]] · [[gate-review-loop]]
