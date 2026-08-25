# Claims, caveats and citation rules

## 인용 전에 반드시 분리할 것

### Software, model, dataset license

- root code: MIT
- FAIR-Chem LAMMPS component: separate GPL-2.0 notice
- pretrained checkpoint: model repository/license별 확인
- dataset: dataset card별 확인

“Fair-Chem은 MIT” 한 줄로 모델과 데이터 재배포까지 허용된다고 쓰면 틀려.

### Source snapshot and release

이번 지식 DB는 official `main@93a03d656806a55f08c7cd126cfaa40ef18181fb`를 고정했어. `main`은 설치 가능한 최신 release와 같은 개념이 아니야. 감사 시점에 관측한 latest core tag는 `fairchem_core-2.22.0`이지만, 실제 논문 계산에는 설치 환경의 package version과 checkpoint revision을 다시 기록해야 해.

### Fair-Chem v1 vs v2

v2는 breaking redesign이야. old `OCPCalculator`/trainer 예제를 v2 코드에 섞지 말고, v1 재현은 별도 pinned environment로 둬.

### OMat vs Materials Project

OMat/UMA energy와 MP energy correction/reference는 직접 호환되지 않아. 우리 Methods에는 다음처럼 쓰는 편이 정확해.

> UMA/OMat energies were used only for within-protocol screening, whereas grand-potential thermodynamics were evaluated in a separately pinned Materials Project phase-set workflow.

### Live documentation quality

HTTP 200은 실행 가능성을 뜻하지 않아. formation-energy, phonons, elastic tutorial은 현재 첫 code cell의 `quacc.recipes.mlp` import가 실패한 상태로 렌더돼 있어. 논문 Methods를 live tutorial copy/paste에 의존하지 말고 pinned source + 우리 execution receipt를 써.

### Sitemap and routes

공식 sitemap/robots가 localhost URL을 내므로 route discovery에는 쓰지 않아. source path가 stable ID고, live slug는 관측값이야.

## Claim status

이 KB는 아래를 한 칸에 합치지 않아.

```text
source_status      official / project
claim_status       fact / caution / inference / policy
applicability      pass / fail / not_assessed / inapplicable
allowed_use        methods / background / diagnostic / blocked
```

현재 curated claim은 [claims.json](../../db/knowledge/fairchem/claims.json)에 있어.

## 권장 citation stack

논문에서 Fair-Chem/UMA를 쓸 때 보통 네 층을 함께 남겨.

1. UMA method paper
2. relevant task/dataset paper, 예: OMat24
3. Fair-Chem software repository/version
4. 우리 local validation/protocol

공식 문서 URL만 인용하고 method paper와 dataset convention을 빼면 재현성이 약해져.

