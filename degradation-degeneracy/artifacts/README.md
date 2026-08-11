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

## 지금 들어 있는 것의 상태 (2026-08-07)

| 묶음 | provenance 검증 | 비고 |
|---|---|---|
| `grid_fine_v1` | ❌ 불가 | F51 이전 실행 — 시작 기록(`manifest_start.yaml`)이 없다 |
| `grid_fine_v2` | ❌ 불가 | 〃 |
| `halfcell_v1` | ❌ 불가 | 〃 + dirty worktree 실행 |

세 묶음 모두 **인용 가능한 상태가 아니다.** 이유는 두 가지다.

1. **실행 자체가 옛 파이프라인이다.** F26(`p_ini` 버그) · F51(시작 provenance) ·
   F58(half-cell 캐시 봉인) 이전이라, 재검증에 필요한 기록이 애초에 없다.
2. **묶는 방식도 옛 기준이었다.** 초판 `archive_results.sh` 는 "재생성 비용"만
   보고 `curves.parquet` 을 버렸는데, 검증기는 봉인된 입력을 **다시 해시**한다
   (F56). 재생성한 curves는 바이트가 달라 digest가 맞지 않는다 —
   재생성으로 대체할 수 없다.

즉 이 세 묶음은 **이력**으로만 남긴다. 논문·보고서 인용은 F55~F62 적용 후의
재실행 산출물로만 한다. `docs/RESULTS.md` 상단 배너가 이 판정을 자동으로 찍는다.

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
