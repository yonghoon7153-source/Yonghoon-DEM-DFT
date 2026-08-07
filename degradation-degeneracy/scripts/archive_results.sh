#!/usr/bin/env bash
# =============================================================================
#  archive_results.sh — 계산 결과를 **외부 clone에서 검증 가능한** 형태로 남긴다
#
#  사용:
#    ./scripts/archive_results.sh                      # 기본 실행 보관
#    ./scripts/archive_results.sh results/halfcell_v3  # 특정 실행만
#
#  왜 필요한가
#  ───────────
#  .gitignore가 results/ 와 *.parquet 을 통째로 제외한다. 용량 때문에 맞는
#  기본값이지만, 그 결과 **계산 결과가 서버에만 존재**하게 된다.
#  V100 컨테이너가 회수되면 fitting 14시간이 사라진다.
#
#  ★ F62 — 무엇을 남길지의 기준이 바뀌었다
#  ───────────────────────────────────────
#  초판의 기준은 "재생성 비용"이었다. 그래서 curves.parquet(재생성 5~8분)을
#  버렸다. 그런데 validate_provenance 는 봉인된 입력을 **다시 해시**한다 (F56).
#  재생성한 curves는 바이트가 달라서 digest가 안 맞는다 — 재생성으로 대체할 수
#  없다. manifest_start.yaml 과 attempts/ 도 마찬가지로 검증기가 디스크에서
#  직접 읽는다 (F57). half-cell 캐시는 .cache/ 가 gitignore라 저장소에 아예 없다.
#
#  즉 기준은 이제 "**clone 한 사람이 이 결과를 검증할 수 있는가**"다.
#  검증에 필요한 것은 비용과 무관하게 전부 남긴다.
#
#    fits.parquet          ★ 조건당 4~10초 × 3,069조건 = 시간 단위
#    manifest.yaml         ★ 서명·run_spec·입력 digest
#    manifest_start.yaml   ★ F57 — 검증기가 디스크에서 읽어 대조한다
#    attempts/*.yaml       ★ F57 — attempt_id 별 시작 기록
#    curves.parquet        ★ F56 — 재생성 불가(바이트가 달라진다). 19 MB지만 남긴다
#    inputs/*_ocp.json     ★ half-cell 캐시. .gitignore 때문에 동봉해야 한다
#    *_summary.yaml, 비교표, figures/*.png    작고 보고서가 읽는다
#
#    degeneracy_map / chunks / completed.jsonl   버린다 (fits에서 재생성)
#
#  복원 — 묶음은 보관 형태이고, 검증은 복원한 뒤에 한다:
#    python -m tools.archive_bundle restore artifacts/halfcell_v3
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
DEST="artifacts"
RUNS=("$@")
if [[ ${#RUNS[@]} -eq 0 ]]; then
  RUNS=(results/grid_fine_v1 results/grid_fine_v2 results/halfcell_v1)
fi

mkdir -p "$DEST"
n_ok=0
n_bad=0

for run in "${RUNS[@]}"; do
  name="$(basename "$run")"
  if [[ ! -d "$run" ]]; then
    printf '건너뜀 (없음): %s\n' "$run"
    continue
  fi
  out="$DEST/$name"

  printf '\n── %s ──\n' "$name"
  "$PY" -m tools.archive_bundle bundle "$run" "$out"

  # 원본 실행이 애초에 인용 가능한 상태였는지도 같이 남긴다.
  # (묶음 자체는 경로가 달라 여기서 검증할 수 없다 — 복원 후에 한다)
  "$PY" - "$run" "$out" <<'PYEOF'
import json, sys
from pathlib import Path
from src.io import validate_provenance
run, out = sys.argv[1], Path(sys.argv[2])
v = validate_provenance(run)
(out / "provenance.json").write_text(
    json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"  원본 provenance: {'통과' if v['ok'] else '실패 — ' + ', '.join(v['fail'][:4])}")
PYEOF

  if "$PY" -m tools.archive_bundle check "$out" | sed 's/^/  /'; then
    n_ok=$((n_ok+1))
  else
    n_bad=$((n_bad+1))
  fi
  printf '  용량 %s\n' "$(du -sh "$out" | cut -f1)"
done

printf '\n검증 가능 %d개, 불완전 %d개, 합계 %s\n' \
  "$n_ok" "$n_bad" "$(du -sh "$DEST" | cut -f1)"
cat <<'EOF'

다음:
  git add artifacts && git commit -m "chore(artifacts): 계산 결과 보관" && git push

clone 한 쪽에서 복원 + 검증:
  python -m tools.archive_bundle restore artifacts/halfcell_v3
  python -c "from src.io import validate_provenance; import json; \
             print(json.dumps(validate_provenance('results/halfcell_v3'), \
             ensure_ascii=False, indent=2))"
  ./run.sh --mode score --in results/halfcell_v3     # 채점 이후는 몇 초다
EOF
