# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, verify, archive, delete

## [2026-07-30] create | Wiki initialized
- Scaffolded from llm-wiki harness (tools + commands + hooks + CI).
- Domain: 이 저장소의 도메인을 한 문장으로 적는다 (무엇에 관한 자료를 모아 무엇에 재사용하는가).

## [2026-07-30] create | Mothership 변환 + 킥오프 가이드
- SCHEMA/CLAUDE/AGENTS 에 Mothership 특칙 추가 (satellite entity 등록, living reference, transcripts).
- guides/new-project-kickoff.md 추가 — `<MOTHERSHIP>` placeholder, 배치 후 실제 경로로 치환.

## [2026-08-06] update | 하네스 v1.8~v1.10 채택 (원본 위키에서 전파)
- frontmatter: `model`/`effort` provenance + `claimType`/`evidenceScope` (single-source→confidence high 금지), 타입 2종 신설 (`questions/` research-question · `syntheses/` synthesis).
- Paper Ingest Mode opt-in 특칙 + guide [[paper-ingest-mode]] + raw changelog. SCHEMA/CLAUDE/AGENTS(parity)/tools/hook/ingest 커맨드/init-wiki.sh 갱신, lint 검사 12~15 추가.

## [2026-08-11] create | Yonghoon-DEM-DFT mothership 이식·적응
- llm-wiki-kit_260730 을 repo root `wiki/` 로 이식. 적응: `wiki-` 접두 커맨드(root `.claude/commands/`), hook 를 `wiki/tools/hooks/` + root settings.json 으로, cross-vault 참조를 repo-root 상대 경로로, 커밋 prefix `<action>(wiki):`, wiki-lint CI (`wiki/**` path filter). 근거: 강의 전사 + 킷 (아래 ingest).
- 연구 파이프라인 경계 명시: `wiki/` 는 degradation-degeneracy 의 code identity(`source_digest`) 밖 — 게이트 리뷰 대상 코드 불변.

## [2026-08-11] ingest | LLM Wiki 강의 (KIST, 커맨드스페이스 구요한)
- raw/transcripts/2026-08-11-llm-wiki-lecture-kist.md (유튜브 자동 전사, 수집 목적: 이 위키 구축의 근거). 컴파일: [[llm-wiki-pattern]].

## [2026-08-11] create | 프로젝트 지식 분류 — satellite 등록 + 개념/가이드/질문 카드
- raw/repositories/degradation-degeneracy-audit.md (기존 프로젝트 감사 스냅샷, HEAD c9970ebc).
- 페이지 5: [[degradation-degeneracy]](entity) · [[fitting-degeneracy]] · [[provenance-fail-closed-verification]] · [[gate-review-loop]] · [[22p-physics-or-degeneracy]](research-question, active).
- 원칙 준수: 수치·발견 상세는 위키로 복사하지 않음 (정본 = artifact·docs, living reference).

## [2026-08-11] ingest | 에이전트 하네스 3종 (ponytail · caveman · superpowers)
- raw/repositories/2026-08-11-agent-harness-repos.md (WebFetch 요약, 원문 아님 — sha256 봉인).
- 컴파일: [[agent-harness-patterns]] — 채택/각색/기각 판단표와 근거.

## [2026-08-11] create | 작업 규율 이식 — 루트 CLAUDE.md + 커맨드 4종
- 루트 `CLAUDE.md` 신설 (저장소 지도, 하드룰, 작업 규율 4항, RUN_SCOPE 경계).
- `.claude/commands/`: /finding(RED-first + fixture 감사) · /lean-review(사다리, 검증 carve-out) · /self-review(다각 렌즈) · /gate-request(기계용 밀도).
- 플러그인 통째 설치는 기각 — 전역 훅이 게이트 리뷰 중인 저장소 행동을 바꾼다.

## [2026-08-11] query | /lean-review 첫 실행 — 중복 후보 원장화
- env 결정축 비교가 baseline.py·halfcell.py 3곳 중복 + _ENV_KEYS 레이어링 어긋남 확인.
- **실행 보류**: 13차 리뷰가 c9970ebc 대상으로 열려 있어 source_digest 변경 금지. [[lean-review-backlog]] 에 원장화.

