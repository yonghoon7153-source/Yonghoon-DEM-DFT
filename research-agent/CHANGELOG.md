# CHANGELOG

## [0.1.3] — 2026-09-04 · 병합 (Claude Code 측)
Cowork v0.1.3 tarball 을 브랜치 상태와 병합했다. 회신문 §5 의 정본 지정을 그대로 따랐다.
- Cowork 정본으로 교체: `cli.py`(dry-run 게이트) · `vault.py`(write_digest 방어 + `_scooping_block`) ·
  `digest.py`(경보 렌더) · `tests/test_dryrun_safety.py` · `VERSION`/`pyproject.toml`/`__init__.py` ·
  `prompts/deep_analysis.md` · `templates/paper_note.md` · `hermes/.../deep_analysis_schema.md` · `cowork/README.md`
- **덮지 않음**(브랜치가 정본): `exporters/litdb.py`(markdown 어댑터) · `config/research_profile.md`(482줄) ·
  `config/agent.yaml`(`litdb.mode: markdown`) · `tests/test_litdb_markdown.py` · `tests/test_triage_db.py` ·
  `data/` · `vault/`(복원한 2026-09-04 디제스트 164줄)
- `triage.py` **머지** — 이쪽 캠페인 용어를 기준으로, Cowork 표에서 빠진 것을 보탰다:
  · 축 A `MPM`·`Taichi`·`voxel`·`Kirchhoff`·`Bruggeman`·`constriction`·`Holm` (MPM 은 그 브랜치 90일 최다 주제인데 없었다)
  · **축 C 한 줄 신설** — `EIS`·`symmetric cell`·`Li-In`·`ASR`·`areal capacity` (이쪽 표에 통째로 없었다)
  · 축 A 물성 — 배위수·force chain·fabric tensor·Von Mises·유효전도도 / 감점에 `CALPHAD`·`potassium-ion`·`BMS`
  실측: 축A 0.950 · 축B 0.625 · 축C 0.800 · 무관 0.000
- 테스트 **24 passed** (이쪽 18 + Cowork 6) — 회신문 §5 의 예측치와 일치


## [0.1.3] — 2026-09-04
### Fixed — P1 데이터 손실 (Claude Code 보고, 실측 피해 발생)
- **`ra morning --dry-run` 이 dry-run 이 아니었다.** `args.dry_run` 이 메일 발송만 막고
  `_vault_sync`·`_git_commit` 은 게이트 밖에 있었다. 디제스트 창(36 h)이 지나 재생성이 0편을 내자
  그 빈 결과가 기존 파일을 덮었고, 2026-09-04 디제스트가 164줄 → 22줄로 소실됐다(Claude Code 가 tarball 에서 복원).
  → dry-run 이면 **메일·vault·git 전부** 건너뛴다.
- `cmd_noon` 에 `--dry-run` 신설 (이전엔 아예 없어 커밋을 막을 방법이 없었다).
- **`Vault.write_digest` 가 더 적은 편수로 기존 디제스트를 덮지 않는다.** frontmatter 의 `n_papers` 를
  비교해 새 결과가 더 적으면 쓰지 않고 이유를 로그로 남긴다. `--force` 로만 덮어쓸 수 있고,
  덮어쓸 때도 `vault/Digests/.backup/<date>.<타임스탬프>.md` 로 원본을 남긴다.
  (게이트 하나만으로는 부족하다 — 둘 다 있어야 같은 사고가 재발하지 않는다.)
- 회귀 테스트 `tests/test_dryrun_safety.py` 6건 — 사고 메커니즘 자체(0편이 5편을 덮는 것)와
  dry-run 부작용 차단을 각각 검증. 총 14 passed.
### Added
- `ra sync` 가 병합 후 **분석이 비어 있는 `triaged` 논문을 자동으로 큐에 넣는다.**
  클라우드가 초록 수준까지만 본 논문을 로컬(교내망·PDF)에서 `paper-analyst` 로 이어받는 경로.

## [0.1.2-dev] — 2026-09-04 (진행 중)
### Added — 브랜치 판정 반영 (Claude Code 2차 보고)
- `config/research_profile.md` **FILLED** — 두 브랜치 전수 조사 결과로 채움. 축이 **셋**임이 확인됨:
  A(DEM/MPM/voxelization, `stoic-knuth-NObVQ` 2652커밋) · B(DFT/MLIP, `friendly-meitner-lldvar`) · C(실험 협업, 이종원 그룹)
- 분석 스키마: `connection_to_my_work.anode_free` → **`.experimental`**(축 C), **`scooping_alert{hit,target,why}`** 신설
- 디제스트·노트에 **선점 경보** 렌더링 — 경보 논문은 Tier와 무관하게 최상단
- `triage.py` 용어 가중치를 세 축 기준으로 재작성 (MPM·Taichi·voxel·Kirchhoff·Holm·LOBSTER·ICOHP·BVSE·EIS·Li-In 등 추가)
- Cowork 트리거 2개를 메모리 `/areas/research-profile.md` 우선 참조로 교체 + 경보·비판 체크리스트 주입
### Fixed — Cowork 추측 오류 3건 (브랜치가 정정)
- "DFT→MLIP→DEM→FEM 단일 파이프라인" → 축은 별개 (사용자 명시 금지 사항)
- "MPM/voxelization은 문헌 단계" → **production**, 최근 90일 최다 주제(283회)
- "두 litdb 통합 여부 미결" → 2026-07-16 결정 완료. 정본은 `friendly-meitner-lldvar/litdb/`(208장), `stoic-knuth` 것(64장)은 **동결**
### Changed
- `sources.scholar_email.enabled: false` — alert 수집은 클라우드 전담(중복 방지). 같은 IMAP 자격증명은 `ra sync`의 handoff 병합에만 사용
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
