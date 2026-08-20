# 단계 3 계약 — protocol 축 분해와 고정 restart bank

> 21차 게이트 리뷰 실행 순서 **4** 의 산출물. 리뷰가 "제안된 형태 그대로
> 단계 3 의 RUN_SCOPE 변경에 착수하는 것은 NO-GO" 라고 판정했으므로, **구현
> 전에** 계약을 문서로 고정하고 22차 리뷰를 받는다.
>
> 이 문서 자체는 `source_digest` 를 바꾸지 않는다 (`docs/` 는 RUN_SCOPE 밖).
> 여기 적힌 것을 `src/` 에 넣는 순간 **기존 산출물 전부가 재실행 대상**이 된다.

## 0. 왜 이 계약이 필요한가 — 실측된 세 가지 교란

셋 다 이 저장소에서 관측된 것이지 가정이 아니다.

| # | 교란 | 실측 근거 |
|---|---|---|
| 1 | `warm_start` 플래그 하나가 **원점과 조건 fitting 을 동시에** 바꾼다 | `src/fitting.py:862` 가 pristine `p_ini` 를 같은 플래그로 계산한다. 404 half-cell: `p_ini(34p)` `[1.509716,−0.418050,1.087242,−0.084175]` → `[1.518503,−0.421892,1.063315,−0.060152]` (`LEG_INVENTORY.md` §23) |
| 2 | `--n-restarts` 는 실행 횟수가 아니라 **예산 상한**이다 | adaptive 조기 종료(F66/F86). 같은 짝에서 2회 종료 행 223 → 238, random-only 34p 표본 607 → 592 |
| 3 | **noise 층을 바꾸면 restart 난수가 통째로 갈린다** | `Condition.cond_id = sha1(asdict(...))[:12]` 가 `noise`·`seed` 를 포함하고 (`src/grid.py:99`), `task["seed"] = int(sha1(cond_id)[:8],16)` 이다 (`src/fitting.py:817`). 잡음 축과 optimizer 축이 분리 불가 |

그래서 "warm 을 켰다/껐다", "restart 5 → 20" 같은 서술은 **한 축을 움직인
것이 아니다.** 계약의 목적은 각 축을 따로 켤 수 있게 만드는 것이다.

## 1. protocol 축 — 6개로 분해한다

현재 `run_spec` 은 `warm_start` 1개 · `optimizer.{adaptive,n_restarts}` 2개로
protocol 을 적는다. 이것을 다음으로 바꾼다.

```yaml
protocol:
  p_ini_restarts:        20        # 원점(pristine) fitting 예산 상한
  condition_restarts:    20        # 조건별 fitting 예산 상한
  p_ini_warm_start:      false     # 원점 연쇄에서 warm seed 를 쓰는가
  condition_warm_start:  true      # 조건 연쇄에서 warm seed 를 쓰는가
  adaptive:              false     # 측정 arm 에서는 항상 false
  restart_bank_version:  1
  restart_bank_sha256:   <64 hex>
```

### 1.1 하위호환은 두지 않는다 — fail-closed

옛 `warm_start` / `n_restarts` 단일 필드를 **읽지 않는다.** 새 필드가 없는
manifest 는 `sig_version: 6` 검사에서 실패한다.

이유: "없으면 옛 뜻으로 해석" 을 허용하면 옛 산출물이 새 계약을 만족하는
것처럼 보인다. 그건 21차 리뷰가 Q4 에서 금지한 "포괄적 동등 선언" 이다.
옛 다리는 §5 의 상태 분류로 다루지, 새 필드를 추론해 채우지 않는다.

### 1.2 `adaptive` 는 측정 arm 에서 강제로 꺼진다

`adaptive=true` 와 `restart_bank_sha256` 은 **양립하지 않는다** — bank 를
고정해도 조기 종료가 조건마다 다른 접두사만 쓰면 예산이 조건별로 달라진다.
둘을 동시에 지정하면 즉시 실패시킨다.

탐색용으로 adaptive 를 쓰는 것은 막지 않되, 그 산출물은
`inference_status: diagnostic_only` 로만 봉인된다.

## 2. restart bank — 물리 조건에 묶고, 접두사로 중첩한다

### 2.1 지금 구조의 문제

```
Condition(lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type, noise, seed)
  → cond_id = sha1(asdict)[:12]          # noise·seed 포함
  → task["seed"] = int(sha1(cond_id)[:8], 16)
  → rng = default_rng(seed); x0 = rng.uniform(lb, ub)
```

같은 물리 조건이라도 noise 층이 다르면 **다른 난수 초기값 집합**을 받는다.
noise 효과를 재려는 모든 비교가 optimizer draw 효과와 섞인다 (교란 3).

