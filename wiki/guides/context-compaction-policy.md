---
title: 컨텍스트 압축 정책 — 계기는 알리기만, 자동압축은 금지
created: 2026-08-11
updated: 2026-08-11
type: guide
tags: [workflow, tooling]
sources: [scripts/context_meter.py, .claude/hooks/context-meter.sh, .claude/settings.json, scripts/context_budget.py, docs/session_20260811_progress.md]
confidence: high
explored: false
verificationStatus: unverified
author: both
claimType: prescriptive
evidenceScope: multi-source-primary
anchored: anchored
scope: absolute
---

# 컨텍스트 압축 정책

## 규칙 (한 줄)
**50 % 에서 알리고, 압축은 사람이 시킨다.**  `.claude/settings.json` 에
`autoCompactWindow` 를 **넣지 않는다**.

## 왜 — 실사고 2건 (같은 날)
1. **자동압축 폭주** (다른 브랜치, 사용자 보고).  `autoCompactWindow: 100000` 을 걸었더니
   압축이 계속 돌아 대화가 못 쓰게 됐다 ("완전 구더기네").  → 설정 자체를 금지.
2. **스테일 읽기** (이 브랜치, 계기 자체의 결함).  압축 **직후** 훅이 `572,191` 을 읽고
   "57.2 % 초과 — /compact 권장" 을 찍었다.  트랜스크립트 꼬리의 마지막 usage 가 아직
   **압축 前** 값이었기 때문 (`compactMetadata.preTokens 573,306` 과 일치).
   ⇒ ①과 ②를 합치면 **압축 → 스테일 → 압축** 무한루프다.  두 사고는 같은 사고의 두 마디.

## 계기의 3 가드 (`scripts/context_meter.py`, selftest 23/23)
| # | 가드 | 무엇을 막나 |
|---|---|---|
| ① | 압축 경계가 마지막 usage **뒤**면 침묵 | 압축 직후 재-압축 권고 (루프의 마디) |
| ② | 마지막 압축 이후 이미 경고했고 `REWARN_STEP`(10 %p) 넘게 안 올랐으면 침묵 | 매 프롬프트 잔소리 (그 자체가 컨텍스트를 먹는다) |
| ③ | 창은 **관측 최대치에 대해 단조** (꼬리 peak ∪ `preTokens` ∪ 사이드카 `<transcript>.ctxpeak`) | 백분율 **과대**보고 |

★ 가드 ③ 이 없으면 압축으로 양이 줄 때 창도 같이 내려잡혀 **부풀어 오른다** — 실측
`170,145 tok` 이 1 M 창의 **17.0 %** 인데 200 k 창으로 오인해 **81.4 %** 로 찍혔다.
압축을 재촉하는 방향의 오차라 셋 중 제일 위험하다.

⚠ **정규식 합산으로 peak 을 구하지 말 것.**  한 줄에 usage 객체가 여럿 실리는 줄이 있어
줄 단위로 더하면 창을 넘는 값이 나온다 (실측 **1,933,526 > 1 M**).  구조로 읽되 후보 줄만
파싱한다 — 8 MB 꼬리에서 795 줄만 파싱해 **86 ms**, 그 뒤엔 사이드카가 맡아 세션당 1회.

## 압축 前 절차 (한정어 보존)
압축은 공짜가 아니다 — 이 리포의 가치는 한정어("하한", "relative-only", "DO NOT
re-screen")에 있고 압축은 그것부터 깎는다 ([[llm-wiki-kit-origin]] 의 caveman 기각과
같은 논리).  그래서 **압축 전에 진행 중 판정·수치를 파일로 내린다** —
`docs/session_<YYYYMMDD>_progress.md` 가 그 자리다 (2026-08-11 실적).

## 토큰 레버 (실측, CLAUDE.md 는 레버가 아니다)
세션 누적 2.34 M tok 기준: CLAUDE.md **1.9 %** · Read 출력 **32 %**(PDF/이미지 9 건이
10 %) · Bash 입력 **19 %**(heredoc) · Bash 출력 **17 %**.  ⇒ 줄일 곳은 ⓐ PDF 는 텍스트
추출 먼저 ⓑ 긴 파이썬은 scratchpad 파일로 ⓒ 출력은 `| tail`·Grep 로 자르기.
전체 규율은 루트 `CLAUDE.md` §작업 규율 3줄 ③, 발췌 도구는 `scripts/context_budget.py`.

## 관련
- [[kit-run-protocol]] — 같은 계열의 "드립 없이 돌리는" 절차 규약
- [[llm-wiki-kit-origin]] — 요약 압축을 왜 거부하는지의 출처
