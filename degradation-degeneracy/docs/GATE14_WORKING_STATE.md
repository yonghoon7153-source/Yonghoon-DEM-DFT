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
| 2 | `source_digest()` 경로 정규화 (POSIX) + RUN_SCOPE 정합 | **완료** — §1.9 참조 (RED 5건 → GREEN, 286 passed) |
| 1 | noise family 교차 invariant (`_verify_observed_curves`) | **완료** — §2.9 참조 (RED 3건 → GREEN, 289 passed) |
| 3 | sweep checker fail-closed (`tools/check_sweep_consistency.py`) | **완료** — §3.1 (RED 1건 → GREEN) |
| 4 | custom `w_grid` 충돌 (`src/weight_sweep.py`) | **완료** — §3.2 (RED 2건 → GREEN) |
| 5 | guards → canonical 3-key recipe (`src/modes.py`·`io.py`·`grid.py`) | **완료** — §3.3 (RED 2건 → GREEN) |
| 6 | report reproduce command (`tools/make_results.py`) | **완료** — §3.4 (RED 4건 → GREEN) |
| 7·8 | archive fail-closed / source_commit (`scripts/archive_results.sh`) | **완료** — §3.5 (smoke 반례 실측) |

**7건 전부 닫혔다.** 전체 테스트 298 passed · strict smoke 통과 (exit 0).

1·2 는 grid v4 생성 전 필수 blocker 였다. 3~6 은 같은 pre-run 커밋에, 7·8 은 archive 경로에 함께 넣었다.

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

- root `CLAUDE.md` 하드룰 3 의 RUN_SCOPE 문구 — **수정 완료**. `RUN_SCOPE` 7개를
  그대로 적고, digest 와 dirty 판정이 같은 목록을 본다고 명시.
- 스크래치패드 `review_request_14.md` — "`source_digest` 가 RUN_SCOPE 6개를 모두 본다"는
  **틀린 주장**이 들어가 있다. 이미 리뷰어에게 보낸 문서라 소급 수정하지 않고
  **15차 요청문에서 정정**한다 (보낸 기록을 고쳐 쓰지 않는다).
- `docs/08_REVIEW_RESPONSE.md:605` 의 "(src/tools/configs 전체 내용 해시)" 는
  **그 시점 F49 의 사실 기록**이라 그대로 둔다. 범위 확대는 14차 항목으로 적는다.

### 1.9 구현 결과 (실측)

`src/io.py`:

- `from pathlib import Path, PurePath` (import 확장)
- `_digest_path_key(rel) -> bytes` — `PurePath(rel).as_posix().encode("utf-8")`
- `_digest_files(root=None, scope=RUN_SCOPE)` — `(POSIX 키, 경로)` 를 **키 기준
  전역 정렬**해서 반환. 항목이 `/` 로 끝나면 `rglob`, 아니면 `root.glob(이름)`.
  `__pycache__`·`.pyc`·`.pyo` 제외는 그대로.
- `source_digest(root=None, scope=RUN_SCOPE)` — 시그니처가 `dirs=` → `scope=` 로
  바뀌었다. 인자를 주는 호출자는 `src/io.py:1280,1282` 의 `source_digest(root)`
  뿐이라(positional) 영향 없음.

**정렬을 전역으로 한 이유**: 항목별로 정렬하면 `RUN_SCOPE` 나열 순서를 바꾸는
것만으로 digest 가 변한다. 전역 정렬이면 목록의 순서는 무관하다.

**`git_info` 와의 유일한 차이**: dirty 판정은 prefix 매칭(`startswith`)이라
`run.sh.bak` 같은 파생 이름도 세지만, digest 는 이름이 정확히 같은 파일만 센다.
digest = "이 파일들의 내용", dirty = "건드렸는가" 이므로 좁은 쪽이 안전하다.

정렬 divergence 의 **실제 원인은 구분자가 아니라 대소문자 접기**였다 (설계 당시
가정이 틀렸다). `PurePath` 비교는 부분 tuple 비교라 구분자에 안 흔들리지만,
Windows flavour 는 각 부분을 소문자로 접는다 — 실측:

```
sorted(PureWindowsPath) → ['src\apple.py', 'src\Zebra.py']
sorted(PurePosixPath)   → ['src/Zebra.py', 'src/apple.py']
str(PureWindowsPath('src/io.py')) → 'src\io.py'
```