### 2.2 `pair_group_id` — 난수를 물리 조건에만 묶는다

```python
# 왜곡(treatment)·잡음(noise)·잡음 seed 를 제외한 물리 좌표만
pair_group_id = sha1(json({lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type}))[:12]
```

restart 난수는 `pair_group_id` + `bounds_preset` + `bank_version` 에서만
유도한다. 그러면 **같은 물리 조건의 모든 arm**(noise 층·왜곡·목적함수)이
정확히 같은 초기값 집합을 받는다.

> `bounds_preset` 을 넣는 이유: 난수가 `rng.uniform(lb, ub)` 라 bound 가
> 바뀌면 같은 난수여도 다른 점이 된다. bank 를 bound 에 묶지 않으면
> "같은 bank" 라는 말이 거짓이 된다.

### 2.3 중첩 접두사 `5 ⊂ 10 ⊂ 20 ⊂ 40`

bank 는 조건당 40개 점을 **한 번** 생성하고, 예산 N 인 arm 은 그 **앞 N개**를
쓴다. 그래서 예산을 늘린 arm 은 작은 arm 의 상위집합이고, 예산-성능 곡선의
차이가 "다른 난수를 뽑아서" 생긴 것이 아님이 구조적으로 보장된다.

```
bank[pair_group_id][0:5]   ⊂ bank[...][0:10] ⊂ bank[...][0:20] ⊂ bank[...][0:40]
```

`restart_bank_sha256` 은 **생성된 bank 전체**(모든 조건 × 40점)의 digest 다.
manifest 에 박아 두면 두 arm 이 같은 bank 를 썼는지 한 줄로 대조된다.

### 2.4 p_ini bank 는 별도다

원점은 조건 하나(`p_ini_cond`)를 fitting 하는 것이므로 조건 bank 와 섞으면
안 된다. `p_ini_bank_sha256` 을 따로 둔다. 이래야 2×2 의 A/B arm(원점만
다름)이 조건 난수를 공유한 채 비교된다.

### 2.5 base_init 과 warm 후보의 자리

리뷰 발견 1 의 요구 — 후보 집합을 **사전에 고정**한다.

```
후보 = [base_init] + ([warm] if 해당 축이 켜졌고 앞 해가 있으면) + bank[0:N]
```

두 가지 측정 방식을 **구분해서** 보고한다 (같은 것으로 섞지 않는다).

| 방식 | 뜻 | 총 후보 수 |
|---|---|---|
| **equal-cost ablation** | warm 이 bank 의 마지막 한 점을 **대체**한다 | 두 arm 모두 `1 + N` |
| **union search** | warm 을 **추가**한다 | no-warm `1+N`, warm `2+N` |

21차 warm 실험은 union 이었다 (warm arm 이 후보 하나 더 가졌다). 그것이
발견 3 의 "random-only 는 양쪽 동일, 결정론적 후보 하나가 늘었을 뿐" 의
정확한 기술이다. 단계 3 은 **둘 다** 돌려서 예산 효과와 warm 효과를 가른다.

## 3. half-cell 2×2 요인실험

`p_ini` 가 있는 것은 half-cell 기준뿐이므로 2×2 는 여기서만 성립한다.

| arm | `p_ini_warm_start` | `condition_warm_start` | 분리하는 것 |
|---|---|---|---|
| **A** | off | off | 기준선 |
| **B** | on | off | 원점 이동 효과 단독 |
| **C** | off | on | 조건 warm 효과 단독 |
| **D** | on | on | 상호작용 (= 현재 기본값) |

- 네 arm 은 **같은 condition bank·같은 p_ini bank·`adaptive=false`·같은
  예산**을 쓴다. 다른 것은 두 플래그뿐이다.
- 격자(grid) 기준은 `p_ini = null` 이라 원점 축이 없다 → **C vs A** 한 축만
  필요하다. 21차의 `paired_fixed5_v4_*` 짝이 이미 그 형태였고, 새 회귀
  `test_warm_pair_manifests_differ_only_by_the_warm_axis` 가 warm 외 차이 0 을
  확인했다.
- 사전 예측(기록해 두고 나중에 맞았는지 본다): B 와 D 에서 원점이 같은
  값으로 이동하고, C 는 원점이 A 와 **자리별로 동일**해야 한다. C 의 원점이
  움직이면 축 분리 구현이 틀린 것이다.

## 4. plateau 판정 — 사전에 고정한다

예산을 얼마나 줘야 "충분" 한지를 **truth 로 고르지 않는다** (발견 1: 모의
truth 로 protocol 을 고르면 선택 편향). 다음이 **전부** 사전 tolerance 안에
들면 plateau 로 본다.

