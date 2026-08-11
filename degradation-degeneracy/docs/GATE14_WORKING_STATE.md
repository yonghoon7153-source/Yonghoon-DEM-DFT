# 14차 게이트 작업 상태 (durable handoff)

> **이 파일의 목적**: 14차 리뷰 7건을 고치는 동안 `src/io.py`(1465줄)·
> `tests/test_fitting.py`(2026줄)·`tests/test_compare.py`(2451줄) 를 **다시 통째로 읽지
> 않기 위해서** 필요한 좌표·코드 조각·설계를 여기에 고정한다. 압축(compaction) 후
> 복구는 이 파일 하나를 읽는 것으로 끝나야 한다.
>
> RUN_SCOPE 밖(`docs/`)이므로 이 파일을 고쳐도 `source_digest` 는 안 바뀐다.

기준 커밋: `393ac3db` (14차 리뷰 대상, base `eb843eea`) · 테스트 281 passed · strict smoke 전 단계 통과.

---

## 0. 진행 상태

| # | 발견 | 상태 |
|---|---|---|
| 2 | `source_digest()` 경로 정규화 (POSIX) + RUN_SCOPE 정합 | **다음 작업** (설계 완료, 코드 미작성) |
| 1 | noise family 교차 invariant (`_verify_observed_curves`) | 대기 (구조 조사 완료) |
| 3 | sweep checker fail-closed (`tools/check_sweep_consistency.py:184-215`) | 대기 |
| 4 | custom `w_grid` 충돌 (`src/weight_sweep.py:52-90`, `:350-355`) | 대기 |
| 5 | guards → canonical 3-key recipe (`src/io.py:907-937`) | 대기 |
| 6 | report reproduce command (`tools/make_results.py:1081-1108`) | 대기 |
| 7·8 | archive fail-closed / source_commit (`scripts/archive_results.sh:170-175, 229-241, 283-290`) | 대기 (계산 후 archive 전) |

1·2 는 **grid v4 생성 전 필수 blocker**. 3~6 은 같은 pre-run 커밋에 함께 권고. 7·8 은 계산 후 archive 전.

---

## 1. 발견 2 — `source_digest()` 경로 정규화

### 현재 코드 (`src/io.py:132-155`, 원문 그대로)

```python
def source_digest(root=None, dirs=("src", "tools", "configs")) -> str:
    """★ F49 — 실제로 import되는 source tree의 내용 해시.

    `run_sig` 에 코드 identity 가 없으면, **코드만 바꾸고 같은 output 에 resume 했을
    때 서로 다른 코드로 만든 행이 같은 서명 아래 섞이고 병합 검사를 통과한다.**
    (2026-08-07 5차 리뷰가 3조건 반례로 재현했다: OLD_CODE 행과 NEW_CODE 행이
    같은 `run_sig` 79f2e9c798ee 로 병합되고 validator 가 ok=True 를 냈다.)

    git commit 만으로는 dirty 실행을 못 잡으므로 파일 내용을 직접 해시한다.
    """
    root = Path(root) if root else Path(__file__).resolve().parent.parent
    h = hashlib.sha256()
    for d in dirs:
        base = root / d
        if not base.exists():
            continue
        for f in sorted(base.rglob("*")):
            if not f.is_file() or "__pycache__" in f.parts:
                continue
            if f.suffix in (".pyc", ".pyo"):
                continue
            h.update(str(f.relative_to(root)).encode())   # ← 153행: OS 의존
            h.update(f.read_bytes())
    return h.hexdigest()[:16]
```

### 리뷰어가 측정한 반례

같은 Git blob 인데 digest 가 셋으로 갈린다:

| 환경 | digest |
|---|---|
| POSIX (V100) | `4fa3e2af0a2e8106` |
| Windows 경로 구분자 `\` | `7ac22c1055eae262` |
| 실제 Windows worktree (잔존 CRLF 포함) | `808f19ea5556d018` |

### 고칠 것

1. **153행 키를 POSIX 정규화**한다. 그리고 **148행 정렬도 그 정규 키 기준**으로 바꾼다
   (`sorted(rglob)` 는 OS 경로 문자열 정렬이라 순서까지 OS 의존이다).
2. **RUN_SCOPE 정합**: 문서(root `CLAUDE.md` 하드룰 3)는 RUN_SCOPE 를
   `src/ tools/ configs/ scripts/ run.sh requirements*.txt` 6개로 적어놨는데
   실제 기본값은 `("src","tools","configs")` **3개뿐**이다. `scripts/`·`run.sh`·
   `requirements*.txt` 가 digest 밖이다.

### RED 테스트 설계 (Linux 에서 실제로 빨개지는 유일한 seam)

Linux 에서는 `str(PosixPath("src/io.py")) == "src/io.py"` 라 순진한 테스트는 처음부터
GREEN 이 된다 → 저장소 규칙상 그건 **fixture 가 진실을 가린 신호**다. 그래서 키 생성만
헬퍼로 뽑아 `PureWindowsPath` 로 때린다:

```python
# src/io.py
def _digest_path_key(rel) -> bytes:
    """digest 에 들어가는 경로 키 — OS 무관 POSIX 정규형."""
    return PurePath(rel).as_posix().encode("utf-8")