구분자는 **해시 키**를 갈라놓고(`str()`), 대소문자 접기는 **정렬**을 갈라놓는다.
둘 다 `_digest_path_key` 로 닫힌다.

**digest 실측 변화** (`root = degradation-degeneracy/`):

| 범위 | 값 | 파일 수 |
|---|---|---|
| 옛 구현 `dirs=("src","tools","configs")` | `a27732aa85181c7d` | 33 |
| 새 구현·좁은 범위 (전역 정렬만 적용) | `f8237e509f0cc457` | 33 |
| 새 구현·`RUN_SCOPE` 전체 | **`e4b10de012b23ff6`** | 46 |

같은 33개 파일인데도 값이 바뀐다 — 전역 정렬로 `configs/` 가 `src/` 앞에 오기
때문이다. 범위 확대로 들어온 13개:
`requirements.txt`, `requirements-gpu.txt`, `run.sh`, `scripts/` 10개
(`archive_results.sh` `bg.sh` `check_run.py` `diagnose_objective.py`
`recompute_lli.py` `setup_env.sh` `smoke_e2e.sh` `verify_env.py`
`watch_fit.sh` `watch_grid.sh`).

→ **기존 baseline·half-cell 캐시는 무효화된다.** GO 후 실행 순서가 이미
`--force` 로 재생성하므로 감당 가능 (§4).

### 1.10 회귀 테스트 (`tests/test_io_bookkeeping.py`)

RED 5건을 먼저 확인하고(`ImportError: cannot import name '_digest_files'` 외)
고친 뒤 GREEN.

| 테스트 | 무엇을 고정하나 |
|---|---|
| `test_digest_path_key_is_posix_on_every_os` | `PureWindowsPath("src/io.py")` → `b"src/io.py"` |
| `test_digest_order_is_posix_order_not_os_path_order` | 대소문자 접기로 갈리는 정렬을 POSIX 바이트 키로 고정 |
| `test_digest_files_sorts_by_posix_key` | 수집 순서가 `Zebra.py` → `apple.py` |
| `test_digest_scope_matches_run_scope` | digest 범위 == `RUN_SCOPE` 전 항목 |
| `test_digest_sources_have_no_crlf` | worktree 바이트에 CRLF 0건 (정책이 아니라 내용) |

마지막 것이 리뷰어의 세 번째 digest(`808f19ea5556d018`, CRLF 잔존 Windows
worktree)를 겨냥한 **positive** 검사다. 기존
`tests/test_compare.py:1604-1605` 는 `.gitattributes` 에 `eol=lf` 가 **있는지만**
봤다 — 정책 존재는 준수의 증거가 아니다.

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

### 2.9 구현 결과 (실측)

**RED 증거** — 리뷰어 반례를 그대로 재현했다. 같은 truth 를 noise=0.0 은
`q=4000`·절편 4.2, noise=0.005 는 `q=2000`·절편 3.2 로 만들면:

```
validate_curves_provenance → ok=True, fail=[], 29개 검사 전부 통과
```

분할 반례(진짜 불능 family 를 관측/실패로 가름)도 `fail=[]` 였다 — 즉
`실패사유_불능재검`·`실패목록_ID결합`·관측∪실패 해시가 **모두 참인 채로** 통과한다.
기존 검사와 겹치지 않는다는 뜻이고, 그 사실을 테스트에 함께 고정했다.

**구현** — `src/io.py` 에 `_verify_noise_families(curves_path, d, man)` 를
**별도 pass** 로 추가하고 `validate_curves_provenance` 에서
`_verify_observed_curves` 바로 뒤에 호출한다. 기존 `groupby("cond_id")` 루프는
건드리지 않았다 (`load_failed(d)` 를 앞으로 끌어올릴 필요도 없었다 — 새 함수가
`failed.csv` 를 직접 읽는다).

| 검사 키 | 내용 |
|---|---|
| `관측_noise_family_구성` | family 마다 noise 집합이 같고 중복 없음 |
| `관측_noise_family_분할` | 한 family 가 관측/실패로 갈리지 않음 |
| `관측_noise_family_q` | 계열 안 `q_mah` 편차 ≤ `1e-6` mAh |
| `관측_noise_family_곡선` | 계열 안 clean 곡선 편차 ≤ `1e-10` V |

보조: `_FAMILY_FIELDS`(noise·seed 를 뺀 5필드), `_family_key()`(float 은 1e-12
자리 반올림 — 축 간격 0.02 이므로 서로 다른 축 값을 합치지 않는다),
`_FAMILY_Q_TOL`·`_FAMILY_V_TOL`.

