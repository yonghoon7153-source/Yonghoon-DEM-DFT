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
