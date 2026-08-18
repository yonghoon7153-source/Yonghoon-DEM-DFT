# artifacts/ — 보관된 계산 결과

`results/` 는 `.gitignore` 에 걸려 있다 (용량). 그래서 fitting 결과가 서버에만
존재하고, 컨테이너가 회수되면 열 시간 단위 계산이 사라진다. 이 디렉터리는
`scripts/archive_results.sh` 가 골라 넣은 **재생성 불가·고비용 산출물**이다.

## 복원

묶음은 보관 형태다. 경로가 원래와 다르므로 **복원한 뒤에** 검증한다.

```bash
python -m tools.archive_bundle restore artifacts/<run>
python -c "from src.io import validate_provenance; import json; \
           print(json.dumps(validate_provenance('results/<run>'), ensure_ascii=False))"
./run.sh --mode score --in results/<run>      # 채점 이후는 몇 초다
```

⚠ **원본 `results/<run>` 이 남아 있는 서버에서는 이 검증이 무의미하다.** restore 가
기존 파일을 만나면(내용이 같으면) 넘어가므로, 검증 대상이 묶음이 아니라 원본이
된다. `scripts/archive_results.sh` 는 보관할 때마다 **빈 임시 root** 에 풀어
거기서 검증한다 (F71). 손으로 확인하려면 같은 방식으로:

```bash
iso=$(mktemp -d)
python -m tools.archive_bundle restore artifacts/<run> --repo-root "$iso"
python -c "import sys; from src.io import validate_provenance; from pathlib import Path; \
           print(validate_provenance(Path('$iso')/'results/<run>', repo_root='$iso'))"
```

## 지금 들어 있는 것 (2026-08-18)

**무엇이 근거인지의 authority 는 `artifact_index.yaml` 이다.** 디스크에 있어도
인덱스에 없으면 근거가 아니다.

### 인덱스에 있는 묶음 — v4.1

| 묶음 | kind | 계산 commit | 상태 |
|---|---|---|---|
| `grid_curves_v4` | grid_producer | `c0f1daa0` | ✅ 검증 통과 |
| `grid_fit_v4` | fit | `c0f1daa0` | ✅ 검증 통과 |
| `halfcell_fit_v4` | fit | `c0f1daa0` | ✅ 검증 통과 |
| `paired_fixed5_v4` | fit | `c0f1daa0` | ✅ 검증 통과 |

`source_commit` 은 **계산을 시작한 코드**의 commit 이다 (보관 시점 HEAD 가
아니다).

#### v4 → v4.1: 파생만 다시 만들었다

17차 발견 1(2%p 경계 부동소수점)로 파생 수치가 바뀌어, **봉인 fits 에서
파생만 재계산해 다시 보관**했다. 재fit 은 없다.

- **raw 파일 변경 0건** — `fits.parquet`·`curves.parquet`·`manifest*.yaml`·
  `attempts/`·`_inputs/`·`wsweep/`·`failed.csv` (payload digest 전수 대조)
- 파생 변경 — `objective_comparison.yaml` 의 `36/98`·`90.0` → `24/66`·`89.09`
  (전체 격자 `34/93`·`3.45`)
- **신규** `analysis_manifest.yaml` — 파생 분석의 provenance. raw 계산
  `manifest.yaml` 과 **분리**한다 (거기에 덧붙이면 후대 분석 코드를 원래
  계산에 거짓 귀속하게 된다)
- `objective_comparison.yaml` 자체에 `_analysis` self-description
  (`schema_version`·`analysis_spec_id`·`fits_sha256`) — 이 파일을 **직접 읽는**
  소비자가 어느 fits 에서 어느 규약으로 나온 값인지 알 수 있어야 한다

파생이 최신 의미를 담는지는 보관 **전에** 게이트가 본다:

```bash
python -m tools.check_derived_fresh results/<run>     # 승격 직전 자동 실행
python -m tools.check_derived_fresh artifacts/<run>   # 보관본 사후 재검사
```

`payload_sha256.yaml` 은 stale bytes 도 충실히 해시한다 — 바이트 무결성은
파생이 최신인지 증명하지 못한다. 그래서 별도 게이트가 필요하다 (18차 발견 6).

### 인덱스 밖 묶음 — **이력**일 뿐이다

| 묶음 | 상태 |
|---|---|
| `grid_fine_v1` | ❌ 검증 불가 — F51 이전 실행, 시작 기록(`manifest_start.yaml`) 없음 |
| `grid_fine_v2` | ❌ 〃 |
| `halfcell_v1` | ❌ 〃 + dirty worktree 실행 |

복원은 되지만 **인용 근거가 아니다.** 이유는 두 가지다.

1. **실행 자체가 옛 파이프라인이다.** F26(`p_ini` 버그) · F51(시작 provenance) ·
   F58(half-cell 캐시 봉인) 이전이라, 재검증에 필요한 기록이 애초에 없다.
2. **묶는 방식도 옛 기준이었다.** 초판 `archive_results.sh` 는 "재생성 비용"만
   보고 `curves.parquet` 을 버렸는데, 검증기는 봉인된 입력을 **다시 해시**한다
   (F56). 재생성한 curves 는 바이트가 달라 digest 가 맞지 않는다 —
   재생성으로 대체할 수 없다.

`docs/RESULTS.md` 상단 배너가 이 판정을 자동으로 찍는다.

## 무엇이 들어가는가

검증 필수 — 하나라도 빠지면 `validate_provenance` 가 깨진다:

- `manifest.yaml` — 서명 · `run_spec` · 입력 digest
- `manifest_start.yaml`, `attempts/manifest_start_<id>.yaml` — 시작 기록 (F57)
- `fits.parquet` — 조건당 4~10초 × 3,069조건
- `curves.parquet` — 19 MB. 재생성 불가(바이트가 달라진다)
- `inputs/*_ocp.json` — half-cell 캐시. `.cache/` 가 gitignore라 동봉해야 한다
- `restore_map.yaml` — 위 `inputs/` 를 원래 경로로 되돌리는 지도
- `provenance.json` — 보관 시점의 원본 실행 검증 결과

보관만 — 재생성되지만 작고 보고서가 읽는다: 요약 yaml, 비교표 csv,
`hessian_*.parquet`, `figures/*.png`, `wsweep/`.

버린다 — `fits.parquet` 에서 몇 초면 다시 나온다: `degeneracy_map.parquet`,
`chunks/`, `fit_chunks/`, `completed.jsonl`.
