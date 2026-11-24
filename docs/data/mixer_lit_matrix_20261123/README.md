# 믹서 문헌 매트릭스 (2026-11-23 · 11-24 갱신) — 웹앱 `/mixer/lit` 자료

믹서 원고 (건식 혼합 DEM · 점착 대비) 의 **문제 정의**와 **공백 주장 G1–G4 의 근거**를 한 표로 모은 문헌 행렬이다.
77 행 = 정본 카드 67 + 카드 전 (제목만) 10.  **개발 자료 · 예비 판정** — 원고 문장의 근거로 옮기기 전에 아래 '상태' 를 본다.
(11-23 판 = 76 행 = 정본 카드 53 + 카드 전 23 → 2026-11-24 갱신 = 큐 14 편의 정본 카드 반영 · 아래 '11-24 갱신'.)

## 파일

| 파일 | 내용 |
|---|---|
| `matrix.json` | 원자료 — `meta` (기준 커밋 · 포함 규칙 · 범례 · 고친 날 `updated` · 갱신 메모 `update_note`) + `rows` 77 |
| `matrix.tsv` | 같은 77 행을 표 꼴로 (열 이름 = 첫 줄 · 37 열) |
| `gap_check.md` | G1–G4 반례 검사 — 판정 (holds · weakened · broken) · 반례 카드 줄 (11-23 판 · 11-24 새 카드) · 좁힌 문장 (권고) |
| `excluded.md` | 뺀 것 — 카드 202 + 큐 3 · 줄마다 이유 (11-23 판 그대로 — 두 기준 사이에 새로 생긴 카드는 큐 14 편뿐이고 모두 행으로 넣었다) |
| `gap_summary.json` | `gap_check.md` 에서 뽑은 공백 4 개 요약 (웹앱 공백 카드 · 11-24 부터 근거 카드 `evidence_cards`) |

## 출처

- 기준 (11-24): litdb 정본 가지 `origin/claude/friendly-meitner-lldvar` @ 커밋 `c32e89830` (`meta.ref_sha` = c32e89830e05b2d588c9d4d0f2bf6c8e62e58f7e · N-157 끝 상태표 커밋).
- 11-23 판 기준: 커밋 `a65bbdb24` (a65bbdb24a1b363fe81746a665aeb2a94e8e585d · `litdb/papers/` 는 커밋 `d0b7bfb88` 과 같다 — 사이에 바뀐 것은 `_curation` 뿐).  두 기준 사이 `litdb/papers/` = 새 카드 14 (617 → 631 .md) + 기존 카드 21 장에 줄 덧붙임 — 덧붙은 줄은 모두 카드 끝 (링크 절) 이라 기존 카드 행 53 의 `card_refs` 와 `gap_check.md` 의 11-23 줄 번호가 그대로 맞다 (git diff -U0 로 확인 · 11-24) · `status.tsv` 는 제자리 고침이라 남은 제목 행의 줄 번호도 같다.
- 카드 행의 근거 = 카드 줄 번호 (`card_refs`) · 숫자는 **카드에 인쇄된 그대로** (`[인쇄]` · `[판독]` · `[카드 산술]` 표지도 그대로).
- 제목 행 (`card` = none · `classified_by` = title) 은 제목 · `status.tsv` · `S8_candidates.md` 후보 표 설명 · `queue.json` 메모로만 분류했다 — 원문 · 카드로 확인하지 않았다 (웹앱 표지 **카드 전**).
- 범위: 이 서랍 (정본 카드 + 큐) 안에서만 찾았다.  서랍 밖 문헌은 찾지 않았다.

## 상태 — 예비 판정

- 11-24: 큐 14 편 (N-110 · N-111 · N-112 두 편 · N-113 · N-118 · N-150–N-157) 이 정본 카드가 되어 반영했다.  남은 카드 전 10 행 (N-95 · N-102 · N-103 · N-114 두 편 · N-115 · N-116 · N-117 · N-127 · N-129) 은 11-23 제목 판정에서 어느 공백의 반례 · 부분 후보도 아니다 (다시 읽지 않음) — 그 카드가 나오면 다시 대조한다.
- `lee2026_mechanical_halogen_argyrodite_drycoating` 은 우리 랩 논문 (카드 L8) — 반례 · 근거로 쓸 때 자기 인용임을 밝힌다 (`gap_check.md` 불확실 3).
- 1저자 답 대기 (인계 `docs/handoff_return_to_stoic_knuth_20261124.md` §3-3): Q1 Figueroa 2009 를 논지 §2 의 출처로 넣기 · Q2 공백 · 새로움 문서 v0 — 이 표는 그 재료다 (판정은 예비).

## 결정

- 1저자 11-23 Q4 — 믹서 문헌 매트릭스를 웹앱에서 보인다 → `/mixer/lit` (읽기 전용 · 개발 자료 · 예비 판정).
- 1저자 11-24 — *"믹서 /mixer/lit 페이지 갱신 (litdb 새 카드 14 편 반영 · G1–G4 좁힌 판정 · 시험 먼저 · 웹앱 같은 묶음)"* → 아래 '11-24 갱신'.

