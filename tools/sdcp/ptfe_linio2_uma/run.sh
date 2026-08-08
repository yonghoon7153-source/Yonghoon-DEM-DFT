#!/usr/bin/env bash
# PTFE/LiNiO2 UMA geometry prescreen runner for gabia.
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-check}"
UMA_PY="${UMA_PY:-/data/apps/miniforge3/envs/uma/bin/python3}"
UMA_MODEL="${UMA_MODEL:-uma-s-1p1}"
UMA_TASK="${UMA_TASK:-oc20}"
PACKAGE_COMMIT="UNRECORDED"
if [[ -s "$PACKAGE_DIR/PACKAGE_COMMIT.txt" ]]; then
  IFS= read -r PACKAGE_COMMIT < "$PACKAGE_DIR/PACKAGE_COMMIT.txt"
fi
PACKAGE_TAG="${PACKAGE_COMMIT:0:12}"
[[ "$PACKAGE_COMMIT" == "UNRECORDED" ]] && PACKAGE_TAG="unrecorded"
OUT="${OUT:-/data/work/runs/ptfe_linio2_uma_2026_08_08_${PACKAGE_TAG}}"
RUN_OUT="$OUT/${UMA_MODEL}_${UMA_TASK}"
LOG_DIR="$OUT/logs"
LOCK_FILE="$OUT/.runner.lock"
export UMA_MODEL UMA_TASK
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export HF_HUB_OFFLINE=1

mkdir -p "$RUN_OUT" "$LOG_DIR"
ts(){ printf '[%s] %s\n' "$(date +'%Y-%m-%d %H:%M:%S')" "$*"; }

export PACKAGE_COMMIT
ts "package commit: $PACKAGE_COMMIT"
OUT_COMMIT="$OUT/PACKAGE_COMMIT.txt"
if [[ -e "$OUT_COMMIT" ]]; then
  [[ "$(cat "$OUT_COMMIT")" == "$PACKAGE_COMMIT" ]] || {
    ts "STOP: output directory belongs to a different package commit: $OUT_COMMIT"
    exit 2
  }
else
  printf '%s\n' "$PACKAGE_COMMIT" > "$OUT/.PACKAGE_COMMIT.tmp.$$"
  mv "$OUT/.PACKAGE_COMMIT.tmp.$$" "$OUT_COMMIT"
fi

if ! command -v flock >/dev/null 2>&1; then
  ts "STOP: flock is required; do not run without a duplicate-execution lock."
  exit 2
fi
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  ts "STOP: another PTFE UMA runner holds $LOCK_FILE"
  exit 3
fi

ACTIVE_CHILD_PID=""
stop_child(){
  local sig="${1:-TERM}"
  if [[ -n "$ACTIVE_CHILD_PID" ]] && kill -0 "$ACTIVE_CHILD_PID" 2>/dev/null; then
    kill -"$sig" "$ACTIVE_CHILD_PID" 2>/dev/null || true
    wait "$ACTIVE_CHILD_PID" 2>/dev/null || true
  fi
  ACTIVE_CHILD_PID=""
}
on_signal(){
  ts "signal received; stopping the active Python process"
  stop_child TERM
  exit 130
}
trap on_signal INT TERM HUP

verify_package(){
  cd "$PACKAGE_DIR"
  command -v sha256sum >/dev/null 2>&1 || { ts "STOP: sha256sum not found"; return 1; }
  sha256sum -c PACKAGE_MANIFEST.sha256
}

check_python(){
  [[ -x "$UMA_PY" ]] || { ts "STOP: UMA Python is not executable: $UMA_PY"; return 1; }
  "$UMA_PY" -c 'import sys; assert sys.version_info >= (3,8), sys.version; import ase, numpy, torch, fairchem; print("python", sys.version.split()[0], "ase", ase.__version__, "torch", torch.__version__)'
}

prepare_model_cache_manifest(){
  local cache_dir="${FAIRCHEM_CACHE_DIR:-${HOME}/.cache/fairchem}"
  local manifest="$RUN_OUT/MODEL_CACHE_MANIFEST.sha256"
  local links="$RUN_OUT/MODEL_CACHE_SYMLINKS.tsv"
  [[ -d "$cache_dir" ]] || { ts "STOP: fairchem cache not found: $cache_dir"; return 1; }
  local tmp_manifest="$RUN_OUT/.MODEL_CACHE_MANIFEST.tmp.$$"
  local tmp_links="$RUN_OUT/.MODEL_CACHE_SYMLINKS.tmp.$$"
  find -L "$cache_dir" -type f -print0 | sort -z | xargs -0 sha256sum > "$tmp_manifest"
  [[ -s "$tmp_manifest" ]] || { ts "STOP: no files found in fairchem cache: $cache_dir"; return 1; }
  : > "$tmp_links"
  while IFS= read -r -d '' link; do
    printf '%s\t%s\n' "$link" "$(readlink "$link")" >> "$tmp_links"
  done < <(find "$cache_dir" -type l -print0 | sort -z)
  if [[ -e "$manifest" || -e "$links" ]]; then
    [[ -s "$manifest" && -f "$links" ]] || {
      ts "STOP: incomplete prior model-cache identity files; use a new OUT directory"
      return 1
    }
    cmp -s "$tmp_manifest" "$manifest" || {
      ts "STOP: fairchem cache contents changed; use a new OUT directory"
      return 1
    }
    cmp -s "$tmp_links" "$links" || {
      ts "STOP: fairchem checkpoint symlink mapping changed; use a new OUT directory"
      return 1
    }
    rm -f "$tmp_manifest" "$tmp_links"
  else
    mv "$tmp_manifest" "$manifest"
    mv "$tmp_links" "$links"
  fi
  UMA_WEIGHTS_FINGERPRINT="$({ sha256sum "$manifest"; sha256sum "$links"; } | sha256sum | awk '{print $1}')"
  export UMA_WEIGHTS_FINGERPRINT
  ts "model-cache manifest SHA256: $UMA_WEIGHTS_FINGERPRINT"
}

