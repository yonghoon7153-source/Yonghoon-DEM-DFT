# Fair-Chem official knowledge bundle — 2026-08-21

## 목적

FAIR Chemistry 공식 문서와 공식 GitHub `main`을 논문·세미나·webapp에서 재사용할 수 있는 source-linked 지식 DB로 정리한 bundle이야.

이 ZIP은 official source code, checkpoint, dataset, PDF를 복제하지 않아. 대신 pinned commit의 모든 tracked path와 hash, live documentation 상태, model/task/dataset/technology/paper index, 우리 LPSCl 적용 범위, 갱신/검증 코드, Claude용 webapp handoff를 담아.

## Source freeze

- Repository: `https://github.com/facebookresearch/fairchem`
- Commit: `93a03d656806a55f08c7cd126cfaa40ef18181fb`
- Commit time: `2026-08-20T23:19:48Z`
- Live docs checked: `2026-08-21`

## 주요 수치

- 944 tracked files
- 66 tracked Markdown pages
- 64 MyST/live pages, all HTTP 200
- 2 source-only orphan pages
- 3 pages rendered with execution errors
- 19 broken internal link targets
- 13 package manifests
- 13 code-registered pretrained model names
- 7 curated UMA tasks
- 13 curated datasets
- 23 technologies/workflows
- 42 official paper-index entries
- 12 LPSCl crosswalk records

## ZIP 구성

```text
kb/fairchem/                     human-readable knowledge views
db/knowledge/fairchem/           machine-readable DB and inventories
tools/fairchem_kb/               rebuild, validate and package code
docs/reviews/..._README.md        this handoff
manifest.json                    per-file SHA256/bytes/status/exclusions
```

먼저 `kb/fairchem/README.md`, 그다음 `kb/fairchem/07_webapp_handoff_for_claude.md`를 읽으면 돼.

## Claude에게 넘길 때

1. embedded `manifest.json`의 hash를 확인해.
2. DB를 read-only seed로 먼저 붙여.
3. 새 UMA 논문은 litdb-curator workflow로 실제 PDF와 figure를 읽어 추가해.
4. official fact, local validation, allowed claim을 별도 status로 유지해.
5. checkpoint/PDF/crop을 public webapp이나 다음 ZIP에 넣지 마.

## 중요한 과학 경계

- UMA task는 DFT method identity의 일부야.
- OMat/UMA total energy와 Materials Project thermodynamics를 직접 섞지 마.
- batch throughput은 농도축이나 replicate를 만들지 않아.
- official workflow capability는 LPSCl validation과 같지 않아.
- official inorganic scope가 우리 project-specific UMA–Li3N 금지를 덮어쓰지 못해.

