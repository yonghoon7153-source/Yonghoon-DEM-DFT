#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# == 2 ]] || exit 2
case "$1" in CHECK_ONLY|GO_SUYOUNG_F32_F48_ONCE) ;; *) exit 2 ;; esac
root=$(pwd -P)
prior=$(realpath -e -- "$2")
sha256sum --strict --status --check SOURCE_SHA256SUMS
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cpu=$("$py" -I -B -c 'import os; print(min(os.sched_getaffinity(0)))')
python=(taskset -c "$cpu" "$py" -I -X utf8 -B)
"${python[@]}" -c 'import sys,os,numpy; assert sys.version_info[:3]==(3,12,3) and numpy.__version__=="2.5.2" and len(os.sched_getaffinity(0))==1'
app=("${python[@]}" "$root/higher.py")
pin=$(cat RELEASE)
printf 'RELEASE=%s\nPHYSICS=eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112\n' "$pin"
"${app[@]}" check "$root" "$prior"
if [[ $1 == CHECK_ONLY ]]; then echo CHECK_ONLY_OK; exit 0; fi
once="$HOME/suyoung_highgrid_1124_once_${pin:0:12}"
mkdir -- "$once" || { echo "ALREADY_RESERVED $once"; exit 2; }
work=$(mktemp -d "$HOME/suyoung_highgrid_work_XXXXXXXX")
ret=$(mktemp -d "$HOME/suyoung_highgrid_return_XXXXXXXX")
run="$work/run"
mkdir -- "$run"
screen="$run/screen.txt"
printf 'WORK_DIRECTORY=%s\nRETURN_DIRECTORY=%s\n' "$run" "$ret" | tee "$once/receipt.txt"
phase=INIT
finish() {
    rc=$?
    trap - EXIT HUP INT TERM
    set +e
    if (( rc != 0 )); then printf '{"label":"DEVELOPMENT_ONLY","phase":"%s","rc":%d,"status":"INCOMPLETE"}\n' "$phase" "$rc" > "$run/operator_incomplete.json"; fi
    printf 'COMMAND_RC=%s\n' "$rc" | tee -a "$screen"
    (cd -- "$run" && find . -type f ! -name SHA256SUMS -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS && sha256sum --strict --status -c SHA256SUMS) &&
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_highgrid_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_highgrid_result.tar.gz screen.txt > SHA256SUMS && sha256sum --strict -c SHA256SUMS && cat SHA256SUMS) ||
    { echo "ARCHIVE_INCOMPLETE WORK_DIRECTORY=$run"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
printf 'DEVELOPMENT_ONLY\nCPU=%s\nRELEASE=%s\nRETRIES=0\nF32_BUDGET_SECONDS=14400\nF48_BUDGET_SECONDS=57600\n' "$cpu" "$pin" | tee "$screen"
cp -- RELEASE SOURCE_SHA256SUMS "$run/"
printf 'grid\tstart_utc\telapsed_s\trc\n' > "$run/arm_status.tsv"
for n in 32 48; do
    phase="F$n"
    if [[ $n == 32 ]]; then wall=14400; else wall=57600; fi
    start=$(date -u +%FT%TZ)
    since=$SECONDS
    printf '%s_BEGIN=%s\n' "$phase" "$start" | tee -a "$screen"
    rc=0
    timeout --kill-after=5s "$((wall+30))s" "${app[@]}" arm "$root" "$prior" --run "$run" --cells "$n" > "$run/$phase.log" 2>&1 || rc=$?
    printf '%s\t%s\t%d\t%d\n' "$n" "$start" "$((SECONDS-since))" "$rc" >> "$run/arm_status.tsv"
    printf '%s_RC=%d\n' "$phase" "$rc" | tee -a "$screen"
    if (( rc != 0 )); then tail -n 5 "$run/$phase.log"; exit "$rc"; fi
done
phase=SUMMARY
sha256sum --strict --status --check SOURCE_SHA256SUMS
"${app[@]}" summary "$root" "$prior" --run "$run" | tee "$run/summary.log"
echo 'HIGHER_PAIRS_DEVELOPMENT_READBACK_COMPLETE' | tee -a "$screen"