| 지표 | tolerance | 왜 |
|---|---|---|
| 조건별 best `J` | 상대 `1e-3` (기존 `agree_tol` 과 같은 값) | 더 낮은 골짜기가 남아 있으면 아직 부족하다 |
| 추정 파라미터 `p` | 절대 `1e-2` (기존 `agree_tol*10`) | J 는 같은데 p 가 갈리면 평평한 골짜기 — 그건 degeneracy 이지 예산 부족이 아니다 |
| 최종 분류(`degenerate`) | 전이 행 비율 ≤ **1%** | 판정이 흔들리면 결론이 흔들린다 |
| restart-source 승자 구성 | 비율 변화 ≤ **2%p** | 승자가 계속 bank 뒤쪽에서 나오면 40 도 부족하다는 신호 |
| 조건별 discordance rate | ≤ **1%** | 위 넷의 조건 수준 집계 |

**측정 순서**: 한 clean source(무왜곡 dense half-cell) 에서 `5 → 10 → 20 → 40`
을 돌리고 인접 쌍을 비교한다. `20 ↔ 40` 이 전부 tolerance 안이면 20 을 채택,
아니면 80 까지 확장한다. 이 pilot 한 번이 §6 재실행 전체의 예산을 정한다.

> ⚠ 21차가 철회한 것을 반복하지 않는다 — `bias_pe2mv_r20` 한 다리는 원점·조건
> 예산·adaptive 가 함께 움직인 n=1 pilot 이었다 (철회[R20_RX]). 이 pilot 은
> 한 축(예산)만 움직이고 중첩 bank 로 난수를 고정한다.

## 5. leg 상태 분류 — Q4 답변의 구현

76다리를 소급 무효화하지도, 포괄적으로 동등 선언하지도 않는다.

| `inference_status` | 뜻 | 인용 |
|---|---|---|
| `canonical` | 새 protocol 정본 | ✅ |
| `historical_valid` | 옛 source commit 의 완전 bundle 로 재검증 가능 | 조건부 (regime 병기) |
| `recorded_only` | summary/manifest(+투영)만 남아 원자료 독립 재계산 불가 | ❌ 진단만 |
| `diagnostic_only` | 교란·교차-digest 라 인과 결론에 부적합 | ❌ 진단만 |
| `superseded` | 새 protocol 정본으로 대체됨 | ❌ |
| `excluded` | 원점 오염 등으로 폐기 | ❌ |

정확히 **하나**여야 한다. 현재 warm-probe 8다리는 행 수준 투영이 붙었으므로
`recorded_only` 이고, 원자료가 보존되면 `historical_valid` 로 올라간다.

### 5.1 `leg_index.yaml` 스키마

```yaml
schema_version: 1
legs:
  - leg_id: fit_22p_seed_404_hc_warm_now
    pair_group_id: <12 hex>            # noise·treatment 뺀 물리 좌표
    treatment: {axis: pe_offset, value: 0.005}   # 무왜곡이면 null
    source_commit: <40 hex>
    producer_source_digest: <16 hex>   # 곡선을 만든 코드
    fit_source_digest: <16 hex>        # fitting 한 코드
    analyzer_source_digest: <16 hex>   # 채점·분석한 코드
    inputs_sha256:
      curves: <64 hex>
      fits:   <64 hex>
    objective_order: [pocv_dvdq, pocv_dvdq_dqdv]
    condition_ids_sha256: <64 hex>
    reference: halfcell
    bounds_preset: halfcell
    target_column: v_full_noisy
    protocol:                          # §1 의 6축을 그대로
      p_ini_restarts: 20
      condition_restarts: 20
      p_ini_warm_start: false
      condition_warm_start: true
      adaptive: false
      restart_bank_version: 1
      restart_bank_sha256: <64 hex>
      p_ini_bank_sha256: <64 hex>
      candidate_mode: union            # union | equal_cost
    p_ini_cond: <12 hex>
    projection_sha256: <64 hex>        # 행 수준 감사 앵커 (§30.1)
    analysis_spec_sha256: <64 hex>
    inference_status: recorded_only
    canonical_output: docs/22p_gap/<file>
    claim_ids: [P22_WARM_SENSITIVITY]
```

**producer / fit / analyzer digest 를 따로 적는 이유** (Q4): 곡선 생성기가
불변이고 봉인 provenance 가 유효하면 `curves.parquet` 은 새 fitting 의
입력으로 **재사용할 수 있다.** 세 identity 를 한 칸에 뭉치면 그 재사용이
불가능해 보인다.

