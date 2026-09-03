# CHANGELOG

## [0.1.2-dev] — 2026-09-04 (진행 중)
### Changed — 연구 프로필을 '추측'에서 '브랜치가 채우는 슬롯'으로
- `config/research_profile.md` 를 **STUB**으로 초기화. Cowork(클라우드)가 추측으로 쓴 연구 내용 전부 제거.
  이 파일은 두 브랜치(`claude/friendly-meitner-lldvar`, `claude/stoic-knuth-NObVQ`)를 읽은 Claude Code가 채운다.
- 사용자 정정 반영: 연구 축은 **DFT/MLIP** 과 **DEM/MPM/voxelization** 두 개이며 **서로 별개**.
  "DFT→MLIP→DEM→FEM 멀티스케일 파이프라인"이라는 서술을 모든 프롬프트·스킬·문서에서 제거.
- `prompts/deep_analysis.md`, Hermes SKILL.md, `paper-analyst` 서브에이전트, Cowork NOON 프롬프트에서
  연구자 정체 서술을 삭제하고 "프로필이 유일한 근거, 비어 있으면 연결점을 지어내지 말 것"으로 대체.
- 클라우드 작업은 repo를 못 읽으므로 메모리 `/areas/research-profile.md` 를 프로필 소스로 참조하도록 변경.

## [0.1.1] — 2026-09-04
### Changed
- 키워드 `anode-less assb` 추적 중단(사용자 요청). `config/agent.yaml`에서 `active: false` — 기존 노트 2편은 아카이브로 보존, 새 alert는 `rejected("키워드 추적 중단")`
- triage: 비활성 키워드에만 잡힌 논문은 자동 rejected (`TriageConfig.active_keywords`)
- Cowork 클라우드 작업 2개 등록(NOON 12:00 / MORNING 09:00 KST) — `cowork/README.md`
- 첫 디제스트(2026-09-04) Cowork Gmail로 발송·DB 기록

## [0.1.0] — 2026-09-04 (prototype)
### Added
- `ra` CLI: status / ingest / triage / analyze / vault / litdb / digest / noon / morning / sync / handoff / schedule
- Google Scholar alert 파서 (HTML `gse_alrt_title` + text fallback, `scholar_url` unwrap, DOI 추출) + fixture 테스트
- IMAP 수집(Gmail 앱 비밀번호), 수동/bootstrap JSON 드롭 폴더
- Crossref/OpenAlex/Semantic Scholar 메타·초록 보강 (로컬 전용, 실패 시 무시)
- 저널 IF 테이블(JCR 2024 근사값, 80여 종) + 정규화 매칭 + 프리프린트 처리
- Triage: 규칙 기반 관련도(3축 core/system/property 가중치) + LLM 재평가 병합, IF-우선 priority, Tier A/B/C
- 심층 분석 계약(`prompts/deep_analysis.md` JSON 스키마) + 큐 프로토콜(`data/analysis/pending`) + 검증/적용(tier 재계산)
- LLM 백엔드: anthropic / claude-cli / hermes(큐) / none
- SQLite DB(papers·alerts·digests·runs) + JSONL 미러, idempotent upsert(DOI/제목 병합)
- Obsidian vault 렌더: 논문 노트(frontmatter·callout·wikilink), 키워드 MOC, 홈 MOC(dataview), 디제스트
- 디제스트 결정적 렌더(Tier별 깊이, 오늘의 한 줄, References) + SMTP 발송(md→html, .md 첨부)
- 클라우드↔로컬 릴레이 `ra-handoff/1` (self-mail JSON 첨부, `ra sync` 병합)
- litdb 내보내기 (file: JSONL/SQLite 병합 · cli: `litdb add DOI`)
- Hermes 스킬 `paper-agent`(SKILL.md, scripts, references) + cron 등록 가이드
- Claude Code: CLAUDE.md, `/paper-noon` `/paper-morning` `/paper-sync`, `paper-analyst` 서브에이전트
- Cowork 예약 작업 프롬프트(noon/morning) 사본 (`cowork/`)
- 문서: README, ARCHITECTURE, SETUP_CLAUDE_CODE, SETUP_HERMES
- Bootstrap: 6편(Nature Commun. ×3, Nature, Adv. Mater., Front. Chem.) 수집·분석·디제스트 생성

### Known limitations
- 샌드박스에서는 출판사 API/페이지 접근이 제한돼 일부 논문이 title/snippet 근거로 분석됨 → 로컬 재분석 필요
- litdb `field_map`은 실제 브랜치 스키마 확인 전 기본값
- `ra quick`(alert 즉시 인사이트)은 미구현(v0.2)
