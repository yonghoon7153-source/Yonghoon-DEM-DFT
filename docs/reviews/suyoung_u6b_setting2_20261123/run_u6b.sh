#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# -eq 2 ]] || exit 2
case "$1" in CHECK_ONLY|GO_SUYOUNG_U6B_SETTING2_ONCE) mode=$1 ;; *) exit 2 ;; esac
pkg=$(pwd -P)
gate=$(realpath -e -- "$2")
sha256sum --status --strict --check SOURCE_SHA256SUMS
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cpu=$("$py" -I -B -c 'import os; print(min(os.sched_getaffinity(0)))')
pyrun=(taskset -c "$cpu" "$py" -I -B)
"${pyrun[@]}" -c 'import os,sys,numpy; assert len(os.sched_getaffinity(0)) == 1 and sys.version_info[:3] == (3,12,3) and numpy.__version__ == "2.5.2"'
app=("${pyrun[@]}" "$pkg/docs/reviews/suyoung_u6b_setting2_20261123/setting2_u6b.py")
inputs=(--root "$pkg" --gate "$gate")
"${app[@]}" check "${inputs[@]}"
pin=$(cat RELEASE)
if [[ "$mode" == CHECK_ONLY ]]; then printf 'CHECK_OK\nRELEASE=%s\n' "$pin"; exit 0; fi
once="$HOME/suyoung_u6b_setting2_once_${pin:0:12}"
mkdir -- "$once" || { printf 'ALREADY_RESERVED %s\n' "$once" >&2; exit 2; }
work=$(mktemp -d "$HOME/suyoung_u6b_setting2_work_XXXXXXXX")
run="$work/run"
mkdir -- "$run"
ret=$(mktemp -d "$HOME/suyoung_u6b_setting2_return_XXXXXXXX")
printf 'RELEASE=%s\nWORK_DIRECTORY=%s\nRETURN_DIRECTORY=%s\n' "$pin" "$run" "$ret" | tee "$once/receipt.txt"
phase=INIT
screen="$run/screen.txt"
finish() {
    local rc=$?
    trap - EXIT HUP INT TERM
    set +e
    if (( rc != 0 )); then
        printf '{"phase":"%s","rc":%d,"status":"INCOMPLETE","label":"DEVELOPMENT_ONLY"}\n' "$phase" "$rc" > "$run/operator_incomplete.json"
    fi
    printf 'COMMAND_RC=%d\n' "$rc" | tee -a "$screen"
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_u6b_setting2_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_u6b_setting2_result.tar.gz screen.txt > SHA256SUMS &&
       sha256sum --strict --check SHA256SUMS && cat SHA256SUMS) ||
    { printf 'ARCHIVE_INCOMPLETE WORK_DIRECTORY=%s\n' "$run"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
printf 'DEVELOPMENT_ONLY\nGATE=U6(b)\nSETTING=2\nRELEASE=%s\nCPU=%s\nAUTOMATIC_RETRIES=0\n' "$pin" "$cpu" | tee "$screen"
cp -- RELEASE SOURCE_SHA256SUMS "$run/"
printf 'grid\tstart_utc\telapsed_s\tprocess_rc\twatchdog_status\n' > "$run/arm_status.tsv"
for cells in 8 12 16 24; do
    phase=S$cells
    case "$cells" in 8) budget=1800 ;; 12) budget=3600 ;; 16) budget=5400 ;; 24) budget=14400 ;; esac
    start=$(date -u +%FT%TZ)
    since=$SECONDS
    printf '%s_BEGIN=%s\n' "$phase" "$start" | tee -a "$screen"
    armrc=0
    timeout --kill-after=5s "$((budget+30))s" "${app[@]}" arm "${inputs[@]}" --run "$run" --cells "$cells" > "$run/$phase.log" 2>&1 || armrc=$?
    watchdog=none
    case "$armrc" in 124) watchdog=timeout ;; 137) watchdog=killed_reason_unconfirmed ;; esac
    printf '%s\t%s\t%d\t%d\t%s\n' "$cells" "$start" "$((SECONDS-since))" "$armrc" "$watchdog" >> "$run/arm_status.tsv"
    printf '%s_RC=%d\n' "$phase" "$armrc" | tee -a "$screen"
    if (( armrc != 0 )); then tail -n 4 "$run/$phase.log"; exit "$armrc"; fi
done
phase=SUMMARY
sha256sum --status --strict --check SOURCE_SHA256SUMS
"${app[@]}" summary "${inputs[@]}" --run "$run" | tee "$run/summary.log"
[[ -s "$run/summary.json" ]]
printf 'SETTING2_U6B_COMPARISON_WRITTEN\n' | tee -a "$screen"
