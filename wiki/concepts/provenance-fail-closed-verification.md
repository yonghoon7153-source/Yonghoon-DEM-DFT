---
title: Provenance & Fail-closed Verification
description: "Verification design principles distilled from 13 adversarial gate-review rounds"
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [provenance, design, gate-review]
sources: [raw/repositories/degradation-degeneracy-audit.md]
confidence: high
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# Provenance & Fail-closed Verification

[[degradation-degeneracy]] 의 13 라운드 적대적 [[gate-review-loop]] 에서 매 라운드
실측 반례로 증류된 재현성 설계 원칙. 인용 가능한(citation-grade) 계산 산출물을
만들려는 어떤 프로젝트에도 재사용할 수 있다.

## 원칙
1. **서명은 계산을 고정한다, 설정이 아니라.** 목적함수 순서·조건 ID 집합·optimizer
   정책·물리 기준점(완방상태)·실제 solver backend·읽은 바이트가 서명에 들어가야
   한다. 이름/설정만 서명하면 같은 이름의 다른 계산이 섞인다.
2. **검증은 자기신고가 아니라 외부 현실과 대조한다.** manifest 가 주장하는 값을
   믿지 말고 디스크를 재해시하고, 파생 숫자를 정본에서 재계산해 대조한다.
3. **보고서는 재계산 값을 렌더한다.** 저장 YAML 을 그대로 실으면 파생 변조·stale
   이 최종 문서에 도달한다.
4. **읽기는 봉인한 바이트로만.** 해시 시점과 읽기 시점 사이는 digest 비교로 못
   막는다 — content-addressed snapshot 을 뜨고 계산은 그것만 읽는다.
5. **fail-closed 기본.** 검증 불가능한 상태(필드 부재·recipe 없음·재검 불가 사유)는
   통과가 아니라 실패다. 단, 결정적으로 자기치유 가능한 것(stale 캐시)은 miss 로
   재계산하는 편이 안전할 수 있다.
6. **fixture 는 진실을 가린다.** validator 를 강화할 때마다 fixture 가 먼저 깨져야
   정상 — 깨지지 않으면 fixture 가 위조 통로였다는 뜻 (프로젝트에서 4회 이상 실측).
7. **신뢰 경계를 명시한다.** untracked 산출물의 값 변조 + 재봉인은 자기신고 seal
   로 원리적으로 구분 불가 — 진본성 anchor 는 커밋되는 digest (commit-time byte
   identity) 이고, 독립 재실행·수치 대조는 별개다.

## 작업 규율과의 연결
원칙 6(fixture 가 진실을 가린다)은 외부 하네스의 TDD RED-first 규칙과 같은 구조다
— 이 저장소에서는 `/finding` 절차로 강제한다. 원칙 2·3(자기신고 대신 외부 현실
대조)의 작업 버전이 "신선한 증거 없이 완료 선언 금지"다. 출처와 채택 근거는
[[agent-harness-patterns]].

## 한계
- 이 원칙들은 위조 방어가 아니라 **정상 실행의 회귀·혼입 검출**이 1차 목적이다.
  형식적으로 완전한 위조는 경계 밖(원칙 7).
- 비용: 서명 스키마가 자랄 때마다 기존 산출물이 fail-closed 로 무효화된다 —
  격자 재생성을 반복하게 만든 실제 비용을 감안하고 스키마를 미리 넓게 잡을 것.
