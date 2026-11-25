# Claude handoff — Fair-Chem webapp section

## 목표

공식 Fair-Chem 사이트의 탐색 구조를 닮되, 우리 페이지의 중심은 “무슨 기능이 있나”보다 “어느 model/task/version이 어떤 증거와 적용성 판정을 가졌나”로 잡아.

이번 ZIP의 JSON은 초기 ingest seed야. production webapp의 장기 원장은 entity별 typed registry로 발전시키는 편이 좋아.

## 권장 route와 탭

```text
/fairchem
├─ Overview
├─ Models & Tasks
├─ Application Domains
│  ├─ Organic Molecules & Crystals
│  ├─ Heterogeneous Catalysis
│  ├─ Inorganic Materials
│  └─ MOFs for Direct Air Capture
├─ Quickstart & Recipes
├─ Tutorials & Common Tasks
├─ Datasets & Benchmarks
├─ Papers
├─ Our LPSCl Use
├─ Local Validation
├─ Decisions & Limitations
└─ Source & Provenance
```

공식 구조와 같은 순서를 쓰되 `Our LPSCl Use`와 provenance가 우리 차별점이야.

## Primary key

Live slug를 ID로 쓰지 마. `/summary-1`…`/summary-9`, `/models-1`…`/models-3`는 build order에 의존해.

```text
page_id = official source_path
snapshot_id = source_path + source_commit
```

`docs/core/uma.md` 같은 source path가 안정 ID고, `https://fair-chem.github.io/uma`는 snapshot observation이야.

## 최소 상태축

```text
nav_status: toc | external_nav | source_orphan | stale_search_only
content_status: live | experimental | warning_present |
                rendered_with_execution_error | source_only_orphan | removed
http_status: integer
execution_status: passed | failed | not_run | not_applicable
claim_status: proposed | verified | disputed | superseded | retracted
applicability: pass | fail | not_assessed | inapplicable
citable_status: no | conditional | yes
```

`HTTP 200`, `example executable`, `project validated`는 서로 다른 축이야.

## 권장 typed registry

```text
db/fairchem/
├─ schema/
├─ sources/<source_id>.json
├─ models/<model_id>.json
├─ tasks/<task_id>.json
├─ datasets/<dataset_id>.json
├─ claims/<claim_id>.json
├─ recipes/<recipe_id>.json
├─ validations/<validation_id>.json
├─ insights/<insight_id>.json
├─ releases/<release_id>.manifest.json
└─ index.json                 # generated only
```

역할 경계:

- PDF·figure interpretation: `litdb`
- 사람용 설명: `kb`
- 우리 수치 정본: `db/properties`
- decision/assessment: `db/governance`
- `db/fairchem`: 위 entity를 FK로 연결하는 검색/관계 DB

우리 수치를 `db/fairchem`에 복사해 두 번째 정본을 만들지 마.

## Page schema seed

```json
{
  "page_id": "docs/core/common_tasks/ase_calculator.md",
  "source_commit": "93a03d656806a55f08c7cd126cfaa40ef18181fb",
  "canonical_url": "https://fair-chem.github.io/ase-calculator",
  "nav_path": ["AI/ML Models & Usage", "Common Tasks"],
  "domain": "cross_domain",
  "page_type": "api_guide",
  "workflow_tags": ["inference", "ase", "relaxation", "md"],
  "http_status": 200,
  "content_status": "live",
  "source_sha256": "..."
}
```

## Model card 최소 필드

```text
model_id
checkpoint revision/hash
fairchem-core version
task matrix
reference DFT conventions
official cautions
license/repository
local validations
project exceptions
allowed uses
source snapshots
```

Software MIT와 gated model license를 같은 필드로 합치지 마.

## 추천 API

```text
GET /api/fairchem/v1/manifest
GET /api/fairchem/v1/pages
GET /api/fairchem/v1/models
GET /api/fairchem/v1/tasks
GET /api/fairchem/v1/datasets
GET /api/fairchem/v1/technologies
GET /api/fairchem/v1/papers
GET /api/fairchem/v1/claims
GET /api/fairchem/v1/lpscl-crosswalk
GET /api/fairchem/v1/sources/<id>
GET /api/fairchem/v1/search?q=...&task=...&status=...
```

모든 응답 envelope:

```json
{
  "schema_version": "...",
  "generated_at": "...",
  "source_commit": "...",
  "status": "ok",
  "warnings": [],
  "data": []
}
```

## UI 규칙

- Official fact와 Our interpretation을 색/열로 분리해.
- legacy model catalog를 current UMA와 한 표에서 current처럼 섞지 마.
- tutorial 200/failed 같은 모순을 배지 두 개로 그대로 보여줘.
- source SHA mismatch, unknown source, incompatible task/model이면 fail-closed해.
- paper entry는 `indexed`, `digest_read`, `figure_reviewed`, `human_approved`를 따로 보여줘.
- official checkpoint나 논문 PDF를 webapp/ZIP에 재배포하지 마.

## Claude가 새 UMA 논문을 추가할 때

1. 기존 ZIP manifest와 source commit을 검증해.
2. 논문을 litdb-curator 규칙으로 읽고 figure crop도 실제 확인해.
3. atomic claim은 `proposed/non-citable`로 추가해.
4. 우리 validation/decision을 FK로 연결해. 값을 복사하지 마.
5. 사람이 승인한 claim만 manuscript insight와 public page에 올려.
6. index와 generated KB는 single writer로 다시 만들어.

## 필수 회귀 테스트

- schema, enum, unique ID, FK, hash
- model/checkpoint/task/package compatibility
- source path ↔ live page status
- source-only orphan과 rendered error가 normal tutorial로 승격되지 않음
- citable claim에 primary evidence + human approval 존재
- superseded/retracted가 default search/manuscript export에서 숨겨짐
- UMA–Li3N 금지 유지
- OMat ↔ MP energy mixing 금지
- single-seed conductivity ratio 인용 금지
- task/model upgrade 뒤 old/new value 자동 병합 금지
- ZIP에 token, checkpoint, PDF, crop, server trajectory가 없음

## 구현 순서

1. 이 ZIP의 machine DB를 read-only loader로 붙여.
2. `/fairchem` overview + model/task + LPSCl crosswalk부터 렌더해.
3. source/hash/status test를 먼저 만들고 Papers를 붙여.
4. 그다음 entity-per-file registry와 paper ingestion을 이관해.
5. 마지막에 search와 release bundle을 자동화해.