```

```python
# tests/test_compare.py (또는 test_io_bookkeeping.py)
from pathlib import PureWindowsPath
assert _digest_path_key(PureWindowsPath("src/io.py")) == b"src/io.py"
```

현재 코드(`str(...)`)면 `PureWindowsPath("src/io.py")` → `"src\\io.py"` 라
**오늘 Linux 에서도 진짜 RED** 다.

### 범위 확대 설계

```python
_SCOPE_DIRS = ("src", "tools", "configs", "scripts")
_SCOPE_FILE_GLOBS = ("run.sh", "requirements*.txt")
```

`(posix_relkey, path)` 쌍을 모아 **posix 키로 정렬**한 뒤 해시.

- `.as_posix()` **만으로는 Linux digest 가 안 바뀐다** (기존 산출물 무효화 없음).
- **범위 확대는 digest 를 바꾼다** → baseline·half-cell 캐시 무효화. 다만 GO 후
  실행 순서가 이미 `--force` 로 재생성하므로 **감당 가능**.

### CRLF 양성 테스트 (리뷰어 요구)

`tests/test_compare.py:1602-1604` 의 현재 검사는 **존재 확인뿐**이라 불충분:

```python
# 저장소 EOL 정책도 있어야 한다 (clone 시점의 바이트를 고정한다)
ga = Path(__file__).resolve().parent.parent / ".gitattributes"
assert ga.is_file() and "eol=lf" in ga.read_text(encoding="utf-8")
```

→ **source tree 안 CRLF 파일 수 == 0** 을 단언하는 양성 테스트를 추가한다.
(바로 다음 함수가 `def test_bundle_restores_and_validates_in_isolated_root(tmp_path):`)

### 호출처 인벤토리 (다시 grep 하지 말 것)

production:

```
src/grid.py:258, :354        "source_digest": source_digest(),
src/fitting.py:540           _src0 = source_digest()
src/fitting.py:868           "source_digest": source_digest(),
src/fitting.py:1021          "source_digest_changed_during_run": bool(_src0 != source_digest()),
src/baseline.py:205          "source_digest": source_digest(),
src/io.py:132                정의
src/io.py:1280, :1282        validator 재계산 (★ F72 주석은 :1273)
src/halfcell.py:288, :291, :306, :377, :378
scripts/smoke_e2e.sh:193     ok = (m.get("source_digest") == source_digest() ...
```

tests:

```
tests/test_fitting.py:441, 529, 545, 632, 641, 887, 892, 1372, 1377, 1393,
                      1529, 1542, 1546, 1547, 1655, 1664, 1809, 1836
tests/test_compare.py:815, 839, 868, 873, 907, 1037, 1704
```

대부분 `source_digest()` 를 **live 호출**이라 범위 확대로 안 깨진다.
`"stale0000000"` 하드코딩(`test_fitting.py:1377`, `:1542`)은 의도적 fail-closed fixture.

### 함께 고칠 문서

- root `CLAUDE.md` 하드룰 3 의 RUN_SCOPE 문구
- 스크래치패드 `review_request_14.md` — "`source_digest` 가 RUN_SCOPE 6개를 모두 본다"는
  **틀린 주장**이 들어가 있다.

---

## 2. 발견 1 — noise family 교차 invariant

### 요구 규칙

family 키 = `(lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type)`.

1. 각 family 는 noise `{0, 0.001, 0.005}` 를 **정확히 한 번씩** 가진다.
2. family 가 observed / failed 로 **쪼개지면 실패**.
3. observed family 안 `q_mah` 최대 편차 ≤ **1e-6 mAh**.
4. x 정렬 후 `v_pe`·`v_ne`·`v_full` pointwise 최대 편차 ≤ **1e-10 V**.
   (실측 2-worker 샘플에서 셋 다 정확히 0)

노이즈는 solve **이후에만** 얹히므로(`src/grid.py:191`
`v_noisy = add_noise(curves["v_full"], cond.noise, cond.seed)`) clean truth 는 family
안에서 같아야 한다.

### 구조 사실 (io.py 재독 방지)

- `_verify_observed_curves(curves_path, spec)` = `src/io.py:613-772`.
  **모든 검사가 `groupby("cond_id", sort=True)`(:667) 루프 안**에 있고
  **cross-condition state 가 없다** → family 검사는 루프 **뒤의 새 pass** 여야 한다.
- 기존 체크 키: `관측조건_단일성`(734) · `관측조건_ID결합`(737) · `관측조건_행수`(741) ·
  `관측_x_norm_공통격자`(745), 그리고 `if phys is not None:`(750) 안에
  `관측_q_mah`(751) · `관측_전압_유한`(756) · `관측_전압_정합`(760) ·
  `관측_noise_재현`(764) · `관측_protocol`(768).
- `_COND_FIELDS` = 602-605, `_PHYS_COLS` = 607-610.
- `_verify_failed_reasons(d, spec, ds)` = docstring 775 / body 795 / 끝 ~856.
- `validate_curves_provenance(curves_dir, repo_root=None)` = `:859`.
- **호출 순서 문제** (`:975-1055`):

```
1019  checks.update(_verify_observed_curves(cp, spec))   ← observed 검증 호출
1020  fail_ids = load_failed(d)                          ← failed ID 는 그 뒤에 로드
1021-37  실패목록_존재 / 실패목록_재해시 / 조건집합_ID분할
1046-7   if n_fail: checks.update(_verify_failed_reasons(d, spec, _ds))
```

→ family-split 규칙(2번)을 쓰려면 **`load_failed(d)` 를 1019 위로 끌어올려 verifier
시그니처를 넓히거나**, 1020 뒤에 **별도 결합 verifier** 를 둔다. (후자가 기존 검사에
손을 덜 댄다)

### 기대 noise 집합의 출처 (하드코딩 금지)

서명된 manifest 에 이미 있다: `src/grid.py:566`
`"noise": sorted({float(c.noise) for c in conditions})`.
설정 쪽은 `configs/grid_fine.yaml:10 noise: [0.0, 0.001, 0.005]`, `:11 noise_seed: 42`,
`:2` 주석 "조건 수: 11 × 11 × 11 × noise 3 = 3,993". `configs/base.yaml` 엔 `noise` 키 없음.
seed 유도: `src/grid.py:105-111`
`seed = noise_seed + int(hashlib.sha1(key.encode()).hexdigest()[:6], 16)`.

### fixture 영향 (예상되는 RED, 정상 신호)

- `_tiny_curves` = `tests/test_fitting.py:393` — **`noise=0.0` 만** 만든다. family 요구를
  넣으면 이걸 쓰는 테스트 다수가 깨진다. 저장소 규칙상 **안 깨지면 fixture 가 위조 통로**.
- `sign_producer(out_dir, df, n_infeasible=0)` = `tests/test_fitting.py:423-550`,
  약 40곳에서 사용. 기본값 `lam_pe_type="de"`, `lam_ne_type="de"`, `noise=0.0`;
  `Condition(..., seed=42+i)`; 공통 `linspace(0,1,n_interp)` 격자 강제;
  `v_pe = v_full + v_ne` 강제; `q_mah=4000.0`; `protocol="charge_first"`;
  spec 에 `grid_sig_version: 4`, `condition_ids_sha256`, `n_conditions_intended`,
  `postprocess {n_interp, n_trim}`, `discharged_state`, `replay_recipe {baseline, guards}`,
  `effective_solver`, `source_digest()`, `env_fingerprint()` 를 넣고
  `sha1(json.dumps(spec, sort_keys=True, default=str))[:12]` 로 서명.

### 새 회귀 테스트 3종

1. 조건별로는 내부 정합하지만 **family 간 clean curve 가 다른** 경우 → 실패해야 함
   (리뷰어 반례: noise-0 은 `q=4000`/offset 4 V, noise-0.005 는 `q=2000`/offset 3 V —
   **현재 모든 검사를 통과한다**).
2. 한 noise level 만 단독 실패 → family split 실패해야 함.
3. noise level 하나 누락 → 실패해야 함.

검증 명령: `python -m pytest tests/test_fitting.py -q -k "observed or noise_family"`

---

## 3. 나머지 발견 좌표

| # | 파일:줄 | 요지 |
|---|---|---|
| 3 | `tools/check_sweep_consistency.py:184-215` | `condition_ids_sha256` 누락/빈값 → 즉시 fail. 양 endpoint digest 가 서명 digest 와 같아야. 최상위 verdict 에 포함. 반례: 54조건을 같은 27조건으로 줄이고 `n_conditions=27` + digest 없음 → **일치로 통과** |
| 4 | `src/weight_sweep.py:52-90`, `:350-355` | `build_weight_objectives([0, 0.001])` 가 키 `wdqdv_0.00` 하나로 붕괴하며 **w=0 seed 를 소리없이 삭제**. finite·nonnegative 요구, 이름 1:1 요구, 충돌 시 fail, 안정 index 또는 충분한 precision |
| 5 | `src/io.py:907-937` (`replay_recipe_schema`) | `_badg` 가 **아무 guard 키나 허용하고 bool 도 통과**. canonical 3-key 로: unknown 키·bool 거부, 없는 known 키는 코드 기본값으로 채운 뒤 서명. 범위 `max_mode_value: 0 ≤ v < 1`, `max_porosity: 0 < v ≤ 1`, `min_vf: 0 < v < 1`. (같은 함수 892-901: `grid_sig_version == 4`, `effective_solver_identity` 는 `effective_class`·`pybamm`·non-None `pybammsolvers`·non-None `casadi` 요구) |
| 6 | `tools/make_results.py:1081-1108` | reproduce 명령이 manifest 의 producer 경로를 grid `--out`/fit `--in` 으로, 현재 `in_dir` 을 fit `--out` 으로. `run_spec.v_col == "v_full"` 이면 `--clean` 출력. 결론 2 는 `RESULTS_PAIRED_FIXED5.md` 를 명시 인용 |
| 7 | `scripts/archive_results.sh:170-175` | 첫 `out → old` 이동에서 fail-closed — 후보 제거하고 `n_bad` 에 계상 |
| 8 | `scripts/archive_results.sh:229-241`, `:283-290` | 계산 시작 커밋(`run_spec.git_commit` / `start_provenance.git_commit`)을 `source_commit` 으로 기록. "다음 commit" 문구 오류 수정 |
| — | `src/modes.py:144-147` | 리뷰 지적 위치 (미착수) |
| — | `src/runner.py:40-43, 75, 115` | 확인 결과 **정상** — 손대지 않는다 |

---

## 4. GO 이후 실행 순서 (변경 금지)

```
python -m pytest tests -q
python -m src.baseline --config configs/grid_fine.yaml --force
python -m src.halfcell --config configs/base.yaml --method ocp --force --verify
./scripts/smoke_e2e.sh
./run.sh --mode grid --config configs/grid_fine.yaml --nproc 32 --out results/grid_curves_v4
```

fitting 전에 invariant 요약을 저장한다:
1,331 family × 3 · observed 1,023 × 3 / failed 308 × 3 · family 별 noise 집합 ==
{0, 0.001, 0.005} · max Δq_mah ≤ 1e-6 mAh · max Δv_pe/Δv_ne/Δv_full ≤ 1e-10 V ·
validator JSON `ok == true` · worker effective solver identity **unique == 1**.

측정된 런타임 identity: `IDAKLUSolver` · PyBaMM `26.7.1.0` · pybammsolvers `0.9.0` ·
CasADi `3.7.2`.

---

## 5. 리뷰어의 발견 인정 기준

1. 지금 계획된 기본 설정에서 **활성**일 것
2. 정상 실행 결함만으로 결론 1~3 의 수치나 인용가능성을 바꿀 수 있을 것
3. 기존 validator/smoke 가 못 잡는다는 것을 **측정 또는 명확한 실행 경로**로 보일 것

14차 scope 는 과학적 타당성 / 수치 재현성 / 실행 일관성이며 **보안(경로 탈출·위조·
우회)은 명시적으로 제외**됐다.
