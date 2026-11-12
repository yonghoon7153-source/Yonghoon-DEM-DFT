# litdb 정리 키트 — 논문 에이전트를 두 세션이 나눠 돌린다 (2026-11-12 · 1저자 요청)

정본 가지 `claude/friendly-meitner-lldvar` 안의 공용 자리다.  카드 · 크롭 · 인덱스 규칙 = `litdb/README.md` + 이 폴더 `CURATOR_BRIEF.md` · `COMMON.md`.  후보 표 (대시보드) = `S8_candidates.md` · 진행 상태의 정본 = `status.tsv` · 추가로 필요한 논문 = `wishlist.md`.

## 1. 나눔 (겹치지 않게)

| 세션 | 맡는 것 | 정독 출력 NN |
|---|---|---|
| 본 세션 (stoic 가지 세션) | 후보 표 1 순위 N-1–N-51 (PDF 가 그 세션에 있다) | 43–100 |
| 대피 세션 (pqwtv8 가지에서 띄운 세션 · 논문 에이전트 한정) | 후보 표 2 · 3 순위 N-52 부터 (1저자가 그 세션에 PDF 를 준다) | 101 부터 |

- 제외 (1저자 · 내려받기 불가): N-31 · N-57 · N-58 · N-59 · N-72 첫째 (Walton–Braun 1986).  N-28 = 정본 doerrer2021 §13 보탬으로 끝.
- **시작 전 `status.tsv` 에 한 줄 (N · 세션 · 도는 중 · 시각) 을 더해 push 한 뒤 시작한다.**  push 가 막히면 fetch 해서 같은 N 줄이 이미 있는지 본다 — 있으면 하지 않는다.  끝나면 그 줄을 끝 (slug · 커밋) 으로 고친다.  1저자가 순서를 바꾸면 그 말이 앞선다.
- 중복 확인은 INDEX 가 아니라 `litdb/papers/` 파일 목록 + DOI · 제목 낱말 · 저자 grep (같은 저자 · 같은 해 다른 논문 조심 — slug 를 다르게 · 서로 가리키게 "관련 카드" 한 줄씩).

## 2. 정본 push 규칙 (세 군데 이상이 같은 가지에 push 한다)

- 시작할 때와 push 직전에 `git fetch origin claude/friendly-meitner-lldvar` → 원격 끝 위로 rebase.  충돌이 INDEX.md · INDEX_DEM.md · comparison_vs_ours_DEM.md · figures/_sources.json · pdf_map.tsv · 이 폴더 파일에서 나면 **두 쪽 줄을 다 살려** 푼다 (남의 카드 · 줄은 지우지 않는다).  push 가 non-fast-forward 로 거부되면 다시 fetch · rebase.  **강제 push 금지.**
- INDEX_DEM.md = `python3 tools/litdb/build_index.py` 로 재생성 (손편집 금지) · 끝에 `python3 tools/litdb/build_index.py --check`.
- 충돌 풀기 세부: INDEX_DEM.md 충돌은 손으로 풀지 말고 rebase 뒤 재생성 · `figures/_sources.json` 은 두 쪽 항목을 다 살린 뒤 `python3 -m json.tool` 로 읽히는지 확인 · 그림 도구가 **남의 카드** `_sources` 항목까지 고쳤으면 그 부분은 되돌린다 · `tools/litdb/build_index.py` 의 SIZE_EFFECT_SLUGS 같은 목록 충돌은 두 줄 다 남긴다.
- 카드 (`papers/<slug>.md`) · 그림 폴더 (`figures/<slug>/`) · 정독 출력 (NN 범위가 나뉨) 은 세션마다 다른 파일이라 충돌하지 않는다 — 충돌은 위 공용 파일에서만 난다.
- 이 가지 밖 (코드 · 문서 가지) 에는 쓰지 않는다.  litdb 한정 커밋 · push 는 1저자 상시 승인.
- 커밋 메시지 끝 두 줄 = 그 세션의 공동 저자 · 세션 줄 (모델 이름은 넣지 않는다).

## 3. 한 편을 처리하는 순서

1. PDF (본문 · SI) 를 정본 작업 트리의 `litdb/inbox/` 에 둔다 (git 이 무시하는 자리).
2. 첫 쪽에서 서지 (저자 · 제목 · 학술지 · 권 · 쪽 · DOI) 를 확인한다 — 후보 표의 서지와 다르면 원문을 따르고 보고.
3. `status.tsv` 시작 줄 push → 논문 에이전트 (litdb-curator) 를 띄운다.  지시 = `COMMON.md` + 그 후보의 S8 행 ('왜' 칸 = 고른 의도 · 근거 칸 = 가리킨 카드 · 중복 확인 칸) + 서지 + 정독 출력 NN + 본으로 삼을 카드 (비슷한 정본 카드 하나).
4. 끝나면 모음 그림 (sheet png) 을 1저자에게 보내고 · `status.tsv` 를 끝으로 고쳐 push · 1저자에게 12 줄 안으로 보고 (+ 의도 대조 한 줄).
5. 한 세션에서 동시에 에이전트 둘까지 (무거운 병렬 실행 없이 · 크롭 렌더는 한 번에 한 쪽씩).

## 4. 정독 출력 (질문 a–n)

`READING_BRIEF.md` 의 `batch_NN.tsv` · `batch_NN_findings.md` 꼴 그대로 · 자리 = 이 폴더 `reading/` (카드와 같은 커밋으로 push).  본 세션 출력 (NN 43–100) 은 본 세션 scratchpad 에 있다 — 본 세션이 나중에 이 폴더로 옮긴다.

## 5. 추가로 필요한 논문 (두 세션 공통)

카드를 쓰다 "원문을 봐야 하는데 정본 카드가 없는" 문헌이 나오면 `wishlist.md` 에 한 줄 (꼴은 그 파일 머리).  서지는 **원문 참고문헌 목록에서만** — 기억 · 검색 요약으로 채우지 않는다 (모르면 [미확인]).  1저자가 여기서 골라 PDF 를 준다.

## 6. 환경 메모

- (대피 세션 · 11-12) 그림 도구 `tools/litdb/extract_figures.py --selftest` 는 PyMuPDF 1.28.2 에서 84/84 통과 · 새로 깔리는 2.1 에서는 1 건 실패 (그림 옆에 붙은 캡션을 못 잡음).  컨테이너를 새로 받으면 `python3 -m pip install "pymupdf==1.28.2" pillow numpy` 뒤 `--selftest` 부터 돌린다.
