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

## [2026-08-11] create | 컨텍스트 계기 자동화 (실측 usage 기반)
- `scripts/context_meter.py` (selftest 11/11) + `.claude/hooks/context-meter.sh`
  (UserPromptSubmit).  트랜스크립트 JSONL 의 `message.usage` 실측으로 점유율 계산 —
  input + cache_creation + cache_read (★ output 은 이중계산이라 제외).
- 46 MB 트랜스크립트를 **꼬리 512 KB 만** 읽어 39 ms (매 프롬프트 부담 없음).
  꼬리에 usage 가 없으면 창을 2배씩 키워 재시도 (긴 도구-출력 한 줄 대응).
- 임계 초과 시에만 한 줄 출력, 평소 조용.  자동 compact 는 **하지 않는다** — 압축은
  한정어를 깎으므로(caveman 기각과 같은 논리) 판단은 사람이 한다.

## [2026-08-11] create | context-compaction-policy — 자동압축 금지 + 계기 3가드
사용자 보고: 다른 브랜치에서 `autoCompactWindow: 100000` 이 압축을 계속 돌려 대화가 망가짐.
이 브랜치엔 그 설정이 **없음**(확인) — 훅은 print 만 한다.  다만 같은 사고의 나머지 마디를
계기 자체에서 발견해 고쳤다:
- 가드 ① 압축 직후 스테일 읽기 (실측: 압축 직후 572,191 = preTokens 573,306 을 읽고 경고).
- 가드 ② 임계 초과 상태에서 매 턴 잔소리 → 이미 경고했고 10 %p 미만 상승이면 침묵.
- 가드 ③ 창 단조 — 압축으로 양이 줄면 창도 내려잡혀 **17.0 % 를 81.4 % 로** 부풀렸다.
  peak = 꼬리 ∪ compactMetadata.preTokens ∪ 사이드카 `<transcript>.ctxpeak`.
  ⚠ 정규식 줄-합산은 틀린다(실측 1,933,526 > 1 M) → 후보 줄만 구조 파싱 (8 MB/86 ms, 세션 1회).
selftest 11→23.  실트랜스크립트 검증: 170,145/1,000,000 = 17.0 %, 훅 침묵.

## [2026-08-12] update | sr01-delta-sigma-sign — ★해결: 점 스탬프가 σ_e 를 ×35.8 과소평가
kit_ps_7_3 두 팔 GPU 완주.  σ_e 0.005122 → 0.1833 S/cm (×35.79) · 소산 share VGCF 4 % → 95 %
(AM_S/AM_P 39/57 → 3/3) · σ_ion −7.4 % · κ +2.4 %.  H1 확정, H2·H3 기각.
⚠ 1 킷 1 베드 · rate-오염 베드라 relative-only · 60 °C.  confidence 는 lint 규칙대로 medium
(single-source + high 금지).
★ 덤: 같은 arm A 를 CPU/GPU 로 각각 돌아 backend 무해성이 **측정**됐다 (인쇄 자릿수까지 동일,
가속 11.2×·23.9×).
