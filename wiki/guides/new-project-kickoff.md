---
title: New Project Kickoff
created: 2026-07-30
updated: 2026-08-11
type: guide
tags: [satellite, wiki]
sources: [raw/transcripts/kit-provenance-260730.md]
confidence: high
explored: false
verificationStatus: unverified
---

# New Project Kickoff

## 용도
새 프로젝트를 시작할 때 그 프로젝트의 Claude 세션에 붙여넣는 킥오프 프롬프트. 폴더 세팅부터 mothership 위키 satellite 등록까지 한 번에.

> **이 모노레포 적응**: 원본 킷의 `<MOTHERSHIP>` 절대 경로 대신 **repo-root 상대 경로 `wiki`** 를 쓴다.
> 위키와 satellite 이 같은 git repo 라 clone 위치(컨테이너·V100·Windows)와 무관하게 통한다.

새 프로젝트 세션에서 이 가이드를 쓰게 하려면 한 줄이면 된다:
`wiki/guides/new-project-kickoff.md 읽고 그대로 세팅해줘. 슬러그/경로/목표/환경: ...`

## 킥오프 프롬프트 (복사해서 [ ] 채우고 붙여넣기)

```
새 프로젝트 시작. 아래대로 세팅해줘.

[프로젝트 정보]
- 이름/슬러그: [예: paper-graph]
- 경로: [예: ~/projects/<이름>_YYMMDD]
- 목표 (1~3줄): [ ]
- 스택/환경: [예: conda env 신설 py3.12 / node / 없음]

[세팅 순서]
1. 폴더 + git init + README.md (목표·구조·실행법)
2. 전용 환경 필요 시 생성 (conda env 이름 = 프로젝트명, environment.yml 기록,
   셸 기본 env에 설치 금지 — 절대경로 python 사용)
3. CLAUDE.md 작성 — 아래 섹션 반드시 포함:

## LLM Wiki 연결 (mothership)
이 프로젝트는 wiki 의 satellite다. 의미 있는 진행(설계 결정,
마일스톤, 실측 결과)이 생기면 세션 마무리에 mothership을 갱신한다:
entities/<슬러그>.md 상태 append + log.md 기록 + python3 tools/lint.py
0 errors + git commit (prefix: ingest/update/create/lint/verify).
raw/ 는 불변, explored 는 사람만 바꾼다.
코드·데이터는 위키로 복사 금지 — living reference (절대경로 참조).

4. Mothership 등록 (wiki):
   - wiki/SCHEMA.md 먼저 읽기 (특히 Mothership 특칙)
   - tools/new-page.py entity <슬러그> → 개요·위치(절대경로)·목표·계획·상태
     채우기, [[wikilink]] 2개 이상
   - index.md 등록 + log.md append + lint 0 errors + commit (create:)
5. 이 킥오프 대화의 설계 결정은 mothership
   raw/transcripts/<슬러그>-design-session-YYMMDD.md 로 기록
```

## 이미 진행 중인 프로젝트를 등록할 때
위 프롬프트에서 1~2번을 빼고, 4번 앞에 "이 저장소를 감사해서 mothership `raw/repositories/<슬러그>-audit.md` 로 저장" 추가.

## 한계·불확실성
- 프로젝트 세션의 Claude 는 다른 프로젝트의 메모리를 못 본다 — 이 프롬프트가 자기완결이어야 하는 이유. 규칙이 바뀌면 이 페이지를 갱신할 것.
- 첫 satellite entity 가 생기면 이 페이지와 상호 `[[wikilink]]` 를 걸어 orphan 을 해소한다.

## 관련
- [[paper-ingest-mode]] — 프로젝트가 특정 논문의 수치·정의를 반복 참조하면 제안하는 opt-in 논문 ingest 모드
- [[degradation-degeneracy]] — 이 절차로 등록된 첫 satellite (기존 프로젝트 등록 경로 사용)
- [[llm-wiki-pattern]] — 이 위키가 구현하는 패턴 자체
