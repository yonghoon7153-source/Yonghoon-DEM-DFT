# Wiki Log

> 모든 위키 행동의 시간순 기록.  Append-only.
> 형식: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, verify, archive

## [2026-08-11] create | Wiki 초기화 (llm-wiki-kit v1.7 개조)
- Karpathy LLM-wiki 패턴 / 구요한 llm-wiki-kit v1.7 을 이 리포 규약으로 재구현.
- 개조: raw 층 = 리포 기존 증거층 재사용 · 논문 = litdb 정본 소관 (Paper Ingest
  Mode 폐기) · model/effort 폐기 → author + 모델-ID lint 오류화 · anchored(§F1)/
  scope(등급 A/B) 축 추가 · single-source+high 오류 상향 · 도구 3종 재작성
  (lint 15 / new_page 9 / status 4 selftest).
- 상세 개조표: entities/llm-wiki-kit-origin.md

## [2026-08-11] create | 시드 20페이지 + 미이관 코퍼스 분류표
- concepts 6 (frame4 · frame5 · ese-softening · quasistatic-gate · dh-collapse · sr01-stamp)
- entities 6 (dem-webapp · mpm-kit · se-curve-kits · litdb-canon · findings-ledger · kit-origin)
- comparisons 1 (network-vs-voxel-sigma) · syntheses 1 (dem-transport-mpm-mechanics)
- questions 3 (sr01-delta-sigma-sign[active] · dh-288-equalization[active] · anchor-waitlist[open])
- guides 3 (kit-run-protocol · adversarial-review-protocol · litdb-canon-procedure)
- index.md 에 docs/ 24편 분류표 (이관 백로그) 포함.

## [2026-08-11] update | 작업 규율 3줄 채택 (ponytail·superpowers) + 컨텍스트 예산 도구
- 외부 3 repo(ponytail/caveman/superpowers) 검토 → 플러그인 설치가 아니라 **우리
  실측 실패 유형에 꽂히는 것만** 채택.  caveman 산문 압축은 **기각** (한정어가 먼저
  깎여 우리 가치를 파괴) — 단 "메모리 파일 압축" 아이디어만 발췌 형태로 수용.
- `scripts/context_budget.py` (selftest 18/18): CLAUDE.md 섹션별 토큰 예산 + 닫힌
  이력 발췌.  제약 **문단**을 원문 그대로 보존하고 유실되면 거부, 절감 0 이하여도 거부.
- 첫 적용: σ_e Stage 21(자체 SUPERSEDED 선언본) 전문 → docs/sigma_e_stage21_history.md.
  CLAUDE.md 44,127 → 41,317 tok (−6.4%), 제약 3문단 유실 0, 섹션 42개 불변.
- guides/adversarial-review-protocol 에 "재현 테스트 먼저" + "만들기 전 사다리" 추가.
