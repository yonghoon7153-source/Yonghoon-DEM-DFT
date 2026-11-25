---
title: LLM 위키 규율 채택 기록 — Karpathy 패턴(llm-wiki-kit 260730)의 이 repo 번안
date: 2026-08-11
updated: 2026-08-11
tags: [kb, wiki, methodology, adoption, schema]
status: 확정
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-mixed
---

## 출처와 결정 방식

입력 3종 — 강의 전사(구요한, LLM 위키 구축), 키트 `llm-wiki-kit_260730`
(SCHEMA/CLAUDE/lint.py/ingest), Karpathy 원 패턴(전사 경유). 이것을 **이미 199개
md 가 살아 있는 kb** 에 얹되, 소급 재작성 없이 **forward-only** 로 채택했다.
규칙 원본은 kb/SCHEMA.md, 집행은 tools/kb_wiki.py (lint|index|new).

한계 1줄: 이 채택안 자체가 아직 운용 1일차다 — 규칙이 부담이 되면 SCHEMA 를
고치는 게 맞지, 문서 작성을 피하는 쪽으로 새면 안 된다.

## 채택 (kit 그대로)

| 항목 | 내용 |
|---|---|
| 3층 구조 | 불변 원본(runs/·PDF) / 위키(해석) / 규칙 — 우리는 여기에 **숫자 정본(db/)** 층이 이미 있어 4층으로 읽힘 |
| 품질 3축 직교 | `confidence`(증거 강도) ⊥ `verificationStatus`(대조 검증) ⊥ `explored`(사람이 읽었나) |
| explored 인간 전용 | 에이전트는 절대 true 로 못 바꾼다 |
| evidenceScope 가 confidence 상한 | single-source ⇒ high 금지 (lint 경고) |
| 문서 3분법 | 위키 / research-question(kb/questions/) / synthesis(kb/syntheses/) |
| Update Policy | 충돌 시 양쪽 기록·덮어쓰기 금지·disputed 강등 — 우리 superseded/retracted 관행과 동형 |
| 반론 보존 | synthesis 의 Counter-arguments 절은 삭제 금지 |

## 번안 (우리 환경에 맞게 변형)

| kit | 우리 | 사유 |
|---|---|---|
| `[[wikilink]]` | **repo-상대경로 인용** + lint 존재 검사 | 경로 인용이 이미 이 repo 의 링크 문화 — living reference 규칙과 합침 |
| model 필드 (작성 모델 기록) | `authoredBy: agent \| human` | 모델 ID 를 repo 산출물에 남기지 않는 세션 규율 — 사람/에이전트 구분만 남기면 충분 |
| verified 단일 축 | `verifiedBy: codex \| self \| both \| human` | Codex 교차검증 + 자체 적대 리뷰라는 이중 채널이 이미 있음 |
| verificationStatus 3값 | + **retracted** | 오늘 §11 BVSE 철회처럼 "본문 보존 + 반증 병기" 상태가 실재함 |
| 수동 index | **생성 index** (`python3 tools/kb_wiki.py index`) | 199개 소급을 손으로 못 함 — freshness 는 lint 가 검사 |
| Paper Ingest 파이프라인 | litdb 로 위임 | .claude/agents/litdb-curator.md 가 이미 그 역할 (litdb/INDEX.md) |

## 기각

| kit | 기각 사유 |
|---|---|
| log.md (작업 로그 파일) | git 이 로그다 — 커밋 prefix 관행(kb:/db:/sei:)이 이미 세밀함 |
| 폴더 재구성 (raw/wiki 분리) | runs/·db/ 가 이미 그 분리를 하고 있음 — 이동은 경로 인용 전부를 깨뜨림 |
| raw/ 레이어 신설 | 위와 동일 — 불변 원본은 runs/ 와 repo 밖 PDF 로 이미 존재 |
| mothership/satellite 위키 분리 | 단일 repo — 대신 living-reference(경로 인용) 규칙으로 흡수 |
| 프론트매터 전면 소급 | 199개 재작성은 검증 불가능한 대량 편집 — forward-only 로 대체 |

## 씨앗 카드 3장 (패턴 증명)

- kb/questions/lpsocl_low_beta_mechanism.md — 저β 기구 (A 케이지 / B sub-diffusion / C 느린 전이)
- kb/questions/sdcp_site_preference.md — LiNiO₂(104) Li vs Ni 자리
- kb/syntheses/xu2026_li_nd_rebuttal.md — Li–Nd alloy 서사 반박 방어

세 장 모두 오늘 실제로 살아 있는 질문/논지다 — 규칙 시연용 가짜가 아니다.

## 운용

새 문서: `python3 tools/kb_wiki.py new <dir> <slug>` → 마무리: `index` 재생성 +
`lint` 0 errors. 상세 규칙과 프론트매터 스펙은 kb/SCHEMA.md 가 정본이다.