## 6. 무엇을 다시 돌리는가 — 사전 목록

`source_digest` 가 바뀌면 **모든** 다리의 code identity 가 달라진다. 그렇다고
76다리를 전부 다시 돌리지 않는다 (비용도, 필요도 없다). 리뷰 순서 8 의
"claim-supporting 다리만" 을 사전에 못박는다.

| 다리 | 재실행 | 왜 |
|---|---|---|
| `paired_fixed5_v4_{nowarm_now,warm}` | ✅ | §20.4 결론 1 의 근거. C vs A 한 축 |
| 404 half-cell 4다리 | ✅ | 2×2 A·B·C·D 로 새로 |
| plateau pilot (무왜곡 dense hc) | ✅ 신규 | §4 |
| `bias_pe{1,1p5,2,5,10}mv` 건강 다리 | ✅ | §7.10 문턱의 근거 |
| 6격자 잡음 층 18다리 | ✅ | §7.10 6격자 표. `pair_group_id` bank 로 돌려야 noise 축이 처음으로 분리된다 |
| 원점 오염 폐기 3다리 | ❌ | `excluded` — 진단 기록으로만 |
| 5 mV 교차-digest 짝 | ❌ 대신 **새로** | 옛 digest 짝은 `diagnostic_only`. 새 protocol 에서 matched 짝을 새로 만든다 |
| 나머지 탐색 다리 | ❌ | `superseded` |

**곡선(`curves.parquet`)은 다시 만들지 않는다** — producer identity 가 안
바뀌면 봉인 입력으로 재사용한다 (§5.1). 재생성 ~28분이 여기서 빠진다.

### 6.1 비용 추정 (실측 기반)

`paired_fixed5_v4_warm`: 3,069조건 × 2목적함수 × 예산상한 5 = **833초**
(nproc 28, adaptive=False). 조건·목적함수·예산에 대략 선형이라고 보면

| 항목 | 조건 | 예산 | 추정 |
|---|---|---|---|
| plateau pilot (5+10+20+40) | 3,069 | 75 합 | ~3.5 h |
| paired C vs A | 3,069 × 2 | 20 | ~3.7 h |
| half-cell 2×2 | 640 × 4 | 20 | ~1.5 h |
| 문턱 5다리 + 6격자 18다리 | 소형 | 20 | ~3 h |
| **합** | | | **~12 h** |

10시간 규모라는 기존 감각과 같다. plateau 결과가 20 대신 40 을 요구하면
두 배가 된다 — 그래서 pilot 을 **먼저** 돌린다.

## 7. 구현 순서 (리뷰 순서 5~8)

1. `pair_group_id` + restart bank 생성기 (`src/grid.py`·`src/fitting.py`)
2. `protocol` 6축을 `run_spec` 으로, `sig_version: 6`, validator fail-closed
3. `p_ini` 경로에 `p_ini_warm_start`·`p_ini_restarts` 분리 (`fitting.py:832-873`)
4. smoke 에 2×2 arm + 중첩 bank 접두사 검증 (작은 fixture)
5. `leg_index.yaml` 생성기를 `tools/` 로 (지금 `docs/` 의 `leg_probe.py`·
   `row_projection.py` 를 승격)
6. 22p semantic freshness gate + archive index merge
7. plateau pilot → 예산 확정
8. §6 목록 재실행 → 정본 승격

**1~3 을 건드리는 순간 `source_digest` 가 바뀐다.** 그 전에 22차 리뷰를 받는다.

## 8. 이 계약이 스스로 지키지 못하는 것

정직하게 적는다.

- **`pair_group_id` 로 난수를 묶어도 noise 인과가 완전히 분리되지는 않는다.**
  잡음 실현 자체가 목적함수 지형을 바꾸므로, 같은 초기값에서 출발해도 경로가
  갈린다. 분리되는 것은 **초기값 축**이지 지형 축이 아니다. 그 이상은 같은
  잡음 실현을 여러 seed 로 반복해야 잴 수 있고, 이번 범위 밖이다.
- **plateau 는 "이 격자·이 화학·이 bound" 의 성질**이다. 다른 조건으로
  일반화하지 않는다.
- **2×2 는 half-cell 한 격자에서만** 돌린다. 격자 기준으로 옮길 수 없다
  (`p_ini` 가 없다).
- **equal-cost 와 union 을 둘 다 돌려도 "옳은 protocol" 이 정해지지 않는다.**
  정해지는 것은 두 estimand 의 값이다. 어느 쪽을 운영 정본으로 삼을지는
  사전 등록된 primary endpoint 로 고르는 것이지 결과를 보고 고르지 않는다.