기대 noise 집합은 **하드코딩하지 않는다**: manifest 의 `effective_axes.noise`
(실제 조건에서 유도된 축, `src/grid.py:562-567`)를 쓰고, 없으면 관측∪실패에서
유도한다. 전역 축은 서명된 `condition_ids_sha256` 이 이미 고정하므로 여기서
보는 것은 **family 마다 같은가**이다.

### 2.10 fixture 감사 — 기존 테스트가 하나도 안 깨졌다

`_tiny_curves` 는 `noise=0.0` 하나만 만든다 → family 마다 원소가 1개 →
새 검사 4종이 **전부 vacuous**. 그래서 286 → 289 로 신규 3건만 늘고 기존은
그대로다. 이 저장소 규칙대로 이건 건강 신호가 아니라 **fixture 가 이 축을 아예
못 태운다**는 신호다. 두 가지로 대응했다:

1. `tests/test_fitting.py` 에 `_noise_family_curves(out_dir, specs, ...)` 를
   따로 뒀다 — `(lli, lam_pe, lam_ne, noise, q_mah, 절편)` 을 직접 지정한다.
2. **smoke 의 noise 축을 `0` → `0,0.005` 로 올렸다** (`scripts/smoke_e2e.sh`).
   1수준이면 실제 파이프라인에서도 검사가 한 번도 실행되지 않은 채 10시간짜리
   본 실행에 들어간다. smoke 는 새 검사 4종의 **존재**뿐 아니라
   `effective_axes.noise` 가 2수준 이상인지도 확인해 **vacuous 통과를 거부**한다.

실측 (커밋 `274dd2d4`):

```
python -m pytest tests -q          → 289 passed (3m02s)
./scripts/smoke_e2e.sh             → 통과 (3m26s)
  ✅ producer 독립 검증 (F74): 통과 (실패라벨 재검 + noise 계열 2수준 교차)
  ✅ 12조건 × 2목적함수   ← 6조건에서 2배 (noise 2수준)
```

`scripts/` 가 이제 RUN_SCOPE 안이므로 smoke 수정은 `source_digest` 를 바꾼다
(발견 2 의 범위 확대 결과). 본 실행 전이라 문제 없다.

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

### 3.1 발견 3 구현 결과 — sweep checker (실측)

**RED**: 본 실행 조건을 두 끝점 모두 **같은 절반**으로 줄이고 `n_conditions` 를
그 수로 맞춘 뒤 `condition_ids_sha256` 를 지우면 `run_check(...)["일치"] == True`.
조건 수도 맞고(`len(sweep_ids) == expected`), 끝점끼리 집합도 같고
(`끝점_조건집합_동일`), sweep 조건이 전부 본 실행에 있어(`missing_in_main` 비어
있음) 아무 검사도 안 걸린다.

`n_conditions` 부재는 이미 fail-closed 였는데(13차 발견 2) **더 강한 쪽**인
digest 부재가 빠져 있었다. 조건 "수" 로는 집합이 고정되지 않는다.

**수정**: digest 부재·계산 불가·불일치 세 경우를 모두 fail-closed 로 만들고
(`_fail_all()` 로 공통화), `끝점_서명digest_일치` 를 최상위 판정 conjunction 에
명시적으로 넣었다. 빈 문자열도 "없음" 과 같게 다룬다. CLI 요약에 무엇으로
조건집합을 고정했는지 한 줄 찍는다.

회귀: `test_sweep_checker_requires_signed_condition_digest`

### 3.2 발견 4 구현 결과 — `build_weight_objectives` (실측)

**RED** (셋 다 그대로 통과했다):

```
build_weight_objectives([0, 0.001])
  → {'wdqdv_0.00': {'w_pocv': 1.0, 'w_dvdq': 1.0, 'w_dqdv': 0.001}}
build_weight_objectives([0, nan])  → 'wdqdv_nan' 생성
build_weight_objectives([0, -0.5]) → 'wdqdv_-0.50' 생성
```

이름이 `f"wdqdv_{w:.2f}"` 라 소수 셋째 자리부터 충돌한다. 두 가지가 한꺼번에
깨진다:

