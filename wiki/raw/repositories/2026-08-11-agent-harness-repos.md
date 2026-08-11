---
source_url: https://github.com/DietrichGebert/ponytail · https://github.com/juliusbrussee/caveman · https://github.com/obra/superpowers
ingested: 2026-08-11
sha256: 3a570a52c5f556107f1783dab5e3536dc7d6a503f5315afa217ceadb4d888d74
---

# 수집 목적: 이 모노레포의 에이전트 작업 규율(CLAUDE.md·커맨드)에 무엇을 채택/각색/기각할지 판단하기 위한 조사. 채택 결과는 concepts/agent-harness-patterns.md.

# 세 에이전트 하네스 저장소 — 조사 노트 (WebFetch 요약)

> **원문이 아니라 요약이다.** 2026-08-11 에 WebFetch 로 각 저장소의 README 를
> 읽고 받은 요약과 직접 인용을 기록한 것. 원문 전체는 아래 URL.

## 1. DietrichGebert/ponytail

목적: 에이전트를 최소·실용 코드 쪽으로 유도하는 플러그인.
"The best code is the code you never wrote."

decision ladder (원문 인용):
```
1. Does this need to exist? → no: skip it (YAGNI)
2. Already in this codebase? → reuse it, don't rewrite
3. Stdlib does it? → use it
4. Native platform feature? → use it
5. Installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that works
```
- 사다리는 **문제를 이해한 뒤** 적용. "Lazy about the solution, never about reading."
- 안전 carve-out (원문 인용): "trust-boundary validation, data-loss handling,
  security, and accessibility are never on the chopping block"
- 강도 모드: lite / full(기본) / ultra / off
- 커맨드: `/ponytail-review`(diff 의 과설계 후보를 우선순위로), `/ponytail-audit`
  (전체 스캔), `/ponytail-debt`(`ponytail:` 로 미뤄둔 것을 원장으로 수집)
- 벤치마크 주장: FastAPI+React 12개 기능 과제 중앙값 LOC ~54% 감소, 비용 ~20%
  감소, 실행 ~27% 단축, 안전성 100% 유지
- 구조: `skills/` `hooks/`(Node lifecycle 훅) + 에이전트별 rule 사본 + `benchmarks/`

## 2. juliusbrussee/caveman

목적: 에이전트의 **출력 토큰** 압축. 산문 응답 ~65% 감소 주장.
"Caveman no make brain smaller. Caveman make mouth smaller."

- 압축 대상은 **말하는 방식**이지 지식이 아니다. 코드·명령·에러 메시지는
  byte-identical 유지
- 정직한 한계 공개: 에이전틱 코딩 실행(도구 호출·diff 위주)에서는 절감이 ~8.5%
  로 떨어짐 (JetBrains 86 과제 측정). 입력·추론 토큰은 안 줄어듦
- 압축 레벨: lite / full / ultra / wenyan
- 세션 시작 훅으로 자동 활성, statusline 에 누적 절감 표시
- 텔레메트리 0, 전 처리 로컬

## 3. obra/superpowers

목적: 코딩 에이전트를 위한 **개발 방법론** 스킬 묶음. 바로 코딩에 뛰어들지 않고
"steps back and asks you what you're really trying to do."

스킬 목록: brainstorming · dispatching-parallel-agents · executing-plans ·
finishing-a-development-branch · receiving-code-review · requesting-code-review ·
subagent-driven-development · systematic-debugging · test-driven-development ·
using-git-worktrees · using-superpowers · verification-before-completion ·
writing-plans · writing-skills

test-driven-development (SKILL.md, frontmatter: name / description):
- RED: 최소 실패 테스트 먼저. "If you didn't watch the test fail, you don't know
  if it tests the right thing."
- 절대 금지: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST." 구현이 먼저
  나왔으면 **삭제**하고 다시 시작 — "Delete means delete." 참고용 보관·변형 금지
- 테스트가 즉시 통과하면: "Test passes? You're testing existing behavior. Fix test."

verification-before-completion:
- "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
- 게이트 절차: 주장을 증명할 명령 식별 → 새로 전체 실행 → 전체 출력과 exit code
  읽기 → 출력이 주장을 실제로 뒷받침하는지 확인 → 그제서야 주장
- 불충분한 근거: 이전 실행 결과, 부분 검사, 린터 통과, "should work", 에이전트의
  자기 성공 보고, 출력 없는 확신
- 금지 표현: "should" "probably" "seems" "looks good"

기타: 2단계 코드 리뷰(스펙 준수 → 품질), 병렬 subagent 개발, 세션 시작 훅으로
자동 활성.