## 11-24 갱신 — 무엇이 바뀌었나

- **행 76 → 77**: 11-23 판의 제목 행 13 (N-110 · N-111 · N-112-1 · N-112-2 · N-113 · N-118 · N-150 · N-151 · N-152 · N-153 · N-154 · N-155 · N-156) 을 정본 카드 행으로 바꿨다 (`slug` = 카드 slug · 큐 번호는 `inclusion_reason` 에) · N-157 (D'Amore 2022 · LPSCl 표면 에너지 DFT) 은 새 행.  줄 순서 = 11-23 카드 53 (그대로) → 11-24 카드 14 (큐 번호 순) → 남은 카드 전 10 (11-23 순서 그대로).
- **새 카드 행의 칸** = 11-23 판과 같은 스키마 · 값은 카드 §0 (한 문장 · 표 · 한정어) · §0-2 (공백 검사) 줄에서 · G 판정 = 카드 §0-2 판정 (반례 · 일부 · 없음) 을 이 표의 낱말로 옮김 (규칙 = `meta.legend.gap_notes` · 카드가 '섞임 ↔ 분리' 만 반례라 한 G1 칸 = partial) · 핵심 결과 칸 끝의 *'우리 쪽 함의'* = 카드 산술 · 가정 · 개발 판단 (측정 아님 · 인계 §3-3 표와 같은 내용).
- **제목 기준 판정 (11-23) → 카드 기준 판정 (11-24) 이 바뀐 칸** (26):

| 큐 | 칸 | 11-23 (제목 기준) | 11-24 (카드 기준) |
|---|---|---|---|
| N-110 | G2 | partial | supports |
| N-110 | G3 | unrelated | supports |
| N-111 | G1 | unrelated | supports |
| N-111 | adhesion_handling | theory_parameter | measured_input |
| N-112-1 | G2 | partial | contradicts |
| N-112-1 | adhesion_handling | theory_parameter | measured_input |
| N-112-2 | G2 | unrelated | contradicts |
| N-112-2 | adhesion_handling | theory_parameter | measured_input |
| N-113 | G1 | partial | supports |
| N-118 | adhesion_handling | not_applicable | none |
| N-118 | first_author | Gilchrist, J. F. | Khakhar, D. V. (카드 L15 — 원문 제1 저자) |
| N-150 | G2 | unrelated | supports |
| N-150 | G4 | partial | supports |
| N-151 | G2 | unrelated | contradicts |
| N-151 | adhesion_handling | theory_parameter | measured_input |
| N-152 | G1 | partial | supports |
| N-152 | G2 | partial | contradicts |
| N-152 | G4 | unrelated | partial |
| N-153 | G2 | unrelated | supports |
| N-154 | G3 | supports | partial |
| N-154 | adhesion_handling | not_applicable | none |
| N-155 | G1 | unrelated | supports |
| N-155 | G3 | supports | partial |
| N-155 | G4 | unrelated | supports |
| N-156 | G1 | unrelated | supports |
| N-156 | G3 | supports | partial |

- **공백 판정 낱말은 그대로** (G1 weakened · G2 broken · G3 weakened · G4 weakened) — 판정 이유 · 좁힌 문장 · 가장 강한 반례를 고쳤다 (`gap_check.md`):
  - G1 = 직접 반례 없음 (덮임 ↔ 뭉침을 점착 대비로 예측한 카드는 없다) · 섞임 ↔ 분리 쪽은 Li–McCarthy 2003 · 2005 · 2006 · Figueroa 2009 · Chaudhuri 2006 이 부분 반례 · Jones 2008 = CAB ↔ 혼합 균일도 무관.
  - G2 = '전지 · 황화물 · 같은 SE 탐침 AFM 쌍별 · 압밀 뒤 이온 경로' 로 좁힘 (정면 반례 = Jones 2008 · Li–McCarthy 2003 · 2005 · 2006 · 일부 = Capece 2015).
  - G3 = '점착 대비가 있는 계에서 rpm 축' 의 맞교환 · 최적 · '한 운동 꼴 안' 으로 좁힘 (벽 부착 ↔ 충돌 세기 대조 = Chen 2004 · Dave 2003 · 부분 = Mellmann 2001 · Li–McCarthy 2006 · Chaudhuri 2006 · Liu 2013).
  - G4 = '점착 축을 넣은 상태도' 로 좁힘 (Mellmann 2001 BBD 가 반례에 가까움 · Chaudhuri 2006 은 상태도 없음 = supports).
- **N-157** 은 네 공백 판정을 바꾸지 않는다 (카드 §0-2 = 네 칸 모두 없음) — 함의는 판가름 수의 분모 쪽 γ_S 사전값뿐 (총 표면 에너지 · 점착 일 W 로 바로 쓰지 않음 · `gap_check.md` 불확실 7).
- **`gap_summary.json`**: 새 칸 `evidence_cards` (공백마다 그 절의 근거 카드 — `slug` · `n_id` (11-24 새 카드만) · `verdict` = `matrix.json` 그 행의 G 판정 · `line_ref` · `note_ko` · `since` = 2026-11-23 / 2026-11-24) · `pending_cards` = 빈 목록 (카드 전 후보가 남지 않았다) · `source.candidate_lines` = '반례 후보 — 카드 전: 없음' 줄.
- **`matrix.json` meta**: 새 칸 `updated` · `update_note` (웹앱이 그대로 보인다 — 화면의 옛 고정 문장 *'N-110 · N-112 · N-150–N-153 카드가 나오면 …'* 은 지웠다) · `ref_sha` · `ref_note` · `n_rows` · `n_card_rows` · `n_title_rows` · `inclusion_rule` (N-157 = (d) 의 표면 에너지를 계산값까지 넓힘 · (e) 의 남은 제목 행) · `legend.labels` · `legend.gap_notes` 고침.
- ⚠ 11-23 판 README 는 *"고칠 일이 생기면 새 날짜 폴더로"* 라고 적었지만 11-24 갱신은 **이 폴더 안에서** 했다 (지시 범위 = 이 폴더 파일 + 웹앱 같은 묶음 · 자료 폴더 이름 `_MIXER_LIT_DIR` 은 봉인 32 파일 `webapp/app.py` 안이라 건드리지 않았다).  11-23 판 = git 이력 (커밋 `9012b2492` 의 이 폴더).
- ⚠ `docs/reviews/doc_refs_allowlist.tsv` 의 `evac/tools/queue.json` 등재는 이 폴더 `gap_check.md` 를 *"원본 그대로 · 고치지 않음"* 으로 적는다 — 11-24 에 고쳤다 (그 경로 언급과 a65bbdb24 판 근거 줄은 그대로 남아 등재는 아직 필요하다 · 등재 설명 문구는 이 묶음 밖이라 고치지 않았다).

## `gap_summary.json` 은 어떻게 뽑았나

- 기계로 뽑음 (`gap_check.md` 그대로): `claim` = 절 제목 · `verdict` = 판정 줄의 첫 낱말 · `verdict_note` = G2 의 분야 한정 (판정 줄 그대로 · 나머지는 null) · `verdict_reason` = 판정 줄의 나머지 (강조 `*` 만 뗌) · `narrowed_wording` = 절 끝 '좁힌 문장 (권고)' 그대로 · `source` = 줄 번호.  (11-24: 같은 추출기가 11-23 판 `gap_check.md` 에서 11-23 판 `gap_summary.json` 의 이 칸들을 그대로 다시 낸다는 것을 먼저 확인했다.)
- 손으로 나눔: `strongest_counterexample` = 요약 표 칸을 slug · 줄 · 한 줄로 나눔 (둘째부터 = `also`) · `pending_cards` = 절의 '반례 후보' 단락에 나온 카드 전 번호 전부 (`in_summary_table` = 요약 표에 오른 것 · `note_ko` = 그 단락 문구를 줄임 · 11-24 = 비었다) · `evidence_cards` (11-24) = 절에 나온 카드 행 — 그 G 에서 반례 · 부분인 카드 행은 전부 + 절이 인용한 supports 행 · `verdict` 는 `matrix.json` 에서 옮겨 적고 대조했다.
- 웹앱 시험 `webapp/test_mixer_lit_page.py` 가 이 값들을 `gap_check.md` · `matrix.json` 과 다시 대조한다 (11-24: ㉟–㊼).

## 다시 만들기

`matrix.json` · `matrix.tsv` · `gap_check.md` · `excluded.md` · `gap_summary.json` 은 scratch 도구 · 리포 밖 (행 파일 · `build.py` · `make_excluded.py` · 요약 추출기) 으로 만들었다 → 리포에서 그대로 다시 만들 수 없다.  11-24 갱신도 scratch 도구 (새 카드 행 파일 · 행 조립기 · gap_check 조립기 · 요약 조립기 · 인용 대조기 · json → tsv 변환기) 로 했다.  11-24 검산: json → tsv 변환기가 11-23 판 `matrix.tsv` 를 바이트 같게 다시 만든다 · `gap_check.md` 의 11-24 새 카드 인용 41 개가 그 카드의 가리킨 줄에 그대로 있다 · 조립기가 근거 카드 판정을 `matrix.json` 행과 대조한다.

## 웹앱

`/mixer/lit` — 읽기 `webapp/app.py` (`_mixer_lit_data`) · 화면 `webapp/templates/mixer_literature.html` · 시험 `webapp/test_mixer_lit_page.py`.  자료가 없거나 깨지면 화면이 200 + 안내를 낸다 (빈 화면 · 500 없음).  11-24: 고친 날 · 갱신 메모 (meta) · 공백 카드마다 근거 카드 목록 (펼치기 · 판정 표지 · 11-24 표지) · 카드 전 후보가 비면 '없음' 안내 — `webapp/app.py` 는 바꾸지 않았다.
