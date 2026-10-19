# 증거 — L214R-S06 (Codex 표기 L214S-CX01 · P3) 빈 ATX 제목도 절 경계 (2026-10-19)

근거 = Codex 재확인 3 판정 §3-2 (S01 · S02 · S04 짧은 재확인 · 검토 핀 `685c2bbdb` · 판정문 · 증거 묶음 lhs214s_recheck_20261019 의 반입 = 본 세션) ·
1저자 10-19 수정 계획 Q1 (가).  기계 = 이 컨테이너 (Linux · Python 3.11.17).
"고치기 전" = 커밋 `216951103` 의 `scripts/supp20_input_receipt.py` (tool sha256 `bcd66961…`) · "고친 뒤" = 이 항목의 커밋 내용 (tool sha256 `2c7e0b81…`).
도구는 봉인 32 밖 → 대기 지문 `2149f8738bb2…` 그대로 (selftest 상태 pending 그대로 · S0 · S0b 통과).

## 시험 · 대조

| 시험 | 고치기 전 | 고친 뒤 | 기록 |
|---|---|---|---|
| `supp20_input_receipt.py --selftest` | 120/122 (새 둘 실패: S12k = 12 꼴 rc 0 · 실패 칸 [] · 값 수용 · S12k2 = 2 꼴 rc 1 · R0 · D1) | 122/122 | `tests/s06_before.log` · `tests/s06_after.log` |
| Codex 빈 제목 반례 19 문서 다시 읽기 (oracle = Codex 판정표의 markdown-it-py 결과) | oracle 과 불일치 14 (fail-open 12 · 거짓 거부 2 — Codex 실측과 차이 0) | 0 (바뀐 문서 = 그 14 뿐 · 대조 5 그대로) | `headings_before.json` · `headings_after.json` |
| Codex 울타리 반례 114 문서 (S01 행렬 · 표준 파서와 제목 불일치) | 0 | 0 — 114 문서 판정 · 영수증 칸 전부 S01 증거 `docs/reviews/lhs214s_fix_evidence_20261019/s01_fences_rerun/fences_after_s01.json` 와 같음 (`tree` 칸만 다름) | `fences_after.json` |
| 실제 보충 20 등록 영수증 · 등록 값 · §3 글 | rc 1 · 실패 칸 [D1] (승인 전 정상) | rc 1 · [D1] — 다른 곳 = 생성 시각 · 도구 자신의 sha256 · 작업 사본 dirty 표시뿐 (값 · 사유 · §3 글 · 대조 칸 같음) | `noimpact/receipt_old.json` · `noimpact/receipt_new.json` |
| (추가) markdown-it-py 3.0.0 commonmark 와 줄 단위 대조 — 0 열 `#` 줄 275,148 개 (그중 제목 34,122) | — | 제목 여부 · 수준 · 제목 글 불일치 0 · 옛 식보다 새로 제목 11,754 · 빠진 제목 0 · §3 식별 차이 0 | `commonmark_fuzz/fuzz_atx_after.json` |
| (추가) 같은 파서와 문서 단위 대조 — 활성 §3 + 줄 4 개 (22 종 조합) + 값 = 234,256 문서 | 불일치 29,784 | 0 | `commonmark_fuzz/fuzz_doc4_before.json` · `commonmark_fuzz/fuzz_doc4_after.json` |

- 실제 등록 문서 (110 줄) 에는 새로 경계가 되는 줄이 없다 — 옛 식 · 새 인식 제목 9 = 9 (같은 줄 · 같은 제목 글).

## 고친 것 (`scripts/supp20_input_receipt.py` 만)

- 제목 인식 = 0 열 ATX 제목 (CommonMark 0.31.2 §4.2): `#` 1–6 개 뒤가 **줄 끝 또는 space · tab** 이면 제목 — 내용은 비어도 된다 (`_MD_ATX_OPEN` · `_md_atx`).
  제목 글 = 끝 space · tab 를 떼고 · space · tab 바로 뒤의 닫는 `#` 줄을 떼고 · 앞뒤 space · tab 를 뗀 것.  NBSP · U+2003 은 내용이다 (그래서 `## ` + NBSP 도 제목 = 경계) ·
  `#5 bolt` · `#hashtag` · `#` 7 개 · `#` 바로 뒤 NBSP 는 제목 아님.
- `_md_section` — 경계 = 위 제목 전부 (빈 제목 포함) · 활성 절 식별 (수준 2 · 제목이 '3.' 로 시작) 은 옛 규칙 그대로 (빈 제목은 해당 없음 — 줄 단위 대조의 §3 식별 차이 0).
  옛 판은 한 식 (`#` 뒤 공백 + `\S` 로 시작하는 내용) 으로 두 일을 해, 빈 제목 · 내용이 NBSP · U+2003 뿐인 제목을 경계로 보지 않았다.
