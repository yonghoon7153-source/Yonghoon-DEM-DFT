# 믹서 문헌 매트릭스 (2026-11-23) — 웹앱 `/mixer/lit` 자료

믹서 원고 (건식 혼합 DEM · 점착 대비) 의 **문제 정의**와 **공백 주장 G1–G4 의 근거**를 한 표로 모은 문헌 행렬이다.
76 행 = 정본 카드 53 + 카드 전 (제목만) 23.  **개발 자료 · 예비 판정** — 원고 문장의 근거로 옮기기 전에 아래 '상태' 를 본다.

## 파일

| 파일 | 내용 |
|---|---|
| `matrix.json` | 원자료 — `meta` (기준 커밋 · 포함 규칙 · 범례) + `rows` 76 |
| `matrix.tsv` | 같은 76 행을 표 꼴로 (열 이름 = 첫 줄) |
| `gap_check.md` | G1–G4 반례 검사 — 판정 (holds · weakened · broken) · 반례 카드 줄 · 좁힌 문장 (권고) |
| `excluded.md` | 뺀 것 — 카드 202 + 큐 3 · 줄마다 이유 |
| `gap_summary.json` | `gap_check.md` 에서 뽑은 공백 4 개 요약 (웹앱 공백 카드) |

## 출처

- 기준: litdb 정본 가지 `origin/claude/friendly-meitner-lldvar` @ 커밋 `a65bbdb24` (`meta.ref_sha` = a65bbdb24a1b363fe81746a665aeb2a94e8e585d · `litdb/papers/` 는 커밋 `d0b7bfb88` 과 같다 — 사이에 바뀐 것은 `_curation` 뿐).
- 2026-11-23 litdb 카드에서 만들었다.  카드 행의 근거 = 카드 줄 번호 (`card_refs`) · 숫자는 **카드에 인쇄된 그대로** (`[인쇄]` · `[판독]` · `[카드 산술]` 표지도 그대로).
- 제목 행 (`card` = none · `classified_by` = title) 은 제목 · `status.tsv` · `S8_candidates.md` 후보 표 설명 · `queue.json` 메모로만 분류했다 — 원문 · 카드로 확인하지 않았다 (웹앱 표지 **카드 전**).
- 범위: 이 서랍 (정본 카드 + 큐) 안에서만 찾았다.  서랍 밖 문헌은 찾지 않았다.

## 상태 — 예비 판정

- N-110 · N-112 (두 편) · N-150–N-153 카드를 아직 쓰는 중이다 (N-112 첫째 = `status.tsv` '도는 중').  카드가 나오면 판정 (특히 G1 · G4 · G3) 이 더 좁아질 수 있다 → 그때 `gap_check.md` 를 다시 대조하고 새 날짜 폴더로 다시 만든다 (이 폴더는 고치지 않는다).
- `lee2026_mechanical_halogen_argyrodite_drycoating` 은 우리 랩 논문 (카드 L8) — 반례 · 근거로 쓸 때 자기 인용임을 밝힌다 (`gap_check.md` 불확실 3).

## 결정

1저자 11-23 Q4 — 믹서 문헌 매트릭스를 웹앱에서 보인다 → `/mixer/lit` (읽기 전용 · 개발 자료 · 예비 판정).

## `gap_summary.json` 은 어떻게 뽑았나

- 기계로 뽑음 (`gap_check.md` 그대로): `claim` = 절 제목 · `verdict` = 판정 줄의 첫 낱말 · `verdict_note` = G2 의 분야 한정 (판정 줄 그대로 · 나머지는 null) · `verdict_reason` = 판정 줄의 나머지 (강조 `*` 만 뗌) · `narrowed_wording` = 절 끝 '좁힌 문장 (권고)' 그대로 · `source` = 줄 번호.
- 손으로 나눔: `strongest_counterexample` = 요약 표 칸을 slug · 줄 · 한 줄로 나눔 (둘째 반례 = `also`) · `pending_cards` = 절의 '반례 후보' 단락에 나온 카드 전 번호 전부 (`in_summary_table` = 요약 표에 오른 것 · `note_ko` = 그 단락 문구를 줄임).
- 웹앱 시험 `webapp/test_mixer_lit_page.py` 가 이 값들을 `gap_check.md` · `matrix.json` 과 다시 대조한다.

## 다시 만들기

`matrix.json` · `matrix.tsv` · `gap_check.md` · `excluded.md` · `gap_summary.json` 은 scratch 도구 · 리포 밖 (행 파일 · `build.py` · `make_excluded.py` · 요약 추출기) 으로 만들었다 → 리포에서 그대로 다시 만들 수 없다.  고칠 일이 생기면 새 날짜 폴더로 만든다.

## 웹앱

`/mixer/lit` — 읽기 `webapp/app.py` (`_mixer_lit_data`) · 화면 `webapp/templates/mixer_literature.html` · 시험 `webapp/test_mixer_lit_page.py`.  자료가 없거나 깨지면 화면이 200 + 안내를 낸다 (빈 화면 · 500 없음).