1. dict 가 뒤엣것으로 덮어써 **w=0 seed 제공자가 사라진다.** `any(w == 0.0)` 는
   참이라 `_seed` 도 안 끼워진다 → 아무도 warm start 를 못 받는다. F20d 가 잰
   "dQ/dV 항은 좋은 초기값 없이는 optimizer 가 못 푼다" 상태로 되돌아간다.
2. 남은 하나는 이름이 `wdqdv_0.00` 인데 실제 가중치가 0.001 이다.
   `check_sweep_consistency` 의 `DEFAULT_PAIRS` 가 이 이름을 본 실행의
   `pocv_dvdq`(w_dqdv=0) 와 짝지어 "정의가 같다" 며 대조한다.

**수정**: 이름 형식을 바꾸면 기존 끝점 짝과 산출물이 깨지므로 **충돌을 거부**한다
(0.01 이상 간격 안내 포함). 비유한·음수·빈 격자는 이름 짓기 **전에** 거부한다.
`w_pocv`·`w_dvdq` 도 같이 검증한다.

회귀: `test_build_weight_objectives_rejects_colliding_names`,
`test_build_weight_objectives_rejects_invalid_weights`

### 3.3 발견 5 구현 결과 — canonical guards (실측)

**RED**: 옛 검사는 "스칼라인가" 뿐이라 다음이 전부 `replay_recipe_schema` 를
통과했다 — 모르는 키(`bogus`), **bool**, 키 누락, 빈 dict, 범위 밖 값
(`max_mode_value: 5.0`/`1.0`, `max_porosity: 0`, `min_vf: -1e-4`/`1.0`).

bool 이 특히 나쁘다: `max_mode_value: True` → `float(True) = 1.0` → 불능 판정이
`[0, 0.9]` 에서 `[0, 1.0]` 로 넓어진다. 불능이던 조건이 풀리고, 그건 인용
모집단의 **분모**가 달라진다는 뜻이다. 키 누락도 재검이 조용히 코드 기본값으로
도는데 서명은 "이 recipe 로 재검했다" 고 말한다.

`validate_config` 는 guards 를 아예 보지 않는다 (실측: `src/config.py` 에 guards
언급 0건). 그래서 관문이 여기뿐이다.

**수정** — `src/modes.py` 를 정본으로:

| 이름 | 내용 |
|---|---|
| `GUARD_DEFAULTS` | `max_mode_value 0.9 · max_porosity 0.95 · min_vf 1e-4` |
| `GUARD_RANGES` | `0 ≤ v < 1` · `0 < v ≤ 1` · `0 < v < 1` |
| `canonical_guards(g)` | 모르는 키 거부 · bool/비유한/범위 밖 거부 · 빠진 키 채움 |

- `build_overrides` 가 인라인 리터럴 대신 이걸 쓴다
- `src/grid.py` 가 **서명 전에** `canonical_guards(cfg.get("guards"))` 로 3키를
  채워 봉인한다 — config 오타면 10시간 뒤가 아니라 거기서 죽는다
- `src/io.py` validator 가 3키 정확 일치 + bool 불가 + 범위를 강제한다

회귀: `test_replay_recipe_guards_must_be_canonical`(9케이스 + 경계 2건),
`test_canonical_guards_fills_and_rejects`

`sign_producer(..., guards=...)` / `_tiny_curves(..., guards=...)` 파라미터를
추가해 fixture 가 이 축을 태울 수 있게 했다.

### 3.4 발견 6 구현 결과 — 재현 명령 (실측)

**RED**: 재현 명령이 fit 실행 디렉터리 하나로 두 단계를 다 가리켰다.

```
./run.sh --mode grid ... --out <fit 디렉터리>     ← 곡선을 여기 만들라고
./run.sh --mode fit   --in <fit 디렉터리> ...      ← 거기서 읽으라고
```

실제 실행은 `--out <producer>` 로 곡선을 만들고 `--in <producer> --out <fit>` 으로
fitting 했다. 그대로 따라 하면 다른 배치가 되고, 최악의 경우 기존 fit 산출물
위에 곡선을 덮어쓴다. producer 경로는 fit manifest 의 `input` 에 있다.

**수정**:

- grid `--out` / fit `--in` = `manifest["input"]`, fit `--out` = 현재 `in_dir`
- `run_spec.v_col`(또는 `target_column`) `== "v_full"` 이면 `--clean` 추가 —
  없으면 재현 실행이 `v_full_noisy` 로 fitting 해 다른 숫자를 낸다
