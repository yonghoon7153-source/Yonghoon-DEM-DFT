# 14차 게이트 사이클 요약 — 리뷰 5라운드 → 본 실행 → 15차 판정

> 이 문서는 2026-08-11 ~ 08-13 사이에 일어난 일을 한 곳에 모은 **사람용 요약**이다.
>
> **수치의 정본은 `artifacts/*/` 의 `fits.parquet`·`objective_comparison.yaml`·
> `degeneracy_summary.yaml`·`artifact_index.yaml` 이다.** `docs/RESULTS*.md` 는
> 15·16차가 지적한 표기·해석 오류를 고쳐 **빈 격리 root 에서 재생성**했고
> (16차 P0 8항목 충족), 승격 여부는 17차 리뷰 판정을 기다린다.
> 발견 원장은 `docs/08_REVIEW_RESPONSE.md` §16~21. 여기 적힌 숫자는 사본이므로
> 인용 근거로 쓰지 말 것.

---

## 0. 한눈에

| 항목 | 상태 |
|---|---|
| 계산 코드 | `c0f1daa0` · `source_digest d50295f980ccaa81` (각 실행의 **시작·종료 digest 가 일치**했고 변경이 검출되지 않음 — periodic 검사가 없으므로 '실행 내내 불변'을 증명한 것은 아니다) |
| 산출물 | `artifacts/{grid_curves_v4, grid_fit_v4, halfcell_fit_v4, paired_fixed5_v4}` — Git blob 합계 **100.3 MB** (95.7 MiB, 88파일). `artifacts/` 디렉터리 전체는 116 MB (옛 v1/v2 포함) |
| 산출물 인용 가능성 | **GO** — 재실행 불필요 (15차 리뷰 판정) |
| 보고서 문구 인용 가능성 | 16차 P0 반영 후 재생성 완료 — **17차 판정 대기** |
| 남은 작업 | **A·A'·B·C·E·F** (Hessian provenance 묶음 + EOL 회귀 + chunk fail-fast) |
| 커밋 | 산출물 `61c1a75` · 코드 `34c156c` (`source_digest 4129e1a7c36c6534`) |

---

## 1. 게이트 리뷰 5라운드 (코드 확정까지)

본 실행 전에 적대적 리뷰를 5번 돌았다. 라운드마다 **차단점을 닫고 → 전체 테스트
+ strict smoke → push → 다음 요청** 을 반복했다.

| 라운드 | 대상 커밋 | 판정 | 주요 발견과 대응 |
|---|---|---|---|
| 1차 | `393ac3db` | NO-GO (8건) | noise family 교차 invariant 신설(`_verify_noise_families`), `source_digest` POSIX 정규화 + RUN_SCOPE 확대, sweep digest fail-closed, `w_grid` 이름 충돌, guards canonical 3-key, 재현 명령 경로, archive fail-closed·`source_commit` |
| 2차 | `0cd1999` | NO-GO (1건 차단) | **fully-failed family 의 noise 완전성** — failed 조건을 noise 없는 set 으로 축약해 불완전 family 가 통과했다(실측 `ok=True`). multiset 으로 고침 + `w_grid` round-trip + 재현 chain 확장 + `in_run_scope()` |
| 3차 | `010aa0b` | NO-GO (2건 차단) | sweep 재현 명령이 `<main-fit>` 을 출력으로 지정 / 존재하지 않는 `--stride` 출력. **fixture 가 `stride` 키를 안 만들어 오류를 가리고 있었다** — fixture 를 실물에 맞추고, 재현 블록의 모든 `./run.sh` 줄을 실제 wrapper 로 파싱 검사 |
| 4차 | `36fdad2` | NO-GO (1건 차단) | strict smoke 의 간헐 SIGABRT — 검사 3건 통과 출력 **뒤** teardown 크래시. 변경 전 커밋에서도 1/7 재현되어 회귀가 아님을 분리 측정. read-only validator 에만 `os._exit(rc)` 적용 |
| 5차 | `c0f1daa` | **GO** | 사전 조건 6개 충족: pytest 304 · smoke **10/10** · 새 digest 기록 · baseline/half-cell 재준비 |

### 이 과정에서 우리가 틀렸던 것

