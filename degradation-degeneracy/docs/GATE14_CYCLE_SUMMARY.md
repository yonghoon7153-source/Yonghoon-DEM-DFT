# 14차 게이트 사이클 요약 — 리뷰 5라운드 → 본 실행 → 15차 판정

> 이 문서는 2026-08-11 ~ 08-13 사이에 일어난 일을 한 곳에 모은 **사람용 요약**이다.
> 수치의 정본은 `artifacts/` 묶음과 `docs/RESULTS*.md` 이고, 발견 원장은
> `docs/08_REVIEW_RESPONSE.md` §16~21 이다. 여기 적힌 숫자는 사본이므로 인용
> 근거로 쓰지 말 것.

---

## 0. 한눈에

| 항목 | 상태 |
|---|---|
| 계산 코드 | `c0f1daa0` · `source_digest d50295f980ccaa81` (실행 내내 불변) |
| 산출물 | `artifacts/{grid_curves_v4, grid_fit_v4, halfcell_fit_v4, paired_fixed5_v4}` 116 MB |
| 산출물 인용 가능성 | **GO** — 재실행 불필요 (15차 리뷰 판정) |
| 보고서 문구 인용 가능성 | **NO-GO** — 수치 표기·해석 6건 수정 필요 |
| 남은 작업 | 체크리스트 13항목 (렌더링 6 + 코드 7) |
| 최신 커밋 | `1a33190` (원장 정정) / 산출물 `61c1a75` |

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
코드      c0f1daa0d92a7625c3602799c81db04b5e2e5783 / d50295f980ccaa81
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
| archive | 요청 4 · 검증 가능 4 · 불완전 0 · 116 MB | — |

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
paired 에서 34p 해의 multimodal 비율이 97% 라 **optimizer 가 그 목적함수를 못 푸는
효과**가 섞여 있다.

> **방어 가능한 문장**: 두 protocol 모두에서 dQ/dV 추가의 개선은 관측되지 않았다.

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

### 4.3 22p 근방

`degenerate_frac = 0.125` 는 **8조건 중 1건**이고, 그 1건은 최대 mode 오차가
2.02248%p 로 임계 2%p 를 0.022%p 넘긴 **경계 사건**이다. 임계를 2.025%p 로 바꾸면
0/8, 1.9%p 로 바꾸면 2/8 이다.

### 4.4 기준 곡선 효과 (Case 1 vs Case 2)

| objective | Case 1 (half-cell) | Case 2 (grid) |
|---|---:|---:|
| 33p | **0.065718** | 0.621951 |
| 34p | 0.099593 | 0.627371 |

목적함수를 바꾼 차이(0.6220 ↔ 0.6274)와 자릿수가 다르다. 다만 두 실행은 reference
외에 bounds·`p_ini`·mode 매핑도 다르므로 **reference 단독 인과효과가 아니라
reference-specific pipeline 비교**로만 말할 수 있다.

### 4.5 모집단

- 격자의 **51.9%** 는 grid 기준에서 원리적으로 복원 불가 (참값 α<1).
- 위 수치는 전부 복원가능군 **5,904행** 에서만 센 값이다.
- 33p·34p 우열은 모집단에 따라 **뒤집힌다** (복원가능군 +0.54%p / 전체 −2.57%p).

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
  `v4_run_extras.tar` (331 MB, sha256 `eb1174…7ece`) 로 백업, 해시 대조 완료.

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

**8시간 재실행은 불필요**하다는 것이 핵심 판정이다. 근거는 `src/io.py:1511-1521` —
`코드_재계산` 은 현재 commit == 기록 commit 이고 clean 일 때만 수행되고, 다른
commit 에서는 `_참고_코드재계산불가` 로 사실만 남긴다. 따라서 코드를 고쳐 digest 가
바뀌어도 **봉인 fits 로 보고서를 재생성할 때 인용 금지 배너가 생기지 않는다.**

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

## 8. 지금 인용해도 되는 문장 (실무용)

✅ 쓸 수 있다

> 이 합성 격자의 grid-reference 복원가능군(5,904행, 전체의 48%)에서, 공정
> paired protocol(fixed-5 restart, no warm start, no adaptive)로 잰 recovery
> failure 는 33p 61.9%, 34p 87.2% 였다. 두 protocol 어디에서도 dQ/dV 추가의
> 개선은 관측되지 않았다.

> 참 LAM 격차가 6%p 이상인 245조건 중 1조건(0.41%)이 복원 격차 2%p 미만으로
> 붕괴했다. 같은 임계·동일가중 격자에서 조건부 사건률 비는 90.0 이며, 전체
> 생성성공 격자에서는 64/604(10.6%), 비 3.69 다.

❌ 쓸 수 없다

- "dQ/dV 는 degeneracy 를 줄이지 못한다" → 정보량 주장. optimizer 난이도와 분리 불가
- "붕괴가 없었다 / 0건 / 0%" → 실제 1/245
- "우도비 90 이므로 22p 는 degeneracy 가 아니다" → 부분집단 조건부, posterior 아님
- "기준 곡선이 목적함수보다 큰 원인" → pipeline 차이가 섞임
- "격자의 52% 는 원리적으로 복원 불가" (물리 명제로) → grid reference 표현식에
  조건부인 진술
