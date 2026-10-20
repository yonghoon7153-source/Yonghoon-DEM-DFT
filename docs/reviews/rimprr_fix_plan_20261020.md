# Rint 조인 재확인 (10-20) — RIMPRR-01 · RIMPR-03 · 04 · SELF-124 수정 계획 (2026-10-20 · 결과 0 건 · 초안 · ⬜ 1저자 비준)

> 근거 = Codex 재확인 `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (검토 핀 `2b9efa253` · 대조 핀 `dcb97f1ed`) · 증거 `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/` (우리 트리 재현 = 판정값 차이 0 · `_README_import.md`).
> 판정 요지: `RIMPR-01` · `02` · Q7 범위 한정 닫힘 (verified) · 새 P1 · P2 없음 · 새 P3 `RIMPRR-01` (원장 `RIMPR-R01` — 원장 ID 규칙 접두 5 글자) · `RIMPR-04` 범위 보강 · `RIMPR-03` = ASCII 범위 명시면 연기 가능 · **①′ 정량 채택 · 생산 HOLD 유지**.
> 범위: 진단 관문 `scripts/rint_iface_join.py` (봉인 32 밖 — 두 Rint 커밋 ∩ `CODE_FILES` = 0 · 10-20 git 확인) · 시험 `scripts/test_rint_g2_join.py` · 문서.  생산 σ 경로 · iface 끔 경로 · 봉인 32 무변경.  **이 문서는 계획만 — 코드는 고치지 않았다.**

## 1. 결함과 최소 해결 (판정문 §3 · §4 · §1 · §7 그대로)

| ID | 결함 | 자리 (핀 `2b9efa253`) | 최소 해결 (판정문) |
|---|---|---|---|
| `RIMPR-R01` (= Codex `RIMPRR-01`) P3 | 구역 분류 `startswith()` + 헤더 표지 전역 `replace()` → `ITEM: ATOMSid …` · `ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS` (및 경계 없음 · 반복 · 후첨 10 건) 이 조인 PASS · 정량 ACCEPT · 소비 배열은 정상과 같음 · 대조 핀에도 있음 | `scripts/rint_iface_join.py:278–279 · 298 · 302` (step / count 의 명시 헤더 검사 `:286–288` 가 이 셋에는 없다) | 구역 이름 = 정확한 단어 경계 · 표지 하나만 앞에서 제거 · 나머지 토큰은 기존 열 · 상자 검사로 · 정상 공백 · 탭 · 쓰지 않는 진단 열은 일괄 금지하지 않음 · 두 사례 + contact 대응 상주 회귀 |
| `RIMPR-04` P3 (범위 보강) | 입력 유한 ≠ 계산 결과 유한 — 비-AM 두 구 x 1e160 → 거리 · 허용폭 norm inf → `inf > inf` 거짓 → 조인 PASS / 정량 ACCEPT (1e150 대조 = REJECT) · 한-AM 1e160 → `delta_bound_um` inf (후단 ledger 가 거부) · `sim_to_um` 1e160 → AM–AM 면적 inf | `scripts/rint_iface_join.py:641–645` · `:767` · `:799` | 연기 가능 (조건 넷 — 원장 note) · 정량 채택 전 결과 유한성 · 수치적으로 안정한 거리 · 오차폭 검토 · 범위 제한이면 명시적 입력 계약 |
| `RIMPR-03` P3 | 정수 정규식 `\d` 가 전각 · 아라비아-인도 숫자를 받는다 (수치 · ID 대응은 ASCII 와 같음) · ASCII 0 앞자리 정규화라 긴 유니코드 0 덧붙임은 거부될 수 있음 | `scripts/rint_iface_join.py:79` (`_INT_RE`) | ASCII 생산 덤프 범위 명시 + open 유지면 연기 가능 |
| `SELF-124` P3 | 요청서가 *"봉인 32 파일 무변경"* 을 범위 한정 없이 · 시험 수를 *"78/135 → 138/138"* (다른 두 시험 판) 로 적음 | `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` 12 · 19 행 · 원장 RIMPR-01 · 02 evidence_tests 첫 줄 · 커밋 `3b9d51789` 메시지 (고칠 수 없음 = 기록만) | §7 권장 문장 · 현재 시험 138 을 옛 코드에 = 81/138 구분 |

## 2. 1저자가 정할 것

| Q | 결정 | 선택지 | 권고 |
|---|---|---|---|
| Q1 | `RIMPR-R01` 고침 방식 | (가) 머리 줄을 `ITEM:` 뒤 낱말로 토큰화해 구역 이름 (`TIMESTEP` · `NUMBER OF …` · `BOX BOUNDS` · `ATOMS` · `ENTRIES`) 을 **정확한 단어 경계**로 대조 → 표지 하나만 앞에서 제거 (슬라이스 · `removeprefix`) → 나머지 토큰은 기존 열 · 상자 플래그 검사에 그대로 (공백 · 탭 구분 · 쓰지 않는 진단 열 허용 그대로) — 예상 (시험 전): 경계 없음 · 붙여 쓴 반복 표지 (`ATOMSITEM:` · `BOUNDSITEM:` 꼴) = 모르는 절 (`frame_layout`) · 상자 표지 후첨 = 플래그 셋 아님 (`box_format`) · 행 표지 후첨 = 머리 열 수 ≠ 행 폭 (`row_width`) (나) 머리 줄 전체를 정규식 하나로 고정 — 열 이름 · 플래그 문법까지 새로 정의 | **(가)** — 판정문 최소 해결 그대로 · 바뀌는 곳 = 분류 · 표지 제거 두 자리뿐이고 열 · 상자 규칙은 그대로라 정상 `%g` 덤프 (real14 · case15 · gzip · CRLF · D19) 에 새 거짓 거부를 만들 길이 좁다 |
| Q2 | 시험 먼저 범위 | (가) 최소 반례 둘 (판정문 §3 문자열 그대로) + contact `ENTRIES` 대응 (경계 없음 · 반복 표지 · 행 표지 후첨) + 원자 쪽 반복 · 후첨 + 상자 경계 없음 · 반복 (Codex 독립 탐침 10 건 전부) + 정상 양성 그대로 (real14 · case15 · 접촉 0 행 · gzip · CRLF · 기존 빈 줄 규약 · D19 · 쓰지 않는 진단 열 · 공백 · 탭) → 고치기 전 판에서 새 반례 실패 확인 뒤 수정 (나) 최소 둘 + contact 대응만 | **(가)** — 판정문 요구 (두 사례 + contact 대응) 의 상위 집합 · 10 건은 이미 Codex 증거 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/evidence/structure_results.json`) 에 입력 · 기대가 있어 옮기기만 하면 된다 |
| Q3 | `RIMPR-04` 지금 범위 | (가) 파생값 유한성 fail-closed — `:641–645` 의 거리 · 허용폭 (와 같은 부류 `:767` 반올림 폭 · `:799` 면적) 이 유한이 아니면 구조화 거부 (새 사유 코드 · 결과 0 건) + 1e160 반례 · 1e150 대조 상주 · 안정한 `hypot` 재작성 · 결과 유한성 전반 검토는 정량 채택 전 (나) 그대로 연기 (조건 넷 원장 기록 — 이미 적음) | **(가)** — 한 줄 꼴 fail-closed 로 알려진 false-PASS 를 막는 비용이 작고 조건 ③ (조인을 소비자 관문처럼 믿지 않음) 을 코드로 받친다 · 안정한 계산은 조건 ④ 대로 정량 채택 전 · 원장은 open 유지 (조건 ①) |
| Q4 | `RIMPR-03` | (가) 지금 — `_INT_RE` 의 `\d` → `[0-9]` (전각 · 아라비아-인도 숫자 = `int_token` 거부 · 반례 상주) (나) 연기 — *"ASCII 생산 덤프 지원"* 범위 명시 · open 유지 | **(가) 지금** — 한 글자 변경 · Q1 과 같은 파일 · 같은 시험 묶음 · 생산 덤프 (ASCII `%g`) 무영향 · 유니코드 0 덧붙임 문제도 같이 사라진다 |
| Q5 | 문서 정정 (`SELF-124`) | 요청서 12 행 → 판정문 §7 권장 문장 (*"이번 Rint 수정 두 커밋은 봉인 32 개를 변경하지 않았다. 대조 핀 이후의 다른 트랙 변경까지 포함한 전체 스냅샷의 동일성은 별도다."*) · 19 행 → *"78/135 (시험 작성 중간 시점 · 135 개) → 138/138 · 현재 시험 138 을 옛 코드에 = 81/138"* · 원문은 지우지 않고 정정 표지 · 원장 첫 줄 = 이력 (verification_note 의 구분으로 충분) | **그대로 반영** — 다음 커밋에서 `SELF-124` claimed_fixed |
| Q6 | Codex 재확인 시점 | (가) 단독 짧은 재확인 (Q1 · Q3 · Q4 수정 diff + 탐침 재실행) (나) Rint ② 설계 리뷰 요청 (`docs/reviews/rint_carbon_additive_plan_20261020.md` Q12 = 구현 전 한 회차) 에 절을 나눠 함께 | **(나) 함께** — 셋 다 P3 · ①′ 정량 채택 HOLD 를 바꾸지 않고, S2 가 같은 조인 · 관문 위에 서므로 ② 구현 전에 고친 조인을 같은 회차에서 보는 편이 맞다 (② 요청이 늦어지면 (가) 로) |