- 4차에서 SIGABRT 원인을 "PyBaMM/CasADi teardown" 으로 단정했으나 실측하면
  `pybamm_loaded=False`, `casadi_loaded=False`, `pyarrow_loaded=True` 였다.
  원인 미확정으로 낮췄다.
- 3차 차단점이 2차에 추가한 테스트를 통과했던 이유는 **fixture 가 실물 producer 와
  달랐기** 때문이다. 저장소 규칙이 예고한 패턴("테스트가 처음부터 통과하면 fixture 가
  진실을 가린 신호")이 그대로 재현됐다.

---

## 2. 동결과 본 실행 (V100)

```
코드      c0f1daa0d92a7625c3602799c81db04b5e2e5783 / d50295f980ccaa81   (시작·종료 일치)
하드웨어  Tesla V100-PCIE-32GB · 32코어 · RAM 125 GB
GPU 사용  없음 — PyBaMM DFN + composite phases 는 IDAKLU(CPU) 경로
```

| 단계 | 결과 | 소요 |
|---|---|---|
| pre-flight | pytest **304 passed** · strict smoke 통과 | 35분 + α |
| baseline `--force` | 36.64970365763882 / 3446.0841935406315 / 58439.87386449178 | — |
| half-cell `--force --verify` | `구조검사 true` · `재생성_배열일치 true` | — |
| grid | ok **3,069** / failed **924** (의도 3,993) | 1,931.6 s |
| main fit (grid 기준) | **12,276행** = 3,069 × 4목적함수 | 10,364.4 s |
| half-cell fit | **12,276행** | 9,332.3 s |
| paired fixed-5 (1차) | 6,138행 — **무효, 폐기** (§3) | 7,046.6 s |
| paired fixed-5 (재실행) | **6,138행** = 3,069 × 2목적함수 | 6,924.5 s |
| wsweep · score · Hessian · 보고서 | — | 약 9 h |
| archive | 요청 4 · 검증 가능 4 · 불완전 0 · Git blob 100.3 MB | — |

### fitting 전 invariant (게이트가 요구한 검사)

```
validator ok = True | fail = []
grid_sig_version = 5 | signed noise = [0.0, 0.001, 0.005]
effective_solver = IDAKLUSolver · pybamm 26.7.1.0 · pybammsolvers 0.9.0 · casadi 3.7.2
observed conditions = 3069   observed family = 1023, noise 불일치 0
max Δq_mah = 0 mAh (≤1e-6)   max Δv = 0 V (≤1e-10)
n_failed_total = 924         fully-failed family = 308, noise 불일치 0
=== INVARIANT PASS ===
```

family 내 편차가 허용오차가 아니라 **정확히 0** 이다 — "noise 는 solve 이후에만
얹힌다"가 3,069조건 전수에서 성립했다.

---

## 3. 실행 중 사고 — 검증 장치가 처음으로 실제 사고를 잡았다

paired fit(20:29~22:30) **도중**, 같은 clone 에서 작업하던 다른 세션이 DEM/MPM
브랜치(`claude/stoic-knuth-NObVQ`)로 전환했다. 그 브랜치에는
`degradation-degeneracy/src/`·`configs/` 가 없어 tracked 파일이 통째로 사라졌다.
이미 import 된 모듈로 계산은 끝까지 돌았지만 코드 정체성은 깨졌다.

```
grid_curves_v4    src_changed=False git_changed=None
grid_fit_v4       src_changed=False git_changed=False
halfcell_fit_v4   src_changed=False git_changed=False
paired_fixed5_v4  src_changed=True  git_changed=True
paired_fixed5_v4  ok=False fail=['입력봉인_교차일치', '실행중_코드불변']
```

- `실행중_코드불변` = `src/` 소멸, `입력봉인_교차일치` = 종료 시점에 봉인 입력을
  재해시할 수 없게 된 것.
- **`--resume` 으로 잇지 않았다.** run_sig 가 같아 기술적으로는 가능하지만 어느
  행이 오염된 상태에서 계산됐는지 증명할 수 없다. 처음부터 재실행했다.
- 무효본은 `results/_INVALID_paired_fixed5_v4_srcchanged` 로 보존.
- 재발 방지: DEM 작업을 `git worktree add ~/dem-work` 로 분리했다.

5차 리뷰(F49)부터 쌓아 온 코드 identity 봉인이 **가정된 위협이 아니라 실제 사고**를
잡은 첫 사례다. 이 장치가 없었다면 결론 2의 인용 정본이 조용히 통과했다.

---

## 4. 결과 — **정정된 수치**

> ⚠ 아래는 15차 리뷰가 지적한 오류를 반영한 값이다. 이전에 보고했던
> "62% → 63%", "붕괴 0%" 는 **틀렸다**.

### 4.1 목적함수 비교 — 정본은 paired

| pipeline | 33p (pOCV+dV/dQ) | 34p (+dQ/dV) | 차이 |
|---|---:|---:|---:|
| 비대칭 main (`grid_fit_v4`) | 0.621951 | 0.627371 | +0.54%p |
| **공정 paired (`paired_fixed5_v4`, 정본)** | **0.619241** | **0.871951** | **+25.27%p** |

공정 비교에서 34p 는 "사실상 변화 없음"이 아니라 **recovery failure 가 61.9% →
87.2% 로 크게 악화**했다. 단 이를 "dQ/dV 의 정보량이 더 나쁘다"로 읽으면 안 된다 —
paired 에서 34p 해의 multimodal 비율이 97% 인데, 이 관측에는 목적함수 지형·실제
비식별성·parameterization·optimizer/protocol 의존성이 모두 섞여 있어 **한 요인으로
귀속할 수 없다**.

> **방어 가능한 문장** (endpoint 를 고정해야 한다): 사전 정의한 raw 2%p max-mode
> recovery-failure endpoint 는 비대칭 main(62.20% → 62.74%)과 matched-budget
> paired(61.92% → 87.20%) 어느 쪽에서도 34p 에서 낮아지지 않았다.

다른 endpoint 까지 싸잡아 "어떤 개선도 없었다"고 쓰면 **거짓**이다 — main 의 행별
max-mode 절대오차 평균은 0.024692 → 0.023970 으로 미세하게 낮아진다. paired 의
bias-corrected failure 는 0.144309 → 0.945122 로 크게 악화한다.

### 4.2 붕괴율과 우도비 — 조건부 값이다

| 모집단 (noise=0, 33p) | 작은 격차에서 "같다" | 넓은 격차 붕괴 | 사건률 비 |
|---|---:|---:|---:|
| grid-recoverable | 36/98 = 36.7% | **1/245 = 0.41%** | **90.0** |
| 전체 생성성공 격자 | 61/156 = 39.1% | **64/604 = 10.6%** | **3.69** |

- 예전에 보고한 "0%" 는 **정수 percent 반올림**이 만든 것이다. 실제 값은
  `gap_collapse_frac = 0.004081632653061225`. 0건이었다면 우도비가 90.0 이 아니라
  무한대여야 한다.
- 넓은 격차 붕괴 **64건 중 63건(98.4%)** 이 recoverability 필터로 제외된다.
  90 을 인용하려면 3.69 와 52% 선택 효과를 **반드시 병기**해야 한다.
- 붕괴 1건: `cond_id c2e8442aa1f3`, truth LAM_PE/NE = 0.16/0.08 (참 격차 8.0%p)
  → 복원 0.16367/0.161593 (복원 격차 0.21%p).

### 4.3 22p 근방 — artifact·목적함수마다 다르다

"12%" 는 **`paired_fixed5_v4`, 33p, noise=0, 최근접 8 grid 조건, raw max-mode
error > 2%p** 에서 `1/8` 이다. 조건을 바꾸면 값이 달라진다:

| artifact | objective | 최근접 8조건 failure |
|---|---|---:|
| paired fixed-5 | 33p | 1/8 = 12.5% |
| paired fixed-5 | 34p | **4/8 = 50%** |
| 비대칭 main | 33p | 1/8 = 12.5% |
| 비대칭 main | 34p | 1/8 = 12.5% |

그 1건은 최대 mode 오차가 2.02248%p 로 임계 2%p 를 0.022%p 넘긴 **경계 사건**이다.
임계를 2.025%p 로 바꾸면 0/8, 1.9%p 로 바꾸면 2/8 이다. 이 8개는 실제 셀 8개가
아니라 설계 격자의 최근접 8점이다.

### 4.4 기준 곡선 효과 (Case 1 vs Case 2)

| objective | Case 1 (half-cell) | Case 2 (grid) |
|---|---:|---:|
| 33p | **0.065718** | 0.621951 |
| 34p | 0.099593 | 0.627371 |

목적함수를 바꾼 차이(0.6220 ↔ 0.6274)와 자릿수가 다르다. 다만 두 실행은 reference
외에 bounds·`p_ini`·mode 매핑도 다르므로 **reference 단독 인과효과가 아니라
reference-specific pipeline 비교**로만 말할 수 있다.

### 4.5 모집단 — 분모를 정확히 쓴다

| 분모 | recoverable 부분집단 |
|---|---:|
| 생성성공 3,069 condition-noise rows | 1,476 = **48.1%** |
| 의도한 3,993 condition-noise rows | 1,476 = **37.0%** |
| family 단위 (1,331) | 492 = **37.0%** |

- **목적함수당 1,476 rows** 다. `5,904` 는 main artifact 의 4목적함수 행 합계
  (파일 행 수)이지 어떤 비율의 분모도 아니다. paired 는 2목적함수라 2,952 행이고
  artifact 전체는 3,069 × 2 = 6,138 행이다.
- gap 분석의 분모는 또 다르다 — noise=0 의 98·245 조건. 22p 는 8조건.
- 1,476 을 독립 셀의 표본 수로 쓰면 안 된다. **492 degradation family × 3 noise
  수준**의 동일가중 설계 격자다.
- 생성성공군의 51.9%(1,593조건)는 **선택한 grid-reference fitter 의 현재 α/bounds
  feasible domain 밖**이다(참 α<1). "원리적으로 복원 불가"라고 쓰지 않는다 — 실제
  셀·다른 reference·다른 parameterization 으로 확장되는 표현이다.
- **모집단에 따른 우열 뒤집힘은 비대칭 main 에만 있다** (`direction_flips=True`,
  recoverable +0.54%p / 전체 −2.57%p). **paired 정본은 뒤집히지 않는다**
  (`direction_flips=False`, recoverable +25.27%p / 전체 +15.74%p).

---

## 5. 보관과 외부 검증

- archive 4/4 승격, `artifacts/artifact_index.yaml` 의 `source_commit` 은 전부
  `c0f1daa0` (계산 **시작** 커밋).
- **다른 clone 에서 실제 확인**: 4개 묶음 모두 `검증 가능: 필요한 파일이 모두 있고
  digest가 일치한다`.
- 하마터면 깨질 뻔한 것: `failed.csv` 는 `csv.writer` 가 CRLF 로 쓰는데
  `.gitattributes` 의 `*.csv text eol=lf` 가 이를 정규화한다. `git add` 경고로
  발견해 `artifacts/** -text` 로 막았다(RUN_SCOPE 밖이라 digest 불변).
- V100 반납 전 git 밖 원본(`results/`·`.cache/`·로그·사고 무효본)을
  `v4_run_extras.tar` (331 MB) 로 백업하고 전송 전후 해시를 대조했다
  (`eb1174509b48a7b4d1d50a96a032da50b8515eba89459e6ea02b65675b167ece`).
  **다만 이 tar 는 저장소 밖에 있어 제3자가 확인할 수 없다** — 재현성 증거로
  쓰려면 full digest 와 파일 목록을 별도 manifest 로 커밋해야 한다. 네 Git
  artifact 의 인용 가능성에는 영향이 없다.

---

## 6. 15차 리뷰 판정

| 대상 | 판정 |
|---|---|
| v4 `curves.parquet`·`fits.parquet`·archive | **GO** — 조건부 기술통계로 인용 가능 |
| 현재 `RESULTS*.md` 문구 | **NO-GO** — 수치·해석 수정 후 재생성 |
| dQ/dV 효과 | 제한적 GO — "개선 미관측"까지 |
| dQ/dV 고유 정보량 | NO-GO — optimizer 난이도와 분리 불가 |
| 실제 22p 셀의 물리 판정 | NO-GO — 부분집단 사건률로 posterior 불가 |
| Case 1 vs Case 2 | 제한적 GO — pipeline 비교로 한정 |
| Hessian | 결론 근거 NO-GO (진단 참고만) |

**8시간 재실행은 불필요**하다. 다만 그 근거는 "배너가 안 뜬다"가 **아니다** —
배너 부재는 validator 정책일 뿐 과학적 증명이 못 된다 (15차-2 발견 11).

올바른 근거는 세 가지다.
1. 봉인된 `c0f1daa0` 코드·입력·출력이 서로 일치한다 (RUN_SCOPE 46파일 digest
   `d50295f980ccaa81`, 네 manifest 의 시작·종료 기록 일치).
2. A~F 는 canonical curves/fits 의 **계산식을 바꾸지 않는다** — 파생 단계(A·B),
   커버리지·보관(C·E), 성능(D), 조기 중단(F)이다.
3. A 의 staging 은 봉인 곡선과 byte-identical 이었고 재계산 Hessian 도 일치했다.

운영상 사실로는 `src/io.py:1511-1521` 이 다른 commit 에서 `코드_재계산` 을 건너뛰고
`_참고_코드재계산불가` 로 남기므로, 새 코드로 보고서를 재생성해도 배너는 생기지
않는다. 그때는 **두 provenance 를 분리 기록**해야 한다 — 계산 generator
(`c0f1daa0` + fits/curves full SHA-256)와 파생 report generator(새 commit·digest).

---

## 7. 남은 작업 (13항목)

### 렌더링·해석 — 보고서 재생성으로 반영

- [ ] paired 정본 수치를 `61.9% → 87.2%` 로 통일
- [ ] `0%` 를 `1/245 (0.41%)` 로, **count 우선** 렌더링
- [ ] LR 90 옆에 전체 격자 LR 3.69 와 52% 선택 효과 병기
- [ ] 22p 12% 를 `1/8` + noise·반경·임계 명시로 교체
- [ ] `평균 |err|` → `행별 max-mode 절대오차의 평균` 으로 라벨 수정
- [ ] Case 1/2 를 reference-specific pipeline 비교로 제한
- [ ] Hessian 절의 자기모순 문장 삭제 (`RESULTS.md:172` vs `:183`)

### 코드 결함 — 회귀 테스트 동반

- [ ] **A** Hessian 이 봉인 `_inputs` 곡선을 자동 해석하거나 `--curves` 를 받도록
      (현재 producer/fit 분리 배치에서 `FileNotFoundError`)
- [ ] **A'** half-cell Hessian 이 live cache 대신 봉인 recipe·cache 를 쓰도록
- [ ] **B** Hessian 이 `degeneracy_summary.yaml` 을 변이시키지 않도록 분리
      (현재 `score → hessian → report` 순서가 인용 금지 배너를 만든다)
- [ ] **C** smoke 에 분리배치 Hessian + `score→hessian→report` stale 회귀 추가
- [ ] **D** `src/io.py:911` 의 `sorted(..., key=repr)` → `key=lambda kv: kv[0]`
      (실측 16.47s → 0.838s, 19.7배)
- [ ] **E** artifact CRLF 의 Git byte round-trip 회귀 테스트 추가
- [ ] **F** chunk 경계 digest fail-fast (인용 게이트가 아니라 조기 중단 장치)
- [ ] `artifacts/README.md` 의 v4 목록 갱신

### 재실행으로는 해결되지 않는 것

LR 모집단 문제(52% 조건부 선택)와 22p 임계 민감도는 **계산이 아니라 해석·조건화의
문제**다. 8시간을 다시 돌려도 바뀌지 않는다. "실제 22p 셀에서 두 전극이 비슷하게
열화했다"는 판정은 이 자료로 불가능하며, 어느 버전에서도 그 문장은 쓰지 않는다.

---

## 8. **보고서 수정 후** 쓸 수 있는 문안 (현재형 아님)

> 아래 문안은 `RESULTS*.md` 재생성·대조가 끝난 뒤에 쓴다. 지금 그대로 인용하면
> 안 된다 (현재 보고서에는 정수 반올림 `0%` 와 비대칭 headline 이 남아 있다).

✅ 수정 후 쓸 수 있다

> 생성에 성공한 3,069 condition-noise grid rows 중, 선택한 grid-reference fitter
> 에서 truth 가 표현 가능한 부분집단은 **목적함수당 1,476 rows** 였다
> (492 degradation family × 3 noise 수준; 생성성공군의 48.1%, 의도한 3,993조건의
> 37.0%). 사전 정의한 raw 2%p max-mode recovery-failure endpoint 는 비대칭 main
> 에서 33p 918/1476(62.20%), 34p 926/1476(62.74%), matched fixed-5/no-warm/
> no-adaptive pipeline 에서 각각 914/1476(61.92%), 1287/1476(87.20%) 였다.
> 이 endpoint 에서는 어느 pipeline 에서도 34p 개선이 관측되지 않았으나,
> 목적함수의 고유 정보량과 optimization/protocol 의존성은 분리되지 않았다.

> `paired_fixed5_v4` 의 33p·noise=0·grid-reference recoverable 부분집단에서,
> 복원 격차 2%p 미만 판정은 참 격차 2%p 미만군의 36/98(36.7%), 참 격차 6%p
> 이상군의 1/245(0.41%) 에서 발생해 **조건부 기술적 사건률 비**가 90.0 이었다.
> 생성성공 격자 전체에서는 각각 61/156(39.1%), 64/604(10.6%) 로 비가 3.69 다.
> 두 값은 2–6%p 중간군을 제외하고 선택한 임계와 동일가중 합성 격자에 조건부이며
> **실제 셀 posterior 가 아니다**. 의도한 3,993조건 중 924조건은 generation
> guard 에서 실패했다.

❌ 쓸 수 없다

- "dQ/dV 는 degeneracy 를 줄이지 못한다" → 정보량 주장. optimizer 난이도와 분리 불가
- "붕괴가 없었다 / 0건 / 0%" → 실제 1/245
- "우도비 90 이므로 22p 는 degeneracy 가 아니다" → 부분집단 조건부, posterior 아님
- "기준 곡선이 목적함수보다 큰 원인" → pipeline 차이가 섞임
- "격자의 52% 는 원리적으로 복원 불가" (물리 명제로) → 현재 fitter 의 α/bounds
  feasible domain 판정이다
- "복원가능군 5,904행" → 목적함수당 1,476 rows 다 (5,904 는 main 4목적함수 합계)
- "모집단에 따라 우열이 뒤집힌다" (paired 에) → 뒤집힘은 **비대칭 main 에만** 있다
- "우도비" (무조건적 표현) → 동일가중 합성격자의 **조건부 기술적 사건률 비**


---

## 9. 이 문서 자체의 정정 이력

`cb32179` 초판에 오류가 있어 15차-2 적대적 교차검토가 14건을 지적했고, 전부
산출물 실측으로 확인해 반영했다.

| # | 초판의 오류 | 정정 |
|---|---|---|
| 1 | `RESULTS*.md` 를 정본이라 하면서 동시에 NO-GO 라 했다 | 정본은 `artifacts/*` 의 parquet·YAML 로 한정. `RESULTS*.md` 는 재생성 후 승격 |
| 2 | paired 분모를 5,904행이라 했다 | **목적함수당 1,476 rows**. 5,904 는 main 4목적함수 합계 |
| 3 | "전체의 48%" 로 분모를 숨겼다 | 생성성공 3,069 기준 48.1% / 의도 3,993 기준 **37.0%** 병기 |
| 4 | 모집단 우열 뒤집힘을 paired 에도 적용했다 | 뒤집힘은 **비대칭 main 에만** (`direction_flips`: main True / paired False) |
| 5 | "어떤 개선도 관측되지 않았다" | endpoint 고정 필요 — main 의 max-mode 오차 평균은 미세 개선(0.024692→0.023970) |
| 6 | 사건률 비 90 문장이 자기완결적이지 않았다 | artifact·목적함수·noise·모집단·중간구간 제외·민감도 명시 |
| 7 | 22p 1/8 을 일반 결과처럼 썼다 | paired 34p 는 **4/8** — artifact·목적함수 명시 |
| 8 | 97% multimodality 를 "optimizer 가 못 푼다"로 단정 | 요인 분리 불가로 완화 |
| 9 | "원리적으로 복원 불가" | 현재 fitter 의 feasible domain 판정으로 수정 |
| 10 | "실행 내내 불변" | 시작·종료 일치 + 변경 미검출로 낮춤 (periodic 검사 없음) |
| 11 | 재실행 불필요 근거를 "배너 안 뜸"으로 제시 | 봉인 코드·입력·출력 일치와 A~F 의 영향 범위로 교체 |
| 12 | v4 묶음 116 MB | Git blob **100.3 MB** (95.7 MiB, 88파일). 116M 은 `artifacts/` 전체 |
| 13 | 체크리스트 13항목 / 최신 커밋 `1a33190` | **15항목**, 이 문서는 `cb32179` |
| 14 | tar 백업을 재현성 증거처럼 제시 | 저장소 밖이라 제3자 확인 불가임을 명시 |

15차-2 가 유지한 판정: **v4 curves/fits/archive 는 GO, 장시간 fit 재실행 불필요.**


---

## 10. 15·16차 반영 이후 (2026-08-16)

계산은 다시 하지 않았다 (`c0f1daa0` / `d50295f980ccaa81` 봉인 그대로). 보고서
생성 코드와 validator 만 고치고 **빈 격리 root** 에서 재생성했다.

| 라운드 | 고친 것 |
|---|---|
| 15차 | 붕괴율 count 우선(`1/245 (0.41%)`), 전체격자 `64/604`·`3.69` 병기, "우도비"→"조건부 사건률 비", 22p 조건 명시, `평균 max-mode \|err\|` 라벨, Case 1/2 pipeline 한정, feasible domain 표현, Hessian 자기모순 제거, 결론 번호 |
| 15차-3 (자체 발견) | `validate_provenance` 가 봉인 입력을 **CWD 우선**으로 찾아 격리 검증이 원본 파일을 대조하던 구멍. 실측: 격리본을 위조해도 `ok=True` → 수정 후 `fail=['입력_digest_재해시']` |
| 16차 | `repo_root` 를 score·compare·report 전 경로에 관통, 상세표 count 우선, 모집단 분모 분리(목적함수당 1,476), **22p 최근접 8점이 "모두 PE=NE" 라는 거짓 전제 제거**(실측 PE=NE 4 + 2%p 4, wide-gap 0), paired 의 adaptive 경고 분기, multistart 서술 완화, 재현 블록에서 Hessian 분리, header 를 artifact producer / report generator 로 분리 |
| D (성능) | family 정렬이 DataFrame 을 문자열화하던 것 제거 — 정렬 41.896 s → 0.0019 s |

최종 재생성본은 두 문서 모두 **인용 금지 배너 없음**이고, header 에 다음이
분리 기록된다.

```
artifact producer git/source_digest: c0f1daa0… / d50295f980ccaa81
report generator git/source_digest/dirty: <생성 commit> / <생성 digest> / False
```

남은 것은 Hessian provenance 묶음(A·A'·B·C)과 E·F 다. Hessian 은 결론 근거에서
이미 제외돼 있으므로 이 묶음은 보고서 승격의 차단점이 아니다.

---

## 11. 17차 게이트 직전 자체 감사 (2026-08-16)

§10 에서 "16차 발견 4 (22p 거짓 전제) 제거" 라고 적었지만, 재생성본을 문장
단위로 다시 읽으니 **같은 전제가 다른 절에 그대로 남아 있었다**. 정정한다.

| # | 발견 | 상태 |
|---|---|---|
| 22.1 | `## 전극 격차를 구분하는가` 절 도입부가 "22p 근방은 참값이 애초에 PE=NE" 를 다시 말함 (`RESULTS.md:128`, paired `:115`) — 같은 문서 `:113` 과 모순 | 고침 |
| 22.2 | 16차 정정 문구 자체가 상수였음 ("절반은 PE=NE", "wide-gap 하나도 없다", "98·245조건, 22p 는 8조건") — 격자를 바꾸면 provenance 통과 배지를 단 채 거짓 | 데이터에서 뽑도록 고침 |
| 22.3 | 그 수정의 첫 판이 구성 count 를 봉인 `objective_comparison.yaml` schema 에 넣어 **인용 금지 배너를 유발**(F87 key 집합 대조). 렌더 전용 파생값으로 분리 | 고침 + schema 회귀 |

§10 의 "16차 — 거짓 전제 제거" 줄은 **부분적으로만 맞았다**: 결론 3 과 22p 절은
고쳤고 격차 절은 놓쳤다. 그 줄을 그대로 두되 이 절이 정본이다.

검증: 전체 **320 passed**, strict smoke 통과, 격리 root 재생성본 두 편 모두
인용 금지 배너 0 / `provenance 검증 통과` 1 / `애초에` 0회.

계산 산출물은 여전히 불변이다 (`c0f1daa0` / `d50295f980ccaa81`).
