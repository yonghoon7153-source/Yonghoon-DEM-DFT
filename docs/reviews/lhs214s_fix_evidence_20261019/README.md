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

## S02 — R01 경계 시험의 환경 의존 (`scripts/test_l214r_r01_restored_full.py` · 시험만 — 생산 코드 · 판정식 · 합격선 그대로)

| 실행 | 고치기 전 | 고친 뒤 | 기록 |
|---|---|---|---|
| 그대로 (이 컨테이너) | 27/27 | 30/30 | `tests/s02_after_normal.log` |
| 등록 입력 box_y +18 ULP (이 컨테이너에서 Codex 환경 꼴 — 출발 raw q 1.4999999999999962 · …960 · …956) | **23/26** (Codex 와 같음: E1 · E3 실패 · E4 `KeyError: 'q_withheld'` · E5 미실행) | 30/30 (E0 탐색 18 · 18 · 17 걸음) | `tests/s02_before_shift18.log` · `tests/s02_after_shift18.log` |
| 등록 입력 box_y −18 ULP (반대 꼴 — 출발 raw q 셋 다 문턱 위) | — | 30/30 | `tests/s02_after_shift-18.log` |

- 고친 것: E0 = 이 환경에서 실 사슬 H0 raw q 가 세 경계와 **정확히** 같아지는 box_y 를 등록 입력에서 ULP 한 걸음씩 찾는다 (상한 512 · 허용 폭 없음 · 엄격 > 그대로 ·
  q = G·T/(bx·by) 의 단조성 · 건너뛰면 그 칸 문제) → 못 찾으면 E1–E4 = 전제 불성립 FAIL (KeyError 로 끊기지 않는다) · E3 가 아니면 E4 는 복원을 부르지 않는다 ·
  E5 (3 노드 정확 경계) = 독립 묶음 · E′ = 찾은 정확한 입력에서 ±18 ULP 출발 → 같은 판정 (이식성 상주 시험) · 복원 helper = 보류 증서가 아니면 KeyError 대신 사유.
- "고치기 전" 기록 = 부모 커밋의 시험 파일을 **바이트 그대로** 불러 E_BY 만 이동해 실행 (`docs/reviews/lhs214s_fix_evidence_20261019/s02_run_shifted.py` — 파일 sha256 을 로그 첫 줄에 적는다).
  Codex 의 원 실패 로그 = 반입 증거 `docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/evidence/rr_numeric_submitted_test_l214r_r01_restored_full.log` (보존 · 덮지 않음).
- 한정: 이식성은 이 컨테이너에서 ±18 ULP 이동으로 재현한 꼴 — Codex Windows 환경에서 다시 돈 것은 아니다 (재확인에서 확인 요청).
