---
title: LLM Wiki Pattern
description: "Karpathy-style LLM wiki: immutable raw layer, compiled pages with YAML metadata, wikilink graph, mothership/satellite vaults"
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [wiki, tooling]
sources: [raw/transcripts/2026-08-11-llm-wiki-lecture-kist.md, raw/transcripts/kit-provenance-260730.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: definition
evidenceScope: multi-source-mixed
---

# LLM Wiki Pattern

에이전트가 컴파일러·사서 역할을 하는 로컬 지식 베이스 패턴 (Karpathy 의 LLM wiki
아이디어 → 커맨드스페이스 구요한의 Obsidian 구현·킷). 이 위키 자체가 그 인스턴스다.

## 핵심 아이디어 (강의에서)
- **왜 로컬에 모으는가**: 웹서치가 아니라, 내가 **관심을 표시한** 지식의 캡처가
  목적 — 사람의 관심(휴먼 바이어스)을 에이전트가 알게 하는 층. 스트레치드 골
  (조금 더 뻗으면 닿는 학습 목표)의 전진기지.
- **3-Layer**: raw 불변 원본(출처 명시) / 컴파일된 위키 페이지 / 규칙(SCHEMA).
- **frontmatter = progressive disclosure**: 에이전트는 메타데이터(빙산의 일각)만
  먼저 훑고 필요한 페이지만 연다. 컨텍스트 윈도우 절약의 구조적 해법.
- **wikilink 그래프**: 페이지 하나의 주소만 줘도 연결된 지식이 소시지처럼 딸려
  읽힌다. vault 밖은 경로 링크로.
- **mothership / satellite**: AI 가 쓴 지식과 내가 쓴 지식, 공용과 프로젝트
  전용을 vault 로 분리. 프로젝트는 entity 1페이지로 등록 (등록 절차:
  [[new-project-kickoff]]).
- **provenance**: 에이전트 작성 페이지에 model/effort 를 기록 — 어떤 모델이 쓴
  지식인지 추적. 수집 시 목적 게이트("왜 모으는가")를 물어 맥락을 남긴다.
- **검색**: 벡터 DB 없이도 렉시컬(BM25급) + 그래프 탐색으로 충분하다는 입장.
- 논문의 수치·정의를 verbatim 재사용해야 하면 opt-in [[paper-ingest-mode]].

## 이 모노레포에서의 적응
킷 원본 대비: repo root `wiki/` 하위 배치, `wiki-` 접두 커맨드, cross-vault
참조를 절대경로 대신 repo-root 상대경로로, 연구 파이프라인 code identity 와의
경계 명시. 상세는 `wiki/README.md`. 첫 satellite: [[degradation-degeneracy]].

## 한계
- 전사 원본이 유튜브 자동 자막이라 고유명사 오류가 많다 (예: "카파시" = Karpathy).
- ingest 는 토큰·시간 비용이 크다 — 강의도 "중요한 자료만 모으라"고 강조.
