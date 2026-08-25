---
title: cascade 재랭킹 런북 ①~⑤ — li_mobility_score 복구 후 실행
date: 2026-08-25
updated: 2026-08-25
tags: [cascade, doping, bvse, ranking, runbook, blocked-on]
status: ①~③완료-④⑤남음
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-25
verifiedBy: "버그는 코드에서 직접 확인(저장 뒤 계산) · 결과는 cascade_v23_all.csv 에서 0/3615 로 실측 · 이동도 정규화 항이 전 행 0.5 동일함을 재계산으로 확인"
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# cascade 재랭킹 런북 ①~⑤ (2026-08-25)

> ✅ **착수 조건 충족 (2026-08-25 20:58)** — AlI₃ x020/x050/x100 완주 (rc=0). ① 진행 중.

## 1. 왜 재랭킹이 필요한가

`bvse_proxy.py` 가 `li_mobility_score` 를 **저장한 뒤에** 계산하고 있었다.
그래서 화면 순위표에만 쓰이고 json 에는 **한 번도 안 들어갔다.**

```
cascade_v23_all.csv   migration_volume_fraction   681/3615   ← 입력은 있다
                      bvs_li_proxy_score          681/3615   ← 입력은 있다
                      li_mobility_score             0/3615   ← 결과가 없다
```

그 빈 열을 `combine_rankings.py` 가 읽고, `normalize()` 의
*"전부 결측이면 0.5"* 규칙이 메웠다. 실측으로 **이동도 정규화 항이 3,615행 전원 0.5** 다.

```
score_combined = 0.4×안정성 + 0.3×탄성 + 0.3×이동도
                                          └─ 전원 0.15 상수 = 순위에 기여 0
```

**⇒ MD σ 를 비용 때문에 접고(stage 10 `TOP_K_SIGMA=0`) BVSE 프록시로 갈아탔는데,
그 BVSE 결과조차 랭킹에 들어간 적이 없다.** `score_combined` 는 사실상
**안정성 + 탄성 두 축**이었다.

⚠ 이것은 "랭킹이 틀렸다" 가 아니라 **"이동도 축이 작동한 적이 없다"** 이다.
  기존 순위는 두 축 기준으로는 유효하다 — 다만 세 축이라고 말하면 안 된다.

**도구 수정은 끝났다** (`bvse_proxy.py`, 2026-08-25). 남은 것은 **기존 데이터 복구와
재랭킹**이고, 그건 결과가 바뀌는 일이라 사람이 판단할 사안이라 자동으로 하지 않았다.

## 2. 순서 ①~⑤

```bash
# ── ① backfill — 새 계산 0. 입력 두 개가 이미 저장돼 있어 산수만 하면 된다
cd /data/work/repo && git fetch origin claude/friendly-meitner-lldvar && git reset --hard FETCH_HEAD
# ⛔ 2026-08-25 정정 — 정본 파일명은 **bvs_report.json** 이다 (bvse_proxy --out 예시
#   그대로). 원판의 'bvse*.json' 패턴은 0건 매치라 ① 이 조용한 no-op 이 될 뻔했다.
for f in $(find /data/work/runs -name 'bvs_report.json' -not -path '*bak*' 2>/dev/null); do
  python3 tools/doping/bvse_proxy.py --backfill --out "$f"
done
# 기대: "채움 N · 이미 있음 0 · 입력 부족 M". 멱등이라 두 번 돌려도 안전.

# ── ② 재랭킹 — 이제 이동도 30 % 가 실제로 일한다
#    ⚠ 실행 전에 **기존 순위를 반드시 떠 둔다** (전후 비교가 판정 근거가 된다)
cp db/properties/cascade_v23_all.csv /data/work/runs/cascade_v23_all_before_rerank.csv
python3 tools/doping/combine_rankings.py --cascade_dir <실제경로> --out <출력>

# ── ③ collect → 정본 CSV 갱신
python3 tools/doping/collect_dataset.py ...

# ── ④ A2: best-of-N 보정
python3 tools/doping/select_winners.py --results <uma_results.json> \
    --out <winners.json> --fixed_n 15
#    후보 수 15~150(10배)이 챔피언 점수와 r=+0.321 로 붙어 있던 인공물 보정.
#    표본 부족 그룹은 탈락시키지 않고 **표시**한다.

# ── ⑤ A3: 축 상관 + Pareto
python3 tools/doping/axis_corr_csv.py                       # 정본 CSV 기준
python3 tools/doping/analyze_screening.py --results <...> --out <...> \
    --axis_corr --pareto
```

## 2-1. ⛔ ① 직후 발견 — **결측이 "최악" 으로 채점되고 있다** (2026-08-25)

`--status` 실측:

```
AlI3_x002    구조 5    stability 5/5   modulus 1/5    mobility 1/5
B2O3_x005    구조 20   stability 20/20 modulus 2/20   mobility 2/20
Y2O3_lowx    구조 60   stability 60/60 modulus 0/60   mobility 6/60
AlI3_x050    구조 5    stability 5/5   modulus 1/5    mobility 1/5
```