- 그대로: 울타리 처리 (S01 — 열 수 들여쓰기 · 닫는 줄 꼬리 space · tab 만) · Q2 (활성 §3 의 code_fp = 그 절 안 울타리 밖 줄에서만) · 수준 규칙 (h1 · h2 만 h2 절을 끝냄 · 빈 h3–h6 은 제목이지만 끝내지 않음).

## 새 시험 (S12k–S12k4)

- S12k ★ = Codex fail-open 12 꼴 (h1 · h2 × 줄 끝 · space · tab · space+tab · space+NBSP · space+U+2003) — 값 없는 활성 §3 → 빈 제목 → `code_fp` 줄 →
  거부 = 이름 있는 경계와 같은 실패 (rc 1 · 실패 칸 정확히 {R0 · D1} · R0 = "§3 안 자리 없음" · 읽은 code_fp None).
- S12k2 ★ = Codex 거짓 거부 2 꼴 — 활성 §3 의 값 (이 체크아웃 지문 = 지금 대기 지문) → 빈 h1 · h2 → 다른 역사 값 (0 × 64) → 활성 값 수용 (rc 0 · 실패 칸 []).
- S12k3 (대조 · 고치기 전도 통과) = 이름 있는 h1 · h2 경계 뒤 값 · 활성 §3 의 값이 코드 블록 속에만 · 정상 활성 값 · 활성 값 + 다른 값을 담은 코드 블록 (Codex 대조 5).
- S12k4 (지킴 · 고치기 전도 통과 · 24 꼴) = 제목 아닌 줄 · 빈 h3 · h6 · 울타리 속 빈 `#` · `##` = h2 절을 끝내지 않음 / 이름 있는 제목 · 닫는 `#` 줄 제목 = 경계 /
  §3 식별은 닫는 `#` 줄과 무관 (`## 3. ##` · `## 3.<tab>#` = §3 · `## 3.##` = §3 아님).
- "고치기 전" 기록 = 커밋 `216951103` 의 파일에 이 새 시험 묶음만 넣어 실행 (작업 트리에 잠시 바꿔 넣고 돌린 뒤 되돌림 — 되돌린 파일 = 고친 판과 바이트 같음).
  재고 대장 `docs/reviews/selftest_inventory.tsv` 의 이 도구 행에 같은 수를 덧붙였다.

## 다시 돌리기

- 빈 제목 반례: `python3 -B repro_headings.py <트리> <묶음 폴더 lhs214s_recheck_20261019> <out.json>` — 사본 = 이 폴더의 `repro_headings.py` (본 세션 재현 스크립트 그대로) ·
  입력 = 묶음의 evidence/s01_new_cases 19 문서 · oracle = 같은 묶음의 s01_heading_boundary_cases 표.  Codex 탐침은 실행하지 않았다.
- 울타리 114: `docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/_repro_ours_20261019/repro_fences.py` (S01 과 같은 명령).
- 무영향: `docs/reviews/lhs214s_fix_evidence_20261019/s01_noimpact/dump_receipt.py` (S01 과 같은 스크립트) — 고치기 전 = 손대기 전의 깨끗한 작업 트리 (HEAD 커밋 `216951103`) ·
  고친 뒤 = 같은 트리의 수정본 (그래서 dirty 표시 · 생성 시각이 다르다).
- CommonMark 대조: `commonmark_fuzz/fuzz_atx.py` · `commonmark_fuzz/fuzz_doc.py` — markdown-it-py 3.0.0 (Codex oracle 과 같은 판) 을 리포 밖 임시 폴더에만 설치해 돌렸다
  (`pip install --target`) · 리포 · CI 의존 아님.  "고치기 전" 문서 대조 = 커밋 `216951103` 의 파일을 잠시 바꿔 넣고 돌림 (각 JSON 의 tool_sha256 칸이 쓴 파일).

## 한정

- 지원 범위 = 울타리 코드 블록 · 0 열 ATX 제목 (빈 제목 포함) — 들여쓴 코드 블록 · 목록 · 인용 · HTML 블록 · 1–3 칸 들여쓴 제목 · setext 제목은 해석하지 않는다
  (옛 판과 같음 · setext 는 이번에 docstring 에 적었다).  그런 꼴의 제목은 경계가 아니다 (CommonMark 와 다름 — 판정문 §3-1 이 요구하지 않은 범위) ·
  HTML 블록 안의 0 열 `#` 줄은 제목으로 본다 (옛 판도 내용 있는 제목은 같았다).
- 줄 끝 = `\n` — 등록 문서는 `read_text` (universal newline) 로 읽어 `\r\n` · `\r` 이 `\n` 이 된다 (Codex 사본 19 문서는 CRLF · 같은 판정).
- CommonMark 대조 = Codex 판정표의 표준 파서 결과 (19 · 114 문서) + 이 컨테이너의 같은 판 markdown-it-py 생성 대조 (위 지원 범위의 줄 · 문서 꼴만) — 전 문법 보증 아님.
- 원장 · 진행 기록 · CLAUDE.md 는 이 커밋에서 고치지 않았다 (본 세션 몫).