## 3. 순서 (비준 뒤)

1. 시험 먼저 (고치기 전 실패 확인) — Q2 의 반례 (`RIMPR-R01` 10 건 · Q3 1e160 · Q4 전각) 를 `scripts/test_rint_g2_join.py` 에 · 정상 양성 묶음 그대로 · 고치기 전 판의 실패 수를 기록 (판 · 집합을 같이 적는다 — `SELF-124` 교훈).
2. 수정 (Q1 · Q3 · Q4) — 기존 시험 138 + `test_rint_g2_am_iface.py` 136 · `test_rint_g2_rrm.py` 55 · t4 · t43 · t2 · 두 selftest 그대로 통과 · iface 끔 무영향.
3. 문서 (Q5) — 요청서 정정 표지 · 원장 `RIMPR-R01` · `RIMPR-03` · `RIMPR-04` (Q3 가 (가) 여도 open 유지 — 조건 ①) · `SELF-124` claimed_fixed.
4. Codex (Q6) — 수정 diff + 이번 묶음 탐침 재실행 요청 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/structure_probe.py` ·
   `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/structure_minimal_replay.py` · `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/numeric_review.py` ·
   `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/numeric_overflow_replay.py` — 고친 뒤 기대: 헤더 반례 10 = 거부 · Q3 (가) 면 1e160 = 거부 · Q4 (가) 면 전각 정수 = 거부 · 그 밖 판정 그대로).