**backfill 은 됐다** — BVSE 가 돈 구조에는 `li_mobility_score` 가 다 있다.
낮은 커버리지(10–20 %)는 결함이 아니라 설계다 (하류가 `--top 10` 만 처리).

문제는 다른 데 있다. `normalize()` 의 마지막 줄:

```python
return [float(x) if not np.isnan(x) else 0.0 for x in norm]
#                                        ^^^ 결측 → 0.0 = **최하점**
```

**미측정 = 최악**으로 채점된다. B2O3_x005 실측 재현:

```
mobility 정규화 → [0.0 × 18개, 1.0]
측정된 구조가 얻는 가산 : 0.3
미측정 구조가 받는 값   : 0.0
순위 격차               : 0.3 점 (만점 1.0)
```

modulus 까지 합치면 **가중치 0.6 이 "측정됐나" 하나로 갈린다.**

### 왜 이게 순위를 망가뜨리나 — 자기강화

1. stability 상위 10개만 BVSE·elastic 을 받는다
2. 그 10개만 modulus·mobility 에서 최대 +0.6 을 받는다
3. 나머지는 0.0 → 11위 이하는 **영원히 못 올라온다**

⇒ 이동도가 뛰어난 구조를 **발견할 수 없는 구조**다. 안정성을 사실상 두 번 세는 셈.

### ⚠ ① 이 이 문제를 **악화시켰다**

| | modulus | mobility |
|---|---|---|
| ① 이전 | 2/20 = 살아있음 → **이미 18개에 0.0 을 주고 있었다** | 0/N = 전부 결측 → 0.5 상수 → **무해** |
| ① 이후 | 동일 | 2/20 = 살아남 → **18개에 0.0 을 주기 시작** |

- **modulus 는 처음부터 이러고 있었다** (커버리지가 부분인 모든 캐스케이드에서).
- **mobility 는 ① 전까지 무해했다** — 전부 결측이라 0.5 로 평평했으니 순위에 기여가 0 이었다.
  ① 이 값을 채우면서 **비로소 이 왜곡에 합류했다.**

⇒ **② 를 지금 그대로 돌리면 안 된다.** "3축 랭킹 복구" 가 아니라
"측정 여부 가산점 0.6 점짜리 랭킹" 이 나온다.

### 판정 대기 — 세 갈래

| | 방식 | 장점 | 단점 |
|---|---|---|---|
| **A** | 측정된 부분집합끼리만 3축, 전체는 stability-only 로 별도 표기 | 데이터를 지어내지 않는다 · `--top 10` 설계와 일치 | 캐스케이드별 FINAL_RANKING 의 의미가 "top-10 재정렬" 로 좁아진다 |
| **B** | 결측을 0.0 대신 **축 중앙값**으로 | 20개를 한 표에 유지 · 미측정에 벌점 없음 | 중앙값도 없는 정보를 지어내는 것 |
| **C** | 현행 유지 (결측=0.0) | 변경 없음 | 안정성을 두 번 세는 왜곡이 남는다 |

**권고: A.** 유일하게 없는 값을 만들어내지 않는다.

---

## 2-2. ✅ ①~③ 실행 완료 (2026-08-25)

### 실행 결과

| 단계 | 결과 |
|---|---|
| ① backfill | 812/812 레코드 확인 (멱등 재실행으로 검증). `--backfill_glob` 로 한 프로세스 |
| ② 재랭킹 | **293개 캐스케이드**에 FINAL_RANKING.json 재작성, 9개 건너뜀(축 1개 이하) |
| ③ collect | 정본 3,615행 + 확장 풀 4,125행 |

**채택된 규칙: A** — 결합점수는 축 집합의 모든 축에 값이 있는 구조들 **안에서만**.
미측정은 `null` (0.0 도 0.5 도 아니다). 판정 기록: `db/governance/decisions.json`
→ `D-2026-08-25-missing-axis-is-unknown-not-worst`.

### 풀의 실제 크기 — 47종이 아니다

```
캐스케이드      302   (314 − v22 계열 12)
구조 전체     4,125   (v23 3,615 + dualx_v23 450 + as2s3_recover 60)
결합점수 있음   741   (18.0 %)
  그중 뜻 있음  692   (49개는 캐스케이드에 채점 대상이 1개뿐 → 상수 0.5)
```

**47종은 ESW 게이트를 통과한 부분집합**이지 풀 전체가 아니었다.

제외: `multi_category_2026_05_19_v22` + `_v22_OLD_radiusonly` (12 캐스케이드 535행).
담긴 도판트가 **Li₂O·Na₂O·Cu₂O 셋뿐**이고 x-level(x002/005/010)까지 v23 과 같아 순수 중복.
`as2s3_recover` 는 x-level 이 x020/050/100 이라 중복이 **아니라서** 남겼다.

