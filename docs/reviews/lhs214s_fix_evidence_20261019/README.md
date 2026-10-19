# 증거 — LHS214 재확인 2 의 새 P3 수정 (L214R-S01 · S02 · S04 · Codex 표기 L214RR2-01 · 02 · 04) (2026-10-19)

근거 = Codex 재확인 2 판정문 `docs/reviews/codex_review_lhs214rr_fix_recheck_20261019.md` §2 · §4 · §5 · 수정 계획 `docs/reviews/lhs214s_fix_plan_20261019.md`
(✅ 1저자 10-19 *"권고대로 ㄱ"* — Q1 (가) · Q2 (가) · Q3 다음 세대 · Q4 같이 · Q5 S01 → S02 → S04 커밋 하나씩) · 우리 트리 재현
`docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/_repro_ours_20261019/README.md`.
기계 = 이 컨테이너 (Linux · Python 3.11.17 · NumPy 2.4.6 · SciPy 1.17.1 · `OMP_NUM_THREADS=1`).  "고치기 전" = 부모 커밋 `be75bdd07` 의 코드 (리포 밖 복제본) ·
새 시험을 먼저 넣고 실행.  "고친 뒤" = 그 항목의 커밋 내용.

## S01 — 등록 파서 공백 (`scripts/supp20_input_receipt.py` · 봉인 밖 → 대기 지문 `2149f8738bb20b6a…` 그대로)

| 시험 | 고치기 전 | 고친 뒤 | 기록 |
|---|---|---|---|
| `supp20_input_receipt.py --selftest` | 114/118 (새 넷 실패: S12i 32 꼴 rc 0 · S12i3 · S12j · S12j2) | 118/118 | `tests/s01_before.log` · `tests/s01_after.log` |

- 고친 것: 울타리 줄 들여쓰기 = 열 수 (탭 = 다음 4 의 배수 열 · CommonMark §2.2 · 0–3 열만 울타리) · 닫는 줄 꼬리 = space · tab 만 (§4.5) ·
  Q2 (가) = 활성 §3 의 `code_fp` 는 그 절 안 **울타리 코드 블록 밖** 줄에서만 읽는다 (`_md_section(…, strip_code=True)`).
- 새 시험: S12i = Codex 판정표의 32 꼴 (두 문자 × 길이 3 · 4 · 5 · 8 × 탭 · 공백+탭 들여쓰기 · NBSP · U+2003 꼬리) → rc 1 · R0 · code_fp None ·
  S12i2 (지킴) = 닫는 줄 들여쓰기 0 · 1 · 3 칸 · 꼬리 space · tab 40 꼴 = 활성 §3 (고치기 전도 같음) · S12i3 = 탭 들여쓴 여는 줄 = 울타리 아님 (표준 판정) ·
  S12j = §3 안 코드 블록 속에만 값 → rc 1 · R0 · S12j2 = 울타리 밖 값 + 다른 값을 담은 예시 블록 → 실물 값 하나 (고치기 전: 값 둘 = R0 실패).
- Codex 반례 114 문서 다시 읽기 (`s01_fences_rerun/fences_after_s01.json` · 스크립트 = `docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/_repro_ours_20261019/repro_fences.py` 를 고친 코드 트리에) =
  표준 파서 (Codex 판정표의 markdown-it-py 결과) 와 활성 §3 판정이 다른 문서 **32 → 0** · 바뀐 판정 = 그 32 꼴 + `active_section_fenced_value` (rc 0 → 1) 뿐.
- 무영향 (`s01_noimpact/`) — 실제 보충 20 등록 문서의 영수증 · 등록 값 · §3 글: 고치기 전 (`receipt_old.json`) ↔ 고친 뒤 (`receipt_new.json`) 다른 곳 =
  도구 자신의 sha256 과 작업 사본 dirty 표시 둘뿐 (rc 1 · 실패 칸 [D1] = 승인 전 정상 · 값 열한 개 · 대기 선언 같음).  만든 스크립트 = `s01_noimpact/dump_receipt.py`.
- 한정: 지원 범위 = 울타리 코드 블록 · ATX 제목 (`#` 0 열) — 들여쓴 코드 블록 · 목록 · 인용 · HTML 블록 · 1–3 칸 들여쓴 제목은 해석하지 않는다
  (들여쓴 제목은 제목으로 안 보여 §3 이 없으면 fail-closed).  CommonMark 대조는 Codex 판정표의 표준 파서 결과로만 (우리는 markdown-it-py 를 다시 돌리지 않았다).