check_exclusive_gpu(){
  local pw
  pw="$(pgrep -af '[p]w\.x' || true)"
  if [[ -n "$pw" ]]; then
    ts "STOP: pw.x is running. Gabia policy forbids pw.x and UMA at the same time."
    printf '%s\n' "$pw"
    return 1
  fi
  local other
  other="$(pgrep -af '[p]ython.*(fairchem|phaseA_v7c_orient_scan|ptfe_linio2_uma.*/scan\.py)' || true)"
  if [[ -n "$other" ]]; then
    ts "STOP: another UMA/fairchem-like Python process is running:"
    printf '%s\n' "$other"
    return 1
  fi
  local compute_apps
  compute_apps="$(nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory \
    --format=csv,noheader,nounits 2>/dev/null || true)"
  if [[ -n "$compute_apps" ]]; then
    ts "STOP: the GPU already has compute processes. Do not overlap UMA/QE/MLIP jobs."
    printf '%s\n' "$compute_apps"
    return 1
  fi
  nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu \
    --format=csv,noheader
}

run_stage(){
  local stage="$1"
  shift
  ts "stage=$stage model=$UMA_MODEL task=$UMA_TASK out=$RUN_OUT"
  "$UMA_PY" "$PACKAGE_DIR/scan.py" "$stage" \
    --out "$RUN_OUT" --model "$UMA_MODEL" --task "$UMA_TASK" --device cuda "$@" &
  ACTIVE_CHILD_PID=$!
  local rc=0
  wait "$ACTIVE_CHILD_PID" || rc=$?
  ACTIVE_CHILD_PID=""
  return "$rc"
}

show_status(){
  local rigid=0 relaxed=0
  [[ -d "$RUN_OUT/rigid_records" ]] && rigid="$(find "$RUN_OUT/rigid_records" -maxdepth 1 -name '*.json' | wc -l)"
  [[ -d "$RUN_OUT/relaxed_records" ]] && relaxed="$(find "$RUN_OUT/relaxed_records" -maxdepth 1 -name '*.json' | wc -l)"
  ts "model/task: $UMA_MODEL / $UMA_TASK"
  ts "rigid records: $rigid / 147"
  ts "relaxed records: $relaxed / 20"
  if [[ -s "$RUN_OUT/RESULTS.md" ]]; then
    printf '\n'
    sed -n '1,120p' "$RUN_OUT/RESULTS.md"
  elif [[ -s "$RUN_OUT/PILOT.json" ]]; then
    ts "pilot exists; full screen has not produced RESULTS.md yet"
  else
    ts "no pilot result yet"
  fi
  nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader || true
}

prepare_vasp(){
  local scope="$1" target="$OUT/vasp_${1}"
  [[ -s "$RUN_OUT/DFT_HANDOFF.json" ]] || {
    ts "STOP: UMA DFT_HANDOFF.json is missing; finish './run.sh screen' first."
    return 1
  }
  "$UMA_PY" "$PACKAGE_DIR/vasp_stage.py" prepare \
    --uma-out "$RUN_OUT" --vasp-out "$target" --scope "$scope"
  ts "VASP $scope package ready: $target"
  ts "Read: $target/VASP_README_KO.md"
}

case "$MODE" in
  check)
    verify_package
    check_python
    check_exclusive_gpu
    ts "CHECK OK"
    ts "output root: $OUT"
    ;;
  plan)
    verify_package
    check_python
    prepare_model_cache_manifest
    run_stage plan
    ;;
  pilot)
    verify_package
    check_python
    check_exclusive_gpu
    prepare_model_cache_manifest
    run_stage plan
    run_stage pilot --fmax "${FMAX:-0.05}" --pilot-steps "${PILOT_STEPS:-2}"
    ts "PILOT OK. Return PILOT.json and the log before starting the full screen."
    ;;
  screen)
    verify_package
    check_python
    check_exclusive_gpu
    prepare_model_cache_manifest
    [[ -s "$RUN_OUT/PILOT.json" ]] || {
      ts "STOP: run './run.sh pilot' first and review PILOT.json."
      exit 4
    }
    "$UMA_PY" - "$RUN_OUT/PILOT.json" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
if not p.get("ok"):
    raise SystemExit("PILOT.json is not OK")
PY
    run_stage rigid
    run_stage relax --fmax "${FMAX:-0.05}" --steps "${STEPS:-200}"
    run_stage report --fmax "${FMAX:-0.05}" --steps "${STEPS:-200}"
    ts "SCREEN COMPLETE: $RUN_OUT/RESULTS.md"
    ;;
  report)
    verify_package
    check_python
    prepare_model_cache_manifest
    run_stage report --fmax "${FMAX:-0.05}" --steps "${STEPS:-200}"
    ;;
  vasp-pilot)
    verify_package
    check_python
    prepare_vasp pilot
    ;;
  vasp-all)
    verify_package
    check_python
    prepare_vasp all
    ;;
  status)
    show_status
    ;;
  *)
    echo "Usage: $0 {check|plan|pilot|screen|report|status|vasp-pilot|vasp-all}" >&2
    echo "Optional env: UMA_PY, UMA_MODEL, UMA_TASK, OUT, FMAX, STEPS, PILOT_STEPS" >&2
    exit 2
    ;;
esac