### ★ 순위가 실제로 얼마나 바뀌었나 — 사과-대-사과

전후 rank 를 그냥 빼면 안 된다. 옛 방식은 **모든 행**에 순위를 줬고(미측정에 조작된 0.0 점),
새 방식은 **채점된 행에만** 준다 — 모집단이 다르다. 그래서 **채점된 행끼리의 상대 순서**만 비교했다:

```
비교 가능한 캐스케이드 (n≥2)   225
순서가 바뀐 캐스케이드          90   (40 %)
★ 1등이 바뀐 캐스케이드         53   (24 %)
Kendall 거리                 22.4 % (불일치 160 / 714 쌍)
```

**네 캐스케이드 중 하나에서 챔피언이 바뀌었다.** 그리고 미측정 **2,934행**이
옛 방식에서 받고 있던 조작된 순위를 잃었다(이제 `null`).

1등이 바뀐 예: `Al2O3_x002` · `AlCl3_x010` · `B2O3_x005` · `BaCl2_x002` · `BaO_x005` · `CaO_x010`

⚠ `Y2O3_x020`·`Y2O3_x050` 는 순위가 **내려갔다**(+4·+3 계단). Y 자리선호 작업과 겹치므로
그 판정을 인용할 때 이 재랭킹 이후 값인지 확인할 것.

### ⛔ 새 CSV 를 읽을 때의 규칙

| 열 | 뜻 |
|---|---|
| `axis_set` | 이 행이 몇 축으로 채점됐나. **다르면 `combined_score` 를 직접 비교 금지** (2축은 0.571/0.429, 3축은 0.4/0.3/0.3 — 척도가 다르다) |
| `rank_combined` | **캐스케이드 안에서의** 결합순위. 전역 순위가 아니다. 미채점은 빈칸 |
| `rank_stability_all` | 안정성 단일축 순위 (전체 행 대상) |
| `combined_score_is_informative` | `false` 면 그 캐스케이드에 채점 대상이 1개뿐이라 점수가 상수 0.5 |

---

## 3. ⏸ 왜 AlI₃ 완주를 기다리나

1. **AlI₃ 가 새 행을 추가한다.** 지금 재랭킹하면 AlI₃ 들어올 때 또 해야 하고,
   그 사이 **순위가 두 판 존재**하게 된다.
2. **AlI₃ cascade 는 수정 이전 코드로 돌고 있다** (gabia 가 그 전 커밋). 그쪽
   BVSE 출력도 `li_mobility_score` 가 비어 있을 것이므로 어차피 ① 대상이다.

⇒ 한 번에 처리한다.

## 4. ⚠ 재랭킹은 판정 이력에 남겨야 한다

순위가 바뀌면 그것은 **결과의 변경**이다. `db/governance/` 에 기록하지 않으면
"언제 왜 47종 순위가 달라졌나" 를 나중에 못 답한다. ② 를 돌릴 때 같이 만든다.
전후 CSV 를 떠 두라고 위에 적은 것이 그 근거 자료다.

## 5. 곁다리로 확인된 것 (재랭킹과 무관, 결함 아님)

`kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` 가 이미 답을 갖고 있다:

- **stage 10(σ MD)·11(W_ad) 는 미실행이다 — 미수확이 아니다.** `TOP_K_SIGMA=0` 으로
  꺼서 돌렸다(비용). 총 투입 ~1,100 GPU-시간이지 4,600 이 아니다.
- 축 커버리지 ~20 % 는 결손이 아니라 설계 — 하류가 `--top 10` 만 처리한다.
- **47종 풀을 가른 축은 ESW 하나다.** 탄성·BVSE 는 90종 전부 있었다.

## 6. A1 실측 (2026-08-25, `axis_corr_csv.py`)

```
공선성(|ρ|≥0.85)  0건
최대 |ρ|          0.326
상충 1건          안정성(ΔE) ↔ |ΔV/V0|   ρ = −0.326
```

Yang 2026(BML)은 σ↔Q_CC 가 붙어 Pareto 가 할 일이 없었는데, **우리는 반대로 축이 거의
독립**이다 ⇒ ⑤ 의 Pareto 가 실제로 선택지를 준다. 가중합으로 뭉개면 그만큼 잃는다.

⚠ 단 지금은 이동도 축이 비어 있어 사실상 두 축짜리 결과다. ①② 뒤에 다시 재야 한다.

## 안 한 것 / 못 하는 것

- **기존 순위를 다시 계산하지 않았다.** 도구만 고쳤다.
- ②③ 의 경로 인자는 실제 디렉터리를 봐야 정해진다 — AlI₃ 완주 후 확정.
- backfill 은 **입력이 없는 행을 0 으로 메우지 않는다.** 0 은 최하점이라
  "없다" 와 다른 거짓말이 된다. 건너뛰고 개수를 보고한다.
