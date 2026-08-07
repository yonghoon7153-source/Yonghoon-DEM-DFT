#!/usr/bin/env bash
# =============================================================================
#  archive_results.sh — 재생성 비용이 큰 산출물만 저장소에 남긴다
#
#  사용:
#    ./scripts/archive_results.sh                      # 기본 3개 실행 보관
#    ./scripts/archive_results.sh results/halfcell_v1  # 특정 실행만
#
#  왜 필요한가
#  ───────────
#  .gitignore가 results/ 와 *.parquet 을 통째로 제외한다. 용량 때문에 맞는
#  기본값이지만, 그 결과 **계산 결과가 서버에만 존재**하게 된다.
#  V100 컨테이너가 회수되면 fitting 14시간이 사라진다.
#
#  무엇을 남기고 무엇을 버리는가 — 기준은 "재생성 비용"이다.
#
#    fits.parquet          ★ 남긴다. 조건당 4~10초 × 3,069조건 = 시간 단위.
#                            이것만 있으면 score/hessian/report는 몇 초다
#    manifest.yaml         ★ 남긴다. 어떤 커밋·설정에서 나왔는지의 근거
#    *_summary.yaml        ★ 남긴다. 작고, 보고서가 읽는다
#    objective_comparison  ★ 남긴다. 최종 비교표
#    figures/*.png         ★ 남긴다. 작고 보고에 바로 쓴다
#
#    curves.parquet        버린다. 19 MB이고 재생성이 5~8분이다
#    degeneracy_map        버린다. fits에서 몇 초면 다시 나온다
#    chunks/ fit_chunks/   버린다. 병합 결과가 fits.parquet에 있다
#    completed.jsonl       버린다. resume 상태일 뿐
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DEST="artifacts"
RUNS=("$@")
if [[ ${#RUNS[@]} -eq 0 ]]; then
  RUNS=(results/grid_fine_v1 results/grid_fine_v2 results/halfcell_v1)
fi

mkdir -p "$DEST"
total=0

for run in "${RUNS[@]}"; do
  name="$(basename "$run")"
  if [[ ! -d "$run" ]]; then
    printf '건너뜀 (없음): %s\n' "$run"
    continue
  fi
  out="$DEST/$name"
  mkdir -p "$out"

  n=0
  for f in fits.parquet manifest.yaml degeneracy_summary.yaml \
           objective_comparison.yaml objective_comparison.csv \
           objective_comparison_by_noise.csv weight_sweep.yaml \
           weight_sweep_summary.csv; do
    [[ -f "$run/$f" ]] && { cp -p "$run/$f" "$out/"; n=$((n+1)); }
  done
  # hessian은 목적함수마다 파일이 따로다
  for f in "$run"/hessian_*.parquet; do
    [[ -f "$f" ]] && { cp -p "$f" "$out/"; n=$((n+1)); }
  done
  # 가중치 sweep은 하위 디렉터리에 있다
  if [[ -d "$run/wsweep" ]]; then
    mkdir -p "$out/wsweep"
    for f in "$run"/wsweep/weight_sweep*.{yaml,csv} "$run"/wsweep/fits.parquet; do
      [[ -f "$f" ]] && { cp -p "$f" "$out/wsweep/"; n=$((n+1)); }
    done
  fi
  if [[ -d "$run/figures" ]]; then
    mkdir -p "$out/figures"
    cp -p "$run"/figures/*.png "$out/figures/" 2>/dev/null && \
      n=$((n + $(ls -1 "$run"/figures/*.png 2>/dev/null | wc -l)))
  fi

  sz=$(du -sh "$out" | cut -f1)
  printf '%-28s 파일 %2d개  %s\n' "$name" "$n" "$sz"
  total=$((total+n))
done

printf '\n합계 %d개 파일, %s\n' "$total" "$(du -sh "$DEST" | cut -f1)"
cat <<'EOF'

다음:
  git add artifacts && git commit -m "chore(artifacts): 계산 결과 보관" && git push

복원하려면 (fits.parquet만 있으면 채점 이후는 전부 재생성된다):
  mkdir -p results/grid_fine_v2
  cp artifacts/grid_fine_v2/fits.parquet results/grid_fine_v2/
  ./run.sh --mode grid --config configs/grid_fine.yaml --nproc 32 --out results/grid_fine_v2  # curves 재생성 5~8분
  ./run.sh --mode score --in results/grid_fine_v2
EOF