- producer 경로가 없으면 **실행 가능한 명령을 만들지 않는다**. 주석으로 이유만
  남긴다 (실행 가능한 틀린 명령이 가장 나쁘다)
- 기본(비대칭) 보고서의 목적함수 비교에 `PAIRED_RESULTS_DOC`
  (`docs/RESULTS_PAIRED_FIXED5.md`) 를 **명시 인용**한다. paired 문서에만 경고를
  두면 기본 문서를 먼저 여는 사람에게는 안 보인다 — 경고는 **읽히는 쪽**에.
  paired 문서 자신은 자기를 인용하라고 하지 않는다(그 사실도 테스트로 고정 —
  안 그러면 첫 단언이 무조건 통과하는 vacuous 검사가 된다).

회귀 4건: `..._uses_producer_path`, `..._emits_clean_flag`,
`..._fails_closed_without_producer`, `test_default_results_points_objective_comparison_to_paired_doc`

### 3.5 발견 7·8 구현 결과 — archive (실측 반례)

**발견 7 RED — 진짜 반례를 측정했다.** PATH 앞에 실패하는 `mv` shim(목적지가
`.previous_*` 일 때만 실패)을 끼우고, smoke 가 만든 **진짜 묶음**에 대해
수정 전/후 스크립트를 같은 조건으로 돌렸다:

| 스크립트 | exit | 기존 봉인 유지 | 중첩 |
|---|---|---|---|
| **수정 전** | **0 — 성공이라고 보고** | yes | **`.candidate_grid_fit`** |
| 수정 후 | 1 | yes | 없음 |

첫 `mv "$out" "$old"` 가 실패해도 결과를 안 봐서, `$out` 이 남은 채 다음 줄의
`mv "$cand" "$out"` 이 돌았다. mv 는 목적지가 **존재하는 디렉터리**면 덮어쓰지
않고 그 안으로 넣으므로 `$out/.candidate_$name` 중첩이 생기고, mv 자체는
성공하니 승격 성공으로 계상되고 스크립트는 **exit 0** 으로 끝난다. 파이프라인은
보관이 성공했다고 믿는다. 12차에서 "중단돼도 둘 중 하나는 남는다" 로 고친
순서인데 그 순서의 첫 단계가 fail-open 이었다.

**발견 8 RED**: smoke 검사를 수정 전 스크립트에 걸면
`❌ source_commit 검사 실패 (14차 발견 8)`. `manifest.yaml` 의 top-level
`git_commit` 은 **기록을 쓴 시점**(계산 종료 후)의 commit 이다.

**수정**: 계산 **시작** 기록을 우선한다 —
fit 은 `manifest.start_provenance.git_commit` → `manifest_start.yaml` →
(fallback) `manifest.git_commit`, grid producer 는
`curves_manifest_start.yaml` → (fallback) `curves_manifest.yaml`. 둘 다 묶음에
동봉된다. 실행 중 코드가 바뀐 실행은 `_주의_실행중_코드변경` 으로 index 에
남긴다. `artifact_index._주의` 의 "다음 commit" 문구도 바로잡았다(바로 위 주석의
순서와 어긋났다).

**smoke 검사에서 내가 만든 masking 통로 2건** (기록해 둔다):

1. `_sealed_before`/`_sealed_after` 를 `sha256sum ... 2>/dev/null` 로만 잡으면
   **둘 다 빈 문자열일 때 "같다"로 통과**한다. 묶음이 아예 없어도 보존된 것처럼
   보인다 → `_sealed_before` 가 비면 전제가 깨진 것으로 보고 실패시킨다.
2. `find "$out" -maxdepth 1 -name '.candidate_*' -o -maxdepth 1 -name "$_NAME"`
   는 시작 디렉터리 자신(basename 이 곧 `$_NAME`)을 매치해 **항상** 중첩으로
   판정했다. `-mindepth 1` + 괄호로 고쳤다.

---

### 3.6 남은 사실 하나 (숨기지 않는다)

발견 3~6 커밋(`c23e9cd7`) **직후 첫 strict smoke 가 1건 실패**했다. 그 실행의
로그를 남기지 않아 **어느 단계였는지 확인하지 못했다.** 이후 같은 커밋에서 6회
연속(그리고 발견 7·8 반영 후 clean 상태에서 다시) 통과했고 재현되지 않았다.
"재시도했더니 통과" 는 이 저장소 기준으로 근거가 아니므로, 원인 미상으로
남긴다는 사실 자체를 15차 요청문에 적는다.

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
