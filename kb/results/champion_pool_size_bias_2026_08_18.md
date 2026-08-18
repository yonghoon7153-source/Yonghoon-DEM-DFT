---
title: 챔피언 점수는 후보를 몇 개 뽑았느냐에 지배된다 — best-of-N 편향이 종간 산포보다 크다
date: 2026-08-18
updated: 2026-08-18
tags: [cascade, ranking, best-of-n, sampling-bias, seminar, provenance]
status: 확정
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-18
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
---

# 챔피언 점수는 후보를 몇 개 뽑았느냐에 지배된다

세미나 12장 소불릿 — *"Candidate counts differ per compound, so **this selection is not a
ranking of elements**"* — 이 왜 있는지 1저자가 물었다. 앞에는 **정성적 경고**만 있었다.
크기를 쟀더니 **경고가 아니라 차단 사유**였다.

출처: `db/properties/cascade_v23_all.csv`. 챔피언은 `combined_score` **최대**가 맞다
(`rank_combined=="1"` 이 270묶음 **전부** 최대와 일치 — 확인함).

## 1. 후보 수가 종마다 10배 차이 난다 (15 ~ 150)

그리고 그 차이는 **성능이 아니라 화학**이 정한다:

| 종 | 구조 수 | 자리 조합 | 전하보상법 |
|---|---|---|---|
| MgO · ZnO | **150** | 2 | **2** (`compound_set`, `compound_set_chain`) |
| Li₂S | 90 | **6** | 1 |
| ScF₃ · TaCl₅ · TiF₄ | **15** | 1 | 1 |

2가 도펀트가 Li⁺ 자리에 가면 보상법이 둘로 갈리고, 앉을 수 있는 부격자가 많으면
자리 조합이 늘어난다. **더 좋아서 후보가 많은 게 아니다.**

## 2. 최댓값과 중앙값이 **반대로** 움직인다 — best-of-N 의 지문

```
후보 수 vs 챔피언(최대) score   r = +0.321
후보 수 vs 중앙값 score         r = −0.212
```

후보가 많은 종은 **전형적인 구조가 더 나쁜데도** 챔피언은 더 높다. 많이 뽑았으니
꼬리가 길어진 것뿐이다.

## 3. 크기를 쟀다 — 전부 15개로 맞추면

n ≥ 30 인 **75종**을 15개로 무작위 축소해 다시 챔피언을 뽑았다 (종당 200회 평균, seed 0):

```
챔피언 점수 하락폭   중앙 0.0837 · 평균 0.0900 · 최대 0.3010
종별 챔피언 점수 표준편차            0.0691
⇒ 표집 효과 / 종간 산포 = 121 %
```

**표집 효과가 종끼리의 차이보다 크다.** 그리고 순위로 보면:

```
같은 크기(15)로 맞췄을 때 움직인 칸수: 중앙 17 / 90 · 최대 74
10칸 넘게 움직인 종: 62 / 90
```

⇒ 챔피언 점수로 90종을 줄 세우면 **읽는 것은 대체로 표집 노력이다.**

## 4. 그래서 슬라이드 문장은 완화하면 안 된다

- ✅ **"this selection is not a ranking of elements"** — 그대로 둔다. 빨강(한계)이 맞다.
- ⛔ "대략적인 순위 정도로는 볼 수 있다" — **안 된다.** 중앙 17칸이 움직인다.
- ⚠ 이 카드는 **챔피언 선택 자체**를 부정하지 않는다. 한 화합물 안에서 1등을 고르는 것은
  정당하다. 부당한 것은 **서로 다른 크기의 풀에서 나온 1등끼리 비교**하는 것이다.

⇒ 이는 `cascade_audit_artifact_status.csv` 의 "승인된 current ranking 0종" 판정과
  **같은 방향의 독립 근거**다 (그쪽은 아티팩트 계보, 이쪽은 표집).

## 이 카드가 말하지 않는 것

- **어떻게 고치는가** — 풀 크기를 맞추거나(공통 N 으로 축소), 챔피언 대신 분위수/중앙값을
  쓰거나, best-of-N 보정을 넣는 세 길이 있는데 **어느 것도 안 해봤다.**
- **`combined_score` 자체가 타당한가** — 가중치·정규화는 여기서 검사하지 않았다.
  이 카드는 "같은 점수라도 비교가 안 된다" 만 말한다.
- **screen 축에서는 이만큼 크지 않다** — `screen_de_per_atom` 으로 재면
  r(챔피언) +0.006 vs r(중앙값) +0.060 으로 편향이 작다. 종합 점수에서 커진 이유는
  안 봤다 (여러 축을 곱/합하면 꼬리가 더 길어지는 것으로 읽히나 미검증).
- **270묶음 단위 vs 90종 단위** — 위 3절은 90종(라벨 합산) 기준이다. 묶음 단위
  (5~50개)로 하면 수가 달라진다.

## 재현

```bash
python3 - <<'PY'
import csv, io, statistics as st, collections, random, sys
sys.path.insert(0,'tools/cascade')
from cascade_ids import base_species
random.seed(0)
pool=collections.defaultdict(list)
for r in csv.DictReader(io.open('db/properties/cascade_v23_all.csv',encoding='utf-8')):
    if r.get("combined_score"):
        pool[base_species(r["dopant"])].append(float(r["combined_score"]))
big={k:v for k,v in pool.items() if len(v)>=30}
d=[max(v)-st.mean(max(random.sample(v,15)) for _ in range(200)) for v in big.values()]
print("하락 중앙 %.4f · 챔피언 산포 %.4f"%(st.median(d),
      st.pstdev([max(v) for v in pool.values()])))
PY
```

## 반영한 곳

| 무엇 | 어디 |
|---|---|
| 12장 `말로만` 에 수치 추가 | `kb/seminars/cascade_dopant_screening_story_2026_08.md` 12장 |
