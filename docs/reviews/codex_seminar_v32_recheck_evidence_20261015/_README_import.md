# 반입 기록 — Codex 연구세미나 덱 v3.2 재확인 (소스 핀 `90ca2c8cd` · 2026-10-15)

- 판정문 (리포 사본) = `docs/reviews/codex_review_seminar_v32_recheck_20261015.md` (묶음 `seminar_recheck_v32_20261014/` 의 같은 이름 파일 · 바이트 그대로 · sha256 `00ca2c76fbf0611748e0eb8759ad4a4f2b6661b5fe8c9921b483ced830294629` · `_verdict_file/` 둘째 사본도 같다).
- 받은 것 = 1저자가 WSL 에서 만든 **미니 묶음** `codex_seminar_v32_recheck_mini_20261015.zip` · sha256 `ae461cdd94ad6d79903b16f38003b4c97999699da26a70e91756f9fb1a821c5d` · 737,170 B · 항목 52.
  원 Codex ZIP `codex_seminar_v32_recheck_20261015.zip` (302 항목 · 57,064,464 B · sha256 `21a16db636fdaa2324115e11ad1343adbaf79d782ffb3b5c857645ae9f088b7a`) 에서
  덱 · PDF · 렌더 · 그림 · 리포 사본 (`source/` · `repo/`) · 2 MB 넘는 파일을 뺀 것이다 — 원 ZIP 의 전 항목 sha256 · 크기 · 넣음 여부 = `_members_original_zip.tsv` (미니 만든 명령이 쓴 그대로).
- 반입 처리: 새 빈 폴더에 복사 → sha256 → 멤버 목록 (절대 경로 · `..` · 링크 0) → 풀기 → **묶음 안 스크립트 (`inspect_deck.py` · `final_checks.py` · 탐침 · `prepare_sources.py` 등) 는 실행하지 않았다** (글로만 보존).
- `_members_mini.tsv` = 미니 묶음 52 항목 전부의 sha256 · 크기 · 처리 (`keep` 26 · `verdict` 1 · `drop` 25) · 뺀 이유.

| 뺀 것 (`drop`) | 이유 (반입 때 대조) |
|---|---|
| `seminar_recheck_v32_20261014/external_fetched/` | 문헌 카드 6 = litdb 정본 커밋 ebfed0ff5 의 litdb/papers/ blob 과 sha256 같음 · LIGGGHTS 헤더 4 = source_upstream/ 과 바이트 같음 (공개 LIGGGHTS-PUBLIC 3d5c00f) |
| `seminar_recheck_v32_20261014/source_upstream/` | LIGGGHTS-PUBLIC 3d5c00f 공개 원본 4 (normal_model_hooke_hysteresis.h · rolling_model_cdt.h · surface_model_default.h · tangential_model_history.h) — 이전 키트 반입과 같은 처리 |
| `seminar_recheck_v32_20261014/agents/lit/` | 문헌 카드 6 = 정본 ebfed0ff5 blob + 파일 끝 개행 하나 (판정문 §2 가 적은 그대로 · 끝 개행을 뺀 바이트 같음) |
| `seminar_recheck_v32_20261014/input/codex_seminar_deck_v3_2_recheck_request_20261014.md` | 우리 요청서 = 핀 90ca2c8cd 의 같은 경로 blob 과 sha256 같음 |
| `seminar_recheck_v32_20261014/baseline/ps73_logs.tgz` | = 리포 docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz (sha256 같음 · 원 고정판 이완 로그) |
| `seminar_recheck_v32_20261014/evidence/pin_commit.json` | GitHub API 의 우리 커밋 90ca2c8cd 응답 (패치 포함 · git 이력으로 재현) |
| `seminar_recheck_v32_20261014/evidence/lit_branch_commit.json` | GitHub API 의 litdb 정본 커밋 ebfed0ff5 응답 (git 이력으로 재현) |
| `_verdict_file/codex_review_seminar_v32_recheck_20261015.md` | 판정문 둘째 사본 (sha256 같음) |

- 판정문 · 노트의 상대 경로 (`evidence/…` · `agents/…` · `inspect_deck.py` · `final_checks.py` …) 는 **묶음 루트 (`seminar_recheck_v32_20261014/`) 기준**이다 — 리포에서는 이 폴더가 그 루트다.
  판정문의 리포 경로 · 줄 번호 (`slide_text_v32.md:44,89` 등) = 소스 핀 `90ca2c8cd` · PPTX 내부 경로 (`ppt/slides/slide18.xml`) = 제출 덱 (리포 밖 · 덱은 커밋하지 않는다).
- 판정문이 적은 포장 누락 (요청서 §6 의 원 수식 PPTX `8e76819a…` 가 ZIP 에 없음) = 원장 `SELF-117` (다음 ZIP 에 넣는다).
