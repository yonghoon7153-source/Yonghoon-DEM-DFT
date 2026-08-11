---
title: llm-wiki-kit — 이 위키의 출처 킷과 개조 내역
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: [wiki]
sources: [https://www.youtube.com/watch?v=MRTQwBFURJs, wiki/SCHEMA.md]
confidence: medium
explored: false
verificationStatus: unverified
author: agent
claimType: historical
evidenceScope: multi-source-mixed
anchored: n-a
scope: n-a
---

# llm-wiki-kit — 출처와 개조 내역

## 개요
이 위키는 Karpathy 의 LLM-wiki 아이디어를 구현한 구요한(CMD Space)
**llm-wiki-kit v1.7** (2026-08-11 KIST 강연에서 공개; 강연 영상 = sources URL,
킷 tar 는 사용자 업로드) 을 참고해, 이 리포 규약에 맞게 **재구현**한 것이다.
킷 코드 이식이 아니라 스키마·명령 개념을 가져와 도구는 새로 썼다 (전부 selftest 보유).

## 킷에서 가져온 것 / 바꾼 것
| | 킷 v1.7 | 우리 |
|---|---|---|
| 페이지 7타입·품질 3축·index/log·`[[위키링크]]` | ✓ | 유지 |
| raw/ 불변층 | 위키 내부 폴더 | **리포 기존 증거층** (docs/data·litdb·ledger·git) 재사용 |
| 논문 ingest (Paper Ingest Mode) | opt-in | **폐기** — 논문은 [[litdb-canon]] 소관 |
| model/effort provenance | frontmatter 기록 | **금지** (리포 모델-ID 규칙) → author 3값 + lint 오류화 |
| 품질축 | 3축 | +2축: anchored(§F1) · scope(등급 A/B) |
| single-source+high | 경고 | **오류** (greenfield 상향) |
| 도구 | lint/status/new-page | 재작성 + `--selftest` 3종 |

## 관련 페이지·경로
- 규칙 원본: wiki/SCHEMA.md · 원장 문화와의 접점: [[findings-ledger]]
- 같은 논리(요약 압축 거부)의 운영판: [[context-compaction-policy]]
