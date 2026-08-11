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
set -uo pipefail   # ★ 개별 실행 실패를 집계해야 하므로 -e 는 쓰지 않는다

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
DEST="artifacts"
RUNS=("$@")
if [[ ${#RUNS[@]} -eq 0 ]]; then
  # ★ F71/8-4 — 기본 대상이 옛 v1/v2 여서, 새 실행을 묶으려던 사람이 무심코
  #   실행하면 quarantine 산출물만 다시 묶였다. 현재 pipeline 의 구조를 따른다.
  RUNS=(results/grid_curves_v3 results/grid_fit_v3 results/halfcell_fit_v3)
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

  ok=1
  "$PY" -m tools.archive_bundle check "$out" | sed 's/^/  /' || ok=0

  # ★ F71 — **격리 복원 검증까지 자동으로 한다.** 원본 results/ 가 남아 있는
  #   서버에서 restore→validate 하면 묶음을 전혀 확인하지 않고 원본을 다시
  #   검증할 수 있다 (8-3). 빈 임시 root 에 풀어서 거기서 검증한다.
  # 원래 상대경로 그대로 격리 root 안에 푼다 — 봉인된 입력 경로가 저장소 root
  # 기준이므로 (F65), run_dir 을 임의로 바꾸면 재해시가 어긋난다.
  iso="$(mktemp -d)"
  if "$PY" -m tools.archive_bundle restore "$out" --repo-root "$iso" >/dev/null 2>&1 \
     && "$PY" - "$iso" "$run" <<'PYEOF' | sed 's/^/  /'
import sys
from pathlib import Path
from src.io import validate_provenance
iso, run = Path(sys.argv[1]), sys.argv[2]
v = validate_provenance(iso / run, repo_root=iso)
print(f"격리 복원 검증: {'통과' if v['ok'] else '실패 — ' + ', '.join(v['fail'][:4])}")
sys.exit(0 if v["ok"] else 1)
PYEOF
  then :; else ok=0; echo "  격리 복원 검증 실패"; fi
  rm -rf "$iso"

  if [[ "$ok" == "1" ]]; then n_ok=$((n_ok+1)); else n_bad=$((n_bad+1)); fi
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
  ./run.sh --mode score --in results/halfcell_fit_v3   # 채점 이후는 몇 초다
EOF

# ★ F71/8-4 — 하나라도 불완전하면 nonzero. 조용히 성공하면 CI·스크립트가
#   "보관됐다"고 믿는다.
[[ "$n_bad" -eq 0 ]] || exit 1