## [2026-08-20] lint | 브랜치 이름 drift 차단 + 죽은 study-path 검사 제거
- 브랜치 통독 중 발견: 위키 5개 파일(SCHEMA/CLAUDE/AGENTS/README/[[degradation-degeneracy]])과 위키 밖 3곳이 **이미 흡수된 브랜치**를 작업 브랜치로 지목하고 있었다. 브랜치 이름의 정본을 루트 `CLAUDE.md` 하드룰 1 하나로 모으고, 위키는 그것을 참조하게 바꿨다.
- `tools/lint.py` 검사 15 신설 — 위키 파일이 브랜치 이름을 하드코딩하면 error. `raw/` 면제(봉인 스냅샷), `.claude/`·`.github/` 경로는 오탐 안 함. 변이 3종으로 확인(주입 시 검출 / 경로 오탐 없음 / raw 면제).
- 킷의 study-path 커버리지 검사와 status 진도 바 제거 — `guides/llm-wiki-study-path.md` 가 없어 **한 번도 실행된 적이 없는** 검사였다. 조용히 통과하는 검사는 커버리지로 오독된다.

## [2026-08-20] update | 본 실행 결과를 satellite·질문 카드에 반영
- [[degradation-degeneracy]]: 13차 대기 → 19차 완료·본 실행 완료로 갱신. 결론 1 철회 / 2 한정 / 3 축소를 상태에 기록(수치는 옮기지 않음 — 정본은 artifact + docs/RESULTS*.md). 한계 절에 남아 있던 모집단 숫자 사본을 참조로 교체.
- [[22p-physics-or-degeneracy]]: 실행 후 Evidence 갱신 — dQ/dV 이점 근거는 **철회**(paired 정본에서 모든 noise 층에 걸쳐 열세), 좌표 원점·restart 예산 축을 새 근거로 추가. status 는 `active` 유지: 질문이 "물리인가"에서 "어떤 모델 정확도·최적화 예산에서 의미를 갖는가"로 좁혀졌다.
- [[lean-review-backlog]]: 보류 사유를 닫힌 13차 리뷰에서 진행 중인 민감도 스윕으로 갱신(영구 부채화 방지).
- 루트 `BRANCHES.md` 신설 — 38개 브랜치의 계열·흡수 관계 지도. degradation-degeneracy 는 갈라져 있지 않음을 실측으로 고정.
- 21차 게이트 리뷰 회답(문서 라운드): [[22p-physics-or-degeneracy]] 의 "모든 noise 층에서 열세" 를 `warm_start=False` protocol 조건부로 재정정 — warm 을 켜면 한 층에서 방향이 뒤집힌다. `wiki/tools/{status,lint}.py` 의 stdout 을 UTF-8 로 재구성(CP949 콘솔에서 status.py 가 죽던 것을 실측 후 수정). `BRANCHES.md` 의 `main` 고립 주장 정정 — shallow clone 산물이었고 full clone 에서는 37/37 브랜치의 공통 조상이다.

## [2026-09-03] ingest | 2026-09-02 BML 세미나 (김시원) — degradation mode ML 프레임워크
- raw 2건 봉인: `raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md` (PDF 15쪽 **페이지별 해체분석** — `[인쇄]`/`[도표]`/`[해석]` 3구분으로 원문 주장과 우리 판단을 분리), `raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md` (구술 메모 전문 + 전사 오인식 대조표 30여 항 + 슬라이드에 없고 구술에만 있는 7가지). 구술은 **09:15 에서 끊겨** p.12~15 가 녹음에 없다 — 그 한계를 파일 머리에 적었다.
- 컴파일 2건: [[pvs-sev-degradation-mode-features]] (concept — PVS/SEV 정의·물리 귀속·모드별 부호표), [[pvs-sev-lli-lampe-separability]] (research-question, status open).
- 발견의 요지: 두 feature 의 **모드별 부호 패턴이 동일**하다 ({LLI, LAM_PE} ↑ vs {LAM_NE} ↓). 부호가 같다고 벡터가 평행한 것은 아니므로 확정은 아니지만, 확정되면 LLI↔LAM_PE 방향에 새 정보가 없다는 뜻이 된다. 원문 p.13 permutation importance 에서 PVS 가 네 target 모두 최하위권이고 LAM_PE 예측을 SOH+프로토콜 식별자가 지배하는 것이 같은 방향의 정황.
- [[22p-physics-or-degeneracy]] 에 분기 기록 추가 (status 는 `active` 유지 — 새 근거 없이 갈라진 질문만 등록).
- 이 커밋은 `wiki/` 만 건드리므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다 (진행 중인 57차 게이트 대상 커밋과 무관).
