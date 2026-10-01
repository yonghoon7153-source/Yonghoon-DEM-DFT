---
title: 일일 GitHub 연구 브리핑 처리 기준
description: "매일 오는 GitHub 연구 브리핑을 받는 절차 — 네 가지 수집 목적(의존성 위험 · 경쟁 도구 · 미세단락 도구 · 실험 아이디어)으로 분류하고, 1차 출처로 대조하고, 브리핑만으로는 RUN_SCOPE 를 건드리지 않는다"
created: 2026-10-01
updated: 2026-10-01
type: guide
tags: [wiki, tooling, research]
sources: [raw/articles/2026-10-01-github-research-briefing.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-opus-5-5
effort: medium
claimType: prescriptive
evidenceScope: user-original
---

# 일일 GitHub 연구 브리핑 처리 기준

## 개요

2026-10-01 부터 GitHub 연구 브리핑이 매일 온다 (첫 회: `raw/articles/2026-10-01-github-research-briefing.md`).
같은 날 사용자가 정한 **수집 목적 네 가지**가 이 페이지의 분류 축이다. 브리핑은 **다른 에이전트의 요약**이다 —
그 자체로 근거가 아니고, 확인할 곳을 알려 주는 색인이다.

## 절차 (브리핑 하나당)

1. **raw 저장:** 원문 그대로 `wiki/raw/articles/YYYY-MM-DD-github-research-briefing.md` (frontmatter `sha256`). 1차
   대조 결과는 같은 파일 하단에 "WebFetch 인용 — 원문 보장 아님" 으로 구분해 붙인다. 이후 수정하지 않는다.
2. **중복:** `wiki/index.md` 에 이미 있는 도구 · 저장소면 그 페이지를 갱신한다 (`updated` bump).
3. **분류 → 라우팅:**

   | 축 | 무엇을 판정하나 | 갈 곳 |
   |---|---|---|
   | ① 의존성 위험 | 우리가 쓰는 도구 (현재 [[pybamm]]) 의 릴리스가 **우리 코드 경로**에 닿는가 — 변경 항목마다 "닿는다 / 아니다 / 열린 물음" 과 이유 | 도구 entity 의 영향 판정표 · 위험이 실재하면 다음 코드 라운드 승인 후보로 |
   | ② 경쟁 · 비교 도구 | 같은 문제 (LLI/LAM 추정) 를 푸는 도구인가, 우리 degeneracy 질문을 적용할 **판정 대상**인가 | 도구 entity (예: [[pyprobe]]) · [[fitting-degeneracy]] · [[22p-physics-or-degeneracy]] Status Log |
   | ③ 미세단락 도구 | ISC 판별을 **실제로** 하는가 (적합도 ≠ 판별) · 라벨이 설계된 데이터인가 | [[isc-detection-vs-balancing-masking]] Status Log · 데이터셋이면 entity |
   | ④ 실험 아이디어 | 제안 실험이 우리 질문의 어느 축을 재는가 · 참값을 아는 합성 곡선으로 할 수 있는가 | 해당 도구 entity 의 "제안 실험 (후보 · 미착수)" 절 |

4. **1차 대조:** 의존성 축은 릴리스 노트 · PR 원문으로 확인한다. 브리핑 문장만 옮기지 않는다. 확인 못 한 것은
   "열린 물음" 으로 적는다.
5. **등록:** 새 페이지는 `index.md` · 모든 브리핑은 `log.md` 에 `## [YYYY-MM-DD] ingest | GitHub 연구 브리핑` 한 항목.
6. **승인된 검증 실험의 기록:** 스크립트 · 실행 로그 · 출력 원문을 `wiki/raw/repositories/YYYY-MM-DD-<slug>.md` 에 그대로
   임베드하고 (큰 결과 JSON 은 같은 이름 `.results.json` 으로 옆에 — lint 는 raw `*.md` 만 본다), **해석은 entity 와 질문 카드에만**.
   첫 두 건: `raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md` · `raw/repositories/2026-10-01-pyprobe-dma-on-synthetic-truth.md`.
7. `python3 wiki/tools/lint.py` 0 errors.

## 하지 않는 것 (하드룰)

- **브리핑만으로 RUN_SCOPE (`src/ tools/ configs/ scripts/ run.sh requirements*.txt`) 를 고치지 않는다.** 버전 상한 하나도
  source_digest 를 바꾼다 (CLAUDE.md 하드룰 3) → 게이트 라운드의 사용자 승인 범위로만.
- **운영 환경에 설치하지 않는다.** 시험해 볼 도구 · 버전은 버리는 별도 가상환경에서, 저장소 산출물 밖에서만 (86차
  §6-b 교훈 — production 진입점 탐침이 운영 등록부에 기록을 남겼다).
- 제안 실험은 **후보**로만 적는다. 착수는 사용자 승인 뒤.
- 브리핑 숫자 · 주장을 위키 정본처럼 인용하지 않는다 (CLAUDE.md 하드룰 4 — 정본은 artifact + `RESULTS*.md`).
- raw 본문을 **unquoted shell heredoc 으로 쓰지 않는다** — 본문의 백틱이 명령으로 실행된다 (2026-09-30 README · 2026-10-01 raw 기록, 두 번 실측 · 저장소 피해 0). `Write` 도구로 쓴다.

## 관련
- [[pybamm]]
- [[pyprobe]]
- [[fitting-degeneracy]]
- [[isc-detection-vs-balancing-masking]]
