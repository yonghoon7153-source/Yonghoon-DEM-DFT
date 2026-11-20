# A5R-01 받은 판정문 두 개 (원바이트 · 11-20 반입 ⑰ 때 보존)

Codex 반박 창이 낸 독립 판정문을 고치지 않고 그대로 둔다. 원장 `A5R-01` 의 `opened_in` · `verified_in` 이 이 두 파일을 가리킨다.

| 파일 | 무엇 | 받은 곳 | sha256 |
|---|---|---|---|
| `FINAL_REVIEW_P1_A5_PRESEAL_a230b908546f_20261120.md` | A5 봉인 직전 독립 검토 (리뷰 핀 `a230b908546f`) · HOLD · 새 지적 A5R-01 (P2) | `codex_p1_a5r01_recheck_9fd6aa9d3bee_20261120.zip` 의 `prior_review/` (ZIP sha256 `4152065b…`) | `6fc8a0f6d721440f40ba61a88d8fd8770099d10a3fe2425dd98ba40254a74f54` |
| `FINAL_REVIEW_A5R01_9fd6aa9d3bee_20261120.md` | A5R-01 독립 재확인 (수정 핀 `9fd6aa9d3bee`) · 한정 종결 가능 (CLOSABLE_LIMITED) · 새 지적 0 | `codex_a5r01_closure_claude_00c622f4bbf7_20261120.zip` 의 `decision/` (ZIP sha256 `ec0666ce…`) | `4cb3f9043219e9bb44b4b3a5edb0465c719932cff4fde806e99520798ba0e3dc` |

- 두 sha256 = Codex 공유 기록 제안 (`docs/reviews/p1_rt_a5r01_20261120/ledger_proposal.json` · `docs/reviews/p1_rt_a5r01_closure_20261120/ledger_proposal.json`) 의 `review_report_sha256` 과 같다.
- 범위: 이 지적 때문에 두었던 A5 봉인 후보 보류의 해제 근거까지다. 운영 봉인 · 새 RJ 발사 · 현장 자격 · 물리 판정 GO 가 아니다.
- 원장은 `claimed_fixed` 로 둔다. 고친 쪽과 재확인한 쪽이 둘 다 Codex 라서, 원장의 독립 검증자 조건 (`verified_by` ≠ `owner`) 을 지어 넣지 않는다 (`LPI-01` · `RTR-01` 과 같은 규약).
