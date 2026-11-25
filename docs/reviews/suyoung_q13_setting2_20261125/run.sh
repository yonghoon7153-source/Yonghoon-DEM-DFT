#!/usr/bin/env bash
set -euo pipefail
umask 077
root=$(pwd -P)
mode=$1
shift
if [[ $mode == READBACK ]]; then
    [[ $# -ge 1 ]] || { echo 'READBACK expects return directory'; exit 2; }
    received=$(realpath -e -- "$1")
    shift
fi
[[ $# == 0 || $# == 2 ]] || { echo 'Supply both original return directories or neither'; exit 2; }
sdir=$(realpath -e -- "${1:-$HOME/suyoung_u6b_setting2_return_tdofg9lp}")
fdir=$(realpath -e -- "${2:-$HOME/suyoung_u6a_setting2_return_wI741Tvz}")
sha256sum --strict --status -c SOURCE_SHA256SUMS
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python=("$py" -I -X utf8 -B)
"${python[@]}" -c 'import numpy,sys; assert sys.version_info[:3]==(3,12,3) and numpy.__version__=="2.5.2"'
pin=$(cat RELEASE)
if [[ $mode == READBACK ]]; then
    temp=$(mktemp -d)
    "${python[@]}" coordinate.py unpack "$received" "$temp"
    "${python[@]}" q13.py replay "$root" "$sdir" "$fdir" --run "$temp/run"
    exit
fi
"${python[@]}" coordinate.py cores
"${python[@]}" q13.py check "$root" "$sdir" "$fdir"
if [[ $mode == CHECK_ONLY ]]; then echo CHECK_ONLY_OK; exit 0; fi
[[ $mode == GO_SUYOUNG_Q13_PAIR_ONCE ]] || exit 2
once="$HOME/suyoung_q13_setting2_1125_once"
mkdir -- "$once" || { echo "ALREADY_RESERVED $once"; exit 2; }
work=$(mktemp -d "$HOME/suyoung_q13_pair_work_XXXXXXXX")
ret=$(mktemp -d "$HOME/suyoung_q13_pair_return_XXXXXXXX")
run="$work/run"
mkdir "$run"
screen="$run/screen.txt"
printf 'RELEASE=%s\nWORK_DIRECTORY=%s\nRETURN_DIRECTORY=%s\n' "$pin" "$run" "$ret" | tee "$once/receipt.txt" "$screen"
cp -- RELEASE SOURCE_SHA256SUMS "$run/"
phase=PAIR
finish() {
    rc=$?
    trap - EXIT INT TERM HUP
    set +e
    if (( rc != 0 )); then printf '{"status":"TECHNICAL_INCOMPLETE","phase":"%s","rc":%d}\n' "$phase" "$rc" > "$run/incomplete.json"; fi
    printf 'COMMAND_RC=%s\n' "$rc" | tee -a "$screen"
    (cd -- "$run" && find . -type f ! -path './SHA256SUMS' -printf '%P\0' | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS && sha256sum --strict --status -c SHA256SUMS) &&
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_q13_pair_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_q13_pair_result.tar.gz screen.txt > SHA256SUMS && sha256sum --strict -c SHA256SUMS && cat SHA256SUMS) ||
    { echo "ARCHIVE_INCOMPLETE WORK_DIRECTORY=$run"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
echo 'DEVELOPMENT_ONLY S36 F36 PARALLEL THREADS_PER_ARM=1 AUTOMATIC_RETRIES=0' | tee -a "$screen"
"${python[@]}" coordinate.py pair "$root" "$run" "$sdir" "$fdir" | tee -a "$screen"
phase=SUMMARY
sha256sum --strict --status -c SOURCE_SHA256SUMS
"${python[@]}" q13.py summary "$root" "$sdir" "$fdir" --run "$run" | tee -a "$screen"
echo Q13_PAIR_READBACK_COMPLETE | tee -a "$screen"
