# Papers and reusable manuscript insights

## 이번 bundle에 들어간 것

공식 `FAIR Chemistry Papers` 페이지의 H3 entry 42개를 구조화했어. 범주는 다음과 같아.

- universal models and architectures
- datasets
- generative models
- sampling and molecular dynamics
- applications and discovery
- training methods and techniques
- electronic structure and properties
- perspectives and introductions

`papers.json`은 discovery index야. 논문을 실제로 읽었다는 뜻은 아니고, 공식 페이지가 연결한 title/category/URL을 잃지 않게 한 거야.

## 우리 연구의 1차 읽기 순서

1. **UMA** — multi-domain task conditioning, MoLE, model family
2. **OMat24** — inorganic training distribution and reference convention
3. **OC25** — solid-liquid interface domain과 LPSCl interface의 차이
4. **eSEN / AllScAIP** — architecture/energy-conservation 비교
5. **active learning / uncertainty** — LPSCl DFT label acquisition 설계
6. **CatTSunami / AdsorbML** — cheap-to-expensive workflow 구조
7. **generative models** — future structure/site candidate generation

## Claude가 새 논문을 넣을 때

기존 `litdb` 규칙을 그대로 따라.

1. 로컬 PDF를 `litdb/papers/` digest로 정리해.
2. `litdb/figures/<slug>/figures.json`을 만들고 실제 crop을 봐.
3. 논문 수치는 `literature_value`로 두고 우리 DB 값과 섞지 않아.
4. `comparison_vs_ours.md`에는 무엇을 차용했고 무엇이 다른지 적어.
5. 아래 insight record를 `draft`로 만든 뒤 사람이 승인해.

```json
{
  "insight_id": "INS-UMA-LPSCL-...",
  "thesis": "...",
  "supporting_claim_refs": [],
  "counterevidence_claim_refs": [],
  "target_sections": ["Methods", "Limitations"],
  "allowed_wording": "...",
  "forbidden_wording": "...",
  "review_state": "draft"
}
```

논문 하나를 넣자마자 manuscript insight를 `verified`로 올리면 안 돼. 기본값은 `draft`, figure를 안 봤으면 `figure_reviewed=false`, 우리 chemistry에 적용하지 못하면 `applicability=not_assessed`가 맞아.

## 왜 PDF와 figure crop을 ZIP에서 뺐나

공식 paper index의 metadata와 link는 넣었지만 PDF와 그림은 재배포 권한이 다를 수 있어. 이번 ZIP은 source-linked metadata와 우리 digest 구조만 포함하고, 실제 PDF/crop은 로컬 litdb에서 관리하는 게 안전해.

Machine index: [papers.json](../../db/knowledge/fairchem/papers.json).

