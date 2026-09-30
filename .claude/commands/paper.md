---
description: 논문 에이전트 — PDF(+SI)를 sha256 봉인 digest + 그림 크로핑 + compare: 블록으로 위키에 흡수하고 질문 카드에 근거를 라우팅한다
---

논문 에이전트(`.claude/agents/paper-curator.md`)를 실행한다. 대상: $ARGUMENTS
(비우면 `wiki/inbox/` 의 PDF/.docx 전부 — 먼저 목록을 보이고 어느 것을 할지 **한 번에** 묻는다.)

절차는 에이전트 파일의 Procedure 1–7 을 그대로 따른다. 요약:

1. **Read** — `.venv/bin/python` + pymupdf 로 텍스트 덤프(스크래치패드), SI .docx 는 stdlib 로 텍스트·이미지 추출.
2. **Extract** — Li2S ASSB 축: 셀 계·복합양극 조성·Li2S 출처·**혼합/합성 조건(장비·rpm·시간·BPR)**·첫 충전 활성화·용량(양단위)·탄소·음극·관측 도구·셀 개수.
3. **Crop + LOOK** — `extract_figures.py --slug <slug> --pdf … --clean`; SI 이미지는 `fig_S<n>.png` 로 `figures.json` 에 추가; 핵심 그림을 Read 한 뒤에 쓴다.
4. **Write digest** — `wiki/raw/papers/<slug>.md`: frontmatter(`compare:` 포함) · 수집 목적 · **공백표(G1…)** · 서지 · 한 문단 요약 · 절별 해체 · SI 대조 · 우리 접점 표 · 비판 · 가져갈 것 · 그림 판독 기록. `[인쇄]/[도표]/[해석]/[재현]` 4구분. 해시 먼저 → 한 번에 Write.
5. **Compile** — 열린 질문 카드 Evidence 라우팅(가설 번호), 개념 신설/갱신, index/log, `python3 wiki/tools/lint.py` 0 errors.
6. **Explain** — 사용자에게 상세히: 질문과 답 · 핵심 수치(양단위) · 그림별 · 방법 · 우리 reference cell/anode-free 접점 · 다음 실험 · 본/안 본 그림.
7. **Commit** `ingest(wiki): …` → push (루트 CLAUDE.md 하드룰 1 브랜치). PR 없음.

금지: raw 수정, 모델 식별자 기재, 단위 없는 비용량, 물음표로 채운 `compare:` 값, 검증 없는 "끝났다".
**여러 편을 병렬로 돌릴 때**: 각 에이전트에 `<scratchpad>/<slug>/` 전용 디렉토리를 쓰라고 지시한다 (2026-09-30 사고 — 공용 스크래치의 `body.md` 충돌로 digest 하나가 다른 논문 본문으로 봉인됐다). 그리고 `index.md`·`log.md`·컴파일·커밋은 **부모가** 한다 — 동시 편집 경합을 피한다.
세미나 논문이면 끝에 `/seminar <slug>` 를 제안한다.
