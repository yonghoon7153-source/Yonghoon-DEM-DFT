# Fair-Chem / UMA knowledge base

이 폴더는 FAIR Chemistry 공식 문서와 공식 GitHub `main`을 한 시점에 고정해 만든 사람용 지식 뷰야. 원문 복사본이 아니라, 나중에 논문·세미나·webapp에서 다시 쓸 수 있도록 출처와 적용 범위를 정리한 색인이야.

## 한눈에 보는 동결본

- Official source commit: `93a03d656806a55f08c7cd126cfaa40ef18181fb`
- Source time: `2026-08-20T23:19:48Z`
- Live audit: `2026-08-21`
- Tracked files: 944
- Tracked Markdown pages: 66
- MyST navigation pages: 64
- Live HTTP 200 pages: 64
- Source-only orphan pages: 2
- Pages rendered with an execution error: 3
- Python package manifests: 13
- Code-registered pretrained checkpoints: 13
- Official paper-index entries: 42

정확한 수치와 해시는 [snapshot.json](../../db/knowledge/fairchem/snapshot.json)이 정본이야.

## 읽는 순서

1. [00_site_map.md](00_site_map.md) — 공식 사이트 구조와 live QA
2. [01_models_and_tasks.md](01_models_and_tasks.md) — 모델, task, DFT identity
3. [02_datasets_and_domains.md](02_datasets_and_domains.md) — 데이터셋과 응용 도메인
4. [03_workflows_and_code.md](03_workflows_and_code.md) — 공식 코드가 제공하는 기술
5. [04_lpscl_research_crosswalk.md](04_lpscl_research_crosswalk.md) — 우리 LPSCl 연구에 어디까지 쓸지
6. [05_papers_and_insight_workflow.md](05_papers_and_insight_workflow.md) — 논문 추가·인사이트 축적 방법
7. [06_claims_caveats_and_citations.md](06_claims_caveats_and_citations.md) — 인용 전 확인할 함정
8. [07_webapp_handoff_for_claude.md](07_webapp_handoff_for_claude.md) — Claude용 webapp 설계 인계
9. [08_update_playbook.md](08_update_playbook.md) — 다음 공식 버전 갱신 절차
10. [09_source_coverage.md](09_source_coverage.md) — “빠짐없이”의 범위와 제외 범위

## Machine-readable DB

`db/knowledge/fairchem/` 아래 파일은 webapp과 후속 자동화를 위한 원장이야.

- `repo_files.{json,csv}` — 공식 commit의 944개 파일 경로·크기·SHA256
- `site_pages.{json,csv}` — 66개 Markdown의 제목·heading·링크·live 상태
- `live_link_audit.json` — broken link, sitemap, rendered error 감사
- `release_observations.json` — package tag와 `main`/release 경계
- `license_observations.json` — software/model/dataset license 범위
- `packages.json` — 13개 `pyproject.toml`
- `models.json` — 코드 registry의 13개 checkpoint name
- `tasks.json` — 7개 UMA task와 방법 범위
- `datasets.json` — 주요 13개 dataset
- `technologies.json` — 23개 코드/워크플로 기술
- `papers.json` — 공식 paper index 42개
- `claims.json` — 공식 사실·경고·우리 정책을 분리한 claim ledger
- `lpscl_crosswalk.json` — Fair-Chem capability ↔ 우리 승인 범위
- `webapp_seed.json` — 공식 사이트를 닮은 webapp 섹션 seed

## 가장 중요한 규칙

`UMA`라는 이름 하나로 결과를 묶지 않아. 최소 method identity는 다음 네 가지가 같이 있어야 해.

```text
model/checkpoint + task + fairchem-core version + source/code revision
```

그리고 세 상태를 분리해.

```text
Official capability != Project validation != Approved claim
```

예를 들어 공식 문서가 OMat task로 inorganic materials를 지원한다고 말해도, 우리 Li3N 금지 판정이나 LPSCl MD seed/window 규약을 덮어쓰지 못해.

## Primary sources

- [Official documentation](https://fair-chem.github.io/)
- [Official GitHub snapshot](https://github.com/facebookresearch/fairchem/tree/93a03d656806a55f08c7cd126cfaa40ef18181fb)
- [UMA guide at the pinned commit](https://github.com/facebookresearch/fairchem/blob/93a03d656806a55f08c7cd126cfaa40ef18181fb/docs/core/uma.md)
- [OMat24 guide at the pinned commit](https://github.com/facebookresearch/fairchem/blob/93a03d656806a55f08c7cd126cfaa40ef18181fb/docs/inorganic_materials/datasets/omat24.md)
