#!/usr/bin/env bash
# 사전 리뷰 — 키트 자체시험 숫자 확인 (리뷰 핀 92e6cda4d · 리포에 쓰지 않음 · -B · TMPDIR = scratch)
# 사용: bash run_selftests.sh <worktree> <outdir> [모듈 ...]
set -u
WT=${1:?worktree}
OUT=${2:?outdir}
shift 2
K=$WT/docs/data/ps45_unload_20261009
mkdir -p "$OUT/tmp" "$OUT/logs"
export TMPDIR=$OUT/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$WT" || exit 9
for spec in "$@"; do
  case "$spec" in
    ul_lib|ul_s3|ul_observers|ul_gates|ul_reader|ul_runner_test) cmd=(python3 -I -B "$K/$spec.py" --selftest); tag=$spec.selftest ;;
    seal_selftest) cmd=(python3 -I -B "$K/seal_kit.py" --selftest); tag=$spec ;;
    seal_check) cmd=(python3 -I -B "$K/seal_kit.py" --check); tag=$spec ;;
    decks_selftest) cmd=(python3 -I -B "$K/make_unload_decks.py" --selftest); tag=$spec ;;
    decks_check) cmd=(python3 -I -B "$K/make_unload_decks.py" --check); tag=$spec ;;
    hist_decks_selftest) cmd=(python3 -I -B "$K/history_test/make_history_decks.py" --selftest); tag=$spec ;;
    hist_decks_check) cmd=(python3 -I -B "$K/history_test/make_history_decks.py" --check); tag=$spec ;;
    hist_read_selftest) cmd=(python3 -I -B "$K/history_test/read_history.py" --selftest); tag=$spec ;;
    *) echo "unknown $spec"; continue ;;
  esac
  t0=$(date +%s.%N)
  nice -n 19 "${cmd[@]}" > "$OUT/logs/$tag.log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  echo "$tag rc=$rc secs=$(python3 -c "print(round($t1-$t0,1))") last=$(tail -1 "$OUT/logs/$tag.log")"
done
