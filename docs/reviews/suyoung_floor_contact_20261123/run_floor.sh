#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -lt 1 || $# -gt 2 ]]; then echo 'CHECK_ONLY or GO_SUYOUNG_FLOOR_PREFIX_ONCE [cross-return.tar.gz]' >&2; exit 2; fi
case "$1" in CHECK_ONLY|GO_SUYOUNG_FLOOR_PREFIX_ONCE) mode=$1 ;; *) exit 2 ;; esac
pkg=$(pwd -P)
cross=4bb6fe0cdff8964c6bf02cfbf3f9dd9f7bdec5199cfddce0e3d8160b0dd4f391
prior=${2:-${SUYOUNG_CROSS_RETURN:-}}
if [[ -z "$prior" ]]; then
    for file in "$HOME"/suyoung_wall_cross_return_*/suyoung_wall_cross_result.tar.gz; do
        if [[ -f "$file" && $(sha256sum < "$file") == "$cross  -" ]]; then prior=$file; break; fi
    done
fi
[[ -n "$prior" && -f "$prior" ]] || { echo 'Provide the original suyoung_wall_cross_result.tar.gz as the second argument.' >&2; exit 2; }
prior=$(realpath -e -- "$prior")
sha256sum --check --strict --status SOURCE_SHA256SUMS
pin=$(cat RELEASE)
[[ "$pin" =~ ^[0-9a-f]{40}$ ]]
review="$pkg/docs/reviews/suyoung_floor_contact_20261123"
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
[[ -x "$py" ]] || { echo 'Project WSL venv missing.' >&2; exit 2; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cpu=$("$py" -I -B -c 'import os; print(min(os.sched_getaffinity(0)))')
runner=(taskset -c "$cpu" "$py" -I -B)
"${runner[@]}" -c 'import sys,os,numpy; assert sys.version_info[:3]==(3,12,3) and numpy.__version__=="2.5.2" and len(os.sched_getaffinity(0))==1, "reference WSL runtime mismatch"'
common=(--root "$pkg" --prior "$prior")
app=("${runner[@]}" "$review/floor_operator.py")
"${app[@]}" check "${common[@]}"
if [[ "$mode" == CHECK_ONLY ]]; then printf 'CHECK_OK\nRELEASE=%s\n' "$pin"; exit 0; fi
once="$HOME/suyoung_floor_prefix_once_${pin:0:12}"
mkdir -- "$once" || { echo "This release already has an attempt. See $once." >&2; exit 2; }
work=$(mktemp -d "$HOME/suyoung_floor_prefix_work_XXXXXXXX")
ret=$(mktemp -d "$HOME/suyoung_floor_prefix_return_XXXXXXXX")
run="$work/run"
mkdir -p -- "$run/candidate"
screen="$run/screen.txt"
printf 'RELEASE=%s\nRETURN_DIRECTORY=%s\nWORK_DIRECTORY=%s\n' "$pin" "$ret" "$work" > "$once/receipt.txt"
phase=IMPORT
printf 'DEVELOPMENT_ONLY\nRELEASE=%s\nCPU=%s\nHARD_LIMIT_SECONDS_PER_ARM=600\nRETRIES=0\n' "$pin" "$cpu" | tee "$screen"
finish() {
    local rc=$?
    trap - EXIT INT HUP TERM
    set +e
    if (( rc != 0 )); then
        printf '{"status":"INCOMPLETE","phase":"%s","rc":%d,"u6_qualified":false,"stage3_go":false}\n' "$phase" "$rc" > "$run/incomplete.json"
    fi
    printf 'COMMAND_RC=%d\n' "$rc" | tee -a "$screen"
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_floor_prefix_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_floor_prefix_result.tar.gz screen.txt > SHA256SUMS &&
     sha256sum --check --strict SHA256SUMS && cat SHA256SUMS) ||
    { printf 'ARCHIVE_INCOMPLETE WORK_DIRECTORY=%s\n' "$work"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
cp -- SOURCE_SHA256SUMS RELEASE "$run/"
common+=(--run "$run")
"${app[@]}" import-original "${common[@]}"
for cells in 8 16; do
    phase="F$cells"
    rc=0
    printf '%s_BEGIN=%s\n' "$phase" "$(date -u +%FT%TZ)" | tee -a "$screen"
    timeout --signal=KILL 600s "${app[@]}" arm "${common[@]}" --cells "$cells" > "$run/$phase.log" 2>&1 || rc=$?
    printf '%s_RC=%d\n' "$phase" "$rc" | tee -a "$screen"
    if (( rc != 0 )); then tail -n 3 -- "$run/$phase.log"; exit "$rc"; fi
done
phase=READBACK
sha256sum --check --strict --status SOURCE_SHA256SUMS
"${app[@]}" table "${common[@]}"
phase=FIGURE
"${runner[@]}" "$review/render_weekly.py" --csv "$run/pressure_displacement.csv" --png "$run/weekly_pressure_displacement.png"
phase=SEAL
"${app[@]}" seal "${common[@]}"
"${app[@]}" verify "${common[@]}"
echo FOUR_NATIVE_CURVES_AND_WEEKLY_PNG_OK | tee -a "$screen"
